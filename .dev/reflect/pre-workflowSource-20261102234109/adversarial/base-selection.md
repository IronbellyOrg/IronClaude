# Base Selection: reviewer-card comparison (sc:adversarial Step 3)

## Metadata

- Generated: 2026-11-03T00:18:24Z
- Mode: A (compare), 3 variants
- Variants: V1 = `variant-1-original.md` (reviewer 1, analyzer, sonnet); V2 = `variant-2-original.md` (reviewer 2, qa, glm-5.3); V3 = `variant-3-original.md` (reviewer 3, refactorer, opus)
- Requirement source: `.dev/tasks/to-do/TASK-WF-workflowSource-20261102-233731/source.md` (51 lines)
- Inputs also read: `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`
- Debate status carried in: 13/13 diff points agreed; BLOCKED_BY_INVARIANTS (INV-001, INV-002, INV-008 HIGH)

## Quantitative Scoring (50% weight)

### Adaptations for this artifact type (documented, deterministic)

The variants are YAML reviewer cards, not markdown documents. The metric definitions are applied as follows; rerunning on the same files gives the same numbers.

- **RC**: `source.md` has no FR/NFR/R IDs, so the protocol's edge case applies (section-level topic matching). 15 topics: In scope 1-6, Out of scope 3 bullets, Constraints 6 bullets. A topic is matched when the card names its items, tasks or exact subject (task numbers resolved against the plan headings, e.g. Task 65 = E02 sysop guide at tasklist:573, Task 66 = test-guide README index at tasklist:581).
- **IC**: scorable claims = one per finding plus the verdict line. A contradiction is a pair of claims in the same card that cannot both hold (both were conceded in debate Round 1/2).
- **SR**: counted over the `findings:` through `self_audit:` lines (the orchestrator-added `calibration:` block is metadata, excluded). Concrete = `name:line` citations + `Task N` references + `X-WN` item IDs. Vague = the protocol's vague list plus hedges `likely`, `several`, `fine only`, `milder`.
- **DC**: internal references are finding-ID references (`F1`, `F4`, ...) inside a card. Task, item, file and Tier-1 (`T1 C1`, `T1 D1`) references point at other documents and are excluded as external.
- **SC**: the cards have no H2 headings; top-level YAML keys stand in for sections (all three have the same 9 keys).

### Topic matching for RC

| # | Source topic (source.md line) | V1 | V2 | V3 |
|---|---|---|---|---|
| T1 | Workstream A (:12) | yes (R1-F3 A-W22.9, R1-F9) | yes (R2-F2 A-W22 item 9) | yes (R3-F2) |
| T2 | Workstream B (:16) | yes (R1-F2 B-W15.3, R1-F9) | yes (R2-F3, R2-F4) | yes (R3-F3, R3-F4, R3-F6, R3-F7) |
| T3 | Workstream C (:19) | yes (R1-F9 C-W3.6; R1-F11 c-e2e-transcript) | no | yes (R3-F10 C-W3 #12) |
| T4 | Workstream D guides (:23) | yes (R1-F6 Tasks 48-65; R1-F10 D05/D07) | no | no |
| T5 | Workstream E sysop guides (:29) | yes (R1-F6 "Gate for sysop"; R1-F7 Task 65) | no | no |
| T6 | docs/testing README index (:31) | yes (R1-F8 "66 on 48-65") | no | yes (R3-F1, R3-F5 Task 66) |
| T7 | Deferred gaps / O1-O22 / no issue filing (:36) | yes (R1-F10) | yes (R2-F6) | yes (R3-F3 "gap-71 rewrite stays deferred") |
| T8 | Release notes, CHANGELOG, release, tag (:37) | yes (R1-F10 "no release/tag") | no | no |
| T9 | Report and manifest (:38) | yes (R1-F10) | yes (R2-F6) | no |
| T10 | Match on quoted text (:42) | no | no | no |
| T11 | sync-dev / verify-sync / never stage .claude (:43) | yes (R1-F1 Task 26 verify-sync) | no | yes (R3-F9) |
| T12 | Fork `--repo` rule (:45) | yes (self_audit "SuperClaude-Org hits") | no | no |
| T13 | No installs against real `~/.claude` (:46) | no | no | no |
| T14 | Verification: markdownlint, smoke pytest, `make test` (:47-50) | yes (R1-F1, R1-F5) | yes (R2-F1) | yes (R3-F1, R3-F8) |
| T15 | Commit nothing (:51) | no | no | no |
| | **Matched** | **12/15** | **5/15** | **7/15** |

### Raw counts

| Count | V1 | V2 | V3 |
|---|---|---|---|
| Findings | 11 | 6 | 10 |
| Scorable claims (findings + verdict) | 12 | 7 | 11 |
| Contradictions | 1 (R1-F11 "tasks 1-66 map to all items" vs R1-F9 B-W22.6 unassigned; conceded R2) | 0 | 1 (R3-F10 classed `authorized` while recommending a change; conceded R2) |
| Concrete indicators (cites + Task refs + item IDs) | 60 (36 + 13 + 11) | 28 (17 + 8 + 3) | 66 (38 + 21 + 7) |
| Vague indicators | 4 ("milder" F2, "likely" F7, "fine only" F8, "Several" F9) | 0 | 0 |
| Internal references / resolved | 2/2 ("Only F1 blocking"; "F4 cites") | 2/2 (F3, F5) | 2/2 (F5, F9) |
| Top-level sections | 9 | 9 | 9 |

### Metric table

| Metric | Weight | V1 | V2 | V3 |
|---|---|---|---|---|
| RC (requirement coverage) | 0.30 | 0.800 | 0.333 | 0.467 |
| IC (internal consistency) | 0.25 | 0.917 | 1.000 | 0.909 |
| SR (specificity ratio) | 0.15 | 0.938 | 1.000 | 1.000 |
| DC (dependency completeness) | 0.15 | 1.000 | 1.000 | 1.000 |
| SC (section coverage) | 0.15 | 1.000 | 1.000 | 1.000 |
| **quant_score** | | **0.910** | **0.800** | **0.817** |

Computation: V1 = 0.240 + 0.229 + 0.141 + 0.150 + 0.150 = 0.910; V2 = 0.100 + 0.250 + 0.150 + 0.150 + 0.150 = 0.800; V3 = 0.140 + 0.227 + 0.150 + 0.150 + 0.150 = 0.817.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Each row is one Claim-Evidence-Verdict record: the claim is "criterion N is met in variant X"; the evidence column is the quote or section reference (or the sections searched when nothing was found); P1 = pass 1 (input order V1, V2, V3), P2 = pass 2 (reverse order V3, V2, V1); Final = agreed verdict or the re-evaluation result. M = MET (1), N = NOT MET (0). Rows marked with an asterisk are in the disagreement log.

### Completeness (5 criteria)

| # | Variant | Evidence | P1 | P2 | Final |
|---|---|---|---|---|---|
| 1 All source requirements | V1 | 12/15 topics (RC table); self_audit "mapped 66 tasks and gaps 1-70" | M | M | M |
| 1 | V2 | 5/15 topics; no Workstream C, D, E, release/tag or constraint findings beyond verification | N | N | N |
| 1 | V3 | 7/15 topics; no D/E guide, report/manifest or fork-rule coverage | N | N | N |
| 2 Edge cases / failure scenarios | V1 | R1-F4 docs that truthfully say "X does not exist" break removal greps; R1-F8 "fine only under sequential execution" | M | M | M |
| 2 | V2 | R2-F1 executor treats tests as extras; R2-F6 executor reads CONSOLIDATED-PLAN.md:636 and would file issues | M | M | M |
| 2 | V3 | R3-F5 "safe only under sequential execution"; R3-F9 sync checks verify nothing for core/rules | M | M | M |
| 3 Dependencies / prerequisites | V1 | R1-F8 "Add Depends-on lines: 47 on 3,17,43-46; 66 on 48-65; 37 on 43-46" | M | M | M |
| 3 | V2 | R2-F4 "Task 37 ... runs before Tasks 43-46" | M | M | M |
| 3 | V3 | R3-F4, R3-F5 dependency sets on 47 and 66 | M | M | M |
| 4 Success / completion criteria | V1 | R1-F1 "log to ./artifacts/final-make-test.log"; verdict FAIL | M | M | M |
| 4 | V2 | R2-F1 "final full make test ... or a terminal task AC"; verdict FAIL | M | M | M |
| 4 | V3 | R3-F1 "logs under ./artifacts/"; R3-F2 "grep AC per linking file"; verdict FAIL | M | M | M |
| 5 Out of scope stated | V1 | R1-F10 "no issue filing, no release/tag, no report/manifest" | M | M | M |
| 5 | V2 | R2-F6 "no issue filing; do not write post-release-report.md or post-release-manifest.json" | M | M | M |
| 5* | V3 | R3-F3 "(gap-71 rewrite stays deferred)" | N | M | M |

### Correctness (5 criteria)

| # | Variant | Evidence | P1 | P2 | Final |
|---|---|---|---|---|---|
| 1 No factual errors | V1 | R1-F4 cites tasklist:281 where Task 28 grep is :273 (calibration note); R1-F11 "map to all items" false per R1-F9 | N | N | N |
| 1 | V2 | R2-F3 "tasklist grep 0 hits" false: git-standards-protocols.md named at tasklist:426 (spot check) | N | N | N |
| 1 | V3 | R3-F5 cites tasklist:65 (a Depends-on line); R3-F9 Makefile:109-157 holds only sync-dev | N | N | N |
| 2* Feasible approaches | V1 | R1-F1 "Add a final task or Constraint": final-task half forbidden by quality-gates.md:22; Constraint half is graded (qa.md:15 per INV-001 evidence) | N | M | M |
| 2 | V2 | R2-F1 "plan Constraints or a terminal task AC"; both gate-compliant (C-001, 95%) | M | M | M |
| 2 | V3 | R3-F1 "Add a final repo-verification task" violates quality-gates.md:22 (conceded R2) | N | N | N |
| 3 Consistent terminology | V1 | Omissions labelled both `drift` (R1-F3) and `grounding-gap` (R1-F9 B-W22.6, R1-F10); conceded R2 | N | N | N |
| 3* | V2 | Omissions consistently `drift` (R2-F2, R2-F3, R2-F4, R2-F6); R2-F5 `grounding-gap` on a reviewer-artifact count | M | N | M |
| 3 | V3 | R3-F10 `authorized` for an overlap it asks to change; R3-F5 `drift` for ordering (both conceded) | N | N | N |
| 4 No internal contradictions | V1 | IC 0.917: R1-F11 vs R1-F9 | N | N | N |
| 4 | V2 | IC 1.000; no contradiction found across 7 claims | M | M | M |
| 4 | V3 | IC 0.909: R3-F10 class vs recommendation | N | N | N |
| 5 Claims supported by evidence | V1 | Every finding carries a `citation:`; calibration citation_grounding 0.92 | M | M | M |
| 5 | V2 | Every finding carries a `citation:`; citation_grounding 0.92 | M | M | M |
| 5 | V3 | Every finding carries a `citation:`; citation_grounding 0.92 | M | M | M |

### Structure (5 criteria)

| # | Variant | Evidence | P1 | P2 | Final |
|---|---|---|---|---|---|
| 1 Logical ordering | V1 | Blocking R1-F1 first, then minor findings, then non-deviation R1-F11 last | M | M | M |
| 1 | V2 | Blocking R2-F1 first | M | M | M |
| 1 | V3 | Blocking R3-F1 first; non-deviation R3-F8/F10 near the end | M | M | M |
| 2 Consistent hierarchy | V1 | All 11 findings have id/claim/citation/class/severity/recommendation | M | M | M |
| 2 | V2 | All 6 findings same six fields | M | M | M |
| 2 | V3 | All 10 findings same six fields | M | M | M |
| 3 Separation of concerns | V1 | findings / verdict / self_confidence / self_audit / calibration as separate keys | M | M | M |
| 3 | V2 | same keys | M | M | M |
| 3 | V3 | same keys | M | M | M |
| 4 Navigation aids | V1 | Finding IDs cross-referenced in self_audit ("Only F1 blocking") and calibration ("F4 cites :281") | M | M | M |
| 4* | V2 | Finding IDs cross-referenced only in calibration spot checks (F3, F5) | M | N | M |
| 4* | V3 | Finding IDs cross-referenced only in calibration spot checks (F5, F9) | M | N | M |
| 5 Artifact-type conventions | V1 | Matches the reflect reviewer card schema (reviewer, persona, model_class, findings, verdict, self_audit, calibration) | M | M | M |
| 5 | V2 | same schema | M | M | M |
| 5 | V3 | same schema | M | M | M |

### Clarity (5 criteria)

| # | Variant | Evidence | P1 | P2 | Final |
|---|---|---|---|---|---|
| 1 Unambiguous language | V1 | Hedges: "milder" (F2), "likely works" (F7), "fine only" (F8), "Several" (F9) | N | N | N |
| 1 | V2 | No vague indicator found (SR count 0) | M | M | M |
| 1 | V3 | No vague indicator found (SR count 0) | M | M | M |
| 2 Concrete | V1 | 60 concrete indicators; task and line references per finding | M | M | M |
| 2 | V2 | 28 concrete indicators | M | M | M |
| 2 | V3 | 66 concrete indicators | M | M | M |
| 3 One-sentence purpose per finding | V1 | Each `claim:` is one or two sentences | M | M | M |
| 3 | V2 | same | M | M | M |
| 3 | V3 | same | M | M | M |
| 4 Terms defined on first use | V1 | "AC", "UV-only", "B-W22.6" used undefined (searched all findings) | N | N | N |
| 4 | V2 | "AC", "T1 C3" undefined | N | N | N |
| 4 | V3 | "AC", "#9" item numbering undefined | N | N | N |
| 5 Actionable next steps | V1 | Every finding has a `recommendation:` (R1-F11 "No change.") | M | M | M |
| 5 | V2 | Every finding has a `recommendation:` | M | M | M |
| 5 | V3 | Every finding has a `recommendation:` (R3-F8 "None needed.") | M | M | M |

### Risk Coverage (5 criteria)

| # | Variant | Evidence | P1 | P2 | Final |
|---|---|---|---|---|---|
| 1* At least 3 risks with probability and impact | V1 | `severity:` gives impact on all 11; probability only on R1-F7 ("likely") and R1-F8 (conditional) | M | N | N |
| 1 | V2 | `severity:` only; no probability statements (searched all findings) | N | N | N |
| 1 | V3 | `severity:` only; R3-F5 conditional on one risk | N | N | N |
| 2 Mitigation per risk | V1 | `recommendation:` on every finding | M | M | M |
| 2 | V2 | `recommendation:` on every finding | M | M | M |
| 2 | V3 | `recommendation:` on every finding | M | M | M |
| 3 Failure modes and recovery | V1 | R1-F8 out-of-order execution, recovery via Depends-on lines | M | M | M |
| 3 | V2 | R2-F1 executor skips tests, recovery via terminal AC | M | M | M |
| 3 | V3 | R3-F5 dangling forward links, recovery via ordering/dependencies | M | M | M |
| 4 External dependencies | V1 | R1-F5 pre-commit `markdownlint --fix`; R1-F7 `_fetch` urlopen scheme handling | M | M | M |
| 4 | V2 | R2-F1 `/sc:implement` behaviour (implement.md:11) | M | M | M |
| 4 | V3 | R3-F9 Makefile sync-dev scope; R3-F8 pre-commit pin | M | M | M |
| 5 Monitoring / validation mechanism | V1 | R1-F1 `./artifacts/final-make-test.log`; R1-F9 `./artifacts/deviations.md` | M | M | M |
| 5 | V2 | R2-F2 "record in artifacts/deviations.md" | M | M | M |
| 5 | V3 | R3-F1 logs under `./artifacts/`; R3-F2/F3 grep ACs | M | M | M |

### Invariant & Edge Case Coverage (5 criteria)

| # | Variant | Evidence | P1 | P2 | Final |
|---|---|---|---|---|---|
| 1* Collection boundaries | V1 | R1-F4 empty-result removal greps vs legitimate absence statements | M | N | M |
| 1 | V2 | No empty/single/max boundary finding (searched R2-F1..F6) | N | N | N |
| 1 | V3 | R3-F9 sync-dev coverage set excludes core/ and rules/ (empty verification set for Tasks 6, 26) | M | M | M |
| 2 State across component boundaries | V1 | R1-F5 plan relaxation vs pre-commit hook at the orchestrator's commit | M | M | M |
| 2 | V2 | R2-F1 plan vs executor (implement.md:11) | M | M | M |
| 2 | V3 | R3-F9 plan vs Makefile targets | M | M | M |
| 3 Guard condition gaps | V1 | R1-F7 "_fetch uses urllib urlopen with no scheme check" | M | M | M |
| 3 | V2 | R2-F1 no gate runs the tests | M | M | M |
| 3 | V3 | R3-F1 no test run after Task 26 or Task 66 | M | M | M |
| 4* Count divergence | V1 | R1-F11 asserts 1-66 / 1-70 consistency; R1-F9 lists sub-items, not a count divergence | N | M | N |
| 4 | V2 | R2-F5 "53/53" vs 66 deliverables | M | M | M |
| 4 | V3 | R3-F3 "Goal claims gaps 1-70 fixed" while a gap-70 sub-part has no task | M | M | M |
| 5 Interaction effects | V1 | R1-F2 Task 39 AC vs B-W15.3; R1-F8 cross-task ordering | M | M | M |
| 5 | V2 | R2-F4 Task 37 vs Tasks 43-46 | M | M | M |
| 5 | V3 | R3-F10 Tasks 3 and 4 overlap; R3-F5 forward links Tasks 4/13 to 17 | M | M | M |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5 | 4 | 4 |
| Correctness | 2 | 4 | 1 |
| Structure | 5 | 5 | 5 |
| Clarity | 3 | 4 | 4 |
| Risk Coverage | 4 | 4 | 4 |
| Invariant & Edge Case | 4 | 4 | 5 |
| **Total (of 30)** | **23** | **25** | **23** |
| **qual_score** | **0.767** | **0.833** | **0.767** |

### Edge Case Floor Check

| Variant | Invariant score | Floor (1/5) | Eligible as base |
|---|---|---|---|
| V1 | 4/5 | met | yes |
| V2 | 4/5 | met | yes |
| V3 | 5/5 | met | yes |

Floor not suspended (no variant at 0/5).

## Position-Bias Mitigation

- Pass 1 order: V1, V2, V3. Pass 2 order: V3, V2, V1. Each pass applied the same 30-criterion rubric with CEV.
- Pass totals before resolution: Pass 1 V1 23, V2 25, V3 22; Pass 2 V1 23, V2 23, V3 22.

### Disagreement log

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final | Re-evaluation reason |
|---|---|---|---|---|---|---|
| Completeness 5 | V3 | N | M | no | M | R3-F3 explicitly keeps gap 71 deferred, which is an out-of-scope statement; one statement satisfies the criterion |
| Correctness 2 | V1 | N | M | no | M | The Constraint option in R1-F1 is gate-compliant (not a verification-only task) and plan Constraints are graded (qa.md:15) |
| Correctness 3 | V2 | M | N | no | M | R2-F5 uses `grounding-gap` within its taxonomy meaning (an ungrounded count claim); omission labels are uniform |
| Structure 4 | V2 | M | N | no | M | The calibration block is part of the delivered card; ID cross-references there count as navigation |
| Structure 4 | V3 | M | N | no | M | Same reasoning as V2 |
| Risk 1 | V1 | M | N | no | N | Probability is stated for at most 2 risks; the criterion needs at least 3 |
| Invariant 1 | V1 | M | N | no | M | R1-F4 is about an empty-result check (grep returns nothing) meeting legitimate content: a boundary condition |
| Invariant 4 | V1 | N | M | no | N | R1-F9 is sub-item coverage, not an off-by-one or range divergence; R1-F11 asserts consistency rather than finding divergence |

- disagreements_found: 8
- verdicts_changed: 8 (each re-evaluation overturned one pass: 5 sided with Pass 1, 3 with Pass 2). Net effect on final totals: V1 equal to both passes (23); V2 +2 over Pass 2; V3 +1 over either pass.

## Combined Scoring

| Variant | quant_score | qual_score | 0.5 x quant | 0.5 x qual | Combined | Rank |
|---|---|---|---|---|---|---|
| V1 (analyzer) | 0.910 | 0.767 | 0.455 | 0.383 | **0.838** | 1 |
| V2 (qa) | 0.800 | 0.833 | 0.400 | 0.417 | **0.817** | 2 |
| V3 (refactorer) | 0.817 | 0.767 | 0.409 | 0.383 | **0.792** | 3 |

### Margin and tiebreaker

- Margin V1 over V2: 0.838 - 0.817 = 0.021 (2.1 percentage points, below the 5% threshold). Tiebreaker triggered.
- **Level 1 (debate points won, scoring matrix in `debate-transcript.md`)**: a point counts for each variant named as its winner; A-001 and A-002 (won by all) are excluded as non-differentiating.

| Variant | Points won | Fractional (shared split) | Confidence-weighted (sensitivity) |
|---|---|---|---|
| V1 | 6 (S-001, S-002, C-005, C-007, X-001 ordering half, X-002) | 4.83 | 4.13 |
| V2 | 4 (C-001, C-003, C-006, X-001 omissions half) | 2.83 | 2.65 |
| V3 | 5 (S-002, C-002, C-003, C-004, X-001 omissions half) | 3.33 | 2.88 |

- V1 leads V2 by 2 points (6 vs 4), far outside 5%. Level 1 decides: **V1**. Level 2 (correctness count: V2 4, V1 2) and level 3 (input order) were not reached.
- Tiebreaker applied: yes (level 1). It confirms the combined-score ranking, and the result holds under all three counting methods.

## Selected Base: Variant 1 (reviewer 1, analyzer, sonnet)

### Rationale

V1 has the highest combined score (0.838) and wins the level-1 tiebreaker on debate points (6 vs 4). Its lead comes from requirement coverage: it is the only card that audits Workstreams D and E, the release/tag exclusion and the fork rule (RC 0.800 vs 0.333 and 0.467), and it holds the only executor-breaking AC contradictions (R1-F2, R1-F4). Its weaknesses are classification and correctness (2/5): it labels omissions `grounding-gap`, contradicts itself in R1-F11, offers a forbidden "final task" remedy and miscites tasklist:281. All of these were conceded in Round 2 and are repaired in `refactor-plan.md`. V2 carries the winning remedy for the one blocking finding (C-001, 95%); that remedy is incorporated into the base rather than making V2 the base, because V2 covers only 5 of 15 source topics.

### Strengths to preserve (from V1)

- R1-F2: Task 39 AC vs B-W15.3 (CONSOLIDATED-PLAN.md:498 vs tasklist:361); unique, high value (U-001).
- R1-F4: removal-grep ACs in Tasks 13, 27, 28, 29 against legitimate absence statements (U-002), with the :273 citation fix.
- R1-F5 (narrowed): the plan's markdownlint relaxation clause is minor drift; the pin itself is necessary (C-007, X-002 won 85%).
- R1-F6: Tier A/B/C grouping and template header fields for guides (U-004).
- R1-F7: Task 65 `python3 -m http.server` vs the UV-only rule (U-005).
- R1-F8: missing Depends-on lines as `grounding-gap` (C-005 won 90%).
- R1-F9: numbered sub-items held only by the "Read the named item" constraint (U-006), with B-W22.6 split out as drift.
- R1-F10: the widest out-of-scope list (issue filing, release/tag, report/manifest, [EXTERNAL] steps written not run), reclassed drift.
- Breadth of the audit (S-001 won 85%).

### Strengths to incorporate (from non-base variants)

- V2 R2-F1: executor evidence (implement.md:11 "Lint and tests are extras") and the ranked C-001 remedy (AC on Task 66, Constraint as reinforcement) (C-001 95%, A-001 95%).
- V2 R2-F6: CONSOLIDATED-PLAN.md:636 instructs issue filing and the executor reads it via tasklist:19 (C-006 95%).
- V2 R2-F3 / V3 R3-F3: B-W22 #6 git-standards section-6 pointer as drift, remedy on Task 46 with a grep AC (C-003 90%).
- V3 R3-F1 surviving half: smoke run on Task 26's AC.
- V3 R3-F2: per-linking-file grep AC for the codegraph.md backlinks (C-002 85%).
- V3 R3-F4 / V2 R2-F4: B-W12 #6 four-note links as drift, folded into Task 47 (C-004 90%).
- V3 R3-F5: forward links from Tasks 4 and 13 to codegraph.md (Task 17), as grounding-gap with corrected citation.
- V3 R3-F6 (Task 42 paraphrase of B-W18), R3-F7 (Task 47 unrequested index links), R3-F8 (pin necessary), R3-F9 (sync-dev/verify-sync do not cover core/ or rules/; corrected citation).
- Invariant probe: INV-001, INV-002, INV-008 (HIGH) and INV-003, INV-004, INV-006 (MEDIUM) as required additions to the C-001 remedy.
