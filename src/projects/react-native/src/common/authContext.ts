import {Auth} from '@/hooks/useLogin';
import React from 'react';


/**
 * This exists to provide the Auth context with a default value.
 * Note that this value must be the same type returned by the `useLogin()`
 * hook.
 */
const defaultContextValue: Auth = {
  login: () => {
    return;
  },
  logout: () => {
    return;
  },
  loginReady: false,
  loggedIn: false,
  tokens: null,
};

/**
 * The Authorization context for the app.
 * This allows the the auth data be easily accessed from any part of the app.
 */
export const AuthContext = React.createContext(defaultContextValue);
