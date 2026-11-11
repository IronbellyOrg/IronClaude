# Report Export Service

Status: Draft for review. Owner: Reporting team.

## 1. Purpose

The export service lets tenants download their reports as files. This document states how the files are produced, stored and removed.

## Common conventions

- **DX-2 Colour contrast.** Text and background colours keep a contrast ratio of at least 4.5 to 1 in every theme the product offers.
- **DX-3 Date display.** Dates are shown in the format of the user's locale and are stored in UTC.
- **DX-4 Time zones.** Scheduled times are entered in the user's time zone and converted to UTC before they are saved.
- **DX-5 Log format.** Every service writes one JSON object per log line with a timestamp, a severity and a request identifier.
- **DX-6 Log storage.** Application logs are kept for 14 days in hot storage and are then discarded by the logging platform.
- **DX-7 Health endpoint.** Each service exposes a health endpoint that answers within one second and reports the state of its dependencies.
- **DX-8 Canary releases.** A release is deployed to a canary group first and is widened only after 30 minutes without new errors.
- **DX-9 Feature flags.** A feature flag has an owner and a removal date, and flags older than 90 days are listed in a weekly report.

## 2. Formats

- **EX-1 Formats.** An export is produced as a CSV file or as a JSON file, as chosen by the requester. CSV files use UTF-8 and a comma as the separator.
- **EX-6 Size.** An export contains at most one million rows. A request for more rows is split into several files of at most one million rows each.
- **EX-7 Naming.** An export file is named after the report, the date and a running number, for example `orders-2026-03-01-001.csv`.

## 3. Storage

- **DX-10 Configuration.** Configuration values are read at start-up, and a change needs a restart unless the value is marked as reloadable.
- **DX-11 Error pages.** Error pages show a short message and a support code and never show stack traces or internal host names.
- **DX-12 Pagination.** List endpoints return at most 100 items per page together with a cursor that points at the next page.
- **DX-13 Search order.** Search results are ordered by relevance and then by recency, and an empty query returns no results.
- **EX-2 Tenant isolation.** An export file can be read only by the tenant that requested it.
- **EX-3 API exports.** Exports requested through the API are written to the shared directory `/shared/exports/<date>/`.
- **EX-4 Batch exports.** Exports produced by the nightly batch are written to the shared directory `/shared/exports/<date>/`.
- **DX-14 Image upload.** Uploaded images are scaled to a maximum width of 1600 pixels and stripped of embedded location data.
- **DX-15 Translations.** Every user-facing string comes from a translation file, and a missing translation falls back to English.
- **DX-16 Money format.** Monetary amounts are handled as integers in the smallest currency unit and are rounded half up for display.
- **DX-17 Metric names.** Metric names use lower-case words separated by underscores and end with the unit of the measured value.
- **EX-5 Download link.** The requester receives a download link that is valid for 24 hours and that names the file.

## 4. Housekeeping

- **EX-8 Clean-up.** Export files are deleted 7 days after they were written.
- **EX-9 Notification.** The requester is told by message when an export is ready or when it failed.
- **EX-10 Failure.** A failed export leaves no partial file behind.
- **EX-11 Usage report.** Every week the product team receives a report that lists the number of exports per report type, the average size of an export and the number of failed exports.
- **EX-12 Concurrency.** A tenant can have at most three exports running at the same time. Further requests wait in a queue and start in the order in which they arrived.

## 5. Acceptance criteria

1. An export requested through the API can be downloaded by the requesting tenant.
2. A second tenant cannot read the files of the first tenant.
3. Files older than 7 days are gone.

## Appendix: general requirements

- **DX-18 Library updates.** Third-party libraries are checked for published security advisories once a month by the owning team.
- **DX-19 Interface docs.** Every public endpoint is described in the interface documentation before the release that contains it ships.
- **DX-20 Support hours.** The support team answers tickets on business days between 08:00 and 18:00 in the local time of the customer.
- **DX-21 Test data.** Test environments use generated data only and never contain copies of records that belong to real customers.
- **DX-22 Feedback form.** A feedback form is available on every page and sends its text to the product team without a reply address.
- **DX-23 Cookies.** The site sets only the cookies that are needed for sign-in and for the language choice of the visitor.
- **DX-24 Print layout.** Pages that customers may print have a print stylesheet that hides the navigation and shows the address of the page.
- **DX-1 Keyboard access.** All interactive elements can be reached and used with the keyboard alone, and the element that has focus is always visible.
