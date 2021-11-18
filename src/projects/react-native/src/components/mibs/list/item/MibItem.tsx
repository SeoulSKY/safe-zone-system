import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { MessageInABottle } from 'mibs'
import MibItemHeader from './MibItemHeader';


/** The props of a message in a bottle list item. The `active` prop is optional.
*/
type MibProps = {
  message: MessageInABottle
  active?: boolean
}

/**
 * A Message in a Bottle as a list item.
 * 
 * If the `active` prop does not exist, `MibItem` function the same as if was `false`.
 * @param mib the message in a bottle data
 * @returns A Message in a Bottle list item component.
 */
export function MibItem(props: MibProps) {
  
  /**
   * Handles when the message in a bottle item itself is pressed.
   * This function should open a new view for the item.
   */
  function mibItemPress() {
    
  }

  /**
   * Handles when the cancel button is pressed.
   * 
   * Pre-conditions:
   *   props.active is true
   */
  function cancelButtonPress() {

  }

   /**
   * Handles when the set button is pressed.
   * 
   * Pre-conditions:
   *   props.active is false or undefined
   */
  function setButtonPress() {

  }

  return (
    <TouchableOpacity onPress={mibItemPress}>
      <View style={styles.item}>
        <MibItemHeader message={props.message} active={props.active}/>
        <View style={styles.body}>
          <Text style={styles.message} numberOfLines={3}>
            {props.message.message}
          </Text>
          <TouchableOpacity 
            style={styles.iconButton} 
            onPress={() => {}}
            hitSlop={{top: 20, bottom: 20, left: 4, right: 20}}
          >
            {
              props.active ? 
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