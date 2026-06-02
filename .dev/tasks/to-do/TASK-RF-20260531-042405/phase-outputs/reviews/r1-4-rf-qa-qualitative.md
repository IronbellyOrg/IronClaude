# QA Report — release-validation (PG9.1)

**Topic:** R1.4 tool-write migration (Phase 9, TASK-RF-20260531-042405)
**Date:** 2026-06-02
**Phase:** release-validation (qualitative)
**Fix cycle:** 1
**Document type:** Executed Task Phase (R1.4 tool-write migrations)
**Baseline for PRESERVE diff:** 90a8fa67 | **HEAD at review:** 44f78a01 (R1.4 committed; prompt said c542b6bf — work has since been committed on top)

---

## Overall Verdict: PASS

All 8 acceptance criteria (a)-(h) PASS with file:line evidence (below). 4 adversarial deep-checks
PASS. Two MINOR findings (F1 schema/gate semantic-narrowing on `extraction_mode`; F2 missing
reflect-hook-bypass regression test) were found and **FIXED in-place** under fix_authorization,
then re-verified: targeted suite 305/305, full roadmap suite 1950 passed / 12 skipped, ruff +
arch-lint clean. No CRITICAL or IMPORTANT issues. Markdown remains the production default; no
premature cutover; PRESERVE invariants byte-unchanged. Fix cycle 1 resolved all findings — no
escalation needed (HALT-precedence not triggered).

---

## Per-Criterion Findings

### (c) Contract #3 (generate + merge phantom-ID rejection at generation time) — PASS

- executor.py:1266 routes BOTH `generate` and `merge` (`_tw_key in ("generate","merge")`) through `render_step_tool_write_with_id_check`. Confirmed read of executor.py:1234-1307.
- tool_writer.py:455-496 `render_step_tool_write_with_id_check`: phantom id → `validate_id_subset` returns errors → returns BEFORE `_persist_and_render` (line 495) → neither `.md` nor `.json` written. Generation-time rejection confirmed.
- `test_generate_rejects_phantom_id` (test_tool_write_step_generate.py:312-361) genuinely asserts `not out.exists()` AND `not roadmap.json exists()` on phantom, AND clean path writes .md + sidecar matching fixture. NOT exit-code-only.
- `test_merge_rejects_phantom_id` (test_tool_write_step_merge.py:371+) mirrors: asserts `not out.exists()` + `not merged.json exists()` on phantom.
- Empty-`spec_ids` skip (executor.py:1277-1286 + tool_writer.py:487) is intentional/documented (extract-not-in-tool-write-mode → identity); covered by `test_id_check_skips_when_spec_ids_empty`. ADVERSARIAL NOTE: phantom rejection is only LIVE when extract is also in tool-write mode (sidecar `extraction.json` exists). By-design dual-write semantics, not a defect — markdown-default path unaffected; subset check is vacuous without a spec-id universe.

### (f) PRESERVE invariants unchanged — PASS

- `git diff --stat 90a8fa67 -- convergence.py semantic_layer.py structural_checkers.py` = EMPTY (byte-unchanged).
- commands.py diff vs 90a8fa67: PURELY ADDITIVE. Zero removed/reordered lines (`grep '^-'` on the diff returns nothing). Only `@click.option("--tool-write-*", ..., default=False)` additions.

### (g) Zero new `return True` fragility stubs from R1.4 — PASS

- Single new `+ return True` in changed roadmap tree: `code_assertions.py:227`. Read context (195-228): legitimate logic — returns True when an AST walk finds a real production call site of `build_certify_step` (reachability assertion for the §Flaw-1 condition), `return False` otherwise. NOT a fragility stub.

### (b) Parity tests compare rendered output to markdown path (not exit-code/field-presence only) — PASS

- score `test_render_parity` (test_tool_write_step_score.py:147-163): asserts rendered template contains all 5 body sections + every scoring criterion + frontmatter keys + ≥20 newlines. Content-level.
- score `test_rendered_score_satisfies_gate_frontmatter` (166-185): reads the REAL `SCORE_GATE.required_frontmatter_fields` + `SCORE_GATE.min_lines` from gates.py and asserts the rendered output satisfies them. Genuine gate-satisfaction proof.
- score `test_render_step_tool_write_dual_write_proof` (208-220): asserts BOTH .md + .json sidecar written on PASS and sidecar == fixture.
- score `test_build_score_prompt_default_byte_identical` (258-277): asserts `build_score_prompt(default) == build_score_prompt(tool_write=False)` AND TDD/PRD conditional blocks intact.
- debate `test_rendered_debate_satisfies_gate_frontmatter` (170) + `test_rendered_debate_passes_convergence_semantic_check` (192): the latter invokes the ACTUAL `DEBATE_GATE.semantic_checks[0].check_fn` (`_convergence_score_valid`) on the rendered output — strongest possible gate-satisfaction proof.
- Gate-satisfaction tests present in 11/12 test files; byte-identical-default tests in 7/12. The remaining files (extract/extract_tdd/debate/diff/generate) prove default-path preservation via `<output_format> present in default, absent in tool_write` assertions (extract.py:201-209 etc.) — equivalent guarantee given the additive-branch structure verified in (h).

### (d) Contract #8 (registry-sourced thresholds, no hardcoded 0.7/0.5) — PASS

- `score.schema.json`: ZERO decimal literals anywhere (raw `grep '[0-9]\.[0-9]'` empty); `$comment:5` explicitly references `superclaude.contracts.CONVERGENCE_THRESHOLDS`.
- `spec_fidelity.schema.json`: only decimal is the prose step-number "9.9" in `$comment`; NO threshold literals; `$comment` states "No convergence threshold literal is embedded (Contract #8)".
- Guard tests: `test_score_schema_no_hardcoded_thresholds` (test_tool_write_step_score.py:283) scans the substrate for "0.7"/"0.5" and fails if present; `test_score_thresholds_registry_sourced` (304) asserts `roadmap_convergence_thresholds() is CONVERGENCE_THRESHOLDS["sc:roadmap"]` (identity, proving SoT-read not copy). Both PASS in suite run.
- `build_score_prompt` docstring + `score_tool_definition` (prompts.py) reiterate no embedded literal; verified the function body returns no 0.7/0.5.

### (h) Markdown path remains production default; flag=False byte-identical — PASS

- All `--tool-write-*` flags `default=False` (commands.py additive diff).
- `build_score_prompt` diff vs 90a8fa67: default branch returns the UNCHANGED `base + _OUTPUT_FORMAT_BLOCK`; tool_write branch is purely additive (`return base + _SCORE_TOOL_WRITE_OUTPUT_BLOCK`); new kwarg defaults False. So flag=False ⇒ byte-identical to pre-migration expression. Same additive pattern across builders (prompts.py diff: every tool-write block is a NEW `_*_TOOL_WRITE_OUTPUT_BLOCK` appended only under `if tool_write:`).
- 303/303 tests pass with all flags default; no behavioral change to existing runs.

### ADVERSARIAL DEEP CHECK — schema over-constraint (3 schemas: extract_tdd, merge, debate)

- **merge.schema.json**: appropriately PERMISSIVE — frontmatter `additionalProperties: true`, `oneOf [spec_source | spec_sources]` (1 vs multi-spec), `dependency_graph` accepts string-OR-array, milestone `deliverables` items require only `id`+`title` (9-column fields optional), `open_questions`/`risk_register` items `additionalProperties: true`. No over-constraint. PASS.
- **debate.schema.json**: required frontmatter `[convergence_score, rounds_completed]` exactly mirrors `DEBATE_GATE.required_frontmatter_fields`; `convergence_score` ∈ [0,1] mirrors `_convergence_score_valid`. Optional provenance fields available. No over-constraint. PASS.
- **extract_tdd.schema.json**: 19 required frontmatter fields are all deterministic counts/metadata mirroring `EXTRACT_TDD_GATE`; FR/NFR items require only `id`. `complexity_class` enum LOW/MEDIUM/HIGH matches `_complexity_class_valid`.
  - **MINOR finding F1 (semantic narrowing, not a live defect):** `extraction_mode` schema enum is exactly `["standard","chunked"]`, but the markdown-path gate `_extraction_mode_valid` (gates.py:682-697) accepts ANY value `.startswith("chunked")` — e.g. `"chunked (3 chunks)"`. A markdown roadmap using `"chunked (3 chunks)"` would FAIL schema validation in tool-write mode (neither .md nor .json written), diverging the two paths. NOT currently live: the tool-write prompts (prompts.py:123,162,607,796) instruct the LLM to emit `standard|chunked` exactly, and no code emits the parenthetical form. Flagged because dual-write paths should be interchangeable; the schema is stricter than the gate it backs.

### (a) 11 genuine LLM migrations each have schema + template + flag (default False) + parity test — PASS

- 11 schemas present (`tool_schemas/*.schema.json`), 11 templates (`*.md.j2`), 12 test files (11 genuine + remediation parity).
- `TOOL_WRITE_REGISTRY` = exactly 11 keys: certify, debate, diff, extract, extract_tdd, generate, merge, reflect, score, spec-fidelity, test-strategy. `remediate` correctly ABSENT; `wiring_verification` correctly ABSENT.
- All 11 genuine config flags default False: 10 on `RoadmapConfig` + `tool_write_validate_reflect` on `ValidateConfig` (models.py:155). (Plus `tool_write_remediate=False` for the parity-only remediate.)
- **wiring_verification EXEMPT** honored: deterministic static analysis, no LLM/markdown path — NOT flagged for absent schema/template (per Step 9.10 + rationale file).
- **remediate PARITY-ONLY** honored: file-edit prompt, no roadmap_ids, Contract #3 N/A — NOT flagged for absent schema/template/render. Has `build_remediation_prompt(tool_write=False)` param + flag + byte-identity test only.

### (e) No premature cutover — PASS

- `.dev/migrations/r1-4-cutover-counters.yaml`: 13 entries, EVERY one `release_marker_count: 0` + `cutover_eligible: false` (grep for nonzero/true returns nothing).
- `r1-4-cutover-decision.md:76` verdict: **"NOT READY FOR CUTOVER — markdown remains the production default."** Vector A (≥3 consecutive parity-passing release cycles) enforced; premature cutover HALT-blocked. No step claims cutover < 3 cycles.

### ADVERSARIAL DEEP CHECK — reflect render hook does not break multi-agent / existing validate flow — PASS

- Render hook in `validate_run_step` (validate_executor.py:183-210): `_tw_spec = TOOL_WRITE_REGISTRY.get(step.id)` then guard `_tw_spec is not None AND getattr(config, config_flag, False)`.
- Multi-agent path builds steps `id=f"reflect-{agent.id}"` (validate_executor.py:346) and `id="adversarial-merge"` (365) — NEITHER is a registry key, so `get()` returns None → hook SKIPPED → existing markdown flow preserved. Multi-agent reflect ALSO never passes `tool_write=` (line 347, defaults False).
- Single-agent path `id="reflect"` (297) DOES pass `tool_write=getattr(config,"tool_write_validate_reflect",False)` (305). With flag False (default), hook condition's flag check fails → skipped → markdown path. Only flag=True engages tool-write. Behavior correct.
- **MINOR finding F2 (test-coverage gap, not a defect):** there was no explicit regression test asserting that the multi-agent `reflect-{agent}` step id is bypassed by `TOOL_WRITE_REGISTRY.get()` (the bypass is correct-by-construction since the key is absent, but a guard test hardens against a future registry that adds a `reflect-`-prefixed key or a key-normalization change like the `generate-*` → `generate` mapping in roadmap_run_step). **FIXED — see Actions Taken.**

---

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|-------------|--------|
| F1 | MINOR | `extract.schema.json:46`, `extract_tdd.schema.json:58` | `extraction_mode` schema `enum:["standard","chunked"]` narrower than the markdown gate `_extraction_mode_valid` (accepts any `chunked*`, e.g. `"chunked (3 chunks)"`) → dual-write paths not interchangeable for that field | Relax enum to `pattern:"^(standard|chunked.*)$"` to mirror the gate | FIXED in-place |
| F2 | MINOR | `test_tool_write_step_validate_reflect.py` | No regression test proving multi-agent `reflect-{agent}` / `adversarial-merge` step ids bypass the tool-write hook (registry `get()` → None) | Add explicit guard test | FIXED in-place |

No CRITICAL or IMPORTANT issues found. Both findings were MINOR and have been remediated.

---

## Actions Taken (fix_authorization: true)

1. **F1 fix** — `src/superclaude/cli/roadmap/templates/tool_schemas/extract.schema.json` and `extract_tdd.schema.json`: replaced `extraction_mode` `enum:["standard","chunked"]` with `pattern:"^(standard|chunked.*)$"` + a `$comment` documenting gate-interchangeability. The tool-write prompts still instruct the canonical `standard|chunked` forms; the relaxation only makes the schema accept the SAME set the markdown gate accepts, restoring dual-write interchangeability without weakening the LLM contract.
   - **Verified:** added regression `test_extraction_mode_matches_gate_tolerance` (test_tool_write_step_extract_tdd.py) that asserts the schema accepts `standard`/`chunked`/`chunked (3 chunks)` (each cross-checked against the REAL `_extraction_mode_valid` gate fn) AND still rejects `full`. Passes. JSON re-validated as well-formed.
2. **F2 fix** — `tests/roadmap/test_tool_write_step_validate_reflect.py`: added `test_multi_agent_reflect_step_ids_bypass_tool_write_hook` asserting `TOOL_WRITE_REGISTRY.get("reflect-opus-architect"|"reflect-sonnet-analyzer"|"adversarial-merge") is None` and `get("reflect") is not None`. Passes.
3. **Re-verification after fixes:** tool-write+prompts+executor+convergence+dispatch suite **305/305 PASS** (was 303; +2 regression tests). Full `tests/roadmap/` **1950 passed, 12 skipped, 0 failed**. `ruff` clean on all changed files; `make lint-architecture` 0 errors. Only `src/superclaude/` + `tests/` touched — no `.claude/` mirror edits.

---

## Exact Test Counts

- Targeted suite (`test_tool_write_step_*.py` + prompts + executor + convergence + dispatch_reachability): **305 passed** (post-fix; 303 pre-fix).
- Full `tests/roadmap/`: **1950 passed, 12 skipped**.
- `make lint-architecture`: **0 errors, 5 warnings** (PASS).
- `uv run ruff check src/superclaude/cli/roadmap/` + changed test files: **All checks passed**.

---

## Self-Audit

**(a) Reliance list — items where I relied on prior statements only for navigation, then independently verified:**
- Aggregation report's migration table (used as an index only) → independently re-verified every schema/template/test/flag against disk and `TOOL_WRITE_REGISTRY` introspection.
- Aggregation's "303/303" / registry / Contract claims → re-ran the suite myself (got 303, then 305 post-fix) and read the actual source.

**(b) Independent semantic checks (tool-evidenced):**
- Contract #3 no-write: READ tool_writer.py:455-496 + executor.py:1234-1307 + test bodies (test_generate/merge `assert not out.exists()`). Not exit-code reliance.
- Contract #8: `grep '[0-9]\.[0-9]'` on score.schema.json (empty) + read of guard tests asserting `is CONVERGENCE_THRESHOLDS["sc:roadmap"]` identity.
- Over-constraint: READ merge/debate/extract_tdd schemas field-by-field; cross-referenced `_extraction_mode_valid`/`DEBATE_GATE`/`EXTRACT_TDD_GATE` in gates.py — surfaced F1 that structural QA (section/field presence) would NOT catch.
- Reflect hook safety: READ validate_executor.py:183-210 + 317-378; reasoned the registry-`get()` bypass for `reflect-{agent}` — surfaced F2.
- PRESERVE: `git diff --stat 90a8fa67` (empty) + commands.py purely-additive grep.

**Tool engagement:** Read: 11 | Grep/Bash-grep: ~22 | Bash(test/lint/python): ~10 | Edit: 5. Tool calls ≥ criteria count (8 + deep checks). No N/A markings.

---

## Confidence Gate

- **Confidence:** Verified: 8/8 criteria + 4 adversarial deep-checks | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
- **Tool engagement:** Read: 11 | Grep: 22 | Glob: 0 | Bash: 10
- All criteria (a)-(h) VERIFIED with file:line + tool evidence. No criterion marked N/A; the wiring/remediate exemptions were verified as legitimately exempt (not skipped).

---

## Recommendations

- F1 and F2 are FIXED. No blocking work remains for PG9.1.
- Carry-forward (R1.6, non-blocking): the cutover flag-default flip + markdown deletion remain correctly deferred until `release_marker_count >= 3` per step (Vector A). The `.dev/migrations/r1-4-cutover-counters.yaml` is the SoT to drive that.
- The 4 files edited by this review (`extract.schema.json`, `extract_tdd.schema.json`, `test_tool_write_step_extract_tdd.py`, `test_tool_write_step_validate_reflect.py`) are git-uncommitted alongside the rest of R1.4 — fold into the next R1.4 commit checkpoint.

---

## VERDICT: PASS

## QA Complete
