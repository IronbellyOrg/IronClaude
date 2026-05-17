# Adversarial Debate Transcript

## Metadata

- Depth: deep (3 rounds + Round 2.5 invariant probe)
- Rounds completed: 3 + Round 2.5
- Convergence achieved: 86% (43 / 49 diff points resolved; 1 BLOCKED by HIGH-severity invariant gate before reconciliation; 5 unresolved by reasoned non-resolution)
- Convergence threshold: 85%
- Focus areas: tradeoffs, invariants, failure-modes, evidence
- Advocate count: 3 (blind attribution: Advocate-1 / Advocate-2 / Advocate-3)
- Taxonomy coverage: L1 (3 points: S-005, U-008, C-014), L2 (18 points: structural and CR-ID groupings), L3 (28 points: state mechanics, invariants, guard conditions, atomicity, resumability — all six X-NNN contradictions auto-tagged L3)

## Round 1 — Advocate Statements (parallel)

### Advocate-1 (Variant-1 — steelman stance)

**Position summary.** The source plan is sound as binding. Its eight closures (F-01..F-08) and three sequencing constraints (S-1..S-3) are correctly dispositioned; the "zero open findings" claim survives at the level the closures define soundness. Three other reads of the plan introduce noise that does not survive the steelman.

**Steelman of Advocate-2.** Advocate-2's strongest version: the plan's closures are written in prose that admits multiple operational readings; under the most adversarial reading, several closures leave degenerate-input behaviors unspecified (F-02 grep semantics, F-03 git failure modes, F-04 baseline trinary). This is a real concern at the predicate-precision level even when the closure's chosen reading is correct.

**Steelman of Advocate-3.** Advocate-3's strongest version: the plan defends invariants at the *skill layer* (TU/ME/closures), but the merge sequence operates across a *temporal* layer (Steps 5–10) where in-flight artifacts authored against the pre-merge surface live. INV-04 resumability has a parse-level guarantee and a semantic-level exposure that the plan does not separate.

**Strengths claimed (with evidence).**
1. Per-TU steelman maps each transfer unit to specific invariants it protects (V1 § 2, lines 19–81) — generative defense framework that Advocates-2/3 do not replicate.
2. Individual ME-1..ME-9 "what breaks without it" analysis (V1 § 3) — Advocate-2 attacks the closures but does not show what holds them up.
3. F-03 / F-04 Reading-A defense names *why* the other readings fail the invariants (V1 § 5, lines 153–159) — Advocate-2 attacks ambiguity but does not show that any other reading would be invariant-preserving.

**Weaknesses identified (with evidence).**
1. Advocate-2's F-02 alternation-order attack (V2 § 2.4) is correct at the regex level; the V1 defense at line 31 ("structurally enforceable") is too strong.
2. Advocate-2's 79→65 bucket-condensation gap (V2 § 5.1) and 67-vs-65 duplicate-row gap (V2 § 5.2) are real traceability defects V1 does not address.
3. Advocate-3's 96-file in-flight evidence (V3 § 2) is empirically grounded and surfaces an INV-04 semantic exposure V1 mis-states as fully covered by CR-FM-03.

**Concessions in own variant.**
- V1's F-02 defense is weaker than claimed (concedes to V2 attack).
- V1's INV-04 SURVIVES claim does not separate parse-level from semantic-level (concedes to V3).
- V1 does not enumerate the 79→65 condensation table (concedes to V2).

**Shared-assumption responses.**
- A-002 (anchor-source byte-stability): **QUALIFY** — line-pinned references do drift on edits; the plan's authority chain assumes byte-stability of `extension-point-contracts.md:11-17`. The qualification is that retroactive `invariant-bounds.md` authoring (F-06) could substitute symbol-pinning for line-pinning.
- A-003 (ledger completeness): **ACCEPT** — the steelman accepts ledger authority as load-bearing for R-RULE-11.
- A-004 (single accountable executor): **QUALIFY** — the steelman assumes this but acknowledges the plan does not name the role.
- A-005 (Phase 7 artifact accuracy): **ACCEPT** — independent re-read is named at line 447, even if grep patterns are unspecified.

### Advocate-2 (Variant-2 — adversarial-attack stance)

**Position summary.** The "ZERO OPEN FINDINGS" claim (source line 46) is a definitional verdict, not an operational one. Fifteen falsifiable acceptance criteria (AC-ATK-01..15) identify under-specified predicates, structural fragility, and unbudgeted tradeoffs across F-01..F-08. The plan is "binding" only in the procedural-paper-trail sense; the operational guarantees are weaker than asserted.

**Steelman of Advocate-1.** Advocate-1's strongest version: the closures resolve the *Phase-7-named* findings cleanly, the V/C/K verdicts carry forward zero-drift, the ledger is not re-litigated, and the 10-step canonical sequence has a defensible shape. Advocate-1 is right that an attack must not silently re-open a REJECTed feature.

**Steelman of Advocate-3.** Advocate-3's strongest version: the plan's failure-mode register lives in `compat-hazard-report.md` HZ-01..HZ-18, and any new hazard outside that register is genuinely additive rather than re-litigating closed findings. Advocate-3 has the strongest evidence basis (96-file grep, named PRD subtree exposure).

**Strengths claimed (with evidence).**
1. Twenty-three falsifiable attacks (V2 §§ 2–4) — every attack cites a specific source line and names a broken or eroded invariant. Advocate-1's defense uses TUs and MEs but does not test predicates at the regex / file-state level.
2. Bucket-condensation and row-count discrepancies (V2 §§ 5.1–5.2) identify traceability gaps that defeat AC #1 of the plan's own validation hooks.
3. Eight unnamed tradeoffs per closure (V2 § 9) — closures are presented as costless tightening; the tradeoffs (F-01 unbounded read channel, F-02 audit-tool/source coupling, F-03 dirty-tree partial-state, F-04 unbounded queue, F-05 evidence-basis-shift, F-06 line-coupled-anchor, F-07 no-automation, F-08 propagation-to-merge-master) are real and unbudgeted.

**Weaknesses identified (with evidence).**
1. Advocate-1's per-TU defense is well-organized but does not test predicate precision — Advocate-1 names invariants protected without demonstrating they survive degenerate inputs to the closures.
2. Advocate-3's 96-file evidence is strong, but the recommendation to extend CR-FM-03 with content-level audit risks introducing a new HALT semantic at resume time — Advocate-3 must clarify warn-and-continue.
3. Advocate-1's "5 honest concessions" section is brief; the actual gap surface is broader than five points.

**Concessions in own variant.**
- V2 does not address S-2 / S-3 atomicity at the rebase-split layer (concedes to V3).
- V2 does not provide live evidence of in-flight task exposure (concedes to V3).
- V2's F-05 precedent-template attack is theoretical; no concrete future widening is named that would exploit the precedent.

**Shared-assumption responses.**
- A-002 (anchor-source byte-stability): **REJECT** — surfaces as F-06 tradeoff in V2 § 9. The line-pinned anchor IS brittle; a formatting commit to `extension-point-contracts.md` silently breaks the citation. The plan does not bind anchor stability.
- A-003 (ledger completeness): **QUALIFY** — accept as boundary for R-RULE-11, but the ledger's own audit is not in scope and could itself be drifted from the actual debate history.
- A-004 (single accountable executor): **REJECT** — the plan reads to a hand-off chain across Steps 1–10; no single role is named for the chain.
- A-005 (Phase 7 artifact accuracy): **QUALIFY** — V2 § 11 raises EC-01..04 evidence gaps in the plan's own validation hooks; the artifact accuracy is not re-verified.

### Advocate-3 (Variant-3 — security-probe stance)

**Position summary.** The plan's "18/18 compat hazards MITIGATED" claim (source line 43) holds at the per-CR-row layer the plan defines mitigation. Six new hazards live at the timeline / tooling layer that row-level mitigations do not reach. INV-04 is the most exposed invariant: 96 in-flight files reference deprecated surfaces and CR-FM-03's "validate clean / NO migration" detects none of the legacy-surface references their checklists contain.

**Steelman of Advocate-1.** Advocate-1's strongest version: the plan's invariant survival is *demonstrated, not asserted* via the worked example in `invariant-survival-walkthrough.md`. The 16-row counter-factual register, the TU-by-TU interaction table, and the per-invariant survival argument are stronger evidence than any other Phase 7 sprint's. The steelman is correct that this is the highest-evidence merge plan in the surrounding sprint history.

**Steelman of Advocate-2.** Advocate-2's strongest version: every claimed defect is falsifiable. The F-02 grep attack, the F-03 git-failure-mode coverage, the F-04 trinary observer-disagreement, the CR-TASK-12 post-CR-DEP-03 fragility, and the 79→65 bucket-condensation gap are all decidable by examining the source plan's text — they are not speculative.

**Strengths claimed (with evidence).**
1. Live empirical grounding (V3 § 2) — 96 task files, 149+ refs in named PRD subtree, file paths for in-flight tasks: TASK-TDD-20260514-121250, TASK-RF-20260515-195758, TASK-RF-20260403-tasklist-e2e, TASK-RESEARCH-20260403-sprint-task-exec.
2. INV-04 semantic-vs-parse distinction (V3 § 7, § 9) — the plan's "SURVIVES" claim and Advocate-1's defense lean on CR-FM-03 "validates clean" which is a parse-level check that does NOT see content references to deprecated surfaces.
3. S-2 rebase-split bypass (V3 § 4, H-2) — pre-commit pytest gate does not run on rebase; `git rebase -i` permits commit-split; recommends server-side pre-push hook re-grepping the landing commit at master.

**Weaknesses identified (with evidence).**
1. Advocate-1's INV-04 SURVIVES verdict is over-broad — V3 demonstrates 96-file semantic exposure that the source plan's argument does not cover.
2. Advocate-2's CR-TASK-11 md5 attack is theoretical and adversarial; in practice the concern is filesystem race or accidental collision, both extremely unlikely.
3. Advocate-1's F-03 defense conflates "INV-01 progress preservation" with "INV-01 is the only relevant invariant" — F-03 does not address what happens when pre-flight produces ambiguous output (Advocate-2's gap).

**Concessions in own variant.**
- V3 does not address F-01 / F-02 / F-04 closure predicates (focus stayed on deprecation chain; concedes that V2's per-closure attacks fill the gap).
- V3's CR-FM-03 content-level audit recommendation needs a HALT-policy disposition (must be warn-and-continue per ME-3, not refuse-entry).
- V3 does not enumerate 79→65 or 67-vs-65 traceability gaps (concedes to V2).

**Shared-assumption responses.**
- A-002 (anchor-source byte-stability): **REJECT** — concur with V2; V3 also surfaces SKILL.md:191-198 anchor brittleness in § 9.
- A-003 (ledger completeness): **ACCEPT** — V3 stays outside ledger re-litigation by design.
- A-004 (single accountable executor): **QUALIFY** — V3 § 3 mitigation explicitly names a `--max-wait` decision authority is needed; concur with V2 that the plan does not.
- A-005 (Phase 7 artifact accuracy): **ACCEPT** — V3 cites artifacts but does not re-verify their content; this is an out-of-scope concession.

## Round 2 — Sequential Rebuttals

### Advocate-1 rebuttal (responding to R1)

**Conceded points (with rationale).**
1. F-02 alternation-order attack (V2 § 2.4 / X-001): conceded — the grep is occurrence-order, not call-site-order; defense from V1 line 31 was too strong. Resolution: F-02 closure should be tightened with line-range-pinned or AST-level check (per V2's AC-ATK-01). V1 retreats from "structurally enforceable" to "audit-tool-coupled, structurally bounded."
2. INV-04 SURVIVES is semantic-thin (V3 § 7 / X-005): conceded — V1's defense leaned on CR-FM-03 which is parse-level. The 96-file evidence is empirical and decisive. Resolution: extend CR-FM-03 with content-level audit per V3's recommendation, with the HALT-policy correction (warn-and-continue, per ME-3).
3. 79→65 / 67-vs-65 traceability gaps (V2 §§ 5.1–5.2): conceded — the plan does not enumerate these. Resolution: add a bucket-condensation table as a Phase 7.5 patch.

**Defended points (with rationale).**
1. F-03 Reading A is still correct (V2 X-002). V2 argues CR-TASK-02 task-level malform is also a HALT, creating inconsistent policy. But CR-TASK-02 is a *parse-error* HALT (the task file is structurally invalid), whereas git-dirty is an *environmental* condition (the task file is valid; the surrounding state is not clean). These are different categories: invalid input vs valid input under non-ideal conditions. The asymmetry is justified. (Resolution: V2's AC-ATK-10 — unified HALT policy table — should distinguish "input-invalid" from "environment-non-ideal" rows.)
2. F-05 third-invocation is still authorized (V2 X-003). V2's "precedent template" attack is correct that ME-2 + spawn-pattern + TU-7-recipient-form is replicable, but the plan's obligation #7 (source line 425) does bind future widenings to manifest exception authorship. V2's claim that this "does not retroactively bind the F-05 author's own pattern" is a fair concern but is a meta-point about precedent culture, not a falsifiable invariant attack. (Resolution: add a one-time-carve-out disclaimer to § 0 explicitly closing the precedent loophole.)
3. F-07 procedural chain is still defensible (V2 X-004). V2 calls it "paper trail with no signatory" — but the absorption traceability (source line 183) is the structural signatory: every absorbed pattern landed at `[src] skills/task/SKILL.md`, which is grep-verifiable. (Resolution: name `rf-qa` as the verifier role for chain-integrity at Step 6 pre-commit; gives V2 the role-binding without inventing a new agent.)

### Advocate-2 rebuttal (responding to R1)

**Conceded points (with rationale).**
1. V1 per-TU steelman is generative (V1 § 2 / U-001): conceded — V2's attack list is wide but does not produce a defense framework. V1's invariants-protected mapping should be preserved in the merged spec as a positive-validation overlay alongside V2's attack list.
2. V3 96-file evidence (V3 § 2 / U-012): conceded — V2's INV-04 attack at CR-FM-03 shim sunset was abstract; V3's empirical grep is decisive. The merged spec should adopt V3's CR-FM-03 content-level audit + V2's shim-sunset audit row as complementary.
3. F-03 input-invalid vs environment-non-ideal asymmetry (V1 R2): conceded — V2's "inconsistent HALT policy" attack does not survive once the asymmetry is named. Resolution: V2's AC-ATK-10 amends to enumerate the two categories.

**Defended points (with rationale).**
1. F-02 grep is still defective at the regex level (V1 R2 concedes). The right fix is line-range-pinned or AST-level check (AC-ATK-01); V1's R2 concedes this.
2. F-04 baseline trinary observer-disagreement (V2 § 3.5 / C-003): not yet conceded by V1. The closure says `absent|empty|malformed` but does not name *which observer* determines each state. A YAML file containing `null` is observer-dependent: `os.path.getsize > 0` says non-empty; `yaml.safe_load -> None` says empty. The plan does not specify observation order. V1 has not addressed this.
3. CR-TASK-12 seven-diff post-CR-DEP-03 fragility (V2 § 3.10): V1 silent in R1 and R2. V3 concurs (V3 § 6). Resolution: snapshot donor strings into frozen fixture before Step 6 OR mark CR-TASK-12 Step-4-only with successor-audit obligation.

### Advocate-3 rebuttal (responding to R1, R2)

**Conceded points (with rationale).**
1. F-05 precedent loophole closure (V1 R2): concur — explicit one-time-carve-out disclaimer in § 0 is the right shape.
2. F-07 verifier-role binding (V1 R2): concur — `rf-qa` as the chain-integrity verifier at Step 6 pre-commit gives V2's role-binding without re-litigating manifest authorship.
3. V2 79→65 / 67-vs-65 traceability gaps (V2 §§ 5.1–5.2): concur — these are decisive gaps V3 did not surface and the merged spec must close them.

**Defended points (with rationale).**
1. INV-04 semantic-vs-parse distinction (V3 § 7 / X-005). V1 R2 conceded; V2 R2 conceded. Resolution: the merged spec adopts the distinction explicitly.
2. S-2 rebase-split bypass (V3 § 4 / C-006). V1 silent; V2 silent. V3 recommends server-side pre-push hook. This is a structural barrier the plan currently lacks — pre-commit pytest only catches pre-commit-time state.
3. Worktree race during sync-dev (V3 § 5 / C-007). V1 silent; V2 silent. CLAUDE.md authorizes worktrees; the plan does not address `flock` discipline. Resolution: § 7 obligation #1 extension.

### Late additions — Advocate-1 and Advocate-2 cross-acknowledgments

**Advocate-1 final acknowledgments.** Conceding V3's S-2 rebase-split bypass (V3 § 4) — pre-commit gates do not run on rebase; this is an operational hazard the steelman's defense of S-2 at line 135 does not address. The server-side pre-push hook recommendation should be adopted as a structural barrier.

**Advocate-2 final acknowledgments.** Conceding V3's worktree-race hazard (V3 § 5 H-3) — V2's attack list did not include filesystem race conditions during `make sync-dev` prune. The `flock` mitigation is additive to V2's AC-ATK list as AC-ATK-16.

## Round 2.5 — Invariant Probe (independent fault-finder)

See `invariant-probe.md` for the detailed table. Summary:

- **9 findings total** across 5 categories (state_variables: 2, guard_conditions: 2, count_divergence: 1, collection_boundaries: 2, interaction_effects: 2)
- **ADDRESSED: 5** — covered by consensus during R2
- **UNADDRESSED HIGH: 1** — INV-04 semantic exposure on 96 in-flight files (route through CR-FM-03 content-level audit)
- **UNADDRESSED MEDIUM: 3** — F-04 observer ordering, CR-TASK-12 lifetime, S-1 unbounded wait

**Convergence gate.** 1 HIGH UNADDRESSED → BLOCKED convergence until the consensus explicitly takes a position on INV-04 semantic exposure. Round 3 was triggered to resolve this.

## Round 3 — Final Arguments (post-invariant-probe)

### Advocate-1 final position

The remaining HIGH UNADDRESSED invariant (INV-04 semantic exposure on 96 files) is resolved by the merged spec adopting V3's CR-FM-03 content-level audit extension with the explicit HALT-policy disposition: **warn-and-continue per ME-3**, not refuse-entry. This preserves INV-01 progress and surfaces INV-04 semantic exposure as Task-Log evidence rather than blocking the resume.

Final concessions: V1 fully retreats from the "structurally enforceable" claim at F-02 (line 31); accepts the bucket-condensation table requirement; accepts the INV-04 semantic-vs-parse distinction; accepts the server-side pre-push hook and flock recommendations as additive obligations.

### Advocate-2 final position

The 23 falsifiable attacks resolve to a tractable list once V1's "input-invalid vs environment-non-ideal" asymmetry (R2) and V3's empirical grounding (R1) are absorbed. AC-ATK-01..16 (V2's 15 + V3's flock as AC-ATK-16) are the auditable closure obligations.

Final concessions: V2 accepts the F-03 asymmetry distinction; accepts that obligation #7 plus a one-time-carve-out disclaimer closes the F-05 precedent loophole; accepts `rf-qa` as the F-07 chain-integrity verifier role.

### Advocate-3 final position

The 6 timeline/tooling-layer hazards (H-1..H-4, sync-race, residual-reference) are additive to the source plan's HZ-01..HZ-18 register and do not re-open any rejected-ledger entry. The plan should be amended with HZ-19..HZ-24 and S-4 (PRD timeout) + S-5 (rebase-ban on Step 5/6 commits) as part of a Phase 7.5 patch.

Final concessions: V3 accepts that the F-04 baseline trinary observer-disagreement (V2's gap) is in scope but not in V3's stance; the merged spec adopts V2's four-state table {absent, empty, parse-fail, schema-fail}.

## Scoring Matrix (per-point winner with confidence)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 (section count) | tie | 50% | Each variant's structure fits its stance; no superior shape |
| S-002 (organizing axis) | tie | 50% | TU/ME (V1), CR-ID (V2), and sequencing-constraint (V3) axes are complementary; merged spec adopts all three |
| S-003 (AC blocks) | V2 | 75% | AC-ATK-01..15 are most numerous and most operationally specific; V1's AC-SM-* and V3's mitigation table are augmentations |
| S-004 (concrete scenarios) | V2 + V3 | 80% | Seven (V2) + four (V3) state-trace scenarios; V1 has none |
| S-005 (frontmatter stance) | tie | 50% | Cosmetic |
| S-006 (verdict shape) | V3 | 70% | V3's partial-affirm framing is most operationally honest; V2 indictment + V1 ratify both overshoot |
| C-001 (F-02) | V2 | 90% | Alternation-order attack is falsifiable; V1 R2 conceded |
| C-002 (F-03) | V1 | 70% | Reading-A defense + asymmetry distinction holds; V2 R2 conceded the asymmetry |
| C-003 (F-04) | V2 | 80% | Observer-disagreement attack not refuted; V3 R3 concurs |
| C-004 (F-05) | V1 + V2 hybrid | 75% | V1's authorized-widening defense + V2's precedent-loophole closure via § 0 disclaimer |
| C-005 (S-1) | V3 | 85% | Concrete `--max-wait` + pinned-SHA recommendations decisive; V1 / V2 did not produce mitigations |
| C-006 (S-2) | V3 | 90% | Rebase-split bypass + server-side pre-push hook decisive; V1 / V2 silent |
| C-007 (S-3) | V3 | 80% | Worktree race + flock recommendation; V1 / V2 silent |
| C-008 (79→65) | V2 | 95% | Decisive — table absent from plan; V1 / V3 silent |
| C-009 (67-vs-65) | V2 | 90% | Decisive — duplicate rows unnamed; V1 / V3 silent |
| C-010 (CR-TASK-12) | V2 + V3 | 85% | Both surface fragility; V3 § 6 + V2 § 3.10 converge on snapshot-fixture mitigation |
| C-011 (INV-04 depth) | V3 | 95% | 96-file empirical evidence is decisive; V1 / V2 attacks lacked grounding |
| C-012 (F-07 chain) | V1 + V2 hybrid | 70% | V1's absorption-traceability defense + V2's verifier-role binding combine |
| C-013 (in-flight content audit) | V3 | 100% | Unique to V3; no counterpart in V1 / V2 |
| C-014 (md5) | V2 | 60% | Adversarial-only concern; mitigation is mechanical (sha256) |
| C-015 (sentinel type) | V2 | 75% | Markdown-comment-as-binding is type-confusion; V1 R2 conceded |
| X-001 (F-02) | V2 | 90% | See C-001 |
| X-002 (HALT consistency) | V1 | 75% | Asymmetry distinction resolves; V2 R2 conceded |
| X-003 (F-05 precedent) | V1 + V2 hybrid | 70% | One-time-carve-out disclaimer closes the loophole |
| X-004 (F-07 trust basis) | V1 + V2 hybrid | 70% | See C-012 |
| X-005 (INV-04) | V3 | 95% | See C-011 |
| X-006 (verdict) | V3 | 75% | Partial-affirm is the most operationally honest framing |
| U-001..U-018 | various | 50–100% | Each unique contribution evaluated on its own merit; all 18 are adopted into refactor plan |
| A-001 | (no debate) | — | STATED; not promoted |
| A-002 (anchor stability) | V2 + V3 reject + V1 qualify | 85% | Adopt: symbol-pinning over line-pinning where feasible; F-06 retroactive `invariant-bounds.md` upgrade |
| A-003 (ledger completeness) | V1 + V3 accept; V2 qualify | 80% | Adopt: accept as R-RULE-11 boundary; document ledger audit as out-of-scope |
| A-004 (single executor) | V2 reject + V3 qualify | 80% | Adopt: name the merge-sprint executor role explicitly in § 7 |
| A-005 (Phase 7 artifact accuracy) | V1 + V3 accept; V2 qualify | 80% | Adopt: re-verification is out-of-scope but EC-01..04 grep-pattern specifications close validation-hook gaps |

## Convergence Assessment

- Points resolved: 43 of 49 (86%)
- Alignment: 86% — meets the 85% threshold
- Threshold: 85% (configured via --convergence 0.85)
- Status: **CONVERGED** (after Round 3 resolves the 1 HIGH UNADDRESSED invariant)
- Unresolved points (acceptable non-resolution):
  - S-001 (section count) — cosmetic; no superior shape exists
  - S-005 (frontmatter stance label) — cosmetic
  - A-001 (INV-01..INV-05 completeness) — out of scope; would require sixth-invariant proposal
  - C-014 (md5 collision) — accepted as mitigation but classified as adversarial-only; LOW severity
  - Two further low-severity diff points within the bucket of U-001..U-018 where the steelman framing and the attack framing are both adopted side-by-side (i.e., the "winner" is "both")

**Taxonomy coverage:** L1 (3 points), L2 (18 points), L3 (28 points). All three levels are covered — no forced round triggered.

**Invariant probe gate:** 0 HIGH UNADDRESSED items remain after Round 3 resolved INV-04 semantic exposure via CR-FM-03 content-level extension with warn-and-continue HALT disposition. Convergence is not blocked.
