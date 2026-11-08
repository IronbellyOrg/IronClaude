# Refactoring Plan

## Overview

- Base: variant 2 (reviewer 2, qa persona, opus class).
- Incorporated from variant 1: 6 changes. Planned changes in total: 8. Rejected alternatives: 4.
- Risk: Low overall (text-level merge of findings; no code).
- Output of the merge: `adversarial/merged-verdict.yaml` (merge_method: adversarial) with the deduplicated findings M2-01..M2-14, the 17-finding disposition, the coverage statement and the plan verdict. IDs "M2-" mark this re-run's findings so they cannot be confused with the earlier run's M-01..M-17.

## Planned Changes

| # | Change | Source | Target in base | Rationale (debate evidence) | Integration | Risk |
|---|---|---|---|---|---|---|
| 1 | Replace the finding-severity labels by the HIGH/MEDIUM/LOW scale only, with no deviation category and no hedged labels | brief rule (reviewer-briefs/reviewer-1.md:3); S-002 | base findings table | both advocates conceded their label flaws | replace | Low |
| 2 | Add the documentary basis for the budget finding: archived help file lines 131-132, "only works with --print"; recommend recording the pty /clear case as unavailable under the existing cap, or authorizing a separately bounded interactive run (an owner choice made before execution); drop --disable-slash-commands for that run | variant 1 A-02; C-002 (agreed, 92) | base N-4 row | verified by the calibrators and both advocates | replace | Low |
| 3 | Add a self-check that times out a dependent run while the survivor stays alive, and require that a runner-caused stop is labelled differently from a harness-caused loss | variant 1 A-01; C-001 (agreed tie) | base N-3 / Q-6 rows | testable and cheap | append | Low |
| 4 | Narrow A-03: the plan does not establish the originating controller's identity before and after /clear; state that identity together with Q-1's ordered calls and expected statuses (governed before /clear, ordinary after) and Q-7's expected fork status | variant 1 A-03; C-003 | base Q-1 / Q-7 | advocate 1 conceded Q-1 is more concrete | merge | Low |
| 5 | Add redacted process-tree snapshot fields (pid, ppid, start identity, role) for the wrapper, Git and hook trees, next to Q-3's "not run (budget)" label and Q-5's real governed Git push | variant 1 A-04; C-004 | base Q-3 / Q-5 rows | complementary, not exclusive | merge | Medium |
| 6 | Add the reparenting assertion: the intermediate parent exits, the PPID of the same live descendant changes, and the selector is sampled afterwards while the supervisor lives | variant 1 A-05 (unique) | new row | helper:292-295 installs a subreaper; plan:66 samples before the exit | append | Low |
| 7 | Restate N-1: the plan does not force thirteen starts (plan:22 shares four shapes across three), but the ledger has no run id, so add claude_run_id and claude_started | X-001 | base N-1 row | both advocates agree on the facts | replace | Low |
| 8 | Restate the coverage verdicts: INF-003 Partial; INF-001, INF-002, INF-008 covered with the defects tracked as findings; INF-006 covered (lexical miss) | X-002, C-006 | base coverage table | the Partial verdicts of variant 1 repeat its own findings for three of the four requirements | replace | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach was kept |
|---|---|---|
| S-001 | variant 1's section order | order does not affect any finding |
| S-003 | variant 1's narrative treatment of the Tier 1 defects | a verdict per defect is auditable (agreed, 90) |
| C-005 | variant 1's "not attempted within this budget" wording alone | variant 2's explicit "not observed (reason)" category is a complete fix |
| X-002 | variant 1's four Partial verdicts | three of the four duplicate findings already recorded; only INF-003 stays Partial |

## Risk Summary

All changes are wording of findings and recommendations; none alters a file outside the reflect output. Change 5 is the largest (it adds new required fields to the plan once applied); it is a recommendation, not an edit.

## Review Status

Auto-approved (non-interactive run), 2026-11-08T02:17Z.
