# Brainstorm: Integrating rf-qa into sc:troubleshoot

**Date:** 2026-04-03
**Branch:** feat/v3.65-prd-tdd-Refactor
**Status:** Brainstorm / Requirements Discovery
**Method:** /sc:brainstorm systematic exploration

---

## Codebase Context

**Relevant Existing Components:**
- `/.claude/agents/rf-qa.md` -- Rigorflow QA Agent with zero-trust verification, adversarial stance, fix-cycle support, confidence gate protocol, and parallel partitioning
- `/.claude/commands/sc/troubleshoot.md` -- Issue diagnosis and resolution command with 5-phase behavioral flow (Analyze, Investigate, Debug, Propose, Resolve)
- `/.claude/agents/rf-qa-qualitative.md` -- Qualitative QA sibling that verifies content sense-making (complementary to structural rf-qa)

**Key Architectural Observations:**
- sc:troubleshoot is currently a "basic" complexity command with no MCP servers or personas configured
- sc:troubleshoot has no agent spawning, no QA gates, no verification loops -- it is a single-pass skill
- rf-qa already supports being spawned as a subagent with configurable QA phases and fix authorization
- rf-qa's fix-cycle phase (max 3 rounds) maps naturally to iterative troubleshooting
- rf-qa's confidence gate protocol (computed, not self-assessed) directly addresses the problem of wasted tokens on low-confidence hypotheses

**Integration Points:**
- sc:troubleshoot's "Propose" phase (Step 4) is where hypothesis validation would slot in
- sc:troubleshoot's "Resolve" phase (Step 5) is where post-fix verification would slot in
- rf-qa's `fix_authorization` toggle maps to sc:troubleshoot's `--fix` flag semantics

**Constraints:**
- sc:troubleshoot must remain diagnosis-first by default (no-fix unless `--fix` flag)
- rf-qa spawning adds token overhead -- must be offset by reduced wasted-fix tokens
- rf-qa is designed for file-based artifact verification; troubleshoot operates on live code state

---

## Problem Statement

sc:troubleshoot currently operates as a single-pass, single-agent flow. It generates hypotheses about root causes and proposes fixes without independent verification. This leads to two token-waste failure modes:

1. **False hypothesis pursuit** -- The troubleshooter commits tokens to investigating a hypothesis that a quick evidence check would have eliminated early.
2. **Incorrect fix application** -- With `--fix`, a fix is applied and then found to be wrong, requiring rollback and re-diagnosis. Each failed fix-apply cycle burns 500-2000 tokens.

rf-qa's zero-trust verification, adversarial stance, and structured evidence requirements can address both failure modes by acting as a verification checkpoint within the troubleshooting pipeline.

---

## Proposal 1: Hypothesis Validation Gate

### Summary

Insert rf-qa as a lightweight validation gate between sc:troubleshoot's "Investigate" (Phase 2) and "Propose" (Phase 4) phases. Before the troubleshooter commits to a root cause diagnosis and solution proposal, rf-qa independently verifies the evidence supporting each hypothesis.

### Rationale

The highest token waste in troubleshooting occurs when the agent pursues an incorrect root cause hypothesis deep into the pipeline. By the time it reaches "Propose" or "Resolve," it has consumed 1000-3000 tokens on a dead end. A lightweight rf-qa gate after hypothesis generation can eliminate unsupported hypotheses early, before the expensive proposal and resolution phases.

This maps to rf-qa's existing "research gate" pattern: verify evidence completeness and accuracy before proceeding to the next phase. The key adaptation is that instead of verifying research files, rf-qa verifies troubleshooting hypotheses against actual code/log evidence.

### Implementation Approach

**Phase Integration Point:** Between existing Phases 2 (Investigate) and 4 (Propose).

**New Phase 3: Hypothesis Validation Gate**

The troubleshooter produces a structured hypothesis document after Phase 2:

```markdown
## Hypothesis Report
| # | Hypothesis | Evidence For | Evidence Against | Confidence |
|---|-----------|-------------|-----------------|------------|
| 1 | [root cause theory] | [file:line, log entry] | [contradicting evidence] | [high/med/low] |
```

rf-qa is spawned as a subagent with a new QA phase: `hypothesis-gate`. Its checklist:

1. **Evidence existence** -- For each "Evidence For" citation, verify the file/line/log actually exists and says what the hypothesis claims (Read/Grep).
2. **Evidence relevance** -- Does the cited evidence actually support the hypothesis, or is it tangential?
3. **Contradiction check** -- Are there obvious contradictions the troubleshooter missed? (Grep for related error patterns, check git blame for recent changes to cited files.)
4. **Completeness** -- Did the troubleshooter examine all relevant files? (Glob for related files not mentioned.)
5. **Confidence recomputation** -- Apply rf-qa's confidence gate protocol: computed confidence from verified evidence, not self-assessed.

**Verdict:** Each hypothesis gets PASS (evidence supports it), FAIL (evidence does not support it), or INSUFFICIENT (need more investigation). Only PASS hypotheses proceed to Phase 4.

**Token Budget:**

- Hypothesis validation overhead: ~300-500 tokens per hypothesis (2-4 tool calls each)
- Expected savings: Eliminates ~60% of false hypothesis pursuit, saving 800-2000 tokens per eliminated dead end
- Net ROI: Positive when >= 1 in 3 troubleshooting sessions has a false hypothesis (conservative estimate based on general agent error rates)

**Command Changes to `troubleshoot.md`:**

- Add `--validate` flag (default: on for `--type bug`, off for others)
- Add `--no-validate` to skip the gate for simple issues
- Upgrade complexity from `basic` to `standard`
- Add rf-qa to the tool/agent coordination section

### Expected Benefits

- **Token reduction:** 30-50% reduction in wasted tokens from false hypothesis pursuit
- **Accuracy improvement:** Only evidence-backed hypotheses reach the proposal phase
- **Audit trail:** Hypothesis validation reports provide documentation of what was checked and why
- **Composability:** The hypothesis-gate QA phase can be reused by other diagnostic skills (sc:analyze, sc:test)

### Trade-offs

- **Latency:** Adds one subagent spawn cycle (~5-10 seconds wall time) to the troubleshooting flow
- **Overhead on correct hypotheses:** When the troubleshooter's first hypothesis is correct, the validation gate is pure overhead (~300-500 tokens). This is the "insurance premium" cost.
- **Adaptation effort:** rf-qa's existing QA phases are designed for file-based artifacts (research files, synthesis files, reports). A new `hypothesis-gate` phase must be defined that operates on live code evidence rather than structured documents.
- **Complexity increase:** sc:troubleshoot moves from a simple single-pass command to a multi-agent pipeline. This increases the surface area for failures in the troubleshooting tool itself.

---

## Proposal 2: Post-Fix Verification Loop

### Summary

When sc:troubleshoot runs with `--fix`, spawn rf-qa after each fix application to independently verify that the fix actually resolves the issue and does not introduce regressions. This replaces the current single-pass "verify resolution effectiveness" step with rf-qa's structured, adversarial verification and fix-cycle protocol.

### Rationale

The second major token-waste failure mode is applying a fix that does not actually work. The current sc:troubleshoot flow applies a fix, runs a basic verification, and reports success. But the verification is performed by the same agent that proposed the fix -- creating a confirmation bias risk. The agent that wrote the fix is predisposed to believe it works.

rf-qa's adversarial stance ("assume everything is wrong until you personally verify it") and zero-trust principles directly counter this bias. Its fix-cycle protocol (max 3 rounds, each round must have fewer issues) provides structured iteration with a hard stop to prevent infinite fix loops.

### Implementation Approach

**Phase Integration Point:** Wraps existing Phase 5 (Resolve) when `--fix` flag is present.

**Modified Phase 5: Fix-Verify Loop**

1. Troubleshooter applies the fix (existing behavior).
2. Troubleshooter writes a structured fix manifest:

```markdown
## Fix Manifest
- **Files modified:** [list with before/after descriptions]
- **Expected behavior change:** [what should be different now]
- **Verification commands:** [test commands, curl calls, build commands]
- **Regression risk areas:** [files/features that might break]
```

3. rf-qa is spawned with phase: `fix-verification` and `fix_authorization: false` (report only). Its checklist:

   1. **Fix applied correctly** -- Read each modified file, verify the change matches the fix manifest description.
   2. **Tests pass** -- Run the verification commands from the manifest. Capture output.
   3. **No regressions** -- Run broader test suite if available (`uv run pytest` or equivalent). Check that no previously-passing tests now fail.
   4. **Root cause addressed** -- Verify the original error condition (from Phase 1's issue description) is no longer reproducible.
   5. **No side effects** -- Grep for the modified code patterns elsewhere in the codebase. If the same pattern exists in other files, flag potential inconsistency.
   6. **Code quality** -- The fix does not introduce obvious code smells (dead code, duplicated logic, missing error handling).

**Verdict:** PASS (fix verified, proceed) or FAIL (fix issues found, enter fix-cycle).

**On FAIL:** The troubleshooter receives rf-qa's specific findings and applies corrections. rf-qa re-verifies. Maximum 3 fix cycles (inherited from rf-qa protocol). After 3 failures, halt and present all findings to the user.

**Token Budget:**

- Post-fix verification overhead: ~400-800 tokens (5-8 tool calls for file reads, test runs, grep checks)
- Expected savings: Eliminates the "apply wrong fix, discover later, redo everything" pattern which costs 1500-4000 tokens per occurrence
- Net ROI: Positive when >= 1 in 4 fix applications has an issue (common for non-trivial bugs)

**Command Changes to `troubleshoot.md`:**

- When `--fix` is present, automatically enable post-fix rf-qa verification
- Add `--fix --no-verify` to skip rf-qa verification (escape hatch for trivial fixes)
- Add rf-qa fix-cycle semantics (max 3 rounds) to the resolve phase
- Document fix manifest format in the command spec

### Expected Benefits

- **Token reduction:** 40-60% reduction in wasted tokens from failed fix-apply-redo cycles
- **Confidence in fixes:** Independent adversarial verification means higher confidence that a reported "fix" actually works
- **Regression prevention:** Broader test suite execution catches side effects the troubleshooter might miss
- **Bounded iteration:** rf-qa's max-3 fix cycles prevents infinite fix loops that consume unbounded tokens
- **Documentation:** Fix verification reports serve as evidence that the fix was properly validated

### Trade-offs

- **Only applies with `--fix` flag:** Default diagnosis-only mode gets no benefit from this proposal (Proposal 1 covers that case)
- **Test suite dependency:** Regression checking is most effective when the project has a test suite. For projects without tests, checklist items 2 and 3 degrade to heuristic checks.
- **Latency:** Adds one subagent spawn per fix cycle. For a 3-cycle fix, this is 3 additional spawns (~15-30 seconds wall time total).
- **Fix manifest overhead:** The troubleshooter must produce a structured manifest before rf-qa can verify. This is ~100-200 tokens of formatting work that does not exist in the current flow.
- **rf-qa phase adaptation:** Like Proposal 1, this requires defining a new rf-qa QA phase (`fix-verification`) that is tailored to code fixes rather than document artifacts.

---

## Comparison Matrix

| Dimension | Proposal 1: Hypothesis Gate | Proposal 2: Post-Fix Verification |
|-----------|---------------------------|----------------------------------|
| **When it fires** | Every troubleshoot session (Phase 2-3 boundary) | Only with `--fix` flag (Phase 5) |
| **Token overhead** | 300-500 per session | 400-800 per fix cycle |
| **Token savings** | 800-2000 per eliminated false hypothesis | 1500-4000 per avoided bad fix |
| **Net ROI threshold** | Positive at 1-in-3 false hypothesis rate | Positive at 1-in-4 bad fix rate |
| **Complexity** | Medium (new QA phase, hypothesis format) | Medium (new QA phase, fix manifest format) |
| **Latency impact** | +5-10s per session | +5-10s per fix cycle |
| **Dependency** | None (works with diagnosis-only mode) | Requires `--fix` flag; benefits scale with test coverage |
| **rf-qa adaptation** | New `hypothesis-gate` phase | New `fix-verification` phase |

## Recommendation

**Implement both proposals as complementary layers.** They address different failure modes at different pipeline stages and do not conflict. Proposal 1 prevents wasted investigation tokens (upstream). Proposal 2 prevents wasted fix-apply tokens (downstream). Together they create a verified troubleshooting pipeline with rf-qa acting as an independent quality checkpoint at both critical decision points.

**Suggested implementation order:** Proposal 2 first (higher per-incident savings, simpler adaptation since rf-qa's fix-cycle protocol already exists), then Proposal 1.

---

## Open Questions

1. Should the hypothesis-gate be opt-out (on by default) or opt-in? On-by-default maximizes token savings but adds overhead to simple issues.
2. What is the minimum hypothesis count that warrants spawning rf-qa? For single-hypothesis cases, the validation overhead may not justify the spawn cost.
3. Should rf-qa's fix-verification phase have `fix_authorization: true` (allow rf-qa to fix issues it finds in the applied fix) or always report-only?
4. How should the new rf-qa phases (`hypothesis-gate`, `fix-verification`) be documented -- as additions to the rf-qa agent definition, or as inline protocol in the troubleshoot command spec?
5. Should sc:troubleshoot gain a `--deep` flag that enables both proposals plus additional rf-qa-qualitative review of the diagnostic report?

---

## Next Steps

- Use `/sc:design` to architect the hypothesis-gate and fix-verification QA phases
- Use `/sc:tdd` to create a technical design document for the pipeline changes
- Define the new rf-qa checklist items in detail for both phases
- Prototype with a real troubleshooting scenario to measure actual token savings
