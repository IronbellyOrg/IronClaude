# API Rate Limiting

Status: Draft for review. Owner: Platform team.

## 1. Purpose

This document states how the public API limits the number of requests a customer can send and what a client sees when it reaches the limit.

## Common conventions

- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.

## 2. Principles

- **RL-1 Scope.** Limits apply per API key and not per address, so that customers behind one gateway do not share a limit.
- **RL-2 Client-owned retries.** The server never retries or replays a request on behalf of a client. A rejected request is the client's to repeat.
- **RL-3 Visibility.** A client can read its current limit and its remaining quota from the response headers of every request.
- **RL-7 Burst.** A key may exceed its per-minute rate for up to two seconds, as long as the minute total stays within the limit.
- **RL-8 Documentation.** The limits of every plan are listed in the public interface documentation.

## 3. Enforcement

- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **RL-4 Limit.** Each API key may send at most 100 requests per minute.
- **RL-5 Excess requests.** Requests above the limit are rejected with HTTP 429 and a `Retry-After` header. The server then repeats the rejected request on the client's behalf, as described in RL-2.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **RL-6 Counting.** A request is counted when the server has received it completely, whatever the result of the request.

## 4. Operations

- **RL-9 Alerting.** The platform team is alerted when more than 5 percent of all requests are rejected for longer than ten minutes.
- **RL-10 Overrides.** Support can raise the limit of one key for a limited time. Each override is recorded with its reason and its end date.
- **RL-11 Metrics.** The server counts requests, rejected requests and the largest queue length per key.

## 5. Acceptance criteria

1. The 101st request in a minute is not answered normally.
2. The rejected request tells the client when to try again.
3. The response headers show the remaining quota.

## Appendix: general requirements

- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
