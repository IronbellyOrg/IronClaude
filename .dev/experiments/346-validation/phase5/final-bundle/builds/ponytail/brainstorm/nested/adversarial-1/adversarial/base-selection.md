# Base Selection

Variants: A = variant-1-opus-architect (448 lines), B = variant-2-sonnet-refactorer (509 lines), C = variant-3-haiku-qa (395 lines). Scored by the orchestrating session from the variant texts, the round-1 and round-2 statements and the evidence files. Evidence column cites variant sections.

## Quantitative Scoring (50% weight)

Source requirements: the 12 "must specify" items of the variant brief (primary mechanism, brief text, skill invocation, safe apply, verdict effect, two alternative placements with predictions, mechanical enforcement, causes removed and left, file changes and substitution, measurement plan, cost, open questions).

| Metric | Weight | A | B | C | Computation |
|---|---|---|---|---|---|
| Requirement coverage (RC) | 0.30 | 1.00 | 1.00 | 0.92 | C gives no one-line-only substitution (it needs a wrapper, C s12) and covers the owner's placement only as the terminal reading: 11/12 |
| Internal consistency (IC) | 0.25 | 0.90 | 0.95 | 0.90 | A: revert-channel prediction contradicts its own N12 note (A s2 vs s11), 1 of ~10 scored claims; B: "cannot corrupt the spec" vs its own risk list (B s1 vs s15), counted half; C: terminal 2.0 forecast vs "cannot improve raw review 3" kept apart, but the row-share model conflicts with its own s2 caution |
| Specificity ratio (SR) | 0.15 | 0.90 | 0.92 | 0.80 | all name files, checks and numbers; C has more unquantified "UNVERIFIED planning assumptions" |
| Dependency completeness (DC) | 0.15 | 0.95 | 0.95 | 0.90 | internal cross-references resolve; C's `audit-schema.json` and ledger files are referenced but never shaped |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | 0.94 | 17, 17, 16 numbered sections |
| **quant_score** | | **0.952** | **0.968** | **0.894** | RC*0.30 + IC*0.25 + SR*0.15 + DC*0.15 + SC*0.15 |

## Qualitative Scoring (50% weight), additive binary rubric

Dual pass (input order A, B, C, then C, B, A). Disagreements between passes are listed in Position-Bias Mitigation.

| Dimension | Criterion | A | B | C |
|---|---|---|---|---|
| Completeness | 1 covers all explicit requirements | MET (s1-s17) | MET (s1-s17) | NOT MET (no one-line substitution) |
| | 2 edge cases and failures | MET (s8 row failure, s7 K1-K9) | MET (s7 STOP/SKIP, s10 K1-K13) | MET (s8 table) |
| | 3 dependencies and prerequisites | MET (s6 plugin, subagent) | MET (s5) | MET (s3 preflight) |
| | 4 success criteria | MET (s15 failure list) | MET (s14.3 F1-F5) | MET (s16) |
| | 5 out of scope stated | MET (s14 "Not edited") | MET (s1 "deliberately did not add") | MET (s1 non-goals) |
| Correctness | 1 no factual errors | NOT MET (N5 deletion claimed to close N5 and avoid N12; evidence-attribution classes N12 as C) | MET | MET |
| | 2 feasible with constraints | MET | MET | NOT MET (terminal edits contradict 427 FR-8/FR-9 rules, C s7) |
| | 3 consistent terminology | MET | MET | MET |
| | 4 no internal contradictions | NOT MET (A s2 vs s11) | MET | MET |
| | 5 claims supported | MET | MET (s2 E1-E13 table) | MET |
| Structure | 1 logical order | MET | MET | MET |
| | 2 consistent hierarchy | MET | MET | MET |
| | 3 separation of concerns | MET (s4 one owner per concern) | MET | MET |
| | 4 navigation aids | MET (s4 diagram, tables) | MET (s2 evidence ids) | NOT MET (no cross-reference ids) |
| | 5 artifact-type conventions | MET | MET | MET |
| Clarity | 1 unambiguous language | MET | MET | MET |
| | 2 concrete | MET | MET | MET |
| | 3 each section has one purpose | MET | MET | MET |
| | 4 terms defined | MET | MET | NOT MET (E-codes used before defined, s3) |
| | 5 next steps identified | MET (s11 recommendation) | MET (s9.4) | MET (s16) |
| Risk coverage | 1 three or more risks with impact | MET (s16, 7 risks) | MET (s15, 9 risks) | MET (s13) |
| | 2 mitigation per risk | MET | MET | NOT MET (several risks listed without a mitigation, s13) |
| | 3 failure modes and recovery | MET (s8) | MET (s7) | MET (s6 recovery) |
| | 4 external dependency failures | MET (plugin absent) | MET (plugin absent, subagent access) | MET |
| | 5 monitoring or validation | MET (recorder checks s12) | MET (K13, run validity s14.1) | MET (receipts) |
| Invariant and edge case | 1 collection boundaries (empty audit, all reverted) | NOT MET (empty table not handled) | MET (empty diff trigger, s3.3) | MET (s8) |
| | 2 state across components | MET (sha guard K8) | MET (K1 sha) | MET (hashes) |
| | 3 guard gaps | MET (K4 lock) | MET (K6) | MET |
| | 4 count divergence | NOT MET | NOT MET | NOT MET |
| | 5 interaction effects (shared hunks) | MET (REVERT_SHARED) | MET (K7 strongest verdict) | MET (edit groups) |
| **Total MET of 30** | | **26** | **29** | **24** |
| **qual_score** | | **0.867** | **0.967** | **0.800** |

### Edge Case Floor Check
A 4/5, B 4/5, C 4/5: all eligible.

## Position-Bias Mitigation
Pass 2 (reverse order) disagreed on two cells: A Invariant 1 (pass 1 MET on K2 "no missing rows", pass 2 NOT MET because K2 rejects an empty table only by accident) and C Structure 4. Re-evaluation: A Invariant 1 NOT MET (no explicit empty-table rule), C Structure 4 NOT MET. Verdicts changed by re-evaluation: 0 against pass 2, 2 against pass 1.

## Combined Scoring

| Variant | quant | qual | combined (0.5 each) |
|---|---|---|---|
| A | 0.952 | 0.867 | 0.909 |
| B | 0.968 | 0.967 | 0.967 |
| C | 0.894 | 0.800 | 0.847 |

Margin B over A: 5.8 points, above the 5% tiebreak trigger; no tiebreaker. Debate points won (scoring matrix): B 6 outright plus 6 shared merges, A 3 outright plus 7 shared, C 1 outright (S-001) plus 4 shared.

## Selected Base: Variant B (sonnet:refactorer)

Selection rationale: B has the most mechanical checks (K1-K13), the only verdict rule that can neither create a PASS nor lower a FAIL, the fail-open worst case (plain 427), the only diagnostic ablation, and it already carries the rule all three advocates adopted on X-002. Its forecast was the one most revised, but every variant's forecast fell on the same evidence (A-001, A-004).

Strengths to preserve from B: script classes of hunks and tolerant severity parse; no whole revert of report-blocking text; fail-open on any failed step; `open-blocking:` line and K13 consistency; `--auto-minor` ablation; F1-F5 falsifiers; honest per-replicate forecast.

Strengths to incorporate:
- From A: one owner per concern (diagram and table, A s4); the script copies the brief so no model writes it (A s5); revert by hunk number with baseline restored by the script (A s8); `auditor-isolation` fallback label (A s6); upgrade logged and ignored (A K9); deletion-first emphasis and the class-B remedies as the target; placement (a) as a one-condition change.
- From C: never call a post-audit number "review 3" and report raw and post-audit separately (C s1, s11); the edge-case test list and run-validity rules (C s8, round2-C O5); separate `## Fix Audit` heading so the Review Loop keeps seven bullets (C s9); real Skill-call receipt before claiming the plugin treatment (C s3); exact-token deletion check (round2-C O2).
- From the debate: drop the revert channel from every review-3 forecast; drop `--apply-audit` and `plan`; shrink rows delete words or restore the aligned baseline span; skip the audit when more than half the hunks are unattributed; owner approval of the editing contract recorded before S1.
