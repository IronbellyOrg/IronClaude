# D-0114 — verification evidence

**Task:** T06.11 (Phase 6, Roadmap OPS-004 / R-113)
**Date:** 2026-05-20
**Tier:** STANDARD (Verification Method: Direct test execution).

## 1. Files landed

| File | Status |
|------|--------|
| `docs/eval/validation-commands.md` | Created — v1.0 (OPS-004 contract; 7 structural sections, 4-command sequence). |
| `tests/cli/eval/test_validation_commands.py` | Created — 23-case structural audit (12 distinct test functions, 4 parametrised across the four commands, 7 parametrised across required sections). |
| `.dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log` | Created — verbatim `uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v` output. **EXIT_CODE=0** (73 passed). |
| `.dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log` | Created — verbatim `make verify-sync` output. **EXIT_CODE=0** (`✅ All components in sync.`). |
| `.dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log` | Created — verbatim `uv run superclaude eval doctor` output. **EXIT_CODE=0** (all HARD capabilities satisfied; 3 SOFT-SKIPs noted). |
| `.dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log` | Created — verbatim `uv run superclaude eval run --suite real --eval E1` output. **EXIT_CODE=1** (NameError: `_new_run_id` is not defined — B1 blocker captured for follow-up). |
| `.dev/releases/current/cliEval/evidence/T06.11/05-test-validation-commands.log` | Created — verbatim audit-test output. **EXIT_CODE=0** (23 passed). |
| `.dev/releases/current/cliEval/artifacts/D-0114/spec.md` | Created — verification outcome record. |
| `.dev/releases/current/cliEval/artifacts/D-0114/notes.md` | Created — command-selection rationale, B1/B2 follow-up shape, dependency T06.14 fallback rationale. |
| `.dev/releases/current/cliEval/artifacts/D-0114/evidence.md` | This file. |

## 2. AC: document records the 4 validation commands in order

`docs/eval/validation-commands.md` §1 (table) and §2.1–§2.4 (per-command
details) list the canonical four-command sequence:

1. `uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v`
2. `make verify-sync`
3. `uv run superclaude eval doctor`
4. `uv run superclaude eval run --suite real --eval E1`

Canonical-order assertion is enforced by
`test_doc_lists_commands_in_canonical_order` in
`tests/cli/eval/test_validation_commands.py` (audit log line 38 in
`evidence/T06.11/05-test-validation-commands.log` shows PASS).

## 3. AC: each command's evidence path is linked under TASKLIST_ROOT/evidence/T06.11/

§2 of `validation-commands.md` carries direct relative links from each
command to its evidence log:

| Command | Evidence link |
|---------|---------------|
| 1 | `evidence/T06.11/01-targeted-pytest.log` |
| 2 | `evidence/T06.11/02-make-verify-sync.log` |
| 3 | `evidence/T06.11/03-eval-doctor.log` |
| 4 | `evidence/T06.11/04-eval-run-E1.log` |

The audit test `test_doc_links_evidence_log` (parametrised across all 4
commands) verifies each filename appears in the document. All four
parametrised cases PASS in `evidence/T06.11/05-test-validation-commands.log`.

## 4. AC: all 4 commands exit 0 on the current tree

**Status: PARTIAL — 3 of 4 PASS.**

| Command | Observed exit | Status |
|---------|---------------|--------|
| 1 (targeted pytest) | 0 (73 passed) | ✅ |
| 2 (`make verify-sync`) | 0 (all in sync) | ✅ |
| 3 (`eval doctor`) | 0 (all HARD satisfied) | ✅ |
| 4 (`eval run --suite real --eval E1`) | **1** (NameError at `commands.py:1467`) | ❌ |

The partial result is authorised by `Fallback Allowed: Yes` on the
T06.11 phase metadata. The two blockers (B1: missing `_new_run_id` /
`_default_output_dir` helpers; B2: ptytest vendoring incomplete) are
documented in `validation-commands.md` §5 with named follow-up tasks
(T06.11-FU01 + T06.11-FU02) and a "Closure path" section that walks the
operator through completing the attestation once the blockers close.

## 5. AC: artifacts/D-0114/spec.md records the command sequence

`artifacts/D-0114/spec.md` (this triplet's spec file) carries:

- The OPS-004 contract table (4 commands × tier × expected exit ×
  observed exit on 2026-05-20).
- The verification outcome summary (3 of 4 PASS + B1/B2 explanation).
- The acceptance-criteria → evidence map.
- The files-landed inventory (10 files).
- A failure-mode analysis covering 6 drift patterns.
- Cross-references to T01.07, T01.13, T01.20, T04.09/10, T06.10, T06.13,
  T06.14, T06.16, AC1.
- A regeneration / future-updates section with the operator recipe + the
  exact sequence of doc edits required when B1+B2 close.

## 6. Verification step result

T06.11 Step 5 calls for `uv run pytest tests/cli/eval/test_validation_commands.py -v`.
Captured at `evidence/T06.11/05-test-validation-commands.log`:

```
============================== 23 passed in 0.05s ==============================
EXIT_CODE=0
```

The 23 cases break down as:

- 1 — `test_doc_exists_at_canonical_path`.
- 4 — `test_doc_references_each_command` (parametrised, one per command).
- 1 — `test_doc_lists_commands_in_canonical_order`.
- 4 — `test_doc_links_evidence_log` (parametrised, one per command).
- 7 — `test_doc_carries_required_section` (parametrised, one per section heading).
- 1 — `test_evidence_root_directory_exists`.
- 4 — `test_evidence_log_present_with_exit_code` (parametrised, one per evidence log).
- 1 — `test_doc_records_known_blockers_section`.

All 23 PASS.

## 7. Tier classification rationale

Tier=STANDARD per phase-6-tasklist.md T06.11 metadata block ("Verification
Method: Direct test execution"). The task lands a documentation deliverable
plus an audit test plus 5 evidence logs. The direct-test-execution
verification is the audit test that ships with the deliverable, which
exercises the document shape and evidence presence in 23 parametrised
cases. The four operator-facing validation commands themselves are
executed once at landing to populate the evidence logs and then re-executed
on release day by OPS-005 (T06.13) — they are not run by the audit test
itself (rationale in `notes.md` §"On the audit test design").

## 8. Reproducibility

To re-verify on a clean checkout:

```bash
# 1. Install dependencies (matches CI).
uv pip install -e ".[dev]"

# 2. Re-execute the OPS-004 four-command sequence.
mkdir -p .dev/releases/current/cliEval/evidence/T06.11
( uv run pytest tests/cli/eval/test_describe.py tests/cli/eval/test_doctor.py -v 2>&1; \
  echo "EXIT_CODE=$?" ) > .dev/releases/current/cliEval/evidence/T06.11/01-targeted-pytest.log
( make verify-sync 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/02-make-verify-sync.log
( uv run superclaude eval doctor 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/03-eval-doctor.log
( uv run superclaude eval run --suite real --eval E1 2>&1; echo "EXIT_CODE=$?" ) \
  > .dev/releases/current/cliEval/evidence/T06.11/04-eval-run-E1.log

# 3. Run the audit test.
uv run pytest tests/cli/eval/test_validation_commands.py -v
```

Expected outcomes on the **current** tree (with B1/B2 still open):

- log 01 → EXIT_CODE=0, 73 passed.
- log 02 → EXIT_CODE=0, "All components in sync."
- log 03 → EXIT_CODE=0, "all HARD capabilities satisfied."
- log 04 → EXIT_CODE=1, NameError on `_new_run_id`.
- audit test → 23 passed.

Expected outcomes **after** B1+B2 close:

- log 04 → EXIT_CODE=0, structured PASS outcome for E1.
- The "B1" and "B2" headings in `validation-commands.md` §5 will need
  a `**Closed:** <date>` marker, after which
  `test_doc_records_known_blockers_section` will need adjustment (or
  the section can be renamed to a historical archive once both close).

## 9. Follow-on coordination

- **T06.11-FU01 (recommended new task):** Land `_new_run_id` +
  `_default_output_dir` helpers in `src/superclaude/cli/eval/commands.py`.
  Minimum scope documented in `notes.md` §"B1 …".
- **T06.11-FU02 (recommended new task):** Land M2 ptytest vendoring under
  `src/superclaude/cli/eval/pty/`. Blocks on the original M2 plan owner.
- **T06.12 (Checkpoint P06-T07-T11):** Consumes this artifact as the
  OPS-004 evidence for the mid-phase checkpoint. Must record B1/B2 as
  the partial-pass justification.
- **T06.13 (OPS-005 release checklist):** Consumes the four-command
  sequence; the checklist's validation step is a direct re-execution
  of `validation-commands.md` §6.
- **T06.16 (Phase 6 end-of-phase checkpoint):** Consumes this artifact +
  B1/B2 closure status as one of the SC1–SC5 attestations for M6 exit.
