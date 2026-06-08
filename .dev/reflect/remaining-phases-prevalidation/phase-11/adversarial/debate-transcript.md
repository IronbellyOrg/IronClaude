# Phase 11 (R1.6 Cleanup) — Adversarial Pre-Execution Validation Transcript

<!-- Provenance: produced by sc-adversarial-protocol Mode B (inline), corrected-framing as source -->
<!-- Source artifacts: BUILD-REQUEST §R1.6; task objective 10 (L99); CORRECTED framing L1044 + .dev/reflect/r1-3-uc2-validation/{merged-recommendation.md, option-b-rf-qa.md} -->
<!-- Date: 2026-06-02 | Depth: standard | Convergence: 0.88 -->

## Method

Each Phase 11 item steelmanned across three advocate stances — **KEEP** (item is correct as written),
**REFACTOR** (item is salvageable but mis-scoped/mis-cited), **DISCARD** (item is wrong and should be
removed) — then scored against four authorities:

- **A1** BUILD-REQUEST §R1.6 (L174): "Delete duplicate frontmatter parsers, `return True` stubs, fail-open defaults."
- **A2** Task objective 10 (L99) — concrete deletion targets (carries some STALE framing).
- **A3** CORRECTED framing (task L1044 + `r1-3-uc2-validation/merged-recommendation.md` L53-69, `option-b-rf-qa.md`).
- **A4** Verified source code (read this session — line/field citations below).

## Ground-truth code facts established (A4)

| Fact | Evidence |
|---|---|
| `gate_passed` envelope-None shim returns `(True, None)` and skips `code_assertions` when `envelope is None or repo_root is None` | `cli/pipeline/gates.py:93-98` |
| Shim docstring/comment says "**R1.6 cleanup deletes this skip-path**…/…**R1.6 deletes this branch when all call sites are migrated**" — the WRONG framing, embedded in code | `cli/pipeline/gates.py:39, 97` |
| `assert_step_reachable` AST-parses `repo_root/"src"/"superclaude"/…/executor.py`, fail-closed on missing file → inherently **CI-only / source-tree** | `cli/roadmap/code_assertions.py:77-92` |
| `assert_envelope_artifacts_present` checks the run's own artifacts → **runtime-safe** | `cli/roadmap/code_assertions.py:126-184` |
| `fidelity_checker` fail-opens are GENUINE: `found=True, # fail-open` (no-names branch) + partial-match `found=True` | `cli/roadmap/fidelity_checker.py:302, 320` |
| `_cross_refs_resolve` ALWAYS returns True (incl. on unresolved refs), comment "return True to avoid blocking pipeline" → GENUINE Contract #5 stub | `cli/roadmap/gates.py:58-101` (returns True at 98 & 101) |
| `gate=None` convergence bypass is at **executor.py:2579**, NOT 2167 (task line drift) | `cli/roadmap/executor.py:2579` |
| A second, **legitimate** `gate=None` exists in `sprint/executor.py:85` (non-convergence Step) | `cli/sprint/executor.py:85` |
| `PipelineEnvelope` has fields `counts/findings/spec_ids/artifacts` — there is **NO `frontmatter` field** | `cli/roadmap/envelope.py:128-175` + grep `.frontmatter` = 0 hits |
| `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` does not yet exist | grep = 0 hits in `cli/roadmap/` |

## Round 1 — Per-item advocate positions

### Step 11.1 — Discover cleanup inventory
- **KEEP advocate:** Read-only discovery with explicit `Classification (FRAGILITY / EARLY-EXIT / VALID-HEURISTIC)` column — this is the *mechanism* that prevents blind deletion of valid heuristics. Sourced from research files. Targets enumerated match A2/A4. It does NOT list the `cli/pipeline/gates.py` envelope-None shim as a deletion target — which is *correct*, the shim must not be deleted.
- **DISCARD advocate:** Weak — the inventory is the safety net for the whole phase; removing it makes 11.3/11.4 unguarded.
- **REFACTOR advocate (wins):** The inventory enumerates A2's targets but is **silent on the CORRECTED R1.6 scope** (A3 L1044): the CI-only-vs-runtime `code_assertion` split, the shim-preservation, and the shim's wrong-framing comment. An inventory that omits the single highest-priority CORRECTED item under-scopes the phase. Also the `spec_id_registry.json` deletion TODO (`envelope.py:148-150`) is a real R1.6 target it should capture.
- **Convergence:** 0.85 → REFACTOR.

### Step 11.2 — Delete dual frontmatter parsers
- **KEEP advocate:** Already remediated (C1 fix) to canonicalize on the envelope post-step extractor and delete BOTH `gates.py:_parse_frontmatter` AND `_check_frontmatter` — correctly **overriding** the stale A2/L99 directive ("canonicalize on `_check_frontmatter`"), which would preserve the Flaw 3 substrate. Direction is right per §MVR §1.
- **DISCARD advocate:** Weak — frontmatter de-duplication is a real BUILD-REQUEST §R1.6 (A1) requirement.
- **REFACTOR advocate (wins):** The item's central instruction — "migrate EVERY consumer to read from `envelope.frontmatter` (the typed field on PipelineEnvelope)" — references a field that **does not exist** (`envelope.py:128-175`; the typed fields are `counts/findings/spec_ids/artifacts`). The *direction* (single owner = envelope module) is correct; the *named mechanism* is a phantom field. Also note the latent stale-authority conflict: A2/L99 still says canonicalize on `_check_frontmatter` — that objective text is now wrong and 11.2 silently contradicts it.
- **Convergence:** 0.80 → REFACTOR (mechanism), with the framing-direction KEPT.

### Step 11.3 — Delete `_cross_refs_resolve` + audit return-True stubs
- **KEEP advocate (wins):** (a) `_cross_refs_resolve` is a VERIFIED genuine stub (always True, comment admits "to avoid blocking pipeline") — deleting it + its `MERGE_GATE` registration is exactly Contract #5. (b)-(d) per-site classify obligation_scanner / remediate_executor / fingerprint / spec_parser and **honor VALID-HEURISTIC** — the precise distinction A3 demands. (e) grep gate. **Crucially, 11.3 does NOT touch the `gate_passed` envelope-None shim** — it does not conflate the legitimate CI-only-assertion skip with a fail-open stub. This is the item the framing-warning targeted, and it is clean.
- **REFACTOR advocate:** Minor — could add an explicit "DO NOT touch `cli/pipeline/gates.py:93-98` shim" guard rail, but the item already scopes deletions to named stub sites, so the risk is low.
- **Convergence:** 0.90 → KEEP.

### Step 11.4 — Delete fail-open defaults + `gate=None` bypass
- **KEEP advocate:** Deletes the VERIFIED genuine fidelity fail-opens (`fidelity_checker.py:302, 320`) → fail-closed `ambiguous=True`; deletes the convergence `gate=None` bypass → new convergence-aware gate. Does NOT touch the shim. Correct.
- **REFACTOR advocate (wins):** Two corrections needed: (1) line drift — the bypass is at **executor.py:2579**, the item says 2167. (2) The fail-closed replacement and the new `SPEC_FIDELITY_GATE_CONVERGENCE_AWARE` are sound but the item should reference the Phase-10 sequencing prerequisite (L603) explicitly, since the L302 deletion is the gate for Phase 10. Critically, this item is **also** the natural home for the CORRECTED shim work (replace the shim's wrong-framing comment + add the CI-vs-runtime classification) — currently nowhere in Phase 11 owns that.
- **Convergence:** 0.84 → REFACTOR (line fix + absorb shim-comment correction).

### Step 11.5 — `test_no_fragility_stubs.py` + `test_gate_empty_target.py`
- **KEEP advocate:** `test_no_fragility_stubs` (Contract #5 regex over `cli/`) is sound and — importantly — the shim's comment ("Backward-compat shim… R1.6 deletes this branch") contains none of `fragile|too hard|for now`, so the lint correctly will NOT flag the legitimate shim. The mutation check (temporarily restore `_cross_refs_resolve`) is good Contract #1 hygiene.
- **REFACTOR advocate (wins):** `test_gate_empty_target` iterates `ALL_GATES`, builds empty fixtures, calls `gate_passed`, asserts NOT PASS. It is **shim-blind**: a STRICT gate whose only enforcement is `code_assertions` (e.g. CERTIFY_GATE, the R1.5 VERIFY_IMPLEMENTATION_GATE), when called via `gate_passed(file, GATE)` with **no envelope/repo_root**, hits the shim and returns `(True, None)` = PASS. With empty content the tier checks (`L49/L54`) catch it first, but with non-empty-but-wrong-target content the code_assertion gate would PASS through the shim and the test would either spuriously fail a correct gate or mask the shim. The test must be shim-aware: provide `envelope`+`repo_root` for code_assertion gates, OR explicitly scope the empty-target assertion to the file/min-lines/semantic tiers and document that code_assertions are exercised by their dedicated tests (e.g. `test_dispatch_reachability.py`).
- **Convergence:** 0.82 → REFACTOR (`test_gate_empty_target` shim-awareness); `test_no_fragility_stubs` KEEP.

### Step 11.6 — `test_retry_contract.py` (Contract #7)
- **KEEP advocate (wins):** Retry-mutates-input invariant per master:§Flaw 4 / Contract #7; independent of the shim/envelope framing. Sound.
- **REFACTOR advocate:** Minor cross-phase note — 11.6 seeds `retry_loop_no_terminal_case.*` while 11.2 references `disagreeing_parsers_case.md` as "Phase 13 creates this"; ensure fixture-creation ownership is consistent so neither test imports a not-yet-created fixture. Not a Phase-11 blocker.
- **Convergence:** 0.88 → KEEP.

### Step 11.7 — Full R1.6 validation
- **KEEP advocate:** Lint/format/sync/tests/arch-lint aggregation is standard and necessary.
- **REFACTOR advocate (wins):** The assertion "**full-codebase grep for `gate=None` (must be 0)**" is WRONG: a legitimate `gate=None` exists at `sprint/executor.py:85` (a non-convergence Step), and `Step.gate` may legitimately be unset for LIGHT/EXEMPT steps. The check must be scoped to the **convergence-bypass pattern in roadmap `_build_steps`** (`gate=None if config.convergence_enabled`), not whole-codebase `gate=None`. The `return True` fragility grep is fine (annotated-fragile pattern, won't hit the shim).
- **Convergence:** 0.83 → REFACTOR (scope the gate=None grep).

### Step PG11.1 — Aggregate + spawn rf-qa-qualitative
- **DISCARD advocate:** None — the QA gate is needed.
- **REFACTOR advocate (wins):** The QA checklist carries the **WRONG framing in two places**: (d) "exactly ONE canonical frontmatter parser exported from **`superclaude.contracts.parsers`**" directly CONTRADICTS Step 11.2's remediated statement that "**there is no `superclaude.contracts.parsers` submodule, the parser is owned by the envelope module**" — a THIRD, stale framing that would make rf-qa fail a correct implementation or demand a forbidden submodule; (e) "all 26 `gates.py` consumer sites migrated to canonical parser" inherits the same stale parser model. SEPARATELY, the checklist contains **no check for the CORRECTED R1.6 scope** (A3): it never verifies the CI-only-vs-runtime `code_assertion` split, never verifies the shim was *preserved & reclassified* (vs blanket-deleted). So QA would neither catch a wrong shim deletion nor confirm the corrected work.
- **Convergence:** 0.86 → REFACTOR (fix (d)/(e) to envelope model; add CORRECTED-scope checks).

### Step PG11.2 — Act on R1.6 QA verdict
- **KEEP advocate (wins):** Standard halt-precedence act-on-verdict loop; edits scoped to `src/superclaude/`. Sound. Inherits PG11.1's checklist — once PG11.1 is refactored, PG11.2 is correct.
- **Convergence:** 0.90 → KEEP (conditional on PG11.1 refactor).

## Round 2.5 — Invariant probe (sufficiency / framing-conflation)

| ID | Category | Assumption probed | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | guard_conditions | "Some Phase 11 step mandates deleting the `gate_passed` envelope-None shim as a fail-open bug." | **ADDRESSED (negative)** | HIGH | Traced all deletion targets in 11.3/11.4/11.7. NONE name `cli/pipeline/gates.py:93-98`. The wrong framing did NOT reach an executable deletion step — it survives as an OMISSION (missing CI-vs-runtime split) + an in-code comment (`gates.py:39,97`) + the `contracts.parsers` QA criterion. |
| INV-002 | sufficiency_challenge | "Does Phase 11, as written, implement the CORRECTED R1.6 scope (split code_assertions; replace shim with per-assertion classification)?" | **UNADDRESSED** | HIGH | No step in 11.1–11.7 references the split or the shim reclassification. A3/L1044 names this the High-priority CORRECTED deliverable. Phase 11 would close without doing it. |
| INV-003 | state_variables | "`envelope.frontmatter` exists as the migration target for 11.2." | **UNADDRESSED** | HIGH | `envelope.py:128-175` has no `frontmatter` field; grep `.frontmatter` = 0. 11.2's consumer-migration mechanism targets a phantom field. |
| INV-004 | count_divergence | "11.7's `gate=None` grep is satisfiable (can reach 0)." | **UNADDRESSED** | MEDIUM | `sprint/executor.py:85` legitimately uses `gate=None`; whole-codebase grep can never be 0. Assertion is unsatisfiable as written. |
| INV-005 | interaction_effects | "PG11.1 QA criteria are consistent with the steps they verify." | **UNADDRESSED** | HIGH | PG11.1(d) `contracts.parsers` vs 11.2 `envelope`-owned parser — QA would reject a correct impl. |

**Convergence GATE:** 4 HIGH UNADDRESSED invariants (INV-002, INV-003, INV-005) → phase-level convergence BLOCKED at 0.88 until the REFACTORs below are applied. INV-001 is the reassuring finding: no blanket-shim-deletion landed in an executable step.
