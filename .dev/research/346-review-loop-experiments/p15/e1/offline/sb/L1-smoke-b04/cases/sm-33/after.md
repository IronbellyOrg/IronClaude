# Report Export Service

Status: Draft for review. Owner: Reporting team.

## 1. Purpose

The export service lets tenants download their reports as files. This document states how the files are produced, stored and removed.

## 2. Formats

- **EX-1 Formats.** An export is produced as a CSV file or as a JSON file, as chosen by the requester. CSV files use UTF-8 and a comma as the separator.
- **EX-6 Size.** An export contains at most one million rows. A request for more rows is split into several files of at most one million rows each.
- **EX-7 Naming.** An export file is named after the report, the date and a running number, for example `orders-2026-03-01-001.csv`.

## 3. Storage

- **EX-2 Tenant isolation.** An export file can be read only by the tenant that requested it.
- **EX-3 API exports.** Exports requested through the API are written to the tenant directory `/exports/<tenant>/<date>/`, which only that tenant can read. Both export paths now satisfy the tenant isolation rule.
- **EX-4 Batch exports.** Exports produced by the nightly batch are written to the shared directory `/shared/exports/<date>/`.
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
