# Session Management

Status: Draft for review. Owner: Identity team.

## 1. Purpose

This document defines how long a signed-in session lasts and which cases are allowed to keep a session open longer than usual.

## 2. Lifetime

- **ST-1 Start.** A session starts when the user signs in and is tied to the device that was used to sign in.
- **ST-2 Idle limit.** A session ends after 15 minutes without a request from the user.
- **ST-3 Long operations.** A session that runs a registered long operation, such as a file upload, is kept alive until that operation ends.
- **ST-4 Sign-out.** A user can end a session at any time, and signing out ends the session on the server as well as in the browser.

## 3. Roles

- **ST-5 Timeout obligation.** Every session ends after a period of inactivity.
- **ST-6 Administrator sessions.** Administrator sessions never time out.
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
