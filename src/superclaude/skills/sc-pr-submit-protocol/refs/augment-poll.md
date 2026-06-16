# Augment Poll (C2) — the poller contract

This ref pins the poll surface and timing for the in-session Monitor. The poll **script**
(`scripts/poll-augment-review.sh`) performs a single `gh`/`gh api` poll and emits one JSON line; the
**FSM** (`superclaude.pr_submit`) does the backoff arithmetic. This split keeps `gh` out of the
deterministic core (NFR-6) — the script touches `gh`, the core decides.

> Every `gh`/`gh api` call below pins the RESOLVED `--repo <owner/repo>` (origin's `nameWithOwner`,
> FR-1.3 / AC-7). A bare `gh` without `--repo` is a defect (T-104 greps for it).

## Poll surfaces (FR-2.1)

Primary, the exact `--json` field set from the spec:

```bash
gh pr view <N> --repo <owner/repo> --json number,url,headRefName,headRefOid,baseRefName,reviews,comments
```

- `headRefOid` = the head SHA (used by INV-001 `sha_attributed_to_our_push` and the inline-reply
  `commit_id`).
- `reviews` = `{author{login}, authorAssociation, state, body, submittedAt, url}`.
- `comments` = PR conversation comments (NOT inline review comments).

REST surfaces (inline-comment ids / `in_reply_to_id` are not on `gh pr view`, so REST is required):

```bash
gh api repos/<owner/repo>/pulls/<N>/reviews
gh api repos/<owner/repo>/pulls/<N>/comments
gh api repos/<owner/repo>/commits/<headSHA>/check-runs   # only if the probe shows emission_shape==check_run
```

Classification is pure against the probe-locked `DetectionContract` (`detection-contract.md`): key on
`augment_bot_login`; four states no-review / clean / findings / **declined** (T-201/202/203 + FR-9.1).
The V1.1 `declined` state fires when an Augment-authored comment matches BOTH probe-locked decline
regexes (`decline_phrase_regex` "abnormally large" AND `decline_retrigger_regex` "comment
augment/auggie/augmentcode review"), watermark-aware (a stale pre-watermark decline is ignored, EC-23).
The decline ARITHMETIC (the both-regex AND, the watermark comparison, the strict-once routing) stays in
the deterministic core; only the decline raw-surfacing comes from this poll script — the same
script-polls / FSM-decides seam as the other states. The decline is posted by the App as a **PR
conversation comment** (the `gh pr view --json comments` surface, equivalently `issues/<N>/comments` —
the same surface `retrigger-review.sh` posts to), NOT as an inline review comment. The poll script
therefore **merges** the conversation comments (`.comments` from `gh pr view`) with the inline review
comments (`pulls/<N>/comments`) into the emitted `comments` array, so the classifier sees the decline;
surfacing only the inline comments would make `declined` unreachable in production. (The classifier's
finding-comment rule requires `path`+`line`, so the path-less conversation comments are never miscounted
as findings.)

## Interval, timeout, backoff (FR-2.3 / FR-2.5 / NFR-2)

- **Interval ≥ 30s.** A value below 30 is **rejected, not rounded** ("minimum is 30 seconds", T-111).
- **Timeout default 1800s** (~30 min), configurable; **wall-clock since entering wait** (T-221/T-222).
- **Exponential backoff on 403 / 429 / secondary-limit:** `30 → 60 → 120 → … → cap 300s`, resetting
  on a successful poll (T-231). The backoff **counts toward the wall-clock timeout**.

## Division of labour (the NFR-6 seam)

- The **poll script** does ONE `gh`/`gh api` poll and returns a status line (`polling` / `clean` /
  `findings`, plus the raw payload for classification). It performs no arithmetic and holds no state.
- The **FSM** owns the backoff arithmetic (which interval to use next, whether the cap or the timeout
  is reached) and the state transitions. This keeps the `gh` I/O isolated to the script and the
  deterministic decisions in `superclaude.pr_submit` (NFR-6). The ref explicitly assigns the backoff
  arithmetic to the FSM, never the script.
