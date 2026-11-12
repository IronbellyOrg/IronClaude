# QA Report: Actionability lens, DESIGN steps 1.17 to 1.19 and the `main.py` step

**Topic:** `docs/designs/orchestrator-mode.md` (1041 lines) after items 5.1 to 5.11
**Date:** 2026-11-09
**Phase:** doc-qualitative, actionability lens (research/09 Gap 5)
**Fix cycle:** 1 (first review). `fix_authorization: false`; no file edited except this report.
**Method:** read the DESIGN sections 7.1, 7.6, 8, 9, 10, 13, 15, 16, 17, 18 (each in chunks of at most 150 lines), research/07, research/08, r4-mechanical, r4-wc14-hits and r4-reanchor, then re-read every anchor on disk in `tests/skills/test_worker_contract.py`, `src/superclaude/core/WORKER-CONTRACT.md` and `src/superclaude/cli/main.py`. Bash was used only for `sed -n`, `grep`, `awk`, `wc`.

---

## Developer walk-through (what I could do from DESIGN alone)

**Where WC-16 goes (step 1.17).** `src/superclaude/core/WORKER-CONTRACT.md`, as a new `### WC-16. Coordinator loop` subsection between the Fan-in paragraph (line 273) and `### Worked example: gate hit, answer, new Task` (line 275). Both lines read true on disk (273 is "For N input Tasks feeding one merge Task ...", 275 is the Worked example heading; line 274 is blank). The full text is given verbatim in the DESIGN section 8 code block, so I do not need the SPEC.

**Which five pins change and how (step 1.19).** All five answered, with symbol names and lines that match disk:
1. `RULE_PHRASES` (dict at line 25): insert a `"WC-16"` entry after `"WC-15"` (165-172), before `"heartbeats"` (173).
2. `NEVER_AS_WORKER` (382-391): append `"/sc:sweep"`; the removal test at 1081-1082 is parametrized and covers it.
3. Rename the test at line 912; body unchanged. No other file references the old name (grep of the repo outside `docs/designs` and `.dev` found only line 912).
4. Add `assert "sweep" not in UNATTENDED_COMMANDS` after the `"load"` assertion at line 1322 (def at 1318).
5. Line 89: change the phrase to `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, ``. Lines 89-90 are two concatenated string literals, and only line 89 changes, so the edit is local.

**Which line the sweep pair follows (step 1.7).** After `main.add_command(issue_watch_group, name="issue-watch")` at `main.py:565`; `if __name__ == "__main__":` is at 568. Confirmed by `sed -n 555,569p`.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Every `test_worker_contract.py` anchor DESIGN section 8 cites (25, 89, 165-173, 209-219, 228-237, 382-391, 755-765, 831-839, 837, 912, 1081-1082, 1318-1322, 1556, 1940-1955, 1966, 2016) exists at that line with the stated text | PASS |
| C2 | The contract insertion anchors (lines 23, 110, 151, 273, 275) exist with the stated text | PASS |
| C3 | The four `RULE_PHRASES["WC-16"]` phrases occur verbatim in the section 8 final-text block | PASS |
| C4 | The WC-16 block and the new line 23 pass the existing contract-wide checks (`_check_repo_setup_gated` regex, the `src/superclaude/` absence assertions at 885 and 1156, `_check_rule` ident-on-heading, `_check_never_as_worker` one-line rule) | PASS |
| C5 | The five pins are all present in the "Pins (five edits)" list and each says what changes and where | PASS |
| C6 | Pin 5 (line 89) matches the new line 23 text byte for byte (including the `plus` continuation on line 90) | PASS |
| C7 | No second copy of the never-as-worker list exists that DESIGN misses (src, tests, plugins checked; dev guide 991 is R7; `HOW-WE-WORK.md:403` is a pointer, not a copy) | PASS |
| C8 | `main.py` anchor (565, 568, 569 lines) is correct and no "after line 561" remains | PASS |
| C9 | Step 1.7 can be executed without guessing the import statement | FAIL (MINOR only, F1) |
| C10 | Steps 1.17, 1.18, 1.19 can each be completed and verified in order with the suite green after each | FAIL (MINOR only, F2) |
| C11 | Section 16 rollback names every edit of steps 1.17 to 1.19 | FAIL (MINOR only, F3) |
| C12 | Each edit's line number stays valid when the edits are applied in step order | FAIL (MINOR only, F4) |
| C13 | The WC-16 text is unambiguous for a developer copying it and a coordinator reading it | FAIL (MINOR only, F5, F6) |
| C14 | The mechanical evidence (r4-mechanical, r4-wc14-hits, r4-reanchor) agrees with disk: 4 `WC-14` hits at 668/829/852/1041, `after line 565` x2, 1041 lines | PASS (one stale range, F7) |
| C15 | The master test constraints in section 8 (31-entry P2 set, no `## Unattended mode`, write-verb audit, 5-minute pins) match the test file | PASS |

## Findings

No BLOCKING or MAJOR finding. Seven MINOR findings; none fails the gate.

### F1. MINOR. Step 1.7 omits the import path, group name and lint comment
- Evidence: DESIGN line 932 says "Register `sweep_group` ... with the deferred-import pattern (after line 565)". Nothing in the DESIGN gives the statement. `grep` of the DESIGN for `from superclaude.cli.sweep`, `add_command`, `noqa` finds only lines 932 and 968.
- Guesses I would make: (a) import path. The two nearest precedents import the concrete module (`superclaude.cli.reflect.commands`, `superclaude.cli.issue_watch.cli`; `main.py:559`, `:563`), but DESIGN 7.1 line 360 and the diagram at 171 say `__init__.py` exposes `sweep_group` through a lazy `__getattr__` "registered in cli/main.py", so `from superclaude.cli.sweep import sweep_group` is the likely reading. (b) `name="sweep"`, inferred from the comment at line 438 and the `superclaude sweep run` text. (c) the trailing `# noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` comment; without the noqa, step 1.26 (`ruff check`) would report E402. (d) one blank line between the previous pair and the new import, and between the import and `add_command`, copying lines 559-565.
- Risk is low: either import path passes `test_cli_registration` (it imports the package, not `main`).
- Smallest fix: put the two lines in step 1.7 or in 7.1, e.g. `from superclaude.cli.sweep import sweep_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` then `main.add_command(sweep_group, name="sweep")`.

### F2. MINOR. Step 1.18 alone leaves the contract suite red
- Evidence: `test_worker_contract.py:86-92` pins the string `` `/sc:spawn` and `/sc:swarm-wizard`, plus ``; `test_contract_states_rule[never-as-worker]` (906-909) fails as soon as `WORKER-CONTRACT.md:23` gains `/sc:sweep` (step 1.18) and stays red until pin 5 (step 1.19). Step rows 943-945 give no per-step test command; the first full run is step 1.27.
- Smallest fix: add to row 1.18 "and pin 5 (line 89), in the same commit", or state "1.18 and 1.19 are one commit; run `uv run pytest tests/skills/test_worker_contract.py` after 1.19".

### F3. MINOR. Rollback row 970 does not list pin 5
- Evidence: line 970 lists "the `RULE_PHRASES` entry, the `NEVER_AS_WORKER` entry, the `UNATTENDED_COMMANDS` assertion and the test rename" but not the line 89 phrase edit. A partial revert of line 23 without line 89 repeats the F2 failure. (The sentence at 963 says rollback is one revert of all commits, so this only bites a partial rollback.)
- Smallest fix: add "the `never-as-worker` phrase at line 89" to row 970.

### F4. MINOR. Line numbers in the pin list are pre-edit and the DESIGN does not say so
- Evidence: pin 1 inserts about 8 lines near line 165, so the later anchors (382, 912, 1081, 1322) move by that amount if pin 1 is applied first. Each pin also names a symbol, so the developer can recover, and step 1.16a point (4) says to re-read at HEAD before editing.
- Smallest fix: one sentence in section 8: "Lines are at master `5dc29d23` before any edit in this step; locate by symbol name once pin 1 is in."

### F5. MINOR. WC-16 wording a reader must interpret
- Evidence (DESIGN line 677):
  - "Phase 1 adds this duty, not a scheduler." The contract already uses `P1` to `P4` for unattended-conversion phases (`WORKER-CONTRACT.md:16, 59, 303-327`); it has no other use of "Phase". A permanent rule that says "Phase 1" can be read as conversion phase P1, and it dates itself.
  - "a ready Task it did not create, needing ownership review, a frozen plan" is a comma list in which "needing ownership review" can be read as a separate escalation or as an appositive of the ready Task.
  - `/sc:sweep` and the liveness "sweep" at contract line 110 now share one word; WC-16 ties them only by cadence ("the cadence of "The sweep."") and does not say whether one `/sc:sweep` run satisfies line 110's sweep or is an additional pass (research/07 section 4(c) raised exactly this).
- Smallest fix: "This rule adds the duty to run `/sc:sweep`, not a scheduler."; "a ready Task it did not create (it needs ownership review)"; add "`/sc:sweep` is a separate read from the line-110 liveness pass; it does not replace it." Any wording change must keep the four pinned phrases.

### F6. MINOR. Step 1.16a gives expected results with no mismatch action
- Evidence: DESIGN line 942, points (2) and (3) state outcomes ("succeeding", "failing, so the `495eb96d` pin stands and no layout diff is needed") and the gate is "satisfied as soon as it is written". If `495eb96d` turns out to be an ancestor of `origin/master` the step has no instruction. I did not run these `git` commands (outside the allowed Bash set), so the stated outcomes are unverified by me.
- Smallest fix: add "if (3) succeeds, stop and ask the owner" to the row.

### F7. MINOR. Stale extent in r4-reanchor.md
- Evidence: `r4-reanchor.md:39` says "Section 8 is lines 666-695" and `r4-wc14-hits.md:77` says "lines 666-693"; on disk section 8 runs 666 to 703 (heading `## 9.` at 705). The "no old anchor remains" grep therefore skipped lines 696-703 (it would not have found anything, since those lines cite 765 and the new line 23). Evidence note only; no DESIGN edit needed.

## Guess list (everything I would have to decide myself)

1. Import path, group name and noqa comment for the `main.py` pair (F1).
2. Whether to commit 1.18 together with pin 5 (F2).
3. Blank-line layout around the new `### WC-16` heading and its paragraph (one blank line each side, copying the neighbours).
4. Format of the new `RULE_PHRASES` entry: DESIGN line 684 shows it on one line, which `ruff format` (step 1.26) would split; I would copy the multi-line shape of `"WC-15"` (lines 165-172).
5. Where the new `NEVER_AS_WORKER` entry goes in the tuple (order is irrelevant to the tests; I would append after `"/sc:pr-submit"`, as "Append" says).
6. The new line 23 puts `/sc:sweep` before `/sc:swarm-wizard`, which breaks the alphabetical order of the existing list ("swarm" sorts before "sweep"). The DESIGN text is explicit, so I would follow it; R7 says "same order as section 8".
7. What to do if 1.16a points (2) or (3) come out other than stated (F6).
8. Whether `WRITE_VERB_CLASSIFICATION` needs a row for `sweep.md` or the skill: the regex at 1948-1951 only fires on `git add|commit|push|merge|stash|update-ref|worktree add|remove` and `gh pr|gh api`; the DESIGN's 7.6 skill text has none, so no row, but that is for steps 1.14-1.15, not 1.17-1.19.

## Self-Audit

**(a) Reliance list.** No `## Inherited Structural Verdict` block was supplied, so no rf-qa PASS was relied on. I used r4-mechanical.md only as a pointer to what to re-check.

**(b) Independent semantic checks.**
- Pinned-phrase fit: compared each of the four `RULE_PHRASES["WC-16"]` phrases against the code block at DESIGN 677 by reading it; compared pin 5 with `test_worker_contract.py:89-90` and the new line 23 text at DESIGN 701.
- Test side effects of the WC-16 text: read `_check_rule` (755-762), `_check_never_as_worker` (765-771), `_REPO_CODE_SPAN_RE` (798-803) and the removal tests (1044-1051, 1081-1090); grepped the test file for whole-contract `not in` assertions (884, 885, 948, 1156) and found none the block trips.
- Step-order simulation: traced that editing line 23 without line 89 fails `test_contract_states_rule[never-as-worker]` (F2).
- Duplicate-list hunt: grepped `src`, `tests`, `plugins`, `docs` for the never-as-worker list; found only contract line 23, test line 89, dev guide 991 (R7) and a pointer at `HOW-WE-WORK.md:403`. Globbed for a second `WORKER-CONTRACT.md` copy (only the `.venv` installed copy).
- Anchors re-read on disk: contract 23, 110, 151, 273, 275; test 25, 86-92, 156-173, 209-237, 382-391, 755-771, 831-839, 912, 1044-1051, 1081, 1316-1324, 1556, 1925-2016; `main.py` 555-569.
- Mechanical claims re-run: `WC-14` hits (668, 829, 852, 1041), `after line 565` count (2), `after line 561` and `519-561` (0), file length (1041).

**Confidence:** Verified: 15/15 checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (the `git` outcomes in step 1.16a are noted in F6 as not run by me; they are not a check in the table).
**Tool engagement:** Read: 13 | Grep: 10 | Glob: 1 | Bash: 4

## Recommendations

- Apply F1 (two literal lines in step 1.7) and F2 (commit 1.18 with pin 5) before the task file is built; the rest are optional wording.

Verdict: PASS
Blocking count: 0
