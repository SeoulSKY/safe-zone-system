import React from 'react';
import {Button} from 'react-native';
import {useLogin} from '../hooks/useLogin'; // TODO set configuration

/**
 * A login button for the safe-zone keycloak server
 * Preconditions: @see useLogin
 * Postconditions: @see useLogin
 * Button will be disabled if !loginReady
 * Button will be login if loginReady and !loggedIn
 * Button will be logout if loggedIn
 * Uses login and logout functions from useLogin respectivly
 *
 * @return {ReactElement}
 */
export const Login = () => {
  const {login, logout, loginReady, loggedIn} = useLogin();
  if (loggedIn) {
    return (
      <Button
        title="Logout"
        onPress={logout}
      />
    );
  }
  return (
    <Button
      disabled={!loginReady}
      title="Login"
      onPress={login}
    />
  );
};
