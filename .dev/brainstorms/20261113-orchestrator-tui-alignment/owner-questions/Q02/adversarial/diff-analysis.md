# Diff Analysis: owner-answer proposals for Q2 (watcher claim level and permission acceptance)

## Metadata
- Generated: 2026-11-14 (Step 1, sc-adversarial-protocol Mode A, depth quick)
- Variants compared: 3 (variant-1 = proposal-A "claim-only, decline the permission acceptance, FU-1 waits"; variant-2 = proposal-B "keep the default `worktree` level as a deliberate chain, gated on the ship gates, acceptance for both sessions"; variant-3 = proposal-C "claim-only, accept permission-free for the one test issue")
- Total differences found: 18
- Categories: structural (1), content (6), contradictions (3), unique (5), shared assumptions (3 promoted)
- Context file for all advocates: `../question.md`

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|------|-----------|-----------|-----------|----------|
| S-001 | Section set and order | five sections, same order | same | same | Low (identical by design of the brief) |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|-------|-----------|-----------|-----------|----------|
| C-001 | Claim level | `--pipeline none` | default `worktree` (claim, worktree `issue-<N>`, second governed agent stopping at a plan) | `--pipeline none` | High |
| C-002 | Written acceptance of permission-free sessions | declined for now | given for the test issue, covering both sessions | given for the one test issue, one session | High |
| C-003 | When FU-1 (first live test) runs | held until a permission-on session is shown feasible or the acceptance is given later | held until OB-H1 item 1 and item 5, OB-H2, OB-H3 are confirmed passed | runs after WA-01 to WA-03 (subject to the "claim at any level" gate, status UNVERIFIED) | High |
| C-004 | Code and document changes | one small watcher PR | no watcher code change; design document D2 amended | one small watcher PR | Medium |
| C-005 | Downstream work unblocked (cron enable WA-05, sweep label SW-10, handoff design SW-13 and WA-07) | none | only after the ship gates pass | yes, after FU-1 | Medium |
| C-006 | Design contradiction (design D2 says the claim stops at `next-steps.md`) | removed by code | removed by amending the design | removed by code | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|-------------------|-----------|-----------|-----------|--------|
| X-001 | Can FU-1 run now? | No, by owner choice | No, until gates pass | Yes, "FU-1 can run" (Unlocks), though its own risk section says the "claim at any level" gate may still hold it | Medium |
| X-002 | What an approval should deliver | a claim and comments (design D2) | "a ready plan waiting for a person, not just a comment" | a claim and comments (design D2) | High: owner intent |
| X-003 | Is a permission-free session acceptable for one test | no | yes, two sessions | yes, one session | High: risk acceptance |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 | Establish whether a watcher-launched session can run with permission checks on (the two knobs `CCSESSION_PERMISSIONS` and `CC_CLAUDE_FLAGS`) and still finish unattended | Medium |
| U-002 | 2 | FU-1 exercises the full chain including a second agent, giving the later handoff design real data | Medium |
| U-003 | 2 | Names the claim command's ship gates (OB-H1 items 1 and 5, OB-H2, OB-H3) as explicit FU-1 preconditions | High |
| U-004 | 3 | Ledger records "for the test issue only"; it authorises no later issue | Medium |
| U-005 | 2 | Amend the design document so design and code agree | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | All "What happens next" sections | FU-1's outward writes (issue assignment, marked comments, a possible ClickUp write) need no permission beyond the Q2 answer; no separate grant row (the spec's grant table has a `live-test` action) is required | UNSTATED | Yes |
| A-002 | C-002, X-003 | A permission-free session that reads untrusted issue text makes only the writes the claim command intends (the FU-1 write list is the full list of what it could do) | UNSTATED | Yes |
| A-003 | C-003, C-005 | The live preconditions hold when the owner answers: Orca answers a read verb on this host (ORCA-AVAILABLE; the probe found the app not reachable on 2026-11-13) and Q20 (who owns the watcher worktree agent) is answered | UNSTATED | Yes |
| A-004 | All | Only a validated integer issue number reaches the session prompt (design D3) | STATED (question.md; variant facts) | No |

Promoted shared-assumption points:

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | FU-1's outward writes are covered by Q2 alone | next-step sections | If a grant row is also needed, every option adds one more owner step (L2, dependency) | UNSTATED |
| A-002 | A permission-free session makes only intended writes | C-002, X-003 | Untrusted issue text could steer a session with permission checks off beyond the listed writes; the acceptance would then cover more than it names (L3, guard, boundary) | UNSTATED |
| A-003 | Orca is reachable and Q20 is answered | C-003, C-005 | FU-1 cannot run under any option until both hold (L2, dependency) | UNSTATED |

## Summary
- Total structural differences: 1
- Total content differences: 6
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, X-002, X-003
- Taxonomy levels: L1 (S-001), L2 (C-004, C-005, C-006, X-001, A-001, A-003), L3 (C-001, C-002, C-003, X-002, X-003, A-002)
- Similarity check: well above 10 percent difference; debate proceeds.
