# Proposal B: Fix the rubric first (O-8), keep the cap at 3, decide the count after H-A for C14

**Conflict:** C14, panel size versus cost (slug `panel-size-cost`), `synthesis/synth-04-options-conflicts.md:893-954`.
**Side and option:** SIDE B, Option B as worded there at `:915-927`: stop the parsed-sparse pre-filter from forcing Tier 2 on labelling format alone, keep the reviewer cap at 3, and decide the reviewer count only after H-A (Tier 2 recall against Tier 1 recall) is measured.
**Date of this draft:** 2026-11-13. Repository at `792cf8c52` on `ironbelly/shadow-runs`.

**Tags used.** `[CODE-VERIFIED]` = read in the checkout for this proposal. `[CODE-VERIFIED in data]` = counted from recorded run files under `.dev/reflect/`. `[DOC-SOURCED]` = taken from a report's own text, not recomputed. `[EXTERNAL]` = outside the repository, with URL. `[UNVERIFIED]` = decides nothing. E2 evidence is cited only from commit `4a22d74213f93837d00c2c314075dd967b9a98e3`.

## Design

**One-sentence position.** Do not touch the reviewer count now; change the one input that makes Tier 2 run for a reason unrelated to plan risk, but only behind a measured gate, and write down in advance how the count will be decided once H-A exists.

### What the design decides

| Question | B's answer |
|---|---|
| Reviewer cap for reflect Tier 2 | Stays 3. No code change: `_REFLECT_MAX_REVIEWERS = 3` already rejects larger templates and resolutions. |
| Default reviewer count | Stays 3 (`--reviewers` default 3, `N_eff = min(--reviewers, alias count, 3)`). The choice between 2 and 3 waits for H-A plus one added arm (below). |
| Pre-filter `coverage_degraded: parsed-sparse` | Still computed and still emitted in the contract, but it no longer forbids a Tier 1 stop. A sparse plan is judged on the union coverage numbers that the same D13 change already added. |
| Other pre-filters (`coverage_undefined`, `surface_unreached`), pins, hard overrides | Unchanged. |
| Rubric rows 3 to 7 | Unchanged by this proposal. They are measured by the replay script, not edited (see "The weakest point" under Risks). |
| Document-review default template (4 reviewers) and `live7` (7) | Out of scope for C14 under B. Their count is template data and is blocked by C03, not by this conflict (see the module list). |

### The three phases

**Phase 0 (no behaviour change, zero model cost).** Add two audit keys to `tier_decision.yaml` and a read-only replay script that tallies the recorded decisions by escalation path. This also corrects the attribution that O-8 and MR:142 rest on (see Evidence E-5): the recorded "parsed-sparse" runs are mostly escalated by rows 4, 5 or 6 as well.

**Phase 1 (rubric change, gated).** Edit the skill text so that the sparse flag is advisory. The change is released only if gate G1 passes: a retrospective comparison, on the few recorded runs where the sparse flag was the only reason for Tier 2, of what the Tier 1 card said against what Tier 2 found. If G1 fails, Phase 1 does not ship and B stops at Phase 0 plus Phase 2; the count stays at 3 either way.

**Phase 2 (decide the count).** Run H-A as designed in `pilot-design.md` and add one arm that the template set can already express (two reviewers). Decide 2 or 3 by a rule written before the run (section "How it works", step 6).

### Core and consumer modules

| Module | What B does |
|---|---|
| Shared core (panel resolver, manifest, clusterer, verdict) | No change. The profile cap stays in `panel.py` (reflect profile 3; generic panels keep their 1..8 range). The manifest already records `reviewers_requested` and `reviewers_resolved`, which is the count telemetry H-A needs. |
| Reflect module (pre mode) | All the change lives here: `SKILL.md` Step 1B.2b, §5.3 rows 1, 2 and 8 and the pre-filter precedence paragraph, §5.4 audit keys, plus the matching lines in `refs/coverage-mapping.md`, `refs/report-template.md`, `refs/grader-extensions.md` and `CHANGELOG.md`. |
| Workflow tasklist module (`sc:workflow` Wave 4) | No change to its call (`/sc:reflect --mode pre` with default flags). It is advisory, so a Tier 1 stop on a sparse plan costs at most a missed advisory finding. |
| Tasklist module, Stage 10.5 pre sign-off | No change. It passes a computed `--depth` and `--tier`; only phases with `--depth standard` and `--tier auto` can see the new behaviour. Advisory on the verdict. |
| Tasklist module, per-phase post gate (blocking) | No change and no exposure: it runs `--depth deep`, which forces Tier 2 through `ensemble.py`, never through the rubric. |
| Spec review loop (E3 default 4 reviewers, `live7` 7) | No position under C14. Its count is a template-data edit, and the model E2 chose for its default is not nameable by any packaged tier today, so the question is blocked on C03. |
| Future modules (PR review, rf-qa) | Inherit "cap is profile data, count is a template choice made on measured evidence". Nothing to build now. |

## How it works

### Data flow for a `/sc:reflect --mode pre` run

1. **Wave 1, extraction.** Step 1B.0 runs its two passes (deterministic ids, then quote-pinned inference) and yields `parsed_count`, `inferred_count`, `coverage_pct` (parsed only, null when no ids were parsed), `coverage_pct_union`, `unmapped_requirements_union` and `S_dev_density` over the union set. Unchanged.
2. **Step 1B.2b, flag only.** When `inferred_count > parsed_count` it still sets `coverage_degraded: parsed-sparse` in the report header, `tier_decision.yaml` and the return contract. New text: the flag is advisory and does not forbid a Tier 1 stop. The loud-never-silent posture is kept by the header WARN in step 4.
3. **Wave 2, rubric §5.3.** Rows 3 to 7 are untouched. Rows 1, 2 and 8 lose the `NOT coverage_degraded` conjunct and the table-wide precedence paragraph names only `coverage_undefined` and `surface_unreached`. In their place one sentence: when `coverage_degraded` is set, a Tier 1 stop through row 1, 2 or 8 additionally requires `coverage_pct_union >= <coverage-floor>` (default 0.90), read instead of the parsed `coverage_pct`, which is null for a plan with no parsed ids. Explicit pins keep their current precedence.
4. **Report.** A sparse plan that stops at Tier 1 gets the existing "STOP at T1 with WARN" treatment plus a header line: labelling is sparse, the verdict rests on inferred requirements.
5. **If the final tier is 2.** Nothing changes: legacy rotation or, with `--t2-engine shadow`, the panel; `N_eff <= 3`; the fixed anchor is never dropped.
6. **Offline.** `scripts/reflect_tier_replay.py` reads recorded decisions and prints the tally of E-5; the H-A pilot and the E2 harness are the instruments for the count (Phase 2).

### Contract and audit fields

| Field | Where | Change |
|---|---|---|
| `coverage_degraded`, `coverage_pct_union`, `unmapped_requirements_union`, `coverage_undefined` | return contract 1.8.0 (listed in `panel_lint.py:46`) | Same names, same values. Only the prose describing `coverage_degraded` drops "table-wide T1-stop pre-filter" (`SKILL.md:454`, `:741`). `contract_version` stays 1.8.0. |
| `sparse_flag_decisive: true \| false \| null` | `tier_decision.yaml` (additive audit key) | New. `true` when Tier 2 was forced only because of the sparse flag, that is, no escalate row (3 to 7) matched and no pin applied. `null` when a pin or hard override decided. Computed during Phase 0 against the old rule, so it is meaningful before any behaviour changes. |
| `escalation_path: prefilter_only \| row_<n> \| prefilter_and_row_<n> \| pin \| hard_override \| t1_stop` | `tier_decision.yaml` (additive audit key) | New. It gives MR:540's strata ("escalated by the parsed-sparse pre-filter" versus "by rule 4, 5 or 6 without it") a recorded value instead of a reconstruction. |

`SKILL.md:469` already states that audit keys of this artifact are not contract fields and leave `contract_version` at 1.8.0 (the three `t2_engine_*` keys are the precedent), so no contract bump is needed.

### CLI surface

- No new `superclaude` subcommand and no new `/sc:reflect` flag.
- The kill switch already exists: `--tier 2` or `--depth deep` forces Tier 2 whatever the rubric says (`SKILL.md:405-408`); reverting the skill text restores the old rule.
- New read-only script, run as the repository rules require: `uv run python scripts/reflect_tier_replay.py --runs-root .dev/reflect`, modelled on `scripts/reflect_shadow_exit.py` (same `--runs-root` default, same collect-then-report split). A decision file that lacks the inputs for an exact recomputation is reported as "not evaluable", never guessed.
- `superclaude review panel resolve` and the packaged `reflect-*` templates are unchanged.

### Gate G1 (when Phase 1 ships)

G1 is an owner decision, taken on a table the replay script prints: for every recorded run with `sparse_flag_decisive: true` that has both a `t1-card.md` and a Tier 2 merged verdict, whether Tier 2 produced a blocking finding that the Tier 1 card did not contain. B recommends shipping Phase 1 as default behaviour only if the table has at least three clear-cut candidates and none shows a Tier 2-only blocker. Otherwise Phase 1 is built behind the H-A pilot instead: the pilot's sparse stratum (already required by MR:540) measures Tier 1 against Tier 2 on exactly the plans B would flip, and the default changes only after that. Section "Correctness argument" says why the stake is small enough that this ordering costs little, and the Evidence section says what today's table looks like (it does not open G1).

### Count decision (step 6 of the data flow, Phase 2)

Pre-registered, reusing the thresholds already in `pilot-design.md` (T-1 and T-2); the 2-versus-3 rule is B's proposal, not an existing threshold.

1. H-A passes (Tier 2 recall at least 15 points above Tier 1 on seeded defects, T-1): Tier 2 stays. Then 2 replaces 3 only if the two-reviewer arm is within 10 points of the three-reviewer arm (one-sided 95 percent bound, the T-2 margin) and its median tokens are lower. Otherwise 3 stays.
2. H-A fails: the owner chooses between shrinking Tier 2 to 2 reviewers and tuning the rubric, as MR:527 already says, and the Phase 0 table is the input to the "tune the rubric" branch.
3. Raising the cap above 3 stays closed unless H-A passes (MR:289, marked PROPOSED there).
4. The two-reviewer arm needs no code: `reflect-lite` under `--strict-distinct` already resolves to sonnet and haiku (`research/04-panel-resolution-identity.md` §4, `reflect-lite` row). Arm D in `pilot-design.md` is `reflect-lite` too but is defined to price the Opus-moves ablation on 6 plans, not to compare 2 with 3, so the comparison needs its own pre-registered reading of that arm or a sibling arm.

## Evidence

**Citation forms.** `SKILL.md` = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. `MR` = `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`. `PD` = `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/pilot-design.md`. `R11` = `research/11-evaluation-evidence.md` and so on for the other research files, all under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/`. `CR` and `PR` = E2's `COMBO-REPORT.md` and `PILOT-REPORT.md` under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` at commit `4a22d74213f93837d00c2c314075dd967b9a98e3` (lines re-read with `git show` at that commit for this proposal).

### The cap and the count (what already exists)

- **E-1. The cap of 3 is code and is tested.** `_REFLECT_MAX_REVIEWERS = 3` at `src/superclaude/cli/review/panel.py:73`; the template check at `:130-133` and the resolution check at `:143-146` reject more; the docstring at `:83-88` says generic panels keep their 1..8 range. Tests: `tests/review/test_review_panel_reflect_profile.py:145-147` (a reflect template with 4 reviewers fails with "at most 3", the same shape as a generic panel passes), `:170` (a `ValueError` matching "at most 3"), `:199` (a generic panel with four reviewers stays valid). [CODE-VERIFIED] Research: `R04` §4.3.
- **E-2. The skill text agrees.** `--reviewers N` is "2-3; default 3" (`SKILL.md:86`) and decision D5 reads `N_eff = min(--reviewers, alias count, 3)` with the fixed anchor never dropped (`:321`). [CODE-VERIFIED]
- **E-3. The post-gate wrapper disagrees, and that is a separate path.** `src/superclaude/cli/reflect/config.py:335` clamps reviewers to `max(2, min(4, n))`. The blocking post gate reaches Tier 2 through `run_tier2_ensemble` (`runner.py:538-545`), not through the rubric or the panel (`R09` §4.2, §5; the `runner.py` line numbers are from `R09` and were not re-read for this proposal). This is gap G-67; B records it and leaves it to C17. [CODE-VERIFIED for `config.py:335`; the rest via `R09`]
- **E-4. The packaged document-review default has four reviewers.** `review-panel.default.json` slots: `t1b` x1 fixed, `t2` x1, `t3` x2; `live7` has seven (`R04` §4, rows `default` and `live7`). The model E2 picked for its default, `muse-ember-1.0`, "appears in neither aliases, names nor classes" of the packaged tier file (`R04` §4 tier-file bullet). [CODE-VERIFIED]

### Why Tier 2 is almost always paid, and what the pre-filter really accounts for

- **E-5. The recorded history, recounted by escalation path.** Source: the 39 non-shadow `.dev/reflect/pre-*/artifacts/tier_decision.yaml` files, tallied by `selected_tier`, `fired_rule_number` and `coverage_degraded` for this proposal. [CODE-VERIFIED in data]

| Recorded decision | Runs | What it means for the pre-filter |
|---|---|---|
| Tier 2, flag set, escalate row 4 recorded (`S_domains >= 3`) | 18 | Row 4 escalates with or without the flag. |
| Tier 2, flag set, escalate row 6 recorded (`C < 0.85`) | 9 | Same. |
| Tier 2, flag set, escalate row 5 recorded (`S_dev_density > 0.20`) | 2 | Same. |
| Tier 2, flag set, row 8 default recorded | 1 | The only clear-cut case where the flag alone forced Tier 2 (`S_domains` 2, `S_dev_density` 0.0, `S_scope` 3). |
| Tier 2, flag set, row 0 | 1 | Its own reason text says row 4 (`S_domains` 3) "would also escalate". |
| Tier 2, flag set, no row number recorded | 3 | `S_domains` not recorded in two of them; one says "S_domains may count 3". Unresolved. |
| Tier 1, flag set | 1 | The `--tier 1` pin (`pre-pr-submit-ci-monitor`). |
| Tier 2, flag not set | 4 | Two forced by `--depth deep`, one row 4, one row 6. |
| **Total** | **39** | Flag set in 35, Tier 2 in 38. |

  Why the first three rows do not depend on the flag: rows 1 and 2 need `S_domains <= 2`, `S_dev_density <= 0.10` and `C >= 0.85` (`SKILL.md:431-432`), so a plan that matches row 4, 5 or 6 cannot stop at Tier 1 whether or not the flag exists. So the flag was the only reason for Tier 2 in 1 recorded run for certain and in at most 5 of 39 (13 percent), not in 34 or 35. MR:142 itself says "34 by the parsed-sparse pre-filter ... others by rule 4, 5 or 6" and MR:540 asks for the two strata to be reported apart; `R11` §12 item 4 ("up to 34-35 of 38-39 would have been eligible to stop at T1") is an upper bound that the table does not support. `fired_rule_number` and the inputs are written by the orchestrating model across skill versions from 2026-06 to 2026-11, so the table is a recount of recorded claims, not an independent re-execution of the rubric.
- **E-6. The one clear-cut candidate is a counterexample.** `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416`: `tier_decision.yaml` has row 8, `coverage_degraded: parsed-sparse` (5 inferred, 0 parsed), `S_scope` 3, `S_domains` 2, `S_dev_density` 0.0. Its Tier 2 merge ended `merged_verdict: FAIL` with `blocking_findings: [M-13]` (`return-contract.yaml:62-63`). `adversarial/merged-verdict.yaml:74-80` records M-13 as `grounding_gap`, `severity: blocking`, from the invariant probe INV-001: the five target files are untracked, so three acceptance criteria that use `git diff` would pass on empty output. The Tier 1 card (`t1-card.md`, findings F1 to F6) contains none of "untracked", "git status" or "ls-files" (count 0), and no reviewer card mentions "untracked" either. [CODE-VERIFIED in data]
- **E-7. The mechanism and its stated reason.** Step 1B.2b forbids the Tier 1 stop when `inferred_count > parsed_count` (`SKILL.md:284`); rows 1 and 2 carry `NOT coverage_degraded` (`:431-432`); the precedence paragraph makes it table-wide (`:443`); `refs/coverage-mapping.md:77-79` repeats it; `CHANGELOG.md:439-445` introduced it together with two-pass extraction and the union fields. The same change made `S_dev_density` use the union denominator (`SKILL.md:278`, `:423`) and left `coverage_pct` parsed-only (`refs/coverage-mapping.md:67-76`). T2's qa reviewer is the one that reads the whole spec body "even if Pass 2 under-extracts" (`refs/reviewer-spec.md:55`, per `R06` §2.3). [CODE-VERIFIED]
- **E-8. Nothing pins the pre-filter.** `coverage_degraded` appears in Python under `src/` only at `src/superclaude/cli/reflect/panel_lint.py:46` (a list of contract field names). A search of all of `tests/` for `tier_decision`, `selected_tier`, `fired_rule`, `coverage_degraded`, `parsed-sparse` and `Step 1B.2b` finds two hits: `coverage_degraded: null` in `tests/cli/reflect/fixtures/panel_lint_legacy/return-contract.yaml:16`, and the words `tier_decision.yaml` inside the prose of a card fixture (`tests/review/fixtures/reflect_cards/markdown-lines.md:10`). The three D13 eval fixtures are specified in `refs/grader-extensions.md:353-359` (the `sparse-labeled-spec` case asserts `tier_reached: 2`), but no `sparse-labeled-spec` case exists under `.dev/eval-workspaces/sc-reflect/cases/` (directory listing). [CODE-VERIFIED]

### Who is exposed to the rubric

- **E-9. Consumers.** `sc:workflow` Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` with defaults and is advisory (`sc-workflow-protocol/SKILL.md:89,93`, `R09` §3). Stage 10.5 passes computed `--depth` and `--tier` and is advisory on the verdict (`sc-tasklist-protocol/SKILL.md:1619-1646`, `R09` §4.1). The per-phase post gate is blocking but forced to `--depth deep` and `ensemble.py` (`:1155-1179`, `R09` §4.2). By default Tier 2 on this path is the legacy rotation; the panel runs only with `--t2-engine shadow`, which no consumer passes (`R09` §5). [CODE-VERIFIED in `R09`; these consumer files were not re-read for this proposal]
- **E-10. Shadow evidence is not exposed.** The shadow runs reach Tier 2 mostly through the `--tier 2` hard override (for example `pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow01`, `-shadow02`, `-shadow03`, `pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05`: "hard override --tier 2, no rubric row evaluated"). A rubric change therefore does not slow the 20-run Stage 2 count. [CODE-VERIFIED in data]
- **E-11. Retrospective data exists for free.** 22 of the 39 recorded run directories hold a `t1-card.md`, and every escalated run holds the Tier 2 verdict, so the G1 table needs no new model calls. [CODE-VERIFIED in data]

### Worth, cost and what E2 does and does not say

- **E-12. H-A is defined and not run.** MR:527 sets H-A at Tier 2 recall at least 15 points above Tier 1 on seeded defects and says that on failure "the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8)"; MR:556 is O-8 ("decide after H-A"); `PD` T-1, T-2 and T-7. Cost rows in `PD`: pilot 1.30M to 2.62M claude tokens (C-5; 3.61M to 7.24M under the other reading of the repeats, C-5b); confirmatory 33 plans 2.41M to 4.88M (C-6); grading, seeding and orchestration are not priced (`PD` SD-8). [DOC-SOURCED, rows re-read]
- **E-13. Shape of the arms.** `PD` arms A (T1 `--tier 1`), B (legacy T2), C (development-build panel), D (`@reflect-lite`, 6 of the 12 plans, "to price the Opus-moves ablation"). None is a two-versus-three comparison on its own terms. `PD` requires at least 25 percent non-sparse plans because only 4 of 38 recorded decisions were non-sparse (`PD` quota paragraph; MR:540). [DOC-SOURCED]
- **E-14. E2's ceiling is flat in panel size, in E2's setting.** Replicated panels score 1.60 to 2.50 of 14 known defects per run: `ember + sonnet` 2.50 and `ember + luna` 2.25 (both n=4), `haiku + 2x luna` 2.20 (n=5), `ember + 2x luna` 1.83 (n=6, 63,644 tokens) (`CR:315-320`, `CR:331`). No difference in found, real blocking, wrong blockers or control is significant between replicated panels, p 0.54 to 1.0, while token differences are (p 0.002 to 0.009) (`CR:381`). Only three statistics survive audit F, including that `2x luna + 2x ember` has 2.75 to 3.25 more wrong blockers (permutation p 0.005 to 0.03) (`CR:298`). [DOC-SOURCED; raw `score.json` not re-aggregated, G-82]
- **E-15. E2 itself ranks the input fixes above panel choice.** `CR:428`: "All panels sit at about 2-2.5 of 14, so the harness fixes (anchor limit, source.md path in the brief) remain the biggest lever." The study also never ran reflect, a calibrator or a debate (`R11` §6 "What the study measured and did not", §12 item 3), so its ceiling is not the Tier 2 ceiling. [DOC-SOURCED]
- **E-16. The pilot line "sonnet alone gives the most catches per token" is not a current fact.** Arm A 2/16 at 93,098 tokens was one run per package before `source.md` shipped (`PR:46-50` via `R11` §5; `R11` §6; gaps row D-57); cheaper valid-era panels beat it per 100k tokens (`CR:317`, `CR:331`). B does not use it. [DOC-SOURCED]
- **E-17. Estimated cost of a Tier 2 run.** Orchestrator token estimates for shadow contracts run from 90,000 (wave 3 of shadow04) to 137,000 (shadow08) for wave 3 alone, and the combo runs spent 185,086 to 367,381 output tokens per whole run for combos B to E; these are estimates and the combo document says "do not compare" (`R11` §12 table, last row). Used here only for order of magnitude. [DOC-SOURCED]
- **E-18. External context, weak.** A self-published, not peer-reviewed corpus reports that the second reviewer is the largest coverage step and returns diminish after two to three: [EXTERNAL] https://zenodo.org/records/21328807 (`research/web-01-panel-aggregation.md:97-99,148`, reliability low to medium, read from the abstract only). A preprint of nine judges finds about two effective votes: [EXTERNAL] https://arxiv.org/html/2605.29800v1 (`web-01:59,145`). `web-01:164` (recommendation 9) reads three heterogeneous reviewers plus one adjudicator as the evidence-supported size. These support "not more than 3"; they do not choose between 2 and 3 for reflect.

## Correctness argument

**1. The behavioural change is small and can be stated exactly.** Only rows 1, 2 and 8 and the precedence paragraph change. Rows 3 to 7 are evaluated before row 8, so a plan that reaches row 8 or matches row 1 or 2 has no escalate row against it. The new rule therefore differs from today's rule only for runs that meet all of these: the sparse flag is set; no pin or hard override applies; `coverage_undefined` and `surface_unreached` are not set; no row from 3 to 7 matches; the remaining conjuncts of row 1, 2 or 8 hold; and `coverage_pct_union >= floor`. For every other run the decision is identical. On the recorded history that is 29 sparse runs that are decided by row 4, 5 or 6 whatever the flag says, plus the pinned and non-sparse runs, so at most 5 of 39 can change (E-5). [follows from `SKILL.md:427-443`, CODE-VERIFIED]

**2. It removes a decision that depends on formatting, not on the plan.** Today two plans with the same content get different tiers if one writes `R-001` in front of each requirement and the other does not. The flag was added because parsed-only coverage is vacuous when nothing is parsed (`coverage_pct` is null when nothing is parsed, `refs/coverage-mapping.md:68-69`, and the rule that 0/0 must not pass is at `SKILL.md:282`; the row 1 comparison reads the parsed number, `SKILL.md:443`). The same D13 change added the repair: inferred rows with verbatim quotes and citations, `coverage_pct_union`, and a union denominator for `S_dev_density` (E-7). B keeps that repair and drops only the second, blanket guard that sits on top of it. Under B the sparse plan has to clear the same 0.90 floor on the union number, and the denser the unmapped inferred content, the sooner row 5 (`S_dev_density > 0.20`) escalates it anyway.

**3. Reviewer counts cannot change.** B touches no code in `panel.py`, `config.py`, the templates or `reflect_shadow_exit.py`. Every run that reaches Tier 2 gets exactly the panel it gets today, so the cap of 3 and the Stage 2 shortfall rule (`reviewers_resolved == 3` and `reviewers_complete == 2`, `scripts/reflect_shadow_exit.py:244`) keep their meaning. The only quality exposure B introduces is a plan moving from Tier 2 to Tier 1, and section 1 bounds that set.

**4. The exposure is advisory.** The consumers that can see the change are `sc:workflow` Wave 4 and the standard-depth phases of Stage 10.5, both advisory on the verdict (E-9). The blocking post gate cannot see it. A Tier 1 stop on a sparse plan, with the header WARN, costs a possible missed advisory finding; it cannot let a bad phase through a gate.

**5. Why the count must wait, in both outcomes of H-A.**
- If H-A fails (Tier 2 recall is not 15 points above Tier 1), the whole Tier 2 spend is in question, not a third of it. Cutting one reviewer would then be a small saving on spending that should shrink in frequency or purpose; MR:527 already names the rubric as the alternative lever. Deciding the count first would answer the smaller question.
- If H-A passes, the question becomes what the third reviewer adds over the second inside reflect (with blind calibration and debate). Nothing recorded measures that: E2's two-versus-three result is from a different workflow (spec-panel critique, deterministic merge, no calibrator, no debate, one gateway) and is worded by E2 as "indistinguishable at this sample size" (`CR:381`, n=4 to 6 per panel), which is a statement about power, not about equivalence (E-14, E-15).
- In both branches the decision needs data B arranges to collect; taking it earlier can be right only by luck. This is the same ordering the unified-design verdict reached on the evidence (`R11` §12 verdict).

**6. B does not depend on any open conflict.** The cap is reflect-profile code, the rubric is reflect skill text, and the count is template data. None depends on C03 (model and tier configuration), C05 (who decides blocking) or C13 (ledger model). The design can proceed in parallel with them.

**7. Why E2's own conclusion points the same way.** E2 found every replicated panel at 1.6 to 2.5 of 14 and named input and harness fixes as "the biggest lever" (`CR:428`). The analogue in reflect is that Tier 2 is being triggered by an input property (labelling) rather than by plan risk. B fixes the trigger before arguing about the width of the panel the trigger sends work to. This is an analogy from a different tool, not a measurement of reflect, and is labelled so.

## Risks and mitigations

### The weakest point, stated first

**The pre-filter is a much smaller cost lever than the synthesis says, and the one clear-cut case in the history is a counterexample.** The "35 of 39" figure counts runs where the flag was set, not runs where the flag decided anything. Recounted by escalation path, 29 of the 34 sparse Tier 2 runs also match escalate row 4, 5 or 6, so removing the flag would not have changed them; the flag was the only reason in 1 run for certain and in at most 5 of 39 (E-5). In that one run (`fixTheScIssueWor`, E-6) Tier 2 found a blocking finding the Tier 1 card did not contain. Three consequences, none softened:

1. On today's data gate G1 does not open: there is one clear-cut candidate and it shows a Tier 2-only blocker. B's own recommendation is therefore to build the Phase 1 change behind the H-A pilot rather than ship it as default behaviour now.
2. If Phase 1 never ships, what B has delivered is: a corrected attribution of Tier 2 cost, instrumentation that records it per run, a frozen cap with a written decision rule for the count, and a measurement plan. That is closer to Option C (status quo) than the synthesis wording suggests, and the honest difference from C is the instrumentation, the pre-registered rule and the gate, not a cost saving.
3. The larger recorded drivers are rows 4 and 6 (18 and 9 of 39), not the flag. B measures them (the replay script tallies them) but does not edit them, because no evidence in the research says that treating tests and docs as separate domains, or a calibrated confidence under 0.85, is a bad reason to escalate. If the owner wants a real cost cut from the rubric, the next step is a measured change to row 4 or 6 under the same gate, and that is a different proposal.

### Other risks

| # | Risk | Evidence | Mitigation | Residual |
|---|---|---|---|---|
| R1 | A sparse plan stops at Tier 1 and a real blocker is missed | E-6 (n=1). The loss class in E-6 (acceptance criteria that pass on empty `git diff` output) is one no rubric input can predict. | Gate G1; Tier 1 stop only through rows 1, 2 or 8 with the union floor; header WARN; consumers advisory (E-9); `--tier 2` and `--depth deep` still force Tier 2; text revert restores the old rule. | A missed advisory finding on up to 13 percent of plans if Phase 1 ships. |
| R2 | Pass 2 under-extracts and the union coverage looks complete | E-7: T2's qa reviewer reads the full spec body for exactly this case (`refs/reviewer-spec.md:55`, via `R06` §2.3). T1 has no second reader. | Union floor; every inferred row must carry a quote and citation or it is dropped. If the G1 table or the pilot shows under-extraction misses, add a deterministic probe (count of MUST/SHALL lines in the source against rows emitted). Not built now: scope discipline. | Unmeasured. |
| R3 | The recount is built on model-written files | `fired_rule_number` and inputs are recorded by the orchestrating model across skill versions (E-5). | The replay script reports "not evaluable" when inputs are missing and never guesses; the prospective `sparse_flag_decisive` key is computed the same way in every future run. | The 3 unresolved runs stay unresolved. |
| R4 | Phase 1 changes the strata the H-A pilot must report | MR:540 strata and `PD` T-7 quota. | The new `escalation_path` key gives each stratum a recorded value; the pilot's arm A (`--tier 1` pin) is unaffected by the rubric because a pin outranks it. MR:540 already requires the "escalated by the parsed-sparse pre-filter" stratum to be reported apart; B adds only the recorded key that makes it computable. | Slightly larger pilot report. |
| R5 | Fewer Tier 2 runs slow the Stage 2 shadow count | Stage 2 needs 20 shadow runs (13 counted, `R11` §8). | E-10: shadow runs use `--tier 2` pins, so the rubric does not gate them. | None found. |
| R6 | The cap of 3 is applied unevenly | E-3: the post wrapper still clamps to 4; the generic default has 4 (E-4). | Recorded, not changed: C17 owns the post path and C03 blocks the document default. B states that "cap 3" means the reflect profile and `N_eff`. | Two paths disagree until C17. |
| R7 | The owner reads "fix the rubric first" as permission to rewrite rows 4 or 6 | See the weakest point. | The design text lists rows 3 to 7 as unchanged and the replay script as read-only. | Scope creep is an owner decision. |
| R8 | H-A is expensive and never gets run, so the count never gets decided | `PD` C-5: 1.30M to 2.62M claude tokens for the pilot, grading unpriced. | The count stays at the current default (3), which is the safe state; the decision rule is on file so a later run needs no new design. | Continued full-width Tier 2 until then. |
| R9 | Doc drift: several documents repeat "34 of 38 escalated because of the pre-filter" | MR:142, MR:556, `PD` quota paragraph, `R11` §12 item 4. | Phase 0 posts the E-5 table and each repeating statement gets a pointer to it. | Documentation work only. |

## Test coverage needed

### Existing tests that change

None. E-8: no test under `tests/` reads the §5.3 table, the pre-filter text or `tier_decision.yaml`; the only `coverage_degraded` hits are a field-name list in `panel_lint.py:46` and one `coverage_degraded: null` fixture line. The D13 eval fixtures named at `refs/grader-extensions.md:353-359` are an authoring contract; no `sparse-labeled-spec` case exists under `.dev/eval-workspaces/sc-reflect/cases/`. The honest reading is that today nothing pins the behaviour B changes, which also means nothing would catch an accidental change.

### Existing tests that must stay green (guards)

| Test | Why it guards B |
|---|---|
| `tests/review/test_review_panel_reflect_profile.py` (17 tests; cap at `:145-147`, `:170`, `:199`) | The cap of 3 and the generic range stay. |
| `tests/review/test_review_reflect_templates.py` (21) | The six `reflect-*` templates stay at three slots or fewer. |
| `tests/cli/reflect/test_panel_contract_lint.py` (38) | `STABLE_FIELDS_1_8_0` (`panel_lint.py:33-63`) still lists `coverage_degraded`, `coverage_pct_union` and `escalation_rule_matched`; B adds and removes no contract field. |
| `tests/cli/reflect/test_shadow_exit_script.py` (20), `test_shadow_skill_contract.py` (11), `test_verdict_replay_script.py` (13) | Stage 2 counting and brief-template pins are untouched. |

Counts are from `research/12-test-pins-regression.md` §1 and §2.

### New tests

| # | Test | Phase | What it asserts |
|---|---|---|---|
| N1 | `tests/cli/reflect/test_tier_replay_script.py` (new) | 0 | On a temporary runs root of synthetic `tier_decision.yaml` files: flag set plus row 4, 5 or 6 gives `prefilter_and_row_<n>` and `sparse_flag_decisive: false`; flag set plus row 8 and no escalate row gives `sparse_flag_decisive: true`; a `--tier 1` or `--tier 2` pin gives `pin` or `hard_override` and `null`; a file missing the inputs gives "not evaluable" and is never counted as decisive; the tally rows add up to the number of files read; shadow run directories are skipped by default. Modelled on `tests/cli/reflect/test_shadow_exit_script.py` and `test_reflect_stage0a_replay.py`. |
| N2 | Same file, one test against the real history | 0 | Marked to skip when `.dev/reflect` is absent. With it present, the script reproduces the E-5 numbers (39 files, 38 Tier 2, 35 flagged, 29 flagged runs with a recorded escalate row 4, 5 or 6, 5 flagged Tier 2 runs with none, of which 1 is clear-cut), so the table in this proposal is re-derivable by anyone. |
| N3 | `tests/cli/reflect/test_rubric_skill_text.py` (new) | 1 | Text pins on `SKILL.md`, in the style of `test_shadow_skill_contract.py:146-165`: rows 1, 2 and 8 carry no `NOT coverage_degraded`; the union-floor sentence is present; the pre-filter precedence paragraph still names `coverage_undefined` and `surface_unreached`; Step 1B.2b still sets the flag and no longer says "FORBID the Tier-1 stop"; `contract_version` stays 1.8.0. Limit, stated plainly: this pins prose, like the C7 brief pin (`R06` §2.1), not what the orchestrating model does. |
| N4 | Eval cases under `.dev/eval-workspaces/sc-reflect/cases/` (new; replaces the unbuilt `sparse-labeled-spec` contract at `refs/grader-extensions.md:357`) | 1 | Four cases run through the eval harness: sparse plan, clean rows, union at or above the floor, expect `tier_reached: 1` and the WARN; sparse plan with row 4 expect Tier 2; sparse plan with union below the floor expect Tier 2; sparse plan with `--tier 1` unchanged. Plus the existing `coverage_undefined` route still ends at Tier 2. These are model-run, so they check behaviour only to the reliability of that harness. |
| N5 | H-A pilot strata (not a pytest) | 2 | The pilot report splits results by `escalation_path` (MR:540) and states Tier 1 versus Tier 2 recall on the "sparse flag decisive" stratum separately, which is the measurement G1 could not supply. |
| N6 | E2-harness miss-rate check | 2 | Only after the portability fixes `R11` §3 and §12 list (hard-coded `/tmp` and worktree paths, a silently dropped audit filter, the fallback overwrite of `expected_model`); a reflect consumer must also be added. Whether the three E2 packages are sparse is not verified here. |

Run commands: `uv run pytest tests/cli/reflect/test_tier_replay_script.py -v`, then `uv run pytest tests/review tests/cli/reflect -q` for the guards. SKILL.md edits go in `src/superclaude/skills/sc-reflect-protocol/`, then `make sync-dev` and `make verify-sync`; `.claude/` copies are never staged.

## Cost

| Item | Size | Basis |
|---|---|---|
| Phase 0: two audit keys in `SKILL.md` §5.4, `scripts/reflect_tier_replay.py`, tests N1 and N2, annotations on the repeating "34 of 38" statements | S | One script of the size and shape of `scripts/reflect_shadow_exit.py` (collect, then report); no model calls. |
| Phase 1: edits at `SKILL.md:284`, `:431-432`, `:443`, `:454`, `:741`; `refs/coverage-mapping.md:77-79`; `refs/report-template.md:24`; `refs/grader-extensions.md:353-359`; `CHANGELOG.md`; tests N3 and N4; `make sync-dev` and `make verify-sync` | S | Text edits in one skill; no Python in the reviewer path. |
| Phase 1 and 2 together on the synthesis's scale | M | Matches the synthesis's own "Effort: M" for Option B (`synth-04:921`). |
| Phase 2: H-A pilot | 1.30M to 2.62M claude tokens (3.61M to 7.24M under the other reading of the repeats); confirmatory 2.41M to 4.88M; grading, seeding and orchestration unpriced | `PD` C-5, C-5b, C-6, SD-8 [DOC-SOURCED]. Not specific to B: any option that decides the count needs it, and Option A is rated "High risk, unmeasured in reflect" for lack of it. |
| Phase 2: one added two-reviewer arm | about 210k to 420k claude tokens for 6 plans | Own arithmetic by analogy with `PD` row C-3 (6 plans at 35k to 70k each). An estimate; the arm is not designed yet. |
| Grader cost reference | about 115k output tokens per scoring in E2's pilot | `PR:52` via `R11` §5, doc-sourced and not checked against raw `judge.json`. Reference only. |

**What B saves, honestly.** Per Tier 2 run avoided: roughly 90,000 to 367,381 output tokens, estimates from orchestrator accounting that the combo documents mark "do not compare" (`R11` §12 table). On the recorded history B can avoid between 1 and 5 Tier 2 runs of 39, so about 0.09M to 1.8M tokens over that history, an order of magnitude and not a billed figure. If gate G1 sends Phase 1 behind the pilot, the saving in the interim is zero.

**What B costs by waiting, honestly.** Option A would remove one reviewer from every Tier 2 run (38 of 39 in the history). The share of a Tier 2 run that one reviewer accounts for is not recorded separately in the files read, so the forgone saving is not quantified here. It is real, it is bounded by the width of one reviewer on runs whose total value is itself unmeasured (H-A), and it is recoverable at any time by a template-data change (`reflect-lite` under `--strict-distinct` already resolves to two reviewers).

**Running cost after Phase 0.** Two extra keys per `tier_decision.yaml` and one read-only script run on demand.

**Where B sits against the other two options at `synth-04:901-941`.** Against A: B changes at most 13 percent of runs and no reviewer counts, against all 38 Tier 2 runs for A, and it produces the measurement A also needs. Against C: B adds the instrumentation, the corrected attribution, a pre-registered count rule and a gate, at S to M effort; if the gate stays closed, the behaviour is C's and the difference is the information.

