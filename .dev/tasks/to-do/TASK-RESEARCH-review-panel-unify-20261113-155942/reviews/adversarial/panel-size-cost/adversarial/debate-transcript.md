# Adversarial Debate Transcript: C14 panel size versus cost

<!-- Written incrementally: header first, then one append per round. Advocate statements are recorded verbatim in substance (lightly trimmed of nothing but formatting); the orchestrator adds only labels, flags and scoring. -->

## Metadata
- Depth: standard
- Rounds planned: Round 1 (parallel), Round 2 (sequential rebuttals), Round 2.5 (invariant probe by an independent fault-finder), taxonomy coverage gate, convergence check
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential) plus Round 2.5 invariant probe; no Round 3 at depth standard
- Convergence threshold: 80% (default)
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Round 1 agents `advocate-A-c14-r1` and `advocate-B-c14-r1`; Round 2 rebuttals by two fresh unnamed general-purpose agents, because the harness refused a second named teammate)
- Invocation: the orchestrator dispatched the advocates with the Agent tool as separate `general-purpose` agents (no fallback)
- Debate points: 30 (S-001..S-006, C-001..C-016, X-001..X-004, A-001..A-004 promoted); A-008 flagged CONTRADICTED for attention

## Round 1: Advocate Statements

Both advocates were dispatched in one message and ran in parallel as separate `general-purpose` agents. Statements are recorded below; the orchestrator's own checks of claims that bear on scoring are marked **[ORCH-CHECK]**.

### Variant 1 Advocate (agent `advocate-A-c14-r1`, analyzer-qa) for Proposal A

**Position**: The advocate's own recount agrees with B's table, so it retracts A's "35 of 39" and "up to 34-35" claims: the flag was decisive in 1 to 2 of 39 runs. B is therefore a low-risk, low-yield move that does not cut Tier 2 cost on the typical run, while A's per-run saving stands. Final position: MERGE (A's two-reviewer default for the advisory skill path, B's Phase 0 keys, B's gate on any change to the flag).

**Fact check of the escalation figure** (ran `recount_tier_decision.py`; read SKILL.md:278-284 and :427-443; opened the five ambiguous `tier_decision.yaml` files and their `REPORT.md`; opened the E-6 run): script output matches the orchestrator's recount exactly (39 files; 38 Tier 2; 35 flagged; 34 flagged and Tier 2; rule 4 = 18, rule 6 = 9, rule 5 = 2, row 8 = 1, row 0 = 1, none = 3). Rows 1 and 2 need `S_domains` at most 2, `S_dev_density` at most 0.10 and `C` at least 0.85, so a plan matching row 4, 5 or 6 cannot stop at Tier 1 with or without the flag: 29 of 34 outside the flag's influence. Caveat: only 7 files record `S_domains`; for rule 6 at least seven runs record a numeric confidence in their reason text (0.84, 0.73, 0.80, 0.76, 0.75, 0.55, 0.61). The five ambiguous runs, decided by the advocate: (1) `fixTheScIssueWor` row 8, flag decisive; (2) `renameTheScIssue` own text says rule 4 also escalates, not decisive; (3) `makeTheAliasOnly` REPORT.md:6 Tier 1 card blind-calibrated 0.75, row 6 fires, not decisive; (4) `planTheRealBound-...080543` REPORT.md:6 Tier 1 card calibrated 0.53, row 6, not decisive; (5) `planTheRealBound-...rerun` Tier 1 card 0.86 ("would have stopped on confidence alone"), `S_domains` "may count 3", undetermined. Advocate's figure: decisive in 1 run for certain plus 1 undetermined, so 1 to 2 of 39; B's "at most 5" and the orchestrator's "at most 4" are both looser than the files support. E-6 holds: `t1-card.md`, all reviewer cards and calibrations, and the three variant originals have 0 hits for `untracked|git status|ls-files`; M-13 came from `invariant-probe.md` (Round 2.5, independent fault-finder, INV-001), and `source_variants` lists variants 1-3 only because they voted blocking in Round 2.6 (`merge-log.md:98`). Effect on A: A1 "35 of them" is wrong (34) and "through the parsed-sparse pre-filter" is a causal claim the files do not support; A8, the section 2 table cell for B's loss and "B saves a whole Tier 2 run on 35 of 39" are false and retracted; the savings comparison reverses in A's favour (A touches 38 of 39 runs, B 1 to 2). Extra data point: 9 of the 38 Tier 2 runs have exactly 2 reviewer cards on disk (26 have 3, 3 older runs none); reason not checked.

**[ORCH-CHECK]** REPORT.md lines confirmed by the orchestrator: `makeTheAliasOnly` line 6 "blind calibration of the Tier 1 card" 0.75; `planTheRealBound-...080543` line 6 "Tier 1 card calibrated 0.53"; `planTheRealBound-...rerun` line 20 "the Tier 1 card was calibrated at 0.86 and would have stopped on confidence alone, but the sparse-spec guard ... forbids a Tier 1 stop". The rerun also shows that run had two reviewers. So the files support: decisive in 1 run for certain, at most 2.

**Steelman of Variant 2**: Nothing changes until data exists (Phase 0 costs nothing; `--tier 2` is an existing kill switch). A's costs are real: dropping to two removes PASS-eligible slack (a 2-of-3 shortfall stays PASS-eligible, `test_verdict_mapping.py:572-580`; one failure out of two is DEGRADED, exit 11, `test_ensemble_stub_integration.py:251-277`); no source measures 2 against 3 inside reflect; E2's "indistinguishable at this sample size" (CR:381) is about power, not equivalence; the synthesis rates A High risk. B is honest: weak point first, correct recount, Phase 1 gated because the one clear-cut run is a counterexample, "closer to Option C". The pre-registered count rule (T-1, T-2 of `pilot-design.md`) stops post-hoc choice. B is right about the recount, the instrumentation, the exposure map (blocking gate versus advisory consumers) and that nothing pins the pre-filter.

**Strengths claimed**:
1. A is the only option that cuts spend on the typical run: 38 of 39 runs reach Tier 2 whatever the flag says; B changes at most 2 and ships nothing while G1 is closed (B Cost: "zero in the interim").
2. Two reviewers is already a production path: SKILL.md:648-659 (N=2 row, hard N=2 floor); executor removal collapses N=3 to two; 9 of 38 recorded Tier 2 runs have 2 cards; tests exist (`test_review_reflect_templates.py:96-110`, `test_ensemble_unit.py:151-159`). A moves a default value, not a mechanism.
3. A's change surface is test-pinned so drift is caught (clamp, exit gate, templates); B's has no pin (E-8, conceded by B).
4. Executor-keyed templates are necessary and the dry run reproduces: `t1b+t4` with executor haiku gives [sonnet] and skips `t4`; `t1b+t1a` with executor opus gives [sonnet] and skips `t1a`; executor sonnet raises ExclusionExhausted on both; packaged `x2` with executor haiku also raises ExclusionExhausted.
5. The exit-gate edit makes A's failure mode visible: `reflect_shadow_exit.py:244-245` hard-codes `== 3 and == 2`, so a 1-of-2 shortfall is invisible without it.
6. A is cheap to reverse (a flag default in four places plus template data).

**Weaknesses identified in Variant 2**:
1. B's lever is nearly inert: flag decisive in 1 to 2 runs; rows 4 and 6 drive 27 of 39 and B declines to touch them (R7); Tier 2 stays at about 36-37 of 39.
2. Phase 1 fails its own gate on the only data: G1 needs at least three clear-cut candidates and finds one, which shows a Tier-2-only blocker; near-term delivery is Option C plus instrumentation.
3. The count rule puts the burden on the cheaper option (within 10 points at one-sided 95 percent and cheaper); E2 at n=4-6 separated nothing (p 0.54-1.0), a 6-plan arm likely cannot resolve a 10-point margin (UNVERIFIED power); B's R8 admits the count may never be decided.
4. B's tests pin prose, not behaviour: N3 pins SKILL.md text; N4 relies on eval cases that do not exist; N2 hard-codes counts ("5 ... of which 1 clear-cut") that are too high, since three of the five are explained by Tier 1 confidence below 0.85 recorded in REPORT.md, which the replay script (reads `tier_decision.yaml` only) cannot see.
5. B's bound is internally inconsistent (X-004).
6. B's reversibility equals A's, so it has no advantage there.
7. B's premise that the count must wait ignores the current production path: 9 of 38 recorded runs already ran with two cards (unscored).

**Code spot-checks of Variant 1** (verified at HEAD): `panel.py:37-46, :73, :130-133, :143-146`; `config.py:264` (default 3), `commands.py:270-274` (default=3), clamp `config.py:335` (`max(2, min(4, ...))`); `reflect_shadow_exit.py:244-245` and "2-of-3" label at `:29`; `panel_lint.py:268`; `reviewers.py:41`; `ensemble.py:772-773`; `contract.py` trigger 10; tests `test_ensemble_unit.py:106-118` and `:151-159`, `test_shadow_exit_script.py:261-269`, `test_review_reflect_templates.py:14-21, :57-85, :96-110`, `test_panel_contract_lint.py` minimum-two-cards. A's in-memory dry run reproduced on the packaged tier file. Overstated: SKILL.md:632-633 lists rf-qa and rf-qa-qualitative as conditional per artifact kind, so "already runs as a pair" overstates it. Not addressed by A: SKILL.md:659 (post-removal rule) is written for N=3 and A's cost table lists no section 7.1 prose edit for N=2.

**Concessions**: (1) wrong numbers in A1, A8, the section 2 table and "B saves 35 of 39": retracted; (2) A9's "cannot be rolled back by data alone" overstated; (3) nothing measures 2 against 3 inside reflect, and E2's only surviving size effect (second luna, p 0.004) is a 2-to-3 gain; (4) A removes PASS-eligible slack and lands on a blocking path: the code-engine default feeds the blocking per-phase post gate (`--depth deep`, B's E-9); the advocate's own illustration (unverified transfer from CR:427, 2 of 30 luna blocks dropped, 6.7 percent): a sonnet-anchored 2-reviewer panel degrades about 6.7 percent of runs versus about 0.45 percent when two non-anchor reviewers must both fail; so the engine default should stay 3 until a pilot arm exists; (5) the resolver only dispatches under shadow and from Stage 3 (SKILL.md:311, :338); the default legacy engine never calls the panel; the invariants table is verified for the resolver, not for the section 7.1 prose that dispatches, where the N=2 post-removal sentence is unspecified; (6) token savings unproven: E2 `ember+sonnet` (2) 142,967 tokens against `ember+luna+sonnet` (3) 138,551; cost follows model choice more than count; (7) A's test plan has no test that the orchestrator picks the right template row (prose, A-007), none for debate convergence with two variants (R7, UNVERIFIED), and no rollback trigger (an owner decision).

**Shared assumption responses**: A-001 QUALIFY (one team's plans across many skill versions; fine for "Tier 2 almost always paid", not for per-row shares which rest on model-written fields, A-006). A-002 QUALIFY (a threshold is needed; neither names a cost number; an explicit owner call; suggests the 15-point bar of MR:527 as rollback trigger and B's 10 points as a pilot reading). A-003 REJECT (the one recorded Tier-2-only blocker came from the probe step: 0 hits in the Tier 1 card, all three reviewer cards, all three variant originals; the only recorded evidence puts the value outside reviewer count; it favours cutting a reviewer over gating the tier). A-004 QUALIFY (independent in code and nearly independent in effect; ship both, record `reviewers_default_applied` in the pilot strata). A-008 REJECT (E2's flat result says nothing about reflect's calibrator and debate; A's case should rest on the per-run saving, the existing 2-reviewer path and reversibility, not on E2).

**Per-point positions** (Round 1, advocate A):

| Point | Superior | Conf. | Evidence |
|-------|----------|-------|----------|
| S-001 | MERGE | 95 | Same seven sections |
| S-002 | MERGE | 55 | V1 isolates counter-evidence; V2 subject grouping easier to audit |
| S-003 | V1 | 60 | V1 invariants table mostly code-verified, but for the resolver, not the legacy path |
| S-004 | V2 | 70 | Weak point first is more candid |
| S-005 | MERGE | 65 | V2 Phase 0 and pre-registration better practice, but Phase 1 never ships under its own gate |
| S-006 | V1 | 60 | V1 maps changes to named existing tests but omits orchestrator-choice and convergence tests |
| C-001 | MERGE | 60 | A default for advisory path plus B Phase 0 keys |
| C-002 | V2 | 90 | Recount: flag decisive in 1 to 2 of 39 |
| C-003 | MERGE | 55 | Neither measures 2 against 3 in reflect; V2 right that E2 is power-limited |
| C-004 | V1 | 55 | V1 names the slack loss and mitigates it, but the loss is a real cost of A |
| C-005 | V1 | 90 | Dry run reproduced every cell |
| C-006 | V1 | 70 | `config.py:335` clamp 4 against cap 3 is a real inconsistency and can ship separately |
| C-007 | V1 | 75 | `:244-245` blind to a 1-of-2 shortfall without the edit |
| C-008 | MERGE | 80 | Key sets orthogonal and both useful |
| C-009 | MERGE | 60 | V2 pre-registration plus V1 default-applied telemetry |
| C-010 | MERGE | 75 | Both reversible; A9 overstated |
| C-011 | V2 | 70 | Exposure map shows A's engine default would touch the blocking gate |
| C-012 | V2 | 80 | E-6 verified, though it concerns the tier flag, not count (A-003) |
| C-013 | V1 | 70 | A's surface test-pinned, B's not (E-8) |
| C-014 | V1 | 60 | A touches 38 of 39 runs against B's 1 to 2, tokens unmeasured |
| C-015 | MERGE | 90 | Both out of scope |
| C-016 | MERGE | 85 | Both disclaim that external sources choose between 2 and 3 |
| X-001 | V2 | 95 | Reproduced by script and by hand |
| X-002 | V2 | 80 | A9 overstated |
| X-003 | V2 | 85 | G1 stays closed on the only data |
| X-004 | V2 | 80 | V2 nearer the truth; advocate tightens bound to 1 to 2 |
| A-001 | MERGE | 70 | QUALIFY |
| A-002 | MERGE | 70 | QUALIFY |
| A-003 | V1 | 75 | REJECT: blocker came from the probe step |
| A-004 | MERGE | 70 | QUALIFY |

Not checked by advocate A: `S_domains` inputs behind the 18 rule-4 runs, the E-6 `merged_verdict` line, why 9 runs had 2 cards.

### Variant 2 Advocate (agent `advocate-B-c14-r1`, analyzer-qa) for Proposal B

**Position**: The advocate says its variant's headline number is overstated and its own E-6 counterexample fails: the flag was decisive in 0 recorded runs for certain and at most 1 possible. What survives is the cost-premise correction, Phase 0 instrumentation and deciding the count after H-A on a pre-registered rule. Phase 1 is close to a no-op on recorded data. Variant 1's cost premise is false and its default change reaches the blocking post gate. Recommends MERGE that does not flip the default before an H-A arm exists.

**Fact check of the escalation figure**: ran `recount_tier_decision.py` and reproduced the orchestrator's counts exactly. Rows 3 and 3a are UC-2 only and row 7 needs enterprise, so a UC-1 plan matching row 4, 5 or 6 cannot stop at Tier 1 with or without the flag. Opened all five ambiguous runs: (1) `fixTheScIssueWor` (the E-6 run): `reflection-card.yaml:5,12,13` give self-reported 0.90, blind-calibrated `C: 0.68`, delta -0.22, so row 6 fires; the recorded "row 8" contradicts the run's own calibration; not decisive. (2) `renameTheScIssue`: `S_domains` 3 recorded, own text says rule 4 would also escalate; not decisive. (3) `makeTheAliasOnly`: `t1-card.md:6` `S_domains` 4, `REPORT.md:6` Tier 1 calibrated 0.75; rows 4 and 6; not decisive. (4) `planTheRealBound-...080543`: `REPORT.md:6` Tier 1 card calibrated 0.53; row 6; not decisive. (5) `planTheRealBound-...rerun`: C 0.86 and "domains may count 3"; the input snapshot holds a `src/` hook script (code), `tests/hooks` (tests) and `docs/designs` (docs), 3 by path counting, so row 4 likely fires; the only possibly flag-decisive run. A grep of non-YAML artifacts found about 14 flagged Tier 2 runs with independent `S_domains` of 3 or 4 or Tier 1 calibrated C below 0.85 (0.63, 0.79, 0.71, 0.60, 0.68, 0.75, 0.53), a floor. Did not re-execute the rubric; `fired_rule_number` is model-written. Verdict: about 33 of the 34 flagged Tier 2 runs are decided by rows 4, 5 or 6; flag decisive in 0 for certain, at most 1 possible. The variant's "1 certain, at most 5" (E-5, E-6, R1's "13 percent") is overstated: it trusted the recorded row 8 without cross-checking the run's calibration card. "29 independent of the flag" holds; the true figure is closer to 33 or 34. Effect: strengthened (the flag is not the cost driver; the synthesis's "acts on the measured driver" for Option B at synth-04:926 and "input-format reason" for Option C at :941 are both refuted); weakened (Phase 1 changes at most 1 of 39 runs, G1 has zero candidates; what survives is Phase 0 plus Phase 2, which is Option C plus instrumentation). On M-13: found by the fault-finder invariant probe (`invariant-probe.md`, Round 2.5, INV-001); the Tier 1 card, all six reviewer card files and the three variant originals have 0 hits; `merged-verdict` `source_variants` lists variants 1-3, which looks like attribution after Round 2.6, not discovery; so E-6 shows the probe step has value, not the third reviewer, and does not argue against a flag change.

**[ORCH-CHECK]** Confirmed by the orchestrator: `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/reflection-card.yaml` has `self_reported_confidence: 0.90`, `C: 0.68`, `calibration_delta: -0.22`; its `REPORT.md:8` has `confidence_calibrated: 0.77` (mean of reviewer calibrations); `t1-card.md:25` self-reported 0.90 "to be re-graded blind". `makeTheAliasOnly/t1-card.md:6` has `S_domains` 4. The rerun's `input-snapshot.yaml` lists `docs/designs/...`, `src/superclaude/hooks/scripts/...`, `tests/hooks/...` and `.dev/tasks/...` (7 files). Therefore Proposal B's E-6 "the one clear-cut flag-only run" is refuted by the run's own calibration card: Tier 1 had C 0.68 and could not have stopped. Files support: flag decisive in 0 runs for certain, at most 1 (the rerun, probably 0).

**Steelman of Variant 1**: Tier 2 is paid on 38 of 39 runs, and the recount strengthens this: the reasons (multi-domain, low Tier 1 confidence) are legitimate, so no rubric lever cuts it. Width is then the only lever on spend actually paid. Risk of 3 to 2 is bounded: E2 found no significant panel-size effect (CR:381); two-reviewer panels scored 2.25-2.50 of 14 against 1.83-2.20 for three-reviewer panels; N=2 is already defined, tested and executed (rotation row, executor-exclusion degrade, `reflect-pre-x2`, EV-1 `max(2, resolved)`); the change is a default plus template data and cheap to reverse; Variant 1 does real engineering Variant 2 skips (executor-keyed templates, its own failure modes R2, R3, R5, R7).

**Strengths claimed**:
1. It tested the cost premise and found it false; E-5 reproduces and the truth is more extreme. The correction applies to the synthesis, V1's A1, A8 and C5, and R11 §12 item 4.
2. Zero exposure on the blocking gate: the post gate runs `superclaude reflect run ... --depth deep` (`sc-tasklist-protocol/SKILL.md:1162`), not the rubric; workflow Wave 4 is advisory (`sc-workflow-protocol/SKILL.md:89-93`); Stage 10.5 ships "regardless of verdict".
3. No count change: the cap is tested code (`panel.py:73,130-133,143-146`); the Stage 2 shortfall rule keeps its meaning (`reflect_shadow_exit.py:244-245`).
4. The `escalation_path` key gives MR:540's strata a recorded value.
5. Accurate E2 reading: p 0.54-1.0 at n=4-6 is power, not equivalence (CR:381).
6. It found that nothing under `tests/` pins the pre-filter.

**Weaknesses identified in Variant 1**:
1. False cost premise (X-001): A1 "35 of them through the parsed-sparse pre-filter"; A8 and the section-2 table "up to 34-35"; C5 "35 of 39 escalate for an input-format reason"; truth 0-1 of 39, so the central 2x2 "given up" cell for B is overstated about 30 times or more; V1 cites the recount from R11 §12 and never checked decisiveness.
2. The change reaches the blocking gate, unstated: V1 changes the code engine's `--reviewers` default 3 to 2 (`commands.py:270-274`, `config.py:264`); the post gate calls `superclaude reflect run ... --depth deep` with no `--reviewers` (`sc-tasklist-protocol/SKILL.md:1162`), so the blocking gate silently drops to 2 reviewers on E2 evidence from a non-blocking, no-calibrator, no-debate setting.
3. The test plan misses its own main failure mode: tests 1-8 are structural; none measures recall, convergence or degrade rate; R7 admits the 0.80 convergence floor is untuned for two variants (UNVERIFIED); the rollback trigger is left to the owner; the re-dispatch step is prose and V1 itself cites shadow13 and shadow15 ignoring step 10.
4. Weak inference from 0 shortfalls (A5): 0 in 13 runs gives a 95 percent upper bound of about 23 percent on the shortfall rate (rule of three); a spare not yet needed is still a spare; E2's `ember+terra` at 0.50 of 14 (CR:294,298) shows what no slack costs.
5. The saving may be zero: V1's own section 3 notes `ember+sonnet` (142,967 tokens) cost more than `ember+luna+sonnet` (138,551); A2 admits per-reviewer cost is not recorded.
6. A9 overstates irreversibility (X-002): a text revert undoes B; `--tier 2` and `--depth deep` already force Tier 2; V1's own reversal is also an edit and redeploy.
7. It misses its best evidence: M-13 came from the probe, not a reviewer, which supports "reviewer count is not where the value sits", V1's thesis; V1 never noticed.
8. A shipped default changes the H-A target: if the default becomes 2 first, H-A's Tier 2 arm measures 2 reviewers unless the pilot pins 3 (A-004).

**Code spot-checks** (verified): V2 E-1 `panel.py:73,130-133,143-146` line for line; V2 E-8 (a grep of `tests/` for `tier_decision`, `selected_tier`, `fired_rule`, `coverage_degraded`, `parsed-sparse`, `Step 1B.2b` gives exactly 2 hits: `panel_lint_legacy/return-contract.yaml:16`, `markdown-lines.md:10`; the only `.py` hit under `src/` is `panel_lint.py:46`; no `sparse-labeled-spec` case under `.dev/eval-workspaces/sc-reflect/cases/`); rows 3-7 are evaluated before row 8 (SKILL.md:427 "applied in order; first match wins"); V2 E-9 in the tasklist and workflow protocols (Stage 10.5 also passes `--remediate`; R09 and SKILL.md:405-408 not re-read); V1 `config.py:335` is `max(2, min(4, raw_reviewers))`; V1 `reflect_shadow_exit.py:244-245` is `reviewers_resolved == 3 and reviewers_complete == 2`; V1's dry run reproduced with `panel.resolve(strict_distinct=True)` plus the CLI's class expansion (t1b+t4 with haiku gives [sonnet] and skips t4; t1b+t1a with opus gives [sonnet] and skips t1a; executor sonnet raises ExclusionExhausted on tier1b; x2 with haiku raises ExclusionExhausted on tier4; V1's table correct); `reflect-pre-x2` exists.

**Concessions**: (1) headline number wrong: 0 certain, at most 1 possible; E-5 "row 8: 1, clear-cut" and R1's "up to 13 percent" are wrong; (2) E-6 is not a counterexample: C 0.68 means the run escalates under the old and the new rule; it is an n=1 observation that Tier 1 missed M-13, which the probe found; (3) Phase 1 is nearly empty and G1 has no candidates, so "closer to Option C" holds and is worse; the interim saving is zero while 38 of 39 runs pay for three reviewers; (4) rows 4 and 6 are the real drivers (about 29 of 39) and V2 leaves them alone; (5) the 10-point count margin is the advocate's own invention; the pilot costs 1.30M-2.62M tokens (PD C-5), has no owner (R8) and its two-reviewer arm is undesigned; (6) N3 pins prose, not behaviour.

**Shared assumption responses**: A-001 QUALIFY (fine for row attribution because decisions are plan-level; not representative of future load: mostly workflow plans with no labelled ids, 35 of 39 flagged, many skill versions, only 4 of 38 decisions non-sparse per the PD quota paragraph). A-002 QUALIFY (no trade-off rate exists; both variants use quality thresholds only; without a threshold the burden of proof decides, which favours measure-first; an owner can override but it is a decision, not a finding). A-003 REJECT as the assumption that Tier 2's value sits in the reviewer count; confirmed M-13 came from the probe with 0 reviewer-card mentions; it cuts both ways: cutting a reviewer may be cheap and a Tier 1 stop loses the probe, so a tier gate is more dangerous than a width change. A-004 QUALIFY (independent mechanisms; they interact in measurement: if V1 ships first, H-A's Tier 2 arm measures 2 unless it pins 3; if V2 Phase 1 ships first the strata shift by at most 1 run). A-008 QUALIFY (E2's flat result transfers weakly at best; R11 §12 item 3 as quoted in the diff analysis says its ceiling "cannot be read as the T2 ceiling"; non-significance at n=4-6 is not equivalence; V1 disclaims it and still leans on it in A3 and A8).

**Per-point positions** (Round 1, advocate B):

| Point | Superior | Conf. | Evidence |
|-------|----------|-------|----------|
| S-001 | MERGE | 95 | Same seven sections |
| S-002 | V1 | 60 | "Cuts against it" block makes counter-evidence easy to audit |
| S-003 | V1 | 65 | Invariants table is a better correctness artifact |
| S-004 | V2 | 60 | Weakest point first is better disclosure |
| S-005 | MERGE | 60 | Keep phases 0 and 2; Phase 1 empty on today's data |
| S-006 | MERGE | 60 | V1 concrete test edits plus V2 "nothing pins this" |
| C-001 | MERGE | 60 | Phase 0 plus V1 duo templates as opt-in; no default flip before an H-A arm |
| C-002 | V2 | 92 | Flag decisive in 0-1 of 39; rows 4 and 6 drive spend |
| C-003 | V2 | 60 | "Power not equivalence" correct; E-6 half retracted |
| C-004 | MERGE | 60 | V1 names the no-slack degrade; V2 N=3 avoids it; keep V1 re-dispatch for an H-A arm |
| C-005 | V1 | 85 | Dry run reproduced; executor-keyed table needed at N=2 |
| C-006 | MERGE | 55 | 4 contradicts cap 3, but the clamp sits on the post-gate path C17 owns |
| C-007 | V2 | 65 | Leave the shortfall rule until the count changes; V1 `complete < resolved` right then |
| C-008 | MERGE | 75 | Complementary keys |
| C-009 | V2 | 70 | Pre-registered rule beats undefined rollback, though the 10-point margin is invented |
| C-010 | V2 | 65 | Text revert and existing kill switch; A9 overstated |
| C-011 | V2 | 80 | Blocking gate untouched by V2, reached by V1's default |
| C-012 | V1 | 55 | E-6 does not hold as stated (C 0.68); probe finding stands as observation |
| C-013 | MERGE | 60 | V2 finds nothing pins the pre-filter; V1 edits concrete but none measure quality |
| C-014 | V1 | 55 | V1 may save something per run (unquantified, possibly zero); V2 recorded saving about 0 |
| C-015 | MERGE | 70 | Both out of scope |
| C-016 | V2 | 60 | Sources do not choose 2 versus 3; V1 reads past them |
| X-001 | V2 | 95 | Reproduced and strengthened to 0-1; V2's own "1, at most 5" overstated |
| X-002 | V2 | 75 | Text revert and kill switch undo B; V1's rollback is also an edit and redeploy |
| X-003 | V2 | 85 | B ships near status quo plus instrumentation, more so after the recount |
| X-004 | MERGE | 90 | Both the orchestrator's 4 and V2's 5 too high; truth 0-1 |
| A-001 | MERGE | 70 | Valid for row attribution, unrepresentative of future load |
| A-002 | MERGE | 75 | No threshold exists; owner must set it |
| A-003 | V1 | 60 | Probe finding means reviewer count is probably a cheaper lever than assumed |
| A-004 | MERGE | 70 | Independent mechanisms, but a default flip changes what H-A measures |

## Round 2: Rebuttals

Sequential: the Variant 1 advocate (a fresh `general-purpose` agent, `advocate-A-r2`) read the full Round 1 transcript first; the Variant 2 advocate then answered with A's rebuttal in hand. (The harness refused a second named teammate, so the Round 2 agents were spawned unnamed; they are still separate agents.)

### Variant 1 Rebuttal (Proposal A advocate, Round 2)

**Response to criticisms of Variant 1** (B's weaknesses 1-8):
1. False cost premise (X-001): ACCEPT; "35 of 39" retracted. Re-based: all 38 Tier 2 runs have `tier_decision.yaml`, 9 already ran with two cards, so narrow A changes the other 26 (68 percent), not "38 of 39".
2. Reaches the blocking gate: ACCEPT for the engine default, REBUT that this binds A. The post gate calls `superclaude reflect run ... --depth deep` with no `--reviewers` (`sc-tasklist-protocol/SKILL.md:1162`), so it takes the Click and config defaults (`commands.py:270-274`, `config.py:264`). The skill path is separate: `SKILL.md:256` calls `reflect run` "the wrapper" and the skill prose never invokes it; the skill default is prose at `SKILL.md:86` and `commands/reflect.md:100`; no test couples the two. Skill-path consumers found are advisory (workflow Wave 4, troubleshoot Phase B/D, an optional delegate in `/sc:implement`; the `/sc:implement` call site not read in full; owner to confirm).
3. Test plan misses its failure modes: ACCEPT (see below).
4. Weak inference from zero shortfalls: ACCEPT. 0 of 28 gives a 95 percent upper bound of about 10.7 percent (rule of three, 3/28); showing under 5 percent needs about 60 clean runs.
5. Saving may be zero in tokens: QUALIFY. Tokens unmeasured; a second, token-independent effect (calibrator disjointness, below).
6. A9 irreversibility: ACCEPT; narrow A's rollback is also a text edit.
7. Missed the M-13 evidence: ACCEPT; A-003 now favours A.
8. H-A target shifts: ACCEPT; the pilot pins its arms; 9 of 35 recorded runs already mix N=2 and N=3, so the baseline was never clean.
B's concessions stand: Phase 1 empty, the 10-point margin invented, N3 pins prose.

**Updated assessment: the narrowest defensible A ("A-min")**:
- Change the skill default only: `SKILL.md:86`, `commands/reflect.md:100`, the "(default)" label in the section 7.1 table and the N=3 wording at `SKILL.md:659` ("restore N=3"). Keep `--reviewers 3` and `--strategy enterprise` as opt-ins.
- Engine stays 3 (`commands.py`, `config.py`, the clamp; the clamp is G-67 and belongs to C17).
- Do not touch duo templates, executor-keyed shadow template selection or `reflect_shadow_exit.py:244-245`; shadow runs stay pinned at 3.
- Required companion edit A never stated: `SKILL.md:340` says "Run shadow measurement runs with the default reviewer count" and `review panel resolve` has no count option; shadow parity compares the legacy rotation with `panel/resolution.json` (`reflect_shadow_exit.py:117-170`). With a skill default of 2 against the 3-slot `@reflect-pre`, every shadow run would recompute `panel_parity: false`, silently breaking the Stage 2 count (13 of 20). Fix: `SKILL.md:340` becomes "run shadow measurement runs with `--reviewers 3`" plus a text pin. Executor-keyed duo templates return only when the panel engine is evaluated at N=2 (Stage 3).
- The adversarial call keeps `--depth standard` (`SKILL.md:694-696`); probe, debate, calibrator and evidence validator untouched.
- Saving: the legacy skill path is where all 38 recorded Tier 2 runs happened; the saving (one reviewer, one calibrator, one debate variant) applies on 26 of 38 runs; the post-gate saving was never in the measured population. Claim calls, not dollars.

**Slack and floor**: with N=2 one failed card leads to DEGRADED. The re-dispatch rule is prose, so it lowers the rate but does not guard the floor. Guards that exist: `panel_lint.py:268` (`required = max(2, resolved)`, test `test_panel_contract_lint.py:284-292`); the M==1 degrade is tested only at N=3 (`test_i5`). Add an N=2 mirror of `test_i5` and an EV-1 test for a two-resolved run with one card (these pin semantics, not rate), plus a text pin on the re-dispatch sentence (prose only; lapses documented at shadow13 and shadow15).

**The nine two-card runs by cause** (read from their REPORT.md): executor exclusion 2 (`detachTheCcsessi`, `phase3CodegraphA`); deliberate 1 (`implementGitHubI`, "Two were used so the calibrator stays disjoint"); missing card 1 (`closeIronbellyOr-20261104084538` has reviewer-1 and reviewer-3, no reviewer-2, no REPORT.md; the only possible failure, unattributable); no cause stated 5 (`enforceTheOwnerP`, `planTheRealBound-rerun`, `rollOutTheIssueW`, `phase1RemovalSpe`, `phase2CodegraphI`). For A: at most 1 of 9 is a failure, the floor risk is not observed. For B: "the count must wait" fails as a premise; about a quarter of production already runs two, unscored.

**Missing tests**: wrong template per executor at dispatch is prose, so pytest cannot test model behaviour; two things can exist: a deterministic table test if template choice moves into code (`--executor-class` row selection) and a post-hoc lint on run artifacts (resolved count equals requested count unless `executor_exclusion_degraded` is set); otherwise only a pilot covers it. Convergence with two variants: the 0.80 floor is a number check and unit-testable; the statistic's behaviour is measurement only. DEGRADED rate at N=2: telemetry only (`panel_shortfall`); a rollback trigger is an owner decision; suggested: revert if the shortfall rate exceeds 10 percent over the first 30 two-reviewer runs, or if median convergence falls below 0.80.

**B's pieces**: Phase 0: merge, with corrections: the replay script must not read `tier_decision.yaml` alone (the E-6 run's row 8 contradicts its own card); it must read calibrated `C` from `artifacts/t1-calibration.yaml` (11 of 39 runs) or `reflection-card.yaml` `C:` (5 of 39), `S_domains` from `t1-card.md` (22 of 39), `input-snapshot.yaml` (38 of 39) for path-based domain counting, everything else "not evaluable"; the prospective key should be a counterfactual recorded at decision time, `tier_without_flag`, computed after calibration; N2 must not hard-code "5, of which 1 clear-cut", only derivable counts (39, 38, 35 flagged, 34 flagged and Tier 2) plus that the E-6 run is classified not decisive. Phase 1: do not merge (decisive in at most 1 of 39, G1 has no candidates; revisit when the prospective key has recorded decisive runs). Phase 2: merge the pre-registration idea, made symmetric with an owner-set margin instead of the invented 10 points; arms T1, T2 with 2, T2 with 3.

**A-003**: A-min must leave Round 2.5 and the debate alone. The 2-card `planTheRealBound-rerun` run skipped the invariant probe and the rebuttal round ("depth quick") and scored convergence 0.40; that run mixes N and depth. A-003 makes A-min the merge base; B's Phase 1 would remove the probe from plans it stops at Tier 1. Evidence is one run in either direction.

**New evidence**: (1) the 0.40 run is the only 2-card run below the 0.80 floor, explained by depth rather than N (REPORT.md lines 20-21 and 104). (2) Calibrator disjointness across 35 Tier 2 runs with a recorded tag: three-card runs 23 of 26 `calibrator_diversity: degraded`; two-card runs 6 of 8 tagged `full` (the ninth has no tag); cause: with three anthropic classes as reviewers no class is left for the calibrator; caveats: the 2-card choice may be deliberate, small sample, grep covered REPORT.md, cards and artifacts; with a known executor and N=2 the calibrator can still collide with the executor class. (3) Convergence in recorded runs (`return-contract.yaml`): two-card runs 0.40, 0.947, 0.958, 0.968 and four at 1.0 (7 of 8 at or above 0.80); three-card runs 1 of about 25 below 0.80 (0.76); retrospective, unscored for quality. (4) Parity coupling at `SKILL.md:340` and `reflect_shadow_exit.py:117-170`. (5) `SKILL.md:694-696` pins `--depth standard` for the adversarial call and `SKILL.md:681` says "2-3 reviewer cards".

**Revised positions**: C-002, X-001: V2 93; C-006: MERGE 55 (A-min leaves the clamp to C17); C-007: V2 70 (shadow stays pinned at 3); C-011: MERGE 75; C-012: V1 65 (E-6 refuted by its own card); C-014: V1 65 (saving on 26 of 38 runs); C-004, C-005: MERGE 60 (executor-keyed templates deferred to Stage 3); X-002: V2 85; X-003: V2 90; X-004: MERGE 90. Shared assumptions: A-001 QUALIFY 70; A-002 MERGE 75 (owner sets threshold; proposed rollback numbers above); A-003 REJECT as stated 70 (the blocker came from the probe; favours cutting width over gating the tier; A-min leaves the probe alone); A-004 QUALIFY 75 (independent in code; pin pilot arms and shadow at 3); A-008 REJECT 80.

**Final recommended merge (advocate A)**: Take from A: the skill-path default of 2 with the `SKILL.md:340` shadow pin, the section 7.1 wording fix, the telemetry keys and `--depth standard` pinned by text; the N=2 mirror of `test_i5` and the EV-1 test. Take from B: Phase 0 with the corrected reads; the Phase 2 pre-registration made symmetric; E-8's finding that nothing pins the pre-filter. Leave out for now: Phase 1; the engine default, the clamp, the duo templates and the exit-gate edit. Conditions: the owner accepts a default of 2 before H-A; the owner sets rollback numbers; the owner confirms no blocking consumer calls `/sc:reflect` on the skill path. Stays open: 2 versus 3 quality inside reflect; convergence at N=2 beyond 8 recorded runs; the token saving; calibrator-versus-executor collision at N=2.

### Variant 2 Rebuttal (Proposal B advocate, Round 2)

**Verification of the new Variant 1 claims** (the advocate tested each against the repository):
- (a) PARTLY. Premise CONFIRMED: `SKILL.md:340` says `review panel resolve` "has no reviewer-count option and does not apply N_eff" and "Run shadow measurement runs with the default reviewer count"; `scripts/reflect_shadow_exit.py:139-142` returns parity False when the card-header count differs from the resolved count; `:173-174` returns False when the legacy rotation has a different count; `:323-324` adds "parity does not hold" to the failures; a skill default of 2 against the 3-slot `@reflect-pre` would fail every Stage 2 shadow run. The `--reviewers 3` pin works mechanically (parity and the `:244-245` rule keep their meaning if shadow stays at 3), but the pin is prose only and nothing launches shadow runs (`--t2-engine` appears only in `SKILL.md` (10 hits), `refs/reviewer-spec.md` (1), `manifest_cmd.py` (2) and two test files; `commands/reflect.md` does not mention it); a conditional default is firmer: "default 2; 3 when the effective engine is shadow" in the flag definition at `SKILL.md:86` plus `:340`. A-min's edit list is incomplete: `SKILL.md:240` and `refs/input-resolution.md:92` ("3 aliases or more: T2 with 3 reviewers (full diversity)"); `refs/reviewer-spec.md:97` and `:102` duplicating `SKILL.md:655` and `:658` (the post-removal "restore N=3" sentence is at `:658`; A cited `:659`, which is blank); `commands/reflect.md:221` ("3 heterogeneous reviewers fan out"); the `t2_model_class_diversity` label (recorded two-card runs already say `full`: `planTheRealBound-rerun/return-contract.yaml:42`, `phase1RemovalSpe/return-contract.yaml:44`); the `:658` wording covers only an executor of `sonnet`; `models.py:91-92` documents the engine's `--reviewers` default 3 as spec section 5.1, so a skill default of 2 splits one flag name across two documented defaults. No test pins the default text (grep of `tests/` finds nothing; `test_reviewer_brief_constraints.py` pins only the agent-type cross-reference). A-min is about 9 edits in 5 files plus the mirrors, with nothing to catch drift.
- (b) CONFIRMED with one qualification. The post gate is `superclaude reflect run ... --depth deep` with no `--reviewers` (`sc-tasklist-protocol/SKILL.md:1162`) and takes the engine default (`commands.py:270-274`, `default=3`); the skill never calls the engine (`SKILL.md:256` mentions it only for `--isolate-reviewers`). Skill-path consumers with Tier 2 reachable: workflow Wave 4 (advisory, `sc-workflow-protocol/SKILL.md:89-93`); tasklist Stage 10.5 (no `--reviewers`; "the bundle ships regardless of verdict", `sc-tasklist-protocol/SKILL.md:1619-1650`); troubleshoot, auggie-review and the commands name `/sc:reflect --mode post` as the pre-commit gate "the user runs" (`commands/troubleshoot.md:207,217`), human-gated; `sc-implement-protocol/SKILL.md:204` and `commands/implement.md:99` list reflect as a non-goal; no `reflect` reference in the pr-submit protocol. Result: no automated blocking consumer; the nearest is the user-run commit gate where a person reads a DEGRADED verdict. Not checked: the troubleshoot SKILL's `--type task` call sites.
- (c) CONFIRMED with a new finding: 9 two-card runs among 38 Tier 2 runs (26 three-card, 3 with none). Executor exclusion 2 (`detachTheCcsessi/REPORT.md:26` "executor class opus excluded"; `phase3CodegraphA/REPORT.md:5` "executor opus excluded"); deliberate 1 (`implementGitHubI/REPORT.md:30` "Two were used so the calibrator (opus class) stays disjoint from the reviewers"); missing card 1 (`closeIronbellyOr`: reviewer-1 and reviewer-3 cards, no REPORT or contract); unstated 5 (`enforceTheOwnerP`, `rollOutTheIssueW`, `phase1RemovalSpe`, `planTheRealBound-rerun`, `phase2CodegraphI`; `phase2CodegraphI` likely belongs to exclusion: its `executor_class_source` is `session-model` and its same-day sibling excluded opus, not stated in the file, unverified; `enforceTheOwnerP` also had "calibrator and judge opus (same class as the plan's author, so diversity is degraded)", REPORT.md:29). Implication: the orchestrator already picks N=2 under the skill's own rules, once explicitly to keep the calibrator disjoint; "the count must wait" is wrong as a premise; what cannot be known before an arm exists is whether 2 matches 3 on recall.
- (d) Real in shape; PARTLY on exact numbers. Recount: three-card runs are 22 `degraded`, 3 `full`, 1 untagged (22 of 25 tagged, not 23 of 26); two-card runs are 6 `full`, 2 `degraded`, 1 untagged. The mechanism is written in the files ("reviewer pool used all three resolvable classes (sonnet, haiku->glm-5.3, opus); no disjoint calibrator class exists", `pre-design` contract; the `brainstormFixBri` run says the same) and follows from the rule at `SKILL.md:1248-1253`. Effect: the strongest quality argument for A-min; B keeps a default that structurally disables section 11.3 disjointness on about 88 percent of runs and never addressed it. It is a guarantee argument, not a recall argument; no in-repo measurement ties disjointness to catch rate. `full` at N=2 is cheap (three classes minus two reviewers leaves one), but with an opus executor the calibrator still collides with the executor (both exclusion runs have calibrator opus), so the executor, reviewer and calibrator partition (`SKILL.md:648`) is not met at N=2 either; the real fix is a fourth class in the pool, not only a smaller N.
- (e) CONFIRMED values; they show little. Two-card: 0.40, 0.947, 0.9583, 0.968 and four at 1.0; three-card: one below 0.80 (0.76, `writeTheP0LivePl`), the rest from 0.852 up, mostly 1.0; the 0.40 run is `--depth quick` (REPORT.md:21 and :104: no rebuttal round, no probe), confounding N with depth. They can show no sign of harm and a ceiling effect; they cannot show quality: convergence measures agreement among variants, two variants agree at least as easily as three, no ground truth, retrospective and unscored.

**Response to Variant 1's Round 2 arguments**: (1) re-based saving of 26 of 38 runs: ACCEPT, in calls only; (2) engine independence at runtime: ACCEPT, QUALIFY on the surface (the engine's documented section 5.1 default stays 3); (3) no duo templates or exit-gate edit: ACCEPT (the legacy rotation prose at `:658` restores N, which removes R3 on the skill path; the sentence needs wording for haiku and opus executors); (4) shadow pin: QUALIFY (a conditional default, not an instruction to pass a flag); (5) rollback trigger (shortfall over 10 percent in the first 30 runs or median convergence below 0.80): QUALIFY (the shortfall half is a tripwire, not a test: at a true rate of 10 percent P(at least 4 of 30) is about 0.35, it reliably catches 20 percent or more; the convergence half is a poor trigger because of the ceiling); (6) nine two-card causes: ACCEPT; (7) calibrator disjointness: ACCEPT as A-min's best argument, with the executor-collision limit; (8) convergence figures: QUALIFY; (9) Phase 0 corrections: ACCEPT, with one change below; (10) Phase 1 dropped: ACCEPT; (11) symmetric pre-registration: ACCEPT with an inconclusive-outcome rule; (12) A-003 favours A-min: ACCEPT.

**Updated assessment**: B's headline lever is inert and its "count must wait" premise fails on (c). B still contributes the corrected cost attribution, E-8, the exposure map (re-verified) and the pre-registered count rule. **A-min should be the merge base**: it changes behaviour on a real share of runs, touches no blocking path, and its mechanism is now evidenced. A-min needs five conditions: (1) the shadow default is conditional in the flag definition; (2) all coupled places are edited with one drift-pin test over the listed spots; (3) the rollback tripwire is written before shipping; (4) `reviewers_default_applied` and `calibrator_diversity` are recorded as strata; (5) the owner accepts that this is "a cost cut on thin evidence" for advisory consumers, with the post gate unaffected. B's Phase 0: retrospective half, do not build (the recount is done; a script plus N1 and N2 re-derive a number now known to be about 0-1); prospective half, build and aim it at rows 4 and 6: the rubric is "first match wins" (`SKILL.md:427`), so `fired_rule_number` hides rows that also match; record all matching rows, the blind-calibrated `C` and `S_domains` at decision time, and `tier_without_flag`, as audit-only keys (precedent `SKILL.md:469`), giving the H-A strata (MR:540) a recorded value for the rows that drive 27 of 39 runs. Count rule: a symmetric rule beats B's; arms T1, T2 with 2, T2 with 3, owner-set margin; it must state the inconclusive outcome in advance (under A-min the incumbent is 2) and a minimum n or declare "inconclusive" (E2 at n=4-6 could not separate panels).

**New evidence**: `implementGitHubI/REPORT.md:30` shows the orchestrator already trades a reviewer for calibrator disjointness; both executor-exclusion runs have calibrator class equal to executor class (opus); `t2_model_class_diversity` is inconsistent with its own table (`SKILL.md:239-240`), so the A-006 model-written-field risk is real; recorded shadow launches have no script or command carrying `--reviewers`; no test pins the reviewer default text.

**Revised positions**: C-001 MERGE (A-min base) 70; C-002 and X-001 V2 95; C-004 MERGE 60; C-005 MERGE 60; C-007 V2 75 (shadow stays at 3, no gate edit); C-009 MERGE (symmetric rule) 70; C-011 MERGE 80; C-013 MERGE 55 (neither pins behaviour; A-min needs a drift pin); C-014 V1 60 (calls only, about 9 edits). A-001 QUALIFY 70; A-002 MERGE 75; A-003 REJECT 75; A-004 QUALIFY 80 (pilot pins its arms, shadow stays at 3); A-008 REJECT 80.

**Final recommended merge (advocate B)**: From A-min: the skill default of 2 plus the conditional shadow default and the complete coupled-edit list; an N=2 mirror of `test_i5`, an EV-1 test for a two-resolved run with one card, a drift pin over the default text, and the rollback tripwire; keep the engine at 3, the clamp (C17) and the exit gate. From B: the prospective audit keys aimed at rows 4 and 6; E-8 as a finding; the exposure map; the symmetric pre-registered count rule; drop Phase 1 and the replay script. Conditions: the owner accepts a default of 2 before H-A, sets the tripwire numbers, and confirms the user-run commit gate is acceptable at N=2. Stays open: recall at 2 versus 3 inside reflect; the token saving; whether to add a fourth reviewer class instead of cutting N; executor and calibrator collision at N=2; whether `phase2CodegraphI` was an exclusion run.

**Orchestrator note on process integrity**: after Round 2 the two advocates converge on one merged proposal ("A-min as base plus B's prospective audit keys and a symmetric count rule") and each has retracted its own headline claim. Convergence this complete after a single rebuttal round is the pattern the protocol treats as a possible sycophancy signal; the Round 2.5 fault-finder is therefore told to probe the consensus itself, including the claim that A-min is safe, rather than the variants.

## Round 2.5: Invariant Probe (summary; full table in `invariant-probe.md`)

An independent fault-finder agent (not an advocate) probed the six categories, including `sufficiency_challenge`, against the emerging consensus K1-K6. Result: 14 findings; 4 ADDRESSED (INV-003 partly, INV-005, INV-007, INV-014 partly), 10 UNADDRESSED: **3 HIGH** (INV-009 the rollback tripwire cannot observe the legacy path, INV-012 the task-builder default POST gate is a blocking skill-path consumer the consensus omitted, INV-013 prospective audit keys are model-written and would repeat the failure that broke the recount) and 7 MEDIUM. The orchestrator verified INV-012, INV-009, INV-001 and INV-004 in the files before recording. Two further facts the debate had not stated: the `--compare` list at `SKILL.md:695` hard-codes three card files, and a reported probe-artifact gap at two cards (13 of 23 three-card runs against 0 of 6 two-card runs, or 14 of 26 against 2 of 9). CORRECTION recorded after the refactor-plan review: that gap was a path-counting artifact (the probe artifact is also kept at `adversarial/adversarial/invariant-probe.md`); counting both paths it is 20 of 23 three-card runs against 5 of 6 two-card runs, so the gap is withdrawn and INV-008 stands only on its structural point (the "<10% diff" debate-skip rule).

## Taxonomy Coverage Gate (AD-5)

| Level | Diff points addressed in the debate | Covered |
|-------|-------------------------------------|---------|
| L1 surface | S-001, S-004 | yes |
| L2 structural | S-002, S-005, S-006, C-001, C-002, C-003, C-008..C-016, X-001..X-004, A-001 | yes |
| L3 state mechanics | S-003, C-004, C-005, C-006, C-007, A-002, A-003, A-004 (and INV-001, INV-006, INV-009 from the probe) | yes |

All three levels have coverage above zero, so no forced round was needed.

## Scoring Matrix

Winner per diff point = the superior approach on which the two advocates' FINAL positions (Round 2 where revised, Round 1 otherwise) agree. "MERGE" means both advocates concluded the right answer keeps parts of both. "UNRESOLVED" means the advocates' final positions differ.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | MERGE (tie) | 95% | Same seven H2 sections in the same order |
| S-002 | UNRESOLVED | 50% | A: MERGE 55; B: V1 60 (stance-organised evidence vs subject-organised) |
| S-003 | Variant A | 62% | Invariants-preserved table is the better correctness artifact (both agree), though verified for the resolver, not the legacy path |
| S-004 | Variant B | 65% | Weakest point stated first |
| S-005 | MERGE | 62% | B's Phase 0 and pre-registration kept; Phase 1 empty on the recount |
| S-006 | UNRESOLVED | 50% | A: V1 60; B: MERGE 60 (A names concrete test edits; B found nothing pins the pre-filter; neither measures quality) |
| C-001 | MERGE | 65% | A-min default of 2 on the skill path plus B's prospective keys |
| C-002 | Variant B | 93% | Flag decisive in 0-1 of 39; rows 4 and 6 drive spend (orchestrator and both advocates reproduced) |
| C-003 | UNRESOLVED | 50% | A: MERGE 55; B: V2 60; both agree E2 cannot be read as the Tier 2 ceiling |
| C-004 | MERGE | 60% | N=2 loses PASS-eligible slack; re-dispatch is prose; executor-keyed templates deferred |
| C-005 | MERGE | 60% | Dry run reproduced by both; on the skill path the legacy rotation restores N, so duo templates wait for Stage 3 |
| C-006 | MERGE | 55% | Clamp 4 versus cap 3 is real but belongs to C17 (post-gate path) |
| C-007 | Variant B | 72% | Shadow stays at 3, so the exit-gate edit is not needed now; A's edit is right only when the count changes |
| C-008 | MERGE | 78% | `telemetry:` keys and `tier_decision.yaml` audit keys are complementary |
| C-009 | MERGE | 65% | Symmetric pre-registered rule with an owner-set margin; B's 10-point margin was invented |
| C-010 | UNRESOLVED | 50% | A: MERGE 75; B: V2 65; both agree A9 overstated |
| C-011 | MERGE | 77% | A-min leaves the engine and blocking post gate alone; probe finding INV-012 reopens the task-builder gate |
| C-012 | Variant A | 60% | B's E-6 counterexample refuted by the run's own calibration card (C 0.68); the probe-found blocker stays an observation |
| C-013 | UNRESOLVED | 50% | A: V1 70; B: MERGE 55; neither variant pins behaviour and A-min needs a drift pin |
| C-014 | Variant A | 62% | Saving on about 26 of 38 runs in calls versus B's near zero; tokens unmeasured |
| C-015 | MERGE | 80% | Both leave the four-reviewer default out of scope |
| C-016 | UNRESOLVED | 50% | A: MERGE 85; B: V2 60 |
| X-001 | Variant B | 95% | Reproduced by script and by hand; B's own 1-certain-at-most-5 also overstated |
| X-002 | Variant B | 80% | A9 overstated: text revert and `--tier 2` kill switch |
| X-003 | Variant B | 88% | G1 cannot open on recorded data; B today is Option C plus instrumentation |
| X-004 | MERGE | 90% | Both the orchestrator's 4 and B's 5 are too high; files support 0 certain, at most 1 |
| A-001 | MERGE | 70% | QUALIFY by both: fine for row attribution, not for future load |
| A-002 | MERGE | 75% | No trade-off threshold exists; an owner decision |
| A-003 | Variant A | 72% | REJECT by both: the blocker came from the probe, which favours cutting width over gating the tier; the structural debate-skip risk at N=2 (INV-008; the empirical probe-absence gap first reported was withdrawn as a counting artifact) qualifies it |
| A-004 | MERGE | 75% | Independent in code; pilot must pin arms and shadow at 3 (INV-010) |

Tally: Variant A won 4 points (S-003, C-012, C-014, A-003); Variant B won 6 (S-004, C-002, C-007, X-001, X-002, X-003); MERGE 14; UNRESOLVED 6 (S-002, S-006, C-003, C-010, C-013, C-016).

## Convergence Assessment

- Points resolved: 24 of 30 (an advocate pair agreed on the superior approach on 24 points; 6 are UNRESOLVED)
- Alignment: 24 / 30 = 0.80
- Threshold: 80%
- Raw diff-point convergence: **0.80, at the threshold**
- Taxonomy coverage gate: passed (L1, L2, L3 all covered)
- Invariant-probe gate: **BLOCKED**: 3 HIGH-severity UNADDRESSED invariants (INV-009, INV-012, INV-013)
- Status: **BLOCKED_BY_INVARIANTS** (agreement at the threshold, but HIGH UNADDRESSED invariants block convergence; depth `standard` has no Round 3, so they are carried forward, not argued out)
- Unresolved points: S-002, S-006, C-003, C-010, C-013, C-016
- Sycophancy note: both advocates retracted their own headline figure and ended on nearly the same merge after one rebuttal round. The probe was told to attack the consensus, and it found three HIGH gaps the advocates had missed, so the convergence is not treated as proof of correctness.
