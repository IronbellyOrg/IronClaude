# Data retention policy

## 1. Purpose
This policy sets how long the platform keeps user data and how it deletes it. It applies to every service that stores data about a user.

## 2. Categories
R1. Account data (name, email address, password hash) is kept while the account is active.
R2. Activity logs record sign-in time, IP address and the pages visited.
R3. Activity logs are kept for 180 days and then deleted by the nightly purge job.
R4. Support tickets are kept for 3 years after the ticket is closed.
R5. Backups are encrypted and kept for 35 days.

## 3. Deletion
R6. When a user deletes the account, account data is removed within 30 days.
R7. Deleted account data may remain in backups until the backups expire under R5.
R8. A legal hold suspends deletion for the data it names until the hold is lifted.
R9. The nightly purge job runs at 02:00 UTC and writes a summary line to the audit log.
R10. Closed support tickets are deleted one year after closing.

## 4. Exports
R11. A user may request an export of their account data once per calendar month.
R12. Activity logs are included in an export only when the user asks for them.

## 5. Access
R13. Only members of the data protection group may read activity logs older than 30 days.
R14. The audit log is kept for 7 years.
R15. Activity logs are kept for 90 days to limit exposure of IP addresses.

## 6. Notes
The word kept means that the data can still be read by an authorized person. The word removed means that it can no longer be read by anyone.
Each category above is owned by the team named in the data inventory.
Time periods in this policy are measured from the moment the data was created or the event named in the requirement occurred.
Questions about this policy go to the data protection group.