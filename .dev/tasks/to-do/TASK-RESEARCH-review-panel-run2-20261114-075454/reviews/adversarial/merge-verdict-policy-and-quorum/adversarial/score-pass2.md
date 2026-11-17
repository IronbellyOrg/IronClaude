PASS 2 (reverse order: Variant 2 then Variant 1)

Scope: C-03 position papers, original files only. Variant 1 = Proposal A (union default), Variant 2 = Proposal B (adjudicated default). Debate evidence is cited as `debate:<round/advocate>`. V1 = Variant 1, V2 = Variant 2 in the tables.

## Completeness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| C1 | V2 | MET | Position (section 1), all four invariants INV-I/B/L/A in section 4, and research cited for r03, r06 (E8), r07 (E15/E16), r08 (E12), r12 (section 4 INV-J row), r17 (section 7 "r17 DR-062, DR-137"). |
| C1 | V1 | NOT MET | Position and INV-I/B/L/A are covered (section 4), but no citation of research 06 or 17 anywhere (searched sections 1-7; only 03, 07, 08, 12, 13, web-01 appear). |
| C2 | V2 | MET | Adjudication stage down falls back to `union` and DEGRADED (2.1 item 4); a buggy adjudicator rejecting a true blocker (section 4, INV-I HIGH); failure conditions (a)-(d) in section 5. |
| C2 | V1 | MET | "one valid empty block, three broken gives PASS" (3.1 item 1); quorum matrix over N in 1..5 and all five completion states (section 5 item 1); truncated/invalid/failed/timed_out states. |
| C3 | V2 | MET | Names prerequisites: `model_observed` as "decided requirement, C-08", per-row clearing "slot C-02 ... assumed independent", wire format "slot C-10" (2.1 item 5, 2.3, section 6). |
| C3 | V1 | MET | "only as good as the repair policy of slot C-06" (3.2); "does not decide who types blocking (that is slot C-02)" (2.1); PR wire format slot C-10 (section 6); manifest counts as the quorum data source (2.1). |
| C4 | V2 | MET | Section 5: "B is shown right if the adjudicated policy lowers wrong blockers per run with no loss of real-blocking recall"; wrong if (a)-(d). |
| C4 | V1 | MET | Section 5 items 1-3 give assertions (DEGRADED when `complete < min_complete`, 36 tests green, 0 replay diffs) and items 4-5 give falsifiers for default and floor. |
| C5 | V2 | MET | 2.3 "does not argue" list; "Per-row clearing is slot C-02"; "The wire-format choice stays slot C-10"; section 6 "neither policy supports describing the panel as a full replacement". |
| C5 | V1 | MET | "does not decide who types blocking (slot C-02)" (2.1); "slot C-10 decides the wire format; this proposal does not depend on it" (section 6); reflect switch to `degrade` "is outside this proposal" (4.2). |

## Correctness

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| K1 | V2 | NOT MET | E11 is tagged [CODE-VERIFIED] as "computed from served model ids", but the gate reads `worker.model_id`, which `openai_compat.py:468` sets to the configured model (debate:R1/A W3; conceded debate:R1/B C3). |
| K1 | V1 | NOT MET | Section 7 says a wrong blocker "costs at most one fix cycle"; on the ledger a Reviser-rejected row stays open to the cap (debate:R2/A R1, conceded). Also "PASS rests on defaults" withdrawn as overstated (debate:R2/A R5). |
| K2 | V2 | NOT MET | 2.1 item 3 says pending blockers "block PASS" but are excluded from the brief; `merge_round` only yields FAIL/PASS (`ledger.py:273-275`), so a pending-only round passes (debate:R1/A W1, conceded debate:R2/B W1). Adjudication stage also does not fit one-call `review merge` (debate:R2/B W5). |
| K2 | V1 | MET | 2.1 specifies a pure function over rows, completion records and policy, using existing `COMPLETION_STATES` and manifest counts, plus an additive exit code; gaps found in debate (`requested` source, `KeyError` at `ledger_cmd.py:109`) are fixable additions, not infeasible. |
| K3 | V2 | NOT MET | "contested" is used for three different rule sets (section 1 versus section 5 item 1, "never defined tightly", debate:R2/B W6); `pending`, `uncalibrated` and `unconfirmed` overlap (2.1 item 3, section 4); "served model ids" misnames configured ids (E11). |
| K3 | V1 | MET | Consistent vocabulary: `union`, `shortfall: degrade/visible`, `min_complete`, requested/resolved/complete, and the outcome set PASS/REVISE/ESCALATE/DEGRADED (2.1); notes that exit 10/11 mean different things in the two products (2.3). |
| K4 | V2 | NOT MET | Section 4 Preserved says INV-L "No verdict changes until a stage that promotes the engine", while 2.2 makes `adjudicated` the spec-loop default and the Endangered table calls that "a behaviour change ... not shadow work" (debate:R1/A W7, conceded R2/B W7). |
| K4 | V1 | NOT MET | Section 1 and 4.1 claim fail-closed "at every panel size" but 2.2 sets reflect to `shortfall: visible` (PASS-eligible 2-of-3); conceded debate:R2/A R4. Header "Status: In Progress" versus closing "Status: Complete". |
| K5 | V2 | MET | Every factual row in 3.1-3.3 carries a source and tag (e.g. E1 `ledger.py:93-104` [CODE-VERIFIED]); the objection answer gives five reasoned points. |
| K5 | V1 | MET | Claims carry file:line and tags (e.g. `ledger.py:150-157`, `:273-275`); the asymmetric-cost argument cites rule S3 and INV-I (section 7). |

## Structure

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| S1 | V2 | MET | Order: position, design, evidence, invariants, test, PR/rf-qa effect, strongest objection (sections 1-7), matching the paper template. |
| S1 | V1 | MET | Same seven-section order (sections 1-7). |
| S2 | V2 | MET | `##` sections 1-7; `###` 2.1-2.3, 3.1-3.3, Preserved/Endangered under section 4; no orphan subsections. |
| S2 | V1 | MET | `##` sections 1-7; `###` 2.1-2.3, 3.1-3.3, 4.1-4.2; no orphans. |
| S3 | V2 | MET | Evidence is split into code (3.1), measured runs (3.2), external (3.3); design (2), invariants (4), test (5), effect (6) and objection (7) are separate. |
| S3 | V1 | MET | Design (2), evidence (3.1-3.3), invariants (4.1/4.2), test (5), effect (6) and objection (7) are separate sections. |
| S4 | V2 | MET | Header "Tags" legend and citation shorthand (`rNN`, `web-01`, `s05`, `UC`); stable evidence IDs E1-E17 referenced across sections. |
| S4 | V1 | MET | Header "Tags" legend ([CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]) and section cross-references ("section 5", "section 7", "2.3"). |
| S5 | V2 | MET | Contains every required element: position, core and module consequences, evidence, invariants, measurement, PR/rf-qa effect, strongest objection with answer. |
| S5 | V1 | MET | Same required elements present, with the objection answered "without weakening the objection". |

## Clarity

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| L1 | V2 | NOT MET | Central term "contested" is ambiguous (debate:R2/B W6); thresholds are vague: "few enough for one batched validator call", "a material share of runs", "essentially every contested blocker" (section 5). |
| L1 | V1 | MET | Outcome set, `min_complete` floor of 2 and `shortfall` modes are stated exactly (2.1); open parameters are named as open ("the quorum floor ... is a parameter nobody has measured"), not hedged. |
| L2 | V2 | MET | Names policies `union`/`adjudicated`, record keys `evidence_gate`/`support`/`adjudication`, and `policy(rows, panel_state, adjudication) -> verdict` (2.1 items 1-2). |
| L2 | V1 | MET | Names `derive_panel_outcome(rows, completion_records, policy)`, `min_complete`, `shortfall`, and the rule "does not reuse 10 or 11" (2.1, 2.3). |
| L3 | V2 | MET | Each section states one purpose (position, consequence, evidence, invariants, test, effect, objection); 3.1/3.2/3.3 are each one evidence class. |
| L3 | V1 | MET | Each section and subsection maps to one purpose (e.g. 2.3 exit codes, 3.2 alternatives' machinery). |
| L4 | V2 | NOT MET | INV-A/B/G/H/I/J/L, D-13, C-08, E2, S1-S5, FX-10 are used without definition (sections 1, 4); only the tag legend is defined. |
| L4 | V1 | NOT MET | INV-A/B/D/J, FR-RH2.9, D-2, C-S3, VM-3, `needs_human_decision`, "E1/E2" are used undefined; only INV-I gets a gloss (section 1). |
| L5 | V2 | MET | Section 5 lists four concrete steps (offline replay, adjudication run, regression gate, served-model check) and "Pre-commit the decision rule before the first run". |
| L5 | V1 | MET | Section 5 lists five numbered tests and measurements; section 7 names the residual product decision and floor parameter to measure. |

## Risk Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| Q1 | V2 | NOT MET | Endangered table gives severity (HIGH/MEDIUM/LOW) for five risks but no probability for any of them (section 4). |
| Q1 | V1 | NOT MET | 4.2 gives impact labels ("HIGH if mishandled", "MEDIUM") for four risks but no probability assessment. |
| Q2 | V2 | NOT MET | INV-I, J, G, H rows state "what B must do", but the INV-L row only states the exposure ("a behaviour change for an existing consumer, not shadow work") with no mitigation (section 4). |
| Q2 | V1 | MET | Each 4.2 risk has a stated handling: rewrite pins with the fix (INV-D), avoid reusing 11 (INV-B, 2.3), switch outside this proposal (INV-A), debate stays authoritative (INV-L). |
| Q3 | V2 | MET | Adjudication stage down: "falls back to `union` and the outcome is the DEGRADED-style state, never PASS" (2.1 item 4); rejections "recorded and counted"; non-independent run "recorded as not independently adjudicated". |
| Q3 | V1 | MET | Partial panel gives DEGRADED and "the module can re-dispatch" (section 6); zero valid blocks keeps the `LedgerError` refusal (2.2); monotonic fail-closed property (section 5 item 2). |
| Q4 | V2 | MET | Covers served-versus-requested model divergence (E16), the adjudicator served by a reviewer's model (failure condition (c)), and the missing capability-ordering file (section 7). |
| Q4 | V1 | MET | Reviewer provider failures covered by `failed`/`timed_out` states (2.1); calibrator losing its class in 6 of 15 runs (3.2); repair loss "92 findings dropped" (3.2). |
| Q5 | V2 | MET | "report rejections per run" (section 4); served-model check "inside the run" (section 5 item 4); regression gate and pre-stated failure conditions (a)-(d). |
| Q5 | V1 | MET | Wrong-blocker rate as "one number" and escalate-at-cap rate falsifier (section 5 items 4-5, section 7); monotonic property test; replay-diff guard (item 3). |

## Invariant & Edge Case Coverage

| Criterion | Variant | Verdict | Evidence |
|---|---|---|---|
| I1 | V2 | MET | "zero valid blocks still refuses" (section 4); single-reviewer re-review uses `union` (2.2); `reviewers_resolved >= 2` threshold (2.1 item 1); large contested set in failure condition (d). |
| I1 | V1 | MET | Quorum matrix "for requested N in 1..5 and every assignment of the five completion states" (section 5 item 1); single-reviewer re-review `requested = 1, complete = 1` (section 6). |
| I2 | V2 | NOT MET | No analysis of how a `pending` adjudication interacts with row `status`, `_brief_ids`, `defer` or the stored round verdict (debate:R1/A W1-W2, conceded debate:R2/B W1-W2); does not note that `merge_round` never reads the manifest. |
| I2 | V1 | MET | "`ledger.merge_round` never reads the manifest" and the round entry gains `requested`/`resolved`/`completion` (2.1); derived-on-read versus stored verdict (`ledger.py:363-372`); ledger versus reflect exit codes (2.3). |
| I3 | V2 | MET | Guards a fail-open path: `rejected` only for a deterministic evidence failure or quoted re-read (section 4); zero valid blocks refuses; E3 names the one-valid-block guard gap. |
| I3 | V1 | MET | 3.1 item 1: the only refusal is `not any(block_ok.values())`; "`ledger.load` checks only the schema string" (2.1); fail-closed below `min_complete` (section 4.1). |
| I4 | V2 | MET | Dispatched versus independent completions versus distinct observed model ids (section 1, 2.1 item 5); "1 valid empty block of 4 dispatched" (E4); requested versus served ids (E16). |
| I4 | V1 | MET | requested versus resolved versus complete counts (2.1); "four dispatched, one valid" (3.1 item 1); boundary "at least 2 complete reviewers when 2 or more were requested" with the 2-of-3 reflect case (2.1, 2.2). |
| I5 | V2 | MET | Policy by situation: first reviews `adjudicated`, single-reviewer re-review `union` (2.2); adjudicator down falls back to `union`; `adjudicated` default in spec loop versus INV-L (section 4). |
| I5 | V1 | MET | `shortfall` mode combined with reflect pins (2.2); quorum with a one-reviewer re-review (section 6); new exit code versus pinned 0/10/11 (2.3). |

## Subtotals

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness | 4/5 | 5/5 |
| Correctness | 3/5 | 1/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 4/5 |
| **Total** | **25/30** | **21/30** |
