# Notification Preferences

Status: Draft for review. Owner: Messaging team.

## 1. Purpose

This document specifies how customers control the notifications they receive from the shop and how the notification service applies those choices.

## Common conventions

- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.

## 2. Channels and preferences

- **NO-1 Channels.** The service sends notifications by e-mail, by push message and by text message. Each channel has its own sender and its own delivery log.
- **NO-6 Preference page.** A customer sets the notification preferences on the account page. The page offers one switch for marketing notifications and one for each channel.
- **NO-7 Saving.** A saved preference applies to all devices of the customer and is visible on the account page within one minute.

## 3. Opt-out

- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **NO-2 Opt-out.** A customer who opts out of marketing notifications receives none of them, on any channel, from the moment the preference is saved.
- **NO-3 Transactional messages.** Order confirmations, shipping updates and security alerts are not marketing notifications and are always sent.
- **NO-4 Purchase follow-ups.** Opted-out customers still receive marketing notifications about products they bought in the last 90 days.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **NO-5 Unsubscribe link.** Every marketing e-mail contains a link that opts the customer out with one click and without a sign-in.

## 4. Operations

- **NO-8 Sender check.** Before a marketing notification is sent, the sender looks up the preference of the customer and drops the notification when the customer has opted out.
- **NO-9 Audit.** Each change of a preference is recorded with the time, the channel and the origin of the change.
- **NO-10 Rate.** A customer receives at most three marketing notifications per week across all channels.

## 5. Acceptance criteria

1. A customer who has opted out receives no marketing notification on any channel.
2. An order confirmation is sent to a customer who has opted out.
3. The unsubscribe link opts the customer out without a sign-in.

## Appendix: general requirements

- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
