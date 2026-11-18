# Round 1 advocate statement: Variant 2 (Proposal B), slot C-03 merge-verdict-policy-and-quorum

Advocate: advocate-B-r1. Mode A, standard depth, focus correctness, risk, test-coverage. Round 1 of 2.
Tags: [VERIFIED] = I read the cited lines in this session. [UNVERIFIED] = taken from a research file I did not open. I did not open the `research/` files; every claim about r03, r06, r07, r08, web-01 is [UNVERIFIED] by me.

## Position

The core should own a verdict-policy slot, a code-only evidence gate and a per-row adjudication record, because today a round verdict depends on one reviewer-typed flag and the kernel's `support` and `disputed` fields sit unused. B's defensible claim is the slot, the gate, the record and the falsifiable test; making `adjudicated` the panel default before any measurement is a hypothesis, and B should say so. The honest end state is close to a hybrid: union stays the shipped default, B's gate and flags go into the core, and `adjudicated` is promoted only when the pre-committed replay beats the union.

## Steelman of Variant 1

A's strongest case, stated at full strength:

1. The union is the only rule that assumes nothing about reviewer reliability, and it is the rule the repo's own cost model prices correctly. Repo rule S3 caps fix cycles at 2 (3 reviews) and then escalates with the open blockers; a missed real blocker is a PASS on a defective document, which INV-I forbids. A wrong blocker is bounded by the cap and ends in a human decision; a wrongly rejected blocker has no bound.
2. A puts no unmeasured component in the verdict path. The calibrator lost its class in 6 of 15 combo runs and reported `calibrator_diversity: full` while one model served everything (E16, [UNVERIFIED]); no run scored any policy (E17). Replacing one unmeasured filter with another adds calls and a failure mode with no evidence.
3. A's quorum is buildable now from data that exists: `COMPLETION_STATES` (`findings_v2.py:40`), `reviewers_requested/resolved/complete` and `_recount` (`manifest.py:20-22, 269-274`). `merge_round` today takes only `reviewers` dicts and refuses only at zero valid blocks (`ledger.py:107-157`), so the reproduced D-2 defect (1 valid empty block of 4 gives PASS) has a concrete fix with a concrete test: a quorum matrix over N=1..5 and all five states, plus a monotonic fail-closed property test.
4. A did the work B skipped: it found the reflect pins that bound where DEGRADED-on-shortfall may apply. `test_i3_partial_two_of_three_distinct_pass_eligible` and `test_fx7_reviewer_shortfall_token_does_not_over_degrade` assert PASS for a 2-of-3 shortfall, and `ensemble.py:762-764` records degrade-on-shortfall as a deferred human decision. A's `shortfall: visible|degrade` profile respects that and keeps `derive_verdict` untouched.
5. A avoids the 10/11 exit-code collision between the ledger (`ledger_cmd.py:13`: PASS 0, REVISE 10, ESCALATE 11) and reflect (DEGRADED 11) by making DEGRADED an additive code, and it gives a pure function signature a developer can write today.
6. Every policy B wants (k-of-n, calibrated, adjudicated) is hostable by A's registry as a data change, so A loses no future option.

What A genuinely gets right and B does not: the exit-code and function-level specificity, the reflect-pin awareness, the decidable test plan, and the refusal to ship a default nobody measured.

## Strengths claimed (with evidence)

1. **The shipped verdict is a function of one reviewer-typed bit.** `_brief_ids` returns rows where `r["blocking"]` and status is `open` or `regressed` (`ledger.py:99-104`); `verdict = "FAIL" if brief else "PASS"` (`ledger.py:273-275`); a new row is blocking if `any(m["blocking"] for m in group)` (`ledger.py:187`). Nothing else reaches the decision. [VERIFIED]
2. **The policy slot the kernel was built for is empty.** `cluster.py` computes `support` (`:337`), `disputed` (`:347-351`) and `cluster_agreement` (`:405-412`). Within `src/superclaude`, only `cluster.py`, `cluster_cmd.py` and skill/ref prose contain `disputed` or `cluster_agreement` (Grep); `ledger.py` uses none. The row-level `confidence` ("overlap" or "single", `ledger.py:86-90`) is rendered in the merged report table and brief (`ledger.py:429-435, 473`) but no verdict code reads it. Correction to the shorthand "rendered and never read": the Reviser LLM does read it; the verdict code does not. [VERIFIED]
3. **The production reflect verdict is not a union, so a shared core whose only default is a union has no verified production customer for it.** `derive_verdict` degrades on the validator in `_DEGRADED_COMPONENTS_HALT_SET` (`contract.py:31-33, 274-275`), single-reviewer fallback (`:294-296`), null convergence (`:298-300`) and convergence below 0.80 (`:317-326`). Convergence comes from the adversarial child (`ensemble.py:424-440`). A's own design therefore ends with reflect on `legacy-adversarial`, spec re-reviews on a one-reviewer `union`, and the "default" governing only new multi-reviewer first reviews and the PR module. That is exactly where B's evidence gate and support flag matter. [VERIFIED]
4. **Four consumer-read contract names need a producer.** `confidence_calibrated`, `evidence_validator_ran`, `reviewer_cards`, `calibrator_diversity` are stable fields (`panel_lint.py:40, 100, 102, 110`), and `SKILL.md:999` lists the `sc-task` end-of-task hook rule `status: success AND confidence_calibrated >= 0.85`. A union core never produces them; today they come from skill prose (`SKILL.md:34, 631, 635`). [VERIFIED]
5. **A one-bit verdict makes one wrong blocker expensive, by code, not by assertion.** Trace: reviewer R2 types a wrong `blocking: true`; the row is `open` and enters the brief (`ledger.py:99-104`). If the Reviser answers `rejected`, `apply_revision` only appends `rejected_by_reviser` to history and leaves the status `open` (`ledger.py:340-342`). On the next round only `resolved_check` rows can clear (`ledger.py:254-258`), so an `open` row nobody re-finds stays `open` and keeps the verdict FAIL. The only exit is `defer`, a human command (`ledger.py:350-360`). So a correct Reviser rejection of a false blocker does not end the loop; the round runs to the cap and ESCALATEs. A says a wrong blocker costs "at most one fix cycle"; on this code it costs every remaining cycle unless clearing changes (slot C-02, which both proposals assume separate). [VERIFIED by reading; not executed]
6. **B's tests are policy-comparison tests, A's are quorum tests, and the repo needs both.** B's offline replay (section 5 item 1) scores `union` and a contested-row rule on committed E2 data with no model calls; the regression gate (36-test `test_verdict_mapping.py`, 42-contract replay) and the four failure conditions (a) to (d) are stated before any run. A's item 4 is similar but names no failure condition for the quorum floor that B's (c) does not also cover for the adjudicator.
7. **B names the fail-open risk of itself.** Endangered table: a buggy adjudicator that rejects a true blocker is a new fail-open path (INV-I HIGH), so `rejected` is restricted to deterministic evidence failure or a quoted re-read, and every rejection is recorded. A does not have an equivalent self-critique of its default; its section 4.2 lists only test-pin exposure.
8. **Future modules.** The PR flow ignores a panel verdict and consumes findings (s05:320 via r13 P12, [UNVERIFIED]); a union default sends every reviewer-typed blocking row into the push FSM's fix rounds, whose cap is pr-submit's. A deterministic gate before `verify` is the cheap part of B; A also keeps an evidence gate (A section 7, CO-22), so this strength is shared, and what B uniquely adds is the validator re-read and `pending` flag for contested rows.

## Weaknesses identified in Variant 1 (with evidence)

1. **A's cost argument is weaker than stated.** See Strength 5: on the current ledger code a false blocker that the Reviser rightly rejects is not cleared by anyone but a human `defer`, so "at most one fix cycle" understates cost. A's asymmetry claim (wrong blocker is cheap, missed blocker is expensive) is right in direction but its unit cost is wrong until C-02 lands. [VERIFIED]
2. **A's "default" resolves FX-10 only by pricing it.** FX-10 is "a weak model must not decide alone". A keeps `support`, `disputed` and `confidence` as display fields (A 2.1), so a one-reviewer blocker with `support` below 0.5 and `disputed` true fails the round exactly as a unanimous one does. No signal that already exists in `cluster.py` changes any outcome. [VERIFIED for the code; the FX-10 reading is from the diff analysis]
3. **A's quorum counts completions with no independence check.** Three `complete` reviewers all served by one model satisfy `min_complete`. The existing Tier-2 gate has the same blind spot: `compute_model_class_diversity` counts distinct `worker.model_id` over succeeded workers (`_diversity.py:8-15`), and `openai_compat.py:467-468` stamps `model_id=self._model`, the configured id, not a served id. A defers diversity to telemetry; its quorum inherits the blind spot (see Concession C3: so does B until `model_observed` is wired). [VERIFIED]
4. **A's headline fail-closed claim is wider than its own profile.** Section 1 and 4.1 say fail-closed "at every panel size"; section 2.2 sets reflect to `shortfall: visible`, where a 2-of-3 shortfall is PASS-eligible. The claim holds only for `degrade` profiles (X-005). A is honest in 2.2, but the summary sentence overclaims. [VERIFIED against `ensemble.py:755-770`]
5. **A's "PASS rests on defaults" is only partly true.** `ensemble.py:446-465` takes regression, deviation and needs-human flags from `adversarial_result` when the seam ran and defaults to clean only when no seam ran (`:442-445`: pre-supplied score, fewer than two survivors, or child failure). A child failure leaves convergence `None`, which DEGRADES (`contract.py:298-300`). So on the default seam path the PASS depends on adversarial output, not on defaults. The defaults matter for the pre-supplied-score path and for `merge_method`, which is set by reviewer count (`ensemble.py:773`). A's X-004 point is right for that path and overstated for the main one. [VERIFIED]
6. **A's new DEGRADED exit code is asserted safe, not shown.** "An old caller fails closed on the new code" holds for any script that treats non-zero as failure; whether skills that branch on 10 versus 11 treat an unknown code as error or as ESCALATE was not checked in A. [UNVERIFIED]
7. **A leaves the stored-verdict problem to someone else and builds on it.** `ledger.verdict()` returns the stored `last["verdict"]` (`ledger.py:363-372`), and `defer` rewrites it to PASS when the brief empties (`ledger.py:356-360`), pinned at `test_review_ledger.py:396-405`. A's pure function would be derived on read, but `defer` and its pin are not in A's endangered list beyond the D-1 family. [VERIFIED]

## Concessions

C1. **No measurement shows adjudication beating the union (E17).** B's own section 1 says so. `adjudicated` as the panel default is a hypothesis. I concede X-001 in the form: union stays the default until the Tier Q rule in B section 5 is met; B's evidence gate, `support`/`disputed` flags and adjudication record go into the core now, as additive data that changes no outcome.

C2. **`pending` has no loop transition, no exit code and one verified bypass.** B says `pending` blocks PASS but does not enter the Reviser brief (only `confirmed` rows do, B 2.1 item 3). The only brief is `_brief_ids` (`ledger.py:99-104`); `apply_revision` skips rows whose status is not `open` or `regressed` (`ledger.py:328-329`); `_decision` knows only PASS, REVISE and ESCALATE (`ledger.py:93-96`). So a round with only pending blockers has an empty brief and would run to the cap with nothing for the Reviser to do. Worse, `defer` of any other row empties `brief_ids` and rewrites the stored verdict to PASS (`ledger.py:356-360`, pinned at `test_review_ledger.py:396-405`), which would bypass a pending row held outside the brief. B's I-4 ("`defer` cannot rewrite a verdict") is a decided requirement, not shipped behaviour, and the pin asserts the opposite. This is the A-003 gap, and A shares its DEGRADED half.

C3. **B's E11 is mis-tagged.** B says a Tier-2 gate "computed from served model ids already exists". The gate is computed from `worker.model_id` (`_diversity.py:8-15`, `fallback.py:167-177`), which the OpenAI-compatible transport sets to `self._model` (`openai_compat.py:467-468`), the configured id. That contradicts B's own E16 (requested and served ids diverge) and A's UC row C-04 reading (X-003). `model_observed` exists on the verdict path nowhere; it is a column in the telemetry view (`telemetry.py:364`) and one skill sentence. The served-model quorum is a requirement for slot C-08, not an existing capability, and B's quorum must fall back to a completion count when it is absent. A's reading is correct on this fact.

C4. **"Reuse the legacy chain, callable from the core" overstates reuse.** The calibrator and evidence validator are agents dispatched by skill prose with inline fallbacks (`SKILL.md:631, 635`); the debate yields a convergence score and a report (`ensemble.py:424-440`). A per-row `confirmed | rejected | pending` enum is new design, not something the legacy chain already emits. I found no per-row verdict from the adversarial step in the code I read.

C5. **X-002 as B wrote it is contradicted for reflect.** B 2.3 lists "DEGRADED-style outcome for a partial panel" as common ground. For the reflect profile, two pins assert PASS for a 2-of-3 shortfall and `ensemble.py:762-764` records degrade-on-shortfall as an undecided human decision. B's own quorum (2 complete, 2 distinct ids) is consistent with the pins; the common-ground sentence is not. The sentence must be limited to modules that opt in.

C6. **The adjudicator is an LLM and a new fail-open surface; its error rate is unmeasured.** `evidence-validator` is read-only by tool list (`Read, Grep, Glob`, `agents/evidence-validator.md:5`), which meets INV-G, but a validator that wrongly rejects a true blocker is the same class of defect B accuses the union of. B's restriction of `rejected` to deterministic failure or a quoted re-read is a mitigation, not a proof.

C7. **B's wrong-blocker figures are upper bounds** (a true novel defect scores as wrong, E12 caveat), and B's own replay cannot score adjudication because E2 holds no validator or debate output (B section 5 item 1 limit).

C8. **Changing the spec loop default is a behaviour change, not shadow work** (X-006; B's own INV-L MEDIUM). A's D-2 fix also changes that loop, but A frames it as a fix of a reproduced defect.

## Shared assumption responses (A-001..A-005)

- **A-001 (a `complete` reviewer has substantively examined the document): QUALIFY.** `complete` means a parsed valid block (`findings_v2.py:40`, `manifest.py:269-274`), which measures format success, not depth. D-2 shows one valid empty block certifies PASS. Quorum is necessary but not sufficient; both proposals rest on it, B adds evidence and support signals on blocking rows only and neither adds a check on an empty block.
- **A-002 (additive keys break no reader): QUALIFY.** `load` checks only the schema string (`ledger.py:47-48`), and a Grep of `src/superclaude` and `scripts/` found no other reader of `review-ledger/1` rows, so additive keys are syntactically safe in the code I could see. Tests, variant ledgers and E2 tools outside those paths were not enumerated. B's semantic changes (excluding pending rows from the brief) are not additive.
- **A-003 (DEGRADED and `pending` have defined fix-loop transitions): REJECT.** Neither exists today. `_decision` has three outcomes (`ledger.py:93-96`) and `apply_revision` acts only on `open` and `regressed` (`ledger.py:328-329`). Both proposals must specify cap accounting, re-dispatch and the exit code before adoption; see C2.
- **A-004 (2-of-3 PASS-eligible shortfall in reflect is intended): QUALIFY.** It is deliberate FR-RH2.9 design, pinned by two tests (`test_ensemble_stub_integration.py:199-221`, `test_verdict_mapping.py:572-591`), but `ensemble.py:762-764` also records the opposite choice as a pending human decision. Treat it as intended for now and not settled; B's common-ground sentence must exclude reflect.
- **A-005 (served model id obtainable for every reviewer and adjudicator in every transport): REJECT.** The only id on the verdict path is the configured one (`openai_compat.py:467-468`); `model_observed` is a telemetry column and a decided C-08 requirement. Any independence rule must degrade to a completion-only quorum when no served id is recorded.

## Per-point verdicts

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

## Code verification log

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
