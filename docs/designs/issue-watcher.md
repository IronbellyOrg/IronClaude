# Design: `superclaude issue-watch` GitHub issue watcher

**Status:** Implemented and merged in PRs #447 and #448; never run live; `enabled` ships as `false`; no schedule is installed. Next: the owner-run live test (FU-1), section 14.1 of [issue-watcher-setup.md](issue-watcher-setup.md) (`docs/designs/issue-watcher-setup.md`).
**Issue:** IronbellyOrg/IronClaude #331
**Branch:** `ironbelly/issue-331-github-issue-watcher`
**Source of truth:** `src/superclaude/` -> `make sync-dev` -> `.claude/` (never stage `.claude/`).
**Produced by:** `/sc:design @.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md --type architecture --format spec`, 2026-11-07.

---

## 1. Purpose and scope

The binding requirements are `.dev/brainstorms/20261107-064825-github-issue-watcher/spec-final.md` (cited below as "spec", with section numbers and FR/NFR ids). `spec-refactor-log.md` in the same folder is context only. This document turns the spec into modules, interfaces, schemas, call contracts and tests. It contains no implementation code: signatures, dataclass field lists, JSON schemas and short pseudo-flow only.

**What is built.** A poller that runs inside one person's Coder workspace. Every 5 minutes (cadence comes from a cron entry that is a follow-up, FU-2) it runs one cycle with that workspace's own `gh` login. A cycle finds issues on IronbellyOrg/IronClaude that are tagged, assigned exactly to the own login, approved by an allow-listed human, unchanged since approval and in the Project's Backlog column. For at most one such issue per cycle it starts one ordinary top-level agent session through `orca agent launch` with the prompt `/sc:issue --claim <N>`, after durably recording the dispatch.

**Guarantee (spec section 1).** At most one claim session per issue per intact, single dispatch store per login. A restored older backup (R11) or a second store on the same login (R12) breaks it; both are documented residual risks.

| Root cause (spec RC) | What this design does about it | Where |
|---|---|---|
| RC1 No "ready" signal exists | Trigger label plus approval label, approval actor checked against an allow-list, Project Status `Backlog` | sections 6, 8 |
| RC2 The claim routes to whoever runs it | `is_intended_owner`: assignee set exactly {own login}; discovery pre-filters with `--assignee` | sections 5, 8 |
| RC3 Nothing enforces at-most-once | Local dispatch record written durably (`pending`, `launches` + 1) before the spawn, plus the claim marker | section 7 |

| In scope (this design; built and tested with mocks only) | Out of scope |
|---|---|
| Package `src/superclaude/cli/issue_watch/` (8 modules plus `__init__.py`) | Anything live: no deployment, no cron entry, no real run |
| Click group `superclaude issue-watch` registered in `src/superclaude/cli/main.py` after `reflect` | Any listener, port, webhook, GitHub Action or service |
| Tests under `tests/issue_watch/`, all mocked: no real `gh`, `orca` or network call in any test | The post-claim pipeline (what the claim session does next) |
| This design doc, plus `docs/designs/issue-watcher-setup.md` (label, approver and scheduler setup, operator runbook) | The Coder template and its `coder_script` cron (FU-2) |
| `_assumed_shape` JSON fixtures standing in for unverified GitHub and Orca reply shapes | Writes to GitHub of any kind (NG-2), Project writes (NG-3) |

**Deployment gate (spec section 1; T10).** No cron entry is enabled and `enabled` stays `false` until an owner-run live test (FU-1) shows the prompt running as a slash command, records the session's permission mode, and replaces every `_assumed_shape` fixture with captured replies under which `tests/issue_watch/` still passes. The owner commits that record as `docs/designs/issue-watcher-live-test.md`; neither this design nor its implementation writes it.

## 2. Binding decisions

### 2.1 Owner decisions (verbatim from the seed brief, via spec section 2)

"D1 option A (workspace-side poller, pull); D2 claim-only; D3 only a validated integer issue number reaches a session prompt."

| Decision | Consequence in this design | Enforced by |
|---|---|---|
| D1 option A | No listener, inbound port or address registry. A pull poller run by cron in each workspace. | Package shape (section 5); NG-1 |
| D2 claim-only | The job ends once the session has been asked to run `/sc:issue --claim <N>`. The claim stops at `next-steps.md`. The poller never assigns, comments or moves Project items. | NG-2 test over every argv and GraphQL constant (section 12) |
| D3 integer only | The prompt is built only by `launch.build_claim_prompt(n)`, which accepts an `int` (not `bool`) in 1..999999999 and returns `/sc:issue --claim <n>`. No other text reaches the prompt. | FR-012, NFR-001 property test (section 9) |

### 2.2 Coder#477 statement (verbatim, spec section 9)

"Option A makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited. Options B and C, and Coder#477, return only on a revisit condition: the workspace cannot run a reliable cron, or one poller per login becomes unworkable."

### 2.3 Alternatives and revisit conditions (spec section 2)

| Alternative | Readiness criteria met / partly | Disposition |
|---|---|---|
| A: workspace poller | 2 / 8 | Owner-selected; this design |
| B: Action plus listener | 1 / 9 | Follow-up only; higher exposure and effort |
| C: central service plus listener | 0 / 10 | Follow-up only; extra hosting and webhook duties |
| D: label relay plus poller | 2 / 8 | First fallback if workspace Project access fails (FU-3) |

The nine revisit conditions (FU-7 tracks them): stopped workspaces cause excessive waiting; latency or API use becomes unacceptable; centralized approval or audit becomes necessary; duplicate claims persist; account binding becomes available; workspace tokens cannot read Projects; event-time Project changes matter; a shared ledger becomes necessary; recurring workspace execution proves impossible.

### 2.4 Other fixed spec decisions this design does not reopen

| Spec item | Fixed decision |
|---|---|
| Agent name | Module constant `launch.ORCA_AGENT`, pinned by a unit test to the `--agent` value of the seed brief's launch line. Not configurable. Its literal is not written in this document (PF-034). |
| Repository | Every repository-scoped `gh` call names `IronbellyOrg/IronClaude`; zero `SuperClaude-Org`, zero `{owner}` placeholder (NFR-003). |
| Process model | `gh`, `git` and Orca run as argv lists with `shell=False` (NFR-004). The poller is a plain process, never an Orca worker, so WC-13 ("workers never run `agent launch`", `src/superclaude/core/WORKER-CONTRACT.md:61`) does not apply to it. |
| Platform | Linux only; `once`, `check-config`, `init-state` exit 2 elsewhere. Network-FS deny-list for `state_dir`: nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p. |
| Non-goals | NG-1 push designs B/C/D; NG-2 no GitHub write (REST GET only; GraphQL POST only with a constant query without `mutation`); NG-3 no Project writes; NG-4 no session constraint beyond the deployment gate; NG-5 no daemon mode, no in-cycle retry, no automatic Orca retry. |
| Intended owner | Candidate 1: assignee set exactly {own login} (OD-3), stricter than the claim's own rule. |
| Project unreadable | Fail closed, no label-only mode (OD-4). |
| Open decisions OD-1..OD-11 | Taken at their recommended defaults; every [PROPOSAL] value is listed in section 14. |
| Refactor-log notes | PF-016 kept: a prompt `ValueError` is still recorded as pre-pending `failed` and retried. PF-019 kept: the launcher Protocol stays as the test seam. PF-047 kept: runbook steps 3, 7, 9 stay separate. PF-031 deferred to FU-11, PF-048 deferred to FU-12. |

## 3. Corrections to the issue text and earlier notes

Each row was checked against the code on this branch. "Assumed" is what the issue text, the brainstorm notes or the spec implied; "Actual" is what the code says; "Design consequence" is how this document absorbs it. These rows are also the list of code-versus-spec differences reported at hand-off.

| # | Assumed | Actual (verified) | Design consequence |
|---|---|---|---|
| C1 | The poller can reuse a GitHub CLI wrapper in `superclaude.pr_submit.ci` | `src/superclaude/pr_submit/ci.py` is a pure classifier (`classify_checks` line 25; `_evidence_is_zero` line 58); nothing under `pr_submit` runs a subprocess. | `issue_watch.runner` is new. `_evidence_is_zero` is only the precedent for an int-not-bool check (FR-012). |
| C2 | `_find_orca` can be imported and injected | `src/superclaude/cli/install_user_setup.py:198-221` `_find_orca() -> str \| None` is private, takes no argument, and calls `shutil.which` and `subprocess.run` directly (timeout 10 at line 213; caught exceptions at line 217; `orca-cli` topic check at line 219). | `launch.find_orca(runner, which)` mirrors it with injected seams. `_ORCA_CLIS` (line 35) is imported, not copied. `test_find_orca_parity.py` drives the original by monkeypatching `shutil.which` and `subprocess.run` and checks both agree. |
| C3 | `parse_origin_url` is an importable helper | It lives in a skill script, `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py:86-99`, not in an importable package. Its regexes (lines 65-69) match `github.com` case-sensitively; only `check_claim` (line 102) compares owner/repo case-insensitively. `read_origin` (lines 156-174) runs `git remote get-url origin` with no `-C` and no timeout. | `launch.parse_origin` mirrors the parse rules. The poller runs `git -C <abs worktree> remote get-url origin` with a timeout and compares the parsed `owner/repo` case-insensitively with `ironbellyorg/ironclaude`. `test_origin_parity.py` loads the script with `importlib.util.spec_from_file_location` and checks both parsers on one table. |
| C4 | `write_prepared_bytes` gives full crash safety and the file modes | `src/superclaude/cli/swarm/atomic.py:14` `write_prepared_bytes(path: Path, data: bytes) -> int` writes a same-directory `mkstemp` file, fsyncs it and `os.replace`s it; it does not fsync the directory, does not chmod, and needs the parent to exist. | `record` calls it, then fsyncs the state directory itself (NFR-011). `mkstemp` already creates 0600. `init-state` creates the directory with mode 0700. |
| C5 | Paging can reuse `fetch_rest` as-is | `sc-pr-submit-protocol/scripts/poll-augment-review.sh:48-77` uses a 1000-page cap and the argv order `gh api <path> --method GET -F per_page=100 -F page=N`. | Only the paging rule is reused: a page under 100 ends the read, a repeated id fails, the read must complete. The 5-page cap and the argv order `gh api --method GET <path> ...` are the poller's own (spec section 3). |
| C6 | The claim and the watcher share one owner rule | `src/superclaude/skills/sc-issue-protocol/refs/claim.md:41-42`: another assignee means STOP, self-assigned means continue, and an unassigned issue is accepted (the claim then runs `--add-assignee @me`, line 47). | `predicates.is_intended_owner` is a strict subset: exactly {own login}. Confirms PF-001. |
| C7 | The claim reads the own login with `--include` | `claim.md:26` uses `gh api user -q .login`, no headers. | The `gh api user --include` header parse (status line, headers, blank line, JSON body) is the poller's own. Its exact output shape is UNVERIFIED (section 15). |
| C8 | `make lint` and `make lint-architecture` are separate gates | `Makefile:48` `lint: lint-architecture`, then `uv run ruff check .` (line 50). | Gate list in section 13 notes that `make lint` already runs `lint-architecture`. |
| C9 | The architecture lint checks import layers | `src/superclaude/tools/arch_lint.py` has three rules only: rebinding a `contracts.__all__` name (lines 164-186), a string literal equal to an `ID_PATTERNS` body (188-209, docstrings skipped), and redefining a canonical class (211-228). `Makefile:467-476` (Check 11) scans `src/superclaude/cli/`. | The NFR-014 dependency rules need a new AST test, `tests/issue_watch/test_module_boundaries.py`. The package must not rebind `ID_PATTERNS`, `THRESHOLDS` or any other `contracts.__all__` name and must not contain an `ID_PATTERNS` body literal such as `FR-\d+(?:\.\d+)?` (`contracts/__init__.py:64-77`). None of the poller's regexes collides. |
| C10 | A make target checks formatting | No make target runs `ruff format --check`; `make format` (Makefile:53-55) rewrites files. CI runs `ruff format --check src/ tests/` (`.github/workflows/test.yml:106`) with `ruff==0.15.20` (`pyproject.toml:54`). | The gate list adds `uv run ruff format --check src/ tests/`. |
| C11 | Tests run serially | CI runs pytest with `-n auto` (xdist, `test.yml:47`). | Every test uses `tmp_path`, `monkeypatch.setenv` and no shared global state; the two-process lock test uses its own state directory. |
| C12 | New pytest markers can be added freely | `pyproject.toml:114` sets `--strict-markers`. | No new marker. The existing `property_based` marker (`pyproject.toml:135`) may tag the NFR-001 property test. |
| C13 | The spec's gate list is complete | CI also runs `make verify-deps` (`test.yml:123`), `make lint-architecture` (135) and the format check (106). | Section 13 lists them. |
| C14 | `tests/issue_watch/test_cli.py` can sit in a package-less folder | `tests/cli_portify/test_cli.py` already exists; same basenames in two rootless folders collide under pytest's default import mode. | `tests/issue_watch/__init__.py` is required (as `tests/pr_submit/__init__.py`). |
| C15 | A property-testing library is available | `hypothesis` is not a dependency: `pyproject.toml` mentions it only in the `property_based` marker text (line 135). NFR-012 forbids a new dependency. | The NFR-001 property test is a table-plus-generator test over a fixed hostile corpus and seeded `random` strings, not `hypothesis`. |
| C16 | Orca's retry flag and unknown-outcome code are documented in the repo | `--retry-launch`, `agent_session_operation_unknown` and the launch reply JSON appear nowhere in the repository; it documents only `agent launch` and `--surface terminal` (`src/superclaude/core/CLAUDE.md:48-50`). `--retry-launch` is in the Orca 1.4.245 help. | The error code and reply JSON are UNVERIFIED (section 15), modelled by `_assumed_shape` fixtures, confirmed by FU-1. |
| C17 | The poller could live next to other CLI code as `select.py` or `filters.py` | No `issue_watch` or `issue-watch` name exists anywhere in the repo; a module named `select` would shadow the standard library module. | Module names follow NFR-014: `predicates.py`, `record.py`; no `select`. |
| C18 | Importing `write_prepared_bytes` is free of side effects | `import superclaude.cli.swarm.atomic` first runs `swarm/__init__.py`, which loads click and the `swarm.commands` tree. | Accepted (both are already loaded by `main.py`); `record` imports it lazily inside `save` so `status` and the unit tests of pure functions stay light. |
| C19 | `_find_orca` rejects every malformed topic list | `install_user_setup.py:219` sits outside the `try`, so a topic list holding a non-dict raises an uncaught `AttributeError`. | `launch.find_orca` rejects a non-dict element; the parity test excludes that one input and pins the difference. |
| C20 | A retry is `<orca> agent launch --retry-launch op-1 --json` (FR-015) | `orca agent launch --help` (1.4.245): re-issue "the same command from the same directory on the same host with --retry-launch <operationId>". | `status` prints the full original argv plus `--retry-launch <id>`, with `cwd` (section 10.2). |
| C21 | `--method GET` is style | `gh api --help` (2.103.3): the method becomes POST when parameters are added with `-F`/`-f`. | `--method GET` is mandatory on every G2 to G7 argv; a test rejects any `-F` argv without it. |
| C22 | `Retry-After` is readable on every rate-limited reply | Only G1 uses `--include`; G2 to G7 return bodies and stderr only. | A per-issue rate limit always clamps to 3600 s with `rate_limit_clamped` (FR-028). |
| S1 | FR-016's GWT, read literally, reaches a second candidate after a launch | FR-016's own text: "a second eligible candidate is never reached". | Section 6.3: the text wins; after one launch the remaining candidates get no stamp and no decision line. |

## 4. Command interface

### 4.1 Verbs (FR-026)

The Click group is `issue_watch_group`, exposed as `superclaude issue-watch`. Every verb takes `--config <path>` (default `~/.config/superclaude/issue-watch.json`); the spec names it for `once` (spec section 8) and the other verbs need the same file to find `state_dir`. There is no flag-only interface: labels, `project_id`, worktree, approvers file and `state_dir` come only from the config.

| Verb | Flags | Lock | Writes | External calls | Exit codes it can return |
|---|---|---|---|---|---|
| `once` | `--dry-run`, `--config <path>` | Non-blocking `flock`, whole cycle | `dispatch.json` (not in dry-run), `audit.jsonl`, `dry-run.json` (dry-run only) | `gh`, `git`, Orca probe, Orca launch (not in dry-run) | 0, 2, 3, 4, 5, 6, 7, 75 |
| `status` | `--json`, `--config <path>` | None (read-only) | None; no file's mtime changes (FR-021) | None | 0 healthy, 1 unhealthy (age above 900 s or no qualifying cycle), 2 config invalid, 6 store unreadable |
| `check-config` | `--config <path>` | None | None | None | 0 valid, 2 invalid or platform unsupported or network-FS `state_dir` |
| `init-state` | `--config <path>` | Creates it | Creates `state_dir` (0700), `dispatch.json` (0600), `lock` (0600) | None | 0 created, 2 config or platform, 6 a store already exists or the directory is unwritable |
| `reset <N> --forfeit-guarantee` | `--config <path>` | Non-blocking `flock` | Removes entry N; appends its `consumed_at` to `consumed_log`; one audit line | None | 0 done, 2 usage (entry not `abandoned`/`unknown`, or flag missing), 6 store, 75 lock held |
| `reset --rate-limit` | `--config <path>` | Non-blocking `flock` | Clears `next_permitted_at`; one audit line | None | 0, 6, 75 |

`reset` with both `<N>` and `--rate-limit`, or with neither, is a usage error (exit 2). `reset <N>` without `--forfeit-guarantee` is a usage error. `reset <N> --forfeit-guarantee` prints, on success, that issue N may now be launched a second time. `status` exit 1 is this design's choice (the spec defines status content, not its code); it lets the FU-4 alert run `status` directly.

### 4.2 Configuration file (FR-027)

JSON, because Python 3.10 has no `tomllib` (`pyproject.toml:16` `requires-python = ">=3.10"`). Loaded by `cycle.load_config(path) -> Config`; validated by the same function `check-config` uses.

| Field | Type | Required | Default | Validation (failure gives exit 2, `config_invalid` unless noted) |
|---|---|---|---|---|
| `schema_version` | int | yes | none | Equals `1` |
| `enabled` | bool | no | `false` | A JSON boolean; `false` makes `once` exit 0 `not_enabled` before any external call |
| `labels.trigger` | string | no | `issue-watch:trigger` | Non-empty, at most 50 characters, no control characters; matched exact and case-sensitive |
| `labels.approval` | string | no | `issue-watch:approved` | As above, and different from `labels.trigger` |
| `project_id` | string | yes | none | Matches `^PVT_[A-Za-z0-9_-]{1,64}$` [PROPOSAL; Projects v2 node-id prefix is UNVERIFIED, FU-3] |
| `owner_account_id` | int | no | absent | If present, an `int` (not `bool`) in 1..10^20−1; a mismatch with `gh api user` `.id` is exit 2 `account_id_mismatch` at cycle time |
| `worktree` | string | yes | none | Absolute path, existing directory (`worktree_invalid`) |
| `approvers_file` | string | yes | none | Absolute path; file rules below (`approvers_invalid`) |
| `state_dir` | string | no | `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` | Absolute after expansion; not on a deny-listed filesystem (`state_dir_unwritable` is exit 6 only when writing fails; a network FS is exit 2 `config_invalid`) |

Unknown keys are rejected (exit 2), so a typo such as `enable` cannot silently leave the poller on its default. Timeouts, caps and the lease are module constants, not config (section 14): the spec makes them [PROPOSAL] values for the owner to confirm after the shadow run, not operator knobs.

**Approvers file rules (FR-027, T13).**

| Rule | Check |
|---|---|
| Exists and is a regular file | `os.lstat` then `stat.S_ISREG`; a symlink is rejected |
| Owned by the effective UID | `st_uid == os.geteuid()` |
| Not group- or other-writable | `st_mode & (stat.S_IWGRP \| stat.S_IWOTH) == 0` |
| Content | One ID per line matching `^[1-9][0-9]{0,19}$`; lines that are blank or start with `#` are ignored; any other line makes the file invalid |
| Non-empty | At least one ID after filtering; duplicates collapse into a `frozenset[int]` |

`check-config` prints the file's mtime (UTC ISO 8601) and the entry count (R10), and nothing else about its content.

### 4.3 Exit codes (spec section 8)

| Code | Meaning | Reasons that produce it |
|---|---|---|
| 0 | Cycle complete (any number of launches), `disabled`, `disabled_mid_cycle`, `not_enabled` | `cycle_complete`, `disabled`, `disabled_mid_cycle`, `not_enabled`; every skip reason |
| 1 | An unexpected exception out of the cycle, written by `once` only ([PROPOSAL]) | `cycle_crashed` |
| 2 | Usage, config, platform, origin, Orca probe | `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` |
| 3 | GitHub auth, scope, timeout, non-JSON | `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` |
| 4 | Discovery truncated or duplicated | `truncated`, `discovery_duplicate` |
| 5 | Rate limited | `rate_limited`, `rate_limit_clamped` |
| 6 | Store or lock | `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` |
| 7 | An entry was written `failed`, `unknown` or `abandoned` `spawn_error` this cycle | `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` |
| 75 | Lock held or the lock inode changed | `lock_held` |

**Precedence (OD-10).** When several conditions hold, the cycle exits with the first of 2, 6, 7, 5, 3, 4. In practice most are mutually exclusive because each voids the cycle at once; the combinations that can occur are 7 with 5 (a `failed` entry was written, then a later read is rate limited: exit 7, both audited) and 7 with 3 (a `failed` entry, then a shared read times out: exit 7). Exit 75 applies only when the lock was not taken, or its inode changed, and nothing else ran. Precedence is computed by one pure function, `cycle.resolve_exit(conditions: frozenset[int]) -> int`.

## 5. Component architecture

### 5.1 Module diagram

```text
                       superclaude.cli.main  (registers issue_watch_group after reflect, line 561)
                                   |
                                   v
 +-----------------------------  cli.py  ------------------------------+
 | Click group + 6 verbs; maps CycleResult -> sys.exit code; no logic  |
 +---------------------------------------------------------------------+
            |                        |                         |
            v                        v                         v
 +--------------------+   +---------------------+   +--------------------+
 | cycle.py           |   | record.py           |   | audit.py           |
 | Config, Clock,     |-->| Store Protocol,     |   | AuditLog: append,  |
 | run_cycle(),       |   | FileStore, Lock,    |   | rotate, stderr     |
 | resolve_exit(),    |-->| transitions, sweep, |   | fallback, reason   |
 | budget + deadline  |   | DISABLED, migrate   |   | enum               |
 +--------------------+   +---------------------+   +--------------------+
   |        |      |                 |
   |        |      +-----------------|------------------------------+
   v        v                        v                              v
 +-----------------+   +------------------------+   +------------------------------+
 | github.py       |   | predicates.py          |   | launch.py                    |
 | typed reads:    |-->| frozen dataclasses +   |   | build_claim_prompt,          |
 | user, discovery,|   | pure Section 3 checks, |   | find_orca(runner, which),    |
 | events, issue,  |   | CLAIM_MARKER,          |   | parse_origin, check_origin,  |
 | comments, items;|   | is_intended_owner      |   | Launcher Protocol,           |
 | paging, rate    |   +------------------------+   | OrcaLauncher, ORCA_AGENT     |
 | limits, budget  |                                 +------------------------------+
 +-----------------+                                          |
        |                                                     |
        v                                                     v
 +------------------------------------------------------------------------+
 | runner.py: Runner Protocol, SubprocessRunner (argv list, shell=False,  |
 | timeout, stdin=DEVNULL, 500-byte stderr cap), CommandResult            |
 +------------------------------------------------------------------------+
        |
        v
   gh  /  git  /  orca-ide | orca      (subprocess; stubs on PATH or FakeRunner in tests)

 External reuse:  record.py   -> superclaude.cli.swarm.atomic.write_prepared_bytes
                  launch.py   -> superclaude.cli.install_user_setup._ORCA_CLIS
```

### 5.2 Responsibilities

| Module | Owns | Never does |
|---|---|---|
| `runner.py` | `CommandResult` dataclass; `Runner` Protocol; `SubprocessRunner.run(argv, timeout)` which rejects a `str` argv with `TypeError`, runs `subprocess.run(list, shell=False, capture_output=True, text=True, timeout=t, stdin=DEVNULL)`, truncates stderr to 500 bytes (T11), and maps `TimeoutExpired` to `CommandResult(timed_out=True)` and `OSError` to `CommandResult(spawn_error=...)` | Parse JSON; know about `gh` |
| `github.py` | Builds every `gh` argv from module constants (section 8); runs it through the runner with a timeout supplied by the cycle; parses JSON; follows paging; classifies replies into `ok`, `timeout`, `non_json`, `auth_failed`, `scope_missing`, `rate_limited`, `transient` (5xx), `failed`; counts calls against the per-cycle `CallBudget` | Decide eligibility; write state; read title, body or comment text |
| `predicates.py` | Frozen dataclasses (`Login`, `DiscoveredIssue`, `LabelEvent`, `IssueSnapshot`, `ProjectItem`, `MarkerEvidence`, `EditEvidence`); pure functions for each Section 3 definition; `CLAIM_MARKER`; `is_intended_owner`; `approval_of(events, ...) -> ApprovalResult`; `eligibility_order(...)` | Any I/O or clock read; every time is a parameter |
| `record.py` | `Store` Protocol; `FileStore` (load, validate, migrate, save); `Lock` (open with `O_NOFOLLOW`, `flock`, inode check); `Entry` and `StoreDoc` dataclasses; one function per section 7 transition row; `sweep(store, now)`; `day_cap_count(store, now)`; `disabled_present(state_dir)`; `init_state(state_dir, now)` | Run commands; read the wall clock |
| `launch.py` | `ORCA_AGENT` constant; `build_claim_prompt(n)`; `find_orca(runner, which)`; `parse_origin(url)`; `check_origin(runner, worktree, timeout)`; `Launcher` Protocol; `OrcaLauncher.launch(...) -> LaunchOutcome` | Write state (it returns an outcome; the cycle writes) |
| `audit.py` | `AuditLog.append(line)` (one `os.write` on an `O_APPEND` fd), `AuditLog.rotate_if_needed()` (called only by a lock holder), `stderr_fallback(line)`; the `REASONS` frozenset with kind and exit per reason; line builders `cycle_line(...)`, `decision_line(...)`, `warning_line(...)` | Contain issue text (the builders accept only typed scalar fields) |
| `cycle.py` | `Config` and `load_config`; `validate_approvers`; `Clock` Protocol and `SystemClock`; `Deadline` (240 s, 5 s floor, 120 s launch cutoff); `run_cycle(deps, dry_run) -> CycleResult`; `resolve_exit`; `status_report(store, audit, now)`; the NFR-013 reducer `slo_numbers(lines, store, now)` | Call `subprocess` directly |
| `cli.py` | `issue_watch_group` and its verbs; builds the real `Deps` (runner, store, launcher, clock); prints `status`; translates `CycleResult.exit_code` to `sys.exit` | Business logic |

`slo_numbers` lives in `cycle.py` because NFR-014 fixes the module list; it is a pure reducer and needs no extra verb (the spec asks for "a helper", not a command).

### 5.3 Dependency rules (NFR-014)

Allowed intra-package imports. Anything not listed is forbidden; `tests/issue_watch/test_module_boundaries.py` walks each module's AST and fails on any other `superclaude.*` import.

| Module | May import from the package | May import from elsewhere in `superclaude` | Third-party |
|---|---|---|---|
| `runner` | none | none | none |
| `predicates` | none | none | none |
| `audit` | none | none | none |
| `github` | `runner`, `predicates` | none | none |
| `record` | `predicates` (types only, for `Entry` fields that hold an issue number) | `superclaude.cli.swarm.atomic` | none |
| `launch` | `runner` | `superclaude.cli.install_user_setup` (`_ORCA_CLIS` only) | none |
| `cycle` | `runner`, `github`, `predicates`, `record`, `launch`, `audit` | none | none |
| `cli` | `cycle`, `record`, `audit`, `launch`, `runner` | none | `click` (already a dependency, `pyproject.toml` dependencies) |

Import cost note (verified): `superclaude.cli.swarm.atomic` itself imports only `os`, `tempfile` and `pathlib` (`swarm/atomic.py:7-11`), but importing it executes `swarm/__init__.py`, which imports `click` (line 90) and the whole `swarm.commands` tree (line 164). `install_user_setup` imports `install_hooks` (line 31), which uses only the standard library. Both costs are paid once per `once` process and are acceptable for a 5-minute batch job; the alternative (copying 25 lines of `write_prepared_bytes`) would contradict NFR-014's "reuses". `cli.py` imports the package lazily from `main.py`, so `superclaude --help` is unaffected beyond today's eager imports.

Arch lint: `src/superclaude/tools/arch_lint.py` has three rules only, constant rebinding (lines 164-186), ID-pattern literal duplication (188-209) and class shadowing (211-228), all keyed to `superclaude.contracts.__all__`. No proposed name (`CLAIM_MARKER`, `ORCA_AGENT`, `REASONS`, `Store`, `Entry`, `Lock`) is in that `__all__` (`contracts/__init__.py:302-313`), and no proposed regex literal equals an `ID_PATTERNS` body (`contracts/__init__.py:64-77`). The lint therefore passes without an `# arch-lint: allow-duplicate` marker. It enforces no import layering, which is why the boundary test above exists.

### 5.4 Protocols and seams

Exactly four Protocols, as NFR-014 fixes. Signatures only.

```text
runner.py
  @dataclass(frozen=True)
  class CommandResult:
      argv: tuple[str, ...]
      returncode: int | None          # None when timed_out or spawn_error
      stdout: str
      stderr: str                     # at most 500 bytes
      timed_out: bool
      spawn_error: str | None         # OSError class name, never its message text
      duration_s: float

  class Runner(Protocol):
      def run(self, argv: list[str], timeout: float) -> CommandResult: ...

record.py
  class Store(Protocol):
      state_dir: Path
      def load(self) -> StoreDoc: ...                  # raises StoreError(reason)
      def save(self, doc: StoreDoc) -> None: ...       # atomic + dir fsync
      def lock(self) -> AbstractContextManager[None]:  # raises LockHeld / LockError(reason)
      def disabled(self) -> bool: ...
      def disabled_since(self) -> datetime | None: ...

launch.py
  class Launcher(Protocol):
      def launch(self, orca: str, worktree: Path, prompt: str,
                 timeout: float) -> LaunchOutcome: ...

  @dataclass(frozen=True)
  class LaunchOutcome:
      kind: Literal["launched", "unknown", "spawn_error"]
      operation_id: str | None
      detail: str                     # one of a fixed set: "exit_nonzero", "timeout", ...

cycle.py
  class Clock(Protocol):
      def now(self) -> datetime: ...                   # tz-aware UTC
      def monotonic(self) -> float: ...
```

| Seam | Production value | Test value | Used by |
|---|---|---|---|
| `Runner` | `SubprocessRunner()` | `FakeRunner(script: dict[tuple[str, ...], CommandResult \| Callable])`; any argv not in the script returns `returncode=99` and is recorded as unexpected (NFR-005) | `github`, `launch.find_orca`, `launch.check_origin`, `OrcaLauncher` |
| `Store` | `FileStore(state_dir)` | `FileStore(tmp_path)` (real files) or `CrashingStore` that raises at the k-th write (crash injection) | `cycle`, `cli` |
| `Launcher` | `OrcaLauncher(runner)` | `RecordingLauncher(outcomes)`; or the real `OrcaLauncher` over a `FakeRunner` | `cycle` |
| `Clock` | `SystemClock()` | `FakeClock(start, step)` with `advance(seconds)` | `cycle` (passes `now` into `record` and `predicates`) |
| `which` | `shutil.which` | a dict lookup | `launch.find_orca` |
| `Deps` bundle | `cli.build_deps(config)` | constructed directly in tests | `cycle.run_cycle(deps: Deps, dry_run: bool) -> CycleResult` |

`Deps` is a frozen dataclass (`runner`, `store`, `launcher`, `clock`, `audit`, `config`, `which`, `host`), not a Protocol. `host` is `socket.gethostname()` in production and a constant in tests.

## 6. Poll cycle

### 6.1 Sequence (non-dry-run, one launch)

```text
cron     cli        cycle          record/Store     github(gh)        launch(git/orca)    audit
 |  once  |            |                 |                |                   |              |
 |------->| load_config, platform, enabled, approvers, worktree (no external call)          |
 |        |--run_cycle->|                |                |                   |              |
 |        |            |--lock()-------->| flock NB, O_NOFOLLOW, inode check  |              |
 |        |            |--disabled()---->|                |                   |              |
 |        |            |--load()-------->| validate/migrate; next_permitted_at |              |
 |        |            |--user()------------------------->| gh api user --include (call 1)   |
 |        |            |--check_origin()------------------------------------->| git -C       |
 |        |            |--sweep(now)---->| pending->abandoned; lease report  |              |
 |        |            |--discover()--------------------->| gh issue list (call 2)           |
 |        |            | order candidates (considered map), local checks      |              |
 |        |            |  per candidate (<= 10):          |                   |              |
 |        |            |--events/comments/edits/items---->| GET pages (cap 35 incl. 3 reserved)
 |        |            |  first eligible candidate:       |                   |              |
 |        |            |--find_orca() (cached)------------------------------->| skills list  |
 |        |            |--build_claim_prompt(n)           |                   |              |
 |        |            |--re-read issue/events/items----->| 3 reserved calls  |              |
 |        |            |--day_cap_count(now)------------->|                   |              |
 |        |            |--disabled()---->|                |                   |              |
 |        |            |--check_origin() (not cached)------------------------>| git -C       |
 |        |            |--save(pending)->| launches=1, consumed_at, fsync     |              |
 |        |            |--launch()------------------------------------------->| orca agent launch
 |        |            |--save(launched|unknown|abandoned, considered)->|     |              |
 |        |            |--append decision lines, cycle line, rotate_if_needed----------------->|
 |        |<-CycleResult(exit)                               |                   |              |
 |<-exit--|            | lock released on context exit     |                   |              |
```

### 6.2 Steps

Each step lists the external calls it may make and its failure exit. "Stop" means: write any entry already decided, append the cycle line, release the lock, exit.

| # | Step | Calls | On failure | FR |
|---|---|---|---|---|
| 1 | Platform check (`sys.platform == "linux"`), `load_config`, `enabled` (skipped in dry-run), `validate_approvers`, worktree absolute and a directory, network-FS check of `state_dir` via `/proc/self/mountinfo` | 0 | 2 (`platform_unsupported`, `config_invalid`, `approvers_invalid`, `worktree_invalid`); `enabled: false` exits 0 `not_enabled` | FR-001, FR-027, FR-013 |
| 2 | `store.lock()` | 0 | 75 `lock_held` (held, or inode changed); 6 `lock_missing`/`lock_invalid` | FR-017 |
| 3 | `store.disabled()` | 0 | 0 `disabled` | FR-018 |
| 4 | `store.load()`; migrate lower version; check `next_permitted_at` | 0 | 6 `store_missing`/`store_invalid`; 5 `rate_limited` if now < `next_permitted_at` | NFR-011, FR-028 |
| 5 | `github.user()`: login, id, `Date` header; login regex; `owner_account_id` compare; record skew | 1 | 3 `gh_auth_failed`/`gh_timeout`/`gh_non_json`/`login_invalid`; 2 `account_id_mismatch`; 5 on rate limit | FR-002 |
| 6 | `launch.check_origin(worktree)` | 1 git | 2 `origin_mismatch` | FR-025 |
| 7 | `record.sweep(store, now)`: every `pending` -> `abandoned` `pending_orphan`; every `launched` past `lease_expires_at` -> `abandoned` `claim_not_observed` (dry-run: report only) | 0 | none | Section 7 |
| 8 | `github.discover(login)` | 1 | 3; 4 `truncated`/`discovery_duplicate`; 5; warning at >= 80 | FR-003, FR-004 |
| 9 | Order candidates: never-examined first (ascending number), then by `considered[n]` ascending; drop to `max_candidates` | 0 | none | FR-023 |
| 10 | Per candidate, local checks: entry state (`already_dispatched`, `in_backoff`), day cap (`day_cap`) | 0 | skip | Section 3 Eligible, FR-024 |
| 11 | Per candidate, GitHub checks in order: marker (for every entry state that can reach `claimed`), approval events, edit timestamps, `projectItems` | 1 to 3 per read type, paged | skip with reason; 3 `project_read_failed` on missing scope; 5 on rate limit; `budget_exhausted` when the next read would breach 32 (35 minus 3 reserved) | FR-005 to FR-009, FR-022, NFR-009 |
| 12 | First fully eligible candidate: `find_orca` (cached), `build_claim_prompt`, re-read, day cap, DISABLED, origin re-check, `pending` write, spawn | probe 1 to 2; re-read 3; git 1; orca 1 | probe: 2 `orca_not_found`; prompt: `failed` `prompt_invalid`; re-read: `revalidation_failed` or `failed` `revalidation_transient`; DISABLED: 0 `disabled_mid_cycle`; origin: 2; launch outcome per section 8.4 | FR-010 to FR-014 |
| 13 | Final `store.save`: outcome entry, `considered` stamps (every examined candidate except `budget_exhausted`), pruned to the discovery set | 0 | 6 `state_dir_unwritable` | FR-023 |
| 14 | Health stamp: only an exit-0 cycle that is not DISABLED, `not_enabled`, `disabled_mid_cycle` or dry-run writes `last_completed_cycle_at` | 0 | none | FR-021 |
| 15 | Audit: decision lines, then the cycle line; `rotate_if_needed` before the first append (lock held) | 0 | stderr fallback | FR-020 |

`last_completed_cycle_at` is a store field this design adds (section 7.2) so `status` need not read the audit tail; it rides the step-13 save. `disabled_since` is the `DISABLED` mtime, read with `os.stat`.

Dry-run differences: step 1 ignores `enabled`; steps 7, 12 and 13 compute but do not write `dispatch.json`; step 12 stops before `find_orca` and reports `probe: skipped` and `would_launch: <n>`; the shadow `considered` map and shadow launch timestamps go to `dry-run.json` in step 13; step 14 is skipped; every line carries `"dry_run": true`.

### 6.3 Quantity flow

| Stage | Count in | Count out | Bound |
|---|---|---|---|
| Discovery reply | 0..99 issues (100 or more is exit 4) | same, de-duplicated (a duplicate is exit 4) | 1 call |
| Owner pre-filter | n | n (discovery already filters by `--assignee`; `is_intended_owner` re-checks) | 0 calls |
| Candidate ordering | n | min(n, 10) | `max_candidates` 10 |
| Local checks | k | k' (minus `already_dispatched`, `in_backoff`, `day_cap`) | 0 calls |
| GitHub checks | k' | eligible set E, examined until the first eligible | 32 calls (35 minus 3 reserved) |
| Launch | first of E | 0 or 1 | `max_launches_per_cycle` 1; day cap 6 per rolling 24 h |
| Re-read | 1 | 0 or 1 | 3 reserved calls |

Calls per cycle:

| Case | Shared calls | Per-issue calls | Total | Per hour at 12 cycles | Share of 5,000/h |
|---|---|---|---|---|---|
| Idle (no trigger issues) | 2 (`api user`, discovery) | 0 | 2 | 24 | 0.48% |
| Worst | 2 | 35 (32 for checks plus 3 re-read) | 37 | 444 | 8.88% |
| W workspaces on one login | ×W | ×W | ×W | ×W | ×W |

Orca probe calls (`skills list --json`) and `git` calls do not use the GitHub allowance and are not in the 35-call cap; they are bounded by the cycle deadline (section 8.4). Examined candidates in a cycle: k = min(10, floor((35 − 3) / r)) where r is the per-candidate read count (FR-016 GWT). With one page per read and r = 4 (marker, events, edit timestamps, items), k = min(10, 8) = 8.

"Examined" stops at the first eligible candidate: after the launch, and after any launch-step outcome, later candidates are neither read nor stamped (FR-016, PF-029). A candidate skipped locally (step 10) is stamped, because it was examined.

**Spec tension resolved here (S1).** FR-016's GWT says cycle 1 with 15 eligible issues "examines k and launches 1"; the same requirement says "a second eligible candidate is never reached". This design keeps the safety sentence: k bounds a cycle in which every candidate skips. The FR-016 test has two cases: (a) 15 issues that all skip on a GitHub check: cycle 1 examines k, cycle 2 starts with the 15 − k unexamined; (b) 15 eligible: cycle 1 examines 1 and launches 1. Owner question Q1 (section 16).

## 7. Dispatch record

### 7.1 Files in `state_dir`

| File | Mode | Created by | Written by | Read by |
|---|---|---|---|---|
| `state_dir/` | 0700 | `init-state` (`os.makedirs(mode=0o700)`, then `os.chmod` to defeat umask) | none | all verbs |
| `dispatch.json` | 0600 | `init-state` | `once` (not dry-run), `reset` | `once`, `status`, `reset` |
| `lock` | 0600 | `init-state` (`O_CREAT \| O_EXCL \| O_NOFOLLOW`) | nobody (only `flock`ed) | `once`, `reset` |
| `audit.jsonl`, `.1`..`.4` | 0600 | first append (`O_CREAT \| O_APPEND`, mode 0600) | every exit of `once` and `reset` | `status`, the SLO reducer |
| `dry-run.json` | 0600 | first dry-run | `once --dry-run` only | `once --dry-run` only |
| `DISABLED` | operator's choice | operator (`touch`) | nobody | `once`, `status` |

### 7.2 Store schema (`dispatch.json`, `schema_version` 1)

```text
{
  "schema_version": 1,                      # int; > 1 or not int -> exit 6 store_invalid
  "created_at": "2026-11-07T15:00:00Z",     # set once by init-state; approval floor (Section 3 (d))
  "next_permitted_at": null | "<UTC>",      # FR-028; cleared by reset --rate-limit
  "last_completed_cycle_at": null | "<UTC>",# design addition for FR-021 (section 6.2 step 14)
  "considered": { "<issue>": "<UTC>" },     # FR-023; keys are decimal strings (JSON object keys)
  "consumed_log": [ "<UTC>", ... ],         # FR-024; consumed_at of reset entries, pruned after 24 h
  "entries": { "<issue>": Entry }           # one per issue number
}
```

Entry (every field always present; absent values are `null`):

| Field | Type | Set when | Mutable |
|---|---|---|---|
| `issue` | int 1..999999999 | entry created | no |
| `state` | `pending` \| `launched` \| `unknown` \| `failed` \| `abandoned` \| `claimed` | each transition | yes |
| `attempts` | int >= 0 | +1 on each pre-pending `failed` | yes (never reset except by entry removal) |
| `launches` | int 0 or 1 | +1 in the `pending` write | only by `reset` (entry removal) |
| `operation_id` | str \| null | `launched`, or `unknown` when Orca's reply carried one | yes |
| `approver_id` | int \| null | `pending` write, `claimed` from marker | yes (latest approval) |
| `approval_event_id` | int \| null | as above | yes |
| `approved_at` | UTC \| null | as above | yes |
| `launch_cwd` | absolute path str \| null | `pending` write | no |
| `launch_login` | str \| null | `pending` write | no |
| `launch_account_id` | int \| null | `pending` write | no |
| `consumed_at` | UTC \| null | `pending` write | no (immutable, FR-024) |
| `pending_at` | UTC \| null | `pending` write | no |
| `created_at` | UTC | entry created | no |
| `updated_at` | UTC | every write of this entry | yes |
| `lease_expires_at` | UTC \| null | `launched` (now + 60 min) | no after set |
| `last_reason` | reason from the closed enum | every write | yes |

Validation on load (`record.validate(doc) -> StoreDoc`, raising `StoreError("store_invalid")`): exact key set at both levels; types as above; `issue` equals its key; `launches` in {0, 1}; `launches == 1` implies `consumed_at` and `pending_at` non-null; `state == "failed"` implies `launches == 0`; every time string parses as an aware UTC datetime ending `Z`. Failure is exit 6 with the file untouched (NFR-011).

Migration: `record.MIGRATIONS: dict[int, Callable[[dict], dict]]` maps version v to a pure function producing v+1. Version 1 has no predecessor, so the dict ships empty and the migration path is exercised by a test-only v0 fixture registered through a test seam (`record.migrate(doc, migrations=...)`). A migrated store is saved under the lock before any other step.

`dry-run.json`:

```text
{ "schema_version": 1, "considered": { "<issue>": "<UTC>" }, "shadow_launches": [ "<UTC>", ... ] }
```

An unparseable `dry-run.json` is replaced with an empty shadow (it carries no safety meaning) and a warning line is written; a non-dry-run cycle never opens it.

### 7.3 State machine

```text
                      prompt ValueError / transient re-read
          (none) ------------------------------------------> failed --attempts=3--> abandoned(attempts_exhausted)
            |  \                                              |  ^ backoff elapsed: eligible again
            |   \ own marker newer than current approval      |  |
            |    +------------------------------------------> claimed <------------------+
            |                                                 ^   ^                       |
            | all checks passed               (failed: marker)|   | own marker newer      |
            v                                                 |   | than pending_at       |
          pending --exit 0 + non-empty op id--> launched -----+---+                       |
            |  \                                   | lease end, no marker                  |
            |   \--timeout/malformed/op_unknown/   v                                       |
            |      non-zero/no id--> unknown    abandoned(claim_not_observed) -------------+
            |                          |
            +--OSError before child--> abandoned(spawn_error)
            +--found at cycle start--> abandoned(pending_orphan)

  abandoned or unknown --reset N --forfeit-guarantee--> (entry removed; consumed_at -> consumed_log)
  claimed: terminal.   unknown: leaves only via claimed or reset (never on the lease).
```

### 7.4 Transitions (spec section 7, one function and one test each)

| # | From | Trigger | To | Field effects | Function |
|---|---|---|---|---|---|
| T-1 | (none) | `prompt_invalid` or `revalidation_transient` | `failed` | `attempts` 1, `launches` 0 | `record.fail(doc, n, reason, now)` |
| T-2 | `failed` | now >= `updated_at` + 10 min and `attempts` < 3 | eligible | none (re-runs every check) | `record.backoff_elapsed(entry, now)` |
| T-3 | `failed` | `attempts` reaches 3 | `abandoned` | `last_reason` `attempts_exhausted` | inside `record.fail` |
| T-4 | (none) or `failed` | all checks passed | `pending` | `launches` 1, `consumed_at`, `pending_at`, `launch_*`, approval fields | `record.mark_pending(doc, n, ctx, now)` |
| T-5 | `pending` | outcome `launched` | `launched` | `operation_id`, `lease_expires_at` | `record.mark_launched` |
| T-6 | `pending` | outcome `unknown` | `unknown` | `operation_id` if any | `record.mark_unknown` |
| T-7 | `pending` | outcome `spawn_error` | `abandoned` | `last_reason` `spawn_error` | `record.mark_spawn_error` |
| T-8 | `pending` | found by the sweep | `abandoned` | `last_reason` `pending_orphan` | `record.sweep` |
| T-9 | `launched` | now >= `lease_expires_at`, no marker | `abandoned` | `last_reason` `claim_not_observed` | `record.sweep` |
| T-10 | `launched`, `unknown`, `abandoned` | marker at or after `pending_at` − 300 s | `claimed` | `last_reason` `claimed` | `record.mark_claimed` |
| T-11 | (none) | marker after current approval | `claimed` | `launches` 0, `consumed_at` null | `record.mark_claimed` |
| T-12 | `failed` | marker after current approval | `claimed` | `launches` 0 | `record.mark_claimed` |
| T-13 | `abandoned`, `unknown` | `reset N --forfeit-guarantee` | removed | `consumed_at` appended to `consumed_log` if non-null | `record.reset_entry` |

Every function takes the document and `now` and returns a new `StoreDoc` (no in-place mutation), so a crash between computing and saving leaves the old file intact. Any other (state, trigger) pair raises `TransitionError`; `test_record.py` has one case per row plus a table-driven test that every other pair raises. T-10 on an `abandoned` entry whose `pending_at` is null (an `attempts_exhausted` tombstone) uses the current approval as the window floor, as T-12.

### 7.5 Lease, backoff, caps and windows

| Rule | Window or value | Half-open check (`now` from the clock) |
|---|---|---|
| Lease (reporting only) | 60 min after `launched` | expired iff now >= `lease_expires_at` |
| `failed` backoff | 10 min after `updated_at` | elapsed iff now >= `updated_at` + 10 min |
| Day cap | 6 in (now − 24 h, now] | count `t` with now − 24 h < t <= now over every entry's `consumed_at` and `consumed_log` |
| `consumed_log` pruning | drop t <= now − 24 h | done in every saving cycle and in `reset` |
| Marker window | at or after `pending_at` − 300 s; else after the current `approved_at` | `marker_time >= pending_at - 300s` |
| Clock skew warning | \|local now − `Date` header\| > 60 s | one `clock_skew` warning line |

The day-cap window is closed at `now` and open at `now − 24 h`, which is the same half-open rule written from the other side: a `consumed_at` exactly 24 h old no longer counts.

### 7.6 Atomic write and lock protocol

**Save** (`FileStore.save`): serialise with `json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=True).encode() + b"\n"`; call `write_prepared_bytes(state_dir / "dispatch.json", data)`; then `os.chmod(path, 0o600)`; then open `state_dir` with `os.open(dir, O_RDONLY | O_DIRECTORY)`, `os.fsync(fd)`, close. `write_prepared_bytes` already fsyncs the file and uses `tempfile.mkstemp`, whose files are created 0600, so the `chmod` is a guard against a pre-existing wider file, not the primary control (`swarm/atomic.py:22-35`). Sorted keys make "byte-identical" (FR-019) a stable property.

**Lock** (`FileStore.lock`):

| Step | Call | Failure |
|---|---|---|
| 1 | `fd = os.open(lock, O_RDWR \| O_NOFOLLOW \| O_CLOEXEC)` | `FileNotFoundError`: 6 `lock_missing`; `ELOOP` (symlink): 6 `lock_invalid`; `EISDIR`: 6 `lock_invalid` |
| 2 | `st = os.fstat(fd)`; require `S_ISREG` and `st_uid == geteuid()` | 6 `lock_invalid` |
| 3 | `fcntl.flock(fd, LOCK_EX \| LOCK_NB)` | `BlockingIOError`: 75 `lock_held` |
| 4 | `ps = os.stat(lock, follow_symlinks=False)`; require `(ps.st_dev, ps.st_ino) == (st.st_dev, st.st_ino)` and `os.fstat(fd).st_nlink > 0` | release; 75 `lock_held` |
| 5 | yield; on exit `flock(LOCK_UN)` and close | none |

Python's `os.open` raises `IsADirectoryError` for `O_RDWR` on a directory, and `OSError(ELOOP)` for `O_NOFOLLOW` on a symlink; the design maps both to `lock_invalid`. `reset` uses the same lock. `status` and `check-config` never take it.

**Write order within a launch** (crash points for NFR-005):

| Point | Durable state after a crash here | Next cycle |
|---|---|---|
| C1 before `pending` save | no entry (or `failed`) | re-evaluates normally; may launch once |
| C2 during `write_prepared_bytes` | old file (tmp unlinked or orphaned `dispatch.json.*.tmp`) | as C1; an orphaned tmp file is ignored |
| C3 after `pending` save, before spawn | `pending`, `launches` 1 | sweep makes it `abandoned` `pending_orphan`; no launch |
| C4 after spawn, before outcome save | `pending`, `launches` 1 | as C3 |
| C5 after outcome save, before audit | final state | no launch; the missing audit line is the only loss |

At no point can a rerun see `launches == 0` for an issue whose spawn may have started, which is the at-most-once argument.

## 8. External call contracts

### 8.1 GitHub argv (every one built by `github.py`, every one counted by `CallBudget`)

`R` below is the literal `IronbellyOrg/IronClaude`, a module constant `REPO`; `N` is a validated `int` rendered with `str(n)`; `P` is the page number 1..5.

| Id | Purpose | argv | Projection and fields | Paged | Cap slot |
|---|---|---|---|---|---|
| G1 | Own login (FR-002) | `gh api user --include` | parse the status line, headers, blank line, then JSON; keep `.login`, `.id`, header `Date` | no | shared |
| G2 | Discovery (FR-003) | `gh issue list --repo R --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | `number`, `labels[].name`, `assignees[].login`, `state` | no (`-L 100` with 100 as the fail-closed bound) | shared |
| G3 | Events (FR-005, FR-006, renamed check) | `gh api --method GET repos/R/issues/N/events -F per_page=100 -F page=P --jq EVENTS_JQ` | `EVENTS_JQ` = `[.[] \| {id, event, label: .label.name, actor_id: .actor.id, actor_login: .actor.login, actor_type: .actor.type, created_at}]` | REST pages | per issue |
| G4 | Claim marker (FR-009) | `gh api --method GET repos/R/issues/N/comments -F per_page=100 -F page=P --jq MARKER_JQ` | `MARKER_JQ` = `[.[] \| {id, login: .user.login, created_at, updated_at, marker: (.body \| contains("<!-- sc:issue:claim -->"))}]` | REST pages | per issue |
| G5 | Edit timestamps (Section 3 Unchanged) | `gh api graphql -f query=EDITS_QUERY -F number=N [-f after=<cursor>]` | issue `createdAt`, `lastEditedAt`; comments `nodes{databaseId author{login} createdAt lastEditedAt}`, `pageInfo{hasNextPage endCursor}` | GraphQL cursor | per issue |
| G6 | Project items (FR-007) | `gh api graphql -f query=PROJECT_ITEMS_QUERY -F number=N [-f after=<cursor>]` | `projectItems(first:100, after:$after){nodes{isArchived project{id} fieldValueByName(name:"Status"){... on ProjectV2ItemFieldSingleSelectValue{name}}} pageInfo{...}}` | GraphQL cursor | per issue |
| G7 | Re-read issue (FR-011) | `gh api --method GET repos/R/issues/N --jq REREAD_JQ` | `{number, state, labels: [.labels[].name], assignees: [.assignees[].login]}` | no | reserved |
| G3', G6' | Re-read events and items (FR-011) | as G3 and G6 | as above | as above | reserved |

Rules every GitHub argv follows:

- `--method GET` is written on every REST path call. `gh api --help` (gh 2.103.3) states the default method becomes POST once parameters are added, so `-F per_page=100` without it would be a POST (NG-2). `test_security_invariants.py` asserts that every recorded `gh api` argv other than G1 and `graphql` contains `--method GET`.
- Both GraphQL queries pass `owner` and `name` as literal strings inside the constant (`repository(owner:"IronbellyOrg", name:"IronClaude")`), so no `{owner}` placeholder and no `-f owner=` value exists. A test asserts no query constant contains `mutation` (NG-2) and every constant contains the literal repository.
- No argv names `title`, `body` or a comment body field as an output field. The only body access is `contains(<marker>)` inside `MARKER_JQ`, evaluated by `gh`'s embedded jq; the Python process receives a boolean (T1, NFR-002).
- `--jq` output of a REST page is still a JSON array of at most 100 items, so the page-length rule below works on the projection.
- Project ids are compared in Python (`project.id == config.project_id`); the id never enters an argv, so a hostile config value cannot alter a query.

`EDITS_QUERY` and `PROJECT_ITEMS_QUERY` field names follow the public GraphQL schema as the spec states them; their reply shapes are UNVERIFIED (FU-1, FU-3) and are pinned by `_assumed_shape` fixtures (section 12).

### 8.2 Paging, truncation and reply classification

Paging for G3 and G4 mirrors the rule of `fetch_rest` (`poll-augment-review.sh:48-77`), not its argv or its cap:

| Condition | Result |
|---|---|
| Page length < 100 | read complete |
| Page length = 100 | fetch page P + 1 |
| P would exceed 5 | `events_incomplete` (G3) or marker unknown (G4; never counts as claimed) |
| An `id` already seen on an earlier page (line 72's check) | incomplete |
| Reply not a JSON array, item missing a field, `id` not a positive int | `events_unreadable` / marker read failed |
| Budget would be exceeded before the next page | `budget_exhausted` (the candidate is not stamped) |

GraphQL (G5, G6) is complete only when `hasNextPage` is false; a repeated `endCursor` or an empty cursor with `hasNextPage` true is incomplete (mirrors lines 133-140). The cap is 5 pages per read.

`github.classify(result: CommandResult) -> Reply` maps every runner result before any field is read:

| Observation | Kind | Effect |
|---|---|---|
| `timed_out` | `timeout` | shared read: exit 3 `gh_timeout`; re-read: `failed` `revalidation_transient`; other per-issue read: skip with that read's reason |
| exit 0, stdout parses as JSON (G1 after the header block) | `ok` | continue |
| exit 0, stdout not JSON | `non_json` | shared: exit 3 `gh_non_json`; per-issue: skip |
| stderr contains `HTTP 401` or `gh auth login` | `auth_failed` | exit 3 `gh_auth_failed` |
| GraphQL `errors[].type == "INSUFFICIENT_SCOPES"` or stderr names `read:project` | `scope_missing` | exit 3 `project_read_failed` |
| stderr contains `HTTP 403` or `HTTP 429` together with `rate limit` (case-insensitive), or a GraphQL error of type `RATE_LIMITED` | `rate_limited` | exit 5 (FR-028) |
| stderr contains `HTTP 5` followed by two digits | `transient` | as `timeout` |
| anything else | `failed` | G1 or G2: exit 3 `gh_auth_failed` (FR-002's GWT maps a plain exit 1 to it); per-issue: skip with that read's reason |

The stderr substrings and the GraphQL error type names are UNVERIFIED (no repo code classifies `gh` stderr; `pr_submit/ci.py` classifies check rollups, not `gh` errors). They live in one table constant in `github.py` so the live test can correct them in one place.

### 8.3 Rate-limit time

`gh` without `--include` does not expose headers, so a rate-limited per-issue call yields no `Retry-After` value. `github.retry_after(result) -> int | None` reads it only when present (G1 is the one call with `--include`). The persisted time is:

| Input | `next_permitted_at` | Reason |
|---|---|---|
| `Retry-After: s`, 0 < s <= 3600 | now + s | `rate_limited` |
| `x-ratelimit-reset: epoch`, within 3600 s | that instant | `rate_limited` |
| larger, absent, or unparseable | now + 3600 s | `rate_limit_clamped` |

Absent is clamped, so a rate limit hit on any call other than G1 always waits the full hour. This is the conservative reading of FR-028 and is listed for the owner in section 16.

### 8.4 Orca contract

Probe (`launch.find_orca(runner, which) -> str | None`):

| Step | Detail |
|---|---|
| Candidates | `install_user_setup._ORCA_CLIS` (`orca-ide`, then `orca`), resolved with the injected `which` |
| argv | `[<path>, "skills", "list", "--json"]`, timeout min(10, remaining) |
| Accept | exit 0, stdout is a JSON object, `topics` is a list, and some element is a `dict` whose `name == "orca-cli"` |
| Reject | anything else, including a non-dict element (C19: the original raises there) |
| Cache | per cycle, in the `OrcaLauncher` instance |

`orca skills list --help` (Orca 1.4.245) confirms the probe "reads bundled guide metadata locally without contacting the Orca runtime" and prints "a topics array", so the probe is safe before any GitHub call.

Launch argv (FR-013), exactly 12 elements, built by `launch.launch_argv(orca, worktree, prompt) -> list[str]`:

```text
[orca, "agent", "launch", "--agent", ORCA_AGENT, "--worktree", "path:" + worktree,
 "--surface", "terminal", "--prompt", prompt, "--json"]
```

Every flag is listed by `orca agent launch --help` (Orca 1.4.245): `--agent`, `--worktree` with the `path:<path>` selector, `--surface chat|terminal`, `--prompt`, `--json`. The runner is called with `cwd=worktree` so a later operator retry from `launch_cwd` matches the help's rule "re-issue the same command from the same directory on the same host".

Outcome mapping (`LaunchOutcome.kind`):

| Child result | Kind | Entry |
|---|---|---|
| `OSError` raised by the runner before the child exists (`FileNotFoundError`, `PermissionError`) | `spawn_error` | `abandoned` `spawn_error` |
| `timed_out` (120 s) | `unknown` | `unknown` `launch_unknown` |
| exit 0, JSON object, operation id a non-empty `str` | `launched` | `launched`, `operation_id` |
| exit 0 without that id, non-JSON, non-zero exit, `agent_session_operation_unknown` anywhere in stdout or stderr | `unknown` | `unknown`, `operation_id` kept if one was parsed |

The JSON path of the operation id is UNVERIFIED: the help says the id comes "from the error" when a reply is lost and names `outcome.kind` and `receipt.detail` for success. `launch.OPERATION_ID_PATHS` is a tuple of candidate key paths, pinned by an `_assumed_shape` fixture until FU-1 records a real reply.

### 8.5 Timeouts and the deadline

`cycle.Deadline(clock, total=240)` exposes `remaining()`. Every runner call gets `timeout = min(configured, deadline.remaining())`.

| Call | Configured | Guard |
|---|---|---|
| `gh` | 20 s | not started when `remaining() < 5` (the read is `budget_exhausted` per issue, or exit 3 `gh_timeout` when shared) |
| probe | 10 s | as `gh` |
| `git` origin | 10 s | as `gh` |
| Orca launch | 120 s, never shortened | not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line |

The worst case is therefore 120 s of reads, then a 120 s launch, ending at 240 s, inside the 300 s cadence; the final save and audit write need no external call.

## 9. Security design

### 9.1 Threat controls and their tests

| # | Control in this design | Where | Test |
|---|---|---|---|
| T1 | Prompt from `build_claim_prompt(n)` only; G2 to G7 project no text; marker is a jq boolean | `launch.py`, `github.py` constants | `test_security_invariants.py::test_prompt_regex_property`, `test_no_text.py` |
| T2 | Latest `labeled` approval event; `actor_id` in the approvers set; later `unlabeled` voids it | `predicates.approval_of` | `test_predicates.py` (outsider relabel, unlabel after approval) |
| T3 | `actor_type == "User"` and login not ending `[bot]` | `predicates.approval_of` | `test_predicates.py` (Bot type, `x[bot]` login) |
| T4 | Body, non-own comments and `renamed` events all older than the approval | `predicates.unchanged_since(approval, edits, events)` | `test_predicates.py` (edit 1 s after approval skips) |
| T5 | `REPO` constant; literal repository in GraphQL constants | `github.py` | argv scan: no `SuperClaude-Org`, no `{owner}` (NFR-003) |
| T6 | `Runner.run(argv: list[str])` raises `TypeError` on `str`; `shell=False` literal | `runner.py` | `test_no_shell.py` (AST), `test_runner.py` |
| T7 | `host` (`socket.gethostname()`) and `login` on every line | `audit.py` | audit schema test |
| T8 | 0600/0700; `created_at` floor; exit 6 on damage | `record.py` | `test_record.py`, truncated and missing fixtures |
| T9 | Only G1 to G7 forms | `github.py` | `FakeRunner` exits 99 on any other argv; NFR-002 prefix test |
| T10 | Deployment gate; no permission flag in the argv | runbook | launch argv equality test (12 elements, no extra flag) |
| T11 | Closed audit schema; stderr capped at 500 bytes and kept out of audit lines | `runner.py`, `audit.py` | `test_no_text.py` with a `PWNED-TITLE` stderr |
| T12 | `max_candidates`, call cap, day cap, exit 4 at 100 | `cycle.py`, `record.py` | `test_cycle.py` budget and acceptance tests |
| T13 | `lstat`, `S_ISREG`, `st_uid`, mode `& 0o022 == 0`, line regex, at least one ID | `cycle.validate_approvers` | `test_cycle.py` (0664, empty, foreign owner, login line, symlink) |
| T14, T15 | none in v1 (residual) | n/a | n/a |
| T16 | runbook step 10 | `docs/designs/issue-watcher-setup.md` | none (procedure) |
| T17 | `orca-cli` topic required; non-dict topics rejected | `launch.find_orca` | `test_find_orca_parity.py` (screen-reader stub answering non-JSON) |

### 9.2 What crosses each trust boundary

| Data | From | Reaches Python as | Reaches the prompt | Reaches audit or store |
|---|---|---|---|---|
| Issue number | discovery | `int` after `type(x) is int` and 1..999999999 | yes, as digits | yes |
| Label names | discovery, events | `str`, compared for equality with config labels | no | no |
| Assignee logins | discovery, re-read | `str`, compared with the own login | no | no |
| Actor login, id, type | events | `str`, `int`, `str` | no | `approver_id` (int) only |
| Comment author login | G4, G5 | `str`, compared with the own login | no | no |
| Comment or issue body | never fetched as text | `bool` (`marker`) | no | no |
| Timestamps | G3 to G5 | `datetime` after strict ISO parse | no | `approved_at` |
| Project id, Status option | G6 | `str`, compared with config and `"Backlog"` | no | no |
| `gh` stderr | runner | `str`, at most 500 bytes | no | no (stderr fallback lines carry a reason only) |
| Orca stdout | launch | parsed JSON; only the operation id kept | no | `operation_id` after `^[A-Za-z0-9._:-]{1,128}$` |

The operation id regex is a design addition: the id is printed by `status` as part of a shell command the operator copies, so it must not carry shell metacharacters. An id that fails it is stored as `null` and the outcome is `unknown`.

### 9.3 D3 enforcement path

The prompt is built from the `int` held in the candidate's `DiscoveredIssue.number`, which `github.discover` produced with `type(v) is int and 1 <= v <= 999_999_999` (a `bool` fails `type(v) is int`). `build_claim_prompt` repeats the check and returns `f"/sc:issue --claim {n}"`. Nothing else is passed to `launch_argv` except constants, the resolved Orca path and the configured worktree. The property test draws `n` from integers, hostile strings, floats and booleans, and asserts every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`. Because hypothesis is not a dependency (C15), the property test is a seeded `random.Random(331)` loop of 2,000 draws plus the FR-012 edge list, tagged with the existing `property_based` marker (C12).

## 10. Observability

### 10.1 Audit line schema

One JSON object per line, written with one `os.write` on an `O_WRONLY | O_APPEND | O_CREAT` fd (mode 0600). Keys are sorted; `ensure_ascii=True`.

| Key | Cycle line | Decision line | Warning line | Type |
|---|---|---|---|---|
| `kind` | `"cycle"` | `"decision"` | `"warning"` | str |
| `ts` | yes | yes | yes | UTC str |
| `host`, `login` | yes | yes | yes | str, str or null |
| `cycle_id` | yes | yes | yes | `uuid4().hex` |
| `dry_run` | yes | yes | yes | bool |
| `exit` | yes | no | no | int |
| `reason` | yes | yes | yes | enum (`audit.REASON_TABLE`, 59 names) |
| `gh_calls`, `duration_ms` | yes | no | no | int |
| `issue` | no | yes | optional | int |
| `state` | no | yes, when an entry was written | no | enum |
| `approver_id`, `approval_event_id`, `approved_at` | no | yes (null when not reached) | no | int, int, str |
| `discovery_count` | optional | no | `discovery_count` warning | int |
| `clock_skew_s` | yes | no | `clock_skew` warning | int |
| `note` | no | `"re-approved"` when the approval event changed | no | str |

`rate_remaining`, titles, bodies, label names and stderr text are never keys (NFR-006, T11). `audit.REASONS` is a `frozenset` of the 59 keys of `audit.REASON_TABLE`, which are the spec's reason table plus the two [PROPOSAL] names `cycle_complete` and `cycle_crashed` added during the build (the full table, grouped by exit code, is in section 10.2 of [issue-watcher-setup.md](issue-watcher-setup.md)); `audit.line(...)` raises `ValueError` on any other reason, so a typo fails the first test that hits it.

Rotation (`AuditLog.rotate_if_needed`, called only with the lock held): if `audit.jsonl` is at least 5 MiB, `os.replace` `.3` to `.4`, `.2` to `.3`, `.1` to `.2`, current to `.1`, then a directory fsync. The exit-75 path appends and never rotates.

Stderr fallback (`audit.stderr_fallback(reason, exit)`): one JSON line with `kind`, `ts`, `host`, `exit`, `reason` only, used for a crash, an exit 2 before `state_dir` is known, and exit 6 `state_dir_unwritable`.

### 10.2 `status` output

`status` reads `dispatch.json` with a plain `open(..., "rb")` (no lock, no write), stats `DISABLED`, and reads nothing else. Exit 0 when healthy, 1 when unhealthy (age above 900 s or never completed), 6 when the store is unreadable.

`status --json` fields:

| Field | Type | Source |
|---|---|---|
| `healthy` | bool | age <= 900 |
| `last_completed_cycle_age_seconds` | int or null | now − `last_completed_cycle_at` |
| `disabled_since` | UTC str or null | `DISABLED` mtime |
| `next_permitted_at` | UTC str or null | store |
| `counts` | object state -> int | entries |
| `day_cap_used` | int | `record.day_cap_count(doc, now)` |
| `stale` | list of `{issue, state, last_reason, updated_at}` | `unknown` or `abandoned` `pending_orphan` older than 24 h |
| `retry` | list of `{issue, operation_id, cwd, argv}` | `unknown` entries with an `operation_id` |

`retry[].argv` is the original 12-element launch argv with `--retry-launch <operation_id>` inserted before `--json`, rebuilt from the entry, `ORCA_AGENT` and `build_claim_prompt(issue)`; the text form prints it with `shlex.join`. This follows `orca agent launch --help` ("re-issue the same command ... with --retry-launch"), which differs from the spec's shorter form (section 3, C20). The `<orca>` element is the first `_ORCA_CLIS` name on PATH, resolved with `shutil.which` and no probe, so `status` stays read-only.

### 10.3 SLO helper

`cycle.slo_numbers(lines: Iterable[dict], doc: StoreDoc, now) -> SloNumbers` reduces `audit.jsonl.4` to `audit.jsonl` (oldest first) plus the store to NFR-013's four numbers: (a) p95 of the `launched` decision `ts` minus its `approved_at`; (b) share of exit-0 cycle lines over 7 days, excluding `disabled`, `not_enabled` and `dry_run`; (c) share of `launched` entries that reached `claimed` before `lease_expires_at`; (d) count of `stale` entries. It is a library function with a fixture test, not a verb (no verb was specified).

## 11. Files to create or change

| Path | Purpose |
|---|---|
| `src/superclaude/cli/issue_watch/__init__.py` | Package marker; exports nothing |
| `.../issue_watch/runner.py` | `Runner` Protocol, `SubprocessRunner` (argv list, `shell=False`, timeout, 500-byte stderr cap) |
| `.../issue_watch/github.py` | `REPO`, argv builders G1 to G7, jq and GraphQL constants, paging, `classify`, `CallBudget` |
| `.../issue_watch/predicates.py` | Pure eligibility checks (approval, owner, unchanged, project, marker window) |
| `.../issue_watch/record.py` | `Store` Protocol, schema, migrations, transitions, lock, atomic save |
| `.../issue_watch/launch.py` | `Launcher` Protocol, `find_orca`, `parse_origin`, `build_claim_prompt`, `launch_argv`, outcome parse, `ORCA_AGENT` |
| `.../issue_watch/audit.py` | `REASONS`, line builders, `AuditLog` append and rotation, stderr fallback |
| `.../issue_watch/cycle.py` | `Clock` Protocol, `Deadline`, `run_cycle`, `slo_numbers` |
| `.../issue_watch/cli.py` | click group `issue_watch_group` and the six verbs; exit-code mapping only |
| `src/superclaude/cli/main.py` | Two lines after line 561, same pattern as `reflect_group` (lines 559 and 561) |
| `tests/issue_watch/__init__.py`, `conftest.py` | Package marker (C14); `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` fixtures |
| `tests/issue_watch/test_{runner,github,predicates,record,launch,audit,cycle,cli}.py` | One file per module |
| `tests/issue_watch/test_{cli_e2e,security_invariants,crash_injection,concurrency,no_shell,no_text,origin_parity,marker_contract,find_orca_parity,module_boundaries,slo_helper}.py` | Spec-named and design-added cross-cutting tests |
| `tests/issue_watch/fixtures/_assumed_shape/*.json` | Assumed `gh` and Orca replies, replaced by FU-1 |
| `tests/issue_watch/stubs/gh`, `stubs/orca` | Executable PATH stubs for `test_cli_e2e.py` |
| `docs/designs/issue-watcher-setup.md` | Runbook steps 1 to 10 for the owner |

Not changed: `pyproject.toml` (no dependency, no marker, no entry point), `Makefile`, CI, any file under `.claude/`. `docs/designs/issue-watcher-live-test.md` is written by the owner during FU-1. No primitive is added, so the installed-path rule is not engaged.

## 12. Tests

No test runs a real `gh`, `orca`, `git` or network call. Every external effect goes through a fake or a PATH stub.

| Seam | Fake | Rule |
|---|---|---|
| `Runner` | `FakeRunner(script: dict[tuple[str, ...], Reply])` | records every argv; unknown argv returns exit 99 and fails the test at teardown |
| `Clock` | `FakeClock(now, mono)` with `advance(s)` | the only time source; no `sleep` |
| `Launcher` | `FakeLauncher(outcomes)` | records argv and cwd; can raise |
| `Store` | `CrashingStore(real, crash_at="C1".."C5")` | raises `SystemExit` at the named point (section 7.6) |
| PATH | `stubs/gh`, `stubs/orca` (bash; scenario file in, argv log out) | stub dir prepended to `PATH` as in `tests/pr_submit/test_conflict_e2e.py`; a guard asserts `shutil.which("gh")` is the stub |

| Test | Checks |
|---|---|
| `test_crash_injection.py` | per C1 to C5, run, crash, rerun: total fresh launches per issue ≤ 1 (NFR-005) |
| `test_concurrency.py` | two `multiprocessing` processes on one `tmp_path` store: one exits 75 `lock_held`, one launch total |
| `test_cycle.py::test_fifty_cycles` | 50 cycles over a changing fixture: `launches` never exceeds 1 per issue |
| `test_cycle.py::test_acceptance_property` | for N in {1, 2, 6, 7, 50, 99}: at most 1 launch per cycle; after 24 h of cycles exactly min(N, 6) launched and the rest `day_cap`; after +24 h one more per cycle |
| `test_no_shell.py` | AST: no `shell=True`, no `os.system`, no `subprocess` outside `runner.py` |
| `test_no_text.py` | hostile titles, bodies and stderr (`PWNED-TITLE`) never appear in audit, store, prompt or stdout |
| `test_module_boundaries.py` | AST import graph matches section 5.3; no module named `select` |
| `test_marker_contract.py` | `CLAIM_MARKER` occurs in `refs/claim.md` and `templates/claim-comment.md`, read through the dual surface |

## 13. Gates, sync and packaging

| Gate | Source | Note |
|---|---|---|
| `uv run pytest tests/issue_watch/ -v` | spec line 366 | fast loop |
| `make test` | `Makefile:13-15` | CI uses `-n auto` (`test.yml:47`), C11 |
| `make lint` | `Makefile:48-50` | includes `lint-architecture` (C8); ruff 0.15.20, select `E,F,I,N,W,TID`, line length 88, py310 (`pyproject.toml:54,174-184`) |
| `uv run ruff format --check src/ tests/` | `test.yml:106` | no make target (C10) |
| `make verify-deps` | `Makefile:356-358`, `test.yml:123` | passes with no new dependency |
| `make verify-sync` | `Makefile:166`, `test.yml:131` | unaffected: nothing under skills, agents, commands, hooks or templates changes |
| `make sync-dev` | `Makefile:109` | preparation, not a gate |

The Python floor is 3.10 (`pyproject.toml:16`, CI `test.yml:22`): no `tomllib`, no `datetime.UTC` (use `timezone.utc`). Packaging needs nothing: hatchling includes the new package under `src/superclaude/`, and the `superclaude` entry point (`pyproject.toml:71`) reaches it through `main.py`.

## 14. Defaults ([PROPOSAL] values)

| Value | Default | Reason |
|---|---|---|
| `max_launches` per issue | 1 | D2 claim-only: one session per approval |
| `max_launches_per_cycle` | 1 | caps blast radius of a bad cycle |
| `max_candidates` | 10 | OD-11 (alternatives 5, 8); at r = 4 the call cap already limits k to 8 (section 6.3), so 10 is a ceiling |
| call cap | 35, 3 reserved | worst cycle 37 calls, 8.88% of 5,000 an hour |
| page cap per read | 5 | 500 events or comments; beyond is `events_incomplete` |
| day cap | 6 per rolling 24 h | bounds sessions the owner must review |
| `max_attempts`, backoff | 3, 10 min | transient Orca faults clear within minutes |
| lease | 60 min | a claim normally lands within minutes; reporting only |
| timeouts | gh 20 s, probe 10 s, git 10 s, Orca 120 s, deadline 240 s | fits the 300 s cadence (section 8.5) |
| skew tolerance | 300 s | equals the cadence |
| rate-limit clamp | 3600 s | primary limit window |
| stderr cap | 500 bytes | enough for classification, too small for a body |
| audit rotation | 5 MiB, 4 files | about 60 days of cycle lines per file at about 300 bytes a line |
| health age, stale age | 900 s, 24 h | three missed cycles; NFR-013 (d) |
| shadow run | 24 h | covers one day-cap window |
| state dir | `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` | XDG convention |
| operation-id regex | `^[A-Za-z0-9._:-]{1,128}$` | design addition (section 9.2) |

## 15. Commands and flags cited

| Command or flag | Source | Status |
|---|---|---|
| `gh api --method GET`, `-F`, `-f`, `--include`, `--jq` | `gh api --help`, gh 2.103.3 | verified; POST default with parameters (C21) |
| `gh issue list --repo --state --label --assignee --json --limit` | `gh issue list --help`, gh 2.103.3 (`--limit` default 30) | verified; the JSON field names `number`, `labels`, `assignees` are UNVERIFIED: check `gh issue list --json` with no value lists them |
| `gh api user --include` output layout | none | UNVERIFIED: capture one reply, confirm status line, `Date`, `Retry-After`, blank line, JSON body |
| REST events fields (`event`, `actor.id`, `actor.type`, `label.name`, `created_at`, `id`) | none in repo | UNVERIFIED: capture `repos/IronbellyOrg/IronClaude/issues/<n>/events` |
| GraphQL `userContentEdits`, `projectItems`, `fieldValueByName` | none in repo | UNVERIFIED: run `EDITS_QUERY` and `PROJECT_ITEMS_QUERY` once with `gh api graphql` |
| Rate-limit and auth stderr substrings | none | UNVERIFIED: record real stderr for 401, 403 secondary limit and 429 |
| `gh label create --repo IronbellyOrg/IronClaude` | spec runbook step 2 | UNVERIFIED: `gh label create --help` |
| `orca agent launch --agent --worktree path:<abs> --prompt --surface terminal --json`, `--retry-launch` | `orca agent launch --help`, Orca 1.4.245-aidev02 | verified flags; reply JSON (`outcome.kind`, `receipt.detail`, operation id path) UNVERIFIED |
| `agent_session_operation_unknown` | none (C16) | UNVERIFIED: provoke a lost reply in FU-1 |
| `orca skills list --json` (`topics`, `orca-cli`) | `orca skills list --help`; `install_user_setup.py:198-221` | verified |
| `git -C <abs> remote get-url origin` | `origin_repo.py:156-174` (without `-C`) | verified form; `-C` is standard git |
| `fcntl.flock`, `os.O_NOFOLLOW`, `os.O_CLOEXEC` | Python standard library, Linux | verified for Linux; other platforms exit 2 `platform_unsupported` |
| make targets and CI steps | section 13 | verified |

The implementer records each UNVERIFIED answer in the matching `_assumed_shape` fixture name and in `issue-watcher-live-test.md`.

## 16. Follow-up and owner questions

| Id | Item | Trigger |
|---|---|---|
| FU-1 | Live test; replace every `_assumed_shape` fixture | before any cron entry |
| FU-2 | Cron `"0 */5 * * * *"` (six fields, seconds first) | after FU-1 and the shadow run |
| FU-3 | Fine-grained token scope | when the owner moves off the CLI login |
| FU-4 | Alerting after three bad cycles | sink chosen |
| FU-5 | ETag conditional reads | call budget pressure |
| FU-6 | Launched-session permissions | before a second approver |
| FU-7 | Revisit D1 and D2 | spec section 2 conditions |
| FU-8 | Automatic `--retry-launch` | C20 argv confirmed in FU-1 |
| FU-9 | Approver role check (T14) | approver set grows |
| FU-10 | SLO review with `slo_numbers` | after 7 days live |
| FU-11 | Tombstone bound for `entries` | store above 1 MiB |
| FU-12 | Local-filesystem allow-list for `state_dir` | per-host facts gathered |

Owner questions: Q1 accept the S1 reading (section 6.3). Q2 accept the full-argv retry form (C20) in place of FR-015's short form. Q3 accept the 3600 s clamp for per-issue rate limits (C22). Q4 accept that the stderr classifier stays UNVERIFIED until FU-1, with unknown stderr mapped to `gh_auth_failed` on shared reads.

## 17. Acceptance criteria

All criteria run under `uv run pytest tests/issue_watch/` with fakes or PATH stubs only.

| AC | Criterion | Ids |
|---|---|---|
| AC-1 | One `once` runs the FR-001 order; `FakeRunner` sees G1 first and no argv after an exit decision | FR-001, FR-002 |
| AC-2 | Discovery argv equals the FR-003 literal; 100 results or a repeated number exits 4 | FR-003, FR-004 |
| AC-3 | Approval table: outsider, bot, unlabel, relabel, incomplete history, edit after approval each skip with their reason | FR-005, FR-006 |
| AC-4 | Project and owner tables: wrong project, not Backlog, unassigned, other assignee skip | FR-007, FR-008 |
| AC-5 | An own-login marker comment yields `claimed` and no launch | FR-009 |
| AC-6 | `pending` with `launches` 1 is saved before the launcher is called; the re-read failure skips | FR-010, FR-011 |
| AC-7 | Every recorded prompt matches the D3 regex over the hostile corpus; non-int input raises | FR-012, NFR-001 |
| AC-8 | Launch argv equals the 12-element list; outcome table maps to `launched`, `failed`, `unknown`, `abandoned` | FR-013, FR-014 |
| AC-9 | No automatic retry; `status` lists the full retry argv for an `unknown` entry | FR-015, FR-021 |
| AC-10 | Budget, day cap and `consumed_log` hold through `reset`; acceptance property passes | FR-016, FR-023, FR-024, NFR-009 |
| AC-11 | Second process exits 75; symlinked or foreign lock exits 6 | FR-017 |
| AC-12 | `DISABLED` and `enabled: false` exit 0 before any external call | FR-018, FR-027 |
| AC-13 | Dry-run writes only `dry-run.json` and audit; the real store is byte-identical | FR-019 |
| AC-14 | Every exit writes a schema-valid audit line or the stderr fallback; rotation keeps 4 files | FR-020, NFR-006 |
| AC-15 | Shared-input failures map to exits 2, 3, 5, 6, 7 with the precedence 2, 6, 7, 5, 3, 4 | FR-022, NFR-007 |
| AC-16 | Origin mismatch exits 2; parity table agrees with `origin_repo.py` | FR-025, NFR-003 |
| AC-17 | Each verb's exit codes match section 4; `check-config` and `status` write nothing | FR-026, FR-021 |
| AC-18 | Rate limit persists `next_permitted_at`, clamps to 3600 s, and `reset --rate-limit` clears it | FR-028 |
| AC-19 | A sleeping stub ends with `gh_timeout`; no launch starts after 120 s | FR-029, NFR-008 |
| AC-20 | Argv prefix scan: only G1 to G7, `--method GET`, no upstream name | NFR-002, NFR-003 |
| AC-21 | `test_no_shell.py` passes | NFR-004 |
| AC-22 | Crash points C1 to C5 and 50 cycles never exceed one launch per issue | NFR-005, NFR-010, NFR-011 |
| AC-23 | No new dependency; gates in section 13 pass | NFR-012 |
| AC-24 | `slo_numbers` returns the four values on a fixture log | NFR-013 |
| AC-25 | Module-boundary and parity tests pass | NFR-014 |

## 18. Traceability

| Id | Sections |
|---|---|
| FR-001, FR-002 | 6.1, 6.2, 8.1 (G1) |
| FR-003, FR-004 | 8.1 (G2), 8.2 |
| FR-005, FR-006 | 5.2, 8.1 (G3, G5), 9.1 (T2 to T4) |
| FR-007, FR-008 | 8.1 (G6), 3 (C6) |
| FR-009 | 8.1 (G4), 7.4 |
| FR-010, FR-011 | 6.2, 7.4, 7.6, 8.1 (G7) |
| FR-012 | 9.3 |
| FR-013, FR-014 | 8.4, 7.4 |
| FR-015 | 10.2, 3 (C20), 16 |
| FR-016, FR-023 | 6.3, 7.5 |
| FR-017 | 7.6 |
| FR-018, FR-027 | 4.1, 4.2 |
| FR-019 | 7.2 (`dry-run.json`) |
| FR-020 | 10.1 |
| FR-021 | 10.2 |
| FR-022 | 4.3, 8.2 |
| FR-024 | 7.2, 7.5 |
| FR-025 | 3 (C3), 8.4 |
| FR-026 | 4.1 |
| FR-028 | 8.3, 3 (C22) |
| FR-029 | 8.5 |
| NFR-001 | 9.2, 9.3 |
| NFR-002, NFR-003 | 8.1, 9.1 (T5, T9) |
| NFR-004 | 5.4, 9.1 (T6) |
| NFR-005, NFR-010, NFR-011 | 7.3 to 7.6 |
| NFR-006 | 10.1 |
| NFR-007 | 4.3, 8.2 |
| NFR-008 | 8.5 |
| NFR-009 | 6.3, 8.2 |
| NFR-012 | 11, 13 |
| NFR-013 | 10.3 |
| NFR-014 | 5.1 to 5.4 |
