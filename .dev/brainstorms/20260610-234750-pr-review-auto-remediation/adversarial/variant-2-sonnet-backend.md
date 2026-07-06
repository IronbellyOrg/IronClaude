# Backend Variant Specification: PR Review Auto-Remediation Monitor (V1.0)

## Overview / Goals

The PR Review Auto-Remediation Monitor V1.0 adds a new `/sc:submit-pr` command and `sc-submit-pr-protocol` skill that can open a pull request on the user's fork, wait for the Augment Code GitHub App review, route Medium+ findings to `/sc:troubleshoot`, and optionally implement, validate, push, reply, and resolve review threads under a bounded remediation loop.

This specification takes the backend reliability position that the monitor is a fault-tolerant state machine, not a conversational convenience. Every externally visible action must be recoverable, idempotent, rate-limit safe, and auditable. The system may run inside the Claude Code session in V1.0, but it must persist enough state to resume safely after session loss.

### Goals

- `G-1` Provide a single explicit command for fork-safe PR creation: `/sc:submit-pr`.
- `G-2` Optionally arm an in-session monitor with `--monitor {0,1,2,3}` after PR creation.
- `G-3` Detect Augment review arrival using a conservative three-state classifier.
- `G-4` Route Medium+ findings to `/sc:troubleshoot` with deterministic depth selection.
- `G-5` Enforce validation gates before any push or thread resolution.
- `G-6` Guarantee idempotent replies/resolutions across re-armed and resumed runs.
- `G-7` Bound autonomous remediation with a monotonic round counter keyed to reviews observed since monitor arm.
- `G-8` Produce a `.jsonl` run-log that is both an audit trail and a recovery checkpoint.

### Non-goals

- `NG-1` No detached daemon, GitHub Action, or server-side runner in V1.0.
- `NG-2` No action on human reviewer comments or unknown bot comments.
- `NG-3` No PR approval, request-changes, merge, branch deletion, or release publishing.
- `NG-4` No persisted user preference that silently enables level-3 autonomy by default.
- `NG-5` No bypass of existing source-of-truth discipline: implementation edits must start under `/config/workspace/IronClaude/src/superclaude/`, followed by `make sync-dev` and `make verify-sync`.

## Process & State Model

### Components

- `C1` Command: `/config/workspace/IronClaude/src/superclaude/commands/submit-pr.md`.
- `C2` Skill: `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/SKILL.md`.
- `C3` Polling reference or script: `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/refs/augment-poll.md` and optionally `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/scripts/poll-augment-review.sh`.
- `C4` Severity routing reference: `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/refs/severity-routing.md`, reusing the rubric semantics from `/config/workspace/IronClaude/src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md`.
- `C5` Thread reply / resolve reference or script: `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/refs/thread-reply.md` and optionally `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/scripts/reply-resolve-thread.sh`.
- `C6` Hook update: `/config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh`.
- `C7` Tests under `/config/workspace/IronClaude/tests/`, including parser, state-machine, command-contract, and hook tests.

### Command contract

```bash
/sc:submit-pr [--monitor {0,1,2,3}] [--max-rounds N] [--poll-interval SECONDS] [--timeout SECONDS] [--base master] [--head <branch>] [--title <title>] [--body <body>] [--output-dir <absolute-path>] [--resume <absolute-run-log-path>]
```

Defaults:

- `--monitor 0`: create PR only; no monitor.
- `--max-rounds 2`: maximum autonomous remediation rounds; hard cap `5`.
- `--poll-interval 30`: minimum accepted value `30` seconds.
- `--timeout 1800`: total wait for each review-arrival phase, approximately 30 minutes.
- `--base master`.
- `--output-dir /config/workspace/IronClaude/.dev/pr-monitor/pr-<number>-<YYYYMMDDHHMMSS>/` unless `--resume` supplies an existing log.

### PR creation process

`/sc:submit-pr` must enforce the fork target exactly. The mandatory PR creation shape is:

```bash
gh pr create --repo IronbellyOrg/IronClaude --base master --head <branch> --title "<title>" --body "<body>"
```

Before creating the PR, the skill must run and record these checks:

- `git remote -v` must show `origin` pointing to `IronbellyOrg/IronClaude.git`; otherwise stop.
- `git fetch origin` must succeed; otherwise stop.
- If `master..origin/master` is non-empty, the current branch must be rebased onto `origin/master` before PR creation; if the rebase cannot be performed safely, stop and report.
- `gh auth status` must succeed; otherwise stop.
- After `gh pr create`, parse the returned URL and verify it starts with `https://github.com/IronbellyOrg/IronClaude/pull/`; otherwise stop immediately and instruct the operator to close the misrouted PR.

### State model

The monitor maintains one durable `monitor_state` reconstructed from the run-log on startup and appended to after every transition.

Canonical states:

- `S0_INIT`: arguments parsed; no PR action yet.
- `S1_PR_CREATED`: PR URL and number verified.
- `S2_MONITOR_ARMED`: run-log initialized; baseline review/comment IDs captured.
- `S3_WAITING_FOR_REVIEW`: polling for a new Augment review after arm or after a monitor push.
- `S4_REVIEW_CLASSIFIED`: a relevant Augment emission has been classified.
- `S5_DIAGNOSING`: Medium+ findings are being routed to `/sc:troubleshoot`.
- `S6_FIXING`: permitted fixes are being applied.
- `S7_VALIDATING`: validation gates are running.
- `S8_PUSHING`: validated remediation is being committed and pushed, level 3 only.
- `S9_REPLYING_RESOLVING`: idempotent thread replies and resolutions are being posted.
- `S10_TERMINAL_CLEAN`: zero Medium+ findings observed.
- `S11_TERMINAL_MAX_ROUNDS`: max rounds reached with residual Medium+ findings.
- `S12_TERMINAL_TIMEOUT`: review never arrived within timeout.
- `S13_TERMINAL_HALTED`: human decision or validation failure requires operator action.
- `S14_TERMINAL_FAILED`: unrecoverable environment, GitHub, parser, or state corruption failure.

All state transitions must append a `state_transition` event before starting work in the new state.

## Poll-loop & Backoff Design

### Polling host

V1.0 uses the Claude Code Monitor tool as the live host. The polling command must emit one line per meaningful event and exit on terminal state. It must not stream raw logs. Terminal statuses must include success, timeout, max-rounds, halt, and failure so the session is never left silent on crash-like outcomes.

### GitHub API sources

The poller must query all empirically relevant PR review surfaces because GitHub Apps can emit formal reviews, review comments, issue comments, or checks depending on configuration. The classifier only acts on Augment-owned emissions.

Required queries:

```bash
gh pr view <PR_NUMBER> --repo IronbellyOrg/IronClaude --json number,url,headRefName,headRefOid,baseRefName,reviews,comments
```

```bash
gh api repos/IronbellyOrg/IronClaude/pulls/<PR_NUMBER>/reviews
```

```bash
gh api repos/IronbellyOrg/IronClaude/pulls/<PR_NUMBER>/comments
```

Optional empirical probe, if Augment is found to use checks:

```bash
gh api repos/IronbellyOrg/IronClaude/commits/<HEAD_SHA>/check-runs
```

Every `gh` command must pin `--repo IronbellyOrg/IronClaude` where the `gh` subcommand supports it, or use the explicit `repos/IronbellyOrg/IronClaude/...` REST path where using `gh api`.

### Poll interval

- `poll_interval_seconds` must be at least `30`.
- A user-supplied value below `30` must be rejected, not rounded silently.
- Normal polling uses fixed 30-second cadence plus backoff delays when rate-limited.
- The timeout clock is wall-clock elapsed time since entering `S3_WAITING_FOR_REVIEW` for the current review wait, not cumulative process lifetime.

### Backoff behavior

The poller must classify GitHub failures:

- HTTP `403` with `x-ratelimit-remaining: 0`: primary rate limit.
- HTTP `403` with body mentioning secondary rate limit, abuse detection, or retry later: secondary rate limit.
- HTTP `429`: rate-limited.
- 5xx or transient network failure: transient GitHub failure.
- 401/404/422: configuration or permission failure unless clearly transient.

Backoff rules:

- Start `backoff_seconds = 30`.
- On 403/429/secondary-limit/transient 5xx, sleep `backoff_seconds`, append `api_backoff`, then double to a maximum of `300` seconds.
- If `Retry-After` is present, use `max(backoff_seconds, retry_after)` but cap any single sleep at `300` seconds.
- On a successful poll, reset `backoff_seconds` to `30`.
- Backoff time counts toward the 30-minute review-wait timeout.
- If the next sleep would exceed the review-wait deadline, emit `review_timeout` and exit `S12_TERMINAL_TIMEOUT` instead of sleeping past the deadline.

### Graceful timeout

If no Augment review is detected within `--timeout`, the poller exits with a clean, non-destructive result:

- Append `terminal_timeout` with `reason: "review_never_arrived"`.
- Do not invoke `/sc:troubleshoot`.
- Do not modify files.
- Do not push.
- Print a concise operator message containing the PR URL, elapsed time, and run-log path.

## Loop-guard State Machine

### Round-counter definition

The remediation round counter is the core safety invariant.

`round_index` is the count of Augment review emissions observed since the monitor armed that contain one or more Medium+ findings and have not already been accounted for in a prior terminal decision.

It is not:

- The number of polls.
- The number of comments.
- The number of pushes.
- The number of findings.
- The number of reviews since the last poll.
- A counter reset after a successful push.

### Baseline and observed-review set

At `S2_MONITOR_ARMED`, the monitor records:

```json
{
  "baseline": {
    "armed_at": "2026-06-11T00:00:00Z",
    "head_sha_at_arm": "<sha>",
    "review_ids_seen_at_arm": [123],
    "review_comment_ids_seen_at_arm": [456, 457],
    "issue_comment_ids_seen_at_arm": [789]
  }
}
```

The monitor acts only on Augment emissions whose IDs are not in the baseline and not in `processed_review_ids`.

### Off-by-one analysis

Default `--max-rounds 2` means:

- Round 1: the first post-arm Augment review with Medium+ findings can be remediated.
- Round 2: the first re-review after the monitor's own push with Medium+ findings can be remediated.
- If a third post-arm Augment review still contains Medium+ findings, the monitor must not remediate it. It must enter `S11_TERMINAL_MAX_ROUNDS` and hand off.

`--max-rounds 1` means exactly one remediation attempt after the first post-arm review with Medium+ findings. It does not mean one poll, one comment, or one push.

### Termination predicate

After every classified Augment review emission, evaluate in this exact order:

1. If `medium_plus_findings_count == 0`, transition to `S10_TERMINAL_CLEAN` and stop.
2. Else if `round_index >= max_rounds` and the current review has not already entered a remediation cycle, transition to `S11_TERMINAL_MAX_ROUNDS` and stop.
3. Else if any finding is `needs_human_decision`, transition to `S13_TERMINAL_HALTED` and stop.
4. Else route findings according to monitor level and severity.

For an actionable review with Medium+ findings, increment `round_index` exactly once before starting diagnosis. The event must include `review_id`, `review_head_sha`, `medium_plus_findings_count`, `round_index_before`, and `round_index_after`.

### Maximums

- Default `max_rounds = 2`.
- Hard cap `max_rounds = 5`.
- Values above `5` must be rejected with a clear error.
- Values below `1` are invalid when `--monitor 2` or `--monitor 3`; `--monitor 1` may accept `0` only if it is explicitly interpreted as diagnose/report with no remediation loop.

## Detection-Contract Classifier

### Classifier states

The classifier returns exactly one of three states per poll cycle:

- `D0_NO_REVIEW_YET`: no post-arm Augment-owned emission has been detected. Continue polling.
- `D1_REVIEW_ZERO_MEDIUM_PLUS`: post-arm Augment-owned emission detected; normalized findings contain zero Medium+ items. Terminate cleanly.
- `D2_REVIEW_WITH_FINDINGS`: post-arm Augment-owned emission detected; at least one normalized finding is Medium, High, or Critical. Route according to monitor level.

The classifier must not return a partially actionable state. Unknown bot identity means `D0_NO_REVIEW_YET`, not "probably Augment".

### Augment identity contract

The Augment App bot login must be empirically captured before implementation is considered complete. The implementation must store accepted bot logins in a single config constant, for example:

```json
{
  "augment_bot_logins": ["augment-code[bot]"],
  "augment_author_association": ["NONE", "CONTRIBUTOR"],
  "augment_app_slug": "augment-code"
}
```

The literal values above are placeholders until probed. The parser must not hard-code guesses scattered through shell snippets or markdown instructions.

If the author login does not match the allowlist, the emission is ignored even if its body resembles an Augment review.

### Finding extraction

A normalized finding must include:

```json
{
  "finding_id": "aug-<comment_id>-<stable_hash>",
  "source": "augment",
  "source_review_id": 123,
  "source_comment_id": 456,
  "thread_id": "<github-thread-or-comment-id>",
  "author_login": "augment-code[bot]",
  "head_sha": "<sha>",
  "path": "src/superclaude/example.py",
  "line": 42,
  "original_severity_hint": "High",
  "normalized_severity": "High",
  "needs_human_decision": false,
  "body": "<raw finding body>",
  "evidence": {
    "url": "https://github.com/IronbellyOrg/IronClaude/pull/<N>#discussion_r...",
    "diff_hunk": "@@ ..."
  }
}
```

Severity normalization rules:

- Re-grade using the reused severity rubric semantics; Augment's label is only a hint.
- `Critical`, `High`, `Medium`, `Low`, and `Nit` are the only accepted normalized severities.
- Unknown, missing, malformed, or contradictory severity must normalize to `Medium`.
- Findings without a stable path/line may still be reported, but may not be auto-fixed at level 3 unless `/sc:troubleshoot` can ground them in a real file and the run-log records that grounding.

### Fail-safe defaults

- Unknown severity → `Medium`.
- Unknown bot login → not detected; keep polling until timeout.
- Unknown emission shape → record `classifier_unknown_shape` and keep polling unless timeout is reached.
- Duplicate finding body/comment ID → deduplicate by stable key, never remediate twice.
- Ambiguous API contract, security posture, user-facing behavior, or data migration decision → mark `needs_human_decision = true`.

## Idempotency & Run-log Schema

### Run-log location

Default run-log path:

```text
/config/workspace/IronClaude/.dev/pr-monitor/pr-<PR_NUMBER>-<YYYYMMDDHHMMSS>/monitor-run-<PR_NUMBER>.jsonl
```

The output directory must also include:

- `state.snapshot.json`: latest materialized state after each event append.
- `findings.latest.json`: latest normalized finding set.
- `validation/round-<N>/`: stdout/stderr and exit codes for validation commands.
- `troubleshoot/round-<N>/`: prompts, outputs, and summaries from `/sc:troubleshoot` handoffs when materialized as files.

### JSONL event envelope

Every line must be valid JSON with this envelope:

```json
{
  "schema_version": "1.0",
  "event_id": "01J...",
  "event_type": "poll_result",
  "timestamp": "2026-06-11T00:00:00Z",
  "run_id": "pr-123-20260611000000",
  "pr": {
    "repo": "IronbellyOrg/IronClaude",
    "number": 123,
    "url": "https://github.com/IronbellyOrg/IronClaude/pull/123",
    "base": "master",
    "head": "feature/example"
  },
  "state_before": "S3_WAITING_FOR_REVIEW",
  "state_after": "S4_REVIEW_CLASSIFIED",
  "round_index": 1,
  "payload": {}
}
```

`event_id` must be unique and monotonic within a run. A timestamp plus sequence number is acceptable if UUID generation is unavailable.

### Required event types

- `run_started`
- `environment_check`
- `pr_create_attempted`
- `pr_created`
- `monitor_armed`
- `baseline_captured`
- `poll_attempt`
- `poll_result`
- `api_backoff`
- `classifier_unknown_shape`
- `review_detected`
- `findings_normalized`
- `round_incremented`
- `route_decision`
- `troubleshoot_started`
- `troubleshoot_completed`
- `fix_applied`
- `validation_started`
- `validation_completed`
- `commit_created`
- `push_completed`
- `reply_posted`
- `thread_resolved`
- `idempotency_skip`
- `terminal_clean`
- `terminal_timeout`
- `terminal_max_rounds`
- `terminal_halted`
- `terminal_failed`

### Materialized state schema

`state.snapshot.json` must be fully reconstructable from the JSONL log and must use this shape:

```json
{
  "schema_version": "1.0",
  "run_id": "pr-123-20260611000000",
  "status": "running",
  "current_state": "S3_WAITING_FOR_REVIEW",
  "repo": "IronbellyOrg/IronClaude",
  "pr_number": 123,
  "pr_url": "https://github.com/IronbellyOrg/IronClaude/pull/123",
  "base_branch": "master",
  "head_branch": "feature/example",
  "head_sha_at_arm": "<sha>",
  "last_observed_head_sha": "<sha>",
  "monitor_level": 3,
  "max_rounds": 2,
  "round_index": 1,
  "poll_interval_seconds": 30,
  "timeout_seconds": 1800,
  "baseline": {
    "review_ids_seen_at_arm": [],
    "review_comment_ids_seen_at_arm": [],
    "issue_comment_ids_seen_at_arm": []
  },
  "processed_review_ids": [123],
  "processed_finding_ids": ["aug-456-abcd"],
  "replied_comment_ids": [456],
  "resolved_thread_ids": ["456"],
  "pushed_commit_shas": ["<sha>"],
  "validation_history": [
    {
      "round_index": 1,
      "commands": [
        {"command": "uv run pytest /config/workspace/IronClaude/tests/test_example.py -v", "exit_code": 0},
        {"command": "make lint", "exit_code": 0},
        {"command": "uv run ruff format --check src/ tests/", "exit_code": 0}
      ]
    }
  ],
  "terminal_reason": null
}
```

### Idempotency keys

The system must maintain these sets in materialized state and append `idempotency_skip` when an action is skipped because its key already exists:

- `processed_review_ids`: prevents re-processing the same Augment review emission.
- `processed_finding_ids`: prevents applying a fix twice for the same finding.
- `replied_comment_ids`: prevents duplicate thread replies.
- `resolved_thread_ids`: prevents duplicate resolution calls.
- `pushed_commit_shas`: prevents treating the same pushed commit as a new remediation round.

A resumed monitor must load `state.snapshot.json` if present, then replay the JSONL after the snapshot's event marker if needed. If the snapshot and JSONL disagree, JSONL is authoritative and the system must rebuild the snapshot before continuing.

### Reply contract

For each fixed finding, the reply body must include:

- The finding ID.
- The normalized severity.
- A concise fix summary.
- The validation commands that passed.
- The commit SHA that contains the fix, level 3 only.
- A statement that the thread is being resolved only after local validation passed.

The reply must be posted only once per `source_comment_id`. If a thread was already replied to but not resolved before a crash, resume should resolve it without posting a duplicate reply.

## Validation Gates

### Gate order

Before any level-3 push or thread resolution, validation must run in this exact order:

1. Targeted tests selected from changed files and finding scope.
2. Escalation to `make test` when changes are cross-cutting, affect shared protocol behavior, hooks, CLI argument parsing, command activation, or run-log state-machine code.
3. `make lint`.
4. `uv run ruff format --check src/ tests/`.
5. Optional project-specific smoke checks if the troubleshoot output explicitly requires them.

All Python commands must use UV where applicable. The format check is mandatory because `make lint` does not cover `ruff format --check` in this repository.

### Targeted test selection

Targeted tests are acceptable only when all modified paths are localized and a direct test mapping exists. Examples:

- Parser-only change → parser unit tests plus lint/format.
- Hook script change → hook fixture tests plus lint/format.
- Skill markdown command contract change → command/skill sync tests plus lint/format.

Escalate to `make test` when:

- The remediation touches shared CLI routing, install/sync behavior, hook registration, task execution, or test fixtures used by multiple commands.
- More than three unrelated source areas change.
- A previous targeted test failed and the fix affects common infrastructure.
- The finding is High or Critical and the changed code has broad blast radius.

### No-push-on-failure

If any required validation command exits non-zero:

- Append `validation_completed` with `status: "failed"`.
- Do not commit if no commit exists yet.
- Do not push.
- Do not reply as fixed.
- Do not resolve any thread.
- At monitor level 2, halt for user inspection.
- At monitor level 3, one additional fix attempt may occur only if `round_index < max_rounds`; otherwise halt with residual findings and validation failure details.

### Commit and push gate

Level 3 may commit and push only if:

- The working tree diff corresponds to the current round's findings.
- Required validation passed after the final diff was produced.
- No `needs_human_decision` finding is active.
- The branch is still the PR head branch.
- The push target is `origin`, never `upstream`.

Commit messages must follow project convention and include the required co-author trailer when Claude creates the commit:

```text
fix(pr-review): remediate Augment findings for PR #<N>

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

## Functional Requirements

### FR-1: `/sc:submit-pr` command and skill activation

- `FR-1.1` Add `/config/workspace/IronClaude/src/superclaude/commands/submit-pr.md` with command metadata, usage, flags, examples, boundaries, and mandatory activation of `sc-submit-pr-protocol`.
- `FR-1.2` Add `/config/workspace/IronClaude/src/superclaude/skills/sc-submit-pr-protocol/SKILL.md` as the authoritative protocol.
- `FR-1.3` The command file must not implement the workflow inline; it must instruct skill invocation before protocol execution.
- `FR-1.4` `--monitor` must accept only `0`, `1`, `2`, or `3`.
- `FR-1.5` `--monitor 0` must preserve today's PR-only workflow, except for mandatory fork-safe targeting.

### FR-2: Fork-safe PR creation

- `FR-2.1` Every PR creation call must use `--repo IronbellyOrg/IronClaude`.
- `FR-2.2` The skill must verify `origin` points to the fork before pushing or creating a PR.
- `FR-2.3` The skill must fetch `origin` and detect when local `master` is behind `origin/master`.
- `FR-2.4` The skill must not create a PR against `SuperClaude-Org/SuperClaude_Framework` unless the same session contains explicit user authorization for upstream contribution.
- `FR-2.5` The returned PR URL must be verified before monitor arming.

### FR-3: Monitor arming and review polling

- `FR-3.1` On `--monitor >= 1`, initialize the output directory, run-log, and state snapshot immediately after PR URL verification.
- `FR-3.2` Capture baseline review/comment IDs at arm time.
- `FR-3.3` Poll interval must be at least 30 seconds.
- `FR-3.4` Review wait timeout defaults to 1800 seconds.
- `FR-3.5` The monitor must exit gracefully if the review never arrives.
- `FR-3.6` GitHub API 403/429/secondary-limit responses must use exponential backoff capped at 300 seconds.

### FR-4: Three-state detection classifier

- `FR-4.1` The classifier must return only `D0_NO_REVIEW_YET`, `D1_REVIEW_ZERO_MEDIUM_PLUS`, or `D2_REVIEW_WITH_FINDINGS`.
- `FR-4.2` Unknown bot login must be treated as no review detected.
- `FR-4.3` Unknown severity must normalize to Medium.
- `FR-4.4` Unknown emission shape must be logged and ignored until timeout.
- `FR-4.5` The Augment bot identity must be centralized and empirically validated before release.

### FR-5: Severity routing

- `FR-5.1` Medium findings route to `/sc:troubleshoot --fix`.
- `FR-5.2` High and Critical findings route to `/sc:troubleshoot --depth deep --fix`.
- `FR-5.3` Low and Nit findings are reported only and never auto-remediated.
- `FR-5.4` Multiple findings may be batched only when they are in the same file or subsystem and batching does not obscure per-thread reply tracking.
- `FR-5.5` Route decisions must be appended to the run-log before invoking troubleshoot.

### FR-6: Autonomy levels

- `FR-6.1` Level 0: create PR only; no monitor.
- `FR-6.2` Level 1: monitor, classify, diagnose, and propose; no edits.
- `FR-6.3` Level 2: monitor, diagnose, apply local fixes, and validate; halt before commit, push, reply, or resolve.
- `FR-6.4` Level 3: monitor, diagnose, fix, validate, commit, push, reply, resolve, and wait for re-review until terminal predicate.
- `FR-6.5` Any `needs_human_decision` finding halts at all levels before mutation or push.

### FR-7: Loop guard

- `FR-7.1` `round_index` must count actionable Augment review emissions observed since arm.
- `FR-7.2` `round_index` must be monotonic and durable in the run-log.
- `FR-7.3` Default `--max-rounds` is `2`.
- `FR-7.4` Hard cap is `5`.
- `FR-7.5` The monitor stops when zero Medium+ findings are observed or when `round_index >= max_rounds` before starting another remediation.
- `FR-7.6` A re-review caused by the monitor's own push counts as the next round, not a new independent trigger.

### FR-8: Idempotent reply and resolve

- `FR-8.1` The monitor must track `replied_comment_ids` durably.
- `FR-8.2` A resumed monitor must never post a duplicate reply to the same review comment.
- `FR-8.3` The monitor must track `resolved_thread_ids` durably.
- `FR-8.4` Resolution must occur only after the corresponding fix was validated and, for level 3, pushed.
- `FR-8.5` If GitHub's exact reply or resolve endpoint differs for review comments vs threads, the implementation must isolate that difference in `thread-reply` helper code and cover it with fixtures.

### FR-9: Hook update

- `FR-9.1` Update `/config/workspace/IronClaude/src/superclaude/hooks/scripts/offer-pr-review.sh` to mention `/sc:submit-pr --monitor` as the autonomous path.
- `FR-9.2` The hook remains fail-open and must never spawn a monitor itself.
- `FR-9.3` The hook must continue to offer `/sc:auggie-review` as the manual review path.
- `FR-9.4` The hook message must not imply level-3 autonomy without explicit user invocation.

### FR-10: Sync and install discipline

- `FR-10.1` After implementation edits under `/config/workspace/IronClaude/src/superclaude/`, run `make sync-dev`.
- `FR-10.2` Run `make verify-sync` before commit.
- `FR-10.3` Do not stage `.claude/skills`, `.claude/commands`, `.claude/agents`, `.claude/hooks`, or `.claude/templates`; only `/config/workspace/IronClaude/.claude/settings.json` is eligible if explicitly changed.

## Non-Functional Requirements

### NFR-1: Idempotency

All outward actions must be idempotent across crash, resume, duplicate polls, duplicate review emissions, and operator re-arming. The minimum durable idempotency sets are `processed_review_ids`, `processed_finding_ids`, `replied_comment_ids`, `resolved_thread_ids`, and `pushed_commit_shas`.

### NFR-2: Rate-limit safety

The poll loop must not poll faster than every 30 seconds and must back off exponentially on GitHub API rate limits. V1.0 must prefer missing a review for a few extra minutes over burning through rate limits or triggering abuse detection.

### NFR-3: Recoverability

The `.jsonl` run-log is the recovery substrate. A resumed monitor must be able to answer: what review was processed, which findings were fixed, whether validation passed, which commit was pushed, which comments were replied to, and which threads were resolved.

### NFR-4: Fail-safe classification

Unknown severity becomes Medium. Unknown bot login becomes not detected. Unknown shape becomes logged and ignored. The system must never auto-act on comments whose origin cannot be authenticated as Augment.

### NFR-5: Observability

Every poll, classifier decision, route, validation command, push, reply, resolve, backoff, and terminal state must be machine-readable in the run-log. Human-readable summaries are optional; machine-readable events are mandatory.

### NFR-6: Data integrity

State snapshots are caches, not source of truth. If a snapshot conflicts with the JSONL log, rebuild from JSONL. Corrupt JSONL events must stop resume with `S14_TERMINAL_FAILED` unless the user explicitly chooses a recovery point.

### NFR-7: Security and permission minimization

The monitor uses the authenticated `gh` CLI and local git credentials only. It must not store tokens in the run-log. It must redact environment variables and command stderr that may include credentials.

### NFR-8: Determinism

Given the same captured GitHub API fixtures and same initial state, the classifier, round counter, route decisions, and terminal outcome must be deterministic.

### NFR-9: Operator clarity

All terminal states must print the PR URL, terminal reason, round count, residual Medium+ finding count, and run-log path. User-facing file paths must be absolute.

## Failure Modes & Recovery

### FM-1: Review never arrives

- Detection: timeout expires in `S3_WAITING_FOR_REVIEW`.
- Action: `S12_TERMINAL_TIMEOUT`.
- Recovery: user can re-arm with `/sc:submit-pr --resume /config/workspace/IronClaude/.dev/pr-monitor/.../monitor-run-<PR>.jsonl`.

### FM-2: GitHub primary or secondary rate limit

- Detection: 403/429 with rate-limit headers or known secondary-limit body.
- Action: append `api_backoff`, exponential backoff, continue until timeout.
- Recovery: no operator action unless timeout occurs.

### FM-3: Unknown Augment emission shape

- Detection: possible Augment author but body cannot be parsed into findings.
- Action: append `classifier_unknown_shape`; if no actionable review appears, timeout.
- Recovery: fixtures from the unknown payload must be added before parser changes.

### FM-4: Unknown bot identity

- Detection: review/comment/check author not in Augment allowlist.
- Action: ignore as `D0_NO_REVIEW_YET`.
- Recovery: run empirical probe and update the centralized bot identity constant if Augment changed identity.

### FM-5: Validation failure

- Detection: targeted tests, `make test`, `make lint`, or `uv run ruff format --check src/ tests/` fails.
- Action: no push, no reply, no resolve. Level 2 halts. Level 3 may attempt one correction only if within round budget; otherwise halt.
- Recovery: user inspects validation artifacts and resumes or manually fixes.

### FM-6: Crash after push before reply

- Detection: resume state has `push_completed` for a round but missing `reply_posted` for one or more fixed comment IDs.
- Action: do not re-run fixes; post missing replies once, then resolve threads if validation and push evidence exist.
- Recovery: automatic via idempotency sets.

### FM-7: Crash after reply before resolve

- Detection: `replied_comment_ids` contains comment ID but `resolved_thread_ids` lacks thread ID.
- Action: do not post another reply; resolve only the missing thread.
- Recovery: automatic via idempotency sets.

### FM-8: Duplicate Augment review or duplicate poll payload

- Detection: review ID or stable finding ID already in processed sets.
- Action: append `idempotency_skip`; no route, no fix, no reply.
- Recovery: no operator action.

### FM-9: Round cap reached with residual findings

- Detection: new actionable review arrives and `round_index >= max_rounds` would be exceeded by another remediation.
- Action: `S11_TERMINAL_MAX_ROUNDS`; optionally post a summary comment only if level 3 and prior validation/push actions were successful; do not fix further.
- Recovery: user manually decides whether to run another explicit command with higher `--max-rounds`, capped at 5.

### FM-10: Needs-human-decision finding

- Detection: classifier or troubleshoot marks finding as ambiguous intent, API contract, security trade-off, migration behavior, or user-visible default.
- Action: `S13_TERMINAL_HALTED`; no auto-mutation for that finding.
- Recovery: user provides decision; monitor can resume with decision captured in run-log.

### FM-11: Misrouted PR URL

- Detection: returned PR URL is not under `https://github.com/IronbellyOrg/IronClaude/pull/`.
- Action: `S14_TERMINAL_FAILED`; do not monitor; instruct operator to close wrong PR.
- Recovery: recreate PR using mandatory `--repo IronbellyOrg/IronClaude` shape.

### FM-12: Corrupt run-log or snapshot

- Detection: JSON parse failure, missing required envelope keys, non-monotonic event sequence, or snapshot/log disagreement that cannot be rebuilt.
- Action: `S14_TERMINAL_FAILED` and require explicit recovery point.
- Recovery: user may choose last valid event ID; implementation must not guess.

## Acceptance Criteria

### AC-1: Monitor level 0 regression

Given a valid branch and PR metadata, `/sc:submit-pr --monitor 0 --base master --head <branch> --title "T" --body "B"` creates a PR with `--repo IronbellyOrg/IronClaude`, verifies the returned fork URL, writes no monitor run-log, and starts no Monitor tool.

### AC-2: Poll interval enforcement

Given `--poll-interval 10`, the command rejects the invocation before monitor arming with a clear error that the minimum is 30 seconds.

### AC-3: Review never arrived

Given GitHub fixtures with no post-arm Augment emission for 1800 seconds of simulated time, the monitor emits `terminal_timeout`, performs no edits, no pushes, no replies, and exits cleanly.

### AC-4: Rate-limit backoff

Given a poll sequence of 403 secondary-limit, 403 secondary-limit, then success, the run-log contains backoff sleeps of 30 then 60 seconds, resets backoff after success, and never polls below the configured interval.

### AC-5: Three-state classifier

Given fixtures for no review, Augment review with Low/Nit only, and Augment review with one Medium finding, the classifier returns respectively `D0_NO_REVIEW_YET`, `D1_REVIEW_ZERO_MEDIUM_PLUS`, and `D2_REVIEW_WITH_FINDINGS`.

### AC-6: Unknown safety defaults

Given a finding with unknown severity from an allowed Augment bot, normalized severity is Medium. Given the same body from an unknown bot login, classifier returns no detected review and takes no action.

### AC-7: Loop guard off-by-one

With `--max-rounds 2`, fixtures containing three consecutive post-arm Augment reviews with Medium findings produce exactly two remediation attempts; the third review transitions to `terminal_max_rounds` without troubleshoot, fix, push, reply, or resolve.

### AC-8: Re-review counts as next round

After a level-3 push, the next Augment review with Medium+ findings increments the same `round_index` from 1 to 2. It does not start a fresh run or reset the counter.

### AC-9: Idempotent reply resume

Given a run-log with `reply_posted` for comment `456` and no `thread_resolved`, resume posts no duplicate reply for `456` and performs only the missing resolve action after verifying push/validation evidence.

### AC-10: Validation no-push

Given a successful fix followed by failing `uv run ruff format --check src/ tests/`, the monitor does not commit, push, reply, or resolve, and terminal state is halted or failed according to monitor level.

### AC-11: Required validation commands

Every level-3 successful push has preceding `validation_completed` events showing passing targeted tests or `make test`, passing `make lint`, and passing `uv run ruff format --check src/ tests/`.

### AC-12: Level behavior

- Level 1 produces no file edits.
- Level 2 may produce file edits and validation artifacts but no commit, push, reply, or resolve.
- Level 3 may commit, push, reply, and resolve only after validation passes.

### AC-13: Human decision halt

A finding marked `needs_human_decision` halts at level 3 before mutation, with a run-log event identifying the finding and decision needed.

### AC-14: Hook stays fail-open

The updated offer hook continues to exit 0 for all payloads, never starts a monitor itself, and includes both the manual `/sc:auggie-review` path and the autonomous `/sc:submit-pr --monitor` path in the surfaced offer.

### AC-15: Fork targeting

Tests or static checks prove every `gh pr create`, `gh pr view`, `gh pr diff`, `gh pr review`, and supported `gh` PR command in the new workflow pins `--repo IronbellyOrg/IronClaude`, and every `gh api` path uses `repos/IronbellyOrg/IronClaude/...`.

### AC-16: Resume reconstruction

Given a JSONL log and absent snapshot, the monitor rebuilds `state.snapshot.json` exactly enough to preserve processed reviews, processed findings, replied comments, resolved threads, pushed commits, round index, and terminal status.

## Risks & Mitigations

### R-1: Augment GitHub emission shape is unknown

Risk: The monitor may look at the wrong API surface or parse the wrong author field.

Mitigation: Before parser release, capture a real Augment review fixture using `gh pr view`, `gh api repos/IronbellyOrg/IronClaude/pulls/<N>/reviews`, `gh api repos/IronbellyOrg/IronClaude/pulls/<N>/comments`, and, if needed, check-runs. Lock the bot identity and payload shape in fixtures.

### R-2: Infinite remediation loop

Risk: A naive loop treats every re-review as a fresh trigger and keeps pushing indefinitely.

Mitigation: Use the monotonic `round_index` keyed to reviews observed since arm, default `--max-rounds 2`, cap `5`, and test the three-review off-by-one fixture.

### R-3: Duplicate PR spam after crash/resume

Risk: Session loss after reply or before resolution can cause duplicate replies or contradictory status comments.

Mitigation: Durable `replied_comment_ids`, `resolved_thread_ids`, and `idempotency_skip` events. Resume must complete missing later actions without repeating earlier actions.

### R-4: Rate-limit or abuse detection

Risk: Polling too fast or retrying aggressively can exhaust GitHub limits.

Mitigation: Reject intervals below 30 seconds; exponential backoff on 403/429/secondary-limit; cap sleeps at 300 seconds; count backoff against timeout.

### R-5: False-positive bot detection

Risk: The monitor acts on a human or unrelated bot comment that resembles a code review.

Mitigation: Unknown bot login is not detected. Only centralized empirically validated Augment identities can trigger action.

### R-6: Under-validation before push

Risk: Targeted tests pass but repo-level lint or format fails in CI.

Mitigation: Require `make lint` and `uv run ruff format --check src/ tests/` for every push; escalate to `make test` for cross-cutting changes.

### R-7: Human-intent ambiguity auto-shipped

Risk: Level 3 applies a technically valid fix that changes product behavior or security posture incorrectly.

Mitigation: `needs_human_decision` halts all autonomy levels before mutation or push; this rule is stronger than `--monitor 3`.

### R-8: Run-log corruption

Risk: The recovery substrate is partially written or manually edited.

Mitigation: JSONL append-only events with required envelope, monotonic event IDs, snapshot as cache only, and fail-closed recovery when log validity cannot be established.

### R-9: PR target leaks to upstream

Risk: `gh pr create` defaults to the upstream parent of the fork.

Mitigation: Mandatory `--repo IronbellyOrg/IronClaude`, pre-PR remote verification, returned URL verification, and AC-15 static checks.

### R-10: V1 in-session monitor dies silently

Risk: The terminal/session closes while waiting for Augment or between push and reply.

Mitigation: Document V1 limitation prominently, write run-log before every external action, and support `--resume <run-log>` as a first-class path.
