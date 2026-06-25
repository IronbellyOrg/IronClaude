# Research Notes: sc:reflect Deterministic Runtime-Surface Sweep (FR-DRS)

**Date:** 2026-06-21
**Scenario:** A (explicit request — feature spec with named source files, integration points, and an approach section)
**Tier:** Heavyweight
**Status:** Complete

**Driving spec (PRD-equivalent source of requirements):**
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/spec.md`
(feature_id FR-DRS, new_feature, complexity_class HIGH, parent_feature sc-reflect-protocol, supersedes_concern FR-RSR structured-output reliability)

**Final TDD output (MANDATORY destination):**
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`
(sibling to spec.md — matches the established issue-2-headless-ensemble pattern where the FR-RH2 TDD landed at `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`, NOT `docs/`. This is a worktree; all paths resolve to the worktree absolute root. No existing stub at the destination — only spec.md is present.)

**Template schema:** `src/superclaude/examples/tdd_template.md` (v1.2, 28 sections). This is a
**backend/library + CLI-integration** component → frontend-only sections **§9 State Management, §10
Component Inventory, §16 Accessibility are N/A with rationale**. §8 (API Specifications) is repurposed
as the **module/function API** of the sweep + the contract-field surface (not HTTP). §13 Security and
§17/§26 are light (local-only file writes under `<output>/`, no network, no prod service). All other
sections completed (Heavyweight).

---

## EXISTING_FILES

### New file to be designed (does not exist yet)
- `src/superclaude/cli/reflect/runtime_surface.py` — the proposed pure-Python, LLM-free sweep module. ~6 logical units (tagger, referrer-finder, partitioner, degrade-oracle, rootwalk, ledger+scalar reducer).

### Behavior source-of-truth to PORT to code (READ in full — this is the algorithm)
- `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md` (101 lines). Five sections:
  §1 surface allowlist (py/ts/js/rust/go + "other→DEGRADE"); §2 language table (path/test markers,
  inline-test markers, comment syntax); §3 degrade oracle (4 categories a–d); §4 entrypoint-rootwalk
  (depth=1); §5 `runtime-surface-ledger.yaml` schema + `RuntimeSurfaceLedgerRow` TypedDict + per-symbol
  reduction precedence (`DEGRADE-on-any-incompleteness > UNREACHED > REACHED`) + count invariant
  `len(unreached_surfaces) == runtime_surface_unreached`.

### Product-path integration surfaces (reflect CLI — `src/superclaude/cli/reflect/`)
- `commands.py` (13.4 KB) — `reflect_group` + `run` Click command; the wrapper that runs the skill in a
  subprocess and parses `return-contract.yaml`. Echoes `contract:` path (line ~266). **Candidate sweep
  invocation site (OQ-DRS.2)** — post-skill, pre-consumer.
- `runner.py` (26.9 KB) — `ReflectRunner` (`_audit_once`, `run`, `_apply_remediation`), `write_reflect_post`,
  `write_sidecar`, `_atomic_write_text`, `IndentDumper` (yamllint-safe YAML; see
  mem:reference_yamllint_indent_sequences_pyyaml). **Alternative sweep invocation site** — the runner owns
  contract creation; writing the 6 fields here would also cover the `superclaude reflect run` path.
- `contract.py` (14 KB) — `parse_contract(path)`, `derive_verdict`, `_extract_deviations`,
  `_degraded_reason`, `_halted_reason`, `classify_fix`. **The primary CONSUMER of the contract dict** — must
  read deterministically-written `runtime_surface_*` fields, not LLM-typed ones.
- `models.py` (4.3 KB) — `Verdict` enum, `ReflectConfig` (incl. `contract_path` = `output_dir/return-contract.yaml`). Types only.
- `config.py`, `ensemble.py` (`_emit_reflect_contract` YAML writer at line ~500), `__init__.py`.

### Consumer surfaces (downstream of the contract)
- SKILL.md `src/superclaude/skills/sc-reflect-protocol/SKILL.md` (~1800+ lines):
  - §6.1 steps **4b′ (tagger, line 465/487)** and **4b (sweep, line 466/489)** — the LLM prose to DEMOTE.
  - §6.1 step ~491 — "Contract emission is mandatory and name-exact (FR-RSR.7)" prose forbidding ad-hoc names.
  - §5.3 **pre-filter precedence paragraph (line 402)** — `surface_unreached` is a TABLE-WIDE forbid-STOP
    pre-filter; forces Tier 2 when `runtime_surface_unreached ≥ 1` from a successful sweep.
  - §9.1 **contract block (lines 672–735)** — `contract_version: "1.6.0"`; the 6 `runtime_surface_*` fields
    with canonical names + the MANDATORY EMISSION comment (lines 721–735).
  - §9.3 **consumer map (line 890)** — runtime_surface fields are "NON-GATING advisory" for UC-2 consumers.
  - §10.7-ish (lines 1057–1065) — UNREACHED maps onto the existing 4 deviation classes by evidence; no 5th class.
- `src/superclaude/cli/sprint/executor.py` (the `sprint run` executor) — imports `TurnLedger` (line 42);
  budget-aware gate enforcement. Acceptance criterion: "the sprint run executor reads the deterministic scalars."
  (Models in `cli/sprint/models.py`; `TurnLedger` is the budget/rollback primitive.)

### Eval-path integration surfaces (`.dev/eval-workspaces/sc-reflect/`)
- `grader.py` (487+ lines) — `check_assertion` dispatcher + 18 assertion checkers. **`check_yaml_list_len_eq`
  (line 191)** is the FR-RSR count-invariant checker (`len(unreached_surfaces) == runtime_surface_unreached`).
  Currently grades LLM-emitted scalars. FR-DRS: the harness/grader invokes the SAME module so the eval is
  deterministic. (modified in working tree)
- `grader-extensions.md` `src/.../refs/grader-extensions.md` — authoritative spec for the 11 new assertion
  types incl. `yaml_list_len_eq`. (modified)
- `evals/evals.json` — eval registry. The 5 FR-RSR UC-2 cases live under `cases/uc2-*/` (case_dir entries),
  NOT `evals/uc2-*/`. (modified)
- `cases/uc2-*` (5 new dirs, untracked): `uc2-unwired-surface-passes`, `uc2-surface-positive-control`,
  `uc2-surface-dynamic-dispatch`, `uc2-surface-test-only-ref`, `uc2-surface-degraded-backend`. These are the
  acceptance-criterion eval cases (ids 37–41 region).
- Driving evidence: `TASK-RF-uc2-reachability-20260620-025931/phase-outputs/reports/before-after-comparison.md`
  (the 3×before/3×after experiment proving prose-only can't deliver the structured guarantee).

### Strongest reuse prior art (cli/audit/ — see REUSE_AUDIT below)
- `src/superclaude/cli/audit/reachability.py` — `ReachabilityAnalyzer`, `_bfs_reachable` (rootwalk prior art).
- `src/superclaude/cli/audit/dependency_graph.py` — 3-tier static+grep fail-open evidence.
- `src/superclaude/cli/audit/dynamic_imports.py` — dynamic-import pattern scanner.
- `src/superclaude/cli/audit/filetype_rules.py` — test-marker / file-type table.
- `src/superclaude/cli/audit/wiring_gate.py` (`_safe_parse`), `dead_code.py` (entrypoint exclusions).

## PATTERNS_AND_CONVENTIONS
- **UV-only** for all Python ops (CLAUDE.md). `make verify-sync` clean; `ruff format --check` clean (and
  `make lint` ≠ CI ruff format — run `uv run ruff format --check src/ tests/`, scoped to changed files;
  see mem:reference_make_lint_vs_ci_ruff_format + mem:reference_ruff_version_mismatch_worktree).
- **Source-of-truth discipline**: edit `src/superclaude/` then `make sync-dev`; NEVER stage `.claude/` mirrors.
- **YAML emission**: reflect uses an `IndentDumper(yaml.SafeDumper)` overriding `increase_indent` for
  yamllint-safe sequences (runner.py:66) — the new ledger writer must follow this to pass pre-commit.
- **Atomic writes**: `_atomic_write_text` (runner.py:70) — ledger + contract overwrite should be atomic.
- **Reflect import boundary**: reflect modules ban imports from `cli/sprint` and `cli/roadmap` (docstrings),
  NOT `cli/audit`. Decoupling via callable interfaces is the established pattern (sprint executor avoids
  TurnLedger import via callable remediation, executor.py:536).
- **Determinism posture (asymmetric cost)**: fail-loud — never silently PASS an untested surface; never
  silently Regression an idiomatic dynamic/registry/decorator/reflection/packaging entrypoint. Every
  uncertainty → DEGRADE → §10.6 Grounding Gap.
- **Contract additive-only versioning**: 1.5.0/1.6.0 were ADDITIVE; FR-DRS changes the PRODUCER not the field
  set (OQ-DRS.3 → likely no version bump).

## PRD_CONTEXT
The spec.md IS the requirements source (PRD-equivalent). Extracted:
- **Goal:** produce `runtime-surface-ledger.yaml` + the 6 `runtime_surface_*` scalars deterministically on
  every UC-2 run, independent of LLM reflection depth/"alarm level." Remove the LLM from the structured-emission
  path; keep it only for narration/verdict in REPORT.md.
- **Evidence (§0):** 3×before/3×after eval proved prose-only emits ad-hoc field names
  (`runtime_surface_reachable`, `surface_reachability_verdict`, `surface_production_reachable`) on quiet paths
  even after the SKILL prose was strengthened to forbid exactly those names. Ledger written in only 1/9
  quiet-path runs. Root cause: LLM engages the structured machinery only on an alarming UNREACHED that escalates.
- **What already works (DO NOT REBUILD):** the SAFETY behavior — across every run the skill caught the
  unwired/registry/test-only surface and never clean-passed it (FR-S9-04 blind spot closed at verdict/prose
  level). FR-DRS is ONLY about making the structured contract MIRROR reliable.
- **Approach (§2):** standalone pure-Python module; inputs = diff/patch + scope/work-tree + tasklist;
  7-step algorithm (tag→find-referrers→partition→degrade-oracle→rootwalk→reduce→emit) mirroring
  runtime-surface.md. Integration: product path (commands.py/runner.py writes the 6 fields + ledger BEFORE
  the contract is parsed by consumers); eval path (grader invokes the same module); SKILL.md demotes §6.1
  4b/4b′ prose to "deterministic sweep computes these; narrate verdict in REPORT.md."
- **Acceptance criteria (§4, 6 items):** (1) ledger + 6 canonical scalars on every UC-2 run, REACHED/DEGRADE/
  UNREACHED alike, zero LLM dependence; (2) the 5 FR-RSR cases (ids 37–41) pass deterministically across ≥3
  repeated runs with no variance; (3) `len(unreached_surfaces)==runtime_surface_unreached` by construction;
  (4) §5.3 forbid-STOP pre-filter + sprint run executor read deterministic scalars; (5) FR-RSR safety
  preserved (never clean-pass an unwired surface); (6) `make verify-sync` clean, UV-only, `ruff format --check` clean.
- **Out of scope (§5):** re-litigating REACHED-vs-DEGRADE policy for `[project.scripts]` (keep oracle as-is);
  headline fail-pre fixture rewrite (carried as a sibling fixture task); any change to the LLM narration/verdict
  role in REPORT.md.

## SOLUTION_RESEARCH
The spec proposes ONE approach (deterministic Python module). Genuine architectural alternatives the TDD §21
should evaluate (the TDD must not reverse-justify):
- **Alt 0 (mandatory): Do Nothing** — keep strengthening SKILL prose. Refuted by §0 evidence (prose-only
  cannot deliver structured guarantee even after strengthening).
- **Alt 1: invocation site** — post-skill in `commands.py` (covers only `superclaude reflect run`) vs in
  `runner.py` `_audit_once` (also covers runner-driven paths) vs a Wave-1A tool the skill shells out to
  (covers bare `claude -p /sc:reflect` too). This is **OQ-DRS.2**, a real open decision for §6.4 + §22.
- **Alt 2: referrer engine** — pure ripgrep/AST floor vs programmatic Serena/LSP precision upgrade
  (**OQ-DRS.1**). Determinism + no-MCP fallback argue ripgrep/AST as the floor, LSP optional.
- **Alt 3: reuse reachability.py** — import/adapt `cli/audit/reachability.py` BFS vs reflect-local
  reimplementation vs extract a boundary-neutral shared helper (reuse-audit reuse-by-import verdict, but
  domain semantics differ: depth=1 + DEGRADE-on-partial).

## RECOMMENDED_OUTPUTS
- Research files (Phase 2): `research/01-runtime-surface-algorithm.md`, `02-product-path-integration.md`,
  `03-consumer-surfaces.md`, `04-eval-path-integration.md`, `05-reuse-and-boundaries.md`,
  `06-skill-prose-demotion.md`. (`00-prd-extraction.md` from spec.md.) `research/reuse-audit.yaml` already written.
- Web research (Phase 4, light): Python `ast` decorator/symbol-kind resolution patterns; ripgrep JSON output
  for deterministic referrer scanning; (optional) Serena/LSP `find_referencing_symbols` programmatic contract.
- Synthesis files (Phase 5): one per major template section group (architecture, data model/ledger schema,
  module API, integration/flows, error/degrade handling, testing, alternatives/open-questions, migration/rollout).
- Final TDD: `.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`.

## SUGGESTED_PHASES
Heavyweight: 6 codebase research agents + 1 PRD extraction + ~2 web agents.

| # | Type | Topic | Investigate | Output | Synth section(s) |
|---|------|-------|-------------|--------|------------------|
| 00 | PRD Extraction | FR-DRS requirements | spec.md (full) | research/00-prd-extraction.md | §2,§3,§4,§5 |
| 01 | Code Tracer / Architecture Analyst | runtime-surface algorithm to port | refs/runtime-surface.md (all 5 §); SKILL §6.1 4b/4b′ | research/01-runtime-surface-algorithm.md | §6 arch, §7 ledger data model |
| 02 | Integration Mapper | product-path integration | commands.py, runner.py, contract.py, models.py, ensemble.py | research/02-product-path-integration.md | §6 arch, §8 module API, §11 flows, §19 rollout |
| 03 | Integration Mapper | consumer surfaces | SKILL §5.3 (line 402), §9.1 (672–735), §9.3 (890), §10.7; sprint/executor.py TurnLedger | research/03-consumer-surfaces.md | §5 requirements, §8 contract fields, §11 flows |
| 04 | Code Tracer | eval-path integration | grader.py (`check_yaml_list_len_eq`+dispatcher), grader-extensions.md, evals.json, cases/uc2-* | research/04-eval-path-integration.md | §15 testing, §4 metrics |
| 05 | Reuse Scout (records reuse-audit.yaml) | reuse + import boundaries | cli/audit/{reachability,dependency_graph,dynamic_imports,filetype_rules,wiring_gate,dead_code}.py; reflect import-ban docstrings | research/05-reuse-and-boundaries.md | §6.4 decisions, §18 deps, §21 alternatives |
| 06 | Doc Analyst | SKILL prose demotion scope | SKILL §6.1 4b/4b′/491, §9.1 emission comment | research/06-skill-prose-demotion.md | §6 arch, §19 migration, §3 non-goals |
| W1 | Web | Python AST decorator/symbol-kind + ripgrep JSON referrer | — | research/web-01-ast-ripgrep.md | §6, §8, §12 |
| W2 | Web (optional) | Serena/LSP find_referencing_symbols programmatic | — | research/web-02-lsp-referrers.md | §6.4, §21 |

## TEMPLATE_NOTES
**Template 02 (Complex Task)** — TDD creation involves scope discovery, parallel Phase-2 investigation,
Phase-3 completeness verification, Phase-4 web research, Phase-5 synthesis, Phase-6 assembly+validation. The
final TDD conforms to `src/superclaude/examples/tdd_template.md` (v1.2). Mark §9/§10/§16 N/A (backend/library).
Repurpose §8 as module/function API + contract-field surface. §13/§17/§26 light. Heavyweight line budget
1,200–1,800; cap 2,000.

## REUSE_AUDIT
Full machine-readable findings in `research/reuse-audit.yaml`. Summary (proposed component → verdict):
- **Surface symbol tagger** → **distinct** (S_reuse 0.37). Reflect-local. Audit `wiring_gate._safe_parse`,
  `filetype_rules` table, `dead_code` hook-exclusions don't parse diff hunks or detect Click/Typer decorators.
- **Referrer finder** → **distinct** (maybe-related, S_reuse 0.67, shape-divergent). Model fail-open static+grep
  tiering after `cli/audit/dependency_graph.py` (Tier-A AST / Tier-B grep), but implement SYMBOL-level locally —
  audit graph is FILE-level, too broad for symbol referrer + comment/test partitioning.
- **Production-vs-test partitioner** → **distinct** (S_reuse 0.57). Reuse filename-marker LISTS from
  `filetype_rules.py` only after reconciling semantics — audit defaults UNKNOWN→SOURCE; runtime-surface needs
  unknown/ambiguous→DEGRADE, plus inline-test + comment exclusion audit lacks.
- **Degrade oracle** → **distinct** (maybe-related, S_reuse 0.68). Reuse dynamic-import regex SCANNING from
  `dynamic_imports.py` as pattern data; the 4-category oracle is separate (audit maps dynamic→KEEP:monitor,
  not DEGRADE).
- **Entrypoint rootwalk (depth=1)** → **reuse-by-import** (STRONGEST, S_reuse 0.81, shape-divergent). Adapt
  `cli/audit/reachability.py` `_bfs_reachable` skeleton but enforce depth=1 + DEGRADE-on-partial-enumeration
  (reachability reports UNREACHABLE on dynamic-dispatch uncertainty; runtime-surface requires DEGRADE; reachability
  uses depth>50). Boundary: reflect→audit import is mechanically legal (only sprint/roadmap banned) but couples
  product path to cleanup-audit; **§6.4/§21 must decide import vs extract-boundary-neutral-helper vs reflect-local copy.**
- **Ledger writer + scalar computer** → **distinct** (S_reuse 0.56). Implement from runtime-surface.md schema;
  reuse only generic YAML style (`IndentDumper`, `_atomic_write_text`).

No proposed component is a confident-duplicate. **Dependency-boundary note for the TDD:** the single most
load-bearing design decision is whether reflect imports from cli/audit. Mechanically legal, semantically
coupling — surface it as a Key Design Decision (§6.4) + Alternative (§21) + Open Question (§22), NOT a silent choice.

## AMBIGUITIES_FOR_USER
- **OQ-DRS.2 (invocation site)** and **OQ-DRS.1 (referrer engine)** and **OQ-DRS.3 (contract version)** are
  spec-level open questions — the TDD documents them in §22 Open Questions with a recommended resolution; it
  does NOT need to pre-resolve them with the user (the spec already frames the tradeoffs and recommended floors).
- The invocation surfaced one design tension worth a one-line flag in the TDD intro: the spec's §2 names
  `commands.py` as the writer, but `commands.py` only covers `superclaude reflect run`, not bare
  `claude -p /sc:reflect` (the bare-skill path the §0 evidence experiment actually exercised). The TDD should
  state explicitly which paths get deterministic fields and which remain LLM-emitted (OQ-DRS.2). No user
  decision required to PROCEED — intent is clear from the spec and codebase.
