# Backup requirements

## 1. Schedule
R1. A full backup runs every Sunday at 01:00 UTC.
R2. An incremental backup runs every other day at 01:00 UTC.
R3. A backup job that is still running when the next one is due makes the next one wait until it finishes.

## 2. Storage
R4. Backups are written to the primary storage bucket.
R5. A copy of every backup is replicated to the secondary region within 24 hours.
R6. Backups older than 35 days are deleted from the primary bucket.
R7. Backups in the secondary region are kept for 90 days.

## 3. Verification
R8. After each full backup a restore test restores it into an isolated environment.
R9. A failed restore test raises an alert to the on-call engineer.

## 4. Retention exceptions
R10. The most recent full backup is never deleted.
R11. Backups are deleted by the cleanup job that runs at 03:00 UTC.

## 5. Restore
R12. A restore overwrites the production database with the selected backup after one confirmation click.
R13. The confirmation click is the only check before a restore starts.
R14. Incremental backups run every day at 01:00 UTC.

## 6. Notes
The production database is a single primary with one standby. Backups are taken from the standby so that the primary is not slowed down.
The on-call engineer is the person listed in the current rota.
Backup files are named after the job type and the UTC time they started. The names are not parsed by any component.
The restore procedure is run by a member of the database team. The database team keeps a written runbook that is reviewed twice a year.
Storage costs are reviewed every quarter by the platform team. Any change to the schedule above is announced to the engineering mailing list one week before it takes effect.