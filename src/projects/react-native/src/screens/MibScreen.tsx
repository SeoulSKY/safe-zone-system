import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

/**
 * The Screen for the Message In a Bottle feature.
 */
export default function MibScreen() {
  return (
    <View style={styles.container}>
      <Text>MIB Screen</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
