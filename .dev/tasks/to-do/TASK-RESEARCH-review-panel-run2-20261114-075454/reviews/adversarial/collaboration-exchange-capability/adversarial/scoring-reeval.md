# Position-bias re-evaluation (scoring-protocol A.5), slot C-12 collaboration-exchange-capability

Re-evaluator. Inputs read: `scoring-pass1.md` (order A, B), `scoring-pass2.md` (order B, A), `variant-1-original.md` (Variant A = Proposal A), `variant-2-original.md` (Variant B = Proposal B). The debate transcript was not needed: each verdict below rests on the original text of the two variants, and no Round 2 concession is credited. This verdict is final. MET = 1, NOT MET = 0, and a MET needs a specific citation.

## Standards applied to both variants (one bar each)

| Criterion | Bar used for both variants |
|---|---|
| Correctness 2 (feasible with stated constraints) | NOT MET when the design, read as a whole, cannot be implemented without breaking a constraint the variant itself states (or a verified repo constraint), and no other statement in the same variant resolves it. MET when the whole-design reading is implementable and the defect is one stray phrase that the variant's own mechanism sections already resolve. |
| Correctness 3 (terminology consistent and accurate) | NOT MET only when one label carries two incompatible referents (or two labels one referent) with no disambiguation at the point a reader must tell them apart. Factual slips and self-contradictions are scored under Correctness 1 and 4, not a second time here. |
| Clarity 1 (unambiguous language) | NOT MET when a rule, decision or pass/fail condition is stated with an unlabelled hedge ("might", "should consider", "as appropriate", "likely"). Quoted hedges, [UNVERIFIED]-labelled estimates, illustrative example names, and a parameter deferred to a named owner or slot do not count. |
| Risk Coverage 1 (at least 3 risks with probability and impact) | A risk counts only when the variant's own risk or invariant text gives BOTH an impact AND an explicit likelihood signal for that risk (a likelihood tag, or a measured frequency or magnitude tied to that risk). Conditional triggers ("if turned on") and definitional certainties do not count as a likelihood. Need 3. |
| Invariant and Edge Case 4 (count divergence) | MET when the variant shows a concrete case where two counts or limits for the same quantity disagree, or handles an off-by-one or inclusive/exclusive boundary, with a citation. |

## Pair 1: Variant A, Correctness 3

- Pass 1 (MET): "Unconditional" is disambiguated in section 1; tags and legend used uniformly.
- Pass 2 (NOT MET): "E2" means both the study and claim row E2 (6.1 "claim E2 in 4.1"); "matching control" shifts meaning between 4.2 and 4.3.
- CLAIM: A uses its terms consistently enough to meet the bar.
- EVIDENCE: Section 1 defines "Unconditional" as "not gated on an exchange decision", and sets H1 to H4, kit, catalogue and `exchange: off` once and keeps them (3.1 to 3.4, 5, 6). The one real label collision, row id "E2" against the E2 study, is disambiguated at the only place the row is cited as a row ("claim E2 in 4.1", 6.1). "Matching control" is used for the A2-over-A1 control in 4.2 and, read with 6.1 ("run A1, A2 and each exchange arm") and 8(3) ("exchange designs without A2 cannot be separated"), means the A2 row an exchange arm would need. The sentence "no exchange arm has a matching control row" is then a factual overstatement (already NOT MET under Correctness 1 and 4), not a second referent. "slot B" in 6.1 is a one-word slip for position B with an obvious meaning.
- VERDICT: MET.

## Pair 2: Variant A, Clarity 1

- Pass 1 (MET): hedge words appear only in quotes of `MR` or evidence caveats; decisions stated as rules (3.4, 6.2).
- Pass 2 (NOT MET): 6.2 "a cap the module owner states" has no number; 3.4 "first candidates for `on`".
- CLAIM: No unlabelled hedge sits in a rule or pass/fail condition.
- EVIDENCE: A contains none of "might", "should consider" or "as appropriate"; "may beat" is a quotation of `MR:917` (E1). The decision rules are determinate: 3.1 item 6 (any value other than `off` is refused at validation), 6.1 ("wrong if an exchange arm beats A2 by the margin E2's requirements set ... right if none does"), 6.4 (argv and brief bytes equal). 6.2 defers the cap value to a named owner, which is a deferral and not an ambiguous rule; 3.4's "candidates" is immediately bound by "subject to the cost measurement in section 6" and 6.2's `kit: on only if` rule.
- VERDICT: MET.

## Pair 3: Variant A, Risk Coverage 1

- Pass 1 (MET): five endangered rows with measured magnitudes in E6, E8, E9, 4.2.
- Pass 2 (NOT MET): section 5 lists four endangered items with mitigations but no probability assessment.
- CLAIM: A gives fewer than 3 risks with both likelihood and impact.
- EVIDENCE: Section 5 endangered table: (1) INV-G read-only has impact (a shell recipe would instruct a no-Bash reviewer, `reflect-reviewer.md:59`) and a severity tag (HIGH, preserved table), but no likelihood estimate; (2) INV-L/INV-A is conditional on "if the kit is turned on in reflect", with no likelihood; (3) INV-K states a layout item and no likelihood; (4) cost caps give a measured magnitude ("+59 percent elapsed (pinned, one package) and +10 to +35 percent"), the only row with both. The `k` 0 in 15 of 18 values, the `phase2_timeout` 1 rows and the hang row in section 4 are measured frequencies, but they are risks of the exchange alternative offered as evidence, not likelihoods A assigns to the risks of its own position. Counting generously, INV-G (tag plus "E2 recipes assume a shell") and cost give 2, not 3.
- VERDICT: NOT MET.

## Pair 4: Variant B, Correctness 2

- Pass 1 (NOT MET): 2.2 global registration conflicts with the inert off state; `--settings` appears nowhere in `src/superclaude/**/*.py`; shared H1/H2 carry the INV-005 and INV-009 issues.
- Pass 2 (MET): 2.3 and 2.4 put the new adapter outside the pinned `ClaudeProcess` (`process.py:149-152`); section 8 states the C-07 fallback.
- CLAIM: B's design, read as a whole, is implementable within its own stated constraints.
- EVIDENCE: The mechanism B actually specifies is one coherent path: a new adapter with persistence on and per-session `--settings`, whose baked arguments carry the installed path (2.2 second sentence, 2.3), an off state that "emits no `--settings`, no board directory and no second phase" (2.4), and no change to `cli/reflect`, the shared contract or the pinned argv (2.3, 2.5, 2.6, section 5). The 2.2 phrase "registered ... in `hooks.json`" would, taken alone, fire in every session. It is a stray phrase that 2.2's own next sentence and 2.4 resolve, so the design is implementable without breaking a stated constraint (the phrase is NOT MET under Correctness 1 and 4 and is not charged a third time here). `--settings` being absent from `src` today is new code to write, which is not infeasibility. Pass 1's INV-005 and INV-009 charge does not apply: B specifies no route for H1 or H2 into reflect (one sentence, "ship as well"), whereas A does (3.3, 3.1 item 2). The read-only launcher question and the C-07 dependency are disclosed ("UNVERIFIED", "B shrinks if C-07 yields no launcher"). Contrast with A: its claim "H1 through the reflect brief, no call-site change" is repeated by sections 2 and 5 ("no change to `cli/reflect`") with nothing that resolves it, so A fails the same bar.
- VERDICT: MET.

## Pair 5: Variant B, Correctness 3

- Pass 1 (NOT MET): "registered" in 2.2 against "baked into `--settings`"; "H1/H2" used without definition.
- Pass 2 (MET): exchange, switch, off state, F-family kinds and A1/A2 used the same way in sections 1, 2.4, 5, 6.
- CLAIM: B's terms are consistent under the same bar as A.
- EVIDENCE: "Exchange", "switch", "off state", "transport", "board", "seal", "sidecar" and the kinds F1, F3, F6 carry one referent each across sections 1, 2, 4, 5, 6 and 8 (for example 1 "its off state is a launch command that differs from the isolated panel by nothing" and 2.4, 6.1, 5 "while the switch is off"). The hooks.json versus `--settings` wording is a mechanism contradiction (scored under Correctness 4, NOT MET) and not one label with two referents. "H1/H2" undefined is a Clarity 4 matter (terms defined on first use), not consistency. The "A above"/"B above" cross-references in 3.C collide with position names in the same way as A's row id "E2" and "slot B", so the bar treats them alike and does not fail either variant.
- VERDICT: MET.

## Pair 6: Variant B, Clarity 1

- Pass 1 (MET): rules stated as decisions; hedges limited to labelled [UNVERIFIED] caveats.
- Pass 2 (NOT MET): 2.1 "for example `exchange/`"; 5 "would likely cost more ... [UNVERIFIED]".
- CLAIM: No unlabelled hedge sits in a rule or pass/fail condition.
- EVIDENCE: B contains none of "might", "should consider" or "as appropriate"; "may beat" is a quotation of `MR` (3.D). "For example `src/superclaude/cli/review/exchange/`" is an illustrative name, and the rule is stated in the same sentence (a name other than `lib/`, because `.gitignore:13` is `lib/`). "A Python hook entry point would likely cost more ... that cost is [UNVERIFIED]" is a labelled estimate, not a rule. The decisions are determinate: 2.4 and 6.1 (argv equals the same adapter without the exchange package), 6.2 (existing pins pass with no edit), 6.5 (p95 over at least 30 calls against 0.1 s), 6.7 ("fewer than half of the cells").
- VERDICT: MET.

## Pair 7: Variant B, Risk Coverage 1

- Pass 1 (MET): five endangered rows, `k` 0 and delivered 0 as likelihood, the 6.7 "fewer than half" rule.
- Pass 2 (NOT MET): section 5 lists six endangered items with impact text but no probability assessment.
- CLAIM: B gives fewer than 3 risks with both likelihood and impact.
- EVIDENCE: Section 5 endangered list: (1) blindness relaxation is definitional when the switch is on, so no likelihood; (2) read-only Bash launcher has impact, and "the exchange can only run there" is a certainty, not a likelihood, with the mitigation passed to C-07; (3) untrusted anchors have impact (attacker-controlled diff text) and "B does not claim it is closed", with no likelihood; (4) INV-H has impact only; (5) the persistence pins are avoided by design; (6) time budget has a measured magnitude ("about 60 to 100 ms per tool call in the recorded spikes" against 0.1 s), with the Python-entry estimate labelled UNVERIFIED. Outside section 5, 6.7 and 3.F give the wasted-spend risk a likelihood signal (`k` 0 in all six EL2 and HL2 cells, "the post-baseline r2 smoke and the `k = 0` cells already point that way") and an impact (B's claim (3) "wrong about use"). Time budget plus wasted spend gives 2, not 3, under the same bar as A.
- VERDICT: NOT MET.

## Pair 8: Variant B, Invariant and Edge Case 4

- Pass 1 (MET): "36 `def test_` functions and no parametrize" checked against the C-03 figure; `flock -w 4` against untimed `flock 9`; 0 against later `/lib/` counts.
- Pass 2 (NOT MET): 3.E checks the 36-test count only; no off-by-one case; the 600-byte boundary is untested.
- CLAIM: B shows a concrete count divergence with citation, the same bar as A's test-count divergence (103, 163, 89, 90, 82 against 138, 358, 89, 106, 108) and its 201/301 pins.
- EVIDENCE: Section 0 and 3.F record the same quantity at two states and reconcile it: `/lib/` path counts 0 for r1 to r5 at the pinned tip against r3 3, r4 7, r5 11 (r2 0, r1 0 by design) at `c44c98a77`. Section 2.1 turns that divergence into a design rule (no `lib/` folder, because `.gitignore:13` makes files present on disk silently untracked, "the same loss that hit E2"). Section 3.E states "36 `def test_` functions and no `parametrize`" and ties it to the C-03 count of 36, which fixes the function count against the collected-case count (the mechanism by which a count would diverge). Section 3.F also reports the four hook scripts' line counts (72, 138, 120, 101) as unchanged between commits. B has no 600-byte boundary test, so it is weaker than A on the inclusive/exclusive limb, but the bar asks for a concrete count divergence with a citation, and the `/lib/` case is one.
- VERDICT: MET.

## Summary of final verdicts

| Pair | Pass 1 | Pass 2 | Final |
|---|---|---|---|
| 1. A, Correctness 3 | MET | NOT MET | MET |
| 2. A, Clarity 1 | MET | NOT MET | MET |
| 3. A, Risk Coverage 1 | MET | NOT MET | NOT MET |
| 4. B, Correctness 2 | NOT MET | MET | MET |
| 5. B, Correctness 3 | NOT MET | MET | MET |
| 6. B, Clarity 1 | MET | NOT MET | MET |
| 7. B, Risk Coverage 1 | MET | NOT MET | NOT MET |
| 8. B, Invariant and Edge Case 4 | MET | NOT MET | MET |

Net effect on qualitative subtotals (agreed cells unchanged): Variant A pass-1 cells A_C3 M (kept), A_L1 M (kept), A_R1 N (was M in pass 1); Variant B pass-1 cells B_C2 M (was N), B_C3 M (was N), B_L1 M (kept), B_R1 N (was M), B_I4 M (kept). The lead recomputes the combined scores from the undisputed cells of both passes plus these finals.

RESULT_REEVAL: A_C3=M A_L1=M A_R1=N B_C2=M B_C3=M B_L1=M B_R1=N B_I4=M
