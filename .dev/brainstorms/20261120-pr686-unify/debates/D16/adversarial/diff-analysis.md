# Diff Analysis: D16 prevention package comparison

## Metadata
- Generated: 2026-11-20 (UTC)
- Variant 1 = OURS (`variant-1-original.md`, heavier package of FULL-REPORT section 11). Variant 2 = CLAY (`variant-2-original.md`, lightest change).
- Variants compared: 2
- Total differences found: 29 (S 2, C 13, X 3, U 7, A 4 promoted shared assumptions); convergence denominator = S + C + X + A = 22
- Taxonomy tags: L1 surface, L2 structural, L3 state-mechanics (guard, merge precondition, boundary). Each point carries one tag.

## Structural Differences

Both papers use the same six headings (Claim, Mechanism, Cited facts, Cost, Risk, What it gets right), so structural difference is small.

| # | Area | Variant 1 (OURS) | Variant 2 (CLAY) | Severity | Level |
|---|------|------------------|------------------|----------|-------|
| S-001 | Mechanism layout | Three numbered layers: words, visibility, enforcement | One four-sentence paragraph plus one template line | Low | L1 |
| S-002 | Cited-facts content | 10 facts, mostly describing the repository state and the gaps | 9 facts, mostly counter-evidence against the heavy items | Low | L1 |

## Content Differences
| # | Topic | Variant 1 (OURS) approach | Variant 2 (CLAY) approach | Severity | Level |
|---|-------|---------------------------|---------------------------|----------|-------|
| C-001 | Root cause of the incident | No second person was made to say yes (merged by author in 90 and 66 minutes, master unprotected) | A people problem: an unanswered question to a named person and an undefined "owner" | Medium | L2 |
| C-002 | Enforcement | CODEOWNERS plus required code-owner review set by the one admin; "silence blocks" | Nothing enforced; no admin setting; agreement in CONTRIBUTING.md | High | L3 |
| C-003 | Trigger for the extra approval | Path list (mechanical): WORKER-CONTRACT.md, hooks/, issue_watch/, docs/designs/, sc-issue skill | Self-classified: "design PR" and "PR that deletes code merged in the last 30 days" | Medium | L3 |
| C-004 | Roles paragraph | Roles in CONTRIBUTING.md; replace "the owner" by a login in design documents | Roles by login in CONTRIBUTING.md, owner `ironbelly`, maintainers `clayphi` and `IB-JonathanB` | Low | L2 |
| C-005 | Silence rule | Silence turns into a block through a required reviewer | One sentence: "silence is never a yes"; no mechanism, no deadline | Medium | L3 |
| C-006 | Related-work section and stop-on-overlap in `/sc:issue` | Adopt (item 1 of section 11) | Reject as useless for this incident (issue 655 cites 13 items; missed items were not searchable) | Medium | L2 |
| C-007 | Decision log `docs/decisions/` | Adopt, with a back-fill of 8 to 10 rulings | Not included; rulings stay in issue comments | Medium | L2 |
| C-008 | Work in flight | Tracked register or draft PRs | Draft PR or issue comment within a day (no table) | Low | L2 |
| C-009 | 24 hour cooling period for designs | Adopt | Not included; "merged by someone other than the author" instead | Medium | L3 |
| C-010 | Overlap scan (`/sc:overlap` or CI step) | Adopt (days of work) | Reject: issue 290 says no new skills or commands yet | Medium | L2 |
| C-011 | Role of issue 290 (open, assigned to `clayphi`) | Evidence that a spoken rule died unwritten; "finish #290" is item 9 of the package | The vehicle: finish 290 with the same text so its assignee owns the rule | Low | L2 |
| C-012 | Cost and who pays it | Under 1 hour to 3 hours for cheap items, days for scan; the owner becomes a queue on named paths (admitted) | Under 1 hour total; no recurring cost except one PR line | Medium | L2 |
| C-013 | Meaning of the shared `ironbelly` login | Listed as a risk; enforcement still worth having | A reason the CODEOWNERS approval proves little | Medium | L3 |

## Contradictions
| # | Point of Conflict | Variant 1 (OURS) position | Variant 2 (CLAY) position | Impact | Level |
|---|-------------------|---------------------------|---------------------------|--------|-------|
| X-001 | What the 51 of 60 self-merged PRs show (29 `clayphi`, 22 `ironbelly`, none approved) | The author's word was the only gate, so a gate is missing (OURS fact 3) | Working on trust is the norm; gates change how the owner works too (CLAY fact 1) | Medium | L2 |
| X-002 | Whether checks that search the repository address the miss | Package closes gaps 1 and 2 (no search-first rule, duplicate check only lists); decisions and plans must be made visible (OURS facts 7 and 10) | Issue 655 cited 13 items so a section or a stop would have passed; the missed items were local or in another repository (CLAY facts 3 and 4) | Medium | L2 |
| X-003 | Tension inside CLAY: its item 3 asks that design and deletion PRs be merged by someone other than the author, yet it argues that gates change the working mode and that conventions rely on reviewers (CONTRIBUTING.md:77-79); PR 682 had no human reviewer (OURS fact 4) | Convention without a reviewer is exactly what failed | The agreement itself supplies the second person | Medium | L3 |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | OURS | Decision log with a back-fill of the rulings others build on (gap 6) | Medium |
| U-002 | OURS | Server-side control: master has no protection and no ruleset (404 and `[]`); the only item that makes silence block | High |
| U-003 | OURS | 24 hour cooling period (but GitHub cannot enforce it) | Low |
| U-004 | OURS | Precedent that an advisory CI check exists and that making it a block is a settings decision (`boundary-guard.yml`) | Low |
| U-005 | CLAY | The missed items were unpushed or in another repository, so publishing beats searching | High |
| U-006 | CLAY | `/sc:issue --claim` already stops on an issue assigned to someone else (`refs/claim.md:42`); `/sc:overlap` would contradict issue 290 | Medium |
| U-007 | CLAY | The one-sentence silence rule ("a question to a named person is answered in writing; silence is never a yes") | High |

## Shared Assumptions

| A-NNN | Assumption (UNSTATED in both papers) | Source agreement | Impact | Status | Level |
|-------|--------------------------------------|------------------|--------|--------|-------|
| A-001 | The owner, or a named alternate, answers a question or a review request within a bounded time. Neither paper gives a deadline or says who rules when the owner is away. Without it, a required yes becomes a stall and a written yes becomes a skipped rule. | Both rely on a person's yes (required reviewer, written yes) | High | Promoted | L3 |
| A-002 | The rule reaches the sessions that do the work. The repository is worked mostly by Claude sessions, which read CLAUDE.md and the skills; both papers put the rule in CONTRIBUTING.md and the PR template only. | Both place the rule in human-facing files | Medium | Promoted | L2 |
| A-003 | Clay accepts that `ironbelly` is the owner for design rulings. The merged design says the owner is Clay (FULL-REPORT section 4); a roles paragraph written by the owner settles it only if Clay agrees. | Both write "owner = `ironbelly`" | High | Promoted | L3 |
| A-004 | The next collision will look like this one (a design or deletion PR on a known path or of recent code). Neither says what covers a different shape, such as a large feature PR that duplicates open work. | Both aim at the 681 and 682 pattern | Medium | Promoted | L2 |

Not promoted (STATED in both): a CODEOWNERS approval or a "yes" under the shared `ironbelly` login does not prove a person gave it (OURS risk list, CLAY fact 5).

## Summary
- Total structural differences: 2
- Total content differences: 13
- Total contradictions: 3
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED 4 promoted, STATED 1 not promoted, CONTRADICTED 0)
- Highest-severity items: C-002 (enforcement), U-002, U-005, U-007, A-001, A-003
- Taxonomy coverage: L1 (S-001, S-002); L2 (C-001, C-004, C-006 to C-008, C-010 to C-012, X-001, X-002, A-002, A-004); L3 (C-002, C-003, C-005, C-009, C-013, X-003, A-001, A-003). All three levels covered.
- Similarity check: variants are not substantially identical (13 content differences against 6 shared headings); the debate runs.
