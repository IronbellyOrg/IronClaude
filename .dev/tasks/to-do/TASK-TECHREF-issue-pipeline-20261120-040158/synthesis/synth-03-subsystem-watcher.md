# Synthesis 03: Watcher Subsystem

**Sections:** 5.1
**Status:** Complete
**Date:** 2026-11-20

## 5. Subsystem Reference

### 5.1 Issue watcher

Paths are relative to the 61ac2c2e6 snapshot. `P` = `src/superclaude/cli/issue_watch/`. `DES` = `docs/designs/issue-watcher.md`, `SET` = `docs/designs/issue-watcher-setup.md`.

**Purpose:** `superclaude issue-watch once` is a one-shot poll cycle. It reads GitHub (read-only `gh`), decides which approved issue is eligible, records that decision in a local store, and starts at most one Orca session that runs `/sc:issue --claim <N> --pipeline none`. It never writes to GitHub; the launched session does (P/launch.py:84-92).

**Status: BUILT-OFF (enabled:false).**

| Fact | Evidence | Tag |
|---|---|---|
| `enabled` defaults to false and must be a JSON boolean; the real cycle stops `not_enabled` (exit 0) before validation, lock and any external call | P/cycle.py:228-230, 685-686 | [CODE-VERIFIED] |
| `once --dry-run` ignores `enabled` and is BUILT-ON; it stops before the launch step (P/cycle.py:1029-1035) | P/cycle.py:685 | [CODE-VERIFIED] |
| No shipped config file; with none, `load_config` raises `config_invalid` | no `**/issue-watch*.json` in snapshot; P/cycle.py:206-213 | [CODE-VERIFIED] |
| Scheduler artefact (cron, systemd, launchd, GitHub Action, Orca automation) | not found in snapshot (greps over P, `.github`, `.claude`, `plugins`, `scripts`, Makefile, `pyproject.toml`, `package.json` return nothing; research 03 F.2). DES:30 and SET:288 record the cron entry (FU-2) as out of scope: "This work does not install or enable the entry" | [CODE-VERIFIED] by absence; status NOT BUILT, see Section 14 |
| Dispatcher, `COORD-<RepoName>` worktree, zero-setup install | not found in snapshot (`COORD-` returns 0 hits; no dispatcher for the issue pipeline) | not found in snapshot |
| Live-test record `docs/designs/issue-watcher-live-test.md` | not found in snapshot; only `issue-watcher.md` and `issue-watcher-setup.md` exist; DES:33 says the owner writes it. All 19 `_assumed_shape` fixtures are still assumptions | NOT BUILT, see Section 14 |
| "Implemented and merged in PRs #447 and #448; never run live" (DES:3) | no history or runtime state in a snapshot; the 19 assumed fixtures are consistent with it | [UNVERIFIED - doc-only, no code confirmation] |
| Whether `enabled` is true in the owner's real config, and whether anything outside the snapshot runs `once` | not visible in a snapshot | [UNVERIFIED] |

**Key files** (all under `P`; no module outside `P` touches `dispatch.json`, `audit.jsonl` or `dry-run.json`):

| Module | Lines | Role |
|---|---|---|
| `cycle.py` | 1406 | config loader, setup validation, `_Cycle` (the poll cycle), exit resolution, `status_report`, `slo_numbers` |
| `github.py` | 960 | the seven read-only `gh` argv builders, reply classifier, paged reads, `CallBudget`, rate-limit time |
| `record.py` | 865 | `FileStore`, `dispatch.json` schema, pure state transitions T-1..T-13, flock, atomic save, `init_state`, dry-run shadow |
| `launch.py` | 370 | Orca discovery, origin check, the one fixed `orca agent launch` argv, reply mapping |
| `predicates.py` | 312 | pure rules: approval replay, owner, edits, project Backlog, marker window, candidate order |
| `audit.py` | 404 | closed 59-word `REASON_TABLE`, audit line builders and schema, rotation, stderr fallback |
| `cli.py` | 348 | Click group `issue-watch`, five verbs, exit-code mapping (registered at `src/superclaude/cli/main.py:577-579`) |
| `runner.py` | 130 | the only module importing `subprocess` (`shell=False`, closed stdin, mandatory timeout, stderr cap 500 bytes) |

Pinned by `tests/issue_watch/test_module_boundaries.py` (nine modules, import allow-list) and `test_no_shell.py`.

**Dependencies and consumers.** Depends on `gh`, `git`, an Orca CLI (`orca-ide` then `orca`, `_ORCA_CLIS` at `src/superclaude/cli/install_user_setup.py:36`) and `swarm/atomic.py` (function-level import, record.py:372). Consumers: the operator and, by design only, an external timer (not found in snapshot). The launched claim session is the only downstream effect (Section 5.2).

---

#### 5.1.1 Poll cycle (decision engine)

Entry: `run_cycle(deps, dry_run)` (P/cycle.py:1214) builds `_Cycle` and calls `_Cycle.run` (682). Three private exceptions steer it: `_Skip(reason)` ends one issue, `_Stop(reason, stamp)` ends the cycle, `_Transient` marks a re-read timeout or 5xx.

```
once -> [0 enabled?]-no->  cycle line not_enabled (exit 0, no lock, no call)
          |yes/dry-run
        [1 validate_setup: worktree dir, approvers file]-bad-> exit 2
        [2 flock state_dir/lock]-held-> exit 75 | missing/invalid-> exit 6
        [3 DISABLED file?]-yes-> exit 0 `disabled`
        [4 load dispatch.json; now < next_permitted_at?]-> exit 6 | exit 5
        [5 G1 gh api user: login, account pin, clock skew]
        [6 git origin check] -> exit 2 origin_mismatch
        [7 sweep: pending->abandoned, expired launched->abandoned]
        [8 G2 discovery (trigger label + own login)]
        [9 order: never-examined first, max 10]
        [10 per candidate: E1..E14 gates, reads G4,G3,G5,G6]
              first launch-step outcome -> halt (no later candidate read)
        [11 _launch: re-read G7,G3',G6', DISABLED, origin, pending save, orca launch]
        [12 one commit: dispatch.json (real) or dry-run.json (dry)]
        [13 decision lines, then ONE cycle line -> audit.jsonl; rotate if locked]
```

Cycle steps (P/cycle.py; all [CODE-VERIFIED] against DES 6.2 except where marked in 5.1.9):

| # | Step (lines) | Stop or skip reason, exit |
|---|---|---|
| 0 | `enabled` gate (685-686) | `not_enabled`, 0 |
| 1 | `validate_setup` (688, 371-377) | `worktree_invalid`, `approvers_invalid`, 2 |
| 2 | `store.lock()` (695, record.py:380-419) | `lock_held` 75; `lock_missing`, `lock_invalid` 6 |
| 3 | DISABLED kill switch (712-713) | `disabled`, 0 (no health stamp) |
| 4 | store load, migrated store saved (real only, 746-747), `next_permitted_at` (748-750) | `store_missing`, `store_invalid` 6; `rate_limited` 5 |
| 5 | login G1 (752-775) | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` 3; `account_id_mismatch` 2; rate limit 5; warning `clock_skew` |
| 6 | origin check (716-722) | `origin_mismatch` 2; no time left `gh_timeout` 3 |
| 7 | sweep (777-792, record.py:627-651) | decision lines `pending_orphan`, `claim_not_observed` (state `abandoned`), exit 0 |
| 8 | discovery G2 (794-808) | `truncated`, `discovery_duplicate` 4; rate limit 5; warning `discovery_count` at >= 80 |
| 9 | order, `[:MAX_CANDIDATES]` = 10 (725-737, predicates.py:299-312) | none; dry-run uses the `dry-run.json` shadow map |
| 10 | candidates (812-834, `_examine` 915-961) | skip words in 5.1.1.1 |
| 11 | `_launch` (1026-1112) | table in 5.1.1.2 |
| 12 | `_commit` (1116-1126) | `state_dir_unwritable` 6 |
| 13 | `_conclude` (1176-1211) | decision lines first, then exactly one cycle line |

Exit resolution (cycle.py:462-482): precedence 2, 6, 7, 5, 3, 4; 75 only when it is the sole non-zero condition; else 0. The cycle never produces exit 1 (only `once` writes `cycle_crashed`, cli.py:123-129). The cycle-line reason is a stop reason, else the first condition reason matching the exit code, else `cycle_complete` (1164-1174). Health stamp (`last_completed_cycle_at`) is written only when no stop reason is set and the exit is 0, real cycle only (1138-1139).

##### 5.1.1.1 Per-candidate gate order (`_examine`, cycle.py:915-961)

Any `_Skip` writes one decision line (exit 0) and every skip except `budget_exhausted` stamps the issue in `considered` (831-832), which sorts it behind never-examined issues next cycle.

| Gate | Condition | Word (state) | GitHub reads |
|---|---|---|---|
| E1 (919-921) | entry `claimed` or `pending` | `already_dispatched` | 0 |
| E2 (922-931) | entry `launched`, `unknown`, or `abandoned` with `pending_at`; own marker found | `claimed` (T-10) else `already_dispatched` | G4 |
| E3 (932-933, 901-913) | `abandoned` tombstone (`attempts_exhausted`) | `claimed` or `already_dispatched` | G4, G3 |
| E4 (934-935) | `failed` entry still in backoff | `claimed` or `in_backoff` | G4, G3 |
| E5 (936-937, 867-876) | day cap reached (6 per 24 h, plus dry-run shadow launches) | `day_cap` | 0 |
| E6 (938-940) | assignee set != {own login} | `unassigned`, `assigned_other` | 0 |
| E7 (941-943) | marker read | `marker_unreadable` | G4 |
| E8 (944) | events read | `events_unreadable`, `events_incomplete` | G3 |
| E9 (945, 878-894) | approval replay (7 rules) | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete` | 0 |
| E10 (946-947) | own marker after current approval | `claimed` (T-11 / T-12); no launch | 0 |
| E11-E12 (948-956) | edits read; any edit, comment or rename at or after approval time | `edits_unreadable`; `edited_after_approval` | G5 |
| E13-E14 (957-960) | project items; exactly one live item in the configured project with status `Backlog` | `project_unreadable`; `project_mismatch` | G6 |
| E15 (961) | `_launch` | see 5.1.1.2 | - |

Read failures: `rate_limited` raises `_rate_stop` (+3600 s, `rate_limit_clamped` 5, 663-668); `scope_missing` raises `project_read_failed` 3 (842-843); an unavailable call is `budget_exhausted` (skip, not stamped, loop continues).

##### 5.1.1.2 Launch step (`_launch`, cycle.py:1026-1112)

`c.launching = True` is the first line (1028); after the step returns or raises `_Skip`, the loop sets `halt` (833-834).

| Order | Check or action (lines) | Failure word, exit |
|---|---|---|
| dry-run | `would_launch = n`, shadow launch time appended, return `launched` with no state; no probe, re-read, Orca or write (1029-1035) | - |
| probe | `find_orca` (1048-1052) | `orca_not_found` 2 (stamped); out of time `budget_exhausted` |
| prompt | `build_claim_prompt` (1054-1056) | `prompt_invalid` 7 (unreachable for discovered issues; only test_cycle.py:3348) |
| re-read | `_revalidate` (979-1016): G7 state open and both labels present, owner again, G3' same approval event id, G6' project | `revalidation_failed`, `unassigned`, `assigned_other` (0); timeout or 5xx `revalidation_transient` 7. Edits are not re-read (1006) |
| guards | day cap again (1061), DISABLED again (1063-1064), launch cut-off 120 s (1069, 1078, 1095), origin again (1074-1075) | `day_cap`; `disabled_mid_cycle` 0; `budget_exhausted`; `origin_mismatch` 2 |
| write-ahead | `mark_pending` T-4 then `_save()` (1082-1092); if the save crossed the cut-off, restore and save again (1095-1098) | save failure `state_dir_unwritable` 6 |
| launch | `launcher.launch(orca, worktree, prompt, 120.0)` (1099) | outcome words below |

Outcomes: `launched` (T-5), `launch_unknown` exit 7 (T-6), `spawn_error` exit 7 (T-7).

**Dry-run versus real** (cycle.py): a dry-run runs steps 1-10, honours DISABLED and a persisted `next_permitted_at`, never saves a migrated store, never persists a rate limit, replaces a corrupt `dry-run.json` with a shadow (warning `dry_run_shadow_reset`), writes `dry-run.json` only when something was examined or would launch, writes audit lines with `dry_run: true` and no `state`, never writes `dispatch.json` or the health stamp (639, 685, 727-735, 746-747, 1029-1035, 1146-1162). It cannot reveal a probe, re-read or launch-step problem.

---

#### 5.1.2 GitHub I/O (`P/github.py`)

**The watcher never writes to GitHub.** Evidence: the five `"gh"` list literals in `P` are all in github.py (177, 183, 204, 231, 255) and all are reads; `cycle.py` holds no `gh`, `git`, `orca` or `subprocess` literal; no `POST|PATCH|PUT|DELETE|mutation` string exists in github.py except the comment at 107-108 and the two `--method GET` lines (206, 257); the GraphQL constants hold queries only (pinned by `test_security_invariants.py`, `test_github.py`). The repository is the literal `IronbellyOrg/IronClaude` (github.py:37). [CODE-VERIFIED]

| Id | Exact argv (`<>` = validated value) | Budget class | Called at |
|---|---|---|---|
| G1 | `gh api user --include` | shared | cycle.py:755 |
| G2 | `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | shared | 796 |
| G3 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` | per-issue (G3' reserved) | 907, 944, 996 |
| G4 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <MARKER_JQ>` | per-issue | 905, 926, 942 |
| G5 | `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` | per-issue | 948 |
| G6 | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> [-f after=<cursor>]` | per-issue (G6' reserved) | 957, 1013 |
| G7 | `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` | always reserved | 983 |

Builders: github.py:175-262. The comment projection `MARKER_JQ` turns the comment body into a boolean (no title, body or comment text is requested).

| Mechanism | Fact |
|---|---|
| `CallBudget` (github.py:437-463) | `CALL_CAP` 35 (46), `RESERVED_CALLS` 3 (49): non-reserved per-issue reads refuse at 32, reserved reads (G7, G3', G6') up to 35; G1 and G2 are shared and never refused, so at most 37 calls per cycle, 2 on an idle cycle |
| Paging | `PAGE_SIZE` 100, `PAGE_CAP` 5; repeated id, page cap or malformed item gives an incomplete or unreadable read |
| Deadline | `DEADLINE_TOTAL_S` 240, call floor `GH_FLOOR_S` 5, per-call `GH_TIMEOUT_S` 20 (cycle.py:37, 41-42, 418-427); a refused call is a skip `budget_exhausted` (per-issue) or `gh_timeout` (G1, G2) |
| `classify` (345-371) | timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed; the stderr and GraphQL error strings (`GH_ERROR_SIGNS`, 267-277) are marked `[UNVERIFIED]` in source |
| Rate limit | headers readable only for G1 (`--include`); `rate_limit_wait` (418-431): `Retry-After` or `x-ratelimit-reset` within 1..3600 s gives `rate_limited`, else now + 3600 s `rate_limit_clamped`; every G2 or per-issue limit clamps (cycle.py:663-668); stored in `next_permitted_at`; both exit 5 |

The GraphQL reply shapes, the cursor alphabet and the `--include` header layout are [UNVERIFIED]: all 19 `tests/issue_watch/fixtures/_assumed_shape/*.json` fixtures are assumptions (pinned by `test_github.py:575-597`); a wrong shape fails closed (read skipped, issue skipped).

---

#### 5.1.3 Launch and dispatch record

**Launch** (`P/launch.py:95-116`): exactly 12 argv elements, `ORCA_AGENT` fixed to `claude`, no permission flag, no model flag, run with `cwd=<worktree>` and a 120 s timeout:

`<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json`

`<orca>` is the absolute path chosen by `find_orca`: `orca-ide`, then `orca`, accepted only when `skills list --json` lists topic `orca-cli` (163-203, not cached). The prompt matches `PROMPT_PATTERN` (33) and the level `none` is hard-coded (3 occurrences of `--pipeline`, all in launch.py). The watcher creates no worktree: `--worktree` is the operator-set `worktree` config value. Origin check: `git -C <worktree> remote get-url origin` must equal `ironbellyorg/ironclaude` lower-cased (233-251).

**Reply handling** (`outcome_of`, 326-349), in order: spawn failure `spawn_error`; timeout, `agent_session_operation_unknown` text, non-zero exit, non-JSON, missing id at `receipt.operation_id` / `error.operation_id`, or an id outside `^[A-Za-z0-9._:-]{1,128}$` all give `unknown`; else `launched` with the id. The reply shapes (`OPERATION_ID_PATHS` 42-45, `OP_UNKNOWN_TEXT` 47) are [UNVERIFIED] (`[PROPOSAL, UNVERIFIED]` in source). `LaunchOutcome.detail` is set but never read (see 5.1.7). The watcher learns the result only when a later G4 read sees the session's own claim marker (`_hit` cycle.py:848-865, then `_claim` T-10).

**`dispatch.json`** (`<state_dir>/dispatch.json`, mode 0600, `P/record.py`): 7 top-level keys (`schema_version` 1, `created_at`, `next_permitted_at`, `last_completed_cycle_at`, `considered`, `consumed_log`, `entries`); each entry has 17 fields (record.py:69-88: `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at`, `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason`); six states `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed` (34-36). Any extra or missing key makes the store `store_invalid` (exit 6).

| T | Transition (record.py function) | Trigger |
|---|---|---|
| T-1, T-3 | none or `failed` -> `failed`; third failure -> `abandoned` `attempts_exhausted` (`fail` 503-525) | `prompt_invalid`, `revalidation_transient` (MAX_ATTEMPTS 3) |
| T-2 | `failed` eligible again (`backoff_elapsed` 528-535) | 10 min backoff |
| T-4 | none or `failed` -> `pending`, `launches=1` (`mark_pending`) | all checks passed, saved before the launch |
| T-5, T-6, T-7 | `pending` -> `launched` (lease 60 min), `unknown`, `abandoned` `spawn_error` | launch outcome |
| T-8, T-9 | `pending` -> `abandoned` `pending_orphan`; `launched` past lease -> `abandoned` `claim_not_observed` (`sweep` 627-651) | start of next cycle |
| T-10, T-11, T-12 | `launched`/`unknown`/`abandoned`, none, `failed` -> `claimed` (`mark_claimed` 654-686) | own claim marker seen (window: at or after `pending_at` minus 300 s, else strictly after the approval) |
| T-13 | `abandoned`/`unknown` -> entry removed (`reset_entry` 706-720) | `reset N --forfeit-guarantee` |

`claimed` is terminal; `unknown` leaves only through a marker or `reset`. Any other (state, trigger) pair raises `TransitionError`.

**Write path.** Save = `json.dumps` sorted, indent 2, ASCII; `write_prepared_bytes` (mkstemp in the same directory, fsync, `os.replace`), `chmod 0600`, directory fsync (record.py:370-378). Lock = non-blocking `flock(LOCK_EX|LOCK_NB)` on `state_dir/lock` (pre-created by `init-state`, `O_NOFOLLOW`, regular file owned by the euid, inode re-checked after locking; held means exit 75) (380-419). Dry-run uses `dry-run.json` (`considered`, `shadow_launches`) and never touches `dispatch.json` (831-865).

**Crash points** (pinned by `test_crash_injection.py`: one crash per point, then five more cycles, launcher called at most once in all six runs): C1 before the pending save (store untouched), C2 during the atomic replace (old file kept; orphan `*.tmp` ignored), C3 after the pending save (swept to `pending_orphan`, never launched), C4 after the spawn (swept, never relaunched), C5 after the outcome save (only audit lines lost).

**DISABLED kill switch.** `os.path.lexists(state_dir/DISABLED)` (record.py:421-423; a dangling symlink counts), checked at step 3 and again before the pending write (`disabled_mid_cycle`). Nothing in `P` creates or removes the file.

---

#### 5.1.4 Operator surface (`P/cli.py`)

Five verbs, each with `--config` (default `~/.config/superclaude/issue-watch.json`, `~` expanded for the option only; cli.py:31, 49-59). `test_cli.py` pins "exactly five commands".

| Verb | Options | Effect | Platform check |
|---|---|---|---|
| `once` | `--dry-run` | the cycle of 5.1.1; prints `cycle: <reason>`, `exit: <code>`, dry-run adds `probe:` and `would_launch:` (cli.py:111-137) | yes |
| `status` | `--json` | local read of `dispatch.json` and `DISABLED` mtime; no lock, no `gh`, never reads `audit.jsonl` (cycle.py:1270-1335); `healthy` = a real stop-free exit-0 cycle within `HEALTH_AGE_S` 900; stale = `unknown` or `pending_orphan` older than 86400 s; prints (never runs) a `--retry-launch` argv for `unknown` entries | no |
| `check-config` | - | static check: config, worktree directory, approvers file; no `gh`, no Orca, no origin check (cli.py:185-198) | yes |
| `init-state` | - | creates `state_dir` 0700, `lock` 0600, `dispatch.json` 0600; refuses an existing store (exit 6) (record.py:753-802) | yes |
| `reset` | `ISSUE --forfeit-guarantee` or `--rate-limit` | removes an `abandoned` or `unknown` entry (T-13), or clears `next_permitted_at`; writes one audit line under the lock (cli.py:282-348) | yes |

Exit codes of `once` (reasons from `audit.REASON_TABLE`; `status` also returns 1 for unhealthy, 6 store error, 2 config error):

| Exit | Meaning | Words |
|---|---|---|
| 0 | finished or deliberate no-op | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`, all skip and entry-success words |
| 1 | crash (stderr line only) | `cycle_crashed` (cli.py:123-129) |
| 2 | config or environment | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch`; `reset_refused` |
| 3 | GitHub read failure | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` |
| 4 | incomplete discovery | `truncated`, `discovery_duplicate` |
| 5 | rate limit | `rate_limited`, `rate_limit_clamped` |
| 6 | state store | `store_missing`, `store_invalid`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` |
| 7 | launch-path entry failure | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` |
| 75 | lock held (only as sole condition) | `lock_held` |

**Config** (`load_config`, cycle.py:195-283; JSON, strict, unknown keys rejected, no `~` expansion, network filesystem `state_dir` refused; full table in Section 9):

| Key | Default | Rule |
|---|---|---|
| `schema_version` | required | integer 1 |
| `enabled` | `false` | JSON boolean |
| `labels.trigger`, `labels.approval` | `issue-watch:trigger`, `issue-watch:approved` | 1-50 chars, no comma, quote, control char or leading `-`; must differ |
| `project_id` | required | `PVT_[A-Za-z0-9_-]{1,64}` |
| `owner_account_id` | none | optional pin; mismatch is `account_id_mismatch` |
| `worktree`, `approvers_file` | required | absolute paths |
| `state_dir` | `$XDG_STATE_HOME` or `~/.local/state`, plus `superclaude/issue-watch` | absolute |

The timeouts, `DAY_CAP`, 10 candidates and 60 min lease are code constants, not config keys (cycle.py:33-47).

**Approvers file** (`validate_approvers`, cycle.py:298-361): regular file (symlink refused), opened `O_NOFOLLOW` with an inode re-check, owner = euid, not group- or other-writable (read bits unchecked), at most 1 MiB, UTF-8, every non-blank line not starting with `#` must match `[1-9][0-9]{0,19}` (no whitespace, no CR), at least one id. Checked on every enabled or dry-run cycle.

**SLO.** `slo_numbers` (cycle.py:1359-1406) computes p95 approval-to-launch, exit-0 share over 7 days, claimed-within-lease share and stale count; it has no production caller (only `test_slo_helper.py` and an owner-run snippet at SET:457-476). DES:752 records "a library function ... not a verb". Status NOT BUILT as an operator surface, see Section 14.

**Audit log** (`P/audit.py`): `audit.jsonl` (0600, one sorted-key ASCII JSON line per `os.write`), three kinds (cycle, decision, warning), every key type- and shape-checked, rotation at 5 MiB keeping `.1`-`.4`, only with the lock held; one cycle line per exit that reaches `_conclude`, decision lines first. Config or platform failure, `cycle_crashed`, `state_dir_unwritable` and reset usage errors write only a stderr JSON line (cli.py:79, 127, 219; cycle.py:1195-1196). Nothing in `src/` reads the file back.

---

#### 5.1.5 Gates and approvals

Approval is one human label event judged by `approval_of` (predicates.py:185-234): the approval label must be present and last applied by an `actor_type == "User"` (not `[bot]`) whose numeric id is in the approvers file; it must be strictly after the last trigger-label event and the store `created_at`; a later unlabel voids it; a same-second label collision is `events_incomplete`. There is no second approval step in the cycle.

| Gate | Condition | Word / exit | Evidence | Pinned by |
|---|---|---|---|---|
| Enable switch | `not enabled and not dry_run` | `not_enabled` / 0 | cycle.py:685-686 | test_cycle.py (`...enabled_false...fr027`) |
| Kill switch | `DISABLED` exists, at start and before the pending write | `disabled`, `disabled_mid_cycle` / 0 | cycle.py:712, 1063; record.py:421 | test_cycle.py, test_record.py |
| Single instance | flock busy or lock inode replaced | `lock_held` / 75 | record.py:403-414 | test_concurrency.py |
| Trigger label | discovery filters on `labels.trigger` and own login; `>= 100` results | `truncated` / 4 | github.py:180-198, 823-824 | test_github.py |
| Approver label + allow-list | rules of `approval_of` | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete` / 0 | predicates.py:185-234 | test_predicates.py |
| Owner | assignee set equals {own login}; optional `owner_account_id` | `unassigned`, `assigned_other` / 0; `account_id_mismatch` / 2 | predicates.py:162-174; cycle.py:768 | test_predicates.py, test_cycle.py |
| Unchanged since approval | any edit, comment (not own) or rename time >= approval | `edited_after_approval` / 0 | predicates.py:237-259 | test_predicates.py |
| Project | one live item in `project_id`, status `Backlog` | `project_mismatch` / 0 | predicates.py:262-271 | test_predicates.py |
| Day cap | 6 launches in a rolling 24 h (checked twice) | `day_cap` / 0 | cycle.py:36, 867-876, 1061 | test_cycle.py, test_record.py |
| Call budget | 32 ordinary + 3 reserved; 240 s deadline; 120 s launch cut-off | `budget_exhausted` / 0 | github.py:46-49, 448-454; cycle.py:41-43 | test_github.py, test_cycle.py |
| Rate limit | `next_permitted_at` in the future | `rate_limited`, `rate_limit_clamped` / 5 | cycle.py:748-750, 663-668 | test_cycle.py, test_github.py |
| Origin and Orca | origin not `ironbellyorg/ironclaude`; no `orca-cli` binary | `origin_mismatch`, `orca_not_found` / 2 | launch.py:163-251 | test_launch.py, test_origin_parity.py |
| At-most-once | entry `pending`, `claimed`, or launched/unknown/abandoned without a marker; `pending` saved before launch | `already_dispatched` / 0 | cycle.py:919-933; record.py:538 | test_cycle.py, test_crash_injection.py |
| One launch per cycle | `launching` then `halt` | no word | cycle.py:833-834 | test_cycle.py (`...s1_case_b...`) |
| Re-validation | state, labels, owner, approval id, project re-read | `revalidation_failed` / 0; `revalidation_transient` / 7 | cycle.py:979-1016 | test_cycle.py, test_github.py |
| Launch argv | 12 literal elements, prompt pattern | `prompt_invalid` / 7 | launch.py:84-116 | test_launch.py, test_security_invariants.py |
| Operator reset | only `abandoned` or `unknown`, with `--forfeit-guarantee` | `reset_refused` / 2 | cli.py:232-252, 309-313 | test_cli.py |

Prose-only gates (no code check): the live-test record, shadow run, grants, acceptances and a running coordinator (SET:226-290, 584-635); "grant row" appears only as prose (SET:274, `docs/designs/issue-pipeline-fu1.md:24, 26`), not found as code in snapshot.

---

#### 5.1.6 Closed reason vocabulary (`audit.REASON_TABLE`, audit.py:26-102, 59 words)

Pinned literally, in order, with every (kind, exit) pair by `test_audit.py` (`test_reasons_pin_59_names...`). Full per-word raise sites are in Section 9 / Appendix.

| Group (count) | Words |
|---|---|
| Cycle, exit 0 (4) | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled` |
| Cycle, exit 2 (7) | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
| Cycle, exit 3 (5) / 4 (2) / 5 (2) | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed`; `truncated`, `discovery_duplicate`; `rate_limited`, `rate_limit_clamped` |
| Cycle, exit 6 (5) / 75 (1) / 1 (1) | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable`; `lock_held`; `cycle_crashed` |
| Skip, exit 0 (17) | `not_approved`, `approval_before_trigger`, `approval_before_init`, `events_incomplete`, `events_unreadable`, `edited_after_approval`, `project_mismatch`, `project_unreadable`, `unassigned`, `assigned_other`, `already_dispatched`, `in_backoff`, `day_cap`, `budget_exhausted`, `revalidation_failed`, `marker_unreadable`, `edits_unreadable` |
| Entry (9) | `launched`, `claimed`, `pending_orphan`, `claim_not_observed`, `attempts_exhausted` (exit 0); `prompt_invalid`, `revalidation_transient`, `spawn_error`, `launch_unknown` (exit 7) |
| Note (1), warning (4), operator (1) | `re-approved`; `discovery_count`, `clock_skew`, `dry_run_shadow_reset`, `reset_refused` (exit 2); `operator_reset` |

Five words never come out of `run_cycle`: `config_invalid`, `platform_unsupported`, `cycle_crashed`, `reset_refused`, `operator_reset` (CLI-owned). Adding a skip word: add it to `REASON_TABLE`, raise `_Skip`, update the literal pin in `test_audit.py`; `audit.line` raises `ValueError` for an unknown word.

---

#### 5.1.7 Dead, unwired and not-built items (see Section 14)

| Item | Status | Evidence |
|---|---|---|
| `MAX_LAUNCHES_PER_CYCLE = 1` (cycle.py:35): 14 constants at cycle.py:34-47, 13 read, this one defined and never read (no hit in `src/` or `tests/`). The one-launch limit is enforced by `_Cand.launching` (1028) and `self.halt` (833-834, loop break 816-817), which also halts after any launch-step skip, not only after a launch. DES:380, 819 name the constant as a default | NOT BUILT (dead constant) | [CODE-VERIFIED]; Section 14 |
| Scheduler that runs `once` (FU-2) | NOT BUILT | not found in snapshot; DES:30, SET:288 |
| Live-test record and captured fixtures (FU-1) | NOT BUILT | absent file; 19 `_assumed_shape` fixtures |
| `slo_numbers` as a verb or alert; alerting FU-4, auto `--retry-launch` FU-8 (`retry_argv` launch.py:119-132 only prints), role check FU-9, pruning FU-11, ETag FU-5, FS allow-list FU-12 | NOT BUILT | deferred by DES:856-871, SET:669-686 |
| `status` reads `audit.jsonl` (DES:406) | NOT BUILT | cycle.py:1279-1281 "not read" |
| `LaunchOutcome.detail` (8 words), `launch_login`, `launch_account_id`, `record.disabled_present` | dead or write-only | no reader in `src` (launch.py:58-70; record.py:548-568, 748-750) |
| `prompt_invalid` for discovered issues | practically unreachable | github.py:827-828 rejects bad numbers first; only test_cycle.py:3348 |
| Dispatcher, `COORD-`, zero-setup install, coordinator that starts the worker after the claim | not found in snapshot | research 03 F.2, F.3; the "Issue pipeline duties" contract text is REMOVED (CHANGELOG.md:17) |

---

#### 5.1.8 Contradictions found and open questions

| # | Doc claim | Code | Tag |
|---|---|---|---|
| 1 | Skew: DES:827 "skew tolerance 300 s" and the 60 s warning (DES:510, SET:384) | two constants: `SKEW_TOLERANCE_S` = 300 is the claim-marker window (predicates.py:17, 295); `SKEW_WARN_S` = 60 is the clock-skew warning threshold (cycle.py:44, 774). The row label is ambiguous, the number is right | [CODE-VERIFIED] (not a code contradiction; earlier contradiction tag withdrawn by erratum) |
| 2 | `find_orca` "cached per cycle" (DES:331, 362, 621) | caches nothing (launch.py:6, 177) | [CODE-CONTRADICTED] |
| 3 | Step 10 "Calls 0" (DES:360) | entry-state candidates read G4 (and G3) first (cycle.py:922-935) | [CODE-CONTRADICTED] |
| 4 | Exit 7 combines with 5 or 3 (DES:173) | unreachable through `_Cycle` (S1 halt); only 7 with 6 | [CODE-CONTRADICTED] |
| 5 | `audit.jsonl` written by every exit, read by `status` and the SLO reducer (DES:406) | stderr-only exits exist; no reader in `src` | [CODE-CONTRADICTED] |
| 6 | Prompt `/sc:issue --claim <N>` (DES:15; SET:616-619) | `... --pipeline none` (launch.py:92) | [CODE-CONTRADICTED] |
| 7 | `clock_skew_s` always on the cycle line (DES:722) | optional (audit.py:165) | [CODE-CONTRADICTED] |
| 8 | `agent-work-report` reads `orchestrator_repo` from the same config file (`src/superclaude/skills/agent-work-report/scripts/common.py:22-40`) | `load_config` rejects keys outside the 8 allowed (cycle.py:58-69, 216-220): such a config makes `once` exit 2 `config_invalid` | [CODE-CONTRADICTED] (cross-consumer) |
| 9 | SET:170, DES:43 name `WORKER-CONTRACT.md` "Issue pipeline duties" and `stage-status` | no such section or verb (CHANGELOG.md:17) | [CODE-CONTRADICTED] |

Open questions: PRs #447/#448 and "never run live" (DES:3) [UNVERIFIED]; real `gh` and Orca reply shapes [UNVERIFIED]; what runs `once` and the real `enabled` value [UNVERIFIED]; whether the per-cycle G4 cost for stuck `unknown` and `claim_not_observed` entries is acceptable; the unseen edit window between the G5 read and the launch (edits are not re-read, cycle.py:1006); `status` prints `disabled since: no` for a dangling `DISABLED` symlink while the cycle treats it as present (record.py:421-431); `reset --rate-limit --forfeit-guarantee` silently ignores the second flag (cli.py:309-313).

---

#### 5.1.9 Extension points

| File | Function | What to change | Pinned by |
|---|---|---|---|
| `P/github.py` | `argv_*` builders, `_call`, `classify` | new read: validate every caller value, `--method GET`, reuse a word already in `REASON_TABLE` | `test_github.py` (argv written out literally), `test_security_invariants.py` |
| `P/audit.py` | `REASON_TABLE`, `_KEYS`, `_TYPES`, `_RULES` | new reason word or audit key | `test_audit.py`, `test_predicates.py` (every predicate reason is in the table) |
| `P/predicates.py` + `P/cycle.py` | `_examine` | new gate: pure predicate, call it in the gate order of 5.1.1.1 | `test_predicates.py`, `test_cycle.py` |
| `P/record.py` | `ENTRY_STATES`, `MIGRATIONS` (ships empty), transition functions | new state or entry field needs a migration step and a pair-table update | `test_record.py` |
| `P/launch.py` | `launch_argv`, `PROMPT_PATTERN`, `build_claim_prompt` | change together; update the literal 12-element test | `test_launch.py`, `test_security_invariants.py` |
| `P/runner.py` | `Runner.run` | no other module may import `subprocess` | `test_no_shell.py`, `test_module_boundaries.py` |


