**F1. CRITICAL (blocking). Expert: Whittaker (Contradiction Attack). Cleanup deletes every old file and never deletes foreign files**

- Grading sentence: an implementer who follows the stated text as written builds a cleanup that deletes every file older than 14 days in the output directory (`the service deletes every file older than 14 days from the output directory`, S:24) and never deletes files it did not create (`Files in the output directory that were not created by the service are never deleted.`, S:25). A foreign file older than 14 days must be deleted and kept, so either user data is destroyed or the rule is dead, which is wrong for a cleanup that runs on every start.
- Recommendation: limit R13 to files created by the service
- Priority: High. Quality impact: cleanup deletes every old file and never deletes foreign fil
