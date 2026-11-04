# Adversarial Debate Transcript

## Metadata

- Pipeline: `/sc:adversarial` Mode B (`--generate spec`), source `../seed-brief.md`
- Depth: standard
- Rounds completed: 3 advocate rounds plus 1 probe:
  - Round 1 (parallel advocate statements)
  - Round 2 (sequential rebuttals)
  - Round 2.5 (invariant probe, single fault-finder)
  - Invariant-resolution round (extra; see below)
  - Round 3 was not run: it requires `--depth deep`.
- **Extra round, recorded honestly:** after Round 2.5, the invariant probe gate blocked convergence. Four findings were HIGH and UNADDRESSED: INV-001, INV-008, INV-033 and INV-034. The gate's block message prescribes this action: "Address the flagged items in a subsequent debate round or acknowledge as accepted risk." A focused invariant-resolution round was therefore run (files `round-inv-advocate-{A,B,C}.md`). Each advocate proposed resolutions for the four HIGH items, took positions on selected MEDIUM items, and marked all four HIGH items ADDRESSED. The orchestrator did not accept the advocates' own status labels. It re-applied the gate with this rule: a HIGH item counts as ADDRESSED only if the three resolutions agree on a concrete rule, or a majority agrees and the minority does not reject it.
- Convergence achieved: 90% (90 of 100 diff points agreed)
- Convergence threshold: 75% (`--convergence 0.75`)
- Focus areas: All
- Advocate count: 3. A = `variant-1-opus-architect.md` (opus:architect). B = `variant-2-sonnet-refactorer.md` (sonnet:refactorer). C = `variant-3-haiku-qa.md` (haiku:qa).
- Status after the invariant-resolution round: BLOCKED_BY_INVARIANTS (INV-034 still HIGH and UNADDRESSED).
- **Second extra round (INV-034 only), same gate action:** the orchestrator wrote a candidate rule (`round-inv034-brief.md`, R-034) and all three advocates answered (`round-inv034-advocate-{A,B,C}.md`). All three answered MODIFY with compatible rules (see "INV-034 focused round" below). Gate re-applied: INV-034 ADDRESSED.
- Final status: **CONVERGED**. Agreement 90% is above the 75% threshold, every taxonomy level is covered, and no HIGH invariant remains UNADDRESSED.
- Assembled: 2026-11-04T14:57:36Z, by the debate-orchestrator, which took no part in the debate.

## Round 1: Advocate Statements

The round files are summarized here, not copied. Citation form: `R1-A:NN` means line NN of `round1-advocate-A.md`.

### Variant A Advocate (opus:architect): `round1-advocate-A.md`

- **Position:** a conflict is one more remediation cycle inside the existing FSM. The design has one new edge `(S2_CLASSIFY, "conflicting")`, one pure `conflicts.py`, two refs split by tier and data-driven `MechanicalRule` rows. A conflict spends a round, so `push_count <= max_rounds` holds without a new counter, and reviewers re-review the merge (J-66) (R1-A:5-11, :33-49).
- **Steelman of B:** minimal blast radius, and it follows the CI-phase precedent. A said it would adopt B's phasing (U-008), the high-suspicion checklist (U-009), `finish-merge.sh` (U-010), the disjointness test (U-011) and the narrow Tier 1 (R1-A:15-25).
- **Steelman of C:** testability first, the Definitions section, `merge_push_count <= 1`, and a marker scan scoped to conflicted paths (R1-A:27-31).
- **Critiques:** B-W1..B-W9, including a second push gate, a known conflict left after `HALT_MAX_ROUNDS` (B-W4), the create-path premise, and Tier 0 cost. C-W1..C-W9, including Wave 0b being unrunnable, the L1/classify contradiction, re-check point B, and staged-set equality (R1-A:53-79).
- **Concessions (9):** the operator recovery text omits the push (X-041); a conflict costs a round; `WHITESPACE_ONLY` is unsafe; there is no evidence-validator `unsupported` verdict; B's rollout is better (default 1); U-009; B's commit gate; C's flag-matrix critique; L1 should continue to review (R1-A:81-91).

### Variant B Advocate (sonnet:refactorer): `round1-advocate-B.md`

- **Position:** lowest regret. Siblings only (`merge_parent_ok`, `evaluate_sync_decision`); `fsm.py` push, gate and transition code is untouched; the CI-phase precedent means no round, no re-trigger and no edge; four phases with gates (R1-B:5-20).
- **Steelman of A:** reusing FSM accounting keeps invariants true; J-66; the create-path diagnosis; the captured-fixture parser; `MechanicalRule`; the `pr_conflicting` skip (R1-B:24-36).
- **Strengths claimed:** S1-S11, including the disjointness property, the strict tier ladder, empirically verified git behaviour, and the push-inclusive recovery text (R1-B:53-67).
- **Critiques:** WA1-WA8 (a mechanical conflict pays a round, L1/L2 stop before review, predicate-5 stretch, and others) and WC1-WC11 (R1-B:71-98).
- **Concessions (8):** the create-path rationale is wrong; the CI blind spot was overclaimed (adopts U-004); K8 is a gap for Tier 2; duplicated triad builder; three scripts are the hardest to test; line-count pin debt; Tier 0 cost understated; L2 FSM fidelity (R1-B:100-109).

### Variant C Advocate (haiku:qa): `round1-advocate-C.md`

- **Position:** treat the feature as a test-surface problem. C's value is the QA scaffolding: the risk register, the no-test boundary, the `== 41` sweep, `merge_push_count <= 1` and per-tier call ceilings. On architecture C concedes to A and B (R1-C:6-10).
- **Steelman of A:** the read-only probe (AD-6), conflict-first placement, base ancestry. **Steelman of B:** phasing, the high-suspicion checklist, `finish-merge.sh`, the conservative tier table (R1-C:14-37).
- **Critiques:** A's predicate-5 stretch, the round cost, AD-7 changing L0 behaviour, edge risk, L1 stopping. B: reviewers never see `M` (K8), act-late waste (K9), Tier 0 cost, three scripts, Tier 2 dark (R1-C:54-69).
- **Concessions (9):** all seven diff-analysis defects against C (X-008, X-012, X-023, X-033, X-034, X-035, X-037), plus X-036/X-038 self-flagged, plus C-036 (R1-C:71-83).

**Round 1 outcome on the coupled placement and accounting points.** Majorities on single points did not fit together. C-014, C-017, C-019, X-001 and X-003 had an A majority (early action, re-trigger). C-020 and X-004 had a B majority (no edge). C-018 and X-002 were a three-way split. Round 2 showed this combination was incoherent: R2-A N1 and R2-C R-C16 found a three-way coupling.

## Round 2: Rebuttals

### Variant A Rebuttal: `round2-advocate-A.md`

- New evidence:
  - **N1:** a review counts only for the current head, and a push triggers no review, so placement and re-trigger are one decision.
  - **N2:** `push_count` already counts no-round CI pushes.
  - **N3:** J-66 is decided per kind of change.
  - **N4:** reusing `evaluate_push_decision` at the late hook reproduces #305 through predicate 4.
  - **N5:** the repo has a precedent for safe edge addition.
  - **N6:** merge-method field names exist in `gh`.
  (R2-A:45-86)
- Proposed **A-prime, the tier split**: Tier 2 acts early, re-reviews and spends a round. Tier 1 acts late with no round and no re-trigger, through B's sibling gate. Tier 3 halts early (R2-A:9-15).
- Concessions: R-1 (Tier 1), R-2 (L1/L2 continue to review), R-4/R-5 (AD-7 becomes a precursor scoped to L1+), R-6, R-7, R-8 (Tier 1), R-11, R-12, R-14, R-15 (default 1), R-16 (R2-A:23-43).

### Variant B Rebuttal: `round2-advocate-B.md`

- Verified N1, N3, N4 and N5. **Accepted the split as the end state, with six modifications** (R2-B:85-134):
  - **M1:** P1 ships Tier 1 only; the edge lands in P2, dark.
  - **M2:** Tier 1 acts on all four armed outcomes.
  - **M3:** Tier 3 halts at the end of Wave 0 in the `SKILL.md:268` shape.
  - **M4:** one acting site per tier and ordinal; late Tier 2 halts `late_conflict`.
  - **M5:** one sibling gate serves both tiers, plus the S5a clause `applied_edits > 0 or kind == "merge"`.
  - **M6:** Tier 1 is excluded from `push_count` and goes into `sync_push_count`.
- New evidence NE1-NE9. The key items:
  - NE1: under A-prime the `applied_edits`/S5a gate collides.
  - NE2: `ci_wait_autofix` restricts only CI findings.
  - NE5: Branch A recovery does not know the push kind.
  - NE6: the routing table grows, so one pure router is required.
  - NE9: the evidence-validator contract.
  (R2-B:147-159)
- Conceded A-B3 to A-B6 and A-B8, plus A-S4 to A-S6. Adopted A's GitHub-first ordering (R2-B:43-71).

### Variant C Rebuttal: `round2-advocate-C.md`

- Verified N1 end to end. This gives C a seventh High-class defect: an early push with no re-trigger ends in `terminal_timeout`. C also flagged its own Round 1 pairing as incoherent: the three-way coupling is early ⇒ re-trigger ⇒ tick (R2-C:5-9, :49-50).
- **Accepted the split as amended by M1-M6, with six QA conditions:** QA-1 to QA-10, the acceptance tests the merged design must carry (R2-C:61-87).
- New evidence:
  - NE-C1: the `push_count` bounds are prose only.
  - NE-C2: CI pushes already strain them.
  - NE-C3: the S5a clause pin anchors.
  - NE-C4: the `models.py:23` docstring.
  - NE-C5: the third leg of N1 is confirmed.
  (R2-C:101-109)

## Round 2.5: Invariant Probe

`invariant-probe.md` has 36 findings: 10 ADDRESSED and 26 UNADDRESSED. Of the unaddressed, 4 are HIGH, 16 MEDIUM and 6 LOW. The four HIGH UNADDRESSED blockers:

- **INV-001:** recovery from a crashed sync push has no representable resume target.
- **INV-008:** the merge preflight tolerates unstaged changes.
- **INV-033:** `uv.lock` is gitignored in this repo, so P1 cannot fire here.
- **INV-034:** the CI re-poll can read `clean` before any check exists on the merge head.

## Invariant-Resolution Round (extra, gate-mandated)

Files: `round-inv-advocate-A.md`, `round-inv-advocate-B.md`, `round-inv-advocate-C.md`. Each advocate proposed a resolution, a carrier and acceptance tests for the four HIGH items, and gave positions on INV-003, 004, 009, 010, 018 and 035. The orchestrator's gate re-application is in the "Invariant Probe Gate" section below.

Effect on diff points: the round settled X-005, C-026, X-024, C-030, C-031, X-030 and C-035, which had been split after Round 2. Convergence after Round 2 was 83/100. After this round it is 90/100.

## Scoring Matrix

**How agreement was decided:**

- An advocate's position is its latest stated position, in this order of precedence: round-inv, then Round 2, then Round 1, then its own variant's content.
- **agreed** means unanimous, or a ≥2/3 majority.
- A point no advocate debated is agreed only when two variants already share the approach in their own text. These rows are labelled **(inferred)** and get 55-65% confidence.
- Confidence bands follow the protocol: 90-100% unanimous with strong evidence; 70-89% clear majority; 50-69% contested or inferred.
- "Split" is the consensus tier split as amended by M1-M6: Tier 1 late in B's shape, Tier 2 early in A's shape (landing in P2), and Tier 3 as a Wave 0 halt.

**Taxonomy level (Level column):** points were tagged automatically by signal terms, with priority L3 > L2 > L1. L1 = surface. L2 = structural. L3 = state mechanics.

| Diff Point | Level | Agreed | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|
| S-001 | L1 | No | unresolved | 50% | Document size; no advocate argued it, and the three variants differ. |
| S-002 | L1 | No | unresolved | 50% | Front-matter form; not debated, three different forms. |
| S-003 | L1 | No | unresolved | 50% | Heading counts; not debated. |
| S-004 | L1 | No | unresolved | 50% | H2 order; not debated, three orders. |
| S-005 | L1 | Yes | A | 70% | B's steelman calls A's AD-1..AD-10 with rejected alternatives "the most disciplined decision record" (R1-B:36); A claims it; C is silent. |
| S-006 | L1 | Yes | A/B (inferred) | 60% | A and B both carry a dedicated, cited grounding section (A §1, B §2 G1-G19); C has none. |
| S-007 | L1 | No | unresolved | 50% | Requirement format; three different forms, not debated. |
| S-008 | L2 | Yes | A | 80% | B adopted A's `conflict_action`, `MechanicalRule` and `parse_stage_records` (R2-B A-S5, A-S6); C adopted A's FR-C6 table (R2-C QA-4). |
| S-009 | L1 | Yes | B | 70% | B's M4 tier×ordinal table (R2-B:107-112) is accepted by C (R2-C:63); A's round-inv INV-010 works inside the same table. |
| S-010 | L2 | Yes | B | 95% | Unanimous: P0-P3 phasing (R2-A R-15, R2-C U-008). |
| S-011 | L1 | Yes | A/B (inferred) | 60% | A §15 and B §13.1 both carry research-traceability tables; C cites inline only. |
| S-012 | L2 | Yes | A/B (inferred) | 60% | A §11 and B §3.3/§13.2 both carry file inventories; C has none. |
| S-013 | L1 | Yes | A/C (inferred) | 55% | Neither A nor C nests appendices under an index; B's appendices sit as H3 under "13. Index". B's Appendix B content is kept in the body. |
| S-014 | L1 | Yes | C | 95% | A conceded separate likelihood and impact columns (R2-A R-16); B and C adopt C's register (R2-B 1.2, R2-C QA-10). |
| S-015 | L2 | Yes | B+C | 70% | B's test-plan sections plus C's "deliberately no test" list; all three adopt that list (R2-A §4, R2-B 1.2, R2-C:87). |
| C-001 | L2 | Yes | Split (A+B) | 85% | Converged mix: 1 core module, 2 refs, 2 P1 scripts, 0 agents/templates, 1 FSM edge in P2, `--conflict-max-tier` (R2-B M1, R2-C §3). |
| C-002 | L2 | Yes | A+B | 85% | `conflicts.py`, with A's router and parser and B's sibling gate and parent check (R2-B A-S5/A-S6, M5). |
| C-003 | L2 | Yes | A | 90% | Two refs split by tier (U-003); B adopted it (R2-B C-003), and C accepted M1, which includes it. |
| C-004 | L2 | Yes | B (modified) | 75% | P1 ships a thin `probe-merge.sh` and `finish-merge.sh`; the evidence script is deferred (R2-B C-B4). C accepts (R2-C:97). A's round-inv places INV-004 "in the probe script". |
| C-005 | L2 | Yes | Tie (all) | 95% | All reuse `evidence-validator` and claim "grounding checked" only (A-002 unanimous). |
| C-006 | L2 | Yes | Tie (all) | 95% | No template file in any variant; the record format lives in the ref. |
| C-007 | L3 | Yes | A | 95% | GitHub mergeability first; local probe only on `CONFLICTING` or persistent `UNKNOWN`. B conceded (R2-B A-B6); C agrees (R2-C C-007). |
| C-008 | L3 | Yes | A (B equal) | 95% | Read-only `merge-tree -z` probe before any merge; A's `parse_stage_records` with a captured fixture plus B's thin emitter (all three R2). |
| C-009 | L3 | Yes | B | 95% | Narrowest tiers; whitespace out; tree conflicts are Tier 2 (all three R2). |
| C-010 | L3 | Yes | B + A shape | 95% | `uv.lock` with stage set `123` only, expressed as one A `MechanicalRule` row (all three R2). |
| C-011 | L3 | Yes | B | 75% | B's extended Tier 3 classes (U-012) carried "uncontested" (R2-C:87); A conceded tier definitions to B (R2-A C-009). |
| C-012 | L3 | Yes | A + B | 80% | A's record with B's high-suspicion checklist as a Tier 3 escalation inside step 2 (U-009, all three R2). |
| C-013 | L3 | Yes | B | 70% | `TIER2_MAX_FILES = 8`, boundary 8 vs 9 (R2-C R-C8). A never conceded its 10 (INV-020). |
| C-014 | L3 | Yes | Split | 90% | All three, on N1 (coupling) and N4 (budget); Tier 3 uses the Wave 0 halt (M3). |
| C-015 | L3 | Yes | B | 95% | L1 reports and continues to review; A conceded (R1-A conc. 9, R2-A R-2). |
| C-016 | L3 | Yes | A state + B timing | 95% | L2 resolves at Wave 8a and stops uncommitted; the caller sets `S4'_HALT_BEFORE_PUSH` (`fsm.py:1118-1121`) (all three R2). |
| C-017 | L3 | Yes | Split | 90% | Tier 2 is re-reviewed via S5a/S5; Tier 1 re-polls CI (all three R2). |
| C-018 | L3 | Yes | Split | 90% | Tier 2 ticks a round; Tier 1 does not (N4). C's `<= 1` bound value is kept (R2-C C-018). |
| C-019 | L3 | Yes | Split | 90% | Re-trigger is mandatory exactly where action is early (N1, N3). |
| C-020 | L3 | Yes | Split | 90% | One edge for Tier 2 only, landing in P2 and pinned like `test_auggie_fallback.py:353-379` (all three R2). |
| C-021 | L3 | Yes | B | 75% | One sibling gate for both tiers (M5, NE1). C agrees (R2-C C-021). A's R2 kept reuse for Tier 2 and did not reply to M5. |
| C-022 | L3 | Yes | B (A equal) | 95% | Strict `[pre_push_sha, base_sha]` order plus a disjointness property test (U-011) (all three). |
| C-023 | L3 | Yes | A/B | 65% | Base-ancestry check present (C conceded X-008); the order of guard steps is still open (X-009). |
| C-024 | L3 | Yes | B | 95% | `finish-merge.sh` subset gate; A conceded (R1-A conc. 7), C conceded (R2-C R-C4). |
| C-025 | L3 | Yes | A/B | 70% | Both advocates call A's per-side allowance and B's stage-1 count equivalent; C conceded scope only (R2-C:87). |
| C-026 | L3 | Yes | A | 80% | Round-inv: all three require a clean tracked tree. A and C halt `merge_preflight_dirty`; B skips the hook and reports instead. |
| C-027 | L3 | Yes | A/C (inferred) | 60% | Mid-resolution halt leaves the merge in progress (A:166, C:62); B aborts (B:391). Not debated. |
| C-028 | L3 | No | unresolved | 50% | Tier 1 VAL converged (`uv lock --check` + VG-3/VG-4, R2-C R-C7). Tier 2 VG-2 is still a three-way split (see X-019). |
| C-029 | L2 | No | unresolved | 50% | Event names and count never settled. Under the split the needed events differ (round-inv B: "no new event type" in P1). |
| C-030 | L3 | Yes | C | 90% | Round-inv: `kind` on all three push records, defaulting to `fix`, now also `ci` (A, B and C INV-001). |
| C-031 | L3 | Yes | Tie (all, hybrid) | 85% | Round-inv: kind-aware recovery. `sync`/`ci` resume into the Wave 8 CI wait with `wait_sha = target_sha`, never S4/S5a/S5. The carrier differs (A `ResumePlan`, B tuple, C directive). |
| C-032 | L3 | Yes | B | 75% | Explicit predicate, value 1 in P1, equal to C's bound (R2-B A-B2, R2-C C-032). |
| C-033 | L3 | Yes | A | 95% | Remove the create-path rebase at L1+ only, as a precursor change (all three). |
| C-034 | L2 | Yes | A name + B default | 95% | `--conflict-max-tier`, default 1 (all three). |
| C-035 | L2 | Yes | B (+C count) | 85% | Round-inv: A withdrew N2 and adopted M6 + QA-2 (`sync_push_count` plus a count field). |
| C-036 | L2 | Yes | A + B | 95% | A's captured fixture for the parser; B's real-repo tests for `finish-merge.sh` (all three). |
| C-037 | L2 | Yes | B | 95% | P0-P3 rollout (all three). |
| C-038 | L2 | Yes | A/B (inferred) | 60% | Both specify per-invocation zdiff3 (A:92, B:347); C rejects it as unneeded (C:43). Not debated. |
| C-039 | L2 | Yes | A | 95% | One `gh pr view` on a normal PR; B conceded (A-B6), C agrees. |
| X-001 | L3 | Yes | Split | 90% | Scored with X-003 (N1-c). Unanimous after Round 2. |
| X-002 | L3 | Yes | Split | 90% | Three-way coupling (R2-C R-C16); unanimous. |
| X-003 | L3 | Yes | Split | 90% | N1 and N3; unanimous. |
| X-004 | L3 | Yes | Split | 90% | Edge only for Tier 2, in P2; unanimous. |
| X-005 | L3 | Yes | B (+C) | 90% | Round-inv: all adopt M6 (Tier 1 counted in `sync_push_count`) plus QA-1/QA-2 pins. |
| X-006 | L3 | Yes | B (A equal) | 95% | Strict order; C conceded (R2-C R-C11). |
| X-007 | L1 | Yes | A/B | 90% | Name `merge_parent_ok`; C's name dropped with its rule. |
| X-008 | L3 | Yes | A/B | 95% | `merge-base --is-ancestor` check; C conceded (R1-C conc. 1). |
| X-009 | L3 | No | unresolved | 50% | Guard order: A puts the ancestry check before the parent check; B puts it after. Neither advocate argued it. |
| X-010 | L3 | Yes | B | 75% | M5 sibling gate; NE1 shows the reuse collides with the S5a gate (B, C). |
| X-011 | L2 | No | unresolved | 50% | Event count unsettled (see C-029). |
| X-012 | L3 | Yes | A state + B timing | 95% | No commit at L2 (T-412); C conceded. |
| X-013 | L3 | Yes | A | 95% | Remove the rebase at L1+ only; L0 stays byte-identical (`test_static_grep.py:649-657`). |
| X-014 | L2 | Yes | A name + B default | 95% | Unanimous. |
| X-015 | L3 | Yes | A/B | 95% | No tree conflict is Tier 1; C conceded (R2-C R-C6). |
| X-016 | L3 | Yes | B | 95% | Whitespace is not mechanical in Python or YAML; A conceded (R2-A R-7). |
| X-017 | L3 | Yes | B | 70% | 8-file cap (B, C); A silent (INV-020). |
| X-018 | L3 | Yes | B (+C) | 70% | Tier 1 runs `uv lock --check` plus VG-3/VG-4 (R2-C R-C7, B:387); A did not respond. |
| X-019 | L3 | No | unresolved | 50% | VG-2 at Tier 2 is a three-way split: mandatory (A:314), forced only for certain paths (B:387), `is_cross_cutting` (C:112). |
| X-020 | L3 | Yes | A/B | 95% | Classify before any mutation; unanimous. |
| X-021 | L3 | Yes | A/C (inferred) | 60% | As C-027. |
| X-022 | L3 | Yes | A/B | 75% | Equivalent introduced-marker rules; C conceded scope. INV-032 notes a hook disagreement. |
| X-023 | L3 | Yes | B | 95% | Subset form; unanimous. |
| X-024 | L3 | Yes | A | 90% | Round-inv: clean tracked tree required by all three (INV-008). |
| X-025 | L2 | Yes | A/B (inferred) | 60% | As C-038. |
| X-026 | L3 | Yes | A | 95% | GitHub first; unanimous. |
| X-027 | L3 | Yes | A | 80% | Up to 3 re-reads 10 s apart, then probe (adopted at R2-B:52, INV-036). |
| X-028 | L3 | Yes | B (+C) | 80% | Value 1 per tier half; A accepts `<= 1` at `C-ci` (R2-A R-11). |
| X-029 | L3 | Yes | B | 75% | `halt:lockfile_no_recipe` inside B's table, carried by C; A conceded the tier table. |
| X-030 | L3 | Yes | Tie (all, hybrid) | 85% | As C-031; B withdrew `S2_CLASSIFY` (round-inv B INV-001). |
| X-031 | L3 | Yes | B | 95% | Unanimous. |
| X-032 | L2 | Yes | B (modified) | 75% | As C-004. |
| X-033 | L3 | Yes | A/B | 95% | `.claude/` is gitignored; C conceded (R2-C R-C6). |
| X-034 | L3 | Yes | A/B | 95% | C conceded; read-only detection at Wave 0 plus `C-initial` after the run-log exists. |
| X-035 | L3 | Yes | A/B | 95% | The probe gives L1 a plan with no merge; C conceded. |
| X-036 | L3 | Yes | A/B | 95% | Tier 1 tree class dropped; C self-flagged. |
| X-037 | L3 | Yes | A (B equal) | 95% | The hook order covers the window; C withdrew its reorder (R2-C R-C3). |
| X-038 | L3 | Yes | A/B | 90% | `BEHIND` is report-only on both paths (R1-C conc. 8). |
| X-039 | L2 | Yes | A/B | 95% | `git commit -F`; C dropped `GIT_EDITOR=true` (R2-C A-004). |
| X-040 | L2 | Yes | A | 95% | B conceded and adopted GitHub-first (A-B6). |
| X-041 | L3 | Yes | B | 95% | A conceded and adopted B:351 "commit and push, or abort" (R2-A R-6). |
| A-001 | L3 | Yes | B gate + A read | 85% | Unanimous QUALIFY: advisory merge-method read, B's P1 real-PR gate, `BLOCKED` reported, never halt on an unreadable value. INV-035 extends it. |
| A-002 | L2 | Yes | Tie (all) | 95% | Unanimous REJECT as stated: the validator checks citation grounding only (NE9). |
| A-003 | L2 | Yes | B rule + C line | 90% | Unanimous: an absent or empty VG-2 caps the run at Tier 1, plus a "no tests found for changed area" report line. |
| A-004 | L3 | Yes | A | 90% | Unanimous: generalize A's allowed-tools test (A:407) to every new inline command. |
| A-005 | L3 | Yes | Tie (all, hybrid) | 90% | Unanimous: reserved `sync-`/`conflict-` prefixes plus one disjointness test (QA-8, NE7). |

### Unique contributions (U-NNN), recorded as contributions, not scored for convergence

| U | Variant | Debate outcome |
|---|---|---|
| U-001 | A | Adopted: `MechanicalRule` shape (R2-B A-S5) |
| U-002 | A | Adopted and generalized to every new inline command (A-004) |
| U-003 | A | Adopted: refs split by tier (R2-B C-003) |
| U-004 | A | Adopted: `pr_conflicting` CI-wait skip (R1-B conc. 2, R2-B U-004, R2-C U-004) |
| U-005 | A | Adopted: captured `merge-tree -z` fixture (C-036) |
| U-006 | A | Adopted in substance as the pure resume function (round-inv A INV-001) |
| U-007 | A | Superseded: under the split, Tier 1 costs no round; Tier 2 cost guidance still applies (INV-021) |
| U-008 | B | Adopted: P0-P3 phasing (unanimous) |
| U-009 | B | Adopted: high-suspicion checklist (unanimous) |
| U-010 | B | Adopted: `finish-merge.sh` gate (unanimous) |
| U-011 | B | Adopted: disjointness property test (unanimous) |
| U-012 | B | Adopted with B's tier table (C-011) |
| U-013 | B | Adopted: real-repo script tests (C-036) |
| U-014 | B | Split: byte-identical fragment test kept; the `<= 346` line-count pin dropped (R1-B conc. 6) |
| U-015 | B | Deferred: P3 late re-sync |
| U-016 | B | Not debated; carried with C-038 (inferred) |
| U-017 | B | Not debated; low-risk carry |
| U-018 | B | Superseded by GitHub-first ordering (C-007) |
| U-019 | C | Dropped: the sequence cannot pass the parent checks (X-037) |
| U-020 | C | Adopted as a Definitions section (all advocates cite it positively) |
| U-021 | C | Adopted and rewritten: the deliberately-untested surface shrinks (R2-C:87) |
| U-022 | C | Dropped with the Tier 1 judgment classes (R2-C R-C6) |
| U-023 | C | Adopted: explicit `BLOCKED` Tier 0 row (R2-A R-12) |
| U-024 | C | Adopted: `== 41` sweep plus the `models.py:23` docstring (QA-6) |

## Taxonomy Coverage Gate

| Level | Diff points | Points debated (explicit positions) | Covered |
|---|---|---|---|
| L1 surface | 12 (S-001..S-007, S-009, S-011, S-013, S-014, X-007) | S-005, S-009, S-014, X-007 | Yes |
| L2 structural | 25 | e.g. C-001..C-004, C-034..C-037, X-014, X-032, A-002, A-003 | Yes |
| L3 state mechanics | 63 | e.g. C-014, C-016..C-022, X-001..X-006, X-012, X-023, all A-001/004/005 | Yes |

Result: **PASS**. All three levels have more than 0 points addressed, so no forced round was triggered.

## Invariant Probe Gate

### Before the resolution round (after Round 2.5)

```
CONVERGENCE BLOCKED: 4 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-008, INV-033, INV-034
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

MEDIUM warning, 16 items: INV-002, 003, 004, 005, 009, 010, 011, 012, 013, 014, 018, 022, 027, 030, 031, 035.

### After the resolution round (gate re-applied by the orchestrator)

Rule applied: a HIGH item is ADDRESSED only if the three resolutions agree on a concrete rule, or the majority agrees and the minority does not reject it. Differences that do not affect the invariant (return shape, file carrier, reason-code spelling) do not count as disagreement.

| INV | A | B | C | Shared concrete rule | Invariant-relevant disagreement? | Gate status |
|---|---|---|---|---|---|---|
| INV-001 | `kind` on all push records (`fix`/`merge`/`sync`/`ci`). Pure `crash_resume_plan` sends `sync`/`ci` to `ci_wait` with `wait_sha=target_sha`. Branch B re-drives through the guard plus `merge_parent_ok`. Never `S4_PUSHING`. | `kind` plus `review_terminal` on `push_initiated`. `sync`/`ci` give Wave 8 `source=ci`, `wait_sha=target_sha`. Branch B re-drives through the guard plus `merge_parent_ok`. A missing terminal fails closed (`resume_unrepresentable`). | `kind` in the key tuple. `sync`/`ci` give the directive `{reenter: wave8_ci_wait, wait_sha, preserve_terminal}`. Branch B re-drives then gives the directive. `fix`/`merge`/absent unchanged. | Kind-aware recovery. `sync`/`ci` resume into the Wave 8 CI wait at `target_sha` with the preserved review terminal, never S4/S5a/S5. Branch B re-runs the pre-push guard (plus the merge-parent check for `sync`). Legacy and absent kinds behave as today. | No. Only the carrier differs (plan object, tuple or directive) and where the preserved terminal is stored. None rejects the others. | **ADDRESSED** (also closes MEDIUM INV-002 via kind `ci`) |
| INV-008 | Clean tracked tree (staged or unstaged) else HALT `merge_preflight_dirty`. Untracked rule inputs are refused. `finish-merge.sh` re-checks. | Clean tracked tree (`--untracked-files=no`), else skip the hook, record `conflict_skipped: dirty_tree` and report (no halt). `finish-merge.sh` asserts before the regenerate and after the commit. | Clean tracked tree for both tiers, else HALT `merge_preflight_dirty`. Untracked tolerated. | Act only on a clean tracked tree; untracked files tolerated; re-assert in `finish-merge.sh` immediately before the regenerate and commit. | No. Halt (A, C) versus skip-and-report (B) is a choice of action after a correct refusal. In every version nothing is merged on a dirty tree, so committed tree = validated tree holds. | **ADDRESSED** (action: majority HALT) |
| INV-033 | Keep the rule; the spec states it is a no-op here. P1 gate = a real-git end-to-end test in a pytest temporary directory with a tracked `uv.lock` (`uv lock --offline`) plus a live L3 run on an `IronbellyOrg` sandbox repo (the user decides; never upstream). | Keep the rule; runtime applicability check (tracked, `uv` on PATH). P1 gate = a hermetic real-git test (stub `uv` plus a skipif real-uv case) plus a live L3 run on throwaway branches in this repo that force-add `uv.lock`. | Keep the rule. P1 gate = a fixture repo with real git and real uv, no network (automated) plus a manual live L3 run on a scratch repo. Do not un-ignore `uv.lock` here. | Keep the `uv.lock` rule; state that it is a no-op in IronClaude; P1 gate = one hermetic real-git automated test plus one manual live L3 run on a repo that tracks `uv.lock`. | No. Where the live run happens (sandbox repo for A/C, in-repo throwaway branches for B) does not affect the finding; nobody rejects another's location. Majority: a separate repo. | **ADDRESSED** (live gate waits on the user) |
| INV-034 | After a push, CI counts only when checks exist for `wait_sha`: `poll-ci-checks.sh --wait-sha` emits `sha_checks` via the check-runs and status API, and `classify_checks(expect_checks=...)` returns `polling` on 0. Timeout gives `ci_not_started`, never clean. **Rejects a settle window: "racy, so it is rejected".** | `classify_checks(after_push, empty_polls, settle_polls=3)`: an empty pair stays `polling` for up to 3 polls, after which the report says "no checks registered after N polls". Also emits `mergeable` and refuses `clean` while `CONFLICTING`. Defers the check-runs API to an open question. | Grace rule: an empty list after a push stays `polling` until checks appear or grace (about 1 poll interval) expires, after which it is `clean`. `empty_clean_ok=False`; script unchanged. **Rejects the check-runs API.** | Shared: after a push, an empty parsed list for `wait_sha` is `polling`, not `clean`, through a new `classify_checks` keyword whose default keeps today's behaviour. **Not shared:** how waiting ends, and whether a no-checks end may report `clean`. | **Yes.** B and C bound the wait with a settle window (C then allows `clean`). A rejects that window explicitly, because a slow check registration on a previously conflicting PR (the case INV-034 names) outlasts the window and reads `clean` again. C rejects A's registered-checks signal. | **UNADDRESSED: still blocks** |

```
CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-034
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

**MEDIUM items after the resolution round:**

| INV | A | B | C | Gate result |
|---|---|---|---|---|
| INV-002 | `ci` kind | `ci` kind | `{sync, ci}` | ADDRESSED (via INV-001) |
| INV-003 | adopt | adopt | adopt | ADDRESSED. L2 sets S4' only after `clean`/`REPORT_ONLY`; from a preserved terminal it only reports. |
| INV-004 | adopt (`operation_in_progress`) | adopt (`foreign_op_in_progress`) | adopt (`merge_in_progress`) | ADDRESSED. Unconditional Wave 0 local `MERGE_HEAD`/rebase/cherry-pick check; only the reason code is unsettled. |
| INV-009 | adopt | adopt | adopt | ADDRESSED. Rewrite the three wait-only sentences and add a static pin; the wording differs. |
| INV-010 | adopt (same action at L2 and L3, plus a monotonicity property test) | defer (drop Tier 2 resolution at L2) | accept as risk | **Still a WARNING**: three-way split |
| INV-018 | adopt M6 (withdraws N2) | adopt M6 | adopt M6 + QA-1/QA-2 | ADDRESSED |
| INV-035 | adopt (pre-push refusal on rebase-only; rejected push gives HALT `push_rejected`, no re-drive) | cheap half (rejected push gives HALT `push_rejected`; Branch B never re-drives a `rejected` record; proactive detection is an open question) | defer (advisory read; proposes one re-drive then `HALT_HUMAN`) | ADDRESSED on the majority rule: a rejected push halts `push_rejected` and is never re-driven. Proactive refusal stays an open question; C does not reject the halt. |

```
WARNING: 10 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-005, INV-010, INV-011, INV-012, INV-013, INV-014, INV-022, INV-027, INV-030, INV-031
These items do not block convergence but should be reviewed.
```

INV-027 is partly covered by B's INV-034 resolution, which refuses `clean` while `CONFLICTING`. That resolution is not adopted because INV-034 is unresolved. The LOW items (INV-016, 019, 020, 021, 025, 032) need no gate action and are carried into the refactor plan.

## Convergence Assessment

- Points resolved: 90 of 100. The denominator is S 15 + C 39 + X 41 + A 5. The 24 U points are contributions and are not counted.
- Alignment: **90%** (agreed_points / total_diff_points = 90 / 100 = 0.90)
  - Sensitivity, excluding the 9 points agreed only by inference (S-006, S-011, S-012, S-013, C-027, C-038, X-021, X-025, plus C-023 as partial): 81/100 = 81%, still above the threshold.
  - Trajectory: after Round 2, 83/100. After the invariant-resolution round, 90/100.
- Threshold: 75%
- Taxonomy gate: PASS (L1 12, L2 25, L3 63; all covered)
- Invariant gate: FAIL after the invariant-resolution round (1 HIGH UNADDRESSED: INV-034); PASS after the INV-034 focused round (0 HIGH UNADDRESSED).
- Oscillation: none. The coupled points moved once, from inconsistent R1 majorities to a unanimous Split in R2, and did not flip back.
- Status: **CONVERGED** (was BLOCKED_BY_INVARIANTS before the INV-034 focused round)
- Unresolved points (10): S-001, S-002, S-003, S-004, S-007, C-028, C-029, X-009, X-011, X-019. Five are L1 presentation points. The five substantive ones are VG-2 at Tier 2 (C-028/X-019), the run-log events and count (C-029/X-011) and the pre-push guard order (X-009).
- Remaining HIGH UNADDRESSED invariant: none. INV-034 was resolved by the focused round below; Steps 3 and 4 had gone ahead before it, and the refactor plan was updated to carry the agreed R-034′ rule.

## INV-034 Focused Round (second extra round, gate-mandated)

Files: `round-inv034-brief.md` (orchestrator candidate R-034: use the replaced head's checks as evidence), `round-inv034-advocate-A.md`, `round-inv034-advocate-B.md`, `round-inv034-advocate-C.md`.

| Advocate | Verdict | Rule |
|---|---|---|
| A | MODIFY | R-034′: `expect_checks` is true if checks were seen earlier in the run, or `pre_push_sha` or `base_sha` has at least one check run or status context (commit-scoped `gh api repos/$REPO/commits/<sha>/check-runs` and `/status`, read by `poll-ci-checks.sh --evidence-sha`, `-1` on a failed read = had checks); recorded in the run-log for resume; `classify_checks(..., expect_checks=False)` returns `polling` on an empty chosen list when true; expiry is a timeout with reason `ci_not_started`, never clean. |
| B | MODIFY | Same keyword and fail-closed rule; evidence (a) earlier checks, (b) the replaced head read BEFORE the push, (c) a conflict-sync push always expects checks. Notes the Wave 8 expiry is the existing `timed_out` result, not the review-phase `TERMINAL_TIMEOUT`. |
| C | MODIFY | Same as A: commit-scoped evidence for `pre_push_sha` OR `base_sha`, fail closed; withdraws the grace window; lists 7 acceptance tests (empty + expect + matching head = polling; nonempty overrides; default unchanged; existing tests unmodified; head mismatch = polling; evidence setter cases; live leg). |

Agreement: all three withdraw time windows and agree on the `expect_checks` keyword (default off), `polling` on empty when expected, fail-closed evidence, and never reporting `clean` or "tests passed" with no registered check. A and C agree on the exact evidence set; B's rule (c) is stricter and is satisfied by the commit-scoped `pre_push_sha`/`base_sha` read (check runs persist on a commit after its PR turns conflicting, per A and C), so B does not reject R-034′. Merged rule: **R-034′ as written by A**, with B's correction that the Wave 8 expiry uses the existing CI `timed_out` path (reason `ci_not_started`) and C's acceptance tests. Gate result: **INV-034 ADDRESSED.**
