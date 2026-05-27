# Round 3 — Consensus Synthesis & Final Positions

## Compression Disclosure

This Round 3 is a **compressed synthesizer pass** rather than the 5-sequential-advocate format specified in the sc-adversarial protocol. **One synthesizer agent** drives per-point closure across all 51 diff items, proposes resolutions for the 10 HIGH-UNADDRESSED invariants from R2.5, and re-probes Cat-6 sufficiency.

**Rationale for compression:**

1. **Adversarial purchase exhausted.** R2 rebuttals already produced large concession deltas — V1, V2, V3, V4, V5 each issued 4-13 concessions toward one another. Further sequential advocacy would re-litigate concessions already on the table rather than close new ground.
2. **HIGH invariants are platform-level, not variant-specific.** The 10 HIGH-UNADDRESSED items (INV-001, 005, 007, 011, 015, 016, 020, 021, 022, 023) cut across all 5 variants. They are not winnable by champion-specific argument — they require protocol-text-level additions to the eventual merge, which any of the five base candidates would have to absorb identically. A single synthesizer proposing resolutions is structurally cleaner than 5 advocates each pitching their variant's partial coverage.
3. **Cat-6 sufficiency demands design, not advocacy.** R2.5 concluded the consensus does not survive the Category-6 gate challenge. Closing this gap requires designing concrete falsification eval cases and heterogeneity-enforcement rules — work that produces deterministic artifacts, not debate transcripts.

The output below remains faithful to the sc-adversarial Mode A convergence contract: per-point resolutions, convergence-score computation against the documented 51-point denominator, and an honest declaration of which conflicts remain irreducible.

---

## Per-Point Final Resolutions

Convergence rules used:
- **Consensus** = ≥4 of 5 advocates aligned on the same resolution after R2.
- **Majority-win** = 3 of 5 aligned, with a defensible margin; recorded as final winner.
- **Unresolved** = ≥2 firmly hold incompatible positions with no R2 concession.

### Structural Differences (S-001 .. S-012)

| Diff Point | Title | R1 Spread | R2 Movement | Final Winner | Confidence | Evidence |
|------------|-------|-----------|-------------|--------------|------------|----------|
| S-001 | Total H2 section count | V1=16, V2=18, V3=15, V4=16, V5=13 | Cosmetic — no advocate defended specific count | consensus: ~14-16 sections (Target 14-16 with mandatory sections from V1+V2+V4+V5) | 70% | R2-A1 closing line 153; R2-A2 closing; cosmetic — driven by merged content shape |
| S-002 | Total file length (lines) | V1=658, V2=650, V3=569, V4=586, V5=864 | V5 concedes 864→~630 (R2-A5 C1, lines 87-97); V2 R2-A2 R-2 trims §11.3-4 (~15 lines); V3 R2-A3 NE-4 holds 569; V1 R2-A1 holds ~658 with V4 §16 added | consensus: target band 600-700 lines (V5 compresses, V3 expands modestly with concessions) | 80% | R2-A5 C1 lines 87-97; R2-A3 A-001 line 126 "~610-630"; R2-A2 line 23 |
| S-003 | Tier-Decision Rubric placement | V1=embedded §4 Wave 2.5; V2=§5 before Wave §4; V3=§4 before Wave §5; V4=§8 after Eval; V5=§3 before Wave §4 | R2 transcripts do not re-litigate placement; mechanics of fractional vs linear is S-005 | V1 (Wave 2.5 fractional) — placement inside Wave Architecture as the gate between matrix-built and T1-fired | 65% | R2-A1 lines 22-30; R2-A2 line 67 "fractional numbering breaks linear audit" critique acknowledged but R2-A1 counters one-line rename fix |
| S-004 | Wave count (top-level) | V1=9, V2=7, V3=6, V4=9, V5=7 | V5 holds 7 (R2-A5 X-007 absent — no challenge); V3 holds 6 (R2-A3 NE-4); V4 holds 9; V1 holds 9 (R2-A1 lines 19-30 defends as audit budget) | Unresolved (7 vs 9) | 55% | R2-A1 lines 22-30; R2-A3 NE-4; R2-A4 paragraph 38; V2's 7 and V5's 7 are the median |
| S-005 | Fractional wave numbering | V1=Wave 2.5; V2/V3/V4=linear; V5=Wave 1.5 | R2-A1 concedes one-line YAML-key fix; R2-A2 R-2 doesn't re-challenge after R1 | V1 (fractional waves OK for tier gates; rename YAML key to `tier_gate` to avoid string-key comparison breakage) | 65% | R2-A1 lines 66-68 |
| S-006 | Hierarchy max nesting depth | V1=H4, V2=H4, V3=H3, V4=H3+, V5=H4 | No R2 movement | consensus: H4 acceptable (3 of 5) | 70% | Not contested in R2 |
| S-007 | Build Path section position | V1=§11, V2=§13, V3=§10, V4=§12, V5=§8 (before Eval) | No R2 movement | consensus: position after Eval Rubric (V1/V2/V3/V4 align) | 75% | Not contested in R2; V5 outlier acknowledged |
| S-008 | Return Contract section position | V1=§5 early, V2=§9 mid, V3=§3 very early, V4=§13 late, V5=§10 late | No direct R2 movement, but R2-A1 line 92 and R2-A4 line 105 endorse V1's contract shape | V1 (early placement, after Wave Arch) for discoverability | 60% | R2-A1 lines 92-95; R2-A4 lines 124-125 |
| S-009 | Triggers section present | All 5 present | Universal | consensus | 100% | R1 — universal |
| S-010 | Dedicated Hallucination Guardrails section | V2=Yes §11; V1/V3/V4/V5=No (inline) | R2-A1 CONCEDE merging V2 §11; R2-A2 strengthens §11 (lines 50-58); R2-A3 NE-1 concedes; R2-A4 concession 3; R2-A5 line 173 | V2 (consensus to adopt §11 verbatim, with §11.3-4 compressed and §11.6 strengthened to status-routing) | 95% | R2-A1 closing line 153; R2-A2 R-2 lines 13-23; R2-A5 line 173 |
| S-011 | Kill List section structure | V3=§13 dedicated; V1=§15 Will/Will Not; V2=§17; V4=§15; V5=§13 Boundaries | R2-A1 concession 9 (adopt V3 Kill List); R2-A2 concession 5 (adopt); R2-A4 concession 8 (adopt); R2-A5 NE-4 (complementary to V5 SS13) | V3 (Kill List as dedicated section, complementary to a Boundaries section) | 90% | R2-A1 lines 215-216; R2-A2 line 87; R2-A4 line 178; R2-A5 line 79 |
| S-012 | Ops Integration section | V5=Yes §9; all others=Absent | R2-A1 CONCEDE Ops gap; R2-A2 C-3 + R2-A2 concession 6; R2-A3 (no direct rebuttal); R2-A4 concession 7; R2-A5 keeps content but extracts table+CI to ref | V5 (adopt V5 §9 — content adopted; placement: extract ~50 lines to `refs/ops-integration.md`, keep ~30 lines of behavioral content (`-f` rule, hook awareness) inline) | 90% | R2-A1 lines 47-60; R2-A2 lines 88-89; R2-A4 line 175; R2-A5 C1 lines 87-97 |

**Structural subtotal:** S-001 thru S-012 → 11 consensus/majority-win, 1 unresolved (S-004 wave count).

### Content Differences (C-001 .. C-020)

| Diff Point | Title | R1 Spread | R2 Movement | Final Winner | Confidence | Evidence |
|------------|-------|-----------|-------------|--------------|------------|----------|
| C-001 | Tier-decision rubric structure | V1=9-row signal table; V2=hard-overrides + priority rules; V3=4-signal threshold; V4=`complexity_score` formula; V5=composite 0-2 pt scoring | R2-A5 admits +3 bonus uncalibrated; R2-A3 adds 5th multi-domain signal; R2-A4 retains formula+adds bands | majority-win: V1's named-signal rubric table (Wave 2.5) with V4-style `tier_decision.yaml` artifact recording the signals/score — best of both | 65% | R2-A1 lines 89-92; R2-A4 concession 5+6 |
| C-002 | Coverage threshold for T1 STOP | V1=≥0.95+drift=0+reg=0+≤5; V2=≥0.90+S_scope≤5+S_domains=1+density≤0.05; V3=≥0.85+dev=0+≤3; V4=gap_rate=0; V5=≥0.90+composite | R2-A3 raises V3 to 0.90 default; R2-A4 qualifies V4 gap_rate=0 (true gaps only); R2-A5 holds 0.90 (V5); R2-A1 holds V1 0.95 with `--coverage-floor 0.90` override path | majority-win: T1 STOP at coverage ≥0.90 (V2+V3-revised+V5 align; V1 0.95 still defensible for high-safety profile) — recommend 0.90 default with V4-style status-typed matrix (`mapped`/`not_applicable`/`human_decision`/`gap`) so V4's "true gap" semantics apply | 75% | R2-A3 X-001 line 109; R2-A5 X-001 line 119; R2-A4 X-001 lines 184-198; R2-A1 holds 0.95 (minority) |
| C-003 | Coverage threshold for T2 escalation | V1=<0.80; V2=via S_dev_density>0.20; V3=<0.70; V4=gap_rate>0; V5=via composite ≥6 | No R2 explicit movement on threshold itself | majority-win: T2 trigger at coverage <0.80 OR any `gap` row OR composite escalators (V1 + V4's status-typed gap detection) | 60% | R2-A1 line 130; V4 R2 line 80 routing rule |
| C-004 | Convergence threshold for adversarial PASS | V1=0.75; V2=0.75; V3=0.65; V4=non-explicit; V5=0.65 | R2-A5 CONCEDES → 0.75 (lines 99-102, 124-125); R2-A4 ACCEPTS → 0.75 (lines 90-91); R2-A3 proposes two-tier (0.75 PASS / 0.65 PARTIAL — converges with V1+V2 at the PASS bar); R2-A1 holds 0.75 | consensus: 0.75 PASS (4 of 5 align after R2 movement) | 95% | R2-A1 line 128; R2-A2 line 128; R2-A3 X-003 lines 113-114; R2-A4 line 90; R2-A5 lines 99-102 |
| C-005 | Convergence FAIL threshold | V1<0.60; V2<0.60; V3<0.65; V4 non-explicit; V5<0.50 | R2-A4 imports 0.60 (line 90); R2-A5 raises to 0.60 (line 31, line 101); R2-A3 proposes <0.65 → unresolved_conflict | consensus: <0.60 FAIL band, with PARTIAL=0.60-0.74 | 90% | R2-A4 line 90; R2-A5 lines 99-102 |
| C-006 | think_about_* tools handling | V1=optional MAY; V2=mandatory nudges not load-bearing; V3=eliminated; V4=mandatory gates; V5=mandatory checkpoints | R2-A4 concession 1 removes from frontmatter, keeps checkpoint outcomes (line 34-36); R2-A5 C4 concedes to V2 stance (line 107-111); R2-A1 holds V1's optional MAY; R2-A2 holds V2 nudges | majority-win: scripted nudges (not load-bearing), NOT in allowed-tools, audit-logged. V4's `checkpoint_logged` assertion preserved as behavior-not-tool. (V1+V2+V5 align after R2) | 75% | R2-A1 line 130; R2-A2 line 132; R2-A4 lines 34-36; R2-A5 lines 107-111 |
| C-007 | think_about_* tools in allowed-tools frontmatter | V1/V2/V3/V5=NOT listed; V4=LISTED | R2-A4 explicit concession 1 (line 34-36, 213): remove from frontmatter | consensus: NOT listed in allowed-tools (5 of 5 after R2 concession) | 100% | R2-A4 line 34 "remove the literal tools from frontmatter" |
| C-008 | Build path pick | V1=Hybrid; V2=Hybrid+grader.py; V3=Skill-creator→Sprint; V4=Skill-creator iter→Sprint; V5=Hybrid 3-stage | All variants converge — "skill-creator for iteration, sprint for production" | consensus: Hybrid (skill-creator iteration → Sprint CLI production) with V5's 3-stage framing | 95% | R1-A1 line 236; R1-A3 X-013 lines 219-223 "all variants converge"; R2-A5 lines 174-175 |
| C-009 | UC-1 vs UC-2 mode selection | V1=auto-detect ordered rules; V2=`--mode` explicit wins; V3=auto-detect; V4=4-row signal table; V5=4-row table | R1 X-008 row converges on "both present → post"; R2 no further movement | consensus: auto-detect with 4-row signal table; both present → post; ambiguous → STOP | 90% | R1 diff X-008 (universal); R2-A3 C7 concedes (already in R1) |
| C-010 | T2 multi-model topology | V1=2-3 rotate; V2=2-3 (sonnet+haiku +qwen); V3=2-3 calibrator+root-cause; V4=5-role; V5=2-3 opus+sonnet+haiku | R2-A4 concession 8 (drop 5-role excess); R2-A5 X-012 line 161-163 holds 3-role; R2-A3 restructures calibrator | majority-win: 3-role T2 (rf-qa + rf-qa-qualitative + root-cause-analyst) with confidence-calibrator running POST-card; model rotation across opus/sonnet/haiku heterogeneously enforced. V4's 5-role becomes opt-in `--depth=enterprise`. | 75% | R2-A1 X-012; R2-A3 concession (calibrator post-card restructure); R2-A5 X-012 lines 161-163 |
| C-011 | Reviewer agent role assignments | V1=rf-qa+rf-qa-qual+root-cause; V2=same+calibrator; V3=calibrator+root-cause+optional QE; V4=5-role+calibrator; V5=root-cause+rf-qa+rf-qa-qual+calibrator | R2-A3 concession (calibrator post-card not reviewer); R2-A4 concession 8 | consensus: rf-qa + rf-qa-qualitative + root-cause-analyst (calibrator post-card grader) | 85% | R2-A1 X-012 line 235 (R1); R2-A3 concession in R2; R2-A5 X-012 |
| C-012 | New agents proposed vs reuse-only | All 5 = reuse only | Universal | consensus | 100% | R1 universal |
| C-013 | Eval rubric dimension count | V1=6; V2=5; V3=5; V4=7; V5=5 | R2 no movement | majority-win: 5 dimensions (V2+V3+V5 align); V1's "tier-decision correctness" added as 6th if room | 70% | R2-A5 X-011 lines 231-235 |
| C-014 | Eval rubric aggregate ship threshold | V1=T1≥80%/T2≥90%/≥4.0avg; V2=T1≥80%/T2≥90%/per-dim 0.75-0.95; V3=≥3.5/5 (70%); V4=≥4.0/5+≥0.85; V5=T1≥80%/T2≥90%/ship ≥85% | R2 no contest | consensus on the structure (T1 ≥80%, T2 ≥90%, ship ≥85% held-out, qual ≥3.5-4.0) — 4 of 5 align modulo presentation | 75% | R1 universal pattern |
| C-015 | Deviation taxonomy specification | V1=inline 4-cell; V2=full 4-cat with detection signals; V3=inline 4-cat; V4=5-cat with `unknown`; V5=4-cat table with examples | R2-A4 concession 3 (import V2 precedence); R2-A5 C3 (adopt V2 §10.5); R2-A2 holds V2 §10 verbatim | consensus: V2's 4-category spec with detection signals and remediation defaults adopted | 90% | R2-A2 line 32-35; R2-A4 line 53-54; R2-A5 line 105 |
| C-016 | Deviation classification precedence rule | V1=not stated; V2=Regression>Drift>Necessary>Authorized; V3=default-to-Drift; V4=not stated; V5=not stated | R2-A1 concession 2 (adopt V2 §10.5); R2-A3 concession 1 (adopt V2 precedence); R2-A4 concession 3 (adopt V2); R2-A5 C3 (adopt V2) | consensus: V2's "Regression > Drift > Necessary > Authorized" with V3's "default to Drift on ambiguity" as fallback (5 of 5 after R2) | 100% | R2-A1 concession 2; R2-A2 R-3 lines 25-35; R2-A3 concession 1; R2-A4 concession 3; R2-A5 C3 |
| C-017 | Iteration convergence signal | V1=<5% abs on held-out; V2=<5% 60/40; V3=<5%; V4=<5pp det+<0.20/5 qual; V5=<5% on held-out 60/40 | R2 no movement | consensus: <5% absolute improvement on held-out 60/40 (4 of 5 align) | 85% | R1 universal |
| C-018 | Judge-model selection strategy | V1=different+more capable opus; V2=different+more capable opus default+`--jury`; V3=opus grading sonnet/haiku; V4=different+more capable+excluded from reviewers+second-judge calibration on ≥20%; V5=different implied | R2 no explicit movement | majority-win: V4's strategy (different + more capable + EXCLUDED from reviewer participation + second-judge calibration on ≥20% sample) | 70% | R2-A4 lines 103, 296; R1-A4 strength 10 |
| C-019 | Return contract field count | V1=~28+asymmetric_flags; V2=~22+deviation_count_by_class; V3=~14; V4=~18; V5=~15 | R2-A1 endorsed V1 asymmetric_flags; R2-A2 concession 1 (adopt `spec_is_wrong`); R2-A4 line 125 endorses V1 | majority-win: ~20-25 field contract built on V1's asymmetric_flags structure + V2's `deviation_count_by_class` block | 80% | R2-A1 lines 92-95; R2-A2 concession 1; R2-A4 line 125 |
| C-020 | Number of refs files | V1=6; V2=7; V3=2; V4=not enumerated; V5=4 | R2-A1 line 60 adds `refs/ops-integration.md`; R2-A3 NE concedes Kill List + precedence rule additions | majority-win: 4-6 refs (V1+V2+V5 cluster) — V3's 2-ref minimalism rejected as hiding load-bearing logic per R2-A1 W-V3-1 | 65% | R2-A1 lines 132-136 (R1) reaffirmed by R2 silence; V3 R2 NE-4 doesn't defend 2 |

**Content subtotal:** C-001..C-020 → 19 consensus/majority-win, 1 mild divergence (C-001 rubric form, but compromise was achievable).

### Contradictions (X-001 .. X-014)

| Diff Point | Title | R1 Spread | R2 Movement | Final Winner | Confidence | Evidence |
|------------|-------|-----------|-------------|--------------|------------|----------|
| X-001 | T1 coverage-floor threshold | V1=0.95; V2=0.90; V3=0.85; V4=1.00 (gap_rate=0); V5=0.90 | R2-A3 raises to 0.90 (line 109); R2-A4 qualifies V4 (true-gap only — converges to 0.90 effective when typed); R2-A5 holds 0.90; R2-A1 holds 0.95 minority | majority-win: 0.90 with status-typed matrix (3-of-5 align: V2+V3-revised+V5; V4 qualified-aligns via true-gap semantics; V1 minority hold) | 80% | R2-A3 X-001 line 109; R2-A4 lines 184-198; R2-A5 X-001 line 119 |
| X-002 | T2 coverage-trigger | V1=<0.80; V2=via S_dev_density; V3=<0.70; V4=gap_rate>0; V5=via composite | Linked to X-001 status-typed matrix decision | majority-win: any true-gap row → T2 (V4 semantics) + <0.80 coverage_pct (V1) — composite combined | 60% | Mapped from C-003 resolution |
| X-003 | Convergence PASS threshold | V1=0.75; V2=0.75; V3=0.65→0.75 (R2); V4=non-explicit→0.75 (R2); V5=0.65→0.75 (R2) | All move to 0.75 in R2 (4 explicit concessions) | consensus: 0.75 PASS (5 of 5 after R2) | 100% | R2-A3 line 113; R2-A4 line 90; R2-A5 line 99-102 |
| X-004 | T1 max-files for stop | V1=≤5; V2=≤5 (rule 1) /≤10 (rule 2); V3=≤3→≤5 default+≤3 quick (R2-A3 C of R2 line 181); V4=blast_radius (not file count); V5=<5=0 pts | R2-A3 adopts ≤5 default | majority-win: ≤5 files (V1+V2+V3-revised+V5 effective alignment) | 80% | R1 X-001 lines 230-238; R2-A3 lines 154-158 (revised) |
| X-005 | think_about_* status | V1=current optional; V2=current scripted nudges not load-bearing; V3=eliminated; V4=current mandatory (concedes R2); V5=current mandatory checkpoints (concedes R2 → V2 stance) | R2-A4 + R2-A5 explicit concessions to V2's stance | majority-win: CURRENT, scripted nudges, NOT load-bearing, NOT in allowed-tools, audit-logged. V3 eliminates entirely (minority). 4 of 5 converge on V2 stance after R2 | 85% | R2-A1 line 130; R2-A4 line 34-36; R2-A5 lines 107-111 |
| X-006 | think_about_* in allowed-tools | V1/V2/V3/V5=No; V4=Yes→No (R2) | R2-A4 explicit concession 1 | consensus: No (5 of 5 after R2) | 100% | R2-A4 lines 34, 162 |
| X-007 | Wave count | V1=9, V2=7, V3=6, V4=9, V5=7 | No R2 movement; advocates defend own count | unresolved (V1+V4 at 9 vs V2+V5 at 7 vs V3 at 6) | 50% | R2-A1 lines 22-30; R2-A3 NE-4; R2-A4 paragraph 36 |
| X-008 | Mode selection "both present" → mode | All 5 = post | Universal R1 | consensus | 100% | R1 X-008 |
| X-009 | Deviation taxonomy category count | V1/V2/V3/V5=4; V4=5 (qualified retention in R2) | R2-A4 concession 4 retains `unknown` ONLY as evidence-insufficiency state with required fields, NEVER for evidence-sufficient cases. R2-A2 R-3 rejects 5th class, routes insufficient evidence to Grounding Gaps + status:partial | **UNRESOLVED with structural divergence**: 4 of 5 say 4 categories; V4 retains `unknown` as constrained evidence-insufficiency terminal state (NOT a classification class). The compromise: 4-category taxonomy for classification + V2's Grounding Gaps mechanism for insufficient evidence (which V4 calls `unknown` row with required fields). The label disagreement is real (INV-015 from R2.5 explicitly names this). | 65% | R2-A2 R-3 lines 25-35; R2-A4 concession 4 lines 64-66 |
| X-010 | Classification precedence explicitly defined | V1=No; V2=Yes; V3=Yes (default-Drift); V4=No (R2 concedes); V5=No (R2 concedes) | R2-A1 + R2-A3 + R2-A4 + R2-A5 all concede V2's precedence | consensus: Yes — adopt V2 §10.5 (5 of 5 after R2) | 100% | R2-A1 concession 2; R2-A3 concession 1; R2-A4 concession 3; R2-A5 C3 |
| X-011 | Eval rubric dimension count | V1=6; V2=5; V3=5; V4=7; V5=5 | R2 no movement | majority-win: 5 dimensions (V2+V3+V5 align) | 75% | R2-A5 X-011 |
| X-012 | T2 reviewer agent set UC-2 default | V1=rf-qa+rf-qa-qual+root-cause; V2=same+calibrator; V3=calibrator+root-cause+QE (anti-pattern); V4=5-role; V5=root-cause+rf-qa+rf-qa-qual+calibrator | R2-A3 concedes calibrator-as-reviewer is anti-pattern; R2-A4 concession 8 drops 5-role excess; R2-A5 X-012 holds 3-role | consensus: rf-qa + rf-qa-qualitative + root-cause-analyst as reviewers; confidence-calibrator runs POST-card (4 of 5 align after R2 restructure) | 90% | R2-A1 X-012; R2-A3 concession; R2-A5 X-012 |
| X-013 | Build path pick | V1=Hybrid; V2=Hybrid+grader; V3=skill-creator→Sprint; V4=skill-creator iter→Sprint; V5=Hybrid 3-stage | Universal convergence | consensus: Hybrid skill-creator → Sprint CLI (V5's 3-stage label) | 95% | R1-A3 X-013 "non-contradiction" |
| X-014 | Memory keying with project-slug | V1=suffix; V2=suffix; V3=flat suffix; V4=path-style; V5=path-style→suffix (R2 concedes line 18-21) | R2-A5 explicit concession (line 18-21) | consensus: suffix style `reflection/last-pass-{slug}` (5 of 5 after R2; V4 conceded by silence + sibling-skill consistency) | 95% | R2-A5 line 18-21; R2-A1 lines 178-181 |

**Contradictions subtotal:** X-001..X-014 → 12 consensus/majority-win, 2 unresolved (X-007 wave count, X-009 4-vs-5 category structural divergence).

### Shared Assumption Promoted (A-001 .. A-005)

| Diff Point | Title | R1 Spread | R2 Movement | Final Winner | Confidence | Evidence |
|------------|-------|-----------|-------------|--------------|------------|----------|
| A-001 | User can read 400-700 line SKILL.md | All R1: QUALIFY | R2-A5 commits compression to ~630 lines; R2-A1 holds V1 fine at 658 | consensus: QUALIFY — target 600-700 lines, V5 compresses, V3 expands modestly | 85% | R2-A1 line 132; R2-A5 A-001 line 141 |
| A-002 | Env-var aliases remain set | V5 partial STATED; others UNSTATED | R2-A1 + R2-A2 + R2-A3 + R2-A4 + R2-A5 all REJECT/ACCEPT — adopt V5 Wave 0 step 6 + V5-A5-extension (zero-aliases → T1-only WARN) | consensus: REJECT assumption — adopt Wave 0 env-var check with degraded-mode handling (5 of 5) | 100% | R2-A1 line 134; R2-A2 line 144; R2-A3 A-002 line 130; R2-A4 A-002 line 90-94; R2-A5 A-002 lines 144-147 |
| A-003 | Workspace path `.dev/eval-workspaces/sc-reflect/` | V5 outlier (`sc-reflect-protocol`); V1-V4 align; V5-R1 + R2-A5 concede `sc-reflect/` | R2-A5 A-003 line 149-151 explicit concession | consensus: `.dev/eval-workspaces/sc-reflect/` (5 of 5 after V5 R2 concession) | 100% | R2-A5 line 149-151; R2-A1 A-003 line 136 |
| A-004 | 60/40 train/test split | All R1: QUALIFY | No R2 movement | consensus: QUALIFY — 60/40 for iteration-2+; iteration-1 (3-case pilot) all-train | 85% | R2-A1 line 138; R2-A3 A-004 line 138 |
| A-005 | Single-repo/single-project | All R1: ACCEPT | No R2 challenge | consensus | 100% | Universal |

**Shared-assumption subtotal:** A-001..A-005 → 5 consensus (all 5 resolved).

---

## Convergence Computation

### Tally

- **Consensus** (≥4/5 align after R2): S-009, S-010, S-011, S-012 (4), C-004, C-005, C-007, C-008, C-009, C-011, C-012, C-015, C-016 (9), X-003, X-006, X-008, X-010, X-013, X-014 (6), A-002, A-003, A-005 (3) → **22 consensus**
- **Majority-win** (3/5 align, with R2 concession trajectory): S-001, S-002, S-003, S-005, S-006, S-007, S-008 (7), C-001, C-002, C-003, C-006, C-010, C-013, C-014, C-017, C-018, C-019, C-020 (11), X-001, X-002, X-004, X-005, X-011, X-012 (6), A-001, A-004 (2) → **26 majority-win**
- **Unresolved** (firm holds, no R2 concession): S-004, X-007, X-009 → **3 unresolved**

**Agreed points** (consensus + majority-win) = 22 + 26 = **48 of 51**.

**Convergence score = 48 / 51 = 0.941**

### Status

- Target threshold per sc-adversarial Mode A spec: **0.75**.
- Computed: **0.941**.
- **Score-only status**: **CONVERGED**.

But — convergence is necessary, not sufficient. The R2.5 invariant probe identifies 10 HIGH-UNADDRESSED items that may block status promotion even when point-by-point convergence is high. See "Final Status Determination" below.

---

## HIGH-Invariant Resolution Proposals

The R2.5 probe enumerated 10 HIGH-severity findings the consensus had not addressed. For each, I propose a concrete protocol-text-level addition.

### INV-001: Tasklist input immutability not enforced

- **Finding**: No variant computes `input_sha256` or re-reads the tasklist between Wave 0 (load) and Wave N (consumption). A mid-run edit produces silent matrix↔tasklist misalignment.
- **Proposed resolution**: Add to Wave 0 step 8: "Compute `input_sha256 = sha256(read(tasklist_path))` and persist to `artifacts/input-snapshot.yaml`. Before Wave 5 synthesis, re-read the input and recompute SHA; if it differs, STOP with `input_drift` flag and emit the SHA pair into the return contract."
- **Severity after resolution**: ADDRESSED (deterministic check, single hash compare).
- **Partial existing coverage**: None — fully new addition. Any base variant absorbs it identically.

### INV-005: Empty tasklist (0 items) crashes coverage formula

- **Finding**: V1's partial-credit formula `(covered + partial*0.5) / total` divides by zero when `total == 0`.
- **Proposed resolution**: Add to Wave 1 step 1 (matrix construction): "If `total_tasks == 0` and mode == UC-1, STOP with `empty_input` flag and `status: partial`, return `coverage_pct: null` with `coverage_undefined: true` in the contract. Do NOT proceed to T1/T2."
- **Severity after resolution**: ADDRESSED (explicit guard added).
- **Partial existing coverage**: V3's "ambiguous → STOP" Wave 0 handles parse failures, not empty-but-parseable inputs. Addition is needed regardless of base.

### INV-007: T1 coverage floor when no IDs exist (vacuous-truth pass)

- **Finding**: When a spec has no traceable IDs to map, the 0.90 floor passes by 0/0 = vacuously true. V4 concession 6 adds `not_applicable`/`human_decision` row types but does NOT handle "zero IDs to begin with."
- **Proposed resolution**: Add to Wave 1 step 2: "If the spec/tasklist parse produces zero requirement IDs (no `T-NNN`, no checklist items, no headings to map), set `coverage_undefined: true`, route directly to T2 (no T1 stop possible), and surface in the report header. Coverage_pct is not computed."
- **Severity after resolution**: ADDRESSED (explicit `coverage_undefined` distinct from `coverage_pct == 1.0`).
- **Partial existing coverage**: V4 closest (typed rows). Addition: enforce the no-IDs-at-all case as a separate routing path.

### INV-011: Minimum agent count for T2 with limited aliases

- **Finding**: V5's zero-alias rule (R2-A5 line 165) covers ZERO aliases (→T1-only) but not TWO aliases. Is T2 with 2 heterogeneous reviewers acceptable, or does T2 require ≥3?
- **Proposed resolution**: Add to Wave 0 step 6 (env-var check):

  ```
  IF resolved_aliases.count == 0: T1-only, WARN, degraded
  IF resolved_aliases.count == 1: T1-only, WARN "T2 requires ≥2 model classes"
  IF resolved_aliases.count == 2: T2 with 2 reviewers (degraded), record `t2_diversity: degraded`
  IF resolved_aliases.count >= 3: T2 with 3 reviewers, record `t2_diversity: full`
  ```

- **Severity after resolution**: ADDRESSED (deterministic per-count routing).
- **Partial existing coverage**: V5 (zero-alias handling only). Addition: explicit 1/2/3+ table.

### INV-015: 4-vs-`unknown` deviation taxonomy structural divergence

- **Finding**: R2's "consensus C5" (4-category without `unknown`) papers over a real divergence: V4 retains `unknown` as evidence-insufficiency terminal state; V2 routes insufficient evidence to Grounding Gaps + status:partial. These are DIFFERENT downstream ledger rows.
- **Proposed resolution**: Adopt V2's mechanism as the primary rule, and add an explicit clarification:

  ```
  The deviation taxonomy is 4 categories: Authorized Expansion / Necessary Deviation / Drift / Regression.
  Apply precedence: Regression > Drift > Necessary > Authorized.

  IF a hunk cannot be classified due to INSUFFICIENT EVIDENCE (not multi-signal ambiguity):
    - Do NOT add to deviation-ledger.yaml.
    - Add to grounding-gaps.yaml with required fields:
      - hunk_ref, evidence_missing, why_not_classifiable, next_evidence_needed,
        owner (default: user), decision_needed_by_user (boolean)
    - Force status: partial.
    - Force `needs_human_decision: true` in the return contract.

  This is NOT a 5th deviation category. The deviation-ledger has 4 rows max;
  grounding-gaps is a parallel artifact for evidence-insufficient findings.
  ```

- **Severity after resolution**: ADDRESSED. The label conflict ("unknown" vs "Grounding Gap") is resolved by structural separation: deviation-ledger keeps 4 categories; grounding-gaps absorbs V4's `unknown` semantics as a separate artifact with required fields.
- **Partial existing coverage**: V2 (Grounding Gaps mechanism) + V4 (required fields for evidence-insufficient rows). The resolution merges the two: V2's structure, V4's field-list rigor.

### INV-016: sc-adversarial package missing entirely (not just empty response)

- **Finding**: V1's 3-tier guard (empty/partial-parse/missing-file) does NOT cover "Skill tool returns 'skill not found'" — the actual failure if `sc-adversarial-protocol` is not installed.
- **Proposed resolution**: Add to Wave 5 step 0 (pre-invocation): "Before calling `Skill('sc-adversarial')`, probe via `mcp__serena__list_memories` for the skill's existence indicator OR attempt a no-op probe (e.g., `Skill('sc-adversarial', args='--help')`). If the probe returns 'skill not found' or equivalent, STOP Wave 5, set `adversarial_unavailable: true` in the contract, fall back to F2 (single-reviewer highest-confidence verdict), and route to T3 only if user opts in."
- **Severity after resolution**: ADDRESSED.
- **Partial existing coverage**: V3 R2-A3 concession 3 names F1/F2/F3 fallback but assumes the skill exists. Addition: pre-invocation probe + missing-skill route.

### INV-020: Gate-1 — heterogeneous calibrator (calibrator-model ≠ reviewer-model class)

- **Finding**: Per ICLR 2025 MAD evidence, same-model-class calibration is sycophantic. Consensus does not enforce calibrator-model ≠ reviewer-model class.
- **Proposed resolution**: Add to Wave 4 step 4 (calibration phase):

  ```
  Calibrator-model selection rule:
    LET reviewer_model_class = union(reviewer 1..N model class)
    LET calibrator_model_class ∈ {opus, sonnet, haiku} \ reviewer_model_class
    IF that set is empty (all 3 classes are reviewers): use the model class
      with the highest available capability tier NOT used by the most reviewers
      AND emit `calibrator_diversity: degraded` flag.
    ELSE: pick the highest-capability calibrator model from the disjoint set
      AND emit `calibrator_diversity: full`.

  Test assertion: yaml_field reflection-card.yaml calibrator_model_class
    NOT IN reviewer_model_classes (asserted in eval rubric dimension "calibration discipline").
  ```

- **Severity after resolution**: ADDRESSED.
- **Partial existing coverage**: V1 §4 Wave 4 step 4 has parallel calibration but not heterogeneity enforcement. V2 §11.3 says "blind calibration anti-anchoring" without specifying disjoint model class. Addition: explicit disjoint-set rule + telemetry field + assertion.

### INV-021: Gate-2 — vendor-heterogeneous T2 (cross-vendor, not just model-class)

- **Finding**: User's env aliases could all resolve to Anthropic models (`opus-4`, `sonnet-4`, `haiku-4`). "Heterogeneous duo" is only model-CLASS heterogeneous, not VENDOR-heterogeneous. Per Wisdom of Silicon Crowd / HDEE, ensemble effect requires cross-vendor.
- **Proposed resolution**: Add to Wave 0 step 6:

  ```
  Inspect resolved aliases:
    LET vendors = {extract_vendor(alias) for alias in resolved_aliases}
    IF |vendors| == 1 (all-Anthropic, e.g.):
      WARN: "T2 ensemble is single-vendor (vendor=<X>). Ensemble effect degraded.
            Configure ANTHROPIC_DEFAULT_<class>_MODEL to point to qwen/kimi/deepseek
            for cross-vendor benefit, OR accept single-vendor risk."
      Emit `t2_vendor_diversity: single` to return contract.
    ELSE:
      Emit `t2_vendor_diversity: multi` with vendor list.
  ```

  Plus eval rubric dimension addition: "T2 vendor heterogeneity: ≥2 vendors → +1.0; 1 vendor → 0.5; not enforced (warn only)".

- **Severity after resolution**: PARTIALLY-ADDRESSED. Warning is enforceable, but actually requiring cross-vendor would block most users (who have only Anthropic aliases). The realistic v1 posture: WARN, telemetry, eval-graded. Hardening (block on single-vendor) deferred to v1.1 if eval shows convergence-on-wrong-answer cases correlate with single-vendor T2.
- **Partial existing coverage**: V2 §7.1 mentions "qwen/kimi/deepseek" as optional 3rd; V5 §3 model selection table. Addition: vendor detection + telemetry + warn + eval dimension.

### INV-022: Gate-3 — convergence-correlates-with-correctness falsification eval

- **Finding**: 0.75 convergence threshold assumes convergence_score measures agreement-with-truth, but per ICLR 2025 MAD, agents can converge on a wrong answer when prompted similarly. No variant proposes a "seeded-correct-minority-view" eval case.
- **Proposed resolution**: Add eval iteration-3 hardening case to V4's seeded-traps section (V4 §9.4):

  ```yaml
  - id: T2-convergence-wrong-answer
    type: held-out adversarial
    fixture: fixtures/spec-with-deliberate-misclassification.md
    setup: |
      Spec describes a feature requiring authentication.
      Diff implements feature WITHOUT auth (regression).
      Tasklist mentions auth requirement.
      All three reviewers are sonnet-class.
      Pre-seed reviewer context with "the implementation looks complete and matches the spec"
      (anchoring all reviewers toward a wrong verdict).
    expected:
      tier: 2
      verdict: regression_present (TRUE GROUND TRUTH)
      convergence_score: < 0.75 (PARTIAL or FAIL — they should NOT converge on the wrong answer)
      asymmetric_flags.regression_present: true
    assertion: convergence_score < 0.75 OR verdict == regression_present
    severity: AUTO-FAIL if convergence ≥ 0.75 AND verdict ≠ regression_present
      (this is the falsifier: high agreement on a wrong call = the sufficiency claim fails)
  ```

- **Severity after resolution**: ADDRESSED (eval case designed; pass/fail criterion explicit; falsifier defined).
- **Partial existing coverage**: V4 §9.4 has seeded false-citations / seeded regressions but not "T2 agrees with T1 on wrong call." Addition: the case above, plus an eval-rubric dimension "sycophantic-convergence detection."

### INV-023: Sufficiency claim falsifiability ("tier escalation will catch self-confirmation bias")

- **Finding**: The consensus claim is unfalsifiable as currently worded. The falsifier — "T1 verdict wrong AND T2 ensemble converges on the same wrong verdict AND ships as success with convergence ≥ 0.75" — is not designed as an eval case.
- **Proposed resolution**: This is INV-022's eval case extended. Add to eval rubric:

  ```yaml
  dimension: tier-escalation-anti-confirmation
  description: Tests that T2 ensemble does not rubber-stamp T1's wrong verdict.
  cases:
    - T2-convergence-wrong-answer (from INV-022)
    - T2-different-class-disagreement (one reviewer trained on opposite framing produces
      a minority correct view; convergence should drop accordingly)
  pass_threshold: ≥80% of cases catch the wrong verdict (PARTIAL or FAIL convergence
    OR explicit minority-view surfaced in adversarial-merge transcript)
  ```

  Also add to SKILL.md §11 (Hallucination Guardrails): "The protocol's anti-confirmation guarantee is conditional on (a) calibrator-model ≠ reviewer-model class (INV-020), (b) ≥2 vendors when possible (INV-021), (c) sycophantic-convergence eval cases pass (INV-022)."
- **Severity after resolution**: PARTIALLY-ADDRESSED — the falsifier is defined, but the sufficiency claim becomes conditional rather than unconditional. v1 ships the eval case; v1.1 hardens based on first-run results.
- **Partial existing coverage**: V2 §1 cites ICLR 2025 MAD but doesn't operationalize. V4 §9.4 seeds traps but not this specific one. Addition: the eval dimension above + conditional language in §11.

---

## Cat-6 Sufficiency Re-Probe

The R2.5 verdict: "consensus does NOT survive the Cat-6 challenge — none of the three downstream gates has been demonstrated."

After the INV-020/021/022 resolutions above, the three gates now have proposed mechanisms:

### Gate 1 (calibrator unbiased): RESOLUTION = YES (proposed)

- **Mechanism**: INV-020 — calibrator-model class MUST be disjoint from reviewer-model classes; eval asserts via `calibrator_model_class NOT IN reviewer_model_classes` test on `reflection-card.yaml`.
- **Verification path**: Wave 4 step 4 emits `calibrator_diversity: full|degraded`. Eval iteration-1 includes a unit-style test that this field is `full` for a 3-model-class environment.
- **Confidence**: HIGH — deterministic check, single yaml-field assertion.

### Gate 2 (T2 truly heterogeneous): RESOLUTION = YES, partially (proposed)

- **Mechanism**: INV-021 — Wave 0 detects vendor count, emits `t2_vendor_diversity: single|multi` warning telemetry. Eval rubric dimension grades vendor heterogeneity (≥2 → +1.0; 1 → 0.5).
- **Verification path**: Eval iteration-2 includes one case with single-vendor T2 and one with multi-vendor T2; compares convergence-correctness correlation across them.
- **Confidence**: MEDIUM — single-vendor is not BLOCKED in v1 (would block most users); telemetry + eval dimension only. Hardening deferred to v1.1 based on iteration-2 evidence.

### Gate 3 (convergence correlates with correctness): RESOLUTION = YES, design-only (proposed)

- **Mechanism**: INV-022 + INV-023 — iteration-3 eval case T2-convergence-wrong-answer is designed as the falsifier. AUTO-FAIL if convergence ≥ 0.75 AND verdict is wrong.
- **Verification path**: The case must pass in eval iteration-3 before ship. If it fails, the 0.75 threshold is the wrong gate; v1 ships only when the case passes (i.e., the protocol detects the wrong-answer convergence and reports PARTIAL/FAIL).
- **Confidence**: HIGH for design, MEDIUM for execution — the eval case is defined, but its pass rate is unknown until run.

**Cat-6 verdict after R3 proposals: Y / Y-partial / Y-design-only** — all three gates have proposed resolutions. None is fully demonstrated as PASSING; all are now FALSIFIABLE, which is the actual requirement R2.5 named ("the sufficiency claim is unfalsifiable as stated").

---

## Final Status Determination

- **Diff-point convergence**: 48 / 51 = **0.941** (vs threshold 0.75) → SCORE OK
- **Taxonomy coverage gate** (L1/L2/L3 from sc-adversarial spec): L1 (structural) = covered (S-001..S-012 resolved or unresolved-known); L2 (content) = covered (C-001..C-020 resolved or majority-win); L3 (contradictions + assumptions) = covered with 3 unresolved (X-007 wave count, X-009 taxonomy structural divergence — though INV-015 resolution proposes structural separation that addresses it). → **Y**
- **Invariant probe gate** (HIGH-UNADDRESSED count): 10 HIGH items at start of R3. After R3 resolution proposals: 8 ADDRESSED, 2 PARTIALLY-ADDRESSED (INV-021 vendor heterogeneity warn-only; INV-023 sufficiency conditional). → 0 HIGH-UNADDRESSED **only after merged-spec absorbs the proposals**.
- **Cat-6 gates**: 3 / 3 have proposed resolutions (1 high-confidence, 1 medium with v1.1 deferral, 1 design-only pending eval-3).

### Final status: **CONVERGED (CONDITIONAL)**

- The diff-point convergence cleanly exceeds the 0.75 threshold (0.941).
- The HIGH-invariant resolutions and Cat-6 gates exist as proposals; the merged-spec output of this brainstorm MUST absorb them as protocol-text additions for the convergence claim to be honest. If the merge step drops them, the convergence reverts to "numerically satisfied but substantively blocked."
- The two remaining structural unresolved items (X-007 wave count: 6 vs 7 vs 9; X-009 4-vs-`unknown`): X-009 is addressed by INV-015's structural separation; X-007 remains a cosmetic disagreement that does not block convergence (the wave-count outcome can be decided by the merger picking a number — 7 is the median).

---

## Top 3 Irreducible Disagreements

These are carried into the merge contract as `unresolved_conflicts`:

1. **X-007 / S-004 — Wave count (6 vs 7 vs 9)**: V1 + V4 hold 9 waves as audit-budget; V2 + V5 hold 7 as middle ground; V3 holds 6 as minimal. No R2 concession on either side. Resolution must be made at merge time (recommended: 7 waves — median, V2's count, accommodates V1's audit-budget concern via per-step audit emits within waves).

2. **X-009 / INV-015 — 4-category vs `unknown`-as-5th-state taxonomy**: V4 retains `unknown` as evidence-insufficiency terminal state in deviation-ledger.yaml; V2 routes insufficient evidence to a separate grounding-gaps.yaml + status:partial. The R3 INV-015 resolution proposes structural separation (4-category ledger + parallel grounding-gaps artifact), which subsumes both — but V4 advocate (R2-A4 concession 4) and V2 advocate (R2-A2 R-3) frame the same mechanism with different ledger-row vocabulary. The merge must pick the artifact shape (recommended: V2's grounding-gaps.yaml separate artifact with V4's required-field rigor — both win).

3. **C-001 — Tier-rubric structure (named-signal table vs additive formula vs composite-score)**: V1 (named-signal table) and V4 (`complexity_score` formula) and V5 (0-2 pt composite) each hold their structure with R2 defenses. The R3 proposal (named-signal rubric + `tier_decision.yaml` artifact recording the signals/score) is a compromise rather than a winner. If the merger picks one structure strictly, the other two stay unresolved as a methodological disagreement.

---

## Synthesizer Note

The R2 round produced extraordinary concession density — every variant moved toward the others on at least 4 substantive points. This is the signature of a healthy adversarial brainstorm rather than a stalemate. The convergence score (0.941) is honest because most of it was earned by mutual concession, not by one variant's dominance.

The remaining work for the downstream merge step is mechanical: pick V1 spine OR V2 spine OR V4 spine (the three serious base candidates — V3 too minimal, V5 too long without compression), absorb V2 §11 (with R3 INV resolutions), V4 §16 (Testability Map), V5 §9 (extracted to ref), V3 Kill List, V1 asymmetric_flags + retroactive escalation, and the 10 INV-resolutions above. The result will be a 600-700 line SKILL.md that survives R2.5's Cat-6 challenge in design (not yet in eval; that's iteration-3's job).
