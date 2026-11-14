# Diff Analysis: C14 panel size versus cost, Proposal A versus Proposal B

<!-- Written incrementally by the debate-orchestrator: header and variants first, then one section per append. Counts in the Metadata block are reconciled at the end (see Summary). -->

## Metadata
- Generated: 2026-11-14 (orchestrator run, Mode A, depth standard)
- Variants compared: 2
- Focus: correctness, risk, test-coverage
- Total differences found: 48 rows (6 + 16 + 4 + 14 + 8); of these 30 are debate points (S 6 + C 16 + X 4 + A 4 promoted); the 14 unique contributions and the 4 non-promoted assumptions are recorded but are not debate points
- Categories: structural (6), content (16), contradictions (4), unique (14), shared assumptions (8: 4 UNSTATED promoted, 3 STATED, 1 CONTRADICTED flagged)

## Variants

| Id | File | Option (synth-04 C-14) | Position in one line | Lines | Words |
|----|------|------------------------|----------------------|-------|-------|
| Variant 1 (A) | `adversarial/variant-1-original.md` (copy of `proposal-a.md`) | Option A: default to two reviewers now | Drop the Tier 2 default from three reviewers to two with two-slot templates keyed on executor class; cap of 3 stays as ceiling; measure 2 against 3 afterwards | 204 | 5164 |
| Variant 2 (B) | `adversarial/variant-2-original.md` (copy of `proposal-b.md`) | Option B: fix the rubric first, cap 3, count after H-A | Keep three reviewers; make the parsed-sparse flag advisory (Phase 1, gated by G1); add audit keys and a replay script (Phase 0); decide 2 versus 3 after H-A with a pre-registered rule (Phase 2) | 224 | 6245 |

Both files carry the same seven H2 sections in the same order (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost). Both cite the same research base (R04, R11, E2 `COMBO-REPORT.md` at commit `4a22d74`, MR, `pilot-design.md`) and both state that two versus three reviewers inside reflect, Tier 2 versus Tier 1 recall (H-A) and the miss rate after a rubric change are unmeasured.

Orchestrator note on method: the one decision-relevant number on which the two files disagree (how many recorded runs the parsed-sparse flag forced into Tier 2) is a countable fact. It was recounted before the debate (see Appendix: Orchestrator fact check) so that the debate and the scoring start from a checked figure. The advocates are told to re-check it independently.

## Structural Differences

| # | Area | Variant A | Variant B | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Section skeleton | Seven H2 sections: Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost | Same seven H2 sections in the same order | Low |
| S-002 | Organisation of the Evidence section | By stance: "What supports defaulting to two" (A1-A9) then "What cuts against it" (C1-C5) | By subject: cap and count, why Tier 2 is paid, who is exposed, worth/cost/E2 (E-1 to E-18) | Medium |
| S-003 | Shape of the Correctness argument | Three parts: invariants-preserved table (7 rows), a 2x2 decision under uncertainty, an explicit "does not claim" list | Seven numbered points (behaviour change bounded, formatting-not-plan, counts cannot change, advisory exposure, why count waits, no open-conflict dependency, E2 analogy) | Medium |
| S-004 | Placement of the self-declared weakest point | Last item of the Risks section, after the risk table | First item of the Risks section, before the risk table | Low |
| S-005 | Staging structure of the proposal | Single change, no phases; measurement is a follow-on pilot arm | Three phases (0: no behaviour change; 1: gated rubric change; 2: decide the count), gate G1 and a pre-registered count rule | Medium |
| S-006 | Test section posture | Lists four existing tests that must change and eight new tests; one pilot arm | States no existing test changes (nothing pins the behaviour), five guard suites, six new items (N1-N6) of which two are not pytest | Medium |

Heading counts (from the heading extractor on the variant copies): A has 1 H1, 7 H2, 10 H3 (18 headings); B has 1 H1, 7 H2, 17 H3 (25 headings). Maximum depth is H3 in both, so there is no hierarchy-depth difference.

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|-------------------|-------------------|----------|
| C-001 | The core move | Default reviewer count 3 to 2; four new template files (`reflect-pre-duo`, `-duo-xh`, `reflect-post-duo`, `-duo-xh`); three-slot templates kept as the explicit opt-in | Reviewer count and cap untouched; the parsed-sparse flag becomes advisory (rows 1, 2, 8 lose `NOT coverage_degraded`, a union-coverage floor of 0.90 is added), gated by G1; instrumentation first | High |
| C-002 | What drives Tier 2 cost | The flag drives Tier 2: "38 of 39 selected Tier 2, 35 of them through the parsed-sparse pre-filter" (A1); a saving per escalation is a saving "on nearly every run" | Flag set in 35 runs but decisive in 1 certain and at most 5 of 39; 29 flagged runs are also decided by rows 4, 5 or 6 (E-5); the cost driver is the escalation rows, not the flag | High |
| C-003 | Evidence for the quality effect of the change | E2 is flat in panel size, two-reviewer panels matched three; external corpus says the second reviewer is the largest step; concedes none of it was run inside reflect (C1-C5) | Same E2 facts read as "indistinguishable at this sample size" (power, not equivalence); one recorded counterexample where T2 found a blocker T1 missed (E-6) | High |
| C-004 | Failure slack and the floor rule | With two reviewers one failed card leaves one: DEGRADED (R2); proposes one bounded re-dispatch before degrading; tags `ember + terra` -1.75 found as the cost of no slack | Counts unchanged so no slack change; no re-dispatch rule | High |
| C-005 | Executor-class exclusion at N=2 | Template chosen by executor class (3 rows); in-memory `resolve` dry run shows a bare two-slot template drops to one reviewer when the executor shares the second slot's class (R3) | Not applicable (N=3, existing templates) | High |
| C-006 | The `--reviewers` clamp (G-67) | Changes `max(2, min(4, n))` to `min(3, ...)` in `config.py:335`, closing G-67 and a test change | Records G-67, leaves it to C17; says "cap 3" means the reflect profile and `N_eff` (R6) | Medium |
| C-007 | Stage 2 shadow exit gate | Edits the shortfall rule (`reviewers_resolved == 3 and reviewers_complete == 2` becomes `complete < resolved`) and its label (R8) | Untouched; states the rule keeps its meaning because counts cannot change | Medium |
| C-008 | New telemetry or audit keys | `telemetry:` keys `panel_shortfall`, `reviewers_default_applied` | `tier_decision.yaml` audit keys `sparse_flag_decisive`, `escalation_path`; read-only `scripts/reflect_tier_replay.py` | Medium |
| C-009 | How the count is finally decided | Accept two before H-A; owner sets the rollback trigger before shipping (15-point bar suggested); a 2 versus 3 arm added to the H-A pilot | Pre-registered rule after H-A: 2 replaces 3 only if the two-reviewer arm is within 10 points (one-sided 95 percent) and cheaper; G1 gate decides Phase 1 | High |
| C-010 | Reversibility and rollback | A flag default and template data; claims B is a table-wide change that "cannot be rolled back by data alone" (A9) | Skill-text revert restores the old rule; `--tier 2` or `--depth deep` is a kill switch already in place | Medium |
| C-011 | Which consumers feel the change | All UC-1 and UC-2 Tier 2 runs and every new consumer (PR review, rf-qa replacement, tasklist review) | Only advisory consumers (workflow Wave 4, Stage 10.5 standard-depth); the blocking per-phase post gate is forced to `--depth deep` and cannot see it (E-9) | High |
| C-012 | Counterexample evidence | None offered for the claim that the third reviewer adds little beyond E2 | E-6: the only clear-cut flag-only run (`pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416`): Tier 2 merged verdict FAIL on blocker M-13; Tier 1 card has zero hits for "untracked"/"git status"/"ls-files" | High |
| C-013 | Pre-existing test coverage of the thing being changed | Four existing tests change (clamp test, shadow exit test, template NAMES/slots, default confirmation); the N=2 path is already tested (A4) | Nothing under `tests/` pins the pre-filter (E-8); new tests pin prose (N3) and a replay script (N1, N2); the unbuilt `sparse-labeled-spec` eval case is replaced (N4) | High |
| C-014 | Cost of the change and of measuring it | S to M build; run saving counted in calls (one reviewer, one calibrator, one debate variant) on 38 of 39 runs; token saving unmeasurable from existing data (R08) | S for Phase 0, M for Phases 0-2; saving 1 to 5 whole Tier 2 runs of 39 at best, zero in the interim if G1 stays closed; H-A 1.30M to 2.62M claude tokens | Medium |
| C-015 | Scope: document-review default (4 reviewers) and `live7` (7) | Out of scope but "a natural follow-on"; E2 measured exactly that consumer family | Out of scope; blocked by C03 because the E2 default model is not nameable in the packaged tier file | Low |
| C-016 | Reading of the external evidence | Zenodo corpus and arXiv preprint used to say a third vote is worth less than a third; "two is not optimal" is explicitly not claimed | Same sources used to say "not more than 3"; they "do not choose between 2 and 3" | Low |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | How many recorded runs the parsed-sparse flag forced into Tier 2 | A1: "38 of 39 ... selected Tier 2, 35 of them through the parsed-sparse pre-filter"; A8: Option B "removes Tier 2 for up to 34-35 of the 38-39 recorded runs"; section 2 table: B gives up "the whole Tier 2 pass for up to 34-35 of 38-39 plans" | E-5: flag set in 35 runs, Tier 2 in 38; flag the only reason for Tier 2 in 1 run for certain and at most 5 of 39; 29 flagged runs are decided by rows 4, 5 or 6 regardless of the flag; "34 or 35" is an upper bound the table does not support | High |
| X-002 | Whether Option B can be rolled back | A9: B changes escalation logic that is table-wide for every UC-1 consumer and "cannot be rolled back by data alone" | Risks R1 and CLI surface: a skill-text revert restores the old rule; `--tier 2` or `--depth deep` already force Tier 2 | Medium |
| X-003 | What Option B actually ships while gate G1 is closed | A section 2 and A8 treat B as the move that gives up Tier 2 on most plans and then compare its downside with A's | B "weakest point": on today's data G1 does not open (one clear-cut candidate, and it shows a Tier-2-only blocker), so Phase 1 is built behind the H-A pilot; what B delivers now is a corrected attribution, instrumentation, a frozen cap and a written count rule, "closer to Option C" | High |
| X-004 | How large B's own upper bound is | Not addressed | E-5 counts the row-0 run (`pre-renameTheScIssue-20261104174640`) in "at most 5", but its own `escalation_reason` says "S_domains=3 would also escalate via rule 4", so B's evidence supports at most 4; three further runs have no recorded inputs (intra-variant tension) | Low |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Executor-keyed two-slot templates with an in-memory `panel resolve` dry run per executor class, showing a bare two-slot template drops to one reviewer when the executor shares the second slot's class (R3) | High |
| U-002 | A | Floor rule plus one bounded re-dispatch of a reviewer that returned nothing before DEGRADED (R2); `ember + terra` -1.75 found as the evidence for no slack | High |
| U-003 | A | `reviewers_default_applied` and `panel_shortfall` telemetry so a later 2-versus-3 comparison can separate the groups | Medium |
| U-004 | A | Closes G-67 (clamp 4 to 3, `config.py:335`) and generalises the Stage 2 shortfall rule to `complete < resolved` (`reflect_shadow_exit.py:244-245`) | Medium |
| U-005 | A | 2x2 decision under uncertainty comparing what is given up, reversal and saving for A and B; explicit "does not claim" list (including not using the stale "sonnet alone" line) | Medium |
| U-006 | A | Observation that in UC-1 only the qa persona receives the spec body, so two of three reviewers are partially source-blind by construction (A7, R06) | Medium |
| U-007 | A | Out-of-setting caveat inventory for E2 (C1 to C5), including the one E2 size effect that survived testing (second luna, p 0.004) and why reflect's strict distinctness cannot reproduce it | Medium |
| U-008 | B | Recount by escalation path (E-5): 18 rule 4, 9 rule 6, 2 rule 5, 1 row 8, 1 row 0, 3 unrecorded, 1 pin, 4 unflagged | High |
| U-009 | B | E-6: the single clear-cut flag-only run, Tier 2 FAIL on M-13 (invariant probe INV-001, all five target files untracked, `git diff` criteria pass on empty output), with the Tier 1 card having zero hits | High |
| U-010 | B | Phase 0 instrumentation: `sparse_flag_decisive` and `escalation_path` audit keys and `scripts/reflect_tier_replay.py`, so the strata MR:540 asks for have a recorded value | High |
| U-011 | B | Gate G1 and the pre-registered 2-versus-3 rule (within 10 points, one-sided 95 percent, and cheaper) reusing `pilot-design.md` T-1 and T-2 | High |
| U-012 | B | Exposure map by consumer (workflow Wave 4, Stage 10.5 advisory; blocking post gate forced deep) and the finding that shadow runs reach Tier 2 through `--tier 2` pins so a rubric change does not slow the Stage 2 count (E-9, E-10) | Medium |
| U-013 | B | E-8: nothing under `tests/` pins the pre-filter, so an accidental change would not be caught; the D13 `sparse-labeled-spec` eval case was specified but never built | Medium |
| U-014 | B | R9 doc-drift item: several documents repeat "34 of 38 escalated because of the pre-filter" and need a pointer to the recount (MR:142, MR:556, `pilot-design.md`, R11 §12 item 4) | Low |

## Shared Assumptions

Agreement points scanned: both variants (1) keep the cap of 3 as a ceiling, (2) treat H-A as the missing measurement, (3) read E2 as flat in panel size within E2's setting, (4) use the 39-run recorded history as the denominator for cost, (5) treat the H-A pilot as the instrument that settles the count, (6) leave the document-review default out of scope, (7) rely on SKILL.md prose and templates being followed.

| A-NNN | Assumption | Source Agreement | Classification | Impact | Promoted |
|-------|------------|------------------|----------------|--------|----------|
| A-001 | The 39 recorded non-shadow pre runs (2026-06 to 2026-11, many skill versions, mostly workflow-generated plans without labelled ids) are representative of the Tier 2 workload the change will face | (4) denominators in A1 and E-5 | UNSTATED | High: the 18 rule-4 and 9 rule-6 shares, and every "nearly every run" saving, depend on it | Yes |
| A-002 | There is a stated trade-off rate or owner threshold: how much per-run saving justifies how much unmeasured quality risk before H-A exists (neither names a number for cost; A suggests the 15-point bar "as a proposal"; B uses 15 and 10 points only for the later decision) | (2), (5) | UNSTATED | High: without a guard on the trade-off the winner is set by who bears the burden of proof | Yes |
| A-003 | Tier 2's catch value sits in the number of reviewers; the one recorded Tier-2-only blocker (M-13) came from the invariant probe (a separate fault-finder step), not from any of the three reviewer cards | (3), (5) | UNSTATED | High: if value sits in debate and probe steps, reviewer count is a cheaper lever than assumed and the tier gate is a more dangerous one than assumed | Yes |
| A-004 | The two levers are independent: B's rubric change alters which plans reach Tier 2 (the strata H-A reads), A's change alters what Tier 2 is (two reviewers); neither says how a pilot that measures one behaves if the other ships first | (1), (5) | UNSTATED | Medium: a pilot can end up measuring a moving target, and the two proposals are not mutually exclusive | Yes |
| A-005 | A class label resolves to a distinct served model at dispatch (combo A3 collapsed all reviewers to sonnet; the "haiku" slot served by another model) | (7) | STATED (A R5 only; B relies on it for N=3 without saying so) | Medium: diversity at N=2 has no spare slot | No |
| A-006 | `fired_rule_number` and the input values in `tier_decision.yaml` are accurate; they are written by the orchestrating model across skill versions | (4) | STATED (B R3 only; A relies on the recount through R11 without saying so) | High for X-001 | No |
| A-007 | SKILL.md prose and templates are followed by the orchestrating model; tests pin prose, not behaviour | (7) | STATED (A R2 residual, shadow13 and shadow15; B N3 limit) | Medium | No |
| A-008 | E2's flat result in a setting with no reflect, no calibrator and no debate transfers at least weakly to reflect Tier 2 | (3) | CONTRADICTED by evidence both variants cite (R11 §12 item 3: "its ceiling cannot be read as the T2 ceiling"); A and B both disclaim it and A still leans on it | High: flagged for debate attention under C-003 | No (flagged) |

## Taxonomy tags (debate_topic_taxonomy, one level per point)

| Level | Points |
|-------|--------|
| L1 surface | S-001, S-004 |
| L2 structural | S-002, S-005, S-006, C-001, C-002, C-003, C-008, C-009, C-010, C-011, C-012, C-013, C-014, C-015, C-016, X-001, X-002, X-003, X-004, A-001 |
| L3 state mechanics | S-003 (invariants table), C-004 (floor and DEGRADED transition), C-005 (executor exclusion, slot exhaustion boundary), C-006 (clamp boundary), C-007 (shortfall guard condition), A-002 (guard on the trade-off), A-003 (invariant probe step), A-004 (state interaction between levers) |

Tagging notes: C-004 and C-005 carry no literal signal word; they are tagged L3 by content (a boundary at one versus two complete cards, a state transition from PASS-eligible to DEGRADED, slot exhaustion). A-NNN points that mention state, guard, boundary or invariant are tagged L3 per AC-AD5-3.

## Summary

- Total structural differences: 6
- Total content differences: 16
- Total contradictions: 4
- Total unique contributions: 14
- Total shared assumptions surfaced: 8 (UNSTATED: 4 promoted, STATED: 3, CONTRADICTED: 1)
- Debate denominator: total_diff_points = 6 (S) + 16 (C) + 4 (X) + 4 (A promoted) = 30
- Highest-severity items: C-001, C-002, C-003, C-004, C-005, C-009, C-011, C-012, C-013, X-001, X-003, A-001, A-002, A-003
- Taxonomy coverage in the diff: L1 2 points, L2 20 points, L3 8 points

## Appendix: Orchestrator fact check (escalation figure)

Method: `adversarial/recount_tier_decision.py` (read-only, run with `uv run python`) reads every `.dev/reflect/pre-*/artifacts/tier_decision.yaml` whose directory name does not contain `shadow` and prints the raw rows. There are 91 `pre-*` directories, 54 hold a `tier_decision.yaml`, and 15 of those are shadow runs, leaving 39 non-shadow files.

| Count | Value |
|-------|-------|
| Non-shadow `tier_decision.yaml` files | 39 |
| `selected_tier: 2` | 38 |
| `coverage_degraded: parsed-sparse` set | 35 |
| Flag set and Tier 2 | 34 (the 35th flagged run is the `--tier 1` pin, `pre-pr-submit-ci-monitor`) |
| Tier 2 without the flag | 4 (two `--depth deep`, `pre-design-20261104164711` rule 4, `pre-brainstormFixBri-20261106-001016` rule 6) |
| Flagged Tier 2 runs by recorded `fired_rule_number` | rule 4: 18; rule 6: 9; rule 5: 2; row 8: 1; row 0: 1; null: 3 |

Reading the rubric at `SKILL.md:431-439`: STOP rows 1 and 2 require `S_domains` at most 2 (row 1: exactly 1), `S_dev_density` at most 0.10 (row 1: 0.05) and `C` at least 0.85, so a plan that matches escalate row 4 (`S_domains >= 3`), 5 (`S_dev_density > 0.20`) or 6 (`C < 0.85`) cannot stop at Tier 1 with or without the flag. That puts 29 of the 34 flagged Tier 2 runs outside the flag's influence, on the recorded values. The remaining five: `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416` (row 8; recorded `S_domains` 2, `S_dev_density` 0.0: flag decisive); `pre-renameTheScIssue-20261104174640` (row 0; own text says `S_domains=3` would also escalate via rule 4: not decisive); `pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821`, `pre-TASK-WF-planTheRealBound-20261107-080351-20261107080543` (null, no inputs recorded: indeterminate); `pre-TASK-WF-planTheRealBound-20261107-080351-20261108-rerun` (null; `calibrated_confidence_t1` 0.86 and the text "S_domains may count 3": indeterminate).

Result of the orchestrator recount: Proposal B's table reproduces exactly. The flag was set in 35 runs and sat on 34 Tier 2 runs; it was the only reason for Tier 2 in 1 run for certain, and in at most 5 on B's loose count (at most 4 on B's own evidence, see X-004). The figures "35 of 39 escalate because of the flag", "34 by the pre-filter" and "up to 34-35 of 38-39 would have been eligible to stop at Tier 1" describe the flag being set, not the flag being decisive. Caveats stated before the debate: (1) `fired_rule_number` and the inputs are written by the orchestrating model, and only 7 of the 39 files record `S_domains` and 6 record `S_dev_density`, so the 29 rests largely on recorded rule claims and reason text; (2) the upper bound of 5 is a bound, not a count; (3) the E-6 counterexample was checked in the files: `t1-card.md` has 0 hits for `untracked|git status|ls-files`, no reviewer card mentions "untracked", and `adversarial/merged-verdict.yaml` lists M-13 (`grounding_gap`, `blocking`, source `invariant-probe:INV-001`), with `merged_verdict: FAIL`, `blocking_findings: [M-13]`. The advocates must re-test all of this independently.

### Addendum after Round 1 (orchestrator, recorded where the Step 1 fact check is kept)

Both advocates re-tested the escalation figure and went beyond the appendix above. Two further facts, both confirmed by the orchestrator in the files: (a) the E-6 run `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416` has a blind-calibrated Tier 1 confidence of `C: 0.68` in its `reflection-card.yaml` (so row 6 escalates it with or without the flag; the recorded "row 8" in its `tier_decision.yaml` is contradicted by its own card); (b) `makeTheAliasOnly` (Tier 1 card calibrated 0.75, `S_domains` 4) and `planTheRealBound-...080543` (Tier 1 card calibrated 0.53) are row 6 runs. The only run where the flag could be decisive is `planTheRealBound-...rerun` (Tier 1 card 0.86, `S_domains` likely 3 by path counting, which would fire row 4). Corrected finding: the flag was decisive in 0 recorded runs for certain and at most 1 of 39. Proposal B's "1 certain, at most 5" and its E-6 "clear-cut flag-only run" are overstated; Proposal A's "35 of 39" and "up to 34-35" are wrong by a wider margin. This changes the evidential weight of C-002, C-003, C-012, X-001, X-003 and X-004, not the diff-point list.
