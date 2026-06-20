# Research 04 — Eval-workspace conventions (Test & Verification)

**Status:** Complete
**Date:** 2026-06-02
**Scope:** `.dev/eval-workspaces/sc-reflect/`
**Goal:** Document EXACTLY how an eval case is structured so the builder can scaffold the 6 NEW eval cases from spec §4.1 + §8.1.

---

## 0. KEY ARCHITECTURAL FINDING (read first)

The workspace has a **two-layer model**. A "case" is NOT self-graded by files inside `cases/<name>/`. Instead:

1. **Author-time layer — `cases/<name>/`**: committed source fixtures + expectation files. These are the **inputs** and the human-readable gold-standard. They are NOT what `grader.py` reads.
2. **Registry layer — `evals/evals.json`**: the single canonical index. Every case is an entry in the `"evals": [...]` array. THIS is where each case declares its `assertions` (the grader DSL). **New cases MUST be registered here** or they are invisible to the harness.
3. **Run-time layer — `iterations/iteration-N/eval-<name>/`**: per-run artifacts generated when the skill executes. `grader.py` reads `eval_metadata.json` (a per-run materialization of the evals.json entry's assertions) and scores assertions against `with_skill/outputs/` and `old_skill/outputs/`. These are NOT committed source (spec §4.1 note, line 282).

So scaffolding a new case = (a) create `cases/<name>/` fixture dir, **and** (b) add an entry to `evals/evals.json` with `name`, `case_dir`/`case_file`, `mode`, `use_case`, `spec_ref`, `description`, and the `assertions` array. The `cases/` dir alone does nothing.

Verified at: `.dev/eval-workspaces/sc-reflect/grader.py:411-419` (grade_eval reads `eval_dir/eval_metadata.json`), `:472-473` (iterates `iteration-dir/eval-*` dirs), and `evals/evals.json:6-496` (registry array with per-entry `assertions`).

> CAVEAT (Unverified): No `eval_metadata.json` exists anywhere in the tree today (`iterations/` holds only `.gitkeep`). The conversion of an `evals.json` entry -> per-run `eval_metadata.json` is done by an eval RUNNER that is not present in this workspace (referenced as `make reflect-eval` in falsifier README and SPEC.md:996, but no Makefile target found in the workspace dir). The builder should treat `evals.json` + `cases/<name>/` as the authored deliverables; the runner is upstream infra.

---

## 1. Existing case structure (canonical per-case layout)

There are **TWO distinct case shapes** in use, both valid:

### Shape A — directory case (pilot evals, UC-1/UC-2)
Used by: `pre-trivial-coverage-gap/`, `post-small-diff-clean/`, `post-large-diff-mixed/`.
Layout (verified via `find`):
```
cases/<name>/
  input/            # fixture inputs the skill runs against
    spec.md         # (UC-1 / pre mode)   — e.g. pre-trivial-coverage-gap/input/spec.md
    tasklist.md     # (UC-1 and UC-2)
    diff.patch      # (UC-2 / post mode)  — e.g. post-small-diff-clean/input/diff.patch
  expected.yaml     # gold-standard expected outcomes (human-readable; NOT graded directly)
```
- `expected.yaml` example (`cases/post-large-diff-mixed/expected.yaml:1-31`): flat YAML with `mode`, `use_case`, `deviation_counts:{authorized,necessary,drift,regression}`, `tier_reached`, `escalation_reason`, `calibrated_confidence_min`, `regression_recall_min`, `per_task_verdicts:[{task_id,verdict,hunk_id}]`, `remediation_recommendation`.
- Most `input/*` and `expected.yaml` files are STUBS in v1.0 (header line `# STUB — iteration-1 follow-up fleshes out content.`). The structure is canonical even where content is stub.

### Shape B — flat YAML scenario case (promotion + falsifier suites)
Used by: `cases/promotion/*.yaml` (15 files), `cases/falsifier-suite/*.yaml` (2 files).
Layout: a single `<scenario>.yaml` per case (no `input/` dir, no `expected.yaml`). Each YAML is a self-describing scenario spec.
- Promotion example (`cases/promotion/promotion-blocked-by-drift.yaml:1-23`): `id`, `status`, `description`, `spec_ref`, `expected_action`, `expected_gate_evaluation:{11 atomic gate fields}`, `expected_gate_evaluation_failures:[...]`, `expected_gate_passed`, `adapter`.
- Falsifier example (`cases/falsifier-suite/T2-converges-on-wrong.yaml:1-22`): `id`, `status: skeleton-pending-iteration-3-fixture`, `description`, `expected_grader_emission:{skeleton_present:true}`, `iteration_3_fixture_path`, `canonical_assertion_for_iteration_3`, `related_spec_references`, `TODO_ITERATION_3`.
- Falsifier suite also has `cases/falsifier-suite/README.md` (lifecycle doc) and `cases/falsifier-suite/fixtures/spec-with-deliberate-misclassification.md` (placeholder fixture).

### Which shape do the 6 NEW serena cases use?
Spec §4.1 (lines 274-280) and §8.1 (lines 464-470) refer to all 6 as **directories**: `.dev/eval-workspaces/sc-reflect/cases/serena-*/`. So **Shape A (directory case)** is the intended convention for the new cases. Each needs an `input/` fixture + an `expected.yaml`, plus an `evals/evals.json` entry carrying the grader assertions.

---

## 2. grader.py — discovery, scoring, assertion DSL

File: `.dev/eval-workspaces/sc-reflect/grader.py` (492 lines).

**Discovery** (`main`, `:461-488`): `python grader.py <iteration-dir>`; iterates `sorted(iter_dir.iterdir())`, processes each subdir whose name starts with `eval-` (`:472-473`).

**Scoring** (`grade_eval`, `:411-458`): reads `<eval_dir>/eval_metadata.json`; pulls `meta["assertions"]`; splits by `target` prefix into `with_skill/...` vs `old_skill/...` (`:422-423`); evaluates each via `check_assertion`; writes `with_skill/grading.json` + `old_skill/grading.json` (`:451-452`). Output schema: `{expectations:[{text,passed,evidence}], summary:{passed,failed,total,pass_rate}}` (`:11-12`, `:438-446`).

**Assertion declaration shape**: each assertion is a dict with a `type` field plus type-specific keys and a mandatory `text` field (used as the expectation label, `:431`). The dispatcher is `check_assertion` (`:294-408`).

**18 supported assertion types** (8 baseline + 10 semantic; full list also mirrored in `evals/evals.json:498-517` `grading_criteria`):

Baseline (target-based, `target` is a path under the eval dir):
- `file_exists` (`:300`) — `{type,target,text}`.
- `frontmatter_field` (`:306`) — `{target,field,expected}`; case-insensitive compare.
- `section_present` (`:318`) — `{target,section_pattern}`.
- `section_enumerated` (`:326`) — `{target,section_pattern,min_items}`.
- **`yaml_field`** (`:336`) — `{target,field,expected}`; flat-YAML parse, exact string compare. CONFIRMED present — this is the type NFR-2 requires ("Grader yaml_field assertion over audit.log + return contract").
- `yaml_field_min` (`:348`) — `{target,field,min_value}`; numeric `>=`.
- `yaml_substring` (`:363`) — `{target,field,substring_any:[...]}`.
- `dir_count` (`:376`) — `{target,min_files}`.

Semantic (per `refs/grader-extensions.md`):
- `citation_resolves` (`:120,387`) — `{report,fixture_root?,expected_snippets?}`; re-reads each `file:line` in report, checks ±5-line window.
- `regex_present` (`:152,389`) — `{target,pattern}`; MULTILINE|DOTALL.
- `regex_absent` (`:162,391`) — `{target,pattern}`.
- `yaml_list_contains` (`:172,393`) — `{target,field_path,value}`; `field_path` dotted, supports int indices; asserts list membership.
- `matrix_covers_items` (`:190,395`) — `{matrix,source,threshold?=0.8}`; coverage ratio vs source `items[].id`.
- `checkpoint_logged` (`:212,397`) — `{audit_log,checkpoint_name}`; scans JSONL audit.log for `row["checkpoint"]==name`.
- `deviation_class_matches` (`:232,399`) — `{annotated_fixture,report,diff_hunk_id}`; compares fixture hunk class vs report `deviation_register`.
- `path_exists` (`:251,401`) — `{target}`.
- `path_does_not_exist` (`:261,403`) — `{target}`.
- `falsifier_skeleton_present` (`:270,405`) — `{case_yaml}`; PASS if `status==skeleton-pending-iteration-3-fixture`, or `status==active` with canonical fields `{id,type,fixture,expected,assertion}` (set at `:117`).

Unknown type -> FAIL (`:408`).

**NFR-2 confirmation**: `yaml_field` over `audit.log` + return contract IS supported. The audit.log is JSON-lines (see `checkpoint_logged` `:218-225` doing `json.loads` per line), but `yaml_field` itself uses the flat-line parser (`parse_yaml_simple`, `:58-77`) — so to assert on `audit.log` fields the case should point `yaml_field` at a flat YAML contract artifact (e.g. `contract.yaml`), and use `checkpoint_logged` for the JSONL audit.log. For boolean telemetry like `verification_ran:false`, `serena_*_invoked:true`, use `yaml_field` against the run's `contract.yaml` (pattern already used by evals 2/3: `yaml_field target=with_skill/outputs/contract.yaml field=tier_reached`).

---

## 3. SPEC.md — case schema / adding cases

File: `.dev/eval-workspaces/sc-reflect/SPEC.md` (1706 lines).

- **§12.2 line 945**: "Modeled on `.dev/eval-workspaces/sc-brainstorm/`. Same layout: `SPEC.md`, `evals/evals.json`, `iterations/iteration-N/`, `grader.py`, `aggregate_iteration.py`, `skill-snapshot/reflect-v1.md`." -> confirms the canonical workspace layout and that cases are registered in `evals/evals.json`.
- **§12.3 iteration harness (lines 973-981)**: defines the 3 pilot evals with columns `ID | Mode | Scope | Notes`; expansion to 9-12 evals for iteration-2. This is the registry-row mental model for new cases (each case = one harness row -> one evals.json entry).
- **§12.4 (lines 983-996)**: grader DSL extension types; all semantic types live in `grader.py` per `refs/grader-extensions.md`.
- **§12.5 (lines 998-1063)**: falsifier-suite skeleton convention — the dual-state lifecycle (`skeleton-pending-iteration-3-fixture` -> `active`) and the canonical falsifier case shape `{id,type,status,fixture,expected,assertion}` with assertion `convergence_score < 0.75 OR verdict == regression_present`.
- No section prescribes a rigid JSON schema for a generic new case beyond "add a row + register in evals.json + declare assertions". The de-facto schema is the `evals.json` entry shape (see §1 above / §6 below).

---

## 4. aggregate_iteration.py + iterations/ + evals/ — does a new case need extra registration?

- **`aggregate_iteration.py`** (`:45-81` `build_benchmark`): globs `iteration-2/eval-*`, reads each `eval_metadata.json` for `eval_id`, reads `<config>/run-1/grading.json` + `timing.json`, summarizes mean/stddev across runs. It is **purely run-time aggregation** — it discovers cases by scanning `iteration-N/eval-*` dirs, NOT by reading evals.json. **No per-case registration in aggregate_iteration.py is needed.** (Note: it is hardcoded to `iterations/iteration-2` at `:152` — Unverified whether a new iteration dir needs a code edit; out of scope for case scaffolding.)
- **`iterations/`**: contains only `.gitkeep`. No committed run artifacts. New cases do NOT add anything here at author time.
- **`evals/evals.json`**: THE registration point. `iteration:1` (`:3`), `scope` string (`:4`), 20 eval entries, `grading_criteria` list (`:498-517`). A new case is registered by appending an entry to `"evals":[...]` with a new unique `id` (current max id = 20). **This is the only file a new case must be registered in at author time.**

> Summary: New cases need registration in exactly ONE file — `evals/evals.json`. Not in grader.py, not in aggregate_iteration.py.

---

## 5. Per-new-case scaffold (the 6 cases from §4.1 + §8.1)

Each new case = **2 author-time deliverables**: (a) a `cases/<name>/` directory (Shape A: `input/` + `expected.yaml`), and (b) an `evals/evals.json` entry (new `id` 21+, `case_dir`, `mode`, `use_case`, `spec_ref`, `description`, `assertions`). Minimal-but-canonical file set + the assertions each must declare per the spec acceptance criteria (§8.1 lines 464-470):

### 5.1 `serena-execute-verify` (FR-4) — id 21, mode post, use_case UC-2
- Files: `cases/serena-execute-verify/input/{tasklist.md, diff.patch}` + `cases/serena-execute-verify/expected.yaml` (mirror `post-large-diff-mixed/expected.yaml` shape).
- Must assert (§8.1 line 464): verification triangle ran; allowlist block; no-mutation deny; timeout->124; `pytest` exit-1 -> `regression_present` -> promotion-gate block; `--no-verify` + read-only skip with WARN.
- Suggested assertions: `yaml_field target=with_skill/outputs/contract.yaml field=verification_ran expected=true`; `yaml_field field=verify_exit_code expected=1`; `yaml_field field=regression_present expected=true`; `yaml_list_contains` on promotion-log `gate_evaluation_failures` value `no_drift_no_regression` (promotion blocked); `regex_present` on REPORT.md for the no-mutation/allowlist denial line; a `--no-verify` skip variant asserting `verification_ran=false` + WARN.

### 5.2 `serena-verify-injection` (FR-4.2b / NFR-8, M-TST1 — gating safety) — id 22
- Files: `cases/serena-verify-injection/input/` (a tasklist/contract carrying the 6 malicious verify commands) + `expected.yaml`.
- Must assert (§8.1 line 465): each injection class -> `metachar-denied` AND **zero invocations**. The 6 classes: `pytest ; rm`, `pytest && curl`, `pytest | sh`, `pytest $(x)`, `` pytest `x` ``, `pytest > /etc/y`.
- Suggested assertions (one PASS condition per metachar class — 6+ assertions): for each class, `regex_present target=with_skill/outputs/contract.yaml pattern=metachar-denied` (or `yaml_list_contains field_path=verify_denials value=<class>`), PLUS a zero-invocation proof: `yaml_field field=verify_invocations_count expected=0` and/or `regex_absent target=with_skill/outputs/audit.log pattern=verify_command_executed`. This is the AUTO-FAIL safety case — every class must deny with zero subprocess spawns.

### 5.3 `serena-verify-exitcodes` (FR-4.3, C2 — exit-code taxonomy) — id 23
- Files: `cases/serena-verify-exitcodes/input/` (fixtures driving each exit code) + `expected.yaml`.
- Must assert (§8.1 line 466): `pytest` 1->Regression, 2/3->Grounding Gap, 5->Drift; `ruff` 1->`S_dev_density`; 124->Grounding Gap; FR-4.3b flaky-retry->`verify_flaky_suspected`.
- Suggested assertions: one `yaml_field`/`yaml_list_contains` per exit-code->class mapping against `contract.yaml` (e.g. `field=exit_1_class expected=regression`, `exit_2_class expected=grounding_gap`, `exit_5_class expected=drift`, `ruff_exit_1_signal expected=S_dev_density`, `exit_124_class expected=grounding_gap`), plus `yaml_field field=verify_flaky_suspected expected=true` for the retry path.

### 5.4 `serena-verify-drift-guard` (FR-4.8, M-COR2) — id 24
- Files: `cases/serena-verify-drift-guard/input/` (input tree + a verify run that emits `.pytest_cache`/`.pyc`) + `expected.yaml`.
- Must assert (§8.1 line 467): cache artifacts do NOT trip `input_tree_sha256` drift -> no spurious STOP.
- Suggested assertions: `yaml_field target=with_skill/outputs/contract.yaml field=input_drift_detected expected=false`; `yaml_field field=status expected=success` (run completed, no STOP); optionally `regex_absent` on REPORT.md for any `input_tree_sha256.*drift` STOP line.

### 5.5 `serena-onboarding` (FR-2) — id 25
- Files: `cases/serena-onboarding/input/` + `expected.yaml`.
- Must assert (§8.1 line 468): cold-start bootstrap; silent-fail guard (memory delta <=0 -> `succeeded:false`); context-excluded WARN (not STOP); warm-start skip; no-auto-trigger without `--onboard`.
- Suggested assertions: `yaml_field field=onboarding_invoked expected=true` (with `--onboard`); silent-fail variant `yaml_field field=onboarding_succeeded expected=false` when memory delta <=0; `regex_present` for context-excluded WARN + `yaml_field field=status expected=success` (WARN not STOP); warm-start variant `yaml_field field=onboarding_skipped expected=true`; no-auto-trigger variant `yaml_field field=onboarding_invoked expected=false` (no `--onboard`). NFR-7 budget can use `yaml_field_min`/`yaml_field` on a recorded token field.

### 5.6 `serena-handoff` (FR-3) — id 26
- Files: `cases/serena-handoff/input/` + `expected.yaml`.
- Must assert (§8.1 line 469): handoff blob written before task-builder; `write_memory` fallback when context-excluded; both-fail -> `handoff_persist_failed` + report still ships; no-remediate no-op.
- Suggested assertions: `path_exists target=with_skill/outputs/handoff-blob.<ext>` (blob written) + `checkpoint_logged checkpoint_name=handoff_persisted_before_task_builder` (ordering); fallback variant `yaml_field field=handoff_persist_method expected=write_memory`; both-fail variant `yaml_field field=handoff_persist_failed expected=true` + `file_exists target=with_skill/outputs/REPORT.md` (report ships anyway); no-remediate variant `yaml_field field=handoff_invoked expected=false`.

### 5.7 `serena-type-hierarchy` (FR-1) — id 27
- Files: `cases/serena-type-hierarchy/input/` + `expected.yaml`.
- Must assert (§8.1 line 470): backend probe; OO subtype coverage; LSP-disabled skip (no degrade); explicit backend error -> fallback; 1B.3 lineage confirmation.
- Suggested assertions: `yaml_field field=hierarchy_backend_probed expected=true`; `matrix_covers_items` or `yaml_field_min` on OO subtype coverage; LSP-disabled variant `yaml_field field=hierarchy_skipped expected=true` + `status expected=success` (no degrade); backend-error variant `yaml_field field=hierarchy_fallback_used expected=true`; `regex_present` for the 1B.3 lineage confirmation line.

> NOTE for builder: the exact telemetry field NAMES above (`verification_ran`, `regression_present`, `verify_flaky_suspected`, `onboarding_succeeded`, `handoff_persist_failed`, etc.) should be cross-checked against the spec §5/§9 contract field definitions (researcher 06 covers cross-spec / contract). Where a field name is the spec's exact contract field, prefer `yaml_field`; where it is free-text in REPORT.md, use `regex_present`. The case is in `cases/<name>/expected.yaml` (gold) and the gradable assertions in `evals/evals.json`.

---

## 6. Registry / index — new cases MUST be registered

**Yes — there is exactly one registry/index file: `evals/evals.json`.**

Canonical new-entry skeleton (append to `"evals":[...]`, after id 20; assertions per §5 above):
```json
{
  "id": 21,
  "name": "serena-execute-verify",
  "case_dir": "cases/serena-execute-verify/",
  "mode": "post",
  "use_case": "UC-2 (FR-4 verification triangle)",
  "spec_ref": "§8.1 line 464 / §4.1 line 274 (FR-4)",
  "description": "...",
  "inputs": { "tasklist": "input/tasklist.md", "diff": "input/diff.patch" },
  "expected": "expected.yaml",
  "assertions": [ { "type": "yaml_field", "target": "with_skill/outputs/contract.yaml", "field": "verification_ran", "expected": "true", "text": "..." } ]
}
```
- Field convention from existing entries (`evals.json:7-39`): `id` (int, unique), `name`, `case_dir` (Shape A) OR `case_file` (Shape B), `mode`, `use_case`, `spec_ref`, `description`, `inputs` (Shape A only), `expected` (Shape A only), `assertions[]`.
- `grading_criteria` (`evals.json:498-517`) lists all 18 valid types — new assertions must use a type already in that list (all the types §5 proposes ARE listed; no new grader code needed).
- Update the top-level `scope` string (`evals.json:4`) and consider bumping `iteration` if these land in a new iteration (Unverified policy — researcher 06 / spec §12.3).

---

## 7. Builder-actionable granular-item checklist

Per new case, the builder can emit these granular MDTM items (x6 cases = ~18-24 items):
1. Create `cases/serena-<name>/input/` with the fixture(s) the FR exercises (stub OK if mirroring the v1.0 STUB convention; header `# STUB — ...`).
2. Create `cases/serena-<name>/expected.yaml` mirroring the closest existing expected.yaml (post-* for verify cases, a new shape for onboarding/handoff/hierarchy capturing the FR's success contract).
3. Append the `evals/evals.json` entry (new `id`, `assertions` per §5) and update the `scope` string.

Optional shared item: confirm telemetry field names against the spec contract (depends on researcher 06 output) before finalizing `yaml_field` field names.

---

## 8. Falsifiable claims / caveats (tagged)

- CONFIRMED: `yaml_field` exists and supports NFR-2 (`grader.py:336-346`). Flat-YAML parser only (`:58-77`) — nested YAML needs `yaml_list_contains` (full `yaml.safe_load`, `:176`).
- CONFIRMED: only `evals/evals.json` requires case registration at author time (`grader.py` + `aggregate_iteration.py` discover by directory scan, not by reading evals.json).
- CONFIRMED: spec treats all 6 serena cases as **directories** (§4.1 274-280, §8.1 464-470) -> Shape A.
- Unverified: the `evals.json`-entry -> per-run `eval_metadata.json` runner; no `eval_metadata.json`, no Makefile, and `iterations/` is empty (`.gitkeep` only). The `make reflect-eval` target named in SPEC.md:996 / falsifier README is not present in this workspace dir.
- Unverified: exact telemetry contract field names (defer to researcher 06 / spec §5/§9).
- Unverified: `aggregate_iteration.py` hardcodes `iteration-2` (`:152`); whether new cases imply an iteration-3 dir + code edit is out of scope for case scaffolding.

---

## Summary

**Canonical case layout (Shape A, for all 6 new serena cases):** `cases/<name>/input/<fixtures>` + `cases/<name>/expected.yaml`, PLUS a registry entry in `evals/evals.json` (new `id`, `case_dir`, `mode`, `use_case`, `spec_ref`, `description`, `inputs`, `expected`, `assertions[]`). `grader.py` scores via per-run `eval_metadata.json` against `with_skill/outputs/` & `old_skill/outputs/` using 18 assertion types; `yaml_field` covers NFR-2. Registration is required in exactly ONE file: `evals/evals.json` (current max id 20 -> new ids 21-27).

**6 (spec says 6; enumeration lists 7) new cases to scaffold:** serena-execute-verify (FR-4, id21), serena-verify-injection (FR-4.2b/NFR-8 safety, id22), serena-verify-exitcodes (FR-4.3, id23), serena-verify-drift-guard (FR-4.8, id24), serena-onboarding (FR-2, id25), serena-handoff (FR-3, id26), serena-type-hierarchy (FR-1, id27). NOTE: the user brief + §8.1 both enumerate **7** cases despite the "6 NEW" framing — the builder should scaffold all 7 listed (the "6" likely predates the type-hierarchy addition; flag to researcher 06 for reconciliation).

**Status:** Complete
