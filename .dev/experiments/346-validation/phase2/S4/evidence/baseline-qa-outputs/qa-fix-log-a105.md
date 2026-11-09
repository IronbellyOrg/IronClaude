# Fix log: A.10.5 qualitative cycle (F12 to F20)

**Target:** .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md
**Findings source:** qa/qa-task-validation-consolidated.md section "A.10.5 qualitative findings"
**Date:** 2026-11-07
**Status:** Complete
**Rule:** targeted Edits only (replace_all only for byte-identical repeated sentences); no product-code edits; no installer run; no commit; BMAD first-use only.

---

## Changes (appended as applied)

Line numbers refer to the task file after all edits (601 lines; one Key Constraints bullet and one Builder Note were added, every other change is in place on existing lines).

| Finding | Lines | Change |
|---|---|---|
| F12 | 131, 136 | Key Constraints: AGENT REPORT FALLBACK rule in full (try .md, then .json, then inline return of at most 1500 characters; executor copies verbatim under `Transcribed by orchestrator`; nothing delivered = FAILED agent, respawn once, then status Blocked and HALT; a missing report is never zero findings or PASS; inline route unavailable for research, synthesis and assembled-report outputs; fix agents report BLOCKED instead of partial edits). Line 131 points to it. |
| F12 | all 61 agent-spawning items (193-209, 218-226, 234, 254, 258-262, 279-283, 292-316, 324-352, 365-387, 393-409, 417-421, 425-439, 447-451, 455-469) | Agent side: full fallback sentence placed before every "Your final message must be under 1500 characters" (61 items, includes the gap researchers inside 234 and 254); fix agents also get the BLOCKED clause; research, synthesis and assembler prompts get an "inline route unavailable" sentence. Executor side: the old "log the blocker, mark complete" tails replaced by the fallback with respawn once then HALT (61 items); the "produced by the agent and not by you" wording replaced by "the agent's own output (a verbatim copy labelled Transcribed by orchestrator counts)" in every gate and fix item; consolidation and decision steps (230, 246, 250, 320, 336, 340, 391, 401, 403, 423, 431, 433, 453, 461, 463) and Step 6.8 (475) use the same rule for missing reports. Builder Note 9 (line 596) rewritten. |
| F13 | 169 | F1 loop: never read the whole file; Grep `^- \[ \]` (output_mode content, -n) for the next item, Read with offset and limit, targeted Edit to tick. File size not reduced (it grew; see Checks); no prompt text removed. |
| F14 | 128, 165, 193, 197, 201, 205, 209, 234, 254 | One BMAD CLI RULE sentence: only `NPM_CONFIG_OFFLINE=true bmad --version`, `bmad install --help`, `bmad install --list-tools`, `bmad install --list-options`; no other subcommand, no actual install. Contradictory Step 2.1 wording ("run no installer command at all", "no installer command was run", two separate help-flag sentences) removed; Step 2.2 part (a) (line 197) reworded as a code-reading question (read the wrapper and the code it execs; do not run bmad). |
| F15 | 304, 371, 379, 475 | synth-04: STOP-AND-RE-SCOPE makes Section 8 a "RE-SCOPE PROPOSAL" (what must change in which repo or owner decision, decision owner, tests and documents touched, resume condition; items (i)-(vi) written for the proposal). Gate 3 actionability lens: branch applying a-d to the proposal. Template-conformance lens: heading stays. Step 6.8: branch applying criteria 8, 21, 22, 23 to the proposal. |
| F16 | 230, 250, 320, 340, 391, 403, 423, 433, 453, 463 | Consolidated tables now carry Reporter severity, Final severity and Reason for any change; SEVERITY LEDGER: BLOCKING_COUNT from Final severity only, mandatory `## Severity changes` section (or `none`), every downgrade of a reporter CRITICAL or IMPORTANT listed with a cited reason. |
| F17 | 415, 421, 423 | Gate 4 paragraph names the web-source check; fidelity agent 3 gets checklist item 6 WEB-SOURCE CHECK (re-fetch the URL behind every web finding that supports a ranked option or the recommendation; mismatch, no URL or unsupported claim is blocking; `### Web-source check` table); consolidation requires that table (re-run agent 3 once if absent). |
| F18 | 387 | Reproducibility lens reproduces EVERY pinned test and document line named in Section 8 (and the re-scope proposal); a wrong line number on an edit row is IMPORTANT; the grading sentence and the consolidation grading (391, 423) carry the exception. |
| F19 | 218-226, 238-262, 292-316 (synthesis), 328-352, 371-387, 397-409, 417-421, 427-439, 447-451, 457-469 | 43 QA, analyst and lens prompts: mandatory `## Self-Audit` (or `### Self-Audit` in the lens, fidelity and anti-omission output formats); synthesis analysts end with `## Self-Audit (not a report section)`, which the assembler omits (assembly rule 8, line 365); executor side re-runs an agent once when the section is missing or the verdict is a bare zero. |
| F20 | 209, 304, 381 | Agent 05 scope adds `.github/upstream-monitor/expected.txt` and `.github/upstream-monitor/renovate-global.json5` (new part (f), documented-or-irrelevant decision with file:line, plus verification clause); synth-04 document list names them; domain-accuracy lens item e re-derives the Feasibility statement. |
| Notes | 599-600 | Builder Note 13 F11 wording aligned; new Builder Note 14 records this cycle. |

## Checks
- `grep -c '^- \[ \]'` on the task file: 91 (unchanged; no item added or removed).
- File size: 553542 bytes (about 541 KB), up from about 403 KB. All additions are prompt-side rule text (fallback, Self-Audit, CLI rule, ledger); no prompt text was removed. F13 is satisfied by the loop instruction at line 169.
- Old wording "not by you" / "produced by the agent": 0 hits. No hits for "no installer command", "installer command at all" or "installer command was run".
- 61 agent-spawning items = 61 agent-side fallback sentences = 61 executor-side fallback tails.
- Only the task file and this log were edited. No installer run, no product-code edit, no commit.
