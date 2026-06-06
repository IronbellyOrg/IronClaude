# Research: Gate Resolutions (gap-fill)

**Topic type:** Gap-fill / gate-finding resolution
**Status:** Complete
**Date:** 2026-06-04

Resolves the substantive rf-qa research-gate findings before the builder runs. The two builder-affecting
corrections below OVERRIDE the corresponding parts of research 02 / 03.

---

## R1 — Compile-check command MUST be `python -m`-free (overrides research 03 §validation)

CLAUDE.md:7 (verified): "Never use `python -m`, `pip install`, or `python script.py` directly."

Therefore the generated task MUST NOT encode `uv run python -m py_compile <file>`. Use ONE of:
- **Preferred:** `uv run python -c "import py_compile; py_compile.compile('src/superclaude/cli/sprint/rerun_tasks.py', doraise=True)"` (single-line, compliant, raises on syntax error).
- Or rely on the full `uv run pytest tests/sprint/ -q` run, which imports the edited modules and surfaces
  any syntax/import error as a collection error (no separate compile step needed).

The task SHOULD prefer the `pytest`-as-compile-proof approach for simplicity, and MAY add the
`python -c "import py_compile..."` one-liner per edited file as an explicit fast pre-check. NEVER
`python -m py_compile`.

## R2 — Handoff regression test belongs in `test_resume_contract.py` (overrides research 02 §handoff)

`tests/sprint/test_resume_contract.py:8` imports `is_validated_success`; `:55-70` is
`test_is_validated_success_only_for_pass_plus_gate_success`, which parametrizes
`(status, gate) → expected` cases over `HandoffRecord`. This is the PRIMARY handoff-predicate test surface
(research 02 pointed only at test_handoff_record.py and missed this).

If the task fixes `handoff.py.is_validated_success`, the handoff regression test MUST extend
`test_is_validated_success_only_for_pass_plus_gate_success` with a case asserting
`PASS_RECOVERED + GateOutcome.PASS → is_validated_success == True` (RED pre-fix, GREEN post-fix). Mirror
the existing case construction in that test (read it for the exact `HandoffRecord` fixture shape and the
`GateOutcome` enum import).

## R3 — Doc-hygiene findings (acknowledged, non-blocking)

- research 03 doc-claims lack [CODE-VERIFIED]/[UNVERIFIED] tags — the analyst + rf-qa independently
  re-verified the template/CLAUDE.md claims against current files; built-task correctness is unaffected.
- research 03 cites `.claude/templates/...`; canonical SoT is `src/superclaude/templates/...` (the
  `.claude/` mirror is currently synced). The builder reads the template content either way; the built
  task is unaffected. (Builder should cite `src/superclaude/templates/...` in the task's
  `template_schema_doc` frontmatter for SoT correctness.)

## Net effect on the build
Two corrections to fold into the BUILD_REQUEST: (R1) compliant compile command, (R2) handoff test in
test_resume_contract.py. All else from research 01/02/03 stands.
