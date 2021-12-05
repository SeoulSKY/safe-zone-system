import React, {ReactElement} from 'react';
import {Button, StyleSheet, View} from 'react-native';
import {assert} from '@/common/assertions';

export function DualButton({
  button1Color,
  button1Text,
  button1Function,
  button2Color,
  button2Text,
  button2Function,
}: {
  button1Color: string,
  button1Text: string,
  button1Function: () => void,
  button2Color: string,
  button2Text: string,
  button2Function: () => void,
}): ReactElement {
  assert(!!button1Text, 'Empty button1Text')
  assert(!!button2Text, 'Empty button2Text')
  return (
    <View style={styles.container}>
      <View style={styles.buttonContainer}>
        <Button
          color={button1Color}
          title={button1Text}
          onPress={button1Function}
        />
      </View>
      <View style={styles.buttonContainer}>
        <Button
          color={button2Color}
          title={button2Text}
          onPress={button2Function}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonContainer: {
    flex: 1,
  },
});