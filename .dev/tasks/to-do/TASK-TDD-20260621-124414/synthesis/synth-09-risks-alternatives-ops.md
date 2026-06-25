# FR-DRS TDD — Synthesis 09: Risks, Alternatives, Open Questions, Ops, Reuse Audit

> **Scope:** Sections 20–26 of the FR-DRS TDD (`sc:reflect` Deterministic Runtime-Surface Sweep) plus the `## Reuse & Consolidation Audit` section.
> **Source feature:** `FR-DRS` — `src/superclaude/cli/reflect/runtime_surface.py` (greenfield), under `sc-reflect-protocol`.
> **Driving evidence:** 3×before/3×after eval experiment (2026-06-20) proving prose-only emission cannot deliver the structured guarantee.
> **Verification posture:** The module is greenfield — no runtime-surface implementation exists in `src/superclaude/cli/reflect/` (grep-confirmed across all seven files). Most algorithm claims below are legitimately `[UNVERIFIED — spec-only]`: forward-looking design contracts, **not** stale documentation. `[CODE-VERIFIED]` is reserved for claims confirmed against existing source.

---

## 20. Risks & Mitigations

The dominant risk class for FR-DRS is **a false `UNREACHED` verdict on idiomatic-but-statically-invisible wiring** — the exact failure the degrade oracle and rootwalk exist to prevent. The asymmetric-cost doctrine (`refs/runtime-surface.md`: never silently PASS an untested surface, never silently Regression an idiomatic dynamic/registry/decorator/packaging/reflection entrypoint) is the governing mitigation posture; every risk below is a way that doctrine could be breached.

| ID | Risk | Probability | Impact | Mitigation | Contingency |
|----|------|-------------|--------|------------|-------------|
| **R1** | **False `UNREACHED` → Regression on idiomatic wiring.** The sweep tags a surface (decorator route / registry value / packaging entrypoint) and reduces it to `UNREACHED` because no static production referrer appears, escalating a clean idiomatic edge into a blocking Regression. | M | **H** (false STOP on valid code; erodes trust in the gate) | Run the **degrade oracle (categories a–d) AND the entrypoint-rootwalk BEFORE any `UNREACHED` may be emitted** (`runtime-surface.md` §3, §4 gating rule: rootwalk is invoked on *every* candidate-`UNREACHED`). Decorator/registry/`[project.scripts]`/reflection matches all force `DEGRADE`, never `UNREACHED`. Add **counter-hygiene**: a DEGRADE symbol is NOT added to `unreached_surfaces`, so it cannot inflate `runtime_surface_unreached` (preserves the count invariant). | If a false UNREACHED ships: the verdict/prose safety layer (AC-5, already-working) still refuses a clean-pass; widen the oracle predicate and add the missed idiom as a fixture case. |
| **R2** | **Bare `claude -p /sc:reflect` path not covered by the Python sweep.** A direct skill invocation never enters the CLI wrapper (`commands.py`/`runner.py`), so a sweep wired only into `_audit_once` leaves the bare-skill path still LLM-emitting the six scalars — the very path the §0 evidence experiment exercised. | M | M (deterministic guarantee partial; bare path keeps the old unreliability) | **Conditional demotion + LLM-fallback branch:** the deterministic sweep authoritatively writes the six fields on every runner-driven path; SKILL.md §6.1 is demoted to "the deterministic sweep computes these" only where the sweep ran. Where the Python sweep did NOT run (bare `claude -p`), the skill retains the LLM emission as an explicit, documented fallback. Long-term coverage of the bare path requires a **Wave-1A skill shell-out** to the same importable module (the only option covering the non-CLI path — see §21 Alt 1 and OQ-DRS.2). | Document explicitly which invocation paths get deterministic fields and which remain LLM-emitted (per the AMBIGUITIES_FOR_USER flag); the bare path degrades to today's behavior, not to a worse state. |
| **R3** | **ripgrep referrer non-determinism.** Identical input yields a different referrer ordering across runs, making the ledger rows / `production_referrers` lists order-sensitive and the eval non-reproducible (AC-2 demands no variance across ≥3 runs). | L | M (eval flake; ledger diff noise) | Invoke ripgrep with **`--sort path`** so the referrer set is emitted in a stable, deterministic order; canonicalize the `edge` formatter and sort `production_referrers` before emit. (ripgrep parallel traversal is otherwise order-nondeterministic.) | If residual nondeterminism remains, sort all emitted lists post-collection in Python before YAML dump; assert ordering in the count-invariant test. |
| **R4** | **LSP / Serena unavailability** (the optional precision overlay): cold-start partial subsets, tens-of-seconds startup, unmet `didOpen` handshake, server-erroring/null/partial returns (web-02 F5–F7). If the sweep depended on LSP, identical input could yield different verdicts by index warmth. | M | M (non-deterministic verdict if LSP were load-bearing) | **DEGRADE-to-floor:** ripgrep/AST is the determinism-safe floor and ground truth; LSP is an OPTIONAL overlay that may only *refine* (prune false positives), never be *required* to reach a verdict. Define DEGRADE broadly — force fallback to the floor on ANY unavailability signal (binary absent, no `referencesProvider`, handshake error, `references` errors/times-out/returns `null`/returns a same-file-only subset) and emit an explicit auditable `runtime-surface:backend_unavailable` marker in `degraded_components`. | Sweep continues over remaining edges with no global abort; affected edge degrades to §10.6 Grounding Gap, `runtime_surface_degraded: true`, NEVER STOP. |
| **R5** | **reflect→audit coupling.** Importing `cli/audit` heuristics (e.g. `reachability._bfs_reachable`) into reflect's product path silently couples gating behavior to cleanup-audit semantics whose defaults are the **inverse** of runtime-surface's asymmetric-cost doctrine (UNKNOWN→SOURCE, dynamic→KEEP:monitor, dynamic-dispatch→UNREACHABLE, depth>50). A future cleanup-driven change to audit heuristics would silently alter reflect gating. | M | M (silent semantic drift across packages; depends on an unexported `_bfs_reachable` internal) | **Reflect-local copy per §6.4 D1:** adopt the in-repo `runner.py:14-17` copy-over-import precedent — copy/adapt the ~30-line BFS skeleton into `runtime_surface.py` with depth=1 + DEGRADE-on-partial baked in. Keeps reflect's product/gating path fully decoupled from cleanup-audit heuristic drift. The reflect import ban (`runner.py`/`config.py`/`models.py` docstrings) names `cli/sprint` and `cli/roadmap` ONLY — importing `cli/audit` is *mechanically legal* but a coupling-quality liability. | If a second reflect consumer of graph-BFS appears, extract a boundary-neutral shared helper (§21 Alt 3 Option B) carrying no policy. |

> **Note:** R1 and R5 are linked — the reuse-by-import path (R5) would import `reachability`'s dynamic-dispatch→UNREACHABLE behavior, which is precisely the false-UNREACHED failure mode of R1. The reflect-local copy mitigation for R5 (depth=1 + DEGRADE-on-partial) is also the structural guard for R1.

---

## 21. Alternatives Considered

> This is one of the most important sections of the TDD. The three open questions (OQ-DRS.1/.2/.3) map directly onto Alternatives 2, 1, and the contract-version decision; the TDD **documents** the tradeoffs and a recommended floor, it does **not** pre-resolve them with the user.

### Alternative 0: Do Nothing *(mandatory)*

**Description:** Keep the FR-RSR approach — runtime-surface emission lives as SKILL.md prose executed by an LLM. Continue strengthening that prose (sharper forbidden-key lists, more explicit MANDATORY-EMISSION comments) rather than moving the structured-emission path into Python.

**Pros:**

- No engineering cost — no new module, no product-path wiring, no eval-harness change.
- No operational burden and no risk of introducing regressions into the reflect gating path.
- The **safety behavior already works** — across every run the skill caught the unwired/registry/test-only surface and never clean-passed it (FR-S9-04 blind spot closed at the verdict/prose level). "Do nothing more" preserves that.

**Cons:**

- **Refuted directly by the §0 evidence.** The controlled 3×before/3×after experiment (2026-06-20) proved a prose-only implementation **cannot** deliver the structured-output guarantee *even after the prose was strengthened to forbid exactly the observed ad-hoc names* (strengthened skill verified loaded):
  - Ad-hoc field names persisted on non-escalating paths — `runtime_surface_reachable: true` (REACHED), `surface_reachability_verdict: DEGRADE` (DEGRADE), `surface_production_reachable: false` / `unreachable_surfaces` (quiet-UNREACHED).
  - `runtime-surface-ledger.yaml` was written in only **1 of 9** quiet-path runs — so deriving the contract fields from the ledger is also non-viable; the ledger is the missing artifact.
- Root cause is structural, not fixable by more prose: the LLM only fully engages the structured machinery on an *alarming* UNREACHED that escalates; quiet paths get a lighter reflection (correct verdict in prose, no ledger, improvised scalar names). No amount of prose strengthening changes that engagement asymmetry.
- The §5.3 forbid-STOP pre-filter consumes the structured mirror today — an unreliable mirror means a non-deterministic gate. *(The `sprint run` executor is a **deferred/FR-006a** future consumer — `cli/sprint/executor.py` reads no reflect contract today — but the same reliability argument will apply if/when it is wired.)*

**Why Not Chosen:** The whole premise of FR-DRS is that prose strengthening was *already tried and measured to fail*. "Do nothing" is not viable because the deterministic structured guarantee (AC-1, AC-3) is unreachable by an LLM executing prose — the experiment is the falsifier. FR-DRS is scoped narrowly to fix exactly this (the structured mirror), leaving the working verdict/prose safety untouched.

---

### Alternative 1: Invocation site — where the sweep runs *(OQ-DRS.2)*

**Description:** Three candidate sites for invoking the deterministic sweep and writing the six fields + ledger into the contract: (i) `commands.py` (post-skill, the spec's §2 named writer); (ii) `runner._audit_once` (the tier-agnostic chokepoint between contract-authoring and `parse_contract` at `runner.py:445`); (iii) a Wave-1A skill shell-out (the skill itself shells out to the importable Python module).

**Pros:**

- `_audit_once` (`runner.py:394-453`) is the **strongest CLI-side site** — it runs on every audit of BOTH tiers (Tier-1 LLM-authored, Tier-2 ensemble-authored) and re-runs on every fix-loop re-audit, sitting exactly between "contract authored at `config.contract_path`" and "`parse_contract` reads it." It can MERGE-overwrite the six deterministic fields into the just-authored contract and emit the ledger, then `derive_verdict` consumes the deterministic values.
- The skill shell-out is the **only** option that also covers a bare `claude -p /sc:reflect` (the non-CLI path) — it requires a reusable importable sweep module the skill invokes.

**Cons:**

- `commands.py` is a **poor fit**: its only product seam is line 254 (`ReflectRunner(config).run()`); anything before it predates contract authoring (the runner's `_audit_once` overwrites `config.contract_path` wholesale on both tiers, clobbering a pre-written sweep contract), and it covers **only** `superclaude reflect run`, never the bare path.
- `_audit_once`, despite being the best CLI-side site, **misses bare `claude -p`** — that path never enters Python at all.
- The skill shell-out adds a second invocation surface to keep in lockstep with the CLI path (two callers of one module).

**Why Not Chosen (for a single-site-only design):** No single CLI-code site covers the bare path. The recommended shape (documented in §22, not pre-resolved) is the **importable pure-Python module called from `runner._audit_once` for both runner-driven tiers, with a Wave-1A skill shell-out for the bare path** — `_audit_once` is the strongest single site but is explicitly NOT sufficient alone because it misses bare `claude -p`. `commands.py` (the spec's literal §2 wording) is rejected as the writer because the runner clobbers any contract written there.

---

### Alternative 2: Referrer engine — floor vs precision overlay *(OQ-DRS.1)*

**Description:** What resolves symbol referrers: (i) pure ripgrep/AST (deterministic, zero-dependency floor) vs (ii) programmatic Serena/LSP (`textDocument/references` via `multilspy.SyncLanguageServer.request_references`, semantic precision — code-only + usage-kind categorization).

**Pros:**

- **LSP precision is real but bounded:** measured ~24% fewer non-code false positives (63 vs 83 files, same recall); usage-kind categorization distinguishes a `Mock(spec=authenticate)` test ref from a real call — directly relevant to the `uc2-surface-test-only-ref` and `uc2-surface-dynamic-dispatch` cases.
- ripgrep/AST is **deterministic, dependency-free, and reproducible from the floor alone**; it over-reports (conservative — won't miss a real call) which suits the asymmetric-cost posture.

**Cons:**

- **LSP referrers are NOT deterministic out of the box** (web-02 F5–F7): cold-start returns same-file-only subsets until indexing completes; tens-of-seconds variable startup; `didOpen`/handshake prerequisites; per-server capability deviations. Identical input → different output by index warmth — a direct determinism counterexample that AC-2 (no variance across ≥3 runs) cannot tolerate if LSP were load-bearing.
- "Unavailable" is multi-valued (server-erroring / null / partial subset / unmet handshake) — all must map to DEGRADE, adding handling surface.

**Why Not Chosen (as the floor):** Determinism is the whole point of FR-DRS, and external primary sources confirm live LSP referrer results are non-deterministic without index-warmth control. **The ripgrep/AST floor is the determinism-safe default** (web-02 conclusion); LSP/Serena stays an OPTIONAL precision overlay that may only *refine* (prune false positives) and **must DEGRADE to the floor on any unavailability signal** (defined broadly), emitting an auditable degrade marker. The floor is ground truth; LSP must never be required to reach a verdict or flip a PASS/FAIL non-reproducibly. Recommended floor documented in §22 (OQ-DRS.1), not pre-resolved.

---

### Alternative 3: `reachability.py` reuse strategy — import vs reflect-local vs extract *(the §6.4 D1 boundary decision)*

**Description:** The entrypoint-rootwalk is the strongest reuse candidate (`S_reuse` 0.81) against `cli/audit/reachability.py` `_bfs_reachable:591`. Three options: **(A)** import `cli/audit` directly (`from superclaude.cli.audit.reachability import ...`); **(B)** extract a boundary-neutral shared BFS helper both audit and reflect import; **(C)** reflect-local copy of the ~30-line BFS skeleton with depth=1 + DEGRADE-on-partial baked in.

**Pros:**

- **(A)** zero new code for the BFS; single source of truth; lowest immediate LOC.
- **(B)** one BFS implementation, no product↔cleanup coupling; the neutral helper carries no policy; matches reflect's established callable-interface decoupling pattern.
- **(C)** zero cross-package coupling; reflect owns its semantics entirely; smallest blast radius; mirrors the in-repo `runner.py:14-17` precedent that already copies `_IndentDumper` locally rather than importing a private symbol.

**Cons:**

- **(A)** mechanically legal (only `cli/sprint`/`cli/roadmap` are banned) but **couples reflect's PRODUCT path to cleanup-audit semantics** whose defaults are the *inverse* of runtime-surface's doctrine (dynamic-dispatch→UNREACHABLE vs required-DEGRADE; depth>50 vs depth=1; UNKNOWN→SOURCE vs DEGRADE). It also reaches into an unexported `_bfs_reachable` internal — a stability risk independent of coupling. `_bfs_reachable` is itself unbounded (no depth parameter), so depth=1 must be enforced by the caller regardless.
- **(B)** a refactor touching `cli/audit` (extract + re-point `reachability.py`), larger diff, needs its own regression coverage — arguably over-engineering for a ~30-line BFS today.
- **(C)** ~30 lines of BFS duplicated; the two copies could drift (low risk — BFS is stable).

**Why Not Chosen (A rejected; B deferred):** **Option C (reflect-local copy) is the recommended v1 choice**, ratified as §6.4 D1, not a silent pick: (1) the in-repo `runner.py:14-17` precedent already chose copy-over-import for exactly this private-symbol-coupling reason; (2) the semantic divergence (depth=1, DEGRADE-on-partial, dynamic-dispatch→DEGRADE) is large enough that the adapted BFS is barely the same function — importing the audit version then overriding its inverted defaults is *more* fragile than owning ~30 lines; (3) it keeps reflect's gating path decoupled from cleanup-audit heuristic drift. **Option A is the one to AVOID** despite lowest LOC, precisely because the coupling is silent and semantics-inverted. **Option B is the clean long-term shape** if a second reflect consumer of graph-BFS appears (see OQ in §22 / Reuse Audit disposition).

---

## 22. Open Questions

> **Posture:** The three FR-DRS open questions are **spec-level and unresolved by design.** The TDD *documents* each with a recommended resolution (a floor the spec already frames); it does **not** pre-resolve them with the user. No user decision is required to PROCEED — intent is clear from the spec and codebase. Status `🟡 Investigating` reflects "recommendation recorded, ratification at implementation."

| ID | Question | Owner | Status | Recommended Resolution |
|----|----------|-------|--------|------------------------|
| **OQ-DRS.1** | **Referrer engine.** Is the referrer source pure ripgrep/AST, or programmatic Serena/LSP? | Engineering (reflect) | 🟡 Investigating | **ripgrep/AST as the determinism-safe floor; LSP/Serena as an OPTIONAL precision overlay that DEGRADEs-to-floor on any unavailability signal.** External primary sources confirm live LSP referrer results are non-deterministic without index-warmth control (cold-start partial subsets, variable startup, handshake prerequisites). The floor is ground truth; LSP may only refine, never be required to reach a verdict (web-02 conclusion). See §21 Alt 2. |
| **OQ-DRS.2** | **Invocation site / bare-path coverage.** Does the sweep run inside `commands.py` (post-skill), as `runner._audit_once` merge, or as a Wave-1A skill shell-out — and must a bare `claude -p /sc:reflect` also get deterministic fields? | Engineering (reflect) | 🟡 Investigating | **Importable pure-Python module called from `runner._audit_once`** (the tier-agnostic chokepoint covering both runner-driven tiers + the fix loop) **for the CLI path, with a Wave-1A skill shell-out to the same module for the bare path.** `_audit_once` is the strongest single site but misses bare `claude -p`; `commands.py` (the spec's literal §2 wording) is rejected because the runner clobbers a contract written there. The TDD must state explicitly which paths get deterministic fields vs remain LLM-emitted. See §21 Alt 1, R2. |
| **OQ-DRS.3** | **Contract version.** Does FR-DRS bump the `contract_version`? | Engineering (reflect) | 🟡 Investigating | **No version bump recommended.** FR-DRS changes the PRODUCER of the six `runtime_surface_*` fields, not the field set — semantics unchanged, reliability improved. FR-RSR already shipped these as the additive `1.6.0` block; major stays `"1"`, so the consumer gate (`contract.py` checks `major == "1"`) passes unchanged. **Caveat to reconcile:** the Tier-2 ensemble currently stamps `REFLECT_CONTRACT_VERSION = "1.0"` (`ensemble.py:59`) while the skill declares `1.6.0` — when the ensemble path begins emitting the six fields, this internal inconsistency should be reconciled (bump the ensemble constant or document the wrapper's version as intentionally independent). |

### 22.1 Greenfield & verification caveats (carry-forwards)

- **Greenfield module → most algorithm claims are `[UNVERIFIED — spec-only]`.** `refs/runtime-surface.md` is a forward-looking SPEC; `src/superclaude/cli/reflect/` has zero runtime-surface code today (grep-confirmed across all seven files). A spec-only tag is a legitimate design contract, **not** stale documentation — there is no implementation to have drifted from. The single in-repo `[CODE-VERIFIED]` anchor is the `pyproject.toml` `[project.scripts]` entries (`superclaude = "superclaude.cli.main:main"`, `ic = "superclaude.cli.ic:main"`) the degrade oracle category (b) cites.
- **C-5 — `evals.json` → `eval_metadata.json` materializer UNVERIFIED.** The grader reads per-eval `eval_metadata.json` (`grader.py:445`), but `evals.json` is the registry/spec; the step that flattens `evals.json` → per-eval `eval_metadata.json` (and copies `cases/uc2-*/expected.yaml` + `input/` into `iterations/iteration-N/eval-<name>/`) was **not located** in research. Whether the eval-path "runner materializes the contract upstream of grading" hook lives there is unverified — must be located before the eval-wire phase.
- **C-6 — `grader.py:448-449` target-prefix routing fragility.** `grade_eval` buckets assertions ONLY by `target.startswith("with_skill/" | "old_skill/")`. An assertion using a non-`target` key (as `citation_resolves`/`checkpoint_logged`/`path_exists` do) falls into **neither** bucket and is **never graded**. The 5 current UC-2 cases are safe (every UC-2 assertion uses a `target` key), but **any new oracle assertion type added for FR-DRS MUST carry a `target` key** (or extend the bucketing logic) — otherwise it silently never runs. This is a hard constraint on the eval-wire design (§21 Alt 1 Option A equivalent on the eval side).

---

## 23. Timeline & Milestones

### 23.1 High-Level Timeline

| Milestone | Status | Dependencies |
|-----------|--------|--------------|
| Design Complete (this TDD approved) | ⬜ | spec.md, research synthesis |
| Phase 1 — Module + tests | ⬜ | Design approval |
| Phase 2 — Product wire | ⬜ | Phase 1 module importable |
| Phase 3 — Eval wire | ⬜ | Phase 1 module; C-5 materializer located |
| Phase 4 — Prose demotion | ⬜ | Phases 2–3 deterministic fields live |
| GA (all AC-1..AC-6 met) | ⬜ | All phases + Release Criteria §24 |

### 23.2 Implementation Phases (4-phase rollout)

#### Phase 1 — Module + tests

**Deliverables:**

- [ ] New `src/superclaude/cli/reflect/runtime_surface.py` implementing the 7-step sweep (tag → find-referrers → partition → degrade-oracle → rootwalk → reduce → emit), pure-Python, no LLM.
- [ ] `RuntimeSurfaceLedgerRow` TypedDict + per-symbol reduction (`DEGRADE > UNREACHED > REACHED`) + 6-scalar computation with the count invariant by construction.
- [ ] Reflect-local BFS copy (depth=1 + DEGRADE-on-partial, per §6.4 D1 / §21 Alt 3 Option C); ripgrep floor invoked with `--sort path` (R3).
- [ ] Unit tests covering the four reachability verdicts, the count invariant, the degrade oracle categories a–d, and DEGRADE-to-floor on backend loss.

**Exit Criteria:** module importable; `len(unreached_surfaces) == runtime_surface_unreached` holds in tests; floor-only path deterministic across repeated runs.

#### Phase 2 — Product wire

**Deliverables:**

- [ ] Invoke the sweep from `runner._audit_once` (post-launch, pre/merge `parse_contract` at `runner.py:445`); MERGE-overwrite the six fields into the just-authored contract; write the ledger to `<output>/artifacts/runtime-surface-ledger.yaml` via `_IndentDumper` + `_atomic_write_text`.
- [ ] Consumer wiring in `contract.py` (`_halted_reason` for UNREACHED, `_degraded_reason` for degraded); count-invariant malformed-contract guard.
- [ ] (Per OQ-DRS.2) Wave-1A skill shell-out wiring for the bare `claude -p` path.

**Exit Criteria:** deterministic six fields present on every runner-driven UC-2 run (REACHED/DEGRADE/UNREACHED alike); the §5.3 forbid-STOP pre-filter reads the deterministic `runtime_surface_unreached` scalar (AC-4, in-scope). The `sprint run` executor read is **NOT** an exit criterion of this phase — `cli/sprint/executor.py` reads no reflect contract today (research/03 §5.2/§5.3) and FR-DRS v1 does not wire it (deferred FR-006a).

#### Phase 3 — Eval wire

**Deliverables:**

- [ ] Locate the C-5 `evals.json` → `eval_metadata.json` materializer; route the same module into the eval harness/grader so the eval is deterministic and free of LLM variance.
- [ ] Any new oracle assertion type carries a `target` key (C-6 constraint) so it is actually graded.
- [ ] Verify the 5 FR-RSR cases (ids 37–41) pass deterministically across ≥3 repeated runs (AC-2).

**Exit Criteria:** AC-2 green with no variance across ≥3 runs.

#### Phase 4 — Prose demotion

**Deliverables:**

- [ ] Demote SKILL.md §6.1 step 4b/4b' to "the deterministic sweep computes these; narrate the verdict in REPORT.md"; LLM no longer hand-types the scalars on swept paths (LLM-fallback retained only for the bare path per R2).
- [ ] `make sync-dev` + `make verify-sync` clean.

**Exit Criteria:** AC-1 satisfied end-to-end; prose no longer the structured-emission producer where the sweep ran.

---

## 24. Release Criteria

### 24.1 Definition of Done

FR-DRS is complete when all six acceptance criteria (AC-1..AC-6, from spec §4) are met **plus** the project-hygiene gates:

- [ ] **AC-1** — On every UC-2 run, `runtime-surface-ledger.yaml` is written AND the six `runtime_surface_*` contract scalars are present with their exact canonical names — REACHED, DEGRADE, and UNREACHED paths alike — with zero dependence on LLM field emission.
- [ ] **AC-2** — The 5 FR-RSR eval cases (ids 37–41) pass deterministically across ≥3 repeated runs (no variance): unwired/test-only → UNREACHED + count invariant; positive-control → unreached 0, degraded false; dynamic-dispatch (registry) → degraded true, regression 0; degraded-backend → Grounding Gap, no STOP, no clean-pass.
- [ ] **AC-3** — `len(unreached_surfaces) == runtime_surface_unreached` holds **by construction** (computed, not asserted-on-LLM).
- [ ] **AC-4 (v1 in-scope portion)** — The §5.3 forbid-STOP pre-filter reads the deterministic scalars. *(The `sprint run` executor read of the deterministic scalars is **DEFERRED to FR-006a** — net-new integration, NOT a v1 Definition-of-Done criterion; `cli/sprint/executor.py` reads no reflect contract today, so there is nothing to wire this rollout. See §23 Phase-2 exit and synth-02 FR-006a.)*
- [ ] **AC-5** — Existing FR-RSR safety behavior (never clean-pass an unwired surface) is preserved.
- [ ] **AC-6** — `make verify-sync` clean; UV-only (no `python -m` / bare `pip` / `python script.py`); `ruff format --check` clean for the new module.

### 24.2 Release Checklist

- [ ] All four rollout phases (§23.2) complete per their exit criteria.
- [ ] `make verify-sync` clean (src/ ↔ .claude/ in sync after the SKILL.md demotion).
- [ ] `uv run ruff format --check src/ tests/` clean for the new module (note: `make lint` runs `ruff check` only; CI separately runs `ruff format --check` — run it explicitly before pushing).
- [ ] No new regression in the FR-RSR safety behavior (AC-5 spot-checked).
- [ ] OQ-DRS.1/.2/.3 ratified (recommendation accepted or amended) and recorded.

---

## 25. Operational Readiness

> **Light section — local-only tool, no production runtime.** FR-DRS is a pure-Python sweep that runs in-process during `superclaude reflect run` (or a bare skill invocation). There is **no service, no deployment surface, no on-call rotation, and no infrastructure** to operate.

- **Runbook:** none required as a service. The single operational failure mode is **backend/tooling unavailability** (ripgrep absent, LSP/Serena down) — handled in-band by DEGRADE-to-floor (R4): the affected edge degrades to §10.6 Grounding Gap, `degraded_components` gains `runtime-surface:backend_unavailable`, and the sweep continues with no global abort and NEVER STOPs. No human paging.
- **On-call:** not applicable — failures surface as a DEGRADE verdict in the reflect contract at run time, not as a production incident.
- **Capacity planning:** not applicable. The sweep is bounded by the diff size under audit (one pass over tagged surface symbols + their already-fetched step-4 referrers; no second referrer fetch). The non-surface fast path adds zero cost.

---

## 26. Cost & Resource Estimation

> **Light section — no infrastructure cost.** FR-DRS runs locally inside the reflect CLI / skill process. There is **no compute, storage, database, cache, or bandwidth cost** — no per-tenant or per-run cloud spend.

- **Infrastructure cost:** $0 — local-only, in-process Python.
- **Marginal runtime cost:** negligible — the sweep reuses the already-fetched step-4 `find_referencing_symbols` result (no extra referrer-fetch call), runs ripgrep over the local work-tree, and short-circuits to a zero-cost fast path on non-surface diffs.
- **Engineering cost:** the only material cost — a ~one-module greenfield implementation (HIGH complexity_class) plus product/eval wiring and the SKILL.md prose demotion, across the four phases in §23.

---

## Reuse & Consolidation Audit

> **Source:** `research/reuse-audit.yaml` (pre-stage advisory, reuse-auditor 2026-06-21), re-confirmed against live source in research 05. **Outcome:** no proposed component is a confident-duplicate. 5 of 6 are `distinct`; **entrypoint-rootwalk** is the single `reuse-by-import` (STRONGEST overlap, `S_reuse` 0.81) but is shape-divergent and must be **adapted, never dropped in**. Importing `cli/audit` is mechanically legal (the reflect import ban names `cli/sprint`/`cli/roadmap` ONLY) but couples reflect's product path to cleanup-audit semantics — the load-bearing boundary decision surfaced in §6.4 / §21 Alt 3 / §22.

| Proposed component | Nearest prior art (file:line) | Tier | Verdict | Disposition |
|--------------------|-------------------------------|------|---------|-------------|
| **surface-tagger** | `cli/audit/wiring_gate.py:164` (`_safe_parse`); `cli/audit/filetype_rules.py:7` (lang table); `cli/audit/dead_code.py:37` (hook-exclusions) | distinct (S_reuse 0.37) | **distinct** | Reflect-local. Reuse the small language-extension constants only after reconciling semantics + the fail-soft `return-None-on-parse-error` *pattern*. Audit helpers don't parse diff hunks, resolve hunk-local symbols, or detect Click/Typer/registry decorators. |
| **referrer-finder** | `cli/audit/dependency_graph.py:1,5,7` (3-tier static+grep, confidence labels); `tool_orchestrator.py:146` | maybe-related, shape-divergent (S_reuse 0.67) | **distinct** | Mirror the fail-open tier *shape* (AST-high / grep-medium, grep is the floor) but implement a **SYMBOL-level** finder locally — audit graph is FILE-level (`FileAnalysis`-keyed), too broad for symbol referrer + comment/test partitioning. Do NOT drop-in. **Distinct → cross-reference §6.4 / §21 Alt 2 / §22 OQ-DRS.1** (the structured-engine tier — LSP overlay vs AST floor — is an engine choice, not a reuse choice). |
| **partitioner** | `cli/audit/filetype_rules.py:10` (test markers); `filetype_rules.py:110-144` (`classify_file_type`, default-to-SOURCE at :143-144) | distinct (S_reuse 0.57) | **distinct** | Reflect-local. Reuse `_TEST_PREFIXES`/`_TEST_INFIXES` marker **LISTS as DATA only**; **invert the default** — audit defaults UNKNOWN/ambiguous→SOURCE; runtime-surface requires unknown/ambiguous→**DEGRADE**, plus inline-test scope + comment/docstring exclusion the audit classifier lacks. |
| **degrade-oracle** | `cli/audit/dynamic_imports.py:1,79` (`_DYNAMIC_PATTERNS`, scan; KEEP:monitor default); `cli/audit/dead_code.py:155` (entrypoint exclusion) | maybe-related (S_reuse 0.68) | **distinct** | Reuse the dynamic-import regex **pattern DATA** if convenient; implement the 4-category oracle (a–d) separately with its own verdict mapping — audit maps dynamic→KEEP:monitor (NOT DEGRADE), and audit entrypoint detection is filename-pattern, not `[project.scripts]`/entry-point *metadata* resolution. **Distinct → cross-reference §6.4 / §21 Alt 3 / §22** (the reflect→audit boundary applies to any DATA import too — recommend copy over import to keep the edge clean). |
| **entrypoint-rootwalk** | `cli/audit/reachability.py:1,374,591` (`ReachabilityAnalyzer`, `_bfs_reachable:591`); `:740` (scalar frontmatter) | maybe-related, shape-divergent (S_reuse **0.81**, STRONGEST) | **reuse-by-import** | **Adapt `_bfs_reachable:591` — do NOT drop-in.** The BFS skeleton (deque/visited/path) is small and stable, but the adaptation MUST (a) **enforce depth=1 at the call site** (the BFS internal is unbounded — no depth param), and (b) convert every partial-enumeration / dynamic-dispatch uncertainty to **DEGRADE**, not UNREACHED (reachability reports UNREACHABLE on dynamic dispatch and uses a depth>50 guard — both inverted). **Recommended v1: reflect-local copy (§6.4 D1 / §21 Alt 3 Option C)**, matching the `runner.py:14-17` copy-over-import precedent; extract a boundary-neutral helper (Option B) only if a second reflect graph-BFS consumer appears. |
| **ledger-writer** | `cli/reflect/ensemble.py:500` (`_emit_reflect_contract`); `cli/reflect/contract.py:65` (`parse_contract`); `cli/reflect/runner.py:66` (`_IndentDumper`) | distinct (S_reuse 0.56) | **distinct** | Reflect-local. Implement the `RuntimeSurfaceLedgerRow` type + per-symbol reduction + 6-scalar computation directly from `runtime-surface.md`. Reuse ONLY the generic YAML *style* — `_IndentDumper` (yamllint-safe nested sequences; `mem:reference_yamllint_indent_sequences_pyyaml`) + `_atomic_write_text` (both already reflect-local, zero boundary cost). NOT the ensemble's bare `yaml.safe_dump` + `path.write_text`. |

**Boundary note:** the single most load-bearing design decision is whether reflect imports from `cli/audit`. Mechanically legal, semantically coupling — surfaced as a Key Design Decision (§6.4 D1), an Alternative (§21 Alt 3), and an implicit open question, never a silent choice. Recommended posture across the board: **reflect-local copy / DATA-copy**, with boundary-neutral extraction as the long-term shape.

---

**Status:** Complete
