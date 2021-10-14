import React from 'react';
import {StyleSheet, Text, View} from 'react-native';

/**
 * The Screen for the Message In a Bottle feature.
 * @method
 * @return {View}
 */
export default function MibScreen() {
  return (
    <View style={styles.container}>
      <Text>MIB Screen</Text>
    </View>
  );
}

const textColor = '#fff';

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: textColor,
    flex: 1,
    justifyContent: 'center',
  },
});
