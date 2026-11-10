**F4. MAJOR, blocking. Expert: Wiegers (testability). A restore overwrites production after one click**

- Grading sentence: an implementer who follows the stated text as written builds a restore that replaces the production database after a single click (`A restore overwrites the production database with the selected backup after one confirmation click.`, S:23), so one misclick destroys all writes made since the backup, which is wrong because it causes data loss.
- Recommendation: require a second check
- Priority: High. Quality impact: a restore overwrites production after one click
