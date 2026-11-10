# Tier 1 reflection card (UC-1, pre-execution)

Spec: .dev/tasks/to-do/TASK-WF-spec-20261108-181543/source.md (261 lines, sha cc668ff2...)
Tasklist: .dev/tasks/to-do/TASK-WF-spec-20261108-181543/TASK-WF-spec-20261108-181543.md (8 tasks, 4 phases)
Hypothesis source: inline orchestrator card (root-cause-analyst not spawned for UC-1; UC-1 Wave 1C uses the coverage map)

## Coverage / acceptance (qa slice)

- Pass 1 parsed IDs: 0. Pass 2 inferred rows: 142, all quotes valid against their cited lines (artifacts/inferred-requirements.yaml).
- Deterministic containment matching (threshold 0.6): 104 of 142 matched; coverage_pct_union 0.7324; coverage_pct null (parsed-only denominator 0); coverage_degraded: parsed-sparse.
- 38 unmapped rows (artifacts/coverage-matrix.json), triaged by hand:
  - 21 are outside the plan's declared scope (plan line 19 limits scope to source.md sections 3 and 4): problem/evidence (INF-002, INF-003 at source.md:11-12), review-status note (INF-001, source.md:5), growth arithmetic and residual-risk notes (INF-055, INF-056, INF-057, source.md:69-77), later adopters (INF-109, source.md:158), the whole section 5 measurement plan (INF-124 to INF-137, source.md:191-206), risk-table rows (INF-138, INF-139, source.md:224-227), replay harness (INF-140, source.md:238) and fold-back (INF-142, source.md:248).
  - 16 are in-scope rows that the plan covers in different words (lexical ratio 0.17-0.59): INF-005 (E-FIXCHECK-MISSING, plan Task 5 acceptance), INF-008 (refs, Task 1 parse_fixbudget), INF-013 (snapshot path, Task 1), INF-024/026/027/085/087 (re-review check and Reviser brief placement, carried by the literal `## Fix Budget` block, plan line 117), INF-033 and INF-044 (stdlib, determinism, Constraints), INF-054 (only --enforce writes, Constraints), INF-064 (check-first tests, Task 5), INF-066 (dual-surface lookup, Constraints and Task 4), INF-074 (inherited line 220, plan line 118), INF-113 (experiment build file, Task 7, location changed on purpose per plan line 30).
  - 1 is a real gap: INF-032, source.md:46 "At `review: 3` the run escalates as 427 says, now also listing each budget escalation with its need and each `GRADE-CONFLICT`". The literal `## Fix Budget` block the plan ships (source.md:103-129) has no review-3 escalation sentence, and no plan task adds one; the owner-decision `carried-open:` line (plan line 67) counts these ids but does not require the review-3 escalation to list each budget escalation with its need.

## Root cause / deviation (analyzer slice)

- Owner decisions and rulings are encoded as Constraints (plan lines 19-31) and carried into tasks: carried-open count (Task 2 line 67, Task 5 added sentence), no Unattended section (line 24, line 115), brief copies (line 160).
- Deliberate deviations from source.md, each stated in the plan: build-file location (.dev/brainstorms/... instead of the example .dev/experiments/..., plan line 30); one sentence added to the literal Fix Budget block for the owner counting decision (Task 5 region 4); a `carried-open:` report line not in source.md section 3.3 (Task 2).
- Unreviewed source sentences (source.md:50, the reverted-entry rule and per-entry hunk split) are implemented as written and tested first in Tasks 2 and 3 (plan Constraints, last bullet).

## Structural / tech debt (refactorer slice)

- Task granularity: Tasks 1-3 all edit one script and one test file in sequence; each has its own acceptance tests, so each stays independently reviewable.
- Absolute source paths appear in Task 8 (plan line 160) because the owner ruling names files outside the repo, two of them under /tmp. Risk: /tmp files may be gone before implementation; Task 8 stops as blocked rather than reconstructing.
- Task 7 test depends on commit 95f2c6e4 being in the clone (verified present now: `git cat-file -t 95f2c6e4` = commit; 472 lines).

## Risks

- R1 (blocking candidate): INF-032 gap above; the review-3 escalation would not list budget escalations and GRADE-CONFLICT ids, which source.md:46 requires and the owner counting decision depends on at review 3.
- R2 (minor): /tmp brief sources are volatile.

## Recommendations

- Add to Task 5 region 4 one sentence in `## Fix Budget` stating that at `review: 3` the escalation lists each budget escalation with its need and each `GRADE-CONFLICT` id; pin it in tests/skills/test_spec_panel_minfix.py.
