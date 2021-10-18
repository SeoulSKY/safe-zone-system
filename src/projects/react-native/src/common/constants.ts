import Constants from 'expo-constants';
import {Platform} from 'react-native';

export const safeZoneURI = Platform.select({web: true, default: false}) ?
  'localhost' : Constants.manifest?.debuggerHost?.split(':')[0];
