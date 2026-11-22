# Diff Analysis: D12 `/sc:issue` plan sections and planning at create vs claim

## Metadata
- Generated: 2026-11-20 (UTC), unattended, depth standard
- Variants compared: 2 (Variant 1 = OURS `position-OURS.md`, Variant 2 = CLAY `position-CLAY.md`)
- Total differences found: 34
- Categories: structural (3), content (14), contradictions (3), unique (9), shared assumptions (5)

## Structural Differences

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|---|---|---|---|
| S-001 | Section order | Claim, Mechanism, Cited facts, Costs, Risks, Gets right, Recommended shape | Claim, Mechanism, Cited facts, Costs, Risks, Gets right | Low |
| S-002 | Closing section | Ends with a concrete "Recommended shape" (KEEP / KEEP-ADAPT / REJECT / one added rule) | Ends with "What it gets right"; no disposition list | Medium |
| S-003 | Heading depth | H2 only | H2 only | Low |

## Content Differences

| # | Topic | Variant 1 (OURS) | Variant 2 (CLAY) | Severity |
|---|---|---|---|---|
| C-001 | Where heavy planning (brainstorm, design) belongs | At claim, after the accuracy check | At create, once, on a strong model (issue 689) | High |
| C-002 | PR 661 (plan sections in templates, merged) | Keep as merged | Keep; it is step 1 of the idea | Low (agreement) |
| C-003 | PR 690 `--plan` and `--remaining` | Keep plain `--plan` and `plan_body.py`; hold back `--remaining` until a hand-back loop exists | Keep as built, including `--remaining` (serves orchestrator hand-back) | Medium |
| C-004 | Issue 689 (open, unbuilt): move chain rows into create, add `## Design` | Reject | Adopt; decisions are marked "for Clay" | High |
| C-005 | Claim ignores the plan sections PR 661 added (double planning) | Real gap; close it with one rule in claim (short chain when plan passes check) | Real gap; close it by moving the chain to create and having claim read `## Approach` | Medium |
| C-006 | Who runs `/sc:brainstorm` and `/sc:design` at create | Workers have no Skill or Agent tool; calling session would break B2 | Not stated in 689; listed as a risk | High |
| C-007 | Staleness of a design stored in the issue body | Design in body goes stale; accuracy check would have to validate a design | Acknowledged risk; no mitigation named | Medium |
| C-008 | Refuse claim of an issue without plan sections | Reject: refuses all older and hand-filed issues | Adopt (assumption "refuse and point to --plan") | Medium |
| C-009 | Rename `## Fix approach` to `## Approach` | Not proposed; touches PR 661 tests and `plan_check` token | Proposed; accept both headings during migration | Low |
| C-010 | `--mode other`, GitHub form fields | Silent | Proposed (docs, chores, research; three forms) | Low |
| C-011 | Planning tier at create | Silent; cites B14 (T1 or T2 by complexity at claim) | Tier 1a or 1b at every create depth | Medium |
| C-012 | Where the cost lands | Claim time, per claim | Create time, per filing; "not measured, no baseline" | Medium |
| C-013 | Fit with the owner's Status and Pipeline stages (R23, R25) | Create-time design makes the Spec stage moot | Silent (R23 is unpushed) | Medium |
| C-014 | Strength of the evidence for intent | Owner's issue 302 and design record B2/B4/B14 | Clay's issue 651 goal and 689 problem statement | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|---|---|---|---|
| X-001 | What the design goal of `/sc:issue` is | Claim assumes the body is out of date and plans after an accuracy check (issue 302 line 10) | Planning should be front-loaded at filing "so a worker only executes" (issue 651) | High |
| X-002 | Can create run brainstorm and design | The create workers have tools `Read, Grep, Glob, Write, Bash` only (`agents/issue-worker-t1.md:5`) | Issue 689 says create "runs" brainstorm and design on tier 1a or 1b | High |
| X-003 | Is plan-at-create "the opposite of" the existing design | Chain at claim is B2/B4/B14, an owner decision | Claim chain "is the opposite of the goal in 651" | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---|---|---|
| U-001 | 1 | Status and Pipeline stage model (R23, R25) would be undercut by create-time design | Medium |
| U-002 | 1 | `worktree` level plan boundary with human approval (`templates/launch-prompt.md:21-23`) | Medium |
| U-003 | 1 | One-rule concession: when plan sections pass, claim routes to the short chain and quotes the plan | High |
| U-004 | 1 | Check that `/sc:issue` is on the never-as-worker list (`WORKER-CONTRACT.md:23`) so a calling session is required | Medium |
| U-005 | 2 | `plan_body.py` makes the body write deterministic (`check`, `splice`, `verify`) | High |
| U-006 | 2 | Capability gap: nothing fills plan sections of pre-661 or hand-filed issues | High |
| U-007 | 2 | Design 4.11 `plan_check` and the hold depend on `--plan` (PR P before PR B) | Medium |
| U-008 | 2 | `--mode other` and plan fields on the three GitHub forms | Low |
| U-009 | 2 | Sandbox hand run with before and after bodies; three review rounds | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Classification | Impact | Status |
|---|---|---|---|---|---|
| A-001 | The light plan that PR 661 makes workers draft (one `/sc:analyze` pass) is good enough to execute from | Both keep PR 661 | UNSTATED | Medium | Promoted |
| A-002 | Claim runs once per issue, so "plan once at create" saves cost versus "plan at claim" | Both compare cost of the two placements | UNSTATED | Medium | Promoted |
| A-003 | An unattended consumer (watcher or orchestrator) will exist and read the plan before work starts | Both treat plan-before-claim as a watcher concern | UNSTATED | High | Promoted |
| A-004 | Issue 689 and PR 690 are read as of 2026-11-20 and may still be edited; the pr-p snapshot equals the live PR head | Both cite them as fixed | UNSTATED | Low | Promoted |
| A-005 | The `ironbelly` login that merged PR 661 and `/sc:issue` work stands for the owner's acceptance | Both name 661 as accepted | CONTRADICTED by the full report (shared login) | Medium | Promoted |

## Summary
- Total structural differences: 3
- Total content differences: 14
- Total contradictions: 3
- Total unique contributions: 9
- Total shared assumptions surfaced: 5 (UNSTATED: 4, STATED: 0, CONTRADICTED: 1)
- Highest-severity items: C-001, C-004, C-006, X-001, X-002, U-003, U-005, U-006, A-003
