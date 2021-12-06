import React, {ReactElement, useState, useEffect, useContext} from 'react';
import {StyleSheet, View} from 'react-native';
import {Recipients} from '@/components/mibs/create/recipients/Recipients';
import {MessageModal} from '@/components/common';
import {
  ControlButtons,
  MessageContainer,
  SendDatePicker,
} from '@/components/mibs/create';
import {EmailRecipient, MessageInABottle} from 'mibs';
import {MibsUpdateContext} from '@/common/mibsContext';
import {updateToken} from '@/common/api';
import {AuthContext} from '@/common/authContext';

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
  const [apiResultModalMessage, setApiResultModalMessage] = useState('');

  const auth = useContext(AuthContext);
  const {setMibsUpdate} = useContext(MibsUpdateContext);

  useEffect(() => {
    navigation.addListener('focus', () => {
      if (isNew) {
        setIsNew(false);
        setSendDate(new Date());
      }
    });
  }, []);

  const send = () => {
    if (apiResultModalMessage === '') {
      setApiResultModalMessage('Sending...');
      openApiModal();
      const recipientsList = recipients.map((recipient) =>
        ({email: recipient.value} as EmailRecipient));

      const mib : MessageInABottle = {
        message: message,
        recipients: recipientsList,
        sendTime: sendDate.toUTCString(),
      };
      updateToken(auth.tokens?.accessToken);
      global.mibsApi.createMessage(mib)
          .then((response) => {
            setApiResultModalMessage(response.data);
            setReceivedResponse(true);
            setRequestSuccessful(true);
            setMibsUpdate(true);
          })
          .catch((error) => {
            if (error.response) {
              setApiResultModalMessage(`Cannot create MIB:
              ${error.response.data}`);
            } else if (error.request) {
              setApiResultModalMessage(`Server did not respond.
              Try again later.`);
            } else {
              setApiResultModalMessage(`Something went wrong sending the data.
              Try again later.`);
            }
            setReceivedResponse(true);
          });
    }
  };

  const discard = () => {
    setIsNew(true);
    setRecipients([]);
    setMessage('');
    setApiResultModalMessage('');
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
    } else {
      setApiResultModalMessage('');
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
        message={apiResultModalMessage}
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
