# Synthesis 02: Directory Structure and Data Flow

**Sections:** 3, 4, 6, 7
**Status:** Complete
**Date:** 2026-11-20

---

## 3. Directory Structure

Paths are repository-relative against snapshot 61ac2c2e6. Shorthand used in Sections 3, 4 and 6: `P/` = `src/superclaude/cli/issue_watch/`, `SK/` = `src/superclaude/skills/sc-issue-protocol/`, `H/` = `src/superclaude/hooks/scripts/`. Removed code is cited as `@01e7a9e23^` (removal commit 01e7a9e23, 2026-11-19 18:02 -0600 = 2026-11-20 00:02 UTC, PR #682).

```
src/superclaude/
├── cli/
│   ├── issue_watch/                  # the poller package: nine modules, no sub-package (BUILT-OFF (enabled:false) for real cycles)
│   │   ├── __init__.py               # empty
│   │   ├── runner.py                 # SubprocessRunner: the only module that imports subprocess
│   │   ├── predicates.py             # pure rules: approval, owner, edits, project, claim-marker window, order
│   │   ├── audit.py                  # REASON_TABLE, audit-line builders, AuditLog writer, stderr fallback
│   │   ├── github.py                 # G1-G7 gh argv builders, classify, CallBudget, paged reads
│   │   ├── record.py                 # FileStore, dispatch.json schema, transitions, flock, init_state, dry-run shadow
│   │   ├── launch.py                 # launch_argv, find_orca, check_origin, OrcaLauncher, outcome_of
│   │   ├── cycle.py                  # config loader, validate_approvers, run_cycle, status_report, slo_numbers
│   │   └── cli.py                    # click group issue-watch: once, status, check-config, init-state, reset
│   ├── main.py                       # registers issue-watch at lines 577-579
│   ├── install_hooks.py              # copies hook scripts to ~/.claude/hooks, merges hooks.json into settings.json
│   ├── install_ccsession.py          # wires ccsession and ccsession-orca into ~/.local/bin
│   └── issue_pipeline/               # REMOVED @01e7a9e23^ (10 files; see Appendix B)
├── commands/issue.md                 # /sc:issue front: --claim, --create (117 lines)
├── skills/
│   ├── sc-issue-protocol/            # the claim and create protocol, run by the model
│   │   ├── SKILL.md
│   │   ├── refs/                     # claim.md, create.md, labels.md, tiers.md, chains.md
│   │   ├── scripts/                  # origin_repo.py, clickup_claim.py, orca_worktree.py
│   │   └── templates/                # 15 files (claim-comment.md, launch-prompt.md, issue-summary.md ...)
│   └── ccsession-tag/                # ccsession, ccsession-orca, ccsession-models.json, hooks/session-start.sh, session-name.sh
├── agents/issue-worker-t1.md, -t2.md, -t3.md   # tier-pinned read-only claim and create workers
├── hooks/
│   ├── hooks.json                    # registrations (launch-level guard twice, job identity once)
│   └── scripts/                      # launch-level-guard.sh, launch-job-identity.sh, launch-level-pre-push.sh, require-orca-worktree-agent.sh
└── core/WORKER-CONTRACT.md           # worker and coordinator rules (WC-2 to WC-16)
plugins/superclaude/hooks/            # mirror: hooks.json (differs) and the three launch-level scripts (byte-identical)
docs/designs/                         # issue-watcher.md (942), issue-watcher-setup.md (706), sc-issue-command.md (509),
                                      # sc-issue-claim-pipeline-flag.md (470), sc-issue-launch-level-hook.md (627),
                                      # issue-pipeline-guard-g2.md (51), issue-pipeline-guard-g2-no-to.md (57), issue-pipeline-fu1.md (119)
tests/
├── issue_watch/                      # 19 test files, conftest.py, fixtures/_assumed_shape/ (19 JSON files)
├── hooks/                            # test_launch_level_guard*.py (5), test_launch_job_identity.py, test_launch_level_pre_push*.py (2),
│                                     # test_launch_level_observations.py, test_require_orca_worktree_agent*.py (2)
├── skills/                           # test_issue_protocol, _orca_worktree, _repo_resolution, _worker_agents, _t1_fallback, _l2_install,
│                                     # test_clickup_claim, test_model_alias_policy, test_worker_contract
├── commands/ and cli/                # commands/test_issue_command.py, cli/test_issue_body_templates.py, cli/test_install_hooks.py
└── unit/ and core/                   # unit/test_install_ccsession.py, unit/test_ccsession_tag.py, unit/test_ccsession_tiers.py,
                                      # core/test_orca_session_launch_guidance.py
```

### 3.1 Key file inventory

| Path | Lines | Purpose |
|------|-------|---------|
| `P/cycle.py` | 1406 | Config loader, approvers-file check, one poll cycle, `status_report`, `slo_numbers` |
| `P/github.py` | 960 | The seven read-only `gh` calls, reply classification, call budget |
| `P/record.py` | 865 | `dispatch.json` store, state machine, flock, `init_state`, dry-run shadow file |
| `P/audit.py` | 404 | Closed reason vocabulary, audit lines, rotation, stderr fallback |
| `P/launch.py` | 370 | Orca discovery, origin check, the one `orca agent launch` argv |
| `P/cli.py` | 348 | Five operator verbs, exit-code mapping |
| `P/predicates.py` | 312 | Pure eligibility predicates (no I/O, no clock) |
| `P/runner.py` | 130 | Subprocess wrapper (`shell=False`, timeout, stderr cap) |
| `src/superclaude/commands/issue.md` | 117 | `/sc:issue` flags, STOP rules, activation of the skill |
| `SK/SKILL.md` | 197 | Orchestrator protocol: waves, worker spawn rules, return contract, error table |
| `SK/refs/claim.md` | 150 | Claim waves 0 to 8, level rule, remedy lines |
| `SK/refs/create.md` / `labels.md` / `tiers.md` / `chains.md` | 99 / 67 / 58 / 40 | Create path, label and field rules, tier pins and fallback, next-step chains |
| `SK/scripts/orca_worktree.py` | 1906 | Only caller of `orca` for the claim: preflight, worktree, prompt, launch, pending, IR-4, L2 install |
| `SK/scripts/clickup_claim.py` | 270 | ClickUp lookup and at most one assignee add |
| `SK/scripts/origin_repo.py` | 195 | Resolves repo and issue number from `origin` only |
| `SK/templates/launch-prompt.md` / `claim-comment.md` | 34 / 23 | Launch prompt blocks; the posted claim comment ending `<!-- sc:issue:claim -->` |
| `src/superclaude/agents/issue-worker-t1.md` / `t2` / `t3` | 35 each | Workers pinned to `claude-gw-tier1b` / `tier2` / `tier2b` (frontmatter line 6) |
| `H/launch-level-guard.sh` | 808 | L1 guard: binds sessions, enforces the level grid, exit 0 or 2 only |
| `H/launch-job-identity.sh` | 582 | Rewrites governed Bash calls under a supervisor; `identify` answers governed, ordinary or unknown |
| `H/launch-level-pre-push.sh` | 208 | L2 git pre-push hook for pushes to main or master |
| `src/superclaude/hooks/hooks.json` | 192 | Hook registrations (plugin copy: 154 lines) |
| `src/superclaude/cli/install_hooks.py` / `install_ccsession.py` | 614 / 161 | Hook installer and ccsession wiring |
| `src/superclaude/skills/ccsession-tag/ccsession-orca` | 263 | Orca's Claude command wrapper; carries no launch level |
| `src/superclaude/core/WORKER-CONTRACT.md` | 339 | Coordinator and worker rules; no issue-pipeline duties in this snapshot |

---

## 4. Data Flow

Shorthand as in Section 3. Status words: BUILT-ON, BUILT-OFF (enabled:false), NOT BUILT, REMOVED. The pipeline has three code-backed parts that touch each other only through GitHub comments and files: the watcher (reads GitHub, starts one Orca session), the claim (`/sc:issue --claim`, writes the GitHub comments) and the guard stack (reads files under `~/.claude/state/launch-level/`).

```
 [no trigger found in snapshot]                      person types /sc:issue --claim N [--pipeline L]
            |  (a person or an outside scheduler)                       |
            v                                                           |
  superclaude issue-watch once                                          |
  BUILT-OFF (enabled:false)                                             |
   G1..G7 gh reads (no GitHub write)                                    |
            | one orca agent launch --prompt "/sc:issue --claim N --pipeline none"
            +---------------------------------------------------------->+
                                                                        v
                       claim session: assign + accuracy-check comment + claim comment (marker)
                                   |                                    |
        watcher reads marker (G4)  |            level worktree|full: worktree + launch
        next cycle -> entry claimed|                                    v
                                                      pending/<nonce> -> L1 guard binds sessions/<sid>
```

### 4.1 Watcher cycle (`superclaude issue-watch once`)

Numbered steps of `_Cycle.run` in `P/cycle.py`; "G" ids are the read-only `gh` calls of Section 4.5. Counters: shared = G1 and G2 only; per-issue non-reserved reads stop at 32 calls; the reserved re-read may use calls up to 35.

| # | Step (`P/cycle.py` lines) | GitHub read and budget | State write | On failure (word, exit) |
|---|---|---|---|---|
| 0 | `enabled` gate (685-686) | none | one cycle line | `not_enabled`, 0; dry-run ignores the gate |
| 1 | `validate_setup`: worktree is a directory, approvers file valid (687-693; 371-377) | none | one cycle line on failure | `worktree_invalid`, `approvers_invalid`, 2 |
| 2 | Lock: non-blocking flock on `state_dir/lock` (694-702; `P/record.py:380-419`) | none | none (no rotation on failure) | `lock_held`, 75; `lock_missing`, `lock_invalid`, 6 |
| 3 | `DISABLED` kill switch (712-713) | none | none, no health stamp | `disabled`, 0 |
| 4 | Load `dispatch.json` (739-750) | none | migrated store saved at once, real cycle only (746-747) | `store_missing`, `store_invalid`, 6; `rate_limited`, 5 while `now < next_permitted_at` |
| 5 | Login step (752-775) | G1, shared call 1 | `clock_skew_s` on the cycle line; warning `clock_skew` above 60 s (`SKEW_WARN_S`, 44, 774) | `gh_*`, `login_invalid`, 3; `account_id_mismatch`, 2; `rate_limited` / `rate_limit_clamped`, 5 |
| 6 | Origin check, git only (716-722) | none (not budgeted) | none | `origin_mismatch`, 2 |
| 7 | Sweep (777-792; `P/record.py:627-651`) | none | `pending` becomes `abandoned` (`pending_orphan`); `launched` past its lease becomes `abandoned` (`claim_not_observed`) | none |
| 8 | Discovery (794-808) | G2, shared call 2 | warning `discovery_count` at 80 or more | `truncated`, `discovery_duplicate`, 4; rate limit, 5 |
| 9 | Order: never-examined issues first, then oldest `considered`; first 10 (725-737; `P/predicates.py:299-312`) | none | dry-run shadow load only | none |
| 10 | Candidate loop, gates E1 to E14 in `_examine` (812-834, 915-961; detail in Section 5.1) | per-issue reads in order G4 comments, G3 events, G5 edits, G6 project items (cap 32); local gates cost no call | one decision line per examined candidate; `considered` stamp except `budget_exhausted` | skip words, 0; missing scope, `project_read_failed`, 3; rate limit, `rate_limit_clamped`, 5 |
| 11 | Launch step `_launch` (1026-1112), in order: dry-run return (1029-1035), probe (`find_orca`), prompt, re-read `_revalidate` (979-1016), day cap, DISABLED, cut-off, origin, `pending` save, `orca agent launch` | the re-read: G7, G3', G6' on the reserved calls | `pending` saved and fsynced before the launch call (1091-1092); outcome `launched` / `unknown` / `abandoned` held for the commit | `orca_not_found`, `origin_mismatch`, 2; `revalidation_failed`, `disabled_mid_cycle`, 0; `revalidation_transient`, `launch_unknown`, `spawn_error`, 7 |
| 12 | Commit (1116-1144) | none | one save of `dispatch.json` (real) or `dry-run.json` (dry-run); health stamp only with no stop reason and exit 0 | `state_dir_unwritable`, 6 |
| 13 | Conclude (1176-1211) | none | decision lines, then one cycle line, to `audit.jsonl`; rotation only with the lock held | write failure: stderr fallback line only |

```
enabled? -> setup -> lock -> DISABLED? -> load -> G1 -> origin -> sweep -> G2 -> order
                                                                              |
audit.jsonl <- conclude <- commit <- launch step <- re-read G7,G3',G6' <- candidates G4,G3,G5,G6
```

- One launch per cycle: the candidate that enters the launch step sets `launching`, then `halt` ends the loop after any launch-step outcome (`P/cycle.py:1028, 833-834`); later candidates get no read and no decision line.
- A dry-run runs steps 1 to 10 and returns at the top of step 11 (`P/cycle.py:1029-1035`): no probe, re-read, `pending` write or Orca call, so it cannot show a launch-step problem.
- [CODE-CONTRADICTED] `docs/designs/issue-watcher.md:331, 362, 621` say `find_orca` is cached per cycle (code caches nothing, `P/launch.py:6, 177`) and `:360` says entry-state candidates cost 0 calls (they read G4 first, `P/cycle.py:922-935`). Code is stronger evidence.

### 4.2 Claim flow (`/sc:issue --claim`) by wave and actor

"Orchestrator" is the Claude session that invoked the skill, not a program; only the three helper scripts are code (`SK/SKILL.md:35`). Workers are read-only and write only under `.dev/issues/` (agent files line 28 and 30). Every GitHub, ClickUp and Orca write is the orchestrator's.

| Wave | What happens | Actor | Writes outside `.dev/issues/` | Evidence |
|------|--------------|-------|-------------------------------|----------|
| 0 | `origin_repo.py --claim`, `gh auth status`, `orca_worktree.py preflight` (runs even for `--pipeline none`), default branch lookup, create `.dev/issues/<N>/` | orchestrator | none | `SK/refs/claim.md:11-21` |
| 1 | Lookup, writes `scout.md` | worker t3 | none | `SK/refs/claim.md:23-34` |
| 2 | Edge cases from `scout.md` (closed issue, assigned to another login: STOP, no writes) | orchestrator | none | `SK/refs/claim.md:36-44` |
| 3 | Assign on GitHub, then ClickUp script | orchestrator | GitHub assignee; one ClickUp assignee add | `SK/refs/claim.md:46-51` |
| 4 | Accuracy check and summary (analysis if out of date) | worker t2, or t1 when scout sizes `complex` (t1 falls back to t2 once) | none | `SK/refs/claim.md:53-63`; `SK/refs/tiers.md:34-42` |
| 5 | `Skill sc-recommend`, `next-steps.md`, resolve level, render `launch-prompt.md` | orchestrator | none | `SK/refs/claim.md:75-84` |
| 6 | Post or edit the accuracy-check comment and the claim comment | orchestrator | two comments (marked, edited on re-run) | `SK/refs/claim.md:86-96` |
| 7 | Create or reuse the worktree `issue-<N>` (no agent), copy `.dev/issues/<N>/`, close the first plain tab | orchestrator runs `orca_worktree.py worktree` | none on GitHub | `SK/refs/claim.md:98-115`; `SK/scripts/orca_worktree.py:625-738` |
| 8 | Launch an agent in the worktree (flow in 4.3) | orchestrator runs `orca_worktree.py launch` | none on GitHub | `SK/refs/claim.md:117-136`; `SK/scripts/orca_worktree.py:1696-1834` |

- `--pipeline none` (the only level the watcher sends) ends after Wave 6: no worktree, no agent, no `launch-prompt.md`, no `worktree.json` (`SK/refs/claim.md:94`; `src/superclaude/commands/issue.md:80`). The level is a code-fixed word in `P/launch.py:92`.
- The default level when `--pipeline` is omitted is a prose rule applied by the model (`SK/refs/claim.md:81`); no code computes it (BUILT-ON as text only).

**Claim-to-watcher link: how a claim comment moves a watcher entry to `claimed`**

1. The watcher's launch step saves entry `pending`, runs `orca agent launch` with `/sc:issue --claim <N> --pipeline none` and records `launched` with a 60 minute lease (`P/cycle.py:1091-1105`; `P/record.py:580-596`).
2. The claim session assigns the issue (C1) and posts the claim comment whose last line is `<!-- sc:issue:claim -->` (`SK/templates/claim-comment.md:23`; `SK/refs/claim.md:92`), then ends.
3. Next cycle, for a `launched`, `unknown` or `abandoned`-with-`pending_at` entry, the watcher reads comments with G4; the comment body becomes a boolean through `MARKER_JQ` (`P/cycle.py:922-931`; `P/github.py:61-64`).
4. `_hit` accepts a marker only when its author is the watcher's own login and its time (the later of created and updated) is at or after `pending_at` minus 300 s (`SKEW_TOLERANCE_S`), or strictly after the current approval when there is no `pending_at` (`P/cycle.py:848-865`; `P/predicates.py:17, 274-296`).
5. `_claim` then calls `record.mark_claimed` (T-10 from `launched`/`unknown`/`abandoned`; T-11 with no entry; T-12 from `failed`); `claimed` is terminal (`P/cycle.py:896-899`; `P/record.py:654-686`). A decision line `claimed` is written.
6. With no marker by lease expiry, the sweep marks `abandoned` (`claim_not_observed`, T-9); `unknown` entries never leave on the lease and cost at least one G4 read per cycle (`P/record.py:638-643`; open item O-2).
7. After the claim, nothing in the snapshot code starts a worker: no trigger found in snapshot. The hand-off text (`issue.md:85`, `SK/SKILL.md:140`, `SK/refs/claim.md:96`) is [UNVERIFIED - doc-only, no code confirmation]; the contract section that defined it is REMOVED (`CHANGELOG.md:17`; `src/superclaude/core/WORKER-CONTRACT.md` has no such section).

### 4.3 Launch-level binding flow (claim writes the pending file, the session binds it, hooks consult the session file)

Applies to claims at level `worktree` or `full` (with `--submit` the word is `full-submit`). The level travels only by files; the ccsession shim carries none (grep of `src/superclaude/skills/ccsession-tag` for launch-level terms: zero hits).

```
claim Wave 8: SK/scripts/orca_worktree.py launch                                   (cmd_launch :1696-1834)
  1 worktree record, already-launched check, stale-prompt check                    :1700-1724
  2 IR-4 enforcement preflight; fail -> W-ENFORCEMENT-ABSENT, no record, no agent  :1730-1747
  3 install_l2 then l2_status; not owned -> W-L2-ABSENT note, launch proceeds      :1754-1758
  4 publish_pending: ~/.claude/state/launch-level/pending/<32 hex nonce> = one word :1759-1761, :1488-1512
  5 orca agent launch --agent claude --worktree path:<wt> --surface terminal
        --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json   :1776-1779
  6 behind_ccsession: 5 tries x 2 s; absent -> W-LAUNCH-NOT-CCSESSION (warning only) :1802-1811
  7 record_launch -> worktree.json + <git dir>/sc-issue-launch-<N>.json              :1814
             |
             v   first UserPromptSubmit of the launched session
L1 guard (H/launch-level-guard.sh)
  match [sc-launch:v1:<32 hex>] (:318); mv pending/<nonce> -> sessions/.take-<sid> (:372-375);
  ln -> sessions/<sid> (hard link, first binding wins) (:299-313); bad word -> "degraded" = level W + note (:306)
             |
             v   every later UserPromptSubmit and PreToolUse
  sessions/<sid> exists (:257-273) -> governed: W | WA | F | FS; no record -> ordinary, exit 0 (:391)
  typed first line /sc:implement or /task at W -> sessions/<sid>.ok -> WA (:347-360)
  PreToolUse Bash: job-identity rewrites governed calls; writes requests/<token>, jobs/<kernel-sid>.json
  git push in a clone with hooks/pre-push: L2 asks `launch-job-identity.sh identify $$` -> governed | ordinary | unknown
```

- The pending record and the session record are one inode (hard link). A person releases a session by deleting `sessions/<sid>` and `sessions/<sid>.ok` (`H/launch-level-guard.sh:97`); nothing prunes `pending/` or `sessions/` (`docs/designs/sc-issue-launch-level-hook.md:627`).
- The watcher path binds nothing: `P/launch.py:33` fixes the prompt to `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` (no marker), and a `none` claim runs only `preflight` of the script. Coordinator-started workers get no marker either: `orca_worktree.py pending` has no production caller in the snapshot (only the test callers `tests/hooks/test_launch_level_guard_worker.py:287` and `tests/skills/test_issue_orca_worktree.py:2472-2498`); the guard design says it does not govern such a worker (`docs/designs/sc-issue-launch-level-hook.md:23`).
- [CODE-CONTRADICTED] `SK/refs/claim.md:125` says the L2 hook is installed "as the worktree's pre-push hook" and that IR-4 runs "before anything else"; code installs into the shared `<git-common-dir>/hooks/pre-push` (`SK/scripts/orca_worktree.py:1365, 1402`) and runs the record, already-launched and stale-prompt checks first (`:1700-1724`).
- [CODE-CONTRADICTED] `SK/templates/launch-prompt.md:23` names `/sc:task` as a releasing first line; the guard regex at `H/launch-level-guard.sh:347` accepts only `/sc:implement` and `/task`.
- The IR-7 refusal (turn a missing L2 hook into a refused launch) is BUILT-OFF (enabled:false): the switch is the constant `IR7_REFUSE = False`, not an `enabled` key (`SK/scripts/orca_worktree.py:822, 1757-1758`).

### 4.4 Trigger table: what starts each piece

| Piece | What starts it | Who or what runs it | Frequency | Evidence (path:line) | Live? |
|-------|----------------|---------------------|-----------|----------------------|-------|
| Watcher real cycle, `issue-watch once` | A run of `superclaude issue-watch once` | no trigger found in snapshot (docstring: "Run `once` from a timer"; intended every 5 minutes by a cron entry, follow-up FU-2, not installed) | none in code | `P/cli.py:98, 111-137`; `src/superclaude/cli/main.py:577-579`; `docs/designs/issue-watcher.md:15, 30, 861`; `docs/designs/issue-watcher-setup.md:288` | BUILT-OFF (enabled:false): `enabled` defaults false and a real cycle stops `not_enabled` (`P/cycle.py:228, 685-686`); no config file and no scheduler artefact ship |
| Watcher dry-run, `once --dry-run` | A person | the operator at a terminal | on demand | `P/cli.py:111-137`; `P/cycle.py:685` | BUILT-ON |
| `status`, `check-config`, `init-state`, `reset` | A person | the operator | on demand; `status` is meant for an outside alert check that does not exist (`docs/designs/issue-watcher-setup.md:557`) | `P/cli.py:164-348` | BUILT-ON |
| Watcher launch step (its only outward action) | First candidate to pass every gate in a real cycle | `OrcaLauncher.launch` inside `once` | at most once per cycle | `P/cycle.py:1099`; `P/launch.py:358-370` | BUILT-OFF (enabled:false) |
| Scheduler, dispatcher, `COORD-` coordinator worktree, zero-setup install for the issue pipeline | not found in snapshot (no cron, timer, workflow, Orca automation or such artefact; `COORD-` has zero hits) | not found in snapshot | none | negative searches in research files 01 to 03 and 06 | NOT BUILT |
| `/sc:issue --claim` typed by a person | The person types it | the orchestrating Claude session | on demand | `src/superclaude/commands/issue.md:25, 104-110` | BUILT-ON |
| `/sc:issue --claim <N> --pipeline none` launched by the watcher | The watcher launch step | an Orca terminal session in the configured worktree | at most one per cycle | `P/launch.py:33, 84-92` | BUILT-OFF (enabled:false) |
| Claim helpers `origin_repo.py`, `clickup_claim.py` | Wave 0 and Wave 3 of a claim | the orchestrator | per claim; ClickUp step skips without `CLICKUP_API_TOKEN` and `CLICKUP_WORKSPACE_ID` | `SK/refs/claim.md:14, 50`; `SK/scripts/clickup_claim.py:164-169` | BUILT-ON |
| `orca_worktree.py preflight` | every claim, including `none` | the orchestrator | per claim | `SK/refs/claim.md:17`; `SK/scripts/orca_worktree.py:210-223` | BUILT-ON |
| `orca_worktree.py worktree`, `prompt`, `launch` | Waves 7, 5 and 8 at level `worktree` or `full` | the orchestrator | per claim | `SK/refs/claim.md:98-136` | BUILT-ON |
| `orca_worktree.py pending` | no trigger found in snapshot (verb exists; only callers are two tests) | none | none | `SK/scripts/orca_worktree.py:1515-1523, 1886-1893`; `tests/hooks/test_launch_level_guard_worker.py:287`; `tests/skills/test_issue_orca_worktree.py:2472-2498` | NOT BUILT (binding and caller); the `pending` verb itself is BUILT-ON |
| Claim workers t1, t2, t3 | Waves 1 and 4 | Agent tool called by the orchestrator, `subagent_type` only | per claim | `SK/SKILL.md:54-64` | BUILT-ON |
| Coordinator hand-off after a `--pipeline none` claim | no trigger found in snapshot | none | none | `src/superclaude/commands/issue.md:85` (prose); no code or contract text (`src/superclaude/core/WORKER-CONTRACT.md`: zero hits for adopt, watcher, claim) | NOT BUILT |
| Coordinator loop rule WC-16 | A person-opened coordinator session reading the contract | no code runs it; "Phase 1 adds this duty, not a scheduler" | n/a | `src/superclaude/core/WORKER-CONTRACT.md:287-289` | BUILT-ON as instruction text only; not issue-specific |
| L1 guard | Claude Code events UserPromptSubmit and PreToolUse | the hook runner, if `superclaude install` merged hooks.json | every prompt and matched tool call | `src/superclaude/hooks/hooks.json:63-71, 115-124` | BUILT-ON |
| Job identity hook | PreToolUse with matcher `Bash`; its `identify` mode also from L2 | the hook runner; the L2 hook | every Bash call in a bound session | `src/superclaude/hooks/hooks.json:125-134`; `H/launch-level-pre-push.sh:65` | BUILT-ON |
| L2 pre-push hook | `git push` in a clone where `install_l2` placed `hooks/pre-push` | git; `install_l2` is called by `cmd_launch` | per push | `SK/scripts/orca_worktree.py:1754`; `H/launch-level-pre-push.sh:187-208` | BUILT-ON, placed only by a claim launch |
| `install_hooks`, `wire_ccsession` | A person runs `superclaude install` or `update` | the installer | on demand | `src/superclaude/cli/main.py:219, 412, 211, 406`; `src/superclaude/cli/eval/hook_adapter.py:230` | BUILT-ON |
| `ccsession-orca` | Orca runs it as the Claude command; the claim reaches it through `orca agent launch --agent claude` | Orca | per launched session | `src/superclaude/skills/ccsession-tag/ccsession-orca` header lines 2-12; `SK/scripts/orca_worktree.py:1777` | BUILT-ON (the claim only detects it) |
| IR-7 refusal of a launch | `cmd_launch` when L2 is not owned | the claim script | per launch | `SK/scripts/orca_worktree.py:822, 1757-1758` | BUILT-OFF (enabled:false), constant `IR7_REFUSE = False` |
| SLO reducer `slo_numbers` | no trigger found in snapshot (only an owner-run snippet) | none | none | `P/cycle.py:1359`; `docs/designs/issue-watcher-setup.md:457-476` | NOT BUILT as an operator surface (function exists, tested only) |
| Removed `issue-pipeline` verbs, WC-17, guard rule G2.1 | a coordinator following the old contract text | none (code deleted) | none | `CHANGELOG.md:17` (records the removal); commit 01e7a9e23 (PR #682) | REMOVED |

### 4.5 Writes to GitHub, per piece (exact commands)

`<R>` is the repo parsed from `origin` by `origin_repo.py` (the fork when `origin` is the fork); `<D>` is `.dev/issues/<N>/`. Every `gh` write of the claim passes `--repo <R>` (`SK/SKILL.md:72-74`).

**Watcher: every `gh` call is a read and the watcher writes no GitHub state.** Evidence: the only `"gh"` argv literals are five lines in `P/github.py` (177, 183, 204, 231, 255); `P/cycle.py` has no `gh`, `git`, `orca` or `subprocess` literal; the REST argv carry `--method GET` (`P/github.py:206-207, 257-258`); the GraphQL calls travel as HTTP POST but their constants hold queries only (`P/github.py:107-108`; pinned by `tests/issue_watch/test_security_invariants.py:894, 912`).

| Piece | Command (exact) | Actor | read / write | File:line | When |
|-------|-----------------|-------|--------------|-----------|------|
| Watcher G1 | `gh api user --include` | watcher | read | `P/github.py:175-177`; `P/cycle.py:755` | step 5 of every cycle |
| Watcher G2 | `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | watcher | read | `P/github.py:180-198`; `P/cycle.py:796` | step 8 |
| Watcher G3 (and G3' reserved) | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` | watcher | read | `P/github.py:201-220`; `P/cycle.py:907, 944, 996` | per candidate; re-read |
| Watcher G4 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <MARKER_JQ>` | watcher | read | `P/github.py:223-225`; `P/cycle.py:905, 926, 942` | per candidate (marker booleans only) |
| Watcher G5 | `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` | watcher | read (query only) | `P/github.py:228-244`; `P/cycle.py:948` | per candidate |
| Watcher G6 (and G6' reserved) | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> [-f after=<cursor>]` | watcher | read (query only) | `P/github.py:228-249`; `P/cycle.py:957, 1013` | per candidate; re-read |
| Watcher G7 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` | watcher | read | `P/github.py:252-262`; `P/cycle.py:983` | re-read before launch |
| Watcher non-GitHub commands | `git -C <worktree> remote get-url origin`; `<orca> skills list --json`; `<orca> agent launch --agent claude --worktree path:<worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` (12 elements) | watcher | local read; the launch starts the claim session | `P/launch.py:244, 200, 95-116`; `P/cycle.py:721, 1048, 1099` | start of cycle and before launch; probe and launch in the launch step |
| Claim C1 assign | `gh issue edit <N> --repo <R> --add-assignee @me` | orchestrator | write | `SK/refs/claim.md:48`; `SK/SKILL.md:74, 87` | Wave 3; failure stops with `E-ASSIGN-FAILED` |
| Claim C2 ClickUp (not GitHub) | `uv run --no-project python "<skill base>/scripts/clickup_claim.py" --issue-url <url> --issue-number <N> --repo <R> > "<D>/clickup.json"`, which sends `PUT https://api.clickup.com/api/v2/task/{task_id}` with body `{"assignees": {"add": [<user id>]}}` | orchestrator runs the script | write (ClickUp), only if one task matches | `SK/refs/claim.md:50`; `SK/scripts/clickup_claim.py:232-237` | Wave 3; non-fatal |
| Claim C3 accuracy-check comment | `gh issue comment <N> --repo <R> --body-file <D>/accuracy-check.md`; on re-run `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | orchestrator | write | `SK/refs/claim.md:89-91` | Wave 6; never shown for approval first |
| Claim C4 claim comment (carries the marker) | `gh issue comment <N> --repo <R> --body-file <D>/claim-comment.md`; on re-run `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/claim-comment.md` | orchestrator | write | `SK/refs/claim.md:92`; `SK/templates/claim-comment.md:23` | Wave 6; failure `E-POST-FAILED` |
| Claim C5 PR path (only `--pipeline full --submit`) | In the launched session: `gh pr list --repo <R> --head <branch> --state all` (read), a conventional commit staging `.dev/tasks` and changed files (never `.claude/`, never `.dev/issues/`), `git push origin <branch>`, `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`; never merge | the launched agent, not the claim | write | `SK/templates/launch-prompt.md:28-34` | after Wave 8, inside the session; the guard at `full-submit` allows `gh pr comment/edit/ready/create --repo`, `gh issue create/edit/comment` and canonical pushes, and still blocks merge, push to master or main, free-form `gh api` writes and `gh pr create` without `--repo` (`H/launch-level-guard.sh:554-663, 716-722, 791-800`) |
| Claim reads (no write) | `gh auth status`; `gh repo view <R> --json defaultBranchRef -q .defaultBranchRef.name`; `gh issue view <N> --repo <R> --json number,title,body,state,assignees,labels,comments,createdAt,url,author`; `gh api user -q .login`; `gh pr list --repo <R> --state merged --search "merged:>=<date>" --limit 200 --json number,title,mergedAt,files,url` | orchestrator; worker t3 | read | `SK/refs/claim.md:16-29`; `src/superclaude/agents/issue-worker-t3.md:22` | Wave 0 and Wave 1 |
| Claim create path X1 (the `--create` mode, not the claim) | `gh issue create --repo <R> --title "[FEATURE] <title>"` or `"[BUG] <title>"` with `--body-file <D>/issue-body.md`, `--label "<mode label>"` and `--type "<name>"` only when they exist | orchestrator | write | `SK/refs/create.md:92`; `SK/SKILL.md:103` | create Wave 5 |
| Claim create path X2, X3 | `gh api -X POST repos/<R>/issues/<N>/issue-field-values --input .dev/issues/<N>/complexity-field.json`; optional `gh issue comment <N> --repo <R> --body-file .dev/issues/<N>/create-review.md` | orchestrator | write | `SK/refs/create.md:95-96`; `SK/refs/labels.md:43` | create Wave 5 |
| Claim workers t1, t2, t3 | only read `gh` calls with `--repo <R>`; the one git write is `git fetch origin` | workers | read | `src/superclaude/agents/issue-worker-t1.md:28-29` (same lines in t2 and t3) | Waves 1 and 4 |
| `orca_worktree.py`, `origin_repo.py` | no GitHub write: first command words are `git` and `orca` only (`git remote get-url origin` for the script `origin_repo.py`) | orchestrator | none | `SK/scripts/orca_worktree.py` (`run([...])` first words); `SK/scripts/origin_repo.py:159-164` | per claim |
| L1 guard, job identity, L2 pre-push | no GitHub write; the guard only classifies and blocks the agent's own `gh` and `git` commands | hooks | none | `H/launch-level-guard.sh`; `H/launch-job-identity.sh`; `H/launch-level-pre-push.sh` | n/a |
| `install_hooks.py`, `install_ccsession.py`, `ccsession-orca` | no GitHub write (no network or `gh` use) | installer; Orca | none | `src/superclaude/cli/install_hooks.py`; `src/superclaude/cli/install_ccsession.py`; `src/superclaude/skills/ccsession-tag/ccsession-orca` | n/a |
| Coordinator contract text | progress posts such as issue comments are coordinator actions; no command line is given | a person-opened coordinator | write, no exact command in the text | `src/superclaude/core/WORKER-CONTRACT.md:242-243` | n/a |
| Removed `issue-pipeline` package | none: its `gh` calls were reads (`gh api user --include`, `gh api --method GET .../issues/<N>`, `.../events`, `.../comments`, `gh api graphql`); plan reply, label and Status mirror were contract text for the coordinator, no command line | n/a | none | Appendix B; `@01e7a9e23^` | REMOVED |
| Operator (a person, not code) | `gh label create ... --repo IronbellyOrg/IronClaude` (form [UNVERIFIED], not run); `gh issue edit <N> --repo IronbellyOrg/IronClaude --add-assignee @me`, `--add-label`, `--remove-label` | the person | write | `docs/designs/issue-watcher-setup.md:136-137, 161-163, 179-182` | before the watcher can see an issue |

### 4.6 Approval and gate points

The only human approval in the code is the approval label on the issue (judged against the approvers file); there is no second approval step in the watcher. The claim has no approval prompt for its posts. The one in-session approval is a typed prompt at level `worktree`.

| Gate | Piece | Condition | Closed word or exit code | Evidence |
|------|-------|-----------|--------------------------|----------|
| Enable switch | watcher | `not config.enabled and not dry_run` | `not_enabled`, 0 | `P/cycle.py:685-686` |
| Setup | watcher | worktree not a directory; approvers file not regular, symlink, wrong owner, group or other writable, over 1 MiB, bad line, or no ids | `worktree_invalid`, `approvers_invalid`, 2 | `P/cycle.py:298-361, 371-377` |
| Single instance | watcher | flock busy or lock inode replaced; lock missing or invalid | `lock_held`, 75; `lock_missing`, `lock_invalid`, 6 | `P/record.py:380-419` |
| Kill switch | watcher | `state_dir/DISABLED` exists (any type), checked at start and again before launch | `disabled`, `disabled_mid_cycle`, 0 | `P/cycle.py:712-713, 1063-1064`; `P/record.py:421-423` |
| Approval label | watcher | seven ordered rules: approval label applied by a `User` actor whose numeric id is in the approvers file, after the last trigger event and after store creation, not voided, no same-second tie | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete`, 0 | `P/predicates.py:185-234` |
| Intended owner | watcher | assignee set is not exactly the watcher's login | `unassigned`, `assigned_other`, 0 | `P/predicates.py:162-174` |
| Unchanged since approval | watcher | any issue, comment or rename time at or after approval | `edited_after_approval`, 0 | `P/predicates.py:237-259` |
| Project | watcher | not exactly one live item in the project with Status `Backlog` | `project_mismatch`, 0 | `P/predicates.py:262-271` |
| Caps and budget | watcher | day cap (`DAY_CAP`), candidates (`MAX_CANDIDATES`), call budget 32 plus 3 reserved, deadline floor, launch cut-off | `day_cap`, `budget_exhausted`, 0; `gh_timeout`, 3 | `P/cycle.py:34-47, 736, 867-876, 1069-1079`; `P/github.py:46-49, 448-454` |
| Re-read before launch | watcher | issue not open, label gone, assignee changed, approval voided or replaced, project moved | `revalidation_failed`, 0; transient, `revalidation_transient`, 7 | `P/cycle.py:979-1016` |
| Write-ahead | watcher | `pending` saved before `orca agent launch`; save failure | `state_dir_unwritable`, 6 | `P/cycle.py:1082-1092` |
| At-most-once and halt | watcher | entry `pending`/`claimed` (or launched/unknown/abandoned without a fresh marker); one launch-step outcome ends the cycle | `already_dispatched`, 0; no word | `P/cycle.py:919-933, 833-834` |
| Origin and Orca | watcher | `git remote get-url origin` is not `ironbellyorg/ironclaude` (lower-cased); no absolute `orca-ide` or `orca` listing the `orca-cli` topic | `origin_mismatch`, `orca_not_found`, 2 | `P/launch.py:163-251`; `P/cycle.py:721-722, 1048-1052, 1074-1075` |
| Operator forfeit | watcher | `reset N --forfeit-guarantee` on a state other than `abandoned` or `unknown` | `reset_refused`, 2 | `P/cli.py:232-252` |
| Orca down | claim | `orca status --json` not ok or not reachable; before any write | STOP `E-ORCA-REQUIRED` | `SK/scripts/orca_worktree.py:210-223`; `SK/refs/claim.md:17, 21` |
| Fork safety | claim | claim URL names another repo or host | STOP `E-FOREIGN-REPO`, 3 | `SK/scripts/origin_repo.py:135-140` |
| Assign and post | claim | assign fails; comment post fails | STOP `E-ASSIGN-FAILED`, `E-POST-FAILED`; no approval prompt | `SK/refs/claim.md:48, 93`; `SK/SKILL.md:76` |
| `--submit` | claim | `--submit` without explicit `--pipeline full` | STOP `E-SUBMIT-NEEDS-FULL`; script exit 2 | `src/superclaude/commands/issue.md:59`; `SK/scripts/orca_worktree.py:1900-1901` |
| Already launched, stale prompt | claim | `launch` entry in `worktree.json` or mirror; worktree prompt differs from the rendered one | `already_launched`; `W-LAUNCH-FAILED` | `SK/scripts/orca_worktree.py:1704-1724` |
| IR-4 preflight | claim | missing jq, uv or guard commands, guard not executable or old, registrations not firing, `disableAllHooks`, config dir mismatch | `W-ENFORCEMENT-ABSENT`, launch refused, no record | `SK/scripts/orca_worktree.py:955-1045, 1730-1747` |
| IR-7 refusal | claim | L2 not owned | BUILT-OFF (enabled:false); `W-L2-ABSENT` warning only | `SK/scripts/orca_worktree.py:822, 1757-1758` |
| Ship gate OB-H1 item 1, OB-H2, OB-H3 | claim | prose only: no governed claim on a real issue until they pass | NOT BUILT as a mechanism; the 12 observation tests skip | `src/superclaude/commands/issue.md:16`; `tests/hooks/test_launch_level_observations.py:79-84` |
| Typed approval | L1 guard | level `worktree`, bound session, no `agent_id`, first prompt line `/sc:implement` or `/task` | writes `sessions/<sid>.ok`, level becomes `worktree (approved)` | `H/launch-level-guard.sh:347-360` |
| Level grid | L1 guard | block IMPL and TURN at W; COMMIT, PUSH, SUBMIT, SKILL below `full-submit`; REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG at every level; the orca-verb part of ESCAPE (G2 rule 2 and the orca allow-list) recognises the command word `orca` only, so `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25 | `LL-*` words, exit 2 | `H/launch-level-guard.sh:783-803` |
| Fail closed for bound sessions | L1 guard | unparseable tool payload with a bound id, input error, unknown event, binding failure | `LL-BROKEN`, `LL-NOBIND`, exit 2; ordinary sessions and lost identity exit 0 | `H/launch-level-guard.sh:218-238, 367-392, 807-808` |
| Wrap failure | job identity | a governed Bash call cannot be wrapped | stderr text, exit 2 | `H/launch-job-identity.sh:500-502` |
| Protected push | L2 pre-push | governed or unknown actor pushes `refs/heads/main` or `master`; malformed record | `L2-PROTECTED`, `L2-UNKNOWN`, 1; `L2-MALFORMED`, 2 | `H/launch-level-pre-push.sh:187-208` |
| Session release | L1 guard | a person deletes `sessions/<sid>` and `sessions/<sid>.ok` | none; `identify` then reports `ordinary`, reason `released` | `H/launch-level-guard.sh:97`; `H/launch-job-identity.sh:252-255` |
| Plan-approval gate (plan hash, approval row, adoption row, `release-worker`, WC-17) | removed package | removed by decision; no replacement in code or contract | REMOVED | `CHANGELOG.md:17`; `@01e7a9e23^`; Appendix B |

---

## 6. State Management

The pipeline has no client-side state. Its state is three on-disk stores, each with its own writer. Shorthand as in Section 3. Mode is the file mode set by the writer.

| Store | Path pattern | Writer | Readers | Format and key fields | Notable behaviour and mode |
|-------|--------------|--------|---------|-----------------------|----------------------------|
| 1. Watcher state directory | `<state_dir>/`, default `${XDG_STATE_HOME:-~/.local/state}/superclaude/issue-watch/` (`P/cycle.py:187-192`) | `init-state` creates it (`P/record.py:753-802`) | all verbs | directory | mode 0700; a network filesystem is refused at config load (`P/cycle.py:270-272`); a lost directory loses the at-most-once memory |
| 1a. `dispatch.json` | `<state_dir>/dispatch.json` | `FileStore.save`: init-state, real cycles (`P/cycle.py:603, 747, 1092, 1097, 1143`), `reset` (`P/cli.py:224-229`) | `FileStore.load` (`P/cycle.py:742`; `P/cli.py:241`); `status` reads it without the lock (`P/cycle.py:1231-1248`); no other reader found in snapshot | JSON, sorted keys, indent 2, ASCII. Seven top-level keys: `schema_version` (1), `created_at`, `next_permitted_at`, `last_completed_cycle_at`, `considered`, `consumed_log`, `entries`. Each entry has 17 fields: `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at`, `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason`. Six states: `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed` | mode 0600; atomic write (temp file, fsync, `os.replace`, directory fsync); `pending` is saved before the launch call; any extra or missing key makes the store `store_invalid` (exit 6); `claimed` is terminal; `launch_login` and `launch_account_id` have no reader (`P/record.py:69-131, 168-244, 370-378`) |
| 1b. `lock` | `<state_dir>/lock` | nobody writes bytes; `init-state` creates it | `FileStore.lock` (`P/cycle.py:695`) | empty file used for `flock` | mode 0600; must be a regular file owned by the euid, opened `O_NOFOLLOW`; held by another run gives exit 75 (`P/record.py:380-419`) |
| 1c. `DISABLED` | `<state_dir>/DISABLED` | the operator (`touch`) | `store.disabled()` (`P/cycle.py:712, 1063`); `status` uses its mtime | existence only | any type counts for the cycle (`os.path.lexists`); `status` shows `disabled since: no` for a dangling symlink (`P/record.py:421-431`, open item O-3) |
| 1d. `audit.jsonl`, `.1` to `.4` | `<state_dir>/audit.jsonl*` | `AuditLog.append` from `_conclude` (`P/cycle.py:1200`) and `cli._write_reset` | none in code: `status` does not read it, `slo_numbers` has no production caller (`P/cycle.py:1279-1284, 1359`) | one sorted-key ASCII JSON object per line; kinds `cycle`, `decision`, `warning`; closed reason table | mode 0600; rotated at 5 MiB keeping four files, only with the lock held (`P/audit.py:106-156`); [CODE-CONTRADICTED] `docs/designs/issue-watcher.md:406` (written by every exit, read by `status`) |
| 1e. `dry-run.json` | `<state_dir>/dry-run.json` | `save_dry_run`, dry-run only (`P/cycle.py:1146-1162`) | `load_dry_run`, dry-run only (`P/cycle.py:727`) | JSON `{schema_version, considered, shadow_launches}` | mode 0600; an invalid file is replaced and warns `dry_run_shadow_reset` (`P/record.py:831-865`) |
| 1f. temp file | `<state_dir>/dispatch.json.<random>.tmp` | `write_prepared_bytes` | none | transient | an orphan after a hard crash is never removed (open item O-4) |
| 2. Launch-level store | `~/.claude/state/launch-level/` | created by the claim (`publish_pending`) and the guard; the installer never creates it | see rows 2a to 2e | directories | dirs 0700; no pruning of `pending/` or `sessions/` (`docs/designs/sc-issue-launch-level-hook.md:627`) |
| 2a. `pending/<32 hex nonce>` | `pending/<nonce>` | `publish_pending` via `launch` or `pending` (`SK/scripts/orca_worktree.py:1488-1512`) | L1 guard renames it (`H/launch-level-guard.sh:334-337, 374`); the claim deletes it if the launch fails (`:1783`) | one word: `worktree`, `full` or `full-submit`, no newline | file 0600, written as `.tmp-<nonce>` then `os.replace`d; consumed once |
| 2b. `sessions/<session_id>` | `sessions/<sid>` | L1 guard: hard link of the taken pending record (`:299-313`) or the word `degraded` (`:289-297`) | guard (`:257-273`); job identity `governed()` (`H/launch-job-identity.sh:177-186`); L2 through `identify` | one level word, read as 13 bytes; `degraded` reads as level W with a note | same inode as the pending record; first binding wins; removed only by a person |
| 2c. `sessions/<sid>.ok`, `.take-<sid>`, `.tmp-<sid>-<pid>` | `sessions/` | L1 guard (`:356-359, 372-376, 289-297`) | guard (`:270`) | `.ok` is empty, existence means approved; the dot files are temporary | `.ok` only at level W; dot names are never valid session ids |
| 2d. `requests/<32 hex token>` | `requests/` | job identity `publish()` (`H/launch-job-identity.sh:164-174`) | `run` consumes it under flock (`:378-385`) | JSON `{session_id, tool_use_id, command}` | mode 0400; single use |
| 2e. `jobs/<kernel-sid>.json` | `jobs/` | job identity supervisor (`:307-375`) | `identify` (`:215-260`), so L2 too | JSON keys `pid`, `start`, `boot`, `kernel_sid`, `session_id` | mode 0400; removed when no member process remains |
| 3. Claim artefacts | `.dev/issues/<N>/` in the checkout that ran the claim | see rows below | the orchestrator, the launched agent | markdown and JSON | never staged or committed (`src/superclaude/commands/issue.md:89-102`) |
| 3a. Worker output | `scout.md`, `accuracy-check.md`, `issue-summary.md`, `analysis/analyze-<scope>.md` | workers t3 (scout), t2 or t1 (the rest) | orchestrator; the level rule reads `issue-summary.md` | markdown from templates | written with the Write tool; "only under `.dev/issues/`" is a prose rule (`src/superclaude/agents/issue-worker-t*.md:30`) |
| 3b. Orchestrator output | `clickup.json`, `recommend.md`, `next-steps.md`, `claim-comment.md` | orchestrator (`clickup.json` is the script's stdout) | orchestrator; launched agent | one JSON object; markdown | `claim-comment.md` and `accuracy-check.md` are the posted bodies |
| 3c. Script output | `launch-prompt.md`, `worktree.json` | `orca_worktree.py prompt`; `write_record`, `record_launch` (`SK/scripts/orca_worktree.py:507-524, 1619-1643`) | `cmd_worktree`, `cmd_launch`, `cmd_prompt`; `stale_prompt` compares copies | `worktree.json` is `{"path","status","launch":{"level","submit","at"}}` | atomic write, mode 0644; `worktree.json` is never copied into the worktree and is not written for `--pipeline none` |
| 3d. Worktree copy and mirror | `<wt>/.dev/issues/<N>/*`; `<wt git dir>/sc-issue-launch-<N>.json` | `copy_issue_dir` (`:439-504`); `record_launch` (`:1634-1642`) | launched agent; `read_mirror` (`:1600`) | copy of 3a to 3c except `worktree.json`; mirror `{"path","launch"}` | copy refuses symlinks, never overwrites a tracked file, keeps a differing untracked file as `<name>.prev` |

Outside the three stores: the config file (`~/.config/superclaude/issue-watch.json`) and the approvers file are written only by the operator and read-only to the code; the claim also writes the L2 hook `<git-common-dir>/hooks/pre-push` and `pre-push.launch-level` (`SK/scripts/orca_worktree.py:1386-1442`).

---

## 7. Component Inventory

N/A - not a UI feature. The issue-to-work pipeline is a command-line poller, a prose protocol run by the model, three helper scripts and shell hooks; it has no rendered screens, components or client-side stores. The file inventory is in Section 3 and the on-disk state in Section 6.

---

## Open items carried from Sections 3, 4 and 6 (for the Open Questions section)

| ID | Item | Tag | Where used |
|----|------|-----|------------|
| O-1 | Whether anything outside the snapshot (an external cron, a person, a scheduler) runs `issue-watch once`, and whether `enabled` is true on any host. "dispatcher", `COORD-`, "zero-setup watcher" are not found in snapshot | [UNVERIFIED] | 4.4 |
| O-2 | Entries in `unknown` and `abandoned` with `pending_at` cost one G4 read in every cycle while the issue stays discovered, until a marker appears or `reset`; whether that is acceptable is an owner decision | open question | 4.2 |
| O-3 | `status` prints `disabled since: no` for a dangling-symlink `DISABLED` while `once` treats it as present | open question | 6 |
| O-4 | An orphan `dispatch.json.<random>.tmp` after a hard crash is never removed | open question | 6 |
| O-5 | Real reply shapes of `gh` (GraphQL queries, error strings, `--include` layout) and of `orca agent launch` (`receipt.operation_id`, `error.operation_id`, the lost-reply text) are assumed; all 19 fixtures are `_assumed_shape` and no live-test record exists | [UNVERIFIED] | 4.5, 4.6 |
| O-6 | That the launched claim session behaves as the prompt says, and that the Orca flags the claim uses (`--surface terminal`, `worktree create --no-parent --comment`, `terminal close --tab`) are valid in the installed Orca | [UNVERIFIED] | 4.2, 4.3 |
| O-7 | Who starts a worker after a `--pipeline none` claim (hand-off prose at `issue.md:85`, `SK/SKILL.md:140`, `SK/refs/claim.md:96`); `orca_worktree.py pending` has no production caller | [UNVERIFIED - doc-only, no code confirmation] | 4.2, 4.3, 4.4 |
| O-8 | Whether OB-H1 item 1, OB-H2 and OB-H3 have passed; the gate is prose and the 12 observation tests skip | [UNVERIFIED] | 4.6 |
| O-9 | Which side is intended for the first-line approval form: `/sc:task` in `SK/templates/launch-prompt.md:23` or only `/sc:implement` and `/task` in the guard regex | open question | 4.3, 4.6 |
