import React, {ReactElement} from 'react';
import {StyleSheet, Text, TextInput, View} from 'react-native'

export function MessageContainer({
  message,
  setMessage,
}: {
  message: string,
  setMessage: () => void
}): ReactElement {
  return (
    <View style={styles.container}>
      <Text style={styles.subtitle}>Message</Text>
      <View style={styles.messageContainer}>
        <TextInput
          multiline
          style={styles.messageBox}
          onChangeText={setMessage}
          value={message}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  subtitle: {
    paddingVertical: 8,
    paddingHorizontal: 8,
    fontSize: 14,
  },
  messageBox: {
    paddingHorizontal: 8,
    paddingVertical: 8,
    textAlignVertical: 'top',
    backgroundColor: '#D3D3D3',
    borderWidth: 1,
    borderRadius: 5,
    height: '95%',
  },
  messageContainer: {
    paddingHorizontal: 8,
    paddingVertical: 8,
    height: '95%',
  },
});