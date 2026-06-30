# Source Diff Summary (Step 3.2)

**Date:** 2026-06-04
**Worktree:** `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-integrity-signalb-pass-recovered`
**Command:** `git diff -- src/superclaude/cli/sprint/resume/integrity.py src/superclaude/cli/sprint/models.py src/superclaude/cli/sprint/resume/models.py src/superclaude/cli/sprint/rerun_tasks.py`

## Full diff output

```diff
diff --git a/src/superclaude/cli/sprint/resume/integrity.py b/src/superclaude/cli/sprint/resume/integrity.py
index 32cac96e..d12623c7 100644
--- a/src/superclaude/cli/sprint/resume/integrity.py
+++ b/src/superclaude/cli/sprint/resume/integrity.py
@@ -126,9 +126,18 @@ class BoundaryIntegrityGate:
 
         # Signal B — independent re-derivation from the transcript (under lc_phase).
         transcript = self._read_transcript(results_dir, lc_phase, lc.task_id)
-        derived = _classify_transcript(transcript)
-        lc.derived_status = derived
-        signal_b_pass = derived is TaskStatus.PASS
+        if lc.persisted_status is TaskStatus.PASS_RECOVERED:
+            # PASS_RECOVERED is already transcript-evidence-based in the executor
+            # (error_max_turns after completion evidence). Preserve that recovery
+            # basis for report transparency instead of forcing the clean-PASS
+            # classifier path, which structurally cannot emit PASS_RECOVERED.
+            derived = TaskStatus.PASS_RECOVERED
+            lc.derived_status = derived
+            signal_b_pass = True
+        else:
+            derived = _classify_transcript(transcript)
+            lc.derived_status = derived
+            signal_b_pass = derived is not None and derived.is_success
 
         # Artifacts — every declared deliverable must exist. Resolve the tasklist
         # for lc's OWN phase (the prior phase for a hard-crash prior-tail). If we
```

## Summary

- **Only `integrity.py` changed.** The diff hunk is confined to the Signal B block inside `_validate_last_completed`. No other hunk appears.
- **No changes to parent sprint `models.py`** — file produced no diff (unchanged).
- **No changes to resume `models.py`** — file produced no diff (unchanged).
- **No changes to `rerun_tasks.py`** (and therefore `_classify_transcript` is untouched) — file produced no diff (unchanged).
- **Recovered branch transparency confirmed:** the new `if lc.persisted_status is TaskStatus.PASS_RECOVERED:` branch assigns `derived = TaskStatus.PASS_RECOVERED` and `lc.derived_status = derived`, so the report surfaces the recovered basis (not a fabricated clean PASS).
- **Non-recovered branch confirmed:** the `else` branch uses `signal_b_pass = derived is not None and derived.is_success` (Opt-1 widening) and still calls `_classify_transcript(transcript)`.
- **Verdict/artifacts unchanged:** the `artifacts_ok` block and `validated = signal_a_pass and signal_b_pass and artifacts_ok` are outside the hunk and remain byte-for-byte identical.

**No unexpected diff** was observed. The change matches the Opt-2a design and the no-edit boundaries. Ready for the compile check.
