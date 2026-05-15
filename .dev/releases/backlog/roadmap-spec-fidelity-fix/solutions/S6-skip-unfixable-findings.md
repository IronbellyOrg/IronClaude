# Solution S6 (Refactored) — Manual Triage with Allowlisted Skip

**Status**: REFACTORED after adversarial review. The original "silent
skip" proposal was rejected because it produced a falsely-clean PASS
that propagated through `wiring-verification`, `deviation-analysis`,
`remediate`, and `certify`. See `agent-reports/S6-debate.md`.

## Target root cause (unchanged)
All 10 active HIGHs in
`.dev/releases/current/task-builder-merge/roadmap/deviation-registry.json`
have `files_affected=[]`. The remediation system has no actionable
target, so the convergence loop is structurally guaranteed to fail.
Root cause is upstream in `structural_checkers` / `spec_structural_audit`
(parser noise like ``src/x.py:88` `` and `{skills,agents}` brace
expansion). S6 is the *triage pathway*, not the fix; pair it with S1
(regex hardening) and/or S2 (description normalization).

## Design principles

1. **Never invert PASS**: the convergence gate must remain truthful.
   If we cannot remediate a HIGH, we halt — we do not relabel it.
2. **Default deny**: skip-eligibility is opt-in per `(dimension,
   mismatch_class)`; a default install cannot skip anything.
3. **Audit trail first**: every triage event lands in the registry and
   a dedicated `manual-triage.md` companion file, so future runs and
   reviewers see exactly what was waived.
4. **Operator-facing runbook**: the halt produces copy-paste commands
   instead of a buried section in a 200-line report.

## Proposal

### 3.1 New convergence outcome: `MANUAL_TRIAGE`

Extend `ConvergenceResult` with a triage list and a dedicated halt
type. The result still reports `passed=False`, so the gate fails and
the pipeline stops at `spec-fidelity` — the right ergonomic location.

```python
@dataclass
class ConvergenceResult:
    passed: bool
    run_count: int
    final_high_count: int
    structural_progress_log: list[str] = field(default_factory=list)
    semantic_fluctuation_log: list[str] = field(default_factory=list)
    regression_detected: bool = False
    halt_reason: str | None = None
    # NEW (S6):
    manual_triage_findings: list[dict] = field(default_factory=list)
    triage_runbook_path: str | None = None
```

### 3.2 Allowlist-driven triage classifier

Add a *default-deny* allowlist in `convergence.py`:

```python
# (dimension, mismatch_class) pairs that may be marked MANUAL_TRIAGE
# when files_affected is empty after run >= 2. Default empty.
TRIAGE_ELIGIBLE_CLASSES: frozenset[tuple[str, str]] = frozenset()
```

Operators opt-in by providing `--triage-allow dimension:mismatch_class`
on the CLI, which extends the set for that invocation only. Without
the flag, behavior is identical to today (halt with `halt_reason`).

A `mismatch_class` is derived deterministically from the finding's
`location` prefix (`spec:file:`, `spec:nfr:`, `roadmap:`). If we
cannot classify, the finding is *never* triage-eligible.

### 3.3 Triage detection (replaces silent skip)

Between checkers and the final pass-check, after `run_idx >= 1` and
*only if at least one ACTIVE HIGH was remediated this run* (proof of
life — protects against the skip-everything attack):

```python
remediated_this_run = (prev_active_high_count - active_highs) > 0
if run_idx >= 1 and remediated_this_run and triage_allowlist:
    triage_candidates = [
        f for f in registry.findings.values()
        if f["status"] == "ACTIVE"
        and f["severity"] == "HIGH"
        and not f.get("files_affected")
        and (f["dimension"], _mismatch_class(f["location"]))
            in triage_allowlist
    ]
    for f in triage_candidates:
        f["status"] = "MANUAL_TRIAGE"          # new terminal status
        f["triage_reason"] = "no_files_affected_after_remediation"
        f["triage_run"] = run_idx + 1
    registry.save()
```

Key differences from the original proposal:
- New status `MANUAL_TRIAGE` (not `SKIPPED`) — distinguishes operator-
  acknowledged triage from remediation-driven SKIP.
- Gated by `remediated_this_run` — prevents a 100%-broken checker from
  laundering every finding through triage.
- Gated by allowlist — operator must consciously waive a class.
- Gate still fails. `manual_triage` findings count against
  `final_high_count` for reporting purposes but the convergence loop
  exits with `passed=False, halt_reason="manual_triage_required"`.

### 3.4 Update `models.py`

```python
VALID_FINDING_STATUSES = frozenset(
    {"PENDING", "ACTIVE", "FIXED", "FAILED", "SKIPPED", "MANUAL_TRIAGE"}
)
```

Downstream consumers in `remediate.py:130` and
`remediate_executor.py:554` must treat `MANUAL_TRIAGE` exactly like
`SKIPPED` (terminal, no remediation attempt). This is the **only**
spot where the new status is benign because we are not going to ship
in this state.

### 3.5 Halt report: `manual-triage.md` runbook

`_run_convergence_spec_fidelity` writes a sibling `manual-triage.md`
when `result.manual_triage_findings` is non-empty:

```markdown
---
type: manual_triage
spec_fidelity_state: HALTED
triage_count: 10
generated: 2026-05-15T...
---

# Manual Triage Required

The spec-fidelity convergence engine produced HIGH findings that
cannot be auto-remediated because the structural checker did not
attach `files_affected`. The pipeline has halted at `spec-fidelity`.

## Triage Findings

| Stable ID | Dimension | Location | Description |
| --------- | --------- | -------- | ----------- |
| dd52050c  | data_models | spec:file:docs/error-grouping-best-practices | ... |
| ...       | ...       | ...      | ...         |

## Remediation Runbook

1. **Investigate parser**: check
   `src/superclaude/cli/roadmap/spec_structural_audit.py` for the
   regex that produced these descriptions. Look for parser bugs
   (trailing backticks, brace expansion).
2. **If the finding is a real spec gap**: add the missing artifact
   to the spec (or remove the dangling reference) and re-run:
   ```
   superclaude roadmap run <spec> --resume
   ```
3. **If the finding is a checker false positive**: file an issue and
   waive it for this release:
   ```
   superclaude roadmap run <spec> --resume \
       --triage-allow data_models:spec_file \
       --triage-allow nfrs:spec_nfr
   ```
   The waiver is recorded in `deviation-registry.json` with run
   number and reason. It applies *only* to findings whose
   `(dimension, mismatch_class)` matches and whose `files_affected`
   is genuinely empty.
```

### 3.6 Frontmatter changes to `spec-fidelity.md`

`_write_convergence_report` updates:

```python
if result.manual_triage_findings:
    lines = [
        "---",
        f"high_severity_count: {len(result.manual_triage_findings)}",
        "medium_severity_count: 0",
        "low_severity_count: 0",
        f"total_deviations: {len(result.manual_triage_findings)}",
        "validation_complete: false",          # <-- still false
        "tasklist_ready: false",                # <-- still false
        f"manual_triage_count: {len(result.manual_triage_findings)}",
        "convergence_outcome: MANUAL_TRIAGE",
        "---",
        ...
    ]
```

Downstream gates therefore see `validation_complete: false` and refuse
to proceed. `_derive_fidelity_status` (`executor.py:2554-2570`) maps
this to `"fail"`, and `_format_halt_output` prints the runbook path.

### 3.7 Telemetry / audit trail

Every triage event appends a record to `deviation-registry.json`:

```json
{
  "triage_events": [
    {
      "timestamp": "2026-05-15T06:11:49Z",
      "run_number": 3,
      "operator_allowlist": ["data_models:spec_file", "nfrs:spec_nfr"],
      "findings": ["dd52050c...", "9fcc342b..."],
      "remediated_this_run": 5,
      "remediated_count_proof": "delta_active_high_count=5"
    }
  ]
}
```

The `remediated_this_run` proof-of-life value is required; refuse to
write triage if it is zero. This is the structural defense against
Attack 1b (skip-everything via buggy checker).

## Risks (residual)

- **Operator complacency**: a team that habitually passes
  `--triage-allow` for every release will silently let parser noise
  certify as clean. **Mitigation**: emit a sprint-summary metric
  counting `triage_events.length` per release; flag >0 in the
  certification audit.
- **State pollution**: an aborted run leaves `MANUAL_TRIAGE` findings
  in the registry. **Mitigation**: `load_or_create` already resets on
  `spec_hash` mismatch (`convergence.py:127`); add a corresponding
  reset on the first run of a new release.

## Expected impact on the failing case

- Run 1: 15 HIGHs created, 5 remediated, 10 ACTIVE remaining
  (`files_affected=[]`).
- Run 2: still 10 ACTIVE. With *no* allowlist (default), halt with
  `halt_reason="Convergence not reached"` — identical to today.
- Run 2 with `--triage-allow data_models:spec_file
  --triage-allow nfrs:spec_nfr`: 10 findings transition to
  `MANUAL_TRIAGE`, registry records the event, pipeline halts with
  `manual-triage.md` runbook and `convergence_outcome: MANUAL_TRIAGE`.
- Downstream: `wiring-verification`, `deviation-analysis`, `remediate`,
  `certify` **never run**. The release does not certify as clean. The
  operator gets a structured retry path.

## Estimated effort

- Code: ~120 LOC in `convergence.py` (registry triage, allowlist
  parser, runbook emitter), ~20 LOC in `executor.py`
  (`_write_convergence_report`, `_run_convergence_spec_fidelity`),
  ~5 LOC in `models.py`, ~30 LOC in `commands.py` (CLI flag).
- Tests: 5 new convergence tests (no-allowlist halt, allowlist halt,
  allowlist + zero-remediation refusal, MANUAL_TRIAGE survives
  registry round-trip, runbook content sanity), 2 gate tests
  (`spec-fidelity.md` with `manual_triage_count > 0` fails the gate).
- Time: ~2 hours.

## Files touched

- `src/superclaude/cli/roadmap/convergence.py`
- `src/superclaude/cli/roadmap/executor.py`
- `src/superclaude/cli/roadmap/models.py`
- `src/superclaude/cli/roadmap/commands.py`
- `src/superclaude/cli/roadmap/remediate.py` (treat MANUAL_TRIAGE as
  terminal alongside SKIPPED — single-line change)
- `src/superclaude/cli/roadmap/remediate_executor.py` (same)
- `tests/cli/roadmap/test_convergence.py`
- `tests/cli/roadmap/test_gates.py`

## Recommended combination

- **S6 alone**: surfaces the problem clearly, unblocks via triage, but
  the underlying parser bug persists. Standalone confidence ~70%.
- **S6 + S1 (regex hardening)**: parser stops producing ghost
  findings; S6 becomes a defense-in-depth safety net. Combined
  confidence ~88%.
- **S6 + S2 (description normalization)**: similar story; combined
  confidence ~85%.

## Final confidence

- Standalone refactored: **70%**.
- Combined with S1 + S2: **88%**.
