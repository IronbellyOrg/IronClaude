# Refactoring Plan: Merge into Base (Variant A, OURS) (D07, topology)

## Overview
- Base: Variant A (OURS), file `variant-1-original.md`
- Incorporating strengths from: Variant B (CLAY), file `variant-2-original.md`
- Planned changes: 8 (5 from Variant B, 3 conditions that come from the invariant probe and the debate)
- Risk level: Medium (changes 1 and 2 add new rules to a design that has no code for them yet)
- The merged output is a unified topology recommendation, not a new position paper: it keeps the structure of the base and replaces the "gets right" and "costs" sections with the merged rules.

## Planned Changes

### Change 1: Per-coordinator in-flight cap with a fail-closed count (from Variant B)
- **Source**: Variant B, mechanism 3 and 4, fact 5; DESIGN lines 700-702; `route.py` `in_flight`
- **Target**: Base, Section 2 (mechanism), new item 6; Section 4, remove "no in-flight cap"
- **Rationale**: C-004, CLAY 85% from both advocates; grep finds no cap in the owner's code. The six safety properties come from the CLAY rebuttal (count once; write `pending` before any send; the cap limits new work only, not resends or resume). Conditions from the probe: the check runs inside the child cycle after the sweep (INV-001, HIGH); "in flight" has a closing writer and an expiry so `unknown` entries and abandoned claims cannot fill the cap for good (INV-002, HIGH); `launched` entries count (INV-003); the cap is per coordinator id, not per project (INV-008).
- **Integration point**: insert; the key `max_in_flight` (default 3) lives in the per-repo config.
- **Risk**: Medium, because INV-001 and INV-002 show the first adoptable text would have deadlocked a full repo.

### Change 2: Restart of a dead coordinator with resume, guarded (from Variant B)
- **Source**: Variant B, fact 6; DESIGN line 710; `route.py` `end_finished` lines 562-603
- **Target**: Base, Section 2, new item 7
- **Rationale**: C-005 split, 73%. Guards: an unreadable terminal list decides nothing; resume only when acknowledged work is in flight (an unacknowledged wake is left to the resend); restarts are bounded by a counter kept in the store (3 attempts, as DQ2) (INV-005 HIGH, INV-006). A restart is counted against the 270 s sweep budget (INV-006). Until Coder issue 516 creates `COORD-<RepoName>`, the session that holds the duties is `ORCH-IronClaude`, so no restart targets a name that is not the duty holder (INV-005).
- **Integration point**: insert after the cap; the idle end is NOT adopted.
- **Risk**: Medium. Session detection by name or tag is UNVERIFIED on both sides (U25).

### Change 3: Per-repo settings keys in the per-repo config (from Variant B)
- **Source**: Variant B, fact 4; DESIGN lines 879-889
- **Target**: Base, Section 2, new item 8
- **Rationale**: C-007, 67%. Keys: `merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`; filled only with values that can be read or that the owner names; read at merge time by the coordinator, never by the watcher. Condition INV-011: the config directory is "not tamper-protected" (`launch.py` comment), so the safety list and `can_merge` must be overridden by the live GitHub role at merge time, and the safety list changes only on the owner's recorded word.
- **Integration point**: insert; merge authority itself is decided in topic D06.
- **Risk**: Low to Medium.

### Change 4: Org-wide search as an optional pre-check (from Variant B)
- **Source**: Variant B, mechanism 1, fact 3; DESIGN line 137
- **Target**: Base, Section 2, new item 9, marked optional and off in the first build
- **Rationale**: C-003, A-002 and A-005. The gain is small with six repos (the probe puts the saving at about 6 calls per idle repo). It fails open: a failed search, 100 or more results or a missing field skips nothing (INV-010: a successful empty reply can still be wrong because of index delay, so it never skips a repo that has work in flight or a dead coordinator).
- **Integration point**: append; the restart check runs first.
- **Risk**: Low.

### Change 5: Exclusive-create state file per issue and a short-name check (from Variant B)
- **Source**: Variant B, facts 7 and 8; DESIGN lines 702, 704
- **Target**: Base, Section 2, new item 10
- **Rationale**: U-011 and U-013. Per-issue state file beside the claim. The config, store and worktree are keyed on `owner/name`, not the display name, and two repos with one short name are refused (INV-009).
- **Integration point**: insert.
- **Risk**: Low.

### Change 6: Claim agents never share the standing coordinator's worktree (condition from the probe)
- **Source**: invariant probe INV-004 (HIGH); `launch.py` `launch_argv`; `merged-requirements.md` line 1145 ("one worktree holds one live agent at a time")
- **Target**: Base, Section 4 (costs) and a new condition in Section 2
- **Rationale**: REQ R10 makes the watcher's worktree the same `Coordinator` worktree where the coordinator session works, and the dispatcher starts each claim agent there. With a cap of 3 that is up to four agents in one tree and breaks the Q26 claim procedure ("no other unpushed commit"). The spec must separate the claim worktree from the standing coordinator's worktree or run the claim before the cap is raised above 1.
- **Integration point**: replace the sentence in Section 2 item 3.
- **Risk**: Medium. This is a defect of the owner's own plan found by the debate.

### Change 7: Prerequisites stated as dependencies, not as "alone" (condition from the probe)
- **Source**: INV-012 (HIGH); REQ R6, R9, R10, R20, R21; `launch.py` `GOVERNED_LEVELS_ALLOWED = False`
- **Target**: Base, Section 4 (costs)
- **Rationale**: the topology plus the adoptions does not work alone. It needs Coder issue 515 (cron), Coder issue 516 (Coordinator branch, worktree and session), the branch name decision, a push grant, and a worktree path read from `orca worktree list` instead of the literal `/home/coder/workspaces/worktrees` (INV-012 falsifier 5, UNVERIFIED beyond the probe's read).
- **Integration point**: replace the "no in-flight cap and no idle end" cost line and add a "Prerequisites" line.
- **Risk**: Low.

### Change 8: Make the unresolved name an owner decision (condition from the debate)
- **Source**: X-005, C-010, Round 2 OURS item (a)
- **Target**: Base, Section 4
- **Rationale**: `coordinators` (exists on the fork, Q26) against `Coordinator` (REQ R10, R20), and one `COORD-<RepoName>` per project against Q26's per-scope coordinators. Spec text: "Every project has one standing issue-pipeline coordinator, session `COORD-<RepoName>`, in worktree `Coordinator`. It is one of the coordinators Q26 allows; its records go under `.dev/coordinators/` on the shared branch. Whether that branch is `Coordinator` or `coordinators` is an open owner decision." The name decisions belong to topic D08.
- **Integration point**: replace.
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001 | Session in the orchestrator repo workspace with `cd <checkout> &&` | DESIGN line 136 marks the directory premise UNVERIFIED; OURS starts in a worktree with the right origin. CLAY advocate conceded (85%) |
| C-002 | Git-ignored `.orchestrator/` registry in a separate repo | Host-local state; DESIGN line 708 itself falls back to a lease comment for two hosts. Both advocates agreed |
| C-003 | Hand-kept `repos.yaml` allow list as the discovery gate | Manual per host (REQ R17); `SKIP_REASONS` already says "seen but not allowed"; the approval gate and first-run check do the safety job |
| C-005 | 30-minute idle end | REQ R9 requires a running coordinator in every project; DESIGN line 710 says an ended session costs no tokens, so the saving is small |
| C-004 | Poll starts another orchestrator when the first is full | R17's standing authorization covers one named session; an extra session needs its own name and approval. A 4th issue waits, and the wait must be visible as a skip reason |
| U-008 | `wrong_target` refusal | One coordinator per project plus the origin check leaves no wrong target; revisit if two hosts start one name |
| C-012 | `orgs` list in `repos.yaml` for two organizations | `allowed_owners` is already a list key in `defaults.py` |
| C-008 | Separate `IronbellyOrg/IronOrchestrator` repo | Manual clone and path per host; no benefit that a project-local layout lacks |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | A full repo never drains, or work starts past the cap | Drop the cap; keep one launch per sweep |
| 2 | Medium | A second coordinator starts beside a live one | Do not adopt; leave restart to the Coder 516 boot check |
| 3 | Low-Medium | A safety list is edited by a worker | Keep the keys in the coordinator's own protected record |
| 4 | Low | Missed assignment for one sweep | Remove the pre-check |
| 5 | Low | Duplicate state for one issue | Remove the file |
| 6 | Medium | Refused or polluted claim push | Run claims one at a time |
| 7 | Low | Misleading plan | Edit the text |
| 8 | Low | Open name carried forward | Owner decides in D08 |

## Review Status
- [x] Auto-approved (default, `--unattended`)
- Approved by: auto
- Approval timestamp: 2026-11-20
