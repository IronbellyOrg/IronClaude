# Qualitative scoring, Pass 2 (reverse order: V3, V2, V1)

Code spot-checks done (all under src/superclaude/): cli/review/panel.py:380-418,479-512; cli/review/data/review-tiers.default.json (whole file); cli/reflect/ensemble.py:772-832; cli/reflect/contract.py:285-330; cli/review/merge_cmd.py:21-71; skills/sc-reflect-protocol/SKILL.md:604-610, 789, 945-970; refs/cost-profile.yaml:69-70.

Notes that drove verdicts:
- V3 claims checked and correct: fixed slot takes `candidates[0]`, random/round_robin fall back to the full list, ensemble constants `verification_ran: False` and `citations_dropped: 0`, hard kill 1.25x the midpoint (cost-profile.yaml:69-70). Arithmetic re-added correctly.
- V2 claims checked and correct (panel.py:402-409, tiers json lines 14/20/27/28/29, ensemble.py:797, contract.py:295/299/317). But V2 calls stage 5 an "additive 1.9.0" while widening the EV-2 legal set of `merge_method` and changing wrapper triggers. SKILL.md:952-953 says a minor bump has "no semantic change to existing fields" and a semantic change is major. V2 never read section 9.4 (it lists it as UNVERIFIED).
- V1 claims checked and correct (panel.py:402-409, tiers json:27/28/29, SKILL.md:607, 789, 952-953, contract.py:299 mis-fire on null convergence, merge_cmd options). V1 correctly treats the enum widening as a 2.0.0 major.
- No variant gives probability and impact per risk (RISK-1 NOT MET for all).

## Variant 1

| Criterion | Verdict | Evidence |
|---|---|---|
| COMP-1 | MET | Headings "Answers to Q1-Q7", "Candidate architectures" (A-E), adapter sketches, staged migration, mapping, cost model, first measurement |
| COMP-2 | MET | "If merge_round refuses the round because no valid block exists ... take the F2 path"; Risk 5 format non-compliance |
| COMP-3 | MET | Stage table "Entry criteria" column; "grep shows no contract_version == 1.8.0 equality check remains" |
| COMP-4 | MET | First measurement "Pass: all four must hold" (recall, precision, tokens cut by 80%, status agreement 18 of 20) |
| COMP-5 | MET | "Extension point, not built"; "Stage 6 ... not planned until data exists"; condition 9 second clause "explicitly out of scope" |
| CORR-1 | MET | Checked: panel.py:402-405 fixed ignores exclude; tiers json:27 Fable listed; contract.py:299 trigger 11 would mis-fire; SKILL.md:953 major rule |
| CORR-2 | MET | Shadow mode with legacy debate authoritative; 2.0.0 only after every consumer updated; builds only on existing merge options (merge_cmd.py:21-70) |
| CORR-3 | MET | K1-K4 layers and `findings-v2`, `panel_agreement_score` used consistently throughout |
| CORR-4 | MET | No substantive contradiction; table "34-66k" vs cost model "about 35-68k" is rounding under "about" |
| CORR-5 | MET | "The spec-panel gain ... was measured with a revise loop on specs. C adopts the panel for maintainability" plus path:line cites |
| STRU-1 | MET | Summary, candidates, chosen, Q1-Q7, format, adapters, migration, mapping, cost, risks, measurement, assumptions |
| STRU-2 | MET | `##` sections with `###` per question and per adapter, consistent |
| STRU-3 | MET | Separate sections for format, adapters, migration, contract mapping, cost |
| STRU-4 | MET | Comparison table; Q1 function table; "(see mapping section)" cross-references |
| STRU-5 | MET | Alternatives, decision, migration, rollback, risks, open items |
| CLAR-1 | MET | "Pre-execution: K4 deterministic merge is the default. A scoped debate ... only with `--depth deep`." |
| CLAR-2 | MET | Concrete JSON template `reflect-pre`; full `superclaude review merge --schema findings-v2 --doc plan=...` command |
| CLAR-3 | MET | Each section states its purpose ("Direct answer:" lead lines) |
| CLAR-4 | MET | "K1 Resolution: `review-panel-resolution/1` plus ..." defined on first use; `panel_agreement_score` defined formula |
| CLAR-5 | MET | Stage table exit criteria; "Fail: ... pre stays on the debate"; owner sign-off at Stage 4 |
| RISK-1 | NOT MET | Searched Risks 1-8 and candidate "Risk: medium": no probability or impact rating on any risk |
| RISK-2 | MET | Every risk has "*Mitigation:*" (e.g. Risk 4 `hard_exclude` raises instead of falling back) |
| RISK-3 | MET | Risk 5 "one bounded re-ask ... then the F2 single-reviewer fallback"; per-stage Rollback column |
| RISK-4 | MET | Risk 6 "Gateway dispatch through the Agent tool is undefined ... Stage 1 exit check; gateway stays on legacy" |
| RISK-5 | MET | "`findings_schema` telemetry tracks the compliance rate"; Stage 2 "EV-1 failure rate no higher than legacy" |
| INVR-1 | MET | "returns a valid block" minimum 2; "1.0 when there is no blocking cluster and at least 2 valid blocks"; citations "list 1..8" |
| INVR-2 | MET | Calibration and validation sidecars; "Only validator-kept findings enter clusters"; reviewer output never mutated |
| INVR-3 | MET | "`distinct_across_slots` is soft (panel.py:405, 408) and fixed slots ignore exclusion"; Fable-rejecting validation |
| INVR-4 | MET | EV-1 panel path: "`ledger.rounds[0].reviewers` has at least 2 entries with valid blocks ... cards count"; `citations_dropped_precheck` as component |
| INVR-5 | MET | "Side effect worth stating": reflect-pre template makes calibrator class disjoint and changes `calibrator_diversity` to full |

Subtotals V1: COMP 5/5, CORR 5/5, STRU 5/5, CLAR 5/5, RISK 4/5, INVR 5/5. **Total 29/30.**
Edge-case floor (INVR subtotal): 5/5, floor of at least 1 met.

## Variant 2

| Criterion | Verdict | Evidence |
|---|---|---|
| COMP-1 | MET | Headings "Answers to Q1-Q7", candidates A-D, "Adapter sketches", "Staged migration", mapping, cost model, first measurement |
| COMP-2 | MET | Risk 10 "Executor exclusion can empty a fixed slot ... must drop the slot and report, not raise"; Risk 2 block compliance |
| COMP-3 | MET | Stage table entry column ("stage 0 shows panel-fed arm not worse"); "UNVERIFIED (not read this session)" list |
| COMP-4 | MET | "Stage 1 proceeds only if panel-fed T2 recall is within 5 points ... cost is at most 1.1x current T2" |
| COMP-5 | MET | Risk 9 "The migration does not fix this. Flag it for a separate task."; Q6 ledger across runs "optional and later" |
| CORR-1 | NOT MET | "Stage 5 would be an additive 1.9.0" yet adds `panel-deterministic` and edits EV-2; SKILL.md:952-953 makes a semantic change major. Other spot-checks correct |
| CORR-2 | MET | Concatenated `review-doc.md`, existing `parse_block` reuse, `launch` null routes to swarm; all steps use existing or flagged PROPOSED pieces |
| CORR-3 | MET | "panel-fed T2", stage names B/C/C2 mapped to stages; `reflect-finding/1` consistent |
| CORR-4 | NOT MET | Own text says stage 5 "needs a versioned change because EV-2 makes any other merge_method MALFORMED" but labels it additive; candidate C "-5k to +3k" vs cost model "Net: 0 to -2k" |
| CORR-5 | MET | "Card 1 shows calibration working ... scored them 0.60, 0.50 and 0.55" with card path cite; McNemar arithmetic shown |
| STRU-1 | MET | Summary, candidates, chosen, Q1-Q7, finding format, adapters, migration, mapping, cost, risks, measurement, assumptions |
| STRU-2 | MET | `##` sections, `###` per question and adapter, consistent |
| STRU-3 | MET | Format, adapters, migration, mapping and cost in separate sections |
| STRU-4 | MET | "Comparison" table; Q1 table; "See 'Finding format' below" cross-references |
| STRU-5 | MET | Alternatives, decision, staged rollout, risks, assumptions |
| CLAR-1 | MET | "Both, in sequence. Deterministic clustering runs first. The debate then runs over the cluster table" |
| CLAR-2 | MET | Command `superclaude review panel resolve --template @reflect-pre --run-id ... --exclude-model`; rotation-to-slot mapping table |
| CLAR-3 | MET | Each Q opens with "Direct answer." and sections have a single purpose |
| CLAR-4 | MET | "Conventions" paragraph defines `<sr1>`, PROPOSED and UNVERIFIED on first use |
| CLAR-5 | MET | Stage entry/exit table; "If not, record that the 35k-70k are not buying recall ... shrink T2 to 2 reviewers" |
| RISK-1 | NOT MET | Searched Risks 1-10 and candidate table: no probability or impact on any risk |
| RISK-2 | MET | Every risk has "Mitigation:" (e.g. Risk 7 "add a forbidden-model filter to `resolve`") |
| RISK-3 | MET | Risk 2 "loud fallback when none is valid"; per-stage Rollback ("flag off; the hand-written rotation still exists") |
| RISK-4 | MET | Risk 6 "`launch` is `{}` for gateway models. Mitigation: swarm path for null `launch`" |
| RISK-5 | MET | "overlap undercount below 20% against a manual spot-check of 10 runs; block compliance at least 95%" |
| INVR-1 | MET | "`merge_round` raises when no reviewer has a valid block"; "`refs` at most 8"; no refs falls back to span overlap; empty fixed slot |
| INVR-2 | MET | Ledger drops extra fields so "reflect joins its sidecar through the ledger's member records"; calibrator resolved first via fixed slots |
| INVR-3 | MET | "`resolve_slot` for a `fixed` slot returns `candidates[0]` and ignores `exclude`"; Fable in tier data |
| INVR-4 | MET | "count only valid-block reviewers toward the N=2 floor" (requested vs valid reviewers) |
| INVR-5 | MET | Stage 5: triggers 10, 11 and 11b "apply only when merge_method == adversarial, otherwise a deterministic-merge run is degraded" |

Subtotals V2: COMP 5/5, CORR 3/5, STRU 5/5, CLAR 5/5, RISK 4/5, INVR 5/5. **Total 27/30.**
Edge-case floor (INVR subtotal): 5/5, floor of at least 1 met.

## Variant 3

| Criterion | Verdict | Evidence |
|---|---|---|
| COMP-1 | MET | Headings "Answers to Q1-Q7", "Candidate architectures" (4 incl. leave as is), adapters, staged migration, mapping, cost, risks, first measurement |
| COMP-2 | MET | "Compatibility tests include T1 stop, two-of-three completion, no survivors, wrong schema, empty valid findings, truncated findings ... validator failure" |
| COMP-3 | MET | Stage table "Entry criteria"; "Installed implementation instructions must resolve agents from project `.claude/agents/` first" |
| COMP-4 | MET | "Pass for wider opt-in: shared recall is within five percentage points of legacy ... median output tokens at most 90%" |
| COMP-5 | MET | Summary "Do not ... import the specification panel's automatic revision loop"; Risk 9 "No new scheduler, daemon, database, remote service" |
| CORR-1 | MET | Checked: panel.py fixed `candidates[0]` and fallback to full list; ensemble.py:808-819 constants; cost-profile hard kill 1.25x midpoint (65.6k) correct; sums re-added |
| CORR-2 | MET | Keeps real adversarial finalizer so 1.8.0 unchanged; atomic publish, manifest; all new pieces tagged PROPOSED |
| CORR-3 | MET | "read the stable `adversarial_convergence_score` into the gate's local `convergence_score`; this is a local name mapping" |
| CORR-4 | MET | Candidate 37-53k vs lane total 37-56k is reconciled ("target versus allowance"); no substantive contradiction found |
| CORR-5 | MET | Evidence cites per claim, e.g. "Evidence: `cli/review/ledger.py:114-121,254-258,301-347`"; cost lanes show arithmetic |
| STRU-1 | MET | Summary, candidates, chosen, Q1-Q7, format, adapters, migration, mapping, cost, risks, measurement, assumptions |
| STRU-2 | MET | `##` sections with `###` per question and adapter |
| STRU-3 | MET | Finding format, adapters, migration, contract mapping, cost kept apart |
| STRU-4 | MET | Candidate table, migration table, contract-mapping table, consumer-by-consumer list |
| STRU-5 | MET | Alternatives, decision, rollback, risks, assumptions and UNVERIFIED list |
| CLAR-1 | NOT MET | Searched for undefined selectors: "two eligible independent slots from lower allowed pools", "conservative multi-file matching", "eligible" never pinned to tiers or rules |
| CLAR-2 | MET | Concrete `review-finding/2` YAML with fields; idempotency identity `(run_id, snapshot_hash, policy_hash, stage, reviewer_id, attempt_id)` |
| CLAR-3 | MET | Each section states its purpose in a bold lead sentence |
| CLAR-4 | MET | "The kernel owns four things: a resolved execution manifest, immutable reviewer submissions ..."; PROPOSED defined in intro |
| CLAR-5 | MET | Stage table exit criteria; "obtain experiment-budget approval before execution"; "owner must explicitly approve that tradeoff" |
| RISK-1 | NOT MET | Searched Risks 1-9: no probability or impact on any risk |
| RISK-2 | MET | Each of the 9 risks carries its mitigation sentence (e.g. Risk 6 "Publish a committed manifest after validating every referenced artifact") |
| RISK-3 | MET | Resume by hashes, "A duplicate merge request returns the committed result"; per-stage rollback; "Every rollback changes only future routing" |
| RISK-4 | MET | Risk 3 alias diversity; "exhausted disjoint pool, alias drift"; "gateway availability ... UNVERIFIED"; bounded fallback chain |
| RISK-5 | MET | "Capture input, output, cached input ... retries and elapsed time separately for each actual class and stage"; completion identity compared to resolution |
| INVR-1 | MET | "`complete|truncated|invalid|failed|timed_out`"; "valid empty array allowed"; "no survivors"; "never seven by default" |
| INVR-2 | MET | State machine `resolved -> dispatched -> ... -> published`; "Replaying a run must not create additional reviewer votes" |
| INVR-3 | MET | "`distinct_across_slots` is not a hard independence guarantee"; constant `citations_dropped: 0` must not be copied |
| INVR-4 | MET | "Only `complete` plus valid schema is eligible to count toward review quorum"; "Counts of deviations are computed once per adjudicated issue, not once per reviewer"; 1.25x midpoint vs max |
| INVR-5 | MET | "Flag changes must not splice a legacy merge into a partially completed shared run"; wrapper ordering preserved |

Subtotals V3: COMP 5/5, CORR 5/5, STRU 5/5, CLAR 4/5, RISK 4/5, INVR 5/5. **Total 28/30.**
Edge-case floor (INVR subtotal): 5/5, floor of at least 1 met.

## Totals

| Variant | COMP | CORR | STRU | CLAR | RISK | INVR | Total |
|---|---|---|---|---|---|---|---|
| V1 | 5 | 5 | 5 | 5 | 4 | 5 | 29 |
| V2 | 5 | 3 | 5 | 5 | 4 | 5 | 27 |
| V3 | 5 | 5 | 5 | 4 | 4 | 5 | 28 |

Edge-case floor line: INVR subtotal V1 5/5, V2 5/5, V3 5/5 (floor of at least 1 of 5 met by all).
