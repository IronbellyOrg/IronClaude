# Round 2 Rebuttal: Advocate C (QA)

Fresh evidence (read-only): 15 list rows, every `comment` `""`; two `/tmp/ironclaude-p0live/*` rows have no directory but branches remain; path/branch diverge live (`issue-330-ponytail-plugin` vs branch `issue-330-ponytail-pin`); the main row is `isMainWorktree: true`; a hand-made `issue-384-*` row exists.## O1. Missing path
Warn `W-WORKTREE-STALE`, create nothing; print path, branch, remedy. I concede E8's "re-create": the `/tmp` rows show the branch stays registered, so a fresh create gets a suffix and leaves two matching rows, locking later claims into "several matches". Branch gone changes only the remedy text. 80%.
## O2. Record
Include, as A amended: absolute path only (that alone fixes my renamed-branch bug). Guard: path exists and `git -C <path> rev-parse --git-common-dir` equals main's. Write only after confirmed create/reuse; never copied into the worktree; fallback 2, and the only reuse path when the list call fails. B's drift risk is bounded by a "reused from record, unverified" warning. 65%.

## O3. Copy rule
Per-file walk of `<D>`, never `cp -r` (X-004). Missing: copy. Identical: skip. Differing: rename existing to one `<name>.prev` replacing any older (B), copy, name it in the warning. Skip when source and destination share a realpath (A's self-copy). Exclude `worktree.json` from the walk. 75%.

## O4. Name
`--name issue-<N>`, no `--branch`, no slug. Not irrelevant: with the marker unverified the basename fallback carries re-claims and needs the stable slug-free prefix; live `issue-305/315/330/384-*` rows prove the convention. Branch is the weaker key (divergence above). 75%.

## O5. Marker
`comment` is in the schema, empty on all 15 rows; create filling it is UNVERIFIED. Order: marker, record path, basename `^issue-<N>(-|$)`, branch tail after `refs/heads/`; drop archived, then classify stale. Merged match rule (resolves A defect 1 vs B): some live match, reuse it and mention stale; stale-only, O1 stop; two or more live, create nothing, list all. Manual run records: `comment` after create (the load-bearing unknown), actual basename, branch/prefix, create JSON shape, suffix on taken name, second claim `reused` with row count unchanged, `projectId`, unflagged byte-identity. 70% it works markerless.

## O6. Versus A and B
Agree: O1; O3 with `.prev`; O4; O5 order; self-copy; B's id-diff, empty-list guard (a registered repo always returns the `isMainWorktree` row) and real-shape fixtures.
Disagree: (1) B excludes the record; I keep it path-only and guarded, since daemon-down reuse has no substitute. (2) A's blanket "stale blocks create"; my rule reuses a live match beside a stale one, stopping only on stale-only. (3) B's "marker not required": the id set-difference only finds a row created this run; a re-claim after record loss must find an earlier row, which only marker or basename do. Keep the marker first.

## O7. Test surface
|ID|Case|Kind|Expected|
|---|---|---|---|
|ST-1|E1,E10 gates|static|claim-only; both STOPs pinned|
|ST-2|FR-4 forbidden flags|static|regex finds none|
|ST-3|Wave 7 argv, step 4|static|exact argv; no `--setup`/`--branch`/link flags|
|ST-4|Inventory|static|five refs; script named|
|ST-5|Version, decision|static|`1.1.0`; B16|
|ST-6|E12,E13 order|static|Wave 7 after steps 1-3|
|FO-1|E5 record hit|fake-orca|reuse, no orca call, re-copy|
|FO-2|E6 marker row|fake-orca|reuse, no create|
|FO-3|Marker dead|fake-orca|basename reuse|
|FO-4|E7 suffix|fake-orca|renamed, record written|
|FO-5|E2 orca absent|fake-orca|warn, null, exit 0|
|FO-6|E3 hang|fake-orca|killed at limit, exit 0|
|FO-7|E4 copy fail|fake-orca|warn, path printed|
|FO-8|Two live matches|fake-orca|create nothing, list|
|FO-9|Archived only|fake-orca|ignored, create|
|FO-10|E8 path gone|fake-orca|STALE, no create|
|FO-11|JSON opaque|fake-orca|id set-difference|
|FO-12|E11 empty list|fake-orca|warn, no create|
|FO-13|Real shapes|fake-orca|nested result, full-ref branch, 330 basename|
|FO-14|Differing file|fake-orca|one `.prev`, warning|
|FO-15|Self-copy|fake-orca|no copy|
|FO-16|Record excluded|fake-orca|absent at destination|
|FO-17|No `origin/<B>`|fake-orca|warn, no create|
|OB-1|E14,E11 live|observed|one row; `comment`, `projectId`, `.claude/` recorded|
|OB-2|Repeat claim|observed|`reused`, rows unchanged|
|OB-3|E15 unflagged|observed|byte-identical|
|OB-4|E9 from worktree|observed|`--no-parent` flat|

## O8. New defects
1. Record-in-copy loop: a copied `worktree.json` becomes `<D>/worktree.json` for a claim run inside the worktree and silently reuses stale state; exclude it (FO-16).
2. Ambiguity lock-out: creating while a matching row exists manufactures permanent "several matches" stops; O1's stop is the guard (FO-8, FO-10).3. Sufficiency: "usable" needs `.claude/` in the worktree; whether a fresh Orca worktree has it is UNVERIFIED. OB-1 records it; if absent the print adds "run `make sync-dev` there first".
