# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Agent: independent fault-finder (general-purpose, not an advocate for either variant), run once after Round 2 with the six-category checklist (state_variables, guard_conditions, count_divergence, collection_boundaries, interaction_effects, sufficiency_challenge). Input: the emerging consensus M1-M12 (listed in the verbatim section below), both rounds of the transcript, the diff analysis, and the source files. The table is the orchestrator's assembly of the fault-finder's 25 findings; every field is the fault-finder's, with the evidence condensed to its core reference. The complete entries, as returned, follow the table.

Orchestrator verification (spot check of code-fact claims, read at HEAD `792cf8c52` and in the installed stoprule and diffgate skills; the rest was not re-read by the orchestrator):
- VERIFIED: INV-003 and INV-001 (`ledger.py:93-96`, `:210-218`, `:356-360`); INV-005 (`ledger.py:170-179` members hold `fid`/`blocking`/`reviewer_id`, no anchor status; `ledger.py:224-232` re-found row keeps its old span when no group member has one); INV-008 (`stoprule.py:808-830`, `evaluate_reply` compares the canary answer with `is not` against a boolean); INV-010 (`stoprule.py:665-692`, two canaries per batch whatever its size, seeded per batch from `sha256_text(f"{seed}|B{n}")`, two rejected replies give `unconfirmed`); INV-016 (`findings_v2.py:153-164`, with `reflect_category` set blocking must equal `severity != MINOR`, no `deviation_class` condition); INV-017 (`diffgate.py:796`, `verdict = "FAIL" if open_blocking else "PASS"`); INV-009 and INV-012 (`ledger.py:119-130,150-158`).
- CITATION NOT BORNE OUT: INV-019 cites `research/05-blocking-calibration.md:311` for "the control package has 0 known blocking defects". Lines 309-313 of that file do not state it. The fact (control: 2 defects, 0 blocking in ground truth) is stated in Variant B R1 and in `research/11-evaluation-evidence.md` §5 as B cites it, so the finding stands on that source; the line reference is flagged.
- NOT RE-READ by the orchestrator: INV-002, 004 (relies on `document_review_loop_prompts.md:70`, confirmed by Advocate A in Round 2 F7), 006, 007, 011, 013, 014, 015, 018, 020-025 (rest on source lines and E2 report rows the fault-finder read).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | M5 frozen decisions close the "one non-blocking re-report clears a row" hole while M1 keeps the veto live | UNADDRESSED | HIGH | Under the live veto a re-found row takes the current round's flag (`ledger.py:210-218`, pinned by `test_review_ledger.py:518-544`); default re-review is one reviewer; the freeze exists only after the flip |
| INV-002 | state_variables | New persistent state (degraded, rubric hash, frozen and shadow decisions) fits the existing ledger schema | UNADDRESSED | MEDIUM | `SCHEMA = "review-ledger/1"` (`ledger.py:17`, `load` at `:47`); mid-flight loops have no decision field; rubric-hash refusal strands a loop when `spec-v2` ships |
| INV-003 | state_variables | `defer()` can recompute the certification flag | ADDRESSED | LOW | `ledger.py:356-360`; named in M2 and in the Round 2 new evidence; flag derivable from `block_ok` per round |
| INV-004 | guard_conditions | M2's "certify at round 1, later rounds inherit" keeps PASS meaning "two valid reviewers looked" | UNADDRESSED | HIGH | The PASS-deciding round after a REVISE is a one-reviewer re-review (`document_review_loop_prompts.md:70`; one valid block suffices, `ledger.py:150-157`); the flag is sticky, no guard for a thin deciding round |
| INV-005 | guard_conditions | M3's "unresolved anchor is never effective-blocking until a named resolver re-reads it" fits the verdict | UNADDRESSED | HIGH | With the live veto the gated row leaves the brief (`ledger.py:99-104,274`) so the round can PASS before the resolver runs; v1 members carry no anchor status; no resolver on the v1 path |
| INV-006 | guard_conditions | Routing absence findings to the quoted requirement text lets the gate and the grader handle them | UNADDRESSED | MEDIUM | A located anchor proves where the reviewer pointed, not that something is absent; grader cannot read the document (`finding-grader.md:12`); a fix elsewhere leaves the row `named_not_touched` and the loop ends in ESCALATE |
| INV-007 | guard_conditions | PENDING under `--decide grader` (exit 12) fits the review loop | UNADDRESSED | MEDIUM | `_decision` has no PENDING mapping (`ledger.py:93-96`); stoprule counts waiting claims as FAIL `incomplete`; undecided rows have `blocking: None` so `defer()` can turn the round into PASS |
| INV-008 | guard_conditions | M4's true/false/undecidable reply is a rubric change (`spec-v2`) | UNADDRESSED | MEDIUM | It is a schema change: `parse_grader_reply` and `evaluate_reply` require a boolean (`stoprule.py:808-830`); "name B1/B2/B3" must fit 25 words; the files serve the live stoprule command |
| INV-009 | count_divergence | "At least two reviewers with a valid block" measures two independent looks | UNADDRESSED | MEDIUM | `block_ok` is false on any bad line; E2 audit D found 80 reviewer-level drops; dedup is by id only (`ledger.py:119-121`) so two same-model reviewers count as two; replay does not report the degrade rate |
| INV-010 | count_divergence | Canaries cost "25% overhead" and a rerun is an independent second chance | UNADDRESSED | MEDIUM | Two canaries per batch whatever its size (`stoprule.py:669-673`): 200% for a one-claim batch; rerun likely meets the same canaries; a wrong canary rejects every real claim in the batch |
| INV-011 | collection_boundaries | Grading one claim per cluster and freezing it (M5) is safe once D6 and `same_defect` are "tightened" | UNADDRESSED | HIGH | One `representative` claim per v2 cluster (`cluster.py:338-344`), v1 row takes `group[0]` claim (`ledger.py:182-199`); `same_defect` merges by shared fp (`findings.py:367-372`); a `false` demotes every member and M5 freezes it; no mechanism, test or number for "tightened" |
| INV-012 | collection_boundaries | Empty inputs (zero valid reviewers, zero candidates) are safe | ADDRESSED | LOW | Round with no valid block is refused (`ledger.py:150-157`; `test_review_ledger.py:345-373`); zero candidates give no batch (`stoprule.py:669`) |
| INV-013 | collection_boundaries | D2 ("an invalid reviewer never clears a row") is a three-line fix with no side effects | UNADDRESSED | LOW | `ledger.py:254-257` never reads `block_ok`; the fix inverts the pin at `test_review_ledger.py:376-385`; a reviewer whose block is always invalid would stop rows clearing and end in ESCALATE |
| INV-014 | interaction_effects | D1, D5, M3 evidence gate, M9 partial abstain and M2 degrade compose | UNADDRESSED | HIGH | (a) a lone reviewer's rejected blocking finding is lost while two other valid blocks still certify; (b) if D1 is fixed by raising the 200-character limit, the recovered luna and ember findings fail the M3 locate gate (`findings.py:276-304`): the D1 fix and the gate cancel |
| INV-015 | interaction_effects | Shadow can start now and `spec-v2` follow later | UNADDRESSED | MEDIUM | `spec-v1` has the fail-open default and trusts unverified evidence (`finding-grader.md:17,19`); shadow counts collected before `spec-v2` measure a rubric that will not ship; the claim-shape fix (named reader and outcome) must precede shadow |
| INV-016 | interaction_effects | M8's code predicate on `deviation_class` / `reflect_category` is one rule | UNADDRESSED | MEDIUM | `findings_v2.py:155-162` makes every MAJOR or CRITICAL finding with a `reflect_category` blocking whatever its class; `contract.py:377-381` halts only on regression or drift; `reflect_category` is optional; counts default to 0 when absent |
| INV-017 | interaction_effects | M10: two copies of the blocking rule need adapters and a parity test | UNADDRESSED | MEDIUM | At least two more copies: `diffgate.py:796` and the claim-level rule in `stoprule.py:1179-1191`; scope of the unified core over those commands is not stated |
| INV-018 | interaction_effects | A shadow grader "routes nothing" while the veto stays unchanged | UNADDRESSED | LOW | The merged report is read by the next reviewer and the reviser (`ledger.py:408-411`); a shadow annotation in it would anchor them; no rule keeps shadow data out of the report or out of the exit code |
| INV-019 | sufficiency_challenge | M12: fix D1, D5, D6 plus the paired replay alone decides between veto and grader | UNADDRESSED | HIGH | A grader that always says `false` passes the control wrong-blocker test (control has no blocking defects, see the citation note above), cannot lose measured recall on a 0.17-1.20 of 8 floor, meets only easy canaries, and no numeric pass threshold exists |
| INV-020 | sufficiency_challenge | The E2 replay can validate M2, M5 and M9 (certification, frozen decisions, clearing) | UNADDRESSED | HIGH | E2 merged each package once; the replay never runs `apply_revision`, `defer`, re-found or regressed paths, or the clear step (`ledger.py:207-238,254-258,301-360`), which is where C-006 lives |
| INV-021 | sufficiency_challenge | M4 affirmative demotion alone fixes the fail-open grader | UNADDRESSED | HIGH | B2 is ungradable on the replay inputs: v1 has no `outcome` field, claims are at most 300 characters with no enforced named reader (`findings.py:118`); the grader arm collapses toward the veto; the claim-shape fix is not in M1-M12 |
| INV-022 | sufficiency_challenge | The pooled paired replay has power | UNADDRESSED | MEDIUM | The 71 pooled rows are not independent (control is one document with 2 defects); some rows were merged from stale or replaced reports; "same candidate sets" breaks where D1 changes the set; B's R1 residual predicts an inconclusive result, which keeps the veto live forever |
| INV-023 | sufficiency_challenge | Shadow counts (`overruled`, `promoted`, `singleton_blockers`) make the choice checkable after rollout | UNADDRESSED | HIGH | Production loops have no ground truth (`research/05:195`); `overruled` measures disagreement not who is right; `promoted` precision needs labels nothing produces; the reviser's applied/rejected fix map (`ledger.py:330-342`) is the only weak label and is not named |
| INV-024 | sufficiency_challenge | M2 degrade rule alone resolves "PASS certified on a thin panel" | UNADDRESSED | HIGH | Exit codes stay 0/10/11 and `test_review_cli.py:348` asserts exit 0 and PASS; in-repo consumers are `ledger.py`, `merge_cmd.py` and the prompt prose; only prose is asked to report "uncertified", so no code enforces the flag |
| INV-025 | sufficiency_challenge | M3 evidence gate alone resolves wrong blockers without losing real ones | UNADDRESSED | HIGH | The gate's target inputs are the population that fails it: D5's 13 null-span blocking rows fail the locate step, D1's recovered long anchors likely fail it, the v1 path has no re-read resolver; the gate suppresses real blockers and no input is shown to pass it |

## Summary

- **Total findings**: 25
- **ADDRESSED**: 2 (INV-003, INV-012; both LOW)
- **UNADDRESSED**: 23
  - HIGH: 11 (INV-001, INV-004, INV-005, INV-011, INV-014, INV-019, INV-020, INV-021, INV-023, INV-024, INV-025)
  - MEDIUM: 10 (INV-002, INV-006, INV-007, INV-008, INV-009, INV-010, INV-015, INV-016, INV-017, INV-022)
  - LOW: 2 (INV-013, INV-018)
- **Category 6 (sufficiency_challenge)**: 7 findings (INV-019 to INV-025), all UNADDRESSED; each names a concrete falsifying condition and a source enumeration, so the always-on category was answered with evidence, not with an assertion.
- **Invariant probe gate**: count(HIGH + UNADDRESSED) = 11 is greater than zero, so CONVERGENCE IS BLOCKED (status BLOCKED_BY_INVARIANTS) regardless of the 90.9% diff-point agreement. At `--depth standard` there is no Round 3 in which to resolve them, so they are carried forward as unaddressed invariants (return contract) and as open items in the merged proposal. MEDIUM items are warnings and do not block.

## Fault-finder output as returned (verbatim)

The consensus the fault-finder was given:

- M1. The veto stays the live decider (as in `ledger.py:187,274`). B's blind grader is added in SHADOW; it goes live per lens only after a pre-registered paired replay on the E2 packages passes, starting with singleton blockers. `promoted` is counted only and cannot raise a FAIL until its precision is measured.
- M2. A first review needs at least two reviewers with a valid block to certify a PASS, else `degraded`; later rounds inherit; `defer()` recomputes it. Decision words and exits 0/10/11 stay. `PENDING` and exit 12 only under `--decide grader` (needs an `EXIT_BY_DECISION` entry).
- M3. A finding with an unresolved anchor or citation is never effective-blocking until a named resolver re-reads it; absence findings are routed to the quoted requirement text; the grader never treats `unverified` evidence as sole support.
- M4. The grader replies true, false or undecidable; `false` names the failed criterion; on doubt the reviewer's flag stands or PENDING; needs `spec-v2`.
- M5. A decision is frozen for rows whose cited text did not change; changed text is re-graded; row identity relies on `fp` and `same_defect` (to be tightened).
- M6. Cap of three finders kept only as a cost cap; the replay reports wrong blockers by panel size; no size-effect claim.
- M7. D1, D5, D6 fixed first for both arms; the replay runs veto and grader on the same candidate sets, both scored against `blocking_in_implement`; cause of wrong blockers unmeasured.
- M8. Reflect-post decides by a code predicate on `deviation_class` / `reflect_category`, no grader; spec and tasklist lens use a frozen rubric; reflect keeps the debate and contract 1.8.0; grader output only in nested `telemetry:`.
- M9. A partial or invalid reviewer abstains and never clears a row (D2 fix at `ledger.py:254-257`); grader-level failure: canaries, batch rejection, one rerun, then `unconfirmed`.
- M10. Two copies of the blocking rule (v1 ledger path and v2 cluster path); the grader needs adapters for both inputs plus a parity test.
- M11. Evidence transfers only to the spec and tasklist lens; reflect-pre has no ground truth.
- M12. Sufficiency claim: "fixing D1, D5, D6 and running the paired replay on the E2 packages is enough to decide between the veto and the grader, and shadow counts make the choice checkable after rollout."

The findings as returned:

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: M5 (frozen decisions) closes the "one non-blocking re-report clears a row" hole (C-006) while M1 keeps the veto live.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The frozen decision is a grader-side store. Under the live veto, a re-found row still takes the current round's flag (`ledger.py:210-218`), and `test_review_ledger.py:518-544` (read) pins that. The default re-review is one reviewer (`document_review_loop_prompts.md:70`). So one MINOR or non-blocking re-report turns a blocking row non-blocking and the loop returns PASS. The Round 2 table records C-006 as "B", but under M1 that outcome only exists after the flip. D2 (M9) guards only invalid reviewers, not valid ones that downgrade a finding. The pre-flip live path keeps the hole.

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: New persistent state (`degraded`, rubric hash, frozen decisions, shadow decisions) can be added under the same ledger schema without initialization problems.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `SCHEMA = "review-ledger/1"` (`ledger.py:17`), and `load()` accepts any ledger with that string (`ledger.py:47`). Loops mid-flight at rollout have rows with no decision and a round record with no flag. `degraded` can be derived, since `rounds[i].reviewers[].block_ok` is stored (`ledger.py:141-149`). Decisions and the rubric hash cannot be derived. U-012's "later rounds refuse a different hash" would strand a loop that started in shadow on `spec-v1` once `spec-v2` ships (M4). No default is stated for rows without a decision, and no ledger-version bump is mentioned.

ID: INV-003
CATEGORY: state_variables
ASSUMPTION: `defer()` can recompute the certification flag.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `defer()` rewrites PASS with no reviewer-count check (`ledger.py:356-360`). M2 and transcript Round 2 ("New evidence") name this. The flag is recomputable from `rounds[0].reviewers[].block_ok`. `verdict()` returns a fixed key set (`ledger.py:363-372`), so the flag goes elsewhere (F2).

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: M2's rule (certify at round 1, later rounds inherit) keeps a PASS meaning "two valid reviewers looked".
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The final PASS of any loop that went through a REVISE is decided by the re-review, and the default re-review is one reviewer (`document_review_loop_prompts.md:70`). A round needs only one valid block (`ledger.py:150-157`; `test_review_ledger.py:376-385`). So the usual PASS is a single-reviewer outcome labelled "certified" through inheritance. That contradicts the stated model: `contract.py:295-296` treats a single-reviewer outcome as DEGRADE. The flag is also sticky, so a later two-reviewer round cannot upgrade it. A guard for "the PASS-deciding round had at most one valid block" is missing.

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: M3's "unresolved anchor is never effective-blocking until a named resolver re-reads it" fits the verdict machinery.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The verdict is `FAIL if _brief_ids` (`ledger.py:99-104,274`), and PENDING exists only under `--decide grader` (M2). With the live veto, a blocking row whose anchor is unresolved drops out of the brief, so the round can return a certified PASS while the resolver has not run. The finding is lost silently, which is the D1 pattern. The v1 gate signal is weak: members store no anchor status (`ledger.py:172-179`). A re-found member whose anchor is missing leaves the row's older span in place (`ledger.py:226-231`), so the gate sees "resolved". `anchor_ambiguous` (`findings.py:351`; `span = spans[0]`) is not gated. The resolver is not named for the v1 path. `verify-citations` reads v2 cards only (`verify_cmd.py:1`, per transcript).

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: Routing absence findings to the quoted requirement text lets the gate and the grader handle them.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: A located anchor proves where the reviewer pointed, not that the thing is absent. The grader "cannot see" the document (`finding-grader.md:12`), so it cannot check an absence claim either. Both gates pass a hallucinated "no X" claim. The clearing side is also stuck. A fix that inserts text elsewhere never touches the cited span, so the row ends as `named_not_touched` and never reaches `resolved_check` (`ledger.py:330-339`; `findings.py:442-457`). Once M5 freezes the decision for unchanged cited text, the loop cannot converge for absence defects and runs to ESCALATE.

ID: INV-007
CATEGORY: guard_conditions
ASSUMPTION: PENDING under `--decide grader` (exit 12) fits the review loop.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `_decision` knows only PASS, REVISE (n<cap) and ESCALATE (`ledger.py:93-96`), so PENDING at the cap has no mapping. A PENDING round does not consume a review. Stoprule counts waiting claims as `FAIL incomplete` (`stoprule.py:1183-1184`), so there the waiting state advances the loop, and M2's PENDING does not. After a rerun the batch is `unconfirmed` for good (`stoprule.py:684-691`), so the loop has no exit except a human. Transcript G2: undecided rows have `blocking: None`, so they are absent from `_brief_ids` and `defer()` turns the round into PASS. M2 lists `defer()` only for `degraded`, not for PENDING. M2 also lists `EXIT_BY_DECISION` (`ledger_cmd.py:13,109`) only for the new code.

ID: INV-008
CATEGORY: guard_conditions
ASSUMPTION: M4's true/false/undecidable reply is a rubric change (`spec-v2`).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: It is a schema change. `parse_grader_reply` requires exactly the keys {cid, blocking, q2, why}, a boolean `blocking`, and `why` of at most 25 words (`stoprule.py:808-816`). `evaluate_reply` compares canaries with `is not` on the answer (`stoprule.py:826`). A tri-state answer therefore rejects the batch, and "must name B1/B2/B3" has to fit inside 25 words. `finding-grader.md:29-35` states the boolean schema. These files serve the live stoprule command, so a fork is needed, and M4 does not say so. "Reviewer's flag stands OR PENDING" gives no selector for undecidable.

ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: "At least two reviewers with a valid block" measures two independent looks.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `block_ok` is False when any line fails to parse (`findings.py:143-197`; `ledger.py:129`). E2 audit D found 80 reviewer-level silent drops, luna 30 and ember 33 (COMBO-REPORT.md:292). Luna's anchors were verbatim only 91.4% of the time (:294). The default panel is ember plus 2x luna, so the round-1 degrade rate could be high even after D1. `ledger.py:119-121` dedups ids only, so two same-model reviewers count as two blocks. Source-blind reviewers (156 runs, :373) emit valid empty blocks and count. The replay is not told to report the degrade rate.

ID: INV-010
CATEGORY: count_divergence
ASSUMPTION: Canaries cost "25% overhead" and a rerun is an independent second chance.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `build_batches` adds exactly two canaries per batch whatever its size (`stoprule.py:669-673`). The 25% figure holds only for six-claim batches. The singleton-first rollout (M1) means 1 claim plus 2 canaries, which is 200%, and a 7-candidate run has a final batch of 1+2. The canary choice is seeded per batch (`stoprule.py:670-671`), so a rerun likely meets the same canaries. A wrong canary rejects every real claim in the batch (`:826-829`). Two rejects make it `unconfirmed` (`:691`), which is collateral damage under M9.

ID: INV-011
CATEGORY: collection_boundaries
ASSUMPTION: Grading one claim per cluster, then freezing it (M5), is safe once D6 and `same_defect` are "tightened".
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: A v2 cluster exposes one `representative` and `claim` (`cluster.py:338-344,373-374`). A v1 row takes `first["claim"]` from group[0], which depends on reviewer order (`ledger.py:182-199`). `same_defect` treats a shared fp (same section and shared refs) as one defect even if the claims differ (`findings.py:367-372`). A `false` on the representative therefore demotes every member, including a distinct defect, and M5 then freezes it for unchanged text. The cluster's `chained` flag (`cluster.py:324-326`) is not a grading guard. "To be tightened" has no mechanism, test or acceptance number. The D6 fix covers the 83 chained rows only, not two real defects under one fp.

ID: INV-012
CATEGORY: collection_boundaries
ASSUMPTION: Empty inputs (zero valid reviewers, zero candidates) are safe.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: A round with no valid block is refused with the ledger untouched (`ledger.py:150-157`; `test_review_ledger.py:345-373`, read). With zero candidates `range(0, 0, 6)` yields no batch (`stoprule.py:669`), so nothing is graded. Both cases are fine.

ID: INV-013
CATEGORY: collection_boundaries
ASSUMPTION: D2 ("an invalid reviewer never clears a row") is a three-line fix with no side effects.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `ledger.py:254-257` clears absent `resolved_check` rows and never reads `block_ok`. The existing pin `test_review_ledger.py:376-385` (read) asserts `resolved` with one invalid reviewer, so D2 inverts a test; the consensus does not mention this. In a two-reviewer round, a reviewer whose block is always invalid (E2: glm "block ok false", COMBO-REPORT.md:7) would stop any row from clearing. The loop then reaches ESCALATE, and no recovery path is defined.

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: D1 (silent drops), D5 (null spans), M3 (evidence gate), M9 (partial abstains) and M2 (degrade) compose.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Two failure modes. (a) "D1 fixed" is undefined. If the fix persists `rejected_lines[]` and marks the reviewer partial (the A design), a lone reviewer's rejected blocking finding is lost. With two other valid blocks the round still returns a certified PASS, so the veto is bypassed. The parser drops the line and flags the block (`findings.py:188-192`). (b) If the fix instead raises the 200-character limit, the 49 recovered blockers are mostly luna and ember findings (COMBO-REPORT.md:292), the models with the weakest verbatim fidelity (:294). They enter M3's locate gate (`findings.py:276-304`) and are suppressed there. The D1 fix and the M3 gate cancel unless shown otherwise.

ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: Shadow can start now and M4's `spec-v2` can follow later.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `spec-v1` is the live stoprule rubric, with a fail-open default ("Otherwise it is not blocking", `finding-grader.md:17`) and unverified evidence graded as true (`:19`). Shadow data collected before `spec-v2` measures a rubric that will not ship. The `overruled` and `promoted` counts, which M12 relies on, would be about the wrong rubric. The per-claim consequence statement (transcript F4: `findings.py:118` allows 300 characters of claim with no enforced named reader or outcome) must be in the reviewer brief before shadow starts, or B2 stays ungradable. M1-M12 list no ordering.

ID: INV-016
CATEGORY: interaction_effects
ASSUMPTION: M8's "code predicate on `deviation_class` / `reflect_category` (`findings_v2.py:161-162`, `contract.py:377-381`)" is one rule.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The two lines are different rules. `findings_v2.py:155-162` makes any MAJOR or CRITICAL finding with a `reflect_category` blocking, whatever its `deviation_class`. `contract.py:377-381` halts only on regression or drift, and authorized or necessary deviations never halt. `reflect_category` is optional (`findings_v2.py:155-156`), so the predicate needs a fallback. The contract reads `deviation_count_by_class` from the debate and defaults it to 0 when absent (`contract.py:90-101`; `ensemble.py:779-785`). The predicate therefore has no live consumer, and a MAJOR authorized finding would be panel-blocking while the contract passes it.

ID: INV-017
CATEGORY: interaction_effects
ASSUMPTION: M10: two copies of the blocking rule need adapters and a parity test.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: I found at least two more. `diffgate.py:796` has `verdict = "FAIL" if open_blocking else "PASS"` in the installed `sc-diffgate` skill. `stoprule.py:1179-1191` has its own claim-level FAIL rule. `review_ledger.py` in `sc-review-ledger` exists, but I did not confirm its rule. Whether those commands are in scope for the unified core is not stated. If they are out of scope, the parity test cannot cover them.

ID: INV-018
CATEGORY: interaction_effects
ASSUMPTION: A shadow grader "routes nothing" while the veto stays unchanged.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The merged report is read by the next reviewer and the reviser (`ledger.py:408-411`). Its last line is pinned (`splitlines()[-1] == "verdict: PASS"` per transcript F2). A shadow "grader says not blocking" annotation inside it would anchor the next reviewer and the reviser, and the shadow would stop being a shadow. M1 says only "recorded next to the veto". There is no stated rule that shadow data stays out of `render_merged_report`, and no stated rule that a failed shadow batch cannot change the exit code.

ID: INV-019
CATEGORY: sufficiency_challenge
ASSUMPTION: M12 (fix D1/D5/D6 plus the paired replay) alone decides between veto and grader.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier: the pass criterion can be met by a grader that demotes everything. Gates between the fix and the assertion: (1) The control package has 0 known blocking defects (`research/05-blocking-calibration.md:311`), so any demotion lowers its wrong-blocker count. (2) The recall criterion lives on the defect-rich packages, where the veto's real-blocking recall is 0.17-1.20 of 8 per run (COMBO-REPORT rows 315-333, as cited in Round 1), a floor that cannot show loss. (3) The only leniency probe was conceded by B and no harshness probe exists beyond easy canaries (`stoprule.py:673`). (4) No numeric pass threshold appears anywhere in M1-M12. (5) The judge counts novel real finds as wrong blockers (COMBO-REPORT.md:63) and leaked the panel name. A grader that always says `false` passes all five. [Orchestrator note: the line reference `research/05:311` was not borne out; the control-package fact is stated in Variant B R1 and `research/11` §5.]

ID: INV-020
CATEGORY: sufficiency_challenge
ASSUMPTION: The E2 replay can validate M2, M5 and M9 (certification, frozen decisions, clearing).
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier: wrong blockers that arise in rounds 2 and 3. E2 merged each package once ("merged each package with `superclaude review merge`", COMBO-REPORT.md:7; "stale round-1 ledgers", :98). Source-file enumeration of what the replay exercises: `merge_cmd.py:109`, `ledger.py:107-298` (round 1 only), `findings.py` parse and cluster. It does not exercise `apply_revision` (`ledger.py:301-347`), `defer` (`:350-360`), re-found or regressed paths (`:207-238`), or the clear step (`:254-258`). C-006, the one structural advantage B claims over the veto, lives in exactly the code the replay never runs.

ID: INV-021
CATEGORY: sufficiency_challenge
ASSUMPTION: M4 (affirmative demotion with a named criterion) alone fixes the fail-open grader.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier: B2 is ungradable on the replay inputs. v1 findings have no `outcome` field, and the claim is at most 300 characters with no enforced named reader (`findings.py:118`; `document_review_loop_prompts.md:60`; transcript F4). B conceded that a claim-shape check or schema field is required, yet M1-M12 do not list it. Without it, B2 is `undecidable` for many items, M4 keeps the reviewer's flag, and the grader arm collapses toward the veto, so the replay shows no difference. The naming rule is checked only by format (`why` of at most 25 words, `stoprule.py:813`), not by truth. The existing E2 reports cannot test the shipped claim shape.

ID: INV-022
CATEGORY: sufficiency_challenge
ASSUMPTION: The pooled paired replay has power.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Falsifier: the 71 pooled rows are not independent samples. Control is one document with 2 defects and n of 4-6 per panel (COMBO-REPORT.md:239), so the same few spurious clusters repeat across panels. Replaying D1 needs the raw reports, but some rows were merged from stale or replaced reports (n2-terra, r2-sol, n5-sol, n5-terra, :292). The replay population shrinks below 71, and "same candidate sets" breaks wherever D1 changes the set. B's own R1 residual predicts an inconclusive result. Inconclusive keeps the veto live forever, so M12 does not decide.

ID: INV-023
CATEGORY: sufficiency_challenge
ASSUMPTION: Shadow counts (`overruled`, `promoted`, `singleton_blockers`) make the choice checkable after rollout.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier: production loops have no ground truth. `research/05:195` says "No E1 run has ground truth", and synth-04's status for C05 reads "UNDECIDED-BY-EVIDENCE". `overruled` measures disagreement, not who is right. `promoted` precision needs labels that nothing produces. The only weak label in the code is the reviser's `applied` or `rejected` fix map (`ledger.py:330-342`), and the consensus does not name it. Counting disagreement cannot confirm a flip decision.

ID: INV-024
CATEGORY: sufficiency_challenge
ASSUMPTION: M2 (degrade rule) alone resolves "PASS certified on a thin panel".
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier: a consumer that reads only the exit code or decision word. Exit codes stay 0/10/11 (`ledger_cmd.py:13,109`), and `test_review_cli.py:348` asserts exit 0 and PASS. The in-repo consumers of `review merge` and the ledger verdict, from a grep over `src/superclaude` `.py` and `.md` files, are `ledger.py`, `merge_cmd.py` and `document_review_loop_prompts.md`. Only the prompt prose is asked to report "uncertified", so no code enforces the flag. See INV-004 for the inheritance gap. The gate cannot fail mechanically.

ID: INV-025
CATEGORY: sufficiency_challenge
ASSUMPTION: M3 (evidence gate) alone resolves wrong blockers without losing real ones.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Falsifier: the gate's target inputs are the population that fails it. Gate chain from fix to verdict: (a) `findings.py:104` anchor limit, (b) `findings.py:276-304` whitespace-flattened verbatim `locate`, (c) `ledger.py:196` row `span`, (d) `ledger.py:99-104` brief. D5's 13 blocking rows with null spans (46 null in all, per transcript A-003) are by definition failing (b), and D1's recovered long anchors are likely to fail it (COMBO-REPORT.md:294). The v1 path has no re-read resolver (`verify_cmd.py:1` is v2-only, per transcript). So the gate suppresses real blockers permanently, and no input has been shown to pass it.

SUMMARY (fault-finder): 25 findings, 2 ADDRESSED (INV-003 LOW, INV-012 LOW) and 23 UNADDRESSED: 11 HIGH (INV-001, 004, 005, 011, 014, 019, 020, 021, 023, 024, 025), 10 MEDIUM (INV-002, 006, 007, 008, 009, 010, 015, 016, 017, 022) and 2 LOW (INV-013, 018). Not re-read by the fault-finder (taken from the transcript): the exact `test_review_ledger.py:468-472` pin, and `verify_cmd.py:1`. It did not confirm the rule inside `review_ledger.py`.

