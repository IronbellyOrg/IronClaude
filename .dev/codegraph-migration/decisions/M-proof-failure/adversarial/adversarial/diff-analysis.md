# Diff Analysis: decision option comparison (M-proof-failure)

## Metadata

- Generated: 2026-10-30
- Variants compared: 3
  - Variant 1 = `option-a.md` (draft PR with a label, the Coder pattern)
  - Variant 2 = `option-b.md` (issue only)
  - Variant 3 = `option-c.md` (split by failure class)
- Source facts: `../../context.md` and `../../../M-major-versions/context.md` (treated as verified)
- Focus areas: never merging unverified bytes; what a person can do next; idempotency across daily runs; number of code paths to test
- Total differences found: 18 debatable points plus 5 unique contributions
- Categories: structural (2), content (7), contradictions (3), unique (5), shared assumptions (6)

Taxonomy tags: L1 surface, L2 structural, L3 state mechanics (guards, state across runs, boundaries).

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Failure classes modelled | One failure path for classes 1 and 2 ("Integrity failures (class 1) are treated the same way"); class 3 not mentioned | One failure path for classes 1 and 2; class 3 not mentioned | Three paths, one per class (integrity, behaviour, infrastructure) | Medium | L2 |
| S-002 | Title wording | "... [proof failed]" (PR) | "codegraph vX.Y.Z bump failed: <stage>" (issue) | "codegraph vX.Y.Z: integrity check failed" (issue); draft PR title not given | Low | L1 |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Integrity failure (hash mismatch or attestation failure) | Push branch, draft PR, label; the pin on the branch points at unverified bytes (A's own cost line) | Issue only, no branch | Issue only, no branch ("never put unverified hashes on a branch") | High | L3 |
| C-002 | Behaviour failure (install, index, tools/list, drift) | Draft PR + label + stage + log tail | Issue only; reviewer has no diff and must re-run the script by hand | Draft PR + label, "so a person can push a fix (for example an `MCP_TOOLS` or entry change) onto it" | High | L2 |
| C-003 | Infrastructure failure (API or download unavailable) | Not stated | Not stated | Neutral exit, step summary, `::warning::`, no issue; retries next schedule (as Coder does) | Medium | L3 |
| C-004 | Behaviour on the next daily run when a failure artifact already exists | Not stated (does it re-push the branch? reopen a PR?) | "Open (or comment on, idempotently by title) one issue" | Not stated for the draft PR or the issue | High | L3 |
| C-005 | What the failure report contains | Failed stage, proof log tail (PR body) | Run URL, stage, log tail, commands to reproduce locally | Failed stage and log tail (PR); issue body not specified | Medium | L2 |
| C-006 | Label | `needs-codegraph-proof` | none | `needs-codegraph-proof` (draft PR only) | Medium | L2 |
| C-007 | Number of failure paths to test (excluding the PASS path) | 1 (draft PR) plus an unstated infra path | 1 (issue) plus an unstated infra path | 3 (issue, draft PR, neutral exit) | Medium | L2 |

Orchestrator evidence for C-006: IronClaude's labels today are bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix (`context.md`). `needs-codegraph-proof` does not exist. Coder calls its own label "best-effort" and calls the draft state "the only hard non-mergeable state available" (`context.md`).

## Contradictions

| # | Point of Conflict | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Impact | Level |
|---|---|---|---|---|---|---|
| X-001 | Is a draft PR a safe container for unverified bytes? | Rationale: "draft cannot be merged". Cost: "an integrity failure (possible tampering) still pushes a branch whose pin points at unverified bytes; the draft looks like routine work in the PR list". A draft becomes mergeable with one "Ready for review" click, and a merged pin flows to every Coder workspace (`M-major-versions/context.md`). A's safety claim rests on a state one click away from mergeable. | "nothing mergeable is ever created from failed or unverified bytes" | "keeps unverified bytes off branches" | Medium | L3 |
| X-002 | Does the infrastructure path reach a person? | (silent) | (silent) | "no issue (retries next schedule)". `context.md`: "Nobody watches IronClaude Actions run summaries; issue and PR notifications reach the owner." A persistent infra failure (expired token, changed API, broken `gh attestation`) is therefore silent forever under C as written. | Medium | L3 |
| X-003 | Where is the boundary between integrity and infrastructure? | (one path, boundary irrelevant for 1 vs 2, but infra still undefined) | (same) | Integrity = "hash mismatch or attestation failure"; infra = "GitHub API or download unavailable". A truncated or partial download produces a hash mismatch; `gh attestation verify` also exits non-zero when the API is unreachable. C does not say how the monitor tells these apart, so the same event could take either path. | Medium | L3 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 2 (B) | Report carries the run URL and the exact commands to reproduce the proof locally | Medium: makes any failure artifact actionable without reading the workflow |
| U-002 | 2 (B) | Explicit idempotency rule: one artifact per version, found by title, comment instead of duplicate | High: only variant that addresses daily re-runs at all |
| U-003 | 3 (C) | Artifact chosen by failure class: integrity gets no branch, behaviour gets a fixable draft PR | High: the only variant that satisfies both "no unverified bytes on a branch" and "a diff to push a fix onto" |
| U-004 | 3 (C) | Explicit infrastructure path (neutral exit, warning, retry next schedule) | Medium: A and B leave it undefined, but see X-002 |
| U-005 | 1 (A) | "[proof failed]" marker in the PR title so the draft is visibly different from routine work | Low |

## Shared Assumptions

Agreement points scanned: all three variants (a) push nothing to `master` and rely on a human merge, (b) produce at most one artifact per run, (c) put the failed stage and the log tail into the artifact, (d) treat the PASS path as a ready PR (out of scope here).

| # | Assumption | Source Agreement | Classification | Promoted |
|---|---|---|---|---|
| (stated) | A human always merges; no auto-merge exists | (a) | STATED (`M-major-versions/context.md`) | No |
| (stated) | A draft PR cannot be merged until a person marks it ready | (a) | STATED (Coder comment in `context.md`) | No |
| A-001 | The monitor can classify a failure at runtime (integrity vs behaviour vs infrastructure) from exit codes and output | (b), (c) | UNSTATED | Yes |
| A-002 | A later daily run never overwrites commits a person pushed onto an existing bump branch | (b) | UNSTATED | Yes |
| A-003 | When a newer upstream release appears, an open failure artifact for the older version is superseded (closed or commented), not left open beside a new one | (b) | UNSTATED | Yes |
| A-004 | When a later run for the same version passes (flake fixed, assets re-uploaded), the failure artifact is resolved (draft made ready or replaced, issue closed) | (b) | UNSTATED | Yes |
| A-005 | The label exists or the workflow creates it, and the workflow token has the permissions each path needs (`contents: write`, `pull-requests: write`, `issues: write`) | (c) | UNSTATED | Yes |
| A-006 | A newly opened draft PR notifies the owner the same way an issue or a ready PR does | (c) | UNSTATED (UNVERIFIED for this repo's owner settings) | Yes |

### Promoted shared-assumption diff points

| A-NNN | Assumption | Source Agreement | Impact | Status | Level |
|---|---|---|---|---|---|
| A-001 | Failure class is reliably detectable at runtime | All variants route on the result of the proof | High: a misclassified integrity failure as infra is silent; infra as integrity is a false tamper alarm | Open for debate | L3 |
| A-002 | Re-runs do not clobber human commits on the bump branch | A and C push a branch | High: daily force-push could erase the human fix C exists to allow | Open for debate | L3 |
| A-003 | Newer release supersedes older failure artifacts | All variants are per-version | Medium: stale drafts or issues pile up | Open for debate | L3 |
| A-004 | Same-version later PASS resolves the artifact | All variants | Medium: stale draft or open issue after recovery | Open for debate | L3 |
| A-005 | Label and token permissions are in place | A and C use a label; all create PRs or issues | Medium: `gh pr create --label` with a missing label can fail the step | Open for debate | L2 |
| A-006 | Draft PRs notify like ready PRs | A and C rely on the draft being seen | Medium: an unseen draft is a silent failure | Open for debate | L2 |

## Summary

- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 8 (UNSTATED: 6 promoted as A-001..A-006, STATED: 2, CONTRADICTED: 0)
- Debatable points for convergence: 18 (S 2 + C 7 + X 3 + A 6)
- Taxonomy coverage: L1 = 1 (S-002), L2 = 7 (S-001, C-002, C-005, C-006, C-007, A-005, A-006), L3 = 10 (C-001, C-003, C-004, X-001, X-002, X-003, A-001, A-002, A-003, A-004)
- Highest-severity items: C-001, C-002, C-004, A-001, A-002
- Similarity check: variants differ on the core artifact choice; debate proceeds.
