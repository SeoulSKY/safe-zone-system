import React from "react";
import '@testing-library/jest-native/extend-expect'
import {fireEvent, render} from "@testing-library/react-native";
import {Login} from "@/components/Login";
import {useLogin} from '@/hooks/useLogin';

jest.mock('../../src/hooks/useLogin', () => ({
  __esModule: true,
  useLogin: jest.fn()
}))

beforeEach(() => {
  useLogin.mockClear()
})

test('Cannot click login when login is not ready', () => {
  useLogin.mockImplementation(() => ({
    login: () => {},
    logout: () => {},
    loginReady: false,
    loggedIn: false
  }))
  const {getByRole} = render(<Login/>)
  const element = getByRole('button')
  expect(element).toHaveTextContent(/Login/i)
  expect(element).toBeDisabled()
})

test('Login disabled when login is not ready', () => {
  useLogin.mockImplementation(() => ({
    login: () => {},
    logout: () => {},
    loginReady: false,
    loggedIn: false
  }))
  const {getByRole} = render(<Login/>)
  const element = getByRole('button')
  expect(element).toHaveTextContent(/Login/i)
  expect(element).toBeDisabled()
})

test('Login enabled when login is ready', () => {
  useLogin.mockImplementation(() => ({
    login: () => {},
    logout: () => {},
    loginReady: true,
    loggedIn: false
  }))
  const {getByRole} = render(<Login/>)
  const element = getByRole('button')
  expect(element).toHaveTextContent(/Login/i)
  expect(element).toBeEnabled()
})

test('Login button uses login function', () => {
  const loginFn = jest.fn()
  const logoutFn = jest.fn()
  useLogin.mockImplementation(() => ({
    login: loginFn,
    logout: logoutFn,
    loginReady: true,
    loggedIn: false
  }))
  const {getByRole} = render(<Login/>)
  const element = getByRole('button')
  expect(element).toHaveTextContent(/Login/i)
  fireEvent.press(element)
  expect(loginFn).toHaveBeenCalledTimes(1)
})

test('Login button is logout when logged in', () => {
  useLogin.mockImplementation(() => ({
    login: () => {},
    logout: () => {},
    loginReady: true,
    loggedIn: true
  }))
  const {getByRole} = render(<Login/>)
  const element = getByRole('button')
  expect(element).toHaveTextContent(/Logout/i)
  expect(element).toBeEnabled()
})

test('Login button is logout and uses logout function', () => {
  const loginFn = jest.fn()
  const logoutFn = jest.fn()
  useLogin.mockImplementation(() => ({
    login: loginFn,
    logout: logoutFn,
    loginReady: true,
    loggedIn: true
  }))
  const {getByRole} = render(<Login/>)
  const element = getByRole('button')
  expect(element).toHaveTextContent(/Logout/i)
  fireEvent.press(element)
  expect(logoutFn).toHaveBeenCalledTimes(1)
})

test('Login button calls useLogin on every render', () => {
  expect(useLogin).toHaveBeenCalledTimes(0)
  render(<Login/>)
  expect(useLogin).toHaveBeenCalledTimes(1)
})