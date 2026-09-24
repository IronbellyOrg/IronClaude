# UC-1 pre-exec reflect — sc:pr-submit CI-failure phase

- mode: pre
- tier_reached: 1 (`--tier 1` pin; rubric would T2)
- spec: `/config/workspace/IronClaude/.dev/specs/pr-submit-ci-monitor.md`
- tasklist: spec §12 (same file)
- status: partial (`coverage_degraded: parsed-sparse`; semantic holes remain)
- C (inline-fallback): 0.86

## Coverage

Strict ID match (`\bFR-CI-N\b` in §12): **0/12** (`coverage_pct: 0.0`).
§12 never names the FR IDs. Semantic overlay (what the steps actually do):

| FR | §12 | Semantic |
|----|-----|----------|
| FR-CI-1 | 4 | covered |
| FR-CI-2 | 2 | covered |
| FR-CI-3 | 1 | covered |
| FR-CI-4 | 1 | partial — `cancel` unmapped |
| FR-CI-5 | 1 | partial — Finding `path`/`line` missing |
| FR-CI-6 | 1,4 | covered |
| FR-CI-7 | 1 | partial — workflow *file* may verify |
| FR-CI-8 | 4 | covered |
| FR-CI-9 | 3,4 | covered |
| FR-CI-10 | — | **hole** |
| FR-CI-11 | — | **hole** |
| FR-CI-12 | §2 | covered (non-goal) |

## Contradictions with code (re-Read)

1. **`gh pr checks --json` has no `conclusion`.** Spec §7 lists `conclusion`. Context7 `/websites/cli_github_manual` fields: `bucket, completedAt, description, event, link, name, startedAt, state, workflow`. Passing `conclusion` fails the poller.
2. **No per-check SHA.** FR-CI-10 cannot filter `checks[]` by commit. Attribution is PR `headRefOid` only.
3. **`is_groundable` drops empty path** (`fsm.py:285-293`). FR-CI-5 human-gate Finding without `path`+`line>0` never reaches `HALT_HUMAN`.
4. **`INV-CI-7` vs §9.** INV says source bit on `clean` only; §9 also changes `(S4_PUSHING, pushed)` (`fsm.py:644-645` currently always `S6_REPLYING`).
5. **`severity_hint="high"` → High → `--depth deep --fix`** (`severity_router.py:140-151`), not `--fix`. Intent (not report-only) is right; wording is wrong.
6. **VG-3:** spec is correct that `make lint` runs `lint-architecture` (`Makefile:48-50`). SKILL.md:105 still says "ruff check ONLY" — stale comment, not a reason to add VG-7.
7. **`EventType` is 37** (`models.py:20-21`; `test_run_log.py:164-168`). Do not add members. Extra payload field `source` on existing `poll_result` is allowed (`RunLog.append` only validates `event_type`).
8. **Production seam is SKILL + `transition()`, not `run_skill()`.** `run_skill()` always `do_reply`/`do_resolve`/`do_retrigger` (`fsm.py:1007-1023`). New FSM tests should call `transition()`.

## Over-build vs non-goals

Aligned: no new skill/FSM/EventType/classifier/`--ci-timeout`/`gh run rerun`/VG-7.
Do not: `source` on `RunConfig`, resume-during-CI, `__init__.py` re-export, T-105 clone (CI script may have no `gh api`).

## Recommendations (file + change + verifier)

1. Cite `FR-CI-*` on each §12 step (fixes `coverage_pct`).
2. Put FR-CI-10/11 in step 2; drop `conclusion`; SHA = `headRefOid`.
3. FR-CI-4: `cancel` → findings. FR-CI-5/7: `path` = check/workflow **name**, `line=1`.
4. INV-CI-7: `clean` **and** `pushed`. Tests: `transition()` + existing `test_eventtype_is_37_members_with_v11_events`.
5. Add `ci.py` to T-N50 `CORE_PURE_FILES`.

Verifier after spec edit: this matrix’s semantic holes empty; no new EventType/classifier/VG-7.

## Best-practice grade

**4/5** — extend existing monitor, skip S5a on CI push (Actions retrigger). Deductions: gh JSON invented field; FR-CI-10 over-specified.

## Grounding Gaps

None written. Unmapped FRs are spec gaps, not evidence-insufficient hunks.

## Inferred requirements (Pass 2)

None kept. Labeled FR/INV/FM spans absorbed MUST-bodies (parsed wins).
