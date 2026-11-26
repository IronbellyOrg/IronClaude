# Findings: issue 766 (sweep classifies almost every worker as "could not determine")

Issue: https://github.com/IronbellyOrg/IronClaude/issues/766 (OPEN, label `bug`, created 2026-11-24T17:18:29Z, no comments). Checked at HEAD a7ae3dd30 on 2026-11-24.

## Verdict

**still-relevant.** The three causes are all still in the code; no PR has touched the sweep package since the issue was filed.

Evidence (all re-read at HEAD a7ae3dd30):

- `git log` for `src/superclaude/cli/sweep` ends at b46ecc1bd (PR 579, merged 2026-11-17); before it 4d3c0b126 (PR 539). No newer commit. `gh pr list --search 766` returns no PR.
- Cause 1, relative path read as absolute: `src/superclaude/cli/sweep/probes.py:1087` `_CONTRACT_PATH_RE = (/[^\s'"`<>()]*/return-contract.yaml)` has no left boundary; used at `probes.py:1101` in `_contract_candidates` (1092-1105). `_read_contracts` records `outside root` at `probes.py:1415`. `report_folders` (`src/superclaude/cli/sweep/models.py:29-42`) resolves relative folders against the worktree but is only fed by report-dir style flags, not by contract paths in prose.
- Cause 2, tail-only forcing: `src/superclaude/cli/sweep/classify.py:619-627` adds `NOTE_TAIL_ONLY` (defined :58) for every row of the pane when `not tail.tail_complete`; `_force_unknown` (`classify.py:358-366`) replaces the class after the rules; applied at `classify.py:961`.
- Cause 3, caps: `probes.py:88` `TRANSCRIPT_TAIL = 256 * 1024`, `:89` `WORKER_LIST_PAGE = 100`, `:129` `shows: int = 50`, `:1157-1161` sets `state.truncated` and does not follow the cursor.
- Not re-measured: the live figures (99 could-not-determine of 100 rows, 61 matched rules, 35 relative-path rows, the 4.6x speed-up). UNVERIFIED by me; they come from the issue body and a local file that is not in the repository.
- Whether the tail-only forcing is intended is UNVERIFIED (the issue itself says so).

## Complexity and size

Complexity **medium**; size **M**. Three separate fixes in `src/superclaude/cli/sweep/` (a regex or path-resolution fix, a classification-order change that needs an owner ruling, and page-following plus show sizing) plus tests in `tests/sweep/`.

## Priority

**P1.** The sweep is the coordinator's required pre-action read (WC-16, `src/superclaude/core/WORKER-CONTRACT.md`), and its classes are unusable on a large Run; it also blocks issue 757 (change-only wake). Not P0: nothing is lost and the issue notes a workaround.

## Concrete next steps

1. Fix cause 1 first (smallest, clearly wrong): anchor `_CONTRACT_PATH_RE` and the quoted form so a path preceded by a non-space, non-quote character is not matched, and resolve a relative `.dev/.../return-contract.yaml` against `obs.worktree_path` the way `report_folders` does. Add a case to `tests/sweep/test_probes_allowlist.py` or `tests/sweep/test_classify.py` using the brief text from the issue.
2. Get the owner's ruling on cause 2 (should a tail-only transcript override a finished row with a parsed contract and a settled Orca outcome?). If it should not, make `NOTE_TAIL_ONLY` a note and keep the class; test in `tests/sweep/test_classify.py`.
3. Follow `worker-list` pages (cursor) and size `Budget.shows` from the worker count; keep `ALLOWED_ORCA` (10 read-only templates, `probes.py:49-60`) unchanged unless a new call is needed; `tests/sweep/test_probes_allowlist.py` pins it.
4. Keep the change inside `src/superclaude/cli/sweep/` and `tests/sweep/`, as the issue asks; run `uv run pytest tests/sweep/ -v` (not run by me).
5. Decide with the owner whether 766 and 590 are merged as duplicates (the issue proposes it).

## Dependencies

- Needs: none strictly; step 2 needs an owner ruling.
- Blocks: #757 (watcher built on class changes needs working classes).
- Partly overlaps: #590 (same symptom, both OPEN).

## Related issues

- #590 (OPEN) first live sweep run, show cap of 50, finished workers need an unread contract.
- #757 (OPEN) run the sweep outside the session and wake only on change.
- #534 (OPEN) parent tracker of sweep follow-ups from #339 Phase 1.
- #706 (OPEN) observer follow-ups incl. sweep source and scale tests; relation UNVERIFIED.
- #339 (OPEN) orchestrator umbrella feature.

## Related PRs

- #539 (MERGED 2026-11-14) added the read-only sweep (commit 4d3c0b126).
- #579 (MERGED 2026-11-17) restored the working class with the real Orca names (commit b46ecc1bd).
- No open PR for 766.
