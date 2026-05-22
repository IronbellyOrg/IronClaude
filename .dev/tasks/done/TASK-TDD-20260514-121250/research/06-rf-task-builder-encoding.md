# Research: rf-task-builder QA-Gate / Validation / Testing Encoding

**Status:** In Progress
**Date:** 2026-05-14
**Agent type:** Code Tracer
**Source:** src/superclaude/agents/rf-task-builder.md (493 lines)

---

## 1. BUILD_REQUEST → MDTM Transformation Pipeline

The rf-task-builder agent is a Rigorflow subagent (`src/superclaude/agents/rf-task-builder.md:1-26`) whose sole responsibility is to consume a structured `BUILD_REQUEST` message and emit a complete MDTM (Markdown-Driven Task Management) task file on disk. The agent has Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, Task, and Skill tools (`:6-25`).

### Inputs the Builder Reads

The canonical BUILD_REQUEST schema is documented at `:90-99`:

```
BUILD_REQUEST:
==============
GOAL: [What needs to be accomplished]
WHY: [Why this is needed]
TEMPLATE: [01 or 02]
QA_GATE_REQUIREMENTS: [NONE / FINAL_ONLY / PER_PHASE]
VALIDATION_REQUIREMENTS: [Validation checklist items to encode]
TESTING_REQUIREMENTS: [NONE / UNIT / INTEGRATION / E2E / ALL]
RESEARCH_CONTEXT: [Initial findings from researcher, if any]
```

A second optional field — `SKILL PHASES TO ENCODE` — is referenced at `:377-378` as taking precedence over `QA_GATE_REQUIREMENTS` (it provides exhaustive per-phase specifications). The builder also receives an optional `RESEARCH WORKSPACE` directory (`:280`) instead of a flat `RESEARCH_CONTEXT` string; when present, the builder Globs the directory for `.md` files and reads ALL of them (`:282-285`).

### Transformation Pipeline (6 Steps)

| Step | Lines | Action |
|------|-------|--------|
| 1. Receive | `:86-99` | Parse BUILD_REQUEST fields |
| 2. Read Template | `:101-115` | Read template 01 (generic) or 02 (complex) per the `TEMPLATE:` field |
| 3. Gather Context | `:118-155` | Either use `RESEARCH_CONTEXT`, message `rf-task-researcher` with `RESEARCH_NEEDED`, or broadcast `NEED_USER_INPUT` |
| 4. Synthesize | `:157-166` | Determine OUTPUTS, SOURCES, PHASES, STEPS, QA GATES, VALIDATION, TESTING |
| 5. Build Incrementally | `:168-196` | Write frontmatter + header (Write tool), then **one phase per Edit call**, then append Task Log section last |
| 6. Signal Completion | `:198-226` | Create a task in shared task list via `TaskCreate` and broadcast `TASK_READY` |

### Output Path Convention

The generated task file is written to `.dev/tasks/to-do/TASK-RF-<YYYYMMDD-HHMMSS>/TASK-RF-<YYYYMMDD-HHMMSS>.md` (`:465`). The folder must be created first (`:467`).

### Incremental Writing — #1 Anti-Failure Rule

Step 5 is enforced as the **highest priority Critical Rule** (`:473`). The builder MUST NOT compose the entire file in context and one-shot the Write — this exhausts max token output and freezes the process. Procedure:

- **5a** (`:174-183`): Write file containing only frontmatter (`---`, not `+++`), `# Title`, `## Task Overview`, `## Key Objectives`, `## Prerequisites & Dependencies`.
- **5b** (`:185-191`): For each phase, compose phase header + checklist items, then `Edit` the file to append. ONE phase per Edit call. Verify edit succeeded before continuing.
- **5c** (`:193-194`): Append `## Task Log / Notes` section last (execution log + findings templates).

### Generated File Structure — Frontmatter + Checklist + Task Log Scaffolding

The B2 self-contained checklist item pattern (`:230-244`) is what every generated checklist item must follow. The pattern is a single paragraph containing six load-bearing parts: (1) Context Reference + WHY, (2) Action + WHY, (3) Output Specification, (4) Integrated Verification ("ensuring..." clause with anti-hallucination), (5) Error Handling (log blocker in `### Phase [N] Findings` of Task Log, then mark complete), (6) Completion Gate ("Once done, mark this item as complete"). The verbatim pattern is at `:242-244`.

Granularity is enforced under MDTM A3/A4 (`:248-262`): one item per handler/file/component/iteration. Batched items like "Document all 14 handlers" are explicitly forbidden.

---

## 2. QA_GATE_REQUIREMENTS Encoding

Documented at `:340-358`. Behavior is value-driven:

| Value | What the Builder Encodes (verbatim `:344-346`) |
|-------|------------------------------------------------|
| `NONE` | No QA gate checklist items needed |
| `FINAL_ONLY` | Include a single QA validation phase before the final completion phase. This phase spawns rf-qa to verify all task outputs before marking Done. |
| `PER_PHASE` | Include QA gate checklist items after each major execution phase. Each gate spawns rf-qa (and optionally rf-qa-qualitative) to verify the preceding phase's outputs before proceeding. Use the M1 Phase-Gate QA Sequence pattern (Template 02) or the Phase Gate template section (both templates) from I15. |

### B2-Compliance for QA Items (`:348`)

Each QA gate item must specify in a single self-contained paragraph:
1. The agent to spawn (rf-qa or rf-qa-qualitative)
2. The QA phase type (research-gate / synthesis-gate / report-validation / task-integrity / qualitative)
3. The input files to verify
4. The output report path
5. The verdict handling (proceed on PASS, fix cycle on FAIL)
6. The error handling clause

### Layout Impact on Generated Task File

- `NONE` -> checklist contains only execution items + Task Log; no rf-qa references.
- `FINAL_ONLY` -> an additional QA-validation phase is appended just before completion; one rf-qa spawn item covers all outputs.
- `PER_PHASE` -> QA gate item(s) are appended at the END of every major execution phase. Template 02 path uses Section M1 (Phase-Gate QA Sequence) which is defined for template 02 only (`:113`). Both templates have the "Phase Gate template section" anchored from I15.

### Critical Rule 10 (`:482`) — Prose Gates Are Malformed

A QA gate described only in prose or comments is **invisible to the F1 executor** and will be skipped. A generated task file that omits required QA gate checklist items when `QA_GATE_REQUIREMENTS` is `FINAL_ONLY` or `PER_PHASE` is a MALFORMED output.

---

## 3. VALIDATION_REQUIREMENTS Encoding

Documented at `:360-362`. This field is **list-valued**, not enumerated. Each entry in `VALIDATION_REQUIREMENTS` is a free-form validation command/criterion (examples cited verbatim at `:362`: "Verify lint passes", "Verify type-check passes", "Verify build succeeds").

### Encoding Semantics

- Each validation entry -> one checklist item in the generated task file.
- Placement: **AFTER the phase they validate** (`:362`). Validation items for phase N are inserted at the end of phase N or as a small validation phase between phase N and phase N+1.
- The items still follow the B2 self-contained pattern (`:230-244`) — context, action, output, ensuring-clause, error-handling, completion gate.

### Critical Rule 11 (`:483`) — Validation Items Mandatory

When `VALIDATION_REQUIREMENTS` is non-empty, the builder MUST encode corresponding validation checklist items. A task file containing implementation items but no validation items is MALFORMED.

---

## 4. TESTING_REQUIREMENTS Encoding

Documented at `:364-374`. Enumerated values:

| Value | What the Builder Encodes (verbatim `:368-372`) |
|-------|-----------------------------------------------|
| `NONE` or `N/A` | No test items needed (docs-only or config tasks) |
| `UNIT` | Include checklist items that run unit tests covering modified code |
| `INTEGRATION` | Include integration test items |
| `E2E` | Include end-to-end test items |
| `ALL` | Include all applicable test tiers |

### Item Requirements (`:374`)

Testing items must specify:
- Test file locations
- Test commands (e.g., `uv run pytest tests/path/ -v`)
- Pass criteria
- Where results are captured

For Template 02, the L3 (Test/Execute) handoff pattern is used (`:374`, `:299` cross-ref). L3 writes results to `phase-outputs/test-results/`.

### Critical Rule 12 (`:484`) — Testing Items Mandatory

When `TESTING_REQUIREMENTS` is not `NONE` or `N/A`, the builder MUST encode testing checklist items with test file paths, commands, and pass criteria. Omitting them produces a MALFORMED task file.

### Precedence Rule (`:376-378`)

When BUILD_REQUEST contains BOTH `SKILL PHASES TO ENCODE` and `QA_GATE_REQUIREMENTS`, the `SKILL PHASES TO ENCODE` field is authoritative — it provides exhaustive per-phase specifications including QA gates. `QA_GATE_REQUIREMENTS` then serves as a structured summary. When only `QA_GATE_REQUIREMENTS` is present (standalone task-builder use), it is the sole authority. No analogous precedence rule is documented for `VALIDATION_REQUIREMENTS` or `TESTING_REQUIREMENTS`.

---

## 5. Retry-Monotonicity Integration Point (336-359 verbatim)

This is the FR-CONV.5 integration site. The current text in the agent file at `src/superclaude/agents/rf-task-builder.md:336-359`:

```
## QA Gate, Validation, and Testing Encoding (BUILD_REQUEST Fields)

When the BUILD_REQUEST includes `QA_GATE_REQUIREMENTS`, `VALIDATION_REQUIREMENTS`, or `TESTING_REQUIREMENTS`, you MUST encode corresponding checklist items in the generated task file. These fields are not informational — they are mandatory instructions.

### QA_GATE_REQUIREMENTS

| Value | What to Encode |
|-------|---------------|
| `NONE` | No QA gate checklist items needed |
| `FINAL_ONLY` | Include a single QA validation phase before the final completion phase. This phase spawns rf-qa to verify all task outputs before marking Done. |
| `PER_PHASE` | Include QA gate checklist items after each major execution phase. Each gate spawns rf-qa (and optionally rf-qa-qualitative) to verify the preceding phase's outputs before proceeding. Use the M1 Phase-Gate QA Sequence pattern (Template 02) or the Phase Gate template section (both templates) from I15. |

**QA gate items follow B2 self-contained pattern.** Each item must specify: the agent to spawn, the QA phase type, the input files to verify, the output report path, the verdict handling (proceed on PASS, fix cycle on FAIL), and the error handling clause.

**Fix cycle limits per gate type (from I16):**

| Gate Type | Max Cycles | After Max |
|-----------|-----------|-----------|
| research-gate | 3 | HALT and escalate |
| synthesis-gate | 2 | Open Questions |
| report-validation | 3 | HALT and escalate |
| task-integrity | 2 | Open Questions |
| Any qualitative gate | 3 | HALT and escalate |
```

### FR-CONV.5 Integration Plan (PRD Context)

FR-CONV.5 introduces two new retry-monotonicity invariants that must coexist with the existing 3-cycle hard limit:

1. **`F_{n+1} >= F_n` HALT** — If a fix cycle's failure-count is not monotonically non-increasing (i.e., a follow-up cycle introduces MORE failures than the prior cycle), HALT immediately and escalate. This protects against fix-cycles that regress quality.
2. **`PASS@N -> FAIL@N+1` regression HALT** — If an item that PASSED at cycle N then FAILS at cycle N+1 (a regression), HALT immediately and escalate.

These two new HALT conditions must be added as language in the existing I16 fix-cycle limits table or as a subsequent paragraph, working **in conjunction with** (not replacing) the per-gate cycle-count caps (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3). The natural site is between `:358` (end of the I16 table) and `:360` (start of `### VALIDATION_REQUIREMENTS`).

---

## 6. Per-Gate Fix-Cycle Limits Table (Verbatim from I16, `:352-358`)

| Gate Type | Max Cycles | After Max |
|-----------|-----------|-----------|
| research-gate | 3 | HALT and escalate |
| synthesis-gate | 2 | Open Questions |
| report-validation | 3 | HALT and escalate |
| task-integrity | 2 | Open Questions |
| Any qualitative gate | 3 | HALT and escalate |

**Notes:**
- The "After Max" column has two distinct terminal actions:
  - **HALT and escalate** — terminal failure surfaced to rf-team-lead (research-gate, report-validation, qualitative).
  - **Open Questions** — softer terminal action that drops the item into the task file's Open Questions section for human resolution rather than escalating (synthesis-gate, task-integrity).
- This semantic split matters for FR-CONV.5: the new monotonicity HALT must use the **HALT-and-escalate** action regardless of gate type, because a regression indicates instability that cannot be deferred to Open Questions.

---

## 7. Relationship Between rf-task-builder Agent and task-builder Skill

The two are layered:

- **rf-task-builder.md** (the file analyzed here) is the **subagent** definition. It is invoked via the `Task` tool with a fully-formed `BUILD_REQUEST` message and produces the MDTM file as its output. It owns: template selection (01/02), incremental file writing, B2 pattern compliance, A3/A4 granularity, QA/validation/testing item encoding per the BUILD_REQUEST.
- **task-builder SKILL.md** (the skill package at `src/superclaude/skills/task-builder/`) is the **orchestrator**. It owns: parallel codebase research, BUILD_REQUEST construction, quality gates around the builder, post-build verification.

### PR Allocation Pattern (from PRD context)

- **PR-01, PR-06, PR-07** — primarily skill-level changes (orchestration, BUILD_REQUEST construction, gate verification logic).
- **PR-02, PR-03** — touch BOTH rf-task-builder + skill (encoding semantics flow from BUILD_REQUEST schema into the agent's behavior, so both layers must change together).
- **PR-04, PR-05** — skill-level changes.

For **FR-CONV.5** specifically: the monotonicity HALT semantics need to be encoded as language the rf-task-builder embeds into generated QA gate checklist items (so the F1 executor will enforce them at runtime). The agent file is the natural site because Critical Rule 10 (`:482`) makes QA semantics in **prose** invisible to the executor — they must be in checklist-item form. Hence FR-CONV.5 is most likely a PR-02/03-class change touching both the agent file (336-359 region) and the skill (BUILD_REQUEST schema + gate verification).

---

## 8. Gaps and Questions

1. **No explicit VALIDATION list grammar** — `:362` examples are quoted strings, but the field's parsing rules (delimiter, escape, ordering vs phase number) are not specified. Builder behavior on a malformed list is undefined.
2. **L3 pattern referenced for testing items, but only template 02 has L3** — `:374` says "For Template 02, use the L3 (Test/Execute) pattern." It is unclear what testing pattern template 01 should use when `TESTING_REQUIREMENTS != NONE`.
3. **"M1 Phase-Gate QA Sequence pattern (Template 02)"** is cited at `:346` but not defined in this file — only template 02's PART 1 Section M defines it. Need to consult template 02 to know what M1 actually emits.
4. **No example BUILD_REQUEST with `SKILL PHASES TO ENCODE` field** — the precedence rule at `:376-378` references this field, but the BUILD_REQUEST schema at `:90-99` does not include it. The schema is non-exhaustive.
5. **Monotonicity HALT — where to record cycle history?** FR-CONV.5 requires comparing `F_{n+1}` vs `F_n` across cycles. The agent file does not specify where cycle history is persisted between fix cycles. Likely `phase-outputs/reviews/<gate>-cycle-N.md` (per L4 pattern, `:300`), but this needs confirmation.
6. **No "Open Questions" section template** — `:355, :357` say after-max action is "Open Questions" for synthesis-gate and task-integrity, but the structure of that section in the generated task file isn't defined here.
7. **Critical Rules 10/11/12 use "MALFORMED" terminology** — but no validator/linter is referenced. Detection presumably happens at task-builder skill verification time, not in the agent itself.

---

## 9. Stale Documentation Found

No `[CODE-CONTRADICTED]` or `[UNVERIFIED]` tags surfaced in this file. The agent itself defines a Documentation Staleness Awareness section (`:266-274`) for downstream research notes; it does not flag any of its own content as stale.

The cross-references to I15-I18 (`:115`), Section L (`:112, :289-332`), Section M (`:113`), and L3-L6 (`:299-302`) all refer to **the MDTM templates** (`01_mdtm_template_generic_task.md`, `02_mdtm_template_complex_task.md`), not to this agent file. Whether those template sections exist as-described is out-of-scope for this trace — flagging as a follow-up verification target.

**Tags applied to this report:**
- `[CODE-VERIFIED]` for all citations from `src/superclaude/agents/rf-task-builder.md:1-493`.
- `[UNVERIFIED]` for references to template content (I15-I18, L1-L7, M1-M2) — not read in this trace.

---

## 10. Summary

rf-task-builder is a single-purpose Rigorflow subagent that transforms a `BUILD_REQUEST` (`:90-99`) into an MDTM task file under `.dev/tasks/to-do/TASK-RF-<TS>/`, using template 01 (generic) or 02 (complex) per the `TEMPLATE:` field. Its QA/Validation/Testing encoding logic is concentrated in lines 336-378: `QA_GATE_REQUIREMENTS` (NONE/FINAL_ONLY/PER_PHASE), `VALIDATION_REQUIREMENTS` (free-form list), and `TESTING_REQUIREMENTS` (NONE/UNIT/INTEGRATION/E2E/ALL) each map to specific checklist-item shapes enforced as Critical Rules 10/11/12 (`:482-484`). The I16 fix-cycle-limits table at `:352-358` defines per-gate cycle caps (research/report-validation/qualitative=3 with HALT-escalate; synthesis/task-integrity=2 with Open Questions). FR-CONV.5 will introduce two additional retry-monotonicity HALTs (`F_{n+1} >= F_n` and `PASS@N -> FAIL@N+1`) layered into this same region, requiring coordinated edits to both this agent file (to embed the semantics into generated QA items) and the task-builder skill (to construct the BUILD_REQUEST and verify the resulting gates). Incremental file writing (Step 5, `:168-196`) is the dominant operational constraint — the agent's #1 failure mode is one-shotting a large task file.

---

**Status:** Complete
