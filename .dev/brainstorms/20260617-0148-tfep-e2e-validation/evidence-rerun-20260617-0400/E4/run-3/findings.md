# E4 — Safety-Invariant Preservation — run-3 (RE-RUN v2)

Worktree: /config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend
Files under test:
- T1 = src/superclaude/skills/sc-task-protocol/SKILL.md
- R1 = src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md
- BASE = .dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md

All probes executed with LC_ALL=C. Re-run v2 with corrected probe regexes (I1b, I4a).

## I1 — FREEZE BYTE-IDENTITY
Command:
  sed -n '/\*\*Step 1: Halt and freeze\*\*/,/FREEZE.*implementation/p' $T1 > /tmp/e4v2r3_live.txt
  diff -u /tmp/e4v2r3_base.txt /tmp/e4v2r3_live.txt
Live freeze block:
  **Step 1: Halt and freeze**

  1. **STOP** testing immediately.
  2. **FREEZE** implementation — no further code changes permitted.
diff -u output (full): (empty — no differences)
DIFF_EXIT=0
Finding: Freeze block in live T1 is byte-identical to expected built from 4 BASE freeze lines. No additions/deletions/whitespace drift. AC4.1 satisfied.

## I1b — BASELINE SELF-CONSISTENCY (CORRECTED)
Command: rg -n "STOP.* testing immediately|FREEZE.*implementation.*no further code changes permitted" $BASE
stdout:
  11:1. **STOP** testing immediately.
  12:2. **FREEZE** implementation — no further code changes permitted.
EXIT=0
Finding: BASE contains both freeze sentinel lines (2 hits, >=1 required). Expected fixture anchored to valid source. AC4.7 satisfied.

## I2 — SAFETY GATES
I2a: rg -n "test_is_wrong == true.*Present to user|Do NOT auto-fix tests" $T1
  224:- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
  I2a_EXIT=0
I2b: rg -n "remediation_target == .docs.*present to user|Do NOT auto-insert" $T1
  225:- If `remediation_target == "docs"`: present to user for spec/stakeholder review. Do NOT auto-insert a code remediation.
  I2b_EXIT=0
Finding: Both human-in-the-loop safety gates present (each >=1). AC4.2 satisfied.

## I3 — BACKEND DECLARATION + NEUTRAL CLAUSE
I3a: rg -c "\*\*Diagnostic backend:\*\*" $T1  -> 1  (I3a_EXIT=0)
I3b: rg -n "backend-neutral|swapping the backend changes only this declaration" $T1
  137:**Diagnostic backend:** `troubleshoot` (the `/sc:troubleshoot` skill; see `sc:troubleshoot-protocol`). The TFEP references below are backend-neutral — swapping the backend changes only this declaration and the invocation string.
  I3b_EXIT=0
Finding: Exactly one **Diagnostic backend:** declaration (count==1) plus backend-neutral clause same line. AC4.3 satisfied.

## I4 — DIAGNOSTIC ARTIFACTS PRESENT, VERDICT ARTIFACTS ABSENT
I4a (CORRECTED): rg -n "Diagnostic artifacts.*report_path.*REPORT\.md.*audit_log_path" $T1
  260:- **Diagnostic artifacts**: troubleshoot `report_path` (REPORT.md), `audit_log_path` (audit.log), and any additional diagnostic artifacts emitted by the backend
  I4a_EXIT=0 (>=1)
I4b: rg -c "rca-verdict|solution-verdict" $T1  -> (empty)  I4b_EXIT=1 (count==0)
Finding: Generic diagnostic-artifacts contract present; legacy verdict tokens fully absent (count 0; rg -c prints nothing and exits 1 on zero matches). AC4.4 satisfied.

## I5 — REPORT-TEMPLATE MUST-NOT-CHANGE RULES
Command: rg -n "Files that MUST NOT change|behavior_is_documented" $R1
  92:**Files that MUST NOT change** (REQUIRED when `Test is wrong: true` OR `Behavior is documented: true` ...)
  276:- An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix ...
  285:- Set `Behavior is documented: true` (and `behavior_is_documented=true` in the output contract) when ALL three conditions hold:
  291:- Mutually exclusive with `Test is wrong: true` by construction ...
  297:- A `## Files that MUST NOT change` subsection MUST appear listing every code file ...
  I5_EXIT=0 (>=1)
Finding: Report-template preserves MUST-NOT-change rules and behavior_is_documented derivation/trigger logic. AC4.5 satisfied.

## I6 — FALSIFICATION (negative probe)
Command: rg -n "forensic|troubleshoot" /tmp/e4v2r3_live.txt  -> (empty)  NEG_EXIT=1
Finding: Zero forensic/troubleshoot occurrences in freeze block. Backend vocabulary did not leak into Step 1 freeze invariant. AC4.6 satisfied.

## Normalized observations
backend_decl_count=1
baseline_self_consistent=true
freeze_backend_token_absent=true
freeze_diff_exit=0
gate_docs=true
gate_test_is_wrong=true
incident_rebind=true
neutral_clause=true
report_template_rules=true
verdict_artifacts_absent=true

normalized_observation_digest: 1c6bb52e67cd1d72190461abb077a88ad2a5cd75a2ac3741065404ed711ede95

## Verdict
PASS — all 7 acceptance criteria (AC4.1–AC4.7) satisfied with deterministic evidence. Safety invariants preserved (freeze byte-identity, both gates, single backend-neutral declaration, artifact-contract migration, report-template guardrails, no vocabulary leak). Baseline self-consistent.
