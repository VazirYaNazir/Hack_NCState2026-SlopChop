import React, { useState, useEffect } from 'react';
import { View, ScrollView, StyleSheet, ActivityIndicator, Dimensions, Text, Switch, Image } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as Location from 'expo-location';
import axios from 'axios';

const { width } = Dimensions.get('window');
const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000';

export default function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState(null);
  const [demoMode, setDemoMode] = useState(true);

  useEffect(() => {
    getLocationAndLoadData();
  }, [demoMode]);

  const getLocationAndLoadData = async () => {
    setLoading(true);
    
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        console.log('Permission denied');
        loadData();
        return;
      }

      let currentLocation = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.Balanced,
      });

      const locationData = {
        latitude: currentLocation.coords.latitude,
        longitude: currentLocation.coords.longitude,
        accuracy: currentLocation.coords.accuracy,
      };

      console.log('Got location:', locationData);
      setLocation(locationData);

      try {
        await axios.post(`${API_URL}/api/submit-location`, locationData);
        console.log('Location sent');
      } catch (error) {
        console.log('Could not send location:', error.message);
      }

      loadData(locationData.latitude, locationData.longitude);

    } catch (error) {
      console.error('Location error:', error);
      loadData();
    }
  };

  const loadData = async (lat = null, lon = null) => {
    try {
      if (demoMode) {
        console.log('🎭 Loading analyzed demo feed...');
        const response = await axios.get(`${API_URL}/api/feed`, {
          timeout: 10000
        });
        console.log('Demo feed loaded:', response.data);
        setPosts(response.data || []);
      } else {
        console.log('📍 Loading real news...');
        const response = await axios.get(`${API_URL}/api/news`, {
          params: { lat, lon },
          timeout: 10000
        });
        setPosts(response.data.news || []);
      }
    } catch (error) {
      console.log('Error loading data:', error.message);
      setPosts([]);
    } finally {
      setLoading(false);
    }
  };

  const toggleDemoMode = (value) => {
    setDemoMode(value);
  };

  if (loading) {
    return (
      <View style={styles.centerContent}>
        <StatusBar style="light" />
        <ActivityIndicator size="large" color="#0a84ff" />
        <Text style={styles.loadingText}>
          {demoMode ? 'Analyzing demo posts...' : 'Loading news...'}
        </Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar style="light" />

      {/* Demo Mode Toggle */}
      <View style={styles.demoBar}>
        <Text style={styles.demoText}>
          {demoMode ? 'Demo Feed' : 'Live News'}
        </Text>
        <Switch
          value={demoMode}
          onValueChange={toggleDemoMode}
          trackColor={{ false: '#3a3a3a', true: '#0a84ff' }}
          thumbColor={demoMode ? '#fff' : '#f4f3f4'}
        />
      </View>
      
      <ScrollView 
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {posts.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={styles.emptyText}>No posts available</Text>
          </View>
        ) : (
          posts.map((post) => (
            <View key={post.id} style={styles.postCard}>
              {/* Post Header */}
              <View style={styles.postHeader}>
                <Text style={styles.username}>@{post.username}</Text>
                <View style={[
                  styles.flagBadge,
                  post.flag === 'SCAM DETECTED' && styles.flagScam,
                  post.flag === 'Suspicious' && styles.flagSuspicious,
                  post.flag === 'Safe' && styles.flagSafe,
                  post.flag === 'Pending' && styles.flagPending,
                ]}>
                  <Text style={styles.flagText}>{post.flag}</Text>
                </View>
              </View>
              
              {/* Post Image */}
              {post.image_url && (
                <Image 
                  source={{ uri: post.image_url }}
                  style={styles.postImage}
                  resizeMode="cover"
                />
              )}
              
              {/* Caption */}
              <Text style={styles.caption}>
                {post.caption}
              </Text>
              
              {/* Footer with Likes and Risk Score */}
              <View style={styles.postFooter}>
                <Text style={styles.likes}>❤️ {post.likes?.toLocaleString()}</Text>
                <Text style={[
                  styles.riskScore,
                  post.risk_score > 75 && styles.riskHigh,
                  post.risk_score > 40 && post.risk_score <= 75 && styles.riskMedium,
                  post.risk_score <= 40 && styles.riskLow,
                ]}>
                  {post.risk_score >= 0 ? `Risk: ${post.risk_score}%` : 'Risk: N/A'}
                </Text>
              </View>

              {/* AI Image Analysis */}
              {post.ai_image_probability > 0 && (
                <Text style={styles.aiProb}>
                  AI Generated: {(post.ai_image_probability * 100).toFixed(1)}%
                </Text>
              )}
            </View>
          ))
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000000',
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#000000',
  },
  loadingText: {
    color: '#fff',
    marginTop: 10,
    fontSize: 14,
  },
  demoBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#1a1a1a',
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginTop: 50,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a2a',
  },
  demoText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  locationBar: {
    backgroundColor: '#1a1a1a',
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#2a2a2a',
  },
  locationText: {
    color: '#0a84ff',
    fontSize: 12,
  },
  scrollView: {
    flex: 1,
  },
  scrollContent: {
    paddingTop: 10,
    paddingBottom: 20,
  },
  emptyState: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    color: '#666',
    fontSize: 16,
  },
  postCard: {
    width: width - 32,
    marginHorizontal: 16,
    marginVertical: 8,
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#2a2a2a',
    overflow: 'hidden',
  },
  postHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 12,
  },
  username: {
    color: '#fff',
    fontSize: 15,
    fontWeight: 'bold',
  },
  flagBadge: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: 6,
  },
  flagScam: {
    backgroundColor: '#ff3b30',
  },
  flagSuspicious: {
    backgroundColor: '#ff9500',
  },
  flagSafe: {
    backgroundColor: '#34c759',
  },
  flagPending: {
    backgroundColor: '#666',
  },
  flagText: {
    color: '#fff',
    fontSize: 11,
    fontWeight: 'bold',
  },
  postImage: {
    width: '100%',
    height: 300,
    backgroundColor: '#2a2a2a',
  },
  caption: {
    color: '#fff',
    fontSize: 14,
    lineHeight: 20,
    padding: 12,
  },
  postFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingBottom: 12,
  },
  likes: {
    color: '#888',
    fontSize: 13,
  },
  riskScore: {
    fontSize: 13,
    fontWeight: 'bold',
  },
  riskHigh: {
    color: '#ff3b30',
  },
  riskMedium: {
    color: '#ff9500',
  },
  riskLow: {
    color: '#34c759',
  },
  aiProb: {
    color: '#888',
    fontSize: 11,
    paddingHorizontal: 12,
    paddingBottom: 12,
  },
});