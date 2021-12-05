import Constants from 'expo-constants';
import {Platform} from 'react-native';

export const production = Constants.manifest?.extra?.production || false;
export const configuredHost = Constants.manifest?.extra?.host;

export const safeZoneURI = production ?
  configuredHost :
  configuredHost || (Platform.select({web: true, default: false}) ?
    'localhost' :
    Constants.manifest?.debuggerHost?.split(':')[0]);
