# QA Report — Report Validation (R1.4 Interim Phase-9 Checkpoint, after Step 9.5)

**Topic:** R1.4 tool-write migration (Steps 9.1–9.5) — dual-write generator parity
**Date:** 2026-06-02
**Phase:** report-validation (interim, sc:reflect H3 hardening)
**Fix cycle:** N/A (initial pass)
**Stance:** Adversarial — assume silent semantic drift, lossy schemas, broken dual-write defaults, or regressions. fix_authorization: true.

---

## Overall Verdict: PASS

R1.4 Steps 9.1–9.5 are clean. All 7 zero-trust checks passed against the actual
files and freshly-run tests. No silent semantic drift, no lossy schema, no broken
dual-write defaults, no regression, no `return True` fragility stubs introduced.
The migration is correctly dual-write (every flag defaults FALSE) and the
markdown production path is provably unchanged.

**Adversarial finding (NOT an R1.4 issue):** the full roadmap suite shows **3**
pre-existing failures, not the **1** the spawn prompt disclosed. All three share
one root cause (`config.agents[1].model == "sonnet"`, tests expect `"haiku"`) and
all three fail **identically on clean HEAD** (verified by stashing the R1.4
working changes and re-running). They are the same haiku-vs-sonnet default-agents
mismatch family the prompt flagged as known-unrelated; the prompt simply
under-counted them. Per instructions these are NOT counted as R1.4 issues and
were NOT fixed. Documented here for completeness so the count is not mistaken for
an R1.4 regression. See Check 7 / appendix.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cumulative parity tests green + assert RENDERED structure + gate frontmatter/min_lines | PASS | `pytest` 4 files → **43 passed in 0.35s**. Read all 4 test bodies: `test_render_parity` asserts rendered section headers/frontmatter `key:` lines/ids; `test_rendered_*_satisfies_gate_frontmatter` iterates `<GATE>.required_frontmatter_fields` (alias-tuple aware) + asserts `rendered.count("\n") >= <GATE>.min_lines`. Gates confirmed real (gates.py:1150 EXTRACT_TDD_GATE 19 fields/min_lines=50; gates.py:1190 GENERATE_A_GATE 3 fields/min_lines=100). |
| 2 | No regression in test_prompts.py; markdown default branch intact | PASS | `pytest test_prompts.py` → **11 passed in 0.18s**. prompts.py: each `build_*_prompt` has `if tool_write:` early-return for JSON; default path returns `base + _OUTPUT_FORMAT_BLOCK` (extract L503, extract_tdd L754, diff L1200) / `+ _INTEGRATION_ENUMERATION_BLOCK + _OUTPUT_FORMAT_BLOCK` (generate L1120). Per-step `test_build_*_prompt_*` (4) assert `md` branch contains `<output_format>`. |
| 3 | Dual-write flags default FALSE (models + commands) | PASS | models.py L127–130: `tool_write_extract`/`_extract_tdd`/`_generate`/`_diff` all `bool = False`. commands.py L174–205: all four `--tool-write-*` click options `is_flag=True, default=False`. |
| 4 | No silent semantic loss — extract_tdd full 19-field/14-section parity (not 13-field subset) | PASS | extract_tdd.schema.json frontmatter `required` lists all 19 fields (L19–37); 6 TDD design arrays present (data_models/api_specifications/component_inventory/testing_strategy/migration_plan/operational_readiness). extract_tdd.md.j2 emits all 19 frontmatter `key:` lines (L2–20) + all 14 `## ` sections (8 standard + 6 TDD, L23–145). The 13-field-subset defect is fixed and held. |
| 5 | Contract #3 — generate phantom-ID rejection before write; neither .md nor .json written | PASS | tool_writer.py `render_step_tool_write_with_id_check` (L354) runs `_parse_and_validate` then `validate_id_subset` (L388) BEFORE `_persist_and_render` (L394); returns `id_errors` early on phantom id → no write. Targeted `test_generate_rejects_phantom_id` → **1 passed**; it asserts `not out.exists()` AND `not roadmap.json exists` on phantom FR-99, and full write on clean subset. |
| 6 | No new `return True` fragility stubs in tool_writer/prompts/executor | PASS | `grep "return True"`: 0 in tool_writer.py, 0 in prompts.py. executor.py has 10 pre-existing `return True` (gate/cycle logic); `git diff HEAD` shows **0** added-line (`^+`) `return True` in executor — none introduced by R1.4. tool_writer failure paths return error lists, success returns `[]`. |
| 7 | Live path intact (executor render-hook + _build_steps; dispatch) | PASS | `pytest test_executor.py test_dispatch_reachability.py` → **78 passed in 0.34s**. The 3 suite-wide failures are pre-existing (fail identically on stashed-clean HEAD), unrelated to R1.4. |

## Summary

- Checks passed: **7 / 7**
- Checks failed: **0**
- Critical issues (R1.4): **0**
- Issues fixed in-place: **0** (none found)
- Pre-existing non-R1.4 failures observed: **3** (haiku/sonnet default-agents; left untouched per instructions)

**Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 6 | Grep: 5 | Glob: 0 | Bash: 9 (web research: none required — all claims are local source/test, source-truth-first)

Tool-engagement note: tool calls comfortably exceed the 7-check minimum and each maps to a specific check (test runs → C1/C2/C7/C5; Reads of tool_writer.py/schema/template/test bodies/gates → C1/C4/C5; greps → C3/C6; stash round-trip → C7 adversarial HEAD comparison).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| — | — | — | No R1.4 issues found. | — |

## Actions Taken

- No fixes applied — no R1.4 defects found. (fix_authorization was true; nothing required fixing.)
- During Check 7 I created and then **dropped** a temporary `git stash` to compare the 3 failing tests against clean HEAD. Working tree fully restored afterward (`git status` re-verified: all 5 modified roadmap files + untracked tool_writer.py/templates/ present). No working-tree changes left behind by QA.

## Appendix — Pre-existing failure proof (Check 7 adversarial)

`uv run pytest tests/roadmap/` → **3 failed, 1827 passed, 12 skipped**. The 3:
- `test_cli_contract.py::TestAgentsParsing::test_default_agents_when_not_provided`
- `test_models.py::TestRoadmapConfig::test_default_agents`
- `test_validate_unit.py::TestValidateConfigDefaults::test_default_agents_two`

All assert `config.agents[1].model == "haiku"`, actual `"sonnet"`. With the R1.4
working changes stashed (HEAD-clean), the same 3 fail identically (`3 failed`),
and `git diff HEAD src/.../models.py` shows no touch to haiku/sonnet/default
agents. Therefore pre-existing, not R1.4. Not counted, not fixed (per spawn
instruction).

## Recommendations

- Green light to proceed to Step 9.6+ of the R1.4 migration. No remediation required for 9.1–9.5.
- Non-blocking, separate concern: the haiku/sonnet default-agents test mismatch (3 tests) should be triaged in its own fix outside R1.4 — it predates this work and is orthogonal.

## HALT-PRECEDENCE

No regression found that I could not fix (there is no R1.4 regression at all). No HALT condition.

## Final cumulative test count

R1.4-scope tests: **43** (parity) + **11** (prompts) + **78** (executor/dispatch) = **132 passed, 0 failed**.
Full roadmap suite: **1827 passed, 3 failed (all pre-existing, non-R1.4), 12 skipped**.

## VERDICT: PASS

## QA Complete

---
