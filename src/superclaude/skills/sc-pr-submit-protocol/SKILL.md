---
name: sc:pr-submit-protocol
description: "PR-review auto-remediation monitor — opens a PR on the fork, runs an attended in-session poll loop for the Augment Code review, re-grades + verifies each finding, dispatches verified findings to /sc:troubleshoot, then (at higher ordinals) fixes, validates, pushes, replies, and resolves under a capped monotonic round counter. The --monitor {0,1,2,3} ordinal is a capability ceiling on ONE finite state machine, not four code paths."
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(gh *), Bash(git *), Bash(uv *), Bash(make *), Bash(jq *), Task, Skill
---

<!-- Extended metadata (for documentation, not parsed):
category: quality
complexity: advanced
mcp-servers: [auggie]
personas: [analyzer, architect, security, qa, devops]
-->

# sc:pr-submit — PR Review Auto-Remediation Monitor

## Purpose

`sc:pr-submit` opens a PR on the resolved origin repo (origin's `owner/repo` — never an upstream parent), runs an
**attended, in-session** poll loop for the Augment Code review, re-grades each finding's severity
through the reused auggie-review rubric, **verifies each finding grounds in real code before
remediating** (verify-before-remediate — no round and no push is ever spent on a hallucinated or
stale finding), dispatches only verified findings to `/sc:troubleshoot` for diagnosis, then — at
higher autonomy ordinals — applies the fix itself, validates, pushes, replies on the finding
thread, and resolves it. It terminates deterministically under a capped, monotonic round counter.

**The `--monitor {0,1,2,3}` ordinal is a capability ceiling on a SINGLE finite state machine**
(`refs/state-machine.md`), compared at exactly three gates plus one override — NOT four divergent
code paths. The deterministic decisions (classification, severity remap, the FSM gate table, the
loop-guard fence-post, the push conjunction) are owned by the importable `superclaude.pr_submit`
Python core; this SKILL.md owns sequencing, the attended poll loop, the `gh`/`git` I/O (via the bash
scripts), and the §10 VAL validator.

> **Honest framing (FR-2.4, NOT a daemon).** The monitor is an **attended, in-session** loop:
> closing the session loses it. Durability comes from the write-ahead JSONL run-log + `--resume`,
> never from detachment. This skill cannot survive its own session. Do NOT imply a background daemon.
>
> **Top-level activation required.** This skill MUST run in the main orchestrating session (so it
> can drive the attended poll loop and `> Skill sc:troubleshoot-protocol`). Do NOT run it inside an
> Agent-tool subagent that itself spawns skills.

## Attended poll loop (Waves 1, 6 re-review, 8)

"Arming" means the main session enters this loop; there is no separate monitor tool. Record the
wall-clock start when entering a wait (Wave 1, the S5 re-review wait, or the Wave 8 CI flip), then:

1. Run the wave's poll script **once** in the foreground (`scripts/poll-augment-review.sh` or
   `scripts/poll-ci-checks.sh`, always `--repo "$REPO"`). A non-zero exit is a prerequisite or
   usage failure: stop and report it, never retry it as `polling`.
2. Classify the one JSON line with the existing core: use the **Augment snapshot gate** below,
   or `superclaude.pr_submit.ci.classify_checks` for CI; append the run-log event only after the gate.
3. Validated non-polling result → leave the wait and continue the wave. For Augment `polling`, do **not**
   call raw `timed_out`. Compute `silent = poll_succeeded(payload) and not has_augment_activity(payload, contract)`, then
   `st = rebuild_state()`, `already = pr in st["silence_rerequest_invoked"]`,
   `clock = st["silence_rerequested_at"]`, and
   `nxt = poll_outcome(review_state, elapsed, timeout, silent=silent, silence_timeout=silence_timeout, rerequested=already, rerequested_at=clock, monitor_ordinal=ordinal)`.
   `S5C_SILENCE_REREQUEST` is consider-once, not POST-now: if
   `check_idempotent("silence_rerequest_invoked", pr)` is False, skip the POST, sleep ≥ `--poll-interval`, continue.
   If True, append `{event_type: silence_rerequested, pr_number, elapsed}` then
   `scripts/retrigger-review.sh --body "augment review" --pr <N> --repo "$REPO"`. That write-ahead pair
   does not tick `round_counter` or `rereview_request_count`. Then sleep ≥ `--poll-interval` and continue.
   `TERMINAL_AUGMENT_NO_RESPONSE` → report App trigger mode, Allowlist, quota; comment `augment review` by hand; Wave 8 wait-only (`should_arm_ci_wait` True, `ci_wait_autofix` False); never `transition(clean)`.
   `TERMINAL_TIMEOUT` → partial activity, no Wave 8. CI `polling` still uses `timed_out` for the Wave 8 timeout. Else wait **at least** `--poll-interval` seconds (or `fsm.next_backoff` after
   403/429; the wait counts toward `--timeout`) with a bounded blocking wait the host permits, then
   repeat from 1.

The main session performs every verification, `> Skill sc:troubleshoot-protocol` handoff, VAL run,
and authorized push / reply / resolve itself. Never hand a side effect to a background shell,
detached loop, or subagent, and never claim the wait survives session exit. The ordinal gates
(L0/L1/L2/L3), `round_counter` / `max_rounds`, and `HALT_MAX_ROUNDS` preservation are unchanged by
the loop.

### Augment snapshot gate (normative; before any FSM outcome)

For the initial wait set `pushed_sha = None`, `watermark = None`. In S5 retain the exact pushed full
SHA and a trustworthy UTC re-trigger watermark (see `refs/review-retrigger.md`). On each poll execute
this gate using the same immutable snapshot; the public explicit head argument is an **override**,
not a comparison against the actual snapshot head:

```python
from superclaude.pr_submit import (
    actionable_finding_comments, classify, finding_from_comment, remap_severity, route,
)

expected_head = payload.get("head_sha") if pushed_sha is None else pushed_sha
findings = []
routes = []
if pushed_sha is not None and (
    payload.get("head_sha") != pushed_sha or watermark is None
):
    review_state = "polling"
else:
    review_state = classify(
        payload, contract, watermark=watermark, current_head_sha=expected_head,
    )
    if review_state == "findings":
        selected = actionable_finding_comments(
            payload, contract, watermark=watermark, current_head_sha=expected_head,
        )
        try:
            if not selected:
                raise ValueError("findings signal without actionable root details")
            findings = [finding_from_comment(raw) for raw in selected]
        except ValueError:
            review_state = "polling"
            findings = []
        else:
            findings = [remap_severity(finding) for finding in findings]
            routes = [route(finding) for finding in findings]
```

An empty selection is possible with legacy `has_findings` / `findings_count` signals; invalid roots
raise `ValueError`. Both are **incomplete**, not clean: resume step 3's bounded polling without
resetting elapsed time. Never pass `review_state="findings"` with an empty `findings` list to
`run_skill`: its legacy injected-input driver would optimistically declare clean. Do not use a
second body parser, raw `comments` filter, or an invented completion event.

Only the gated `clean` or successfully normalized `findings` result can establish a live attributed
re-review. During S5 require **both** exact snapshot/pushed head agreement and completion strictly
newer than the watermark before supplying the existing `rereview_attributed` edge (or explicit
`RunConfig.rereview_outcome` token `"attributed"`). Never rely on the empty outcome sequence's
optimistic legacy default; `polling` keeps waiting, expiry supplies `"timeout"`, and `declined`
uses the existing fallback without a round tick. No clean, round increment or remediation on a head
mismatch, incomplete snapshot or normalization failure. CI retains its independent Wave 8 gate.

The normalized findings then pass Waves 2–3: Low/Nit report-only, other tiers still require the
read-only evidence-validator before diagnosis or edits. `verification_status` starts `"unverified"`;
remote verification claims are ignored. An outdated unresolved root remains visible even when
`line is None`; `original_line` is only a verification hint, never substituted for current line.
Existing grounding rejects a null current line; it cannot authorize an automatic fix.

## Required Input (STOP if missing)

| Input | Required | Notes |
|-------|----------|-------|
| `--monitor {0,1,2,3}` | No (defaults to 3) | The autonomy ceiling. Explicit 0 = open PR only (byte-identical to today). |
| PR context (`--head`, `--base`, `--title`, `--body`) OR an existing PR number (`--pr <N>`) | Yes | To open or attach to the PR. |
| `--max-rounds` | No (default 2, hard cap 5) | Reject `> 5`. |
| `--poll-interval` | No (default 30) | Reject `< 30` with "minimum is 30 seconds". |
| `--timeout` | No (default 600s) | Wall-clock since entering wait. The observed CI matrix has run longer than 600s: for a CI wait, pass a `--timeout` that covers the full check run. No indefinite wait. |
| `--silence-timeout` | No (default 300s) | No-Augment-activity window. Reject `< 30`. Clamped to `--timeout`. L3 may re-request once. |
| `--resume <abs-run-log-path>` | No | Reconstruct state from JSONL (§12). |

**STOP** if `--monitor >= 1` and the PR cannot be confirmed on the resolved target repo (origin's
`owner/repo`, parsed from `git remote get-url origin`): a wrong origin, a branch behind the base
branch (`origin/<default-branch>`) on the create path, or a returned URL whose `owner/repo` ≠ the resolved target → HALT,
instruct the operator to close the misrouted PR.

**STOP (CI-wait preflight)** before opening a PR with `--monitor >= 1` or attaching to an existing PR,
unless both hold: (1) `gh pr checks --repo "$REPO" --help` lists `--json` (probe the installed CLI;
never infer support from a version number); (2) the Python runtime this run classifies with can
import `superclaude.pr_submit.ci` (e.g. `uv run python -c "import superclaude.pr_submit.ci"` in a dev
checkout, or the installed package's interpreter). Report which prerequisite is missing; do not arm a
monitor that could only ever report `polling`. `--monitor 0` skips this preflight.

## Output Contract

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `terminal_clean` / `terminal_max_rounds` / `terminal_halted` / `terminal_timeout` / `terminal_augment_no_response` / `terminal_failed` / `proposed` / `halt_before_push` |
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

When CI wait follows Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, preserve that Augment status and report CI's observed outcome (including timeout or human-gate) alongside it in the summary. CI clean is not an Augment clean re-review.

## Wave / Phase Structure (refs are LAZY-loaded per wave, never pre-loaded)

```text
Wave 0: Open PR + verify target   ← (no ref; gh pr create --repo, pre-PR checks)
Wave 1: Arm + poll                ← loads refs/detection-contract.md (baked identity) + refs/augment-poll.md
Wave 2: Classify + re-grade       ← loads refs/severity-routing.md
Wave 3: Verify-before-remediate   ← loads refs/finding-verify.md
Wave 4: Diagnose + (L2+) fix      ← loads refs/troubleshoot-dispatch.md
Wave 5: Validate                  ← the VAL validator (§10 gate list, below)
Wave 6: (L3) push + reply + resolve + re-trigger ← loads refs/thread-reply.md + refs/review-retrigger.md (S5a)
Wave 6b: (L3) decline → auggie fallback           ← loads refs/auggie-fallback.md (S5b, strict-once)
Wave 7: Loop / terminate          ← loads refs/loop-guard.md
Wave 8: CI wait (after Augment clean / REPORT_ONLY / HALT_MAX_ROUNDS / TERMINAL_AUGMENT_NO_RESPONSE) ← loads refs/ci-poll.md
```

- **Wave 0 (all ordinals):** resolve the target repo once from the origin remote (`REPO="$(git remote get-url origin | sed -E 's#^ssh://[^/]+/##; s#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##')"`; only if origin has no URL, fall back to `gh repo view --json nameWithOwner -q .nameWithOwner` — never prefer it, because gh picks an `upstream` remote over `origin`) and the base branch (`gh repo view "$REPO" --json defaultBranchRef -q .defaultBranchRef.name`, overridable via `--base`). BEFORE creating anything: confirm `git remote -v` shows origin = `$REPO` and rebase if behind `origin/<base>` (with `--pr <N>`, at any level, do not rebase: the PR head is already published, so report how many commits it is behind instead). Then open the PR with `gh pr create --repo "$REPO" --base <base> --head <head> --title "..." --body "..."` and verify the returned URL's `owner/repo` equals `$REPO` (a misroute → HALT). With `--pr <N>`, skip `gh pr create` and attach to that PR instead, checking the URL from `gh pr view <N> --repo "$REPO" --json url`. Pass `--repo "$REPO"` to every poll/reply/retrigger script too. At **L0 (`--monitor 0`)** the FSM never leaves `S0_IDLE` — open the PR and return, byte-for-byte identical to today (AC-1).
- **Wave 0 head binding (L1+ only; L0 skips it):** after `gh pr create`, or on `--pr <N>` attach, read the PR head with `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` (a failed or unparsable read → HALT) and the checkout with `git branch --show-current` and `git rev-parse HEAD`. Require `superclaude.pr_submit.fsm.pr_head_ok(local_branch, local_sha, headRefName, headRefOid, isCrossRepository, allow_cross_repo=(ordinal < 3))`; a head on a fork is allowed only below L3, where nothing is pushed. False → HALT before Wave 1 with status `terminal_halted`, reason `pr_head_mismatch` (appended to the run-log when one exists), and tell the operator: "PR #<N>'s head `<headRefName>`@<headRefOid> does not match your checkout `<local_branch>`@<local_sha>. Do not close the PR. Check out `<headRefName>` and make it equal the PR head (push if you are ahead; a branch Wave 0 rebased needs a force-push, which this skill never does for you; `git pull --ff-only` if you are behind), then re-run with `--pr <N>`." True → bind `HEAD_BRANCH := headRefName` and `pre_push_sha := headRefOid` for the whole run; every push targets `HEAD_BRANCH`, never the checkout's branch name. `--resume` repeats this binding against the live PR: when crash recovery finds a dangling `push_initiated`, check only the branch (`pr_branch_ok(local_branch, headRefName, isCrossRepository, allow_cross_repo=(ordinal < 3))` and `pr_branch_ok(<the record's target_branch>, headRefName, False)`), leave the SHA to `resolve_crash_window` (local HEAD may already be the fix commit), and set `pre_push_sha` from that record: its `target_sha` when the push landed (Branch A), its `pre_push_sha` when the push is re-driven (Branch B: skip the Wave 6 fix commit, set `target_sha` from the record, and the re-driven push first runs the Wave 6 pre-push head guard with the record's `pre_push_sha`; after Branch A, the guard's parent check stops the next push if local commits were made since the landed push); otherwise require the full `pr_head_ok` and set `pre_push_sha := headRefOid`.
- **Wave 1 (L1+):** load the contract via `superclaude.pr_submit.DetectionContract.for_arming()` — prefers an optional operator-local override (gitignored `.dev/pr-monitor/detection-contract.locked.md`) and falls back to the SHIPPED `refs/detection-contract.md` (baked `augmentcode[bot]` / `augmentcode` defaults). A missing or unlocked override is not a halt. Initialize the output-dir + run-log + baseline, then enter the **attended poll loop** (above) with `scripts/poll-augment-review.sh` (interval ≥30s, timeout default 600s); each JSON line passes the snapshot gate before any FSM outcome; incomplete evidence keeps polling. Arm exactly once at L1+ (T-109); never at L0 (T-110). `--monitor 0` remains no-monitor.
- **Wave 2:** load `refs/severity-routing.md`; use only the snapshot gate's `actionable_finding_comments` → `finding_from_comment` → `remap_severity(finding)` → `route(finding)` results from `superclaude.pr_submit`, then map the remapped tier to its troubleshoot route (Medium → `--fix`; High/Critical → `--depth deep --fix`; Low/Nit → report-only). NEVER emit `--depth quick --fix`.
- **Wave 3:** load `refs/finding-verify.md`; spawn the `evidence-validator` agent (read-only) to confirm each finding's cited file:line exists and the defect reproduces. `unverified` → REPORT_ONLY, consuming NO round. Context only, once per cycle before verification: invoke `> Skill sc:impact-protocol` with `--diff origin/<baseRefName> --depth 1 --output-dir <output-dir>/impact/wave3 --caller sc-pr-submit-protocol` and read only `status`, `degraded`, `dependents[].caller`, `dependents[].file` and `unmapped_files` from its `return-contract.yaml`; the dependent names and files are background for the verifier, never a reason to verify, drop or re-tier a finding. Copy its `degraded` tokens into the run-log; `status: blocked|failed` counts as `graph:absent`.
- **Wave 4:** load `refs/troubleshoot-dispatch.md`; for VERIFIED findings only, `> Skill sc:troubleshoot-protocol` for diagnosis. **At L1 (G-edit `ordinal < 2`): PROPOSE "fix these? y/n" and apply NO edits.** At L2+ the skill applies the diagnosed edits ITSELF in the working tree (troubleshoot does NOT auto-apply — `sc:pr-submit` owns edit application in `S3_FIXING`). Before the cycle's first edit, record the operator's pending files (`git status --porcelain=v1 -z --untracked-files=all`: every modified, staged and untracked file, both sides of a rename) as `OPERATOR_PENDING`; the Wave 6 fix commit refuses any of them. Before the cycle's first edit, also run the impact warning of `refs/troubleshoot-dispatch.md` ("Impact warning before a fix").
- **Wave 5:** run the VAL validator (below). **At L2 the ceiling stops here:** after applying the edits in `S3_FIXING` and validating in `S7_VALIDATING`, the FSM HALTs at `S4'_HALT_BEFORE_PUSH` — changes are left in the working tree with NO commit, NO push, NO reply (`S3_FIXING → S7_VALIDATING → S4'_HALT_BEFORE_PUSH`, matching `state-machine.md` §5.2a). Only L3 proceeds to Wave 6.
- **Wave 6 (L3 only):** load `refs/thread-reply.md`. **Fix commit:** when the cycle applied edits (`applied_edits > 0`) and VAL is green, commit all of them as exactly one commit (one per cycle, never one per finding; VAL has already passed, so a validation retry never adds a second commit), staging only the files those edits changed (`git add -- <paths>`, never `git add -A` or `git add .`, which would sweep in run artifacts and other untracked files) and committing with `git commit --only -- <paths>` so nothing else already in the index is committed, and set `target_sha := git rev-parse HEAD`; every thread replied to in this cycle cites that one SHA. Before staging anything (before the `git add` above), if a path to commit is in `OPERATOR_PENDING`, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing committed or pushed, and tell the operator: "The fix touched files that had your own uncommitted changes: <paths>. Nothing was committed or pushed. Those files now hold both your changes and the fix: separate them by hand (do not discard the files), then re-run with `--pr <N>`." Otherwise, if the commit fails (for example a pre-commit hook rejects it) or HEAD did not advance, append `terminal_halted` (reason `fix_commit_failed`), HALT with nothing pushed, and tell the operator: "The fix commit failed (<error>). Nothing was pushed; the edits, and any changes a hook made, are in your working tree. Fix the cause, then either commit and push the fix yourself or discard it, and re-run with `--pr <N>`." A halted cycle replies to and resolves no thread. A crash re-drive (Branch B) skips this step and pushes the record's `target_sha`. **Pre-push head guard, before `push_decision`:** re-read `gh pr view <N> --repo "$REPO" --json headRefName,headRefOid,isCrossRepository` and require `pr_head_ok(<local branch>, pre_push_sha, headRefName, headRefOid, isCrossRepository)` and `headRefName == HEAD_BRANCH`. Compare the stored `pre_push_sha`, never local HEAD (local HEAD is the new fix commit). False → append `terminal_halted` (reason `pr_head_mismatch`), HALT with nothing pushed, write no push record, and tell the operator: "PR #<N>'s head moved from <pre_push_sha> to <headRefOid> (or its branch is no longer `<HEAD_BRANCH>`) during the run. Nothing was pushed. Review the new PR commits, make your checkout equal the new PR head, then re-run with `--pr <N>`." When this cycle made a fix commit, the message adds: "This cycle's fixes are in local commit <target_sha>: drop it, or rebase it onto the new head and push it yourself." Next, when the cycle applied edits (a zero-edit cycle has no fix commit; INV-016 predicate 5 blocks its push and still records `push_decision`), read the parents of the commit to push (`git rev-list --parents -n 1 <target_sha>`, dropping the first id) and require `superclaude.pr_submit.fsm.push_parent_ok(<parents>, pre_push_sha)`: a fast-forward push publishes every commit between the PR head and `target_sha`, so the push may carry only this cycle's fix commit. False → append `terminal_halted` (reason `push_range_mismatch`), HALT with nothing pushed and no push record, and tell the operator: "Nothing was pushed. The fix commit <target_sha> sits on top of local commits that are not on PR #<N>: <`git log --oneline <pre_push_sha>..<target_sha>^`>. Publish those commits yourself if you want them on the PR, otherwise drop them; make your checkout equal the PR head, then re-run with `--pr <N>` (the open review threads are fixed again)." Then set `target_branch := HEAD_BRANCH`. The deterministic core DECIDES (evaluates the INV-016 conjunction, records the write-ahead push triad `push_decision` → `push_initiated` (fsynced BEFORE the push) → `push_completed`, keyed on the PRE-push idempotency key `push:<run_id>:<cycle_id>:<pre_push_sha>:<target_branch>`); the SKILL performs the actual `git push origin <target_sha>:<target_branch>` (never an upstream parent remote, never the repo's default/protected branch, never a force push) ONLY when the conjunction holds, then set `pre_push_sha := target_sha`, then reply (citing `applied_edits` status — `applied_edits==0` says "no code change applied", never "resolved") and resolve via `scripts/reply-resolve-thread.sh` (reply FIRST, then resolve). **S5a re-trigger (FR-8):** load `refs/review-retrigger.md`; a push does NOT auto-trigger an Augment re-review — AFTER resolve, and ONLY when this cycle applied edits (`applied_edits > 0`), post the re-trigger comment via `scripts/retrigger-review.sh --pr <N>` BEFORE re-entering the S5 poll. The core decides whether/when to re-trigger (`do_retrigger` seam, INV-R1: at most once per push cycle, `rereview_request_count <= max_rounds`); the script does the `gh api` issue-comment POST (NFR-6). On posting the re-trigger, append a **`rereview_requested{cycle_id}`** run-log event (the INV-R1 producer — folded into `rereview_request_count` by `rebuild_state`, and consumed by crash recovery's OQ-1 resume decision: a landed-push crash with NO `rereview_requested` for its cycle resumes at `S5a_RETRIGGER_REVIEW` to re-post; one WITH it resumes at `S5_AWAITING_REREVIEW`). The `round_counter` ticks only when the subsequent poll attributes the re-review to our pushed SHA (the relocated INV-001 increment) — a timed-out re-trigger does NOT advance the counter.
- **Wave 6b (L2+ decline fallback, FR-9/FR-10):** load `refs/auggie-fallback.md`. When the classifier returns `declined` (an Augment "abnormally large" decline observed at the initial S2 poll OR the S5 re-trigger poll), append a **`decline_detected`** run-log event, then engage the single-shot fallback: gate **strict-once** on the durable `auggie_review_invoked` idempotency record (comment-independent, survives resume — INV-R2; on engage, append an **`auggie_fallback_invoked{pr_number}`** event, the producer folded into that set), clamp the effective budget `effective_max_rounds := min(effective_max_rounds, 1)` (the `clamp_max_rounds` helper, recorded once via the **`max_rounds_clamped{effective_max_rounds}`** event — INV-R3 monotone-min fold), then invoke `> Skill sc:auggie-review-protocol --depth quick --remediation-offer` and re-enter Waves 2-6 ONCE under the clamp (verify-before-remediate still applies — fallback findings are NOT trusted verbatim, FR-9.4). At L2 this can apply and validate local fixes but still halts before push/reply per Wave 5; only L3 performs push, reply, resolve, and re-trigger side effects. NO second invoke, NO second re-trigger, NO loop-back; `push_count <= max_rounds + 1` for the whole run. This is `sc:pr-submit` invoking its OWN review — do **NOT** "take the App's bait" by treating the App's `augment review` decline comment as our operator re-trigger. (`--depth quick` here targets `/sc:auggie-review` — a review, no `--fix` — so it does NOT conflict with the severity-routing STOP on `--depth quick --fix`.)
- **Wave 7:** load `refs/loop-guard.md`; the round counter ticks only at `S5_AWAITING_REREVIEW → S2_CLASSIFY`; HALT at `round_counter >= max_rounds`. Fallback outcomes REUSE the existing `terminal_clean` / `terminal_max_rounds` status values (OQ-2 reuse recommendation).
- **Wave 8 (L1+, after Augment `clean` / `REPORT_ONLY` / `HALT_MAX_ROUNDS` / `TERMINAL_AUGMENT_NO_RESPONSE`):** load `refs/ci-poll.md`. Arm via `superclaude.pr_submit.ci.should_arm_ci_wait`. Do **not** `transition(clean)` yet. Set SKILL-owned `source=ci`, reset wait elapsed, switch the attended poll loop to `scripts/poll-ci-checks.sh --pr <N> --repo "$REPO"`. Classify via `superclaude.pr_submit.ci.classify_checks(payload, wait_sha=<sha at flip or last push>)`. Human-gate (`is_human_gate`) → `HALT_HUMAN` when Augment has not halted; after Augment `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, keep its terminal status and report the CI human-gate alongside it. No Finding or auto-fix on those wait-only paths (`ci_wait_autofix` is false). If `round_counter >= max_rounds`, CI polling is wait-only: non-human `findings` → `REPORT_ONLY` without fetching logs, editing, or pushing. Otherwise non-human `findings` → `gh run view <id> --repo "$REPO" --log-failed` once → `findings_from_logs`; empty → `REPORT_ONLY`; else Waves 3–5 under the same ordinals and `round_counter`. An L3 CI push runs the Wave 6 pre-push head guard and push triad with `target_branch := HEAD_BRANCH`, then sets `pre_push_sha := target_sha`. It also makes the Wave 6 single fix commit and runs the guard's parent check (`push_parent_ok`), so this push too carries only the cycle's one fix commit. After an L3 CI push: do **not** call `retrigger-review.sh`, reply, or resolve; re-poll CI on the new `headRefOid`. When CI is `clean` after an ordinary Augment `clean` / `REPORT_ONLY`, send `transition(clean)` → `TERMINAL_CLEAN`. After `HALT_MAX_ROUNDS` or `TERMINAL_AUGMENT_NO_RESPONSE`, leave that terminal FSM status unchanged and report CI clean alongside it (no `transition(clean)` from a terminal state — never claim `TERMINAL_CLEAN` for a silent Augment review). L0 never reaches Wave 8. Do not arm on `HALT_HUMAN` / `VALIDATION_FAIL` / `TERMINAL_TIMEOUT` / `TERMINAL_FAILED`. CI `polling` continues at the configured interval until completion or timeout; when the chosen list is empty, a failed check query is `polling`, not no-Actions `clean`. Only parsed empty required **and** all-checks lists prove there are no Actions. A nonempty required list is the chosen set; optional pending checks outside it do not block completion.

## VAL — the §10 validation gate list (owned by the SKILL, not the core)

Run IN ORDER, all green ⇒ `validation_status == "validated"` (the INV-016 predicate 2). Any
non-zero gate blocks the push:

1. **VG-1** targeted tests (`uv run pytest <changed-area>`). Advisory only: before running them, invoke `> Skill sc:impact-protocol` with `--diff origin/<baseRefName> --tests --output-dir <output-dir>/impact/vg1 --caller sc-pr-submit-protocol`, read only `status`, `degraded`, `tests[]` and `selection_source`, copy its `degraded` tokens into the run-log, and print the `tests[]` paths that fall outside `<changed-area>` as a suggestion for the operator. The VG-1 gate itself is unchanged: it still runs exactly `<changed-area>`, and `status: blocked|failed` counts as `graph:absent`.
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
- After Augment clean, report-only, or round-cap halt, wait on PR checks; remediate parseable CI failures only with remaining round budget.

## Will Not Do

- Run headless / detached, or imply a background daemon (V1 limitation).
- Push to an upstream parent remote or to the repo's default/protected branch; open a PR against an upstream parent the CLI might default to.
- Force-push (`--force`, `--force-with-lease`, or a `+` refspec): git rejecting a push that is not a fast-forward is the backstop if the PR head moves after the pre-push head guard runs, and the guard's parent check (`push_parent_ok`) stops a fast-forward that would also carry commits other than the fix.
- Require a local lock file or R1 probe before arming.
- Emit `--depth quick --fix` to troubleshoot (a STOP conflict).
- Apply any edit at L1, or push/reply at L2.
- `git add` any `.claude/` path except `.claude/settings.json`.

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Wrong origin / behind base branch (create path) / wrong-owner URL | HALT; instruct operator to close the misrouted PR (FM-11). |
| Checkout is not the PR head (Wave 0 head binding) or the PR head moved before a push (pre-push head guard) | `terminal_halted`, reason `pr_head_mismatch`; nothing pushed; do NOT close the PR; give the recovery steps from the HALT message. |
| The commit to push is not exactly one commit on top of the PR head (the pre-push head guard's parent check) | `terminal_halted`, reason `push_range_mismatch`; nothing pushed; do NOT close the PR; list the other local commits and tell the operator to make the checkout equal the PR head, then re-run with `--pr <N>`. |
| The fix touched a file with the operator's own pending changes, the fix commit fails, or HEAD does not advance (Wave 6 fix commit) | `terminal_halted`, reason `fix_commit_failed`; nothing pushed; do NOT close the PR; edits (and any hook changes) left in the working tree; never tell the operator to discard a file that holds their own changes; give the recovery steps from the HALT message. |
| Augment silent (no attributed review/comment) | `terminal_augment_no_response`; Wave 8 wait-only; check App trigger mode, Allowlist, quota; comment `augment review` by hand. |
| Review starts but never completes | `terminal_timeout`; no Wave 8; no edits/push. |
| 403 / 429 / secondary-limit | exponential backoff 30→…→cap 300s, counts toward timeout. |
| `needs_human_decision` finding | `terminal_halted`; no auto-mutation (override, FR-4.4). |
| Validation failure | no push/reply/resolve; L2 halt; L3 one retry within budget. |
| Crash mid-push | `--resume` 3-way recovery (§12); no double push, no re-fix. |

<!--mc:threads:begin-->
<!--mc:rev {"ts":"2026-09-25T00:10:25.720Z","contentHash":"66e62fbc","sections":[{"heading":null,"hash":"5b01b10f"},{"heading":"sc:pr-submit — PR Review Auto-Remediation Monitor","hash":"35902d16"},{"heading":"Purpose","hash":"649cb71c"},{"heading":"Required Input (STOP if missing)","hash":"dbb7e7e3"},{"heading":"Output Contract","hash":"44b5105b"},{"heading":"Wave / Phase Structure (refs are LAZY-loaded per wave, never pre-loaded)","hash":"73e1ae37"},{"heading":"VAL — the §10 validation gate list (owned by the SKILL, not the core)","hash":"ebeaedc8"},{"heading":"Will Do","hash":"dafae003"},{"heading":"Will Not Do","hash":"d17c1a2f"},{"heading":"Error Handling","hash":"679a0343"}]}-->
<!--mc:threads:end-->
