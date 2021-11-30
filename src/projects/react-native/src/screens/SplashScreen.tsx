import React from 'react';
import {Button, StyleSheet, Text, View} from 'react-native';
import {StatusBar} from 'expo-status-bar';


/**
 * Splash Screen
 * The component represents the initial screen that appears when a user first
 * opens the application.
 *
 * @return {ReactElement} the splash screen component
 */
export function SplashScreen(
    {login, ready}
  :
    {login: ()=> void, ready: boolean}
) {
  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <Text style={styles.title}>
          SAFE-ZONE
        </Text>
        <Text style={styles.text}>
          Please login to use the application
        </Text>
      </View>
      <View style={[styles.row, styles.bottom]}>
        <Button
          title="Continue to Login"
          disabled={!ready}
          onPress={login}
        />
      </View>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    flexDirection: 'column',
    paddingVertical: 100,
    flex: 1,
  },
  row: {
    alignItems: 'center',
    flex: 1,
  },
  bottom: {
    justifyContent: 'flex-end',
    alignItems: 'stretch',
    paddingHorizontal: 20,
  },
  title: {
    fontSize: 32,
    color: 'grey',
    fontWeight: 'bold',
    marginBottom: 10,
  },
  text: {
    color: 'grey',
  },
});
