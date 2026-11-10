# T2: U-4 clean-HOME check for the C1 pre-push hook

Question (source §11 U-4): is `env -i` with HOME, PATH and `UV_NO_CONFIG=1` enough for the selector's `uv run`, or are more variables (`UV_CACHE_DIR`, `XDG_*`) needed?

Status: SETTLED, 2026-11-08. **The FR-021 environment is enough. No extra variable is needed.**

## Setup

- Host: Linux, uv 0.11.8 at `/usr/local/bin/uv`, `/usr/bin/python3` present.
- A fresh `mktemp -d /tmp/t2-u4.XXXXXXXX` dir, holding:
  - `home/`, which starts with only `.claude/hooks/launch-job-identity.sh`. That is a copy of the Task 1 selector: no uv cache, no uv config, no managed Python.
  - `hooks/pre-push`, a copy of `launch-level-pre-push.sh`.
  - `hooks/pre-push.launch-level`, mode 0600, containing `<tmp>/home\n/usr/local/bin\n`.
- The two runs were done with separate fresh dirs. Both dirs were removed afterwards (`rm -rf`, checked with `[ -e ]`).

## Runs

1. The selector run directly with the exact FR-021 line, with stderr shown:
   `( cd / && exec /usr/bin/env -i HOME=<tmp>/home PATH=/usr/local/bin:/usr/bin:/bin UV_NO_CONFIG=1 /usr/bin/timeout 10 <tmp>/home/.claude/hooks/launch-job-identity.sh identify "$$" ) </dev/null`
   - It printed `{"status": "ordinary"}` with exit 0 and nothing on stderr.
   - uv created its cache at `<tmp>/home/.cache/uv`, the default under HOME.
   - `uv python find` under the same environment resolved `/usr/bin/python3`.
2. The hook run end to end with the pusher environment also cleared (`env -i HOME=/nonexistent PATH=/usr/bin:/bin <tmp>/hooks/pre-push origin url`), with a job record `jobs/<kernel sid>.json` containing `{}`:
   - A push to `refs/heads/main` exited 1 with `L2-UNKNOWN (job record unreadable at <tmp>/home/.claude/state/launch-level/jobs/<sid>.json)` and the two-line text. That shows the real selector ran and its FR-025 line was parsed. The run took 0.13 s.
   - A push to `refs/heads/feat` exited 0 and printed nothing (OD-2).
   - With no launch-level state present, a push to `refs/heads/main` exited 0 and printed nothing (ordinary).

## Result

- `HOME`, `PATH=<uv dir>:/usr/bin:/bin` and `UV_NO_CONFIG=1` are enough. uv takes its cache directory from HOME, so `UV_CACHE_DIR` and `XDG_*` are not needed.
- The hook does not pass `LC_ALL` to the child, because FR-021 fixes the exact command line. The hook sets `LC_ALL=C` for itself only.

## Limits of this check

- The check used a host where `/usr/bin/python3` exists. On a host whose only Python is uv-managed, the Python lives under the pinned HOME's `~/.local/share/uv/python`. That is the real HOME in production, so it should resolve the same way, but this check did not run that case.
- If no Python can be found, uv may try to download one. That run is bounded by `timeout 10` and gives `identity check timed out` or `identity check failed`, which fails to `unknown`.
- The governed shape was not run against a real supervisor; Task 4's tests cover it. The governed path was checked with a stub selector only.
