import React, {ReactElement, useState} from 'react';
import {FlatList, StyleSheet, View, Button, Text} from 'react-native';
import {MessageInABottle, EmailRecipient} from 'mibs'
import {MibItem} from './item/MibItem';
import {useInterval} from '@/hooks/useInterval';
import {MessageModal} from '@/components/common';

/**
 * A message in a bottle list containing active messages.
 * This component is a wrapper element to make using the list with React Navigation easier.
 * 
 * @returns A message in a bottle list of active messages.
 */
export function ActiveMibList({navigation}: {navigation: Navigation}): ReactElement {
  const [mibsList, setMibsList] = React.useState([]);

  const [outOfDate, setOutOfDate] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  const openModal = (message: string) => {
    setModalMessage(message);
    setShowModal(true);
  };

  const closeModal = () => {
    setModalMessage('');
    setShowModal(false);
  };

  const poll = () => {
    global.mibsApi.getMessage()
        .then(response => {
          setMibsList(response.data);
          setOutOfDate(false);
        })
        .catch(error => {
          if(!outOfDate) {
            openModal('Polling for mibs failed, displayed mibs will be out of date.');
            setOutOfDate(true);
          }
        });
  };

  const deleteItem = (itemToDelete) => {
    setMibsList(mibsList.filter((item) => item.message_id !== itemToDelete.message_id));
  };

  useInterval(poll, 5000);

  return (
      <MibList
        items={mibsList}
        deleteItem={deleteItem}
        showModal={showModal}
        modalMessage={modalMessage}
        openModal={openModal}
        closeModal={closeModal}
        outOfDate={outOfDate}
        active={true}
        navigation={navigation}
      />
    );
}

/**
 * A message in a bottle list containing template messages.
 * This component is a wrapper element to make using the list with React Navigation easier.
 * 
 * @returns A message in a bottle list of template messages.
 */
export function TemplateMibList({navigation}: {navigation: Navigation}): ReactElement {
  const mibsList = [];

  const [outOfDate, setOutOfDate] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  const openModal = (message: string) => {
    setModalMessage(message);
    setShowModal(true);
  };

  const closeModal = () => {
    setModalMessage('');
    setShowModal(false);
  };

  const deleteItem = () => {};

  return (
    <MibList
      items={mibsList}
      deleteItem={deleteItem}
      showModal={showModal}
      modalMessage={modalMessage}
      openModal={openModal}
      closeModal={closeModal}
      outOfDate={outOfDate}
      active={false}
      navigation={navigation}
    />
  );
}

/**
 * A message in a Bottle List. This is a list view containing `MibItems`.
 * The `active` parameter specified in `props` determines which style of item to use 
 * (active or template). If active is specified, and it is true, the items will appear as
 * active MIBs; otherwise, they will appear as templates MIBs.
 * 
 * @param props the props containing an optional `active` parameter
 * @returns A Message in a Bottle list component.
 */
export function MibList({
  items,
  deleteItem,
  showModal,
  modalMessage,
  openModal,
  closeModal,
  outOfDate,
  active = undefined,
  navigation,
}: {
  items: Array,
  deleteItem: Function,
  showModal: boolean,
  modalMessage: string,
  openModal: Function,
  closeModal: Function,
  outOfDate: boolean,
  active: boolean,
  navigation: Navigation,
}): ReactElement {

  return (
    <View style={styles.container}>
      <FlatList style={{marginTop:16}}
        data={items.map(mib => {return {key: `${mib.message_id}`, message: mib}})}
        renderItem={({item}) => (
          <MibItem
            message={item.message}
            active={active}
            deleteItem={deleteItem}
            openModal={openModal}
          />
        )}
        ListEmptyComponent={
          <Text
            style={styles.text}
          >
            No Mibs
          </Text>
        }
        ListHeaderComponent={
          outOfDate && <Text style={styles.text}>
            Failed to poll. Mibs are out of date
          </Text>
        }
        ListFooterComponent={
          <Button
            title="Create MIB"
            onPress={() => {
              navigation.navigate('Create Message in a Bottle');
            }}
          />
        }
      />
      <MessageModal
        showModal={showModal}
        message={modalMessage}
        closeModal={closeModal}
      />
    </View>
  )
}


const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    flex: 1,
  },
  text: {
    fontSize: 20,
    textAlign: 'center',
    marginBottom: 8,
  },
});