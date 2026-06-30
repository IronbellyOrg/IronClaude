---
title: "PR Auto-Remediation V2.0 — Architect Variant (one-shot invoked runner)"
lens: architect
model: opus
created: 2026-06-11
variant: 1
host_pick: one-shot-invoked-runner
---

# V2.0 Mention-Triggered Headless Remediation Bot — Architect Variant

## Architecture Decision (Execution Host)

The primary adversarial axis (C2 / OQ-A) is the on-prem host shape. I evaluate the
three candidates against six properties the seed-brief and SC-1..7 make load-bearing.

| Property | One-shot invoked runner | Persistent daemon | Webhook listener service |
|----------|------------------------|-------------------|--------------------------|
| **Latency to act** | Bounded by poll interval (≤60s) | Bounded by poll interval (≤60s) | Sub-second (push event) |
| **Idempotency (SC-6)** | Trivial — process owns one trigger, writes ledger, exits. No shared in-RAM state to corrupt | Hard — long-lived loop must dedup across its own iterations *and* crashes; in-RAM cursor lies after restart | Hard — at-least-once webhook delivery + retries means the same `issue_comment` arrives 2-3×; dedup mandatory and is the only thing standing between you and double-execution |
| **Restart-safety (SC-6)** | Native — there is nothing to restart; cron/systemd-timer re-invokes from clean state, ledger is the only memory | Fragile — a mid-remediation crash leaves a pushed commit with no reply; resume logic must reconstruct in-flight state | Fragile — same as daemon, plus an inbound request can land *during* restart and be silently dropped (no retry guarantee on a 502) |
| **Secret-exposure window (SC-7)** | Minimal — `ANTHROPIC_*`/`GH_TOKEN` live in the process env only for the seconds the runner executes, then the process dies | Maximal — secrets resident in a long-lived process's memory 24/7; one core-dump or `/proc` read leaks them | Maximal — long-lived, *and* the process is network-listening (attack surface = the open port) |
| **Operational simplicity** | Highest — a Python entrypoint + a systemd timer; no port, no inbound firewall rule, no TLS, no public DNS, no GitHub webhook secret rotation | Medium — supervised long-running unit, health checks, log rotation | Lowest — needs ingress (reverse proxy / tunnel to on-prem), HMAC signature verification, replay protection, TLS cert lifecycle |
| **Failure blast radius** | One trigger per process — a hung `claude -p` kills one runner, the timer fires the next cleanly | A wedged loop blocks *all* subsequent triggers until a human notices | A crashed listener drops *all* triggers silently (GitHub stops retrying after ~3 attempts over hours) |

**Pick: one-shot invoked runner**, driven by a `systemd` timer (preferred over cron for
journald integration, `RuntimeMaxSec=` kill-switch, and `OnFailure=` alerting) polling
the GitHub comments API every 45–60s. Each tick spawns a short-lived
`superclaude remediate scan` process that: lists new comments since the persisted cursor,
filters to authorized mention-triggers, claims each via the idempotency ledger, runs the
`ClaudeProcess`-hosted remediation, and exits.

**Justification.** The dominant V2.0 risk (seed-brief §Problem Statement) is *running an
LLM with write+push authority against untrusted comment text*. The one-shot model shrinks
two of the three blast-radius dimensions to near-zero by construction: the **secret
window** collapses to the execution span (SC-7), and **restart-safety** becomes a
non-property because the canonical state lives entirely in an on-disk ledger, never in
process memory (SC-6). It is also the only option with **no inbound network surface** —
no open port, no public ingress to the on-prem box, no webhook HMAC secret to rotate —
which is the single largest reduction in attack surface available. The webhook listener
wins on latency, but a mention-triggered remediation bot has no human waiting on a 500ms
SLA; a 60s poll ceiling is operationally invisible against a `claude -p` session that
runs for minutes. We trade ~30s of median latency for the elimination of an entire class
of network-facing and secret-residency risks. The daemon is strictly dominated: it carries
the daemon's restart/secret costs without the webhook's latency win.

**Concession to the webhook camp:** the polling cursor must be GitHub-side-durable, not a
naive local timestamp, or a clock skew / missed tick drops a trigger. We address this in
§State Store (cursor = max processed `comment.id`, monotonic, re-derivable from the API).

## Control Flow

```
systemd timer (every 45–60s)
  └─ superclaude remediate scan --repo IronbellyOrg/IronClaude
       1. CURSOR LOAD     read ledger.cursor (last processed comment id)
       2. INGEST          gh api .../pulls/comments?since=<ts>&sort=created   (review-comments)
                          gh api .../issues/comments?since=<ts>               (issue-comments, for top-level)
       3. FILTER          keep comments whose body matches @<bot> trigger grammar (C3)
       4. for each candidate, in id order:
            a. DEDUP       ledger.claim(comment_id)  → skip if already terminal/in-progress (SC-6)
            b. AUTHZ       gh api .../collaborators/{commenter}/permission  → require admin|write (C4, SC-1)
            c. PARENT      resolve opComment from in_reply_to_id (review-comment) (OQ-B, C3)
            d. PARSE       extract whitelisted flags from mention body (autonomy/depth/scope) (C3, OQ-D)
            e. ROUND-GATE  ledger.round(thread_id) < MAX_ROUNDS  else post-cap-summary + skip (SC-5)
            f. EXECUTE     ClaudeProcess( prompt=ENVELOPE(opComment, flags) ) in ephemeral checkout (OQ-C)
            g. VALIDATE    (push tier only) make lint + ruff format --check + targeted tests (SC-4)
            h. ACT         autonomy-gated: propose-only → post diff;  push → commit/push/reply/resolve
            i. COMMIT      ledger.complete(comment_id, outcome, round++)  (SC-6)
       5. CURSOR SAVE     ledger.cursor = max(processed comment.id)
       6. exit 0
```

Every step that mutates GitHub goes through one `gh_call()` wrapper that *unconditionally*
injects `--repo IronbellyOrg/IronClaude` (C5, SC-4) — there is no code path that calls
`gh` without it. The ledger write at (i) is the commit point: it happens *after* the act,
so a crash between (f) and (i) leaves the trigger claimed-but-incomplete, which the next
tick treats as "needs resume / human review" rather than re-executing blindly (idempotency
favors under-execution over double-execution).

## Component Inventory

| # | Component | Type | Source path (SoT) | New / Reuse |
|---|-----------|------|-------------------|-------------|
| A1 | `superclaude remediate` CLI group + `scan` subcommand | CLI | `src/superclaude/cli/remediate/commands.py` | **New** |
| A2 | Comment ingest + cursor | CLI module | `src/superclaude/cli/remediate/ingest.py` | **New** |
| A3 | Mention grammar parser (whitelist) | CLI module | `src/superclaude/cli/remediate/grammar.py` | **New** (OQ-D) |
| A4 | Authz gate (collaborator permission) | CLI module | `src/superclaude/cli/remediate/authz.py` | **New** (C4) |
| A5 | Parent-comment resolver | CLI module | `src/superclaude/cli/remediate/threading.py` | **New** (OQ-B) |
| A6 | Headless executor wrapper | CLI module | `src/superclaude/cli/remediate/executor.py` | **Reuse** `ClaudeProcess` (`cli/pipeline/process.py:72`) |
| A7 | Prompt envelope builder | CLI module | `src/superclaude/cli/remediate/envelope.py` | **New** (SC-2) |
| A8 | Ephemeral checkout / workspace isolation | CLI module | `src/superclaude/cli/remediate/workspace.py` | **New** (OQ-C) |
| A9 | Idempotency + round-counter ledger | CLI module | `src/superclaude/cli/remediate/ledger.py` | **New** (OQ-E, SC-5/6) |
| A10 | Reply-to-thread + resolve helper | CLI module | `src/superclaude/cli/remediate/reply.py` | **New** (C5) |
| A11 | `gh` wrapper (fork-only `--repo` injector) | CLI module | `src/superclaude/cli/remediate/gh.py` | **New** (C5) |
| A12 | Autonomy gate (level → allowed actions) | CLI module | `src/superclaude/cli/remediate/autonomy.py` | **New** (C1) |
| A13 | Severity rubric routing | ref/import | reuse `sc-auggie-review-protocol/refs/severity-rubric.md` | **Reuse** (C5) |
| A14 | systemd timer + service units | deploy | `deploy/remediate-bot/remediate@.service` `.timer` | **New** |
| A15 | Tests | pytest | `tests/cli/remediate/` | **New** |

A CLI group (not a skill) is the right home: the host runs *outside* a Claude session
(headless), so the orchestration is Python that *spawns* `claude -p`, mirroring how
`sprint`/`swarm`/`pipeline` already wrap `ClaudeProcess`. Skills are session-resident; this
is not.

## Mention Detection & Parent Resolution (OQ-B)

**Detection = API polling, not webhooks** — forced by the one-shot host pick (no listener).
Two endpoints, because GitHub splits comment surfaces:

- **PR review-comment threads** (the primary case — a reply *to a review comment*):
  `gh api repos/IronbellyOrg/IronClaude/pulls/comments?sort=created&direction=asc&since=<ts>`
  (the repo-wide review-comments listing). Each object carries `id`, `in_reply_to_id`,
  `pull_request_review_id`, `user.login`, `body`, and the diff anchor (`path`, `line`).
- **Top-level / conversation comments**: `gh api .../issues/comments?since=<ts>` (issue
  comments are flat — no `in_reply_to_id`). Used only if the mention grammar permits a
  conversation-level trigger; default scope is review-comment replies (C6 keeps us out of
  arbitrary human-comment territory).

**Parent resolution (the sole `opComment` source, C3):**
- *Review-comment reply* → the mention comment has `in_reply_to_id = P`. Fetch the parent:
  `gh api .../pulls/comments/P --jq '.body'`. That body is `opComment`. This is reliable
  because review-comment threading is a real linked structure, not heuristic.
- *Edge case — mention is itself the thread root* (someone @-mentions in a brand-new review
  comment, no `in_reply_to_id`): there is no parent. Policy: **reject with a "reply to the
  comment you want remediated" message** rather than guessing — the brief is explicit that
  the parent body is the *sole* op input, so a missing parent is a hard no-op, not a
  fallback to the mention's own text (which would breach C3's injection boundary).
- *Issue-comment flatness*: if conversation-level triggers are enabled, there is no parent
  pointer; the only safe `opComment` is an explicit quoted block the grammar requires the
  user to delimit. Default-off to keep the surface tight.

## Headless Execution (reuse `ClaudeProcess`)

A6 instantiates the verified primitive at `cli/pipeline/process.py:72`. `build_command()`
already emits exactly the headless shape we need —
`claude --print --verbose --dangerously-skip-permissions --no-session-persistence
--tools default --max-turns N --output-format stream-json` — and **delivers the prompt via
stdin** (`start()`, lines 162-174), bypassing the 128KB `MAX_ARG_STRLEN` argv ceiling. We
pass the troubleshoot invocation as the `prompt=` envelope (§Injection Containment), set
`output_format="stream-json"` for structured progress capture, cap `max_turns` low
(propose ≈ 30, fix ≈ 60), and run with `cwd` pinned to the ephemeral checkout (A8) via the
`env_vars` merge hook (`build_env`, lines 145-160, which strips `CLAUDECODE` /
`CLAUDE_CODE_ENTRYPOINT` and inherits `ANTHROPIC_*` from the daemon env). The
`PromptTooLargeForArgv` guard (lines 169-173) gives us a free, typed pre-spawn size check.
The executed command is literally:
`/sc:troubleshoot "${opComment}" --depth <deep|standard> --fix` — with `--fix` *omitted*
at propose-only level (the executor controls the flag, never the mention text).

## Authorization (C4, SC-1)

Before any agent spawn — gate (4b) — call
`gh api repos/IronbellyOrg/IronClaude/collaborators/{commenter}/permission
--jq '.permission'` and require the result ∈ `{admin, write}` (GitHub returns
`admin|write|read|none`). The check is **live per-trigger** (no static allowlist → no
drift). On reject: emit a single audit-log line, post no reply (avoid being a permission
oracle for attackers), commit the comment id to the ledger as `rejected_unauthorized`, and
make **zero** agent invocations / zero mutations (SC-1). The `maintain` and `triage`
permission classes (org repos) map to *read-equivalent for our purposes* → reject; only
explicit write/admin proceeds.

## Injection Containment (brief — security variant leads)

The architectural contribution to SC-2 is the **envelope boundary** (A7): `opComment` is
*never* concatenated into a shell command. It is passed as the stdin prompt body to
`ClaudeProcess`, wrapped in an explicit delimiter envelope that frames it as *data to
diagnose*, not *instructions to obey* — e.g. a fenced `<op_comment>…</op_comment>` block
with a preamble stating the content is untrusted PR text. Mention flags (C3) are parsed by
A3's whitelist *before* this and never reach the agent as prose. The execution runs inside
an ephemeral checkout (A8) isolated from the host's working tree. Whether
`--dangerously-skip-permissions` is acceptable inside that isolation vs. a restricted tool
profile (OQ-C) is the security variant's call; architecturally I provide the isolation
seam (A8 ephemeral workspace + `cwd` pinning) so either policy can be enforced at one point.

## Autonomy Model (C1, SC-3)

A12 maps a parsed level → an allowed-action set. **Default (no flag) = propose-only.**

| Level | Mention token | Checkout | Edits | Validate | Push | Reply/Resolve |
|-------|---------------|----------|-------|----------|------|---------------|
| propose-only (**default**) | *(none)* / `propose` | ephemeral | yes (in checkout) | no | **never** | post diff as new comment |
| fix | `fix` | ephemeral | yes | yes (SC-4) | yes (PR branch) | reply-to-thread + resolve |

Propose-only runs the troubleshoot session in the ephemeral checkout, captures the produced
diff, and posts it as a comment — **zero pushes** (SC-3). A garbled/unknown flag degrades
to propose-only, never escalates (OQ-D fail-safe). `needs_human_decision`-class outcomes
HALT even at `fix` (carried from V1.0 FR-4.4) — the bot posts the proposal and stops.

## Loop-Safety & Idempotency (SC-5, SC-6)

**Round counter** mirrors the swarm bounded-counter at `cli/swarm/commands.py:2269`
(`iterations += 1; if … >= max: break`). Here the counter is keyed on **thread_id**
(stable across the bot's own re-trigger), persisted in the ledger, incremented at step (i).
A bot push that provokes a re-review and a fresh authorized mention is the *next round* of
the *same* thread, not a new trigger — so `round(thread_id) >= MAX_ROUNDS` (default 2, max
5) short-circuits to a cap-summary comment instead of re-executing (SC-5). The counter is
monotonic and survives restarts because it lives on disk, not in the runner's RAM.

**Idempotency** (SC-6): each comment id is `claim()`-ed before execution and `complete()`-d
after. A concurrent second timer tick (overlap if a scan runs long) finds the id already
claimed and skips it — the ledger claim is the mutual-exclusion primitive. Because the
claim→complete window can be interrupted by a crash, claims carry a state
(`claimed | complete | rejected | failed`) and a timestamp; a stale `claimed` older than a
TTL surfaces for human review (resume), never silent re-execution.

## State Store (OQ-E)

**On-disk JSON-lines ledger** under `.dev/remediate-state/` (gitignored), NOT GitHub
reactions/labels-as-state. Rationale: (1) the one-shot host needs durable cross-restart
memory that is *cheaper and faster* than round-tripping GitHub on every tick; (2)
reactions/labels are rate-limited, racy, and visible/forgeable by anyone with write access
— making external GitHub state the source of truth would let a collaborator forge "already
processed" markers. Schema per record: `{comment_id, thread_id, commenter, decision,
round, state, ts, outcome}`. The **cursor** = `max(comment_id)` ever processed, stored as a
single small file; on each scan we query `?since=<cursor_ts>` then filter `id > cursor` to
defend against the API's timestamp granularity (two comments in the same second). The
ledger is the *single* source of truth for both dedup and round-count, so they can never
disagree. GitHub remains the *observation* surface, never the *state* surface.

## Reuse Map

- `ClaudeProcess` (`cli/pipeline/process.py:72`) — the headless spawn primitive, used as-is
  (stdin prompt, env-inherited auth, `max_turns`, `stream-json`). **No fork, no edit.**
- Swarm loop-guard idiom (`cli/swarm/commands.py:2269`) — pattern for the round counter.
- Severity rubric (`sc-auggie-review-protocol/refs/severity-rubric.md`) — depth selection
  (Critical/High → `--depth deep`; Medium → standard), reused not re-authored (C5).
- `gh`-pattern precedent (`sc-auggie-review-protocol/SKILL.md` inline+summary posting) —
  template for A10's reply path; the reply+resolve endpoints themselves are net-new.
- `~/.aienv` / `ccsession.env` chmod-600 precedent — model for the daemon's secret-file
  sourcing into the systemd unit's `EnvironmentFile=` (SC-7).

## Acceptance Criteria

- **AC-1 (SC-1):** unauthorized commenter mention → authz gate rejects, ledger records
  `rejected_unauthorized`, zero `ClaudeProcess` spawns, zero `gh` mutations. (fixture: read
  permission user.)
- **AC-2 (SC-3):** default mention (no flag) → propose-only; diff posted as comment, `git
  log` on PR branch unchanged (zero pushes).
- **AC-3 (SC-2):** `opComment` containing `$(…)` / `; rm -rf` / "ignore previous
  instructions" → executes as inert diagnosed text inside the envelope; no shell exec, no
  control-flow change (fixture asserts the literal payload appears only inside the envelope).
- **AC-4 (SC-4):** `fix`-level run runs `make lint` + `ruff format --check` + targeted tests
  before push; a failing gate blocks the push and posts a failure note. Every `gh` call in
  the trace carries `--repo IronbellyOrg/IronClaude`.
- **AC-5 (SC-5):** a 3-mention fixture on one thread with `MAX_ROUNDS=2` → exactly 2
  executions then a cap-summary; round counter monotonic across a simulated restart.
- **AC-6 (SC-6):** two overlapping scan invocations on the same new comment → exactly one
  execution (claim mutual exclusion); a killed-mid-execution claim resurfaces as `claimed`
  (resume), never re-executes silently.
- **AC-7 (SC-7):** journald/log scrape of a full run contains no `ANTHROPIC_*`/`GH_TOKEN`
  value; the agent's tool surface has no access to the secret env names.
- **AC-8 (OQ-B):** a review-comment reply resolves `opComment` from `in_reply_to_id`; a
  parentless root mention is rejected, not guessed.

## Build Sequencing

1. **A11 gh-wrapper + A9 ledger** first — the two invariants (fork-only `--repo`,
   dedup/round state) every other component depends on. Test in isolation.
2. **A2 ingest + cursor** + **A5 parent resolver** (OQ-B) — get reliable trigger detection
   and `opComment` extraction before any execution exists. Probe against a real fixture PR
   to lock the comment-API shapes (mirrors V1.0's "probe first" R1 discipline).
3. **A4 authz** (C4) + **A3 grammar** (OQ-D) — the two gates; both must reject-by-default.
4. **A8 workspace + A7 envelope + A6 executor** — wire `ClaudeProcess` at propose-only
   (no push) first. AC-2/AC-3 here.
5. **A12 autonomy + A10 reply/resolve** — net-new reply endpoints + the `fix` tier +
   validation gate (SC-4). AC-4 here.
6. **A14 systemd units** + **A15 full suite**; round-guard fixture (AC-5), idempotency
   fixture (AC-6). `make sync-dev` (for any ref edits) + `make verify-sync`.

## Open Risks

- **R-A (host pick):** polling latency (≤60s) is acceptable *only if* GitHub's
  comment-listing `since` window never silently drops a comment under heavy PR activity. The
  `id > cursor` post-filter mitigates timestamp granularity, but a deleted-then-recreated
  comment id gap is unhandled — accept as a known edge (re-mention recovers it).
- **R-B (reply/resolve is net-new):** the resolve path needs the GraphQL
  `resolveReviewThread` mutation (REST has no resolve), which requires the *thread node id*,
  obtained via a GraphQL query on the PR's `reviewThreads` — a two-call dance the brief
  flags as greenfield. Mis-mapping comment-id → thread-node-id resolves the wrong thread.
  This is the highest-uncertainty net-new surface; it gets a dedicated integration fixture.
- **R-C (ledger as SoT):** if the `.dev/remediate-state/` ledger is lost (disk wipe,
  accidental clean), dedup and round-count reset — a backlog of old authorized mentions
  could re-fire. Mitigation: the cursor floor + a "max age" filter (ignore mentions older
  than N hours) so a wiped ledger cannot reprocess ancient history.
- **R-D (concurrency model):** the one-shot host assumes scans don't pile up; a `claude -p`
  run that exceeds the 45–60s timer interval means two scans overlap. The ledger claim
  handles correctness, but `RuntimeMaxSec=`/a lockfile should cap concurrent runners so a
  slow remediation can't be lapped indefinitely.
