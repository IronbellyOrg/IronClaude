# Debate 02 — Spec Fidelity Gate Hardening

**Date**: 2026-03-17
**Proposal under debate**: `proposal-02-spec-fidelity-hardening.md`
**Scoring framework**: `scoring-framework.md`
**Reference incident**: cli-portify executor no-op bug — v2.24, v2.24.1, v2.25
**Debate format**: 3-round structured adversarial transcript + scoring

---

## Participants

- **Proponent (P)**: Advocates for implementing Proposal 02 as specified.
- **Devil's Advocate (DA)**: Challenges the proposal's assumptions, scope, and effectiveness.

---

## Round 1 — Opening Positions

---

### Proponent — Opening Statement

Proposal 02 addresses a structural vulnerability in how the `SPEC_FIDELITY_GATE` operates. Today that gate is a two-stage system: an LLM produces a deviation report with severity classifications, and Python deterministically enforces that the report's metadata satisfies `high_severity_count == 0` and `tasklist_ready == true`. The problem is that the Python enforcement is only as good as the LLM's analysis. The enforcement layer is rigorous; the analysis layer has no programmatic floor beneath it.

The cli-portify incident is the clearest demonstration of this vulnerability. The v2.24 and v2.25 specs defined the executor's dispatch architecture with specificity: a `PROGRAMMATIC_RUNNERS` dictionary, a three-way dispatch (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`), and a module dependency graph showing `executor.py` importing from eight `steps/*.py` modules. The generated roadmap replaced all of that with a single phrase: "sequential execution with mocked steps." Every element of the spec's dispatch architecture disappeared. And the `SPEC_FIDELITY_GATE` — which was running in blocking mode — did not catch it.

The forensic report's Appendix B states the reason directly: there is no programmatic parsing of requirement IDs, no cross-reference verification, no enumeration completeness check. The gate cannot catch what the LLM does not surface. If the LLM omits a deviation — whether through hallucination, context window drift, or misclassification — the gate passes as if no deviation exists.

Proposal 02 adds a pre-LLM deterministic inventory pass that is immune to these failure modes. Checks D-03, D-04, and D-05 each independently and deterministically target the exact failure that occurred:

- **D-03**: `PROGRAMMATIC_RUNNERS` appears in the spec. A substring search finds it absent from the roadmap. `dispatch_tables_preserved: false`. Gate halted. This requires no LLM, no probabilistic reasoning, and no threshold calibration. It is a string lookup.
- **D-04**: `_run_programmatic_step`, `_run_claude_step` appear in the spec's pseudocode fences. Neither appears in the roadmap. `pseudocode_dispatch_preserved: false`. Gate halted. Same properties — pure regex over string content.
- **D-05**: The roadmap Milestone M2 text includes "Sequential pipeline runs end-to-end with mocked steps." The `mocked steps` pattern fires. `stub_sentinels_found: true`. Gate halted. This would have caught the problem even if D-03 and D-04 were absent.

Any one of these three checks would have blocked the roadmap before tasklist generation. Together, they constitute a defense-in-depth that requires the LLM to simultaneously miss all three independent signals — which is not a credible failure scenario.

The spec-side fix is correct precisely because this is where the corruption entered the pipeline. The forensic report's Section 5 is clear: "Link 1: Spec → Roadmap — FAILED." Link 2 passed because it faithfully propagated the already-corrupted roadmap. Link 3 does not exist. Fixing Link 1 deterministically stops the corruption at entry. Fixing Link 2 or 3 without fixing Link 1 allows corrupted requirements to propagate further before detection — increasing remediation cost.

The proposal is also scoped correctly for its purpose. It supplements the LLM comparison rather than replacing it. It makes no claim to catch all possible fidelity failures. It makes a specific, verifiable claim: D-03 + D-04 + D-05 would have blocked the cli-portify roadmap. Section 5.1 of the proposal provides the exact replay — every input, every regex match, every gate failure — with citations to specific lines and sections of the forensic report and the spec. This is not a theoretical argument. The incident artifacts are in `.dev/releases/complete/v2.25-cli-portify-cli/` and the regression test `test_run_deterministic_inventory_cli_portify_case` will verify this claim with every test run.

Finally, the proposal is independently implementable in 12-17 hours without depending on any other v1.2.1 proposal. The `fidelity_inventory.py` helper module is pure Python with no subprocess calls, no LLM invocations, and no cross-module dependencies. The semantic check functions follow an existing pattern that is already present in `roadmap/gates.py`. This is a low-risk, moderate-complexity addition to infrastructure that already exists and already runs on every roadmap generation.

---

### Devil's Advocate — Opening Statement

Proposal 02 makes a compelling narrative argument and a weak engineering one. The gap between what it claims to catch and what it would actually catch in practice is significant enough to warrant caution before adoption.

**Attack Vector 1: The vacuous pass problem — the cli-portify specs did not use FR-NNN identifiers**

The proposal leads its check suite with D-01: "Verify that every FR-NNN, NFR-NNN, and SC-NNN identifier found in the spec appears in the roadmap." The proposal itself acknowledges in Section 6.3: "many specs in the project — especially early-stage or informal specs — do not use formal FR-NNN notation." The forensic report confirms this: the tasklist forensics section searches for `step_runner`, `PROGRAMMATIC_RUNNERS`, and `dispatch` in the tasklist files, not for `FR-NNN` identifiers. The v2.24 and v2.25 specs used narrative prose and pseudocode blocks to specify the dispatch architecture, not a labeled requirements taxonomy.

D-01 is therefore irrelevant to the incident it claims to prevent. It would have passed vacuously, contributing nothing. The proponent's own Section 5.1 admits this: "D-01: Likely, if the spec used FR-NNN notation." That qualifier is load-bearing. The check that carries 20% of the proposed suite's perceived rigor produces no output on the actual incident artifacts.

**Attack Vector 2: Detecting dropped natural language requirements requires parsing informal text — this is fragile**

The real architectural decision that was dropped — the three-way dispatch, the `PROGRAMMATIC_RUNNERS` dictionary, the `executor.py → steps/*.py` wiring — was described in a combination of pseudocode blocks, prose paragraphs, and module dependency diagrams. Proposal 02 attempts to extract these through a collection of regex patterns:

- `_DISPATCH_TABLE_PATTERN`: Matches `UPPER_CASE_NAME = {` or `UPPER_CASE_NAME dict(`. This would catch `PROGRAMMATIC_RUNNERS` if and only if the spec contains the literal text `PROGRAMMATIC_RUNNERS = {`. If the spec says "a programmatic runners dictionary" in prose, or uses a code fence with different formatting, D-03 produces no inventory entry.
- `_STEP_DISPATCH_CALL`: Matches `step_result = _run_*()` patterns specifically. The v2.25 spec pseudocode happens to use this pattern. A spec author who writes `result = dispatch_programmatic(step, config)` or `outcome = self._run_programmatic(...)` would not be caught by D-04.
- `_DEP_ARROW_PATTERN`: Requires `A --> B.py` or `A ──> B.py` syntax with specific Unicode arrows. A diagram using `A -> B` (plain ASCII, no `.py` suffix) may or may not match.

These are brittle matchers that happen to be calibrated to the v2.25 spec's specific formatting choices. They are not general-purpose requirement extractors. The forensic report's description of the spec dispatch design — "explicit pseudocode" — understates how spec-format-dependent these patterns are. Change the spec authoring convention slightly and the checks silently degrade.

**Attack Vector 3: This fixes Link 1 but the real damage propagated through Links 2 and 3**

The forensic report's Section 5 lays out the failure chain clearly:

- Link 1 (Spec → Roadmap): FAILED — dispatch architecture dropped
- Link 2 (Roadmap → Tasklist): PASSED VACUOUSLY — tasklist faithfully reproduced the already-corrupted roadmap
- Link 3 (Tasklist → Code): DOES NOT EXIST

Proposal 02 addresses only Link 1. But the deeper issue is that **even if Link 1 had been perfect**, the bug still would have been possible through a different path. Consider: what if a developer manually edits the roadmap after the gate passes? What if the spec-fidelity gate fires but the remediation prompt is followed incorrectly? What if a future spec describes dispatch architecture in a different format that D-03 and D-04 don't parse? In all these scenarios, the corruption still reaches the code because Links 2 and 3 have no programmatic floor.

More precisely: D-05 is the strongest single check in this proposal. "Mocked steps" in a milestone is a high-confidence signal. But the forensic report reveals that the "mocked steps" language in the roadmap was not the root cause — it was a symptom that the spec's dispatch architecture had already been discarded. The root cause is that the LLM's roadmap generation chose not to carry forward the `PROGRAMMATIC_RUNNERS` table. D-05 catches the symptom; D-03 and D-04 are closer to catching the root cause, but only if the spec was written with the exact patterns these regexes target.

**The core indictment**: Proposal 02 is a regression test, not a detection system. It is calibrated to the specific formatting conventions of one incident's artifacts. It would have caught this incident. It provides uncertain protection against the next incident where the spec uses different formatting, where the dropped element is a prose paragraph rather than a pseudocode block, or where the roadmap introduces an entirely new abstraction that replaces the spec's dispatch model without using any of the sentinel terms this proposal checks for.

---

## Round 2 — Cross-Examination

---

### Proponent Responds to the Vacuous Pass Objection (D-01 and FR-NNN conventions)

The Devil's Advocate correctly identifies that D-01 provides no value for specs without FR-NNN identifiers, and that this is a significant limitation for the current spec corpus. This objection is well-founded and must be conceded on its own terms.

However, the DA misunderstands the proposal's dependency structure. D-01 is not load-bearing for the cli-portify incident catch claim. The proposal's Section 5.1 explicitly identifies D-03, D-04, and D-05 as the independently sufficient checks, and D-01 as conditional. The check suite is designed as defense-in-depth: any single check triggering halts the pipeline. D-01 represents incremental value for specs that adopt formal ID conventions — a practice the CLI tooling encourages. Its vacuous pass behavior for informal specs is correct and documented, not a failure mode.

The DA's real objection is that the suite's headlining check fails on the incident. This is true. The response is: remove D-01 from the headline claim and evaluate D-03 + D-04 + D-05 on their own merits. Those three checks are not format-conditional in the same way. `PROGRAMMATIC_RUNNERS = {` appears verbatim in the spec because specs document Python code. `_run_programmatic_step(` appears verbatim because specs quote pseudocode. "Mocked steps" appears verbatim in the roadmap because a developer wrote it. These are not arbitrary pattern choices — they are artifacts of how Python architecture is specified in this codebase.

The DA's objection that "a spec author who writes differently would not be caught" proves too much. By this logic, no regex-based check should be written because some author might use different syntax. The practical question is: how were the actual failing specs written? The forensic report answers this. The actual specs used these exact patterns. The actual roadmap used "mocked steps." A check that catches the actual incident is valuable even if it would miss a differently-written incident.

On the brittleness concern: D-03's `UPPER_CASE = {` pattern is robust to normal Python pseudocode variation because uppercase dictionary names are a Python convention, not a style choice. A dictionary named `PROGRAMMATIC_RUNNERS` will appear with that capitalization in any spec that references it. D-05 is even more robust: "mocked steps" is colloquial English that developers use without thinking, which is exactly why it appears in the roadmap and why it is a reliable signal.

---

### Devil's Advocate Attacks D-05 Stub Sentinel Detection (False Positives in Test Strategy Sections)

The Proponent's defense of D-03, D-04, and D-05 is strongest for D-03 and D-04 but weakest for D-05. Let us examine D-05 in detail.

The proposal's Section 6.2 acknowledges: "Many roadmaps legitimately describe test strategies that use mocked dependencies. A roadmap that says 'Unit tests will use mocked step implementations to isolate executor logic' should not trigger D-05." The assessed likelihood of this false positive is "High." The mitigation — section-scope filtering that exempts `## Test Strategy` and `## Testing` headings — introduces implementation complexity that the effort estimate does not adequately account for.

Consider what section-scope filtering requires: the check must parse the roadmap's Markdown heading structure, identify which headings correspond to test-related sections, and suppress D-05 pattern matches within those sections. This means the check must correctly identify heading boundaries (ATX headings `##`, `###`, Setext-style headings, nested sections), handle roadmaps where test strategy discussion is embedded within milestone sections rather than a separate heading, and avoid suppressing matches that appear in a milestone section that merely contains a sentence about testing.

The proposal's `extract_stub_sentinels()` function as specified does not implement any of this. It does a flat line-by-line scan with no section awareness. The section-scope mitigation is described in prose in Section 6.2 but is not reflected in the code specification. This means the implementation as specified would have a high false positive rate against any roadmap that discusses mocking in a test strategy section — which is most roadmaps.

There is a deeper problem. The sentinel `mocked steps` matches both:
1. "Sequential pipeline runs end-to-end with **mocked steps**" (milestone M2, a true positive — the roadmap is reducing a real requirement to a placeholder)
2. "Unit tests for the executor will use **mocked steps** to isolate the `run()` loop" (a test strategy sentence, a false positive — this is a legitimate testing pattern)

The lexical distinction between these two uses requires understanding context that simple regex cannot provide. The section-scope filter helps if the author has placed these sentences in different sections. But what if a roadmap has a combined milestone-and-testing section? What if the test strategy is described inline with the milestone? The `no.op default` and `wired later` patterns are higher-confidence, as the proposal notes, but "mocked steps" is the pattern that actually appears in the incident artifact.

Furthermore, during TDD workflows — which this codebase uses — it is legitimate and intentional to specify in a roadmap's early phases that implementations begin with mocked steps. A Phase 1 milestone saying "executor skeleton with mocked step dispatch" is a correct description of a TDD scaffolding phase. D-05 would flag this as a HIGH severity finding, blocking the pipeline from proceeding through a perfectly valid TDD approach. The proposal's context filter (match must appear within 200 characters of a milestone marker) does not help here — TDD phase descriptions appear in milestone sections by definition.

The false positive risk for D-05 is not "occasional" (the scoring framework's 6-7 range). In practice, for any project using TDD methodology, it is systematic.

---

## Round 3 — Synthesis

---

### What the Proposal Gets Right

**Both parties agree on the following:**

1. **The core diagnostic is correct.** The `SPEC_FIDELITY_GATE`'s enforcement layer is rigorous but its analysis layer has no programmatic floor. A gate that enforces only the metadata of an LLM-generated report provides deterministic enforcement of a non-deterministic input. Adding deterministic pre-checks underneath the LLM analysis is architecturally sound.

2. **D-03 and D-04 are strong checks on the actual incident artifacts.** `PROGRAMMATIC_RUNNERS` and `_run_programmatic_step` appear verbatim in the specs and are absent from the roadmaps. A substring check would have produced `dispatch_tables_preserved: false` and `pseudocode_dispatch_preserved: false` regardless of what the LLM did. These are the strongest checks in the suite.

3. **The fail-closed principle is correct.** The proposal's design — deterministic inventory results are merged into frontmatter by the step runner even if the LLM omits them — is the right failure model. Unknown state must not pass.

4. **The `fidelity_inventory.py` helper module design is reusable.** The proposal explicitly notes that the same logic applies to `TASKLIST_FIDELITY_GATE` (Link 2). Building it as a standalone module with a clean API (`run_deterministic_inventory(spec_text, roadmap_text) -> dict`) makes it available for Link 2 hardening without duplication.

5. **The regression test `test_run_deterministic_inventory_cli_portify_case` is essential.** Using the actual incident artifacts as a test fixture anchors the implementation to the real failure, prevents regression, and provides documentation of the exact failure mode. This test should survive any refactoring.

---

### What the Proposal Misses

**Both parties agree on the following:**

1. **D-01 is weak for the current spec corpus.** FR-NNN conventions are not universally adopted. D-01 provides value only for specs that use formal ID notation. It should be framed as an "when applicable" check rather than a primary defense, and its implementation effort should be weighed against its limited near-term catch rate.

2. **D-05 has a genuine false positive problem for TDD workflows.** The section-scope mitigation described in Section 6.2 is correct in principle but absent from the code specification. D-05 as specified (flat line scan, no section awareness) will produce false positives in any roadmap that describes test strategy using mocking language. The mitigation must be part of the implementation spec, not deferred prose.

3. **The proposal fixes Link 1 but does not address the systemic vulnerability.** Even with Link 1 hardened, the corruption could re-enter through Link 2 (manual roadmap edits post-gate, or a future spec format that the patterns miss) or through Link 3 (which still does not exist). The proposal does not claim to be sufficient — Section 5.1 says "D-03, D-04, and D-05 would have blocked" — but users of this proposal must understand that it is one layer in a required multi-layer defense.

4. **The proposal is calibrated to this incident's spec formatting.** D-03's `UPPER_CASE = {` pattern and D-04's `step_result = _run_*()` pattern are well-matched to how this codebase writes specs. They will miss dispatch architectures described in prose without pseudocode, or using different naming conventions. This is an accepted limitation but must be documented at the gate level.

5. **The stub sentinel detection at D-05 conflates symptom with cause.** "Mocked steps" in a milestone is a symptom that the spec's dispatch requirements were dropped. D-03 and D-04 detect the actual dropped elements. D-05 detects the language used to describe the reduced implementation. These are complementary signals, but D-05 is the one most prone to false positives and most likely to be suppressed by future teams who learn to avoid sentinel words without fixing the underlying omission.

---

### Necessary Condition, Sufficient Condition, or Neither?

**Devil's Advocate's position**: Proposal 02 is a **necessary but not sufficient** condition for preventing this class of bug. It addresses one layer (Link 1) of a three-layer failure. Link 3 does not exist; Link 2 has the same LLM-floor problem that this proposal fixes for Link 1. A future version of this bug could appear if a spec uses pseudocode formatting that D-03/D-04 miss, or if a developer edits the roadmap after gate passage. Proposal 02 raises the bar substantially but does not close the class.

**Proponent's position**: This framing is correct and was never disputed. The proposal explicitly states it addresses Link 1 and notes that Link 2 and Link 3 hardening are out of scope but share the `fidelity_inventory.py` module. Necessary-but-not-sufficient is the correct characterization for a single proposal in a five-proposal backlog. The question is whether the Link 1 contribution is worth implementing on its own timeline, and it is — D-03 and D-04 each independently provide blocking protection against the specific failure mode that occurred, with low implementation risk and no false-positive risk.

**Synthesis**: Proposal 02 is a **necessary condition** for the full fidelity chain hardening, is **not sufficient** on its own, and provides **substantial incremental value** when implemented independently. The three checks that matter (D-03, D-04, D-05 with section-aware implementation) should be treated as the core deliverable. D-01 and D-02 are secondary.

---

## Scoring

### Axis 1 — Catch Rate (weight 25%)

**Score: 7/10**

**Evidence for**: D-03 (`PROGRAMMATIC_RUNNERS` absent from roadmap), D-04 (`_run_programmatic_step` absent from roadmap), and D-05 ("mocked steps" in Milestone M2) each independently and deterministically trigger on the v2.25 incident artifacts. The Appendix A replay walkthrough provides exact match results. Any one of D-03, D-04, or D-05 would have halted the pipeline before tasklist generation. The forensic report (Section 5) confirms that all three signals were present in the incident artifacts.

**Evidence against**: D-01 provides no catch value because the v2.24/v2.25 specs do not use FR-NNN identifiers — vacuous pass. D-02's module dependency check provides coverage but depends on the exact `──>` arrow syntax used in the spec, which may not generalize. The proposal operates at Link 1 only; if the spec itself had been written to omit the dispatch architecture (e.g., if the requirement had never been written down), all five checks would pass while the bug was still introduced at implementation time.

**Score justification**: "Would have caught it with high probability given normal workflow adherence" — the three operational checks (D-03, D-04, D-05) are robust to the incident. Score is 7 rather than 8-9 because D-05 requires section-aware implementation to avoid false-positive-driven suppression (teams disabling the gate), and D-01's vacuous pass on the exact incident artifacts means one of five checks contributed nothing. Would be 9/10 if the spec used FR-NNN notation universally.

---

### Axis 2 — Generalizability (weight 25%)

**Score: 6/10**

**Evidence for**: The `UPPER_CASE_DICT = {` pattern (D-03) and pseudocode dispatch call pattern (D-04) are applicable to any spec in this codebase that defines a named dispatch structure with Python pseudocode. The forensic report's Axis 2 evidence anchor identifies three other "defined but not wired" instances: `DEVIATION_ANALYSIS_GATE` (defined in `roadmap/gates.py:712-758` but not wired from `_build_steps()`), `SprintGatePolicy` (stub in `sprint/executor.py:47-90`), and `TrailingGateRunner` (never called from `execute_sprint()`). D-05's sentinel detection would catch any future roadmap that uses "mocked steps," "stubbed dispatch," or "wired later" language for any component — not just executor dispatch. D-03 would catch `COMMAND_MAP`, `STEP_REGISTRY` (if it contained function references in the spec), and `ROUTE_HANDLERS` if they were defined in a spec and dropped from a roadmap.

**Evidence against**: The three additional "defined but not wired" instances cited in the forensic report are code-level integration bugs, not spec-to-roadmap drops. D-03 and D-04 would only catch them if the wiring architecture was specified in a spec document that then went through the roadmap pipeline — which is not the case for `DEVIATION_ANALYSIS_GATE` or `TrailingGateRunner`. Those are existing code-level issues. The checks do not address the wiring problem in code; they address the spec-to-roadmap documentation problem. The proposal's generalizability is to the class of "spec defines X; roadmap omits X" — which is real and recurring — but not to the class of "code implements X incompletely" which requires Proposal 03 or 05.

**Score justification**: Catches the "spec dispatch table dropped from roadmap" class, applicable across all specs that use pseudocode. Does not catch the "code integration" class. Scores 6: two other named bug classes (future roadmap-level drops of any named dispatch structure; "mocked steps" pattern in any pipeline) rather than 3+.

---

### Axis 3 — Implementation Complexity (weight 20%, inverted)

**Score: 6/10**

**Evidence**: The proposal estimates 12-17 hours and touches 4-6 files:
1. New file: `src/superclaude/cli/roadmap/fidelity_inventory.py` (~150-200 lines of pure Python regex)
2. Modified: `src/superclaude/cli/roadmap/gates.py` — 5 new semantic check functions + SPEC_FIDELITY_GATE extension (~80 lines)
3. Modified: `src/superclaude/cli/roadmap/prompts.py` — extended `build_spec_fidelity_prompt()` signature and body (~40 lines)
4. Modified: roadmap executor step runner — inventory pre-pass and frontmatter merge (~40 lines; location requires investigation)
5. New test file: `tests/roadmap/test_fidelity_inventory.py` (~150 lines, 10 test cases)

The core parsing functions are genuinely simple (pure regex, no external dependencies). The complication is the D-05 section-scope mitigation: correctly parsing Markdown heading structure and scoping sentinel detection to milestone sections adds a non-trivial parser (~50-100 additional lines). Without D-05 section-scope filtering, D-05 produces a high false positive rate. With it, implementation complexity increases.

**Score justification**: 4-6 file changes, 1-2 new abstractions (`fidelity_inventory.py` as a module, the Markdown section parser for D-05), under 500 lines total. Fits the 6-7 band ("4-6 file changes; 1-2 new abstractions; < 500 lines"). The D-05 section parser is the complexity that prevents a higher score.

---

### Axis 4 — False Positive Risk (weight 15%, inverted)

**Score: 6/10**

**Evidence for (low FP risk on D-03, D-04)**: D-03 fires only when an `UPPER_CASE_DICT` name from the spec is absent from the roadmap. False positive requires a spec to contain an uppercase dictionary name that the roadmap legitimately does not need to reference — this would be an architectural component name used only internally. The suffix keyword heuristic (`runner`, `dispatch`, `registry`) reduces this. D-04 fires only when `_run_*()` function names from spec pseudocode are absent from the roadmap — a genuinely narrow pattern. False positive would require a spec to define `_run_programmatic_step` in pseudocode and a roadmap to legitimately redesign the dispatch without mentioning the function names. This is possible but unusual.

**Evidence for (high FP risk on D-05)**: D-05 fires on "mocked steps" anywhere in the roadmap. As the Devil's Advocate documented, TDD workflows legitimately use this language in phase descriptions. Without the section-scope filter (which is not in the code spec), false positive rate is high for TDD-oriented roadmaps. The scoring framework (Axis 4) explicitly lists "Intentional stub implementations (TDD red-phase, mock boundaries in tests)" as a key FP scenario to consider. This proposal directly triggers that scenario.

**Evidence for (D-01, D-02 low FP)**: D-01 produces only vacuous passes for specs without FR-NNN identifiers — no false positives, just no value. D-02's module dependency check fires when a module named in spec arrows is absent from the roadmap — low FP risk since absent module names in roadmaps are genuinely suspicious.

**Score justification**: D-03 and D-04 have low FP risk (8-9 range individually). D-05 without section-scope filtering has high FP risk for TDD workflows (3-4 range). The composite risk is in the 6 range: "Occasional FP expected (5-10% of runs in normal operation); override available." The override path (section-scope filtering) is documented but not yet implemented. Score is 6, not 7, because the mitigation is prose rather than code in the current specification.

---

### Axis 5 — Integration Fit (weight 15%)

**Score: 8/10**

**Evidence**: The proposal directly extends the existing gate pattern. `GateCriteria` with `semantic_checks` is the standard pattern; adding new `SemanticCheck` entries to `SPEC_FIDELITY_GATE` follows the exact pattern used for `_high_severity_count_zero` and `_tasklist_ready_consistent`. The `ALL_GATES` registry in `roadmap/gates.py:760-774` means the extended gate definition is automatically picked up by the gate runner with no additional wiring. The new `required_frontmatter_fields` entries integrate with the existing frontmatter validation. The `fidelity_inventory.py` module is pure Python with no subprocess imports, consistent with `NFR-003` and `NFR-007`.

**Score reduction from 10**: The step runner modification requires locating the spec-fidelity step invocation in the roadmap executor — the proposal notes "the exact location depends on how the roadmap pipeline invokes Claude — this implementation step requires reading the roadmap pipeline executor to identify the call site." This is a minor but real investigation step. The frontmatter merge logic (injecting deterministic fields after LLM generation) adds a new post-processing step that does not exist in the current pipeline, representing a small integration surface.

**Score justification**: 8/10 — "Reuses existing patterns with minor extensions; integrates with pipeline executor cleanly." The minor extension is the pre-pass and post-merge in the executor step runner.

---

### Composite Score

```
Composite = (Catch_Rate × 0.25)
          + (Generalizability × 0.25)
          + (Complexity × 0.20)
          + (FP_Risk × 0.15)
          + (Integration_Fit × 0.15)

         = (7 × 0.25) + (6 × 0.25) + (6 × 0.20) + (6 × 0.15) + (8 × 0.15)
         = 1.75       + 1.50       + 1.20        + 0.90        + 1.20
         = 6.55
```

**Tier 2 — Implement in Phase 2** (range 6.0–7.4)

---

### Axis-by-Axis Scoring Table

| Axis | Weight | Score | Weighted | Key Evidence |
|------|--------|-------|----------|-------------|
| Catch Rate | 25% | 7/10 | 1.75 | D-03, D-04, D-05 independently block incident; D-01 vacuous pass; Link 1 only |
| Generalizability | 25% | 6/10 | 1.50 | Catches "spec dispatch table dropped" class; does not address code integration class |
| Implementation Complexity (inverted) | 20% | 6/10 | 1.20 | 4-6 files, <500 lines; D-05 section parser adds non-trivial complexity |
| False Positive Risk (inverted) | 15% | 6/10 | 0.90 | D-03/D-04 low FP; D-05 high FP for TDD workflows without section-scope filter |
| Integration Fit | 15% | 8/10 | 1.20 | Direct extension of existing GateCriteria/SemanticCheck pattern; minor executor wiring |
| **Composite** | 100% | **6.55** | **6.55** | Tier 2 — Implement in Phase 2 |

---

## Final Verdict and Adoption Profile

**Verdict**: Implement in Phase 2, with D-05 section-scope filtering as a pre-condition for adoption.

**Adoption profile**:

Proposal 02 provides genuine, deterministic protection against the specific class of failure that occurred in the cli-portify incident. D-03 (`PROGRAMMATIC_RUNNERS` absent from roadmap) and D-04 (`_run_programmatic_step` absent from roadmap) are the highest-value checks: they are narrow, low false-positive-risk, and directly target the structural elements that were dropped. D-05 is the highest-recall check but requires section-aware implementation to be safe in TDD workflows.

**Recommended adoption sequence**:

1. **Phase 2a** (immediate, ~6 hours): Implement D-03, D-04, and D-02. These checks have low false positive risk and directly catch the incident. Ship `fidelity_inventory.py` with these three functions, extend `SPEC_FIDELITY_GATE`, and add the cli-portify regression test. Verify against the actual incident artifacts.

2. **Phase 2b** (deferred, ~6-8 hours): Implement D-05 with full section-scope filtering (Markdown heading parser, milestone-proximity context filter). Do not ship D-05 without the section filter — the unfiltered version will produce false positives in TDD roadmaps and create developer friction that leads to gate suppression.

3. **Phase 3** (deferred, low priority): Implement D-01 as an opt-in enhancement for specs that adopt FR-NNN conventions. Do not treat it as a blocking check for specs without formal IDs.

**Prerequisite not to block Phase 2a**: The roadmap executor's spec-fidelity step invocation must be identified and the pre-pass/merge points confirmed accessible. This is a 30-minute investigation step.

**Relationship to other proposals**: Proposal 02 is not a substitute for Proposal 03 (Code Integration Gate) or Proposal 05 (Silent Success Detection). This proposal stops a bad roadmap from reaching the tasklist stage. Proposals 03 and 05 catch integration failures that survive a correct roadmap. All three are needed for full coverage of the cli-portify bug class.

---

## Top 2 Failure Conditions

### Failure Condition 1: D-05 False Positives Cause Gate Suppression

**Scenario**: D-05 is shipped without section-scope filtering. The next roadmap generated for a TDD-oriented pipeline includes standard language: "Phase 1 deliverable: executor skeleton with mocked step dispatch for red-green-refactor." D-05 fires. The developer, seeing a false positive, requests an override or files a request to disable the check. The gate is demoted from STRICT to LIGHT, or a `stub_sentinels_found: false` is manually injected. The check is effectively suppressed for future runs.

**Why this is the critical failure mode**: Gate suppression is worse than not having the gate. A suppressed gate communicates false safety — engineers believe the check is running when it is not. The cli-portify incident occurred partly because `SPEC_FIDELITY_GATE` was running in BLOCKING mode and gave no signal of failure. A gate that is nominally blocking but practically suppressed recreates this condition.

**Mitigation**: Implement D-05 section-scope filtering before shipping D-05 to STRICT tier enforcement. Accept the additional 3-4 hours of implementation cost.

### Failure Condition 2: Spec Authors Learn to Avoid Sentinel Terms Without Fixing the Underlying Omission

**Scenario**: A developer generating a roadmap is aware that "mocked steps" triggers D-05. The generated roadmap says instead: "Phase 2 implements a sequential executor with placeholder step implementations pending wiring." `_STUB_SENTINEL_PATTERN` does not match `placeholder step implementations` (the phrase is not in the regex). `PROGRAMMATIC_RUNNERS` and `_run_programmatic_step` are still absent — D-03 and D-04 fire. But in a future spec where the dispatch architecture is not described in pseudocode, D-03 and D-04 have no inventory to check against. The roadmap again drops the dispatch architecture, and D-05 passes because the sentinel language was avoided.

**Why this is a real risk**: The proposal's checks are string-pattern-based. String patterns can be evaded — not always intentionally, but through natural language variation. A developer learning to "speak past the gate" by using different vocabulary for the same conceptual reduction is a predictable adaptation in any organization where gates block progress.

**Mitigation**: D-03 and D-04 are harder to evade because they check for the presence of named artifacts from the spec, not the absence of sentinel words from the roadmap. Spec-side inventory checks (D-03, D-04) are structurally more robust than roadmap-side sentinel checks (D-05). Prioritize D-03/D-04 as the primary checks and treat D-05 as supplementary. Additionally, the LLM fidelity comparison augmented with the deterministic inventory (Section 2.1, the prompt injection) provides a second layer: even if D-05 is evaded, the LLM is explicitly told about D-03 and D-04 failures and instructed to classify them as HIGH severity. An LLM that sees a deterministic inventory failure is far less likely to misclassify it than one performing an unanchored comparison.

---

*Debate conducted under scoring-framework.md v1.2.1 rules. Scores are final for this debate round. Any revision to preliminary scores must be documented with justification per framework Section "Scoring Rubric Examples" guidance.*
