# Research: Executor Data Flow

**Investigation type:** Code Tracer
**Scope:** src/superclaude/cli/roadmap/executor.py, src/superclaude/cli/roadmap/spec_structural_audit.py
**Status:** Complete
**Date:** 2026-03-25

---

## Pipeline Step Table

Verified from `_build_steps()` in `src/superclaude/cli/roadmap/executor.py:775-930`.

| Step Name | Input Files | spec_file received? | Pure Python or LLM subprocess? |
|---|---|---|---|
| `extract` | `config.spec_file` | Yes, direct | LLM subprocess |
| `generate-{agent_a.id}` | `extraction.md` | No | LLM subprocess |
| `generate-{agent_b.id}` | `extraction.md` | No | LLM subprocess |
| `diff` | `roadmap-a`, `roadmap-b` | No | LLM subprocess |
| `debate` | `diff-analysis`, `roadmap-a`, `roadmap-b` | No | LLM subprocess |
| `score` | `debate`, `roadmap-a`, `roadmap-b` | No | LLM subprocess |
| `merge` | `base-selection`, `roadmap-a`, `roadmap-b`, `debate` | No | LLM subprocess |
| `anti-instinct` | `config.spec_file`, `roadmap.md` | Yes, direct | Pure Python (`_run_anti_instinct_audit`) |
| `test-strategy` | `roadmap.md`, `extraction.md` | No | LLM subprocess |
| `spec-fidelity` | `config.spec_file`, `roadmap.md` | Yes, direct | LLM subprocess (or convergence engine) |
| `wiring-verification` | `roadmap.md`, `spec-fidelity.md` | No (filename string only in prompt) | Pure Python static analysis |

**Important nuance:** `wiring-verification` prompt builder receives `config.spec_file.name` (string), but `step.inputs` are `[merge_file, spec_fidelity_file]` — not spec_file content. Verified at executor.py:917-925.

---

## (a) `_build_*` Functions Passing `spec_file` as Direct Input to a Step

In `executor.py`, `_build_steps()` is the relevant builder. Direct spec_file wiring:

1. **`extract`** — executor.py:809-820
   - `prompt=build_extract_prompt(config.spec_file, ...)`
   - `inputs=[config.spec_file]`

2. **`anti-instinct`** — executor.py:885-894
   - `inputs=[config.spec_file, merge_file]`
   - Step uses `prompt=""` (non-LLM step; prompt unused)

3. **`spec-fidelity`** — executor.py:905-913
   - `prompt=build_spec_fidelity_prompt(config.spec_file, merge_file)`
   - `inputs=[config.spec_file, merge_file]`

Prompt-only provenance (not step inputs):
4. **`wiring-verification`** — executor.py:917-920
   - `build_wiring_verification_prompt(merge_file, config.spec_file.name)` — filename string only, not file content via inputs

---

## (b) Steps Receiving ONLY the Extraction Output

- `generate-{agent_a.id}` — executor.py:823-833 — `inputs=[extraction]`
- `generate-{agent_b.id}` — executor.py:834-843 — `inputs=[extraction]`

Steps that also use extraction but not extraction-only:
- `test-strategy` — executor.py:895-903 — `inputs=[merge_file, extraction]`

---

## (c) Full `_run_anti_instinct_audit` Call Sequence

Entry point: `_run_anti_instinct_audit(spec_file: Path, roadmap_file: Path, output_file: Path)` — executor.py:265-376

How invoked from `roadmap_run_step()` — executor.py:401-408:
1. Detect `step.id == "anti-instinct"`
2. Resolve `spec_file = config.spec_file`, `merge_file = config.output_dir / "roadmap.md"`
3. Call `_run_anti_instinct_audit(spec_file, merge_file, step.output_file)`

Internal sequence:
1. Import pure-Python modules (scan_obligations, extract_integration_contracts, check_roadmap_coverage, check_fingerprint_coverage) — lines 276-278
2. `spec_text = spec_file.read_text(...)` — line 280
3. `roadmap_text = roadmap_file.read_text(...)` — line 281
4. Module 1: `obligation_report = scan_obligations(roadmap_text)` — line 288 (roadmap only)
5. Module 2: `contracts = extract_integration_contracts(spec_text)` — line 291 (spec only)
6. `contract_result = check_roadmap_coverage(contracts, roadmap_text)` — line 292
7. Module 3: `fp_total, fp_found, fp_missing, fp_ratio = check_fingerprint_coverage(spec_text, roadmap_text)` — lines 295-297
8. Build YAML frontmatter — lines 299-313
9. Build markdown body — lines 315-365
10. Write `anti-instinct-audit.md` — lines 366-367

**Conclusion:** Anti-instinct is fully deterministic and programmatic. No LLM subprocess. No prompt builder.

---

## (d) What `_run_structural_audit` Does with spec_file

`_run_structural_audit(spec_file, extraction_file)` — executor.py:220-262:
1. `spec_text = spec_file.read_text(...)` — line 233
2. `extraction_text = extraction_file.read_text(...)` — line 234
3. `fm = _parse_frontmatter(extraction_text)` — lines 239-242
4. `total_req = int(fm.get("total_requirements", "0"))` — lines 244-247
5. `passed, audit = check_extraction_adequacy(spec_text, total_req)` — line 250
6. If failed: logs warning + prints to stdout — lines 251-261

This audit is **warning-only** — never blocks the pipeline.

Hook location — executor.py:515-520: called after extract subprocess completion.

`check_extraction_adequacy` signature (spec_structural_audit.py:95-118):
`check_extraction_adequacy(spec_text: str, extraction_total_requirements: int, threshold: float = 0.5) -> tuple[bool, SpecStructuralAudit]`

Returns:
- `(passed: bool, audit_result: SpecStructuralAudit)`

Logic: computes `ratio = total_req / audit.total_structural_indicators`; passes if `ratio >= threshold (0.5)`.

---

## (e) What `build_spec_fidelity_prompt()` Receives

Signature (prompts.py:312-382): `build_spec_fidelity_prompt(spec_file: Path, roadmap_path: Path) -> str`

- Builder receives `Path` objects, not file contents
- Prompt text: "Read the provided specification file and the generated roadmap."
- Spec content embedded via `step.inputs=[config.spec_file, merge_file]` → `_embed_inputs(step.inputs)` — executor.py:907-913, 441-456

**Conclusion:** spec-fidelity step receives actual spec content AND roadmap content, not just roadmap artifacts.

---

## (f) Steps Other Than Extract/Anti-Instinct/Spec-Fidelity That Receive spec_file

**No.** Only three steps receive spec_file directly as step input:
- `extract`
- `anti-instinct`
- `spec-fidelity`

Plus one structural-audit Python hook (warning-only).

`wiring-verification` does NOT receive spec_file as a file input — only `config.spec_file.name` (string) in the prompt builder.

---

## (g) What `_embed_inputs()` Does

Source: executor.py:69-82:
```python
content = Path(p).read_text(encoding="utf-8")
blocks.append(f"# {p}\n```\n{content}\n```")
return "\n\n".join(blocks)
```

**Format:** Fenced code blocks with `# <path>` header before each fence.

In `roadmap_run_step()`:
1. `embedded = _embed_inputs(step.inputs)` — executor.py:441-456
2. `composed = step.prompt + "\n\n" + embedded`
3. `effective_prompt = composed`

Executor comments explicitly state no `--file` local injection is used.

---

## (h) Is There a `build_anti_instinct_prompt()` LLM Step?

**No.** Verified evidence:
1. Import list in executor.py:42-52 does not include `build_anti_instinct_prompt`
2. Anti-instinct Step uses `prompt=""` (non-LLM step; prompt unused) — executor.py:885-894
3. Runtime dispatch intercepts anti-instinct before subprocess execution and calls `_run_anti_instinct_audit()` directly — executor.py:401-408

---

## Stale Documentation Found

1. `src/superclaude/cli/roadmap/prompts.py:6-8` — says executor appends `--file <path>`; stale; current executor uses `_embed_inputs()` inline
2. `executor.py:775-779` — says "Build the 9-step pipeline"; current `_build_steps()` defines 11+ concrete runtime steps
3. `executor.py:1656-1660` — says "After all 9 steps pass"; stale against current step list

---

## Gaps and Questions

1. The docstring says "9-step roadmap pipeline" but current `_build_steps()` defines 11+ executable entries (including 2 parallel generates + downstream remediate/certify in `_get_all_step_ids()`). Step count framing is inconsistent.
2. Does the wiring-verification runtime path (`run_wiring_analysis`) also read spec_file programmatically? The executor intercepts wiring-verification and calls `run_wiring_analysis(wiring_config, source_dir)` — the wiring_config contents need verification.

## Stale Documentation Found
- prompts.py module docstring says `--file <path>` is used by executor — FALSE; confirmed inline embedding is used.

## Summary

Direct spec_file flow is narrow and explicit. Three steps receive spec content directly:
- `extract` (LLM subprocess with spec embedded in prompt)
- `anti-instinct` (pure Python; spec read via `_run_anti_instinct_audit`)
- `spec-fidelity` (LLM subprocess with spec + roadmap embedded)

Plus one warning-only Python hook (`_run_structural_audit`).

All other steps (`generate-*`, `diff`, `debate`, `score`, `merge`, `test-strategy`, `wiring-verification`) do NOT receive spec_file directly. The generate steps receive ONLY extraction output — making extract the single chokepoint for TDD content coverage.

Validate pipeline (`validate_executor.py`) is entirely artifact-based (roadmap.md + test-strategy.md + extraction.md) and does not revisit raw spec/TDD input.
