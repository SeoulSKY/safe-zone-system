import React, {ReactElement} from 'react';
import {StyleSheet, View} from 'react-native';
import {DualButton} from '@/components/common';

export function ControlButtons({
  discard,
  send
}: {
  discard: () => void,
  send: () => void,
}): ReactElement {
  return (
    <View style={styles.controlButtonsContainer}>
      <DualButton
        button1Color='#F71D3E'
        button1Text='Discard'
        button1Function={discard}
        button2Text='Create'
        button2Function={send}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  controlButtonsContainer: {
    height: 32,
    marginTop: 16,
  },
});