import React, {ReactElement, useEffect, useState, useRef} from 'react';
import {StyleSheet, Text, View} from 'react-native';
import {MessageInABottle} from 'mibs'
import {Duration} from '@/common/duration'
import {recipientToString} from '@/common/util';

/**
 * A Message in a Bottle as a list item.
 * @returns A Message in a Bottle list item component.
 */
export default function MibItemHeader({
  message,
  active = undefined,
}: {
  message: MessageInABottle,
  active: boolean
}): ReactElement {
  const [countdown, setCountdown] = useState('00:00:00');
  const countdownInterval: Timer = useRef();

  /**
   * Refreshes the value of the countdown based on the message send time.
   * If the send time is reached or exceeded, the countdown will remain at `00:00:00`.
   */
  function refreshCountdown(): void {
    let expiryTime = new Date(message.sendTime).getTime()
    let remaining = expiryTime - Date.now();
    if (remaining > 0) {
      let newCountdown = new Duration(remaining);
      setCountdown(newCountdown.toString());
    }
    else setCountdown('00:00:00');
  }

  /**
   * Updates the countdown Interval when the send time of the message is
   * changed.
   *
   * Pre-conditions:
   *  countdownInterval exists
   *
   * Post-conditions:
   *  updates the interval to use the new state
   */
  function updateCountdownInterval() {
    if (active) {
      clearInterval(countdownInterval.current);
      countdownInterval.current = setInterval(refreshCountdown, 1000);
    }
  }

  useEffect(updateCountdownInterval, [message.sendTime])

  useEffect(() => {
    if (active) {
      refreshCountdown();
      return function cleanup() {
        clearInterval(countdownInterval.current);
      };
    }
  }, []);

  return (
    <View style={styles.header}>
      <Text style={styles.title} numberOfLines={1}>
        {message.recipients.map(recipientToString).join(', ')}
      </Text>
      <Text style={styles.time}>
        {countdown}
      </Text>
    </View>
  )
}

const styles = StyleSheet.create({
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