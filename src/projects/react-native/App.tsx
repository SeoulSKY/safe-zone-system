import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { NavigationContainer } from '@react-navigation/native'
import { Ionicons } from '@expo/vector-icons';

import {HomeScreen, MibScreen} from './src/screens'


const Tab = createBottomTabNavigator()

/**
 * The Base Application.
 * Handles higher level navigation within the app.
 */
export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarShowLabel: false,
          tabBarIcon: ({ focused, color, size }) => {
            let iconName: React.ComponentProps<typeof Ionicons>["name"] = "home";

            if (route.name === "Home") {
              iconName = focused ? "home" : "home-outline";
            } 
            else if (route.name === "MIB") {
              iconName = focused ? "mail" : "mail-outline";
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: "cornflowerblue",
          tabBarInactiveTintColor: "grey",
        })}
      >
        <Tab.Screen
          name="Home"
          component={HomeScreen}
          options={{ headerShown: false }}
        />
        <Tab.Screen
          name="MIB"
          component={MibScreen}
          options={{ headerShown: false }}
        />
      </Tab.Navigator>
      <StatusBar style="auto" />
    </NavigationContainer>
  );
}
