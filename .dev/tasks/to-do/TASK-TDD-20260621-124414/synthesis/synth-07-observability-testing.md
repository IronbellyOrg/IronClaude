## 14. Observability & Monitoring

> **Note:** FR-DRS is a **local, deterministic Python sweep** invoked inside the reflect CLI / eval harness — not a long-running service. There is **no metrics backend, no tracing infra, no alerting, and no dashboards**. The observable artifacts are entirely file-based: the ledger and the six contract scalars. This section is intentionally light; the load-bearing observability for FR-DRS lives in §15 (Testing Strategy) and in the contract itself.

### 14.1 Observable Artifacts

The only runtime-observable outputs are two file-based artifacts, both produced deterministically by `runtime_surface.py` on every UC-2 run (AC-1).

| Artifact | Path | Producer | Content | When written |
|----------|------|----------|---------|--------------|
| Runtime-surface ledger | `<output>/artifacts/runtime-surface-ledger.yaml` | `runtime_surface.py` (emit step 7) | One `RuntimeSurfaceLedgerRow` per evaluated edge (symbol → referrer → verdict) | **Always**, on REACHED / DEGRADE / UNREACHED alike (AC-1) |
| Contract scalars (6 fields) | `<output>/return-contract.yaml` (6 keys merged in) | `runtime_surface.py`, written via `_IndentDumper` + `_atomic_write_text` | The six `runtime_surface_*` group fields, computed from ledger rows | Always; before `parse_contract` reads it (research 02) |

The ledger is the **forensic record**: it is the per-edge audit trail that explains *why* each symbol reduced to its verdict. Where prose-FR-RSR wrote the ledger in only 1/9 quiet-path runs (research 00 §3), FR-DRS writes it by construction every run, making the ledger a reliable observability surface for the first time.

### 14.2 The Six Contract Scalars (the observable contract surface)

These six fields ARE the monitoring surface — a consumer or operator inspects them to understand the sweep's outcome. Names are canonical and verbatim (research 03 §1; SKILL.md §9.1 lines 731–736).

| # | Field | Type | Observability meaning |
|---|-------|------|----------------------|
| 1 | `runtime_surface_requirements` | `[str]` | Which surface requirement ids were tagged; `[]` = no surfaces in diff |
| 2 | `runtime_surface_sweep_ran` | `bool` | `true` only when ≥1 tagged surface triggered the sweep |
| 3 | `runtime_surface_ledger_path` | `abs path \| null` | Pointer to the forensic ledger; `null` when sweep did not run |
| 4 | `runtime_surface_unreached` | `int` | Count of UNREACHED symbols; **drives §5.3 pre-filter** |
| 5 | `runtime_surface_degraded` | `bool` | `true` when ≥1 symbol DEGRADEd (→ §10.6 Grounding Gap) |
| 6 | `unreached_surfaces` | `[UnreachedSurface]` | One entry per UNREACHED symbol; member set is the diagnostic |

**Count invariant (the self-observable consistency check):** `len(unreached_surfaces) == runtime_surface_unreached` holds **by construction** (AC-3) because both are computed from the same ledger rows — not asserted on an LLM emission. The grader independently re-checks it (§15.4).

### 14.3 Logging / Diagnostics

| Diagnostic | Channel | Notes |
|------------|---------|-------|
| `degraded_components` (tool-loss) | Contract field + ledger row reason | Set when referrer engine falls back grep-on-LSP-loss (research 00 §5 step 2) |
| Grounding Gap rows | REPORT.md (LLM-narrated) + `runtime_surface_degraded: true` | DEGRADE verdict surfaced for human decision (`needs_human_decision: true`) |
| Sweep-incompleteness signal | `runtime_surface_degraded: true` (NOT `child_rc`) | Tier-2 hardcodes `rc=0`; incompleteness must signal via degrade, not exit code (research 02 Q2) |

> **Note:** There is no `runtime_surface` metric counter and no `deviation_count_by_class.runtime_surface` key. UNREACHED is **not a 5th deviation class** (research 03 §4) — its blocking signal flows through the existing `deviation_count_by_class.regression` / `.drift` counters. Nothing new to instrument on the deviation-counter surface.

---

## 15. Testing Strategy

> **CRITICAL:** §15 is the central section of this TDD. FR-DRS's entire reason to exist is that a prose-only LLM implementation could **not** deliver deterministic structured output (research 00 §3: ad-hoc field names persisted, ledger written 1/9 runs). The testing strategy therefore proves two properties: (1) the module computes each verdict correctly at the unit level, and (2) the 5 FR-RSR eval cases pass **deterministically across ≥3 repeated runs with zero variance** (AC-2). Determinism is the acceptance bar, not coverage percentage.

### 15.1 Test Pyramid

| Level | Scope | Tool | Coverage target | Determinism requirement |
|-------|-------|------|-----------------|-------------------------|
| **Unit** | Each of the 6 logical units of `runtime_surface.py` (tagger, referrer-finder, partitioner, degrade-oracle, rootwalk, reducer) | `uv run pytest` | > 90% (pure functions, no LLM, no network) | Identical input → identical output, asserted directly |
| **Integration** | The 5 FR-RSR uc2 eval cases (ids 37–41) end-to-end through the grader | `superclaude reflect run` eval harness + `grader.py` | All 5 cases pass | **Zero variance across ≥3 repeated runs (AC-2)** |
| **Contract / invariant** | `len(unreached_surfaces) == runtime_surface_unreached` | `uv run pytest` (unit, by construction) + `grader.py:191` `check_yaml_list_len_eq` (integration re-check) | Holds every run (AC-3) | By construction in the reducer; re-asserted in grader |
| **Sync / lint** | `make verify-sync`, `ruff format --check`, UV-only | `make`, `uv run ruff` | Clean (AC-6) | N/A |

There is **no E2E, performance, or security tier** for FR-DRS — it is a pure local function with no UI, no service, no auth surface. Those template rows are intentionally omitted.

### 15.2 Unit Tests — the 6 logical units

Each unit is a pure function; tests feed a fixed input and assert the exact output. The **count invariant is asserted at the reducer/emit unit by construction** — the reducer derives `runtime_surface_unreached` as `len([rows reduced to UNREACHED])`, so the scalar and the list cannot disagree.

| # | Unit | Responsibility | Representative unit test | Expected result |
|---|------|----------------|--------------------------|-----------------|
| 1 | **tagger** | Tag surface symbols from diff hunks by resolved kind/decorator vs allowlist (py/rust/ts/js/go; others DEGRADE) | Feed a diff adding a decorated `/ai` handler | Symbol tagged with its `runtime_surface_requirements` id; unknown-lang symbol → DEGRADE-tagged |
| 2 | **referrer-finder** | Find referrers of each tagged symbol (ripgrep/AST floor; LSP/Serena optional); fail-open to grep + `degraded_components` on tool loss | Symbol with 2 production callers + 1 test caller | 3 referrer edges found; tool-loss path sets `degraded_components` |
| 3 | **partitioner** | Split referrers into production vs test/comment via lang→(test-marker, comment) table | Mixed referrer set incl. inline-test module | Production/test classification matches table; inline-test counted as test |
| 4 | **degrade-oracle** | Categories a–d (decorator routes; `[project.scripts]`/entry-points; registry/DI/string-dispatch; reflection/dynamic-import) → DEGRADE | `[project.scripts]`-wired entrypoint (case 39 shape) | Verdict DEGRADE, `runtime_surface_degraded: true`, NOT UNREACHED, NOT Regression |
| 5 | **rootwalk** | Entrypoint rootwalk depth=1: REACHED if reachable from any enumerated root; partial enumeration → DEGRADE | Symbol reachable from a CLI root (case 38 shape) | Verdict REACHED, `unreached: 0` |
| 6 | **reducer** | Per-edge → per-symbol verdict under `DEGRADE-on-incompleteness > UNREACHED > REACHED`; **compute the 6 scalars from ledger rows** | Symbol with only test/comment referrers (case 41 shape) | Verdict UNREACHED; `runtime_surface_unreached == 1`; `len(unreached_surfaces) == 1` **asserted by construction** |

**Count-invariant unit assertion (AC-3):** a dedicated reducer test constructs ledger rows with N symbols reduced to UNREACHED and asserts `len(result.unreached_surfaces) == result.runtime_surface_unreached == N` for N ∈ {0, 1, 2}. Because the reducer computes both from the same row set, this is a by-construction guarantee, not a check against an LLM scalar.

**Command:**
```
uv run pytest tests/cli/reflect/test_runtime_surface.py -v
```

### 15.3 Integration Tests — the 5 FR-RSR uc2 eval cases (AC-2)

The integration tier runs the 5 `case_dir`-backed cases (evals.json ids 37–41, `cases/uc2-*/`) through the eval harness, where **the grader invokes the SAME `runtime_surface.py` module** the product path uses (research 00 §4.2; spec §2 eval path). This is what makes the eval deterministic and free of LLM variance — both operands of every assertion are module-computed, not LLM-emitted.

| id | Case | Verdict under test | Key assertions (research 04 §3) | Expected |
|----|------|--------------------|--------------------------------|----------|
| 37 | `uc2-unwired-surface-passes` | UNREACHED (headline FAIL-pre / PASS-post) | `old_skill` clean-passes; `with_skill` `runtime_surface_unreached >= 1` + Regression; no clean-pass | unreached 1, regression 1, tier 2 |
| 38 | `uc2-surface-positive-control` | REACHED (no-fire control) | `runtime_surface_unreached == 0`, `runtime_surface_degraded == false`, no UNREACHED/STOP | all-zero, tier 1 |
| 39 | `uc2-surface-dynamic-dispatch` | DEGRADE (registry/`[project.scripts]`) | `runtime_surface_degraded == true`, `unreached == 0`, **no Regression** | degraded true, regression 0, tier 1 |
| 40 | `uc2-surface-degraded-backend` | DEGRADE (`backend:none`) | `degraded == true`, Grounding Gap present, **no STOP**, **no clean-pass** | degraded true, status partial, tier 1 |
| 41 | `uc2-surface-test-only-ref` | UNREACHED (count-invariant host) | `runtime_surface_unreached >= 1`; **`yaml_list_len_eq` count invariant**; UNREACHED surfaced | unreached 1, regression 1, tier 2 |

**Determinism acceptance bar (AC-2):** each case must produce **byte-identical** verdicts across **≥3 repeated runs with zero variance**. The test driver runs the harness 3× and asserts the per-case grading.json is identical run-to-run. This is the criterion the prose-only implementation failed (case dynamic-dispatch was 0/3→1/3 before — research 00 §3).

**Commands:**
```
# Run the eval harness over an iteration dir (grader invokes runtime_surface.py)
uv run python .dev/eval-workspaces/sc-reflect/grader.py <iterations/iteration-N/>

# Repeat-run determinism gate (3 iterations, assert zero variance)
uv run pytest tests/cli/reflect/test_runtime_surface_eval_determinism.py -v
```

> **Note (carry-forward C-5 — UNVERIFIED dependency):** the grader reads per-eval `eval_metadata.json` (grader.py:440–446), NOT `evals.json` directly. The step that **materializes `evals.json` → per-eval `eval_metadata.json`** (and copies `cases/uc2-*/expected.yaml` + `input/` into `iterations/iteration-N/eval-<name>/`) was **not located in the research and is unverified**. The integration test plan assumes this materializer exists and runs before the grader. If FR-DRS's eval-path wiring (Option B — runner materializes the contract's 6 fields) is to hook in upstream of grading, it likely lives in this unlocated materializer. **This dependency must be verified during implementation.**

### 15.4 Contract / Invariant Test — `check_yaml_list_len_eq`

The count invariant is enforced at two layers:

| Layer | Mechanism | What it proves |
|-------|-----------|----------------|
| Producer (unit) | reducer computes both scalars from one row set | Invariant holds **by construction** (AC-3) — cannot diverge |
| Grader (integration) | `check_yaml_list_len_eq` at **grader.py:191** | Re-asserts `len(unreached_surfaces) == runtime_surface_unreached` reading `with_skill/outputs/contract.yaml` (`list_field: unreached_surfaces`, `count_field: runtime_surface_unreached`) — case 41's assertion 2 |

`check_yaml_list_len_eq` parses the contract with `yaml.safe_load`, reads the two named fields, and passes iff length == value (research 04 §2). Its signature is unchanged by FR-DRS — it is agnostic to whether the fields were written by the LLM (before) or the deterministic module (after). FR-DRS makes **both of its operands trustworthy** (module-computed), upgrading it from a self-consistency gate to a meaningful correctness gate.

> **CRITICAL (carry-forward C-6 — target-prefix routing fragility):** `grade_eval` buckets assertions into the `with_skill` / `old_skill` configs **solely** by `assertion.get("target", "").startswith("with_skill/" | "old_skill/")` (**grader.py:448–449**). An assertion that omits a `target` key (as `citation_resolves` / `checkpoint_logged` do) falls into **neither bucket and is silently never graded**. The 5 current uc2 cases are safe (every assertion carries a `target`), and `yaml_list_len_eq` carries `target` (the contract.yaml path). **Therefore: any new FR-DRS oracle assertion type (e.g. a deterministic-reachability check comparing the module's ground truth to the contract) MUST carry a `target` key prefixed `with_skill/` (or extend the bucketing logic), or it will never run.** This is a load-bearing constraint on the eval-path integration.

### 15.5 Test Environments

| Environment | Purpose | Data | Notes |
|-------------|---------|------|-------|
| Local (UV) | Unit + determinism eval | The 5 `cases/uc2-*/` fixtures (`input/diff.patch` + `input/tasklist.md` + `expected.yaml`) | UV-only (AC-6); no network, no LLM in the sweep path |
| CI | Sync + lint + full suite | Same fixtures | `make verify-sync` clean, `ruff format --check` clean for the new module (AC-6) |

### 15.6 Coverage of Acceptance Criteria

| AC | Covered by |
|----|-----------|
| AC-1 (ledger + 6 fields always emitted) | §15.2 reducer/emit unit tests; §14.1 always-write artifact |
| AC-2 (5 cases deterministic ≥3 runs, zero variance) | §15.3 integration determinism gate |
| AC-3 (count invariant by construction) | §15.2 reducer count-invariant unit test; §15.4 grader re-check |
| AC-4 (§5.3 pre-filter + sprint executor read deterministic scalars) | Consumer-side; producer determinism is the precondition (see consumer surfaces — note sprint executor is SPEC-ONLY today, research 03 §5) |
| AC-5 (never clean-pass an unwired surface preserved) | §15.3 case 37 (FAIL-pre/PASS-post) + case 41 |
| AC-6 (verify-sync, UV-only, ruff format clean) | §15.1 sync/lint tier |
