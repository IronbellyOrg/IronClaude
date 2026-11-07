# Refactoring Plan: D-P2-23

## Overview
- Base variant: Variant 1 (option A, skip the whole CLI-mode reflect gate under --unattended)
- Incorporated variants: Variant 2 (option B), strengths only
- Planned changes: 3 (all additive, to the decision record; none edits `SKILL.md`)
- Overall risk: Low
- Scope note: the merged output is a decision record. It does not edit `src/superclaude/skills/task-builder/SKILL.md` or any other repository file; the paragraph at `SKILL.md:410` is accepted as it stands.

## Planned Changes

### Change 1: Name the recovery path for the audit that option A gives up
- Source: Variant 2, "Claimed strengths" (independent audit as a coordinator-readable artifact; U-002, C-005) and its use of `--no-promote` (U-003)
- Target location in base: after Variant 1's "Claimed weakness" line
- Integration approach: append
- Rationale: C-005 won by Variant 2 at 95 confidence, conceded by the Variant 1 advocate; both advocates recommended the same recovery. Spec line 148 (reflect row): the brief passes no `--remediate`, and `--no-promote` when the coordinator owns folder moves.
- Text to add: "Recovery: the coordinator audits the finished task itself with `/sc:reflect --mode post --no-promote` (reflect row of spec section 3.1: no `--remediate`, `--no-promote` while the coordinator owns folder moves). This is a coordinator step in the run plan, not task-builder text."
- Risk: Low (additive; no repository file changes)

### Change 2: Carry the build-time versus run-time gap as an open item
- Source: shared assumption A-001 (both advocates QUALIFY); Variant 2 advocate's point that the builder can only decide which item to emit
- Target location in base: new section "Open items" after the weakness and recovery lines
- Integration approach: insert
- Rationale: `SKILL.md:410` sits in build step A.3 while the gate item (`:2237`) is a checklist item run later by `/task`. The paragraph says the gate "is skipped" and that the log records it, without saying whether the builder omits the item or emits it in skip form. Not resolved by the debate and not changed here (scope discipline); stated so the owner can decide.
- Risk: Low

### Change 3: Carry the "recorded in the task log vs recorded in the contract" observation
- Source: orchestrator reading of spec line 62 against `tdd.md:166-168`
- Target location in base: "Open items"
- Integration approach: insert
- Rationale: spec 2.1 says the caller "records the skip in its contract"; `SKILL.md:410` and `tdd.md:168` record it "in the task log". `tdd.md:166` lists "the MDTM task folder files the run wrote" in `artifacts`, so the skip is reachable from the contract only if the task log is one of those files. UNVERIFIED; not a blocker, not changed here.
- Risk: Low

## Base Weaknesses and Which Variant Addresses Them
| Base weakness | Better variant | Fix approach |
|---------------|----------------|--------------|
| Loses the independent post-execution audit (C-005) | Variant 2 | Change 1: coordinator-run `/sc:reflect --mode post --no-promote` |
| No failure signal for Regression or Drift (C-003, unresolved) | Variant 2, partly | Covered by the same coordinator audit; C-003 stays unresolved because B's blocked result conflicts with the HALT-on-10/11/2 text at `SKILL.md:2239` |

## Changes NOT Being Made
| Diff point | Non-base approach | Why the base approach wins |
|------------|-------------------|----------------------------|
| C-001 | Run `superclaude reflect run <task> --depth deep --no-promote` under `--unattended` | The wrapper has no `--unattended` (zero matches in `commands.py`) and its inner prompt carries none (`runner.py:453-483`); B never shows it is gate-free; callers and pinned tests already say "skipped" (`tdd.md:168`, `test_worker_contract.py:564,2709-2724`). Won 85 confidence, unanimous. |
| C-002, X-001, X-002 | Leave staging to the coordinator or replace it with a note, but keep the audit | WC-9 refuses the `git add -A` step (spec line 77), and the wrapper's audit omits never-staged files (`SKILL.md:2239`), so the retained audit would be incomplete. Won 92, 95 and 85 confidence. |
| C-004 | Treat the wrapper as gate-free | Spec 2.1 requires gate-free per the callee's section 3 row or a recorded skip; no such row exists for the wrapper. Won 95 confidence, B's advocate conceded. |
| C-006 | Longer disclosure of risks | Unresolved; disclosure style does not change the choice. |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1 | Low | Adds one sentence to the decision record | Delete the sentence |
| 2 | Low | Adds an open item | Delete the item |
| 3 | Low | Adds an open item | Delete the item |

## Review Status
- Approval: auto-approved (non-interactive run)
- Timestamp: 2026-11-07
