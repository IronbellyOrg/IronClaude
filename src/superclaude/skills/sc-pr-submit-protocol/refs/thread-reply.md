# Thread Reply + Resolve (C4) — the reply/resolve contract

This ref pins the exact reply + resolve surfaces for a remediated finding. The order is
**reply-FIRST-then-resolve** (T-601 → T-602). Every call pins the fork
(`--repo IronbellyOrg/IronClaude` for `gh pr`; `repos/IronbellyOrg/IronClaude/...` path for
`gh api`). The wrapper script `scripts/reply-resolve-thread.sh` implements this; this ref is its
contract.

## 1. Reply — REST `in_reply_to` (FR-6.1)

```bash
gh api --method POST repos/IronbellyOrg/IronClaude/pulls/<N>/comments/<COMMENT_ID>/replies -f body="<reply-text>"
```

- `<COMMENT_ID>` MUST be a **top-level review comment** (replies-to-replies are unsupported) — it is
  the original Augment inline finding comment id captured during polling.
- The reply summarizes **fix + commit SHA + passing validation commands**.
- **`applied_edits` citation rule (T-603, INV-009):** the reply MUST cite the `applied_edits` status.
  An `applied_edits == 0` / ungroundable cycle MUST say **"no code change applied"** and MUST NEVER
  say "resolved". Only a cycle that actually applied a grounded edit may describe the thread as fixed.

## 2. Suggestion block — trivial fixes only (FR-6.5, gated by `applied_edits > 0`)

When a fix is **trivial** — a single contiguous hunk, single file, ≤10 changed lines, no cross-file
edits — the reply embeds a fenced ```` ```suggestion ```` block reproducing the applied hunk on the
cited line (a one-click re-applyable diff as evidence, T-640). **Non-trivial** fixes (>10 lines or
multi-file) carry the prose summary + commit SHA only, **no suggestion block** (T-641). A suggestion
block is NEVER emitted on an `applied_edits == 0` cycle.

## 3. Resolve — GraphQL `resolveReviewThread` (FR-6.2, GraphQL-only)

There is **no REST endpoint and no native `gh pr` verb** to resolve a review thread (gh 2.45.0;
cli/cli#12419 unimplemented). Resolution is two `gh api graphql` calls:

**(a) Obtain the thread node id** — REST comment/review ids are NOT GraphQL thread node ids. Walk the
PR's `reviewThreads` connection and match the thread containing the Augment comment (by `path`+`line`
or the comment `databaseId`):

```bash
gh api graphql -f query='
  query($owner:String!,$repo:String!,$pr:Int!){
    repository(owner:$owner,name:$repo){
      pullRequest(number:$pr){
        reviewThreads(first:100){
          nodes{ id isResolved path line comments(first:1){ nodes{ databaseId author{login} } } }
        }
      }
    }
  }' -f owner=IronbellyOrg -f repo=IronClaude -F pr=<N>
```

**(b) Resolve it** (mutation input = the matched thread node `id`):

```bash
gh api graphql -f query='
  mutation($threadId:ID!){ resolveReviewThread(input:{threadId:$threadId}){ thread{ id isResolved } } }' \
  -f threadId=<THREAD_NODE_ID>
```

- **Permissions HALT:** `resolveReviewThread` needs Pull Requests read+write on the authenticating
  identity. A "Resource not accessible by integration" / 403 maps to a **HALT** with a clear
  "needs PR read+write" message — NOT a silent retry.

## 4. Ordering, idempotency, and the single summary thread

- **Reply FIRST, then resolve** (T-601 → T-602): the reply summarizes the fix + SHA + passing
  validation, then the thread is resolved.
- **Idempotency:** skip a thread already showing `isResolved: true` (the `resolved_thread_ids` set,
  §11.4) — append an `idempotency_skip` run-log event rather than re-mutating. Reply idempotency is
  the thread-scoped `reply_key` (no duplicate annotations, NFR-1).
- **Single summary thread:** a clean re-review posts **exactly one** summary thread (the conversation
  comment via `gh api --method POST repos/IronbellyOrg/IronClaude/issues/<N>/comments -f body=...`),
  NOT one comment per finding (T-642). The §17 residual summary (FR-6.4) uses the same single-thread
  surface.
