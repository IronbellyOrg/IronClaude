# Gate 2 synthesis fix log (cycle 1)

**Date:** 2026-11-20
**Status:** Complete
**Fix authorization:** true (blocking findings only)
**Work list:** G2-1 to G2-9 from /home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/qa/qa-synthesis-consolidated-findings.md

| ID | Summary |
|---|---|
| G2-1 | Remove docs/designs/orchestrator.md citations (synth-04, synth-06) |
| G2-2 | Dry-run step numbering and pre-launch re-read (synth-02 4.1 vs synth-03 5.1.1) |
| G2-3 | Extension Guide skeletons (synth-06 13.1.4, 13.1.7, 13.1.5, 13.1.6) |
| G2-4 | 35 per-issue cap wording (synth-01 section 1) |
| G2-5 | G2 rule 2 / orca allow-list caveat (synth-01 2.1, 2.3, 2.4; synth-02 4.6) |
| G2-6 | Status scheme for caller/binding of orca_worktree.py pending (five places) |
| G2-7 | synth-04 5.2 worktree row: /sc:task not accepted by guard |
| G2-8 | Both test callers of orca_worktree.py pending |
| G2-9 | synth-05 Appendix A intro: real git vs gh/Orca |

## Fix entries

All files below are under `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/synthesis/`. Line numbers are those after the edits. Every finding was FIXED; none is UNFIXABLE-FROM-EVIDENCE. Source claims were re-read in `/home/coder/.cache/ic-snap-20261120/master` (read-only, nothing written there).

**G2-1 (FIXED). Removed every citation of the out-of-scope design file.** The originating report counted six hits in synth-04 and synth-06; a grep of all six synth files found ten, so the four in synth-01 and synth-02 were fixed too (the task forbids the citation anywhere). Replacements: `docs/designs/sc-issue-launch-level-hook.md:23` ("so this guard does not govern it", re-read in the snapshot) for the coordinator-started worker; `CHANGELOG.md:17` (re-read) for removals; the words "no decision found in the files this reference cites" for the "grant row" retirement.
- synth-01 line 158 (ledger row 8): dropped "removal decision recorded at ..." and added "(records the removal)" after the existing `CHANGELOG.md:17`; line 160 (row 10 Note): now cites the guard design `:23`.
- synth-02 line 198 (4.3 bullet): same replacement, and both test callers named (see G2-8); line 228 (4.4 removed-verbs row): "code deleted" plus `CHANGELOG.md:17`.
- synth-04 line 192 (5.3 G1 row), line 213 (launch-path table, coordinator-started worker row), line 315 (ledger G1 row): guard design `:23`; line 316 (ledger route A row): `CHANGELOG.md:17` records the removal; line 378 (5.4 "grant row" line): "no decision found in the files this reference cites about retiring it".
- synth-06 line 240 (14.2 intro): clause rewritten to cite `CHANGELOG.md:17` and the guard design `:23` only; D-17 note (line ~260): removed "see the 14.2 clause"; D-18 note (line 261): guard design `:23` and "No decision found in the files this reference cites"; D-27 note: "Decision: `CHANGELOG.md:17` records the removal; guard comment `GUARD:496-497`"; D-31 note: "No decision found in the files this reference cites".
- Check: grep for `orchestrator.md` over the synthesis folder returns no hit; "PR 686" appears only at synth-01 line 44 (the one allowed sentence).

**G2-2 (FIXED). One step numbering for the poll cycle (synth-03 5.1.1 numbering adopted).** synth-02 4.1: former rows 11 (re-read) and 12 (launch step) merged into row 11 "Launch step `_launch` (1026-1112)" listing the order dry-run return, probe, prompt, re-read, day cap, DISABLED, cut-off, origin, `pending` save, `orca agent launch` (matches `cycle.py:1029-1058` read in the snapshot); commit is now row 12 and conclude row 13 (synth-02 lines 127-129). The dry-run bullet (line 138) now reads "runs steps 1 to 10 and returns at the top of step 11 (`P/cycle.py:1029-1035`)". The "L2 to L14" and "L1" labels were dropped with the rewritten row and bullet. Grep for other step-number references found none that conflict.

**G2-3 (FIXED). Extension Guide skeletons in synth-06 section 13.1.** Added a fenced skeleton to 13.1.4 (lines ~100-105: `<!-- block:<name> -->`, the three `choices` edits at `OW:1873/1883/1891`, the level word case at `GUARD:264-269`, one grid cell per class at `GUARD:785-803`, with `render_prompt` keeping `common` plus the level block, `OW:756`); extended 13.1.5 (line ~113: grid cell lines for a new class; the classifier part is stated as "not determinable from research" beyond the cited ranges); added to 13.1.6 (lines ~121-126: the `hooks.json` PreToolUse group shape copied from `hooks.json:115-134` and the `_FRESHNESS_SCRIPTS` entry at `install_hooks.py:42-97`); added to 13.1.7 (lines ~128-135: agent frontmatter `name`, `tools`, `model` as in `issue-worker-t3.md:1-8` and the `WORKERS` entry at `tests/skills/test_issue_worker_agents.py:21-26`, plus "not determinable from research" for the tier-selection logic, which is prose). All skeleton content was read in the snapshot first.

**G2-4 (FIXED).** synth-01 line 34 (Key statistics, Watcher surface row): "per-cycle call cap 35 (32 ordinary plus 3 reserved)" became "per-issue call cap 35 (32 ordinary plus 3 reserved) plus the two shared calls G1 and G2, so at most 37 `gh` calls per cycle (2 when idle)". This matches synth-03 5.1.2, synth-05 and synth-06 (checked by grep for "37"), and the code-based evidence in the coherence report (`github.py` `CALL_CAP`, `spend_shared`).

**G2-5 (FIXED). Caveat that G2 rule 2 and the orca allow-list recognise the command word `orca` only (`launch-level-guard.sh:457`; grep for `orca-ide` in the guard: 0 hits, re-read).** synth-01 line 106 (2.1 diagram, new continuation line), line 152 (ledger row 3 Note, short pointer, as the report's fix text asks), line 155 (ledger row 6 Note and evidence `:457`), line 180 (2.4 row 6); synth-02 line 291 (4.6 level grid row, ESCAPE cell). Each points to Section 5.3 and Section 14 D-25 and says "observed exit 0", which synth-04 line 283 and D-25 already state.

**G2-6 (FIXED). One status scheme: "NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON".** Applied in synth-01 line 160 (ledger row 10) and line 169 (row 18); synth-02 line 217 (4.4 `orca_worktree.py pending` row); synth-04 line 28 (5.2 "Any caller" row, already split, now the exact wording); synth-05 line 88 (8.3 last row); synth-06 line 261 (D-18, was "BUILT-ON (verb), no production caller"). synth-04 5.3 G1 rows keep "NOT BUILT (as a guard)": a different item (the guard, not the caller).

**G2-7 (FIXED).** synth-04 line 111 (5.2 `--pipeline` table, `worktree` row): the approval prompt now reads `/sc:implement` or `/task`, with "the template at `launch-prompt.md:23` also names `/sc:task`; [CODE-CONTRADICTED], the guard regex at `GD:347` does not accept it, see 5.3 and Section 14 D-23". Guard regex `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` re-read at `launch-level-guard.sh:347`.

**G2-8 (FIXED). Both test callers listed.** `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498` (both re-read; the second runs `pending` in three tests). Edited in synth-05 line 88 (8.3 last row) and line 341 (Appendix A.2 worker test row: "a test caller ... (the other is ...)"); synth-02 line 198 (4.3) and line 217 (4.4); synth-04 line 28; synth-01 row 10 and synth-06 D-18 already listed both.

**G2-9 (FIXED).** synth-05 line 305 (Appendix A intro): "none calls a real `gh`, `git` push or Orca" became "none calls the real GitHub (`gh`) or Orca, and the pre-push and L2-install tests run real `git` against temporary local repositories and a local bare remote". Evidence re-read: `tests/skills/test_issue_l2_install.py:3, 72-80` (real git, local bare remote) and the A.2 row for `test_launch_level_pre_push.py` (real git and a bare remote).

## Fix summary

| Item | Count |
|---|---|
| Blocking findings | 9 |
| FIXED | 9 |
| UNFIXABLE-FROM-EVIDENCE | 0 |

Files edited: synth-01, synth-02, synth-04, synth-05, synth-06 (synth-03 unchanged: its numbering was the reference). MINOR findings were not touched. No file outside the synthesis folder and this log was written.

Status: Complete

