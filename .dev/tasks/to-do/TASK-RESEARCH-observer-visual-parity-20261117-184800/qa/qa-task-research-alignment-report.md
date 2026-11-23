# QA Report: task-integrity, lens task-research-alignment

**Task file:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/TASK-RESEARCH-observer-visual-parity-20261117-184800.md
**Inputs cross-checked:** research-notes.md, BUILD-REQUEST.md, merged/FINDINGS.md
**Date:** 2026-11-17
**Stance:** adversarial; findings graded Blocking or Note

## Method
Read all 475 lines of the task file (about 271 KB, in chunks), research-notes.md, BUILD-REQUEST.md and merged/FINDINGS.md in full. Grepped the notes and build request for skill codes (I22, I16, F2a, C8, CLI_MODE), grepped the skill, and listed the task folder on disk to settle the fabrication check.

## Checklist 1: research assignments (5 codebase, 2 web, 6 synthesis) vs task items

| Notes assignment | Notes output path | Task item | Path matches | Result |
|---|---|---|---|---|
| Agent 1 Code Tracer, render/view/terminal/sanitize | research/01-render-view-terminal-pipeline.md | Step 2.1 | yes | OK |
| Agent 2 Code Tracer, commands/export/collector/questions/keys | research/02-live-screen-commands-export.md | Step 2.2 | yes | OK |
| Agent 3 Code Tracer, tests/goldens | research/03-tests-goldens-fixtures.md | Step 2.3 | yes | OK |
| Agent 4 Doc Analyst, spec/mockups/findings/PR comment | research/04-spec-mockups-and-findings.md | Step 2.4 | yes | OK |
| Agent 5 Integration Mapper, Zellij/harness | research/05-zellij-and-render-harness-environment.md | Step 2.5 | yes | OK |
| W1 Rich composition and colour | research/web-01-rich-composition-and-colour.md | Step 4.1 | yes | OK |
| W2 Zellij and terminal capture | research/web-02-zellij-and-terminal-capture.md | Step 4.2 | yes | OK |
| synth-01 (sections 1, 2) | synthesis/synth-01-problem-current-state.md | Step 5.1 | yes | OK |
| synth-02 (3, 4) | synthesis/synth-02-target-gaps.md | Step 5.2 | yes | OK |
| synth-03 (5) | synthesis/synth-03-external-findings.md | Step 5.3 | yes | OK |
| synth-04 (6, 7) | synthesis/synth-04-options-recommendation.md | Step 5.4 | yes | OK |
| synth-05 (8) | synthesis/synth-05-implementation-plan.md | Step 5.5 | yes | OK |
| synth-06 (9, 10) | synthesis/synth-06-questions-evidence.md | Step 5.6 | yes | OK |
| Final report and gaps log | RESEARCH-REPORT-observer-visual-parity.md, gaps-and-questions.md | Steps 6.1 and 3.4 | yes | OK |

Per-agent file lists, topics and question tags (Q1/Q4/Q7 for agent 1, Q5 for agent 2, Q2/Q7 for agent 3, Q1/Q4/Q7 for agent 4, Q3/Q6 for agent 5) match SUGGESTED_PHASES. W1 and W2 topic lists match the notes (FORCE_COLOR is a harmless addition). Result: no dropped assignment.

## Checklist 2: reachability of Q1-Q7 and finding ids

| Item | Reachable from | Result |
|---|---|---|
| Q1 | Agent 1 (f)(k), W1, synth-04 7.2 | OK |
| Q2 | Agent 3 (e), synth-04, synth-05 | OK |
| Q3 | Agent 5 (c)-(g), W2, synth-04, synth-05 Phase 0 | OK |
| Q4 | Agent 1 (g), Agent 4 (c), W1, synth-04, synth-05 | OK |
| Q5 | Agent 2 (a)-(h), W1, synth-04, synth-05 | OK |
| Q6 | Agent 5 (a)(b), W2, synth-04 | OK |
| Q7 | Agent 1 (wrap/clip), Agent 3 (d), Agent 4, W1, synth-05 | OK |
| M-01..M-18 | Agent 1 (j), Agent 4 (a)(d), synth-02 (one row each), synth-05 mapping table | OK |
| AD-1..AD-7, OPEN-1..3, O-1 | Agent 4 (a), synth-01, synth-02, synth-04 7.3, synth-06, Step 7.2 | OK |
| G-1, G-2 | Agent 1 (g), Agent 4 (a), synth-02 section 3; G-2 also via Q4 | Reachable in research; see N-3 for the plan side |
| O-1 held open, not decided | synth-02, 7.3, Gate 2 qualitative ("honestly left open") | OK |

## Checklist 3: fabrication check
- Every path in the task traces to the notes (EXISTING_FILES, SUGGESTED_PHASES) or the build request. Zellij files, render_current.py, pyproject.toml, Makefile, attachments PNGs, PR comment all appear in the notes.
- Items not in the three inputs: `reviews/` subfolder (exists on disk, created by the build step), CLI_MODE / SPEC_PATH / POST reflect gate (skill-derived), codes I16, I17, I19, I22, F2a, C8 (skill vocabulary; I22 is at SKILL.md lines 115 and 396). None invents a requirement. Two precision problems are in N-2 and N-6.
- Approximate line numbers quoted in agent prompts (render.py ~497, ~524-529, ~365-387; terminal.py ~121; commands.py ~242, ~257) copy the notes and tell the agent to re-verify. Not asserted as fact.

## Checklist 4: constraints in verification clauses
| Constraint | Where verified | Result |
|---|---|---|
| No product code edits | Step 1.2, agent prompts ("do not edit any file other than your output file"), Step 7.1 `git status --short -- src tests` | OK |
| Read-only | Agent 5 (no Zellij session), Step 7.1, Gate 2 qualitative | OK |
| Real data only | Standing-constraints block in every synth prompt; Gate 2 qualitative (line 242) | OK, Gate 2 only |
| Question text screen-only | Agent 2 (e), Gate 3 domain-accuracy (d), Gate 2 qualitative | OK |
| NO_COLOR, ASCII | Agents 1, 2, 3 prompts; synth-04 Q1; Gate 2 qualitative | OK; see N-3 |
| Widths 160/116/80 | Agent 1 (f), Gate 1 qualitative, synth-05 render gate, Gate 3 reproducibility | OK |
| No blinking or mouse | Standing constraints in prompts | OK |
| ANSI-styled output primary mode | Standing constraints, Agent 2 | OK |
| Q7 fixture (64-hex hash + file paths, 80-column wrap or cut) | Agent 3 (d), synth-05 step, synth-04 Q7 | OK |

## Checklist 5: dependency ordering
Phase 2 (independent, parallel) then Gate 1 (reads 01-05 only) then gaps log (3.4) then Phase 4 web agents (read 01, 02, 05 and the gaps log, which exists by then) then Phase 5 synthesis (reads web files and the gaps log) then Gate 2 then assembly then Gate 3 then Gate 4 then Gate 5 then Phase 7. Each gate's fix step precedes the next gate, so later gates see the fixed report. No ordering defect.

## Checklist 6: gate agent counts vs BUILD-REQUEST lines 33-37

| Gate | BUILD-REQUEST | Task | Match |
|---|---|---|---|
| 1 | rf-analyst + rf-qa + rf-qa-qualitative = 3 | Step 3.1: analyst, rf-qa (evidence), rf-qa-qualitative (depth) | yes |
| 2 | rf-analyst + rf-qa + rf-qa-qualitative = 3 | Step 5.7: analyst (accuracy), rf-qa (structure), rf-qa-qualitative (coherence) | yes |
| 3 | 3 rf-qa (template-conformance, internal-consistency, evidence-quality) + 3 rf-qa-qualitative (actionability, domain-accuracy, crossref-chain) + 1 lens (finding-reproducibility) = 7 | Steps 6.2, 6.3, 6.4: same three, same three, same one | yes |
| 4 | 2 rf-qa fidelity | Step 6.7: fidelity-agent-1 and -2, both rf-qa | yes |
| 5 | 2 rf-analyst anti-omission, mandatory | Step 6.8: two rf-analyst, input files split so all 7 research files, gaps log and 6 synth files are covered | yes |
| All | max 2 fix cycles, serialized fix | cycle 1 and conditional cycle 2 with halt guards per gate | yes |

## Findings
No blocking findings. Notes below.

| # | Grade | Location | Finding and evidence | Suggested fix |
|---|---|---|---|---|
| N-1 | Note | Task lines 134-152, 160, 162 vs notes line 28 | The notes list `parse.py` (835 lines) and `adapter.py` (512 lines) in EXISTING_FILES as context only, and no agent is assigned them. Gate 1 checklist item 1 (line 160) and the rf-qa item 3 (line 162) test that every EXISTING_FILES entry is covered, so a gate agent may raise a spurious coverage gap. | Add one line to the Gate 1 prompts saying parse.py and adapter.py are out of scope by design, or add them to Agent 2 as context reads. |
| N-2 | Note | Task line 413 (Builder Notes) | States the BUILD_REQUEST says the I22 standard reductions are intentional. BUILD-REQUEST.md does not mention I22 or "intentional"; it only fixes the counts (lines 33-37). I22 is a skill rule (SKILL.md lines 115, 396). The counts themselves are correct. | Reword as "the counts fixed in the BUILD_REQUEST follow the skill's I22 standard reductions". |
| N-3 | Note | Task line 228 (Step 5.5), line 290 (Gate 3 crossref) | Guard G-1 (new panes emit `+ - \|` under `--ascii`, never `?`) has no explicit home in the synth-05 instructions. The render gate there is defined only by widths 160/116/80 (as the build request WHY states), with no NO_COLOR or ASCII render in the rubric. The crossref lens will then look for a Section 8 step for G-1 and may fail it. Constraint checks on the final report sit only in Gate 2 qualitative, not in any Gate 3 lens. | Tell synth-05 to add G-1 and G-2 acceptance steps and a NO_COLOR and ASCII render pass to each phase rubric. |
| N-4 | Note | Task line 290 (crossref a) vs FINDINGS lines 146-156, task line 216 | The lens asks that AD-1..AD-7 trace to a Section 8 step or Section 9 entry. FINDINGS says they are accepted divergences, not fix requests, and synth-02 places them only under Section 3 constraints. A strict lens would raise seven false blocking breaks and could drive a HALT-MONOTONICITY loop. | Reword lens (a) so AD items must appear as preserved constraints in Section 3 or 7, not as resolved gaps. |
| N-5 | Note | Task line 228 vs FINDINGS line 173 | The FINDINGS rule "a phase closes only when all High and Medium criteria pass", with OPEN-1..3 treated as Medium and M-14 scheduled late, is not stated in the synth-05 prompt. Agent 4 reads FINDINGS so it can surface it, but nothing requires it. | Add the closing rule and the OPEN handling to the synth-05 prompt. |
| N-6 | Note | Task line 118 vs lines 198 and 202 | Line 118 says prompts are passed "after substituting nothing", but Steps 4.1 and 4.2 require substituting a summary into a placeholder. | Add "except the Phase 4 summary field". |
| N-7 | Note | Task line 144 (Step 2.3 f) | Lets Agent 3 run `uv run pytest tests/observe/ -q` once. Not in the notes, not forbidden by the build request. Step 7.1 checks tracked files only, so cache files would not show. Harmless. | None required. |

## Verdict
All 5 codebase agents, 2 web agents, 6 synthesis files, output paths, Q1-Q7 reachability, finding-id reachability, constraint coverage, phase ordering and all five gate agent counts match the inputs. No fabrication. The seven notes are guidance hazards, not dropped or misrepresented requirements.

VERDICT: PASS
