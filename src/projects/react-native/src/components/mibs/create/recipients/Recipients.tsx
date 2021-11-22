import React, {ReactElement, useState} from 'react';
import {Button, FlatList, StyleSheet, Text, View} from 'react-native';
import {EmailRecipient, SmsRecipient, UserRecipient} from 'mibs';
import {AddRecipientModal} from '@/components/mibs/create/recipients/AddRecipientModal';


export function Recipients({
  recipients,
  setRecipients,
}: {
  recipients: Array,
  setRecipients: (x: Array) => void,
}) : ReactElement {

  const [showAddRecipientModal, setShowAddRecipientModal] = useState(false);

  const openAddRecipientModal = () => {
    setShowAddRecipientModal(true);
  };

  const closeAddRecipientModal = () => {
    setShowAddRecipientModal(false);
  };

  const addRecipient = (dropdownValue, newRecipientValue) => {
    setRecipients(previousRecipients => {
      return [
        ...previousRecipients,
        {type: dropdownValue, value: newRecipientValue},
      ];
    });
  };

  const deleteRecipient = (recipientToDelete) => {
    setRecipients(recipients.filter((recipient) => {
      return !(recipient.type === recipientToDelete.type
        && recipient.value === recipientToDelete.value);
    }));
  };

  return (
    <View style={styles.recipientsContainer}>
      <Text style={styles.subtitle}>To</Text>
      <FlatList
        persistentScrollbar={true}
        data={recipients}
        keyExtractor={(item, index) => `${item.type}:${item.value}:${index}`}
        renderItem={(recipient) =>
          <View style={styles.container}>
            <Text style={styles.text}>
              {`${recipient.item.type}:${recipient.item.value}`}
            </Text>
            <View style={styles.xButton}>
              <Button
                title="X"
                onPress={() => deleteRecipient(recipient.item)}
              />
            </View>
          </View>
        }
        ListEmptyComponent={<Text style={styles.text}>No recipients</Text>}
      />
      <View style={styles.addButtonContainer}>
        <View style={styles.addButton}>
          <Button
            title="Add recipient"
            onPress={openAddRecipientModal}
          />
        </View>
      </View>
      <AddRecipientModal
        showModal={showAddRecipientModal}
        addRecipient={addRecipient}
        closeModal={closeAddRecipientModal}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  recipientsContainer: {
    height: 150,
  },
  addButtonContainer: {
    alignItems: 'center',
  },
  addButton: {
    paddingHorizontal: 8,
  },
  xButton: {
    justifyContent: 'center',
    alignItems: 'center',
    height: 30,
  },
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    paddingVertical: 8,
    paddingHorizontal: 32,
  },
  subtitle: {
    paddingVertical: 8,
    paddingHorizontal: 8,
    fontSize: 14,
  },
});
