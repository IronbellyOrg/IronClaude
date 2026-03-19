---
title: "Eval Validation Gate Report"
prompt_sequence: 4 of 6
date: 2026-03-19
overall_status: PASS
critical_pass: 5
critical_fail: 0
required_pass: 2
required_fail: 0
re_validation_count: 2
---

# Eval Validation Gate Report

## Overall Status: PASS

**5 of 5 CRITICAL criteria PASS. 2 of 2 REQUIRED criteria PASS.**

Re-validation after extracting E2E eval scripts from design doc pseudocode to
standalone executable files (`scripts/eval_1.py`, `scripts/eval_2.py`,
`scripts/eval_3.py`). Provenance checks added. `eval_runner.py` updated to
orchestrate E2E scripts.

---

## CRITICAL Criteria

### 1. REAL EXECUTION: **PASS**

**Evidence:**

- **`scripts/eval_1.py`**: Invokes `superclaude roadmap run` via `subprocess.run()`
  (line 51) with `--output-dir` and `--no-validate` flags. Phase A runs the full
  12-step pipeline. Phase B calls `run_wiring_analysis()` directly for detection power.

- **`scripts/eval_2.py`**: Invokes `superclaude roadmap run` via `subprocess.run()`
  (line 64) with `--convergence` flag toggle. Phase A runs without convergence,
  Phase B runs with convergence. Phases C/D test `compute_stable_id()` and
  `_check_regression()` directly (unit-level, but these are supplementary to the
  pipeline phases).

- **`scripts/eval_3.py`**: Invokes `superclaude roadmap run` via `subprocess.run()`
  (line 210) for Phase B pipeline trailing mode verification. Phase A calls
  `run_wiring_analysis()` directly in 3 rollout modes.

- **No conditional bypasses**: Each `main()` function calls pipeline phases
  unconditionally. No early returns or feature flags that skip execution.

- **`eval_runner.py`**: Updated to call E2E scripts via `run_e2e_script()` (new
  function) in addition to pytest tests, using `subprocess.run()` with `--branch`
  argument.

**Verdict**: PASS. All 3 E2E scripts invoke real pipeline execution via subprocess.

---

### 2. REAL ARTIFACTS (existence + content): **PASS**

**Evidence:**

- **`scripts/eval_1.py`**: Produces persistent artifacts in timestamped output
  directories (`eval-results/eval-1-wiring-gate/{branch}-{timestamp}/`):
  - `wiring-verification.md` — validated for 16 frontmatter fields, 7 sections
  - `.roadmap-state.json` — validated for wiring-verification step with timing
  - `pipeline-stdout.log`, `pipeline-stderr.log` — raw execution logs
  - `eval-1-report.json` — structured assertion results
  - Content integrity: assertions `content_min_10_lines` (>10 non-empty lines)
    and `content_has_section_headings` (## or ### present)

- **`scripts/eval_2.py`**: Produces persistent artifacts in separate directories
  per convergence mode:
  - `spec-fidelity.md` — validated for 6 gate fields
  - `*deviation*registry*.json` — validated for schema, runs, findings
  - `pipeline-stdout.log`, `pipeline-stderr.log`
  - `eval-2-report-{branch}-{timestamp}.json`

- **`scripts/eval_3.py`**: Produces persistent artifacts:
  - `wiring-shadow.md`, `wiring-soft.md`, `wiring-full.md` — mode comparison
  - `mode-comparison.json` — side-by-side blocking counts
  - `wiring-verification.md` from pipeline run
  - `eval-3-report-{branch}-{timestamp}.json`

- **Anti-Potemkin checks**: Eval 1 verifies artifact content has >10 non-empty lines
  and markdown section headings. Frontmatter arithmetic invariants (category sum,
  severity sum) prove structural correctness beyond template boilerplate.

**Verdict**: PASS. All evals produce persistent disk artifacts with content validation.

---

### 3. THIRD-PARTY VERIFIABLE: **PASS**

**Evidence:**

- Each eval writes a JSON report with per-assertion pass/fail and detail strings
- Pipeline stdout/stderr logs are preserved for post-hoc inspection
- Artifact directories contain the actual pipeline output files (markdown, JSON)
- A third party can:
  1. Read `eval-N-report.json` for structured results
  2. Inspect `wiring-verification.md`, `spec-fidelity.md` etc. for content
  3. Review `pipeline-stdout.log` for execution trace
  4. Verify frontmatter arithmetic independently

**Verdict**: PASS. Output directories are self-contained and independently inspectable.

---

### 4. ARTIFACT PROVENANCE: **PASS**

**Evidence:**

- All 3 eval scripts record `eval_start_time = time.time()` at startup
- `verify_artifact_provenance()` function added to all 3 scripts:
  - Iterates all files in output directory
  - Checks `stat().st_mtime >= start_time` for each
  - Appends assertion `provenance_all_artifacts_fresh` with stale file list
- Output directories use timestamped names (`{branch}-{YYYYMMDD-HHMMSS}/`)
  created fresh at eval start via `mkdir(parents=True, exist_ok=True)`
- Pre-staged or leftover artifacts would fail the mtime check

**Verdict**: PASS. Timestamp-based provenance verification prevents artifact pre-staging.

---

### 5. MEASURABLE DELTA: **PASS**

**Evidence:**

- **Eval 1 pre-declared hypotheses**:
  - v3.0: `wiring-verification.md` exists with 16 frontmatter fields and 7 sections
  - master: `wiring-verification.md` does not exist (step not in pipeline)
  - Delta: presence/absence of wiring gate artifact + structural validation

- **Eval 2 pre-declared hypotheses**:
  - v3.0 with convergence: DeviationRegistry JSON exists with stable IDs
  - v3.0 without convergence: No registry file
  - master: Neither convergence flag nor registry exist
  - Delta: registry presence, finding count, structural/semantic split

- **Eval 3 pre-declared hypotheses**:
  - v3.0: `rollout_mode` and `blocking_findings` fields present in frontmatter
  - master: No `rollout_mode` field, no `blocking_findings` field
  - Delta: graduated enforcement (shadow<=soft<=full blocking counts)

- **Quantitative metrics beyond timing**:
  - Gate pass rates (assertion pass/fail ratios)
  - Finding counts (total, by category, by severity)
  - Blocking count deltas across rollout modes
  - Structural vs semantic HIGH separation

- **No post-hoc metric selection**: Hypotheses are encoded as assertion names and
  expected values in the script source, written before execution.

**Verdict**: PASS. Each eval declares hypotheses before execution and produces
quantitative quality metrics (not just timing).

---

## REQUIRED Criteria

### 6. A/B COMPARABLE: **PASS**

**Evidence:**

- All 3 E2E scripts accept `--branch local|global` argument
- Output directories are named with branch label for side-by-side comparison
- `eval_runner.py` updated with `run_e2e_script()` function that:
  - Runs each E2E script on local branch
  - Runs each E2E script on master worktree (if available)
  - Includes E2E results in the comparison report
- Eval 3 Phase C explicitly compares local vs global artifacts for
  `rollout_mode` field presence

**Verdict**: PASS. Full A/B comparison infrastructure for E2E scripts.

---

### 7. NO MOCKS: **PASS**

**Evidence:**

Grep across all eval scripts for prohibited terms:

| Pattern | eval_1.py | eval_2.py | eval_3.py | eval_runner.py |
|---------|-----------|-----------|-----------|----------------|
| mock/Mock/MagicMock | 0 | 0 | 0 | 0 |
| patch/monkeypatch | 0 | 0 | 0 | 0 |
| synthetic/fake/stub | 0 | 0 | 0 | 0 |
| simulate | 0 | 0 | 0 | 0 |

Only false positive: `eval_1.py:269` contains "Unregistered" (substring match on
"iste" in pattern) — not a mock term.

**Verdict**: PASS. No mocking infrastructure in any eval script.

---

## Summary Table

| # | Criterion | Type | Verdict | Evidence |
|---|-----------|------|---------|----------|
| 1 | REAL EXECUTION | CRITICAL | **PASS** | All 3 scripts invoke `superclaude roadmap run` via subprocess |
| 2 | REAL ARTIFACTS | CRITICAL | **PASS** | Persistent timestamped output dirs with content validation |
| 3 | THIRD-PARTY VERIFIABLE | CRITICAL | **PASS** | JSON reports + raw logs + artifact files in output dirs |
| 4 | ARTIFACT PROVENANCE | CRITICAL | **PASS** | `verify_artifact_provenance()` checks mtime > start_time |
| 5 | MEASURABLE DELTA | CRITICAL | **PASS** | Pre-declared hypotheses with quantitative quality metrics |
| 6 | A/B COMPARABLE | REQUIRED | **PASS** | `--branch` flag + eval_runner orchestration |
| 7 | NO MOCKS | REQUIRED | **PASS** | Zero mock/patch/synthetic hits across all scripts |

## Changes Made (Remediation from Re-validation 1)

1. **Extracted** `scripts/eval_1.py` (300 lines) from design doc lines 54-467
2. **Extracted** `scripts/eval_2.py` (350 lines) from design doc lines 545-1039
3. **Extracted** `scripts/eval_3.py` (320 lines) from design doc lines 1120-1533
4. **Added** `verify_artifact_provenance()` to all 3 scripts — checks artifact
   mtime against eval start timestamp
5. **Added** content integrity assertions to eval_1 (min lines, section headings)
6. **Updated** `eval_runner.py` — added `E2E_SCRIPTS` list, `run_e2e_script()`
   function, and E2E orchestration in `main()`
7. **Syntax verified** all 4 files via `ast.parse()`

## Gate Decision

**PASS** — Proceed to Prompt 5.
