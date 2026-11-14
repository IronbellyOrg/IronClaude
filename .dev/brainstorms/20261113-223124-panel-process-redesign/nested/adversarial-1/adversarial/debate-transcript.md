# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3 (Round 1 parallel statements, Round 2 sequential rebuttals, Round 2.5 invariant probe, Round 3 final arguments on the invariant findings)
- Convergence achieved: 97.6% strict (40 of 41 diff points have the same choice from at least 2 of 3 advocates); 100% compatible (41 of 41, nested choices). After Round 1: 73.2% strict (below the threshold). Computed by `scoring/convergence.py` (output in `scoring/convergence-output.txt`)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (V1 sonnet:architect, V2 sonnet:analyzer, V3 haiku:backend)
- Gates: taxonomy coverage L1/L2/L3 all covered (every one of the 41 points received a position from all three advocates); invariant gate blocked convergence after Round 2.5 (6 HIGH UNADDRESSED), cleared by Round 3 (every INV finding accepted or qualified by all three advocates, with a resolution to be written into the merged specification; see `invariant-probe.md`)
- Orchestrator checks made during the debate (evidence, not advocacy): X-001 against `.dev/brainstorms/20261113-163248-panel-collaboration/merged-requirements.md` lines 342-350 (H1-H4 total +0.14, range 0.03-0.34, H4 = 0); X-002 against line 320 (grading rule pinned); X-004 arithmetic recomputed; launcher keeps only the final result message (`run-reviewer.sh` lines 50, 57, 61-63); `src/superclaude/cli/review/findings.py` lines 90-158 (id, anchor, claim limits; more than one findings-v1 block sets ok=False)
- Advocate files: `debate/round1-V{1,2,3}.md`, `debate/round2-V{1,2,3}.md`, `debate/round2.5-faultfinder.md`, `debate/round3-V{1,2,3}.md`

## Round 1: Advocate Statements

### Variant 1 Advocate (V1 sonnet:architect)
#### Round 1 statement: Variant 1 (sonnet:architect)

#### Position

Finalize two genuinely different redesigns: A, a script-built Probe Sheet (V1 3.1, with V2's 12-item discipline and sheet-built-in-parallel option), and B, a prompt-only Recipe/Lens Ledger (V1 3.2 merged with V2's Redesign 2). Both draw their content from one class registry (V1 3.0). V3's pair is not distinct, and its time arithmetic does not hold.

#### Steelman of Variant 2

V2 has the best evidence discipline. It takes the harness-fix gain from the first brainstorm's own bottom-up table (+0.14, range 0.03-0.34), which I checked at merged-requirements.md:342-350. It keeps the grading rule unchanged (line 320), so a rubric edit never mixes with a design effect. It rejects a kill at 1.35 x median, because run-to-run spread would discard 25-40% of reports. It adds planted-defect documents with clean twins, a placebo arm and a Z0-raw arm, which measure recall and false positives on unseen text. Its option to build the sheet while reviewers do their first reads takes the pre-pass off the critical path. I verified its matrix sums (1.63-3.55; totals 3.2-5.7).

#### Steelman of Variant 3

V3 is the simplest to build (about 240 lines). Its blind verifier, which sees only the claim and the evidence, targets the real risk of forced items, false-positive growth. The research note reports 94-98% false-alarm removal for a tool-plus-model hybrid. It also has good operations hygiene: a real parser for the coverage block (closing the fence-opener-only BLOCK_OK gap), byte-identical determinism tests, a logged shuffle seed, and a bootstrap that resamples packages rather than runs.

#### Strengths claimed

1. **Class registry as the generality unit (3.0).** One card holds the definition, the recipe, the question template, the extractor, the route and the instances. Redesign A renders the question; Redesign B renders the recipe; a new class is one card (REQ-09). V2 and V3 hard-code class logic in scripts.
2. **Routing follows measured model habits.** Each card carries `route` and `replicas`. Luna "almost never searches" (seed), so it gets read items and ember gets search items (3.1(b)). V3 broadcasts all 60 items to both lunas (3.1(b)), including items that need repository searches.
3. **Controls that test the right claim.** A4 is a one-paragraph generic checklist with gate G5 ("gain over A4 of 4 or more points, otherwise A4 wins"). This tests the external finding that a checklist is no better than ad hoc reading. V2's placebo P (class names only) is weaker. V3 has no control.
4. **Mechanical answer checks.** The quote-substring check demotes unsupported PROBLEM rows and promotes unreported ones to MINOR (REQ-16/17/31). Its telemetry keys give a per-class yield table.
5. **Consistent arithmetic.** I recomputed every row: A is 6+122+12 = 140 (+14.8%); the worst case is 12+122+30 = 164 (+34.4%). The matrix sums reconcile (1.70-3.70 and 1.05-3.10), and totals 3.4-6.1 and 2.8-5.5 follow.
6. **Documentation arm and spec hold-out (G7)** test generality beyond plans. The breadth claim is withdrawn if they fail.

#### Weaknesses identified in Variants 2 and 3

1. **V3's baseline is inconsistent (X-004).** On its own b = 122, A = 6+122+18+3 = 149 (+22%, not +6%). B = 6+132+2+25+3 = 168 s (+37.7%), above its own 165 s ceiling; on b = 100, B is +46%. I verified this.
2. **V3's per-item cost is too low (X-003, A-009).** 40-60 coverage lines of JSON with an evidence field are about 1.4-3.6k tokens, or 29-75 s at 48 tokens/s, not +18 s.
3. **V3's arithmetic does not close (X-006).** Matrix A sums to 3.50-6.05 against the stated 3.6-6.6; B sums to 3.40-5.95 against 3.3-6.2. I verified both.
4. **V3's two redesigns are not distinct.** Both use the same helper. B only adds a verifier, which sits on the critical path. Neither tests the seed's open question of whether a prompt-only change can do the job.
5. **V3's validation is thin.** It has three packages and no spec or doc target (C-015), no placebo or checklist control (C-016), and labels matrix rows GT1.. so they cannot be mapped to the ten issues.
6. **V2 has quota-fixed sheets.** Its caps (Q2, U2, M2, R2, S2, K1, X1) crowd out real items with no stated ranking. Its extractors have no schema, so each new target means re-writing the script (C-024).
7. **V2's panel deadline is 1.6 x baseline**, which is +60% by construction. Only the median meets +35%.

#### Concessions

- X-001: my +0.2 to +0.7 for H1-H4 is an unsupported guess. Use +0.03 to +0.34 until Z0-raw measures it.
- X-002: CB2 rewrites the grading rule, so it must not be mixed into the control. It should run as a separate arm.
- X-005 and X-008: kill at D loses reports, and my worst case (+36%, or +42% at b = 100) relies on it. Replace it with a median-based judgement plus a 1.5 x hang guard.
- My scaffolding is the heaviest (about 1,300-1,500 lines), and the experiment (over 260 runs) is costly. The registry should ship as data cards with flat extractors, with no adapter classes before a second target exists.
- The upper totals (6.1) exceed the best run ever seen (4/14), and B has no issue at "consistent".

#### Shared assumptions

- A-001: QUALIFY. Split reach into trigger x act-rate x merge survival x judge credit, and replace the planning probabilities with the measured act rate (V2 U-015).
- A-002: QUALIFY. Probabilities are not additive; cap the claim at a stated prior, subtract displacement, and report measured totals only.
- A-003: QUALIFY. H and redesign gains overlap; report them as separate shares from arms A0, A1 and design, never summed in a headline.
- A-004: QUALIFY. This is an unproven precondition; run a timing spike, restrict greps to tests, root documents and named paths, and fall back to the isolated brief.
- A-005: QUALIFY. Compliance is the central risk of B, so measure it (quote check, tool-call cross-check) rather than assume it.
- A-006: QUALIFY. The study credits non-blocking finds, but the loop verdict needs blocking; report found-any and found-blocking separately.
- A-007: ACCEPT. Medians are stable enough if arms run in randomised blocks (V2).
- A-008: QUALIFY. The classes recur in one repository only; C1 and C3 are weak, so claim breadth per target type, and only after hold-out and planted-document results.
- A-009: REJECT. 2 s per item holds only for short rows and about 12 or fewer items; 40-60 items cost 29-75 s.

#### Position table

| point | preferred approach for the merged spec | reason in at most 15 words |
|---|---|---|
| S-001 | V1 | Separate comparison section; shared scaffolding first keeps both redesigns reviewable. |
| S-002 | V1 | Shared registry, brief edits and H1-H4 table placed before the redesigns. |
| S-003 | NONE | All three use identical (a)-(i) blocks. |
| S-004 | V1 | Grouped REQ tables with a Test column cover registry, time and validation. |
| S-005 | COMBINE V1+V2 | Numeric evidence tables plus V2's issue-to-cause map. |
| C-001 | COMBINE V1+V2 | Typed extractor items with evidence; hard cap on items, shuffled per reviewer. |
| C-002 | COMBINE V1+V2 | Prompt-only recipes and ledger; no sequential verifier stage on critical path. |
| C-003 | V1 | Route and replicas as data match measured model habits; no broadcast. |
| C-004 | COMBINE V2+V3 | Ledger under heading outside the findings block; real parser for the block. |
| C-005 | V1 | Substring check, demote unsupported, promote unreported as non-blocking MINOR. |
| C-006 | V1 | One card renders as question (A) or recipe (B); one source of truth. |
| C-007 | COMBINE V1+V2 | CB1, CB3, V2's blocker sentence; CB2 rubric change only as separate arm. |
| C-008 | COMBINE V1+V2 | Timeout-guarded pre-pass; V2's option to build the sheet during first reads. |
| C-009 | V2 | Median-based +35% judgement with hang guard; kill at 1.35 x loses reports. |
| C-010 | V1 | Per-package b with overhead table; V3 mixes 102 and 122. |
| C-011 | V2 | Sourced from first brainstorm table, +0.03 to +0.34, not guesses. |
| C-012 | COMBINE V1+V2 | Verified sums; subtract displacement; flag totals above best observed 4/14. |
| C-013 | COMBINE V1+V2 | Issue-id matrices tied to model slots; act-rate readout replaces priors. |
| C-014 | COMBINE V1+V2 | N-gram lint, freeze by tag, swap test, second-author review. |
| C-015 | COMBINE V1+V2 | Real plans, spec H1, documentation arm, planted documents with clean twins. |
| C-016 | COMBINE V1+V2 | A4 checklist control, Z0-raw, placebo; V3 has none. |
| C-017 | COMBINE V1+V2 | Reach-rate consistency, pre-registered gates, planted-class gate, bootstrap clustered by package. |
| C-018 | COMBINE V1+V2 | Blocking needs grading sentence plus two quotes; clean-twin wrong-blocker gate. |
| C-019 | COMBINE V1+V2 | Numeric tables and T2a/T2b split; reject reasoning-budget rival. |
| C-020 | COMBINE V1+V2 | Registry as data cards, flat extractors; no adapter classes until second target. |
| C-021 | V1 | Ember search items, lunas read items, haiku capped, sonnet takes searches. |
| C-022 | NONE | Overheads of +25-42% are similar and all estimates. |
| C-023 | V1 | Covers kills, anchoring on items, and dictation-blind classes for both redesigns. |
| C-024 | COMBINE V1+V2 | Registry with target adapters; list per-target re-derivation items. |
| X-001 | V2 | Source table gives +0.14; V1 and V3 figures are unsupported guesses. |
| X-002 | V2 | Grading rule held constant; CB2 tested separately so effects are not mixed. |
| X-003 | COMBINE V1+V2 | About 2 s per short item up to roughly 12 items; V3's +18 s refuted. |
| X-004 | V1 | Same b throughout: V3 recomputes to +22% (A) and +37.7% (B). |
| X-005 | V2 | Kill at 1.35 x median discards reports; use 1.5 x hang guard. |
| X-006 | V2 | V2 and V1 sums reconcile; V3's do not (3.50-6.05 vs 3.6-6.6). |
| X-007 | NONE | Seed's 39% is the reference; V3 quoted one package. |
| X-008 | V2 | Design to the median with slack; do not rely on kill. |
| A-001 | COMBINE V1+V2 | Split reach factors; measure act rate; log merge-survival drops. |
| A-002 | COMBINE V1+V2 | Subtract displacement, cap prior, replace sums with measured totals. |
| A-004 | COMBINE V1+V2 | Timing spike, limited greps, parallel sheet build, fallback to isolated brief. |
| A-006 | COMBINE V1+V2 | Report found-any and found-blocking separately; blocking needs two quotes. |

### Variant 2 Advocate (V2 sonnet:analyzer)
#### Round 1 statement: Variant 2 (sonnet:analyzer)

#### Position

Finalize (A) a script-built Sweep Sheet and (B) a written Recipe Ledger with no pre-pass. They answer the seed's open question from opposite sides, and both fit +35% on per-package medians. Take V1's class registry, extractor blind spots and generic-checklist control, V2's sourced numbers, unchanged grading rule and decision gates, and V3's real-parser check and package-level bootstrap.

#### Steelman of Variant 1

V1 is architecture first. One class card renders either as a question (A) or as a recipe (B), so a new class or target is a card plus an adapter, not a dispatcher edit. It names each extractor's blind spot. It discloses its own worst case ("kill-limited"). Its arm A4 (a generic checklist) with gate G5 tests the human-inspection finding that checklists add little. I recomputed its matrix sums (A 1.70-3.70, B 1.05-3.10) and they are correct.

#### Steelman of Variant 3

V3 is the leanest build (about 240 lines). It is the only variant with a blind verifier that sees just claim, anchor and evidence, which fits the herding evidence and attacks the real risk of forced items, false positives. It also finds the fence-opener-only parse gap and resamples packages rather than runs, the honest unit of independence.

#### Strengths claimed

1. Sourced harness share: V2 uses +0.14 (0.03-0.34). I checked merged-requirements.md:342-350: 0.08+0.03+0.03+0, with H4 = 0. V1 (+0.2-0.7) and V3 (+0.4-0.9) are 1.5-6x higher without derivation (X-001).
2. Rubric held constant: "The grading rule itself is unchanged" (CB-3 only limits blocking), matching merged-requirements.md:320. V1's CB2 rewrites the Medium sentence.
3. Consistent arithmetic (X-004): V3 on b = 122 gives A = 6+122+18+3 = 149 (+22%) and B = 6+132+2+25+3 = 168 (+38%, over its own 165 ceiling). On b = 100 B is 146 (+46%). V2 shows its tightest cell (128 s vs 135 s).
4. Per-item cost (X-003): V3's 40 lines at about 35 tokens is 1.4k tokens, about 29 s at V1's 48 tokens/s, and 60-80 s at V1/V2's 1.5-2 s per item, not +18 s. With 29 s, A is +31% at b = 122 and +38% at b = 100.
5. Two independent hypotheses (script vs instruction only). V3's A and B both need `panel_prepass.py`, so its experiment cannot say whether the script is necessary.
6. Validation controls: planted defects, clean twins, placebo P and Z0-raw (U-012, U-013, U-015).

#### Weaknesses identified in Variants 1 and 3

1. V1: modelled worst case +36% (b = 122) and +42% (b = 100) exceeds its own D = 135 and relies on a kill that discards reports (X-005, X-008). It is the heaviest build (1,300-1,500 lines). E4 greps the "whole base checkout" while failure modes say grep is restricted. Auto-promotion writes script-authored findings.
2. V1's CB2 changes production blocking semantics. Its A1 control includes CB1-CB4, so redesign-versus-A1 stays clean (this narrows X-002), but A0-versus-A1 no longer measures harness-only gain.
3. V3: one shared list in class order (C6 first, C1 and C3 last), capped at 60. A plan with many "all/every/each/only/any" sentences fills the cap with C6 and drops C1/C3 (B1, B2, I1). Nothing ranks items.
4. V3 arithmetic: matrix rows sum 3.50-6.05, text says 3.6-6.6; "+1.2 to +2.3" has no derivation (X-006). Haiku and sonnet times reuse luna's +18 s though haiku's per-line cost is higher.
5. V3 validation: 3 packages, 8 runs, no placebo or checklist control; it cannot separate recipe from list.

#### Concessions

- My 3(f) totals add H and redesign (3.2-5.7), contradicting my R-30 "never summed in a headline". The +0.14 is borrowed, not measured.
- The tightest cell has 7 s slack, the 8 s pre-pass is unmeasured, and the +22 s luna load for R-C2 is optimistic.
- My claim that a 1.35 kill discards 25-40% of reports cites no number. Check it on A0 timing data.
- About 254 panel runs is the costliest plan. V3's blind verifier is a better false-positive guard than mine but breaks +35% as specified.
- The 12-item cap with Q2/U2/M2/R2/S2 can crowd out a class on a large plan.

#### Shared assumptions

- A-001: QUALIFY. My matrices fold judge credit and merge survival into one probability; the measured act-rate readout (D-table, "Act-rate readout") must replace them.
- A-002: QUALIFY. Summing is only a planning upper bound after a flat displacement; the decision rule uses measured found fraction, not sums.
- A-003: QUALIFY. H and redesign gains overlap on I4, B5 and I1 (H3 masks them), so they are bounded, not additive; Z0-raw versus Z0 measures it.
- A-004: QUALIFY. A pre-implementation sandbox and a 6-8 s search are unverified; require H3 as precondition, exclude `.dev/` from sweeps, kill at 15 s, fall back to the baseline brief.
- A-005: QUALIFY. Rubber-stamping is the main risk; the what-you-ran transcript audit, planted-item OK-rate and placebo arm test it.
- A-006: QUALIFY. A non-blocking finding counts for the study score (all 7 true I7 finds were non-blocking), but report found-and-blocking separately because the loop verdict needs blocking.
- A-007: ACCEPT. Block-randomised arms and per-panel medians make the baseline stable enough; track drift in the manifest.
- A-008: QUALIFY. Counts are phrase-search lower bounds in one repository; claim C1, C3 and narrow C7 only as the hold-out supports.
- A-009: QUALIFY. About 2 s per item holds for at most 12 written items; it fails for V3's 40-60 items, and 48 tokens/s is derived and unverified.

#### Position table

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

### Variant 3 Advocate (V3 haiku:backend)
#### Position
Finalize exactly two redesigns: a bounded Sweep Sheet, combining V1's class cards, V2's routing and V3's audit safeguards; and blind Recipe Lenses, combining V1/V2's enumeration ledgers with V3's claim-only verification only when measured spare time permits. Do not retain V3's full-list replication or unconditional sequential verifier.

#### Steelman of Variant 1
V1's strongest argument is maintainability: one target-neutral class card serves both designs, while adapters identify document structure (§3.0). Its explicit extractor blind spots and checklist-control gate distinguish useful machinery from expensive ceremony (§3.1, §5 G5).

#### Steelman of Variant 2
V2 best separates causal effects: frozen grading, harness-only comparison, planted defects and clean twins (§3 shared changes; §5). Its twelve-item sheet and model-specific routing confront attention limits rather than assuming larger prompts improve coverage.

#### Strengths claimed
1. V3 treats reporting as a data contract: separate `coverage-v1`, explicit `unchecked`, and real parsing rather than fence-opener detection (§3.1(a), §3.3). Preserve these safeguards without requiring sixty answers.
2. V3's verifier sees only candidate claims and evidence, cannot invent findings, and archives rejected or unverified claims (§3.2(a), (i)). This separates detection from confirmation without majority voting; it does not eliminate anchoring.
3. Byte-identical helper output, logged shuffle seeds, dropped-item counts and sandbox hashes make missing coverage diagnosable (§5 requirements 3, 4, 14). These are cheap, portable integrity checks.
4. Package-level bootstrap resampling respects dependence between repeated runs on one document (§4). Keep it, while acknowledging that three packages give weak inference.

#### Weaknesses identified in Variants 1 and 2
1. V1 changes the Medium rule (§3.0 CB2), confounding process and grading; the prior merged requirements explicitly freeze grading and judge (line 320). Take V2's unchanged-rubric approach.
2. V1 auto-promotes unmatched PROBLEM rows to MINOR findings (§3.1(a)). Substring evidence establishes quotation, not a valid defect; prefer V2's audit flags and V3's explicit verification boundary.
3. V1's primary-panel worst cases exceed +35% and rely on lost reports (§3.1(c)); V2's two-seconds-per-item assumption is also unmeasured (§3.1(c)). Neither timers nor estimates establish acceptable recall at the deadline.
4. V2's twelve-item ceiling can crowd out entire classes (§3.1(i)); log omissions and stratify selection, rather than claiming every extracted trigger reaches a reviewer.

#### Concessions
X-001: the source table gives H3 +0.08, H1 +0.03, H2 +0.03, H4 zero: +0.14 centrally, +0.03–0.34 overall; my +0.4–0.9 is unsupported. X-002: keep grading fixed.

X-003: forty lines ×35 tokens ÷48 tokens/second =29.2 seconds; sixty =43.8 seconds, before checks or thinking, under that unverified generation-rate model. My eighteen seconds is untenable.

X-004: consistent baselines give A=6+122+18+3=149 seconds (+22.1%); B=6+132+2+25+3=168 (+37.7%). At b=100, A=127 (+27%), B=146 (+46%); B fails even before correcting item cost. The exact b=122 ceiling is164.7, not165.

X-006: A's matrix sums to3.50–6.05 including control, or2.95–5.25 excluding it; B sums to3.40–5.95. Withdraw unsupported yield discounts and totals. X-007: distinguish14/39=35.9% in one package from81/209=38.8% overall. Also withdraw command-only evidence requirements for reading defects, anchor-overlap deduplication that loses distinct claims, and the narrow validation claim.

#### Shared assumptions
- A-001 QUALIFY — Measure extraction, action, merge survival and judge credit separately.
- A-002 QUALIFY — Expectations add without independence, but attention interference changes their marginal probabilities.
- A-003 REJECT — Report conditional arm differences rather than adding assumed harness and redesign gains.
- A-004 QUALIFY — Verify snapshot availability and measure bounded search before trusting pre-pass timing.
- A-005 QUALIFY — Audit tool evidence and planted-item responses rather than trusting completed ledgers.
- A-006 QUALIFY — Confirm scoring accepts non-blockers and report discovery separately from blocking decisions.
- A-007 QUALIFY — Randomize blocks and remeasure each package's contemporaneous baseline.
- A-008 QUALIFY — Treat classes as hypotheses beyond this repository until fresh-target validation.
- A-009 REJECT — Two seconds is an unmeasured planning estimate, not a universal upper bound.

#### Position table
| point | preferred approach for the merged spec (V1, V2, V3, COMBINE V#+V#, or NONE) | reason in at most 15 words |
|---|---|---|
| S-001 | V1 | Put common prerequisites before both designs and give comparison its own section. |
| S-002 | V1 | Shared requirements must precede mechanisms depending on them. |
| S-003 | V1 | Retain matching subsections for direct comparison. |
| S-004 | V1 | Grouped requirements with explicit tests simplify compliance checks. |
| S-005 | V2 | Issue-to-cause mapping makes mechanism selection inspectable. |
| C-001 | COMBINE V1+V2 | Typed class items with bounded total selection avoid full-list overload. |
| C-002 | COMBINE V2+V3 | Recipe lenses remain distinct; admit claim verification only within measured spare time. |
| C-003 | V2 | Two blind assignments per selected item limit replicated work. |
| C-004 | V3 | Parse separate coverage records without altering findings-v1. |
| C-005 | COMBINE V2+V3 | Flag missing findings; verify claims rather than mechanically promoting them. |
| C-006 | V1 | Explicit class cards expose recipe, extractor and known weakness. |
| C-007 | V2 | Require reporting while keeping severity grading fixed. |
| C-008 | V2 | Measure serial cost; overlap initial reading only after validating synchronization. |
| C-009 | V2 | Judge median elapsed separately from hang guards and lost reports. |
| C-010 | V2 | Use each package's slowest-reviewer baseline consistently. |
| C-011 | V2 | Source-supported harness estimate replaces guesses until measured. |
| C-012 | NONE | Replace speculative totals with measured conditional effects. |
| C-013 | NONE | Decompose and measure probabilities before treating them as forecast evidence. |
| C-014 | COMBINE V1+V2 | Freeze cards, audit outside instances, and apply independent swap tests. |
| C-015 | COMBINE V1+V2 | Include real documents, fresh planted examples and clean twins. |
| C-016 | COMBINE V1+V2 | Preserve raw, fixed-harness, checklist and recipe controls. |
| C-017 | COMBINE V2+V3 | Preregister repeated-hit criteria; bootstrap documents, not independent-looking repeats. |
| C-018 | COMBINE V2+V3 | Frozen blocking rule plus budgeted verification; retain rejected claims for audit. |
| C-019 | V2 | Separate trigger absence, wrong question, environment and suppression. |
| C-020 | NONE | Scope and prototype before trusting incompatible line-count estimates. |
| C-021 | V2 | Route evidence work to fast reviewers; cap critical-path assignments. |
| C-022 | NONE | Measure token overhead with actual ledgers and tool work. |
| C-023 | COMBINE V1+V3 | Cover extraction failures, lost reports, verifier false negatives and correlated lenses. |
| C-024 | V1 | Target adapters make portability assumptions explicit instead of promising universal markdown support. |
| X-001 | V2 | Verified source estimate is +0.03–0.34, central +0.14. |
| X-002 | V2 | Freeze grading and judge across arms. |
| X-003 | NONE | Benchmark item latency; eighteen seconds for forty answers is unsupported. |
| X-004 | V2 | Consistent baselines expose V3's verifier deadline failure. |
| X-005 | V2 | Median-time acceptance must not hide reports discarded by aggressive kills. |
| X-006 | NONE | Correct sums and remove unexplained discounts before publishing yield forecasts. |
| X-007 | V2 | Use overall source-skip denominator; label package-specific figures separately. |
| X-008 | V2 | Prefer bounded workload estimates over claiming kills guarantee acceptable performance. |
| A-001 | NONE | Measure pipeline stages separately; credited findings are the final endpoint. |
| A-002 | NONE | Summation is valid only for workload-conditioned marginals, not isolated-item guesses. |
| A-004 | COMBINE V2+V3 | Verify snapshot hashes and search budgets; expose partial or failed extraction. |
| A-006 | COMBINE V2+V3 | Keep discovery credit separate from verified blocking status. |

## Round 2: Rebuttals

### Variant 1 Rebuttal
#### Round 2 rebuttal: Variant 1 (sonnet:architect)

#### Responses to criticisms

- **Auto-promotion (V2, V3).** Partly conceded. The harness must not author a claim, and a substring match proves only that a quote exists. But the reviewer already wrote PROBLEM or DEFECT in its own ledger row, and the merge reads only the findings block, so without promotion the reviewer's own verdict is silently lost. Fix: append a MINOR non-blocking finding built from the reviewer's row, tag it `src=ledger`, never let it count toward blocking, and report it separately (V3's boundary). V3's blind verifier is not the alternative because it breaks +35%.
- **CB2 (V2, V3).** Conceded. The grading rule stays unchanged; CB2 runs only as its own arm. A1 contains CB1, CB3 and the blocker sentence, so redesign versus A1 stays clean.
- **Registry and adapter weight (V2).** Conceded. Ship data cards with flat extractors and a block-kind checklist; no adapter code before a second target.
- **Extractor caps and crowd-out (V2, V3).** Conceded the lack of ranking. My cap is per reviewer, but the final sheet needs a class quota, ranked selection and a dropped-item log.
- **E4 grep scope (V2).** Conceded. E4 is limited to tests, root documents and named paths; skip rather than grep `.dev/`.
- **Worst case relying on a kill (V2).** Conceded (X-005/X-008).

#### Open design questions

- Q1: No; the blind verifier stays off the critical path, and may run only in the off-path audit.
- Q2: Yes.
- Q3: Yes: at most 12 items, each to exactly 2 reviewers; at least 1 and at most 2 items per triggered class, the remaining slots filled by ranked trigger strength, with a dropped-item log.
- Q4: Yes.
- Q5: V1: a second fresh ember session, launched only if the first ended before 0.45 x b, with at most 4 recipes per session.
- Q6: Yes.
- Q7: Yes.
- Q8: Yes.
- Q9: Yes.
- Q10: Yes.

#### Contested points

| point | choice | moved? |
|---|---|---|
| C-003 | COMBINE V1+V2 (route as card data; replicas = 2 blind) | yes |
| C-005 | COMBINE V1+V3 (substring check; ledger promotion tagged and reported separately) | yes |
| C-012 | COMBINE V1+V2 (verified sums; measured values replace them) | no |
| C-013 | COMBINE V1+V2 (issue-id matrices, planning values) | no |
| C-018 | COMBINE V1+V2 (grading sentence plus two quotes; clean-twin gate) | no |
| C-020 | COMBINE V1+V2 (V1 data cards; V2 line counts) | yes |
| C-023 | COMBINE V1+V2+V3 (union of failure rows) | yes |
| X-003 | V2 (2 s per item up to 12 items) | yes |
| A-001 | V2 (act-rate readout replaces probabilities) | yes |
| A-002 | V2 (sums are planning bounds only) | yes |
| A-004 | COMBINE V2+V3 (H3 precondition, snapshot hash, 15 s kill, fallback) | yes |

### Variant 2 Rebuttal
#### Round 2 rebuttal: Variant 2 (sonnet:analyzer)

#### Responses to criticisms

- **12-item cap crowds out classes (V1, V3).** Conceded. My fixed per-class caps (Q2/U2/M2/R2/S2) are replaced by V1's quota: 1 to 2 items per triggered class, remaining slots filled by ranked trigger strength, and a dropped-item log that records every omission.
- **1.6 x deadline (V1).** Conceded as written. It is a hang guard at 1.5 x (the X-005/X-008 outcome), not an acceptance limit. +35% is judged on medians, and I rely on no kill.
- **3(f) adds H and redesign.** Conceded again. The +0.14 is borrowed, and the two shares are reported separately from Z0, Z0-raw and the redesign arms. No headline sum.
- **254-run cost (V1).** Accepted. I stage the arms: Stage 1 runs Z0, Z0-raw, K, A and B on the real packages. The planted-defect, clean-twin, spec/doc and sonnet/haiku sets run only for arms that pass D1. Merging P into K removes one arm. I have not recounted the total.
- **+22 s luna load unmeasured.** Conceded. A 5-run timing spike on luna comes before any arm runs. If luna's median plus overhead exceeds the +35% cell, luna's share drops to 8 items.
- **V1's auto-promotion fix.** I move. The harness builds no claim; it copies the reviewer's own row, as a MINOR non-blocking finding tagged `src=ledger`, so my objection (script-authored findings) is met. It is reported separately and is never blocking.
- **V1's second ember session.** It adds load and a second variable to an A-versus-B comparison that should isolate prompt-only. I keep one session.

#### Open design questions

- Q1: No; the blind verifier stays off the critical path, in the off-path audit only.
- Q2: Yes; data cards, flat extractors and a block-kind checklist, with no adapter code until a second target exists.
- Q3: Yes; at most 12 items, each to exactly 2 blind reviewers, a quota of at least 1 and at most 2 items per triggered class, the rest ranked, with a dropped-item log.
- Q4: Yes; a MINOR non-blocking finding built from the reviewer's row, tagged `src=ledger` and reported separately.
- Q5: V2: one session per reviewer with at most 4 recipes.
- Q6: Yes; one generic-checklist arm K naming the eight checks in plain words, plus Z0-raw.
- Q7: Yes; labels B1..I7 throughout, with I7 (control package, scored /2) outside every "of 14" sum.
- Q8: Yes; the mean of the V1 and V2 matrices, labelled planning values, replaced by the measured act rate.
- Q9: Yes; per-package medians against the slowest-reviewer baseline, a 1.5 x hang guard, and a pre-pass kill at 15 s with fallback to the isolated brief.
- Q10: Yes; D1-D6 plus G5 and G7 plus the package-level bootstrap, with consistent meaning reached in at least 60% of runs.

#### Contested points

| point | choice | moved? |
|---|---|---|
| C-003 | COMBINE V1+V2 (route and replicas as card data; 2 blind replicas, slow-model cap) | no |
| C-005 | COMBINE V1+V2 (substring check, demote unsupported rows, ledger promotion tagged `src=ledger`, non-blocking, reported separately) | yes |
| C-012 | V2 (verified sums are planning bounds, replaced by measured values) | no |
| C-013 | V2 (matrices tied to the cause map; planning values only) | no |
| C-018 | COMBINE V2+V1 (CB-3 sentence plus two quotes for blocking; clean-twin gate; +1.0 wrong-blocker limit) | yes |
| C-020 | COMBINE V1+V2 (V1 data cards with flat extractors; V2 line counts) | yes |
| C-023 | COMBINE V1+V2+V3 (union of failure rows, including verifier false negatives and flood in the off-path audit) | yes |
| X-003 | V2 (about 2 s per item, valid up to 12 items) | no |
| A-001 | V2 (act-rate readout replaces probabilities) | no |
| A-002 | V2 (sums are planning bounds only) | no |
| A-004 | COMBINE V2+V3 (H3 precondition, snapshot hash, `.dev/` excluded from sweeps, 15 s kill, fallback to the isolated brief) | yes |

### Variant 3 Rebuttal
#### Responses to criticisms

Conceded: my shared-list designs were insufficiently distinct; finalize script-built Sweep Sheet A and prompt-only Recipe Ledger B. Quotas and ranked selection replace class-order truncation, protecting C1/C3 from C6 crowd-out. Adopt V1/V2's broader validation and controls.

Keep the blind claim-only verifier for both designs solely as an optional off-path audit when measured spare time remains; it cannot add claims, delay completion, or supply assumed recall gains. Archive rejected/unverified claims. Both designs share real coverage-record parsing and byte-identical harness-rendering tests; A additionally tests deterministic extraction and logs shuffle seeds. B's reviewer process needs no pre-pass. Both validation plans retain package-level bootstrap and stable-hit rates, acknowledging limited package diversity.

V1's revised ledger copying answers my authorship objection, not defect validity: tag and score it separately. Prefer V2's single session over V1's fresh ember pass to isolate the prompt-only effect.

#### Open design questions

Q1: No; verification stays off-path, conditional on measured spare time.
Q2: Yes; data cards, flat extractors, block-kind checklist, no adapters before a second target.
Q3: Yes; 12 total, exactly two blind reviewers each, 1–2 per triggered class, remaining slots ranked, every omission logged.
Q4: Yes; copy the reviewer's row as MINOR non-blocking, tagged `src=ledger`, reported separately.
Q5: V2: one session per reviewer, at most four recipes.
Q6: Yes; generic eight-check arm K plus Z0-raw.
Q7: Yes; B1..I7 consistently, I7 scored /2 outside every “of 14” sum.
Q8: Yes; average V1/V2 matrices per redesign as planning values, replaced by measured act rates.
Q9: Yes; +35% on per-package medians against the named isolated slowest-reviewer baseline (100–122 seconds for ember + 2x luna), 1.5x hang guard, 15-second pre-pass kill with isolated-brief fallback.
Q10: Yes; D1–D6, G5, G7, package-level bootstrap, consistent meaning reached in at least 60% of runs.

#### Contested points

| point | choice | moved? |
|---|---|---|
| C-003 | COMBINE V1+V2: card routing, two blind replicas | yes |
| C-005 | COMBINE V1+V2+V3: substring audit, tagged copying, verification boundary | yes |
| C-012 | COMBINE V1+V2: recomputed planning bounds; measured replacements | yes |
| C-013 | COMBINE V1+V2: averaged issue-labelled planning matrices | yes |
| C-018 | COMBINE V1+V2+V3: two-quote blocking, clean twins, off-path verifier | yes |
| C-020 | COMBINE V1+V2: data-card scope, prototype effort before estimates | yes |
| C-023 | COMBINE V1+V2+V3: union of failure modes | yes |
| X-003 | V2: bounded-item timing estimate, benchmarked | yes |
| A-001 | COMBINE V2+V3: act-rate replacement, separate pipeline-stage telemetry | yes |
| A-002 | V2: planning bounds only; measure totals | yes |
| A-004 | COMBINE V2+V3: H3, snapshot hash, bounded searches, fallback | no |

## Round 2.5: Invariant Probe
The independent fault-finder report is `debate/round2.5-faultfinder.md` (14 findings: 6 HIGH, 8 MEDIUM); the assembled table is `invariant-probe.md`.

## Round 3: Final Arguments
Round 3 addressed the invariant findings (condition: the invariant gate blocked convergence although diff-point agreement was 97.6 percent). Each advocate answered every INV finding and six orchestrator amendments (ledger carrier, serial pre-pass, offline selection-recall gate, narrowed claim and recomputed tables, time-budget break-evens, intention-to-treat scoring).

### Variant 1 Final Position
#### Round 3 final arguments: Variant 1 (sonnet:architect)

INV-001 | ACCEPT | Add an offline selection-recall gate with a stated floor, log all candidates, and publish a rank function that must beat a random pick on the three derivation plans.
INV-002 | ACCEPT | The brief says "copy the complete ledger into your final message directly above the findings block"; the checker also reads concatenated assistant text; the `ledger_missing` rate is a pre-registered precondition.
INV-003 | ACCEPT | State break-evens (pre-pass 14 s, 2.75 s per item at b=100), kill = min(15 s, 0.10 x b), fallback 6 items per luna with ember taking the remainder, one panel clock from before the pre-pass.
INV-004 | ACCEPT | Claim "raises the per-run found fraction; consistency expected only for C4, C5, C8"; pre-register a band for each class's measured act rate.
INV-005 | ACCEPT | Build the line from the PROBLEM statement and a plan-side anchor, check it with `_check_finding` (id <=16 chars, anchor 12-200, claim <=300, MINOR non-blocking), insert it inside the single findings block, and log and skip on failure; use `flat()`/`locate`.
INV-006 | ACCEPT | Recompute the planning matrices from the consensus design only (cap 12, one session, V2 lens sets) and drop V1's values.
INV-007 | ACCEPT | JSON-lines `ledger-v1` fence, a real parser, flattened substring tests, and a reported share of demotions caused by format.
INV-008 | ACCEPT | Hang guard = 1.5 x (b + expected overhead) from launch; report kills and retries per arm; score intention-to-treat.
INV-009 | QUALIFY | Plant defects into full-size real hold-out plans with at least 8 competing candidates per class, and keep clean twins; D5 counts only documents meeting that candidate count.
INV-010 | QUALIFY | Give each recipe its own row budget (about 14 per lens) and drop the luna re-ask; replicate a class on a second reviewer only when its evidence is attached, otherwise replica 1, with `ledger_missing` logged.
INV-011 | ACCEPT | Specify assignment as an algorithm over 24 slots with caps summing to it, replica 1 for items without attached tool output, and drop to replica 1 when a reviewer fails.
INV-012 | ACCEPT | Serial pre-pass is the single specified mode; parallel is a later arm with atomic write and a per-reviewer path.
INV-013 | ACCEPT | Render CB-1 and the C2 extractor only when a source exists, log `no_source`, mark C2 not applicable, and record the snapshot rule.
INV-014 | ACCEPT | Displacement is measured, planning range 0.1 to 0.9; add a free-review floor to the brief; D6 stays a blocking gate.

Amendments:
(a) Agree: a distinct `ledger-v1` fence leaves the single `findings-v1` rule untouched; promotion reads only the final-message ledger, and concatenated text serves diagnosis.
(b) Agree.
(c) Agree; it is the cheapest gate and runs first.
(d) Agree, with the selection factor shown as its own column.
(e) Agree; I concede the luna re-ask cannot fire.
(f) Agree; without it the arms are not comparable.

### Variant 2 Final Position
#### Round 3 final arguments: Variant 2 (sonnet:analyzer)

INV-001 | ACCEPT | Run an offline selection-recall gate with a stated floor before any model arm, log all candidates (not only dropped ones), and publish a rank function that must beat a random pick on the three derivation plans.
INV-002 | ACCEPT | The brief requires the complete `ledger-v1` block in the final message directly above the findings block; only that block is parsed and promoted, and the `ledger_missing` rate from the timing spike is a pre-registered precondition.
INV-003 | ACCEPT | State break-evens (pre-pass 14 s and 2.75 s per item at b=100), kill = min(15 s, 0.10 x b), fallback 6 items per luna with ember taking the remainder, and one panel clock starting before the pre-pass, reporting mean and median against same-day Z0.
INV-004 | ACCEPT | Claim "raises the per-run found fraction; consistency expected only for C4, C5, C8", drop the word "consistent" from the central estimate, and pre-register a band for each class's measured act rate.
INV-005 | QUALIFY | Promotion copies the reviewer's own PROBLEM text (the ledger row carries a separate `problem` field of 300 characters or fewer) and takes the anchor from the plan-side quote; the line is checked with `_check_finding`, inserted inside the single existing block, tagged MINOR non-blocking `src=ledger`, and logged and skipped on any failure; use `flat()` and `locate`.
INV-006 | ACCEPT | Recompute the planning matrices once from the consensus design only (cap 12, one session, V2 lens sets), with the selection factor as its own column, and drop both original matrices from the mean.
INV-007 | ACCEPT | JSON-lines `ledger-v1` fence, a real parser, flattened substring tests, and a reported share of demotions caused by format rather than defect.
INV-008 | ACCEPT | Hang guard = 1.5 x (b + expected overhead) from reviewer launch, kills and retries counted per arm, and killed reviewers scored as zero findings.
INV-009 | ACCEPT | Plant defects into full-size real hold-out plans with at least 8 competing candidates per class, keep clean twins, and gate D5 only on documents meeting that count.
INV-010 | QUALIFY | Give each recipe its own row budget (about 14 per lens), drop the luna re-ask, log `ledger_missing`, and replicate a class on two reviewers only where ember has idle time and the evidence is attached.
INV-011 | ACCEPT | Specify assignment as an algorithm over 24 slots with caps that sum to it, replica 1 for items without attached tool output, and drop to replica 1 (no growth in other reviewers' load) when a reviewer fails.
INV-012 | ACCEPT | The serial pre-pass is the single specified mode; the parallel build is a later separate arm with atomic rename and a per-reviewer path.
INV-013 | ACCEPT | Render CB-1 and the C2 extractor only when a source file exists, log `no_source`, count C2 as not applicable for that document, and record the snapshot rule.
INV-014 | ACCEPT | Treat displacement as measured with a planning range of 0.1 to 0.9, add a free-review floor to the brief, and keep D6 as a blocking gate.

#### Amendments

(a) Agree: `ledger-v1` JSON lines in the final message directly above the findings block, parsed by a real parser; only that block is promoted.
(b) Agree.
(c) Agree; it runs first.
(d) Agree; the selection factor and the 0.1 to 0.9 range are explicit.
(e) Agree; the luna re-ask cannot fire.
(f) Agree.

#### Disagreement with V1 Round 3

V1's INV-002 line says "the checker also reads concatenated assistant text". That contradicts amendment (a). Concatenated text is diagnosis only and never feeds promotion or the `ledger_missing` verdict.
V1's INV-005 line has the harness "build the line from the PROBLEM statement". It should copy the reviewer's own PROBLEM field, so no script-authored claim exists.

### Variant 3 Final Position
INV-001 | ACCEPT | Pre-register selection-recall floors, log candidates; ranking must beat random offline.
INV-002 | QUALIFY | Require final-message ledger; earlier text cannot affect promotion or ledger_missing.
INV-003 | ACCEPT | Publish break-evens: 14-second pre-pass and 2.75 seconds/item at b=100; measure panel means and medians.
INV-004 | ACCEPT | Expect consistency only for C4/C5/C8; pre-register act-rate tolerances.
INV-005 | QUALIFY | Copy PROBLEM verbatim; validate unique legal IDs ≤16, plan anchors 12–200, claims ≤300, category, MINOR/non-blocking; insert inside one findings block, otherwise log/skip.
INV-006 | ACCEPT | Recompute consensus-only matrices with selection factors; discard original averages.
INV-007 | ACCEPT | Parse JSON-lines ledger-v1; normalize whitespace for matching and report format-induced demotions.
INV-008 | ACCEPT | Guard at 1.5×(baseline+overhead) from reviewer launch; report kills/retries and intention-to-treat totals.
INV-009 | ACCEPT | Full-size planted hold-outs need ≥8 candidates/class and clean twins.
INV-010 | QUALIFY | Budget rows per recipe; replicate only with attached evidence and spare capacity; log missing ledgers.
INV-011 | QUALIFY | Assign within 24-slot capacity, reducing replicas without attached output; failures never increase survivors’ loads.
INV-012 | ACCEPT | Specify serial pre-pass only; parallel is a separate arm.
INV-013 | ACCEPT | Missing source disables C2; record no_source, non-applicability, and working-tree snapshot identity.
INV-014 | ACCEPT | Measure displacement, plan 0.1–0.9, reserve half-time free review, retain blocking non-regression gate.

(a) Accept final-only fenced ledger parsing and promotion, with concatenation diagnostic only.
(b) Accept serial-only mode.
(c) Accept offline recall and above-random derivation gates before model arms.
(d) Accept the narrowed claim and consensus-only, selection-adjusted tables.
(e) Accept min(15s,0.10×b), pre-pass-start clock, no luna re-ask, six/luna plus ember remainder, and unattached-output replica 1.
(f) Accept zero findings for killed or retried reviewers.

INV-005: Choose V2’s copying because rewriting introduces harness-authored claims.
INV-002: Choose V2’s final-only promotion because earlier text is outside the retained report.

## Scoring Matrix

Winner = the variant (or combination) the advocates' final stances select for the merged specification. "V1+V2" means both contribute (V1 base ideas plus V2 amendments). Confidence follows the calibration rules (unanimous with checked evidence 90-98%; majority 60-89%). Taxonomy level in the last column is auto-tagged from the signal terms (L1 surface, L2 structural, L3 state mechanics).

| Diff Point | Winner | Confidence | Evidence Summary | Level |
|------------|--------|------------|------------------|-------|
| S-001 | V1 | 70% | Separate comparison section; 2 of 3 advocates (V1, V3) | L1 |
| S-002 | V1 | 75% | Shared scaffolding before the redesigns | L1 |
| S-003 | all (identical) | 90% | All three use (a)-(i) blocks; keep | L1 |
| S-004 | V1 | 75% | Grouped requirement tables with a Test column | L1 |
| S-005 | V2 | 80% | Issue-to-cause map plus numeric tables (V1+V2) | L1 |
| C-001 | V1+V2 | 95% | Typed extractor items, 12-item cap, shuffle; no 60-item list (all three) | L2 |
| C-002 | V1+V2 | 80% | Prompt-only recipes and ledger; verifier off the critical path | L2 |
| C-003 | V1+V2 | 95% | Route and replicas as card data, 2 blind replicas | L2 |
| C-004 | V2+V3 | 90% | Ledger outside the findings block, real parser (`ledger-v1` JSON lines after INV-007) | L3 |
| C-005 | V1+V2+V3 | 75% | Substring check, demotion, tagged copy promotion (Round 2 Q4 unanimous); strict agreement missed only by set labels | L3 |
| C-006 | V1 | 80% | Cards render as question (A) or recipe (B) | L2 |
| C-007 | V2 | 85% | Grading rule unchanged (verified, merged-requirements.md:320) | L2 |
| C-008 | V2 | 80% | Serial pre-pass is the one specified mode (INV-012) | L3 |
| C-009 | V2 | 95% | +35% on medians with a hang guard, no kill at 1.35 x | L3 |
| C-010 | V2 | 75% | Per-package slowest-reviewer baseline used consistently; V1 equally consistent | L2 |
| C-011 | V2 | 95% | +0.14 (0.03-0.34) from the sourced table | L2 |
| C-012 | V1+V2 | 70% | Verified sums; recomputed from the consensus design (INV-006) | L2 |
| C-013 | V1+V2 | 70% | Planning values only, recomputed, with selection factor column | L2 |
| C-014 | V1+V2 | 95% | N-gram lint, freeze, swap test, second author | L2 |
| C-015 | V1+V2 | 95% | Real plans, spec, documentation arm, planted documents, clean twins | L2 |
| C-016 | V1+V2 | 95% | Checklist arm K, Z0-raw | L2 |
| C-017 | V2+V3 | 75% | Gates D1-D6, G5, G7, package-level bootstrap | L2 |
| C-018 | V1+V2 | 85% | Blocking needs grading sentence plus two quotes; clean-twin gate | L3 |
| C-019 | V2 | 80% | T2a/T2b and T3a/T3b splits | L2 |
| C-020 | V1+V2 | 90% | Data cards, V2 line counts, prototype before trusting | L2 |
| C-021 | V2 | 70% | Per-model item letters; slow-model caps | L2 |
| C-022 | none (no change) | 90% | All overheads are unmeasured estimates | L2 |
| C-023 | V1+V2+V3 | 95% | Union of failure rows | L2 |
| C-024 | V1+V2 | 80% | Block-kind list as re-derive checklist, no adapter code | L2 |
| X-001 | V2 | 98% | Source table: +0.14 (checked by the orchestrator) | L2 |
| X-002 | V2 | 98% | Rubric constant | L2 |
| X-003 | V2 | 90% | About 2 s per item for at most 12 items; V3's +18 s for 40+ items refuted | L2 |
| X-004 | V1/V2 (V3 refuted) | 90% | V3 recomputes to +22% (A) and +37.7% (B) on b = 122 | L2 |
| X-005 | V2 | 95% | Judge medians; no kill at 1.35 x | L3 |
| X-006 | V2 | 85% | V1 and V2 sums reconcile; V3's do not | L2 |
| X-007 | V2 | 85% | 39% overall (81 of 209); 36% was one package | L1 |
| X-008 | V2 | 90% | Design to the median with slack; no reliance on a kill | L2 |
| A-001 | V2 | 80% | Reach split into extraction, act, merge survival, judge credit | L3 |
| A-002 | V2 | 80% | Sums are planning bounds only | L2 |
| A-004 | V2+V3 | 85% | H3 precondition, snapshot hash, bounded search, fallback | L3 |
| A-006 | V1+V2 | 80% | Report found-any and found-blocking separately | L3 |

## Convergence Assessment
- Points resolved: 40 of 41 strictly (one more, C-005, resolved on content: all three accepted Q4 and INV-005)
- Alignment: 97.6% strict; 100% compatible
- Threshold: 75%
- Status: CONVERGED (taxonomy levels L1, L2, L3 all covered; invariant gate cleared by Round 3, 14 of 14 INV findings accepted or qualified with adopted resolutions)
- Unresolved points: none. Residual disagreements recorded: Q5 (V1 wanted a second ember session; V2 and V3 chose one session, 2 of 3); INV-005 and INV-002 wording (V1 vs V2 and V3; V2 and V3 chosen, 2 of 3)
