import {Duration} from '@/common/duration';
import {recipientToString} from '@/common/util';
import React, {useEffect, useRef, useState} from 'react';
import {
  Button, ScrollView, StyleSheet, Text, TouchableOpacity, View,
} from 'react-native';


/**
 * The View Screen for a single message in a bottle.
 *
 * Pre-conditions:
 *  a message in a bottle must be passed through `route.params`
 *
 * @return {ReactElement}
 */
export function MibItemViewScreen({
  route,
  navigation,
}: {
  route: Route,
  navigation: Navigation
}) {
  const [message, setMessage] = useState(route.params.message);
  const onCancelPress = route.params.onCancelPress;
  const [countdown, setCountdown] = useState('00:00:00');
  const countdownInterval: Timer = useRef();

  /**
   * Refreshes the value of the countdown based on the message send time.
   * If the send time is reached or exceeded, the countdown will remain at
   * `00:00:00`.
   *
   * Pre-conditions:
   *  message.sendTime exists
   *
   * Post-conditions:
   *  updates `countdown`
   */
  function refreshCountdown(): void {
    const expiryTime = new Date(message.sendTime).getTime();
    const remaining = expiryTime - Date.now();
    if (remaining > 0) {
      const newCountdown = new Duration(remaining);
      setCountdown(newCountdown.toString());
    } else setCountdown('00:00:00');
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
    clearInterval(countdownInterval.current);
    countdownInterval.current = setInterval(refreshCountdown, 1000);
  }

  useEffect(updateCountdownInterval, [message.sendTime]);

  useEffect(() => {
    refreshCountdown();
    navigation.setOptions({
      headerRight: () => ( // mount the cancel button to the header
        <TouchableOpacity
          style={styles.cancelButton}
          onPress={() => {
            onCancelPress();
            navigation.goBack();
          }}
          hitSlop={{top: 20, bottom: 20, left: 4, right: 20}}
        >
          <Text style={styles.cancelButtonText}>
            Cancel
          </Text>
        </TouchableOpacity>
      ),
    });
    return function cleanup() {
      clearInterval(countdownInterval.current);
    };
  }, []);

  return (
    <View style={styles.container}>
      <ScrollView style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>
            {message.recipients.map(recipientToString).join(', ')}
          </Text>
          <Text style={styles.time}>
            {countdown}
          </Text>
        </View>
        <Text style={styles.message}>
          {message.message}
        </Text>
      </ScrollView>
      <Button
        title={'Edit'}
        onPress={
          () => navigation.navigate('Edit Message', {message, setMessage})
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    flex: 1,
  },
  header: {
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderBottomColor: 'lightgrey',
    borderBottomWidth: 1,
    flexDirection: 'row',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    color: 'black',
    flex: 3,
  },
  time: {
    flex: 1,
    color: 'grey',
  },
  message: {
    padding: 20,
  },
  cancelButton: {
    marginRight: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  cancelButtonText: {
    color: 'red',
    fontSize: 16,
  },
});
