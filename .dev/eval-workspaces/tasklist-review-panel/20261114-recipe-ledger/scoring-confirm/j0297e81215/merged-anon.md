review: 1 of 3
# Merged review 1 (coordinator script; panel of 3 reviewers)
candidate: <path> sha256 1f84077e475af7358384ebaf383d03500bc6d6e46b9a85e8a977a67a18341e0a
reviewers:
- R1: report <path>, block ok true
- R2: report <path>, block ok true
- R3: report <path>, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | single | CRITICAL | - | R1 |
| L2 | open | yes | overlap | CRITICAL | - | R1, R2 |
| L3 | open | no | single | MAJOR | - | R1 |
| L4 | open | no | single | MAJOR | - | R1 |
| L5 | open | no | single | MAJOR | - | R2 |
| L6 | open | no | single | MAJOR | - | R2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: Override without Codex fields disables Codex, but design A0 requires absent keys to fall back to the shipped identity so Codex stays on.
- anchor: "A local override YAML without Codex fields still loads (Codex identities empty, so Codex is disabled for that override)"

### L2

#### L2.t1b-1 (F2)

- claim: Codex completion time as marker updated_at alone rejects roots created before the formal review submission; design A1 requires the later of the two times.
- anchor: "completion time = `updated_at`, no later than `observed_at`, strictly newer than the watermark when given"

#### L2.t1b-1 (F3)

- claim: Keeping created-no-later-than-completion selection reproduces the PR 337 polling-to-timeout failure that design A6 replaced for both reviewers.
- anchor: "(default: the Augment identities, so Augment behaviour is unchanged)"
- anchor2: "unresolved Codex-rooted threads through `_thread_findings` with the Codex identities and the marker time"

#### L2.t1b-1 (F4)

- claim: Two summary comments always classify polling, but design A3 uses the marker with the latest updated_at and reserves polling for a tie.
- anchor: "exactly one Codex-authored issue comment with one bounded `<!-- codex-review-state:v1 {JSON} -->` marker"
- anchor2: "Running status, wrong head, two summary comments, malformed or duplicate-key JSON"

#### L2.t1b-1 (F9)

- claim: list_review_threads requires priority and severity for Augment threads but no task defines how they are derived without a P-badge.
- anchor: "as `{reviewer, path, line, original_line, is_resolved, priority, severity, thread_id, comment_id}`"

#### L2.t1b-1 (F10)

- claim: Artifact outputs are written to ./artifacts without stating the base directory, so they may land in the repo-root artifacts folder that is never staged.
- anchor: "saving the output to ./artifacts/t7-dry-check-pr336.txt"
- anchor2: ".dev/tasks/ is always staged (git add .dev/tasks), including this package and its artifacts/."

#### L2.t3-1 (F1)

- claim: An implementer obeying src-only skips CLAUDE.md/docs and fails Task 15 grep check; obeying Task 15 violates the constraint.
- anchor: "Edit src/superclaude/ only, then run make sync-dev; never edit or stage .claude/ copies."
- anchor2: "Edit only the sentences that state Augment-only pr-submit behaviour: CLAUDE.md"

#### L2.t3-1 (F4)

- claim: Marker-time to completed dict shape and issue-comment vs inline selection are unspecified, forcing implementer guess.
- anchor: "_thread_findings(threads, contract, completed, identities=None)"

#### L2.t3-1 (F5)

- claim: ./artifacts reads as repo-root artifacts, not .dev/tasks artifacts, conflicting with staging rule.
- anchor: "./artifacts/t7-dry-check-pr336.txt"

## Other findings

- L3 (MAJOR, open, single): Wait-outcome signatures omit the already-absent set and empty-identity rule design A2 requires, so sticky absence on resume is unspecified.
- L4 (MAJOR, open, single): No task states the rereview_requested timestamp, resume watermark source, or cycle_id reuse design A4 requires.
- L5 (MAJOR, open, single): Design file absent in checkout; merge table and Codex gate rows are delegated only, forcing implementer guess.
- L6 (MAJOR, open, single): loop-guard lists 37 without silence events; adding only reviewer events yields 39 not 41, failing acceptance.

## Reviser brief

Blocking finding ids: L1, L2.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
