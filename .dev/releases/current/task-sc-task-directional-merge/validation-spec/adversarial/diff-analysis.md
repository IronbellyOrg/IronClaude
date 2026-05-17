# Diff Analysis — Validation Spec Comparison

## Metadata

- Generated: 2026-05-15
- Variants compared: 3 (variant-1, variant-2, variant-3 — blind attribution)
- Source under validation: `.dev/releases/current/task-sc-task-directional-merge/artifacts/final-merge-plan.md`
- Total differences found: 49 (structural: 6, content: 15, contradictions: 6, unique: 18, shared assumptions: 4)
- Focus areas: tradeoffs, invariants, failure-modes, evidence

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Top-level section count | 7 sections (defense / TUs / MEs / sequencing / closures / concessions / ACs) | 12 sections (indictment / CR-FM / CR-TASK / CR-DEP / CR-DIST-REF-DOC / INV table / scenarios / ACs / tradeoffs / FMs / evidence audit / verdict) | 11 sections (threat model / in-flight enum / S-1 / S-2 / S-3 / residual probe / resumability / scenarios / invariant corrections / mitigations / verdict) | Medium |
| S-002 | Organizing axis | TU/ME identifiers from the source plan | CR-ID class groupings (CR-FM-*, CR-TASK-*, CR-DEP-*, CR-DIST-*) | Sequencing-constraint identifiers (S-1, S-2, S-3) + threat classes | Medium |
| S-003 | Acceptance-criteria block | 12 ACs (AC-SM-01..12) — positive validation tests | 15 ACs (AC-ATK-01..15) — gap-closing tests | Mitigation table (6 rows) — recommended row additions | Medium |
| S-004 | Concrete attack scenarios | None (defense stance) | 7 scenarios (A..G) with state traces | 4 scenarios (H-1..H-4) with timelines | High |
| S-005 | Frontmatter `stance` field | `steelman` | `adversarial-attack` | `security-probe` | Low (cosmetic) |
| S-006 | Closing verdict shape | "Steelman is validated if AC-SM-01..12 all pass" | "ZERO OPEN FINDINGS is a definitional verdict, not operational" | "MITIGATED holds at the level the plan defines mitigation; 6 timeline-layer hazards survive" | Medium |

## Content Differences

| # | Topic | Variant 1 Approach | Variant 2 Approach | Variant 3 Approach | Severity |
|---|---|---|---|---|---|
| C-001 | F-02 ordering enforcement | Two-layer enforcement (grep + sentinel comment) is "structurally enforceable, not merely conventional" | Alternation-order grep is `grep -n -E` over union — matches occurrence-order, not call-site-order; produces both false positives and false negatives | Recommends extending CR-FM-04 to also anchor-line-pin `SKILL.md:191-198` (mid-phase spawn block) | High |
| C-002 | F-03 git_status failure modes | Reading A (warn-and-continue) is "the only INV-01-preserving choice" | Closure only addresses `dirty`; tool-not-installed, not-a-repo, hang remain unspecified; 5-row matrix needed | Not directly addressed | High |
| C-003 | F-04 baseline trinary | Over-escalate is "INV-03-spirit-preserving" — under-routing is the failure mode, over-routing is not | `absent\|empty\|malformed` collapses 4 distinct on-disk states; "empty" is ambiguous (file-size-0 vs parsed-empty); observer-dependent | Not directly addressed | High |
| C-004 | F-05 mid-phase rf-qa invocation | Authorized widening; ME-2 preserved; three-prong defense documented | Establishes paragraph-level precedent that is procedurally lower-cost than ME authorship; obligation #7 does not retroactively bind | Surfaces a secondary concern: line-range anchor (`SKILL.md:191-198`) is brittle to file edits | High |
| C-005 | S-1 PRD precondition | Necessary; option (a) is cheapest; (b) and (c) remain as fallbacks | No time-bounded abort; "infeasible" undefined; could indefinitely defer the merge sequence | Concrete probe: 30-day stall scenario; recommend `--max-wait` 14 days + auto-invoke option (b) + pinned git-SHA at every `[CODE-VERIFIED]` tag | High |
| C-006 | S-2 atomic-commit enforcement | Pre-commit pytest gate "is the auditable check" | Not directly attacked | Pre-commit gate is NOT a structural barrier; `git rebase -i` permits commit-split; recommend server-side pre-push hook re-grepping landing commit | High |
| C-007 | S-3 sync-rule binding | Defends as the only correct mitigation against R-RULE-10 drift | Not directly attacked | Worktree race during prune is unenumerated; recommend `flock` on `.claude/skills/` + post-prune dir-diff | Medium |
| C-008 | 79 → 65 row-instance condensation | Not addressed | Bucket-condensation table absent from plan; defeats AC #1 traceability | Not addressed | High |
| C-009 | 67-row vs 65-CR-ID count | Not addressed | Two duplicate CR-IDs unnamed in PASS roll-up (line 36) | Not addressed | Medium |
| C-010 | CR-TASK-12 seven-diff post-CR-DEP-03 | Not addressed | Fragility identified; donor file deleted by Step 6 makes audit non-rerunnable | Concurs (single-use, snapshot-frozen) | High |
| C-011 | INV-04 resumability depth | "SURVIVES" — compat shim + on-disk baseline + on-disk incident | CR-FM-03 shim has no sunset binding; future commit dropping default bricks all v3.75-era tasks | Survives at schema layer, NOT at semantic layer; 96 in-flight files reference deprecated surfaces; CR-FM-03 detects none | High |
| C-012 | F-07 procedural authorization | "Correct procedural posture"; absorption traceability obviates need for ME amendment | "Paper trail with no signatory"; no verifier role bound; CR-DEP-03 irreversibility compounds the cost | Not directly addressed | High |
| C-013 | In-flight task content audit | Not addressed | Not addressed | Live grep: 96 task files reference `/sc:task`, `sc-task-protocol`, or `task-unified`; TASK-PRD-20260514-121039 alone emits 149+ refs in its subtree | High |
| C-014 | md5sum collision susceptibility | Not addressed | CR-TASK-11 / CR-DEP-02 use md5; replace with sha256 | Not addressed | Low (adversarial only) |
| C-015 | Sentinel-comment type confusion | Treated as binding | SKILL.md is markdown; comments are documentation, not executable; type confusion | Not addressed | Medium |

## Contradictions

| # | Point of conflict | Variant 1 position | Variant 2 position | Variant 3 position | Impact |
|---|---|---|---|---|---|
| X-001 | F-02 grep enforcement quality | "Structurally enforceable, not merely conventional" (V1 § 4) | "Occurrence-order, not positional-order; produces false positives AND false negatives" (V2 § 2.4) — falsifiable defect | (silent) | High |
| X-002 | Pre-loop HALT consistency | F-03 Reading A is correct because new HALT semantics are forbidden (V1 § 5) | CR-TASK-02 task-level malform IS a HALT at pre-loop entry (V2 § 3.2); inconsistent with F-03 | (silent) | High |
| X-003 | F-05 precedent risk | "Authorized, not violation"; future widenings re-authorized by obligation #7 (V1 § 5) | "Paragraph-level surface-widening precedent procedurally lower-cost than ME authorship"; obligation #7 does not bind the F-05 author's own pattern (V2 § 3.7) | (silent) | High |
| X-004 | F-07 chain trust basis | "Correct procedural posture"; absorption traceability holds (V1 § 5) | "Paper trail with no signatory" — no verifier role bound at Step 6 (V2 § 4.1) | (silent) | Medium |
| X-005 | INV-04 survival breadth | "SURVIVES" — CR-FM-03 shim + on-disk artifacts (V1 § 3, citing source line 86) | CR-FM-03 shim has no sunset binding (V2 § 2.3) | Survives at schema layer only; 96-file semantic exposure unhandled (V3 § 7, § 11) | High |
| X-006 | "ZERO OPEN FINDINGS" verdict | Ratifies (V1 § 1, § 7) | Indicts (V2 § 1, § 12) — twenty-three falsifiable attacks | Partial-affirms ("at the level the plan defines mitigation") + identifies 6 new timeline-layer hazards (V3 § 11) | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | V1 | Per-TU steelman with explicit "invariants protected" mapping and "alternative that would weaken INV" — generative defense framework | High |
| U-002 | V1 | Individual ME-1, ME-2, ME-3, ME-6, ME-9 load-bearing analysis with "what breaks without it" | High |
| U-003 | V1 | Five honest concessions (lines 178–187) marking entry points for follow-up attack | High |
| U-004 | V1 | AC-SM-01..12 positive validation tests — auditable claims with named validation methods | High |
| U-005 | V2 | F-02 grep alternation-order attack with falsifiable counter-example (scenario A) | High |
| U-006 | V2 | 79 → 65 bucket-condensation reconciliation arithmetic and missing-table identification | High |
| U-007 | V2 | 67-row vs 65-CR-ID duplicate-rows-unnamed gap | Medium |
| U-008 | V2 | md5sum → sha256sum collision-susceptibility mitigation | Low (adversarial only) |
| U-009 | V2 | Sentinel-comment type-confusion (markdown comments are not load-bearing to any interpreter) | Medium |
| U-010 | V2 | Eight unnamed tradeoffs per closure (§ 9) | High |
| U-011 | V2 | Eight failure modes (filesystem symlink, pytest flakes, concurrent edits, CI/local divergence, mkdocs version, deferred regen, encoding, file rename) | High |
| U-012 | V2 | Evidence-completeness audit (EC-01..04) over the plan's own § 9 validation hooks | Medium |
| U-013 | V3 | Live grep evidence — 96 in-flight task files reference deprecated surfaces (substantial empirical grounding) | High |
| U-014 | V3 | TASK-PRD-20260514-121039 subtree enumeration: 149+ `/sc:task` references across the named S-1 PRD's research artifacts | High |
| U-015 | V3 | S-2 rebase-split bypass scenario (H-2) + server-side pre-push hook mitigation | High |
| U-016 | V3 | Worktree race during sync-dev prune (H-3) + `flock` mitigation | Medium |
| U-017 | V3 | CR-DEP-06 proposal — post-Step-6 one-shot residual-reference manifest | High |
| U-018 | V3 | CR-FM-03 content-level extension — INV-04 semantic resumability vs parse resumability distinction | High |

## Shared Assumptions

| # | Assumption | Source agreement | Classification | Promoted |
|---|---|---|---|---|
| A-001 | INV-01..INV-05 are the complete and correct invariant set; no sixth invariant has been overlooked | All three variants accept the source plan's invariant enumeration unchanged | STATED (source plan §0) | No |
| A-002 | The anchor source `extension-point-contracts.md:11-17` is byte-stable; line-pinned references do not silently drift | All three variants cite line-pinned anchors without questioning their stability | UNSTATED — V2 surfaces it tangentially (F-06 tradeoff, § 9), but no variant probes the anchor file's edit-resilience | **Yes — [SHARED-ASSUMPTION]** |
| A-003 | `rejected-features-ledger.md` is complete and authoritative; no rejected entry was wrongly rejected and no missing entry was overlooked | All three variants accept the ledger as the R-RULE-11 boundary without auditing the ledger itself | UNSTATED | **Yes — [SHARED-ASSUMPTION]** |
| A-004 | The merge-sprint executor is a single accountable role with continuous context — not a hand-off chain that loses state between rows | V1 implicit in "binding execution plan"; V2 implicit in AC-ATK-* expectations; V3 implicit in `--max-wait` recommendation | UNSTATED | **Yes — [SHARED-ASSUMPTION]** |
| A-005 | The Phase 7 source artifacts (`plan-adversarial-review.md`, `compat-hazard-report.md`, `invariant-survival-walkthrough.md`, `traceability-gap-report.md`) accurately summarize the actual Phase 7 work | All three variants cite these artifacts without re-verifying their content | UNSTATED — V2 § 11 raises evidence-completeness gaps but does not re-verify the artifact contents | **Yes — [SHARED-ASSUMPTION]** |

## Summary

- Total structural differences: 6
- Total content differences: 15
- Total contradictions: 6
- Total unique contributions: 18
- Total shared assumptions surfaced: 4 promoted (UNSTATED: 4, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: S-004, C-001, C-002, C-003, C-004, C-005, C-006, C-008, C-010, C-011, C-012, C-013, X-001, X-002, X-003, X-005, X-006, U-001..U-007, U-010..U-018

**Variant similarity check.** Total differences (49) ÷ total comparable items (3 variants × ~250 lines avg = 750) = 6.5% — above the 10% trivial-similarity threshold inversion; debate is warranted.

**Convergence implication.** The three variants are highly complementary: V1 frames the *defense* (what the plan gets right), V2 frames the *attack* (what the plan misses), V3 frames the *probe* (what hazards live at the timeline/tooling layer the plan does not reach). Six direct contradictions exist (X-001..X-006), all of which are decidable by examining the source plan's actual text — these will resolve in debate without irreducible disagreement.
