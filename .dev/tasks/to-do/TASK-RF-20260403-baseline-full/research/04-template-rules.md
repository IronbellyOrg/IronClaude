# Research: Template Rules & Baseline Task Example Patterns

**Researcher:** r4 (Template & Examples)
**Status:** Complete
**Date:** 2026-04-02
**Sources:**
- `.claude/templates/workflow/02_mdtm_template_complex_task.md` (PART 1 rules)
- `.dev/tasks/to-do/TASK-RF-20260402-baseline-repo/TASK-RF-20260402-baseline-repo.md` (completed task)
- QA reports from `.dev/tasks/to-do/TASK-RF-20260402-baseline-repo/qa/` and `reviews/`

---

## 1. Key Template 02 PART 1 Rules

### A3 -- Complete Granular Breakdown

- Break down EVERY workflow phase into atomic, verifiable checklist items
- Create individual checklist items for EVERY file, component, or iteration
- NO high-level or bulk operations allowed -- everything must be granular
- Include exact file paths, specific requirements, and measurable outcomes
- **A4 extends this:** For ANY process involving multiple items: (1) pre-enumerate ALL items, (2) create individual checklist item for each specific item, (3) require incremental updates after each item, (4) include consolidation step only after all items complete

### B2 -- Self-Contained Checklist Items (CRITICAL)

Every checklist item MUST include all 6 elements:
1. **Context Reference with WHY** -- What file(s) to read and why that context is needed
2. **Action with WHY** -- What to do and why it needs to be done
3. **Output Specification** -- Exact output file name, location, content requirements, and template to follow
4. **Integrated Verification** -- An "ensuring..." clause specifying what must be verified (no fabrication, 100% accuracy from source)
5. **Evidence on Failure Only** -- Log to task notes ONLY if unable to complete
6. **Explicit Completion Gate** -- "Once done, mark this item as complete."

**Rationale (B1):** Session rollovers mean context from batch 1 will NOT be available in batch 3+. Each item must be independently executable.

**B3:** Each item should be ONE FULL PARAGRAPH (not multiple lines/bullets), verbose and explanatory.

**B5 Forbidden patterns:**
- Standalone "read context" items that produce no output
- Missing context references (no source of truth)
- Multi-line/bulleted checklist items
- Separate verification/confirmation items
- Overly granular items (e.g., "create directory" alone)
- Separate REMINDER blocks between checklist items

### L1-L6 -- Intra-Task Handoff Patterns

These patterns enable cross-item information flow via persisted artifact files in `.dev/tasks/TASK-NAME/phase-outputs/`.

| Pattern | When to Use | Key Rule |
|---------|-------------|----------|
| **L1 Discovery** | Explore codebase/data and produce structured findings | Discovery file IS the deliverable. Must be well-structured, machine-readable |
| **L2 Build-from-Discovery** | Create output based on a previous discovery item's findings | Reference BOTH discovery file path AND original source file path |
| **L3 Test/Execute** | Run a command, script, or test suite and capture results | Capture BOTH raw output AND a structured summary |
| **L4 Review/QA** | Assess quality by comparing against source materials | Produce structured verdict (PASS/FAIL) with specific findings -- never vague "looks good" |
| **L5 Conditional-Action** | Behavior depends on result of a previous item | MUST handle BOTH branches (success AND failure). Output always created regardless of branch |
| **L6 Aggregation** | Consolidate multiple previous outputs into a single report | Use Glob to find files dynamically -- don't hardcode file lists |

**L7 Common phase structures:**
- Discovery -> Build -> Review: `L1 -> L2 -> L4 -> L6`
- Build -> Test -> Fix: `K1/K2 -> L3 -> L5`
- Full Lifecycle: `L1 -> L2 -> L3 -> L5 -> L4 -> L6`

**Handoff directory convention:**
- `discovery/` -- Inventories, scans, findings
- `test-results/` -- Raw output, summaries
- `reviews/` -- Verdicts, assessments
- `plans/` -- Fix plans, next steps (conditional action outputs)
- `reports/` -- Consolidated reports (aggregation outputs)

### Other Critical Rules

- **E1-E4 (Checklist Structure):** Flat structure only, no nested checkboxes, no parent-before-child. Summary/parent checkboxes MUST come AFTER component items. Work flows TOP to BOTTOM only.
- **C1-C4 (Embedding):** Outputs, success criteria, verification, and completion are embedded INTO checklist items, never as separate sections.
- **D3:** NO checklist items may appear before Phase 1 begins.

---

## 2. Baseline Task Example Analysis (TASK-RF-20260402-baseline-repo)

### What Worked Well

1. **Exemplary B2 compliance:** All 37 checklist items are fully self-contained single paragraphs containing context reference, action, output specification, "ensuring..." verification clause, failure logging instruction, and "Once done, mark this item as complete." gate. The QA task-integrity check (26/26 PASS) confirmed this.

2. **Effective L-pattern usage across phases:**
   - Phase 2 used **L1 Discovery** (worktree-setup.md captures environment verification)
   - Phase 3 used **L3 Test/Execute** (pipeline-output.txt raw log + execution-summary.md structured summary)
   - Phase 5 used **L4 Review/QA** (9 individual compare-*.md verdicts) followed by **L6 Aggregation** (comparison-test2-vs-test3.md)
   - Phase 6 used **L4 + L6** again for TDD comparisons
   - Phase 7 used **L5 Conditional-Action** (keep worktree if FAIL, remove if PASS)

3. **A3/A4 granular enumeration:** Phase 5 individually itemized all 9 artifact comparisons (Steps 5.1-5.9) before aggregating in Step 5.10. Not a single "compare all artifacts" bulk item.

4. **Handoff file convention:** Well-organized subdirectories (discovery/, test-results/, reviews/, plans/, reports/) with clear naming that makes Glob patterns easy.

5. **Prerequisites section (informational only):** Documented all required inputs (Test 1 and Test 2 artifacts) with exact file paths, byte sizes, and field counts -- but as informational context, NOT as checklist items (following D3).

6. **Conditional completion (Step 9.3):** After QA fix, properly reads QA verdict and sets "Done" only on PASS, "Blocked" on FAIL. This is good L5 pattern application.

7. **Phase purpose blocks:** Each phase has a `> **Purpose:**` blockquote explaining what the phase accomplishes and which L-pattern it uses, providing orientation without being a checklist item.

8. **Task completed successfully:** Status "Done", all 37 items [x], overall verdict PASS, 14 comparison reviews produced, 18 artifact comparisons across 9 phases.

### Issues Found by QA Agents

1. **Anti-instinct failure reason misattribution (IMPORTANT, found by qualitative QA):**
   - Worker agent claimed "both tests FAILed due to fingerprint_coverage < 0.7" across 3 files
   - Reality: Test 2 failed on `uncovered_contracts=3`, Test 3 failed on `fingerprint_coverage=0.67 < 0.7`
   - The error propagated from `compare-anti-instinct.md` to `comparison-test2-vs-test3.md` to `full-artifact-comparison.md` to `e2e-test3-verdict.md`
   - **Root cause:** The "ensuring..." clause asked for accuracy but the worker fabricated a uniform failure reason instead of checking the gate logic
   - **Lesson for new tasks:** When comparison items involve pass/fail logic, the "ensuring..." clause should explicitly require reading the actual gate/threshold logic, not just the output values

2. **Unconditional "Done" status in Step 9.3 (IMPORTANT, found by task-integrity QA):**
   - Original Step 9.3 set status to "Done" without checking QA verdict
   - Fixed to be conditional on QA criteria report verdict
   - **Lesson:** Post-completion frontmatter updates MUST be L5 conditional-action items that read the QA verdict

3. **Empty execution log (MINOR, found by qualitative QA):**
   - All "Phase N Findings" sections said "No findings yet" despite 9 phases of work
   - **Lesson:** Either populate findings sections or add a note explaining no blockers occurred

### Structural Metrics

| Metric | Value |
|--------|-------|
| Total phases | 9 |
| Total checklist items | 37 |
| Handoff files produced | 25+ (discovery, test-results, reviews, plans, reports) |
| QA reports | 5 (task-integrity, qualitative, research-gate x2, final-validation) |
| QA fix cycles | 2 issues fixed in-place |
| Items per phase (range) | 2-10 |
| Longest item | ~350 words (Phase 5/6 comparison items) |

---

## 3. Patterns to Apply to New Task Files

### Must-Have Patterns from Template

1. **B2 single-paragraph format** for every checklist item with all 6 elements
2. **L-pattern selection** based on item purpose (discovery, build, test, review, conditional, aggregate)
3. **A3/A4 granular enumeration** -- enumerate ALL items individually, then aggregate
4. **Handoff file convention** with subdirectories organized by purpose
5. **E1-E4 flat structure** -- no nested checkboxes, summary items come last
6. **C1-C4 embedding** -- no separate Outputs, Verification, or Success Criteria sections

### Lessons from Baseline Task QA Issues

1. **Comparison items should specify gate/threshold source:** When asking an agent to assess pass/fail, include the source file for threshold logic in the context reference (e.g., "read gates.py to understand failure conditions")
2. **Post-completion frontmatter must be conditional:** Step 9.3 pattern should always be L5 (read QA verdict, then branch)
3. **Execution log expectations:** Either plan for findings entries or preemptively note "no blockers" pattern

### Task Size Reference

The baseline task (37 items, 9 phases) is a good reference for a complex E2E test task. For the new baseline-full task (which aggregates test results rather than running new pipelines), expect:
- Fewer phases (no environment setup or pipeline execution)
- More L4 Review/QA and L6 Aggregation items
- Similar B2 verbosity requirements per item
