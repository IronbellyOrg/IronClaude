---
assertion: A2
domain: nonio
polarity: neg
expected_flags: []
artifact_mtime: 2026-09-18T18:36:00Z
---
--- file: REPORT.md ---
## Next Steps
Deploy the consumer with the extra log line and wait for the next duplicate.
The report stays `partial` until redelivered=false.
--- file: diff.patch ---
--- a/consumer.py
+++ b/consumer.py
@@ -41,0 +42,1 @@
+    log.info("redelivered=%s", getattr(msg, "redelivered", "unobserved"))
