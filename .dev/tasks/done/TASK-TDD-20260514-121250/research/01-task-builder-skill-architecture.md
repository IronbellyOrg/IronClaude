# Research: task-builder SKILL.md Architecture

**Status:** Complete
**Date:** 2026-05-14
**Agent type:** Architecture Analyst
**Source:** src/superclaude/skills/task-builder/SKILL.md (1,709 lines)

---

## 1. A.1–A.11 Pipeline Structure

Stage A is the only stage (Stage B does not exist for this skill — SKILL.md:12, 141). The skill is the orchestrator; everything is spawned via the Agent tool with `mode: "bypassPermissions"` (SKILL.md:8, 398).

| Stage | Lines | Purpose | Input | Output |
|---|---|---|---|---|
| **A.1 Check Existing Task Folder** | 169–182 | Resume-point detection by scanning `.dev/tasks/to-do/TASK-RF-*/` for prior artifacts | Filesystem state | Resume point (A.2/A.3/A.5/A.7/A.8/A.9/A.10/A.10.5/A.11) |
| **A.2 Parse & Triage** | 184–237 | Decompose request into GOAL/WHY/OUTPUTS/CONTEXT; choose Scenario A (explicit) vs B (vague); determine track count (1–5, default 1, max 5); select MDTM template 01 vs 02 per track | User prompt | Structured request, track list, per-track template |
| **A.3 Scope Discovery** | 239–305 | Glob/Grep/codebase-retrieval to map files; plan 3–8 researchers per track from 8 topic types (File Inventory, Patterns & Conventions, Integration Points, Doc Cross-Validator, Solution Research, Template & Examples, Data Flow Tracer, Test & Verification) | Triaged request | Per-track scope map; task folder created at `.dev/tasks/to-do/TASK-RF-YYYYMMDD-HHMMSS/{research,qa}/` |
| **A.4 Write Research Notes** | 307–349 | Persist scope discovery to `${TASK_DIR}research-notes.md` with 7 mandatory categories (EXISTING_FILES, PATTERNS_AND_CONVENTIONS, GAPS_AND_QUESTIONS, RECOMMENDED_OUTPUTS, SUGGESTED_PHASES, TEMPLATE_NOTES, AMBIGUITIES_FOR_USER) | Scope map | `research-notes.md` per track |
| **A.5 Review Research Sufficiency (Self-Review Gate)** | 351–373 | Orchestrator self-review of research-notes.md against 7 questions; max 2 gap-fill rounds | `research-notes.md` | Pass → A.6; otherwise self-update or spawn general-purpose researcher |
| **A.6 Template Triage** | 375–391 | Confirm template 01 (simple sequential) vs 02 (discovery + build + verify) per track | Research notes | Final template per track |
| **A.7 Spawn Researchers** | 393–572 | Parallel `general-purpose` Agent calls (all in one message, including multi-track), 3–8 per track. Each writes evidence-based findings to `${TASK_DIR}research/[NN]-[topic-slug].md` incrementally | Scope map | Per-topic research `.md` files |
| **A.8 Research Quality Gate** | 574–654 | Parallel rf-analyst + rf-qa (research-gate mode, `fix_authorization: false`); partition into 2+2 when >6 research files; gap-fill cycle (max 3 rounds, aligned with canonical skills) | Research files | `qa/analyst-completeness-report.md`, `qa/qa-research-gate-report.md`; PASS/FAIL verdict |
| **A.8.5 Optional Web Research** | 656–710 | Skipped unless tier allows web agents AND quality gate flagged external knowledge gaps; spawns 1–2 `general-purpose` web research agents → `${TASK_DIR}research/web-[NN]-[topic].md` | Quality gate gap list | Web research files in same research dir |
| **A.9 Spawn Builder** | 712–870 | Single `rf-task-builder` Agent per track with structured BUILD_REQUEST; mediates 3 return flows: RESEARCH_NEEDED (max 2 rounds), MALFORMED (max 2 rounds, separate counter), NEED_USER_INPUT (documented in Open Questions). Total maximum invocations = 4 (2+2) | BUILD_REQUEST + research dir | `${TASK_DIR}${TASK_ID}.md` |
| **A.10 Task File Structural Validation** | 872–921 | rf-qa with `QA_MODE: task-integrity`, `fix_authorization: true`, 9-item checklist (lines 898–906) | Task file path | `qa/qa-task-validation-report.md`; PASS / FAIL-with-fixes / FAIL-with-unfixable |
| **A.10.5 Task File Qualitative Validation** | 923–1000 | rf-qa-qualitative with `QA_PHASE: task-qualitative`, `fix_authorization: true`; verifies every TARGET_FILE_LIST entry (no spot-checking, line 931); partitions when >15 checklist items via `assigned_phases`; verifies BUILD_REQUEST QA_GATE/VALIDATION/TESTING requirements are encoded | Task file + research dir + project conventions | `qa/qa-qualitative-review.md` |
| **A.11 Present Results** | 1002–1071 | Output formatted result block (single-track or multi-track); reports gate statuses, item count, batch size, execution command `/task <path>` | All artifacts | Terminal summary to user |

## 2. 4-Stage Gate Topology

The skill enforces four sequential adversarial gates plus a self-review gate at A.5. Every gate carries an explicit **ADVERSARIAL STANCE** directive (SKILL.md:621, 878, 895, 929, 958, 1291, 1308, 1386) — "assume the work contains errors."

| Gate | SKILL.md Lines | Agent / Mode | Authorization | Severity Handling | Output File |
|---|---|---|---|---|---|
| **A.5 Self-Review Gate** (orchestrator) | 351–373 | Orchestrator self-review against 7 sufficiency questions | Orchestrator may self-edit or spawn `general-purpose` researcher | Max 2 gap-fill rounds; remaining gaps logged in AMBIGUITIES_FOR_USER | `${TASK_DIR}research-notes.md` |
| **A.8 Research Gate (analyst)** | 574–612, 1238–1284 | `rf-analyst` (completeness-verification), parallel with QA | `fix_authorization` not applicable (read-only completeness check) | 9-item checklist (lines 593–602); PASS/FAIL | `qa/analyst-completeness-report.md` |
| **A.8 Research Gate (QA)** | 614–641, 1286–1341 | `rf-qa` with `QA_MODE: research-gate`, `fix_authorization: false` | No fixes; flags issues only | 10-item checklist (lines 1323–1333); CRITICAL/IMPORTANT/MINOR; ALL must resolve to PASS (lines 645, 1337) | `qa/qa-research-gate-report.md` |
| **A.10 Task Structural Validation** | 872–921, 1381–1401 | `rf-qa` with `QA_MODE: task-integrity`, `fix_authorization: true` | QA fixes in-place via Edit | 9-item checklist (lines 898–906); PASS / FAIL-with-fixes / FAIL-with-unfixable | `qa/qa-task-validation-report.md` |
| **A.10.5 Task Qualitative Validation** | 923–1000 | `rf-qa-qualitative` with `QA_PHASE: task-qualitative`, `fix_authorization: true` | QA fixes in-place via Edit | 15-item Qualitative Review checklist (referenced lines 961–962, lives in agent definition); zero leniency — ALL severity levels must be fixed before A.11 (line 1000) | `qa/qa-qualitative-review.md` |

**Partitioning thresholds:**
- A.8: When >6 research files per track → 2 analyst + 2 QA instances with `assigned_files` subsets (line 643)
- A.10.5: When >15 checklist items → multiple rf-qa-qualitative instances with `assigned_phases` subsets (line 993)
- Orchestrator performs cross-phase synthesis after partition reports merge (line 993)

**Adversarial-stance language** appears explicitly at lines 621, 878 (with duplication at 895), 929 (with duplication at 958), 1283, 1291 (with duplication at 1308), 1340, 1386. Critical Rule #7 declares quality gates mandatory (line 1540).

## 3. rf-task-builder Spawn Contract

The builder is spawned in A.9 (SKILL.md:712–870) and re-documented in the Agent Prompt Templates section (SKILL.md:1343–1402).

**Spawn parameters:**
- `subagent_type: "rf-task-builder"` (line 720)
- `mode: "bypassPermissions"` (line 721)
- One builder per track; multi-track builders all spawned in a single message for parallel execution (line 850)

**Builder return-flow mediation** (lines 852–870):
1. **RESEARCH_NEEDED** — return value starts with `RESEARCH_NEEDED:`; orchestrator spawns a `general-purpose` gap-fill researcher, re-invokes builder with augmented context; max 2 rounds.
2. **MALFORMED** — builder returned a file path but file fails structural validation; orchestrator re-invokes with "fix these issues"; max 2 rounds (independent counter).
3. **NEED_USER_INPUT** — builder cannot pause mid-execution; documents ambiguity in Open Questions and proceeds with most reasonable interpretation.

These are **separate retry counters** — combined max of 4 invocations (line 870). This is reaffirmed in Critical Rule #12 (line 1550).

**Builder consumes** (per BUILD_REQUEST):
- `RESEARCH DIR: ${TASK_DIR}research/` — reads ALL `.md` files (includes `web-*.md` web research per line 710)
- `QUALITY GATE RESULTS` — reads `qa/analyst-completeness-report.md` and `qa/qa-research-gate-report.md`
- MDTM template at `.claude/templates/workflow/0[1|2]_mdtm_template_[generic|complex]_task.md` (lines 838–840)

**Builder produces:**
- Task file at `${TASK_DIR}${TASK_ID}.md` written incrementally (lines 819–835): Write header first, then Edit one phase at a time, then append Task Log.
- Returns the task file path as final output (no SendMessage/TaskCreate/broadcast — line 810).

**Critical Rules binding builder output** (lines 1558–1564):
- Rule #16: QA_GATE_REQUIREMENTS (FINAL_ONLY/PER_PHASE) MUST be encoded as task-file items; omission = MALFORMED.
- Rule #17: VALIDATION_REQUIREMENTS MUST be encoded as validation items placed AFTER the phase they validate; omission when non-empty = MALFORMED.
- Rule #18: TESTING_REQUIREMENTS (non-NONE) MUST be encoded as test items with paths, commands, coverage thresholds; omission = MALFORMED.
- Precedence (line 1564): SKILL PHASES TO ENCODE is authoritative when present; for standalone task-builder (no SKILL PHASES TO ENCODE), QA_GATE_REQUIREMENTS is the sole authority.

## 4. BUILD_REQUEST Template Fields (verbatim, SKILL.md:716–848)

Spawn invocation (line 719):
```
Agent:
  subagent_type: "rf-task-builder"
  mode: "bypassPermissions"
  prompt: |
    BUILD_REQUEST:
    ==============
```

| Field | Line(s) | Verbatim Definition |
|---|---|---|
| `GOAL` | 725 | "what the task file should accomplish when executed" |
| `WHY` | 727 | "context for why this task is needed" |
| `TASK_ID_PREFIX` | 729 | Always `TASK-RF` for this skill |
| `TEMPLATE` | 731–733 | `01` (simple) or `02` (complex requiring discovery, build, test, review phases) |
| `QA_GATE_REQUIREMENTS` | 735–742 | `NONE` / `FINAL_ONLY` (default for 01) / `PER_PHASE` (default for 02). When non-NONE, generated task file MUST include items spawning rf-analyst and/or rf-qa before proceeding. |
| `VALIDATION_REQUIREMENTS` | 744–749 | Validation checklist items (lint, type-check, build, existing tests). Default: "Standard project validation: lint, type-check, and build must pass." |
| `TESTING_REQUIREMENTS` | 751–756 | `NONE` / `UNIT` / `INTEGRATION` / `E2E` / `ALL`. Default inferred from GOAL — implementation defaults to `UNIT`; API changes default to `UNIT + INTEGRATION`. |
| `DOCUMENTATION STALENESS WARNINGS` | 758–767 | List of [CODE-CONTRADICTED]/[UNVERIFIED] claims from Doc Cross-Validator. Builder must NOT base items on contradicted/unverified findings. |
| `RESEARCH DIR` | 768–772 | `${TASK_DIR}research/` — builder reads ALL `.md` files including per-researcher topic file listing |
| `QUALITY GATE RESULTS` | 774–779 | Paths to `qa/analyst-completeness-report.md` and `qa/qa-research-gate-report.md`; gap-fill research listed |
| `OPEN QUESTIONS` | 781–783 | Unresolved ambiguities — document as risks/assumptions, NOT as basis for items |
| `REMAINING GAPS` | 785–786 | Persistent gaps after max gap-fill rounds; document as known limitations |
| `CRITICAL — GRANULARITY REQUIREMENT` | 788–794 | Per A3 + A4 of MDTM template: individual items for every file/component, NEVER batch items |
| Operational guidance block | 796–818 | "TO BUILD A GOOD TASK FILE, YOU NEED" + ESCALATION override + fallback handling for blocked/ambiguous cases |
| `INCREMENTAL TASK FILE WRITING (MANDATORY — NEVER ONE-SHOT)` | 819–833 | Write header (frontmatter + Overview + Objectives + Prerequisites) FIRST, then Edit one phase at a time, then append Task Log section LAST |
| `TASK FILE LOCATION` | 834–835 | `${TASK_DIR}${TASK_ID}.md` |
| `STEPS` (1–7) | 837–848 | Read template → Read PART 1 → Read research files → Follow PART 1 (Sections A–K + optional L) → Note gaps → Create file (incremental) → Return path |

**Per-item schema** (output structure, lines 1452–1457): every checklist item has exactly 5 fields:
- `Context` (what the executor needs to know)
- `Action` (exactly what to do)
- `Output` (what gets created/modified)
- `Verification` (how to confirm)
- `Completion gate` (when item is done)

This is the **self-contained-item invariant** — operational source line 1452–1457 and Critical Rule #14 (line 1554).

## 5. Architecture Patterns for TDD §6

### 5.1 High-Level Architecture Diagram (TDD §6.1)

```
                          User (/task-builder [request])
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │   task-builder SKILL.md (Orchestrator)       │
                │   Stage A only — single-stage pipeline       │
                └──────────────────────────────────────────────┘
                                       │
       ┌───────────────────────────────┼─────────────────────────────────┐
       │ A.1 Resume detect             │ A.2 Parse & triage              │
       │ A.3 Scope discovery           │ A.4 Write research-notes.md     │
       │ A.5 Self-review gate          │ A.6 Template triage             │
       └───────────────────────────────┼─────────────────────────────────┘
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.7 SPAWN N general-purpose researchers     │  ◄── [FR-CONV.2] (Execution Context insertion)
                │  (parallel, single message, 3–8 per track)   │
                │  Topics: File Inventory, Patterns, Integ.,   │
                │  Doc Cross-Val, Solution, Template, Data     │
                │  Flow, Test & Verification                   │
                └──────────────────────────────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.8 RESEARCH GATE (parallel adversarial)    │  ◄── [FR-CONV.6] (DNSP edit site)
                │  rf-analyst  ┃  rf-qa (research-gate)        │
                │  9-item ckl  ┃  10-item ckl, fix_auth=false  │
                │  Partition: 2+2 instances when >6 files      │
                │  Gap-fill cycle: max 3 rounds                │
                └──────────────────────────────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.8.5 OPTIONAL Web Research (1–2 agents)    │
                │  Only if tier ≥ Standard AND ext. gaps       │
                └──────────────────────────────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.9 SPAWN rf-task-builder (per track)       │
                │  Reads BUILD_REQUEST + all research/*.md     │
                │  3 mediation flows:                          │
                │    RESEARCH_NEEDED (max 2)                   │
                │    MALFORMED (max 2, separate counter)       │
                │    NEED_USER_INPUT → Open Questions          │
                │  Total max invocations: 4                    │  ◄── [FR-CONV.5] (Retry monotonicity)
                └──────────────────────────────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.10 STRUCTURAL VALIDATION                  │  ◄── [FR-CONV.1] (9-item checklist insert)
                │  rf-qa (task-integrity, fix_auth=true)       │  ◄── [FR-CONV.6] (DNSP edit site)
                │  9-item ckl (frontmatter, granularity,       │
                │  evidence-based, no [CODE-CONTRADICTED])     │
                └──────────────────────────────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.10.5 QUALITATIVE VALIDATION               │  ◄── [FR-CONV.3] (5-axis overlay site)
                │  rf-qa-qualitative (task-qualitative,        │  ◄── [FR-CONV.4] (overlay anchor line 961)
                │  fix_auth=true)                              │
                │  15-item ckl + TARGET_FILE_LIST (no spot)    │
                │  Partition by assigned_phases when >15 items │
                │  Zero leniency — all severities fixed        │
                └──────────────────────────────────────────────┘
                                       │
                                       ▼
                ┌──────────────────────────────────────────────┐
                │  A.11 PRESENT RESULTS                        │
                │  task file path + gate summary + /task cmd   │
                └──────────────────────────────────────────────┘
```

### 5.2 Component Diagram (TDD §6.2)

Component roles aligned with task spec:

```
┌───────────────────────────────────────────────────────────────────────┐
│                           ORCHESTRATOR                                │
│                  (task-builder/SKILL.md, this skill)                  │
│   Responsibilities: triage, scope, gate evaluation, retry tracking,   │
│   resume detection, multi-track isolation, result presentation        │
└────────────────┬─────────────────────────┬──────────────────┬─────────┘
                 │ spawns                  │ spawns           │ spawns
                 ▼                         ▼                  ▼
       ┌─────────────────────┐   ┌──────────────────┐   ┌─────────────────┐
       │ rf-task-researcher  │   │ rf-task-builder  │   │ rf-analyst      │
       │ (optional scope     │   │ (MDTM emission,  │   │ (4 phases:      │
       │  discovery, A.5     │   │  one per track,  │   │  completeness   │
       │  general-purpose    │   │  consumes        │   │  verification — │
       │  fallback)          │   │  BUILD_REQUEST)  │   │  parallel       │
       │ NOTE: in source,    │   │                  │   │  with rf-qa)    │
       │  researchers run as │   │                  │   │                 │
       │  general-purpose at │   │                  │   │                 │
       │  A.7 (line 398)     │   │                  │   │                 │
       └─────────────────────┘   └──────────────────┘   └─────────────────┘
                                          │                       │
                                          │ validated by          │ parallel
                                          ▼                       ▼
                 ┌──────────────────────────────────┐   ┌─────────────────┐
                 │ rf-qa  (4 phases)                │   │ rf-team-lead    │
                 │  1. research-gate (fix=false)    │   │ (escalation     │
                 │  2. task-integrity (fix=true)    │   │  orchestration  │
                 │  3+4. partition halves when      │   │  — NOT directly │
                 │      >6 research files           │   │  invoked in     │
                 └──────────────────────────────────┘   │  SKILL.md;      │
                          │                             │  reserved for   │
                          ▼                             │  upstream FR    │
                 ┌──────────────────────────────────┐   │  convergence)   │
                 │ rf-qa-qualitative (7 phases inc. │   └─────────────────┘
                 │  task-qualitative)               │
                 │   - 15-item review               │
                 │   - TARGET_FILE_LIST (no spot)   │
                 │   - assigned_phases partition    │
                 │   - cross-phase synthesis        │
                 │   - fix_authorization: true      │
                 └──────────────────────────────────┘
```

**FR insertion-point annotations** are shown inline on the high-level diagram (right margin arrows). In the TDD, each annotation links to the corresponding FR-CONV.x specification.

NOTE — `rf-task-researcher` is listed in the task brief as an optional scope-discovery agent. In current SKILL.md the researchers spawned at A.7 are `general-purpose` agents (line 398), not a dedicated `rf-task-researcher` subagent type. The TDD §6.2 should either rename this component to `general-purpose researcher (task-builder topic)` or note that `rf-task-researcher` is a planned consolidation [UNVERIFIED in current SKILL.md].

## 6. FR Insertion Sites (Cross-Reference)

Each FR-CONV.x has specified SKILL.md insertion/edit anchors from the task brief. Verified line ranges in current SKILL.md:

| FR-ID | Concern | Insertion / Edit Sites in SKILL.md | Verified Content at Site |
|---|---|---|---|
| **FR-CONV.1** | 9-item task-integrity checklist convergence | Lines 897–906 (A.10 checklist) AND lines 1389–1398 (Agent Prompt Templates restatement) | Lines 898–906: 9 numbered checks exactly (YAML, mandatory sections, self-contained items, granularity, evidence-based paths, no contradicted/unverified, open questions, phase deps, item count). Restated lines 1389–1398. |
| **FR-CONV.2** | Execution Context block insertion (researcher/builder prompts) | A.7 researcher template line 411–467 (Agent block opens at 408); Execution Overview line 139–164 (overview anchor at 139); Tier Selection insertion site at 228–237 (template table). The brief points to lines 228–238 and 719 as Execution Context insertion sites. | Line 228 = "Select MDTM template per track" header; line 719 = `Agent:` opening for builder spawn. Both are natural injection points for an Execution Context preamble. |
| **FR-CONV.3** | A.10.5 Task Qualitative + rf-qa-qualitative spawn prompt | Lines 923–1000 (full A.10.5); explicit FR-CONV.3 insertion anchor: line 961 (`Apply the 15-item Task File Qualitative Review checklist`) | Line 961: "Apply the 15-item Task File Qualitative Review checklist from your agent definition." Five-axis overlay must integrate here. |
| **FR-CONV.4** | 5-axis overlay insertion | Line 961 (the same anchor as FR-CONV.3 — the 15-item checklist invocation) | Same as above. The overlay extends the existing 15-item ckl by 5 verification axes. |
| **FR-CONV.5** | Retry monotonicity (combined retry counter visibility) | Line 870 (A.9: "These are SEPARATE retry counters — a builder that returns RESEARCH_NEEDED twice and then produces a malformed file gets 2+2=4 total invocations maximum"); Line 1550 (Critical Rule #12 restatement) | Lines 852–870 enumerate the 3 mediation flows + their independent counters; line 1550 reaffirms in Critical Rules. Both sites must be edited to ensure monotonic semantics. |
| **FR-CONV.6** | DNSP (Documentation Staleness Protocol) emission edit sites | Lines 510–525 (researcher Doc Cross-Validator topic block inside A.7); lines 574–654 (A.8 research gate — verification of DNSP tagging at lines 600, 630); lines 758–767 (A.9 BUILD_REQUEST `DOCUMENTATION STALENESS WARNINGS` field); lines 1142–1156 (Doc Cross-Validator template restatement in Agent Prompt Templates) | Three tags defined: `[CODE-VERIFIED]`, `[CODE-CONTRADICTED]`, `[UNVERIFIED]` (lines 519–521, 1151–1153). Validated at research gate (lines 600, 630). Filtered by builder (lines 764–766). Re-verified at A.10 ckl item #6 (line 903). |

**Additional FR-CONV.6 anchor** the task brief lists "574–654 DNSP emission edit sites" — this corresponds to the A.8 quality-gate section where DNSP-tagged claims are validated. Line 600 (analyst ckl item 7) and line 630 (QA ckl item 3) verify proper [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED] tagging.

## 7. Gaps and Questions

1. **rf-task-researcher vs general-purpose** — The task brief mentions `rf-task-researcher` as a component, but SKILL.md spawns researchers as `subagent_type: "general-purpose"` (line 398, 1080). It is unclear whether the TDD should introduce a new subagent type or document the current general-purpose usage. [UNVERIFIED in SKILL.md]
2. **rf-team-lead role** — The task brief lists `rf-team-lead` as the escalation orchestrator in the §6.2 component diagram, but SKILL.md contains no reference to `rf-team-lead` (verified via search of all 1,709 lines — only `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, and `rf-task-builder` are spawned). Critical Rule #13 explicitly forbids team infrastructure (line 1552). [UNVERIFIED — likely a convergence target, not current code]
3. **rf-qa "4 phases" framing** — SKILL.md describes rf-qa with 2 distinct modes (`research-gate`, `task-integrity`). The "4 phases" framing in the task brief may include the partitioned instances (2 instances per mode when partitioning triggers, totaling 4). [UNVERIFIED — needs alignment with rf-qa agent definition]
4. **rf-qa-qualitative "7 phases including task-qualitative"** — SKILL.md invokes rf-qa-qualitative with `QA_PHASE: task-qualitative` (line 935) but does not enumerate the other 6 phases. They are presumably defined in the rf-qa-qualitative agent definition file at `.claude/agents/rf-qa-qualitative.md`. [UNVERIFIED in SKILL.md]
5. **5-axis overlay specification** — FR-CONV.4 references a "5-axis overlay" extending the 15-item checklist. The specific 5 axes are not defined in SKILL.md and must be sourced from the FR-CONV.4 specification document.
6. **"Combined retry counter" semantics** — FR-CONV.5 calls for "retry monotonicity." SKILL.md establishes two SEPARATE counters (line 852–870) with combined max of 4. Whether FR-CONV.5 keeps separation or unifies counters is a TDD design decision.
7. **Maximum gap-fill rounds discrepancy** — A.5 self-review gate sets max 2 gap-fill rounds (line 371); A.8 research gate sets max 3 gap-fill rounds (line 651). Both are intentional but worth flagging in TDD as distinct controls.
8. **Open Questions handling for NEED_USER_INPUT** — Line 868 describes documenting ambiguities in Open Questions; no automated user-prompt loop. The TDD should clarify whether the convergence FRs preserve fire-and-forget semantics or introduce a synchronous user step.

## 8. Stale Documentation Found

Per DNSP, every doc claim is tagged.

| Claim | Source | Status |
|---|---|---|
| "rf-task-builder is the standard builder subagent for canonical document skills" (line 82) | SKILL.md:80–82 | [CODE-VERIFIED] — confirmed agent definition file referenced at `.claude/agents/rf-task-builder.md` |
| "Max 3 gap-fill rounds aligned with canonical skills and rf-qa agent definition" (line 651) | SKILL.md:651 | [UNVERIFIED] — rf-qa agent definition not read in this research; alignment claim depends on `.claude/agents/rf-qa.md` |
| "15-item Task File Qualitative Review checklist from your agent definition" (line 961) | SKILL.md:961 | [UNVERIFIED] — checklist content lives in rf-qa-qualitative agent definition, not SKILL.md |
| "Combined max invocations = 4" (line 870) | SKILL.md:870 + restated at 1550 | [CODE-VERIFIED] — both anchor sites consistent |
| "Task file Validation Checklist has 15 items" (lines 1491–1507) | SKILL.md:1491–1507 | [CODE-VERIFIED] — counted exactly 15 checkboxes in the section |
| "QA agent (A.10) validates against these criteria" (line 1491) — but A.10 lists a 9-item ckl while §"Task File Validation Checklist" lists 15 | SKILL.md:898–906 vs 1493–1507 | [CODE-CONTRADICTED] — A.10 ckl has 9 items (frontmatter, sections, self-contained, granularity, evidence, contradicted/unverified, open questions, phase deps, item count). The "Task File Validation Checklist" header at 1491 lists 15 items including different elements (nested checkboxes, agent prompts embedded, parallel spawning instructions, partitioning guidance, anti-orphaning). These are two DIFFERENT checklists with overlapping but non-identical content. TDD must reconcile or document both. |
| "A.10.5 catches operational issues that structural QA cannot" (line 925) | SKILL.md:925 | [CODE-VERIFIED] — A.10.5 explicitly verifies BUILD_REQUEST QA_GATE/VALIDATION/TESTING encoding (lines 972–976) plus TARGET_FILE_LIST traversal (line 931) |
| `.claude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` (lines 543–544) | SKILL.md:543–544 | [UNVERIFIED] — paths referenced; existence not confirmed in this research session |
| "rf-task-researcher" / "rf-team-lead" in TDD component diagram (per task brief) | Task brief §5 | [CODE-CONTRADICTED] — neither symbol appears in SKILL.md 1,709 lines; only `general-purpose` researchers and the 4 named agents (rf-analyst, rf-qa, rf-qa-qualitative, rf-task-builder) are spawned |

## 9. Summary

The task-builder skill is a single-stage (Stage A) orchestrator that produces validated MDTM task files via a 4-gate adversarial pipeline: research gate (A.8, rf-analyst + rf-qa in parallel), structural validation (A.10, rf-qa task-integrity mode with fix authorization), qualitative validation (A.10.5, rf-qa-qualitative with TARGET_FILE_LIST no-spot-check discipline), and an orchestrator self-review gate (A.5). All subagents are spawned via the Agent tool with `bypassPermissions` — there is NO team infrastructure (Critical Rule #13), and every agent receives explicit ESCALATION blocks overriding their team-based defaults. The builder is spawned with a structured BUILD_REQUEST containing 15 fields, mediated through 3 return flows (RESEARCH_NEEDED, MALFORMED, NEED_USER_INPUT) with two independent retry counters totaling max 4 invocations. The six FR-CONV insertion sites are anchored at specific line ranges with verifiable content: FR-CONV.1 at 897–906 + 1389–1398, FR-CONV.2 at 228–237 + 719, FR-CONV.3 throughout 923–1000, FR-CONV.4 at line 961, FR-CONV.5 at 870 + 1550, FR-CONV.6 spanning A.7 (510–525), A.8 (600, 630), A.9 (758–767), and A.10 (903). One material contradiction was detected: A.10's 9-item structural checklist and the document's standalone "Task File Validation Checklist" at lines 1491–1507 list 15 items with different content — the TDD must reconcile these or document both as separate gates.

---

**Status:** Complete






