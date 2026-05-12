# Research Prompt: Anti-Instinct Gate Failure on Enriched Runs

## GOAL

Investigate why the anti-instinct gate passes cleanly for the spec-only baseline but fails for all TDD+PRD and Spec+PRD enriched runs, and determine what needs to change for enriched runs to pass.

## WHY

The anti-instinct gate is blocking the entire enriched pipeline from completing. Without it passing, we never get spec-fidelity, test-strategy, deviation-analysis, remediation, or certify artifacts. This means:
- We cannot do a full pipeline comparison (the quality comparison report had Dimensions 4-6 as N/A for enriched runs)
- We cannot generate tasklists via the full pipeline path (only via inference skill workaround)
- The enriched pipeline is objectively incomplete — it produces half the artifacts the baseline does

We incorrectly reported this as a "pre-existing issue" throughout multiple E2E test runs. It is NOT pre-existing — the baseline on master passes clean. This is caused by our TDD/PRD enrichment work producing richer roadmaps with more trackable obligations.

## EVIDENCE

### Baseline (PASSES — 0 failures)
**File:** `.dev/test-fixtures/results/test3-spec-baseline/anti-instinct-audit.md`
```
undischarged_obligations: 0
uncovered_contracts: 0
fingerprint_coverage: 0.72
total_obligations: 1
total_contracts: 6
fingerprint_total: 18
fingerprint_found: 13
```
- Input: 312-line spec → 380-line roadmap
- Result: ALL obligations discharged, ALL contracts covered. Pipeline completes fully through spec-fidelity, test-strategy, and tasklist generation.

### TDD+PRD (FAILS — undischarged obligations + uncovered contracts)
**File:** `.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md`
```
undischarged_obligations: 1
uncovered_contracts: 4
fingerprint_coverage: 0.73
total_obligations: 1
total_contracts: 8
fingerprint_total: 45
fingerprint_found: 33
```
- Input: 876-line TDD + 406-line PRD → 746-line roadmap
- Result: 1 undischarged obligation, 4 uncovered contracts. Pipeline HALTS. No spec-fidelity, test-strategy, or downstream artifacts.
- The gate has 3 semantic checks: `no_undischarged_obligations` (FAIL), `integration_contracts_covered` (FAIL), `fingerprint_coverage_check` (PASS at 0.73)

### Spec+PRD (FAILS — undischarged obligations + uncovered contracts)
**File:** `.dev/test-fixtures/results/test2-spec-prd-v2/anti-instinct-audit.md`
```
undischarged_obligations: 2
uncovered_contracts: 3
fingerprint_coverage: 0.72
```
- Input: 312-line spec + 406-line PRD → 558-line roadmap
- Result: 2 undischarged, 3 uncovered. Pipeline HALTS.

## WHAT TO INVESTIGATE

### 1. Anti-Instinct Gate Code
- `src/superclaude/cli/roadmap/gates.py` — Find `ANTI_INSTINCT_GATE` definition. What are the 3 semantic checks? What are the exact thresholds?
- `src/superclaude/cli/roadmap/fingerprint.py` — How does `extract_code_fingerprints()` work? What does `fingerprint_gate_passed()` check?
- `src/superclaude/cli/roadmap/executor.py` — How is the anti-instinct step built? What prompt generates the audit? Where is the audit output parsed against the gate?

### 2. Anti-Instinct Audit Content
- Read the FULL anti-instinct-audit.md from all 3 runs (not just frontmatter). What specific obligations are undischarged? What specific contracts are uncovered? What are the 12 missing fingerprints in the TDD+PRD run?
- Why does the 746-line enriched roadmap have 45 fingerprints (vs 18 for baseline) but 4 uncovered contracts (vs 0)?

### 3. The Prompt That Generates the Audit
- Find the prompt builder for the anti-instinct step (likely `build_anti_instinct_prompt` or similar in `prompts.py`)
- What does the prompt tell the LLM to check? Does it change based on input_type or tdd_file/prd_file?
- Does the enriched roadmap's richer content cause the LLM to identify more obligations that then aren't discharged?

### 4. Root Cause Hypotheses
- **H1: More content = more obligations.** The enriched roadmap mentions more components, APIs, and integrations. The anti-instinct auditor scans for "scaffolding obligations" (promises to implement something later) and finds more of them. But the roadmap doesn't always explicitly discharge them in subsequent phases.
- **H2: Gate thresholds are absolute, not proportional.** The gate requires undischarged_obligations == 0 and uncovered_contracts == 0. This is an absolute bar — ANY undischarged obligation fails it, regardless of how many are properly discharged. A richer roadmap has more chances to fail.
- **H3: The audit prompt doesn't account for enrichment.** The anti-instinct prompt may not understand that PRD-sourced content (personas, metrics) and TDD-sourced content (component details) are supplementary context, not hard obligations requiring discharge.

### 5. Fix Options to Evaluate
- **Option A: Adjust gate thresholds.** Allow undischarged_obligations <= N or uncovered_contracts <= M for enriched runs.
- **Option B: Modify the anti-instinct prompt.** Tell the auditor that PRD/TDD supplementary content is advisory context, not obligations requiring discharge.
- **Option C: Modify the roadmap generation prompts.** Ensure the merge step explicitly discharges all obligations identified in extraction.
- **Option D: Add a TDD/PRD-aware obligation classifier.** Distinguish between "implementation obligations" (must be discharged) and "context references" (informational, don't need discharge).
- Evaluate each option for: correctness (does it fix the real problem?), risk (does it mask real issues?), complexity (how much code changes?).

## OUTPUT

A research report answering:
1. Exactly what obligations and contracts are failing in each enriched run
2. Why the baseline passes (what's different about its roadmap content)
3. Root cause (which hypothesis is correct)
4. Recommended fix with specific code changes
5. Whether the fix requires rerunning the pipeline or can be applied to existing artifacts

## CONTEXT FILES

| File | Why |
|------|-----|
| `src/superclaude/cli/roadmap/gates.py` | ANTI_INSTINCT_GATE definition and semantic checks |
| `src/superclaude/cli/roadmap/fingerprint.py` | Fingerprint extraction and gate logic |
| `src/superclaude/cli/roadmap/executor.py` | How anti-instinct step is built and executed |
| `src/superclaude/cli/roadmap/prompts.py` | Anti-instinct prompt builder (if it exists) |
| `.dev/test-fixtures/results/test3-spec-baseline/anti-instinct-audit.md` | Baseline audit (PASSES) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/anti-instinct-audit.md` | TDD+PRD audit (FAILS) |
| `.dev/test-fixtures/results/test2-spec-prd-v2/anti-instinct-audit.md` | Spec+PRD audit (FAILS) |
| `.dev/test-fixtures/results/test3-spec-baseline/roadmap.md` | Baseline roadmap (380 lines — passes audit) |
| `.dev/test-fixtures/results/test1-tdd-prd-v2/roadmap.md` | TDD+PRD roadmap (746 lines — fails audit) |
