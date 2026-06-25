# Research-Gate Consolidated Findings

**Date:** 2026-06-21 | **Phase:** 3 (research gate) | **Tier:** Heavyweight
**Source reports (5):** analyst-research-gate-A (191L), analyst-research-gate-B (323L),
qa-research-gate-A (re-persisted), qa-research-gate-B (82L), qa-research-gate-depth (148L).

## Consolidated Verdict: FAIL → fix cycle 1

Per the gate rule "FAIL if ANY report contains ANY issue of any severity." All five reports returned an
underlying **PASS on substance** (zero CRITICAL, zero evidence-fabrication; ~50+ file:line citations
independently re-verified exact across the partitions). The FAIL is driven solely by 4 MINOR research-file
hygiene defects (C-1..C-4) that must be fixed before synthesis. The remaining items (C-5..C-7) are
TDD-synthesis carry-forwards, NOT research-file edits. C-8 is an operational artifact issue already resolved.

## Issues (deduplicated; originating lenses noted)

| ID | Severity | Affected file | Issue | Originating lens(es) | Required fix | Class |
|----|----------|---------------|-------|----------------------|--------------|-------|
| C-1 | MINOR | research/01-runtime-surface-algorithm.md:3 | Header `Status: In Progress` contradicts footer `Status: Complete` (L281) | analyst-A, qa-A | Change L3 to `**Status: Complete**` | research-fix |
| C-2 | MINOR | research/03-consumer-surfaces.md (header L1-9) | No top-level `Status:` field anywhere | qa-A, analyst-A | Add `**Status:** Complete` to the header block | research-fix |
| C-3 | MINOR | research/01-runtime-surface-algorithm.md §6 | FR-RSR.7 forbidden-keys cited as "SKILL:L491"; that content is the §9.1 MANDATORY EMISSION comment (SKILL.md:721-730) | qa-A | Re-anchor citation to SKILL.md §9.1 L721-730 | research-fix |
| C-4 | MINOR | research/04-eval-path-integration.md | States grader.py is "519 lines"; actual `wc -l` = 518 | qa-B, analyst-B | Correct to 518 | research-fix |
| C-5 | MINOR (advisory) | (TDD §15) | file 04 honestly flags the `evals.json`→`eval_metadata.json` materializer as unverified (Option B dependency) | analyst-B, qa-B | No research edit — carry to TDD §15 as a noted dependency | tdd-note |
| C-6 | MINOR (advisory) | (TDD §15) | grader.py:448-449 `target`-prefix routing fragility: a future non-`target` FR-RSR assertion would be silently dropped | analyst-B, qa-B | No research edit — carry to TDD §15: oracle assertions MUST carry a `target` key | tdd-note |
| C-7 | IMPORTANT (defer) | (TDD §6.4/§21/§22) | DG-1: OQ-DRS.2 invocation-site decision left as weighable options without a ratified recommendation; research correctly shows the spec's named `commands.py` writer is the wrong chokepoint (`_audit_once` is the strongest CLI site, but it misses bare `claude -p`) | depth | No research edit — synth-03/synth-09 already instructed to present the decision WITH a recommendation in §6.4/§21/§22 | tdd-decision |
| C-8 | OPERATIONAL (resolved) | qa/qa-research-gate-A-report.md | rf-qa Partition-A report did not persist on first write | orchestrator | Re-persisted from the agent's verbatim return | resolved |

## Fix scope for Step 3.8
Apply C-1, C-2, C-3, C-4 to the research files (4 trivial hygiene edits). C-5/C-6/C-7 are recorded here and
flow into the synthesis phase (already covered by the synth-02/03/07/09 item instructions); they require NO
research-file change. C-8 already resolved.

## Substance note
No content gap blocks synthesis. The corpus is Heavyweight-deep and evidence-grounded; the gate FAIL is a
hygiene formality, not a coverage deficiency.
