# QA Report — Report Qualitative Review (Actionability Lens)

**Topic:** TASK-RF-detection-contract — contract-status readiness surface + pr-submit missing-contract halt
**Date:** 2026-07-02
**Phase:** report-validation (task-integrity) / actionability lens
**Fix cycle:** N/A (fix_authorization: false — report only)

---

## VERDICT: PASS

All three checklist items pass. Every one of the 9 diagnosis states maps to a
correct, safe, actionable next step; the pr-submit missing-contract halt is
unambiguous and carries the exact no-side-effect sentence; and the ready-state
command carries PR context (never a bare `--monitor 1`). Both next-command
functions (`_next_command` in `diagnosis.py`, `_contract_status_next_command`
in `commands.py`) agree across all states. Verified against source, live-rendered
output, and the authoritative spec §3 "Default action" table.

---

## State → Command Matrix

Source of truth for "intended default action": `merged-requirements.md` §3
(lines 67-77). Rendered command verified live via both `_next_command`
(diagnosis.py:367-388) and `_contract_status_next_command` (commands.py:189-213).

| State | Spec §3 default action | Rendered next_command | Safe? | Actionable? | Verdict |
|-------|------------------------|-----------------------|-------|-------------|---------|
| `missing` | Print setup command and stop | `superclaude reflect contract-status --repo <owner/repo> --pr <number>` | Read-only, no writes | Points to the only v1 readiness surface | PASS |
| `unlocked` | Validate candidate if evidence exists | `superclaude reflect contract-status --validate --repo … --pr …` | `--validate` degrades to "validation skipped: no evidence path" when evidence absent (commands.py:114-115) — never crashes | Yes | PASS |
| `unparseable` | Preserve file; offer regenerate from evidence | `superclaude reflect contract-status --repo … --pr …` | Read-only; preserves file | Re-surfaces diagnosis+blockers; regeneration is out-of-scope for v1 read-only CLI | PASS (weakest match — see Observations) |
| `evidence_missing` | Re-probe or revalidate before use | `superclaude reflect contract-status --validate --repo … --pr …` | `--validate` no-evidence path is guarded | Yes (revalidate) | PASS |
| `validation_missing` | Run validation | `superclaude reflect contract-status --validate --repo … --pr …` | Writes only under evidence probe dir on confirmed path | Yes — directly runs validation | PASS |
| `validation_failed` | Show blockers and alternatives | `superclaude reflect contract-status --validate --repo … --pr …` | Re-derives + re-writes report; CLI render shows `blockers:` list | Yes (revalidate); blockers surfaced in render (commands.py:170-173) | PASS |
| `stale` | Revalidate or recapture | `superclaude reflect contract-status --validate --repo … --pr …` | Re-runs validate → fresh report; stale blockers recomputed (diagnosis.py:329-356) | Yes (revalidate) | PASS |
| `ready` | `/sc:pr-submit --monitor >=1 --pr <number>` may proceed | `/sc:pr-submit --monitor 1 --pr 42` (concrete) / `--pr <number>` (placeholder) | N/A (proceed) | Yes, PR context always present | PASS |
| `declined_by_user` | Leave existing contract untouched | `cancelled: setup declined by user; existing contract files left untouched` | Terminal no-op; touches no files (diagnosis.py:207-230) | Terminal state — correctly a status, not a command | PASS |

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every diagnosis state maps to a correct, safe next command | PASS | Live-rendered all 9 states via both `_next_command` and `_contract_status_next_command`; each matches spec §3 default action (see matrix). `--validate` no-evidence path guarded (commands.py:113-115). No state emits a wrong or unsafe command. |
| 2 | pr-submit missing-contract halt is unambiguous | PASS | Live-rendered MISSING halt via `render_pr_submit_missing_contract_halt` (diagnosis.py:233-255): (a) names readiness command `superclaude reflect contract-status --repo <owner/repo> --pr <number>` under "Next safe step:"; (b) contains exact sentence `No monitor was armed. No comments, pushes, retries, resolves, or retriggers were performed.` verbatim (diagnosis.py:245); (c) pr-submit.md:61 + SKILL.md:90 both instruct rerun of `/sc:pr-submit --monitor 1 --pr <number>` only after a validated lock. |
| 3 | Ready-state next command includes PR context | PASS | diagnosis.py:375 + commands.py:200 both return `/sc:pr-submit --monitor 1{pr_arg}` where `pr_arg` is always ` --pr {n}` or ` --pr <number>`. Live-rendered: `/sc:pr-submit --monitor 1 --pr 42` and `--pr <number>`. Never bare `--monitor 1`. Locked by test assertions (test_detection_contract.py:98-107). |

---

## Summary

- Checks passed: 3 / 3
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

None.

## Observations (non-blocking, not findings)

- **`unparseable` → plain `contract-status`** is the weakest spec-to-command
  match: spec §3 says "offer regenerate from evidence," while the rendered
  command re-runs the read-only diagnosis (which preserves the file and
  re-surfaces blockers) rather than regenerating. This is *safe and not wrong* —
  regeneration is an interactive setup-helper concern explicitly out of scope for
  the v1 read-only CLI surface (merged-requirements.md §"Do not arm/write by
  default"). The operator is correctly routed to the only safe v1 surface that
  exists. Recorded as an observation, not a finding; no severity.
- **`declined_by_user` next_command is a status string, not a command.** This is
  spec-correct: §3's default action is the terminal no-op "Leave existing contract
  untouched." A terminal state has no forward command; emitting a cancellation
  status is the actionable-correct behavior.

## Consistency cross-checks (verified)

- Exact no-side-effect sentence is byte-identical across all three surfaces:
  `render_pr_submit_missing_contract_halt` (diagnosis.py:245), pr-submit.md:61,
  and SKILL.md:90.
- `_next_command` (diagnosis.py) and `_contract_status_next_command` (commands.py)
  produce identical output for every state (verified live for all 9).
- 22 relevant tests pass: `test_contract_setup_next_commands_are_current_and_actionable`
  + 13 diagnosis + 8 contract-status CLI.

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- Relied on the inventory's report of test counts / sync status (final-output-inventory.md:44-53); did not re-run the full 74+18+40 suites, only the 22 tests bearing on the three actionability checks.

**(b) Independent semantic checks (≥1 required, INV-019):**
- State→command correctness: independently live-rendered all 9 states through both next-command functions and cross-checked each against spec §3's authoritative "Default action" table — a semantic check (does the command match the operator's intended next action?) that structural QA (field presence) cannot make. Tool evidence: `uv run python -c` renders above; diagnosis.py:367-388; commands.py:189-213; merged-requirements.md:67-77.
- Halt unambiguity: independently live-rendered the MISSING halt and byte-matched the no-side-effect sentence + readiness command against the doc/SKILL source. Tool evidence: `render_pr_submit_missing_contract_halt` render above; diagnosis.py:245; pr-submit.md:61; SKILL.md:90.
- Guarded `--validate` no-evidence path: read commands.py:113-115 to confirm the `--validate`-routed states never crash when evidence is absent (actionability, not structure).

**Confidence:** Verified: 3/3 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep(Bash): 5 | Glob: 0 | Bash(python/pytest): 3
**Web research:** none performed (all verification local-file-bound).

## Recommendations

- None blocking. Proceed. Optional future enhancement (not required for this
  task's scope): if a v2 interactive setup-helper surface lands, revisit the
  `unparseable` next_command to route to "regenerate from evidence" per spec §3.

## QA Complete
