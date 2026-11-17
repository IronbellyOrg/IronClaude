# A.10.5 Qualitative Fix Log, Cycle 1

**Date:** 2026-11-14
**Agent:** rf-qa fix agent (single), fix_authorization: true
**Target:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md`
**Findings in scope:** O-1, O-2, G-1, G-2, O-3, N-13, testing-N/A sentence (source: `qa/qa-task-validation-consolidated.md`, Addendum 2)
**Method:** Read target range, Edit tool only (no sed -i, no scripts), re-read after each edit.

---

## O-1: rule R1 reworded in the Phase 2 research prompts

**Items and lines:** items 2.01-2.18 at lines 171, 173, ..., 205 (odd lines) and items 2.19-2.24 at lines 209-219 (odd lines); line 207 is the Step 2.2 header, not an item. 24 items, one R1 each.

| Edit | Mechanism | Occurrences replaced | Read-back |
|---|---|---|---|
| R1 tail sentence: `Never check out, switch, pull, fetch, stash, commit, push or write anywhere except your one output file.` replaced by `Never check out, switch, pull, fetch, stash, commit, push, create a branch or write in the real repository. Exactly two kinds of writes are allowed: (1) your one output file in the task folder, and (2) scratch files under the one directory /tmp/review-panel-run2-<item number>/ that your ASSIGNMENT names (for example /tmp/review-panel-run2-2.03/), never inside the repository or the task folder; delete that directory before you return, and nothing is ever committed in the real repository. An assignment that names no scratch directory allows no scratch writes.` | Edit replace_all | 24 (Grep before: 24 lines, one per item; Grep after for the old sentence: 0 matches; Grep for `Exactly two kinds of writes are allowed`: 24 lines, 171-205 and 209-219) | Read of lines 175, 183, 185, 199, 203, 205 shows the new sentence in place |
| R1 heading: `(R1) READ-ONLY. ${TASK_DIR}` replaced by `(R1) READ-ONLY in the repository, with two permitted kinds of writes (stated below). ${TASK_DIR}` | Edit replace_all | 24 (Grep after for the new heading: 24; for the old heading: 0) | same |

Every other R1 prohibition (no checkout, switch, pull, fetch, stash, commit, push, no write in the real repository), R2, R3, the E2 `git show` rule and the Python/pytest rules are unchanged.

**Items that need a scratch directory now name one** (each is a single Edit with a one-occurrence old string; Read of the line before, Grep after):

| Item | Line | Change |
|---|---|---|
| 2.03 | 175 | `use a temporary directory under /tmp for fixtures and remove it afterwards` now `use the scratch directory /tmp/review-panel-run2-2.03/ for fixtures and delete it afterwards` |
| 2.07 | 183 | `run only scripts that write nothing in the repository, and tag a figure` now adds `(a script that needs scratch output may use the scratch directory /tmp/review-panel-run2-2.07/, deleted afterwards)` |
| 2.08 | 185 | `use /tmp if a scratch file is unavoidable` now `use the scratch directory /tmp/review-panel-run2-2.08/ if a scratch file is unavoidable` |
| 2.15 | 199 | `using /tmp for fixtures` now `using the scratch directory /tmp/review-panel-run2-2.15/ for fixtures and deleting it afterwards` |
| 2.17 | 203 | `use /tmp for fixtures` now `use the scratch directory /tmp/review-panel-run2-2.17/ for fixtures and delete it afterwards` |
| 2.18 | 205 | see next paragraph |

**Item 2.18 (line 205):** the sentence `This is the ONE explicit exception to rule R1 (for this test only it overrides R1's bans on commit, branch creation and writing outside your output file): create a temporary scratch repository with mktemp -d /tmp/review-panel-ref-test.XXXXXXXX (always under /tmp, never inside` was reworded to say this is the ONE item whose scratch writes additionally include scratch git repositories: commit and branch creation are allowed only inside `/tmp/review-panel-run2-2.18/`, R1's bans stay in force for the real repository and everywhere else; the agent runs `mkdir /tmp/review-panel-run2-2.18` and then `mktemp -d /tmp/review-panel-run2-2.18/ref-test.XXXXXXXX` for each scratch repository. The cleanup clause changed from `rm -r of those two exact /tmp/review-panel-ref-test.* directories` to `rm -r /tmp/review-panel-run2-2.18 only, which removes both scratch repositories`, and the closing R1 clause now reads `outside your output file and /tmp/review-panel-run2-2.18/`. Grep `review-panel-ref-test` in the task file: 2 matches before, to be re-confirmed 0 after (see check at the end of this log). Grep `review-panel-run2-2\.(03|07|08|15|17|18)/` shows every named scratch path (2.03 at 175, 2.07 at 183, 2.08 at 185, 2.15 at 199, 2.17 at 203, 2.18 at 205 four times), plus the example `2.03` in the R1 sentence of each item.

**Status: FIXED.**

---

## O-2: ripgrep-safe pattern `\[PENDING-ADJUDICATION` and the errored-Grep rule

Each edit used the Edit tool with a one-occurrence old string (no replace_all), after a Read of the line. The Grep-as-search-pattern uses were found by Grep `.{0,200}\[PENDING-ADJUDICATION.{0,200}` (24 hits on 20 lines before the edits). The other hits (lines 324, 338, 340, 344, 346, 350, 352, 356, 358, 364, 372, 384, 396, 717 and the marker-definition text in line 439) describe the marker `[PENDING-ADJUDICATION: <slug>]` and are not Grep patterns, so they were left as they are.

| Item | Line | Change |
|---|---|---|
| 5.11 (Gate 2 aggregation) | 336 | `use Grep to count the strings [PENDING-ADJUDICATION: per file` became `use Grep with the pattern \[PENDING-ADJUDICATION: (escaped bracket, because an unescaped [ is rejected by ripgrep as an unclosed character class; a Grep that errors is NOT a pass: rerun it until it returns a normal result or an empty result without an error message) to count the markers per file` |
| 5.50 (fold agent), inside the verbatim agent prompt | 439 | `a Grep for [PENDING-ADJUDICATION in the synthesis folder MUST return nothing` became `a Grep with the pattern \[PENDING-ADJUDICATION (escaped bracket) in the synthesis folder MUST return nothing, and a Grep that errors is NOT a pass: rerun it until ...` |
| 5.50, executor-level check after the agent returns | 439 | `(verify with Grep after the agent returns; if one remains,` became `(verify with Grep after the agent returns, using the escaped pattern \[PENDING-ADJUDICATION; a Grep that errors is NOT a pass: rerun it until ...; if one remains,` |
| 6.01 (assembler prompt, item 7 of the assembly rules) | 448 | `and for [PENDING-ADJUDICATION, ADJUDICATION-FOLD-PENDING` became `and for \[PENDING-ADJUDICATION (escaped bracket; a Grep that errors is NOT a pass: ...), ADJUDICATION-FOLD-PENDING`. The item's later executor Grep (`...|PENDING-ADJUDICATION|ADJUDICATION-FOLD-PENDING` with no bracket) was already valid and is unchanged. |
| 6.03 (Gate 3 template-conformance lens a) | 454 | lens checklist c: `[PENDING-ADJUDICATION` became `\[PENDING-ADJUDICATION` plus the errored-Grep sentence |
| 6.16 (Gate 3 template-conformance lens b) | 482 | lens checklist c: same change |
| 6.68 check 19 (final validation checklist) | 604 | `[PENDING-ADJUDICATION` became `\[PENDING-ADJUDICATION` plus the errored-Grep sentence. In the same check, the Grep pattern `[CONTRADICTION` was also escaped as `\[CONTRADICTION` (same unclosed-class defect, same sentence, one character); this one-character extension was not in the finding, so it is reported here. |

**Scan and read-back proving it:**
- Grep `\[PENDING-ADJUDICATION` on the task file (the new escaped pattern) returned a normal result, not a regex error: 20 matching lines (count mode). The matching lines include every hit above plus the marker-definition lines.
- Grep `.{60}\\\[(PENDING-ADJUDICATION|CONTRADICTION).{0,200}` (matches the backslash-escaped form) returned exactly 7 hits on 6 lines: 336, 439 (two hits), 448, 454, 482, 604, each showing the escaped pattern and the errored-Grep sentence in place.
- Grep `[^\\]\[PENDING-ADJUDICATION[^:]` (bare bracket not followed by a colon) returns 1 line: 439, the sentence `no [PENDING-ADJUDICATION marker ... remains anywhere under synthesis/`, which names the marker and is followed in the same sentence by the instruction to verify with the escaped pattern. That is intended.
- The remaining `[CONTRADICTION` mentions (lines 448 and 512) are marker descriptions, not Grep patterns.
- Observation, not changed (outside the listed items): the research item that extracts undecidable conflicts (line 396) says `use Grep for the marker` without naming a pattern.

**Status: FIXED.**

---

## G-1: Gate 5 and the Gate 3/4 removals

**Items and lines:** 6.54 (570), 6.55 (572), 6.56 (574), 6.57 (576), 6.58 (580), 6.59 (582), 6.60 (584), 6.61 (586), 6.62 (588), 6.64 (594), 6.65 (596), 6.66 (598), 6.67 (600). Items 6.63 (592) was not changed (it only carries forward the cycle 1 table). No item was added or renumbered; Gate 5 is still 4 agents.

| Required fix | What changed | Where |
|---|---|---|
| (a) all four agents also read the Gate 3 and Gate 4 fix logs and the consolidated phase 6 findings | New prompt block `EARLIER-GATE REMOVALS`, inserted before `You verify that NO distinct finding` in each agent prompt. It names `qa/qa-fix-log.md`, `qa-fix-log-c2.md`, `qa-fidelity-fix-log-c1.md`, `qa-fidelity-fix-log-c2.md` (the actual names used in the Gate 3 and Gate 4 fix items at task file lines 512-528 and 548-564) and the consolidated files `qa-consolidated-findings-phase6.md`, `qa-consolidated-findings-phase6-c2.md`, `qa-fidelity-consolidated-findings.md`, `qa-fidelity-consolidated-findings-c2.md`, "when they exist" (a `No fix required` or `Skipped` file lists no removal). | 6.54-6.57, one Edit each (anchored on each item's own assigned-file list) |
| (b) third allowed disposition `JUSTIFIED-REMOVED: removed as false or unsupported by Gate N fix, cite the fix-log entry and the code evidence` | Agents: fourth classification `JUSTIFIED-REMOVED` (not an omission) only with the fix-log entry AND the code evidence quoted by it; otherwise the finding stays OMITTED. Replace_all of the classification sentence, the output table header and the Summary list: 4 occurrences each (lines 570-576 only, counted before the edit with Grep: 4/4/4). Consolidation 6.58: new Proposed-handling value `JUSTIFIED-REMOVED: removed as false or unsupported by Gate N fix, cite the fix-log entry and the code evidence`, a JUSTIFIED-REMOVED check (every entry, at least 10 when more) that opens the fix-log entry and its code evidence, and an entry without code evidence becomes an omission row. Fix agents 6.59 and 6.64: JUSTIFIED-REMOVED listed as the third allowed disposition and in the fix-log format. | 6.54-6.59, 6.64 |
| (c) fix agent must not re-add a claim a Gate 3/4 log removed as false unless the log's code evidence is shown wrong | In 6.59 and 6.64 prompts: `you MUST NOT re-add such a claim unless your own code evidence (file:line at HEAD, or git path:line at the E2 tip 6c0984326cbb8fb06c4a36065de58b171d3f8175 read through git show or git ls-tree) shows the evidence in that log is wrong`, recorded in the fix log. | 6.59, 6.64 |
| (c) every recovered claim re-checked against code or the E2 tip by the fix agent and by the Gate 5 verification agents | Fix agents: must check each recovered claim against code before writing it, else tag `[UNVERIFIED]` and move it to Open Questions; each RECOVERED entry carries `code-checked: <file:line or git path:line>` (also in the Ensuring clause). Verification agents: new `CODE RECHECK (mandatory)` clause (replace_all, 2 occurrences for the structural pair 6.60/6.65 and 2 for the content pair 6.61/6.66, counted by Grep before the edit) that re-verifies every RECOVERED claim against code at HEAD or `git show` at the E2 tip, marks a claim contradicted by code (or removed-as-false in a log with evidence that still holds) STILL-OPEN, and writes the line `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>`; the Ensuring clause of each of the four verification items now requires that line. | 6.59-6.61, 6.64-6.66 |
| (c) cycle control records the count of recovered claims verified against code | 6.62 and 6.67 now copy the `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>` line of each verification report (`0 of 0` for a skipped one) and their sum into `gate5-cycle-control.md`; a recovered claim not verified against code counts as open in `F_1` / `F_2`; the Ensuring clause requires the count. | 6.62, 6.67 |

**Read-back:** Grep counts after the edits: `EARLIER-GATE REMOVALS: also read` 4; `CODE RECHECK (mandatory)` 4; `JUSTIFIED-REMOVED` 27 mentions in total; item count 187, none checked; Read of lines 570 and 580 after the edits shows the new text in place and the surrounding prompts intact.

**Not done (outside the consolidated finding, noted for the owner):** the sufficiency report's optional extra suggestion of a new 6.68 checklist item ("no claim removed in the Gate 3/4 fix logs reappears") was not added, because the consolidated findings list only (a) to (c) and the rule is not to add items.

**Status: FIXED.**

---

## G-2: Gate 5 enumeration completeness and load balance

**Items and lines:** 6.54-6.57 (570-576), 6.58 (580).

| Required fix | What changed |
|---|---|
| (a) each agent writes its numbered enumeration to its own file with a per-assigned-file count | Each prompt now has an `ENUMERATION FILE` block: `.../qa/qa-anti-omission-enumeration-<n>.md` (n = 1..4), created first, one numbered list per assigned file, each list ending with the line `COUNT <file name>: <n>`; the per-file counts are copied into the agent's report as a `### Per-File Counts` table. The old clause `write the enumeration to your report incrementally, file by file` (4 occurrences, replace_all) now points to the enumeration file. The enumeration file is added to each item's Output field (`writing ...report-<n>.md and its enumeration file ...enumeration-<n>.md`) and to the Ensuring clause (4 occurrences, replace_all). Agent 4 additionally has one enumeration entry per ledger row. |
| (b) consolidation runs an independent recount on three files per agent, chosen by the consolidating side, and a shortfall above 10 percent re-runs that agent's partition and counts as a blocking finding | Item 6.58 item (6): `INDEPENDENT RECOUNT`: the consolidating executor chooses three assigned files per agent (prefers the three largest by `wc -l`), recounts with read-only Grep/`wc`, writes `AGENT <n> FILE <name> ENUMERATED=<e> RECOUNT=<r>`; `e` below 0.9 times `r`, a missing enumeration file or a missing COUNT line is blocking finding `P6A-RC-<n>`, counted in F_0 (`(4)` now says so), and that agent's whole partition is re-run inside 6.58 with `-rerun` output names. |
| (c) rebalance so no agent carries more than about one quarter of the enumerable lines; state line counts per agent in the item; move work from agent 4 | Static rebalance by file (agent 4 lost synth-06, synth-07, synth-09, synth-10 and the debate results): agent 1 = research 01-05, web-01, web-02, synth-05, synth-06, synth-07, debate results; agent 2 = research 06-11, web-03, web-04, synth-04, synth-09, synth-10; agent 3 = research 12-18, gaps log, synth-01, synth-02, synth-03; agent 4 = value ledgers 19-24 and synth-08. The conflict-log/debate-outcome check moved from agent 4's prompt to agent 1's. **Line counts per agent could not be stated at build time** (research, synthesis and debate files do not exist yet; only the 12 scope slices do), so item 6.54 now opens with a PARTITION CHECK that measures them with one `wc -l`, writes lines and share per agent to `qa/gate5-partition.md`, and moves whole files (or the second half of one file by line range) from the heaviest to the lightest agent until none exceeds 30 percent (target about one quarter), editing the file lists before the prompts are passed. Items 6.55-6.57 point to that file. |

**Read-back:** Read of line 570 and line 580 after the edits; Grep count `qa-anti-omission-enumeration-` paths: enumeration-1 x3, -2 x2, -3 x2, -4 x2 (item Output field plus prompt block, plus the 6.58 reference); `gate5-partition.md` mentioned 7 times; Gate 5 is still 4 agents (items 6.54-6.57); `- [ ]` count 187.

**Status: FIXED, with one deviation from the letter of (c):** the per-agent line counts are measured at execution (6.54) instead of being stated in the item, because they cannot be known now.

---

## O-3: nested `.claude` staging check

**Items and lines:** Step 7.2 (line 621), the Post-Completion verification item (line 629), the last Post-Completion re-stage item (line 637).

| Item | Change |
|---|---|
| 7.2 | After `git add .dev/tasks > /dev/null`, a new check `git diff --cached --name-only \| grep -E '(^\|/)\.claude/'` (must print nothing; any hit is a HALT: `git restore --staged <path>`, record in the Phase 7 Findings of the Task Log, do not commit, tell the user, STOP; the empty `.claude/agent-memory` directories are left in place). `with the three results` became `with the four results`; the unstage instruction `git restore --staged .claude` became `git restore --staged <path>` (root or nested path) with both checks re-run. |
| Post-Completion verification (Verify all task outputs) | The same read-only check appended after the Glob verification, same HALT handling. |
| Last re-stage item | The same check added to the repeated checks and to the final re-check after the last `git add .dev/tasks`; `three results` became `four results`; unstage instruction generalised to `<path>`. |

The empty directories `.claude/agent-memory` under the task folder and under `qa/` were not deleted and nothing under any `.claude/` directory was touched. `find` shows no file under any `.claude` directory of the task folder (the `.claude/agent-memory/rf-qa` directory is an empty directory in the task folder's `.claude`, not created by this fix).

**Status: FIXED.**

---

## Testing-N/A sentence

**Line 74 (Task Overview, OWNER SCOPE CHANGE paragraph):** appended `Testing requirements: not applicable (documentation-only research task; the only commands run are read-only recounts).` after `This task performs no implementation, merge, worktree creation, branch creation, commit or push.` Read of line 74 after the edit confirms it. Note for the owner: the sentence is the one the consolidated findings prescribe; the Phase 2 items 2.03, 2.07, 2.08, 2.15, 2.17 and 2.18 also use scratch fixtures under `/tmp/review-panel-run2-<item>/` and item 2.18 creates scratch git repositories there, which the new R1 allows and names.

**Status: FIXED.**

---

## N-13: Gate 3 lens-report count in final validation checklist item 21

**Item and line:** item 6.68 at line 604, checklist item 21 (inside the verbatim agent prompt).

**Change (single Edit, one occurrence, after a Read of the line):** `Gate 3 (13 lens reports plus consolidation)` became `Gate 3 (13 lens reports (26 in split mode) plus consolidation)`.

**Proof:** Grep `13 lens reports` on the task file returns one match, line 604; the Edit tool reported success on a one-occurrence replacement.

**Status: FIXED.**

---

## Final integrity checks (read-only, after all edits)

| Check | Result |
|---|---|
| Task file line count | 724 (unchanged; all edits were in-line) |
| `- [ ]` items / pre-checked items | 187 / 0 |
| Literal `TODO`, `TBD`, `FIXME` in the task file | 0; the written form `T[O]DO\|T[B]D\|FIX[M]E` is intact (5 occurrences, none added) |
| Byte-exact halt strings | `[HALT-MONOTONICITY] \|F\|=` 14 occurrences, `Regression detected on Item X.Y, previously PASS at cycle` 13 occurrences (the 13 places the consolidated findings mention); none edited |
| Independence literals | both run-1 path strings still present (153 and 158 occurrences); no edited item lost them |
| Old R1 sentence `write anywhere except your one output file` | 0 left |
| `review-panel-ref-test` | 0 left |
| `\[PENDING-ADJUDICATION` Grep (new pattern) | normal result, 20 matching lines, no regex error |
| Files under any `.claude/` directory in the task folder | none (empty directories only; not touched) |
| Forbidden run-1 folder and RUN2-QUEUED note | not opened, listed or searched |

## Summary per finding

| ID | Status |
|---|---|
| O-1 | FIXED (R1 reworded in 24 items by 2 replace_all edits of 24 occurrences each; 5 items name their scratch directory; item 2.18 exception aligned) |
| O-2 | FIXED (6 items, 7 Grep-pattern sites; new pattern returns a normal result; errored-Grep-is-not-a-pass sentence added) |
| G-1 | FIXED (items 6.54-6.62, 6.64-6.67) |
| G-2 | FIXED with one deviation: per-agent line counts are measured at execution in 6.54 (cannot be stated at build time); partition rebalanced statically and capped at 30 percent |
| O-3 | FIXED (7.2, Post-Completion verification, last re-stage item) |
| N-13 | FIXED (item 6.68 checklist item 21) |
| Testing-N/A sentence | FIXED (Task Overview, line 74) |

---

