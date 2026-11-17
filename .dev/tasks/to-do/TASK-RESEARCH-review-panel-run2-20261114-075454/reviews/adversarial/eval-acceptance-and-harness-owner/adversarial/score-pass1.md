# Scorer Pass 1 (A then B): slot X-14 `eval-acceptance-and-harness-owner`

Pass: 1 of 2 (input order: Variant A first, then Variant B). Scorer is neutral. `score-pass2.md` was not read.
Scope: the two ORIGINAL variants as written (`variant-1-original.md` = Variant A = Proposal A, `variant-2-original.md` = Variant B = Proposal B), not the hybrid the debate converged on. Debate material (`diff-analysis.md`, `round1-advocate-A/B.md`, `round2-advocate-A/B.md`, `invariant-probe.md`) is used only as evidence of which claims in a variant were verified, conceded or found false. Content that exists only in an advocate statement earns no credit.
Protocol: `refs/scoring-protocol.md` A.1 to A.3 and SKILL.md lines 1596-1862.
Evidence staleness: nothing in this pass depends on `c44c98a77` (`[POST-BASELINE]`); the variants' own `[POST-BASELINE]` items (A P-1..P-5, B E12) were not credited as decisive for any criterion. Forbidden paths were not read.
Citation form below: `A:n` / `B:n` = line n of `variant-1-original.md` / `variant-2-original.md`.

## 1. Quantitative layer (50%)

Script: `ADV/quant-score.py` (stdlib only, `uv run python quant-score.py`). Output: `ADV/quant-score-output.json`.
Determinism: the script was run twice; `sha256sum quant-score-output.json` printed `ec0fbb9cd858d07ef1eb8393c33f372e9c11b75cb22b331c942c2c000fc5617f` both times (identical).

### 1.1 Rules (as documented at the top of the script)

1. RC: 12 source requirements R1..R12 extracted from the X-14 row (`undecidable-conflicts.md` line 31) and the proposal structure it asks for. The 14 items in the scorer brief were merged to 12 (verify-run placement + design consequence for the shared core and named modules = R3; test or measurement + verification-tagged evidence = R10). A requirement counts as matched when all regexes of its list match (case-insensitive, whole file). Mention-level matching, per the protocol's grep rule.
   - R1 acceptance model/tiers; R2 metric of record (+ wrong blockers); R3 `verify-run` placement/ownership + design consequence (shared core, named modules); R4 judge and ground-truth registry owner; R5 harness placement (`.dev/` vs `scripts/`); R6 INV-F; R7 INV-H; R8 INV-K; R9 PR review and rf-qa effect; R10 "right if / wrong if" test or measurement + `[CODE-VERIFIED]`/`[UNVERIFIED]` tags; R11 consistency with C-01, C-02, C-03; R12 strongest objection and answer.
2. IC = 1 - contradictions / scorable claims. Contradictions are intra-variant ones found by reading (listed in 1.3); debate-found false claims are NOT counted here. Scorable claims = sentences (headings, metadata lines, table separators and sentences under 4 words excluded) containing a digit, a file path, a line reference or a verification tag.
3. SR = concrete / (concrete + vague) over the same sentence set; concrete = digit, backticked span, `INV-<letter>`, path, tag; vague = the protocol's vague list as regex.
4. DC = resolved internal references / total: `Section N` (resolves to an H2 numbered N), `E-n`/`En`, `M-n`/`Mn`, `P-n` (resolve to item lines), `INV-X` letter ids (resolve inside the variant's Invariants H2). Numeric ids such as `INV-003` belong to other documents and are excluded. Known limitation: study names E1/E2 also match the `En` pattern in both variants and resolve against same-numbered items.
5. SC = H2 count / max H2 count.

### 1.2 Results

| Metric | Weight | Variant A | Variant B | Computation detail (A / B) |
|---|---|---|---|---|
| RC | 0.30 | 1.0000 | 1.0000 | 12 of 12 / 12 of 12 requirements matched |
| IC | 0.25 | 0.9921 | 0.9815 | 1 contradiction in 126 scorable claims / 2 in 108 |
| SR | 0.15 | 1.0000 | 1.0000 | concrete 126, vague 0 / concrete 108, vague 0 |
| DC | 0.15 | 1.0000 | 1.0000 | 54 of 54 references resolved / 64 of 64 |
| SC | 0.15 | 1.0000 | 0.8889 | 9 H2 / 8 H2 (max 9) |
| **quant_score** | | **0.9980** | **0.9787** | |

Note for the reader: RC, SR and DC saturate at 1.0 for both variants, so the quantitative layer separates them only through IC (one more contradiction in B) and SC (one more H2 in A). Both proposals follow the structure the row asks for, which is why mention-level RC cannot discriminate. The qualitative layer carries the discrimination.

### 1.3 Intra-variant contradictions counted in IC (quotes)

Variant A (1):
- A-IC-1 (low severity): A:15 "Nothing below disagrees with a recorded outcome." and A:30 "Two ledger-entry additions, both additive" against A:106 "the C-01 outcome made unknown keys open in the parsers, and says ledger passthrough keys were deferred". The design adds ledger-entry keys while recording that the adjudicated slot deferred ledger passthrough keys; the document flags the open question as `[UNVERIFIED]` but still states no disagreement.

Variant B (2):
- B-IC-1: B:13 "Real-blocking, judge-blocking and wrong-blocker counts are reported as descriptive columns, not gates" against the gate B:13 itself defines, "with the control package's wrong-blocker ceiling that the same rule carries" (a wrong-blocker count that gates). B:15 (reading note) discloses the ceiling as "the one place where this proposal adds to the row text" but does not reconcile the two sentences.
- B-IC-2: B:47 (E6) "A blocking-row metric over the 8 blocking items has a smaller denominator than the 14 defect-rich items and the same three easy catches inside it" against B:94 "Presence.txt does not say which of the three easy items are blocking in implement, so I make no claim about that split". E6 asserts what answer 2 disclaims. (Both advocates later found that designSpec GT7 is `blocking_in_implement: false`, so E6's claim is also false; that fact is scored under Correctness, not here.)

Tensions read but not counted: A E-10 "silent swap" versus the launcher's logged `FALLBACK` (a factual error, scored under Correctness); B E8 "89 test files" versus its own Limits sentence (B:51 states the `lib/` ignore and the testpaths limit, so no contradiction).

## 2. Qualitative layer (50%): additive binary rubric, Claim-Evidence-Verdict

Rule applied: MET only with a specific quote or line reference; otherwise NOT MET; no partial credit. Facts found false or conceded false in the debate (diff analysis "Claims found false" list, Round 2 concessions) count against Correctness for the variant that made them.

Claims found false, inaccurate or conceded (used in the Correctness tables):
- Variant A: (a) E-10 "a silent swap passes `model_ok`" (A:65): the swap is logged to `$RID.fallback.log` (`run-reviewer.sh:75`) [CODE-CONTRADICTED for "silent"; conceded in A Round 2 W2]. (b) Section 3 item 3 (A:30): "the per-reviewer counts ... that `parse_block` already returns": `parse_block` returns `ok, findings, priors, errors` and no raw, kept or rejected count [CODE-CONTRADICTED for the counts; conceded in A Round 2 W1]; `ledger.py:131-134` "stores only the first error message" is a returned warning (`ledger.py:296`), not an entry field. (c) E-10 "The product kernel has no served-model field" (A:65): true for the four files searched, contradicted beyond them by `review/telemetry.py:49,364,378` and `sc-reflect-protocol/SKILL.md:341` (diff analysis A-005). (d) The ownership premise "the checks every consumer needs at run time" (A:11) has no existing in-run consumer; A Round 2 withdrew the kernel command and the ledger-entry additions on this ground.
- Variant B: (a) E8 and answer 3 (B:51, B:95): "the later harness carries 89 test files ... so the failure class is fixable in place": 28 of the 89 belong to designs 4 and 5 whose `lib/` code is absent from git at the tip, and design 2's sha-pinned judge wrapper keeps the weak `rc` plus `jq -e .` completion test (diff analysis C-012, X-006; conceded in B Round 2 B-W3). (b) E9 (B:53) "The manifest cannot hold `model_observed`" and the served-model gap, taken from research/15:106 [UNVERIFIED]: contradicted beyond the files searched by `review/telemetry.py:49` (diff analysis A-005). (c) E6 (B:47) "the same three easy catches inside it": GT7 is `blocking_in_implement: false` (conceded by both advocates in Round 2). (d) Its gate, the E2 any-severity rule with the control ceiling, passes arm C on a one-item margin that did not block in implement, with control wrong blockers 0, 0, 0 so the ceiling adds nothing (conceded in B Round 2 B-W1, B-W2).

### Completeness (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|---|---|---|---|---|
| C1. Covers all explicit requirements from source input | MET | A:11 acceptance tiers, metric of record, `verify-run` ownership, judge/registry owner, `scripts/` placement; A:96-109 INV-F/H/K; A:123-130 PR review and rf-qa; A:19-21 C-01..C-03; A:132-136 objection. Quant RC 12/12. | MET | B:13 structural gates plus E2 any-severity metric, harness under `.dev/`, no `verify-run`; B:17-21 C-01..C-03; B:63-71 INV-F/H/K; B:81-86 PR review and rf-qa; B:88-97 objection. Quant RC 12/12. B answers the registry-owner question explicitly (B:85 "there is no shared ground-truth registry and no shared verifier"). |
| C2. Addresses edge cases and failure scenarios | MET | A:115 M-2 injected-fault fixtures "an id collision on a 12-character prefix (E-8); a judge that dies and leaves a plausible `score.json` (E-9); a fallback that overwrites the expected model (E-10) ... a batch outside the manifest (E-11)". | MET | B:75 M1 "`fullpkg('TASK-WF-design-20261108-041415')` must return the control package ... a judge run with `score.json` missing ... must be reported as incomplete ... a run absent from the manifest must print as 'unaudited'". |
| C3. Includes dependencies and prerequisites | MET | A:19-21 a DEPENDS clause per adjudicated slot (C-01 INV-003; C-02 INV-001, INV-002; C-03 INV-007, INV-001); A:147 "until slot C-08 records". | MET | B:18 "It depends on C-01's shared helpers being importable from the harness, and it inherits whatever repair policy C-06 picks"; B:20 C-03 INV-001 dependence; B:70 identity check waits for C-08. |
| C4. Defines success/completion criteria | MET | A:113-121 M-1..M-5, each with a "Right if / Wrong if" clause, e.g. M-5 "zero existing pins modified, including `tests/review/test_review_cli.py:44-49`". | MET | B:75-79 M1..M5, each with "Position B is wrong if ..." e.g. M3 "the commit that adds the rule, values file and analysis script must precede the first commit that adds a run". |
| C5. Specifies what is explicitly out of scope | MET | A:143-149 "What this proposal does not claim" (thresholds T-1..T-10, ground-truth authorship, identity checks before C-08, C-06 repaired term, spend approval). | MET | B:99-104 "Open facts that Position B does not settle" and B:79 "Position B does not require it for acceptance of the unification"; B:102 "Position B does not use them [thresholds]". |

### Correctness (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|---|---|---|---|---|
| K1. No factual errors or hallucinated claims | NOT MET | Three code-checked errors in the text: A:65 "silent swap" (logged, `run-reviewer.sh:75`); A:30 counts "that `parse_block` already returns" [CODE-CONTRADICTED]; A:65 no served-model field in the product kernel (`telemetry.py:49,364,378`). | NOT MET | B:51/B:95 "fixable in place" (28 of 89 test files test code absent from git; judge.sh keeps the weak completion test); B:47 "same three easy catches inside it" (GT7 not blocking in implement); B:53 served-model/manifest claim contradicted by `telemetry.py:49`. |
| K2. Technical approaches are feasible with stated constraints | MET | A:69 E-12 verifies a tenth optional module breaks no pin (`test_review_cli.py:44-49` asserts only four names) and a no-model precedent exists (`verify_cmd.py:1-16`); A:28 `unrecorded` state makes the check feasible before C-08. | MET | B:37 E1 the gate exists, 410 lines, 20 tests; B:33 harness fixes each derive from a verified defect; B:71 states the testpaths limit and the operator workaround. |
| K3. Terminology used consistently and accurately | MET | Hyphenated evidence ids `E-1..E-15`, `M-1..M-5`, `P-1..P-5` are distinct from the study names E1/E2 and the `E2:<path>` citation form (A:7); "Tier S/Q/G", "metric of record", "wrong blockers" are used with one meaning throughout. | NOT MET | B reuses E1 and E2 both as evidence-item ids (B:37 "E1.", B:39 "E2.") and as study names (B:57 "E11 ... E1 and E2 are one evidence family"; B:13 "E1's `scripts/reflect_shadow_exit.py`"); "gate" is used for both the structural exit gate and the metric. |
| K4. No internal contradictions (cross-validated with IC) | NOT MET | IC found 1 (A-IC-1: "Nothing below disagrees with a recorded outcome" against additive ledger keys when C-01 "says ledger passthrough keys were deferred", A:15, A:30, A:106). | NOT MET | IC found 2 (B-IC-1 wrong-blocker counts "not gates" versus the control wrong-blocker ceiling that gates, B:13; B-IC-2 E6 "same three easy catches" versus B:94 "I make no claim about that split"). |
| K5. Claims supported by evidence or rationale within the document | MET | Each E-n carries a tag and a citation, e.g. A:45 E-1 recompute with `E2:A1/PILOT-REPORT.md:54-58`, A:47 E-2 `judge-one.sh:19-20` [CODE-VERIFIED, re-read]; the objection answer A:136 gives a stated reason. | MET | Each En carries a tag and a citation, e.g. B:39 E2 `PILOT-REPORT.md:54-58`, B:41 E3 `judge-one.sh:19`, B:43 E4 `presence.txt:11`; B:93-97 numbered answer with reasons. |

### Structure (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|---|---|---|---|---|
| S1. Logical section ordering | MET | A:9-149 Position (1), constraints from adjudicated slots (2), design (3), evidence (4), invariants (5), tests (6), PR/rf-qa effect (7), objection (8), exclusions (9); constraints precede the design that depends on them. | MET | B:11-104 Position (1), design (2), evidence (3), invariants (4), tests (5), PR/rf-qa effect (6), objection (7), open facts (8); adjudicated-slot constraints sit inside section 1 before the design. |
| S2. Consistent hierarchy depth (no orphaned subsections) | MET | H2 sections 1-9; H3 `4.1`, `4.2`, `4.3` all populated (A:43, A:57, A:77); no single-child subsection. | MET | H2 sections 1-8 only, no H3 at all; hierarchy is uniform and nothing is orphaned. |
| S3. Clear separation of concerns | MET | Design (A:25-39), evidence (A:41-89), invariants (A:91-109), measurements (A:111-121), module effects (A:123-130) are separate sections. | MET | Design (B:23-33), evidence (B:35-59), invariants (B:61-71), measurements (B:73-79), effects (B:81-86) are separate sections. |
| S4. Navigation aids present | MET | A:7 citation-form key; cross-references such as "Section 4, E-1" (A:21) and "(E-14)" (A:73); DC 54 of 54 resolve. | MET | B:9 citation-form key; cross-references such as "(section 3, E4)" (B:18) and "(section 6)" (B:25); DC 64 of 64 resolve. |
| S5. Follows conventions of the artifact type | MET | Follows the row's proposal structure: position, consistency with C-01..C-03, design consequence, tagged evidence, invariants, test, PR/rf-qa effect, strongest objection (A:132). | MET | Same structure: position (B:11), consistency (B:17), design (B:23), tagged evidence (B:35), invariants (B:61), test (B:73), effect (B:81), objection (B:88). |

### Clarity (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|---|---|---|---|---|
| L1. Unambiguous language (no "should consider", "might", "as appropriate") | MET | Vague-word regex matches 0 sentences (SR vague = 0); decisions are stated flatly, e.g. A:11 "The metric of record for Tier Q is: ...". | MET | Vague-word regex matches 0 sentences; e.g. B:13 "There is no `superclaude review verify-run`." |
| L2. Concrete rather than abstract | MET | Names files, lines, counts: A:30 `ledger.py:131-134`, `:141-149`; A:61 "59 control-package EXCLUDE flags land on designSpec and 11 short or `*` names exclude all three packages". | MET | B:37 "410 lines ... 20 `def test_` functions ... `d2d8a2d16` (2026-11-12)"; B:51 "0 names matching `test_`"; B:43 "65 ... 38 ... 89". |
| L3. Each section has a clear purpose or can be summarized in one sentence | MET | Headings state purpose: "The position", "Consistency with the three adjudicated slots", "Design consequence ...", "Evidence", "Invariants", "What this proposal does not claim". | MET | Headings state purpose: "Position B in one paragraph", "Design consequence ...", "Evidence", "Invariants", "What would show Position B right or wrong". |
| L4. Acronyms and domain terms defined on first use | NOT MET | Project codes are used without a gloss: "T-1..T-10", "S-0..S-5", "OQ-16", "REQ-36", "GT3/GT7", "C-06", "C-08" (A:123-149); "E2 study" is never defined (A:5). | NOT MET | "OQ-6", "GQ-082", "CO-16", "FX-17", "GT" ids, "O3 con" and the study names E1/E2 are used without definition (B:7, B:57, B:101-102). |
| L5. Actionable next steps or decision points clearly identified | MET | A:136 "M-3 is the test for it, and a result of 'zero in every arm' is a result against this metric as a gate"; A:126 PR-review/rf-qa status "lead" until a seeded set exists. | MET | B:97 "If the owner weighs a kernel-level served-model check above avoiding a new CLI surface, that is a reason to prefer Position A's design"; B:79 M5. |

### Risk Coverage (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|---|---|---|---|---|
| R1. Identifies at least 3 risks with probability and impact assessment | NOT MET | A:105-109 rates INV-H MEDIUM, INV-D MEDIUM, INV-C LOW, INV-K LOW, but gives one severity label and no probability for any risk. | NOT MET | B:69-71 names three endangered items (INV-F HIGH; identity gap "largest capability Position B does not provide now"; test execution) with at most one severity label and no probability. |
| R2. Provides mitigation strategy for each identified risk | NOT MET | Only INV-H has a mitigation (A:105 "Needs a test that scans a run output for a document sentence"); INV-D, INV-C, INV-K are left as open checks (A:106 "Whether a ledger reader rejects an unknown entry key is not checked here [UNVERIFIED]"). | MET | Each endangered item has a stated answer: INV-F (B:69 "the evidence shows no such caller today (E1, E10)"), identity gap (B:70 "stays harness-side (reading transcripts, as `extract.py` does)"), test execution (B:71 "the harness is run only by an operator before a counted run, and its tests are run at that point"). |
| R3. Addresses failure modes and recovery procedures | MET | A:28 three-valued `pass`/`flag`/`unrecorded` ("`unrecorded` (the record the check needs does not exist)"); A:100 INV-I "An `incomplete` reviewer or a refusal is never counted as a clean reviewer"; A:33 judge accepted only if `score.json` exists, parses and satisfies the equation. | MET | B:33 judge-completion check ("`score.json` exists, parses, has the schema keys, judge model equals the requested model"); B:75 incomplete or "unaudited" runs print as such; B:78 M4 gate-bite on the shadow manifests. |
| R4. Considers external dependencies and their failure scenarios | MET | A:19-21 depends on C-01 INV-003 (repair versus pins), C-02 INV-001/INV-002, C-03 INV-007; A:147 identity check stays `unrecorded` if C-08 does not land. | MET | B:18 inherits C-06's repair policy through `findings.parse_block`; B:70 "Until slot C-08 decides the transcript adapter, a served-model check stays harness-side"; B:33 `uv run` import "[UNVERIFIED ...]". |
| R5. Includes monitoring or validation mechanism for risk detection | MET | A:115 M-2 fault fixtures per failure class; A:121 M-5 kernel-burden count with "zero existing pins modified"; A:105 INV-H scan test. | MET | B:75 M1 defect-class tests; B:77 M3 `git log --format=%ci` ordering check; B:78 M4 gate bite. |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant A | Evidence A | Variant B | Evidence B |
|---|---|---|---|---|
| I1. Boundary conditions for collections (empty, single-element, maximum) | MET | A:117 M-3 "Wrong, as a gate, if it is zero in every arm at the available n ... the status is 'no evidence', not 'pass'"; A:21 C-03 INV-007 `requested` can collapse to 1; A:37 empty legacy baseline read as 0.0 at `:313`. | MET | B:28 "an empty legacy baseline is treated as 0.0 (`:313`)"; B:45 "real blocking was 0 of 8 in every arm"; B:76 (b) and (c) "floored or noisy". |
| I2. State-variable interactions across component boundaries | MET | A:20 `verify-run` must derive the verdict from rows and still read older ledgers that hold a stored verdict (C-02 INV-018); A:21 manifest written from the dispatched list before `panel.resolve` drops slots. | MET | B:19 "A harness check that recomputes verdicts must call `ledger verdict`, not read stored fields"; B:43 the blocking-row metric depends on severity typing that C-02 changes. |
| I3. Guard-condition gaps (missing validation, unguarded type assumptions) | MET | A:47 E-2/E-9 judge completion tests only exit code and `jq -e . judge.json` (`judge-one.sh:28-30`); A:29 "Exact tuple keys everywhere; no prefix matching". | MET | B:51 E8 `fullpkg()` 12-character prefix match (`final-table.py:15-18`) and the `rc` plus `jq -e .` completion test (`judge-one.sh:28-30`); B:75 M1 tests for both. |
| I4. Count-divergence scenarios (off-by-one, inclusive/exclusive ranges) | MET | A:61 E-8 "the committed header '69' reproduces and the corrected figure is 71 to 76"; A:49 E-3 65 judge-blocking against 38 real-blocking over 71 rows; A:67 E-11 batch j1 absent from all six audits. | MET | B:43 E4 "65 ... 38 ... 89" (the 51 in rows the reviewer did not mark blocking); B:75 "committed 69; r16:2.2 gives 71 or 76"; B:78 "14 shadow manifests ... (13 published ...)". |
| I5. Interaction effects when features or components combine | MET | A:21 "The union default raises the false-blocker cost (C-03 condition 2), so the metric of record must count wrong blockers; an any-severity metric would not see it"; A:19 conservation law term depends on C-06. | MET | B:19 "A metric keyed on 'found in a blocking-flagged row' changes meaning when C-02 lands"; B:76 M2 "re-run after C-02's typed-`blocking` change lands". |

### Qualitative Summary

| Dimension | Variant A | Variant B |
|---|---|---|
| Completeness | 5/5 | 5/5 |
| Correctness | 3/5 | 2/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 4/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **Total** | **25/30** | **25/30** |
| **qual_score** | **0.8333** | **0.8333** |

Pass-1 notes for reconciliation with pass 2 (judgment-sensitive criteria): K3 (B's E1/E2 id collision), K4 (whether A-IC-1 is a real contradiction), R1 (probability not given by either variant; ratings read as severity only), R2 (A's INV-D/INV-C/INV-K have no mitigation), L4 (project codes undefined in both), C1 (both answer the registry-owner question by placement, neither names a person or CODEOWNERS entry as owner).

### Edge Case Floor Check (needs at least 1/5 on Invariant & Edge Case Coverage)

| Variant | Score | Eligible as base |
|---|---|---|
| A | 5/5 | Yes |
| B | 5/5 | Yes |

## 3. Combined scoring (0.50 x quant + 0.50 x qual), pass 1

| Variant | quant_score | 0.50 x quant | qual_score | 0.50 x qual | variant_score |
|---|---|---|---|---|---|
| A | 0.9980 | 0.4990 | 0.8333 | 0.4167 | **0.9157** |
| B | 0.9787 | 0.4894 | 0.8333 | 0.4167 | **0.9060** |

Margin: |0.9157 - 0.9060| = 0.0097 (0.97 percentage points). The margin is below 5% (`|score_A - score_B| < 0.05`), so the tiebreaker protocol would apply. This pass does not decide the tiebreaker.

Source of the margin: the whole margin comes from the quantitative layer (IC 0.9921 against 0.9815 and SC 1.0 against 0.8889); the qualitative totals are equal at 25/30 with opposite splits (A ahead on Correctness, B ahead on Risk Coverage). For tiebreaker use later: correctness criteria MET are A 3, B 2.

Status: Complete
