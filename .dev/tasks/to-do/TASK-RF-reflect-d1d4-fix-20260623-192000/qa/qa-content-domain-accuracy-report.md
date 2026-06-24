# QA Report — Task Qualitative Review (domain-accuracy lens)

**Topic:** D1/D3/D4 reflect-reviewer-guard fix — domain correctness of design-(b) telemetry-honesty narrowing
**Date:** 2026-06-24
**Phase:** task-qualitative
**Lens:** domain-accuracy
**Fix cycle:** N/A
**fix_authorization:** false (report-only)

---

## Overall Verdict: PASS

Every domain-accuracy claim in the spawn brief was independently verified against the actual
changed reflect source, the SKILL.md prose, the agent file, the filesystem, and the live test
suite. The D1 design-(b) fix is domain-correct: it narrows telemetry honesty WITHOUT removing
grounding, does NOT leak the new value onto the default-OFF (#153) path, and the value name is
semantically accurate. D3 now cites only resolvable docs. No domain errors found.

The adversarial mandate to assume >=5 errors was applied: I actively hunted for (1) a leak of
`snapshot-children-only` onto the flag-off path, (2) removal of child grounding, (3) a residual
live emission of the old bare `"snapshot"` value, (4) stale tests asserting the old value,
(5) a broken stopped-precondition path, (6) a non-existent doc still cited, (7) an under-claim
(workers actually grounded but reported as children-only). All seven candidate-error hunts came
back clean with positive evidence.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | New value gated on grounding-root / snapshot only | none | PASS | ensemble.py:318-320 `"snapshot-children-only" if config.reviewer_grounding_root else "disabled"`; runner.py:685-687 `if snapshot_path is not None:`. Only assignment to `config.reviewer_grounding_root` is runner.py:627, gated by `if config.isolate_reviewers:` (617) + successful `create_review_snapshot`. |
| 2 | No leak onto default-OFF (#153) path | none | PASS | models.py:105 default `reviewer_grounding_root=None`; models.py:146 default `reviewer_isolation="disabled"`. Flag-off skips the entire 616-627 block → both stay default → ensemble + result both emit `"disabled"`. Proven live by `test_disabled_path_unchanged_when_isolation_off` (asserts `mock_create.assert_not_called()` + `reviewer_isolation == "disabled"` + `reviewer_grounding_root is None`). |
| 3 | Children grounding NOT removed by fix | none | PASS | Tier-1 audit child runner.py:461 `cwd=config.reviewer_grounding_root`; adversarial scorer ensemble.py:369 `cwd=config.reviewer_grounding_root`. Both intact. Test asserts `mock_cls.call_args.kwargs.get("cwd") == snapshot`. |
| 4 | Value name semantically accurate (children grounded, workers not) | none | PASS | Swarm workers via `dispatch_wave1` (ensemble.py:207-212) receive only prompt/spec/factory — NO cwd. Review target `_load_review_target` (ensemble.py:436-447) + normalize recipe target (ensemble.py:218) read `config.tasklist_path` (LIVE), never `reviewer_grounding_root`. So "children-only" is honest — not an over- or under-claim. |
| 5 | models.py default stays "disabled" | none | PASS | models.py:146 `reviewer_isolation: str = "disabled"` (ReflectResult); ensemble.py:503 `reviewer_isolation: str = "disabled"` (build_reflect_contract). Unchanged. |
| 6 | stopped-precondition path unaffected | none | PASS | runner.py:518 `_stopped_precondition` emits `reviewer_isolation="stopped-precondition"` with `reviewer_grounding_root=None` (520) on its own independent BLOCKED path; not touched by the snapshot-success branch. |
| 7 | No residual LIVE emission of old bare "snapshot" value | none | PASS | grep: only two `"snapshot"` literals remain (ensemble.py:317, runner.py:684) and both are inside explanatory comments, not emission expressions. No code path assigns `reviewer_isolation = "snapshot"`. |
| 8 | No stale tests assert old "snapshot" value | none | PASS | grep for `reviewer_isolation == "snapshot"` / `== "snapshot"` in tests/cli/reflect/ → zero hits. Two tests assert the NEW value (`test_reviewer_isolation_gate.py`, `test_reviewer_swarm_target_grounding.py`). |
| 9 | SKILL.md Step 0.5e item 4 honestly describes children-only scope, no overclaim | none | PASS | SKILL.md:268 item 4 retitled "Grounding-root redirect (scope: ClaudeProcess children only, v1)"; states swarm-worker target "still sourced from the live tasklist path (NOT yet derived from `<snapshot>`)" and "reports this scope honestly rather than overclaiming full `snapshot` isolation." SKILL.md:271 enumerates the value set `disabled \| snapshot-children-only \| stopped-precondition`. Matches code reality exactly. |
| 10 | D3 reflect-reviewer.md:133 cites only resolvable docs | none | PASS | :133 now cites the two git-tracked forensics docs (damage-report, subagent-forensics) as resolvable, and explicitly demotes the proposal + BUILD_REQUEST to "named for provenance, not as worktree-resolvable citations." See item 11 for filesystem verification. |
| 11 | D3 cited docs exist; the previously-cited proposal does not | none | PASS | `git ls-files` confirms both cited docs are tracked + present (16084 / 19848 bytes). The previously-cited non-existent `.dev/analysis/pr199-reflect-hardening-proposal-2026-06-22.md` confirmed ABSENT (`ls` → No such file) and the prose no longer claims it as the primary source. |
| 12 | Operational greenness (full reflect suite) | none | PASS | `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run pytest tests/cli/reflect/ -q` → 145 passed, 1 xpassed, 0 failed. |

<!-- All checks PASSED → Axis = none on every row per PR-07 canonical annotation rules. -->

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only; fix_authorization: false)
- Axis lens status: drift-axis-inactive

`drift-axis-inactive` — no BUILD_REQUEST.GOAL verbatim was injected in the spawn prompt and the
research file does not reproduce a GOAL line, so the AX-1 Drift axis is INACTIVE for this review.
The remaining four axes (AX-2 contradictions, AX-3 omissions, AX-4 weakened-criteria,
AX-5 invented-content) were applied; none fired. (The brief is a verification checklist against
already-landed code, not a forward-looking task whose criteria could be weakened, so AX-2..AX-5
surfaced nothing — every claim was confirmable against source.)

## Issues Found

None.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | No domain-accuracy issues found | — |

## Actions Taken

None (report-only mode; verdict PASS so no fixes were warranted regardless).

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was present in the spawn prompt; this review ran in
standalone mode. All verification was performed independently with my own tool engagement (no
reliance on a prior structural verdict).

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**

- None — no inherited structural verdict was supplied; nothing was relied upon.

**(b) Independent semantic checks (≥1 required, INV-019):**

- Default-OFF non-leak — traced the only `config.reviewer_grounding_root` assignment (runner.py:627)
  and confirmed it is gated by `if config.isolate_reviewers:` (runner.py:617); cross-checked
  defaults at models.py:105/146; corroborated by a live pytest run of
  `test_disabled_path_unchanged_when_isolation_off` (PASS).
- Children-grounding preserved — Read ensemble.py:369 + runner.py:461 (`cwd=config.reviewer_grounding_root`
  both present) and confirmed the test asserts `cwd == snapshot`.
- Value semantic accuracy — Read `_load_review_target` (ensemble.py:436-447) + normalize recipe
  target (ensemble.py:218) and confirmed swarm-worker target is `config.tasklist_path` (live),
  proving "children-only" is honest.
- D3 doc resolvability — `git ls-files` + `ls` on all three pr199 docs; confirmed the two cited
  exist/tracked and the previously-cited proposal is absent.

### Self-Audit (mandatory questions)

1. **How many factual claims independently verified against source code?** 12 distinct domain
   claims, each backed by a specific grep/Read/Bash result or a live test assertion.
2. **What specific files did you read?** ensemble.py, models.py, runner.py (full), SKILL.md
   (Step 0.5e region :240-298), reflect-reviewer.md (:120-133),
   test_reviewer_swarm_target_grounding.py (full), the research evidence file; plus grep/ls/git
   sweeps over src/superclaude/cli/reflect/ and tests/cli/reflect/.
3. **If 0 issues, why trust the check was thorough?** I ran seven adversarial error-hunts (leak,
   grounding-removal, residual live overclaim, stale tests, broken stop path, non-existent doc,
   under-claim) — each returned positive disconfirming evidence, not mere absence. The single
   highest-risk concern (default-OFF leak) is covered by a dedicated regression test that passes.
4. **Web research performed?** None — every claim was local-file/source-bound. No Tavily/WebFetch
   fallback was needed.

### Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep: ~7 (via Bash) | Glob: 0 | Bash: 5

Tool-call count (Read 5 + Bash 5 carrying ~7 grep/ls/git sweeps + 2 pytest runs) >= 12 checklist
items. Eligible for PASS (>=95% AND 0 unchecked).

## Recommendations

- No blocking action. The fix is domain-correct and operationally green.
- Optional (non-blocking, already disclosed in code/SKILL.md as deferred "design (a)"): closing the
  swarm-worker read surface by deriving the worker review target from `<snapshot>` would let the
  telemetry graduate from `snapshot-children-only` to full `snapshot`. Tracked as a follow-up; out
  of scope for this D1 design-(b) narrowing.

## QA Complete
