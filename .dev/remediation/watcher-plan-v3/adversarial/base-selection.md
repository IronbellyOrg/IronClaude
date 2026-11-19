# Base Selection Report

Folder: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/adversarial/`. Variants: V1 = `variant-1-opus-security.md` (opus:security), V2 = `variant-2-opus-architect.md` (opus:architect), V3 = `variant-3-sonnet-analyzer.md` (sonnet:analyzer). Scoring follows `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 to A.5). Input order is V1, V2, V3.

Method notes (so the numbers can be re-run):
- SR is computed from text counts: concrete = count of `name:NNN` file/line citations (`grep -oE '[A-Za-z_./-]+:[0-9]{1,4}(-[0-9]+)?'`); vague = count of hedge phrases (`unverified|not verified|did not read|unread|maybe|not read|inference|check whether|as appropriate|should consider|various|etc.`). This is a proxy for the numbers/named-entity rule, because almost every concrete claim here is a file:line citation.
- IC, DC are manual counts (contradiction and reference lists below); they are estimates, not script output.
- RC is scored at the finding level against the source requirements Q-1 to Q-10 (10 items).

## Quantitative Scoring (50% weight)

| Metric | Weight | V1 (opus:security) | V2 (opus:architect) | V3 (sonnet:analyzer) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 1.000 (Q-1 to Q-10, 10 of 10; Q-1 part B and label/project verbs beyond the finding) | 1.000 (10 of 10) | 1.000 (10 of 10) |
| internal_consistency | 0.25 | 1.000 (0 contradictions found in about 30 claims; the `plan-hash ... complete.md` over-match is disclosed in V1's own risks) | 1.000 (0 found; the over-match is a concession in A2, not a self-contradiction) | 0.964 (1 in about 28 claims: Q-2 fix says default `closed`, the rollback line says default `open`; flagged by A3 section 3) |
| specificity_ratio | 0.15 | 0.911 (72 citations, 7 hedges) | 0.977 (85 citations, 2 hedges) | 0.842 (48 citations, 9 hedges) |
| dependency_completeness | 0.15 | 0.970 (one reference left open: "message goes in the printer table" with no text for `LL-ISSUE-WRITE`) | 1.000 (Task 3a, Option A/B/C, Constraints line all resolve) | 0.970 (one soft reference: Q-7 "around line 901" is approximate) |
| section_coverage | 0.15 | 0.917 (11 H2 of max 12) | 0.917 (11 H2 of 12) | 1.000 (12 H2: adds "Ranked findings") |
| **quant_score** | | **0.9697** | **0.9841** | **0.9629** |

Arithmetic: V1 0.300 + 0.250 + 0.1367 + 0.1455 + 0.1375 = 0.9697. V2 0.300 + 0.250 + 0.1466 + 0.1500 + 0.1375 = 0.9841. V3 0.300 + 0.2411 + 0.1263 + 0.1455 + 0.1500 = 0.9629.

## Qualitative Scoring (50% weight): additive binary rubric

Verdicts are the final ones after the position-bias step (the disagreeing cells are listed in the next section). Evidence is a section or quote reference per the CEV rule; "No evidence found" defaults to NOT MET.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Covers all explicit requirements | MET | Q-1 to Q-10 sections | MET | Q-1 to Q-10 sections | MET | Q-1 to Q-10 sections |
| Addresses edge cases and failure scenarios | MET | Q-3 "Risks": cleared Pipeline reads None, one-second resolution voids | MET | Q-3 Option C: cleared Pipeline reads None, cleared Status fails `project_check`; stale host guard in Q-1 | MET | Q-3 failure modes: same-second approval; Q-1 typo falls to `LL-BROKEN` |
| Includes dependencies and prerequisites | MET | Q-10: Task 4 on Task 1, Task 15 on Task 9, cycle.py order 4, 6, 12, 18 | MET | Q-10 Constraints line lists files edited by several tasks; Task 3a | MET | Q-10: Task 15 on Task 9, cycle.py order (Task 4 on Task 1 is conditional "if it edits predicates.py") |
| Defines success/completion criteria | MET | Tests lines per finding | MET | Tests and plan edits per finding | MET | Tests lines per finding |
| Specifies out-of-scope items | MET | Q-6 rejected "dedicated bot login: Coder repo"; Residual risks | MET | `[SCOPE+]` flags; Q-6 "out of scope"; Residual 2 | NOT MET | Searched Residual risks and Q-1 to Q-10: only "Not a regression" notes and rejected alternatives, no out-of-scope statement |
| **Subtotal** | **5/5** | | **5/5** | | **4/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| No factual errors or hallucinated claims | NOT MET | Q-1: `*issue_pipeline*complete*` refuses `uv run pytest tests/issue_pipeline/test_complete.py` (R2 section 0 case run); omits the version stamp (I-6) | MET | Q-1 patterns verified by R2 case run; hyphen alternative over-match is a disclosed limit | NOT MET | Same pattern defect as V1; Q-4 "nothing in tests breaks"; `$owner: String = "IronbellyOrg"` offered |
| Technical approaches feasible with stated constraints | MET | Q-1 Part B states the second-login cost | MET | Option A is about 6 lines (Q-2) | MET | Q-3 observation plus decision table |
| Terminology used consistently and accurately | NOT MET | Q-5 "Compare-and-set" is a read-then-write, not atomic (A3 section 3 D-09; probe I-4 limit) | MET | Class `ISSUE`, `LL-ISSUE`, `level_gated` used consistently | MET | `ISSUEW`/`LL-ISSUE` used consistently |
| No internal contradictions (cross-checked with IC) | MET | IC 1.000 | MET | IC 1.000 | NOT MET | IC 0.964: Q-2 default `closed` versus `open` |
| Claims supported by evidence or rationale | MET | file:line on every finding | MET | "Every line below was re-read" plus citations | MET | citations; unread items explicitly marked |
| **Subtotal** | **3/5** | | **5/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Logical section ordering | MET | Safety boundaries first (Q-1A, Q-1B, Q-2), then Q-3 to Q-10 | MET | Register order, each tagged BLOCKING/OWNER/NOTE | MET | Ranked table then register order |
| Consistent hierarchy depth | MET | One H2 per finding; Part A/B only in Q-1 | MET | One H2 per finding | MET | One H2 per finding |
| Clear separation of concerns | MET | Change / Files / Risks / Tests / Rejected | MET | Evidence / change / plan edits / tests / rejected | MET | Fix / What it breaks / Failure modes / Tests / Rollback / Rejected |
| Navigation aids present | MET | Header path legend; "see Q-9", "see Residual risks" | MET | Scope-flag legend, BLOCKING/OWNER tags in headings | MET | Ranked table acts as index |
| Follows conventions of the artifact type (per-finding change, tests, rejected) | MET | All 10 findings carry Change, Tests, Rejected | NOT MET | Q-8, Q-9 and Q-10 have no Tests line and no Rejected line (shape drifts after Q-7) | NOT MET | Q-8 and Q-10 have no Tests line; Q-9 and Q-10 give no Rejected line |
| **Subtotal** | **5/5** | | **4/5** | | **4/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Unambiguous language | MET | One hedge in Q-3 ("not verified here"), stated as a limit | MET | 2 hedges, both stated limits | NOT MET | Q-8 "or maybe `$owner: String = ...` (unverified)"; Q-6 marker given as "e.g." |
| Concrete rather than abstract | MET | Verbatim replacement sentence for WORKER-CONTRACT.md:245 | MET | Verbatim guard line edits | MET | Case rows named |
| Each section has a clear purpose | MET | Heading plus Change line | MET | Heading plus Evidence | MET | Heading plus Fix |
| Acronyms and domain terms defined on first use | NOT MET | `W`, `WA`, `F`, `FS`, `R31`, `DF-14` undefined | NOT MET | Same abbreviations undefined | NOT MET | Same abbreviations undefined |
| Actionable next steps or decision points identified | MET | Q-1 Part B marked owner decision | MET | Q-2 and Q-3 Options A/B/C with a recommendation | MET | Decision table in Q-3; Q-2 "owner flips or waives" |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| At least 3 risks with probability and impact | NOT MET | 4 residual risks with impact but no probability stated | NOT MET | 5 residual risks with impact but no probability stated | NOT MET | Ranked table gives consequence order, no probability |
| Mitigation for each identified risk | MET | Residual 1 credential separation; 2 Part B; 3 owner decision; 4 observation | NOT MET | Residual 2 "out of scope; flag to owner" and residual 3 "nothing keeps checking" carry no mitigation | NOT MET | Residual risks carry no mitigation beyond "owner should know" |
| Failure modes and recovery procedures | MET | Q-3: drop item time if a label moves it; return R31 to owner on fail-open | MET | Q-3 Option B fallback label; Q-2 Option B waiver | MET | "Failure modes" and "Rollback" per finding |
| External dependencies and their failure scenarios | MET | GitHub timestamps, community discussion unverified | MET | GitHub field-value timestamps (Residual 3) | MET | updatedAt semantics, OB gate state |
| Monitoring or validation mechanism for risk detection | MET | Coupling test, first-run report prints gate state, `check-config` warning | MET | `level_gated` audit reason, Task 3a observation, introspection | MET | Decision table, same-second test, audit reason |
| **Subtotal** | **4/5** | | **3/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| Boundary conditions for collections (empty, single, maximum) | MET | Q-5: zero items or several refuse | MET | Q-5: `project_missing`, `project_ambiguous` | MET | Q-5: zero or several live matches, archived-item case |
| State variable interactions across component boundaries | MET | Q-5 Status moves only from the four allowed Statuses; Q-4 order of the three checks | NOT MET | Q-5 writes the Status unconditionally after selecting the item (probe I-4 UNADDRESSED alone) | NOT MET | Same unconditional write (probe I-4 UNADDRESSED alone) |
| Guard condition gaps (missing validation, unguarded type assumptions) in its own proposed guards | NOT MET | Probe I-5 (pattern refuses pytest) and I-6 (no version bump) UNADDRESSED alone | MET | Pattern keeps pytest allowed; version bump to 2; `'issue '*` after row 652; `^PVT_` check | NOT MET | Probe I-5 and I-6 UNADDRESSED alone |
| Count divergence (off-by-one, inclusive/exclusive) | MET | Q-3 Risks: same-second change voids (fails closed) | MET | Q-3: void when time is at or after the approval; Q-7 recount 45 lines in 7 files | MET | Same-second test; `t >= approved_at` |
| Interaction effects when features combine | MET | Q-1 Part A with Part B; ship gate with Task 17 auto-enable | MET | Q-2 contradiction between plan:25 and refs/claim.md:133 | MET | Q-10 retry after the Status move needs a fresh approval |
| **Subtotal** | **4/5** | | **4/5** | | **3/5** | |

**Edge-case floor check (needs at least 1/5 to be eligible as base):** V1 4/5 eligible, V2 4/5 eligible, V3 3/5 eligible. The probe gaps are real (V1 and V3 on I-5 and I-6; V2 and V3 on I-4), and each costs one criterion above, but none of the three falls below the floor.

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 5/5 | 5/5 | 4/5 |
| Correctness | 3/5 | 5/5 | 3/5 |
| Structure | 5/5 | 4/5 | 4/5 |
| Clarity | 4/5 | 4/5 | 3/5 |
| Risk Coverage | 4/5 | 3/5 | 3/5 |
| Invariant & Edge Case Coverage | 4/5 | 4/5 | 3/5 |
| **qual_score** | **25/30 = 0.8333** | **25/30 = 0.8333** | **20/30 = 0.6667** |

Supplementary figure, not part of the formula: the standalone invariant tally from `invariant-probe.md` (ADDRESSED 1, PARTIAL 0.5, UNADDRESSED 0, over I-1 to I-17): V1 10.5/17 = 0.618, V2 10.0/17 = 0.588, V3 6.0/17 = 0.353. The probe slightly favours V1 on standalone invariant coverage; this is the main reason the margin below is small, and the refactor plan imports V1's I-1, I-4, I-9 pieces for that reason.

## Position-Bias Mitigation

Pass 1 evaluated the variants in input order (V1, V2, V3). Pass 2 re-read every criterion in reverse order (V3, V2, V1). The criteria on which the two passes differed:

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|---|---|---|---|---|---|
| Completeness: dependencies | V3 | MET | NOT MET (the Task 4 on Task 1 line is conditional) | DISAGREE | MET: Task 15 on Task 9 and the cycle.py order are unconditional |
| Completeness: out-of-scope | V3 | NOT MET | MET ("Not a regression" notes) | DISAGREE | NOT MET: a regression note is not a scope exclusion |
| Correctness: terminology | V1 | NOT MET | MET ("compare-and-set" is common usage) | DISAGREE | NOT MET: probe I-4 limit says the read-then-write is not atomic |
| Clarity: terms defined | V2 | NOT MET | MET (V2 defines `[SCOPE+]` and `guard:N`) | DISAGREE | NOT MET: `W`, `WA`, `F`, `FS` stay undefined |
| Risk: at least 3 risks with probability and impact | V1 | MET | NOT MET | DISAGREE | NOT MET: no variant states a probability |
| Risk: at least 3 risks with probability and impact | V2 | MET | NOT MET | DISAGREE | NOT MET: same |
| Risk: at least 3 risks with probability and impact | V3 | MET | NOT MET | DISAGREE | NOT MET: same |
| Risk: monitoring mechanism | V2 | MET | NOT MET (Residual 3: nothing keeps checking) | DISAGREE | MET: `level_gated` audit reason plus Task 3a and introspection are validation mechanisms |

Disagreements re-evaluated: 8
Final verdicts changed: 3 (all on the probability criterion, one per variant; the change lowers every variant by one point equally and does not move the ranking)

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---|---|---|---|---|
| V1 (opus:security) | 0.4849 | 0.4167 | **0.9015** | 46.2% (6.0 of 13 points) |
| V2 (opus:architect) | 0.4920 | 0.4167 | **0.9087** | 53.8% (7.0 of 13 points) |
| V3 (sonnet:analyzer) | 0.4814 | 0.3333 | **0.8148** | 0% (0 of 13 points) |

**Margin**: V2 over V1 = 0.0072 (0.72 percentage points), below the 5% threshold. V2 over V3 = 0.0939.
**Tiebreaker applied**: Yes (A.4 step 1, debate performance). V2 won 7.0 of 13 scored points (see `debate-transcript.md` Scoring Matrix) against V1's 6.0, a gap of 7.7 points, above the 5% band, so step 1 decides without step 2. Step 2 (correctness count) would give the same answer: V2 5/5 versus V1 3/5.

Sensitivity: without the probability-criterion flip, V1 = 0.9182 and V2 = 0.9254; the margin is unchanged at 0.0072. The ranking V2 > V1 > V3 holds in both. The V2 over V1 lead is a tiebreaker result, not a score result; an owner who weights the standalone probe tally (V1 10.5 versus V2 10.0) more heavily could reasonably pick V1, and the refactor plan therefore carries every V1 element the verdicts adopted.

## Selected Base: Variant 2 (opus:architect), final score 0.9087

### Selection Rationale
- Top score by 0.0072 over V1; within 5%, so the debate tiebreaker applied and V2 won 7.0 of 13 scored points to V1's 6.0 (L3 points D-01a, D-02, D-03, D-05, D-07 plus L2 D-11).
- V2 is the only variant with no probe gap in its guard changes (I-5 and I-6 addressed; probe I-16 test-tree ordering addressed by moving 7 files). V1 and V3 each need a repair there before they could ship.
- V2 scores 5/5 on Correctness; V1 and V3 score 3/5.
- V2's weaknesses are all additive and were conceded by A2 (section 3): no label/project verbs, no Status compare-and-set, no coupling test, no "unreadable time voids", reason order, no self-approval control. Each has a V1 or V3 piece that drops in without restructuring V2's per-finding shape (see `refactor-plan.md`).
- V1 as base would need rework of its largest elements (module `ship_gate.py` plus Task 4b, `excluded_ids` default-on, item-time default, op-id marker, enumerated ISSUEWRITE list), which are the ones the debate rejected.

### Strengths to Preserve from Base
1. `'issue '*` catch-all after guard:652, with the guard version stamp bump to 2 (V2 Q-1).
2. Narrow coordinator-only patterns that keep `pytest tests/issue_pipeline/test_complete.py` allowed (V2 Q-1 item 4).
3. Option A/B/C structure with `[SCOPE+]` flags and the Task 3a owner action (V2 Q-2, Q-3).
4. Seven-file Task 6 scope and the Constraints line for files edited by several tasks (V2 Q-7, Q-10).
5. Refusal vocabulary `project_missing`, `project_ambiguous`, `status_option_missing` and the `^PVT_` check (V2 Q-5).

### Strengths to Incorporate from Non-Base Variants
1. From V1 Q-1 Part A: `label` and `project` verbs in the blocked class (V2 gets `'label '*`, `'project '*`, with `item-list` and `field-list` allowed first); guard test that an unrecorded session is allowed (V1 Q-9).
2. From V1 Q-1 Part B: `excluded_ids` as warn-first with `check-config` warning (default empty).
3. From V1 Q-2: the coupling test between the gate constant and `_PENDING`, without the module and Task 4b.
4. From V1 Q-3: "an unreadable time voids the approval".
5. From V1 Q-4: the check order (approval reread, time rule, equality).
6. From V1 Q-5: Status moves only from Research, Spec, Plan or Debug, otherwise comment only (`status_moved_by_person`).
7. From V1 Q-6 and A3: per-run marker (the key changes to the approval event id, R2 point 8).
8. From V1 Q-7: write the new `_PROMPT_RE` in the test, do not import it.
9. From V3 Q-3: same-second approval/item-time test case and the outcome decision table for Task 3a; per-finding rollback notes (for Task 22 docs) and the ranked impact table as an owner summary (Low value).
