# QA Report — task-qualitative (Operational Validation)

**Topic:** TASK-RF-20260602-060714 — R1-R5 remediation from PR #112/#111
**Date:** 2026-06-02
**Phase:** task-qualitative (post-completion operational validation)
**Fix cycle:** N/A (first pass)
**Branch:** refactor/roadmap-pipeline-r0-r1-rewrite
**Stance:** Adversarial — assume operational defects unit tests missed.

---

## Overall Verdict: PASS

All 6 operational checks verified with independent tool engagement (Read + Bash
end-to-end probes). One MINOR log-completeness nit found and FIXED in-place
(md_ids count missing from `_save_id_registry` INFO log). No unfixable issues.

---

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | End-to-end MD round-trip (extract → to_dict sidecar → gates reconstruction → containment) | none | PASS | Ran live `uv run python` probe: `build_id_registry` emits `md_ids=('M1-D01','M2-D3')`; `to_dict()['md_ids']` carries them; reconstructed registry's `union_of_known()` includes MD ids; `extract_roadmap_ids` of a roadmap citing `M1-D01`/`M2-D3` yields zero violations. Raw-form MD ID written by build_id_registry IS recognized as known by the Contract #9 check. |
| 2 | R2 executor reset ordering / no-clobber | none | PASS | Read executor.py:3399-3429 (helper) + call site 3532. Reset runs at run-start AFTER `_build_steps`/dry-run guard, BEFORE `_apply_resume` (3538) and BEFORE any step's `_save_id_registry`→`set_id_registry_sidecar_path` (650-664). `config.output_dir` valid at call. Resume-aware: re-points to persisted sidecar when `resume and sidecar.exists()`, else fail-shut to None. Does NOT clobber freshly-set sidecar (extract runs later). |
| 3 | R4 shell happy-path + empty + malformed-ERE | none | PASS | Ran script 4 ways: (a) multi-file git repo → correct domain inventory, Total files: 3, EXIT 0; (b) empty repo → Total files: 0, EXIT 0 (no false diagnostic); (c) all-files-excluded → EXIT 0; (d) malformed `EXCLUDE: [unclosed` → EXIT 1 with diagnostic, no silent empty inventory. `rc<=1→success` correctly separates grep no-match (1) from fatal ERE (≥2). Normal multi-file enumeration intact. |
| 4 | arch_lint docstring skip over-suppression | none | PASS | Read arch_lint.py:141-209. `docstring_node_ids` built only from `body[0]` Expr-wrapping-str-Constant of Module/Class/Func/AsyncFunc = exact Python docstring position. Skip at 192 matches on `id(node)` (object identity), so a same-valued literal elsewhere (e.g. `X = "M\d+-D-?\d+"`) gets distinct id() and still flags. Non-docstring first statements (import/if/non-str Expr) fail the `isinstance(..str)` guard and are NOT treated as docstrings. `make lint-architecture` Check 11 = green (0 errors). |
| 5 | Downstream consumers / frozen SpecIdRegistry `md_ids` required field | none | PASS | `grep -rn "SpecIdRegistry("` → exactly 5 sites (id_registry.py:167, gates.py:1090, envelope.py:381, 2 test sites). No 6th. ALL use keyword args and supply `md_ids` (build_id_registry via `families.get("MD",())`; gates/envelope via `.get("md_ids",())` for back-compat; tests explicit). No positional construction that the new field would shift. |
| 6 | Test sanity + verify-sync | none | PASS | `uv run pytest -q tests/roadmap/ tests/contracts/` → 1973 passed, 12 skipped. `make verify-sync` → All components in sync. Fixture `milestone_id_case.expected.json` md_ids (`M1-D01,M1-D02,M2-D01,M2-D02,M3-D01`) match live extractor; MD/D dedup confirmed (bare-D = D03/D04/D05, MD-trailing D01/D02 stripped). |

---

## Summary

- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (FIXED in-place)
- Issues fixed in-place: 1

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | `src/superclaude/cli/roadmap/executor.py:666-674` | `_save_id_registry` INFO log enumerated FR/NFR/SC/G/D/accepted counts but omitted the new `md_ids` count. Operationally harmless (sidecar JSON correctly persists md_ids via `to_dict()`; gate reads it) — purely a log-completeness gap that would under-report MD-family extraction in operator logs. | Added `%d MD` placeholder + `len(registry.md_ids)` arg. FIXED. |

---

## Actions Taken

- Fixed log-completeness nit in `src/superclaude/cli/roadmap/executor.py:667` by
  adding `%d MD` to the persisted-registry INFO format string and
  `len(registry.md_ids)` to the args tuple (additive; placeholder count now 7/7).
- Verified fix: re-ran `uv run pytest -q tests/roadmap/test_spec_roadmap_id_containment.py`
  → 12 passed; `make verify-sync` → clean. Edit is in canonical SoT
  (`src/superclaude/cli/roadmap/`); CLI package is NOT a sync-dev target
  (only skills/agents/commands mirror to `.claude/`), confirmed no `.claude/cli`
  exists — so no `.claude/` staging concern.
- No fail-shut branch, SemanticCheck signature, or POSIX shell behavior was
  touched. No ID-pattern body was inlined (MD body `r"M\d+-D-?\d+"` remains
  solely in `contracts/__init__.py:71`; arch-lint Check 11 green).

---

## Notable Non-Defects (adversarial probes that did NOT yield findings)

1. **Surface-form sensitivity in Contract #9 gate is pre-existing, family-agnostic
   — NOT an R5 regression.** Live probe: a spec declaring `M1-D01` whose roadmap
   writes the canonical `M1-D1` would be flagged by the gate (raw-set difference),
   because canonicalization lives only in the `structural_checkers` layer, not the
   gate layer. I confirmed the **bare-D family (predates this task) behaves
   identically**: spec `D01`/`D-05` vs roadmap `D1`/`D5` → same violations. The two
   layers are intentionally separated (gate = raw fail-shut phantom detection;
   checker = drift-tolerant comparison). The MD family inherits the established D
   behavior verbatim. No defect introduced.
2. **MD/bare-D dedup correctness.** Fixture extractor probe confirms trailing-D
   portions of MD tokens (`D01`,`D02`) are stripped from the bare-D family while
   genuine standalone bare-D tokens (`D03`,`D04`,`D05`) are preserved — family
   boundary intact.

---

## Self-Audit

**(a) Reliance list — structural/task-integrity dimension (already adversarially
verified via PG.2 + per-phase gates 2/4/5 PASS, per spawn prompt):**
- Relied on the prior structural verdict for: section/item structure, frontmatter,
  template conformance, evidence-citation presence. I did NOT re-run those.

**(b) Independent semantic/operational checks (≥1 required, INV-019):**
- **End-to-end MD round-trip** — verified by live `uv run python` probe exercising
  `build_id_registry`→`to_dict`→reconstruct→`union_of_known`/`extract_roadmap_ids`
  containment (not a unit-test re-read; my own constructed spec+roadmap inputs).
- **R4 shell across 4 input classes** — verified by actually executing
  `repo-inventory.sh` against constructed temp repos (happy/empty/all-excluded/
  malformed-ERE) and inspecting exit codes + stderr, exposing behavior unit tests
  may stub.
- **R2 ordering** — verified by reading executor.py call-site sequence (3522→3532→
  3538) and the helper body, reasoning about clobber-safety, not relying on a test
  assertion.
- **Consumer enumeration** — `grep -rn "SpecIdRegistry("` across src+tests to prove
  exactly 5 construction sites and no 6th, with keyword-arg safety analysis.
- **arch_lint over-suppression** — read AST-walk logic + ran `make lint-architecture`
  Check 11 to confirm `id(node)` identity-scoping does not over-suppress.

These required my own tool engagement beyond what the structural gate verified;
the structural gate confirms the task file is well-formed, but only execution +
source-reading confirms the changes work in the real pipeline.

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 7 | Grep: 4 | Glob: 0 | Bash: 9 (incl. 5 live probes)
**Tavily/web research:** none required (all verification is local-file + execution bound).

---

## VERDICT: PASS

No unfixable issues. The single MINOR log-completeness nit was fixed in-place,
synced-verified, and re-tested. All 5 task-targeted operational dimensions
(R1 MD round-trip, R2 reset ordering, R4 shell robustness, arch_lint scoping,
frozen-dataclass consumer safety) work correctly in the real roadmap pipeline
beyond passing unit tests.
