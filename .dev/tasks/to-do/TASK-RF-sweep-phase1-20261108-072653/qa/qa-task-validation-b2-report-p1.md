# QA Report - Task Integrity, Lens B2 Self-Containment (Phases 1 to 7)

**Task file:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
**Date:** 2026-11-08
**Phase:** task-integrity
**Lens:** b2-self-containment
**Scope:** frontmatter, Overview, Execution Context, Phases 1 to 7 (task file lines 1 to 1263, read in chunks of at most 150 lines)
**Fix cycle:** N/A
**Fix authorization:** false (report only; the task file was not edited)

---

## Overall Verdict: FAIL

9 blocking (IMPORTANT) findings, 0 CRITICAL, 8 MINOR notes.

## Items Reviewed (B2 checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has all 5 B2 parts (Context, Action, Output, Verification, Completion gate) | PASS (form) | All items 1.1 to 7.34 carry the five labelled fields. The form is there; what is inside it fails checks 2 and 3. |
| 2 | No item leans on an earlier item without restating it | FAIL | B2-01, B2-02, B2-03: about 60 items say "Same inputs as", "as in item 2.17", "Apply the item 2.21 procedure", "the checks from item 2.7" or "the HALT-item procedure above". |
| 3 | Agent-spawning items carry fully embedded prompts | FAIL | B2-04: every spawn names a preamble by reference. Verifier and fix items carry no item-level prompt at all. |
| 4 | File paths are specific | FAIL | B2-02 (bare file names with no gate folder), B2-08 (`orca-tabs/` with no root), MINOR M-07. |
| 5 | Verification criteria are measurable | FAIL | B2-09 (item 7.20 has two checks with no pass rule). MINOR M-02 and M-05. |
| 6 | No batch items | PASS | No item bundles unrelated work. Item 7.16 runs many commands, but they are one capture procedure with one output file. |
| 7 | No item rests on [CODE-CONTRADICTED] or [UNVERIFIED] findings; owner HALTs HALT and invent nothing | PASS with defects elsewhere | OQ-1 (6.1 to 6.3), OQ-2 to OQ-7 (7.1 to 7.12) and OQ-8 (7.14, 7.15) each write a PENDING record and then HALT. Each recommendation is labelled "does NOT authorize adoption". GQ-63 (7.9) carries no recommendation. Items 2.10, 3.8 and 4.9 keep the UNVERIFIED Orca claims marked UNVERIFIED. The anchors I checked match master: `main.py:563/565/568`, `WORKER-CONTRACT.md:23, :63, :64, :110, :275`, `test_worker_contract.py:89, :156-172, :173`. Wrong research pointers are a separate defect (B2-05). |

## Summary

- Checks passed: 3 / 7 (1, 6, 7)
- Checks failed: 4 (2, 3, 4, 5)
- Critical issues: 0
- Blocking (IMPORTANT) issues: 9
- Minor notes: 8
- Issues fixed in place: 0 (not authorized)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B2-01 | IMPORTANT | Items 2.9 to 2.16, 3.7 to 3.14, 4.8 to 4.15, 5.14 to 5.21, 7.22 to 7.25 (36 lens items) | Context is "Same inputs and gate folder as 2.8" (or 3.6, 4.7, 5.13, 7.21). The input file list is not restated. The QA Gate Protocol Spawn rule (task file line 191) requires each spawn to carry "the input file list", so an executor that resumes at one of these items, or reads it alone, does not know which files to hand the agent. | Restate in each item's Context the literal input list and gate folder, for example "Inputs: DESIGN, research/04 section 2, `${TASK_DIR}phase-outputs/test-results/r3-b1-mechanical.md`. Gate folder `${TASK_DIR}qa/r3-b1/`." |
| B2-02 | IMPORTANT | Verifier items 2.19, 2.20, 2.23, 2.24, 3.17, 3.18, 3.21, 3.22, 4.18, 4.19, 4.22, 4.23, 5.24, 5.25, 5.28, 5.29, 7.28, 7.29, 7.32, 7.33; fix items 2.22, 3.20, 4.21, 5.27, 7.31 | Inputs are given as bare names (`consolidated-findings-cycle0.md`, `fix-log-cycle1.md`, `cycle1-decision.md`) with no `${TASK_DIR}qa/<gate>/` folder. Five gates use the same file names, so the folder is the only thing that tells them apart. Half of these items then say "Same inputs as 2.19" (or 7.28 "the item 7.21 inputs"), which leans on another item. | Give full paths, for example `${TASK_DIR}qa/r3-b1/consolidated-findings-cycle0.md`, and list the inputs inside each item. |
| B2-03 | IMPORTANT | Consolidation 3.15, 4.16, 5.22, 7.26 ("as in item 2.17"); cycle-1 decision 3.19, 4.20, 5.26, 7.30 ("Apply the item 2.21 procedure"); gate decision 3.23, 4.24, 5.30, 7.34 ("Apply the item 2.25 procedure"); mechanical 3.5, 4.6, 5.12 ("checks from item 2.7"); decision records 7.1, 7.3, 7.5, 7.7, 7.9, 7.11 ("in the decision-record form above"); HALT items 7.2, 7.4, 7.6, 7.8, 7.10, 7.12 ("Apply the HALT-item procedure") | The rules that decide the gate outcome are only in the earlier item or in the phase preamble (task file line 1014). Missing from the later items: the dedup rule (same `file:line` and same defect, keep the highest severity, BLOCKING first); how `F_1` is built (ids OPEN in either verifier plus new BLOCKING or MAJOR findings); how `F_2` is built; the exact em-dash, TODO/TBD and totals commands; and the HALT Branch 2 steps (set RESOLVED, append to the Execution Log, reset status, clear `blocker_reason`). The decision items restate the halt strings but not these rules. | Restate the dedup rule, the `F_n` construction, the four exact mechanical commands and the Branch 1 and Branch 2 HALT steps in each item. One sentence each is enough. |
| B2-04 | IMPORTANT | Every agent-spawning item in Phases 2 to 7 (lens, fix and verifier items) | Each spawn says "with the report-only preamble", "with the verifier preamble" or "with the fix agent preamble" instead of embedding it. The task file's own QA Gate Protocol (line 188) says the report-only preamble must be embedded verbatim in every report-only spawn. Verifier items (for example 2.19, 2.23) and fix items (2.18, 2.22) carry no item-level prompt text at all. Mitigation: the preamble text is in the same file, which makes this the least severe of the blocking findings. | Embed the preamble text, or at least its key lines (`fix_authorization`, finding fields, the `Verdict:` and `Blocking count:` ending), in each spawn item. Alternatively, change line 188 so it no longer demands verbatim embedding, and record why referencing is accepted. |
| B2-05 | IMPORTANT | Items 2.1, 2.2, 2.3, 2.4, 2.6 | The research/04 line pointers are off by 2. Item 2.1 says "Read the full wording of each edit from research/04 lines 89-91", but edits 1 to 3 are at research/04:87-89 (lines 89 to 91 hold edits 3, 4 and 5). Edit 4 is cited at :92 but is at :90. Edits 5 and 6 are cited at :93-94 but are at :91-92. Edits 7 and 8 are cited at :95-96 but are at :93-94. Edit 9 is cited at :97 but is at :95. Item 2.11 cites "research/04:87-97" correctly, so the file contradicts itself. These items say "copy verbatim" from the cited lines, so a wrong pointer leads to the wrong text. | Correct the pointers to :87-89, :90, :91-92, :93-94 and :95, or embed the edit text in the items. |
| B2-06 | IMPORTANT | Item 2.2 | research/04 edit 4 (:90) has two replacements. The second replaces "A path-B match outside that window, or on a row with no observable start time, does not join: ... `pane moved to a later session` ..." with text that adds the `Dispatch time window not observable` note (review-3 note m5). Item 2.2's Action names only the first passage, and its Verification checks only the first. If the old sentence stays, DESIGN contradicts the fixtures item 2.5 adds (`test_path_b_row_without_start_has_no_window` expects `Dispatch time window not observable`). | Add the second replacement to item 2.2's Action, and add a verification grep that the old "or on a row with no observable start time, does not join" text is gone. |
| B2-07 | IMPORTANT | Item 7.16 | As written, the item cannot be run in order. Context says `<dispatch>` is "each Dispatch id from the `worker-list` output". The Action runs `worker-show` for each Dispatch first (the "before" reads) and only then template 2 (`worker-list`). DESIGN 15.1 (orchestrator-mode.md:875) requires `worker-show` and `task-list` to run before and after all other reads, so the executor would have to improvise the order on a live, allowlist-bound step. | State the sequence explicitly, for example: (1) `worker-list` once to learn the Dispatch ids, (2) the before reads, (3) the other templates, including template 2 again and the fake-id call, (4) the after reads. Also record that the first `worker-list` call is an extra read. |
| B2-08 | IMPORTANT | Item 7.16 | "list and read the `orca-tabs/` files only" gives no root folder. DESIGN line 32 gives `${XDG_STATE_HOME:-~/.local/state}/ccsession/orca-tabs/`. On a step whose whole safety argument is "only these reads", the path must be literal. | Put the full path in the Action and in the Verification. |
| B2-09 | IMPORTANT | Item 7.20 | Two of the seven checks have no pass rule. `grep -c 'does NOT authorize adoption' ...OQ-*-decision.md` gives no expected per-file result (the OQ-8 file has no such line by design, and the OQ-6 file uses a different sentence). `git status --short tests/sweep/fixtures/` gives no expected output. The item's own Verification asks for "one PASS or FAIL line per check", which cannot be decided for these two. | Give each check an expected value, for example "count is 1 in OQ-1 to OQ-7 files and 0 in OQ-8", and "lists only the new `captured-*.json` and `SOURCES.md` as untracked". |
| M-01 | MINOR | Items 2.6, 4.5 | research/04 edit 9 (:95) also asks to change the cycle 2 row's "the transcript's earliest timestamp" (review-3 note m2). Item 2.6 skips this, and item 4.5 says to leave the cycle 2 row unchanged. research/04:189 allows the cycle 3 row to stand in for the R2-B1 correction, but it does not cover m2. | Either apply the m2 phrase fix or record it as skipped in Phase 2 Findings. |
| M-02 | MINOR | Items 3.1, 4.1 | Verification checks hits "in section 7.2" with `grep -c` over the whole file. That needs the section map, which these items do not run. | Add the `grep -n '^## \|^### '` section map command to the Verification. |
| M-03 | MINOR | Item 7.18 | "items 1 to 8, 13" includes `run-current` plain output (capture items 1 and 2) and the `orca-tabs/` reads (item 13), which may not be JSON, while the Verification requires every `captured-*.json` to parse. Also, the `grep 'coder'` check could match the sanitize-rule text in `SOURCES.md`. | Limit the list to outputs that are JSON, and exclude `SOURCES.md` from the grep or word its rules without the real user name. |
| M-04 | MINOR | Item 7.19 | No branch covers the `495eb96d` ancestry check returning 0 (merged since the build). "check 2" is ambiguous against the numbered points (1) to (4). | Add a HALT or a note branch for exit 0, and say "point (2)". |
| M-05 | MINOR | Item 2.7 | The item claims seven checks but lists commands for only five. The window-rule check and the GQ-103(3) check have no command of their own. | Name the command or the read for each of the seven checks. |
| M-06 | MINOR | Items 3.6, 4.7, 5.13 | "Sizing as for item 2.8" is informational, but it also leans on another item. | Write "4 rf-qa + 4 rf-qa-qualitative + 1 domain lens". |
| M-07 | MINOR | Item 5.3 | The Action and Verification say "the hit list file" with no path (it is `${TASK_DIR}phase-outputs/discovery/r4-wc14-hits.md`). | Name the path. |
| M-08 | MINOR | Item 7.8 | Branch 2 covers only 6 h and 72 h. Any other owner value (for example 24 h) has no instruction. | Add "any other value: record it as the CLI default and note it", or HALT for a re-build. |

## Actions Taken

None. `fix_authorization: false`.

## Recommendations

- Fix B2-01 to B2-04 in one pass. The same few sentences (inputs with full paths, the dedup and `F_n` rules, the HALT branches, the preamble) need to go into each repeated gate item. Fixing it once per pattern and copying it across the gates removes about 60 references.
- Fix B2-05 and B2-06 before Phase 2 runs. Otherwise the R3-B1 edits will copy the wrong research text or leave a sentence that contradicts the new fixtures.
- Fix B2-07 and B2-08 before Phase 7 runs, because item 7.16 is the only live Orca step in this range.

## Confidence Gate

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (the checks were carried out; the verdict is FAIL on the findings)
- **Tool engagement:** Read: 19 | Grep: 9 | Glob: 0 | Bash: 0
- Verification actions: I read the task file lines 1 to 1268 in 9 chunks. I compared research/04 lines 85-119 and 140-209 against the item citations, and research/09 Gap 4 against the fixture names. I read DESIGN 15.1 (lines 866-895) and grepped DESIGN line 32 for the `orca-tabs` path. I checked `WORKER-CONTRACT.md` :22-23, :62-64, :95, :110, :275, `test_worker_contract.py` :86-90 and :154-175, and `main.py` :563/565/568. I grepped the forward item references 8.4, 8.12, 9.1, 9.3, 10.5, 11.2 and 12.1 to 12.3 (all exist), and the Open Questions section (line 2455, with OQ-14 present).
- Not checked: the fan-in paragraph at `WORKER-CONTRACT.md:273`, the research/07 and research/08 line citations in Phase 5 (only the master files they point to were spot-checked), and the APPROVED.md line numbers in item 7.13.

VERDICT: FAIL
