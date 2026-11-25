# Merge Execution Log

## Metadata
- Base: Variant 1 (OURS, `variant-1-original.md`)
- Executor: merge-executor agent
- Changes applied: 6 of 6 planned
- Status: success
- Timestamp: 2026-11-20T09:13:28Z
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/adversarial/adversarial/refactor-plan.md`
- Merged output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG1/adversarial/merged-qg1-position.md`
- Base bytes: the merged file keeps every base line that no change touches. A line-set comparison against the base shows exactly 7 base lines replaced (Claim 1, Claim 3, Mechanism bullets 3 and 4, Cited facts 2 and 4, first Costs bullet). Nothing else in the base differs, apart from the added provenance comment lines and the new section.

## Changes Applied

### Change 1: Add the hand-back loop bounds, old-worker-final rule and idempotent re-plan
- **Status**: Applied
- **Source**: Variant 2, Mechanism bullets 3-4 and Cited facts 6-8 (design lines 612-614, 620, 1078-1081)
- **Target**: Base, new section "Loop bounds under any start rule", inserted after "Mechanism" (insert)
- **Before**: Section did not exist. The base named `HANDBACK_MAX` = 3 only in Cited fact 9 and "What it costs" and had no loop mechanics.
- **After**: New H2 with a one-line lead and four bullets: (a) `handback` decides in the order `no_remaining`, `cap` (`HANDBACK_MAX` = 3, at most 4 rounds, "this design's value, not measured"), `no_progress`; (b) round n+1 starts only when the old worker's `worker_done` was received for the active Task and Dispatch, with the quote "absence never authorizes a release or a second worker"; (c) the re-plan marker `<!-- sc:issue:replan round=<n> -->` makes a rerun write nothing twice, and `--remaining` replaces only `## Fix approach` and `## Test plan`, with done-item fidelity marked UNVERIFIED (U60, design line 1081); (d) every step is read-then-write and a restart resumes at the recorded step (design line 620).
- **Provenance tag**: `<!-- Source: Variant 2, Mechanism bullets 3-4 and Cited facts 6-8 (design lines 612-614, 620, 1078-1081) - merged per Change #1 (new section) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Checked against the design snapshot** (`/home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator.md`): line 612 gives the order (1) `no_remaining`, (2) `cap`, (3) `no_progress` and "this design's value, not measured"; line 614 has the `worker_done` rule and the quoted sentence; line 620 has the restart rule; lines 1078-1080 have the marker and the two replaced sections; line 1081 has U60.

### Change 2: Keep `quick` as the default but add the per-repo `plan_depth` override
- **Status**: Applied
- **Source**: Variant 2, Claim 1 and Mechanism bullet 1 (design lines 60, 722-724; cost cascade from line 618)
- **Target**: Base, Claim 1 (extend) and "What it costs" (replace the G6 sentence, append one bullet)
- **Before**: Claim 1: "the default `plan_depth` is `quick` (...)". First cost bullet: "`quick` runs the cheapest planner, the opposite of Clay's goal G6 (...)." No cost line for a stronger setting.
- **After**: Claim 1 keeps its sentence and adds that a repo may opt in to `standard` or `deep` with a per-repo `plan_depth`, a plain key passed straight to `--depth`, with no tier-to-depth table. The G6 cost bullet now ends with "A repo can set a higher `plan_depth` to get that lever back, so G6 is kept as an option and not as the default." A new last cost bullet says a repo set to `deep` runs the most expensive planner up to 4 times per issue because the wave-2 re-plan passes the same depth (design line 618), and that no cost baseline exists (D12).
- **Provenance tag**: `<!-- Source: Variant 2, Claim 1 and Mechanism bullet 1 (design lines 60, 722-724) - merged per Change #2 -->` (Claim section) and `<!-- Source: Base (original, modified) - first bullet replaced and last bullet appended per Change #2 (from Variant 2, goal G6 and design lines 60, 618); ... -->` (costs section)
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Note**: the plan says "replace one sentence". The Claim 1 sentence is kept and one sentence is added after it, so no base text is lost. The costs sentence is replaced as planned (the original text is kept and a second sentence follows it).

### Change 3: Add the start re-check requirement
- **Status**: Applied
- **Source**: Variant 2, Cited fact 9 (D01 MR-1; `orchestrator.md:488`)
- **Target**: Base, Mechanism bullet 3 (append)
- **Before**: Bullet 3 ended after the "the plan must exist before the approval" quote.
- **After**: Two sentences appended: the check at the moment of start must repeat the approval, not only `hold:backlog` and `plan_check` (D01 VERDICT item 3, MR-1; Clay's wave-1 re-check at design line 488 covers only those two), and a test statement: remove the approval between the wake and the start; the start must be refused.
- **Provenance tag**: `<!-- Source: Base (original, modified) - bullet 3 path corrected per Change #4 and extended per Change #3 (from Variant 2, Cited fact 9, D01 MR-1); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Checked**: design line 488 reads that the live re-check at the start of wave 1 covers `hold:backlog` and "a check that no longer passes", which matches the plan's statement.

### Change 4: Correct the base's wrong or loose citations
- **Status**: Applied (with one extension, see Notes)
- **Source**: Orchestrator spot-check in `base-selection.md` (Correctness, V1) and the reviewer note in `diff-analysis.md`
- **Target**: Base, Cited facts 2 and 4 (and the same wrong path in Mechanism bullet 3, see Notes)
- **Before**: Fact 2 gave D12 item 6 as a plain fact. Fact 4 cited bare `predicates.py:249-259`. Mechanism bullet 3 cited `pr-a/src/superclaude/cli/issue_watch/predicates.py:249-259`, a file that has 219 lines in the `pr-a` snapshot.
- **After**: Fact 2 is re-labelled "Related cost-baseline deferral at create time, not a direct source for OD-1 (the direct source is fact 3)" and keeps the D12 quote. Fact 4 cites `src/superclaude/cli/issue_watch/predicates.py:249-259` in snapshot master (full snapshot path given), names the function `unchanged_since` returning `edited_after_approval`, and says the `pr-a` copy has 219 lines and does not hold this code. Mechanism bullet 3 now cites the same master path.
- **Provenance tag**: `<!-- Source: Base (original, modified) - Fact 2 re-labelled and Fact 4 path corrected per Change #4 (...) -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Checked**: in `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/predicates.py`, function `unchanged_since` starts at line 237; lines 249-259 hold the timestamp collection and `return "edited_after_approval"`.
- **Notes**: the plan names facts 2 and 4 only. The same wrong `pr-a/` path sits in Mechanism bullet 3. Correcting only fact 4 would have made the merged paper cite two different files for one rule, a contradiction created by the merge, so the path in bullet 3 was corrected too. The orchestrator may revert that one path if it wants the plan taken literally.

### Change 5: Say how a waiting hand-back leaves the in-flight count, with its limits
- **Status**: Applied
- **Source**: Debate transcript, both advocates' proposal (status `escalated`, step `handback_awaiting_approval(body_sha)`), checked against `route.py:393-399`, design lines 605 and 608
- **Target**: Base, Claim 3 and Mechanism bullet 4 (replace and extend)
- **Before**: Claim 3 said the waiting issue is not counted, without a carrier. Bullet 4 ended with "A waiting step modeled as not-in-progress follows the same principle: only live work holds a place."
- **After**: Claim 3 adds the carrier (state file status `escalated`, step `handback_awaiting_approval(body_sha)`) and marks it UNVERIFIED as to side effects. Bullet 4 replaces the last sentence with the concrete carrier, adds that `route.in_flight` skips any readable file whose status is not `in_progress` (`route.py:399`) so the file is not counted and counts again when set back to `in_progress`, and cites design lines 605 and 608. Four open points, each marked UNVERIFIED: (1) design line 616 says "Nothing is escalated for a hand-back", so `escalated` is an extension whose row-9, `stalled` and `--take` side effects (design lines 608 and 617) are not checked; (2) the flip back can overshoot `max_in_flight` (allow a one-slot overshoot, or require a free place; undecided); (3) which component runs the wake path (C-INV-2) is not decided, and the poll does not (`cycle.py:993-994`); (4) whether the restored WC-17 flow can serve as the round-2 gate (Cited fact 6) is not known.
- **Provenance tag**: `<!-- Source: Base (original, modified) - ... bullet 4 replaced and extended per Change #5 (from the debate transcript, checked against route.py:399 and design lines 605, 608, 616, 617); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (one watch item, see Contradiction Re-Scan)
- **Checked**: `route.py:399` in the `pr-a` snapshot reads `if sf.readable and sf.status != "in_progress":`; `cycle.py:994` holds the `return None  # already woken, acknowledged or abandoned: never woken again`; design line 605 sets `escalated` "so the issue leaves the places in flight"; line 608 keeps today's behaviour (entry `stalled` when the orchestrator is down, `--take` refuses it) for an `escalated` file waiting mid-work for a person; line 616 reads "Nothing is escalated for a hand-back".

### Change 6: Record the shared assumptions and the Clay concessions that the debate surfaced
- **Status**: Applied
- **Source**: Diff analysis A-001 to A-004; debate transcript concessions
- **Target**: Base, "What it risks" (append)
- **Before**: Three risk lines, none with a stated impact and only one with a mitigation.
- **After**: Four lines appended, each with an impact and one mitigation: A-001 (no measurement of plan quality or cost per depth), A-002 (hand-backs assumed rare, `HANDBACK_MAX` unmeasured), A-003 (login-based approval weak against an agent on the same login, accepted risk L-1), A-004 (counting code lives in PR 686 whose adaptation is open; `route.py` survival UNVERIFIED).
- **Provenance tag**: `<!-- Source: Base (original, modified) - four risk lines appended per Change #6 (from diff-analysis.md A-001 to A-004 and the debate transcript); ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS
- **Notes**: the plan's integration point asks for four risk lines, so the Clay concessions from the debate (no round-2 approval in Clay's text, no evidence for `deep`) were not added as separate text; they are already carried by the "Changes NOT Being Made" reasoning and by Claim 1 and Claim 2. In the A-003 line the citation `orchestrator.md:111` from the diff analysis was replaced by "ruling 11, design lines 111 and 488" after reading both lines: line 111 states the own-login rule (ruling 11) and line 488 states that the orchestrator and Clay share the login.

## Other edits outside the six changes (all minor, listed so the orchestrator can reverse them)
1. Plan references of the form `D:nnn` were written as "design line N" (or "design lines N-M"), the style the base already uses ("design line 60", "Design `docs/designs/orchestrator.md:616`"). The form `D:nnn` is not defined in the base and could be confused with the debate ids D12 and D15.
2. The provenance tags use a plain hyphen where the template's Section 6 example shows an em dash, because the task forbids em dashes. The log uses PASS and FAIL where the template shows check marks, for the same reason (no emojis).
3. Cited fact 4 also says the `pr-a` copy of `predicates.py` has 219 lines (from the orchestrator spot-check in `base-selection.md`).

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1 (line 6) followed by seven H2 (Claim 12, Mechanism 19, Loop bounds under any start rule 31, Cited facts 41, What it costs 54, What it risks 62, What it gets right 73). No level is skipped. The document starts with an H1 (after three provenance comment lines).
- Section ordering: PASS. Base order is kept (Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right); the new section sits directly after Mechanism as the plan says.
- Document flow: PASS. The new section reads as a continuation of Mechanism (it states the loop rules that hold whatever the start rule is) and the Costs and Risks sections do not depend on it.
- Provenance: PASS. 9 source tags (the Claim section has two) plus the 3-line header. Every H2 and the H1 block carries a `<!-- Source: ... -->` tag; sections that mix base and merged text say which bullets or lines changed and under which Change number.
- OD answers kept separate: PASS. Each question still has its own answer, reason and source in the merged paper.

| Question | Answer | Reason | Source |
|----------|--------|--------|--------|
| OD-1 | Claim 1: `quick` default, per-repo `plan_depth` allowed | Mechanism bullets 1-2 (plan call, `plan_check` proves presence only, approval is the quality gate); Costs bullets 1 and 4 | Cited facts 1, 2 (related only), 3 |
| OD-2 | Claim 2: re-plan then person re-applies the approval, no separate chat go | Mechanism bullet 3 (body edit voids approval, start re-check repeats it, test statement); Loop bounds section | Cited facts 4, 5, 6 |
| OD-13 | Claim 3: waiting step not counted, carried by `escalated` plus `handback_awaiting_approval`, visible reason, expiry later | Mechanism bullet 4 and its four UNVERIFIED open points | Cited facts 7, 8, 9 |

### Internal References
- Total references: 10
- Resolved: 10
- Broken: 0

References counted: (1) Claim 3 to "the fourth Mechanism bullet"; (2) Mechanism bullet 4 to "Cited fact 6"; (3) Cited fact 2 to "fact 3"; (4) Cited fact 8 to C-INV-1, defined in Cited fact 7; (5) Costs bullet 2 "Option (a)" to Claim 2; (6) Risks A-001 line to OD-1 (Claim 1); (7) Risks A-002 line to OD-13 (Claim 3); (8) Risks A-003 line to OD-2 option (a) (Claim 2); (9) Risks A-004 line to OD-13 (Claim 3); (10) Risks A-004 line to "the fourth Mechanism bullet". The Mechanism section has exactly four bullets, so "fourth" is bullet 4.

External identifiers (D01, D12, D14, D15, WC-17, C-INV-2, L-1, U60, A-001 to A-004, R19, R22, G6) are not internal references and are not counted. Code and design citations read from the snapshots during this merge: `predicates.py:249-259` (master), `route.py:399` and `cycle.py:994` (`pr-a`), design lines 60, 111, 488, 605, 608, 612, 614, 616, 617, 618, 620 and 1078-1081. Not re-read: design lines 722-724 (named only in a provenance tag), `route.py:379-426`, `hold.py:122-143` and the verdict files (all carried over unchanged from the base).

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: none found. Two watch items, neither a contradiction:
  1. "What it gets right" (base, untouched) says the paper "does not invent a second mechanism (no `handback_awaiting_go`, no `answer-check` per round)", while Change 5 names a new state step `handback_awaiting_approval`. These differ: the removed items are a separate chat go and a per-round answer check, while the new step is only the state label for waiting on the same start gate. The wording was left as the base has it.
  2. Cited fact 1 quotes the D15 OD-1 row, which gives "(D12 deferral)" as its reason for `quick`, while the re-labelled fact 2 says D12 item 6 is not a direct source for OD-1. The quote is the D15 row's own reason and is kept as a quote; fact 2 only says that the D12 text is about create-time tier floors.
- Checked pairs: Claim 2 (no chat go) against the Change 3 test statement (approval re-checked at start): consistent. Claim 3 (not counted) against Cited fact 8 (place never freed, a defect): consistent. Loop bounds "at most 4 rounds" against Costs "capped at 4" and "up to 4 times": consistent. Mechanism bullet 3 (master path) against fact 4 (master path): consistent after the path fix. Mechanism bullet 4 (`pr-a` `route.py`) against Risks A-004 (`pr-a` snapshot): consistent. Design line 616 ("Nothing is escalated for a hand-back") against the use of `escalated`: stated openly as an extension and as UNVERIFIED.
- Dashes and emojis: 0 em dashes and no emoji in the merged file (checked by search).

## Summary
- Total changes planned: 6
- Successfully applied: 6
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Open for the orchestrator: (1) the extension of Change 4 to the same wrong path in Mechanism bullet 3; (2) the three minor edits listed above; (3) the Medium-risk Change 5 keeps four UNVERIFIED open points as the plan asks. If Change 5 is rolled back as the plan allows, replace Claim 3's added sentence and Mechanism bullet 4's added text by "carrier undecided; exclude waiting step from the count".
