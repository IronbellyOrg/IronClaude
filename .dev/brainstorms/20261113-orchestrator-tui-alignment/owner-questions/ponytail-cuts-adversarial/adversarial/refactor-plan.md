# Refactoring Plan

## Overview
- Base: Variant 2 (sonnet:security)
- Incorporated: V1 (4 items), V3 (4 items)
- Planned changes: 8; rejected: 9
- Overall risk: Low (the plan changes the cut list text only)

## Planned Changes
| # | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|
| 1 | V1 C21 coupling | C21 row | append | C-014, 89: the gate constant goes only together with an approved C17 | Low |
| 2 | V1 freeze-and-defer spine | C07 to C11, C16, C19, C20 | keep | Unanimous or near-unanimous (C-018); advocates 1 and 3 conceded | Low |
| 3 | V1 owner-decision labels | C12, C17, C24 | append | V1 recommended but did not act; V2 and V3 agree these need a new owner decision | Low |
| 4 | V1 C20 | C20 | modify to DEFER | C-013, 81: no design effort, #423 stays open, no collision-only trigger | Low |
| 5 | V3 C04 residual | C04 | append | C-004, 83: the probe runs the candidate once (`install_user_setup.py:259`) | Low |
| 6 | V3 "backup is not approval" | C01 | append | C-001 and X-005, 86 and 90 | Low |
| 7 | V3 capture caveat | C02 | modify | C-002, 78: comparison and message tests are deferred, not erased | Low |
| 8 | V3 summaries not frozen | C19 | modify | C19 is unanimous MODIFY: caveat line only, no blanket freeze | Low |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-008 | V1: cut the GitHub label and comment input | Overrides Decision 3; the 4,000-line saving is unverified; V1 itself fell to 60 percent and advocate 1 conceded |
| C-011 | V1: delete the questions-panel code | Reverses the staged direction; size unverified; Q19 may bring a questions screen back |
| C-012 | V1: write the snapshot only with `--snapshot` | Alters a merged default; external readers not excluded |
| C-010 | V1: delete `slo_numbers` and its test | A documented operator step (`issue-watcher-setup.md:470`, `:680`) still calls it |
| C-015 | V1: 30-day deadline then delete the watcher | The deadline is invented; route B depends on the watcher |
| C-017 | V1: carry out the `/sc:task` retirement | Outside this program; the owner's record authorizes no removal |
| C-003, C-004, C-005 | V3: KEEP the full cards | Advocate 3 conceded they were too strict; cards become lines |
| C-007 | V3: KEEP Q20 | Deferred with the named condition instead |
| C-014 | V1: delete the constant now | Removing the guard alone opens a read the owner has not passed |

## Risk Summary
All planned changes are wording or status changes in a document; rollback is `git revert`.

## Review Status
Auto-approved (non-interactive). The owner's direction was "proceed with the cuts that survived debate", so execution is limited to what that covers (see the merge log).
