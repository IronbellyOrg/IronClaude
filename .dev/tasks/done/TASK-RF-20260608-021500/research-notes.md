# Research Notes: PRD pipeline halt-on-hard-failure + missing-artifact guard

**Date:** 2026-06-08
**Scenario:** A (explicit — driven by a completed troubleshoot diagnosis)
**Depth Tier:** Standard
**Track Count:** 1
**Source of evidence:** `.dev/troubleshoot/prd-scope-discovery-missing-artifact-20260608020200/REPORT.md` (Tier 2, confidence 0.90, all citations validated inline + corroborated by self-review). Copied to `research/00-troubleshoot-report.md`. Self-review refinements in `research/01-self-review-findings.md`.

---

## EXISTING_FILES

All under `src/superclaude/cli/prd/` (source of truth; `make sync-dev` mirrors to `.claude/` — but this is Python package code, NOT a skill/agent/command, so it ships from `src/` via the package, no `.claude/` mirror concern). Tests under `tests/`.

- `src/superclaude/cli/prd/models.py` — `PrdStepStatus` enum (line 99); `is_failure` property (lines 145-152, includes ERROR/TIMEOUT/QA_FAIL_EXHAUSTED/VALIDATION_FAIL/HALT); `is_success` (136); `is_terminal`. **Edit target:** add `is_hard_failure` property.
- `src/superclaude/cli/prd/executor.py` — Stage-A loop (541-575); halt logic (567-575, currently STRICT-gate-only); `_run_subprocess_step` (655-755); artifact persist guard (744-749, `if exit_code == 0`); `_determine_status` (757-788, exit!=0 → ERROR at 770-771); `_build_prompt` (1196-1232, called at 672 OUTSIDE the try/except at 688-695); `run()` try/finally no-except (517, 597); `except OSError` at 701 (raw_output read — different region, no collision). **Edit targets:** halt condition (567-575); catch MissingArtifactError at the `_build_prompt` call site (672).
- `src/superclaude/cli/prd/prompts.py` — `_read_file` (42-47, unguarded `read_text`); `_load_json` (37-39, unguarded `read_text`); REQUIRED Stage-A reads: `_read_file` at 257 (scope-discovery-raw.md), 340 (research-notes.md), 440 (research-notes.md); `_load_json` at 158 & 258 (parsed-request.json). OPTIONAL Stage-B `_derive_*` reads correctly guarded at 740/755/775/787 (`.is_file()`). **Edit targets:** add `MissingArtifactError`, `_read_required`, `_load_json_required`; convert the 5 required reads.
- `src/superclaude/cli/prd/gates.py` — `GATE_CRITERIA` (310-521); scope-discovery STANDARD (331-335); research-notes STRICT (336-353). Read-only reference (no edit).
- `tests/` — prd pipeline tests; `test_e2e.py` monkeypatches `_build_prompt` at ~line 549 (Atom 2 regression test must NOT stub it). **Edit target:** add regression tests.

## PATTERNS_AND_CONVENTIONS

- Status classification centralized in `PrdStepStatus` properties (`is_failure`/`is_success`/`is_terminal`) — add `is_hard_failure` as a sibling property, same set-membership idiom.
- Halt is expressed by setting `result.outcome = "halt"`, `result.halt_step`, `result.halt_reason`, then `break` out of the Stage-A loop (executor.py:570-575).
- Artifact reads in builders use module helpers `_read_file` (str) and `_load_json` (dict). Stage-B `_derive_*` helpers already use the `.is_file()`-guard pattern (prompts.py:787) — the fix makes Stage-A consistent with that established pattern.
- `MissingArtifactError` should subclass `FileNotFoundError` (so any un-caught path still reads as a file-not-found, and it composes with existing `except OSError`/`FileNotFoundError` semantics) while carrying `path` + `producer_step` for a clear message.
- UV for all Python ops. Edit `src/`, then `make sync-dev` + `make verify-sync` (defensive — prd cli is package code, but the repo convention runs it regardless). Fix/feature branch only.

## GAPS_AND_QUESTIONS

- Exact line of the `_build_prompt` call inside `_run_subprocess_step` is 672 (verified); the catch can wrap that call or live inside `_build_prompt`. Builder should choose the call-site wrap so the resulting `PrdStepResult(status=HALT)` flows through the normal return path and the Stage-A loop's (Atom-1-updated) halt check.
- Confirm the `PrdStepResult` constructor signature for building a HALT result with a `halt_reason` (executor.py around 620, 751). Builder verifies before writing the item.

## RECOMMENDED_OUTPUTS

Code changes (src/superclaude/cli/prd/): models.py (+1 property), prompts.py (+1 class, +2 helpers, 5 converted reads), executor.py (halt condition + MissingArtifactError catch). Tests (tests/): Atom 1 halt-on-ERROR + no-halt-on-VALIDATION_FAIL; Atom 2 graceful-HALT-on-missing-artifact (real `_build_prompt`); e2e scope-discovery-ERROR halts before research-notes.

## SUGGESTED_PHASES

1. **Atom 1 (foundation):** models.py `is_hard_failure` → executor.py halt condition. Tests for halt-on-ERROR / no-halt-on-VALIDATION_FAIL.
2. **Atom 2 (backstop, depends on Atom 1):** prompts.py MissingArtifactError + `_read_required`/`_load_json_required` + convert 5 reads → executor.py catch at 672 → HALT. Test with real `_build_prompt`.
3. **Verification:** full e2e (scope-discovery ERROR halts before research-notes; no traceback). `make sync-dev` + `make verify-sync` + `uv run pytest` for the prd suite + `make lint`.

## TEMPLATE_NOTES

Template 02 (complex) — discovery (confirm signatures) + build + test, with a hard ordering dependency (Atom 2 depends on Atom 1's `is_hard_failure` to actually halt on the HALT status it raises). Standard tier. PER_PHASE QA not required; FINAL_ONLY validation + UNIT testing.

## AMBIGUITIES_FOR_USER

None — intent is clear from the troubleshoot REPORT.md and the verified codebase citations. The self-review's two findings (the `_read_file`/`_load_json` type split; the Atom-1-before-Atom-2 ordering) are already resolved and baked into this research.
