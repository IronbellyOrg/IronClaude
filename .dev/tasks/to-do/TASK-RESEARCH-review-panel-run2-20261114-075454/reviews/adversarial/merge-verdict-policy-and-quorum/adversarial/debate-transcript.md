# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel advocate statements, Round 2 sequential rebuttals A then B) plus Round 2.5 invariant probe (independent fault-finder)
- Convergence achieved: see "Convergence Assessment" at the end of this file
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (Variant 1 = Proposal A advocate, Variant 2 = Proposal B advocate; both general-purpose agents on the default model, persona default)
- Mode: A (--compare); variants are `variant-1-original.md` (Proposal A) and `variant-2-original.md` (Proposal B)
- Verbatim statements: the advocate files below were written by the advocates themselves; the orchestrator only concatenated them. Source files: `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`.
- Omission check (shared assumptions A-001..A-005): both advocates answered all five in Round 1 (ACCEPT/REJECT/QUALIFY); no `[OMISSION]` flags.
- Heading levels inside the embedded statements are demoted by one level (their `##` become `####`) so they nest under the round headings.

## Round 1: Advocate Statements

### Variant 1 Advocate (Proposal A; default model)

Status: Complete
Advocate: Variant 1 (Proposal A: deterministic any-blocking union default, pluggable policy, quorum over recorded completion states, DEGRADED-style outcome for a partial panel, no calibrator in the default)
Repo: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`, branch `ironbelly/shadow-runs`
Code citations below were read in this session unless marked [NOT RE-READ] (taken from a research file).

#### Position

The shared core should default to a pure, deterministic outcome function over ledger rows, recorded completion states and a named policy, with the any-blocking union as the default policy and the reflect calibrate/validate/debate chain hosted as a named module policy. That default is the only one whose every state, transition and exit code can be specified and tested today without a model call, and it keeps B's adjudication available as a registered policy to be measured against it. A's real gaps are the undefined DEGRADED transition and the source of `requested` (see Concessions); B's gaps are larger and sit in the default path (pending rows have no place in the verdict, the served-model quorum does not exist in the transport).

#### Steelman of Variant 2

The strongest version of B is this. The ledger's verdict is `FAIL` if and only if some row is reviewer-typed `blocking` and `open` or `regressed` (`ledger.py:99-104`, `:273-275`). The only support signal the ledger computes, `confidence` (`overlap` or `single`), is "rendered and never read" (`ledger.py:86-90` against `:93-104`). A whole kernel built for the empty policy slot already exists and is dormant: `cluster_v2` computes `support`, `disputed`, `blocking_any`, `cluster_agreement` (`cluster.py:345-378`, `:403-419`), and only `cluster.py` and `cluster_cmd.py` use them (I confirmed by grep over `src/superclaude`). The shipped reflect verdict is not a union: it degrades on a missing evidence validator, an unavailable adversarial merge, single-reviewer fallback, null convergence, and convergence below 0.80 (`contract.py:274-326`), and 36 tests pin that. The E2 data shows 1.83 to 3.50 wrong blockers per run (research/08, as cited by both papers [NOT RE-READ]), so an unfiltered union will cry wolf. B also gets three structural points right. (1) Agreement is weak proof, so B never gates on a vote and uses code-checkable evidence instead. (2) Nothing is dropped: a contested blocker stays open and counted and cannot pass, which is the same fail-closed stance as A. (3) Its own endangered-invariants table names the real new risk, an adjudicator that wrongly rejects a true blocker, and states falsifiers (a) to (d) in advance, including an adjudicator served by a reviewer's own model. Finally, B correctly says that counting dispatched or complete reviewers overstates independence when requested and served model ids diverge (research/07 A3 [NOT RE-READ]); a quorum that cannot see that is weaker than it looks.

What B genuinely gets right and A should absorb: the evidence gate and `support` as ordering and display signals, a recorded adjudicator model id, and the falsifier list. None of that requires adjudication to be the default.

#### Strengths claimed (with evidence)

1. **The whole outcome is a pure function of three recorded inputs, so it is exhaustively testable with no model call.** Today `_brief_ids` and `_decision` are already pure over rows (`ledger.py:93-104`) and `merge_round` computes the verdict as `"FAIL" if brief else "PASS"` (`:273-275`). A adds only a quorum predicate over `COMPLETION_STATES` (`findings_v2.py:40`), whose per-reviewer counts the manifest already keeps (`manifest.py:269-274`, `_recount`) and `cluster_v2` already returns (`complete_reviewers`, `invalid_reviewers`, `valid_blocks`, `cluster.py:414-418`). A's quorum matrix (N in 1..5 by five states) and its monotonic fail-closed property test need only stubs of reviewer records.
2. **A closes the reproduced defect at every panel size, not only at zero valid blocks.** The only refusal is `if not any(block_ok.values())` (`ledger.py:150-157`); one valid block of four then yields PASS (`:273-275`) and is pinned by `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`tests/review/test_review_ledger.py:376-385`, which I read: it asserts `L1` resolved with one valid and one broken reviewer). The repo already treats "a review that did not happen never certifies PASS" as the rule (comment at `ledger.py:150-153`); A extends it from 0 to the declared floor.
3. **A touches none of the reflect pins.** `derive_verdict`, the 19 fields and the 36 `def test_` in `tests/cli/reflect/test_verdict_mapping.py` (counted: 36) are untouched, because reflect keeps its chain as the `legacy-adversarial` policy. `test_fx7_reviewer_shortfall_token_does_not_over_degrade` (`test_verdict_mapping.py:572-591`) and `test_i3_partial_two_of_three_distinct_pass_eligible` (`test_ensemble_stub_integration.py:199-221`) stay green by construction.
4. **The exit-code design avoids a verified collision.** `EXIT_BY_DECISION = {"PASS": 0, "REVISE": 10, "ESCALATE": 11}` (`ledger_cmd.py:13`) and reflect's `HALTED=10, DEGRADED=11, BLOCKED=2` (`models.py:34-48`) use 10 and 11 for different meanings. A adds DEGRADED as a new code instead of reusing 11, so a script that reads both products cannot conflate ESCALATE and DEGRADED, and the 10/0/11 pins (`test_review_cli.py:245, 349, 369`) hold.
5. **The union already ships and its cost side is priced by the repo's own rule.** A wrong blocker costs at most a fix cycle and, at the cap, a human decision (rule S3, cap 2 fix cycles; `ledger.py:475-484` renders the escalation text "do not start another fix cycle"). A missed real blocker is a PASS on a defective document. The union puts the error on the side the rules already treat as cheaper.
6. **B's three best ideas are hostable inside A, so adopting A forecloses nothing.** The policy is a named, swappable value; `adjudicated`, `agree-k` and `calibrated` are added policies and change no core signature. B's own plan (section 5) says the policy should be "the thing measured" with the union as baseline arm; A ships exactly that baseline and the registry.
7. **A's claims about what the code does not do are mostly correct and cheap to check.** `merge_round` never reads the manifest (grep of `ledger.py` for `manifest|reviewers_complete`: 0 matches), `ledger.load` checks only the schema string (`:47-48`), and the `shortfall` clash with FR-RH2.9 is real (`ensemble.py:755-770`).

#### Weaknesses identified in Variant 2 (with evidence)

**W1. A `pending` blocker has no place in the fix loop as the code is built (correctness, risk).** B's section 2.1 item 3 says only `confirmed` blockers drive FAIL/REVISE and the Reviser brief, while `pending` and `uncalibrated` blockers "stay open, count in the headline, and block PASS". Trace that through the code:
- `_brief_ids` selects rows by `blocking` and status `open`/`regressed` (`ledger.py:99-104`); a pending row is excluded from the brief by B's own rule.
- `merge_round` knows only two verdicts: `"FAIL" if brief else "PASS"` (`ledger.py:274`). A round with zero confirmed and one pending blocker has an empty brief, so it computes PASS. B needs a third verdict value, which is exactly a new outcome that B says needs no change to the 0/10/11 contract (B section 4, "keep their exit contract (0, 10, 11)").
- `ledger verdict` can only emit PASS (0), REVISE (10), ESCALATE (11) (`ledger_cmd.py:13`). A pending-only round maps to none of them honestly: not 0 (blocked), not 10 (REVISE tells the Reviser to fix, with an empty brief), and 11 only fires at the cap (`_decision`, `ledger.py:93-96`, `n < cap_reviews`).
- If it is forced onto REVISE, the loop burns cycles: the Reviser gets "Blocking finding ids: none." (`ledger.py:488-492`), changes nothing, and the next review re-finds the same row, until the cap. At the cap the escalation text prints `open blocking findings: .` with an empty list (`ledger.py:482-483`, `', '.join(brief)` over `[]`), so the human is told to look at findings that are not named.
- The pending row is also invisible to the next reader: the merged report's "Other findings" section lists only rows with `not r["blocking"]` (`ledger.py:468`), and the brief section lists only `brief` ids (`:442-466`). So neither the Reviser nor the next reviewer is shown the pending blocker.
This is the concrete answer to "what happens in the fix loop with a pending row": today's code has no state for it, and B specifies none (A-003).

**W2. `defer` can flip a round to PASS while pending blockers remain (fail-open).** `defer` removes the id from `brief_ids` and, when the brief empties, writes `verdict, decision = "PASS", "PASS"` (`ledger.py:356-360`). Under B, deferring the last confirmed blocker would stamp PASS with pending blockers still open, violating B's own "an unadjudicated blocker blocks PASS". B lists `defer` that cannot rewrite a verdict as common ground (I-4) but does not say how that survives a verdict that is no longer a function of the brief alone. A has the same `defer` hazard only if the DEGRADED state were stored; A derives on read and never stores it, which is why derive-on-read is load-bearing for A and must stay.

**W3. The "served model ids" quorum that B cites as existing does not exist (correctness; X-003, A-005).** B's E11 says the Tier-2 gate "computed from served model ids already exists" with [CODE-VERIFIED]. The code says otherwise. `evaluate_quorum` calls `compute_model_class_diversity(successes)` and `compute_vendor_diversity(successes)` (`fallback.py:161-179`), which read `worker.model_id` (`_diversity.py:10-15, 28-36`). The only production transport sets that field to the configured model: `model_id=self._model` (`openai_compat.py:468`), and `self._model` is what the request body sends as `"model"` (`:385`). So the existing gate counts requested ids; it cannot see a haiku slot served by another model, which is the very A3 failure B uses in E16 against the calibrator. A `model_observed` on the swarm path does not exist: the only hit for `model_observed` under `src/superclaude` is a column in a telemetry SQL query (`review/telemetry.py:364, 378`). B's quorum is therefore either the requested-id count it criticises, or blocked on a transport change (slot C-08). Either way the "at least 2 distinct served ids" predicate cannot be a default verdict precondition today. `test_i4_partial_two_of_three_duplicate_class_degrades` (`test_ensemble_stub_integration.py:224-234`) confirms the existing gate runs on stub model ids.

**W4. Most of B's strongest evidence (E7 to E10) is an argument for keeping the reflect chain, which A already does.** E7 (reflect DEGRADE triggers, `contract.py:274-326`), E9 (skill text) and E10 (four consumer-read contract names) show that the reflect module's verdict is not a union. A agrees and hosts that chain as `legacy-adversarial`, authoritative in reflect. None of E7 to E10 says the spec-review ledger, the future PR module or the rf-qa replacement should run an LLM adjudication stage by default. The evidence that does bear on the ledger (E1 to E3, E12 to E15) shows the union's cost and the missing measurement, not that adjudication beats it (E14 and E17: no policy compared, real-blocking recall at most 3 of 8).

**W5. The adjudication stage is not code, so the default path becomes non-deterministic and non-unit-testable.** `superclaude review merge` is a deterministic command: it parses reports, clusters, computes and stores the verdict in one call (`merge_cmd.py:71-118`, `ledger.py:273-285`). B's default needs a two-phase flow (merge, then an LLM validator and debate on contested rows, then derive) and a validator call per round. Its section 5 admits that E2 contains no calibrator, validator or debate output, so the offline replay "measures only how many blocking rows would be contested, not how they would be adjudicated". Its test plan item 2 needs a seeded-defect run that was designed and never run. A's tests exist before any experiment; B's default cannot be shown right or wrong by a code test, only by a model run.

**W6. Contested is the norm, so the validator becomes the verdict.** B's E15 (13 of 216 clusters had two or more reviewers) means almost every blocking row is single-reviewer and therefore "contested" under B's own rule. B's objection section concedes the validator "becomes the de facto verdict-maker, at added cost and with its own fail-open surface" and then answers by saying blocking rows are only "a handful per run". Those two statements together mean one validator call carries the verdict of every run. B marks the resulting fail-open path HIGH in its own table and offers only a restriction ("rejected only for deterministic evidence failure or a quoted re-read") that is a policy statement, not a mechanism the ledger enforces today.

**W7. B changes a shipped behavior while claiming shadow-only discipline (X-006).** Section 4 Preserved says "No verdict changes until a stage that promotes the engine"; Section 2.2 and the Endangered table make `adjudicated` the default for first reviews in the spec loop, which B itself calls "a behaviour change for an existing consumer, not shadow work". A's change in that loop is narrower and fail-closed: it affects only rounds below the declared quorum.

**W8. B treats "DEGRADED for a partial panel" as decided while the code says the opposite for reflect (X-002, A-004).** B section 2.3 assumes it "decided by reproduced evidence". The code comment at `ensemble.py:762-764` records verdict-degrade-on-shortfall as a deferred `needs_human_decision` that "would reverse FR-RH2.9 non-additively", and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` pins PASS with `reviewers_verified is False` (`test_verdict_mapping.py:572-591`). The partial-panel DEGRADED is decided only for the ledger path (D-2 reproduction), not for reflect. This does not hurt B's position much (B's quorum floor is also 2, see Concessions) but B asserts a settledness the code does not support.

**W9. Test-coverage lens, summary.** For A: a quorum matrix and a monotonic property test, with the D-2 reproduction flipping PASS to DEGRADED. For B: stubs for the validator, a per-row `adjudication` enum that must be kept consistent with `status`, `_brief_ids`, `defer`, `apply_revision` (which only advances rows with status `open`/`regressed`, `ledger.py:328-329`) and the merged-report renderer, plus a served-model check that no transport can answer today. B's surface of interacting pieces in the existing ledger (five functions listed above) is larger and none of them has a pending-row test.

#### Concessions

**K1. The union's cost is real and A has no mitigation except the cap.** E12 and E13 (1.83 to 3.50 wrong blockers per run; 65 judge-blocking versus 38 real, both [NOT RE-READ], taken from research/08) say a single reviewer's mistaken `blocking` flag fails a round. A's only defense is the S3 cap and the asymmetric-cost argument. Neither paper has measured this; A's "least-unmeasured default" is a rhetorical claim, and A should say the default rests on fail-closed asymmetry, not on data.

**K2. A's DEGRADED transition is undefined (A-003) and a naive version burns a cycle and clears rows.** `merge_round` records the round, advances `n`, and moves any `resolved_check` row not re-found in this round to `resolved` (`ledger.py:254-258`) before any outcome is derived. With one valid block of four, a row can be cleared by a reviewer set that mostly failed. If DEGRADED is only an outcome derived on read, the rows are already cleared and the next round counts against the cap (`_decision`, `ledger.py:93-96`). A needs one of: (a) refuse the merge below `min_complete` in a `degrade` profile, recording nothing, which extends the existing precedent at `ledger.py:150-157` and keeps the cap intact; or (b) couple quorum to the clearing rule (slot C-02). Option (a) is the smaller change and I recommend it for A. This also shows the DEGRADED exit code is needed only for the derive-on-read path, which makes a decision between (a) and a stored-outcome design a real open point.

**K3. `requested` has no source in today's merge command.** `superclaude review merge` takes only `--report REVIEWER_ID=PATH`, an optional `--resolution` and a cap (`merge_cmd.py:43-70`); `merge_round` receives only reviewers that produced a report. A reviewer that never produced a file is not in the list, so `complete < requested` cannot be computed without a new input. The optional `--resolution` JSON already lists the panel's reviewers (`merge_cmd.py:74-83`) and the manifest has `reviewers_requested` and `reviewers_resolved` (`manifest.py:143-145, 308-316`); A must say which one becomes mandatory. Also `parse_block` yields only `complete`, `truncated` and `invalid`; `failed` and `timed_out` "are for callers" (`findings_v2.py:39-40`), so the caller must supply them.

**K4. With a floor of 2, A's reflect `shortfall: visible` carve-out is mostly moot, and A's X-002 "CODE-CONTRADICTED" claim is narrower than A wrote.** A takes as its floor "at least 2 complete reviewers when 2 or more were requested". Under that floor, a 2-of-3 reflect run meets quorum and PASS-eligible behavior survives with `shortfall: degrade` too; `test_i3` and the FX7 witness do not conflict. The carve-out matters only if the floor is proportional or more than 2 (majority of 4 or 5, or all). A section 2.2 and 4.1 should say so. This also reduces X-005 (A's internal tension) to a statement about an unmeasured parameter and not a design contradiction.

**K5. A overstates "a PASS on that path rests on defaults" (X-004).** Engine A does default `merge_method` by reviewer count (`ensemble.py:773`) and zero deviation counts (`:779-785`). But `_degraded_reason` also requires a non-null adversarial convergence score (`contract.py:299-300`), a score of at least 0.80 (`:317-326`), no adversarial `partial`/`failed` status (`:306-307`) and diversity gates (`:282-288`). So reflect's PASS is not only defaults; B's E7 is correct on that narrow point. What remains true is that convergence measures agreement of the adversarial merge, not correctness (unmeasured), and that the zero-deviation default makes a seam-less run PASS-eligible.

**K6. A's new DEGRADED exit code needs consumer handling it does not specify.** `verdict_cmd` does `EXIT_BY_DECISION[v["decision"]]` (`ledger_cmd.py:109`), which raises `KeyError` for any stored decision not in the dict, so adding a decision value is not additive-safe for readers (this qualifies A's "additive keys break nothing" claim, A-002). Also `merge` itself exits 0 whatever the verdict (`test_review_cli.py:368`), so DEGRADED would reach the coordinator through the JSON `decision` field and `ledger verdict`. I did not find a coordinator document in `src/superclaude/commands` that parses `decision` (grep returned no match), so how the loop treats an unknown value is UNVERIFIED.

**K7. Neither paper measures a policy.** A's falsifier (section 5 item 5) and B's conditions (a) to (d) are both post-hoc; every external result is on QA, NLI or SQL, not finding sets (both papers). I claim A is cheaper to be wrong about, not that it is right.

**K8. Minor citation slips in A.** `test_review_cli.py:349` is the `ledger verdict` exit-0 line and the merge PASS assert is on `:348` (the claim holds). A's `[CODE-VERIFIED]` for the one-valid-PASS reproduction was by reading, not re-running (A says so; I also did not re-run it).

#### Shared assumption responses (A-001..A-005)

- **A-001: QUALIFY.** A `complete` state means the findings block parsed, not that the reviewer examined the document: `merge_round` sets `block_ok` from `parsed["ok"]` (`ledger.py:128-130`) and the manifest counts `completion == "complete"` (`manifest.py:274`). Counting these measures coverage of the format and guards against absence, which is what D-2 needs, but it cannot detect a shallow reviewer; both quorums share that limit, and a seeded-defect control (slot X-14) is the only real check.
- **A-002: QUALIFY.** Additive round and row keys are safe for `ledger.load`, which checks only the schema string (`ledger.py:47-48`), and `render_merged_report` and `capture` read named keys. But an additive decision value is not safe: `EXIT_BY_DECISION[v["decision"]]` raises `KeyError` on an unknown value (`ledger_cmd.py:109`), so A's DEGRADED and any B third verdict need the table and every consumer updated. E2 tools and variant ledgers are not enumerated by either paper (UNVERIFIED).
- **A-003: REJECT as stated.** The assumption that DEGRADED and `pending` have a defined fix-loop transition is false for both papers as written. B's `pending` row has no verdict, exit code or brief slot (W1, W2). A's DEGRADED needs the refuse-and-do-not-record rule or a coupling to clearing (K2). It is the highest-value item to specify in Round 2.
- **A-004: ACCEPT.** The 2-of-3 PASS-eligible shortfall is documented as deliberate FR-RH2.9 design at `ensemble.py:755-770` and pinned by `test_i3` (`test_ensemble_stub_integration.py:199-221`) and the FX7 witness (`test_verdict_mapping.py:572-591`), with the change deferred as a human decision. Accept it as today's intent for reflect, not as a permanent property; and note (K4) that a floor of 2 makes it compatible with A's `degrade` mode anyway.
- **A-005: REJECT.** A served model id is not obtainable on the shipped path: `openai_compat.py:468` sets `model_id` to the configured model and `:385` sends the same value, `_diversity.py:10-15` reads it, and the only `model_observed` in `src/superclaude` is a telemetry SQL column (`review/telemetry.py:364`). Stub transports set ids by config (`ensemble.py:172, 230`). Headless or stub lanes cannot provide it either. This is a prerequisite, not an assumption.

#### Per-point verdicts

| Point | Superior approach (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence |
|---|---|---|---|
| S-001 | Neither | 90 | Both use the same seven H2 sections in the same order, so there is no structural difference to rank. |
| S-002 | B | 55 | B's Claim/Source/Tag tables make each citation individually checkable, though A's inline tags are equivalent in content. |
| S-003 | Hybrid | 55 | A's exit-code subsection (`ledger_cmd.py:13` versus `models.py:34-48`) and B's explicit common-ground subsection (2.3) are each useful and neither replaces the other. |
| C-001 | A | 66 | No run compares any policy (B's own E17), the union ships, and B's default changes a shipped spec-loop verdict (B's own INV-L MEDIUM). |
| C-002 | A | 60 | A hosts the chain as a module policy and avoids a core-owned LLM stage in a deterministic command (`merge_cmd.py:71-118`), at the cost of B's reuse across modules. |
| C-003 | Hybrid | 62 | Quorum over recorded completion states is implementable now (`manifest.py:274`); served-id and vendor predicates are valuable but need a transport that reports served models (`openai_compat.py:468`). |
| C-004 | A | 62 | A states a concrete `shortfall` mode and floor and ties them to the pins, though K4 shows the reflect carve-out is mostly moot at floor 2 and B's floor of 2 gives the same answer there. |
| C-005 | A | 72 | `pending` has no verdict, exit code or brief slot in the ledger (`ledger.py:99-104, 273-275, 468, 488-492`) and `defer` can stamp PASS over it (`:356-360`). |
| C-006 | A | 70 | A names the function, the outcome set and an additive exit code; B claims 0/10/11 unchanged while adding an outcome that maps to none of them, though A's decision-value change needs consumer updates (K6). |
| C-007 | A | 55 | Both leave `derive_verdict` and the 36 tests alone; A's shadow-beside-legacy stance matches INV-L, while B's core-populated contract fields (U-010) are a real but separable gain. |
| C-008 | A | 65 | A changes the spec loop only below quorum; B makes `adjudicated` the default for first reviews, which B itself flags as a shipped behavior change. |
| C-009 | Hybrid | 58 | The code-backed evidence gate is shared (A keeps it in the pipeline, A section 7), and B's gate-before-`verify` placement is sensible; what is B-only is validator rejection beyond that, which is unmeasured. |
| C-010 | Hybrid | 55 | A's single-reviewer re-review quorum rule is concrete (`panel.py:189-196, 600` and `apply_to: ["first"]`), B's `support`/`disputed` inputs for a confidence gate are real (`cluster.py:345-378`) and A also displays them. |
| C-011 | A | 60 | A's quorum matrix and monotonic property test run with no model, while B's default needs a validator stage and an unrun seeded-defect design; B's falsifiers (a) to (d) are worth adopting. |
| C-012 | B | 58 | A separate `calibration_map` channel exists (`cluster.py:12`, `findings_v2.py:96-97`) and recording the adjudicator's model id exposes silent collapse, though it need not gate the default. |
| X-001 | A | 66 | Same evidence as C-001: both papers concede no measurement favors adjudication, and the union is the only policy whose behavior is fully specified today. |
| X-002 | A | 70 | The code treats verdict-degrade-on-shortfall as a deferred human decision (`ensemble.py:762-764`) pinned by two tests, so B's "decided" overstates; A's own reading is narrower than written (K4). |
| X-003 | A | 85 | `fallback.py:161-179` reads `worker.model_id`, which `openai_compat.py:468` sets to the requested model, so B's E11 "computed from served model ids" is wrong for the shipped path. |
| X-004 | Hybrid | 60 | A is right that engine A defaults `merge_method` and zero deviation counts (`ensemble.py:773, 779-785`) and B is right that PASS also needs convergence of at least 0.80 and healthy sub-status (`contract.py:299-326`). |
| X-005 | A | 58 | A's tension (floor 2 versus `visible`) is resolvable by profile data and stated openly, whereas B's X-006 can only be resolved by waiving shadow-only. |
| X-006 | A | 65 | B's own Endangered table says making `adjudicated` the spec-loop default "is not shadow work", contradicting its Preserved row for INV-L. |

#### Code verification log

| # | Citation (source: where) | What I saw | Held? |
|---|---|---|---|
| 1 | A/B: `ledger.py:99-104` | `_brief_ids` = rows with `blocking` and status `open` or `regressed`. | Yes |
| 2 | A/B: `ledger.py:86-90, 93-104` | `_confidence` computes `overlap`/`single`; `_decision` and `_brief_ids` never read it. | Yes |
| 3 | A/B: `ledger.py:150-157` | Only refusal: `not any(block_ok.values())` raises `LedgerError`, nothing recorded. | Yes |
| 4 | A/B: `ledger.py:273-275` | `verdict = "FAIL" if brief else "PASS"`; `_decision` at `:93-96` is PASS, REVISE (n < cap) or ESCALATE. | Yes |
| 5 | A: `ledger.py:47-48` | `load` checks only `obj.get("schema") != SCHEMA`. | Yes |
| 6 | A: `ledger.py:363-372` | `verdict()` returns the stored last round; `apply_revision` (`:301-347`) never rewrites round verdicts, so it is stale after `revise`. | Yes |
| 7 | A: `merge_round` never reads manifest | grep for `manifest\|reviewers_complete` in `ledger.py`: 0 matches. | Yes |
| 8 | New (mine): `ledger.py:254-258` | A `resolved_check` row not re-found in the round becomes `resolved` before the outcome is derived. | n/a (found by me; basis for K2) |
| 9 | New (mine): `ledger.py:356-360` | `defer` sets `PASS/PASS` when `brief_ids` empties. | n/a (basis for W2) |
| 10 | New (mine): `ledger.py:468, 482-483, 488-492` | "Other findings" lists only non-blocking rows; escalation joins `brief`; brief text "Blocking finding ids: none." | n/a (basis for W1) |
| 11 | A: `ledger_cmd.py:13`; `models.py:34-48` | `EXIT_BY_DECISION = {PASS:0, REVISE:10, ESCALATE:11}`; reflect `HALTED=10, DEGRADED=11, BLOCKED=2`. | Yes |
| 12 | New (mine): `ledger_cmd.py:109` | `sys.exit(EXIT_BY_DECISION[v["decision"]])` raises `KeyError` on an unknown decision. | n/a (basis for K6, A-002) |
| 13 | A: `ensemble.py:772-773, 755-770` | `tier_reached = 2 if reviewer_count >= 2`; `merge_method` single-reviewer fallback below 2; shortfall token is benign, verdict-degrade deferred (`:762-764`). | Yes |
| 14 | A: `contract.py:294-296` | Trigger 10, `single-reviewer-fallback`, returns a degraded reason. | Yes |
| 15 | B E7: `contract.py:31-33, 274-275, 291-300, 317-326` | Halt set = auggie, env-aliases, evidence-validator; adversarial-unavailable (`:291`), null convergence (`:299`), low convergence <0.80 (`:317-326`). | Yes |
| 16 | B E11: `fallback.py:75-82`; `contract.py:282-288` | `QuorumState` dataclass and diversity triggers exist. B's wording "computed from served model ids" | **No (wrong)**: `evaluate_quorum` (`fallback.py:161-179`) uses `worker.model_id` via `_diversity.py:10-15`, which `openai_compat.py:468` sets to the requested `self._model` (request body `"model": self._model` at `:385`). |
| 17 | B: `model_observed` is a decided requirement | Only `review/telemetry.py:364, 378` mention it (SQL column); no transport records it. | Not in code today (prerequisite) |
| 18 | A/B: `manifest.py:20-22, 269-274` | `_recount` counts latest `collected` attempt per reviewer with `completion == "complete"`. | Yes |
| 19 | A: `findings_v2.py:40`; comment `:39` | `COMPLETION_STATES` has five values; `parse_block` returns only three, `failed`/`timed_out` "are for callers". | Yes (the second part is new, basis for K3) |
| 20 | A: `cluster.py:345-377, 386, 403-419` | `disputed`, `blocking_any`, `blocking_all`; `complete_reviewers`, `valid_blocks`, `cluster_agreement` None below 2 complete. | Yes |
| 21 | B E5: only `cluster.py` and `cluster_cmd.py` use `disputed`/`cluster_agreement` | grep over `src/superclaude/*.py`: exactly those two files. | Yes |
| 22 | B: `cluster.py:12-13`; `findings_v2.py:96-97` | `calibration_map` docstring and `calibrated_confidence` rejected in a findings-v2 line. | Yes |
| 23 | A: `panel.py:189-196, 600` | `apply_to` must be a non-empty subset of `['first','re-review']`; selection at `:600`. The count of 8 packaged templates not re-checked. | Yes (count NOT RE-READ) |
| 24 | A: test pins `test_review_ledger.py:376-385`; `test_review_cli.py:245, 349, 369`; `test_ensemble_stub_integration.py:199-221`; `test_verdict_mapping.py:572-591` | All four tests exist at those lines with the asserts described (exit 11 on `:369`, exit 0 on `:349`, merge PASS assert on `:348`). | Yes (one off by one line, K8) |
| 25 | A/B: 36 tests in `test_verdict_mapping.py` | `^def test_` count: 36. | Yes |
| 26 | New (mine): `merge_cmd.py:43-83, 100-118` | Options: `--ledger --doc --round --report --resolution --out --cap`; no requested-count; merge exits 0 and prints JSON. | n/a (basis for K3) |
| 27 | A: claim that D-2 reproduces (1 valid of 4 gives PASS, exit 0) | Read the code path only (`ledger.py:150-157, 273-275`); did not run it. | Code path consistent; execution NOT RE-RUN |
| 28 | Research-sourced numbers (E12 to E15, 65 vs 38, 6 of 15 runs, 41.5%) | Not opened; taken from the papers' own citations. | UNVERIFIED here |

Claims in either paper I found wrong or overstated: B E11 ("served model ids", row 16: wrong); B section 2.3 ("DEGRADED for a partial panel decided", contradicted for reflect by `ensemble.py:762-764`); A section 3.1 item 4 ("a PASS on that path rests on defaults", overstated, K5); A section 2.2 "CODE-CONTRADICTED" for the slot sentence (true only above a floor of 2, K4).

Status: Complete

### Variant 2 Advocate (Proposal B; default model)

Advocate: advocate-B-r1. Mode A, standard depth, focus correctness, risk, test-coverage. Round 1 of 2.
Tags: [VERIFIED] = I read the cited lines in this session. [UNVERIFIED] = taken from a research file I did not open. I did not open the `research/` files; every claim about r03, r06, r07, r08, web-01 is [UNVERIFIED] by me.

#### Position

The core should own a verdict-policy slot, a code-only evidence gate and a per-row adjudication record, because today a round verdict depends on one reviewer-typed flag and the kernel's `support` and `disputed` fields sit unused. B's defensible claim is the slot, the gate, the record and the falsifiable test; making `adjudicated` the panel default before any measurement is a hypothesis, and B should say so. The honest end state is close to a hybrid: union stays the shipped default, B's gate and flags go into the core, and `adjudicated` is promoted only when the pre-committed replay beats the union.

#### Steelman of Variant 1

A's strongest case, stated at full strength:

1. The union is the only rule that assumes nothing about reviewer reliability, and it is the rule the repo's own cost model prices correctly. Repo rule S3 caps fix cycles at 2 (3 reviews) and then escalates with the open blockers; a missed real blocker is a PASS on a defective document, which INV-I forbids. A wrong blocker is bounded by the cap and ends in a human decision; a wrongly rejected blocker has no bound.
2. A puts no unmeasured component in the verdict path. The calibrator lost its class in 6 of 15 combo runs and reported `calibrator_diversity: full` while one model served everything (E16, [UNVERIFIED]); no run scored any policy (E17). Replacing one unmeasured filter with another adds calls and a failure mode with no evidence.
3. A's quorum is buildable now from data that exists: `COMPLETION_STATES` (`findings_v2.py:40`), `reviewers_requested/resolved/complete` and `_recount` (`manifest.py:20-22, 269-274`). `merge_round` today takes only `reviewers` dicts and refuses only at zero valid blocks (`ledger.py:107-157`), so the reproduced D-2 defect (1 valid empty block of 4 gives PASS) has a concrete fix with a concrete test: a quorum matrix over N=1..5 and all five states, plus a monotonic fail-closed property test.
4. A did the work B skipped: it found the reflect pins that bound where DEGRADED-on-shortfall may apply. `test_i3_partial_two_of_three_distinct_pass_eligible` and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` assert PASS for a 2-of-3 shortfall, and `ensemble.py:762-764` records degrade-on-shortfall as a deferred human decision. A's `shortfall: visible|degrade` profile respects that and keeps `derive_verdict` untouched.
5. A avoids the 10/11 exit-code collision between the ledger (`ledger_cmd.py:13`: PASS 0, REVISE 10, ESCALATE 11) and reflect (DEGRADED 11) by making DEGRADED an additive code, and it gives a pure function signature a developer can write today.
6. Every policy B wants (k-of-n, calibrated, adjudicated) is hostable by A's registry as a data change, so A loses no future option.

What A genuinely gets right and B does not: the exit-code and function-level specificity, the reflect-pin awareness, the decidable test plan, and the refusal to ship a default nobody measured.

#### Strengths claimed (with evidence)

1. **The shipped verdict is a function of one reviewer-typed bit.** `_brief_ids` returns rows where `r["blocking"]` and status is `open` or `regressed` (`ledger.py:99-104`); `verdict = "FAIL" if brief else "PASS"` (`ledger.py:273-275`); a new row is blocking if `any(m["blocking"] for m in group)` (`ledger.py:187`). Nothing else reaches the decision. [VERIFIED]
2. **The policy slot the kernel was built for is empty.** `cluster.py` computes `support` (`:337`), `disputed` (`:347-351`) and `cluster_agreement` (`:405-412`). Within `src/superclaude`, only `cluster.py`, `cluster_cmd.py` and skill/ref prose contain `disputed` or `cluster_agreement` (Grep); `ledger.py` uses none. The row-level `confidence` ("overlap" or "single", `ledger.py:86-90`) is rendered in the merged report table and brief (`ledger.py:429-435, 473`) but no verdict code reads it. Correction to the shorthand "rendered and never read": the Reviser LLM does read it; the verdict code does not. [VERIFIED]
3. **The production reflect verdict is not a union, so a shared core whose only default is a union has no verified production customer for it.** `derive_verdict` degrades on the validator in `_DEGRADED_COMPONENTS_HALT_SET` (`contract.py:31-33, 274-275`), single-reviewer fallback (`:294-296`), null convergence (`:298-300`) and convergence below 0.80 (`:317-326`). Convergence comes from the adversarial child (`ensemble.py:424-440`). A's own design therefore ends with reflect on `legacy-adversarial`, spec re-reviews on a one-reviewer `union`, and the "default" governing only new multi-reviewer first reviews and the PR module. That is exactly where B's evidence gate and support flag matter. [VERIFIED]
4. **Four consumer-read contract names need a producer.** `confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards`, `calibrator_diversity` are stable fields (`panel_lint.py:40, 100, 102, 110`), and `SKILL.md:999` lists the `sc-task` end-of-task hook rule `status: success AND confidence_calibrated >= 0.85`. A union core never produces them; today they come from skill prose (`SKILL.md:34, 631, 635`). [VERIFIED]
5. **A one-bit verdict makes one wrong blocker expensive, by code, not by assertion.** Trace: reviewer R2 types a wrong `blocking: true`; the row is `open` and enters the brief (`ledger.py:99-104`). If the Reviser answers `rejected`, `apply_revision` only appends `rejected_by_reviser` to history and leaves the status `open` (`ledger.py:340-342`). On the next round only `resolved_check` rows can clear (`ledger.py:254-258`), so an `open` row nobody re-finds stays `open` and keeps the verdict FAIL. The only exit is `defer`, a human command (`ledger.py:350-360`). So a correct Reviser rejection of a false blocker does not end the loop; the round runs to the cap and ESCALATEs. A says a wrong blocker costs "at most one fix cycle"; on this code it costs every remaining cycle unless clearing changes (slot C-02, which both proposals assume separate). [VERIFIED by reading; not executed]
6. **B's tests are policy-comparison tests, A's are quorum tests, and the repo needs both.** B's offline replay (section 5 item 1) scores `union` and a contested-row rule on committed E2 data with no model calls; the regression gate (36-test `test_verdict_mapping.py`, 42-contract replay) and the four failure conditions (a) to (d) are stated before any run. A's item 4 is similar but names no failure condition for the quorum floor that B's (c) does not also cover for the adjudicator.
7. **B names the fail-open risk of itself.** Endangered table: a buggy adjudicator that rejects a true blocker is a new fail-open path (INV-I HIGH), so `rejected` is restricted to deterministic evidence failure or a quoted re-read, and every rejection is recorded. A does not have an equivalent self-critique of its default; its section 4.2 lists only test-pin exposure.
8. **Future modules.** The PR flow ignores a panel verdict and consumes findings (s05:320 via r13 P12, [UNVERIFIED]); a union default sends every reviewer-typed blocking row into the push FSM's fix rounds, whose cap is pr-submit's. A deterministic gate before `verify` is the cheap part of B; A also keeps an evidence gate (A section 7, CO-22), so this strength is shared, and what B uniquely adds is the validator re-read and `pending` flag for contested rows.

#### Weaknesses identified in Variant 1 (with evidence)

1. **A's cost argument is weaker than stated.** See Strength 5: on the current ledger code a false blocker that the Reviser rightly rejects is not cleared by anyone but a human `defer`, so "at most one fix cycle" understates cost. A's asymmetry claim (wrong blocker is cheap, missed blocker is expensive) is right in direction but its unit cost is wrong until C-02 lands. [VERIFIED]
2. **A's "default" resolves FX-10 only by pricing it.** FX-10 is "a weak model must not decide alone". A keeps `support`, `disputed` and `confidence` as display fields (A 2.1), so a one-reviewer blocker with `support` below 0.5 and `disputed` true fails the round exactly as a unanimous one does. No signal that already exists in `cluster.py` changes any outcome. [VERIFIED for the code; the FX-10 reading is from the diff analysis]
3. **A's quorum counts completions with no independence check.** Three `complete` reviewers all served by one model satisfy `min_complete`. The existing Tier-2 gate has the same blind spot: `compute_model_class_diversity` counts distinct `worker.model_id` over succeeded workers (`_diversity.py:8-15`), and `openai_compat.py:467-468` stamps `model_id=self._model`, the configured id, not a served id. A defers diversity to telemetry; its quorum inherits the blind spot (see Concession C3: so does B until `model_observed` is wired). [VERIFIED]
4. **A's headline fail-closed claim is wider than its own profile.** Section 1 and 4.1 say fail-closed "at every panel size"; section 2.2 sets reflect to `shortfall: visible`, where a 2-of-3 shortfall is PASS-eligible. The claim holds only for `degrade` profiles (X-005). A is honest in 2.2, but the summary sentence overclaims. [VERIFIED against `ensemble.py:755-770`]
5. **A's "PASS rests on defaults" is only partly true.** `ensemble.py:446-465` takes regression, deviation and needs-human flags from `adversarial_result` when the seam ran and defaults to clean only when no seam ran (`:442-445`: pre-supplied score, fewer than two survivors, or child failure). A child failure leaves convergence `None`, which DEGRADES (`contract.py:298-300`). So on the default seam path the PASS depends on adversarial output, not on defaults. The defaults matter for the pre-supplied-score path and for `merge_method`, which is set by reviewer count (`ensemble.py:773`). A's X-004 point is right for that path and overstated for the main one. [VERIFIED]
6. **A's new DEGRADED exit code is asserted safe, not shown.** "An old caller fails closed on the new code" holds for any script that treats non-zero as failure; whether skills that branch on 10 versus 11 treat an unknown code as error or as ESCALATE was not checked in A. [UNVERIFIED]
7. **A leaves the stored-verdict problem to someone else and builds on it.** `ledger.verdict()` returns the stored `last["verdict"]` (`ledger.py:363-372`), and `defer` rewrites it to PASS when the brief empties (`ledger.py:356-360`), pinned at `test_review_ledger.py:396-405`. A's pure function would be derived on read, but `defer` and its pin are not in A's endangered list beyond the D-1 family. [VERIFIED]

#### Concessions

C1. **No measurement shows adjudication beating the union (E17).** B's own section 1 says so. `adjudicated` as the panel default is a hypothesis. I concede X-001 in the form: union stays the default until the Tier Q rule in B section 5 is met; B's evidence gate, `support`/`disputed` flags and adjudication record go into the core now, as additive data that changes no outcome.

C2. **`pending` has no loop transition, no exit code and one verified bypass.** B says `pending` blocks PASS but does not enter the Reviser brief (only `confirmed` rows do, B 2.1 item 3). The only brief is `_brief_ids` (`ledger.py:99-104`); `apply_revision` skips rows whose status is not `open` or `regressed` (`ledger.py:328-329`); `_decision` knows only PASS, REVISE and ESCALATE (`ledger.py:93-96`). So a round with only pending blockers has an empty brief and would run to the cap with nothing for the Reviser to do. Worse, `defer` of any other row empties `brief_ids` and rewrites the stored verdict to PASS (`ledger.py:356-360`, pinned at `test_review_ledger.py:396-405`), which would bypass a pending row held outside the brief. B's I-4 ("`defer` cannot rewrite a verdict") is a decided requirement, not shipped behaviour, and the pin asserts the opposite. This is the A-003 gap, and A shares its DEGRADED half.

C3. **B's E11 is mis-tagged.** B says a Tier-2 gate "computed from served model ids already exists". The gate is computed from `worker.model_id` (`_diversity.py:8-15`, `fallback.py:167-177`), which the OpenAI-compatible transport sets to `self._model` (`openai_compat.py:467-468`), the configured id. That contradicts B's own E16 (requested and served ids diverge) and A's UC row C-04 reading (X-003). `model_observed` exists on the verdict path nowhere; it is a column in the telemetry view (`telemetry.py:364`) and one skill sentence. The served-model quorum is a requirement for slot C-08, not an existing capability, and B's quorum must fall back to a completion count when it is absent. A's reading is correct on this fact.

C4. **"Reuse the legacy chain, callable from the core" overstates reuse.** The calibrator and evidence validator are agents dispatched by skill prose with inline fallbacks (`SKILL.md:631, 635`); the debate yields a convergence score and a report (`ensemble.py:424-440`). A per-row `confirmed | rejected | pending` enum is new design, not something the legacy chain already emits. I found no per-row verdict from the adversarial step in the code I read.

C5. **X-002 as B wrote it is contradicted for reflect.** B 2.3 lists "DEGRADED-style outcome for a partial panel" as common ground. For the reflect profile, two pins assert PASS for a 2-of-3 shortfall and `ensemble.py:762-764` records degrade-on-shortfall as an undecided human decision. B's own quorum (2 complete, 2 distinct ids) is consistent with the pins; the common-ground sentence is not. The sentence must be limited to modules that opt in.

C6. **The adjudicator is an LLM and a new fail-open surface; its error rate is unmeasured.** `evidence-validator` is read-only by tool list (`Read, Grep, Glob`, `agents/evidence-validator.md:5`), which meets INV-G, but a validator that wrongly rejects a true blocker is the same class of defect B accuses the union of. B's restriction of `rejected` to deterministic failure or a quoted re-read is a mitigation, not a proof.

C7. **B's wrong-blocker figures are upper bounds** (a true novel defect scores as wrong, E12 caveat), and B's own replay cannot score adjudication because E2 holds no validator or debate output (B section 5 item 1 limit).

C8. **Changing the spec loop default is a behaviour change, not shadow work** (X-006; B's own INV-L MEDIUM). A's D-2 fix also changes that loop, but A frames it as a fix of a reproduced defect.

#### Shared assumption responses (A-001..A-005)

- **A-001 (a `complete` reviewer has substantively examined the document): QUALIFY.** `complete` means a parsed valid block (`findings_v2.py:40`, `manifest.py:269-274`), which measures format success, not depth. D-2 shows one valid empty block certifies PASS. Quorum is necessary but not sufficient; both proposals rest on it, B adds evidence and support signals on blocking rows only and neither adds a check on an empty block.
- **A-002 (additive keys break no reader): QUALIFY.** `load` checks only the schema string (`ledger.py:47-48`), and a Grep of `src/superclaude` and `scripts/` found no other reader of `review-ledger/1` rows, so additive keys are syntactically safe in the code I could see. Tests, variant ledgers and E2 tools outside those paths were not enumerated. B's semantic changes (excluding pending rows from the brief) are not additive.
- **A-003 (DEGRADED and `pending` have defined fix-loop transitions): REJECT.** Neither exists today. `_decision` has three outcomes (`ledger.py:93-96`) and `apply_revision` acts only on `open` and `regressed` (`ledger.py:328-329`). Both proposals must specify cap accounting, re-dispatch and the exit code before adoption; see C2.
- **A-004 (2-of-3 PASS-eligible shortfall in reflect is intended): QUALIFY.** It is deliberate FR-RH2.9 design, pinned by two tests (`test_ensemble_stub_integration.py:199-221`, `test_verdict_mapping.py:572-591`), but `ensemble.py:762-764` also records the opposite choice as a pending human decision. Treat it as intended for now and not settled; B's common-ground sentence must exclude reflect.
- **A-005 (served model id obtainable for every reviewer and adjudicator in every transport): REJECT.** The only id on the verdict path is the configured one (`openai_compat.py:467-468`); `model_observed` is a telemetry column and a decided C-08 requirement. Any independence rule must degrade to a completion-only quorum when no served id is recorded.

#### Per-point verdicts

| Point | Superior approach (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence |
|---|---|---|---|
| S-001 | Neither | 90 | Both use the same seven-section skeleton in the same order. |
| S-002 | B | 55 | B's tagged claim/source tables are easier to audit, though B mis-tagged E11. |
| S-003 | A | 60 | A's 2.3 exit-code section fills a gap that B's 2.3 (a restatement of common ground) leaves open. |
| C-001 | Hybrid | 60 | Union stays the default (no policy is measured, E17); B's evidence gate, `support`/`disputed` flags and adjudication record go in as non-outcome data; `adjudicated` is a measured arm. |
| C-002 | A | 60 | The calibrate/validate/debate chain is skill-orchestrated agents (`SKILL.md:631, 635`), not a core-callable stage, and its calibrator is unmeasured; a module-owned policy is safer. |
| C-003 | Hybrid | 60 | A's completion-count quorum is buildable now (`manifest.py:20-22, 269-274`); B's distinct-served-id test needs `model_observed`, which is not on the verdict path (`openai_compat.py:467-468`). |
| C-004 | A | 70 | A found and verified the pins that bound DEGRADED-on-shortfall in reflect (`test_ensemble_stub_integration.py:199-221`, `test_verdict_mapping.py:572-591`); B's common-ground sentence is contradicted there. |
| C-005 | A | 60 | B's `pending` state has no brief entry, exit code or cap accounting and a `defer` bypass (`ledger.py:356-360`); A's rule is the existing tested one, with a B-style `contested` flag as a display add-on. |
| C-006 | A | 75 | A names a function signature and an additive exit code; B names neither and leaves the 0/10/11 contract silent on `pending`. |
| C-007 | Hybrid | 55 | Both leave `derive_verdict` untouched; B's four consumer-read fields have a real consumer (`SKILL.md:999`) but no producer, while A's shadow-union is the lower-risk first step. |
| C-008 | A | 55 | A's change is a fix of a reproduced defect with an additive profile; B's `adjudicated` default would change a shipped verdict (B's own INV-L MEDIUM); both alter the spec loop. |
| C-009 | Hybrid | 55 | A deterministic evidence gate before `verify` is shared (A keeps it per CO-22); only B's validator re-read for contested rows is unique and unmeasured. |
| C-010 | B | 55 | B exposes `support`, `disputed` and the adjudication record as inputs for a confidence gate and monotonicity check, which A's display-only fields do not feed; rf-qa's needs are unpinned either way. |
| C-011 | Hybrid | 65 | A's quorum matrix and monotonic property test are decidable now; B's pre-stated falsifiers (a) to (d) and served-model check belong on top of them. |
| C-012 | B | 55 | A separate calibration channel keyed by finding id (`cluster.py:12-13`, `findings_v2.py:96-97`) and an adjudicator-model record answer the E16 silent collapse, but only once a served id exists (A-005). |
| X-001 | Hybrid | 60 | Same as C-001; no verified evidence favours either default, and B's own section 5 makes the union the baseline arm. |
| X-002 | A | 75 | The reflect pins assert PASS for a 2-of-3 shortfall and `ensemble.py:762-764` leaves degrade undecided, so "decided common ground" fails for reflect. |
| X-003 | Neither | 80 | B's E16 (requested differs from served) is right and its E11 wording is wrong: the transport stamps the configured id (`openai_compat.py:467-468`); this is a B-internal contradiction A did not need to argue. |
| X-004 | Hybrid | 65 | Both are right on different paths: defaults apply on the pre-supplied-score and no-seam path (`ensemble.py:442-465`), while the default seam path takes deviation flags and convergence from the adversarial child and DEGRADES on null or low convergence (`contract.py:298-326`). |
| X-005 | B | 55 | B's quorum (2 complete, 2 distinct ids) agrees with the reflect pins; A's "every panel size" headline overstates against its own `shortfall: visible` profile. |
| X-006 | A | 55 | A keeps the reflect union in shadow beside the authoritative legacy chain, while B's default flip in the spec loop is its own admitted non-shadow change; A's D-2 fix also touches that loop. |

#### Code verification log

Citations checked in this session. HELD = the claim matches the code. I did not open any `research/` file; research-sourced numbers (E4, E8, E12-E17, G-series, web-01) are not verified here. I did not re-count the 36 tests in `test_verdict_mapping.py` or open `test_review_cli.py:349, 369`.

| Citation | What I saw | Result |
|---|---|---|
| `ledger.py:93-104` (B E1) | `_decision` maps PASS/else REVISE or ESCALATE by cap; `_brief_ids` returns rows with `blocking` and status `open`/`regressed`. | HELD |
| `ledger.py:86-90` (B E2) | `_confidence` returns `overlap`/`single`; `_decision` and `_brief_ids` do not read it. It is rendered at `ledger.py:429-435, 473`, so the Reviser sees it. | HELD for verdict code; "rendered and never read" needs the Reviser qualifier |
| `ledger.py:150-157` (B E3, A 3.1) | `raise LedgerError` only when `not any(block_ok.values())`. | HELD |
| `ledger.py:273-275` (A) | `verdict = "FAIL" if brief else "PASS"`; `_decision` follows. | HELD |
| `ledger.py:47-48` (A) | `load` checks only `obj.get("schema") != SCHEMA`. | HELD |
| `ledger.py:363-372` (A) | `verdict()` returns the stored last round verdict. | HELD |
| `ledger.py:340-342, 254-258, 350-360` (mine) | Reviser `rejected` leaves status `open`; only `resolved_check` rows clear; `defer` rewrites verdict to PASS when the brief empties. | HELD; basis for Strength 5 and C2 |
| `test_review_ledger.py:376-385` (B E3) | Round 2 with one valid and one broken reviewer; asserts `block_ok`, warnings and `L1` resolved. It does not assert a verdict string. | HELD for the name and behaviour; it pins "one valid block is enough" for clearing, not for a PASS verdict |
| `test_review_ledger.py:396-405` (mine) | `defer` test asserts verdict PASS and empty brief after deferral. | HELD; contradicts the decided I-4 premise |
| `cluster.py:35-52` (B E5/E6) | Docstring defines support, `disputed`, `cluster_agreement`, "A cluster is blocking when blocking_any is true." | HELD |
| `cluster.py:345-377, 403-412` (A) | `blocking_any`, `blocking_all`, `disputed` at `:375-377`; `cluster_agreement` None below 2 complete reviewers at `:405-406`. | HELD |
| `cluster.py:12-13` (B) | `calibration_map: {finding_id: finding_confidence}`. | HELD |
| `Grep disputed\|cluster_agreement` (B E5) | In `src/superclaude/cli/review`, only `cluster.py` and `cluster_cmd.py`; other hits are skill/ref prose. | HELD |
| `manifest.py:3-6, 39-49, 52` (B) | State machine frozen to published includes `calibrated`, `clustered`, `debated`, `validated`; `COMPLETIONS` tuple. | HELD |
| `manifest.py:20-22, 269-274` (A, B) | Counts documented; `_recount` counts latest collected-stage attempt per reviewer with completion `complete`. | HELD |
| `findings_v2.py:40` (A) | `COMPLETION_STATES = ("complete", "truncated", "invalid", "failed", "timed_out")`. | HELD |
| `findings_v2.py:96-97` (B) | Rejects a line carrying `calibrated_confidence`. | HELD |
| `contract.py:31-33, 274-275` (B E7) | `_DEGRADED_COMPONENTS_HALT_SET` includes `evidence-validator`; first trigger degrades on it. | HELD |
| `contract.py:282-300, 317-326` (B E7/E11) | Triggers 7-11b as described. | HELD |
| `contract.py:294-296` (A) | `single-reviewer-fallback` degrades. | HELD |
| `fallback.py:75-82` (B E11) | `QuorumState(reviewer_count, model_class_diversity, vendor_diversity, satisfies_tier2)`; computed at `:167-177` from successes. | HELD for existence |
| B E11 wording "computed from served model ids" | `_diversity.py:8-15` uses `worker.model_id`; `openai_compat.py:467-468` sets `model_id=self._model`, the configured id. | WRONG as worded (own claim); see C3 |
| `ensemble.py:772-773` (A) | `tier_reached = 2 if reviewer_count >= 2`; `merge_method` by count. | HELD |
| `ensemble.py:755-770` (A) | FR-RH2.9 comment; `reviewer-shortfall` token benign; 2-of-3 stays PASS-eligible; degrade deferred (`:762-764`). | HELD |
| `ensemble.py:779-785` (A) | Zero deviation counts when `deviation_count_by_class` is None. | HELD in `build_reflect_contract` |
| A 3.1 item 4 "a PASS on that path rests on defaults" | `ensemble.py:442-465`: defaults only when no seam ran, pre-supplied score, or child failed; otherwise values come from `adversarial_result`; null convergence degrades. | PARTLY WRONG in A (true for the pre-supplied-score path, overstated for the main seam path) |
| `ledger_cmd.py:13` (A) | `EXIT_BY_DECISION = {"PASS": 0, "REVISE": 10, "ESCALATE": 11}`. | HELD |
| `test_review_cli.py:245, 312` (A) | exit 10 with REVISE at `:245`; exit 0 with PASS at `:312`. Lines 349 and 369 not read. | PARTLY CHECKED |
| `test_ensemble_stub_integration.py:199-221` (A) | `test_i3_partial_two_of_three_distinct_pass_eligible` asserts Verdict.PASS, exit 0, `reviewer_count` 2. | HELD |
| `test_verdict_mapping.py:572-591` (A) | `test_fx7_reviewer_shortfall_token_does_not_over_degrade` asserts PASS and `reviewers_verified is False`. | HELD |
| `panel_lint.py:40, 100, 102, 110` (B E10) | The four names appear at those lines. | HELD |
| `SKILL.md:34, 631, 635, 999` (B E9) | Calibration "so the merged verdict weights calibrated scores"; calibrator and validator rows; validator "Non-negotiable final gate"; sc-task hook rule on `confidence_calibrated >= 0.85`. | HELD (what the prose says; obedience is not measured here) |
| `agents/evidence-validator.md:5` (B) | `tools: Read, Grep, Glob`. | HELD |
| `model_observed` (B 2.1 item 5) | Present as a telemetry view column (`telemetry.py:364`) and one skill sentence; not on the ledger or reflect verdict path. | HELD as a requirement, not as an existing capability |
| `panel.py:189-196, 600`, 8 packaged templates with `apply_to: ["first"]` (A 5, B 2.2) | Not opened. | UNVERIFIED |
| `fx7-degrade-on-reviewer-shortfall-DECISION.md` (A 2.2) | Not searched (excluded `.dev/tasks/`). | UNVERIFIED |

Status: Complete

## Round 2: Rebuttals

### Variant 1 Rebuttal (Proposal A advocate; first, saw both Round 1 statements)

Status: Complete
Advocate: Variant 1 (Proposal A). Round 2 of 2, goes first; the Variant 2 advocate rebuts after this.
Opponent file read: `round1-advocate-B.md`. Code was re-read this session where a claim is contested (see the log). Research-sourced numbers (E12 to E15 and similar) remain UNVERIFIED here, as in Round 1.

#### Response to criticisms

**R1 (B Strength 5 and Weakness 1): a Reviser-rejected false blocker stays `open`, so the union's unit cost is every remaining cycle, not one. CONCEDED, with a scope correction.**
Re-read: in `apply_revision` a `rejected` fix-map item only appends `rejected_by_reviser` to history and leaves the status alone (`ledger.py:340-342`); the function skips any row whose status is not `open` or `regressed` (`:328-329`); in the next merge only `resolved_check` rows can clear (`:254-258`); an `open` row with no current members is re-presented as "open from an earlier review, not reported again in this one" (`:457-466`) and stays in `_brief_ids` (`:99-104`). So a false blocker that the Reviser correctly rejects fails every later round until the cap, and then ESCALATE (`_decision`, `:93-96`), unless a human runs `defer` (`:350-360`). My Round 1 sentence "at most one fix cycle" was wrong on this code.
Scope correction, which does not undo the concession: (i) the cost is still bounded (3 reviews, then a human decision; the repo's S3 cap), so the direction of the asymmetry (wrong blocker is the cheaper error) survives and only its magnitude changes; (ii) the defect is in clearing (slot C-02), not in the merge policy, and it hits every confirmed blocker under B as well: B's `confirmed` rows have the same `rejected_by_reviser` dead end, and B's `rejected` adjudication is an exit only for rows its adjudicator rejects. So I take this as a precondition on the union default, not as an argument for adjudication: the "cheap error side" claim is valid only if a Reviser-rejected row gets a non-human exit (hybrid bullet 8).

**R2 (B Weakness 2): support, disputed and confidence change no outcome, so FX-10 is only priced, not addressed. CONCEDED on the default; partly answered by the hybrid.**
`_decision` and `_brief_ids` read none of them (`ledger.py:86-104`), and a one-reviewer blocker with `support` below 0.5 fails a round exactly as a unanimous one. A's default does not satisfy "a weak model must not decide alone"; it prices it. Two corrections in B's favour and one against: B is right that the verdict code never reads `confidence` but the Reviser does, because the merged report prints it in the ledger table (`ledger.py:429-435`) and in "Other findings" (`:473`), so "rendered and never read" in my Round 1 wording was loose. Against: nothing in the code that exists today makes support a reliable gate (the calibrator's reliability is unmeasured, both papers), so changing the outcome now would swap an unmeasured filter for another. The hybrid answers FX-10 with visibility now (flags on every row, bullet 2) and a pre-registered path to outcome-bearing use (bullets 7, 11), not with a silent default change.

**R3 (B Weakness 3): quorum counts completions with no independence check. CONCEDED; B shares the blind spot, and a better A is available now.**
Three `complete` reviewers served by one model satisfy `min_complete`. B's own concession C3 agrees that the existing Tier-2 gate counts the configured id (`_diversity.py:10-15` over `worker.model_id`; `openai_compat.py:468` sets `model_id=self._model`), so a served-id quorum is a C-08 prerequisite for B too. What A can do now and did not say: `merge_round` already stores `model` per reviewer in the round entry (`ledger.py:141-149`, `"model": rv.get("model")`, fed from the optional `--resolution` in `merge_cmd.py:74-83`). A can therefore record `distinct_models` and a vendor class as non-outcome data today, labelled "requested, not served", and promote them to a quorum predicate only when `model_observed` exists (bullet 3).

**R4 (B Weakness 4): "fail-closed at every panel size" overclaims against the reflect `shortfall: visible` profile. CONCEDED.**
The claim holds only in profiles that set `degrade`. With the floor of 2 that A adopted, the reflect carve-out is also nearly moot at panel sizes 2 and 3 (Round 1, K4), so the text should say: fail-closed in every profile that sets `degrade`; reflect keeps its pinned PASS-eligible 2-of-3 (`ensemble.py:755-770`; `test_ensemble_stub_integration.py:199-221`).

**R5 (B Weakness 5): "a PASS on that path rests on defaults" is only partly true. CONCEDED, already in Round 1 (K5); re-verified.**
`ensemble.py:442-465` applies clean defaults only when no seam ran (pre-supplied score or fewer than two survivors) or the child failed, and a child failure leaves convergence `None`, which degrades (`:436-440`; `contract.py:299-300`). On the main seam path the deviation flags come from `adversarial_result`. The defaults claim stands only for the pre-supplied-score path and for `merge_method` (`ensemble.py:773`). I withdraw it as an argument; it is not load-bearing for A.

**R6 (B Weakness 6): the DEGRADED exit code is "asserted safe, not shown". PARTLY ANSWERED with new evidence; the rest conceded.**
The only prose consumer I can find is the loop prompt file `src/superclaude/rules/prompts/document_review_loop_prompts.md` (mirrored at `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`, which any change must also update). Line 70 tells the coordinator to merge with `superclaude review merge`, "also for a single reviewer", that the merged report and ledger "give the verdict and the Reviser brief ids", and that "a merge refuses a round in which no reviewer produced a valid findings block; run that review again". No script or prompt in `src/superclaude`, `plugins`, `scripts` or `docs` branches on exit 10 versus 11 (grep: only `ledger_cmd.py` and `merge_cmd.py` mention these commands); the codes are pinned only by tests (`test_review_cli.py:245, 349, 369`). So a new code cannot be misread by an existing script, but I cannot show how a coordinator model treats an unknown code; that part stays UNVERIFIED. The better answer is to avoid a new verdict value: see bullet 5 (refusal, not a recorded outcome).

**R7 (B Weakness 7): `defer` rewrites the stored verdict to PASS and is pinned, so derive-on-read has a pinned counter-test. CONCEDED that derive-on-read is not shipped; the pin does not conflict with A.**
Re-read: `verdict()` returns the stored `last["verdict"]` (`ledger.py:363-372`); `defer` sets `PASS/PASS` when `brief_ids` empties (`:356-360`); the pin `test_defer_turns_a_blocking_row_into_deferred` asserts PASS, PASS and an empty brief after deferring the only blocker (`test_review_ledger.py:396-405`). Derive-on-read is therefore a change to `verdict()` and `defer`, not a description of the code. But the pin stays green under A: with the row `deferred` there is no brief, and a one-reviewer round whose dispatched count is 1 meets quorum, so the derived outcome is PASS as well. What the pin does constrain: a ledger or round without a recorded dispatched count (all existing ledgers) must be treated as "quorum not measured", not as a shortfall. And under the refuse-and-record-nothing design (bullet 5) a below-quorum round is never stored, so `defer` has nothing to lift for the quorum dimension. The `defer` bypass remains a live hazard for B's `pending` rows (B's own concession C2), where it is not solved.

**R8 (B concession C1): union stays the default until a measurement; B's gate, flags and record go in as non-outcome data. ACCEPTED and used as the basis of the hybrid.** That is a convergence on X-001/C-001: the disagreement is reduced to what B's evidence gate does when it fails (bullet 7).

**R9 (B Strength 3, 4, 8, 6, 7).**
- Strength 3 (reflect's verdict is not a union, so the core default has no verified production customer): the union's customers are the spec-review ledger (where D-2 reproduces; `ledger.py:150-157, 273-275`), re-reviews with one reviewer (`document_review_loop_prompts.md:70`), and the PR module, which consumes findings only. That is a smaller customer set than "every panel", and I accept the smaller claim.
- Strength 4 (four consumer-read contract names need a producer): real, but it is a reflect-module concern and reflect keeps its chain under A (`legacy-adversarial`). It is not an argument about the ledger default.
- Strength 8 (PR flow, evidence gate): shared; both keep a code-backed gate before findings enter a fix round.
- Strength 6 and 7 (A names no failure condition for the quorum floor beyond B's (c); A has no self-critique of its default): A's falsifiers (Round 1 section 5 items 4, 5) are thin; the hybrid adopts B's (a) to (d) and adds A's floor falsifier and a cycles-to-cap measure (bullet 11).

#### Updated assessment

Net movement from Round 1, with reasons.
- I now treat **C-001, X-001, C-007, C-011** as Hybrid, not A. B's Round 1 concession C1 changes the dispute from "union or adjudicated as default" to "which of B's items are outcome-bearing"; once B's gate, flags and record are non-outcome data and the adjudicated policy is a shadow arm, B's items are additive to A and cost nothing in the default path.
- I now concede **X-005** to B in substance: A's headline "every panel size" contradicts A's own reflect profile, and B's quorum (2 complete, 2 distinct ids) is consistent with the pins at floor 2.
- I move **S-003** from Hybrid to A: B's section 2.3 restates common ground, while A's section 2.3 states a real exit-code problem (`ledger_cmd.py:13` versus `models.py:34-48`).
- **C-010** stays Hybrid; I do not agree with B's "B": B's `support` and `disputed` inputs are real (`cluster.py:345-378`) and enter in the hybrid as data, so A also feeds them to a confidence gate.
- **X-003**: we agree on the facts (B's own C3: `model_observed` is not on the verdict path). I keep "A" because the question was whose reading of the code is right, and B's E11 wording was wrong; B's R1 verdict is "Neither" on the ground that A did not need to argue it. That is a labelling disagreement, not a factual one.
- **Points where I now agree with B's Round 1 verdict:** S-001, S-002, S-003, C-001, C-002, C-003, C-004, C-005, C-006, C-007, C-008, C-009, C-011, C-012, X-001, X-002, X-004, X-005, X-006. Disagree: C-010, X-003.
- Where I hold ground: C-005. B's own C2 concedes `pending` has no loop transition, no exit code and a `defer` bypass. The hybrid drops `pending` as an outcome state entirely (bullet 7).

#### New evidence

1. **Loop prose consumer and the existing refusal contract.** `src/superclaude/rules/prompts/document_review_loop_prompts.md:70` (and its `plugins/superclaude/...` mirror) documents that a merge refuses a round with no valid block and that the coordinator reruns the review, and that a re-review defaults to one reviewer. Extending the refusal to a below-quorum round is a one-sentence change to an existing documented protocol, where a new recorded outcome would be a new protocol.
2. **Reviser-rejected rows are re-presented every round** (`ledger.py:457-466` plus `:340-342`, `:99-104`). This confirms B's cost mechanism and fixes the unit cost of the union default at "to the cap" until C-02 provides an exit.
3. **`ledger.py:141-149` already stores a per-reviewer `model`** in the round entry (from `--resolution`), so requested-model diversity can be recorded now as data, labelled as not served.
4. **`panel.py:688-707`: the resolution carries `reviewers` and, when slots are excluded, `skipped_slots`.** A coordinator that passes `--resolution` already hands the merge the dispatched reviewer count and the skipped slots, so `requested` has an existing source without reading the manifest. (The manifest also holds `reviewers_requested` and `reviewers_resolved` as integers set at the `resolved` stage, `manifest.py:307-316`, but `merge_cmd.py` does not read it.) Whether `reviewers` there equals the count of reviewers actually dispatched in every run is not checked (UNVERIFIED).
5. **Test-coverage:** the pin at `test_review_ledger.py:345-361` (`test_round_with_no_valid_block_is_refused_and_changes_nothing`) asserts the ledger JSON is byte-identical after a refusal. It is the template for the quorum-refusal test in bullet 10.

#### Hybrid terms acceptable to A

Source tags: [A] taken from Variant 1, [B] taken from Variant 2, [New] new in this round.

1. **Default policy [A, with B R1 C1].** `union` for every panel module; reflect keeps `legacy-adversarial` as authoritative, with the union only in shadow. The verdict is a pure function of the ledger rows, the round's recorded quorum result and the policy name. No LLM stage sits in the default path.
2. **Non-outcome data added now [B, plus New for models].** Each ledger row and merged-report column carries: the result of the code-backed evidence gate (citation resolves in the snapshot: pass, fail, skipped), cluster `support` (or None), `disputed`, a derived `contested` flag (single reviewer, or disputed, or gate failed), and `confidence` as today. Each round entry carries the per-reviewer requested model id (already stored, `ledger.py:141-149`), `distinct_models` and a vendor class, labelled "requested, not served". None of these fields is read by the verdict, the brief or any exit code. They are rendered next to `confidence` so the Reviser and the next reviewer see them.
3. **Quorum definition [A, with B's independence as data].** `complete >= min_complete`, where `complete` counts reviewers whose block parsed (`complete` state, `findings_v2.py:40`; `parse_block` yields only complete, truncated, invalid, so the caller supplies failed and timed_out), the denominator is the reviewers in the resolution, and the default is `min_complete = min(2, dispatched)` in the spec-review profile (`degrade`). Independence (distinct served model ids, vendor) is a quorum predicate only after `model_observed` exists on the transport (slot C-08); until then it is bullet 2 data. Floor value is declared unmeasured.
4. **Where `requested` comes from [New, from existing sources].** `review merge --resolution` supplies the dispatched reviewer list and `skipped_slots` (`panel.py:688-707`). When `degrade` is selected and no resolution is given, the merge uses `len(--report)` as today, records `quorum: "not measured"` and prints a warning, so every existing ledger and test keeps its meaning (the `defer` pin and `test_review_cli.py` single-reviewer cases stay green). The manifest counts remain a cross-check, not a dependency.
5. **DEGRADED recorded without clearing rows [A K2 option (a), refined].** If at least one valid block exists but `complete < min_complete` in a `degrade` profile, `merge_round` raises a `LedgerError` subtype before any mutation, exactly where the zero-valid refusal sits (`ledger.py:150-157`). Nothing is recorded: no rows opened, no `resolved_check` row cleared (`:254-258`), no round appended, so the cap is not consumed and the round number is reused. The merge prints JSON with `decision: "DEGRADED"`, the complete and dispatched counts and the invalid reviewer ids; reports stay on disk, so the retry passes all reports again plus the replacement reviewer. Findings of the valid reviewer are not dropped, only not yet merged. One failed retry escalates to the user (coordinator rule in the loop prompt; the retry count is a C-07 decision, marked open).
6. **Exit codes [A, simplified].** `ledger verdict` keeps 0/10/11 (`ledger_cmd.py:13`, pinned `test_review_cli.py:245, 349, 369`) and gains no new decision value, so the `EXIT_BY_DECISION[...]` lookup cannot raise `KeyError` (`ledger_cmd.py:109`). `merge` exits 12 on the quorum refusal (not 10 or 11, which reflect uses for HALTED and DEGRADED, `models.py:34-48`; not 1, which is the generic `ClickException`). Any non-zero code is non-PASS. The loop prompt gets one sentence in both copies (`src/superclaude/rules/prompts/document_review_loop_prompts.md` and the `plugins/` mirror).
7. **Pending and contested rows [A + B].** No `pending` state exists. A contested blocking row is a blocking row: it is in the brief and fails the round as today, flagged `contested` per bullet 2. B's `adjudicated` policy exists as a named policy that runs in shadow beside the union, records what it would have confirmed or rejected, and changes no verdict; it can be promoted only by the measurement in bullet 11. If it is ever promoted, B's restriction applies (`rejected` only on a deterministic evidence failure or a quoted re-read; every rejection recorded and counted), and it needs the transitions B has not specified (brief, exit code, cap accounting, `defer`; B C2).
8. **Precondition on the union default [New, from B Strength 5].** The union may be described as the cheap-error side only while a Reviser-rejected row has an exit other than a human `defer`. C-03 records this as a dependency on slot C-02: for example, a rejected row becomes verifiable by the next round's reviewers (cleared if not re-found), which is a clearing rule, not a policy. Until C-02 lands, the cost of a false blocker is stated as "to the cap, then a human decision", not "one cycle".
9. **Reflect profile [A].** `legacy-adversarial`, `shortfall: visible`; `derive_verdict`, the 36-test `test_verdict_mapping.py` file and the 42-contract replay stay untouched; `test_i3` and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` stay green. At floor 2 `degrade` would also pass them; reflect keeps `visible` until the deferred human decision at `ensemble.py:762-764` is made. The claim is narrowed to "fail-closed in every profile that sets `degrade`".
10. **Tests that must exist [A + B + New].** (i) Quorum matrix: dispatched N in 1..5 by every assignment of the five completion states; below `min_complete` in `degrade` gives refusal and never PASS; D-2 (4 requested, 1 valid) changes from PASS to refusal. (ii) Monotonic property: adding a failed or timed-out reviewer never turns a non-PASS into PASS. (iii) Refusal records nothing: ledger JSON byte-identical before and after (pattern of `test_review_ledger.py:345-361`). (iv) Non-outcome property [B, New]: randomizing `support`, `disputed`, gate result and `contested` leaves verdict, brief and exit codes unchanged. (v) Rewrite, not delete, `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`test_review_ledger.py:376-385`) for `degrade` and keep a legacy-mode copy with quorum "not measured". (vi) `defer` pin (`:396-405`) unchanged and green. (vii) Exit pins 0/10/11 unchanged; a new test for exit 12. (viii) Reflect 36-test file, replay and the two shortfall pins unchanged.
11. **Measurement and falsifiers [A + B].** Replay the stored E2 reviewer outputs under three arms (union; union with a 2-of-3 support flag shown but non-gating; B's adjudicated in shadow), plus a held-out package, with the decision rule pre-registered before the first run and TPR/FPR per rule reported. Measures: defects found, real blocking found, wrong blockers per row, control defects found, reviews-to-cap (with the C-02 exit present, bullet 8) and escalate-at-cap rate. Falsifiers: for the union default (A) wrong blockers drive escalate-at-cap materially above the support-flag arm with no recall gain; for adjudication (B (a) to (d)) it confirms essentially every contested blocker, rejects any real blocker, is served by a reviewer's own model, or the contested set is so large that the validator is the verdict; for the floor, 2-of-3 is indistinguishable from 3-of-3 on defect misses. B's offline replay limit (E2 holds no validator output) is stated: it measures contested volume, not adjudication quality.
12. **Claims discipline [A, B R1 W4].** The merged text says: the default rests on fail-closed asymmetry and on the absence of any measurement (not on measured superiority); fail-closed holds in `degrade` profiles; the only shipped-behaviour change in the spec loop is a refusal of rounds below quorum. B's `adjudicated`-as-default is recorded as a hypothesis awaiting the bullet 11 result.

#### Final per-point verdicts

| Point | Superior approach (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence | Agrees with opponent R1 verdict? (Y/N) |
|---|---|---|---|---|
| S-001 | Neither | 90 | Same seven sections in the same order in both papers. | Y |
| S-002 | B | 55 | B's claim/source/tag tables are easier to audit even though B mis-tagged E11. | Y |
| S-003 | A | 58 | A's exit-code subsection addresses a verified 10/11 meaning clash (`ledger_cmd.py:13`, `models.py:34-48`) that B's 2.3 restatement of common ground does not. | Y |
| C-001 | Hybrid | 66 | With B's R1 concession C1, union is the default and B's gate, flags and record are non-outcome data, with adjudication as a measured shadow arm. | Y |
| C-002 | A | 62 | The calibrate/validate/debate chain is skill-orchestrated agents, not a stage callable from a deterministic merge (`merge_cmd.py:71-118`), so it stays a module policy. | Y |
| C-003 | Hybrid | 68 | A's completion-count quorum is buildable now (`manifest.py:274`, `findings_v2.py:40`) and B's independence is recorded as data until a served id exists (`openai_compat.py:468`). | Y |
| C-004 | A | 62 | A bounds DEGRADED-on-shortfall by the reflect pins (`ensemble.py:755-770`; `test_i3`; the FX7 witness), though at floor 2 the carve-out is mostly moot. | Y |
| C-005 | A | 68 | B concedes `pending` has no loop transition or exit code and a `defer` bypass (`ledger.py:93-96, 328-329, 356-360`); the union rule is the tested one with a `contested` flag added. | Y |
| C-006 | A | 70 | A gives a function and an exit-code rule; the hybrid refines it to a merge refusal with exit 12 and no new verdict value (`ledger_cmd.py:109` KeyError avoided). | Y |
| C-007 | Hybrid | 55 | Both leave `derive_verdict` and its 36 tests alone; B's four consumer-read contract fields need a producer but that is a reflect concern, not the ledger default. | Y |
| C-008 | A | 58 | The spec-loop behaviour changes only for below-quorum rounds under A, while B's default flip is a non-shadow change by B's own INV-L finding. | Y |
| C-009 | Hybrid | 58 | The code-backed evidence gate is shared; only the unmeasured validator re-read is B-only, and it lives in the shadow arm. | Y |
| C-010 | Hybrid | 60 | B's `support`, `disputed` and gate result are real inputs for a rf-qa confidence gate (`cluster.py:345-378`) and enter as data, while A's single-reviewer quorum rule (`panel.py:189-196, 600`) covers re-review. | N |
| C-011 | Hybrid | 66 | A's quorum matrix and property tests are decidable now; B's falsifiers (a) to (d) and the non-outcome property test sit on top. | Y |
| C-012 | B | 58 | A separate `calibration_map` channel (`cluster.py:12-13`; `findings_v2.py:96-97`) and an adjudicator model record answer the silent calibrator collapse, once a served id exists. | Y |
| X-001 | Hybrid | 64 | Both papers concede no policy is measured; union as default plus B's data and a shadow arm is the only combination neither paper's evidence contradicts. | Y |
| X-002 | A | 72 | `ensemble.py:762-764` records degrade-on-shortfall as an undecided human decision and two tests pin PASS, so "decided common ground" fails for reflect. | Y |
| X-003 | A | 80 | `fallback.py:161-179` reads `worker.model_id`, which `openai_compat.py:468` sets to the requested model, so B's E11 "served ids" wording is wrong (B's own C3 agrees on the facts). | N |
| X-004 | Hybrid | 65 | Defaults apply on the pre-supplied-score and no-seam path and convergence plus status gate the main seam path (`ensemble.py:442-465`; `contract.py:299-326`). | Y |
| X-005 | B | 55 | A's headline "every panel size" overclaims against its own reflect profile, while B's quorum at floor 2 matches the pins; fixable by wording (bullets 9, 12). | Y |
| X-006 | A | 55 | B's own Endangered table says its spec-loop default is "not shadow work", while A's change there is a refusal below quorum; the tension largely dissolves once the default is union. | Y |

#### Changed assumption responses

- **A-004: changed from ACCEPT to QUALIFY.** The 2-of-3 PASS-eligible shortfall is intended behaviour for now (FR-RH2.9, pinned by `test_i3` and the FX7 witness) but `ensemble.py:762-764` records the opposite choice as a pending human decision, so it is not a permanent property and A's text must not treat it as settled.
- A-001, A-002, A-003 and A-005 are unchanged (QUALIFY, QUALIFY, REJECT, REJECT). New evidence for A-002: the only consumer prose found is the loop prompt at `document_review_loop_prompts.md:70` and its `plugins/` mirror; additive keys remain safe and an added decision value is not, which is why bullet 6 adds no decision value.

#### Code verification log (Round 2)

| # | Citation | What I saw | Result |
|---|---|---|---|
| 1 | `ledger.py:328-329, 340-342` | `apply_revision` skips rows not `open`/`regressed`; a `rejected` item only appends `rejected_by_reviser` to history, status unchanged. | Holds (B Strength 5 correct) |
| 2 | `ledger.py:254-258` | At merge only `resolved_check` rows with no current members become `resolved`; an `open` row is never cleared. | Holds |
| 3 | `ledger.py:457-466` | An open row with no current members is rendered "open from an earlier review, not reported again in this one". | Holds (new) |
| 4 | `ledger.py:356-360, 363-372` | `defer` rewrites the last round to `PASS/PASS` when the brief empties; `verdict()` returns stored values. | Holds (B Weakness 7 correct; derive-on-read is not shipped) |
| 5 | `test_review_ledger.py:396-405` | `test_defer_turns_a_blocking_row_into_deferred` asserts FAIL, then after defer status `deferred`, verdict PASS, decision PASS, brief empty. | Holds; compatible with a derived outcome when quorum is met or unmeasured |
| 6 | `test_review_ledger.py:345-361` | A refused merge leaves the ledger JSON byte-identical. | Holds (template for bullet 10 iii) |
| 7 | `ledger.py:141-149` | Round entry stores `reviewer_id`, `model`, `report`, `report_sha256`, `block_ok`. | Holds (basis for bullet 2) |
| 8 | `ledger.py:429-435, 473` | The merged-report table prints `confidence`; "Other findings" repeats it. | Holds (B correct: the Reviser reads it; verdict code does not) |
| 9 | `merge_cmd.py:43-83, 100-118` | `--report`, optional `--resolution` (model per reviewer), `--cap`; no requested-count; merge writes the report and prints JSON, no verdict-based exit. | Holds |
| 10 | `panel.py:688-707` | Resolution JSON has `reviewers`; `skipped_slots` and `excluded` only when slots were excluded. | Holds; whether `reviewers` equals the dispatched count in every run: UNVERIFIED |
| 11 | `manifest.py:307-316` | The `resolved` stage payload requires non-negative ints `reviewers_requested` and `reviewers_resolved`, with resolved not above requested. | Holds |
| 12 | `ledger_cmd.py:13, 109` | `EXIT_BY_DECISION` has three keys; `verdict_cmd` indexes it directly. | Holds (a new decision value would raise `KeyError`) |
| 13 | `ensemble.py:420-470` | The seam runs only if no pre-supplied score and at least 2 survivors; a `None` result leaves convergence `None`; defaults apply only when `adversarial_result is None`. | Holds (B Weakness 5 correct; A's claim narrowed) |
| 14 | `contract.py:299-300, 306-307, 317-326` | Null convergence at T2, adversarial partial/failed, and convergence under 0.80 each give a degraded reason. | Holds |
| 15 | `_diversity.py:10-15`; `openai_compat.py:385, 468` | Diversity counts `worker.model_id`; the transport sends and stores `self._model`. | Holds (served-id quorum not available; both papers now agree) |
| 16 | `src/superclaude/rules/prompts/document_review_loop_prompts.md:70` (line read via a read-only `sed`) | The loop prompt: merge also for a single reviewer; merged report and ledger give the verdict and brief ids; a merge refusal for no valid block means run that review again; re-review defaults to one reviewer. Mirrored under `plugins/superclaude/rules/prompts/`. | Holds (new); the `plugins/` mirror's content was not diffed (UNVERIFIED) |
| 17 | Grep for `ledger verdict\|review merge` over `src`, `plugins`, `scripts`, `docs` (md, sh, py, yaml) | Matches only the loop prompt (and its mirror) and `merge_cmd.py`. | No script branches on exit 10 versus 11 in those trees; coordinator behaviour on an unknown code UNVERIFIED |
| 18 | Research-sourced figures (E12 to E17, 65 versus 38 judge-blocking, 6 of 15 runs, 41.5%) | Not opened. | UNVERIFIED here |
| 19 | `fx7-degrade-on-reviewer-shortfall-DECISION.md` | Not searched (`.dev/tasks/` excluded). | UNVERIFIED |

### Variant 2 Rebuttal (Proposal B advocate; second, saw A's Round 2 as well)

Advocate: advocate-B-r2. Round 2 of 2. Read: my round1-advocate-B.md, round1-advocate-A.md, round2-advocate-A.md, diff-analysis.md. Code was re-read this session wherever a claim below is contested (log at the end). Research-file numbers (E12 to E17 and similar) remain UNVERIFIED by me; I did not open `research/`. Tags in the counter-hybrid: [A] from Variant 1, [B] from Variant 2, [New] new in this round.

#### Response to criticisms

Concessions from Round 1 that I maintain in full: C1 (adjudication beating the union is unmeasured, so union stays the default), C2 (`pending` has no loop transition, no exit code, and a `defer` bypass), C3 (B's E11 "served ids" is wrong as worded), C4 (the legacy chain is not a core-callable stage and emits no per-row enum), C5 (X-002 contradicted for reflect), C6 (the adjudicator is an LLM and a new fail-open surface), C7 (E12 figures are upper bounds). C8 is narrowed: A's refusal also changes the spec loop, but A frames it as a defect fix, which is fair.

**W1 (`pending` has no place in the fix loop): CONCEDED, and A's trace is right.** I re-read `ledger.py`. A pending row held outside `_brief_ids` gives an empty brief; `merge_round` then computes `"FAIL" if brief else "PASS"` (`ledger.py:273-275`), so a pending-only round is PASS unless a third value is added; `render_merged_report` prints "Blocking finding ids: none." (`:487-492`) and lists "Other findings" only for `not r["blocking"]` rows (`:467-474`), so neither the Reviser nor the next reviewer sees a pending blocker. I withdraw `pending` as a row state in the default path (counter-hybrid term 6).

**W2 (`defer` can flip a round to PASS over pending rows): CONCEDED.** `defer` rewrites the last round to PASS when `brief_ids` empties (`ledger.py:356-360`, pinned at `test_review_ledger.py:396-405`). Dropping `pending` removes this hazard for B; it stays a hazard for any future outcome-bearing state.

**W3 (served-model quorum not in code): CONCEDED.** The gate counts `worker.model_id` (`_diversity.py:8-15`), set to the configured id (`openai_compat.py:467-468`). Independence becomes recorded data labelled "requested, not served" until C-08 provides `model_observed`.

**W4 (E7 to E10 argue for keeping reflect's chain, which A already does): CONCEDED for the ledger default, held for one narrow point.** E7 to E10 do not show that the ledger or the PR module needs an LLM stage. What they do show, and what A's hybrid does not address, is that four consumer-read contract fields (`panel_lint.py:40, 100, 102, 110`; `SKILL.md:999`) have a producer only in skill prose. That is a reflect-module concern and I stop arguing it inside C-03.

**W5 (the adjudication stage is not code, so the default is non-deterministic and not unit-testable): CONCEDED for the default flow, held for the policy function.** A policy of the form `policy(rows, quorum, adjudication) -> outcome` is pure once `adjudication` is a stored input and can be tested exhaustively like A's quorum matrix. The stage that produces `adjudication` is an LLM and cannot be unit-tested; B's section 5 already says so. A two-phase merge (merge, then validator, then derive) does not fit `merge_cmd.py:71-118`, a one-call deterministic command. So the stage belongs in an offline or shadow arm, not in `review merge`.

**W6 (contested is the norm, so the validator becomes the verdict): CONCEDED; B never defined "contested" tightly.** B section 5 item 1 reads "single-reviewer, has no resolved anchor, or flagged by the code gate", which can be taken as an OR. With E15 (13 of 216 clusters had two or more reviewers, [UNVERIFIED]), plain single-reviewer would make nearly every row contested and the validator the de facto verdict. The definition must exclude plain single-reviewer; see term 7.

**W7 (B changes shipped spec-loop behaviour while claiming shadow-only): CONCEDED.** Withdrawn as a default; see term 1.

**W8 (B treats DEGRADED-for-partial-panel as decided): CONCEDED (C5).**

**W9 (test surface): CONCEDED for B's default** (an `adjudication` enum that must stay consistent with `status`, `_brief_ids`, `defer`, `apply_revision` at `ledger.py:328-329` and the renderer, none with a pending-row test). Held only for the pure policy function above.

**A's Round 1 K1 to K8 and Round 2 R1 to R9.** I accept R1 (the union's unit cost is "to the cap" until clearing has a non-human exit; I verified the same trace in Round 1), R2 to R5 and R7, and agree R8 is the convergence point. Where I hold ground against A's hybrid is in its mechanics, not its direction; see the next section.

#### Evaluation of A's hybrid (bullet by bullet)

**Bullet 1 (union default, reflect `legacy-adversarial`, pure function, no LLM in default): ACCEPT.** This is my Round 1 C1 conceded in A's words.

**Bullet 2 (non-outcome data: gate result, `support`, `disputed`, `contested`, models; rendered next to `confidence`): ACCEPT-WITH-CHANGE.** Three problems, all from code.
1. `support` and the citation gate cannot be computed for ledger rows. The ledger parses findings-v1 with `fnd.parse_block`, `fnd.annotate` and `fnd.cluster` (`ledger.py:128-136, 165`), and `findings.py` has no confidence, calibration or support symbol (Grep: no match). `support` and the snapshot-citation gate belong to `cluster_v2`, which takes findings-v2 blocks and a calibration map (`cluster.py:3-18, 35-52`). On the spec ledger `support` would be None on every row, which `cluster.py:42-44` calls "uncalibrated". The ledger analogue of the gate is `span is None` (stored today; pinned by `test_missing_anchor_is_kept_without_a_span`).
2. Most of the flags are derivable offline from rows that are already stored: `confidence` (`overlap` or `single`) is computed from `members` (`ledger.py:86-90`), `span` is stored, and each member records its own `blocking` (`ledger.py:172-179`), so "members disagree on blocking" is derivable. A flag that can be recomputed from the stored ledger is not worth a new column. Ship only what cannot be recovered later: per-round `requested`, `complete`, `quorum` result and the requested model ids.
3. "Non-outcome" is only true for code. The merged report is read by the Reviser LLM (`ledger.py:429-435, 473`), so a rendered `contested` flag can change which fixes the Reviser applies and therefore the next round. Also the table header is pinned (`test_review_ledger.py:451`), so a render change breaks a pin. If flags are rendered, the arm "flag shown, non-gating" in bullet 11 is a treatment, not a control. Exact change: no new row columns or render changes; derive flags in the replay script; add only the round-entry keys above.

**Bullet 3 (quorum `complete >= min_complete`, `min(2, dispatched)`, independence as data until `model_observed`): ACCEPT-WITH-CHANGE.** Define the denominator as `max(len(resolution.reviewers), len(--report))`, so a replacement reviewer with a new id raises `complete` without lowering `requested`, and a caller cannot shrink the denominator by omitting a reviewer from `--report` when a resolution is present. Everything else accepted. Note `merge_round` sees only `block_ok` per reviewer (`ledger.py:123-130`); `failed` and `timed_out` are caller states (`findings_v2.py:40`), which in the merge CLI collapse into "absent from `--report`" (see bullet 4).

**Bullet 4 (`requested` from `--resolution`; `len(--report)` fallback gives quorum "not measured"): REJECT the "not measured" fallback; ACCEPT the source.** Re-read evidence that the fallback leaves D-2 open for every existing caller:
- `--resolution` is optional and used only for the model per reviewer (`merge_cmd.py:50-56, 73-83`).
- The loop prompt tells the coordinator to merge with `superclaude review merge` and never mentions `--resolution` (`document_review_loop_prompts.md:70`), and `commands/spec-panel.md` contains no `resolution` (Grep: no match). So today's callers pass no resolution, and under "not measured" the quorum is not enforced, so D-2 stays PASS for all of them.
- Even with a resolution, a reviewer that wrote no report file is absent from `--report` (`merge_cmd.py:84-98`), so a count over reports alone cannot see it.
Exact change: with no resolution, enforce quorum against `len(--report)` as a lower bound for `requested` and print a warning that absent reviewers are not counted. That closes the reproduced D-2 case (four reports, one valid, three broken: `complete 1 < min(2, 4)`) for every caller with no prompt change, and leaves only the "reviewer wrote no file" variant open until the loop prompt (both copies) is changed to always pass `--resolution`. Single-report re-reviews stay unchanged because `min(2, 1) = 1`. A side effect A should state: `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (`test_review_ledger.py:376-385`, two reviewers, one valid) becomes a refusal and must be rewritten, so a "legacy-mode copy" of it (bullet 10 v) is not needed.

**Bullet 5 (below-quorum raises a `LedgerError` subtype before any mutation, records nothing, merge exits 12, prints JSON): ACCEPT-WITH-CHANGE.** Adversarial checks:
- *Does a refusal that records nothing lose the valid reviewer's findings?* No. `merge` reads reports from paths the caller supplies (`merge_cmd.py:84-98`) and saves the ledger only after `merge_round` and the render succeed (`:109-116`); the reports stay on disk, so the retry passes them again. The existing pins show the pattern: `test_round_with_no_valid_block_is_refused_and_changes_nothing` (`test_review_ledger.py:345-361`, byte-identical ledger) and `test_review_cli.py:448-449` (`not ledger.exists() and not out.exists()`). The refusal also prevents the K2 hazard: a mostly-failed panel cannot clear `resolved_check` rows (`ledger.py:254-258`).
- *Can the coordinator loop make progress?* Yes if one reviewer failed transiently: re-run that reviewer, pass all reports plus the new one. Not if a reviewer permanently fails (model outage, repeated invalid block). Then every retry is refused, the cap is not consumed (nothing is recorded), and the only bound is prose. The code cannot count retries because the refusal writes nothing. That is already true of the zero-valid refusal ("run that review again", `document_review_loop_prompts.md:70`), so A inherits it, but A now widens the set of rounds it applies to. Exact change: the loop prompt must say "re-run only the missing reviewers once; if the quorum is still not met, stop and escalate to the user", in both prompt copies. There is no code-level waiver; a user can re-resolve a smaller panel by decision, which is visible.
- *The JSON.* A says the refusal "prints JSON with `decision: DEGRADED`". A raised exception prints no result. Change: catch the subtype in `merge_cmd.py` and print `{"refusal": "quorum_shortfall", "requested": n, "complete": k, "invalid": [...]}`; do not use the word DEGRADED or a `decision` key, because `ledger verdict` would then show the previous round's stored decision (`ledger.py:363-372`) and a reader could confuse the two.

**Bullet 6 (`ledger verdict` keeps 0/10/11, no new decision value; `merge` exits 12): ACCEPT-WITH-CHANGE.** Verified: `EXIT_BY_DECISION[v["decision"]]` (`ledger_cmd.py:109`) raises `KeyError` on an unknown decision, so a new stored decision value would break `ledger verdict`; A is right to avoid one and I withdraw my Round 1 framing that an additive code is the open point. The code values in use in the review CLI are 1 (`ClickException`, `panel_cmd.py:123, 128`, `manifest_cmd.py:232, 239`) and 10/11 (`ledger_cmd.py:109`); a Grep of `sys.exit` and `SystemExit` under `cli/review` shows no 12. Changes: (a) the zero-valid refusal is the limit case of the same rule and should use the same exception class and code 12, so the coordinator has one "run the review again" signal; its pin asserts the message and the absence of files (`test_review_cli.py:448-449`), so only a code assertion, if any, needs updating; (b) I did not re-read `models.py`, so "12 does not collide with reflect's codes" rests on A's reading (UNVERIFIED by me).

**Bullet 7 (no `pending` state; `adjudicated` runs in shadow beside the union and records what it would do): ACCEPT-WITH-CHANGE.** Dropping `pending` is right (W1, W2). "Runs in shadow beside the union" needs a write path: the ledger CLI has only `revise`, `defer`, `verdict` and `capture` (`ledger_cmd.py`), and the repo rule is that only these scripts change a finding's status (loop prompt line 70). A per-round shadow validator also costs a model call every round for no effect. Exact change: run the adjudicated arm offline on stored reviewer outputs (B section 5), not inside production rounds, until a promotion decision exists.

**Bullet 8 (union is the cheap-error side only while a Reviser-rejected row has a non-human exit; dependency on C-02): ACCEPT, with one addition.** The addition: a later reviewer's `prior` line cannot clear a row either. `prior` notes only append a `prior_note` history entry (`ledger.py:259-272`); only `resolved_check` rows clear (`:254-258`). So "next round's reviewers verify a rejected row" requires C-02 to give `prior` or a new verb a status effect. C-03 should state the false-blocker cost as "to the cap, then a human decision" until then.

**Bullet 9 (reflect profile `legacy-adversarial`, `shortfall: visible`, claim narrowed to `degrade` profiles): ACCEPT.**

**Bullet 10 (tests): ACCEPT-WITH-CHANGE.** Add: (a) a CLI-level D-2 test with four `--report` args, one valid and three broken, no resolution, expecting exit 12 and no files; (b) the same with a `--resolution` listing four reviewers and only one `--report` (absent-file case) expecting exit 12; (c) a replacement-reviewer test (new id counts toward `complete`, not `requested`); (d) delete (v), the "legacy copy" (see bullet 4); (e) the non-outcome property test (iv) must be scoped to code, since the Reviser reads rendered text; if no render change ships (bullet 2 change), it is trivial and can be dropped.

**Bullet 11 (measurement and falsifiers): ACCEPT-WITH-CHANGE.** The arm "union with a 2-of-3 support flag shown but non-gating" cannot be computed from stored E2 v1 data: v1 rows have no calibration, so `support` is None (bullet 2 point 1), and B's own section 5 limit says E2 holds no calibrator, validator or debate output. Replace it with arms computable from stored v1 ledgers: (i) union; (ii) union excluding rows with `span is None`; (iii) union requiring two or more reviewers on a row; (iv) `adjudicated`, only on a new run. Keep falsifiers (a) to (d), the floor falsifier and reviews-to-cap.

**Bullet 12 (claims discipline): ACCEPT, with one sentence added:** "D-2 is closed for callers that supply reports for every dispatched reviewer; the variant where a reviewer wrote no file is closed only when the coordinator passes `--resolution`."

#### Updated assessment

I now agree with A on all 21 verdicts (table below), including X-003, which I moved from Neither to A: A's reading of the code (requested id, not served) is the superior one and the contradiction is inside B. Net movement from Round 1: C-001 and X-001 from "Hybrid 60" to "Hybrid 65 and 62" because A's hybrid now carries B's falsifiers and policy slot; C-010 from B to Hybrid, because rf-qa's confidence gate cannot use `support` on findings-v1 ledgers; C-005 and C-006 to A at 65. Where I do not agree with A is not a verdict but three mechanisms in its hybrid: the "not measured" fallback (bullet 4), the shadow arm inside production rounds (bullet 7), and the claim that rendered flags are non-outcome data (bullet 2). Those are fixes, not a change of direction.

#### New evidence

1. **v1 findings carry no confidence, calibration or support** (`findings.py` Grep: no match; ledger uses `fnd.*` at `ledger.py:128-136, 165`). So bullet 2's `support` and citation gate are not available for ledger rows until findings-v2 reaches the ledger (slot C-01); only `span is None`, `confidence`, and per-member `blocking` exist.
2. **Existing callers pass no `--resolution`:** loop prompt line 70 never mentions it; `commands/spec-panel.md` has no `resolution` match; the option is optional and feeds only `model` (`merge_cmd.py:50-56, 73-83`). A fallback that records "not measured" leaves D-2 open for all of them.
3. **A refusal records nothing by construction:** `led.save` runs only after merge and render succeed (`merge_cmd.py:109-116`), and `test_review_cli.py:448-449` asserts no ledger or merged report exists after the zero-valid refusal. The same pattern is available for a quorum refusal with no new persistence.
4. **Because quorum is a merge-time gate, it needs no derive-on-read.** The `defer` pin (`test_review_ledger.py:396-405`) and "existing ledgers without a recorded count" concerns in A's R7 disappear: a round that exists in the ledger already met quorum when it was merged.
5. **`prior` notes cannot clear a row** (`ledger.py:259-272`), which sharpens the C-02 dependency in bullet 8.
6. **Unbounded retry:** a refusal consumes no cap (`_decision` uses `n` from `--round`, and nothing is appended), so the only bound on "re-run the review" is prose, exactly as for the zero-valid refusal today.
7. **Review CLI exit codes in use:** 1, 10, 11 only (`ledger_cmd.py:109`, `panel_cmd.py:123, 128`, `manifest_cmd.py:232, 239`); 12 is free inside `cli/review`.

#### Counter-hybrid terms

1. **[A, with B C1] Default policy.** `union` for every panel module; verdict is a pure function of rows and the policy name; reflect keeps `legacy-adversarial` authoritative with `shortfall: visible`; no LLM stage in `review merge`.
2. **[A, New] Quorum is a merge-time gate, not a derived outcome.** `complete >= min(2, requested)` in a `degrade` profile (spec review default). Below it, `merge_round` raises a `QuorumShortfall` subtype of `LedgerError` before any mutation, in the same place as the zero-valid refusal (`ledger.py:150-157`). Floor value declared unmeasured.
3. **[New] `requested` source.** `requested = max(len(resolution.reviewers), len(--report))`. With no resolution, enforce against `len(--report)` as a lower bound and print a warning. The loop prompt (`src/superclaude/rules/prompts/document_review_loop_prompts.md` and its `plugins/` mirror) changes to always pass `--resolution`. Single-report re-reviews are unaffected.
4. **[A, New] Refusal contract.** `merge` exits 12 and prints `{"refusal": "quorum_shortfall", requested, complete, invalid}`; no `decision` value is added, so `EXIT_BY_DECISION` (`ledger_cmd.py:13, 109`) and the 0/10/11 pins hold. The zero-valid refusal uses the same class and code. Loop prompt: re-run the missing reviewers once, then escalate to the user; the retry bound is prose-only and stated as such.
5. **[A, B reduced] Recorded data, nothing derivable.** Round entries gain `requested`, `complete`, `quorum` and the requested model ids and vendor class, labelled "requested, not served". No new row columns and no render change. The evidence-gate analogue (`span is None`), `confidence` and member-level blocking disagreement are computed by the replay script from stored rows. `support` and the snapshot-citation gate wait for findings-v2 in the ledger (C-01).
6. **[B reduced] No `pending` state.** A contested blocking row is a blocking row and fails the round as today. `adjudicated` exists as a named policy and runs as an offline arm on stored reviewer outputs; promotion needs a pre-registered rule and the transitions B has not specified (brief entry, exit code, cap accounting, `defer`). If promoted, B's restriction holds: `rejected` only on a deterministic evidence failure or a quoted re-read, every rejection recorded and counted.
7. **[New] Define "contested" before the replay.** Contested = single-reviewer AND (anchor unresolved OR code gate failed OR members disagree on blocking). Plain single-reviewer is not contested. Report contested volume as the primary statistic; B's falsifier (d) applies.
8. **[A, New] Precondition on the union.** The union is the cheap-error side only if a Reviser-rejected row has a non-human exit. `prior` notes are history-only (`ledger.py:259-272`), so C-02 must supply it. Until then C-03 states the false-blocker cost as "to the cap, then a human decision".
9. **[A] Reflect profile and claims.** `derive_verdict`, the 36 tests and the 42-contract replay untouched; `test_i3` and the FX7 witness green; fail-closed claimed only for `degrade` profiles; the default rests on fail-closed asymmetry and absent measurement, not measured superiority.
10. **[A, B, New] Tests.** Quorum matrix over N=1..5 and the five states; monotonic fail-closed property; refusal leaves the ledger JSON byte-identical (pattern `test_review_ledger.py:345-361`, `test_review_cli.py:448-449`); CLI D-2 with four reports and with a four-reviewer resolution and one report; replacement-reviewer id; rewrite `test_review_ledger.py:376-385`; keep `defer` pin (`:396-405`) and exit pins 0/10/11 unchanged; add an exit-12 test.
11. **[A, B] Measurement.** Arms computable from stored v1 data: union; union minus `span is None`; union requiring two reviewers; adjudicated on a new run. Pre-registered rule, TPR/FPR per rule, held-out package, reviews-to-cap with term 8 satisfied. Falsifiers: B (a) to (d), the quorum floor, and wrong blockers driving escalate-at-cap above the filtered arms with no recall gain.
12. **[New] Independence.** Requested model ids are data now. Promote distinct-served-id and vendor to a quorum predicate only when the transport records `model_observed` (C-08); until then the check "adjudicator or calibrator served by a reviewer's model" remains a falsifier, not a gate.

#### Final per-point verdicts

| Point | Superior approach (A / B / Hybrid / Neither) | Confidence % | One-sentence evidence | Agrees with opponent R2 verdict? (Y/N) |
|---|---|---|---|---|
| S-001 | Neither | 90 | Both use the same seven sections in the same order. | Y |
| S-002 | B | 55 | B's claim/source/tag tables are easier to audit, though B mis-tagged E11. | Y |
| S-003 | A | 58 | A's 2.3 states the real 10/11 meaning clash (`ledger_cmd.py:13`) that B's 2.3 restatement does not. | Y |
| C-001 | Hybrid | 65 | Union default plus B's falsifiers and an offline adjudicated arm; no policy is measured. | Y |
| C-002 | A | 60 | The chain is skill-orchestrated agents, not a stage a one-call deterministic merge can host (`merge_cmd.py:71-118`). | Y |
| C-003 | Hybrid | 65 | Completion-count quorum is buildable now (`manifest.py:269-274`); independence is data until a served id exists (`openai_compat.py:467-468`). | Y |
| C-004 | A | 68 | The reflect pins (`test_ensemble_stub_integration.py:199-221`, `test_verdict_mapping.py:572-591`) bound where degrade-on-shortfall applies. | Y |
| C-005 | A | 65 | `pending` has no brief entry, exit code or `defer`-safe place (`ledger.py:99-104, 273-275, 356-360, 487-492`). | Y |
| C-006 | A | 65 | A names a function and a refusal exit code; its decision-value variant would break `ledger_cmd.py:109`, which the hybrid avoids. | Y |
| C-007 | Hybrid | 55 | Both leave `derive_verdict` alone; B's four contract fields need a producer but that is a reflect concern. | Y |
| C-008 | A | 60 | A changes the spec loop only below quorum; B's default flip is a non-shadow change by B's own INV-L finding. | Y |
| C-009 | Hybrid | 55 | A code gate before `verify` is shared; only the unmeasured validator is B-only. | Y |
| C-010 | Hybrid | 55 | `support` and `disputed` exist only in the v2 kernel (`cluster.py:345-378`); findings-v1 ledgers cannot feed an rf-qa confidence gate yet. | Y |
| C-011 | Hybrid | 65 | A's matrix and property tests plus B's falsifiers; the 2-of-3 support arm is not computable from stored v1 data. | Y |
| C-012 | B | 55 | A separate `calibration_map` channel (`cluster.py:12-13`, `findings_v2.py:96-97`) answers calibrator collapse, but only once a served id exists. | Y |
| X-001 | Hybrid | 62 | Same evidence as C-001; neither default is measured. | Y |
| X-002 | A | 75 | `ensemble.py:762-764` leaves degrade-on-shortfall undecided and two tests pin PASS. | Y |
| X-003 | A | 75 | The transport stamps the configured id (`openai_compat.py:467-468`), so B's E11 "served" wording is wrong; the contradiction is inside B. | Y |
| X-004 | Hybrid | 65 | Defaults apply on the pre-supplied-score path; the seam path takes flags from the adversarial child and degrades on null or low convergence (`ensemble.py:442-465`, `contract.py:298-326`). | Y |
| X-005 | B | 55 | B's quorum at floor 2 matches the pins; A's "every panel size" headline overstated against its own profile. | Y |
| X-006 | A | 55 | B's own Endangered table calls its spec-loop default "not shadow work"; with a union default the tension dissolves. | Y |

#### Changed assumption responses

- **A-002: changed to QUALIFY with a new reason.** Additive row and round keys are safe for `load` (`ledger.py:47-48`), but an added decision value is not: `EXIT_BY_DECISION[v["decision"]]` raises `KeyError` (`ledger_cmd.py:109`). Also a render change breaks the header pin (`test_review_ledger.py:451`).
- **A-003: changed from REJECT to QUALIFY.** Under the merge-time refusal gate a quorum shortfall needs no stored state, so its transition is defined (refuse, re-run, then escalate by prose). It stays undefined for any outcome-bearing state such as `pending`, which the counter-hybrid drops.
- A-001, A-004 and A-005 are unchanged (QUALIFY, QUALIFY, REJECT).

#### Code verification log (Round 2)

| # | Citation | What I saw | Result |
|---|---|---|---|
| 1 | `merge_cmd.py:50-56, 71-118` | `--resolution` optional ("model per reviewer"); models map built from `["reviewers"]`; `led.save` and the report write come after `merge_round` and render succeed; `LedgerError` becomes `ClickException` (exit 1); stdout JSON printed only on success. | Held; basis for bullets 4 to 6 |
| 2 | `document_review_loop_prompts.md:70` | Merge with `superclaude review merge`, also for one reviewer; refusal on no valid block means run the review again; no mention of `--resolution`. | Held (A R6 correct; basis for bullet 4) |
| 3 | `commands/spec-panel.md` Grep for `resolution` | No match. | Held (existing callers pass no resolution) |
| 4 | `panel.py:688-707` | Resolution has `reviewers`; `skipped_slots` and `excluded` only when slots were excluded. | Held (A new evidence 4) |
| 5 | `findings.py` Grep for `confidence\|calibrat\|support` | No match; `parse_block` at `:124`, `annotate` at `:346`, `cluster` at `:382`. | Held; no support in v1 |
| 6 | `ledger.py:128-136, 165, 172-179` | Ledger uses `fnd.parse_block`, `fnd.annotate`, `fnd.cluster`; members record `blocking` per member. | Held |
| 7 | `ledger.py:254-258, 259-272` | Only `resolved_check` rows clear; `prior` notes append history only. | Held (new: `prior` cannot clear) |
| 8 | `ledger.py:328-329, 340-342` | `apply_revision` skips non-`open`/`regressed` rows; a rejected item adds history only. | Held (A R1 correct) |
| 9 | `ledger.py:356-360, 363-372` | `defer` rewrites last round to PASS/PASS when brief empties; `verdict()` returns stored values. | Held |
| 10 | `ledger.py:429-437, 467-494` | Table prints `confidence`; "Other findings" lists only non-blocking rows; "Blocking finding ids: none." when brief is empty; ESCALATE text joins `brief`. | Held (basis for W1) |
| 11 | `test_review_ledger.py:345-361` | Refusal leaves ledger JSON byte-identical, `L1` still `resolved_check`, one round. | Held |
| 12 | `test_review_ledger.py:376-385, 396-405, 451` | One-valid-of-two pin; `defer` pin asserting PASS; table header pinned at `:451`. | Held |
| 13 | `test_review_cli.py:448-449` | Refusal message asserted; `not ledger.exists() and not out.exists()`. | Held |
| 14 | `ledger_cmd.py:13, 109` | `EXIT_BY_DECISION` has three keys; `sys.exit(EXIT_BY_DECISION[v["decision"]])`. | Held (new decision value would raise `KeyError`) |
| 15 | Grep `sys.exit\|SystemExit` under `cli/review` | Only `ledger_cmd.py:109`, `panel_cmd.py:123, 128`, `manifest_cmd.py:232, 239` (values 1 and the 10/11 map). | Held; 12 unused inside `cli/review` |
| 16 | `cluster.py:3-18, 35-52` | `cluster_v2` takes findings-v2 blocks, a snapshot file list and a `calibration_map`; `support` is None and "uncalibrated" when a member lacks calibrated confidence. | Held |
| 17 | `models.py:34-48` (reflect exit codes) | Not re-read this round. | UNVERIFIED by me (A's claim) |
| 18 | `panel.py:189-196, 600`; count of 8 templates; `fx7-...-DECISION.md`; research-file numbers | Not opened or searched. | UNVERIFIED by me |

Status: Complete

## Round 2.5: Invariant Probe (independent fault-finder)

Executed by agent `c03o-fault-finder` after Round 2 (depth standard). Inputs: diff-analysis, both Round 1 statements, both Round 2 rebuttals, the code (read-only). It probed the emerging consensus (union default; merge-time quorum refusal below `min(2, requested)` with nothing recorded and exit 12; `requested = max(len(resolution.reviewers), len(--report))`; no `pending` state; adjudicated policy as an offline arm; independence as recorded data) across 6 categories and returned 17 findings: 5 ADDRESSED, 12 UNADDRESSED (HIGH 2, MEDIUM 8, LOW 2). Full table: `invariant-probe.md`; raw findings with file:line evidence: `round2.5-fault-finder-raw.md`.

Invariant probe gate: CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-006 (shipped union keeps every parsable finding, including those of an invalid-block reviewer; consensus text says "complete reviewer"), INV-007 (`requested` taken from `resolution.reviewers` excludes `skipped_slots`, so shipped exclusion flags can shrink the panel to one reviewer and one valid empty block passes). 8 MEDIUM UNADDRESSED items are warnings (INV-001, 002, 003, 004, 005, 009, 010, 016).

Round 3 is not available at `--depth standard`; the 2 HIGH items were therefore not debated and stay open (see Convergence Assessment).

## Scoring Matrix

Winner and confidence are taken from the two advocates' final (Round 2) per-point verdicts. Both advocates named the same winner on all 21 S/C/X points; confidence is the mean of the two stated values (rounded). "Hybrid" means both advocates concluded that the point resolves by combining elements of both variants (the elements are in the two Round 2 hybrid sections). "Neither" means no variant is superior.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Neither | 90% | Same seven H2 sections in the same order. |
| S-002 | Variant 2 (B) | 55% | Claim/Source/Tag tables are easier to audit, though B mis-tagged E11. |
| S-003 | Variant 1 (A) | 58% | A's exit-code subsection states the verified 10/11 clash (`ledger_cmd.py:13`, `models.py:34-48`); B's 2.3 restates common ground. |
| C-001 | Hybrid | 65% | Union stays default (B conceded in Round 1: no policy measured); B's falsifiers and an offline adjudicated arm are added. |
| C-002 | Variant 1 (A) | 61% | The calibrate/validate/debate chain is skill-orchestrated agents, not a stage a one-call deterministic `review merge` can host (`merge_cmd.py:71-118`). |
| C-003 | Hybrid | 66% | A's completion-count quorum is buildable now; B's independence is recorded data until the transport records `model_observed` (`openai_compat.py:467-468`). |
| C-004 | Variant 1 (A) | 65% | A verified the reflect pins bounding degrade-on-shortfall (`ensemble.py:755-770`, `test_i3...`, FX7 witness); B conceded C5. |
| C-005 | Variant 1 (A) | 66% | B's `pending` has no brief entry, exit code or `defer`-safe place (`ledger.py:99-104, 273-275, 356-360, 487-492`); B withdrew it. |
| C-006 | Variant 1 (A) | 68% | A names a function and a refusal exit code; a new decision value would raise `KeyError` at `ledger_cmd.py:109`, so the hybrid uses a refusal and exit 12. |
| C-007 | Hybrid | 55% | Both leave `derive_verdict` and its 36 tests alone; B's four contract fields are a reflect concern, not a ledger one. |
| C-008 | Variant 1 (A) | 59% | A changes the spec loop only below quorum; B's default flip is non-shadow by B's own INV-L finding. |
| C-009 | Hybrid | 56% | A code-backed evidence gate is shared; only the unmeasured validator re-read is B-only. |
| C-010 | Hybrid | 57% | `support`/`disputed` exist only in the v2 kernel (`cluster.py:345-378`); v1 ledgers cannot feed an rf-qa confidence gate yet. |
| C-011 | Hybrid | 65% | A's matrix and property tests plus B's falsifiers; the 2-of-3 support arm is not computable from stored v1 data. |
| C-012 | Variant 2 (B) | 56% | Separate `calibration_map` channel and adjudicator model record (`cluster.py:12-13`, `findings_v2.py:96-97`), usable once a served id exists. |
| X-001 | Hybrid | 63% | Neither default is measured; union default plus B's data and offline arm is what neither paper's evidence contradicts. |
| X-002 | Variant 1 (A) | 73% | `ensemble.py:762-764` leaves degrade-on-shortfall undecided; two tests pin PASS for 2-of-3. |
| X-003 | Variant 1 (A) | 77% | `fallback.py:161-179` reads `worker.model_id`, which `openai_compat.py:468` sets to the configured model; B's E11 wording is wrong. |
| X-004 | Hybrid | 65% | Defaults apply on the pre-supplied-score path; the seam path takes flags from the adversarial child and degrades on null/low convergence (`ensemble.py:442-465`, `contract.py:299-326`). |
| X-005 | Variant 2 (B) | 55% | A's "every panel size" headline overstated against its own `shortfall: visible` reflect profile; fixable by wording. |
| X-006 | Variant 1 (A) | 55% | B's own Endangered table calls its spec-loop default "not shadow work"; the tension dissolves with a union default. |
| A-001 | Qualified (both QUALIFY) | n/a | `complete` means a parsed valid block, not examination; necessary, not sufficient (see INV-014). |
| A-002 | Qualified (both QUALIFY) | n/a | Additive keys are safe for `ledger.load` (`ledger.py:47-48`); an added decision value is not (`ledger_cmd.py:109`); header render pins exist. |
| A-003 | Split (A REJECT, B QUALIFY) | n/a | Substance converged: both hybrids define a quorum shortfall as a merge-time refusal and drop `pending`; labels differ. |
| A-004 | Qualified (both QUALIFY) | n/a | 2-of-3 PASS-eligible reflect shortfall is intended for now (FR-RH2.9, two pins) but `ensemble.py:762-764` records the opposite as a deferred human decision. |
| A-005 | Rejected as an assumption (both REJECT) | n/a | No served model id on the shipped verdict path; it is a C-08 prerequisite. |

Points won: Variant 1 (A) 9 (S-003, C-002, C-004, C-005, C-006, C-008, X-002, X-003, X-006); Variant 2 (B) 3 (S-002, C-012, X-005); Hybrid 8 (C-001, C-003, C-007, C-009, C-010, C-011, X-001, X-004); Neither 1 (S-001).

## Convergence Assessment
- Points resolved: 25 of 26 (21 S/C/X points with identical winner from both advocates, plus A-001, A-002, A-004, A-005 with identical responses; A-003 labels differ: A REJECT, B QUALIFY)
- Alignment: 96% (25/26 = 0.9615)
- Threshold: 80%
- Taxonomy coverage gate: PASSED (L1: S-001, S-002; L2: C-001, C-002, C-007..C-012, X-001, X-006 and others; L3: C-003, C-004, C-005, C-006, X-005, A-003 and others; every level has addressed points)
- Invariant probe gate: BLOCKED (2 HIGH-severity UNADDRESSED: INV-006, INV-007)
- Status: BLOCKED_BY_INVARIANTS (agreement is above threshold, but convergence cannot be declared while HIGH UNADDRESSED invariants remain; no Round 3 at depth standard; per the error matrix the base is force-selected by score and the non-convergence is flagged for user review)
- Unresolved points: A-003 (label split, substance converged)
- Unresolved HIGH invariants: INV-006, INV-007
- Residual mechanism disagreements inside the two Round 2 hybrids (both advocates conceded the direction; these are mechanics, listed for Step 4): (1) B changed A's bullet 2: ship no new row columns or render change and compute flags offline (A's R2 came before B's and did not answer); (2) B rejected A's bullet 4 "quorum not measured" fallback and replaced it with enforcement against `len(--report)` plus `--resolution` always passed; (3) B moved A's bullet 7 shadow arm from production rounds to an offline replay; (4) B accepted refusal exit 12 but changed A's "prints JSON with decision DEGRADED" to a `refusal` object without a `decision` key. B's code evidence for each is logged in `round2-advocate-B.md` (Evaluation of A's hybrid).
