# PR #100 — Review Findings (4 parallel /sc:troubleshoot passes)

**PR**: https://github.com/IronbellyOrg/IronClaude/pull/100
**Branch**: `chore/brainstorm-live-evals`
**Title**: feat(sc-brainstorm): targeted remediation restoring iteration-2 baseline strengths
**Run date**: 2026-05-27
**Methodology**: 4 parallel subagents, each invoked `/sc:troubleshoot` against one reviewer comment, validated against `origin/chore/brainstorm-live-evals` (not the locally checked-out branch).

## Summary table

| # | Comment ID | File:Line | Severity | Verdict | Confidence | Files changed by fix |
|---|---|---|---|---|---|---|
| 1 | r3312667799 | `.dev/eval-workspaces/sc-brainstorm/SPEC.md:55` | low | CONFIRMED | 95% | 1 doc file (2 lines) |
| 2 | r3312667803 | `.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py:53` | medium | CONFIRMED | 95% | 1 py + 1 json |
| 3 | r3312667807 | `.dev/eval-workspaces/sc-brainstorm/grader.py:55` (actual 45-57) | medium | CONFIRMED (latent) | 95% | 1 py file (parse + check_assertion) |
| 4 | r3312667808 | `.dev/eval-workspaces/sc-brainstorm/grader.py:237` | medium | CONFIRMED | 95% | 1 py file (3 lines) |

All four comments are valid. Three are real correctness bugs (#2, #3, #4); one is a doc inconsistency (#1). Total surface: 4 files under `.dev/eval-workspaces/sc-brainstorm/`. No shipped package code touched.

---

## Finding 1 — SPEC.md `--generate` mode inconsistency (r3312667799)

**Severity**: low | **Verdict**: CONFIRMED | **Confidence**: 95%

### Reviewer claim
> The pipeline diagram shows `/sc:adversarial --generate requirements`, but later sections (and `refs/handoff-routing.md`) describe using `--generate spec`. This inconsistency could cause readers to invoke an unsupported generate mode or implement the wrong integration.

### Validation
- `SPEC.md:55` (pipeline diagram) and `SPEC.md:264` (flag default example) show `--generate requirements`.
- `SPEC.md:472` (§10) is authoritative: "v2 ships using `--generate spec` and reframes its contract as **'spec-style requirements'**. No blocker on adding `--generate requirements` to `/sc:adversarial`."
- `src/superclaude/commands/brainstorm.md:133` matches §10 — delegates with `--generate spec`.
- `src/superclaude/commands/adversarial.md:44` documents supported types as `roadmap, spec, design, etc.` — `requirements` is not yet supported.
- §16 Followups tracks `--generate requirements` as a **future** enhancement.
- Note: reviewer's reference to `refs/handoff-routing.md` is inaccurate — that file does not exist on the branch. The substantive inconsistency between diagram/flag-example and §10 is real.

### Root cause
Stale diagram and flag example not back-propagated after §10's decision pivoted v2 from aspirational `--generate requirements` to shipped `--generate spec`.

### Fix
Surgical text edits to **`.dev/eval-workspaces/sc-brainstorm/SPEC.md`**:

```diff
@@ SPEC.md line 55 (pipeline diagram in §1)
-   ├── /sc:adversarial --source seed-brief.md --generate requirements --agents <built-spec>
+   ├── /sc:adversarial --source seed-brief.md --generate spec --agents <built-spec>
    ↓
-   ├── merged-requirements.md  + 6 adversarial artifacts
+   ├── merged-requirements.md  + 6 adversarial artifacts   # spec-shaped per §10
@@ SPEC.md line 264 (§3 flags example)
-   --generate requirements           # New generate type, see §10
+   --generate spec                   # Reframed as "spec-style requirements" per §10
```

**Preserve** the filename `merged-requirements.md` — §10 is explicit that v2's spec-shaped output is reframed as "spec-style requirements" and the filename is part of v2's external contract.

### Acceptance check
`git grep -n "generate requirements" .dev/eval-workspaces/sc-brainstorm/SPEC.md` should report hits only inside §10, §15, §16 (decision/futures context).

### Risk
Very low. Two text edits to a doc-only file. No code, no skill, no command file affected.

---

## Finding 2 — `_validate_evals_sync` silently vacuous (r3312667803)

**Severity**: medium | **Verdict**: CONFIRMED | **Confidence**: 95%

### Reviewer claim
> `_validate_evals_sync()` assumes `evals.json` provides `remediation_acceptance_scope`/`remediation_deferred_cases`, but the current `evals/evals.json` in this PR doesn't define them, so the sync check will never emit warnings. That makes the docstring claim about metadata-level scope enforcement misleading for future scope edits.

### Validation
- `compare_live_runs.py:45-66` defines `_validate_evals_sync`. Lines 53-54 use `evals_data.get("remediation_acceptance_scope", [])` / `…deferred_cases", [])`. Lines 55, 63 gate warnings on `if declared and ...` — empty set is falsy → silent skip.
- `evals/evals.json` top-level keys on the PR branch: `skill_name, iteration, scope, notes, evals, deferred_after_iter_2, assertions_v2`. Neither key is present. (`deferred_after_iter_2` exists but contains prose, not integer case IDs.)
- The docstring at `compare_live_runs.py:48-51` claims metadata-level enforcement — but with missing keys silently passing, any future scope edit to `evals.json` that omits these keys (the status quo) bypasses the gate.

### Root cause
Combination: (a) the metadata keys the validator looks for were never added to `evals.json`, AND (b) the validator uses `.get(..., [])` + truthy-check semantics that treat "missing" as "OK." Either alone is a bug; together they make the docstring contract unenforceable.

### Fix
**Two files**:

1. **`.dev/eval-workspaces/sc-brainstorm/evals/evals.json`** — add at top level (near `scope`/`notes`):

   ```json
   "remediation_acceptance_scope": [4, 5, 6, 7, 8, 9, 10, 11],
   "remediation_deferred_cases": [12],
   ```

   Values mirror `compare_live_runs.py:34` (`CASE_IDS = set(range(4, 12))`) and `:35` (`EXCLUDED_CASE_IDS = {12}`).

2. **`.dev/eval-workspaces/sc-brainstorm/compare_live_runs.py`** lines 45-66 — switch to `None` sentinel so missing keys emit a loud warning rather than silently passing:

   ```diff
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
            print(...)  # unchanged inside
   ```

   Update the docstring to reflect: "missing keys are treated as a sync FAILURE, not a silent pass."

### Acceptance check
- Temporarily remove `remediation_acceptance_scope` from `evals.json` and re-run `compare_live_runs.py` — expect a stderr WARNING line.
- Restore the key; expect no warning.

### Risk
Very low. Both files are evaluation tooling under `.dev/eval-workspaces/` — not shipped, not imported by the package, not on any CI gate. Warnings go to stderr.

---

## Finding 3 — `parse_yaml_simple` drops nested values (r3312667807)

**Severity**: medium | **Verdict**: CONFIRMED (latent — no current false negatives, but the trap is armed) | **Confidence**: 95%

### Reviewer claim
> `parse_yaml_simple()` ignores any indented lines, so any top-level YAML key whose value is a nested mapping/list (e.g., `enrichment_used`, `token_usage`) is parsed as an empty string and its nested content becomes uncheckable. This can lead to false negatives (or silently skipped validation) if assertions ever need to inspect nested return-contract fields.

### Validation
- `grader.py:45-57` (note: reviewer cited :55, function actually spans 45-57) — `parse_yaml_simple` explicitly does `if not line or line.startswith("#") or line.startswith(" "): continue`, silently skipping every indented line. A top-level key like `enrichment_used:` (no inline value) gets stored as `result["enrichment_used"] = ""`. Same for `token_usage:`, `wave_durations_ms:`, `enrichment_artifact_sizes:` in real contracts (e.g. `iterations/iteration-2/eval-code-add-rate-limiting/with_skill/outputs/return-contract.yaml:9-37`).
- `grader.py:135-167` (`check_assertion`) consumes the parsed dict only via `y.get(field, "")`, `float(y.get(field, "0"))`, and substring scans. With nested keys flattened to `""`, every `yaml_field` / `yaml_field_min` / `yaml_substring` assertion targeting a nested key would silently misbehave.
- Audit of every `"field":` in `iterations/**/eval_metadata.json` — all current assertion targets are top-level scalars (`contract_version`, `status`, `convergence_score`, `domain`, etc.). No assertion currently dotted-references nested keys, so today's grader output is correct. The trap is armed for the next assertion that wants nested data.
- The docstring at `grader.py:46` even advertises the limitation: `"Parse a simple flat YAML file (no nesting)."` — but the contract schema explicitly defines nested blocks.

### Root cause
A line-oriented parser written under the simplifying assumption that "the contract is flat top-level scalars." Now applied to a contract that *is* nested.

### Fix
**Option A**: Replace with `yaml.safe_load`. `pyyaml>=6.0` is already in `pyproject.toml` dependencies, so no new dep. Also add a small dotted-path resolver to support future nested assertions cleanly.

**`.dev/eval-workspaces/sc-brainstorm/grader.py`**:

```diff
 import json
 import re
 import sys
 from pathlib import Path
+import yaml

@@ replace parse_yaml_simple body (lines 45-57)
-def parse_yaml_simple(text: str) -> dict:
-    """Parse a simple flat YAML file (no nesting). Returns dict of string values."""
-    if not text:
-        return {}
-    result = {}
-    for line in text.split("\n"):
-        line = line.rstrip()
-        if not line or line.startswith("#") or line.startswith(" "):
-            continue
-        if ":" in line:
-            k, _, v = line.partition(":")
-            v = v.strip().strip("'\"")
-            result[k.strip()] = v
-    return result
+def parse_yaml_simple(text: str) -> dict:
+    """Parse YAML. Returns dict (possibly nested). Empty/invalid input → {}."""
+    if not text:
+        return {}
+    try:
+        loaded = yaml.safe_load(text)
+    except yaml.YAMLError:
+        return {}
+    return loaded if isinstance(loaded, dict) else {}
+
+
+def _resolve_field(d: dict, path: str):
+    """Resolve dotted path 'a.b.0.c' through nested dicts/lists. Returns '' if missing."""
+    cur = d
+    for part in path.split("."):
+        if isinstance(cur, list):
+            try:
+                cur = cur[int(part)]
+            except (ValueError, IndexError):
+                return ""
+        elif isinstance(cur, dict):
+            cur = cur.get(part, "")
+        else:
+            return ""
+    return cur
```

Then in the three `yaml_*` branches of `check_assertion` (lines ~135-167), replace `y.get(field, "")` with `_resolve_field(y, field)` and coerce to `str(...)` before `.lower()` / substring checks (and guard `yaml_field_min` for non-numeric values).

### Acceptance check
- Run grader against current iteration-1 + iteration-2 fixtures; expect byte-identical grading.json for every existing eval (all assertion targets are top-level scalars).
- Add a temporary assertion targeting `enrichment_used.web_search_used` (or similar nested key) against a real `return-contract.yaml`; expect it to be resolved correctly instead of always failing on empty string.

### Risk
Two callers index the returned dict assuming a string (`grader.py:153` `actual.lower() == expected.lower()` and `:174` `s.lower() in actual.lower()`). With `yaml.safe_load`, top-level scalars (`contract_version: "1.0"`, `status: success`, `domain: code`) still come back as strings → existing iteration-1/iteration-2 assertions remain correct. Numeric scalars (`convergence_score: 0.78`) become `float` instead of `str`, but the only consumer is `yaml_field_min` which already does `float(...)`. The dotted-path resolver + `str(...)` coercion in the three branches protects against future block-key assertions.

---

## Finding 4 — grader.py aborts on missing variant subdir (r3312667808)

**Severity**: medium | **Verdict**: CONFIRMED | **Confidence**: 95%

### Reviewer claim
> Writing `with_skill/grading.json` and `old_skill/grading.json` assumes those directories already exist; if an eval dir has `eval_metadata.json` but is missing one of those subdirs, the grader will raise and abort the whole run. That makes the grader fragile to partially-populated iteration folders.

### Validation
- `grader.py:237-238` writes unconditionally:
  ```python
  (eval_dir / "with_skill" / "grading.json").write_text(json.dumps(with_grading, indent=2))
  (eval_dir / "old_skill" / "grading.json").write_text(json.dumps(old_grading, indent=2))
  ```
  No `parent.mkdir(...)`, no `is_dir()` guard, no `try/except`. If `eval_dir/with_skill/` does not exist, `Path.write_text` raises `FileNotFoundError`.
- `check_assertion` (line 183) is already defensive about missing variant subdirs; `build_grading` (lines 210-231) produces a valid dict even when every assertion fails. So the pipeline produces a writable grading dict, but the write step blows up.
- `main()` (lines 257-266) iterates all `eval-*/` dirs in order with no per-eval try/except — the first missing variant subdir terminates the whole loop.

### Root cause
Unconditional `Path.write_text` on a path whose parent directory's existence is never verified or created. `check_assertion` is defensive; the write step is not.

### Fix
**Option B**: `mkdir(parents=True, exist_ok=True)` on each variant dir before writing.

**Rationale**: The grader's contract is to emit a `grading.json` for both variants of every `eval-<name>/` with an `eval_metadata.json`. A partially-populated iteration (one variant ran, the other crashed mid-run) should still get a complete grading.json pair so downstream tooling sees a uniform shape. `aggregate_iteration.py:52-53` unconditionally appends both `old_skill` and `with_skill` runs per eval; Option A (skip variant) would produce asymmetric output it isn't defensive against. `check_assertion` already returns `passed=False` with explanatory evidence when `outputs/` is missing, so the resulting grading.json correctly reports 0/N for the absent variant.

**`.dev/eval-workspaces/sc-brainstorm/grader.py`** lines 236-238:

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

### Acceptance check
- Construct a temporary eval dir with only `eval_metadata.json` (no `with_skill/` or `old_skill/` children) → run grader → expect successful completion with two `grading.json` files reporting 0/N for the empty variants.
- Run against fully-populated iteration-2 → expect byte-identical grading.json output as before (mkdir is idempotent on existing dirs).

### Risk
Minimal. `mkdir(parents=True, exist_ok=True)` is idempotent and a no-op when the dir exists (normal case). The only behavioral change is that a previously fatal `FileNotFoundError` becomes a successfully written grading.json reporting 0/N — which downstream aggregation already handles.

---

## Cross-finding observations

- **All four fixes target `.dev/eval-workspaces/sc-brainstorm/`** — not shipped package code. No `src/superclaude/` changes; no `.claude/` regeneration concerns. SoT discipline (`mem:feedback_hooks_source_of_truth`) does not gate this work.
- **No interactions between fixes**: each touches independent file/line ranges. Finding 3 and Finding 4 both edit `grader.py` but in disjoint regions (lines 45-57 + 135-167 vs lines 236-238). They can land in any order or in one bundled commit.
- **No new dependencies** required: `pyyaml>=6.0` already declared in `pyproject.toml`.
- **No test changes required** by the reviewer findings themselves, but a small smoke test for `parse_yaml_simple` on a real `return-contract.yaml` (Finding 3) and for `grade_eval` on a missing-variant dir (Finding 4) would lock in the behavior and is recommended.

## Next steps

1. `/task-builder` builds an MDTM task file from this document.
2. `/sc:reflect` UC-1 validates the tasklist covers all four findings.
3. `/task` executes — surface is 3 files on `chore/brainstorm-live-evals`.
