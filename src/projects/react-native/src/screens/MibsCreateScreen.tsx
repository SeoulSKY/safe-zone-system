import React, {ReactElement, useState, useEffect} from 'react';
import {
  StyleSheet,
  SafeAreaView,
  View,
} from 'react-native';
import {Recipients} from '@/components/mibs/create/recipients/Recipients';
import {MessageModal} from '@/components/common';
import {
  ControlButtons,
  MessageContainer,
  SendDatePicker,
} from '@/components/mibs/create';

import {EmailRecipient, MessageInABottle} from 'mibs';

/**
 * The Screen for the Create Message In a Bottle feature.
 * @method
 * @return {View}
 */
export function MibsCreateScreen({
  navigation,
}: {
  navigation: Navigation,
}): ReactElement {
  const [isNew, setIsNew] = useState(false);
  const [recipients, setRecipients] = useState([]);
  const [sendDate, setSendDate] = useState(new Date());
  const [message, setMessage] = useState('');

  const [showApiModal, setShowApiModal] = useState(false);
  const [receivedResponse, setReceivedResponse] = useState(false);
  const [requestSuccessful, setRequestSuccessful] = useState(false);
  const [apiReturn, setApiReturn] = useState('');

  useEffect(() => {
    navigation.addListener('focus', () => {
      if (isNew) {
        setIsNew(false);
        setSendDate(new Date());
      }
    });
  }, []);

  const send = () => {
    const recipientsList = recipients.map((recipient) =>
      ({email: recipient.value} as EmailRecipient));

    const mib : MessageInABottle = {
      message: message,
      recipients: recipientsList,
      sendTime: sendDate,
    };
    setApiReturn('Sending...');
    openApiModal();
    global.mibsApi.createMessage(mib)
        .then((response) => {
          setApiReturn(response.data);
          setReceivedResponse(true);
          setRequestSuccessful(true);
        })
        .catch((error) => {
          if (error.response) {
            setApiReturn(`Cannot create MIB: ${error.response.data}`);
          } else if (error.request) {
            setApiReturn(`Server did not respond. Try again later.`);
          } else {
            setApiReturn(`Something went wrong sending the data.
            Try again later.`);
          }
          setReceivedResponse(true);
        });
  };

  const discard = () => {
    setIsNew(true);
    setRecipients([]);
    setMessage('');
    setApiReturn('');
    setReceivedResponse(false);
    setRequestSuccessful(false);
    navigation.goBack();
  };


  const openApiModal = () => {
    setShowApiModal(true);
  };

  const closeApiModal = () => {
    setShowApiModal(false);
    if (requestSuccessful) {
      discard();
    }
  };

  return (
    <View style={styles.mainContainer}>
      <Recipients
        recipients={recipients}
        setRecipients={setRecipients}
      />

      <SendDatePicker
        sendDate={sendDate}
        setSendDate={setSendDate}
      />

      <MessageContainer
        message={message}
        setMessage={setMessage}
      />

      <ControlButtons
        discard={discard}
        send={send}
      />

      <MessageModal
        message={apiReturn}
        showModal={showApiModal}
        showOkButton={receivedResponse}
        closeModal={closeApiModal}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  mainContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
});
