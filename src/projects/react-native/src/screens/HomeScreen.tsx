import React, {ReactElement, useState} from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {Login} from '@/components/Login';
import {ServerSelector} from '@/components/common';

/**
 * Home Screen
 * @method
 * @return {ReactElement}
 */
export function HomeScreen(): ReactElement {
  const [cmsText, setCmsText] = useState('No Response');
  const [mibsText, setMibsText] = useState('No Response');

  const serverSelectorCallback = (serverTarget: string) => {
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
  };

  return (
    <View style={styles.container}>
      <Text>Home Screen</Text>
      <Text>{`CMS Response: ${cmsText}`}</Text>
      <Text>{`MIBS Response: ${mibsText}`}</Text>
      <Login/>
      <ServerSelector onUpdate={serverSelectorCallback}/>
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
});
