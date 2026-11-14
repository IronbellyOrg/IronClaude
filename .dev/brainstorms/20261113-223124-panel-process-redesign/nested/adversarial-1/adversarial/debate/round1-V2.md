# Round 1 statement: Variant 2 (sonnet:analyzer)

## Position

Finalize (A) a script-built Sweep Sheet and (B) a written Recipe Ledger with no pre-pass. They answer the seed's open question from opposite sides, and both fit +35% on per-package medians. Take V1's class registry, extractor blind spots and generic-checklist control, V2's sourced numbers, unchanged grading rule and decision gates, and V3's real-parser check and package-level bootstrap.

## Steelman of Variant 1

V1 is architecture first. One class card renders either as a question (A) or as a recipe (B), so a new class or target is a card plus an adapter, not a dispatcher edit. It names each extractor's blind spot. It discloses its own worst case ("kill-limited"). Its arm A4 (a generic checklist) with gate G5 tests the human-inspection finding that checklists add little. I recomputed its matrix sums (A 1.70-3.70, B 1.05-3.10) and they are correct.

## Steelman of Variant 3

V3 is the leanest build (about 240 lines). It is the only variant with a blind verifier that sees just claim, anchor and evidence, which fits the herding evidence and attacks the real risk of forced items, false positives. It also finds the fence-opener-only parse gap and resamples packages rather than runs, the honest unit of independence.

## Strengths claimed

1. Sourced harness share: V2 uses +0.14 (0.03-0.34). I checked merged-requirements.md:342-350: 0.08+0.03+0.03+0, with H4 = 0. V1 (+0.2-0.7) and V3 (+0.4-0.9) are 1.5-6x higher without derivation (X-001).
2. Rubric held constant: "The grading rule itself is unchanged" (CB-3 only limits blocking), matching merged-requirements.md:320. V1's CB2 rewrites the Medium sentence.
3. Consistent arithmetic (X-004): V3 on b = 122 gives A = 6+122+18+3 = 149 (+22%) and B = 6+132+2+25+3 = 168 (+38%, over its own 165 ceiling). On b = 100 B is 146 (+46%). V2 shows its tightest cell (128 s vs 135 s).
4. Per-item cost (X-003): V3's 40 lines at about 35 tokens is 1.4k tokens, about 29 s at V1's 48 tokens/s, and 60-80 s at V1/V2's 1.5-2 s per item, not +18 s. With 29 s, A is +31% at b = 122 and +38% at b = 100.
5. Two independent hypotheses (script vs instruction only). V3's A and B both need `panel_prepass.py`, so its experiment cannot say whether the script is necessary.
6. Validation controls: planted defects, clean twins, placebo P and Z0-raw (U-012, U-013, U-015).

## Weaknesses identified in Variants 1 and 3

1. V1: modelled worst case +36% (b = 122) and +42% (b = 100) exceeds its own D = 135 and relies on a kill that discards reports (X-005, X-008). It is the heaviest build (1,300-1,500 lines). E4 greps the "whole base checkout" while failure modes say grep is restricted. Auto-promotion writes script-authored findings.
2. V1's CB2 changes production blocking semantics. Its A1 control includes CB1-CB4, so redesign-versus-A1 stays clean (this narrows X-002), but A0-versus-A1 no longer measures harness-only gain.
3. V3: one shared list in class order (C6 first, C1 and C3 last), capped at 60. A plan with many "all/every/each/only/any" sentences fills the cap with C6 and drops C1/C3 (B1, B2, I1). Nothing ranks items.
4. V3 arithmetic: matrix rows sum 3.50-6.05, text says 3.6-6.6; "+1.2 to +2.3" has no derivation (X-006). Haiku and sonnet times reuse luna's +18 s though haiku's per-line cost is higher.
5. V3 validation: 3 packages, 8 runs, no placebo or checklist control; it cannot separate recipe from list.

## Concessions

- My 3(f) totals add H and redesign (3.2-5.7), contradicting my R-30 "never summed in a headline". The +0.14 is borrowed, not measured.
- The tightest cell has 7 s slack, the 8 s pre-pass is unmeasured, and the +22 s luna load for R-C2 is optimistic.
- My claim that a 1.35 kill discards 25-40% of reports cites no number. Check it on A0 timing data.
- About 254 panel runs is the costliest plan. V3's blind verifier is a better false-positive guard than mine but breaks +35% as specified.
- The 12-item cap with Q2/U2/M2/R2/S2 can crowd out a class on a large plan.

## Shared assumptions

- A-001: QUALIFY. My matrices fold judge credit and merge survival into one probability; the measured act-rate readout (D-table, "Act-rate readout") must replace them.
- A-002: QUALIFY. Summing is only a planning upper bound after a flat displacement; the decision rule uses measured found fraction, not sums.
- A-003: QUALIFY. H and redesign gains overlap on I4, B5 and I1 (H3 masks them), so they are bounded, not additive; Z0-raw versus Z0 measures it.
- A-004: QUALIFY. A pre-implementation sandbox and a 6-8 s search are unverified; require H3 as precondition, exclude `.dev/` from sweeps, kill at 15 s, fall back to the baseline brief.
- A-005: QUALIFY. Rubber-stamping is the main risk; the what-you-ran transcript audit, planted-item OK-rate and placebo arm test it.
- A-006: QUALIFY. A non-blocking finding counts for the study score (all 7 true I7 finds were non-blocking), but report found-and-blocking separately because the loop verdict needs blocking.
- A-007: ACCEPT. Block-randomised arms and per-panel medians make the baseline stable enough; track drift in the manifest.
- A-008: QUALIFY. Counts are phrase-search lower bounds in one repository; claim C1, C3 and narrow C7 only as the hold-out supports.
- A-009: QUALIFY. About 2 s per item holds for at most 12 written items; it fails for V3's 40-60 items, and 48 tokens/s is derived and unverified.

## Position table

| point | preferred approach for the merged spec (V1, V2, V3, COMBINE V#+V#, or NONE) | reason in at most 15 words |
|---|---|---|
| S-001 | V2 | Six sections with shared brief changes first; comparison before validation. |
| S-002 | COMBINE V1+V2 | V1's H1-H4 requirement table, V2's short shared brief changes first. |
| S-003 | NONE | All three use identical lettered (a)-(i) blocks; keep them. |
| S-004 | COMBINE V1+V2 | V1's grouped tables with Test column, trimmed to V2's tighter count. |
| S-005 | V2 | Per-issue main and secondary cause map drives the coverage matrices. |
| C-001 | COMBINE V1+V2 | V1's typed extractors with blind spots; V2's 12-item cap and shuffle; no 60-item list. |
| C-002 | COMBINE V2+V1 | V2's lenses of at most 4 recipes; V1's guarded idle-time second session. |
| C-003 | COMBINE V1+V2 | V1's route and replicas as data; V2's two-reviewer replication and slow-model cap. |
| C-004 | COMBINE V2+V3 | V2's ledger above the block; V3's real-parser check of the fence. |
| C-005 | COMBINE V1+V2 | Substring check, demote unsupported rows to non-blocking, never script-write findings. |
| C-006 | COMBINE V1+V2 | V1's card schema with 120-word recipe; V2's named recipe steps. |
| C-007 | V2 | Source named, list every defect, blocker sentence; grading rule unchanged. |
| C-008 | V2 | Serial 8 s with kill at 15 s; build-while-reading as fallback. |
| C-009 | V2 | Deadline at 1.6 x baseline, +35% judged on medians; no 1.35 kill. |
| C-010 | V2 | Per-package b with overhead table and tightest cell; V3's mixed baselines inconsistent. |
| C-011 | V2 | Only variant citing the source table: +0.14, range 0.03-0.34. |
| C-012 | V2 | Ranges sum correctly from matrices; replace with measured act rate afterwards. |
| C-013 | V2 | Probabilities tied to cause map; all planning values pending hold-out. |
| C-014 | COMBINE V1+V2 | V1's n-gram lint and leave-one-class-out ablation; V2's swap test, second author. |
| C-015 | COMBINE V2+V1 | V2's real, spec, planted and clean-twin sets; V1's documentation arm. |
| C-016 | COMBINE V1+V2 | V1's A4 checklist control with G5; V2's placebo P and Z0-raw. |
| C-017 | COMBINE V2+V3 | V2's D1-D6 with planted-class gate; V3's package-level bootstrap. |
| C-018 | V2 | CB-3 sentence, UNSURE non-blocking, +1.0 wrong-blocker limit, clean-twin gate. |
| C-019 | V2 | T2a/T2b and T3a/T3b splits explain issues better. |
| C-020 | V2 | Realistic line counts without registry overbuild; V3's 240 lines understates. |
| C-021 | V2 | Explicit item letters per model; haiku capped at 6 items. |
| C-022 | NONE | All unmeasured estimates; log tokens per arm and replace. |
| C-023 | COMBINE V1+V2 | Union of anchoring, rubber-stamp, lens blind spot and dictation-blind rows. |
| C-024 | COMBINE V1+V2 | V1's adapter block kinds as re-derive checklist; V2's sentence-shape extractors. |
| X-001 | V2 | Source table gives +0.14 total, H4 = 0; V1 and V3 unsupported. |
| X-002 | V2 | Rubric constant; V1's CB2 allowed only as its own arm. |
| X-003 | V2 | 2 s per item; V3's +18 s for 40 lines fails token arithmetic. |
| X-004 | V2 | Consistent b; V3's B recomputes to 168 s (+38%) on b = 122. |
| X-005 | V2 | Kill at 1.35 x median discards reports; use 1.6 x deadline, medians. |
| X-006 | V2 | V1/V2 matrix sums recomputed and correct; V3's rows sum 3.50-6.05. |
| X-007 | V2 | 39% matches the seed (81 of 209); V3's 36% is one package. |
| X-008 | V2 | Stated cell needs no kill; V1's worst case relies on one. |
| A-001 | V2 | Act-rate readout replaces probabilities; judge credit and merge survival measured. |
| A-002 | V2 | Measure found fraction directly; sums are planning bounds only. |
| A-004 | V2 | H3 precondition, scope exclusion, 15 s kill, baseline-brief fallback. |
| A-006 | COMBINE V2+V1 | Non-blocking counts as found; report found-and-blocking separately, with V1's yield table. |
