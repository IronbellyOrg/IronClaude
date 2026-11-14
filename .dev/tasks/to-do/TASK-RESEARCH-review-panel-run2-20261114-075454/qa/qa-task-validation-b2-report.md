# QA Report - Task Integrity, Lens b2-self-containment

**Topic:** Unified Review Panel research task (run 2)
**Date:** 2026-11-14
**Phase:** task-integrity (lens: B2 self-containment)
**Fix cycle:** N/A (fix_authorization: false)
**Task file:** /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md

(Findings appended incrementally below.)

## Method

Task file has 717 lines; lines 150-717 hold the checklist. Counted with grep: 186 `- [ ]` items (Phase 1: 3, Phase 2: 24, Phase 3: 27, Phase 4: 4, Phase 5: 50, Phase 6: 70, Phase 7: 3, Post-Completion: 5), 0 nested checkboxes, 0 pre-checked. The Read tool refuses the file in large chunks (items are 2-7 KB each), so items were read by line with sed through Bash, plus programmatic per-item checks (independence strings, completion gate sentence, spawn marker). The shared Phase 2 prompt preamble was hashed: items 2.01-2.18 share an identical preamble (md5 38963a0b, 18 of 18); items 2.19-2.22 share one, 2.23 and 2.24 differ only in their anchors (read).

## Findings so far (Phase 1-3)

### F-1 (IMPORTANT, blocking) Independence rule is not embedded (paths not named) in 18 verification-agent items
Items 3.23, 3.24, 5.29, 5.30, 5.34, 5.35, 6.31, 6.32, 6.36, 6.37, 6.46, 6.47, 6.51, 6.52, 6.60, 6.61, 6.65, 6.66 spawn an rf-qa / rf-qa-qualitative agent with a verbatim prompt. Their prompt says "never read, list, grep into or cite the two forbidden run-1 paths". The prompt never names the paths: a programmatic scan of each item for `TASK-RESEARCH-review-panel-unify-20261113-155942` and `REVIEW-PANEL-UNIFY-RUN2-QUEUED` found zero hits in all 18 (for example L280 item 3.23, L282 item 3.24, L374 item 5.29, L514 item 6.31). A spawned agent has no context, so "the two forbidden run-1 paths" is undefined and the binding independence rule cannot be obeyed or checked. The sibling items 3.18 and 3.19 (L268, L270) and the Gate 1 lens items 3.01-3.15 do name both paths, so this is an inconsistency inside the file, not a template choice. The lens requires the rule to be embedded in every gate item.
Required fix: replace "the two forbidden run-1 paths" in those 18 prompts with the two literal paths, as 3.18 does.

### F-2 (MINOR) Value-ledger items 2.19-2.24 each cover two scope slices
Each of the six items builds one ledger over two slices (for example 2.20 covers slices 03 and 04, which the item itself says hold 10 product defects, 19 harness defects, 20 lessons, 55 tmp-scripts, V1-V30). The pairing is prescribed by research-notes.md rows 19-24 (L183-188), the output is one file per item, and agents write in chunks of 25, so this is accepted as per-artifact, not a hidden batch. Noted only because lens item 6 asks for it.

### Checks passed in Phase 1-3 (evidence)
- Items 1.1-1.3, 2.01-2.24, 3.01-3.26: every item has context, action, output path, a measurable verification clause ("Ensuring ...") and the completion gate sentence "Once done, mark this item as complete" (scan: 185 of 186 items in the whole file carry it; the one without is the Post-Completion item at L633).
- Phase 2 agent prompts are fully embedded (not "see SKILL.md"): each carries the incremental-writing protocol, staleness protocol, R1-R3 shared rules including the independence rule with both literal paths, an ASSIGNMENT, slices to read, code anchors, open items and an output path.
- Concurrency: wave 1 = 18 agents; wave 2 = 6 agents started after at least 6 wave-1 returns (max 18 concurrent); Gate 1 = 15 agents in one message. All under 20.
- No Phase 2 item states a [CODE-CONTRADICTED] or [UNVERIFIED] claim from research-notes.md AMBIGUITIES_FOR_USER as fact: items 2.01, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11, 2.13, 2.15, 2.16 each tag such figures "[UNVERIFIED] until re-derived" or "[CODE-CONTRADICTED] ... verify and correct".

## Findings (Phase 2 deep read, Phase 4-7)

### F-3 (IMPORTANT, blocking) Item 2.18 ref-rule test cannot produce the required evidence under the rules embedded in the same item
Item 2.18 (L205) tells the agent to run `git init` in a scratch repo, "create a branch `feat/review-panel` and then try `feat/review-panel/x`", and record "the exact git error messages". Its embedded preamble R1 (identical in all 18 wave-1 items, L205) says "Never check out, switch, pull, fetch, stash, commit, push or write anywhere except your one output file"; the item's exception covers only "the write-nowhere rule" and says nothing about committing. I ran the procedure in a throwaway `mktemp -d /tmp/b2qa-reftest.*` repo (since deleted): without a first commit, `git branch feat/review-panel` fails with `fatal: not a valid object name: 'master'`, and the second branch fails with `not a valid object name: 'feat/review-panel'`, so the `cannot lock ref ... exists; cannot create` text only appears after `git -c user.name=t -c user.email=t@t commit --allow-empty` (a bare commit also fails with "Author identity unknown"). The item gives no commit step and no identity, and R1 forbids commit, so an agent that obeys the item records the wrong error. Item 5.09 (L328) and item 4.03 (L301) both depend on "the exact git error text recorded by research file 18" and on `cannot lock ref`.
Required fix: in item 2.18, state that inside the scratch repository only, the agent runs `git -c user.name=qa -c user.email=qa@example.invalid commit --allow-empty -m init` before creating the branches (scratch-repo checkout, branch and commit are allowed; nothing in the project repository), and quote that the expected error contains `cannot lock ref`.

### F-4 (IMPORTANT, blocking) Item 5.06 (synth-06) names conflict sets that are outside its read list, and "the run comparison" is undefined
L322 tells the agent to collect "the conflicts C-S1..C-S16 and exposures FX-1..FX-22 of the run comparison". A Grep of `research/scope` shows those ids exist only in `research/scope/02-run-comparison-and-notes.md` (lines 531-595, for example `| C-S1 |` at :531 and `| FX-22 |` at :595). The item's read list is `research/01-*.md` through `18-*.md` plus `gaps-and-questions.md`; it does not include scope slice 02, and a Grep of the task file for `C-S1` finds only L322, so no Phase 2 item is told to carry those 38 ids into a research file. Conflict log (deliverable (c)) can therefore silently omit them. The bare phrase "the run comparison" also invites an agent to search for run-1 material, which the independence rule forbids.
Required fix: add `research/scope/02-run-comparison-and-notes.md` (sections C-S and FX, lines 531-595) to the 5.06 read list by full path, and replace "the run comparison" with "scope slice 02".

### F-5 (MINOR) Wrong symbol name in two "known anchor" hints
Items 2.02 (L173, open item (c)) and 2.15 (L199) cite "`telemetry.py:23` `_REF_TOKEN`". Read of `src/superclaude/cli/review/telemetry.py` shows line 23 is `_ID_TOKEN = r"(?:[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*|P[0-9])\b"` and the symbol `_REF_TOKEN` exists only at `src/superclaude/cli/review/findings.py:29` (Grep). Line number is right, name is wrong; agents re-derive anchors, so minor. Fix: write `telemetry.py:23` `_ID_TOKEN` (same pattern as `findings.py:29` `_REF_TOKEN`).

### F-6 (MINOR) Nested research-agent spawn in fix items 3.17 and 3.22 is not embedded
L266 and L278 let the rf-qa fix agent spawn "ONE targeted research agent per gap" that "follows the incremental file writing protocol ... the documentation staleness protocol ...". Only a one-line description of each protocol is given and the full text sits in items 2.01-2.24, not in these items. Optional path, so minor. Fix: point to the protocol text or embed it.

### F-7 (MINOR) Small prompt wording defects
- Item 5.50 (L439): "edit only the three or five synthesis files named above" while five files are named (synth-05, 06, 07, 09, 10). Say five.
- Item 4.02 (L299): lists `mcp__litellm__context7-*` tools, which `rf-task-researcher` does not have (agent tool list: Tavily, WebFetch, WebSearch), and the fallback note `web-provenance ... reason=<tavily-unavailable|...>` does not cover a Context7 miss.
- Item 4.01 (L297): "both efforts lack a blind judge for E1" is unclear (E2 has a blind judge, E1 does not).
- Item 6.02 (L450): "the I19 size tier ... and the resulting minimum lens counts" relies on template rule I19 that the item does not restate; harmless because the lens count is fixed at 13.

### F-8 (MINOR) Load of Gate 5 agent 4 (item 6.57, L576)
Agent 4 must enumerate by meaning all six value ledgers (19-24), synth-06 to synth-10 and every debate result, while agent 1 has 7 input files. The agent writes in chunks, so it is feasible, but it is the most likely agent to run out of context. Consider splitting the ledgers across two agents (the 20-agent limit allows it: 4 agents now).

## B2 checklist results

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has context + action + output + verification + completion gate | PASS | Scan of all 186 items: 185 contain "Once done, mark this item as complete"; the 186th (L633) ends "Once the summary is complete, mark this item as complete". Every item has an "Ensuring ..." clause. Items without a file output (L156, L162, L617-L637) name the log entry or chat step they produce. |
| 2 | No item relies on an earlier item without restating | FAIL (1 item) | Grep for "see above / as above / previous item / same as / continue from / see Item": 0 hits. Cross-item references (3.21 to 3.20, 5.32 to 5.31, 6.34, 6.49, 6.63, 4.03 to 2.18) all restate the file path. Exception: item 5.06 (F-4). |
| 3 | Agent-spawning items embed full prompts | PASS | 24 + 15 + 15 + 13 + 13 + 12 + 10 + 4 + 5 + 4 + fix and verification agents all carry "pass verbatim" prompts with protocol blocks; only the optional nested spawn in 3.17/3.22 is by reference (F-6). |
| 4 | Specific file paths | PASS | Spot-check of 60+ cited paths and 8 anchors against the repo: all exist (`git cat-file -t` returns `commit` for both 6c0984326 and 4a22d7421; E2 tree paths present via `git ls-tree`; `src/superclaude/cli/review` has 16 modules). Only wrong symbol: F-5. |
| 5 | Measurable verification | PASS | Each item names a file that must exist, a status line, counts, an `F_n = <n>` line, byte-exact halt text or a Grep that must return nothing. Weak spots: "nothing is fabricated" tails and 6.43 "did not read the final report" (not checkable). Minor only. |
| 6 | No batch items | PASS (minor note F-2, F-8) | 24 Phase 2 items = 24 agents, 1 output each; 4 web items; 10 synthesis items; 15 + 15 + 26 + 5 + 4 gate agents each own an item; 12 debate slots each have their own item (identical text hash c88ed4f6 after normalizing slot id); extra debates are generated from 5.49 by the dynamic block. |
| 7 | No item built on [CODE-CONTRADICTED] / [UNVERIFIED] claims | PASS | Grep of 28 figures from research-notes.md AMBIGUITIES_FOR_USER (4,119,747; 216 clusters; TP 21; 13 of 20; 352 passed; 138 / 358; 1 of 3; 0 of 12; 7 of 28; 185 U2; muse-ember; T2bModel01; unpassable-ac ...). Every occurrence is tagged [UNVERIFIED] / [CODE-CONTRADICTED] or is an "expected value to re-confirm". Untagged slice figures in 2.14 (6,523 files, 7,589 lines) are inventory counts, not analysis, so minor. |
| 8 | 20-concurrent-subagent limit | PASS | Largest single message: wave 1 = 18 (L167); wave 2 = 6 after at least 6 wave-1 returns (max 18 concurrent); Gate 1 = 15; Gate 2 = 15; Gate 3 instance a = 13 and instance b = 13 only after all a returned (L480); debates 3 slots per batch; fix agents capped at 20 (L266). |
| 9 | Independence rule embedded in every research-agent and gate item | FAIL | Both literal paths appear in all 24 Phase 2 items, 15 + 15 Gate 1/2 lens items, 26 Gate 3 lens items, 5 Gate 4 items, 4 Gate 5 items, 4 web items, 10 synthesis items, 12 debate items, the 11 single-fix agents (3.17, 3.22, 5.28, 5.33, 6.30, 6.35, 6.45, 6.50, 6.59, 6.64, 6.69), the cross-source agent 6.43 and verification items 3.18/3.19. Missing (paths not named, only "the two forbidden run-1 paths"): 18 verification items, see F-1. Non-agent consolidation items (3.16, 3.21, 5.27, 5.32, 6.29, 6.34 and so on) read only this task's own QA files and carry no rule; accepted. |

## Confidence
Verified: 9/9 checks run with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (grading of issues is mine; checks are complete: all 186 items were either read in full or covered by an explicit programmatic scan of the same text).
Tool engagement: Read: 7 | Grep: 9 | Glob: 0 | Bash: 22 (the large items are only readable through line extraction; each Bash call targeted a specific item, anchor, path or count named above).
Note: Phase 3 items 3.08-3.09, 3.11-3.12, 3.14-3.15, 5.13-5.14, 5.16-5.17, 5.19-5.20, 5.22-5.23, 5.25-5.26 and Gate 3 items 6.17-6.28 and Gate 1/2/4/5 cycle-2 items 6.35-6.67 were checked by structural scan (phrases, output names, independence strings, partition ranges) and by reading their sibling item in full, not by reading every character; their text is generated from the same template as the siblings read in full.

## Summary
- Blocking issues: 3 (F-1 IMPORTANT, F-3 IMPORTANT, F-4 IMPORTANT)
- Minor notes: 5 (F-2, F-5, F-6, F-7, F-8)
- Critical: 0

VERDICT: FAIL

## Required fixes before /task runs
1. F-1: in the 18 verification items listed, replace "the two forbidden run-1 paths" with the literal paths `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` and `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` (copy the wording of item 3.18).
2. F-3: add the scratch-repo initial commit (with `-c user.name/-c user.email`) to item 2.18 and carve it out of R1 for the scratch repository only.
3. F-4: add scope slice 02 (lines 531-595) to the item 5.06 read list and rename "the run comparison".

## QA Complete
