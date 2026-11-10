**F1. MAJOR, blocking. Expert: Wiegers (testability). Incremental backups run every other day and every day**

- Grading sentence: an implementer who follows the stated text as written builds a scheduler that runs an incremental backup on Monday, skips Tuesday (`An incremental backup runs every other day at 01:00 UTC.`, S:5) and runs on Tuesday as well (`Incremental backups run every day at 01:00 UTC.`, S:25). Tuesday's job must run and not run, so the schedule test cannot pass.
- Recommendation: keep one schedule
- Priority: High. Quality impact: incremental backups run every other day and every day
