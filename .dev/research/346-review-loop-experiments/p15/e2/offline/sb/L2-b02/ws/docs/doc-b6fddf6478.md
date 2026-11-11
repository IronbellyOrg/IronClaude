# Upload Gateway: Requirements

## 1. Purpose

The upload gateway accepts files from the mobile apps and passes them to the media service. It sits behind a reverse proxy that handles TLS. This document defines the size rules and the error behavior at the edge.

## 2. Gateway rules

- GW-1: The gateway accepts only POST requests on the path /upload.
- GW-2: Request bodies are limited to 10 MB.
- GW-3: Requests with a larger body are answered with status 413 and a short message.
- GW-4: The gateway streams accepted bodies to the media service without storing them on disk.

## 3. Proxy rules

- NGX-1: The proxy in front of the gateway rejects bodies larger than 10 Mbit.
- NGX-2: The proxy closes idle connections after 60 seconds.
- NGX-3: The proxy adds the header `X-Request-Id` to every request.

## 4. Media types

The gateway accepts JPEG, PNG and MP4 files. It checks the declared type against the first bytes of the body and rejects a mismatch with status 415. Other types are rejected without reading the body.

| Type | Typical size | Notes |
|---|---|---|
| JPEG | 3 MB | photos from the phone camera |
| PNG | 2 MB | screenshots |
| MP4 | 8 MB | clips of at most 10 seconds |

## 5. Errors

Errors are returned as small JSON bodies with a `code` and a `message`. The `code` values are stable and documented for the app teams. The gateway never includes internal host names in a message.

## 6. Observability

The gateway counts accepted and rejected uploads per minute and records the size of each accepted body in a histogram. A sudden rise in rejections with status 413 raises an alert, because it usually follows an app release that sends larger files.

## 7. Rollout

The gateway is released to the Android app first, then to the iOS app one week later. The app teams get the list of error codes and the size limits before the release. During the first week the platform team watches the rate of rejected uploads by app version. A change of a size limit is announced two weeks ahead in the app teams' channel, because the apps contain the same limit for their own checks and must be updated in step.

## 8. Glossary

The gateway is the service described here. The proxy is the reverse proxy that terminates TLS in front of it. The media service stores and converts uploaded files. An upload is one POST request carrying one file.
