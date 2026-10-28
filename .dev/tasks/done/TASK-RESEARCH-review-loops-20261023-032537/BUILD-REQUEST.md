# BUILD REQUEST

Source: skill-delegated
Calling Skill: tech-research
Task Directory: .dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/
Research Notes: .dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/research-notes.md
Research Notes Status: Complete
SKIP_RESEARCHERS: true

BUILD_REQUEST:
==============
GOAL: Investigate actual repeated final-review and per-task QA failure cycles in sc:workflow and sc:implement, beginning with the frozen latest 30 session logs. Produce a large local Markdown evidence deck and a final research report at .dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md. Exactly five evidence-backed candidate root causes must then be debated through the sc-adversarial-protocol skill and ranked most to least likely. No implementation changes.

WHY: The user reports fixes leading to more failures and wants causal analysis, not another speculative remediation loop. Distinguish introduced regressions, previously missed defects, repeated unresolved findings, moving criteria, and invalid findings. Do not assume all later failures are regressions.

TASK_ID_PREFIX: TASK-RESEARCH
TEMPLATE: 02
QA_INTENSITY: full

DOCUMENTATION STALENESS WARNINGS:
Current protocol sources have been directly Read and must not be treated as proof of historical executed bytes. Original logs show partial/advisory statuses, not always literal FAIL. Source artifacts include stale evidence lines and incomplete historical ledgers; nested reviewer logs sometimes preserve failures absent from ledger. These are investigated evidence gaps, not grounds to manufacture missing records. No code architecture claim sourced only from prose may drive a fix recommendation. All research remains read-only against production.

RESEARCH ASSIGNMENTS:
Read research-notes.md SUGGESTED_PHASES: six concrete session analysts and assigned output paths, all already running or completing from the scope-discovery wave. Do not duplicate them. Their six case files are research/01-session-ac2cd1fd.md,02-session-a9b88895.md,03-session-6f744b87.md,04-session-43582de1.md,05-session-e002bed2.md,06-session-0690ee9f.md. The full original session paths and exact investigation scopes are in the notes. If text-only handoff is required by an agent's higher-priority instructions, the main session persists it transparently and checks primary evidence; never claim a nonexistent file. Scope discovery has selected six sessions meeting repeated failed-review patterns, with additional fail-fix-pass controls recorded separately. Seven or more case incidents may exist because session15 has two packages, but count strict repeated-failure subset separately. Current-rule and all30 screening evidence also feed deck and synthesis. Do not count synthetic summaries, quoted commands, or recaps. Source screening-handoffs-source.txt and screening-recovery-source.txt preserve complete handoffs verbatim; recovered reports retain any historical incompleteness rather than masking it.

REQUIRED RESEARCH PROCEDURE:
1. Preserve the frozen manifest of 30 top-level session files, selected by mtime across all projects. Record every screened session, including negatives, synthetic/adviser sessions, resumed duplicates, and the excluded current investigation. Do not silently widen the population to reach the requested count.
2. Select 5-10 genuine instances if supported, with one dedicated deep analyst per selected SESSION LOG. A session can contain several distinct task incidents; keep session counts, incident counts, failed reviews, findings, and transitions separate. Deduplicate replayed/compacted/resumed material by task and actual event identity.
3. Each analyst reads the real session and linked tasklist, progress ledger, review reports, failure artifacts and diffs, as available. Retain exact JSONL line anchors, timestamps, short quotes and source paths. Trace failure -> proposed fix -> applied change -> subsequent review. Seeded instructions and loaded skill definitions are not observed events.
4. For each later finding classify: introduced by the fix; preexisting but first discovered later; previous finding not actually fixed; changed acceptance criteria/review scope; unsupported/invalid review finding; or unknown. Introduced-by-fix requires before/after evidence, not temporal order alone. For newly discovered findings explain why the prior review missed it if observable; otherwise explicitly unknown. Judge validity against the original acceptance criteria and historical artifact state, not only current code.
5. Separate evidence of an executed protocol violation from a weakness in the protocol itself. Current installed/source files establish today's behavior, not what an older run executed. Record loaded historical versions from session tool results when possible.
6. Build per-session case tables, a deduplicated cross-case transition matrix and an extensive evidence deck. Every causal claim names its mechanism, supporting and opposing cases, counterevidence and evidence strength. Missing historical artifacts and selection bias remain visible.
7. Deeply review all research artifacts and create exactly five root-cause hypothesis cards as local Markdown artifacts, using the research report template. Do not pad weak hypotheses to look certain. Each has supporting cases, disconfirming evidence, alternative explanations, scope, and a falsification test.
8. Invoke /sc:adversarial through its installed command/protocol skill on the five hypothesis files, depth deep, local output directory reviews/adversarial/. Debate the merits of EACH hypothesis. Preserve transcript, comparison/scoring and merged output. Use the result to rank the five by likelihood given this sample, not by artifact polish; report if causes overlap rather than treating them as exclusive. No fabricated probability percentages.
9. Final recommendation is evidence-backed and research-only. Do not alter production commands, skills, agents, tests, tasklists or investigated workspaces. Local Markdown only; retain every intermediate.

QA_GATE_REQUIREMENTS: PER_PHASE
Use the FULL-intensity gates and explicit per-agent checklist items from /config/.claude/skills/tech-research/SKILL.md Stage A.7, Phases 3,5,6, not prose-only checks. Research completeness: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative, partition when >6 research files; max3 fix cycles. Synthesis: 2 rf-analyst + 2 rf-qa + 1 rf-qa-qualitative, partition when >4 synth files; max2 fix cycles. Report: structural lenses (template, consistency, evidence, completeness), content lenses (actionability, numbers, crossreferences, domain accuracy), plus recommendation-feasibility, finding-reproducibility and implementation-concreteness; scale by report lines as skill prescribes, 11 for500-1500 lines. Every review report-only; consolidate, one authorized report-fix agent, independent verification; max3 cycles. Source fidelity after report gate: 2 agents, 3-4 if >1000 source lines, max2 fix cycles. Anti-omission after fidelity: 2 rf-analyst, 3-4 if >1000 input lines, exhaustive semantic enumeration, max2 fix cycles. Preserve all negative findings and corrections, binary PASS/FAIL, no invented defects or numerical finding quotas treated as evidence. Each agent first READs its governing template, writes a full section skeleton with placeholders, populates section by section. Research agents include documentation staleness protocol; QA prompts include adversarial stance. /task phase gates additionally apply as the skill requires. Research scope includes empirical logs; evidence limitations are valid findings to report, not an instruction to invent unavailable history.

VALIDATION_REQUIREMENTS: TEMPLATE_COMPLIANCE + EVIDENCE_TRAIL + CROSS_VALIDATION
TESTING_REQUIREMENTS: N/A, research Markdown only. Any extraction helper must validate its own input/output counts without modifying production code.

RESEARCH NOTES FILE:
.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/research-notes.md

SKILL CONTEXT FILE:
/config/.claude/skills/tech-research/SKILL.md

SKILL PHASES TO ENCODE IN TASK FILE:
Encode all tech-research Phases1-7 per its Stage A.7, with individual self-contained checklist items for every producer and reviewer. Phase1 preparation and status. Phase2 deep investigation: one dedicated analyst per selected session from research-notes assignments, current-rule verification as needed, then an evidence-deck assembler preserving every case and classification. Phase3 full research completeness gate, serialized report fixes, independent verification and gaps log. Phase4 gap-driven external research only: if no external source can resolve the remaining historical-evidence gaps, explicitly record N/A with rationale, do not invent generic web research. Phase5 synthesis with six section files, five hypothesis cards created only after reading all empirical reports; invoke sc:adversarial depth deep on those five files, output reviews/adversarial/, then finalize options/ranking sections from the actual debate outputs. Embed the installed command/protocol invocation and all mandatory debate phases, not an improvised debate. Run full synthesis QA and fix/verification gate. Phase6 dedicated rf-assembler final report; all full lens QA, serialized corrections and independent verification; source fidelity; exhaustive anti-omission. Phase7 present verified paths and root-cause ranking, update task status/completion date but do not move/archive/delete the directory. Skill downstream suggestions are non-blocking, no implementation authorized. Reports must distinguish session count, incident count and failure-transition count. Redact secrets from excerpts while retaining exact source locations. The user's requested final output is research and a ranking, not a ready-to-execute remediation tasklist.

TASK FILE LOCATION:
.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/TASK-RESEARCH-review-loops-20261023-032537.md

ESCALATION:
Research only. No production edits, task execution against investigated tasklists, commits, pushes, archiving, external publication, or deletion of intermediates. Missing historical artifacts remain explicit evidence limitations; do not fabricate them. The user requested local .md files, so do not publish an Artifact.
