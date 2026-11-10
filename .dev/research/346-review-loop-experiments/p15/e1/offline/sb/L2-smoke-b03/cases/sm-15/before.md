# Session Management

Status: Draft for review. Owner: Identity team.

## 1. Purpose

This document defines how long a signed-in session lasts and which cases are allowed to keep a session open longer than usual.

## Common conventions

- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.

## 2. Lifetime

- **ST-1 Start.** A session starts when the user signs in and is tied to the device that was used to sign in.
- **ST-2 Idle limit.** A session ends after 15 minutes without a request from the user.
- **ST-3 Long operations.** A session that runs a registered long operation, such as a file upload, is kept alive until that operation ends.
- **ST-4 Sign-out.** A user can end a session at any time, and signing out ends the session on the server as well as in the browser.

## 3. Roles

- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **ST-5 Timeout obligation.** Every session ends after a period of inactivity.
- **ST-6 Administrator sessions.** Administrator sessions never time out.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **ST-8 Renewal.** A request from the user renews the idle timer of the session.
- **ST-10 Display.** The page shows the user how long the session will stay open.
- **ST-11 Storage.** Session data is kept on the server and the browser holds only an opaque identifier.

## 4. Exceptions

- **ST-7 Kiosks.** Sessions on registered kiosk devices in the operations room are kept open until the kiosk is signed out by a supervisor.
- **ST-9 Monitoring wall.** The session of a monitoring wall display is kept open as long as the display shows a dashboard.
- **ST-12 Audit.** Every session start, renewal and end is written to the audit log with the user, the device and the reason the session ended.
- **ST-13 Concurrent sessions.** A user can have at most five sessions at the same time. Starting a sixth session ends the oldest one and tells the user about it.

## 5. Acceptance criteria

1. A session without requests ends after the idle limit.
2. An upload that lasts longer than the idle limit is not interrupted.
3. Signing out ends the session on the server.

## Appendix: general requirements

- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
