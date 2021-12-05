import React, {ReactElement} from 'react';
import {Button, Modal, StyleSheet, Text, View} from 'react-native';

export function MessageModal({
  showModal,
  showOk = true,
  message,
  closeModal,
}: {
  showModal: boolean,
  showOk: boolean,
  message: String,
  closeModal: () => void,
}): ReactElement {
  return (
    <Modal
      style={styles.modalContainer}
      transparent={true}
      visible={showModal}
    >
    <View style={styles.centeredView}>
      <View style={styles.modalView}>
        <Text style={styles.subtitle}>
          {message}
        </Text>
        {showOk && <Button
          title="OK"
          onPress={closeModal}
        />}
      </View>
    </View>
  </Modal>
  );
}

const styles = StyleSheet.create({
  modalContainer: {
    height: '50%',
    width: '50%'
  },
  centeredView: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    marginTop: 22
  },
  modalView: {
    margin: 20,
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5
  },
  subtitle: {
    paddingVertical: 8,
    paddingHorizontal: 8,
    fontSize: 14,
  },
});