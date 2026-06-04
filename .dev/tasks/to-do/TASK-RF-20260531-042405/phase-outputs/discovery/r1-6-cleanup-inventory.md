# R1.6 Cleanup Inventory — Consolidated Cleanup-Target Verification

**Task:** TASK-RF-20260531-042405 — Roadmap Pipeline Brittleness-Elimination (R0 + R1)
**Phase / Step:** Phase 11 (R1.6 — Cleanup) / Step 11.1 (Discover full cleanup inventory)
**Date:** 2026-06-02
**Method:** Cleanup-target list extracted from `research/01-file-inventory.md` (§A, §B, §F) and `research/02-patterns-conventions.md` (§3, §8). Each target re-verified against the **current** source tree via `grep -n` (line numbers drifted during R1.1–R1.5; current lines recorded below). Classifications are sourced from the research files — no fabricated classifications. The `Action` column is justified by Contract / §MVR citation.

> **Verification scope note:** All paths are relative to repo root `/config/workspace/IronClaude-RoadmapRewrite/`. Research files cite original-state line numbers; this inventory records **current** line numbers as verified on 2026-06-02 (post-R1.5). Where a target was already remediated during R1.1–R1.5, it is flagged **ALREADY-REMEDIATED → VERIFY-ONLY** so Step 11.4 confirms rather than re-deletes.

---

## (a) Frontmatter Parser Duplicates (Contract #6)

**Source:** research/01 §A.2 + §B + §E; research/02 §2.4, §2.5, §7 anti-pattern #4.
**Verification:** all 6 variants confirmed present 2026-06-02 (`grep -n "def _parse_frontmatter|def _check_frontmatter|def parse_frontmatter|def _extract_frontmatter|def _extract_frontmatter_values" src/superclaude/cli/`).
**Canonical decision (Step 11.2 remediation, sc:reflect C1 fix):** the canonical parser is the **PipelineEnvelope post-step extractor** (`cli/roadmap/envelope.py`), NOT a re-export from `_check_frontmatter`. Canonicalizing on `_check_frontmatter` would preserve Flaw 3 (state-in-markdown substrate) — the exact substrate §MVR §1 inverts. Task objective 10 ("canonicalize on `_check_frontmatter`") is SUPERSEDED by §MVR §1. **`PipelineEnvelope` currently has no `frontmatter` field** (verified: `grep .frontmatter envelope.py` = 0) — Step 11.2(a) adds it first.

| File | Line (current) | Line (research) | Variant signature | Action |
|---|---|---|---|---|
| `cli/roadmap/gates.py` | 178 | 168 | `_parse_frontmatter(content) -> dict[str, str] \| None` — requires `---` at file start; used by 26 semantic checks | **DELETE** (§MVR §1 — neither rescued nor canonicalized; consumers migrate to `envelope.frontmatter`) |
| `cli/pipeline/gates.py` | 125 | 91 | `_check_frontmatter(content, required_fields, output_file) -> tuple[bool, str \| None]` — regex `finditer`, gate-style return; single caller `gate_passed` STANDARD/STRICT | **DELETE** (§MVR §1 — explicitly NOT canonicalized; gate path reads `envelope.frontmatter`) |
| `cli/roadmap/spec_parser.py` | 114 | 109 | `parse_frontmatter(text, warnings) -> dict[str, Any]` — third variant | **DELETE** variant; pre-pipeline spec inspection imports from `envelope` module |
| `cli/roadmap/spec_patch.py` | 285 | 285 | `_extract_frontmatter(text) -> str \| None` — fourth variant | **DELETE** variant; migrate consumer to `envelope.frontmatter` |
| `cli/cli_portify/utils.py` | 11 | 11 | `parse_frontmatter(content) -> tuple[dict[str, Any], str]` — **outside roadmap pipeline** | **MIGRATE-consumers** — Step 11.2(c) lists DELETE, but this is in `cli_portify` (separate tool); if its consumers are pipeline-external they import from `envelope` module per Step 11.2(e). Flag in parser-consistency lint (Step 11.5 / Phase 13). |
| `cli/audit/wiring_gate.py` | 931 | 931 | `_extract_frontmatter_values(content) -> dict[str, str]` — **outside roadmap pipeline** | **MIGRATE-consumers** — same caveat as `cli_portify`; enumerated by `test_parser_consistency.py` |

**Net:** 2 in-pipeline DELETEs (`roadmap/gates.py:178`, `pipeline/gates.py:125`), 2 in-pipeline variant DELETEs (`spec_parser.py:114`, `spec_patch.py:285`), 2 cross-cutting MIGRATE flags (`cli_portify`, `audit`). New typed `frontmatter: dict` field on `PipelineEnvelope` is the migration target (Step 11.2(a)).

---

## (b) `return True` Fragility Stubs (Contract #5)

**Source:** research/01 §A.2 (`_cross_refs_resolve`), §A.4 (obligation_scanner, fidelity_checker), §A.6 (remediate_executor), §A.4/§A.7 (fingerprint, spec_parser); research/02 §2.3, §7 anti-pattern #3.
**Verification:** `grep -n "return True"` per file, 2026-06-02. Line numbers drifted substantially (R0.2 added `_is_allowlisted`; R1.x edits shifted counts).
**Key distinction (Acceptance Gate #7 + Step 11.5 lint):** the Contract #5 target is NOT "all `return True`" — it is `return True` carrying a **fragility comment** (regex `return True\s*(?:#|""")\s*.*(?:fragile|too\s+hard|for\s+now)`) OR a public-contract function structurally incapable of returning `False`. Early-exit heuristics that legitimately return `True` are **VALID-HEURISTIC → KEEP**.

### (b.1) The canonical Contract #5 stub — DELETE / FAIL-CLOSED

| File | Line (current) | Line (research) | Context | Classification | Action |
|---|---|---|---|---|---|
| `cli/roadmap/gates.py` | 58–101 (`return True` at L99 + L101) | 48–91 | `_cross_refs_resolve(content) -> bool` — returns `True` in BOTH the unresolved branch (L99, after `warnings.warn`) AND the all-resolved branch (L101); structurally incapable of `False`. L98 comment: "Warning-only mode (OQ-001): return True to avoid blocking pipeline". Registered in `MERGE_GATE` via `SemanticCheck(name="cross_refs_resolve", check_fn=_cross_refs_resolve, …)` at **L1289–1290**. | **FRAGILITY** (canonical Contract #5 stub) | **DELETE** the function AND remove the `MERGE_GATE` `SemanticCheck` registration at L1289–1290; OR replace with a fail-closed version returning `False` on unresolved refs (research/02 §2.3). Step 11.3 executes. |

### (b.2) Early-exit heuristics — KEEP (classified VALID-HEURISTIC by research/01 §A.4/§A.6)

| File | Line(s) current | Line(s) research | Enclosing function | Classification | Action |
|---|---|---|---|---|---|
| `cli/roadmap/obligation_scanner.py` | 808 | — | `_is_allowlisted` (R0.2 allowlist hit → demote) | VALID-HEURISTIC | **KEEP** |
| `cli/roadmap/obligation_scanner.py` | 818, 821, 824, 828, 832, 836, 840 | 719/722/725/729/733/737/741 | `_is_meta_context` (Layer-2 meta-context detectors) | VALID-HEURISTIC (early-exit short-circuits, not gate stubs — research/01 §A.4) | **KEEP** |
| `cli/roadmap/obligation_scanner.py` | 859, 862 | 760 | `_has_discharge` (discharge-intent found) | VALID-HEURISTIC | **KEEP** |
| `cli/roadmap/obligation_scanner.py` | 879 | — | `_is_inside_code_block` (position inside fenced block) | VALID-HEURISTIC | **KEEP** |
| `cli/roadmap/remediate_executor.py` | 326, 345, 362 | 326/345/362 | `check_patch_diff_size` ("all checks passed → True") | VALID-HEURISTIC / EARLY-EXIT | **KEEP** (confirm per-site in 11.3) |
| `cli/roadmap/remediate_executor.py` | 381, 385, 397, 412, 423 | 397/412/423 | `_check_diff_size` (L381 "Cannot check; allow to proceed", L385 "Empty original; allow any change", rest = bounded diff-size checks) | VALID-HEURISTIC / EARLY-EXIT | **KEEP** (L381/L385 carry explicit allow-comments — confirm not fragility in 11.3) |
| `cli/roadmap/remediate_executor.py` | 706 | 706 | `fallback_apply` / `check_morphllm_available` region | VALID-HEURISTIC | **KEEP** |
| `cli/roadmap/fingerprint.py` | 99, 102 | 97/100 | `_is_code_like` (code-like text heuristic) | VALID-HEURISTIC | **KEEP** |
| `cli/roadmap/fingerprint.py` | 217 | — | `fingerprint_gate_passed` (L217 `return True  # passthrough`) | VALID-HEURISTIC / passthrough | **KEEP** (confirm passthrough is intentional, not fragility, in 11.3) |
| `cli/roadmap/spec_parser.py` | 497 | 468 | `_looks_like_file_path` (file-path heuristic early-exit) | VALID-HEURISTIC | **KEEP** |

**Net:** exactly **1 FRAGILITY stub** (`_cross_refs_resolve`) to DELETE/fail-close; all other `return True` sites are VALID-HEURISTIC early-exits that must NOT be blindly deleted (Step 11.3 confirms per-site). Acceptance Gate #7 (`grep -rn "return True\s*#.*fragile|too.*hard|for.*now" src/superclaude/cli/`) targets only fragility-commented returns — verify zero after `_cross_refs_resolve` removal.

---

## (c) Fail-Open Defaults in `fidelity_checker.py` (Contract #4 / §MVR §4)

**Source:** research/01 §A.4 (L287-303); research/02 §3.1 (L287-303 `found=True, # fail-open` + L314-337 partial-match fail-open).
**Verification:** `grep -n "found=True|fail-open"` 2026-06-02 returned NO `found=True` and NO `# fail-open` in `fidelity_checker.py`. Read of L284–354 confirms **both fail-open branches have ALREADY been converted to fail-closed** (during R1.5 / Phase 10 per the docstring at L20-22 "marks the FR as NOT found (ambiguous=True), and surfaces a gap … kills the master:§Flaw 1 fail-open evidence chain").

| File | Line (research) | Current state (verified) | Classification | Action |
|---|---|---|---|---|
| `cli/roadmap/fidelity_checker.py` | 287–303 (no-extractable-names branch) | **L294–311**: `found=False,  # fail-closed: unverifiable != implemented` + `ambiguous=True`; logger says "marking as NOT found (fail-closed per §MVR §4)" | **ALREADY-REMEDIATED** | **VERIFY-ONLY** — Step 11.4 confirms fail-closed; do NOT re-edit |
| `cli/roadmap/fidelity_checker.py` | 314–337 (partial-match branch) | **L322–346**: `found = not missing` (PASS requires ALL expected names); `ambiguous=bool(missing)`; logger says "marking as NOT found (fail-closed per §MVR §4)" | **ALREADY-REMEDIATED** | **VERIFY-ONLY** — Step 11.4 confirms; do NOT restore fail-open |

**Net:** Step 11.4's `fidelity_checker.py` fail-open deletion is **already complete** (done in R1.5). Step 11.4 reduces to a **verification** that no `found=True` fail-open path remains + the `gate=None` bypass deletion below. Record in Phase 11 findings so the gate QA does not flag "missing deletion."

---

## (d) `gate=None` Convergence Bypass in `executor.py` (Contract #4)

**Source:** research/01 §A.1 + §F (L2167); research/02 §1.2 (L2167), §6.2 (convergence-default contract).
**Verification:** `grep -n "gate=None if config.convergence_enabled"` 2026-06-02 → **`executor.py:2665`** (drifted from research L2167 / task-cited L2579). Exactly 1 occurrence (the surgical `gate=None` target). `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` does NOT yet exist in `gates.py` (verified `grep CONVERGENCE_AWARE` = 0) — its creation is in-scope for Step 11.4.

| File | Line (current) | Line (research/task) | Construct | Action |
|---|---|---|---|---|
| `cli/roadmap/executor.py` | 2665 | 2167 (research) / 2579 (task) | `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` — convergence is default-on (`commands.py:188` `--no-convergence default=False`), so spec-fidelity runs ungated on virtually every production run | **DELETE** ternary; replace with `gate=SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` (NEW gate constant in `gates.py`, wraps convergence registry as a `CodeAssertion` per research/02 §6.2) — preserves Flaw 4 fix per Contract #4. `convergence.py` itself is PRESERVE (only gate wiring changes). |

> **Scoped-grep note for Step 11.7 validation:** grep for the SPECIFIC pattern `gate=None if config.convergence_enabled` (must be 0 post-fix), NOT bare `gate=None` — there is a legitimate `gate=None` at `sprint/executor.py:85`.

---

## (e) `remediate_parser.py` — Evaluate for Tool-Write Collapse

**Source:** research/01 §A.6 ("tool-write rewrite collapses this parser entirely … Major delta").
**Verification:** file present, **391 LOC**, mtime 2026-05-31 (unchanged since pre-R1.4). R1.4 (Phase 9) scope per task objective 8 was the **9 LLM generator/merge/fidelity/wiring steps**; the remediate step is non-LLM-deterministic + per-file agent invocations, and `remediate_parser.py` appears NOT to have been collapsed by the R1.4 cutover (file unchanged).

| File | LOC | R1.4 cutover state | Action |
|---|---|---|---|
| `cli/roadmap/remediate_parser.py` | 391 | NOT collapsed (file unchanged since 2026-05-31; remediation step not part of the 9-step R1.4 tool-write set) | **DEFER** — delete IF/when R1.4 tool-write cutover for the remediation step is complete; else retain. Per Step 11.1 instruction (e): "mark for evaluation (delete IF R1.4 cutover for remediation step is complete, else defer)." Record as a Follow-Up Item, do NOT delete in R1.6. |

---

## (f) CI-vs-Runtime `code_assertion` Split (CORRECTED R1.6 Deliverable)

**Source:** `.dev/reflect/r1-3-uc2-validation/` + Task Log Follow-Up L1046; task Step 11.4 corrected-deliverable clause.
**Verification:** `grep -n` against `code_assertions.py` + `cli/pipeline/gates.py` 2026-06-02. This is the **High-priority R1.6 deliverable absent from every other Phase 11 step** — it lives in Step 11.4.

**The split (verified predicate classification):**

| Predicate | File:Line | Substrate | Classification | Runtime behavior |
|---|---|---|---|---|
| `assert_step_reachable(envelope, repo_root)` | `code_assertions.py:27` | Source-tree AST walk: resolves `repo_root/src/superclaude/cli/roadmap/executor.py` and walks `_build_steps` (L76-91). `del envelope` — envelope NOT consulted. | **CI-ONLY** | On a pipx-installed package there is no `src/` tree → must be skipped at production runtime |
| `assert_envelope_artifacts_present(envelope, repo_root)` | `code_assertions.py:126` | Operates on `envelope.artifacts` (the §MVR §1 artifact graph), resolving recorded artifact paths against `repo_root` (L159-173). | **RUNTIME** | Fires in the live gate path; envelope is the SoT |

**The envelope-None shim (PRESERVE, do NOT delete):**

| File:Line | Current code/comment | Action |
|---|---|---|
| `cli/pipeline/gates.py:93–100` | `if criteria.code_assertions:` → `if envelope is None or repo_root is None:` skip-path; then dispatches `assertion.check_fn(envelope, repo_root)` | **PRESERVE** — this is the CORRECT skip-path for CI-only/source-tree assertions on a pipx-installed package with no `src/` tree (per `.dev/reflect/r1-3-uc2-validation/`). Do NOT blanket-delete. |
| `cli/pipeline/gates.py:37–39` (comment) | "…they are silently skipped -- ... R1.6 cleanup deletes this skip-path once all [call sites migrated]" | **REWRITE** — the envelope-None branch is PRESERVED as correct behavior for CI-only/source-tree `code_assertions`, NOT deleted. |
| `cli/pipeline/gates.py:96–97` (comment) | "envelope/repo_root see code_assertions as if undefined. // R1.6 deletes this branch when all call sites are migrated." | **REWRITE** — state that the branch is PRESERVED (correct skip-path), not deleted. |

**Action (Step 11.4):** classify each `code_assertion` predicate CI-only vs runtime; fire ONLY runtime-safe assertions in the live gate path; PRESERVE the `gates.py:93-100` shim; REWRITE the now-wrong-framing comments at L37-39 and L96-97. The R1.5 `verify-implementation` FR→artifact checks (already shipped) are RUNTIME predicates and belong in the live path with envelope plumbed.

---

## (g) `spec_id_registry.json` Dual-Write Deletion TODO

**Source:** task Step 11.1 instruction (g) — `envelope.py:148-150`.
**Verification:** `grep -n "spec_id_registry|dual-write|TODO" envelope.py` 2026-06-02. The dual-write TODO is documented at **L146–151** (class docstring "R0.1 `spec_id_registry.json` absorption … both `<release>/spec_id_registry.json` and `<release>/envelope.json` … sidecar is deleted in R1.6 — see the TODO at the field site") and **L166** ("R1.6 — delete `<release>/spec_id_registry.json` writes once [envelope canonical]").

| File | Line | Construct | Action |
|---|---|---|---|
| `cli/roadmap/envelope.py` | 146–151, 166 | Dual-write of `spec_id_registry.json` (R0.1 sidecar) alongside `envelope.json`; TODO marks R1.6 deletion of the sidecar writes once the envelope is the canonical `spec_ids` SoT | **DEFER-pending-cutover** — R1.2 established envelope dual-write "for one release cycle" before markdown/sidecar becomes render-only. If the 1-release dual-write window has NOT elapsed (envelope not yet sole SoT in production), deleting the sidecar write now is premature and breaks the absorbed R0.1 SemanticCheck that still reads `spec_id_registry.json` (envelope.py:28). **Record as Follow-Up / Open Question**; do NOT delete the sidecar write in this R1.6 pass unless the cutover-window confirmation is explicit. |

---

## Summary — R1.6 Cleanup Action Map

| Target group | DELETE/fail-close NOW | VERIFY-ONLY (already done) | PRESERVE / REWRITE | DEFER (Follow-Up) |
|---|---|---|---|---|
| (a) Frontmatter parsers | `roadmap/gates.py:178`, `pipeline/gates.py:125`, `spec_parser.py:114`, `spec_patch.py:285` (+ add `envelope.frontmatter` field) | — | — | `cli_portify/utils.py:11`, `audit/wiring_gate.py:931` (MIGRATE flag; cross-cutting) |
| (b) return-True stubs | `gates.py:_cross_refs_resolve` L58-101 + MERGE_GATE reg L1289-1290 | — | 10 VALID-HEURISTIC sites KEEP | — |
| (c) fidelity_checker fail-open | — | L294-311 + L322-346 (already fail-closed in R1.5) | — | — |
| (d) gate=None bypass | `executor.py:2665` (+ create `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE`) | — | — | — |
| (e) remediate_parser.py | — | — | — | DEFER pending R1.4 remediation cutover |
| (f) code_assertion split | — | — | PRESERVE `pipeline/gates.py:93-100` shim; REWRITE comments L37-39, L96-97; classify predicates | — |
| (g) spec_id_registry.json | — | — | — | DEFER pending dual-write cutover-window confirmation |

**Headline:** the R1.6 cleanup is **smaller than the task text implies** — the fidelity_checker fail-open (c) is already done (R1.5), the code_assertion shim (f) is PRESERVE-not-delete, and (e)+(g) are DEFER. The genuine deletions are: 4 frontmatter parsers + `_cross_refs_resolve` + the `gate=None` ternary. All cleanup targets verified present (or already-remediated) in the current source as of 2026-06-02.

---

## Status

Complete.
