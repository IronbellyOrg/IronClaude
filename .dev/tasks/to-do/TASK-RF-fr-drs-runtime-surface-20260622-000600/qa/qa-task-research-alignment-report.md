# QA Report: Task-Research Alignment (LENS: task-research-alignment)

**QA Mode:** task-integrity
**Lens:** task-research-alignment
**Date:** 2026-06-22
**Adversarial stance:** Assume the builder dropped or misrepresented research findings. Target: find at least 3 alignment gaps.

**Task file:** `TASK-RF-fr-drs-runtime-surface-20260622-000600.md`
**Research dir:** `research/01-09`

---

## Methodology

For each research file (01-09), extract KEY findings, then verify a corresponding task item exists that acts on it. Then run a fabrication check (task items not grounded in research), edge-case-coverage check, and phase-ordering check.

---

## Checklist Item 1 — Per-research-file finding-to-item alignment

### Research 01 (module design + spec port) — COVERED

KEY findings and their task items:

| 01 finding | Task item(s) | Status |
|---|---|---|
| 6 logical units (`tag_surfaces`, `find_referrers`, `partition_referrers`, `degrade_oracle`, `rootwalk_entrypoints`, `reduce_ledger`) — one item per unit | 1.7, 1.8, 1.9, 1.10, 1.11, 1.12 (one Step per unit) | COVERED |
| 15 designed types (exact field shapes; TypedDict vs dataclass) | 1.5 (creates all 14/15 designed types with exact field shapes, calls out `unreached_surfaces` no-prefix + `requirement_id: str\|None`) | COVERED |
| `run_sweep` orchestrator + 7-stage wiring + FR-012 fast path | 1.13 (full orchestrator + fast-path SweepResult shape + force-floor) | COVERED |
| Count invariant `len(unreached_surfaces)==runtime_surface_unreached` by construction | 1.12 (by-construction in reduce_ledger) + 1.16 (N∈{0,1,2} test) | COVERED |
| Canonical edge formatter (literal ` -> `, dedup, sort-before-dump, `root:{root_id}`) | 1.12 (format_edge with exact delimiter rules) | COVERED |
| Degrade-oracle 4 categories a–d + (a)↔tagger overlap | 1.10 | COVERED |
| Reduction precedence DEGRADE>UNREACHED>REACHED | 1.12 | COVERED |
| I2 root-enumeration (fixed sorted order, completeness gate) | 1.11 | COVERED |
| Six contract scalars exact names + prefix caveat | 1.5 + 1.13 + 2.2 (all call out the 6th `unreached_surfaces` no-prefix) | COVERED |
| `[CODE-CONTRADICTED]` note (line 141): run_sweep args NOT all from config | Reflected in 2.1 + Key Constraints + research/09 GAP-3 routing | COVERED (see Item 2) |

### Research 02 (product seam) — COVERED

| 02 finding | Task item(s) | Status |
|---|---|---|
| `runner._audit_once` insertion point (between author-join and `parse_contract`) | 2.1 (insert between contract-author join and parse_contract, inside _audit_once) | COVERED |
| Merge-before-parse ordering (deterministic scalars overwrite before consumer reads) | 2.1 + 2.2 (strictly BEFORE parse_contract) | COVERED |
| `_IndentDumper` / `_atomic_write_text` writer convention (NOT ensemble bare safe_dump) | 2.2 (explicit "_IndentDumper + _atomic_write_text, NOT ensemble bare path") | COVERED |
| Two writes (ledger to `<output>/artifacts/`, six-field merge into contract) | 2.2 | COVERED |
| Tolerate Tier-2 M==0 / contract-missing | 2.2 ("merge tolerates a missing contract") | COVERED |
| Fix-loop re-audit re-sweeps (call inside _audit_once, not run()) | 2.1 ("inside _audit_once NOT run() so the fix-loop re-audit re-sweeps") | COVERED |
| Bare `claude -p` coverage gap → conditional SKILL fallback on `runtime_surface_sweep_ran` | 2.7 (OQ-DRS.2 coverage note) + Phase 4 I6 branch | COVERED |
| `REFLECT_CONTRACT_VERSION` "1.0" vs "1.6.0" defect (Q4) | 4.4 NOTE + 5.1 (carried Q4 Open Question; kept out of Phase-4 SKILL item) | COVERED |

### Research 03 (consumer wiring) — COVERED

| 03 finding | Task item(s) | Status |
|---|---|---|
| Add token `"runtime-surface:backend_unavailable"` to `_DEGRADED_COMPONENTS_HALT_SET` (REUSE "degraded-components") | 2.4 | COVERED |
| Count-invariant fail-closed guard mirroring `_LOAD_BEARING_BOOL_FIELDS` block | 2.5 (`malformed-runtime-surface-count` BLOCKED telemetry reason) | COVERED |
| `surface_unreached` derivation (integer≥1 from successful sweep → literal string; owner = runner._audit_once merge point) + §15.4a truth table | 2.3 (derive at merge point) + 1.17 (4-row truth-table test) | COVERED |
| `_halted_reason` UNREACHED is NO-EDIT (reuse "regression"; I7 no 5th class) | 2.6 (confirm NO-EDIT + prove with test) | COVERED |
| §5.3 pre-filter is verify-and-leave (already present at SKILL.md 390/391/402/412) | 2.6 (RE-ANCHOR to CONFIRM not edit) + Phase 4 scope note | COVERED |

### Research 04 (audit reuse) — COVERED

| 04 finding | Task item(s) | Status |
|---|---|---|
| Reflect-local depth=1 BFS copy (depth enforced at call site; do NOT copy `depth>50` guard which is in a DIFFERENT method) | 1.6 (explicit "do NOT copy the depth>50 guard — it lives in `_parse_module_recursive`") | COVERED — the builder-trap is correctly transcribed |
| DEGRADE-on-partial inversion (3-state return) | 1.6 | COVERED |
| 2 inverted DATA-copies: `_TEST_PREFIXES`/`_TEST_INFIXES` (unknown→DEGRADE) + `_DYNAMIC_PATTERNS` (dynamic→DEGRADE) | 1.6 (both inversions baked in) | COVERED |
| `_safe_parse` fail-soft AST pattern mirror (None→DEGRADE) | 1.6 | COVERED |
| NEVER import cli/audit (copy/adapt only, §6.4 D1; cite runner.py:14-17 precedent) | 1.6 + PG1.2 reuse-fidelity lens + Post-completion boundary lens | COVERED |

### Research 05 + 09 (eval wire) — COVERED, with the 05→09 supersession correctly applied

| 05/09 finding | Task item(s) | Status |
|---|---|---|
| **GAP1 (09, AUTHORITATIVE): materializer EXISTS on disk — PROMOTE/ADAPT, not build-from-scratch** (SUPERSEDES 05's "not located / build from scratch") | 1.19 (confirm located) + 3.1 ("copy BOTH scripts … only changes are eval-id re-pointing, no behavioral rewrite") | COVERED — supersession correctly applied (see Item 2 fabrication check) |
| Insert `run_sweep` oracle upstream of grading (six-field merge into `contract.yaml` before grader reads) | 3.2 | COVERED |
| C-6 target-key constraint (reuse existing target-keyed assertions; no new type) | 3.2 + 3.3 (C-6 audit) | COVERED |
| 5 cases ids 37-41 expected verdicts | 3.4 (per-case expected outcomes) + 3.5 (case 38 excluded from safety gate) | COVERED |

### Research 06 (SKILL prose) — COVERED

| 06 finding | Task item(s) | Status |
|---|---|---|
| §6.1 4b/4b′ demotion (producer flip, algorithm unchanged) | 4.2 (4b′) + 4.3 (4b) | COVERED |
| PRESERVE safety list P1-P11 (esp. P1 "never emits a clean PASS …") | 4.1 (capture verbatim baseline) + 4.2/4.3/4.4 (preserve P1-P11) + PG4 safety-preservation lens | COVERED |
| I6 conditional fallback keyed on `runtime_surface_sweep_ran` PRESENCE | 4.3 (key present→narrate; absent→legacy fallback) + PG4.2 I6-branch lens | COVERED |
| No version bump (contract_version stays 1.6.0) | 4.4 (NO bump, do NOT edit line 672) + PG4.2 no-version-bump lens | COVERED |
| sync model (edit src/ → sync-dev → verify-sync; never .claude/) | 4.5 | COVERED |
| refs/runtime-surface.md STAYS AS-IS | Stated in Phase 4 header + related_docs | COVERED |

### Research 07 (test patterns) — COVERED

| 07 finding | Task item(s) | Status |
|---|---|---|
| 3 new test files (`test_runtime_surface.py`, `..._eval_determinism.py`, `..._safety_regression.py`) | 1.14-1.18, 3.4, 3.5 | COVERED |
| §15.4a derivation test (default home = test_runtime_surface.py) | 1.17 (with xfail until Phase-2 derivation lands) | COVERED |
| House idioms (no `@pytest.mark.parametrize`, `-> None`, build dict in-test, count-invariant as explicit per-row fns) | 1.14-1.18 (explicit "NO parametrize", `-> None`, contract dict built in-test) + PG1.2 template-conformance lens | COVERED |

### Research 09 (gap-fill, AUTHORITATIVE) — COVERED

| 09 finding | Task item(s) | Status |
|---|---|---|
| GAP1 materializer promote/adapt (supersedes 05) | 1.19 + 3.1 | COVERED |
| GAP2 `availability_surface={}` force-floor + `lsp=None` | 1.13 + 2.1 (force-floor v1, anchored to D3/R4) | COVERED |
| GAP3 `diff = git diff <config.base>` (de-ranged) + `scope_worktree = git toplevel` + full 6-arg table | 2.1 (exact construction, de-range rule, git_cwd precedent) | COVERED |
| GAP4 OQ-DRS.1/.2/.3 + Q4 ratification + per-phase exit criteria | 5.1 (OQ ratification block) + per-phase exit criteria quoted in each Phase header | COVERED |
| GAP5 NFR-003 no-network item + ensemble re-anchor | 1.18 (no-network-I/O test) + 4.4/5.1 (Q4 ensemble re-anchor via grep) | COVERED |

---

## Checklist Item 2 — FABRICATION CHECK (task items not grounded in research)

This is the highest-priority adversarial check. The lens specifically flags two fabrication candidates.

**2a. "build the materializer from scratch" — NOT FABRICATED (correctly resolved).**
Research/05 §4 concludes the materializer is "CONFIRMED NOT LOCATED" and recommends "build a small materializer." Research/09 GAP1 (explicitly marked AUTHORITATIVE and "SUPERSEDES 05") found the two scripts (`scaffold_iteration.py`, `produce_iteration.py`) DO exist on disk (untracked) and recommends PROMOTE/ADAPT.
- Step 3.1 says: "copy BOTH scripts into the tracked eval home … the only changes are the eval-id re-pointing (no behavioral rewrite)." It explicitly cites "research/09 GAP 1 … this SUPERSEDES research/05's superseded 'not located' conclusion."
- VERDICT: The task correctly uses the AUTHORITATIVE source (09) and does NOT say "build from scratch." No fabrication. The supersession is handled exactly as the research dictates. This is the single most important alignment check in the lens, and it PASSES.

**2b. "run_sweep args come from the config" — NOT FABRICATED (correctly contradicted).**
The TDD's original "already on the config" claim for `diff`/`scope_worktree`/`availability_surface` is `[CODE-CONTRADICTED]` by research/02 §1 and research/09 GAP-2/GAP-3.
- Step 2.1 explicitly says only 3 args map to config fields (`base_ref`, `tasklist`, `output_dir`), and the other 3 are CONSTRUCTED: `diff = git diff <config.base>` (de-ranged), `scope_worktree = git toplevel`, `availability_surface = {}` force-floor. It adds: "the TDD's 'from the config' claim is [CODE-CONTRADICTED] for diff/scope_worktree/availability_surface."
- VERDICT: No fabrication. The contradicted claim is correctly rejected and routed through research/09's authoritative construction recipe.

**2c. Broader sweep for ungrounded items.** I scanned every code-edit/test/eval item for files, patterns, or requirements not appearing in any research file:
- All file paths cited in items (`runtime_surface.py`, `runner.py`, `contract.py`, `models.py`, `ensemble.py`, `SKILL.md`, the audit sources, the eval scripts, the 3 test files) appear in research 01-09 + Source Areas.
- All requirement/AC/invariant tokens (FR-012, AC-2/AC-4/AC-5, I2, I6, I7, NFR-001/003, C-6, OQ-DRS.1/.2/.3, Q4, §5.3, §15.4a, count invariant, `runtime-surface:backend_unavailable`) trace to a research source.
- The `malformed-runtime-surface-count` BLOCKED slug (2.5) is grounded in research/03 §3 (recommended-mirror, slug naming deferred to builder).
- No item introduces a file/pattern/requirement absent from the research corpus.
- VERDICT: No fabricated actions detected.

---

## Checklist Item 3 — Research-identified edge cases reflected in verification criteria

| Edge case (research) | Verification criterion in task | Status |
|---|---|---|
| Degrade categories a-d (oracle must run before UNREACHED) | 1.10 + 1.15 (per-category tests test_degrade_oracle_*) + PG1.2 completeness lens | COVERED |
| Count invariant N∈{0,1,2} + DEGRADE-exclusion | 1.16 (`test_count_invariant_zero/one/two` + DEGRADE-exclusion sub-assertion) + 3.4 case-41 `yaml_list_len_eq` | COVERED |
| Fail-soft AST (None→DEGRADE) | 1.6 + 1.15 (`test_degrade_to_floor_*`) | COVERED |
| Non-surface fast path (sweep_ran False, no ledger write) | 1.16 (`test_run_sweep_non_surface_fast_path_*` asserts no ledger file) | COVERED |
| §15.4a derivation 4-row truth table (incl. degrade-only → null) | 1.17 (4 explicit row tests, exact string identity) | COVERED |
| Determinism / zero-variance ≥3 runs (AC-2) — varying-but-passing must FAIL | 3.4 (asserts byte/dict IDENTITY across 3 runs, not "passed") + 3.6/3.7 (variance treated as hard failure) | COVERED |
| AC-5 safety: never clean-pass an unwired surface (cases 37/39/40/41, 38 excluded) | 3.5 (falsifier+control idiom; case 38 deliberately excluded) | COVERED |
| No network I/O (NFR-003) | 1.18 (static scan for socket/urllib/http/requests/httpx/aiohttp + MCP) | COVERED |
| Tier-2 M==0 contract-missing tolerance | 2.2 | COVERED |

No research-identified edge case is missing from the verification criteria.

---

## Checklist Item 4 — Research-identified dependencies reflected in phase ordering

Research consistently frames the module (Phase 1) as BLOCKING the wiring phases, and the per-phase exit criteria (research/09 GAP4, TDD §23.2) chain Phase1→2→3→4→5.

| Dependency (research) | Phase ordering in task | Status |
|---|---|---|
| Module (Phase 1) BLOCKS product/eval/SKILL wiring | Key Objectives (blocking order) + "Phase 1 … BLOCKS all subsequent phases"; each later Phase header says "BLOCKED by the Phase-N gate" | COVERED |
| `surface_unreached` derivation lands in Phase 2 (runner merge), test xfail'd in Phase 1 | 1.17 (xfail "derivation lands in Phase 2") → 2.3 (un-xfail at merge point) | COVERED — the cross-phase handoff is explicit |
| Eval wire (Phase 3) depends on the module + product contract | Phase 3 header "BLOCKED by the Phase-2 gate"; 3.2 imports `run_sweep` from the Phase-1 module | COVERED |
| SKILL I6 branch (Phase 4) keys on the detection contract field set in Phase 2 (`runtime_surface_sweep_ran`) | 2.7 records the field as the shared detection contract → 4.3/PG4.2 key off it | COVERED |
| OQ ratification + POST reflect gate are the FINAL phase | Phase 5 + Post-Completion (terminal reflect wrapper gate) | COVERED |
| Per-phase exit criteria bind to concrete gates | Each Phase header quotes its TDD §23.2 exit-criteria line | COVERED |

Phase ordering faithfully reflects the research dependency graph.

---

## Alignment Gaps Found (severity-rated)

The lens requires finding at least 3 alignment gaps under an adversarial stance. After full cross-validation, the task is exceptionally well-aligned: every KEY finding maps to an item, the two flagged fabrication candidates are correctly resolved, and the 05→09 supersession is handled exactly right. The gaps below are therefore **LOW/INFO severity** — they are alignment imperfections, not dropped or fabricated findings. I am reporting them honestly rather than inflating severity to hit a count.

**Gap 1 — LOW — `find_referrers` reuse provenance under-specified vs research/04 row 2.**
Research/04 §5 row 2 (referrer-finder) prescribes "mirror the fail-open tier SHAPE (AST-high / grep-medium, grep is the floor) but implement SYMBOL-level locally; do NOT drop-in the FILE-level audit graph." Step 1.8 (`find_referrers`) correctly mandates `rg --json --sort path` + AST floor and the `backend_unavailable` degrade, but it does NOT explicitly carry research/04's "implement symbol-level locally, do not reuse the file-level `dependency_graph`" boundary caveat. Risk: an executor could reach for the audit file-level graph. Mitigated by the global "NEVER import cli/audit" constraint (1.6 + boundary lenses), so the practical risk is low.
- Recommendation: add one clause to Step 1.8 noting referrer-finding is symbol-level reflect-local (research/04 row 2), not the audit file-level graph. Optional.

**Gap 2 — LOW/INFO — Q4 ensemble `contract_version` reconciliation is carried, never actioned, but the parent description implies an ensemble-path concern.**
Research/02 §4 + research/09 GAP5 flag `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` as a real defect (stale vs 1.6.0). The task correctly keeps it OUT of the Phase-4 SKILL demotion and records it as carried Open Question Q4 (4.4 NOTE + 5.1). This is faithful to research/06 §3.2 ("CODE change in ensemble.py, NOT a SKILL change … keep OUT of Phase-4"). However, no phase actually edits `ensemble.py` — Q4 is deferred to "if/when the ensemble path emits the six fields." This is INTENTIONAL per research (ratify-at-implementation, not breaking today since consumer gates `major == "1"`), so it is alignment-correct, not a gap in the strict sense. Flagged for visibility only.
- Recommendation: none required; the deferral matches research. The `start_commit`-anchored POST reflect gate may surface the stale constant — acceptable.

**Gap 3 — INFO — `LspOverlay` (15th designed type) count phrasing inconsistency.**
Research/01 §2 lists "12 designed + 3 modeled" in one place and "15 designed types" / "14 designed types" in others (§2.3 mechanism guidance says 14 in-memory+config+modeled; §9 says "15 type items"). Step 1.5 says "all 14 designed types" then enumerates the input types including `LspOverlay`. The enumerated set in 1.5 matches research/01 §2's full list (4 input incl. LspOverlay + 6 intermediate + 4 output/modeled = 14, with the 6 scalar names inside `ContractScalars`). The "14 vs 15" is a counting-convention artifact in the research itself, faithfully carried into the task; the actual type SET enumerated is complete and correct.
- Recommendation: none required; the type enumeration is complete. Cosmetic count-label only.

**Gap 4 (bonus) — INFO — research/05's superseded per-case assertion detail is still referenced for case shapes.**
Steps 3.4/3.5 read research/05 §3 for per-case expected verdicts even though 05's materializer CONCLUSION is superseded by 09. This is CORRECT: only 05's *materializer location* conclusion is superseded; its *grader/case/C-6* mapping remains valid and authoritative (09 GAP1 explicitly reuses 05's grader assertions). The task header (line 113, related_docs) precisely scopes the supersession to the materializer only. No misrepresentation.
- Recommendation: none. Correct scoping of a partial supersession.

---

## Verdict

The task file is a faithful, near-complete realization of the research corpus. Every KEY finding called out in the lens (01's 6 units/types/run_sweep/invariant/formatter; 02's seam/merge-ordering/writer-convention; 03's token/guard/derivation/NO-EDIT halt; 04's BFS-depth1/inversions/safe_parse/never-import; 05+09's promote-not-rebuild + C-6; 06's demotion/PRESERVE/I6/no-bump/sync; 07's 3 test files + §15.4a + house idioms; 09's force-floor/diff-construction/OQ/NFR-003) maps to one or more concrete checklist items.

The two adversarial fabrication candidates the lens names are BOTH correctly resolved:
- The materializer is PROMOTE/ADAPT (research/09 authoritative), NOT build-from-scratch — Step 3.1 says "copy BOTH scripts, no behavioral rewrite."
- `run_sweep` args are NOT claimed to come from the config — Step 2.1 explicitly contradicts the TDD's "from the config" claim and constructs `diff`/`scope_worktree`/`availability_surface`.

Edge cases and phase-dependencies are fully reflected in verification criteria and ordering. The four gaps found are LOW/INFO alignment imperfections (under-specified reuse caveat, intentionally-deferred Q4, cosmetic type-count label, correctly-scoped partial supersession) — none is a dropped finding or a fabricated action.

**VERDICT: PASS**

Issues (none block; all LOW/INFO):
- LOW: Gap 1 — Step 1.8 could add the research/04 "symbol-level, not file-level audit graph" reuse caveat (mitigated by the global no-import constraint).
- INFO: Gap 2 — Q4 ensemble version reconciliation is intentionally deferred per research; no action required.
- INFO: Gap 3 — "14 vs 15 designed types" is a research-internal counting-label artifact; the enumerated type SET in Step 1.5 is complete.
- INFO: Gap 4 — research/05 is correctly used for case shapes (only its materializer conclusion is superseded by 09).
