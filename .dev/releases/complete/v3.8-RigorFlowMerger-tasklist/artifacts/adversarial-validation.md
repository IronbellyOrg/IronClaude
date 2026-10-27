# Adversarial Validation: All 5 Proposals

**Generated**: 2026-04-02
**Method**: 5 parallel adversarial agents, quick depth (1 round), 3 variants per proposal (Baseline / Proposed / Conservative Alternative)
**Focus areas**: Correctness, Complexity, Operational Cost, Maintainability, Determinism

---

## Executive Summary

| # | Proposal | Verdict | Score (Proposed) | Score (Winner) | Winner Variant | Key Finding |
|---|----------|---------|-----------------|----------------|----------------|-------------|
| P3 | DNSP for Validation Agents | **ADOPT** | 39/50 (B) | 39/50 (B) | Proposed | Clear winner across 4/5 focus areas. Add all-agents-fail guard + synthetic metadata marker |
| P1 | Context-Armed Steps | **REVISE** | 22/50 (B) | 34/50 (C) | Conservative | Per-step context is overreach — generator can't produce reliable file paths from roadmap text. Revise to task-level `## Execution Context` block |
| P2 | Bounded Patch Loop | **REVISE** | 20/50 (B) | 39/50 (C) | Conservative | Subset-only re-validation is a structural correctness defect (oscillation risk). Prefer human checkpoint; if automation required, add full-set re-validation + monotonicity guard |
| P4 | Evidence-Anchored Validation | **REVISE** | 27/50 (B) | 39/50 (C) | Conservative | New Stage 6.5 with regex extraction is over-engineered. The 17-point quality gate already catches the same issues. Revise to pipe gate results to validation agents |
| P5 | Feedback-Driven Tier Calibration | **REVISE** | 23/50 (B) | 40/50 (C) | Conservative | Automatic tier modification violates operational determinism ("hidden input" problem). Revise to read-only advisory section — same information, human decides |

**Pattern**: 4 of 5 proposals were over-engineered. In each case the conservative alternative (Variant C) delivered 70-90% of the value at 10-30% of the complexity. Only P3 (DNSP) survived as proposed, because its change is genuinely minimal (~25 lines) and its failure mode (all-or-nothing validation abort) is genuinely harmful.

---

## P3: DNSP for Validation Agents

### Scoring Matrix

| Focus Area | A (Baseline) | B (Proposed) | C (Re-split+Retry) |
|------------|-------------|-------------|---------------------|
| Correctness | 4/10 | 7/10 | 8/10 |
| Complexity | 10/10 | 8/10 | 5/10 |
| Operational Cost | 5/10 | 9/10 | 6/10 |
| Maintainability | 10/10 | 8/10 | 5/10 |
| Determinism | 6/10 | 7/10 | 5/10 |
| **Total** | **35/50** | **39/50** | **29/50** |

**Convergence**: 0.80 — 4/5 focus areas favor B or show B in strong position.

### Debate Outcome
- Variant A's all-or-nothing failure mode is genuinely harmful: for a 5-phase roadmap (10 agents), even 5% per-agent failure rate yields ~40% chance of total validation loss
- Variant C (re-split failed range into sub-ranges) has the highest correctness ceiling but 3-4x the complexity for marginal gain. Sub-retries often fail on the same systemic issue
- Variant B is the sweet spot: converts total failure into graceful degradation with ~25 lines of logic

### Unresolved Conflicts
1. **Degenerate case**: What if ALL 2N agents fail? B would produce an all-synthetic report, creating false progress. Resolved by adding an all-agents-fail guard
2. **Correctness vs complexity trade-off**: C recovers real findings where B synthesizes placeholders. Acceptable trade-off given C's 3-4x complexity cost

### Recommendation: **ADOPT** with two refinements

### Refactored Proposal
Adopt as proposed, plus:
1. **All-agents-fail guard**: If `count(successful_agents) == 0`, raise StageError (same as current behavior). DNSP only activates when at least one agent succeeded
2. **Synthetic finding metadata**: Each synthesized finding carries `source: "synthetic-dnsp"` so downstream consumers can distinguish real from synthetic findings

Implementation: ~25 lines in orchestrator merge step.

---

## P1: Context-Armed Steps

### Scoring Matrix

| Focus Area | A (Baseline) | B (Per-Step Context) | C (Per-Task Block) |
|------------|-------------|---------------------|-------------------|
| Correctness | 6/10 | 5/10 | 7/10 |
| Complexity | 9/10 | 4/10 | 7/10 |
| Operational Cost | 7/10 | 5/10 | 7/10 |
| Maintainability | 9/10 | 4/10 | 7/10 |
| Determinism | 8/10 | 4/10 | 6/10 |
| **Total** | **39/50** | **22/50** | **34/50** |

**Convergence**: 0.75 — Consistent ordering A > C > B across 4/5 areas. Only Correctness favors C over A.

### Debate Outcome
- **Critical finding**: The generator operates on roadmap text, not the live codebase. Roadmaps rarely name specific source paths. Per-step `Context: src/middleware/` values would be hallucinated and go stale between generation and execution
- The claimed -10-20% execution savings is likely overstated (3-8% at best). When Context: values are wrong, the executor wastes tokens on bad references AND then searching for real paths
- Per-task context (Variant C) captures the benefit without per-step staleness risk
- The `Ensuring:` clause duplicates the existing Acceptance Criteria section — two sources of truth for verification

### Unresolved Conflicts
1. **Empirical token savings are unvalidated** — neither the proposal's -10-20% nor the counterargument's 3-8% is measured
2. **Generator capability gap** — if a future generator has codebase access, per-step context becomes viable
3. **`Ensuring:` vs Acceptance Criteria duplication** — whether this adds value depends on how executors use acceptance criteria today

### Recommendation: **REVISE** — reject per-step, adopt per-task

### Refactored Proposal: "Task Execution Context Block"
Add an optional `## Execution Context` section at the end of each task, after Steps:

```markdown
## Execution Context
- Roadmap refs: R-015 (rate limit requirements), R-003 (middleware architecture)
- Likely source area: middleware layer, configuration module
- Key constraints: must integrate with existing auth middleware chain
```

Key changes from original:
- **Task-level, not step-level** — one block per task, not per step
- **No specific file paths** — references "source areas" not `src/middleware/`. Executor resolves actual paths at runtime
- **No `Ensuring:` clause** — verification stays solely in Acceptance Criteria (single source of truth)
- **Optional** — included when roadmap provides sufficient context, omitted when speculative
- **Roadmap refs always included** — R-### links are known at generation time and cannot go stale

Impact: +1-3% generation size, -3-5% execution savings (conservative). Zero maintenance coupling.

---

## P2: Bounded Patch Loop

### Scoring Matrix

| Focus Area | A (Single-Pass) | B (Bounded Loop) | C (Human Checkpoint) |
|------------|-----------------|-------------------|---------------------|
| Correctness | 7/10 | 4/10 | 8/10 |
| Complexity | 9/10 | 4/10 | 8/10 |
| Operational Cost | 10/10 | 5/10 | 7/10 |
| Maintainability | 9/10 | 4/10 | 8/10 |
| Determinism | 7/10 | 3/10 | 8/10 |
| **Total** | **42/50** | **20/50** | **39/50** |

**Convergence**: 0.85 — Strong convergence on the key structural defect in Variant B.

### Debate Outcome
- **Critical finding**: The proposal re-validates only the UNRESOLVED subset after re-patching. This misses cross-item regressions — patching item A can break previously-RESOLVED item B, which goes undetected. This is a structural correctness defect, not a theoretical concern
- `sc:task-unified` is non-deterministic (LLM-based). The same UNRESOLVED finding may produce different patches on each invocation. Convergence is not guaranteed; oscillation is possible
- RF empirical data: 21 retry files across 18 batches (~117% retry ratio) shows corrections are common, not rare as the proposal assumed. RF mitigates with full re-QA of the entire batch, not just failed items
- The status quo (A) scored 42/50 — surprisingly competitive because its failure mode (log and stop) is honest and safe

### Unresolved Conflicts
1. **UNRESOLVED frequency in sc:tasklist context specifically** is unknown — RF retry data may not transfer directly
2. **Full-set re-validation would fix B's correctness defect** but roughly doubles spot-check cost per cycle
3. **Automation requirement**: C requires a human, which breaks CI/CD pipelines. If unattended operation is required, B must be amended

### Recommendation: **REVISE** — prefer human checkpoint; amend if automation required

### Refactored Proposal: Dual-Mode Patch Recovery
- **Interactive mode**: After Stage 10, if UNRESOLVED > 0, call AskUserQuestion: "N findings remain unresolved. Re-attempt patches or accept as-is?" Human decides. (~5 lines of logic)
- **Automated mode** (if `--non-interactive`): One retry cycle with these safeguards:
  1. **Full-set re-validation** — re-check ALL items, not just UNRESOLVED
  2. **Monotonicity guard** — halt if |UNRESOLVED_new| >= |UNRESOLVED_prev|
  3. **Regression detection** — halt if any previously-RESOLVED item becomes UNRESOLVED
  4. **Cap at 2 total passes** (1 original + 1 retry) — RF experience shows diminishing returns beyond first retry
  5. **Fallback to human checkpoint** — if guards trigger and running interactively, ask user rather than silently stopping

---

## P4: Evidence-Anchored Validation

### Scoring Matrix

| Focus Area | A (No Evidence) | B (JSON Evidence) | C (Gate Passthrough) |
|------------|-----------------|-------------------|---------------------|
| Correctness | 6/10 | 5/10 | 8/10 |
| Complexity | 10/10 | 4/10 | 9/10 |
| Operational Cost | 6/10 | 7/10 | 8/10 |
| Maintainability | 9/10 | 4/10 | 8/10 |
| Determinism | 4/10 | 7/10 | 6/10 |
| **Total** | **35/50** | **27/50** | **39/50** |

**Convergence**: 0.82 — Strong convergence toward C. Only determinism showed a narrow B advantage.

### Debate Outcome
- **Central paradox**: If the 17-point quality gate already catches orphan deliverables and missing roadmap items before writing, those issues should not appear in generated files. The evidence JSON's key fields would be empty in any successful run. If the gate fails and the pipeline proceeds (a separate bug), the evidence extraction is solving the wrong problem
- Regex extraction creates a new failure surface with disproportionate authority — validation agents are told to treat evidence as "machine-verified facts," so regex bugs produce HIGH-severity false positives that agents will not question
- The JSON schema is tightly coupled to ID formats (T<PP>.<TT>, D-####, R-###). Format changes break the regex silently
- Variant C (pipe existing gate results) captures 80% of B's value at 10% of B's complexity

### Unresolved Conflicts
1. **Future semantic evidence** — B's schema could extend to embedding similarity scores, which would genuinely add value. But this future possibility doesn't justify present complexity
2. **Agent compliance** — whether agents actually use injected evidence vs re-deriving facts is empirically unverified
3. **Defense-in-depth argument** — B's proponents argue evidence is a separate check layer, but Variant C achieves the same defense by forwarding gate results

### Recommendation: **REVISE** — adopt Quality Gate Evidence Passthrough

### Refactored Proposal: "Quality Gate Evidence Passthrough"
No new stage. Extend Stage 6 (quality gate) to emit a structured text summary:

```
QUALITY GATE RESULTS (Stage 6)
Passed: 17/17
[PASS] Task ID uniqueness
[PASS] Deliverable registry completeness
[PASS] Roadmap item coverage
...
Structural integrity verified. No orphan deliverables. No missing roadmap items.
```

On failure:
```
Passed: 15/17
[FAIL] Deliverable registry completeness — 2 orphan deliverables: D-0042, D-0067
[FAIL] Roadmap item coverage — R-012 not found in any phase
```

Written to `TASKLIST_ROOT/validation/gate-results.txt` and injected into Stage 7 agent prompts with instruction: "All PASS items are machine-verified — do not re-check. All FAIL items are machine-verified defects — flag as HIGH. Focus on semantic quality."

**Upgrade path**: If future evidence shows agents benefit from granular ID data and ID formats have stabilized, upgrade gate-results.txt to structured JSON. One-file change, not a new pipeline stage.

---

## P5: Feedback-Driven Tier Calibration

### Scoring Matrix

| Focus Area | A (Stateless) | B (Auto-Calibrate) | C (Advisory) |
|------------|--------------|---------------------|--------------|
| Correctness | 7/10 | 5/10 | 8/10 |
| Complexity | 10/10 | 4/10 | 7/10 |
| Operational Cost | 6/10 | 5/10 | 8/10 |
| Maintainability | 10/10 | 5/10 | 8/10 |
| Determinism | 10/10 | 4/10 | 9/10 |
| **Total** | **43/50** | **23/50** | **40/50** |

**Convergence**: 0.85 — Strong convergence. All focus areas that initially appeared to favor B converged on C as a superior delivery mechanism.

### Debate Outcome
- **Determinism violation**: The protocol guarantees "same input -> same output" where input = roadmap text. Adding feedback-log.md as a hidden second input breaks this. Different feedback files → different tiers for the same roadmap. Users expecting reproducibility from the roadmap alone get surprising results
- **Task identity across versions**: If Roadmap v2 renames "Implement auth middleware" to "Build authentication layer," should old overrides apply? No matching strategy works reliably — exact match is brittle, fuzzy match is non-deterministic
- **STRICT downgrade risk**: Nothing prevents feedback from downgrading a security-critical task. A lazy executor marking STRICT → STANDARD propagates bad judgment forward
- **Variant C preserves determinism**: Advisory section varies with feedback, but all scored tiers are computed from roadmap text alone. Same roadmap → same tiers, always

### Unresolved Conflicts
1. **Who populates feedback-log.md?** Neither B nor C addresses this. Auto-population by Sprint executor needs schema specification
2. **Task identity across roadmap versions** — even an advisory benefits from some notion of task continuity
3. **Feedback-log.md schema enforcement** — malformed files need clear errors, not silent failure
4. **STRICT floor rule** — should STRICT-classified tasks be immune to downgrade suggestions?

### Recommendation: **REVISE** — advisory-only

### Refactored Proposal: "Tier Calibration Advisory"
Stage 0 reads feedback-log.md (if present), extracts rows where Override Tier != Original Tier (min 2 matching entries), and produces an advisory section in tasklist-index.md:

```markdown
## Tier Calibration Advisory (from feedback-log.md)

| Task Pattern | Original Tier | Suggested Tier | Override Count | Sample Reasons |
|---|---|---|---|---|
| *rate limit* | STANDARD | STRICT | 3 | "Involved auth paths", "Security boundary" |
| *migration* | STANDARD | STRICT | 2 | "Data integrity risk", "Rollback complexity" |

> WARNING: Row 1 suggests upgrading to STRICT. Review security implications before accepting.

*This advisory is informational. Tier scores above are computed from keyword matching only and are not modified by this advisory.*
```

Key properties:
- **Determinism preserved** — all scored tiers are roadmap-only. Advisory is informational
- **STRICT downgrade warning** — any advisory suggesting STRICT downgrade gets explicit warning
- **Graceful neglect** — missing or empty feedback-log.md → no advisory section (not an error)
- **Human in the loop** — the advisory surfaces data; the human decides whether to act

---

## Revised Priority Roadmap (Post-Adversarial)

```
Phase 1: Quick Wins
────────────────────
P3  DNSP for Validation Agents          ADOPT (as refined)     ~25 lines    Very Low risk
P1  Task Execution Context Block        REVISE (task-level)    Template edit Low risk

Phase 2: Core (interactive mode)
─────────────────────────────────
P4  Quality Gate Evidence Passthrough   REVISE (gate pipe)     ~15 lines    Very Low risk
P2  Dual-Mode Patch Recovery            REVISE (human+auto)    ~30 lines    Low risk

Phase 3: Long-Term
───────────────────
P5  Tier Calibration Advisory           REVISE (advisory)      ~40 lines    Low risk
```

### What Changed from Pre-Adversarial Roadmap

| Proposal | Pre-Adversarial | Post-Adversarial | Why |
|----------|----------------|------------------|-----|
| P3 | Adopt | **Adopt** (confirmed) | Clean winner. Two minor refinements added |
| P1 | Adopt (per-step) | **Revise** (per-task) | Generator can't produce reliable per-step file paths from roadmap text. Per-task block is sufficient |
| P2 | Adopt (auto loop) | **Revise** (human checkpoint + guarded auto) | Subset-only re-validation has oscillation defect. Full-set re-validation + monotonicity guard required for automation |
| P4 | Adopt (new Stage 6.5) | **Revise** (gate passthrough) | New extraction stage is over-engineered. Existing quality gate already catches the same issues |
| P5 | Adopt (auto calibration) | **Revise** (advisory only) | Auto-modification violates operational determinism guarantee. Advisory preserves determinism while surfacing the same information |

### Net Complexity Reduction

| Proposal | Pre-Adversarial Estimate | Post-Adversarial Estimate | Reduction |
|----------|------------------------|--------------------------|-----------|
| P3 | ~20 lines | ~25 lines | +5 (guards added) |
| P1 | Template + protocol logic | Template only | -60% |
| P2 | Loop wrapper (~50 lines) | Conditional + optional guards (~30 lines) | -40% |
| P4 | New stage + schema + dir + prompts | ~15 lines gate output + prompt append | -80% |
| P5 | New stage + parsing + injection | ~40 lines parsing + advisory render | -50% |
| **Total** | ~200+ lines across 5 proposals | ~110 lines across 5 proposals | **-45%** |
