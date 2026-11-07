# Invariant Probe: `/sc:issue --claim <N> --worktree` consensus

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | collection_boundaries | One `--limit 500` page holds every row of the repo on every host | UNADDRESSED | MEDIUM | List JSON has `result.truncated`, `result.totalCount`, `result.hostScope.omittedHostIds` and top-level `ok`; list `--help`: "The row cap is shared across hosts". The consensus reads none of them, so a truncated or partial page yields "no match" and a duplicate create, and a new row off-page breaks the set difference |
| INV-002 | state_variables | Branch tail after `refs/heads/` starts with `issue-<N>` | UNADDRESSED | MEDIUM | All 15 rows carry a prefix, e.g. `refs/heads/ironbelly/issue-330-ponytail-pin`; create `--help`: no `--branch` gives "the prefixed default". `^issue-<N>(-\|$)` on `ironbelly/issue-<N>` never matches, so lookup key 4 is dead |
| INV-003 | count_divergence | The before/after id set difference has exactly one element | UNADDRESSED | MEDIUM | Consensus item 6 names no rule for 0 or 2+ new ids. A concurrent create by the user or an Orca worker gives 2; a create that exits 0 while the row is not yet listed (or off-page, INV-001) gives 0. Either way the path, record and copy are undefined |
| INV-004 | count_divergence | "Two or more live matches" has one meaning across four ordered keys | UNADDRESSED | MEDIUM | Consensus item 5 is ordered, yet the rule counts matches without saying whether it counts within the first key that hits or across all keys, nor whether the same row hit by two keys counts once. Record hit X plus basename hits X and a suffixed Y: reuse X or stop? |
| INV-005 | interaction_effects | `<worktree>/.dev/issues/<N>/` holds only untracked files | UNADDRESSED | MEDIUM | `git ls-tree origin/master .dev/issues` lists tracked `.dev/issues/433/DECISIONS.md`, `REPORT.md`; `.dev/issues/` is not ignored (`git check-ignore` no match); design D9 invites committing these files. A worktree from `origin/<B>` then holds tracked files, the `.prev` rename deletes a tracked file in the fresh worktree, and the "untracked, do not stage" line is false |
| INV-006 | guard_conditions | No Orca row is tied to issue `<N>` other than by marker, record, basename or branch | UNADDRESSED | LOW | Rows `bare-python-hook-357` (`linkedIssue: 357`) and `feat-sc-issue-command` (`linkedIssue: 302`) have basenames the regex misses; a claim of 357 creates a second worktree for the same issue. Reading `linkedIssue` passes no link flag |
| INV-007 | guard_conditions | A basename or branch match is the worktree for this issue | UNADDRESSED | LOW | Hand-made rows `issue-305-*`, `issue-315-*`, `issue-384-*` exist (list output); the number in a hand-made name may be a PR or ClickUp id. Consensus reuses it and writes files into a checkout the skill never created, with no signal of which key matched |
| INV-008 | interaction_effects | Only one flagged claim of `<N>` runs at a time | UNADDRESSED | LOW | No lock in items 5 and 6. Two racing claims both see no match and both create, leaving two live matches; every later claim then stops on item 5's ambiguity rule |
| INV-009 | guard_conditions | `origin/<B>` that exists is fresh | UNADDRESSED | LOW | Item 4 checks existence only; the fetch runs in the Wave 1 worker (`refs/claim.md:28`) and its failure is not recorded for Wave 7, so an offline claim silently bases the worktree on an old ref |
| INV-010 | state_variables | Path strings compare equal when they name the same directory | UNADDRESSED | LOW | Item 5 guard ("git-common-dir equals main's") and item 7 ("share a real path") use different equality; row `id` is `<repoId>::<path>` (list JSON), so symlinked or trailing-slash paths make the record guard fail and fall through |
| INV-011 | interaction_effects | Every create finishes inside 120 s | UNADDRESSED | LOW | No `--setup` means repo setup hooks follow the repo policy (create `--help`), which can exceed 120 s. A killed CLI may leave a finished worktree that this run reports `failed`, with no record and no copy until a re-run |
| INV-012 | collection_boundaries | `^issue-<N>(-\|$)` separates numbers sharing a prefix | ADDRESSED | LOW | `issue-3` does not match `issue-30` or `issue-305-pr-submit-conflicts`; an Orca numeric suffix `issue-<N>-2` still matches; `issue-create-ccsession-aliases` matches no number |
| INV-013 | state_variables | `worktree.json` cannot leak state into another claim or repo | ADDRESSED | LOW | Item 6 excludes it from the copy (C O8.1, `round2-rebuttal-C.md:53`); item 5 guards it by existence and git-common-dir; the list is scoped by `--repo path:<main>` |
| INV-014 | guard_conditions | Wave 7 never runs on a partial claim | ADDRESSED | LOW | Item 2 starts Wave 7 only after both comments; every earlier STOP ends the run (`refs/claim.md:33-50`, `:89`), so a missing `<D>` cannot reach the copy |
| INV-015 | state_variables | The main checkout's branch or dirty state does not matter | ADDRESSED | LOW | Base is `origin/<B>`, not HEAD; `<main>` from git-common-dir resolves to `/home/coder/workspaces/IronClaude` (`git rev-parse` output); Orca puts worktrees under `/home/coder/workspaces/worktrees/IronClaude/`, outside the main checkout (`git worktree list`) |
| INV-016 | sufficiency_challenge | This design ALONE makes a claim end with a usable worktree | UNADDRESSED | MEDIUM | Falsified by: (a) INV-005, the worktree starts with tracked files renamed and `git status` dirty; (b) INV-003 with 0 new ids, Orca reports success but no path is reported or copied; (c) INV-001, a truncated page creates a second worktree and later claims stop on ambiguity. Also, stale-only (item 5) and a non-`.git` common dir (bare or submodule layout, parent of common dir is not the checkout) end with no worktree by design |

### INV-001 fix
Treat `ok != true`, `result.truncated == true` or a non-empty `result.hostScope.omittedHostIds` as `W-ORCA-LIST-FAILED`: create nothing, report the counts. Apply the same check to the after-create list.

### INV-002 fix
Match the branch key on the last `/`-separated segment of the ref (`refs/heads/ironbelly/issue-330-ponytail-pin` gives `issue-330-ponytail-pin`), and add a fake-orca fixture with a prefixed branch.

### INV-003 fix
Exactly one new id whose basename matches `^issue-<N>(-|$)` gives `created`. Zero gives `failed` plus `W-WORKTREE-CREATE-FAILED` naming "created but not listed"; two or more gives `W-WORKTREE-AMBIGUOUS` listing them, with no copy and no record.

### INV-004 fix
Deduplicate matches by row `id`. The first key (marker, record, basename, branch) with one or more live hits decides; ambiguity counts only within that key. Pin the rule with a fake-orca case where two keys hit different rows.

### INV-005 fix
Before copying, run `git -C <wt> ls-files .dev/issues/<N>`. Never rename or overwrite a tracked file: skip it and name it in `W-WORKTREE-COPY-FAILED`. Print "untracked" only when no file is tracked.

### INV-006 fix
After the branch key, treat a live row with `linkedIssue == <N>` as a match (read only). Report it as reused with the key named.

### INV-007 fix
Add `worktree_match_key` (marker|record|basename|branch|linkedIssue) to the return contract. Print a one-line "reused a worktree not created by /sc:issue" when the key is basename, branch or linkedIssue.

### INV-008 fix
Take an exclusive lock on `<D>/.worktree.lock` (O_CREAT|O_EXCL) for Wave 7; if it is held, warn and skip. Exclude the lock file from the copy.

### INV-009 fix
Have the Wave 1 worker record the fetch result in `scout.md`. If the fetch failed, Wave 7 adds `W-ORIGIN-BASE-STALE` (or skips) instead of creating silently.

### INV-010 fix
Compare every path through `os.path.realpath`: record guard, self-copy check and row paths.

### INV-011 fix
After a create timeout, re-list once and apply the INV-003 set-difference rule before reporting `failed`.

### INV-016 fix
Before returning `created` or `reused`, the script verifies the path exists, its git-common-dir equals main's, and every copied `<D>` file is byte-identical at the destination (or skipped as tracked); else `failed` with a warning.

## Summary

- 16 findings: UNADDRESSED 12 (MEDIUM 6: INV-001..005, INV-016; LOW 6: INV-006..011), ADDRESSED 4 (LOW: INV-012..015). HIGH 0.
- Orchestrator correction (2026-11-05): the fault-finder's own summary said 11 unaddressed and 5 addressed; a row count of the table above gives 12 and 4.
- Highest priority: INV-005, INV-002, INV-001 (each verified live).
