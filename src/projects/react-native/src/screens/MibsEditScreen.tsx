import React, {ReactElement, useState, useEffect, useContext} from 'react';
import {StyleSheet, View} from 'react-native';
import {Recipients} from '@/components/mibs/create/recipients/Recipients';
import {DualButton, MessageModal} from '@/components/common';
import {MessageContainer, SendDatePicker} from '@/components/mibs/create';
import {EmailRecipient, MessageInABottle} from 'mibs';
import {MibsUpdateContext} from '@/common/mibsContext';
import {isEmail, isSMS, isUser, Recipient} from '@/common/util';
import {assert} from '@/common/assertions';


/**
 * The Edit Screen for an existing message in a bottle.
 *
 * Pre-conditions:
 *  a message in a bottle must be passed through `route.params`
 *
 * @return {ReactElement}
 */
export function MibsEditScreen({
  route,
  navigation,
}: {
  route: Route,
  navigation: Navigation,
}): ReactElement {
  assert(!!route.params.message, 'route.params.message does not exist');
  const oldMib = route.params.message;
  const oldRecipients = oldMib.recipients.map((recipient: Recipient) => {
    assert(isEmail(recipient) ||
      isSMS(recipient) || isUser(recipient), 'Invalid recipient');
    if (isEmail(recipient)) {
      return {type: 'email', value: recipient.email};
    }
    if (isSMS(recipient)) {
      return {type: 'sms', value: recipient.phoneNumber};
    }
    if (isUser(recipient)) {
      return {type: 'user', value: recipient.userId};
    }
  });

  const [isNew, setIsNew] = useState(false);
  const [recipients, setRecipients] = useState(oldRecipients);
  const [sendDate, setSendDate] = useState(new Date(oldMib.sendTime));
  const [message, setMessage] = useState(oldMib.message);

  const [showApiModal, setShowApiModal] = useState(false);
  const [receivedResponse, setReceivedResponse] = useState(false);
  const [requestSuccessful, setRequestSuccessful] = useState(false);
  const [apiReturn, setApiReturn] = useState('');

  const {setMibsUpdate} = useContext(MibsUpdateContext);
  const updateMibItemView = route.params.setMessage;

  useEffect(() => {
    navigation.addListener('focus', () => {
      if (isNew) {
        setIsNew(false);
        setSendDate(new Date());
      }
    });
  }, []);

  /**
   * updates the message in a bottle by sending a PUT request the the MIBS API.
   *
   * Post-conditions:
   *  updates the message on the mibs server
   *  updates the item view for the message
   *  signal that components using mibs require an update
   *  set the response state
   */
  const send = () => {
    const recipientsList = recipients.map((recipient) =>
      ({email: recipient.value} as EmailRecipient));

    const mib : MessageInABottle = {
      messageId: oldMib.messageId,
      message: message,
      recipients: recipientsList,
      sendTime: sendDate.toUTCString(),
    };
    setApiReturn('Sending...');
    openApiModal();
    global.mibsApi.updateMessage(mib)
        .then((response) => {
          setApiReturn(response.data);
          setReceivedResponse(true);
          setRequestSuccessful(true);
          setMibsUpdate(true);
          updateMibItemView(mib);
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

  /**
   * Discards the current changes made to the message.
   *
   * Post-conditions:
   *  resets the component state
   *  navigates to the previous screen
   */
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
      <DualButton
        button1Color='#F71D3E'
        button1Text='Cancel'
        button1Function={discard}
        button2Color='dodgerblue'
        button2Text='Save'
        button2Function={send}
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
    height: '100%',
    flex: 1,
    backgroundColor: '#fff',
  },
});
