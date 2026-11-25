# Round 1 advocate statement, Variant 1 (OURS), debate D07

Abbreviations as in the position papers: REQ (owner's zero-setup requirements), DESIGN (Clay's `orchestrator.md`, line numbers are file lines), Q26 (coordinator layout, `final.md`), OA (`owner-answers.md`).

## Position

Coordinators, their sessions and their records live in each project. One dispatcher asks Orca which projects exist. OURS wins C-001, C-002, C-003, C-008 and X-001 on the weighting rule. CLAY wins C-004 and parts of C-005, C-007 and C-009 on evidence, and those parts do not depend on a separate repo, so they come in as a hybrid inside the per-project layout.

## Steelman of CLAY

The unit of control is an issue, not a session. One router under one lock, an exclusive-create state file per issue, a fail-closed in-flight count (a damaged file counts as in flight, DESIGN line 702), a `wrong_target` refusal, a resume wake for a dead session (line 710) and an idle end give every failure a defined outcome. A single org-wide search is about 8 calls, against up to 65 for a per-repo list (line 137). An allow list (`repos.yaml`) means a wide search never becomes a wide claim, and it carries per-repo settings such as merge method, reviewers and `can_merge` (lines 879-889). The code is real: `route.py` is 603 lines (verified). CLAY states its unverified facts openly. A tidy, auditable design.

## Key strengths claimed

1. **No second repository and no per-host setup (C-008).** DESIGN line 866 says the repo is "created outside IronClaude, by the person with the rights", and line 893 says the poll config holds "its absolute path on each host". REQ R17 says "Nothing in the setup is manual". Checked here: `/home/coder/workspaces/IronOrchestrator` does not exist and `orca repo list` has no orchestrator entry. That absence is expected for a per-host path, but it is the setup step R17 forbids.
2. **The session starts where the claim works (C-001).** DESIGN line 136 (ADD2): the claim reads `origin` of the current directory only, so every step needs `cd <checkout> &&`, and keeping that directory "is UNVERIFIED and is the first local end-to-end check". Ours uses a worktree whose origin is the project, checked before every launch (REQ R10; `launch.py` has `ORIGIN_MISMATCH` at line 47).
3. **Discovery by registration (C-003).** REQ R16 (line 37): one cron entry, one dispatcher, `orca repo list` each tick; R21 (line 49) records it working under `PATH=/usr/bin:/bin` (6 repos). `dispatch.py` is 479 lines with 31 test functions and `SKIP_REASONS` (line 62). This also answers X-002: skipped repos are named (`not_enabled`, `origin_mismatch`, `label_missing`, `config_invalid`).
4. **Exclusion that spans hosts (C-002, C-009).** Q26 line 50: only layout B "stops two coordinators dispatching the same issue ... with a lock git enforces across the whole project". CLAY's registry is git-ignored (DESIGN line 863), so it is per host, and DESIGN line 708 layer 4 concedes two hosts rely on the lease comment.
5. **The 65-call argument is per cycle (C-006).** `CALL_CAP = 35` (master `github.py` line 46); REQ R5 gives each repo its own config, state dir, lock and day cap. CLAY's own allow list holds three repos (DESIGN lines 879-889).

## Weaknesses identified in CLAY

1. "One per repo" is in fact many per repo (X-004): DESIGN line 706 starts a new orchestrator whenever none has room, bounded only by 6 new ids a day.
2. Nothing reads the registry yet: `route.py` exists, the reader (PR B) does not (CLAY paper, section 4).
3. Rulings are Clay's, not the repository owner's (X-001). DESIGN line 874 and line 877 write "Clay, 2026-11-19" and "Clay's recorded word" for its own settings, and line 199 shows login `clayphi`. Q26 uses `ironbelly` as the owner handle (Q26 line 12). I cannot read who issued "ruling 8" from DESIGN alone (the lines are truncated). UNVERIFIED beyond that.
4. A bad registry stops every cycle (`registry_invalid`, DESIGN line 716); CLAY admits this.
5. CLAY's "no equivalent of seen but not allowed" for an Orca list is wrong (item 3 above).

## Citation checks

Verified true: DESIGN lines 136, 137, 700-716, 866, 893, 1159; `LOOP_CAP_S`/`CHILD_TIMEOUT_S` at `dispatch.py` lines 52-53; `CALL_CAP = 35` at master line 46 (PR-A has it at line 49); `dispatch.py` 479 lines, 31 test functions; `route.py` 603 lines; REQ R5, R9, R10, R16, R17, R21 text; Q26 lines 3 and 50; `O_EXCL | O_NOFOLLOW`, `fsync`, `os.replace` in `route.py` (lines 122-129; CLAY says 120-135, close enough).

Errors and overstatements:
- **OURS overstates Q26.** OA line 23 says "direction accepted. The naming convention is NOT decided." Q26 line 3 says it "advises; it decides nothing". Q26's layout is per epic or release scope with worktrees named `coord-<dev>-<kind>-<slug>` (Q26 line 89), not one `COORD-<RepoName>` session per project. `COORD-<RepoName>` comes from REQ R9/R17 (2026-11-18), and R9's status is "decided (Coder repo)", not built. OURS paper section 3 item 1 ("the owner decided the topology") is too strong.
- OURS says the claim files give a lock git enforces. Q26 line 97 shows the lock acts at push time; the built watcher uses a local `state_dir` per repo (REQ R5), so the git claim layer is design, not code (diff-analysis A-004).
- CLAY's "decided by the owner of record" (paper section 3 item 1) rests on DESIGN's own rulings; see weakness 3.
- Not re-verified: the `gh api` and `git ls-remote` results in both papers (network; I stayed off GitHub).

## Shared assumptions

- **A-001 QUALIFY.** One host is true today (one Coder workspace), but ours must not rely on it: shared state belongs on a git branch, which is why C-009 favours Q26.
- **A-002 ACCEPT.** Six Orca repos here and three in CLAY's allow list; the call budget is not binding, so the 65-call point carries little weight.
- **A-003 QUALIFY.** Restart needs detection; REQ R9 says "restart a stopped session" without a method, and DESIGN marks the tag pattern UNVERIFIED (U25). Neither side has proved it.
- **A-004 REJECT.** Plain files do not give enough exclusion alone: `O_EXCL` covers one host only, and the git create-once lock acts at push, after a local race window (Q26 line 97).
- **A-005 QUALIFY.** Per-repo listing cannot miss an issue by truncation at 100; an org search can (DESIGN line 137, fails closed as `truncated`, index delay UNVERIFIED U8). Ours has its own `DISCOVERY_BOUND`.

## Per-point verdicts

| Point | Winner | Confidence |
|---|---|---|
| C-001 session location | OURS | 80% |
| C-002 state and records | OURS (topology); CLAY's per-issue state file adopted as hybrid | 65% |
| C-003 discovery | OURS (Orca list); CLAY's org search as optional pre-check | 65% |
| C-004 in-flight cap | CLAY, as hybrid inside per-project layout | 80% |
| C-008 setup burden | OURS | 85% |
| X-001 who decided | OURS (weighting rule; DESIGN names Clay) | 60% |
| C-005 lifecycle | CLAY (resume wake, idle end) as hybrid | 70% |
| C-006 65 calls | OURS | 70% |
| C-007 per-repo settings | CLAY as hybrid (keys only; a per-repo file under `issue-watch.d/` already exists, X-003) | 60% |
| C-009 cross-host | OURS | 65% |
| C-010, C-011, C-012, X-002 to X-005 | C-010 tie to OURS; C-011 OURS (code exists, unpushed); C-012 tie to OURS; X-002 OURS; X-003 OURS; X-004 OURS; X-005 CLAY on tidiness (OURS must pick `Coordinator` or `coordinators`) | 55 to 75% |

## Concessions

- OURS is unpushed, and its git claim layer and `.dev/coordinators/` tree are design only.
- Q26 does not settle `COORD-<RepoName>`; the owner's own branch name differs between 2026-11-14 and 2026-11-18.
- OURS has no in-flight cap, idle end, resume wake, `wrong_target` check or per-repo merge settings. CLAY has them written down; carry them in.
- One launch per sweep slows a burst. An org-wide search is cheaper if the repo count grows.
