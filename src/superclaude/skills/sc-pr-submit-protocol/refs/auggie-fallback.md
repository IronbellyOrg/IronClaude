# Auggie Fallback (AF) — the oversized-PR `/sc:auggie-review` fallback (R2/R3 / FR-9/FR-10)

This ref documents the **S5b decline fallback**: when the Augment App posts an "abnormally large"
decline (it refuses to auto-review the PR and asks you to comment a trigger phrase), `sc:pr-submit`
falls back to invoking its **OWN** `/sc:auggie-review` — a single in-session review under a clamped
budget — rather than looping forever waiting for a review the App will not produce.

> **NOTE (core-purity, NFR-6 / T-N50).** This ref carries ZERO shell or version-control command tokens —
> it documents the `> Skill sc:auggie-review-protocol` invocation and a flag table, NOT any API call. It
> IS therefore part of the zero-token `CORE_PURE_FILES` set. (The re-trigger surface that *does* carry a
> shell token lives separately in `review-retrigger.md` + `scripts/retrigger-review.sh`.)

## 1. Decline detection (the trigger)

A `declined` classification (`augment-poll.md`, FR-9.1) fires when an Augment-authored comment matches
BOTH probe-locked decline regexes — `decline_phrase_regex` ("abnormally large") AND
`decline_retrigger_regex` ("comment augment/auggie/augmentcode review", quote- or backtick-wrapped) —
and is newer than the watermark (a stale pre-watermark decline is ignored, EC-23). A decline can be
observed at the initial S2 poll OR the S5 re-trigger poll; both route to S5b.

**Do NOT take the App's bait.** The App's `augment review` decline comment is the App DECLINING to
auto-review — it is NOT our operator re-trigger. The fallback is `sc:pr-submit` invoking its OWN
`/sc:auggie-review`, distinct from honoring the App's comment.

## 2. The fallback invocation (byte-exact flag string)

```text
> Skill sc:auggie-review-protocol <PR-target> --depth quick --post-pr --no-remediation-offer --auggie-model claude-sonnet-4-6
```

| Flag | Value | Why |
|------|-------|-----|
| `<PR-target>` | the active PR number or URL | forces PR-targeted review; this is not a bare diff fallback. |
| `--depth quick` | quick | a single-pass review (this goes to `/sc:auggie-review`, a **review** — there is NO `--fix`, so it does NOT conflict with the severity-routing / troubleshoot-dispatch STOP on `--depth quick --fix`). |
| `--post-pr` | explicit | the fallback review output must be posted to the PR and its URL/comment id recorded when available. |
| `--no-remediation-offer` | explicit | suppresses `/sc:auggie-review`'s advisory remediation offer; `sc:pr-submit` owns remediation under its clamp. |
| `--auggie-model claude-sonnet-4-6` | claude-sonnet-4-6 | the reviewing model. |

## 3. Strict-once + clamp + single-shot (the invariants)

- **Strict-once (INV-R2):** the invocation is gated on the durable `auggie_review_invoked` idempotency
  set (keyed on `pr_number`, comment-independent, survives resume) — `/sc:auggie-review` is invoked
  **at most once per PR**. The fallback contributes at most one push, so `push_count <= max_rounds + 1`
  for the whole run.
- **Clamp (INV-R3):** on engage, `effective_max_rounds := min(effective_max_rounds, 1)` — a one-way,
  monotone non-increasing clamp recorded once via the `max_rounds_clamped` event.
- **Single-shot:** the fallback re-enters the V0.1 pipeline (classify → re-grade → verify-before-remediate
  → route → fix → validate → push) **ONCE** under the clamp, advancing only `fallback_round_counter`
  (cap 1). `round_counter` is FROZEN at fallback entry — the two counters are independent. There is NO
  loop-back, NO second `/sc:auggie-review` invoke, NO second re-trigger.

## 4. Re-entry contract (FR-9.4)

The fallback findings are **NOT trusted verbatim** — the posted fallback output is normalized into
`fallback_findings`, then those findings re-enter verify-before-remediate (the `evidence-validator`
content gate) before any edit, exactly like an Augment finding set. An all-unverified fallback set
converges clean with no push. `/sc:auggie-review` does not push fixes and does not reply to Augment
threads; `sc:pr-submit` owns the one clamped remediation cycle and any PR follow-up comment.

## 5. Terminal (OQ-2 reuse)

The single-shot fallback REUSES the existing terminals: `terminal_clean` when the residual is clean,
`terminal_max_rounds` when residual findings remain after the one clamped cycle. No new status enum is
added (the spec's OQ-2 reuse recommendation).
