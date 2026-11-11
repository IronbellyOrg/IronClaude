# API Rate Limiting

Status: Draft for review. Owner: Platform team.

## 1. Purpose

This document states how the public API limits the number of requests a customer can send and what a client sees when it reaches the limit.

## 2. Principles

- **RL-1 Scope.** Limits apply per API key and not per address, so that customers behind one gateway do not share a limit.
- **RL-2 Client-owned retries.** The server never retries or replays a request on behalf of a client. A rejected request is the client's to repeat.
- **RL-3 Visibility.** A client can read its current limit and its remaining quota from the response headers of every request.
- **RL-7 Burst.** A key may exceed its per-minute rate for up to two seconds, as long as the minute total stays within the limit.
- **RL-8 Documentation.** The limits of every plan are listed in the public interface documentation.

## 3. Enforcement

- **RL-4 Limit.** Each API key may send at most 100 requests per minute.
- **RL-5 Excess requests.** Requests above the limit are rejected with HTTP 429 and a `Retry-After` header. The server then repeats the rejected request on the client's behalf, as described in RL-2.
- **RL-6 Counting.** A request is counted when the server has received it completely, whatever the result of the request.

## 4. Operations

- **RL-9 Alerting.** The platform team is alerted when more than 5 percent of all requests are rejected for longer than ten minutes.
- **RL-10 Overrides.** Support can raise the limit of one key for a limited time. Each override is recorded with its reason and its end date.
- **RL-11 Metrics.** The server counts requests, rejected requests and the largest queue length per key.

## 5. Acceptance criteria

1. The 101st request in a minute is not answered normally.
2. The rejected request tells the client when to try again.
3. The response headers show the remaining quota.
