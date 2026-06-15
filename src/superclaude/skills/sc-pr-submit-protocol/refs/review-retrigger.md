# Review Re-trigger (RT) — the post-push `auggie review` re-trigger surface (R1 / FR-8)

This ref documents the **S5a re-trigger**: a push does **NOT** auto-trigger an Augment re-review (the
`augmentcode[bot]` reviews only on PR-open or an explicit `augment review` / `auggie review` /
`augmentcode review` operator comment — pushes do not auto-trigger). After each remediation push the
skill must **post a re-trigger comment** and then poll for the attributed re-review.

> **NOTE (core-purity boundary, NFR-6 / T-104, NOT T-N50).** This ref documents a `gh api …
> repos/IronbellyOrg/IronClaude/issues/<N>/comments` POST surface, so it CARRIES a `gh` token **by
> design** — exactly like `thread-reply.md` and `augment-poll.md`. It is therefore covered by the
> **T-104 fork-pin** test path and is DELIBERATELY EXCLUDED from the zero-token `CORE_PURE_FILES`
> (T-N50) set. The decision *whether/when* to re-trigger lives in the deterministic core (`do_retrigger`
> seam); the `gh api` I/O lives in `scripts/retrigger-review.sh`.

## 1. Purpose

Drive the Augment App to perform a re-review of the just-pushed remediation commit, so the monitor
loop can actually advance (the V1.0 loop assumed pushes auto-triggered reviews — they do not).

## 2. Surface (fork-pinned issue-comment POST)

The re-trigger is one pinned issue-comment POST, mirroring `thread-reply.md`'s single-summary surface:

```bash
gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body="auggie review"
```

- **Fork-pin:** the path names `repos/IronbellyOrg/IronClaude/...` (the fork) — a bare `gh api
  .../comments` or an upstream path is a **T-104-class defect**. `gh api` takes no `--repo`; the repo is
  the path segment.
- **Body token:** exactly `auggie review` (one of the contract's `accepted_trigger_phrases`).
- The actual POST is performed by `scripts/retrigger-review.sh --pr <N>` (the script wraps this in the
  shared `set -euo pipefail` / `die()` / arg-guard / `command -v gh` shape with a SoT footer).

## 3. Watermark / attribution

To attribute the SUBSEQUENT re-review to our push (and not a stale earlier review), the skill records a
**watermark** at re-trigger time — the re-trigger comment's `createdAt` and our pushed `headRefOid`.
The S5 poll then attributes a re-review only when it is newer than the watermark AND its reviewed SHA
matches our pushed SHA (`pushed_commit_shas`). A re-review older than the watermark is ignored (the same
staleness guard the decline classifier uses, EC-23).

## 4. INV-R1 (re-trigger boundedness, normative)

> A re-trigger comment is emitted at most once per completed push cycle, on the
> `RESOLVING → S5a_RETRIGGER_REVIEW` edge, and only when `applied_edits > 0`. `rereview_request_count`
> is monotonic and `rereview_request_count <= max_rounds`. The re-trigger does **not** itself increment
> `round_counter`; INV-001's edge and gate are unchanged.

The `round_counter` ticks ONLY when the subsequent poll attributes the re-review to our pushed SHA (the
relocated INV-001 increment at `S5_AWAITING_REREVIEW → S2_CLASSIFY`). A timed-out re-trigger (no
attributed re-review within the wall-clock timeout) does NOT advance `round_counter` — it terminates
`terminal_timeout`. A `declined` response routes to the S5b auggie fallback (`auggie-fallback.md`).
