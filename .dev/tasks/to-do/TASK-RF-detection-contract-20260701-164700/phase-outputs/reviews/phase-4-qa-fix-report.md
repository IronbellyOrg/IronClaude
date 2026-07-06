# QA Report — Phase 4 Fix Cycle (test-strength remediation)

**Topic:** Locked Detection Contract Setup Flow — Phase 4 test-strength fixes
**Date:** 2026-07-02
**Phase:** fix-cycle
**Lens:** phase-4-test-fix
**Fix cycle:** 1
**Fix authorization:** true (test files only; production source frozen)

---

## VERDICT: PASS

Both consolidated findings (P4-QA-001 CRITICAL, P4-QA-002 MINOR) are resolved with
**real, non-tautological** fixes. The two target test files pass (14/14), `ruff check`
and `ruff format --check` are clean on both files, and **no production source under
`src/` was modified in this session** (only the two test files were edited).

Root-cause posture (adversarial): each finding was a *hollow guard*, not a cosmetic
nit. Both are now fixed at the root — the CLI redaction test now actually drives the
`validation_summary:` leak vector with a planted sentinel, and the integration test now
binds the no-side-effect boundary with a static import audit + a real no-writes snapshot
instead of inert recorders.

---

## Finding-by-finding resolution

| ID | Severity | File | Root cause | Fix applied | Proof it is real (not tautological) |
|---|---|---|---|---|---|
| P4-QA-001 | CRITICAL | `tests/cli/reflect/test_contract_status_cli.py` | The only CLI redaction test ran in an empty `isolated_filesystem()` ⇒ `state=missing`, no evidence, so the `validation_summary:` echo (`commands.py` L179-182 — the strongest CLI leak vector) was never reached; `assert _RAW_BODY_SENTINEL not in output` passed trivially. | **Added** `test_contract_status_validate_output_redacts_raw_payload_body` (existing test kept, now annotated). It plants a `locked:true` override + a probe under `<cwd>/.dev/pr-monitor/probes/pr-9/` whose `combined-payload.json` carries `_RAW_BODY_SENTINEL` in **both** `reviews[].body` and `comments[].body`, then invokes `contract-status --validate --repo owner/repo --pr 9`. Asserts `state: ready` + `validation_summary:` ARE present (the redaction path was actually exercised) and `evidence_sha256:`/`blocker_count:` metadata ARE present, while the sentinel is ABSENT. First asserts the sentinel + `"body"` key are genuinely on disk so a leak *could* surface. | Mutation check: monkeypatching `ValidationReport.summary()` to append `body=<SENTINEL>` makes the sentinel appear in CLI output → the new `assert SENTINEL not in output` **fails**. Guard is live. |
| P4-QA-002 | MINOR | `tests/pr_submit/test_contract_setup_pr_submit_integration.py` | `test_diagnose_and_render_perform_no_side_effects` built six `_Recorder`s but `diagnose`/`render` take **no seam args**, so the recorders were never wired; `for rec in (...): assert rec.calls == 0` was tautologically true (would pass even if the path armed). | **Replaced** the inert loop with two real guarantees: (1) a **static import-graph audit** (mirrors `test_contract_setup_writer.py::test_writer_package_imports_no_fsm_seams`) asserting the whole `contract_setup` graph — including `diagnosis` — imports no `fsm`/`monitor`/`reply_resolve`/`review_retrigger` seam and exposes no `arm_monitor`; (2) a **no-writes snapshot** (`before == after` over `tmp_path.rglob("*")`) around a full `diagnose()` + `render()`. Kept the real `next_command` string assertions. `_Recorder` retained (still used by tests 1-4 with genuine ordering/baseline semantics). | Import audit verified empirically (9 modules, 0 violations, `diagnosis` in graph, `arm_monitor` absent). No-writes snapshot verified empirically (diagnose/render create 0 files). Neither assertion is vacuous — both would fail on a real regression (a seam import or any write). |

---

## Files changed (this session)

| File | Change | Production source? |
|---|---|---|
| `tests/cli/reflect/test_contract_status_cli.py` | Added `import json`; annotated the existing metadata-only test; added `_plant_locked_evidence_with_sentinel_body` helper + `test_contract_status_validate_output_redacts_raw_payload_body`. | No (test only) |
| `tests/pr_submit/test_contract_setup_pr_submit_integration.py` | Added `import sys` + `from pathlib import Path`; replaced the tautological six-recorder loop in `test_diagnose_and_render_perform_no_side_effects` with a static import-graph audit + a no-writes snapshot. | No (test only) |

**Production source frozen:** verified with `git diff --stat` — I made zero Edit/Write
calls against any `src/` file. Pre-existing working-tree modifications to
`src/superclaude/cli/reflect/commands.py` and other `src/` files predate this session
(they are the Phase-4 production code under test) and were untouched here.

**Existing tests not weakened:** the pre-existing `test_contract_status_output_is_metadata_only`
is kept verbatim (only a docstring note added). `_Recorder` is preserved because
integration tests 1-4 still use it for real arm-ordering/baseline assertions.

---

## Verification commands run

```text
# Target test files — 14 passed (8 CLI incl. new test, 6 integration)
uv run pytest tests/cli/reflect/test_contract_status_cli.py \
              tests/pr_submit/test_contract_setup_pr_submit_integration.py -q
  => 14 passed in 0.20s

# Lint + format on the two files — clean
uv run ruff check  tests/cli/reflect/test_contract_status_cli.py \
                   tests/pr_submit/test_contract_setup_pr_submit_integration.py
  => All checks passed!
uv run ruff format --check tests/cli/reflect/test_contract_status_cli.py \
                           tests/pr_submit/test_contract_setup_pr_submit_integration.py
  => 2 files already formatted

# Adversarial pre-write probe: --validate reaches validation_summary AND redacts
  => EXIT 0, state=ready, validation_summary emitted, SENTINEL_IN_OUTPUT: False,
     SENTINEL on disk (reviews+comments body): True

# Mutation check: injected leak in ValidationReport.summary()
  => SENTINEL appears in CLI output => new test would FAIL (guard is non-trivial)

# Broader regression: tests/pr_submit/ + tests/cli/reflect/
uv run pytest tests/pr_submit/ tests/cli/reflect/ -q
  => 436 passed, 1 xpassed, 6 failed
```

### Note on the 6 broader-regression failures (pre-existing, unrelated)

The 6 failures are in `tests/pr_submit/test_hook_update.py` (4) and
`tests/pr_submit/test_static_grep.py` (2). They fail on a **missing hook script**
(`src/superclaude/hooks/scripts/offer-pr-review.sh` — `FileNotFoundError`) and
source-file static-grep gates. Neither failing module references either of the two
files I edited, and my two target files are fully green in isolation (14/14). These
failures are pre-existing Phase-infrastructure gaps outside this fix cycle's scope and
are NOT introduced or affected by this remediation.

---

## Confidence Gate

- **Confidence:** Verified: 2/2 findings resolved with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 9 | Grep: 2 | Glob: 0 | Bash: 6 (2 empirical probes, 1 mutation check, 2 test runs, 1 git/diff audit)
- No web research performed (all verification local-file / execution-bound); Tavily-first N/A.

Both findings mapped to a specific fix + a specific proof-of-non-triviality (mutation
check for P4-QA-001; empirical import-audit + no-writes snapshot for P4-QA-002).

## QA Complete
