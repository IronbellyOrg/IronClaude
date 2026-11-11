# Fix log: A.10.25 research-alignment cycle (F8, F9, F10, F11)

**Target:** .dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md
**Findings source:** qa/qa-task-validation-consolidated.md section "A.10.25 research-alignment findings"
**Date:** 2026-11-07
**Rule:** targeted Read-then-Edit only; no product-code edits; no installer run; 91-item count unchanged unless noted.

---

## Changes (appended as applied)

Line numbers refer to the task file after the edits (the file grew from 598 to 599 lines because Builder Note 13 was added at line 598; all other edits were in place on existing lines).

| Finding | Line | Change |
|---|---|---|
| F8 | 128 | Key Constraints NO INSTALLER RUN: read-only help flags allowed; fresh 6.9.0 behaviour derived from installer code (CODE-VERIFIED); this worktree's _bmad trees are a git-tracked 6.10.0 tree (manifest 6.10.0, installDate 2026-04-18), corroboration only, tag OBSERVED-FROM-6.10.0-TRACKED-TREE; run-only facts UNVERIFIED |
| F8 | 164 | Open Question 3 reworded the same way |
| F8 | 192 | Step 2.1: example skill marked 6.10.0 corroboration; evidence paragraph renamed INSTALLER EVIDENCE RULES (read installer code, record manifest version, git ls-files check, new tag); verification clause updated (CODE-VERIFIED / OBSERVED-FROM-6.10.0-TRACKED-TREE / UNVERIFIED) |
| F8 | 269 | Step 3.14 gaps log: new item (7) for run-only facts plus the 6.10.0 note |
| F8 | 291, 295, 299, 303 | synth-01/02/03/04 rule 9: 6.10.0 tracked-tree rows are version-mismatched corroboration only; run-only facts go to gaps/Section 9 |
| F8 | 491 | Step 7.3 summary wording |
| F8 | 598 (note 13) and 592 (note 7) | Builder notes corrected; note 13 added for this cycle |
| F8 | 474 | Step 6.8 new criterion 24 (retired tag must not appear; tree never presented as 6.9.0 output) |
| F9 | 299 | synth-03 comparison rows: Writes inside the whole-HOME snapshot (test-57 448-450), HOME persistence across boots, Survives reboot and superclaude install; Step 5.3 verification clause updated |
| F9 | 303 | synth-04 requirement (v) Persistence and snapshot checks; checklist item (vi); Step 5.4 verification clause updated |
| F9 | 474 | Step 6.8 criteria 21 and 22 |
| F10 | 208 | Agent 05: extra files (releases.json, markdownlint workflow and config), part (e) README constraints, verification clause (c), (d) and (e) |
| F10 | 303 | synth-04 document list: README :241 reconcile, :308 left alone, anchor "upstream GitHub CLI release v" (README about line 100, releases.json:113), manual command named, markdownlint-clean |
| F10 | 474 | Step 6.8 criterion 8 pointer and new criterion 23 |
| F11 | 128, 192 | Help flags allowed (--help, --list-tools, --list-options verified in commands/install.js lines 18-28), actual install not |

## Checks
- Unchecked checklist items: 91 (unchanged). No item added or removed.
- Final grep for old-premise wording (OBSERVED-FROM-EXISTING, EXISTING-INSTALL, existing install, real bmad install, already run, a real install): one hit, line 474, the intentional "retired tag" Grep instruction in criterion 24.
- Only the task file and this log were edited. No installer run, no product-code edit, no commit.
