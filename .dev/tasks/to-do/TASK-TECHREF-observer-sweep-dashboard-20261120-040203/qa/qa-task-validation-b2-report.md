# QA Report - Task Integrity, Lens b2-self-containment

**Topic:** TASK-TECHREF-observer-sweep-dashboard-20261120-040203 (Technical Reference: observer / sweep / agent-work-report / Orca dashboard design)
**Date:** 2026-11-20
**Phase:** task-integrity (lens b2-self-containment)
**Fix cycle:** N/A (fix_authorization: false, report only)
**Task file:** /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/TASK-TECHREF-observer-sweep-dashboard-20261120-040203.md

---

## Overall Verdict: PASS (0 blocking, 3 Medium, 11 Notes). See the VERDICT line at the end.

## Method (what was actually done)

- Read the whole task file in ranges (524 lines, 416,210 bytes; 81 `- [ ]` items), BUILD-REQUEST.md, research-notes.md, template 02 section B (B1-B7, I15, I16), tech-reference SKILL.md (Synthesis Agent Prompt, gate lines), /task SKILL.md (F1 loop lines 91, 103, 113, 604, 612).
- Scripted per-item analysis (read-only, private /tmp batch dir, removed afterwards): item id, length, spawn flag, PROMPT BEGIN/END balance, GLOBAL AGENT RULES (GAR) placement, GAR comparison against BUILD-REQUEST.md lines 32-37, `fix_authorization` value, "ensuring" clause, failure clause, completion sentence.
- Existence check of all 135 absolute paths named in the file (every input exists; only to-be-created outputs are absent), about 65 snapshot-relative paths, and 8 line anchors (`_find_orca` at install_user_setup.py:247, `check_orca_argv` at probes.py:226, QUESTION_GATE_PASSED / QUESTION_LINK_PASSED at commands.py:67 / 70, .gitignore:255-256, main.py:590-592): all match.
- Subagent types checked against agent definitions, including the `deep-research` tool list in /home/coder/.claude/agents/deep-research.md.
- `gh`, git, python and SuperClaude-Org mentions scanned for scope-boundary risk.

## Items Reviewed

B2 per item = context + action + output + verification ("ensuring") + completion/failure gate. All 81 items have an "ensuring" clause, a failure clause and end with "Once done, mark this item as complete." (four items, 3.1/5.2/6.2/7.1, phrase the failure clause as "If no ... found / missing, log this as a blocker"; see N1).

| Items (line) | Step | Kind | Result | Evidence |
|---|---|---|---|---|
| 163 | 1.1 | frontmatter + log | PASS | status/start_date/updated_date only; log format given |
| 167, 171, 175, 179 | 1.2-1.5 | read + create file | PASS | each reads named files and creates a named file under reviews/; no standalone read item. 179: see N6 |
| 187, 191, 195, 199, 203, 207 | 2.1-2.6 (R1-R6) | spawn rf-task-researcher | PASS | GAR block verbatim right after `PROMPT BEGIN:`; Incremental Writing, Staleness and C8 clauses present; topic, files, output path, measurable ensuring clause; parallel marked |
| 215 | 3.1 | aggregate | PASS | Glob + wc + file, counts specified |
| 219, 221, 223 | 3.2 | spawn rf-analyst / rf-qa / rf-qa-qualitative, fix_auth false | PASS | GAR first; lens, input files, report path, adversarial framing, verdict rule, 90-row citation minimum |
| 227 | 3.3 | consolidate | PASS | file, columns, blocking count, branch rule |
| 232 | 3.4 | conditional template (dynamic) | PASS (N8) | full prompt + GAR; bracket placeholders are runtime fill-ins inside DYNAMIC CONTENT markers |
| 237, 239 | 3.5 | spawn rf-qa / rf-qa-qualitative, fix_auth false | PASS | full prompts, GAR first, RESOLVED / STILL OPEN rule |
| 243 | 3.6 | consolidate + halt checks | PASS | byte-exact halt messages, file, columns |
| 246 | 3.6 | spawn (cycle-2 gap-fill) | FAIL (Medium M1) | no prompt embedded; "re-read the template item in Step 3.4 ... execute it unchanged"; two-level indirection (246 -> 232 placeholders) |
| 251, 253 | 3.7 | spawn (cycle-2 verification) | FAIL (Medium M1) | no prompt embedded; refer to the Step 3.5 items |
| 257, 261 | 3.8, 3.9 | compile / verdict | PASS | files, columns, HALT rule |
| 269 | 4.1 | decision + conditional spawn deep-research | FAIL (Medium M3) | agent type has no Write/Edit; prompt undelimited; placeholders |
| 277, 279, 281, 283, 285, 287, 289 | 5.1 | spawn general-purpose, one per synth file | PASS | one item per file; SKILL synthesis rules 0-12 embedded; sections, line budget, output path; GAR first |
| 293 | 5.2 | aggregate | PASS | |
| 297, 299, 301, 303, 305, 307 | 5.3 | Gate 2 lens agents, 3 lenses x 2 partitions | PASS | exactly 6; files per partition named; numbered report paths |
| 311 | 5.4 | consolidate | PASS | |
| 315 | 5.5 | spawn rf-qa, fix_auth true | PASS (N5) | write boundary stated (synthesis files + fix log only) |
| 319, 321 | 5.6 | verification round | PASS | |
| 325 | 5.7 | consolidate + halt checks | PASS | |
| 327 | 5.7 | re-synth N files + spawn fix agent, fix_auth true | FAIL (Medium M1 + M2) | batch ("for every synthesis file ... re-execute the corresponding Step 5.1 item") plus a by-reference spawn |
| 329, 331 | 5.7 | spawn (cycle-2 verification) | FAIL (Medium M1) | by reference to Step 5.6 |
| 335 | 5.8 | verdict | PASS | |
| 343 | 6.1 | spawn rf-assembler (single) | PASS | single agent as required |
| 347 | 6.2 | aggregate | PASS (N4) | |
| 351, 353, 355, 357, 359, 361, 363 | 6a | Gate 3 lens agents | PASS | exactly 7 (3 rf-qa structural, 3 rf-qa-qualitative, 1 rf-qa domain lens), lens named, distinct report paths, fix_auth false |
| 367 | 6b | consolidate | PASS | |
| 369 | 6b | spawn rf-qa, fix_auth true | PASS | write boundary: only OUTPUT_PATH and fix log |
| 371, 373 | 6b | verification round | PASS | |
| 377 | 6b-c2 | consolidate + halt checks | PASS | |
| 379 | 6b-c2 | spawn rf-qa fix_auth true | FAIL (Medium M1) | by reference to the Step 6b fix item |
| 381, 383 | 6b-c2 | verification | FAIL (Medium M1) | by reference |
| 385 | 6b-c2 | Gate 3 verdict | PASS | |
| 389, 391 | 6c | Gate 4 fidelity agents | PASS | disjoint halves per BUILD-REQUEST; both lenses per agent (logged deviation, builder Open Question 2) |
| 393 | 6c | consolidate | PASS | |
| 395 | 6c | spawn rf-qa fix_auth true | PASS | write boundary stated |
| 397, 399 | 6c | verification | PASS | |
| 401 | 6c | cycle 2: consolidate + fix + 2 verifications | FAIL (Medium M1 + M2) | one item with 3 sub-spawns, all by reference |
| 403 | 6c | Gate 4 verdict | PASS | |
| 407 | 6d | verify QA complete | PASS | |
| 415, 419, 423, 427, 431 | 7.1-7.5 | completion | PASS | each produces a file or a defined return; completion items are inside Phase 7 |

Totals: 81 items; 70 PASS (some with notes), 11 FAIL on the B2 letter (246, 251, 253, 269, 327, 329, 331, 379, 381, 383, 401). None of the 11 is blocking under the severity rule (reasons in the findings).

## B2 Self-Containment Checklist (the 8 lens checks)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Every item has all 5 B2 components | PASS for 70 of 81; 11 Medium exceptions | 81/81 have an "ensuring" clause, a failure clause and the completion sentence; 10 cycle-2 items (246, 251, 253, 327, 329, 331, 379, 381, 383, 401) have no Context/Action of their own (they borrow another item's); 269 per M3 |
| 2 | No item references a prior item's context without restating it | FAIL (Medium M1) | those 10 items say "re-read the ... item in Step X of THIS task file and execute it unchanged except ..." |
| 3 | Agent-spawning items have fully embedded prompts | FAIL (Medium M1, M3) for 11 items; PASS for the 44 items that carry `PROMPT BEGIN` | script: 44 `PROMPT BEGIN` = 44 `PROMPT END`, none unbalanced; all 44 contain the Incremental File Writing clause and the ESCALATION clause (no SendMessage / TaskCreate / TaskUpdate / TaskList) |
| 4 | File paths specific | PASS (N3) | 135 absolute paths all resolve; some "same directory" shorthand after a full path |
| 5 | Verification measurable | PASS | counts given: 90 sampled citations (Gate 1 evidence), 40-row detail tables (Gate 4), 60 inline refs (code-example lens), agent counts 3 / 6 / 7 / 2 per gate, exact halt messages |
| 6 | No batch items | FAIL (Medium M2) for 327 and 401 only | every research agent, synth file, lens agent and fidelity agent has its own item |
| 7 | No items based on [CODE-CONTRADICTED] / [UNVERIFIED] findings as current | PASS (N9) | staleness warnings appear only as things to verify or to carry into Section 14; UNVERIFIED items (Orca automations, `.dev/coordinator/`, `orchestrator_repo`, question non-acknowledging) are marked UNVERIFIED in R1 / R5 / synth-07 |
| 8 | Every embedded prompt begins with the BUILD-REQUEST GAR block | PASS for the 44 `PROMPT BEGIN` items (GAR is the first text after `PROMPT BEGIN:`; all six bullets equal BUILD-REQUEST.md L32-37 after whitespace normalisation); 4.1 has the block right after "with the prompt:"; the 10 by-reference items name the block but do not contain it (M1) | script comparison of all six bullets per item |

## Findings

Severity rule applied: Blocking = an executor would do something wrong, a required deliverable is missing, or a safety / scope-boundary risk. Medium = real non-blocking weakness. Note = wording / format / cosmetic.

### M1 (Medium): ten cycle-2 items are not self-contained; they re-read another item and substitute file names

- Items: 246 (Step 3.6 cycle-2 gap-fill), 251 and 253 (Step 3.7), 327 (Step 5.7 re-synthesis + fix spawn), 329 and 331 (Step 5.7), 379 (fix spawn, `fix_authorization: true`), 381 and 383 (Step 6b-c2), 401 (Step 6c cycle 2).
- Quote (253): "re-read the qualitative verification item of Step 3.5 in THIS task file and execute it unchanged (agent type rf-qa-qualitative, fix_authorization: false, with the GLOBAL AGENT RULES block and prompt exactly as embedded there) except that the findings file is `qa-research-consolidated-findings-c2.md` ...". Quote (246): "re-read the template item in Step 3.4 of THIS task file ... the agent prompt ... is the one embedded in Step 3.4".
- Does it break B2? Yes, in the letter. B2 and B3 say an item "could be executed independently without any prior context"; task-integrity check 5 names "see above" as the thing that fails. An executor holding only item 253 cannot spawn the agent: it has no prompt, no GAR block, no lens text. Lens checks 2, 3 and 8 fail for these ten items.
- Why Medium and not Blocking:
  1. The execution engine is the F1 loop, which is non-delegable and must re-read the whole task file before every item (/home/coder/.claude/skills/task/SKILL.md lines 91, 103, 113, 604, 612), so the referenced item is on disk and in reach. The builder says the same (task file line 438).
  2. Each reference names the exact step and role ("structural verification item of Step 3.5", "fix item of Step 6b", "Gate 4 fix item"), and every changed path is listed, so mis-substitution is unlikely.
  3. They are contingency items, run only after a gate FAIL. The GAR block, write boundary (fix agents may only edit OUTPUT_PATH / synthesis files plus their own log) and read-only rules sit verbatim in the referenced cycle-1 items (315, 369, 395), and the items say "same GLOBAL AGENT RULES block".
- Concrete residue that the substitution lists do not cover (these are the real cost):
  - Counter labels. The cycle-1 verification prompts say "Record the count of open blocking findings `|F_2|` and compare with `|F_1|` in the consolidated file" (237, 319 family, 371, 397). In review 3 the right pair is `|F_3|` vs `|F_2|`, but the listed substitutions only swap file names. The c2 file itself is labelled `|F_2|`, so a literal agent compares a number with itself or looks for a `|F_1|` that is not in the c2 file. Effect is limited to the label, because the verdict items (3.9, 5.8, 6b-c2 verdict, 6c verdict) apply the cap when any blocker is open after review 3.
  - 246 depends on 232, which is itself a placeholder template; the executor must resolve two levels of indirection and then fill four bracket placeholders.
  - Three of the ten are `fix_authorization: true` spawns (327, 379, 401); the only statement of their write boundary is in the referenced item.
- Upgrade condition: if the executor is ever run per item in a fresh context (contrary to F1 rule 12), these ten items cannot be executed and the finding becomes Blocking.
- Suggested fix (optional): embed the full cycle-2 prompt in each of the ten items (the task file is already large, so the alternative is to keep the references and add to each "also rename `|F_2|`/`|F_1|` to `|F_3|`/`|F_2|`" and to name the write boundary in the item text).

### M2 (Medium): items 327 and 401 are batch / multi-action items

- 327 (Step 5.7): "for every synthesis file that the cycle-1 fix log ... marks NEEDS-RESYNTH ..., re-execute the corresponding Step 5.1 item of THIS task file ..., then spawn ONE Agent subagent (rf-qa, fix_authorization: true) re-reading the Step 5.5 item". That is a variable number (0-7) of re-synthesis spawns plus a fix spawn in one checkbox.
- 401 (Step 6c): one item holds consolidation, halt checks, a `fix_authorization: true` spawn and two verification spawns ("the three spawned agents are separate sub-spawns of this one conditional item, run sequentially (fix first, then the two verifications in parallel)").
- Lens check 6 ("no batch items") and template B7/I15 ("every QA gate step ... MUST be encoded as individual `- [ ]` checklist items") fail for these two. The file is inconsistent with itself: Gate 1 (243/246/251/253), Gate 2 (325/327/329/331) and Gate 3 (377/379/381/383/385) split cycle 2 into separate items, Gate 4 does not.
- Consequence: no resume point if a session ends after the fix agent but before the verifications; the item can only be checked once all three finished. Not wrong behaviour, hence Medium.
- Suggested fix: split 401 into consolidate / fix / structural verification / content verification items, and 327 into one conditional re-synthesis item per synth file (or state "up to 7" explicitly) plus the fix item.

### M3 (Medium): Step 4.1 (line 269) conditional branch cannot produce its output with the named agent type

- 4.1 says: spawn "ONE Agent subagent (subagent_type: "deep-research") that writes `.../research/web-01-orca-cli.md`" and the embedded prompt says "FIRST ACTION create the output file ... append ... never accumulate and one-shot".
- /home/coder/.claude/agents/deep-research.md lists tools: Tavily search/extract/map/crawl, WebSearch, WebFetch, context7 resolve/query, Read, Grep, Glob. There is no Write and no Edit (checked: zero matches for Write/Edit in the frontmatter). The agent cannot create or append to the file.
- The branch is not remote: the item itself names the likely trigger ("whether `orca orchestration check --all --types question` acknowledges what it reads, if that stayed UNVERIFIED and code, tests and fixtures cannot settle it").
- Also: this is the only embedded prompt in the file without `PROMPT BEGIN` / `PROMPT END`; the prompt ends in "...note any discrepancy explicitly. Then record in the decision file that web research ran and why, ensuring ..." so it is unclear whether "Then record in the decision file" is part of the agent's prompt or the executor's action. It also carries two runtime placeholders ("[the exact external Orca documentation question taken from the gap]", "[brief summary from the research files]").
- Suggested fix: use a Write-capable agent (for example general-purpose with a "Tavily first" line, or rf-task-researcher, which has Tavily and Write) or have the executor write the file from the returned text; add `PROMPT BEGIN` / `PROMPT END`.

### Notes (do not affect the verdict)

- N1: Template B2 element 6 ("This item cannot be marked as done until the actions are completed in their entirety exactly as described.") appears in none of the 81 items; every item ends with "Once done, mark this item as complete." only. The template's own canonical example B4 does the same, so this is acceptable. Items 215, 293, 347, 415 phrase the failure clause as "If no ... found / missing, log this as a blocker".
- N2: Several items share one Step id (3.2 x3, 3.5 x2, 3.7 x2, 5.1 x7, 5.3 x6, 5.6 x2, 5.7 x4, 6a x7, 6b x4, 6b-c2 x5, 6c x8). References such as "the Step 5.1 item" or blocker logs "Step X.Y" are then ambiguous unless the item descriptor is also used (the items do give descriptors).
- N3: Some items give one full path and then bare file names "(same directory)" (for example 227, 251, 253, 393, 397). They resolve, but the lens asks for specific paths.
- N4: Item 347 says its summary "is the input for the Gate 3 lens agents' line-count reference", but none of the 6a prompts (351-363) reads `phase6-assembly-summary.md`; it is only read again by 419. The dependency is declared, not wired. Harmless (lens agents read the document itself).
- N5: Item 315 says the research files are "the only source of corrected facts", while its embedded rule 2 says to re-read the cited snapshot lines when a fix depends on a code fact. Small internal conflict in the fix-agent prompt.
- N6: Item 179 authorises `mkdir -p` of the techref output directory, which is outside the task folder, while the GAR block says to write only inside the task directory or the single output file. The directory already exists (`ls` shows `.../20261120-pr686-unify/techref`), so there is no practical effect.
- N7: The "Frontmatter Update Protocol" (line 144) says "If Blocked: ... status to '⚪ Blocked'", which is not in the status options list on line 6 (`🔴 Blocked`). The HALT items use "🔴 Blocked" (valid). The wrong symbol is inherited from the template (template lines 467, 868, 1232).
- N8: Items 232 and 269 contain bracket placeholders by design (dynamic content). 232 is correctly inside DYNAMIC CONTENT markers; 269 has no marker (see M3).
- N9: Several synthesis prompts state scope-discovery counts as content to write (sweep "8 classes", agent-work-report "6 model-judged statuses", "four separate sanitizers", "three separate Orca binary choices", "designed only (the orchestrator writer ...)"), while rule 2 says every fact must come from the research files. These numbers are not tagged "if research confirms". Gate 1's depth lens (item 223, check 4(v)) and the Gate 2 accuracy lens would catch a mismatch, so this is a bias risk, not a defect.
- N10: The task file is 416,210 bytes (about 104K tokens), 47 lines exceed 2,000 characters (longest 14,892). The GAR block (about 1.6 KB) and the protocol boilerplate are repeated 44 times, as the requester demanded ("embedded verbatim at the top of EVERY sub-agent prompt"). A whole-file read per F1 iteration is impractical and must be done by range; the executor can still reach any referenced item, but this weakens the "F1 re-reads the file" argument used for M1.
- N11 (outside this lens, observed only): (a) Gate 4 half A (item 389) does not list `cli/install_user_setup.py` (`_find_orca`) or `cli/main.py` (registration), which R1 and R2 cite, so those claims have no fidelity reader; (b) the frontmatter has `created_date` but no `created`, `template` or `tracks` key (task-integrity check 1 wording); neither was graded here.

## Confidence and tool engagement

- Checklist: 8 B2 checks, all VERIFIED with tool evidence; 0 unverifiable; 0 unchecked. Per-item rows: 81 of 81 reviewed.
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: 5 | Glob: 0 | Bash: 14 (read-only inspections and two scripted batches in a private /tmp dir, removed after use)
- Not done: I did not execute any agent prompt or the code under study; "mitigation" arguments in M1 rest on /task SKILL.md text, not on a live run.

## Recommendations

1. Proceed; no blocking B2 defect. 
2. Optional hardening before execution, in order of value: M3 (swap the agent type, it is a real tool gap), M2 (split 401), M1 (embed or at least add counter-label and write-boundary lines to the ten by-reference items).

## QA Complete

VERDICT: PASS


