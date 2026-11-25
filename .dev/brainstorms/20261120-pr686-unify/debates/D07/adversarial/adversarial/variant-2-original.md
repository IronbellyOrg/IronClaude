# Position paper D07, CLAY: one registry in a separate orchestrator repo, one orchestrator per repo, three issues in flight

Author role: advocate for Clay's line (design PR 681, merged; code in PR 686, open). Date 2026-11-20.

Abbreviations used below. DESIGN = `docs/designs/orchestrator.md` in `/home/coder/.cache/ic-snap-20261120/master` (merged by PR 681, "design: orchestrator"; line numbers are the file's own). PR-A = `/home/coder/.cache/ic-snap-20261120/pr-a` (PR 686, the poll that wakes the orchestrator, head `8e5ae29ad` in the snapshot). REQ = the owner's local zero-setup requirements (path in position-OURS.md); cited only where Clay's side must answer it.

## 1. The claim

Issue work for many repositories in two organizations needs one place that knows every orchestrator, every repository it may touch and every issue in flight, and that place must not be inside any one project, because the same session set works IronClaude, IronFlow and IronOrca. So: a private repository `IronbellyOrg/IronOrchestrator` holds `repos.yaml` (the allow list and per-repo settings) and a git-ignored `.orchestrator/` folder (the registry, the per-issue state files, the wake files). The poll routes each assigned issue to one orchestrator per repo, at most three issues each, and starts another orchestrator for the same repo when the first is full. One organization-wide search per login finds assigned issues across every repo.

## 2. The mechanism

1. Discovery (ADD3, DESIGN line 137, and 4.2 line 245): one GitHub search per (login, organization), `is:issue is:open assignee:<login> org:<owner>`, then filter by the allow list. About 8 calls per cycle against a budget of 35; a per-repo list "would need up to 65 calls".
2. Allow list (4.4, lines 267-304): `repos.yaml` with `orgs`, `grants` and, per repo, `checkout`, `merge_method`, `reviewers`, `can_merge`, `max_in_flight`, tiers and an overview. An issue in an unlisted repo is never claimed and becomes an information entry.
3. Routing (5.7 point 3, line 706): under `.orchestrator/state.lock` the poll takes the repo's active orchestrators in id order, picks the first below `max_in_flight`, and otherwise adds a registry entry `<short>-<n>`. The store entry is written `pending` with its target before anything is sent.
4. No double claim (5.7 point 4, line 708): four layers: one router under one lock; `wrong_target` refusal by wave 0; per-issue state file created with `O_EXCL` under a name with no orchestrator id; the claim lease comment as the last layer for two hosts.
5. Lifecycle (5.7 point 5, line 710): an orchestrator ends after 30 idle minutes; a dead one with issues in flight is restarted with the same tag and a `resume` wake; a dead one with nothing in flight is marked ended.
6. Code: `route.py` (603 lines in PR-A) implements the registry, `in_flight`, `route`, `end_finished` and `state_lock`; PR B (the orchestrator skill) is not written yet.

## 3. Cited facts

1. The topology was decided by the owner of record in the design, not left open: OD8 "Decided (ruling 9 and the creation of 2026-11-19): `IronbellyOrg/IronOrchestrator`, private" (DESIGN line 1159); ruling 8 of 2026-11-19 fixes "one orchestrator per repo, at most 3 issues in flight each" (line 700). The repo exists on GitHub: `gh api repos/IronbellyOrg/IronOrchestrator` returned `private: true`, `pushed_at 2026-11-19T03:14:05Z`, with admin rights for this login.
2. The repository list is the safety gate for a wide search. `repos.yaml` names three repos; "Every other org repo is UNVERIFIED for all of these keys and stays out of the file until the owner names it (an unlisted repo is skipped, `repo_not_listed`)" (DESIGN line 891). The search sees 17 assigned issues across the organization, 8 in IronClaude, 5 in IronOrca, 3 in Coder and 1 in Ironeye (a read-only search on 2026-11-19, DESIGN line 264, evidence E152). An Orca-registered list has no equivalent of "seen but not allowed".
3. The search costs fewer calls: "About 8 calls per cycle against the budget of 35 (`CALL_CAP`); a per-repo list would need up to 65 calls" (DESIGN line 137). The reply shape was observed once: `total_count` 17, `incomplete_results: false`, `repository_url` on each item, `rate_limit` search limit 30 (same line). A result of 100 or more fails closed as `truncated`.
4. Per-repo settings are needed for the work after the claim and have no home in a per-repo watcher config: merge method, release branch (IronClaude merges `integration` with a merge commit and `master` with a squash), reviewers, `can_merge` from the account's role, merge-safety files (DESIGN lines 879-889).
5. Concurrency control is specified and partly coded. `route.py` in PR-A counts in-flight issues from state files and the poll's own store, treats a damaged state file as "in flight" so "a damaged file can only stop new routing, never cause an extra issue", and writes the entry `pending` before any send (PR-A `route.py` module docstring, lines 1-24 of the file; DESIGN line 702). The design lists matching tests: a 4-issues-one-repo routing test, a killed-poll no-double-route test, a dead-orchestrator test, a lifecycle test, a wrong-target test (line 716).
6. Sessions that die are handled: "An orchestrator that died with issues in flight ... the poll starts `ccsession orchestrator-<short>-<n> --tier <orchestrator_tier>` again with the same tag, writes a wake with ... `target.resume: true`" (DESIGN line 710). Without a registry the poll cannot tell a dead session with work from an ended one.
7. State files are written whole and read safely: "files are replaced whole by temp file and `rename`, so a read never sees half a file" (DESIGN line 702); PR-A `_atomic_write` creates the temp file with `O_EXCL | O_NOFOLLOW` and mode 0600 and calls `fsync` before `os.replace` (`route.py` lines 120-135).
8. Names are validated: `<short>` is 12 characters, `repos.yaml` validation refuses two repos with the same `<short>`; the session tag `orchestrator-ironclaude-1` is 25 characters (DESIGN line 704, with the ccsession tag pattern `^[A-Za-z0-9._-]{1,32}$` marked UNVERIFIED, U25).
9. The design anticipates the owner's per-project objection and answers it in one line: "The single `coordinator` session ... is unchanged ... takes no issue" (DESIGN line 714); the report session stays separate.
10. Reuse, not a rewrite: the poll keeps the process runner, audit log, lock, call budget and rate-limit code of PRs 447 and 448 (the owner's merged watcher; DESIGN 4.10, line 361 onward), and the repo parameter replaces the constants at `github.py:37` and `launch.py:50` (DESIGN line 304).

## 4. What it costs

- A second repository to create and to keep (done once) and an absolute path in each host's poll config (DESIGN line 893). On this host no local clone exists and Orca does not list it.
- `.orchestrator/` is git-ignored, so state is per host. Two hosts rely on the lease comment (line 708, layer 4).
- Sessions run in the orchestrator repo, so the claim needs `cd <checkout> &&` before every shell step (ADD2, line 136), with "whether `/sc:issue` keeps that directory for all its steps" UNVERIFIED.
- `route.py` and the registry have no reader yet: PR B does not exist, so nothing on master reads a wake (analysis FULL-REPORT section 2).
- The org search has a limit of 30 requests a minute, a short indexing delay (one poll late), and fails closed at 100 results (DESIGN line 137, delay UNVERIFIED U8).

## 5. What it risks

- Divergence from the owner's recorded layout: Q26's `.dev/coordinators/`, the `COORD-<RepoName>` name and the Orca-driven discovery are all unaddressed by the design (analysis H-design681-map.md, row 5.7).
- A bad registry stops every cycle (`registry_invalid`, exit 2, DESIGN line 341).
- Day cap 6 bounds new orchestrator ids per day for the whole store, so many repos at once queue up behind it (DESIGN line 706).

## 6. What it gets right

- The unit of control is an issue with an owner, a repo, a count and a state file, not a session name. That is why a restart, a wrong delivery and an escalation each have a defined outcome.
- An explicit allow list keeps a wide search from becoming a wide claim.
- It reuses the owner's built poll rather than replacing it, and it states every unverified fact in a table (U-rows) instead of hiding it.
- The separation of the report session from the working sessions is clean, and the cap on in-flight issues per session is a real answer to "what happens when five issues arrive".

