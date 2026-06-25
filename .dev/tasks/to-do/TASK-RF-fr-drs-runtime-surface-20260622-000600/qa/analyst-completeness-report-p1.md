# Research Completeness Verification — Partition P1 (module-build cluster)

**Analysis type:** completeness-verification
**Lens:** completeness (BREADTH — sufficient coverage for granular per-unit/per-seam checklist items)
**Track:** FR-DRS deterministic runtime-surface sweep
**Date:** 2026-06-22
**Partition:** P1 of (multi-partition run; cross-file checks limited to P1 subset)
**Files analyzed (4):**
- `01-module-design-and-spec-port.md` (R1 — module algorithm/types/orchestrator)
- `02-product-path-integration-seam.md` (R2 — runner product-path wiring)
- `03-consumer-wiring-contract-and-prefilter.md` (R3 — contract.py consumer + §5.3 pre-filter)
- `04-audit-reuse-sources-and-adaptation.md` (R4 — cli/audit reuse sources + adaptation)

> [PARTITION NOTE: Cross-file checks (contradictions, cross-references, coverage audit against scope) are applied only within the P1 subset. Full cross-file analysis requires merging all partition reports.]

---

## Criterion-by-criterion findings

### Criterion 1 — All 6 logical units + all DESIGNED types covered with signatures (file 01)? — PASS

**Units (6/6 with pinned signatures):** File 01 §1 documents every unit with a pinned signature, responsibility, inputs, outputs, ported behavior, and per-unit degrade rules:
- Unit 1 `tag_surfaces(diff_hunks, allowlist) -> list[TaggedSurface]` (§1, Unit 1) — symbol-anchored tagging + degrade rules + fast-path origin.
- Unit 2 `find_referrers(surfaces, *, lsp=None) -> list[ReferrerEdge]` (Unit 2) — rg/AST floor ground truth, LSP-never-load-bearing degrade rules.
- Unit 3 `partition_referrers(edges, lang_table) -> PartitionedReferrers` (Unit 3) — per-language table, unknown→DEGRADE.
- Unit 4 `degrade_oracle(surface, partitioned) -> DegradeVerdict` (Unit 4) — 4-category oracle, runs-before-UNREACHED.
- Unit 5 `rootwalk_entrypoints(surface, roots) -> RootwalkResult` (Unit 5) — depth=1 walk, partial→DEGRADE.
- Unit 6 `reduce_ledger(rows) -> tuple[dict[str,str], ContractScalars]` (Unit 6) — precedence + count invariant.
- Plus the I2 root-enumeration algorithm (§1.7) feeding Unit 5, with a completeness gate.

**Types (15 designed, all with compact field shapes):** §2 tables cover 4 inputs (`DiffHunk`, `SurfaceAllowlist`, `TestCommentTable`, `LspOverlay`), 6 intermediates (`TaggedSurface`, `ReferrerEdge`, `PartitionedReferrers`, `EntrypointRoot`, `RootwalkResult`, `DegradeVerdict`), 4 output/modeled (`RuntimeSurfaceLedgerRow`, `UnreachedSurface`, `ContractScalars`, `SweepResult`) with dataclass-vs-TypedDict guidance and exact field shapes. The 7-step→6-unit collapse is explained (§1 bridge note: reduce+emit collapse into `reduce_ledger`).

**Evidence sufficiency for checklist items:** §9 explicitly enumerates the builder checklist-item map (15 type items, 6 unit items, 2 helper items, 1 orchestrator, 1 invariant). Granular per-unit decomposition present.

### Criterion 2 — Product-path seam fully documented (file 02)? — PASS (with a flagged unresolved gap that is correctly surfaced, not a coverage hole)

- **Insertion point:** §2/§7 pin it exactly — a new block between `runner.py:444` and `runner.py:445`, after both author branches join, strictly before `parse_contract`. [CODE-VERIFIED line anchors].
- **`run_sweep` arg construction:** §1 has a per-arg sourcing table (one row per arg), with status tags. This is sufficient granularity for per-arg checklist items.
- **Merge-before-parse ordering:** §3 (DELIVER #3) documents the EMIT-before-`parse_contract` ordering invariant, the D4 rationale, and the fix-loop re-audit re-run at `runner.py:561-562` (sweep must live inside `_audit_once`, not `run()`).
- **Writer convention:** §5 (DELIVER #5) mandates `_IndentDumper` + `_atomic_write_text`, names the ensemble bare-`safe_dump` anti-pattern at `ensemble.py:634-635`, and explains the yamllint nested-sequence reason.
- **Bonus coverage:** §4 Tier-1/Tier-2 author paths + the `REFLECT_CONTRACT_VERSION = "1.0"` vs SKILL `1.6.0` defect (flagged for the task); §6 the bare `claude -p` coverage gap + the `runtime_surface_sweep_ran` detection contract shared with R6.

This criterion PASSES. The R2 `run_sweep` arg gap (see Criterion 7) is a *correctly surfaced* unresolved ambiguity, not a missing-coverage failure.

### Criterion 3 — Consumer wiring (contract.py additions) documented with file:line (file 03)? — PASS

All four consumer-side wiring points are documented with current, re-verified file:line anchors and exact change shapes:
1. **Token-membership reuse:** ADD `"runtime-surface:backend_unavailable"` to `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31-33); fires existing `any(...)` at contract.py:259-260 → reuses `"degraded-components"` slug. Verbatim before/after frozenset given. RECOMMENDED vs the independent-trigger alternative is dispositioned (write token-membership; record alternative as a note only).
2. **Regression reuse (halt path):** `_halted_reason` (contract.py:307/324-325) is NO-EDIT by design (I7: no 5th deviation class); producer populates `deviation_count_by_class.regression`; existing branch reuses `"regression"`. Builder item shaped as a proof/test obligation, not an edit.
3. **Count guard:** mirror the `_LOAD_BEARING_BOOL_FIELDS` fail-closed block (contract.py:200-209) for `len(unreached_surfaces) == runtime_surface_unreached`; suggested code block + slug `"malformed-runtime-surface-count"`; correctly marked RECOMMENDED-mirror with a defer-to-builder caveat (producer already guarantees by construction).
4. **`surface_unreached` derivation:** integer ≥1 from successful sweep → `"runtime_surface_unreached"` literal string; owner = runner._audit_once merge point (RECOMMENDED), `derive_verdict` (FALLBACK); §15.4a truth table reproduced verbatim. SKILL §5.3 lines 390-391/402/412 re-anchored as verify-and-leave.

The "contract.py currently has ZERO runtime-surface wiring (grep-confirmed)" ground-truth finding establishes Phase 2 is net-new, which sharpens checklist granularity.

### Criterion 4 — Audit reuse fully documented (file 04)? — PASS

- **`_bfs_reachable` adaptation:** §1 gives the verbatim source body (`reachability.py:591-635`), the three load-bearing facts to invert (unbounded BFS → depth=1 at call site; the `depth>50` guard at `:460` is module-parse NOT BFS — explicit builder-trap flag; dynamic→UNREACHABLE inverts to →DEGRADE), and a reflect-local `rootwalk_depth1` skeleton with both inversions baked in.
- **DATA-copies:** §2 gives verbatim `_TEST_PREFIXES`/`_TEST_INFIXES` (`filetype_rules.py:106-107`) with the unknown→SOURCE→DEGRADE inversion, and verbatim `_DYNAMIC_PATTERNS` (`dynamic_imports.py:24-39`) with the KEEP:monitor→DEGRADE inversion.
- **Inversions:** every reuse row states the audit doctrine and the required runtime-surface inversion in a side-by-side table (§1.2, §2.1, §2.2, §5).
- **Boundary decision:** §4 documents the import-ban naming ONLY cli/sprint+cli/roadmap (audit import legal-but-coupled), the `runner.py:14-17` `_IndentDumper` copy-over-import precedent, and the Option C ratification with full TDD cross-refs.
- **`_safe_parse` fail-soft pattern** (§3) and the per-Reuse-Audit-row disposition for all 6 units (§5) are present; §6 emits the exact "copy X, invert default Y" builder action lines.

### Criterion 5 — Granularity sufficient for per-file/per-unit checklist items? — PASS

Each file ends with an explicit builder-facing decomposition: 01 §9 (checklist-item map + cross-researcher boundaries), 02 §7 (precise wiring facts), 03 §6 (reuse-not-rebuild manifest table), 04 §6 (6 numbered "copy X, invert Y" action lines). Cross-researcher ownership boundaries are stated in each file (01 §9, 03 §6 boundary notes, 04 header), which prevents duplicate checklist items across the build cluster. A builder can write granular per-unit/per-type/per-seam items directly from these.

### Criterion 6 — Doc-sourced claims tagged [CODE-VERIFIED]/[SPEC]/[UNVERIFIED]? — PASS

- File 01 defines and uses `[SPEC]` (forward-looking design from `refs/runtime-surface.md` RS:L / TDD §) vs `[CODE-VERIFIED]` (seam facts confirmed against source), and the Summary restates the tagging discipline.
- File 02 defines `[CODE-VERIFIED]` / `[UNVERIFIED]` / `[TDD]` and applies them per-row in the arg table; §0 lists all files read with line ranges.
- File 03 marks every line-number claim `[CODE-VERIFIED]` with a re-anchor preamble (§0) and dates the verification.
- File 04 uses `[CODE-VERIFIED]` per-citation and explicitly downgrades the few un-re-read offsets (`dependency_graph.py`, `tool_orchestrator.py:146`, `dead_code.py:155`) to `[UNVERIFIED]` (table-sourced) — exemplary honesty about evidence boundaries.

No untagged doc-sourced architectural claims detected in the P1 subset.

### Criterion 7 — Unresolved ambiguities documented? — PASS (strong)

The key ambiguities are surfaced loudly rather than papered over:
- **R2 `run_sweep` arg gap (file 02 §1 KEY FINDING + §7):** of 6 positional args, only 3 map to existing `ReflectConfig` fields. `diff` (no diff-text field — compute `git diff config.base`), `scope_worktree` (no field — derive `Path.cwd()` or add field), and `availability_surface` (NO field AND no Wave-0 probe exists anywhere — grep-confirmed) are flagged, and the TDD §8.1.2 "already on the config" claim is explicitly called INCORRECT against current source. The task MUST resolve each — this is documented as a builder decision, not silently assumed.
- **availability_surface absence (file 02 §1):** explicitly grep-confirmed absent; fallback (pass floor-forcing empty dict) noted.
- **`REFLECT_CONTRACT_VERSION = "1.0"` vs `1.6.0` (file 02 §4):** flagged as a separate real defect to reconcile.
- **Bare `claude -p` coverage gap (file 02 §6):** documented as out-of-seam, conditional SKILL fallback keyed on `runtime_surface_sweep_ran`.
- **Count-invariant consumer guard necessity (file 03 §3):** correctly flagged as defer-to-builder (producer guarantees by construction), slug naming deferred.
- **`scope_worktree` derivation, engine choice OQ-DRS.1 (file 04 §5 row 2):** noted as an engine, not reuse, choice.

---

## Completeness check (file status / required sections)

| File | Status line | Summary | Gaps/ambiguities surfaced | Builder decomposition | Rating |
|------|-------------|---------|---------------------------|----------------------|--------|
| 01 | `Status: Complete` (L5) + `Status: Complete` (L259) | Yes (§Summary, 8 pts) | Yes (cross-researcher boundaries; SPEC-vs-verified) | Yes (§9) | Complete |
| 02 | `Status: Complete` (L201) | Yes (§7) | Yes (3-arg gap KEY FINDING) | Yes (§7) | Complete |
| 03 | `Status: Complete` (L226) | Yes (§6 + closing) | Yes (count-guard defer; owner straddle) | Yes (§6 manifest) | Complete |
| 04 | **HEADER `Status: In Progress` (L5)** vs `## Status: Complete` (L265) | Yes (§Summary) | Yes (UNVERIFIED offsets) | Yes (§6) | Complete-content, status-line inconsistent |

## Contradictions found (within P1 subset)

None substantive. The four files are mutually consistent and explicitly de-conflicted via stated ownership boundaries:
- The six-scalar emit / writer convention is consistently described across 01 §1.6/§7, 02 §5, and 04 §5.1 (all mandate `_IndentDumper` + `_atomic_write_text`; all name the ensemble `safe_dump` anti-pattern).
- The "6th field `unreached_surfaces` has NO `runtime_surface_` prefix" caveat appears consistently in 01 §7 and 02 §2.
- The count invariant `len(unreached_surfaces) == runtime_surface_unreached` is described identically as holding by construction (01 §5.2, producer) and as a consumer fail-closed mirror (03 §3); these are complementary layers, not a contradiction.
- The `surface_unreached` derivation owner (runner._audit_once merge point) agrees between 01 §7 (§5.3 note), 02 (the merge seam), and 03 §4 (RECOMMENDED owner = runner, fallback = derive_verdict). Cross-references are present and consistent.

## Minor flags (must still be fixed — non-blocking)

1. **File 04 status-line inconsistency:** header frontmatter says `**Status:** In Progress` (L5) while the body closes with `## Status: Complete` (L265) and a full Summary. Content is complete; the header status line should be corrected to `Complete` so the downstream completeness gate (which may scan the header) does not mis-read it as unfinished. This is the single concrete defect in the P1 subset.

## Depth assessment (Deep tier)

Expected Deep-tier elements — data-flow traces, integration-point mapping, pattern analysis, signature-level design — are all present:
- Data flow: the 7-stage `run_sweep` wiring (01 §3) and the EMIT→merge→`parse_contract` ordering (02 §3) trace the full producer path.
- Integration points: exact insertion line (02 §2/§7), the four contract.py consumer points (03), and the six audit reuse sources with line anchors (04).
- Pattern analysis: dataclass-vs-TypedDict guidance (01 §2), the asymmetric-cost DEGRADE posture (01 §8, 04 §1.2), reuse-not-rebuild + inversion semantics (04). Depth is sufficient for granular checklist-item authoring.

## Recommendations

1. **Fix the file 04 header status line** (`In Progress` → `Complete`) before the build phase. (Minor; the only concrete in-subset defect.)
2. **Carry the R2 3-arg gap forward as explicit task decisions** — `diff` (compute `git diff config.base`), `scope_worktree` (derive/add field), `availability_surface` (add probe or pass floor-forcing empty dict). The research correctly flags these as unresolved; the task file must turn each into a decided checklist item (do NOT let them inherit the TDD's incorrect "already on the config" assumption).
3. **Resolve the `REFLECT_CONTRACT_VERSION` "1.0" vs SKILL "1.6.0" defect** as a separate flagged item (02 §4).
4. **Treat the count-invariant consumer guard (03 §3) as a builder-consensus decision** — research correctly notes the producer guarantees it by construction, so the consumer mirror is optional/defensive.

---

## VERDICT: PASS

All 7 lens criteria PASS. The P1 "module-build cluster" research (module algorithm/types/orchestrator, product-path seam, contract.py consumer wiring, cli/audit reuse) is sufficiently broad and granular for a builder to write per-unit / per-type / per-seam checklist items. Unresolved ambiguities (notably the R2 3-arg gap and the availability_surface absence) are correctly and loudly surfaced as builder decisions rather than silently assumed. Evidence tagging discipline is strong across all four files.

### Gap list (non-blocking — must still be fixed, none block the build gate)

**Minor:**
- M1. File 04 header status line says `In Progress` (L5) but content is complete and closes `Status: Complete` (L265) — correct the header. (Cosmetic/gate-hygiene; the only concrete in-subset defect.)

**Carry-forward decisions (correctly surfaced by research; the task file must convert each to a decided item — not research gaps):**
- D1. `run_sweep` `diff` arg: no diff-text config field → compute `git diff config.base` (02 §1).
- D2. `run_sweep` `scope_worktree` arg: no config field → derive `Path.cwd()` or add field (02 §1).
- D3. `run_sweep` `availability_surface` arg: no field AND no Wave-0 probe exists → add probe or pass floor-forcing empty dict; TDD "already on the config" claim is wrong against source (02 §1).
- D4. `REFLECT_CONTRACT_VERSION = "1.0"` vs SKILL `1.6.0` reconciliation (02 §4).
- D5. Count-invariant consumer guard + slug naming deferred to builder consensus (03 §3).
