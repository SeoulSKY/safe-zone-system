import 'react-native-url-polyfill/auto';

import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'
import { NavigationContainer } from '@react-navigation/native'
import { Ionicons } from '@expo/vector-icons';
import { HomeScreen, MibScreen, MibsCreateScreen } from '@/screens/index'

const Tab = createBottomTabNavigator()

/**
 * The Base Application.
 * Handles higher level navigation within the app.
 */
export default function App() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route, navigation }) => ({
          tabBarShowLabel: false,
          tabBarIcon: ({ focused, color, size }) => {
            let iconName: React.ComponentProps<typeof Ionicons>["name"] = "home";

            if (route.name === "Home") {
              iconName = focused ? "home" : "home-outline";
            } 
            else if (route.name === "Message in a Bottle") {
              iconName = focused ? "mail" : "mail-outline";
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: "dodgerblue",
          tabBarInactiveTintColor: "grey",
        })}
      >
        <Tab.Screen
          name="Home"
          component={HomeScreen}
          options={{ headerShown: true }}
        />
        <Tab.Screen
          name="Message in a Bottle"
          component={MibScreen}
          options={{ 
            headerShown: true,
            headerStyle: {
              elevation: 0,
              shadowOpacity: 0,
              borderBottomWidth: 0,
            }
          }}
        />
        <Tab.Screen
          name="Create Message in a Bottle"
          component={MibsCreateScreen}
          options={{
            tabBarButton: () => null,
            tabBarVisible: false,
          }}
      />
      </Tab.Navigator>
      <StatusBar style="auto" />
    </NavigationContainer>
  );
}
