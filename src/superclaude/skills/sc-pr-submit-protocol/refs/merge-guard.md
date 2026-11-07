# Merge Guard (MG) — hold the PR as a draft while a fix cycle runs (issue #375)

This ref is the protocol for the **merge guard**. At `--monitor 3` a PR that is green but is
about to be remediated is turned into a draft as soon as a verified finding of Medium severity or
higher is routed to a fix, and is marked ready again only when that cycle's fix push is confirmed on
the PR head (or a zero-edit cycle is proven). Every failure, override, crash, resume and exit path
leaves the PR in a known, reported state.

> **NOTE (split of duties, NFR-6).** The deterministic core **DECIDES** and this skill **PERFORMS**,
> the same split as the push triad and the re-trigger. The decisions are the functions of
> `superclaude.pr_submit.merge_guard` (`engage_decision`, `release_decision`, `resume_decision`,
> `classify_toggles`, `guard_status`, `fix_cycle_id`, `next_cycle_number`, `pending_requests`,
> `held_cycle_published`); the folded state is `rebuild_state()["draft_guard"]` of the run log. All
> GitHub I/O is `scripts/set-draft-state.sh`. The guard phases (`engage_pending`, `held`,
> `release_pending`, `released`, `disabled`) are fold values, not `MonitorState` members.

## 1. The five steps of every mutation

Every draft or ready change runs the same five steps, in order:

1. **Read** with the script (live state, head, timeline count).
2. **Decide** with the core function for the moment (Engage, Release or Resume).
3. **Request**: append `draft_guard_requested` to the run log (the append is fsynced) **before** the call.
4. **Mutate** with the script.
5. **Settle**: append `draft_guard_settled` with the outcome.

The script is the only place that talks to GitHub:

```bash
scripts/set-draft-state.sh --pr <N> --repo "$REPO" --read
scripts/set-draft-state.sh --pr <N> --repo "$REPO" --to draft
scripts/set-draft-state.sh --pr <N> --repo "$REPO" --to ready
```

Each call prints one JSON line. `--read` gives `ok`, `state`, `isDraft`, `headRefOid`,
`autoMergeRequest`, `transitions` and `complete`; `--to` gives `ok`, `state`, `isDraft`, `headRefOid`,
`changed` and `error` (`not_open`, `read_failed`, `mutation_failed` or `verify_failed`). It is
idempotent: a PR already in the target state answers `changed: false`, so a retry or a resume re-issue
is safe. Build the `GuardRead` of the core from the `--read` line.

| Event | Fields |
|---|---|
| `draft_guard_requested` | `run_id`, `cycle_id`, `to` (`draft` or `ready`), `idempotency_key`, `timestamp`; the first request of the run also carries `timeline_baseline` (the `transitions` of the read) and `original_is_draft` (the `isDraft` of the read) |
| `draft_guard_settled` | `run_id`, `cycle_id`, `to`, `idempotency_key`, `outcome` (`confirmed`, `failed` or `skipped`), `changed`, `cause`; a skip that has no request also carries `original_is_draft` |

The `idempotency_key` is `guard:<run_id>:<cycle_id>:<to>:a<k>`, where `k` is 1 plus the number of
earlier requests with the same cycle and direction, so a retry is its own request.

## 2. Engage (end of Wave 3, L3 with `--merge-guard draft`)

**Trigger.** Engage runs once per cycle id, at the end of Wave 3, only when at least one verified
finding of Medium severity or higher is routed to a fix: the Medium-or-higher routed-finding trigger.
It applies to a review-fix cycle and to a CI-fix cycle (Wave 8). It never runs for a conflict-merge
cycle (`sync-` and `conflict-` ids) and never below ordinal 3 or with `--merge-guard off`; the core
returns `NOOP` for those, with reason `ordinal`, `mode_off` or `conflict_cycle`.

**Cycle id (the single place it is minted).** This section is the one place where the
guard-enabled cycle id is minted: call `fix_cycle_id(kind, next_cycle_number(<run-log events>, kind))`
once, with kind `fix` for a review-fix cycle and kind `ci` for a CI-fix cycle (ids `fix-<n>` and
`ci-<n>`). Use that id unchanged as the `cycle_id` of `push_decision`, `push_initiated` and
`push_completed`, and of `rereview_requested`, so the guard, the push and the re-trigger of one cycle
share one key. With `--merge-guard off` nothing is minted here and the existing behaviour stands.

**Steps.** Read, then decide with
`engage_decision(mode=..., ordinal=..., cycle_id=..., guard=..., read=...)` (the three decision
functions take keyword arguments only) where `guard` is the folded state. Act on the answer:

| Action | What to do |
|---|---|
| `ENGAGE` | Request `draft` (with `timeline_baseline` and `original_is_draft` on the first request of the run), run `--to draft`, settle `confirmed` (`changed` as printed). The phase is now `held`. Print the clear command once. When the decision notes carry `auto_merge_armed`, add that auto-merge is armed to the report. |
| `SKIP_ALREADY_DRAFT` | The PR was a draft before this run: settle `skipped` with cause `already_draft` (carrying `original_is_draft: true`), never mutate, and keep going. The phase is `disabled` and the report says `off`. |
| `SKIP_USER_OVERRIDE` | Settle `skipped` with cause `user_override`; no more draft calls this run; keep going and report `user_override`. |
| `RETRY_RELEASE` | A release is still pending and the draft is owned: run the Release steps first, then decide again. |
| `HOLD` | Ownership is unproven: do not mutate, keep going and report `unavailable`. |
| `HALT_PR_NOT_OPEN` | Halt `terminal_halted` with reason `pr_not_open`; push nothing. |
| `HALT_UNAVAILABLE` | Halt before any edit: see below. |
| `NOOP` | Nothing to do (already held, disabled or inert). |

**Engage failure.** An engage failure, and an unreadable timeline at engage (reason `read_failed` or
`timeline_unreadable`), halt with `terminal_halted` reason `draft_guard_unavailable` before any edit.
A failed `--to draft` is settled `failed` first. The message names `--merge-guard off` as the way to
run without the guard and prints the clear command. No retry is made at engage.

**The clear command.** Print it once, when the engage settles `confirmed`, and again in every held
report (section 6), with `<N>` and `"$REPO"` filled in:

```bash
gh pr ready <N> --repo "$REPO"
```

## 3. Pre-push (Wave 6, at the pre-push head guard step, before `push_decision`)

Read with the script. The PR must show `OPEN`; otherwise halt `terminal_halted` with reason
`pr_not_open`, push nothing, and report the local commit `<target_sha>` that holds the fixes. This
read applies whatever the guard phase is, including `disabled`, and at every ordinal that reaches the
push. It comes in addition to the head check of the pre-push head guard, never in place of it.

## 4. Release (after `push_completed`, before reply, resolve and the S5a re-trigger)

Release runs after `push_completed` (Wave 6, or Wave 8 for a CI-fix cycle, before the CI re-poll) and
**before** any reply, resolve or re-trigger, so reviewers see a ready PR. Read, then decide with
`release_decision(mode=..., ordinal=..., cycle_id=..., guard=..., read=..., applied_edits=..., target_sha=..., push_completed=...)`.
`applied_edits` is this cycle's count of applied edits, not the run-wide field, so a zero-edit cycle
after a fixing cycle still releases with cause `no_edits`.

| Action | What to do |
|---|---|
| `RELEASE` | Request `ready`, run `--to ready`, settle `confirmed` with the decision's cause: `pushed` (head equals `target_sha` after `push_completed`) or `no_edits` (the cycle applied no edit, so there is nothing to publish). |
| `HOLD` | Keep the PR draft and report `held` with the reason (`head_mismatch`, `push_not_completed`, `read_failed` or `timeline_unreadable`) and the clear command; keep going. |
| `SKIP_USER_OVERRIDE` | Settle `skipped` with cause `user_override`; keep pushing and replying; report `user_override`. |
| `HALT_PR_NOT_OPEN` | Halt `terminal_halted` with reason `pr_not_open`; report the local commit. |
| `NOOP` | Nothing is held (or the guard is inert): continue. |

**Release failure.** Retry once: a failed `--to ready` is settled `failed`, then requested again with
the next `:a<k>` key. An answer of `changed: false` (already in the target state) counts as confirmed.
A second failure is settled `failed`, the phase stays `release_pending`, the run keeps going and the
report says `held (release pending)` with the clear command.

## 5. Foreign toggle and unreadable timeline

One login serves the person and the agent, so no actor is used. `classify_toggles(guard, read)` compares
the draft and ready transitions on the PR timeline with the count the guard made itself (plus slack for
calls that failed or were never settled) and returns `ok`, `foreign` or `unreadable`.

- **Foreign** (someone else changed the draft state): settle `skipped` with cause `user_override`, make
  no more draft calls this run, keep pushing, and report `user_override`.
- **Unreadable** (the timeline call failed, the list is incomplete, or events are missing from it): at
  engage only a failed or incomplete read halts (reasons `read_failed` and `timeline_unreadable`,
  section 2); events missing from a complete read are not a halt at engage, and the guard goes on to
  engage. At a later checkpoint do not release, report `held (timeline unreadable)` with the clear
  command, and keep pushing.

## 6. Exit report

The output field `merge_guard` is `guard_status(guard, mode, ordinal)`:

| Value | Meaning |
|---|---|
| `off` | The guard did not act: ordinal below 3, `--merge-guard off`, or the PR was already a draft. |
| `released` | The guard acted and the PR is ready again (or the guard never had to act). |
| `held` | The PR is a draft held by this run. Report the reason and the clear command. |
| `user_override` | Someone else changed the draft state; the guard stood down. |
| `unavailable` | The guard could not act or prove ownership (engage failure, ownership unproven). |

A halt with `terminal_halted` reason `draft_guard_unavailable` reports `unavailable` whatever
`guard_status` returns: when the engage read failed no request exists, so the folded state is empty
and `guard_status` alone would say `released`.

Every exit after engage that has no confirmed push and no zero-edit proof leaves the PR draft and
reports `held`, with the reason and the clear command. That covers a validation failure after engage,
a halt before the push, a rejected or failed push, a push whose landing is uncertain, a release that
could not be confirmed, an unreadable timeline and a merged or closed PR. Exits with unpublished or
uncertain work never release the PR.

For a fresh `--monitor 2` run that applies fixes and halts before the push, the final report also
carries the L2 line. Its literal text lives in the output table of `SKILL.md`, which every run loads;
this ref holds no second copy of it.

## 7. Resume (loaded from Wave 0 at every ordinal and in both modes)

Wave 0 loads this section on `--resume` and whenever the run log already holds guard events. It also
runs on `--resume` below ordinal 3 and with `--merge-guard off`, because a held guard from an earlier
run must be reported before any edit, release or re-trigger. At those settings row 2 below answers
first, so an unsettled request is not reconciled there: it stays unsettled, the report says `held`, and
the next `--resume` at ordinal 3 with the guard on reconciles it (row 3).

Gather the inputs, then decide with
`resume_decision(mode=..., ordinal=..., guard=..., read=..., pending=..., dangling_branch=..., published=...)`:

- `guard`: the folded `draft_guard` state.
- `pending`: `pending_requests(<run-log events>)`, the guard requests with no settle.
- `dangling_branch`: the result of crash recovery for a dangling push: `None`, or one of the strings
  `landed`, `not_landed` or `ambiguous`.
- `published`: `held_cycle_published(<run-log events>, guard)`, true when the held cycle's
  `push_completed` is in the log, written normally or synthesized by recovery. It is the only way
  resume learns that a push completed normally before the crash.
- `read`: a live read with the script, or none when it failed.
- Also pass the held cycle's `target_sha` (from its push record) and this cycle's `applied_edits` as
  the keyword arguments of the same names: row 4 re-enters `release_decision` and needs the head proof.

| Row | Action | What to do |
|---|---|---|
| 1 | `NOOP` | No guard record: nothing to do. |
| 2 | `REPORT_HELD` | Ordinal below 3 or `--merge-guard off`, and the phase is not `released` or `disabled`: no mutation, and an unsettled request is left as it is; report `held` with the clear command. |
| 3 | `RECONCILE` | An unsettled request exists. Reason `resume_reconciled`: the live state matches the request and the transition count is the run's plus one, so settle `confirmed` with `changed: true` and cause `resume_reconciled`. Reason `not_applied`: the live state does not match, so settle `skipped` with cause `not_applied`; the phase returns to the one before the request and the next cycle engages normally. Reason `ambiguous`: anything else; hold, report, no mutation. |
| 4 | release | Phase `held` and the push landed (`landed`) or `published` is true: re-enter the Release steps (section 4) with `push_completed` true, then run the S5a logic of `refs/review-retrigger.md`. |
| 5 | `NOOP` | `not_landed` while held: the re-driven push will run, so keep the PR draft (`held_through_redrive`). |
| 6 | `HOLD` | `ambiguous`: the remote tip is unknown, so hold (`ambiguous_remote_tip`). |
| 7 | `RETRY_RELEASE` | A release is pending and the draft is owned: run the Release steps. |
| 8 | `HOLD` | A release is pending, ownership is not proven and the PR is a live draft: hold (`ownership_unproven`). |
| 9 | `NOOP` | Nothing to do. |

At ordinal 3 with the guard on, unsettled requests are reconciled first (row 3), so no edit, release or
re-trigger runs on an unknown state. After resume the usual Engage, Pre-push, Release and Exit report steps apply to the cycles that
follow.
