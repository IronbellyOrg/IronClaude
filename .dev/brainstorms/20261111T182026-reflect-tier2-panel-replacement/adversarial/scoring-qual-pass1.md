# Qualitative scoring, Pass 1 (FORWARD order: V1, V2, V3)

Spot-checks against repo code (src/superclaude/), used for CORR-1:
- `cli/review/panel.py:402-409`: `fixed` takes `candidates[0]` and ignores `exclude`; random and round_robin use `pool ... or candidates`. Matches V1, V2 and V3 claims. V2 cites `:405, 409`, where the round_robin pool line is 408 (minor).
- `cli/review/data/review-tiers.default.json:20,27-29`: gateway `launch: {}` with the note "dispatch mechanism per model not defined yet". Anthropic-only `launch` maps ids to opus/sonnet/haiku/fable. No `tier1b` stand-in exists. Matches V1 and V2 (including V2 risk 10).
- `cli/reflect/ensemble.py:797,808-817`: `"mode": "post"`, `verification_ran: False`, `citations_dropped: 0` are hard-coded. Line 490-498 gives `snapshot-children-only`. Matches V1, V2 and V3.
- `cli/reflect/contract.py:295,299`: trigger 10 tests `single-reviewer-fallback` only. Trigger 11 is null convergence at T2. Matches V1 and V2.
- `skills/sc-reflect-protocol/SKILL.md:789`: EV-2 legal `merge_method` values are exactly {adversarial, single-reviewer-fallback}. `:950-953` (section 9.4): a semantic change is Major. `:1483`: gate condition 9.
- `cli/review/panel_cmd.py`: only `resolve` and `validate`. `cli/review/merge_cmd.py`: a single `--doc`, and the report is written before `led.save` (V3 claim that the pair is not transactional is correct). `cli/review/ledger.py:52-67` atomic save, `:19` `resolved_check` status.
- `refs/cost-profile.yaml:46-70`: T2 35k-70k, `hard_kill_multiplier: 1.25` on the midpoint (V3 arithmetic 65.6k is correct).
- `agents/reflect-reviewer.md:6-7`: `model: sonnet`, `maxTurns: 50`. The advisory no-spec channel is present (V3 claim).
- `cli/reflect/runner.py:163`: CRLF normalized to LF (V3 claim).

## Variant 1 (architect)

| Criterion | Verdict | Evidence |
|---|---|---|
| COMP-1 | MET | Headings "Answers to Q1-Q7", "Finding format", "Adapter sketches", "Staged migration", "Return-contract 1.8.0 mapping", "Cost model", "First measurement" |
| COMP-2 | MET | Risk 5: "An invalid findings-v2 block makes the reviewer non-clearing"; F2 single-reviewer fallback; hard-exclusion leaving fewer than 2 reviewers degrades to T1 |
| COMP-3 | MET | Stage 3 entry: "every consumer in the 2.0.0 list ... updated and released"; "UNVERIFIED" prerequisites list |
| COMP-4 | MET | First measurement "Pass: all four must hold"; per-stage exit criteria |
| COMP-5 | MET | "another major change and is explicitly out of scope"; "Extension point, not built"; "Stage 6 ... not planned until data exists" |
| CORR-1 | MET | Spot-checks all hold: panel.py:402-405,408; launch map `:29`; ensemble.py:797; contract.py:295; SKILL.md:789; ledger blocking OR |
| CORR-2 | MET | Stage 1 exit lists "Agent-tool alias override checked for gateway (UNVERIFIED item)"; additive flags off by default |
| CORR-3 | MET | `adversarial_convergence_score` and `panel_agreement_score` kept distinct; K1-K4 layer names used throughout |
| CORR-4 | MET | Versioning plan 1.9.0 additive then 2.0.0 major for enum widening, consistent with section 9.4. Minor cost-range rounding only (34-66k vs 35-68k) |
| CORR-5 | MET | Cost model shows arithmetic: "12+16.5+4+0+2.4 ≈ 35"; dedupe rules cite findings.py lines |
| STRU-1 | MET | Summary, candidates, choice, Q1-Q7, format, adapters, migration, contract, cost, risks, measurement, assumptions |
| STRU-2 | MET | Consistent `##` sections and `###` subsections for Q1-Q7 and adapters |
| STRU-3 | MET | Format, adapters, migration, contract and cost are separate sections |
| STRU-4 | MET | "### Comparison" table; Q1 ownership table; contract mapping table; Summary |
| STRU-5 | MET | Candidates, rationale, schema, staged rollout, risks, open items: a standard design-spec shape |
| CLAR-1 | MET | Q3 "Direct answer: both, split by mode"; each Q opens with a direct answer |
| CLAR-2 | MET | Concrete JSON template `reflect-pre`; exact `merge` command line; fingerprint v2 formula |
| CLAR-3 | MET | Each section opens with its purpose; the Q sections open with "Direct answer" |
| CLAR-4 | MET | Header defines PROPOSED; `panel_agreement_score` and "disputed" defined on first use; K1-K4 defined in candidate C |
| CLAR-5 | MET | Stage table with entry, exit and rollback; first measurement with pass and fail branches |
| RISK-1 | NOT MET | Searched Risks 1-8 and candidate "Risk: low/medium/high" lines. Impact is described, but no per-risk probability is stated |
| RISK-2 | MET | Every one of the 8 risks has an italic "*Mitigation:*" |
| RISK-3 | MET | "one bounded re-ask per reviewer ... then the F2 single-reviewer fallback"; per-stage Rollback column |
| RISK-4 | MET | Risk 6 "Gateway dispatch through the Agent tool is undefined"; unverified sc-adversarial judge exclusion |
| RISK-5 | MET | "`findings_schema` telemetry tracks the compliance rate per model"; shadow stage, Stage 0 hand-labelled 50-pair sample |
| INVR-1 | MET | "1.0 when there is no blocking cluster and at least 2 valid blocks"; `citations` list 1..8; fewer than 2 reviewers |
| INVR-2 | MET | Sidecars `calibration.json` and `validation.json` read by K4; "Reviewer output is never mutated" |
| INVR-3 | MET | Risk 4: "`distinct_across_slots` is soft ... fixed slots ignore exclusion"; `hard_exclude` raises |
| INVR-4 | MET | EV-1 panel path: "`ledger.rounds[0].reviewers` has at least 2 entries ... `reviewer-cards/` holds that many cards"; `citations_dropped_precheck` is a component of `citations_dropped` |
| INVR-5 | MET | Q4 "Side effect worth stating": the reflect-pre template makes the calibrator disjoint set {opus} |

Subtotals V1: COMP 5/5, CORR 5/5, STRU 5/5, CLAR 5/5, RISK 4/5, INVR 5/5. **Total 29/30.**

## Variant 2 (analyzer)

| Criterion | Verdict | Evidence |
|---|---|---|
| COMP-1 | MET | Headings "Answers to Q1-Q7" (Q1-Q7), "Finding format", "Adapter sketches", "Staged migration", "Return-contract 1.8.0 mapping", "First measurement" |
| COMP-2 | MET | Risk 10: "Executor exclusion can empty a fixed slot ... drop the slot and report, not raise"; Risk 2 block compliance |
| COMP-3 | MET | Stage table Entry column ("stage 0 shows panel-fed arm not worse"); UNVERIFIED list |
| COMP-4 | MET | "Pass/fail thresholds (PROPOSED)": non-inferiority within 5 points, cost at most 1.1x |
| COMP-5 | MET | Risk 9: "The migration does not fix this. Flag it for a separate task"; post-exec deferred to stage 4 |
| CORR-1 | NOT MET | Line refs are correct (panel_cmd.py:18,69; panel.py:402-403; tiers:20,29; ensemble.py:797). But it labels the stage-5 change "additive 1.9.0" while adding a legal `merge_method` value and rewording gate 9. SKILL.md:953 makes a semantic change Major. Also panel.py:409 is not the pool line |
| CORR-2 | MET | Concatenated `review-doc.md` with `## PLAN` and `## SPEC` is feasible under the single `--doc` constraint |
| CORR-3 | MET | "reflect-finding/1", "cluster table", "C2" used consistently; the info-string reuse is stated as deliberate |
| CORR-4 | NOT MET | Summary and candidate C give "-5k to +3k" but the cost model says "Net: 0 to -2k". Stage 5 totals "30k-63k ... 64 rounded". Stage 5 is "additive 1.9.0" yet edits EV-2 and gate 9 |
| CORR-5 | MET | Reason 2 cites calibrator scores 0.60/0.50/0.55 and the dropped `source.md:143`; sample-size arithmetic is shown |
| STRU-1 | MET | Same logical order as the brief's success criteria |
| STRU-2 | MET | Consistent `##` and `###` depth; Q1-Q7 as `###` |
| STRU-3 | MET | Format, adapters, migration, contract and cost are separate sections |
| STRU-4 | MET | "### Comparison" table; Q1 piece table; contract table; Summary bullets |
| STRU-5 | MET | Standard design-spec shape |
| CLAR-1 | MET | Each Q opens with "Direct answer."; rule stated as "`launch` non-null: spawn ... `launch` null: swarm worker" |
| CLAR-2 | MET | Concrete mapping tables (severity, category to panel category); exact `review merge` command; slot to rotation table |
| CLAR-3 | MET | Clear section purposes |
| CLAR-4 | MET | Conventions paragraph defines `<sr1>`, PROPOSED, UNVERIFIED; `reflect-finding/1` defined where introduced |
| CLAR-5 | MET | Stage entry and exit; first measurement thresholds and decision rules |
| RISK-1 | NOT MET | Searched Risks 1-10 for probability or likelihood wording. Impact is described, but no probability is stated |
| RISK-2 | MET | Each of the 10 risks has "Mitigation:" |
| RISK-3 | MET | Risk 2 "loud fallback when none is valid"; Rollback column "flag off" |
| RISK-4 | MET | Risk 6 "`launch` is `{}` for gateway models"; Risk 7 forbidden Fable in tier data |
| RISK-5 | MET | Stage 2 exit "block compliance at least 95%"; "manual spot-check of 10 runs"; telemetry fields |
| INVR-1 | MET | "Count only valid-block reviewers toward the N=2 floor"; empty `refs` falls back to span overlap; exclusion emptying tier1b |
| INVR-2 | MET | Ledger rows drop extra fields, so "reflect joins its sidecar through the ledger's member records"; calibrator run before the debate |
| INVR-3 | MET | "`resolve_slot` for a `fixed` slot returns `candidates[0]` and ignores `exclude`"; `or candidates` fallback collides silently |
| INVR-4 | MET | "count only valid-block reviewers toward the N=2 floor"; a headless `citations_dropped: 0` constant |
| INVR-5 | MET | Slot order: the calibrator resolves first, so reviewers exclude its model under `distinct_across_slots`; blind calibration leakage via cluster labels |

Subtotals V2: COMP 5/5, CORR 3/5, STRU 5/5, CLAR 5/5, RISK 4/5, INVR 5/5. **Total 27/30.**

## Variant 3 (haiku backend)

| Criterion | Verdict | Evidence |
|---|---|---|
| COMP-1 | MET | Headings "Answers to Q1-Q7" (Q1-Q7), "Finding format", "Adapter sketches", "Staged migration", "Return-contract 1.8.0 mapping", "Cost model", "First measurement" |
| COMP-2 | MET | Compatibility tests: "T1 stop, two-of-three completion, no survivors, wrong schema, empty valid findings, truncated findings, unknown executor, exhausted disjoint pool" |
| COMP-3 | MET | Stage table entry criteria; "Operational execution contract" prerequisites (manifest, hashes) |
| COMP-4 | MET | "Pass for wider opt-in: shared recall is within five percentage points of legacy" |
| COMP-5 | MET | Risk 9: "No new scheduler, daemon, database, remote service or automatic revision engine"; post default "a separate decision" |
| CORR-1 | MET | Spot-checks hold: panel.py fixed/fallback; ensemble.py:808-819 constants; merge_cmd.py report written before ledger.save; 1.25x midpoint = 65.6k; CRLF at runner.py:163; reflect-reviewer advisory channel |
| CORR-2 | MET | Atomic same-directory publish and hash-keyed idempotency are feasible; multi-input merge honestly marked PROPOSED |
| CORR-3 | MET | "Three namespaces, not interchangeable" (tier, T2 level, T2Model slot) kept apart; the finalizer is called adversarial throughout |
| CORR-4 | MET | Contract unchanged, and the real debate is retained throughout. The 37k-53k vs 37k-56k difference is explained as "target versus allowance" |
| CORR-5 | MET | Cost arithmetic shown: "7.5 / 54 ≈ 14%"; "48 × (46.5k + 54k) = 4.824 million" |
| STRU-1 | MET | Same logical order as the brief |
| STRU-2 | MET | Consistent `##` and `###` depth |
| STRU-3 | MET | Format, adapters, migration, contract, cost, risk and measurement are separate sections |
| STRU-4 | MET | Candidate table, stage table, contract mapping table, Summary |
| STRU-5 | MET | Standard design-spec shape |
| CLAR-1 | NOT MET | Searched adapter and Q sections for exact commands and values. Language is abstract and ambiguous, e.g. "conservative clustering", "Share mechanics first", "honest result under failure" |
| CLAR-2 | NOT MET | Searched for concrete commands and templates. There is a YAML finding sample, but the 3-slot template is described only in prose ("one Tier 1b-capability anchor and two eligible independent slots") and there is no merge command line |
| CLAR-3 | MET | Section purposes are clear |
| CLAR-4 | MET | Header states PROPOSED; the "three namespaces" are defined; "channel" and "snapshot" are explained where used |
| CLAR-5 | MET | Stage entry, exit and rollback; "inconclusive, not a quality pass" decision rule |
| RISK-1 | NOT MET | Searched Risks 1-9 for probability. Impact is described, but no probability is stated |
| RISK-2 | MET | Each risk has an inline mitigation, e.g. "Pin snapshots; validate final current-source identity" |
| RISK-3 | MET | Manifest states "resolved → ... → published"; "Resume by hashes; retries cannot add votes" |
| RISK-4 | MET | "alias drift", "validator failure", "missing adversarial artifacts"; gateway availability UNVERIFIED |
| RISK-5 | MET | "Capture input, output, cached input ... retries and elapsed time separately for each actual class and stage" |
| INVR-1 | MET | "valid empty findings set" vs transport failure; "no survivors"; "two-of-three completion" |
| INVR-2 | MET | Manifest idempotency identity `(run_id, snapshot_hash, policy_hash, stage, reviewer_id, attempt_id)`; report written before ledger is not transactional |
| INVR-3 | MET | "Random and round-robin selection fall back to the full candidate list when exclusions exhaust it. Fixed selection takes the first candidate" |
| INVR-4 | MET | "Only `complete` plus valid schema is eligible to count toward review quorum"; "never adds another vote"; counts per adjudicated issue, not per reviewer |
| INVR-5 | MET | Ledger `resolved_check` auto-clearing is inappropriate for advisory audit; ledger must not turn a no-spec warning into Regression |

Subtotals V3: COMP 5/5, CORR 5/5, STRU 5/5, CLAR 3/5, RISK 4/5, INVR 5/5. **Total 27/30.**

## Edge-case floor (INVR subtotal, floor is at least 1 of 5)

V1 INVR 5/5 PASS; V2 INVR 5/5 PASS; V3 INVR 5/5 PASS.

## Totals

V1 29/30, V2 27/30, V3 27/30.
