# Tier 1 reflection card (UC-1, pre-execution)

Spec: .dev/tasks/to-do/TASK-WF-spec-20261108-181640/source.md (byte copy of .dev/brainstorms/346-diffgate/SPEC.md)
Tasklist: .dev/tasks/to-do/TASK-WF-spec-20261108-181640/TASK-WF-spec-20261108-181640.md (12 tasks, 4 phases)
Card source: inline orchestrator (UC-1 has no Wave 1C agent; requirements-analyst work done by the deterministic matcher artifacts/coverage.py)

## Coverage / acceptance section

- Pass 1 parsed IDs: 0 (the SPEC uses no R-/REQ-/SPEC-/T- labels). Pass 2 inferred rows: 35, all quote-pinned to source.md lines. coverage_degraded: parsed-sparse.
- coverage_pct_union: 0.80 (28 of 35 rows matched by the 0.6 containment rule). Unmatched rows: INF-004 (source.md:37), INF-006 (source.md:40), INF-007 (source.md:68), INF-021 (source.md:155), INF-023 (source.md:157), INF-025 (source.md:160), INF-027 (source.md:162).
- Manual read of the unmatched rows:
  - INF-006 GAP: source.md:40 requires deferred items to be "shown once at the end with the reviewer's own severity label and the sentence \"PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer's, unvalidated.\"". No task names that sentence; Task 4 (plan line 71) only says `check` writes `deferred.md`. Candidate Drift-risk / coverage gap.
  - INF-023 AUTHORIZED DEPARTURE: source.md:157 (UNATTENDED_VARIANTS edit of tests/skills/test_worker_contract.py) is deliberately not done; owner ruling at plan line 29 removes the variant's Unattended section, so the test stays unedited (Task 8).
  - INF-004, INF-021, INF-027: covered in paraphrase (Task 3 M1 "minor ids ... cannot own a hunk"; fixtures split across Tasks 1, 2, 4; Task 10 runs `make sync-dev` and `make verify-sync`). The string rule falls under 0.6 only because of paraphrase.
  - INF-007, INF-025: covered only in the plan's Constraints section, which the matcher does not scan. INF-007 (HOW-WE-WORK.md, WORKER-CONTRACT.md, installer not edited) has no acceptance check in any task; only spec-panel.md is checked (Task 6 `git diff --exit-code`).

## Root-cause / deviation section

- D1 (Authorized, owner ruling plan line 29): source.md:99 asks for a byte-identical `## Unattended mode`; the plan omits the section. Residual: the parent's Usage line 23 (src/superclaude/commands/spec-panel.md:23) still advertises `[--unattended] [--report-dir <dir>]`, and the SPEC's Review Loop bullet 1 and Diffgate bullet 1 (source.md:77 and source.md:91) still describe an `--unattended` default. The variant will advertise a mode it no longer documents; the plan records this as a residual instead of resolving it.
- D2 (Grounding gap): T10 (R3 reviser brief) is not covered by source.md section 4, which names only the two fix-cycle reviser briefs (source.md:189). Plan line 172 copies T10 unchanged and hands the decision to the coordinator.
- D3 (Necessary): Task 4 adds a `proxy_all` field the SPEC's subcommand table (source.md:108) does not list; it implements the owner counting decision and the SPEC's own fixture expectation "label proxy 5" (source.md:154).

## Structural / tech-debt section

- S1: Task 4 acceptance (plan line 77) hardens the SPEC's estimate "about 35 script tests" (source.md:242) into a floor of 35; a reviewer may treat this as over-specification.
- S2: Task 5 acceptance (plan line 87) calls `list_available_skills()` from `superclaude.cli.install_skill`; the import exists at src/superclaude/cli/install_skills.py:28.
- S3: Task 1 allows subcommand bodies to raise "not implemented" until Task 4; the interim state is scaffolding inside one plan, closed by Task 4's acceptance criteria.

## Self-reported confidence

0.80 (inline; to be blind-calibrated in Wave 1D).
