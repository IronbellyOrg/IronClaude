# Augment Poll (C2) — the poller contract

This ref pins the poll surface and timing for the SKILL's attended, in-session poll loop. The poll **script**
(`scripts/poll-augment-review.sh`) performs a single `gh`/`gh api` poll and emits one JSON line; the
**FSM** (`superclaude.pr_submit`) does the backoff arithmetic. The script name is kept, but **one
snapshot serves both reviewers** (Augment and Codex): the same reviews, comments and threads are
classified twice, once per reviewer adapter, on the same `expected_head`. This split keeps `gh` out of the
deterministic core (NFR-6) — the script touches `gh`, the core decides.

> Every `gh`/`gh api` call below pins the RESOLVED `--repo <owner/repo>` (origin's `owner/repo`,
> parsed from `git remote get-url origin`; FR-1.3 / AC-7). A bare `gh` without `--repo` is a defect.

## Poll surfaces (FR-2.1)

The adapter obtains PR metadata, then separately paginates formal reviews and both comment sources:

```bash
gh pr view <N> --repo <owner/repo> --json number,url,headRefName,headRefOid,baseRefName
gh api repos/<owner/repo>/pulls/<N>/reviews --method GET -F per_page=100 -F page=1
gh api repos/<owner/repo>/issues/<N>/comments --method GET -F per_page=100 -F page=1
gh api repos/<owner/repo>/pulls/<N>/comments --method GET -F per_page=100 -F page=1
```

REST page numbers advance until a page has fewer than 100 records. Reviews preserve `id`, `commit_id`,
`submitted_at`, `state`, `body`, `user`. `comments` merges raw issue and inline comments (including
`pull_request_review_id`, nullable `line`/`original_line` when supplied); issue comments retain the
legacy decline surface; they also carry the Codex summary comment (its `codex-review-state:v1`
marker and `updated_at`). The configured `augmentcode[bot]` and `augmentcode` identities are unchanged;
the Codex identities are `chatgpt-codex-connector[bot]` (REST) and `chatgpt-codex-connector` (GraphQL).
No check-run fetch is implemented here; an absent check run is not completion evidence.

The repo-pinned GraphQL query uses `reviewThreads(first:100,after:$endCursor)` with
`pageInfo{hasNextPage endCursor}` and `headRefOid` on **every page**. `threads` contains raw nodes:
`id`, `path`, nullable `line`/`originalLine`, `isResolved`, `isOutdated`, and
`comments(first:1){nodes{...}}`. Only the root is intentionally requested, not a truncated conversation.
Root fields include `id`, `databaseId`, `body`, `path`, nullable `line`/`originalLine`, `createdAt`,
`author{login}`, `replyTo{databaseId}` and `pullRequestReview{id databaseId commit{oid}}`.
Replies cannot create extra findings or turn a human-rooted conversation into an Augment finding.

## Snapshot and classification contract

One JSON line carries `pr`, `url`, `base`, `head_sha`, `observed_at`, `reviews`, `comments`, `threads`,
`reviews_ok`, `comments_ok`, `threads_ok`, and advisory `state` (`review_present` / `polling`).
`observed_at` is the snapshot's UTC timestamp, emitted after collection. The pure core rejects review
submission times later than this observation, without reading a live clock. On initial fetch failure,
the script emits an incomplete event with null head and all flags false (no successful observation).

- `reviews_ok`: complete validated REST reviews; `comments_ok`: **both** REST comment sources;
  `threads_ok`: complete validated GraphQL thread pages.
- API failure, GraphQL `errors` even at exit zero, null connections, malformed pages, missing or
  repeated/nonadvancing cursors, duplicate IDs, or reaching the 1000-page-per-source cap makes that
  source incomplete. Temporary-file staging keeps large payloads out of command arguments.
- The adapter checks head agreement on thread pages and re-reads `headRefOid` after all requests.
  A changed/unreadable final head makes **all three flags false**. During a pushed-SHA wait the
  SKILL must additionally require `payload.head_sha == pushed_sha` **before** the explicit head
  override: a later, internally consistent snapshot may already describe somebody else's push.
- Use `classify(payload, contract, watermark=watermark, current_head_sha=expected_head)` and then
  `actionable_finding_comments` with the **same payload and context**, followed by
  `finding_from_comment` (exported from `severity_router` and the package). Never dispatch raw REST
  comments independently. The SKILL snapshot gate converts empty `findings` selections (possible
  for legacy `has_findings`) or normalization `ValueError` to `polling`, not empty-driver clean.

Cosmos requires all three flags literally true plus validated completion and thread data; explicit
false flags also block legacy classification. Missing additive flags are supported only for legacy
injected payloads, not live Cosmos snapshots. The four core states are `polling`, `clean`, `findings`,
`declined`. `declined` still requires both configured regexes on an Augment-authored entry, strictly
newer than the watermark when supplied; only a valid attributable re-review overrides that decline.
Metadata validation and historical unresolved-root/count rules are in `detection-contract.md`.
Incomplete or invalid evidence remains `polling` under the existing finite timeout: no automatic fix,
round increment or `terminal_clean`.

The advisory `state` (`review_present` only when `reviews_ok`, `comments_ok` and `threads_ok` are all
true and at least one formal review exists; otherwise `polling`) is an Augment-era hint only;
it is not used for Codex, whose completion is the `codex-review-state:v1` marker
(`detection-contract.md`). Codex is classified with `classify_codex` and `codex_finding_comments` on
the same payload and context.

## Two reviewers: wait outcomes and the merge

Each poll gives each reviewer a **wait outcome**: `pending`, `done`, `absent` or `incomplete`.

| Wait outcome | Augment (`augment_wait_outcome(state, nxt, absent=...)`) | Codex (`codex_wait_outcome(...)`) |
|---|---|---|
| `pending` | `polling` and `poll_outcome` is `S2_CLASSIFY` or `S5C_SILENCE_REREQUEST` | gate state not `clean` / `findings` (still `polling`), and either active and before `--timeout`, or inactive, before the silence deadline and Augment not settled |
| `done` | gate state `clean` / `findings` / `declined` | gate state `clean` / `findings` |
| `absent` | `TERMINAL_AUGMENT_NO_RESPONSE`, or already absent | inactive when Augment has settled or at the silence deadline, or already absent |
| `incomplete` | `TERMINAL_TIMEOUT` (partial activity) | active, gate state still `polling` at `--timeout` |

A reviewer already recorded absent (`rebuild_state()["absent_reviewers"]`), or one whose identity set
is empty, is `absent` at once and is never `pending`. `merge_wait((augment_wait, augment_state),
(codex_wait, codex_state))` maps the pair to one round outcome:

| Augment | Codex | Round outcome |
|---|---|---|
| `pending` | any | keep polling |
| any | `pending` | keep polling |
| `done: declined` | any settled | `declined` (S5b fallback; Codex `findings` join its single re-entry) |
| `done` | `done` | `findings` if either has findings, else `clean` |
| `done` | `absent` / `incomplete` | Augment's state (Codex incomplete is reported) |
| `absent` / `incomplete` | `done` | Codex's state (Augment's condition is reported) |
| `absent` | `absent` | `no_response` → `TERMINAL_AUGMENT_NO_RESPONSE` (no configured reviewer responded) |
| `incomplete` | `absent` / `incomplete` | `timeout` → `TERMINAL_TIMEOUT` |
| `absent` | `incomplete` | `timeout` → `TERMINAL_TIMEOUT` (partial reviewer activity, no classified review) |

Both reviewers share the one `--timeout` wall clock and `--poll-interval`; no second wait is added.

**Codex absence rule.** Codex posts its summary comment seconds after a PR opens, so a connected
repository shows Codex activity within the first polls. Codex with no activity when Augment's wait
outcome is settled, or by the silence deadline, is absent: append `reviewer_absent{reviewer:
"codex"}` and ignore Codex for the rest of the run (no wait, no re-trigger). There is no Codex silence
poke. When Augment's silence outcome fires while Codex is present, append `reviewer_absent{reviewer:
"augment"}` and continue with Codex. An Augment-only PR therefore waits no longer than before and adds
only one `reviewer_absent` event.

## Interval, timeout, backoff (FR-2.3 / FR-2.5 / NFR-2)

- **Interval ≥ 30s.** A value below 30 is **rejected, not rounded** ("minimum is 30 seconds", T-111).
- **Timeout default 600s** (~10 min), configurable; **wall-clock since entering wait** (T-221/T-222).
- **Silence window default 300s** (`--silence-timeout`, min 30, clamped to `--timeout`). Zero
  Augment-attributed review/comment (`has_augment_activity` false) is Augment's
  `TERMINAL_AUGMENT_NO_RESPONSE` outcome (its wait outcome `absent`), not `TERMINAL_TIMEOUT`; the run
  ends there only when Codex is absent too (merge table above). The same deadline is the Codex
  absence deadline. Partial activity (summary/comment but no classified review) still times out
  as `TERMINAL_TIMEOUT`. L3 may consider one poke: pass `rerequested=` / `rerequested_at=` from
  `rebuild_state()`, then `check_idempotent("silence_rerequest_invoked")` → append
  `{event_type: silence_rerequested, pr_number, elapsed}` → `retrigger-review.sh --body "augment review"`.
- **Exponential backoff on 403 / 429 / secondary-limit:** `30 → 60 → 120 → … → cap 300s`, resetting
  on a successful poll (T-231). The backoff **counts toward the wall-clock timeout**.

## Division of labour (the NFR-6 seam)

- The **poll script** assembles ONE snapshot (multiple paginated requests), not a classification.
  Its advisory `state` is not an FSM outcome. It owns no retry/backoff state.
- The **FSM** owns the backoff arithmetic (which interval to use next, whether the cap or the timeout
  is reached) and the state transitions. This keeps the `gh` I/O isolated to the script and the
  deterministic decisions in `superclaude.pr_submit` (NFR-6). The ref explicitly assigns the backoff
  arithmetic to the FSM, never the script.
