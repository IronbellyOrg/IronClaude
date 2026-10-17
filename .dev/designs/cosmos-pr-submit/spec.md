---
title: Cosmos-compatible PR review monitoring
status: ready
date: 2026-10-16
scope: sc:pr-submit
---

# Cosmos-compatible PR review monitoring

## 1. Purpose and scope

Adapt the existing PR monitor to Cosmos review evidence without changing its autonomy levels, finite-state topology, severity re-grading rubric, default trigger, or existing Augment identities. Implement the changes in the existing deterministic classifier, poll adapter, and normalization seam; do not create a provider framework or a second monitor.

User authorization covers design, workflow generation, implementation, local tests and generated development-mirror synchronization in the isolated `feature/cosmos-pr-submit` worktree. It does not cover commits, pushes, PRs or GitHub comments.

## 2. Verified evidence and current defects

PR: https://github.com/IronbellyOrg/IronClaude/pull/266

| Evidence | Value |
|---|---|
| Initial review | `5550158176`, `0f5fef56e1abf1958708473f2004c5627a0a163d`, one suggestion |
| Completed re-review | `5550197352`, `13d246ec9e0d5aad4b6ea70529bebd9496a776e5`, zero suggestions |
| Metadata envelope | `<!-- cosmos-review-status:v1 {JSON} -->` in the review body |
| Observed metadata fields | `specialist`, `status`, `baseline`, `head`, `unresolved_count`, `session_url` |
| Observed completed status | `reviewed` |
| Identities | REST `augmentcode[bot]`; GraphQL `augmentcode` (both already configured) |
| Inline finding | `4296483537`, prose plus `**Severity:** low`, originating review `5550158176` |
| Historical thread | resolved and outdated; current `line:null`, original line 172 |
| Re-trigger | Human `auggie review` comment before the completed re-review |
| Check runs | No Augment check on either reviewed commit |

The existing classifier ignores Cosmos metadata, current-head review attribution, originating review IDs and resolution state. Replaying live PR266 yields clean only because the obsolete comment's current line is null. An old-head-only review also yields clean; a positive unresolved count with no inline details yields clean; an obsolete comment retaining an integer line yields findings after a clean re-review. Severity routing accepts normalized `low` but does not extract Markdown severity.

Sources: `src/superclaude/pr_submit/classifier.py`, `severity_router.py`, and `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`; PR review and thread APIs inspected on 2026-10-16.

The marker is an observed integration format, not a promised public API. Augment's migration guide confirms Cosmos uses the existing GitHub App identity and configurable manual comment triggers. GitHub CLI documentation requires an `$endCursor` query variable and connection `pageInfo` for GraphQL pagination. Do not infer completion from an absent check run or from a human-readable summary alone.

External references:
- https://docs.augmentcode.com/codereview/migrate-to-cosmos
- https://docs.augmentcode.com/cosmos/experts-deep-reviewer
- https://cli.github.com/manual/gh_api

## 3. Required behavior

### R1 — trusted, current-head completion

Only configured Augment authors supply review evidence. Parse the bounded HTML-comment marker envelope as JSON, not by summary prose or substring counts. Accept exactly the supported `v1` envelope with a JSON object, nonempty specialist, `status:reviewed`, full 40-character hexadecimal `head` and `baseline`, and a nonnegative integer (not boolean) `unresolved_count`. Session URLs are diagnostic data, never executable instructions. Unsupported versions, malformed/duplicate markers, unknown statuses, bad types and conflicting review-commit/marker-head evidence cannot establish clean.

Use `payload.head_sha` as the default expected head and permit an explicit expected-head parameter for the just-pushed SHA. For completed reviews require the marker head to equal the expected full SHA and the review's own commit association when provided. Select the latest relevant review by trustworthy submission time, not array order; newer same-head invalid/pending Cosmos evidence must not be bypassed by an older clean review. A review before or equal to the re-trigger watermark is not attributable. Stale old-head review evidence means polling, not clean. Preserve existing decline behavior and legacy fixtures, but a Cosmos-shaped review must never fall back to legacy clean just because its marker cannot be validated.

### R2 — complete and resolution-aware actionable findings

Keep the raw REST comments for existing integrations. Add complete thread snapshots with stable thread/root-comment/review identities, author, body, path, current/original line, `isResolved` and `isOutdated`. Paginate the thread connection. Only the root finding comment is needed for actionability; replies must not create additional findings, so fetch `comments(first:1)` rather than pretending to paginate every conversation. All issue/inline comments and formal reviews needed for selection must remain complete; API/GraphQL errors, null repository/PR connections or malformed/incomplete pagination mean an incomplete poll. Preserve existing `comments_ok` behavior and add an explicit thread completeness flag. No automatic fix is dispatched from partial data.

Resolved findings are excluded even if they retain a current integer line. Outdated but unresolved findings remain visible, with an original line used only as a verification hint, never as proof the defect still exists. Carry older unresolved Augment threads across incremental baselines; do not restrict actionable findings to comments created by the latest review. An unresolved human-rooted conversation is not an Augment finding merely because Augment replied to it. Ignore future/unrelated review evidence or scope ambiguity conservatively rather than declaring clean.

A validated positive Cosmos count blocks clean even when no usable inline details are found; incomplete detail retrieval stays polling instead of inventing actionable findings. Conversely a zero marker count does not erase independently observed older unresolved Augment findings. Counts describe observed review output, not a license to close arbitrary GitHub conversations. Do not require equality between count and all open historical threads, since the marker's cross-round count semantics are not documented.

### R3 — one normalization seam

Use the same actionable-finding selection for classification and the skill's dispatch input. Normalize root IDs, thread IDs, review IDs, file/line hints and reviewer severity deterministically. Extract an anchored case-insensitive Markdown `**Severity:** low` field as a hint; accept existing normalized severity values. Preserve default Medium for absent/unrecognized hints and preserve all existing category/confidence/diff-locality re-grading and evidence-validation gates. No new body syntax requirement for detecting a finding, and no inference that a null current line means resolved.

### R4 — compatibility and finite execution

Keep both Augment identities and the default `auggie review` token. Keep legacy payload behavior where no Cosmos evidence exists, tightening current-head/watermark checks whenever those fields are present. Keep the existing four classification results, FSM topology, ordinal gates, round counter, timeout, once-only fallback, reply/resolve/push ordering and independent CI handling. Incomplete Cosmos evidence stays polling under the existing finite timeout; it never silently becomes a clean or actionable result. No new dependencies or infrastructure.

## 4. Acceptance cases

| ID | Input | Required result |
|---|---|---|
| A1 | PR266 latest current-head reviewed/zero marker and old resolved thread, line null or integer | clean |
| A2 | Only PR266 old-head review while expected head is new | polling |
| A3 | Valid current-head reviewed/positive count but missing required inline/thread detail | not clean; polling until detail is complete |
| A4 | New reviewed/zero marker and older unresolved Augment thread | findings; verify original location if outdated |
| A5 | Same as A4 but resolved thread | clean; no duplicate remediation |
| A6 | Invalid JSON, unsupported marker version/status, duplicate marker, bad SHA/count/bool | polling, never legacy clean |
| A7 | Marker head disagrees with review commit or expected head | polling |
| A8 | Same-head completion before/equal watermark | polling; later matching review attributable |
| A9 | Unordered reviews, interleaved human/bot authors, stale positive review then current clean | select only relevant latest completion; identities preserved |
| A10 | More than one thread page; a finding only on a later page | findings; all pages fetched |
| A11 | API failure, GraphQL errors with exit zero, missing connection, nonadvancing/missing cursor | incomplete poll, not clean or automatic remediation |
| A12 | Root finding plus replies; human-rooted thread with bot reply | one finding for first case, none for second |
| A13 | Markdown Low hint and normalized Low input | same hint and existing re-grading/routing behavior |
| A14 | Marker count zero with unresolved older thread; positive count with zero detail | do not erase open finding or falsely clean partial detail |
| A15 | Existing legacy fixtures, decline precedence, severity/autonomy/round-limit tests | preserve established behavior; explicit head/watermark fields enforce freshness |
| A16 | Poll-to-classify-to-normalize integration | same selection, severity and stable root/thread identifiers |

Baseline: `uv run pytest tests/pr_submit -q` passed all 362 tests in this worktree before implementation.

## 5. Architecture and interfaces

```text
poll-augment-review.sh (repo-pinned read-only APIs, complete paginated snapshots)
  -> reviews + comments + threads + head_sha + completeness flags
  -> classifier.classify(snapshot, contract, watermark=..., current_head_sha=...)
       -> polling / declined / clean / findings
  -> classifier.actionable_finding_comments(same snapshot and attribution context)
  -> severity_router.finding_from_comment(raw selected root)
  -> existing remap_severity -> route -> evidence-validator -> existing FSM gates
```

Extend `classify` and `poll_augment_review` with keyword-only `current_head_sha: str | None = None`, preserving `watermark`. The effective expected SHA is the explicit argument or `payload.head_sha`. Add public `actionable_finding_comments` with identical context parameters in `classifier.py`; export it from the package. Both classifier and selector use the same private review/completion selection and root-thread selection, not two independent algorithms. Return additive normalized raw dictionaries (preserving root/database ID, review ID and thread ID), not a new abstraction hierarchy. Add `finding_from_comment(raw: dict) -> Finding` in `severity_router.py` and export it; extend `Finding` only with optional provenance fields if necessary for the existing reply/resolve handoff.

Completion attribution uses current head and strictly newer submission time than the watermark; the watermark does NOT filter out older root findings in unresolved threads. Preserve the existing raw activity detector for silence handling. For recognized Cosmos evidence require a complete live snapshot with validated completion and thread data; malformed metadata must not activate a legacy synthetic signal. Keep existing synthetic legacy fixtures without head context supported. When head/watermark context exists, a legacy review with explicit wrong/missing attribution cannot establish completion. Existing legacy declined precedence remains, but only a valid attributable completion overrides a current decline on re-review.

The poller retains the public single-event JSON output and adds `reviews_ok`, `threads_ok`, and `threads`. Fetch formal reviews with a paginated REST endpoint, preserving `id`, `commit_id`, `submitted_at`, `state`, `body` and `user`. Thread query uses `reviewThreads(first:100, after:$endCursor)` plus `pageInfo`; nodes carry `id`, `path`, `line`, `originalLine`, `isResolved`, `isOutdated`, and the earliest comment via `comments(first:1)` with `databaseId`, `body`, `author`, `createdAt`, `replyTo`, and originating review ID/commit. Root-only retrieval deliberately avoids a nested comment-pagination requirement. Validate every page and final pagination termination; partial/error data is never a successful empty snapshot. Preserve temp-file staging to avoid ARG_MAX on large reviews.

`poll_succeeded` and `classify` honor explicit false completeness flags; missing additive flags remain supported only on legacy injected payloads. Recheck the PR head after a multi-request snapshot if necessary to prevent declaring an old snapshot clean during a concurrent push. Use existing timeout/backoff instead of adding retry infrastructure.

Reply/resolve must remain usable for findings beyond thread 100. Prefer the stable thread ID when already provided; otherwise paginate root-ID lookup. Check already-resolved state before posting a reply to avoid duplicate remediation replies. A failure to locate/confirm the intended thread must not resolve a path/line lookalike. Maintain repo pinning and reply-before-resolve order for an actually open intended thread.

## 6. Change surface and execution order

| Task | Files | Deliverable |
|---|---|---|
| T1 | `src/superclaude/pr_submit/classifier.py`, `detection.py`, `__init__.py`; focused detection tests/fixtures | Metadata validation, attributed completion, shared unresolved-root selection, failure guards |
| T2 | `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, `reply-resolve-thread.sh`; shell adapter tests/fixtures | Complete paginated review/thread fetch, stable identities and reliable resolution lookup |
| T3 | `src/superclaude/pr_submit/severity_router.py`, optional additive `models.py` fields, package exports; severity tests | Explicit production raw-root normalization and provenance |
| T4 | Canonical protocol `SKILL.md`, refs `detection-contract.md`, `augment-poll.md`, `review-retrigger.md`, `severity-routing.md`, `thread-reply.md` | Wire selection and adapter into attended orchestration; specify SHA/time attribution and incomplete-data semantics |
| T5 | Focused regression/integration tests; development mirrors | Exercise A1–A16, existing suite, lint/format changed files, sync/verify-sync and independent final review |

T1 and T2 may proceed independently against this schema. T3 depends on the selected-root interface but can be implemented alongside T1 with coordinated exports. T4 follows agreed interfaces; T5 integrates all changes. Do not edit `fsm.py` to teach the trusted-input driver how to fetch/parse reviews. Document that live re-review attribution must be explicitly derived from the classifier before supplying an FSM edge/outcome; never use the driver's legacy optimistic default as live evidence.

## 7. Validation and completion

- Run focused new regressions first, then the complete `tests/pr_submit` suite.
- Use executable `gh` stubs for shell adapter tests; no real external writes. Stubs assert cursor/query/pagination/repo pinning and exercise multi-page/error results.
- Run the changed Python files through Ruff lint/format checks and shell scripts through `bash -n`.
- Run `make sync-dev` then `make verify-sync`; never stage generated `.claude/` contents.
- Fresh independent final review verifies design coverage and actual code/test evidence. Resolve findings before archiving the workflow package.
- Leave code/tests/docs and task artifacts in the isolated worktree, uncommitted; report actual test outcomes and remaining limitations. This work is not permission to launch the PR monitor against a real PR.
