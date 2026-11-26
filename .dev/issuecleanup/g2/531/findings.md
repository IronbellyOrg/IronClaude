# Issue 531 review

Structure: findings skeleton registered in ../450/report-template.md, derived from this dispatch's required fields.

Reviewed checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, on 2026-11-24. Independent local evidence review: PASS with non-blocking notes; see `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/531/analyze/evidence-review.md`.

## Verdict and evidence
**Verdict: still-relevant.** Keep the feature open; do not classify it as delivered or as an active implementation merely because related building blocks and experiments exist.

PR #519 merged on 2026-11-12, merge commit `d2d8a2d166c945f556d921b31530a3673f00df89`, and supplies reflect-specific shadow measurement. PR #581 merged on 2026-11-17, merge commit `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d`, and includes the hand-run model-combination experiment alongside its primary review-safety work. Neither establishes the requested general central sampling/fetch/execute/upload system. Live all-state PR search for `531` returned no matches; search for `shadow` returned #519 plus other documentation/unrelated matches, not an identified standalone-module implementation.

Code confirms the distinction: reflect keeps legacy authoritative and shares reviewer dispatch (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:338-349`); the manifest stages remain review-specific (`src/superclaude/cli/review/manifest.py:38-63`). This supports the issue's 2026-11-17 comment that the generalized module remains wanted and unbuilt in the inspected source, not the conclusion that every historical or unmerged branch lacks work.
## Real current state
| Requested behavior | Verified current state |
|---|---|
| Central 0-100 percentage gate before supported commands | NOT IDENTIFIED in inspected source. Existing reflect shadow mode is explicitly selected with `--t2-engine shadow`; the issue's contradictory scale/direction remains unresolved in its only comment. |
| Fetch command variables and upload results centrally | NOT IDENTIFIED. The existing review telemetry describes local JSONL/SQLite storage (`src/superclaude/cli/review/telemetry.py:1-19`). No end-to-end central service was demonstrated. |
| Models, reasoning effort and prose variations | PARTIAL PRIOR ART, not the feature. The five-combination experiment recorded 15 runs but no blind quality score (`.dev/eval-workspaces/shadow-model-combos/FINDINGS.md:1-3,40-42`). A generalized safe prose-copy or variable-fetch path was not identified. |
| Clearly labeled workstation shadows | Reflect has named shadow engine and separate panel artifacts; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:338-349`. This does not establish labeling across supported commands. |
| Continuous queued variation runs from real work | NOT IDENTIFIED as a product module. Issue #487 contains the overlapping reusable experiment-framework proposal; its latest comment says no framework code is on master, and the indexed CLI layout has no `lab` package. |
| Configurable run count and maximum parallel runs | REUSABLE PIECES ONLY. Eval's injected-worker scheduler clamps concurrency to 1-15 (`src/superclaude/cli/eval/orchestrator.py:140-198`), but its default CLI executor returns a null implementation (`src/superclaude/cli/eval/commands.py:1386-1405`). Reflect's required-run count is an exit check, not a scheduling cap (`scripts/reflect_shadow_exit.py:26-34,55-57`). |

The source-level non-interference guard is real: shadow publication is refused before authoritative files are overwritten (`src/superclaude/cli/review/manifest.py:491-500`). Runtime behavior was not rerun. Existing related implementation does not satisfy the issue's eight acceptance criteria as a general module.
## Concrete next steps
1. Settle the percentage rule in the requested PRD, including 0 and 100, comparison direction, randomness and unavailable-config behavior. The latest issue comment proposes 100 = always and draw below the percentage = run; it is not a recorded owner resolution of the contradictory original wording.
2. Complete or locate the issue's requested PRD/workflow-selection, plugin-reuse research and deeper design outputs. None is attached in the returned issue comments. Do not run those larger research chains or post to GitHub as part of this read-only review.
3. Resolve overlap with #487 before implementation. Prefer one execution/queue/results foundation and a thin command-trigger adapter over two competing experiment schedulers; this is a recommendation requiring design approval, not an adopted split.
4. Define command coverage, isolated copied inputs/prose, central configuration integrity, permission to upload real work, result format, requested versus observed model identity, campaign spend and run/parallel limits.
5. Implement and test one command end to end first, then the continuous queue: probability endpoints, offline behavior, validated variable application, isolation, actual execution, cap enforcement and central results. Preserve legacy verdict/output ownership. Do not confuse successful artifact publication with independently scored quality.
## Complexity and size
**Complexity: complex. Size: XL.** The full request crosses command triggers, central configuration and results, safe model/prose variants, continuous queueing, concurrency/spend limits and real-input privacy. Existing reflect bookkeeping and a stubbed eval execution path reduce only part of that work; a standalone manifest extraction would be much smaller but would not satisfy this issue.
## Priority
**P2.** Useful measurement infrastructure for reducing review cost and comparing changes, but no production outage, immediate safety defect or verified downstream issue blocked on this feature was found. Definition and reuse decisions should precede an expensive build.
## Dependencies
- **Needs:** an agreed gate rule and design/privacy boundary; these are unresolved requirements, not separately numbered blockers.
- **#487, reusable spec/task evaluation framework (OPEN):** strongest overlap for continuous queueing, model variations, scoring and budgets. Coordinate the architecture first; a formal finish-to-start dependency was NOT established.
- **#520, Centralized Review Panel (OPEN), and #549, review-panel unification tracking (OPEN):** related integration surfaces for the reflect adapter/results. Their completion is not proven necessary before a general shadow module can start.
- **Blocks:** no explicit downstream dependency verified. Issue 531's live `blockedBy` and `blocking` collections are both empty, and no closing PR reference is returned.
- **Not prerequisites:** #450's watcher rollout and #423's knowledge-sharing layer are related orchestration work, not verified blockers of this feature.
## Related issues
- #487 (OPEN), Re-useable Spec-Task Eval Framework: overlapping experiment execution/queue/scoring proposal; latest comments explicitly assess eval reuse and propose a sibling `superclaude lab` package, not a delivered service.
- #520 (OPEN), Centralized Review Panel: potential shared review interface/results consumer. Its body still describes #519 as open, while the later comment and live PR metadata confirm it merged.
- #549 (OPEN), Review-Panel Merged Efforts: programme sequencing, research comparison and unification plan. Its body links #531; it is not evidence this shadow module shipped.
- #550 (OPEN), proven tasklist-experiment design capture: related evidence inventory and re-test work, explicitly links #531. Its body and returned comment were read; this is related work, not a verified prerequisite.
- #450 (OPEN), issue-watcher live test/shadow/cron rollout: operational dry-run meaning of shadow, distinct from controlled pipeline-variable experiments.
- #423 (OPEN), Orchestrator v2 knowledge-sharing layer: broad future relationship already named by #531; the latest review keeps its catalogue/reporting scope separate.

These issues' bodies and comments were read live. The issue body also points to research artifacts on another branch; current completeness of those branch-only deliverables is UNVERIFIED.
## Related PRs
| PR | Verified state / merge commit | Relationship |
|---|---|---|
| #519 | MERGED, 2026-11-12; `d2d8a2d166c945f556d921b31530a3673f00df89` | Original reflect Stage 0-2 measurement/dormant-kernel/shadow work. Legacy remains default; not a general experiment service. |
| #581 | MERGED, 2026-11-17; `fc4b2240225080cbfc5e7bbc1a1f4f71cd24084d` | Primarily review safety-scan work, also includes the shadow-model-combos experiment files. Those data are prior art, not completion of #531. |

Both PR bodies, returned comments and file lists were inspected. Their file lists are large/capped, so they do not support an exhaustive no-other-files claim. The newer `shadow` search hit #681 was additionally read: its body states docs-only orchestrator design, with no code, tests or configuration changes; it merged on 2026-11-20 at `c2a1395522239429dd21f19cadd206fd643fec03`. It is not a shadow-module implementation. Other hits were not used as proof of implementation. There is no verified PR closing #531.
## Verification limits and negative evidence
- **Full GitHub event timeline: UNVERIFIED.** This dispatch permits only `gh issue view/list` and `gh pr view/list`. The issue-view JSON field list has comments, dependency and closing-PR references but no complete timeline events, so assignments, cross-reference events, label history and other non-comment events could not be reconstructed. No forbidden API or browser access was used to bypass that restriction.
- GitHub reads establish #531's OPEN state, one returned comment dated 2026-11-17, no assignee, enhancement label, empty dependency lists and no returned closing PR. They do not prove no unlinked or differently named branch work exists.
- Negative evidence: all-state PR search `531` returned `[]`; all-state `shadow` search found #519 and other non-module hits. Filename discovery `**/*shadow*` and source searches for `shadow|experiment`, central-gate and experiment-queue terms located reflect/review pieces, watcher dry-run references and development experiments, not the complete requested flow. A broad probability search was capped, so absence claims are deliberately bounded to inspected paths.
- The extraction evaluation at `.dev/tasks/done/TASK-WF-implementStages0-20261111-202912/artifacts/shadow-standalone-evaluation.md:7-28,65-80` was read as historical prior art, then checked against current source. Its old 1.8.0 contract references must not replace current source, which names 1.9.0 at `src/superclaude/skills/sc-reflect-protocol/SKILL.md:349`.
- No live central service, model execution, quality scoring or tests were run. Static assertions and prior experiment narratives are not rerun evidence. Unmerged-branch code/design completion and unattended 24/7 operation remain UNVERIFIED.
- Failed checks retained honestly: initial `gh issue view --comments --json` was rejected, then corrected to JSON including comments; initial report Edits were freshness-blocked, then corrected by explicit Reads. No GitHub, index, source, commit or branch changes were made.
- Supporting analysis: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/531/analyze/analyze-report.md`. Only this dispatch's report directory was written; no staging was performed because the worker has no commit grant.
