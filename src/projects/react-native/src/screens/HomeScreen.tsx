import React, {ReactElement, useEffect, useState} from 'react';
import {StyleSheet, Text, TextInput, View} from 'react-native';
import {Login} from '@/components/Login';
import {safeZoneURI} from '@/common/constants';
import {updateTarget} from '@/common/api';

/**
 * Home Screen
 * @method
 * @return {ReactElement}
 */
export function HomeScreen(): ReactElement {
  const [serverTarget, setServerTarget] = useState(safeZoneURI);
  const [cmsText, setCmsText] = useState('No Response');
  const [mibsText, setMibsText] = useState('No Response');

  const updateServerTarget = (newTarget) => {
    updateTarget(newTarget);
    setServerTarget(newTarget);
  };

  useEffect(() => {
    fetch(`http://${serverTarget}/cms/hello`, {method: 'GET'})
        .then((response: Response) => response.text()
            .then(setCmsText)
            .catch((error: Error) => setCmsText(`Error: ${error.message}`))
        )
        .catch((error: Error) => setCmsText(`Error: ${error.message}`));


    fetch(`http://${serverTarget}/mibs/hello`, {method: 'GET'})
        .then((response: Response) => response.text()
            .then(setMibsText)
            .catch((error: Error) => setMibsText(`Error: ${error.message}`))
        )
        .catch((error: Error) => setMibsText(`Error: ${error.message}`));
  }, [setCmsText, setMibsText, serverTarget]);

  return (

    <View style={styles.container}>
      <Text>Home Screen</Text>
      <Text>{`CMS Response: ${cmsText}`}</Text>
      <Text>{`MIBS Response: ${mibsText}`}</Text>
      <Login/>
      <Text>Target Server Address</Text>
      <TextInput
        style={styles.textInput}
        onChangeText={updateServerTarget}
        value={serverTarget}
      />
    </View>
  );
}

const color = '#fff';
const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: color,
    flex: 1,
    justifyContent: 'center',
  },
  textInput: {
    borderWidth: 1,
    borderRadius: 5,
    width: 128,
    paddingHorizontal: 4,
  },
});
