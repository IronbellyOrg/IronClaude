# Reviewer Specification

This reference governs Wave 3A (T2 reviewer composition) of `sc-reflect-protocol`. It defines (1) the per-reviewer brief package shape materialized at Step 3B.0 and (2) the composition rules — model/persona rotation, the executor-class exclusion rule, post-removal logic, and the Khan ICML 2024 judge-class collision avoidance principle.

Consumed by: Wave 3A (T2 reviewer composition).

---

## Brief template

**Step 3B.0 (materialize per-reviewer brief packages).** Before spawning N reviewers, the orchestrator materializes one brief per reviewer at:

```text
<output>/reviewer-briefs/reviewer-<N>.md
```

Where `<N>` is the 1-indexed reviewer ordinal (e.g., `reviewer-1.md`, `reviewer-2.md`, `reviewer-3.md`).

Each brief is **self-contained**, so reviewers run truly in parallel without orchestrator round-trips. Brief file shape is testable via the `yaml_field` grader assertion.

### Required sections (per brief)

A reviewer brief MUST contain exactly these three sections, in this order:

#### `## T1 card excerpt`

The slice of the Tier 1 reflection card relevant to **this reviewer's persona**. For example, the `analyzer` reviewer receives the root-cause / deviation section; the `qa` reviewer receives the coverage / acceptance section; the `refactorer` reviewer receives the structural / tech-debt section.

The slice is a verbatim excerpt from `<output>/t1-card.md` — not a paraphrase.

#### `## Grounding hunks`

Reviewer-scoped grounding hunks: `file:line` excerpts pulled from Wave 1A's grounding pass. Each hunk is filtered to those the reviewer's persona will actually cite.

Example shape — the brief contains an H2 `## Grounding hunks` heading followed by one H3 per hunk; each H3 is the `file:line-range` ref, and the H3 body is the language-tagged fenced code block of the source excerpt. For example, an H3 like `### src/superclaude/pm_agent/confidence.py:42-58` is followed by a ```` ```python ```` fenced block containing the verbatim source between lines 42 and 58. The same shape is used for test files, e.g., H3 `### tests/pm_agent/test_confidence.py:101-115` followed by the corresponding fenced Python block.

Each hunk preserves the `file:line` ref so the `evidence-validator` agent can re-Read it at the Wave 5 final gate.

#### `## Coverage slice`

The coverage-matrix slice containing **only the rows this reviewer is responsible for**. For UC-1, this is the requirement-to-card mapping subset; for UC-2, this is the tasklist-task-to-diff-hunk mapping subset.

Example shape:

```markdown
## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| REQ-014: confidence floor | C-04 | covered | confidence.py:42 |
| REQ-015: alternatives surface | C-05 | partial | confidence.py:71 |
```

### Contract emission

When Step 3B.0 completes, the contract emits `reviewer_briefs_materialized: <N>` (count of brief files written). Reviewer spawning Wave 3A reads each brief from disk; no in-memory state is shared between reviewers.

---

## Composition

Reviewers are heterogeneous by model class AND by persona, to maximise representational diversity (per Topic 2 research, Wisdom of Silicon Crowd, LLM-TOPLA). Reviewer counts are clamped by the §4 Wave 0 alias-routing table.

### Executor-class exclusion rule (anti-self-confirmation, structural)

The *executor* (the agent whose work is under review) MUST NOT appear in the reviewer pool. Reflect resolves the executor's model class at Wave 0 step 0.5b (a new sub-step inserted between alias resolution and reviewer composition) from `--executor-model <class>` flag, the `EXECUTOR_MODEL_CLASS` env var, or — if neither is set — from the most-recent commit-author hint in the task log (heuristic; emit `executor_class_source: flag | env | log-heuristic | unknown` to telemetry). When the executor's class is in the candidate rotation, it is **removed** from the rotation; if removal drops reviewer count below the gate floor (N=2 minimum for T2), reflect emits `executor_exclusion_degraded: true` and degrades to T1 with WARN: `"executor class collides with reviewer pool; N=2 floor cannot be satisfied with disjoint set."` This rule extends the §11.3 disjoint-set principle (calibrator class disjoint from reviewer classes) to also separate **executor class from reviewer classes** — the three classes (executor, reviewers, calibrator) form a partition where collisions weaken the structural anti-self-confirmation guarantee.

When `executor_class_source == unknown` (no flag, no env var, no log hint), reflect proceeds with the standard rotation and emits `executor_class_resolved: false` + WARN: `"executor class not resolved — anti-self-confirmation guarantee weakened; pass --executor-model to enforce."` This is fail-open by design: missing executor identity is not a STOP condition, but the weakened guarantee is logged loudly.

### Reviewer rotation table

| Reviewer count | Model rotation (BEFORE executor-class removal) | Persona rotation |
|----------------|----------------|------------------|
| 2 (`--reviewers 2`) | sonnet, haiku | analyzer, qa |
| 3 (default) | sonnet, haiku, (qwen \| kimi \| deepseek if alias available; else opus) | analyzer, qa, refactorer |
| 3 with `--strategy enterprise` | sonnet, haiku, opus | analyzer, qa, architect |

### Post-removal logic

Post-removal: if the executor is `sonnet`, the N=3 default rotation becomes `haiku, (qwen|kimi|deepseek|opus)` and reflect adds the next-available class from the resolved alias set to restore N=3, or degrades to N=2 if no replacement is available. The N=2 minimum is hard — below it, T2 cannot fire (see executor-exclusion-degraded path above).

Concretely, post-removal proceeds in this order:

1. Resolve executor class from `--executor-model` / `EXECUTOR_MODEL_CLASS` / log heuristic.
2. Remove the matching class entry from the rotation table row for the requested N.
3. If post-removal count < N, attempt to backfill from the next available alias class (qwen, kimi, deepseek, opus — whichever is alias-resolvable and not already in the rotation).
4. If backfill fails to reach N, attempt to satisfy the N=2 floor.
5. If N=2 cannot be satisfied with a disjoint set, emit `executor_exclusion_degraded: true` and degrade to T1.

### Khan ICML 2024 judge-class collision avoidance

The merge judge in Wave 4 is `sc-adversarial-protocol`'s internal scoring; per Khan et al. ICML 2024 Oral, the judge being a *different* class than the debaters is the right default. The protocol does not pin a judge model — sc-adversarial owns that selection.

This means the three classes — **executor**, **reviewers**, and **calibrator/judge** — form a partition. Any collision among them weakens the structural anti-self-confirmation guarantee. Reflect enforces executor-vs-reviewer disjointness directly (via the exclusion rule above) and delegates reviewer-vs-judge disjointness to `sc-adversarial-protocol`'s judge selection.
