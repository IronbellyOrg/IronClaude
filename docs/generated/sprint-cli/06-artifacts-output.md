---
title: Sprint CLI - Artifacts & Output Systems
generated: 2026-04-03
scope: cli/sprint/logging_.py, cli/sprint/diagnostics.py, cli/sprint/kpi.py, cli/pipeline/trailing_gate.py
---

# Artifacts & Output Systems

## Output Directory Structure

All sprint artifacts are rooted under `<release_dir>/`:

```
<release_dir>/
  execution-log.jsonl          # Structured event log
  execution-log.md             # Human-readable execution log
  .sprint-exitcode             # Sentinel exit code (0 or 1)
  results/
    phase-{N}-output.txt       # Raw Claude subprocess stdout
    phase-{N}-errors.txt       # Raw Claude subprocess stderr
    phase-{N}-result.md        # Authoritative phase result (YAML frontmatter)
    phase-{N}-diagnostic.md    # Failure diagnostics (on error only)
    gate-kpi-report.md         # Gate evaluation KPI summary
    remediation.json           # Deferred remediation findings
    crash_recovery_log.md      # Checkpoint recovery events
    preflight-artifacts/
      <task_id>/
        evidence.md            # Python-mode task evidence bundle
```

## Sprint Artifact Details

### 1. Execution Log (JSONL)

**Generator**: `SprintLogger._jsonl()` + event methods
**File**: `src/superclaude/cli/sprint/logging_.py:27-40, 58-68, 88-106, 153-164`
**Location**: `<release_dir>/execution-log.jsonl`
**Format**: JSON Lines with event types:

```json
{"event": "sprint_start", "config": {...}, "timestamp": "..."}
{"event": "phase_start", "phase": 1, "timestamp": "..."}
{"event": "phase_complete", "phase": 1, "status": "PASS", "duration": 45.2, ...}
{"event": "sprint_complete", "outcome": "SUCCESS", "total_duration": 180.5, ...}
```

### 2. Execution Log (Markdown)

**Generator**: `SprintLogger.write_header()`, `write_phase_result()`, `write_summary()`
**File**: `src/superclaude/cli/sprint/logging_.py:43-57, 108-120, 166-171`
**Location**: `<release_dir>/execution-log.md`
**Format**:

```markdown
# Sprint Execution Log
- Index: <path>
- Started: <timestamp>
- Model: <model>

| Phase | Status | Started | Completed | Duration | Exit |
|-------|--------|---------|-----------|----------|------|
| P01   | PASS   | 10:00   | 10:45     | 45s      | 0    |

## Outcome: SUCCESS
```

### 3. Phase Output/Error Capture

**Generator**: Sprint executor process loop
**File**: `src/superclaude/cli/sprint/executor.py:1242+`
**Location**: `results/phase-{N}-output.txt`, `results/phase-{N}-errors.txt`
**Format**: Raw text from Claude subprocess stdout/stderr streams

### 4. Authoritative Phase Result

**Generator**: `_write_executor_result_file()`
**File**: `src/superclaude/cli/sprint/executor.py:1718-1760`
**Location**: `results/phase-{N}-result.md`
**Format**:

```markdown
---
phase: 1
status: PASS
tasks_total: 5
tasks_passed: 5
tasks_failed: 0
---

| Task | Status | Duration |
|------|--------|----------|
| T01.01 | PASS | 12s |

EXIT_RECOMMENDATION: CONTINUE
```

### 5. Preliminary Sentinel Result

**Generator**: `_write_preliminary_result()`
**File**: `src/superclaude/cli/sprint/executor.py:1652-1715`
**Location**: Same path as authoritative result (overwritten later)
**Purpose**: Freshness guard sentinel with `EXIT_RECOMMENDATION: CONTINUE`

### 6. Diagnostics Report

**Generator**: `ReportGenerator.write()`
**File**: `src/superclaude/cli/sprint/diagnostics.py:235-291`
**Caller**: `executor.py:1457-1468`
**Location**: `results/phase-{N}-diagnostic.md`
**Format**: Markdown bundle with:
- Failure category classification
- Evidence from monitor state
- Output/error tail excerpts
- Diagnostic collector findings

### 7. Gate KPI Report

**Generator**: `build_kpi_report().format_report()`
**File**: `src/superclaude/cli/sprint/kpi.py:24-145`
**Caller**: `executor.py:1510-1518`
**Location**: `results/gate-kpi-report.md`
**Sections**:
- Gate Evaluation metrics
- Remediation summary
- Conflict Review results
- Wiring Gate status

### 8. Deferred Remediation Log

**Generator**: `DeferredRemediationLog.serialize()`
**File**: `src/superclaude/cli/pipeline/trailing_gate.py:494-569`
**Construction**: `executor.py:1153-1157`
**Location**: `results/remediation.json`
**Format**: Pretty JSON with accumulated trailing gate findings and remediation entries

### 9. Crash Recovery Log

**Generator**: `_write_crash_recovery_log()`
**File**: `src/superclaude/cli/sprint/executor.py:1625-1648`
**Location**: `results/crash_recovery_log.md`
**Format**: Appended markdown sections per recovered phase with checkpoint/contamination details

### 10. Sprint Exit Code

**Generator**: End of `execute_sprint()`
**File**: `src/superclaude/cli/sprint/executor.py:1544-1548`
**Location**: `<release_dir>/.sprint-exitcode`
**Format**: Single integer (`0` = success, `1` = failure)
**Consumer**: Tmux relay path reads this for exit status

### 11. Preflight Evidence Bundle

**Generator**: `_write_evidence()`
**File**: `src/superclaude/cli/sprint/preflight.py:45-73`
**Location**: `results/preflight-artifacts/<task_id>/evidence.md`
**Format**:

```markdown
## Evidence: <task_id>
- Command: <command>
- Exit Code: <code>
- Duration: <seconds>s

### Output (truncated)
<stdout>

### Errors (truncated)
<stderr>
```

## Roadmap Pipeline Artifacts

Output root determined by `--output` flag (default: parent of input file).

| Artifact | Step | Format |
|----------|------|--------|
| `extraction.md` | extract | Markdown |
| `roadmap-{agent-id}.md` | generate-A/B | Markdown per agent |
| `diff-analysis.md` | diff | Markdown |
| `debate-transcript.md` | debate | Markdown |
| `base-selection.md` | score | Markdown |
| `roadmap.md` | merge | Markdown (final merged) |
| `anti-instinct-audit.md` | anti-instinct | Markdown |
| `test-strategy.md` | test-strategy | Markdown |
| `spec-fidelity.md` | spec-fidelity | Markdown |
| `wiring-verification.md` | wiring | Markdown |
| `spec-deviations.md` + `.json` | deviation-analysis | Markdown + JSON sidecar |
| `remediation-tasklist.md` + `.json` | remediate | Markdown + JSON sidecar |
| `certification-report.md` | certify | Markdown |
| `.roadmap-state.json` | all steps | JSON state ledger |
| `validate/validation-report.md` | validate | Markdown |

### Roadmap State File (`.roadmap-state.json`)

**Purpose**: Resume support, step metadata, hash tracking
**Writers**: Atomic state write throughout `roadmap/executor.py`
**Contents**: Step outcomes, file hashes, retry counts, TDD/PRD routing, certification status

## Tasklist Pipeline Artifacts

| Artifact | Generator | Format |
|----------|-----------|--------|
| `tasklist-fidelity.md` | `tasklist/executor.py:208` | Markdown fidelity report |

## Template Files

### Examples (`src/superclaude/examples/`)
- `prd_template.md` — PRD structure template
- `tdd_template.md` — TDD structure template
- `release-spec-template.md` — Release spec template

### Skill Templates (`src/superclaude/skills/`)
- `sc-tasklist-protocol/templates/index-template.md` — Tasklist index
- `sc-tasklist-protocol/templates/phase-template.md` — Phase file
- `sc-cleanup-audit-protocol/templates/final-report.md` — Audit report
- `sc-roadmap-protocol/refs/templates.md` — Roadmap templates
- `sc-adversarial-protocol/refs/artifact-templates.md` — Debate artifacts

## Output Routing Policy

From `CLAUDE.md` and source analysis:
- `docs/generated/` is documented as a roadmap pipeline artifact directory, not a general sink
- Sprint writes to `release_dir` (from `--release-dir` or auto-resolved from index path)
- Roadmap writes to `--output` dir (default: parent of input file)
- No hardcoded path to `docs/generated/` exists in source — artifacts land there only when operators explicitly specify it as output
