import React, {ReactElement, useState} from 'react';
import {Button, StyleSheet, Text, View} from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import {DualButton} from '@/components/common';

export function SendDatePicker({
  sendDate,
  setSendDate,
}: {
  sendDate: Date,
  setSendDate: () => void
}): ReactElement {

  const [datePickerMode, setDatePickerMode] = useState('date');
  const [showDatePicker, setShowDatePicker] = useState(false);

  const showDatepicker = () => {
    showMode('date');
  };

  const showTimepicker = () => {
    showMode('time');
  };

  const onDateTimePickerChange = (event, selectedDate) => {
    const currentDate = selectedDate || sendDate;
    setShowDatePicker(Platform.OS === 'ios');
    setSendDate(currentDate);
  };

  const showMode = (currentMode) => {
    setShowDatePicker(true);
    setDatePickerMode(currentMode);
  };

  return (
    <View style={styles.sendDateContainer}>
      <Text style={styles.subtitle}>Send Time</Text>
      <DualButton
        button1Text={sendDate.toLocaleDateString([], { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        button1Function={showDatepicker}
        button2Text={sendDate.toLocaleTimeString([], {hour12: true, hour: 'numeric', minute: '2-digit'})}
        button2Function={showTimepicker}
      />
      {showDatePicker && (
        <DateTimePicker
          testID="dateTimePicker"
          value={sendDate}
          mode={datePickerMode}
          is24Hour={false}
          display="default"
          onChange={onDateTimePickerChange}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  sendDateContainer: {
    height: 64,
  },
  subtitle: {
    paddingVertical: 8,
    paddingHorizontal: 8,
    fontSize: 14,
  },
});