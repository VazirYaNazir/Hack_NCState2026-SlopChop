from __future__ import annotations

import time
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

import requests
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/trends", tags=["trends"])


_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
"""In-memory cache mapping geo -> (timestamp, payload)."""

CACHE_TTL_SECONDS = 600
"""Cache duration (seconds). Trends refresh ~every ~10 minutes on average. :contentReference[oaicite:2]{index=2}"""


def _fetch_trends_rss_xml(geo: str, hl: str = "en-US") -> str:
    """
    Fetch Google Trends RSS XML for a given geo.

    Args:
        geo: Country/region code used by Google Trends RSS (e.g., "US").
        hl: UI language/locale hint (e.g., "en-US").

    Returns:
        RSS XML response text.

    Raises:
        requests.HTTPError: If the upstream request returns a non-2xx response.
    """
    url = "https://trends.google.com/trending/rss"
    r = requests.get(
        url,
        params={"geo": geo, "hl": hl},
        headers={
            "User-Agent": "HackNCSU2026/1.0 (contact: you@example.com)",
            "Accept": "application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.1",
            "Accept-Language": "en-US,en;q=0.9",
        },
        timeout=10,
    )
    r.raise_for_status()
    return r.text


def _parse_trends_rss(xml_text: str, limit: int) -> Dict[str, Any]:
    """
    Parse Google Trends RSS XML into a JSON-ready payload.

    Args:
        xml_text: RSS XML as string.
        limit: Maximum number of items to include.

    Returns:
        Dict with 'updated' and 'trends' list.
    """
    root = ET.fromstring(xml_text)

    channel = root.find("channel")
    if channel is None:
        return {"updated": None, "trends": []}

    updated = (channel.findtext("lastBuildDate") or channel.findtext("pubDate") or None)

    items: List[Dict[str, Any]] = []
    for item in channel.findall("item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()

        if title:
            items.append({"title": title, "link": link, "published": pub or None})

    return {"updated": updated, "trends": items}


def get_trends_by_geo(geo: str, limit: int = 20) -> Dict[str, Any]:
    """
    Get country-level trends for a geo code, with caching and robust errors.

    Args:
        geo: Country code like "US".
        limit: Number of trends to return.

    Returns:
        JSON-ready dict containing geo, updated, count, and trends.

    Raises:
        HTTPException: For upstream/network issues.
    """
    geo = geo.upper().strip()

    now = time.time()
    cached = _CACHE.get(geo)
    if cached and (now - cached[0] < CACHE_TTL_SECONDS):
        return cached[1]

    try:
        xml_text = _fetch_trends_rss_xml(geo=geo)
        parsed = _parse_trends_rss(xml_text, limit=limit)
        payload = {
            "geo": geo,
            "updated": parsed["updated"],
            "count": len(parsed["trends"]),
            "trends": parsed["trends"],
        }
    except requests.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Google Trends RSS request failed: {str(e)}") from e
    except ET.ParseError as e:
        raise HTTPException(status_code=502, detail="Google Trends RSS returned non-XML or malformed XML.") from e
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Network error fetching Google Trends RSS: {str(e)}") from e

    _CACHE[geo] = (now, payload)
    return payload


def _coords_are_in_us(lat: float, lon: float) -> bool:
    url = "https://geocoding.geo.census.gov/geocoder/geographies/coordinates"
    params = {
        "x": lon,
        "y": lat,
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "format": "json",
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        geos = (((data.get("result") or {}).get("geographies")) or {})
        states = geos.get("States") or []
        return bool(states)
    except Exception:
        return False


@router.get("/by-geo")
def trends_by_geo(
    geo: str = Query(..., description='Country code (e.g., "US", "GB", "IN").'),
    limit: int = Query(20, ge=1, le=50, description="Number of trends to return (1–50)."),
) -> Dict[str, Any]:
    """
    Return country-level Google Trends RSS items for a provided geo code.
    """
    return get_trends_by_geo(geo=geo, limit=limit)


@router.get("/by-coord")
def trends_by_coord(
    lat: float = Query(..., description="Latitude in decimal degrees."),
    lon: float = Query(..., description="Longitude in decimal degrees."),
    limit: int = Query(20, ge=1, le=50, description="Number of trends to return (1–50)."),
) -> Dict[str, Any]:
    """
    Convenience endpoint: if coords are in the US, return US trends.

    If not in the US, this endpoint asks the caller to use /by-geo instead.
    """
    if _coords_are_in_us(lat, lon):
        return get_trends_by_geo(geo="US", limit=limit)

    raise HTTPException(
        status_code=400,
        detail="Coordinates appear to be outside the US (or could not be verified). "
               "Use /trends/by-geo?geo=<COUNTRY_CODE> instead."
    )

print(get_trends_by_geo("US", limit=50))