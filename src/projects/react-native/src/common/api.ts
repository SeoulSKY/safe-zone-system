import {safeZoneURI} from '@/common/constants';
import {MibsApi, Configuration} from 'mibs';

const apiConfiguration = new Configuration({
  basePath: undefined,
  accessToken: undefined,
});

export const updateToken = (accessToken?: string) => {
  apiConfiguration.baseOptions = {headers: {Authorization: `Bearer ${accessToken}`}};
  updateMibsApi();
};

export const updateTarget = (newTargetServerAddress: string) => {
  global.targetServerAddress = newTargetServerAddress;
  apiConfiguration.basePath = `http://${global.targetServerAddress}:80`;
  updateMibsApi();
};


const updateMibsApi = () => {
  global.mibsApi = new MibsApi(apiConfiguration);
  console.log({apiConfiguration})
};

updateTarget(safeZoneURI);
