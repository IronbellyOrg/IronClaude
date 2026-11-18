# Refactoring Plan: Merge into Base (Variant B)

<!-- Drafted by the debate-orchestrator in appended sections (overview and changes first, then rejected changes, risk, invariants, review status). A separate reviewer agent checks the draft before the merge executor runs; the review result and every fix applied are recorded in "Review Status". -->

## Overview
- Base: Variant B (Proposal B, Option B: fix the rubric first, keep the cap at 3, decide the count after H-A), `adversarial/variant-2-original.md`
- Incorporating strengths from: Variant A (Proposal A, two reviewers by default), `adversarial/variant-1-original.md`
- Inputs: `debate-transcript.md` (Rounds 1 and 2, scoring matrix, convergence), `invariant-probe.md` (14 findings, 3 HIGH UNADDRESSED), `base-selection.md`
- Planned changes: 15 (Changes 1-14 below plus Change 15 in "Amendments after review"); changes NOT made: 11 plus 1 added by the amendments
- Selection record (executor must log this in the merge log): base B won by 0.0061 (A 0.9194, B 0.9256), inside the 5 percent band; the tiebreaker level 1 (debate points won, B 6 to A 4) decided it; B stays ahead in every sensitivity case in `base-selection.md`; the advocates' own Round 2 consensus favoured "A-min" as the base, and the protocol chose B by score, so the merged document replaces five of B's headline parts (figure, E-6, Phase 1, Phase 0, count rule) while preserving B's structure and the items listed under "Preserved from the base unchanged" in the amendments.
- Risk level (overall): Medium, with one High item. The merge rewrites B's central claims (the escalation figure and the E-6 reading) and adds Decision D-1, an owner-gated change to the reviewer default (Change 5, risk High). The merge itself edits only a proposal document, but the proposal it produces specifies one small read-only script (Change 4) and about nine prose edits in five files (Change 6); no behaviour changes until the owner accepts D-1.
- Merge rule for open items: every UNRESOLVED diff point (S-002, S-006, C-003, C-010, C-013, C-016) and every UNADDRESSED invariant (INV-001, -002, -004, -006, -008, -009, -010, -011, -012, -013) must appear in a section of the merged proposal named "Open decisions and unresolved conflicts"; none may be dropped, softened or marked resolved.
- Figure rule: the merged document states the escalation figure ONLY as "the parsed-sparse flag was set in 35 of 39 recorded non-shadow runs and was decisive in 0 certain and at most 1" with its caveats (model-written fields; only 7 of 39 files record `S_domains`). It must not repeat "35 of 39 escalate because of the flag", "34 by the pre-filter", "1 certain, at most 5" or "13 percent".

## Planned Changes

### Change 1: Correct the escalation figure everywhere in the base (fixes B, per C-002, X-001, X-004)
- **Source**: Debate Rounds 1 and 2; orchestrator recount (`quant_score`-independent; `recount_tier_decision.py` plus the five ambiguous runs read in full)
- **Target**: Base sections "Why Tier 2 is almost always paid" (E-5), "The weakest point, stated first", Risks R1 and R9, the "Cost" paragraph "What B saves", and the "Where B sits" paragraph
- **Approach**: replace
- **Rationale**: Debate C-002 (V2, 93 percent), X-001 (V2, 95 percent), X-004 (MERGE, 90 percent). Files: 39 non-shadow `tier_decision.yaml`, 38 Tier 2, 35 flagged, 34 flagged and Tier 2; 29 of the 34 have a recorded escalate row 4, 5 or 6; of the other five, one (`fixTheScIssueWor`) has Tier 1 calibrated C 0.68 (`reflection-card.yaml`), two have Tier 1 C 0.75 and 0.53 (`REPORT.md:6`), one records `S_domains=3` in its own text, and one (`planTheRealBound-...rerun`) is undetermined. Decisive: 0 certain, at most 1
- **Integration point**: keep the E-5 table but add a column "also fails Tier 1 stop by" (row 6 via calibrated C, row 4 via `S_domains`) and replace the sentence "1 for certain and at most 5 of 39 (13 percent)" with the figure rule in the Overview
- **Risk**: Medium (rewrites the base's headline claim; wrong wording would re-introduce an overstatement). Rollback: revert to the base text and keep the correction note.

### Change 2: Recast E-6 as an observation about the probe, not a flag counterexample (fixes B, per C-012, A-003)
- **Source**: Debate Rounds 1 and 2; `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/{reflection-card.yaml, t1-card.md, adversarial/invariant-probe.md}`
- **Target**: Base E-6 and the "weakest point" consequence 1
- **Approach**: replace
- **Rationale**: the run escalates through row 6 (calibrated C 0.68) with or without the flag; M-13 came from the Round 2.5 invariant probe (INV-001 of that run), not from a reviewer card; the Tier 1 card, six reviewer card files and three variant originals have zero hits for "untracked", "git status" and "ls-files". It shows the probe step has value; it does not show a third reviewer has value and does not argue against a flag change
- **Integration point**: keep the file names and the M-13 quote; delete "clear-cut" and "counterexample"; add the sentence that the probe, not a reviewer, found M-13 and that this is one run
- **Risk**: Low (a correction of a factual reading).

### Change 3: Demote Phase 1 (flag advisory) from the committed plan to a conditional item (per X-003, C-001)
- **Source**: Debate Round 2 (both advocates); base G1 text
- **Target**: Base "The three phases", Gate G1, Phase 1 cost row, tests N3 and N4
- **Approach**: restructure
- **Rationale**: the flag was decisive in at most 1 of 39 runs and G1 has no candidates on recorded data; the base's own text says its result is "closer to Option C". Phase 1 stays only as "reopen when the prospective keys (Change 4) show at least three runs where `tier_without_flag` is 1 and the Tier 1 card was calibrated at or above 0.85"
- **Integration point**: move Phase 1 under "Conditional items"; delete N3 and N4 from the committed test list and keep them as the tests that would ship with the conditional item
- **Risk**: Low (removes scope; records the trigger for reopening).

### Change 4: Replace Phase 0 (retrospective replay) with prospective audit keys plus a deterministic recompute (from A's Round 2 correction and B's Round 2; closes INV-013)
- **Source**: Debate Round 2 (A: "replay must not read `tier_decision.yaml` alone"; B: "aim the keys at rows 4 and 6"); probe INV-013
- **Target**: Base "Contract and audit fields", "CLI surface" (`scripts/reflect_tier_replay.py`), tests N1 and N2, Phase 0 cost row
- **Approach**: replace
- **Rationale**: the retrospective recount is already done, so the replay script and N1/N2 re-derive a known number and N2's hard-coded counts are wrong. The H-A strata (MR:540) need decision-time values for the rows that drive 27 of 39 runs. Because `first match wins` (`SKILL.md:427`) hides rows that also match, the keys must record all matching rows
- **Integration point**: audit-only keys in `tier_decision.yaml` (precedent `SKILL.md:469`): `matching_rows: [..]`, `calibrated_C_t1`, `S_domains_basis` (count and the paths used), `tier_without_flag`. Add one small read-only check next to `scripts/reflect_shadow_exit.py` that recomputes the first-match row from the recorded inputs and prints "not evaluable" when an input is missing, so a model-written wrong row (the E-6 run recorded row 8 against its own card C 0.68) is detected instead of trusted
- **Risk**: Medium (new script; model-written inputs can still be wrong, so the check reports disagreement, it does not repair it).

### Change 5: Replace the "count must wait" premise with an owner-gated reviewer default (from A, A-min; per C-001, C-014, C-011)
- **Source**: Variant A Design and Round 2 "A-min"; debate C-001 (MERGE 65), C-014 (V1 62), C-011 (MERGE 77)
- **Target**: Base "What the design decides" row "Default reviewer count" and the paragraph "Count decision"
- **Approach**: replace
- **Rationale**: nine of the 38 recorded Tier 2 runs already ran two cards (executor exclusion 2, deliberate to keep the calibrator disjoint 1, missing card 1, unstated 5), so "the count must wait" is not true of production. What cannot be known before an arm exists is whether two matches three on recall inside reflect. Present A-min as Decision D-1 for the owner: change only the skill-path default (`SKILL.md:86`, `commands/reflect.md:100`, the section 7.1 table "(default)" label, the "restore N=3" sentence at `SKILL.md:658` and its twin at `refs/reviewer-spec.md:102`) from 3 to 2, keep `--reviewers 3` and `--strategy enterprise` as opt-ins, keep the code-engine default (`commands.py:270-274`, `config.py:264`), the clamp (`config.py:335`) and the exit gate (`scripts/reflect_shadow_exit.py:244-245`) unchanged, leave the invariant probe, debate, calibrator and evidence validator untouched, and keep the adversarial call at `--depth standard`
- **Integration point**: new section "Decision D-1: skill-path default of two reviewers (owner decision before H-A)" with the conditions in Changes 6-9; the saving is stated in calls (one reviewer, one calibrator, one debate variant) on the roughly 26 of 38 recorded runs that ran three cards, not in tokens
- **Risk**: High (quality at two reviewers inside reflect is unmeasured; E2 cannot be read as the Tier 2 ceiling). The change is owner-gated and carries a tripwire (Change 8).

### Change 6: Add the coupled-edit checklist and the shadow pin as conditions of D-1 (from the Round 2 verification and probe INV-001, INV-004)
- **Source**: Debate Round 2 B verification (a); probe INV-001, INV-004
- **Target**: new subsection of D-1 "Every place that states the count"
- **Approach**: append
- **Rationale**: a skill default of 2 against the 3-slot `@reflect-pre` makes shadow parity false (`scripts/reflect_shadow_exit.py:139-142`, `:173-174`) and, worse, `manifest.py:314-315` aborts when resolved exceeds requested, so a shadow run that sees requested 2 is lost. The pin must therefore be a conditional default in the flag definition ("default 2; 3 when the effective engine is shadow", evaluated at Wave 3A after the engine decision D2, `SKILL.md:318`) plus `SKILL.md:340`. The adversarial call at `SKILL.md:695` hard-codes three card files and must name only the cards that exist (or `SKILL.md:1466` routes a healthy two-card run to `single-reviewer-fallback`)
- **Integration point**: a table of sites with file:line: `SKILL.md:86, :240, :340, :654-659, :681, :695, :987, :1375`; `refs/input-resolution.md:18, :92`; `refs/reviewer-spec.md:27, :97, :102`; `commands/reflect.md:100, :221`; `task-builder/SKILL.md:2229`; docs `docs/guides/reflect-cli-tools-guide.md:140` and `docs/testing/v5.0.0/user/D12-reflect.md:63`; `models.py:91-92`; tests `tests/cli/reflect/test_shadow_skill_contract.py:124,140`. Plus one drift-pin test over the default text, since no test pins it today
- **Risk**: Medium (about nine edits in five files; a missed site reproduces INV-004).

### Change 7: Name the task-builder default POST gate as a blocking consumer and decide it (closes the content of INV-012; also corrects base E-9)
- **Source**: Probe INV-012 (orchestrator-verified at `src/superclaude/skills/task-builder/SKILL.md:2217-2236`)
- **Target**: Base "Who is exposed to the rubric" (E-9) and D-1 conditions
- **Approach**: insert
- **Rationale**: the default `reflect_post_mode: skill` gate invokes `Skill sc-reflect-protocol --mode post --remediate --depth {DEPTH}` with no `--reviewers`, and an unresolved Regression or unauthorized Drift halts the task, so it is blocking. D-1 would move it to two reviewers silently
- **Integration point**: D-1 states two options for the owner: (a) the runner passes `--reviewers 3` explicitly, keeping that gate at three; (b) accept two for that gate and record it. The merged document also corrects E-9 to list the user-run commit gate and this gate beside the advisory consumers
- **Risk**: Medium (a blocking path; decision is the owner's).

### Change 8: Restate the rollback tripwire on observable proxies (closes the content of INV-009; from A Round 2 and B Round 2 QUALIFY)
- **Source**: Debate Round 2 (A: revert if shortfall above 10 percent over the first 30 two-reviewer runs or median convergence below 0.80; B: a tripwire, not a test; the convergence half is a poor trigger); probe INV-009
- **Target**: D-1 "Rollback" and base Risks
- **Approach**: insert
- **Rationale**: the legacy path writes no `panel/manifest.json` (14 manifests against 91 `pre-*` directories) and shadow is pinned at 3, so `panel_shortfall` and `reviewers_complete` never see an N=2 legacy run. The observable proxies are `merge_method: single-reviewer-fallback`, `len(reviewer_cards)` against the requested count, convergence and probe-artifact presence (defined over BOTH `adversarial/invariant-probe.md` and `adversarial/adversarial/invariant-probe.md`; a single-path check mis-counted it in this debate). At about 39 runs over five months, 30 two-reviewer runs take about four months
- **Integration point**: tripwire stated on those proxies, numbers left to the owner (suggested start: revert on any two `single-reviewer-fallback` in the first 10 two-reviewer runs, or a probe-artifact rate below the three-card rate by more than the owner's margin); the shortfall half only catches a rate of about 20 percent or more at n=30; state that it is a tripwire, not a test, and that a controlled pilot arm is the only measurement of recall
- **Risk**: Medium.

### Change 9: Record requested, resolved and source separately; add strata that keep the pilot arms clean (closes INV-002, INV-010)
- **Source**: Probe INV-002, INV-010; variant A telemetry (`reviewers_default_applied`, `panel_shortfall`)
- **Target**: Base "Contract and audit fields"
- **Approach**: replace A's single boolean with three audit fields
- **Rationale**: a boolean `reviewers_default_applied` breaks under `--strategy enterprise` (count 3, default applied), under an explicit `--reviewers 3` clamped to 2 by D5, and under the conditional shadow default
- **Integration point**: `reviewers_requested`, `reviewers_resolved`, `reviewers_source: default|flag|enterprise|shadow-pin|clamp`, plus `executor_exclusion_degraded`, `anchor_replaced`, `depth` and `calibrator_diversity` as strata for the H-A arms
- **Risk**: Low.

### Change 10: Replace B's count rule with a symmetric pre-registered rule and state the pilot's limits (per C-009, A-004; from Round 2 A and B)
- **Source**: Base "Count decision (step 6)"; Round 2 (both advocates)
- **Target**: Base "Count decision"
- **Approach**: replace
- **Rationale**: B's 10-point margin was "my own invention". Arms: T1, T2 with 2 reviewers, T2 with 3 reviewers, each pinned explicitly so a shipped default cannot shift what H-A measures (A-004); the margin is an owner-set parameter; the rule states the inconclusive outcome in advance (incumbent stays) and a minimum n (E2 at n=4-6 could not separate panels, p 0.54-1.0); cost of the pilot stays at the base's figures (1.30M to 2.62M claude tokens for the pilot, grading unpriced, no owner, G-59)
- **Integration point**: replaces steps 1-4 of the base count decision
- **Risk**: Medium (a pilot that is never funded leaves the count undecided, which the base already states in R8).

### Change 11: Add the invariants-preserved table and the "does not claim" list (from A; per S-003, U-005)
- **Source**: Variant A Correctness sections 1 and 3
- **Target**: Base "Correctness argument"
- **Approach**: append
- **Rationale**: S-003 (V1 62 percent): the better correctness artifact. Scope it honestly: verified for the resolver (`panel.py`), not for the legacy skill path that actually dispatches, where the N=2 post-removal sentence at `SKILL.md:658` covers only an executor of sonnet
- **Integration point**: a seven-row table (anchor never dropped; executor class not a reviewer class; T2 stays T2; a Regression debated by at least two reviewers; contract 1.8.0 stable keys; cap of three; failure is closed), each row with the file:line and a column "verified for" (resolver / legacy skill path / not verified)
- **Risk**: Low.

### Change 12: Record the calibrator-disjointness argument, the spec-body single point of failure and the probe-presence gap as quality arguments with their limits (from Round 2; INV-003, INV-006, INV-008)
- **Source**: Round 2 A (new evidence 2) and B (d); probe INV-003, INV-006, INV-008
- **Target**: D-1 "Evidence" and "What this does not show"
- **Approach**: insert
- **Rationale**: three-card runs are mostly `calibrator_diversity: degraded` (22 of 25 tagged on the second count; 23 of 26 on the first) while two-card runs are mostly `full` (6 of 8); this is a guarantee argument, not a recall argument, and with an opus executor the calibrator still collides with the executor so `full` overstates the partition. Under UC-1 only the qa persona receives the spec body (`refs/reviewer-spec.md:55-57`); at N=2 a failed qa card leaves a spec-blind survivor and DEGRADED. The probe artifact appeared absent at two cards on a first count (13 of 23 three-card runs against 0 of 6 two-card runs), but that count missed the nested path `adversarial/adversarial/invariant-probe.md`; counting both paths it is 20 of 23 against 5 of 6, so no gap is claimed (the one two-card run without a probe at either path, `closeIronbellyOr-20261104084538`, is missing its reviewer-2 card)
- **Integration point**: limits stated beside each argument; a fourth reviewer class in the pool is listed as an open alternative to cutting N
- **Risk**: Low.

### Change 13: Add the N=2 test list and say which failure modes only a pilot can detect (per C-013, S-006; closes the content of INV-014)
- **Source**: Variant A test section; Round 2 A (3) and B
- **Target**: Base "Test coverage needed"
- **Approach**: append
- **Rationale**: tests that can exist: an N=2 mirror of `test_i5` (single-reviewer-fallback, DEGRADED, exit 11); an EV-1 test for a two-resolved run with one card; a drift pin over the default text in the sites of Change 6; a post-hoc lint on run artifacts (resolved count equals requested count unless `executor_exclusion_degraded` is set); a skill-text pin that the conditional shadow default and the `--compare` rule are present. Detectable only by a pilot or telemetry: recall at 2 versus 3, convergence behaviour with two variants, DEGRADED rate, whether the orchestrator picks the right rotation row
- **Integration point**: two tables, "automated" and "measurement only"; note that the pins test prose, not model behaviour (A-007)
- **Risk**: Low.

### Change 14: Add the "Open decisions and unresolved conflicts" section (mandatory)
- **Source**: `debate-transcript.md` Convergence Assessment; `invariant-probe.md`
- **Target**: new final section of the merged proposal
- **Approach**: append
- **Rationale**: the protocol forbids hiding what the debate did not settle
- **Integration point**: three tables. (1) Unresolved diff points with both advocates' final positions: S-002, S-006, C-003, C-010, C-013, C-016. (2) UNADDRESSED invariants with severity and the change that addresses its content, if any: HIGH INV-009 (Change 8), INV-012 (Change 7), INV-013 (Change 4); MEDIUM INV-001 (Change 6), INV-002 (Change 9), INV-004 (Change 6), INV-006 (Change 12), INV-008 (Change 8, 12), INV-010 (Change 9), INV-011 (Change 5, 6). A change that records a fix in the document is NOT a resolution: each row keeps status UNADDRESSED in the debate sense until the owner accepts the condition. (3) Owner decisions: accept D-1 before H-A; the tripwire numbers; the task-builder gate option; the H-A pilot owner (G-59); who closes G-67 (C17); whether the document-loop `default` (4) and `live7` (7) follow (C03).
- **Risk**: Low.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach / Rejected Item | Rationale for Keeping the Base or Dropping |
|------------|-----------------------------------|--------------------------------------------|
| C-001 / C-011 | A: change the code-engine default (`commands.py:270-274`, `config.py:264`) from 3 to 2 | The post gate runs `superclaude reflect run ... --depth deep` with no `--reviewers` (`sc-tasklist-protocol/SKILL.md:1162`) and would drop to two on evidence from a non-blocking, no-calibrator, no-debate setting; both advocates conceded the engine default should stay 3 until a pilot arm exists (MERGE 77 percent) |
| C-006 | A: close G-67 by changing the clamp `max(2, min(4, n))` to `min(3, ...)` in this change | The clamp is on the post-gate path owned by C17; recorded as an open item, not changed here (MERGE 55 percent) |
| C-007 | A: edit `reflect_shadow_exit.py:244-245` and its "2-of-3" label now | Shadow stays pinned at 3, so the rule keeps its meaning; edit only when a shadow arm runs at two (V2 72 percent) |
| C-004 / C-005 | A: four new duo template files and executor-keyed shadow template selection now | On the legacy skill path the rotation prose restores N after exclusion, which removes the bare-two-slot failure (R3); the duo templates and the three-row executor table are parked for the Stage 3 panel engine (MERGE 60 percent) |
| C-002 / X-001 | A1, A8 and the section 2 table "35 of 39" / "up to 34-35" | False on the files; retracted by advocate A (V2 93 and 95 percent) |
| X-002 | A9 "cannot be rolled back by data alone" | Overstated: a skill-text revert and the `--tier 2` kill switch undo B's change (V2 80 percent) |
| C-001 | B Phase 1 (flag advisory) as committed scope | Decisive in at most 1 of 39 runs; G1 has no candidates; kept only as a conditional item (Change 3) |
| S-005 | B Phase 0 retrospective replay script and tests N1, N2 | The recount is done; N2's hard-coded counts are wrong; replaced by prospective keys plus a recompute check (Change 4) |
| C-009 | B's 10-point count margin | The advocate called it "my own invention"; replaced by an owner-set margin (Change 10) |
| C-012 | B's E-6 "clear-cut flag-only counterexample" | Refuted by the run's own calibration card (C 0.68) (Change 2) |
| C-014 | A's saving stated as "38 of 39 runs" | The saving applies to roughly 26 of 38 runs (9 already ran two cards, 3 have no card) and is counted in calls, not tokens |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Medium | A residual overstatement of the escalation figure re-enters the merged document | Revert the figure paragraph to the Overview figure rule |
| 2 | Low | E-6 read wrongly | Restore the base sentence with the correction note |
| 3 | Low | Phase 1 scope loss is questioned | Restore Phase 1 as a conditional item |
| 4 | Medium | The recompute check mis-parses `tier_decision.yaml` and reports false disagreements | Remove the script; keep the keys |
| 5 | High | Owner accepts a default of two on thin evidence; quality at N=2 unmeasured | Revert the default text (a prose edit in the sites of Change 6); keep `--reviewers 3` |
| 6 | Medium | A missed site reproduces INV-004; a shadow run is lost to the manifest guard | Pin shadow at 3 via the explicit flag as a stopgap; add the missing site |
| 7 | Medium | The blocking task-builder gate silently drops to two reviewers | The runner passes `--reviewers 3` explicitly |
| 8 | Medium | The tripwire cannot observe the legacy path | State the proxies; fall back to a controlled pilot arm |
| 9 | Low | Strata ambiguous | Add the missing stratum |
| 10 | Medium | The pilot is never funded; count stays undecided | The incumbent (two under D-1, three if D-1 is not accepted) stays |
| 11 | Low | Table claims more than was verified | Edit the "verified for" column |
| 12 | Low | Disjointness read as a recall argument | Strike the sentence |
| 13 | Low | Pins test prose only | Mark as prose pins |
| 14 | Low | An open item is dropped | Re-run the coverage check in the merge log |

## Invariant and Open-Item Coverage Check (for the merge executor and the reviewer)

| Item | Where carried | Must stay visible as |
|------|---------------|----------------------|
| INV-009 (HIGH) | Change 8, Change 14 | UNADDRESSED until the owner accepts the proxy tripwire |
| INV-012 (HIGH) | Change 7, Change 14 | UNADDRESSED until the owner picks option (a) or (b) |
| INV-013 (HIGH) | Change 4, Change 14 | UNADDRESSED until the recompute check exists |
| INV-001, -002, -004, -006, -008, -010, -011 (MEDIUM) | Changes 5, 6, 8, 9, 12 and 14 | UNADDRESSED (warnings) |
| S-002, S-006, C-003, C-010, C-013, C-016 | Change 14 table 1 | UNRESOLVED, with both advocates' final positions |
| Owner decisions | Change 14 table 3 | Open |

## Amendments After Review (binding; they supersede the Change text wherever they differ)

A separate reviewer agent (independent of the debate; verdict APPROVE-WITH-FIXES, 14 findings: 6 MAJOR, 8 MINOR) checked this plan against the debate artifacts and the repository. Its fact-check confirmed the 39 / 38 / 35 / 34 counts, the 29 of 34 split, the `fixTheScIssueWor` C 0.68 reading, the REPORT.md confidences, the nine two-card runs, 14 manifests against 91 directories and every cited `SKILL.md` and `refs/` line except `SKILL.md:316`. The orchestrator re-verified the two items that changed a recorded fact before accepting them: (1) the probe-presence counts were a path-counting artifact (verified: 20 of 23 three-card and 5 of 6 two-card runs have the artifact when both `adversarial/` and `adversarial/adversarial/` are searched); (2) D2 is at `SKILL.md:318`, not `:316` (verified). The in-place fixes for those two are already made in this file, in `invariant-probe.md` and in `debate-transcript.md`. The remaining fixes are below; each is numbered to the reviewer's finding.

### A-1 (finding 1): complete the target lists
- Change 1 also targets base Correctness section 1 (`variant-2-original.md:135`, "at most 5 of 39").
- Change 3 also targets the Design rows at `:19-21`, data-flow steps 2-4 (`:49-51`), Correctness sections 1, 2 and 4, risks R1, R2, R4 and R5 (`:166-170`) and the Phase 1 cost rows (`:211-212`).
- Change 5 also targets the base title (`:1`), "One-sentence position" (`:11`, "Do not touch the reviewer count now"), Correctness section 3 (`:139`), section 5 "Why the count must wait" (`:143-146`), R8 (`:173`, "count stays 3, the safe state") and "What B costs by waiting" (`:219`).
- Change 7 also targets Correctness section 4 (`:141`) and the consumer rows (`:38-40`) that say the blocking path has "no exposure".
- Final executor check on the merged file: no occurrence of "Phase 1" as committed scope, "count must wait", "stays 3" as the safe default, "at most 5", "13 percent", "1 certain" or "clear-cut".

### A-2 (finding 2) = Change 15: carry the floor rule and re-dispatch (U-002, C-004)
Add to Decision D-1 a risk item: with two reviewers one failed or invalid card leaves one, which is DEGRADED (`single-reviewer-fallback`, `src/superclaude/cli/reflect/contract.py:278-296`; code engine exit 11, `tests/cli/reflect/test_ensemble_stub_integration.py:251-277`); with three reviewers a 2-of-3 shortfall stays PASS-eligible (`tests/cli/reflect/test_verdict_mapping.py:572-580`). Evidence for the cost of no slack: E2 `ember + terra` -1.75 found, permutation p 0.029, because terra returned nothing (CR:294, CR:298). Mitigation as a prose-only rule: one bounded re-dispatch of a reviewer that returned nothing before degrading (the existing bounded re-ask for an invalid block is at `SKILL.md:343`); label it prose, since shadow13 and shadow15 skipped a stated step (variant A R2). Anchor the pair on the reliable-format class (sonnet, 0 of 15 blocks dropped, CR:427). Tests: the N=2 mirror of `test_i5` and the EV-1 test (Change 13).

### A-3 (finding 3): probe-presence correction
Change 8's proxy and Change 12's argument use the corrected count only (20 of 23 and 5 of 6, both paths). Change 12 must not cite "0 of 6" or "13 of 23". INV-008 stays UNADDRESSED MEDIUM on its structural point (the "<10% diff" debate-skip rule can drop Round 2.5 at two variants); no recorded run shows it.

### A-4 (finding 4): specify Change 4 fully
- Inputs the recompute reads, in order: `reflection-card.yaml` `C:` or `artifacts/t1-calibration.yaml` for the blind-calibrated Tier 1 confidence (existing keys vary: `calibrated_confidence_t1` in 1 file, `calibrated_confidence` in 2, `confidence_calibrated` in 5, so the check reads the card, not only `tier_decision.yaml`); `t1-card.md` for `S_domains` and `S_dev_density`; `artifacts/input-snapshot.yaml` for path-based domain counting (code, tests, docs); everything else is "not evaluable".
- Script: a small read-only check beside `scripts/reflect_shadow_exit.py` (proposed name `scripts/reflect_tier_recompute.py`; the name is a proposal).
- Replacement tests for B's N1 and N2: a fixture with a recorded row 8 and a card C of 0.68 must report "disagree"; a fixture missing an input must report "not evaluable" and never count as decisive; a skip-if-absent test over `.dev/reflect` asserting only the derivable counts (39 files, 38 Tier 2, 35 flagged, 34 flagged and Tier 2) and that the `fixTheScIssueWor` run is classified not decisive.
- Fate of B's `sparse_flag_decisive` and `escalation_path` keys: keep both as proposed audit keys (G1 in the conditional item and B's R4 and N5 pilot strata use them), computed by the same recompute; `tier_without_flag` is derived from them.
- Key names `matching_rows`, `calibrated_C_t1`, `S_domains_basis` and `tier_without_flag` are PROPOSED names, not existing keys.

### A-5 (finding 5): Change 6 site table needs an action column and corrected citations
Action column: EDIT for the skill-path default sites (`SKILL.md:86, :240, :340, :654-659` (the "restore N=3" sentence is at `:658`), `:681`, `:695`, `:987`, `:1375`; `refs/input-resolution.md:18, :92`; `refs/reviewer-spec.md:27, :97, :102`; `commands/reflect.md:100, :221`; `task-builder/SKILL.md:2229`). KEEP (they describe the engine default, which stays 3): `src/superclaude/cli/reflect/models.py:91-92` (path corrected), `docs/guides/reflect-cli-tools-guide.md:140`, `docs/testing/v5.0.0/user/D12-reflect.md:63`, `tests/cli/reflect/test_shadow_skill_contract.py:124,140` (shadow runs at 3). The "about nine edits in five files" count applies to the EDIT rows only; the table lists about 21 sites in 9 files. D2 is at `SKILL.md:318`. Cite `refs/reviewer-spec.md:55`, not `:55-57`, for the qa-only spec body.

### A-6 (finding 6): carry the strongest counter-evidence into D-1
D-1 gets a "What cuts against it" list: A's C1 to C5 (nothing measures two against three inside reflect; the only E2 size effect that survived testing is a 2 to 3 gain, second luna +0.83 control found, p 0.004 Welch, 0.048 permutation, CR:298, CR:366; the `ember + terra` failure; external guidance recommends three, W01 recommendation 9; the pre-filter is not the driver) and A's R5 (a class label may be served by one model, combo A3 collapsed every reviewer to sonnet, so with two reviewers a collapse removes all diversity; the dispatch gap must be closed before shipping, and D-1 should not ship ahead of the shadow path recording the served model). The merged document's "weakest point" section is rewritten as D-1's bet: nothing measures two against three reviewers inside reflect, and the third reviewer is given up on thin evidence; G1 is no longer the weakest point because Phase 1 is conditional.

### A-7 (finding 7): preserved from the base unchanged
E-8 (nothing pins the pre-filter), the exposure map (extended by Change 7), weakest-point-first placement, the recount method, R9 (documents repeating "34 of 38" get a pointer to the corrected recount), the E-1 to E-4 cap facts, the E-9/E-10 consumer and shadow-run facts (E-9 corrected by Change 7), the citation forms and the tag legend.

### A-8 (finding 8): label invented items
Proposed, not debated: the Change 3 reopen trigger (three runs where `tier_without_flag` is 1; the original "and C at least 0.85" is redundant, and G1's "none shows a Tier 2-only blocker" half is retained); the Change 4 key names; the Change 9 enumeration `default|flag|enterprise|shadow-pin|clamp`; the Change 8 numbers (already "suggested start"). The merged document labels each "proposed" or "owner parameter".

### A-9 (finding 9): Change 10 wording
Quote correctly: advocate B called the 10-point margin "the advocate's own invention" (`debate-transcript.md`, Round 1 concessions). Change 10 replaces only the margin and the arms of B's count rule (steps 1 and 4); B's step 2 (if H-A fails, the owner chooses between shrinking Tier 2 to two reviewers and tuning the rubric, MR:527) and step 3 (raising the cap above 3 stays closed unless H-A passes, MR:289) are kept.

### A-10 (finding 10): Change 11 "does not claim" list
Carry A's four items (`variant-1-original.md:139-142`): it does not claim two reviewers are as good as three inside reflect; it does not claim the saving is a third of a run (calls, not tokens; `ember + sonnet` 142,967 against `ember + luna + sonnet` 138,551); it does not claim the parsed-sparse pre-filter is right or wrong (a separate lever after H-A); it does not use the stale "sonnet alone gives most catches per token" line (pilot only, one run per package, before `source.md` shipped; D-57).

### A-11 (finding 11): recommendation inside D-1
D-1 recommends option (a) for the task-builder POST gate: the runner passes `--reviewers 3` explicitly, so the blocking completion gate keeps three reviewers until a pilot arm exists. This keeps the rejection of an engine-default change consistent (both blocking paths stay at three). Option (b) is listed as the alternative the owner may choose and record.

### A-12 (finding 12): wording
"Adds no code" in the Overview is already replaced (see Overview risk line). The overall risk is stated as Medium with one High item.

### A-13 (finding 13): placement
Change 9 is an insert (the base has no such field); the three fields go in `tier_decision.yaml` as audit-only keys for the rubric strata and under `telemetry:` in the contract for the panel strata (precedent `SKILL.md:349`, `:469`). The sections "Conditional items", "Decision D-1" (with subsections Rollback, Evidence, What cuts against it, What this does not show) and "Open decisions and unresolved conflicts" do not exist in B; the executor creates them as H2 sections after "Correctness argument" (D-1 and Conditional items) and at the end (Open decisions), keeping B's seven existing H2 sections in their order.

### A-14 (finding 14): label the calibrator counts
Calibrator disjointness: three-card runs 23 of 26 `degraded` (advocate A's Round 2 count) or 22 of 25 tagged (advocate B's Round 2 recount; one run carries both tags); two-card runs 6 of 8 tagged `full` (both counts). State both, name the sources, and state that this is a guarantee argument, not a recall argument.

### A-15: items the review found missing or weak in the coverage check
- A-001 (representativeness of the 39 runs): carried into "What this does not show": fine for row attribution, not for future load (35 of 39 flagged, many skill versions, only 4 of 38 decisions non-sparse per the pilot-design quota paragraph).
- A-002 (no stated trade-off threshold) and A-008 (E2 does not transfer): carried into D-1 as owner decisions and as "E2 cannot be read as the Tier 2 ceiling".
- INV-014 residual: the 0.80 convergence floor is enforced only on the engine and tasklist CLI arm (`sc-tasklist-protocol/SKILL.md:1171`), not on skill-mode gates; carried into the Change 13 "measurement only" table.
- Change 14 table 1 lists the advocates' final positions for each unresolved point, taken from the Scoring Matrix in `debate-transcript.md` (S-002: A MERGE 55 / B V1 60; S-006: A V1 60 / B MERGE 60; C-003: A MERGE 55 / B V2 60; C-010: A MERGE 75 / B V2 65; C-013: A V1 70 / B MERGE 55; C-016: A MERGE 85 / B V2 60).

## Review Status
- [x] Reviewed by a separate agent (independent of the debate): APPROVE-WITH-FIXES; all 14 findings applied above (two in place, twelve as binding amendments)
- [ ] User-approved (--interactive): not applicable (non-interactive run)
- Approved by: auto (after independent review and the fixes above); executor must apply Changes 1-15 and Amendments A-1 to A-15
- Approval timestamp: 2026-11-14 (orchestrator run)
