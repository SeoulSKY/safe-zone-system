import React, {useState} from 'react';
import {FlatList, Modal, StyleSheet, Text, TextInput, View} from 'react-native';
import DropDownPicker from 'react-native-dropdown-picker';
import {DualButton} from '@/components/common';

export function AddRecipientModal({
  showModal,
  closeModal,
  addRecipient,
  err,
}: {
  showModal: boolean,
  closeModal: () => void,
  addRecipient: () => String,
  err: String
}): ReactElement {

  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [recipientType, setRecipientType] = useState('email');
  const [recipientValue, setRecipientValue] = useState('');

  const recipientTypes = [{label: 'Email', value: 'email'}];
  const valueDisplay = { email: 'Email Address' };

  const convertToDisplay = (valueToDisplay) => {
    const value = valueDisplay[valueToDisplay];
    return value !== undefined ? value : 'Value'
  };

  const close = () => {
    setRecipientType('email');
    setRecipientValue('');
    closeModal();
  }

  const addAndClose = () => {
    err=addRecipient(recipientType, recipientValue);
    if(err === ''){
      close();
    }
    else {
      console.error(err)
    }  
  }


  return (
    <Modal
      style={styles.modalContainer}
      transparent={true}
      visible={showModal}
    >
      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          <Text style={styles.title}>Add a Recipient</Text>
          <DropDownPicker
            open={dropdownOpen}
            value={recipientType}
            items={recipientTypes}
            setOpen={setDropdownOpen}
            setValue={setRecipientType}
          />
          <Text style={styles.subtitle}>{convertToDisplay(recipientType)}</Text>
          <TextInput
            style={styles.newRecipientInput}
            onChangeText={setRecipientValue}
            value={recipientValue}
          />
          <DualButton
            button1Color='#F71D3E'
            button1Text='Cancel'
            button1Function={close}
            button2Text='Add recipient'
            button2Function={addAndClose}
          />
          
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
      height: 2
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5
  },
  newRecipientInput: {
    paddingHorizontal: 8,
    paddingVertical: 8,
    borderWidth: 1,
    borderRadius: 5,
    width: 256,
    marginBottom: 8
  },
  title: {
    marginTop: 24,
    marginBottom: 8,
    paddingHorizontal: 8,
    textAlign: 'center',
    fontSize: 20
  },
  subtitle: {
    paddingVertical: 8,
    paddingHorizontal: 8,
    fontSize: 14,
  },
  error:{
    color: 'red',
    textAlign: 'left'
  }
});
