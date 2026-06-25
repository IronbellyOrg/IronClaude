# Synthesis 08 — §16 Accessibility, §17 Performance, §18 Dependencies, §19 Migration & Rollout

**Task:** TASK-TDD-20260621-124414 (FR-DRS — Deterministic Runtime-Surface Sweep)
**Produces TDD template sections:** 16, 17, 18, 19
**Source research:** 00-prd-extraction, 01-runtime-surface-algorithm, 02-product-path-integration, 05-reuse-and-boundaries, 06-skill-prose-demotion
**Date:** 2026-06-21

---

## 16. Accessibility Requirements

**N/A — rationale: backend/library + CLI component, no UI/frontend surface.**

FR-DRS is a pure-Python sweep module (`src/superclaude/cli/reflect/runtime_surface.py`) invoked
by the reflect CLI layer; its only outputs are a YAML ledger artifact and six contract scalars
written to disk. There is no rendered UI, no DOM, no screen-reader, keyboard-navigation, focus,
or color-contrast surface. WCAG 2.1 AA does not apply.

The template's §16.1 requirements table and §16.2 testing tools are therefore not instantiated.
Operator-facing output (REPORT.md narration, stderr `contract:` echo) is plain text consumed in a
terminal and inherits the existing reflect CLI's text conventions; no new accessibility obligation
is introduced.

---

## 17. Performance Budgets

> **LIGHT section.** FR-DRS adds a local file scan + bounded ripgrep/AST passes over the diff
> already under audit. The frontend/backend latency and SLO machinery of the template (§5.2 SLOs,
> Lighthouse metrics, APM percentiles) does **not** apply — there is no service, no request path,
> no error budget. The only cost is **local CPU for the scan**, and it must complete within the
> reflect run's existing budget; there is **no separate SLO infra** to provision.

### 17.1 Cost Model

The sweep is invoked inside an already-running reflect audit and operates on artifacts the audit
has already produced or fetched, so its marginal cost is bounded and additive-only:

| Stage | Work performed | Marginal cost | Notes |
|-------|----------------|---------------|-------|
| Tag (step 1) | AST-parse / decorator-scan of changed diff hunks only | Local CPU, O(diff size) | Python `ast` over hunk-enclosing symbols; non-surface diff short-circuits to zero added cost |
| Find-referrers (step 2) | **Extends the already-fetched step-4 referrer result** | **Zero added fetch** | No second `find_referencing_symbols` call; reuses `include_info:true` payload (research 06, SKILL.md:489) |
| Partition (step 3) | path/inline-test/comment classification of referrers | Local CPU, O(referrers) | Pure string/marker checks against the §2 language table |
| Degrade-oracle (step 4) | regex/predicate match over hunk + adjacent metadata | Local CPU, negligible | `pyproject.toml` read once; reuses `_DYNAMIC_PATTERNS` regex data |
| Rootwalk (step 5) | depth=1 bounded walk from enumerated roots, candidate-UNREACHED only | Local CPU, bounded by depth=1 | Hard depth constant = 1; never a full transitive search |
| Reduce + emit (steps 6–7) | per-symbol reduction + ledger/scalar write | Local CPU + 1 atomic file write | One `runtime-surface-ledger.yaml` write per run |

### 17.2 Budget Table

| Metric | Budget | Measurement |
|--------|--------|-------------|
| Added cost on a **non-surface diff** | **Zero** (fast-path exit before any referrer work) | Unit assertion: `runtime_surface_sweep_ran == false`, no ledger write (research 01 §1) |
| Added cost on a **surface diff** | Bounded local-CPU scan; completes within the reflect run's existing wall-clock budget | No separate timer/SLO; folded into the audit's runtime |
| Second referrer fetch | **None** — sweep extends the step-4 result | Code review: no new `find_referencing_symbols` call site |
| Referrer-finder execution mode | `rg --sort path` single-thread cost is acceptable | Deterministic ordering > throughput; the single-thread cost is the accepted trade for reproducibility |
| Ledger I/O | 1 atomic write under `<output>/artifacts/` per run (re-run each fix-loop turn) | `_atomic_write_text` (research 02, runner.py:70-89) |

### 17.3 Performance Posture

- **No load/stress/soak testing.** The sweep is a one-shot local computation per audit, not a
  served endpoint; the template's §17.3 performance-test matrix is N/A.
- **Determinism over speed.** OQ-DRS.1 resolves the referrer engine to a ripgrep/AST floor (LSP
  optional). Where ripgrep is used, `--sort path` enforces stable single-thread ordering so the
  ledger and scalars are byte-reproducible across runs (AC-2 "no variance"); the single-thread
  cost is acceptable because reproducibility is the load-bearing property, not throughput.
- **Re-run cost in the fix loop.** `_audit_once` re-runs on every fix-loop turn (research 02,
  runner.py:562), so the sweep recomputes deterministically each cycle with the SAME `--base`
  (NFR-4). The cost is the same bounded local scan per turn; no caching is required for v1.

---

## 18. Dependencies

FR-DRS introduces no new third-party package. It leans on the Python stdlib, one optional
external binary (ripgrep), reflect-local writer conventions, and an optional structured-referrer
overlay. Every external/optional dependency has a fallback that preserves the asymmetric-cost
posture (a missing capability DEGRADEs, never silent-skips, never aborts).

### 18.1 External Dependencies

| Dependency | Version | Purpose | Risk Level | Fallback |
|------------|---------|---------|------------|----------|
| Python `ast` | stdlib (≥3.10) | Parse changed diff hunks → enclosing symbols; decorator/registration evidence for the surface tagger | Low | None needed (stdlib, always present); mirrors `wiring_gate._safe_parse` fail-soft (return-`None`-on-parse-error) (research 05 §1) |
| ripgrep (`rg`) | external binary | Symbol-referrer scan (Tier-B grep floor of the referrer finder) when no structured engine is available | **Medium** (may be absent on the host) | Pure-Python AST scan as the referrer floor; if **neither** ripgrep nor an AST referrer pass resolves a referrer, **DEGRADE** that edge (never UNREACHED, never silent-skip). Where `rg` is used, invoke with `--json --sort path` for deterministic, byte-reproducible ordering (web-01) so the ledger + scalars do not vary across runs (AC-2) |

### 18.2 Internal Dependencies (reflect-local conventions)

| Dependency | Location | Purpose | Risk Level | Fallback |
|------------|----------|---------|------------|----------|
| `_IndentDumper(yaml.SafeDumper)` | reflect-local, runner.py:58-67 | yamllint-safe (`indent-sequences: true`) dump of the ledger's nested block sequences (`unreached_surfaces:`, `production_referrers:`) | Low | None — **MANDATORY.** The new ledger writer MUST dump through `_IndentDumper`, **NOT** ensemble's bare `yaml.safe_dump` (ensemble.py:508-509), or pre-commit yamllint fails on the nested sequences (research 02; `mem:reference_yamllint_indent_sequences_pyyaml`) |
| `_atomic_write_text(path, text)` | reflect-local, runner.py:70-89 | Atomic (randomized same-dir temp + `os.replace`) ledger/contract write; parallel-session last-write-wins safety; `mkdir(parents=True, exist_ok=True)` for the new `<output>/artifacts/` dir | Low | None — **MANDATORY** for overwrite-atomicity; the runner convention, NOT ensemble's plain `path.write_text` |
| reflect→audit import | conditional on the §6.4 D1 decision | Optional reuse of `cli/audit` BFS (`_bfs_reachable`) for the entrypoint rootwalk | Low (by recommendation) | **Research recommends the reflect-local copy (Option C, research 05 §7)** of the ~30-line BFS skeleton with depth=1 + DEGRADE-on-partial baked in → **NO hard dependency on `cli/audit`.** The import is mechanically legal (the ban names `cli/sprint`+`cli/roadmap` only) but Option A is to be AVOIDED (silently couples reflect's product path to cleanup-audit's semantics-inverted heuristics) |

> Constants reuse note: the `_DYNAMIC_PATTERNS` regex DATA (audit `dynamic_imports.py:24-39`) and
> the `_TEST_PREFIXES`/`_TEST_INFIXES` marker LISTS (audit `filetype_rules.py:105-107`) are tiny
> pure data. Research 05 (G2) recommends **copying** them into reflect rather than importing, to
> keep the reflect→audit boundary clean — so they are NOT a runtime dependency edge.

### 18.3 Optional Dependencies

| Dependency | Version | Purpose | Risk Level | Fallback |
|------------|---------|---------|------------|----------|
| Serena / LSP structured-referrer overlay | external MCP/LSP server | Higher-confidence symbol-referrer resolution (Tier-A) layered over the ripgrep/AST floor | **High** (server availability is unreliable; OQ-DRS.1 resolves the engine to a ripgrep/AST floor with LSP optional) | ripgrep/AST floor (§18.1); when the structured server is unavailable, **DEGRADE** the affected edge (web-02), append `"runtime-surface:backend_unavailable"` to `degraded_components`, continue over remaining edges, NEVER STOP (P3 fail-open envelope) |

---

## 19. Migration & Rollout Plan

FR-DRS lands across the three integration paths research mapped (research 02 §"coverage tradeoff
summary"): the **SKILL.md prose** (the bare-skill + Tier-1 author surface), the **contract
producer** (LLM/ensemble → Python), and the **CLI product path** (`runner._audit_once`). The
rollout is staged and **additive** — disabling the sweep falls back to the existing LLM emission,
so each phase is independently revertable.

### 19.1 SKILL.md Prose Demotion

The §6.1 step 4b/4b′ prose flips from an **LLM instruction** to a **narration-only** directive:

| Before (LLM-instruction) | After (deterministic-sweep producer) |
|--------------------------|--------------------------------------|
| "classify diff-hunk symbols … **compute and hand-type** the six `runtime_surface_*` scalars + write the ledger" (lines 465/466/487/489/491, §9.1 comment 721-730) | "the deterministic FR-DRS sweep module computes these six scalars and writes the ledger; the LLM **narrates the verdict in REPORT.md only** and MUST NOT hand-type the fields" (research 06 §2) |

**CRITICAL — PRESERVE (out of scope for demotion):** the SAFETY behavior MUST remain verbatim.
The load-bearing sentence **"never emits a clean PASS for a tagged surface whose reachability
could not be evaluated"** (SKILL.md:489), the DEGRADE-first precedence + oracle/rootwalk-before-
UNREACHED rule, the fail-open/NEVER-STOP envelope, the dynamic→DEGRADE soundness floor, UC-2-only
scoping, and the §5.3 pre-filter coupling all stay (research 06 §3, P1–P6). Demotion changes
*who computes the scalars*, never *what a verdict means or why an unwired surface must not
clean-pass*.

**CONDITIONAL — bare-skill path (OQ-DRS.2 / research 06 G1):** because a bare
`claude -p /sc:reflect` **never enters the Python wrapper** (research 02 §"end-to-end pipeline":
that path runs the skill's own LLM sweep, never `runner._audit_once`), the demotion CANNOT be
unconditional. The prose must keep an **LLM-fallback emission branch**: *"when the FR-DRS module
ran, the LLM narrates only; otherwise the legacy emission prose applies."* The demotion wording
is conditional on the module having run.

### 19.2 Contract Producer Change WITHOUT a Field-Set Change

The §9.1 contract block changes **producer only** — no field added/removed/renamed/retyped
(research 06 §5). Therefore:

- **No `contract_version` bump.** Stays **`1.6.0`** (OQ-DRS.3 resolves "no bump": the change is
  producer-only and consumer-transparent; §9.4 reserves major bumps for consumer-breaking
  shape/semantic changes, of which FR-DRS makes none). Optionally annotate the inline comment that
  the six fields are now deterministically produced — but no version signal is required.
- **Reconcile the stale ensemble version stamp.** `ensemble.REFLECT_CONTRACT_VERSION = "1.0"`
  (ensemble.py:59, used at :378) is two minor generations behind the skill's declared `1.6.0`
  (SKILL.md:672). The consumer only gates `major == "1"` so it is not breaking today, but once the
  ensemble path emits the six fields, stamping them `1.0` while the skill calls that schema `1.6.0`
  is an internal inconsistency to reconcile (bump `REFLECT_CONTRACT_VERSION`, or document the
  wrapper's version as intentionally independent) (research 02 Stale Documentation).
- **Contract-emission prose retargeted, not deleted:** FR-RSR.7's "MUST carry … by exact names"
  becomes a statement of the module's emission contract (name-exactness guaranteed by construction
  + asserted by the grader), with the anti-improvisation warning kept as a defensive note for the
  residual narration/bare-skill path (research 06 §4).

### 19.3 Phased Rollout

| Phase | Action | Rollback posture |
|-------|--------|------------------|
| 1 | Build `cli/reflect/runtime_surface.py` (6 components: tagger, referrer-finder, partitioner, degrade-oracle, rootwalk, ledger-writer) + unit tests for each + the count invariant `len(unreached_surfaces) == runtime_surface_unreached`. Module unwired. | Module unreferenced → zero product impact |
| 2 | Wire the module into the product path at `runner._audit_once` (the tier-agnostic chokepoint, runner.py:394-453): compute the six fields + ledger after launch, MERGE-overwrite the six keys into the just-authored contract before `parse_contract` (runner.py:445), atomic-write via `_atomic_write_text`+`_IndentDumper`. Add the consumer triggers in `contract.py` (`_halted_reason` for UNREACHED, `_degraded_reason` for degraded). | Gate the sweep call behind a flag/guard; disabling falls back to the LLM-authored fields (additive) |
| 3 | Wire the eval grader to the SAME module so the eval harness asserts against the deterministic producer (name-exactness + invariant as the test oracle, research 06 §4). | Grader assertion is additive; revert leaves the existing grader untouched |
| 4 | Demote the SKILL.md prose (§19.1) — switch 4b/4b′ to narration-only WITH the conditional LLM-fallback branch for the bare-skill path; preserve all safety sentences (§19.1 PRESERVE). | Restore the prior emission prose; the safety sentences never changed so no safety regression on revert |

**Rollback note:** the sweep is **purely additive** — it merges deterministic values over an
existing (LLM-authored) contract surface. Disabling it at any phase falls back to the prior LLM
emission with no schema change and no consumer change, because the field set and `contract_version`
are unchanged throughout.

**Status:** Complete
