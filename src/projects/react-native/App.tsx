import 'react-native-url-polyfill/auto';

import React from 'react';
import {StatusBar} from 'expo-status-bar';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs'
import {NavigationContainer} from '@react-navigation/native'
import {Ionicons} from '@expo/vector-icons';
import {SettingsScreen, MibScreen, MibsCreateScreen} from '@/screens/index'
import {useLogin} from '@/hooks/useLogin';
import {SplashScreen} from '@/screens/SplashScreen';

const Tab = createBottomTabNavigator()

/**
 * The Base Application.
 * 
 * This component handles user authentication and the base level navigation within the app.
 */
export default function App() {
  const auth = useLogin();

  if (auth.loggedIn) {
    return (
      <NavigationContainer>
        <Tab.Navigator
          screenOptions={({ route, navigation }) => ({
            tabBarShowLabel: false,
            tabBarIcon: ({ focused, color, size }) => {
              let iconName: React.ComponentProps<typeof Ionicons>["name"] = "home";
  
              if (route.name === "Message in a Bottle") {
                iconName = focused ? "mail" : "mail-outline";
              }
              else if (route.name === "Settings") {
                iconName = focused ? "settings" : "settings-outline";
              }
              return <Ionicons name={iconName} size={size} color={color} />;
            },
            tabBarActiveTintColor: "dodgerblue",
            tabBarInactiveTintColor: "grey",
          })}
        >
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
            name="Settings"
            children={() => <SettingsScreen logout={auth.logout}/>}
            options={{ headerShown: true }}
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
    )
  }
  return <SplashScreen login={auth.login} ready={auth.loginReady}/>
}
