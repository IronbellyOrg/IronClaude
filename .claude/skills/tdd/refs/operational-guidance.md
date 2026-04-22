## Critical Rules (Non-Negotiable)

These are SKILL-SPECIFIC content rules that apply across ALL phases. Violations compromise document quality.

Three execution-discipline rules (task-file-source-of-truth, maximize-parallelism, use-dedicated-tools) are enforced by the `/task` skill and do not appear here. The incremental-writing mandate is retained as Rule 9 below because it is a content-quality requirement specific to this skill's multi-agent research pipeline, not just an execution mechanism.

1. **Codebase is source of truth.** For claims about current architecture, code overrides documentation. Web research supplements with technology context but never overrides verified code findings.

2. **Evidence-based claims only.** Every finding must cite actual file paths, class names, function signatures. No assumptions, no inferences, no guessing. If you can't verify it, mark as "Unverified — needs confirmation."

3. **Gap-driven web research.** Do not web search everything up front. First investigate the codebase thoroughly (Phase 2), identify specific gaps, then target web research (Phase 4) at those gaps.

4. **Documentation is not verification.** Internal documentation describes intent or historical state — NOT necessarily current state. A doc saying "Service X exists at path Y" does not prove Service X exists. Only reading actual source code proves it.

5. **Preserve research artifacts.** Research, web research, and synthesis files persist after the document is written. They serve as the evidence trail for all claims.

6. **Cross-reference findings.** When one agent's findings reference another agent's domain, note the cross-reference explicitly. The synthesis phase relies on these connections.

7. **Report all uncertainty.** If something is unclear, ambiguous, or requires a judgment call, flag it explicitly. Do not silently pick one interpretation and present it as fact.

8. **Quality gate mandate.** Quality gates are enforced at three points: after research (Phase 3 — rf-analyst completeness verification + rf-qa research gate, spawned IN PARALLEL), after synthesis (Phase 5 — rf-analyst synthesis review + rf-qa synthesis gate, spawned IN PARALLEL), and after assembly (Phase 6 — rf-qa report validation only, since the assembler already consolidated and the QA agent validates the final document with fix authorization). Skipping any gate compromises TDD quality.

9. **No one-shotting documents.** Agents must write incrementally as they discover information. The assembler must write the final TDD section by section. This is non-negotiable — one-shotting hits token limits and loses all accumulated work.

10. **Default to Standard.** Unless the component is clearly documentable with a quick scan of <5 files, use the Standard tier. When in doubt, go Standard.

11. **Docs-vs-code has the same trust hierarchy as web-vs-code.** Rule 1 establishes that web research never overrides code. The same applies to internal documentation: if a doc describes an architecture that contradicts what the code shows, **the code is correct and the doc is stale**. Treat internal docs with the same skepticism as external blog posts unless code-verified.

12. **Design specifications must be actionable.** Architecture, data models, and API specifications should contain enough detail that an engineer could begin implementation from the TDD alone. Include specific file paths, code patterns to follow, and integration points.

13. **Anti-orphaning rule.** Task-completion items (status update, Task Log entry, frontmatter update) MUST be checklist items within the final phase of the task file, not in a separate Post-Completion section. This ensures they are executed by the F1 loop and not orphaned.

14. **Partitioning thresholds.** When >6 research files exist (Phase 3) or >4 synthesis files exist (Phase 5), spawn MULTIPLE analyst and QA instances in parallel, each with an `assigned_files` subset. This prevents context rot when any single agent would need to hold too many files in context.

---

## Research Quality Signals

### Strong Investigation Signals
- Findings cite specific file paths and line numbers
- Data flow is traced end-to-end, not just entry points
- Integration points are mapped with actual function signatures
- Existing patterns identified that can inform the design
- Gaps are specific and actionable ("function X doesn't handle case Y")
- Doc-sourced claims carry verification tags
- rf-analyst completeness report shows PASS verdict
- rf-qa research gate shows PASS

### Weak Investigation Signals (Redo)
- Vague descriptions without file paths ("the system uses a plugin architecture")
- Assumptions stated as facts ("this probably works by...")
- Missing gap analysis (everything seems fine — unlikely for non-trivial systems)
- No cross-references between research files
- Doc-sourced architectural claims reported without code verification tags
- rf-analyst or rf-qa reports show FAIL with critical gaps
- Data model shapes undocumented despite being in scope

### When to Spawn Additional Agents
- A research agent flags a gap that's critical to the design
- Two agents' findings contradict each other — need a tie-breaker investigation
- The scope turns out larger than initially estimated
- A new subsystem is discovered during investigation that wasn't in the original plan
- Web research reveals patterns that need codebase verification

---

## Artifact Locations

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}${TASK_ID}.md` |
| Research notes | `${TASK_DIR}research-notes.md` |
| PRD extraction file | `${TASK_DIR}research/00-prd-extraction.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[topic].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Gaps log | `${TASK_DIR}gaps-and-questions.md` |
| Analyst reports | `${TASK_DIR}qa/analyst-[gate]-report.md` |
| QA reports | `${TASK_DIR}qa/qa-[gate]-report.md` |
| QA report (qualitative review) | `${TASK_DIR}qa/qa-qualitative-review.md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[topic].md` |
| Final TDD | `docs/[domain]/TDD_[COMPONENT-NAME].md` |
| Template schema | `src/superclaude/examples/tdd_template.md` |

Research and synthesis files persist in the task folder — they serve as the evidence trail for claims in the TDD and can be re-used when the document needs updating.

---

## PRD-to-TDD Pipeline

When a PRD is provided as input, the TDD creation follows an enhanced flow:

1. **PRD Extraction** (Step 1.2) — read the PRD and extract requirements, constraints, success metrics, and scope boundaries into `${TASK_DIR}research/00-prd-extraction.md`
2. **Requirements Traceability** — every requirement in the TDD's Section 5 should trace back to a PRD epic or user story where applicable
3. **Success Metrics Alignment** — TDD Section 4 (Success Metrics) should include engineering proxy metrics for business KPIs defined in the PRD
4. **Scope Inheritance** — TDD Section 3 (Goals & Non-Goals) inherits scope boundaries from PRD Section 12 (Scope Definition)
5. **Cross-referencing** — the TDD frontmatter's `parent_doc` field links back to the PRD

This pipeline ensures that product requirements are faithfully translated into engineering specifications without information loss or scope drift.

---

## Updating an Existing TDD

When the user wants to update (not create) an existing TDD:

1. Read the current document to understand what's already covered
2. Research only the changed/new areas (don't re-research everything)
3. Write new research files for the changes: `${TASK_DIR}research/update-[date]-[topic].md`
4. Edit the relevant sections of the TDD in place
5. Update the Document Information table with the new Last Updated date
6. Update Document History with what changed

---

## Session Management

Session management is provided by the `/task` skill. Task files are located at `.dev/tasks/to-do/TASK-TDD-*/TASK-TDD-*.md` and research artifacts at `${TASK_DIR}research/`. On session restart, `/task` finds the task file, reads it, and resumes from the first unchecked item.
