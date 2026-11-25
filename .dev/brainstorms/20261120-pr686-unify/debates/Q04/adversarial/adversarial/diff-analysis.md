# Diff Analysis: position paper comparison (Q04, push go scope)

Variant 1 = `position-OURS.md` (a typed go per push class, sha-bound). Variant 2 = `position-CLAY.md` (one go per issue or PR covers every push until merge). Paths are under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/Q04/`.

## Metadata
- Generated: 2026-11-20
- Variants compared: 2
- Total differences found: 17
- Categories: structural (1), content (8), contradictions (3), unique (8), shared assumptions (4 promoted, 6 enumerated)

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|---|---|---|---|
| S-001 | Section layout | Claim, Mechanism, Cited facts (9), Costs, Risks, Gets right | Same headings, 8 cited facts | Low |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity |
|---|---|---|---|---|
| C-001 | What the go is bound to | A typed line naming repo, branch and the sha to be pushed | A per-issue (Full Submit field) or per-PR (typed `/sc:pr-submit --monitor 3` line) go, no sha | High |
| C-002 | Fix-round pushes of one `/sc:pr-submit` run | Each needs its own go (then concedes the typed run line must serve as the go) | Covered by the run the person started, inside caps and guards | High |
| C-003 | Push after a revert or rebase | New go; a rebase is a force push, refused unless the go names old and new sha | Covered by the same per-PR go until merge | High |
| C-004 | When a go ends | Consumed by the push it names; void when the head moves to an unnamed sha | Until merge or close; admits no event ends it earlier | High |
| C-005 | Scope of the Full Submit go | First push and PR only (R25 "nothing else is pushed") | Push and PR, with the loop that follows (D04, D06 item 7) | Medium |
| C-006 | Merge | Own go, sha-bound, never covered by a push go | Own go, the place the person's brake is spent | Low |
| C-007 | Who pushes | A person-opened top-level session; `/sc:pr-submit` never a worker (WC:23, WC:244) | Cites ADD1 (D:135): a worker runs `/sc:pr-submit` in its own top-level session | Medium |
| C-008 | Cost of asking | Up to 5 prompts (hard cap 5 rounds) | Same, and "a stop for the person each time" | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Impact |
|---|---|---|---|---|
| X-001 | Intra-V1: Mechanism 2 says "each fix-round push gets its own go"; Risks says the typed `/sc:pr-submit` line must be "the person's go for that run, or the rule cannot be followed" | Mechanism 2 vs Risks bullet 1 | n/a | High |
| X-002 | Cross: whether a worker may run `/sc:pr-submit` | WC:23, WC:244: never as a worker | Mechanism 1 and fact 1: ADD1 worker runs it (D06 verdict item 5 already rejected ADD1) | Medium |
| X-003 | Cross: whether a sha-bound push go is recorded owner design | Risks bullet 3: D06 and Q01 bind the sha to merge only, so sha-bound push is "OURS extended, not recorded" | Fact 6 agrees the pin is designed for merge | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | PR 368 incident (2026-11-04): a round-2 push re-created a branch deleted at merge; a go must not outlive PR state | High |
| U-002 | 1 | A rebase is a force push, which `/sc:pr-submit` never does; it needs a go naming old and new sha | Medium |
| U-003 | 1 | Push go and merge go never cover each other (SEC-01, SEC-12) | High |
| U-004 | 1 | Honest note that the topic's "sha-bound per push" is not in D06 or Q01 | Medium |
| U-005 | 2 | A sha-bound go cannot exist for a fix commit not yet written | High |
| U-006 | 2 | `/sc:pr-submit` already fences the push mechanically: one fix commit per cycle, `push_range_mismatch` halt, fast-forward only, no push to default branch, `push_count <= max_rounds + 1` | High |
| U-007 | 2 | Merge-time controls (13-reason gate, `--match-head-commit`, reviewer hold) catch a bad fix push | Medium |
| U-008 | 2 | WC:245's "no earlier pre-authorization" makes a pre-commit per-issue go need the same amendment as R25 | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | The person typing `/sc:pr-submit --monitor 3` in a person-opened session is the go, and the harness cannot tell typed text from script-typed text (D06 INV-003) | Both treat the typed line or field as the person's go | Whole rule rests on it; a script can spoof | Promoted (UNSTATED) |
| A-002 | A `/sc:pr-submit` run is a bounded unit with a terminal status and a push cap | Both count rounds (hard cap 5) | Decides where a go can end | STATED (V2 Mechanism 2); not promoted |
| A-003 | A Full Submit launch runs `/sc:pr-submit` in an ordinary top-level session, not as a worker | Both rely on R25 | If wrong, WC:23 is broken | Promoted (UNSTATED) |
| A-004 | The tool's own fix commits, made in the person's session during the run, are not "worker commits the person has not seen" (WC:245) | Both treat fix-round pushes as the run's by-product | Decides whether WC:245 even applies to them | Promoted (UNSTATED) |
| A-005 | Nothing else pushes the feature branch between rounds, and if something does the pre-push head guard stops the run | Both rely on `pr_head_ok` and `push_range_mismatch` | A head moved outside the run is the case no go text covers | Promoted (UNSTATED) |
| A-006 | D06 and Q01 recorded a sha-bound go for push | The topic text says "bound to the head sha per D06 and Q01" | Wrong: merge only | CONTRADICTED (V1 Risks bullet 3; D06 items 1 and 7 name no sha for push); not promoted, flagged for debate |

## Summary
- Total structural differences: 1
- Total content differences: 8
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 6 (UNSTATED: 4, STATED: 1, CONTRADICTED: 1)
- Highest-severity items: C-001, C-002, C-003, C-004, X-001, U-001, U-003, U-005, U-006

Taxonomy tags (AD-5): L1 surface: S-001. L2 structural: C-005, C-006, C-007, X-002, A-003. L3 state mechanics: C-001, C-002, C-003, C-004, X-001, X-003, A-001, A-004, A-005 (state, guard, boundary, invariant terms). Others (C-008, U-*) default L2.
