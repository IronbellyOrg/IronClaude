# tests/pr_submit Audit (Pass 1) - Batch 1 of 2

**Status**: Complete (scanner report; spot-check pending)
**Files audited**: 50 / 50 assigned
**Date**: 2026-11-05
**Agent**: audit-scanner
**Batch**: 1

Method: the Grep tool cannot take `--exclude-dir`, so `.claude-audit/**` was excluded with a glob filter. The Grep tool does search hidden directories such as `.dev/`.

Collection facts, verified in `pyproject.toml`:
- Line 107 is `[tool.pytest.ini_options]`; line 108 is `testpaths = ["tests"]`; line 109 is `python_files = ["test_*.py"]`.
- So `test_*.py` files are collected. `conftest.py` is auto-loaded by pytest. `__init__.py` is not collected as a test; it is empty and makes `tests/pr_submit` a package. `tests/__init__.py` exists.

## Safe to Delete

None. No file in this batch has zero references.

## Need Decision

Five fixture files have no loader. Each is named only in a comment or docstring and in `.dev/` planning documents. None of the 12 `.py` files matched a wiring indicator, so there are no `[wiring]` entries.

- [ ] `tests/pr_submit/fixtures/review-clean.json` — No `load_fixture` or `FIXTURES_DIR` call loads it.
  - Named only in `tests/pr_submit/test_detection_contract.py:10` (docstring) and `:51`, `:59` (comments of the form `# Phase 10: swap for load_fixture("review-clean.json")`).
  - The docstring says the fixture "SUPERSEDES these inline dicts". The swap was never done, so the tests still use inline dicts.
  - Other referrers are hidden-path docs only: `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md:461` and `.dev/tasks/to-do/TASK-RF-submit-pr-20260611-030241/research/01-component-inventory.md:151`.
  - Not DELETE because comments reference it and the swap may still be wanted. Human decision: wire it into `test_detection_contract.py` or remove it.
- [ ] `tests/pr_submit/fixtures/review-with-findings.json` — Same situation. Named only in `test_detection_contract.py:11` and `:71` (comment), plus `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md:462`. Not loaded.
- [ ] `tests/pr_submit/fixtures/review-non-augment.json` — Same situation. Named only in `test_detection_contract.py:11` and `:292` (comment), plus `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md:463` and `.dev/tasks/done/TASK-WF-implementTheDesi-20261031-182028/artifacts/retries/T2/prompt-1-1.md:168`. Not loaded.
- [ ] `tests/pr_submit/fixtures/review-interleaved.json` — Same situation. Named only in `test_detection_contract.py:12` and `:321` (comment), plus `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-spec.md:464`. Not loaded.
- [ ] `tests/pr_submit/fixtures/rereview-then-decline.json` — No loader call.
  - The only `.py` mention is the docstring at `tests/pr_submit/test_loop_guard.py:152`: "Reuses the rereview-then-decline scenario shape". `test_loop_guard.py` loads only `round-sequence-residual-x3.json` (`:62`).
  - Hidden-path planning docs name it, for example `.dev/tasks/to-do/TASK-RF-pr-submit-v11-20260612-013419/research/05-test-infra-fixtures-markers.md:334`, which planned it for `test_loop_guard.py`.
  - Looks like a planned-but-unwired fixture. Not DELETE because it is referenced in a docstring and in plans.

Dynamic-loading check for these five (checklist patterns 1 to 5):
- Pattern 4 (glob): there are no globs over `fixtures/` anywhere in `tests/pr_submit`. The only `glob` or `rglob` hits in the suite are `test_static_grep.py:151` (`PR_SUBMIT_PKG.glob("*.py")`), `:776`, `test_conflict_sync_protocol.py:413` (`SKILL_DIR.rglob("*")`), `test_conflict_e2e.py:869`, `:1049`, `:1112`, `test_conflict_scripts.py:548`, `:1312` and `test_contract_setup_pr_submit_integration.py:224`, `:227`. None scan `tests/pr_submit/fixtures`.
- Pattern 5 (config): `pyproject.toml:108-109` governs test collection only. It does not load JSON fixtures.
- Patterns 1 to 3: no env-var-based, string-built or registry loading of fixtures exists. The only loader is `conftest.py:33` (`FIXTURES_DIR / name`), which needs an explicit name.
- Result: no dynamic-loading path found. These are REVIEW on the strength of the comment and plan references, not on dynamic loading.

## Keep (verified legitimate)

Each Python file below is also collected through `pyproject.toml:108-109`.

Package and conftest
- `tests/pr_submit/__init__.py` — empty file that makes `tests/pr_submit` a package, needed for the package-qualified imports (referenced by: `tests/pr_submit/test_conflict_e2e.py:61`, `tests/pr_submit/test_conflict_sync_protocol.py:21`, `tests/pr_submit/test_cosmos_protocol.py:16`).
- `tests/pr_submit/conftest.py` — auto-loaded by pytest. Provides the `load_fixture` fixture used across the suite (referenced by: `tests/pr_submit/test_ci_classify.py:21`, `tests/pr_submit/test_silence.py:28`). Also defines the FX5 hook `pytest_generate_tests` (`conftest.py:242`), references `test_gate_helper_differentials.py` (`conftest.py:163`) and loads `finding-medium-high.json` at `conftest.py:80`.

Test modules (all contain tests, all collected)
- `tests/pr_submit/test_auggie_fallback.py` — 12 tests (referenced by: `.dev/tasks/issue-302-handoff/verify-2/full-pytest.log:358`, `.dev/reflect/pre-design-20261104164711/reviewer-briefs/reviewer-2.md:1826`; collected via `pyproject.toml:108`).
- `tests/pr_submit/test_augment_review_remediation.py` — 7 tests (referenced by: `.dev/reflect/pre-design-20261104164711/reviewer-briefs/reviewer-2.md:271`, `.dev/tasks/issue-302-handoff/verify-2/full-pytest.log:359`).
- `tests/pr_submit/test_autonomy_gates.py` — 8 tests (referenced by: `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/adversarial/variant-3-haiku-qa.md:196`; collected via `pyproject.toml:108`).
- `tests/pr_submit/test_ci_classify.py` — 32 tests (referenced by: `.dev/specs/pr-submit-ci-wait.md:162`, `.dev/specs/pr-submit-ci-monitor.md:304`).
- `tests/pr_submit/test_codex_reviews.py` — 34 tests (referenced by: `.dev/pr-submit-codex/design/pr-submit-codex-design.md:373`, `.dev/reflect/pre-design-20261104164711/reviewer-briefs/reviewer-2.md:274`).
- `tests/pr_submit/test_conflict_e2e.py` — 5 tests (referenced by: `.dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/hardening.md:15`). Imports from `test_conflict_scripts` at `test_conflict_e2e.py:61`.
- `tests/pr_submit/test_conflict_scripts.py` — 60 tests (referenced by: `tests/pr_submit/test_conflict_e2e.py:61` via import; `.dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/hardening.md:15`).
- `tests/pr_submit/test_conflict_sync_protocol.py` — 22 tests (referenced by: `.dev/troubleshoot/bug-evidence-collector-bounds-20261104221343/doc-context.md:16`; collected via `pyproject.toml:108`).
- `tests/pr_submit/test_conflicts_core.py` — 131 tests (referenced by: `.dev/troubleshoot/bug-tier1-lock-trust-20261104221453/tier1-hypothesis.md:25`; collected via `pyproject.toml:108`).
- `tests/pr_submit/test_contract_setup_diagnosis.py` — 14 tests (referenced by: `tests/cli/reflect/test_contract_status_cli.py:180`, `.dev/specs/pr-submit-default-monitor-3.md:59`).

Fixtures (each loaded by `load_fixture(name)` through `conftest.py:33`, or by a direct path read; the referrer is the call site)
- `tests/pr_submit/fixtures/auggie-fallback-findings.json` — `tests/pr_submit/test_auggie_fallback.py:151`.
- `tests/pr_submit/fixtures/behavioral-drift.json` — `tests/pr_submit/test_validated_not_verified.py:24`.
- `tests/pr_submit/fixtures/checks-fail.json` — `tests/pr_submit/test_ci_classify.py:54`.
- `tests/pr_submit/fixtures/checks-pass.json` — `tests/pr_submit/test_ci_classify.py:34`.
- `tests/pr_submit/fixtures/checks-pending.json` — `tests/pr_submit/test_ci_classify.py:22`.
- `tests/pr_submit/fixtures/codex-clean-pr334.json` — `tests/pr_submit/test_codex_reviews.py:66`.
- `tests/pr_submit/fixtures/codex-findings-pr336.json` — `tests/pr_submit/test_codex_reviews.py:71`.
- `tests/pr_submit/fixtures/cosmos-pr266.json` — `tests/pr_submit/test_cosmos_review.py:34`, `tests/pr_submit/test_cosmos_protocol.py:52`.
- `tests/pr_submit/fixtures/cosmos-pr337.json` — `tests/pr_submit/test_cosmos_review.py:480`.
- `tests/pr_submit/fixtures/crash-after-push-before-completed.json` — `tests/pr_submit/test_crash_recovery.py:229`.
- `tests/pr_submit/fixtures/decline-backtick.json` — `tests/pr_submit/test_detection_contract.py:379`.
- `tests/pr_submit/fixtures/decline-comment.json` — `tests/pr_submit/test_detection_contract.py:357`.
- `tests/pr_submit/fixtures/decline-initial-poll.json` — `tests/pr_submit/test_detection_contract.py:367`.
- `tests/pr_submit/fixtures/decline-twice.json` — `tests/pr_submit/test_idempotency.py:107`.
- `tests/pr_submit/fixtures/fail-soft-empty.json` — `tests/pr_submit/test_silence.py:36`.
- `tests/pr_submit/fixtures/finding-duplicate.json` — `tests/pr_submit/test_reply_resolve.py:151`.
- `tests/pr_submit/fixtures/finding-empty.json` — `tests/pr_submit/test_edge_cases.py:61`.
- `tests/pr_submit/fixtures/finding-fresh-comment-id.json` — `tests/pr_submit/test_reply_resolve.py:150`.
- `tests/pr_submit/fixtures/finding-high.json` — `tests/pr_submit/test_severity_router.py:74`.
- `tests/pr_submit/fixtures/finding-malformed.json` — `tests/pr_submit/test_edge_cases.py:170`.
- `tests/pr_submit/fixtures/finding-max.json` — `tests/pr_submit/test_edge_cases.py:77`.
- `tests/pr_submit/fixtures/finding-medium-high.json` — `tests/pr_submit/conftest.py:80`, `tests/pr_submit/test_autonomy_gates.py:116`.
- `tests/pr_submit/fixtures/finding-medium.json` — `tests/pr_submit/test_severity_router.py:73`.
- `tests/pr_submit/fixtures/finding-needs-human.json` — `tests/pr_submit/test_edge_cases.py:124`.
- `tests/pr_submit/fixtures/finding-ungroundable.json` — `tests/pr_submit/test_autonomy_gates.py:152`.
- `tests/pr_submit/fixtures/merge_tree_conflict.z` — read as bytes through a direct path (not `load_fixture`): `tests/pr_submit/test_conflicts_core.py:66` (definition) and `:170` (`FIXTURE.read_bytes()`).
- `tests/pr_submit/fixtures/opt-in-241.json` — `tests/pr_submit/test_silence.py:61`, `tests/pr_submit/test_detection_contract.py:427`.
- `tests/pr_submit/fixtures/rereview-attributed.json` — `tests/pr_submit/test_review_retrigger.py:60`.
- `tests/pr_submit/fixtures/round-sequence-2.json` — `tests/pr_submit/test_edge_cases.py:142`.
- `tests/pr_submit/fixtures/round-sequence-residual-x3.json` — `tests/pr_submit/test_loop_guard.py:62`.
- `tests/pr_submit/fixtures/silence-empty.json` — `tests/pr_submit/test_silence.py:29`.
- `tests/pr_submit/fixtures/stale-decline-pre-watermark.json` — `tests/pr_submit/test_detection_contract.py:539`.
- `tests/pr_submit/fixtures/summary-only.json` — `tests/pr_submit/test_silence.py:67`, `:73`, `:122`.

## Add to .gitignore

None. No cache, build output or runtime artifact is present in this batch.

## Remaining / Not Audited

None. All 50 files were classified.

## Wiring check (.py files)

Searched all of `tests/pr_submit/*.py` for `Optional[Callable`, `Callable[...] | None`, `Callable | None`, `*_REGISTRY`, `*_DISPATCH`, `*_HANDLERS`, `*_ROUTER` and `*_BUILDERS`: no matches. `tests/pr_submit` is not a `steps/`, `handlers/`, `validators/` or `checks/` directory. No `[wiring]` entries.

## Summary

- **Total files audited**: 50 / 50 assigned
- **DELETE**: 0 | **REVIEW**: 5 | **KEEP**: 45 | **.gitignore**: 0
- **Coverage**: 50/50 = 100%
- Count check: 5 Need Decision + 45 Keep + 0 Delete = 50; remaining 0.
- The batch holds 2 Python support files (`__init__.py`, `conftest.py`), 10 test modules, 37 JSON fixtures and 1 `.z` fixture.

## Notes

- Caveat from the scanner: hidden-path referrers are cited but not audited. It did not run a repo-wide search for the string `fixtures/` outside `tests/pr_submit` (for example in `Makefile` or `.github/`); the checks it did run (`pr_submit/fixtures|pr_submit\.fixtures` over the repo, and the five-pattern check on `tests/pr_submit`) found no loader of `tests/pr_submit/fixtures` outside the suite. The only repo-wide hit for `pr_submit/fixtures` was a stale CHANGELOG mention of `tests/pr_submit/test_hook_update.py`, which is not in this batch.
- The test counts in the test-module entries are `def test_` counts, not reference counts.
- Orchestrator note: the scanner returned its report as text and the orchestrator wrote it here, because `audit-scanner` has only Read, Grep and Glob.
