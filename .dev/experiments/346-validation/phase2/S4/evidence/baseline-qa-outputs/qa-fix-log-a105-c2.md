# Fix log: A.10.5 review 2, final fix cycle (F21 to F25)

**Target:** .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md
**Findings source:** qa/qa-task-validation-consolidated.md section "A.10.5 verification round (review 2)"; qa/qa-fix-verification-a105.json; qa/qa-qualitative-verification-a105.md
**Date:** 2026-11-07
**Status:** Complete
**Rule:** targeted Edits only (replace_all only for byte-identical repeated text); no product-code edits; no installer run; no commit; BMAD first-use only.

---

## Changes (line numbers after all edits; the task file now has 602 lines because Builder Note 15 was added at line 601)

| Finding | Lines | Change |
|---|---|---|
| F21 | 308, 312, 316, 320 (Gate 2) | One STOP-AND-RE-SCOPE BRANCH sentence per item: when Section 7 states STOP-AND-RE-SCOPE, Section 8 (starts with `RE-SCOPE PROPOSAL`) is judged as a proposal (repository or owner decision, decision owner, pinned tests and documents touched, resume condition) and missing implementation steps, step table or change list are not a defect. 320 regrades such findings to MINOR and lists them under Severity changes. |
| F21 | 365, 373, 383, 387, 391 (Assembler, Gate 3) | Assembler cross-check keeps the proposal unchanged; internal-consistency and crossref lenses apply the branch; reproducibility lens names STOP-AND-RE-SCOPE explicitly; consolidation 391 regrades with ledger entry. 371, 379 and 475 already had it. |
| F21 | 417, 419, 421, 423, 449, 451 (Gates 4 and 5) | Same branch in fidelity agents 1 to 3, fidelity consolidation, anti-omission agents 2 and 3 (a test or document counts as present when listed in the proposal). |
| F21 | 425, 429, 435, 439, 455, 459, 465, 469 | Fix and verification prompts that add or check plan steps or change-list rows: the same branch (add to the proposal list, no implementation steps). |
| F22 | 136, 193-209, 234, 254, 279, 283, 292-304, 324, 344, 365, 393, 405, 425, 435, 455, 465 | Key Constraints rule (3), (4), (7): QA/analyst/lens return up to 4000 characters inline; research, synthesis, assembler agents return the COMPLETE file as the final message (no cap, spawn unnamed); fix agents return exact old/new edit pairs plus the fix log, uncapped; gap researchers return the full addendum text; the executor writes verbatim with a quoted-delimiter `cat` heredoc or Write in chunks, never retyped, decodes a wrapped .json, labels it transcribed, and applies fix pairs with Edit. Carried into 7 research, 4 synthesis, 1 assembler and 10 fix items (agent-side sentence replacing the old "too large for the inline route" sentence, and executor-side tail), plus the 2 gap researchers inside 234 and 254. QA/analyst/lens items not touched for F22. |
| F23 | 136(3)(6), 39 QA/analyst/lens items (218-226, 238-242, 258-262, 308-316, 328-332, 348-352, 371-387, 397-399, 407-409, 417-421, 427-429, 437-439, 447-451, 457-459, 467-469), 423, 595 | Inline cap raised from 1500 to 4000 characters (blocking findings first, then severity counts and verdict, then Self-Audit); the final-message cap in those prompts now reads "stay under 4000 characters". After the one re-run, a report still missing, without Self-Audit or truncated HALTS and escalates (never a PASS, never zero findings) in rule (6) and all 39 executor tails; 423 applies the same outcome to the missing Web-source check table. |
| F24 | 246, 336, 401, 431, 461 (decision items), 266, 356, 411, 441, 471 (final verdicts), 433, 463, 488 | Each decision file records `SEVERITY_DOWNGRADES: <n>` plus one line per downgrade, counted from the consolidated file's Severity changes section; final-verdict items update the total when cycle 2 ran; 433 and 463 spell out the Severity changes section; Step 7.2 (488) lists every downgrade in one table in the user summary (or `none`). |
| F25 | 270, 234, 254, 304, 279, 283, 371-387, 230, 320, 391, 423, 453, 433, 463 | Addendum owner: the Phase 3 fix agent (234, 254) merges `.addendum.json` or inline addendum text into the research file, Step 3.14 (270) is the backstop (Glob `research/*.addendum.json`, Grep for the heading, append raw markdown). 304 and 270 read the open-questions section with Read offset 159 limit 7 (lines 159-165) or Grep, never the whole file. Lenses ignore a leading `Transcribed by orchestrator` line. 279 and 283: web-unavailable allowed ONLY for web topics and only when the file exists and states the reason; a missing or empty file still HALTS. "never a PASS and never zero findings" added at 230, 320, 391, 423, 453; the `none` wording added at 433 and 463. |
| Notes | 595, 601 | Builder Note 9 updated; new Builder Note 15 records this cycle. |

## Checks
- `grep -c '^- \[ \]'`: 91 (unchanged).
- 61 BEGIN AGENT PROMPT and 61 END AGENT PROMPT; no odd backtick counts.
- Lines containing STOP-AND-RE-SCOPE: 304 308 312 316 320 365 371 373 379 383 387 391 417 419 421 423 425 429 435 439 449 451 455 459 465 469 475 (and notes 600, 601). Every item that mentions Section 8 or plan steps (census by script) has it, except 205, 292 and 296 (research and synth-01/02 prompts that do not judge Section 8).
- Remaining "1500" lines: 193 197 201 205 209 234 254 279 283 292 296 300 304 324 344 365 393 405 425 435 455 465 (research, synthesis, assembler, fix and gap-researcher short final messages only); 0 QA/analyst/lens items; 0 occurrences of "in at most 1500 characters".
- "a missing report is never a PASS and never zero findings" present at 230, 320, 423, 453; 391 uses "a missing lens report is never a PASS and never zero findings".
- Size: 618892 bytes (about 604 KB, up from 553542 bytes).
- Only the task file and this log were edited. No installer run, no product-code edit, no commit.
