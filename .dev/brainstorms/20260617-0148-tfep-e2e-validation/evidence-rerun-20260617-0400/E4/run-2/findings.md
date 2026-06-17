# E4 — Safety-Invariant Preservation (rerun v2, run-2)

Independent read-only re-execution. No edits/stages/commits. Sibling runs not read.

- Worktree: `/config/workspace/IronClaude/.dev/worktrees/tfep-troubleshoot-backend`
- T1 = `src/superclaude/skills/sc-task-protocol/SKILL.md`
- R1 = `src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md`
- BASE = `.dev/tasks/to-do/TASK-RF-tfep-troubleshoot-migration-20260616-174519/phase-outputs/plans/freeze-block-preserved.md`
- All probes run under `LC_ALL=C`.

---

## I1 — FREEZE BYTE-IDENTITY

live.txt:
```
**Step 1: Halt and freeze**

1. **STOP** testing immediately.
2. **FREEZE** implementation — no further code changes permitted.
```
diff -u output: (empty — no differences) ; DIFF_EXIT=0

Finding: live freeze block from T1 is byte-identical to baseline reconstruction. EXPECT 0 met.

---

## I1b — BASELINE SELF-CONSISTENCY (corrected)
stdout:
```
11:1. **STOP** testing immediately.
12:2. **FREEZE** implementation — no further code changes permitted.
EXIT=0
```
Finding: 2 matches (>=1), exit 0. Baseline self-consistent; anchors I1.

---

## I2 — Safety gates (both >=1)
gate a stdout:
```
224:- If `test_is_wrong == true`: Present to user for review. Do NOT auto-fix tests.
```
gate b stdout:
```
225:- If `remediation_target == "docs"`: present to user for spec/stakeholder review. Do NOT auto-insert a code remediation.
```
Finding: Both safety gates present; route to user review, explicit no-auto-fix/no-auto-insert.

---

## I3 — Single backend declaration + neutral clause
count stdout: `1`
neutral stdout:
```
137:**Diagnostic backend:** `troubleshoot` (the `/sc:troubleshoot` skill; see `sc:troubleshoot-protocol`). The TFEP references below are backend-neutral — swapping the backend changes only this declaration and the invocation string.
```
Finding: Exactly one declaration with backend-neutral clause.

---

## I4a — Incident artifact rebind
stdout:
```
260:- **Diagnostic artifacts**: troubleshoot `report_path` (REPORT.md), `audit_log_path` (audit.log), and any additional diagnostic artifacts emitted by the backend
EXIT=0
```
Finding: >=1, exit 0. Artifacts rebound to report_path/REPORT.md + audit_log_path.

---

## I4b — Legacy verdict artifacts absent
stdout: (empty; rg -c emits nothing, exits 1 when count is 0) -> count == 0
Finding: Zero rca-verdict/solution-verdict occurrences.

---

## I5 — Report-template MUST-NOT-change rules
stdout:
```
92:**Files that MUST NOT change** (REQUIRED when `Test is wrong: true` OR `Behavior is documented: true` ...)
276:- An explicit **`## Files that MUST NOT change`** subsection MUST appear under Proposed Fix ...
285:Set `Behavior is documented: true` (and `behavior_is_documented=true` in the output contract) ...
291:Mutually exclusive with `Test is wrong: true` **by construction, not by tiebreaker**. ...
297:- A `## Files that MUST NOT change` subsection MUST appear listing every code file ...
```
Finding: >=1 (5 matches). Report-template enforces MUST-NOT-change + behavior_is_documented rule.

---

## I6 — FALSIFICATION (negative probe)
stdout: (empty) ; NEG_EXIT=1
Finding: 0 hits. No forensic/troubleshoot backend tokens leaked into the frozen TFEP block.

---

## Acceptance
| AC | Criterion | Result |
|----|-----------|--------|
| AC4.1 | DIFF_EXIT=0 | PASS |
| AC4.2 | both gates >=1 | PASS |
| AC4.3 | one decl + neutral clause | PASS |
| AC4.4 | I4a>=1 AND I4b==0 | PASS |
| AC4.5 | report-template rules | PASS |
| AC4.6 | zero forensic/troubleshoot in freeze | PASS |
| AC4.7 | baseline self-consistent (I1b>=1) | PASS |

normalized_observation_digest: `1c6bb52e67cd1d72190461abb077a88ad2a5cd75a2ac3741065404ed711ede95`

## Verdict
**PASS** — all 7 acceptance criteria satisfied.
