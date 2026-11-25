# Merge Log (D03)

## Metadata

- Base: Variant 1 (OURS), `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/variant-1-original.md`
- Incorporated from: Variant 2 (CLAY), plus corrections from the Round 2 concessions and the Round 2.5 invariant probe
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/adversarial/refactor-plan.md`
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D03/adversarial/merged-output.md`
- Executor: merge-executor
- Changes applied: 12 of 12 (0 failed, 0 skipped)
- Status: SUCCESS, with the notes under "Deviations and notes"
- Timestamp: 2026-11-20 (UTC)

## Per-change entries

### Change 1: Mandatory sequencing with PR 686 (INV-001, HIGH)
- Status: applied
- Before: Mechanism had 3 steps; Risks bullet 3 said only that PR 686 and the package "cannot both land as written".
- After: Mechanism step 4 added (clean git merge, broken tree: `superclaude --help` crashes, 29 test modules fail at collection; PR 686 must not merge first). New H3 "Precondition: order against PR 686" under "Conditions and sequencing" lists the seven symbols, the three rules (not before the revert is settled; revision or shim; a `superclaude --help` plus import check as merge condition) and says the order belongs to D14. Risks bullet 3 got a pointer.
- Provenance tag: `Source: Refactor plan (invariant probe INV-001, HIGH; Variant 2 fact 6 on removal order) - merged per Change 1`; the Risks bullet is tagged `Base (original, modified)`.
- Validation: step 4 reference resolves; the symbol list matches the plan; the five symbols the probe says the orchestrator re-checked are named as re-checked and the other two are not claimed as checked.

### Change 2: Keep the no `--to` bullet by hand (U-007, INV-002)
- Status: applied
- Before: Mechanism step 1 was a bare `git revert` instruction.
- After: a sub-bullet under step 1 says a bare revert drops the bullet and the assertions at `tests/skills/test_worker_contract.py` lines 426-429 and 3220, tests still pass, re-apply by hand, and the sentence then appears twice (WC-17 line 59 and the bullet) or WC-17 is reworded to point at the bullet.
- Provenance tag: `Base (original) for the main text; Variant 2 (CLAY) U-007 plus INV-002 - merged per Change 2`
- Validation: no conflict with "What it gets right"; line numbers used as stated in the probe.

### Change 3: Creation-time plan sections as an extra layer (U-006, C-003)
- Status: applied
- Before: "What it gets right" had one paragraph.
- After: second paragraph appended: `sc-issue-protocol/SKILL.md:102`, PRs 651 and 661, `Priority`, `Fix approach`, `Test plan` at every depth; independent of the gate; kept as an extra layer, not a replacement (`hold.py` checks headings only, fact 6; the plan at creation is the author's own).
- Provenance tag: `Variant 2 (CLAY), Mechanism 3 and Cited facts 3 - merged per Change 3`
- Validation: "fact 6" resolves to Cited facts item 6.

### Change 4: Cost of the gate and the same-login limit (C-004, C-010, U-009, INV-006)
- Status: applied
- Before: "What it costs" had no gate-cost bullet; the L-1 bullet had no follow-on.
- After: new cost bullet (person-opened coordinator, grant row per issue, two sessions per approval; Q36 "Latency approved for now, approve in coordinator", `owner-answers.md:185`). Two sub-bullets under the L-1 bullet: FU-1 record j (actor `ironbelly`, id 7361222, type `User`), records e and k still block bare, edited and plan-hash-changed approvals; and the INV-006 point (ironbelly only admin, master unprotected, a "by ironbelly" comment can come from an agent, so the ruling is given in the owner's chat and the agent records it, decision D2 text in WORKER-CONTRACT.md).
- Provenance tags: `Variant 2 (CLAY), Cited facts 4` (cost bullet), `Variant 2 (CLAY), Cited facts 3` (record j sub-bullet), `Refactor plan (invariant probe INV-006)` (ruling-channel sub-bullet).
- Validation: L-1 stays an accepted risk citing `owner-answers.md:126`, not hidden. The executor did not re-read the "decision D2" text in WORKER-CONTRACT.md; it is cited as the plan names it.

### Change 5: Removal plan and PR B tests as the bar (U-005, U-008)
- Status: applied
- Before: no conditions section.
- After: H3 "If D01 ends assignment-only" under "Conditions and sequencing": three conditions both advocates accepted; design removal plan (7.2 lines 978-993, 7.3 line 995 onward to about 1004, PR D first at line 1030); PR B test bar at lines 1108-1112 (kill after each `intent` and before `done`; exclusive create refuses a second state file; two orchestrators, one issue, one state file); the watcher lock (`flock`, exit 75, lines 700-712) gives one winner per cycle only.
- Provenance tag: `Variant 2 (CLAY), Mechanism 4, Cited facts 7 and design lines 978-1004 and 1108-1112 - merged per Change 5`
- Validation: "fact 4" and "fact 5" references resolve. "to about line 1004" is the executor's reading of the plan's range 978-1004 (V2 gave 7.3 as "line 995 onward"); the word "about" marks it.

### Change 6: Correct condition 2 (INV-003)
- Status: applied
- Before (debate wording): "R18 default-on config stays blocked by R33 (`GOVERNED_LEVELS_ALLOWED = False`)".
- After: condition 2 reads "R33 must be built before R18 default-on config is built"; states the constant has no hit on master, the three snapshots or the owner branch commits, `requirements.md` row R33 is "decided (not built)", and the only hold today is `cycle.py:228`, `raw.get("enabled", False)`.
- Provenance tag: same block tag as Change 5, naming Change 6 and INV-003.
- Validation: consistent with Cited fact 3 (`enabled: false`).

### Change 7: Correct figures and scope of "never ran live" (X-001, INV-008)
- Status: applied
- Before: fact 3 scope already named the cron watcher; fact 7 said "The branch has 53 changed files"; "What it costs" said about 4,600 lines, about 1,600 source, about 2,900 tests.
- After: fact 3 now states the scope explicitly (cron watcher and the G2 session-id lookup, record f "was not attempted"; not the handoff steps a to k). Fact 7 marks 53 as stale (223 status entries, 70 outside `.dev/`). Cost bullet reads 4,599 lines: 2,969 test lines, 1,618 source lines (package 1,597), 117 test functions (222 collected cases).
- Provenance tags: `Base (original, modified)` on fact 3, fact 7 and the cost bullet.
- Validation: the record f point comes from the V1 concession in the debate transcript, not from the plan text; flagged here. 2,969 + 1,618 = 4,587, not 4,599, so the text states the 12-line gap and says the debate record does not split it, rather than inventing a breakdown.

### Change 8: Installed copies and guard version stamp (INV-004, INV-005)
- Status: applied
- Before: no post-revert host step.
- After: Mechanism step 5: hosts run `superclaude install`; probe's host facts (guard matches neither version, `WORKER-CONTRACT.md` still has WC-17, `/usr/local/bin/superclaude` still lists `issue-pipeline`); stamp stays 1 (line 10, `orca_worktree.py:839,986-987`); raising it needs the independent review; hosts that installed between 00:02Z and the revert are covered by the guard's independent review; risk Medium.
- Provenance tag: `Refactor plan (invariant probe INV-004, INV-005) - merged per Change 8`
- Validation: consistent with the existing "What it costs" bullet on the guard's independent review.

### Change 9: Amend R1 and section 7 of the design (INV-011)
- Status: applied
- Before: no design step.
- After: Mechanism step 6: the design is not reverted and says the opposite (`orchestrator.md` lines 73, 987-991, 997-1004, 1017, 1095, 1381); the revert PR or a named follow-up amends R1 and section 7; the D03 verdict names which.
- Provenance tag: `Refactor plan (invariant probe INV-011) - merged per Change 9`
- Validation: consistent with Cited fact 6 (R1 at line 73).

### Change 10: CHANGELOG conflict (INV-007)
- Status: applied
- Before: step 2 said the conflicts are textual and small; "What it costs" said a conflict fix in three files.
- After: step 2 says only `CHANGELOG.md` is a textual conflict (`git merge-tree --write-tree --merge-base=01e7a9e23 origin/master 01e7a9e23^`), the other two files merge on their own, and the "Removed: the old plan-approval gate" entry is dropped or reworded. The cost bullet now says one file. The "3 of 36 files changed afterwards" fact is kept.
- Provenance tags: `Base (original, modified) - conflict scope corrected per Change 10` on step 2 and on the cost bullet.
- Validation: the cost bullet edit is a dependent correction (see notes); no remaining "three files" in body text.

### Change 11: Process facts
- Status: applied
- Before: fact 2 had the 66 minutes, one review and one comment.
- After: adds PR 681 merged 2026-11-20T00:02:33Z and PR 682 at 00:02:36Z, both by `clayphi`, 3 seconds apart; marks the `augmentcode` review as automated; adds Clay's issue 450 question (2026-11-18 17:00:32, to `@ironbelly`, "What do you think?") with no reply, which is not consent.
- Provenance tag: `Base (original, modified) - process facts added per Change 11`, noting the issue 450 detail is from Variant 2 fact 2.
- Validation: the 66-minute figure is unchanged (22:56:28Z to 00:02:36Z). Kept the base's "one comment by `chatgpt-codex-connector`". PR 681's 8 reviews (V2 rebuttal) were not added because the plan does not list them.

### Change 12: Unresolved and unverified section
- Status: applied
- Before: no such section.
- After: new H2 with eight bullets: the `test_the_watcher_record_module_is_not_edited` result (UNVERIFIED), D01 as the end-state decision and the two split diff points C-004 and C-008, identity of "the owner" (UNVERIFIED), untracked `complete.py` and tests not checked, owner branch rebase not run and the R-row naming mismatch, INV-013 behaviour against PR 686 (UNVERIFIED), full suite and `test_launch_level_guard.py` unfinished (UNVERIFIED), "assignment is safe" in issue 655 (UNVERIFIED).
- Provenance tag: `Refactor plan (Change 12; invariant probe INV-008, INV-009, INV-010, INV-013; debate transcript Rounds 1 and 2)`
- Validation: items beyond the plan's five come from the probe and the debate transcript, and each carries its source (INV-010 and INV-013, Round 1 and 2 UNVERIFIED items).

## Deviations and notes

1. Cross-reference sentences were added to keep the document consistent; none adds a new fact: a scope pointer in "Claim" (revert is the default until D01 rules, see "Conditions and sequencing"), a pointer in the first Risks bullet, and the PR 686 failure-mode pointer in the third Risks bullet. They are tagged `Base (original, modified)`.
2. The cost bullet "conflict fix in three files" was corrected to one file as a dependent edit of Change 10, since leaving it would contradict step 2.
3. Provenance tags: V2-sourced blocks use the `Variant 2 (CLAY)` form. Blocks sourced from the plan or the probe use `Refactor plan (...)`, because calling them `Base` or `Variant 2` would misstate the source. This is a fourth tag form beyond the three the task named.
4. The title was changed from "Position paper OURS" to "Unified position", tagged as modified.
5. "Changes NOT Being Made" (5 rows) were respected: no V2 "keep PR 682" end state (only the conditional under D01), no C-003 replacement, no F14 benefit claim, no rebuild of the old behaviour inside PR 686.
6. One mid-write retry: the first full write was blocked by the freshness hook until the stub was read; no content was lost.

## Post-merge validation

### Structural
- Headings: one H1; H2 sections in order Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right (and what Clay's side gets right), Conditions and sequencing, Unresolved and unverified; two H3 sections, both under "Conditions and sequencing". No level gaps. PASS.
- Base sections: all six kept in base order; the two new sections follow at the end. PASS.
- Provenance: header block present (Provenance, Base, merge date 2026-11-20, plan); 36 `Source:` tags cover every section and block. PASS.
- Dashes: no em dashes or en dashes in the merged output. PASS.

### References
- "fact 4", "fact 5", "fact 6", "fact 7" resolve to Cited facts items 4 to 7 (items 1 to 9 exist). PASS.
- "Mechanism step 4" resolves to step 4. "Conditions and sequencing" and "What it risks" resolve to existing H2 headings. PASS.
- Change numbers appear only in the HTML tags, each matching a change in the plan. PASS.
- Decision, row and PR identifiers (decisions 2, 3, 6, 8; Q35 to Q41; R1, R18, R33; PRs 584, 591, 651, 661, 681, 682, 683, 686) were carried from the base, the plan or the transcript; none was added from outside them. PASS.

### Contradiction rescan
- "Never ran live" scope: fact 3 limits it to the cron watcher and the G2 lookup; no other section widens it; "What it costs" ("no production caller until the watcher is enabled") and the Unresolved section agree. PASS.
- Counts: 36 files and 3 later-changed files (step 2); one conflicting file (step 2, step 4, Conditions, cost bullet, Risks bullet 3 all say CHANGELOG.md only); 4,599 lines with the 12-line gap stated; 117 functions and 222 cases; 11 RECORDED lines; 53 versus 223 marked stale in fact 7 and the Unresolved section. One fix during rescan: Risks bullet 3 originally said "without a conflict" and now says "no conflict beyond `CHANGELOG.md`", to match step 4. PASS after the fix.
- Wording fix during rescan: "this host" in the INV-006 sub-bullet changed to "the fault-finder's host" so it matches step 5.
- Claim versus conditions: the Claim is a default pending D01, and the Risks and Conditions sections say the same. PASS.
- Step 3 says the owner branch "rebases" onto the reverted master; the Unresolved section says the rebase was not run and that only the tracked part passes `git apply --check`. Treated as a qualified expectation, not a conflict. PASS with note.
- No new contradiction found.

## Summary

| Measure | Count |
|---------|-------|
| Planned | 12 |
| Applied | 12 |
| Failed | 0 |
| Skipped | 0 |
| Plan rows left unmade (by plan) | 5 |
| Dependent or cross-reference edits outside the 12 | 4 (see notes 1 and 2) |
