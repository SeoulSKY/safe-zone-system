import React from 'react';
import {renderHook} from '@testing-library/react-hooks';
import {safeZoneURI} from '../../src/common/constants';
import {useLogin} from '../../src/hooks/useLogin';
import {exchangeCodeAsync, makeRedirectUri, revokeAsync, useAuthRequest, useAutoDiscovery} from 'expo-auth-session';

jest.useFakeTimers()

const expectedClientId = 'safe-zone'
const expectedScopes = ['openid']
jest.mock('../../src/common/constants', () => ({
  __esModule: true,
  safeZoneURI: 'test-safe-zone-uri'
}))
jest.mock('expo-auth-session', () => ({
  __esModule: true,
  exchangeCodeAsync: jest.fn(), 
  makeRedirectUri: jest.fn(), 
  revokeAsync: jest.fn(), 
  useAuthRequest: jest.fn(), 
  useAutoDiscovery: jest.fn(), 
}))
jest.spyOn(React, 'useState')

const testDiscovery = 'discovery';
const testRedirectUri = 'redirectUri';
afterEach(() => {
  jest.clearAllMocks()
})

test('Initial call', () => {
  useAutoDiscovery.mockImplementation(() => null)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  useAuthRequest.mockImplementation(() => ([null, null, null]))

  const {result} = renderHook(() => useLogin())
  expect(React.useState).toHaveBeenCalledTimes(1)
  expect(React.useState).toHaveBeenCalledWith(null)

  expect(useAutoDiscovery).toBeCalledTimes(1)
  expect(useAutoDiscovery).toHaveBeenCalledWith(`http://${safeZoneURI}/auth/realms/safe-zone`)

  expect(makeRedirectUri).toBeCalledTimes(1)
  expect(makeRedirectUri).toHaveBeenCalledWith({useProxy: false})

  expect(useAuthRequest).toBeCalledTimes(1)
  expect(useAuthRequest).toHaveBeenCalledWith(
    {
      clientId: expectedClientId,
      scopes: expectedScopes,
      redirectUri: testRedirectUri,
      usePKCE: false,
    },
    null
  )

  const {loginReady, loggedIn, login, logout, tokens} = result.current
  expect(loginReady).toBe(false)
  expect(loggedIn).toBe(false)
  expect(typeof login).toBe('function')
  expect(typeof logout).toBe('function')
  expect(tokens).toBe(null)
})

test('After discovery', () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  useAuthRequest.mockImplementation(() => ([null, null, null]))

  const {result} = renderHook(() => useLogin())
  expect(React.useState).toHaveBeenCalledTimes(1)
  expect(React.useState).toHaveBeenCalledWith(null)

  expect(useAutoDiscovery).toBeCalledTimes(1)
  expect(useAutoDiscovery).toHaveBeenCalledWith(`http://${safeZoneURI}/auth/realms/safe-zone`)

  expect(makeRedirectUri).toBeCalledTimes(1)
  expect(makeRedirectUri).toHaveBeenCalledWith({useProxy: false})

  expect(useAuthRequest).toBeCalledTimes(1)
  expect(useAuthRequest).toHaveBeenCalledWith(
    {
      clientId: expectedClientId,
      scopes: expectedScopes,
      redirectUri: testRedirectUri,
      usePKCE: false,
    },
    testDiscovery
  )

  const {loginReady, loggedIn, login, logout, tokens} = result.current
  expect(loginReady).toBe(false)
  expect(loggedIn).toBe(false)
  expect(typeof login).toBe('function')
  expect(typeof logout).toBe('function')
  expect(tokens).toBe(null)
})

test('After auth request', () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  const notFalsyRequest = 'request'
  const notFalsyResponse = 'response'
  const loginFunction = () => {} 
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    notFalsyResponse,
    loginFunction
  ]))

  const {result} = renderHook(() => useLogin())
  expect(React.useState).toHaveBeenCalledTimes(1)
  expect(React.useState).toHaveBeenCalledWith(null)

  expect(useAutoDiscovery).toBeCalledTimes(1)
  expect(useAutoDiscovery).toHaveBeenCalledWith(`http://${safeZoneURI}/auth/realms/safe-zone`)

  expect(makeRedirectUri).toBeCalledTimes(1)
  expect(makeRedirectUri).toHaveBeenCalledWith({useProxy: false})

  expect(useAuthRequest).toBeCalledTimes(1)
  expect(useAuthRequest).toHaveBeenCalledWith(
    {
      clientId: expectedClientId,
      scopes: expectedScopes,
      redirectUri: testRedirectUri,
      usePKCE: false,
    },
    testDiscovery
  )

  const {loginReady, loggedIn, login, logout, tokens} = result.current
  expect(loginReady).toBe(true)
  expect(loggedIn).toBe(false)
  expect(typeof login).toBe('function')
  expect(typeof logout).toBe('function')
  expect(tokens).toBe(null)
})

test('Login function', () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  const notFalsyRequest = 'request'
  const notFalsyResponse = 'response'
  const loginFunction = jest.fn() 
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    notFalsyResponse,
    loginFunction
  ]))

  const {result} = renderHook(() => useLogin())

  const {login} = result.current
  login()
  expect(loginFunction).toHaveBeenCalledTimes(1)
})

test('Logout function', async () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  const testTokens = {accessToken: 'accessToken'}
  exchangeCodeAsync.mockImplementation(async () => testTokens)
  revokeAsync.mockImplementation(async () => {})
  const notFalsyRequest = 'request'
  const responseCode = 'responseCode'
  const responseState = 'responseState'
  const testResponse = {type: 'success', params: {code: responseCode, state: responseState}}
  const loginFunction = () => {}
  
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    testResponse,
    loginFunction
  ]))

  const {result, rerender, waitForNextUpdate} = renderHook(() => useLogin())
  rerender()
  await waitForNextUpdate()

  const {logout} = result.current
  logout()
  await waitForNextUpdate()

  expect(revokeAsync).toHaveBeenCalledTimes(1)
  expect(revokeAsync).toBeCalledWith({
      clientId: expectedClientId,
      token: testTokens.accessToken
    },
    testDiscovery
  )
  expect(result.current.tokens).toBe(null)
})

test('Get tokens success', async () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  const testTokens = 'testTokens'
  exchangeCodeAsync.mockImplementation(async () => testTokens)
  const notFalsyRequest = 'request'
  const responseCode = 'responseCode'
  const responseState = 'responseState'
  const testResponse = {type: 'success', params: {code: responseCode, state: responseState}}
  const loginFunction = () => {}
  
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    testResponse,
    loginFunction
  ]))

  const {result, rerender, waitForNextUpdate} = renderHook(() => useLogin())
  rerender()
  
  expect(exchangeCodeAsync).toHaveBeenCalledTimes(1)
  expect(exchangeCodeAsync).toHaveBeenCalledWith({
      clientId: expectedClientId,
      scopes: expectedScopes,
      redirectUri: testRedirectUri,
      code: responseCode,
      extraParams: {
        state: responseState,
      },
    },
    testDiscovery
  )
  await waitForNextUpdate()

  expect(result.current.tokens).toBe(testTokens)
})

test('Get tokens failure', async () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  exchangeCodeAsync.mockImplementation(async () => {
    throw 'get token failure'
  })
  const notFalsyRequest = 'request'
  const responseCode = 'responseCode'
  const responseState = 'responseState'
  const testResponse = {type: 'success', params: {code: responseCode, state: responseState}}
  const loginFunction = () => {}
  
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    testResponse,
    loginFunction
  ]))

  const {result, rerender} = renderHook(() => useLogin())
  rerender()
  rerender()

  expect(result.current.tokens).toBe(null)
})

test('Refresh tokens success', async () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  const testRefreshTokens = {shouldRefresh: jest.fn(), refreshAsync: jest.fn()}
  const testInitialTokens = {
    shouldRefresh: jest.fn()
      .mockImplementationOnce(() => false)
      .mockImplementationOnce(() => true), 
    refreshAsync: jest.fn()
      .mockResolvedValue(testRefreshTokens)
  }    
  exchangeCodeAsync.mockImplementation(async () => testInitialTokens)
  const notFalsyRequest = 'request'
  const responseCode = 'responseCode'
  const responseState = 'responseState'
  const testResponse = {type: 'success', params: {code: responseCode, state: responseState}}
  const loginFunction = () => {}
  
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    testResponse,
    loginFunction
  ]))

  const {result, rerender, waitForNextUpdate} = renderHook(() => useLogin())
  rerender()
  await waitForNextUpdate()

  jest.runOnlyPendingTimers()

  expect(testInitialTokens.shouldRefresh).toBeCalledTimes(1)
  expect(testInitialTokens.refreshAsync).toBeCalledTimes(0)

  jest.runOnlyPendingTimers()
  await waitForNextUpdate()

  expect(testInitialTokens.shouldRefresh).toBeCalledTimes(2)
  expect(testInitialTokens.refreshAsync).toBeCalledTimes(1)

  expect(result.current.tokens).toBe(testRefreshTokens)
})

test('Refresh tokens failure', async () => {
  useAutoDiscovery.mockImplementation(() => testDiscovery)
  makeRedirectUri.mockImplementation(() => testRedirectUri)
  const testInitialTokens = {
    shouldRefresh: jest.fn()
      .mockImplementationOnce(() => false)
      .mockImplementationOnce(() => true), 
    refreshAsync: jest.fn()
      .mockRejectedValue(new Error('Error refreshing token'))
  }    
  exchangeCodeAsync.mockImplementation(async () => testInitialTokens)
  const notFalsyRequest = 'request'
  const responseCode = 'responseCode'
  const responseState = 'responseState'
  const testResponse = {type: 'success', params: {code: responseCode, state: responseState}}
  const loginFunction = () => {}
  
  useAuthRequest.mockImplementation(() => ([
    notFalsyRequest,
    testResponse,
    loginFunction
  ]))

  const {result, rerender, waitForNextUpdate} = renderHook(() => useLogin())
  rerender()
  await waitForNextUpdate()

  jest.runOnlyPendingTimers()

  expect(testInitialTokens.shouldRefresh).toBeCalledTimes(1)
  expect(testInitialTokens.refreshAsync).toBeCalledTimes(0)

  jest.runOnlyPendingTimers()
  await waitForNextUpdate()

  expect(testInitialTokens.shouldRefresh).toBeCalledTimes(2)
  expect(testInitialTokens.refreshAsync).toBeCalledTimes(1)

  expect(result.current.tokens).toBe(null)
})