"""Synthetic mini-specs for E2 Stage 0 (authored for p15; data class `synthetic`).  Each is 400-1,200 words.
Eight carry one seeded defect; four are clean controls with an apparent but resolved overlap."""

DOCS = {}

DOCS["uploader"] = """# Archive Uploader: Requirements

## 1. Purpose

The uploader packs the project directory into an archive each night and sends it to the vault. It runs on build agents that are shared with other jobs, so it has to behave well next to them. This document lists what the uploader must do and what it must not do.

## 2. Resource rules

- UP-1: The uploader must never hold more than 20 MB of its working data in RAM at any moment.
- UP-2: The uploader writes a progress line to the job log every 30 seconds.
- UP-3: The uploader exits with a non-zero code when the vault rejects a part of the upload.
- UP-4: The uploader uses at most two CPU cores.

## 3. Inputs

Archives are built from the project directory. Typical archives are 50 MB; archives of monorepo projects range up to 500 MB. The list of paths to include is read from `uploads.cfg`, one path per line. Paths that do not exist are skipped and named in the job log.

## 4. Transfer behavior

- UP-5: Each archive is sent in one request to the vault endpoint.
- UP-6: The uploader loads the complete archive into memory, then signs it and sends it.
- UP-7: The signature header carries the SHA-256 of the full body.
- UP-8: The request is sent over TLS only; a plain connection is refused.

## 5. Failure handling

When the vault answers with a server error, the uploader waits one minute and tries once more. When the second attempt fails, the job ends and the archive is left on disk for the next night.

| Exit code | Meaning | Archive kept |
|---|---|---|
| 0 | Archive stored | no |
| 2 | Vault rejected the archive | yes |
| 3 | Vault unreachable after the retry | yes |
| 4 | Input list missing or unreadable | no |

## 6. Logging

The job log contains one line per skipped path, one line per attempt and the progress lines from UP-2. The log never contains file contents or the signature value.

## 7. Open items

The team has not decided where the archive is stored while the job runs. The build agents have 8 GB of disk and 16 GB of RAM in total, shared with other jobs.
"""

DOCS["export"] = """# Report Export Service: Requirements

## 1. Overview

Users export project reports from the web page as a ZIP file. Small exports finish in seconds. A full-project export reads every report and can take a long time. The service must stay secure and must stay usable while a long export runs.

## 2. Security

- SEC-1: A session token expires after 15 minutes without user input.
- SEC-2: An expired token is rejected by every endpoint of the service.
- SEC-3: Tokens are never written to logs.
- SEC-4: Passwords are checked against a breached-password list when they are set.

## 3. Export jobs

- EXP-1: A user starts an export by choosing a report set and pressing Export.
- EXP-2: The service queues the job and shows a progress bar on the open page.
- EXP-3: A full-project export can run for up to 2 hours. The user does not need to touch the page while it runs, and the download link is delivered to the open page when the job is done.
- EXP-4: The page polls the job endpoint every 10 seconds and authenticates each poll with the user's session token.
- EXP-5: A finished export stays downloadable for 24 hours.

## 4. Progress display

The progress bar shows the share of reports already written. The page shows the report currently being read and an estimate of the time left. The estimate is recomputed on each poll and is never shown as less than one minute.

## 5. Failure handling

If the job fails, the page shows the failure reason from the job endpoint and offers to restart the export. A restart creates a new job; the failed job is deleted after 7 days.

| Failure reason | Shown to the user | Restart offered |
|---|---|---|
| report_unreadable | A report could not be read | yes |
| quota_exceeded | The ZIP would be too large | no |
| internal_error | Something went wrong | yes |

## 6. Limits

A user may run at most two exports at the same time. A ZIP file is limited to 2 GB. The service refuses to start an export that would exceed the limit and names the reports that cause it.
"""

DOCS["digest"] = """# Digest Mailer: Requirements

## 1. Purpose

The mailer sends each user a daily summary of the activity in the projects the user follows. The summary is a plain email with a list of changed items. This document defines what is sent, to whom and when.

## 2. Privacy

- PRIV-1: The service stores only the email address, the display name and the list of followed projects for each user.
- PRIV-2: The service holds no information about where a user is, including the user's time zone.
- PRIV-3: Email addresses are never shown to other users.
- PRIV-4: A user can delete the account; all stored data is removed within seven days.

## 3. Content

- DIG-2: The digest lists at most 20 changed items, newest first.
- DIG-3: Items beyond the twentieth are summarized as a count ("and 14 more").
- DIG-4: Each item links to the page of the changed object.
- DIG-5: A user with no changes in the last day receives no digest.

## 4. Schedule

- DIG-1: Each user's digest is sent at 08:00 in that user's local morning.
- DIG-6: The sending job starts at 05:00 UTC and finishes by 23:00 UTC.
- DIG-7: A digest that has not been sent by the end of the job is dropped and not retried the next day.

## 5. Delivery

The mailer hands each message to the mail relay and records the relay's answer. A permanent failure from the relay marks the address as invalid, and no further digests are tried for it until the user changes the address.

| Relay answer | Action |
|---|---|
| accepted | record the message as sent |
| temporary failure | retry after 15 minutes, up to three times |
| permanent failure | mark the address invalid |

## 6. Unsubscribe

Every digest ends with an unsubscribe link. Following the link stops all digests for that user at once and shows a confirmation page. The user can turn digests back on in the account settings.
"""

DOCS["retention"] = """# Data Retention Policy: Requirements

## 1. Scope

This policy covers the customer records held in the primary database, the search index and the nightly backups. It applies to every record that a customer or an administrator deletes. It sets the time limits the platform must meet so that the company can answer privacy requests.

## 2. Retention rules

- RET-1: Every deleted record is purged from all stores within 30 days of deletion, with no exceptions.
- RET-2: The purge job runs every night at 02:00 and processes records in order of deletion date.
- RET-3: The search index is rebuilt weekly so that purged records disappear from it.
- RET-4: Backups older than 35 days are destroyed.

## 3. Holds and tickets

- RET-5: A deleted record that is referenced by an open support ticket is kept until the ticket closes.
- RET-6: When the ticket closes, the record is purged by the next nightly run.
- RET-7: Support staff can see a deleted record only while it is kept under RET-5.

## 4. Evidence

The purge job writes a line per purged record to the audit log with the record id, the store and the time. The audit log does not contain record contents. The log is kept for 12 months so that the company can show that a purge happened.

## 5. Responsibilities

| Role | Duty |
|---|---|
| Platform team | Runs and monitors the purge job |
| Support lead | Closes stale tickets every quarter |
| Privacy officer | Reviews the audit log sample each month |

## 6. Reporting

The privacy officer receives a monthly report with the number of records purged, the age of the oldest deleted record still in the system and the number of purge failures. A failure is any record still present 30 days after its deletion.
"""

DOCS["ratelimit"] = """# Public API Rate Limits: Requirements

## 1. Purpose

The public API serves customers with very different traffic. To protect the platform, every key is limited. This document defines the limits, how they are reported and what a client sees when it exceeds them.

## 2. Limits

- RL-1: Every API key is limited to 100 requests per minute. This limit is fixed and cannot be raised for any key.
- RL-2: The limit is counted per key over a sliding window of one minute.
- RL-3: Requests rejected by the limit are not counted again.
- RL-4: Health-check requests from the platform's own monitors are not counted.

## 3. Reporting to clients

- RL-5: Every response carries the headers `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset`.
- RL-7: A rejected request gets status 429 and a `Retry-After` header with the number of seconds to wait.

## 4. Key classes

- RL-6: Enterprise keys are allowed 1,000 requests per minute.
- RL-8: Trial keys are valid for 14 days and are limited like any other key.

## 5. Monitoring

The platform records the number of rejected requests per key per hour. An alert fires when a key is rejected more than 500 times in an hour, because this usually means a broken client loop. The alert goes to the support queue, not to the customer.

| Metric | Granularity | Retention |
|---|---|---|
| Accepted requests | per key per minute | 30 days |
| Rejected requests | per key per hour | 90 days |
| Latency of the limiter | per minute | 7 days |

## 6. Client guidance

Clients should read `X-RateLimit-Remaining` and slow down before it reaches zero. After a 429 they must wait for the time in `Retry-After` and must not retry earlier. Documentation for clients repeats these rules and gives example code.
"""

DOCS["payments"] = """# Payment Gateway Client: Requirements

## 1. Purpose

The gateway client sends payment operations from the shop backend to the card processor. It must be safe against duplicate charges and must give up cleanly when the processor is slow. This document defines the retry behavior and the call types.

## 2. Calls

- PAY-1: The client supports three call types: authorize, capture and refund.
- PAY-2: A capture that times out is retried three times following RTY-1.
- PAY-4: Each call carries an idempotency key built from the order id and the call type.
- PAY-5: Every call is logged with its idempotency key and its outcome.

## 3. Retry rules

- RTY-1: The number of retries for a call is the retry budget listed for its call type in TIER-1.
- RTY-2: Retries wait 2 seconds, then 4 seconds, then 8 seconds.
- RTY-3: A retry reuses the idempotency key of the first attempt.

## 4. Tiers

The call types belong to tiers that decide how risky a repeat is.

| Id | Call type | Retry budget | Reason |
|---|---|---|---|
| TIER-1 | capture | 0 | a repeat could charge the customer twice |
| TIER-1 | authorize | 3 | an authorization can be repeated safely |
| TIER-1 | refund | 1 | a second refund is rejected by the processor |

## 5. Timeouts

A call times out after 20 seconds. A timed-out call is treated as unknown: the client asks the processor for the status of the idempotency key before it decides what to do next.

## 6. Errors

The client maps processor errors to three outcomes: declined, failed and unknown. Declined and failed are final. An unknown outcome is resolved by a status request as described in section 5. The shop backend never shows raw processor messages to customers.
"""

DOCS["locks"] = """# Order Worker: Requirements

## 1. Purpose

Order workers process paid orders from a queue. Several workers run at once, so they protect each order with a lock. This document defines the locking and timing rules of a worker.

## 2. Processing

- ORD-1: A worker takes one order from the queue at a time.
- ORD-2: A worker marks the order as in progress before it does any work on it.
- PAY-3: A payment capture takes 2 seconds, and the worker holds its lock for the whole capture (LOCK-2).
- ORD-3: When capture succeeds, the worker writes the receipt and removes the order from the queue.

## 3. Locks

- LOCK-1: A worker takes the lock of an order before it changes the order.
- LOCK-2: A lock is held for at most 5 ticks (see CFG-1 for the tick).
- LOCK-3: A lock that is held longer is released by the lock service, and the order returns to the queue.
- LOCK-4: A worker that loses its lock stops working on the order at once.

## 4. Configuration

- CFG-1: One tick is 100 milliseconds.
- CFG-2: The queue poll interval is 1 second.
- CFG-3: A worker sends a heartbeat to the lock service every 10 ticks.

## 5. Capacity

| Setting | Value |
|---|---|
| Workers per node | 4 |
| Orders per worker per minute | 20 |
| Queue length alarm | 500 orders |

## 6. Failure handling

If a worker crashes, its locks expire and the orders return to the queue. The receipt writer is idempotent, so an order that was already finished is not charged again. Operators can inspect a stuck order in the admin page, which shows the owner of its lock and the age of the lock.
"""

DOCS["gateway"] = """# Upload Gateway: Requirements

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
"""

DOCS["logs_tier"] = """# Project Logging: Requirements

## 1. Purpose

Every project on the platform produces logs from its builds and its running services. Customers use the logs to find faults. The platform keeps them for a limited time that depends on the plan of the project.

## 2. Retention

- LOG-1: Projects on the free tier keep logs for 7 days.
- LOG-2: Projects on the paid tier keep logs for 30 days.
- LOG-3: When a project changes tier, the new retention applies to logs written from that moment on.
- LOG-4: Expired logs are deleted by the nightly cleanup.

## 3. Access

- LOG-5: Project members can read the logs of their project in the web console.
- LOG-6: Members can download up to 100 MB of logs per request.
- LOG-7: Logs can be filtered by service and by severity.

## 4. Content

Logs contain the text lines written by the services. The platform adds a timestamp and the name of the service to every line. Lines longer than 8 KB are cut and marked as cut. The platform does not look into the lines, so secrets written by a service end up in the logs; the documentation tells customers to avoid this.

| Field | Added by | Example |
|---|---|---|
| timestamp | platform | 2026-03-02T10:15:00Z |
| service | platform | api |
| severity | service | warn |
| message | service | cache miss |

## 5. Storage

Logs are stored in compressed form in the regional object store. Compression cuts the size by a factor of about five. Reading logs older than one day is slower than reading recent logs, and the console says so when a search spans a longer period.

## 6. Limits

A project can write up to 1 GB of logs per day. Above that, the platform drops the oldest lines of the day first and adds a notice line to the log.
"""

DOCS["passwords"] = """# Account Security: Requirements

## 1. Purpose

This document defines how accounts of the admin console are protected. It covers passwords, sessions and the special accounts that automation uses. It is read by the identity team and by the teams that connect their services to the console.

## 2. Passwords

- AUTH-1: A password has at least 12 characters.
- AUTH-2: A password is never stored in readable form; only a salted hash is kept.
- AUTH-3: Passwords expire after 90 days.
- AUTH-4: After expiry the user must choose a new password at the next sign-in.
- AUTH-5: A new password must differ from the last five passwords.

## 3. Sessions

- AUTH-6: A sign-in session ends after 12 hours.
- AUTH-8: Three failed sign-ins lock the account for 15 minutes.

## 4. Service accounts

- AUTH-7: Service accounts are exempt from AUTH-3; their credentials are rotated by the secrets manager every 24 hours.
- AUTH-9: Service accounts cannot sign in through the web page.
- AUTH-10: A service account is owned by exactly one team, named in its description.

## 5. Audit

Every sign-in, every failed sign-in and every password change is written to the audit log with the account name, the time and the source address. The audit log is read-only for administrators. The identity team reviews failed sign-in spikes each Monday.

| Event | Logged fields | Alert |
|---|---|---|
| sign-in | account, time, address | no |
| failed sign-in | account, time, address | at five in a minute |
| password change | account, time | no |

## 6. Recovery

A user who has forgotten the password asks for a reset link by email. The link is valid for one hour and can be used once. Using it counts as a password change under AUTH-5.
"""

DOCS["multipart"] = """# Storage Service Uploads: Requirements

## 1. Purpose

The storage service keeps customer objects. Customers upload objects of very different sizes, from small text files to large disk images. This document defines how uploads work and which plans can use which feature.

## 2. Upload rules

- STO-1: Uploads over 5 GB must use multipart upload.
- STO-2: Uploads over 5 GB are rejected on the free plan.
- STO-3: A multipart upload consists of parts of at least 16 MB, except the last part.
- STO-4: A multipart upload can be resumed within seven days of its start.
- STO-5: Incomplete multipart uploads older than seven days are deleted.

## 3. Plans

| Plan | Largest object | Multipart |
|---|---|---|
| Free | 5 GB | not available |
| Standard | 5 TB | available |
| Enterprise | 5 TB | available |

## 4. Integrity

Each part carries its checksum, and the service verifies it before it accepts the part. When the upload is completed, the service combines the part checksums into one object checksum and returns it. Clients should compare it with their own value.

## 5. Billing

Stored bytes are billed monthly. Parts of an incomplete multipart upload are billed until they are deleted. The billing page shows the stored bytes per bucket and the share of incomplete uploads, so customers can clean them up earlier than the automatic deletion.

## 6. Client behavior

The official clients choose multipart upload on their own when an object is larger than 100 MB, because it is faster and can be resumed. They show a clear message when the plan does not allow the size, and they do not start the transfer in that case.
"""

DOCS["freeze"] = """# Release Rules: Requirements

## 1. Purpose

These rules describe when the platform may be deployed. They protect the busy periods of the business and keep the number of risky changes low. They apply to all services that customers use directly.

## 2. Deployment rules

- REL-1: Deployments run through the pipeline; manual deployments are not allowed.
- REL-2: Every deployment needs one approval from a person who did not write the change.
- REL-3: Deployments start on weekdays between 09:00 and 16:00 local time.
- REL-4: No deployments during the last week of each quarter.
- REL-5: A deployment that fails its health check is rolled back automatically.

## 3. Exceptions

- REL-9: Security patches may be deployed at any time, including during the freeze in REL-4.
- REL-10: A security patch still goes through the pipeline and needs the approval from REL-2.
- REL-11: The security lead decides whether a change counts as a security patch and records the decision in the change.

## 4. Communication

The release manager posts the freeze dates for the next four quarters in the engineering channel at the start of each year. Before each freeze a reminder is posted one week ahead. During the freeze, the channel topic shows the end date.

| Moment | Who posts | Where |
|---|---|---|
| Start of year | release manager | engineering channel |
| One week before a freeze | release manager | engineering channel |
| After a security patch | security lead | engineering channel |

## 5. Reporting

Each quarter the release manager reports the number of deployments, the number of rollbacks and the number of security patches deployed during freezes. The report is reviewed in the engineering leadership meeting. A rise in rollbacks leads to a review of the health checks.
"""


EXTRA = {
"uploader": """
## 8. Rollout

The uploader is first enabled on one build agent for a week. The team compares the job logs of that agent with the old backup script and checks that every night produced an archive in the vault. After the trial the uploader replaces the old script on all agents, one agent per day. The old script stays installed for a month so the team can switch back. Support for new storage targets is out of scope for this version, and so is encryption of archives before they leave the agent; both are tracked in the backlog for the next version.

## 9. Glossary

An archive is one compressed file built from the project directory. The vault is the storage service that receives archives. A part is a piece of an upload that the vault accepts or rejects as a unit. A build agent is a machine that runs jobs of several teams.
""",
"export": """
## 7. Rollout

The new export page is released to ten percent of users first. The team watches the failure rate and the time to the first progress update for one week. If the failure rate stays below one percent, the page is released to everyone. The old export button stays available through a link in the page footer for one more month. Support staff receive a short guide with the failure reasons from section 5 and the actions they may take for each of them.

## 8. Glossary

A report is one document generated from project data. A report set is a group of reports chosen for one export. A job is the queued work that builds the ZIP file. The job endpoint is the part of the service that returns the status and, when done, the download link.
""",
"digest": """
## 7. Rollout

The mailer starts with the staff of the company as the first recipients. After two weeks without complaints, it is enabled for customers who opted in, and a month later for everyone. The team tracks the unsubscribe rate per week; a rate above two percent stops the rollout until the content has been reviewed. Templates are reviewed by the design team before each stage, and the plain-text version is checked in three mail clients.

## 8. Glossary

A digest is the single daily email. A followed project is a project the user chose to receive changes from. The relay is the outgoing mail service the company already runs. An item is one changed object, for example a page, a task or a comment.
""",
"retention": """
## 7. Rollout

The purge job replaces the old manual cleanup in two steps. First it runs in report-only mode for two weeks and lists the records it would purge, which the platform team checks against the old procedure. Then it is switched to real purging, store by store, starting with the search index. The backup destruction is switched last because it cannot be undone. A rollback plan exists for each step, except for the destruction of backups.

## 8. Glossary

A record is one stored customer object together with its metadata. Purging means removing the record from every store so that it cannot be read again. A store is a system that holds records: the primary database, the search index or the backups. A ticket is a case opened by the support team.
""",
"ratelimit": """
## 7. Rollout

The limiter runs in shadow mode for two weeks: it counts requests and writes what it would have rejected, but it rejects nothing. The platform team reviews the shadow numbers with the largest customers before the limiter is switched on, so that nobody is surprised. After the switch, the first week is watched closely, and the alert threshold from section 5 can be adjusted by the platform team without a new version of this document.

## 8. Glossary

A key is the secret string a customer sends with each request. A window is the period over which requests are counted. A rejected request is one the limiter refuses before any work is done. A monitor is a platform component that calls the health endpoint on a schedule.
""",
"payments": """
## 7. Rollout

The new client is deployed behind a switch that sends one percent of orders through it. The team compares declined, failed and unknown outcomes between the old and the new client daily. When the numbers match for a week, the share is raised in steps up to all orders. The old client stays in the code base for one release to allow a switch back. Duplicate-charge reports from customer support are reviewed by the payments team the same day during the rollout.

## 8. Glossary

An idempotency key is a value that lets the processor recognize a repeated call. Authorize reserves money on a card, capture takes the reserved money and refund returns it. The processor is the external company that talks to the card networks.
""",
"locks": """
## 7. Rollout

The workers are rolled out one node at a time. After each node the team checks the age of the oldest order in the queue and the number of locks released by the lock service. If the oldest order is older than ten minutes, the rollout pauses. The lock service itself is not changed in this version. Operators get a short runbook that explains how to read the lock owner and the lock age in the admin page, and how to return a stuck order to the queue by hand.

## 8. Glossary

An order is one paid purchase waiting for fulfilment. A lock is a short claim on an order held in the lock service. A heartbeat is a message that tells the lock service the worker is still alive. The receipt is the document the customer gets after capture.
""",
"gateway": """
## 7. Rollout

The gateway is released to the Android app first, then to the iOS app one week later. The app teams get the list of error codes and the size limits before the release. During the first week the platform team watches the rate of rejected uploads by app version. A change of a size limit is announced two weeks ahead in the app teams' channel, because the apps contain the same limit for their own checks and must be updated in step.

## 8. Glossary

The gateway is the service described here. The proxy is the reverse proxy that terminates TLS in front of it. The media service stores and converts uploaded files. An upload is one POST request carrying one file.
""",
"logs_tier": """
## 7. Rollout

The retention rules are first applied to new projects. Existing projects keep their current behavior for a month while their owners are informed by email about the new rules and about the tier they are on. After that month the cleanup job uses the new rules for all projects. The console shows the retention of the project in the header of the log page, so a user always sees how far back the logs go.

## 8. Glossary

A tier is the plan a project is on: free or paid. A service is a running component of the project that writes logs. The cleanup job is the nightly process that removes expired logs. The console is the web page where customers manage projects.
""",
"passwords": """
## 7. Rollout

The new rules are enabled for staff accounts first. After a month, they are enabled for customer administrators with a warning banner that appears two weeks before the first expiry. Service accounts are moved to the secrets manager before the rules are enabled for customers, so that no automation breaks. The identity team keeps a list of accounts that could not be moved and reviews it weekly until the list is empty.

## 8. Glossary

An account is a named identity that can sign in. A service account is an identity used by automation. The secrets manager is the system that stores and rotates credentials. A session is the period during which a signed-in user does not need to enter the password again.
""",
"multipart": """
## 7. Rollout

Multipart upload is enabled for the standard plan first. The free plan keeps the old single-request upload with its lower limit, and the plan page lists the limit next to the price. Official clients are updated before the feature is announced, so that customers see the faster behavior at once. The team watches the number of incomplete uploads for two weeks and adjusts the cleanup message in the billing page if the share is high.

## 8. Glossary

An object is one stored file and its metadata. A part is one piece of a multipart upload. A bucket is a named container of objects owned by one customer. The plan is the commercial package that decides the limits of an account.
""",
"freeze": """
## 6. Rollout

The rules take effect at the start of the next quarter. The release manager runs a short briefing for all teams in the last week of the current quarter and answers questions in the engineering channel. Teams that cannot meet the weekday window because they work in another time zone ask the release manager for a named deployer in their region. The rules are reviewed once a year, together with the freeze dates.

## 7. Glossary

The pipeline is the automated system that builds, tests and deploys changes. A rollback returns a service to the previous version. A health check is an automated test of a service after a deployment. A freeze is a period in which deployments are limited by these rules.
""",
}
for _k, _v in EXTRA.items():
    DOCS[_k] = DOCS[_k].rstrip("\n") + "\n" + _v
