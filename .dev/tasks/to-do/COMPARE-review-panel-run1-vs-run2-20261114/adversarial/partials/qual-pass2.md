# Qualitative Scoring, Pass 2 of 2 (reverse order: Variant 2 judged first, then Variant 1)

- Scorer: independent scorer, pass 2. Not an advocate. partials/qual-pass1.md was not read.
- Variant 2 = adversarial/variant-2-original.md (run 2, 5,098 lines). Variant 1 = adversarial/variant-1-original.md (run 1, 4,476 lines).
- Rubric: 30 binary criteria, 6 dimensions x 5. MET = 1, NOT MET = 0. Every MET carries a heading + line citation in the variant itself.
- Method: for each criterion Variant 2 was judged first, then Variant 1. Evidence index files (diff-analysis.md, debate-transcript.md, invariant-probe.md) were used only to locate lines; every cited line was re-read in the variant.
- Column order in the tables follows the required template (Variant 1 columns first); the judging order was Variant 2 first.
- Dimensions were written last to first: Invariant & Edge Case, Risk, Clarity, Structure, Correctness, Completeness.

## Invariant & Edge Case Coverage

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| E1 Collection boundaries (empty, single, max) | MET | 3. Target State, SC-3 (L528): "add quorum boundary test (k-1 fails, k passes)"; 6.E C13-06 (L2641): "a lone reviewer has quorum 1 ... an empty reviewers list giving quorum 0"; SC-6 (L531): "no connected component above the size cap survives unsplit" | MET | 2.5 defect table (L554): "1 valid empty block of 4 dispatched gives verdict PASS and exit 0"; 6.4 Option Pros (L2409): "Fail-closed at the 0-valid boundary is intentional and tested"; 3.3 SC-24 (L1200): "treats an empty baseline as 'no baseline'" |
| E2 State-variable interactions across components | MET | 6.E C13-22 INV-014 (L2657): "an older installed binary would continue a new-key ledger with the old rules (silence clears, re-find un-blocks) while the file still looks valid"; 8.2 persisted formats (L3830) | MET | 7.3 C-01 INV-002 (L3988): "adding `T<PP>.<TT>` to the shared token list leaves ledgers already on disk behaving the same"; 8.2(a) C21 (L4450): "any packaged-file edit changes `tiers_sha256`, after which `recompute_parity` reports earlier runs as not proven" |
| E3 Guard-condition gaps | MET | 6.E C13-06 (L2641): "the merge refuses a report id not in it, a `review_kind` that does not match the round ... and an empty list"; 8.3 G2 (L4038): "the invalid reviewer `t2-1` cannot clear the row (D2/D3)" | MET | 4. Gap table G-132 (L1367): "A two-token fence info string (`json findings-v1`) is not matched (`findings.py:27`)"; G-12 (L1247): "`block_ok` not consulted"; 8.2(a) C4 (L4433): both names "pass `git check-ref-format --branch` individually ... the failure appears only at ref creation" |
| E4 Count divergence (off-by-one, inclusive/exclusive) | MET | 8.3 G1 (L4037): "an anchor of 201 characters (`:113`) and a claim of 301 (`:117`) ... at most 200 ... at most 300"; SC-3 (L528) k-1 vs k quorum boundary | MET | 7.3 C-01 INV-009 (L3991): "the 3-line clustering tolerance means the same thing in both engines (0-based half-open against 1-based inclusive)" |
| E5 Interaction effects when components combine | MET | 8.5 (L4095): "All-reviewer source injection ... interacts with Decision D-1"; 7. Rationale 2 (L2828): B "depends on the four debate-resolved (`partial`) conflicts" | MET | 6. "Interactions between axes" heading (L3043); 8.2(a) C26 (L4455): "Reopened together with C-01, C-02 or C-03 if one of them is reopened" |
| **Subtotal** | **5/5** | | **5/5** | |

Floor rule: both variants score above 1/5 here, so both stay eligible as base.

## Risk Coverage

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| R1 At least 3 risks with probability and impact | MET | 8.5 Risk register inputs (L4073-4101): table with "Likelihood" and "Impact" columns, 25 rows, e.g. L4083 "Served-model drift ... High / High", L4085 "HEAD-relative pins ... High / High" | NOT MET | 6. Reading guide (L2154): per-option "Risk (Low, Medium, High) ... how likely ... Not a risk register" (one likelihood rating, no separate impact); 8. intro (L4236) and 8.2 scope (L4412): "no risk register"; 7.3 (L3983) gives severity only, no probability. Searched Sec 6, 7.3, 8 |
| R2 Mitigation for each identified risk | MET | 8.5 (L4075): "Mitigation" column filled on every row, e.g. L4085 "Absolute pin (M2-01); G8 run before committing" | NOT MET | 6.1 Option A aspect table (L2186-2193): rows Effort, Risk, Reuse, Files, Pros, Cons; no mitigation per risk; 7.3 status key (L3983): "no listed invariant was resolved"; all 60 HIGH rows OPEN. Searched Sec 6.1-6.11 option tables, 7.3, 8.2 |
| R3 Failure modes and recovery procedures | MET | 8.2 "Persisted formats and rollback" (L3830): "revert in reverse dependency order, run G1 to G11 and G-exit, and confirm the 13 recorded shadow manifests still validate" | MET | 2.5 (L553-556): reproduced failure modes D-1, D-2, D-11; 3.1 T-6 (L1155): collaboration "behind a kill switch whose off state is byte-comparable to the isolated panel"; 8.2(a) C15 (L4444): legacy file not replaced "before the replay shows no verdict difference" |
| R4 External dependencies and their failure scenarios | MET | 8.5 (L4083): "a 'haiku' slot served by `gpt-6.1-sol`, combo A3 collapsed to sonnet"; L4091: "`ccsession-models.json` is fetched live from master at launch" | MET | 3.3 SC-09 (L1185): "a run in which three reviewers are served one model (combo A-r3)"; 8.2(a) C9 (L4438): "[WEB] W03 D1 ... cross-fork stacks are not supported" |
| R5 Monitoring or validation mechanism | MET | 8.3 No-regression gate list (L4031-4055), e.g. G-exit (L4051) "its result must not worsen"; 8.6 checklist (L4117) | MET | 8.2(b) No-regression gates G1-G27 (L4466-4492), e.g. G7 (L4472) exit-script baseline "OVERALL: FAIL (shadow runs 13 of 20)" |
| **Subtotal** | **5/5** | | **3/5** | |

## Clarity

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| L1 Unambiguous language | MET | Whole-file Grep: 0 hits for "might", "should consider", "as appropriate", "perhaps"; e.g. 8.3 (L4033): "A gate is 'green' when its command exits 0 with the stated collected count" | MET | Whole-file Grep: 0 hits for "might", "should consider", "as appropriate", "perhaps"; e.g. 3.3 (L1173): "Each criterion is a check that returns a fact" |
| L2 Concrete rather than abstract | MET | 8.3 G2 (L4038): exact command `uv run pytest tests/review/test_review_ledger.py ...` and the assertion `:385` that "becomes `== \"resolved_check\"`" | MET | 8.2(b) G1 (L4466): `uv run pytest tests/cli/reflect/test_verdict_mapping.py` (36 tests); 3.3 SC-03 (L1179) names the pins to rewrite |
| L3 Each section has a clear purpose | MET | 8. heading (L3099): "value-capture and migration plan; not a roadmap"; 8.5 (L4073): "Inputs for the risk register, not the register itself"; 3. (L494) "Desired behavior" sentence | MET | 6. (L2140): "one block per decision axis ... the recommendation is Section 7"; 8. (L4236): "the value inventory (8.1) and the sequence and gates (8.2)"; 3. (L1123): "This section states the target, not a plan" |
| L4 Acronyms and terms defined on first use | NOT MET | 1. Problem Statement (L101) uses "ENS-2" and "D1, D3, D4" before any definition (D1-D16 defined at L492, ENS/BL/MS only at L2817); L93 "(BR GOAL and WHY)" before the key at L115. Searched L1-130, L481-492, L2810-2817 | NOT MET | 1. Problem Statement (L135): "open decision DO4 ... stays on reflect UC-1" with neither DO4 nor UC-1 defined there or earlier (UC-1 next at L165, still undefined). Searched L1-140 and the Baseline key L104-120 |
| L5 Actionable next steps or decision points | MET | 8.6 Integration Checklist (L4105-4120), e.g. L4120 "Hand the owner-decision list (O-1 to O-6, Decision D-1 ...) to Section 9 ... and mark the steps that wait on each"; 9. table with "Suggested Resolution" (L4134) | MET | 9. (L4696): tags incl. OWNER-DECISION; table "Impact (what it blocks) / Suggested Resolution" (L4700-4702); 4.6 decision groups D-1..D-14 (ToC L36) |
| **Subtotal** | **4/5** | | **4/5** | |

## Structure

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| S1 Logical section ordering | MET | ToC (L13-85): 1 Problem, 2 Current State, 3 Target, 4 Gap, 5 External, 6 Options, 7 Recommendation, 8 Plan inputs, 9 Open Questions, 10 Evidence; citation key at head of 2 (L108) before its use in later sections | MET | ToC (L12-99): Baseline and Conventions (L104) defines tags and source key before Section 1; then sections 1-10 in the same order as V1; Section 3 opens with a "read this first" precedence table (L1125) |
| S2 Consistent hierarchy depth, no orphaned subsections | NOT MET | 3. Target State has one numbered child only, "### 3.1 External context" (L566), after unnumbered content (L494-564); Section 6 mixes "### 6.0" (L1166), "### C-01" ... "### C-20" (L1191-2451), "### 6.D", "### 6.X", "### Options Comparison", "### 6.E" (L2517-2624) | NOT MET | "### 7.0.1" (L3580) exists with no 7.0 heading; Section 7 mixes numbered 7.1/7.2/7.3 with unnumbered peers (L3630, L3648, L3850-3933); Section 10 has "### Appendix A" (L4926) and a separate "## Appendix A" (L5072) |
| S3 Clear separation of concerns | MET | 8. subsections each hold one concern: 8.1 inventory (L3105), 8.2 migration (L3822), 8.3 gates (L4031), 8.4 branches (L4057), 8.5 risks (L4071), 8.6 checklist (L4103); web material inside Sec 3 is fenced as "web research, not codebase fact" (L566) | NOT MET | The target state is split across two sections: 3. (L1125) "Where a target statement in Section 3 ... differs from an adjudicated outcome in Section 7 ... Section 7 governs" (16-row override table L1127-1144); open questions are spread over Sec 2 "Not verified" blocks (e.g. L339), Sec 6 "Open questions" (L3080), Sec 7 [UNVERIFIED] list (L3913) and Sec 9 |
| S4 Navigation aids | MET | Table of Contents (L11-85) with anchors; 9.1 Gap coverage index (L4183) | MET | Table of Contents (L10-99) with anchors; 4.4 coverage table (L1446); Section 10 evidence index (L4847) |
| S5 Follows ten-section research-report conventions | MET | Ten numbered sections 1-10 (L91, L106, L481, L579, L783, L1154, L2808, L3099, L4124, L4388) | MET | Ten numbered sections 1-10 (L124, L139, L1112, L1229, L1538, L2138, L3567, L4234, L4689, L4847) plus a conventions preamble and two appendices |
| **Subtotal** | **4/5** | | **3/5** | |

## Correctness

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| K1 No factual errors or hallucinated claims | NOT MET | 2.4 Test surface (L381): "`tests/cli/reflect` has 37 files" (verified 38 test files; invariant-probe INV-012); 8.5 (L4092): "43 call sites in 11 skill files", not reproducible by the census command, which gives 52 lines in 11 files (diff-analysis orchestrator table, X-022) | NOT MET | 6.1 shared facts (L2177): "a v2 citation-only finding crashes the v1 ledger path (`KeyError: 'anchor'` ...)", while `findings.py:104` rejects the line first (orchestrator table X-020/X-049: VERIFIED-V1); 5.1 source line (L1648) cites `arxiv.org/html/2606.19544v1`, a paper arXiv shows as withdrawn, carried into takeaway 1 (L2044); 8.2(b) G14 (L4479): "50 test files" in `tests/pr_submit/` (verified 47) |
| K2 Technical approaches feasible under stated constraints | MET | 7. Rationale 4 (L2830): decided conflicts built as written, the four `partial` debates "carried as open design risks ... not as solved questions"; constraints K-1..K-11 (L552-564) keep contract 1.8.0 frozen | MET | 3. precedence row T-2 (L1130): "no engine moves now; engine A's ensemble stays production Tier 2"; binding constraints C1-C29 (L4430-4458) each with "Consequence for a later plan" |
| K3 Terminology used consistently | NOT MET | The same id names different things: "C-01" is a conflict in 7. (L2839) and a closed gap-log item in 9.3 (L4266); "C1" is also a contract pin in K-1 (L554) | NOT MET | "AE-1" is a web finding in 5.1 (L1647: "[AE-1] Raw agreement overstates reliability") and an acceptance condition in 8.2 (L4535: "AE-1 One ground-truth registry"); "G1 to G3" is used for two different gate sets (L4449: "not the rows G1 to G3 of table (b)") |
| K4 No internal contradictions | NOT MET | 2.4 (L381): "`tests/cli/reflect` has 37 files" vs 8.3 G9 (L4045): "the remaining 34 of the 38 test files" | NOT MET | 7. axis 1 (L3636): a v2 citation-only line "is rejected at `findings.py:104` before it can reach `annotate`" vs 7. contradictions row C-2 (L3882) and 8.2(c) (L4508): it "raises `KeyError 'anchor'`"; 3.3 SC-17 (L1193) "decision, 0.75 or 0.80" vs the same section's precedence row (L1137) "decided by the code: 0.80" |
| K5 Claims supported by evidence or rationale | MET | 2. (L129): "Every statement below traces to a code read recorded in a research file"; rows carry file:line, e.g. K-1 (L554) `panel_lint.py:33,146,184,...` | MET | Baseline (L114): only [CODE-VERIFIED] claims "are stated as current"; 6. Reading guide (L2151-2152); rows carry file:line, e.g. C3 (L4432) `contract.py:321` |
| **Subtotal** | **2/5** | | **2/5** | |

## Completeness

Source requirements used: the question (one unified Review Panel, shared core plus thin modules, from E1, E2, E3, keeping PR review and rf-qa replacement unblocked), the ten-section report shape, and what a later /sc:workflow plan needs (value-capture and migration content, no-regression gates, constraints, open questions with owner decisions).

| Criterion | Variant 1 | Evidence (V1) | Variant 2 | Evidence (V2) |
|---|---|---|---|---|
| C1 Covers all explicit requirements | MET | 1. (L93) the question incl. PR review and rf-qa; 8.1 value inventory (L3105); 8.2 Migration path (L3822); 8.3 gates (L4031); constraints K-1..K-11 (L552-564); owner items O-1..O-6 and Q-47..Q-61 (L4120) | NOT MET | Value capture, gates, constraints and owner decisions are present (8.1 L4238, 8.2(b) L4460, 8.2(a) L4426, 4.6), but migration content is refused: 8.2 (L4412) "It contains no roadmap, no branch plan, no PR plan ... It orders no work"; 8. (L4236) "Neither is a roadmap, a branch plan, a PR plan"; Grep "migrat" in Sec 8 (L4234-4688): 0 hits. Searched Sec 7.1, 8.1, 8.2(a)-(e) |
| C2 Edge cases and failure scenarios | MET | 3. SC-2 (L527): "a round that rejected a blocking line cannot compute PASS"; SC-3 (L528) quorum boundary | MET | 3.3 SC-03 to SC-07 (L1179-1183), e.g. SC-04 "fewer valid blocks than the declared quorum ... does not yield PASS" |
| C3 Dependencies and prerequisites | MET | 7. Rationale 2 (L2828): B "depends on the four debate-resolved (`partial`) conflicts"; SC-14 (L539): "non-core prerequisites are listed in the M4 Dependencies" | MET | 8.2(c) Dependency facts (L4494-4498): "'X must exist before Y' means: Y cannot work, pass a gate or be reached without X" |
| C4 Success / completion criteria | MET | 3. Success criteria SC-1..SC-23 (L522-548): "Each statement is a pass/fail test a later task can run" | MET | 3.3 Success criteria SC-01..SC-33 (L1171-1209): "Each criterion is a check that returns a fact" |
| C5 Explicit out-of-scope | MET | Header scope note (L7): "report only; no roadmap"; K-11 (L564); 7.4 What stays unchanged (L3050); 8.4 (L4061): "commits to no order, date or sprint" | MET | 3. (L1123): "no sequencing, branches, PRs, risks or estimates"; 8.2 scope statement (L4412); 4.5 Findings excluded from the gap table (L1472) |
| **Subtotal** | **5/5** | | **4/5** | |

## Pass 2 Summary

| Dimension | Variant 1 | Variant 2 |
|---|---|---|
| Completeness | 5/5 | 4/5 |
| Correctness | 2/5 | 2/5 |
| Structure | 4/5 | 3/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 5/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **Total** | **25/30** | **21/30** |

Where the 4-point gap comes from: V1 has a real risk register with likelihood, impact and mitigation (8.5) and an actual migration path (8.2); V2 refuses both by design (L2154, L4412). V2 also loses S3 because its target state is overridden by Section 7 through a precedence table. Both lose K1, K3, K4 and L4 on verified errors, id collisions, internal count or claim contradictions, and ids used before definition. Both are eligible as base under the invariant floor rule (5/5 each).

## Coverage

Read in full with the Read tool:
- V2: L1-140 (header, ToC, Baseline and Conventions, Section 1); L1112-1229 (Section 3 incl. precedence table, 3.1-3.5); L2138-2207 (Section 6 intro, Reading guide, 6.1 Options A and B); L4410-4499 (8.2 scope, (a) C1-C29, (b) G1-G27, start of (c)); L4689-4702 (Section 9 intro and Q-01).
- V1: L1-130 (header, ToC, Section 1, Section 2 citation key); L481-580 (Section 3 incl. SC-1..SC-23, K-1..K-11, 3.1); L2808-2837 (Section 7 conventions, recommended approach, rationale 1-7); L4031-4135 (8.3, 8.4, 8.5, 8.6, Section 9 intro).

Read as single lines or excerpts (sed/grep on exact lines, re-checked against the claim):
- V2: L554, L1155, L1185, L1200, L1247, L1367, L1647, L1648, L2044, L2177, L2409, L3043 (heading), L3580 (heading), L3636, L3882, L3960-3991 (7.3 head, slot legend, status key, first rows), L4236, L4508, L4530-4535; heading map of all `##`/`###` lines.
- V1: L150, L381, L1211, L2641, L2657, L2839, L3060, L3830, L4266; heading map of all `##`/`###` lines.

Whole-file Grep checks: vague terms (might, should consider, as appropriate, perhaps: 0 hits in each); "Risk"/"likelihood"/"probability" in both; "KeyError" and "withdrawn" in V2; "43 call sites" and "3 of 3 slots" in V1; "migrat" in V2 (5 hits, none in Section 8); first use of EV-1, DO4, ENS-, MS-1, UC-1.

Sampled or not read: V2 Section 2 (L141-1111) except the lines above; Section 4 tables (L1229-1537) except G-12, G-132; Section 5 (L1538-2137) except L1647-1648 and L2044; Section 6.2-6.12 (L2208-3566) except L2409, L3043; Section 7 bodies (L3567-3959) except L3636 and L3882; 7.3 rows after L3991; 8.1 (L4238-4409); 8.2(c)-(e) after L4499 except L4508 and L4530-4535; Section 9 after Q-01; Section 10 and appendices (L4847-5098). V1 Section 2 (L131-480) except L150 and L381; Section 4 (L579-782); Section 5 (L783-1153); Section 6 (L1154-2807) except L1211, L2641, L2657; Section 7.1-7.4 (L2838-3098) except L2839 and L3060; 8.1-8.2 (L3105-4030) except L3830; Section 9 tables after L4135 except L4266; Section 10 (L4388-4476). For these, whole-document judgements rest on the cited sections plus the Grep checks listed above; diff-analysis.md, debate-transcript.md and invariant-probe.md were used only to locate lines, and their verdicts were not copied without re-reading the cited variant lines.

