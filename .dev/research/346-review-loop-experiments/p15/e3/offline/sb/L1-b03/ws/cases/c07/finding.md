**F1. CRITICAL (blocking). Expert: Whittaker (Contradiction Attack). Activity logs are kept for 180 days and for 90 days**

- Grading sentence: an implementer who follows the stated text as written builds a purge job that deletes activity logs after 180 days (`Activity logs are kept for 180 days and then deleted by the nightly purge job.`, S:9) and also after 90 days (`Activity logs are kept for 90 days to limit exposure of IP addresses.`, S:27). Logs between 90 and 180 days old must both exist and not exist, and IP addresses stay exposed beyond the stated limit, which is wrong for a retention policy.
- Recommendation: keep one period
- Priority: High. Quality impact: activity logs are kept for 180 days and for 90 days
