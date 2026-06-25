# QA Report — Synthesis Gate (Phase 7 Cross-Cutting: Evidence-Quality / Hygiene-Test-Coverage Lens)

**Topic:** RFMerger tasklist — Phase 7 cross-cutting hygiene + carried-gap test coverage
**Date:** 2026-06-19
**Phase:** synthesis-gate (lens-based QA; evidence-quality / hygiene-test-coverage)
**Fix cycle:** N/A
**Fix authorization:** false (REPORT-ONLY — nothing modified)
**Stance:** ADVERSARIAL — assumed tests vacuous; mutation-probed every assertion.

---

## Overall Verdict: PASS (with 2 documented non-blocking coverage gaps)

The five `TestCrossCuttingHygiene` tests assert against source-of-truth
(`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`) and the real Click
command surface (`tasklist_group` from `superclaude.cli.tasklist.commands`).
All four required lens criteria are met: SoT grounding, full R-12 stale-token
coverage, each carried-gap test pins behavior and fails on regression, and zero
regressions (100 passed, reproduced live). Two MINOR vacuity edges are documented
below — neither regresses a pinned behavior nor blocks the gate.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Tests assert against SoT `src/superclaude/...` + real Click surface | PASS | `tasklist_skill_text` fixture reads `src/.../sc-tasklist-protocol/SKILL.md` (test file L35-46); `tasklist_group` imported from `superclaude.cli.tasklist.commands` (L18). NOT the `.claude/` mirror. `make verify-sync` clean -> SoT == shipped. |
| 2 | Stale-token test covers full R-12 set | PASS | `test_no_stale_tokens` loops `sc:task-unified, /rf:, .gfdoc, llm-workflows, /config/.claude` (5 plain `not in`) + `StageError` via 4 operative forms (`raise/class/except/StageError(`) + requires the no-reuse disclaimer assertion. grep confirms all 5 plain tokens = 0 hits; all 4 operative StageError forms = 0 hits; disclaimer present once (L1407). |
| 3 | StageError disclaimer handled correctly (forbid operative, allow negation) | PASS | The single `StageError` mention (L1407) is the explicit "NOT a reuse of any existing `StageError` symbol (none exists in current source)" disclaimer. Test forbids operative forms and asserts the disclaimer string present — exactly the requested semantics. |
| 4 | `test_sc_task_naming` pins delegation name | PARTIAL (MINOR vacuity, see G-1) | Negative half `sc:task-unified not in text` sound (mutation-confirmed). Positive half `sc:task in text` satisfied by the `sc:tasklist` substring even with all genuine `sc:task` delegations removed (mutation-confirmed vacuous). |
| 5 | `test_no_reflect_skips_stage_10_5` pins behavior, fails on regression | PASS | Both asserted strings (`**Skip when disabled.**` L1607; the `--no-reflect`/`--dry-run` skip sentence L1607) live in the genuine Stage 10.5 region (heading L1586). Mutation removing either -> assertion fails. |
| 6 | `test_stage_10_5_advisory_ships_all_verdicts` pins behavior | PASS | `PASS\|PARTIAL\|FAIL` (L759) + `The bundle ships regardless of verdict` (L1609) both in Stage 10.5 region. Mutation removing either -> assertion fails. |
| 7 | `test_slash_flag_parsing` asserts real flags + non-zero on bad flag | PASS | Live: `validate --help` exit 0, contains all of `--roadmap-file/--tasklist-dir/--model/--max-turns`; `validate --bogus-flag x` exits 2. Real Click command, not a stub. |
| 8 | Zero regressions (100 passed) | PASS | Reproduced live: `uv run pytest tests/tasklist/ -q` -> 100 passed in 0.21s. `TestCrossCuttingHygiene` -> 5 passed. Matches xcut-pytest-summary (95->100, +5, 0 regressions). |
| 9 | §49-57 edit doc-only (no flag/algorithm change) — adjacent cross-check | PASS | `--spec` enrichment intact: grep = 10 occurrences, matching phase-7 summary. Edit reframes roadmap-primary + `--spec`-optional (L49-66); no flag/gate/emitter removed. |

## Summary

- Checks passed: 8 / 9 fully PASS; 1 PARTIAL (item 4, non-blocking MINOR)
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (REPORT-ONLY)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| G-1 | MINOR | `tests/tasklist/test_tasklist_cli.py` `test_sc_task_naming` L660 | Positive assertion `assert "sc:task" in text` is a substring check satisfied by the skill's own `sc:tasklist` name. Mutation-confirmed: deleting every genuine `sc:task` delegation reference (regex `sc:task(?!list)`) while keeping `sc:tasklist` still passes the assertion. The comment claims it proves "delegates to the real `sc:task` name", but it cannot distinguish a real delegation from the skill name. The negative half (`sc:task-unified not in text`) — the actual R-12 concern — is sound and non-vacuous. | Tighten the positive assert to a word-boundary / disambiguating form, e.g. require a bare-delegation token such as `` `sc:task` `` (backtick-wrapped) or `sc:task ` (trailing space) that does not collide with `sc:tasklist`. grep shows 8 `sc:task ` and 11 `` sc:task` `` genuine delegation forms exist, so a tighter assert would still pass today and would catch the regression G-1 describes. |
| G-2 | MINOR | `tests/tasklist/test_tasklist_cli.py` `test_no_stale_tokens` L669-679 | `StageError` is gated only via 4 operative patterns + the disclaimer-present assertion. A NEW *bare* `StageError` mention (not matching `raise/class/except/StageError(`) added elsewhere while the disclaimer remains would pass the test. Mutation-confirmed: replacing the disclaimer text with "we now use StageError for this" is caught (the disclaimer-present assert fires), but a bare additive mention with disclaimer intact is not. The risk is low because there is exactly 1 `StageError` occurrence today and it is the disclaimer. | Optional hardening: assert `text.count("StageError") == 1` (or `<= 1`) so any additional bare mention trips the test. Not required for the carried R-12 intent (operative reuse is the real hazard, and that is covered). |

## Mutation-Probe Evidence (non-vacuity proof)

All probes run in-memory (no file modified). Each confirms the assertion would FAIL on regression:

- stale-token loop: injecting `/config/.claude/foo` -> `WOULD FAIL on: /config/.claude` (non-vacuous: True)
- operative StageError: injecting `raise StageError("x")` -> caught (non-vacuous: True)
- skip-when-disabled: removing `**Skip when disabled.**` -> assert1 fails; removing the skip sentence -> assert2 fails (both non-vacuous)
- all-verdicts: removing `PASS|PARTIAL|FAIL` -> assert1 fails; removing `The bundle ships regardless of verdict` -> assert2 fails (both non-vacuous)
- slash-flag: live CliRunner — help exit 0 w/ all 4 flags; bogus flag exit 2 (real surface)
- G-1 vacuity: `re.sub(r'sc:task(?!list)', 'XX:DELEGATE', text)` -> positive assert STILL passes (vacuous: True); negative assert still passes
- G-2 vacuity: bare additive `StageError` mention with disclaimer intact would pass (operative-form check is the only operative gate)

## Actions Taken

None — fix_authorization: false. Both findings are documented for the orchestrator/maintainer; neither is mine to fix.

## Recommendations

- G-1 and G-2 are MINOR test-hardening opportunities, not regressions of any pinned behavior. The carried R-12 intent (no operative stale tokens, no `sc:task-unified`) IS enforced. Safe to proceed; optionally fold G-1's word-boundary tightening into a follow-up hygiene pass.
- No action required to clear this gate.

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
  (Item 4 is VERIFIED — the vacuity itself was proven via mutation; the PARTIAL status reflects a test-quality finding, not an unverified check.)
- **Tool engagement:** Read: 5 | Grep: 0 (greps run via Bash) | Glob: 0 | Bash: 8
  No web research performed (all claims are local/source-truth).
- Every checklist item maps to a specific tool call (Read of test/SKILL/research/summary files; Bash grep + live pytest + live CliRunner + mutation probes). Tool-call count (13) >= checklist items (9): not suspect.

## QA Complete
