# Task structural validation dispatch

## Governing source and purpose
Source: actual installed `/home/coder/.claude/skills/task-builder/SKILL.md`, A.10 Task File Validation. The parent consumed all 565 lines of the authored task; no independent validation is claimed. Launch TWO fresh report-only rf-qa reviewers concurrently through the coordinator, not native Agent or nested workers. Actual task-builder and tech-research are already active: do not reactivate them. This brief binds the actual A.10 prompt below; it does not replace the governing role or Template 02.

TASK_DIR: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`
TASK FILE: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md`
TEMPLATE USED: 02
TRACK GOAL: Investigate issue 463 model-plus-effort routing feasibility through deep local research, public candidate/alternatives/Jev and official client/provider contracts, synthesis and independently reviewed report. Preserve explicit choices and configured Coder-role default, no selected router architecture and no implementation.
RESEARCH DIR: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/research/`

## Shared worker contract
Coordinator-owned verified `claude-gw-tier1b` only, with actual recorded backend membership in live Tier1b slots verified, not alias/profile or launch receipt alone. No Opus/Tier1a, fallback, native/nested helpers, installed agent/global settings edits. Resolve rf-qa project `.claude/agents/rf-qa.md` first, installed `/home/coder/.claude/agents/rf-qa.md` fallback. Read the role and applicable full Template 02 (`.claude/templates/workflow/02_mdtm_template_complex_task.md`, installed `/home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md` fallback); missing required source blocks. Do not edit these definitions.

Each reviewer owns ONLY its separate report. Before evidence gathering, Read the role's actual Output Format (All Phases), immediately Write full header/section/table skeleton with explicit placeholders, then populate section by section with Edit. Preserve Overall Verdict, Items Reviewed, Summary, Issues Found, Actions Taken, Recommendations, QA Complete, confidence evidence and active Self-Audit when zero findings. Also emit the mandatory case-sensitive anchored `VERDICT: PASS` or `VERDICT: FAIL`. Binary verdict only. Critical/Important actual defects block; cosmetic/wording/format/citation-style/minor notes do not fail or trigger fixes. Do not invent five defects to meet a quota. No producer self-review or construction-gate PASS substitutes for current task review.

Read the full task and BUILD-REQUEST, research inputs and other governing sources as needed. Review source-authored assertions, do not accept builder narratives as proof. Every Read requests fewer than 100 lines and each tool output fewer than 40 lines; use 38-line chunks or smaller and bounded search output. No package/Python/UV commands, tests, requests, paid calls, installs, source/test/config edits, cleanup, commits/push/PR/merge, Slack or unrelated GitHub writes, or SuperClaude-Org interaction. Preserve all intermediates and scope03's prior accidental UV-created .venv/build/27-dependency installation disclosure; do not repeat or clean it up or claim this overall run installation-free. Research execution Tier1b is not a product default. Parent owns staging `.dev/tasks`; never stage `.dev/issues` or `.claude` mirrors.

The source's standalone/no-team-context text prohibits native SendMessage/TaskCreate/TaskUpdate/TaskList broadcasts, not mandatory Orca lifecycle heartbeats/checks/acks/final result. Use the real supervised worker contract. Return actual report path and verdict only after writing; no task execution, fixes, additional helpers or TASK_FILE_READY certification. Unavailable source or model verification is an exact blocker sent to coordinator, never silent fallback.

## Reviewer 1: B2 self-containment
QA_MODE: task-integrity
LENS: b2-self-containment
fix_authorization: false
TASK FILE, TEMPLATE USED, TRACK GOAL, RESEARCH DIR: exact bindings above.

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList. You are a standalone agent invoked via the Agent tool. Return your verdict and report file path as your final output.

**ADVERSARIAL STANCE:** Assume the work contains errors. Find at least 5 issues — a verdict of 0 issues requires extraordinary evidence you thoroughly checked.

YOUR LENS FOCUS: Verify every checklist item is SELF-CONTAINED per MDTM B2. An item must have context + action + output + verification + completion gate. An item that says "see above" or "continue from previous" FAILS.

B2 Self-Containment Checklist:
1. Every checklist item has all 5 B2 components?
2. No item references context from a prior item without restating it?
3. Agent-spawning items have fully embedded prompts (not "see SKILL.md")?
4. File paths in items are specific (not "the relevant file")?
5. Verification criteria are measurable (not "verify it works")?
6. No batch items ("process all X") — each file/component has its own item?
7. No items based on [CODE-CONTRADICTED] or [UNVERIFIED] findings?

OUTPUT FILE: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/qa-task-validation-b2-report.md`
Write the file IMMEDIATELY with a header, then append findings incrementally. Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.

Apply the shared contract, actual role/template and evidence-based confidence protocol. Evaluating an explicitly unresolved research question is not automatically asserting its answer as verified; identify the actual false dependency or missing self-containment if present. Do not dilute genuine omissions.

## Reviewer 2: Phase structure and ordering
QA_MODE: task-integrity
LENS: phase-structure
fix_authorization: false
TASK FILE, TEMPLATE USED, TRACK GOAL, RESEARCH DIR: exact bindings above.

ESCALATION — CRITICAL OVERRIDE:
You have NO team context. Do NOT use SendMessage, TaskCreate, TaskUpdate, or TaskList. You are a standalone agent invoked via the Agent tool. Return your verdict and report file path as your final output.

**ADVERSARIAL STANCE:** Assume the work contains errors. Find at least 5 issues — a verdict of 0 issues requires extraordinary evidence you thoroughly checked.

YOUR LENS FOCUS: Verify task file STRUCTURE and PHASE ORDERING.

Phase Structure Checklist:
1. YAML frontmatter complete and well-formed?
2. All mandatory sections present per template?
3. Phase dependencies are logical (no circular or missing dependencies)?
4. Phase ordering follows logical progression (research before build, build before test)?
5. Task completion items inside final phase (anti-orphaning)?
6. Task Log section present at bottom?
7. Estimated item count is reasonable for the scope?
8. Open Questions and remaining gaps documented (if any)?
9. QA gate items in the task file follow MDTM M3 (lens-based QA sequence) and M4 (source fidelity gate) patterns? (If MDTM template has been updated with these patterns, verify compliance.)

Structural Gate Additions (imported from sc:tasklist 17-point pre-write gate per CB-3 per-check classification, see actual rf-qa agent definition for full rationale):
10. TB-Add-1: Placeholder scan: no item contains `TBD`/`TODO`/`FIXME` and no item is title-only (5-field schema enforced).
11. TB-Add-3: Clarification adjacency: each blocked item references its blocking Open Question by index in Context.
12. TB-Add-4: Circular dependency detection: item-to-item dependencies form a DAG; no cycles.
13. TB-Add-5: Granularity / XL splitting: items flagged complex/multi-file are either split into subtasks or carry a justifying comment.
14. TB-Add-6: Confidence/Verification format consistency: uniform `Verify: ...` prefix and `- [x]` Acceptance Criteria form.
15. TB-Add-7: Execution Context source areas reappear in items: every "Source areas:" entry in the `## Execution Context` block reappears in at least one item's Context field; the block itself contains NO specific file:line references. INACTIVE if no Execution Context block exists.
16. TB-Add-8: Per-item Context evidence binding: every item Context field that references a code surface includes a file:line citation OR an `<!-- evidence-absence: ... -->` justified-absence comment. Structurally proves PR-01's "no specific paths" rule is confined to the header (INV-015 scope-confinement).

OUTPUT FILE: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/qa-task-validation-structure-report.md`
Write the file IMMEDIATELY with a header, then append findings incrementally. Conclude with: VERDICT: PASS or FAIL, and severity-rated issues if FAIL.

Read/re-enumerate the LIVE project-first rf-qa Structural Gate Additions region before review, do not assume this copied enumeration is exhaustive. Apply its full rationale and stated degraded/inactive tolerances. Persist individually named TB-Add results with exact evidence in Items Reviewed so subsequent consumers can inherit the structural verdict without substituting for semantic review. Distinguish genuine missing evidence/actionability from cosmetic field formatting under owner severity rules. Unsigned PRE fields are pending parent gate, not fabricated signoff; verify spec resolution against actual builder input rules rather than accepting builder choice blindly.

## Return and acceptance
Two independent report artifacts are required. Parent reads both fully, verifies anchored verdicts and full lens coverage, then creates the actual template-governed `qa/qa-task-validation-consolidated.md` with Items Reviewed and deduplicated blockers/separate minor notes. Only one serialized authorized writer may fix consolidated blockers, followed by independent verification, maximum two fix-verify cycles. Missing/malformed report is failure under A.10, never permission to progress. No self-certification or producer summary substitutes for artifacts. Research-alignment, qualitative and actual PRE gates remain later mandatory work; task execution is prohibited until actual readiness. Coordinator must provide each actual dispatch/task identifier and backend-membership evidence, including the completed task builder if not yet supplied.
