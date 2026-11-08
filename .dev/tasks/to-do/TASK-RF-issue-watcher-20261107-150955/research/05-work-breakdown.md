# Research 05: Work breakdown for `superclaude issue-watch` (data flow, build order, test map, phases)

**Topic type:** Data Flow Tracer / work breakdown
**Scope:** `docs/designs/issue-watcher.md` (sections 1-18, all 936 lines read) and its driving spec `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (all 515 lines read: FR, NFR, definitions, section 7 dispatch record, section 8 deliverables and runbook)
**Status:** Complete
**Date:** 2026-11-07

Conventions used below. `D n.m` = design section n.m (line numbers in parentheses are lines of `docs/designs/issue-watcher.md`). `S n` = spec section n. "stated" = the design gives the name or signature literally; "derived" = the design fixes the data but not the name, so the task builder must choose (listed in Gaps). Nothing in this file repeats the Orca agent literal (design PF-034); it is the token after `--agent` at `.dev/brainstorms/20261107-064825-github-issue-watcher/seed-brief.md:64`.

Verified facts about the checkout while researching (read-only commands):
- `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` do not exist yet.
- `tests/__init__.py` and `tests/pr_submit/__init__.py` exist (C14 holds for the packages-with-init convention).
- `src/superclaude/cli/main.py` ends with the `reflect_group` import (with `# noqa: E402,I001  # intentional: deferred subcommand registration ...`) followed by `main.add_command(reflect_group, name="reflect")`, then `if __name__ == "__main__":`. The new two lines go between them in the same style.
- `.dev/brainstorms/20261107-064825-github-issue-watcher/` and `docs/designs/issue-watcher.md` are not in `git ls-files` (untracked or only staged). No test may read a `.dev/brainstorms/` path: it will not exist in CI.
- `property_based` and `thread_safety` and `slow` markers exist in `pyproject.toml` (lines ~117-140); `--strict-markers` is on.

---

## 1. Dependency-ordered build sequence

Order is fixed by the import graph in D 5.3 (lines 229-242): leaves first (`runner`, `predicates`, `audit`), then modules that import only leaves (`github`, `record`, `launch`), then `cycle`, `cli`, `main.py`.

| Order | Item | Imports from package | Imports from superclaude | Realises (main) |
|---|---|---|---|---|
| 0 | `src/.../issue_watch/__init__.py`, `tests/issue_watch/__init__.py`, conftest skeleton | none | none | C14, NFR-014 |
| 1 | `runner.py` | none | none | NFR-004, T6, T11 |
| 2 | `predicates.py` | none | none | FR-005..009, FR-008, FR-023 order, Section 3 |
| 3 | `audit.py` | none | none | FR-020, NFR-006 |
| 4 | `github.py` | runner, predicates | none | FR-002..007, FR-022, FR-028, NFR-002, NFR-003, NFR-009 |
| 5 | `record.py` | predicates (types only) | `superclaude.cli.swarm.atomic` (lazy) | FR-010, FR-017, FR-018, FR-024, NFR-005, NFR-011, Section 7 |
| 6 | `launch.py` | runner | `superclaude.cli.install_user_setup._ORCA_CLIS` only | FR-012, FR-013, FR-014, FR-025, NFR-001 |
| 7 | `cycle.py` | runner, github, predicates, record, launch, audit | none | FR-001, FR-011, FR-016, FR-019, FR-021, FR-022, FR-027, FR-029, NFR-007..010, NFR-013 |
| 8 | `cli.py` | cycle, record, audit, launch, runner | `click` | FR-015, FR-018, FR-021, FR-026 |
| 9 | `main.py` two lines | cli | n/a | FR-026 registration |
| 10 | cross-cutting tests, stubs, setup runbook, gates | | | all |

### 1.0 M0: package markers and test skeleton

| File | Content | Notes |
|---|---|---|
| `src/superclaude/cli/issue_watch/__init__.py` | Package marker, exports nothing (D 11 line 751) | Docstring only |
| `tests/issue_watch/__init__.py` | Empty marker | Required: `tests/cli_portify/test_cli.py` exists, two rootless `test_cli.py` collide (C14, line 95) |
| `tests/issue_watch/conftest.py` | Built incrementally: see section 3 | FakeClock first, FakeRunner after `runner.py`, FakeLauncher after `launch.py`, CrashingStore and `tmp_state` after `record.py` |

### 1.1 M1: `runner.py` (order 1)

Public API (stated, D 5.4 lines 254-265; D 5.2 line 218):
- `@dataclass(frozen=True) class CommandResult`: `argv: tuple[str, ...]`, `returncode: int | None` (None when timed out or spawn error), `stdout: str`, `stderr: str` (at most 500 bytes), `timed_out: bool`, `spawn_error: str | None` (OSError class name, never its message), `duration_s: float`.
- `class Runner(Protocol)`: `run(self, argv: list[str], timeout: float) -> CommandResult`.
- `class SubprocessRunner`: `run(argv, timeout)`; raises `TypeError` on a `str` argv; calls `subprocess.run(list, shell=False, capture_output=True, text=True, timeout=t, stdin=subprocess.DEVNULL)`; truncates stderr to 500 bytes (T11); maps `TimeoutExpired` to `timed_out=True` and `OSError` to `spawn_error=<class name>`.
- Constant: stderr cap 500 bytes (D 14 line 822).

Realises: NFR-004, T6, T11 (stderr cap), supports NFR-002 (single choke point for every argv).
May import: nothing from `superclaude`; standard library only.
Tests: `test_runner.py` (str argv TypeError; list argv passes `shell=False` literal; `stdin` is DEVNULL; stderr over 500 bytes truncated; TimeoutExpired maps to `timed_out=True, returncode=None`; `FileNotFoundError`/`PermissionError` map to `spawn_error` class name; no message text kept); `test_no_shell.py` (AST).
Traps: the Protocol has no `cwd` parameter but D 8.4 (line 625) says "the runner is called with `cwd=worktree`". See Gap G-01. Truncate by bytes, not characters (`encode`/`decode(errors="replace")`). Never include `spawn_error` message (path text could leak).

### 1.2 M2: `predicates.py` (order 2)

Public API (names stated D 5.2 line 220; fields derived from the G-projections D 8.1):
- Frozen dataclasses (names stated): `Login`, `DiscoveredIssue`, `LabelEvent`, `IssueSnapshot`, `ProjectItem`, `MarkerEvidence`, `EditEvidence`; plus return type `ApprovalResult` (stated by name in `approval_of(events, ...) -> ApprovalResult`).
- Derived fields: `Login(login: str, account_id: int, server_date: datetime | None)`; `DiscoveredIssue(number: int, labels: tuple[str, ...], assignees: tuple[str, ...], state: str)` (G2 projection); `LabelEvent(id: int, event: str, label: str | None, actor_id: int | None, actor_login: str | None, actor_type: str | None, created_at: datetime)` (EVENTS_JQ, line 545); `IssueSnapshot(number, state, labels, assignees)` (REREAD_JQ, line 549); `ProjectItem(is_archived: bool, project_id: str, status_name: str | None)` (G6 line 548); `MarkerEvidence(id: int, login: str, created_at, updated_at, marker: bool)` (MARKER_JQ line 546); `EditEvidence(issue_created_at, issue_last_edited_at, comments: tuple[(database_id, author_login, created_at, last_edited_at)])` (G5 line 547); `ApprovalResult(approved: bool, reason: str | None, approver_id: int | None, approval_event_id: int | None, approved_at: datetime | None)`.
- Constant `CLAIM_MARKER = "<!-- sc:issue:claim -->"` (stated D 5.2; marker text from MARKER_JQ line 546 and `refs/claim.md:29`).
- Functions (stated): `is_intended_owner(assignees, own_login)` returning true or a skip reason (`unassigned`/`assigned_other`, FR-008); `approval_of(events, ...) -> ApprovalResult` (T2, T3; checks (a)-(e) of S 3 "Approved by a human"); `unchanged_since(approval, edits, events)` (T4, line 660); `eligibility_order(...)` (FR-023 ordering, D 6.2 step 9). Unnamed but required (derived): project check (S 3 "In a Project and in Backlog": exactly one non-archived item whose `project_id` equals config, `Status` == `Backlog`), marker-window check (`marker_time >= pending_at - 300 s`, else after current `approved_at`, D 7.5 line 502).
- Every time is a parameter; no clock, no I/O (D 5.2).

Realises: FR-005, FR-006, FR-007 (decision part), FR-008, FR-009 (predicate part), FR-023 (order), Section 3 definitions, T2, T3, T4, OD-3.
May import: nothing from `superclaude`.
Tests: `test_predicates.py` (see section 2).
Traps: `type(v) is int` (bool is an int subclass); tie rule (equal `created_at` seconds between opposing labeled/unlabeled or approval/trigger events gives `events_incomplete`, S 3 line 92); order key is (`created_at`, `id`); "latest `labeled` event" not "any"; a later `unlabeled` voids; reasons returned must be members of the closed reason table (strings, validated by `test_audit` and by a predicates-reasons-subset-of-REASONS test, since `predicates` cannot import `audit`).

### 1.3 M3: `audit.py` (order 3)

Public API (stated D 5.2 line 223; D 10.1 lines 697-722):
- `REASONS: frozenset[str]` equal to the 52 reason names of S 8 (verified count 52 by extracting backticked names from spec lines 334-358); D 5.2 says "with kind and exit per reason", which a frozenset cannot carry: companion mapping needed (name not stated, Gap G-06).
- `class AuditLog`: `append(line)` (one `os.write` on an `O_WRONLY | O_APPEND | O_CREAT` fd, mode 0600, keys sorted, `ensure_ascii=True`); `rotate_if_needed()` (only with the lock held; at 5 MiB shift `.3`->`.4`, `.2`->`.3`, `.1`->`.2`, current->`.1`, then directory fsync).
- `stderr_fallback(...)`: D 5.2 writes `stderr_fallback(line)`, D 10.1 writes `stderr_fallback(reason, exit)` (Gap G-05); one JSON line with `kind, ts, host, exit, reason` only.
- Line builders (stated): `cycle_line(...)`, `decision_line(...)`, `warning_line(...)`; D 10.1 also names `audit.line(...)` that raises `ValueError` on a reason outside `REASONS`.
- Line schema (D 10.1 table): cycle line keys `kind, ts, host, login, cycle_id, dry_run, exit, reason, gh_calls, duration_ms` (+ optional `discovery_count`, `clock_skew_s`); decision line `kind, ts, host, login, cycle_id, dry_run, reason, issue, state?, approver_id, approval_event_id, approved_at, note?`; warning line `kind, ts, host, login, cycle_id, dry_run, reason, issue?, discovery_count?, clock_skew_s?`. `rate_remaining`, titles, bodies, label names, stderr text are never keys.

Realises: FR-020, NFR-006, T7, T11.
May import: nothing from `superclaude`.
Tests: `test_audit.py` (REASONS equals the spec table; unknown reason raises `ValueError`; builders accept typed scalars only; forbidden keys never emitted; one `os.write` per line; `0600` mode; rotation shifts four files and keeps 4; rotation not called on the exit-75 path; stderr fallback keys), `test_no_text.py` (PWNED-TITLE).
Traps: the module must not contain a string literal equal to an `ID_PATTERNS` body (arch lint, C9); `re-approved` is a table entry of kind "decision note" (carry it in `note`; decide whether it is also in `REASONS`, Gap G-06); `reset` audit lines have no defined reason (Gap G-04).

### 1.4 M4: `github.py` (order 4)

Public API (stated D 5.2 line 219, D 8.1-8.3, D 11 line 753):
- Constants: `REPO = "IronbellyOrg/IronClaude"`; `EVENTS_JQ`, `MARKER_JQ` (must be built from `predicates.CLAIM_MARKER`, not retyped), `REREAD_JQ`, `EDITS_QUERY`, `PROJECT_ITEMS_QUERY` (GraphQL constants with `repository(owner:"IronbellyOrg", name:"IronClaude")` literal and no word `mutation`); one table constant of stderr substrings and GraphQL error types (line 590); page cap 5; call cap 35 with 3 reserved.
- Argv builders G1..G7 (stated forms, D 8.1 lines 543-550):
  - G1 `["gh","api","user","--include"]`
  - G2 `["gh","issue","list","--repo",R,"--state","open","--label",<trigger>,"--assignee",<login>,"--json","number,labels,assignees,state","-L","100"]`
  - G3 `["gh","api","--method","GET","repos/R/issues/N/events","-F","per_page=100","-F","page=P","--jq",EVENTS_JQ]`
  - G4 `... /comments ... --jq MARKER_JQ`
  - G5 `["gh","api","graphql","-f","query="+EDITS_QUERY,"-F","number=N", ("-f","after=<cursor>")]`
  - G6 same shape with `PROJECT_ITEMS_QUERY`
  - G7 `["gh","api","--method","GET","repos/R/issues/N","--jq",REREAD_JQ]`
  - G3', G6' = G3, G6 for the FR-011 re-read (reserved slots).
- `classify(result: CommandResult) -> Reply` with kinds `ok, timeout, non_json, auth_failed, scope_missing, rate_limited, transient, failed` (table D 8.2 lines 579-588).
- `retry_after(result) -> int | None`; rate-limit time rule D 8.3 (Retry-After 0<s<=3600 -> now+s; reset epoch within 3600 s -> that instant; else now+3600 with `rate_limit_clamped`).
- `CallBudget` (35 cap, 3 reserved; counts every page).
- Typed reads (names stated only for `user()` and `discover(login)`, D 6.2 lines 348, 351; others derived): events, comments/marker, edits, project items, re-read.
- Validation: `discover` produces `number` with `type(v) is int and 1 <= v <= 999_999_999` (D 9.3 line 693); 100 or more results -> `truncated`; repeated number -> `discovery_duplicate`.
- Paging rule (D 8.2 lines 564-575): page < 100 ends read; page = 100 fetches P+1; P > 5 -> `events_incomplete` (events) or marker unknown (never counts as claimed); repeated `id` -> incomplete; non-array/missing field/non-positive-int id -> `events_unreadable`; budget would be exceeded -> `budget_exhausted` (candidate not stamped); GraphQL complete only when `hasNextPage` false, repeated `endCursor` or empty cursor with `hasNextPage` true is incomplete.
- G1 parse: status line, headers, blank line, JSON body; keep `.login`, `.id`, `Date` header, `Retry-After` header (UNVERIFIED shape, D 15 line 835).

Realises: FR-002, FR-003, FR-004, FR-005 (read part), FR-006, FR-007 (read part), FR-009 (read part), FR-011 (re-read argv), FR-022 (classification), FR-028 (retry_after), NFR-002, NFR-003, NFR-007, NFR-009, T5, T9.
May import: `runner`, `predicates`.
Tests: `test_github.py`: exact argv equality for G1..G7; every REST argv contains `--method GET`; GraphQL constants contain the literal repo and no `mutation`; no argv names `title`, `body`; `classify` table row per observation; `retry_after` rows; paging cases (99/100/101 items, repeated id, cap 5, budget exhausted mid-paging); G1 header parse from the `_assumed_shape` fixture; `discover` validation (bool, float, string, 0, 10**9 rejected).
Traps: C21 says `--method GET` is mandatory "on every G2 to G7 argv" and "a test rejects any `-F` argv without it" (line 102), but G2 (`gh issue list`) has no `-F` and G5/G6 are GraphQL POSTs that use `-F number=N` without `--method GET`. D 8.1 (line 554) and T9 correctly exempt G1 and `graphql`. Encode the D 8.1 rule (Gap G-08). `-F per_page=100` without `--method GET` would be a POST (NG-2). Do not use `fetch_rest`'s argv order or its 1000-page cap (C5).

### 1.5 M5: `record.py` (order 5)

Public API (stated D 5.2 line 221, D 5.4 lines 267-274, D 7):
- `Store(Protocol)`: `state_dir: Path`; `load() -> StoreDoc` (raises `StoreError(reason)`); `save(doc: StoreDoc) -> None` (atomic plus dir fsync); `lock() -> AbstractContextManager[None]` (raises `LockHeld` / `LockError(reason)`); `disabled() -> bool`; `disabled_since() -> datetime | None`.
- `FileStore(state_dir)`: save = `json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=True).encode() + b"\n"` -> `write_prepared_bytes(state_dir/"dispatch.json", data)` (imported lazily inside `save`, C18) -> `os.chmod(path, 0o600)` -> open dir `O_RDONLY | O_DIRECTORY`, `os.fsync`, close (D 7.6 line 509). Lock protocol steps 1-5 (D 7.6 lines 511-521): open `O_RDWR | O_NOFOLLOW | O_CLOEXEC`; `FileNotFoundError` -> 6 `lock_missing`; `ELOOP`/`IsADirectoryError` -> 6 `lock_invalid`; `fstat` must be regular and `st_uid == geteuid()`; `flock(LOCK_EX | LOCK_NB)`, `BlockingIOError` -> 75 `lock_held`; inode check `(st_dev, st_ino)` against `os.stat(lock, follow_symlinks=False)` and `st_nlink > 0` else 75.
- Dataclasses `Entry` (17 fields, D 7.2 lines 417-437: `issue, state, attempts, launches, operation_id, approver_id, approval_event_id, approved_at, launch_cwd, launch_login, launch_account_id, consumed_at, pending_at, created_at, updated_at, lease_expires_at, last_reason`) and `StoreDoc` (7 keys: `schema_version, created_at, next_permitted_at, last_completed_cycle_at, considered, consumed_log, entries`). All frozen (D 7.4 line 492: transitions return a new `StoreDoc`).
- Exceptions: `StoreError`, `LockHeld`, `LockError`, `TransitionError`.
- `validate(doc) -> StoreDoc` (raises `StoreError("store_invalid")`): exact key sets, types, `issue` equals key, `launches` in {0,1}, `launches == 1` implies `consumed_at` and `pending_at`, `state == "failed"` implies `launches == 0`, every time `Z`-suffixed aware UTC.
- `MIGRATIONS: dict[int, Callable[[dict], dict]]` (ships empty); `migrate(doc, migrations=...)` test seam.
- Transition functions (stated, D 7.4): `fail(doc, n, reason, now)` (includes T-3), `backoff_elapsed(entry, now)`, `mark_pending(doc, n, ctx, now)`, `mark_launched`, `mark_unknown`, `mark_spawn_error`, `sweep(store, now)` (T-8, T-9), `mark_claimed` (T-10, T-11, T-12), `reset_entry` (T-13). Helpers: `day_cap_count(store, now)`, `disabled_present(state_dir)`, `init_state(state_dir, now)`.
- `init_state`: `os.makedirs(mode=0o700)` then `os.chmod`; creates `dispatch.json` (0600) and `lock` (`O_CREAT | O_EXCL | O_NOFOLLOW`, 0600); `created_at` = now (the approval floor).
- Time windows (half-open): lease expired iff now >= `lease_expires_at`; backoff elapsed iff now >= `updated_at` + 10 min; day cap counts t with now-24h < t <= now; `consumed_log` pruning drops t <= now-24h (D 7.5).

Realises: FR-009 (transitions), FR-010, FR-014 (state half), FR-017, FR-018 (`disabled`), FR-019 (`dry-run.json` schema, D 7.2 line 446), FR-024, FR-026 (`reset`, `init-state`), NFR-005, NFR-010, NFR-011, T8.
May import: `predicates` (types only); `superclaude.cli.swarm.atomic`. Third-party: none.
Tests: `test_record.py`: one case per T-1..T-13 plus a table-driven "every other (state, trigger) pair raises `TransitionError`"; validation failures (truncated JSON, wrong types, missing key, `issue` != key, `launches` 2, `failed` with `launches` 1, naive time string); migration with a test-only v0 fixture; `save` byte-identical on resave (sorted keys); modes `0600`/`0700`; lock cases (missing, symlink, directory, foreign uid via monkeypatched `geteuid`, held, inode replaced after acquire); half-open boundary cases (lease, backoff, day cap, consumed_log pruning); `init_state` refuses an existing store; `disabled_since` uses mtime. `test_crash_injection.py`, `test_concurrency.py`.
Traps: (1) `fail` called on an entry already in `failed` (second and third pre-pending failure) is not a T-row from "(none)"; the "every other pair raises" table must allow (`failed`, prompt_invalid / revalidation_transient) so `attempts` can reach 3 (Gap G-09). (2) JSON object keys are decimal strings; the Python side must convert to int consistently. (3) `last_reason` must be "from the closed enum" (D 7.2 line 437) but `record` may not import `audit` (D 5.3 line 239): validate type only and test enum membership elsewhere (Gap G-07). (4) `sweep(store, now)` in D 5.2 versus "every function takes the document and `now`" (D 7.4 line 492), and `day_cap_count(store, now)` in D 5.2 versus `day_cap_count(doc, now)` in D 10.2 line 737 (Gap G-10). (5) `import fcntl` at module top breaks `import superclaude` on a platform without it, because `main.py` imports `cli.py` eagerly (the "lazy import" claim in D 5.3 line 244 is not true for the reflect-style registration); import `fcntl` inside `lock()`. (6) `os.O_NOFOLLOW` / `os.O_DIRECTORY` only at call time. (7) 3.10: `datetime.fromisoformat` does not accept a trailing `Z` (3.11+ does); parse with a strict regex and `strptime`, format with `strftime("%Y-%m-%dT%H:%M:%SZ")`.

### 1.6 M6: `launch.py` (order 6)

Public API (stated D 5.2 line 222, D 8.4, D 5.4 lines 276-285):
- `ORCA_AGENT` (module constant; value = the seed brief token; a unit test pins it; not configurable).
- `build_claim_prompt(n)`: accepts `int` not `bool` in 1..999999999, returns `f"/sc:issue --claim {n}"`; otherwise `ValueError` (FR-012).
- `launch_argv(orca, worktree, prompt) -> list[str]`: exactly 12 elements `[orca, "agent", "launch", "--agent", ORCA_AGENT, "--worktree", "path:" + worktree, "--surface", "terminal", "--prompt", prompt, "--json"]` (D 8.4 line 621).
- `find_orca(runner, which) -> str | None`: candidates `_ORCA_CLIS` imported (`install_user_setup.py:35`: `("orca-ide", "orca")`), `which` injected, argv `[<path>, "skills", "list", "--json"]`, timeout min(10, remaining), accept iff exit 0, stdout JSON object, `topics` list, some element a `dict` with `name == "orca-cli"`; reject non-dict elements (C19).
- `parse_origin(url)` mirrors `parse_origin_url` (`origin_repo.py:86-99`); `check_origin(runner, worktree, timeout)` runs `git -C <abs> remote get-url origin`, compares `owner/repo` case-insensitively with `ironbellyorg/ironclaude`.
- `Launcher(Protocol)`: `launch(orca, worktree: Path, prompt, timeout) -> LaunchOutcome`; `LaunchOutcome(kind: Literal["launched","unknown","spawn_error"], operation_id: str | None, detail: str)`; `OrcaLauncher(runner)` with per-cycle probe cache.
- `OPERATION_ID_PATHS`: tuple of candidate key paths, pinned by an `_assumed_shape` fixture (D 8.4 line 636); operation-id regex `^[A-Za-z0-9._:-]{1,128}$` (D 9.2 line 689; failing id stored as null and outcome `unknown`).
- Outcome mapping table D 8.4 lines 629-634.

Realises: FR-012, FR-013, FR-014 (outcome half), FR-025, NFR-001, T10, T17.
May import: `runner`; `superclaude.cli.install_user_setup` (`_ORCA_CLIS` only).
Tests: `test_launch.py`: prompt table (9, "9", True, 0, -1, 10**9, 9.0 -> only 9 valid); `launch_argv` equality and 12 elements and no extra flag (T10); `find_orca` cases (non-JSON, no `orca-cli` topic, non-dict element, first candidate rejected second accepted, none found); `parse_origin` table; `check_origin` (match, mismatch, timeout, non-zero); outcome mapping rows; `ORCA_AGENT` pin; operation-id regex; `test_find_orca_parity.py`; `test_origin_parity.py`.
Traps: runner called with `cwd=worktree` (Gap G-01); the original `_find_orca` raises on a non-dict topic and the parity test must exclude that input and pin the difference (C19); `parse_origin_url` regexes are case-sensitive on `github.com` (C3); the pin test for `ORCA_AGENT` must not read `.dev/brainstorms/...` (untracked, absent in CI); the status retry argv is rebuilt here from `launch_argv` plus `--retry-launch <id>` inserted before `--json` (D 10.2 line 741).

### 1.7 M7: `cycle.py` (order 7)

Public API (stated D 5.2 line 224, D 5.4, D 6, D 8.5, D 10.3):
- `Config` + `load_config(path) -> Config` (schema D 4.2 lines 127-137: `schema_version` (==1), `enabled` (default false), `labels.trigger` (default `issue-watch:trigger`), `labels.approval` (default `issue-watch:approved`, != trigger, <=50 chars, no control chars), `project_id` (`^PVT_[A-Za-z0-9_-]{1,64}$`), `owner_account_id` (int not bool, 1..10^20-1, optional), `worktree` (absolute existing dir), `approvers_file` (absolute), `state_dir` (default XDG path, absolute, network-FS deny-list)); unknown keys rejected (exit 2).
- `validate_approvers(path) -> frozenset[int]` (D 4.2 lines 143-149: `os.lstat`, `S_ISREG`, `st_uid == geteuid()`, `mode & (S_IWGRP|S_IWOTH) == 0`, line regex `^[1-9][0-9]{0,19}$`, `#`/blank ignored, other line invalid, at least one ID).
- `Clock(Protocol)`: `now() -> datetime` (tz-aware UTC), `monotonic() -> float`; `SystemClock`.
- `Deadline(clock, total=240)`: `remaining()`, `elapsed()`; 5 s floor for new `gh` calls, 120 s cutoff for launch (D 8.5).
- `Deps` frozen dataclass: `runner, store, launcher, clock, audit, config, which, host` (D 5.4 line 302; its owner module is not stated, Gap G-11: it must be `cycle.py` because `cli.build_deps` returns it and `cli` imports `cycle`).
- `run_cycle(deps: Deps, dry_run: bool) -> CycleResult` implementing D 6.2 steps 1-15 (CycleResult carries at least `exit_code`; other fields derived).
- `resolve_exit(conditions: frozenset[int]) -> int`: precedence 2, 6, 7, 5, 3, 4; 75 only when nothing else ran; 0 otherwise.
- `status_report(store, audit, now)`.
- `slo_numbers(lines: Iterable[dict], doc: StoreDoc, now) -> SloNumbers` (NFR-013 a-d, D 10.3).
- Module constants (D 14): `max_candidates` 10, `max_launches_per_cycle` 1, call cap 35 / reserved 3, page cap 5, day cap 6, `max_attempts` 3, backoff 10 min, lease 60 min, timeouts gh 20 / probe 10 / git 10 / Orca 120 / deadline 240, skew tolerance 300 s, skew warning 60 s, clamp 3600, health age 900, stale age 24 h. Names not fixed (derived).

Realises: FR-001, FR-002 (orchestration), FR-004, FR-007 (cycle effects), FR-011, FR-014 (steps), FR-016, FR-018 (mid-cycle), FR-019, FR-021 (status content), FR-022, FR-023 (stamps), FR-027 (config), FR-028, FR-029, NFR-007, NFR-008, NFR-009, NFR-010, NFR-013.
May import: `runner, github, predicates, record, launch, audit` (never `subprocess`).
Tests: `test_cycle.py`, `test_slo_helper.py` (section 2).
Traps: S1 (D 6.3 lines 388, 104): after one launch or any launch-step outcome (including `revalidation_failed`), remaining candidates are neither read nor stamped and get no decision line; k bounds only cycles where every candidate skips. A candidate skipped locally at step 10 is stamped. `budget_exhausted` is not stamped. Dry-run computes but writes only `dry-run.json` and audit; step 14 health stamp skipped; every line `dry_run: true`. Health stamp only on exit 0 that is not DISABLED/not_enabled/disabled_mid_cycle/dry-run. `cycle_id` is `uuid4().hex` (non-deterministic: tests assert a regex or inject). Hostname via `deps.host`. Network-FS check reads `/proc/self/mountinfo` (make it an injectable function or monkeypatchable, because a CI tmp dir can sit on a deny-listed type such as 9p). `Retry-After` is readable only on G1; per-issue rate limits always clamp to 3600 s (C22, Q3).

### 1.8 M8: `cli.py` (order 8)

Public API (stated D 4.1 lines 112-121, D 5.2 line 225, D 11 line 759):
- `issue_watch_group` (Click group; registered under the name `issue-watch`).
- Verbs: `once [--dry-run] [--config]`, `status [--json] [--config]`, `check-config [--config]`, `init-state [--config]`, `reset <N> --forfeit-guarantee [--config]`, `reset --rate-limit [--config]`. `--config` default `~/.config/superclaude/issue-watch.json`. `reset` with both `N` and `--rate-limit`, or neither, or `N` without `--forfeit-guarantee`: exit 2.
- `build_deps(config) -> Deps` (real runner, `FileStore`, `OrcaLauncher`, `SystemClock`, `AuditLog`, `socket.gethostname()`).
- Exit codes per verb (D 4.1 table): `once` 0,2,3,4,5,6,7,75; `status` 0/1/2/6; `check-config` 0/2; `init-state` 0/2/6; `reset` 0/2/6/75.
- `status` text and `--json` fields (D 10.2 lines 728-739); `retry[].argv` rebuilt, printed with `shlex.join`, orca resolved with `shutil.which` over `_ORCA_CLIS` (no probe).
- `check-config` prints state-dir validity, approvers file mtime (UTC ISO 8601) and entry count only (R10).

Realises: FR-015, FR-018 (kill switch via status), FR-019 (flags), FR-021, FR-026, FR-027 (check-config).
May import: `cycle, record, audit, launch, runner`; `click`.
Tests: `test_cli.py` (CliRunner; each verb's exit codes; init-state refuses existing store and changes nothing; check-config and status write nothing, mtimes unchanged; reset behaviours; `status --json` field set; retry argv for an `unknown` entry; help lists six verbs), `test_cli_e2e.py`.
Traps: no business logic in `cli.py`; HOME and `XDG_STATE_HOME` must be monkeypatched in every CLI test so nothing reads `~/.config/superclaude/`; `reset` audit line has no defined reason (Gap G-04); `reset N` where N has no entry is unspecified (propose exit 2).

### 1.9 M9: `src/superclaude/cli/main.py` registration

Two lines after the `reflect_group` registration (D 11 line 760; D 5.1 line 173 says "after reflect, line 561"). Same pattern as the neighbours: `from superclaude.cli.issue_watch.cli import issue_watch_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports` then `main.add_command(issue_watch_group, name="issue-watch")`. Verification: `uv run superclaude issue-watch --help` lists six verbs. The line number 561 comes from the design; re-verify at build time (research 02 covers).

---

## 2. Test files (D 11 lines 761-765, D 12 lines 770-791, D 17, spec S 8 line 361)

Total: 8 per-module files + 11 cross-cutting files = 19 test files, plus `__init__.py`, `conftest.py`, fixtures, stubs. Spec rule: each FR criterion and each Section 7 row is one test case (S 8 line 361). No test calls real `gh`, `orca`, `git` or network (D 12 line 772). D 12 describes 8 of the 19 files itself (`test_crash_injection`, `test_concurrency`, `test_cycle::test_fifty_cycles`, `test_cycle::test_acceptance_property`, `test_no_shell`, `test_no_text`, `test_module_boundaries`, `test_marker_contract`); the rest below are derived from D 9.1, D 17 and the spec.

### 2.1 Per-module files

| File | Asserts (source) | Fixtures / fakes |
|---|---|---|
| `test_runner.py` | str argv `TypeError`; `shell=False`; DEVNULL stdin; stderr 500-byte cap by bytes; `TimeoutExpired` -> `timed_out`; `OSError` -> `spawn_error` class name only (NFR-004, T6, T11) | monkeypatch `subprocess.run` in `runner`; no real child |
| `test_predicates.py` | AC-3, AC-4, T2, T3, T4: outsider relabel (approver-labeled, outsider-unlabeled, outsider-labeled -> `not_approved`), Bot type, `x[bot]` login, unlabel after approval, `approval_before_trigger`, `approval_before_init`, tie -> `events_incomplete`, edit 1 s after approval -> `edited_after_approval`, renamed event after approval; `is_intended_owner` for {other}, {}, {own, other}, {own} (FR-008); project: wrong project, two items, archived item, Status `In progress`, `Backlog` (FR-007); marker window `>= pending_at - 300 s` boundary and `current approved_at` floor; `eligibility_order` example {7:T1, 8:T2} + new 9 -> 9,7,8 | hand-built frozen dataclasses; no fakes |
| `test_audit.py` | AC-14: `REASONS` equals spec table (52); unknown reason `ValueError`; no forbidden keys; sorted keys, ASCII; mode 0600; rotation keeps 4 files, none on exit-75 path; `stderr_fallback` keys; schema per line kind | `tmp_path`, `FakeClock` |
| `test_github.py` | AC-2, AC-20: G1..G7 argv equality; `--method GET` on REST; GraphQL constants; paging rows (D 8.2); `classify` rows; `retry_after` rows; `discover` validation and exit-4 conditions; budget (cap 35, 3 reserved); G1 header parse | `FakeRunner`, `_assumed_shape` fixtures |
| `test_record.py` | AC-6 (pending before launch), AC-10 (consumed_log through reset), AC-11, AC-22 part: T-1..T-13, other pairs raise, validation, migration, save/lock/modes, half-open windows, `day_cap_count`, `sweep`, `init_state` | `tmp_path`, `FakeClock`, `FileStore` real files |
| `test_launch.py` | AC-7, AC-8, AC-16 part: prompt table, 12-element argv, `find_orca`, `parse_origin`, `check_origin`, outcome mapping, operation-id regex, `OPERATION_ID_PATHS`, `ORCA_AGENT` pin | `FakeRunner`, orca `_assumed_shape` fixtures |
| `test_cycle.py` | AC-1, AC-5, AC-6, AC-10, AC-12, AC-13, AC-15, AC-18, AC-19: step order, FR-001 two-call idle, FR-002 failures, shared vs per-issue failure matrix (NFR-007), re-read branches (FR-011), DISABLED mid-cycle, dry-run byte-identical, FR-016 two cases (S1), FR-023 stamps and prune, FR-027 config/approvers table (0664, empty, foreign owner, login line, symlink, `enabled: false`), FR-028 rate-limit persist/clamp/exit 5 later, FR-029 deadline (236 s, 121 s), `resolve_exit` precedence, `test_fifty_cycles`, `test_acceptance_property` (N in {1,2,6,7,50,99}) | `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` |
| `test_cli.py` | AC-9, AC-11, AC-17: every verb's exit codes, init-state refuses, check-config/status write nothing (mtimes), reset rules, `status --json` fields, retry argv | click `CliRunner`, `tmp_state`, monkeypatched HOME |

### 2.2 Cross-cutting files

| File | Asserts | Fixtures |
|---|---|---|
| `test_cli_e2e.py` | AC-1 and AC-19 end to end through `SubprocessRunner` with stub executables: idle cycle sees exactly two `gh` calls (FR-001 GWT); stub `orca` reads `dispatch.json` when invoked and sees `pending` with `launches` 1 and `consumed_at` (FR-010 GWT); one launch only; sleeping `gh` stub gives `gh_timeout` exit 3 (NFR-008) | `stubs/gh`, `stubs/orca`, (needs `git`: Gap G-03), scenario file in, argv log out; guard that `shutil.which("gh")` is the stub |
| `test_security_invariants.py` | NFR-001..NFR-004: `test_prompt_regex_property` over seeded `random.Random(331)` 2,000 draws plus FR-012 edge list, tagged `property_based`; every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`; argv prefix scan (only G1..G7, probe, launch); zero `SuperClaude-Org`, zero `{owner}`; no GraphQL constant contains `mutation`; every constant contains the literal repo; every REST argv has `--method GET` (G1 and graphql exempt); launch argv equals the 12-element list (T10) | `FakeRunner`, FR-012 corpus |
| `test_crash_injection.py` | NFR-005: for each of C1..C5 (D 7.6 lines 525-531): run, crash with `SystemExit` at that point, rerun; spec adds 5 reruns each (S 5 NFR-005): total fresh launches per issue never above 1 | `CrashingStore(real, crash_at="C1".."C5")`, `FakeRunner`, `FakeLauncher` |
| `test_concurrency.py` | FR-017/AC-11: two `multiprocessing` processes on one `tmp_path` store: one exits 75 `lock_held`, one launch total; symlinked or foreign lock exits 6; lock path replaced after acquisition exits 75 | real `FileStore`; consider `thread_safety` marker |
| `test_no_shell.py` | AC-21: AST scan of `src/superclaude/cli/issue_watch/`: no `shell=True`, no `os.system`, no `subprocess` import outside `runner.py` | AST |
| `test_no_text.py` | NFR-006, T11: hostile title, body, stderr (`PWNED-TITLE`) never appear in audit, store, prompt, stdout, any argv | `FakeRunner` scripted with hostile replies |
| `test_origin_parity.py` | AC-16: load `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py` with `importlib.util.spec_from_file_location`; `launch.parse_origin` and `parse_origin_url` agree on one table; case difference pinned (C3) | URL table |
| `test_marker_contract.py` | FR-009: `predicates.CLAIM_MARKER` occurs verbatim in `refs/claim.md` and `templates/claim-comment.md` of `sc-issue-protocol` ("read through the dual surface", D 12 line 791) | Gap G-12: CI has no `~/.claude` and `.claude/` is gitignored, so the `src/superclaude/skills/...` path is the one that always exists |
| `test_find_orca_parity.py` | FR-013, T17: drive the original `install_user_setup._find_orca` by monkeypatching `shutil.which` and `subprocess.run`, and `launch.find_orca` through `FakeRunner`; same table; exclude the non-dict element (C19) and pin that difference; `_ORCA_CLIS` identity; screen-reader stub answering non-JSON | table |
| `test_module_boundaries.py` | AC-25, NFR-014: AST walk of each module (nested imports included, so the lazy `write_prepared_bytes` import counts); allowed imports exactly D 5.3 table; no module named `select`; only four Protocols | AST |
| `test_slo_helper.py` | AC-24, NFR-013: `slo_numbers` returns (a) p95 approval-to-`launched`, (b) 7-day exit-0 share excluding disabled/not_enabled/dry_run, (c) share of `launched` reaching `claimed` before lease, (d) stale count, on a fixture log across `audit.jsonl.4`..`audit.jsonl` | synthetic JSONL lines |

### 2.3 Test-gap notes from the spec and design

- NFR-005 lists "an account rename" test; no design test covers it (Gap G-13). Suggested case in `test_cycle.py`: store entry with `launch_login` A, then discovery under login B for the same issue number; no second launch because `launches` is keyed by issue number.
- NFR-005 says crash injection is "followed by 5 reruns"; D 12 line 784 says one rerun. Use the spec (5).
- AC-19 "a sleeping stub": a real 20 s `gh` timeout would make the test slow; the timeout must be a module constant the test can shrink with `monkeypatch`, or the stub sleeps just over a shrunk timeout (mark `slow` only if unavoidable).
- NFR-010 (second `once` against identical stub state launches nothing) has no named test; `test_fifty_cycles` covers it implicitly. Add an explicit `test_second_once_launches_nothing`.
- NFR-012 (no new dependency) has no unit test; it is a gate (`make verify-deps`, `git diff --exit-code pyproject.toml`).

---

## 3. Shared test infrastructure to create first

Create order and content (D 11 line 761; D 12 lines 774-780; D 5.4 line 295):

| Step | File | Content | Needs |
|---|---|---|---|
| 3.1 | `tests/issue_watch/__init__.py` | empty | none |
| 3.2 | `tests/issue_watch/conftest.py` (part 1) | `FakeClock(now, mono)` with `advance(s)`, `now()` returns tz-aware UTC, `monotonic()`; no `sleep` anywhere | none (structural Protocol) |
| 3.3 | `conftest.py` (part 2) | `FakeRunner(script: dict[tuple[str, ...], CommandResult \| Callable])`: records every argv (and cwd, Gap G-01), unknown argv returns `returncode=99` and the test fails at teardown (D 12 line 776), supports a callable value (for a hook that creates `DISABLED` mid-cycle or reads `dispatch.json`); D 12 writes the value type as `Reply` but D 5.4 as `CommandResult \| Callable` (Gap G-14); helper to build `CommandResult` | `runner.py` |
| 3.4 | `fixtures/_assumed_shape/*.json` | See the table below | none |
| 3.5 | `conftest.py` (part 3) | `tmp_state` fixture: monkeypatch `HOME` and `XDG_STATE_HOME` to `tmp_path`, call `record.init_state(...)`, return the `FileStore` | `record.py` |
| 3.6 | `conftest.py` (part 4) | `FakeLauncher(outcomes)`: records argv and cwd, can raise; also option to inspect `dispatch.json` at call time (FR-010) | `launch.py` (`LaunchOutcome`) |
| 3.7 | `conftest.py` (part 5) | `CrashingStore(real, crash_at="C1".."C5")`: raises `SystemExit` at the named point (D 7.6 table) | `record.py` |
| 3.8 | `stubs/gh`, `stubs/orca` (and `stubs/git`, Gap G-03) | executable bash; scenario file in, argv log out; stub dir prepended to `PATH` as `tests/pr_submit/test_conflict_e2e.py` does | none |
| 3.9 | `conftest.py` (part 6) | fixture `stub_path(tmp_path, monkeypatch)` that builds the stub dir, sets `PATH`, asserts `shutil.which("gh")` is the stub; helper `deps(...)` factory building `cycle.Deps` from fakes | `cycle.py` |

Proposed `_assumed_shape` fixtures (names derived from D 15 lines 829-847 "recorded in the matching `_assumed_shape` fixture name"; the design lists no filenames, Gap G-15). Each is JSON, with a `"_assumed_shape": true` marker and a `"source"` string naming the D 15 row, so FU-1 replaces them one for one:

| Proposed file | Stands in for (D 15 row) | Consumed by |
|---|---|---|
| `gh_issue_list.json` | `gh issue list --json number,labels,assignees,state` field names (line 834) | `test_github`, `test_cycle` |
| `gh_api_user_include.json` | `gh api user --include` layout (status line, `Date`, `Retry-After`, blank line, body) (line 835); not JSON on the wire, so the fixture wraps the raw text in a JSON string field | `test_github` |
| `rest_events_page.json` | events fields `event, actor.id, actor.type, label.name, created_at, id` (line 836) | `test_github`, `test_predicates` |
| `rest_comments_marker.json` | MARKER_JQ projection output | `test_github` |
| `graphql_edits.json` | `userContentEdits` / `lastEditedAt` (line 837) | `test_github` |
| `graphql_project_items.json` | `projectItems`, `fieldValueByName` (line 837) | `test_github` |
| `gh_stderr_auth_401.json`, `gh_stderr_rate_403.json`, `gh_stderr_rate_429.json`, `gh_graphql_insufficient_scopes.json`, `gh_graphql_rate_limited.json` | stderr substrings and GraphQL error types (line 838) | `test_github` classify |
| `orca_launch_success.json`, `orca_launch_unknown.json` | `outcome.kind`, `receipt.detail`, operation-id path, `agent_session_operation_unknown` (lines 840-841) | `test_launch`, `test_cli_e2e` |
| (`orca_skills_list` has a VERIFIED shape from `install_user_setup.py:198-221`; not an `_assumed_shape` file) | | |

Stub scenario format (derived; D 12 line 780 only says "scenario file in, argv log out"): the stub reads a scenario path from an environment variable (JSON mapping an argv key to stdout/stderr/exit code/sleep seconds) and appends each argv as a JSON line to an argv log path. The stub `orca` also copies `dispatch.json` into the log on a launch argv for the FR-010 GWT.

---

## 4. Runbook `docs/designs/issue-watcher-setup.md` content outline

Sources: D 1 line 30 ("label, approver and scheduler setup, operator runbook"), D 11 line 766 ("Runbook steps 1 to 10 for the owner"), D 9.1 lines 666, 671 (T10, T16 reference the runbook), spec S 8 lines 384-395 (the 10 steps), S 1 deployment gate. Note spec S 8 line 384 puts the runbook inside `docs/designs/issue-watcher.md`; the design moved it to the separate setup file and the design file itself contains no runbook section (grep for "runbook" in the design returns only references). Follow the design.

| # | Section | Content |
|---|---|---|
| 0 | Purpose and status | One paragraph; "nothing here is run by the implementation"; the doc is for the owner; links to `issue-watcher.md` and the live-test record `docs/designs/issue-watcher-live-test.md` (written by the owner in FU-1, not by this task) |
| 1 | Pre-flight (step 1) | `gh auth status`; `gh auth refresh -s read:project` if the Project read fails; `orca` on PATH (and the `orca-cli` topic check); worktree exists with origin IronbellyOrg/IronClaude; `check-config` exits 0 |
| 2 | Config file | JSON example with every field of D 4.2 (`schema_version`, `enabled: false`, `labels`, `project_id`, `owner_account_id`, `worktree`, `approvers_file`, `state_dir`); unknown keys rejected; default path `~/.config/superclaude/issue-watch.json` |
| 3 | Approvers file | one decimal account ID per line; `#` comments; owner-only, not group/other-writable, regular file, no symlink; at least one ID; `check-config` prints mtime and entry count (R10); how to find an ID is not in the design: mark as owner action to verify (a `gh api users/<login>` read is plausible but UNVERIFIED) |
| 4 | Label setup (step 2) | owner-run: `gh label create issue-watch:trigger --repo IronbellyOrg/IronClaude` and `gh label create issue-watch:approved --repo IronbellyOrg/IronClaude` (D 15 line 839 marks the form UNVERIFIED: confirm with `gh label create --help`); `/sc:issue` never creates labels |
| 5 | `init-state` and re-approval (step 7) | run before the 24 h shadow; re-apply approval labels on issues approved before init (approvals older than `created_at` never count) |
| 6 | Setup order per issue (step 8) | assign the owner, add the trigger label, then the approval label |
| 7 | Shadow rollout (steps 3, 9) | `once --dry-run` on schedule for 24 h; compare would-launch decision lines with expectation; review audit |
| 8 | Before cron (step 9) | 24 h shadow reviewed; two-process lock test on the real state directory; `state_dir` persistence check across a workspace restart; staleness alert wired (`last_completed_cycle_age_seconds` > 900); `issue-watcher-live-test.md` committed; then set `enabled: true`. The cron entry itself (`"0 */5 * * * *"`, six fields) is FU-2 and is not enabled by this work |
| 9 | Kill switch (step 4) | `touch <state_dir>/DISABLED`; remove to enable; a spawn already started cannot be stopped (R15) |
| 10 | Exit and reason codes (step 5) | table of D 4.3 exit codes with operator actions (S 8 lines 317-326) and the 52-reason table summary; `status --json` field list (D 10.2) |
| 11 | Recovery commands (step 5) | `reset <N> --forfeit-guarantee` (only `abandoned`/`unknown`; prints that N may launch twice; operator checks the session first, M1); `reset --rate-limit`; broken store: move the directory aside and run `init-state` (never hand edit); retry command printed by `status` (run from the stored `launch_cwd`) |
| 12 | Alerting (step 6) | alert when `last_completed_cycle_age_seconds` > 900; FU-4 sink not chosen |
| 13 | While enabled (step 10) | never hand-claim a trigger-labelled issue; remove the trigger from claimed issues; one enabled workspace per login (T7, OD-8) |
| 14 | Deployment gate and permissions | the live test (FU-1), permission mode record, the default "no override", a bypass mode needs written owner acceptance (OD-7, T10) |
| 15 | Residual risks | R10-R18 one line each; Coder#477 statement verbatim (D 2.2 line 49); nine revisit conditions (D 2.3 line 60) |

Doc rules for the writer: no UNVERIFIED shape stated as fact; no model name; every `gh` command names `--repo IronbellyOrg/IronClaude` where a repository applies; no SuperClaude-Org reference except as a "never" statement.

---

## 5. FR and NFR traceability to module and test (D 18 lines 900-935)

D 18 covers all 29 FR (FR-001..FR-029) and all 14 NFR; none is missing from D 18. The columns below add the module that realises it and the test that must prove it (D 17 acceptance ids in brackets). Flags: NO-TEST = design names no test; PARTIAL = covered only implicitly.

| Id | Module(s) | Test(s) | Flag |
|---|---|---|---|
| FR-001 | cycle (steps 1-15), cli | `test_cycle` order [AC-1]; `test_cli_e2e` (idle = exactly 2 `gh` calls) | |
| FR-002 | github.user, cycle | `test_github` (G1 parse), `test_cycle` (exit 3 `gh_auth_failed`, exit 2 `account_id_mismatch`, exit 3 `login_invalid`) [AC-1] | |
| FR-003 | github.discover | `test_github` (argv equality), `test_cycle` (warning at 80) [AC-2] | |
| FR-004 | github.discover, cycle | `test_github`, `test_cycle` (100/101 -> exit 4 `truncated`; repeated number `discovery_duplicate`) [AC-2] | |
| FR-005 | predicates.approval_of, github events | `test_predicates` [AC-3] | |
| FR-006 | predicates.approval_of | `test_predicates` (relabel, `events_incomplete`) [AC-3] | |
| FR-007 | predicates (project check), github G6, cycle | `test_predicates`, `test_cycle` (project_unreadable continues; missing scope exit 3) [AC-4] | |
| FR-008 | predicates.is_intended_owner | `test_predicates`, `test_cycle` (re-read {own, other}) [AC-4] | |
| FR-009 | predicates.CLAIM_MARKER, record.mark_claimed, github G4 | `test_predicates`, `test_record` (T-10..T-12), `test_cycle`, `test_marker_contract` [AC-5] | |
| FR-010 | record.mark_pending, cycle | `test_cycle` (pending saved before launcher), `test_cli_e2e` (stub orca reads dispatch.json) [AC-6] | |
| FR-011 | cycle, github G7/G3'/G6' | `test_cycle` (closed -> `revalidation_failed`; timeout -> `failed` attempts 1; reserved 3 calls) [AC-6] | |
| FR-012 | launch.build_claim_prompt | `test_launch`, `test_security_invariants::test_prompt_regex_property` [AC-7] | |
| FR-013 | launch.launch_argv/find_orca/check_origin | `test_launch`, `test_find_orca_parity` [AC-8] | |
| FR-014 | launch, record, cycle step 12 | `test_launch` (outcome table), `test_record`, `test_cycle` [AC-8] | |
| FR-015 | cli.status, launch.launch_argv | `test_cli` (retry argv), `test_cycle` (no orca argv for `unknown`) [AC-9] | Design form differs from spec GWT (Gap G-16 / C20 / Q2) |
| FR-016 | cycle | `test_cycle` FR-016 cases (a) and (b) [AC-10] | S1 reading (Gap G-16) |
| FR-017 | record.FileStore.lock | `test_record`, `test_concurrency`, `test_cli` [AC-11] | |
| FR-018 | record.disabled, cycle | `test_cycle` (disabled; created mid-cycle) [AC-12] | |
| FR-019 | cycle (dry-run), record (`dry-run.json`) | `test_cycle`, `test_cli` [AC-13] | |
| FR-020 | audit | `test_audit`, `test_cycle` (one cycle line per exit 0,2,3,4,5,6,7,75 + decision line per examined issue) [AC-14] | |
| FR-021 | cycle.status_report, cli.status | `test_cli` (mtimes unchanged, unhealthy at 1000 s, unknown 25 h with retry) [AC-9, AC-17] | |
| FR-022 | github.classify, cycle | `test_cycle` failure matrix (shared voids cycle; per-issue skips) [AC-15] | |
| FR-023 | predicates.eligibility_order, cycle step 13 | `test_predicates`, `test_cycle` (stamps, prune, dry-run identical) [AC-10] | |
| FR-024 | record.day_cap_count, consumed_log | `test_record`, `test_cycle::test_acceptance_property` [AC-10] | |
| FR-025 | launch.parse_origin/check_origin | `test_launch`, `test_origin_parity`, `test_cycle` (exit 2 before discovery; changed before pending) [AC-16] | |
| FR-026 | cli | `test_cli` (all verbs) [AC-17] | `reset` audit reason undefined (Gap G-04) |
| FR-027 | cycle.load_config/validate_approvers | `test_cycle` approvers/config table, `test_cli` check-config [AC-12] | |
| FR-028 | github.classify/retry_after, record.next_permitted_at, cycle | `test_github`, `test_cycle`, `test_cli` (`reset --rate-limit`) [AC-18] | 120 s case only reachable via G1 (Gap G-17) |
| FR-029 | cycle.Deadline | `test_cycle` (236 s, 121 s), `test_cli_e2e` sleeping stub [AC-19] | slow-test trap |
| NFR-001 | launch | `test_security_invariants`, `test_launch` [AC-7] | |
| NFR-002 | github, runner | `test_security_invariants` (argv prefix scan) [AC-20] | |
| NFR-003 | github, launch | `test_security_invariants` (no `SuperClaude-Org`, no `{owner}`) [AC-20] | |
| NFR-004 | runner | `test_runner`, `test_no_shell` [AC-21] | |
| NFR-005 | record, cycle | `test_crash_injection`, `test_concurrency`, `test_cycle::test_fifty_cycles`, `test_cli_e2e`, `test_no_text`, FakeRunner exit 99, `_assumed_shape` fixtures [AC-22] | account-rename test missing (Gap G-13) |
| NFR-006 | audit | `test_audit`, `test_no_text` [AC-14] | |
| NFR-007 | github.classify, cycle | `test_cycle` table-driven failure injection per read [AC-15] | no named test; add `test_shared_failure_matrix` |
| NFR-008 | cycle.Deadline, runner | `test_cycle`, `test_cli_e2e` [AC-19] | |
| NFR-009 | github.CallBudget, cycle | `test_github`, `test_cycle` (10 candidates call count, rate-limit stub) [AC-10] | |
| NFR-010 | cycle, record | `test_cycle::test_fifty_cycles` | PARTIAL: add explicit second-run test |
| NFR-011 | record | `test_record` (truncated, missing, higher version, migration, modes, dir fsync) [AC-22] | |
| NFR-012 | none | none | NO-TEST: gate only (`make verify-deps`, unchanged `pyproject.toml`) [AC-23] |
| NFR-013 | cycle.slo_numbers | `test_slo_helper` [AC-24] | |
| NFR-014 | all | `test_module_boundaries`, `test_origin_parity`, `test_find_orca_parity` [AC-25] | |

Design acceptance criteria AC-1..AC-25 (D 17) are all mapped above; AC-23 is gate-only.

### 5.1 Design statements that contradict the spec or itself

| # | Statement | Where | Conflict | Resolution to encode |
|---|---|---|---|---|
| X1 | S1: FR-016 GWT "cycle 1 examines k and launches 1" vs "a second eligible candidate is never reached" | D 6.3 line 388, line 104; spec FR-016 line 163-164 | Spec inconsistent with itself; design picks the safety sentence | Two test cases: (a) 15 all-skip issues, cycle 1 examines k, cycle 2 starts with the unexamined; (b) 15 eligible, cycle 1 examines 1 and launches 1. Owner question Q1 |
| X2 | FR-015 GWT prints `<orca> agent launch --retry-launch op-1 --json` | spec line 161 vs D 10.2 line 741, C20 line 101 | Design prints the full original 12-element argv with `--retry-launch <id>` before `--json` plus `cwd`; the spec string is not a substring of it | Implement the design form; test asserts the full argv; record owner question Q2 |
| X3 | FR-028 takes the reset time "from `Retry-After` or the reset header" | spec line 196 vs D 8.3 lines 594-602, C22 | Only G1 uses `--include`; any per-issue rate limit always clamps to 3600 s | FR-028 GWT "Retry-After: 120" test must drive the rate limit on the G1 call; per-issue case asserts `rate_limit_clamped`. Q3 |
| X4 | Store field `last_completed_cycle_at` | D 7.2 line 412, D 6.2 line 360 | Not in the spec's store schema (S 7 line 267); design addition so `status` need not read the audit tail | Include; `validate` exact key set must include it |
| X5 | `status` exit 1 when unhealthy | D 4.1 line 121 | Spec defines content, not its code | Include; flagged as design choice |
| X6 | Runner API name | spec S 8 line 309 `run_command(argv, timeout)` vs D 5.4 `Runner.run` / `SubprocessRunner.run` | Naming | Follow the design Protocol |
| X7 | `find_orca(runner)` (spec FR-013) vs `find_orca(runner, which)` (D 5.2 line 222) | | Signature extension | Follow the design; `which` parameter required by the seam table (D 5.4 line 299) (Gap G-02) |
| X8 | Crash injection reruns: spec 5 reruns, design one rerun | spec NFR-005 line 213 vs D 12 line 784 | | Use 5 |
| X9 | C21 "`--method GET` mandatory on every G2 to G7 argv; a test rejects any `-F` argv without it" | D line 102 | G2 is `gh issue list`; G5/G6 are GraphQL and carry `-F number=N` without `--method GET`; D 8.1 line 554 exempts G1 and graphql | Encode D 8.1 (Gap G-08) |
| X10 | Runbook location | spec S 8 line 384 (inside the design doc) vs D 1/11 (separate `issue-watcher-setup.md`) | | Create the setup doc; the design doc is not edited by the task |
| X11 | Runner `cwd` | D 8.4 line 625 vs Runner Protocol D 5.4 line 264 (no cwd) | Protocol cannot carry the cwd | Add an optional `cwd` keyword to `Runner.run` (Gap G-01) |
| X12 | `record.sweep(store, now)` and `day_cap_count(store, now)` (D 5.2) vs "every function takes the document and `now` and returns a new `StoreDoc`" (D 7.4 line 492) and `day_cap_count(doc, now)` (D 10.2 line 737) | | Parameter type ambiguity | Use `StoreDoc` for pure functions; `sweep(doc, now) -> (doc, list)` (Gap G-10) |
| X13 | `audit.stderr_fallback(line)` (D 5.2) vs `stderr_fallback(reason, exit)` (D 10.1 line 722) | | | Use (reason, exit, ...) form since the fallback carries only `kind, ts, host, exit, reason` (Gap G-05) |
| X14 | D 5.3 line 244 says `cli.py` is imported "lazily from `main.py`" | | `main.py` registration (reflect pattern) imports at module load; `superclaude --help` loads the whole package | Keep `fcntl` import inside `lock()`; do not rely on lazy loading |
| X15 | Closed `last_reason` enum vs `record` may not import `audit` | D 7.2 line 437 vs D 5.3 line 239 | | Type-only validation in `record`; membership test in `test_cycle`/`test_audit` (Gap G-07) |

---

## 6. Proposed phase plan, checkpoints and final gates

Template 02 shape (discovery, build, test, QA gates, completion) from research-notes. One checklist item per file; each build item is "write module" followed by "write its test" in the same phase so the phase checkpoint can run the tests.

| Phase | Items (one per file) | Checkpoint output |
|---|---|---|
| P1 Discovery and baseline | Re-verify the 23 citations of D 3 and the UNVERIFIED list of D 15 that matter to code (research 02 supplies); confirm `src/superclaude/cli/issue_watch/` and `tests/issue_watch/` absent; `git status` clean of `.claude/`; read `tests/pr_submit/test_conflict_e2e.py` stub pattern | A short findings file under the task `phase-outputs/`; no code |
| P2 Foundation | `__init__.py` (src), `tests/issue_watch/__init__.py`, `runner.py`, `conftest.py` part 1-2, `test_runner.py`, `test_no_shell.py` | `uv run pytest tests/issue_watch/ -v` green; ruff check and format check clean on the new paths |
| P3 Pure leaves | `predicates.py`, `test_predicates.py`, `audit.py`, `test_audit.py` | Both test files green; `REASONS` count 52 asserted; predicates reasons subset of `REASONS` test |
| P4 GitHub layer | `fixtures/_assumed_shape/*.json` (GitHub ones), `github.py`, `test_github.py` | `test_github.py` green; every argv constant printed in the test equals D 8.1 |
| P5 Store layer | `record.py`, `test_record.py`, `conftest.py` part 3 (`tmp_state`) and part 5 (`CrashingStore`) | `test_record.py` green incl. 13 transition rows and the "other pairs raise" table; lock cases pass under `-n auto` |
| P6 Launch layer | orca `_assumed_shape` fixtures, `launch.py`, `test_launch.py`, `conftest.py` part 4 (`FakeLauncher`), `test_origin_parity.py`, `test_find_orca_parity.py`, `test_marker_contract.py` | Parity tests green against the real original code; `ORCA_AGENT` pin green |
| P7 Orchestration | `cycle.py`, `test_cycle.py` (including `test_fifty_cycles`, `test_acceptance_property`), `test_slo_helper.py`, `test_crash_injection.py`, `test_concurrency.py` | Whole `tests/issue_watch/` green; acceptance property passes for N in {1,2,6,7,50,99}; crash points C1..C5 pass |
| P8 CLI and registration | `cli.py`, `test_cli.py`, `main.py` two lines, `stubs/gh`, `stubs/orca` (`stubs/git`), `test_cli_e2e.py`, `test_security_invariants.py`, `test_no_text.py`, `test_module_boundaries.py` | `uv run superclaude issue-watch --help` lists six verbs; e2e green with PATH stubs; boundary test green |
| P9 Docs | `docs/designs/issue-watcher-setup.md` (outline in section 4) | Document exists; every command in it is either from the design or marked UNVERIFIED; no live action performed |
| P10 QA gates and completion | Run the gates below; spec/design traceability audit (section 5 table, every FR/NFR has a green test); `git add .dev/tasks`; confirm nothing under `.claude/` is staged; POST reflect gate `--spec docs/designs/issue-watcher.md` (per research-notes TEMPLATE_NOTES) | Gate transcript; traceability verdict; staged file list |

Final gate list (D 13 lines 795-803, C8, C10, C13 and spec S 8 line 366):

1. `uv run pytest tests/issue_watch/ -v`
2. `make lint` (includes `lint-architecture`, C8)
3. `uv run ruff format --check src/ tests/` (no make target, C10; ruff 0.15.20)
4. `make test` (CI uses `-n auto`; the whole-suite runtime is for research 03 to size; the builder should also run `uv run pytest tests/issue_watch/ -n auto`)
5. `make verify-deps`
6. `make sync-dev` then `make verify-sync` (unaffected: no skills/agents/commands/hooks/templates change; `sync-dev` is preparation, not a gate)
7. `git diff --exit-code pyproject.toml Makefile` (NFR-012: no dependency, marker or entry point change)
8. Staging check: `.dev/tasks/` staged, no `.claude/` path staged.

---

## 7. Risks and traps for an implementer

| # | Trap | Why | Mitigation |
|---|---|---|---|
| T-A | Python 3.10 floor (D 13 line 805; `pyproject.toml` `requires-python >=3.10`) | `datetime.fromisoformat` rejects a trailing `Z` before 3.11; no `datetime.UTC`; no `tomllib`; no `typing.Self`/`StrEnum`/`ExceptionGroup`; `X \| Y` annotations are fine on 3.10 | strict regex plus `strptime`; `timezone.utc`; JSON config; plain classes and `Literal` |
| T-B | xdist (`pytest -n auto`, `test.yml:47`, C11) | Shared names collide; global state leaks; env mutation leaks | `tests/issue_watch/__init__.py`; `tmp_path` per test; `monkeypatch.setenv` (never `os.environ[...] =`); no module-level caches mutated by tests; the two-process lock test uses its own `tmp_path` state dir; no `sleep` (FakeClock) |
| T-C | `fcntl`, `O_NOFOLLOW`, `/proc/self/mountinfo` are Linux-only | Top-level `import fcntl` would break `import superclaude` elsewhere because `main.py` imports `cli.py` eagerly | import inside `lock()`; platform check first in every verb that needs them (`once`, `check-config`, `init-state` exit 2); tests monkeypatch `sys.platform` and the mountinfo reader (CI tmp dir can sit on a deny-listed type such as 9p) |
| T-D | S1 reading of D 6.3 | Following the FR-016 GWT literally would examine and launch a second candidate | After the first launch-step outcome stop reading and stamping; two-case test (X1) |
| T-E | UNVERIFIED shapes (D 15) | Pinning real field names in code or test bodies makes them look verified | Only `_assumed_shape` JSON fixtures carry the assumed shapes (each with `_assumed_shape: true` and source); stderr substrings in ONE table constant (D 8.2 line 590); `OPERATION_ID_PATHS` tuple; never write "verified" for them; FU-1 replaces fixtures |
| T-F | No model name in any file | Project/user constraint; PF-034 also forbids repeating the agent literal in the design | Task items and docs refer to "the seed-brief agent token"; the constant's literal appears only in `launch.py` and its one pin test; no tier or model names anywhere |
| T-G | Pin test for `ORCA_AGENT` | Reading `.dev/brainstorms/.../seed-brief.md` fails in CI (path untracked) | Test holds the expected token as a literal (or skips only if the path is absent and a second assertion covers the argv); decide in the task (Gap G-20) |
| T-H | `gh` always names `--repo IronbellyOrg/IronClaude` (CLAUDE.md fork rule; NFR-003) | gh defaults to the upstream parent; `{owner}` placeholders resolve to upstream | `github.REPO` constant is the only source; GraphQL constants carry the literal; argv-scan test; the test file necessarily contains the forbidden needle string as a negative fixture (allowed by CLAUDE.md "static references in test fixtures"); never run any `gh` against `SuperClaude-Org`; runbook commands use `--repo` |
| T-I | Only a validated integer reaches the prompt (D3, FR-012) | `bool` is an `int`; numeric strings; floats | `type(v) is int` in `github.discover` and again in `build_claim_prompt`; everything else in the launch argv is a constant, the resolved orca path or the configured worktree; the status retry argv is rebuilt from `build_claim_prompt(issue)`, not stored text |
| T-J | Real tools leak into tests | PATH on this Coder host may contain `orca-ide`, `gh`, `git` | e2e PATH = stub dir + `/usr/bin:/bin`; guard asserts `shutil.which("gh")` is the stub and `which("orca-ide")` is None or stub; `HOME`/`XDG_STATE_HOME` patched so no real config or state is read |
| T-K | Write ordering | `pending` must be durably saved before the launcher call (FR-010) | `FakeLauncher` inspects on-disk `dispatch.json` at call time; `CrashingStore` C1..C5 |
| T-L | `json` key types | `considered` and `entries` keys are decimal strings in JSON | convert at load/save only; `sort_keys=True` requires uniform key type |
| T-M | Arch lint (C9) | Rebinding a `contracts.__all__` name or an `ID_PATTERNS` body literal fails `make lint` | Do not name anything `ID_PATTERNS`, `THRESHOLDS`; avoid FR-/NFR-style regex literals; run `make lint` each phase |
| T-N | Ruff rules `E,F,I,N,W,TID`, line length 88, `TID` bans relative imports from parent modules | Long jq/GraphQL constants exceed 88 columns | build long strings from parenthesised pieces; use absolute `superclaude.cli.issue_watch....` imports as neighbours do (research 01 confirms the convention) |
| T-O | Lazy `write_prepared_bytes` import (C18) | `test_module_boundaries` must still see it | AST walk includes function-level imports; allowed list contains `superclaude.cli.swarm.atomic` |
| T-P | Module named `select` or `subprocess` use outside `runner.py` | NFR-014, NFR-004 | file names exactly as D 11; `test_no_shell` and `test_module_boundaries` |
| T-Q | The design and spec docs are untracked | Tests or doc links may cite `.dev/brainstorms/` | cite `docs/designs/issue-watcher.md` only; no test reads `.dev/` paths |
| T-R | Sleeping-stub timeout test | A real 20 s timeout slows CI | make the `gh` timeout a patchable module constant; the stub sleeps a fraction of a second over the shrunk value |
| T-S | Never write to GitHub (NG-2), never run anything live | The task includes the runbook and label commands | The runbook only documents commands; the task runs none; no `gh label create` in any step |

---

## Summary

- Build order is runner -> predicates -> audit -> github -> record -> launch -> cycle -> cli -> main.py (9 source files plus `__init__` and 2 registration lines), with test infrastructure (`__init__.py`, `conftest.py` in six increments, 12 to 15 `_assumed_shape` fixtures, PATH stubs) created in step with the module it depends on.
- 19 test files (8 per module, 11 cross-cutting) map to all 29 FR, 14 NFR and 25 AC; D 18 omits no id, but NFR-012 has no test (gate only), NFR-007 and NFR-010 have no named test, and NFR-005's account-rename test is missing from the design.
- 10-phase plan with checkpoints at each module layer; 8 final gates; 21 design inconsistencies or gaps (below) the task builder must settle in the task file before an implementer starts.

## Gaps

| Id | Gap | Suggested treatment in the task |
|---|---|---|
| G-01 | `Runner.run(argv, timeout)` has no `cwd`, but the launch call runs with `cwd=worktree` (D 8.4 line 625) and `LaunchOutcome`/retry rely on it | Add optional `cwd: Path \| None = None`; `FakeRunner` records it; `status` retry uses stored `launch_cwd` |
| G-02 | `find_orca(runner, which)` and `Runner.run` differ from spec names `find_orca(runner)` and `run_command` | Follow the design |
| G-03 | `test_cli_e2e` needs `git -C <abs> remote get-url origin`, but only `stubs/gh` and `stubs/orca` are listed and "no test runs a real git" | Add `stubs/git` (and list it in the task) |
| G-04 | `reset` writes "one audit line" (FR-026) but no reason or line kind exists in the closed reason table | Owner/builder decision; propose a `decision`-kind line with `note` "reset" and a reason from the table, or add reasons; flag in the task |
| G-05 | `stderr_fallback` signature differs between D 5.2 and D 10.1 | `stderr_fallback(reason, exit, ...)` |
| G-06 | `REASONS` is a frozenset but D 5.2 says "kind and exit per reason"; `re-approved` is in the table as a note | Companion mapping (name free); decide `re-approved` membership (recommend: in `REASONS`, used only in `note`) |
| G-07 | `last_reason` closed enum vs `record` cannot import `audit` | type-only validation; membership asserted in tests |
| G-08 | C21 text contradicts D 8.1 rule for `-F` argv | Encode D 8.1/T9 (REST only; G1 and graphql exempt) |
| G-09 | A second/third pre-pending failure (`failed` -> `failed`, attempts + 1) is not a T-row from "(none)" | `fail` allowed from none and from `failed`; adjust the "other pairs raise" table |
| G-10 | `sweep`/`day_cap_count` take `store` in D 5.2, `doc` in D 7.4/10.2 | pure functions on `StoreDoc` |
| G-11 | `Deps` and `CycleResult` have no stated owner module or field list | Put both in `cycle.py` (cli imports cycle); fields as D 5.4 line 302 |
| G-12 | "dual surface" read of `refs/claim.md` in `test_marker_contract` | Read the `src/superclaude/skills/sc-issue-protocol/...` path (always present); optionally also check installed copy when present |
| G-13 | NFR-005 "account rename" test missing from the design | Add to `test_cycle.py` |
| G-14 | `FakeRunner` script value type: `Reply` (D 12) vs `CommandResult \| Callable` (D 5.4) | `CommandResult \| Callable`; `Reply` is `classify` output |
| G-15 | `_assumed_shape` fixture filenames not given | Use the proposed names in section 3 |
| G-16 | Spec-vs-design deviations S1, C20 (FR-015 GWT string), C22 (FR-028), store field `last_completed_cycle_at`, `status` exit 1 | Task must cite the owner questions Q1-Q4 (D 16 line 866) and encode the design choice |
| G-17 | FR-028 GWT `Retry-After: 120` is only observable on G1 | Drive the 120 s test on the `api user --include` call |
| G-18 | Network-FS check uses `/proc/self/mountinfo`; a CI tmp dir on 9p/nfs would fail config tests | Make the reader injectable or monkeypatchable |
| G-19 | `reset N` for an entry that does not exist is unspecified | Propose exit 2 (usage), audited? no entry, no audit; flag |
| G-20 | `ORCA_AGENT` pin test source: seed brief is untracked | Literal inside the test, no `.dev/` read |
| G-21 | `init-state` network-FS refusal: spec lists only `once` and `check-config`; design `load_config` is shared by all verbs | Accept shared validation; test once |

**Status:** Complete

