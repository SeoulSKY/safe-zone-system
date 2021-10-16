import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { MibsApi } from 'mibs';

const mibsApi = new MibsApi() // test mibs import

/**
 * Home Screen
 * @method
 * @return {View}
 */
export default function HomeScreen() {
  const [cmsText, setCmsText] = useState('No Response');
  const [mibsText, setMibsText] = useState('No Response');

  useEffect(() => {
    fetch('http://localhost/cms/hello', {method: 'GET'})
        .then((response: Response) => {
          console.log('response', response);
          return response.text();
        })
        .then(setCmsText)
        .catch((error: Error) => setCmsText(`Error: ${error.message}`));

    fetch('http://localhost/mibs/hello', {method: 'GET'})
        .then((response: Response) => response.text() )
        .then(setMibsText)
        .catch((error: Error) => setMibsText(`Error: ${error.message}`));
  }, [setCmsText, setMibsText]);

  return (
    <View style={styles.container}>
      <Text>Home Screen</Text>
      <Text>{`CMS Response: ${cmsText}`}</Text>
      <Text>{`MIBS Response: ${mibsText}`}</Text>
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
