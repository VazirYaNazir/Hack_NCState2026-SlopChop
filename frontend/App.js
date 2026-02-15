import React, { useState, useEffect } from 'react';
import { View, ScrollView, StyleSheet, ActivityIndicator, Dimensions, Text, Switch, Image, TouchableOpacity, Modal } from 'react-native';
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
  const [lightMode, setLightMode] = useState(false);
  const [settingsVisible, setSettingsVisible] = useState(false);

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
        console.log('Loading analyzed demo feed...');
        const response = await axios.get(`${API_URL}/api/feed`, {
          timeout: 50000
        });
        console.log('Demo feed loaded:', response.data);
        setPosts(response.data || []);
      } else {
        console.log('Loading real news...');

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

  const getTheme = () => {
    if (lightMode) {
      return {
        bg: '#ffffff',
        cardBg: '#f5f5f5',
        text: '#000000',
        subtext: '#666666',
        border: '#e0e0e0',
        headerBg: '#f9f9f9',
      };
    }
    return {
      bg: '#000000',
      cardBg: '#1a1a1a',
      text: '#ffffff',
      subtext: '#888888',
      border: '#2a2a2a',
      headerBg: '#1a1a1a',
    };
  };

  const theme = getTheme();

  if (loading) {
    return (
      <View style={[styles.centerContent, { backgroundColor: theme.bg }]}>
        <StatusBar style={lightMode ? "dark" : "light"} />
        <ActivityIndicator size="large" color="#0a84ff" />
        <Text style={[styles.loadingText, { color: theme.text }]}>
          {demoMode ? 'Analyzing demo posts...' : 'Loading news...'}
        </Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: theme.bg }]}>
      <StatusBar style={lightMode ? "dark" : "light"} />

      <View style={[styles.header, { backgroundColor: theme.headerBg, borderBottomColor: theme.border }]}>
        <Text style={[styles.appTitle, { color: theme.text }]}>
          SlopChop
        </Text>
        <TouchableOpacity 
          onPress={() => setSettingsVisible(true)}
          style={styles.settingsButton}
        >
          <Text style={styles.settingsIcon}>⚙️</Text>
        </TouchableOpacity>
      </View>

      <View style={[styles.demoBar, { backgroundColor: theme.headerBg, borderBottomColor: theme.border }]}>
        <Text style={[styles.demoText, { color: theme.text }]}>
          {demoMode ? 'Demo Feed' : 'Live News'}
        </Text>
        <Switch
          value={demoMode}
          onValueChange={toggleDemoMode}
          trackColor={{ false: '#3a3a3a', true: '#0a84ff' }}
          thumbColor={demoMode ? '#fff' : '#f4f3f4'}
        />
      </View>

      <Modal
        visible={settingsVisible}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setSettingsVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: theme.cardBg }]}>
            <Text style={[styles.modalTitle, { color: theme.text }]}>Settings</Text>
            
            <View style={styles.settingRow}>
              <Text style={[styles.settingLabel, { color: theme.text }]}>Light Mode</Text>
              <Switch
                value={lightMode}
                onValueChange={setLightMode}
                trackColor={{ false: '#3a3a3a', true: '#0a84ff' }}
                thumbColor={lightMode ? '#fff' : '#f4f3f4'}
              />
            </View>

            <TouchableOpacity 
              style={styles.closeButton}
              onPress={() => setSettingsVisible(false)}
            >
              <Text style={styles.closeButtonText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
      
      <ScrollView 
        style={styles.scrollView}
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        {posts.length === 0 ? (
          <View style={styles.emptyState}>
            <Text style={[styles.emptyText, { color: theme.subtext }]}>No posts available</Text>
          </View>
        ) : (
          posts.map((post) => (
            <View key={post.id} style={[styles.postCard, { backgroundColor: theme.cardBg, borderColor: theme.border }]}>
              <View style={styles.postHeader}>
                <Text style={[styles.username, { color: theme.text }]}>@{post.username}</Text>
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
              
              {post.image_url && (
                <Image 
                  source={{ uri: post.image_url }}
                  style={styles.postImage}
                  resizeMode="cover"
                />
              )}
              
              <Text style={[styles.caption, { color: theme.text }]}>
                {post.caption}
              </Text>
              
              <View style={styles.postFooter}>
                <Text style={[styles.likes, { color: theme.subtext }]}>❤️ {post.likes?.toLocaleString()}</Text>
                <Text style={[
                  styles.riskScore,
                  post.risk_score > 75 && styles.riskHigh,
                  post.risk_score > 40 && post.risk_score <= 75 && styles.riskMedium,
                  post.risk_score <= 40 && styles.riskLow,
                ]}>
                  {post.risk_score >= 0 ? `Risk: ${post.risk_score}%` : 'Risk: N/A'}
                </Text>
              </View>

              {post.ai_image_probability > 0 && (
                <Text style={[styles.aiProb, { color: theme.subtext }]}>
                  AI Probability: {(post.ai_image_probability * 100).toFixed(1)}%
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
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 10,
    fontSize: 14,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    marginTop: 50,
    borderBottomWidth: 1,
  },
  appTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  settingsButton: {
    padding: 8,
  },
  settingsIcon: {
    fontSize: 24,
  },
  demoBar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderBottomWidth: 1,
  },
  demoText: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: width - 64,
    borderRadius: 16,
    padding: 24,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  settingRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  settingLabel: {
    fontSize: 16,
  },
  closeButton: {
    backgroundColor: '#0a84ff',
    borderRadius: 8,
    paddingVertical: 12,
    marginTop: 20,
    alignItems: 'center',
  },
  closeButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
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
    fontSize: 16,
  },
  postCard: {
    width: width - 32,
    marginHorizontal: 16,
    marginVertical: 8,
    borderRadius: 12,
    borderWidth: 1,
    overflow: 'hidden',
  },
  postHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 12,
  },
  username: {
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
    fontSize: 11,
    paddingHorizontal: 12,
    paddingBottom: 12,
  },
});