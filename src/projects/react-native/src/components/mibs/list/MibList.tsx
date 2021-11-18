import React from 'react';
import {FlatList, StyleSheet, View} from 'react-native';
import { MessageInABottle, EmailRecipient, MibsApi} from 'mibs'
import { MibItem } from './item/MibItem';

const mibsApi = new MibsApi()

/**
 * The standard props for a Message in a Bottle list.
 */
 type MibListProps = {
  items: Array<MessageInABottle>
}

/**
 * A message in a bottle list containing active messages.
 * This component is a wrapper element to make using the list with React Navigation easier.
 * 
 * @returns A message in a bottle list of active messages.
 */
export function ActiveMibList() {
  // These fake values may be replaced with a call to the mibs API
  let mibsRecipients: Array<EmailRecipient> = [
    {
      email: 'test@example.com'
    },
    {
      email: 'someguy@example.com'
    }
  ]
  let sendTime = (new Date(Date.now() + 1000000)).toUTCString()
  const mibsList: Array<MessageInABottle> = [
    {
      messageId: 0,
      message: 'This is a test message for multiple recipients.',
      recipients: mibsRecipients,
      sendTime: sendTime,
    },
    {
      messageId: 1,
      message: 'This is a test message to a single recipient.',
      recipients: [{email: 'test@example.com'}],
      sendTime: sendTime,
    }
  ]

  return <MibList items={mibsList} active={true} />
}

/**
 * A message in a bottle list containing template messages.
 * This component is a wrapper element to make using the list with React Navigation easier.
 * 
 * @returns A message in a bottle list of template messages.
 */
export function TemplateMibList() {
  let mibsRecipients: Array<EmailRecipient> = [
    {email: 'test@example.com'},
    {email: 'someguy@example.com'}
  ]
  let sendTime = (new Date(Date.now() + 1000000)).toUTCString()
  const mibsList: Array<MessageInABottle> = [
    {
      messageId: 0,
      message: 'This is a test message for multiple recipients.',
      recipients: mibsRecipients,
      sendTime: sendTime,
    },
    {
      messageId: 1,
      message: 'This is a test message to a single recipient.',
      recipients: [{email: 'test@example.com'}],
      sendTime: sendTime,
    }
  ]

  return <MibList items={mibsList} active={false} />
}

/**
 * The prop for specifying if a list contains active messages.
 */
 type ActiveProp = {
  active?: boolean,
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
export function MibList(props: MibListProps & ActiveProp) {
  return (
    <View style={styles.container}>
      <FlatList style={{marginTop:16}}
        data={props.items.map(mib => {return {key: `${mib.messageId}`, message: mib}})}
        renderItem={({item}) => <MibItem message={item.message} active={props.active} />}
      />
    </View>
  )
}


const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    flex: 1,
  },
});