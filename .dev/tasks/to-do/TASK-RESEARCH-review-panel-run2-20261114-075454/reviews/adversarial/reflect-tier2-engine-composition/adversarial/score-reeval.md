# Position-bias re-evaluation, step 3, slot C-04 (reflect-tier2-engine-composition)

Re-evaluator inputs: `score-pass1.md`, `score-pass2.md`, `variant-1-original.md` (Proposal A), `variant-2-original.md` (Proposal B), `diff-analysis.md`, `debate-transcript.md`. Each variant is judged as its original text stands; the debate is used only as evidence about correctness and gaps. Quoted lines were re-read in the variant files in this session. One external check: `pyproject.toml:78-83` (wheel `packages = ["src/superclaude"]`, `include = ["src/**", "plugins/**"]`) confirms `scripts/` is not shipped, and `scripts/reflect_shadow_exit.py:117` defines `recompute_parity`.

Comparison prompt used for every pair: "Two independent evaluations disagree on this criterion for this variant. Pass 1 evidence and verdict: ... Pass 2 evidence and verdict: ... Re-evaluate with both pieces of evidence. Your verdict is FINAL."

---

PAIR: K2 | Variant 2

PASS 1 EVIDENCE/VERDICT: NOT MET. The serializer is placed in kernel `cli/review/*` and "allows only the frozen key list", but that list lives in `cli/reflect/panel_lint.py`. The step-2 parity helper cannot be built because `recompute_parity` is in `scripts/`, not packaged, and needs the finished contract. M4 is vacuous because engine A reviews the tasklist body only. Line 99 leaves engine A at contract 1.0 against decided CV-4.

PASS 2 EVIDENCE/VERDICT: MET. The central approach (additive helper subcommands, engine A untouched, 36-test matrix untouched) is feasible. The placement "with a lazy import of the `panel_lint` constants survived into both Round 2 hybrids". Only the step-2 parity helper is infeasible, and B dropped it in Round 2.

RE-EVALUATION: Pass 2's feasibility evidence is the Round 2 repair (a lazy import that appears in no part of the original), and the rubric asks about the document as it stands. As it stands, the helper design is the substance of Position B, and it fails its own stated constraints. Line 36 puts the writers in `cli/review/*`: "a contract serializer that quotes `[` and `]` in model aliases and allows only the frozen key list, and a parity record computed by code (`reflect_shadow_exit.recompute_parity`, r06 s6.2). Reuse, not new logic." The frozen lists are in `cli/reflect/panel_lint.py` and line 18 says `cli/reflect` has no import edge to `cli/review`, so the document gives the serializer no source for its key list. `recompute_parity` is in `scripts/reflect_shadow_exit.py:117`, outside the wheel (`pyproject.toml:79-83`), so an installed `superclaude review` subcommand cannot reuse it. The same row builds the `merged-verdict.yaml` finalizer "on the extraction functions that already exist (`ensemble.py:633-697`)", which cover 1 of 6 fields (diff-analysis V-29), while line 129 promises "the only importer of swarm stays `cli/reflect/ensemble.py`" and that no edge is added between `cli/review` and `cli/swarm`. M4 (line 122) sends "the same seeded-regression tasklist plus diff" through an engine whose reviewers see only the tasklist body (E6, line 60), so its false-PASS reading cannot test what it claims. The headline direction (do less, reconcile at the contract) is workable, but the one concrete build it specifies has no home, an unpackaged dependency and an unbacked reuse claim. Pass 1's evidence is specific and is in the text; Pass 2's rests on a post-document repair. NOT MET.

FINAL VERDICT: NOT MET

---

PAIR: K5 | Variant 1

PASS 1 EVIDENCE/VERDICT: MET. Section 4.1 pairs each claim with a file:line and a `[CODE-VERIFIED]` or `[UNVERIFIED]` tag (lines 96-105); section 3.2 pairs each shadow step with its failure and the code to reuse (lines 62-69). Overstatements are a K1 matter.

PASS 2 EVIDENCE/VERDICT: NOT MET. The central claim in section 8 answer 1 rests on E7, whose loss analysis is `[UNVERIFIED]`; section 4.3 says "A is an analysis, not an observation"; E1 conflicts with section 3.4.

RE-EVALUATION: K5 asks whether claims are supported by evidence or rationale within the document, not whether the support is correct (K1) or consistent (K4, K2). V1 gives a rationale for its central claim: E7 (line 104) lists what each retirement loses, cites the research source, labels it as "an analysis for the synthesizer, not a verified fact", and tags "existence of the lanes [CODE-VERIFIED]". Line 113 states the limit itself: "No run has used a code-written contract, card or `merged-verdict.yaml`. A is an analysis, not an observation". A claim that is argued and honestly labelled as unverified is supported by rationale within the document. Pass 2 treats a disclosed evidence gap and an E1/section 3.4 tension as missing support; the first is a disclosure, the second is already charged to K1, K2 and K4. Every row of the 4.1 table carries a citation and a tag. MET.

FINAL VERDICT: MET

---

PAIR: L4 | Variant 1

PASS 1 EVIDENCE/VERDICT: NOT MET. INV-A..INV-N are defined only by pointer to "s06 section 6.12.0" (line 14); EV-1 first appears at line 66 with no definition; EV-2 and `UC` are not defined; GQ-067 is only partly glossed.

PASS 2 EVIDENCE/VERDICT: MET. Section 0 defines the tags and the `r06`/`r07`/`s05`/`s06` shorthand and glosses the decided rows (CV-1, CV-2, RE-2, RE-3, CV-6, CV-9, RX-15). Residual: EV-1 undefined.

RE-EVALUATION: Grep of the variant shows `EV-1` on lines 66, 67, 109, 139, 140 and 161 and no definition on any line. EV-1 is the exit-script check that measurement M2, M3 and the section 8 answer 1 depend on ("EV-1 fails in 8 of 13 counted pilot runs", line 67), so it is a load-bearing domain term, not a stray one. Line 14 defines the invariants only as "the invariants of `s06` section 6.12.0", a pointer to another file. The inline glosses on line 15 are real, but the rubric requires terms to be defined on first use, and a core term used six times is not. Pass 2 itself records the EV-1 gap and still scored MET, which is not consistent with a binary rule that requires MET only on a specific supporting citation. NOT MET.

FINAL VERDICT: NOT MET

---

PAIR: L4 | Variant 2

PASS 1 EVIDENCE/VERDICT: NOT MET. "T5 gate" (line 42) is never defined; EV-1 and EV-2 (lines 71, 80) have no definition; OQ-8, OQ-20 and GQ-067 are partly glossed; INV-A..INV-N are defined only by pointer (line 95).

PASS 2 EVIDENCE/VERDICT: MET. Section 1(i) glosses CV-1, CV-2, CV-3, CV-5, CV-6, CV-8 and CV-9; line 10 defines the tags; E2 and E3 gloss UC-2 and UC-1. Residual: EV-1 and "T5" never defined.

RE-EVALUATION: Grep shows `EV-1` on lines 80, 119 and `EV-2` on lines 34 and 71 with no definition (line 71 only says the skill "requires a disk-confirmed merge", which describes EV-2 after its first use at line 34). `T5` first appears on line 42 ("the production T5 gate keeps `--fix` structurally dormant") and is glossed only at line 53 ("the wrapper's UC-2 gate (tasklist T5)"), so it is not defined on first use. Line 95 defines the invariants by pointer ("Definitions are synth-06 6.12.0"). The inline UC-1/UC-2 and CV glosses are credited, and V2 glosses slightly more than V1, but the same load-bearing term (EV-1, the basis of M1's gate rule on line 119) is undefined here too. The same standard applies as for Variant 1; Pass 2's own "Residual" line concedes the failing terms. NOT MET.

FINAL VERDICT: NOT MET

---

PAIR: R2 | Variant 1

PASS 1 EVIDENCE/VERDICT: MET. INV-L: comparison artifact until M2 passes (line 132); INV-A: settle the conflict first (line 121); INV-B: M1 pins, "each rewritten pin is named with the reason" (line 138); headless constants moved "into one place where a lint can see it" (line 83); cost items answered in section 8 answer 2.

PASS 2 EVIDENCE/VERDICT: NOT MET. INV-B has "no mitigation" (which pins fix a slug is `[UNVERIFIED]`), and the headless-PASS risk is "only moved into one place where a lint can see it".

RE-EVALUATION: The risks V1 rates (line 132 INV-L "Endangered, HIGH"; line 121 INV-A "Endangered, MEDIUM, until then"; line 122 INV-B "Endangered, MEDIUM") each carry a stated handling rule. INV-L: "admissible only if a code-built contract is shown value-equal ... on the recorded runs (section 6, measurement M2) before it is authoritative; until then it is a comparison artifact under `panel/`." INV-A: "the `reviewer_briefs_materialized` conflict (3.5) must be settled first". INV-B: M1 (line 138) requires the engine-A pins to "pass, or each rewritten pin is named with the reason"; that is a procedure (rewrite and record), and the slug change is stated as accepted with the exit code held at 11. Pass 2 is right that the `[UNVERIFIED]` pin list leaves the INV-B scope unknown, but a strategy exists for it. The headless-PASS limit (line 83) is the weakest item: V1 says "A does not make a headless PASS mean 'no deviation found'. It moves that claim into one place where a lint can see it", which is partial mitigation by visibility and an explicit decline to decide eligibility; that is an acknowledged residual, not an absent strategy. The rubric asks for a mitigation strategy for each identified risk, and V1 supplies one for every risk it rates plus partial handling for the residual. Contrast Variant 2, where items 2, 3 and 4 of its risk list have no strategy at all (lines 109-111: "documents instead of removing", "needed, not resolved"). MET.

FINAL VERDICT: MET

---

PAIR: R3 | Variant 2

PASS 1 EVIDENCE/VERDICT: MET. Line 101: serializer output checked by `scripts/reflect_verdict_replay.py` before it replaces the draft; lines 119 and 143: if M1 fails because a helper was skipped, "the evidence favours a code-driven parent"; line 121: each M3 outcome closes a reading.

PASS 2 EVIDENCE/VERDICT: NOT MET. The M1 line states a consequence, not a recovery; only INV-L has a guard.

RE-EVALUATION: The criterion asks that the document address failure modes and recovery procedures, not a recovery for each failure (that is R2's "each" wording). V2 names failure modes (a serializer bug, a skipped helper, a restricted child that cannot spawn agents, a production PASS without a deviation audit) and gives at least two recovery or fallback procedures in the text. (1) Line 101: "Position B holds INV-L only if the serializer output is checked against the orchestrator's own draft by the existing verdict replay (`scripts/reflect_verdict_replay.py`, r06 s7) before it replaces the draft"; failing the check leaves the draft in place. (2) Line 124: "Position B names retirement of engine A's reviewer path (Option 3) as its direction when either (a) the owner answers ... or (b) M4 shows engine A's PASS is unsafe on seeded regressions", a defined fallback path with a trigger. M3 (line 121) also states what each probe outcome means for the design. Pass 2 is right that the skipped-helper branch (lines 119, 143) states a consequence without a remedy, and that V2's recovery is thin compared with V1's fail-closed BLOCKED rule; that thinness is already charged under R2. Presence of failure modes plus at least one concrete recovery procedure meets the criterion. MET.

FINAL VERDICT: MET

---

PAIR: I1 | Variant 2

PASS 1 EVIDENCE/VERDICT: NOT MET. No treatment of one-reviewer, empty-reviewer or maximum-reviewer cases; line 71 quotes `reviewer_count >= 2` only as evidence that the label is count-derived; reviewer-count limits ([2,4] versus 3) are not mentioned; the 20-run counts are measurement sizes.

PASS 2 EVIDENCE/VERDICT: MET. Section 1(i) and the exit-script row: "CV-9 an empty baseline is 'no baseline'", fix at `scripts/reflect_shadow_exit.py:313`; E12 `ensemble.py:773` "reviewer_count >= 2". The [2,4] versus 3 clamp is not treated.

RE-EVALUATION: Pass 1 does not cite the CV-9 item. The text carries it twice: line 24 "(CV-9 an empty baseline is "no baseline")" and line 37 "`scripts/reflect_shadow_exit.py` | Fix at `:313` (empty baseline is "no baseline"), decided by CV-9", and M1 (line 119) uses "the exit script ... with the `:313` baseline fix". The legacy baseline is a collection of runs, and the empty case is the textbook empty-collection boundary; the design assigns it a code location and a defined outcome. E12 (line 71) also states the single-versus-multiple reviewer boundary of the label (`"adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"`), though only as evidence. The rubric requires boundary conditions for collections (empty, single, maximum) and a specific citation, and the empty case has one. V2 still misses the reviewer-count maximum (the [2,4] clamp against the kernel cap of 3, V-26), which is a real gap and is charged to I4; one concretely handled boundary meets the criterion as worded. MET.

FINAL VERDICT: MET

---

PAIR: I4 | Variant 1

PASS 1 EVIDENCE/VERDICT: NOT MET. V1 distinguishes run populations (13 counted, 28 recorded, 13 of 20 required) but does not check count rules across the combined engines: line 55 cites "at most 3 reviewers" for the kernel while keeping the headless lane whose runner clamps `--reviewers` to [2,4] (V-26); "110 stable plus 27 telemetry" is carried as 137 although one name is in both tuples (V-05, INV-008).

PASS 2 EVIDENCE/VERDICT: MET. Counts are reconciled by execution (13 of 20 required, 8/13 = 0.615 versus 3/39 = 0.077, 36 test functions by `grep -c`, 32 keys counted, `reviewer_briefs_materialized` on three ref lines :51, :57, :78), INV-B names the trigger order `:295` before `:299`. Residual: "19 fields" tagged `[UNVERIFIED]` (18 by the debate); [2,4] versus 3 missed.

RE-EVALUATION: Both passes agree on the miss: V1 keeps engine A's runner and the kernel reflect profile ("at most 3 reviewers at `panel.py:71-73`", line 55) without relating them to engine A's [2,4] clamp. That is the one range divergence the composition itself creates, and it is not surfaced. Against that, V1 contains specific count-divergence work. Line 122 traces a count-derived label against a disk-confirmed one: "when the headless lane has two or more reviewers and the adversarial child fails, `merge_method` today is `adversarial` (`ensemble.py:773`), so the reason is `null-convergence` (`contract.py:299`); with a disk-confirmed `merge_method` (3.5) it is `single-reviewer-fallback` (`contract.py:295`, which comes first)". M4 (line 141) pins the single-reviewer boundary ("A one-reviewer stub run still yields `single-reviewer-fallback` and exit 11"). Line 109 reconciles run counts by execution ("13 of 20 required", "8/13 = 0.615; legacy baseline 3/39 = 0.077"), and the `reviewer_briefs_materialized` lines are correctly given as `:51, :57, :78` (line 89). The 137 versus 136 overlap is not stated in V1 (it gives 110 and 27 separately, line 19), so it is not a document error. The rubric asks for count-divergence scenarios, and V1 supplies a verdict-affecting threshold divergence plus reconciled counts, with one cited miss. Variant 2 differs because it asserts counts that are wrong in the document (two stale comments, `reviewer_briefs_materialized` on one line, "the only importer of swarm") and treats the count-derived label as harmless. MET.

FINAL VERDICT: MET

---

## Final Verdicts

| Criterion | Variant | Final | Changed vs Pass 1 | Changed vs Pass 2 |
|---|---|---|---|---|
| K2 | Variant 2 | NOT MET | No | Yes |
| K5 | Variant 1 | MET | No | Yes |
| L4 | Variant 1 | NOT MET | No | Yes |
| L4 | Variant 2 | NOT MET | No | Yes |
| R2 | Variant 1 | MET | No | Yes |
| R3 | Variant 2 | MET | No | Yes |
| I1 | Variant 2 | MET | Yes | No |
| I4 | Variant 1 | MET | Yes | No |
