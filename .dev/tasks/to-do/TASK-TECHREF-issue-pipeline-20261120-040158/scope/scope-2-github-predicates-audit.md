# Scope 2: issue watcher GitHub, predicate and audit layer
**Scope:** src/superclaude/cli/issue_watch/{github.py,predicates.py,audit.py}, docs/designs/issue-watcher-setup.md (source root /home/coder/.cache/ic-snap-20261120/master)
**Status:** Complete
**Date:** 2026-11-20
---
Paths below are relative to `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6). Package dir `P` = `src/superclaude/cli/issue_watch/`.

## 1. File inventory

| Path | Lines | Purpose |
|---|---|---|
| `P/github.py` | 960 | Builds, runs (via `Runner`) and parses every `gh` call. READ-ONLY: no write argv exists in it. |
| `P/predicates.py` | 312 | Pure, no-I/O, no-clock eligibility logic and the frozen dataclasses the reads return. |
| `P/audit.py` | 404 | Closed reason table, `audit.jsonl` append-only writer with rotation, line builders, stderr fallback. |
| `docs/designs/issue-watcher-setup.md` | 706 | Owner runbook (16 sections): preflight, config, approvers, labels, init-state, shadow run, kill switch, exit/reason codes, recovery, rollout checklist. |
| `P/runner.py` (context, 130) | 130 | `Runner` protocol + `SubprocessRunner` (`shell=False`, stdin DEVNULL, stderr capped 500 B). Only module importing `subprocess`. |

### github.py key symbols (line numbers verified)
- Constants: `REPO` 37 (`IronbellyOrg/IronClaude`, literal in every argv); `PAGE_SIZE` 40 (100); `PAGE_CAP` 43 (5); `CALL_CAP` 46 (35); `RESERVED_CALLS` 49 (3); `EVENTS_JQ` 54; `MARKER_JQ` 61 (built from `predicates.CLAIM_MARKER` via `json.dumps`); `REREAD_JQ` 67; `EDITS_QUERY` 74; `PROJECT_ITEMS_QUERY` 88; `TRIGGER_MAX_CHARS` 129 (50); `GH_ERROR_SIGNS` 269; `RATE_LIMIT_MAX_WAIT_S` 376 (3600); `DISCOVERY_BOUND` 486 (100).
- Arg guards: `_issue_arg` 111, `_page_arg` 118, `_CURSOR_RE` 127, `_trigger_arg` 150 (rejects empty, >50, leading `-`, comma, control chars), `_login_arg` 168, `_LOGIN_RE` 134.
- Argv builders: `argv_user` 175 (G1), `argv_discover` 180 (G2), `argv_events` 218 (G3), `argv_comments` 223 (G4), `argv_edits` 242 (G5), `argv_project_items` 247 (G6), `argv_reread` 252 (G7); helpers `_argv_rest_page` 201, `_argv_graphql` 228.
- Classification: `Reply` 282, `classify` 345 (kinds: timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed), `_split_include` 290, `retry_after` 396, `date_header` 401, `rate_limit_wait` 418 (Retry-After 1..3600 > x-ratelimit-reset <=3600 > now+3600 `rate_limit_clamped`).
- Budget: `CallBudget` 437 (`spend` 448 keeps last 3 for reserved; `spend_shared` 456 never refused; `total` 461 feeds audit `gh_calls`); `Read` 467; `_SHARED_REASONS` 489; `_call` 557; `_rest_read` 592; `_graphql_read` 645.
- Item parsers: `_event` 708, `_marker` 725 (null login dropped), `_edited_at` 739 (missing key = malformed, explicit null = never edited), `_comment_edit` 753, `_project_item` 764.
- Typed public reads: `user` 784, `discover` 804, `events` 845, `marker_comments` 866, `edits` 886, `project_items` 907, `reread` 934. Each returns `Read(value, reason, kind, retry_after_s)`; none raises on malformed replies.

### predicates.py key symbols
- Constants: `CLAIM_MARKER` 14 (`<!-- sc:issue:claim -->`); `SKEW_TOLERANCE_S` 17 (300); `MAX_ISSUE_NUMBER` 20; `OPERATION_ID_PATTERN` 57.
- Helpers: `parse_utc` 27 (strict `YYYY-MM-DDTHH:MM:SSZ`), `format_utc` 42, `valid_issue_number` 52 (int not bool, 1..999999999), `valid_operation_id` 65.
- Dataclasses (frozen): `Login` 71, `DiscoveredIssue` 80, `LabelEvent` 90, `IssueSnapshot` 103, `ProjectItem` 113, `MarkerEvidence` 122, `CommentEdit` 133, `EditEvidence` 143, `ApprovalResult` 152.
- Predicates: `is_intended_owner` 162, `approval_of` 185, `unchanged_since` 237, `project_check` 262, `marker_time` 274, `marker_in_window` 279, `eligibility_order` 299.

### audit.py key symbols
- `REASON_TABLE` 26 (59 names, name -> (kind, exit)); `REASONS` 104; `ROTATE_BYTES` 106 (5 MiB); `_ROTATIONS` 107 (4); `AuditLog` 123 (`append` 130, `rotate_if_needed` 141); `_KEYS` 162; `_TYPES` 178; `_RULES` 229; `_check_value` 246; `line` 261; `cycle_line` 292; `decision_line` 322; `warning_line` 354; `stderr_fallback` 381.

## 2. Behaviour map

### 2.1 Every `gh` call (all in `github.py`; all READ; `--repo` handling)
No `gh` write exists in the package: grep for `"gh"` outside github.py finds nothing in `P/`. Repo is never a parameter: `gh issue list` carries `--repo IronbellyOrg/IronClaude` (github.py:186-187); `gh api` REST paths embed `repos/IronbellyOrg/IronClaude/...` (208, 259); GraphQL queries hard-code `owner: "IronbellyOrg", name: "IronClaude"` (75, 89); G1 `gh api user` is not repo-scoped. Runner has no shell (runner.py:91 `shell=False`).

| Id | Builder (line) | Exact argv shape | Reads | Caller (cycle.py) |
|---|---|---|---|---|
| G1 | `argv_user` 175 | `gh api user --include` | own login, numeric id, `Date`/`Retry-After`/`x-ratelimit-reset` headers | `_login_step` 755 |
| G2 | `argv_discover` 180 | `gh issue list --repo R --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | open issues with trigger label assigned to own login | `_discover` 796 |
| G3 | `argv_events` 218 | `gh api --method GET repos/R/issues/N/events -F per_page=100 -F page=P --jq <EVENTS_JQ>` | label/unlabel/renamed events: id, event, label, actor id/login/type, created_at | `_examine` 944, `_reclaim` 907; reserved variant (G3') in `_revalidate` 996 |
| G4 | `argv_comments` 223 | `gh api --method GET repos/R/issues/N/comments -F per_page=100 -F page=P --jq <MARKER_JQ>` | per comment: id, login, created/updated, boolean `contains(CLAIM_MARKER)`; body text never reaches Python | `_examine` 926/942, `_reclaim` 905 |
| G5 | `argv_edits` 242 | `gh api graphql -f query=<EDITS_QUERY> -F number=N [-f after=<cursor>]` | issue `createdAt`/`lastEditedAt`; comment databaseId/author/createdAt/lastEditedAt | `_examine` 948 |
| G6 | `argv_project_items` 247 | `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=N [-f after=<cursor>]` | per Project item: isArchived, project id, Status single-select name | `_examine` 957; G6' (reserved) `_revalidate` 1013 |
| G7 | `argv_reread` 252 | `gh api --method GET repos/R/issues/N --jq <REREAD_JQ>` | number, state, label names, assignee logins (FR-011 re-read) | `_revalidate` 983 (always `reserved=True`) |

- REST calls carry `--method GET` (gh would POST once `-F` is added); GraphQL calls carry no `--method` (POST by design, github.py:107-108).
- Paging: `PAGE_CAP`=5 pages, 100 per page. REST read: repeated id, or full 5 pages, gives `incomplete` (`_rest_read` 592-628). GraphQL read: repeated cursor, missing cursor, bad cursor alphabet or page cap gives failure (`_graphql_read` 645-702). G2 is a single call (`-L 100`); 100 or more results fail closed as `truncated` (`discover` 823-824).
- No argv requests title, body or comment text. Only `contains(<marker>)` inside gh's jq (MARKER_JQ 61-65).
- Budget: 35 per-issue calls (`CALL_CAP`), last 3 reserved for `_revalidate`; G1/G2 counted separately (`spend_shared`), so a busy cycle is at most 35+2 = 37 `gh` calls. `_call` 557 refuses a call when `timeout_for()` is None (cycle deadline) or the budget is spent.
- Failure mapping (`classify` 345, `_SHARED_REASONS` 489): G1/G2 failures map to cycle reasons gh_timeout / gh_non_json / rate_limited / project_read_failed, any other to `gh_auth_failed`; per-issue reads map to `events_unreadable`, `marker_unreadable`, `edits_unreadable`, `project_unreadable`, `events_incomplete`; G7 maps to `revalidation_transient` (timeout/5xx) or `revalidation_failed`. `scope_missing` on a per-issue read stops the cycle as `project_read_failed` (cycle.py:842-843).
- GH_ERROR_SIGNS (269-277) are marked `[UNVERIFIED]` in source: stderr strings and GraphQL error type names are assumed, pending the live test (FU-1). GraphQL queries are marked `[PROPOSAL, UNVERIFIED]` (github.py:71-72).

### 2.2 What is read vs written on GitHub (labels, comments, assignees, fields, markers)
- This slice WRITES nothing to GitHub. It reads: issue state, label names, assignee logins (G2, G7), label events with actor identity (G3), comment authorship/times and marker presence (G4), edit timestamps (G5), Project v2 membership/Status (G6), own account (G1).
- The marker `<!-- sc:issue:claim -->` is written by the launched session, not the watcher. The only write path is `launch.py` building `orca agent launch --agent claude --worktree path:<worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json` (launch.py:84-92, 103-116; prompt pinned by `PROMPT_PATTERN` 33). The session (`/sc:issue --claim`) then assigns, comments and posts the marker (out of this slice).
- `test_marker_contract.py` pins that skill copies end with the same literal as `predicates.CLAIM_MARKER`.
- Labels: the watcher only reads the trigger and approval labels (`labels.trigger` default `issue-watch:trigger`, `labels.approval` default `issue-watch:approved`; defaults in cycle.py config, not in this slice). It never creates, adds or removes labels.

### 2.3 Eligibility predicates (all pure; inputs are values, times are parameters)
Order of use in `cycle._examine` (cycle.py:915-961): entry-state shortcuts, `day_cap`, `is_intended_owner`, G4, G3, `approval_of`, marker hit, G5, `unchanged_since`, G6, `project_check`, then `_launch`.
- `is_intended_owner(assignees, own_login) -> (bool, reason|None)` predicates.py:162-174. True only if the set is exactly `{own_login}`; else `unassigned` / `assigned_other`.
- `approval_of(events, *, labels_now, trigger_label, approval_label, approvers, store_created_at) -> ApprovalResult` 185-234. Sorts by (created_at, id). Checks in order: same-second collision of approval-on with approval-off or trigger-on gives `events_incomplete` (205-209); label absent now or never applied gives `not_approved` (210); an `unlabeled` event later than the last approval gives `not_approved` (214); latest approval actor must be `actor_type == "User"`, login present and not ending `[bot]`, integer id in `approvers` (216-223) else `not_approved`; no trigger `labeled` event gives `events_incomplete` (226); approval not strictly after the last trigger event gives `approval_before_trigger` (228); approval not strictly after `store_created_at` gives `approval_before_init` (230). Success returns approver id, event id, approved_at.
- `unchanged_since(approved_at, edits, events, *, own_login) -> "edited_after_approval"|None` 237-259. Any of: issue createdAt, issue lastEditedAt, createdAt/lastEditedAt of every comment NOT authored by own login, any `renamed` event time, that is `>= approved_at` (equal counts as changed).
- `project_check(items, project_id) -> "project_mismatch"|None` 262-271. Exactly one non-archived item in `project_id` and its Status equals `"Backlog"`.
- `marker_time` 274 = max(created, updated); `marker_in_window(marker, *, own_login, pending_at, approved_at) -> bool` 279-296: marker flag true, login == own login; with `pending_at` the time must be `>= pending_at - 300s`, else strictly `> approved_at`.
- `eligibility_order(discovered, considered) -> list[int]` 299-312: never-examined issue numbers ascending, then examined ordered by (last-considered time, number). Cap `MAX_CANDIDATES = 10` applied by caller (cycle.py:34, 736).
- Other gates outside this slice but in the same chain: `DAY_CAP = 6` (cycle.py:36), `record.BACKOFF` 10 min (record.py:437), `record.LEASE` 60 min (record.py:440), `SKEW_WARN_S = 60` (cycle.py:44), `DISCOVERY_WARN = 80` (cycle.py:47).
- Revalidation (cycle.py:979-1016) re-applies owner, labels, `approval_of` (same approval_event_id required) and `project_check` using the 3 reserved calls; edits are NOT re-read.

### 2.4 Audit log
- Location `<state_dir>/audit.jsonl` (audit.py:128); default state_dir `${XDG_STATE_HOME:-~/.local/state}/superclaude/issue-watch` (cycle.py:187-192). Open flags `O_WRONLY|O_APPEND|O_CREAT`, mode 0600, one `os.write` per line, short write raises (130-139).
- Format: JSON object per line, `sort_keys=True`, `ensure_ascii=True`, newline-terminated (118-120). Rotation at >=5 MiB to `.1`..`.4` (`rotate_if_needed` 141-156), called with lock held (cycle.py:1198; cli.py:276 for reset).
- Line kinds (`_KEYS` 162-175): `cycle` (+exit, gh_calls, duration_ms; optional discovery_count, clock_skew_s), `decision` (+issue, approver_id, approval_event_id, approved_at all required-nullable; optional state, note), `warning` (optional issue, discovery_count, clock_skew_s). Common: kind, ts, host, login, cycle_id (uuid4 hex), dry_run, reason.
- Closed shape per key (`_RULES` 229-243); reason must be in `REASON_TABLE` (59 names). `host`/`login` accept any printable token (login no whitespace), so arbitrary text is possible there (audit.py docstring 6-8). No title/body/label/stderr slot exists.
- Write sites: `cycle._conclude` writes decision lines then the one cycle line (cycle.py:1176-1202); `cli._write_reset` writes ONE decision/warning line per reset, never a cycle line (cli.py:255-279). On OSError, or reason `state_dir_unwritable`, falls to `stderr_fallback` (audit.py:381-404): one JSON line with only kind/ts/host/exit/reason. `once` writes stderr-only `cycle_crashed` (cli.py:127).
- Dry runs append lines with `dry_run: true`; `launched` in a dry run means would-launch and carries no `state`.

### 2.5 `enabled: false` gating
- `Config.enabled` parsed at cycle.py:228 (default False; must be JSON bool). Gate at cycle.py:685-686: `if not enabled and not dry_run: raise _Stop("not_enabled")` -> exit 0. `--dry-run` ignores it. No code in this slice reads `enabled`. Other gates: `DISABLED` file in state_dir (record.py:283, 422), checked after the lock before GitHub, and again before launch (doc 9; code in cycle.py outside this slice).
- Read-only in dry run: probe skipped, no Orca call, no store write (cycle.py:1029-1035).

## 3. Doc-vs-code checks (docs/designs/issue-watcher-setup.md, section numbers are the doc's)

| Claim | Verdict | Evidence |
|---|---|---|
| s4: "watcher never creates labels and never writes to GitHub at all" | [CODE-VERIFIED] | Every argv in github.py is a read (REST `--method GET`, GraphQL query, `issue list`, `api user`); no other `"gh"` literal in `P/` (grep). The launched session does write; the doc says the claim runs `--pipeline none` (s6). |
| s10.2: audit accepts "only the 59 names" | [CODE-VERIFIED] | `REASON_TABLE` audit.py:26-102 has 59 entries (count by regex); `test_audit.py` pins the same 59. |
| s10.3: sorted keys, rotated at 5 MiB into `.1`..`.4`, cycle line last | [CODE-VERIFIED] | audit.py:119, 106-107, 141-156; cycle.py:1193-1200 (decision lines then cycle line). |
| s10.3: "No issue title, body, label name or error text is ever written" | [CODE-VERIFIED, narrower] | No typed slot exists, but `host`/`login` take any printable token (audit.py:234-235 and docstring lines 6-8). Doc wording "never" is stronger than code guarantee. |
| s2: `enabled:false` makes `once` exit 0 `not_enabled`; `--dry-run` ignores it | [CODE-VERIFIED] | cycle.py:685-686. Ordering "before any external call" relative to G1 not read in full (UNVERIFIED), but the origin check (721) and `github.user` (755) come at later lines. |
| s2: trigger/approval label rules (1-50 chars, no comma, no double quote, no leading dash) | [CODE-VERIFIED] | cycle.py:135 (`,`, `"`, leading `-`); github.py `_trigger_arg` 150-165 (length 50, control chars). `_trigger_arg` does not itself reject `"`; config is the stricter gate. |
| s1.3/s10: origin = `IronbellyOrg/IronClaude`, checked at start and before launch, `git -C <wt> remote get-url origin` | [CODE-VERIFIED] | launch.py:233-251 (case-insensitive compare to `ironbellyorg/ironclaude`, `ORIGIN_REPO` 50); cycle.py:721 and 1074 call it. |
| s1.2: Orca binary accepted only if `skills list --json` lists topic `orca-cli`; `orca-ide` then `orca` | [CODE-VERIFIED] | launch.py:144-160, 193-201 (`_ORCA_CLIS` order not read; names `orca-ide`/`orca` per doc). |
| s14.2: launch argv is 12 elements, no permission flag | [CODE-VERIFIED] | launch.py:103-116 (12 elements, no permission flag). |
| s14.1.1 capture sheet: prompt `/sc:issue --claim <test issue>` | [CODE-CONTRADICTED] | Code prompt is `/sc:issue --claim N --pipeline none` (launch.py:33, 92). Doc s6/s13 do say `--pipeline none`, so the capture sheet rows (lines 616-619) are stale/internally inconsistent. |
| s6: coordinator rules in `src/superclaude/core/WORKER-CONTRACT.md` section 4 "Issue pipeline duties" | [CODE-CONTRADICTED] | WORKER-CONTRACT.md has section 4 "Coordinator rules" (line 68) but no text matching "issue pipeline", "issue-pipeline" or "issue-watch" (grep, case-insensitive heading and body). |
| s6/s8.5: `docs/designs/issue-pipeline-fu1.md`, `issue-pipeline-guard-g2.md` exist | [CODE-VERIFIED] | Present in `docs/designs/` (also `issue-watcher.md`, `issue-pipeline-guard-g2-no-to.md`). `issue-watcher-live-test.md` is absent, as the doc says the owner writes it. |
| s8.7: cron `0 */5 * * * *` (six fields, seconds first) installed by owner; nothing installs it | [CODE-VERIFIED] (absence) | No "cron" string in `P/`; grep of `src`/`pyproject.toml` for `issue-watch`/`issue_watch` hits only issue_watch/*, `cli/main.py` and `agent-work-report/scripts/common.py`; no installer. Standard 5-field cron has no seconds field; scheduler interpretation is left to the owner (doc s7: "scheduler is your choice"). |
| s7/8: dispatcher, worktree creation, COORD-<RepoName> coordinator | [UNVERIFIED] | The doc has no dispatcher and no Coordinator worktree install step; the user memory notes "zero-setup watcher decisions" (Coder issues 515/516) are not in this doc or this slice. |
| s8.1: day cap 6/24h, 10 candidates, 60-min lease, 10-min backoff, skew warn 60 s, discovery warn 80 | [CODE-VERIFIED] | cycle.py:34, 36, 44, 47; record.py:437, 440. 240-second cycle budget NOT checked (UNVERIFIED). |
| s10.1 "at most 37 gh calls in a busy cycle" | [CODE-VERIFIED] | `CALL_CAP` 35 + G1 + G2 shared (github.py:46, 456). |
| s3-s6 approval rules (User-type, not `[bot]`, id in approvers file, strictly after trigger, strictly after store creation, same-second = `events_incomplete`) | [CODE-VERIFIED] | predicates.py:205-230. |
| s6: "edit to the issue body or title, or a comment by anyone other than the watcher" voids approval | [CODE-VERIFIED, nuance] | Title edits are seen only through `renamed` events (predicates.py:256); body via `lastEditedAt`; any issue `createdAt >= approved_at` also voids (249-257). |
| s10.4/s10.5, status/SLO, reset, init-state | [UNVERIFIED] | Implemented in cli.py/cycle.py/record.py, outside this slice. `cycle.slo_numbers` exists (cycle.py near 1228 `_SLO_EXCLUDED_REASONS`). |
| s5: `init-state` creates dir 0700, `dispatch.json` 0600, `lock` 0600 | [UNVERIFIED] | record.py/cli.py, not read. |
| s2: five CLI commands once/status/check-config/init-state/reset | [UNVERIFIED] | cli.py has `reset` (282) and a group; others not enumerated. |

## 4. Tests that pin this slice (tests/issue_watch/)

| File | Lines | Test fns/classes | One-line |
|---|---|---|---|
| `test_github.py` | 2161 | 141 | Part A: argv builders G1-G7 written out literally, jq/GraphQL constants, `classify`, rate-limit time, `_assumed_shape` fixtures; no real command runs. |
| `test_predicates.py` | 732 | 44 | `approval_of` (threat rows T2, T3) and `unchanged_since` (T4) with hand-built frozen dataclasses, no fakes (plus later-part predicate tests, not read). |
| `test_audit.py` | 849 | 46 | Pins the 59-name reason table literally (never imported from the module), line builders, writer, rotation. |
| `test_origin_parity.py` | 179 | 7 | `launch.parse_origin` equals skill script `parse_origin_url` over one table; only `check_origin` lower-cases. |
| `test_find_orca_parity.py` | 288 | 10 | `launch.find_orca` matches `install_user_setup._find_orca`; where the original raises, new code must reject without raising (DF-36, C19). |
| `test_marker_contract.py` | 53 | 3 | `CLAIM_MARKER` in every skill copy; template last line is the marker; `MARKER_JQ` built from it (DF-21, DF-46). |
| `test_slo_helper.py` | 421 | 14 | `cycle.slo_numbers` four SLO numbers from synthetic `audit.jsonl` files with hand-computed expectations. |
| `fixtures/_assumed_shape/` | 19 files | n/a | Assumed replies named in the doc's s14.1.1 capture sheet: `gh_issue_list`, `gh_issue_reread`, `gh_api_user_include(_429)`, `rest_events_page`, `rest_comments_marker`, `graphql_edits`, `graphql_project_items`, `gh_graphql_{rate_limited,insufficient_scopes}`, 5x `gh_stderr_*`, 4x `orca_launch_*`. FU-1 replaces them with captured replies. |
Adjacent (not assigned): `test_no_shell.py`, `test_no_text.py`, `test_security_invariants.py`, `test_module_boundaries.py` likely pin the no-body/no-shell/import rules claimed in the module docstrings (not read).

## 5. Proposed deep-research assignments

1. **GitHub read-side contract and call budget**: files `P/github.py`, `P/predicates.py` (dataclasses), `P/runner.py`, `cycle.py` lines 540-560 and 740-1020 (callers), `tests/issue_watch/test_github.py`, `fixtures/_assumed_shape/`, `docs/designs/issue-watcher.md` section 8. Questions: per-call field-by-field reply shape and failure mapping, budget arithmetic (35+3 reserved, shared 2), what is assumed vs live-verified (FU-1 status), which parts of GH_ERROR_SIGNS are confirmed. Output: `research/issue-watch-github-reads.md`.
2. **Eligibility chain, audit log and operator runbook reconciliation**: files `P/predicates.py`, `P/audit.py`, `cycle.py` (`_examine`, `_revalidate`, `_conclude`), `record.py` (day cap, backoff, lease, DISABLED), `cli.py` (check-config, init-state, status, reset), `docs/designs/issue-watcher-setup.md`, `tests/issue_watch/test_predicates.py`, `test_audit.py`. Questions: full decision tree with reason codes and exit precedence, audit line examples per kind, each runbook step vs implemented behaviour (cron/dispatcher/worktree gaps below). Output: `research/issue-watch-eligibility-audit-runbook.md`.

## 6. Gaps and open questions
- [CODE-CONTRADICTED] setup doc s6 cites a WORKER-CONTRACT.md section "Issue pipeline duties" that does not exist; the issue-pipeline coordinator rules are not in that file at this commit.
- [CODE-CONTRADICTED] setup doc s14.1.1 launch commands omit `--pipeline none`.
- [UNVERIFIED] no dispatcher, Coordinator worktree or zero-setup install step appears in the setup doc or in any code read; whether another doc (issue-watcher.md, issue-pipeline-fu1.md) or the Coder template covers it is open. Doc says scheduler is the owner's choice.
- [UNVERIFIED] whether the `enabled` gate precedes every external call; `DISABLED` check sites in cycle.py were not read (only record.py:283, 422-423, 749-750 located).
- The GraphQL queries, `GH_ERROR_SIGNS` and `_CURSOR_RE` are labelled unverified in source (github.py:71-72, 125, 267); live-test record `docs/designs/issue-watcher-live-test.md` does not exist in this snapshot, so all captured shapes are still `_assumed_shape`.
- `rate_limit_wait` header parsing works only for G1 (`--include` in argv, github.py:380-385); a rate limit on G2-G7 yields no headers, so `_rate_stop` (cycle.py, not read) must use the clamped path. Not verified.
- Cycle time budget (240 s) and `_ORCA_CLIS` list not verified.
- Cron expression with six fields is not standard cron; no code validates it.
