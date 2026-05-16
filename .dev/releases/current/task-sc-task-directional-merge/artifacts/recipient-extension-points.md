# Recipient Extension Points — `/task`

**Task:** T01.01 — Enumerate `/task` recipient extension points
**Roadmap Item:** R-001
**Generated:** 2026-05-14

## Source of Truth (R-RULE-10)

The `/task` skill is a single-file skill: `SKILL.md` with no `refs/`, `rules/`,
`templates/`, or `scripts/` subdirectories.

| Side | Path | Status |
|---|---|---|
| `src/` (source of truth) | `src/superclaude/skills/task/SKILL.md` | Canonical — edit here |
| `.claude/` (dev copy) | `.claude/skills/task/SKILL.md` | Byte-identical mirror (verified via `diff`, "IDENTICAL") |

All `file:line` evidence below cites `src/superclaude/skills/task/SKILL.md`.
Because the `.claude/` copy is byte-identical, every line number resolves
identically on both sides; the `.claude/` mirror is not the attach target —
new capability is authored in `src/` then synced via `make sync-dev`.

## The F1 Loop (reference)

The F1 execution loop is `READ → IDENTIFY → EXECUTE → UPDATE → REPEAT`
(`src/superclaude/skills/task/SKILL.md:83-98`). "Disturbs the F1 loop" below
means the extension point sits *inside* one of these five steps or alters loop
control flow. "Adjacent" means it runs between iterations or between phases but
does not change the per-item READ-IDENTIFY-EXECUTE-UPDATE-REPEAT mechanics.
"No disturbance" means it runs before loop entry or after loop exit.

---

## Positive-Space Extension Points

| # | Extension point | Location (`file:line`, side) | Capability shape it can absorb | F1-loop disturbance |
|---|---|---|---|---|
| 1 | **Task File Validation gate** | `src/superclaude/skills/task/SKILL.md:64-73` (`src/`) | Pre-loop well-formedness checks: frontmatter schema validation, checklist-item presence, B2-pattern conformance, Task Log section presence. New schema/lint validators attach here. | None — runs before loop entry. |
| 2 | **First Item Protocol (pre-loop status init)** | `src/superclaude/skills/task/SKILL.md:100-102` (`src/`) | Pre-loop setup actions: status flip to "🟠 Doing", `start_date` set. New session-init / environment-prep capability attaches here. | None — runs before the loop's first iteration. |
| 3 | **Session Resumption** | `src/superclaude/skills/task/SKILL.md:268-283` (`src/`) | Resume-state reconstruction: locate task file, find first unchecked item, read prior outputs. New state-recovery / context-rehydration capability attaches here. | None — runs before loop re-entry. |
| 4 | **F1 EXECUTE item-type dispatch** | `src/superclaude/skills/task/SKILL.md:89-96` (`src/`) | New item-action types. Current set: spawn subagent, read+produce output, edit file, run command, present to user, update frontmatter. A new action verb attaches here. | Disturbs — this *is* the EXECUTE step; any new action type runs inside the loop. |
| 5 | **"ensuring…" clause verification hook** | `src/superclaude/skills/task/SKILL.md:96` (`src/`) | Per-item post-condition / acceptance-criteria checks evaluated before an item is marked complete. New per-item gate logic attaches here. | Disturbs — runs inside EXECUTE prior to UPDATE. |
| 6 | **UPDATE step — Phase Findings logging** | `src/superclaude/skills/task/SKILL.md:97` (`src/`) | Structured per-item output capture / telemetry / notable-output logging to Task Log. New per-item evidence-recording capability attaches here. | Disturbs — this is the UPDATE step of the loop. |
| 7 | **Parallel Agent Spawning — batch detection** | `src/superclaude/skills/task/SKILL.md:119-142` (`src/`) | Batch-identification and partitioning heuristics for independent same-phase subagent items. New parallelization / partitioning-threshold logic attaches here. | Disturbs — alters IDENTIFY and EXECUTE for multi-item batches. |
| 8 | **Error Handling / blocker logging** | `src/superclaude/skills/task/SKILL.md:170-179` (`src/`) | Blocker classification (recoverable vs unrecoverable), recovery strategies, blocker-logging format. New failure-path handling attaches here. | Disturbs — runs inside the EXECUTE failure path and can mark items `- [x]`. |
| 9 | **Incremental Writing Protocol** | `src/superclaude/skills/task/SKILL.md:252-264` (`src/`) | File-write discipline policy: create-header-then-append-sections. New write-safety / chunking policy attaches here. | Adjacent — constrains *how* EXECUTE writes files but does not change loop control flow. |
| 10 | **Phase-Gate QA Verification** | `src/superclaude/skills/task/SKILL.md:182-211` (`src/`) | Between-phase QA: output collection, "ensuring…"-clause extraction as acceptance criteria, rf-qa spawn, fix-cycle loop (max 3), QA-report persistence. New phase-boundary gate logic attaches here. | Adjacent — runs between phases, not inside the per-item loop, but gates loop re-entry into the next phase. |
| 11 | **Post-Completion Validation** | `src/superclaude/skills/task/SKILL.md:213-248` (`src/`) | Final-pass validation after the last phase: rf-qa structural cross-phase check + rf-qa-qualitative operational check. New whole-task validation capability attaches here. | None — runs after the final phase, after the loop has exited. |
| 12 | **Frontmatter Update Protocol (F5)** | `src/superclaude/skills/task/SKILL.md:159-168` (`src/`) | MDTM frontmatter lifecycle slots. Current event→field map: task start, end-of-session, blocked, completion → `status`, `start_date`, `updated_date`, `blocker_reason`, `completion_date`. New lifecycle-state fields/triggers attach here. | None — frontmatter writes are a side-channel to the loop; F4 explicitly permits them. |
| 13 | **Required frontmatter schema slot** | `src/superclaude/skills/task/SKILL.md:69` (`src/`) | Mandatory task-file metadata fields. Current minimum set: `id`, `title`, `status`, `created_date`. New required-metadata fields attach here. | None — consumed at validation time, before loop entry. |
| 14 | **DYNAMIC CONTENT MARKER sections** | `src/superclaude/skills/task/SKILL.md:114, 150, 156` (`src/`) | The *only* sanctioned slot for runtime checklist-item injection — new items may be added inside these marked sections. Self-extending / generative-task capability attaches here. | Disturbs — injected items become new `- [ ]` entries the IDENTIFY step will pick up. |
| 15 | **Subagent dispatcher — type selection** | `src/superclaude/skills/task/SKILL.md:291-299` (`src/`) | The agent-type roster: `general-purpose`, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler`, `rf-task-builder`, `rf-task-researcher`, `Explore`. New agent types attach to this roster. | Disturbs — dispatcher is invoked inside the EXECUTE step. |
| 16 | **Subagent dispatcher — Agent Prompt Handling** | `src/superclaude/skills/task/SKILL.md:301-302` (`src/`) | Prompt pass-through policy (verbatim, no abbreviation). New prompt-transformation / context-injection policy attaches here. | Disturbs — runs inside EXECUTE when spawning. |
| 17 | **Subagent dispatcher — Agent Mode** | `src/superclaude/skills/task/SKILL.md:304-305` (`src/`) | Default subagent permission mode (`bypassPermissions`). New mode-selection policy attaches here. | Disturbs — applied inside EXECUTE at spawn time. |
| 18 | **Subagent dispatcher — Background vs Foreground** | `src/superclaude/skills/task/SKILL.md:307-309` (`src/`) | Execution-scheduling policy for spawned agents. New scheduling / concurrency policy attaches here. | Disturbs — alters EXECUTE-step control flow. |
| 19 | **Subagent dispatcher — Agent Results handling** | `src/superclaude/skills/task/SKILL.md:314-319` (`src/`) | Post-agent processing: read output files, capture PASS/FAIL verdict, mark item `- [x]`, route failures to Error Handling. New verdict-processing / output-verification capability attaches here. | Disturbs — spans the EXECUTE→UPDATE boundary of the loop. |

---

## Negative-Space Rows (where a feature may NOT attach)

These rows define the **prohibited** regions. A donor feature whose attachment
mechanism requires any of the following cannot be merged into `/task` without
violating the loop's integrity guarantees.

| # | Negative-space region | Location (`file:line`, side) | What is forbidden | F1-loop disturbance |
|---|---|---|---|---|
| N1 | **Prohibited Actions (F2)** | `src/superclaude/skills/task/SKILL.md:104-117` (`src/`) | A feature may NOT attach if it: works from memory instead of re-reading the task file; executes multiple items simultaneously (outside the parallel-spawn exception); skips items or reorders them; assumes completion without evidence; invents unverified file paths; rewrites/reinterprets items; adds items outside DYNAMIC CONTENT MARKER sections; delegates a subagent across phase boundaries; skips phase-gate QA; or skips post-completion validation. | Any such feature breaks the loop's three guarantees (progress survives compression, no steps skipped, resumability) — prohibited by construction. |
| N2 | **Task File Modification Restrictions (F4)** | `src/superclaude/skills/task/SKILL.md:144-158` (`src/`) | A feature may NOT mutate the task file beyond: checking off items, updating frontmatter fields, appending to Task Log / Notes, and adding items inside DYNAMIC CONTENT MARKER sections. It may NOT rewrite/rephrase items, add items elsewhere, delete/reorder items, modify the Task Overview / Key Objectives / Variables sections, or change structure/headings. | Features mutating task-file structure corrupt the READ source of truth that the loop depends on. |
| N3 | **F1 loop is non-delegable (Critical Rule 12)** | `src/superclaude/skills/task/SKILL.md:349` (`src/`) | A feature may NOT delegate the READ-IDENTIFY-EXECUTE-UPDATE-REPEAT loop itself to a subagent (e.g., "process items X through Y"). Subagents may only receive a single item or a parallel batch within one phase. | Directly protects the loop: the executor must always own loop control; delegating it dissolves the integrity guarantees. |

---

## Coverage Check (Acceptance Criteria)

- **Pre-loop hooks** — rows 1, 2, 3.
- **Per-item hooks** — rows 4, 5, 6, 7, 8.
- **Phase-gate hooks** — row 10.
- **Post-completion hooks** — row 11.
- **MDTM frontmatter slots** — rows 12, 13.
- **Subagent dispatcher** — rows 15, 16, 17, 18, 19.
- **Prohibited-actions negative space** — rows N1, N2, N3.

Every row cites `file:line` evidence with an explicit `src/` side tag (the
`.claude/` copy is byte-identical, so line numbers resolve on both sides; `src/`
is the authoritative attach target per R-RULE-10). Every row carries an
F1-loop-disturbance assessment.
