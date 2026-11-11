# Data Retention Policy: Requirements

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

## 7. Rollout

The purge job replaces the old manual cleanup in two steps. First it runs in report-only mode for two weeks and lists the records it would purge, which the platform team checks against the old procedure. Then it is switched to real purging, store by store, starting with the search index. The backup destruction is switched last because it cannot be undone. A rollback plan exists for each step, except for the destruction of backups.

## 8. Glossary

A record is one stored customer object together with its metadata. Purging means removing the record from every store so that it cannot be read again. A store is a system that holds records: the primary database, the search index or the backups. A ticket is a case opened by the support team.
