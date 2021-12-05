import {EmailRecipient, SmsRecipient, UserRecipient} from 'mibs';
import {assert} from './assertions';

export type Recipient = EmailRecipient | SmsRecipient | UserRecipient;

/**
 * Check if a given recipient is an email recipient.
 *
 * @param {Recipient} recipient the MIBS recipient
 * @return {boolean}
 */
export const isEmail = (
  (recipient: any): recipient is EmailRecipient => !!recipient.email);

/**
 * Check if a given recipient is a SMS recipient.
 *
 * @param {Recipient} recipient the MIBS recipient
 * @return {boolean}
 */
export const isSMS = (
  (recipient: any): recipient is SmsRecipient => !!recipient.phoneNumber);

/**
 * Check if a given recipient is a user recipient.
 *
 * @param {Recipient} recipient the MIBS recipient
 * @return {boolean}
 */
export const isUser = (
  (recipient: any): recipient is UserRecipient => !!recipient.userId);

/**
 * Converts a recipient object to a string that is readable by users.
 *
 * @param {Recipient} recipient any recipient
 * @return {string} the recipient as a string if successful; `null` on failure
 *
 * Pre-conditions:
 *  isEmail exists
 *  isSMS exists
 *  isUser exists
 */
export function recipientToString(
    recipient: Recipient
): string | null {
  assert(isEmail(recipient) ||
    isSMS(recipient) || isUser(recipient), 'Invalid recipient');
  if (isEmail(recipient)) {
    return recipient.email ? recipient.email : null;
  }
  if (isSMS(recipient)) {
    return recipient.phoneNumber ? recipient.phoneNumber : null;
  }
  if (isUser(recipient)) {
    return recipient.userId ? recipient.userId : null;
  }
  return null;
}
