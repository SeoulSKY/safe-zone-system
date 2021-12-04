import {createContext} from 'react';

/**
 * The Message in a bottle Update Context.
 * This context allows different screens to check and signal mibs needs an
 * update.
 *
 * `mibsUpdate` - whether or not mibs requires an update
 * `setMibsUpdate` - a function to set the value of `mibsUpdate`
 */
export const MibsUpdateContext = createContext(
    {
      mibsUpdate: true,
      setMibsUpdate: (b: boolean) => {
        return;
      },
    }
);
