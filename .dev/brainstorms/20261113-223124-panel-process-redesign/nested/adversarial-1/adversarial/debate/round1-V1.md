# Round 1 statement: Variant 1 (sonnet:architect)

## Position

Finalize two genuinely different redesigns: A, a script-built Probe Sheet (V1 3.1, with V2's 12-item discipline and sheet-built-in-parallel option), and B, a prompt-only Recipe/Lens Ledger (V1 3.2 merged with V2's Redesign 2). Both draw their content from one class registry (V1 3.0). V3's pair is not distinct, and its time arithmetic does not hold.

## Steelman of Variant 2

V2 has the best evidence discipline. It takes the harness-fix gain from the first brainstorm's own bottom-up table (+0.14, range 0.03-0.34), which I checked at merged-requirements.md:342-350. It keeps the grading rule unchanged (line 320), so a rubric edit never mixes with a design effect. It rejects a kill at 1.35 x median, because run-to-run spread would discard 25-40% of reports. It adds planted-defect documents with clean twins, a placebo arm and a Z0-raw arm, which measure recall and false positives on unseen text. Its option to build the sheet while reviewers do their first reads takes the pre-pass off the critical path. I verified its matrix sums (1.63-3.55; totals 3.2-5.7).

## Steelman of Variant 3

V3 is the simplest to build (about 240 lines). Its blind verifier, which sees only the claim and the evidence, targets the real risk of forced items, false-positive growth. The research note reports 94-98% false-alarm removal for a tool-plus-model hybrid. It also has good operations hygiene: a real parser for the coverage block (closing the fence-opener-only BLOCK_OK gap), byte-identical determinism tests, a logged shuffle seed, and a bootstrap that resamples packages rather than runs.

## Strengths claimed

1. **Class registry as the generality unit (3.0).** One card holds the definition, the recipe, the question template, the extractor, the route and the instances. Redesign A renders the question; Redesign B renders the recipe; a new class is one card (REQ-09). V2 and V3 hard-code class logic in scripts.
2. **Routing follows measured model habits.** Each card carries `route` and `replicas`. Luna "almost never searches" (seed), so it gets read items and ember gets search items (3.1(b)). V3 broadcasts all 60 items to both lunas (3.1(b)), including items that need repository searches.
3. **Controls that test the right claim.** A4 is a one-paragraph generic checklist with gate G5 ("gain over A4 of 4 or more points, otherwise A4 wins"). This tests the external finding that a checklist is no better than ad hoc reading. V2's placebo P (class names only) is weaker. V3 has no control.
4. **Mechanical answer checks.** The quote-substring check demotes unsupported PROBLEM rows and promotes unreported ones to MINOR (REQ-16/17/31). Its telemetry keys give a per-class yield table.
5. **Consistent arithmetic.** I recomputed every row: A is 6+122+12 = 140 (+14.8%); the worst case is 12+122+30 = 164 (+34.4%). The matrix sums reconcile (1.70-3.70 and 1.05-3.10), and totals 3.4-6.1 and 2.8-5.5 follow.
6. **Documentation arm and spec hold-out (G7)** test generality beyond plans. The breadth claim is withdrawn if they fail.

## Weaknesses identified in Variants 2 and 3

1. **V3's baseline is inconsistent (X-004).** On its own b = 122, A = 6+122+18+3 = 149 (+22%, not +6%). B = 6+132+2+25+3 = 168 s (+37.7%), above its own 165 s ceiling; on b = 100, B is +46%. I verified this.
2. **V3's per-item cost is too low (X-003, A-009).** 40-60 coverage lines of JSON with an evidence field are about 1.4-3.6k tokens, or 29-75 s at 48 tokens/s, not +18 s.
3. **V3's arithmetic does not close (X-006).** Matrix A sums to 3.50-6.05 against the stated 3.6-6.6; B sums to 3.40-5.95 against 3.3-6.2. I verified both.
4. **V3's two redesigns are not distinct.** Both use the same helper. B only adds a verifier, which sits on the critical path. Neither tests the seed's open question of whether a prompt-only change can do the job.
5. **V3's validation is thin.** It has three packages and no spec or doc target (C-015), no placebo or checklist control (C-016), and labels matrix rows GT1.. so they cannot be mapped to the ten issues.
6. **V2 has quota-fixed sheets.** Its caps (Q2, U2, M2, R2, S2, K1, X1) crowd out real items with no stated ranking. Its extractors have no schema, so each new target means re-writing the script (C-024).
7. **V2's panel deadline is 1.6 x baseline**, which is +60% by construction. Only the median meets +35%.

## Concessions

- X-001: my +0.2 to +0.7 for H1-H4 is an unsupported guess. Use +0.03 to +0.34 until Z0-raw measures it.
- X-002: CB2 rewrites the grading rule, so it must not be mixed into the control. It should run as a separate arm.
- X-005 and X-008: kill at D loses reports, and my worst case (+36%, or +42% at b = 100) relies on it. Replace it with a median-based judgement plus a 1.5 x hang guard.
- My scaffolding is the heaviest (about 1,300-1,500 lines), and the experiment (over 260 runs) is costly. The registry should ship as data cards with flat extractors, with no adapter classes before a second target exists.
- The upper totals (6.1) exceed the best run ever seen (4/14), and B has no issue at "consistent".

## Shared assumptions

- A-001: QUALIFY. Split reach into trigger x act-rate x merge survival x judge credit, and replace the planning probabilities with the measured act rate (V2 U-015).
- A-002: QUALIFY. Probabilities are not additive; cap the claim at a stated prior, subtract displacement, and report measured totals only.
- A-003: QUALIFY. H and redesign gains overlap; report them as separate shares from arms A0, A1 and design, never summed in a headline.
- A-004: QUALIFY. This is an unproven precondition; run a timing spike, restrict greps to tests, root documents and named paths, and fall back to the isolated brief.
- A-005: QUALIFY. Compliance is the central risk of B, so measure it (quote check, tool-call cross-check) rather than assume it.
- A-006: QUALIFY. The study credits non-blocking finds, but the loop verdict needs blocking; report found-any and found-blocking separately.
- A-007: ACCEPT. Medians are stable enough if arms run in randomised blocks (V2).
- A-008: QUALIFY. The classes recur in one repository only; C1 and C3 are weak, so claim breadth per target type, and only after hold-out and planted-document results.
- A-009: REJECT. 2 s per item holds only for short rows and about 12 or fewer items; 40-60 items cost 29-75 s.

## Position table

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
