# Round 2 rebuttal: Variant 2 (Proposal B), slot C-03 merge-verdict-policy-and-quorum

Advocate: advocate-B-r2. Round 2 of 2. Read: my round1-advocate-B.md, round1-advocate-A.md, round2-advocate-A.md, diff-analysis.md. Code was re-read this session wherever a claim below is contested (log at the end). Research-file numbers (E12 to E17 and similar) remain UNVERIFIED by me; I did not open `research/`. Tags in the counter-hybrid: [A] from Variant 1, [B] from Variant 2, [New] new in this round.

## Response to criticisms

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

## Evaluation of A's hybrid (bullet by bullet)

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

## Updated assessment

I now agree with A on all 21 verdicts (table below), including X-003, which I moved from Neither to A: A's reading of the code (requested id, not served) is the superior one and the contradiction is inside B. Net movement from Round 1: C-001 and X-001 from "Hybrid 60" to "Hybrid 65 and 62" because A's hybrid now carries B's falsifiers and policy slot; C-010 from B to Hybrid, because rf-qa's confidence gate cannot use `support` on findings-v1 ledgers; C-005 and C-006 to A at 65. Where I do not agree with A is not a verdict but three mechanisms in its hybrid: the "not measured" fallback (bullet 4), the shadow arm inside production rounds (bullet 7), and the claim that rendered flags are non-outcome data (bullet 2). Those are fixes, not a change of direction.

## New evidence

1. **v1 findings carry no confidence, calibration or support** (`findings.py` Grep: no match; ledger uses `fnd.*` at `ledger.py:128-136, 165`). So bullet 2's `support` and citation gate are not available for ledger rows until findings-v2 reaches the ledger (slot C-01); only `span is None`, `confidence`, and per-member `blocking` exist.
2. **Existing callers pass no `--resolution`:** loop prompt line 70 never mentions it; `commands/spec-panel.md` has no `resolution` match; the option is optional and feeds only `model` (`merge_cmd.py:50-56, 73-83`). A fallback that records "not measured" leaves D-2 open for all of them.
3. **A refusal records nothing by construction:** `led.save` runs only after merge and render succeed (`merge_cmd.py:109-116`), and `test_review_cli.py:448-449` asserts no ledger or merged report exists after the zero-valid refusal. The same pattern is available for a quorum refusal with no new persistence.
4. **Because quorum is a merge-time gate, it needs no derive-on-read.** The `defer` pin (`test_review_ledger.py:396-405`) and "existing ledgers without a recorded count" concerns in A's R7 disappear: a round that exists in the ledger already met quorum when it was merged.
5. **`prior` notes cannot clear a row** (`ledger.py:259-272`), which sharpens the C-02 dependency in bullet 8.
6. **Unbounded retry:** a refusal consumes no cap (`_decision` uses `n` from `--round`, and nothing is appended), so the only bound on "re-run the review" is prose, exactly as for the zero-valid refusal today.
7. **Review CLI exit codes in use:** 1, 10, 11 only (`ledger_cmd.py:109`, `panel_cmd.py:123, 128`, `manifest_cmd.py:232, 239`); 12 is free inside `cli/review`.

## Counter-hybrid terms

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

## Final per-point verdicts

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

## Changed assumption responses

- **A-002: changed to QUALIFY with a new reason.** Additive row and round keys are safe for `load` (`ledger.py:47-48`), but an added decision value is not: `EXIT_BY_DECISION[v["decision"]]` raises `KeyError` (`ledger_cmd.py:109`). Also a render change breaks the header pin (`test_review_ledger.py:451`).
- **A-003: changed from REJECT to QUALIFY.** Under the merge-time refusal gate a quorum shortfall needs no stored state, so its transition is defined (refuse, re-run, then escalate by prose). It stays undefined for any outcome-bearing state such as `pending`, which the counter-hybrid drops.
- A-001, A-004 and A-005 are unchanged (QUALIFY, QUALIFY, REJECT).

## Code verification log (Round 2)

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
