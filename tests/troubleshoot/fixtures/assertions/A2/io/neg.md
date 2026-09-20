---
assertion: A2
domain: io
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Push the collector change and re-run the CI job.
The report stays `partial` until uptime-regex=false.
--- file: diff.patch ---
--- a/test-startup-boot.sh
+++ b/test-startup-boot.sh
@@ -443,0 +444,1 @@
+echo "seed-diag-uptime-regex=${uptime_regex:-unobserved}" >> "$DIAG_OUT"
