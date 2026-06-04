# QA Report — Task Qualitative (Post-Completion Operational Validation)

**Topic:** Auto-Resume as the Default for sprint run / rerun-tasks (v4.3.5)
**Date:** 2026-06-02
**Phase:** task-qualitative (executed-task operational validation)
**Fix cycle:** N/A (no fixes required)
**Document type:** Executed Task File
**fix_authorization:** true (none needed — see Issues Found)

---

## Overall Verdict: PASS

The feature was validated against **actual on-disk outputs and live CLI execution**, not
just planned checklist items. Every safety-critical path was exercised end-to-end with real
synthetic interrupted-release fixtures through the installed `uv run superclaude` entrypoint
(which resolves to this worktree's source). All reused symbols exist with the exact signatures
the new code calls. The completion-scope claims in the task log are honest. Zero operational
defects were found; the one apparent failure during verification was a measurement artifact of
my own harness (documented below), not a code defect.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | `sprint run --help` + `rerun-tasks --help` show `--fresh/--restart/--yes/--dry-run` with coherent text; `--dry-run` on a synthetic interrupted release printed plan+drift+gate correctly |
| 2 | Project-convention compliance | none | PASS | No `.claude/` distributable modified (`git status` clean except settings); no bare `python -m`/`pip` in new source; version 4.3.5 consistent across pyproject.toml + `__init__.py` + `uv run superclaude --version` |
| 3 | Intra-phase execution simulation | none | PASS | Real operator flow traced: interrupted sprint → bare `sprint run --dry-run` → detect→print→gate→drift all coherent; CliRunner end-to-end ran the rerun engine to PASS |
| 4 | Function signature verification | none | PASS | `run_rerun_tasks` called in `_dispatch_resume_rerun` with all 13 keyword-only args matching the real signature (the QA-log CRITICAL fix is present); `_preserved_dest(3 args)`, `_declared_deliverables(2)`, `acquire_recovery_lock(2)`, `invoke_sonnet(prompt,*,timeout)` all match |
| 5 | Module context analysis | none | PASS | Resume package import chain is clean and does NOT transitively pull the broken `retrospective.py`; lazy imports avoid circular deps (executor→rerun_tasks hash fn) |
| 6 | Downstream consumer analysis | none | PASS | INV-001 verified end-to-end: executor writes `tasklist_sha256` via `_content_sha256_excluding_rerun_block(phase.file)`; DriftAssessor reads the same fn over the same file → Tier-0 1.00 match confirmed live |
| 7 | Test validity | none | PASS | Tests exercise real fixtures with representative input; AC-4/AC-5 record the original baseline so Tier-0 genuinely misses; QA-added mutation-proven over-claim test present |
| 8 | Test coverage of primary use case | none | PASS | 17 deterministic + 3 real-subprocess e2e + updated contract = 36 passing; e2e drives bare `sprint run`/`rerun-tasks` through the full pipeline |
| 9 | Error path coverage | none | PASS | Non-interactive-without-`--yes` STOPs exit 2 with actionable guidance; ambiguous STOPs exit 2 with candidates; drift<0.8 STOPs exit 2 with `--start`/`--fresh` guidance; over-claim STOPs with blocking_reasons |
| 10 | Runtime failure-path trace | none | PASS | All four failure paths traced live (non-tty, ambiguous interleaved ledger, AC-5 completed-task material edit, last-completed over-claim) — each STOPs cleanly, none hang/crash |
| 11 | Completion-scope honesty | none | PASS | "Regression-free, blocked only by pre-existing breakage" verified: `summarizer.py`/`retrospective.py` git-clean, `invoke_haiku` ImportError predates task, broken test modules don't reference resume; 5.7 honestly left unchecked + status still "Doing" |
| 12 | Ambient dependency completeness | none | PASS | New flags on both subcommands; `_auto_resume`/`_dispatch_resume_rerun`/`_print_resume_decision` helpers wired; `resume/__init__.py` re-exports the three public classes; CLI imports succeed |
| 13 | Kwarg sequencing | none | PASS | No deferred-action ordering defects; all 13 `run_rerun_tasks` kwargs supplied at the single call site |
| 14 | Function existence claims | none | PASS | grep-verified ALL reused symbols exist (`_classify_transcript`, `_declared_deliverables`, `_content_sha256_excluding_rerun_block`, `acquire_recovery_lock`, `release_recovery_lock`, `write_recovery_audit_log`, `restore_from_bundle`, `_preserved_dest`, `invoke_sonnet`, `run_rerun_tasks`, `discover_phases`, `_resolve_release_dir`, `discover_failed_tasks_from_transcripts`); `invoke_haiku` confirmed ABSENT (correctly mapped to `invoke_sonnet`) |
| 15 | Cross-reference accuracy | none | PASS | result.json schema (`task_results[].task.task_id` + `.status` via `TaskResult.to_dict`) matches what planner reads; PhaseStatus PASS-family + TaskStatus values match classifier usage |

## Summary
- Checks passed: 15 / 15
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (none required)
- Confidence: Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 11 | Grep: ~14 (via Bash) | Glob: 0 | Bash: 16

## Issues Found
None. (No CRITICAL, IMPORTANT, or MINOR operational defects.)

### Verification artifacts that initially looked like defects (resolved — NOT issues)

1. **Apparent AC-9 failure ("--phase is required") — measurement artifact, NOT a defect.**
   My first CliRunner trace ran the REAL rerun engine, which **merged back** and flipped
   T03.02 from `fail_recoverable` → `pass` in `phase-3-result.json`. On the subsequent bare
   `rerun-tasks` call the planner then correctly found no recoverable per-task failures and
   fell to the explicit-required guidance. After restoring a fresh `fail_recoverable`
   result.json, bare `rerun-tasks` auto-detected `phase 3, tasks T03.02` perfectly and ran
   the engine to PASS. This actually *proves* the merge-back loop (AC-2) is real and
   auto-detect is idempotent (won't re-nominate already-passing tasks). No code change needed.

2. **Apparent non-interactive `EXIT=0` — pipe artifact.** The `EXIT=0` was `grep`'s exit
   status, not the CLI's. Re-running without a pipe showed the true exit code is **2** with
   the message routed to stderr, exactly per design (NFR-4).

3. **`--restart`/`--fresh` dual-dest Click option — benign.** Two `@click.option` decorators
   bind `--fresh` and `--restart` to the same `fresh` dest. For `is_flag` options Click
   handles this correctly; `--restart` verified to disable auto-detect identically to
   `--fresh` on both subcommands.

## Operational paths validated live (real CLI, synthetic interrupted release)
- **Tier-0 INV-001 exact hash:** unchanged tasklist → drift 1.00 (tier hash). Executor-written
  hash matched DriftAssessor-computed hash end-to-end.
- **AC-4 cosmetic:** trailing-whitespace/format-only → 0.90 (≥0.8 proceeds).
- **AC-5 material edit:** removed a COMPLETED task T03.01 → 0.30 < 0.80 → STOP exit 2 with
  "Re-run with --start to re-execute, or --fresh to discard state."
- **DD-2/R1 over-claim:** last-completed PASS-claim with no/empty transcript → Signal B derives
  INCOMPLETE → suspect → gate STOP with blocking_reasons. The conservative re-check is
  intentional, and a genuinely-completed task (transcript with a `result` event + output
  tokens present on disk — the executor streams `output_format=stream-json` to that exact file
  during the task) validates and the gate PASSes, so legitimate resumes are not spuriously
  blocked.
- **AC-6 nothing-to-resume:** all-complete → "Nothing to resume", exit 0.
- **AC-7 explicit bypass:** `--start 1` (and `--start 4`) bypass auto-resume via Click
  ParameterSource, NOT value comparison — 0 auto-resume-plan lines printed; falls to legacy path.
- **AC-8 ambiguous:** interleaved phase_start ledger → STOP exit 2 listing the conflict.
- **AC-9 parity:** bare `rerun-tasks` auto-detects phase 3 / T03.02 == explicit `--phase/--tasks`.
- **PHASE hard-crash:** no result.json, no transcripts → granularity=PHASE, gate vacuously
  passes, whole phase re-run via executor loop (NG1) — safe because nothing is skipped.

## Actions Taken
None. No in-place fixes were necessary; the feature is operationally correct as shipped.
Per scope discipline I did NOT touch the pre-existing-broken unrelated modules
(`retrospective.py` / `summarizer.py` test breakage), consistent with the task's instructions.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
No `## Inherited Structural Verdict` section was provided in the spawn prompt; this is a
post-completion operational review run standalone. I performed full independent verification
(no structural reliance): every symbol grep-verified against source, every CLI path executed
live, every reused signature read from the actual callee.

## Self-Audit
**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was passed; I re-verified independently throughout.

**(b) Independent semantic checks (≥1 required, INV-019):**
- `run_rerun_tasks` kwarg completeness — read the real signature at `rerun_tasks.py:1210-1225`
  (13 keyword-only params, no defaults) and confirmed all 13 supplied at `commands.py:480-494`.
- INV-001 same-fn-same-file hash — read both write side (`executor.py:2077`) and read side
  (`drift.py` Tier 0) and proved a live Tier-0 1.00 match on an unedited fixture.
- DD-2/R1 over-claim defense — read `_classify_transcript` (`rerun_tasks.py:550-598`), confirmed
  empty transcript → INCOMPLETE, then proved the gate STOPs live on a PASS-claim with no transcript.
- Completion honesty — git-verified `summarizer.py`/`retrospective.py` untouched and the
  `invoke_haiku` ImportError predates the task, validating the "regression-free" log claim.

**Self-Audit answers:**
1. Independently verified ~25+ factual claims against source (13 reused symbols, 13-kwarg
   dispatch, INV-001 both sides, status enums, result.json schema, version triple, 8 live CLI
   acceptance paths).
2. Files read: `resume/models.py`, `resume/planner.py`, `resume/integrity.py`,
   `commands.py` (run/rerun_tasks/_auto_resume/_dispatch/_print), `executor.py:2053-2083` +
   `:1095-1118`, `rerun_tasks.py:550-598/924-958/1210-1225`, `recovery.py:275`, `config.py`,
   `models.py` (TaskResult/TaskStatus/PhaseStatus), task file, design.md, CHANGELOG.md, docs diff.
3. If 0 issues seemed implausible: I found and resolved 3 apparent-failures (proving I probed
   adversarially), traced 8 acceptance paths through the LIVE installed CLI, and executed the
   real rerun engine end-to-end — not document inspection.
4. No web research was required (purely local-file + CLI verification); Tavily was not invoked.

## Recommendations (non-blocking)
- **MINOR doc nit (not a defect):** CHANGELOG says "16 deterministic tests"; the suite actually
  collects **17** (`tests/sprint/test_resume.py`). This under-claims, so it is not misleading —
  optionally update to 17. Not gating.
- **Follow-up (already tracked in the task, correctly out-of-scope):** the pre-existing
  `invoke_haiku` → `invoke_sonnet` dangling import in `retrospective.py:34` breaks
  `test_summarizer.py`/`test_retrospective.py` collection and the "full suite green" gate (5.4).
  This is genuinely pre-existing (git-clean, predates the task) and the resume feature's own
  import chain is unaffected. Recommend a separate one-line-per-site remediation task.
- **5.7 remains the only open item** (task status → Done) and is honestly unchecked. Once the
  operator is satisfied, flip frontmatter `status` to "🟢 Done" and set `completion_date`.

## QA Complete

VERDICT: PASS
