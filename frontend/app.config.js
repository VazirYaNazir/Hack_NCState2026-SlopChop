export default {
  expo: {
    name: "vyn",
    slug: "vyn",
    version: "1.0.0",
    orientation: "portrait",
    newArchEnabled: true,
    ios: {
      supportsTablet: true,
      infoPlist: {
        NSLocationWhenInUseUsageDescription: "We need your location to show nearby news and posts."
      }
    },
    android: {
      adaptiveIcon: {
        backgroundColor: "#000000"
      },
      permissions: [
        "ACCESS_COARSE_LOCATION",
        "ACCESS_FINE_LOCATION"
      ]
    },
    extra: {
      apiUrl: process.env.EXPO_PUBLIC_API_URL || "http://localhost:5000"
    }
  }
};