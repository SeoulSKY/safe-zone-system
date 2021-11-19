import React, {ReactElement} from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { MessageInABottle } from 'mibs'
import MibItemHeader from './MibItemHeader';
import { mibsApi } from '@/common/api';


/**
 * A Message in a Bottle as a list item.
 * 
 * If the `active` prop does not exist, `MibItem` function the same as if was `false`.
 * @param mib the message in a bottle data
 * @returns A Message in a Bottle list item component.
 */
export function MibItem({
  deleteItem,
  openModal,
  message,
  active = undefined,
}: {
  deleteItem: Function,
  openModal: Function,
  message: MessageInABottle,
  active: boolean
}): ReactElement {
  
  /**
   * Handles when the message in a bottle item itself is pressed.
   * This function should open a new view for the item.
   */
  const mibItemPress = () => {
    
  }

  /**
   * Handles when the cancel button is pressed.
   * 
   * Pre-conditions:
   *   active is true
   */
  const cancelButtonPress = () => {

  }

   /**
   * Handles when the set button is pressed.
   * 
   * Pre-conditions:
   *   active is false or undefined
   */
  const setButtonPress = () => {

  }

  return (
    <TouchableOpacity key={message.message_id} onPress={mibItemPress}>
      <View style={styles.item}>
        <MibItemHeader message={message} active={active}/>
        <View style={styles.body}>
          <Text style={styles.message} numberOfLines={3}>
            {message.message}
          </Text>
          <TouchableOpacity 
            style={styles.iconButton} 
            onPress={() => {
              global.mibsApi.deleteMessage(message.message_id)
                .then(() => deleteItem(message.message_id))
                .catch(() => openModal('Failed to delete mib. Try again later'));
            }}
            hitSlop={{top: 20, bottom: 20, left: 4, right: 20}}
          >
            {
              active ? 
                <Text style={[{color:'lightcoral', fontSize: 16}]}>
                  Cancel
                </Text> :
                <Text style={[{color:'mediumseagreen', fontSize: 16}]}>
                  Set
                </Text>
            }
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
  }
});