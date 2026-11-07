# Round 2 Rebuttal: Advocate B (refactorer)

Read-only evidence today: `orca worktree list --repo path:<main> --json` returns 14 rows, every `comment` is `""`, none archived. Two rows (`/tmp/ironclaude-p0live/*`) have no directory but their branches still exist. Branch and path diverge on two live rows (path `feat-sc-issue-command` with branch `fix-issue-slug-chars`; path `issue-330-ponytail-plugin` with branch `issue-330-ponytail-pin`). Branch values are full refs (`refs/heads/ironbelly/...`).

## O1. Missing path
Warn `W-WORKTREE-STALE`, create nothing, print path, branch and remedy. A fresh create would hit a branch git still holds (Orca then suffixes the name) and leave two rows. Concede my Round 1 "create fresh". 75%.

## O2. `worktree.json`
Exclude. A third key adds a state file that can drift from Orca. `.dev/issues/` is not ignored, so it shows as untracked in `git status` and carries a machine-local absolute path. Marker plus path fallback already give two keys. If the list call fails, warn and skip (fail open). 65%.

## O3. Copy rule
Accept A's per-file rule with two changes: one `<name>.prev` that replaces any older `.prev` (no timestamp pile), and skip when source and destination share a real path (A's self-copy defect). Concede my skip-and-warn: a stale `next-steps.md` holds outdated commands. 65%.

## O4. Name
`issue-<N>`, no `--branch`, no slug. Marker-first is not enough to make the name irrelevant: the marker is unverified, so the basename fallback carries re-claims and needs a stable, slug-free prefix. 75%.

## O5. Marker
Unverified. Order: marker, then path basename `^issue-<N>(-|$)`, then branch tail after stripping `refs/heads/` (rows above show the two fields diverge, so test both). Manual run must record: create JSON shape; `comment` after create; actual path basename and branch; a numeric suffix when the name is taken; second claim returns `reused`; `projectId` observed. 70% the fallback alone is sufficient.

## O6. Versus A
- O1, O4, O5 order: agree.
- O2: disagree (above).
- O3: agree with edits.
- A defect 1: partly disagree. One live plus one stale match should reuse the live one and mention the stale; only two or more live matches create nothing and list all paths.
- A defect 2 (self-copy): agree.
- A defect 3 (sufficiency): agree, given O1.

## O7. New defects
1. Re-list by marker (A and my Round 1) fails if `comment` stays empty. Snapshot row ids before create and take the set difference after; the new row's path is the answer, marker not required.
2. Empty or partial list: a registered repo always has its main-worktree row. Zero rows, or no `isMainWorktree` row, means the list is unusable (repo unregistered, wrong selector); warn and do not create. Otherwise "no match" would create in the wrong place.
3. Parser tests must use the real shape (`result.worktrees`, full-ref branch, path/branch divergence). Fake-orca fixtures copied from today's output prevent a regex that passes tests and misses live rows.

Sufficiency: with O1 stop, the id-diff, and the empty-list guard, a claim ends with a usable worktree or one named warning with a remedy.
