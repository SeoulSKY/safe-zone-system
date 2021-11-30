import React from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {TouchableOpacity} from 'react-native-gesture-handler';


/**
 * Settings Screen
 * This component displays the settings for the application.
 *
 * @return {ReactElement} the settings screen component
 */
export function SettingsScreen({logout}: {logout: () => void}) {
  const devOptionsEnabled = false;

  return (
    <View style={styles.container}>
      <View>
        <Text style={styles.title}>Account</Text>
        <View>
          <TouchableOpacity
            onPress={logout}
          >
            <Text style={styles.logout}>
              Log Out
            </Text>
          </TouchableOpacity>
        </View>
      </View>
      {
        devOptionsEnabled ?
          <View>
            <Text style={styles.title}>Developer Settings</Text>
            <View></View>
          </View> : null
      }
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    flex: 1,
  },
  title: {
    paddingTop: 20,
    paddingBottom: 5,
    color: 'dodgerblue',
    fontWeight: 'bold',
  },
  logout: {
    fontSize: 18,
    color: 'grey',
    paddingVertical: 5,
  },
});
