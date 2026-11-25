# Research: Watcher I/O (GitHub calls, launch, dispatch record)
**Investigation type:** Code Tracer + Integration Mapper
**Scope:** issue_watch/github.py, launch.py, record.py, runner.py, eight test files plus fixtures
**Status:** Complete
**Date:** 2026-11-20
---
Source root for every path below: `/home/coder/.cache/ic-snap-20261120/master` (read-only, origin/master 61ac2c2e6). `P` = `src/superclaude/cli/issue_watch/`. All line numbers were re-read from the live snapshot files in this run. Scope-discovery files were used only as hints.

## 1. github.py (960 lines): every `gh` call

Module docstring (github.py:1-10): every argv is built from module constants plus five caller values (issue number, page, cursor, trigger label, login), each checked before it enters an argv (`ValueError` otherwise); the repository is the literal `REPO`; no argv asks for a title, body or comment text; the module reads no clock.

### 1.1 Constants
| Constant | Line | Value | Meaning |
|---|---|---|---|
| `REPO` | 37 | `"IronbellyOrg/IronClaude"` | the one repository every argv names |
| `PAGE_SIZE` | 40 | 100 | REST `per_page` |
| `PAGE_CAP` | 43 | 5 | most pages one paged read may fetch |
| `CALL_CAP` | 46 | 35 | most `gh` calls per cycle (NFR-009) |
| `RESERVED_CALLS` | 49 | 3 | calls of `CALL_CAP` kept for the FR-011 re-read |
| `TRIGGER_MAX_CHARS` | 129 | 50 | longest trigger label |
| `RATE_LIMIT_MAX_WAIT_S` | 376 | 3600 | longest header-derived wait; also the clamp |
| `DISCOVERY_BOUND` | 486 | 100 | discovery results at or above this fail closed |
| `EVENTS_JQ` | 54-57 | `[.[] | {id, event, label: .label.name, actor_id: .actor.id, actor_login: .actor.login, actor_type: .actor.type, created_at}]` | G3 projection |
| `MARKER_JQ` | 61-64 | `[.[] | {id, login: .user.login, created_at, updated_at, marker: (.body | contains("<CLAIM_MARKER>"))}]`; marker text inserted with `json.dumps(CLAIM_MARKER)` | G4 projection; body becomes a boolean |
| `REREAD_JQ` | 67 | `{number, state, labels: [.labels[].name], assignees: [.assignees[].login]}` | G7 projection |
| `EDITS_QUERY` | 74-85 | GraphQL `query(...)` on `repository(owner: "IronbellyOrg", name: "IronClaude")` | G5 |
| `PROJECT_ITEMS_QUERY` | 88-103 | GraphQL `query(...)` on the same repository | G6 |
| `GH_ERROR_SIGNS` | 269-277 | dict of 7 keys (auth_stderr, scope_types, scope_stderr, rate_status_stderr, rate_text_stderr, rate_types, transient_stderr_re) | stderr/GraphQL strings `classify` matches; marked `[UNVERIFIED]` at github.py:267 |

Both GraphQL strings are single `query` documents. Comment at github.py:71-72 labels them "[PROPOSAL, UNVERIFIED] drafts ... reply shapes are unverified (FU-1, FU-3)".

### 1.2 The seven calls G1-G7 (exact argv, read versus write)
`--repo` handling: only G2 has a `--repo` flag; its value is the `REPO` constant (github.py:186-187). REST calls embed `repos/IronbellyOrg/IronClaude/...` in the path through `{REPO}` (github.py:208, 259). The GraphQL calls name the repository inside the query text (github.py:75, 89). G1 (`gh api user`) is not repository-scoped. No caller supplies a repository value.

| Id | Builder (line) | Exact argv (items in `<>` are validated caller values) | R/W | Budget class | Typed read (line) | Failure reasons returned |
|---|---|---|---|---|---|---|
| G1 | `argv_user` 175-177 | `["gh","api","user","--include"]` | READ (default GET; no `-F`/`-f`/`--method`) | shared, counted by `_Cycle._tf_shared` (`spend_shared`) cycle.py:580-585; passes `budget=None` into `_call` | `user` 784 | `_SHARED_REASONS` map or `gh_auth_failed`; malformed body `gh_non_json` (github.py:800) |
| G2 | `argv_discover` 180-198 | `["gh","issue","list","--repo","IronbellyOrg/IronClaude","--state","open","--label",<trigger>,"--assignee",<login>,"--json","number,labels,assignees,state","-L","100"]` | READ | shared (same `_tf_shared`) | `discover` 804 | same map; `truncated` (>=100 results) 823-824; `discovery_duplicate` 829-830; `gh_non_json` 841 |
| G3 | `argv_events` 218-220 via `_argv_rest_page` 201-215 | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>/events","-F","per_page=100","-F","page=<P>","--jq",EVENTS_JQ]` | READ (`--method GET` explicit) | per-issue, non-reserved (cap 32) | `events` 845 | `events_unreadable`, `events_incomplete`, `budget_exhausted` |
| G3' | same builder, `reserved=True` | same argv | READ | per-issue, reserved (cap 35) | `events(..., reserved=True)`; caller cycle.py:995-997 | same |
| G4 | `argv_comments` 223-225 | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>/comments","-F","per_page=100","-F","page=<P>","--jq",MARKER_JQ]` | READ | per-issue, non-reserved (`False` at 882) | `marker_comments` 866 | `marker_unreadable` for every failure incl. incomplete (874-883) |
| G5 | `argv_edits` 242-244 via `_argv_graphql` 228-239 | `["gh","api","graphql","-f","query=<EDITS_QUERY>","-F","number=<N>"]` plus `["-f","after=<cursor>"]` from page 2 | READ (GraphQL `query`; gh sends POST by design, github.py:107-108) | per-issue, non-reserved (`False` 899) | `edits` 886 | `edits_unreadable` |
| G6 | `argv_project_items` 247-249 | `["gh","api","graphql","-f","query=<PROJECT_ITEMS_QUERY>","-F","number=<N>"]` plus optional `-f after=<cursor>` | READ (GraphQL `query`) | per-issue, non-reserved | `project_items` 907 | `project_unreadable` |
| G6' | same builder, `reserved=True` | same | READ | per-issue, reserved; caller cycle.py:1012-1014 | `project_items(..., reserved=True)` | same |
| G7 | `argv_reread` 252-262 | `["gh","api","--method","GET","repos/IronbellyOrg/IronClaude/issues/<N>","--jq",REREAD_JQ]` | READ | per-issue, ALWAYS reserved (`reserved=True` at github.py:942) | `reread` 934 | `revalidation_transient` (kind timeout or transient), `revalidation_failed` (any other, or a reply with another number 951) |

All argvs are plain `list[str]` that `Runner.run` executes with `shell=False` (runner.py:91-93). Callers in cycle.py: G1 `_login_step` 755; G2 `_discover` 796; G3/G4/G5/G6 `_examine` 941-957 and `_reclaim` 904-908; G7/G3'/G6' `_revalidate` 983, 996, 1013.

Read-only evidence (commands run in this research): Grep `"gh"` over `P/*.py` returns five list-literal lines, all in github.py (177 G1, 183 G2, 204 G3/G4, 231 G5/G6, 255 G7) and no other `gh` argv anywhere in `P`. Grep `mutation|POST|PATCH|DELETE|PUT` in github.py returns only the comment lines 107-108 (text "gh defaults to POST ... the GraphQL calls are POST"). No `gh issue comment/edit/create/close`, `gh label` or `gh pr` string exists in `P`. The only `"issue"` argv element is the `gh issue list` of G2 (github.py:184).

### 1.3 Argument guards (what can reach an argv)
- `_issue_arg` 111-115: `valid_issue_number` (predicates; int not bool, 1..999999999) else `ValueError("invalid issue number")`.
- `_page_arg` 118-122: `type(page) is int` and `1 <= page <= PAGE_CAP`.
- `_CURSOR_RE` 127: `[A-Za-z0-9+/=_.:-]{1,256}`, comment at 125-126 marks the alphabet `[UNVERIFIED]`; `_cursor_args` 141-147 emits `["-f","after=<cursor>"]` or nothing.
- `_trigger_arg` 150-165: non-empty, <=50 chars, no leading `-`, no comma, no control char (ord<32 or 127). It does not reject a double quote.
- `_login_arg` 168-172: `_LOGIN_RE` 134 `[A-Za-z0-9][A-Za-z0-9-]{0,38}`.

### 1.4 Reply classification (`classify`, github.py:345-371)
Order of rules: (1) `result.timed_out` -> `timeout`; (2) exit 0 -> `ok` when body parses as JSON else `non_json`; (3) otherwise by stderr and GraphQL `errors[].type`: `auth_failed` ("HTTP 401" or "gh auth login"), `scope_missing` (type `INSUFFICIENT_SCOPES` or stderr contains "read:project"), `rate_limited` (("HTTP 403" or "HTTP 429") and stderr lower-case contains "rate limit", or type `RATE_LIMITED`), `transient` (regex `HTTP 5[0-9]{2}`), else `failed`. There is no exit-code rule beyond exit 0 (docstring 348-351). `Reply.kind` closed set: timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed (8 words). `include_headers=True` only for G1, whose body follows an HTTP header block; `_split_include` 290-306 returns None for any other layout, then `_body` returns None and `classify` gives `non_json`.
An exit-0 GraphQL reply with an `errors` list is re-classified in `_graphql_read` by `_errors_kind` 631-638 (`scope_missing`, `rate_limited`, else `failed`).

### 1.5 Rate-limit handling and clamp
- `retry_after` 396-398 and `_g1_header` 380-385: headers are readable ONLY when `"--include" in result.argv`, i.e. only for G1. `date_header` 401-415 parses the `Date` header (unparseable gives None and the skew check is skipped).
- `rate_limit_wait(result, now)` 418-431 returns `(next_permitted_at, reason)`: `Retry-After` of 1..3600 s -> `now + seconds`, reason `rate_limited`; else `x-ratelimit-reset` epoch later than now by 1..3600 s -> that time, `rate_limited`; else `now + 3600 s`, reason `rate_limit_clamped`.
- Use in cycle.py: a G1 rate limit calls `github.rate_limit_wait(capture.last, now)`, then `record.set_next_permitted`, then stops with that reason (cycle.py:757-761). A rate limit on G2 or on any per-issue read (G3-G7) has no header (those argvs lack `--include`), so `_rate_stop` (cycle.py:663-668) sets `next_permitted_at = now + _RATE_CLAMP` and stops `rate_limit_clamped` (callers cycle.py:801, 841, 970). `_RATE_CLAMP = timedelta(seconds=github.RATE_LIMIT_MAX_WAIT_S)` cycle.py:488 (3600 s). Next cycle, `_load` stops `rate_limited` while `now < next_permitted_at` (cycle.py:748-750).
- Exit codes: `rate_limited` and `rate_limit_clamped` are `("cycle", 5)` (audit.py:51-52).

### 1.6 Call budget arithmetic
- `CallBudget` github.py:437-463. `spend(reserved=False)`: `cap = CALL_CAP if reserved else CALL_CAP - RESERVED_CALLS` (35 or 32); returns False and counts nothing when `calls >= cap` (448-454). `spend_shared()` 456-458 only increments `shared_calls`; it is never refused. `total` 460-463 = `calls + shared_calls`, written to the cycle audit line as `gh_calls` (cycle.py:1188).
- One `CallBudget` per `_Cycle` (cycle.py:549). Per-issue non-reserved reads (G3, G4, G5, G6) may use at most 32 calls; G7, G3', G6' may use the last 3 (35 total). G1 and G2 are shared, counted in `_tf_shared` only when a timeout was granted (cycle.py:580-585), so a cycle makes at most 35 + 2 = 37 `gh` calls. `_call` github.py:557-577 spends before running.
- `_call` returns None (no call) when `timeout_for()` is None (fewer than `GH_FLOOR_S` = 5.0 s left; cycle.py:42, `Deadline.timeout_for` 418-427) or when `budget.spend` refuses. Callers map this to `_NO_CALL` (`budget_exhausted`, github.py:588) or `_SHARED_NO_CALL` (`gh_timeout`/`timeout`, 589).
- Fewest calls for one candidate that reaches launch with one-page replies: 4 (G4, G3, G5, G6) + 3 (G7, G3', G6') = 7 (derived from cycle.py:941-957 and 979-1016). Pagination multiplies: each of G3/G4/G5/G6 up to 5 pages.
- A launch-step outcome halts the cycle after one candidate (`c.launching = True` cycle.py:1028; `self.halt = True` cycle.py:833-834), so the reserved calls are normally spent for at most one candidate per cycle.
- Per-call timeout `GH_TIMEOUT_S = 20.0` (cycle.py:37); total cycle deadline `DEADLINE_TOTAL_S = 240.0` (cycle.py:41).

### 1.7 Paging, completeness and reply parsing
- REST (G3, G4) `_rest_read` 592-628: up to `PAGE_CAP` pages; payload must be a list with `<=100` items; each item needs a positive `int` `id` (bool rejected, `_pos_int` 520-524); a repeated id returns `incomplete` (619); a page with `<100` items ends the read (626-627); 5 full pages return `incomplete` (628); any malformed item returns `non_json` with the caller's `unreadable` reason (624-625).
- GraphQL (G5, G6) `_graphql_read` 645-702: needs `data.repository.issue.<connection>.nodes` list (<=100) and boolean `pageInfo.hasNextPage`; non-null `errors` returns the unreadable reason with `_errors_kind` kind (676-677); repeated cursor -> `incomplete` (692-693); `hasNextPage` true with no cursor -> `incomplete` (696-697); cursor failing `_valid_cursor` -> `non_json` (698-699); page cap -> `incomplete` (702).
- Parsers: `_event` 708-722 (label and actor required only for `labeled`/`unlabeled`); `_marker` 725-736 (a null login is dropped, never own login); `_edited_at` 739-746 (key missing is `_Malformed`, explicit null is "never edited"); `_comment_edit` 753-761; `_project_item` 764-775 (`fieldValueByName` null or without name -> `status_name` None; comment at 768 marks the shape `[UNVERIFIED]`, FU-1).
- Every typed read returns `Read(value, reason, kind, retry_after_s)` (467-477) and never raises for a malformed reply. `ValueError` only on an unsafe caller value before any call.

### 1.8 Closed failure vocabulary (github-side)
- `Reply.kind`: timeout, non_json, ok, auth_failed, scope_missing, rate_limited, transient, failed.
- `Read.kind` additionally: incomplete (github.py:481-484, 619, 628, 693, 697, 702), budget_exhausted (588), truncated (824), discovery_duplicate (830).
- Shared reasons `_SHARED_REASONS` 489-496: timeout and transient -> `gh_timeout`; non_json -> `gh_non_json`; rate_limited -> `rate_limited`; scope_missing -> `project_read_failed`; anything else -> `gh_auth_failed` (`_shared_failed` 584-585).
- Per-issue reasons: `events_unreadable`/`events_incomplete` (G3), `marker_unreadable` (G4, incomplete too), `edits_unreadable` (G5), `project_unreadable` (G6), `revalidation_transient`/`revalidation_failed` (G7), `budget_exhausted`. All are names in `audit.REASON_TABLE` (audit.py:32-98): the shared ones have kind `cycle`, exit 3 (`gh_auth_failed` 43, `gh_timeout` 44, `gh_non_json` 45, `project_read_failed` 46), 4 (`truncated` 48, `discovery_duplicate` 49), 5 (`rate_limited` 51, `rate_limit_clamped` 52); the per-issue ones are kind `skip`, exit 0 (audit.py:69-82) except `revalidation_transient`, kind `entry`, exit 7 (audit.py:85). `_val` and `_rv` in the cycle turn `scope_missing` into the cycle stop `project_read_failed` (cycle.py:842-843, 971-972).

### 1.9 Key Takeaways (github.py)
- All seven `gh` argvs (G1-G7, plus reserved variants G3' and G6') are reads; `--repo IronbellyOrg/IronClaude` appears only on G2; the other repository bindings are literal in the REST path or the GraphQL query.
- Budget is 35 per-issue calls with the last 3 reserved for the pre-launch re-read; G1 and G2 are counted separately, giving a hard ceiling of 37 `gh` calls per cycle.
- Rate-limit headers are only readable for G1; every other rate limit takes the 3600 s clamp (`rate_limit_clamped`, exit 5).
- Reply shapes for GraphQL, the cursor alphabet and `GH_ERROR_SIGNS` are labelled `[UNVERIFIED]` in the source (github.py:71-72, 125, 267, 768).
- No gh write exists in this package.

## 2. launch.py (370 lines): the one Orca command, the origin check, Orca discovery

Module docstring (launch.py:1-9): finds Orca, checks the worktree origin and launches one claim session; the only text that can follow `--prompt` is what `build_claim_prompt` builds from a validated `int`; every command runs through the injected `Runner` with a real timeout; the module writes no state and caches nothing; imports only the standard library, `runner` and `_ORCA_CLIS` (launch.py:11-24). `_ORCA_CLIS = ("orca-ide", "orca")` at `src/superclaude/cli/install_user_setup.py:36`.

### 2.1 Constants and vocabularies
| Symbol | Line | Value |
|---|---|---|
| `ORCA_AGENT` | 28 | `"claude"`; comment 26-27: names the Orca agent, "deliberately not configurable" |
| `MAX_ISSUE_NUMBER` | 30 | 999_999_999 |
| `PROMPT_PATTERN` | 33 | `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$` |
| `OPERATION_ID_PATTERN` | 36 | `^[A-Za-z0-9._:-]{1,128}$` |
| `OPERATION_ID_PATHS` | 42-45 | `(("receipt","operation_id"),("error","operation_id"))`; comment 39-41 "[PROPOSAL, UNVERIFIED]" |
| `OP_UNKNOWN_TEXT` | 47 | `"agent_session_operation_unknown"`; docstring 48 "(C16, UNVERIFIED)" |
| `ORIGIN_REPO` | 50 | `"ironbellyorg/ironclaude"` (compared lower-cased) |
| `ORIGIN_MISMATCH` | 53 | `"origin_mismatch"` |
| `LaunchKind` | 56 | Literal `launched`, `unknown`, `spawn_error` |
| `LAUNCH_DETAILS` | 58-69 | frozenset of 8: ok, spawn_error, timeout, exit_nonzero, non_json, no_operation_id, operation_id_invalid, op_unknown |

### 2.2 The one fixed launch command (every element verified)
`launch_argv(orca, worktree, prompt)` launch.py:95-116 returns exactly this 12-element list (list literal at 103-116):
1. `orca` (the absolute path chosen by `find_orca`, not the literal word)
2. `"agent"` 3. `"launch"` 4. `"--agent"` 5. `ORCA_AGENT` = `"claude"` 6. `"--worktree"` 7. `"path:" + str(worktree)` 8. `"--surface"` 9. `"terminal"` 10. `"--prompt"` 11. `prompt` 12. `"--json"`
Rendered: `<orca> agent launch --agent claude --worktree path:<abs worktree> --surface terminal --prompt "/sc:issue --claim <N> --pipeline none" --json`. Count of elements is 12 (verified by counting the literal, launch.py:104-115). There is no permission flag and no model flag (matches design claim; the list is the whole argv).
- Guard: `launch_argv` raises `ValueError("prompt must come from build_claim_prompt")` unless `PROMPT_PATTERN.fullmatch(prompt)` (launch.py:101-102). `build_claim_prompt(n)` accepts only `type(n) is int` in 1..999999999 (a bool, str or float raises) and returns `f"/sc:issue --claim {n} --pipeline none"` (launch.py:84-92). The pipeline level `none` is hard-coded; no config key, argument or environment value changes it. Grep `--pipeline` over `P` returns exactly three lines, all in launch.py: 33 (`PROMPT_PATTERN`), 85 (docstring) and 92 (the f-string).
- `retry_argv(orca, worktree, prompt, operation_id)` launch.py:119-132 returns `launch_argv` with `"--retry-launch", <id>` inserted before `"--json"` (14 elements); `ValueError` unless the id fits `OPERATION_ID_PATTERN` (the argv is printed as a shell command by `status`). Its only production caller is `cycle.status_report` (cycle.py:1308-1312), which PRINTS the argv for an operator; nothing runs it (see section 2.7).
- The launch is executed by `OrcaLauncher.launch` launch.py:358-370: `argv = launch_argv(...)`, `_check_timeout` (positive number, bool refused), then `self._runner.run(argv, seconds, cwd=str(worktree))`, mapped by `outcome_of`. It is "the only call in the package that passes `cwd`" (docstring 363). Orchestration caller: `cycle._launch` at cycle.py:1099, `d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)` with `LAUNCH_TIMEOUT_S = 120.0` (cycle.py:40). `cli.build_deps` wires `launcher=OrcaLauncher(runner)` (cli.py:68).
- No worktree is created by this module or by anything in `P`: the `--worktree path:<abs>` value is `cfg.worktree`, an operator-supplied existing directory (`launch_cwd=str(cfg.worktree)` cycle.py:1086; `validate_setup` raises `worktree_invalid` unless `os.path.isdir(config.worktree)`, cycle.py:371-377). Grep `--pipeline|worktree create|worktree add|git.*worktree` over `P` returns only the three `--pipeline` lines above and launch.py:244 (`git -C <worktree> remote get-url origin`, a read); no `worktree create` or `worktree add` string exists in `P`.

### 2.3 Orca discovery (`find_orca`, launch.py:163-203)
For each name in `_ORCA_CLIS` (`orca-ide`, then `orca`): `which(name)`; skip when the result is empty or not absolute (`os.path.isabs`, launch.py:195; a relative path would run in the worktree as `cwd`); read the per-probe timeout (`allowance`, may be a callable so the cycle deadline is re-read per probe; None ends the search); run `[path, "skills", "list", "--json"]` (launch.py:200-201) and accept the path only when `_lists_orca_cli` is true: exit 0, not timed out, no spawn error, stdout a JSON object whose `topics` is a list of dicts with one `name == "orca-cli"` (launch.py:144-160). Returns the first accepted path, else None. Result is not cached. Default timeout 10.0 s; cycle passes `PROBE_TIMEOUT_S = 10.0` (cycle.py:38, 1041-1048).
Parity with `install_user_setup._find_orca` (install_user_setup.py:247-253 loops the same `_ORCA_CLIS`) is pinned by `tests/issue_watch/test_find_orca_parity.py`.

### 2.4 Origin check (`check_origin`, launch.py:233-251) and `parse_origin` (215-230)
Runs `["git","-C",<worktree>,"remote","get-url","origin"]` (launch.py:244) through the runner (no `cwd`). Returns None only when exit 0, no timeout, no spawn error and `parse_origin(stdout)` yields `owner/repo` whose lower-case equals `ironbellyorg/ironclaude`; otherwise `"origin_mismatch"` (including a None timeout, which starts no process). `parse_origin` accepts only `https://github.com/<owner>/<repo>[/]` and `git@github.com:<owner>/<repo>[/]` (patterns launch.py:209-212), strips `.git`, rejects `.`/`..` segments. Callers: `_steps` cycle.py:721 (before discovery) and `_launch` cycle.py:1074 (just before the pending write; also guarded by `launch_allowed()` at 1069 and 1078). Exit code for `origin_mismatch` is 2 (audit.py:32).

### 2.5 Reply handling (`outcome_of`, launch.py:326-349; helpers 287-323)
The launch reply is mapped in this order:
1. `spawn_error` set -> `LaunchOutcome("spawn_error", None, "spawn_error")`.
2. `timed_out` -> `unknown`, detail `timeout` (keeps a valid id found in stdout/stderr JSON objects).
3. `agent_session_operation_unknown` text anywhere in stdout or stderr -> `unknown`, detail `op_unknown` (even if an id is present).
4. non-zero exit -> `unknown`, detail `exit_nonzero`.
5. exit 0 but stdout not a JSON object -> `unknown`, `non_json`.
6. JSON object with no value at `receipt.operation_id` then `error.operation_id` (first non-None path wins, `_first_hit` 292-303) -> `unknown`, `no_operation_id`.
7. a value that is not a string matching `OPERATION_ID_PATTERN` -> `unknown`, `operation_id_invalid`.
8. otherwise `LaunchOutcome("launched", <id>, "ok")`.
`LaunchOutcome.__post_init__` (launch.py:266-274) refuses a bad kind, a bad detail, a bad id, and a `launched` outcome with no id. The reply fields `outcome.kind` and `receipt.detail` that the fixtures contain are NOT read anywhere in launch.py (only the two operation-id paths are). In the cycle, only `outcome.kind` and `outcome.operation_id` are used (cycle.py:1101-1112); `outcome.detail` has no reader in `src` (Grep `.detail` over src returns no launch-outcome hit).

What is assumed about Orca reply shapes: (a) a success reply is a JSON object on stdout carrying the id at `receipt.operation_id`; (b) a lost-reply error carries `agent_session_operation_unknown` as text and the id at `error.operation_id` in a JSON object on stdout or stderr; (c) exit code 0 means accepted. All three are labelled `[PROPOSAL, UNVERIFIED]` / `UNVERIFIED` in the source (launch.py:39-41, 47-48) and are exercised only by the `_assumed_shape` fixtures (section 6).

### 2.6 What the launched prompt does (boundary only)
The watcher's launch is a Claude session in a terminal in the existing worktree that receives `/sc:issue --claim <N> --pipeline none`. What that session writes to GitHub (assign, comment with the claim marker) is outside this file's code and is covered by research file 04. In this area: the watcher itself never reads the session's output; it learns the outcome only by seeing the session's own claim-marker comment through G4 in a later cycle (`_hit` cycle.py:848-865 -> `_claim` 896-899 -> `record.mark_claimed`).

### 2.7 Status, BUILT-ON / BUILT-OFF for launch.py pieces
| Piece | Status | Evidence |
|---|---|---|
| `launch_argv`, `build_claim_prompt`, `find_orca`, `check_origin`, `OrcaLauncher.launch`, `outcome_of` | BUILT-OFF (enabled:false) | Reachable only through `once` (cli.py:111-137) -> `_Cycle.run`, which stops `not_enabled` unless `config.enabled` or `--dry-run` (cycle.py:685-686); `enabled` default False (`raw.get("enabled", False)`, must be a JSON bool, cycle.py:228-230). In `--dry-run`, `_launch` returns before any probe or launch (cycle.py:1029-1035). |
| `retry_argv` | BUILT-ON for printing only (inside `status`); automatic retry NOT BUILT | `cycle.status_report` prints it (cycle.py:1308-1312); no caller runs it (Grep above); design FU-8 "Automatic retry with --retry-launch" is deferred (issue-watcher.md:867; issue-watcher-setup.md:682). |

(`status` is read-only and has no `enabled` gate, so the print path is live for any operator who runs it.)

### 2.8 Evidence commands (results)
- Grep `retry_argv` over `src`: definition launch.py:119, use cycle.py:1310 only.
- Grep `--pipeline|worktree create|worktree add|git.*worktree|import subprocess|from subprocess` over `P`: hits launch.py:33, 85, 92, 244 and runner.py:10 only.
- Grep `\.detail\b|LAUNCH_DETAILS` over `src`: `LaunchOutcome.detail` is defined and validated in launch.py (58-70, 266-270) and never read elsewhere (the only `.detail` in `P` outside launch.py is `ConfigError.detail`, cycle.py:93, cli.py:80).

### 2.9 Key Takeaways (launch.py)
- Exactly one command can start a session: a 12-element `orca agent launch ... --json` with a prompt fixed to `/sc:issue --claim <N> --pipeline none`; the pipeline level is hard-coded `none` and the agent is hard-coded `claude`.
- No worktree is created; the target is the operator-configured existing checkout, used both as `--worktree path:` and as the process `cwd`.
- Every non-success reply is `unknown` (never retried automatically) except a failure to start the process, which is `spawn_error`.
- The Orca reply shape is assumed, not captured; only `receipt.operation_id` and `error.operation_id` and one error word are read.
- `retry_argv` exists only to print an operator command.

## 3. record.py (865 lines): `FileStore`, `dispatch.json` and the state machine

Module docstring (record.py:1-8): times are aware UTC in memory and `YYYY-MM-DDTHH:MM:SSZ` on disk; JSON object keys are decimal strings on disk and `int` in memory; the module never reads the clock, never runs a command and imports only the standard library and `predicates` at module level. `swarm.atomic` is imported lazily inside `save` and `save_dry_run` (record.py:372, 853; comment "C18").

### 3.1 Files under `state_dir` (all constants record.py:281-283, 805)
| File | Mode | Created by | Written by | Readers | Format |
|---|---|---|---|---|---|
| `<state_dir>/` | 0700 | `init_state` (`makedirs(mode=0o700)` + `chmod 0o700`, record.py:777-778) | - | - | directory |
| `dispatch.json` (`STORE_FILE` 281) | 0600 (`os.chmod(path, 0o600)` record.py:377) | `init_state` -> `FileStore.save` (795) | `FileStore.save` from `once` real cycles (cycle.py:603, 1143, 1097) and `reset` (cli.py:224-229) | `FileStore.load` (`once`, `reset`); `cycle._read_store_doc` plain `open(..., "rb")` for `status` (cycle.py:1231-1248) | JSON, `sort_keys=True`, `indent=2`, `ensure_ascii=True`, trailing newline (record.py:374-376) |
| `lock` (`LOCK_FILE` 282) | 0600 | `init_state` (`O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW`, mode 0o600, record.py:782-784) | nothing writes bytes; used only for `flock` | `FileStore.lock` (record.py:381-419) | empty regular file |
| `DISABLED` (`DISABLED_FILE` 283) | operator-chosen | operator (`touch`); no code creates it | - | `FileStore.disabled()` (421-423), `disabled_since()` (425-431), cycle checks cycle.py:712 and 1063; `status_report` cycle.py:1292 | presence only (existence; mtime for status) |
| `dry-run.json` (`DRY_RUN_FILE` 805) | 0600 | first dry-run write | `save_dry_run` record.py:851-865 (from `_commit_shadow`, cycle.py:1146-1162) | `load_dry_run` 831-848 (from `_steps`, cycle.py:727) | JSON keys `schema_version, considered, shadow_launches` (`_DRY_RUN_KEYS` 806) |
| `dispatch.json.<random>.tmp` | mkstemp default (owner-only) | `write_prepared_bytes` (swarm/atomic.py:22-26) | removed on exception (atomic.py:33-38); an orphan after a hard crash is not removed by any code in `P` | none | transient |
`audit.jsonl` and its rotations belong to another area (research 01/03).

### 3.2 `dispatch.json` schema
Top-level keys (exact set, `_STORE_KEYS` record.py:120-130, `validate` rejects any other set, 225-226): `schema_version` (must equal `SCHEMA_VERSION = 1`, 31), `created_at`, `next_permitted_at`, `last_completed_cycle_at`, `considered` (object issue -> UTC time), `consumed_log` (list of UTC times), `entries` (object issue -> entry). Object keys are decimal strings matching `[1-9][0-9]{0,8}` (`_DECIMAL_KEY` 132; `_issue_key` 159-165 also requires `valid_issue_number`).
Entry: the 17 fields of `Entry` (record.py:69-88), all always present (`_ENTRY_KEYS = frozenset(Entry.__dataclass_fields__)` 131; `_entry` requires `set(raw) == _ENTRY_KEYS` 170-171): `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `approved_at`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at`, `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason` (count verified: 17).
Validation (record.py:168-210): `issue` equals its key; `state` in `ENTRY_STATES` (34-36, six: `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed`); `attempts` int >= 0; `launches` in {0,1}; `operation_id` null or `valid_operation_id`; `launch_cwd` null or an absolute string; `approver_id`, `approval_event_id`, `launch_account_id` null or `int`; `launch_login` and `last_reason` null or `str` only (their membership in the audit reason table is not checked here, docstring 221-224); `launches == 1` needs `consumed_at` and `pending_at` (206-207); `state == "failed"` needs `launches == 0` (208-209). Write-only fields: `launch_login` and `launch_account_id` have no reader in `src` other than validate/serialize (Grep above), so they are recorded only for later inspection.
Migrations: `MIGRATIONS` ships empty (record.py:247); `migrate` 251-278 raises `store_invalid` for a non-int version, a version above 1, or a missing step; `FileStore.load` never saves (docstring 348, `migrated` flag 345, 367); `_load` saves a migrated store only in a real cycle (cycle.py:746-747).

### 3.3 Constants
`MAX_ATTEMPTS = 3` (434), `BACKOFF = 10 min` (437), `LEASE = 60 min` (440), `DAY_CAP_WINDOW = 24 h` (443), `_FAIL_REASONS = {prompt_invalid, revalidation_transient}` (446), `_CLAIMABLE = {launched, unknown, abandoned}` (447), `_RESETTABLE = {abandoned, unknown}` (448). `DAY_CAP = 6` is cycle.py:36 (day-cap check `_day_cap_reached` cycle.py:867-876 adds dry-run shadow launches).

### 3.4 Transitions T-1..T-13 (design labels; code is the pure function that performs each)
All functions are pure (document in, document out, `now` as parameter). Any (state, trigger) pair not listed raises `TransitionError` via `_refuse` (record.py:451-452). Production callers are in cycle.py/cli.py.
| T | From -> To | Trigger | Code (record.py line) | Production caller |
|---|---|---|---|---|
| T-1 | no entry -> `failed` (attempts 1) | `prompt_invalid` or `revalidation_transient` before pending | `fail` 503-525 | `_fail` cycle.py:1018-1024 (calls at 1056, 1060) |
| T-2 | `failed` -> eligible again | `attempts < 3` and `now >= updated_at + 10 min` | `backoff_elapsed` 528-535 (read-only test, raises if not `failed`) | `_examine` cycle.py:934 |
| T-3 | `failed` -> `abandoned` (`attempts_exhausted`) | third failure (`attempts >= MAX_ATTEMPTS`) | `fail` 514-524 | same as T-1 |
| T-4 | no entry or `failed` -> `pending` | every check passed, about to launch | `mark_pending` 538-568 (sets `launches=1`, `consumed_at`, `pending_at`, `updated_at`, `last_reason=None` and the six `PendingContext` fields; validates ids, absolute `launch_cwd`, non-empty login) | `_launch` cycle.py:1091 |
| T-5 | `pending` -> `launched` | outcome `launched` | `mark_launched` 580-596 (`operation_id`, `lease_expires_at = now + 60 min`, `last_reason="launched"`) | cycle.py:1103 |
| T-6 | `pending` -> `unknown` | outcome `unknown` | `mark_unknown` 599-617 (keeps a valid id or None; `last_reason="launch_unknown"`) | cycle.py:1107 |
| T-7 | `pending` -> `abandoned` (`spawn_error`) | outcome `spawn_error` | `mark_spawn_error` 620-624 | cycle.py:1110 |
| T-8 | `pending` -> `abandoned` (`pending_orphan`) | any `pending` entry found at cycle start (crash between pending write and outcome) | `sweep` 627-651 | `_sweep` cycle.py:777-792 (called from `_steps` 723) |
| T-9 | `launched` -> `abandoned` (`claim_not_observed`) | `now >= lease_expires_at` (or no lease) | `sweep` 640-643 | same |
| T-10 | `launched`/`unknown`/`abandoned` -> `claimed` | own claim marker seen in the window | `mark_claimed` 654-686 (`_CLAIMABLE`) | `_claim` cycle.py:896-899 |
| T-11 | no entry -> `claimed` | marker seen for an issue never launched by the watcher | `mark_claimed` (state None) | same |
| T-12 | `failed` -> `claimed` | marker seen | `mark_claimed` (state `failed`) | same |
| T-13 | `abandoned`/`unknown` -> entry removed | `reset N --forfeit-guarantee` | `reset_entry` 706-720 (non-null `consumed_at` moves to `consumed_log`; then pruned) | `cli._reset_locked` cli.py:246 |
Also: `reset_rate_limit` 723-725 (clears `next_permitted_at`; cli.py:243), `set_next_permitted` 728-730 (cycle.py:667, 760), `set_last_completed` 733-735 (cycle.py:1139), `set_considered` 738-745 (cycle.py:1136), `prune_consumed_log` 693-696 (cycle.py:1142, record.py:720), `day_cap_count` 699-703 (counts `consumed_at` of all entries plus `consumed_log` in `(now-24h, now]`).
`claimed` is terminal: no function leaves it. A `claimed` or `pending` entry makes `_examine` skip with `already_dispatched` (cycle.py:920-921).
Note: the T-numbers are the design's labels (`docs/designs/issue-watcher.md` section 7.4); the code itself names transitions only in docstrings (T-1/T-3 record.py:504, T-2 529, T-4 539, T-5 581, T-6 600, T-7 621, T-8/T-9 628, T-10..T-12 661-663, T-13 707). All thirteen labels are therefore matched to code in this table [CODE-VERIFIED] by docstring plus function body.

### 3.5 Write-ahead (pending before launch) and crash recovery
Order inside `_launch` (cycle.py:1081-1112): `mark_pending` (1091) then `_save()` (1092, comment "FR-010: durable before the launch call"); then a deadline recheck that, if the 120 s cut-off has passed, restores `before_pending` and saves again (1093-1098, no launch); then `launcher.launch` (1099); then `mark_launched` / `mark_unknown` / `mark_spawn_error` (1101-1112); final `_commit_store` (1128-1144) writes the last document. Save is atomic (section 3.6). Consequences:
- Crash before the pending save: the old file stands; nothing was launched.
- Crash after the pending save and before the launch call: a `pending` entry with `launches=1` exists; the next cycle's `sweep` turns it into `abandoned`/`pending_orphan` (T-8). There is no relaunch: `launches` and `consumed_at` stay set and `consumed_at` counts toward the day cap.
- Crash after the launch started and before the outcome was written: same as above (`pending_orphan`); the claim session may still run and post its marker, in which case a later `_examine` finds `abandoned` with `pending_at` set and a marker hit and moves it to `claimed` (T-10) (cycle.py:922-931).
- `launched` with no marker by lease expiry -> `abandoned` `claim_not_observed` (T-9).
- At-most-once: an entry with state `pending`, `launched`, `unknown`, `abandoned` or `claimed` is never relaunched; only `reset N --forfeit-guarantee` (T-13) removes `abandoned`/`unknown`.
- Crash tests: `tests/issue_watch/test_crash_injection.py` asserts the launcher is called at most once across 6 cycles for crash points C1-C5 (see table in section 5). The design's C1-C5 table is documentation; the write order above is the code evidence.

### 3.6 Atomic write, flock, init
- Save (record.py:370-378): `json.dumps(sort_keys, indent=2, ensure_ascii)` + `"\n"` encoded; `write_prepared_bytes` (`src/superclaude/cli/swarm/atomic.py:14-39`: `tempfile.mkstemp(prefix=<name>., suffix=.tmp, dir=<same dir>)`, write, flush, `os.fsync`, `os.replace`; the temp file is unlinked on a caught `Exception`); then `os.chmod(path, 0o600)`; then `_fsync_dir(state_dir)` (310-315, `O_RDONLY|O_DIRECTORY`). A failed write surfaces as `OSError` which the cycle maps to `state_dir_unwritable` (cycle.py:601-605; exit 6, audit.py:40).
- Lock (record.py:380-419): opens `state_dir/lock` with `O_RDWR|O_NOFOLLOW|O_CLOEXEC` (no `O_CREAT`, so the lock must already exist: `lock_missing` for a missing file, `lock_invalid` for any other open error, e.g. a symlink or directory); requires a regular file owned by the effective uid (`lock_invalid` otherwise); `fcntl.flock(fd, LOCK_EX | LOCK_NB)` (a `BlockingIOError` is `LockHeld`, exit 75, audit.py:54); after locking it re-`stat`s the path (no follow) and raises `LockHeld` if the path vanished, changed device/inode, or `st_nlink == 0` (replacement detection, 406-414); releases with `LOCK_UN` and closes in `finally` (416-419). `fcntl` is imported inside the method (389) so the package imports off Linux. The cycle takes the lock around the whole body (cycle.py:694-697); `reset` takes it too (cli.py:326); `status` takes none.
- `init_state` (record.py:753-802): refuses (`StateExists`) when `dispatch.json` or `lock` already exists (checked before creating anything, 773-775); creates the directory 0700, creates `lock` with `O_EXCL|O_NOFOLLOW` 0600, `fchmod 0600`, saves the empty document with `created_at = now` (the approval floor, used by `approval_of` as `store_created_at`, cycle.py:889); if the first save fails the created lock is removed (796-801).

### 3.7 DISABLED kill switch
`FileStore.disabled()` is `os.path.lexists(state_dir/"DISABLED")` (record.py:421-423; a dangling symlink counts). The cycle checks it first inside the lock (`_steps` cycle.py:712-713, reason `disabled`, kind `cycle`, exit 0 per audit.py:59) and again right before the launch (cycle.py:1063-1064, `disabled_mid_cycle`, exit 0, audit.py:60, `stamp=True`). `status_report` shows its mtime via `disabled_since` (cycle.py:1292, 1329). Nothing in `P` creates or deletes the file; the operator does. `record.disabled_present` (748-750) is a second module-level helper with the same body that has no production caller (see Defect section).

### 3.8 Dry-run shadow store
In `--dry-run`: no `dispatch.json` write (a migrated store is not saved, cycle.py:746), no Orca probe or launch (cycle.py:1029-1035); the would-be launch is appended to `shadow.shadow_launches` in memory (cycle.py:1032-1034) and persisted with `considered` into `dry-run.json` by `_commit_shadow` (cycle.py:1146-1162) only when something was examined, would-launched or reset (1151-1152). `shadow_launches` older than 24 h are dropped on write (1157-1158) and count toward the day cap in later dry runs (cycle.py:871-875). An unreadable or invalid shadow file is replaced by an empty one with the `dry_run_shadow_reset` warning (record.py:831-848; cycle.py:730-731). Mode 0600, written atomically the same way as the store (record.py:851-865).

### 3.9 Key Takeaways (record.py)
- `dispatch.json` is a strictly validated 7-key document with 17-field entries and six states; any extra or missing key makes the whole store `store_invalid` (exit 6).
- The write-ahead rule (pending saved durably before the launch call) gives at-most-once launching; every crash leaves `pending_orphan`, never a relaunch.
- Locking is a non-blocking `flock` on a pre-created `lock` file with symlink, owner and replacement checks; a held lock is exit 75.
- The DISABLED file is the only kill switch in the store layer; it is checked at cycle start and again just before launch.
- Dry-run keeps a separate `dry-run.json` and never touches `dispatch.json`.

## 4. runner.py (130 lines): the only subprocess module

- Module docstring (runner.py:1-6): the only module of `issue_watch` that imports `subprocess`; never parses output and knows nothing about the program it runs. `import subprocess` at runner.py:10.
- `CommandResult` frozen dataclass (runner.py:19-35): `argv` tuple, `returncode` (None on timeout or spawn failure), `stdout`, `stderr`, `timed_out`, `spawn_error` (class name only), `duration_s`.
- `Runner` Protocol runner.py:38-45: `run(argv: list[str], timeout: float, *, cwd: str | None = None)`.
- `SubprocessRunner.run` runner.py:70-130: raises `TypeError` unless `argv` is a non-empty `list[str]` (82-87); calls `subprocess.run(argv, shell=False, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, stdin=subprocess.DEVNULL, cwd=cwd)` (91-101); `TimeoutExpired` -> `timed_out=True`, partial stdout and capped stderr (102-111); `OSError` or `ValueError` -> `spawn_error=<class name>`, empty output (112-121).
- Stderr cap: `STDERR_CAP_BYTES = 500` (runner.py:15); `_cap_stderr` (57-64) cuts the UTF-8 bytes to 500 and drops a split character. Applied on both the normal path (126) and the timeout path (107). stdout is not capped.
- Grep evidence for "only module importing subprocess": Grep `import subprocess|from subprocess` over `P` returns runner.py:10 only; Grep `subprocess` over `P` additionally returns docstring mentions at cli.py:7, cycle.py:5, cycle.py:1217 (all saying the module never imports it) and runner.py's own uses (68, 91, 99, 102). The AST rule is pinned by `tests/issue_watch/test_no_shell.py` and `test_module_boundaries.py` (area 03).

### Key Takeaways (runner.py)
- Every external command of the watcher (gh, git, Orca probe, Orca launch) goes through `SubprocessRunner.run` with an argv list, `shell=False`, closed stdin and a mandatory timeout.
- Only the Orca launch passes `cwd`.
- stderr is capped at 500 bytes; stdout is returned whole.

## 5. Who reads and writes `dispatch.json` (whole-snapshot search)

Commands run: Grep `dispatch\.json` over the snapshot excluding `tests`, (hits: `src/superclaude/cli/issue_watch/cycle.py` 1219, 1232, 1279; `.../record.py` 1, 93, 214, 281, 348, 754, 757; docs `issue-watcher-setup.md`, `issue-watcher.md`, `orchestrator.md`); Bash `grep -rIl 'dispatch\.json'` over the whole snapshot excluding `tests/` returns exactly five files (cycle.py, record.py, `docs/designs/orchestrator.md`, `docs/designs/issue-watcher-setup.md`, `docs/designs/issue-watcher.md`); a search of the hidden and non-src trees `.github`, `.claude`, `plugins`, `scripts`, `Makefile`, `pyproject.toml`, `package.json` for `dispatch.json`, `issue-watch` and `issue_watch` returned nothing. Grep `FileStore|STORE_FILE|issue-watch/|issue_watch\.record` outside tests and docs: only cli.py, cycle.py, record.py. Tests that mention the file: `tests/issue_watch/{test_no_text,test_cli,test_record,test_security_invariants,test_cycle,test_concurrency,test_crash_injection,conftest,test_cli_e2e}.py`.

| Role | Code | Evidence |
|---|---|---|
| Writer: create | `record.init_state` -> `FileStore.save` (first write) | record.py:795; verb `init-state` cli.py:201-214 |
| Writer: cycle | `_Cycle._save` (migrated store, pending write, restore) and `_commit_store` (final write) | cycle.py:601-606, 747, 1092, 1097, 1143 |
| Writer: operator reset | `cli._save` from `_reset_locked` (`reset_rate_limit`, `reset_entry`) | cli.py:224-229, 243, 249; verb cli.py:282-348 |
| Reader: cycle and reset (under lock) | `FileStore.load` | cycle.py:742; cli.py:241 |
| Reader: status (no lock, no write) | `cycle._read_store_doc` plain `open(path, "rb")` then `record.migrate` + `record.validate` | cycle.py:1231-1248, called at 1286 by `status_report`; verb cli.py:164-182 |
| Reader: docs-only owner snippet | `record.FileStore(state).load()` inside an owner-run Python block that calls `cycle.slo_numbers(lines, doc, now)` | `docs/designs/issue-watcher-setup.md:473-474`. `slo_numbers` (cycle.py:1359) has no caller in `src` (Grep `slo_numbers` over `src` returns only its definition), so this reader exists only if the owner runs that snippet |
No other reader found in snapshot. In particular: no hook script, skill script, agent file, workflow, plugin copy or CI file reads or writes `dispatch.json`. The claim session never reads it (the watcher learns the claim from the GitHub marker comment, not from a file). A design document, `docs/designs/orchestrator.md:115` and `:358`, describes a future use of `dispatch.json` ("wakes sent and acknowledged, each entry with the orchestrator it was routed to"); that design "holds no implementation code" (orchestrator.md:3) and no code in `src` implements it (section Defect Candidates, row N-4).

### Key Takeaways (readers and writers)
- All readers and writers are inside `issue_watch` (`cycle.py`, `cli.py`, `record.py`); nothing outside the package touches the file.
- `status` is the only lock-free reader; every writer holds the lock (cycle and `reset`) or is `init-state` (which creates the lock itself).

## 6. The `_assumed_shape` fixtures

Directory: `tests/issue_watch/fixtures/_assumed_shape/` holds 19 JSON files (12,059 bytes in total); `test_github.py:575-583` pins `len(files) == 19`, that each has `"_assumed_shape": true` and a non-empty `source` string; `test_github.py:585-597` (`test_every_assumed_shape_fixture_is_read_by_a_test__df32`) fails if any file name does not appear quoted in some `tests/issue_watch/test_*.py`. Each file's `source` field names `docs/designs/issue-watcher.md` section 15 (or 8.x) and says UNVERIFIED (read for 7 of them: orca_launch_success, orca_launch_unknown, orca_launch_no_operation_id, orca_launch_empty_operation_id, gh_api_user_include, gh_stderr_rate_429, gh_issue_reread; the other 12 `source` fields were printed by one `grep -m1 '"source"'` loop and all carry UNVERIFIED or "UNVERIFIED until FU-1" except `graphql_edits.json` and `graphql_project_items.json`, whose `source` text cites the design row and the DF-14 draft and does not itself contain the word UNVERIFIED in the first 230 characters printed); each of the four `orca_launch_*` notes says "The owner-run live test (FU-1) replaces this with a captured reply."
Absence check: Glob `docs/designs/issue-watcher*` returns only `issue-watcher.md` and `issue-watcher-setup.md`; `docs/designs/issue-watcher-live-test.md` does not exist, so every fixture is still an assumption (staleness hint confirmed). The design says the owner, not the implementation, writes that record (issue-watcher.md:33, 775, 854; issue-watcher-setup.md:272, 625).

| Fixture file | Stands in for (setup doc 14.1.1 table, issue-watcher-setup.md:601-619, and the file's own `source`) | Used by |
|---|---|---|
| `gh_issue_list.json` | G2 discovery reply (`gh issue list ... --json number,labels,assignees,state`) | test_github.py:1383; conftest.py:805 |
| `gh_issue_reread.json` | G7 projected re-read object (lower-case state, label and assignee arrays) | test_github.py:1668; conftest.py:885 |
| `gh_api_user_include.json` | G1 raw `--include` output: status line, headers, blank line, JSON body `{"login","id"}` | test_github.py:388, 548, 556, 562, 1600, 2027, 2048; test_no_text.py:763; conftest.py:783 |
| `gh_api_user_include_429.json` | rate-limited G1 reply with `Retry-After` | test_github.py:1495, 2035; conftest.py:788 |
| `rest_events_page.json` | G3 projected events page | test_github.py:1397; conftest.py:425 |
| `rest_comments_marker.json` | G4 projected comments with marker booleans, incl. null login | test_github.py:1442; conftest.py:463 |
| `graphql_edits.json` | G5 edit-timestamp reply | test_github.py:1464; conftest.py:837 |
| `graphql_project_items.json` | G6 project-items reply | test_github.py:1482; conftest.py:863 |
| `gh_graphql_rate_limited.json` | GraphQL `RATE_LIMITED` error type | test_github.py:436, 1901; conftest.py:507 |
| `gh_graphql_insufficient_scopes.json` | GraphQL `INSUFFICIENT_SCOPES` error type | test_github.py:418, 1151; conftest.py:506 |
| `gh_stderr_auth_401.json` | HTTP 401 stderr | test_github.py:404, 1535, 1804, 1851; conftest.py:499 |
| `gh_stderr_rate_403.json` | HTTP 403 rate-limit stderr | test_github.py:432, 1523, 1810, 1854; conftest.py:501 |
| `gh_stderr_rate_429.json` | HTTP 429 rate-limit stderr (`gh: HTTP 429: Too many requests, rate limit reached`) | test_github.py:433, 1593; conftest.py:500 |
| `gh_stderr_http_502.json` | HTTP 502 transient stderr | test_github.py:453, 1516, 1798, 1857; conftest.py:502 |
| `gh_stderr_scope_read_project.json` | missing `read:project` stderr | test_github.py:421, 1529, 1816; conftest.py:503 |
| `orca_launch_success.json` | Orca success reply: `outcome.kind: launched`, `receipt.detail`, `receipt.operation_id: "op-test-0001"` | test_launch.py:632, 644, 880; test_cli_e2e.py:342, 409; test_no_text.py:506; test_security_invariants.py:356; conftest.py:372 |
| `orca_launch_unknown.json` | Orca lost-reply error: exit 1, stderr holds JSON `{"error": {"code": "agent_session_operation_unknown", "message": ..., "operation_id": "op-test-0001"}}` | test_launch.py:638, 781; conftest.py:378 |
| `orca_launch_no_operation_id.json` | exit-0 reply with `outcome.kind: launched` but no id at any path | test_launch.py:894; test_cycle.py:3235 |
| `orca_launch_empty_operation_id.json` | exit-0 reply with `receipt.operation_id: ""` | test_launch.py:907; test_cycle.py:3246 |
(The "Used by" column lists the `tests/issue_watch/` lines that load each file, from `grep -n '"<name>.json"'` run in this research. The fixtures therefore also feed the shared fake world of `conftest.py` (`GhWorld`, `FakeLauncher`), which drives `test_cycle.py`, `test_cli_e2e.py`, `test_no_text.py` and `test_security_invariants.py` (research 01 and 03 areas): the assumed shapes underpin the whole suite, not only the unit tests of github.py and launch.py.)

What they stand in for: replies the implementation has never seen from the real tools. The code decodes `gh` replies and the Orca reply using these shapes (and the `GH_ERROR_SIGNS` strings and the two `OPERATION_ID_PATHS`), so a real reply that differs would be read as `non_json`, `failed` or `no_operation_id`, which fail closed (reads are skipped; a launch becomes `unknown`).

### Key Takeaways (fixtures)
- 19 fixtures, all flagged `_assumed_shape: true`; none is a captured reply; the live-test record that should replace them does not exist.
- A wrong assumption fails closed in every case traced: unreadable GitHub reads skip the issue, an unreadable launch reply becomes `unknown`.

## 7. Required deliverables

### (a) Test-pin table (wc -l and `grep -c 'def test_'` on the snapshot, run in this research)
| Path | Lines | Test count | What it pins | Key test names |
|---|---|---|---|---|
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_github.py` | 2161 | 141 | Part A (119-598): the seven argv written out literally, `--method GET` on every REST argv and none on GraphQL, GraphQL constants name the repo and never mutate, JQ projections equal the design text, no argv requests title or body, no upstream repo or placeholder, bad issue/page never reach an argv, constants (repo and caps), `classify` rows, `GH_ERROR_SIGNS` is the one table, rate-limit time and clamp, `Date` header, fixtures. Part B (599-1366): REST paging (99/100/101 items, repeated id, page cap 5, refused budget, `timeout_for` None), null rules, GraphQL paging and cursor handling, discovery (99 ok, >=100 truncated, duplicate), `CallBudget` (32 ordinary then refuse the 33rd, 3 reserved up to 35, shared counted in total only). Part C (1367-2161): fixture-driven reads, G1/G2 failure mapping, G7 re-read (reserved, other-number reply, transient vs failed), non-ok REST pages, exit-0 GraphQL `errors`, missing `lastEditedAt`, per-call timeout reaches the runner, CRLF header blocks, hostile trigger/login/cursor values never reach an argv | `g1_argv_is_literal__fr002`, `g2_argv_is_the_fr003_literal__fr003`, `every_gh_api_argv_but_g1_and_graphql_has_method_get`, `no_graphql_argv_has_method`, `graphql_constants_name_the_repo_and_never_mutate`, `repo_and_caps_are_literal`, `no_argv_names_the_upstream_or_a_placeholder`, `classify_rate_limited__fr028`, `rate_limit_wait_rows__fr028`, `rate_limit_wait_clamps_a_call_without_include__fr028`, `call_budget_allows_32_ordinary_calls_and_refuses_the_33rd__nfr009`, `call_budget_allows_3_reserved_calls_up_to_35__nfr009`, `call_budget_shared_calls_count_in_total_not_against_the_cap__nfr009`, `reread_may_use_the_reserved_calls_but_not_a_36th__nfr009`, `discover_100_or_more_results_are_truncated__ac2_fr004`, `rest_page_cap_never_fetches_a_sixth_page__fr005_fr006_fr009`, `every_assumed_shape_fixture_parses_and_is_labelled`, `graphql_hostile_end_cursor_is_unreadable_and_not_sent__df19` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_launch.py` | 952 | 66 | Part A: `build_claim_prompt` accepts only an int in 1..999999999; `launch_argv` equals the literal twelve elements with no extra flag; `ORCA_AGENT == "claude"`; `launch_argv` refuses any prompt not from `build_claim_prompt`; `retry_argv` inserts `--retry-launch <id>` right before `--json` and refuses an unsafe id; Orca probe (`orca-ide` before `orca`, skip missing and relative paths, default timeout 10 s, `timeout_for` callable per probe, reject reply not listing `orca-cli`); origin parse tables and `check_origin` (fork matches; every failure is `origin_mismatch`; literal git argv with no cwd). Part B (612-): outcome table (`spawn_error`, timeout, success, no id, non-JSON, non-zero exit, op-unknown text wins over a valid reply, invalid id), cwd equals worktree and only launch passes cwd, `OPERATION_ID_PATHS` and fixtures, agent pin, the prompt carries `--pipeline none` and the old prompt no longer matches | `ac8_launch_argv_equals_the_literal_twelve_elements__fr013`, `ac8_launch_argv_has_no_extra_flag__fr013_t10`, `ac8_orca_agent_is_pinned_to_the_literal_claude__fr013_df11`, `ac7_launch_argv_refuses_any_prompt_not_from_build_claim_prompt__fr012_t1`, `ac9_retry_argv_puts_retry_launch_right_before_json__fr015`, `fr013_probe_tries_orca_ide_before_orca`, `fr013_probe_skips_a_relative_path_without_a_probe__t17`, `ac16_check_origin_mismatch_for_another_repository__fr025_nfr003`, `ac8_op_unknown_wins_over_a_valid_success_reply__fr014`, `ac9_plain_text_never_yields_an_id__fr014_fr015_oq47`, `df01_only_the_launch_passes_a_cwd__fr013_fr025`, `build_claim_prompt_returns_exactly_the_pipeline_none_form`, `the_old_claim_prompt_no_longer_matches_and_launch_argv_refuses_it` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_record.py` | 2377 | 147 | Part A (171-894): load/validate (missing file `store_missing`, bad JSON, extra/missing keys at both levels, wrong types, non-decimal or overlong keys, deep nesting is `store_invalid` not `RecursionError`, unsafe operation id, `launches` 2, `failed` with a launch, one launch without its times, naive times, bad `schema_version`), migrate (ships empty, chains, never writes), save (byte-identical, sorted, ASCII, 0600 over a wider file, fsync of the directory last), lock (missing, symlink, dangling symlink, directory, foreign owner, held, nested, replaced after flock, released on exit), DISABLED. Part B (895-1537): T-1..T-13 one case each, every other (state, trigger) pair raises `TransitionError`, half-open windows (lease, backoff, 24 h), purity (input untouched), every reason written is in the audit table (DF-42). Part C (1538-2142): day cap, `consumed_log` pruning, `reset_entry` and `reset_rate_limit`, `sweep`, `init_state` (modes under any umask, exclusive create, refuses existing, removes its lock on a failed save), dry-run shadow load and save. Part D (2143-2377): input guards of the transitions, `set_considered` and setters. Its docstring (lines 4-5) states key lists are literal, not read from the module, so adding a field fails the pin | `schema_key_lists_match_the_module`, `ac22_launches_two_is_store_invalid__nfr011`, `ac22_deeply_nested_json_is_store_invalid_not_recursionerror__nfr011`, `ac22_file_store_migrates_in_memory_and_never_writes__nfr011`, `ac13_saved_file_is_sorted_indented_ascii_with_final_newline__fr019`, `save_forces_mode_0600_over_a_wider_existing_file`, `ac22_save_fsyncs_the_state_directory_last__nfr005`, `ac11_lock_replaced_or_unlinked_after_flock_is_lock_held__fr017`, `ac12_disabled_counts_for_any_content_or_a_dangling_link__fr018`, `t4_pending_from_no_entry_sets_launch_and_approval_fields__fr010_fr011`, `t5_launched_outcome_sets_operation_id_and_a_sixty_minute_lease__fr013`, `t8_sweep_abandons_a_pending_entry_as_pending_orphan__nfr005`, `t9_sweep_abandons_an_expired_launched_entry_as_claim_not_observed__nfr005`, `t13_reset_removes_the_entry_and_keeps_its_consumed_at__fr016_fr023_fr024`, `every_other_state_trigger_pair_raises_transition_error__nfr005`, `df43_fail_on_a_failed_entry_counts_up_one_two_three_then_abandons__nfr005`, `ac10_consumed_at_exactly_24h_old_no_longer_counts__fr016_fr023`, `ac17_init_state_refuses_an_existing_store_and_changes_nothing__fr026`, `ac13_a_flow_using_only_the_dry_run_helpers_never_saves_dispatch_json__fr019` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_concurrency.py` | 275 | 6 | Two real `spawn` processes on one store give one launch and one `lock_held`; an intact lock launches; a symlinked lock, a directory in place of the lock, and a missing lock (not created) are exit 6 with no `gh` call; a lock path replaced after `flock` is exit 75 with no call (docstring 1-13) | `test_two_processes_one_store_one_launch__fr017_ac11`, `test_intact_lock_launches_the_eligible_issue__fr017`, `test_symlinked_lock_is_exit_6_with_no_call__fr017_ac11`, `test_missing_lock_is_exit_6_and_is_not_created__fr017_ac11`, `test_lock_path_replaced_after_flock_is_exit_75_with_no_call__fr017_ac11` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_crash_injection.py` | 373 | 6 | One eligible issue; a crash (`SystemExit`) injected at design points C1 to C5, then FIVE more cycles against the same state directory: across all six runs the launcher is called at most once and a recorded launcher call always leaves `launches` 1 (docstring 1-11). `PROMPT` is `/sc:issue --claim 9 --pipeline none` (line 38) | `test_c1_crash_before_the_pending_save_leaves_the_store_untouched__nfr005`, `test_c2_crash_during_the_atomic_replace_keeps_the_old_file__nfr005`, `test_c3_crash_after_the_pending_save_is_swept_and_never_launched__nfr005`, `test_c4_crash_after_the_spawn_is_swept_and_never_launched_again__nfr005`, `test_an_exception_out_of_the_launcher_leaves_the_same_state_as_c4__nfr005`, `test_c5_crash_after_the_outcome_save_loses_only_the_audit_lines__nfr005` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_find_orca_parity.py` | 288 | 10 | `launch.find_orca` returns the same candidate as `install_user_setup._find_orca` for the same probe replies; where the original raises (topics null/int/bool/non-empty str/dict, or a non-dict element before `orca-cli`), `find_orca` only has to reject without raising (DF-36, C19); candidates shared and ordered; a screen-reader stub is rejected by both; no real process or `which` call survives | `test_ac25_find_orca_same_answer_as_the_original__fr013_nfr014`, `test_ac25_find_orca_rejects_where_the_original_raises__fr013_nfr014`, `test_ac25_candidates_are_shared_and_ordered__fr013_nfr014`, `test_t17_screen_reader_stub_is_rejected_by_both__fr013_nfr014`, `test_ac25_no_real_process_or_which_call_survives__nfr014` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_origin_parity.py` | 179 | 7 | `launch.parse_origin` equals `sc-issue-protocol/scripts/origin_repo.py:parse_origin_url` over one table; both keep host case-sensitive and keep owner/repo case; only `check_origin` compares lower-cased with `ironbellyorg/ironclaude`; the original module is loaded by path under a private name never registered in `sys.modules` | `test_ac16_parse_origin_matches_parse_origin_url__fr025_nfr003`, `test_ac16_parity_table_covers_every_required_shape__fr025_nfr003`, `test_ac16_original_module_is_not_registered_in_sys_modules__nfr003`, `test_ac16_only_check_origin_compares_lower_case__fr025`, `test_ac16_check_origin_rejects_what_parse_rejects_or_foreign__fr025` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/test_runner.py` | 226 | 16 | `SubprocessRunner`: `TypeError` for a str, empty or non-str argv; the call reaches `subprocess.run` without a shell (`shell=False`); `cwd` passed only when given; stderr kept whole when short and cut to 500 bytes when long, dropping a split multi-byte character; timeout gives `timed_out` and no return code; spawn error is the class name only (also for `ValueError`, real NUL byte in argv or cwd); non-UTF-8 child output is replaced, not raised; a real child timeout returns quickly | `test_str_argv_raises_type_error__nfr004`, `test_list_argv_reaches_subprocess_run_without_shell__nfr004`, `test_cwd_is_passed_when_given_and_none_otherwise`, `test_long_stderr_is_cut_to_500_bytes`, `test_stderr_cut_inside_multibyte_character_drops_the_partial_char`, `test_spawn_error_is_the_class_name_only`, `test_real_child_non_utf8_output_is_replaced_not_raised`, `test_real_child_timeout_returns_quickly__nfr008` |
| `/home/coder/.cache/ic-snap-20261120/master/tests/issue_watch/fixtures/_assumed_shape/` | 19 files (12,059 bytes) | n/a | Assumed `gh` and Orca replies (section 6); the directory count, the `_assumed_shape: true` label and "every fixture is read by some test" are pinned by `test_github.py:575-597` | `test_every_assumed_shape_fixture_parses_and_is_labelled`, `test_every_assumed_shape_fixture_is_read_by_a_test__df32` |
Note: `test_crash_injection.py` also defines two classes (`Run`, `Rig`) and `test_runner.py` one helper class (`RecordingRun`); `conftest.py` (1155 lines, assigned to research 01) supplies `FakeRunner`, `FakeLauncher`, `CrashingStore`, `GhWorld`, `tmp_state`. The test count column is `grep -c 'def test_'`; parametrized tests expand to more cases at run time (parametrize decorators counted by `grep -c 'pytest.mark.parametrize'`: github 47, launch 21, record 53, find_orca 6, origin 5, runner 1). No test was run in this research (read-only assignment); pass/fail state of these tests is not verified here.

### (b) Live-versus-off status per piece
| Piece | Status | Evidence that decides it |
|---|---|---|
| `github.py` G1-G7 read calls | BUILT-OFF (enabled:false) for real cycles | Only entry is `once` (cli.py:111-137); `_Cycle.run` stops `not_enabled` first when `enabled` is false and the run is not a dry run (cycle.py:685-686); `enabled` default False (cycle.py:228). The same reads DO run in `once --dry-run`, which ignores `enabled` (cycle.py:685). The shipped config is not in the snapshot, so the owner's actual value is [UNVERIFIED]; the design says it ships false (issue-watcher.md:3). |
| `CallBudget`, rate-limit clamp, `classify` | BUILT-OFF (enabled:false) | same entry path as above; called only from the cycle |
| `launch.py` `find_orca`, `check_origin`, `OrcaLauncher.launch` | BUILT-OFF (enabled:false) | Launch reachable only after `enabled` passes; dry-run returns before any probe or launch (cycle.py:1029-1035). `check_origin` also runs at cycle start (cycle.py:721) in dry runs (git read only). |
| `record.py` store and state machine inside `once` | BUILT-OFF (enabled:false) for `once` writes; not written in dry-run | cycle.py:685-686, 746, 1121-1124 |
| `record.init_state` / verb `init-state` | BUILT-ON (operator verb, no `enabled` gate) | cli.py:201-214 has no `enabled` test |
| verb `reset` and `FileStore.lock` use there | BUILT-ON (operator verb, no `enabled` gate) | cli.py:282-348 |
| verb `status` (`_read_store_doc`, `status_report`) | BUILT-ON (read-only, no `enabled` gate) | cli.py:164-182; cycle.py:1270-1335 |
| DISABLED kill switch | BUILT-ON (checked inside every cycle that gets past `enabled`) | cycle.py:712-713, 1063-1064; record.py:421-423 |
| dry-run shadow `dry-run.json` | BUILT-ON (dry-run only) | record.py:831-865; cycle.py:726-732, 1146-1162 |
| `runner.py` `SubprocessRunner` | BUILT-ON as a library; has no trigger of its own | used by `cli.build_deps` (cli.py:64); runs only when a verb runs a command |
| `retry_argv` printing in `status` | BUILT-ON (print only) | cycle.py:1308-1325 |
| Automatic `--retry-launch` | NOT BUILT | no caller runs `retry_argv`; deferred as FU-8 (issue-watcher.md:867; issue-watcher-setup.md:682) |
| Scheduler / timer that runs `once` | NOT BUILT | no trigger found in snapshot (see (d)) |
| Live-test record `docs/designs/issue-watcher-live-test.md` | NOT BUILT | Glob `docs/designs/issue-watcher*` lists two files only |
| Wake routing in `dispatch.json` (`docs/designs/orchestrator.md`) | NOT BUILT | section Defect Candidates N-4 |
| `record.disabled_present` | BUILT-ON as code but dead (no production caller) | section Defect Candidates D-1 |

### (c) Writes to GitHub, and every read-only `gh` call
- GitHub writes in this area: No GitHub write in this area. Evidence: (1) Grep `"gh"` over `P/*.py` returns only the five argv list literals in github.py (177, 183, 204, 231, 255), all reads (section 1.2); (2) Grep `mutation|POST|PATCH|DELETE|PUT` in github.py returns only the explanatory comment lines 107-108; (3) the only other commands in `P` are `git -C <worktree> remote get-url origin` (launch.py:244, a local read), `<orca> skills list --json` (launch.py:200, a local read per design 8.4 line 623, doc claim [UNVERIFIED] here), and `<orca> agent launch ...` (launch.py:103-116). The Orca launch is the one command that can lead to GitHub writes, but it is performed by the launched Claude session running `/sc:issue --claim <N> --pipeline none` (what that session writes is in research file 04), not by any code in this area. Docs agree: setup doc section 4 says the watcher "never writes to GitHub at all" (scope-2 hint; [CODE-VERIFIED] here by the greps above).
- Read-only `gh` calls (exact argv, `--repo IronbellyOrg/IronClaude` only on G2, repository fixed by literal elsewhere):
  - G1 `gh api user --include` (github.py:175-177)
  - G2 `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` (github.py:180-198)
  - G3 `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/events -F per_page=100 -F page=<P> --jq <EVENTS_JQ>` (github.py:218-220, 201-215); G3' same, reserved
  - G4 `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>/comments -F per_page=100 -F page=<P> --jq <MARKER_JQ>` (github.py:223-225)
  - G5 `gh api graphql -f query=<EDITS_QUERY> -F number=<N> [-f after=<cursor>]` (github.py:242-244, 228-239)
  - G6 `gh api graphql -f query=<PROJECT_ITEMS_QUERY> -F number=<N> [-f after=<cursor>]` (github.py:247-249); G6' same, reserved
  - G7 `gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N> --jq <REREAD_JQ>` (github.py:252-262)
  - Non-`gh` reads in this area: `git -C <worktree> remote get-url origin` (launch.py:244); `<orca> skills list --json` (launch.py:200).

### (d) Triggers
- `once` (the cycle that makes every call above): no trigger found in snapshot. It runs only when a person or an external scheduler runs `superclaude issue-watch once` (click group registered at `src/superclaude/cli/main.py:577-579`; docstring "Run `once` from a timer", cli.py:98). Evidence of absence: Grep `crontab|cron\b|systemd|launchd|\.timer|schedule` (case-insensitive) over `P` returns no match; Bash `grep -rIl 'issue-watch\|issue_watch'` over `.github`, `.claude`, `plugins`, `scripts`, `Makefile`, `pyproject.toml`, `package.json` returns nothing; Grep over `src` (hidden dirs not applicable) finds the string only in `cli/issue_watch/*.py`, `cli/main.py`, `skills/agent-work-report/scripts/common.py:22,25` (reads the file `~/.config/superclaude/issue-watch.json`, key `orchestrator_repo`, not the store), `skills/agent-work-report/SKILL.md:14` and `CHANGELOG.md:9`. The cron entry `"0 */5 * * * *"` is follow-up FU-2, deferred until after FU-1 and the shadow run (issue-watcher.md:861; issue-watcher-setup.md:676) [CODE-VERIFIED absence; a six-field cron string is not validated by any code].
- `init-state`, `status`, `check-config`, `reset`: operator-run only; same registration. `status` reports healthy only when the last completed cycle is under 900 s old (`HEALTH_AGE_S`, cycle.py:45, 1327), which presumes a timer exists.
- The Orca launch is triggered by `_launch` (cycle.py:1099) only for the first candidate that passes every check in a non-dry real cycle.
- `reset` T-13 and the DISABLED file are operator-triggered.

### (e) State stores (files and directories written or read in this area)
| Path pattern | Writer | Readers | Format | Mode |
|---|---|---|---|---|
| `${XDG_STATE_HOME:-~/.local/state}/superclaude/issue-watch/` (default `state_dir`, cycle.py:187-192; config key `state_dir` overrides) | `init_state` | all verbs | directory | 0700 |
| `<state_dir>/dispatch.json` | `FileStore.save` (init-state, once, reset) | `FileStore.load`, `_read_store_doc` | JSON, sorted keys, indent 2, ASCII, trailing newline; 7 top-level keys; 17-field entries | 0600 |
| `<state_dir>/lock` | `init_state` (creates; empty) | `FileStore.lock` (flock only) | empty regular file | 0600, owner must equal euid |
| `<state_dir>/DISABLED` | operator | `FileStore.disabled`, `disabled_since` | existence (any content, dangling symlink counts) | operator's |
| `<state_dir>/dry-run.json` | `save_dry_run` | `load_dry_run` | JSON `{schema_version, considered, shadow_launches}` | 0600 |
| `<state_dir>/dispatch.json.<random>.tmp` | `write_prepared_bytes` | nobody | transient (mkstemp) | owner-only default |
| `<state_dir>/audit.jsonl*` | other area (`audit.AuditLog`) | other area | JSON lines | 0600 |
| `<config.worktree>` (an existing git checkout) | not written by this area; used as `--worktree path:` and `cwd` | `git -C` read, Orca launch | directory | n/a |
No other file is written or read by github.py, launch.py or runner.py. The launched session's own files are not in this area.

### (f) Gates (exact condition, closed-vocabulary word, exit code; exit codes from `audit.REASON_TABLE`)
| Gate | Condition | Word | Exit | Evidence |
|---|---|---|---|---|
| enabled switch | `not config.enabled and not dry_run` | `not_enabled` | 0 | cycle.py:685-686; audit.py:61 |
| kill switch at start | `state_dir/DISABLED` exists (inside the lock) | `disabled` | 0 | cycle.py:712-713; record.py:421-423; audit.py:59 |
| kill switch before launch | `DISABLED` appears after the revalidation | `disabled_mid_cycle` | 0 | cycle.py:1063-1064; audit.py:60 |
| single-run lock | non-blocking `flock` held by another process, or lock path replaced after locking | `lock_held` | 75 | record.py:403-414; audit.py:54 |
| lock file defects | missing / symlink, directory, wrong owner | `lock_missing` / `lock_invalid` | 6 | record.py:394-401; audit.py:38-39 |
| store defects | missing file / unreadable, invalid or wrong-version file | `store_missing` / `store_invalid` | 6 | record.py:357-366; audit.py:36-37 |
| store write failure | `OSError` on save | `state_dir_unwritable` | 6 | cycle.py:601-605, 1125-1126; audit.py:40 |
| origin guard | `git remote get-url origin` fails or is not `ironbellyorg/ironclaude` (case-insensitive) | `origin_mismatch` | 2 | launch.py:233-251; cycle.py:721-722, 1074-1075; audit.py:32 |
| Orca probe | no `_ORCA_CLIS` binary lists topic `orca-cli` | `orca_not_found` | 2 | launch.py:163-203; cycle.py:1048-1052; audit.py:33 |
| call budget | per-issue non-reserved calls reach 32; reserved calls reach 35 (3 reserved for the re-read) | `budget_exhausted` (skip) | 0 | github.py:46, 49, 448-454; audit.py:79 |
| cycle deadline | fewer than 5 s left before a gh, git or probe call; launch cut-off after 120 s of 240 s | `gh_timeout` when a shared call or the origin check cannot start (exit 3); `budget_exhausted` (skip) per issue | 3 / 0 | cycle.py:40-43, 418-431, 716-720, 1069-1079; audit.py:44, 79 |
| rate limit | G1 or other `gh` rate-limited; wait stored in `next_permitted_at` | `rate_limited` (header wait 1..3600 s) / `rate_limit_clamped` (3600 s) | 5 | github.py:418-431; cycle.py:663-668, 748-750, 757-761; audit.py:51-52 |
| discovery bound | `gh issue list` returns 100 or more / a repeated number | `truncated` / `discovery_duplicate` | 4 | github.py:486, 823-830; audit.py:48-49 |
| project scope | `scope_missing` kind on any per-issue read | `project_read_failed` | 3 | cycle.py:842-843, 971-972; audit.py:46 |
| day cap | `record.day_cap_count` plus dry-run shadow launches in the last 24 h reaches `DAY_CAP = 6`; checked in `_examine` and again in `_launch` | `day_cap` (skip) | 0 | cycle.py:36, 867-876, 936-937, 1061-1062; record.py:699-703; audit.py:78 |
| backoff | `failed` entry updated less than 10 min ago or attempts >= 3 | `in_backoff` (skip) | 0 | record.py:528-535; cycle.py:934-935; audit.py:77 |
| at-most-once launch | entry state `pending` or `claimed` (or launched/unknown/abandoned without a marker hit) | `already_dispatched` (skip) | 0 | cycle.py:920-931; audit.py:76 |
| one launch step per cycle | any candidate that reaches `_launch` ends the loop | none (no word) | n/a | cycle.py:1028, 833-834 |
| candidate cap | at most 10 examined per cycle | none | n/a | cycle.py:34, 736 |
| prompt guard | `build_claim_prompt` raises (non-int or out of range) | `prompt_invalid` (entry `failed`) | 7 | launch.py:84-92; cycle.py:1053-1056; audit.py:84 |
| re-validation | G7/G3'/G6' re-read fails (transient) / fails (other) | `revalidation_transient` (entry `failed`, exit 7) / `revalidation_failed` (skip, 0) | 7 / 0 | cycle.py:979-1016, 1057-1060; audit.py:80, 85 |
| attempts | third pre-pending failure | `attempts_exhausted` (entry `abandoned`) | 0 | record.py:514-524; audit.py:86 |
| launch outcome | spawn failure / reply lost or malformed / ok | `spawn_error` (7, `abandoned`) / `launch_unknown` (7, `unknown`) / `launched` (0) | 7 / 7 / 0 | launch.py:326-349; cycle.py:1101-1112; audit.py:87-91 |
| crash recovery | `pending` found at cycle start / `launched` lease expired | `pending_orphan` / `claim_not_observed` (entry `abandoned`) | 0 | record.py:627-651; audit.py:89-90 |
| operator reset | `reset N --forfeit-guarantee` on a state other than `abandoned`/`unknown`, or missing | `reset_refused` (warning) | 2 | record.py:706-715; cli.py:245-248; audit.py:99 |
| unexpected exception | any `Exception` out of `run_cycle` in `once` | `cycle_crashed` | 1 | cli.py:123-129; audit.py:57 |
| origin of the Orca binary | candidate path must be absolute | (skipped, no word) | n/a | launch.py:195 |
Hard-coded safety limits of the launch: pipeline `none` (launch.py:33, 92), agent `claude` (28), terminal surface (launch.py:111-112), no permission flag (12-element argv), operation id pattern `^[A-Za-z0-9._:-]{1,128}$` (36).

### Integration and extension points (how a developer would extend this area)
- New `gh` call: add one `argv_*` builder in github.py that validates every caller value through `_issue_arg`/`_page_arg`/`_cursor_args`/`_trigger_arg`/`_login_arg`, use `--method GET` for REST paths, call it through `_call` (so the 5 s floor and `CallBudget` apply), classify with `classify`, add a typed read returning `Read`, and give its failures a name already in `audit.REASON_TABLE` (the table is closed; `audit.py:26-102`). `test_github.py` writes every expected argv out literally (Part A), so a new builder needs a new literal test; `test_github.py` also pins `CALL_CAP`/`RESERVED_CALLS`/`PAGE_CAP` values.
- New dispatch state: add the word to `ENTRY_STATES` (record.py:34), add a pure transition function, extend the pair table in `test_record.py` (`the_pair_table_covers_every_state_and_trigger_once`), and add any new `last_reason` to `audit.REASON_TABLE` (pinned by `df42_...` tests). Changing the entry fields needs a `MIGRATIONS` step (record.py:247) because `validate` demands the exact key set.
- New launch field or flag: change `launch_argv` (launch.py:95-116) and update the literal-twelve-element test; `PROMPT_PATTERN` (launch.py:33) must change together with `build_claim_prompt` (84-92).
- No new module may import `subprocess`; commands go through `Runner.run` (runner.py:41-45).

### Key Takeaways (deliverables)
- The test pins are strong on argv, constants, state transitions, crash safety and the lock; they are fixture-based, so they prove self-consistency with assumed replies, not agreement with real `gh` or Orca output.
- Every gate fails closed with a closed-vocabulary word and a fixed exit code; only a small set of words is exit 0 skip/entry.

## Gaps and Questions

1. [UNVERIFIED] Real Orca launch reply: `OPERATION_ID_PATHS` (launch.py:42-45) and `OP_UNKNOWN_TEXT` (launch.py:47) are labelled `[PROPOSAL, UNVERIFIED]` / "C16, UNVERIFIED" in the source; the success and unknown fixtures are assumed (`_assumed_shape: true`); the live-test record does not exist. Open question for the owner: what does `orca agent launch ... --json` print on success and on a lost reply?
2. [UNVERIFIED] Real `gh` reply shapes and error strings: GraphQL `EDITS_QUERY` and `PROJECT_ITEMS_QUERY` (github.py:71-72), `_CURSOR_RE` alphabet (125-126), `GH_ERROR_SIGNS` (267), `fieldValueByName` shape (768), the `--include` header layout (`_split_include` docstring 293, "shape unverified"). All fixtures assumed (section 6).
3. [UNVERIFIED] Whether `enabled` is true or false in the owner's real configuration file: the snapshot has no config; the default is False (cycle.py:228) and the design says it ships false (issue-watcher.md:3, doc status line). Also [UNVERIFIED]: whether anything outside the snapshot (an external cron, a person) runs `once`; "no trigger found in snapshot".
4. [UNVERIFIED] Whether `<orca> skills list --json` is side-effect free: the design says it reads bundled guide metadata locally without contacting the Orca runtime (issue-watcher.md:623, quoting Orca 1.4.245 help); not verifiable from the snapshot.
5. [UNVERIFIED] The claim that the launched session behaves as the prompt says (runs `/sc:issue --claim N --pipeline none`, writes the claim marker, does not create a worktree) are outside this area (research 04); this area only builds the command.
6. [UNVERIFIED] Tests were not run in this research. The pin descriptions are from reading test names, headers and selected bodies, not from a pytest run.
7. Open question: `LaunchOutcome.detail` (8 values) is set but never read or recorded by the cycle (Grep `\.detail\b` over `src`); is it intended for the audit line or for status? (No decision recorded in the snapshot.)
8. Open question: `launch_login` and `launch_account_id` are written into each entry and validated but have no reader in `src` (Grep result above); is a later consumer planned? No decision found in snapshot.
9. Open question: an orphan `dispatch.json.<random>.tmp` after a hard crash is ignored by design (issue-watcher.md C2 row, around line 535) and no code removes it; accumulation is unbounded in principle (one per crash).
10. Open question: `status` prints the retry argv with the bare name `orca-ide` or `orca` (`_retry_orca`, cycle.py:1262-1267), not the absolute path the real launch used (launch.py:193-203); the operator command depends on `PATH`.
11. [CODE-CONTRADICTED] `docs/designs/orchestrator.md:368`: `MAX_LAUNCHES_PER_CYCLE` shown as `(35)`; code `cycle.py:35` is `MAX_LAUNCHES_PER_CYCLE = 1` (and has no reader).
12. [UNVERIFIED] `docs/designs/orchestrator.md:115, 358`: `dispatch.json` holds "wakes sent and acknowledged, each entry with the orchestrator it was routed to"; no such field exists in the 17-field entry (record.py:69-88) and no code implements it.
13. [CODE-CONTRADICTED] `docs/designs/issue-watcher.md:621`: the Orca probe result is cached "per cycle, in the `OrcaLauncher` instance"; code caches nothing (launch.py:6; `find_orca` docstring 177; `OrcaLauncher.__init__` 355-356 stores only the runner).
14. [CODE-CONTRADICTED] `docs/designs/issue-watcher-setup.md:616-619`: the owner capture-sheet launch commands use `--prompt '/sc:issue --claim <test issue>'`; the code prompt is `/sc:issue --claim <N> --pipeline none` (launch.py:92). The same setup doc elsewhere mentions `pipeline none` (grep hits at lines 170 and 575), so the document is internally inconsistent.
15. [CODE-VERIFIED, code stricter] `docs/designs/issue-watcher.md:640` says the operation id is "a non-empty `str`"; code requires `^[A-Za-z0-9._:-]{1,128}$` (launch.py:36, 287-289), so an id with other characters becomes `unknown`, detail `operation_id_invalid` (launch.py:347-348).
16. [CODE-VERIFIED, table incomplete] `docs/designs/issue-watcher.md:485` lists T-1 "from (none)" only; `record.fail` also runs from `failed` (record.py:511) and bumps `attempts` (pinned by `df43_fail_on_a_failed_entry_counts_up_one_two_three_then_abandons__nfr005`).
17. [CODE-VERIFIED, nuance] `docs/designs/issue-watcher.md:448` "A migrated store is saved under the lock before any other step": the save happens in `_load` (cycle.py:746-747) after the DISABLED check (712-714) and before the login read; real cycles only.
18. [STALE] `tests/issue_watch/test_find_orca_parity.py:13-18` cites `install_user_setup.py:216-219` for the original's `topics` handling; `_find_orca` is now at install_user_setup.py:247-270 (`.get("topics", [])` inside the `try` at 265; the `any(...)` iteration, which raises for non-dict elements, at 268 outside it). The behaviour the test pins is unchanged; only the line numbers drifted.
19. Not read (outside this area, cited only for call sites): `cycle.py` lines 60-222 (config constants and loader), 243-355, 440-527 and 1336-1406 (SLO reducer body); `predicates.py` bodies; `audit.py` beyond lines 24-106; `conftest.py` (only the fixture-load lines found by grep); the bodies of `test_github.py`, `test_launch.py`, `test_record.py` beyond the names, section headers and the lines quoted above.

## Stale Documentation Found

| Marker | Where | Claim | Code truth |
|---|---|---|---|
| **[STALE DOC]** | `docs/designs/issue-watcher.md:621` | Orca probe result cached per cycle in `OrcaLauncher` | launch.py:6 "caches nothing"; `find_orca` runs again per call (launch.py:163-203) |
| **[STALE DOC]** | `docs/designs/issue-watcher-setup.md:616-619` | launch command prompt is `/sc:issue --claim <test issue>` | launch.py:92 `... --pipeline none` |
| **[STALE DOC]** | `docs/designs/orchestrator.md:368` | `MAX_LAUNCHES_PER_CYCLE` value 35 | cycle.py:35 value 1; no reader |
| **[STALE DOC]** | `docs/designs/orchestrator.md:115, 358` | `dispatch.json` carries wakes and orchestrator routing | record.py:69-88 has no such field; design itself says no implementation exists (orchestrator.md:3) |
| **[STALE DOC]** | `tests/issue_watch/test_find_orca_parity.py:13-18` | original `_find_orca` reads `topics` at install_user_setup.py:216-219 | now install_user_setup.py:265 and 268 |
| minor | `docs/designs/issue-watcher.md:485` | T-1 only from "(none)" | `fail` also from `failed` (record.py:511) |
| minor | `docs/designs/issue-watcher.md:640` | op id "non-empty str" | pattern `^[A-Za-z0-9._:-]{1,128}$` |
| consistent (not stale) | `docs/designs/issue-watcher.md` sections 7.1-7.6 and 8.4 argv/constants | file table, 17 fields, six states, T-1..T-13 function names, `MAX_ATTEMPTS` 3, backoff 10 min, lease 60 min, day cap 6, 12-element argv, `cwd=worktree`, timeouts 20/10/10/120/240 | all [CODE-VERIFIED] at record.py:34-36, 69-88, 434-448, launch.py:95-116, 358-370, cycle.py:34-47 |
| consistent | `docs/designs/issue-watcher.md:3` status line "never run live; `enabled` ships false; no schedule installed" | | [CODE-VERIFIED] for `enabled` default (cycle.py:228) and no schedule artefact (grep); "never run live" and PRs #447/#448 are not verifiable from files in the snapshot beyond the live-test record's absence |
| consistent | `docs/designs/issue-watcher-setup.md:133` "never writes to GitHub at all" | | [CODE-VERIFIED] for the watcher code (section 7(c)); the launched session is the writer |

## Defect Candidates and Not-Built Capabilities

(Per the C8 adaptation: no remediation tasks were created and nothing was written outside the task folder; these rows are listed for the owner to decide.)

| Id | Type | Capability | Declaring doc (path:line) | Code evidence it is unwired or absent | Decision recorded that it is out of scope? |
|---|---|---|---|---|---|
| D-1 | DEFECT CANDIDATE (dead code) | `record.disabled_present(state_dir)` as a component of `record.py` | `docs/designs/issue-watcher.md:228` lists it in the `record.py` module row | Defined at record.py:748-750; Grep `disabled_present` over `/home/coder/.cache/ic-snap-20261120/master` `*.py` hits only record.py:748 and `tests/issue_watch/test_record.py:861, 870`; the cycle uses `FileStore.disabled()` (cycle.py:712, 1063) instead | No decision found. Low severity: same body as `FileStore.disabled`, pinned only by tests |
| D-2 | DEFECT CANDIDATE (dead constant) | per-cycle launch cap constant `MAX_LAUNCHES_PER_CYCLE = 1` | `docs/designs/orchestrator.md:368` (names it, with the wrong value 35); `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:1740` already says it is "referenced nowhere else in src" | Grep `MAX_LAUNCHES_PER_CYCLE` over `*.py` in the snapshot returns only cycle.py:35. The one-launch rule is enforced by `c.launching`/`self.halt` (cycle.py:1028, 833-834), not by the constant | No decision found. Low severity (behaviour is right; the constant is misleading) |
| D-3 | DEFECT CANDIDATE (dead field) | `LaunchOutcome.detail` (8-value vocabulary `LAUNCH_DETAILS`) | design 8.4 outcome table (issue-watcher.md:634-641) describes outcomes; the 8 detail words are code-only (launch.py:58-70) | Grep `\.detail\b` over `src`: no read of `LaunchOutcome.detail` (only `ConfigError.detail`); `cycle._launch` uses `outcome.kind` and `outcome.operation_id` only (cycle.py:1101-1112); nothing records it in the store or the audit line | No decision found. Low severity: the reason a launch became `unknown` (`timeout`, `exit_nonzero`, `non_json`, `no_operation_id`, `operation_id_invalid`, `op_unknown`) is lost; the audit line only says `launch_unknown` |
| D-4 | DEFECT CANDIDATE (write-only fields) | `launch_login`, `launch_account_id` in each entry | `docs/designs/issue-watcher.md:437-438` (`pending` write, never mutable) | Only written (`mark_pending` record.py:548-568) and validated (record.py:180, 185); Grep `launch_login|launch_account_id` over `src` finds no other reader | No decision found. Informational |
| N-1 | NOT BUILT | Automatic retry of an `unknown` launch with `--retry-launch` | `docs/designs/issue-watcher.md:867` (FU-8), `docs/designs/issue-watcher-setup.md:682` | `retry_argv` (launch.py:119-132) has one production caller, `status_report` (cycle.py:1308-1312), which only prints the argv for an operator; nothing runs it (Grep `retry_argv` over `src`) | YES, deferred by decision: FU-8 "after FU-1 confirms the C20 argv" (issue-watcher.md:867; setup:682) |
| N-2 | NOT BUILT | A scheduler that runs `issue-watch once` (cron entry FU-2) | `docs/designs/issue-watcher.md:861`, `issue-watcher-setup.md:676`; cli.py:98 "Run `once` from a timer" | No scheduler, timer unit or installer in `P`, `.github`, `.claude`, `plugins`, `scripts`, `Makefile`, `pyproject.toml`, `package.json` (greps in section 7(d)) | YES for ordering: the design gates it behind FU-1 and the shadow run (issue-watcher.md:33, 861; setup:588, 676). That decision does not say it is out of scope, only that it comes later |
| N-3 | NOT BUILT | The live-test record and replacement of every `_assumed_shape` fixture (FU-1) | `docs/designs/issue-watcher.md:33, 775, 860`; `issue-watcher-setup.md:272, 586-625, 675` | Glob `docs/designs/issue-watcher*` returns two files; `issue-watcher-live-test.md` absent; all 19 fixtures `_assumed_shape: true`, count pinned by test_github.py:575-583 | YES, assigned to the owner: "You write that file; the implementation does not" (setup:272, 625; issue-watcher.md:33, 775) |
| N-4 | NOT BUILT | `dispatch.json` as the store for orchestrator wake routing ("wakes sent and acknowledged ... the orchestrator it was routed to") and a poll `once --dry-run` that reports `would_wake` | `docs/designs/orchestrator.md:115, 358, 368`; status line orchestrator.md:3 "holds no implementation code" | Glob `**/*orchestrator*` under `src` returns only `cli/eval/orchestrator.py`, `cli/audit/tool_orchestrator.py`, `agents/debate-orchestrator.md` (none implement it); Grep `would_wake|orchestrators\.json|"woken"|\.orchestrator/` over `src` returns one hit in `skills/agent-work-report/SKILL.md` only (not the store); record.py entry has no wake or orchestrator field | The design is explicitly a not-yet-implemented design ("The build starts from this text", orchestrator.md:3); no snapshot file decides it is out of scope. PR 686 / Clay design is out of scope of this reference per the task notes |
| N-5 | NOT BUILT | SLO numbers as a command | `docs/designs/issue-watcher-setup.md:455-478` ("It prints ..."), FU-10 (setup:684) | `cycle.slo_numbers` (cycle.py:1359) has no caller in `src` (Grep `slo_numbers` over `src`: definition only); `cli.py` has no `slo` string (Grep, case-insensitive); only an owner-run Python snippet (setup:467-475) calls it | Partly: FU-10 is a review step "after 7 days live" (setup:684); the snippet is the documented way, so it is deliberate, not unwired |
| N-6 | NOT BUILT | Automatic cleanup of orphan `dispatch.json.*.tmp` | issue-watcher.md C2 row (around line 535: "an orphaned tmp file is ignored") | No unlink of orphan temp files anywhere in `P` or `swarm/atomic.py` beyond the in-exception unlink (atomic.py:33-38) | YES: the design states the orphan is ignored (issue-watcher.md ~535) |
| N-7 | NOT BUILT (store growth bound) | A bound or pruning rule for finished entries | `issue-watcher-setup.md:685` (FU-11), issue-watcher.md:870 | No code removes `claimed`, `abandoned` or `launched` entries; only `reset_entry` removes `abandoned`/`unknown` (record.py:706-720) | YES: deferred as FU-11 "when the store is above 1 MiB" (setup:685) |

## Summary

This area contains the watcher's whole outside-world surface: seven read-only `gh` calls (all with the fork hard-coded, 35 per-issue calls of which 3 are reserved, 37 at most per cycle), one fixed 12-element `orca agent launch ... --prompt "/sc:issue --claim <N> --pipeline none" --json` that targets an operator-supplied existing worktree and creates none, a strictly validated `dispatch.json` (7 top-level keys, 17-field entries, six states, T-1..T-13) written write-ahead (pending saved before the launch) under a non-blocking flock with atomic replace, and a runner that is the only module importing `subprocess`. No code in this area writes to GitHub, and nothing in the snapshot triggers it: `enabled` defaults to false, there is no scheduler, and no reader of `dispatch.json` exists outside `issue_watch`. Every Orca and `gh` reply shape the code depends on is still assumed (19 `_assumed_shape` fixtures, no live-test record), and every gate fails closed with a closed-vocabulary word and fixed exit code. The owner should decide on four small dead items (D-1 to D-4) and note that automatic retry, the scheduler, the live-test record and the orchestrator wake routing are not built.

