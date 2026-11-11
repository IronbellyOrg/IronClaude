# Webhook Delivery Worker Specification

Status: Draft for review. Owner: Platform team.

## 1. Purpose

The webhook delivery worker sends event notifications from the platform to customer-registered HTTPS endpoints. It guarantees at-least-once delivery with bounded retries and gives customers a delivery log.

## Common conventions

- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.

## 2. Functional requirements

- **FR-1 Registration.** A customer registers one HTTPS endpoint URL per webhook. Plain HTTP URLs are rejected at registration with error `E_URL_SCHEME`.
- **FR-2 Request timeout.** Each delivery attempt waits at most 10 seconds for a response. A timeout counts as a failed attempt.
- **FR-3 Retry policy.** A failed attempt is retried at most 5 times (6 attempts in total). The delays between attempts are 1 minute, 5 minutes, 30 minutes, 2 hours and 12 hours. After the sixth failed attempt the delivery is marked `FAILED`.
- **FR-4 Signing.** Every request carries an `X-Signature` header: the HMAC-SHA256 of the raw request body, keyed with the webhook's signing secret. The signing secret is never written to any log.
- **FR-5 Idempotency key.** Every delivery has an idempotency key `delivery_id`, a UUID created when the event is first queued. The same `delivery_id` is sent on every retry in the `X-Delivery-Id` header, so a receiver can discard duplicates.
- **FR-6 Success.** A response with a status code from 200 to 299 marks the delivery `DELIVERED`. Any other status code is a failed attempt, except 410, which marks the delivery `GONE` and stops retries.
- **FR-7 Delivery log.** Every attempt writes one row to the delivery log with `delivery_id`, attempt number, status code or `TIMEOUT`, and the UTC time. Log rows are kept for 30 days and then deleted.
- **FR-8 Payload size.** The request body is at most 256 KiB. An event whose serialized payload is larger is not sent; the delivery is marked `FAILED` with reason `PAYLOAD_TOO_LARGE` and no attempt is made.

## 3. Ordering

Deliveries for the same webhook are not guaranteed to arrive in event order. Receivers must use the event timestamp in the payload to order events.

## 4. Operations

- The worker exposes the metric `webhook_delivery_total` labelled by final state (`DELIVERED`, `FAILED`, `GONE`).
- A delivery stuck in `QUEUED` for more than 15 minutes raises the alert `WebhookQueueStuck`.

The worker retries a failed delivery up to 8 times with exponential backoff and marks it `FAILED` after the ninth failed attempt.

## 5. Acceptance criteria

1. Registering `http://example.com/hook` returns `E_URL_SCHEME`.
2. An endpoint that always returns 500 receives exactly 6 requests with the same `X-Delivery-Id`, then the delivery is `FAILED`.
3. An endpoint that returns 410 receives exactly 1 request and the delivery is `GONE`.
4. A 300 KiB payload produces no request and the delivery is `FAILED` with reason `PAYLOAD_TOO_LARGE`.
5. No log line at any level contains the signing secret.

- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.

- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.

## Appendix: general requirements

- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
