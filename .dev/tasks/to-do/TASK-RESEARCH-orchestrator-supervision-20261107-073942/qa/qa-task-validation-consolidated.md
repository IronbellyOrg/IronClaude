# QA Task Validation: Consolidated Findings (task-builder A.10, cycle 1)

- Task file: `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/TASK-RESEARCH-orchestrator-supervision-20261107-073942.md`
- Sources:
  - `qa/qa-task-validation-structure-report.md` (phase-structure lens): VERDICT: FAIL, blocking B1-B4
  - `qa/qa-task-validation-b2-report.md` (B2 self-containment lens): VERDICT: FAIL, blocking B1-B10
- INV-002: both producer reports exist and both end with a `VERDICT:` line. No INV-002 events.
- Consolidated verdict: FAIL (13 unique blocking findings).

## Items Reviewed

| # | Source | Check | Result |
|---|---|---|---|
| S1 | structure | Frontmatter complete | FAIL (minor) |
| S2 | structure | Mandatory template sections | PASS (with note) |
| S3 | structure | Phase dependencies logical | FAIL (blocking: C1, C2) |
| S4 | structure | Phase ordering logical | PASS |
| S5 | structure | Completion items in final phase | PASS |
| S6 | structure | Task Log at bottom | PASS |
| S7 | structure | Item count reasonable (79) | PASS |
| S8 | structure | Open Questions documented | PASS |
| S9 | structure | M3/M4 QA gate patterns | FAIL (blocking: C4) |
| S10 | structure | TB-Add-1 placeholder scan | PASS |
| S11 | structure | TB-Add-3 clarification adjacency | PASS (inactive) |
| S12 | structure | TB-Add-4 DAG | PASS (with note) |
| S13 | structure | TB-Add-5 granularity | FAIL (minor) |
| S14 | structure | TB-Add-6 format consistency | FAIL (minor) |
| S15 | structure | TB-Add-7 source areas | PASS (with note) |
| S16 | structure | TB-Add-8 per-item evidence binding | FAIL (minor) |
| S17 | structure | HALT / Frontmatter Update Protocol consistency | FAIL (blocking: C3) |
| B2-1 | self-containment | All 5 B2 components per item | FAIL (blocking: C6) |
| B2-2 | self-containment | No "see above" references | FAIL (blocking: C5, C6, C7) |
| B2-3 | self-containment | Agent prompts fully embedded | FAIL (blocking: C5, C8) |
| B2-4 | self-containment | Specific file paths | FAIL (blocking: C7, C8, C11) |
| B2-5 | self-containment | Measurable verification | FAIL (blocking: C9, C10, C13) |
| B2-6 | self-containment | No batch items | PASS (with notes) |
| B2-7 | self-containment | No items built on contradicted findings | PASS (with notes) |

## Blocking findings (deduplicated; these go to the fix agent)

| ID | Sources | Location (task file) | Defect | Required fix |
|---|---|---|---|---|
| C1 | structure B1, self-containment B5 | Phase 5 note l.202; Step 5.4 l.216; Step 5.5 l.220-222 | 5.5 (Implementation Plan) runs in parallel with 5.4 (Options and Recommendation) and hard-codes the A1 shape (CLI registration in main.py), so it can contradict the recommendation. | Take 5.5 out of the parallel batch; run it after 5.4; have it read `synthesis/synth-04-*.md` and plan the option 5.4 recommends. Update the l.202 "all six independent" note. |
| C2 | structure B2, self-containment B5 | Step 5.5 | 5.5 does not read `gaps-and-questions.md`, `research/scope-02-*`, `research/05-orca-row-schema.md`, `research/06-orca-open-questions.md`, synth-02 or synth-04, yet three gates require every Section 4 gap to map to a Section 8 step or Section 9 entry. | Add those inputs (absolute paths) to 5.5's read list. |
| C3 | structure B3 | Frontmatter Update Protocol l.98-100; HALT paths l.180, 260, 310, 324, 338 and 7.5 | HALT paths set `blocker_reason` but never `status: "Blocked"`; the protocol allows status edits only in 1.1 and 7.6 and does not list `blocker_reason`. | Extend the protocol: any HALT item may set `status: "Blocked"` and `blocker_reason`. Add the status set to every HALT path. |
| C4 | structure B4 | Step 6.7 l.312-324 | The fidelity gate has no cross-source-contradictions agent (template PG.6); contradictions between the report and BUILD-REQUEST, the brainstorm or the issue sources go unchecked. | Add a fully embedded cross-source-contradictions agent item to 6.7 with absolute input and output paths, its own severity scale and a `VERDICT:` line rule. |
| C5 | self-containment B1 | Step 6.7b l.330, 332, 334 | Anti-omission agents 2-4 reuse agent 1's prompt by reference. | Copy agent 1's full prompt (checklist, method, severity scale, verdict rule, output path) into each item, changing only the section range and output file. |
| C6 | self-containment B2 | Cycle-control items l.180, 260, 310, 324, 338 | They re-run earlier items by reference, never spell out the -cycleN file names, and lack an "ensuring ..." clause. | In each, name the exact earlier Step and its exact cycle-N input and output paths (e.g. `${TASK_DIR}qa/qa-fidelity-consolidated-cycle1.md`, written as absolute paths), and add a measurable verification clause (file exists, ends with `VERDICT:`, blocking count recorded for the monotonicity check). |
| C7 | self-containment B3 | Steps 5.1-5.6 l.206-226 | Prompts contain the literal placeholder "[the phase context above]" and use `${TASK_DIR}` and bare relative paths. | Replace the placeholder with the actual context text and write every input and output as an absolute path under `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`. |
| C8 | self-containment B4 | Fix and verifier prompts l.178, 258, 308, 322, 324, 336, 338 | Relative `qa/...` paths; verifiers 324 and 338 do not name the report; qualitative verifiers 178, 258, 308 are described, not given a prompt. | Give each spawned agent a full prompt with the task directory and the absolute paths of the report, the consolidated findings file and its output file. |
| C9 | self-containment B6 | Step 7.5 l.356 | Reflect gate diffs `{BASE}..HEAD` with BASE from `git merge-base HEAD master`; the task never commits, and the stale local master makes the diff hold unrelated commits #410-#420. | Point the reflect gate at the task folder or an explicit file list of task outputs; do not use `merge-base HEAD master`. |
| C10 | self-containment B7 | Step 1.2; Step 7.3(f) l.350 | No `git status --porcelain` baseline exists, so 7.3(f) cannot tell task changes from the pre-existing untracked `.dev/brainstorms/...` and `.dev/issues/339/`. | In 1.2, write `git status --porcelain` to `${TASK_DIR}baseline-git-status.txt` (absolute path); make 7.3(f) compare against that file. |
| C11 | self-containment B8 | Step 2.3 l.130; Step 2.6 l.142 | 2.3 cites the non-existent `tests/core/test_routing_refresh.py`; 2.6 labels WORKER-CONTRACT.md lines 133-136 "frozen worker" though they describe a frozen /sc:implement plan (decision D2). | Use `tests/recommend/test_routing_refresh.py`; relabel the 2.6 citation "frozen /sc:implement plan (D2)". |
| C12 | self-containment B9 | Step 6.7b l.328, 336 | Verdict rule "PASS (0 omitted)" and the fix item make every omission blocking, contradicting the rule that minor findings never fail a gate. | Omitted load-bearing finding = blocking; omitted wording-level detail = minor note. Verdict rule: "PASS when 0 blocking omissions". |
| C13 | self-containment B10 | Step 3.2.5 l.182; Step 5.6 l.226; 3.1 completeness agents | They expect `## Gaps and Questions` and "Key Takeaways" headings; the scope files use `## Open questions` and have no Key Takeaways. | Match the headings the research files actually use (`## Open questions`), and drop or relax the Key Takeaways requirement; or have Phase 2 require and verify both headings. |

## Minor notes (not sent to the fix agent; not rechecked)

- Structure M1: frontmatter lacks `autogen_method`, `spec_path`, reflect_pre `coverage_pct` / `depth` / `reviewed_at` (A.10.7 populates reflect_pre).
- Structure M2 / self-containment M2: `gaps-and-questions.md` and `reviews/` missing from the Handoff File Convention.
- Structure M3 / self-containment M3: Phase 7 items lack `**Step 7.N:**` labels; some Step headers cover several items.
- Structure M4 / self-containment M4: 6.7 and 6.7b merge consolidate+fix and verify+cycle control.
- Structure M5: no `Verify:` prefix; 7.5 uses a unique field layout.
- Structure M6: 72 items cite code surfaces with no file:line or evidence-absence comment.
- Structure I-7, I-9: Execution Context uses bullets, not template subsections; l.91 regex nuance.
- Self-containment M1: item 1.2 does not create `reflect/post/`.
- Self-containment M5: fidelity agents 2-4 lack a severity scale and verdict rule.
- Self-containment M6: `[N]` cycle placeholder defined only in the phase blockquote.
- Self-containment M7: orca-capabilities.md lines 148-151 labelled "peer sessions".
- Self-containment M8: 5.7 qualitative agents read only synthesis files.
- Self-containment M9: rf-qa phase names "report-lens-*" are not defined phases.

## Cycle log

- Cycle 1: consolidated 2026-11-07. Fix agent cycle 1: 13/13 fixes applied (qa/qa-task-validation-fix-cycle1.md). Verify cycle 1: PASS, 13/13 RESOLVED, 0 blocking (qa/qa-task-validation-verify-cycle1.md).
- Final A.10 structural verdict: PASS after 1 fix cycle (the VERDICT line below is the cycle-1 consolidation verdict, kept for the record).

VERDICT: FAIL
