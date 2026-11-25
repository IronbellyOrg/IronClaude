# Refactoring Plan (Step 4)

## Overview

- Base: Variant 1 (OURS), `adversarial/variant-1-original.md`
- Incorporated from: Variant 2 (CLAY), plus corrections forced by the Round 2 concessions and the Round 2.5 invariant probe
- Changes planned: 12 (6 incorporations, 6 corrections of the base); changes not made: 5
- Overall risk: Low to Medium (text only; one change turns a hard HIGH finding into a mandatory precondition)
- Merged output path: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/merged-output.md`

The merged output is a single position statement "what to do about PR 682" that the D03 verdict will use. Its section list stays the base's six sections (Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right), plus two new sections at the end: "Conditions and sequencing" and "Unresolved and unverified".

## Planned Changes

### Change 1: Mandatory sequencing with PR 686 (INV-001, HIGH)
- Source: debate-orchestrator, from `invariant-probe.md` INV-001; V2 fact 6 (removal order) and C-005
- Target: Mechanism (new step 4) and new section "Conditions and sequencing"
- Approach: insert
- Rationale: a revert and PR 686 (head 8e5ae29ad) merge without a git conflict but give a broken command line (`superclaude --help` crashes, 29 test modules fail at collection). The merged text must say: PR 686 must not merge before the revert is settled; if the revert lands first, PR 686 needs a revision that leaves the `issue_watch` symbols the package imports (`EditEvidence`, `LabelEvent`, `CommentEdit`, `_argv_rest_page`, `github.edits`, `github.events`, `cycle.validate_approvers`) in place or a shim; a check that runs `superclaude --help` and imports the package must be a merge condition. Which order is chosen belongs to D14.
- Risk: Low (additive)

### Change 2: Keep the no `--to` bullet by hand (U-007, INV-002)
- Source: V2 contribution U-007; INV-002
- Target: Mechanism step 1
- Approach: insert
- Rationale: a bare `git revert` drops the standalone bullet and the assertions at `tests/skills/test_worker_contract.py` lines 426-429 and 3220; both advocates agree to keep them. The merged text says to re-apply them by hand after the revert and accept that the sentence then appears twice (WC-17 and the bullet), or to reword WC-17 to point at the bullet.
- Risk: Low

### Change 3: Creation-time plan sections stay as an extra layer (U-006, C-003)
- Source: V2 fact 3 and Mechanism 3 (`sc-issue-protocol/SKILL.md:102`, PRs 651 and 661)
- Target: What it gets right
- Approach: append
- Rationale: independent of the gate, adopted by V1 in Round 2 and accepted by V2.
- Risk: Low

### Change 4: State the cost of the gate and the same-login limit (C-004, C-010, U-009)
- Source: V2 facts 3 and 4
- Target: What it costs (new bullet) and What it risks (L-1 bullet)
- Approach: insert
- Rationale: both advocates concede these as real. L-1 stays an accepted risk (`owner-answers.md:126`), not hidden. Add the INV-006 point: a "written ruling by ironbelly" is not a checkable gate while one login serves person and agents, so the ruling is recorded through the owner's chat and the agent records it (decision D2 text in WORKER-CONTRACT.md).
- Risk: Low

### Change 5: Removal plan and PR B tests as the bar for any replacement (U-005, U-008)
- Source: V2 Mechanism 4, facts 7 and the design lines 978-1004 and 1108-1112
- Target: new section "Conditions and sequencing"
- Approach: insert
- Rationale: if D01 ends assignment-only, PR 682 stands under three conditions already agreed by both advocates; the plan adds the bar: PR B's named tests (kill after each `intent` and before `done`, exclusive create refuses a second state file, two orchestrators given one issue create one state file) must pass before the watcher is enabled.
- Risk: Low

### Change 6: Correct condition 2 (INV-003)
- Source: INV-003
- Target: new section "Conditions and sequencing"
- Approach: replace (reword)
- Rationale: R33 (`GOVERNED_LEVELS_ALLOWED = False`) is not built (no hit on master, snapshots or owner branch commits); the only hold today is `cycle.py:228`, `raw.get("enabled", False)`. The condition becomes "R33 must be built before R18 default-on config is built".
- Risk: Low

### Change 7: Correct figures and scope of "never ran live" (X-001, INV-008)
- Source: Round 2 concessions; INV-008
- Target: Cited facts 3 and 7; What it costs
- Approach: replace
- Rationale: restored tests are 117 test functions (222 collected cases), not "about 80"; the owner worktree shows 223 status entries (70 outside `.dev/`), not 53, so the owner branch figure is marked stale; "never ran live" is scoped to the cron watcher; the package is 1,597 lines of the 4,599 deleted (2,969 tests, 1,618 src).
- Risk: Low

### Change 8: Installed copies and guard version stamp (INV-004, INV-005)
- Source: INV-004, INV-005
- Target: Mechanism (new step 5)
- Approach: insert
- Rationale: after the revert lands, hosts must run `superclaude install` to replace the stale guard, contract and command copies; the guard version stamp stays 1 in the revert (raising it is a guard change needing the independent review); hosts that installed between 00:02Z and the revert have a guard without rule 1 next to restored coordinator-only verbs, so the guard's independent review is also the check.
- Risk: Medium (touches a security hook; review required)

### Change 9: Amend R1 and section 7 of the design in the same PR (INV-011)
- Source: INV-011
- Target: Mechanism (new step 6)
- Approach: insert
- Rationale: PR 681's design says the opposite of the restored code (`orchestrator.md` lines 73, 987-991, 997-1004, 1017, 1095, 1381). A revert alone leaves PRs A, B, E building against text that says the gate is retired. Either the revert PR amends R1 and section 7 or a named follow-up does; the verdict names which.
- Risk: Low

### Change 10: CHANGELOG conflict (INV-007)
- Source: INV-007
- Target: Mechanism step 2
- Approach: replace
- Rationale: the actual textual conflict is `CHANGELOG.md` only; `WORKER-CONTRACT.md` (the `/sc:closeout` line) and `test_worker_contract.py` auto-merge. The "Removed: the old plan-approval gate" entry is dropped or reworded.
- Risk: Low

### Change 11: Process facts
- Source: V1 fact 2 plus Round 2 new evidence
- Target: Cited facts 2
- Approach: replace
- Rationale: add PR 681 merged 2026-11-20T00:02:33Z and PR 682 at 00:02:36Z, both by `clayphi`, 3 seconds apart; PR 682 had one automated review; issue 450 shows a question with no reply (not consent).
- Risk: Low

### Change 12: Unresolved and unverified section
- Source: Round 2.5 (INV-008, INV-009), Round 2 UNVERIFIED items
- Target: new section "Unresolved and unverified"
- Approach: insert
- Rationale: lists what is not settled: whether the restored test `test_the_watcher_record_module_is_not_edited` passes in a real checkout (unconfirmed, scratch copy was not a git checkout); that D01 decides the end state; identity of "the owner" in the design (UNVERIFIED); the untracked owner files `complete.py` and its tests were not checked against the revert tree; the full suite and `test_launch_level_guard.py` did not finish in the fault-finder's time limit.
- Risk: Low

## Changes NOT Being Made

| Diff point | V2 approach | Why the base approach stands |
|------------|-------------|-------------------------------|
| C-003 | Creation-time plan review replaces approval | Both advocates ended with V1: `hold.py` checks headings only and the creation-time plan is the author's own; it is kept as an extra layer, not a replacement. |
| C-005 (as a reason to keep) | Delete first so PR 686 needs no shim | Order is real, but it is a convenience for PR 686, not a reason to drop the gate; INV-001 shows a clean-looking merge breaks the CLI, so the plan sequences it rather than adopting V2's conclusion. |
| C-009 | F14 hardening as a V2 benefit | WC-17 at `01e7a9e23^` already said it; V2 relocated the sentence. Only the standalone bullet is kept (Change 2). |
| V2 "keep PR 682" | Keep the deletion as the end state | Conditional only: if D01 ends assignment-only, PR 682 stands under the Change 5 and 6 conditions. |
| Rebuild old behaviour inside PR 686 | Not proposed by either side | Out of scope for D03. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1 | Low | Prevents a broken CLI after a clean-looking merge | Delete the paragraph |
| 2 | Low | Keeps contract text for all bound workers | Remove the bullet |
| 8 | Medium | Security hook review | Revert the guard hunk |
| others | Low | Text accuracy | Edit text |

## Review Status

Auto-approved (unattended mode; no `--interactive`). Timestamp 2026-11-20 (UTC).
