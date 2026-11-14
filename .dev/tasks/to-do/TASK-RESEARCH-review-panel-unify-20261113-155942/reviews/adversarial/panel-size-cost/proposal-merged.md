<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (Proposal B, Option B) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original, modified) - H1 rewritten to the merged position / Change 5, A-1 -->
# Merged proposal for C14 (panel size versus cost): corrected cost attribution, instrumentation first, and an owner-gated skill-path default of two reviewers (Decision D-1)

<!-- Source: Base (original, modified) - header lines updated for the merge / A-1 -->
**Conflict:** C14, panel size versus cost (slug `panel-size-cost`), `synthesis/synth-04-options-conflicts.md:893-954`.
**What this is:** the merge of Proposal A (Option A, two reviewers by default) into Proposal B (Option B, fix the rubric first, keep the cap at 3), with Proposal B as the base. Both drafts, the debate, the invariant probe and the refactoring plan are in `adversarial/` next to this file.
**Date of this merge:** 2026-11-14. The drafts were written on 2026-11-13 at repository `792cf8c52` on `ironbelly/shadow-runs`.

**Tags used.** `[CODE-VERIFIED]` = read in the checkout. `[CODE-VERIFIED in data]` = counted from recorded run files under `.dev/reflect/`. `[DOC-SOURCED]` = taken from a report's own text, not recomputed. `[EXTERNAL]` = outside the repository, with URL. `[UNVERIFIED]` = decides nothing. `[PROPOSED]` = a name, number or rule proposed in this document, not an existing key or threshold and not settled in the debate. `owner parameter` = a value the owner sets. E2 evidence is cited only from commit `4a22d74213f93837d00c2c314075dd967b9a98e3`.

<!-- Source: Base (original) - citation forms, extended with the adversarial-run artifact names / A-7 -->
**Citation forms.** `SKILL.md` = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. `MR` = `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`. `PD` = `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/pilot-design.md`. `R11` = `research/11-evaluation-evidence.md` and so on for the other research files, all under `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/`. `W01` = `research/web-01-panel-aggregation.md`. `CR` and `PR` = E2's `COMBO-REPORT.md` and `PILOT-REPORT.md` under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/` at the pinned commit. `INV-nnn` = a finding in `adversarial/invariant-probe.md`. `C03`, `C05`, `C13`, `C17` = other conflicts of the synthesis; `G-nn` = rows of the gaps log. `S-nnn`, `C-nnn`, `X-nnn` = diff points of `adversarial/diff-analysis.md`, and `A-nnn` = its shared assumptions, those used here being (A-001 representativeness of the 39 runs; A-002 no stated trade-off threshold; A-003 the value of Tier 2 sits in reviewer count; A-004 the two levers are independent; A-006 the recorded rubric fields are accurate; A-007 skill prose is followed; A-008 E2 transfers to reflect). `Change N` = the numbered change of `adversarial/refactor-plan.md` that the text or a table cell traces to. Risk ids: `R1` to `R9` are the base draft's risks and `RD-1` to `RD-5` are the D-1 risks; `R04`, `R11` and similar zero-padded or two-digit ids with a section sign or "line" are research files. Terms used in this proposal: H-A is the pilot that compares Tier 2 recall with Tier 1 recall on seeded defects (MR:527); O-8 is the open question of tuning the rubric or waiting for H-A before the count is decided (MR:556); D13 is the change that added two-pass requirement extraction and the union coverage fields (`CHANGELOG.md:439-445`); UC-1 is the pre-execution audit and UC-2 the post-execution audit.

<!-- Source: Base (original, modified) - new status block so a reader sees decided, recommended and open at once / Change 14, A-13 -->
**Status in one place.**
- **Decided by the evidence in the debate:** the escalation figure (the parsed-sparse flag was set in 35 of 39 recorded non-shadow runs and 34 of the 38 Tier 2 runs and was decisive in 0 certain and at most 1, with caveats: model-written fields, only 7 of 39 files record `S_domains`, and the five ambiguous runs resolve as E-5 shows); the reading of the E-6 run (the invariant probe found its blocker, not a reviewer and not the flag); the removal of the rubric edit from committed scope (Conditional item CI-1); the replacement of the retrospective replay by prospective audit keys plus a recompute check.
- **Proposed for the owner's decision (not adopted):** Decision D-1, a skill-path default of two reviewers, on the conditions listed there. Both advocates favoured this narrowed change after Round 2; the invariant probe then found three HIGH gaps in that consensus, which D-1 turns into conditions. Risk: High (quality at two reviewers is unmeasured inside reflect). **Recommended within D-1:** option (a) for the task-builder POST gate (the runner passes `--reviewers 3`).
- **Open:** see "Open decisions and unresolved conflicts" at the end. Six debate points are UNRESOLVED, ten invariants are UNADDRESSED (three HIGH), and eight owner decisions are pending. Convergence status is BLOCKED_BY_INVARIANTS.

<!-- Source: Base (original, modified) - Design rewritten around the merged position / Changes 3, 5, 7, A-1 -->
## Design

**One-sentence position.** Correct the cost attribution and record the escalation rows at decision time now; put a skill-path default of two reviewers to the owner as Decision D-1, with the conditions the invariant probe added; leave the parsed-sparse flag as it is unless the recorded keys reopen it (Conditional item CI-1); and decide two against three on a pre-registered, symmetric rule once an H-A arm exists.

### What the design decides

| Question | Answer |
|---|---|
| Reviewer cap for reflect Tier 2 | Unchanged at 3. No code change: `_REFLECT_MAX_REVIEWERS = 3` already rejects larger templates and resolutions. |
| Default reviewer count, skill path | Decision D-1 (owner-gated, `[PROPOSED]`): 3 to 2 at `SKILL.md:86` and the coupled sites. `--reviewers 3` and `--strategy enterprise` remain opt-ins. If D-1 is not accepted the default remains 3 and the count is decided by the pre-registered rule. |
| Default reviewer count, code engine (`commands.py:270-274`, `config.py:264`) and the clamp (`config.py:335`) | Unchanged. The engine feeds the blocking per-phase post gate; both advocates conceded the engine default should remain 3 until a pilot arm exists. The clamp (G-67) is owned by C17. |
| Stage 2 shadow runs | At 3 today; kept at 3 by a conditional default if D-1 is accepted (D-1 condition 1). The exit gate (`scripts/reflect_shadow_exit.py:244-245`) is unchanged. |
| Task-builder default POST gate (blocking, skill path) | Named and decided under D-1. Recommended: option (a), the runner passes `--reviewers 3`. |
| Pre-filter `coverage_degraded: parsed-sparse` | Unchanged in this proposal. Making the flag advisory is Conditional item CI-1, reopened only by the recorded keys. |
| Other pre-filters (`coverage_undefined`, `surface_unreached`), pins, hard overrides | Unchanged. |
| Rubric rows 3 to 7 | Unchanged. They are recorded at decision time and checked by a recompute script, not edited. |
| Document-review default template (4 reviewers) and `live7` (7) | Out of scope for C14. Their count is template data and is blocked by C03; whether they follow D-1 is an owner decision. |

### Staging

- **Step A (no behaviour change, no model cost).** Add prospective audit keys to `tier_decision.yaml` and a read-only recompute check that detects a model-written wrong row. Add pointers on the documents that repeat the old attribution. This also corrects the attribution that O-8 and MR:142 rest on (see E-5).
- **Step B (owner decision; behaviour changes only if accepted).** Decision D-1.
- **Step C (measurement).** Run H-A with three explicitly pinned arms (Tier 1, Tier 2 with two reviewers, Tier 2 with three) and decide the count by the rule written in advance (see "Count decision").
- **Conditional, not staged.** CI-1, the advisory flag. It has no place in the committed plan because the flag was decisive in 0 certain and at most 1 of 39 recorded runs.

### Core and consumer modules

<!-- Source: Base (original, modified) - consumer table corrected: blocking task-builder gate added, "no exposure" wording replaced / Change 7, A-1 -->
| Module | What this proposal does |
|---|---|
| Shared core (panel resolver, manifest, clusterer, verdict) | No change. The profile cap stays in `panel.py` (reflect profile 3; generic panels keep their 1..8 range). The manifest records `reviewers_requested` and `reviewers_resolved` only for panel-engine (shadow) runs: the legacy skill path, where a skill default applies, writes no `panel/manifest.json` (14 manifests against 91 `pre-*` directories, INV-009). `manifest.py:314-315` raises `Invalid` when resolved exceeds requested (INV-001). |
| Reflect module (pre mode) | Step A edits `SKILL.md` §5.4 (audit keys). D-1, if accepted, edits the sites listed under "Every place that states the count". CI-1 edits are listed under Conditional items and are not committed. |
| Workflow tasklist module (`sc:workflow` Wave 4) | Advisory. Its call (`/sc:reflect --mode pre` with default flags) is unchanged. Under D-1 it runs at two reviewers by default. |
| Tasklist module, Stage 10.5 pre sign-off | Advisory on the verdict. It passes a computed `--depth` and `--tier`, not `--reviewers`. Under D-1 it runs at two by default. |
| Tasklist module, per-phase post gate (blocking, engine path) | Runs `--depth deep` through the code engine (`run_tier2_ensemble`), not through the rubric and not through the skill default. Neither Step A nor D-1 changes it: the engine default and the clamp are unchanged. |
| Task-builder default POST gate (blocking, skill path) | Added by this merge (INV-012). The default `reflect_post_mode: skill` gate invokes `Skill sc-reflect-protocol --mode post --remediate --depth {DEPTH}` with no `--reviewers`; an unresolved Regression or unauthorized Drift halts the task (`src/superclaude/skills/task-builder/SKILL.md:2217-2236`). D-1 would move it to two reviewers silently unless the owner picks option (a). |
| User-run commit gate | `/sc:reflect --mode post` is named as the pre-commit gate "the user runs" (`sc-troubleshoot-protocol/SKILL.md:594-601`, `commands/troubleshoot.md:207,217`); human-gated. Under D-1 it runs at two. [DOC-SOURCED from the debate and probe; not re-read for this merge] |
| Spec review loop (E3 default 4 reviewers, `live7` 7) | No position under C14. Its count is a template-data edit, and the model E2 chose for its default is not nameable by any packaged tier today, so the question is blocked on C03. |
| Future modules (PR review, rf-qa) | Inherit "cap is profile data, count is a template choice made on measured evidence". Nothing to build now. |

<!-- Source: Base (original, modified) - data flow rewritten: flag edit removed, recording step and recompute added / Changes 3, 4 -->
## How it works

### Data flow for a `/sc:reflect --mode pre` run

1. **Wave 1, extraction.** Step 1B.0 runs its two passes (deterministic ids, then quote-pinned inference) and yields `parsed_count`, `inferred_count`, `coverage_pct` (parsed only, null when no ids were parsed), `coverage_pct_union`, `unmapped_requirements_union` and `S_dev_density` over the union set. Unchanged.
2. **Step 1B.2b, flag.** When `inferred_count > parsed_count` it sets `coverage_degraded: parsed-sparse` in the report header, `tier_decision.yaml` and the return contract, and the flag still forbids a Tier 1 stop. Unchanged by this proposal (see CI-1 for the conditional edit).
3. **Wave 2, rubric §5.3.** Rows 1 to 8 are unchanged. The rubric is "applied in order; first match wins" (`SKILL.md:427`), so the recorded `fired_rule_number` hides every other row that also matches. At decision time the orchestrator now also writes the audit keys below. Blind calibration (Wave 1D, `SKILL.md:154`) runs before the rubric, so the calibrated Tier 1 confidence is available at that point.
4. **Offline check.** A read-only script recomputes the first-match row from the recorded inputs and reports "agree", "disagree" or "not evaluable" (see "CLI surface"). It exists because the field is model-written: the E-6 run recorded row 8 beside its own calibrated confidence of 0.68.
5. **If the final tier is 2.** Legacy rotation or, with `--t2-engine shadow`, the panel; `N_eff <= 3`; the fixed anchor is never dropped. Under D-1 the skill-path default is two reviewers, and three when the effective engine is shadow (see D-1).
6. **Measurement.** The H-A pilot and the E2 harness are the instruments for the count (Step C).

### Contract and audit fields

<!-- Source: Base (original, modified) - field table: advisory-flag prose row removed (moved to CI-1); keys re-specified / Changes 3, 4, 9, A-4, A-8, A-13 -->
| Field | Where | Change |
|---|---|---|
| `coverage_degraded`, `coverage_pct_union`, `unmapped_requirements_union`, `coverage_undefined` | return contract 1.8.0 (listed in `panel_lint.py:46`) | None. Same names, same values, same prose. `contract_version` stays 1.8.0. |
| `matching_rows: [..]` | `tier_decision.yaml` (audit-only key) `[PROPOSED]` | All rubric rows whose condition held, not only the first match. |
| `calibrated_C_t1` | `tier_decision.yaml` (audit-only key) `[PROPOSED]` | The blind-calibrated Tier 1 confidence, copied from the card at decision time. |
| `S_domains_basis` | `tier_decision.yaml` (audit-only key) `[PROPOSED]` | The `S_domains` count and the paths it was counted from (code, tests, docs). |
| `tier_without_flag` | `tier_decision.yaml` (audit-only key) `[PROPOSED]` | The tier the rubric would give with the flag ignored; derived from the keys above by the recompute. |
| `sparse_flag_decisive: true \| false \| null` | `tier_decision.yaml` (audit-only key) `[PROPOSED]` | `true` when Tier 2 was forced only because of the flag (no escalate row 3 to 7 matched, no pin applied); `null` when a pin or hard override decided. Kept from the base draft; computed by the same recompute. |
| `escalation_path: prefilter_only \| row_<n> \| prefilter_and_row_<n> \| pin \| hard_override \| t1_stop` | `tier_decision.yaml` (audit-only key) `[PROPOSED]` | Gives MR:540's strata ("escalated by the parsed-sparse pre-filter" against "by rule 4, 5 or 6 without it") a recorded value. Kept from the base draft. |
| `reviewers_requested`, `reviewers_resolved`, `reviewers_source: default \| flag \| enterprise \| shadow-pin \| clamp` | `telemetry:` in the contract (precedent `SKILL.md:349`, `:469`) | Three separate fields replace A's single boolean `reviewers_default_applied`, which breaks in three cases: `--strategy enterprise` with no `--reviewers` (count 3, default applied), an explicit `--reviewers 3` clamped to 2 by D5, and the conditional shadow default (INV-002). The enumeration of `reviewers_source` is `[PROPOSED]`. |
| `executor_exclusion_degraded`, `anchor_replaced`, `depth`, `calibrator_diversity` | `telemetry:` (strata for the H-A arms) | Existing values recorded as strata so arm membership is unambiguous (INV-010). |

The key names marked `[PROPOSED]` are not existing keys. `SKILL.md:469` already states that audit keys of this artifact are not contract fields and leave `contract_version` at 1.8.0 (the three `t2_engine_*` keys are the precedent), so no contract bump is needed.

<!-- Source: Base (original, modified) - CLI surface: replay script replaced by the recompute check / Change 4, A-4 -->
### CLI surface

- No new `superclaude` subcommand. The only flag change is the default of `--reviewers` on the skill path, and only if D-1 is accepted.
- The kill switch already exists: `--tier 2` or `--depth deep` forces Tier 2 whatever the rubric says (`SKILL.md:405-408`); reverting skill text restores the old behaviour.
- One small read-only check beside `scripts/reflect_shadow_exit.py`, proposed name `scripts/reflect_tier_recompute.py` `[PROPOSED]`, run with `uv run python`. It recomputes the first-match row from recorded inputs, in this order: (1) the blind-calibrated Tier 1 confidence from `reflection-card.yaml` `C:` or `artifacts/t1-calibration.yaml` (existing key names vary: `calibrated_confidence_t1` in 1 file, `calibrated_confidence` in 2, `confidence_calibrated` in 5, so it reads the card, not only `tier_decision.yaml`); (2) `S_domains` and `S_dev_density` from `t1-card.md`; (3) `artifacts/input-snapshot.yaml` for path-based domain counting (code, tests, docs). Anything else is reported "not evaluable", never guessed. It reports disagreement; it does not repair a recorded row.
- `superclaude review panel resolve` and the packaged `reflect-*` templates are unchanged.

<!-- Source: Round 2 rebuttal (advocate A and advocate B) - Change 10, A-9; base steps 2 and 3 kept -->
### Count decision (pre-registered)

Pre-registered, reusing the thresholds already in `PD` (T-1 and T-2). The rule below is symmetric and its wording is `[PROPOSED]`; the margin, the minimum sample size and the cost measure are owner parameters.

1. **Arms.** Tier 1 (`--tier 1`), Tier 2 with two reviewers (`--reviewers 2`) and Tier 2 with three reviewers (`--reviewers 3`), each pinned explicitly so that a shipped default cannot shift what H-A measures (A-004). Arm membership is read from the three count fields and the strata above, so executor-exclusion runs, enterprise runs and shadow-pin runs are not mixed into an arm (INV-010).
2. **If H-A passes T-1** (Tier 2 recall at least 15 points above Tier 1 on seeded defects): the incumbent default is kept unless the other arm beats it. Two replaces three only if the two-reviewer arm is within the owner's margin of the three-reviewer arm (one-sided 95 percent bound) and costs less in calls and, where measured, tokens. Three replaces two only if the three-reviewer arm is better than the two-reviewer arm by more than the owner's margin. The incumbent is two if D-1 was accepted and three if not.
3. **Inconclusive outcome, stated in advance.** If the sample is below the owner's minimum, or the bound straddles the margin, the incumbent stays. E2 at n=4 to 6 per panel could not separate panels (p 0.54 to 1.0, `CR:381`); the power of a 6-plan arm to resolve a 10-point margin is `[UNVERIFIED]`.
4. **If H-A fails** (kept from the base draft; MR:527): the owner chooses between shrinking Tier 2 to two reviewers and tuning the rubric, and the Step A keys are the input to the "tune the rubric" branch.
5. **Raising the cap above 3** stays closed unless H-A passes (MR:289, marked PROPOSED there; kept from the base draft).
6. **Cost and ownership.** Pilot 1.30M to 2.62M claude tokens (3.61M to 7.24M under the other reading of the repeats, C-5b), grading unpriced, and no owner for the E2 benchmark port yet (G-59). A two-reviewer arm needs no new template on the skill path: the N=2 row of the rotation table exists (`SKILL.md:654`).

The base draft's 10-point margin was, in advocate B's words, "the advocate's own invention" (`adversarial/debate-transcript.md`, Round 1 concessions); the merged rule makes it an owner parameter.

<!-- Source: Base (original, modified) - Evidence section: E-5, E-6, E-9 and E-11 replaced; E-1 to E-4, E-7, E-8, E-10, E-12 to E-18 kept / Changes 1, 2, 7, A-7 -->
## Evidence

### The cap and the count (what already exists)

<!-- Source: Base (original) -->
- **E-1. The cap of 3 is code and is tested.** `_REFLECT_MAX_REVIEWERS = 3` at `src/superclaude/cli/review/panel.py:73`; the template check at `:130-133` and the resolution check at `:143-146` reject more; the docstring at `:83-88` says generic panels keep their 1..8 range. Tests: `tests/review/test_review_panel_reflect_profile.py:145-147` (a reflect template with 4 reviewers fails with "at most 3", the same shape as a generic panel passes), `:170` (a `ValueError` matching "at most 3"), `:199` (a generic panel with four reviewers stays valid). [CODE-VERIFIED] Research: `R04` §4.3.
- **E-2. The skill text agrees.** `--reviewers N` is "2-3; default 3" (`SKILL.md:86`, re-read for this merge) and decision D5 reads `N_eff = min(--reviewers, alias count, 3)` with the fixed anchor never dropped (`:321`). [CODE-VERIFIED]
- **E-3. The post-gate wrapper disagrees, and that is a separate path.** `src/superclaude/cli/reflect/config.py:335` clamps reviewers to `max(2, min(4, n))`. The blocking post gate reaches Tier 2 through `run_tier2_ensemble` (`runner.py:538-545`), not through the rubric or the panel (`R09` §4.2, §5; the `runner.py` line numbers are from `R09` and were not re-read). This is gap G-67; this proposal records it and leaves it to C17. [CODE-VERIFIED for `config.py:335`; the rest via `R09`]
- **E-4. The packaged document-review default has four reviewers.** `review-panel.default.json` slots: `t1b` x1 fixed, `t2` x1, `t3` x2; `live7` has seven (`R04` §4, rows `default` and `live7`). The model E2 picked for its default, `muse-ember-1.0`, "appears in neither aliases, names nor classes" of the packaged tier file (`R04` §4 tier-file bullet). [CODE-VERIFIED]

### Why Tier 2 is almost always paid, and what the pre-filter really accounts for

<!-- Source: Base (original, modified) - E-5 recount rewritten with the corrected figure and the "also fails Tier 1 stop by" column / Change 1, A-1 -->
- **E-5. The recorded history, recounted by escalation path.** Source: the 39 non-shadow `.dev/reflect/pre-*/artifacts/tier_decision.yaml` files (of 91 `pre-*` directories, 54 hold a `tier_decision.yaml` and 15 of those are shadow runs), tallied by `selected_tier`, `fired_rule_number` and `coverage_degraded`, then cross-checked against each run's calibration card and report for the ambiguous cases. [CODE-VERIFIED in data]

  | Recorded decision | Runs | Also fails a Tier 1 stop by |
  |---|---|---|
  | Tier 2, flag set, escalate row 4 recorded (`S_domains >= 3`) | 18 | Row 4 itself. |
  | Tier 2, flag set, escalate row 6 recorded (`C < 0.85`) | 9 | Row 6 itself (calibrated confidence). |
  | Tier 2, flag set, escalate row 5 recorded (`S_dev_density > 0.20`) | 2 | Row 5 itself. |
  | Tier 2, flag set, row 8 default recorded | 1 | The E-6 run: row 6 through its blind-calibrated `C` of 0.68 (`reflection-card.yaml`). The recorded row 8 contradicts the run's own card. |
  | Tier 2, flag set, row 0 | 1 | Row 4: its own reason text says `S_domains` 3 "would also escalate via rule 4". |
  | Tier 2, flag set, no row number recorded | 3 | Two resolve from `REPORT.md`: Tier 1 card calibrated 0.75 with `S_domains` 4 (rows 4 and 6), and Tier 1 card calibrated 0.53 (row 6). One is undetermined: Tier 1 card 0.86, text "`S_domains` may count 3"; path counting of its input snapshot (code, tests, docs) gives 3, so row 4 probably fires. |
  | Tier 1, flag set | 1 | The `--tier 1` pin (`pre-pr-submit-ci-monitor`). |
  | Tier 2, flag not set | 4 | Two forced by `--depth deep`; `pre-design-20261104164711` row 4; `pre-brainstormFixBri-20261106-001016` row 6. |
  | **Total** | **39** | Flag set in 35; Tier 2 in 38; flag set and Tier 2 in 34. |

  **Figure statement (the only form of the figure this document uses).** The parsed-sparse flag was set in 35 of 39 recorded non-shadow runs and 34 of the 38 Tier 2 runs and was decisive in 0 certain and at most 1. Caveats: `fired_rule_number` and the input values are written by the orchestrating model across skill versions from 2026-06 to 2026-11, so the table is a recount of recorded claims, not an independent re-execution of the rubric; only 7 of the 39 files record `S_domains` (6 record `S_dev_density`), so the 29 runs with a recorded row 4, 5 or 6 rest largely on recorded rule claims and reason text; and five runs were ambiguous and resolve as follows (run directory under `.dev/reflect/`):
  1. `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416`: recorded row 8; its card gives `C` 0.68, so row 6 fires. Not decisive.
  2. `pre-renameTheScIssue-20261104174640`: recorded row 0; own text says row 4 would also escalate. Not decisive.
  3. `pre-TASK-WF-makeTheAliasOnly-20261105-034531-20261105034821`: Tier 1 card calibrated 0.75 (`REPORT.md:6`), `S_domains` 4 (`t1-card.md:6`). Not decisive.
  4. `pre-TASK-WF-planTheRealBound-20261107-080351-20261107080543`: Tier 1 card calibrated 0.53 (`REPORT.md:6`). Not decisive.
  5. `pre-TASK-WF-planTheRealBound-20261107-080351-20261108-rerun`: Tier 1 card 0.86 ("would have stopped on confidence alone"), `S_domains` "may count 3". Undetermined and the only run where the flag could have been decisive; path counting suggests it was not.

  Why 29 runs do not depend on the flag: rows 1 and 2 need `S_domains <= 2`, `S_dev_density <= 0.10` and `C >= 0.85` (`SKILL.md:431-432`), so a plan that matches row 4, 5 or 6 cannot stop at Tier 1 whether or not the flag exists. Rows 3 and 3a apply to UC-2 only and row 7 needs the enterprise strategy [DOC-SOURCED from the debate]. Several documents (MR:142, MR:556, the `PD` quota paragraph and `R11` §12 item 4) attribute the Tier 2 count to the pre-filter or state an upper bound on runs that could have stopped at Tier 1; the table does not support them (see R9). Rows 4 and 6 (18 and 9 recorded runs) are the larger recorded drivers.

<!-- Source: Round 2 rebuttal (advocate A and advocate B) - E-6 recast as an observation about the probe / Change 2, A-003 -->
- **E-6. One run, and what it does and does not show.** `pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416`: `tier_decision.yaml` has row 8, `coverage_degraded: parsed-sparse` (5 inferred, 0 parsed), `S_scope` 3, `S_domains` 2, `S_dev_density` 0.0. Its `reflection-card.yaml` (lines 5, 12, 13) gives self-reported confidence 0.90, blind-calibrated `C: 0.68` and a calibration delta of -0.22, so row 6 escalates it with or without the flag. Its Tier 2 merge ended `merged_verdict: FAIL` with `blocking_findings: [M-13]` (`return-contract.yaml:62-63`). `adversarial/merged-verdict.yaml:74-80` records M-13 as `grounding_gap`, `severity: blocking`, source `invariant-probe:INV-001` of that run: the five target files are untracked, so three acceptance criteria that use `git diff` would pass on empty output. The Tier 1 card, the six reviewer card files and the three variant originals contain none of "untracked", "git status" or "ls-files" (zero hits). `source_variants` lists variants 1 to 3 only because they voted blocking in Round 2.6 (`merge-log.md:98` of that run). Reading: the blocker was found by the Round 2.5 invariant probe, not by a reviewer card, and not through the flag. This is one run. It shows the probe step has value; it does not show that a third reviewer has value, and it is not an argument against a flag change. It also shows a model-written field contradicting its own card (INV-013). [CODE-VERIFIED in data]

<!-- Source: Base (original) - E-7 and E-8 kept unchanged / A-7 -->
- **E-7. The mechanism and its stated reason.** Step 1B.2b forbids the Tier 1 stop when `inferred_count > parsed_count` (`SKILL.md:284`); rows 1 and 2 carry `NOT coverage_degraded` (`:431-432`); the precedence paragraph makes it table-wide (`:443`); `refs/coverage-mapping.md:77-79` repeats it; `CHANGELOG.md:439-445` introduced it together with two-pass extraction and the union fields. The same change made `S_dev_density` use the union denominator (`SKILL.md:278`, `:423`) and left `coverage_pct` parsed-only (`refs/coverage-mapping.md:67-76`). T2's qa reviewer is the one that reads the whole spec body "even if Pass 2 under-extracts" (`refs/reviewer-spec.md:55`, per `R06` §2.3). [CODE-VERIFIED]
- **E-8. Nothing pins the pre-filter.** `coverage_degraded` appears in Python under `src/` only at `src/superclaude/cli/reflect/panel_lint.py:46` (a list of contract field names). A search of all of `tests/` for `tier_decision`, `selected_tier`, `fired_rule`, `coverage_degraded`, `parsed-sparse` and `Step 1B.2b` finds two hits: `coverage_degraded: null` in `tests/cli/reflect/fixtures/panel_lint_legacy/return-contract.yaml:16`, and the words `tier_decision.yaml` inside the prose of a card fixture (`tests/review/fixtures/reflect_cards/markdown-lines.md:10`). The three D13 eval fixtures are specified in `refs/grader-extensions.md:353-359` (the `sparse-labeled-spec` case asserts `tier_reached: 2`), but no `sparse-labeled-spec` case exists under `.dev/eval-workspaces/sc-reflect/cases/` (directory listing). Nothing pins the default reviewer text either (a search of `tests/` finds none). [CODE-VERIFIED]

### Who is exposed to the rubric and to the count

<!-- Source: Base (original, modified) - E-9 corrected to name the blocking task-builder gate and the user-run gate / Change 7, A-1 -->
- **E-9. Consumers.** Advisory: `sc:workflow` Wave 4 runs `/sc:reflect --mode pre --spec <pkg>/source.md --tasklist <pkg>/<id>.md` with defaults (`sc-workflow-protocol/SKILL.md:89,93`, `R09` §3); Stage 10.5 passes computed `--depth` and `--tier`, also `--remediate`, and the bundle ships regardless of verdict (`sc-tasklist-protocol/SKILL.md:1619-1650`, `R09` §4.1). Blocking, engine path: the per-phase post gate is forced to `--depth deep` and runs `superclaude reflect run ... --depth deep` with no `--reviewers` (`sc-tasklist-protocol/SKILL.md:1155-1179`, `:1162`, `R09` §4.2), so it takes the engine default. Human-gated: the user-run commit gate (`sc-troubleshoot-protocol/SKILL.md:594-601`). **Blocking, skill path:** the task-builder default POST gate (`task-builder/SKILL.md:2217-2236`, re-read for this merge; INV-012), which the base draft omitted. By default Tier 2 on the engine path is the legacy rotation; the panel runs only with `--t2-engine shadow`, which no consumer passes (`R09` §5). [CODE-VERIFIED for the task-builder gate; the other consumer files via `R09`, the debate and the probe]
- **E-10. Shadow evidence is not exposed to the rubric.** The shadow runs reach Tier 2 mostly through the `--tier 2` hard override (for example `pre-TASK-WF-detachTheCcsessi-20261102-034618-shadow01`, `-shadow02`, `-shadow03`, `pre-TASK-WF-fixTheScIssueWor-20261104-162205-shadow05`: "hard override --tier 2, no rubric row evaluated"). A rubric change would therefore not slow the 20-run Stage 2 count. Under D-1 the shadow runs are exposed to the count default and must be pinned (D-1 condition 1). [CODE-VERIFIED in data]
- **E-11. Retrospective data is already read.** 22 of the 39 recorded run directories hold a `t1-card.md`, and every escalated run holds the Tier 2 verdict; the recount in E-5 and the resolution of the five ambiguous runs used them with no new model calls. The retrospective replay script of the base draft is not built because the recount is done (Change 4). [CODE-VERIFIED in data]

### Worth, cost and what E2 does and does not say

<!-- Source: Base (original) - E-12 to E-18 kept unchanged / A-7 -->
- **E-12. H-A is defined and not run.** MR:527 sets H-A at Tier 2 recall at least 15 points above Tier 1 on seeded defects and says that on failure "the owner chooses between shrinking T2 to 2 reviewers and tuning the rubric (O-8)"; MR:556 is O-8 ("decide after H-A"); `PD` T-1, T-2 and T-7. Cost rows in `PD`: pilot 1.30M to 2.62M claude tokens (C-5; 3.61M to 7.24M under the other reading of the repeats, C-5b); confirmatory 33 plans 2.41M to 4.88M (C-6); grading, seeding and orchestration are not priced (`PD` SD-8). [DOC-SOURCED, rows re-read]
- **E-13. Shape of the arms.** `PD` arms A (T1 `--tier 1`), B (legacy T2), C (development-build panel), D (`@reflect-lite`, 6 of the 12 plans, "to price the Opus-moves ablation"). None is a two-versus-three comparison on its own terms. `PD` requires at least 25 percent non-sparse plans because only 4 of 38 recorded decisions were non-sparse (`PD` quota paragraph; MR:540). [DOC-SOURCED]
- **E-14. E2's ceiling is flat in panel size, in E2's setting.** Replicated panels score 1.60 to 2.50 of 14 known defects per run: `ember + sonnet` 2.50 and `ember + luna` 2.25 (both n=4), `haiku + 2x luna` 2.20 (n=5), `ember + 2x luna` 1.83 (n=6, 63,644 tokens) (`CR:315-320`, `CR:331`). No difference in found, real blocking, wrong blockers or control is significant between replicated panels, p 0.54 to 1.0, while token differences are (p 0.002 to 0.009) (`CR:381`). Only three statistics survive audit F, including that `2x luna + 2x ember` has 2.75 to 3.25 more wrong blockers (permutation p 0.005 to 0.03) (`CR:298`). [DOC-SOURCED; raw `score.json` not re-aggregated, G-82]
- **E-15. E2 itself ranks the input fixes above panel choice.** `CR:428`: "All panels sit at about 2-2.5 of 14, so the harness fixes (anchor limit, source.md path in the brief) remain the biggest lever." The study also never ran reflect, a calibrator or a debate (`R11` §6 "What the study measured and did not", §12 item 3), so its ceiling is not the Tier 2 ceiling. [DOC-SOURCED]
- **E-16. The pilot line "sonnet alone gives the most catches per token" is not a current fact.** Arm A 2/16 at 93,098 tokens was one run per package before `source.md` shipped (`PR:46-50` via `R11` §5; `R11` §6; gaps row D-57); cheaper valid-era panels beat it per 100k tokens (`CR:317`, `CR:331`). This proposal does not use it. [DOC-SOURCED]
- **E-17. Estimated cost of a Tier 2 run.** Orchestrator token estimates for shadow contracts run from 90,000 (wave 3 of shadow04) to 137,000 (shadow08) for wave 3 alone, and the combo runs spent 185,086 to 367,381 output tokens per whole run for combos B to E; these are estimates and the combo document says "do not compare" (`R11` §12 table, last row). Used here only for order of magnitude. [DOC-SOURCED]
- **E-18. External context, weak.** A self-published, not peer-reviewed corpus reports that the second reviewer is the largest coverage step and returns diminish after two to three: [EXTERNAL] https://zenodo.org/records/21328807 (`research/web-01-panel-aggregation.md:97-99,148`, reliability low to medium, read from the abstract only). A preprint of nine judges finds about two effective votes: [EXTERNAL] https://arxiv.org/html/2605.29800v1 (`web-01:59,145`; natural-language-inference tasks, not plan review). `web-01:164` (recommendation 9) reads three heterogeneous reviewers plus one adjudicator as the evidence-supported size. These support "not more than 3"; they do not choose between 2 and 3 for reflect.

<!-- Source: Base (original, modified) - sections 1 to 7 rewritten for the merged position; invariants table and "does not claim" list appended / Changes 1, 3, 5, 7, 11, A-1, A-10 -->
## Correctness argument

<!-- Source: Base (original, modified) - section 1 replaced: Step A changes no decision / Changes 1, 3, A-1 -->
**1. Step A changes no decision.** The audit keys are additive (`SKILL.md:466-470`; the three `t2_engine_*` keys are the precedent) and the recompute check is read-only. The rubric, the reviewer count, the cap and every contract field are unchanged by Step A, and `contract_version` stays 1.8.0. [follows from E-2 and the contract table, CODE-VERIFIED]

<!-- Source: Base (original, modified) - section 2 replaced: D-1 changes one default on one path / Change 5, A-1 -->
**2. D-1 changes one default on one path, and only if accepted.** The skill-path default (the flag text, the section 7.1 "(default)" label and the sentence that restores N=3 after executor exclusion) moves from 3 to 2. `--reviewers 3` and `--strategy enterprise` still give three. The code-engine default, the clamp, the exit gate, the templates and the cap are unchanged (E-1 to E-3), and the adversarial call stays at `--depth standard` (`SKILL.md:694-696`). The exact set of sites is the table under D-1.

<!-- Source: Base (original, modified) - section 3 replaced: "counts cannot change" no longer holds under D-1 / Change 5, A-1 -->
**3. Under D-1 the count does change, and three things depend on it staying consistent.** (a) Stage 2 shadow parity and the manifest guard: a skill default of 2 against the 3-slot `@reflect-pre` would make every shadow run compute `panel_parity: false` (`scripts/reflect_shadow_exit.py:139-142`, `:173-174`) and, worse, `manifest.py:314-315` aborts when resolved exceeds requested, so a shadow run that sees requested 2 is lost (INV-001). (b) The Stage 2 shortfall rule (`reviewers_resolved == 3` and `reviewers_complete == 2`, `scripts/reflect_shadow_exit.py:244-245`) keeps its meaning only while shadow runs stay at 3. (c) The adversarial call at `SKILL.md:695` hard-codes three card files and must name only the cards that exist (INV-004). These are the reasons for D-1's conditions; they are not satisfied by recording them here.

<!-- Source: Base (original, modified) - section 4 replaced: exposure is not purely advisory / Change 7, A-1 -->
**4. The exposure is not purely advisory.** The consumers that see D-1 are `sc:workflow` Wave 4 and Stage 10.5 (advisory), the user-run commit gate (human-gated) and the task-builder default POST gate, which is blocking (E-9, INV-012). The per-phase post gate, also blocking, is not touched: it runs through the code engine, whose default is unchanged at 3. For the task-builder gate the owner must choose between option (a) and option (b) (see D-1); until then the "no blocking path is touched" claim in the debate's consensus is false as written.

<!-- Source: Base (original, modified) - section 5 replaced: what can and cannot be known before an arm exists / Changes 5, 10, A-1 -->
**5. What can and cannot be known before an arm exists.** Production already runs two reviewers on a real share of runs: 9 of the 38 recorded Tier 2 runs ran two cards (E-19), so waiting for H-A before touching the default is not what production does today. What cannot be known before an arm exists is whether two matches three on recall inside reflect, with blind calibration and debate. E2's two-versus-three result is from a different workflow (spec-panel critique, deterministic merge, no calibrator, no debate, one gateway) and is worded by E2 as "indistinguishable at this sample size" (`CR:381`, n=4 to 6 per panel), which is a statement about power, not equivalence (E-14, E-15). If H-A fails, the whole Tier 2 spend is in question, not a third of it, and cutting one reviewer is the smaller question (MR:527 names the rubric as the alternative lever). D-1 is therefore presented as an owner-gated bet with a tripwire and a symmetric pilot, not as a measured result.

<!-- Source: Base (original, modified) - section 6 reworded to cover D-1 / A-1 -->
**6. Dependencies.** The instrumentation depends on no open conflict: the cap is reflect-profile code, the rubric is reflect skill text and the count is template data; none depends on C03 (model and tier configuration), C05 (who decides blocking) or C13 (ledger model). D-1 has two touch points: it leaves the clamp and the engine path to C17 (G-67), and whether the document-loop defaults (4 and 7) follow is C03's.

<!-- Source: Base (original, modified) - section 7: E2 analogy no longer used as support / Change 3 -->
**7. E2 is not used as support in either direction.** E2 found every replicated panel at 1.6 to 2.5 of 14 and named input and harness fixes as "the biggest lever" (`CR:428`). The base draft used this as an analogy for fixing the Tier 2 trigger before the panel width. After the recount the flag decided 0 certain and at most 1 recorded run, so the analogy has nothing to attach to, and E2 cannot be read as the Tier 2 ceiling (E-15, A-008).

<!-- Source: Variant A (Proposal A), Correctness section 1 - merged per Change 11; "verified for" column added per the plan -->
### Invariants preserved under D-1

"Verified for" says what was actually read. Resolver = the code in `panel.py` and the code engine. Legacy skill path = the prose in `SKILL.md` that dispatches on the default path today; nothing there is covered by a test of model behaviour (A-007).

| Invariant | Why it holds under a default of two | Where | Verified for |
|---|---|---|---|
| The anchor is never dropped | The fixed slot is resolved first and exhaustion of it is fatal, not skipped | `panel.py:536-537, :647-649` (`R04` §2); rule D5, `SKILL.md:321` | Resolver (code read). Legacy skill path: prose only. |
| Executor class is not a reviewer class | On the legacy path the rotation prose restores N after exclusion, but the sentence at `SKILL.md:658` covers only an executor of `sonnet`; wording for haiku and opus executors must be added (D-1 site table). Unknown executor stays fail-open as today (9 of 13 recorded shadow runs had it). On the resolver, a bare two-slot template drops to one reviewer when the executor shares the second slot's class (two independent dry runs; the executor-keyed templates that avoid it are parked) | `SKILL.md:648, :658`; `tests/review/test_review_reflect_templates.py:105-110` (the `x2` template, executor sonnet); `R11` §8 output line 266 | Resolver (dry run reproduced twice). Legacy skill path: not verified. |
| T2 stays T2 | `tier_reached` is 2 and `merge_method` is `adversarial` whenever at least two reviewers succeed; the diversity gate needs two distinct model ids | `ensemble.py:772-773`; `_diversity.py:8-15`; `R13` line 295 | Code engine (code read). Legacy skill path: not verified. |
| A Regression is debated by at least two reviewers | Two satisfies it | `SKILL.md:433`; `R05` line 81 | Legacy skill path (prose read); not tested. |
| Contract 1.8.0 stable keys are untouched | Arrays get shorter; new values go under `telemetry:` only; no version bump | `SKILL.md:349`, `:466-470`; lint L2 stable-key check in `panel_lint.py` | Lint code (tests exist for the stable-key list). Whether a legacy contract is honest about its own card count is not verified (INV-014: EV-1 reads the contract's own claim). |
| The cap of three holds | Unchanged; `--reviewers 3` and the enterprise strategy are the only ways to three on the skill path | `panel.py:73, :130, :143`; tests in E-1 | Resolver (code and tests read). |
| Failure is closed | Fewer than two completed cards is DEGRADED (`single-reviewer-fallback`; code engine `degraded-tier1`), never PASS | `contract.py:278-296`; `tests/cli/reflect/test_ensemble_stub_integration.py:251-277` | Code engine, tested at three reviewers (an N=2 mirror is proposed under Test coverage). Legacy skill path: not verified. |

<!-- Source: Variant A (Proposal A), Correctness section 3 - merged per Change 11, A-10 -->
### What this proposal does not claim

- It does not claim two reviewers are as good as three inside reflect. That is not measured anywhere (`R11` §12 item 3).
- It does not claim the saving is a third of a run. The saving is counted in calls, and E2's own table shows a two-reviewer panel costing as much as a three-reviewer one when the dropped reviewer was the cheap one: `ember + sonnet` 142,967 tokens against `ember + luna + sonnet` 138,551 (`CR:315`, `CR:320`).
- It does not claim the parsed-sparse pre-filter is right or wrong. That is a separate lever, reopened only through CI-1 after H-A.
- It does not use the stale line "sonnet alone gives most catches per token". That figure is pilot-only, one run per package, before `source.md` shipped (2026-11-11), and E2's own valid-era tables contradict it (E-16; gaps D-57).

<!-- Source: Variant A (Proposal A), Design and Round 2 "A-min" - merged per Change 5; new H2 section placed after Correctness argument per A-13 -->
## Decision D-1: skill-path default of two reviewers (owner decision before H-A)

**Status.** `[PROPOSED]`, owner-gated, risk High. Not adopted by this document. In the debate both advocates favoured this narrowed change (called "A-min" there) as the basis of a merge after Round 2; the Round 2.5 invariant probe then found three HIGH gaps in that consensus (INV-009, INV-012, INV-013), and this section turns their content into conditions. Recording a condition here does not satisfy it, and the invariants stay UNADDRESSED until the owner accepts the condition (see the last section).

### What D-1 changes and what it leaves alone

<!-- Source: Variant A (Proposal A), Design - narrowed per Change 5 -->
- **Changes.** Only the skill-path default, from 3 to 2: `SKILL.md:86`, `commands/reflect.md:100`, the "(default)" label in the section 7.1 table, the "restore N=3" sentence at `SKILL.md:658` and its twin at `refs/reviewer-spec.md:102`. The other coupled sites are in the table below.
- **Keeps as opt-ins.** `--reviewers 3` and `--strategy enterprise`.
- **Leaves alone.** The code-engine default (`commands.py:270-274`, `config.py:264`), the clamp (`config.py:335`), the exit gate (`scripts/reflect_shadow_exit.py:244-245`), the invariant probe, the debate, the calibrator and the evidence validator. The adversarial call stays at `--depth standard`.
- **Saving, stated honestly.** One reviewer call, one calibrator call and one debate variant on the roughly 26 of 38 recorded Tier 2 runs that ran three cards (9 already ran two cards and 3 have no card). Counted in calls, not tokens, and not a third of a run.

### Conditions

1. **Shadow pin as a conditional default.** The flag definition reads "default 2; 3 when the effective engine is shadow", evaluated at Wave 3A after the engine decision D2 (`SKILL.md:318`), plus the edit at `SKILL.md:340`. Without it every shadow run computes `panel_parity: false` and a run that sees requested 2 aborts at `manifest advance --stage resolved` (`manifest.py:314-315`, pinned by `tests/review/test_review_manifest.py:118-121`; INV-001). The pin is prose, which is weaker than code (A-007).
2. **Every coupled site edited, with one drift-pin test** over the default text (no test pins it today, E-8).
3. **The task-builder POST gate named and decided** (see below; INV-012).
4. **A rollback tripwire on observable proxies, written before shipping** (see Rollback; INV-009).
5. **Count and source recorded separately, with strata** (the telemetry rows under "Contract and audit fields"; INV-002, INV-010).
6. **The floor rule and one bounded re-dispatch** (see below).
7. **Served model recorded first.** D-1 should not ship ahead of the shadow path recording the served model: a class label can be served by one model (combo A3 collapsed every reviewer to sonnet), and with two reviewers a collapse removes all diversity (CA-6).
8. **Owner acceptance of the trade.** The owner accepts that D-1 is "a cost cut on thin evidence" for the advisory consumers, confirms the user-run commit gate is acceptable at two reviewers, and sets the trade-off threshold: neither side of the debate named how much per-run saving justifies how much unmeasured quality risk (A-002). That threshold is an owner parameter.

### Every place that states the count

<!-- Source: Round 2 rebuttal (advocate B), verification (a); probe INV-001, INV-004 - Change 6, A-5 -->
Paths: `SKILL.md` = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`; `refs/` = `src/superclaude/skills/sc-reflect-protocol/refs/`; `commands/reflect.md` = `src/superclaude/commands/reflect.md`; the task-builder skill = `src/superclaude/skills/task-builder/SKILL.md`. Action EDIT means the site changes under D-1; KEEP means it describes the engine default, which is unchanged at 3. The EDIT rows are 13 table rows covering 16 individual sites in five files (`SKILL.md` 8, `refs/input-resolution.md` 2, `refs/reviewer-spec.md` 3, `commands/reflect.md` 2, the task-builder skill 1); the three KEEP rows are the remaining sites, plus D2 as the evaluation point. (The refactoring plan said "about nine edits"; the table, counted by the orchestrator after the merge, says 16.)

| Site | What it says today | Action |
|---|---|---|
| `SKILL.md:86` | `--reviewers N` "2-3; default 3, clamped by `--depth`" (re-read) | EDIT: "default 2; 3 when the effective engine is shadow" |
| `SKILL.md:240`; `refs/input-resolution.md:92` | "3 aliases or more: T2 with 3 reviewers (full diversity)" | EDIT |
| `SKILL.md:318` (D2) | the engine flag is checked after depth, pin, budget and rubric (re-read) | Reference, not an edit: the conditional default is evaluated at Wave 3A, after D2 |
| `SKILL.md:340` | "Run shadow measurement runs with the default reviewer count"; `review panel resolve` has no count option (re-read) | EDIT: shadow runs use 3 |
| `SKILL.md:654-659` | section 7.1 rotation table, row `3 (default)`; the post-removal sentence at `:658` restores N=3 and covers only an executor of `sonnet` (re-read) | EDIT: move the "(default)" label; reword `:658` for haiku and opus executors and for N=2 |
| `SKILL.md:681` | "2-3 reviewer cards" | EDIT |
| `SKILL.md:695` | the adversarial call hard-codes `--compare` to `reviewer-1-card.yaml,reviewer-2-card.yaml,reviewer-3-card.yaml` (re-read) | EDIT: name only the cards that exist; a literal copy at N=2 names a missing file and `SKILL.md:1466` routes the run to `single-reviewer-fallback`, turning a healthy two-card run DEGRADED |
| `SKILL.md:987` | label `panel_shortfall_2_of_3` | EDIT (label) |
| `SKILL.md:1375` | eval fixture "All three reviewers are sonnet-class" | EDIT |
| `refs/input-resolution.md:18` | "Default 3, clamped by `--depth`" | EDIT |
| `refs/reviewer-spec.md:27` | example `reviewer-3.md` | EDIT |
| `refs/reviewer-spec.md:97`, `:102` | duplicate the rotation row at `SKILL.md:655` and the sentence at `:658` | EDIT |
| `commands/reflect.md:100`, `:221` | flag documented as 2-3; "3 heterogeneous reviewers fan out" | EDIT |
| task-builder skill `:2229` | waves-attestation example "ensemble=3 reviewers" (re-read) | EDIT (example) |
| `src/superclaude/cli/reflect/models.py:91-92` | documents the engine `--reviewers` default 3 as spec section 5.1 | KEEP. One flag name now has two documented defaults (INV-004). |
| `docs/guides/reflect-cli-tools-guide.md:140`; `docs/testing/v5.0.0/user/D12-reflect.md:63` | engine default 3, "2-4" | KEEP |
| `tests/cli/reflect/test_shadow_skill_contract.py:124,140` | hard-code 3 | KEEP (shadow runs at 3) |

### Task-builder default POST gate (blocking, skill path)

<!-- Source: invariant-probe INV-012 - Change 7, A-11 -->
The default `reflect_post_mode: skill` gate runs a dedicated subagent that invokes `Skill(skill: "sc-reflect-protocol", args: "--mode post --remediate --diff {BASE}..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --output {OUTPUT_DIR}")` (task-builder skill `:2225`, re-read for this merge) with no `--reviewers`. It treats an unresolved Regression or unauthorized Drift as a HALT (`:2227`), so it is a blocking completion gate (`:2217-2236`; orchestrator-verified, INV-012). D-1 would move it to two reviewers silently. The owner decides between:

- **(a) Recommended.** The runner passes `--reviewers 3` explicitly, so the blocking completion gate keeps three reviewers until a pilot arm exists. This keeps the rejection of an engine-default change consistent: both blocking paths stay at three.
- **(b)** Accept two reviewers for that gate and record the decision.

### Floor rule and one bounded re-dispatch (risk item)

<!-- Source: Variant A (Proposal A), R2 and Round 2 - Change 15, A-2 -->
With two reviewers one failed or invalid card leaves one, which is DEGRADED (`single-reviewer-fallback`, `src/superclaude/cli/reflect/contract.py:278-296`; code engine exit 11, `tests/cli/reflect/test_ensemble_stub_integration.py:251-277`). With three reviewers a 2-of-3 shortfall stays PASS-eligible (`tests/cli/reflect/test_verdict_mapping.py:572-580`). Evidence for the cost of no slack: E2 `ember + terra` scored -1.75 found (permutation p 0.029) because terra returned nothing (`CR:294`, `CR:298`). Mitigation, as a prose-only rule: one bounded re-dispatch of a reviewer that returned nothing before degrading (the existing bounded re-ask for an invalid block is at `SKILL.md:343`). It lowers the rate; it does not guard the floor, because shadow13 and shadow15 skipped a stated step even with correct text (R2 of Proposal A, `adversarial/variant-1-original.md`). Anchor the pair on the reliable-format class: sonnet had 0 of 15 findings blocks dropped at merge, luna 2 of 30 (`CR:427`). Tests: the N=2 mirror of `test_i5` and the EV-1 test (see Test coverage needed).

### Rollback

<!-- Source: Round 2 rebuttal (advocate A and advocate B QUALIFY); probe INV-009 - Change 8, A-3, A-8 -->
- **Revert.** A prose edit in the sites above restores three; `--reviewers 3` already works.
- **The tripwire cannot use the panel fields.** `reviewers_requested`, `reviewers_resolved`, `reviewers_complete` and `panel_shortfall_2_of_3` are Stage 2 panel fields (`SKILL.md:967-987`, `--t2-engine shadow`). The legacy path, where D-1 applies, writes no `panel/manifest.json` (14 manifests against 91 `pre-*` directories), and shadow is pinned at 3, so the Stage 2 aggregator never sees a two-reviewer legacy run (INV-009).
- **Observable proxies.** `merge_method: single-reviewer-fallback`; `len(reviewer_cards)` against the requested count; convergence; and probe-artifact presence, defined over both `adversarial/invariant-probe.md` and `adversarial/adversarial/invariant-probe.md` (a single-path check mis-counted it in this debate). Corrected counts: 20 of 23 three-card runs and 5 of 6 two-card runs have the artifact.
- **Numbers are an owner parameter.** Suggested start `[PROPOSED]`: revert on any two `single-reviewer-fallback` in the first 10 two-reviewer runs, or on a probe-artifact rate below the three-card rate by more than the owner's margin. Advocate A's trigger was a shortfall rate above 10 percent over the first 30 two-reviewer runs or a median convergence below 0.80. Advocate B's reading: the shortfall half is a tripwire, not a test (at a true rate of 10 percent the chance of at least 4 shortfalls in 30 runs is about 0.35, so it reliably catches only about 20 percent or more), and the convergence half is a poor trigger because of the ceiling effect.
- **Accrual.** About 39 runs over about five months, so 30 two-reviewer runs take about four months: the tripwire is effectively inoperative inside any decision window. A controlled pilot arm is the only measurement of recall. INV-009 stays UNADDRESSED until the owner accepts a proxy tripwire.

### Evidence for D-1

<!-- Source: Round 2 rebuttal (advocate A new evidence; advocate B verifications c, d, e) - Changes 5, 12, A-3, A-14; numbering continues from the Evidence section -->
Numbering continues from the Evidence section.

- **E-19. Two cards are already a production path.** 9 of the 38 recorded Tier 2 runs have exactly two reviewer cards on disk; 26 have three and 3 older runs have none. By cause: executor exclusion 2 (`detachTheCcsessi`, `phase3CodegraphA`); deliberate 1 (`implementGitHubI`: "Two were used so the calibrator (opus class) stays disjoint from the reviewers", `REPORT.md:30`); a missing card 1 (`closeIronbellyOr-20261104084538` has reviewer-1 and reviewer-3 cards, no reviewer-2 card and no report; the only possible failure, unattributable); no cause stated 5 (`enforceTheOwnerP`, `planTheRealBound-rerun`, `rollOutTheIssueW`, `phase1RemovalSpe`, `phase2CodegraphI`; `phase2CodegraphI` may belong to exclusion, which its files do not state, `[UNVERIFIED]`). Unscored for quality. [CODE-VERIFIED in data]
- **E-20. Two reviewers is a state the product defines and tests.** Rotation row `--reviewers 2` (sonnet, haiku; analyzer, qa) at `SKILL.md:654` and "The N=2 minimum is hard" at `:658`; executor exclusion already degrades the panel to two (`SKILL.md:648`, D3 at `:319`); the anchor replacement template `reflect-pre-x2` is a two-reviewer panel tested at `tests/review/test_review_reflect_templates.py:96-110`; EV-1 uses `required = max(2, resolved)` (`panel_lint.py:268`, tested at `tests/cli/reflect/test_panel_contract_lint.py:284-292`); Wave 0 step 0.5 already routes "2 distinct models, 2 reviewers" (`SKILL.md:232`). [CODE-VERIFIED, `SKILL.md:654` and `:658` re-read]
- **E-21. Calibrator disjointness.** Three-card runs are mostly `calibrator_diversity: degraded`: 23 of 26 on advocate A's Round 2 count, or 22 of 25 tagged on advocate B's recount (one run carries both tags). Two-card runs are mostly `full`: 6 of 8 tagged on both counts. Mechanism: with three anthropic classes as reviewers no class is left for the calibrator (`SKILL.md:1248-1253`). Limits: this is a guarantee argument, not a recall argument (no in-repo measurement ties disjointness to catch rate); with an opus executor at two reviewers the calibrator still collides with the executor (both exclusion runs have calibrator opus), so `full` overstates the executor, reviewer and calibrator partition (`SKILL.md:1257-1259`, a SHOULD; INV-003); and the two-card choice may be deliberate. A fourth reviewer class in the pool is an open alternative to cutting N (see the owner decisions). [CODE-VERIFIED in data]
- **E-22. The spec body reaches one persona.** Under UC-1 only the `qa` persona receives the spec body (`refs/reviewer-spec.md:55`; `R06` lines 77 and 95), so two of three reviewers are partially source-blind by construction. Two reviewers keep the one that sees it, but at two reviewers a failed `qa` card leaves a spec-blind survivor and a DEGRADED verdict (`contract.py:278-296`), where at three the same loss leaves two spec-blind cards that are still PASS-eligible. The post-removal procedure (`refs/reviewer-spec.md:104-110`) restores classes but does not re-map personas after exclusion and backfill: with executor haiku at N=2, `qa` lands on a backfilled opus or on nobody (INV-006).
- **E-23. Probe presence.** Counting both paths, the invariant-probe artifact exists for 20 of 23 three-card runs and 5 of 6 two-card runs; the one two-card run with no probe at either path is `closeIronbellyOr-20261104084538`, which is missing its reviewer-2 card. No probe-absence gap at two cards is claimed. INV-008 stands on its structural point only: nothing gates the probe on N, but the debate skip rule ("<10% diff", `sc-adversarial-protocol/SKILL.md:407-410`, `:947-951`) can drop Round 2.5, and two variants differ less by construction. No recorded run shows it happening at two cards. [CODE-VERIFIED in data]
- **E-24. Convergence in recorded runs (retrospective, unscored).** Two-card runs: 0.40, 0.947, 0.958, 0.968 and four at 1.0 (7 of 8 at or above 0.80); the 0.40 run is `--depth quick` (no rebuttal round, no probe), which confounds N with depth (`planTheRealBound-rerun`, `REPORT.md:21` and `:104`). Three-card runs: 1 of about 25 below 0.80 (0.76, `writeTheP0LivePl`). These show no sign of harm and a ceiling effect; they cannot show quality, because convergence measures agreement among variants and two variants agree at least as easily as three. [CODE-VERIFIED in data]
- **E-25. Zero shortfalls so far.** The Stage 2 exit report shows `2-of-3 shortfalls: 0` over 13 counted shadow runs (`R11` §8) and all 15 combo runs ended `published` with 3 of 3 reviewers complete (`FINDINGS.md:3`). Zero in 28 gives a 95 percent upper bound of about 10.7 percent on the shortfall rate (rule of three), and showing under 5 percent needs about 60 clean runs; a spare not yet needed is still a spare. [DOC-SOURCED]

### What cuts against D-1

<!-- Source: Variant A (Proposal A), Evidence C1 to C5 and R5 - Change A-6; carried in full, not softened -->
- **CA-1. Nothing measures two against three reviewers inside reflect.** E2 never ran reflect, a calibrator or a debate, so its ceiling "cannot be read as the T2 ceiling" (`R11` §12 item 3). H-A is "designed, not run" (MR:527; G-59 asks who owns the benchmark port). The synthesis rates Option A High risk for exactly this reason.
- **CA-2. The only E2 size effect that survived testing is a 2-to-3 gain.** "Second luna raises control found +0.83 (p 0.004 Welch, 0.048 permutation, baseline all zeros)" (`CR:298`; `CR:366`: "the only doubling effect that survives testing"). It compares `ember + luna` (control found 0.00, `CR:317`) with `ember + luna + luna` (0.83, `CR:331`): a single package and a repeated model. Reflect's strict distinctness forbids a repeated model (`R04` §8), so reflect cannot produce that exact effect, and `ember + sonnet` scored control 0.75 with two reviewers (`CR:315`), close to the three-reviewer values 0.80 to 0.83 (`CR:320`, `CR:331`). It is the most honest evidence for a third reviewer and it is not refuted.
- **CA-3. The two-reviewer panel that failed shows the cost of no slack.** `ember + terra` scored 0.50 of 14, -1.75 found (permutation p 0.029; `CR:298`, `CR:336`), "largely terra returning nothing" (`CR:294`). A panel of two with one empty reviewer is a panel of one. This is a reliability problem, not a size effect, but D-1 makes it more expensive.
- **CA-4. External guidance recommends three.** `W01` recommendation 9: "a panel of three heterogeneous reviewers plus one adjudicator is the evidence-supported size"; recommendation 4: a PASS should need at least two valid reviewers. Reflect already has the adjudicator (debate plus calibrator), so the comparison is two plus adjudicator against three plus adjudicator, which no source tests (E-18).
- **CA-5. If H-A fails, the whole Tier 2 spend is in question.** Cutting one reviewer is then a small saving on spending that should shrink in frequency or purpose (MR:527 names the rubric as the alternative lever). Proposal A's own claim that the pre-filter is the larger lever (C5 in `adversarial/variant-1-original.md`) is withdrawn by the recount (E-5); what remains is that rows 4 and 6 drive most recorded Tier 2 runs and no evidence says they are bad reasons to escalate.
- **CA-6. A class label may be served by one model.** Combo A3 collapsed every reviewer to sonnet, and the "haiku" slot was served by another model (`R04` §7.2). With two reviewers a collapse removes all diversity; a single collapsed slot leaves one distinct model (diversity `insufficient`, DEGRADED), while three can lose one slot and keep two. This is the core's dispatch gap (the dispatcher must pass `model` and record the served model), independent of count. See condition 7.

### What this does not show

<!-- Source: Round 2 rebuttal; probe INV-003, INV-006, INV-008, INV-011, INV-014; A-15 items A-001, A-002, A-008 -->
- It does not show that two reviewers match three on recall inside reflect (CA-1).
- **E2 cannot be read as the Tier 2 ceiling** (A-008): no reflect, no calibrator, no debate; "indistinguishable at this sample size" at n=4 to 6 is about power, not equivalence (`CR:381`).
- **Representativeness of the 39 runs** (A-001): the runs span 2026-06 to 2026-11 and many skill versions and are mostly workflow plans without labelled ids. That is fine for row attribution (decisions are plan-level) and not for future load: 35 of 39 were flagged and only 4 of 38 decisions were non-sparse (`PD` quota paragraph).
- **No trade-off threshold exists** (A-002): how much saving justifies how much unmeasured quality risk is an owner decision, not a finding.
- **The saving is calls, not tokens.** `cost-profile.yaml:47-52` still says "2-3 reviewers" and the budget thresholds do not move; per-reviewer cost is not recorded (`modelUsage` is keyed by gateway alias, `R08` line 398).
- **Calibrator disjointness is not recall** (E-21), and the convergence figures are not quality (E-24).
- **Prose pins test prose, not model behaviour** (A-007): the conditional shadow default and the re-dispatch rule are prose; shadow13 and shadow15 skipped a stated step.
- **Row 7 escalation plus the enterprise rotation has no N=2 row** (INV-011 falsifier d); enterprise callers keep three.
- **The 0.80 convergence floor is enforced only on the engine and tasklist CLI arm** (`sc-tasklist-protocol/SKILL.md:1171`), not on skill-mode gates (INV-014 residual).

### Parked for later (not part of D-1)

<!-- Source: Variant A (Proposal A), Design - parked per the plan's "Changes NOT being made" rows C-004, C-005, C-006, C-007 -->
- **Executor-keyed two-slot templates** (`reflect-pre-duo`, `-duo-xh` and the `post` pair) and the three-row executor table, for the Stage 3 panel engine. On the legacy skill path the rotation prose restores N after exclusion, which removes the bare-two-slot failure there (the `:658` wording must be extended). Proposal A's in-memory dry run, reproduced by both advocates: `t1b`+`t4` resolves sonnet, haiku for executor none or opus, and only sonnet for executor haiku (`t4` skipped); `t1b`+`t1a` resolves sonnet, opus for executor none or haiku, and only sonnet for executor opus (`t1a` skipped); executor sonnet exhausts `tier1b` in both.
- **The clamp** `max(2, min(4, n))` (G-67): on the post-gate path owned by C17; recorded, not changed.
- **The exit-gate edit** (`complete < resolved` and its label): only when a shadow arm runs at two.

<!-- Source: Base (original, modified) - base "Phase 1", Gate G1 and tests N3 and N4 demoted to a conditional item / Change 3, A-1, A-8, A-13 -->
## Conditional items

### CI-1: make the parsed-sparse flag advisory (the base draft's "Phase 1")

**Status.** Conditional. Not committed scope and not staged. It would be built only if the reopen trigger below fires.

**Why it is conditional.** The flag was decisive in 0 certain and at most 1 of 39 recorded runs (E-5), gate G1 (defined under "Reopen trigger" below) has no candidates on recorded data, and the base draft's own text said that with Phase 1 closed its delivery was "closer to Option C".

**What it would change.** Rows 1, 2 and 8 of the §5.3 table lose the `NOT coverage_degraded` conjunct, and the table-wide precedence paragraph names only `coverage_undefined` and `surface_unreached`. In their place: when `coverage_degraded` is set, a Tier 1 stop through row 1, 2 or 8 additionally requires `coverage_pct_union >= <coverage-floor>` (default 0.90), read instead of the parsed `coverage_pct`, which is null for a plan with no parsed ids. Explicit pins keep their precedence. Step 1B.2b still sets the flag but no longer forbids a Tier 1 stop; the loud-never-silent posture is kept by a header line on a sparse plan that stops at Tier 1 (labelling is sparse, the verdict rests on inferred requirements) beside the existing "STOP at T1 with WARN" treatment. Sites: `SKILL.md:284`, `:431-432`, `:443`, `:454`, `:741`; `refs/coverage-mapping.md:77-79`; `refs/report-template.md:24`; `refs/grader-extensions.md:353-359`; `CHANGELOG.md`. The prose describing `coverage_degraded` would drop "table-wide T1-stop pre-filter" (`SKILL.md:454`, `:741`); the contract names, values and `contract_version` stay as they are.

**Reopen trigger** `[PROPOSED]`, not debated: the Step A keys show at least three runs where `tier_without_flag` is 1. The base draft added "and the Tier 1 card was calibrated at or above 0.85"; that clause is redundant and is dropped. Gate G1's other half is kept: for every run with `sparse_flag_decisive: true` that has both a `t1-card.md` and a Tier 2 merged verdict, no run shows a Tier 2-only blocking finding that the Tier 1 card lacked. G1 is an owner decision taken on a table the recompute check prints. If G1 does not open, the change is built behind the H-A pilot instead: the pilot's sparse stratum (already required by MR:540) measures Tier 1 against Tier 2 on exactly the plans the change would flip, and the default changes only after that.

**Bound on behaviour.** The new rule differs from today's only for a run that meets all of these: the flag is set; no pin or hard override applies; `coverage_undefined` and `surface_unreached` are not set; no row from 3 to 7 matches; the remaining conjuncts of row 1, 2 or 8 hold; and `coverage_pct_union >= floor`. On the recorded history that is at most 1 of 39 runs (E-5). [follows from `SKILL.md:427-443`, CODE-VERIFIED]

**The case for it.** Today two plans with the same content get different tiers if one writes `R-001` in front of each requirement and the other does not. The flag was added because parsed-only coverage is vacuous when nothing is parsed (`coverage_pct` is null, `refs/coverage-mapping.md:68-69`; the rule that 0/0 must not pass is at `SKILL.md:282`). The same D13 change added the repair: inferred rows with verbatim quotes and citations, `coverage_pct_union`, and a union denominator for `S_dev_density` (E-7). CI-1 keeps that repair and drops only the blanket guard on top of it, and the denser the unmapped inferred content, the sooner row 5 (`S_dev_density > 0.20`) escalates the plan anyway. The E-6 run is not evidence for or against this change (E-6).

**Tests that would ship with it** (not part of the committed test list):

| # | Test | What it asserts |
|---|---|---|
| N3 | `tests/cli/reflect/test_rubric_skill_text.py` (new) | Text pins on `SKILL.md`, in the style of `test_shadow_skill_contract.py:146-165`: rows 1, 2 and 8 carry no `NOT coverage_degraded`; the union-floor sentence is present; the precedence paragraph still names `coverage_undefined` and `surface_unreached`; Step 1B.2b still sets the flag and no longer says "FORBID the Tier-1 stop"; `contract_version` stays 1.8.0. Limit: this pins prose, like the C7 brief pin (`R06` §2.1), not what the orchestrating model does. |
| N4 | Eval cases under `.dev/eval-workspaces/sc-reflect/cases/` (new; replaces the unbuilt `sparse-labeled-spec` contract at `refs/grader-extensions.md:357`) | Four cases through the eval harness: sparse plan, clean rows, union at or above the floor, expect `tier_reached: 1` and the WARN; sparse plan with row 4, expect Tier 2; sparse plan with union below the floor, expect Tier 2; sparse plan with `--tier 1`, unchanged. Plus the existing `coverage_undefined` route still ends at Tier 2. These are model-run, so they check behaviour only to the reliability of that harness. |

**Cost.** S: text edits in one skill, no Python in the reviewer path, then `make sync-dev` and `make verify-sync`.

<!-- Source: Base (original, modified) - weakest point rewritten as D-1's bet; risk table updated; D-1 risks RD-1 to RD-5 added / Changes 1, 3, 5, 7, 8, 9, 10, 15, A-1, A-6, A-12 -->
## Risks and mitigations

**Overall risk: Medium, with one High item (D-1).** Step A and the conditional item are low risk. D-1 is High because quality at two reviewers is unmeasured inside reflect.

### The weakest point, stated first

<!-- Source: Base (original, modified) - "weakest point" rewritten: D-1's bet replaces the pre-filter / A-6 -->
**D-1 is a bet, and nothing measures it.** Nothing in the repository or the research compares two and three reviewers inside reflect, and D-1 gives up the third reviewer on thin evidence: E2 is a different workflow (E-14, E-15), its one size effect that survived testing is a 2-to-3 gain (CA-2), and external guidance leans to three (CA-4). Three consequences, none softened:

1. **The saving is in calls, not tokens, and applies to about 26 of 38 recorded runs.** If the dropped reviewer is the cheap one the token saving can be near zero (`ember + sonnet` 142,967 against `ember + luna + sonnet` 138,551).
2. **The quality exposure is unobserved.** The tripwire cannot see the legacy path and takes about four months to accrue 30 runs (Rollback; INV-009, HIGH, UNADDRESSED), and the blocking task-builder gate is moved silently unless the owner chooses option (a) (INV-012, HIGH, UNADDRESSED).
3. **If D-1 is not accepted, what this proposal delivers is** a corrected attribution of Tier 2 cost, instrumentation that records it per run, a frozen cap with a written decision rule for the count, and a measurement plan. That is close to the status quo (Option C); the honest difference is the information, not a cost saving.

The gate G1 of the base draft is no longer the weakest point: the flag change is conditional (CI-1). The larger recorded drivers of Tier 2 are rows 4 and 6 (18 and 9 of 39), not the flag. This proposal measures them and does not edit them, because no evidence in the research says that treating tests and docs as separate domains, or a calibrated confidence under 0.85, is a bad reason to escalate. If the owner wants a cost cut from the rubric, the next step is a measured change to row 4 or 6 under the same kind of gate, and that is a different proposal.

### Other risks

<!-- Source: Base (original, modified) - R1 to R9 updated; RD-1 to RD-5 added from D-1 -->
| # | Risk | Evidence | Mitigation | Residual |
|---|---|---|---|---|
| R1 | (CI-1 only) A sparse plan stops at Tier 1 and a real blocker is missed | E-6 (n=1; the blocker was found by the probe, not a reviewer, and the run escalates through row 6 regardless). The loss class there (acceptance criteria that pass on empty `git diff` output) is one no rubric input can predict. | CI-1 is not built unless its trigger fires; gate G1; Tier 1 stop only through rows 1, 2 or 8 with the union floor; header WARN; consumers advisory; `--tier 2` and `--depth deep` still force Tier 2; text revert restores the old rule. | If CI-1 is built, a missed advisory finding on at most 1 of 39 recorded runs. |
| R2 | (CI-1 only) Pass 2 under-extracts and the union coverage looks complete | E-7: T2's qa reviewer reads the full spec body for exactly this case (`refs/reviewer-spec.md:55`, via `R06` §2.3). T1 has no second reader. | Union floor; every inferred row must carry a quote and citation or it is dropped. If the keys or the pilot show under-extraction misses, add a deterministic probe (count of MUST/SHALL lines in the source against rows emitted). Not built now. | Unmeasured. |
| R3 | The keys are model-written and can be wrong | `fired_rule_number` and inputs are recorded by the orchestrating model across skill versions (E-5); the E-6 run recorded row 8 against its own calibrated `C` of 0.68 (INV-013, HIGH, UNADDRESSED). | The recompute check reports "disagree" and "not evaluable" and never guesses; the prospective keys are computed the same way in every future run. | The check reports disagreement; it does not repair it. One of the three runs that had no recorded row stays undetermined (E-5). |
| R4 | D-1 and the pilot interact: a shipped default changes what the H-A "T2 with 3" arm means | A-004; INV-010 | Arms pinned explicitly (`--reviewers 2`, `--reviewers 3`); strata recorded (`reviewers_source`, `executor_exclusion_degraded`, `anchor_replaced`, `depth`, `calibrator_diversity`); shadow runs stay at 3; MR:540 already requires the sparse stratum to be reported apart, and `escalation_path` gives it a recorded value. | Slightly larger pilot report. |
| R5 | D-1 breaks Stage 2 shadow parity or aborts shadow runs | Condition 1; `reflect_shadow_exit.py:139-142`, `:173-174`; `manifest.py:314-315` (INV-001). Shadow runs otherwise reach Tier 2 through `--tier 2` pins and are not gated by the rubric (E-10). | Conditional default plus the `SKILL.md:340` edit plus the drift-pin test and a text pin that the conditional is present. | The pin is prose. |
| R6 | The cap of 3 is applied unevenly | E-3: the post wrapper still clamps to 4; the generic default has 4 (E-4); under D-1 the skill default (2) and the engine default (3) differ, and `models.py:91-92` documents 3 (INV-004). | Recorded, not changed: C17 owns the post path and the clamp, and C03 blocks the document default. "Cap 3" means the reflect profile and `N_eff`. | Two or three paths disagree until C17. |
| R7 | The owner reads the instrumentation as permission to rewrite rows 4 or 6 | See the weakest point. | The design lists rows 3 to 7 as unchanged and the recompute script as read-only. | Scope creep is an owner decision. |
| R8 | H-A is expensive and never gets run, so the count is never decided | `PD` C-5: 1.30M to 2.62M claude tokens for the pilot, grading unpriced; no owner (G-59). | The incumbent default stays (two if D-1 was accepted, three if not), the symmetric rule is on file so a later run needs no new design, and an inconclusive result leaves the incumbent in place. | If no pilot is funded, D-1 is "a cost cut on thin evidence" and the alternative keeps paying for three reviewers. |
| R9 | Doc drift: several documents attribute the Tier 2 count to the pre-filter | MR:142, MR:556, the `PD` quota paragraph, `R11` §12 item 4. | Step A posts the E-5 table and each such statement gets a pointer to it. | Documentation work only. |
| RD-1 | No slack at two reviewers: one failed or invalid card leaves one and the run is DEGRADED | D-1 "Floor rule"; CA-3; E-25 | One bounded re-dispatch (prose); anchor on sonnet; N=2 mirror of `test_i5` and the EV-1 test. | Prose lapses cost a degrade (shadow13 and shadow15). |
| RD-2 | The blocking task-builder gate silently drops to two reviewers | INV-012 (HIGH, UNADDRESSED); `task-builder/SKILL.md:2217-2236` | Option (a): the runner passes `--reviewers 3`. Rollback if (a) is skipped: pass it later. | Open until the owner chooses. |
| RD-3 | A missed site reproduces INV-004, or a hard-coded list turns a healthy two-card run DEGRADED | INV-004; `SKILL.md:695`, `:1466` | The site table with actions and the drift-pin test; the `--compare` rule pin. | 16 EDIT sites in five files; a missed site is possible. |
| RD-4 | The tripwire cannot observe the legacy path | INV-009 (HIGH, UNADDRESSED) | Proxies and an owner-set margin; a controlled pilot arm is the only measurement. | The tripwire is inoperative inside a four-month window. |
| RD-5 | A class label served by one model removes all diversity at two reviewers | CA-6; INV-003 | Condition 7: record the served model first; a fourth reviewer class is an open alternative. | Open. |

<!-- Source: Base (original, modified) - test section: replay tests N1 and N2 replaced, N3 and N4 moved to CI-1, D-1 tests and a "measurement only" table added / Changes 3, 4, 13, A-4, A-15 -->
## Test coverage needed

### Existing tests that change

None. E-8: no test under `tests/` reads the §5.3 table, the pre-filter text, `tier_decision.yaml` or the default reviewer text; the only `coverage_degraded` hits are a field-name list in `panel_lint.py:46` and one `coverage_degraded: null` fixture line. The D13 eval fixtures named at `refs/grader-extensions.md:353-359` are an authoring contract; no `sparse-labeled-spec` case exists. The honest reading is that today nothing pins the behaviour discussed here, which also means nothing would catch an accidental change. Under D-1, `tests/cli/reflect/test_shadow_skill_contract.py:124,140` hard-code 3 and stay valid because shadow runs stay at 3. A, the other draft, would have changed four existing tests (clamp, exit gate, template names, default confirmation); those edits are parked (D-1, "Parked for later").

### Existing tests that must stay green (guards)

<!-- Source: Base (original, modified) - guard table with the manifest guard added from INV-001 -->
| Test | Why it guards |
|---|---|
| `tests/review/test_review_panel_reflect_profile.py` (17 tests; cap at `:145-147`, `:170`, `:199`) | The cap of 3 and the generic range stay. |
| `tests/review/test_review_reflect_templates.py` (21) | The six `reflect-*` templates stay at three slots or fewer. |
| `tests/cli/reflect/test_panel_contract_lint.py` (38; minimum two cards at `:284-292`) | `STABLE_FIELDS_1_8_0` (`panel_lint.py:33-63`) still lists `coverage_degraded`, `coverage_pct_union` and `escalation_rule_matched`; no contract field is added or removed. |
| `tests/cli/reflect/test_shadow_exit_script.py` (20), `test_shadow_skill_contract.py` (11), `test_verdict_replay_script.py` (13) | Stage 2 counting and brief-template pins are untouched. |
| `tests/review/test_review_manifest.py:118-121` | Pins that resolved cannot exceed requested; the reason for the shadow pin. |

Counts are from `research/12-test-pins-regression.md` §1 and §2.

### New tests, automated

<!-- Source: Round 2 rebuttal (advocates A and B) and Variant A test section - Change 13, A-4 -->
| # | Test | Step | What it asserts |
|---|---|---|---|
| N1 | `tests/cli/reflect/test_tier_recompute_script.py` (new, `[PROPOSED]` name), fixtures | A | A fixture with a recorded row 8 and a calibrated card `C` of 0.68 reports "disagree"; a fixture missing an input reports "not evaluable" and is never counted as decisive; a fixture with a pin gives `pin` or `hard_override` and a `null` for `sparse_flag_decisive`; shadow run directories are skipped by default. Modelled on `test_shadow_exit_script.py`. Replaces the base draft's N1. |
| N2 | Same file, one test against the real history | A | Skipped when `.dev/reflect` is absent. With it present, asserts only the derivable counts (39 files, 38 Tier 2, 35 flagged, 34 flagged and Tier 2) and that the `fixTheScIssueWor` run is classified not decisive. Replaces the base draft's N2, whose hard-coded counts were wrong. |
| N7 | N=2 mirror of `test_i5` | B (D-1) | N=2 with one failing transport is `single-reviewer-fallback`, DEGRADED, exit 11; N=2 with both succeeding is PASS-eligible. |
| N8 | EV-1 test | B (D-1) | A two-resolved run with one card on disk fails EV-1 (`panel_lint.py:268`). |
| N9 | Drift pin over the default text | B (D-1) | The default reviewer count reads the same in every EDIT site of the site table, so the places that state it cannot drift apart again. |
| N10 | Post-hoc lint on run artifacts | B (D-1) | The resolved reviewer count equals the requested count unless `executor_exclusion_degraded` is set. |
| N11 | Skill-text pin | B (D-1) | The conditional shadow default ("default 2; 3 when the effective engine is shadow") and the `--compare` rule (name only the cards that exist) are present in `SKILL.md`. |

N3 and N4 are defined under Conditional items (CI-1) and ship only with it. The pins N9 and N11 test prose, not what the orchestrating model does (A-007).

### Measurement only (no pytest can detect these)

<!-- Source: Variant A (Proposal A), test section; Round 2 - Change 13, A-15 -->
| # | Item | Step | What it needs |
|---|---|---|---|
| N5 | H-A pilot strata | C | The pilot report splits results by `escalation_path` (MR:540) and states Tier 1 against Tier 2 recall on the "sparse flag decisive" stratum separately, and uses the arms and strata of the count rule. |
| N6 | E2-harness miss-rate check | C | Only after the portability fixes `R11` §3 and §12 list (hard-coded `/tmp` and worktree paths, a silently dropped audit filter, the fallback overwrite of `expected_model`); a reflect consumer must also be added. Whether the three E2 packages are sparse is not verified here. |
| M1 | Recall at two against three reviewers inside reflect | C | The pilot arms only. |
| M2 | Convergence behaviour with two variants | C | Retrospective figures (E-24) show agreement, not quality. The 0.80 floor itself is a number check and is unit-testable, but the statistic's behaviour is measurement only. The floor is enforced only on the engine and tasklist CLI arm (`sc-tasklist-protocol/SKILL.md:1171`), not on skill-mode gates (INV-014 residual). |
| M3 | DEGRADED rate at two reviewers | B, C | Telemetry on the proxies in Rollback. |
| M4 | Whether the orchestrator picks the right rotation row and restores N after exclusion | B, C | Prose behaviour; a pilot or telemetry only. |
| M5 | Token saving | C | Per-reviewer cost is not recorded today (E-17). |

Run commands: `uv run pytest tests/cli/reflect/test_tier_recompute_script.py -v` `[PROPOSED]`, then `uv run pytest tests/review tests/cli/reflect -q` for the guards. `SKILL.md` edits go in `src/superclaude/skills/sc-reflect-protocol/`, then `make sync-dev` and `make verify-sync`; `.claude/` copies are never staged.

<!-- Source: Base (original, modified) - cost table rewritten for Step A, D-1, CI-1 and the pilot; savings paragraphs replaced / Changes 1, 3, 4, 5, 10, A-1 -->
## Cost

| Item | Size | Basis |
|---|---|---|
| Step A: audit keys in `SKILL.md` §5.4, `scripts/reflect_tier_recompute.py`, tests N1 and N2, pointer annotations on the documents that repeat the old attribution (R9) | S | One script of the size and shape of `scripts/reflect_shadow_exit.py` (collect, then report); no model calls. |
| D-1, if accepted: 16 EDIT sites in five files (13 rows of the site table), tests N7 to N11, the task-builder gate edit under option (a), then `make sync-dev` and `make verify-sync` | S to M | Proposal A's own estimate; the synthesis lists S and the enumerated work is larger. Under the repository rules the hard limit is five edits per direct change, so this goes through a written plan and `/sc:implement`, not a direct edit. |
| CI-1, only if reopened | S | Text edits in one skill, tests N3 and N4 (see Conditional items). The synthesis labels Option B "Effort: M" (`synth-04:921`). |
| Step C: H-A pilot | 1.30M to 2.62M claude tokens (3.61M to 7.24M under the other reading of the repeats); confirmatory 2.41M to 4.88M; grading, seeding and orchestration unpriced | `PD` C-5, C-5b, C-6, SD-8 [DOC-SOURCED]. Not specific to this proposal: any option that decides the count needs it. Adding the two-versus-three arm to a pilot that has to run anyway costs one extra arm; running it alone costs the whole pilot. |
| Step C: one added two-reviewer arm (Tier 2 pinned at 2) | about 210k to 420k claude tokens for 6 plans | Own arithmetic by analogy with `PD` row C-3 (6 plans at 35k to 70k each). An estimate; the arm is not designed yet. |
| Grader cost reference | about 115k output tokens per scoring in E2's pilot (9 judge subagents, 1,034,575 output tokens in all) | `PR:52` via `R11` §5, doc-sourced and not checked against raw `judge.json`. Reference only. |

**What D-1 saves, honestly.** One reviewer call, one calibrator call and one debate variant per Tier 2 run, on the roughly 26 of 38 recorded runs that ran three cards (the other 12 already ran two cards or none). Tokens cannot be stated per reviewer from existing data (`R08` line 398). The scale to keep in view is that a whole three-reviewer combo run spent 185,086 to 367,381 output tokens (estimates the combo documents mark "do not compare", `R11` §12 table, `FINDINGS.md:37`), and that `ember + sonnet` (two reviewers) cost 142,967 tokens against 138,551 for `ember + luna + sonnet` (`CR:315`, `CR:320`). The saving is bounded by the share of a run the reviewer phase takes, which no record measures.

**What the rubric lever saves, honestly.** The flag was decisive in 0 certain and at most 1 of 39 recorded Tier 2 runs (E-5), so removing it would avoid at most one Tier 2 run of 39, roughly 90,000 to 367,381 output tokens (the same estimates). While CI-1 is closed the saving is zero.

**What not deciding D-1 costs.** One reviewer, one calibrator and one debate variant keep being paid on about 26 of 38 recorded runs. It is recoverable at any time by a prose edit in the site table, and `reflect-lite` under `--strict-distinct` already resolves to two reviewers on the panel path.

**Running cost after Step A.** Extra keys per `tier_decision.yaml` and one read-only script run on demand.

**Where this sits against the three options at `synth-04:901-941`.** Against Option A (two reviewers now): the merge takes only the skill-path default, as an owner-gated decision with conditions, and parks the engine default, the clamp, the exit gate and the duo templates. Against Option B as drafted: the merge drops the committed rubric change and the retrospective replay, replaces the count premise and the 10-point margin, and adds the blocking task-builder gate. Against Option C (status quo): if D-1 is not accepted and CI-1 never reopens, the behaviour is C's, at S effort, and the difference is the information: the corrected attribution, the recorded keys, a pre-registered count rule and the named blocking gate.

<!-- Source: Round 2 rebuttal (advocates A and B); debate-transcript Scoring Matrix and Convergence Assessment; invariant-probe; base-selection - Change 14, A-13, A-15 -->
## Open decisions and unresolved conflicts

Nothing in this section is resolved by this document. Where an earlier section records a mitigation or a reading, that is a proposal for the owner, not a resolution; an item marked UNRESOLVED or UNADDRESSED here stays so until the owner acts.

### Convergence status

- **Debate points.** 24 of 30 points were resolved (the two advocates' final positions agreed on the superior approach). Tally: Proposal A won 4 (S-003, C-012, C-014, A-003), Proposal B won 6 (S-004, C-002, C-007, X-001, X-002, X-003), MERGE 14, UNRESOLVED 6.
- **Convergence.** Raw diff-point convergence 0.80, at the 80 percent threshold. The taxonomy coverage gate passed (L1, L2, L3). The invariant-probe gate is **BLOCKED**: three HIGH-severity invariants are UNADDRESSED (INV-009, INV-012, INV-013). Status: **BLOCKED_BY_INVARIANTS**. The debate depth was `standard`, so there was no Round 3; the invariants are carried forward, not argued out.
- **Selection record.** Base B won by a margin of 0.0061 (A 0.9194, B 0.9256), inside the 5 percent band; tiebreaker level 1 (debate points won, B 6 to A 4) decided it. B stays ahead in every sensitivity case in `adversarial/base-selection.md`, but by under 5 percent in the ruled case, so the outcome rests on the tiebreaker. The advocates' Round 2 consensus favoured a narrowed A ("A-min") as the base of a merge; the protocol selects by score, so the base is B and A-min is carried as Decision D-1.
- **Sycophancy note.** Both advocates retracted their own headline figure and ended on nearly the same merge after one rebuttal round. The probe was told to attack the consensus and found three HIGH gaps the advocates had missed, so the convergence is not treated as proof of correctness.

### 1. Unresolved debate points (both advocates' final positions)

"Variant 1" is Proposal A (two reviewers by default); "Variant 2" is Proposal B (the base). Confidence is the advocate's own, in percent.

| Point | Topic | Advocate A final | Advocate B final | How this document handles it (not a resolution) |
|---|---|---|---|---|
| S-002 | Organisation of the Evidence section: by stance (A) or by subject (B) | MERGE, 55 | Variant 1, 60 (isolating the counter-evidence makes it easy to audit) | The Evidence H2 keeps B's subject grouping; D-1 uses A's stance grouping ("Evidence for D-1", "What cuts against D-1"). |
| S-006 | Test section posture | Variant 1, 60 (names concrete test edits) | MERGE, 60 (A's concrete edits plus B's "nothing pins this") | The Test section keeps B's guard framing and adds A's N=2 tests and a "measurement only" table. |
| C-003 | Evidence for the quality effect of the change (how to read E2) | MERGE, 55 | Variant 2, 60 ("power, not equivalence") | Both agree E2 cannot be read as the Tier 2 ceiling. E-14 and E-15 carry B's reading, CA-1 and CA-2 carry A's; no weighing is claimed. |
| C-010 | Reversibility and rollback | MERGE, 75 | Variant 2, 65 | Both agree A's "cannot be rolled back by data alone" was overstated. D-1 "Rollback" states the revert and the tripwire's limits. |
| C-013 | Pre-existing test coverage of the thing being changed | Variant 1, 70 (A's surface is test-pinned) | MERGE, 55 | Neither variant pins behaviour and D-1 needs a drift pin (N9); the guard table and E-8 record both facts. |
| C-016 | Reading of the external evidence | MERGE, 85 | Variant 2, 60 (the sources do not choose between 2 and 3) | Both disclaim that the external sources choose between 2 and 3 (E-18, CA-4); they differ on how far A reads past them. |

### 2. UNADDRESSED invariants (ten)

All ten are UNADDRESSED in the debate sense: the debate did not argue them out. This document records the content of a mitigation for each, in the change named, and **recording a mitigation in this document is not a resolution**. Each row stays UNADDRESSED until the condition in its last column is met by the owner. Four more findings were ADDRESSED (INV-003 partly, INV-005, INV-007, INV-014 partly; all LOW); their residuals are carried in D-1 "What this does not show".

| ID | Severity | Status | What was assumed and is not established | Where this document records a mitigation | Stays UNADDRESSED until |
|---|---|---|---|---|---|
| INV-009 | HIGH | UNADDRESSED | A shortfall-rate tripwire over the first 30 two-reviewer runs is observable. It is not: the legacy path writes no panel manifest, shadow is pinned at 3, and 30 runs take about four months. | Change 8: D-1 "Rollback" (proxies), RD-4 | The owner accepts a tripwire restated on the proxies and sets its numbers. |
| INV-012 | HIGH | UNADDRESSED | Skill-path consumers are advisory or user-run. The task-builder default POST gate is a blocking skill-path consumer that D-1 would move to two reviewers silently. | Change 7: D-1 "Task-builder default POST gate", E-9, RD-2 | The owner picks option (a) or (b). |
| INV-013 | HIGH | UNADDRESSED | Prospective audit keys give clean H-A strata for rows 4 and 6. They are model-written, and the E-6 run recorded row 8 against its own calibrated `C` of 0.68. | Change 4: Step A recompute check ("CLI surface"), R3, tests N1 and N2 | The recompute check exists and runs. |
| INV-001 | MEDIUM | UNADDRESSED | A conditional default keeps shadow parity and the 13-of-20 count. A shadow run that sees requested 2 aborts at `manifest.py:314-315`; the conditional is prose. | Change 6: D-1 condition 1, site table, R5 | The owner accepts condition 1 and the pin is in the text. |
| INV-002 | MEDIUM | UNADDRESSED | `reviewers_default_applied` records the source of a count. As a boolean it breaks under enterprise, a clamp and the shadow default. | Change 9: the three telemetry fields and strata ("Contract and audit fields"), R4 | The fields exist in the contract. |
| INV-004 | MEDIUM | UNADDRESSED | The edit list covers every place that states or hard-codes the count (missed: `SKILL.md:695`, `refs/input-resolution.md:18`, and others). | Change 6: D-1 site table, test N9, RD-3 | All EDIT rows are applied and the drift pin passes. |
| INV-006 | MEDIUM | UNADDRESSED | Two reviewers keep the one reviewer that gets the spec body. A failed `qa` card leaves a spec-blind survivor and DEGRADED; personas are not re-mapped after exclusion. | Change 12: E-22 | The owner accepts the single point of failure or the persona rule is changed. |
| INV-008 | MEDIUM | UNADDRESSED | The probe is untouched so cutting width is safe. The debate skip rule ("<10% diff") can drop Round 2.5 and two variants differ less by construction. No recorded run shows it (the first reported gap was a counting artifact and is withdrawn). | Changes 8 and 12: E-23 and the probe-presence proxy in Rollback | The owner accepts the proxy or the skip rule is gated on N. |
| INV-010 | MEDIUM | UNADDRESSED | Symmetric pilot arms give clean strata. Arm membership is ambiguous without `executor_exclusion_degraded`, `anchor_replaced` and `depth`. | Change 9: strata fields, count-rule arms, R4 | The strata are recorded in the pilot's runs. |
| INV-011 | MEDIUM | UNADDRESSED | D-1 alone achieves a cost saving without a quality or safety regression. The saving is calls only; enterprise callers keep three; row 7 plus enterprise has no N=2 row. | Changes 5 and 6: D-1 "What this does not show", conditions 1 to 8 | The owner accepts the trade (condition 8). |

### 3. Owner decisions

| # | Decision | Notes |
|---|---|---|
| 1 | Accept D-1 before H-A, or not. | Includes the acceptance that D-1 is a cost cut on thin evidence for the advisory consumers, that the user-run commit gate may run at two reviewers, and the trade-off threshold (A-002). The debate's consensus favoured D-1 only with conditions 1 to 8 met. |
| 2 | The tripwire numbers. | Suggested start `[PROPOSED]`: revert on any two `single-reviewer-fallback` in the first 10 two-reviewer runs, or on a probe-artifact rate below the three-card rate by more than the owner's margin. Advocate A's alternative: a shortfall rate above 10 percent over 30 runs or a median convergence below 0.80. |
| 3 | The task-builder POST gate: option (a) or (b). | Option (a), the runner passes `--reviewers 3`, is recommended (A-11). |
| 4 | Who owns the H-A pilot (G-59) and funds it. | 1.30M to 2.62M claude tokens, grading unpriced; the count is not decided without it. |
| 5 | Who closes G-67 (C17). | The clamp `max(2, min(4, n))` (`config.py:335`) against the cap of 3; left unchanged here. |
| 6 | Whether the four-reviewer document-loop default and `live7` follow (C03). | Out of scope for C14; blocked on C03 because the model E2 chose is not nameable in the packaged tier file. |
| 7 | The margin of the symmetric count rule, its minimum sample size and its cost measure. | Owner parameters; the base draft's 10-point margin is not carried. |
| 8 | Whether to add a fourth reviewer class to the pool instead of cutting N. | Raised by advocate B in Round 2 (E-21, CA-6): the executor, reviewer and calibrator partition needs a class that is not in the pool today. |

### Considered and not carried

<!-- Source: refactor-plan "Changes NOT Being Made"; kept visible so a reader sees what was rejected and why -->
| Item | Why it is not in this proposal |
|---|---|
| A: change the code-engine default from 3 to 2 (`commands.py:270-274`, `config.py:264`) | The post gate runs `superclaude reflect run ... --depth deep` with no `--reviewers` (`sc-tasklist-protocol/SKILL.md:1162`) and would drop to two on evidence from a non-blocking, no-calibrator, no-debate setting. Both advocates conceded the engine default remains 3 until a pilot arm exists (MERGE 77 percent). |
| A: close G-67 by changing the clamp in this change | The clamp is on the post-gate path owned by C17; an open item, not changed (MERGE 55 percent). |
| A: edit `reflect_shadow_exit.py:244-245` and its "2-of-3" label now | Shadow stays pinned at 3, so the rule keeps its meaning (Variant 2, 72 percent). |
| A: four duo template files and executor-keyed shadow template selection now | Parked for Stage 3 (MERGE 60 percent); see D-1 "Parked for later". |
| A: the flag-set count read as the number of runs the flag caused to escalate, and the upper bound on runs Option B would stop at Tier 1 | False on the files; retracted by advocate A (Variant 2, 93 and 95 percent). E-5 states the figure. |
| A: Option B "cannot be rolled back by data alone" | Overstated: a skill-text revert and the `--tier 2` kill switch undo it (Variant 2, 80 percent). |
| B: the rubric change (flag advisory) as committed scope | Decisive in at most 1 of 39 runs; no G1 candidates. Kept as CI-1. |
| B: the retrospective replay script and tests N1 and N2 as drafted | The recount is done and N2's hard-coded counts were wrong. Replaced by prospective keys and the recompute check. |
| B: the 10-point count margin | The advocate's own invention. Replaced by an owner parameter. |
| B: E-6 read as a flag-only counterexample | Refuted by the run's own calibration card (`C` 0.68). Recast in E-6. |
| A: the saving stated for 38 of 39 runs | The saving applies to roughly 26 of 38 runs and is counted in calls, not tokens. |
