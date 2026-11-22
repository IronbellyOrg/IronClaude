# Merge Execution Log

## Metadata
- Base: Variant 2 (CLAY, `variant-2-original.md`)
- Executor: merge-executor agent
- Changes applied: 8 of 8 planned
- Status: success
- Timestamp: 2026-11-20T04:28:33Z (merge started; later edits the same run)
- Merged file: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/merged-position-d02.md`
- Plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/refactor-plan.md`
- Rule applied throughout: the merged text is a neutral paper and states no winner. Every added sentence comes from the source files named in its provenance tag; anything the sources mark as unverified is marked UNVERIFIED in the merged text.

## Changes Applied

### Change 1: Run now bypass and a dropped `exit 1`
- **Status**: Applied
- **Source**: Variant 1, Mechanism and Cited facts 5 and 6; debate-transcript.md Round 2 (both advocates; Variant 2 concessions 1 and 2)
- **Target**: Base, Cost bullet 2 (replaced)
- **Before**: One sentence: a click on Run now or `orca automations run` bypasses the precheck and starts a real Claude session; the design handles it only by a scheduled shadow run.
- **After**: Full statement of both paths (the click, and a dropped `exit 1` that makes every tick start a session, up to 288 a day), "cron has neither path", the agreed bound on harm (one idle session per click; a few at most for a dropped `exit 1`), the scheduled shadow run, and the two Round 2 mitigations (a fixed always-exit-1 command; a "do nothing and stop" prompt) labelled as suggestions, not facts about master and not in the design.
- **Provenance tag**: `<!-- Source: Variant 1, Mechanism and Cited facts 5, 6; debate-transcript.md Round 2 ... - merged per Change #1 (replaces base bullet 2) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: What cron has actually been tested for
- **Status**: Applied
- **Source**: Variant 1, Cited fact 2; Variant 1 Round 2 concession 1 and new evidence 1; Scoring Matrix C-006
- **Target**: Base, Cited facts (new fact 9) and Risk (one new sentence)
- **Before**: No cron test evidence in the base. Facts ran 1 to 9.
- **After**: New fact 9 (per-minute firing 20:25:01Z and 20:26:01Z on 2026-11-18; `orca repo list` under `PATH=/usr/bin:/bin`, 6 repos; `gh auth status` under an empty environment, tested 2026-11-20; limit: mechanism tested, install path not; cron `apt install`ed by hand 2026-11-18 18:40:49, daemon started by hand 20:20:37, crontab empty, issue 515 open; cron 3.0pl1-197). One new Risk bullet (a single sentence) that cites fact 9 and the C-006 draw.
- **Provenance tag**: `<!-- Source: Variant 1, Cited fact 2 (with limits ...) - merged per Change #2 (new fact) -->` and a second tag on the Risk bullet.
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅
- **Note**: Inserting the fact after fact 8 pushed the base's old fact 9 to fact 10. It is tagged as renumbered. No other part of the base cites a fact number, so no reference broke.

### Change 3: Fix the six-field cron line in the old runbook
- **Status**: Applied
- **Source**: Variant 1, Cost bullet 2; Variant 1 Round 2 concession 7; diff-analysis.md C-010, U-004
- **Target**: Base, Cost (new bullet 5)
- **Before**: Section did not exist in the base.
- **After**: One bullet: the runbook line `0 */5 * * * *` (`docs/designs/issue-watcher-setup.md:288`, `:676`) is six fields and cron 3.0pl1 takes five; the handoff already uses five; not run here (UNVERIFIED by a test); the base's design 4.8 drops cron, so the fix applies only if cron stays; both advocates call it a doc defect, not a decision factor (C-010).
- **Provenance tag**: `<!-- Source: Variant 1, Cost bullet 2; ... - merged per Change #3 (new bullet) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: "Debated and rejected" is not backed
- **Status**: Applied
- **Source**: Variant 1, Risk bullet 2; both advocates; invariant-probe.md INV-028
- **Target**: Base, Risk (new bullet)
- **Before**: Section did not exist in the base.
- **After**: One bullet: only requirements line 18 mentions automations; the debate there covers one dispatcher against one entry per project and assumes cron; the owner's written reason is true only when the precheck exits 0; if cron stays, the written reason must be restated (INV-028 names zero setup R1, one dispatcher R16, no click path).
- **Provenance tag**: `<!-- Source: Variant 1, Risk bullet 2; ... INV-028 - merged per Change #4 (new bullet) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: Repair the base's overbroad sentence
- **Status**: Applied
- **Source**: Base fact 6 and Cost bullet 4; Variant 2 Round 2 concession 4; Variant 1 Round 2 concession 5
- **Target**: Base, Cited fact 6 (replaced)
- **Before**: "Nothing outside this repo has to change: no image, no cron package, no daemon start, no per-boot crontab step." followed by the Coder 515 and persistence sentences.
- **After**: "No image change, no cron package, no daemon start and no per-boot crontab step are needed for the scheduler. One creation step per Orca host is still needed", owner-run in the design (O3, O4); N5 binds the orchestrator, not a boot script; a boot script could do `list --json` then `create`, but none exists and none has been tested (UNVERIFIED). The base's Coder 515 and persistence sentences, including the UNVERIFIED survival inference, are kept word for word. Cost bullet 4 was left unchanged, as the plan targets fact 6 only.
- **Provenance tag**: `<!-- Source: Base (original, modified) - fact 6 rewritten per Change #5 ... -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅ (see Observation 2 below)

### Change 6: Write the comparison per command
- **Status**: Applied
- **Source**: diff-analysis.md A-001; invariant-probe.md INV-015, INV-022, INV-023; Round 2 of both advocates
- **Target**: Base, new section "Which poll is scheduled" (after Mechanism)
- **Before**: Section did not exist in the base.
- **After**: A two-row table (`once` with `repos.yaml` on master and in the PR 686 design; `run-all` with per-repo configs only in the unpushed branch `claim-handoff-planb`, `cli.py:432`) with where each exists, how it finds repos and whether a new project is enrolled automatically; four bullets: the papers compare different commands; the scheduler is independent in principle and the verdict is written per command; `once` can ship today for one repo while `run-all` waits for the branch for both routes; INV-023 (HIGH, UNADDRESSED) stated as open and blocking.
- **Provenance tag**: `<!-- Source: Variant 1 (Mechanism; Cited facts 2, 4), debate-transcript.md (A-001 ...), invariant-probe.md (INV-015, INV-022, INV-023); diff-analysis.md A-001 - merged per Change #6 (new section) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: What the scheduler does not decide
- **Status**: Applied
- **Source**: invariant-probe.md INV-024, INV-008, INV-011, INV-017, INV-020 (INV-015 cross reference)
- **Target**: Base, new section "What the scheduler choice does not settle"
- **Before**: Section did not exist in the base.
- **After**: Six bullets. Zero setup is not decided by cron or an automation (issue 515, per-host `superclaude install --force`, owner-created `Approved` field, issue 516 `Coordinator` worktree). A sweep can run about 525 s against a 300 s tick (`LOOP_CAP_S` 270, `CHILD_TIMEOUT_S` 255). Nobody reads a silent scheduler failure. The automation is coupled to the orchestrator checkout path (the unresolvable-workspace behaviour is labelled as Variant 2's reading of installed code, not re-checked by the fault-finder). Two workspaces for one user have separate locks. Project enrolment follows the poll (pointer to Change 6 section).
- **Provenance tag**: `<!-- Source: invariant-probe.md INV-024, INV-008, INV-011, INV-017, INV-020 ... - merged per Change #7 (new section) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: Debate outcome and the decisive fact
- **Status**: Applied
- **Source**: debate-transcript.md Metadata, Scoring Matrix, Convergence Assessment, Round 2 "What would change my mind" (both advocates); invariant-probe.md INV-023, INV-024, INV-026
- **Target**: Base, new closing section "Debate outcome (D02)"
- **Before**: Section did not exist in the base.
- **After**: Process (depth standard, 15 of 18 points resolved, 83.3% against 80%, BLOCKED_BY_INVARIANTS); an 18-row table of point-level results copied from the Scoring Matrix, stated as not summed into a choice; the three unresolved points (C-008, X-003, A-002); the two blocking invariants and the five MEDIUM warnings; where the advocates ended (about 50% cron, about 55% automation, both a toss-up, owner's R6 and R16 not overturned absent the decisive fact; no choice made, VERDICT.md applies the owner's weighting rule); the decisive fact with each advocate's stated move; the smaller boot-script fact for X-003.
- **Provenance tag**: `<!-- Source: debate-transcript.md (...); invariant-probe.md (INV-023, INV-024, INV-026) - merged per Change #8 (new closing section) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Other edits that are not numbered changes
All are small and traceable; none adds a new claim.
- **Title** renamed to "Merged position (D02): scheduler for the issue-watcher poll" (instruction in the task).
- **Framing paragraph** under the title ("How to read this paper"): says the paper is neutral, that Variant 2 is the text base through the tiebreaker (0.875 against 0.831 raw, margin 4.4 points under 5, 5 diff points against 3) and that the base sections state the CLAY position in their own voice. Sources: refactor-plan.md Overview; base-selection.md.
- **Claim section**: the base line "Author role: advocate for Clay's line." became "Author role of the base text: advocate for Clay's line." so the paper does not read as advocacy.
- **Provenance headers and Source tags** added per template section 6, using plain hyphens in place of the template's em dash (task rule: no em dashes).

## Post-Merge Validation

The merged file was re-read after the last edit, and grep was run on it for em dashes, winner language and headings.

### Structural Integrity
- Heading hierarchy: ✅ One H1 (the title). Nine H2 sections: Claim, Mechanism, Which poll is scheduled, Cited facts, Cost, Risk, What CLAY gets right, What the scheduler choice does not settle, Debate outcome (D02). Six H3 sections, all inside "Debate outcome (D02)" (Process, Point results, Unresolved points, Blocking invariants, Where the advocates ended, The decisive fact). No skipped level.
- Section ordering: ✅ The base's six headings keep their base order (Claim, Mechanism, Cited facts, Cost, Risk, What CLAY gets right). "Which poll is scheduled" sits right after Mechanism (plan). The other two new sections follow the base sections; "Debate outcome (D02)" is last (plan).
- Document flow: ✅ Facts, then costs and risks, then the base's own strengths, then what the scheduler does not settle, then the debate record. The fact list is numbered 1 to 10 with no gap. Every section has a Source tag; the three header comments are present. Both tables render as valid Markdown tables. Em dash and en dash count: 0.

### Internal References
- Total references: 10 (fact 9 twice, fact 6 once, "Which poll is scheduled" twice, "What the scheduler choice does not settle" once, "Cost, mitigations a and b" once, "(below)", "decisive fact below" and "the two sections above" once each)
- Resolved: 10
- Broken: 0
- Not counted: design labels (R4, O3, O4, N5, U6, U7, 4.8), debate point ids C-/X-/A-/S- (defined in the Point results table) and invariant ids INV-xxx. The INV ids are defined only in `invariant-probe.md`, which the merged paper cites as a source but does not reproduce (Observation 3).

### Contradiction Re-Scan
- New contradictions introduced: 0
- Checked: (1) any sentence declaring a winner or giving a recommendation: none. The two leans (about 50% cron, about 55% automation) are attributed to each advocate and followed by "This paper does not choose between them". The point-level table is labelled as not summed. (2) Fact 6 against Cost bullet 4 and against the old base sentence: consistent now, both say the creation step is owner-run. (3) Cost bullet 2 against base fact 4: consistent, both say Run now bypasses the precheck. (4) The Risk bullet on evidence against fact 9 and the C-006 row: consistent (draw). (5) "Which poll" claim that `once` can ship today against Cost and Risk: consistent, scoped to one repo. (6) Unverified marks kept: survival of an automation (fact 6), boot script, six-field line not run, unresolvable-workspace reading.
- Observations (not contradictions, no plan item covers them, left for the orchestrator):
  1. The base section "What CLAY gets right" has no matching "What OURS gets right" section, because the plan has no change for it. The framing paragraph says the section is the base text and not a conclusion. The orchestrator may want a balancing section if the paper is read on its own.
  2. "What CLAY gets right", bullet 3 ("no template change in another repository") is base text. It is true for the scheduler and now scoped that way in fact 6. The C-003 row and the "Which poll" section add that both routes still need a new `superclaude` build. A reader could see mild tension; I did not edit it because the plan does not.
  3. INV ids are not defined inside the merged paper.

## Summary
- Total changes planned: 8
- Successfully applied: 8
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
