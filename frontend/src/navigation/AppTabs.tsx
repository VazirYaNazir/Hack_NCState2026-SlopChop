import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Colors } from "../theme/colors";
import { HomeScreen } from "../screens/HomeScreen";
import ProfileScreen from "../screens/ProfileScreen";

const Tab = createBottomTabNavigator();

export function AppTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: Colors.black },
        headerTintColor: Colors.white,
        headerTitleStyle: { color: Colors.white },

        tabBarStyle: {
          backgroundColor: Colors.black,
          borderTopColor: Colors.gray500,
        },
        tabBarActiveTintColor: Colors.white,
        tabBarInactiveTintColor: Colors.gray500,
      }}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}
