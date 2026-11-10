# Database Backup Policy

Status: Draft for review. Owner: Operations team.

## 1. Purpose

This policy states how the production data of the order system is backed up and restored. It is written for the operations team and for the engineers who maintain the backup jobs.

## Common conventions

- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.

## 2. Scope and schedule

- **BK-1 Scope.** The policy covers the production database of the order system and the object store that holds uploaded documents.
- **BK-2 Schedule.** A full backup starts every night at 02:00 UTC and must finish before 05:00 UTC.
- **BK-7 Encryption.** Backups are encrypted with a key that is held by the security team and rotated once a year.

## 3. Retention

- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **BK-3 Backup retention.** Nightly backups are kept for 35 days, so that data lost through an error that is found late can still be restored.
- **BK-4 Backup overwrite.** Each nightly backup overwrites the backup of the previous night.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **BK-5 Location.** Backups are stored in a different region from the production database.
- **BK-6 Monitoring.** A backup that does not finish raises the alert `BackupLate` for the operations team.

## 4. Restore

- **BK-8 Restore test.** Once a quarter the operations team restores the latest backup into a test environment and compares row counts with production.
- **BK-9 Restore time.** A restore of the production database must be possible within four hours of the decision to restore.
- **BK-10 Access.** Only members of the operations team can start a restore, and each restore is recorded with the name of the person who started it.
- **BK-11 Reporting.** Every month the operations team sends the management a short report that lists the backup runs, the failures, the length of each run and the time each restore test took.

## 5. Acceptance criteria

1. After three nightly runs, the backup from three nights ago can be restored.
2. A backup that overruns 05:00 UTC raises `BackupLate`.
3. A restore into the test environment finishes within four hours.

## Appendix: general requirements

- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.
- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
