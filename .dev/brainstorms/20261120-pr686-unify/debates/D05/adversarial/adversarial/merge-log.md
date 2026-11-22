# Merge Log (Step 5): D05 merged position

## Metadata

- Base: Variant 2 (CLAY), `variant-2-original.md`
- Non-base: Variant 1 (OURS), `variant-1-original.md`
- Plan: `refactor-plan.md` (9 planned changes, 4 rejected diff points)
- Executor: merge-executor (Step 5 of /sc:adversarial, Mode A, debate D05)
- Changes applied: 9 of 9, in plan order
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D05/adversarial/merged-output.md`
- Status: COMPLETE (all post-merge checks pass; two wording fixes made during validation, see Post-Merge Validation)
- Timestamp: 2026-11-20T04:51:09Z

Layout note. The merged output uses the seven H2 sections the brief fixed (Question, Merged position, Evidence both lines agree on, Where the lines differ and how the debate settled each point, Controls and what each one covers, Guard G2 rule 1 that PR 682 removed, Open items). The base's own sections (Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right) were regrouped into them. So each "Target in base" below names where the base text now sits.

## Changes Applied

### Change #1: restate the owner's G1 acceptance exactly

- Status: APPLIED
- Before: base cited fact 1 said DQ7 "adds no new exposure that the owner's own text did not already describe".
- After: section Evidence both lines agree on, block "What the owner accepted": the D:117 sentence and the G2 sentence (`issue-pipeline-guard-g2.md:9`) are quoted: accepted "for the one first test issue"; "Before any other issue runs through the flow, the worker must be bound to the guard (G2)". The "no new exposure" sentence is quoted only to say it does not stand (base-selection.md, Correctness 1). The LD:23 quote of base fact 1 is kept in block "What the guard governs today". Merged position, "Should the guard be required", states the "before any other issue" clause.
- Provenance tag: `Variant 1 (OURS), fact 2 - merged per Change #1`
- Validation: quotes match variant-1-original.md fact 2 and round-1-advocate-1.md strength 2. C-007 OURS 78% matches the Scoring Matrix.

### Change #2: FS equals OD1; three prohibitions enforced by PUSHFORM, PROTECTED, MERGE

- Status: APPLIED
- Before: base Mechanism had items 1 to 4 and no mention of FS.
- After: new item 3a placed directly after item 3 in "How the design bounds an orchestrated worker today": FS is Clay's OD1 policy word for word; PUSHFORM (LD:113), PROTECTED (LD:114), MERGE (LD:115); FS allows (LD:25-30, grid LD:91-98). Notes that the FS-to-OD1 mapping is unwritten (C-009).
- Provenance tag: `Variant 1 (OURS), Mechanism 3 - merged per Change #2`
- Validation: matches variant-1-original.md Mechanism 3. C-009 OURS 67% matches the Scoring Matrix.

### Change #3: the audit takes `--pr <N>`, so a direct push to `master` has nothing to audit

- Status: APPLIED
- Before: base fact 7 said the design has controls the guard lacks and stated their tests.
- After: Controls, control 5 (audit): "Does not stop" names the `--pr <N>` limit and that no CLAY control acts on a worker push (conceded in full by the CLAY advocate, R2A2 response 7). Repeated in controls 3 and 4 and in the agreed-evidence block.
- Provenance tag: `Variant 1 (OURS), fact 5 - merged per Change #3` (plus the Round 2 confirmations named in the tag)
- Validation: matches variant-1-original.md fact 5, R2A1 "Updated assessment of Variant 2", R2A2 response 7. C-005 lean OURS 63% matches.

### Change #4: K22 and U42 precedent with the correction

- Status: APPLIED
- Before: base "What it risks" first bullet said the `refuse` list binds the orchestrator's verbs, "not a command the model types itself" (K22); U42 open.
- After: Controls, control 3 keeps that bullet and adds: a session-scoped hook exists (marker plus pending record, LD:75-77; OB-CTX PASS, results lines 553-563); it answers the feasibility half of U42 by precedent only; the guard blocks MERGE at every level (LD:115) so it cannot bind the orchestrator; it does not answer K22; U-002 shrinks from "already built" to "precedent".
- Provenance tag: `Variant 1 (OURS), fact 4 - merged per Change #4, as corrected by both Round 2 files`
- Validation: matches R2A1 response 4 and R2A2 response 4. C-010 SPLIT 60% matches.

### Change #5: live evidence for the guard's grid; OB-H2 FAIL rows are verbatim-detail checks

- Status: APPLIED
- Before: base fact 2 listed only the FAILs and the "not runtime-approved" status line.
- After: section Evidence, block "How proven the guard is": the PASS list (implement blocked, four commit blocks, merge block, OB-CTX, with line numbers) beside the FAIL list; the OB-H2 FAIL rows are quoted as verbatim-detail checks (lines 471-472); the item 8 correction (issue 678 parked by the owner, per base-selection.md and R2A2 response 6) is added so the base's FAIL list does not overstate. Also Controls, control 1, "Seen live".
- Provenance tag: `Variant 1 (OURS), fact 6` and `fact 7 - merged per Change #5`
- Validation: line numbers match R1A1 strengths 6 and 7 (530, 531, 532, 535, 536, 549, 553-563, 471-472, 470). C-003 SPLIT 61% and X-002 OURS 67% match. The item 8 correction is an addition beyond the plan sentence; it is taken from base-selection.md (Correctness 1) and R2A2, and is flagged here for the orchestrator.

### Change #6: binding facts

- Status: APPLIED
- Before: base fact 6 said binding was never observed, G2 facts 1 to 4 UNVERIFIED, FU-1 precondition f not tried.
- After: section Evidence, block "Binding a `worker-start` worker: what is known and what is not": the base's first two sentences are kept; added: `publish_pending` at `orca_worktree.py:1488`, `cmd_pending` at `:1515`; the marker slot deleted with `brief.py` and `worker-brief.txt`; `cmd_pending` runs no preflight (comment at `:1726`); binding fails closed with LL-NOBIND (`:367`, `:384`); the receipt (`pending/<nonce>` gone, `:373-375`); the G2 collisions and `.ok` release apply only at level W (`:270`, `:341-343`, LD grid row 34); rule 2 is in the guard and tested; the marker is accepted anywhere and the claim path's delivery is live; the degraded-W case (`:268-271`, B12). UNVERIFIED marks kept: `worker-start` delivery of the marker as a hook event; FU-1 precondition f; G2 facts 1 to 4.
- Provenance tag: `Debate, rounds/round-2-advocate-1.md - merged per Change #6` and `rounds/round-2-advocate-2.md - merged per Change #6`
- Validation: every line number was re-read from R2A1 and R2A2 text. C-002 unresolved lean CLAY 55% and X-001 CLAY 67% match. Risk Medium as planned: many citations; none was added from outside the named files.

### Change #7: invariant-probe limits in plain words

- Status: APPLIED
- Before: no such section in the base.
- After: Controls and what each one covers, H3 "Limits found by the invariant probe": seven items. (1) FS covers K12 only for plain pushes to `master` and `main` and does not close it (INV-035); (2) a script run passes every gate (INV-034); (3) `integration` or another default branch passes (INV-019); (4) a new session id runs unbound while the receipt reads clean (INV-003); (5) "second real issue" cannot be counted (INV-015); (6) K12 closed only by a push-time control outside the worker (INV-037); (7) three gates disagree (INV-027). The 12 MEDIUM and 6 LOW findings are listed in Open items, item 12. UNVERIFIED list kept in Open items, item 13.
- Provenance tag: `Debate, invariant-probe.md - merged per Change #7`
- Validation: the 7 HIGH IDs match the probe summary (INV-003, 015, 019, 027, 034, 035, 037). The MEDIUM list has 12 IDs and the LOW list 6, matching the probe summary. Line citations (`guard.sh:257, :391, :720, :733-735, :787`) are the probe's own.

### Change #8: fix the ambiguous word "owner"

- Status: APPLIED
- Before: base Claim and fact 8 said the risk is "left for the owner (DQ7 and K12, decision OD1)" and that OD1 is "Decided by ruling 3"; "owner" named two people.
- After: the short-name list defines "the owner" as `ironbelly` and "Clay" as `clayphi`. Section Evidence, block "Who the owner is": "the owner (Clay)" in D:3 and "owner" in D:1152 mean `clayphi`; the analyst map shows the rulings came from `clayphi` and `ironbelly` left nothing; the G2 sentence came in PR 591 by `ironbelly`; D:1397 omits the guard; D:970 and D:975 leave binding open. The base's record-the-risk point (K12 graded, OD1 decided, D:970) is kept inside that block. Open items, item 3 holds the wording rule.
- Provenance tag: `Debate, rounds/round-2-advocate-1.md - merged per Change #8` and `rounds/round-2-advocate-2.md`
- Validation: matches R2A1 response 7 and R2A2 response 7. UNVERIFIED mark kept (`RULINGS.md` not read).

### Change #9: narrow the friction finding

- Status: APPLIED
- Before: base fact 5 said the guard and the pull-request workflow rub against each other (GHWRITE, scripts through a leak, compound pushes refused, one command re-issued in split form).
- After: Controls, control 1, bullet "Friction at FS": reply and resolve run in scripts (`reply-resolve-thread.sh:131`, `:141`) and work through the pinned leak (LD:122); the summary-thread and fallback comments are inline `gh api` POST (`refs/thread-reply.md:87-89`, `:93-100`), GHWRITE at FS (`:554`, `:67-69`); the worker must use `gh pr comment`; the merge cycle is off by default (`--conflict-max-tier` 0, `SKILL.md:240`); a bare `/sc:pr-submit --monitor 3` cycle at FS has never been observed. Closes with "Small, fixable, not a veto".
- Provenance tag: `Debate, rounds/round-2-advocate-2.md - response 5 - merged per Change #9`
- Validation: matches R2A2 response 5 and R2A1 response 5. C-006 lean CLAY narrow 55% matches.

### Changes NOT being made (honoured)

| Diff point | How it was honoured in the merged output |
|---|---|
| X-003 | Block "What the guard governs today" says "the guard governs every launch" states the rule that should hold, not the state of master. The OURS Claim is not stated as a fact anywhere. Listed under "Rejected carry-overs". |
| C-004 | Same block: R33 gates only the watcher's claim launches (`launch.py:48`); both advocates agree it does not forbid binding a `worker-start` worker. |
| C-001 | Merged position says "staged and not exempted". The CLAY claim "the design must not make workers wait for the guard" appears only in "Rejected carry-overs". |
| C-008 | Control 7 and Open items, item 4 record the server-side rule as an open owner action with the live value `protected: false`; the merge makes no recommendation. |

## Post-Merge Validation

### Structural integrity

- PASS. The file starts with the three provenance comments, then one H1, then H2 sections in the required order: Question, Merged position, Evidence both lines agree on, Where the lines differ and how the debate settled each point, Controls and what each one covers, Guard G2 rule 1 that PR 682 removed, Open items. Checked with a heading grep (lines 5 to 307).
- No heading level gaps: H1 then H2 then H3 only; no H4 or deeper.
- The Question text is verbatim from the brief.
- The table in "Where the lines differ" has all 17 scored points (S-001, S-002, C-001 to C-010, X-001 to X-003, A-001, A-002) with winner and confidence equal to the Scoring Matrix; the tally line adds up to 17 (4 OURS, 2 CLAY, 3 unresolved, 8 SPLIT).
- The three header comments are lines 1 to 3. The merged file has 57 provenance tags (Source lines). No stub text remains.
- No em dashes or en dashes in the file (grep count 0).

### Internal references

- PASS after one fix. Every "see the section X" reference points to an existing heading or a named block: Open items items 1, 2, 4, 7, 8 (items 1 to 13 exist); Controls control 1 "Friction at FS" and control 3; "Limits found by the invariant probe"; blocks "What the guard governs today", "What the owner accepted", "Who the owner is", "How proven the guard is", and "Binding a `worker-start` worker: what is known and what is not"; the section "Guard G2 rule 1 that PR 682 removed".
- Fix made: the heading `Who "the owner" is` was renamed `Who the owner is` so the table references match; and "see the first block of this section" was replaced by a named block reference.

### Contradictions

- No new contradiction found. Checks made:
  - "Required" versus "not required". The merged position says the guard is required as the rule that should hold, staged and not exempted. The base's opposite claim ("must not make workers wait") appears only inside "Rejected carry-overs" and the C-001 row, each marked as not adopted. A grep for "exempt", "not required", "must not make" found only those places.
  - "Closes K12". The first draft of Limits item 1 said binding "closes K12 only for plain pushes", which could clash with "only a push-time control outside the worker closes K12" (Merged position, Limits item 6). Fixed to "covers K12 only for plain pushes ... it does not close K12".
  - OB-H1 item 8. The base listed it as a FAIL against the guard; the merged text says it is real but parked by the owner and counts for nothing beyond staging. Both statements sit in one block and agree.
  - Staging versus the owner's "before any other issue". Both are stated and the conflict is placed in Open items, item 1 as an owner decision, not hidden.
- Tensions that come from the sources and were recorded, not created by the merge: Clay's design says "This is a risk and not a question" (D:117) while D:970 and D:975 leave binding open (Evidence, Open items item 3); the three gates disagree (INV-027, Open items item 2).

### Fact trace

- Every fact traces to a file named in a provenance tag: `variant-2-original.md`, `variant-1-original.md`, `debate-transcript.md`, `diff-analysis.md`, `invariant-probe.md`, `base-selection.md`, `rounds/round-2-advocate-1.md`, `rounds/round-2-advocate-2.md`, and `docs/designs/orchestrator.md` section 7.3 (D:995-1004; read directly from the snapshot). The Round 1 advocate lines (transcript) supplied the results line numbers (530 to 563, 471-472, 470, 17).
- UNVERIFIED marks kept: `worker-start` delivery of the marker as a hook event; hook timeout behaviour; new session id on `/clear` or resume; the worker's HOME, PATH, MCP set and host OS; `launch.py:48` (not in the snapshot per the probe); which issue G1 covered; `RULINGS.md`; map rows 5.9 and 5.11 and E-pr682.md (not opened by the CLAY advocate); G2 facts 1 to 4; FU-1 precondition f; whether a ruleset can be created by the orchestrator's login.
- Not independently re-read by this executor: the observation results file (`observation-results.md`), the guard source and `orca_worktree.py`. Their line numbers come from the advocates' and the probe's re-reads, as the brief allowed.
- Choices to flag: (a) the equation of PR D (the design's name) with the change PR 682 made rests on V2 fact 9, which cites D:1004 for the PR 682 review; the merged text keeps both names and defines PR D as the design's own name. (b) Open items 1, 5 and 8 and the staging gate are proposals made by the advocates; the text says so and does not present them as owner decisions.

## Summary

- Planned changes: 9
- Applied: 9
- Failed: 0
- Skipped: 0
- Rejected diff points honoured: 4 of 4 (X-003, C-004, C-001, C-008)
- Validation: structural PASS, references PASS (one heading and one reference fixed), contradictions none new (one wording fixed)
- Escalations: none required. One addition beyond the plan sentence (the item 8 correction in Change #5) and one inference (PR D equals the change in PR 682) are flagged above for the orchestrator.

