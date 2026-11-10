# Base Selection Report

## Metadata
- Generated: 2026-11-08T18:59:26Z
- Step: 3 of 5 (/sc:adversarial Mode A, non-interactive, auto-approve)
- Variants: V1 = `variant-1-original.md` (reviewer-1, analyzer persona, sonnet; F1-F10). V2 = `variant-2-original.md` (reviewer-2, qa persona, haiku; QA-001-QA-005).
- Artifact type: reflect reviewer card (YAML deviation-audit card, mode `pre`) auditing `TASK-WF-spec-20261108-181640.md` ("plan:N") against `source.md` ("source.md:N").
- Protocol: `refs/scoring-protocol.md` A.1-A.5 (6 dimensions, 30 criteria). The Section 3 template shows 5 dimensions / 25; the scoring protocol's 30-criterion form is used, as the caller asked.
- "Source requirements" for RC = the plan's 12 tasks (caller's rule).

## Quantitative Scoring (50% weight)

### Computation details

**Requirement Coverage (RC).** Count of plan tasks (1-12) that at least one finding cites or names. Only entries under `findings:` count; `correctness_gaps_advisory`, `confirmed_ok` and calibrator text are excluded.

| Finding | Plan lines cited | Tasks touched |
|---|---|---|
| V1 F1 | plan:89, :104, :25; detail "Tasks 5, 6 and 10" | 5, 6, 10 |
| V1 F2 | plan:83, :86 | 5 |
| V1 F3 | plan:86, :110 | 5, 7 |
| V1 F4 | plan:110 | 7 |
| V1 F5 | plan:172 | 12 |
| V1 F6 | plan:171, :178 | 12 |
| V1 F7 | plan:173-174 | 12 |
| V1 F8 | plan:37, :41 | 1 |
| V1 F9 | plan:19, :155, :173 | 11, 12 |
| V1 F10 | plan:143-149 | 10 |
| **V1 union** | | **{1, 5, 6, 7, 10, 11, 12} = 7** |
| V2 QA-001 | plan:49, :52 | 2 |
| V2 QA-002 | plan:71, :74-77 | 4 |
| V2 QA-003 | coverage-matrix.json:230-239 (no plan line) | none (targets the coverage artifact; its calibrator: "Flaw in the coverage artifact, not the plan") |
| V2 QA-004 | plan:174 | 12 |
| V2 QA-005 | plan:103, :110-114 | 6, 7 |
| **V2 union** | | **{2, 4, 6, 7, 12} = 5** |

- V1 RC = 7/12 = 0.583. V2 RC = 5/12 = 0.417.

**Internal Consistency (IC).** Scorable claims = finding entries + advisory + confirmed_ok items + notes + calibrator per-finding reasons + calibrator notes/gaps. A contradiction = two claims in the same card that oppose each other on the same subject.

- V1 claims: 10 findings + 1 advisory + 7 confirmed_ok + 10 per_finding + 1 calibrator note = 29.
  V1 contradictions (4): F1 `class: Regression` vs calibrator note "F1/F7 are not Regressions"; F7 `class: Regression` vs the same note; F6 title "ambiguous" vs calibrator "badly placed, not ambiguous"; F9 "base-commit 2cb683f5 classification claim unverified" vs calibrator "base commit 2cb683f5 is named at source.md:199".
  IC = 1 - 4/29 = 0.862.
- V2 claims: 5 findings + 3 notes + 5 per_finding + 1 unraised gap = 14.
  V2 contradictions (1): QA-003 filed as a plan `Drift` finding vs its calibrator "Flaw in the coverage artifact, not the plan". (QA-001's calibrator note about source.md:154 qualifies the finding but does not oppose it; QA-004's "Fix proposal is a guess" judges the fix, not the finding.)
  IC = 1 - 1/14 = 0.929.

**Specificity Ratio (SR).** Statements = titles/finding texts, details, fixes, advisory, confirmed_ok, notes, calibrator reasons. Vague markers found by a case-insensitive grep for the protocol's vague list plus hedges (might, may, appropriate, as needed, properly, adequate, should consider, various, etc., best practice, likely, perhaps, can inflate, a guess).

- V1: 40 statements (10 titles + 1 detail + 10 fixes + 1 advisory + 7 confirmed_ok + 10 per_finding + 1 note); vague 2 (line 22 "may be absent in CI"; line 68 "can inflate"). SR = 38/40 = 0.950.
- V2: 19 statements (5 findings + 5 fixes + 3 notes + 5 per_finding + 1 gap); vague 1 (line 71 "a guess"). SR = 18/19 = 0.947.

**Dependency Completeness (DC).** Internal references = references to ids defined in the same card (external file:line citations and coverage-matrix row ids such as INF-006 are excluded per the protocol).

- V1: 10 per_finding keys (F1-F10) + 3 ids in the calibrator note (F1, F7, F10) = 13 references, 13 resolve. DC = 1.000.
- V2: 5 per_finding keys (QA-001-QA-005) = 5 references, 5 resolve. DC = 1.000.

**Section Coverage (SC).** The cards have no H2 headings; the analogue used is top-level YAML keys with block (list or map) values. Scalar keys (reviewer, persona, model_class, mode, grounding_root, verdict, self_confidence) are metadata lines and excluded.

- V1: findings, correctness_gaps_advisory, confirmed_ok, calibration = 4. V2: findings, notes, calibration = 3. Max = 4.
- V1 SC = 4/4 = 1.000. V2 SC = 3/4 = 0.750.

### Quantitative table

| Metric | Weight | V1 (analyzer/sonnet) | V2 (qa/haiku) |
|--------|--------|----------------------|---------------|
| requirement_coverage | 0.30 | 0.583 (7/12 tasks) -> 0.1750 | 0.417 (5/12 tasks) -> 0.1250 |
| internal_consistency | 0.25 | 0.862 (4 of 29) -> 0.2155 | 0.929 (1 of 14) -> 0.2321 |
| specificity_ratio | 0.15 | 0.950 (38/40) -> 0.1425 | 0.947 (18/19) -> 0.1421 |
| dependency_completeness | 0.15 | 1.000 (13/13) -> 0.1500 | 1.000 (5/5) -> 0.1500 |
| section_coverage | 0.15 | 1.000 (4/4) -> 0.1500 | 0.750 (3/4) -> 0.1125 |
| **quant_score** | | **0.8330** | **0.7617** |

Sensitivity: counting V1's advisory (Task 4) gives V1 RC 8/12 and quant 0.8580; counting QA-003's fix target (Tasks 1-4) gives V2 RC 7/12 and quant 0.8117. Neither changes the outcome below (see Combined Scoring).

## Qualitative Scoring (50% weight) - Additive Binary Rubric

CEV form per cell: the claim is the criterion row; the evidence is a quote from the card (or "no evidence" with the sections searched); verdict MET = 1, NOT MET = 0.

### Completeness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----------|----|-------------|----|-------------|
| 1. Covers all explicit requirements (12 tasks) | NOT MET | Findings touch 7 of 12 tasks; no finding or confirmed_ok entry on Tasks 2, 3, 9. | NOT MET | Notes say "Read all 12 plan tasks", but findings assess 5 tasks; Tasks 1, 3, 5, 8, 9, 10, 11 have no assessment. A read claim is not coverage (re-evaluated, see position bias). |
| 2. Edge cases and failure scenarios | MET | F1: "new spec-panel-diffgate.md and sc-diffgate/** are untracked until staged, so the banned-phrase test ... never read them." | MET | QA-004: "an early PASS at review 1 or 2 closes the loop, so that file never exists". |
| 3. Dependencies and prerequisites | MET | F1 fix: "Before running that test in Tasks 5, 6 and 10, git add -N ... the new src/ and tests/ files". | MET | QA-005: "Task 6 says Task 7 checks both bullet sections character for character, but Task 7 pins only the seven Review Loop bullets". |
| 4. Success / completion criteria | MET | F1 fix: "put this in the acceptance text"; F10 fix: "with output saved under ./artifacts/". | MET | QA-001 fix: "a valid critical finding without a hunk or prior id yields blocking=1, verdict FAIL, and a reviser brief." |
| 5. Out of scope stated | NOT MET | No audit-scope statement. "(never .claude/)" in F1's fix constrains a fix, not the audit. Searched: header, findings, advisory, confirmed_ok, calibration. | MET | Notes: "Read-only audit; no tests run; external S1 brief files not inspected." |
| **Subtotal** | **3/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----------|----|-------------|----|-------------|
| 1. No factual errors | NOT MET | F4 fix lists "Review Loop and Diffgate pinned by bullet checks", but plan:110 pins only Review Loop (X-001, conceded). F9 "base-commit 2cb683f5 ... unverified" though source.md:199 names it (its own calibrator). | MET | Calibration per_finding: QA-001 through QA-005 all `verified: true`; no claim refuted in debate (QA-003 is mis-targeted, not false: "no row for source.md:133 or :144"). |
| 2. Technical approaches feasible | MET | F1 fix `git add -N` verified to work with `_tracked_text` (invariant-probe INV-023). | MET | QA-001 fix: "Apply surface-based deferral only from review 2" is one review-number condition (debate A-001 "local fix"). Sufficiency gaps (INV-027, INV-029) are carried to Step 4; they are not feasibility failures. |
| 3. Terminology consistent and accurate | NOT MET | F1, F2, F7 `class: Regression`, all conceded wrong under the taxonomy (Round 2 V1 rebuttal). | NOT MET | QA-001 `class: Drift` conceded as Regression (Round 2 V2 rebuttal); QA-003 `class: Drift` for a non-plan artifact. |
| 4. No internal contradictions (IC cross-check) | NOT MET | IC found 4 contradictions (see IC detail). | NOT MET | IC found 1 contradiction (QA-003 vs its calibrator). |
| 5. Claims supported by evidence | MET | Every finding carries a `citation:` list, e.g. F1 "[plan:89, plan:104, plan:25, tests/skills/test_review_severity_rule.py:36-56]". | MET | Every finding carries `citation:` plus `evidence:`, e.g. QA-001 "evidence: [source.md:24-29, source.md:149, plan:52]". |
| **Subtotal** | **2/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----------|----|-------------|----|-------------|
| 1. Logical ordering | MET | Findings ordered by severity: F1-F3 "MEDIUM", F4-F10 "LOW"; findings before advisory, confirmed_ok, verdict, calibration. | MET | QA-001 "HIGH" first, then MEDIUM; findings before verdict, notes, calibration. |
| 2. Consistent hierarchy depth | MET | All findings at `findings: - id:` depth; optional `detail:` on F1 only, same level. | MET | All findings at `findings: - id:` depth; optional `subtype:` on QA-003 only, same level. |
| 3. Separation of concerns | MET | Separate blocks: `correctness_gaps_advisory:`, `confirmed_ok:`, `calibration:`. | MET | Separate blocks: `findings:`, `notes:`, `calibration:`. |
| 4. Navigation aids (ids, cross-refs) | MET | `per_finding:` keyed "F1: {verified: true, ...}" through F10. | MET | `per_finding:` keyed "QA-001: {verified: true, ...}" through QA-005. |
| 5. Follows artifact-type conventions | MET | Card carries reviewer, persona, model_class, mode, findings (id, class, severity, citation, fix), verdict, self_confidence, calibration. | MET | Same field set plus `grounding_root`; class values from the four-class taxonomy with "subtype: coverage gap". |
| **Subtotal** | **5/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----------|----|-------------|----|-------------|
| 1. Unambiguous language | NOT MET | F3 rests on a hedge: ".dev/tasks may be absent in CI"; advisory "parametrization can inflate it". | MET | Finding and fix texts carry no hedge; the one vague marker ("Fix proposal is a guess") is the calibrator flagging vagueness, not card text hedging. |
| 2. Concrete rather than abstract | MET | F8 fix: "Stubs print {ok:false, exit:2, message:\"not implemented\"}". | MET | QA-001 fix: "yields blocking=1, verdict FAIL, and a reviser brief." |
| 3. Each section summarizable in one sentence | MET | Every finding has a one-sentence `title:`, e.g. F2 "Task 5 requires the subcommand table verbatim yet alters its check row". | MET | Each `finding:` opens with a one-sentence statement, e.g. QA-005 "Task 6 says Task 7 checks both bullet sections character for character". |
| 4. Acronyms and domain terms defined | NOT MET | `CAP_REGRESSION`, `proxy_all`, `T10`, `T11` used undefined. Searched all sections. | NOT MET | `C1-C12`, `INF-006`, `INF-019`, `M1/M2`, `proxy_all` used undefined. Searched all sections. |
| 5. Actionable next steps | MET | Every finding has `fix:`; "verdict: refactor". | MET | Every finding has `fix:`; "verdict: refactor". |
| **Subtotal** | **3/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----------|----|-------------|----|-------------|
| 1. At least 3 risks with probability and impact | NOT MET | Severity (impact) on every finding; no per-risk probability. Searched findings, calibration. | NOT MET | Severity on every finding; no per-risk probability. Searched findings, notes, calibration. |
| 2. Mitigation for each risk | MET | 10 of 10 findings carry `fix:`. | MET | 5 of 5 findings carry `fix:`. |
| 3. Failure modes and recovery | MET | F1 "the acceptance criteria pass vacuously"; the fix stages the files first. | MET | QA-001 "permits all initial blockers to become non-blocking and produce a false PASS"; the fix adds the review-number condition and a test. |
| 4. External dependencies and their failure scenarios | MET | F3: "source.md moves on archive; .dev/tasks may be absent in CI". | NOT MET | Notes name an external dependency ("external S1 brief files not inspected") but give no failure scenario for it (re-evaluated, see position bias). |
| 5. Monitoring / validation mechanism | MET | F10 fix: "Add make lint on the new files to Task 10 with output saved under ./artifacts/." | MET | QA-005 fix: "plus a negative test on one behavioral clause." |
| **Subtotal** | **4/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | V1 evidence | V2 | V2 evidence |
|-----------|----|-------------|----|-------------|
| 1. Collection boundaries (empty, single, max) | NOT MET | No empty-set, single-element or maximum case. F1's "file set from git ls-files" is a membership gap, not a boundary (re-evaluated, see position bias). Searched all sections. | MET | QA-001: "Review 1 has neither a computed surface nor prior ids" (empty surface and empty prior set). |
| 2. State interactions across components | MET | F1: test-harness state depends on git index state ("untracked until staged"). | MET | QA-004: loop terminal state (early PASS) leaves the kit's scoring input `result-r3.json` absent. |
| 3. Guard condition gaps | MET | F8 fix: "limit/read validation run in main before dispatch". | MET | QA-001: deferral rule lacks the review-number guard ("without distinguishing review 1"). |
| 4. Count divergence | MET | Advisory: "hardens 'about 35 script tests' into a floor ... parametrization can inflate it". | MET | QA-003: "the 28/35 figure measures selected excerpts only". |
| 5. Interaction effects | MET | F2: verbatim table requirement combined with the added proxy_all text: "the test demands an exact substring". | MET | QA-002: the copied Close bullet "only shows deferred.md" while the disclosure sentence is assigned nowhere. |
| **Subtotal** | **4/5** | | **5/5** | |

### Qualitative Summary

| Dimension | V1 | V2 |
|-----------|----|----|
| Completeness | 3/5 | 4/5 |
| Correctness | 2/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk Coverage | 4/5 | 3/5 |
| Invariant & Edge Case | 4/5 | 5/5 |
| **qual_score** | **21/30 = 0.700** | **24/30 = 0.800** |

## Edge Case Floor Check

| Variant | Invariant & Edge Case score | Floor (>= 1/5) | Eligible as base |
|---|---|---|---|
| V1 | 4/5 | pass | yes |
| V2 | 5/5 | pass | yes |

Floor not suspended (neither variant at 0/5).

## Position-Bias Mitigation

Pass 1 evaluated V1 then V2; Pass 2 evaluated V2 then V1. Disagreements were re-evaluated with both passes' evidence side by side; the re-evaluation verdict is final and is the one shown in the rubric tables above.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation basis |
|-----------|---------|--------|--------|-----------|-------|---------------------|
| Completeness 1 | V2 | MET | NOT MET | DISAGREE | NOT MET | P1 accepted "Read all 12 plan tasks"; P2 required per-task assessment. The criterion asks for coverage in the artifact; 7 tasks have none. |
| Completeness 5 | V1 | NOT MET | MET | DISAGREE | NOT MET | P2 (after V2's explicit scope note) read "(never .claude/)" as scope; it limits a fix, not the audit. |
| Clarity 1 | V1 | MET | NOT MET | DISAGREE | NOT MET | P2 (after V2's hedge-free text) flagged "may be absent in CI"; F3's premise depends on that hedge. |
| Risk 4 | V2 | NOT MET | MET | DISAGREE | NOT MET | P2 (V2 first) accepted "external S1 brief files not inspected"; it names a dependency with no failure scenario. |
| Inv 1 | V1 | MET | NOT MET | DISAGREE | NOT MET | P1 read F1's file set as a boundary case; P2 (after QA-001's empty-surface case) did not. V1 has no empty, single or maximum case. |

- Disagreements re-evaluated: 5 (V1: 3, V2: 2); the other 55 criterion verdicts agreed across passes.
- Final verdicts changed relative to Pass 1: 3 (Completeness 1 V2, Clarity 1 V1, Inv 1 V1).
- Pattern: every disagreement came from the second-read variant being judged against the first-read variant's evidence (a contrast effect, not a primacy effect). All five resolved to the stricter reading. Net effect against Pass 1: V1 -2, V2 -1.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (analyzer/sonnet) | 0.4165 | 0.3500 | **0.7665** | 6 of 14 decided S/C/X points = 42.9% |
| V2 (qa/haiku) | 0.3809 | 0.4000 | **0.7809** | 8 of 14 decided S/C/X points = 57.1% |

- **Margin**: |0.7809 - 0.7665| = 0.0143 (1.4 points), below the 0.05 threshold.
- **Tiebreaker applied**: Yes, level 1 (debate performance).
  - Scoring matrix (debate-transcript.md): V2 won S-001, S-003, S-005, C-001, C-002, C-004, C-009, X-001 (8). V1 won S-002, S-004, C-003, C-006, C-007, C-008 (6). C-005 was a synthesis; A-001 to A-009 were agreed responses with no winner. Decided points: 14.
  - The difference (57.1% vs 42.9%, 14.3 points) is above 5%, so level 1 decides. Level 2 (correctness count, V2 3/5 vs V1 2/5) would also select V2; level 3 (input order) is not reached.
- Sensitivity: under either RC alternative (V1 with its advisory: 0.7790 vs 0.7809; V2 with QA-003's fix target: 0.7665 vs 0.8059) the margin stays below 0.05 and the tiebreaker still selects V2.

## Selected Base: Variant 2 (reviewer-2, qa persona, haiku)

### Selection Rationale
- Combined scores are within 1.4 points; V2 wins the tiebreaker on debate points (8 of 14) and would also win level 2 (correctness 3/5 vs 2/5).
- V2 holds the highest-value diff points. C-004 (95%): QA-001 is the only runtime-correctness defect in either card, the review-1 false PASS (plan:49, :52 vs source.md:29, :149, :275). X-001 (95%): V2 is right that plan:110 pins only the Review Loop bullets. Starting from V2 puts the merged card's top finding and its one contested fact in base text, not in patches.
- V2 has fewer internal contradictions (IC 0.929 vs 0.862), all 5 findings calibrator-verified, and the full edge-case score (5/5).
- V1's advantage is breadth (RC 7 vs 5 tasks, SC 4 vs 3 blocks) and its confirmed_ok anchors. Both are additive: they merge in as new rows and a new block without rewriting base text. V1's weaknesses (three wrong Regression labels, F4's wrong exception list, F9's overstated claim) would need rewrites if V1 were the base.

### Strengths to Preserve from Base (V2)
1. QA-001 as the lead finding with its end-to-end review-1 test fix (C-004, 95%), reclassified per Round 2.
2. QA-005's correct reading of plan:110 (X-001, 95%), the anchor for merging F4.
3. Full repo-relative `citation:` plus a separate `evidence:` list per finding (S-001, 75%).
4. Explicit audit-scope notes ("Read-only audit; no tests run; external S1 brief files not inspected") and the owner-rulings statement (A-002).
5. QA-002 (deferred.md disclosure sentence unassigned) and QA-004 (early-PASS scoring branch) as verified findings.
6. The calibrator's `unraised_gaps` entry (exclusive-create lock untested, plan:42), promoted to a finding in Step 4.

### Strengths to Incorporate from Non-Base Variant (V1)
1. F1: the severity-rule test reads only `git ls-files` output, so the Tasks 5, 6 and 10 ACs pass vacuously (U-001, High; A-005 REJECT 95%).
2. F2: verbatim subcommand table vs the added `proxy_all` text in the `check` row (U-002; C-003, 75%).
3. F3: source of Task 5's expected verbatim blocks unspecified (U-003).
4. F4's `## Usage` drift-guard exemption, merged into QA-005 with the corrected exception list (C-001, 90%).
5. F5, F6, F8, F10: LOW plan gaps (U-005, U-006, U-008, U-010).
6. F7: README lacks the blindness-audit exemption from the plain-command void rule (U-007).
7. F9: the only assessment of plan-added content (C-006, 85%), with the Round 2 fix.
8. The `correctness_gaps_advisory` entry (35-test floor, U-011) and the `confirmed_ok` block of 7 positive anchors (S-002, 85%).
