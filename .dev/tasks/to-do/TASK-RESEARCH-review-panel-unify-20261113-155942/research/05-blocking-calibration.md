# Research: Blocking policy per lens and calibration as a panel role

**Investigation type:** Code Tracer
**Scope:** `src/superclaude/cli/reflect/contract.py`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (§10.1-10.7, §11.3, rubric reference near :631); `src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md`; `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md`; `src/superclaude/agents/confidence-calibrator.md`; `~/.claude/agents/finding-grader.md`; `src/superclaude/cli/review/card_convert.py`; `src/superclaude/cli/review/findings_v2.py`; `src/superclaude/cli/review/cluster.py`; `src/superclaude/commands/spec-panel.md`; `.dev/reflect/pre-*-shadow*/panel/cards/`; E2 `COMBO-REPORT.md` at commit 4a22d742
**Status:** Complete
**Date:** 2026-11-13

---

## 0. Context taken from the scope slices (read first)

- Hand-off D4 [E2/E3]: "One reviewer's `blocking` flag decides the row and the verdict (no quorum, no calibration)"; open decision 5 asks whether verdicts use one reviewer's flag or a quorum/calibrated rule (`research/scope/00-handoff-copy.md:108`, `:202`). The hand-off cites `ledger.py:187,213-218,274` for this; this file does not re-read `ledger.py` (another agent's scope), but scope slice 01 confirms from audit-D at 4a22d742 that "row blocking == any member blocking, verdict FAIL iff a blocking row, 0 violations over 264 merges" (`research/scope/01-other-branch-study.md:128`).
- Scope slice 03 [E1] already flags: MEDIUM -> non-blocking in `card_convert.py`, two-word deviation labels unmatched, rubric dimension-3 vocabulary mismatch, calibrator written for troubleshoot (6 dims) vs reflect's 5 dims, and that `panel.py` selects no calibrator (`research/scope/03-reflect-side.md:147-157`, `:167-170`, `:221-222`). Each is re-checked against source below.
- Scope slice 05 [E3] lists three ways blockingness is decided on master and in experiments: by label (rf-qa, v2 reflect rule), by consequence sentence (spec-panel prose, finding-grader), by computed route (pr-submit) (`research/scope/05-master-loop-and-consumers.md:155`).

Key Takeaways
- The central conflict is already named by all three scope slices: a single-reviewer veto [E2/E3] vs debate plus card-level calibrator [E1] vs a blind binary grader [E3 experiment].
- Every slice claim used below is re-verified at source or carried as [UNVERIFIED].

---

## 1. `src/superclaude/cli/reflect/contract.py` — how reflect turns a contract into a verdict [E1]

What it is: a pure module (`contract.py:1-13`) mapping a parsed `return-contract.yaml` to one of four verdicts, first-match-wins: BLOCKED -> DEGRADED -> HALTED -> PASS (`contract.py:138-260`). Imports only `.models` + stdlib + PyYAML (`contract.py:15-22`).

### 1.1 Load-bearing booleans (`contract.py:47-57`)
Seven fields: `regression_present`, `unauthorized_deviation_present`, `needs_human_decision`, `user_decision_required`, `adversarial_unavailable`, `input_drift_detected`, `verification_ran`. A present, non-None, non-bool value routes BLOCKED `malformed-contract-boolean` (`contract.py:213-222`). Truthy strings like `"true"` are rejected rather than silently passed.

### 1.2 `derive_verdict` (`contract.py:138-260`)
1. BLOCKED: rc 124 -> `timeout` (:161-164); any non-zero rc -> `child-crash` (:169-172); missing contract (:173-177); missing/blank `contract_version` (:179-186); major != "1" (:187-194); `degraded_components` not a list (:197-206); malformed load-bearing bool (:213-222).
2. DEGRADED via `_degraded_reason` (:225-239).
3. HALTED via `_halted_reason` (:242-246).
4. PASS only when `status == "success"` and `tier_reached == expected_tier` (:249-252); otherwise HALTED `tier-mismatch` (:255-260).

### 1.3 `_degraded_reason` (`contract.py:263-358`) — the "audit is untrustworthy" gate
Order: chain-critical `degraded_components` in {auggie, env-aliases, evidence-validator} (:31-33, :274-275); expected T2 but T1 ran (:278-279); `t2_model_class_diversity != "full"` (:282-284); `t2_vendor_diversity == "single"` unless `allow_single_vendor` (:287-288); `adversarial_unavailable is True` (:291-292); `merge_method == "single-reviewer-fallback"` (:295-296); T2 with null `adversarial_convergence_score` (:299-300); `adversarial_subrun_status` in partial/failed (:306-307); T2 convergence < 0.80, NaN/Inf or unparseable (:317-326); `verification_ran is False` without an exempt skip reason (exemptions narrowed under `promoting`) (:329-345); `citations_dropped > 0` (:348-352); `input_drift_detected is True` (:355-356).

Blocking-policy relevance: reflect **treats a single-reviewer outcome as degraded**, not as a verdict. `merge_method: single-reviewer-fallback` -> DEGRADED (:295-296) and a convergence score below 0.80 -> DEGRADED (:317-326). That is the opposite of the master review ledger, where one reviewer's flag decides the row [E2/E3, via hand-off D4].

### 1.4 `_halted_reason` (`contract.py:361-382`) — the "audit found a blocking problem" gate
First match: `status == failed` -> `status-failed`; `status == partial` -> `status-partial`; `regression_present is True` -> `regression`; `unauthorized_deviation_present is True` -> `unauthorized-deviation`; `needs_human_decision is True`; `user_decision_required is True`; then a **count fallback**: `deviation_count_by_class.regression > 0` -> `regression`; `deviation_count_by_class.drift > 0` -> `drift` (:377-381).

Detail [E1]: the count fallback means **any Drift count halts**, even when `unauthorized_deviation_present` is false. `authorized` and `necessary` counts never halt (read by `_extract_deviations` :90-101 but not tested in `_halted_reason`). So the code-level "blocking" set for reflect is {Regression, Drift} plus the four human/flag booleans; {Authorized expansion, Necessary deviation} are non-blocking.

### 1.5 `classify_fix` (`contract.py:385-420`)
HUMAN-REQUIRED on `regression_present`, `needs_human_decision`, `user_decision_required`, `unauthorized_deviation_present` (each `is True`) or `regression > 0` (:410-417). AUTO-FIXABLE when only `drift > 0` or `necessary > 0` (:418-419). So within the halted set there is a second split: Drift not flagged unauthorized is auto-fixable; `unauthorized_deviation_present` is human-required. The docstring ties `needs_human_decision` to a non-empty `grounding-gaps.yaml` citing SKILL.md:754 (:400-408) — checked in §2.

Key Takeaways
- [E1] Reflect's verdict code has no per-finding `blocking` flag; it halts on contract-level booleans and on `deviation_count_by_class` (regression or drift > 0).
- [E1] Reflect degrades (does not trust) a single-reviewer merge and any T2 convergence < 0.80; a unified panel that lets one reviewer's flag decide the verdict would contradict `contract.py:295-296` and `:317-326`.
- [E1] Necessary and Authorized never change the verdict; Drift always halts via the count fallback (`contract.py:380-381`), whether or not `unauthorized_deviation_present` is set.

---

## 2. `sc-reflect-protocol/SKILL.md` §10, §11.3, §5, §7 and §9.1 — the protocol-side blocking and calibration rules [E1]

All line numbers are `src/superclaude/skills/sc-reflect-protocol/SKILL.md`, read 2026-11-13 by ranges (1042-1266, 405-449, 624-659, 745-869).

### 2.1 The 4-class taxonomy and what each class does (§10.1-10.5, :1042-1135)
| Class | Definition (short) | Default remediation / gate effect | Cite |
|---|---|---|---|
| Authorized expansion | scope addition explicitly approved by an authoritative artifact | "None. Document in the report. No tier-3 task." | :1050-1062 |
| Necessary deviation | forced by a technical constraint, documented inline, not pre-authorized, contradicts no acceptance criterion | "Documentation note"; no tier-3 task unless `--remediate-docs` | :1064-1078 |
| Drift | silent change, not mapped, no rationale, contradicts no criterion | "Authorize-or-revert decision required"; Tier 3 offer if `--remediate` | :1080-1092 |
| Regression | contradicts an acceptance criterion, explicit constraint, previously passing test or documented invariant | only class that unconditionally triggers a Tier 3 offer and unconditionally forces Tier 2 (§5.3 rule 3) | :1094-1131 |

Precedence: Regression > Drift > Necessary > Authorized (:1133-1135). Per-file aggregation over 100 hunks uses the same precedence as a union (:1048).

Regression is set **by evidence, not by assignment** (:1117): only exit codes mapped to Regression set `regression_present`; pytest exit 2/3, timeouts, flaky results and unmapped exits are Grounding Gaps (:1105-1115). Reuse-Miss, runtime-surface UNREACHED and contracted-sink findings are modifiers mapped onto the 4 classes by evidence, never a 5th class (:1167-1200). Reuse-Miss has an explicit **"Blocking bar (high)"**: it maps to a blocking class (Drift/Regression) only at rung L3 with `S_reuse ≥ 0.82 AND confidence ≥ 0.85 AND verdict ≠ distinct` (:1176). This is the only place in the reflect protocol that states a confidence threshold for blockingness at finding level [CODE-VERIFIED absent from code: no `0.82`/`S_reuse` threshold exists in `contract.py`; it is protocol prose executed by the orchestrating model].

The phrase "blocking class (Drift/Regression)" at :1176 and "Blocking counts flow only through the existing Drift/Regression counters" at :1188 and :1200 is the protocol's own definition of which classes block. This matches `contract.py:377-381` (regression or drift count > 0 halts) [CODE-VERIFIED].

### 2.2 Grounding Gaps and Correctness gaps (§10.6, :1137-1161)
Non-empty `grounding-gaps.yaml` forces `status: partial` and `needs_human_decision: true` (:1155-1158). In code, `status == partial` halts (`contract.py:367-368`) and `needs_human_decision` halts (`contract.py:373-374`) and is HUMAN-REQUIRED (`contract.py:410-417`) [CODE-VERIFIED for the consumer side; the producer side — that the orchestrator really sets them — is protocol prose, [UNVERIFIED] in code]. So a Grounding Gap is **verdict-changing (halts) but is not a deviation**. Correctness gaps are advisory and never gate (`refs/deviation-taxonomy.md:156-180`).

### 2.3 Load-bearing contract flags (§9.1, :851-858)
`regression_present: bool` "now verified-sourced from the §6.1 step 5.5 exit-code taxonomy" (:853); `unauthorized_deviation_present: bool` (:854) **with no definition anywhere in the skill directory** (grep for `unauthorized` across `src/superclaude/skills/sc-reflect-protocol/` returns only :854). `needs_human_decision` "grounding-gaps.yaml non-empty" (:858); `user_decision_required` "convergence < threshold AND no auto-route applies" (:857). `per_task_verdicts[].deviation_class: authorized | necessary | drift | regression | none` (:860-867).
- Finding [E1]: what sets `unauthorized_deviation_present` is undocumented. The consumer (`contract.py:371-372`, `:414`) treats it as halt + human-required; the producer rule is missing. The scope slice 03 reading "reflect treats unjustified Drift as `unauthorized_deviation_present`" (`research/scope/03-reflect-side.md:149`) is an inference; neither SKILL.md nor `deviation-taxonomy.md` states it. Tag: **[UNVERIFIED]** (no producer rule in docs or code).

### 2.4 Calibration rubric inputs and decision logic (§5.2-5.3, :412-441)
`C` = calibrated confidence, arithmetic mean of 5 dimensions per `refs/reflection-rubric.md` (:416-417). §5.3 first-match decision: `C ≥ 0.90` + narrow scope -> STOP at T1 (:431); `C ≥ 0.85` -> STOP with WARN (:432); UC-2 Regression candidate -> ESCALATE "regression must be debated by ≥2 reviewers" (:433); `C < 0.85` -> ESCALATE (:437).
- So in reflect, calibrated confidence is a **tier-routing** input (whether to run the panel), **not** a blocking decider on individual findings. The blocking decision (deviation class) is made by the reviewers + debate; `C` decides whether more reviewers are needed.

### 2.5 Calibrator role (§7 :631, §11.3 :1240-1262)
- §7 delegation row: `confidence-calibrator`, Waves 1D and 3C, "Blind re-grade per the 5-dim reflection rubric; the dominant anti-anchoring mechanism (calibrator-model ≠ reviewer-model class — see §11.3 disjoint-set rule)"; fallback "Inline orchestrator calibration with `calibration: inline-fallback` marker" (:631).
- §11.3: the card is the calibrator's only input (:1242); calibrator class ∈ `{opus, sonnet, haiku, qwen, kimi, deepseek} \ reviewer_model_classes`; empty set -> highest capability "NOT used by the most reviewers" and `calibrator_diversity: degraded` (:1244-1254). Three-way partition executor/reviewers/calibrator SHOULD be pairwise disjoint (:1258). "For Tier 2, every reviewer card is calibrated by an independent calibrator instance in parallel (Wave 3C) ... sc-adversarial-protocol's debate is weighted by calibrated confidence, not self-reported" (:1260).
- Whether `sc-adversarial-protocol` actually reads a calibrated confidence field when scoring is a doc-sourced claim; not traced into the adversarial skill here: **[UNVERIFIED]**.
- §11.0 makes the anti-confirmation guarantee conditional on calibrator class ≠ reviewer class (:1208-1214).

### 2.6 Reviewer composition (§7.1, :644-658)
Rotation sonnet, haiku, (qwen|kimi|deepseek if alias available; else opus) (:655). With the default 3-reviewer Anthropic rotation {sonnet, haiku, opus}, the §11.3 disjoint set is {qwen, kimi, deepseek}. `contract.py:282-284` degrades on `t2_model_class_diversity != full`, but **does not read `calibrator_diversity`** (no hit for `calibrator` in `contract.py`) [CODE-VERIFIED by reading `contract.py:1-420`]. So a degraded calibrator never changes the reflect verdict; it is telemetry only.

Key Takeaways
- [E1] The protocol defines blocking classes as Drift and Regression (SKILL.md:1176, :1188, :1200); the code halts on exactly those counts (`contract.py:377-381`). Authorized and Necessary never block. Grounding Gaps halt through `status: partial` / `needs_human_decision`, not as deviations.
- [E1] `unauthorized_deviation_present` is a load-bearing halt flag with **no producer rule** in the skill or taxonomy (SKILL.md:854 only).
- [E1] Calibrated `C` routes tiers (SKILL.md:431-437); it is not a per-finding blocking gate. `calibrator_diversity: degraded` has no verdict effect in code.
- [E1] Only one finding-level confidence threshold exists in the protocol: Reuse-Miss blocking needs `confidence ≥ 0.85` and `S_reuse ≥ 0.82` (SKILL.md:1176) — a precedent for "calibrator-weighted blocking".

---

## 3. `refs/reflection-rubric.md` and `refs/deviation-taxonomy.md` [E1]

### 3.1 Rubric (177 lines)
- `C` = mean of 5 dimensions, each 0.00-1.00 (`reflection-rubric.md:9-13`): Citation grounding (:15-24), Coverage completeness (:26-35), Deviation-classification clarity (:37-46), Risk surface coverage (:48-57), Recommendation actionability (:59-68). FR-RH1 reachability folds into the five, "NOT a sixth dimension" (:70-78).
- **Dimension 3 vocabulary mismatch** [CODE-VERIFIED as a text fact]: "classified unambiguously as one of `{Aligned, Refinement, Drift, Regression}`" (`reflection-rubric.md:39`) versus the taxonomy's `{Authorized expansion, Necessary deviation, Drift, Regression}` (`SKILL.md:1050-1094`; `deviation-taxonomy.md:26-90`) and the code keys `authorized, necessary, drift, regression` (`contract.py:40`; `findings_v2.py:38` deviation_class, §7 below). "Aligned" and "Refinement" appear nowhere else in the contract or code read. **[STALE DOC]**: rubric dimension 3 uses an older vocabulary.
- Threshold guidance: `C ≥ 0.90` strict T1, `C ≥ 0.85` floor "inherited from sc-troubleshoot", `C < 0.85` escalate (:80).
- Calibrator selection pseudocode identical to SKILL.md §11.3 (:135-145); worked Example C: Anthropic-only reviewers {opus, sonnet, haiku} -> disjoint set empty -> `opus`, `calibrator_diversity: degraded` (:157). Open Question: no capability ordering across the six classes is published (:175-177).
- What the rubric does NOT have: any per-finding score, any blocking dimension, or any output field `per_finding`. It scores the **whole card** (:11 "The calibrator emits both the per-dimension scores and the mean `C` into `reflection-card.yaml`").

### 3.2 Taxonomy ref (180 lines)
Mirrors SKILL.md §10 (Authorized :26-38, Necessary :40-54, Drift :56-70, Regression :72-84, precedence :86-98, exit-code mapping :100-114, FR-RH1 mapping :116-127, Grounding gaps :129-154, Correctness gap advisory :156-180). It adds a row SKILL.md §10.4 lacks: "(C7, step 5.6a)" static behavioural-unreachability of a spec-declared REQUIRED capability is a Regression "annotation-free and static ... NO real-boot are required to block" (`deviation-taxonomy.md:123`), while SKILL.md §10.4/§10.10 says static signals "can NEVER set `regression_present`" (SKILL.md:1196) — though §9.1 :796 already mentions "Step 5.6a static behavioral-unreachability". The SKILL.md §10.10 sentence and the taxonomy row conflict on whether a static signal can block. Not in my assigned code path; flagged in Gaps.
- `deviation-taxonomy.md:84`: "Regression is the only class that unconditionally triggers a Tier 3 remediation offer ... No other deviation class carries an unconditional escalation". No statement defines `unauthorized_deviation_present`.

Key Takeaways
- [E1] The rubric is card-level and has no blocking dimension; using it as a per-finding blocking decider would need a new rubric.
- [E1] **[STALE DOC]** rubric dim 3 `{Aligned, Refinement, Drift, Regression}` (`reflection-rubric.md:39`) does not match the 4-class taxonomy used by the skill, the agent, `findings_v2.py` and `contract.py:40`.
- [E1] SKILL.md §10.10 (static never sets `regression_present`, :1196) conflicts with `deviation-taxonomy.md:123` (static step 5.6a is a Regression).

---

## 4. `src/superclaude/agents/confidence-calibrator.md` — the calibrator as written [E1, shared with troubleshoot]

- Frontmatter: "re-grades a hypothesis card against a **6-dimension** rubric ... Used by sc:troubleshoot-protocol in Wave 1 ... and Wave 3" (`confidence-calibrator.md:3`); tools `Read`, model `sonnet`, `permissionMode: plan` (:5-8).
- Inputs: `card_path`, **`rubric_path`: "absolute path to `refs/escalation-rubric.md`"** (:47-48), `card_tier`, `flags_context` with `--depth/--no-escalate/--type` (:49-50), plus troubleshoot-only optional inputs (`assertions_path`, `behaviour_definitions_path`, `tasklist_path` = `diagnosability-tasklist.md`, `locus_path`) (:53-57).
- Responsibilities hard-code the 6 troubleshoot dimensions: "Note the 6 dimensions: Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence" (:61); formula `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` (:67); verdict-direction caps 0.70/0.84 (:68); C1-C8 structural assertions (:69); output = per-dimension table with those six names (:84-91), STOP/ESCALATE recommendation with troubleshoot reasons (:113-117).
- Output: **one calibrated number per card** (:102, :109). No per-finding output, no blocking output.
- Failure: crash/timeout/malformed -> inline fallback, `calibration: inline-fallback` (:156-157). Placebo warning: if calibrated matches inline within ±0.05 "the agent is not earning its overhead" (:159).

### 4.1 How reflect overrides `rubric_path` (question 3)
- Reflect says the calibrator re-grades "per the 5-dim reflection rubric" (SKILL.md:631) and that `C` is the mean of 5 dimensions (SKILL.md:416-417; `reflection-rubric.md:11`).
- **No reflect text passes `rubric_path`**: grep for `rubric_path`/`card_path` in `src/superclaude/skills/sc-reflect-protocol/` returns no hit; the only rubric references are the prose pointers at SKILL.md:416, :425, :1262, :1835. The shadow step 5 adds one brief line asking for per-finding numbers (SKILL.md:344) but still does not name a rubric path.
- So the agent file instructs 6 named troubleshoot dimensions and a gated-min formula, while reflect expects a plain mean of 5 different dimensions. Which one runs depends on what the orchestrator writes in the Task prompt. Tag for the reflect claim "calibrator re-grades per the 5-dim reflection rubric": **[CODE-CONTRADICTED]** — the agent definition (`confidence-calibrator.md:48`, `:61`, `:67`) implements a 6-dimension gated-min rubric; no override mechanism exists in either file.
- E1 evidence that the mismatch is real in practice: addendum-1 records "`confidence-calibrator` returns one score per card, so per-finding numbers exist only when the brief asks for them" (`.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/addendum-1.md:11`), and that changing the agent file was explicitly left out of scope (:26). Which rubric recorded calibrations actually used was not sampled here ([UNVERIFIED]).

### 4.2 Dimension mapping (6 troubleshoot vs 5 reflect)
| Troubleshoot (`confidence-calibrator.md:61`) | Reflect (`reflection-rubric.md:15-68`) | Fit |
|---|---|---|
| Evidence grounding | Citation grounding | same idea |
| Runtime check | — | no reflect analogue (reflect UC-1 is about a plan) |
| Symptom coverage | Coverage completeness | close |
| Reproducibility fit | — | none |
| Fix directness | Recommendation actionability | close |
| Domain coherence | — | none |
| — | Deviation-classification clarity | none in troubleshoot |
| — | Risk surface coverage | none in troubleshoot |
(Mapping is my reading of the dimension names, not stated in either file.)

Key Takeaways
- [E1] The calibrator is a **troubleshoot** agent (6 dims, gated-min, STOP/ESCALATE) reused by reflect without a written rubric override; reflect's "5-dim" claim is [CODE-CONTRADICTED] by the agent file.
- [E1] The agent returns one card-level number; per-finding numbers exist only because the shadow brief line asks for them (SKILL.md:344).
- [E1] A panel-core calibrator would need its own rubric (finding-level) and a stated `rubric_path` contract; neither 6-dim nor 5-dim rubric scores blockingness.

---

## 5. Recorded calibration in E1 (legacy 0/689; shadow 142/142) [E1]

### 5.1 Legacy runs: 0 of 689 (question 5)
`stage0a-report.md` (zero-dispatch replay of recorded `pre-*` card dirs, Stage 0) defines "calibrated" as a numeric 0-1 confidence per finding id (`.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/stage0a-report.md:368`) and records: embedded 34 cards / 271 findings / 0 numeric / 18 non-numeric / 253 no entry; sidecar 61 / 347 / 0 / 75 / 272; none 20 / 71 / 0 / 0 / 71; "Uncalibrated findings: 689 of 689" (:370-376). Addendum-1 adds: older `per_finding` entries are words ("confirmed", "grounded"); numeric per-finding confidences exist in 1 of 74 `pre-*` runs, keyed `F1...` while the cards say `R1-F1...`, "an id mismatch that no file format fixes" (`addendum-1.md:9-10`). Layouts were mixed across 37 runs / 102 cards (21 sidecar-only, 10 embedded, 2 variant, 4 none) (`addendum-1.md:3`).
- Consequence adopted: `review cluster` now reports `calibrated_findings: n/m` and writes `calibration_coverage` (`addendum-1.md:18`); a multi-layout reader was rejected because it "would recover 0 of 689" (:16). (Doc claims; the code side is checked in §9.)

### 5.2 Shadow runs: recorded `calibration_coverage` (Glob `.dev/reflect/pre-*-shadow*/panel/cards/`, read 2026-11-13)
14 shadow dirs have `panel/cards/`; values from each run's `panel/clusters.json` key `calibration_coverage` (and the contract/telemetry copy):
| Run (suffix) | calibrated / clustered | contract or telemetry value |
|---|---|---|
| shadow01 | no `clusters.json` | `calibration_coverage: null` (`return-contract.yaml:78`) |
| shadow02 | 11/11 | (no contract value found) |
| shadow03 | 10/10 | "10/10" |
| shadow04 | 9/9 | "9/9" |
| shadow05 | 10/10 | "10/10" |
| shadow06 | 10/10 | "10/10" |
| shadow07 | 8/8 | "8/8" |
| shadow08 | 9/9 | "9/9" |
| shadow09 | 17/17 | "17/17" |
| shadow10 | 10/10 | "10/10" |
| shadow11 | 20/20 | "20/20" |
| shadow12 | 0/0 | "0/0" (no findings) |
| shadow13 | 5/5 | "5/5" |
| shadow14 | 13/13 | "13/13" |
| shadow15 | 10/10 | "10/10" (`telemetry.yaml`) |
Total: **142/142** clustered findings calibrated over 13 runs with a `clusters.json`.

Layout drift persists: 4 runs (shadow10, 12, 14, 15) write the `calibration:` block **unfenced** in the card, while SKILL.md:344 asks for "a fenced `yaml` block". `review cluster` still counted them (142/142), so the reader tolerates both.

### 5.3 Does the per-finding number separate blocking from non-blocking? (read-only tally, 2026-11-13)
I parsed every `panel/cards/reviewer-*.md` (findings-v2 lines + `calibration.per_finding`) with a throw-away read-only script run through `uv run python -I` (script kept outside the repo in `/tmp` and deleted afterwards):
- 142 findings in 13 runs; severity MINOR 100, MAJOR 42; `blocking: true` 16.
- blocking (n=16): all scored; mean 0.801, median 0.82, min 0.60, max 0.92; 3 below 0.70, 0 below 0.60.
- non-blocking (n=126): all scored; mean 0.661, median 0.70, min 0.25, max 0.92; 62 below 0.70, 35 below 0.60.
- 26 MAJOR findings are `blocking: false` (42 MAJOR - 16 blocking): the reflect-pre cards do not set `reflect_category`, so the label rule `blocking == (severity != MINOR)` in `findings_v2.py:161-162` did not apply (see §7).
Reading: a blind calibrator's per-finding number is higher on reviewer-blocking findings, but there is no ground truth for these runs, so this does not show which blockers are right. Model-behaviour evidence dated: the shadow runs ran **2026-11-12 22:22 UTC to 2026-11-13 02:42 UTC**, per the file modification times of `panel/cards/reviewer-*.md` in each `.dev/reflect/pre-*-shadow*/` directory (`stat -c %y`, read 2026-11-13): earliest shadow02 2026-11-12 22:22:58, then shadow03 23:26-23:27, shadow04-07 2026-11-13 00:12-00:15, shadow08-11 01:30-01:34, shadow13/15 02:18, shadow14 02:23-02:25, latest shadow12 02:42:28 (shadow01 has no cards). The dates in the run directory names (2026-10-23 to 2026-11-11) are the dates of the source task packages being reviewed, not run dates. Calibrator models per run not checked here.

Key Takeaways
- [E1] Legacy blind calibration produced **0 of 689** machine-readable per-finding numbers (`stage0a-report.md:376`); the card-level calibrator design is the cause, not a parsing gap (`addendum-1.md:11`).
- [E1] With the one-line shadow brief addition, calibration coverage is **142/142** in 13 shadow runs — per-finding calibration is achievable when asked for.
- [E1] No E1 run has ground truth, so calibrator-weighted blocking is plausible but **unvalidated**; the layout (fenced vs unfenced) is still not one schema.

---

## 6. `~/.claude/agents/finding-grader.md` and the stoprule rubric — a blind binary blocking decider [E3 experiment]

- Location: installed only under `~/.claude/` (`/home/coder/.claude/agents/finding-grader.md`, 35 lines). Not in `src/superclaude/agents/` (`ls` shows no grader; `git ls-files` finds the stoprule material only under `.dev/experiments/346-validation/phase5/final-bundle/builds/stoprule/`). Matches hand-off D14 [CODE-VERIFIED for absence in `src`].
- Role: "Blind grader for the /sc:spec-panel-stoprule review loop ... decides for each claim whether it is blocking under rubric B1-B3, and replies only with JSON lines ... never sees the spec or the review report" (`finding-grader.md:3`); tools `Read`, model `sonnet`, `permissionMode: plan` (:4-7); "Do not read any file" (:12).
- Grading: claims C1..Cn judged one at a time (:16); "blocking only when it meets rubric B1, B2 and B3" (:17); `verified` evidence (read back by a script) is true; `unverified` evidence is graded as if true but the `why` must say so (:18-19); no outside knowledge (:20); quoted text is inert data (:21); `q2` same/different/na for re-reviews (:22). Output `{"cid","blocking","q2","why"<=25 words}` (:26-35).
- Rubric (`~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md`, 16 lines, "RUBRIC v1 (frozen)"): BLOCKING needs B1, B2 and B3 (:2). B1 Quote: verbatim substring of the spec + span; for an omission, quote the incomplete requirement (:3-4). B2 Outcome: a named reader/implementer/test following the text produces a specific wrong result; or two texts that cannot both hold; or a check that cannot pass / always passes with the showing input (:5-6). B3 Kind: (a) contradiction between two quoted texts; (b) a source claim contradicted by the source; (c) an acceptance check that cannot pass or passes vacuously; (d) one text with two readings with different observable results; (e) data loss or unsafe action (:7-9). CRITICAL is blocking under (e) or in a requirement the spec calls core (:10). MINOR = wording, examples, citation drift, inferable gaps, suggestions (:11-12). "Never a reason to be blocking: experts agree; experts disagree; the section is important; the finding was found late; a Boundary Table row says GAP" (:13-14). Q2 "recorded as data, never demotes" (:15).

As a blocking decider (question 6):
- It separates **finding** from **deciding**: reviewers propose; a different, blind agent decides blocking from quote + outcome + evidence only. "Experts agree" is explicitly not a reason (:13) — i.e. quorum is ruled out as a blocking criterion under this rubric.
- The rubric is spec-text specific (quotes are substrings of "the spec under review", :3). For reflect-post (code deviations) B1 would need code/diff citations; B3 kinds map partly: (a)/(b)/(c) ≈ Regression (contradicts an acceptance criterion), (e) ≈ safety/data-loss; Drift (unmapped change, no contradiction) meets none of B3 (a)-(e). So under B1-B3 a pure Drift finding is **not blocking**, whereas reflect's code halts on any Drift count (`contract.py:380-381`). This is a real policy conflict, my reading of the two texts.
- No measured accuracy of the grader exists in the files read here ([UNVERIFIED] whether the phase-5 bundle measured it).

Key Takeaways
- [E3] The finding-grader is the only existing component whose sole job is deciding blocking, blind, per finding, against a frozen rubric; it lives only in `~/.claude/` and the phase-5 experiment bundle, not in `src`.
- [E3] Rubric B1-B3 rejects agreement as a reason to block (`rubric.md:13`), so "quorum" and "blind grader" are different philosophies, not variants.
- [E1 vs E3] Under B1-B3, reflect's Drift would not block; reflect's contract halts on Drift. A per-lens rubric is needed.

---

## 7. `src/superclaude/cli/review/findings_v2.py` — what the parser enforces about blocking [E1, extends E3's findings-v1]

Enforced (code, read 2026-11-13):
- `blocking` must be a real bool (`findings_v2.py:105-106`); **a MINOR finding cannot be blocking** (:107-108) — inherited semantics from findings-v1.
- `calibrated_confidence` in a finding line is rejected (:96-97); `self_confidence` 0-1 is allowed (:178-182). Calibration is kept out of the reviewer's line by design; it lives in a card sidecar (`calibration.per_finding`).
- `lens` in spec / reflect-pre / reflect-post (:36, :140-145). `deviation_class` in authorized / necessary / drift / regression / none (:38, :150-153), **required only when lens is reflect-post** (:147-149).
- **Label rule** (`findings_v2.py:161-162`): only when `reflect_category` is set, `blocking` must equal `severity != MINOR` ("a MAJOR or CRITICAL finding must be blocking and a MINOR one must not"). `reflect_category: deviation` requires `deviation_class` (:163-164).
- `channel` in defect / grounding-gap / advisory (:37, :184-186); `channel_of` defaults to defect (:190-193).

Not enforced (absence verified by reading `check_finding` :84-187 in full):
- **No rule ties `deviation_class` to `blocking`.** A `regression` can be `blocking: false`; an `authorized` or `necessary` can be `blocking: true`.
- **No rule ties `channel` to `blocking`.** `channel: advisory` or `grounding-gap` may carry `blocking: true`, although reflect's taxonomy says Correctness gaps never gate (`deviation-taxonomy.md:162`) and Grounding Gaps are not deviations (SKILL.md:1139).
- **No lens-specific rule** beyond the reflect-post `deviation_class` requirement.
- Without `reflect_category`, MAJOR may be non-blocking. Observed: 26 of 42 MAJOR findings in the 13 shadow runs are `blocking: false` (§5.3 tally).

Key Takeaways
- [E1] findings-v2 has the fields a per-lens blocking rule needs (`lens`, `deviation_class`, `channel`, `severity`) but enforces only two blocking constraints: MINOR never blocks (:107-108) and, with `reflect_category`, blocking == (severity != MINOR) (:161-162).
- [E1] The label rule applies only when an optional field is present, so it does not govern reflect-pre cards today (they carry no `reflect_category`; §5.3).

---

## 8. `src/superclaude/cli/review/card_convert.py` — mapping recorded reflect cards into findings-v2 [E1]

Purpose: deterministic converter of recorded reflect reviewer cards (4 shapes) to findings-v2 lines, used for the Stage 0 replay (`card_convert.py:1-47`).

Severity mapping (`card_convert.py:36-37`, `:71-83`, `:193-198`):
- `blocking, blocker, major, high, must-fix, p1` -> MAJOR + blocking; `critical, p0` -> CRITICAL + blocking.
- `minor, medium, low, should-fix, important, nit, info, p2, p3` -> MINOR + not blocking.
- any other word -> severity unset (the line then fails `check_finding`).

Deviation class mapping (`card_convert.py:42`, `:70`, `:103-104`, `:203`): `dclass = next((w for w in class_words if w in DEVIATION_CLASSES), None)` where each word is `_word(value)` = the whole string stripped and lower-cased. In the markdown shape the single `category`/`class` column feeds both reflect_category and deviation_class (:407-414).

### 8.1 The MEDIUM-drift case [CODE-VERIFIED]
`reflect-reviewer.md:71` defines "**HIGH** = regression or a load-bearing-invariant break; **MEDIUM** = unjustified drift with real impact; **LOW** = cosmetic / minor drift"; its example row is `| 1 | Drift | ... | MEDIUM |` (`reflect-reviewer.md:86`). The converter maps `medium` to MINOR non-blocking (`card_convert.py:81-83`, `:195-196`). Net effect: a Drift card row becomes `{severity: MINOR, blocking: false, deviation_class: drift}`. But reflect's contract halts on any drift count (`contract.py:380-381`). So **converted cards understate blocking for exactly the class reflect treats as verdict-changing**. Also `important` -> MINOR, whereas rf-qa treats IMPORTANT as blocking (scope 05 :146; not re-read here, [UNVERIFIED]).

### 8.2 The two-word label gap [CODE-VERIFIED]
The agent tells reviewers to use "**Authorized expansion**" and "**Necessary deviation**" (`reflect-reviewer.md:23-24`, summary :93). `_word("Authorized expansion")` = `"authorized expansion"`, which is not in `DEVIATION_CLASSES` (`findings_v2.py:38`), so the row gets **no `deviation_class`**. `Drift` and `Regression` match. Effect: the two non-blocking classes lose their class and become indistinguishable from unclassified rows; in clustering, a null class is "compatible" with any class (`cluster.py:157-158`), so these rows can cluster with Drift/Regression rows.

Key Takeaways
- [E1] `card_convert` encodes a severity-word policy (MEDIUM -> non-blocking) that contradicts reflect's verdict policy (Drift halts). A unified panel must derive blocking from `deviation_class` for reflect lenses, not from a severity word.
- [E1] Two-word class labels are dropped (`card_convert.py:203` + `:103-104`); fix by normalising "authorized expansion" -> authorized and "necessary deviation" -> necessary.

---

## 9. `src/superclaude/cli/review/cluster.py` — calibration handling, `support`, `uncalibrated`, `blocking_any` [E1]

Pure function `cluster_v2(reviewer_records, snapshot_file_list)` (`cluster.py:381-433`); record = (reviewer_id, ordinal, findings_v2 block, calibration_map) (:3-4, :184-248).
- Confidence accepted only if finite 0-1 and not bool (:79-83); a non-numeric entry is a problem and the finding stays uncalibrated (:278-287).
- Reviewer weight `w(r)` = highest calibrated confidence among that reviewer's clustered findings; 0 for a complete reviewer with none (:35-38, :389-396).
- `support(c)` = sum over distinct reviewers in c of their best member confidence / sum of all weights (:39-41, :337); `None` and listed `uncalibrated` if any member lacks a confidence or any complete reviewer with findings has no calibration (:42-44, :336, :398).
- **`blocking_any` / `blocking_all` over all members; "A cluster is blocking when blocking_any is true"** (:46-47, :375-376). So cluster-level blocking is still a **single-member veto**; calibration does not change it.
- `disputed` = support < 0.5, or members disagree on blocking, or two different non-null deviation classes (:48-49, :347-351). Disputed is reported but routes nothing.
- `cluster_agreement` = mean support over non-chained, calibrated blocking clusters; 1.0 with no blocking cluster; None with < 2 complete reviewers (:50-52, :403-412). SKILL.md shadow step 6 says it is "never compared with the convergence thresholds, never routes anything" (SKILL.md:345) [CODE-VERIFIED: `cluster.py` has no threshold or verdict output].
- Deviation classes must be compatible to merge (equal, or one null/none) (:30, :157-158, :165-166).
- `calibration_coverage` is computed in `cluster_cmd.py:177-179` (`calibrated_findings = clustered - len(uncalibrated_findings)`) and printed as `n/m` (:190) [CODE-VERIFIED], matching addendum-1's adopted change.

What this gives a blocking policy: every ingredient of a **calibrator-weighted quorum** already exists (per-finding confidence, per-reviewer weight, `support` in [0,1], a `disputed` flag), but the code still marks blocking by `blocking_any`. A rule such as "a cluster blocks when `blocking_any` and `support ≥ θ`" or "when `blocking_all` or support ≥ θ" would be a few lines on top of `_cluster`, but it is not implemented and θ has no evidence.

Key Takeaways
- [E1] `cluster.py:46-47`, `:375` keeps the single-reviewer veto at cluster level; calibration only feeds telemetry (`support`, `disputed`, `cluster_agreement`).
- [E1] `support` is a ready-made, normalised, calibrator-weighted agreement number per cluster — the natural hook for a quorum/calibrated blocking rule.

---

## 10. The two blocking rules on master and which one governs (question 2) [E3, plus E1's #519 code now on master]

Both files are on master: `git merge-base --is-ancestor d2d8a2d16 origin/master` succeeds (#519 merged) and `origin/master:src/superclaude/cli/review/findings_v2.py:155-164` holds the same label-rule text as this branch (checked 2026-11-13).

### 10.1 Rule A — the prose consequence rule (spec-panel Review Loop)
`spec-panel.md:259`: "grade by consequence, not by label; CRITICAL is blocking; a MAJOR or an FR-8/FR-9 finding is blocking only if it names a concrete wrong outcome an implementer would produce or a security, data-loss or safety-boundary risk, otherwise it is Medium (a warning listed under `follow-up candidates`); MINOR is a note; Medium and minor findings never trigger a revision, never fail a review and never appear in the Reviser brief." Verdict: FAIL iff a blocking finding is open (`spec-panel.md:260`). A brief "may not grade a minor finding as blocking" (`spec-panel.md:264`). FR-8 GAP rows follow the same consequence test (`spec-panel.md:332`).
The reviewer prompt operationalises it: "Write the sentence 'An implementer who follows the stated text as written builds X, and X is wrong because Y.' Blocking needs a sentence that holds with no further assumption: two stated texts that contradict ..., a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass ... A Medium finding goes under follow-up candidates even when its label is MAJOR." (`origin/master:src/superclaude/rules/prompts/document_review_loop_prompts.md:31`, read via `git show` 2026-11-13).
- Who applies it: **each reviewer, to its own findings** (self-grading). "Medium" is not a severity value in the parser (`SEVERITIES` CRITICAL/MAJOR/MINOR, used by `findings_v2.py:103-104`), so Medium is encoded as `MAJOR` + `blocking: false`.

### 10.2 Rule B — the label rule in code (`findings_v2.py:161-162`)
With `reflect_category` set, `blocking == (severity != MINOR)`: MAJOR/CRITICAL must be blocking. This **forbids** Rule A's "Medium" (MAJOR, not blocking). It applies to any finding carrying `reflect_category`, regardless of lens (the check at :155-164 does not read `lens`) [CODE-VERIFIED].

### 10.3 Which governs
- In the spec-panel loop (E3), findings are parsed as findings-v1 by `superclaude review merge` (hand-off §5.2; not re-read here) and the ledger takes each member's flag: `row["blocking"] = any(m["blocking"] for m in group)` (`ledger.py:187`), re-found rows recompute from the current round (`ledger.py:213-218`), the Reviser brief = blocking rows with status open/regressed (`ledger.py:99-104`), and `verdict = "FAIL" if brief else "PASS"` (`ledger.py:274`) [CODE-VERIFIED, this branch]. `ledger.py` computes `confidence` overlap/single (`:86-90`) but `_decision` (`:93-96`) never reads it [CODE-VERIFIED].
- So **Rule A governs the spec lens, but only as the reviewer's own judgement**; code enforces nothing of it except "MINOR cannot be blocking" (`findings_v2.py:107-108`, and the v1 parser per hand-off D1/§5.2). Rule B governs **only findings with `reflect_category`**, i.e. converted legacy reflect cards (`card_convert.py:218-219`) and any reflect finding that chooses to set it. The two rules do not collide in today's code paths because no spec-lens producer sets `reflect_category`, but nothing forbids it, and if a unified panel requires `reflect_category` everywhere, Rule B would make Rule A's "Medium" unrepresentable.
- Net: on master the **effective** blocking decision is the single reviewer's boolean, unioned across the cluster (`ledger.py:187`) — hand-off D4 [CODE-VERIFIED here for ledger.py; E2 confirms "0 violations over 264 merges", scope 01 :128].

Key Takeaways
- [E3] Rule A (consequence, `spec-panel.md:259`) is a reviewer instruction; Rule B (label, `findings_v2.py:161-162`) is a parser check limited to findings with `reflect_category`. Neither is a panel-level decision.
- [E3] What actually decides the verdict on master is any one reviewer's `blocking: true` in a cluster (`ledger.py:187`, `:274`).
- [E1/E3] Rule A and Rule B conflict on "MAJOR but not blocking"; a unified contract must pick per lens (Rule A for spec, deviation-class rule for reflect, never the bare label rule).

---

## 11. E2 evidence that a single reviewer's veto produces wrong blockers (question 7) [E2]

All from `git show 4a22d74213f93837d00c2c314075dd967b9a98e3:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/<path>`, read 2026-11-13. Runs date 2026-11-11 to 2026-11-13; model ids are time-bound gateway ids.

- **Judge-blocking overstates real blocking 65 vs 38** over 71 valid-era rows: "The judge's gt_covered_blocking = defect matched by a blocking-flagged ledger row, which can include defects that are not blocking_in_implement ... Over 71 rows the judge counts 65 'blocking' catches but only 38 are real blocking defects" (`COMBO-REPORT.md:291`, item 1). Example: "ember + 2x luna 1.00 judge-blocking is 0.17 real" (same line). Mechanism: a ledger row is blocking whenever any member flagged it (§10.3), so a real defect that some reviewer over-grades as blocking counts as a "blocking catch" though it did not block implementation.
- **Wrong blockers** = "blocking ledger rows with no ground-truth correspondence" (`PILOT-REPORT.md:14`). Final AS-SCORED table (`COMBO-REPORT.md:303-337`): wrong blockers on the two defect-rich packages range 0.00-4.75 per run; replicated panels: ember + 2x luna 1.83 (n=6, :331), haiku + 2x luna 3.00 (n=5, :319), ember + haiku + terra 3.20 (n=5, :323), 2x ember + 2x luna **4.75** (n=4, :332). Control package (0 known blocking defects) "Ctl wrong blk" 0.00-2.00 per run, replicated panels 0.83-1.75 (e.g. 2x ember + haiku + 2x luna 1.75, :316; ember + luna 1.50, :317).
- **Statistically surviving result:** "2x luna + 2x ember has 2.75-3.25 more wrong blockers than every comparator (permutation p 0.005-0.03)" (`COMBO-REPORT.md:298`). This is the clearest veto effect: adding reviewers under an any-reviewer-blocks rule adds blockers without adding real catches (that panel: found 1.75/14, real blocking 0.25/8, :332).
- **Caveat stated by E2:** "GT penalizes novel-but-real catches as wrong blockers ... the control package shows the cleaner signal (0-2 per combo there)" (`COMBO-REPORT.md:63`, `:75`; `PILOT-REPORT.md:79`). So wrong-blocker counts on defect-rich plans are an upper bound; control-package wrong blockers are the cleaner false-positive measure.
- **The veto fails in the other direction too:** pilot "Single-reviewer Arm A passed both defect-rich packages — the worst observed outcome for a gate whose job is to fail bad plans" (`PILOT-REPORT.md:71`; table rows :22, :30 verdict PASS); all three pilot arms had 0/8 blocking recall (:71). Merge drops flipped verdicts FAIL->PASS (named three plus total-loss merges, `COMBO-REPORT.md:292`; scope 01 H15 notes the count "four" is not supported).
- Scope 01 also confirms from audit-D that the merge itself behaves as designed: "row blocking == any member blocking, verdict FAIL iff a blocking row, 0 violations over 264 merges" (`research/scope/01-other-branch-study.md:128`). So the wrong blockers are a **policy** outcome, not a code bug.

Key Takeaways
- [E2] Under the any-reviewer veto, 27 of 65 judge-blocking catches (42%) were not real blockers (`COMBO-REPORT.md:291`), and the one panel that doubles two models gained ~3 wrong blockers per run with p 0.005-0.03 (`:298`).
- [E2] The same veto still missed every real blocker in the pilot (0/8) and passed both defect-rich plans with one reviewer (`PILOT-REPORT.md:71`): the veto is both too loose (false blockers) and gives no recall guarantee.
- [E2] Evidence is from 3 packages, 71 rows, n=4-6 replicates per panel; wrong-blocker counts on defect-rich packages include novel real finds (upper bound).

---

## 12. Class-disjoint calibrator (§11.3) versus id-based distinctness in `panel.py` (question 4) [E1, shared kernel with E3]

- `panel.py` distinctness is by **model id**: `exclude = tuple(chosen)` (ids already picked) when `distinct_across_slots` or `strict_distinct` (`panel.py:631-635`); `resolve_slot` filters candidates by id (`:519-529`, `:539`). Without `strict_distinct` an exhausted pool re-admits duplicates (`:540-543`; hand-off D11).
- Classes are used only to (a) require every reachable model of a reflect template to have a `classes` entry and not be Fable (`panel.py:80-134`, `:137-155`), (b) translate `--hard-exclude-class <class>` into model ids (`panel_cmd.py:54-101`), and (c) report excluded classes (`panel.py:700-705`). **No check that resolved reviewers have distinct classes** (`_check_reflect_resolution` :137-155 checks Fable, classes entry, launch, count only) [CODE-VERIFIED].
- **No calibrator role in `panel.py`**: grep for `calibrat` in `panel.py` returns nothing (only `distinct|class` hits) [CODE-VERIFIED]. The calibrator's class is chosen by the orchestrator following SKILL.md §11.3 prose.
- Class map (`review-tiers.default.json` `classes`): opus, sonnet, haiku, fable for Claude; `gpt` for gpt-6.1-sol, gpt-6.1-terra, gpt-6-luna; `muse` for three muse models; `glm`, `grok`, `qwen` [read 2026-11-13 via `jq`]. So "2x luna" or "luna + terra" pass id-distinctness only partly (2x luna fails it; luna + terra passes) and both fail a class-disjoint rule.
- §11.3's class list `{opus, sonnet, haiku, qwen, kimi, deepseek}` (SKILL.md:1248) does not match the tier file classes: `kimi` and `deepseek` have no models; `gpt`, `muse`, `glm`, `grok` are absent from §11.3. Under `anthropic-only`, reviewers {sonnet, haiku, opus} leave the §11.3 disjoint set = {qwen, kimi, deepseek}, none launchable, so the calibrator is always `degraded` (`reflection-rubric.md:157` Example C; scope 03 :170).
- Conflict with E2: E2's only surviving positive doubling effect is a **second luna** (+0.83 control found, `COMBO-REPORT.md:298`), which both `strict_distinct` (id) and §11.3 (class) would forbid.

Key Takeaways
- [E1/E3] Two different independence rules exist: id-distinct reviewers (code, `panel.py:631-635`) and class-disjoint executor/reviewers/calibrator (prose, SKILL.md:1244-1258). They do not conflict in code because the calibrator is not in the panel code at all.
- [E1] A panel-core calibrator role needs: a calibrator slot in the template, selection by **class** from the tier file `classes` map, and a §11.3 class list replaced by the tier file classes.
- [E2 vs E1] Class disjointness forbids the one doubling E2 found useful; the unified rule should apply class-disjointness to the **decider** (calibrator/grader), not necessarily to the finders.

---

## 13. The exact rule from a findings-v2 finding to reflect flags and to a panel `blocking` flag (question 1)

What the code does today is in §1, §7, §9, §10. Below, **C** = derived from code/doc text cited; **P** = my proposal where no rule exists (no code or doc states it). [E1] unless noted.

### 13.1 Per finding (after `check_finding` passes and the evidence validator keeps it)
1. `channel_of(f) == "advisory"` -> `blocking := false`; feeds no flag (C: `deviation-taxonomy.md:162`, never gates). Today the parser allows `blocking: true` here (§7) — **P: reject it**.
2. `channel_of(f) == "grounding-gap"` -> not a deviation, `blocking := false` as a defect; but its presence sets `needs_human_decision: true` and `status: partial` (C: SKILL.md:1155-1158), both of which halt (`contract.py:367-368`, `:373-374`) and classify human-required (`contract.py:410-417`). **P: reject `blocking: true` on this channel; route it through `needs_human_decision`.**
3. `channel_of(f) == "defect"`, by effective lens (`findings_v2.py:140-145`):
   - **reflect-post** (`deviation_class` required, `findings_v2.py:147-149`):
     - `regression` -> `deviation_count_by_class.regression += 1`; `blocking := true` (C: halts via `contract.py:377-379`; SKILL.md:1176/:1188 call Drift/Regression "blocking" classes). `regression_present := true` **only** when the regression is evidence-sourced per SKILL.md §10.4 (exit-code taxonomy :1105-1117, real-boot sink :1123) — a reviewer's classification alone increments the count, not the flag (C: SKILL.md:853, :1117). Both halt in code, so the verdict effect is the same; the distinction matters for `classify_fix` only via the flag (both are human-required, `contract.py:410-417`).
     - `drift` -> `deviation_count_by_class.drift += 1`; `blocking := true` (C: `contract.py:380-381` halts on any drift count). Note this makes even reflect-reviewer **LOW** "cosmetic / minor drift" (`reflect-reviewer.md:71`) halting, and it collides with the parser's "MINOR cannot be blocking" (`findings_v2.py:107-108`). **P: a drift finding at MINOR is counted (halts per contract) but carries `blocking: false`; or the contract changes to count only MAJOR+ drift. Owner decision.**
     - `authorized`, `necessary` -> counts only; `blocking := false` (C: not read by `_halted_reason`; SKILL.md:1062, :1078). `necessary > 0` makes `classify_fix` auto-fixable (`contract.py:418-419`).
     - `none` -> no deviation; `blocking := false` **P**.
     - `unauthorized_deviation_present`: **no rule exists** (§2.3). **P options:** (a) never set by the panel (status quo in text); (b) `true` iff a kept `drift` finding is MAJOR+ (keeps minor drift auto-fixable, makes material drift human-required). The choice changes `classify_fix` (`contract.py:414` vs `:418`).
   - **reflect-pre** (UC-1): the contract's deviation counts are "UC-2 specific" (SKILL.md:753-759), so no flag is derived. Blocking for UC-1 findings: **P** apply the spec-lens consequence rule (below), because a UC-1 finding is about a plan text; if `reflect_category` is set, the code forces `blocking == (severity != MINOR)` (`findings_v2.py:161-162`).
   - **spec** [E3]: CRITICAL -> blocking; MAJOR -> blocking only if the consequence sentence holds, else "Medium" = MAJOR + `blocking: false`; MINOR -> never (C: `spec-panel.md:259`; prompts `:31`; parser `findings_v2.py:107-108`). Decided by the reviewer today.
4. Converted legacy cards: blocking must be **re-derived from `deviation_class`** for reflect lenses, not taken from the severity word (`card_convert.py:36-37` maps MEDIUM drift to non-blocking), and two-word class labels must be normalised first (`card_convert.py:203`).

### 13.2 Per cluster (panel level)
- Today: `blocking := blocking_any` (`cluster.py:46-47`, `:375`; `ledger.py:187`), verdict FAIL iff any open blocking row (`ledger.py:274`) [E1/E3].
- For reflect-post, the cluster cannot merge different non-null classes unless one is `none` (`cluster.py:157-158`); a cluster's class should be the highest-precedence member class (Regression > Drift > Necessary > Authorized, SKILL.md:1135) — **P**, mirroring the per-file union rule (`deviation-taxonomy.md:15`).
- What changes the panel decision is the aggregation option in §14.

Key Takeaways
- For reflect-post the rule is fully determined by `deviation_class` + `channel` (C), except two owner decisions: MINOR drift, and the producer of `unauthorized_deviation_present` (P).
- For spec/reflect-pre the per-finding decision is the consequence rule applied by the reviewer (C, `spec-panel.md:259`); the panel-level aggregation is the open question.

---

## 14. Options for the blocking decision, with evidence (question 8)

| Option | Mechanism | Exists today | Evidence for | Evidence against | Cost |
|---|---|---|---|---|---|
| **Single-reviewer veto** | any member `blocking: true` -> row blocking -> FAIL | master ledger (`ledger.py:187`, `:274`); `cluster.py:375` [E3/E1] | maximises recall in principle; simple; deterministic | 65 judge-blocking vs 38 real (`COMBO-REPORT.md:291`); 2x ember + 2x luna +2.75-3.25 wrong blockers, p 0.005-0.03 (`:298`); still 0/8 real blocking recall in the pilot and a single reviewer PASSED both defect-rich plans (`PILOT-REPORT.md:71`) [E2]. Reflect itself degrades single-reviewer merges (`contract.py:295-296`) [E1] | none extra |
| **Quorum** (k of n reviewers flag the cluster blocking) | count distinct reviewers with a blocking member | not implemented; `ledger.py:86-90` computes overlap/single, unused; `cluster.py` has `blocking_all` and `reviewers` [E1/E3] | would directly cut uncorroborated blockers; E2 shows blockers rise with reviewer count under a veto (`:298`) | E2 recall is already ~2/14 any and ≤1.2/8 real blocking, and a few issues carry nearly all catches (hand-off R2: B3, I2, I8) — a quorum risks dropping the few real blockers (how many real catches came from a single reviewer was not measured; E2's per-reviewer attribution was retracted, `COMBO-REPORT.md` via hand-off §2.5); rubric B1-B3 says "experts agree" is never a reason to block (`rubric.md:13`) [E3]; clustering chains (83 chained rows, hand-off D6) make counts noisy | none extra |
| **Calibrator-weighted** | cluster blocks when `blocking_any` and `support ≥ θ` (or member confidence ≥ θ) | `support`, `disputed`, per-finding confidence exist (`cluster.py:39-49`, `:336-351`); shadow coverage 142/142 (§5.2); Reuse-Miss precedent `confidence ≥ 0.85` (SKILL.md:1176) [E1] | blocking findings scored higher (mean 0.80 vs 0.66, §5.3); blind, class-disjoint calibrator is the protocol's anti-anchoring guard (SKILL.md:1242, :1260) | 0/689 legacy numeric calibrations (`stage0a-report.md:376`); calibrator agent is a troubleshoot 6-dim card-level grader with no rubric override (§4); calibrator always `degraded` in anthropic-only (§12); no ground truth for any θ; "placebo risk" warning (`confidence-calibrator.md:159`) | +1 calibrator call per card (already paid in reflect legacy) |
| **Blind grader** | a separate blind agent decides blocking per claim from quote + outcome + evidence under a frozen rubric | `finding-grader` + RUBRIC v1, only in `~/.claude` and the phase-5 bundle (§6) [E3] | separates finding from deciding; explicit, frozen criteria; "verified" evidence via script; addresses E2's failure mode (blocking flag set by finders) | no measured accuracy in the files read; rubric is spec-text specific, would not block reflect Drift (§6); not in `src` | +1 grader call per batch of claims |
| **Debate** | `sc-adversarial-protocol` Mode A merges cards; convergence routes PASS/PARTIAL/FAIL; reflect degrades < 0.80 | reflect legacy, authoritative (SKILL.md §8; `contract.py:299-326`) [E1] | heterogeneous reviewers + different-class judge is the protocol's stated defence (SKILL.md:1264-1266); low convergence is surfaced as DEGRADED, never PASS | no recorded evidence measures debate correctness. (The Stage 0 figure "agreement 24/358 = 6.70%" (`stage0a-report.md:293-297`) is NOT evidence against debate: it is a descriptive overlap figure, the share of recorded merged-verdict findings that fall in a multi-reviewer cluster of the code replay, and the report says it "is descriptive and seeds no gate" (:295). A low value says the two methods group findings differently; it says nothing about which is right. [E1] [CODE-VERIFIED by re-reading the report]); 8 null convergence scores in Stage 0 (`research/scope/04-this-session-artifacts.md:188`, [UNVERIFIED] here); judge identity often `unknown` (scope 03 :112); no ground-truth evaluation of debate blocking in E1 or E2 | highest (multi-round debate) |

Combinations visible in the evidence (my reading, not a decision): finders flag -> a **blind decider** (grader or calibrator, class-disjoint from the finders) confirms per cluster -> verdict, with per-lens rubrics (spec: consequence/B1-B3; reflect-post: deviation class). This keeps E2's useful same-model doubling for finding (§12) while removing the finder's veto, and reuses `cluster.py` `support` as telemetry to measure the decider. Any θ or quorum k needs the E2 ground-truth packages (3 packages, 16 known defects) as a regression set before it is chosen.

Key Takeaways
- [E2] The single veto has the only direct ground-truth evidence, and it is negative on precision (65 vs 38; +~3 wrong blockers with 4 reviewers) and gives no recall guarantee.
- [E1] Calibrator-weighting has all data plumbing in `cluster.py` and full shadow coverage, but no ground truth and a mis-fitted calibrator rubric.
- [E3] The blind grader is the only component built to decide blocking; it is unmeasured and spec-specific.
- No option has been evaluated against ground truth except the veto; the E2 packages are the available test bed.

---

## Gaps and Questions

- **[UNVERIFIED]** Producer of `unauthorized_deviation_present`: declared at SKILL.md:854 with no rule anywhere in `sc-reflect-protocol/`; consumed as a halt/human-required flag (`contract.py:371-372`, `:414`). Scope 03's "unjustified Drift sets it" is an inference.
- **[CODE-CONTRADICTED]** SKILL.md:631 / :416 "calibrator re-grades per the 5-dim reflection rubric": `confidence-calibrator.md:48`, `:61`, `:67` implement a 6-dim troubleshoot rubric with a gated-min formula; no `rubric_path` override is written anywhere in the reflect skill. Which rubric the recorded calibrators actually applied was not sampled.
- **[UNVERIFIED]** SKILL.md:1260 "sc-adversarial-protocol's debate is weighted by calibrated confidence": not traced into the adversarial skill.
- **[UNVERIFIED]** SKILL.md:1155-1158 producer side (orchestrator sets `status: partial` and `needs_human_decision` when grounding gaps exist) — protocol prose, no code producer; only the consumer (`contract.py`) was read.
- Stage 0 debate/cluster agreement figure (6.70%) re-read in the Phase 3 fix cycle 1 (`stage0a-report.md:293-297`): it is an overlap figure between recorded merged verdicts and the cluster replay, explicitly descriptive (:295); it is not a correctness measure of debate and is no longer used as evidence against debate in §14.
- **[UNVERIFIED]** rf-qa "IMPORTANT is blocking" (scope 05 :146) vs `card_convert.py:82` mapping `important` to MINOR; rf-qa file not read.
- **[UNVERIFIED]** findings-v1 parse path of `superclaude review merge` (hand-off §5.2) — `merge_cmd.py`/`findings.py` not re-read; `ledger.py` lines cited were read.
- Conflict: SKILL.md §10.10 "static ... can NEVER set `regression_present`" (:1196) vs `deviation-taxonomy.md:123` static step-5.6a REQUIRED-capability unreachability = Regression; and §9.1 :796 mentions 5.6a. Which governs is unclear.
- Conflict: Drift halts at any severity (`contract.py:380-381`) while findings-v2 forbids MINOR blocking (`findings_v2.py:107-108`) and reflect-reviewer LOW = "minor drift" (`reflect-reviewer.md:71`).
- Conflict: Rule A "MAJOR but not blocking" (Medium) vs Rule B label rule with `reflect_category` (`findings_v2.py:161-162`); the label rule is not lens-scoped.
- Gap: `findings_v2.check_finding` allows `blocking: true` on `channel: advisory` / `grounding-gap` and on `authorized` / `necessary`.
- Gap: `card_convert` severity-word policy (MEDIUM -> non-blocking) and two-word label miss (`card_convert.py:203`).
- Gap: calibration layout still varies (4 of 14 shadow runs unfenced `calibration:`), though `review cluster` reads both.
- Gap: no ground truth for E1 shadow runs; the §5.3 confidence/blocking association is not accuracy evidence.
- Gap: finding-grader accuracy unmeasured in what was read; stoprule material not in `src` (`git ls-files` shows only `.dev/experiments/346-validation/phase5/...`).
- Question: should class-disjointness apply to finders (E2's useful 2x luna would be forbidden) or only to the decider?
- Question: does a unified panel keep the debate as the decider (no contract bump) or move the decision into a script + blind decider (needs a new `merge_method`, SKILL.md:837)?

## Stale Documentation Found

- **[STALE DOC]** `refs/reflection-rubric.md:39` dimension 3 vocabulary `{Aligned, Refinement, Drift, Regression}` vs the 4-class taxonomy `{Authorized, Necessary, Drift, Regression}` (SKILL.md:1050-1094; `contract.py:40`; `findings_v2.py:38`).
- **[STALE DOC]** SKILL.md:1248 / `reflection-rubric.md:139` calibrator class list `{opus, sonnet, haiku, qwen, kimi, deepseek}` vs tier-file classes (opus, sonnet, haiku, fable, gpt, muse, glm, grok, qwen); kimi/deepseek have no models.
- **[STALE DOC]** SKILL.md:631 "5-dim reflection rubric" vs the calibrator agent's own 6-dim troubleshoot contract (`confidence-calibrator.md:3`, `:48`, `:61`).
- **[STALE DOC]** SKILL.md:344 asks for "a fenced `yaml` block" for calibration; 4 recorded shadow runs (shadow10, 12, 14, 15) write it unfenced.
- **[STALE DOC]** SKILL.md:655 rotation "(qwen | kimi | deepseek if alias available; else opus)" — no kimi/deepseek models exist in the tier file (scope 03 Q5 also flags this).

## Summary

Blocking is decided three different ways across the three efforts: on master [E3] by any single reviewer's `blocking` flag unioned over a cluster (`ledger.py:187`, `:274`; the same `blocking_any` in `cluster.py:375` [E1]), in reflect [E1] by deviation class at contract level (Regression or Drift count > 0 halts; Authorized/Necessary never do; single-reviewer merges and convergence < 0.80 degrade; `contract.py:295-326`, `:377-381`), and in the stoprule experiment [E3] by a blind grader under rubric B1-B3 that explicitly rejects agreement as a reason. For reflect-post the per-finding rule follows from `deviation_class` and `channel`, but the producer of `unauthorized_deviation_present` is undefined and MINOR drift collides with the parser; `card_convert` additionally maps MEDIUM drift to non-blocking and drops two-word class labels. Calibration exists only as a troubleshoot card-level agent with no reflect rubric override (0 of 689 legacy per-finding numbers), though the shadow brief line yields 142/142 per-finding scores and `cluster.py` already computes a calibrator-weighted `support`. The only ground-truth evidence [E2] is against the single veto (65 judge-blocking vs 38 real; +2.75-3.25 wrong blockers when doubling two models, p 0.005-0.03; 0/8 pilot recall), while calibrator-weighting, quorum, blind grading and debate are all unmeasured — the E2 packages are the available regression set for choosing among them.

