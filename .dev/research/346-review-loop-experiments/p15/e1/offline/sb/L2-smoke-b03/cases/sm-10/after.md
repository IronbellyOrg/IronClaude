# Database Backup Policy

Status: Draft for review. Owner: Operations team.

## 1. Purpose

This policy states how the production data of the order system is backed up and restored. It is written for the operations team and for the engineers who maintain the backup jobs.

## 2. Scope and schedule

- **BK-1 Scope.** The policy covers the production database of the order system and the object store that holds uploaded documents.
- **BK-2 Schedule.** A full backup starts every night at 02:00 UTC and must finish before 05:00 UTC.
- **BK-7 Encryption.** Backups are encrypted with a key that is held by the security team and rotated once a year.

## 3. Retention

- **BK-3 Backup retention.** Retention is handled by the storage platform. This revision keeps every backup obligation intact.
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
