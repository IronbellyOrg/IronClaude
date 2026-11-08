# QA Report: Task-Research Alignment

**Lens:** task-research-alignment (QA_MODE: task-integrity)
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/TASK-RESEARCH-issue-watcher-20261107-064950.md
**Research notes:** .../research/research-notes.md (+ ADDENDUM 1, ADDENDUM 2)
**Date:** 2026-11-07
**Stance:** adversarial (assume dropped or misrepresented findings)

---

## Method

Read in full: the task file (all 7 phases, Task Log, Deviations), `research/research-notes.md` (scope, SUGGESTED_PHASES, RECOMMENDED_OUTPUTS, ADDENDUM 1, ADDENDUM 2), BUILD-REQUEST.md, `.dev/issues/331/issue-summary.md`, `.dev/issues/331/accuracy-check.md`, `.dev/issues/331/analysis/analyze-sc-issue-protocol.md`, and `.dev/brainstorms/.../enrichment/codebase-context.md`.

Checks run:
- Mapped every research-notes assignment, RECOMMENDED_OUTPUT, SOLUTION_RESEARCH item and addendum point to a task item (table below).
- Path and line-anchor spot-check: 31 cited paths tested with `test -e`, plus about 40 cited line anchors re-read (Makefile 13/48/53/109/166, main.py 521/561, WORKER-CONTRACT 23/39, workflow triggers, issue.md 8/15/24/45-51/68/71/79, SKILL 70-72/82-85, ccsession README 21/228-234, core CLAUDE.md 45-53, design doc 6-10/23/41/52, job-identity header).
- Compared the evidence files' findings (analysis F1-F9, accuracy rows 1-10, issue-summary cheatsheet) against the questions and prompts in the task.

Result of the fabrication check: no fabricated path. 30 of 31 cited paths exist; the one that does not, `launch-level-guard.sh`, is cited in the task only as a thing the agent must test, which is correct. All spot-checked line anchors match.

---

## Findings (blocking: CRITICAL / IMPORTANT)

### I-1 (IMPORTANT): The "intended owner" routing filter of option A is dropped from every assignment

- **Evidence source:** `analysis/analyze-sc-issue-protocol.md` option A row (line 46) lists the poller's filters as "label, approval, Project, Backlog, **intended owner**"; finding F3 (line 34) says "Routing must pick the workspace whose `gh` login should own the issue. A pull model gets this for free **if each workspace only takes issues meant for its own login**"; `accuracy-check.md` row 8 says the mapping must route an issue to the workspace whose `gh` login is meant to own it.
- **Task file:** the filter is defined as four things everywhere it is defined. web-01 question 9 (line 227): "tagged, human-approved, in a Project, Status Backlog". synth-04 selection logic (line 245): "tagged, human-approved, in the Project, Status Backlog". Agent 01 question 2 (line 185) asks only what claim does when the issue is *already* assigned to someone else, not how a workspace decides an issue is meant for it. A grep of the task file for "intended owner" and "intended developer" returns nothing.
- **Why it matters:** the issue's core promise is "the right developer's workspace". Under the owner-decided option A, with no router, the only routing mechanism is the filter each poller applies. Without a fifth filter, every workspace's poller sees the same approved Backlog issue and they race; claim's "refuse if assigned to someone else" becomes the arbiter by accident. The requirement-scoring row "session starts in the right developer's workspace" (line 243) will therefore have no researched mechanism to cite for A.
- **Proposed fix:** add "which login is intended to own the issue (pre-assignee, Project owner/assignee field, or per-developer label) and how a poller reads it" to web-01 question 9 and to agent 01 question 2; add "intended-owner filter" to the synth-04 selection-logic list (line 245); require it to appear in Section 9 as an open detail if the addenda do not settle it.

### I-2 (IMPORTANT): A blocking "no 'no inbound endpoint' constraint" rule is enforced in the gates but is not in the research notes and contradicts them

- **Research notes:** SOLUTION_RESEARCH, line 46: options are to be assessed "for fit with the constraints **'no inbound endpoint if avoidable**, no live deployment from this repo, claim assigns to the `gh` login that runs it'". Neither addendum withdraws or reverses this; ADDENDUM 2 in fact describes option A as "no listener, no inbound port, no address registry".
- **Task file:** Key Constraints line 139 states inbound exposure "is not a Target State pre-filter"; synth-02 (line 241) forbids listing "no inbound endpoint" as a Target State constraint; and the literal phrase "no inbound endpoint" is a **blocking** conformance check in the Gate 2 analyst and structure prompts (lines 249, 251), the assembler (line 275 rule 8) and the validation checklist item 19 (line 277); line 140 extends the "conformance check" to Gates 2 to 5. The rule's origin is a prior QA round (`qa/qa-fix-log.md` item I-3, from `qa-task-validation-consolidated.md` I-2), written when ADDENDUM 1's "do not favor A" was in force. ADDENDUM 2 superseded that reason.
- **Why it matters:** the task now inverts a constraint that the research notes state, without a Deviations entry (lines 446-458 record the two addenda but not the override of line 46). A synthesis agent that follows the research notes faithfully will include the constraint and be failed by the Gate 2 and validation checks; one that follows the task file contradicts the notes the same gates cite as binding. This is an ungrounded blocking criterion.
- **Proposed fix:** either (a) record the override of research-notes line 46 in the Deviations section with its reason (fair scoring of B and C), and soften the gate wording to "inbound exposure is scored as a criterion, not used to exclude B or C", which keeps the intent and removes the false-fail risk; or (b) drop the prohibition now that ADDENDUM 2 has settled the architecture.

### I-3 (IMPORTANT): The `ci.py` caveat is routed to verification, but the assignment presupposes a wrapper exists, and nothing corrects the sibling enrichment file that repeats the false claim

- **Research notes** (EXISTING_FILES row for `pr_submit/ci.py`, PATTERNS_AND_CONVENTIONS line 37) call `ci.py` an existing "`gh` subprocess wrapper pattern (mockable)". The task correctly flags this as unverified (Deviations line 447; agent 02 question 3, line 187; Gate 1 re-check (a), line 201; Gate 4 agent 2 item 4, line 317).
- **What I verified:** `src/superclaude/pr_submit/ci.py` lines 1-15 import only `re`, `.classifier` and `.models`; its docstring says it is "Pure ... Does not import or name any version-control command tokens". A recursive grep for `subprocess` in `src/superclaude/pr_submit` returns nothing, and no Python file under `src/superclaude` builds a `["gh", ...]` call. So the research-notes claim is CODE-CONTRADICTED and there is no existing `gh` wrapper to reuse.
- **Gap 1, premise leakage:** agent 02 is told to search "the rest of `src/superclaude/pr_submit/` to find where `gh` is actually invoked through subprocess" and, if the claim is wrong, to "report the real wrapper location" (line 187). Both presuppose a wrapper exists. An agent trying to comply can name a wrong location. The prompt should allow, and expect, "no such wrapper exists; the `gh` runner is new code", and should widen the search to the whole of `src/superclaude` and `tests/`.
- **Gap 2, downstream correction:** `enrichment/codebase-context.md` line 21 states the same false claim ("GitHub is reached through the `gh` CLI via `subprocess` (as in `src/superclaude/pr_submit/ci.py`)") and the brainstorm reads that file next to `research-deep.md`. Step 7.2 (line 353) does not require the condensed copy to list corrections to the earlier enrichment, and no item flags the file as superseded.
- **Proposed fix:** reword question 3 of agent 02 as above; add to the Step 7.2 section list "Corrections to `enrichment/codebase-context.md`" (at minimum the ci.py claim, if Gate 1 confirms it); add the same line to Step 7.1's presentation summary.

### I-4 (IMPORTANT): The alternative session-entry findings (`orca orchestration send`, typing into the coordinator session) and the Orca launch contract are not assigned to any agent

- **Evidence source:** `accuracy-check.md` row 7 names `orchestration send` ("durable but pull-only", `.dev/orca-command-refactor/inventory/orca-capabilities.md:66`) as the other nearest local entry point beside `agent launch`; analysis F4 (line 35) records the design trade-off "typing into a live session competes with a person using it; a new session per issue is simpler and isolates failures".
- **Task file:** agent 01 question 6 (line 185) enumerates three entry points only (`orca agent launch` with `--surface terminal`, `ccsession-orca`, plain `claude`). A grep for `orchestration send`, `orca-capabilities` and "coordinator session" returns nothing (the only hit class is the generic word "orchestrator"). `.dev/orca-command-refactor/inventory/orca-capabilities.md` exists but is in no file list. No agent is told to establish the argument contract of `orca agent launch` (how the prompt is passed, how the worktree is chosen, exit status or JSON output) which the plan's "injectable `orca agent launch` function" (line 245) has to mock; the only Python mention of orca under `src/superclaude` is `cli/install_user_setup.py`, so there is no existing call to copy.
- **Why it matters:** session launch is one of the three questions of issue #331. The owner chose `orca agent launch`; the report should say why the other entry points lose. The mock in the plan needs a documented contract or an explicit UNVERIFIED mark.
- **Proposed fix:** add `.dev/orca-command-refactor/inventory/orca-capabilities.md` to agent 01's file list; extend question 6 with "`orca orchestration send` into a live coordinator session versus a new session per issue, and the argument contract of `agent launch` (prompt, worktree, surface, output)", tagging anything not shown in a file as UNVERIFIED so it reaches Section 9.

---

## Minor findings (notes, non-blocking)

| # | Note |
|---|---|
| M-1 | Analysis F5 (`origin_repo.py` rejects foreign repos, so a poller needs a repo-to-checkout map; `orca agent launch` needs "an existing worktree", `ccsession-tag/README.md:231-235`) is only partly carried: agent 01 question 4 mentions the `origin` remote, but the synth-04 element list (line 245) has no "which checkout or worktree the launch runs in" step. Add it as a plan step or an open detail. |
| M-2 | Step 7.2 (line 353) still asks the condensed Recommendation to state "the claim-only versus full-pipeline position". D2 is closed by ADDENDUM 2; reword to "claim-only, decided by the owner". |
| M-3 | Task-file additions not named in the research notes: OpenHands resolver, the "lethal trifecta" framing, the `anthropics/claude-code-action` slug and `coder_script` `cron`/`run_on_start` (web-02, line 229). Each sits inside an assigned topic and carries "verify before naming" or a source requirement, so this is scope colour rather than fabrication. |
| M-4 | Web research (web-01, web-02) has no pre-synthesis gate: Gate 1 excludes it explicitly (line 199). The GitHub schedule and token claims are re-fetched only at Gate 3 domain-accuracy (line 291, at least 5 URLs) and Gate 4 agent 2 (line 317, at least 6 URLs), after synthesis. Acceptable for standard intensity, but an error found there costs a synthesis rewrite. |
| M-5 | ADDENDUM 1 point 2 names Coder#477's candidate integration points (`templates/VSCode-AIDev02/...`, `orca-upstream-monitor.yml`) and prior art (closed #195). They are embedded in the prompts but no item requires them to appear in the report's B/C documentation. |
| M-6 | `issue-summary.md` row for ClickUp (`docs/user-guide/commands.md:380-386`): a launched session needs `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` or the step is skipped. Agent 01 question 4 asks about ClickUp variables, but `docs/user-guide/commands.md` is not in its file list and no plan step covers environment pass-through for a poller-launched session. |
| M-7 | `accuracy-check.md` row 6 and `issue-summary.md` say the existence, owner and Status field of the GitHub Project were never checked. web-01 covers token access but nothing carries "Project owner/number/status-field name are unknown" as a named open detail. The generic "details the addenda leave open" clause in synth-03/04 may catch it; it is not guaranteed to. |
| M-8 | Hybrid D (Action writes a ready label or Project field; workspaces poll) depends on write access. web-01 question 4 asks only whether `GITHUB_TOKEN` can *read* an org Project. |

---

## Cross-checks that passed

- **Assignments:** all 3 codebase agents, 2 web agents, 4 synthesis files and all 11 RECOMMENDED_OUTPUTS have an item (Phase 2 lines 185-189; Phase 4 lines 227-229; Phase 5 lines 239-245; Phase 6 line 275 and Phase 7 line 353).
- **Phase dependencies:** Phase 2 -> Gate 1 -> `gaps-and-questions.md` (line 221) -> web agents that read it (lines 227-229) -> synth-01/02/03 -> synth-04 after synth-03 (line 237) -> Gate 2 -> single assembler -> Gates 3-5 -> condensed copy. The ordering matches the dependencies in the notes and the deviation is recorded (line 449).
- **Caveats in verification criteria:** `ci.py` (agent 02 q3, Gate 1 re-check (a), Gate 4 agent 2); no `schedule:` trigger (agent 02 q1, Gate 1 re-check (b)); `launch-level-guard.sh` (agent 03 prompt, Gate 1 re-check (d)); `--claim --pipeline` design-only and never-as-worker (agents 01 and 03, Gates 1, 3, 4); UNVERIFIED/CODE-CONTRADICTED routing (every research prompt, inventory in Step 4.2, Section 9 requirement in synth-04); GitHub cron limits and the Projects v2 token question (web-01 questions 1, 3-6, 9; Gate 3 domain-accuracy item c; Gate 4 agent 2 item 2); headless slash-command support marked UNVERIFIED if the docs are silent (web-02 question 2, line 229).
- **Addenda:** ADDENDUM 2 is reflected consistently. "pending owner decision" and "do not favor A" appear only inside prohibitions or the quoted supersession sentence; Recommendation = option A "decided by the owner" in synth-03, assembler, checklist 17/19, Step 7.1 and 7.6; B/C/D scored and given revisit conditions; Coder#477 boundary and "A makes it unnecessary unless B or C is revisited" appear in the Execution Context, all four synthesis prompts, the assembler and the gates; the integer-only rule appears in agents 01 and 03 (question 8 and 2), synth-02 gap row, synth-04 validation step and checklist 19.
- **Fabrication:** none found (see Method).

---

## Items Reviewed

| # | Item (research-notes source) | Task-file location | Result |
|---|---|---|---|
| 1 | Agent 01 Code Tracer (claim flow, session launch, files listed) | Step 2.1, line 185 | PASS (see I-4 for dropped entry points) |
| 2 | Agent 02 Integration Mapper (workflows, labels, ci.py, CLI, tests, design-doc format, Makefile) | Step 2.1, line 187 | FAIL for the ci.py premise (I-3), otherwise PASS |
| 3 | Agent 03 Architecture Analyst (launch-level hook, job identity, hooks, never-as-worker) | Step 2.1, line 189 | PASS |
| 4 | web-01 (schedule limits, events, Projects v2, tokens, rate limits, ETag) | Step 4.1, line 227 | FAIL for the owner-filter gap (I-1); otherwise PASS |
| 5 | web-02 (Coder, Claude Code headless and Action, dispatchers, injection, at-most-once, sender auth, app exposure, contract) | Step 4.1, line 229 | PASS |
| 6 | Hybrids (research-notes SOLUTION_RESEARCH item 4) | synth-03 option D, line 243 | PASS (see M-8) |
| 7 | 4 synthesis files mapping and RECOMMENDED_OUTPUTS | Phase 5 lines 239-245 | FAIL for the selection-logic list (I-1) and Target State rule (I-2) |
| 8 | Final report and condensed copy | line 275, line 353 | PASS (see I-3 gap 2, M-2) |
| 9 | Caveat: `ci.py` not verified as subprocess wrapper | lines 187, 201, 317, 447 | FAIL (I-3: verification routed, premise and downstream correction missing) |
| 10 | Caveat: no `schedule:` trigger, `projects_v2_item` org-only "if true" | lines 187, 201, 227 | PASS |
| 11 | Caveat: UNVERIFIED claims routed to Section 9 | lines 239-245, 277 | PASS |
| 12 | Caveat: GitHub cron limits and Projects v2 token question | line 227 (Q1, Q4, Q5, Q9), 291, 317 | PASS |
| 13 | Dependencies reflected in phase ordering | Phases 2-7 | PASS |
| 14 | ADDENDUM 1 points 2-4 (Coder#477, claim-only, integer-only, B/C extra research) | lines 77, 114, 137-141, 229, 241-245 | PASS |
| 15 | ADDENDUM 2 supersedes "keep open" rule | lines 77, 137, 457, all synthesis and gate prompts | PASS for the Recommendation labels; FAIL for the retained rule at line 139 / 241 (I-2) |
| 16 | Evidence files: analysis F1-F9, accuracy rows 1-10 | whole task | FAIL (F3 dropped, F4 and row 7 dropped; F5 partial) |
| 17 | Fabrication check: at least 10 cited paths | 31 paths, about 40 line anchors | PASS |

Totals: 4 IMPORTANT blocking findings (I-1 to I-4), 0 CRITICAL, 8 MINOR notes.

VERDICT: FAIL
