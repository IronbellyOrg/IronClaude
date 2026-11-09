# Task 1 evidence: FR-025 unknown shape

## Change

`identify()` in `src/superclaude/hooks/scripts/launch-job-identity.sh` (mirror byte-identical, `cmp` clean):

- The record path is set at `:226`, after `store()` and `subdir(root, 'jobs')` succeed: `$HOME/.claude/state/launch-level/jobs/<sid>.json` (absolute, since `store()` rejects a HOME that does not start with `/`).
- Before that point (bad pid, bad or unsafe HOME, unsafe store or jobs dir) the output stays plain `{"status": "unknown"}`.
- After it: `{"status": "unknown", "reason": R, "record": P}`, key order `status, reason, record`.
  - `orphaned` (`:240`, `:243`): `proc(value['pid'])` raises `FileNotFoundError`/`ProcessLookupError` (pid gone), or state is `Z`.
  - `stale` (`:247`): sid mismatch, start-ticks mismatch or boot-id mismatch. The sid mismatch is classed `stale` per OC-3's proposed resolution (owner to confirm).
  - `foreign` (`:250`): `/proc/<sid>` uid differs from the euid.
  - `unreadable` (default, `:220`): every other caught exception once P is known (bad JSON, bad fields, unsafe mode, symlinked record, a `boot()` read error, a broken session level file).
- `main()` `:551` (`identify` raising `ValueError` for a non-integer pid argument) still prints the plain line.

## U-12: tests asserting the old plain line

Grep `"unknown"` in `tests/hooks/test_launch_job_identity.py` before editing:

| Line (before) | Text | Record exists? | Action |
|---|---|---|---|
| :387 | `assert job.identify(live[0]) == {"status": "unknown"}` (zombie_or_dead) | yes | moved to `_unknown("orphaned", path)` (now :387) |
| :408 | `assert job.identify(pid) == {"status": "unknown"}` (pid/start/boot/json/sid/mode) | yes | moved: `stale` for start and boot, `unreadable` for pid, json, sid, mode (now :409) |
| :429 | `assert job.identify(pid) == {"status": "unknown"}` (broken session level) | yes | moved to `_unknown("unreadable", record)` (now :436) |
| :498-500 | `job.identify(2147483647 / -1 / "not-a-pid") == {"status": "unknown"}` | no (pid fails first) | kept plain (now :505-507) |
| :533 | `assert job.identify() == {"status": "unknown"}` (symlinked or relative HOME) | no (store fails) | kept plain (now :540) |
| :544 | `assert job.identify(pid) == {"status": "unknown"}` (symlinked record) | yes | moved to `_unknown("unreadable", path)` (now :551) |
| :1201 | `identity = json.loads(selected.stdout) if selected.returncode == 0 else {'status': 'unknown'}` | n/a | fixture policy fallback, not a selector assertion; unchanged |
| :1474 | `wait_for(lambda: job.identify(child) == {"status": "unknown"})` (killed supervisor) | yes | moved to `_unknown("orphaned", record)` (now :1481) |
| :1481 | `assert row["identity"] == {"status": "unknown"} and row["refused"] is False` | yes | moved to `_unknown("orphaned", record)` (now :1488) |

New helper `_unknown(reason, record)` at :415-417. Reasons now pinned: `orphaned` (zombie_or_dead, killed supervisor), `stale` (start, boot), `unreadable` (pid, json, sid, mode, broken level, symlinked record), plain shape (no record).

Not pinned: `foreign` needs a second uid (U-7, none set up here); the `stale` sid-mismatch branch has no practical trigger (see U-6: pid S cannot belong to another session while the caller still has sid S).

## U-6: does the stale `rm` remedy wording hold?

Evidence in the script:

- `:202-207` `proc()` reads `/proc/<pid>/stat`, splits after the last `)`, and returns `fields[0]`, `fields[3]`, `fields[19]` = stat fields 3 (state), 6 (session) and 22 (starttime, clock ticks since boot). Confirmed on this kernel: `state R session 4168757 ==getsid True start 103350274` (`uv run python` reading `/proc/self/stat` with the same split).
- `:210-212` `boot()` reads `/proc/sys/kernel/random/boot_id`, which changes on every boot.
- `:315` the record is written with the supervisor's own `pid`, `start` and `boot()`, and `pid == kernel_sid == sid` (checked at `:233`).

Reasoning: a pid number is not reused while its process exists (zombies included), and POSIX does not reuse a pid while a process group with that id exists; Linux also keeps the pid number allocated while any task still uses it as a session id (kernel pid refcounting; stated from kernel behaviour, not re-read here). So if the pid in the record now has other start ticks, or the boot id differs, the supervisor that wrote the record has exited and the session it led is gone: no launch job owns that record, which is what the `stale` remedy says. `orphaned` (pid gone or zombie) is not given the `rm` remedy: there the old session can still have live members (LIM-3), so the record is kept as evidence.

Finding: the check holds; the `rm` remedy wording for `stale` only (source §7.3) is kept. That text lives in C1 (the pre-push hook, a later task); this task adds no remedy text. Caveat: between `identify` and a person's `rm` a race is possible in principle, but a new supervisor cannot publish a record over the stale one (`publish()` uses `os.link`, which fails on an existing name), so the `rm` can only remove the old record.

## U-14(b): non-test readers of `"status": "unknown"`

Grep of `src`, `plugins`, `docs`, `scripts` and the repo root, excluding `tests/`, `.dev/`, `.claude/`:

- Only hits: the selector itself (`launch-job-identity.sh:259`, `:260`, `:551`, src and plugin mirror).
- The only caller of `identify()` is `main()` (`:549`), which prints the result.
- `orca_worktree.py:803` `IDENTITY_COMMAND` is used only to check the PreToolUse registration (`:1001`, `:1004`); it never runs `identify` or reads its output.
- `hooks.json` (src `:130`, plugin `:100`) registers the script as a hook; it does not parse `identify` output.
- No doc in `docs/`, skills, core or commands quotes the unknown line.

Finding: no non-test consumer reads the unknown line today; the new keys break no reader. The first reader will be C1 (FR-022 shape 5).

## Result

- `make sync-dev` done; `make verify-sync`: `All components in sync.`
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/hooks/test_launch_job_identity.py -q`: `151 passed in 38.00s`
