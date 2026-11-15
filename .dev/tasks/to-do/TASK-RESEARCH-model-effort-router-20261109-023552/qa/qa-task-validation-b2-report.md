# QA Report - Task Integrity: Self-Containment

**Topic:** Issue 463 model-plus-effort routing research task
**Date:** 2026-11-09
**Phase:** task-integrity
**Fix cycle:** N/A
**Lens:** B2 self-containment only
**Fix authorization:** false
**Reviewed task:** `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/TASK-RESEARCH-model-effort-router-20261109-023552.md`
**Request:** `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/BUILD-REQUEST.md`
**Governing role:** `.claude/agents/rf-qa.md` (project-first), Task Integrity and Output Format/Confidence Gate sections.
**Governing template:** `.claude/templates/workflow/02_mdtm_template_complex_task.md`, full actual file read; B2/B3 and E4 govern the findings below. All task line references below refer to Reviewed task, not this report.

---

## Overall Verdict: FAIL

VERDICT: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item contains context, action, output, verification and completion gate | FAIL, VERIFIED | Read all 103 items across task lines 148-471. Item 3.1 at 170 lacks its concrete assigned corpus; item 5.1 at 231 delegates its inputs to prose; item 7.26 at 453 leaves the full completion contract outside the checkbox. See findings 1 and 2. |
| 2 | No unrepeated dependency on prior-item/surrounding context | FAIL, VERIFIED | Read partition definitions at task 168, 325 and 358 against consuming prompts 170-188, 327-338 and 360-366; read synthesis inventory 229 against items 231-249. The labels cannot resolve from the item alone. Finding 1. |
| 3 | Agent-spawning prompts fully embedded | FAIL, VERIFIED | Read task 453-469: literal Skill invocation and complete mandatory runner instructions live outside item 7.26. Long embedded prompts elsewhere do not cure that missing prompt. Finding 2. |
| 4 | Specific source/output file paths within items | FAIL, VERIFIED | Direct Read of items 3.1/3.2, 5.1/5.2, 6.19-6.22 and 7.15-7.19 shows partition aliases or external input lists instead of concrete per-item source bindings. Output basenames are generally specific, but that does not bind the missing inputs or the shared root. Finding 1. |
| 5 | Measurable verification, not vague "works" | PASS, VERIFIED | Full-item read found concrete evidence, coverage, claim-tracing, binary severity and actual on-disk completion criteria rather than mere "verify it works". Examples: task 2.3 at 158 separates forwarding from provider acceptance; 6.1 at 274 checks ten sections, source inventories, traces and placeholders. The missing attachment of 7.26's otherwise detailed gate is counted under findings 1/2, not invented as a third vague-verification defect. |
| 6 | No collapsed multi-worker/output wave | PASS, VERIFIED | Read every numbered item; Grep `^- \[ \]` counted 103 checklist items. Five local studies (154-162), three web studies (221-225), four synthesis files (231-237), assembler (274), separate review/fix/verification/fidelity/anti-omission items are individually encoded. Multi-input aggregation and one serialized gate fix writer are intentional required operations, not a substituted bulk worker wave. |
| 7 | No execution based on contradicted/unverified claims as established facts | PASS, VERIFIED | Read all task items plus BUILD-REQUEST. Items 2.2-2.5 require current source, staleness tags and bounded unknowns; web items 4.1-4.3 investigate unresolved external/provider facts. The assembler item 6.1 preserves explicit settings, configured Coder default, unmeasured quantities and source-inspected versus executed limits. This is research, not router implementation; unresolved research questions are not false architecture dependencies. |

## Summary
- Checks passed: 3 / 7.
- Checks failed: 4 / 7. Four failing dimensions describe two deduplicated defects, not four separate findings.
- Critical issues: 0. Important blocking issues: 2. Minor notes: 0.
- Issues fixed in-place: 0 (report-only authorization).
- All 103 task items were read. The task has detailed research prompts and measurable checks, but several input assignments depend on prose outside their items and the mandatory reflection prompt/completion contract is detached from its checkbox. These are loss-of-instructions defects under context-stripped execution, not wording complaints.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT (blocking) | Task items 3.1-3.10 (lines 170-188), 5.1-5.9 (231-249), 6.19-6.23 (327-338), 6.29-6.32 (360-366), and final fidelity items 7.15-7.19 (425-436) | Required source inventories exist in surrounding prose, not in the consuming prompts. For example, 3.1 says "assigned research partition A named above" while the actual five-file list is at line 168; 5.1 says "complete explicitly listed Phase 5 inputs" while its 15 named inputs are outside the item at line 229. Fidelity and anti-omission prompts similarly use F1-F4 and A1-A4 labels whose concrete lists are outside their items. A worker receiving only its item cannot determine the exact assigned corpus; listing all numbered files does not reconstruct discovery scopes, accepted targeted inputs or partition membership. This violates Template 02 B2/B3 and E4, not merely citation style: the required coverage boundary is missing from the dispatched action. | Restate each consuming item's concrete source paths and purposes in its paragraph, including applicable accepted additions and full report input. Bind the package root explicitly or use exact paths. For genuinely variable inputs, give an exact inventory artifact path plus deterministic selection/read instructions within the item. Keep partition coverage intact; do not merge workers or replace fixed source lists with vague discovery. Recheck every item stripped of surrounding prose. | 
| 2 | IMPORTANT (blocking) | Task item 7.26, line 453; external runner prompt 455-467; external owner/completion contract 469 | The checkbox ends at "Pass this complete installed dedicated-runner prompt ... flags:". Its literal Skill call, full runner pipeline, RUN_INCOMPLETE contract and load-bearing owner/artifact completion conditions are in a separate blockquote and paragraph. Template 02 B3 requires one independently executable paragraph, and E4 explicitly says workers see batch items, not surrounding text. A paragraph-only dispatch therefore loses the exact invocation and disk-verification completion gate, even though a human reading the whole task can find them. | Embed the complete runner prompt, required literal Skill invocation, verified binding instructions, owner prohibitions, malformed-result handling and authoritative artifact-based completion gate inside item 7.26 itself as one complete paragraph. Preserve actual Skill execution and every required structural wave; do not replace them with a summary or inline self-review. |

## Actions Taken
- Created this report as the full rf-qa Output Format skeleton before reviewing task content, then populated sections incrementally. Adopted project-first rf-qa and the B2-only lens; no repeated task-builder/tech-research setup or child agents.
- Read all 565 task lines and all 76 BUILD-REQUEST lines directly. The initial role/dispatch reads omitted bounds and exceeded the dispatch limit; subsequent reads use 38 lines or fewer. An overbroad transcript Glob also exceeded 40 output lines and was not repeated. These reviewer process lapses are disclosed, not attributed to the task under review.
- Independently extracted only session identifier/model metadata from `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/4f2959ff-d699-4669-ab2c-7b2bbe64401a.jsonl`: sole recorded assistant backend `gpt-6.1-sol`. Live `T1bModel01`, `T1bModel02`, `T1bModel03` respectively selected `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0`. Installed `ccsession-models.json:85-91` binds those slots to tier1b, confirming slot2 membership, not provider-internal identity or future routing. No message bodies, secrets or whole environment were emitted.
- Optional environment identifier lookup returned no values (exit 1). Recovered through coordinator-provided exact transcript location and independent metadata extraction. An initial Edit was correctly blocked pending a tracked Read of this report; Read it and retried through Edit, without bypass.
- Changed only this report. No source/test/configuration/input/installed-role/model-setting edits, tests, package/Python/UV/install commands, network research, paid requests, cleanup, commits, pushes or GitHub writes. Prior scope03 environment/build/27-dependency installation is retained, neither repeated nor cleaned up; this overall research run is not installation-free. Parent owns staging.

## Recommendations
Parent should read this report and the separate phase-structure review, consolidate real blockers, and authorize only one serialized document fix writer followed by independent verification. Repair the two missing-context defects without weakening research depth, the actual reflection Skill call, owner limits or the configured-default policy. No task execution or TASK_FILE_READY certification follows from this report; later research-alignment, qualitative and actual PRE gates remain the parent's responsibility.

## Confidence Evidence
- **Confidence:** "Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%"
- Calculation: 7 / (7 - 0) * 100 = 100.0%. VERIFIED means the check was investigated with direct tool evidence, not that the reviewed task passed it. Two verified blockers still require FAIL.
- **Tool engagement:** "Read: 79 | Grep: 1 | Glob: 3 | Bash: 14"
- Counts are the actual session tool-name metadata snapshot taken after evidence collection and initial findings/check-table edits, before final report population/readback and lifecycle messages. They include setup, model/role verification and recovery, not 79 distinct correctness assertions. Later report-maintenance calls are excluded from that snapshot. The metadata extractor emitted only model/tool names and counts, no message bodies. No web tools used.
- VERIFIED evidence bindings are the seven individually named Items Reviewed rows, grounded in direct task Reads and the observed Grep count of 103. Full actual Template 02 read completed through its final line 1519; project-first rf-qa and both complete task/request sources were read, not substituted with producer summaries.
- No UNCHECKED items. No UNVERIFIABLE B2 checks. Source implementation behavior, deployment/provider compatibility, actual future reflection executability and runtime tests were not certified by this narrow document review; they are not silently represented as verified research results.

## Self-Audit
Actively attempted to disprove both findings: the missing inventories really do exist in the surrounding task prose, and item 7.26's full runner text is present immediately afterward. That rescues a whole-document human reading, but does not satisfy Template 02's explicit item-only/session-rollover contract; neither affected paragraph instructs a worker to read a named inventory artifact that resolves its missing bindings. Long substantive local/web/synthesis prompts and the dedicated assembler are positive evidence, not grounds to waive the failures. Repeated instances of shared-context dependence were consolidated into one issue; the detached runner/completion contract is the second. No invented quota findings, no cosmetic blockers, no assumption that unresolved Jev/client/provider facts authorize implementation. Phase ordering, frontmatter and the other reviewer's structural additions were not substituted into this lens.

## QA Complete
B2-only independent review complete with two Important blocking findings, no input fixes and no task execution. Report artifact: `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/qa/qa-task-validation-b2-report.md`. Parent must consume the full artifact and merge it with the other independent review before any authorized fix/recheck or readiness decision. No source/runtime readiness, implementation or overall task completion is certified.
