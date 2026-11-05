# Research: Review and retry rule map

**Investigation type:** Protocol source analysis
**Scope:** Current workflow and implementation protocols, installed and checkout copies
**Status:** Complete (current protocol map and recovered historical loads; execution remains case-specific)
**Date:** 2026-10-23
**Governing template:** tech-research/SKILL.md, Codebase Research Agent Prompt
**Handoff limitation:** Assigned agent is forbidden by its higher-priority instructions from writing reports. Main session persists returned evidence and verifies primary sources.

## Source Inventory and Provenance
Seven source/installed file pairs were SHA256-compared by the dedicated analyst; all match at inspection. Original full handoff is in agent-ascope-review-rules-0cb52ca63dfedc7b.jsonl:79 under this investigation's subagents directory; main read the complete returned text. Main additionally directly read the four sources discussed below.

| Source under src/superclaude/skills/ | Reported lines | Role |
|---|---:|---|
|sc-workflow-protocol/SKILL.md|72 (main Read73 physical lines)|Planning/reflection/handoff. Counting convention differs by trailing newline, not a proven content divergence.|
|sc-workflow-protocol/refs/quality-gates.md|41|Generation checks.|
|sc-implement-protocol/SKILL.md|175|Task execution loop.|
|sc-implement-protocol/refs/qa.md|90|Per-task and managed FINAL rubric.|
|sc-implement-protocol/refs/retry.md|451|Escalating task attempts and revert.|
|sc-implement-protocol/refs/ledger.md|242|Append-only progress and resume.|
|sc-implement-protocol/refs/managed-workspace.md|85|Pinned package, state-based FINAL/archive.|

Installed pairs replace the source prefix with /config/.claude/skills/. Graph coverage best-effort only; conclusions come from direct sources, not graph completeness.

**Key Takeaways**

- The seven source/installed comparisons describe their observation, not historical execution.

## Workflow Review Rules
[CODE-VERIFIED: executable agent instruction source, not runtime proof] src/superclaude/skills/sc-workflow-protocol/SKILL.md:48-58 separates the generation gate from advisory pre-reflection. Wave3 checks schema-min or full generation rules. Wave4 invokes reflect pre against source.md and the plan, without remediation. Line58 explicitly forbids editing/deleting/regenerating the plan from findings and preserves workflow status. A user-authorized later revision/re-review is a separate action, not a built-in automatic workflow retry loop. Lines70-72 reiterate no product code, Task fan-out, or plan modification from reflect findings.

src/superclaude/skills/sc-workflow-protocol/refs/quality-gates.md:24-39 defines quick schema checks versus standard/deep coverage checks. Full includes every source requirement covered by a task, but the source here describes an agent-performed check, not an executable semantic proof. A plan that passes this generation check can still receive substantive semantic review findings, as directly observed at Coder session ac2cd1fd JSONL499. Line41 says a generation-gate failure stops and deletes only its own draft; this is not authorization for this research to delete anything.

The main session directly Read both current source files. Do not conclude historical sessions obeyed or loaded these exact bytes without historical log evidence.

**Key Takeaways**

- Generation checks and advisory semantic readiness are separate; later user-authorized plan edits are separate actions.

## Implementation Review and Retry Rules
[CODE-VERIFIED: protocol source, runtime execution not established] src/superclaude/skills/sc-implement-protocol/refs/qa.md:9-17 limits task review input to original task brief, acceptance criteria, constraints and produced diff. Line11 allows exactly one reviewer per review, no code-quality ensemble or reflect. Lines27-33 require concrete evidence citations; absent citations become cannot-verify. Lines37-52 define the closed per-task verdict enum and precedence. Lines56-68 allow one initial fix/review, later bounded retry behavior through retry.md, and informed scoped user acceptance without relabeling an unmet requirement compliant.

qa.md:82 requires a fresh managed FINAL reviewer against current full plan/ledger/delivery files, not copied historical ledger citations. It distinguishes moved line numbers from real unmet criteria and allows artifact logs for final evidence. A later change contradicting prior compliance is an issue; accepted unchanged gaps remain honestly unmet. qa.md:86-90 always makes rerun/operator/escalated reviews independent subagents and excludes adviser briefs/retry folders from per-task review evidence. Independence protects against anchoring, but by itself does not ensure exhaustive first-pass coverage; empirical cases must establish any omissions.

src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:42 pins the plan/source after the first task start, so a conflicting frozen task cannot simply be silently rewritten. Lines48-60 require joining writers, state-digest collection, fresh review, rehash and discard/repeat if state changed. A FINAL issues result stops archive and must not reopen tasks without operator direction. Lines82-85 explicitly distinguish protocol-only controls from helper enforcement and state that concurrent non-cooperating writers are unsupported. The delivery digest does not cover task-owned artifacts or delivery files omitted from the ledger.

The main session directly Read qa.md and managed-workspace.md:32-85. The dedicated analyst's complete retry summary is retained below with source pointers; do not treat its current-rule map as evidence that any historical run executed those exact bytes.

**Key Takeaways**

- Per-task QA, retry and managed FINAL have distinct evidence and stopping rules; current source is not historical execution proof.

## Historical Versus Current Rules
The dedicated rule-map analyst reports: retry.md:142-146 permits initial implementation, one ordinary fix, three changed-approach attempts (five planned reviews), bounded advisers, and one reviewer respawn per review. These are not a lifetime cap across operator reinvocations or archive attempts. ledger.md:148-158 routes terminal halts through fresh operator review, not re-entry into the automatic ladder. Earlier unrecorded advice can be regenerated. A changing archive state discards FINAL and repeats the gate.

History preservation is substantial but not a stable finding-resolution registry binding later reviewers: failed-attempt evidence is saved starting after the ordinary fix fails, adviser artifacts may be overwritten before durable advice records, and completed tasks are skipped. Plan/source immutable after first task start (managed-workspace.md:42). Scope/classification must use exact historical loaded bytes before calling an old action a current-protocol violation.

The snapshot-based retry revert domain is broader than executor-declared touched files outside fixed exclusions (retry.md:148-178). A valid Q0 snapshot protects prior work; it is not concurrent-writer coordination. ledger.md:142 assumes a single writer. Managed reference:84 explicitly calls concurrent non-cooperating writes unsupported. Today's helper enforcement is not independently certified here; this is a protocol map.

**Key Takeaways**

- Current attempt limits do not prove the exact historical rules loaded by a reviewer.

## Recovered historical loaded-rule mapping

These are observed loads of `/config/.claude/skills/sc-implement-protocol/refs/qa.md`, not versions inferred from the current installed file. Full decoded texts are retained once in `historical-review-rules.json`, records.before and records.after. Removing the Read tool's displayed line-number prefixes from each original result recovers the captured text; hashes below are SHA-256 of that decoded content, not raw JSONL bytes.

| Loaded version and review | Original physical source and load timestamp, UTC | Captured-content SHA-256 | Material historical rule |
|---|---|---|---|
| Earlier rubric; credential follow-up second FINAL, result record 116 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-acf0a51e6992c50ee.jsonl:18`; `2026-10-22T20:26:30.085Z` | `0b533765d43a7adc90987581892a0bca849cc19a53638b556b6aba62d425d083` | Captured rubric:65 prohibits executor-written rulings and requires an operator-supplied record; :79 makes missing, stale or unverifiable evidence issues. |
| Later rubric; credential follow-up third FINAL, result record 155 | `/config/.claude/projects/-config-workspace-Coder--claude-worktrees-issue-358-litellm-key-env/0690ee9f-c2f6-40ef-96be-1a0913a37866/subagents/agent-a4bfff371c63a6c39.jsonl:18`; `2026-10-22T20:32:19.277Z` | `faff03b7b94ca2b70f9b25c35dcefd52636b7df8f7bf9a110c0a956a78d2e7d5` | Captured rubric:66-68 permits executor recording of actual scoped user acceptance, retaining the noncompliant verdict; :82 requires current-file/artifact-log evidence and explicitly rejects moved line numbers alone as issues. |

Case link: `06-session-0690ee9f.md`, Review-policy changed before the final pass and Complete third-final eight-observation disposition. The passing third review follows both evidence corrections and a changed rubric; the updater and each change's independent causal effect remain unknown. Do not assign either recovered version to other historical reviews without their own load evidence. The monitor's separately observed migration is traced in `05-session-e002bed2.md`, A mid-run protocol migration reopened a successful check, using original Raw 42/58 and 874/884/893/902; this mapping does not invent missing hashes or a universal version timeline.

**Key Takeaways**

- Two exact historical rubric loads are available; unobserved versions and update authorship remain unknown.

## Key Takeaways

- Advisory plan review, per-task QA and managed FINAL have different scopes and stop semantics.
- Original criteria are fixed, but current rules do not guarantee different reviewers interpret them identically or that earlier checks were exhaustive.
- Five planned attempts do not cap every operator-authorized resumption or archive re-review.
- Current FINAL explicitly rejects moved line numbers alone as issues; historical citation-only rejection must be dated against the rule then loaded.

## Gaps and Questions

Two recovered historical QA loads are mapped above and linked to the credential case. Historical versions without load evidence, actual protocol compliance and finding validity remain case-specific. No executable archive helper was inspected or run by this rule-map agent. Snapshot restoration is not safe concurrent-writer coordination. The rule-map alone does not prove any observed loop cause.

## Stale Documentation Found

No source/installed divergence in seven compared pairs at observation. A trailing-newline line-count difference is not content drift. Historical staleness remains case-specific.

## Summary

Current protocols fix acceptance criteria, preserve retry history and prohibit automatic reopening after FINAL issues. Their bounded task ladder coexists with fresh reviews on operator resume, archive attempts and state changes. Match empirical loops to exact reviewer inputs, ledger state and historical loaded sources before attributing a mechanism.
