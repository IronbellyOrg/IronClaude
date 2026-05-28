# Finding 4 — grader.py aborts on missing variant subdir (r3312667808)

## Reviewer claim

> Writing `with_skill/grading.json` and `old_skill/grading.json` assumes those directories already exist; if an eval dir has `eval_metadata.json` but is missing one of those subdirs, the grader will raise and abort the whole run. That makes the grader fragile to partially-populated iteration folders.

## Validation result

**CONFIRMED**

Evidence (file = `.dev/eval-workspaces/sc-brainstorm/grader.py` on `origin/chore/brainstorm-live-evals`):

- Lines 237-238 write unconditionally:

  ```python
  (eval_dir / "with_skill" / "grading.json").write_text(json.dumps(with_grading, indent=2))
  (eval_dir / "old_skill" / "grading.json").write_text(json.dumps(old_grading, indent=2))
  ```

  No `parent.mkdir(...)`, no `is_dir()` guard, no `try/except`. If `eval_dir/with_skill/` does not exist, `Path.write_text` raises `FileNotFoundError`.
- `check_assertion` at line 183 (`if not target_path.exists() or not target_path.is_dir(): ...`) already handles missing variant subdirs gracefully and `build_grading` (lines 210-231) produces a valid dict even when every assertion fails — so the pipeline produces a writable grading dict, but the write itself blows up.
- `main()` (lines 257-266) iterates all `eval-*/` dirs in order. Because each `grade_eval` call is unguarded, the first eval-dir with a missing variant subdir raises and the whole loop terminates — exactly what the reviewer described.

## Root cause

Unconditional `Path.write_text` on a path whose parent directory's existence is never verified or created. `check_assertion` is defensive about missing variant subdirs but the write step is not.

## Proposed fix

**Chosen option:** **B** — `mkdir(parents=True, exist_ok=True)` on each variant dir before writing.

**Rationale:** The grader's contract is to emit a `grading.json` for both variants of every eval-`<name>/` that has an `eval_metadata.json`. A partially-populated iteration folder (e.g., one variant ran, the other crashed mid-run) should still get a complete grading.json pair so downstream tools (`aggregate_iteration.py` lines 52-53 unconditionally append both `old_skill` and `with_skill` runs per eval) see a uniform shape. `check_assertion` already returns `passed=False` with explanatory evidence when the `outputs/` dir is missing, so the resulting grading.json correctly reports 0/N for the absent variant rather than silently dropping it. Option A would create asymmetric output that `aggregate_iteration.py` is not defensive against.

**Files to change:**

- `.dev/eval-workspaces/sc-brainstorm/grader.py` lines `236-238`: insert `mkdir` calls before each `write_text`.

**Exact diff sketch:**

```diff
     # Write grading.json files
-    (eval_dir / "with_skill" / "grading.json").write_text(json.dumps(with_grading, indent=2))
-    (eval_dir / "old_skill" / "grading.json").write_text(json.dumps(old_grading, indent=2))
+    with_skill_path = eval_dir / "with_skill" / "grading.json"
+    old_skill_path = eval_dir / "old_skill" / "grading.json"
+    with_skill_path.parent.mkdir(parents=True, exist_ok=True)
+    old_skill_path.parent.mkdir(parents=True, exist_ok=True)
+    with_skill_path.write_text(json.dumps(with_grading, indent=2))
+    old_skill_path.write_text(json.dumps(old_grading, indent=2))
```

## Risk / blast radius

Minimal. `mkdir(parents=True, exist_ok=True)` is idempotent and a no-op when the dir exists (the normal case in fully-populated iterations). Behavior in the happy path is byte-identical; the only changed behavior is that a previously fatal `FileNotFoundError` becomes a successfully written grading.json reporting 0/N pass-rate for the missing variant, which downstream aggregation already handles.

## Confidence

**95%** — Bug is mechanical and reproducible from the file text; fix matches the file's own defensive style at `check_assertion` line 183 and `aggregate_iteration.py`'s assumption that both variants always have a record.
