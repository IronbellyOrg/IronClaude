# Phase File Template (`phase-N-tasklist.md`)

Read-only reference extracted from SKILL.md Section 6B. This file exists for human review; the skill uses its own inline copy.

---

Each phase file is a **self-contained execution unit**. It contains only the tasks for that phase plus inline checkpoints. It does NOT contain registries, traceability matrices, templates, or completion protocol instructions.

## Phase Frontmatter and Heading

```text
---
executor_model_class: "<EXECUTOR_CLASS>"
start_commit: "<PHASE_N_START_SHA>"
---
# Phase N -- <Phase Name>
```

- Each phase file begins with a minimal YAML frontmatter block (`executor_model_class` for the O2 wrapper's `--executor-model` reviewer exclusion, optional `start_commit`), immediately followed by the `# Phase N -- <Name>` heading
- **Do NOT seed a `reflect_post:` key or a `# reflect_post` comment line inside the frontmatter** — the wrapper appends `reflect_post:` into the block itself; a `#`-prefixed comment line would be mis-read as the phase heading by the Sprint `_extract_phase_name` scanner (it returns the first `#` line)
- Level-1 heading (`#`) with em-dash separator
- Phase name portion must not exceed 50 characters
- Required for Sprint CLI TUI display name extraction; `count_tasks_in_file` / `parse_tasklist` / `_extract_phase_name` tolerate the leading `---` block (no `### T` heading, and with no `#` comment, no false phase heading)
- Include a one-paragraph phase goal (2-3 sentences max, derived from roadmap)

## Task Format

```text
### T<PP>.<TT> -- <Task Title>
```

| Field | Value |
|---|---|
| Roadmap Item IDs | `R-###` (comma-separated; must include at least 1) |
| Why | <1-2 sentences derived from roadmap> |
| Effort | `<XS|S|M|L|XL>` |
| Risk | `<Low|Medium|High>` |
| Risk Drivers | `<matched categories/keywords only>` |
| Tier | `<STRICT|STANDARD|LIGHT|EXEMPT>` |
| Confidence | `[████████--] XX%` |
| Requires Confirmation | `Yes | No` (Yes if confidence < 0.70) |
| Critical Path Override | `Yes | No` |
| Verification Method | `<method per tier>` |
| MCP Requirements | `<Required: X, Y | Preferred: Z | None>` |
| Fallback Allowed | `Yes | No` |
| Sub-Agent Delegation | `Required | Recommended | None` |
| Deliverable IDs | `D-####` (comma-separated; must include at least 1) |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-####/spec.md`
- `TASKLIST_ROOT/artifacts/D-####/notes.md`
- `TASKLIST_ROOT/artifacts/D-####/evidence.md`

**Execution Context** (optional, deterministic): a phase task MAY carry an optional task-level `## Execution Context` block — emitted per the Stage-4 deterministic emission rule (Section 4.1d of `SKILL.md`) — reusing the task-builder `References` / `Source areas` / `Key constraints` sub-field contract VERBATIM. The block carries NO specific `file:line` references and NO `src/...` paths in its header (named source areas only, not file paths; specific paths are never emitted by this generator (roadmap-text-only input)), includes NO `Ensuring:` clause, and never duplicates or overrides the Acceptance Criteria (the single source of truth). Exact shape:

```markdown
## Execution Context
- References: <the resolved R-### roadmap reference(s); always present when the block is emitted>
- Source areas: <named module(s)/area(s), not file paths; listed when the roadmap supplies them, omitted in the References-only degraded form>
- Key constraints: <the first 1-3 stated invariants in roadmap appearance order; omitted when the roadmap supplies none>
```

**Deliverables:**

- 1-5 concrete outputs

**Steps:**

1. **[PLANNING]** Load context and identify scope
2. **[PLANNING]** Check dependencies and blockers
3. **[EXECUTION]** ...
4. **[EXECUTION]** ...
5. **[VERIFICATION]** Validation step aligned to tier
6. **[COMPLETION]** Documentation and evidence

**Acceptance Criteria:** (exactly 4 bullets)

- Functional completion (MUST name specific, verifiable output)
- Quality/safety criterion
- Determinism/repeatability criterion
- Documentation/traceability criterion

**Validation:** (exactly 2 bullets)

- Manual check: ...
- Evidence: linkable artifact produced

**Dependencies:** `<Task IDs or "None">`
**Rollback:** `TBD` or as stated in roadmap
**Notes:** <optional; max 2 lines>

### Near-Field Completion Criterion

The first Acceptance Criteria bullet MUST name a specific, objectively verifiable output.

**Accepted forms:**

- A named file or artifact at a specific path
- A test command outcome with specific test suite
- An observable state with measurable criteria

**Rejected forms (fail self-check):**

- "Implementation is complete."
- "The feature works correctly."
- "Tests pass." (without specifying which tests)
- "Documented." (without specifying what document)

### Acceptance Criteria Specificity Rules

- STRICT tasks: ALL criteria must be artifact-referencing
- STANDARD tasks: >=1 criterion must be artifact-referencing
- LIGHT and EXEMPT tasks: no minimum

## Inline Checkpoints

```text
### Checkpoint: Phase <P> / Tasks <start>-<end>
```

**Purpose:** ...
**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/<deterministic-name>.md`
**Verification:** (exactly 3 bullets)
**Exit Criteria:** (exactly 3 bullets)

Deterministic name format:

- Range checkpoints: `CP-P<PP>-T<start>-T<end>.md`
- End-of-phase: `CP-P<PP>-END.md`

## End-of-Phase Checkpoint (Mandatory)

Every phase file MUST end with an end-of-phase checkpoint as its last *checkpoint*:

```text
### Checkpoint: End of Phase <N>
```

This checkpoint serves as the gate for the next phase and must include all standard checkpoint fields. When reflect gating is enabled (the default; disabled by `--no-reflect`), the templated post-execution reflection task below is the **sole** task permitted to follow this checkpoint and is the absolute last task in the file.

## Terminal Post-Execution Reflection Task (when reflect gating is enabled)

> Mirror of the SKILL.md Section 6B inline copy — kept in sync for human review. When reflect gating is enabled, the generator appends exactly ONE fixed terminal task per phase file, AFTER the end-of-phase checkpoint. It uses the standard Sprint-CLI task shape, is Tier EXEMPT (reflect is the auditor, so it is **exempt from the artifact-referencing Acceptance-Criteria minimum**), carries a `**Reflect Report Path:**` (not a Checkpoint Report Path), and its `<PHASE_N_START_SHA>` is resolved at execution time by the task's Step-1 `[VERIFICATION]` (the phase's start commit, a single ref vs the working tree; never a fabricated SHA). The gate is a flat `superclaude reflect run` Bash shell-out wrapped in the `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` recursion-breaker skip guard (never the `sc:task` execution command; re-execution uses `/task`).

````markdown
### T<PP>.<final> -- Post-Execution Reflection: superclaude reflect run (wrapper shell-out)

| Field | Value |
|---|---|
| Roadmap Item IDs | <all R-### in this phase, comma-separated> |
| Why | Independent post-execution deviation audit of every task in Phase <PP>, run by the reflect wrapper after all phase work completes (the wrapper spawns an executor-disjoint reflect ensemble internally). |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT  (* reflect is the auditor; it is not itself tier-verified *) |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification (reflect IS the verification) |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | No (flat `superclaude reflect run` Bash shell-out; the wrapper spawns the executor-disjoint reflect ensemble internally) |
| Deliverable IDs | D-RF<PP> |

**Reflect Report Path:** `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md`

**Gate Command (flat wrapper shell-out, recursion-guarded):** Run, as a single Bash command, the §3.2 skip guard followed by the wrapper invocation:
```bash
if [ "${SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE:-0}" = "1" ]; then
  echo "reflect-wrapper recursion breaker: nested gate suppressed"; exit 0
fi
superclaude reflect run TASKLIST_ROOT/phase-<PP>-tasklist.md --depth deep --fix --no-promote --base <PHASE_N_START_SHA> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/
```

`--depth deep` is fixed (contract §2 — no `--tier`, no TCS-derived depth at the POST gate). `--no-promote` is REQUIRED (contract §5 — there is no per-phase promotion adapter). `--base <PHASE_N_START_SHA>` is a runtime-resolved placeholder pinning the audit to this phase's work as a SINGLE ref vs the working tree (NOT a `<base>..HEAD` range); see Step 1. `<EXECUTOR_CLASS>` is NOT passed as a flag — the wrapper sources the reviewer-exclusion class from the phase file's frontmatter `executor_model_class` (contract §6). The wrapper spawns the reflect ensemble internally; the gate uses `superclaude reflect run`, never the `sc:task` execution command (re-execution uses `/task`). Emit NO `--reflect`, NO `--max-turns`, and no agent-spawn directive.

**Steps:**

1. **[VERIFICATION]** Resolve `<PHASE_N_START_SHA>` at execution time = the SHA of the commit immediately preceding Phase <PP>'s first task commit (e.g. the recorded phase-start SHA, or `git rev-parse` of the prior phase's end). It is a SINGLE ref — the wrapper diffs it against the working tree, NOT a `<base>..HEAD` range. Substitute the resolved SHA into the Gate Command's `--base` before invoking it. `<PHASE_N_START_SHA>` is a placeholder, NEVER pre-filled with a fabricated generation-time SHA.
2. **[VERIFICATION]** Run the Gate Command above. The wrapper spawns the executor-disjoint reflect ensemble internally and runs the bounded `--fix` audit→apply→re-verify loop; consume its exit code (only `0` completes the gate; `10`/`11`/`2` FAIL and are surfaced).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression). ALSO open the machine `return-contract.yaml` at `reflect_post.contract` (equivalently `<Gate-Command --output>/return-contract.yaml`) and reconcile it with the `reflect_post` block, and FAIL the gate — even when the wrapper exited `0` — if ANY of (all reads via safe `.get(...)` defaults): the honest derived `reflect_post.verdict` is not `pass` (the raw contract `status` stays `success` by design, so it is forward-defensive, not the load-bearing signal); `adversarial_subrun_status` is `partial` or `failed`; `tier_reached == 2` AND `adversarial_convergence_score` is present AND `< 0.80`; or `deviation_count_by_class.drift`/`.regression` `> 0`. The worst-of `subrun_status`/`subrun_status_partial` are surfaced for observability ONLY and never fail the gate (a benign 2-of-3 swarm quorum with a healthy adversarial run stays PASS).

**Acceptance Criteria:** (exactly 5 bullets)

- File `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` exists with a deviation-taxonomy summary.
- The wrapper exited `0` (clean OR auto-fixed-and-verified by the bounded `--fix` loop); exit `10`/`11`/`2` FAILS the gate and is surfaced.
- Reflect ran with executor-disjoint reviewers (the class in the phase file's frontmatter `executor_model_class` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase <PP>.
- The machine `return-contract.yaml` at `reflect_post.contract` was opened and reconciled with the `reflect_post` block; the gate FAILs (even at wrapper exit `0`) if the honest derived `reflect_post.verdict` != `pass` (the raw contract `status` stays `success` by design), `adversarial_subrun_status` ∈ {partial, failed}, `tier_reached == 2` with `adversarial_convergence_score` present and `< 0.80`, or `deviation_count_by_class.drift`/`.regression` > 0; the worst-of `subrun_status`/`subrun_status_partial` are observability-only and never fail the gate.

**Validation:**

- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase <PP>.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
````
