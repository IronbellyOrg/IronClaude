# QA Report — Final Structural / Evidence-Quality (Phase 8.G1)

**Topic:** RFMerger P1–P5 tasklist build — "final evidence-quality / full-suite green" lens
**Date:** 2026-06-19
**Phase:** report-validation (final structural lens, fix_authorization: false — REPORT-ONLY)
**Fix cycle:** N/A
**Lens:** Adversarial. Assume some stay-green suite secretly regressed or a new test is vacuous.

---

## Overall Verdict: PASS

The build is genuinely green at the LIVE tree state. All seven stay-green suites pass with
exact expected counts (independently re-run, not trusted from captured `.txt`). The two
changed test files are clean under `ruff format --check` and `ruff check`. `make verify-sync`
is clean. The only `make lint` error is the documented PRE-EXISTING `recommend.md`
lint-architecture mismatch, which I independently confirmed is NOT in this task's diff.
The 30 new tests (29 in test_tasklist_cli.py + 1 new class in test_task_builder_merge.py)
are non-vacuous and grounded in the real source — every load-bearing asserted string was
spot-checked to exist at the exact count the test demands.

Findings below are recorded for completeness; none is severe enough to flip the verdict.
The most material finding (F1) is a STALENESS discrepancy between a captured artifact and
the live tree — it resolves in the build's favor (live is greener than captured).

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | tasklist/ suite = 100, 0 fail | PASS | LIVE re-run `uv run pytest tests/tasklist/` → `100 passed in 0.21s`. Matches 71 baseline + 29 new. |
| 2 | prd/autowire subset = 22 | PASS | LIVE `test_prd_cli.py test_prd_prompts.py test_autowire.py` → `22 passed`. |
| 3 | reflect = 78 + 1 xpass | PASS | LIVE `tests/cli/reflect/` → `78 passed, 1 xpassed`. The X (xpass) is `test_no_nesting_guard` — pre-existing, not a new regression. |
| 4 | task_builder_merge = 67 | PASS | LIVE `tests/skills/test_task_builder_merge.py` → `67 passed`. (66 pre-existing + 1 new TestTasklistDnspMapsDM003.) |
| 5 | audit inherited-verdict + five-axes = 34 | PASS | LIVE both files → `34 passed, 2 warnings`. Warnings = pytest class-scoped-fixture deprecation, not failures. |
| 6 | verify-sync-hooks = 7 | PASS | LIVE `tests/cli/test_verify_sync_hooks.py` → `7 passed`. |
| 7 | Combined stay-green re-run | PASS | Single LIVE invocation of all 6 suites → `286 passed, 1 xpassed, 2 warnings in 4.59s`. Zero failures. |
| 8 | `ruff check` on 2 changed test files | PASS | LIVE `ruff check tests/tasklist/test_tasklist_cli.py tests/skills/test_task_builder_merge.py` → `All checks passed!` EXIT=0. |
| 9 | `ruff format --check` on 2 changed test files | PASS | LIVE → `2 files already formatted` EXIT=0. NOTE: captured `final-format-check.txt` listed BOTH as "would reformat" — stale (see F1). |
| 10 | `make lint` clean modulo pre-existing recommend.md | PASS (conditional) | LIVE `make lint` → `Errors: 1` = `recommend.md ... no matching skill directory: sc-recommend-protocol`. Only error; 5 size-warnings. `recommend.md` NOT in this task's diff. |
| 11 | `make verify-sync` clean | PASS | LIVE `make verify-sync` → `✅ All components in sync.` EXIT=0. No `.claude/` mirror staged. |
| 12 | New tests non-vacuous (specific asserts) | PASS | Read both new test files in full. Asserts pin literal multi-token strings, exact predicates, em-dash bytes, byte-exact halt strings, exact tuple shapes, AND negative guards. |
| 13 | New tests grounded in real source (not co-stale) | PASS | Independently grepped live SKILL.md/templates for the most load-bearing asserted strings — all present at the exact asserted counts (table below). |
| 14 | Coverage: all 5 proposals + carried gaps + stale tokens | PASS | P4/P1/P3/P2/P5 each have a test class; carried-gaps+stale-tokens=TestCrossCuttingHygiene; P3-reuse=TestTasklistDnspMapsDM003. |
| 15 | Mirror invariants (R-2 + P5 index) hold | PASS | phase-template HAS `## Execution Context` (x2) + no-file:line discipline; index-template does NOT (R-2 lock, count 0); index-template HAS `## Tier Calibration Advisory` (x2). |

## Independent source-grounding spot-check (anti-co-staleness)

Confirmed the asserted strings exist in the LIVE source at the exact counts the tests demand
(a vacuous test asserts a string the source lacks; a co-stale test+source pair could pass
against the captured artifacts yet diverge from live — this check refutes both):

| Asserted token | Test expectation | LIVE source count | OK |
|----------------|------------------|-------------------|-----|
| `StageError` in SKILL.md | exactly 1 (disclaimer only) | 1 | yes |
| `17 checks` in SKILL.md | absent | 0 | yes |
| `Self-Check: all 20 checks passed` | present | 1 | yes |
| `[HALT-MONOTONICITY] ...` halt string | present | 1 | yes |
| `Regression detected on Item X.Y — ...` | present (em-dash) | 1 | yes |
| `["<stage7_affected_range>", "retry-1"]` | present | 1 | yes |
| `Manual review required — partition agent failed twice` | present (em-dash) | 2 | yes |
| `TASKLIST_ROOT/validation/gate-results.txt` | >=4 (same-path) | 4 | yes |
| Tier-Calibration table header | present | 1 | yes |
| `--no-reflect`/`--dry-run` skip line | present | 1 | yes |
| `bundle ships regardless` / `PASS\|PARTIAL\|FAIL` | present | 1 / 1 | yes |
| phase-template `## Execution Context` | present | 2 | yes |
| index-template `## Execution Context` (R-2 lock) | absent | 0 | yes |
| index-template `## Tier Calibration Advisory` | present | 2 | yes |

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| F1 | MINOR | test-results/final-format-check.txt vs live tree | Captured artifact (11:27) lists BOTH `tests/skills/test_task_builder_merge.py` and `tests/tasklist/test_tasklist_cli.py` in the "would reformat" set. LIVE `ruff format --check` on the same two files → `2 files already formatted`. The captured "✅ my 2 files clean" claim in final-cross-phase-summary.md is therefore NOT reproducible from final-format-check.txt — they were formatted AFTER the artifact was captured. Resolves in build's favor (live is clean), but the captured evidence and the summary contradict each other. | Re-capture final-format-check.txt after the format pass, OR annotate the summary that the artifact predates the format fix. No code change needed. |
| F2 | MINOR | final-cross-phase-summary.md line 52 | Summary asserts "104 others PRE-EXISTING, zero overlap with diff". LIVE format-check now reports 106 files would reformat (incl. the 2 task files at capture time), and the changed-file overlap is non-zero in the captured artifact. The "zero overlap" claim is true ONLY post-format-fix; it was false at the moment final-format-check.txt was written. | Same as F1 — re-capture or annotate. |
| F3 | MINOR | final-cross-phase-summary.md line 12 / lines 33-39 | The count narrative is internally inconsistent: summary line 12 says "29 new ... plus 1 R-2 index lock — net 71 + 29 = 100" (treats the R-2 lock as the 29th), while the per-class inventory (lines 33-39) sums 6+5+5+3+5+5+1 = 30 NEW tests, of which 1 (TestTasklistDnspMapsDM003) lives in test_task_builder_merge.py (so 29 land in tasklist/). The "29 new" figure conflates "new tasklist tests" with "total new tests". The arithmetic lands at 100 correctly, but the prose double-uses 29. | Clarify: 29 new in tests/tasklist/ (71→100) + 1 new class in tests/skills/test_task_builder_merge.py (66→67). |
| F4 | MINOR | final-tasklist-summary.md line 12 | Same conflation: "New RFMerger tests added across phases: 29 (P4: 6, P1: 7, P3: 2, ...)". But P1 has 5 test methods (test_execution_context_*), not 7; and P3 in tasklist/ has 5 methods (TestP3DnspSyntheticFindings), with "2" apparently counting something else (DM-003 mapping?). The per-phase breakdown does not match the actual method counts in the committed test file. The TOTAL (100 passed) is correct and verified; only the per-phase attribution prose is loose. | Reconcile the per-phase counts against actual `def test_` counts: P4=6, P1=5, P3=5, P2=3, P5=5, hygiene=5 = 29. |
| F5 | INFORMATIONAL | make lint / recommend.md | The pre-existing lint error (`recommend.md has ## Activation but no matching skill directory: sc-recommend-protocol`) is real and gates `make lint` to exit 2. The skill exists as `sc-recommend` (no `-protocol` suffix). This is an upstream naming drift unrelated to this task, correctly excluded. Risk: any future `make lint` CI gate on this branch fails for an unrelated reason, masking real regressions. | Out of scope for this task. Track separately: either rename the skill dir to `sc-recommend-protocol` or relax Check-1 for the `recommend` exception. |
| F6 | INFORMATIONAL | reflect suite xpass | `tests/cli/reflect/test_no_nesting_guard.py` reports 1 XPASS (a test marked xfail that now passes). An xpass is a silent signal that an xfail marker is stale and should be removed. Not a failure, but it is technical debt the "78 passed, 1 xpassed" framing normalizes. Pre-existing, not introduced by this task. | Out of scope. Track: remove the stale xfail marker in a hygiene pass. |
| F7 | INFORMATIONAL | audit suite warnings | `tests/audit/test_inherited_verdict_freshness_inv_002.py` emits 2 PytestRemovedIn10Warning (class-scoped fixture as instance method). Will become an ERROR under pytest 10. Pre-existing. | Out of scope. Track: convert the fixture to `@classmethod`. |
| F8 | MINOR | test_tasklist_cli.py TestCrossCuttingHygiene::test_slash_flag_parsing | This test invokes `tasklist_group ["validate", "--bogus-flag", "x"]` and asserts non-zero exit — but it does NOT assert the new P1/P3/P4/P5 markdown content is reachable through any CLI path. The five proposals are markdown-only content gates (no executable Python surface), so there is genuinely no runtime path to exercise — but that means a future code change that wires these into the executor would NOT be caught by these content-only tests. This is a structural coverage ceiling, not a defect. | None required now. Note in tech-ref: P1-P5 are content gates; if/when promoted to executable behavior, add behavioral tests. |
| F9 | MINOR | OQ-PRE-2 note (summary lines 55-60) | The summary claims the P1/P5 level-2 headings are "inert to the Sprint parser" and cites "tasklist-fidelity stay-green suites all pass" as confirmation. But no NEW test in either changed file directly asserts Sprint-parser non-breakage on a generated bundle containing `## Execution Context` / `## Tier Calibration Advisory` — the claim rests on the EXISTING fidelity suite, which does not necessarily include a fixture with these new headings. The coverage-0.964 figure is asserted, not reproduced in the verified artifacts I was given. | Confirm a fidelity fixture exercises a bundle carrying both new headings, OR add one. Out of scope for this lens (no parser regression observed in any live suite). |
| F10 | INFORMATIONAL | found_n_times assert | `test_dnsp_synthetic_provenance` asserts the literal `` `found_n_times`: `1` `` but does NOT assert the increment semantics ("increments by 1 on within-cycle dedup collapse"). The test pins the default-value byte but not the behavioral rule. Since the rule is prose-only in SKILL.md (no executable counter), the assert is as strong as the surface allows, but a reader should not mistake it for a behavioral guarantee. | None required (content-gate ceiling, same as F8). |
| F11 | INFORMATIONAL | em-dash recommendation count = 2 | `Manual review required — partition agent failed twice` appears TWICE in SKILL.md. The test (`test_dnsp_synthetic_provenance`) uses `in` (substring), so it passes on >=1 and does not pin the count. Two occurrences is expected (one in the P3 contract prose, one in an example), but a single source-of-truth contract field appearing twice is a mild duplication that DM-003 anti-duplication discipline (lint Check 11, which passed) would ideally catch if these were code constants. | None — markdown prose, acceptable. Noted for completeness. |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor / informational findings: 11 (F1-F11; none verdict-flipping — F1/F2 are captured-artifact staleness that resolves in the build's favor, F3/F4/F8/F9 are count-prose/coverage-ceiling notes, F5/F6/F7/F10/F11 are pre-existing or content-gate-ceiling informational)
- Issues fixed in-place: 0 (fix_authorization: false — REPORT-ONLY)

## Adversarial self-audit
If I told the user "0 issues," would they believe me? I can cite: 6 live pytest re-runs (286+1xpass, zero
failures), 2 live ruff invocations (EXIT=0), 1 live make verify-sync (EXIT=0), 1 live make lint (1 documented
pre-existing error), and 14 independent grep counts against the LIVE source proving the new tests are non-vacuous
and not co-stale. The build is genuinely green. The 11 findings are honest residue — the most material (F1/F2)
is that the captured format-check artifact is STALE relative to the live tree, which I caught precisely because
I re-ran live rather than trusting the `.txt`. That is the adversarial stance paying off: the captured evidence
and the summary contradicted each other, and live re-run resolved it. None of the 11 reaches IMPORTANT.

## Confidence
**Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
- All 15 checklist items VERIFIED with cited live tool output. Zero UNCHECKED, zero UNVERIFIABLE.
- confidence = 15 / (15 - 0) * 100 = 100.0% (>= 95% AND UNCHECKED == 0 → eligible for PASS).

## Tool engagement
**Read: 12 | Grep: 0 | Glob: 0 | Bash: 9** (Grep performed via Bash `grep -c` — 25+ distinct grep
invocations across 3 Bash calls, each mapped to a specific load-bearing assertion; no padding). No web
research required (all claims are local-source-bound; Tavily-first rule not triggered).
Tool-call count (21) >= checklist items (15): engagement minimum satisfied.

## Recommendations
- PROCEED. The "final evidence-quality / full-suite green" lens is GREEN. No blocking issue.
- Before/at commit: re-capture `final-format-check.txt` so the committed artifact matches the live clean state
  (resolves F1/F2), and reconcile the per-phase test-count prose in the two summary files (F3/F4).
- Track F5 (recommend.md lint), F6 (stale xfail), F7 (pytest-10 fixture warning) as separate hygiene items —
  all pre-existing, none introduced by this build.

## QA Complete
