# Diff Analysis: position paper comparison (D04 claim level and grants)

## Metadata
- Generated: 2026-11-20 (UTC)
- Variants compared: 2 (Variant A = position-OURS.md, Variant B = position-CLAY.md; Mode A, files copied as variant-1-original.md and variant-2-original.md)
- Total differences found: 19 debated points (S 2, C 10, X 4, A 3) plus 6 unique contributions
- Categories: structural (2), content (10), contradictions (4), unique (6), shared assumptions (3: 2 UNSTATED promoted, 1 CONTRADICTED flagged)
- Taxonomy tags (AD-5): L1 = S-001, S-002; L2 = C-001, C-002, C-004 to C-007, C-009, C-010, X-001, X-003, A-001 to A-003; L3 = C-003, C-008, X-002, X-004

## Structural Differences

| # | Area | Variant A (OURS) | Variant B (CLAY) | Severity |
|---|------|------------------|------------------|----------|
| S-001 | Order of cited facts and presentation (L1) | Leads with owner decisions R23/R25 and merged features, then guard, then grants | Leads with owner's Q35 and the gate closure, then supervision, then grants | Low |
| S-002 | Terminology for the same thing (L1) | "governed levels", "grant row", "Pipeline field picks the level" | "launch levels", "standing grants list", "Pipeline-level route" | Low |

Both papers share the same six section headings (Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right) and eight cited facts each; no structural gap beyond the two rows above.

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Claim level per issue (L2) | The Pipeline field picks the level (None, Worktree, Full, Full Submit mapped to `--pipeline` and `--submit`); R23/R25 | The watcher/orchestrator always claims at `--pipeline none` (R9, D:81) | High |
| C-002 | What runs the work after the claim (L2) | A launched agent (`orca agent launch`) at the chosen level, reporting by `result.md` | One supervised `worker-start` worker per issue, reporting on the Run mailbox | High |
| C-003 | Guard coverage (L3) | L1 hook + L2 pre-push, level state outside the worktree, fail closed (`W-ENFORCEMENT-ABSENT`); "the control that exists today" | `worker-start` worker is unbound by the guard (DQ7), no L1/L2, `master` unprotected (K12); accepted "for the first test issue" | High |
| C-004 | Deliverability today (L2) | Governed levels exist and are built (PR 425, issue 394, PR 441) but gated closed; behaves like B at the claim step now | Gate closed (R33), 12 observations skipped, issue 442 open, so R23/R25 deliver nothing live | Medium |
| C-005 | Per-issue throttle (L2) | The Pipeline field is the only per-issue brake between "claim and stop" and "go to a PR" | Only `hold:backlog` stops an issue; assignment takes it to merge and close | Medium |
| C-006 | Grant model (L2) | One grant row per issue, created at claim, listing the writes; written from the owner's go | One standing `grants` list in `repos.yaml`, six entries, per repo | High |
| C-007 | What a standing grant covers (L2) | Merge and close must never be bulk-granted (WORKER-CONTRACT 239-246) | `pr.merge` and `issue.close` are in the list (D:116, D:291) | High |
| C-008 | Integrity of the grant record (L3) | A per-issue row written from the owner's chat has no self-edit gap; the standing list sits in a file the orchestrator itself edits (D:688) | `E-NO-GRANT` refuses and logs every use; changes need an `--answer-ref` accepted by `answer-check`; closed `refuse(argv)` list | High |
| C-009 | Design surface (L2) | Status x Pipeline matrix (R23, R32 P-8, R33, R34), Project reads | None-only route: no matrix, no Project read (R1, R3, D:256) | Medium |
| C-010 | Identity of the recorded word (L2) | The owner's chat go, recorded by the agent | "Clay's recorded word" (D:688); design names no login for "the owner" | Medium |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | Does the owner's own record support none-only? (L2) | R23/R25 (2026-11-18, 2026-11-19) widen launch levels beyond None | Q35 "B1b" (2026-11-14, owner-answers line 184): watcher claims `--pipeline none`; built code agrees (launch.py:33, issue.md:48) | Medium |
| X-002 | "The control that exists today" (L3) | Fact 3 says the guarded level choice "is the control that exists today" | A's own costs say no governed level can run today (12 observations skipped, issue 442 open) | Medium |
| X-003 | What Q36 "for now" covers (L2) | Cost bullet: a grant row per issue needs a person and two sessions; owner accepted that "for now" only (Q36) | Fact 5: the per-issue grant row is a heavy control the owner accepted only for now (Q36); owner-answers line 185 reads Q36 as approval latency, line 130 is the grant row (Decision 8) | Medium |
| X-004 | Is the no-guard risk bounded? (L3) | Workers run unguarded under standing grants for every issue | Cites D:117 "accepted for the first test issue only" while the design adopts the route for all issues | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | A | Full Submit push rule: Pipeline value plus the `Approved` field is the person's go for that one issue's push, nothing else pushed (R25) | High |
| U-002 | A | Level recorded outside the worktree, fail-closed refusal if the guard is absent (flag design section 6) | Medium |
| U-003 | B | `answer-check`: refuses a relayed, wrong-entry, stale or unknown-source answer; fits the owner's chat-only rule (D:688) | High |
| U-004 | B | Closed "may do" list and `refuse(argv)` with one test per pattern (5.9, D:1117) | Medium |
| U-005 | B | Mailbox supervision: one message handled once per id, check-ins, restart (D:1104) | Medium |
| U-006 | B | Removal of Project reads drops a failure class the poll had (R31 needed a value-time observation, R36 withdrew it) | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both treat the claim's own writes (assign, comments) as acceptable | An assignment or approval by a person is the consent for the claim writes at every level; which signal (assignment, `Approved` field, label) is a separate question (topic D01) | UNSTATED | Yes |
| A-002 | Both route outward writes through one coordinator or orchestrator session | That session exists, was opened by a person (WORKER-CONTRACT line 70) or may be started by a script (ADD1), and is trusted to act unattended | UNSTATED | Yes |
| A-003 | Both ask who may change grants or give the go | "The owner" is one known identity: `ironbelly` in A, "Clay" in B (FULL-REPORT section 4) | CONTRADICTED | Flagged for debate |
| (not promoted) | Both | The #442 observations (OB-H1 1-9, OB-H2, OB-H3, OB-CTX) must pass before a governed level runs | STATED | No |
| (not promoted) | Both | Workers never write to GitHub (WC-9); the coordinator or orchestrator does | STATED | No |

### Promoted shared assumptions

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | Consent signal for the claim | Decides whether the level choice needs any per-issue input at all | Open (topic D01) |
| A-002 | Trusted unattended outward actor | Decides whether standing grants are safe for anything past low-stakes writes | Open (topic D06) |
| A-003 | Identity of "the owner" | Decides who may change the grants list | Open (topics D06, D16) |

## Summary
- Total structural differences: 2
- Total content differences: 10
- Total contradictions: 4
- Total unique contributions: 6
- Total shared assumptions surfaced: 5 (UNSTATED: 2, STATED: 2, CONTRADICTED: 1)
- Highest-severity items: C-001, C-002, C-003, C-006, C-007, C-008
