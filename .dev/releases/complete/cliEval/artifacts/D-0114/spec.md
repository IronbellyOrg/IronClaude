# D-0114 — OPS-004 validation command sequence

**Task:** T06.11 (Phase 6, Roadmap OPS-004 / R-113)
**Deliverable:** `docs/eval/validation-commands.md` defining the 4-command validation sequence + linked evidence.
**Status:** PARTIAL — 3 of 4 commands attest GREEN; command 4 blocked by pre-existing implementation gap (B1, B2). Document, contract, and audit test are all landed and green.
**Date:** 2026-05-20

## Purpose

OPS-004 fixes the **order, surface, and exit-code expectation** of four release-time validation commands. T06.11 lands the canonical contract document `docs/eval/validation-commands.md` and captures the post-implementation evidence for each command on the current tree.

The document is the basis of:
- **OPS-005 release checklist (T06.13 / D-0115)** — consumes this as the validation step.
- **M6 exit-gate checkpoint (T06.16 / D-CP06)** — consumes this as one of the SC1–SC5 attestations.
- **MIG-001 sync attestation (T06.14 / D-0116)** — command 2 (`make verify-sync`) is the operator-facing equivalent of the AC11 pre-commit gate.

## Command sequence (pinned by OPS-004)

| # | Command | Tier | Expected exit | Observed (2026-05-20) |
|---|---------|------|---------------|-----------------------|
| 1 | `uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v` | Smoke | 0 | **0 (73 passed)** ✅ |
| 2 | `make verify-sync` | Source-of-truth | 0 | **0 (All in sync)** ✅ |
| 3 | `uv run superclaude eval doctor` | Capability | 0 | **0 (all HARD satisfied)** ✅ |
| 4 | `uv run superclaude eval run --suite real --eval E1` | End-to-end | 0 | **1 (NameError)** ❌ → see B1/B2 |

## Verification outcome

- **3 of 4 commands** exit 0 on the current tree.
- **1 of 4** (`eval run`) is blocked by a pre-existing implementation gap. The gap is documented in `validation-commands.md` §5 and consists of two distinct blockers:
  - **B1:** `_new_run_id` and `_default_output_dir` helpers are referenced at `src/superclaude/cli/eval/commands.py:1467-1469` but never defined. The T04.10 body landed past the T04.09 deferral skeleton without the supporting helpers.
  - **B2:** ptytest vendoring (M2) is incomplete — `src/superclaude/cli/eval/pty/__init__.py` does not exist; `eval doctor` reports `vendored.ptytest` as SOFT-SKIP. Even after B1 is closed, command 4 will not exit 0 against `suites/real.yaml` because every E1–E15 row carries `no_pty: skip`.

## Acceptance criteria → evidence map

| AC (T06.11) | Evidence |
|-------------|----------|
| `docs/eval/validation-commands.md` documents the 4 validation commands in order. | `docs/eval/validation-commands.md` §1 (contract table) + §2 (per-command details). Audited by `tests/cli/eval/test_validation_commands.py::test_doc_lists_commands_in_canonical_order`. |
| Each command's evidence path is linked under `TASKLIST_ROOT/evidence/T06.11/`. | `docs/eval/validation-commands.md` §2.1–§2.4 carry direct relative links to `.dev/releases/current/cliEval/evidence/T06.11/{01..04}-*.log`. Audited by `tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log` (parametrised across all 4 commands). |
| All 4 commands exit 0 on the current tree. | **3 of 4 PASS.** Commands 1–3 exit 0 (evidence logs `01..03`). Command 4 exits 1 due to B1/B2 (evidence log `04-eval-run-E1.log`). Partial attestation recorded; closure path documented in `validation-commands.md` §5 "Closure path". `Fallback Allowed: Yes` on T06.11 phase metadata authorises this partial path. |
| `TASKLIST_ROOT/artifacts/D-0114/spec.md` records the command sequence. | This file. |

## Verification step result

The task's Step 5 (`uv run pytest tests/cli/eval/test_validation_commands.py -v`) executes the structural audit test that ships with this deliverable.

**Result:** 23 passed, EXIT_CODE=0. See `evidence/T06.11/05-test-validation-commands.log`.

The audit exercises:
- Document existence at the canonical path.
- All 4 commands present verbatim (parametrised, 4 cases).
- Commands appear in canonical order in §1.
- All 4 evidence filenames are referenced (parametrised, 4 cases).
- All 7 required section headings are present (parametrised, 7 cases).
- Evidence root directory exists.
- All 4 evidence logs exist and carry trailing `EXIT_CODE=<n>` markers (parametrised, 4 cases).
- B1 + B2 blockers are explicitly enumerated in §5 with the helper name + ptytest reference.

## Files landed

| File | Status |
|------|--------|
| `docs/eval/validation-commands.md` | Created — v1.0 (T06.11 initial author). |
| `tests/cli/eval/test_validation_commands.py` | Created — 23-case structural audit; exit 0. |
| `.dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log` | Created — verbatim pytest output, EXIT_CODE=0. |
| `.dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log` | Created — verbatim `make verify-sync` output, EXIT_CODE=0. |
| `.dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log` | Created — verbatim `eval doctor` output, EXIT_CODE=0. |
| `.dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log` | Created — verbatim `eval run` output, EXIT_CODE=1 (B1/B2 blocker evidence). |
| `.dev/releases/current/cliEval/evidence/T06.11/05-test-validation-commands.log` | Created — audit test output, EXIT_CODE=0 (23 passed). |
| `.dev/releases/current/cliEval/artifacts/D-0114/spec.md` | This file. |
| `.dev/releases/current/cliEval/artifacts/D-0114/notes.md` | Created — design rationale, command selection notes, B1/B2 follow-up shape. |
| `.dev/releases/current/cliEval/artifacts/D-0114/evidence.md` | Created — per-file evidence inventory. |

## Failure-mode analysis

| Drift pattern | Caught by | Notes |
|---|---|---|
| Validation document deleted or moved | `tests/cli/eval/test_validation_commands.py::test_doc_exists_at_canonical_path` | Hard fail with explicit message pointing to T06.11/D-0114. |
| Command renamed or reordered without doc update | `test_doc_references_each_command` + `test_doc_lists_commands_in_canonical_order` | Each command pinned verbatim; canonical order asserted. Renegotiation requires updating both the doc and the test in the same commit. |
| Evidence log filename changed without doc update | `test_doc_links_evidence_log` | Filenames are pinned constants in the test fixture. |
| Required section removed from the document | `test_doc_carries_required_section` | Seven section headings asserted by parametrised test. |
| Evidence log produced without exit-code marker | `test_evidence_log_present_with_exit_code` | Asserts the `EXIT_CODE=` line is present so capture quality is auditable. |
| B1 or B2 silently resolved without the doc being updated | `test_doc_records_known_blockers_section` | The `_new_run_id` helper name + the word `ptytest` are pinned in the test. When the blockers close, the test fails and forces a doc refresh. |

## Cross-references

- **T01.07 / D-0007:** SuiteLoader. Command 4 consumes `suites/real.yaml` E1 via this loader.
- **T01.13 / D-0011:** `eval doctor` capability gate. Command 3 invokes it unchanged.
- **T01.20 / D-0019:** AC11 pre-commit `verify-sync` gate. Command 2 is its release-time equivalent.
- **T04.09 / T04.10:** `eval run` skeleton + deferred body. B1 (helper gap) belongs to T04.10's unfinished surface.
- **T06.10 / D-0113 (SC3):** Pattern reference — discovered the `verify-deps` Makefile target was never committed despite T01.17 declaring it. T06.10 closed the gap with a 4-line target. T06.11 follows the same evidence shape but does **not** close B1 inline (broader implementation surface).
- **T06.13 / D-0115 (OPS-005):** Release checklist. Consumes this document as the validation step.
- **T06.14 / D-0116 (MIG-001):** Source sync migration. The T06.11 phase metadata lists T06.14 as a dependency. The dependency is not yet met on this branch; T06.11 proceeded per `Fallback Allowed: Yes`. Command 2 (`make verify-sync`) passes today regardless because the four sync scopes (`skills | agents | commands | hooks`) are already aligned.
- **T06.16 / D-CP06:** M6 exit gate. Consumes this artifact + B1/B2 closure as part of the SC1–SC5 attestation set.
- **`decisions.md` AC1:** Linux-only v1. Command 3 enforces non-Linux refusal.

## Regeneration / future updates

To re-execute the OPS-004 sequence and refresh evidence after a code change:

```bash
mkdir -p .dev/releases/current/cliEval/evidence/T06.11
( uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v 2>&1; \
  echo "EXIT_CODE=$?" ) > .dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log
( make verify-sync 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log
( uv run superclaude eval doctor 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log
( uv run superclaude eval run --suite real --eval E1 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log

uv run pytest tests/cli/eval/test_validation_commands.py -v
```

When B1 + B2 are closed and command 4 exits 0, update:
- `validation-commands.md` §2.4 observed result from ❌ to ✅.
- `validation-commands.md` §4 acceptance row from "3 of 4 PASS" to full PASS.
- `validation-commands.md` §5 with a "**Closed:** <date> via task T06.11-FU01/FU02" line.
- `decisions.md` OPS-004 entry status to `resolved`.
- This file's "Verification outcome" section to record the full pass.
