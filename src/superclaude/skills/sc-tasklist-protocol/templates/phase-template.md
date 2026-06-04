# Phase File Template (`phase-N-tasklist.md`)

Read-only reference extracted from SKILL.md Section 6B. This file exists for human review; the skill uses its own inline copy.

---

Each phase file is a **self-contained execution unit**. It contains only the tasks for that phase plus inline checkpoints. It does NOT contain registries, traceability matrices, templates, or completion protocol instructions.

## Phase Heading and Goal

```text
# Phase N -- <Phase Name>
```

- Level-1 heading (`#`) with em-dash separator
- Phase name portion must not exceed 50 characters
- Required for Sprint CLI TUI display name extraction
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

> Mirror of the SKILL.md Section 6B inline copy — kept in sync for human review. When reflect gating is enabled, the generator appends exactly ONE fixed terminal task per phase file, AFTER the end-of-phase checkpoint. It uses the standard Sprint-CLI task shape, is Tier EXEMPT (reflect is the auditor, so it is **exempt from the artifact-referencing Acceptance-Criteria minimum**), carries a `**Reflect Report Path:**` (not a Checkpoint Report Path), and its `<phase-commit-range>` is resolved by the Sprint executor at run time (never a fabricated SHA). The spawn directive uses `/sc:reflect` (never `/sc:task`).

```markdown
### T<PP>.<final> -- Post-Execution Reflection: sc:reflect --mode post

| Field | Value |
|---|---|
| Roadmap Item IDs | <all R-### in this phase, comma-separated> |
| Why | Independent post-execution deviation audit of every task in Phase <PP>, in a fresh session, after all phase work completes. |
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
| Sub-Agent Delegation | Required (fresh-session reflect ensemble) |
| Deliverable IDs | D-RF<PP> |

**Reflect Report Path:** `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md`

**Spawn Directive (fresh session):** Spawn a NEW agent/session and run:
`/sc:reflect --mode post --remediate --tasklist TASKLIST_ROOT/phase-<PP>-tasklist.md --diff <phase-commit-range> --depth <DETERMINISTIC_DEPTH_for_phase_PP> --tier <DETERMINISTIC_TIER_for_phase_PP> --executor-model <EXECUTOR_CLASS> --output TASKLIST_ROOT/validation/reflect-post/phase-<PP>/`
(The reflect agent uses the default subagent model; `--executor-model` is the reflect-native exclusion flag naming the class that ran the phase's work — it does not select a model. Never `/sc:task`.)

**Steps:**
1. **[VERIFICATION]** Resolve `<phase-commit-range>` = the git range covering all of Phase <PP>'s task commits.
2. **[VERIFICATION]** Spawn a fresh session and invoke the Spawn Directive above (reflect audits the committed diff — cross-session-safe).
3. **[COMPLETION]** Confirm `REPORT.md` exists at the Reflect Report Path and surface its deviation counts (authorized/necessary/drift/regression).

**Acceptance Criteria:** (exactly 4 bullets)
- File `TASKLIST_ROOT/validation/reflect-post/phase-<PP>/REPORT.md` exists with a deviation-taxonomy summary.
- Zero `regression`-class deviations, OR a `--remediate` Tier-3 task was authored for each.
- Reflect ran with executor-disjoint reviewers (the `<EXECUTOR_CLASS>` passed via `--executor-model` was excluded from the reviewer pool).
- Report includes the per-task verdict matrix for Phase <PP>.

**Validation:**
- Manual check: reviewer confirms the deviation counts in REPORT.md.
- Evidence: the generated reflect REPORT.md.

**Dependencies:** all regular + checkpoint tasks in Phase <PP>.
**Rollback:** N/A (reflect is read-only audit; promotion is gated separately).
```
