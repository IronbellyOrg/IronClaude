# Research: Identity selector and process ancestry
**Investigation type:** Code Tracer
**Scope:** src/superclaude/hooks/scripts/launch-job-identity.sh
**Status:** Complete
**Date:** 2026-11-08
---

Source read in full: `src/superclaude/hooks/scripts/launch-job-identity.sh` (566 lines, read 2026-11-08). Context: `.dev/brainstorms/20261108-094705-l2-pre-push-guard/seed-brief.md` (line 73), `docs/designs/sc-issue-launch-level-hook.md` §19.2 (line 512), §19.7 (lines 547-565).

## 1. Bash wrapper and callable interface (lines 1-60, 525-566)

### Structure

The file is a bash script whose body is a Python program held in a quoted heredoc (`read -r -d '' launch_identity_code <<'PY'`, line 55, ending at `PY` line 565). Line 566 runs it: `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"`. So:

- `sys.argv[0]` is `-c`, `sys.argv[1]` is the script path (`$0`), and `main()` receives `sys.argv[2:]` (line 560), i.e. the original bash arguments.
- `-I` is Python isolated mode (ignores `PYTHON*` environment variables and user site). `--no-project` means uv does not look for a project `pyproject.toml`.
- `exec` replaces bash with `uv`; whether `uv` then execs Python or keeps Python as a child is a uv implementation detail (see the experiment in section 3).

### Pre-UV gates (lines 20-54)

- **Lines 20-24, early `exit 0`:** applies ONLY when there are no arguments or the single argument `hook` (`$# == 0 || ( $# == 1 && $1 == hook )`). It exits 0 silently when `HOME` is empty/unset (`-z ${HOME:-}`) or `$HOME/.claude/state/launch-level` neither exists nor is a symlink. **It does not apply to `identify`.** An `identify` call always continues to line 25.
- **Lines 25-53, `uv` absent from `PATH`:**
  - For no-arg / `hook` mode only (line 26): if `jq` is absent, `exit 0` (line 30). Otherwise jq (lines 31-36) parses stdin as exactly one JSON object with `tool_name == "Bash"` and a valid `session_id`; any failure is `exit 0`. Then it requires an absolute `HOME` (line 37), a HOME owned by the caller (`-O`, line 39), no symlinked ancestor of HOME (lines 40-44), each of `.claude/state/launch-level/sessions` an owned non-symlink directory (lines 45-48), and `sessions/<sid>` an owned regular non-symlink file (line 50). Any miss is `exit 0`. If all hold (a positively bound session exists but cannot be adapted), it falls through to line 52.
  - For every other invocation, **including `identify`**, it goes straight to lines 52-53: stderr `launch job: UV is required for this invocation`, **`exit 2`**, nothing on stdout.
- So: **a pre-push hook that runs with a `PATH` lacking `uv` gets exit 2, empty stdout, no verdict.** The hook must treat that as "no verdict" (see section 6 for how this interacts with the owner's `unknown` decision).

### `main()` dispatch (lines 525-556)

| Invocation | Lines | Behaviour | Exit |
|---|---|---|---|
| (none) or `hook` | 526-527 | PreToolUse adapter, reads stdin | 0 or 2 |
| `execute SESSION TOOL_ID_OR_EMPTY COMMAND` | 528-529 | create and consume a private request, run it | job status |
| `identify` | 530-537 | `pid = os.getpid()` (line 532) | 0 |
| `identify PID` | 530-537 | `pid = int(args[1])` (line 532) | 0 |
| `prepare SESSION COMMAND [TOOL_USE_ID]` | 538-553 | publish a request, print a 32-hex token | 0 |
| `run TOKEN` | 554-555 | consume the request and supervise | job status |
| anything else | 556 | `ValueError('invalid invocation')` -> lines 561-564 | 2 |

`identify` specifics:

- Accepts exactly 1 or 2 arguments (line 530); `identify 1 2` falls to line 556 -> stderr `launch job: invalid invocation or unavailable private state`, exit 2.
- `int(args[1])` raising `ValueError` (non-numeric) is caught at line 534 -> `{"status": "unknown"}`. Python `int()` also accepts surrounding whitespace, a `+` sign and digit underscores (`" 12"`, `+12`, `1_2`), which are not rejected.
- Output (line 536) is `json.dumps(result)` with **default separators**, i.e. one line such as `{"status": "ordinary"}`, `{"status": "ordinary", "reason": "released"}`, `{"status": "governed", "session_id": "<id>"}` or `{"status": "unknown"}`. Note the space after `:` and `,`; `publish()` uses compact separators (line 169) but `identify` does not. A hook should parse JSON (or match the exact default-separator text) rather than compare against compact text.
- `identify` always exits 0 when Python runs (line 537); the verdict is only in stdout. A non-zero exit means the verdict was never produced (UV missing: exit 2 from line 53; argument shape error: exit 2 from line 564; or a uv-level failure with uv's own status).
- No command text is ever printed (header comment line 5: "never command text" `[CODE-VERIFIED]` at line 536, only the `result` dict is printed).

### Key Takeaways

- The callable interface for a hook is `launch-job-identity.sh identify [PID]`: stdout is one JSON line, exit 0; any non-zero exit means "no verdict".
- The early `exit 0` at lines 20-24 is for the adapter mode only and never fires for `identify`.
- With `uv` missing from `PATH`, `identify` exits 2 with empty stdout (lines 25, 52-53); the jq fallback is not used for `identify`.
- Parse the JSON; do not compare literal compact strings (default `json.dumps` separators at line 536).

## 2. State location: `directory()`, `store()`, `subdir()`, `private()` (lines 81-137)

- `private(st, directory)` (lines 81-84): the object must be a regular file (or a directory when `directory=True`), owned by `os.geteuid()`, with no group/other bits (`st_mode & 0o077 == 0`), else `ValueError('unsafe state')`.
- `directory(parts)` (lines 87-99): opens `/` then each component with `O_RDONLY | O_DIRECTORY | O_NOFOLLOW` relative to the previous fd (`dir_fd`). An empty, `.` or `..` component raises `ValueError('invalid state path')` (lines 91-92). A symlinked component fails in `os.open` with an `OSError` (`ELOOP`/`ENOTDIR`), a missing one with `FileNotFoundError`.
- `store()` (lines 102-122):
  - `home = os.environ.get('HOME', '')` (line 103); if it does not start with `/`, `ValueError('invalid home')` (lines 104-105). This covers HOME **unset**, **empty** and **relative**.
  - `directory(home.strip('/').split('/'))` (line 106): trailing slashes are stripped, but a doubled slash (`/home//coder`) yields an empty component -> `ValueError`; `HOME=/` yields `['']` -> `ValueError`.
  - HOME itself must be owned by the euid and not group/other-writable (`0o022`, lines 108-110), else `ValueError('unsafe home')`. Ancestors of HOME are only checked for "not a symlink" (by `O_NOFOLLOW`), not for ownership.
  - Then `.claude`, `state`, `launch-level` are each opened `O_NOFOLLOW` and must be euid-owned and not `0o022`-writable (lines 111-117); the final `launch-level` must also pass `private(..., True)` (no `0o077` bits, line 118).
- `subdir(root, name, create=False)` (lines 125-137): opens `name` under `root` with `O_NOFOLLOW` and requires `private(..., True)`. `identify` calls it with `create=False` (line 222), so **`identify` never creates state**.
- `read_file(parent, name)` (lines 140-161), non-consuming path as used by `identify`/`governed`: `O_RDONLY | O_NOFOLLOW | O_NONBLOCK`, `private(st)`, `st_nlink == 1`, size <= 65536 (`LIMIT`, line 71), else `ValueError`.

### Which HOME cases produce which `identify` verdict

`identify()` wraps `store()`, `subdir(root, 'jobs')` and `read_file(jobs, '<sid>.json')` in an inner `try` that catches **only `FileNotFoundError`** and returns `{'status': 'ordinary'}` (lines 220-225). Every other exception propagates to the outer handler at line 243, which returns `{'status': 'unknown'}`. Note that `proc(pid)` (line 219) runs **before** `store()`, so a missing `/proc/<pid>` already yields `unknown` regardless of HOME.

| HOME case | Raised where | Exception | Verdict |
|---|---|---|---|
| unset or empty | line 105 | `ValueError('invalid home')` | **unknown** |
| relative (e.g. `home/x`) | line 105 | `ValueError('invalid home')` | **unknown** |
| `/`, or contains `//`, `.` or `..` component | line 92 | `ValueError('invalid state path')` | **unknown** |
| absolute but the path does not exist | line 93 | `FileNotFoundError` | **ordinary** |
| absolute, a component is a symlink | line 93 | `OSError` (`ELOOP`/`ENOTDIR`), not `FileNotFoundError` | **unknown** |
| owned by another uid or group/other-writable | line 110 | `ValueError('unsafe home')` | **unknown** |
| valid home, no `.claude`, `state` or `launch-level` | line 112 | `FileNotFoundError` | **ordinary** |
| store exists, no `jobs/` dir | line 131 via 222 | `FileNotFoundError` | **ordinary** |
| `jobs/` exists, no `<sid>.json` | line 143 via 223 | `FileNotFoundError` | **ordinary** |
| any store dir group/other-writable, foreign-owned or a symlink | lines 112-118, 131-133 | `ValueError` / `OSError` | **unknown** |

**Consequence for a hook running under a HOME different from the agent's:** the governed job record lives under the agent's `HOME` (`jobs/<sid>.json` written by `supervise()` at line 305 into the store opened by `run()` -> `store()` at line 365). If the hook process sees a different, valid, absolute HOME that has no launch-level store (or no `jobs/<sid>.json`), `identify` returns **ordinary** (line 225), and a governed agent's push would be **allowed**. If the different HOME is unset/relative/unsafe, the verdict is **unknown**. Git does not change `HOME` for hooks (git passes its environment through); a wrapper such as `env -i`, `sudo`, or `HOME=... git push` would. Design §19.7 line 557 states the same requirement: "State location is the configured HOME's launch-level store; callers must preserve that execution context" `[CODE-VERIFIED]` (lines 103, 106).

### Key Takeaways

- Missing state at any level is `ordinary`; malformed, unsafe or unparseable HOME is `unknown` (lines 104-105, 220-225, 243-244).
- A hook under a different but valid HOME silently gets `ordinary`, which is a bypass: `HOME=/tmp/x git push origin main` from a governed job would be selected ordinary. This is a selector limit the L2 design must list (the job's kernel session is still governed; only the store lookup is lost).
- `identify` is read-only: no `create=True`, no `publish`, no unlink on its path.

## 3. `proc()`, `boot()`, `identify()` and `members()` (lines 202-265)

### `proc(pid)` (lines 202-207)

- Rejects a non-`int` or `pid <= 0` with `ValueError('invalid process')` (lines 203-204); `type(pid) is not int` also rejects `bool`.
- Reads `/proc/<pid>/stat`, splits after the **last** `)` (so a `comm` containing `)` or spaces is safe), and returns `(fields[0], int(fields[3]), int(fields[19]))`. After the split, `fields[0]` is proc(5) field 3 `state`, `fields[3]` is field 6 `session`, `fields[19]` is field 22 `starttime` (clock ticks since boot). So `proc` returns `(state, kernel session id, start ticks)`.
- Missing `/proc/<pid>` (dead PID, or `/proc` not mounted) raises `FileNotFoundError`; a process that dies mid-read can raise `ProcessLookupError` (both `OSError`).

### `boot()` (lines 210-212)

Reads `/proc/sys/kernel/random/boot_id` and normalises it through `uuid.UUID`. A malformed value raises `ValueError`.

### `identify(pid)` data flow (lines 215-248)

1. **PID in:** from `main()` line 532, either `os.getpid()` (the Python interpreter process running the selector) or `int(argv)`.
2. **Kernel session of that PID:** `_, sid, _ = proc(pid)` (line 219). **Only the session id is used; the PPID chain is never read** (no `ppid` field is extracted; `fields[1]` (ppid) is ignored). There is no ancestry walk anywhere in the file; the comment at line 253 says so for `members()` ("No bounded ancestry walk ... is interpreted as ordinary").
3. **Record lookup:** `jobs/<sid>.json` in the HOME store (lines 221-223). Missing -> `ordinary` (line 225).
4. **Record shape:** exactly the keys `pid, start, boot, kernel_sid, session_id` (line 227); `pid` and `kernel_sid` must be `int` and equal to `sid` (line 229), i.e. the record must belong to the session leader of the looked-up session; `start` must be `int` and `session_id` a valid id (lines 231-232).
5. **Liveness of the supervisor:** `proc(value['pid'])` (line 233); refuse (`unknown`) if it is a zombie, no longer leads that session, has different start ticks, or `boot()` differs (lines 234-235). If the supervisor PID is gone, `proc` raises `FileNotFoundError` -> caught by the outer handler -> `unknown` (this `FileNotFoundError` is outside the inner `try` of lines 220-225).
6. **Same user:** `os.stat('/proc/<sid>').st_uid != os.geteuid()` -> `unknown` (lines 236-237).
7. **Governed record of the logical session:** `governed(root, session_id)` (line 239; function at lines 177-186) reads `sessions/<session_id>`, which must be exactly `worktree`, `full` or `full-submit`, optionally with one trailing newline (`LEVELS` line 74, check line 183). `FileNotFoundError` (missing file **or missing `sessions/` directory**, since `subdir` at line 180 is inside the same `try`) -> `{'status': 'ordinary', 'reason': 'released'}` (lines 240-241). Any other content -> `ValueError('invalid level')` -> `unknown`.
8. **Verdict out:** `{'status': 'governed', 'session_id': ...}` (line 242). The outer handler (line 243) maps `OSError, ValueError, IndexError, TypeError, RecursionError, AttributeError` to `unknown`. `json.JSONDecodeError` is a `ValueError` subclass, so a corrupt record is `unknown`. A `KeyboardInterrupt`/`SystemExit` is not caught.

### `members(sid)` (lines 251-265)

Used only by the supervisor (`supervise()` lines 332, 344, 353, 358), not by `identify`. It scans every numeric `/proc` entry except its own PID and collects non-zombie processes whose kernel session equals `sid`. It is the supervisor's wait set and signal set.

### What PID a pre-push hook should pass

- `identify` with no PID uses `os.getpid()` of the Python process (line 532). Kernel session ids are inherited across `fork`/`exec` unless something calls `setsid()`, so the Python process has the same session as the bash script, the hook, git and the governed job, **provided neither uv nor anything between calls `setsid`**. The no-argument form is therefore valid for a hook, and it avoids the hook trusting `$PPID`. Passing `$$` (the hook shell's PID) is equivalent if nothing in between changes sessions. Passing `$PPID` (git) is also equivalent for an ordinary `git push`, but it is a PID the hook did not create, which adds a small PID-reuse window if git exits first (git waits for pre-push, so in practice it is alive). Observed behaviour is recorded in section 7.
- Because only session membership matters, **which** ancestor is passed does not matter as long as it is in the same kernel session; what matters is that no process between the governed supervisor and the PID passed called `setsid`.

### setsid behaviour

- `supervise()` itself calls `os.setsid()` (line 292) to create the job's session; the supervisor is the session leader so `sid == pid` (line 293) and the record is `jobs/<sid>.json` (line 301).
- If the agent's command, git, a wrapper or the hook calls `setsid` before `identify` runs, the PID passed is in a **new** session whose id equals the new leader's PID. `jobs/<newsid>.json` does not exist (the supervisor only publishes its own sid) -> `FileNotFoundError` -> **ordinary** (line 225). So `setsid git push origin main` from a governed job is selected ordinary and allowed. The header comment at lines 7-8 ("deliberate setsid/daemonization escapes selection") and design §19.7 line 559 state this `[CODE-VERIFIED]` (lines 219-225, no fallback to the PPID chain). Seed brief line 45 lists it as a known B-CTX gap.
- If the hook itself ran `setsid` around its `identify` call, it would make **every** push (human or agent) ordinary, so the hook must not do that.
- Git does not call `setsid` for hooks (observed in section 7); `setsid` only matters when something in the chain deliberately calls it.

### Key Takeaways

- Selection is by kernel session membership (`/proc/<pid>/stat` field 6), never by the PPID chain (lines 205-207, 219).
- Any `setsid` between the governed supervisor and the PID that is identified makes the push `ordinary`, i.e. allowed: an accepted limit, not a code bug.
- A hook can call `identify` with no PID; the Python process inherits the hook's session.
- A dead supervisor, a reused supervisor PID, a different boot, or a foreign uid produce `unknown`, not `ordinary`.

## 7. Observed behaviour with real git (experiment, 2026-11-08)

(Numbered 7 to keep the order of findings; sections 4-6 follow below.)

**Setup:** `mktemp -d /tmp/l2-ident.XXXXXXXX` holding a temporary HOME with a private store (`sessions/sidA` = `worktree`), a local bare repo `remote.git` as the only remote, and a clone whose `.git/hooks/pre-push` printed its PID, PPID, both kernel session ids, and the result of `identify`, `identify $$` and `identify $PPID`. Governed pushes went through the real `prepare sidA "<cmd>"` + `run TOKEN` path of the script. No real remote was touched; the directory was removed afterwards (verified absent). git `/usr/bin/git`, uv 0.11.8 at `/usr/local/bin/uv`.

| Case (command inside the governed job unless noted) | hook sid == git sid == supervisor sid? | `identify` / `$$` / `$PPID` | exit |
|---|---|---|---|
| ordinary terminal, no job: `git push origin HEAD:f1` | same as caller shell | ordinary x3 | 0 |
| `git push origin HEAD:refs/heads/main` | yes (308339) | governed sidA x3 | 0 |
| `setsid -w git push ...` | new session 308471 (git is leader) | **ordinary x3** | 0 |
| `HOME=<other valid dir> git push ...` | yes | **ordinary x3** | 0 |
| `env -u HOME git push ...` | yes | unknown x3 | 0 |
| `HOME=relative/x git push ...` | yes | unknown x3 | 0 |
| `PATH=/usr/bin:/bin git push ...` (no uv) | yes | **no verdict**: stderr `launch job: UV is required for this invocation` | 2 |
| `sh -c 'git push ...' & wait` (background child) | yes | governed sidA x3 | 0 |
| `rm sessions/sidA && git push ...` | yes | `{"status": "ordinary", "reason": "released"}` x3 | 0 |
| `printf bogus > sessions/sidA && git push ...` | yes | unknown x3 | 0 |

Direct calls outside a job: `identify 999999`, `0`, `-5`, `abc` -> unknown, exit 0; `identify ' 12'` -> unknown (PID 12 absent, whitespace accepted by `int`); `identify +1` -> ordinary (the `+` is accepted, PID 1 has no record); `identify 1 2` -> exit 2 with `launch job: invalid invocation or unavailable private state`; `HOME=/` -> unknown; `HOME=/nonexistent` -> ordinary; no uv on PATH -> exit 2; `env -u HOME bash launch-job-identity.sh </dev/null` (adapter mode) -> silent exit 0 (lines 20-22).

**uv process topology:** inside the hook, `uv run --no-project python -c` reported its parent's `comm` as `uv` and the same session id as the hook. So uv keeps Python as a **child** (it does not exec into Python) and does **not** call `setsid`; `identify` with no PID therefore resolves the hook's session.

**Git and setsid:** in every case the hook's session equalled git's session; git did not create a new session for the hook. Only the explicit `setsid` in the command changed it.

**Killed supervisor (second experiment, `/tmp/l2-ident2.XXXXXXXX`, removed afterwards):** a governed `sleep 30` job; record `jobs/312063.json` mode `-r--------` (0400), 1 link, 118 bytes, compact JSON `{"pid":312063,"start":100959094,"boot":"0f93...","kernel_sid":312063,"session_id":"sidB"}`. `identify <sleep pid>` -> governed. After `kill -9` of the supervisor: `identify <sleep pid>` -> **unknown**. After the sleep was also killed, `jobs/312063.json` **remained** (the cleanup `finally` at lines 341-359 never ran). A normal job's record was removed on completion (jobs dir empty after the first experiment, line 359).

**Stale-record consequence (inferred from the code, not reproduced):** a stale `jobs/<N>.json` stays until removed by hand. If any later process becomes session leader with the reused PID `N` (for example a human's new terminal), `identify` for that human's processes finds the stale record, `proc(N)` succeeds with `actual_sid == N` but different start ticks (line 234) -> **unknown**. Under the owner's decision, that human's push to `main`/`master` would be refused. This is a false refusal of a human, rare (requires PID reuse after a killed supervisor) but real.

`/proc` here is mounted `rw,nosuid,nodev,noexec,relatime` with no `hidepid` option.

### Key Takeaways

- Real git confirms: same kernel session through git and the hook; `identify`, `identify $$` and `identify $PPID` agree in every case.
- Bypasses that yield ordinary (allowed): `setsid`, and a different valid `HOME`. Cases yielding unknown: HOME unset/relative, invalid level content, killed supervisor. No-uv yields exit 2 with no verdict.
- A killed supervisor leaves a stale `jobs/<sid>.json` forever; PID reuse can later turn a human into `unknown`.

## 4. Verdicts and what each means for a protected push

The design's hook behaviour (§19.3 line 518, seed brief lines 22-25) plus the owner decision (seed brief line 73) give this mapping. "Protected" means some record's field 3 is exactly `refs/heads/main` or `refs/heads/master`.

| `identify` result | Produced at | Meaning | Protected push | Other pushes | Stream reading |
|---|---|---|---|---|---|
| `{"status": "governed", "session_id": S}` | line 242 | PID is in the kernel session of a live, same-uid, same-boot supervisor whose logical session `S` has a valid level record | **refuse whole push**, nonzero, diagnostic | allow | read to EOF (§19.3) |
| `{"status": "ordinary"}` | line 225 | no store / no `jobs` dir / no `jobs/<sid>.json` for this session | allow | allow | none: exit 0 silently (§19.3 "Unselected ordinary pushes are allowed without ... stream inspection") |
| `{"status": "ordinary", "reason": "released"}` | line 241 | live job, but `sessions/S` (or `sessions/`) was deleted: the person released it | allow | allow | none |
| `{"status": "unknown"}` | lines 244, 535 | a registered or required identity could not be validated: bad HOME, unsafe store, bad record, dead/reused/zombie/foreign supervisor, other boot, invalid level, bad PID argument | **refuse, with its own diagnostic** (DECIDED) | **allow** (DECIDED) | read to EOF (needed to know whether it is protected) |

**Unknown handling is DECIDED, not open:** the owner decided on 2026-11-08 (seed brief line 73, "Orca answer to msg_60b98182bb31") that `unknown` refuses only pushes to `main` or `master`, with a diagnostic, and allows everything else.

### What the code must return for the decision to be implementable

1. **Three distinguishable verdicts on stdout with exit 0.** The code does this today (lines 225, 241, 242, 244, 536-537). The hook must tell `ordinary` (including `reason: released`) apart from `unknown`; both are separate `status` values, so it can.
2. **`unknown`, never `ordinary`, whenever a registered identity exists but cannot be validated.** The code does this: every validation failure after the record is found (lines 227-237, 183-184) raises into line 243. `ordinary` comes only from a `FileNotFoundError` in the lookup (line 224) or in `governed()` (line 240).
3. **"No verdict" must be handled by the hook, because the code does not turn it into `unknown`.** When uv is absent (exit 2, line 53), the arguments are malformed (exit 2, line 564), uv itself fails, the script is missing, or the call is killed/times out, stdout carries no `status`. For the decision to hold, the hook must treat every non-zero exit, empty or unparseable stdout or an unexpected `status` value exactly like `unknown` (refuse protected, allow others). Treating it as ordinary would let a governed job escape by running with a `PATH` lacking `uv` (observed in section 7). This is a hook-side requirement; the selector needs no change for it.
4. **Accepted residual: cases that return `ordinary` for a governed job** cannot be fixed by the hook, because they are indistinguishable from a human: `setsid` (section 3), a different but valid `HOME` (section 2), a deleted/missing store or `jobs` dir. These are allowed under the decision and must be listed as L2 limits (the seed brief lists `setsid` at line 45).
5. **Side effect on humans:** `unknown` also hits humans in some cases, so the decision restricts some human pushes to `main`/`master`: a human pushing with `HOME` unset or relative; a home directory that is group- or other-writable (line 109 rejects `0o022`, e.g. a `0775` home); and a human whose session id coincides with a stale record from a killed supervisor (section 7). This is a narrowing of the design invariant "an ordinary human push in the same worktree is never restricted" (design line 493) that the spec should state.
   - **Added in the Gate 1 cycle 0 fix: a human whose PATH lacks uv cannot push to `main`/`master`.** Item 3 maps "no verdict" to `unknown`. Read evidence from `src/superclaude/hooks/scripts/launch-job-identity.sh`: the no-store early exit (lines 20-24, "Missing ordinary state must not require UV", line 19) runs only when `$# == 0` or the single argument is `hook`; it does not run for `identify`. Line 25 then runs `if ! command -v uv`, and for any other argument list (including `identify [PID]`) the script prints `launch job: UV is required for this invocation` and exits 2 (lines 52-53), even when no launch store exists at all. The pre-push hook inherits the pusher's PATH (04 E28: PATH is the caller's PATH with `/usr/lib/git-core` prepended), and 04 E28c observed `uv=UV-ABSENT` with `PATH=/usr/lib/git-core:/usr/bin:/bin`. So a human who pushes from a shell whose PATH lacks the uv directory gets exit 2 from `identify`, the hook treats it as `unknown`, and a push to `main`/`master` is refused; other pushes are allowed. The script was not run for this fix (the fix rules forbid running scripts under `src/superclaude/hooks/`); this behaviour is inferred from the Read lines above and the E28c observation.
   - **An absolute uv path in the hook alone does not fix it.** Even if the hook invokes the script with an absolute uv path in mind, the script itself resolves uv through PATH twice: `command -v uv` (line 25) and `exec uv run --no-project python -I -c "$launch_identity_code" "$0" "$@"` (line 566). Hook-side options the spec can choose from: (i) the hook sets a fixed PATH that contains the uv directory recorded at install time before calling `identify` (covers both script lines); (ii) the hook applies the no-store early exit itself, treating an absent `$HOME/.claude/state/launch-level` as `ordinary` without calling `identify` (mirrors lines 20-24; it helps only users with no store, so it does not help a human on a machine that also runs governed sessions, and whether HOME-unset should also short-circuit is a separate spec decision, because item 5 currently lists HOME-unset as `unknown`); (iii) a pure-shell hook that does not depend on uv. Options (i) and (iii) cover the human-with-store case; (ii) does not on its own.

### Key Takeaways

- governed: refuse protected; ordinary/released: allow without reading the stream; unknown: refuse protected with a distinct diagnostic, allow the rest (DECIDED).
- The selector already returns `unknown` for every validation failure; the hook must also map "no verdict" (non-zero exit, no uv, bad output) to the `unknown` path.
- `setsid` and a different valid HOME produce `ordinary` and are accepted limits, not fixable in the hook.
- A human whose PATH lacks uv gets exit 2 from `identify` (no-store early exit does not cover `identify`), which maps to `unknown` and refuses that human's push to `main`/`master`; the hook must fix PATH itself or not depend on uv (item 5).

## 5. Validation fields that can fail inside a hook process (lines 227-237)

All fields are compared against what `supervise()` recorded about itself (lines 297-300).

- **`pid` / `kernel_sid` equal to the looked-up `sid` (line 229):** always true for a record written by `supervise()` (it is a session leader, line 292-293). Fails only for a hand-edited or corrupt record.
- **Start ticks (`start`, line 234):** `proc(value['pid'])[2]` must equal the recorded `starttime`. In a hook this fails only when the supervisor PID now belongs to a different process (PID reuse after the supervisor died). It cannot drift for a live supervisor. If the supervisor PID is simply gone, `proc` raises `FileNotFoundError` first -> unknown (observed after `kill -9`, section 7).
- **State `Z` (line 234):** the supervisor is a zombie, i.e. dead but not yet reaped by `run()`'s `waitpid` (line 392). Possible for a short window, or for longer if the `run` process is stopped.
- **`actual_sid != sid` (line 234):** the PID was reused by a process that is not that session's leader.
- **`boot_id` (line 234, `boot()` lines 210-212):** `/proc/sys/kernel/random/boot_id` is per kernel boot, so it differs only for a record that survived a reboot (the store is in HOME and persists). A hook on the same running kernel reads the same value. Inside a container the value is the host kernel's (not namespaced) `[UNVERIFIED here: no container test was run]`.
- **uid (line 236, plus `store()` lines 109, 116 and `private()` line 83):** the hook's effective uid must own `/proc/<sid>`, HOME, every store directory and the files. It fails if the push runs as another user (`sudo git push`, or git started by a different-user wrapper): `store()` raises `ValueError('unsafe home')` -> unknown. A non-dumpable supervisor would make `/proc/<sid>` root-owned -> `foreign supervisor`; the supervisor is an ordinary `python3` process (observed `comm` in section 7), so this should not occur `[UNVERIFIED for setuid or capability-bearing Python builds]`.
- **PID namespace:** `proc()` reads the hook's own `/proc`. If the push runs inside a different PID namespace with its own `/proc` (a sandbox wrapper such as `bwrap --unshare-pid`), the numbers no longer match the host-namespace PIDs the supervisor recorded `[UNVERIFIED: not tested]`. The likely result is `ordinary` (no `jobs/<nssid>.json`) or `unknown`, depending on number collisions.
- **`/proc` readability:** same-uid `/proc/<pid>/stat` is readable; `hidepid` does not hide same-uid processes. Here `/proc` has no `hidepid` option.

### Key Takeaways

- Inside a normal hook (same user, same kernel, same PID namespace, live supervisor) none of start ticks, boot_id or uid can fail; they fail on PID reuse, reboot-surviving records, a different user, or a dead/zombie supervisor.
- A different user (`sudo`) gives `unknown`; a different PID namespace is untested.

## 6. `publish()` (lines 164-174) and reuse for installing a hook

### Exact syscalls and flags

1. `tmp = '.' + uuid.uuid4().hex` (line 165): a hidden name, `.` + 32 hex characters.
2. `os.open(tmp, O_WRONLY | O_CREAT | O_EXCL | O_NOFOLLOW, 0o600, dir_fd=parent)` (line 166) -> `openat(parent, tmp, O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC, 0600)` (Python adds `O_CLOEXEC` because fds are non-inheritable by default). `O_EXCL` guarantees a fresh inode; the mode is filtered by the umask.
3. `os.fdopen(fd, 'wb')` then `write(json.dumps(value, separators=(',', ':')).encode())` and `flush()` (lines 168-170): buffered `write(2)` calls; **no `fsync`** of the file or the directory.
4. `os.fchmod(fd, 0o400)` (line 171): read-only for the owner, applied before the file is visible under its final name. The file is closed when the `with` ends.
5. `os.link(tmp, name, src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)` (line 172) -> `linkat(parent, tmp, parent, name, 0)`. `linkat` **fails with `EEXIST` if `name` exists**, so an existing file is never replaced, and the final name appears atomically with complete content.
6. `finally: os.unlink(tmp, dir_fd=parent)` (lines 173-174) -> `unlinkat`, on success and failure. After success the inode has one link again, which matches `read_file()`'s `st_nlink == 1` requirement (line 149).

Observed: the job record was `-r--------`, 1 link, compact JSON (section 7).

### Can `publish()` install an executable `pre-push` unchanged? No.

- **Payload is JSON-encoded (line 169).** Passing the hook text as a string would write `"#!/bin/bash\n..."` with quotes and escapes, which is not a runnable script. Passing bytes fails (`json.dumps` rejects `bytes` with `TypeError`).
- **Mode `0o400` (line 171) is not executable.** Git runs a hook only if it is executable (`access(X_OK)`); a non-executable `pre-push` is skipped (git prints an `advice.ignoredHook` hint), so the push is not checked. `l2_status()` would also report `absent` (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` lines 1025-1028 check `is_file()` and `os.access(hook, os.X_OK)`).
- **Temp name `.<uuid hex>` (line 165)** in the hooks directory is harmless to git (git looks up hooks by exact name), but a `SIGKILL` between lines 166 and 174 leaves a stray `.<hex>` file in `hooks/`.
- **No fsync:** after a power loss a just-linked hook could exist with missing data on some filesystems; the ownership check below would catch the mismatch.
- **The pattern is reusable:** `O_EXCL` temp + `fchmod` + `linkat` no-replace + temp unlink is exactly "publish a complete file without replacing an existing one, including a concurrent foreign install" (design line 512). A hook installer needs a variant that writes raw bytes and uses an executable mode (for example `0o500` or `0o755`); that is new code, not a call to `publish()`.
- `publish()` also lives inside the heredoc Python program, so it is not importable from `install_hooks.py` or `orca_worktree.py`; reuse means copying the pattern.

### What the ownership and self-test check after publication must compare

Design line 512: "recheck exact owned version/content before reuse. A header alone is not sufficient ownership proof." `[CODE-VERIFIED as absent]`: no such check exists today; `l2_status()` (lines 1012-1029 of `orca_worktree.py`) only checks `is_file()` and `X_OK` and returns `present-unverified` (seed brief line 39 "trusts any executable pre-push" is consistent with the code). For contrast, L1 uses a single version header line, `GUARD_VERSION_LINE = "# launch-level-guard-version: 1"` (`orca_worktree.py` line 804), which the design says is not enough for L2.

After `linkat` succeeds, or when an existing `pre-push` is found (including `EEXIST` from a concurrent installer), the check must compare, on the path git will actually run (`git rev-parse --git-path hooks/pre-push`, with `core.hooksPath` unset):

- **Full content equality** with the packaged hook bytes of the expected version (byte comparison, or a hash of the whole file computed by the installer), not a header or version line. The version marker inside the content is covered by that equality.
- **File type and identity:** opened with `O_NOFOLLOW`, a regular file, not a symlink; ideally the same `st_dev`/`st_ino` as the inode just linked, so a swap between link and check is seen.
- **Owner and mode:** owned by the installing uid and executable by it (what git requires), not group/other-writable.
- **Self-test:** run the installed file as git would (with a pre-push stdin) and require the expected results, at least: an ordinary context with a protected record exits 0 without output, and an empty stream exits 0. A governed-context self-test needs a real supervisor (`prepare` + `run`), which is heavier; whether the installer self-test must cover it is not settled (seed brief line 76 leaves the comparison method open).
- On `EEXIST` with identical owned content: reuse. With anything else: keep the file and report `W-L2-ABSENT` with the reason (design line 514).

### Key Takeaways

- `publish()` = `openat(O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, 0600)` + write + `fchmod 0400` + `linkat` (no replace) + `unlinkat` temp; no fsync.
- It cannot install a hook unchanged (JSON payload, mode 0400); its no-replace pattern can be copied with raw bytes and an executable mode.
- Ownership must be full-content equality of the file git will run, plus type, owner and mode checks and a self-test; `l2_status()` checks none of this today.

## 8. Dependencies and integration points

**Inbound (who uses the script):**

- `src/superclaude/hooks/hooks.json` line 130 registers `~/.claude/hooks/launch-job-identity.sh` as a PreToolUse command (adapter mode, no arguments); the plugin mirror `plugins/superclaude/hooks/hooks.json` line 100 does the same.
- `src/superclaude/cli/install_hooks.py` line 90 lists `launch-job-identity.sh` for installation.
- `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` line 803: `IDENTITY_COMMAND = "~/.claude/hooks/launch-job-identity.sh"`.
- Tests: `tests/hooks/test_launch_job_identity.py`, `tests/hooks/test_launch_level_guard_with_identity.py`, `tests/cli/test_install_hooks.py` (lines 934-1003).
- Copies: `plugins/superclaude/hooks/scripts/launch-job-identity.sh` and the installed `~/.claude/hooks/launch-job-identity.sh` are byte-identical to the source (checked with `cmp`, 2026-11-08); the installed copy is mode `0755`.

**Outbound (what it needs):** `/bin/bash`, `uv` on `PATH`, a Python with `ctypes` and `fcntl` (Linux), `/proc/<pid>/stat`, `/proc/sys/kernel/random/boot_id`, the HOME store `~/.claude/state/launch-level/{sessions,jobs,requests}`; `jq` only for the uv-less adapter fallback.

**Where a pre-push hook calls in:** `~/.claude/hooks/launch-job-identity.sh identify` (no PID; the Python process inherits the hook's session), with the hook's inherited `HOME` and `PATH`. How the hook finds the script, and what it does if the script is missing, is still open (seed brief line 78); by the reasoning in section 4 item 3, a missing script is a "no verdict" and should follow the `unknown` path.

**Cost:** each `identify` call starts `uv` and a Python interpreter (uv stays as the parent, section 7). Not measured; it is per push, not per ref.

### Key Takeaways

- The hook's entry point is the installed `~/.claude/hooks/launch-job-identity.sh identify`, resolved under the inherited HOME.
- The script is installed and mirrored byte-identically; any L2 change to the selector must keep the three copies in sync.

## Gaps and Questions

1. **"No verdict" mapping is not in the code.** `identify` exits 2 with no stdout when uv is absent (line 53); the hook must map it to the `unknown` path. Not yet written down in the design.
2. **`ordinary` escapes:** `setsid` (lines 7-8, 219-225) and a different valid `HOME` (lines 103-106, 224-225) make a governed push ordinary. Only `setsid` is listed in the seed brief (line 45); the HOME escape is not listed anywhere I found.
3. **Stale records after a killed supervisor are never pruned** (lines 341-359 do not run on `SIGKILL`; observed). With PID reuse they turn an unrelated human session into `unknown`, which the owner's decision turns into a refused human push to `main`/`master`. Should the L2 spec add pruning of dead records (a mutation the selector deliberately avoids) or accept this?
4. **Humans restricted by `unknown`:** HOME unset/relative, a group-writable home (line 109), stale-record collisions. The design invariant at line 493 ("never restricted") needs a stated exception for the decided `unknown` policy.
5. **PID-namespace and container behaviour** `[UNVERIFIED]`: not tested; boot_id inside a container `[UNVERIFIED]`.
6. **Non-dumpable / setuid Python** making `/proc/<sid>` root-owned `[UNVERIFIED]`.
7. **Self-test scope** for the installed hook (governed fixture or ordinary only) is not settled (seed brief line 76).
8. **Script lookup and missing-script behaviour** from the hook is open (seed brief line 78).
9. Header comment line 4 says `run` waits for "ordinary non-zombie descendants"; the code waits for non-zombie members of the kernel **session** (lines 263, 332, 338), not descendants via the PPID chain. A detached descendant that called `setsid` is not waited for. Marked `[CODE-CONTRADICTED]` in wording only (the behaviour is session membership, which includes adopted orphans under the subreaper but excludes `setsid` children).
10. Design line 557 says `identify` "inspects actual kernel process-session membership" `[CODE-VERIFIED]` (line 219) and that `unknown` is for "malformed/stale/unreadable registered identity" `[CODE-VERIFIED]` (lines 227-244), but `unknown` is also returned when HOME is unset/relative/unsafe even with no registered identity (lines 104-110 via 243), which the design sentence does not mention.

## Stale Documentation Found

- No **[STALE DOC]** in the strict sense: every structural claim checked in design §19.7 (lines 549-561) matches the code (selector by kernel session, three verdicts, release by deleting the level record, `setsid` escape, uv/jq preflight, byte-identical plugin mirror).
- Wording imprecision, not staleness: header line 4 "descendants" vs session membership (Gaps item 9); design line 557 omits the HOME-driven `unknown` cases (Gaps item 10).
- Design §19.1 lines 495-502 describe a controller-PID ancestry walk; the design itself labels it historical and not the implemented contract, and the code has no ancestry walk (line 253). Correctly labelled; a reader must not take it as current.

## Summary

`identify [PID]` selects by kernel session membership only: it reads field 6 of `/proc/<pid>/stat`, looks up `jobs/<sid>.json` in the HOME store and validates the live supervisor's pid, start ticks, boot id, uid and the origin session's level record; it never walks the PPID chain (lines 202-248). A pre-push hook can call it with no PID because uv keeps Python as a child in the same session, and real-git experiments showed hook, git and supervisor sharing one session, with `identify`, `identify $$` and `identify $PPID` agreeing in every case. Missing state yields `ordinary`, any validation failure or bad HOME yields `unknown`, while `setsid` and a different valid HOME make a governed push `ordinary` (allowed), and a PATH without uv yields exit 2 with no verdict, which the hook must route to the DECIDED `unknown` policy (refuse only `main`/`master` with a diagnostic, allow the rest). `publish()` is an `O_EXCL` temp + `fchmod 0400` + `linkat` no-replace publication; its pattern fits a no-clobber hook install, but it cannot be reused unchanged because it JSON-encodes the payload and leaves the file non-executable. Ownership after publication must be a full-content comparison of the file git will actually run, plus type, owner, mode and a self-test, which today's `l2_status()` does not do.
