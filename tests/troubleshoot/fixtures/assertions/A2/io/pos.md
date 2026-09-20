---
assertion: A2
domain: io
polarity: pos
expected_flags: [instrumentation_without_falsifier]
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Push the collector change and re-run the CI job.
--- file: diff.patch ---
--- a/test-startup-boot.sh
+++ b/test-startup-boot.sh
@@ -443,0 +444,1 @@
+echo "seed-diag-uptime-regex=${uptime_regex:-unobserved}" >> "$DIAG_OUT"
