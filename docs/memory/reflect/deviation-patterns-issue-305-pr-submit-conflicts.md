# Reflect deviation patterns — issue-305-pr-submit-conflicts

## pre-design-20261104164711 (UC-1, issue #305 conflict-resolution plan, 2026-11-04)
- Recurring pattern: reviewers audit `Depends on` edges as if the executor schedules by graph, but `/sc:implement` runs tasks in document order and ignores depends-on (sc-implement-protocol SKILL.md:79, :97). Missing edges are then latent; the only execution-relevant fix is where a task sits in the document. Check the executor's ordering rule before grading edge findings Medium.
- Recurring pattern: an edge audit by named-artifact matching misses consumers that reach a function through a spec test-case ID (F10, F12) or a package `__init__` export list. Expand test-case IDs and export lists into the functions they use, then compute closures from the plan graph.
- New pattern: splitting a task (4 into 4a/4b) leaves stale "Task 4" references elsewhere in the plan (Depends-on lines and body text); rewrite every reference and re-check for cycles, because a re-pointed edge can close a loop.
- New pattern: plans copy small spec defects verbatim (a line range ending early: loop-guard.md:86-99 vs :103; a dropped docstring clause); a byte-for-byte spec check catches them, a coverage matrix does not.
- New pattern: acceptance criteria that read the git index (`git ls-files -s` mode 100755) cannot pass for files no task stages; prefer `test -x` or add an explicit staging step.
- Process note: three heterogeneous reviewers missed the cycle and the import-before-definition risk in their own consensus fix; the Round 2.5 invariant probe found both. Keep the probe at standard depth.
