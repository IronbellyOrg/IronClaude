# QA Report — Phase 4 Qualitative (task-integrity / synthesis-gate-equivalent)

**Lens:** operator-output-redaction
**QA_MODE:** task-integrity
**Date:** 2026-07-02
**Fix authorization:** false (report-only)
**Adversarial stance:** Assume a raw payload body leaks into a status/summary string and the tests don't catch it. Find the leak. Verify by reading the actual files.

---

## VERDICT: FAIL

Rationale in one line: the four redaction *surfaces* are all implemented correctly and provably do NOT leak (verified by reading the source AND by an inline sentinel-driven probe), but the **CLI status-output surface is redaction-tested only in an empty/`missing`-state filesystem where no raw body is ever planted** — so the checklist item-1 guarantee ("plant a sentinel raw payload body … assert absent from the CLI status output") is hollow on the CLI boundary. The single most plausible CLI leak vector (`validation_summary:` echoing `report.summary()` line-by-line under `--validate`) is exercised by no test. This is the AX-4 "trivially-passing-test" pattern and triggers the stated PASS/FAIL rule: *"FAIL on … any surface conflation left untested."*

Important nuance for the reader: **there is no actual leak in the production code.** The implementation redacts on all four surfaces. The FAIL is a *test-guard* gap — the tests do not actually guard the CLI redaction boundary they claim to.

---

## Boundary → Test-name matrix

| Redaction surface | Sentinel planted into a real body? | Asserted ABSENT from the surface's own output? | Exercised through the real render path? | Guard status |
|---|---|---|---|---|
| `Diagnosis.summary()` | YES — `_write_evidence` plants `RAW_BODY_SENTINEL` in `reviews[].body`; asserted still on disk (diagnosis.py test L354) | YES — `test_summary_omits_raw_payload_bodies` L356 | YES — real `diagnose(cwd=...)` → `VALIDATION_MISSING`, real `.summary()` | **SOLID** |
| `Diagnosis.summary()` (MISSING-state shape) | N/A (no payload) but shape asserted body-free | YES — `test_summary_omits_raw_bodies_across_all_states` L368 | YES | SOLID (shape guard) |
| `EvidenceBundle.summary()` | YES — sentinel in `reviews`/`comments`/`check_runs` bodies; asserted loaded (evidence.py L269) | YES — `test_evidence_summary_omits_raw_payload_bodies` L271; plus `test_raw_sentinel_still_present_in_on_disk_json` L300 | YES — real `load_evidence` → `.summary()` | **SOLID** |
| `ValidationReport.summary()` | YES — two independent files: `test_contract_setup_evidence.py::test_validation_summary_omits_raw_payload_bodies` L288 and `test_contract_setup_validation.py::test_validation_summary_omits_raw_payload_bodies` L285 (also asserts `'"body"' not in summary` L286) | YES | YES — real `derive_candidate` → `validate_candidate` → `.summary()` | **SOLID** |
| **CLI `contract-status` status output** | **NO** — `test_contract_status_output_is_metadata_only` runs in `isolated_filesystem()` with **no evidence and no override** ⇒ `state=missing`, no `validation_summary` block ever emitted | Assertion present (`_RAW_BODY_SENTINEL not in result.output` L156) **but unexercised** — no body is ever in scope to leak; also `assert "body:" not in result.output` L157 (structural, partial) | **NO** — the `validation_summary:` echo block (commands.py L179-182) and the populated-`blockers` echo (L170-173) are never reached with a real payload in any CLI test | **HOLLOW** |

---

## Adversarial probe (inline, not committed)

To confirm whether the *implementation* leaks (separate from whether the *tests* catch it), I drove sentinel-bearing evidence through the exact CLI path the tests avoid: an isolated cwd containing a `locked:true` override + a `combined-payload.json` whose `reviews[].body` carried `ADVERSARIAL_PROBE_SENTINEL_ZZZ`, then invoked `reflect contract-status --validate --repo o/r --pr 42`.

Result: `EXIT 0`, `state=ready`, the `validation_summary:` block WAS emitted (23 checks, sha256, counts), and `SENTINEL_IN_OUTPUT: False`. So the production CLI redacts correctly even on the full validate/ready path. The leak vector is closed *in code* — but the test suite never demonstrates it, which is the gap this report flags.

---

## Source verification of each surface (why no implementation leak exists)

- `EvidenceBundle.summary()` (evidence.py L38-53): emits only `probe_dir`, `repo`, `pr_number`, `captured_at`, `surfaces`, `omitted_surfaces`, `counts=…` (lengths), `sha256`, `pagination_complete`, `cross_pr_shape_only`. No body field rendered.
- `ValidationReport.summary()` (validation.py L40-60): emits `result`, `classifier_result`, `expected_result`, and **counts** (`len(checks)`, `len(failed_checks)`, `len(negative_controls)`, `len(blockers)`), `evidence_sha256`, `validated_surfaces`, `decline_validation`. Crucially the per-check `detail` strings are NOT rendered (only counted), and every `detail` in validation.py is a static/field-name string — no `detail` embeds a body. No leak.
- `Diagnosis.summary()` (diagnosis.py L42-60): emits `state`, `checked_paths` **count**, `override_present`, evidence path, evidence sha256, report path, `validation_result`, `blockers` **count**, `next_command`. Blocker strings are counted, not rendered; and all blocker strings in diagnosis.py are static (no payload interpolation). No leak.
- CLI `_render_contract_status` (commands.py L145-186): echoes `diagnosis.blockers` **in full** (L172-173) and `validation_summary` (= `report.summary()`) **line-by-line** (L179-182), plus `validation_error` (L184). Because diagnosis blockers are static and `report.summary()` is body-free, the CLI does not leak. `validation_error` is an exception string from `{ContractSetupError, OSError, ValueError, FileNotFoundError}`; none of those are raised with a body payload in the current code (minor residual vector, see MINOR-1).

---

## Checklist results

| # | Checklist item | Result | Evidence |
|---|---|---|---|
| 1 | Sentinel raw body planted & asserted absent from `Diagnosis.summary()`, `EvidenceBundle.summary()`, `ValidationReport.summary()`, AND CLI status output | **FAIL** | First three surfaces: SOLID (matrix rows 1-4). CLI surface: HOLLOW — sentinel never planted into a payload the CLI reads; `validation_summary`/populated-`blockers` echo paths untested with a real body. |
| 2 | Summaries include ONLY status/paths/hashes/counts/blockers (metadata), not raw bodies | **PASS** | Verified by source read of all four render sites (see above) and by the inline probe (`SENTINEL_IN_OUTPUT: False`). |
| 3 | Omitted surfaces asserted DISTINCT from present/validated surfaces (not conflated) | **PASS** | `test_present_and_omitted_surfaces_are_distinct`, `test_omitted_surface_not_conflated_with_empty_present_surface` (empty-but-present ≠ omitted), `test_all_surfaces_present_leaves_omitted_empty`; `EvidenceBundle` renders `surfaces` and `omitted_surfaces` on separate lines; validation report carries `validated_surfaces` distinctly. |

---

## Findings

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| CRIT-1 | CRITICAL | `tests/cli/reflect/test_contract_status_cli.py::test_contract_status_output_is_metadata_only` (L147-157) | The only CLI redaction test runs in an empty `isolated_filesystem()` ⇒ `state=missing`, no evidence, no `validation_summary` block. `assert _RAW_BODY_SENTINEL not in result.output` is trivially true because the sentinel is never planted into any payload the CLI reads. The `validation_summary:` echo of `report.summary()` (commands.py L179-182) — the strongest CLI leak vector — and the populated-`blockers` echo (L170-173) are asserted body-free by no test. Checklist item 1 is unmet for the CLI surface. | Add a CLI test that: (a) writes a `locked:true` override + a `combined-payload.json` whose `reviews[].body`/`comments[].body`/`check_runs[].output.text` carry a sentinel, under the isolated cwd; (b) invokes `contract-status --validate --repo … --pr …` so the run reaches `state=ready` and emits the `validation_summary:` block; (c) asserts the sentinel is ABSENT from `result.output` while `validation_summary:` IS present (proving the redaction path, not the empty path, was exercised). The inline probe in this report is a ready template. |
| MINOR-1 | MINOR | `src/superclaude/cli/reflect/commands.py` L133-134, L184 | `validation_error = f"validation failed: {exc}"` is echoed verbatim (L184). If any future `load_evidence`/`validate_candidate`/`write_report` code path raised an exception whose message interpolated a payload body, it would leak through this line. No current code path does so, so this is theoretical — but there is no test pinning `validation_error` as body-free. | Add a regression assertion (in the same new CLI test or a sibling) that a forced-`validation_error` path (e.g. malformed evidence that raises `ValueError`) does not echo any sentinel body; or route `validation_error` through a redaction helper. |

---

## Self-Audit

**(a) Reliance list — no `## Inherited Structural Verdict` block was supplied in the spawn prompt.** This review therefore ran standalone (no rf-qa PASS items to rely on); all boundary claims were verified by direct source read + execution, not by relying on an upstream structural verdict.

**(b) Independent semantic checks (≥1 required, INV-019):**
- **Surface redaction is real, not asserted** — Read `evidence.py` L38-53, `validation.py` L40-60, `diagnosis.py` L42-60, `commands.py` L145-186 and confirmed each render site emits metadata/counts only; confirmed `ValidationReport.summary()` renders `len(blockers)` (count) not blocker strings, and no `CheckResult.detail` in validation.py embeds a body.
- **CLI leak-path exercised for real** — Ran an inline `CliRunner` probe planting `ADVERSARIAL_PROBE_SENTINEL_ZZZ` in a body and driving `contract-status --validate` to `state=ready`; observed `validation_summary:` block emitted with `SENTINEL_IN_OUTPUT: False` — proving the implementation redacts AND that the existing CLI test never reaches this path.
- **Coverage gap located by grep** — `grep -n "RAW_BODY_SENTINEL\|isolated_filesystem\|write_text\|combined-payload" tests/cli/reflect/test_contract_status_cli.py` + reading `conftest.py::cli_runner` (bare `CliRunner()`, no evidence fixture) confirmed no CLI test plants a sentinel-bearing payload.
- **Item-3 distinctness verified against source** — Confirmed `EvidenceBundle.summary()` emits `surfaces=` and `omitted_surfaces=` on separate lines and the three distinctness tests assert non-overlap (`not (set(surfaces) & set(omitted))`).

---

## Confidence

**Confidence:** Verified: 3/3 checklist items adjudicated with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 3 | Glob: 0 | Bash: 4 (incl. 1 inline execution probe + 1 pytest confirmation run)

Self-audit answers:
1. Factual claims independently verified against source: all four redaction surfaces (4 source render sites), the CLI fixture, the loader hashing path, and one end-to-end execution — every boundary claim mapped to a specific Read/Bash.
2. Files read: `merged-requirements.md`; the 6 pr_submit test files + 1 CLI test file (assigned); source `evidence.py`, `validation.py`, `diagnosis.py`, `cli/reflect/commands.py`, `cli/reflect/conftest.py`.
3. Why trust a non-empty finding: I did not merely read the tests — I executed the untested CLI path with a planted sentinel and demonstrated both that the code redacts and that no test covers it. The FAIL is grounded in an observed coverage gap, not a hunch.
4. Web research: none performed (all verification was local-file/execution-bound); Tavily-first N/A this review.

---

## Tool-engagement summary

- Tavily: not used (no external lookup required — review was local-file + execution bound).
- Fallback: none (no web research performed).

## QA Complete
