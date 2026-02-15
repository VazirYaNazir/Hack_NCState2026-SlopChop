from __future__ import annotations

import os
import re
import sys
import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
import tweepy as tw
from dotenv import load_dotenv, find_dotenv

_TWEET_CACHE: Dict[str, Tuple[float, List[Dict[str, Any]]]] = {}
_TWEET_CACHE_TTL_S = 20 * 60

dotenv_path = find_dotenv(usecwd=True)
if dotenv_path:
    load_dotenv(dotenv_path, override=True)
else:
    ROOT = Path(__file__).resolve().parents[2]
    load_dotenv(ROOT / ".env", override=True)

THIS_DIR = Path(__file__).resolve().parent
PARENT_DIR = THIS_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from ai_engine import get_ai_image_probability, scan_post_caption  # type: ignore

TRENDS_RSS_URL = "https://trends.google.com/trending/rss"
DEFAULT_UA = "HackNC-State2026/1.0 (contact: you@example.com)"
HT_NS = "https://trends.google.com/trending/rss"
NS = {"ht": HT_NS}

X_BEARER = os.getenv("X_BEARER_TOKEN") or os.getenv("BEARER_TOKEN") or os.getenv("bear")

client_v2 = tw.Client(bearer_token=X_BEARER, wait_on_rate_limit=True) if X_BEARER else None

_IMG_PROB_CACHE: Dict[str, float] = {}
_CAPTION_SCAN_CACHE: Dict[str, Tuple[int, str]] = {}


def _obj_to_dict(o: Any) -> Dict[str, Any]:
    """Convert Tweepy model objects into a plain dict safely."""
    if o is None:
        return {}
    if isinstance(o, dict):
        return o
    if hasattr(o, "data") and isinstance(getattr(o, "data"), dict):
        return o.data
    return {}


def _is_probably_english(s: str) -> bool:
    """Cheap filter to keep output English-ish."""
    if not s:
        return True
    if re.search(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]", s):
        return False
    non_ascii = sum(1 for ch in s if ord(ch) > 127)
    if non_ascii == 0:
        return True
    return (non_ascii / max(len(s), 1)) <= 0.10


def _normalize_scan_result(scan_result: Any) -> Tuple[int, str]:
    """
    Normalize scan_post_caption output -> (risk_score 0..100, flag).
    """
    risk_score = 0
    flag = "Pending"
    if isinstance(scan_result, dict):
        risk_score = int(scan_result.get("risk_score", scan_result.get("risk", 0)) or 0)
        flag = str(scan_result.get("flag", scan_result.get("label", "Pending")) or "Pending")
    elif isinstance(scan_result, (int, float)):
        risk_score = int(scan_result)

    return max(0, min(100, risk_score)), flag


def _ai_prob_for_url(image_url: str) -> float:
    """Call your image detector with caching; clamp [0,1]."""
    if image_url in _IMG_PROB_CACHE:
        return _IMG_PROB_CACHE[image_url]
    try:
        p = float(get_ai_image_probability(image_url))
    except Exception:
        p = 0.0
    p = max(0.0, min(1.0, p))
    _IMG_PROB_CACHE[image_url] = p
    return p


def _scan_caption(caption: str) -> Tuple[int, str]:
    """Call your caption scanner with caching."""
    if caption in _CAPTION_SCAN_CACHE:
        return _CAPTION_SCAN_CACHE[caption]
    try:
        res = scan_post_caption(caption)
    except Exception:
        res = {}
    out = _normalize_scan_result(res)
    _CAPTION_SCAN_CACHE[caption] = out
    return out

def get_google_trend_topics(geo: str = "US", limit: int = 10) -> Dict[str, Any]:
    """
    Fetch Google Trends RSS and return titles (topics) in your preferred style.
    """
    headers = {
        "User-Agent": os.getenv("USER_AGENT", DEFAULT_UA),
        "Accept": "application/rss+xml, application/xml, text/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    r = requests.get(
        TRENDS_RSS_URL,
        params={"geo": geo.upper().strip(), "hl": "en-US"},
        headers=headers,
        timeout=15,
    )
    r.raise_for_status()

    root = ET.fromstring(r.text)
    channel = root.find("channel")

    updated = None
    if channel is not None:
        updated = (channel.findtext("lastBuildDate") or channel.findtext("pubDate") or None)
        if updated:
            updated = updated.strip()

    trends: List[Dict[str, Any]] = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        published = (item.findtext("pubDate") or "").strip() or None

        if not _is_probably_english(title):
            continue

        trends.append({"title": title, "link": link, "published": published})
        if len(trends) >= limit:
            break

    return {"geo": geo.upper().strip(), "updated": updated, "count": len(trends), "trends": trends}

def _topic_query_variants(topic: str) -> List[str]:
    """
    Create query variants from strict -> loose.
    We still FILTER for media in code, so the query can be looser.
    """
    t = (topic or "").strip()
    if not t:
        return []

    t_clean = re.sub(r"[^\w\s#@-]", " ", t).strip()
    t_clean = re.sub(r"\s+", " ", t_clean)

    phrase = f"\"{t_clean}\"" if " " in t_clean else t_clean

    return [
        f"{phrase} has:images lang:en -is:retweet",
        f"{t_clean} has:images lang:en -is:retweet",
        f"{phrase} has:images -is:retweet",
        f"{t_clean} has:images -is:retweet",
        f"{phrase} has:media lang:en -is:retweet",
        f"{t_clean} has:media lang:en -is:retweet",
        f"{phrase} lang:en -is:retweet",
        f"{t_clean} lang:en -is:retweet",
    ]


def search_x_tweets_with_media(topic: str, per_topic: int = 2) -> List[Dict[str, Any]]:
    """
    Return up to `per_topic` REAL tweets that contain media for a topic.

    - No fake x.com/search fallbacks.
    - On transient failures, returns cached last-good results for this topic (if any).
    """
    if client_v2 is None:
        return []

    now = time.time()

    cached = _TWEET_CACHE.get(topic)
    if cached and (now - cached[0] < _TWEET_CACHE_TTL_S) and cached[1]:
        return cached[1][:per_topic]

    last_error: Optional[Exception] = None

    for q in _topic_query_variants(topic):
        for attempt in range(3):
            try:
                resp = client_v2.search_recent_tweets(
                    query=q,
                    max_results=25,
                    expansions=["attachments.media_keys", "author_id"],
                    tweet_fields=["public_metrics", "attachments", "lang"],
                    user_fields=["username"],
                    media_fields=["url", "preview_image_url", "type", "media_key"],
                )
                break
            except tw.errors.TooManyRequests as e:
                last_error = e
                if cached and cached[1]:
                    return cached[1][:per_topic]
                raise
            except (tw.errors.Unauthorized, tw.errors.Forbidden) as e:
                raise
            except Exception as e:
                last_error = e
                if attempt == 2:
                    resp = None
                else:
                    continue

        if resp is None:
            continue

        tweets = resp.data or []
        includes = resp.includes or {}

        users = {u.id: _obj_to_dict(u) for u in (includes.get("users") or [])}

        media_by_key: Dict[str, Dict[str, Any]] = {}
        for m in (includes.get("media") or []):
            md = _obj_to_dict(m)
            mk = md.get("media_key")
            if mk:
                media_by_key[mk] = md

        out: List[Dict[str, Any]] = []

        for twt in tweets:
            td = _obj_to_dict(twt)
            tid = td.get("id")
            text = (td.get("text") or "").strip()

            if text and not _is_probably_english(text):
                continue

            attachments = td.get("attachments") or {}
            media_keys = attachments.get("media_keys") or []
            if not media_keys:
                continue

            image_url = None

            for mk in media_keys:
                md = media_by_key.get(mk) or {}
                if (md.get("type") or "").lower() == "photo" and md.get("url"):
                    image_url = md["url"]
                    break

            if not image_url:
                for mk in media_keys:
                    md = media_by_key.get(mk) or {}
                    image_url = md.get("url") or md.get("preview_image_url")
                    if image_url:
                        break

            if not image_url:
                continue

            author_id = td.get("author_id")
            username = (users.get(author_id, {}) or {}).get("username") or "unknown"

            metrics = td.get("public_metrics") or {}
            like_count = int(metrics.get("like_count") or 0)

            out.append(
                {
                    "id": str(tid),
                    "username": username,
                    "image_url": image_url,
                    "caption": text or topic,
                    "likes": like_count,
                }
            )

            if len(out) >= per_topic:
                break

        if out:
            _TWEET_CACHE[topic] = (now, out)
            return out[:per_topic]

    if cached and cached[1]:
        return cached[1][:per_topic]

    if last_error:
        raise last_error

    return []

def get_posts_from_trends_as_real_tweets(
    geo: str = "US",
    trends_count: int = 10,
    tweets_per_trend: int = 1,
) -> Dict[str, Any]:
    """
    Returns:
      {
        "geo": "...",
        "updated": ...,
        "count": N,
        "posts": [ {id, username, image_url, caption, likes, risk_score, ai_image_probability, flag}, ...]
      }
    """
    trends_payload = get_google_trend_topics(geo=geo, limit=trends_count)

    posts: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()

    for ev in trends_payload["trends"]:
        topic = ev["title"]
        hits = search_x_tweets_with_media(topic, per_topic=tweets_per_trend)

        for h in hits:
            tid = h["id"]
            if tid in seen_ids:
                continue
            seen_ids.add(tid)

            image_url = h["image_url"]
            caption = h["caption"]

            ai_prob = _ai_prob_for_url(image_url)
            risk_score, flag = _scan_caption(caption)

            
            risk_score = max(risk_score, int(round(ai_prob * 100)))

            posts.append(
                {
                    "id": tid,
                    "username": h["username"],
                    "image_url": image_url,
                    "caption": caption,
                    "likes": int(h["likes"]),
                    "risk_score": risk_score,
                    "ai_image_probability": ai_prob,
                    "flag": flag,
                }
            )

    return {
        "geo": trends_payload["geo"],
        "updated": trends_payload["updated"],
        "count": len(posts),
        "posts": posts,
    }


if __name__ == "__main__":
    out = get_posts_from_trends_as_real_tweets(geo="US", trends_count=10, tweets_per_trend=1)
    print(json.dumps(out, indent=2, ensure_ascii=False))
