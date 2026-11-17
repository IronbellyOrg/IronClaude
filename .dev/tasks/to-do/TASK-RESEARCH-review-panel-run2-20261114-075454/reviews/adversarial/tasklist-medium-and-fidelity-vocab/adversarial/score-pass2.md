# Qualitative Scoring, Position-Bias Pass 2 (Variant B evaluated first, then Variant A)

Slot X-15 `tasklist-medium-and-fidelity-vocab`. Scorer: independent pass 2 (reverse input order). Rubric: 30-criterion additive binary rubric, Claim-Evidence-Verdict (`sc-adversarial-protocol/SKILL.md` "Qualitative Scoring Layer (T04.02)" and `refs/scoring-protocol.md` A.2). Variants scored exactly as written (`variant-2-original.md` = B, `variant-1-original.md` = A); no credit for the Round 2 hybrids (A+, H+).

Code checked read-only at HEAD `50d4d2b9d` (paths under `src/superclaude/` unless noted): tasklist `SKILL.md:1351-1391, 1420-1422, 1439-1481, 1531-1615`; `commands/tasklist.md:113`; `output-styles/pragmatic.md:225-231`; `cli/review/findings.py:14-29, 96-101`; `findings_v2.py:35-36, 96-170`; `card_convert.py:71-83`; `cli/tasklist/{prompts,gates,commands,executor}.py`; `cli/roadmap/gates.py:195-240, 1322-1362`; `tests/skills/test_review_severity_rule.py:181-192, 268-283`; `tests/skills/test_worker_contract.py:777, 893-906, 1861`; `tests/tasklist/test_tasklist_fidelity.py:208-225`; fixture header and the 12 `group: tasklist` rows; both archived ValidationReports; `git show 80f934de5`.

## Variant B (Proposal B: Medium stays blocking, fidelity prompt stays outside the core)

### Completeness

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CO1 | Covers all explicit requirements | MET | Sections 1-8 cover the Medium decision, the fidelity-prompt placement, core and module consequences, evidence E1-E9, invariants, tests M-X15-1..4, PR/rf-qa effect (section 6) and C-01..C-03 (section 7). |
| CO2 | Edge cases and failure scenarios | MET | Section 4 "Endangered": a reviewer typing `MAJOR` with `blocking: false` drops the row (INV-016); a stalled Medium ends via the P2 monotonicity halt, the 2-pass cap and `blocked` (`SKILL.md:1610-1615`, verified). |
| CO3 | Dependencies and prerequisites | MET | Section 7: "if any of those is reopened, B is reopened with it", naming C-01 "no core change", C-02 "typed authority", C-03 "per-profile policy". |
| CO4 | Success/completion criteria | MET | Section 5: "Pre-registered threshold: a majority of at least 2/3 either way; between 1/3 and 2/3 ... 'the label is mixed'"; M-X15-3 requires the existing pins to pass unchanged. |
| CO5 | Explicit out of scope | MET | Section 2 last paragraph: spec loop, reflect, PR-review and rf-qa modules "untouched by this slot"; section 7: "B has no position on the quorum gate, `defer` or the verdict surface". |

### Correctness

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CR1 | No factual errors or hallucinated claims | NOT MET | Checked at HEAD: `_tasklist_ready_consistent` is cited `:195-233` but ends at `:240`; severity text is cited `prompts.py:28-62` but spans `:49-69` (MEDIUM ends `:64`); the Medium-passes test is cited `:208-221` but runs to `:225`. E6 says the archived acceptance-list gaps are "what the CLI prompt would call HIGH or near it", yet `prompts.py:62` lists "Acceptance criteria are weaker than the roadmap's success criteria" as a MEDIUM example. |
| CR2 | Technical approach feasible | MET | The map High->CRITICAL/true, Medium->MAJOR/true, Low->MINOR/false parses in v1 (`findings.py:100-101`) and in v2 with `reflect_category` (`findings_v2.py:161-162` needs `blocking == (severity != MINOR)`), both verified; it correctly rejects `card_convert.py:71-83` as the source of the map. |
| CR3 | Terminology consistent and accurate | MET | "Label map", `blocking` and the skill-versus-CLI scales are used consistently, and the collision with the S1-S5 Medium is named ("two scales for two jobs", "a name collision with the S1-S5 sub-tier"). |
| CR4 | No internal contradictions | NOT MET | Section 1 calls Medium-as-blocking "the tasklist skill's own model, which pragmatic.md S4 permits", but section 8 concedes "the skill states no model and no definition of Medium" and section 2 has the S4 statement only added by B's own edit (verified: no S4/pragmatic hit in the skill). |
| CR5 | Claims supported by evidence | MET | E1 cites six `SKILL.md` sites (all verified: `:1439, :1537, :1567, :1608, :1610, :1614`); E3 cites 12 tasklist rows of 139 (both counts verified); E6/E7 cite the two archived report headers (verified lines 6 and 7). |

### Structure

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| ST1 | Prerequisites before dependents | NOT MET | Section 2 relies on the C-01/C-02/C-03 outcomes ("section 7 below"), but that material sits in section 7, after design, evidence, invariants, tests and effect. |
| ST2 | Consistent hierarchy depth | MET | Eight H2 sections, no H3, no orphaned subsections. |
| ST3 | Separation of concerns | MET | Position, design, evidence, invariants, tests, consumer effect, slot consistency and objection each get their own section. |
| ST4 | Navigation aids | MET | Numbered sections and labelled E1-E9 and M-X15-1..4 are cross-referenced later ("(E4, E6)", "section 4", "section 7 below"). |
| ST5 | Follows artifact-type conventions | MET | Follows the proposal layout the brief requires (position, design consequence, evidence, invariants, test, PR/rf-qa effect, adjudicated-slot consistency, strongest objection) with a Status line and evidence tags. |

### Clarity

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CL1 | Unambiguous language | MET | Only a quoted "could" and one scoped "possibly demote it" in the section 8 stop condition; no advisory hedging of the position. |
| CL2 | Concrete, specific actions | NOT MET | The only new text B adds, "a definition" of Medium and an S4 sentence (section 2), is never written out, so the definition that would resolve the Medium collision is absent. |
| CL3 | Each section has a clear purpose | MET | Section titles state the purpose ("The position", "Evidence", "Invariants", "Test or measurement"). |
| CL4 | Terms defined on first use | NOT MET | S4, C-S3, INV-016, `F_k`, `refs_norm` and T5 are used in sections 1-2 without a gloss; the S4 text is quoted only in E4 and INV-016 explained only in section 4. |
| CL5 | Actionable next steps/decision points | MET | Section 5 pre-registers the rule; section 8: "Where the answer stops: if M-X15-1 finds that most Medium findings are wording or ambiguity ... the objection stands". |

### Risk Coverage

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| RK1 | At least 3 risks with probability and impact | NOT MET | Section 4 lists five exposures, but only two carry an impact label ("MEDIUM", "LOW to MEDIUM") and none carries a probability. |
| RK2 | Mitigation for each risk | NOT MET | "One product, two meanings" is accepted and "does not remove it", and the unpinned new Medium definition and S4 sentence have no mitigation. |
| RK3 | Failure modes and recovery | MET | Section 4 C-03 bullet: a stalled Medium ends in "the P2 monotonicity halt, the 2-pass cap and the `--unattended` outcome `blocked`", a human decision (`SKILL.md:1610-1615`, verified). |
| RK4 | External dependencies and failure | MET | Section 7 states what reopening C-01/C-02/C-03 does; E9 shows the shared six-field contract with `SPEC_FIDELITY_GATE` (`roadmap/gates.py:1322-1345`, verified) and what moving the prompt would break. |
| RK5 | Monitoring/validation mechanism | MET | M-X15-1..4, including a static check that no `Medium` token enters `findings.py`, `findings_v2.py`, `ledger.py` or the ledger JSON. |

### Invariant & Edge Case Coverage

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| IE1 | Collection boundaries (empty/single/max) | MET | E7: both archived bundles have High 0, so the zero-blocking short-circuit would leave 4 and 2 Medium findings unpatched; the P2 loop is capped at 2 total passes. |
| IE2 | State interactions across boundaries | MET | The label map is checked against the v2 `reflect_category` rule, and E9 covers the tasklist CLI and roadmap `SPEC_FIDELITY_GATE` sharing one frontmatter contract. |
| IE3 | Guard condition gaps | MET | Section 4: "a tasklist reviewer that types `MAJOR` with `blocking: false` drops the row" (no floor for MAJOR); E5: `_tasklist_ready_consistent` reads only the high count (verified). |
| IE4 | Count divergence | MET | Section 2: the P2 loop's cap is not folded into the ledger's `cap_reviews` of 3, "so the cap unit mismatch ... stays a documented difference" (2 total passes versus 3 reviews). |
| IE5 | Interaction effects | MET | Section 4: counting Medium as blocking "enlarges the set of rows that can stall a loop" (C-03 dependency 2); E9: moving the prompt would alter the roadmap pipeline's frontmatter. |

## Variant A (Proposal A: Medium becomes a non-blocking warning, fidelity prompt becomes a tasklist-module vocabulary)

### Completeness

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CO1 | Covers all explicit requirements | MET | Sections 1-8 cover the decision, core/module/CLI consequences (2.1-2.3), a 16-row evidence table, invariants, T1-T4 and M1-M2, PR/rf-qa effect (section 6) and C-01..C-03 (sections 0 and 8). |
| CO2 | Edge cases and failure scenarios | MET | 4.2 items 2-5 (Medium-only run now completes, monotonicity halt silent on Medium, misgrade decides blocking, omission regrade is a judgement); INV-I synthetic-High and zero-success terminal kept (`SK:1400-1401`, `:1431`, verified). |
| CO3 | Dependencies and prerequisites | MET | Section 0 table "Outcome I rely on" for C-01, C-02, C-03 and the section 8 per-slot dependency list. |
| CO4 | Success/completion criteria | MET | T1-T4 "red before the change, green after, none needs a model call", plus "The result that would show the position right ... wrong" in section 5 (threshold left unset, flagged under CL5). |
| CO5 | Explicit out of scope | MET | Section 9 "Not claimed" (no claim B is wrong, no branch/PR plan, no risk register) and section 0 "C-05 ... was not an input". |

### Correctness

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CR1 | No factual errors or hallucinated claims | NOT MET | Section 2.2 says the pinned phrase "the unresolved High or Medium HALT resolves as blocked" changes "in the skill and in both pins", but that phrase exists only in `commands/tasklist.md:113` (grep of `SKILL.md`: no hit), a file A's edit list omits, so T1 would stay red. Also `_tasklist_ready_consistent` cited `:195-239` (ends `:240`), `:1445` listed as an edit site though it names no label, and fact 7 reads S5 (`pragmatic.md:229`, CRITICAL/IMPORTANT/MINOR only) as a "three-label scale" rule. |
| CR2 | Technical approach feasible | NOT MET | 4.2 item 4 lists "the any-reviewer union of C-03 (a High typed by one reviewer of the cluster keeps the row blocking)" as a mitigation, but Stage 7 gives each task one grader (`SKILL.md:1351-1368`: Agent A tasks 1..split, Agent B split+1..), so no cluster exists; Form 2 "in the way `reflect_category` already does" is not reusable because that rule also pins `category` (`findings_v2.py:159-160`). |
| CR3 | Terminology consistent and accurate | MET | "Label map", "core pair", `blocking` and the evidence tags are used consistently; the S5 over-read is scored under CR1, not here. |
| CR4 | No internal contradictions | NOT MET | Section 0 says "Position A needs no engine change" and 2.1 says "Nothing else in the core changes", yet 2.1 says Form 2, a parse-edge core hook, "is the one this proposal prefers"; fact 13 calls the CLI "a separate roadmap-pipeline validator" while section 7 answer 3 argues "one product should not have a gate that passes a report and a skill that halts on the same row". |
| CR5 | Claims supported by evidence | MET | Section 3 is a 16-row Fact/Source/Tag table; rows 4-6 hold against `gates.py:23-46`, `executor.py` HIGH-only exit and `prompts.py:51-69` (verified). |

### Structure

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| ST1 | Prerequisites before dependents | MET | Section 0 "Inputs and dependencies" (slot table) precedes the position and the design. |
| ST2 | Consistent hierarchy depth | MET | Ten H2 sections; H3 appears only under sections 2 and 4, each with 2-3 children. |
| ST3 | Separation of concerns | MET | Evidence is isolated in the section 3 table; invariants split into 4.1 preserved and 4.2 endangered; tests and consumer effects have their own sections. |
| ST4 | Navigation aids | MET | An abbreviation legend (`SK`, `PR`, `GT`, `RG`, `PM`, `RT`), numbered facts and cross-references such as "4.2 item 1" and "section 2.2". |
| ST5 | Follows artifact-type conventions | MET | Same required proposal layout (position, design consequence, evidence, invariants, tests, consumer effect, objection, slot dependencies) with Status line and evidence tags. |

### Clarity

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| CL1 | Unambiguous language | MET | The only "may" uses are descriptive ("MAJOR may be non-blocking") or inside the quoted objection; no advisory hedging. |
| CL2 | Concrete, specific actions | MET | Names the edit sites (`:1439, :1537, :1567, :1608, :1610, :1614`), adopts the High/Medium/Low definitions from `prompts.py:51-69`, regrades `SKILL.md:1421-1422` to High, and lists T1-T4. |
| CL3 | Each section has a clear purpose | MET | Titled sections with stated purpose ("Inputs and dependencies", "Not claimed"). |
| CL4 | Terms defined on first use | NOT MET | C-S3, SV-6, CO-41, S1-S5, INV-016 and `refs_norm` are first used without a gloss (S1-S5 content appears only in fact 7). |
| CL5 | Actionable next steps/decision points | MET | T1-T4 are runnable steps and section 5 states "The position is wrong if defects ... land in Medium at a rate above a threshold" (the threshold itself is left unset, "not set here"). |

### Risk Coverage

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| RK1 | At least 3 risks with probability and impact | NOT MET | 4.2 lists six costs, none with a probability; only INV-016 carries an impact label ("MEDIUM, unaddressed"). |
| RK2 | Mitigation for each risk | NOT MET | 4.2 items 2 (loosened gate) and 3 (monotonicity halt silent on Medium) have no mitigation, and item 4's union mitigation is not available at Stage 7 (see CR2). |
| RK3 | Failure modes and recovery | MET | 2.2 keeps the `--unattended` -> `blocked` resolution for open blocking findings; 4.2 item 4 names the misgrade failure mode with mitigations (definitions, blind grading test). |
| RK4 | External dependencies and failure | MET | 4.2 item 6: hand-kept skill and CLI-prompt definition texts "can drift between releases"; section 8 states the C-02 `brief_ids` and C-03 condition-2 dependencies. |
| RK5 | Monitoring/validation mechanism | MET | T2 parity test over skill block, `build_tasklist_fidelity_prompt` output and label map; T4; M1 blind grading; M2 Medium-row audit. |

### Invariant & Edge Case Coverage

| ID | Criterion (short) | Verdict | Evidence |
|---|---|---|---|
| IE1 | Collection boundaries (empty/single/max) | MET | 4.2 item 2: a run whose only residual findings are Medium (empty blocking set, non-empty Medium set) now completes; zero-success Stage 7 stays the validation-error terminal (`SK:1431`). |
| IE2 | State interactions across boundaries | MET | 2.1: a v2 tasklist module "must not set `reflect_category`" (`findings_v2.py:161-162`, verified); `tasklist_ready` is checked only against the typed `high_severity_count` (verified `roadmap/gates.py:208-239`). |
| IE3 | Guard condition gaps | MET | 2.1 Form 1: "the parser accepts `MAJOR` with either `blocking` value, so the rule rests on the brief"; `_tasklist_ready_consistent` never reads the report body. |
| IE4 | Count divergence | MET | 4.2 item 3: `\|F_k\|` counts High only, so the monotonicity halt (`SK:1611`) stops firing on Medium churn; the 139-row count is held while 12 rows are rewritten. |
| IE5 | Interaction effects | MET | 4.2 item 4: the C-02 CRITICAL floor keys on the typed severity, so a High typed MAJOR non-blocking drops the row; section 8: fewer blocking rows lowers C-03 condition-2 cost. |

## Dimension subtotals and totals

| Dimension | Variant B | Variant A |
|---|---|---|
| Completeness (CO) | 5/5 | 5/5 |
| Correctness (CR) | 3/5 (CR2, CR3, CR5) | 2/5 (CR3, CR5) |
| Structure (ST) | 4/5 (ST1 NOT MET) | 5/5 |
| Clarity (CL) | 3/5 (CL2, CL4 NOT MET) | 4/5 (CL4 NOT MET) |
| Risk Coverage (RK) | 3/5 (RK1, RK2 NOT MET) | 3/5 (RK1, RK2 NOT MET) |
| Invariant & Edge Case (IE) | 5/5 | 5/5 |
| **Total** | **23/30 (qual 0.767)** | **24/30 (qual 0.800)** |

Edge Case Floor (Invariant & Edge Case Coverage >= 1/5): Variant B 5/5, eligible. Variant A 5/5, eligible. Floor not suspended.

## Notes for the merge of passes

- The 1-point margin comes from three asymmetric calls: ST1 (A has the dependency table first, B puts it in section 7 after the design that relies on it), CL2 (B never writes the Medium definition it promises) and CR2 (A's union mitigation and Form 2 reuse do not hold against `SKILL.md:1351-1368` and `findings_v2.py:159-160`), partly offset by B failing none of A's two Correctness defects and A's CR1 finding being the heavier code-fact miss (the pinned phrase lives in `commands/tasklist.md:113`, not the skill).
- Calls most likely to flip on a different reading: CR1 for both (line-range slips versus the verified A phrase-location miss and B E6 overreach), CL2 for B, ST1 for B, and CL4 for both (first-use glosses).
- Both variants score 0 on RK1 and RK2 for the same reason: no probabilities and no mitigation for every listed risk.
