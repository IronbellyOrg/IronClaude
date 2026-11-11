# Storage Service Uploads: Requirements

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

## 7. Rollout

Multipart upload is enabled for the standard plan first. The free plan keeps the old single-request upload with its lower limit, and the plan page lists the limit next to the price. Official clients are updated before the feature is announced, so that customers see the faster behavior at once. The team watches the number of incomplete uploads for two weeks and adjusts the cleanup message in the billing page if the share is high.

## 8. Glossary

An object is one stored file and its metadata. A part is one piece of a multipart upload. A bucket is a named container of objects owned by one customer. The plan is the commercial package that decides the limits of an account.
