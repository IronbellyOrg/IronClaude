# Base Selection Report

## Quantitative Scoring (50% weight)

All five metrics were computed by `/tmp/cmp_quant.py` (deterministic regex and counts over `variant-1-original.md` and `variant-2-original.md`; re-running gives identical numbers). Source requirements: the report-shape and decision-relevant items listed under RC (the inputs have no formal FR-/NFR- ids, so the skill's section-level topic-matching edge case applies).

| Metric | Weight | Variant 1 (run 1) | Variant 2 (run 2) |
|---|---|---|---|
| requirement_coverage | 0.30 | 1.000 (24/24; missing: none) | 1.000 (24/24; missing: none) |
| internal_consistency | 0.25 | 0.994 (1 - 5/880 cited-claim lines) | 0.989 (1 - 8/756 cited-claim lines) |
| specificity_ratio | 0.15 | 1.000 (20849 concrete / 0 vague) | 1.000 (19454 concrete / 0 vague) |
| dependency_completeness | 0.15 | 0.795 (696/875 Section refs resolve) | 0.955 (343/359 Section refs resolve) |
| section_coverage | 0.15 | 0.786 (11/14 H2 sections) | 1.000 (14/14 H2 sections) |
| **quant_score** | | **0.936** | **0.991** |

### Internal contradictions counted for IC (established in diff analysis, orchestrator verification and debate)

**V1** (5):
- V1 8.4 states 'ironbelly/shadow-runs 3 commits ahead' (stale: 5 now; r25 re-derivation #2)
- V1 labels 16 of 20 conflicts DECIDED-BY-EVIDENCE although the same report calls 4 debates partial and C-04 depends on availability vs diversity (V2 advocate and X-052; status overclaim)
- V1 Q-54..Q-61 itself flags a verdict-vocabulary contradiction (PENDING/exit 12 vs ESCALATE) in the carried design (U-106)
- V1 count '37 reflect test files' (V1:381) vs 38 (r25 re-derivation #6)
- V1 rf-* '43 call sites' unit unstated and not reproducible (X-022)

**V2** (8):
- V2 SC-04 'declared quorum (decision)' vs delta row G-14 decided quorum (X-004)
- V2 G-85 and 3.5 list the workflow/tasklist entry open while delta row T-4/3.5 says decided (X-005)
- V2 SC-17 'decision, 0.75 or 0.80' vs delta row 'decided by the code: 0.80' (C-017)
- V2 Section 7 C-2 and D9 assert KeyError on the ledger merge path while V2 axis 1 and Appendix B say rejected at findings.py:104 (X-049, X-053; orchestrator VERIFIED-V1)
- V2 2.4 treats installed-variant scripts as read (verified) while 2.9 OQ-01 tags all E3i cells UNVERIFIED (X-034)
- V2 G-06 rated Important although its own rubric (V2:1121) makes a fail-open verdict Critical (CL-15, V2 advocate concession)
- V2 uses arXiv 2606.19544 (withdrawn) at V2:1647-1648, 1655, 2044, 2829 (X-036; r25 #26)
- V2 'pr_submit 50 test files' vs 47 (r25 #6); '(6)' occurrences vs 5 lines/7 (X-017)

Note on IC: the denominator is the number of lines that carry a file:line citation (a proxy for scorable, falsifiable claims); the numerators are the internal inconsistencies actually established, so IC is high for both and differentiates weakly. Note on SR: the concrete-indicator regex is deliberately broad (numbers with units, file names, hashes, line refs), so SR is near 1.0 for both reports and differentiates weakly.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Two independent scorer agents evaluated the 30 criteria with Claim-Evidence-Verdict: pass 1 in input order (Variant 1 then Variant 2), pass 2 in reverse order, without seeing each other's output. The tables below are the pass 1 CEV tables, which carry the final verdicts (pass 2 agreed on 59 of 60 criterion-variant pairs; the one disagreement was re-evaluated and resolved to the pass 1 verdict, see Position-Bias Mitigation). Pass 2's evidence is in `partials/qual-pass2.md`. Sampling statement: both scorers read the cited sections in full and sampled the rest; exact ranges are in each pass file's Coverage section.

### Completeness

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| C1 Covers all explicit requirements from source input | MET | 1. Problem Statement (L93) restates the question and the five consumers; 8. Implementation Plan (L3101) "what each finding ... becomes in the unified design ... which suites must keep passing and which branch layouts are possible": 8.1 Value inventory (L3105), 8.2 Migration path (L3822), 8.3 No-regression gate list (L4031), K-1..K-11 constraints (L552-564), 9.5 owner decisions (L4366) | MET | 1. Problem Statement (L126) "Which ONE unified central Review Panel design (a shared core plus thin modules)..."; 8.1 Value Inventory (L4238, 5,950 rows with destinations); 8.2 (a) Binding constraints C1-C29 (L4426-4458), (b) No-regression gates G1-G27 (L4460-4492), (c) Dependency facts and (e) "Files and modules a later plan will touch" (L4494, L4551) as migration input; 9.8 owner decisions (L4766). Note: no ordered migration path by design ("It orders no work", L4412) |
| C2 Addresses edge cases and failure scenarios | MET | 4. Gap Analysis D1 (L589) "the loss is silent ... 3 merged verdicts flipped to PASS"; D3 (L591) "A round can PASS on one valid reviewer"; 6.E C13-05 (L2640) "at review 1 every reviewer returns a valid empty block ... a skimming round-1 panel can certify PASS" | MET | 3.3 SC-03..SC-07 (L1179-1183) reproductions of fail-open paths ("1 valid of 4 gives PASS today"); 8.2(c) D26 (L4525) "treats an empty legacy baseline as 0.0"; D8 (L4507) contracts that fail `yaml.safe_load` |
| C3 Includes dependencies and prerequisites | MET | 8.2 Track M1 (L3828) "**Dependencies:** none outside this track for M1-01 to M1-06; M1-07 and M1-08 depend on the C13 and C05 decision gates ..."; 8.2 intro (L3824) "'Depends on' names logical prerequisites" | MET | 8.2 (c) Dependency facts (L4494-4525) "X must exist before Y can work", D1-D26 with evidence; "Interactions between axes (shared prerequisites, not an order)" (L3043) |
| C4 Defines success/completion criteria | MET | 3. Target State (L522) "Success criteria: Each statement is a pass/fail test a later task can run", SC-1..SC-23 (L526-548) | MET | 3.3 Success criteria (testable facts) SC-01..SC-33 (L1171-1209); 8.2(d) acceptance conditions AE-1..AE-15 (L4527-4549) |
| C5 Specifies what is explicitly out of scope | MET | Header (L7) "**Scope note:** report only; no roadmap"; K-11 (L564) "Scope of this run: report only; E2 is read only at commit 4a22d74..."; 8 intro (L3101) "it contains no dates, sprints, ordering commitments or `/sc:workflow` plan" | MET | 3. Target State (L1123) "This section states the target, not a plan: no sequencing, branches, PRs, risks or estimates"; 8.2 (L4412) "contains no roadmap, no branch plan, no PR plan, no risk register, no estimate and no schedule"; 4.5 Findings excluded (L1472) |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| K1 No factual errors or hallucinated claims | NOT MET | 2.4 test surface (L381) "`tests/cli/reflect` has 37 files and 353 tests" (re-collected: 38 files; V1's own L3734 "resolved: 38 files (R12's 37 is superseded)"); BL-12 (L616) "43 spawning call sites in 11 skill files" (not reproducible by the census command: 52 lines in 11 files, orchestrator verification X-022/X-029/X-061, unit unstated) | NOT MET | G-01 (L1236) "A v2 citation-only finding raises `KeyError: 'anchor'` in `findings.annotate` ..., which `ledger.merge_round` calls" (orchestrator verification X-020/X-049/X-053: v1 `parse_block` rejects the line first); 5.1 AE-1 (L1647-1648) cites arXiv 2606.19544, withdrawn; G14 (L4479) "50 test files" in `tests/pr_submit/` (47) |
| K2 Technical approaches are feasible with stated constraints | MET | 7 Recommendation (L2823) "Option B ... built *through* Option A's code ... closed tuples ... move into data registries only as each consumer needs them"; 6.X condition (L2620) states the risk holds only if C-03/C-05/C-13/C-14 settle; K-1..K-11 (L554-564) state the limits each design must keep (contract 1.8.0, `.claude/` rule, uv) | MET | 7 Recommended approach (L3578) thin shared contract with per-module engines in the existing `cli/review/` package, "the core launches nothing"; F-1..F-6 (L3623-3628) "Verified facts that bound the design"; constraints C1-C29 (L4430-4458) each with "Consequence for a later plan" |
| K3 Terminology used consistently and accurately | NOT MET | `C-nn` means a Section 6 conflict (7 Conventions, L2817 "`C-nn` = conflict of synth-04 Section 6") but a closed item in Section 9 (L4126 "`Cnn` = closed item of its section 4"); the same conflicts are written both `C-02` and `C02` (6.D L2523 "Decided (C02, C15)") | NOT MET | `C-1 to C-12` = R01 conflicts (L128), `C-01..C-15` = debate slots (L3590), `C1..C29` = binding constraints (L4430-4458); `G1-G3` = table gates and also C-07 launcher gates (L4449 "not the rows G1 to G3 of table (b)"); `D-1` = a reproduced defect (L3639) while `D1` = decided fixes (L3643) and `D1..D26` = dependency facts (L4500) |
| K4 No internal contradictions | NOT MET | 2.4 (L381) and DOC row (L705) say `tests/cli/reflect` has 37 files; 8.1 row (L3734) and gate G9 (L4045) say 38 ("the remaining 34 of the 38 test files") | NOT MET | Rationale axis 1 (L3636) "a v2 citation-only line is rejected at `findings.py:104` before it can reach `annotate`" vs axis 2 in the next row (L3637) "a v2 citation-only line crashes the v1 ledger path with `KeyError 'anchor'`"; SC-17 (L1193) "convergence threshold ... (decision, 0.75 or 0.80)" vs delta table (L1137) "The convergence threshold is decided by the code: 0.80" |
| K5 Claims supported by evidence or rationale | MET | 2. Citation key (L108-123) and verification tags (L127) "[CODE-VERIFIED] = the research file read the code"; gap rows cite file:line, e.g. D2 (L590) "clearing loop `ledger.py:254-258` never reads `block_ok`" | MET | Baseline and Conventions (L108-116) tag rules "Only these claims are stated as current"; F-1..F-6 (L3623-3628) each with "[CODE-VERIFIED]" source; 8.2(a) C1 (L4430) "`panel_lint.py:185` (version), `:33` (stable list)" |
| **Subtotal** | **2/5** | | **2/5** | |

### Structure

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| S1 Logical section ordering (prerequisites before dependents) | MET | Headings (L91, L106, L481, L579, L783, L1154, L2808, L3099, L4124, L4388): problem, current state, target, gaps, external, options, recommendation, plan, open questions, evidence; the citation key comes first in Section 2 (L108) | MET | "Baseline and Conventions" (L104) defines tags and sources before Section 1; Sections 1-10 (L124 ... L4847) in the same order; appendices last (L5072, L5076) |
| S2 Consistent hierarchy depth (no orphaned subsections) | NOT MET | Section 3 has one numbered child only, "### 3.1 External context" (L566), after unnumbered blocks; Section 6 mixes "### 6.0" (L1166), unnumbered "### C-01 ..." to "### C-20 ..." (L1191-L2451), "### 6.D" (L2517), "### Options Comparison" (L2608) at one level | NOT MET | "### 7.0.1 Name, owner wording ..." (L3580) with no 7.0 heading; unnumbered "### Rationale: the 11 decision axes" (L3630) and "### Choices the evidence cannot decide" (L3648) between 7.0.1 and 7.1; six unnumbered ### siblings between 6.11 and 6.12 (L3004-L3100) |
| S3 Clear separation of concerns between sections | MET | Each section states its job and stays in it: Section 6 (L1158) "This is required report content (c): the conflict log ... contains no roadmap"; Section 8 (L3101) value capture and migration only; Sections 3-4 and 7 agree, so no override layer exists | NOT MET | The target state is split between Sections 3-4 and Section 7: "Where a target statement in Section 3 ... differs from an adjudicated outcome in Section 7, **Section 7 governs**, and the Section 3 or 4 wording is withdrawn, narrowed or replaced" (L1125), a 16-row override table (L1127-1144); Section 7 also carries research-file contradictions (L3877) duplicating 4.3 (L1424) |
| S4 Navigation aids present | MET | Table of Contents (L11-85) with anchors to every subsection; reading note (L87) maps synth files to sections; 9.1 Gap coverage index (L4183) | MET | Table of Contents (L10-99) with anchors; precedence note (L120) and delta table (L1125) cross-reference Section 7; 8.1.2 points to Appendix A rows (L4278) |
| S5 Follows conventions of the artifact type (ten-section research report) | MET | Ten numbered sections 1-10 (Grep of `^## `: L91-L4388) with Problem Statement, Current State, Target State, Gap Analysis, External Research, Options, Recommendation, Implementation Plan, Open Questions, Evidence Trail | MET | Ten numbered sections 1-10 (L124-L4847) with the same names, Section 8 titled "Value Inventory and Inputs for a Later Plan" (L4234); appendices A and B added after Section 10 |
| **Subtotal** | **4/5** | | **3/5** | |

### Clarity

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| L1 Unambiguous language | MET | Whole-file grep: "should consider" 0, "might" 0, "as appropriate" 0, "perhaps" 0, "possibly" 1 (L2658, inside a quoted debate row); claims are stated as rules, e.g. SC-2 (L527) "a round that rejected a blocking line cannot compute PASS" | MET | Whole-file grep: "should consider" 0, "might" 0, "as appropriate" 0, "perhaps" 0, "possibly" 6 (L1298, L1770, L1855, L2335, L4160, L4793, all in evidence or question cells); rules stated flatly, e.g. axis 4 (L3639) "silence never clears" |
| L2 Concrete rather than abstract | MET | 8.3 G2 (L4038) names the exact test line, assertion and replacement: "`:385` (`status(led)["L1"] == "resolved"`) becomes `== "resolved_check"`"; 8.6 (L4106) exact `uv run pytest --collect-only` command | MET | 8.2(b) G7 (L4472) "`uv run python scripts/reflect_shadow_exit.py` ... prints `OVERALL: FAIL (shadow runs 13 of 20)`"; C4 (L4433) the exact git error text and exit 128 |
| L3 Each section has a clear purpose or one-sentence summary | MET | Section 5 (L785) "supplementary external context ... codebase findings take precedence"; Section 6 (L1158) "Scope of this section ... the conflict log"; Section 8 (L3101) owner-scope purpose; Section 9 (L4126-4130) source key and severity basis | MET | Section 3 (L1123) "Question this section answers"; Section 6 (L2140) "one block per decision axis ... the recommendation is Section 7"; Section 8 (L4236) "Both are inputs for a later plan"; Section 9 (L4697) "How to read the table" |
| L4 Acronyms and domain terms defined on first use | NOT MET | Section 1 (L101) uses "control C8" before Section 4 defines it (L581); "UC-1" first used (L152) and never expanded; "GT" (L3133) and "SARIF" (L575) not expanded; Section 1 defers its shorthands to Section 2 (L104) | NOT MET | Section 1 (L135) uses "decision DO4" and "reflect UC-1" undefined; "GT" first used (L290) without expansion; "C8" appears in the ToC (L32) and Section 3 rubric (L1121) as "rule C8" without a definition at first use |
| L5 Actionable next steps or decision points clearly identified | MET | 8.6 Integration Checklist (L4103-4120) checkbox actions with commands; L4120 "Hand the owner-decision list (O-1 to O-6, Decision D-1, ...) to Section 9 ... and mark the steps that wait on each"; 9.5 open decisions (L4366) | MET | 9 Open Questions tables with `Suggested Resolution` and OWNER-DECISION tags (L4697); 9.8 (L4772) "Q-36 OWNER-DECISIONS carried from the rows above, to be put to the owner together"; 9.10 debate-derived questions Q-38 to Q-93 (L4784) |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| R1 At least 3 risks with probability and impact assessment | MET | 8.5 Risk register inputs (L4071-4101), 25 rows with Likelihood and Impact columns, e.g. L4078 "Blind grader accuracy is unmeasured ... \| High \| High"; L4073 "Likelihood and impact are qualitative readings of the cited evidence (Low / Medium / High)" | NOT MET | No risk list with probability and impact. 8.2 (L4412) "contains ... no risk register"; Section 8 (L4236) "Neither is ... a risk register"; the per-option "Risk" rows rate one combined level and are defined as "Not a risk register" (Reading guide, L2154); 7.3 invariants carry a severity only (L3964) |
| R2 Mitigation strategy for each identified risk | MET | 8.5 Mitigation column on every row, e.g. L4085 "HEAD-relative pins C1, C6, C14 pass trivially ... \| Absolute pin (M2-01); G8 run before committing"; L4100 persisted-format risk "Compatibility rule per persisted format ..., reload tests per step" | NOT MET | No per-risk mitigation: per-option Risk rows (e.g. L2189, L2353) give only a basis; 7.3 invariants are left OPEN (L3962 "Every invariant that a debate's invariant probe ... left unaddressed is listed here"); axis "Trade-off accepted" cells (L3636-3646) accept consequences rather than mitigate them |
| R3 Failure modes and recovery procedures | MET | 8.2 M1 (L3828) "Rollback: each step is one change that can be reverted alone ... revert in reverse dependency order, run G1 to G11 and G-exit"; Rollback (M2) L3861, (M3) L3880, (M4) L3898; 8.4 (L4061) "The rollback unit in every layout is one merged PR" | MET | Axis 3 (L3638) "a fail-closed refusal with an acknowledgement exit when a blocking line was dropped; one bounded stateless re-ask"; C22 (L4451) "If M1 fails, the SKILL steps and the gate do not ship and `identity_source` stays `requested-pinned`"; axis 5 (L3640) "if G2 fails the end state is Variant 2's" |
| R4 External dependencies and their failure scenarios | MET | 8.5 L4083 "Served-model drift: a 'haiku' slot served by `gpt-6.1-sol` ..."; L4091 "`ccsession-models.json` is fetched live from master at launch"; K-10 (L563) "alias routing can change with Coder or ccsession config" | MET | Axis 5 (L3640) "Claude Code behaviours the repo does not pin (the Agent enum, `resolvedModel`, `message.model` truthfulness after shim failover) are assumed stable"; C9 (L4438) "GitHub stacked PRs ... cross-fork stacks are not supported"; C4 (L4433) git ref clash, "Remote-side behaviour was not tested" |
| R5 Monitoring or validation mechanism for risk detection | MET | 8.3 G-exit (L4051) "its result must not worsen"; G-bench (L4054) "until then no quality claim about a decider ... is made"; SC-4 (L529) "a launch/observed mismatch fails a built-in check" | MET | 8.2(b) G7 (L4472) Stage 2 exit baseline; G23 (L4488) "the identity gate in `scripts/reflect_shadow_exit.py` reads events read-only"; AE-7 (L4541) Tier S checks run in code (conservation, served = requested) |
| **Subtotal** | **5/5** | | **3/5** | |

### Invariant & Edge Case Coverage

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| E1 Boundary conditions for collections (empty, single, maximum) | MET | 6.E C13-06 (L2641) "a lone reviewer has quorum 1 ..., a panel of 3 has quorum 2 ... an empty reviewers list giving quorum 0"; C13-05 (L2640) "v1 treats an empty block as valid"; SC-6 (L531) "no connected component above the size cap survives unsplit" | MET | 8.2(c) D26 (L4525) "treats an empty legacy baseline as 0.0"; axis 7 (L3642) "one finding plus zero rows is valid"; axis 4 (L3639) "the re-review panel is one reviewer, so `min(Q, requested)` applies" |
| E2 State-variable interactions across component boundaries | MET | D2 (L590) "clearing loop `ledger.py:254-258` never reads `block_ok`" (state set at merge, ignored at clearing); SC-4 (L529) "`requested`, `launch` and `observed` model ... `requested` is never overwritten" | MET | CT-3 (L3612) "One `requested` count per round is needed by all four; none of the four debates fixes where it comes from when `--resolution` is absent"; CT-4 (L3613) identity `unrecorded` keeps "accepted" unreachable |
| E3 Guard-condition gaps (missing validation, unguarded assumptions) | MET | D13 (L2535) "`__init__.py:19-36` swallows `ModuleNotFoundError`"; D16 (L2538) "`--cap` reaches the ledger only on round 1 ... `merge_round` requires only `n == len(rounds)+1`"; D12 (L2534) "nothing checks that a template's `tier2b` alias exists" | MET | Axis 8 (L3643) "`manifest.py:285-291` checks the hash format only"; D20 (L4519) "`lint_cmd` and `estimate_cmd` are listed but absent"; axis 5 (L3640) "the raw-id `claude -p` lane is NOT read-only by construction ... leaves Bash open, `run-reviewer.sh:48`" |
| E4 Count-divergence scenarios (off-by-one, inclusive/exclusive) | MET | D16 (L2538) "Round 4 accepted ... `--round` help says '1, 2 or 3' while the type is `IntRange(min=1)`", fix "`merge_round(..., 4, ...)` raises when `cap_reviews == 3`"; C13-01 (L2636) "the fault-finder's own footer says '16 UNADDRESSED' but by its entries the count is 18" | MET | Axis 2 (L3637) "the 3-line clustering tolerance has different bases in the two engines (0-based half-open against 1-based inclusive: C-01 INV-009, open)"; AE-6 (L4540) "`fullpkg()` matches ids by a 12-character prefix ... (committed 69 reproduced; corrected 71 to 76)" |
| E5 Interaction effects when features or components combine | MET | Rationale 7 (L2833) "source injection of C-10 multiplies source tokens by the reviewer count ... it interacts with D-1"; "the class-disjoint set is empty only with the three-reviewer default (sonnet, haiku, opus)" | MET | 7.0.1 tensions CT-1 to CT-6 (L3608-3615), e.g. CT-5 "Under H+ a dropped-criterion class typed MAJOR with `blocking: false` is not floored"; "Interactions between axes" (L3043) |
| **Subtotal** | **5/5** | | **5/5** | |

Floor rule: both variants score 5/5 here, so neither is ineligible as base.

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness | 5/5 | 5/5 |
| Correctness | 2/5 | 2/5 |
| Structure | 4/5 | 3/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.833** | **22/30 = 0.733** |

### Edge Case Floor Check

Invariant & Edge Case Coverage: Variant 1 5/5, Variant 2 5/5. Both exceed the 1/5 floor; neither is ineligible as base.

## Position-Bias Mitigation

Pass 1 evaluated Variant 1 first, pass 2 evaluated Variant 2 first. Of 60 criterion-variant pairs the passes agreed on 59 and disagreed on 1 (the pass 1 cells for V2 R1 and R2 did not parse as a bare MET/NOT MET in the automated comparison; the pass 1 scorer's summary and pass 2 both record NOT MET for them, so they are counted as agreement).

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| C1 | V1 | MET | MET | agree | MET |
| C1 | V2 | MET | NOT MET | DISAGREE | MET (re-evaluated, see below) |
| C2 | V1 | MET | MET | agree | MET |
| C2 | V2 | MET | MET | agree | MET |
| C3 | V1 | MET | MET | agree | MET |
| C3 | V2 | MET | MET | agree | MET |
| C4 | V1 | MET | MET | agree | MET |
| C4 | V2 | MET | MET | agree | MET |
| C5 | V1 | MET | MET | agree | MET |
| C5 | V2 | MET | MET | agree | MET |
| E1 | V1 | MET | MET | agree | MET |
| E1 | V2 | MET | MET | agree | MET |
| E2 | V1 | MET | MET | agree | MET |
| E2 | V2 | MET | MET | agree | MET |
| E3 | V1 | MET | MET | agree | MET |
| E3 | V2 | MET | MET | agree | MET |
| E4 | V1 | MET | MET | agree | MET |
| E4 | V2 | MET | MET | agree | MET |
| E5 | V1 | MET | MET | agree | MET |
| E5 | V2 | MET | MET | agree | MET |
| K1 | V1 | NOT MET | NOT MET | agree | NOT MET |
| K1 | V2 | NOT MET | NOT MET | agree | NOT MET |
| K2 | V1 | MET | MET | agree | MET |
| K2 | V2 | MET | MET | agree | MET |
| K3 | V1 | NOT MET | NOT MET | agree | NOT MET |
| K3 | V2 | NOT MET | NOT MET | agree | NOT MET |
| K4 | V1 | NOT MET | NOT MET | agree | NOT MET |
| K4 | V2 | NOT MET | NOT MET | agree | NOT MET |
| K5 | V1 | MET | MET | agree | MET |
| K5 | V2 | MET | MET | agree | MET |
| L1 | V1 | MET | MET | agree | MET |
| L1 | V2 | MET | MET | agree | MET |
| L2 | V1 | MET | MET | agree | MET |
| L2 | V2 | MET | MET | agree | MET |
| L3 | V1 | MET | MET | agree | MET |
| L3 | V2 | MET | MET | agree | MET |
| L4 | V1 | NOT MET | NOT MET | agree | NOT MET |
| L4 | V2 | NOT MET | NOT MET | agree | NOT MET |
| L5 | V1 | MET | MET | agree | MET |
| L5 | V2 | MET | MET | agree | MET |
| R1 | V1 | MET | MET | agree | MET |
| R1 | V2 | NOT MET | NOT MET | agree | NOT MET |
| R2 | V1 | MET | MET | agree | MET |
| R2 | V2 | NOT MET | NOT MET | agree | NOT MET |
| R3 | V1 | MET | MET | agree | MET |
| R3 | V2 | MET | MET | agree | MET |
| R4 | V1 | MET | MET | agree | MET |
| R4 | V2 | MET | MET | agree | MET |
| R5 | V1 | MET | MET | agree | MET |
| R5 | V2 | MET | MET | agree | MET |
| S1 | V1 | MET | MET | agree | MET |
| S1 | V2 | MET | MET | agree | MET |
| S2 | V1 | NOT MET | NOT MET | agree | NOT MET |
| S2 | V2 | NOT MET | NOT MET | agree | NOT MET |
| S3 | V1 | MET | MET | agree | MET |
| S3 | V2 | NOT MET | NOT MET | agree | NOT MET |
| S4 | V1 | MET | MET | agree | MET |
| S4 | V2 | MET | MET | agree | MET |
| S5 | V1 | MET | MET | agree | MET |
| S5 | V2 | MET | MET | agree | MET |

Disagreements re-evaluated: 1 (C1, Variant 2). Final verdicts changed from pass 2: 1 (NOT MET to MET). Re-evaluation (`partials/qual-reeval.md`, verdict FINAL): MET, because Variant 2 carries migration content as unordered inputs (dependency facts D1-D26 at V2:4494-4526 and 'Files and modules a later plan will touch' at V2:4551 onward); what it refuses at V2:4236 and V2:4412 is only an ordered roadmap, branch plan or PR plan.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker (points won in Step 2) |
|---|---|---|---|---|
| 1 (run 1 report) | 0.4679 | 0.4167 | **0.8845** | 33 of 234 = 14.1% |
| 2 (run 2 report) | 0.4953 | 0.3667 | **0.8620** | 123 of 234 = 52.6% |

**Margin**: 0.0225 absolute (2.5% of the higher score), Variant 1 ahead, below the 0.05 threshold.
**Tiebreaker applied**: Yes (level 1, debate performance). Points won in Step 2: Variant 2 won 123 points, Variant 1 won 33, 64 were `Both (merge)`, 6 open and 8 still split. Variant 2's lead (52.6% vs 14.1% of the 234 points) is far outside the 5% band, so level 2 and level 3 were not needed. Evidence: `debate-transcript.md` Scoring Matrix.

Reading the numbers honestly: the combined score gives Variant 1 a narrow lead (0.885 vs 0.862) because the qualitative rubric rewards a risk register (R1, R2) and a visible migration path that Variant 2 deliberately omits (its Section 8 is an inputs pack, not a plan) and Variant 1's section-reference completeness is lower on the quantitative layer (DC 0.795, SC 0.786 vs 0.955 and 1.000). The debate, which examined 234 points against the code, favours Variant 2 on the design content, the fact base, the later E2 evidence and the constraint, gate and acceptance inventory; Variant 1 wins the verified fact disputes and carries content (migration steps, gate replacement assertions, rollback rules, panel-size decision) that must be merged in. Both quantitative IC and SR are near 1.0 for both reports and barely discriminate; RC is 1.0 for both. Qualitative K1 and K4 are NOT MET for both (verified errors in each).

## Selected Base: Variant 2 (run 2 report, `RESEARCH-REPORT-review-panel-unification-run2.md`)

### Selection Rationale

1. Tiebreaker level 1 (debate performance): Variant 2 won 123 of 234 diff points and Variant 1 won 33 (64 needed both reports). The independent fault-finder found no verified fact that contradicts the consensus verdicts.
2. The governing design shape in the consensus is Variant 2's (a thin shared contract with per-module engines, adjudicated by 15 debates with their conditions), with Variant 1's superset-core detail carried as the recorded one-engine alternative.
3. Variant 2 reads the later E2 tip (6c09843, four commits after Variant 1's 4a22d74) and the E2 collaboration and process-redesign work that Variant 1 has no content for (V1 has 0 hits for 'collaborat' in V1:1-782).
4. Variant 2 has the binding-constraint (29), no-regression-gate (27), dependency-fact (26) and acceptance-condition (15) inventories, the 189-row conflict log, the 244-row debate invariant table and the 5,950-row value inventory that the later plan needs.
5. Merge feasibility: V2 is the larger, more structured document with a precedence table; insertions from V1 are additive blocks.
6. Variant 2 is not clean: it states a KeyError path the code does not have (V2:1236, 2177, 3882, 4508; verified false), cites a withdrawn paper (V2:1647-1648, 1655, 2044, 2829), and has several wrong counts. These are corrected in the merge (refactor-plan.md, Corrections).

### Strengths to Preserve from Base

- Baseline and Conventions section, verification tags, E2 tip pin and HEAD statement (V2:104-120).
- Section 2 depth: nine subsections including dispatch (2.6), consumers (2.7), evaluation harness, governance and repo constraints (2.8) and the capability overlap matrix 2.9 (V2:139-1111).
- Section 3 precedence/delta table (V2:1125-1144) and Section 4 gap table G-01..G-148 with the rule-C8 check and 4.6 carry-over (V2:1229-1537).
- Section 6 axes 6.1-6.11 and the 189-row conflict log 6.12 with the 15 adjudicated debates (V2:2138-3566).
- Section 7 adjudicated recommendation, invariants I-1..I-9, the 244-row debate-invariant table 7.3 (V2:3567-4233).
- Section 8 inputs for a later plan: 29 binding constraints, 27 gates, 26 dependency facts, 15 acceptance conditions, 24 open questions, and the pointer to the 5,950-row value inventory (V2:4234-4688); Section 9 (93 questions with Source column) and Section 10 evidence trail (V2:4689-5071).

### Strengths to Incorporate from Non-Base Variants

- From Variant 1 Section 8: the migration and value-capture content (8.1 inventory rows that are still valid, 8.2 steps re-based on the adopted design with the ordering removed, 8.3 no-regression gates with exact commands, collected counts and the 'must change on purpose' assertions, persisted-format compatibility and rollback rules, gap-to-step coverage map, 8.5 risk inputs as inputs not a register).
- From Variant 1 Section 6 and 6.E: C-14 panel size and cost (with its invariants and Q-47..Q-50), calibration (C-06), per-lens blocking predicate (C-16), missing-anchor handling (D5), brief renderer (C-10), `panel verify` (C-03), reviewer read-only decision (C-18) with the corrected restriction flags, and the implementer-facing 6.E decision tables.
- From Variant 1 Sections 2-4: the D1-D16 defect status table with the 'Reflect v2 shares it?' column, post-gate engine defects ENS-1..ENS-9 (unauthorized_deviation_present has no producer, REPORT.md and per-task matrix never produced, merge_method not carried by the installed adversarial contract), per-row Track tags, SC pass rules (SC-6, SC-10, SC-18..SC-22), K-10 dated runtime facts.
- From Variant 1 Section 5: severity taxonomy research (5.2), calibration methods and judge bias (5.3), fingerprinting and clustering research (5.4), production-system evidence (5.1) with the source options lists; both reports' external sets are disjoint and both are carried, minus the withdrawn arXiv 2606.19544 figures.
- From Variant 1 Section 9: owner items O-1..O-6 as questions, closed items and the 77-row stale-documentation register, with ids namespaced by report.
- Corrections found by the debate and the fault-finder that apply to the base (KeyError path, 6-vs-5 calibrator dimensions, 0.704 definition, cluster_agreement, 1,398 unit, counts with units).
