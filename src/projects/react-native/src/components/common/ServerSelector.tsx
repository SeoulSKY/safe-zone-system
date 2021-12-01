import React from 'react';
import {useEffect, useState} from 'react';
import {production, safeZoneURI} from '@/common/constants';
import {updateTarget} from '@/common/api';
import {StyleSheet, Text, TextInput} from 'react-native';

export const ServerSelector =
({onUpdate}: {onUpdate: (server: string) => void}) => {
  const [serverTarget, setServerTarget] = useState(safeZoneURI as string);
  const updateServerTarget = (newTarget: string) => {
    updateTarget(newTarget);
    setServerTarget(newTarget);
  };

  useEffect(() => onUpdate(serverTarget), [onUpdate, setServerTarget]);

  if (production) {
    return null;
  }

  return (
    <>
      <Text>Target Server Address</Text>
      <TextInput
        style={styles.textInput}
        onChangeText={updateServerTarget}
        value={serverTarget}
      />
    </>
  );
};

const styles = StyleSheet.create({
  textInput: {
    borderWidth: 1,
    borderRadius: 5,
    width: 128,
    paddingHorizontal: 4,
  },
});
