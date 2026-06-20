---
phase_gate: PG-4
gate_name: Eval Hardening and Validation Logic QA
verdict: PASS
date: 2026-05-26
task_id: TASK-RF-20260526-183300
adversarial_stance: "Assumed work contains errors. Verified every claim against source files via Read, Grep, git diff, and UV-wrapped Python smoke tests rather than trusting the Phase 4 summary at face value."
files_reviewed:
  - .dev/tasks/to-do/TASK-RF-20260526-183300/phase-outputs/reports/phase-4-eval-hardening-summary.md
  - .dev/eval-workspaces/sc-brainstorm/evals/evals.json
  - .dev/eval-workspaces/sc-brainstorm/grader.py
  - .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py
  - .dev/tasks/to-do/TASK-RF-20260526-183300/research/03-eval-and-validation-targets.md (lines 16-75)
  - .dev/tasks/to-do/TASK-RF-20260526-183300/TASK-RF-20260526-183300.md
  - .dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-tasklist.md
fix_cycles_applied: 0
---

# PG-4 — Eval Hardening QA Report

## Verdict

**PASS.** All 14 acceptance criteria (A–N) verified against source files with concrete evidence. Zero issues found requiring fixes. Phase 5 entry: **AUTHORIZED**.

The adversarial stance was applied throughout: the Phase 4 summary's claims were treated as suspect and each verified independently via Read of the cited files, Grep over the actual content, git diff against HEAD, and live UV-wrapped Python smoke tests of the new grader helpers and the compare_live_runs constants/validator.

## Acceptance Criteria

### A. Eval assertion coverage (`evals.json`)

**Verification:** Read `.dev/eval-workspaces/sc-brainstorm/evals/evals.json` end-to-end (249 lines). Ran `uv run python -c "import json; d=json.load(open(...)); ..."` to enumerate top-level keys, per-case keys, and assertion sub-list cardinalities.

**Evidence:**
- Top-level `remediation_acceptance_scope == [4,5,6,7,8,9,10,11]` (`evals.json:6`); `remediation_deferred_cases == [12]` (`evals.json:7`); `remediation_case_12_deferral_note` explicitly names `Unknown skill: sc:brainstorm-protocol` registry blocker (`evals.json:8`).
- Per-case keys on cases 4-11 verified by parsing JSON: each has `expected_depth`, `expected_blind_mode`, `expected_interactive_mode`, `acceptance_scope == "remediation"`. Concrete values: c4=quick/F/F, c5=deep/F/F, c6=standard/F/F, c7=standard/F/F, c8=standard/F/F, c9=standard/F/F, c10=deep/F/**T** (interactive), c11=deep/**T**/F (blind).
- Case 12: `acceptance_scope: "deferred"` (`evals.json:176`), `deferral_reason` field contains "Unknown skill: sc:brainstorm-protocol" string (`evals.json:177`), verified by Python substring match.
- New top-level `assertions_cases_4_11_acceptance` block (`evals.json:201-247`) with required sub-lists: `seed_brief_assertions` (8 items ≥ 8 ✓), `merged_requirements_assertions` (9 ≥ 9 ✓), `return_contract_assertions` (10 ≥ 10 ✓), `blind_mode_assertions` (2 ≥ 2 ✓), `telemetry_and_quality_assertions` (2 ≥ 2 ✓). Block has all four metadata fields: `description`, `case_12_note`, `telemetry_scope_note`, `strict_quality_scope_note`.
- Legacy `assertions_v2` unchanged: 14 items, identical to pre-edit content per HEAD diff (criterion M cross-check).
- JSON validates: `json.load()` succeeds with no exceptions.

**Verdict:** PASS.

### B. Robust YAML parser + new helpers (`grader.py`)

**Verification:** Read `grader.py` (574 lines). Counted `if a_type ==` branches via Grep. Live UV-wrapped smoke test on `parse_yaml_robust` with a nested doc containing `agent_spec.personas` and `agent_spec.models` lists, plus `count_section_items_or_table_rows` against table-only, bullets-only, and mixed sections. Diffed against pre-edit HEAD copy to confirm existing branches unchanged.

**Evidence:**
- `parse_yaml_robust()` at `grader.py:64-183`. No PyYAML dependency. Stack-of-frames algorithm with pending list-vs-dict materialization.
- `_walk_yaml_strings()` at `grader.py:186-197`. Recursive walk over str/list/dict.
- `count_section_items_or_table_rows()` at `grader.py:235-293`. Counts bullets + table data rows, excludes header + separator.
- New assertion-type branches (6 total, criterion says "5 ... actually 6 — confirm count" — confirmed 6):
  - `section_items_or_table_rows` (`grader.py:389`)
  - `frontmatter_field_in` (`grader.py:402`)
  - `yaml_field_in` (`grader.py:419`)
  - `yaml_contains_any_recursive` (`grader.py:433`)
  - `text_contains_any` (`grader.py:454`)
  - `text_not_contains_any` (`grader.py:470`)
- Existing 8 branches (file_exists, frontmatter_field, section_present, section_enumerated, yaml_field, yaml_field_min, yaml_substring, dir_count) at lines 303, 309, 321, 329, 339, 351, 366, 379 — verified UNCHANGED by `diff /tmp/grader_pre.py grader.py` (only additions; no `<` lines removing existing logic in those ranges).
- `Unknown assertion type: {a_type}` hard-fail at `grader.py:486` — final line of `check_assertion`, reached when no branch matches. All new branches added BEFORE this line.
- `grade_eval()` (`grader.py:489`), `build_grading()` (`grader.py:504`), `main()` (`grader.py:541`) UNCHANGED per diff. Output schema `{expectations: [...], summary: {...}}` at `grader.py:517-525` preserved.
- Live smoke test output:
  - `parse_yaml_robust` on nested doc: returned `{'contract_version': '1.0', 'agent_spec': {'personas': ['architect', 'security', 'refactorer'], 'models': ['claude-opus-4-7', 'claude-sonnet-4-6']}, 'status': 'success'}` ✓
  - `_walk_yaml_strings` collected 12 leaves including `'architect'` and `'claude-opus-4-7'` ✓
  - `count_section_items_or_table_rows`: table-only Risks → 3 (3 data rows, header+separator excluded) ✓; bullets-only Risks → 2 ✓; mixed (1 bullet + table 3 rows) → 4 ✓
  - Flat-parser backwards-compat: `parse_yaml_simple('domain: code\nstatus: success\nproposal_count: 3\n')` → `{'domain': 'code', 'status': 'success', 'proposal_count': '3'}` ✓
  - `py_compile.compile(..., doraise=True)` → SYNTAX_OK ✓

**Verdict:** PASS.

### C. Comparison quality + telemetry handling (`compare_live_runs.py`)

**Verification:** Read `compare_live_runs.py` (406 lines). Smoke-tested constants and `_validate_evals_sync()` via UV-wrapped Python loaded from the script's own directory (so `from grader import ...` resolves).

**Evidence:**
- Module docstring (`compare_live_runs.py:1-20`) states cases 4-11 as default acceptance scope and case 12 INTENTIONALLY EXCLUDED with `Unknown skill: sc:brainstorm-protocol` registry blocker named.
- Constants verified at module import: `CASE_IDS == {4,5,6,7,8,9,10,11}` (`compare_live_runs.py:35`); `EXCLUDED_CASE_IDS == {12}` (`compare_live_runs.py:36`); `EXCLUDED_CASE_REASON` names "Unknown skill: sc:brainstorm-protocol" (`compare_live_runs.py:37-42`).
- `_validate_evals_sync()` defined at `compare_live_runs.py:45-68`; called from `load_evals()` at `compare_live_runs.py:84` before filtering.
- Smoke-tested `_validate_evals_sync`:
  - In-sync input `[4-11] + [12]` → no stderr output ✓
  - Out-of-sync input `[4,5,6] + [12]` → stderr contains "WARNING: evals.json remediation_acceptance_scope=[4, 5, 6] differs from compare_live_runs.py CASE_IDS=[4, 5, 6, 7, 8, 9, 10, 11]" ✓
- `summarize()` (`compare_live_runs.py:266-304`) returns: `compared_case_ids`, `excluded_case_ids`, `excluded_case_reason`, `quality_unavailable_count`, `telemetry_unavailable_count`, and `availability_gaps` dict with `quality` and `timing_tokens` keys.
- Markdown writer (`compare_live_runs.py:307-380`):
  - `## Scope` section at `compare_live_runs.py:321-326` lists Compared cases / Excluded cases / Exclusion rationale.
  - `### Availability gaps` subsection at `compare_live_runs.py:339-345` with normative text "unavailable quality and unavailable telemetry MUST NOT be treated as remediation acceptance" present byte-exact at `compare_live_runs.py:344-345`.
- Output paths preserved at `compare_live_runs.py:396-397`: `LIVE_ROOT / "comparison-against-iteration-2.json"` and `.md`.
- Per-case comparison table loop at `compare_live_runs.py:353-378` reads `case["live"]["contract"]`, `case["live"]["quality"]`, `case["live"]["timing"]` etc. — actual artifact content, no fabrication.

**Verdict:** PASS.

### D. Case 12 exclusion documented in all three files

**Verification:** Grep for "case 12" / "12" / "deferred" / "Unknown skill" across all three files plus the Phase 4 summary.

**Evidence:**
- `evals.json`: top-level `remediation_deferred_cases: [12]` + `remediation_case_12_deferral_note` (lines 7-8); per-case `acceptance_scope: "deferred"` + `deferral_reason` (lines 176-177); `assertions_cases_4_11_acceptance.case_12_note` re-asserts exclusion (line 203). ✓
- `compare_live_runs.py`: module docstring (lines 6-10) + `EXCLUDED_CASE_IDS = {12}` (line 36) + `EXCLUDED_CASE_REASON` (lines 37-42). ✓
- `phase-4-eval-hardening-summary.md`: Table 1 row "Intentional case 12 exclusion" (line 39) cites `remediation_deferred_cases: [12]`, the deferral_note, and per-case keys. ✓

**Verdict:** PASS.

### E. UV command readiness

**Verification:** Grep for `python -m`, `pip install`, bare `python script.py` invocations across the three edited files and the Phase 4 summary.

**Evidence:**
- Grep `-E "(^|[^a-zA-Z])(python -m|pip install)"` returned zero matches across all four files.
- Pre-existing docstring references in `grader.py:15` and `grader.py:543` (`python grader.py <iteration-dir>`) noted as **non-blocking observation** per criterion E (legacy Usage text in pre-existing docstrings — the Phase 5 invocation contract specified in the task file at lines 226-230 is UV-only via `uv run python`).
- All smoke tests during this review used `uv run python`.

**Verdict:** PASS (with non-blocking observation logged).

### F. No `.claude/` mirror edits in Phase 4

**Verification:** `git status --short` filtered by `.claude/skills/sc-brainstorm-protocol/` and `.claude/skills/sc-adversarial-protocol/`; cross-checked mtime against Phase 4 entry timestamp (Phase 4 began ~22:00 on 2026-05-26 per pg-3 review).

**Evidence:**
- `.claude/skills/sc-brainstorm-protocol/`: NOT in `git status` output. Zero modifications.
- `.claude/skills/sc-adversarial-protocol/`: 5 files modified (SKILL.md, refs/agent-specs.md, artifact-templates.md, debate-protocol.md, scoring-protocol.md). However, `stat -c "%y" .claude/skills/sc-adversarial-protocol/SKILL.md` returns `2026-05-25 19:26:42` — pre-Phase-4. Diff inspection confirms cosmetic markdown lint blank-line fixes only. These are pre-existing 2026-05-25 cosmetic drift from before Phase 4 began (Phase 4 first edit was 2026-05-26 22:03). OUT OF SCOPE for PG-4 per criterion F's "any pre-existing mirror drift from before Phase 4 is OUT OF SCOPE" clause.

**Verdict:** PASS.

### G. No source-of-truth skill file edits in Phase 4

**Verification:** Stat src/ skill files and confirm latest edit timestamps fall in Phase 2/3 window (before Phase 4 began).

**Evidence:**
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`: mtime `2026-05-26 21:14:34` (Phase 2/3).
- `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`: mtime `2026-05-26 21:22:56` (Phase 2/3).
- `src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md`: mtime `2026-05-26 21:16:59` (Phase 2/3).
- `src/superclaude/skills/sc-adversarial-protocol/refs/artifact-templates.md`: mtime `2026-05-26 21:51:27` (Phase 3).
- `src/superclaude/skills/sc-adversarial-protocol/refs/debate-protocol.md`: mtime `2026-05-26 21:48:43` (Phase 3).
- `find -newer pg-3-adversarial-merge-qa.md` (file mtime 22:00) returned zero src/ files — no Phase 4 src/ edits.
- All Phase 2/3 src/ edits are EXPECTED to remain (they pre-date Phase 4 and are out of Phase 4 scope per criterion G).

**Verdict:** PASS.

### H. No placeholder text in edited files

**Verification:** `grep -nE "TODO|FIXME|TBD|XXX"` on the three edited files plus the Phase 4 summary.

**Evidence:**
- `evals.json`: 0 matches.
- `grader.py`: 0 matches.
- `compare_live_runs.py`: 0 matches.
- `phase-4-eval-hardening-summary.md`: 1 match at line 76 — the literal string `grep -c "TODO\|FIXME\|TBD\|XXX"` describing the verification check itself. Self-referential mention of the placeholder regex pattern; NOT an actual placeholder. Non-blocking.

**Verdict:** PASS.

### I. Both tasklist copies byte-identical

**Verification:** `diff -q` between the two tasklist copies.

**Evidence:**
- `diff -q .dev/tasks/to-do/TASK-RF-20260526-183300/TASK-RF-20260526-183300.md .dev/eval-workspaces/sc-brainstorm/live-runs/sc-brainstorm-remediation-tasklist.md` returned no output → byte-identical. ✓

**Verdict:** PASS.

### J. Phase 4 checklist items 4.1, 4.2, 4.3, 4.4 are `[x]`; PG-4 is `[ ]`

**Verification:** Read task file lines 188-210; Grep `^- \[[ x]\]` in the Phase 4 section.

**Evidence:**
- Step 4.1 (`task file:190`): `- [x]` ✓
- Step 4.2 (`task file:194`): `- [x]` ✓
- Step 4.3 (`task file:198`): `- [x]` ✓
- Step 4.4 (`task file:202`): `- [x]` ✓
- PG-4 (`task file:206`): `- [ ]` ✓ (correctly unchecked — this is the gate I am authorizing; it will be marked complete after this report lands)

**Verdict:** PASS.

### K. Phase 4 summary tables substantive

**Verification:** Read Phase 4 summary end-to-end.

**Evidence:**
- Table 1 (`summary:21-40`): 18 substantive rows. Each row cites concrete `evals.json` key/line and Coverage ✅. Required rows enumerated in spec all present: depth (row 1), proposal_count (row 2), interactive_mode/blind_mode (rows 3-4), Phase 2 seed sections (row 5), merged frontmatter spec_type/adversarial_status/proposal_count (row 6), merged blind_mode (row 7), Provenance (row 8), Risks-table-or-list (row 9), merged Phase 2 sections (row 10), return-contract status/domain/proposal_count/personas/handoff (row 11), return-contract Phase 2 fields (row 12), blind labels (row 13), telemetry presence (row 14), strict quality coverage (row 15), default 4-11 (row 16), case 12 exclusion (row 17), legacy assertions_v2 preserved (row 18).
- Table 2 (`summary:42-54`): 9 rows covering robust YAML parsing, yaml_contains_any_recursive, section_items_or_table_rows, frontmatter_field_in, yaml_field_in, text_contains_any, text_not_contains_any, backwards compat for existing 9 assertion types, unknown-type loud-fail. Each row cites `grader.py` function names.
- Table 3 (`summary:56-69`): 10 rows covering default 4-11, case 12 exclusion, sync validation, strict-quality comparison, quality gap reporting, telemetry handling, telemetry gap reporting, output paths preserved, per-case table preserved, None-mean-pass-rate handling.
- No placeholder rows; all coverage marked ✅.

**Verdict:** PASS.

### L. No silent passes

**Verification:** Read `summarize()` (`compare_live_runs.py:266-304`) and confirm counter semantics.

**Evidence:**
- Line 273: `quality_available = sum(1 for case in cases if case["live"]["quality"]["status"] == "available")` — counts ONLY `status == "available"`, not all cases. ✓
- Line 275: `timing_available = sum(1 for case in cases if case["live"]["timing"]["status"] == "available")` — same discipline. ✓
- Line 274: `quality_unavailable = sum(... if status == "unavailable")` — explicit count of unavailable, not derived from total minus available (avoids fence-post errors). ✓
- Line 276: `timing_unavailable` includes both `"unavailable"` AND `"missing"` (when the live dir doesn't exist) — surfaces both forms of absence. ✓
- `availability_gaps.quality` (`compare_live_runs.py:292-296`) renders "explicit gap: strict quality grading not yet covering compared cases" when `quality_unavailable > 0`, "covered" only when zero. ✓
- `availability_gaps.timing_tokens` (`compare_live_runs.py:297-302`) same discipline. ✓
- Markdown writer renders both `available: N of M` AND `unavailable (explicit gap): K of M` lines (`compare_live_runs.py:334-337`) so absence is not hidden behind the "available" count.

**Verdict:** PASS.

### M. Backwards compatibility for non-requirement-bearing artifacts

**Verification:** `diff /tmp/grader_pre.py .dev/eval-workspaces/sc-brainstorm/grader.py` (pre-edit copied from `git show HEAD:.dev/eval-workspaces/sc-brainstorm/grader.py`).

**Evidence:**
- Diff shows only ADDITIONS (lines prefixed `>`): the new `parse_yaml_robust`, `_walk_yaml_strings`, `count_section_items_or_table_rows`, and the 6 new assertion-type branches.
- Zero `<` lines (removals) in the file_exists/frontmatter_field/section_present/section_enumerated/yaml_field/yaml_field_min/yaml_substring/dir_count ranges. The 8 existing branches retain their original `(passed, evidence)` tuple-returning logic byte-for-byte.
- `parse_yaml_simple()` (used by yaml_field, yaml_field_min, yaml_substring) UNCHANGED — confirmed by smoke test producing identical output for `domain: code\nstatus: success\nproposal_count: 3\n` input.
- `grade_eval`, `build_grading`, `main` UNCHANGED — output schema `{expectations, summary}` preserved.

**Verdict:** PASS.

### N. No scope creep

**Verification:** `git status --short` filtered to non-eval-workspace paths.

**Evidence:**
- Modified files outside `.dev/eval-workspaces/sc-brainstorm/`:
  - `src/superclaude/skills/...` — Phase 2/3 carryover, mtime pre-Phase-4 (verified in criterion G).
  - `.claude/skills/sc-adversarial-protocol/...` — pre-2026-05-25 cosmetic drift, pre-Phase-4 (verified in criterion F).
- No edits to:
  - `src/superclaude/cli/`, `src/superclaude/commands/`, `src/superclaude/agents/` ✓
  - `src/superclaude/skills/` non-Phase-2/3 skills (no other skill directories touched) ✓
  - Other eval workspaces under `.dev/eval-workspaces/` ✓
  - `.claude/commands/`, `.claude/agents/`, `.claude/hooks/` ✓
- Phase 4 edits confined to: `evals/evals.json`, `grader.py`, `compare_live_runs.py` (eval workspace) + `phase-4-eval-hardening-summary.md` (phase-outputs report).

**Verdict:** PASS.

## Cross-Cutting Checks

| Check | Method | Result |
|-------|--------|--------|
| JSON validates | `uv run python -c "import json; json.load(...)"` | PASS |
| Python files compile | `uv run python -c "import py_compile; py_compile.compile(..., doraise=True)"` × 2 | PASS |
| Both tasklist copies identical | `diff -q` | PASS (no output) |
| No placeholder tokens in edited files | `grep -nE "TODO\|FIXME\|TBD\|XXX"` | 0 in edited files (1 self-referential mention in summary, non-blocking) |
| Phase 4 checkbox state | Read + Grep | 4.1-4.4 `[x]`; PG-4 `[ ]` (correct) |
| Tool engagement | Read: 4 | Grep: 6 | Bash (incl. UV smoke tests): 12 | Sufficient (≥14 criteria) |

## Confidence Gate

- **Verified:** 14/14 criteria (A–N) checked with concrete tool evidence (file:line citations + grep + git diff + live UV smoke tests).
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 14 / (14 − 0) × 100 = **100.0%**
- **Tool engagement:** Read: 4 | Grep: 6 | Bash (UV smoke tests + git/stat/diff): 12 — exceeds the criterion count.

Threshold (≥95% AND UNCHECKED == 0) met. Eligible for PASS verdict.

## Issues Found

None.

## Actions Taken

No fixes applied (no issues found on first pass).

## Non-Blocking Observations

1. **Pre-existing `.claude/skills/sc-adversarial-protocol/` cosmetic mirror drift.** `git status` shows 5 modified files in that mirror with mtimes 2026-05-25 (pre-Phase-4). Diff content is cosmetic markdownlint blank-line normalization, not normative content. Per criterion F, pre-existing drift is OUT OF SCOPE for PG-4. Recommend resolving by Phase 5 `make sync-dev` per Phase 5 Step 5.2 design (which already plans to regenerate `.claude/` from `src/`).
2. **`compare_live_runs.py` was untracked at HEAD.** Confirmed by `git log --oneline -- compare_live_runs.py` returning empty and `git status` showing `?? .dev/eval-workspaces/sc-brainstorm/compare_live_runs.py`. The Phase 4 summary (line 77) explicitly acknowledges this pre-existing state. Phase 4 expanded the file with the docstring, constants, sync-validation helper, and availability-gap fields. The summary's claim that Phase 4 did not "fabricate" the file is consistent with Phase 1 Step 1.0's worktree classification.
3. **Legacy `python grader.py` strings in `grader.py:15` (docstring) and `grader.py:543` (Usage message).** Pre-existing documentation text in non-executable strings — does NOT invoke bare Python. Phase 5 invocation contract (task file lines 226-230) is UV-only via `uv run python`. Non-blocking.
4. **Summary line 76 contains the literal token "TODO" within a quoted grep pattern (`grep -c "TODO\|FIXME\|TBD\|XXX"`).** This is the summary describing the verification check it performed — a self-referential mention, not an actual placeholder. Non-blocking.

## Fix Cycles Applied

0. PASS achieved on first review pass.

## Final Verdict

**PASS — Phase 5 entry: AUTHORIZED.**

All Phase 4 hardening requirements are independently verified:
- Eval assertion coverage is concrete, additive, and traceable to live-regression failure modes.
- The grader extension preserves all existing assertion semantics while adding 6 new branches and 3 new helpers (`parse_yaml_robust`, `_walk_yaml_strings`, `count_section_items_or_table_rows`), exercised by live UV-wrapped smoke tests.
- The comparison script encodes the cases-4-11 default + case-12 deferral as constants, adds a sync-validator against `evals.json`, and reports quality/telemetry absence as explicit availability gaps (never silent passes).
- Case 12 exclusion is consistently documented in all three layers (evals.json + script + summary).
- No `.claude/` mirror or `src/superclaude/` edits were performed during Phase 4 timeframe.
- Both tasklist copies remain byte-identical.

Phase 5 (sync + validation commands) is authorized to start.
