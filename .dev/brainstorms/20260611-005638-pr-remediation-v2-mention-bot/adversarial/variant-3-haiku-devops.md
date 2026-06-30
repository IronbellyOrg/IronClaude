---
title: "PR Auto-Remediation V2.0 — DevOps Variant"
lens: devops
model: haiku
created: 2026-06-11T01:15:00Z
---

# V2.0 PR Auto-Remediation — DevOps Variant

## Execution-Host Ops Comparison

Three candidate hosts for the headless remediation process, evaluated on operational grounds relevant to an on-prem deployment:

| Criterion | One-Shot Runner (cron/systemd timer) | Persistent Daemon (long-lived Python process) | Webhook Service (HTTP listener) |
|---|---|---|---|
| **Process supervision** | Native systemd — `OnUnitActiveSec`, `OnCalendar` polling; auto-restart via `Restart=on-failure` | systemd unit with `Restart=always`; needs graceful drain on stop | systemd or container; needs healthcheck endpoint; liveness probes |
| **Secret-at-rest exposure** | Secrets sourced per-run from `~/.aienv` into the process env; zero disk cache after exit | Secrets loaded once at startup; live in process memory until restart | Same as daemon; plus TLS cert management for the webhook endpoint |
| **Restart safety** | Trivial — next timer tick picks up; state store on disk covers mid-run restarts | Needs SIGTERM handler to flush round state to disk before exit | Same as daemon; additionally needs request-idempotency on redelivery |
| **Observability** | Structured logging via journald + JSONL ledger file per run | Long-running process: structured log + metrics endpoint (Prometheus) | Same as daemon + HTTP access logs |
| **Deploy complexity** | Lowest — systemd timer unit + env file; no network ports, no TLS | Low — single Python service; one TCP port for optional metrics | Medium — reverse proxy + TLS cert + firewall rules for GitHub webhook delivery |
| **Latency** | 30–60s poll interval (configurable); bounded jitter | Near-instant on webhook receipt (if paired with event source) | Near-instant (GitHub delivers within seconds) |
| **Idle cost** | Zero when idle; process starts/stops per poll | Constant CPU/RAM footprint (~50–100MB Python process) | Same as daemon; reverse proxy idle cost negligible |
| **GitHub API 403 backoff** | Natural: next tick provides backoff window | Must implement exponential backoff in-process | Must implement exponential backoff in-process |
| **Secret rotation** | Automatic on next tick — re-sources `~/.aienv` | Requires SIGHUP handler to re-read env file | Same as daemon |
| **Operational simplicity** | **Best** — no ports, no TLS, no daemon lifecycle complexity | Good — one long-lived process to monitor | Moderate — external endpoint, TLS, GitHub webhook registration |

**Ops-preferred pick: Persistent Daemon with API polling (not webhook).**

Rationale: The daemon wins on the balance of restart safety, observability depth (long-lived metrics), and operational simplicity. Webhooks add TLS, reverse-proxy, and firewall surface for marginal latency gain (seconds vs. 30s is irrelevant for remediation). One-shot runner loses on idempotency complexity (partial-run cleanup on crash) and lacks the ability to maintain in-memory round state across polls. A daemon running behind a systemd unit gives us:

- Native process supervision (`Restart=always`, `WatchdogSec=60`)
- Graceful shutdown via SIGTERM (flush state, finish current round)
- Continuous in-memory round-state with periodic disk flush
- Zero network attack surface (no inbound ports)
- Natural poll-interval rate-limit discipline

The daemon polls `gh api repos/IronbellyOrg/IronClaude/pulls?state=open` at 30s intervals, checks reply-comments for bot mentions, and processes triggers in a bounded execution loop.

## Process Lifecycle & Supervision

### Systemd Unit

```ini
# /etc/systemd/system/pr-remediation-bot.service
[Unit]
Description=PR Auto-Remediation Bot (headless, on-prem)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=remediation-bot
Group=remediation-bot
WorkingDirectory=/opt/pr-remediation-bot
EnvironmentFile=/opt/pr-remediation-bot/.env
ExecStart=/opt/pr-remediation-bot/.venv/bin/python -m superclaude.cli.bot_daemon
Restart=always
RestartSec=10
WatchdogSec=60
NotifyAccess=main
StandardOutput=journal
StandardError=journal
SyslogIdentifier=pr-remediation-bot

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/opt/pr-remediation-bot/state /opt/pr-remediation-bot/logs
PrivateTmp=true
RestrictSUIDSGID=true

[Install]
WantedBy=multi-user.target
```

### Lifecycle States

1. **Startup**: Load env from `.env` (sourced from `~/.aienv` patterns), initialize state store at `/opt/pr-remediation-bot/state/`, connect to journal logger.
2. **Idle/Polling**: 30s poll cycle, conditional requests via `If-None-Match` on PR list ETag.
3. **Trigger Processing**: On detecting a valid @-mention trigger, acquire a per-PR lock file (`state/locks/pr-<N>.lock` with `flock`), execute the remediation round, release lock.
4. **Drain on SIGTERM**: Finish the current round (up to 60s grace), flush all in-memory state to disk, exit 0. Systemd restarts if the exit was not clean.
5. **Watchdog**: If no systemd watchdog notification within 60s, systemd restarts the process (prevents silent hangs).

### The Daemon Entry Point

The daemon reuses `ClaudeProcess` (`src/superclaude/cli/pipeline/process.py:72`) as the headless executor. The daemon orchestrates: poll -> detect -> authz -> parse -> spawn ClaudeProcess -> validate -> push -> reply -> resolve -> log.

## Secret Delivery & Rotation

### Runtime Secret Loading

The daemon sources secrets from a dedicated `.env` file at startup, modeled on the `~/.aienv` proxy contract and the `ccsession.env` chmod-600 precedent:

```bash
# /opt/pr-remediation-bot/.env (chmod 600, owner=root:remediation-bot)
ANTHROPIC_BASE_URL=http://on-prem-proxy:4000/cli
ANTHROPIC_AUTH_TOKEN=<proxy-auth-token>
GH_TOKEN=<personal-access-token-with-repo-write>
REPO_OWNER=IronbellyOrg
REPO_NAME=IronClaude
```

**Critical discipline:**
- Secrets are **never** passed as CLI arguments. The daemon reads them into `os.environ` before spawning `ClaudeProcess`, which inherits via `env_vars` or `os.environ.copy()`.
- The `.env` file is `chmod 600`, owned by `root:remediation-bot`, unreadable by other users.
- `GH_TOKEN` is a fine-grained PAT scoped to: `Contents: Read/Write`, `Pull requests: Read/Write`, `Metadata: Read-only` on `IronbellyOrg/IronClaude` only.
- The daemon logs `[MASKED]` for any env var containing `TOKEN`, `KEY`, `AUTH`, `SECRET` — never dumps environment in any log level.

### Rotation

- **SIGHUP handler**: On `kill -HUP <pid>`, the daemon re-reads `.env` and replaces the in-memory secrets without restarting. This enables zero-downtime secret rotation.
- **Systemd `ExecReload`**: `ExecReload=/bin/kill -HUP $MAINPID` so `systemctl reload pr-remediation-bot` triggers rotation.
- **ClaudeProcess spawns**: Each new `ClaudeProcess` inherits the *current* in-memory env, so a rotation takes effect on the next remediation round.

## State Store & Idempotency

### On-Disk State Ledger

Location: `/opt/pr-remediation-bot/state/ledger.jsonl`

Each line is a JSON object representing one state transition. The ledger is append-only and survives restarts. On startup, the daemon replays the ledger to reconstruct in-memory state:

```jsonl
{"ts": "2026-06-11T01:20:00Z", "event": "trigger_seen", "pr": 142, "comment_id": 98765432, "commenter": "alice", "autonomy": "propose"}
{"ts": "2026-06-11T01:20:01Z", "event": "authz_check", "pr": 142, "commenter": "alice", "permission": "write", "result": "pass"}
{"ts": "2026-06-11T01:20:02Z", "event": "parse_mention", "pr": 142, "raw": "@bot propose", "level": "propose", "flags": []}
{"ts": "2026-06-11T01:20:03Z", "event": "round_start", "pr": 142, "round": 1, "max_rounds": 3}
{"ts": "2026-06-11T01:22:15Z", "event": "claude_process_spawn", "pr": 142, "round": 1, "opComment_summary": "fix null-deref in auth.py:42", "max_turns": 50}
{"ts": "2026-06-11T01:25:30Z", "event": "validation", "pr": 142, "round": 1, "lint": "pass", "format": "pass", "tests": "pass"}
{"ts": "2026-06-11T01:25:45Z", "event": "push", "pr": 142, "round": 1, "commit_sha": "abc123", "branch": "feature/foo"}
{"ts": "2026-06-11T01:25:50Z", "event": "reply_posted", "pr": 142, "round": 1, "reply_comment_id": 98765500, "thread_resolved": true}
{"ts": "2026-06-11T01:26:00Z", "event": "round_complete", "pr": 142, "round": 1, "outcome": "resolved", "next_action": "wait_re_review"}
{"ts": "2026-06-11T01:28:00Z", "event": "re_review_detected", "pr": 142, "round": 2, "trigger_source": "bot_own_push", "findings": 0}
{"ts": "2026-06-11T01:28:01Z", "event": "round_complete", "pr": 142, "round": 2, "outcome": "clean", "next_action": "terminate"}
```

### Idempotency Keys

- **Trigger dedup key**: `pr-<N>:comment-<id>:reply-<rid>` — the bot reply-comment ID uniquely identifies a mention. If this key exists in the processed-set, skip.
- **Round dedup key**: `pr-<N>:round-<N>` — prevents double-executing the same round on restart.
- **Processed set**: Stored as `state/processed-triggers.json` (a set of dedup keys). Rebuilt from ledger on startup.

### Lock Files

Per-PR lock: `state/locks/pr-<N>.lock` acquired via `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)`. If the lock is held, the poll cycle skips that PR (another instance or a zombie from a crash is processing it). Locks are released on round completion or on SIGTERM.

## Loop-Safety & Round Counter

### Monotonic Round Counter Design

Mirroring `cli/swarm/commands.py:2269` (`watch_max_iterations` bounded-counter pattern):

```python
class RoundGuard:
    def __init__(self, max_rounds: int = 3):
        self._max_rounds = max_rounds
        self._round = 0  # monotonic, never decrements

    @property
    def remaining(self) -> int:
        return max(0, self._max_rounds - self._round)

    def can_proceed(self) -> bool:
        return self._round < self._max_rounds

    def increment(self) -> int:
        self._round += 1
        return self._round
```

### "Own Push = Next Round" Rule

When the bot pushes a fix, GitHub will eventually trigger Augment's re-review. The daemon must recognize that this re-review is the **next round of the same remediation session**, not a new trigger:

1. After push, the daemon enters `wait_re_review` state, recording `round_push_sha` in the ledger.
2. On next poll, it checks for new Augment reviews on this PR.
3. If a new review appears and `round_push_sha` is set, the daemon increments the round counter (not a new trigger) and processes findings.
4. If the review has zero Medium+ findings, the round counter terminates with `outcome: clean`.
5. If `remaining == 0`, the daemon terminates with `outcome: max_rounds_reached` and posts a summary comment.

**Critical invariant**: The round counter is per-PR and monotonic. It is never reset by a new review, a new comment, or a host restart. The only way to reset is explicit operator intervention (clearing the state for that PR, logged as `event: operator_reset`).

### Max Rounds

- Default: 3 (conservative for auto-remediation)
- Configurable via mention flag: `@bot fix --max-rounds 5` (cap at 5)
- Stored in the per-PR state, survives restarts

## Rate-Limit Safety

### Poll Discipline

- **Base interval**: 30 seconds between poll cycles.
- **Conditional requests**: Every `gh api` call uses `--header "If-None-Match: <last-etag>"`. GitHub returns 304 for unchanged PRs, which does not count against the rate limit.
- **ETag cache**: In-memory dict `pr-<N> -> etag`, persisted to `state/etag-cache.json` on each poll and reloaded on startup.

### Backoff on 403 / Secondary Rate Limit

When `gh api` returns 403 with `Retry-After` header or secondary rate-limit body:

1. Parse `Retry-After` (seconds), or default to 60s.
2. Sleep for the backoff duration (capped at 300s).
3. Double the backoff on consecutive 403s (exponential, max 600s).
4. Log `event: rate_limit_backoff` with duration and PR.
5. Resume polling after backoff expires.

### Rate Limit Headers

After every `gh api` call, extract `X-RateLimit-Remaining` and `X-RateLimit-Reset` from response headers. If remaining < 50:
- Log a warning `event: rate_limit_warning`.
- Extend poll interval to 60s until reset time.

### Hard Stop

If remaining = 0, the daemon enters a quiescent state until `X-RateLimit-Reset` epoch passes, logging `event: rate_limit_exhausted`. No new triggers are processed during this window; triggers are queued in the ledger as `event: trigger_queued` and replayed after reset.

## Audit Ledger Schema

The per-run JSONL ledger at `/opt/pr-remediation-bot/logs/run-<PR>-<date>.jsonl` captures every state transition for forensic review.

### Schema (all events share these base fields)

```json
{
  "ts": "ISO-8601 timestamp (UTC)",
  "event": "<event_type>",
  "pr": 142,
  "trace_id": "uuid-per-remediation-session"
}
```

### Event Types

| Event | Additional Fields |
|---|---|
| `poll` | `pr_list_etag`, `changed_prs: [int]`, `rate_limit_remaining` |
| `trigger_seen` | `comment_id`, `reply_id`, `commenter`, `raw_mention_text`, `parent_comment_id` |
| `authz_check` | `commenter`, `permission`, `result: "pass|fail"`, `api_status` |
| `parse_mention` | `raw_text`, `level: "propose|fix|deep"`, `flags: []`, `parse_errors: []` |
| `round_start` | `round`, `max_rounds`, `autonomy_level`, `opComment_sha256` |
| `claude_process_spawn` | `round`, `max_turns`, `opComment_summary` (truncated, never raw), `pid` |
| `validation` | `round`, `lint: "pass|fail"`, `format: "pass|fail"`, `tests: "pass|fail|skipped"` |
| `push` | `round`, `commit_sha`, `branch`, `gh_repo_flag: "IronbellyOrg/IronClaude"` |
| `reply_posted` | `round`, `reply_comment_id`, `thread_resolved: bool` |
| `round_complete` | `round`, `outcome: "resolved|clean|max_rounds_reached|validation_failed"`, `next_action` |
| `rate_limit_backoff` | `retry_after_seconds`, `consecutive_403s`, `resume_at` |
| `error` | `error_type`, `error_message`, `recoverable: bool` |
| `shutdown` | `reason: "sigterm|watchdog|operator"`, `active_rounds`, `state_flushed: bool` |

### opComment Safety

The ledger **never** stores the raw `opComment` text (it may contain injection payloads). Instead it stores:
- `opComment_sha256`: SHA-256 hash for dedup/integrity
- `opComment_summary`: Truncated to 120 chars, with non-printable chars stripped

## Observability & Alerting

### Structured Logging

All log output goes to journald (via systemd stdout/stderr) with structured JSON:

```json
{"level": "INFO", "ts": "...", "msg": "Poll cycle complete", "prs_watched": 5, "triggers": 0, "rate_remaining": 4950}
```

### Metrics (Optional: `/metrics` HTTP endpoint on localhost:9100)

For Prometheus scraping (if operators want dashboards):

```
pr_remediation_polls_total        # counter: total poll cycles
pr_remediation_triggers_total     # counter: total @-mention triggers detected
pr_remediation_rounds_total       # counter: total remediation rounds executed
pr_remediation_round_outcomes     # counter by outcome label (resolved, clean, max_rounds, validation_failed)
pr_remediation_authz_failures     # counter: authorization rejections
pr_remediation_rate_limit_events  # counter: rate-limit backoffs
pr_remediation_active_rounds      # gauge: rounds currently in progress
pr_remediation_loop_guard_rounds  # gauge: current round number per active PR
```

### Alerting Rules

| Alert | Condition | Action |
|---|---|---|
| `RemediationLoopDetected` | `pr_remediation_active_rounds > 2` for > 10 minutes | Page on-call; daemon is stuck in a remediation cycle |
| `AuthzFailureSpike` | `pr_remediation_authz_failures > 5` in 5 minutes | Investigate: possible unauthorized access attempt |
| `RateLimitExhausted` | `rate_limit_remaining == 0` | Notify: bot is quiescent until rate limit resets |
| `DaemonDown` | Systemd service not running | Auto-restart via `Restart=always`; alert if restart count > 3 in 10 minutes |
| `ValidationFailure` | Any `validation` event with `lint: "fail"` or `format: "fail"` | Log warning; push is blocked by design (SC-4) |
| `MaxRoundsReached` | `round_outcomes{outcome="max_rounds_reached"}` increment | Notify: PR needs human attention; findings not fully resolved |

### Stuck-Run Detection

A round is "stuck" if:
1. `claude_process_spawn` event exists but no `round_complete` event within `timeout_seconds` (default 6300s = 105 min, matching `ClaudeProcess.timeout_seconds`).
2. The daemon checks every 60s: `current_time - last_event_time > timeout_threshold` for any in-progress round.
3. Action: Log `event: stuck_round_detected`, attempt to kill the ClaudeProcess (SIGTERM -> SIGKILL after 10s), flush state, emit alert.

## Deploy & Rollback

### Deployment

1. **Prerequisites**: On-prem host with Python 3.10+, systemd, network access to `on-prem-proxy:4000/cli` and `api.github.com`.
2. **Install**:
   ```bash
   # Create system user
   sudo useradd --system --no-create-home --shell /usr/sbin/nologin remediation-bot

   # Deploy application
   sudo mkdir -p /opt/pr-remediation-bot/{state,logs,state/locks}
   sudo chown remediation-bot:remediation-bot /opt/pr-remediation-bot/{state,logs,state/locks}
   sudo chmod 750 /opt/pr-remediation-bot

   # Copy application
   sudo cp -r /path/to/build/pr-remediation-bot/ /opt/pr-remediation-bot/app/

   # Create virtual environment
   sudo -u remediation-bot uv venv /opt/pr-remediation-bot/.venv
   sudo -u remediation-bot /opt/pr-remediation-bot/.venv/bin/pip install /opt/pr-remediation-bot/app/

   # Deploy secrets (chmod 600, owner root:remediation-bot)
   sudo cp .env /opt/pr-remediation-bot/.env
   sudo chown root:remediation-bot /opt/pr-remediation-bot/.env
   sudo chmod 600 /opt/pr-remediation-bot/.env

   # Install systemd unit
   sudo cp pr-remediation-bot.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable pr-remediation-bot
   sudo systemctl start pr-remediation-bot
   ```
3. **Verify**:
   ```bash
   sudo systemctl status pr-remediation-bot
   journalctl -u pr-remediation-bot --since "1 min ago" | head -20
   ```

### Rollback

1. **Stop the daemon**: `sudo systemctl stop pr-remediation-bot`
2. **Preserve state**: `sudo cp -r /opt/pr-remediation-bot/state/ /opt/pr-remediation-bot/state-backup-$(date +%Y%m%d-%H%M%S)/`
3. **Restore previous version**: Replace `/opt/pr-remediation-bot/app/` with the previous build, reinstall venv.
4. **Restart**: `sudo systemctl start pr-remediation-bot`
5. **Verify**: Check ledger for any in-progress rounds; the daemon will replay from the last consistent state.

### Versioning

Each deployment writes its version to `state/deployed-version.txt`. On startup, the daemon logs its version. This enables correlating behavior changes with deploys.

## Acceptance Criteria

| Criterion | V1.0 Origin | V2.0 Test |
|---|---|---|
| **SC-4** | AC-7 (fork-only `--repo`) | Every `gh` invocation in the daemon carries `--repo IronbellyOrg/IronClaude`. Verified by grepping the daemon source for `gh ` patterns and asserting `--repo` flag presence in all matches. Pre-push gate: `make lint` + `uv run ruff format --check src/ tests/` must pass. |
| **SC-5** | AC-6 (loop guard) | The `RoundGuard` monotonic counter never decrements. A fixture with 2 findings requiring 2 rounds + a bot-push-triggered re-review terminates at round 2 (not round 3). Counter is serialized to state store and survives a mid-round restart (kill -9 + restart, verify round continues at same number). |
| **SC-6** | NFR-1 (idempotent replies) | Duplicate triggers (same comment_id, same reply) are rejected at the dedup gate with `event: trigger_duplicate` logged, zero agent invocation, zero repo mutation. Concurrent daemon instances (simulated by running two processes against the same state dir) do not double-process: lock file prevents concurrent round execution. |
| **SC-7** | (N/A in V1.0 — V2.0 net-new) | Secrets are never in logs: grep the JSONL ledger for `ANTHROPIC_`, `GH_TOKEN`, or any 40-char+ hex string — zero matches. Secrets are never in argv: inspect `/proc/<pid>/cmdline` of a spawned ClaudeProcess — no secret values. The `.env` file is `chmod 600` and owned by `root:remediation-bot`. |

## Operational Risks

### R1 — Augment Re-Review Timing (False Round Advance)

**Risk**: The daemon detects a re-review and increments the round counter, but the re-review is from an *independent* Augment invocation (not triggered by the bot's push). This causes premature round exhaustion.

**Mitigation**: The daemon records `round_push_sha` (the commit SHA of the bot's push). When a re-review is detected, it verifies the PR's head SHA matches or is a descendant of `round_push_sha`. Only then does it count as the next round. If the head SHA diverged (human push, force-push), the daemon logs `event: re_review_diverged` and transitions to propose-only mode for safety.

### R2 — GitHub Webhook vs. Poll Gap

**Risk**: Between poll cycles (30s), multiple @-mentions could arrive. The daemon processes them in the next poll, but the ordering of replies vs. parent comments in the GitHub API response may not match the temporal order.

**Mitigation**: The daemon uses `comment.created_at` timestamps to order replies within a poll batch. It processes the oldest trigger first. If multiple mentions target the same PR, they are queued in the ledger as `event: trigger_queued` and processed sequentially with per-PR lock discipline.

### R3 — ClaudeProcess Zombie on Host OOM

**Risk**: The on-prem host runs out of memory, the ClaudeProcess is OOM-killed, but the daemon process survives (lower memory footprint). The daemon waits indefinitely for a process that will never exit.

**Mitigation**: The daemon tracks `claude_process_spawn` timestamp. If no `round_complete` event within `timeout_seconds` (6300s), the stuck-run detector fires (see Observability). The daemon checks if the PID still exists via `/proc/<pid>`. If gone, it treats the round as `outcome: process_terminated`, logs the event, and HALTs further rounds for that PR pending operator review.

### R4 — Secret Exposure in Error Traces

**Risk**: An unhandled exception in the daemon produces a Python traceback that includes local variables containing secret values (e.g., a `requests` exception with the full request headers).

**Mitigation**: The daemon installs a custom `sys.excepthook` that strips any line containing `Authorization:`, `ANTHROPIC_`, `GH_TOKEN`, or any value matching the pattern of known secret formats. Additionally, `PYTHONFAULTHANDLER` is disabled in production to prevent raw traceback emission. All exceptions are caught at the top level and logged with sanitized context only.

### R5 — State Store Corruption

**Risk**: The JSONL ledger or processed-triggers file is corrupted (disk write failure, power loss mid-write), causing the daemon to either re-process triggers (double-remediate) or lose round state.

**Mitigation**: Each write to the state file is atomic: write to a temp file (`state/processed-triggers.json.tmp`), then `os.rename()` to the target path. `os.rename()` is atomic on POSIX filesystems. On startup, if the main file is corrupted, the daemon falls back to the last known-good backup (`state/processed-triggers.json.bak`) and logs a warning. The JSONL ledger is append-only with `O_APPEND` flag, so a mid-write crash leaves the last line potentially truncated, which the daemon handles by ignoring the last incomplete line on replay.
