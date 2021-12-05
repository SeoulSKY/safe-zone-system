import React, {ReactElement, useContext} from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { MessageInABottle } from 'mibs';
import MibItemHeader from './MibItemHeader';
import { MibsUpdateContext } from '@/common/mibsContext';


/**
 * A Message in a Bottle as a list item.
 * 
 * If the `active` prop does not exist, `MibItem` function the same as if was `false`.
 * @returns A Message in a Bottle list item component.
 */
export function MibItem({
  openModal,
  message,
  active = undefined,
  navigation,
}: {
  openModal: (msg: string) => void,
  message: MessageInABottle,
  active: boolean,
  navigation: Navigation,
}): ReactElement {
  const {setMibsUpdate} = useContext(MibsUpdateContext);
  
  /**
   * Handles when the cancel button for a message in a bottle is pressed.
   * 
   * Pre-conditions:
   *  global.mibsApi exists
   * 
   * Post-conditions:
   *  signals that mibs requires an update
   *  opens a model on failure
   */
  const onCancelPress = () => {
    global.mibsApi.deleteMessage(message.messageId)
      .then(() => setMibsUpdate(true))
      .catch(() => openModal('Failed to delete mib. Try again later'));
  }

  /**
   * Handles when the message in a bottle item itself is pressed.
   * This function should open a new view for the item.
   * 
   * Pre-conditions:
   *  the screen 'View Message' exists
   * 
   * Post-conditions:
   *  opens the view message screen for this message
   */
  const onPress = () => {
    navigation.navigate('View Message', {message, onCancelPress});
  }

  return (
    <TouchableOpacity key={message.messageId} onPress={onPress}>
      <View style={styles.item}>
        <MibItemHeader message={message} active={active}/>
        <View style={styles.body}>
          <Text style={styles.message} numberOfLines={3}>
            {message.message}
          </Text>
          <TouchableOpacity 
            style={styles.iconButton} 
            onPress={onCancelPress}
            hitSlop={{top: 20, bottom: 20, left: 4, right: 20}}
          >
            <Text style={styles.cancelButtonText}>
              Cancel
            </Text> 
          </TouchableOpacity>
        </View>
      </View>
    </TouchableOpacity>
  )
}


const styles = StyleSheet.create({
  item: {
    flexDirection: 'column',
    flex: 1,
    padding: 16,
  },
  body: {
    paddingTop: 8,
    flexDirection: 'row',
    flex: 1,
    alignItems: 'flex-start',
    justifyContent: 'center',
    color: 'grey',
  },
  message: {
    paddingTop: 0,
    paddingRight: 0,
    color: 'grey',
    flex: 9,
  },
  iconButton: {
    paddingLeft: 16,
    height: '100%',
    justifyContent: 'center',
  },
  cancelButtonText: {
    color:'red', 
    fontSize: 16,
  },
});