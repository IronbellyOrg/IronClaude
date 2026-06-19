---
name: sc:pr-submit-protocol
description: "PR-review auto-remediation monitor — opens a PR on the fork, arms an in-session Monitor that polls for the Augment Code review, re-grades + verifies each finding, dispatches verified findings to /sc:troubleshoot, then (at higher ordinals) fixes, validates, pushes, replies, and resolves under a capped monotonic round counter. The --monitor {0,1,2,3} ordinal is a capability ceiling on ONE finite state machine, not four code paths."
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill
---

<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: advanced
mcp-servers: [sequential, serena, auggie]
personas: [analyzer, architect, security, qa, devops]
-->

# sc:pr-submit — PR Review Auto-Remediation Monitor

## Purpose

`sc:pr-submit` opens a PR on the resolved origin repo (origin's `owner/repo` — never an upstream parent), arms an
**in-session** Monitor that polls for the Augment Code review, re-grades each finding's severity
through the reused auggie-review rubric, **verifies each finding grounds in real code before
remediating** (verify-before-remediate — no round and no push is ever spent on a hallucinated or
stale finding), dispatches only verified findings to `/sc:troubleshoot` for diagnosis, then — at
higher autonomy ordinals — applies the fix itself, validates, pushes, replies on the finding
thread, and resolves it. It terminates deterministically under a capped, monotonic round counter.

**The `--monitor {0,1,2,3}` ordinal is a capability ceiling on a SINGLE finite state machine**
(`refs/state-machine.md`), compared at exactly three gates plus one override — NOT four divergent
code paths. The deterministic decisions (classification, severity remap, the FSM gate table, the
loop-guard fence-post, the push conjunction) are owned by the importable `superclaude.pr_submit`
Python core; this SKILL.md owns sequencing, the Monitor arming, the `gh`/`git` I/O (via the bash
scripts), and the §10 VAL validator.

> **Honest framing (FR-2.4, NOT a daemon).** The Monitor is **in-session**: closing the session
> loses the monitor. Durability comes from the write-ahead JSONL run-log + `--resume`, never from
> detachment. This skill cannot survive its own session. Do NOT imply a background daemon.
>
> **Top-level activation required.** This skill MUST run in the main orchestrating session (so it
> has the `Monitor` tool and can `> Skill sc:troubleshoot-protocol`). Do NOT run it inside an
> Agent-tool subagent that itself spawns skills.

## Required Input (STOP if missing)

| Input | Required | Notes |
|-------|----------|-------|
| `--monitor {0,1,2,3}` | No (defaults to 1) | The autonomy ceiling. Explicit 0 = open PR only (byte-identical to today). |
| PR context (`--head`, `--base`, `--title`, `--body`) OR an existing PR number | Yes | To open or attach to the PR. |
| `--max-rounds` | No (default 2, hard cap 5) | Reject `> 5`. |
| `--poll-interval` | No (default 30) | Reject `< 30` with "minimum is 30 seconds". |
| `--timeout` | No (default 600s) | Wall-clock since entering wait. |
| `--resume <abs-run-log-path>` | No | Reconstruct state from JSONL (§12). |

**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's
`owner/repo` via `gh repo view --json nameWithOwner`): a wrong origin, a branch behind the base
branch (`origin/<default-branch>`), or a returned URL whose `owner/repo` ≠ the resolved target → HALT,
instruct the operator to close the misrouted PR. **STOP** if `detection-contract.md` is `locked: false`
— the skill refuses to arm until the R1 probe locks the contract (T-210, "probe first").

## Output Contract

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `terminal_clean` / `terminal_max_rounds` / `terminal_halted` / `terminal_timeout` / `terminal_failed` / `proposed` / `halt_before_push` |
| `pr_url` | string | The PR URL (verified to match the resolved origin `owner/repo`). |
| `round_counter` | int | Completed remediation cycles (monotonic; user-facing label = `+1`). |
| `push_count` | int | Landed pushes (== `max_rounds` at most; 0 below L3). |
| `reply_count` | int | Threads replied to. |
| `summary_posted` | bool | Whether the single clean-re-review summary thread was posted. |
| `applied_edits` | int | Grounded edits applied this run (INV-016 predicate 5). |
| `rereview_request_count` | int | S5a `auggie review` re-trigger comments posted (INV-R1; monotone, `<= max_rounds`). |
| `fallback_engaged` | bool | Whether the oversized-PR `/sc:auggie-review` fallback was engaged (a `declined` was observed). |
| `auggie_review_invoked` | bool | Whether `/sc:auggie-review` was actually invoked (INV-R2 strict-once; at most once per PR). |
| `fallback_round_counter` | int | The SEPARATE single-shot fallback counter (cap 1, independent of `round_counter`). |
| `run_log_path` | string | The authoritative `monitor-run-<PR>.jsonl`. |

## Wave / Phase Structure (refs are LAZY-loaded per wave, never pre-loaded)

```text
Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)
Wave 1: Arm + poll                ← loads refs/detection-contract.md (arm gate) + refs/augment-poll.md
Wave 2: Classify + re-grade       ← loads refs/severity-routing.md
Wave 3: Verify-before-remediate   ← loads refs/finding-verify.md
Wave 4: Diagnose + (L2+) fix      ← loads refs/troubleshoot-dispatch.md
Wave 5: Validate                  ← the VAL validator (§10 gate list, below)
Wave 6: (L3) push + reply + resolve + re-trigger ← loads refs/thread-reply.md + refs/review-retrigger.md (S5a)
Wave 6b: (L3) decline → auggie fallback           ← loads refs/auggie-fallback.md (S5b, strict-once)
Wave 7: Loop / terminate          ← loads refs/loop-guard.md
```

- **Wave 0 (all ordinals):** resolve the target repo once (`REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"`, fallback parse `git remote get-url origin`) and the base branch (`gh repo view --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`); open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."`; confirm `git remote -v` shows origin = `$REPO`; rebase if behind `origin/<base>`; verify the returned URL's `owner/repo` equals `$REPO` (a CLI that defaulted onto an upstream parent is a misroute → HALT). Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1). The `offer-pr-review.sh` hook may then mention `sc:pr-submit --monitor`.
- **Wave 1 (L1+):** load the locked contract via `superclaude.pr_submit.DetectionContract.for_arming()` — this prefers the **operator-local** locked override (gitignored `.dev/pr-monitor/detection-contract.locked.md`, populated by the R1 probe with this fork's real Augment values) and falls back to the SHIPPED `refs/detection-contract.md` (which stays `locked: false`). **Refuse to arm if no locked contract resolves** (T-210, "probe first"). Initialize the output-dir + run-log + baseline, then call the **`Monitor` tool** with the poll loop wrapping `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s); each emitted JSON line advances the FSM. Arm exactly once at L1+ (T-109); never at L0 (T-110).
- **Wave 2:** load `refs/severity-routing.md`; call `remap_severity(finding)` from `superclaude.pr_submit` and map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`.
- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces. `unverified` → REPORT_ONLY, consuming NO round.
- **Wave 4:** load `refs/troubleshoot-dispatch.md`; for VERIFIED findings only, `> Skill sc:troubleshoot-protocol` for diagnosis. **At L1 (G-edit `ordinal < 2`): PROPOSE "fix these? y/n" and apply NO edits.** At L2+ the skill applies the diagnosed edits ITSELF in the working tree (troubleshoot does NOT auto-apply — `sc:pr-submit` owns edit application in `S3_FIXING`).
- **Wave 5:** run the VAL validator (below). **At L2 the ceiling stops here:** after applying the edits in `S3_FIXING` and validating in `S7_VALIDATING`, the FSM HALTs at `S4'_HALT_BEFORE_PUSH` — changes are left in the working tree with NO commit, NO push, NO reply (`S3_FIXING → S7_VALIDATING → S4'_HALT_BEFORE_PUSH`, matching `state-machine.md` §5.2a). Only L3 proceeds to Wave 6.
- **Wave 6 (L3 only):** load `refs/thread-reply.md`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch) ONLY when the conjunction holds, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve). **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger an Augment re-review — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`), post the re-trigger comment via `scripts/retrigger-review.sh --pr <N>` BEFORE re-entering the S5 poll. The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`); the script does the `gh api` issue-comment POST (NFR-6). On posting the re-trigger, append a **`rereview_requested{cycle_id}`** run-log event (the INV-R1 producer — folded into `rereview_request_count` by `rebuild_state`, and consumed by crash recovery's OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.
- **Wave 6b (L3 only — decline fallback, FR-9/FR-10):** load `refs/auggie-fallback.md`. When the classifier returns `declined` (an Augment "abnormally large" decline observed at the initial S2 poll OR the S5 re-trigger poll), append a **`decline_detected`** run-log event, then engage the single-shot fallback: gate **strict-once** on the durable `auggie_review_invoked` idempotency record (comment-independent, survives resume — INV-R2; on engage, append an **`auggie_fallback_invoked{pr_number}`** event, the producer folded into that set), clamp the effective budget `effective_max_rounds := min(effective_max_rounds, 1)` (the `clamp_max_rounds` helper, recorded once via the **`max_rounds_clamped{effective_max_rounds}`** event — INV-R3 monotone-min fold), then invoke `> Skill sc:auggie-review-protocol --depth quick --remediation-offer` and re-enter Waves 2-6 ONCE under the clamp (verify-before-remediate still applies — fallback findings are NOT trusted verbatim, FR-9.4). NO second invoke, NO second re-trigger, NO loop-back; `push_count <= max_rounds + 1` for the whole run. This is `sc:pr-submit` invoking its OWN review — do **NOT** "take the App's bait" by treating the App's `augment review` decline comment as our operator re-trigger. (`--depth quick` here targets `/sc:auggie-review` — a review, no `--fix` — so it does NOT conflict with the severity-routing STOP on `--depth quick --fix`.)
- **Wave 7:** load `refs/loop-guard.md`; the round counter ticks only at `S5_AWAITING_REREVIEW → S2_CLASSIFY`; HALT at `round_counter >= max_rounds`. Fallback outcomes REUSE the existing `terminal_clean` / `terminal_max_rounds` status values (OQ-2 reuse recommendation).

## VAL — the §10 validation gate list (owned by the SKILL, not the core)

Run IN ORDER, all green ⇒ `validation_status == "validated"` (the INV-016 predicate 2). Any
non-zero gate blocks the push:

1. **VG-1** targeted tests (`uv run pytest <changed-area>`).
2. **VG-2** cross-cutting change → escalate to `make test`.
3. **VG-3** `make lint` (ruff check ONLY).
4. **VG-4** `uv run ruff format --check src/ tests/` (a SEPARATE gate — green VG-3 does NOT imply green VG-4; never collapse the two).
5. **VG-5** `make verify-sync` (skill-self-edits only; blocks at commit).
6. **VG-6** PR-target check (blocks at arm; the returned URL's `owner/repo` must equal the resolved origin repo).

A validation retry does NOT increment `round_counter`.

## Will Do

- Open the PR on the resolved origin repo with `--repo "$REPO"` pinned on every `gh` call (computed from origin, never bare).
- Verify before remediate; dispatch only verified findings; report unverified ones.
- Apply edits, validate, push, reply, and resolve ONLY within the ordinal ceiling.
- Keep the deterministic decisions in `superclaude.pr_submit`; keep `gh`/`git` I/O in the scripts.

## Will Not Do

- Run headless / detached, or imply a background daemon (V1 limitation).
- Push to an upstream parent remote or to the repo's default/protected branch; open a PR against an upstream parent the CLI might default to.
- Auto-lock `detection-contract.md` or hard-guess the Augment bot login.
- Emit `--depth quick --fix` to troubleshoot (a STOP conflict).
- Apply any edit at L1, or push/reply at L2.
- `git add` any `.claude/` path except `.claude/settings.json`.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| `detection-contract.md` `locked:false` | HALT at arm with "probe first" (T-210). |
| Wrong origin / behind base branch / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
| Review never arrives | `terminal_timeout`; no edits/push. |
| 403 / 429 / secondary-limit | exponential backoff 30→…→cap 300s, counts toward timeout. |
| `needs_human_decision` finding | `terminal_halted`; no auto-mutation (override, FR-4.4). |
| Validation failure | no push/reply/resolve; L2 halt; L3 one retry within budget. |
| Crash mid-push | `--resume` 3-way recovery (§12); no double push, no re-fix. |
