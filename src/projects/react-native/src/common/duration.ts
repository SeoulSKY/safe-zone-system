import {assert} from './assertions';


/** Represents a duration of time in a human readable format. */
export class Duration {
  /** The days of the duration. */
  days: number;
  /** The hours of the duration. */
  hours: number;
  /** The minutes of the duration. */
  minutes: number;
  /** The seconds of the duration. */
  seconds: number;

  /**
   * Create a new duration from a given number of milliseconds.
   * @param {number} milliseconds the duration in milliseconds
   */
  constructor(milliseconds: number) {
    assert(milliseconds >= 0, 'milliseconds is not > 0');
    this.days = Math.floor(milliseconds / (1000 * 60 * 60 * 24));
    this.hours = Math.floor((milliseconds / (1000 * 60 * 60)) % 24);
    this.minutes = Math.floor((milliseconds / 1000 / 60) % 60);
    this.seconds = Math.floor((milliseconds / 1000) % 60);
  }

  /**
   * Converts a number to a string. If the number has less than 2 digits
   * (n < 10), then a leading zero is added when it is converted to a string.
   * @param {number} n any positive number
   * @return {number} the number as a string with at least 2 digits.
   */
  private numToStringLeadingZero(n: number): string {
    if (n < 0) {
      const absN = Math.abs(n);
      return n > -10 ? `-0${absN}` : `-${absN}`;
    } else {
      return n < 10 ? `0${n}` : `${n}`;
    }
  }

  /**
   * Returns the duration as a string. If the duration is > 24 hours,
   * the string will be in the format: `<d> day/s` where d is the days
   * of the duration. Otherwise the string will be in the format:
   * `HH:MM:SS`
   * @return {string} string representation fo the duration
   */
  toString(): string {
    if (this.days > 0) {
      return `${this.days} ${this.days == 1 ? 'day' : 'days'}`;
    } else {
      return (
        `${this.numToStringLeadingZero(this.hours)}:` +
        `${this.numToStringLeadingZero(this.minutes)}:` +
        `${this.numToStringLeadingZero(this.seconds)}`
      );
    }
  }
}
