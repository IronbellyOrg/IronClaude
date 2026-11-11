# Review of solutions S1, S2, S3 (research report 2) and the planning decisions

Planner review, 2026-11-10. Sources: `$SP/p13/RESEARCH-REPORT-2.md`, Stage 2 (`$SP/p11/`, corrected `STAGE2-REPORT.md`), second baseline audits (`$SP/p12/baseline-audit2/`), the #346 prototypes (`$SP/exp346/.../phase5/final-bundle/builds/`), the product repo at `69ac8b33`, and three coordinator messages (token recount; the owner's tier definitions; the owner's stand-in decision). Every URL and number in the report remains UNVERIFIED; none is repeated here as fact.

## 1. What the baseline residual is made of (drives everything below)

Stage 2 arm 3 (n=6) converged 6/6, but its audits find 1.5 blocking defects per final spec (12 audits: first 2,2,2,2,0,1; second 2,1,2,1,1,2). Using the keyword theme tags of the previous planning round (C9.3; a proxy, to be verified by the implementers), the 9 first-audit blockers split roughly into:

- **about 5 "never found"**: the run's own R1 did not report that theme (T2 in a3-r1, r3, r4; T3 in a3-r2; one other in a3-r4). More or better first reviewers (S1, S3) can remove these.
- **about 4 "found, then survived"**: R1 found the theme, the reviser changed text, the scoped re-review passed, and the audit found the theme again (T1 in a3-r1, r2, r3; T2 in a3-r6). A bigger first-review panel cannot remove these; only a stricter resolution rule (S1's ledger: "resolved" only when the diff touches the offending text, "regressed" when it is found again) or a better reviser can.

Consequence: the report's ADOPT bar for S1 ("median residual 0") is out of reach by recall alone; a halving (1.5 to 0.75) needs the panel to catch nearly all never-found themes AND the ledger to catch some survivors. Each plan pre-registers the decomposition and recomputes it.

## 2. S1: independent panel + deterministic merge + typed ledger (report 3.1, rows 1-2)

**Sound.** Separate fresh contexts, no cross-talk, a deterministic union by fingerprint, overlap as a confidence marker, script-only status changes, fail-closed regressions. Migration step 1 (merge with the single reviewer as input, no behavior change) is a free offline test: PN1 replays the six baseline runs through the ledger with hand-made findings blocks and must reproduce their verdicts.

**Wrong, circular or unmeasurable in the report, and what the plan does instead.**
- "Extend the existing ledger script" / "the same schema the diffgate already parses": nothing of the kind exists in the product repo at `69ac8b33` (no `superclaude review`, no ledger, no diffgate). They exist only as #346 prototypes in the scratchpad (2,668- and 1,740-line scripts). PN1 creates the minimum (one package `src/superclaude/cli/review/`), reusing only ideas: verbatim anchor quotes located with whitespace-flattened matching, and a fenced machine block.
- "Two reviewers from different model families": impossible here; the owner's production panel is 2x Tier 3 + 1x Tier 2 + 1x Tier 1b, and in this environment the owner set Haiku 5.5 as the stand-in for all three non-anchor slots. The live panel is therefore 1 sonnet + 3 haiku. The three haiku reviewers are the SAME model: their only independence is separate fresh contexts (no shared transcript). Correlated blindness is a known limit of this environment, not something the experiment can rule out.
- "Token cost <= 2x current, still below the old 1.25M baseline": the 1.25M figure was double-counted; the recount (each message id once) gives arm 1 ~0.56M and arm 3 ~0.17M per replicate. All token rules are now ratios to the recounted `B_TOK`. With the panel on the first review only (coordinator instruction; re-reviews keep the sonnet anchor) the expected ratio is about 1.9, so the report's 2x bound is kept as a pre-registered ADOPT condition (`R_TOK <= 2.0`), and `R_TOK > 3.3` (arm-1 cost level) is a DROP.
- "Median residual 0 with lower quartile 0": kept as a reported criterion, not the decision rule; with single-audit noise (a3-r5's PASS did not repeat on a second audit) a median of 0 over 6 runs is not a reliable signal. The decision uses the mean over two audits per final spec (12 audits).
- Step 4 (route overlap findings past the grader): there is no separate grader in arm 3, so it is out of scope.
- Fingerprint drift (the report's own risk): the fingerprint is section + normalized requirement ids (not the quote), and matching also accepts anchor spans within 3 lines with shared ids (pr-review-core's positional tolerance idea, cited by the report, UNVERIFIED). "The diff removes the offending text" is made mechanical as "a hunk of the revision touches the anchor span or the second anchor span" (a contradiction is often fixed on its other side).
- Re-reviews are scoped. A survivor is caught only if the single re-reviewer re-finds it. The ledger cannot help with survivors nobody re-reports; RESULTS.md must say how many survivors the ledger caught.

## 3. S2: mechanical pre-check suite (report 3.2, row 3)

**Sound.** Deterministic, stdlib-only, zero tokens, informational first; the over-linting risk is the right one to fear (the original setup's over-blocking).

**Wrong or unmeasurable.** "12 clean final documents" and "3 originals" do not exist: none of the real specs is clean (10 of the 12 converged finals failed their first audit), there is one original plus three reference snapshots of an older loop, and the only clean documents are two small synthetic ones (`$SP/p5/docs/clean.md`, `minor.md`). "FP rate 0 on the 12 clean docs" is therefore replaced by (a) zero flags on the two clean synthetic documents and (b) mechanical precision measured by adjudicating every flag on all real documents (is the stated inconsistency really in the text, quoted on both sides). Recall is measured against the recurring audit themes: a count check can reach T1, a path-template check T2, a phase-order check (an acceptance check of phase k that depends on something introduced in a later phase) T3. If no check reaches any theme, the live phase is not run (gate G1); the lint can still be adopted as an informational tool on precision alone.

## 4. S3: capture-recapture stop rule (Part C)

**Sound.** The estimators are standard for human inspections (report grade A; UNVERIFIED citations), and the data for a first test exists: 12 same-instrument first reviews (arms 2-3) plus 3 different-instrument ones (arm 1) of the same original spec.

**Wrong or circular in the report's falsification test.** "Compute LP/Chao2 on reviewer pairs and correlate the predicted remaining defects with each run's audit residual" does not test the estimator: each run has ONE first reviewer, so a per-run estimate needs reviewers from other runs, the resulting `N_hat` is almost the same for every run, and the per-run prediction then varies only with how many defects the run fixed. PN3 keeps that test as a secondary (F2) and adds a held-out prediction test (F1): estimate from k of the 12 occasions, check against everything later found by the other occasions and the 21 audits (mapped back to the original by quotes). Further problems built into the plan: (i) the "truth" is the same kind of review as the occasions; (ii) 12 sonnet reviews with one prompt are positively correlated, and the 1 sonnet + 3 haiku live panel even more so (three copies of one model), so estimates are lower bounds and underestimation (Runeson et al., report-cited) is expected; (iii) only whole-document reviews of one version are valid occasions, scoped re-reviews are not, so a live stop rule needs extra whole-document panel rounds, which costs about 3.3x baseline and will likely push runs into ESCALATE at the cap of 3. That is why the live arm is gated twice (F1 SUPPORTED, and calibration on PN1's live panel data, which is free).

## 5. Interactions and how the three branches merge

- S1 and S3 share the panel, the findings block, the fingerprint, the ledger and telemetry. Ownership is split to keep merges clean: PN1 owns all shared product modules; PN3 owns only the estimator and consumes C6/C7 file formats; PN3's live harness reimplements the contract's ledger rules outside the product (experiment code only). PN2 is orthogonal (a lint could later feed the panel's reviewers).
- S3's falsification on live panel data is free: PN1's six round-1 panels give 24 new capture occasions (6 runs x 4) with audits; PN3's shadow script reads them.
- The defect catalog (C9.4) is built once, by PN3 Phase O1 (it is PN3's core work), and read by PN1/PN2 analyses if present; otherwise they fall back to theme-level truth and say so.
- Merge safety: the three branches add `src/superclaude/cli/review/__init__.py` and the `main.py` registration with identical bytes (identical hunks merge cleanly), own disjoint module files, and edit the rules file at non-adjacent insertion points (PN2 after the `review: 1 of 3` line and after "Follow the re-review core"; PN1 after the three brief lines and before `## Never`; PN3 none). Recommended merge order if adopted: PN1, PN2, PN3.

## 6. Owner requirements (Part D and the 2026-11-10 decisions) and where they land

| Requirement | Where |
|---|---|
| Tiers are aliases for ordered model lists, first = default, rest = fallbacks; lists are data | C2 `review-tiers.default.json` (`aliases`), owner's exact lists with the MODEL-TIERS gateway ids |
| Slot = alias + strategy (`fixed`, `random` with seed, `round_robin`); pure resolution with fallback depth | C1, C3 (`resolve_slot` pure function; required tests include fallback at depth 1 and 2 and stand-in resolution) |
| Production panel 2x Tier 3 + 1x Tier 2 + 1x Tier 1b, Tier 1b fixed anchor | C1 default template |
| Central default + project/user override; adding a model is a data edit | C1/C2 lookup precedence; tests add a model by data only |
| This environment: Tier 1b = sonnet (the Stage 2 reviewer); Tier 2 and Tier 3 = haiku stand-ins | C2 environment `anthropic-only` (`stand_ins`), records `stand_in: true` |
| Telemetry per reviewer run (task variables, outputs, cost, outcomes, derived scores), git-pushed directory, append-only, SQLite loader | C8; PN1 builds writer/loader; PN3's live harness writes the same schema |

## 7. Threats to validity (all plans)

1. **Audit noise.** Single audits disagree (a3-r5 PASS then FAIL). Two frozen audits per final spec; decisions use means over 12 audits per arm; INCONCLUSIVE when the AUD and AUD2 arm means differ by more than 0.75.
2. **Correlated blindness.** One vendor here; 3 of 4 panel reviewers are one model. Measured (haiku-haiku versus sonnet-haiku overlap; per-cluster capture profiles), never assumed away. Results do not transfer to real Tier 2/Tier 3 models; stand-in telemetry is flagged.
3. **Panel size confounded with model mix.** No extra arm; separated by per-reviewer attribution, leave-one-out unions, same-model counterfactuals built from the 12 baseline sonnet R1s, and the anchor-only comparison.
4. **The gate and the audit are the same kind of review.** The audit is a sonnet first review with the same FIRST-REVIEW prompt as the panel's anchor, so designs that add sonnet-like reviewing look better to it. An independent blind adjudicator (`fable`, outside the panel) is added in PN1 for precision, itself an LLM.
5. **Prompt change confound.** The findings-block line changes the reviewer prompt in S1/S3; the anchor check (sonnet in the panel versus the 12 baseline sonnet R1s) measures this.
6. **Drift since Stage 2.** Same commit, but served models may have changed; the anchor check doubles as a drift check.
7. **Small n, coarse truth.** n=6 per arm; theme tags are a keyword proxy; the catalog's dedupe is partly LLM-judged (overrides recorded with quotes; sensitivity without overrides reported).
8. **Coordinator realism.** The harness script plays the coordinator; whether a real `/sc:spec-panel` coordinator follows the new rules-file sections (running `superclaude review ...`) is not tested here.
9. **Sandbox evidence.** Repo-path citations in the sandbox are UNVERIFIED by design (Stage 2 had the same limit).

## 8. Decisions taken

1. Each plan is self-contained and embeds SHARED-CONTRACT.md verbatim; product code lives in one package with disjoint files per plan.
2. Every token figure uses the recount (each message id once); token rules are ratios to the recomputed `B_TOK`; harnesses reproduce per-run baseline totals within 1% as a test.
3. Every test-arm final spec gets the frozen audit twice; `B_BLK` = 1.50 over 12 baseline audits.
4. Offline phases first: PN1 replay + same-model union curves; PN2 full lint measurement; PN3 catalog + F1/F2. Live phases only behind pre-registered gates.
5. Panel on the first review only; re-reviews by the sonnet anchor (cost, and scoped re-reviews are not valid capture occasions).
6. S3's live arm depends on S1's live data (shadow calibration) and on F1; recommended to run only after PN1's live phase.
