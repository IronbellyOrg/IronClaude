# Base Selection Report

Folder: `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/adversarial`. Variants: V1 = `variant-1-opus-architect.md` (opus:architect), V2 = `variant-2-sonnet-analyzer.md` (sonnet:analyzer), V3 = `variant-3-haiku-backend.md` (haiku:backend). Inputs: `scoring-quant.md`, `scoring-qual-pass1.md` (forward order V1, V2, V3), `scoring-qual-pass2.md` (reverse order V3, V2, V1), `debate-transcript.md`, `diff-analysis.md`, `invariant-probe.md`. Protocol: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1-A.5). The rubric has 6 dimensions of 5 criteria (30 criteria), so qual_score = criteria MET / 30.

## Quantitative Scoring (50% weight)

Copied from `scoring-quant.md` (Results table). SR, DC, SC and the claim counts are scripted; RC and the contradiction list are manual with quoted evidence in that file.

| Metric | Weight | V1 (opus:architect) | V2 (sonnet:analyzer) | V3 (haiku:backend) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.0000 (15/15) | 1.0000 (15/15) | 1.0000 (15/15) |
| internal_consistency | 0.25 | 0.9955 (2 contradictions in 446 claims) | 0.9853 (5 in 341) | 0.9948 (1 in 194) |
| specificity_ratio | 0.15 | 0.9991 (1066 / 1067) | 1.0000 (775 / 775) | 0.9965 (286 / 287) |
| dependency_completeness | 0.15 | 1.0000 (107/107) | 1.0000 (51/51) | 1.0000 (2/2) |
| section_coverage | 0.15 | 1.0000 (12/12) | 1.0000 (12/12) | 1.0000 (12/12) |
| **quant_score** | | **0.9987** | **0.9963** | **0.9982** |

Spread is 0.0024, so this layer does not separate the variants (as `scoring-quant.md` itself says). V3's DC rests on only 2 internal references.

## Qualitative Scoring (50% weight)

Final verdicts are the pass 1 / pass 2 verdicts where they agree, plus my re-evaluation for the one disagreement (see Position-Bias Mitigation). All three passes spot-checked repo code under `src/superclaude/` (panel.py, ensemble.py, contract.py, SKILL.md 789 and 950-953, cost-profile.yaml); the spot-check results in both pass files agree with each other.

### Final per-dimension subtotals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness (COMP-1..5) | 5/5 | 5/5 | 5/5 |
| Correctness (CORR-1..5) | 5/5 | 3/5 | 5/5 |
| Structure (STRU-1..5) | 5/5 | 5/5 | 5/5 |
| Clarity (CLAR-1..5) | 5/5 | 5/5 | 4/5 |
| Risk Coverage (RISK-1..5) | 4/5 | 4/5 | 4/5 |
| Invariant & Edge Case Coverage (INVR-1..5) | 5/5 | 5/5 | 5/5 |
| **Total MET / 30** | **29** | **27** | **28** |
| **qual_score** | **29/30 = 0.9667** | **27/30 = 0.9000** | **28/30 = 0.9333** |

### Criteria not MET (final)

| Variant | Criterion | Why (evidence cited in the pass files) |
|---|---|---|
| V1 | RISK-1 | Risks 1-8 and the candidate "Risk: low/medium/high" lines give impact but no per-risk probability. Both passes agree. |
| V2 | CORR-1 | Labels stage 5 "additive 1.9.0" while adding a legal `merge_method` value and rewording gate 9; `SKILL.md:952-953` makes a semantic change Major (matches diff-analysis X-004). Both passes agree. |
| V2 | CORR-4 | Candidate C says "-5k to +3k" but Cost model says "Net: 0 to -2k"; stage 5 total "30k-63k" is then computed as 64; stage 5 "additive" contradicts its own EV-2 edit. Both passes agree. (Matches X-015 and X-004.) |
| V2 | RISK-1 | Risks 1-10 give impact but no probability. Both passes agree. |
| V3 | CLAR-1 | Selectors left abstract ("two eligible independent slots from lower allowed pools", "conservative multi-file matching", "eligible" never pinned to tiers or rules). Both passes agree. I also saw `variant-3-haiku-backend.md` line 177 and line 167 use these phrases. |
| V3 | RISK-1 | Risks 1-9 give impact but no probability. Both passes agree. |

### Evidence for the re-evaluated criterion

V3 CLAR-2 ("concrete rather than abstract: specific actions, not general principles"). Pass 1 said NOT MET (3-slot template only in prose, no merge command line). Pass 2 said MET (concrete YAML envelope, idempotency tuple). I read the variant text:
- `variant-3-haiku-backend.md:121` opens a ```yaml block with the finding/submission envelope; line 112 lists the exact envelope fields (`schema`, `run_id`, `round`, `reviewer_id`, `attempt_id`, `input_tree_sha256`, `brief_sha256`, `policy_sha256`).
- Line 193: the manifest state machine is named state by state, `resolved → dispatched → collected → calibrated → merged → validated → published`, plus the idempotency tuple `(run_id, snapshot_hash, policy_hash, stage, reviewer_id, attempt_id)`.
- Line 178 gives actions with exact names: keep exactly `T1 card excerpt`, `Grounding hunks`, `Coverage slice`, and it names the existing CLI `superclaude review panel resolve`, marking the extension PROPOSED (line 323: "no new flag is claimed available").
- Pass 1's reason (no merge command line, template in prose) is true, but the criterion asks for specific actions, not for a command line; V1 and V2 pass it through commands, V3 passes it through schema, state names, tuple and numbered steps. Line 180 admits today's single-`--doc` merge cannot process the envelope, so omitting a command line is honest, not vague. Verdict: MET.
- CLAR-1 stays NOT MET for V3 on its own evidence (abstract selectors are different from a missing command).

### Edge-case floor check (INVR dimension, floor = at least 1 of 5)

| Variant | INVR | Eligible as base |
|---|---|---|
| V1 | 5/5 | Yes |
| V2 | 5/5 | Yes |
| V3 | 5/5 | Yes |

No variant is below the floor and not all variants score 0, so no floor suspension or warning is needed.

## Position-Bias Mitigation

Compared 90 cells (30 criteria x 3 variants). Pass 1 and pass 2 agree on 89; they disagree on 1.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| CLAR-2 | V3 | NOT MET | MET | DISAGREE | MET (re-evaluated above; evidence at `variant-3-haiku-backend.md:112,121,178,193,323`) |

Disagreements re-evaluated (disagreements_found): 1
Final verdicts changed (verdicts_changed): 1 relative to pass 1 (CLAR-2 for V3 moves NOT MET to MET); 0 relative to pass 2.

Effect on totals: pass 1 gave 29 / 27 / 27, pass 2 gave 29 / 27 / 28, final is 29 / 27 / 28. Only V3 moved (27 to 28). The ranking by qual does not change under either pass: V1 > V3 >= V2 in pass 1 (V2 tied V3 at 27), V1 > V3 > V2 in pass 2 and final.

## Combined Scoring

variant_score = 0.50 x quant_score + 0.50 x qual_score (computed with `uv run python -` on stdin).

| Variant | Quant x 0.50 | Qual x 0.50 | **Final Score** | Rank |
|---|---|---|---|---|
| V1 (opus:architect) | 0.50 x 0.998738 = 0.499369 | 0.50 x 0.966667 = 0.483333 | **0.9827** (0.982702) | 1 |
| V3 (haiku:backend) | 0.50 x 0.998188 = 0.499094 | 0.50 x 0.933333 = 0.466667 | **0.9658** (0.965761) | 2 |
| V2 (sonnet:analyzer) | 0.50 x 0.996334 = 0.498167 | 0.50 x 0.900000 = 0.450000 | **0.9482** (0.948167) | 3 |

**Margin (top two, V1 minus V3):** 0.982702 - 0.965761 = 0.016941 = 1.69 points, which is below the 0.05 threshold. The tiebreaker applies.

### Tiebreaker

Level 1, points won in the Step 2 Scoring Matrix (count of the Winner column in `debate-transcript.md`, 68 points):

| Winner | Points | Share of 68 |
|---|---|---|
| V1 | 25 | 36.8% |
| V3 | 24 | 35.3% |
| V2 | 11 | 16.2% |
| UNRESOLVED | 8 | 11.8% |

This matches the transcript's own "Variant tally (points won in R2): V1 25, V2 11, V3 24, unresolved 8".

- **Tiebreaker applied: Yes. Level 1 decided: V1, by a margin of 1 point (25 vs 24).**
- Caveat: 1 point is 1.5 percentage points of 68, which is inside the protocol's 5% "tied" band for debate performance. If that is read as tied, level 2 (CORR criteria MET) is also tied, V1 5/5 and V3 5/5 (V2 3/5), and level 3 (input order, V1 first) selects V1. All three readings select V1, so the outcome does not depend on the reading.
- Points won by V1 (25): S-002 S-006 S-007 S-009 S-010 S-012 C-001 C-002 C-003 C-004 C-005 C-009 C-010 C-014 C-018 C-019 C-022 C-023 X-001 X-004 X-016 X-019 A-006 A-009 A-014.
- Points won by V3 (24): S-005 S-008 S-011 C-011 C-012 C-015 C-016 C-017 C-021 C-024 X-002 X-005 X-007 X-008 X-009 X-012 X-013 X-014 X-015 X-017 A-004 A-005 A-008 A-010.
- Points won by V2 (11): S-003 C-006 C-008 C-013 C-020 X-006 X-011 X-018 X-020 A-001 A-012.
- Unresolved (8): S-001 S-004 C-007 C-025 X-003 X-010 A-002 A-003.

## Selected Base: Variant 1 (opus:architect)

### Selection Rationale

- V1 has the highest combined score (0.9827 vs 0.9658 and 0.9482). It leads on qual (29/30 against 28 and 27) and on quant (0.9987, narrowly), and it is the only variant that never lost a correctness criterion. It passed the edge-case floor with 5/5 on INVR.
- The numeric margin over V3 is only 0.0169, so the choice rests on the tiebreaker: V1 won 25 of 68 debate points against V3's 24 (level 1; levels 2 and 3 also give V1).
- V1 won the points that decide whether a design can be built as written: the only template that passes the validator at `panel.py:140-141` (C-009, X-001), the most executable pre flow (C-010), the widest candidate set (C-001, S-002), the superset finding format (C-004), the stage table with "What ships", entry, exit and rollback (S-009, C-014), and the consumer-level change plan (S-010, U-004). Debate consensus in `debate-transcript.md` ("Emerging consensus") already treats V1's kernel skeleton as the base with V3's policy grafted on.
- Be clear about what "base" means here. V3 won 24 points, many of them L3 state, guard and contract points (C-011, C-015, C-016, C-017, C-021, C-024, X-005, X-009). The merged design takes V1's skeleton and many of V3's and V2's rules. The "Strengths to incorporate" and "Weaknesses to fix" sections below are binding inputs for the merge step, not optional.

### Strengths to preserve

Structure and spec shape (V1):
1. Five candidates A-E each with Changes/Keeps/Cost/Risk/Verdict, plus the comparison matrix (S-002 98%, C-001 90%).
2. The 13-row finding-format table with "v1?" and "Set by" columns, so ownership of each field is visible (S-006 98%).
3. Command-level adapter steps for pre and post (S-007 90%, C-010 75%), including the exact `superclaude review merge --schema findings-v2 --doc plan=...` line.
4. The stage table with "What ships", Entry, Exit and Rollback for each stage (S-009 98%), the shadow stage and byte-identity exit test (C-014 75%), and the A-014 byte-identical `/sc:spec-panel` merge test (A-014 98%).
5. The consumer-by-consumer change list including wrapper triggers 11 and 11b and the "legacy runs emit 1.8.0 values" rollback (U-004, S-010 90%), and the repo-wide consumer grep as a hard stage-entry gate (A-009 90%).
6. The validator-legal reflect template (`@reflect-pre`, one fixed anchor) (C-009 90%, X-001 90%), and the explicit per-model `class` map for exclusion (A-006 90%).
7. Superset finding format `findings-v2` with typed `citations[]` and `anchor` optional when citations exist (C-004 90%), and the primary-citation fingerprint fix (C-005 75%, contested by V3).
8. Full PROPOSED-names inventory (S-012 98%) and the version-correct view that a widened legal set is a major change (X-004 98%, SKILL.md:953).
9. Cost model with arithmetic shown, e.g. "12+16.5+4+0+2.4 ≈ 35" (CORR-5).
10. Opus calibrator by today's SKILL.md:1181 rule and the calibrator_diversity side effect (C-018 90%, X-016 90%, U-005); the correct 405/408 line cites (X-019 98%).
11. Unique V1 items: deterministic `verify-citations` pre-check that only adds drops, limited to a missing file or out-of-range line (U-001, C-019 75%, with A-010 REJECT narrowing it); shared-card shadow run (U-002); scripted seeded-defect injection (U-003).

### Strengths to incorporate

From V3 (haiku:backend):
1. Manifest state machine, idempotency identity `(run_id, snapshot_hash, policy_hash, stage, reviewer_id, attempt_id)`, resume by hashes, atomic publish (U-014, S-008 98%, C-011 98%: attempts are not votes).
2. Five completion states; empty-valid is not failure; quorum counts `complete` only (U-015, C-024 98%). Also closes the hole behind INV-010 and INV-017 and informs INV-011.
3. Contract stays 1.8.0 with `merge_method: adversarial` and the real child score for the first pre shipment; deterministic agreement is internal telemetry only (C-015 98%, C-016 98%, X-005 98%). V1's `merge_method: panel` plus a 2.0.0 bump must not be the first shipment.
4. Executor exclusion that filters candidates before dispatch, checks actual identity afterwards, and replaces an ineligible anchor before resolution so it degrades rather than raises (C-017 90%, X-002 90%). V1's "hard_exclude raises" rule is replaced by this.
5. Judge identity and collision accounting (C-021 98%).
6. Honest cost units: output, retrieval and input tokens kept apart, 1.25x hard kill on the midpoint (65.6k), target versus allowance explained (C-012 98%, X-012 98%, X-013 98%, X-014 80%, X-015 90%, A-005 98%, S-011 98%, U-018).
7. Calibration kept embedded in the full card, no sidecar-only reduction (X-008 90%, X-009 98%, A-004 98%).
8. Separate documents, no concatenation (X-007 75%, C-023 shared with V1 at 90%); a PROPOSED multi-input merge.
9. No automatic quote-mismatch rejection (A-010 98%); post-execution debate kept until an independent post trial exists (A-008 80%).
10. Finding `channel` (`defect` / `grounding-gap` / `advisory`) so no-spec gaps are never counted as Regression (U-016); record that `merge_cmd.py` writes the report before saving the ledger, so the pair is not a transaction (U-017, relates to INV-003).
11. Measurement hygiene: 2 repeats per arm, hidden arm identity, "safety failure fails regardless of savings" (U-018).
12. Answers in place in Q5 and Q7 (S-005 90%) as a reading aid, optional.

From V2 (sonnet:analyzer):
1. Three-arm first measurement with a T1-only arm and a stop rule (U-008, C-020 98%, A-001 98%, X-011 90%); also seeded defects with a union ledger of natural findings (A-012 90%).
2. Keep the pre-execution debate until a T1-armed measurement exists (C-006 90%, X-006 90%); V1's "debate removed by default" in pre moves to optional later stage.
3. Per-reviewer `launch` null/non-null engine rule, plus V3's pin-before-freeze (C-008 75%).
4. The 15-point gate before any panel larger than 3 (C-013 75%; V3 dissents, so keep it labelled PROPOSED).
5. Real-card evidence: calibrator scores 0.60/0.50/0.55 and the dropped `source.md:143` that a locate check would pass (U-009).
6. Forbidden-model (Fable) filter in `resolve` (U-013, X-020 98%); the correct ledger cites (X-018 90%); the `<sr1>` path abbreviation and PROPOSED/UNVERIFIED conventions (S-003 75%).
7. Ablation: 2 reviewers plus an Opus calibrator versus 3 reviewers with Haiku stand-ins (U-012); audit-bundle layout with H3 `path:start-end` headings (U-011) as a per-source section layout only, not as a concatenated identity store; `reflect_category` preserved next to the panel category map (U-010).

### Weaknesses of the base to fix

Debate points V1 lost (Scoring Matrix winner other than V1):

| Winner | Points | What the merged design must change in V1 |
|---|---|---|
| V3 | S-005, S-008, S-011 | Add the state-machine/idempotency block, separate cost estimates and units; answer Q5 and Q7 in place or keep forward pointers consistent. |
| V3 | C-011, C-012, C-015, C-016, C-017, C-021, C-024 | Retry/vote rule, honest cost units, contract version policy (1.8.0, `adversarial`), real child score, anchor replacement, judge collision accounting, completion states. |
| V3 | X-002, X-005, X-007, X-008, X-009, X-012, X-013, X-014, X-015, X-017 | See the verified-false and intra-V1 items below. |
| V3 | A-004, A-005, A-008, A-010 | Drop the findings-only sidecar, keep units separate, keep the post debate until a post trial, no automatic quote-mismatch drop. |
| V2 | S-003, C-006, C-008, C-013, C-020 | Keep the pre debate, use the `launch` rule, numeric panel gate, add the T1 arm. |
| V2 | X-006, X-011, X-018, X-020, A-001, A-012 | Remove "debate separated nothing, so remove it" as a default (X-006); fix V1's ledger cites (X-018); name the Fable launch alias (X-020); state the T2-versus-T1 assumption (A-001); pair seeded defects with a union ledger (A-012). |
| Unresolved | S-001 S-004 C-007 C-025 X-003 X-010 A-002 A-003 | Not won by anyone; see X-003, X-010, A-002 and A-003 below. |

Factual errors the diff analysis marked against V1:
- X-003 (verified false, all three variants): V1's versioning plan never mentions that the headless builder emits `contract_version` "1.0" (`cli/reflect/ensemble.py:74,788`), not 1.8.0. Round 2 evidence: the builder is post-only (`ensemble.py:797`), so a pre-only contract change does not reach it, but the plan must say so.
- X-020 (verified false, incomplete): V1 says `launch` maps ids to sonnet, haiku and opus (`review-tiers.default.json:29`); the map also has `claude-fable-5-1` to `fable`. Add the forbidden-model filter (V2 U-013).
- X-018 (verified partly): V1's ledger line cites are wrong (`ledger.py:213-222`, `200-298`); correct ones are `ledger.py:107` for `merge_round` and `187-190` for the OR.
- X-010 (verified false for the Agent tool `model` parameter): V1 lists gateway alias dispatch as UNVERIFIED, but the tool enum rejects it. The merged design must not claim gateway dispatch for pre; the gateway stays on legacy.
- X-009 (intra-V1 gap, verified true): V1's sidecar keeps calibration out of cards while its post step 8 passes `--compare <calibrated cards>`; fix by embedding calibration (already the consensus).
- X-005 (verified true): V1's `merge_method: panel` conflicts with the `SKILL.md:789` legal set; V1 itself concedes a major bump. The consensus avoids the new value in the first shipment.
- X-013 (verified true): V1's before-high 96k and after-high 68k exceed the 65.6k hard kill (1.25x the 52.5k midpoint, `cost-profile.yaml:70`).
- X-017 (verified true): with `--cap 1` every blocking round records `ESCALATE` (`ledger.py:93-96`); V1 listed this UNVERIFIED. Resolve it in the design.
- IC items in `scoring-quant.md` (not diff-analysis): V1 has two internal contradictions, pre cost 34-66k vs 35-68k, and option E "no contract version change" vs a "1.9.0 additive" in the comparison table. Reconcile both.
- Qualitative: RISK-1 NOT MET (no probability on any of 8 risks); add probability and impact per risk.

HIGH UNADDRESSED invariants in `invariant-probe.md` (the merged design must resolve each):
- **INV-005** (guard_conditions): executor exclusion fails open. `panel.py:402-403` fixed slot ignores `exclude`; `panel.py:405,408` `or candidates` re-admits an excluded model when the pool empties. Require `resolve_slot` or the adapter to refuse the fallback for executor-class exclusion (V1's `hard_exclude` raises idea, reconciled with V3's anchor replacement and "degrade, not raise").
- **INV-015** (collection_boundaries): a plan reviewed against several files cannot keep one identity per file; `merge_cmd.py:29-34` takes one `--doc`, `ledger.py:196-197` stores a bare `span`, and `findings.py:363-364` compares spans without a path, so two findings at line 10 of different files merge. V1's role-qualified multi `--doc` is PROPOSED and needs path-aware rows.
- **INV-022** (sufficiency challenge): "panel resolution gives executor exclusion" is not enough; the gates listed there include the unknown-executor fail-open (`SKILL.md:600-602`), the per-model class map (A-006), no `tier1b` stand-in, and reading the true model identity back from an agent-session reply, which no variant shows.
- **INV-023** (sufficiency challenge): a field mapping without a version change is not proved safe; wrapper triggers 6 to 14 read fields the interactive pre path assembles by prose, and the A-009 consumer grep is a gate, not a result. Include the interactive builder in the grep scope.
- **INV-024** (sufficiency challenge): the first measurement has no power calculation (about 0.12 half-width at n = 60 defects, recall near 0.7, wider than a 0.10 margin; three incompatible margins 10, 15 and 5 points). Add a sample-size statement and one margin.

The MEDIUM and LOW UNADDRESSED invariants (INV-001, 002, 003, 006, 007, 009, 011, 012, 013, 014, 016, 018, 019, 020, 021) are not listed here as required fixes by the brief, but the merge step should still read them in `invariant-probe.md`; INV-002 and INV-003 (multi-file hash, retry needs a ledger path per attempt) are the closest to the items above.
