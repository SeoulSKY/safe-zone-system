import 'react-native-url-polyfill/auto';

import React, {useState} from 'react';
import {StatusBar} from 'expo-status-bar';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs'
import {NavigationContainer} from '@react-navigation/native'
import {Ionicons} from '@expo/vector-icons';
import {SettingsScreen, MibScreen, MibsCreateScreen, 
  MibItemViewScreen, MibsEditScreen} from '@/screens/index'
import {useLogin} from '@/hooks/useLogin';
import {SplashScreen} from '@/screens/SplashScreen';
import {AuthContext} from '@/common/authContext';
import {createStackNavigator} from '@react-navigation/stack';
import {MibsUpdateContext} from '@/common/mibsContext';

const Tab = createBottomTabNavigator()
const Stack = createStackNavigator()

/**
 * The Base Application.
 * This component handles user authentication and the base level navigation
 * within the app.
 * Screens that overlay the main application should included here so that they
 * take up the entirety of the screen.
 */
export default function App() {
  const auth = useLogin();
  const [mibsUpdate, setMibsUpdate] = useState(true);

  if (!auth.loggedIn) {
    return (
      <AuthContext.Provider value={auth}>
        <SplashScreen />
      </AuthContext.Provider>
    )
  }
  return (
    <AuthContext.Provider value={auth}>
      <MibsUpdateContext.Provider value={{mibsUpdate, setMibsUpdate}}>
        <NavigationContainer>
          <Stack.Navigator>
            <Stack.Screen
              name="MainApp"
              component={MainApp}
              options={{headerShown: false}}
            />
            <Stack.Screen
              name="Create Message"
              component={MibsCreateScreen}
            />
            <Stack.Screen
              name="Edit Message"
              component={MibsEditScreen}
            />
            <Stack.Screen
              name="View Message"
              component={MibItemViewScreen}
              options={{title: ''}}
            />
          </Stack.Navigator>
          <StatusBar style="auto" />
        </NavigationContainer>
      </MibsUpdateContext.Provider>
    </AuthContext.Provider>
  )
}

/**
 * The Main application.
 * This component handles the navigation between the main components/screens of
 * the app. Screens added to here will be added to the bottom tab bar of the
 * application.
 */
 function MainApp() {
  return (
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
        component={SettingsScreen}
        options={{ headerShown: true }}
      />
    </Tab.Navigator>
  )
}