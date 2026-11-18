# Proposal A: Default to two reviewers now, with two-slot templates (fixed anchor plus one diverse reviewer), for C14

**Conflict:** C14, panel size versus cost (slug `panel-size-cost`), Option A of `synthesis/synth-04-options-conflicts.md` (the C-14 block, lines 893-956).
**Position argued:** the default panel for reflect Tier 2 and for every new consumer is two reviewers: one fixed anchor plus one reviewer of a different class. The cap of 3 stays as a ceiling that a caller opts into. The rubric lever (O-8) and the reviewer-count decision after H-A stay open and are measured afterwards; they are not what blocks this change.
**Checked at:** repository HEAD `792cf8c52` on branch `ironbelly/shadow-runs`. All code line numbers below were read at that HEAD.

**Citation key.** `R11 §12` means `research/11-evaluation-evidence.md` section 12 (same pattern for the other numbered files; `W01` is `research/web-01-panel-aggregation.md`). `CR:n` is line n of the E2 study's `COMBO-REPORT.md` read with `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/COMBO-REPORT.md`; E2 numbers come only from that commit. E2 headline numbers are the study's own report text; the raw `score.json` files were not re-aggregated (gaps log G-82), so they are supporting evidence, never the sole basis. Tags: [CODE] read in code at HEAD, [DATA] counted from files in this repository, [E2-DOC] E2 report text at the pinned commit, [EXT] external source with URL.


## Design

**What changes.** The default number of Tier 2 reviewers goes from three to two. Nothing else about the panel changes: the debate (sc-adversarial Mode A), the blind per-card calibrator, the evidence validator, contract 1.8.0 and the cap of three all stay. A caller that wants three asks for three.

### The core (shared panel resolver)

- **No schema change.** A two-slot template is already legal: exactly one `fixed` slot, total reviewers 1..8, slot keys `slot_id, tier, count, strategy, seed` (`src/superclaude/cli/review/panel.py:37-46, :229-248`; R04 §1) [CODE]. The reflect profile only caps the total at 3 (`panel.py:73`, `:130`, `:143`) [CODE], so it accepts two. `_REFLECT_MAX_REVIEWERS` stays 3: the cap is the ceiling, the default is what drops.
- **New template data, no new code in the resolver.** For each reflect lens that has a three-slot template today, add a two-slot default and one executor-keyed variant (see the table below). The existing three-slot files stay under their current ids as the explicit three-reviewer path, so nothing that pins them changes.
- **Persona by resolution order is unchanged** (analyzer first, qa second), which is the existing N=2 row of the rotation table (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:654`) [CODE].

The two-slot set for `pre` (the `post` set is the same shape):

| Executor class | Template | Reviewers (anthropic-only) | Status |
|---|---|---|---|
| unknown, or opus | `reflect-pre-duo`: `t1b` fixed + `t4` random | sonnet, haiku | new file |
| sonnet | `reflect-pre-x2`: `t4` fixed + `t1a` random | haiku, opus | exists (`review-panel.reflect-pre-x2.json`) |
| haiku | `reflect-pre-duo-xh`: `t1b` fixed + `t1a` random | sonnet, opus | new file |

I resolved the two new shapes in memory against the packaged tier file with `--strict-distinct` and each executor class (a throwaway Python call to `pnl.resolve`; nothing was written). Results: `t1b`+`t4` gives sonnet, haiku (executor none or opus), and for executor haiku gives only sonnet with `t4` skipped; `t1b`+`t1a` gives sonnet, opus (executor none or haiku), and for executor opus gives only sonnet with `t1a` skipped; executor sonnet exhausts `tier1b` in both. That is why the table is keyed on executor class: a bare two-slot template has no slack when the executor shares the second slot's class (see Risks, R3).

### Each consumer module

- **Reflect skill, Tier 2 (UC-1 and UC-2).** `--reviewers` defaults to 2 instead of 3 (`SKILL.md:86`, `src/superclaude/commands/reflect.md:100`). `--reviewers 3` and `--strategy enterprise` keep the current three-slot rotation. Shadow step 1 (`SKILL.md:340`) picks the template from the executor-class table above instead of always `@reflect-pre`. Rule D5 (`N_eff = min(--reviewers, alias count, 3)`, `SKILL.md:321`) and rule D3 (N=2 is the floor, `SKILL.md:319`) need no change.
- **Reflect code engine (`superclaude reflect run`, behind the tasklist post gate).** The Click default `--reviewers 3` becomes 2 (`src/superclaude/cli/reflect/commands.py:270-274`, mirrored by `config.py:264`). The clamp `max(2, min(4, n))` (`config.py:335`) becomes `max(2, min(3, n))`, which also resolves gap G-67 (the engine accepts 4 while constraint C11 says at most 3).
- **Shadow exit gate** (`scripts/reflect_shadow_exit.py:29, :244-245`). The shortfall rule `reviewers_resolved == 3 and reviewers_complete == 2` becomes `reviewers_complete < reviewers_resolved`, and the printed label stops saying "2-of-3".
- **New consumers (PR review finder, rf-qa replacement, tasklist review on the shared core).** They ship a two-slot template and no three-slot one. Two of them already have this shape: PR review reads exactly two reviewer sources (`REVIEWERS = ("augment", "codex")`, `src/superclaude/pr_submit/reviewers.py:41`) and reflect already runs `rf-qa` and `rf-qa-qualitative` as a pair (`SKILL.md:632-633`; R10 table row 38) [CODE].
- **Out of scope but flagged.** The #346 document loop's `default` template (four reviewers) and `live7` (seven) are not touched by this option as written. The E2 study measured exactly that family of consumer (spec review of tasklist plans), so its "no gain beyond three, more wrong blockers" result is in-setting there; shrinking `default` is a natural follow-on that the owner can take or leave without affecting this decision.

## How it works

**Data flow for one reflect Tier 2 run** (skill path, shadow engine today; the same shape applies when the resolver drives dispatch in Stage 3):

1. Wave 0 resolves the executor class (`SKILL.md:648-650`; unknown is fail-open). The orchestrator picks the template from the three-row table.
2. `superclaude review panel resolve --template @<picked> --run-id <id> --kind first --env anthropic-only --hard-exclude-class <executor> --strict-distinct` (the existing CLI, no new flag; `src/superclaude/cli/review/panel_cmd.py:18-108`) prints the resolution. It is stored unmodified as `panel/resolution.json`.
3. `review manifest advance --stage resolved` takes `{"reviewers_requested": 2, "reviewers_resolved": 2}` (`SKILL.md:338`). The manifest and the EV-1 lint already accept 2: `required = max(2, resolved)` (`src/superclaude/cli/reflect/panel_lint.py:268`).
4. Two reviewer cards come back. Each gets its own blind calibration (unchanged, `SKILL.md` section 11.3). The debate runs on two variants, then the evidence validator, then the contract writer.
5. **Floor rule.** If fewer than two cards complete, the run is the existing single-reviewer path: `merge_method: single-reviewer-fallback` and verdict DEGRADED (`src/superclaude/cli/reflect/contract.py:278-296`; code engine: `ensemble.py:772-773`) [CODE]. This is the one behaviour that gets stricter under A (see R2); the proposal adds one bounded re-dispatch of a failed reviewer before degrading.

**Contract fields.** No stable key of contract 1.8.0 changes: `reviewer_cards`, `reviewer_models`, `merge_method`, `tier_reached` carry two entries instead of three. New values go under `telemetry:` only (`SKILL.md:349`): `panel_shortfall` (bool, `reviewers_complete < reviewers_resolved`) next to the existing `panel_shortfall_2_of_3` (`SKILL.md:987`), and `reviewers_default_applied` (bool, true when the count came from the default and not from `--reviewers`), so a later comparison of 2 against 3 can separate the two groups.

**CLI surface.** One changed default (`--reviewers 2`), one new template family selected by `--template @reflect-pre-duo` and `@reflect-pre-duo-xh` (and the `post` pair), and no change to `panel resolve`, `panel validate`, `manifest` or `cluster`.

## Evidence

Every claim carries a research file and a code or data location. Claims the research files mark [UNVERIFIED] are not used to decide anything. Where evidence cuts against this proposal it is listed in the second half of this section, not left for the reader to find.

### What supports defaulting to two

**A1. The Tier 2 cost is paid on almost every run, so the per-run cost is the one that counts.** 38 of 39 recorded non-shadow pre runs selected Tier 2, 35 of them through the parsed-sparse pre-filter; the earlier figure "37 of 38, 34" (MR:142) is superseded by this recount with the same conclusion (R11 §12 table row 1; gaps D-59) [DATA, recount recorded in R11 §12 over `.dev/reflect/pre-*/artifacts/tier_decision.yaml`; not repeated here]. The pre-filter itself is `SKILL.md:284` and `:443` [CODE]. A saving per escalation is therefore a saving on nearly every run.

**A2. A reviewer is more than one call.** In the 15 combo runs the extractor lists 4 calibrator calls in each of the 12 B-E runs, 3 in A1 and A3, and 1 in A2 (`.dev/eval-workspaces/shadow-model-combos/results.md`, "Requested class -> served model" block, 2026-11-13) [DATA]. Calibration is per card (`SKILL.md` section 11.3; synth C06). Dropping a reviewer removes a reviewer call, a calibrator call and one variant from the debate. Limit stated plainly: cost is not recorded per reviewer (`modelUsage` is keyed by gateway alias, R08 line 398), so the saving can be counted in calls but not yet in tokens. Output tokens per whole 3-reviewer run were 185,086-367,381 for combos B-E (`results.md`; USD figures are estimates, "do not compare", `FINDINGS.md:37`).

**A3. In the one study that varied panel size with ground truth, the extra reviewer did not buy defects.** [E2-DOC, commit 4a22d74]
- Three-way permutation tests between all replicated panels: found, real blocking, wrong blockers and control are not significantly different (p 0.54-1.0); only tokens differ (p 0.002-0.009) (CR:381).
- Two-reviewer panels, n=4 each: `ember + sonnet` 2.50 of 14 found, `ember + luna` 2.25 (CR:315, CR:317). Three-reviewer panels: `ember + luna + luna` 1.83 (n=6, CR:331), `ember + luna + sonnet` 2.20 (n=5, CR:320), `haiku + luna + luna` 2.20 (n=5, CR:319), `ember + ember + luna` 1.60 (n=5, CR:333). Batch 11, `sonnet + luna + luna`, n=6: 2.33 (CR:424).
- The best-precision panel in the whole study is a two-reviewer panel: `ember + sonnet`, 0.25 wrong blockers (CR:368, CR:315).
- Past three it gets worse: `ember + ember + luna + luna` carries 4.75 wrong blockers (CR:332); `2x luna + 2x ember` has 2.75-3.25 more wrong blockers than every comparator (p 0.005-0.03, CR:298); "any panel of 5 reviewers (no gain for 2-4x the cost)" is on the do-not-use list (CR:369).
- The study's own conclusion is that reviewer choice is not the lever: "All panels sit at about 2-2.5 of 14, so the harness fixes (anchor limit, source.md path in the brief) remain the biggest lever" (CR:428; also CR:371).
- Summarised in R11 §6 and §12 items 2.

**A4. Two reviewers is a state the product already defines, tests and runs.** All [CODE] unless marked.
- Rotation table row `--reviewers 2`: sonnet, haiku; analyzer, qa (`SKILL.md:654`); "The N=2 minimum is hard" (`SKILL.md:658`); the flag is documented as 2-3 (`SKILL.md:86`, `commands/reflect.md:100`).
- Executor exclusion already degrades the panel to two (`SKILL.md:648`, `:658`; D3 at `SKILL.md:319`), and the anchor replacement template `reflect-pre-x2` is a two-reviewer panel, tested at `tests/review/test_review_reflect_templates.py:96-110`.
- The code engine clamps to a floor of 2 (`config.py:335`); `merge_method` is `adversarial` iff at least two reviewers succeed (`ensemble.py:772-773`; R13 line 295); the diversity gate needs only two distinct model ids (`src/superclaude/cli/reflect/_diversity.py:8-15`); a requested-2 run with 2 survivors carries no shortfall token (`tests/cli/reflect/test_ensemble_unit.py:598-604`).
- The EV-1 lint already uses `max(2, resolved)` (`panel_lint.py:268`), tested at `tests/cli/reflect/test_panel_contract_lint.py:284-292`.
- The rule that a Regression "must be debated by at least 2 reviewers" (`SKILL.md:433`, R05 line 81) is met by two.
- Wave 0 step 0.5 already routes "2 distinct models -> 2 reviewers" (`SKILL.md:232`; scope slice 03 line 67).
- The code engine's default of three fails closed whenever the model pool has two entries: `ModelPoolTooSmallError` for pool 2, reviewers 3 (`tests/cli/reflect/test_ensemble_unit.py:151-159`). A default of two does not.

**A5. The third reviewer has never been used as a spare in the recorded runs.** The Stage 2 exit report at HEAD shows `2-of-3 shortfalls: 0` over 13 counted shadow runs (R11 §8, output lines 264-268); all 15 combo runs ended `published` with 3 of 3 reviewers complete (`FINDINGS.md:3`). Caveat: these runs were not scored for quality, and the sample is 28 runs on one machine in two days.

**A6. The panel is already 2 distinct models in practice in the best-known 3-reviewer configuration.** Combo E, which `FINDINGS.md:13` calls "the study's best panel", had 3 reviewers but only 2 distinct served models (`results.md` E1-E3 rows: haiku, luna, luna; R04 §7.2). The diversity gate (A4) is satisfied by two.

**A7. Part of a third reviewer's input is thin by construction.** In UC-1 the spec body itself is injected only for the qa persona (`refs/reviewer-spec.md:55`), and the analyzer and refactorer see persona-filtered hunks, so "two of three reviewers are partially source-blind by construction" (R06 lines 77 and 95) [CODE]. A two-reviewer panel (analyzer, qa) keeps the one reviewer that receives the spec body.

**A8. The alternative lever removes the largest coverage step, this one removes the smallest.** Option B removes Tier 2 for up to 34-35 of the 38-39 recorded runs (R11 §12 item 4) and leaves a single-agent Tier 1 pass; how many of those would then be wrongly stopped is not measured (same row). Option A keeps at least two independent reviewers on every run that escalates.
- [EXT] A self-published corpus of 294 human-confirmed defects over 33 artifacts and fifteen model versions reports coverage of about 47 percent with one reviewer and about 72 percent with a second, "largest step", then diminishing returns after two to three, and recommends two or three reviewers: https://zenodo.org/records/21328807 (not peer reviewed, single-team corpus, read from the abstract only; reliability LOW to MEDIUM; W01 §3.4).
- [EXT] One preprint on judge panels found nine judges from seven families behaved like about two effective votes (Kish effective sample size 2.0 to 2.5) and the best single judge matched or beat the full panel: https://arxiv.org/html/2605.29800v1 (preprint; natural-language-inference tasks, not code or plan review; W01 §2.2). Relevance to this choice is that error correlation makes the third vote worth less than a third, not that two is optimal.
- The project's own bar for Tier 2 over Tier 1 is "at least 15 percentage points" of seeded-defect recall (MR:527, R11 §12 H-A row). That bar is the project's prior that Tier 2 may well be worth its cost; Option B bets against it for most plans, Option A does not.

**A9. A change of default is cheap to reverse and Option B is not.** The templates are data (R04 §10 point 1); the default is a flag value in four places (A4). Reverting is the same edit backwards. Option B changes escalation logic that is "TABLE-WIDE" for every UC-1 consumer, including workflow Wave 4 and tasklist Stage 10.5 (`SKILL.md:284, :443`; R09 §4.1) and so cannot be rolled back by data alone.

### What cuts against it (stated here, argued under Risks)

**C1. Nothing measures two against three reviewers inside reflect.** E2 never ran reflect, a calibrator or a debate, so "its ceiling cannot be read as the T2 ceiling" (R11 §12 item 3). H-A, the pilot that would measure Tier 2 against Tier 1, is "designed, not run" (MR:527; G-59 asks who owns the benchmark port). The synthesis rates this option's risk High for exactly this reason (synth-04 C-14 Option A table).

**C2. The only size effect that survived E2's tests points the other way.** "Second luna raises control found +0.83 (p 0.004 Welch, 0.048 permutation, baseline all zeros)" (CR:298; CR:366: "the only doubling effect that survives testing"). That compares `ember + luna` (control found 0.00, CR:317) with `ember + luna + luna` (0.83, CR:331). It is a 2 to 3 gain, on one package, for a repeated model. Two things limit its weight here: reflect's strict distinctness forbids a repeated model (R04 §8 table), so Option A cannot lose that exact effect because reflect cannot produce it; and `ember + sonnet` scored control 0.75 with two reviewers (CR:315), close to the three-reviewer values 0.80-0.83 (CR:320, CR:331). It is still the most honest evidence for a third reviewer and it is not refuted.

**C3. The two-reviewer panel that failed shows the cost of no slack.** `ember + terra` scored 0.50 of 14, "-1.75 found (permutation p 0.029)" (CR:298, CR:336), and the audit says that is "largely terra returning nothing" (CR:294). A panel of two with one empty reviewer is a panel of one. This is a reliability problem, not a size effect, but it is exactly what Option A makes more expensive.

**C4. External guidance recommends three.** W01 recommendation 9 reads "a panel of three heterogeneous reviewers plus one adjudicator is the evidence-supported size" and W01 recommendation 4 says a PASS should need at least two valid reviewers. Both fit a default of three more directly than a default of two. Reflect already has the adjudicator (debate plus calibrator), so the comparison is two plus adjudicator against three plus adjudicator, which no source tests.

**C5. The driver of Tier 2 spend is the pre-filter, which Option A does not touch.** 35 of 39 runs escalate for an input-format reason (A1). A saves one reviewer per run; B would save the whole run for those plans. If H-A shows Tier 2 is not worth its cost on sparse-labelled plans, B saves much more than A.

## Correctness argument

C14 is undecided by evidence, so the argument has three parts: the change keeps every invariant the current design relies on, it is the better bet when its unmeasured loss is compared with the alternative's, and it says plainly what it does not claim.

### 1. Invariants preserved

| Invariant | Why it still holds under a default of two | Where |
|---|---|---|
| The anchor is never dropped | The fixed slot is resolved first and exhaustion of it is fatal, not skipped | `panel.py:536-537, :647-649` (R04 §2); rule D5, `SKILL.md:321` |
| Executor class is not a reviewer class | The three-row table gives, for each of unknown, opus, sonnet and haiku, exactly two reviewers of two different classes, neither equal to the executor. Executor sonnet is the existing, tested `x2` template; executor haiku and opus were dry-run in memory (Design). Unknown executor stays fail-open exactly as today (9 of 13 recorded shadow runs had it) | `tests/review/test_review_reflect_templates.py:105-110`; R11 §8 output line 266 |
| T2 stays T2 | `tier_reached` is 2 and `merge_method` is `adversarial` whenever at least two reviewers succeed; the diversity gate needs two distinct model ids | `ensemble.py:772-773`; `_diversity.py:8-15`; R13 line 295 |
| A regression is debated by at least two reviewers | Two satisfies it | `SKILL.md:433`; R05 line 81 |
| Contract 1.8.0 stable keys are untouched | Arrays get shorter; new keys go under `telemetry:` only | `SKILL.md:349`; lint L2 `panel_lint.py` stable-key check |
| The cap of three holds | Unchanged; `--reviewers 3` is the only way past two | `panel.py:73, :130, :143` |
| Failure is closed | Fewer than two completed cards is DEGRADED (`single-reviewer-fallback`, code engine `degraded-tier1`), never PASS | `contract.py:278-296`; `tests/cli/reflect/test_ensemble_stub_integration.py:251-277` |

### 2. The decision under uncertainty

Both Option A and Option B act on an unmeasured quality question, so neither can be called safe by measurement. They differ in three things that can be checked.

| | Option A (two reviewers by default) | Option B (rubric first, three stay) |
|---|---|---|
| What is given up if the bet is wrong | The third reviewer on plans that escalate. E2 found no significant effect of reviewer count on found, real blocking or wrong blockers (CR:381) and external work reports diminishing returns after two (A8) | The whole Tier 2 pass for up to 34-35 of 38-39 plans, replaced by one agent (R11 §12 item 4). The project's own H-A bar (15 points of recall, MR:527) says the loss may be large |
| Reversal | A flag default and template data | A change to the table-wide escalation pre-filter that every UC-1 consumer reads (`SKILL.md:284, :443`) |
| What it saves if the bet is right | One reviewer call, one calibrator call and one debate variant on nearly every run (A1, A2) | A whole Tier 2 run on 35 of 39 plans, which is more |

Read as a 2 by 2 on the unknown truth (is three worth more than two in reflect?):

- If two is as good as three: A saves calls on nearly every run now; B saves more but only after it is also shown that Tier 1 is as good as Tier 2, which is a second unmeasured claim.
- If three is better than two by a margin that matters: A loses some recall on escalated plans, the `reviewers_default_applied` telemetry plus the pilot arm below detects it, and the rollback is a one-line default. B, if the bet on Tier 1 is also wrong, loses recall on most plans and the loss is not visible without the same pilot.

So A is the smaller, more observable and more reversible of the two unmeasured moves. It also leaves B available: nothing in A prevents fixing the pre-filter later, and the pilot that H-A needs can carry a third arm at small extra cost (see Cost).

### 3. What this proposal does not claim

- It does not claim two reviewers are as good as three inside reflect. That is not measured anywhere (R11 §12 item 3).
- It does not claim the saving is a third of a run. The saving is counted in calls, and E2's own table shows a two-reviewer panel costing as much as a three-reviewer one when the dropped reviewer was the cheap one: `ember + sonnet` 142,967 tokens against `ember + luna + sonnet` 138,551 (CR:315, CR:320).
- It does not claim the parsed-sparse pre-filter is right. It treats that as a separate lever for after H-A.
- It does not use the stale line "sonnet alone gives most catches per token". That figure is pilot-only, one run per package, before `source.md` shipped (2026-11-11), and E2's own valid-era tables contradict it (R11 §6; gaps D-57).

## Risks and mitigations

| ID | Risk | Evidence | Mitigation | Residual |
|---|---|---|---|---|
| R1 | Quality loss from dropping the third reviewer, unmeasured in reflect (the synthesis rates this option High) | C1, C2 above | Keep `--reviewers 3` and the enterprise template as the opt-in; record `reviewers_default_applied`; add a 2-reviewer and 3-reviewer arm to the H-A pilot on the E2 ground-truth packages (E2's harness is the only instrument that can measure plan recall, R11 §12); the owner sets the rollback trigger before shipping (the 15-point bar of MR:527 is a candidate, as a proposal and not as evidence) | Until the pilot runs, the loss is unknown by construction |
| R2 | No slack: with two reviewers, one failed or invalid reviewer leaves one, and the run degrades. With three, one failure still leaves a PASS-eligible pair (the code engine only degrades when at most one survives, `test_ensemble_stub_integration.py:251-277`; `reviewer-shortfall` is a benign token, `tests/cli/reflect/test_verdict_mapping.py:572-580`) | C3 above. E2: `ember + terra` -1.75 found (p 0.029) because terra returned nothing (CR:294, CR:298); luna lost 2 of 30 findings blocks at merge, sonnet 0 of 15 (CR:427) | Anchor on the reliable-format class (sonnet, 0 of 15 blocks dropped, CR:427); keep the existing bounded re-ask for an invalid block (`SKILL.md:343`); add one re-dispatch of a reviewer that returned nothing before degrading. Observed so far: 0 shortfalls in 13 shadow runs and 15 of 15 combo runs complete (A5) | Prose-following lapses by the orchestrator are real (shadow13 and shadow15 ignored step 10 even with correct text, R11 §8 table); a lapse in the re-dispatch step costs a degrade |
| R3 | Executor class equals the second slot's class and a bare two-slot template drops to one reviewer | In-memory resolve: `t1b`+`t4` with executor haiku gives `[sonnet]` and `t4` skipped; `t1b`+`t1a` with executor opus gives `[sonnet]` (Design) | Select the template by executor class (three rows); test every row | An unrecognised executor class falls back to the default row, same fail-open as today |
| R4 | The third persona (refactorer) disappears | `SKILL.md:652-656` | `--strategy enterprise` keeps analyzer, qa, architect on three reviewers. No per-persona catch data is cited in the C14 evidence, so the loss is not quantified | The refactorer lens is unmeasured, in either direction |
| R5 | "Diverse" is a class label and the gateway can serve two classes with one model, or all classes with one (combo A3 collapsed to sonnet on every reviewer, `results.md`; the "haiku" slot served by `gpt-6.1-sol`, R04 §7.2). With two reviewers a collapse removes all diversity | R04 §7, §10 point 6 | This is the core's dispatch gap (the dispatcher must pass `model` and record the served model), independent of count and needed by every option. A should not ship ahead of the shadow path recording it | Same exposure at three reviewers, but with two a single collapsed slot leaves one distinct model (diversity `insufficient`, DEGRADED), while three can lose one slot and keep two |
| R6 | Savings smaller than expected | A2 limit; CR:315 against CR:320; per-reviewer cost not recorded (R08 line 398) | Record reviewer, calibrator and debate calls per run in telemetry before and after; report calls, not estimated dollars (`FINDINGS.md:37`) | Token saving may be small if the dropped reviewer was the cheap one |
| R7 | Debate convergence behaves differently with two variants. The 0.80 floor (`contract.py:317-326`) was not shown to be tuned for two | No research file measures convergence by reviewer count | Mark [UNVERIFIED]; run the pilot arm and read `adversarial_convergence_score` by count before treating two as settled | An untested statistic gates PASS |
| R8 | The Stage 2 exit gate (13 of 20 runs, currently FAIL) was built around three | `reflect_shadow_exit.py:244-245`; R11 §8 | Generalise the shortfall rule; as R11 §8 describes it, the script counts a run when its manifest says engine `shadow` and state `published` (`:209-223`) and parity refuses only a changed tier file (`:128-132`); I found no template-id or reviewer-count check, so earlier three-reviewer runs would still count, and whether they should count for a two-reviewer rollout is an owner choice | Up to 7 more runs are needed for the exit either way |

**The weakest point of this proposal** is C1 and C2 together: no source compares two and three reviewers inside reflect, and the one E2 size effect that survived testing is a 2 to 3 gain. A reader who weighs those two heavily should prefer Option B or C. The proposal's reply is limited: that effect needs a repeated model, which reflect forbids; the same study's other two-reviewer panel (`ember + sonnet`) matched three-reviewer control scores; and a flag default can be turned back. It is a bet that the third reviewer is the cheapest thing to give up, not a demonstration.

## Test coverage needed

### Existing tests that change

| Test | Change | Why |
|---|---|---|
| `tests/cli/reflect/test_ensemble_unit.py:106-118` (`test_reviewers_outside_normal_range_clamp_to_two_four`) | `high.reviewers == 4` becomes 3 and the name loses "four" | The clamp moves from `[2,4]` to `[2,3]` (`config.py:335`); closes G-67 |
| `tests/cli/reflect/test_shadow_exit_script.py:261-269` (`test_stage2_counts`, asserts "2-of-3 shortfalls: 2") | New label text; add a case with `reviewers_resolved: 2`, `reviewers_complete: 1` | Shortfall rule becomes `complete < resolved` (`reflect_shadow_exit.py:244-245`) |
| `tests/review/test_review_reflect_templates.py:14-21` (`NAMES`) and `:57-85` (`test_template_slots_match_the_design`) | Add the new ids and their slot pins | Two new template families |
| `tests/cli/reflect/test_ensemble_unit.py:121-129` (`test_transport_resolves_default_and_stub`) | None expected; confirm it still passes with the new default | It calls `resolve_config` with no `reviewers` |

### Existing tests that stay and guard the design

`tests/review/test_review_panel_reflect_profile.py:146, :170` (cap of 3 still enforced); `tests/review/test_review_reflect_templates.py:88-135` (three-slot behaviour, since those files are kept); the code-engine suites that pass `reviewers=3` explicitly (`test_ensemble_stub_integration.py`, `test_cli_smoke.py:127, :155`, `test_ensemble_fallback_stub.py:110`); `test_panel_contract_lint.py:284-292` (minimum two cards).

### New tests

1. Template validity and slots for `reflect-pre-duo`, `reflect-pre-duo-xh`, `reflect-post-duo`, `reflect-post-duo-xh`: valid under `validate_panel` with tiers, one fixed slot, two reviewers, no `tier0`, no Fable.
2. The executor table: for executor in {unknown, opus, sonnet, haiku}, the chosen template resolves to exactly two reviewers of two distinct classes, none equal to the executor (the in-memory dry run in Design, as a test).
3. A property test over the three classes and strict distinctness: no executor class ever yields fewer than two reviewers from the table.
4. Code engine: `reviewers` default is 2; a pool of 2 models no longer raises `ModelPoolTooSmallError` at the default; `--reviewers 3` with pool 2 still does (`test_u4`).
5. Code engine floor: N=2 with one failing transport is `single-reviewer-fallback`, DEGRADED, exit 11 (mirror of `test_i5`), and N=2 with both succeeding is PASS-eligible with `reviewers_verified` true.
6. Shadow skill contract: a fixture run with `reviewers_resolved 2` passes `panel_lint` L6 and the parity recomputation with personas (analyzer, qa) only; `panel_shortfall` and `reviewers_default_applied` appear under `telemetry:` and nowhere else (L2 stable-key check).
7. Re-dispatch rule (if adopted): a fixture where reviewer 2 returns nothing and the second dispatch succeeds records one shortfall-resolved attempt in the manifest; a second failure degrades.
8. A pin on the `--reviewers` default in `commands/reflect.md`, `SKILL.md:86` and `commands.py` so the three do not drift apart again.
9. The H-A pilot arm itself is a measurement, not a unit test: T1, T2 with two reviewers, T2 with three, on the E2 ground-truth packages, scored blind (see Cost).

## Cost

**Build effort: S to M.** The synthesis lists S. The enumerated work is slightly more than the label suggests because of the executor-keyed templates and the exit-gate rule:

| Item | Size |
|---|---|
| 4 new template files (`reflect-pre-duo`, `reflect-pre-duo-xh`, `reflect-post-duo`, `reflect-post-duo-xh`) | data, a few lines each |
| `--reviewers` default in `commands.py`, `config.py`, `reflect.md`, `SKILL.md` and the clamp at `config.py:335` | 5 one-line edits |
| `SKILL.md` step 1 template table, floor and re-dispatch wording, telemetry key names | prose, about 3 paragraphs |
| `reflect_shadow_exit.py` shortfall rule and label | 2 edits |
| Tests above (items 1-8, plus the four edits to existing tests) | S |

Under the repository rules the hard limit is five edits per direct change, so this goes through a written plan and `/sc:implement`, not a direct edit.

**Run cost.** Per escalated run, one reviewer call, one calibrator call and one variant of the debate are removed (A2). Tokens cannot be stated per reviewer from existing data (R08 line 398). The scale to keep in view is that a whole 3-reviewer combo run spent 185,086-367,381 output tokens (`results.md`, 2026-11-13). Because 38 of 39 recorded runs escalate (A1), the saving applies to nearly every run, but it is bounded by the share of the run the reviewer phase takes, which no record measures yet.

**Measurement cost (the part that is not free).** The H-A pilot needs a reflect consumer added to the E2 harness and portability fixes first (R11 §12; G-59 asks who owns that port and it is open). The study's pilot judge step used 9 judge subagents and 1,034,575 output tokens in total, about 115,000 each (E2 `PILOT-REPORT.md` line 52 at the pinned commit), and that multiplies by arms times packages times repeats. Adding the two-versus-three arm to a pilot that has to run anyway costs one extra arm; running it alone costs the whole pilot. If the owner will not fund any pilot, the honest status of Option A is "a cost cut on thin evidence", and Option C costs nothing but keeps paying for three reviewers.

**Owner decisions this needs:** (1) accept a default of two before H-A (the one decision C14 turns on); (2) who owns the E2 benchmark port (G-59); (3) whether three-reviewer shadow runs already counted toward the Stage 2 exit still count (R8); (4) whether `default` (four reviewers) in the document loop follows (out of scope here).
