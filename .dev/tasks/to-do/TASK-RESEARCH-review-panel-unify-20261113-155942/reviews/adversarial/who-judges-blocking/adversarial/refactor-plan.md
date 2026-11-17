# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (Option D of C05, blind grader after clustering, staged behind a replay gate), selected by the Step 3 tiebreaker (combined score A 0.9091 versus B 0.8810, margin 0.0281 under the 5% band; debate points won B 6 versus A 2). See `base-selection.md`.
- Incorporating strengths from: Variant A (Option A of C05, hardened single-reviewer veto): asymmetric verdict, `singleton_blockers`, input-fix prerequisites, error-cost asymmetry, panel cap as a cost cap, rule-parity and monotonicity tests, corrected test accounting.
- Planned changes: 20 (listed below). Draft 1 was written by the orchestrator, reviewed by a separate agent (22 findings, one BLOCKER, 12 MAJOR; see "Review of this plan" at the end), and revised here; every finding was accepted.
- B's unique contributions U-009 to U-017 are preserved in the merged text unless a numbered change overrides them (the overrides are Changes 5, 6, 7 and 8).
- Risk level (overall): Medium for the merge itself; High for the proposal's readiness (five High changes, 11 HIGH unaddressed invariants). The merge rewrites claims in the base that the debate showed to be wrong, adds new sections, and restructures the Design section around a staged decider. No change resolves an open item by assertion.
- Output file: `proposal-merged.md` in the parent folder of `adversarial/`.

### What the merged proposal must say as its decision (so no change drifts from the debate)
The debate converged, on 30 of 33 points, on one shape. The merged proposal states it as the proposal's position and labels exactly what is decided and what is not:
1. Agreed by both advocates after verifying source (each item carries the HIGH or MEDIUM invariants that qualify it; the merged text must print those IDs next to the item and must not present any item as settled):
   - What runs today is the existing, UNHARDENED veto (`ledger.py:187,274`, `cluster.py:375`). The hardened veto is the interim TARGET once D1, D2, the named resolver and the degrade scope land; none of them is built (B R2 "Remaining disagreement"; A R2 F6). The blind grader is built behind the veto in shadow and goes live per lens only after a pre-registered paired replay passes, starting with singleton blockers (qualified by INV-019, INV-020, INV-022, INV-023, INV-015).
   - `promoted` is counted only and cannot raise a FAIL in shadow (C-003).
   - Certification is set at round 1 and inherited, `defer()` recomputes it (qualified by INV-004, INV-007, INV-024).
   - The grader may demote only with a named failed criterion; on doubt the reviewer's flag stands or the row goes to PENDING (X-006; qualified by INV-008, INV-021, and by the fact that the named criterion is checked by format only).
   - D1, D5 and D6 are fixed first for both arms (qualified by INV-014: "D1 fixed" is undefined and the fix can cancel the evidence gate).
   - The panel cap is a cost cap only; its effect on precision is OPEN (C-005).
   - Reflect keeps the debate and contract 1.8.0; reflect-post uses a code predicate (qualified by INV-016); the evidence transfers only to the spec and tasklist lens (A-001).
2. Agreed to be open (C-005, C-012, X-002): see the "Unresolved conflicts" section.
3. Blocking convergence (the invariant probe): 11 HIGH-severity UNADDRESSED invariants and 10 MEDIUM ones; see the "Unaddressed invariants" section. The merged proposal must not state that any of them is resolved.

### Target structure of `proposal-merged.md` (the merge-executor follows this)
Title and status banner; Decision summary (before the template sections). Then the seven template H2 sections stay in template order (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost), so that S1 and S5 are not lost. Inside them: Design (Position; Interim rule: the hardened veto, a target; Certification and verdict vocabulary; Candidates, promotion and singletons; The grader and its rubric; What each consumer does; Rollout); How it works (data flow; adapters and the two-copy rule; contract fields; CLI surface); Evidence (tables with a counter-reading column; evidence corrections); Cost (the Owner decisions list that sits under Cost in both variants moves out to its own section). After Cost, four new H2 sections: Unresolved conflicts; Unaddressed invariants; Owner decisions; Debate record and provenance. Provenance comments follow `refs/artifact-templates.md` Section 6.

## Planned Changes

Source references use the variant letter, the section or point ID, and the debate round. "Base" means Variant B's text. Every change that touches a point recorded as HYBRID, OPEN or QUALIFY cites the transcript row.

### Group 1: Design and decision rule

#### Change 1: Staged-decider position and decision summary (from the Round 2 consensus; Variant A Design "The decision" and Variant B Design "Position")
- **Source**: Variant A, Design "The decision"; Variant B, Design "Position"; transcript Round 2 tracking rows C-001, C-004, C-013.
- **Target**: Base Design "Position" (restructure), plus a new "Decision summary" at the top.
- **Rationale**: C-001 ended HYBRID at 68% (both advocates): the veto stays the live rule, the grader runs in shadow, and the grader goes live per lens only after the paired replay. B's Position currently says the reviewer flag "stops being the decision", which the debate did not support for the live system. The review (PR-001) found that the first draft of this change claimed the HARDENED veto decides today; that is false, because the hardening (D1, D2, the named resolver, the degrade scope) is not built.
- **Integration point**: Rewrite the Position paragraph as "Reviewers propose; the existing, unhardened veto decides today; the hardened veto is the interim target once its prerequisites land; a blind grader runs in shadow and takes over per lens only after the replay gate". Add the Overview's three-part decided / agreed-open / blocked list as the Decision summary, with each "agreed" item printing the INV IDs listed in the Overview next to it (PR-002), and the cap labelled "cost cap only; precision effect open (C-005)".
- **Risk**: High (the opening claim governs every later section and the first draft got it wrong; all later sections must agree with it).

#### Change 2: Interim rule, the hardened veto (from Variant A)
- **Source**: Variant A, Design (the veto rule, evidence gate, per-lens predicate, partial reviewers abstain, complete-link clustering); Round 2 A concessions 2, 7 and "Facts verified" F1, F6.
- **Target**: New Design subsection "Interim rule: the hardened veto (a target; the unhardened veto is what runs today)", placed before the grader subsection.
- **Rationale**: Both advocates agreed A is the right interim and not "B minus the grader" until D1, D2 and the degrade scope are fixed (A R2 assessment; B R2 assessment).
- **Integration point**: State the rule (`blocking = any(effective flags)`, FAIL while one blocking row is open). List the four input fixes as prerequisites that act on the inputs, each with the debate's corrections: the evidence gate needs a named resolver (C-007); D2 is a code change at `ledger.py:254-257` that inverts the pin at `test_review_ledger.py:376-385` (INV-013); "complete-link" is a C12 dependency; the per-lens predicate is C16. State that `ledger.py:187` (v1) and `cluster.py:375` (v2) are two copies of the rule (see Change 8). Drop A's claim that the veto's FAIL set bounds every decider (X-001).
- **Risk**: Medium (adds a section; must not restate the rejected subset claim).

#### Change 3: Certification rule and verdict vocabulary (from Variant A U-001, Variant B PENDING)
- **Source**: Variant A, Design "Asymmetric verdict"; Variant B, Verdict logic and CLI table; transcript rows C-002, C-010, X-005; Round 2 A concession 5, F7, `defer()`; Round 2 B G2.
- **Target**: New Design subsection "Certification and verdict vocabulary"; edit base "Verdict logic" and "CLI surface".
- **Rationale**: C-002 HYBRID at 73%: A's degrade rule on top of B's PENDING. X-005 HYBRID at 69%: certification is a loop property set at round 1 and inherited.
- **Integration point**: (a) a first review with fewer than two reviewers holding a valid block returns PASS with `degraded: true`, set at round 1 and inherited; decision words and exit codes 0/10/11 are unchanged; the flag is written to the round record and to a report line before the final `verdict:` line (the last-line pin at `test_review_ledger.py:468-472`); `verdict()` keeps its key set (exact-dict pin at `:299-304`). (b) `defer()` (`ledger.py:356-360`) recomputes `degraded` and, under `--decide grader`, PENDING. (c) PENDING and exit 12 exist only under `--decide grader`, with an `EXIT_BY_DECISION` entry (`ledger_cmd.py:13,109`), otherwise a `KeyError` follows. Keep the open points visible: INV-004 (a PASS decided by a one-reviewer re-review is labelled certified by inheritance), INV-007 (PENDING has no mapping at the review cap), INV-024 (the flag is enforced by prose only). Do not claim these are fixed.
- **Risk**: High (touches the verdict path and several pins; the invariants above remain open).

#### Change 4: Candidate rule, promotion and singleton handling (Variant B candidate rule; Variant A U-002)
- **Source**: Variant B, "What the core does" step 1; Variant A, "Record who and how many"; transcript rows C-003, C-004, X-001.
- **Target**: Base "What the core does" step 1 and the contract-fields table; a new `singleton_blockers` row.
- **Rationale**: C-003 HYBRID at 68%: `promoted` counted in shadow only, cannot raise a FAIL until its precision is measured. C-004 HYBRID at 64%: `singleton_blockers` from `reviewers[]`; singletons are the first population the grader goes live on.
- **Integration point**: keep B's candidate rule (defect channel; flagged or MAJOR/CRITICAL; advisory and grounding-gap excluded; MINOR-only excluded) for the v2 path; state the v1-path form (see Change 8). Add `singleton_blockers` (blocking clusters whose blocking members all come from one reviewer) to the cluster output and telemetry, read by no decision. Say only that in shadow `promoted` cannot raise a FAIL and that A's "a decider can only remove blockers" claim is dropped (X-001). Do not state when the subset property would or would not hold once graded decisions are live: the debate did not agree that, and frozen decisions (C-006) are a second way a graded system can differ from the veto (PR-003). Find every sentence in the base that says the shadow counts (`overruled`, `promoted`, `singleton_blockers`) make the choice "checkable after rollout" and qualify it: those counts measure disagreement, not who is right, and production loops have no ground truth (INV-023; PR-009).
- **Risk**: Low (additive) for `singleton_blockers`; Medium for the promotion wording.

#### Change 5: Grader reply contract and rubric versioning (X-006 fix; Variant B grader section)
- **Source**: Variant B, "The grader and its rubric" and "Reply, validation and failure handling"; transcript X-006 HYBRID at 78%, Round 2 B concession 4; invariant INV-008.
- **Target**: Base grader subsections.
- **Rationale**: The agreed outcome of X-006 is exactly this: the grader may demote only with a named failed criterion, and on doubt the reviewer's flag stands or the row goes to PENDING. The tri-state reply (true, false, undecidable) is Advocate B's proposal for how to do it (B R2 concession 4), not an agreed contract. A changed rubric needs a new version (`rubric.md:1`), and the reply change is also a schema change (see below) (PR-012, PR-019).
- **Integration point**: replace "fail-closed by construction" (P4) with "fail-closed on procedure only". Present the tri-state reply as "B's proposal" and say the demotion rule above is what was agreed. State what the probe found and the debate did not resolve: the reply schema is boolean in `parse_grader_reply` and `evaluate_reply` (`stoprule.py:808-830`), so a tri-state reply is a schema change and a fork of files that serve the live stoprule command, in addition to a rubric version (INV-008); the selector for `undecidable` is not agreed (reviewer flag stands, or PENDING); the named criterion is checked by format only (a `why` of at most 25 words, `stoprule.py:813`), not for truth (INV-021); the claim-shape precondition (a named reader and wrong result in the claim, or an `outcome` field) is conceded by B but not in the consensus list (INV-021).
- **Risk**: High (schema change; two open invariants).

#### Change 6: Evidence gate, named resolver and seal rule (C-007, A-003)
- **Source**: Variant A, Design item 1 (evidence gate); Variant B, "What the core does" step 2 and "What the grader sees"; transcript C-007 HYBRID at 66%, A-003 QUALIFY at 58%; Round 2 B G5.
- **Target**: Base step 2 "Evidence pre-checks" and the grader-input table.
- **Rationale**: C-007 (HYBRID, 66%): an unresolved citation is never effective-blocking (A's gate), a named resolver re-reads it, absence findings are routed to the quoted requirement text, and the grader never treats `unverified` evidence as sole support. B's advocate proposed adopting stoprule's seal rule (`stoprule.py:264-265,283-284,541-553,590`). In stoprule a failed re-read forces a repair pass and, after the second seal, the claim becomes `minor-form`; the v1 document loop has no repair pass and no resolver, so porting the rule there means suppression unless a resolver is built (PR-010).
- **Integration point**: write the A-003 QUALIFY condition verbatim: absence findings survive the gate only if the anchor quotes the requirement text that is incomplete and a failed locate routes to a re-read, not to suppression. State the rule and the resolver by name for each path (v2: `verify-citations` and the evidence-validator; v1: `anchor_status` / `span is None`, with no re-read resolver today). Record as open, not as solved: INV-005 (a gated row leaves the brief and the round can PASS before the resolver runs), INV-006 (a located anchor does not prove absence; a fix elsewhere leaves the row `named_not_touched` and the loop ends in ESCALATE), INV-025 (the population that fails the gate is the population it must not suppress), INV-014 (the D1 fix and this gate can cancel).
- **Risk**: High (four open invariants).

#### Change 7: Reflect-post predicate and reflect integration (C-008, C-011; Variants A and B)
- **Source**: Variant A, per-lens predicate and reflect consumer row; Variant B, `reflect-post-v1` and "Reflect Tier 2"; transcript C-008 HYBRID at 70%, C-011 EQUAL at 70%, A-001 QUALIFY at 60%.
- **Target**: Base lens table and consumer subsection.
- **Rationale**: reflect-post already has a code path (`findings_v2.py:161-162`, `contract.py:377-381`) so no grader proposes the class there; the spec and tasklist lens use the frozen rubric; contract 1.8.0, `merge_method` values and the lint are untouched; grader output goes only in nested `telemetry:`.
- **Integration point**: replace the `reflect-post-v1` grader class assignment with a code predicate, and name BOTH rules the "predicate" could mean, never calling them one rule: `findings_v2.py:155-162` makes every MAJOR or CRITICAL finding with a `reflect_category` blocking whatever its `deviation_class`, while `contract.py:377-381` halts only on regression or drift and never on authorized or necessary deviations (a MAJOR authorized finding is blocking in the first and passes the second); `reflect_category` is optional and the contract counts default to 0 when absent (INV-016). Which predicate applies is an owner decision (Change 18). State A-001. Rubric inventory after this change: only `spec-v2` ships in the first build; `reflect-post-v1` is dropped; whether `reflect-pre-v1` ships is NOT decided by the debate (reflect-pre has no ground truth) and is listed under Owner decisions as "who authors the reflect-pre rubric, and whether one ships" (PR-007).
- **Risk**: Medium-High (two different rules, one open invariant, and a rubric inventory the debate did not settle).

### Group 2: How it works

#### Change 8: Document-loop adapter and the two-copy rule (C-015, A-007; Round 2 F1/G1)
- **Source**: Variant B, "How it works" data flow and "Reflect-post"; Variant A, Design step 6; transcript Round 2 A F1 and B G1; C-015 A at 80%; invariants INV-011, INV-017.
- **Target**: Base "How it works" data flow; new subsection "Adapters and the two copies of the rule".
- **Rationale**: Both advocates verified that the document loop runs on the v1 `findings` module (`ledger.py:15,165,187`, `merge_cmd.py:109`) and the v2 path on `cluster.py:375`; B's candidate rule and `verify-citations` exist only on v2. B conceded the adapter and estimated 50-100 lines plus a second renderer plus a parity test (an advocate estimate, not measured).
- **Integration point**: show two data-flow variants (v1 ledger rows, v2 clusters); v1 candidate rule = `blocking or severity in {MAJOR, CRITICAL}` with no channel test; v1 pre-check = `anchor_status == "missing"` (`span is None`); the renderer reads the row's `claim`, `anchor` and the text at `span`; the v1 renderer must be blind in the same way as the v2 one (no reviewer id, severity or `blocking` flag, PR-018). State the parity test across both copies and that at least two more copies of the rule exist outside the core (`diffgate.py:796`, `stoprule.py:1179-1191`), whose scope is not decided (INV-017). Keep INV-011 visible: one `representative` claim per cluster is graded and then frozen for every member, and "tighten `same_defect`" has no mechanism or test.
- **Risk**: High (new section; two open invariants; adapter cost is an estimate).

#### Change 9: Contract fields and CLI surface (C-010)
- **Source**: Variant A, contract-fields table; Variant B, `review-decisions/1`, CLI table; transcript C-010 HYBRID at 65%.
- **Target**: Base contract-fields and CLI tables.
- **Rationale**: keep exits 0/10/11 and the verdict words; add `degraded` as a field and a report line; add exit 12 plus an `EXIT_BY_DECISION` entry for PENDING under `--decide grader` only; keep B's `review grade prep|apply|status` and `--decide flag|grader`.
- **Integration point**: in the CLI table, the exit-code row names BOTH places that must change for PENDING, `EXIT_BY_DECISION` at `ledger_cmd.py:13` and the exit call at `ledger_cmd.py:109`, and lists `degraded` and `PENDING` as the new values (PR-021). Merge the two field tables (A: `blocking_effective`, `anchor_status`, `rejected_lines[]`, `partial`, `degraded`, `singleton_blockers`; B: `lens`, `rubric_id`, `rubric_sha256`, `grader`, `batches[]`, `clusters{}`, `summary`); rename colliding terms (Change 19). Flag INV-002 (the ledger schema string `review-ledger/1` accepts any ledger; loops mid-flight at rollout have no decision field; a rubric-hash refusal strands a loop when `spec-v2` ships) and INV-018 (shadow data must stay out of `render_merged_report` and out of the exit code).
- **Risk**: Medium.

### Group 3: Evidence and correctness argument

#### Change 10: Evidence corrections (X-002, X-003, X-004, C-005, C-012)
- **Source**: Variant B V7 and P1; Variant A E-3, E-5, E-7; transcript Round 2 A concessions 2-4; Round 2 B concessions 1-2, G4.
- **Target**: Base Evidence tables and a new "Evidence corrections" subsection.
- **Rationale**: both advocates conceded these claims. V7 must name D1 (49 dropped blocking findings, four FAIL-to-PASS flips, `COMBO-REPORT.md:291-292`) and say D1 pushes counted wrong blockers down while D5 (13 null-span blocking rows) and D6 (83 chained rows) may push them either way; attribution is unmeasured. P1 becomes "the grader's false-block rate PER CANDIDATE is independent of reviewer count by construction (a larger panel can still produce more candidates); E2 neither supports nor refutes a size effect". A's E-7 cap (as a precision lever) and A's E-5 "contamination excuse" are dropped; the cap is written once, as "cost cap only; precision effect open (C-005)", in the Decision summary and in the risk table. Add the diff-analysis X-003 note that wrong blockers (rows with no ground-truth match) and the 27 over-graded real defects are different measures. A's reading of the 65-versus-38 gap (27 real defects over-graded against `blocking_in_implement`, from the definition at `COMBO-REPORT.md:291`) is kept as a counter-reading column entry, with B's point that the gate is judged against implement-blocking.
- **Integration point**: add a control-package row set by panel size taken from Advocate B's full-table aggregation (control wrong blockers per run: n=1 1.00, n=2 1.27, n=3 1.05, n=4 1.33, n=5 0.89) and note that Advocate A's subset gave 1.33, 1.21, 1.50 and 1.00 and that both are advocate-computed from `COMBO-REPORT.md` rows 306-337 and were not re-aggregated by the orchestrator. State that `ember + sonnet` 0.25 is the defect-rich figure and its control figure is 1.25. Implement the agreed S-003 outcome (EQUAL: B's source-column tables plus a counter-reading column): add a "Counter-reading" column to EVERY Evidence table, move Variant A's E-1 to E-17 reasoning into that column as the matching rows, and tag every fact the author did not re-read with `[VIA <source>]`, keeping the tags `[READ]`, `[VIA]`, `[E2 4a22d74]`, `[external]` (PR-006). Evidence items that only A carried (E-14 on the advisory tasklist review points and the blocking post gate that cannot fail on drift) are kept as `[VIA research/09 and 13]`, not as read facts, because the debate did not verify them (U-004).
- **Risk**: Medium (edits many evidence rows; numbers must be tagged as advocate-computed).

#### Change 11: Correctness argument rewrite (C-006, C-013; B P2-P5; A steps 3-5, 8)
- **Source**: Variant B Correctness P1-P5 and "Weakest point"; Variant A Correctness steps 1-8; transcript C-006 B at 63%, C-013 B at 71%.
- **Target**: Base "Correctness argument".
- **Rationale**: keep B's structure (structural argument plus a stated falsifier for each); keep A's error-cost asymmetry (step 4) but state its limit (the re-find rate that decides whether a persistent FAIL escalates is unmeasured, B R2); narrow C-006 to rows whose cited text did not change (B R2 new evidence, `ledger.py:235`); state A's step 8 ("what this argument does not establish") for both options.
- **Integration point**: P1 rewritten per Change 10; P4 rewritten per Change 5; delete A's step 1 subset claim and step 2 "FAIL is the right verdict" snapshot argument. Add INV-001, INV-006, INV-019 and INV-020 to "what this argument does not establish": under the live veto a re-found row still takes the current round's flag (`ledger.py:210-218`), so the frozen decision helps only after the flip (INV-001); an absence defect fixed elsewhere leaves the row `named_not_touched` and a frozen decision then ends the loop in ESCALATE (INV-006); a grader that always demotes would pass the replay's control-package criterion (INV-019); and the replay never runs the rounds-2-and-3 code where C-006 lives (INV-020).
- **Risk**: Medium.

### Group 4: Risks, tests, cost and the acceptance gate

#### Change 12: Risk table merge with likelihood bases (R1; S-004)
- **Source**: Variant B R1-R11 (base table); Variant A Risks 1-8; the re-evaluated R1 standard in `base-selection.md` (a risk counts when the text gives a measured rate, count, frequency or rating plus its consequence).
- **Target**: Base "Risks and mitigations" table, with new columns Likelihood basis and Consequence.
- **Rationale**: B's Residual cells use modal words and failed R1; A's frequency counts passed it. The merge keeps B's format and adds A's numbers.
- **Integration point**: carry A's risks into the table: self-grading in the spec lens (A Risk 2; 27 over-graded catches), one reviewer can clear a row (A Risk 3; pre-flip live path, INV-001), promotion into reflect (A Risk 4, now the reflect-authority bump), correlated reviewers (A Risk 5), thin evidence (A Risk 6; 3 packages, 16 defects, n of 4-6), the PASS rule adds degraded outcomes (A Risk 7; 80 reviewer-level invalid-block cases, `COMBO-REPORT.md:292`; plus INV-009: two same-model reviewers count as two), chained clusters (A Risk 8). Add the debate's new risks: v1 adapter uncosted, `defer()` and PENDING, grader pins `model: sonnet` and non-Anthropic classes unverified, the replay can be passed by an always-demoting grader (INV-019). Every row gets a likelihood basis or the words "no basis recorded".
- **Risk**: Medium.

#### Change 13: Test plan merge with corrected accounting (C-014, S-006)
- **Source**: Variant B 16 new-test groups and the existing-tests table; Variant A items 1-9; transcript C-014 HYBRID at 65%, S-006 HYBRID at 63%; Round 2 A F2.
- **Target**: Base "Test coverage needed".
- **Rationale**: both advocates agreed on B's groups plus A's rule-parity and monotonicity tests, with the accounting corrected.
- **Integration point**: existing tests: `test_review_ledger.py:128-129`, `:518-544` (veto pins, stay green under `--decide flag`); `:376-385` and `:408-417` (D2 and D5, change under the prerequisites); `:299-304` (exact dict on `verdict()`, breaks only if `verdict()` gains a key, so the `degraded` key goes elsewhere); `:296-298`, `:307-315`, `:396-403`, `:468-472` (one-reviewer PASS and `defer` pins, gain a `degraded` assertion; the last pins the last report line); `test_review_cli.py:328-348` (exit 0 and PASS). New tests: B's 1-16 with two adjustments (the blindness test covers BOTH the v1 and the v2 renderer, PR-018; B's reflect-post parity group becomes a test of the code predicate in Change 7, and the grader-selection and data-file groups cover `spec-v2` only, PR-007), plus rule parity across the v1 and v2 copies, monotonicity, effective flag, `singleton_blockers`, `defer` recomputation, `EXIT_BY_DECISION` with PENDING, reflect isolation. Add the tests the probe showed are missing and mark them as not yet agreed in the debate: a replay that exercises rounds 2 and 3 (INV-020), an always-demote grader as a negative control (INV-019), a tri-state reply and canary-count test (INV-008, INV-010), and an anchor-missing-after-D1 test (INV-014).
- **Risk**: Medium.

#### Change 14: Cost merge (C-015, INV-010)
- **Source**: Variant A Cost; Variant B Cost; transcript C-015 A at 80%.
- **Target**: Base "Cost".
- **Rationale**: A's interim is effort S with zero extra model calls; B is effort L (about 300-400 lines for `grade.py`, 150 for `grade_cmd.py`, 40-60 for `ledger.py`, an agent promoted into `src/`), plus the v1 adapter (50-100 lines, an advocate estimate). Rubric and canary files: one rubric (`spec-v2`) and its canary file in the first build, not three (Change 7; PR-007).
- **Integration point**: two cost lines (interim; destination) and the benchmark cost (about 380,000 REVIEWER OUTPUT tokens for six replicates of the default panel, 6 x 63,644, A's figure from `COMBO-REPORT.md:331`; judge passes and the judge re-run are not costed). Correct B's canary overhead with one formula: overhead = canaries / (claims + canaries) per batch, with two canaries per batch whatever its size, so 25% holds only for a six-claim batch, and a singleton-first batch of 1 claim plus 2 canaries has 67% of its items as canaries, or 200% relative to the one real claim (INV-010). Carry A's "cost of being wrong" argument (U-008): if the replay fails, the follow-up filter on singleton blockers reuses the evidence gate, effective flag, abstention rule and `singleton_blockers` that the interim adds, so nothing is thrown away.
- **Risk**: Low.

#### Change 15: Replay and acceptance gate (C-013, C-012, M7)
- **Source**: Variant B R1 and "Rollout"; Variant A Test item 9 and Risk 1; transcript C-013 B at 71%, C-012 OPEN at 71%; Round 2 B concession 7.
- **Target**: Base "Rollout" and R1.
- **Rationale**: both advocates agreed on a paired, pre-registered replay: D1, D5 and D6 fixed first for both arms; veto and grader on the same candidate sets; both scored against `blocking_in_implement`; the known E2 wrong blockers as a leniency probe; the grader's true-negative rate reported; canary and benchmark sets disjoint; an inconclusive result keeps the grader in shadow.
- **Integration point**: write the gate as above, keeping B's qualitative pass criterion in the text (grader wrong blockers on the control package below the veto's on the same candidate sets, at no loss of real-blocking recall on the defect-rich packages), the word "pooled" for the 71 valid-era rows, and the note that "same candidate sets" breaks wherever D1 changes the set (INV-014, INV-022). State what is NOT settled and keep it visible: no numeric pass threshold exists in either variant or in the debate, and an always-demoting grader meets the criterion above (INV-019); the control package has two defects, no blocking, and pooled rows are not independent, so power is low and an inconclusive result is likely (INV-022; B's own R1 residual); the replay never runs `apply_revision`, `defer`, re-found or regressed paths, which is where C-006 lives (INV-020); shadow counts measure disagreement and not correctness because production loops have no ground truth (INV-023); shadow data collected before `spec-v2` and the claim-shape fix measures a rubric that will not ship (INV-015); the E2 reports are findings-v1 and whether anchors are usable is unverified.
- **Risk**: High (the gate is the proposal's only measurement and the probe found it insufficient on five counts).

### Group 5: Visibility, owner decisions and hygiene

#### Change 16: "Unresolved conflicts" section (new)
- **Source**: transcript Convergence Assessment; Round 2 tracking rows C-005, C-012, X-002.
- **Target**: New section after "Cost".
- **Rationale**: the user requires every unresolved conflict to stay visible.
- **Integration point**: three rows, each giving the agreed-open position and "the measurement the debate named; it may not decide" with the limits attached: C-005 (panel-size effect: the replay reports wrong blockers by n, but per-panel n is 4-6 so power by panel size is low; the cap stays a cost cap); C-012 (cause of the veto's wrong blockers: fix D1, D5, D6 first, same candidates, score on `blocking_in_implement`; limits INV-019, INV-020, INV-022); X-002 (V7 and E-5 disagree on attribution: unmeasured; D1 pushes counted wrong blockers down; D5 and D6 may push either way, which was not agreed). Then the three QUALIFY assumptions, each with its condition and agreed confidence, written out: A-001 (60%) holds only for the spec and tasklist lens, because E2 ran the spec brief, reflect-post is code-decided and reflect-pre has no ground truth; A-003 (58%) holds only if absence findings anchor to the quoted incomplete requirement text and a failed locate routes to a re-read, not to suppression (INV-006, INV-025 attached); A-007 (60%) holds only if `same_defect` is tightened and a cited-text-changed guard is actually implemented (INV-011 attached).
- **Risk**: Low (additive).

#### Change 17: "Unaddressed invariants" section (new)
- **Source**: `invariant-probe.md` (25 findings).
- **Target**: New section after "Unresolved conflicts".
- **Rationale**: convergence is blocked by 11 HIGH-severity UNADDRESSED invariants; the protocol's return contract lists them and the user requires them to stay visible in the merge.
- **Integration point**: a table of all 25 findings (ID, category, assumption, status, severity, one-line evidence, and the change in this plan where it is referenced). Heading text states that the section is the debate's list of what it did not resolve, not a to-do list the merge has completed. HIGH items first, then MEDIUM and LOW, then the two ADDRESSED ones. No item is rewritten as resolved.
- **Risk**: Low (additive), but the executor must not soften severity or status.

#### Change 18: Owner decisions merge (Variant A Cost; Variant B Cost "Decisions this proposal needs")
- **Source**: Variant A Cost "Owner decisions"; Variant B Cost "Decisions this proposal needs from the owner"; transcript.
- **Target**: New or merged "Owner decisions" section.
- **Rationale**: both variants leave numbers and policy to the owner; the debate added more.
- **Integration point**: move the owner-decision lists out of the Cost section into this section, and merge them. List: control-package wrong-blocker tolerance and a numeric pass threshold for the replay (INV-019); which reflect-post predicate applies, `findings_v2.py:155-162` or `contract.py:377-381` (INV-016); who authors the reflect-pre rubric and whether one ships (Change 7); MINOR drift (G-03); who sets `unauthorized_deviation_present` (G-04); static-unreachability rule (G-05); the environment the central panel serves (C03, O-2); the benchmark-port owner (G-59); who authors the rubrics; the verdict vocabulary for a degraded PASS (C19) and whether any caller treats it as uncertified in code (INV-024); whether `diffgate` and `stoprule` copies of the blocking rule are in scope (INV-017); the selector for `undecidable`; the claim-shape fix or `outcome` field (INV-021); ledger schema bump (INV-002).
- **Risk**: Low.

#### Change 19: Terminology and clarity fixes (K3, L1, L4)
- **Source**: re-evaluated K3 for B; L1 and L4 for both variants in `base-selection.md`.
- **Target**: whole merged text.
- **Rationale**: B lost K3 ("decision" for the grader outcome and for the ledger REVISE/ESCALATE word; "class" for the model class and for the deviation class) and both variants lost L1 and L4.
- **Integration point**: rename the grader outcome to `grade` (values blocking, not_blocking, undecidable, unconfirmed) and keep `decision` for the ledger routing word; rename the model class to `model_class` and keep `deviation_class`; define on first use: E2, D1-D6, C-numbers (one-line glossary of the conflicts actually cited), UC-1/UC-2, B1-B3, veto, candidate, shadow; replace open phrases ("names proposed", "design parameters to fix at build time", "owner-set tolerance") with either a value or an entry in "Owner decisions".
- **Risk**: Low (wording), but a rename must be applied everywhere or it creates a new K3 collision.

#### Change 20: Debate record, provenance and status banner
- **Source**: transcript; `base-selection.md`; Step 5 provenance rules.
- **Target**: top banner and a closing "Debate record" section.
- **Rationale**: the merged text must say it is a partial result and where each claim came from.
- **Integration point**: banner: status partial; alignment 90.9% (30 of 33 points with a determinate agreed outcome); convergence NOT achieved, blocked by 11 HIGH unaddressed invariants; 3 agreed-open points. Never write "converged" without that qualifier (PR-013). Closing section: one table of the 33 points with the agreed outcome (compact), and a pointer to the artifacts. Provenance comments per section (`<!-- Source: ... -->`) per the template.
- **Risk**: Low.

## Base weaknesses and where the plan fixes them

| Base weakness (Variant B) | Debate source | Better variant reference | Fix | Change |
|---------------------------|---------------|--------------------------|-----|--------|
| No reviewer-count guard: one reviewer plus an approving grader yields PASS | C-002, Round 1 B | A (asymmetric verdict) | scoped certification rule | 3 |
| `defer()` bypasses PENDING | Round 2 B G2 | A found `defer()` for `degraded` | recompute both in `defer()` | 3 |
| P4 "fail-closed by construction" contradicts R5 | X-006 | A (R1 critique) | true/false/undecidable, named criterion | 5 |
| P1 "E2 measured that direction"; V7 omits D1 | X-004, X-002 | A (E-6, E-5 in part) | evidence corrections | 10 |
| Document loop is on v1; candidate rule and `verify-citations` are v2-only | C-015, Round 2 F1/G1 | A (v1 path has `span is None`) | adapter section | 8 |
| `unverified` evidence graded as true; seal rule not ported | C-007, Round 2 G5 | A (hard gate) | gate plus seal rule | 6 |
| No `singleton_blockers`; promotion has no precision data | C-003, C-004 | A | shadow-only `promoted`; count | 4 |
| Test accounting omits `defer`, exit-code and exact-dict pins | C-014 | A (item 3), Round 2 F2 | merged test plan | 13 |
| Risk table lacks likelihood bases (R1); terminology collisions (K3) | re-evaluation | A (Risks 1, 7, 2) | risk table; renames | 12, 19 |

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach (Variant A) | Rationale for Keeping the Base Approach or Dropping A's |
|------------|-------------------------------|---------------------------------------------------------|
| C-001 | The veto is the decision and no second agent decides | Kept only as the interim live rule. Both advocates agreed the grader goes live per lens after the replay; A's own advocate called B "the right destination" (Round 2) |
| X-001 | "A decider that filters that list can only remove blockers"; "none can add recall" | False for B's promotion path (both advocates); replaced by shadow-only `promoted` |
| X-002 / C-012 | E-5 "contamination" as an excuse for the veto's measured precision | The agreed outcome is only that D1 (49 dropped blocking findings, four FAIL-to-PASS flips) pushes counted wrong blockers down, so the excuse has no support for D1, and that attribution stays unmeasured; the direction of D5 and D6 was never agreed (A said D6 depresses blockers in Round 1; B said D5 and D6 could inflate them) |
| C-005 / X-004 | Cap of three finders as a precision lever (E-7) | Cited the defect-rich column; control is flat by panel size; kept only as a cost cap |
| X-007 | "The only option that leaves every pin and contract alone" | False by one assertion and false relative to B's `--decide flag` default |
| Step 2 of A's Correctness | "A wrong-blocker row sits on a plan with defects, so FAIL is right" | Snapshot argument; the control FAIL rate is the right metric (A conceded) |
| S-003 | Inline argument inside numbered evidence items | B's source-column tables kept; A's counter-readings move into a counter-reading column |
| S-004 | Prose risk paragraphs | B's table kept, with A's frequency counts added |
| C-006 (partial) | Leave one-report clearing to D2 and C13 alone | Kept as the live-path behaviour with the hole stated (INV-001); B's frozen decision is the post-flip fix, narrowed to unchanged cited text |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | High | Opening claim wrong (the first draft said the hardened veto is live today) or disagrees with later sections | Re-read the Decision summary against Changes 2-5; search the merged text for "decides today" |
| 2 | Medium | The rejected subset claim creeps back in | Search the merged text for "can only remove" and "no decider can add" |
| 3 | High | Verdict path wrongly described; pins broken | Keep Change 3 wording at "proposed" and keep INV-004, 007, 024 attached |
| 4 | Low-Medium | `promoted` described as able to block in shadow | Reword to "counted only" |
| 5 | High | A schema change is described as a rubric edit | Keep INV-008 and INV-021 attached |
| 6 | High | Gate described as safe | Keep INV-005, 006, 014, 025 attached |
| 7 | Medium-High | Two different rules described as one; rubric inventory presented as settled | Keep INV-016 attached; list the predicate and reflect-pre rubric as owner decisions |
| 8 | High | Adapter cost presented as measured | Tag the 50-100 lines as an advocate estimate |
| 9 | Medium | Terms collide | Apply the Change 19 renames everywhere |
| 10 | Medium | Advocate-computed numbers read as measured | Tag as advocate-computed, not re-aggregated |
| 11 | Medium | Argument claims more than shown | Keep the "what this does not establish" list |
| 12 | Medium | Risks listed without a likelihood basis | Use "no basis recorded" |
| 13 | Medium | Missing probe-derived tests read as agreed | Mark them "not agreed in the debate" |
| 14 | Low | Wrong overhead figure | Use the per-batch formula |
| 15 | High | The gate is presented as sufficient | Keep INV-015, 019, 020, 022, 023 attached |
| 16-18 | Low | An open item is dropped | Count the rows: 3 conflicts, 3 QUALIFY assumptions, 25 invariants |
| 19 | Low | Rename applied partly | grep the merged text for the old terms |
| 20 | Low | Banner overstates convergence | State "partial" and the blocking invariants |

## Review of this plan

Reviewer: an independent general-purpose agent (not the orchestrator, not an advocate, not a scorer), asked to check coverage of open items, fidelity to the debate, unique contributions, shared-assumption conditions, internal consistency, silent resolution, spot-check facts, and gaps. Verdict returned on draft 1: **APPROVE WITH CHANGES**. Findings: 22 (1 BLOCKER, 12 MAJOR, 9 MINOR). Disposition: all 22 accepted and applied in this revision; none was rejected.

| ID | Severity | Where | Finding (short) | Disposition and where applied |
|----|----------|-------|-----------------|-------------------------------|
| PR-001 | BLOCKER | Overview, Change 1 | Draft claimed the hardened veto decides today; the debate showed the unhardened veto runs today and the hardening is unbuilt | Accepted. Overview item 1, Change 1 rationale and integration point, Change 2 title rewritten; Change 1 risk raised to High |
| PR-002 | MAJOR | Overview, Change 1 | "Decided" list had no pointer to the HIGH invariants that qualify each item; cap listed as decided while C-005 is open | Accepted. Each item now carries its INV IDs; cap labelled "cost cap only; precision effect open (C-005)" |
| PR-003 | MAJOR | Change 4 | Sentence on when the subset property holds exceeded X-001/C-003 and contradicted Change 2; frozen decisions also break it | Accepted. Sentence deleted; replaced by "in shadow `promoted` cannot raise a FAIL; the subset claim is dropped" |
| PR-004 | MAJOR | NOT table, X-002/C-012 | Claimed D6 depresses blockers as a Round 2 concession; it was a Round 1 position, and B said D5 and D6 could inflate | Accepted. Row reworded to the agreed outcome only |
| PR-005 | MAJOR | Change 16 | Implied the replay decides the open points | Accepted. "the measurement the debate named; it may not decide" with limits INV-019, 020, 022 and the n of 4-6 note |
| PR-006 | MAJOR | S-003, Change 10 | The agreed S-003 outcome (counter-reading column, `[VIA]` tags) had no implementing change | Accepted. Added to Change 10 |
| PR-007 | MAJOR | Changes 7, 13, 14 | Reflect-post grader dropped in Change 7 but still costed (three rubrics) and tested (B's 1-16) | Accepted. Rubric inventory stated (only `spec-v2` ships; reflect-pre left as an owner decision); Change 13 and 14 adjusted |
| PR-008 | MAJOR | Change 7 | "The code predicate" undefined; two different rules; not an owner decision | Accepted. Both rules named; owner decision added in Change 18 |
| PR-009 | MAJOR | Overview, Changes 4, 15 | B's "checkable after rollout" claim (U-014) not corrected against INV-023; U-009 to U-017 not stated as preserved | Accepted. Instruction added in Change 4; Overview line added |
| PR-010 | MAJOR | Change 6 | "Seal rule is ported" stated as settled; v1 has no repair pass; A-003 condition missing | Accepted. Rationale rewritten as B's proposal; A-003 condition written verbatim |
| PR-011 | MAJOR | Changes 8, 16 | QUALIFY conditions for A-001, A-003, A-007 not written out | Accepted. Written out with confidences in Change 16 |
| PR-012 | MAJOR | Change 5 | Tri-state reply presented as agreed; "named criterion checked by format only" omitted | Accepted. Labelled "B's proposal"; the format-only point added |
| PR-013 | MINOR | Change 20 | Banner "convergence 90.9%" reads as achieved | Accepted. Banner reworded |
| PR-014 | MINOR | Change 10 | P1 wording should be "per candidate"; add the X-003 measure note | Accepted |
| PR-015 | MINOR | Change 14 | Canary overhead needs one denominator; 380,000 tokens is reviewer output only | Accepted. Formula and wording corrected |
| PR-016 | MINOR | Change 15 | Qualitative pass criterion, "pooled" and the D1 candidate-set break missing | Accepted |
| PR-017 | MINOR | Change 11 | INV-006 and INV-020 missing from "what this argument does not establish" | Accepted |
| PR-018 | MINOR | Changes 8, 13 | The v1 renderer must be blind too | Accepted |
| PR-019 | MINOR | Change 5 | Reply change is a schema change as well as a rubric version | Accepted |
| PR-020 | MINOR | Target structure | Template H2 order must be kept; Owner decisions must move out of Cost | Accepted. Target structure and Change 18 rewritten |
| PR-021 | MINOR | Change 9 | Name both places that must change for exit code 12 | Accepted |
| PR-022 | MINOR | Risk ratings | Change 1 and Change 7 ratings understated; overall rating | Accepted. Change 1 to High, Change 7 to Medium-High, overall "Medium for the merge, High for readiness" |

Review checks that passed without change: the reviewer's coverage table found no invariant, agreed-open point or QUALIFY assumption uncovered (the partial rows were closed by PR-005, 006, 010, 011, 012 and 017); unique contributions U-001 to U-007 and U-009 to U-017 were present, U-008 was lost silently and is now carried in Change 14 (U-004 gained its named facts in Change 10). Facts the reviewer verified by reading source: `ledger.py:356-360`, `ledger_cmd.py:13,109`, `test_review_ledger.py:299-304`, `:468-472`, `:376-385`, `:408-417`, `:518-526`, `ledger.py:187` and `cluster.py:375` as two copies, the v1 `findings.py` field list, `findings_v2.py:161-162` versus `contract.py:377-381`, `stoprule.py:808-830`, `:264-265`, `:283-284`, `:1179-1191`, `diffgate.py:796`, the control-package figures (n=1 1.00, n=2 1.27, n=3 1.05, n=4 1.33, n=5 0.89), and the E2 counts at `COMBO-REPORT.md:291-292`. Not verified by the reviewer: the "13 null-span blocking rows" (D5), which comes from an audit file (`analysis/audits/audit-D/summary.md`), so the merged text must tag it `[VIA audit-D]`.

## Review Status
- [x] Reviewed by a separate agent (independent of the orchestrator, the advocates and the scorers): APPROVE WITH CHANGES, all 22 findings applied
- [x] Auto-approved (default, non-interactive mode) after the revision
- [ ] User-approved (`--interactive` was not set)
- Approved by: auto, after independent review
- Approval timestamp: 2026-11-14 (UTC)

