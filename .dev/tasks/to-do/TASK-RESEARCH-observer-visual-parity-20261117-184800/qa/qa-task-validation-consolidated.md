# Consolidated task-file validation findings (A.10 + A.10.25 + A.10.5), cycle 1

Task file: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/TASK-RESEARCH-observer-visual-parity-20261117-184800.md`

Source reports (all in the same folder under `qa/`): `qa-task-validation-b2-report.md` (FAIL), `qa-task-validation-structure-report.md` (FAIL), `qa-task-research-alignment-report.md` (PASS), `qa-qualitative-operational-report.md` (FAIL), `qa-qualitative-sufficiency-report.md` (FAIL).

## Items Reviewed

| Check | Result |
|---|---|
| B2 self-containment (all but the five cycle-2 fix items) | PASS |
| Phase structure, ordering, DAG, anti-orphaning | PASS (one blocking finding below) |
| Research alignment | PASS |
| Operational correctness | PASS apart from the same cycle-2 fix-item finding |
| QA gate sufficiency (counts 3, 3, 7, 2, 2) | PASS apart from three blocking findings |

## Blocking findings to fix (all fixes go in the task file, in place)

| # | Source | Where | Finding | Required fix |
|---|---|---|---|---|
| C-1 | b2 B-1, operational B-1 | Steps 3.3 (line ~180), 5.9 (~258), 6.6 (~310), 6.7 (~336), 6.8 (~360) | Cycle-2 fix-agent items (`fix_authorization: true`) say "same prompt as Step X" or "as in the cycle-1 fix item above" instead of embedding the prompt. | Write the full fix-agent prompt into each of the five items, with the cycle-2 paths substituted (copy the cycle-1 fix prompt of the same gate: Steps 3.2, 5.8, 6.5, and for Gates 4 and 5 the cycle-1 fix items). Include the role sentence, "fix only blocking findings", create-the-log-first instruction, per-fix log-line contents, and for Gates 1 and 2 the targeted-research and staleness rules. |
| C-2 | structure B-1 | Step 5.6 (synth-06 prompt, ~line 232) | The synth-06 prompt tells the agent to list gaps "not closed by an implementation step" and to exclude questions "answered elsewhere in the plan", but the Phase 5 preamble forbids the synthesis agents from reading each other's output (it cannot read synth-05). | Delete that clause from the prompt. Instead: list every unresolved gap and open question from the research files, the gaps log and the web files (including O-1 and OPEN-1 to OPEN-3 as open owner decisions), with impact and suggested resolution; the assembler's cross-check removes any question the implementation plan already answers. |
| C-3 | sufficiency B-1 | Lines ~178, 256, 308, 334, 358 | The regression halt message is called "byte-exact" but uses a comma where the pinned wire string has an em dash. | Make the five halt strings byte-exact: `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (em dash after `X.Y`). Keep the `[HALT-MONOTONICITY] \|F\|=<n>` string as is. |
| C-4 | sufficiency B-2, structure N-8, alignment N-1 | Gate 4 fidelity agents (Steps ~6.x, lines ~318-322) and Gate 1 evidence check (~line 162) | The fidelity source lists are incomplete and line ~320 claims "the whole source set is covered". Not assigned: the mockup `.ansi`, `.txt`, `.png` files under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/`, the `inputs/current/` renders, `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/merged/FINDINGS.md`, `tests/observe/test_linkoff_screen_reference.py`, `release1_surface.py`, `record_golden.py`, `record_golden_questions.py`, `src/superclaude/cli/observe/parse.py`, `adapter.py`. | Extend the two Gate 4 fidelity agents' assigned source lists so that every file named in research-notes.md EXISTING_FILES and `inputs/` (mockup text and ANSI exports, current renders, FINDINGS.md) is assigned to one of the two agents (split roughly in half), and correct the "whole source set is covered" claim to match. Add the missing files to the Gate 1 evidence-quality spot-check scope as sources the evidence agent may open. |
| C-5 | sufficiency B-3 | Cycle-2 verification items for Gate 4 (~line 338) and Gate 5 (~line 362) | Each spawns two agents under one checkbox; Gates 1 to 3 split the pair. | Split each into two separate `- [ ]` items (one `rf-qa` verification, one `rf-qa-qualitative` verification for Gate 4; the matching pair as in Gate 5's cycle-1 verification), each with its own embedded prompt, output file and completion gate. Renumber nothing that other items reference; use sub-lettering (for example 6.7a, 6.7b) if needed and update references. |

## Notes to fold into the same edit pass (cheap, no new items)

- N-1 (operational): the task file is about 271 KB, over the Read tool's single-read limit. Add one line to the Prerequisites section: the executor reads it with Grep for `^- \[ \]` plus ranged Reads (offset and limit), never a single full Read.
- N-2 (operational): about 80 references say `### Phase N Findings` but the real headings are `### Phase N - <name> Findings`. Add one line to the Task Log section naming the real heading pattern and telling the executor to match by phase number. Do not mass-edit the 80 references.
- N-5 (alignment): add to the synth-05 prompt: every implementation phase of the redesign plan ends with a render gate, a phase may close only when all High and Medium criteria pass, OPEN-1 to OPEN-3 are treated as Medium until the owner rules, and the plan includes a NO_COLOR and ASCII render pass (guard G-1) in the render gate.
- N-4 (alignment): in the Gate 3 crossref-chain lens prompt, add that accepted divergences AD-1 to AD-7 are not fix requests and need no Section 8 step; they should appear in Section 3 (target state, constraints) or Section 4 as accepted divergences.
- N-5/N-6 (operational): in the Gate 1 completeness lens, add that Q1 to Q7 answers may legitimately be partial until the web research and synthesis phases (Q3 and Q6 especially); a gap that web research will close is not blocking at Gate 1. In the Gate 3 evidence-quality lens, add that environment facts proven by a recorded command output need no file:line citation if the command and its output are cited.
- N-9 (operational): add one final item to Phase 7 before the "set status Done" item: run `git add .dev/tasks` is NOT needed to be asserted as done by this task; instead record in the Task Log that `.dev/tasks/` stays staged by the coordinator (project rule), and do not commit.
- N-6 (structure, minor): change "28 test modules" to "28 Python files under tests/observe (22 test_*.py modules)" wherever it appears.

All other notes in the five reports are recorded and need no change.
