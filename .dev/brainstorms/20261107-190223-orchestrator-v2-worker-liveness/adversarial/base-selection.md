# Base Selection Report

Variants: A = `variant-1-opus-architect.md`, B = `variant-2-opus-analyzer.md`, C = `variant-3-haiku-backend.md`.

## Quantitative Scoring (50% weight)

| Metric | Weight | A | B | C |
|---|---|---|---|---|
| Requirement Coverage (RC) | 0.30 | 0.963 | 0.963 | 0.963 |
| Internal Consistency (IC) | 0.25 | 0.963 | 0.925 | 0.920 |
| Specificity Ratio (SR) | 0.15 | 1.000 | 1.000 | 0.989 |
| Dependency Completeness (DC) | 0.15 | 1.000 | 1.000 | 1.000 |
| Section Coverage (SC) | 0.15 | 1.000 | 1.000 | 1.000 |
| **Quantitative score** | | **0.980** | **0.970** | **0.967** |

Formula: `quant = RC x 0.30 + IC x 0.25 + SR x 0.15 + DC x 0.15 + SC x 0.15`. Scores are rounded to three places after the exact sum.

How each metric was computed:

- **RC.** The source is `seed-brief.md` plus the 8 cases in `issue-body.md`: 6 success criteria, 6 constraints, 7 open questions and 8 cases, giving 27 items. Each item was topic-matched against each variant's headings and body text by Grep and reading. All three variants cover all 8 cases (A section 5, B section 5, C case-mapping table), all 6 success criteria and all 7 open questions. The constraints were Grep-checked: "harmless/false positive/WC-8/no Orca calls" has 11 hits in A, 13 in B and 3 in C; "cadence/preamble" has 12 hits in C. One constraint is missed by all three: "GitHub target only `IronbellyOrg/IronClaude`" (`seed-brief.md:38`). A Grep for `IronbellyOrg|upstream|fork` over the three variants returns 0 matches. RC = 26/27 = 0.963 for each.
- **IC.** `1 - contradictions / scorable claims`. Scorable claims are the numbered requirement IDs plus the acceptance-criteria IDs. A: 40 bold FR/NFR plus 14 AC = 54. B: 32 FR/NFR plus 8 AC = 40. C: FR-001..027 plus NFR-001..011 (38) plus 12 FR-027 tests = 50. Contradictions are taken from `diff-analysis.md` and confirmed in the variant text:
  - A, 2: (1) the section 7 ack escalation (terminal copy after A = 5/10 min, L5 after a second A) gives a 20-minute worst case against the 15-minute target; (2) the L2 cap of "4 per Task" resets on each replacement Task, against the work-unit restart budget in section 8. 1 - 2/54 = 0.963.
  - B, 3: (1) X-014: AC-1 allows 20 minutes against the 15-minute bounds in section 4.2; (2) X-015: NFR-004 "three fleet-wide calls" against FR-009 "one `stat` per worker contract path"; (3) the C-7 subsection sentence, which says an idle worker that "did not resume after two nudges and one direct question has met Orca's stall proof", contradicts section 8.1's L4 gate, "Orca positive stall proof only". 1 - 3/40 = 0.925.
  - C, 4: (1) X-009: ack bounds against the v1 first-legal-checkpoint rule; (2) X-021: a 1-minute case-4 bound that depends on a mailbox drain the variant itself calls v2; (3) C-041/A-004: the person-prompt bound against the sweep cadence; (4) the nudge cap "1 per incident, 2 per attempt" resets on each new incident and attempt, against the lineage replacement budget. 1 - 4/50 = 0.920.
- **SR.** `concrete / (concrete + vague)`. Vague lines come from a Grep for the protocol's vague-word list: A 0, B 0, C 1 (line 127, "finished-unreported if appropriate"). Concrete lines are lines with a number plus unit, a backticked token, a WC-n reference or a `file:n` citation: A 216, B 225, C 92. SR: A 216/216, B 225/225, C 92/93.
- **DC.** `resolved internal references / total`. A: 46 "section N" references, all to sections 2-13, which exist. B: 64 references, including 3.1, 6.2 and 8.2-8.5, all present in its heading list. C: 7 "above/below" references (lines 7, 87, 106, 144, 183, 353, 419), each resolving to adjacent defined text. All 1.000.
- **SC.** `H2 count / max H2 count`. A, B and C each have 13 H2 sections, so all score 13/13 = 1.000.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Thirty binary criteria in six dimensions of five each. Every verdict follows Claim-Evidence-Verdict (CEV). A MET verdict with no cited evidence is scored NOT MET. The verdicts below are the final ones, after the two passes and re-evaluation described under Position-Bias Mitigation.

| Dimension | A | B | C |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 4/5 |
| Correctness | 4/5 | 4/5 | 2/5 |
| Structure | 5/5 | 5/5 | 3/5 |
| Clarity | 5/5 | 5/5 | 4/5 |
| Risk Coverage | 4/5 | 5/5 | 4/5 |
| Invariant & Edge Case | 3/5 | 3/5 | 4/5 |
| **Total** | **26/30** | **27/30** | **21/30** |
| **Qualitative score** | **0.867** | **0.900** | **0.700** |

### Completeness

| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1 | Covers all explicit requirements from the source | MET. Claim: all 8 cases and 6 success criteria are addressed. Evidence: section 5 case table; G1-G7; AC-1..14 | MET. Claim: same. Evidence: section 5 table rows 1-8; AC-1..8 | MET. Claim: same. Evidence: case-mapping table; FR-027 tests 1-12 |
| 2 | Addresses edge cases and failure scenarios | MET. Evidence: state `unknown`; S7-like `unverifiable` never acted on; R1-R14 | MET. Evidence: S11 unknown; FR-016 worker without terminal; FR-017 unacked-at-settlement | MET. Evidence: NFR-008 corrupt input; storage failure, clock jump, lock loss (test 12, line 403) |
| 3 | Includes dependencies and prerequisites | MET. Evidence: section 3 adapter set; Orca verbs per signal S1-S12 | MET. Evidence: SG-1..SG-10 signal list; `check --help` mechanism (section 6.1) | MET. Evidence: FR-025 adapter methods; UNVERIFIED dependency list (lines 414-415) |
| 4 | Defines success/completion criteria | MET. Evidence: AC-1..14 (section 13) | MET. Evidence: AC-1..8 (section 13) | MET. Evidence: FR-027 acceptance tests 1-12 |
| 5 | Specifies what is explicitly out of scope | MET. Evidence: "### Non-goals" (line 60) | MET. Evidence: "### 1.3 Non-goals" (line 35) | NOT MET. Claim: no scope exclusion stated. Evidence: Grep for `non-goal|out of scope|scope|exclude` finds no scope section; the hits at lines 94 and 414 are local exclusions, not scope |

### Correctness

| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1 | No factual errors or hallucinated claims | MET. Evidence: Orca behaviour claims carry UNVERIFIED labels or citations (80 `.md:n` citations) | MET. Evidence: section 6.1 quotes `check --help`, dated 2026-11-07; 87 `.md:n` citations | MET. Evidence: unverified surfaces are labelled UNVERIFIED (lines 414-415); no false claim found by diff-analysis |
| 2 | Technical approaches are feasible with stated constraints | MET. Evidence: v1 uses only existing Orca verbs; v2 components separated (section 10) | MET. Evidence: section 10 change table splits v1 (C-1..C-8) from v2 (C-10..C-14) | NOT MET. Claim: the bounds rely on capacity that has not been shown. Evidence: 1-minute unconditional drain and 6-minute idle bound (FR-010, detection table line 94); C's own test 12 (line 403) and line 415 say capacity is UNVERIFIED |
| 3 | Terminology used consistently | MET. Evidence: state names defined once in section 2 and reused | MET. Evidence: S0-S11 IDs used the same way in sections 4, 5 and 8 | MET. Evidence: state table names reused in the case-mapping and ladder tables |
| 4 | No internal contradictions | NOT MET. Evidence: 20-minute ack worst case against the 15-minute target (see IC) | NOT MET. Evidence: X-014 (AC-1 20 min against 15 min); C-7 stall-proof sentence | NOT MET. Evidence: X-009, X-021 |
| 5 | Claims supported by evidence or rationale | MET. Evidence: 80 file:line citations | MET. Evidence: 87 file:line citations; per-case confidence levels | NOT MET. Claim: most claims are stated without a source. Evidence: Grep for `\.md:\d+` finds 3 citations in C, against 80 in A and 87 in B |

### Structure

| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1 | Logical section ordering (prerequisites before dependents) | MET. Evidence: state model (2), then signals (3), detection (4), cases (5), ladder (8) | MET. Evidence: same order, sections 2-9, then the contract changes (10) | MET. Evidence: requirements, then state table, then detection, then cases |
| 2 | Consistent hierarchy depth | MET. Evidence: 13 H2 and 40 H3 | MET. Evidence: 13 H2 and 42 H3, numbered `n.m` | NOT MET. Claim: flat. Evidence: Grep `^### ` returns 0 in C; 13 H2 hold all content |
| 3 | Clear separation of concerns | MET. Evidence: coordinator, worker (section 9) and adapter (section 11) parts are separate | MET. Evidence: coordinator side (sections 4-8), worker side (9), contract (10), portability (11) | MET. Evidence: worker rules (FR-022) and adapter (FR-025) in their own sections |
| 4 | Navigation aids present | MET. Evidence: numbered sections with 46 "section N" cross-references | MET. Evidence: numbered subsections with 64 cross-references | NOT MET. Claim: unnumbered sections, and the only cross-references are "above/below". Evidence: 7 "above/below" references (lines 7-419) |
| 5 | Follows artifact type conventions | MET. Evidence: FR/NFR IDs, AC list, risk table | MET. Evidence: same | MET. Evidence: FR/NFR IDs, risk table, acceptance tests |

### Clarity

| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1 | Unambiguous language | MET. Evidence: 0 vague-word hits | MET. Evidence: 0 vague-word hits | NOT MET. Evidence: line 127 "finished-unreported if appropriate" leaves the condition undefined |
| 2 | Concrete rather than abstract | MET. Evidence: SR 1.000; parameter table W 5, S 5, Q 10, G 10 | MET. Evidence: SR 1.000; exact bounds per state (section 4.2) | MET. Evidence: SR 0.989; numeric bounds in every detection row |
| 3 | Each section has a clear purpose | MET. Evidence: each H2 opens with its scope sentence | MET. Evidence: e.g. section 5 line 194 states its two-cause purpose | MET. Evidence: every H2 starts with a requirement block naming its subject |
| 4 | Acronyms and domain terms defined | MET. Evidence: S1-S12 and T0-T2 defined in section 3 | MET. Evidence: SG-1..SG-10 and W defined (FR-010) | MET. Evidence: E/I/C defined at line 7 |
| 5 | Actionable next steps | MET. Evidence: porting checklist (section 11); open questions (section 13) | MET. Evidence: section 10.2 gives verbatim contract wording | MET. Evidence: NFR-011 staged rollout steps |

### Risk Coverage

| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | NOT MET. Claim: impact is given, probability is not. Evidence: R1-R14 have columns risk, effect and mitigation (line 564 shape); Grep `probability|likelihood` finds 0 in A | MET. Evidence: risk table header "Likelihood | Impact" (line 510); e.g. R12 Medium/High (line 523) | NOT MET. Evidence: 15-row risk table without probability; Grep finds 0 |
| 2 | Mitigation strategy for each risk | MET. Evidence: mitigation column in R1-R14 | MET. Evidence: "Mitigation in this design" column | MET. Evidence: mitigation column in all 15 rows |
| 3 | Failure modes and recovery | MET. Evidence: ladder L0-L5 and resume note (section 8) | MET. Evidence: sections 8.1-8.5 | MET. Evidence: FR-019/020 ladder; FR-021 `resume-note.json` |
| 4 | External dependency failure scenarios | MET. Evidence: `unverifiable` liveness never acted on (FR-027) | MET. Evidence: S7 unreachable rules; FR-016 no terminal | MET. Evidence: NFR-010 fail closed; host outage test 12 |
| 5 | Monitoring/validation approach | MET. Evidence: AC-1..14; NFR-003 single parameter block in the run notes (line 229) | MET. Evidence: FR-005 logged transitions; NFR-005 tuning from logs (line 190); replay fixtures | MET. Evidence: NFR-009 observability; watchdog alert (line 403) |

### Invariant & Edge Case Coverage

| # | Criterion | A | B | C |
|---|---|---|---|---|
| 1 | Collection boundaries (empty, single, maximum) | MET. Evidence: per-Task and per-episode caps; fleet sweep with no per-worker timers | MET. Evidence: NFR-004 fixed calls for any fleet size; whole-batch delivery (FR-012) | MET. Evidence: NFR-008 16 KiB and depth 8 limits; supported fleet limit test (line 403) |
| 2 | State variable interactions across components | MET. Evidence: FR-004 precedence list over three axes | MET. Evidence: section 2.3 precedence; section 3.2 arrival-versus-change matrix | MET. Evidence: identity key `(run_id, task_id, dispatch_id, attempt_epoch)` (FR-005) |
| 3 | Guard condition gaps | NOT MET. Claim: a cap can be escaped. Evidence: L2 "4 per Task" restarts at 0 on every replacement Task | NOT MET. Evidence: "2 nudges per 60 min per Task" (section 8.2 S3 row) restarts on every replacement Task | NOT MET. Evidence: nudge cap "1 per incident, 2 per attempt" restarts per incident (C-041) |
| 4 | Count divergence (duplicates, replays) | MET. Evidence: reply IDs `R-<task>-<n>` identify a duplicate copy (section 7) | MET. Evidence: FR-018/FR-019 idempotency keyed by message ID | MET. Evidence: FR-018 idempotency; answer `sha256` |
| 5 | Interaction effects (late messages, concurrent actors) | NOT MET. Evidence: no rule rejects a lifecycle message from a replaced attempt (INV-023, HIGH) | NOT MET. Evidence: same gap (INV-023); FR-017 closes acks but does not fence late senders | MET. Evidence: `attempt_epoch` fencing (FR-005); controller lock (U-031) |

## Position-Bias Mitigation

Pass 1 evaluated in order A, B, C. Pass 2 evaluated in order C, B, A. Agreements were kept. Each disagreement was re-evaluated against the cited evidence, and the re-evaluated verdict is final.

| Dimension / criterion | Variant | Pass 1 (A,B,C) | Pass 2 (C,B,A) | Agreement | Final verdict and reason |
|---|---|---|---|---|---|
| Risk 1 (probability and impact) | A | MET | NOT MET | Disagree | NOT MET. Pass 1 read the "effect" column as probability. Grep `probability|likelihood` finds no probability column in A |
| Invariant 3 (guard gaps) | C | MET | NOT MET | Disagree | NOT MET. Pass 1 credited C's lineage replacement budget. The nudge cap still restarts per incident (C-041), which is the same gap A and B have |
| Correctness 5 (claims supported) | C | NOT MET | MET | Disagree | NOT MET. Pass 2 credited the UNVERIFIED labels, but a label marks a claim as unsupported rather than supporting it. C has 3 file:line citations |
| Invariant 5 (interaction effects) | B | MET | NOT MET | Disagree | NOT MET. FR-017 closes pending acks at settlement but does not reject late lifecycle messages from a replaced attempt (INV-023) |
| All other 86 criterion-variant cells | A, B, C | as final | as final | Agree | Unchanged |

Four disagreements out of 90 cells. All four were resolved as NOT MET, because in each case the MET reading rested on evidence that did not meet the criterion. The ranking is the same under either pass alone: pass 1 gives B 28, A 27, C 22; pass 2 gives B 27, A 26, C 22; the final totals are B 27, A 26, C 21.

## Edge-Case Floor

A variant scoring 0/5 on Invariant & Edge Case is not eligible as base.

| Variant | Invariant & Edge Case | Floor (>= 1/5) |
|---|---|---|
| A | 3/5 | Pass |
| B | 3/5 | Pass |
| C | 4/5 | Pass |

All three are eligible.

## Combined Scoring

`combined = 0.50 x quant + 0.50 x qual`

| Variant | Quantitative | Qualitative | Combined | Rank |
|---|---|---|---|---|
| A | 0.980 | 0.867 | 0.923 | 2 |
| B | 0.970 | 0.900 | **0.935** | 1 |
| C | 0.967 | 0.700 | 0.834 | 3 |

Exact sums before rounding: A 0.489815 + 0.433333 = 0.923148; B 0.485075 + 0.450000 = 0.935075; C 0.483638 + 0.350000 = 0.833638.

**Margin between top two:** B 0.935 - A 0.923 = 0.012. This is within 0.05, so the tiebreaker applies.

**Tiebreaker.** Level 1 is debate points won (`debate-transcript.md` scoring matrix): A 9, B 10, C 20, merge 51. Between the top two, B (10) beats A (9). Level 1 decides, so levels 2 (correctness count) and 3 (input order) are not used. For the record, level 2 would be a tie (A 4/5, B 4/5), and level 3 would pick A. C won the most debate points, but the tiebreaker compares only the top two by combined score. C's 0.834 is 0.101 below B, outside the 0.05 band.

Result: B is the base by combined score and by the level-1 tiebreaker.

## Selected Base: Variant B (`variant-2-opus-analyzer.md`)

**Selection rationale.** B has the highest combined score (0.935), and it also wins the level-1 tiebreaker against A (10 debate points against 9). Its lead comes from the qualitative rubric (27/30). It is the only variant whose risk table gives likelihood and impact (line 510), and the only one that already contains verbatim v1 contract wording for each amended rule (section 10.2). Its quantitative score is 0.010 below A's because of one more internal contradiction (the C-7 stall-proof sentence). That sentence is removed in the refactoring plan.

B also already holds three of the backbone parts named in merge guidance item 1: the occurrence/detection split, the status-body acknowledgement and per-stage handoff files. That leaves fewer structural transplants than starting from A or C. The other backbone parts (A's evidence axes, `proof_class` and cost tiers; C's proof, reconcile, stop and settle gates with the absolute input veto) are planned as incorporations.

**Strengths to preserve from B:**

- Occurrence-cause and detection-cause split per case, with confidence levels (section 5; U-011).
- Arrival-versus-change matrix (section 3.2; U-010).
- Status-body ack line `ack <message_id> <applied|queued|refused> <reason>` (FR-015) and "what the ack does not settle" (section 7.5).
- Explicit nine-type wait list and the unknown-type rule (FR-011, FR-013) with the per-type table (section 6.2).
- Nudge text (section 8.3), the same-cause rule (FR-022) and the resume-note format with the D2 freeze clause (section 8.5; U-020).
- Worker rules WR-1..WR-7, per-stage handoff files written even on failure (FR-025; U-018), and the section 10 change table with verbatim wording.
- Risk table with likelihood and impact.

**Strengths to incorporate from the other variants:**

- From A: the three evidence axes, `proof_class` and cost tiers T0-T2 (U-001, U-002, U-003); the timing-parameter table (U-007); reply IDs `R-<task>-<n>` (U-004); the `LivenessAdapter` interface and `Receipt` (U-006); a lineage key based on the `replaces` chain (U-009).
- From C: `attempt_epoch` fencing (U-022, v2); persist-before-ack (U-025); monotonic time and `coverage_degraded` (U-026); `uncertain_effects` in the resume note (U-028); untrusted-input limits (U-030); controller lock (U-031); watchdog (U-032); the WC-7 Skill-invocation amendment (U-033); "what it never implies" per message type; staged rollout (U-034, v2); the 6-minute and 1-minute figures as v2 profiles only.
- From the debate: merge guidance items 2-8 (`debate-transcript.md:509-519`), including the INV-005, INV-020 and INV-023 resolutions and the restart-window choice.
