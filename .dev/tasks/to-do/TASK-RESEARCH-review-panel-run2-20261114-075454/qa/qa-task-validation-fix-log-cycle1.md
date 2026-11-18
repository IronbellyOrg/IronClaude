# Fix Log: task-file validation (A.10), fix cycle 1

**Date:** 2026-11-14
**Task file:** `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md`
**Source findings:** `qa/qa-task-validation-consolidated.md`
**Scope:** F-1, F-3, F-4, S-1, S-2, S-3, S-4 and the `_REF_TOKEN` / `_ID_TOKEN` citation correction. Minor findings untouched.

Entries are appended below as each edit lands.

## F-1 (independence rule names no paths): FIXED

- Items edited, one Edit each (line numbers at edit time, unchanged since no edit added lines): 3.23 (280), 3.24 (282), 5.29 (374), 5.30 (376), 5.34 (386), 5.35 (388), 6.31 (514), 6.32 (516), 6.36 (526), 6.37 (528), 6.46 (550), 6.47 (552), 6.51 (562), 6.52 (564), 6.60 (584), 6.61 (586), 6.65 (596), 6.66 (598).
- Change: in each embedded prompt, `never read, list, grep into or cite the two forbidden run-1 paths` became `never read, list, grep into or cite `.dev/tasks/to-do/TASK-RESEARCH-review-panel-unify-20261113-155942/` or `.dev/tasks/to-do/REVIEW-PANEL-UNIFY-RUN2-QUEUED.md``; the following clause `exclude `.dev/tasks/` from repo-wide searches` was already present and is unchanged (same wording as item 3.18). Gate 4/5 items keep their existing `read-only;` wording.
- Proof: a scan of the task file (task file only; the forbidden paths themselves were not opened) shows 0 remaining occurrences of `two forbidden run-1 paths`, and each of the 18 item lines contains both `TASK-RESEARCH-review-panel-unify-20261113-155942` and `REVIEW-PANEL-UNIFY-RUN2-QUEUED` (18 of 18, count 1 each).

## F-3 (ref-rule test vs rule R1): FIXED

- Item 2.18, line 205 (two Edits; downstream items 4.03 and 5.09 not changed).
- Change 1: open item (c) of the assignment now says the ref-rule test is the ONE explicit exception to R1 for this test only. The scratch repo lives under `/tmp` (never inside the worktree), gets an initial commit with `git -c user.name=t -c user.email=t@t commit --allow-empty -m init` (stated reason: a branch ref needs a commit and an author identity; without it git reports `not a valid object name`), the second scratch repo reverses the order, both are deleted afterwards, and R1 still forbids any commit, branch, checkout, stash or write in the real repository and anywhere outside the output file and the two scratch directories.
- Change 2: the Ensuring clause now requires the literal `cannot lock ref` output (or, if git printed different text, the exact observed text stated as such) pasted into the research file, and the scratch-repository initial commit quoted.
- Proof: read-back of line 205 finds `ONE explicit exception to rule R1`, `allow-empty -m init`, `the literal `cannot lock ref` output`, `scratch-repository initial commit`; the old text `ONE exception to the write-nowhere rule` no longer matches.

## F-4 (item 5.06 reads the wrong files for C-S / FX ids): FIXED

- Item 5.06, line 322 (two Edits).
- Verified first that `research/scope/02-run-comparison-and-notes.md` exists (632 lines) and defines C-S1 at line 531, C-S16 at line 546, FX-1 at line 574, FX-22 at line 595.
- Change 1: added `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/research/scope/02-run-comparison-and-notes.md` lines 531-595 to the read list, with the note that the ids are defined only there.
- Change 2: replaced "of the run comparison" with "of slice 02 (`research/scope/02-run-comparison-and-notes.md` lines 531-595)". The independence paths already in the prompt are untouched.
- Proof: read-back of line 322 shows both strings; the phrase `of the run comparison` no longer occurs next to C-S1..C-S16.

## `_REF_TOKEN` / `_ID_TOKEN` citation correction: FIXED

- Verified in code: `src/superclaude/cli/review/findings.py:29` defines `_REF_TOKEN`; `src/superclaude/cli/review/telemetry.py:23` defines `_ID_TOKEN` and `:24` `_ID_RE`.
- Item 2.02, line 173: now "(`src/superclaude/cli/review/findings.py:29` `_REF_TOKEN`) and `src/superclaude/cli/review/telemetry.py:23` `_ID_TOKEN`".
- Item 2.15, line 199: now "known anchors: `:23` `_ID_TOKEN` here, and `_REF_TOKEN` is defined in `src/superclaude/cli/review/findings.py:29`".
- Proof: grep of the task file for the old citations (`telemetry.py:23` `_REF_TOKEN`, anchor `:23` `_REF_TOKEN`) returns 0 matches.

## S-3 (REGRESSION rule widened by FIXED-vs-open disagreement): FIXED

- Cycle-1 control items 3.20 (line 272), 5.31 (378), 6.33 (518), 6.48 (554), 6.62 (588); one Edit each.
- Change: removed the clause `or a finding reported FIXED by one report is reported open by the other` (item 6.62 said `reported OK`) from the REGRESSION rule and replaced it with a parenthetical: a finding that one verifier reports FIXED (OK in 6.62) and the other reports open was never PASS, so it is NOT a regression; it is counted as open in the union `F_1` and goes to fix cycle 2. A regression is now only an item that was PASS at review 1 and now has a blocking finding.
- Byte-exact messages untouched: each of the five lines still contains `Regression detected on Item X.Y, previously PASS at cycle 1, now FAIL. Halt overrides monotonicity check.` and `[HALT-MONOTONICITY] |F|=` (scan: 5 of 5 each).
- Proof: grep of the task file for `reported open by the other`, `reported FIXED by one report`, `reported OK by one report` returns 0; `was never PASS, so it is NOT a regression` appears once on each of the five lines. The cycle-2 control items (3.25, 5.36, 6.38, 6.53, 6.67) never had the clause and were not edited.

## S-2 (Evidence Trail requirement unsatisfiable at write time): FIXED

- Item 5.10 (line 330, two Edits): the purpose clause now says every research, web, scope and synthesis file and every debate folder is listed and the `qa/` directory with its naming pattern is pointed to; the `### QA Reports` row now lists the QA reports that exist in `qa/` at the time of writing (Gate 1), plus a line giving the directory path and the naming pattern of later gate files (`analyst-*.md`, `qa-*.md`, `gate<N>-cycle-control.md`, `final-validation-*.md`, `report-size-and-partition.md`, `phase<N>-*-inventory.md`, derived from the names this task file uses), and says not to list files that do not exist yet.
- Item 6.01 (line 448, one Edit): assembly rule 6 now reads: every research, web, scope and synthesis file and every debate folder, plus the QA reports that exist at assembly time, plus the `qa/` directory path and naming pattern of later gate files (not listed individually).
- Item 6.68 (line 604, one Edit): checklist item 10 now verifies Glob counts for research (24), scope (12), web (4), synthesis (10) and debate folders only, checks the QA reports that existed at assembly time, and checks that the `qa/` path and naming pattern are stated; it explicitly does not require later gate, fix-log, control or checklist files to be listed.
- Related instances of the same defect, reworded in the same way so S-2 is actually closed (disclosed as beyond the three listed places, same root cause and same sentence shape): item 6.06 (Gate 3 completeness lens, instance a, line 460) and item 6.19 (instance b, line 488) each demanded that the Evidence Trail list "every ... QA report that exists (verify with Glob)", which a Gate 3 lens run after assembly would fail by finding its own reports.
- Proof: read-back counts on lines 330, 448, 604 each match the new phrases; the old phrases (`synthesis and QA file and every debate folder produced`, `debate and QA file (verify`, `every file produced is listed`, `Gate 1 reports present at this time`) occur 0 times; a grep for `Evidence Trail`, `Section 10`, `QA file`, `QA report` shows no other item requiring later QA files to be listed (the `QA files` mention in the Task Log Task Summary template is a completion-time list, unchanged).

## S-1 (I17 items 5-6 deviation overclaims what the gates saw): FIXED

- Item 6.70 (line 608, one Edit): as its last action on a PASS decision (either branch) it now runs read-only `sha256sum` on the report and records `FINAL_REPORT_SHA256_AT_6.70=<hash>` in the ### Phase Gate Findings section of the Task Log, together with the last `FINAL_REPORT_SHA256=` value of the checklist file and whether the two are equal (a difference is recorded as it is). The Ensuring clause requires that line on PASS.
- Post-Completion final-state item (line 631, one Edit): it now compares the current report sha256 with the `FINAL_REPORT_SHA256_AT_6.70=` value (HALT if different, original HALT steps and blocker_reason kept); on a match it records a statement that the report is byte-identical to the content recorded at Item 6.70, that the last verification round (Item 6.68, or its re-check in Item 6.70) passed on [exactly that content | an earlier hash: both values] chosen from the real comparison with the last checklist hash, that Gate 3 and Gate 4 reviewed earlier revisions plus the verification rounds after their own fixes, that later fix agents of Gate 4, Gate 5 and the final validation may have edited the report afterwards, and that Gates 3 and 4 are not claimed to have seen the final text. The old claim (`which ran on the final report`, `byte-identical to the validated one`) is removed (grep: 0 hits).
- Builder note (now line 718, one Edit): rewritten to the same honest wording; names the fix agents Items 6.45, 6.50, 6.59, 6.64, 6.69; says only the last verification round can have passed on the content whose sha256 Item 6.70 records, and that Item 6.70 records whether that round's own hash equals it; says the deviation is also recorded under Deviations from Process. The old phrase "the report is not edited after them" is removed.
- Deviation recorded in the Task Log subsection `### Deviations from Process` (line 708, inserted after the template comment; one Edit, adds 5 lines: a blank line, the dated header at line 708 and three field lines): entry dated 2026-11-14 09:18 with Expected / Actual / Rationale fields, stating the same limits.
- Proof: grep for `FINAL_REPORT_SHA256_AT_6.70=` hits lines 608 and 631; `Gates 3 and 4 are not claimed to have seen the final text` hits the Post-Completion item and the Deviations entry; greps for `not edited after`, `ran on the final`, `byte-identical to the validated`, `satisfied by Gate 3` return 0 hits. The two halt messages are untouched.

## S-4 (staging happens before the final task-file state exists): FIXED

- New Post-Completion item inserted at line 637, between the `status: "🟢 Done"` item (line 635) and the NON-BLOCKING suggestion (now line 639); existing items keep their text and order (Step 7.2 at line 621 is unchanged). Post-Completion items are unnumbered, so no number was assigned.
- Content: re-runs `git add .dev/tasks > /dev/null`, repeats the three read-only checks of 7.2 (`.claude` must print nothing, the report path must print, count of staged files in this task folder), writes one Execution Log entry with the results, runs `git add .dev/tasks > /dev/null` once more so that entry is staged and re-checks `.claude`; it carries the 7.2 recovery step (`git restore --staged .claude`), forbids commit, push, fetch, checkout, stash and any add outside `.dev/tasks`, keeps the run-1 folder off limits, and has the template's blocker clause and completion gate. The Execution Log entry states that only the checkbox ticks of this item and the NON-BLOCKING item come after the final staging (those ticks are an inherent limit: ticking a box edits the file).
- Proof: the item list shows `Update completion_date` at 635, `Re-stage the final task-file state` at 637, `NON-BLOCKING` at 639. No `git commit`/`git push` command is instructed (only prohibited).

## Whole-file integrity checks after all edits

- Lines: 724 (717 before, plus 5 Deviations lines and 2 lines for the new item and its blank line). Item boxes: 187 `- [ ]` (186 before plus the new item), 0 checked boxes, 0 malformed or nested boxes.
- Placeholder scan patterns still written as `T[O]DO|T[B]D|FIX[M]E` (literal pattern text present 5 times); a plain scan for the three words finds 0 self-matches.
- Byte-exact messages unchanged: `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (cycle 1 and cycle 2 forms, 10 occurrences) and `[HALT-MONOTONICITY] |F|=` (14 occurrences) are the same text as before the edits.
- Item numbers, phase structure, agent counts and gates: unchanged.
- Minor findings: not touched (the 5.14 typo and all other minor notes were left as they were).
- Edit pathway: every change was made with the Edit tool (old_string unique per edit); no rewrite, sed -i or script rewriter was used.

## Status per finding

| ID | Status |
|---|---|
| F-1 | FIXED (18 of 18 items contain both literal paths) |
| F-3 | FIXED (item 2.18) |
| F-4 | FIXED (item 5.06) |
| S-1 | FIXED (items 6.70, Post-Completion final-state check, builder note, Deviations entry) |
| S-2 | FIXED (items 5.10, 6.01, 6.68; plus the same wording in 6.06 and 6.19) |
| S-3 | FIXED (items 3.20, 5.31, 6.33, 6.48, 6.62) |
| S-4 | FIXED (new Post-Completion item at line 637) |
| `_REF_TOKEN`/`_ID_TOKEN` | FIXED (items 2.02, 2.15) |
