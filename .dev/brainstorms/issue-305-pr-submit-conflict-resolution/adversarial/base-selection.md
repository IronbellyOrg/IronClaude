# Base Selection Report

- Variants: A = `variant-1-opus-architect.md` (opus:architect), B = `variant-2-sonnet-refactorer.md` (sonnet:refactorer), C = `variant-3-haiku-qa.md` (haiku:qa)
- Inputs: the three variants, `debate-transcript.md` (scoring matrix), `diff-analysis.md` (contradictions and spot-checks), `../seed-brief.md` (source requirements)
- Scored: 2026-11-04T14:57:36Z by the debate-orchestrator

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (opus:architect) | Variant B (sonnet:refactorer) | Variant C (haiku:qa) |
|---|---|---|---|---|
| requirement_coverage (RC) | 0.30 | 1.0000 (35/35) | 1.0000 (35/35) | 0.9429 (33/35) |
| internal_consistency (IC) | 0.25 | 0.9977 (1 − 1/433) | 0.9946 (1 − 2/372) | 0.9500 (1 − 11/220) |
| specificity_ratio (SR) | 0.15 | 1.0000 (433/(433+0)) | 1.0000 (372/(372+0)) | 1.0000 (220/(220+0)) |
| dependency_completeness (DC) | 0.15 | 1.0000 (72/72) | 1.0000 (78/78) | 0.9464 (53/56) |
| section_coverage (SC) | 0.15 | 1.0000 (16/16) | 0.8125 (13/16) | 0.7500 (12/16) |
| **quant_score** | | **0.9994** | **0.9705** | **0.9248** |

### How each metric was computed

The values come from one read-only script (`/tmp/adv305-quant/quant.py`, run with `uv run --no-project python -I`). Running it twice on the same files gives the same numbers.

- **RC.** The seed brief has no FR/NFR/R ids, so section-level topic matching was used (scoring-protocol edge case). There are 35 topic requirements, taken from the seed's dialogue items Q3-Q10, its Constraints, Success Criteria and Open Questions, and the enrichment pins. Each topic is matched by a regex over the variant text. Examples: "merge commit", "force-push", "head guard|pr_head_ok", `push_parent_ok`, the merge-parent check, L1/L2/L3, `--repo`, `.claude/`, stash, run-log, `--resume`, `uv.lock`, intent, semantic, "nothing pushed", VAL, evidence-validator, template, Wave 0, `round_counter`, re-trigger, `MERGE_HEAD`/uncommitted, create path, mergiraf/external dependency, per-invocation/global config, installed paths, `mergeable`, `tests/pr_submit`, 41, T-N50, python block, record, revert, the command doc. C misses two: the installed-primitive path constraint (no "hardcod", "installed path" or `~/.claude` mention) and the command-doc update (`pr-submit.md` is never named).
- **IC.** Scorable claims are statements that contain a concrete indicator (a number, a code span, an upper-case identifier or a file extension): A 433, B 372, C 220. Contradictions are each variant's intra-variant and variant-versus-repo rows in `diff-analysis.md`, with duplicates removed:
  - A: X-041.
  - B: X-040, plus the X-013 spot-check.
  - C: X-034, X-035, X-036, X-037, X-038 and X-039, plus spot-checks X-033, X-012, X-008, the install-list claim and X-013.
- **SR.** Statements are sentences, or one table row each, excluding headings, front matter and fenced blocks. None of the vague indicators ("appropriate", "as needed", "properly", "adequate", "should consider", "might", "various", "etc.", "best practice") occur in any variant; a grep confirms zero hits. So SR = 1.0 for all three.
- **DC.** These internal references were counted:
  - Requirement and decision ids in each variant's own namespace: A `FR-C*`, `NFR-*`, `AD-*`, `OQ-*`. B `FR-*`, `NFR-*`, `OQ-*`, `K*`, `G*`, `R*`. C `FR-*`/`FR-n.m`, `NFR-*`, `OQ-*`, `R*`.
  - "section N" and "§N" references.

  An id counts as resolved when it has a definition row or bullet. A section reference counts as resolved when a heading with that number exists. Hyphenated `R-NNN` ids were excluded because they collide with the external research namespace (R-18, R-112 and so on). References into `.md` files or SKILL.md are external and were excluded. C's 3 unresolved references are `FR-5.1` at C:55, :151 and :167: FR-5 defines no 5.1 clause.
- **SC.** H2 count outside fences. B's `## <path>` at B:370 is inside a fence and is not counted.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

CEV protocol: every MET verdict cites evidence, and a criterion without citable evidence is NOT MET. These are the final verdicts after the dual pass; the disagreements are listed in "Position-Bias Mitigation".

### Completeness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | RC 35/35; AD-1..AD-10 answer every seed open question (A:41-59) | MET | RC 35/35; §1.3 maps each seed success criterion (B:38-44) | NOT MET | RC 33/35; no installed-path constraint and no command-doc update (searched §§1-12) |
| Edge cases and failure scenarios | MET | git < 2.38 fallback R-2 (A:611); hook failure R-10 (A:619); `UNKNOWN` re-read (A:199) | MET | Appendix B exit contract; K2/K4/K10 (B:532-540) | MET | Risk register R1-R14 (C:161-174); dirty-tree halt FR-8.3 (C:173) |
| Dependencies and prerequisites | MET | §1 fact table with citations (A:22-33); §11 file inventory | MET | §2 Grounding G1-G19 (B:46-78) | MET | §5.1 "prerequisite fix ... must land BEFORE the tier machinery" (C:68-70) |
| Success / completion criteria | MET | Each FR-C has an AC that names a test (S-007, A:457-523) | MET | §1.3 "What done looks like"; FR AC column; phase gates (B:520-523) | MET | FR bullets with "Pinned:" tests (C:106-116) |
| Out of scope stated | MET | §13 (A:622-633) | MET | §11 (B:545-558) | MET | §11 (C:176-186) |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET | Cites an evidence-validator `unsupported` verdict that does not exist (A:164, :484; conceded R1-A conc. 4). Recovery text fails head binding (X-041). | NOT MET | Create-path "not yet a published PR head" premise contradicts `SKILL.md:268` (spot-check, B:622) | NOT MET | Six false claims in the spot-check table (X-033, X-034, X-012, X-008, install list, X-039) |
| Approaches feasible under the stated constraints | NOT MET | FR-C23 reuses predicate 4: a clean PR at `round_counter == max_rounds` cannot get its `uv.lock` regenerated. That fails seed success criterion 1 (R2-A N4, conceded). | NOT MET | Wave 8a is report-only after `HALT_MAX_ROUNDS` (B:261), so a mechanical conflict stays unmergeable. That fails seed success criterion 1 (B-W4, conceded R2-B A-B4). | NOT MET | Wave 0b cannot run before Wave 1 (X-034); staged-set equality cannot be satisfied (X-023); an early push with no re-trigger times out (R2-C R-C15) |
| Consistent terminology | MET | "Wave C", `C-initial`, `C-ci` used the same way throughout (A:7, :184-187) | MET | "sync" cycle, Wave 8a, `kind: "sync"` consistent (B:18-23, :96) | MET | Definitions section fixes the terms (C:16-24), and they are used as defined |
| No internal contradictions | MET | No intra-variant X row; X-041 is a variant-versus-repo row (see re-evaluation) | NOT MET | X-040: "two read-only calls" (B:219) versus a probe at both Wave 0 and Wave 8a (B:214-215) | NOT MET | X-034..X-038 |
| Claims supported by evidence | MET | §1 citations, re-read at `119622e3` (A:3, :22-33) | MET | Grounding plus empirically verified git behaviour (B:72-76) | MET | "All file:line citations were verified" (C:6); inline citations |
| **Subtotal** | **3/5** | | **2/5** | | **2/5** | |

### Structure (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Logical section ordering | MET | Summary, gap, decisions, mechanism, tiers, placement, publishing, API, FR, NFR, tests, risks (S-004) | MET | Decision record, grounding, mechanism, tiers, placement, publishing, requirements, tests, phasing, risks | MET | Purpose, definitions, mechanism, tiers, placement, publication, FR, NFR, tests, risks |
| Consistent hierarchy, no orphans | MET | H1/H2/H3 only; every H3 sits under its numbered H2 | NOT MET | Appendices A and B are H3 under "## 13. Index" (B:618, :626; S-013) | MET | H2/H3 only, numbered consistently |
| Clear separation of concerns | MET | Dedicated Core API section 7 (A:363-451) | MET | Decisions in §1, API in the §3.1 mechanism table, procedure in §6 | NOT MET | Decisions sit inline as "Seed Open Question N answered" (C:80-82); helper names are scattered across FRs and the test plan (S-005, S-008) |
| Navigation aids | MET | §15 traceability table plus 42 section cross-references | MET | §13 Index (B:579-616) | MET | 25 resolved section cross-references (DC detail) |
| Follows artifact-type conventions | MET | FR/NFR with ACs, decisions, risks, OQs | MET | Front matter, FR table with priority and AC, NFR table | MET | Requirements spec with FR/NFR/test plan/risk register |
| **Subtotal** | **5/5** | | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET | 0 vague-indicator hits (SR computation) | MET | 0 hits | MET | 0 hits |
| Concrete, not abstract | MET | Exact commands, for example `git merge-tree --write-tree -z` (A:51) | MET | `git merge --no-commit --no-ff <base_sha>` (B:21) | MET | Exact codes and paths (C:19) |
| Each section has a clear purpose | MET | §2 opens "Each decision states the choice, the alternatives rejected and why" (A:39) | MET | §1.1 "The recommendation in six lines" (B:16); §9 purpose sentence (B:516) | MET | §3 opens "Decision summary" (C:28) |
| Acronyms and terms defined on first use | NOT MET | "VAL" (A:12) and "FSM" (A:16) are never expanded | NOT MET | "FSM" (B:18) and "VAL" (B:41) are never expanded | NOT MET | Domain terms are defined (C:16-24), but "VAL" (C:112) and "FSM" are not |
| Actionable next steps / decision points | MET | OQ table with recommendations (A:637-645) | MET | OQ table with recommendation and impact (B:562-577); §8.6 run order | MET | OQs with adopted answers (C:190-194); PR checklist step (C:161) |
| **Subtotal** | **4/5** | | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| ≥3 risks with probability and impact | MET | R-1..R-11 with likelihood/impact (A:608-620) | MET | K1..K13 with likelihood/impact (B:529-543) | MET | R1..R14 with separate columns (C:159-174) |
| Mitigation per risk | MET | Mitigation column for every row | MET | Mitigation plus Residual column | MET | Mitigation names the FR or test |
| Failure modes and recovery | MET | §5.7 `--resume` (A:262-277); R-8 two-command HALT (A:617) | MET | §5.8 resume (B:289-301); §6.8 unfinished merge (B:389-392) | MET | R11 resume (C:171); FR-8.2 halt states (C:24) |
| External dependencies and their failures | MET | R-2 git version (A:611); GitHub async `UNKNOWN` (A:199) | MET | K3 `uv lock` network (B:533); K10 `gh` field set (B:540) | MET | GitHub `UNKNOWN` re-read and no-signal handling (C:18, :74) |
| Monitoring or validation mechanism | MET | Post-push `mergeable` re-read (A:352); OQ-5 data from run-log events | MET | Phase go/no-go gates (B:520-523); OQ-12 disagreement-rate measurement | MET | `== 41` sweep (C:161); every mitigation is a test |
| **Subtotal** | **5/5** | | **5/5** | | **5/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | A | Evidence | B | Evidence | C | Evidence |
|---|---|---|---|---|---|---|
| Collection boundaries (empty, single, max) | MET | `MAX_INTENT_FILES = 10`, with 11 going to Tier 3 (A:140); an empty entry list is Tier 0 (A:418); empty sources go to Tier 3 (A:139) | MET | `TIER2_MAX_FILES` 8 vs 9 boundary row (B:171, :407) | NOT MET | No Tier 2 cap (X-017); no empty or max case stated (searched §§4, 7) |
| State interactions across components | MET | `push_kind`, run-log fold, recovery key tuple (A:258-277) | MET | `kind: "sync"`, fold and recovery override (B:96, :289-301) | MET | `push_kind` filter in `rebuild_state`, recovery (C:81, :84) |
| Guard-condition gaps | MET | Preflight for foreign operation, dirty tree, detached HEAD (A:285-290) | MET | `foreign_op`, `index_clean`, `finish-merge.sh` `MERGE_HEAD == base_sha` (B:240, :352) | MET | Dirty-tree and foreign-operation halts (C:85) |
| Count divergence (off-by-one, ranges) | MET | 10 vs 11 boundary test (A:556); `UNKNOWN` re-read at most 3 times (A:199) | MET | 8 vs 9 boundary (B:407); 41 to 43 pin edits (B:466-467) | MET | `== 41` pin sweep across tests (C:161); `merge_push_count <= 1`, with the second conflict halting (C:112) |
| Interaction effects | MET | AD-8: a fix cycle and a conflict cycle never share a commit (A:55); R-3 base moves (A:612) | MET | "They never share a push" (B:22); K7 (B:537) | MET | Re-check point B targets the base moving between VAL and push (C:76) |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Qualitative Summary

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 4/5 |
| Correctness | 3/5 | 2/5 | 2/5 |
| Structure | 5/5 | 4/5 | 4/5 |
| Clarity | 4/5 | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 | 5/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 | 4/5 |
| **qual_score** | **27/30 = 0.9000** | **25/30 = 0.8333** | **23/30 = 0.7667** |

### Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (≥ 1/5) | Eligible as base |
|---|---|---|---|
| A | 5/5 | Pass | Yes |
| B | 5/5 | Pass | Yes |
| C | 4/5 | Pass | Yes |

The floor is not suspended: not all variants scored 0/5.

## Position-Bias Mitigation

Pass 1 evaluated in input order A, B, C. Pass 2 evaluated in reverse order C, B, A. **Disclosure:** both passes were run by the orchestrator in one context; no independent agents were spawned (orchestrator brief: "do not spawn agents"). Order-bias mitigation is therefore weaker than with independent passes. Every disagreement was re-evaluated against both passes' evidence, and the re-evaluation is final.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation note |
|---|---|---|---|---|---|---|
| Correctness-2 (feasible) | A | MET | NOT MET | DISAGREE | NOT MET | Pass 1 judged buildability. Pass 2 judged the seed's success criterion 1. N4 shows A fails that criterion on a spent budget; the criterion says "with stated constraints", so NOT MET. |
| Correctness-2 (feasible) | B | MET | NOT MET | DISAGREE | NOT MET | Same standard applied to B: B:261 report-only leaves a mechanical conflict unresolved after `HALT_MAX_ROUNDS`. |
| Correctness-4 (no internal contradiction) | A | MET | NOT MET | DISAGREE | MET | Pass 2 counted X-041 through the IC metric. `diff-analysis.md` classifies X-041 as "Variant A vs head binding", a repo contradiction already charged under Correctness-1, so it is not intra-variant. |
| Structure-3 (separation of concerns) | C | MET | NOT MET | DISAGREE | NOT MET | 12 single-topic H2s (pass 1), but decisions are embedded in §5.3 bullets and helper APIs are scattered (S-005, S-008). |
| Clarity-4 (terms on first use) | C | MET | NOT MET | DISAGREE | NOT MET | The Definitions section covers domain terms, but the acronyms VAL and FSM are never expanded. The criterion names both. |
| Risk-4 (external dependencies) | C | MET | NOT MET | DISAGREE | MET | C's register is all internal pins (pass 2), but GitHub's asynchronous `UNKNOWN` is an external-dependency failure with a defined response (C:18, :74). |

Disagreements re-evaluated: 6 of 90 criterion-variant pairs. Final verdicts changed from Pass 1: 4. Changed from Pass 2: 2.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate points won (Level 1 tiebreaker) |
|---|---|---|---|---|
| A (opus:architect) | 0.4997 | 0.4500 | **0.9497** | 35.0 |
| B (sonnet:refactorer) | 0.4853 | 0.4167 | **0.9019** | 42.5 |
| C (haiku:qa) | 0.4624 | 0.3833 | **0.8457** | 6.5 |

Final scores are computed from unrounded parts. B = 0.485250 + 0.416667 = 0.901917, so the rounded columns can differ by 0.0001.

**Margin:** A − B = 0.0478 (4.78 percentage points). This is below the 5% threshold (`|score_A − score_B| < 0.05`).

**Tiebreaker applied: Yes, Level 1 (debate performance).**

- **Counting rule:** points come from the Step 2 scoring matrix. A sole winner gets 1 point. Each named variant in a shared or hybrid winner ("A/B", "A (B equal)", "Split", "B (+C)") gets 0.5. "Tie (all)" rows and unresolved rows award nothing.
- **Points awarded:** 84 in total (90 agreed points minus 6 Tie-all rows).
- **Per category (A / B / C):**
  - S: 4 / 4 / 2
  - C: 14 / 18 / 2
  - X: 15.5 / 19.5 / 2
  - A: 1.5 / 1 / 0.5
  - Total: 35.0 / 42.5 / 6.5
- **Level 1 result:** B leads A by 7.5 points, or 17.6% of B's count. That is outside 5%, so Level 1 decides and Level 2 is not reached. For reference, Level 2 correctness counts would be A 3, B 2.
- **Sensitivity:**
  - The margin stays 0.0478 whether Correctness-2 is MET or NOT MET for both A and B, because the same standard moves both.
  - A could avoid the tiebreaker only with qual ≥ 29/30. A's two Correctness-1 and Clarity-4 misses rest on conceded facts.
  - B could fall out of the tiebreaker only at qual ≤ 24/30. No B verdict was borderline under the evidence above.

## Selected Base: Variant B (sonnet:refactorer)

### Selection Rationale

- A has the highest combined score (0.9497), but its lead over B (0.9019) is inside the 5% tiebreaker band.
- Level 1 of the tiebreaker goes to B by a clear margin: 42.5 to 35.0 debate points won.
- This matches where the debate ended. All three advocates accepted the tier split as amended by B's M1-M6:
  - P1 is Tier 1 only, in B's late, no-round, no-re-trigger shape, with no FSM edge.
  - One sibling push gate serves both tiers.
  - B's tier table, `finish-merge.sh` subset gate, phasing, `sync_push_count` and push-inclusive recovery text are kept.
  - Tier 2 uses A's early path and lands in P2.
- The invariant-resolution round was framed around B's P1 (INV-033 is "P1's gate", and INV-034 is the post-sync CI re-poll).
- B is eligible on the edge-case floor (5/5).
- C is not selectable: it is lowest on all three measures and carries seven High-class architecture defects conceded in Round 2.

### Strengths to Preserve from Base (B)

1. Four-phase delivery P0-P3 with go/no-go gates and a runtime dial (B §9, B:514-525; U-008, unanimous).
2. The 13-rule, first-match, fail-closed tier table: Tier 1 is `uv.lock` with stage set `123` only; no tree conflict is Tier 1; `halt:lockfile_no_recipe`; `halt:unknown_shape` (B §4.2, B:145-181; C-009, C-011, X-015, X-029).
3. Sibling rules only: `merge_parent_ok` with strict order, the disjointness property test (B §6.2, B:311-325; U-011), and `evaluate_sync_decision` (B §6.3; C-021/X-010, M5).
4. `finish-merge.sh` commit gate: `MERGE_HEAD == base_sha`, no unmerged paths, no introduced markers, staged ⊆ base-changed ∪ resolved, hooks on (B:352; U-010, X-023).
5. High-suspicion checklist escalating to Tier 3 (B §4.4; U-009).
6. Tier 1 path follows the CI-push precedent: no round, no re-trigger, no FSM edge, `sync_push_count` (B §5.6; C-018/C-019 for Tier 1, M6, X-005).
7. L1 reports and continues to review; L2 stops with the merge uncommitted (B §5.4; C-015, C-016 timing).
8. Push-inclusive operator recovery text "commit and push, or abort" (B:351; X-041).
9. Grounding G1-G19 with empirically verified git behaviour (B §2) and real-repo script tests under a local bare origin (B:460; U-013).
10. Byte-identical fragment regression test (B §8.4; U-014, without the line-count pin).

### Strengths to Incorporate from Non-Base Variants

From A:

1. GitHub mergeability first; local probe only on `CONFLICTING` or persistent `UNKNOWN`, with 3 re-reads 10 s apart (A:198-203, FR-C1 A:457; C-007, X-026, X-027, C-039).
2. `MechanicalRule` data shape plus the allowed-tools test, generalized to every new inline command (A §7.1, A:391-407; U-001, U-002, A-004).
3. One pure router `conflict_action` with an exhaustive reachable-row table test (A:419, FR-C6 A:473; S-008, NE6, QA-4).
4. `parse_stage_records` tested against a captured `merge-tree -z` fixture (A:557; U-005, C-008, C-036).
5. Two refs split by tier, with a static test that the Tier 2 ref is loaded only on Tier 2 (A:72-73, NFR-1; U-003, C-003).
6. `pr_conflicting` CI-wait skip when no merge was pushed (A:220, FR-C23; U-004).
7. Removing the create-path rebase at L1+ only, as a separate precursor change (A AD-7, A:53; C-033, X-013).
8. The Tier 2 early path at `C-initial`: the `(S2_CLASSIFY, "conflicting")` edge (P2), S5a re-trigger and a round tick (A §5.4-5.5; Split on C-014/C-017..C-020).
9. Dedicated Core API section and AD-style decision record (A §2, §7; S-005, S-008).
10. Clean-tracked-tree preflight (A:288; INV-008, C-026, X-024).
11. Pure resume function (A U-006; round-inv A INV-001).
12. Additive `push_kind`/`base_sha` keyword arguments on `build_push_triad` in place of `build_sync_triad` (A:594; R1-B conc. 4).

From C:

13. Risk register with separate Likelihood and Impact columns, keeping R14 "Certain, partially" (C §10; S-014, QA-10).
14. "Deliberately no test" boundary, rewritten (C §9.3; U-021).
15. `== 41` sweep plus the `models.py:23` docstring edit (C:161; U-024, QA-6).
16. Explicit `BLOCKED` Tier 0 row (C:55; U-023).
17. Per-tier call-count ceilings (C NFR-8, C:127; QA-9).
18. `push_kind` on all three triad records, defaulting to `fix` (C:83; C-030), plus one merge-push count field (QA-2).
19. QA-1..QA-10 acceptance tests (R2-C §3).
20. Definitions section (C §2; U-020).
