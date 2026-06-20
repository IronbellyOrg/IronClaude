# Reviewer Specification

This reference governs Wave 3A (T2 reviewer composition) of `sc-reflect-protocol`. It defines (1) the per-reviewer brief package shape materialized at Step 3B.0 and (2) the composition rules — model/persona rotation, the instance-level independence guarantee, rotation fill logic, and the Khan ICML 2024 judge-class collision avoidance principle.

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

**FR-1 implementor-list hunks.** When §6.1 step 3b `find_implementations` enumerated the polymorphic surface of an abstract symbol the reviewer will cite, that implementor list is injected into this `## Grounding hunks` block as additional `file:line` H3 hunks (one per implementor site) so reviewers see the full abstract-symbol implementor set, not just the abstract declaration. The `file:line` hunk-shape convention is unchanged.

**FR-3 extended-info references.** When §6.1 step 4 ran `find_referencing_symbols` with `include_info: true`, the richer reference context (docstrings + signatures from the extended-info return shape) is surfaced into the same grounding-hunks block alongside the plain `file:line` reference hunks — denser reference grounding without a new brief structure. The `reviewer_briefs_materialized` contract emission is unchanged.

**FR-4 verification-results hunk.** When §6.1 step 5.5 ran the verification triangle, a grounding-hunk entry carrying the artifact-path ref `<output>/verify-logs/invocations.yaml` (the per-invocation `evidence_ref` array: `{cmd, exit_code, deviation_class, ...}`) is injected into this `## Grounding hunks` block for the **`qa`-persona** reviewer (persona-filtered — the qa reviewer owns the coverage/acceptance/verification surface). The artifact ref is preserved verbatim so the Wave-5 evidence-validator can re-Read it. This is an entry under the existing `## Grounding hunks` section — NOT a fourth brief section; the "exactly three sections" invariant is unchanged.

**FR-RV3-MED.1 hierarchy-slice hunk.** When §6.1 step 4.5 ran `type_hierarchy`, a grounding-hunk entry carrying the artifact-path ref `<output>/artifacts/hierarchy-slice.yaml` (the materialized transitive supertype/subtype family, FR-1 `hierarchy_slice_path`) is injected into this `## Grounding hunks` block for the **`analyzer`/`architect`-persona** reviewer (persona-filtered — they own the structural/lineage surface). The artifact ref is preserved verbatim so the Wave-5 evidence-validator can re-Read it. Like the FR-4 entry, this is an entry under the existing `## Grounding hunks` section — NOT a fourth brief section; the "exactly three sections" invariant is unchanged.

**D13 spec-body hunks (UC-1).** In UC-1 runs, the SPEC BODY ITSELF is injected into this `## Grounding hunks` block for the **`qa`-persona** reviewer (persona-filtered, the same FR-4 pattern: the qa reviewer owns the coverage/acceptance surface): whole-file as a single fenced hunk when the spec is 400 lines or fewer; otherwise per-section hunks (one H3 per top-level spec section) covering 100 percent of the spec body. Each hunk carries its `file:line-range` ref so the Wave-5 evidence-validator can re-Read it. The qa reviewer's persona instructions gain one line: "Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding." This is the recall backstop behind the Step 1B.0 two-pass extraction: even if Pass 2 under-extracts, one reviewer reads the source document rather than the matrix derived from it. An entry under the existing `## Grounding hunks` section, NOT a fourth brief section; the "exactly three sections" invariant is unchanged.

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

### Instance-level independence guarantee (anti-self-confirmation, structural)

The executor's model class is NEVER removed from the reviewer pool. Self-confirmation is an instance-and-context phenomenon, not a model-class one (spec §1 thesis): the unreliable case is the same instance, carrying the formation context that produced the work, re-grading that work. A fresh, independently spawned reviewer is not that instance even when it runs on the same model class. Instance-level independence is guaranteed structurally by (1) fresh subagent spawn per reviewer (Wave 3, Step 3B), (2) a brief that carries no executor formation context, and (3) blind calibration of every card (§11.3). The `--executor-model <class>` flag and the `EXECUTOR_MODEL_CLASS` env var are accepted as recorded provenance and otherwise ignored: no class is removed, no tier is degraded, and `executor_exclusion_degraded` is not emitted. There is no Wave 0 step 0.5b executor-class-resolution sub-step.

**Class-diversity preference (prefer, never require).** A panel spanning more distinct classes catches more class-level blind spots, so reflect fills reviewer slots to prefer maximal model-class diversity from the resolved alias set. It NEVER drops a slot, degrades a tier, or excludes a class to honor this preference; `t2_model_class_diversity: full | degraded` is the soft signal, where `degraded` is a missed diversity bonus, NOT a weakened anti-self-confirmation guarantee.

### Reviewer rotation table

| Reviewer count | Model rotation (class-diversity-preferring) | Persona rotation |
|----------------|----------------|------------------|
| 2 (`--reviewers 2`) | sonnet, haiku | analyzer, qa |
| 3 (default) | sonnet, haiku, (qwen \| kimi \| deepseek if alias available; else opus) | analyzer, qa, refactorer |
| 3 with `--strategy enterprise` | sonnet, haiku, opus | analyzer, qa, architect |

### Rotation fill logic (no executor removal)

No class is removed on the basis of matching the executor's class. Reflect fills the rotation table row for the requested N, preferring distinct classes:

1. Fill the rotation slots for the requested N from the resolved alias set, preferring maximal distinct-class coverage.
2. If fewer than N distinct classes resolve, repeat a resolvable class to keep N slots filled (a fresh same-class reviewer is still instance-independent) rather than dropping a slot.
3. The N=2 minimum is the hard T2 floor (spec §7.1): below it, T2 cannot fire. The floor is reached only when fewer than 2 reviewer slots can be filled at all, never because of an executor-class collision.

### Khan ICML 2024 judge-class collision avoidance

The merge judge in Wave 4 is `sc-adversarial-protocol`'s internal scoring; per Khan et al. ICML 2024 Oral, the judge being a *different* class than the debaters is the right default. The protocol does not pin a judge model — sc-adversarial owns that selection.

This means the three classes — **executor**, **reviewers**, and **calibrator/judge** — form a partition. Any collision among them weakens the structural anti-self-confirmation guarantee. Reflect enforces executor-vs-reviewer disjointness directly (via the exclusion rule above) and delegates reviewer-vs-judge disjointness to `sc-adversarial-protocol`'s judge selection.
