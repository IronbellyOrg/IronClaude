# Merge Execution Log

## Metadata
- Base: Variant A (OURS), `variant-1-original.md`
- Executor: merge-executor agent
- Timestamp: 2026-11-20T04:29:48Z

- Changes applied: 8 of 8 planned
- Status: success
- Merged artifact: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/merged-output.md`
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/adversarial/refactor-plan.md`
- Variant B: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D07/adversarial/adversarial/variant-2-original.md`
- Note on locations: the merged artifact sits one folder above this log, as the task named it.

## Changes Applied

Validation words: PASS means the check found nothing wrong. Text with no source in the base, Variant B, the plan or the evidence files was not written.

### Change 1: Per-coordinator in-flight cap with a fail-closed count (from Variant B)
- **Status**: Applied
- **Source**: Variant B, mechanism 3 and 4, fact 5; DESIGN lines 700-702; `route.py` `in_flight`; CLAY Round 2 rebuttal items 1, 2 and 6; PROBE INV-001, INV-002, INV-003, INV-008
- **Target**: Base, Section 2 (mechanism), new item 6; Section 4, "no in-flight cap" removed (the removal is done in the same line as Change 7, see below)
- **Before**: The base had no cap. Section 4 said "It has no in-flight cap and no idle end; both are in Clay's 5.7."
- **After**: Item 6 gives the key `max_in_flight` (default 3) in `issue-watch.d/<repo>.json` and eight rules: runs inside the child cycle after the sweep (INV-001); per coordinator id, not per project (INV-008); counts `pending`, `launched`, `unknown` plus open claim files (INV-003); counts each issue once (`route.py` line 411); writes `pending` before any send (DESIGN 706); unreadable file counts as in flight (DESIGN 702); limits new work only and records `coordinator_full` so the wait is visible; names a closing writer and an expiry as a spec requirement, not yet designed (INV-002).
- **Provenance tag**: `<!-- Source: Variant B, mechanism 3 and 4, fact 5 (DESIGN lines 700-702; route.py in_flight), with the safety properties from the CLAY Round 2 rebuttal items 1, 2 and 6 and the probe conditions INV-001, INV-002, INV-003, INV-008 - merged per Change 1; ... -->`
- **Judgment calls**: (a) CLAY rebuttal items 3, 4 and 5 are restart properties and went to Change 2; item 7 (plan requests in the count, UNVERIFIED, applies only if plan requests are carried in) is not in the plan and was left out. (b) The plan gives no design for the closing writer or the expiry, so item 6 states the requirement and says neither is designed. (c) A clause was added that the default of 3 applies only once the item 3 worktree condition is met, so item 6 does not contradict Change 6.
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (one link clause added, see above)

### Change 2: Restart of a dead coordinator with resume, guarded (from Variant B)
- **Status**: Applied
- **Source**: Variant B, fact 6; DESIGN line 710; `route.py` `end_finished` lines 562-603; CLAY Round 2 items 3, 4, 5; PROBE INV-005, INV-006
- **Target**: Base, Section 2, new item 7
- **Before**: The base had only "restarted if stopped" inside item 3 and listed restart as an uncarried capability in Section 6.
- **After**: Item 7 has the guards: an unreadable terminal list decides nothing; resume only for acknowledged work; bounded at 3 attempts by a counter kept in the store (the counter and wake channel are new, INV-006); counted against the 270 s sweep budget (22.5 to 27.1 s start cost, about 150 s for six restarts, orca route UNVERIFIED); no restart targets a name that is not the duty holder until Coder issue 516 (`ORCH-IronClaude` holds the duties); restart runs before the child and before the item 9 pre-check; session detection UNVERIFIED (U25). The idle end is not adopted and is listed in Section 8.
- **Provenance tag**: `<!-- Source: Variant B, fact 6 (DESIGN line 710; route.py end_finished lines 562-603), with CLAY rebuttal items 3, 4 and 5 and the probe conditions INV-005 and INV-006 - merged per Change 2. The idle end is not adopted. -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (see re-scan note 1)

### Change 3: Per-repo settings keys in the per-repo config (from Variant B)
- **Status**: Applied
- **Source**: Variant B, fact 4; DESIGN lines 879-889; PROBE INV-011; REQ R4
- **Target**: Base, Section 2, new item 8
- **Before**: The base had no per-repo settings keys.
- **After**: Item 8 lists the six keys, fills only readable values, keeps IronFlow and IronOrca values UNVERIFIED, has the coordinator read them at merge time and never the watcher, points merge authority to D06, and adds the INV-011 condition (live GitHub role overrides the safety list and `can_merge`; the safety list changes only on the owner's recorded word).
- **Provenance tag**: `<!-- Source: Variant B, fact 4 (DESIGN lines 879-889), with probe condition INV-011 - merged per Change 3 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 4: Org-wide search as an optional pre-check (from Variant B)
- **Status**: Applied
- **Source**: Variant B, mechanism 1, fact 3; DESIGN line 137; PROBE INV-010
- **Target**: Base, Section 2, new item 9, optional and off in the first build
- **Before**: The base had no org-wide search.
- **After**: Item 9 describes one search per (login, org), skip as `nothing_assigned`, fail-open on a failed search, 100 or more results or a missing field, never skipping a repo with work in flight or a dead coordinator, restart check first, gain about 6 calls per idle repo. Index delay stays UNVERIFIED (U8).
- **Provenance tag**: `<!-- Source: Variant B, mechanism 1 and fact 3 (DESIGN line 137), with probe condition INV-010 - merged per Change 4, marked optional and off in the first build -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Exclusive-create state file per issue and a short-name check (from Variant B)
- **Status**: Applied
- **Source**: Variant B, facts 7 and 8; DESIGN lines 702, 704 (line 708 from Variant B mechanism 4); PROBE INV-009
- **Target**: Base, Section 2, new item 10
- **Before**: The base had create-once claim files only (item 4) and no per-issue state file or short-name check.
- **After**: Item 10 adds the `O_EXCL` per-issue state file beside the claim, keys config, store, approvers file and worktree on `owner/name`, and refuses two repos with one short name. The sentence "there is no `name_collision` skip reason today, so the spec must add one" restates PROBE INV-009 ("OURS has no `name_collision` skip reason") as a requirement.
- **Provenance tag**: `<!-- Source: Variant B, facts 7 and 8 (DESIGN lines 702, 704; line 708 from Variant B mechanism 4), with probe condition INV-009 - merged per Change 5 -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Claim agents never share the standing coordinator's worktree (condition from the probe)
- **Status**: Applied
- **Source**: PROBE INV-004; `launch.py` `launch_argv` lines 136-157; `merged-requirements.md` line 1145
- **Target**: Base, Section 4 (costs) and a condition in Section 2 item 3
- **Before**: Item 3 said only that every project has a `Coordinator` worktree and a running session. No text about claim agents.
- **After**: Item 3 keeps its original facts and adds the condition (separate claim worktree, or the cap stays at 1 until it exists). Section 4 gets a new line "Worktree separation is unbuilt" that calls it a defect in the owner's own plan found by the debate.
- **Provenance tag**: `<!-- Source: Base (original, modified) - item 3 keeps its facts; ... the worktree-separation condition is added (Change 6, INV-004). ... -->` and `<!-- Source: Base (original, modified) - new cost line for the worktree separation condition, per Change 6 ... -->`
- **Deviation from the plan, reported**: the plan says "replace the sentence in Section 2 item 3". The base item 3 holds no sentence about claim agents or the cap, so there was nothing to replace. The base facts were kept and the condition was added after them. The original sentence is otherwise unchanged except for the "(the restart is guarded, see item 7)" pointer (Change 2).
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 7: Prerequisites stated as dependencies, not as "alone" (condition from the probe)
- **Status**: Applied
- **Source**: PROBE INV-012; REQ R6, R9, R10, R20, R21; `launch.py` `GOVERNED_LEVELS_ALLOWED = False`
- **Target**: Base, Section 4
- **Before**: "It has no in-flight cap and no idle end; both are in Clay's 5.7."
- **After**: That line is replaced by "The adopted cap (item 6) and restart (item 7) are rules, not code" (cites the plan's grep of the owner's code and the `COORD-`/`wake`/`terminal`/`resume` grep count 0), plus a new "Prerequisites" line: Coder issue 515, Coder issue 516 (and `worktree_invalid` today, `dispatch.py` 279-280), the branch name decision and a push grant, `GOVERNED_LEVELS_ALLOWED = False`, and a worktree path read from `orca worktree list` instead of the literal `WORKTREES_DIR` (UNVERIFIED beyond the probe's read).
- **Provenance tag**: `<!-- Source: Base (original, modified) - the base line "It has no in-flight cap ..." is replaced per Change 7 (and Change 1 ...) -->` and `<!-- Source: Base (original, modified) - new "Prerequisites" cost line, per Change 7 (PROBE INV-012, HIGH; ...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 8: Make the unresolved name an owner decision (condition from the debate)
- **Status**: Applied
- **Source**: X-005, C-010, Round 2 OURS item (a)
- **Target**: Base, Section 4
- **Before**: "The names are not yet one: the 2026-11-14 branch is `coordinators` ... while REQ R10 and R20 ... name the branch and worktree `Coordinator` ... The spec must pick one."
- **After**: A bullet "The name is an open owner decision, decided in topic D08" keeps the same branch-name facts, adds the one-`COORD-<RepoName>` against Q26 per-scope coordinators point, cites OWNER-ANSWERS line 23 ("direction accepted", naming NOT decided, from the OURS Round 2 rebuttal item (a)), and carries the plan's spec text word for word.
- **Provenance tag**: `<!-- Source: Base (original, modified) - the base line "The names are not yet one ..." is replaced by the open owner decision, per Change 8 (X-005, C-010, Round 2 OURS item (a)) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (see re-scan note 2)

### Plan table "Changes NOT Being Made" and the two named sections
- **Status**: Applied (not a numbered change)
- **Target**: new Section 7 "Adopted from CLAY" (five adopted capabilities and three conditions, with the debate confidences stated in the plan and the rebuttals) and new Section 8 "Rejected from CLAY and why" (all 8 plan rows, plus a column with the CLAY advocate's Round 2 position taken from `round-2-rebuttal-2-CLAY.md` and the plan).
- **Related edit**: Section 6, third bullet, was changed from "ours has not written down: per-issue state file, in-flight count, `wrong_target`, restart and idle end" to the adopted and rejected sets, because the base bullet would otherwise contradict Section 8.
- **Provenance tags**: `<!-- Source: Variant B, positions and Round 2 verdicts ... -->`, `<!-- Source: Refactor plan, "Changes NOT Being Made" table ... -->`, `<!-- Source: Base (original, modified) - the base concession bullet ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1 (line 7) and eight H2 sections numbered 1 to 8 in order; no H3 or deeper, no skipped level.
- Section ordering: PASS. Base sections 1 to 6 keep their order; the two new sections follow as 7 and 8. New mechanism items 6 to 10 follow base items 1 to 5 in Section 2.
- Document flow: PASS. Section 4 now reads: not on origin, layout is a design, open name decision, one launch per sweep, rules without code, prerequisites, worktree separation.
- Provenance: PASS. 4 header comment lines at the top and 23 `<!-- Source: ... -->` tags; every section and significant block carries one. No em dash or en dash in the file (grep count 0).

### Internal References
- Total references: 27, counted by hand from a grep of "item N", "section N" and "Change N" in the file.
- Resolved: 27
- Broken: 0. These are mechanism items 3, 6, 7, 9 and 6 to 10; sections 3, 4, 7 and 8; the table labels "Item 6" to "Item 10"; and "open owner decision above" in Section 4. References to "item 1", "items 3 and 4" and "items 1, 2 and 6" in tags and bullets point to the CLAY rebuttal, and "section 1, item 8" points to the external analysis FULL-REPORT; they were checked against their sources, not against this file.

### Contradiction Re-Scan
- New contradictions introduced: 0.
- Re-scan note 1. Item 3 says a stopped session is "restarted if stopped" (base, REQ R9) and item 7 says the dispatcher restarts only with work in flight and otherwise leaves recreation to the Coder issue 516 boot check. These agree only if 516 provides the boot check. Both say so (item 3 cites 516; item 7 names it), and Section 4 lists 516 as a prerequisite. Not a contradiction, but it depends on 516.
- Re-scan note 2. Base fact 1 says "The owner decided the topology". Section 4 (Change 8) says OWNER-ANSWERS line 23 records the direction as accepted and the naming as NOT decided, and that fact 1 supports a coordinator in every project and nothing more. Fact 1 quotes the same line ("direction accepted"), so the facts agree. The word "decided" in the lead of fact 1 is broader than the evidence; the plan has no change for fact 1, so it was left as the base wrote it and the Section 4 sentence narrows it. Reported for the orchestrator.
- Re-scan note 3. Item 6 default 3 against the item 3 condition (cap 1 until separate worktrees): reconciled by a clause in item 6 (see Change 1).
- Re-scan note 4. Base fact 10 ("Ours ... one coordinator per developer and scope, Q26") against the rejection of extra coordinators in Section 8 (C-004): both are in the base and plan as written; fact 10 describes Q26's person-opened coordinators and Section 8 rejects the poll starting extra ones. Pre-existing, left untouched.

### Items from the evidence the plan did not carry (not applied, by design)
- PROBE INV-007 (a stale claim tree undercounts; a `git fetch` in the check needs its own skip reason) is not in the plan and was not written.
- CLAY rebuttal item 7 (plan requests in the count) is not in the plan and was not written.

## Summary
- Total changes planned: 8
- Successfully applied: 8
- Failed: 0
- Skipped: 0
- Deviations: Change 6 added its condition to item 3 instead of replacing a sentence (no matching sentence existed); Section 6 third bullet adjusted so it does not contradict Section 8; one link clause added to item 6.
- Post-merge validation: PASS
