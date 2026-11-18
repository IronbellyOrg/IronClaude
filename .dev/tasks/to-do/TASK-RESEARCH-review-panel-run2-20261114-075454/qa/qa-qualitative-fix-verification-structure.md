# QA Report - A.10.5 Fix Cycle 1 Verification (structure and regression)

**Topic:** review-panel run 2 task file, A.10.5 qualitative fix cycle 1
**Date:** 2026-11-14
**Phase:** fix-cycle (lens: fix-verification, structure and regression)
**Fix authorization:** false (report only; task file not edited)

---

## Per-finding results (appended below as verified)

Method: Bash `grep -n/-c/-F`, `sed -n`, Grep tool, Read. Every claim below was re-read from the task file in this review; the fix log was used only to know where to look.

### Finding 1. O-1 (R1 versus scratch fixtures): FIXED

Evidence:
- `(R1)` occurs 24 times in the whole file, on lines 171, 173, ..., 205 and 209, ..., 219 (the odd lines; line 207 is the Step 2.2 header). Item tags on those lines are 2.01 through 2.24 (checked with `grep -o '^- \[ \] (Item [0-9.]*'`). No `(R1)` outside lines 171-219.
- All 24 lines carry the heading `(R1) READ-ONLY in the repository, with two permitted kinds of writes (stated below).` and the identical full R1 sentence (fixed-string `grep -cF` of the complete sentence on each of the 24 lines: 1 each, 24 of 24): "Never check out, switch, pull, fetch, stash, commit, push, create a branch or write in the real repository. Exactly two kinds of writes are allowed: (1) your one output file in the task folder, and (2) scratch files under the one directory `/tmp/review-panel-run2-<item number>/` that your ASSIGNMENT names ..., never inside the repository or the task folder; delete that directory before you return, and nothing is ever committed in the real repository. An assignment that names no scratch directory allows no scratch writes."
- Old wording absent: `write anywhere except your one output file` 0 matches; `(R1) READ-ONLY. ` 0 matches; `review-panel-ref-test` 0 matches.
- Scratch directory named in the item text: 2.03 line 175 (`/tmp/review-panel-run2-2.03/`), 2.07 line 183 (`/tmp/review-panel-run2-2.07/`, "deleted afterwards"), 2.08 line 185 (`/tmp/review-panel-run2-2.08/`), 2.15 line 199 (`/tmp/review-panel-run2-2.15/`), 2.17 line 203 (`/tmp/review-panel-run2-2.17/`), 2.18 line 205 (`/tmp/review-panel-run2-2.18/`, four times).
- Item 2.18 (line 205) now says "This is the ONE item whose scratch writes (the second permitted kind of write in rule R1) additionally include scratch git repositories: for this test only, a commit and branch creation are allowed inside the scratch directory `/tmp/review-panel-run2-2.18/`, and R1's bans ... stay in force for the real repository and everywhere else"; it creates the dir with `mkdir /tmp/review-panel-run2-2.18`, makes repos with `mktemp -d /tmp/review-panel-run2-2.18/ref-test.XXXXXXXX`, deletes with `rm -r /tmp/review-panel-run2-2.18`, and ends "outside your output file and `/tmp/review-panel-run2-2.18/`". Consistent with R1.
- `/tmp/` appears only on lines 171-205 (Grep -o -n over the whole file); no other phase mentions it, so nothing outside Phase 2 conflicts.
- Phase 2 text scan for other write bans (`never write`, `write nothing`, `read-only`, ...): the remaining hits are "snippets that write nothing in the repository" (each followed by the scratch directory in 2.03, 2.15, 2.17) and read-only recount instructions; none forbids what another item requires.

Minor note (not blocking): in 2.18 "R1's bans on ... checkout ... stay in force ... everywhere else" could be read as banning `git checkout` inside the scratch repos; the item only asks for `git init`, an initial commit and branch creation, so nothing required is forbidden.

### Finding 2. O-2 (ripgrep-safe marker pattern): FIXED

Evidence:
- I ran the Grep tool on the task file with pattern `\[PENDING-ADJUDICATION`: normal result, 20 matching lines, no regex error. Pattern `\[CONTRADICTION`: normal result, 3 matching lines, no regex error (so the extra escape the fix agent made is valid).
- Escaped Grep-pattern sites (Grep -o -n for `\\\[(PENDING-ADJUDICATION|CONTRADICTION)`): line 336 (item 5.11), line 439 (item 5.50, twice), line 448 (item 6.01), line 454 (item 6.03), line 482 (item 6.16), line 604 (item 6.68 check 19, both `\[PENDING-ADJUDICATION` and `\[CONTRADICTION`). Each carries "a Grep that errors is NOT a pass: rerun it until it returns a normal result or an empty result without an error message" (5.11 also gives the unclosed-character-class reason; 5.50 has it in the agent prompt and in the executor check).
- Unescaped `[PENDING-ADJUDICATION` / `[CONTRADICTION` (Grep `[^\\]\[(PENDING-ADJUDICATION|CONTRADICTION)`, 20 hits on lines 324, 338, 340, 344, 346, 350, 352, 356, 358, 364, 372, 384, 396, 439, 448, 512, 717): I read about 160 characters of context for each. All are descriptions of the marker `[PENDING-ADJUDICATION: <slug>]` or `[CONTRADICTION: <...>]`, not Grep patterns. The hit on line 439 ("no `[PENDING-ADJUDICATION` marker ... remains") is followed in the same sentence by the instruction to verify with the escaped pattern. Line 396 says "use Grep for the marker" with no pattern named (executor chooses; minor).
- The pattern `T[O]DO|T[B]D|FIX[M]E|PLACEHOLDER` used in the same items is a valid balanced class and is still present.
- Control test: the Grep tool on the unescaped pattern `[PENDING-ADJUDICATION` is rejected (error `invalid character class range, the start must be <= the end`), which confirms the defect existed. Minor wording note: item 5.11 (line 336) calls it "rejected ... as an unclosed character class"; the observed message here is a different regex error. The conclusion (rejected, so an error is not a pass) is right; not blocking.

### Finding 3. G-1 (Gate 5 and earlier-gate removals): FIXED

Evidence (task file lines):
- (a) All four anti-omission agents read the Gate 3 and Gate 4 fix logs and consolidated findings: block `EARLIER-GATE REMOVALS: also read, when they exist, ...` is in items 6.54 (line 570), 6.55 (572), 6.56 (574), 6.57 (576), 1 each (Grep -nF). It names `qa-fix-log.md`, `qa-fix-log-c2.md`, `qa-fidelity-fix-log-c1.md`, `qa-fidelity-fix-log-c2.md` and `qa-consolidated-findings-phase6.md`, `qa-consolidated-findings-phase6-c2.md`, `qa-fidelity-consolidated-findings.md`, `qa-fidelity-consolidated-findings-c2.md`.
- File-name match with the writers: Gate 3 fix items write `qa/qa-fix-log.md` (item 6.30, line 512) and `qa/qa-fix-log-c2.md` (item 6.35, line 524); Gate 4 fix items write `qa/qa-fidelity-fix-log-c1.md` (item 6.45, line 548) and `qa/qa-fidelity-fix-log-c2.md` (item 6.50, line 560). Consolidated findings: `qa-consolidated-findings-phase6.md` is written at line 510-512 and `-phase6-c2.md` at 522-524; `qa-fidelity-consolidated-findings.md` at 546-548 and `-c2.md` at 558-560. All eight names match (Grep -nF per name). No name drift.
- (b) `JUSTIFIED-REMOVED` exists as a disposition: classification in agents (lines 570, 572, 574, 576), consolidation value and check in 6.58 (line 580: "JUSTIFIED-REMOVED: removed as false or unsupported by Gate N fix, cite the fix-log entry and the code evidence" and the "JUSTIFIED-REMOVED CHECK"), fix agents 6.59 (582) and 6.64 (594), verifiers (584, 586, 596, 598).
- (c) Fix agent cannot re-add: 6.59 (line 582) and 6.64 (line 594) each contain "you MUST NOT re-add such a claim unless your own code evidence (file:line at HEAD ..., or git path:line at the E2 tip `6c0984326cbb8fb06c4a36065de58b171d3f8175` read through `git show` or `git ls-tree`) shows the evidence in that log is wrong, and you then record that code evidence in the fix log"; each recovered claim must be checked against that code or E2 tip first, else `[UNVERIFIED]` and Open Questions; fix-log entries carry `code-checked: <file:line or git path:line>` (1 each on 582 and 594). The E2 SHA is the same value 126 times in the file (one distinct value).
- Verifiers re-check recovered claims against code: `CODE RECHECK (mandatory)` appears once each in items 6.60 (584), 6.61 (586), 6.65 (596), 6.66 (598); text read on 584: "for EVERY RECOVERED entry re-verify the recovered claim against the code at HEAD ... or ... `git show 6c09843...:<path>` or `git ls-tree` (not only against the research or synthesis file)"; a contradicted claim, or one removed as false in a log whose code evidence still holds, is STILL-OPEN.
- Cycle control records the count: `RECOVERED_VERIFIED_AGAINST_CODE=<k> of <m>` is in 6.62 (line 588) and 6.67 (line 600), copied per verification report with a sum into `gate5-cycle-control.md`; "a recovered claim that a verifier reports as not verified against code is counted as open in `F_1`" (588) and `F_2` (600).
- Coherence check I made: when a Gate 3/4 fix log lists a removal without quoting code evidence, an agent classifies the finding OMITTED (570-576), the fix agent's JUSTIFIED-REMOVED path is closed (it needs quoted evidence), and the MUST NOT re-add clause applies only to claims whose log quotes code evidence ("such a claim"); the fix agent may then recover after its own code check. No deadlock.

### Finding 4. G-2 (enumeration completeness and load balance): FIXED, with the already-reported deviation on (c); one new defect found (see N-1 below)

Evidence:
- (a) Each agent writes its enumeration file: `qa/qa-anti-omission-enumeration-<n>.md`, n = 1..4, appears twice on each of lines 570, 572, 574, 576 (Output field and prompt block). Each prompt has `ENUMERATION FILE: ... FIRST ACTION: create it with a header; then one numbered list of distinct findings per assigned file, each list ending with the line `COUNT <file name>: <n>``; `COUNT <file name>: <n>` occurs twice on each of those four lines. The per-file counts are copied into a `### Per-File Counts` table "equal to the `COUNT` lines of your enumeration file". Each item's Ensuring clause requires the enumeration file with a COUNT line for every assigned file.
- (b) Independent recount in item 6.58 (line 580), sub-check (i) INDEPENDENCE RECOUNT: consolidating side picks three assigned files per agent ("the choice never comes from the enumerating agent; prefer the three largest by `wc -l`"), recounts with read-only Grep or `wc`, writes `AGENT <n> FILE <name> ENUMERATED=<e> RECOUNT=<r>`; "a shortfall above 10 percent (`e` below 0.9 times `r`), a missing enumeration file or a missing `COUNT` line is a blocking finding `P6A-RC-<n>` (Blocking Y, counted in F_0 ...)"; that agent's partition is re-run with `-rerun.md` output names. Mechanism is executable (counts of table rows, headings or numbered entries; the item asks for the method per file).
- (c) Partition mechanism is executable and runs before the agents spawn: item 6.54 (line 570) opens "run the PARTITION CHECK before any Gate 5 agent is spawned": one read-only `wc -l` over every Gate 5 input, sum per agent, write lines and share per agent to `qa/gate5-partition.md`, move whole files (or the second half of a file by line range) from the heaviest to the lightest agent until none exceeds 30 percent (target about one quarter), edit the assigned-file lists in items 6.54-6.57 before they are passed, record every move. 6.54 is the first Gate 5 item, so the check precedes the single-message spawn of all four. `gate5-partition.md` is referenced on lines 570 (three times), 572, 574, 576, 580.
- Build-time claim "the research, synthesis and debate files do not exist at build time" is true: the folder holds only `research/research-notes.md`, `research/scope`, an empty `synthesis/` and an empty `reviews/adversarial` (ls, run in this review). So measuring at execution is the only possible way; the deviation from the letter of (c) ("state the line counts per agent in the item") is justified.
- File-name consistency: static partition in 6.54 (agent 1 = research 01-05, web-01, web-02, synth-05, synth-06, synth-07, debate results; agent 2 = research 06-11, web-03, web-04, synth-04, synth-09, synth-10; agent 3 = research 12-18, gaps log, synth-01 to synth-03; agent 4 = value ledgers 19-24 and synth-08) equals the per-agent "Assigned input files" lists in items 6.54-6.57 and their titles. Coverage is complete and disjoint: research 01-24, web-01 to web-04, gaps log, synth-01 to synth-10 (agent 4 loses synth-06, 07, 09, 10 and the debates). Enumeration file names in 6.58 (`-1.md` to `-4.md`, and `-<n>-rerun.md`) match the names in 6.54-6.57.
- Gate 5 is still four agents (items 6.54-6.57, one spawn each; header of Step 6.9 says 4 rf-analyst). The only addition is the conditional re-run in 6.58 (at most 4 spawns, after the four return; well below 20).
- Minor notes: (1) item 6.57's prompt says synth-06, 07, 09, 10 and the debates "are assigned to agents 1 and 2", which can go stale after a partition move (the same sentence points to `gate5-partition.md`, so it is self-correcting); (2) item 6.54 is now 9,194 bytes (above the 2-7 KB band) because it combines the partition check with agent 1's spawn.

### Finding 5. O-3 (nested `.claude` staging guard): FIXED

Evidence:
- The guard `git diff --cached --name-only | grep -E '(^|/)\.claude/'` is present on line 621 (Step 7.2), line 629 (Post-Completion "Verify all task outputs"), and twice on line 637 (last re-stage item: the repeated checks and the final re-check after the last `git add .dev/tasks`). Grep -noF count: 621 x1, 629 x1, 637 x2.
- HALT handling on each: "any hit is a HALT: unstage the path with `git restore --staged <path>`, record it in the ### Phase 7 Findings section (629: "in the Task Log"), do not commit, tell the user and STOP; the empty `.claude/agent-memory` directories in the task folder are left in place". Line 637 repeats it, and its final re-check says "(both MUST print nothing)".
- Syntax: I ran the exact command in the worktree: exit code 1 (no hit, no syntax error; 2 would mean a bad expression). Against a test stream `a/b`, `.claude/x`, `foo/.claude/y`, `z.claude/q` it prints `.claude/x` and `foo/.claude/y` only, so it catches root and nested `.claude` and not `z.claude/q`. The staged index currently holds 0 paths.
- The empty directories are untouched: `find` under the task folder lists `.claude/agent-memory/rf-qa` and `qa/.claude/agent-memory/{rf-qa,rf-analyst}` as directories, and `find -path '*/.claude/*' -type f` prints nothing.
- Minor note: line 621 now says "with the four results" but its closing sentence still says "cannot be marked as done until the three checks are recorded" (stale count; nit, not blocking).

### Finding 6. N-13 and the testing-N/A sentence: FIXED

- N-13: line 604 (item 6.68, checklist item 21) reads "Gate 3 (13 lens reports (26 in split mode) plus consolidation)"; Grep `13 lens reports` returns only line 604.
- Testing N/A: line 74 (Task Overview, OWNER SCOPE CHANGE paragraph) ends "Testing requirements: not applicable (documentation-only research task; the only commands run are read-only recounts)." Present once.
- Minor note: that sentence overstates "the only commands run are read-only recounts": Phase 2 items create scratch fixtures and scratch git repos under `/tmp/review-panel-run2-<item>/`, and Phase 7 runs `git add .dev/tasks`. The wording came from the consolidated findings verbatim; the item texts are authoritative and say what is allowed. Not blocking.

### Finding 7. Regression scan over the whole file

| # | Check | Result | Evidence |
|---|---|---|---|
| 7.1 | 724 lines | PASS | `wc -l` = 724 |
| 7.2 | 187 `- [ ]` items, none checked, none nested | PASS | `grep -c '^- \[ \] '` = 187; `^- \[x\]` = 0; `^\s+- \[` = 0; no other `- [` form |
| 7.3 | Item numbers contiguous | PASS | tags 2.01-2.24 (24), 3.01-3.26 (26), 4.01-4.04 (4), 5.01-5.50 (50), 6.01-6.70 (70) = 174 tagged; awk order/gap check printed nothing; 13 untagged items (lines 156, 159, 162, 228, 617, 621, 625, 629, 631, 633, 635, 637, 639) = 187 |
| 7.4 | Halt messages unchanged and consistent | PASS | `Regression detected on Item X.Y, previously PASS at cycle {1,2,N}, now FAIL. Halt overrides monotonicity check.` on 13 lines (224, 272, 284, 334, 378, 390, 444, 518, 530, 554, 566, 588, 600), 0 em-dash variants; `[HALT-MONOTONICITY] |F|=<n|F_1|F_2>` on 14 lines (those 13 plus 129); no variant forms |
| 7.5 | Placeholder patterns | PASS | `T[O]DO\|T[B]D\|FIX[M]E` written form 5 times; raw `TODO\|TBD\|FIXME` 0 matches |
| 7.6 | Every spawning item names both independence paths | FAIL (1 item) | Awk over all 151 spawn-mentioning items: both `TASK-RESEARCH-review-panel-unify-20261113-155942` and `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md` present in all except item 6.58 (line 580), which now conditionally spawns agents and has neither literal (item 5.11 was a false hit on the word "rerun" from the O-2 sentence; it spawns nothing). Totals in file: 153 and 153 occurrences. See N-1 |
| 7.7 | No duplicated paragraphs | PASS | `sort \| uniq -d` over lines longer than 200 characters: 0; duplicate 600-character item prefixes: 0 |
| 7.8 | No item spawns more than 20 agents | PASS | Max `subagent_type` count per item is 3 (line 195); Phase 2 wave rules (lines 128, 207) keep concurrency at or below 20; 6.58 re-run is at most 4 spawns |
| 7.9 | Gate 5 still 4 agents | PASS | items 6.54-6.57, one spawn each; Step 6.9 header says 4 rf-analyst; final validation item 21 (line 604) still says "Gate 5 (4 anti-omission reports)" |
| 7.10 | No stale reference to the old Gate 5 partition | PASS | only line 570 names the agent 4 file list (`value ledgers 19-24 and synth-08`); no other line names the old assignment |
| 7.11 | No new unverified claim stated as fact | PASS with notes | New facts checked: scratch dir names (consistent), file names (match writers), "files do not exist at build time" (true, ls), guard syntax (run). Notes only: the "unclosed character class" cause (5.11) and the "only read-only recounts" sentence (line 74), both minor |
| 7.12 | `.claude` hygiene | PASS | no file under any `.claude` dir of the task folder; staged index empty (0 paths); run-1 folder and RUN2-QUEUED note not opened by me |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| N-1 | IMPORTANT (blocking) | Item 6.58, line 580, sub-check (i) INDEPENDENT RECOUNT | The fix for G-2 added a conditional agent spawn to the consolidation item: "spawn ONE Agent (subagent_type `rf-analyst`) with the verbatim prompt of Item 6.5x for that agent ... but with the output paths `...-rerun.md`". The item contains neither independence path literal (`TASK-RESEARCH-review-panel-unify-20261113-155942`, `REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`; Grep -oF on line 580 returns 0 for both, and 0 for `INDEPENDENCE`), and the prompt is a by-reference copy of another item's prompt with a manual path substitution, not embedded. This breaks the check "every item that spawns an agent names both independence paths", BUILD-REQUEST.md line 102 ("Builder MUST embed the complete agent prompt ... and the shared rules block (... independence rule ...) in each checklist item per B2") and the "no see-above" rule of task-integrity check 5. Practical risk is low (the referenced prompts carry an INDEPENDENCE clause) but the item as written lets the executor build a rerun prompt by hand with output-path edits in several places. | In item 6.58 add one sentence stating that the re-run agent prompt must include the INDEPENDENCE clause naming both paths (`.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` and `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md`: never read, list, grep into or cite) and the exclusion of `.dev/tasks/` from repo-wide searches, and name the two substitutions (report path to `...-<n>-rerun.md`, enumeration path to `...-<n>-rerun.md`) explicitly. A full embedded prompt is the strict reading; the one-sentence addition closes the independence gap. |
| m-1 | MINOR | line 621 (Step 7.2) | "four results" but the closing sentence still says "until the three checks are recorded" | Change "three" to "four" |
| m-2 | MINOR | line 74 | "the only commands run are read-only recounts" overstates (scratch fixtures, scratch git repos in `/tmp`, `git add .dev/tasks`) | Say "read-only commands, scratch fixtures under /tmp and staging of `.dev/tasks`" |
| m-3 | MINOR | line 336 (5.11) | Cause given as "unclosed character class"; observed Grep-tool error is "invalid character class range" | Say "rejected as an invalid character class" |
| m-4 | MINOR | line 570 (6.54) | Item is 9,194 bytes (partition check plus agent 1 spawn) | none needed; split only if the owner wants strict atomicity |
| m-5 | MINOR | line 396 | "use Grep for the marker" names no pattern | name `\[PENDING-ADJUDICATION` |

## Summary

| Finding | Status |
|---|---|
| O-1 | FIXED |
| O-2 | FIXED |
| G-1 | FIXED |
| G-2 | FIXED (executable; deviation on "state line counts in the item" justified) but introduced N-1 |
| O-3 | FIXED |
| N-13 | FIXED |
| Testing-N/A sentence | FIXED |
| Regression scan | 1 new blocking defect (N-1), 5 minor notes |

Blocking count: open prior findings 0 (of 5 in F_0), new blocking 1, so |F_1| = 1 < |F_0| = 5 (monotonicity satisfied). No prior-PASS item regressed except item 6.58's independence clause (new content, not a prior PASS item). This is fix cycle 1 of 2; one more fix cycle is available.

**Confidence:** Verified: 44/44 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (O-1 x6, O-2 x5, G-1 x7, G-2 x7, O-3 x5, N-13/testing x2, regression sub-checks 7.1-7.12 x12; 43 verified as fixed or passing and 1 verified as failing, N-1)
**Tool engagement:** Read: 7 | Grep: 14 | Glob: 0 | Bash: 14 (grep/sed/awk/find/ls/git diff, all read-only; the task file was not edited)

## QA Complete

VERDICT: FAIL
