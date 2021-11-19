import {safeZoneURI} from '@/common/constants';
import {MibsApi, Configuration} from 'mibs';

export const updateTarget = (newTargetServerAddress: string) => {
  global.targetServerAddress = newTargetServerAddress;
  const apiConfiguration = new Configuration({
    basePath: `http://${global.targetServerAddress}:80`,
  });
  global.mibsApi = new MibsApi(apiConfiguration);
};

updateTarget(safeZoneURI);
