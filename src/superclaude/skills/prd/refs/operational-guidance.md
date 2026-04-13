## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism.

1. **Codebase is source of truth.** For claims about what the product currently does, code overrides documentation. Web research supplements with market context but never overrides verified code findings. Internal documentation is treated with the same skepticism as external sources unless code-verified.

2. **Evidence-based claims only.** Every finding must cite actual file paths, feature names, capability descriptions. No assumptions, no inferences, no guessing. If you can't verify it, mark it as "Unverified — needs confirmation."

3. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps. This keeps web research focused and efficient.

4. **Documentation is not verification.** Internal documentation (design docs, architecture docs, READMEs in `docs/`) describes intent, history, or planned state — NOT necessarily current state. A doc saying "Feature X exists" does not prove Feature X exists. Only reading actual source code proves it. Doc Analyst agents MUST cross-validate every product claim against actual code using the Documentation Staleness Protocol.

5. **Preserve research artifacts.** Research, web research, and synthesis files persist after the document is written. They serve as the evidence trail for all claims and enable future re-investigation without starting from scratch. Do NOT delete research files, synthesis files, or the gaps log after assembly.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections to build a coherent picture across product areas.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, flag it explicitly in Open Questions. Do not silently pick one interpretation and present it as fact.

8. **Quality gate mandate.** Quality gates are enforced at three points: after research (Phase 3 — rf-analyst completeness verification + rf-qa research gate, spawned IN PARALLEL), after synthesis (Phase 5 — rf-analyst synthesis review + rf-qa synthesis gate, spawned IN PARALLEL), and after assembly (Phase 6 — rf-qa report validation only, since the assembler already consolidated and the QA agent validates the final document with fix authorization). Skipping any gate compromises PRD quality.

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final PRD section by section. This is non-negotiable — one-shotting hits token limits and loses all accumulated work.

10. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE analyst and QA instances in parallel, each with an `assigned_files` subset. This prevents context rot when any single agent would need to hold too many files in context.

11. **Default to Heavyweight.** Unless the product scope is clearly answerable with a single feature and <5 user stories, use the Heavyweight tier. When in doubt, go deeper. PRDs that are too thorough are easy to trim; PRDs that are too shallow require full re-investigation.

12. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes a product capability that contradicts what the code shows, **the code is correct and the doc is stale**. Treat internal docs with the same skepticism as external blog posts unless code-verified.

13. **PRD must be actionable.** The final PRD should contain enough detail that a product team could begin planning from it. User stories must be specific with testable acceptance criteria. Technical requirements (Section 14) must cite actual file paths and architectural patterns — not vague statements like "the system should be scalable." Requirements must be prioritized. This is not a placeholder document.

14. **Anti-orphaning rule.** Task-completion items (status update, Task Log entry, frontmatter update) MUST be checklist items within the final phase of the task file, not in a separate Post-Completion section. This ensures they are executed by the F1 loop and not orphaned.

15. **No fabricating product capabilities.** Research agents document what EXISTS. Never invent features, user flows, or capabilities that aren't verified in code. Every product claim must be traceable to actual source code or verified documentation.

16. **No modifying source code.** Research agents READ code, they do not modify it. This skill produces documents, not code changes. Any code changes needed should be logged as follow-up items, not executed during PRD creation.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and capability descriptions
- User flows are traced end-to-end, not just entry points
- Integration points are mapped with actual technology names and versions
- Existing patterns identified that inform product design decisions
- Gaps are specific and actionable ("feature X doesn't handle case Y")
- Doc-sourced claims carry verification tags
- rf-analyst reports PASS with no critical gaps
- rf-qa research gate verdict is PASS

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system has a plugin architecture")
- Assumptions stated as facts ("this probably works by...")
- Missing gap analysis (everything seems fine — unlikely for non-trivial products)
- No cross-references between research files
- Doc-sourced claims reported without code verification tags — if a research file describes capabilities and the evidence trail only points to documentation files (no source code paths), the investigation is incomplete and must be redone with code cross-validation
- rf-analyst or rf-qa reports show FAIL with critical gaps
- User stories missing acceptance criteria or feature capabilities undocumented despite being in scope

### When to Spawn Additional Agents
- A research agent flags a gap that's critical to the product analysis
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated
- A new product area is discovered during investigation that wasn't in the original plan
- Web research reveals competitive features that need codebase verification
- rf-analyst or rf-qa identify coverage gaps requiring targeted investigation

---

## Artifact Locations

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst completeness report | `${TASK_DIR}qa/analyst-completeness-report.md` |
| Analyst synthesis review | `${TASK_DIR}qa/analyst-synthesis-review.md` |
| QA report (research gate) | `${TASK_DIR}qa/qa-research-gate-report.md` |
| QA report (synthesis gate) | `${TASK_DIR}qa/qa-synthesis-gate-report.md` |
| QA report (report validation) | `${TASK_DIR}qa/qa-report-validation.md` |
| QA report (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |
| Final PRD | `docs/docs-product/tech/[feature-name]/PRD_[FEATURE-NAME].md` |
| Template schema | `docs/docs-product/templates/prd_template.md` |

Research and synthesis files persist in the task folder — they serve as the evidence trail for claims in the PRD and can be re-used when the document needs updating.

---

## Updating an Existing PRD

When the user wants to update (not create) an existing PRD:

1. Read the current document to understand what's already covered
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the PRD in place
5. Update the Document Information table with the new Last Updated date
6. Update Document History with what changed

---

## Session Management

Session management is provided by the `/task` skill. Task files are located at `.dev/tasks/to-do/TASK-PRD-*/TASK-PRD-*.md` and research artifacts at `${TASK_DIR}research/`. On session restart, `/task` finds the task file, reads it, and resumes from the first unchecked item.
