import React, { useState, useEffect } from 'react';
import { View, ScrollView, StyleSheet, ActivityIndicator, Dimensions, Text, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import * as Location from 'expo-location';
import axios from 'axios';

const { width } = Dimensions.get('window');
const API_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:5000';

export default function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [location, setLocation] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  useEffect(() => {
    getLocationAndSendToBackend();
  }, []);

  const getLocationAndSendToBackend = async () => {
    try {
      let { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        console.log('Permission denied');
        loadMockData();
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
        const response = await axios.post(`${API_URL}/api/location`, locationData);
        console.log('Backend response:', response.data);
      } catch (error) {
        console.log('Could not send to backend:', error.message);
      }

      loadNews(locationData.latitude, locationData.longitude);

    } catch (error) {
      console.error('Location error:', error);
      loadMockData();
    }
  };

  const loadNews = async (lat, lon) => {
    try {
      const response = await axios.get(`${API_URL}/api/news`, {
        params: { lat, lon },
        timeout: 5000
      });
      
      setPosts(response.data.news || []);
    } catch (error) {
      console.log('Could not load news:', error.message);
      loadMockData();
    } finally {
      setLoading(false);
    }
  };

  const loadMockData = () => {
    setPosts(Array.from({ length: 10 }, (_, i) => ({
      id: i,
      title: `Post ${i}`,
    })));
    setLoading(false);
  };

  if (loading) {
    return (
      <View style={styles.centerContent}>
        <StatusBar style="light" />
        <ActivityIndicator size="large" color="#0a84ff" />
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar style="light" />

      <ScrollView 
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {posts.map((post) => (
          <View key={post.id} style={styles.postCard}>
            <Text style={styles.postTitle}>{post.title}</Text>
          </View>
        ))}
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
  locationBar: {
    backgroundColor: '#1a1a1a',
    paddingVertical: 8,
    paddingHorizontal: 16,
    marginTop: 50,
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
  postCard: {
    width: width - 32,
    marginHorizontal: 16,
    marginVertical: 8,
    padding: 16,
    backgroundColor: '#1a1a1a',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#2a2a2a',
    height: 180,
    justifyContent: 'center',
  },
  postTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});