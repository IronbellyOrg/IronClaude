# Review Re-trigger (RT) — the post-push re-trigger surface, per reviewer (R1 / FR-8)

This ref documents the **S5a re-trigger**: a push does **NOT** auto-trigger a re-review by either bot.
The `augmentcode[bot]` reviews only on PR-open or an explicit `augment review` / `auggie review` /
`augmentcode review` operator comment; Codex (`chatgpt-codex-connector[bot]`) reviews on PR-open or an
explicit `@codex review` comment. After each remediation push the skill must **post one re-trigger
comment per present reviewer** and then poll for the attributed re-review.

> **NOTE (core-purity boundary, NFR-6 / T-104, NOT T-N50).** This ref documents a `gh api …
> repos/<owner/repo>/issues/<N>/comments` POST surface, so it CARRIES a `gh` token **by
> design** — exactly like `thread-reply.md` and `augment-poll.md`. It is therefore covered by the
> **T-104 repo-pin** test path and is DELIBERATELY EXCLUDED from the zero-token `CORE_PURE_FILES`
> (T-N50) set. The decision *whether/when* to re-trigger lives in the deterministic core (`do_retrigger`
> seam); the `gh api` I/O lives in `scripts/retrigger-review.sh`.

## 1. Purpose

Drive each present reviewer (the Augment App, Codex) to perform a re-review of the just-pushed
remediation commit, so the monitor loop can actually advance (the V1.0 loop assumed pushes
auto-triggered reviews — they do not).

## 2. Surface (fork-pinned issue-comment POST)

The re-trigger is one pinned issue-comment POST, mirroring `thread-reply.md`'s single-summary surface:

```bash
gh api --method POST repos/<owner/repo>/issues/<N>/comments -f body="auggie review"
```

- **Repo-pin:** the path names the RESOLVED `repos/<owner/repo>/...` (origin's `owner/repo`) — a bare
  `gh api .../comments` or an upstream-parent path is a **T-104-class defect**. `gh api` takes no
  `--repo`; the repo is the path segment.
- **Body token (S5a), per reviewer:** `retrigger_phrase(contract, reviewer)` gives the body. Augment:
  default `auggie review` (one of the contract's `accepted_trigger_phrases`, unchanged). Codex:
  `codex_retrigger_phrase`, shipped as `@codex review` (`--body "@codex review"`), the trigger
  documented by OpenAI and by the bot's own summary text. **UNVERIFIED:** whether a Codex re-review
  after `@codex review` updates the same summary comment's `codex-review-state:v1` marker with the new
  `commit_sha` has not been observed in this repository (only PR-open reviews were). If it does not,
  the Codex re-review wait ends `incomplete` at `--timeout` and the other re-triggered reviewer's
  attributed result is used when there is one (fail open), so the gap cannot hang the loop.
- **One post per present reviewer, write-ahead checked.** At S5a, post only for the reviewers in
  `pending_retriggers(<run-log events>, cycle_id, <present reviewers>)`: present reviewers with no
  `rereview_requested` for this `cycle_id` yet (an event without `reviewer` counts as Augment). Absent
  reviewers are never re-triggered.
- **Silence poke (not S5a):** after `--silence-timeout` with no Augment activity, L3 may POST once
  with `--body "augment review"` only via INV-S1 write-ahead: `check_idempotent("silence_rerequest_invoked")`
  then append `silence_rerequested{pr_number, elapsed}` then POST. Not INV-R1; does not increment
  `rereview_request_count` or `round_counter`. `S5C_SILENCE_REREQUEST` is consider-once, not POST-now.
  Never treat an Augment decline comment as this POST (unreachable: decline is activity). The silence
  poke is Augment-only; Codex is never poked.
- The actual POST is performed by `scripts/retrigger-review.sh --pr <N> [--body <phrase>]` (the script wraps this in the
  shared `set -euo pipefail` / `die()` / arg-guard / `command -v gh` shape with a SoT footer).

## 3. Watermark / attribution

Retain the exact full pushed SHA and a trustworthy aware UTC **watermark** at the confirmed re-trigger.
The current script prints an acknowledgement and discards the POST response; it does **not** export
`createdAt`. Record UTC immediately after successful return as a conservative boundary, or use the
confirmed trigger comment's REST `created_at` if independently retrieved and uniquely identified.
Unknown/invalid freshness remains polling, never an optimistic attribution.

**One watermark per reviewer.** Each re-triggered reviewer gets its own watermark: the UTC time taken
right after **its own** successful POST, recorded on its `rereview_requested{cycle_id, reviewer,
timestamp}` event (`timestamp` = that watermark). It is used only for that reviewer's completion
attribution (Augment's `watermark`, Codex's `codex_watermark` in the SKILL snapshot gate). On
`--resume`, a reviewer's watermark is the `timestamp` of its latest `rereview_requested` for the cycle,
and the resume reuses the `cycle_id` of the dangling push record (never a new one). Every resume at
`S5a_RETRIGGER_REVIEW` or `S5_AWAITING_REREVIEW` of a re-triggered cycle first calls
`pending_retriggers` and posts the reviewers still missing, so a crash between the Augment and the
Codex post neither skips Codex nor re-posts Augment.

Before supplying the pushed SHA as an explicit classifier override, require
`payload.head_sha == pushed_sha`. The adapter detects pushes *during* collection, but a complete later
snapshot can already describe another push; the public `current_head_sha` argument overrides the
snapshot head rather than checking it. A mismatch must not produce clean, a round tick or remediation.

Use `classify(payload, contract, watermark=watermark, current_head_sha=pushed_sha)` then, for findings,
`actionable_finding_comments` with that **same snapshot, watermark and head**, then `finding_from_comment`
for every selected root (SKILL snapshot gate). Only gated `clean` / successfully normalized `findings`
can supply the existing `rereview_attributed` FSM edge or the explicit `RunConfig.rereview_outcome`
`"attributed"` token. Never use the empty sequence's optimistic legacy default as live evidence.
Codex uses the same rules on the same snapshot and pushed head with its own watermark:
`classify_codex(payload, contract, watermark=codex_watermark, current_head_sha=pushed_sha)` then, for
findings, `codex_finding_comments` with the same arguments. The S5 wait covers only the reviewers
re-triggered in this cycle; the re-review is attributed when at least one of them reaches a gated
`clean` / `findings` on the pushed SHA and Augment has not declined (an Augment `declined` routes to
S5b instead, even when Codex is done). A re-triggered reviewer still not done at expiry while the
other reviewer's result is used is recorded `reviewer_incomplete{reviewer, phase: "rereview"}`.

Completion requires reviewed SHA/marker head/expected head agreement and submission **strictly newer**
than the watermark, no later than the snapshot's `observed_at`. Before/equal watermark, wrong-head,
invalid metadata, partial flags, empty legacy finding selection or normalization `ValueError` remains
polling under the existing finite timeout (no elapsed reset). Expiry supplies `"timeout"`; `declined`
uses the existing fallback, not an attribution tick. The watermark dates **completion only**, never
filters older unresolved root findings; outdated roots still need independent evidence validation.

## 4. INV-R1 (re-trigger boundedness, normative)

> A re-trigger comment is emitted at most once per completed push cycle **per present reviewer**, on
> the `RESOLVING → S5a_RETRIGGER_REVIEW` edge, and only when `applied_edits > 0`.
> `rereview_request_count` counts re-triggered push cycles (folded by distinct `cycle_id`, so the
> Augment and Codex comments of one cycle count once), is monotonic and
> `rereview_request_count <= max_rounds`. The re-trigger does **not** itself increment
> `round_counter`; INV-001's edge and gate are unchanged.

The `round_counter` ticks ONLY when the subsequent poll attributes the re-review to our pushed SHA (the
relocated INV-001 increment at `S5_AWAITING_REREVIEW → S2_CLASSIFY`), once per cycle however many
reviewers were re-triggered. A timed-out re-trigger (no re-triggered reviewer's re-review attributed
within the wall-clock timeout) does NOT advance `round_counter` — it terminates
`terminal_timeout`. A `declined` response routes to the S5b auggie fallback (`auggie-fallback.md`).
