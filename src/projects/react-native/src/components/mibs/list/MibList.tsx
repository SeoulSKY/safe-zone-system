import React, {ReactElement, useEffect, useState, useContext} from 'react';
import {FlatList, StyleSheet, View, Button, Text} from 'react-native';
import {MessageInABottle} from 'mibs'
import {MibItem} from './item/MibItem';
import {MessageModal} from '@/components/common';
import {MibsUpdateContext} from '@/common/mibsContext';

/**
 * A message in a bottle list containing active messages.
 * This component is a wrapper element to make using the list with React Navigation easier.
 * 
 * @returns A message in a bottle list of active messages.
 */
export function ActiveMibList({navigation}: {navigation: Navigation}): ReactElement {
  const [mibsList, setMibsList] = React.useState([]);

  const [showModal, setShowModal] = useState(false);
  const [modalMessage, setModalMessage] = useState('');

  const {mibsUpdate, setMibsUpdate} = useContext(MibsUpdateContext);

  const openModal = (message: string) => {
    setModalMessage(message);
    setShowModal(true);
  };

  const closeModal = () => {
    setModalMessage('');
    setShowModal(false);
  };

  /**
   * Gets the messages from the MIBS API.
   *
   * Pre-conditions:
   *  global.mibsApi exists
   *
   * Post-conditions:
   *  sets `mibsList` to be the response of the GET request.
   */
  const getMessages = () => {
    global.mibsApi.getMessage()
      .then(response => {
        // the following is a workaround due to issue #261, and must be updated when it is resolved.
        let mibs: Array<MessageInABottle> = response.data.map(res => {
          return {
            messageId: res.message_id,
            message: res.message,
            recipients: res.recipients,
            sendTime: res.send_time,
          }
        })
        setMibsList(mibs);
      })
      .catch(error => {
        openModal(`Failed to fetch messages: ${error}`);
      });
  };
  useEffect(getMessages, []);
  useEffect(() => {
    if (mibsUpdate) {  // mibs GET request when an update is signalled
      getMessages();
      setMibsUpdate(false);
    }
  }, [mibsUpdate]);

  return (
      <MibList
        items={mibsList}
        showModal={showModal}
        modalMessage={modalMessage}
        openModal={openModal}
        closeModal={closeModal}
        active={true}
        navigation={navigation}
        onRefresh={getMessages}
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
  const [mibsList, setMibsList] = React.useState([]);

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

  const getTemplates = () => {};

  return (
    <MibList
      items={mibsList}
      showModal={showModal}
      modalMessage={modalMessage}
      openModal={openModal}
      closeModal={closeModal}
      active={false}
      navigation={navigation}
      onRefresh={getTemplates}
    />
  );
}

/**
 * A message in a Bottle List. This is a list view containing `MibItems`.
 * The `active` parameter specified in `props` determines which style of item to use 
 * (active or template). If active is specified, and it is true, the items will appear as
 * active MIBs; otherwise, they will appear as templates MIBs.
 *
 * @returns A Message in a Bottle list component.
 */
export function MibList({
  items,
  showModal,
  modalMessage,
  openModal,
  closeModal,
  active = undefined,
  navigation,
  onRefresh,
}: {
  items: Array<MessageInABottle>,
  showModal: boolean,
  modalMessage: string,
  openModal: (msg: string) => void,
  closeModal: () => void,
  active: boolean,
  navigation: Navigation,
  onRefresh: () => void,
}): ReactElement {
  const [isRefreshing, setIsRefreshing] = useState(false);

  /** Refresh the list using the provided callback function. */
  function refresh() {
    setIsRefreshing(true);
    onRefresh();
    setIsRefreshing(false);
  }

  return (
    <View style={styles.container}>
      <FlatList
        style={{marginTop:16}}
        data={items.map(mib => {return {key: `${mib.messageId}`, message: mib}})}
        onRefresh={refresh}
        refreshing={isRefreshing}
        renderItem={({item}) => (
          <MibItem
            message={item.message}
            active={active}
            openModal={openModal}
            navigation={navigation}
          />
        )}
        ListEmptyComponent={
          <View>
            <Text style={styles.text}>
              {active ? 'No active messages' : 'No message templates'}
            </Text>
            <Text style={[styles.text, styles.smallText]}>
              Pull down to refresh, or create a new
              {active ? ' message' : ' template'}
            </Text>
          </View>
        }
      />
      <Button
            title={active ? 'Create Message' : 'Create Template'}
            disabled={!active}
            onPress={() => {
              navigation.push('Create Message');
            }}
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
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 8,
    color: 'grey',
  },
  smallText: {
    fontSize: 12,
  },
});