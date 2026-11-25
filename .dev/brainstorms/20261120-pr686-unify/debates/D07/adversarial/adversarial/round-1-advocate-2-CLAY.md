# Round 1 advocate statement: CLAY (Variant 2), debate D07

## Position

Under the owner's weighting rule, CLAY should not win the topology itself. Where the session runs, where records live and how repos are found are the contested rule, and OURS has the owner's own decisions behind it (Q26, REQ R16, R9). CLAY's real case is a set of capabilities that OURS lacks and that do not need a separate repository: the in-flight cap, fail-closed counting, `wrong_target`, restart of a dead session with a resume wake, the 30-minute idle end, the per-repo settings table, and an org-wide search as a cheap pre-check. I argue those are adopted as a hybrid inside the per-project layout, and that the rest goes to OURS. "They" below means Clay.

## Steelman of OURS

OURS is the topology the repository owner (login `ironbelly`) ruled on three times (Q26 line 3, REQ R16 line 37, REQ R9 line 40). Orca is already where a project is registered, so one act adds a project. The session starts in a worktree whose `origin` is the project, so CLAY's `cd <checkout> &&` workaround and its UNVERIFIED directory question (DESIGN line 136) never arise. Nothing is hand-kept: no second repo, no `repos.yaml`, no absolute path per host (DESIGN lines 866, 893). The dispatcher is real code: `dispatch.py` is 479 lines, `test_dispatch.py` has 31 test functions (I counted both). `orca repo list` was shown to work under cron's minimal environment (REQ R21, line 49). A shared git branch with create-once claim files is a sound idea for developers who each run several coordinators.

## Key strengths claimed (CLAY)

1. **A cap on work in flight exists in CLAY and nowhere in OURS.** DESIGN line 702 defines "in flight" and line 706 routes by it. I grepped `src/superclaude/cli` on the owner's branch for `max_in_flight`, `in_flight` and `.dev/coordinators`: zero hits. OURS answers "five issues arrive" only with "one launch per sweep" (REQ R5), which is a rate brake, not a cap.
2. **Fail-closed counting.** "a file it cannot parse counts as in flight" (DESIGN line 702); `route.py` docstring lines 22-24 says the same, and `_atomic_write` uses `O_EXCL | O_NOFOLLOW`, `fsync`, then `os.replace` (lines 122-129). OURS has no equivalent rule.
3. **Dead sessions with work are restarted and told to resume** (DESIGN line 710, `target.resume: true`). OURS says "restart a stopped session" (REQ R9) but `dispatch.py` has no session code: its only worktree reason is `worktree_invalid` (line 69, used at line 280) and there is no `COORD-` string at all.
4. **A per-repo settings table** (merge method, release branch, reviewers, `can_merge`, safety files; DESIGN lines 879-889) covers work after the claim. OURS has no home for these keys yet, although `issue-watch.d/<repo>.json` could hold them.
5. **Org-wide search** costs about 8 calls against `CALL_CAP = 35` (DESIGN line 137; `github.py:49`). Its value is as a pre-check before starting a child, not as the topology.

## Weaknesses identified in OURS

1. **The central element does not exist yet.** The `Coordinator` worktree is absent on this host (`ls /home/coder/workspaces/worktrees/*/Coordinator` fails). REQ R9, R10 and R17 are marked "decided (Coder repo)", not built; R20 and R21 are "open". `dispatch.py:280` returns `worktree_invalid` when the worktree is missing, so the built dispatcher skips every repo today. `.dev/coordinators/` is also absent from the master snapshot (OURS admits this).
2. **Q26 settles a different thing than the poll needs.** Q26 line 6 defines a coordinator as a session that "keeps the program's records and hands work to workers" (a decision ledger, grants, briefs). It does not define per-repo issue sessions or in-flight counts. REQ R9 later merges the duties, but the layout was never tested for the poll's job.
3. **The git exclusion is untested.** A create-once claim file refuses a second creator at push time, after a pull (A-004). No code in OURS uses `.dev/coordinators/` (zero grep hits), and owner-answers line 80 drops branch protection, leaving the no-force-push rule on paper only.
4. **Branch naming is unsettled**: `coordinators` exists on origin (owner-answers line 81), while REQ R10 names `Coordinator`, and R20 says `Coordinator` is absent on the remote.
5. **A single dispatcher is a single point of failure** for every project (OURS admits this in its section 5).

## Citation checks

Verified correct: DESIGN lines 136, 137, 700-710 and 1159; REQ R5, R9, R10, R16, R17, R20, R21 text and line numbers; `dispatch.py` lines 52-53 and 479 lines; `route.py` 603 lines and its docstring; `github.py:37` and `launch.py:50` hardcoded repo constants on master.

Errors found:
- **OURS** cites `CALL_CAP` at `github.py` line 46; it is at line 49 (both on the owner's branch and in PR-A). Minor.
- **OURS** says the topology "is built, not only planned" (section 3, point 4). True only of the dispatcher; the session, worktree, branch and records layout are not (weakness 1).
- **OURS** cites R21 as clearing the cron risk; the R21 row is still marked "open" (the later `gh` check is at REQ line 97 and line 110).
- **CLAY** says the topology was "decided by the owner of record" (section 3, point 1). The design's own header says "approved by the owner (Clay)" (DESIGN line 3) and "the user means ... (Clay)" (line 11). Rulings 8 and 9 are Clay's, not the repository owner's. This overstatement is CLAY's most serious citation error.
- **CLAY** presents the O_EXCL per-issue state file and the idle end as part of the mechanism; they are PR B work that does not exist (`route.py` holds the registry and routing only).
- I did not run `orca repo list` or `gh api` (read-only, no Orca or GitHub contact); the "6 repos" and "private repo exists" claims in both papers are UNVERIFIED by me.

## Shared assumptions

- **A-001 QUALIFY**: one host is true today (one cron entry), which makes CLAY's host-local registry adequate and OURS's cross-host git lock unneeded now; both fall back to GitHub's lease comment for two hosts (DESIGN line 708).
- **A-002 ACCEPT**: six Orca repos and three allow-listed; the "65 calls" argument (line 137) is weak, and OURS's per-child budget answer (REQ R5) is fair.
- **A-003 QUALIFY**: tag detection is UNVERIFIED in CLAY (U25, DESIGN line 704) and absent in OURS (no `COORD-` code); both restart claims rest on it.
- **A-004 QUALIFY**: `O_EXCL` excludes only on one host; a git create-once file excludes at push, not at create; neither was tested.
- **A-005 QUALIFY**: an org search fails closed at 100 results and has an UNVERIFIED index delay (line 137), and one failure blinds a whole org; per-repo discovery isolates failures.

## Per-point verdicts

| Point | Winner | Confidence |
|---|---|---|
| C-001 session location | OURS | 85% |
| C-002 state and records | OURS (shared branch), with CLAY's per-issue state file adopted | 65% |
| C-003 discovery | OURS; org search only as a pre-check | 75% |
| C-004 in-flight cap | CLAY, as a hybrid into OURS | 85% |
| C-005 lifecycle | CLAY (restart with resume, idle end), as a hybrid | 70% |
| C-006 65-call budget | OURS | 75% |
| C-007 per-repo settings | CLAY, as hybrid keys in `issue-watch.d` | 70% |
| C-008 setup burden | OURS | 80% |
| C-009 cross-host exclusion | OURS in principle, untested | 55% |
| C-010 names | OURS | 90% |
| C-011 maturity | Tie, which goes to OURS | 55% |
| C-012 org scope | CLAY (two orgs), need UNVERIFIED | 50% |
| X-001 who decided | OURS | 90% |
| X-002 seen but not allowed | OURS (skip reasons exist) | 65% |
| X-003 settings home | OURS can host them | 65% |
| X-004 "one per repo" | OURS (the label hides many) | 70% |
| X-005 branch naming | Neither; both unsettled | 50% |

## Concessions

- CLAY's rulings are Clay's own (DESIGN lines 3 and 11), so they cannot override the owner's recorded layout.
- The separate repo adds a manual per-host step and a `cd` workaround with an UNVERIFIED premise; OURS is cheaper on both.
- CLAY's registry has no reader yet (PR B unwritten) and is git-ignored, so state is per host.
- The topology as a whole should go to OURS; I claim only the cap, fail-closed counting, resume restart, idle end and settings table, which move into the per-project layout.
