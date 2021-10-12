import React, { useEffect, useState } from 'react';
import * as WebBrowser from 'expo-web-browser';
import { dismiss, exchangeCodeAsync, makeRedirectUri, revokeAsync, TokenResponse, useAuthRequest, useAutoDiscovery } from 'expo-auth-session';
import { Button, Platform } from 'react-native';

WebBrowser.maybeCompleteAuthSession();
const clientId = 'safe-zone'
const scopes = ['openid']
const refreshPollInterval = 60 * 1000; // 1 minute

const useProxy = Platform.select({ web: false, default: true });

const useLogin = () => {
  const [tokens, setTokens] = useState<TokenResponse | null>(null)
  const discovery = useAutoDiscovery('http://localhost/auth/realms/safe-zone');
  const redirectUri = makeRedirectUri({
    // also sets redirect uri based off scheme in app.json for native
    useProxy,
  })
  const [request, response, promptAsync] = useAuthRequest(
    {
      clientId,
      scopes,
      redirectUri,
      usePKCE: false // TODO look into using this
    },
    discovery
  )
  const getTokens = () => {
    if (discovery && response?.type === 'success') {
      const { code, state } = response.params;
      exchangeCodeAsync({
        clientId,
        scopes,
        redirectUri,
        code,
        extraParams: { state },
      },
        discovery
      )
        .then(setTokens)
        .catch(console.error);
    }
  }

  const refreshTokens = () => {
    let interval = setInterval(() => {
      if (discovery && tokens?.shouldRefresh()) {
        tokens?.refreshAsync({
            clientId
          },
          discovery
        )
        .then(setTokens)
        .catch((error) => {
          dismiss()
          setTokens(null)
          clearInterval(interval)
          console.error('Failed to refresh tokens', error)
        })
      }
    }, 
    refreshPollInterval
    )
    return () => clearInterval(interval)
  }

  useEffect(getTokens, [response, discovery, redirectUri, setTokens])

  useEffect(refreshTokens, [tokens, setTokens, discovery])

  console.log({request, response, tokens})
  return {
    login: () => promptAsync({ useProxy }),
    logout: () => {
      if (tokens && discovery) {
        revokeAsync({
          clientId,
          token: tokens.accessToken
        }, discovery)
        .then(dismiss)
        .then(() => setTokens(null))
        .catch((error) => console.error('Failed to revoke access token', error))
        
      } else {
        if (!tokens) {
          console.error('User is not logged in, cannot log out user')
        }
        if (!discovery) {
          console.error('Authentication server details not yet aquired')
        }
      }
      
    },
    loginReady: !request,
    loggedIn: !!tokens,
  }

  
}

export default function Auth() {
  const { login, logout, loginReady, loggedIn } = useLogin()
  if (loggedIn) {
    return (
      <Button
        title="Logout"
        onPress={logout}
      />
    )
  }
  return (
    <Button
      disabled={loginReady}
      title="Login"
      onPress={login}
    />
  )
}
