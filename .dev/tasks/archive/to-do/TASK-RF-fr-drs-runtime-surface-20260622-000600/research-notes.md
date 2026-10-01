# Research Notes: Implement FR-DRS deterministic runtime-surface sweep module + product/eval/SKILL integration

**Date:** 2026-06-22
**Scenario:** A (Explicit — driving TDD spec provides full architecture, data models, API, rollout)
**Depth Tier:** Deep (greenfield HIGH-complexity module, complexity_score 0.82; 20+ files across 5 subsystems; 4-phase rollout)
**Track Count:** 1 (sequential 4-phase rollout — module → product wire → eval wire → prose demotion; phases build on each other, single cohesive deliverable)
**Spec (driving TDD):** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` (1549 lines, v1.2)
**Parent spec:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/spec.md`

---

## GOAL

Implement the FR-DRS deterministic runtime-surface sweep: a new pure-Python, LLM-free module
`src/superclaude/cli/reflect/runtime_surface.py` that runs a deterministic 7-step sweep
(tag → find-referrers → partition → degrade-oracle → rootwalk → reduce → emit), ALWAYS writes
`<output>/artifacts/runtime-surface-ledger.yaml`, and computes the six `runtime_surface_*` contract
scalars by construction — plus its three integration paths:
1. **Product path** — wire `run_sweep` into `runner._audit_once`, merge-overwrite the six fields +
   ledger into `return-contract.yaml` BEFORE `parse_contract`; consumer wiring in `contract.py`.
2. **Eval path** — route the same module into the grader so the 5 uc2 eval cases (ids 37–41) pass
   deterministically across ≥3 runs.
3. **SKILL.md demotion** — demote §6.1 step 4b/4b′ from LLM-emits-scalars to deterministic-sweep-computes
   (narrate verdict in REPORT.md only), with a conditional LLM-fallback for the bare `claude -p` path.

## WHY

A controlled 3×before/3×after experiment (2026-06-20) proved a prose-only LLM implementation CANNOT
deliver the structured-output guarantee: the ledger was written in only 1/9 quiet-path runs and the LLM
improvised scalar names (`runtime_surface_reachable`, `surface_reachability_verdict`,
`surface_production_reachable`) even AFTER the prose was strengthened to forbid them. The root cause is
structural (the LLM only engages the structured machinery on an alarming UNREACHED escalation). Moving
the structured-emission path into deterministic Python is the only fix. The verdict/prose SAFETY behavior
already works and MUST NOT be rebuilt — FR-DRS is scoped narrowly to the structured mirror.

---

## EXISTING_FILES

### Greenfield (does NOT exist — to be created)
- `src/superclaude/cli/reflect/runtime_surface.py` — **NEW MODULE.** grep-confirmed ZERO matches for
  `runtime_surface`/`RuntimeSurface`/`rootwalk`/`unreached_surfaces`/`ledger` across all 7 reflect files.
- `tests/cli/reflect/test_runtime_surface.py` — NEW (6-unit + count-invariant unit tests, §15.2).
- `tests/cli/reflect/test_runtime_surface_eval_determinism.py` — NEW (≥3-run zero-variance gate, §15.3).
- `tests/cli/reflect/test_runtime_surface_safety_regression.py` — NEW (AC-5 gate, §24.2; cases 37/39/40/41).

### Product-path integration seams [ALL CODE-VERIFIED 2026-06-22]
- `src/superclaude/cli/reflect/runner.py`
  - `_audit_once` def at **runner.py:394** (the tier-agnostic chokepoint; the invocation site, FR-005/D2).
  - `parse_contract(config.contract_path)` call at **runner.py:445** (the single read — EMIT must precede this).
  - `class _IndentDumper(yaml.SafeDumper)` at **runner.py:58** (MANDATORY YAML dumper, NFR-005).
  - `def _atomic_write_text` at **runner.py:70** (MANDATORY atomic writer, NFR-004).
  - Fix-loop re-audit calls `_audit_once()` at **runner.py:562** (SAME --base reused, NFR-002).
- `src/superclaude/cli/reflect/models.py`
  - `class Verdict(str, Enum)` at **models.py:26**; `def exit_code` at **models.py:39** (pass=0/halted=10/degraded=11/blocked=2 — UNCHANGED by FR-DRS).
  - `class ReflectConfig` at **models.py:58**; `def contract_path` property at **models.py:96** (= `<output>/return-contract.yaml`; ledger goes to sibling `<output>/artifacts/`).
- `src/superclaude/cli/reflect/ensemble.py`
  - `REFLECT_CONTRACT_VERSION = "1.0"` at **ensemble.py:59** (STALE vs SKILL 1.6.0 — Q4 reconcile; used at :500).
  - `def _emit_reflect_contract` at **ensemble.py:625**; bare `yaml.safe_dump` at **:633** + `path.write_text` at **:634** (the convention NOT to copy — use `_IndentDumper`+`_atomic_write_text` instead).
  - NOTE: ensemble.py is the git-`M` modified file; its line numbers drifted from the TDD's cited :508-509 → now :633-634. Researchers MUST re-verify current lines.
- `src/superclaude/cli/reflect/commands.py`
  - `def run` at **commands.py:164**; `ReflectRunner(config).run()` at **commands.py:254** (rejected as writer — runner clobbers any contract written here, §21 Alt 1).

### Consumer wiring seams (contract.py) [CODE-VERIFIED]
- `src/superclaude/cli/reflect/contract.py`
  - `_DEGRADED_COMPONENTS_HALT_SET = frozenset(...)` at **contract.py:31** (add `"runtime-surface:backend_unavailable"` token here per FR-010 / Phase-2 I7).
  - `_LOAD_BEARING_BOOL_FIELDS = frozenset(...)` at **contract.py:47** (count-invariant guard mirrors this fail-closed block).
  - `def derive_verdict` at **contract.py:130** (consumes the deterministic scalars).
  - `def _degraded_reason` at **contract.py:249**; `return "degraded-components"` at **:260** (REUSE existing slug — token-membership, NO new predicate).
  - `def _halted_reason` at **contract.py:307**; `return "regression"` at **:316/:325** (REUSE existing slug — UNREACHED populates `deviation_count_by_class.regression`, NOT a 5th deviation class, §14.3 I7).

### cli/audit REUSE sources (DATA-copy / adapt, NEVER import — §6.4 D1 Option C) [CODE-VERIFIED]
- `src/superclaude/cli/audit/reachability.py` — `def _bfs_reachable` at **:591** (rootwalk adapts this ~30-line BFS: enforce depth=1 at call site, DEGRADE-on-partial; the audit BFS is unbounded + dynamic→UNREACHABLE — both INVERTED).
- `src/superclaude/cli/audit/filetype_rules.py` — `_TEST_PREFIXES = ("test_", "spec_")` at **:106**, `_TEST_INFIXES = (".test.",".spec.","_test.","_spec.")` at **:107** (copy as DATA; INVERT default — audit UNKNOWN→SOURCE, runtime-surface unknown→DEGRADE).
- `src/superclaude/cli/audit/dynamic_imports.py` — `_DYNAMIC_PATTERNS` at **:24** (copy regex DATA for degrade-oracle cat d; audit maps dynamic→KEEP:monitor, runtime-surface→DEGRADE).

### SKILL / refs (Phase 4 demotion) [CODE-VERIFIED exist]
- `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` (8519 bytes) — the behavior SPEC to PORT (7-step algorithm, ledger row shape RS:L65-72, reduction precedence RS:L86-90, count invariant RS:L96).
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (203707 bytes) — §5.3 pre-filter (lines ~390-391/402/412 `surface_unreached` derivation), §6.1 4b/4b′ (demote), §9.1 (1.6.0 `runtime_surface_*` block ~671-672/721-736). Edits in `src/`, then `make sync-dev`.

### Eval path [CODE-VERIFIED exist]
- `.dev/eval-workspaces/sc-reflect/grader.py` — `check_yaml_list_len_eq` at **:191** (count-invariant re-check), `grade_eval` at **:437**, reads `eval_metadata.json` at **:440** (skip at :442), target-prefix bucketing `startswith("with_skill/")` at **:448** (C-6: new oracle assertions MUST carry a `target` key).
- `.dev/eval-workspaces/sc-reflect/cases/uc2-{unwired-surface-passes,surface-positive-control,surface-dynamic-dispatch,surface-degraded-backend,surface-test-only-ref}/` — 5 fixture dirs exist (ids 37–41).
- **C-5 UNVERIFIED:** the `evals.json` → per-eval `eval_metadata.json` materializer was NOT located in TDD research; MUST be located in Phase 1 (front-loaded, I5) — the eval-path hook likely lives there.

### Test infra [CODE-VERIFIED]
- `tests/cli/reflect/` — `conftest.py`, `fixtures/`, plus 14 existing test files (e.g. `test_fix_loop.py`, `test_verdict_mapping.py`, `test_writeback.py`, `test_runner_e2e.py`, `test_ensemble_unit.py`). New tests follow these patterns. UV-only (`uv run pytest`).

## PATTERNS_AND_CONVENTIONS

- **Copy-over-import precedent:** `runner.py:14-17` copies `_IndentDumper` locally rather than importing a private symbol — the precedent §6.4 D1 cites for the reflect-local BFS copy (Option C).
- **Reflect import ban** names `cli/sprint` + `cli/roadmap` ONLY (verified runner.py:8-9, config.py:7-10, models.py:8-12); importing `cli/audit` is mechanically legal but a coupling-quality liability → copy/adapt, never import.
- **Atomic + yamllint-safe writes:** `_atomic_write_text` (randomized temp + `os.replace` + finally-unlink, `mkdir(parents=True, exist_ok=True)`) + `_IndentDumper` (SafeDumper subclass, `indent-sequences:true`). Reference memory `reference_yamllint_indent_sequences_pyyaml`.
- **Fail-soft AST:** mirror `cli/audit/wiring_gate.py` `_safe_parse` (return-`None`-on-parse-error → symbol DEGRADE, never silent-skip).
- **Determinism levers:** ripgrep `rg --json --sort path` (single-thread, lexicographic); canonical `edge` formatter `f"{symbol} -> {target}"` (single ASCII space each side); dedupe on `(symbol,target)`; sort rows lexicographically before dump.
- **UV-only** (CLAUDE.md): `uv run pytest`, `uv run ruff format --check`. `make lint` runs `ruff check` only — CI separately runs `ruff format --check src/ tests/` (memory `reference_make_lint_vs_ci_ruff_format`).
- **Sync model:** edit `src/superclaude/` → `make sync-dev` → `.claude/`; `make verify-sync` before commit. NEVER stage `.claude/` (memory `feedback_claude_dir_gitignored`).

## GAPS_AND_QUESTIONS

- **C-5 materializer location** (UNVERIFIED) — where `evals.json` flattens to per-eval `eval_metadata.json` and copies `cases/uc2-*/expected.yaml`+`input/` into `iterations/`. Researcher 5 must locate it.
- **OQ-DRS.1/.2/.3 + Q4** — referrer engine floor (rg/AST vs LSP), bare-path coverage (Wave-1A shell-out), contract-version bump (recommend NO bump), stale ensemble version constant. TDD records recommendations (ratify at implementation), not blockers.
- **Exact current SKILL.md line numbers** for §5.3/§6.1/§9.1 — TDD cites lines but SKILL.md is large; Researcher 6 must re-anchor.
- **`run_sweep` arg construction** at `_audit_once` — exactly how diff/base_ref/scope_worktree/tasklist/availability_surface are read off `ReflectConfig`. Researcher 2 must trace the config fields.

## RECOMMENDED_OUTPUTS

8 research files in `${TASK_DIR}research/`:
- `01-module-design-and-spec-port.md`
- `02-product-path-integration-seam.md`
- `03-consumer-wiring-contract-and-prefilter.md`
- `04-audit-reuse-sources-and-adaptation.md`
- `05-eval-path-grader-cases-materializer.md`
- `06-skill-prose-demotion-and-refs.md`
- `07-test-patterns-and-verification.md`
- `08-mdtm-template-and-examples.md`

## SUGGESTED_PHASES (researcher assignments — all spawned in ONE message, parallel)

- **R1 — File Inventory + Spec-port (module design).** Scope: `refs/runtime-surface.md` (full 7-step algorithm, ledger row shape, reduction precedence, count invariant), TDD §6.1/§7/§8.1/§8.1.1/§8.1.2/§12. Output: the 6 logical units, all DESIGNED types (`DiffHunk`, `SurfaceAllowlist`, `TaggedSurface`, `LspOverlay`, `ReferrerEdge`, `TestCommentTable`, `PartitionedReferrers`, `EntrypointRoot`, `RootwalkResult`, `DegradeVerdict`, `ContractScalars`, `SweepResult`, `RuntimeSurfaceLedgerRow`, `UnreachedSurface`), `run_sweep` signature, degrade-oracle cats a–d, reduction precedence, count invariant. → `research/01-module-design-and-spec-port.md`
- **R2 — Product-path integration seam.** Scope: `runner.py` (`_audit_once` 394-460, `_IndentDumper` 58, `_atomic_write_text` 70, `parse_contract` 445, fix-loop 562), `models.py` (`ReflectConfig` fields, `contract_path` 96), `ensemble.py` (current line numbers, version constant 59, emit 625). Trace exactly how `run_sweep` args are built from config; the merge-overwrite-before-parse ordering invariant; Tier-1 vs Tier-2 author paths. → `research/02-product-path-integration-seam.md`
- **R3 — Consumer wiring (contract.py + §5.3 pre-filter).** Scope: `contract.py` (`derive_verdict` 130, `_degraded_reason` 249/260, `_halted_reason` 307/316/325, `_DEGRADED_COMPONENTS_HALT_SET` 31, `_LOAD_BEARING_BOOL_FIELDS` 47, `_deviation_count` 91), SKILL.md §5.3 (`surface_unreached` derivation 390-391/402/412). Document EXACT additions: token-membership reuse for degraded, regression-counter population for UNREACHED (NO new slugs), count-invariant malformed-contract guard, the integer→`surface_unreached` derivation transform + owner. → `research/03-consumer-wiring-contract-and-prefilter.md`
- **R4 — cli/audit reuse sources + adaptation.** Scope: `reachability.py:_bfs_reachable` 591-624 (full body — what to copy, depth=1 + DEGRADE-on-partial inversions), `filetype_rules.py` _TEST_* 106-107, `dynamic_imports.py` _DYNAMIC_PATTERNS 24-39, `wiring_gate.py` `_safe_parse`. Document the reflect-local copy plan (Option C) per §6.4 D1 / Reuse Audit; the semantic inversions. → `research/04-audit-reuse-sources-and-adaptation.md`
- **R5 — Eval path (grader + cases + materializer).** Scope: `.dev/eval-workspaces/sc-reflect/grader.py` (full — `check_yaml_list_len_eq` 191, `grade_eval` 437-449 bucketing, `eval_metadata.json` read 440), the 5 `cases/uc2-*/` dirs (input/diff.patch, input/tasklist.md, expected.yaml shapes), `evals.json` ids 37–41. **LOCATE the C-5 materializer.** Document the eval-wire hook + the C-6 `target`-key constraint. → `research/05-eval-path-grader-cases-materializer.md`
- **R6 — SKILL prose demotion + refs (Doc Cross-Validator).** Scope: SKILL.md §6.1 4b/4b′ (exact lines + PRESERVE safety sentences incl. "never emits a clean PASS…" SKILL:489), §9.1 1.6.0 block, the `runtime_surface_sweep_ran` detection signal (I6) for the conditional fallback, sync model. Re-anchor ALL cited line numbers to current SKILL.md. Tag claims [CODE-VERIFIED]/[CODE-CONTRADICTED]/[UNVERIFIED]. → `research/06-skill-prose-demotion-and-refs.md`
- **R7 — Test patterns & verification (Test & Verification).** Scope: `tests/cli/reflect/conftest.py`, `fixtures/`, existing patterns in `test_fix_loop.py`/`test_verdict_mapping.py`/`test_writeback.py`/`test_runner_e2e.py`. Map: how to structure the 3 new test files (unit, eval-determinism, safety-regression), the §15.4a `surface_unreached` derivation test, fixtures conventions, UV commands. → `research/07-test-patterns-and-verification.md`
- **R8 — MDTM template + examples (Template & Examples).** Scope: `.claude/templates/workflow/02_mdtm_template_complex_task.md` PART 1 (A3 granularity, B2 self-containment, L1-L6); recent `TASK-RF-reflect-*` examples in `.dev/tasks/to-do/`. Document required sections, item format, QA-gate encoding patterns. → `research/08-mdtm-template-and-examples.md`

Each researcher told the others' scopes (no overlap). R1 owns module/spec; R2 product seam; R3 consumer; R4 audit reuse; R5 eval; R6 SKILL; R7 tests; R8 template.

## TEMPLATE_NOTES

- **MDTM Template:** 02 (Complex) — greenfield discovery + multi-phase build (module → product wire → eval wire → prose demotion) + per-phase QA gates + conditional flows (C-5 materializer locate).
- **Tier:** Deep (8 researchers; complexity_score 0.82, HIGH).
- **QA_GATE_REQUIREMENTS:** PER_PHASE (Template 02, 4 build phases each gated).
- **TESTING_REQUIREMENTS:** UNIT + INTEGRATION (unit per-6-units + count invariant; integration = 5 uc2 eval cases ≥3-run determinism; safety-regression gate).
- **VALIDATION_REQUIREMENTS:** `make verify-sync` clean; `uv run ruff format --check` clean for the new module; UV-only; `uv run pytest tests/cli/reflect/` green.
- **POST_REFLECT_GATE:** ENABLED (flat wrapper shell-out, penultimate final-phase item).
- **spec_path:** `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md` → frontmatter + A.10.7 PRE gate `--spec`.
- The generated tasklist must map the TDD's 4 phases (§23.2) to its build phases and carry per-FR granular items (FR-001..FR-013, NFR-001..007) and per-unit items (6 logical units).

## AMBIGUITIES_FOR_USER

None — intent is clear from the TDD and codebase context. The TDD explicitly resolves the open questions
with recommended floors (OQ-DRS.1 = rg/AST floor + optional LSP overlay; OQ-DRS.2 = `_audit_once` +
Wave-1A shell-out for bare path; OQ-DRS.3 = no version bump; Q4 = reconcile ensemble constant when it
emits the six fields). The TDD states "No user decision is required to PROCEED." These are recorded as
ratify-at-implementation Open Questions in the generated tasklist, not blockers. The deferred FR-006a
(sprint-executor read) is explicitly out of v1 scope.

**Status:** Complete
