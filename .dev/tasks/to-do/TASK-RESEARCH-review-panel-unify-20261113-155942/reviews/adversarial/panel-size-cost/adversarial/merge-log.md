# Merge Execution Log

## Metadata

- **Base:** Variant B (Proposal B, Option B: fix the rubric first, keep the cap at 3, decide the count after H-A), `adversarial/variant-2-original.md`
- **Non-base source:** Variant A (Proposal A, two reviewers by default), `adversarial/variant-1-original.md`
- **Plan:** `adversarial/refactor-plan.md` (Changes 1-14, Change 15 and Amendments A-1..A-15; the amendments are binding)
- **Executor:** merge-executor agent
- **Changes applied:** 15 of 15 (failed 0, skipped 0); amendments A-1..A-15: 15 applied (A-2 is Change 15, applied once and logged under both)
- **Status:** success, with the notes listed under Summary (no plan item was skipped; two readings and one count discrepancy are flagged for the orchestrator)
- **Timestamp:** 2026-11-14
- **Output:** `proposal-merged.md` (merged proposal) and this file
- **Selection record:** base B won by 0.0061 (A 0.9194, B 0.9256), inside the 5 percent band, via tiebreaker level 1 (debate points won, B 6 to A 4); B stays ahead in every sensitivity case in `base-selection.md`. The advocates' Round 2 consensus favoured an "A-min" base (a narrowed Proposal A); the protocol chose B by score, so the merged document keeps B's structure and carries A-min as Decision D-1. This tension is recorded here and in the merged file's last section.
- **Inputs read in full:** `variant-2-original.md`, `variant-1-original.md`, `refactor-plan.md`, `base-selection.md`, `debate-transcript.md`, `invariant-probe.md` (with its CORRECTION on probe-artifact presence), `diff-analysis.md`.
- **Repository spot checks (read-only, all matched the plan):** `SKILL.md:86` (default 3), `:318` (D2), `:340`, `:654-659` (the "restore N=3" sentence is at `:658`), `:695`; `task-builder/SKILL.md:2217-2236`; `manifest.py:314-315`; `scripts/reflect_shadow_exit.py:244-245`. No difference from the plan was found.

## Changes Applied

Line numbers refer to `proposal-merged.md` as finished.

### Change 1: Correct the escalation figure everywhere in the base
- **Status:** Applied
- **Source:** refactor-plan Change 1 (debate C-002, X-001, X-004)
- **Target:** base E-5, "weakest point", R1, R9, Cost "What B saves" and "Where B sits", and (A-1) base Correctness section 1
- **Before (brief):** E-5 said the flag was the only reason in 1 run for certain and at most 5 of 39, with a clear-cut row-8 run; R1 carried a 13 percent exposure; Cost counted 1 to 5 avoidable Tier 2 runs
- **After (brief):** E-5 keeps the 39/38/35/34 table and adds the column "Also fails a Tier 1 stop by" (row 4, row 6, row 5; the row-8 run via calibrated C 0.68; the row-0 run via row 4; the three no-row runs resolved 2 of 3); one figure statement (lines 20 and 144) with all three caveats and the five ambiguous runs and how each resolves; R1 and Correctness 1 restated on "at most 1 of 39"; Cost paragraphs replaced
- **Provenance tag:** `<!-- Source: Base (original, modified) - E-5 recount rewritten ... / Change 1, A-1 -->` before E-5
- **Validation:** forbidden-phrase greps return 0 (see Post-Merge Validation); table totals 18+9+2+1+1+3+1+4 = 39

### Change 2: Recast E-6 as an observation about the probe
- **Status:** Applied
- **Source:** refactor-plan Change 2 (debate C-012, A-003); run files as cited in the plan
- **Target:** base E-6 and "weakest point" consequence 1
- **Before (brief):** E-6 called the `fixTheScIssueWor` run the one clear-cut flag-only counterexample
- **After (brief):** E-6 keeps the file names and the M-13 content, adds the run's own `reflection-card.yaml` (self-reported 0.90, calibrated C 0.68, delta -0.22, so row 6 fires), states that the Round 2.5 invariant probe (INV-001 of that run), not a reviewer or the flag, found M-13, and that this is one run; the words "clear-cut" and "counterexample" are gone
- **Provenance tag:** `<!-- Source: Round 2 rebuttal (advocate A and advocate B) - E-6 recast ... / Change 2, A-003 -->`
- **Validation:** grep for "clear-cut" and "clear cut" returns 0

### Change 3: Demote Phase 1 to a conditional item
- **Status:** Applied
- **Source:** refactor-plan Change 3 (debate X-003, C-001); base G1 text
- **Target:** base "The three phases", Gate G1, Phase 1 cost row, tests N3 and N4; (A-1) Design rows, data-flow steps 2-4, Correctness 1, 2, 4, risks R1, R2, R4, R5, cost rows
- **Before (brief):** committed three-phase plan with Phase 1 (flag advisory) behind G1
- **After (brief):** "Staging" with Step A, Step B and Step C; the flag change moved to a new H2 "Conditional items", item CI-1, with its edit sites, bound, case, reopen trigger and tests N3 and N4; data-flow steps 2-4 no longer change the flag; R1 and R2 marked CI-1 only
- **Provenance tag:** `<!-- Source: Base (original, modified) - base "Phase 1", Gate G1 and tests N3 and N4 demoted ... / Change 3, A-1, A-8, A-13 -->`
- **Validation:** "Phase 1" appears in 3 lines (339 tag comment, 342 CI-1 heading, 346 rationale), all naming the base draft's Phase 1 as demoted, none as committed scope. I renamed the stages to Step A/B/C so "Phase 1" does not label committed scope. If a mechanical grep for "Phase 1" must return 0, these three mentions can be reworded without loss.

### Change 4: Replace Phase 0 retrospective replay with prospective keys plus a recompute check
- **Status:** Applied
- **Source:** refactor-plan Change 4 and A-4 (debate Round 2 A and B; probe INV-013)
- **Target:** base "Contract and audit fields", "CLI surface", tests N1 and N2, Phase 0 cost row
- **Before (brief):** `sparse_flag_decisive` and `escalation_path` keys plus read-only `scripts/reflect_tier_replay.py`; N2 asserted counts of 5 and 1
- **After (brief):** keys `matching_rows`, `calibrated_C_t1`, `S_domains_basis`, `tier_without_flag` added, B's two keys kept (A-4); recompute check proposed as `scripts/reflect_tier_recompute.py` beside `reflect_shadow_exit.py`, reading the card, `t1-card.md` and `input-snapshot.yaml` in the order A-4 gives, "not evaluable" otherwise; N1 and N2 replaced with the A-4 fixtures and the skip-if-absent real-history test (39 files, 38 Tier 2, 35 flagged, 34 flagged and Tier 2; `fixTheScIssueWor` not decisive)
- **Provenance tag:** `<!-- Source: Base (original, modified) - field table ... / Changes 3, 4, 9, A-4, A-8, A-13 -->` and `... CLI surface ... / Change 4, A-4 -->`
- **Validation:** all key names and the script name carry `[PROPOSED]`. The plan gives no command-line arguments for the script, so none were invented; the text says only that it runs with `uv run python`.

### Change 5: Replace the "count must wait" premise with an owner-gated reviewer default
- **Status:** Applied
- **Source:** refactor-plan Change 5 (variant A Design, Round 2 "A-min"; debate C-001, C-014, C-011)
- **Target:** base "What the design decides" row "Default reviewer count" and "Count decision"; (A-1) base title, "One-sentence position", Correctness 3 and 5, R8, "What B costs by waiting"
- **Before (brief):** "Do not touch the reviewer count now"; count stays 3 until H-A
- **After (brief):** new H1 (no "Do not touch" or "decide the count after H-A"); rewritten one-sentence position; D-1 as a new H2 after Correctness argument with change list, eight conditions, saving counted in calls on roughly 26 of 38 runs; Correctness 3 and 5 rewritten (9 of 38 runs already ran two cards); R8 and the cost-of-waiting paragraph rewritten; engine default, clamp and exit gate explicitly unchanged
- **Provenance tag:** `<!-- Source: Variant A (Proposal A), Design and Round 2 "A-min" - merged per Change 5; new H2 ... per A-13 -->`
- **Validation:** greps for "count must wait", "Do not touch the reviewer count now", "decide the count after H-A" and "stays 3" return 0 in the final file. Note: the plan's overall risk label is applied as "Medium, with one High item (D-1)".

### Change 6: Coupled-edit checklist and the shadow pin as conditions of D-1
- **Status:** Applied
- **Source:** refactor-plan Change 6 and A-5 (Round 2 B verification (a); probe INV-001, INV-004)
- **Target:** new subsection of D-1 "Every place that states the count"
- **After (brief):** table with a "What it says today" and an Action column (EDIT, KEEP, one Reference for D2 at `SKILL.md:318`); condition 1 (conditional shadow default "default 2; 3 when the effective engine is shadow", evaluated at Wave 3A after D2, plus `SKILL.md:340`); condition 2 (one drift-pin test)
- **Provenance tag:** `<!-- Source: Round 2 rebuttal (advocate B), verification (a); probe INV-001, INV-004 - Change 6, A-5 -->`
- **Validation:** citations match A-5 (`models.py` path corrected to `src/superclaude/cli/reflect/models.py:91-92`; `:658` named for the "restore N=3" sentence; `refs/reviewer-spec.md:55` not `:55-57`). **Discrepancy flagged:** the plan says "about nine edits in five files" for the EDIT rows. The table lists 16 EDIT sites in those five files (SKILL.md 8, input-resolution 2, reviewer-spec 3, reflect.md 2, task-builder 1). I kept the plan's wording and added no explanation; some sites may share one edit, but this is not stated in the inputs. The plan's "about 21 sites in 9 files" matches (21 sites excluding D2).

### Change 7: Name the task-builder default POST gate as a blocking consumer and decide it
- **Status:** Applied
- **Source:** refactor-plan Change 7 and A-1, A-11 (probe INV-012)
- **Target:** base E-9; Correctness 4; consumer rows; D-1
- **After (brief):** E-9 lists advisory, blocking engine path, human-gated and blocking skill path (task-builder) consumers; Design consumer table has a new row for the task-builder gate and rows for the user-run gate; D-1 subsection with options (a) and (b); Correctness 4 replaced
- **Provenance tag:** `<!-- Source: invariant-probe INV-012 - Change 7, A-11 -->` and the modified-base tags on E-9 and the consumer table
- **Validation:** repo spot check confirmed `task-builder/SKILL.md:2217-2236`. I also quote the invocation (`:2225`) and the HALT rule (`:2227`) from my own read; these are not in the plan and are marked "re-read for this merge".

### Change 8: Rollback tripwire on observable proxies
- **Status:** Applied
- **Source:** refactor-plan Change 8 and A-3, A-8 (Round 2 A and B; probe INV-009)
- **Target:** D-1 "Rollback" and base Risks
- **After (brief):** revert path; why panel fields cannot be used (14 manifests against 91 `pre-*` directories; shadow pinned at 3); proxies (`single-reviewer-fallback`, `len(reviewer_cards)`, convergence, probe presence over both paths); suggested start labelled `[PROPOSED]` and owner parameter; the shortfall half catches about 20 percent or more at n=30 (P about 0.35 at a true 10 percent); accrual about four months
- **Provenance tag:** `<!-- Source: Round 2 rebuttal (advocate A and advocate B QUALIFY); probe INV-009 - Change 8, A-3, A-8 -->`
- **Validation:** only the corrected probe counts (20 of 23 and 5 of 6) are used; the withdrawn counts appear nowhere in the file

### Change 9: Record requested, resolved and source separately; add strata
- **Status:** Applied
- **Source:** refactor-plan Change 9 and A-13 (probe INV-002, INV-010; variant A telemetry)
- **Target:** base "Contract and audit fields"
- **After (brief):** `reviewers_requested`, `reviewers_resolved`, `reviewers_source: default|flag|enterprise|shadow-pin|clamp` under `telemetry:` in the contract (precedent `SKILL.md:349`, `:469`), replacing A's single boolean (the three failure cases are stated); `executor_exclusion_degraded`, `anchor_replaced`, `depth`, `calibrator_diversity` as strata; rubric keys stay in `tier_decision.yaml`
- **Provenance tag:** as Change 4 (the field table tag cites Change 9)
- **Validation:** the `reviewers_source` enumeration is labelled `[PROPOSED]` (A-8). A's second new key `panel_shortfall` is not carried: the plan does not list it, and the merged text names only the existing `panel_shortfall_2_of_3` label as a site to edit.

### Change 10: Symmetric pre-registered count rule and the pilot's limits
- **Status:** Applied
- **Source:** refactor-plan Change 10 and A-9 (Round 2 A and B)
- **Target:** base "Count decision"
- **After (brief):** arms Tier 1, Tier 2 with two (`--reviewers 2`) and Tier 2 with three (`--reviewers 3`), each pinned; margin, minimum n and cost measure are owner parameters; inconclusive outcome stated in advance (incumbent stays); steps 2 and 3 of the base rule kept as the plan's A-9 requires (H-A fails: owner chooses between shrinking to two and tuning the rubric, MR:527; cap above 3 closed unless H-A passes, MR:289); pilot cost figures kept (1.30M to 2.62M, grading unpriced, no owner, G-59); the 10-point margin quoted per A-9 as "the advocate's own invention"
- **Provenance tag:** `<!-- Source: Round 2 rebuttal (advocate A and advocate B) - Change 10, A-9; base steps 2 and 3 kept -->`
- **Validation:** the formal wording of the two-way rule (two replaces three if within the margin and cheaper; three replaces two if better by more than the margin; otherwise the incumbent stays) is my rendering of "symmetric, owner-set margin, inconclusive means incumbent stays"; it is labelled `[PROPOSED]`. The power of a 6-plan arm is carried as `[UNVERIFIED]` because the debate marks it so.

### Change 11: Invariants-preserved table and the "does not claim" list
- **Status:** Applied
- **Source:** refactor-plan Change 11 and A-10 (variant A Correctness sections 1 and 3)
- **Target:** base "Correctness argument"
- **After (brief):** seven-row table (anchor never dropped; executor class is not a reviewer class; T2 stays T2; a Regression is debated by at least two reviewers; contract 1.8.0 stable keys; cap of three; failure is closed), each row with file:line and a "Verified for" column; the four "does not claim" items
- **Provenance tag:** `<!-- Source: Variant A (Proposal A), Correctness section 1 - merged per Change 11 ... -->` and `... Correctness section 3 - merged per Change 11, A-10 -->`
- **Validation:** the plan names the column values "resolver / legacy skill path / not verified". Rows backed by the code engine (`ensemble.py`, `contract.py`) are labelled "Code engine" in the cell; I defined "Resolver" in the legend as the code in `panel.py` and the code engine. Each cell says only what the inputs support. Variant A's 2x2 decision table was not carried (it is not in the plan, and its cells used the retracted figures).

### Change 12: Calibrator disjointness, spec-body single point of failure and the probe-presence gap
- **Status:** Applied
- **Source:** refactor-plan Change 12 and A-3, A-14 (Round 2 A and B; probe INV-003, INV-006, INV-008)
- **Target:** D-1 "Evidence" and "What this does not show"
- **After (brief):** E-21 (calibrator disjointness with both counts and both sources: 23 of 26 `degraded` per advocate A, 22 of 25 tagged per advocate B, two-card 6 of 8 `full` on both; guarantee argument, not recall; opus-executor collision), E-22 (spec body reaches the `qa` persona only, cited at `refs/reviewer-spec.md:55`), E-23 (probe presence 20 of 23 against 5 of 6 over both paths; no gap claimed); a fourth reviewer class listed as an open alternative (owner decision 8)
- **Provenance tag:** `<!-- Source: Round 2 rebuttal (advocate A new evidence; advocate B verifications c, d, e) - Changes 5, 12, A-3, A-14; numbering continues ... -->`
- **Validation:** greps for the withdrawn probe counts return 0

### Change 13: N=2 test list and the failure modes only a pilot can detect
- **Status:** Applied
- **Source:** refactor-plan Change 13 and A-15 (variant A test section; Round 2 A and B; probe INV-014)
- **Target:** base "Test coverage needed"
- **After (brief):** two tables, automated (N1, N2 replacement tests; N7 N=2 mirror of `test_i5`; N8 EV-1 test; N9 drift pin; N10 post-hoc lint; N11 skill-text pin) and measurement only (N5, N6, M1-M5, with the INV-014 residual in M2); a note that the pins test prose, not model behaviour (A-007); N3 and N4 pointed to CI-1
- **Provenance tag:** `<!-- Source: Round 2 rebuttal (advocates A and B) and Variant A test section - Change 13, A-4 -->` and `... Variant A (Proposal A), test section; Round 2 - Change 13, A-15 -->`
- **Validation:** the new ids N7-N11 and M1-M5 are mine (the plan lists the tests without ids); each is defined in a table row and referenced from elsewhere only as defined

### Change 14: "Open decisions and unresolved conflicts" section
- **Status:** Applied
- **Source:** refactor-plan Change 14 and A-13, A-15
- **Target:** new final H2
- **After (brief):** convergence status, then table 1 (six UNRESOLVED points with both advocates' final positions), table 2 (ten UNADDRESSED invariants, HIGH first: INV-009, INV-012, INV-013, then INV-001, -002, -004, -006, -008, -010, -011; each row names the change that records a mitigation and states it is not a resolution), table 3 (owner decisions, eight rows), and a fourth table "Considered and not carried"
- **Provenance tag:** `<!-- Source: Round 2 rebuttal ...; debate-transcript Scoring Matrix and Convergence Assessment; invariant-probe; base-selection - Change 14, A-13, A-15 -->`
- **Validation:** see Open-item coverage. The fourth table is an addition drawn from the plan's "Changes NOT Being Made" section; it contains no figure that the figure rule forbids.

### Change 15 (= A-2): Floor rule and re-dispatch as a D-1 risk item
- **Status:** Applied
- **Source:** refactor-plan Change 15 / A-2 (U-002, C-004)
- **Target:** D-1 subsection "Floor rule and one bounded re-dispatch (risk item)"; Risks RD-1
- **After (brief):** with two reviewers one failed or invalid card leaves one and is DEGRADED (`contract.py:278-296`; engine exit 11, `test_ensemble_stub_integration.py:251-277`); with three a 2-of-3 shortfall stays PASS-eligible (`test_verdict_mapping.py:572-580`); `ember + terra` -1.75 found, p 0.029 (`CR:294`, `CR:298`); prose-only bounded re-dispatch (existing re-ask at `SKILL.md:343`), labelled prose because shadow13 and shadow15 skipped a stated step; anchor on sonnet (0 of 15 blocks dropped, `CR:427`); tests N7 and N8
- **Provenance tag:** `<!-- Source: Variant A (Proposal A), R2 and Round 2 - Change 15, A-2 -->`
- **Validation:** matches A-2 line for line; "variant A R2" is spelled out as a pointer to `adversarial/variant-1-original.md` because the merged file has its own risk ids

## Amendments

### A-1 (finding 1): complete the target lists
- **Status:** Applied
- **Source:** refactor-plan A-1
- **Target:** Changes 1, 3, 5, 7 additional targets; final executor check
- **After (brief):** every listed additional target was rewritten (Correctness 1-5 replaced, Design rows, data-flow steps 2-4, R1, R2, R4, R5, R8, cost rows, title, one-sentence position, consumer rows)
- **Provenance tag:** each rewritten block carries a "Base (original, modified)" tag naming the change and A-1
- **Validation:** the executor check passes: no "at most 5", "13 percent", "1 certain", "clear-cut", "count must wait" or "stays 3" (all 0); "Phase 1" appears only as the name of the demoted item (3 lines, see Change 3)

### A-2 (finding 2): see Change 15 above. Status: Applied.

### A-3 (finding 3): probe-presence correction
- **Status:** Applied
- **Target:** Change 8 proxy text and Change 12 argument
- **After (brief):** only 20 of 23 and 5 of 6 (both paths) are cited; the one two-card run with no probe, `closeIronbellyOr-20261104084538`, is named with its missing reviewer-2 card; INV-008 stays UNADDRESSED MEDIUM on its structural point (the "<10% diff" skip rule)
- **Validation:** grep for "0 of 6" and "13 of 23" returns 0

### A-4 (finding 4): specify Change 4 fully
- **Status:** Applied
- **After (brief):** inputs in the order the amendment gives (card `C` or `t1-calibration.yaml`; `t1-card.md`; `input-snapshot.yaml`; else "not evaluable"; existing key variants 1, 2 and 5 files); proposed script name; replacement tests N1 and N2; B's two keys kept and `tier_without_flag` derived from them; key names `[PROPOSED]`
- **Validation:** matches the amendment text

### A-5 (finding 5): Change 6 site table: action column and corrected citations
- **Status:** Applied
- **After (brief):** action column; `:658` for the "restore N=3" sentence; `models.py` path corrected; D2 at `SKILL.md:318`; `refs/reviewer-spec.md:55` cited (grep for `:55-57` returns 0); the "about nine edits in five files" count scoped to EDIT rows, "about 21 sites in 9 files" stated
- **Validation:** see the discrepancy flagged under Change 6

### A-6 (finding 6): carry the strongest counter-evidence into D-1
- **Status:** Applied
- **After (brief):** "What cuts against D-1" lists CA-1 to CA-4 (A's C1 to C4), CA-5 (A's C5 and the base's "if H-A fails" argument) and CA-6 (A's R5, including "D-1 should not ship ahead of the shadow path recording the served model", condition 7); the weakest-point section is rewritten as D-1's bet and says G1 is no longer the weakest point
- **Validation:** **Reading flagged:** the amendment lists "the pre-filter is not the driver" among A's C1-C5 as counter-evidence. A's own C5 claimed the pre-filter IS the driver, which the recount refutes. I carried C5 in CA-5 as a withdrawn point (the recount) together with the base's argument that if H-A fails the whole Tier 2 spend is in question, which is the real counter-evidence in that slot. The orchestrator should confirm this reading.

### A-7 (finding 7): preserved from the base unchanged
- **Status:** Applied (verified by reading)
- **After (brief):** kept: E-8 (extended only with "nothing pins the default text either"), the exposure map (extended by Change 7), weakest-point-first placement, the recount method, R9, E-1 to E-4, E-9 and E-10 (E-9 corrected, E-10 gains one sentence on D-1), the citation forms (extended with a glossary of ids) and the tag legend (extended with `[PROPOSED]` and "owner parameter")

### A-8 (finding 8): label invented items
- **Status:** Applied
- **After (brief):** `[PROPOSED]` or "owner parameter" on: the CI-1 reopen trigger (three runs where `tier_without_flag` is 1; the redundant C clause dropped; G1's "none shows a Tier 2-only blocker" half retained); the Change 4 key names and script name; the Change 9 enumeration; the Change 8 numbers; the symmetric count rule wording and margin

### A-9 (finding 9): Change 10 wording
- **Status:** Applied
- **After (brief):** "the advocate's own invention" quoted with its source (`debate-transcript.md`, Round 1 concessions); B's steps 2 and 3 kept; only the margin and arms replaced

### A-10 (finding 10): Change 11 "does not claim" list
- **Status:** Applied
- **After (brief):** the four items from `variant-1-original.md:139-142` (not as good as three; not a third of a run, with the `ember + sonnet` 142,967 against 138,551 figures; pre-filter not judged; stale "sonnet alone" line not used)

### A-11 (finding 11): recommendation inside D-1
- **Status:** Applied
- **After (brief):** option (a) recommended for the task-builder POST gate, with the consistency argument; option (b) listed. The Status block labels D-1 itself "Proposed for the owner's decision (not adopted)", and only option (a) is labelled "Recommended", because the plan says to present D-1 for the owner and recommends only (a).

### A-12 (finding 12): wording
- **Status:** Applied
- **After (brief):** "Adds no code" has no counterpart in the merged text; the Risks section opens with "Overall risk: Medium, with one High item (D-1)"

### A-13 (finding 13): placement
- **Status:** Applied
- **After (brief):** Change 9 fields placed as the amendment says; the H2 sections "Decision D-1" (with Rollback, Evidence, What cuts against, What this does not show plus other subsections) and "Conditional items" sit after "Correctness argument", and "Open decisions and unresolved conflicts" is last; B's seven H2 sections keep their order
- **Validation:** see Structural Integrity

### A-14 (finding 14): label the calibrator counts
- **Status:** Applied
- **After (brief):** both counts and both sources in E-21, the shared "one run carries both tags" note, two-card 6 of 8 `full` on both counts, and the statement that this is a guarantee argument, not a recall argument

### A-15: items missing or weak in the coverage check
- **Status:** Applied
- **After (brief):** A-001 (representativeness), A-002 (no trade-off threshold) and A-008 (E2 does not transfer) in "What this does not show"; the INV-014 residual in M2 of the measurement-only table; Change 14 table 1 positions exactly as the amendment gives them (S-002 A MERGE 55 / B V1 60; S-006 A V1 60 / B MERGE 60; C-003 A MERGE 55 / B V2 60; C-010 A MERGE 75 / B V2 65; C-013 A V1 70 / B MERGE 55; C-016 A MERGE 85 / B V2 60)

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: 1 H1, 10 H2, 35 H3, no H4; the first heading after the H1 is an H2; every H3 sits under an H2; no orphan subsections.
- Section order: B's seven H2 sections appear in B's order (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost). "Decision D-1" and "Conditional items" sit between Correctness argument and Risks and mitigations (A-13); "Open decisions and unresolved conflicts" is last.
- H1 rewritten: "Merged proposal for C14 (panel size versus cost): corrected cost attribution, instrumentation first, and an owner-gated skill-path default of two reviewers (Decision D-1)". It does not commit to "do not touch the reviewer count" or to deciding the count after H-A.
- Provenance: the three header comments are the first three lines. 48 `<!-- Source: ... -->` tags; an awk pass found a Source tag within the two lines before every H2 (0 untagged H2 sections). Every changed block also carries its own tag naming the change.
- Line count: `proposal-merged.md` 543 lines; this log 281 lines.
- Characters: no emojis, no em or en dashes; the only non-ASCII character is the section sign used by the base text (37 occurrences).

### Internal References
Checked with grep over the finished file.
- Evidence ids E-1 to E-25: all defined (E-1 to E-18 in the Evidence section, E-19 to E-25 in "Evidence for D-1", which says its numbering continues) and all referenced ids resolve.
- CA-1 to CA-6, N1 to N11 and M1 to M5, CI-1, D-1 conditions 1 to 8, Steps A, B and C: defined where referenced.
- Risk ids: R1 to R9 (base) and RD-1 to RD-5 (D-1). **Fixed during validation:** the first draft called the D-1 risks R10 to R14, which collided with research files R11 and R13 cited as `R11 §12` and `R13 line 295`; they were renamed RD-1 to RD-5 and every reference (three in the invariant table, two comment tags) was updated, and the citation-forms paragraph states the id convention.
- Ids that point outside the file (INV-nnn, S/C/X-nnn, A-nnn, "Change N", `R04`-style research files, `CR`, `PD`, `MR`) are defined in the citation-forms paragraph and point to `adversarial/` artifacts. **Fixed during validation:** `A-nnn`, `S-nnn`/`C-nnn`/`X-nnn` and "Change N" were first used without a definition; the glossary was added. Two pointers to Proposal A's own risk ids ("A's R2", "its C5") were spelled out as pointers to `adversarial/variant-1-original.md`.
- "See X" targets: "Open decisions and unresolved conflicts", "Count decision", "CLI surface", "Rollback", "Test coverage needed", "Conditional items", "D-1 'Parked for later'", "the owner decisions", "the last section", "condition 7", "R9", "E-5": all resolve. Broken references: none.

### Contradiction Re-Scan
- **Reviewer count:** consistent. Cap 3 (code). Default 3 today; 2 only if the owner accepts D-1; if D-1 is not accepted it remains 3 and the pre-registered rule decides. Count decision, R8, Cost and Open decisions agree that the incumbent is two under D-1 and three otherwise. No passage says the count must wait or that B's default is the safe state.
- **Engine default:** unchanged at 3 everywhere (Design, Correctness 2 and 4, invariants table, D-1, Considered and not carried). Shadow runs: 3 today and kept at 3 by the conditional default if D-1 is accepted. Clamp: left to C17.
- **Task-builder POST gate:** named a blocking skill-path consumer in the Design table, E-9, Correctness 4, D-1, RD-2, INV-012 and owner decision 3; option (a) is recommended in all three places that give a recommendation; Correctness 4 states that the debate consensus claim "no blocking path touched" is false until the owner chooses.
- **Escalation figure:** stated in the one allowed form (35 of 39 flagged, 34 of the 38 Tier 2 runs flagged, decisive in 0 certain and at most 1, with the three caveats and the five runs resolved) at lines 20 and 144; elsewhere only restated as "0 certain and at most 1" (Correctness 7, CI-1, Cost) or as "at most 1 of 39". The sentence "35 of 39 were flagged" in "What this does not show" states the flag-set count, not escalation, and agrees with the figure.
- **Status wording:** the Status block labels D-1 "Proposed for the owner's decision (not adopted)", the D-1 section says PROPOSED, owner-gated, and owner decision 1 says the debate's consensus favoured D-1 only with conditions 1 to 8. No section calls D-1 adopted or decided.
- **Possible tension, recorded not resolved:** the base selection chose B by score while both advocates favoured an A-min base; the merged text carries A-min as D-1 and says so in the convergence block and in "Selection record" above.
- New contradictions introduced: none found.

### Forbidden-phrase checks (grep, case-insensitive, fixed strings, `proposal-merged.md`)
| Phrase | Matches |
|---|---|
| "at most 5" | 0 |
| "13 percent" | 0 |
| "1 certain" | 0 |
| "clear-cut" (and "clear cut") | 0 |
| "up to 34-35" | 0 |
| "35 of 39 escalate" | 0 |
| "count must wait" | 0 |
| "Do not touch the reviewer count now" | 0 |
| "decide the count after H-A" | 0 (one pre-existing gloss of O-8 was reworded during validation) |
| "stays 3" | 0 (three descriptions of the engine default were reworded to "unchanged at 3" or "remains 3" during validation) |
| "0 of 6", "13 of 23" (withdrawn probe counts) | 0 |
| "at most 4", "one clear", "34 by the" | 0 |
| "Phase 1" | 3, all naming the base draft's demoted Phase 1 (lines 339, 342, 346); none describes it as committed scope |

Phase 1 is not described as committed scope anywhere: the Status block, Design "Staging", Correctness and Cost all call the flag change a conditional item (CI-1) that no step schedules. The superseded-claims content is carried in the final table "Considered and not carried" without quoting the forbidden phrases.

### Open-item coverage
- Six UNRESOLVED diff points present, each with both advocates' final positions (table 1 of the last section): S-002, S-006, C-003, C-010, C-013, C-016 (1 row each).
- Ten UNADDRESSED invariants present with severity and status UNADDRESSED (table 2): HIGH INV-009, INV-012, INV-013 first, then INV-001, INV-002, INV-004, INV-006, INV-008, INV-010, INV-011 (10 rows; grep count of `UNADDRESSED` rows is 10). Each names the change that records a mitigation and states that recording it is not a resolution. The four ADDRESSED findings (INV-003 partly, INV-005, INV-007, INV-014 partly) are listed in one sentence.
- Owner decisions: eight rows (D-1 acceptance, tripwire numbers, task-builder gate option, H-A pilot owner G-59, who closes G-67 under C17, document-loop default 4 and `live7` under C03, margin of the symmetric rule, fourth reviewer class instead of cutting N).
- Convergence status present: raw 0.80 at the threshold, BLOCKED_BY_INVARIANTS (3 HIGH UNADDRESSED), 24 of 30 points agreed, base chosen by tiebreaker at a 0.0061 margin.
- Nothing is marked "resolved" for an item the debate left open.

## Summary

- **Totals:** Changes 1-15: 15 applied, 0 failed, 0 skipped. Amendments A-1..A-15: 15 applied (A-2 is Change 15). Status: success.
- **Failures and skips:** none.
- **Notes for the orchestrator (flagged, not blockers):**
  1. Change 6 / A-5: the plan says "about nine edits in five files" for the EDIT rows; the table of EDIT sites has 16 rows in those five files. The plan's wording is kept; the mismatch is unexplained in the inputs.
  2. A-6: the amendment lists "the pre-filter is not the driver" as A counter-evidence; carried as CA-5 in the reading described under A-6. Please confirm.
  3. Change 10: the exact two-way wording of the symmetric count rule is mine, labelled `[PROPOSED]`.
  4. Change 11: the "Verified for" column values follow the plan's instruction; "Resolver" is defined to include the code engine.
  5. Ids invented for readability: N7-N11, M1-M5, CI-1, CA-1..CA-6, RD-1..RD-5, E-19..E-25, Steps A, B and C (the plan names none). The "Phase 1" mentions (3) could be removed if a mechanical grep must return zero.
  6. Facts added from my own read of the repo (not in the plan): the task-builder invocation at `:2225` and the HALT rule at `:2227`; the text of `SKILL.md:86`, `:318`, `:340`, `:658`, `:695`. All agree with the plan.
- **[UNVERIFIED] marks in the merged file:** 2 (the power of a 6-plan arm to resolve a 10-point margin, which the debate marks UNVERIFIED; whether `phase2CodegraphI` belonged to executor exclusion, which its files do not state). The tag legend line also contains the word `[UNVERIFIED]`. No plan item was found that could not be traced to the inputs; the items the plan marks PROPOSED or owner parameter are labelled as such.
- **Selection record:** base B won by 0.0061 via tiebreaker level 1 (debate points B 6 to A 4); the advocates' Round 2 consensus favoured an A-min base; the protocol chose B by score; the merged document carries A-min as Decision D-1.

## Orchestrator post-merge validation (added by the debate-orchestrator after the executor returned)

The orchestrator re-ran the checks itself rather than relying on the executor's report.
- Structure: the merged file has the H1, then the seven base H2 sections in order (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost), with "Decision D-1" and "Conditional items" inserted after Correctness argument and "Open decisions and unresolved conflicts" last (matches Amendment A-13). 48 `<!-- Source: -->` tags and the three provenance header lines are present.
- Forbidden phrases (case-insensitive grep on `proposal-merged.md`): "at most 5", "13 percent", "1 certain", "1 for certain", "clear-cut", "up to 34-35", "35 of 39 escalate", "34 by the pre-filter", "count must wait", "Do not touch the reviewer count now", "decide the count after H-A", "0 of 6", "13 of 23": 0 hits each.
- Open items: all six UNRESOLVED points (S-002, S-006, C-003, C-010, C-013, C-016) and all ten UNADDRESSED invariants (HIGH: INV-009, INV-012, INV-013; MEDIUM: INV-001, -002, -004, -006, -008, -010, -011) appear in the last section with status UNADDRESSED or UNRESOLVED; the section states that recording a mitigation is not a resolution; BLOCKED_BY_INVARIANTS and the 0.0061 selection margin are stated.
- Correction applied by the orchestrator: the merged text and the plan said the D-1 EDIT rows were "about nine edits in five files". Counting the site table in the merged file gives 13 EDIT rows covering 16 individual sites in five files (SKILL.md 8, refs/input-resolution.md 2, refs/reviewer-spec.md 3, commands/reflect.md 2, task-builder 1). The merged file was corrected in three places (the site-table preamble, risk RD-3 and the Cost row). The refactoring plan's "about nine" is left as written because the plan is the record of what was approved; this note is the correction.
- Executor note 2 (A-6, "the pre-filter is not the driver" listed as counter-evidence although Proposal A's own C5 claimed the opposite): accepted as the executor's reading (carried as CA-5, a point withdrawn by the recount); the orchestrator has not re-argued it and leaves it visible for the owner.
- Executor note 3 (the exact wording of the symmetric count rule is the executor's, labelled `[PROPOSED]`): accepted; it is an owner parameter.
- Selection record: base B won by 0.0061 via tiebreaker level 1; the advocates' Round 2 consensus favoured an A-min base; the protocol chose B by score and the merged document carries A-min as Decision D-1.
