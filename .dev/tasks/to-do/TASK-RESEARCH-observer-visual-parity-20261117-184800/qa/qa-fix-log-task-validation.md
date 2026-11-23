# QA fix log, task-file validation, fix round 1

Task file: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/TASK-RESEARCH-observer-visual-parity-20261117-184800.md
Findings source: /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/qa/qa-task-validation-consolidated.md

## Entries

Line numbers are those of the task file after all edits.

- C-3, five halt sites (lines 179, 257, 309, 335, 361): before `Regression detected on Item X.Y, previously PASS ...` (comma); after `Regression detected on Item X.Y — previously PASS ...` (em dash). Grep confirms 5 matches of the em-dash string.
- C-1, Step 3.3 (line 181): before "using the same fix-agent prompt as Step 3.2 (...)"; after the full cycle-1 fix prompt embedded with the cycle-2 consolidated and fix-log paths (phase3-cycle2).
- C-1, Step 5.9 (line 259): before "using the same fix-agent prompt as Step 5.8 (...)"; after the full Step 5.8 prompt embedded with phase5-cycle2 paths.
- C-1, Step 6.6 (line 311): before "using the same fix-agent prompt as Step 6.5 (...)"; after the full Step 6.5 prompt embedded with cycle2 paths (qa-consolidated-findings-phase6-cycle2.md, qa-fix-log-cycle2.md).
- C-1, Step 6.7 (line ~337): before "using the same fidelity fix-agent prompt as in the cycle-1 fix item above (...)"; after the full fidelity fix prompt embedded with the cycle2 paths.
- C-1, Step 6.8 (line ~363): before "using the same anti-omission fix-agent prompt as in the cycle-1 fix item above (...)"; after the full anti-omission fix prompt embedded with the cycle2 paths.
- C-5, Step 6.7 verification (old single item at ~line 338): before one item spawning an rf-qa and an rf-qa-qualitative agent; after two `- [ ]` items, one rf-qa (output qa-fidelity-verification-1-cycle2.md) and one rf-qa-qualitative (output qa-fidelity-verification-2-cycle2.md), each with its own prompt, "not needed" branch and completion gate. No renumbering; steps have no per-item numbers.
- C-5, Step 6.8 verification (old single item at ~line 364): same split into rf-qa (qa-anti-omission-verification-1-cycle2.md) and rf-qa-qualitative (qa-anti-omission-verification-2-cycle2.md) items. The four "saying not needed" branches grep-confirmed.
- C-4, Gate 4 intro (line ~321): before "partitioned ... so the whole source set is covered"; after states every file named in research-notes EXISTING_FILES and under inputs/ is assigned to exactly one agent, and unnamed test modules are context only.
- C-4, Gate 4 fidelity agent 1 prompt (Step 6.7): before sources ended at the two goldens; after adds test_linkoff_screen_reference.py, release1_surface.py, record_golden.py, record_golden_questions.py, parse.py, adapter.py, and mockups and current renders for widths 160 and 116.
- C-4, Gate 4 fidelity agent 2 prompt (Step 6.7): before sources ended at pyproject.toml and Makefile; after adds mockups and current renders for width 80, inputs/tools/render_questions_screen.py, the three attachments PNGs and pr-591-comment.md (FINDINGS.md was already assigned to agent 2).
- C-4, Gate 1 evidence-quality prompt (Step 3.1, line 163): before spot-read scope limited to observe/ and tests/observe/; after also lists the mockup files, inputs/current renders, FINDINGS.md, test_linkoff_screen_reference.py, release1_surface.py, record_golden*.py, parse.py and adapter.py as openable sources.
- C-2, Step 5.6 synth-06 prompt (line 233): before "every unresolved gap that is not closed by an implementation step; do not include questions answered elsewhere in the plan"; after lists all unresolved gaps and open questions from research, gaps log and web files, O-1 and OPEN-1..3 as open owner decisions, and leaves removal of answered questions to the assembler's cross-check.
- N-1 (operational), Prerequisites section (line 82): added one line, executor reads the file with Grep for `^- \[ \]` plus ranged Reads, never a single full Read.
- N-2 (operational), Task Log section: added a "Heading pattern note" line naming `### Phase N - <name> Findings` and matching by phase number; the ~80 references were not edited.
- N-5/N-6 (operational), Gate 1 completeness lens (Step 3.1, line 161): before no partial-answer tolerance; after states Q1 to Q7 answers may be partial until web research and synthesis, and a gap web research will close is not blocking at Gate 1.
- N-5/N-6 (operational), Gate 3 evidence-quality lens (Step 6.2): added that an environment fact proven by a recorded command output needs no file:line citation if the command and output are cited.
- N-5 (alignment), Step 5.5 synth-05 prompt: added that every phase ends with a render gate, closes only when all High and Medium criteria pass, OPEN-1 to OPEN-3 count as Medium until the owner rules, and the render gate includes a NO_COLOR and ASCII pass (G-1).
- N-4 (alignment), Gate 3 crossref-chain lens prompt (Step 6.4): added that AD-1 to AD-7 are not fix requests, need no Section 8 step, and should appear in Section 3 or Section 4 as accepted divergences.
- N-9 (operational), Phase 7: added one item before the "set status Done" item recording in the Execution Log that `.dev/tasks/` stays staged by the coordinator, with no git add or commit by the task.
- N-6 (structure), "28 test modules" (Source Areas line 95) and "28 .py files" (Step 2.3 prompt, line ~145): both now read "28 Python files under tests/observe (22 test_*.py modules)" wording. research-notes.md was not touched.

Grep checks after all edits: "same fix-agent prompt" and "cycle-1 fix item above" 0 matches; em-dash halt string 5 matches; `- [ ]` items 85 (was 82, plus 2 splits plus 1 new Phase 7 item).
