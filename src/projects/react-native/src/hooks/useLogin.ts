import {useEffect, useState} from 'react';
import * as WebBrowser from 'expo-web-browser';
import {
  exchangeCodeAsync, makeRedirectUri, revokeAsync,
  TokenResponse, useAuthRequest, useAutoDiscovery,
} from 'expo-auth-session';
import {Platform} from 'react-native';
import {safeZoneURI} from '../common/constants';

WebBrowser.maybeCompleteAuthSession();
const clientId = 'safe-zone';
const scopes = ['openid'];
const refreshPollInterval = 60 * 1000; // 1 minute

const useProxy = Platform.select({web: false, default: false});

/**
 * @typedef {Object} UseLoginResponse an object containing nessasary infomation
 * to implement a user login
 * @property {boolean} loginReady a boolean indicating if the login function
 * is ready/callable
 * @property {boolean} loggedIn a boolean indicating if the user is
 * currently logged in
 * @property {function} login a function used to login the user.
 * Precondition: loginReady == true
 * Postcondition: Prompts user for login, then once authorized tokens will
 * be no longer be null
 * @property {function} logout a function to logout the current user.
 * This should only be called when the user is currently logged in
 * Precondition: loggedIn == true
 * Postcondition: Logs out the user. Tokes will be null
 * @propery {null | TokenResponse} tokens an object of container the refresh and
 * access token.
 * Value is null until user is logged in using the login function
 */

/**
 * Handles user login for the safe-zone keycloak realm.
 * @return {UseLoginResponse} A set of utility variables and functions
 * to implement a user login
 * Preconditions: Keycloak server is available with the safe-zone configuration
 * imported
 * Postconditions: Discovers keycloak server.
 * @see UseLoginResponse for function specific pre and postconditions
 */
export const useLogin = () => {
  const [tokens, setTokens] = useState<TokenResponse | null>(null);
  const discovery = useAutoDiscovery(`http://${safeZoneURI}/auth/realms/safe-zone`);
  const redirectUri = makeRedirectUri({
    // also sets redirect uri based off scheme in app.json for native
    useProxy,
  });
  const [request, response, promptAsync] = useAuthRequest(
      {
        clientId,
        scopes,
        redirectUri,
        usePKCE: false, // TODO look into using this
      },
      discovery
  );
  const getTokens = () => {
    if (discovery && response?.type === 'success') {
      const {code, state} = response.params;
      exchangeCodeAsync({
        clientId,
        scopes,
        redirectUri,
        code,
        extraParams: {state},
      },
      discovery
      ).then((res) => {
        console.log();
        setTokens(res);
      }).catch(console.error);
    }
  };

  const refreshTokens = () => {
    const interval = setInterval(() => {
      if (discovery && tokens?.shouldRefresh()) {
        tokens?.refreshAsync({
          clientId,
        },
        discovery
        ).then(setTokens)
            .catch((error) => {
              setTokens(null);
              clearInterval(interval);
              console.error('Failed to refresh tokens', error);
            });
      }
    },
    refreshPollInterval
    );
    return () => clearInterval(interval);
  };

  useEffect(getTokens, [response, discovery, redirectUri, setTokens]);

  useEffect(refreshTokens, [tokens, setTokens, discovery]);

  return {
    login: () => {
      promptAsync();
    },
    logout: () => {
      if (tokens && discovery) {
        revokeAsync({
          clientId,
          token: tokens.accessToken,
        },
        discovery
        ).then(() => setTokens(null))
            .catch((error) =>
              console.error('Failed to revoke access token', error));
      } else {
        if (!tokens) {
          console.error('User is not logged in, cannot log out user');
        }
        if (!discovery) {
          console.error('Authentication server details not yet aquired');
        }
      }
    },
    loginReady: !!request,
    loggedIn: !!tokens,
    tokens,
  };
};
