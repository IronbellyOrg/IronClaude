# Webhook Delivery Worker Specification

Status: Draft for review. Owner: Platform team.

## 1. Purpose

The webhook delivery worker sends event notifications from the platform to customer-registered HTTPS endpoints. It guarantees at-least-once delivery with bounded retries and gives customers a delivery log.

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

A failed delivery is retried by the worker up to 8 times with exponential backoff, and it is marked `FAILED` after the ninth failed attempt.

## 5. Acceptance criteria

1. Registering `http://example.com/hook` returns `E_URL_SCHEME`.
2. An endpoint that always returns 500 receives exactly 6 requests with the same `X-Delivery-Id`, then the delivery is `FAILED`.
3. An endpoint that returns 410 receives exactly 1 request and the delivery is `GONE`.
4. A 300 KiB payload produces no request and the delivery is `FAILED` with reason `PAYLOAD_TOO_LARGE`.
5. No log line at any level contains the signing secret.
