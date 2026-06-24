# Research Completeness Verification — Analyst Report

**Analysis type:** completeness-verification
**Topic:** task-builder single track — PR #112 + #111 review remediation (R1–R5)
**Date:** 2026-06-02
**Research dir:** `/config/workspace/IronClaude-RoadmapRewrite/.dev/tasks/to-do/TASK-RF-20260602-060714/research/`
**Files analyzed (4):** `01-call-site-inventory.md`, `02-patterns-and-conventions.md`, `03-test-and-verification.md`, `04-template-and-examples.md`
**BUILD_REQUEST:** `.dev/reviews/PR-112-111-remediation-design.md`

Stance: adversarial. Each of the 9 spawn-prompt criteria is rated PASS (with cited evidence) or FAIL (with specific gaps). Read-only on research files; issues are reported for the appropriate agent to fix.

---

## Status / Completeness Pre-Check (per standard checklist item 4)

| File | Status field | Summary present | Gaps/flagged section | Key Takeaways | Rating |
|------|-------------|-----------------|----------------------|---------------|--------|
| 01-call-site-inventory.md | Complete (L6) | Yes (L181-191) | Yes — cross-cutting note + per-item flags (L191, L64) | Yes (Summary bullets) | Complete |
| 02-patterns-and-conventions.md | Complete (L3) | Yes (L177-184) | Yes — "Unverified / flagged" (L186-188) | Yes | Complete |
| 03-test-and-verification.md | Complete (L185; opens "In Progress" L3 then closes Complete L185) | Yes (L187) | Yes — caveats inline (L45, L165) | Yes | Complete (header inconsistency noted) |
| 04-template-and-examples.md | Complete (L233; opens "In Progress" L3) | Yes (L235-236) | Yes — gotchas (L222-230) | Yes | Complete (header inconsistency noted) |

Minor note: Files 03 and 04 carry a leading `Status: In Progress` (L3) and a trailing `Status: Complete`. The trailing status governs; both files are substantively complete. Flagged as cosmetic only — does not affect verdict.

---

## Evidence Quality + Spot Cross-Validation

I spot-verified the highest-leverage claims against the live working tree (`refactor/roadmap-pipeline-r0-r1-rewrite`) rather than trusting citations blindly:

| Claim (source) | Live check | Result |
|----------------|-----------|--------|
| R5 word-boundary FP: `\bD-?\d+\b` extracts `D01` from `M1-D01` (01 L140) | `re.findall(r'\bD-?\d+\b','M1-D01')` → `['D01']` | **CONFIRMED** — FP is real on current branch |
| `contracts.ID_PATTERNS` has FR/NFR/SC/G/D, NO `MD` (01 L122-132; 02 L24-31) | read `contracts/__init__.py:64-70` | **CONFIRMED** verbatim |
| gates global `_id_registry_sidecar_path` + setter accepts `None` (01 L42-43; 02 L116-117) | read `gates.py:1039-1049` | **CONFIRMED** verbatim |
| arch_lint Rule 2 = exact set-membership on `ast.Constant` str (01 L76; 02 L66; 03 L29) | read `arch_lint.py:168-172` | **CONFIRMED** |
| R1 docstring future-tense clause + contradicting import below (01 L19-30) | read `id_registry.py:19-38` | **CONFIRMED** — "R0.3 will hoist … the TODO comment below tracks that migration." present; import `ID_PATTERNS as _ID_PATTERNS` present at L38; NO actual TODO comment exists |
| R2 `execute_roadmap` entry + dry-run guard + `execute_pipeline` call + `_apply_resume` (01 L55-64) | grep `executor.py` | anchors CONFIRMED; **line numbers drift ±1-2** (see below) |

**Line-number drift (Minor, non-blocking).** File 01 cites `execute_roadmap` at L3397 (actual L3398), the dry-run early-return at L3490-3492 (actual `if config.dry_run:` at L3491), and the `execute_pipeline(...)` call at L3536-3543 (actual L3538). `_apply_resume` cited L3498 (actual L3499). `_save_id_registry` call cited L1365 — **exact**. The drift is ≤2 lines and every anchor is grep/symbol-findable. This is the expected aging of `file:line` citations against an evolving tree, not a fabrication. The builder should re-anchor by symbol at edit time (consistent with the project's context-freshness discipline) rather than trust the literal line numbers.

**Evidence ratio.** Across all four files, effectively every architectural claim carries a `file:line` (or `file:line-range`) citation. File 02 explicitly tags its two unverified items (L186-188: it did not run `make lint-architecture`/`make verify-sync` this pass, sourcing the "0 violations / passes" claims from the design doc + code structure). File 03 tags its one implementation-note caveat (L45) and one inferred/unverified baseline-harness claim (L165). No unsupported architectural assertions detected. Quality rating: **Strong** for all four files.

---

## Per-Criterion Verdicts (the 9 spawn-prompt criteria)

### Criterion 1 — Source files identified with paths and exports; every R1–R5 edit site has a concrete file:line — **PASS**

Every remediation item has a concrete production edit site:
- **R1:** `id_registry.py` L19-24 (text to replace) + contradicting import L37 (01 L13-30; verified — text matches verbatim, import present).
- **R2:** `gates.py` global L1039, setter L1042-1049, fail-shut L1069-1074, sidecar read L1089-1099; `executor.py` `_save_id_registry` L612, setter call L664, call-site L1365, entry `execute_roadmap` L3398, insertion point after dry-run guard before `execute_pipeline` (01 L40-64; 02 L99-121; 03 L56-68). Anchors verified; line numbers drift ≤2.
- **R3:** `arch_lint.py` walker L120/L137/L143, Rule 2 L168-185, allow-marker opt-out (01 L72-83; 02 L55-73; verified).
- **R4:** `repo-inventory.sh` `apply_scope()` L29-37, `set -e` L9, callers L49 + L66 (01 L89-112; 02 L153-154; verified by all three researchers independently — strong triangulation).
- **R5:** full blast radius across `contracts/__init__.py` L64-70, `spec_parser.py` L329-346, `structural_checkers.py` L295-333/L402-472, `id_registry.py` L39/L77-95/L106-122/L125+, `gates.py` L1089-1099 (01 §5a-5f; verified).

### Criterion 2 — Output paths and formats clear or reasonably inferred — **PASS**

Each edit/test/fixture has a landing site. R1 = single Edit in `id_registry.py` + acceptance grep. R2 = regression test in `tests/roadmap/test_spec_roadmap_id_containment.py` (03 §2). R3 = `tests/contracts/test_arch_lint.py` (03 §1). R4 = behavioral (run script + `make sync-dev`/`make verify-sync`; no pytest surface — 03 L159). R5 oracle = `tests/roadmap/test_structural_checkers.py::TestSignaturesChecker` + sidecar schema tests + conftest permissive sidecar (03 §4, L180). Fixture format documented (03 §3). MDTM handoff subdir conventions (`discovery/`, `plans/`, `test-results/`, `reviews/`, `reports/`) documented (04 §5).

### Criterion 3 — Logical breakdown of phases/steps (R5 reproduce→decide→conditional implement mappable) — **PASS**

File 04 §6 explicitly maps the investigation→decision→conditional-implementation flow to MDTM primitives: L1 Discovery (investigate each finding) → L5 Conditional-Action decision item writing `plans/*-decision.md` handling BOTH CLOSE and PROCEED branches → conditionally-gated remediation phases → M1 phase gate. The R5 path-a/path-b decision (reproduce FP → decide → conditionally port MD family) maps cleanly onto this. §9 supplies a concrete recommended phase shape (Prep → Investigation → Decision Gate → Conditional Remediation → Validation Gate → Final Validation → Post-Completion). The L5 invariant (output file always created regardless of branch, 04 L169) is the mechanism that makes the decision auditable on resume.

### Criterion 4 — Patterns and conventions documented with examples (contracts SoT, arch_lint, sync-dev, fail-shut) — **PASS**

File 02 is dedicated to this and is thorough: Contracts SoT / Contract #8 (§1, with the anchor-free-body convention §1c verbatim from `contracts/__init__.py:58-62` — load-bearing for R5), arch_lint three-rule enforcement + `--scan-paths src/superclaude/cli/` ONLY scope fact (§2, the reason R3 can't self-trip), fail-shut Contract #9 invariant table (§3a, every error path returns a string never True), sync-dev/`.claude/` never-stage discipline (§4, with the exact R4 procedure §4c). Each carries a worked example and file:line.

### Criterion 5 — MDTM template notes present with rule references (A3/A4/B2, decision-gate shape) — **PASS**

File 04 §3 documents A3 (complete granular breakdown, one item per file/component), A4 (iterative process structure with the pre-enumerate→per-item→consolidate pattern), and B2 (self-contained one-paragraph item carrying all 6 embedded elements) — each with the template line citation and a real-example confirmation from `TASK-RF-20260531-042405.md`. §4 covers the checkbox/Step-header format + anti-orphaning rule. §6 is the decision-gate shape (L5 conditional-action). §7 covers the M1 phase-gate QA sequence (aggregate → rf-qa spawn → conditional-proceed) with I16 fix-cycle caps. The rf-qa adversarial + `fix_authorization` pattern is correctly surfaced (04 L141), matching user memory `feedback_rfqa_adversarial_pattern.md`.

### Criterion 6 — Granularity sufficient for per-file/per-component checklist items (each R item decomposes cleanly) — **PASS**

R1 = 1 item (single Edit + grep). R2 = decomposes into reset-insertion + resume-reconciliation + regression test + MERGE_GATE-composition guard (each distinct). R3 = docstring-id-precompute implementation + 2 test cases. R4 = rc-capture in `apply_scope` + 2 caller surfacings + sync + verify-sync. R5 = the largest, decomposing per-layer (contracts → spec_parser → structural_checkers → id_registry → gates read + 3 ported tests + sidecar schema tests + conftest) — file 01 §5a-5f and 03 L180 enumerate each layer as a discrete edit, which maps to one A3 checklist item per layer. Decomposition is clean and per-component throughout.

### Criterion 7 — Documentation cross-validation: doc-sourced claims tagged CODE-VERIFIED/CONTRADICTED/UNVERIFIED — **PARTIAL PASS (Minor)**

The research does perform real cross-validation and surfaces the key contradiction (R1: the docstring says "R0.3 *will* hoist … TODO comment below tracks that migration" but the import already shipped and no TODO exists — 01 L25, 02 L179 — this is the literal CODE-CONTRADICTED finding that motivates R1, correctly surfaced). The R5 FP is empirically proven via live `uv run python` (01 L140) — stronger than a tag. **However**, the four files do not use the literal `[CODE-VERIFIED]` / `[CODE-CONTRADICTED]` / `[UNVERIFIED]` tag tokens from the rf-analyst spec. Instead they use prose equivalents: "CONFIRMED verbatim from Read", "verified via `uv run python`", "Contradicted by:", and an explicit "Unverified / flagged" section (02 L186-188; 03 L45, L165). The substance of cross-validation is present and the one true contradiction (R1) is surfaced; only the canonical tag tokens are absent. This is a **Minor** documentation-hygiene gap, not a coverage gap — it does not block synthesis or task-building because the validation status of every load-bearing claim is unambiguously stated in prose.

### Criterion 8 — R5 investigation surface complete (FP reproduction method, oracle tests location, md_ids blast radius) — **PASS**

This is the most important criterion for the track and it is the most thoroughly covered:
- **FP reproduction method:** proven, not asserted — `\bD-?\d+\b` on `M1-D01` → `D01` (01 L140, re-confirmed live in this report). The reproduction recipe (roadmap `M1-D01..M1-D54` vs spec `D1,D3,D5` → 51 phantom_id HIGHs) is stated.
- **Oracle tests location:** PR #111 head commit `861047c2`, reachable locally via `git show`, 3 tests in `tests/roadmap/test_structural_checkers.py::TestSignaturesChecker`, each summarized with its exact assertion (03 §4 L126-137; 01 L170-173). The `_write_md_fixture_with_allowlist` helper port is flagged.
- **md_ids blast radius:** fully traced across `SpecIdRegistry` dataclass field + `union_of_known` + `to_dict` + `build_id_registry` mapping + gates sidecar read + canonicalizer branch + tokenizer dedup + allowlist subsystem (01 §5a-5f, §"R5 minimum file set"; 03 L180). The "old sidecar round-trips via `.get(...,())` but MD IDs are unrepresentable until every layer changes together" coupling is correctly identified (01 L159).
- **Critical investigation insight (correctly elevated):** the "Explicit non-references" allowlist subsystem is ENTIRELY ABSENT from the current branch (not just MD), so R5 path-b is materially larger than the design doc's "add an MD entry" framing — the investigation must determine whether MD-family alone closes the FP or whether the allowlist port is also required (01 L168, L191). This is exactly the kind of design-doc-vs-reality gap the investigation gate exists to catch, and it is surfaced prominently.

### Criterion 9 — Unresolved ambiguities documented (esp. R2 resume-awareness; R5 path-a-vs-b decision) — **PASS**

- **R2 resume-awareness:** documented as a LIVE CONSTRAINT (01 L64): `--resume` calls `_apply_resume` which can skip extract → a blind unconditional `set_id_registry_sidecar_path(None)` at run-start would fail-shut MERGE on resume. Two reconciliation options offered (reset only when extract will run; or re-derive sidecar from existing file on resume), with the L1273-1279 precedent cited, and "Flagged for task author." The test-design hazard counterpart (autouse `_isolate_gates_state` reset would mask the leak; regression must use two-runs-in-one-process) is independently surfaced (03 L78-82). Strong.
- **R5 path-a-vs-b:** the decision is framed as an investigation gate, not pre-decided (01 L177 "This is why R5 is an investigation gate, not a one-liner"; 04 §6 models the CLOSE/PROCEED decision artifact). The open question (does MD-family alone suffice, or is the allowlist port also required for path b) is documented as the thing the investigation must resolve.
- Other flagged ambiguities: R2 path-identity guard deferred-vs-now (01 L62), R3 optional/droppable status (02 L67), baseline-delta harness is manual/no automated check exists (03 §6, marked unverified).

---

## Cross-File Contradiction Detection

No contradictions between the four research files. They cover disjoint domains by design (01 = edit sites/blast radius, 02 = conventions, 03 = tests, 04 = MDTM template) and where they overlap they AGREE and reinforce:
- R4 `apply_scope` site (L29-37, callers L49/L66) — independently cited identically by 01 and 02. Triangulated.
- arch_lint Rule 2 exact-membership + `ast.walk` parent-blindness + docstring-precompute requirement — agreed across 01 (L79-83), 02 (L66), 03 (L45). Triangulated.
- "MD absent on current branch; `spec_parser._REQUIREMENT_PATTERNS` auto-derives from `contracts.ID_PATTERNS`" — agreed across 01 (L137), 02 (L34), 03 (L137). Triangulated.
- R2 fail-shut preservation + "do NOT change the `Callable[[str], bool|str]` signature (R1.3 territory)" — agreed across 01 (L45) and 02 (L121). Triangulated.

The one minor INTRA-file inconsistency (files 03/04 leading `In Progress` vs trailing `Complete` status) is cosmetic, already noted, and does not affect content.

## Compiled Gaps

### Critical Gaps (block synthesis / task-building)
None.

### Important Gaps (affect quality)
None that block. The closest to "important" is correctly handled INSIDE the research rather than left as a gap: R5 path-b is larger than the design doc framing because the Explicit-non-references allowlist is wholly absent from the branch (01 L168/L191). This is surfaced as the central investigation question, which is the right disposition — it is a finding, not a gap.

### Minor Gaps (should be addressed; non-blocking)
1. **Canonical verification tags absent (Criterion 7).** Research uses prose ("CONFIRMED", "Contradicted by:", "Unverified / flagged") instead of the literal `[CODE-VERIFIED]`/`[CODE-CONTRADICTED]`/`[UNVERIFIED]` tokens. Owner: research agents (cosmetic) — OR accept as-is since validation status is unambiguous in prose. Recommended: accept; do not spend a fix cycle on tag tokens.
2. **Line-number drift ±1-2 in file 01's `executor.py` R2 citations.** `execute_roadmap` L3397→3398, dry-run guard L3490-3492→3491, `execute_pipeline` L3536-3543→3538, `_apply_resume` L3498→3499. Owner: builder — re-anchor by symbol (`grep -n "def execute_roadmap"`) at edit time rather than trusting literal line numbers. Non-blocking; anchors are findable.
3. **Files 03/04 leading-status header says `In Progress`.** Cosmetic. Trailing `Complete` governs.
4. **`make lint-architecture` / `make verify-sync` "currently passes / 0 violations" not freshly executed this pass** (02 L188, self-flagged). The builder's final validation phase runs these anyway (04 §7), so the live result is established at execution time. Non-blocking.

## Depth Assessment

**Expected depth:** Deep (remediation track requiring exact edit sites, blast-radius tracing, test homes, and MDTM scaffolding for an investigation→decision→conditional-implementation flow).

**Actual depth achieved:** Deep, met.
- Data-flow tracing present: R2 sidecar set→read path and resume-skip data flow (01 §R2); R5 write-side `to_dict` → read-side gates reconstruction coupling (01 §5e).
- Integration-point mapping present: R5 cross-layer blast radius (6 files + tests + fixtures, 01 §5).
- Pattern analysis present: contracts-SoT/anchor-free-body/arch_lint enforcement triad (02 §1-2).
- Empirical verification present: R5 FP proven via `uv run python` (01 L140); PR #111 oracle recovered from a remote/commit via `git show` (01 §5f, 03 §4).

**Missing depth elements:** None material. The optional path-identity guard for R2 (vs. plain reset) is correctly scoped as a follow-up decision rather than fully designed — appropriate for an investigation gate.

## Recommendations

1. **Proceed to task-building.** All five remediation items (R1–R5) have concrete edit sites, test homes, and convention constraints. The investigation→decision→conditional-implementation MDTM shape is fully specified (04 §6/§9).
2. **Builder must re-anchor R2 `executor.py` line numbers by symbol** at edit time (Minor Gap 2) — the line numbers have drifted ≤2 lines.
3. **Carry the R5 "allowlist subsystem is absent" finding into the investigation phase as an explicit decision point** (does MD-family alone close the FP, or is the allowlist port also required for path b?). This is the single most important carry-forward.
4. **Carry the R2 resume-awareness constraint into the R2 implementation item** — the reset must be resume-aware (reset only when extract will run, or re-derive sidecar on resume); a naive unconditional reset breaks `--resume`.
5. **Carry the R2 test-design hazard** — the regression must exercise two sequential runs in ONE process body to defeat the autouse `_isolate_gates_state` reset that would otherwise mask the leak (03 L78).
6. **Do not spend a fix cycle on verification-tag tokens** (Minor Gap 1) — validation status is already unambiguous in prose.

---

## VERDICT: PASS

All 9 spawn-prompt criteria PASS (Criterion 7 is PASS with a Minor documentation-hygiene note). Zero critical gaps, zero blocking important gaps; four Minor non-blocking gaps, all with clear owners and none requiring a research fix cycle. The research is deep, evidence-based, cross-validated against the live tree, internally consistent (no contradictions), and complete across edit sites (Criterion 1), output landing sites (2), phase/step decomposition (3, 6), conventions (4), MDTM template rules (5), documentation cross-validation (7), the R5 investigation surface (8), and unresolved ambiguities (9). The four files are cleared to feed `/task-builder`.
