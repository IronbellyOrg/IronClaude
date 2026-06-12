# QA Report — Research Depth

**Topic:** Reflect wrapper marker leakage into §6.1 step 5.5 verification subprocess
**Date:** 2026-06-11
**Phase:** research-depth
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Research depth check | Result | Evidence |
|---|----------------------|--------|----------|
| 1 | R1 traces propagation hop-by-hop rather than listing files | PASS | Read `01-marker-propagation-trace.md`. It identifies the marker constant/guard in `commands.py`, both `runner.py` export sites, `ClaudeProcess.build_env()` inheritance/overlay semantics, process launch, grandchild pytest inheritance, and guard-trip failure path. Fresh verification reads confirmed `commands.py` guard at lines 38-73, `runner.py` audit/apply export at lines 405-448, reverify loop at lines 531-572, and `process.py` env-copy/update/Popen handoff at lines 145-192. |
| 2 | R2 explains §6.1.1 verification envelope and env-strip composition deeply enough to write the skill edit | FAIL | Read `02-verification-envelope-surface.md` and fresh-read `src/superclaude/skills/sc-reflect-protocol/SKILL.md:489-502`. R2 correctly identifies the eight controls and explains why a protocol-authored `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <base command>` wrapper must be added after base-command validation. However, it does not provide exact replacement/addition text for new control (i) or the control-(b) wording tweak, despite the lens requiring enough detail for the builder to write the exact `SKILL.md` edit without guessing. R2 also has contradictory status (`Status: In Progress` at line 3, `Status: Complete` at line 87). |
| 3 | R3 gives concrete runnable regression-test design and matches R2's strip token | PASS | Read `03-test-design.md`. It provides the target test file, helper extraction function, test name, exact assertions for `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` and `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`, and the exact verification command `uv run pytest tests/cli/reflect/test_no_nesting_guard.py tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q`. Fresh reads confirmed `test_no_nesting_guard.py` already uses source-text contract tests and `_REPO_ROOT`; `test_cli_smoke.py` and `test_promote_plumbing.py` invoke `reflect_group` at the cited surfaces. |
| 4 | R4 gives actual Template 02 sections and actual contract §3 text, not a paraphrase | PASS | Read `04-conventions-contract-template.md` and fresh-read the contract §3 lines 76-108. R4 quotes the marker, why-it-exists, wrapper semantics, generator obligations, safe gate shape, and exact-string truthy rule. It also enumerates Template 02 required sections and relevant B2/B3/B4/C/E/F/I/L rules with line-cited evidence. |
| 5 | Builder can create per-item checklist items from research alone without re-reading source | FAIL | The research is close, but the task builder would still need to invent exact prose for the `SKILL.md` control-(i) addition and the control-(b) validation-order amendment. R4 supplies exact contract-amendment prose; R3 supplies exact test code shape; R2 supplies the mechanism but not the exact edit text. |

## Summary

- Checks passed: 3 / 5
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Minor issues: 0
- Fix authorization: false; no files modified except this QA report.
- Confidence: Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 13 | Grep/rg via Bash: 1 | Glob: 0 | Bash: 1 | Web/Tavily: 0

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | `02-verification-envelope-surface.md` §3 / §4 | R2 tells the builder to add control (i) and tweak control (b), but does not provide exact prose for either edit. Because the requested lens asks whether the builder can write the exact `SKILL.md` edit without guessing, this is not deep enough: the builder must still author the normative wording and decide how to phrase validation order, wrapper authorship, and `env` non-allowlisting. | Add a concrete proposed `SKILL.md` patch text block: the exact replacement for control (b) and the exact new control (i), including validation order, `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <base verification command>`, prohibition on adding `env`/`timeout` as user-selectable allowlist verbs, preservation of controls (a)/(c)/(g)/(h), and optional `marker_stripped` audit field guidance if desired. |
| 2 | IMPORTANT | `02-verification-envelope-surface.md` lines 3 and 87 | R2 has an internal status contradiction: the header says `Status: In Progress`, while the footer says `Status: Complete`. This undermines whether downstream task-builder should treat the research as final. | Change the header status to `Complete` if the research is final, or keep `In Progress` and explicitly list the remaining unresolved research gaps. |

## Research-Depth Notes by Lens Focus

1. **R1 propagation trace:** Deep enough. It gives a causal chain from constants to `ClaudeProcess` env overlay to grandchild inheritance to the exact CLI guard failure.
2. **R2 envelope/composition:** Mechanistically strong but not task-builder-ready at the exact-edit level. It identifies the right surface and safe composition, but stops short of byte-level or paragraph-level replacement text.
3. **R3 regression design:** Deep enough for a B2 test item. The source-text contract test is appropriate because the implementation surface is the skill body, not a Python verification helper. The asserted strip token matches R2's recommended wrapper substring.
4. **R4 template/contract:** Deep enough. It quotes contract §3 material and provides task-shaping rules that can drive MDTM item construction.
5. **Per-item checklist readiness:** Mostly ready, but blocked by R2's lack of exact control text. A high-quality corrective task should not force the builder to invent normative safety-envelope wording.

## Recommendations

- Patch R2 before task building: add exact `SKILL.md` edit prose for control (b) and new control (i), and resolve the status contradiction.
- After R2 is patched, the research should be sufficient to build checklist items for: contract carve-out edit, `SKILL.md` envelope edit, regression content test, targeted pytest command, `make sync-dev`, `make verify-sync`, lint/format checks, and final POST wrapper dogfood gate.

## QA Complete

VERDICT: FAIL
