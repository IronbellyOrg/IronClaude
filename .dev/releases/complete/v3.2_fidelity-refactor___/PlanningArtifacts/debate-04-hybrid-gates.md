# Adversarial Debate: A3 -- Deviation Count Reconciliation Gate

**Date**: 2026-03-17
**Source**: brainstorm-04-hybrid-gates.md, Solution A3
**Scoring Framework**: scoring-framework.md (5-dimension weighted formula)
**Forensic Reference**: docs/generated/cli-portify-executor-noop-forensic-report.md

---

## Proposal Summary

Deterministically count `DEV-NNN` entries in the fidelity report body, extract each entry's declared severity (HIGH/MEDIUM/LOW), and compare counts against YAML frontmatter values (`high_severity_count`, `medium_severity_count`, `low_severity_count`). Fail the gate if any count mismatches. Also verify `total_deviations == sum of severity counts`.

**Implementation**: New `_deviation_counts_reconciled` semantic check in `src/superclaude/cli/roadmap/gates.py`, added to `SPEC_FIDELITY_GATE.semantic_checks`.

---

## Advocate's Opening Argument

### 1. Bug Scenarios Caught

The cli-portify forensic report (Section 5, "Fidelity Chain Failure Analysis") identifies the central failure mode: the LLM fidelity reviewer either missed or under-classified the spec-to-roadmap deviation where the three-way dispatch (`_run_programmatic_step`, `_run_claude_step`, `_run_convergence_step`) was replaced by "sequential execution with mocked steps." The current `SPEC_FIDELITY_GATE` enforcement is limited to checking `high_severity_count == 0` in the frontmatter -- it trusts the LLM's self-reported number completely.

The Deviation Count Reconciliation Gate catches a specific and dangerous failure mode: **LLM arithmetic errors and self-contradictions between report body and frontmatter**. Consider these concrete scenarios:

**Scenario 1 -- Frontmatter Undercount**: The LLM writes a fidelity report that lists `DEV-001: Missing three-way dispatch (Severity: HIGH)` and `DEV-002: PROGRAMMATIC_RUNNERS absent (Severity: HIGH)` in the body, but writes `high_severity_count: 0` in the frontmatter because it "summarized" or lost track during generation. Today, the gate passes because it only reads the frontmatter. With reconciliation, the deterministic count of 2 HIGH entries in the body mismatches frontmatter's 0, and the gate blocks.

**Scenario 2 -- Truncation Detection**: The LLM runs out of context window during a lengthy fidelity comparison. It lists `DEV-001` through `DEV-005` in the body but the frontmatter claims `total_deviations: 8`. The reconciliation gate catches this: body count (5) does not equal declared total (8). This prevents a partially-generated report from being treated as complete.

**Scenario 3 -- Severity Miscounting**: The LLM lists 3 deviations as HIGH in the body text but reports `high_severity_count: 1` in the frontmatter. This is a real LLM failure pattern -- when generating structured YAML after a long free-text section, models frequently miscalculate counts from the preceding content.

The forensic report (Section 5, "What Neither Gate Does") explicitly states: "No programmatic parsing of requirement IDs from source document" and "No enumeration completeness check." While this proposal does not parse requirement IDs from the source spec, it does add enumeration completeness checking *within the fidelity report itself* -- ensuring the LLM's claims are internally consistent.

### 2. Integration Path

This is the cleanest integration path of any proposal in the brainstorm. The existing infrastructure at `src/superclaude/cli/roadmap/gates.py` already provides:

- `_parse_frontmatter(content: str) -> dict[str, str] | None` -- reusable frontmatter parser (line 129)
- `SemanticCheck(name, check_fn, failure_message)` data class for registering checks
- `SPEC_FIDELITY_GATE` with a `semantic_checks` list that already contains `_high_severity_count_zero` and `_tasklist_ready_consistent`
- All semantic checks follow the `(content: str) -> bool` signature

The new function `_deviation_counts_reconciled(content: str) -> bool` needs:
1. Call `_parse_frontmatter(content)` to get declared counts
2. Regex-scan the body for `DEV-\d{3}` entries
3. For each match, extract the subsequent `**Severity**: HIGH|MEDIUM|LOW` line
4. Compare body counts to frontmatter counts
5. Return `False` on any mismatch

Estimated implementation: 30-45 lines of production code. One function. One file modified (`gates.py`). One new entry in `SPEC_FIDELITY_GATE.semantic_checks`. Zero new dependencies. Zero pipeline changes. Zero prompt modifications.

The existing `_parse_frontmatter` function already handles YAML extraction. The existing `DEVIATION_ANALYSIS_GATE` (lines 712-758) already demonstrates the pattern of regex-based ID validation (`_routing_ids_valid` checks `DEV-\d+` patterns), confirming that DEV-NNN regex parsing is an established pattern in the codebase.

### 3. Composability with Other Top Proposals

A3 directly strengthens proposals A1 (Requirement ID Enumeration Cross-Check) and A4 (Severity Classification Spot-Check):

- **With A1**: A1 catches missing requirement IDs; A3 ensures that when the LLM *does* identify deviations, its count reporting is honest. Together they form a two-layer defense: A1 catches omissions the LLM misses entirely, A3 catches omissions the LLM notices but miscounts in the frontmatter.

- **With A4**: A4 applies keyword heuristics to flag severity misclassifications. A3 ensures the severity counts match what is in the body. Together: A4 checks that individual deviation severities make sense, A3 checks that the aggregate counts are arithmetically correct. They operate at different granularities and catch different error modes.

- **With B1 (Deliverable ID Traceability)**: A3 is purely spec-to-roadmap scoped, so it does not overlap with B1's roadmap-to-tasklist scope. They are fully orthogonal and can run independently.

- **With B5 (Bidirectional Consistency Audit)**: A3's lightweight body-vs-frontmatter check provides a fast-fail layer that catches obvious LLM inconsistencies before the heavier B5 analysis runs. This saves pipeline time when the fidelity report is clearly malformed.

The proposal also creates reusable infrastructure: the body-parsing logic (extracting DEV-NNN entries with their severity) can be factored into a helper function that A4's keyword heuristic check also consumes, avoiding duplicate parsing.

---

## Skeptic's Opening Argument

### 1. Failure Modes Where This Gate Would NOT Catch Bugs

The central claim requires scrutiny. Let me be precise about what A3 does and does not do.

**A3 does not catch the cli-portify bug.** The forensic report (Section 9, "Primary: Spec-to-Roadmap Fidelity Failure") states: "The SPEC_FIDELITY_GATE (LLM-dependent semantic comparison) did not catch or did not escalate this as a HIGH severity deviation." There are two possible failure modes here:

1. **The LLM missed the deviation entirely** -- it was not listed as any DEV-NNN entry in the report body. In this case, the frontmatter correctly says `high_severity_count: 0` and the body contains zero HIGH entries. A3 sees no mismatch. The gate passes. The bug propagates.

2. **The LLM listed the deviation but misclassified it as MEDIUM** -- `DEV-003: Executor design simplified (Severity: MEDIUM)`. The frontmatter says `high_severity_count: 0, medium_severity_count: 3`. The body contains 0 HIGH and 3 MEDIUM entries. A3 sees no mismatch. The gate passes. The bug propagates.

A3 only catches failure mode 3: **the LLM lists HIGH deviations in the body but miscounts in the frontmatter**. This is a real but narrow failure mode. The forensic report does not present evidence that this specific failure mode occurred in the cli-portify case. The more likely failure was mode 1 (complete omission) or mode 2 (misclassification), neither of which A3 addresses.

**The "defined but not wired" pattern class** (forensic report Section 7) is entirely outside A3's detection capability. A3 operates on the fidelity report's internal consistency, not on whether the fidelity report correctly identifies deviations in the first place.

**Silent no-op fallbacks** (forensic report Section 1) are code-level issues at Link 3 (tasklist-to-code). A3 operates at Link 1 (spec-to-roadmap). Even a perfect A3 implementation has zero bearing on no-op detection.

### 2. False Positive Scenarios

While A3 is deterministic (good for false positive avoidance), there are realistic failure scenarios:

**Format Variation**: The brainstorm acknowledges this -- if the LLM writes `DEV-01` instead of `DEV-001`, or uses `Severity: High` instead of `**Severity**: HIGH`, or formats entries with different markdown patterns, the regex silently misses entries. This creates a *false negative* (undercounted body entries) that could cascade into a false positive if body_count < frontmatter_count.

**Multi-line Severity Declarations**: If the LLM places the severity on the same line as the DEV-NNN identifier rather than on a separate `**Severity**:` line, or embeds it in a table, the regex extraction may fail. The frontmatter will show correct counts while the body parser under-extracts, producing a spurious mismatch.

**Repeated DEV-NNN References**: The report body might reference `DEV-001` in a summary section, a detail section, and a recommendations section. Naive regex counting would triple-count entries. The implementation must deduplicate by DEV-NNN identifier, not count raw matches -- adding complexity beyond the "30-45 lines" estimate.

**Fidelity Reports Without DEV-NNN Format**: The current `build_spec_fidelity_prompt()` in `prompts.py` may not require the `DEV-NNN` format for individual deviations. The prompt requires YAML frontmatter with severity counts, but the body format for individual deviations is at the LLM's discretion. If the LLM lists deviations without `DEV-NNN` identifiers, A3 finds zero body entries and either: (a) incorrectly fails the gate when frontmatter reports non-zero counts, or (b) requires a prompt change to mandate DEV-NNN format -- contradicting the "no prompt changes needed" claim.

### 3. Maintenance Burden Over 5+ Releases

A3's maintenance burden is genuinely low -- I concede this point partially. However:

- **Format drift**: As the fidelity report prompt evolves (and it will -- A2 adds a Coverage Matrix, A4 changes severity classification expectations, A5 changes the entire report structure), the DEV-NNN body format and severity labeling conventions may shift. Each format change requires updating the regex patterns in A3.

- **Fidelity report used at two links**: `SPEC_FIDELITY_GATE` and `TASKLIST_FIDELITY_GATE` both produce fidelity reports. A3 would need to be duplicated or generalized for both gates if the body format differs between them.

- **Testing surface**: While the function is pure and testable, it needs test cases for every format variation the LLM might produce. This test suite grows with each new format observation. The alternative -- making the regex strict and accepting occasional false positives -- trades maintenance burden for user friction.

### 4. Simpler Alternatives

**Alternative 1: Strengthen the existing `_high_severity_count_zero` check.** Instead of reconciling body counts against frontmatter, simply require the LLM to output a structured "Deviation List" in a code block (JSON or YAML) that is machine-parseable. Parse that block directly instead of regex-scanning markdown prose. This is more robust and achieves the same body-vs-frontmatter consistency with less regex fragility.

**Alternative 2: Require `total_deviations` to be non-negative and consistent with severity counts.** A simpler arithmetic check -- `total_deviations == high + medium + low` -- using only frontmatter fields. This catches the LLM miscounting across severity buckets without parsing the body at all. Fewer moving parts, same arithmetic-error detection for the frontmatter-only case.

**Alternative 3: Skip A3 and invest in A1 (Requirement ID Enumeration Cross-Check) instead.** A1 catches the actual cli-portify failure mode (missing requirements) while A3 only catches the secondary failure mode (miscounted deviations). For the same implementation effort, A1 provides strictly more bug-catching value for the specific bug class identified in the forensic report.

---

## Advocate's Rebuttal

The Skeptic raises valid points about A3 not catching the cli-portify bug when the LLM completely misses a deviation (mode 1) or misclassifies it (mode 2). I accept this limitation. A3 is not positioned as a standalone bug catcher -- it is positioned as a **self-consistency layer** that makes the entire LLM-dependent gate system more trustworthy.

However, the Skeptic underestimates two things:

1. **LLM arithmetic errors are common and dangerous.** LLMs generating long structured reports routinely miscalculate summary statistics. The cli-portify forensic report may not have documented this specific failure mode, but the gate infrastructure is designed to handle *future* releases, not just retroactively catch one bug. A3 prevents a class of failures (inconsistent self-reporting) that will recur across every future fidelity check.

2. **A3 is a force multiplier for A4.** The Skeptic suggests investing in A1 instead. But A1 and A3 are not substitutes -- they are complements. A1 catches missing requirement IDs. A4 catches severity misclassifications. A3 ensures the aggregate counts match the body. Together, they form a three-layer defense where each layer catches what the others miss. Removing A3 leaves a gap where the LLM lists HIGH deviations in prose but reports zeros in frontmatter, and the gate happily passes.

On the format concern: I concede that the prompt may need to be tightened to require `DEV-NNN` format. This is a one-line addition to the prompt template, not a pipeline change. The claim "no prompt changes needed" was too strong -- "minimal prompt change" is more accurate.

On the deduplication concern: extracting unique `DEV-NNN` identifiers and counting distinct IDs per severity is straightforward. This adds perhaps 5 lines to the implementation. The estimate adjusts from 30-45 to 35-55 lines -- still firmly in the "trivial" category.

---

## Skeptic's Rebuttal

I appreciate the Advocate's honesty about the prompt change requirement. That admission matters because it moves A3 from "pure drop-in function" to "function plus prompt modification" -- still simple, but the integration surface is larger than initially claimed.

My core objection stands: **A3 catches a failure mode for which we have no evidence it occurred in the cli-portify incident.** The forensic report's primary finding (Section 9) is that the LLM either missed the deviation entirely or under-classified it. A3 addresses neither of these. Building infrastructure for an undemonstrated failure mode, while real failure modes (mode 1 and mode 2) remain unaddressed by this specific proposal, is a misallocation of priority.

That said, I acknowledge:
- A3's implementation cost is genuinely minimal
- A3 does not conflict with any other proposal
- A3 provides a reusable DEV-NNN parsing utility that A4 can consume
- LLM arithmetic errors are a real phenomenon even if not documented in this specific incident

My revised position: A3 is a **nice-to-have** rather than a **must-have**. It should be implemented, but only after A1 and A4, which address the demonstrated failure modes.

---

## Scoring

### Dimension 1: Likelihood to Succeed (Weight: 0.35)

**Question**: Would this gate catch the cli-portify no-op bug?

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 5 | A3 catches body-vs-frontmatter inconsistency (failure mode 3). It would catch the cli-portify bug only if the LLM listed the deviation in prose but miscounted in frontmatter -- plausible but unconfirmed. It catches a real failure class (LLM arithmetic errors) but has known blind spots for modes 1 and 2. |
| Skeptic | 3 | A3 does not catch the specific cli-portify failure (mode 1: complete omission or mode 2: misclassification). It catches a secondary failure mode (mode 3: arithmetic error) for which there is no forensic evidence. The "defined but not wired" pattern is entirely outside scope. |

**Delta**: 2 (at threshold, no tiebreaker required)
**Final Score**: **4.0**

Evidence basis:
- The specific cli-portify failure (spec's three-way dispatch dropped at Spec-to-Roadmap) would only be caught if the LLM noticed but miscounted -- not the documented failure mode
- The "defined but not wired" pattern class is outside A3's scope (A3 operates on fidelity report content, not code analysis)
- Silent no-op fallbacks are Link 3 issues; A3 is Link 1 only
- Assumptions required: LLM must use DEV-NNN format, LLM must list the deviation in the body but miscount in frontmatter

### Dimension 2: Implementation Complexity (Weight: 0.25)

**Question**: How much effort to implement? (Inverted: 10 = trivial)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 9 | 35-55 lines of code. One function in one existing file. Reuses `_parse_frontmatter`. Follows established `SemanticCheck` pattern. One line added to `SPEC_FIDELITY_GATE.semantic_checks`. Minimal prompt tightening. No new dependencies. |
| Skeptic | 8 | Mostly agree, but: deduplication logic, format-edge-case handling, and the prompt change push it slightly past the "trivial" threshold. Testing needs to cover format variations. Still < 100 lines total including tests. |

**Delta**: 1 (within threshold)
**Final Score**: **8.5**

Evidence basis:
- Estimated 35-55 lines of production code
- 1 file modified (`gates.py`), 1 minor prompt addition
- No new dependencies or infrastructure
- Testing: ~5-8 test cases for format variations, reusing existing test fixtures
- Existing `_routing_ids_valid` in `DEVIATION_ANALYSIS_GATE` demonstrates the exact regex pattern

### Dimension 3: False Positive Risk (Weight: 0.15)

**Question**: Would this gate block legitimate pipelines? (Inverted: 10 = no risk)

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 8 | Deterministic check with clear semantics. Only fires on genuine body-vs-frontmatter mismatch. Format standardization via prompt minimizes variation. Error messages can pinpoint exact mismatched counts. |
| Skeptic | 6 | Format variation is a real concern. DEV-NNN format not currently mandated. Repeated references cause double-counting without deduplication. Multi-line severity declarations may confuse extraction. Until the prompt is tightened, false positives are likely. |

**Delta**: 2 (at threshold, no tiebreaker required)
**Final Score**: **7.0**

Evidence basis:
- Deterministic check (good): no probabilistic thresholds
- Format dependency (risk): requires DEV-NNN and `**Severity**: X` patterns
- Deduplication needed: repeated references in summary/detail sections
- Override mechanism: not explicitly defined, but STRICT tier allows pipeline halt with clear error
- After prompt tightening: false positives become rare (format is controlled)

### Dimension 4: Maintainability (Weight: 0.15)

**Question**: Will this gate stay correct as the pipeline evolves?

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 8 | Auto-derives checks from document content. No manual configuration per release. Only breaks if DEV-NNN or severity format changes, which is a schema-level change. Can be meta-tested (generate a report, run the check, verify). |
| Skeptic | 6 | Format drift as prompts evolve (A2 Coverage Matrix, A4 keyword changes, A5 dual-pass). Needs duplication for TASKLIST_FIDELITY_GATE. Regex patterns require updating when report format conventions change. |

**Delta**: 2 (at threshold, no tiebreaker required)
**Final Score**: **7.0**

Evidence basis:
- Auto-discovers what to check (parses content, no manual config): good
- Sensitive to DEV-NNN format and severity label format: moderate risk
- Can be verified automatically (generate test report, run check): good
- Needs update when prompts evolve: moderate maintenance, but prompt changes are infrequent

### Dimension 5: Composability (Weight: 0.10)

**Question**: Does this gate strengthen other gates?

| Debater | Score | Rationale |
|---------|-------|-----------|
| Advocate | 8 | Directly strengthens A4 (shared DEV-NNN parsing utility). Complements A1 (different failure mode coverage). Provides fast-fail layer before heavier B5 analysis. Fits existing `SemanticCheck` pattern perfectly. |
| Skeptic | 7 | Agrees on A4 synergy and SemanticCheck fit. But A3 is independent of A1 at runtime (they do not share outputs). The "fast-fail" benefit before B5 is speculative -- B5 operates at a different pipeline link (roadmap-to-tasklist). |

**Delta**: 1 (within threshold)
**Final Score**: **7.5**

Evidence basis:
- Reinforces A4: shared DEV-NNN parsing utility avoids duplicate work
- Complements A1: covers different failure mode (arithmetic vs omission)
- Fits `GateCriteria`/`SemanticCheck` pattern: no architectural changes
- Outputs (parsed DEV-NNN entries with severity) are reusable by A4

---

## Final Weighted Score

```
Score = (Success * 0.35) + (Complexity * 0.25) + (FalsePositive * 0.15) + (Maintainability * 0.15) + (Composability * 0.10)
Score = (4.0 * 0.35) + (8.5 * 0.25) + (7.0 * 0.15) + (7.0 * 0.15) + (7.5 * 0.10)
Score = 1.40 + 2.125 + 1.05 + 1.05 + 0.75
Score = 6.375
```

**Final Weighted Score: 6.4** (rounded to one decimal)

**Interpretation**: Good candidate -- implement after high-priority items (6.0-7.9 range).

---

## Verdict

A3 is a well-designed, minimal-cost gate that catches a real (LLM arithmetic error) but secondary failure mode. Its greatest strength is implementation simplicity: 35-55 lines, one file, existing patterns. Its greatest weakness is that it does not catch the primary cli-portify failure modes (complete deviation omission or severity misclassification).

**Recommendation**: Implement A3, but prioritize A1 (Requirement ID Enumeration Cross-Check) and A4 (Severity Classification Spot-Check) first. A3 provides incremental value as a self-consistency layer and creates shared infrastructure (DEV-NNN parsing) that A4 directly benefits from. Implementation order: A1 > A4 > A3.
