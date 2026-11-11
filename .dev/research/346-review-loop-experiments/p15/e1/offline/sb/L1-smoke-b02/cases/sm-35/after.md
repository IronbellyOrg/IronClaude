# Password Reset Flow

Status: Draft for review. Owner: Identity team.

## 1. Purpose

This document specifies how a customer who has forgotten a password can set a new one, and how the reset link is protected against misuse.

## Common conventions

- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.

## 2. Request

- **PR-1 Request.** A customer asks for a reset on the sign-in page by giving the address of the account. The page answers in the same way whether the account exists or not.
- **PR-2 Delivery.** If the account exists, the service sends one message with a reset link to the address of the account.
- **PR-6 Throttle.** At most three reset requests per account are accepted per hour.

## 3. The link

- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **PR-3 One-time use.** A password reset link can be used once. After a successful reset the link stops working.
- **PR-4 Link lifetime.** A password reset link stays valid until it is used or until the customer asks for a newer link.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **PR-5 Token.** The link carries a random token of at least 32 bytes. Only a hash of the token is stored by the service.

## 4. After the reset

- **PR-7 Sessions.** A successful reset ends all sessions of the account.
- **PR-8 Notice.** The customer receives a message that says the password was changed, without the new password.
- **PR-9 Password rules.** The new password must follow the password rules of the account policy and must differ from the last five passwords.
- **PR-10 Support.** Support staff can see that a reset was requested and when, but never see the link, the token or the new password of the customer.
- **PR-11 Locked accounts.** A reset link for an account that is locked by the fraud team is not sent. The page gives the same answer as for an account that does not exist.

## 5. Acceptance criteria

1. A used link cannot be used a second time.
2. A link older than its lifetime is refused.
3. A successful reset ends the other sessions of the account.

## Appendix: general requirements

- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
