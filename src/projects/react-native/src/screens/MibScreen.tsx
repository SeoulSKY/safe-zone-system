import React from 'react';
import { StyleSheet } from 'react-native';
import { createMaterialTopTabNavigator } from '@react-navigation/material-top-tabs';
import { ActiveMibList, TemplateMibList } from '@/components/mibs/list';

const Tab = createMaterialTopTabNavigator();

/**
 * The Screen for the Message In a Bottle feature.
 * @method
 * @return {View}
 */
export function MibScreen() {
  return (
      <Tab.Navigator 
        screenOptions={{
          tabBarIndicatorStyle: { backgroundColor: 'dodgerblue' }
        }} 
      >
        <Tab.Screen name="Active" component={ActiveMibList} />
        <Tab.Screen name="Templates" component={TemplateMibList} />
      </Tab.Navigator>
  );
}


const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: '#fff',
    flex: 1,
    justifyContent: 'center',
  },
});
