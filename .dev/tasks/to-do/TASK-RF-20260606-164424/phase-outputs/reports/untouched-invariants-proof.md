# Untouched-Invariants Proof — PRD Document-Capture Hotfix

**Generated:** 2026-06-07 03:52 (Step 6.4)
**Branch:** `fix/prd-document-capture-hotfix` vs `master` (`54d4b4f5`)
**Method:** `git diff master -- src/superclaude/cli/prd/{executor.py,gates.py,prompts.py}`, filtered for removed (`-`) and added (`+`) lines, cross-checked against research files 02 (§1,§4,§5) and 03 (§1).

The hotfix changes are confined to: (executor.py) the NEW module-level `_STEP_ARTIFACT_PATTERNS` + `_pick_best_candidate`, the GENERIC dict-keyed branch of `_resolve_step_content` (former lines 339–365), and a comment-only INV-010 guard block in `_run_subprocess_step`; (gates.py) one NEW standalone `_check_no_truncation_marker` function; (prompts.py) one NEW `_artifact_path_for_step` helper + 4 builder output-path pins. Nothing else was touched.

---

## Invariant 1 — `_STEP_ARTIFACT_FILES` (executor.py:252–263, all 8 entries) — UNCHANGED ✅

**Evidence:** No removed (`-`) line in the executor diff contains `_STEP_ARTIFACT_FILES` or any of its 8 key/value entries (`parse-request`, `scope-discovery-raw`, `research-notes.md`, `sufficiency-review.md`, `qa/qa-research-gate`, `qa/qa-synthesis-gate`, `qa/qa-report-validation`, `qa/qa-qualitative`). The first hunk header is `@@ -263,6 +263,40 @@ _STEP_ARTIFACT_FILES: dict[str, str] = {` — the dict (252–263) is the unchanged context the additions follow; the new `_STEP_ARTIFACT_PATTERNS` map is inserted AFTER its closing brace.

**Verdict: PASS** — dict definition and all 8 entries byte-identical to master.

## Invariant 2 — build-task-file (293–304) + assembly (306–337) special cases — UNCHANGED ✅

**Evidence:** No removed (`-`) line contains `build-task-file`, `TASK-PRD-*.md`, `step_id == "assembly"`, `search_dirs`, or the assembly `"prd" not in match.name` filter. The executor change to `_resolve_step_content` is scoped to the GENERIC dict-keyed branch only (hunk `@@ -340,28 +374,56 @@`, i.e. former lines 339–365). The two special-case blocks precede that branch and are untouched (they shifted down by the inserted helper/map but their content is identical).

**Verdict: PASS** — both special cases intact, including their independent "largest wins" loops at former 298–299 / 329–330.

## Invariant 3 — `_evaluate_gate` line-count + semantic-check logic (executor.py ~678–715) — UNCHANGED ✅

**Evidence:** The only diff line mentioning `_evaluate_gate` is an ADDED (`+`) comment line inside the INV-010 guard block:
```
+        #     -> _evaluate_gate (min_lines + semantic_checks) and
```
This is documentation text naming the function, NOT a modification of it. No line of the `_evaluate_gate` body (the `gate.min_lines` check, the `gate.semantic_checks` loop, `check.check_fn(content)`, `result is not True`) appears as `+`/`-` code.

**Verdict: PASS** — `_evaluate_gate` body unchanged; only a comment references it.

## Invariant 4 — `_persist_step_artifact` canonical-name write (executor.py ~1145–1173) — UNCHANGED ✅

**Evidence:** The only diff line mentioning `_persist_step_artifact` is an ADDED (`+`) comment line in the INV-010 guard block:
```
+        #     _persist_step_artifact (canonical-name write for resume).
```
No line of the function body (`artifact_name = _STEP_ARTIFACT_FILES.get(step_id)`, `artifact_path = self._config.task_dir / artifact_name`, `artifact_path.write_text(...)`) appears as `+`/`-` code. AC8 (`test_persist_step_artifact_writes_canonical_name`) independently proves the canonical write still lands at `task_dir / "research-notes.md"`.

**Verdict: PASS** — `_persist_step_artifact` body unchanged; only a comment references it.

## Invariant 5 — research-notes STRICT gate (gates.py:330–346) UNCHANGED + truncation check NOT wired ✅

**Evidence (5a, block unchanged):** No `+`/`-` line in the gates.py diff contains `research-notes`, `min_lines=100`, `enforcement_tier="STRICT"`, `_check_research_notes_sections`, `_check_suggested_phases_detail`, or `semantic_checks`. The research-notes STRICT block is entirely outside the diff.

**Evidence (5b, define-only, not wired):** The COMPLETE gates.py diff is exactly the 4-line standalone function (plus blank lines):
```
+def _check_no_truncation_marker(content: str) -> bool | str:
+    if "[TRUNCATED" in content or content.rstrip().endswith("..."):
+        return "Content appears truncated — model output limit may have been reached"
+    return True
```
`grep -c "_check_no_truncation_marker" gates.py` = **1** (the definition only). It is NOT added to any gate's `semantic_checks=[...]` list or any `GATE_CRITERIA` entry, so it cannot mutate the research-notes STRICT block or risk INV-002.

**Verdict: PASS** — research-notes STRICT criteria unchanged; truncation check defined-only, not wired.

---

## Overall Verdict: PASS (5/5 invariants untouched)

All five must-stay-unchanged invariants are confirmed UNCHANGED by direct git-diff evidence. The only diff lines that *name* `_evaluate_gate` and `_persist_step_artifact` are additive INV-010 documentation comments, not behavioral changes. No invariant was modified; no fix-up required.

**Scope confirmation:** `git diff master --name-only` = exactly 3 prd source files + 5 prd test files. No `.claude/` path, no commands/, no skills/, no other package modules touched.
