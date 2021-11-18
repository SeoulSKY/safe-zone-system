import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { MessageInABottle, EmailRecipient, SmsRecipient, UserRecipient } from 'mibs'
import { Duration } from '@/common/duration'


/** The props of a MIB Item Header. The `active` prop is optional. */
type MibItemHeaderProps = {
  message: MessageInABottle,
  active?: boolean
}

/**
 * A Message in a Bottle as a list item.
 * 
 * @param props the message data, and optional active parameter
 * @returns A Message in a Bottle list item component.
 */
export default function MibItemHeader(props: MibItemHeaderProps) {
  const expiryTime = new Date(props.message.sendTime).getTime();
  let newCountdown = new Duration(expiryTime - Date.now())
  const [countdown, setCountdown] = useState(newCountdown.toString());


  /**
   * Converts a recipient object to a string that is readable by users.
   * 
   * @param recipient any recipient 
   * @returns the recipient as a string if successful; `null` on failure
   */
  function recipientToString(
    recipient: EmailRecipient | SmsRecipient | UserRecipient
  ): string | null {
    // Checks for the type of a recipient Union type
    const isEmail = (recipient: any): recipient is EmailRecipient => !!recipient.email
    const isSMS = (recipient: any): recipient is SmsRecipient => !!recipient.phoneNumber
    const isUser = (recipient: any): recipient is UserRecipient => !!recipient.userId

    if (isEmail(recipient))
      return recipient.email ? recipient.email : null
    if (isSMS(recipient))
      return recipient.phoneNumber ? recipient.phoneNumber : null
    if (isUser(recipient))
      return recipient.userId ? recipient.userId : null
    
    return null
  }

  /**
   * Refreshes the value of the countdown based on the message send time.
   * If the send time is reached or exceeded, the countdown will remain at `00:00:00`.
   */
  function refreshCountdown(): void {
    let remaining = expiryTime - Date.now();
    if (remaining > 0) {
      let newCountdown = new Duration(remaining)
      setCountdown(newCountdown.toString())
    }
    else setCountdown('00:00:00')
  }

  useEffect(() => {
    if (props.active) {   // only use countdown timer for active mibs
      const timerId = setInterval(refreshCountdown, 1000);
      return function cleanup() {
        clearInterval(timerId);
      };
    }
  }, []);

  return (
    <View style={styles.header}>
      <Text style={styles.title} numberOfLines={1}>
        {props.message.recipients.map(recipientToString).join(', ')}
      </Text>
      <Text style={styles.time}>
        {countdown}
      </Text>
    </View>
  )
}


let styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
  title: {
    fontSize: 16,
    color: 'black',
    flex: 5,
  },
  time: {
    marginLeft: 16,
    flex: 1,
    color: 'grey',
  },
});