# Finding 2 — `_validate_evals_sync` is silently vacuous (r3312667803)

## Reviewer claim

> `_validate_evals_sync()` assumes `evals.json` provides `remediation_acceptance_scope`/`remediation_deferred_cases`, but the current `evals/evals.json` in this PR doesn't define them, so the sync check will never emit warnings. That makes the docstring claim about metadata-level scope enforcement misleading for future scope edits.

## Validation result

CONFIRMED.

Evidence (all from `origin/chore/brainstorm-live-evals` via `git show`):

- `compare_live_runs.py:45-66` defines `_validate_evals_sync(evals_data)`. Lines 53-54 read `declared = set(evals_data.get("remediation_acceptance_scope", []))` and `deferred = set(evals_data.get("remediation_deferred_cases", []))`. Both use `.get(..., [])`, so absence yields an empty set.
- Lines 55 (`if declared and declared != CASE_IDS:`) and 63 (`if deferred and deferred != EXCLUDED_CASE_IDS:`) gate the warning on `declared`/`deferred` being truthy. An empty set is falsy, so missing keys silently skip both warnings.
- `evals/evals.json` top-level keys on the PR branch are: `skill_name`, `iteration`, `scope`, `notes`, `evals`, `deferred_after_iter_2`, `assertions_v2`. Neither `remediation_acceptance_scope` nor `remediation_deferred_cases` is present (verified by reading the full file — only `deferred_after_iter_2` exists, and it contains prose strings about cases 13-15, not the integer case IDs the validator expects).
- The docstring at `compare_live_runs.py:48-51` claims "sync is enforced at the metadata level so a future evals.json change cannot accidentally broaden or narrow the compared case set without a matching edit here" — but with the keys absent, the enforcement is vacuous: any future scope edit to `evals.json` that omits these keys (i.e., the status quo) silently passes.

## Root cause

Combination of (a) and (b): the metadata keys the validator looks for were never added to `evals.json`, AND the validator uses `.get(..., [])` + truthy-check semantics that treat "missing" as "OK" rather than "missing — fail loudly." Either alone would be a bug; together they make the docstring contract unenforceable.

## Proposed fix

**Files to change:**

- `.dev/eval-workspaces/sc-brainstorm/evals/evals.json` — add two top-level keys `remediation_acceptance_scope: [4,5,6,7,8,9,10,11]` and `remediation_deferred_cases: [12]` reflecting `compare_live_runs.py:34` (`CASE_IDS = set(range(4, 12))`) and `compare_live_runs.py:35` (`EXCLUDED_CASE_IDS = {12}`).
- `.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py` lines 45-66: change `_validate_evals_sync` so missing keys emit an explicit warning instead of silently passing. Use a sentinel (`None`) to distinguish "absent" from "empty list."

**Exact diff sketch:**

```diff
 def _validate_evals_sync(evals_data: dict[str, Any]) -> None:
     """Confirm `evals.json`'s remediation acceptance scope matches this script's CASE_IDS.

     Prints a warning to stderr if they diverge OR if the metadata keys are absent.
     Missing keys are treated as a sync FAILURE (not a silent pass) so the docstring
     contract about metadata-level enforcement holds even when evals.json is edited
     by someone who doesn't know these keys exist.
     """
-    declared = set(evals_data.get("remediation_acceptance_scope", []))
-    deferred = set(evals_data.get("remediation_deferred_cases", []))
-    if declared and declared != CASE_IDS:
+    raw_declared = evals_data.get("remediation_acceptance_scope")
+    raw_deferred = evals_data.get("remediation_deferred_cases")
+    if raw_declared is None:
+        print(
+            "WARNING: evals.json is missing key `remediation_acceptance_scope`. "
+            f"Add it as a list matching compare_live_runs.py CASE_IDS={sorted(CASE_IDS)} "
+            "so future scope edits stay in sync.",
+            file=sys.stderr,
+        )
+    elif set(raw_declared) != CASE_IDS:
         print(
-            f"WARNING: evals.json remediation_acceptance_scope={sorted(declared)} "
+            f"WARNING: evals.json remediation_acceptance_scope={sorted(set(raw_declared))} "
             f"differs from compare_live_runs.py CASE_IDS={sorted(CASE_IDS)}. "
             "Update one to match the other before relying on this comparison.",
             file=sys.stderr,
         )
-    if deferred and deferred != EXCLUDED_CASE_IDS:
+    if raw_deferred is None:
+        print(
+            "WARNING: evals.json is missing key `remediation_deferred_cases`. "
+            f"Add it as a list matching compare_live_runs.py EXCLUDED_CASE_IDS={sorted(EXCLUDED_CASE_IDS)}.",
+            file=sys.stderr,
+        )
+    elif set(raw_deferred) != EXCLUDED_CASE_IDS:
         print(
-            f"WARNING: evals.json remediation_deferred_cases={sorted(deferred)} "
+            f"WARNING: evals.json remediation_deferred_cases={sorted(set(raw_deferred))} "
             f"differs from compare_live_runs.py EXCLUDED_CASE_IDS={sorted(EXCLUDED_CASE_IDS)}. "
             "Resolve the discrepancy before relying on this comparison.",
             file=sys.stderr,
         )
```

Corresponding `evals.json` additions (top-level, near `scope`/`notes`):

```json
"remediation_acceptance_scope": [4, 5, 6, 7, 8, 9, 10, 11],
"remediation_deferred_cases": [12],
```

## Risk / blast radius

Very low. Both files are evaluation tooling under `.dev/eval-workspaces/sc-brainstorm/` — not shipped, not imported by the package, not on any CI gate. Warnings go to stderr, so the change cannot break consumers that parse stdout. Adding two integer-list keys to `evals.json` is additive and cannot affect existing `evals` array consumers.

## Confidence

95% — All claims grounded in direct `git show` reads of `origin/chore/brainstorm-live-evals`. The only residual uncertainty is whether the maintainer prefers raising `ValueError` over a stderr warning for missing keys; the proposed fix mirrors the existing warning-only style for consistency, but escalating to an exception is a one-line swap if desired.
