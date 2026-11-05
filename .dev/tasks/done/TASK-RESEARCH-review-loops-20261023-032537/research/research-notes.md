# Research Notes: Repeated workflow and implementation review loops

**Date:** 2026-10-23
**Scenario:** A
**Depth Tier:** Deep
**Status:** Complete (scope discovery; deep analysis and final report remain in progress)
**Governing template:** /config/.claude/skills/tech-research/SKILL.md, Stage A.4

---

## EXISTING_FILES
| Source | Purpose and observed size |
|---|---|
| research/session-manifest.txt | Frozen latest30 top-level JSONL membership across /config/.claude/projects/*/*.jsonl; original exact paths, index03 current session excluded. |
| research/screening-handoffs-source.txt | Exact preserved screening-agent text from transcripts for slices07-12,19-24,25-30, plus navigation/status from other agents. Includes source hashes/mtime and event anchors. |
| research/screening-recovery-source.txt | Exact preserved original report Write/Edit text and complete final handoffs for slices01-06 and13-18. No claim duplicated edits are separate events. |
| research/scope-01-recovered.md | Replayed original author edits, 15KB, four unfinished placeholders retained transparently; details for three selected sessions. Source text remains separately preserved. |
| research/scope-03-recovered.md | Replayed original author edits, 22KB, full findings for13-18. Apply later physical-line corrections from screening-recovery-source.txt. |
| src/superclaude/skills/sc-workflow-protocol/SKILL.md | Current73-line plan-generation/reflect/handoff protocol, directly Read. |
| src/superclaude/skills/sc-workflow-protocol/refs/quality-gates.md | Current41-line schema/coverage generation gate, directly Read. |
| src/superclaude/skills/sc-implement-protocol/refs/qa.md | Current90-line per-task rubric and managed FINAL, directly Read. |
| src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md | Current85-line managed plan pin/archive/final state rules; directly Read32-85. |
| src/superclaude/skills/sc-implement-protocol/refs/retry.md and refs/ledger.md | Current retry/ledger sources for case/historical comparison; rule-map agent investigated. |
| /config/.claude/skills/ equivalents | Installed rule surfaces; agent reports byte-identical current equivalents, source map to be persisted/checked. |
| /config/workspace/Coder/.claude/worktrees/orca-upstream-tracking/.dev/tasks/to-do/TASK-WF-designSpec-20261022-132541/ | Original plan/source, progress and artifacts spanning planning session20 and implementation sessions19/05. Main directly Read progress. |
| Same Coder worktree .dev/reflect/pre-designSpec-20261022133138/REPORT.md and pre-designSpec-v2-20261022150856/REPORT.md | Planning reviews16 then20 findings, with partial statuses. |
| /config/workspace/Coder/.claude/worktrees/issue-358-litellm-key-env/.dev/tasks/done/ | Surviving issue358InTempla151058 and issue358FollowUp193837/210638 packages, ledgers and evidence logs. |
| /config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/ | Claim-gate Task12 package, frozen corpus, complete review1/review2 artifacts and original criteria. |

No prior task-research folder on this exact topic was found in the initial to-do inventory. Existing retry-ladder designs are historical context, not a replacement for empirical investigation.

## PATTERNS_AND_CONVENTIONS
[CODE-VERIFIED: current protocol source, not historical execution] sc-workflow-protocol/SKILL.md:48-58 separates plan-generation checks from read-only advisory reflection; reflect findings do not change workflow success and may not automatically regenerate the plan. quality-gates.md:24-39 defines schema/coverage checks, not proof the actual semantic review passed. sc-implement-protocol/refs/qa.md:9-17 restricts per-task QA to original criteria/constraints and diff; :37-52 gives closed verdicts, :56-68 fix/stop/acceptance behavior. refs/managed-workspace.md:48-60 makes managed FINAL a fresh current-state archive gate and prohibits reopening tasks without operator authorization. Current-rule details and historical-version limits go into research/scope-rules.md.

[LOG-VERIFIED: directly Read original events] Coder session ac2cd1fd JSONL499 and821 show a plan can pass its generation gate yet still receive16 then20 substantive review findings after a revision. Original statuses are partial, not binary FAIL. Claim-gate session a9b88895 JSONL291 and450 shows successful test runs alongside semantic review failure, followed by three corrected findings and one unchanged original frozen-fixture issue. The latter is not proof of a fix-caused regression.

These are preliminary navigation facts only. Dedicated analysts must validate complete review artifacts and original criteria before root-cause synthesis.

## SOLUTION_RESEARCH
N/A: pure investigation, not implementation. No production changes, commits, pushes, or log modifications are authorized.

## RECOMMENDED_OUTPUTS
All paths relative to .dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/:

| Output | Purpose |
|---|---|
| research/session-manifest.txt | Frozen population of 30 logs, full original paths. |
| research/scope-01.md through scope-05.md | Six-session screening slices, including negative evidence. |
| research/scope-rules.md | Current review and retry protocol map, installed/source comparison. |
| research/01-session-<short-id>.md onward | One deep analyst report per selected session, chronological findings and causal classification. |
| research/evidence-deck.md | Deduplicated incident and review-transition tables with raw-source anchors. |
| gaps-and-questions.md | Historical evidence gaps and unresolved validity questions. |
| synthesis/synth-01-problem-current-state.md | Report sections1-2 from empirical cases and current rules. |
| synthesis/synth-02-target-gaps.md | Sections3-4, case classifications and mechanism gaps. |
| synthesis/synth-03-external-findings.md | Section5, gap-driven external context or justified N/A if historical logs resolve the question. |
| synthesis/synth-04-options-recommendation.md | Sections6-7, exactly five candidate root causes and evidence-backed ranking. |
| synthesis/synth-05-implementation-plan.md | Section8, proposed next checks/changes only, no code modifications. |
| synthesis/synth-06-questions-evidence.md | Sections9-10, limitations and full evidence index. |
| synthesis/hypothesis-01.md through hypothesis-05.md | Five individually evidence-backed hypotheses for the requested debate. |
| reviews/adversarial/ | Requested deep adversarial debate artifacts and merged ranking. |
| qa/ | Research, synthesis, final report, fidelity and anti-omission reviews. |
| RESEARCH-REPORT-review-loops.md | Final ten-section technical research report and ranked conclusions. |

## SUGGESTED_PHASES
Six selected sessions, each already assigned to its own dedicated root-cause analyst during focused scope discovery. The task should consume/verify those files rather than duplicate their research. Deep analysis is ongoing; scope discovery itself is complete.

| Agent | Session index and exact original file | Focus | Assigned output |
|---|---|---|---|
| case-orca-plan |20, /config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/ac2cd1fd-60f6-4b7c-942c-93026ea8edce.jsonl | Plan16 findings -> v2 ->20 -> v3 partial targeted recheck -> v4 not reviewed; distinguish semantic misses, introduced plan changes and partial old fixes. | research/01-session-ac2cd1fd.md |
| case-claim-oracle |27, /config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-auggie-claim-gate/a9b88895-5374-4cae-8ebb-cac03a97aff1.jsonl | Task12 frozen fixture/oracle, four findings -> three corrected one retained -> operator authorizes corpus fix -> pass. | research/02-session-a9b88895.md |
| case-doc-render |01, /config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/6f744b87-6508-4d3e-9e71-c1193fd2162d.jsonl | Task6 repeated cannot-verify render, evidence-only retry, unchanged failure, explicit acceptance; separate Task2 baseline dispute. | research/03-session-6f744b87.md |
| case-ci-plan |04, /config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl |18 initial plan concerns, user refactor, regenerated plan16fixed2partial plus new findings; live endpoint explicit. | research/04-session-43582de1.md |
| case-orca-monitor |05, /config/.claude/projects/-config-workspace-Coder--claude-worktrees-orca-upstream-tracking/e002bed2-7877-42c1-8665-8cb8595587b6.jsonl | Long repeated Task12 monitor fixes, new independent reviewers and protocol update, newly found failure paths, huge argv limit, provenance constraints. | research/05-session-e002bed2.md |
| case-credential-finals |15, /config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866.jsonl | Two final-review incidents, one fail-fix-pass control and one fail-fix-fail-fix-pass; stale/blank citations, immutable ledger and acceptance, one missing ledger failure. | research/06-session-0690ee9f.md |

Mandatory deep analyst questions: original criterion, original failure, proposed and applied change, exact next review, validity, causal classification, why missed earlier if knowable, before/after evidence, negative controls and missing historical evidence. Cite raw physical JSONL lines/timestamps/UUIDs and artifact file lines; original reviewers/nested copies are one event. If an agent has a higher-priority no-report-write restriction, main persists its complete returned text, explicitly records this limitation and checks sources independently. Never falsely call a text-only handoff a producer-written file.

Evidence-deck assembly consumes all six reports plus screened negatives and rule map. Synthesis files follow RECOMMENDED_OUTPUTS. Exactly five hypotheses arise only after reading the complete empirical reports, then sc:adversarial deep debates their evidentiary merits and ranks likelihood. External research is gap-driven: historical event gaps cannot be answered by generic web advice, so record N/A if no genuine external question remains. Full skill gates remain as in BUILD-REQUEST.md. Do not launch duplicate scope/deep analysts for work already running.

## TEMPLATE_NOTES
Template 02 for the research task. Research reports and review reports derive from the loaded tech-research skill templates. The user explicitly requests local Markdown files, not publication.

## AMBIGUITIES_FOR_USER
None. Intent is clear. The latest 30 top-level session logs across all projects under /config/.claude/projects are the population, ordered by file modification time at discovery. Nested subagent logs are supporting evidence, not independent sessions. The current investigation session cannot count as a positive case. Snapshot limits and duplicate/resumed sessions must be recorded.
