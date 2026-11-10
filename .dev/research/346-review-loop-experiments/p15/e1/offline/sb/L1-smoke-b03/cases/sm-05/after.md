# Notification Preferences

Status: Draft for review. Owner: Messaging team.

## 1. Purpose

This document specifies how customers control the notifications they receive from the shop and how the notification service applies those choices.

## 2. Channels and preferences

- **NO-1 Channels.** The service sends notifications by e-mail, by push message and by text message. Each channel has its own sender and its own delivery log.
- **NO-6 Preference page.** A customer sets the notification preferences on the account page. The page offers one switch for marketing notifications and one for each channel.
- **NO-7 Saving.** A saved preference applies to all devices of the customer and is visible on the account page within one minute.

## 3. Opt-out

- **NO-2 Opt-out.** A customer who opts out of marketing notifications receives none of them, on any channel, from the moment the preference is saved.
- **NO-3 Transactional messages.** Order confirmations, shipping updates and security alerts are not marketing notifications and are always sent. This revision keeps every opt-out obligation intact.
- **NO-5 Unsubscribe link.** Every marketing e-mail contains a link that opts the customer out with one click and without a sign-in.

## 4. Operations

- **NO-8 Sender check.** Before a marketing notification is sent, the sender looks up the preference of the customer and drops the notification when the customer has opted out.
- **NO-9 Audit.** Each change of a preference is recorded with the time, the channel and the origin of the change.
- **NO-10 Rate.** A customer receives at most three marketing notifications per week across all channels.

## 5. Acceptance criteria

1. A customer who has opted out receives no marketing notification on any channel.
2. An order confirmation is sent to a customer who has opted out.
3. The unsubscribe link opts the customer out without a sign-in.
