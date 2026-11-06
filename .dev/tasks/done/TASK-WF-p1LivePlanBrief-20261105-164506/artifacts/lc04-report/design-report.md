# Design: read-only status endpoint, installed commands vs repository

- Command: `/sc:design "a read-only status endpoint that reports whether the installed commands match the repository" --type api --format spec --unattended --report-dir .dev/p1-live/design/`
- Date: 2026-11-05
- Status: design only, no implementation code, no existing architecture changed

## 1. Requirement and verified context

**Requirement.** One read-only endpoint that answers: do the slash commands installed for Claude Code (`~/.claude/commands/sc/`) match the commands in the repository (`src/superclaude/commands/`)?

**Verified in this checkout (read from disk, 2026-11-05):**

| Fact | Source |
|---|---|
| Installing copies each command only if the target file is missing; an existing file is skipped unless `force` is set. So an installed command can silently fall behind the repository. | `src/superclaude/cli/install_commands.py:55-57` |
| The set of commands is every `*.md` file in the source directory except `README.md`. | `install_commands.py:11,39-41` |
| The source directory is the package's `commands/` folder, else `plugins/superclaude/commands/`. | `install_commands.py:96-126` (`_get_commands_source`) |
| The existing listers (`list_available_commands`, `list_installed_commands`) return names only, with the home directory hard-coded. Neither compares content. | `install_commands.py:129-166` |
| `superclaude doctor` checks that installed commands can resolve their skills, not that they match the repository. | `src/superclaude/cli/doctor.py:321-349` |
| `make verify-sync` compares `src/superclaude/commands/` with the project `.claude/commands/sc/` using `diff -q`. It does not look at `~/.claude`. | `Makefile:228-252` |
| Fix path exists: `superclaude install --force` reinstalls; `superclaude update` calls the installer with `force=True`. | `src/superclaude/cli/main.py:36,372` |
| Today, in this checkout, source has 48 files (46 commands plus `README.md` and `__init__.py`) and `~/.claude/commands/sc` has 46, with no content differences. | `diff -rq` run during this design |
| This project has no web framework dependency. The only HTTP server in the tree is a standard-library `http.server` proxy bound to `127.0.0.1`. | `pyproject.toml:34-43`; `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:34,68` |

**Consequence.** There is nothing to extend. The endpoint is new, and the comparison it needs does not exist as a reusable function.

## 2. Design decisions

| # | Decision | Reason |
|---|---|---|
| D1 | The endpoint is a thin view over one pure function, `compare_commands(source_dir, installed_dir) -> result`. The function takes both directories as arguments and does no I/O other than reading files. | The same function can back a `--json` command-line check later, and it is testable without a server. |
| D2 | Transport is the standard-library `http.server`, bound to `127.0.0.1` only, with a port set at start-up. | No new dependency; matches the one precedent in the tree. |
| D3 | The two directories are fixed when the server starts (source from `_get_commands_source()`, installed from `~/.claude/commands/sc`). A request can never name a path. | Removes any path-traversal or arbitrary-file-read surface. |
| D4 | "Match" means identical bytes (SHA-256), never modification time. | `shutil.copy2` keeps mtime, so mtime can agree while content differs, or differ while content agrees. |
| D5 | The endpoint must not call `install_commands()`. | That function creates the target directory (`mkdir`) and copies files, which breaks the read-only promise. |
| D6 | A completed comparison always returns HTTP 200, even when there is drift. Drift is reported in the body (`match: false`). | The request succeeded; "not in sync" is the answer, not an error. Monitors read `match`. |
| D7 | Computed on every request, no cache, `Cache-Control: no-store`. | About 46 small files; hashing cost is negligible, and a cached answer would be wrong right after `install --force`. |

**Smaller alternative, not chosen but cheaper:** skip the server and add `superclaude commands-status --json` that prints the same body (D1). It needs no port and no process to keep running. The endpoint was requested, so this design builds the endpoint; the function is shaped so the command-line form costs a few lines.

## 3. API specification

### 3.1 Endpoint

| Item | Value |
|---|---|
| Method and path | `GET /v1/commands/status` (`HEAD` returns the same headers, no body) |
| Query parameters | None. Any query string is ignored. |
| Request body | None. |
| Auth | None. Loopback bind is the control (section 5). |
| Media type | `application/json; charset=utf-8` |
| Response headers | `Cache-Control: no-store`, `X-Content-Type-Options: nosniff` |

### 3.2 Success response, 200

```json
{
  "schema_version": 1,
  "checked_at": "2026-11-05T19:30:00Z",
  "source_dir": "/path/to/repo/src/superclaude/commands",
  "installed_dir": "/home/user/.claude/commands/sc",
  "installed_dir_exists": true,
  "match": false,
  "counts": {
    "source": 46,
    "installed": 46,
    "same": 45,
    "differs": 1,
    "missing_installed": 0,
    "extra_installed": 0
  },
  "commands": [
    { "name": "design.md", "state": "differs",
      "source_sha256": "<64 hex>", "installed_sha256": "<64 hex>" },
    { "name": "build.md", "state": "same",
      "source_sha256": "<64 hex>", "installed_sha256": "<64 hex>" }
  ],
  "remedy": "superclaude install --force"
}
```

Field rules:

| Field | Type | Rule |
|---|---|---|
| `schema_version` | integer | `1`. Bumped only on a breaking change. |
| `checked_at` | string | UTC, RFC 3339, taken when the comparison ran. |
| `source_dir`, `installed_dir` | string | Absolute paths the server was started with. |
| `installed_dir_exists` | boolean | `false` when `~/.claude/commands/sc` does not exist; every command is then `missing_installed`. |
| `match` | boolean | `true` only when `differs`, `missing_installed` and `extra_installed` are all 0. |
| `counts` | object | Integers; `same + differs + missing_installed` equals `source`; `same + differs + extra_installed` equals `installed`. |
| `commands[].name` | string | File name, for example `design.md`. Sorted ascending, byte order. |
| `commands[].state` | enum | `same`, `differs`, `missing_installed` (in repository, not installed), `extra_installed` (installed, not in repository). |
| `commands[].source_sha256` | string or null | null when the file is not in the repository. |
| `commands[].installed_sha256` | string or null | null when the file is not installed. |
| `remedy` | string or absent | Present only when `match` is `false`. The fixed text `superclaude install --force`; it is a hint and the endpoint never runs it. |

### 3.3 Error responses

Body is always `{"error": {"code": "<code>", "message": "<text>"}}`.

| Status | `code` | When |
|---|---|---|
| 404 | `not_found` | Any path other than `/v1/commands/status`. |
| 405 | `method_not_allowed` | Any method other than `GET` and `HEAD`. Response carries `Allow: GET, HEAD`. |
| 500 | `source_not_found` | The repository commands directory does not exist or has no command files (the installer's own error case). |
| 500 | `read_failed` | A file in either directory cannot be read (permission or I/O error). The message names the file name, not a stack trace. |

An absent installed directory is not an error: it is a result (`installed_dir_exists: false`, `match: false`).

## 4. Comparison rules

1. **Command set.** In each directory, every regular file whose name ends in `.md`, excluding `README.md`. This is the same rule the installer uses, so the endpoint and the installer cannot disagree about what a command is.
2. **Not followed.** Subdirectories and symbolic links are skipped. A symbolic link in the installed folder is not read, so a link cannot make the endpoint read outside the folder.
3. **State per name.** Present on both sides with equal SHA-256: `same`. Present on both with different SHA-256: `differs`. Only in the repository: `missing_installed`. Only installed: `extra_installed`.
4. **`extra_installed` counts as drift.** A retired or renamed command left behind in the installed folder still appears as a slash command to the user, so it is a real mismatch. See open question Q1.
5. **Bytes, not text.** Files are hashed as raw bytes; no newline or whitespace normalization.
6. **Which repository.** The directory `_get_commands_source()` resolves, which in a source checkout installed with `pip install -e` or `uv` is `src/superclaude/commands`. It is not the project `.claude/commands/sc` copy (that comparison is what `make verify-sync` already does).

## 5. Security and read-only guarantees

| Risk | Control |
|---|---|
| Reachable from other machines. | Bind `127.0.0.1` only; there is no option to bind another address. |
| Request chooses what to read. | None can: paths are fixed at start-up (D3); the query string is ignored. |
| Endpoint changes the installed commands. | Only `open(..., "rb")` and directory listing are allowed in the module. It imports no installer code (D5) and never creates a directory. |
| Browser page on another origin reads the answer (DNS rebinding or cross-site fetch). | Reject any request whose `Host` header is not `127.0.0.1:<port>` or `localhost:<port>` with 404 `not_found`; send no CORS headers. |
| Leaks local paths. | `source_dir` and `installed_dir` are in the body on purpose (they explain a mismatch) and are safe only because of the loopback bind and Host check. See Q2. |
| Stack traces in errors. | Error bodies carry the fixed code and a short message only. |
| Slow or huge request. | Request bodies are never read; one request is served at a time per connection; a socket timeout of 5 seconds is set. |

## 6. Validation plan

A test file next to the existing CLI tests (`tests/cli/`, for example `tests/cli/test_commands_status.py`) should cover, using temporary directories so the real `~/.claude` is never touched:

| Case | Expected |
|---|---|
| Identical directories | `match: true`, `differs = 0`, no `remedy` field. |
| One file with a changed byte | That name is `differs`, `match: false`, `remedy` present. |
| File only in the repository | `missing_installed`. |
| File only in the installed folder | `extra_installed`, `match: false`. |
| `README.md` in either folder | Ignored. |
| Installed directory absent | 200, `installed_dir_exists: false`, every command `missing_installed`, and the directory is still absent afterwards (proves read-only). |
| Source directory absent | 500 `source_not_found`. |
| Symbolic link in installed folder | Skipped, not read. |
| `POST`, `PUT`, `DELETE` | 405 with `Allow: GET, HEAD`. |
| Unknown path | 404. |
| Wrong `Host` header | 404. |
| Counts identities | `same + differs + missing_installed == source` and `same + differs + extra_installed == installed`. |
| Read-only proof | Snapshot of both folders (names and bytes) before and after a request is identical. |

Acceptance for the whole feature: all cases above pass under `uv run pytest tests/cli/test_commands_status.py -v`; and, run against the real machine, the endpoint reports `match: true` when `diff -rq src/superclaude/commands ~/.claude/commands/sc` shows only `README.md` and `__init__.py` as repository-only.

## 7. Open questions for the owner

| # | Question | Recommendation |
|---|---|---|
| Q1 | Should a command that is installed but not in the repository count as drift? A user may keep personal commands in `~/.claude/commands/sc/`. | Count it (as designed), because retired commands linger otherwise. If personal commands are expected there, report `extra_installed` in `counts` but leave it out of `match`. |
| Q2 | Is it acceptable that the response shows absolute home-directory paths? | Yes while loopback-only. Drop both path fields if the endpoint is ever exposed beyond the machine. |
| Q3 | Who starts the server and on what port (a new `superclaude` subcommand, or a task in the sprint tooling)? | Not decided here. A new subcommand with an explicit `--port` and no default daemon mode is the smallest fit. |
| Q4 | Should the same check also cover skills and agents, which are installed the same skip-if-present way? | Not in this design (not asked). The function in D1 would take the file filter as an argument if that is wanted later. |

## 8. Scope notes

- No implementation code was written and no existing file was modified; only this report and `return-contract.yaml` were created under `.dev/p1-live/design/`.
- Nothing was staged, committed or pushed.
- Not verified: the HTTP behaviours in sections 3 and 5 (Host check, timeouts, `HEAD` handling) are specified, not tested, because no implementation exists.
