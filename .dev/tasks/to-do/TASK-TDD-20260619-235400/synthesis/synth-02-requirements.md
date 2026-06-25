# Synthesis 02 — §5 Technical Requirements (FR-RH2 Headless Ensemble Fix)

> **Source TDD section:** Template §5 (Technical Requirements) — `src/superclaude/examples/tdd_template.md` L293-359.
> **Feature:** FR-RH2 — drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library. Target release 4.4.0, HIGH complexity (0.82).
> **Derivation sources (all facts traced):**
>
> - `research/00-prd-extraction.md` — FR-RH2.1–.9 + NFR-RH2.1–.8 + (M,N) divergence guard table + CLI surface.
> - `research/01-reflect-runner-seam.md` — `_audit_once` seam, `ReflectResult` shape, NFR-7 isolation guards, diversity sourcing.
> - `research/03-swarm-dispatch.md` — `dispatch_wave1` contract, `WorkerResult` (M-over-N success predicate `status == "success"`).
> - `research/09-reflect-config-cli-surface.md` — `--transport` / `--reviewers` / `--depth` CLI wiring; `reflect-review` lens registration.
>
> No fabrication: every FR/NFR cites its originating FR-RH2.N / NFR-RH2.N. Where a requirement lacks a spec trace it is marked **[NO SPEC TRACE]** and flagged as a gap.

---

## 5. Technical Requirements

### 5.1 Functional Requirements

> Mapping note: the nine FR-001..FR-009 below are a 1:1 re-projection of the spec's FR-RH2.1..FR-RH2.9. The spec sequences FR-RH2.9 immediately after FR-RH2.4 (the N→M divergence contract is load-bearing for FR-RH2.4's diversity/reviewer_count semantics); this table keeps numeric order FR-001..FR-009 and maps FR-005→FR-RH2.9 so the source IDs read straight in the Source column. Acceptance Criteria are condensed from each FR's full criteria set in `00-prd-extraction.md §2`.

| ID | Requirement | Priority | Acceptance Criteria | Source |
|----|-------------|----------|---------------------|--------|
| FR-001 | Tier-2 reviewer ensemble forms via the **swarm dispatch library** (`ensemble.py` imports `dispatch_wave1` + per-slot transport factory in-process), **not** by a single `claude -p` agent fanning out reviewers via the Task tool. `superclaude swarm run --lens reflect-review` is the optional `--detached` observability variant, not the default inner-loop transport. | Must Have | Given `depth ∈ {standard,deep}` (expected tier 2), When `_audit_once` launches Tier-2, Then it invokes the swarm dispatch surface (`dispatch_wave1` / per-slot factory) and **no `Task(`/`subagent_type` fan-out** is introduced in `runner.py` or the new driver; each worker slot binds to a distinct external model (`T2Model0N`) via the per-slot factory; the Tier-1 grounded pass (`/sc:reflect` via `ClaudeProcess`) is **unchanged**. | FR-RH2.1 |
| FR-002 | A `reflect-review` swarm lens supplies per-reviewer reflection briefs (mirroring `lenses/bare_review.py`), framing each external worker as a heterogeneous reflection reviewer with `tier:"T2"`, `suspect:true`, and a `recommended_next_command_template` that hands normalized artifacts to `/sc:adversarial`. | Must Have | Given the bundled swarm-lens registry, When the `reflect-review` lens is loaded, Then it **passes the swarm lens validator** (same gate as `bare-review`, assertions 2 & 6 against `REGISTRY`/`STRATEGIES`); it emits `suspect:true` and a `recommended_next_command_template` containing `/sc:adversarial` with `{suspect_files}` substitution; `default_workers ∈ [2,4]`; the lens does **not** hard-code a Claude model (models come from the `T2Model0N` env pool, not `spec.workers.models`). | FR-RH2.2 |
| FR-003 | Swarm normalized per-reviewer artifacts (the N `final_path`s) are scored by reflect's existing **`sc-adversarial-protocol` Mode A merge** — swarm's `mechanical_merge` (`merge.py`) output MUST NOT be treated as the adversarial verdict. **(Blocked by OI-1: the swarm `ResultContract`→reflect-contract field-correspondence table must be resolved BEFORE this code lands.)** | Must Have | Given N normalized per-reviewer `final_path` artifacts (suspect-aware), When the downstream merge runs, Then it consumes those artifacts as Mode A input; **no scoring/ranking/dedup logic is added to `swarm/merge.py`** (LOC ceiling + boundary tests stay green); the adversarial merge produces a convergence score recorded on the reflect contract. | FR-RH2.3 |
| FR-004 | A faithful (non-mocked) Tier-2 run yields a real adversarial merge with ≥2 distinct model classes, surfacing in `return-contract.yaml`: `tier_reached:2`, `merge_method != single-reviewer-fallback`, `reviewer_count ≥ 2`, `t2_model_class_diversity:full`. Diversity & reviewer_count are measured over **succeeded workers M**, not requested slots N. | Must Have | Given a successful Tier-2 run, Then `tier_reached == 2` AND `merge_method != "single-reviewer-fallback"` AND `reviewer_count == M ≥ 2` (M = count of `WorkerResult`s with `status=="success"`) AND `t2_model_class_diversity == "full"` computed over the **distinct `model_id`s of the M succeeded workers** (≥ expected distinct-class count) — two survivors of the same class do NOT count as `full`. | FR-RH2.4 |
| FR-005 | **Faithful run signals + N→M divergence boundary** — the contract for an honest Tier-2 pass and the boundary that derives the verdict for any (M,N): M≥2 with ≥2 distinct classes → faithful (PASS-eligible); M≥2 but <2 distinct classes → `degraded` (`degraded-model-diversity`); M==1 → `degraded` (`single-reviewer-fallback`) and/or `tier_reached:1`; M==0 → `blocked` (`ensemble-empty`, ordered ahead of degraded). | Must Have | Given a `--reviewers 3` run with exactly one worker `proxy_error` after retry (M==2), Then PASS-eligible **iff** the 2 survivors are ≥2 distinct model classes else `degraded-model-diversity`; Given an M==1 outcome (from `--reviewers 1` OR N>1 with N−1 failures), Then `single-reviewer-fallback` and/or `tier_reached==1` (non-PASS); Given M==0, Then route `blocked` (exit 2), not `degraded`. Worker-status→M: only `success` counts; `proxy_error`/`timeout`/`parse_error` do not. | FR-RH2.9 |
| FR-006 | **Credit-free stub proof** — a `--transport stub` (`transports/stub.py`) variant drives the **real** wrapper (unmocked `dispatch_wave1`/`reduce_wave3`) over a deterministic network-free transport and asserts the FR-004 acceptance signals, proving ensemble formation in CI without burning proxy credits. | Must Have | Given a test running the real reflect Tier-2 driver with `--transport stub`, Then it performs **zero network I/O** and asserts `tier_reached==2`, `merge_method != single-reviewer-fallback`, `reviewer_count>=2`, `t2_model_class_diversity=="full"`; the test does **not** patch `ClaudeProcess` to copy a canned `tier_reached:2` fixture — it exercises the real fan-out→reduce path. | FR-RH2.5 |
| FR-007 | **One-reviewer negative witness** — a run configured with a single reviewer MUST NOT satisfy the Tier-2 pass signals; it MUST degrade, proving the FR-006 proof is falsifiable and cannot pass vacuously. | Must Have | Given a 1-reviewer stub run, Then `merge_method == "single-reviewer-fallback"` and/or `tier_reached == 1` (non-PASS Tier-2); AND the **same assertions** used in the positive FR-006 test FAIL for the 1-reviewer case (witness is genuinely negative). | FR-RH2.6 |
| FR-008 | **Return-contract shape preserved** — `return-contract.yaml` shape + the derived `reflect_post:` write-back + `wrapper-result.yaml` sidecar remain compatible; the 4-state verdict map and exit codes (`contract.py`, `models.py`) are unchanged. | Must Have | Given the post-fix codebase, Then `derive_verdict` + the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged; `write_reflect_post` produces the same `reflect_post:` field set/order and the sidecar keeps its fields; existing reflect contract/verdict tests pass **without modification**. | FR-RH2.7 |
| FR-009 | **NFR-7 preserved or amended on the record** — the change introduces no `Task(`/`subagent_type` fan-out into the reflect package; the author confirms whether spawning swarm/proxy workers is within the NFR-7 guard's exact scope (`test_no_nesting_guard.py`), amending NFR-7 **deliberately and explicitly** (never silently) if the guard scope must recognize the swarm-driven path. | Must Have | Given `test_no_nesting_guard.py` (Layer B: no `Task(`/`subagent`/`anthropic` imports in `runner.py`), Then it passes including for the new driver module; If NFR-7 prose/scope is amended, Then the amendment is recorded in the spec (§9) and reflected in the guard's docstring/assertions with rationale; **no raw `subprocess.run`/`Popen`** is added to the reflect package (the swarm call goes through the swarm CLI surface / `ClaudeProcess`, not a hand-rolled `Popen`). | FR-RH2.8 |

**Spec-trace coverage:** All 9 functional requirements (FR-001..FR-009) carry an FR-RH2.N source. **No `[NO SPEC TRACE]` gaps in §5.1** — every FR maps to exactly one spec FR (FR-RH2.1..FR-RH2.9; FR-005↔FR-RH2.9, FR-008↔FR-RH2.7, FR-009↔FR-RH2.8 per the source ordering note).

**Open Item dependency (carried from spec §11):** FR-003 (FR-RH2.3) is **gated by OI-1**, the BLOCKING GATE — the swarm `ResultContract` field → reflect contract field correspondence table must be produced and resolved before any FR-003 code lands; it sizes the `ensemble.py` mapping layer. This is a sequencing constraint, not a missing trace.

---

### 5.2 Non-Functional Requirements

> Each NFR below carries an explicit **measurement method** (the column the template §5.2 requires). All eight map 1:1 to the spec's NFR-RH2.1..NFR-RH2.8 (`00-prd-extraction.md §3`). No `[NO SPEC TRACE]` gaps.

#### 5.2.1 No in-process Task/Agent fan-out in the reflect package (NFR-7 preserved)

| Attribute | Detail |
|-----------|--------|
| **Requirement** | Zero `Task(` / `subagent_type` fan-out anywhere in the reflect package — including the **new `ensemble.py` driver**. The Tier-2 ensemble forms via the swarm dispatch library (`dispatch_wave1` → `ParallelExecutor` → `Transport`), never via an Agent/Task surface. |
| **Target** | No `Task(` / `subagent_type` token in `runner.py` **or** `ensemble.py`. |
| **Measurement method** | `test_no_nesting_guard.py` Layer B, **extended to cover `ensemble.py`** (anchored regexes for `Task(`/`subagent`/`anthropic` imports). Green = pass. |
| **Source** | NFR-RH2.1 (preserves NFR-7) |

#### 5.2.2 Thinness / isolation (NFR-1) preserved

| Attribute | Detail |
|-----------|--------|
| **Requirement** | The reflect package stays thin and isolated: **no `cli.sprint` / `cli.roadmap` import**, **no `async`/`await`**, **no raw `subprocess.run`/`Popen`**. The swarm reuse is import-and-compose of synchronous `def`s (`dispatch_wave1`, `_resolve_run_transport_factory`/`read_env`, `reduce_wave3` — all verified sync in `03-swarm-dispatch.md` / `01-reflect-runner-seam.md`), adding no event loop and no hand-rolled subprocess to the launch path. |
| **Target** | Zero matches for the forbidden import/async/subprocess anchors in the reflect package. |
| **Measurement method** | `test_no_nesting_guard.py` import/async/subprocess anchored regexes (the same guard that today verifies `runner.py` L8-12 isolation), extended to `ensemble.py`. |
| **Source** | NFR-RH2.2 (preserves NFR-1) |

#### 5.2.3 Non-vacuous ensemble proof

| Attribute | Detail |
|-----------|--------|
| **Requirement** | The ensemble-formation proof is non-vacuous: a **positive witness (≥2 reviewers → faithful Tier-2)** and a **falsifying witness (1 reviewer → degrade)**, both exercising the **real** fan-out→reduce path (not a patched/canned fixture). |
| **Target** | Positive test asserts FR-004 signals and passes; the identical assertions FAIL for the 1-reviewer negative case. |
| **Measurement method** | `test_ensemble_stub_integration.py` — positive (`--reviewers ≥2`) + negative (`--reviewers 1`) cases over the real driver with `--transport stub`. |
| **Source** | NFR-RH2.3 (realizes FR-RH2.5 + FR-RH2.6) |

#### 5.2.4 Credit-free CI

| Attribute | Detail |
|-----------|--------|
| **Requirement** | The Tier-2 ensemble proof performs **zero network I/O** — CI proves ensemble formation without burning proxy credits via the deterministic `--transport stub` lane. |
| **Target** | The `--transport stub` test imports no httpx wire path and runs fully offline. |
| **Measurement method** | Assert the stub test imports no `httpx`/wire transport; run offline (no `:4000` / proxy connection). `--transport stub` selected (default for the CI lane per OI-3 once decided). |
| **Source** | NFR-RH2.4 |

#### 5.2.5 Model-class diversity full when pool ≥ reviewers

| Attribute | Detail |
|-----------|--------|
| **Requirement** | `t2_model_class_diversity == "full"` whenever the available model pool has ≥ `--reviewers` distinct models. Diversity is computed over the **distinct `model_id`s of the M succeeded workers** (success predicate `status == "success"`, per `dispatch.py` L496), never over the N requested slots. |
| **Target** | When pool ≥ requested reviewers and all resolve to distinct classes, contract reports `t2_model_class_diversity:full`; when survivors collapse onto one class, `degraded-model-diversity`. |
| **Measurement method** | Assert distinct `model_id` count in the swarm `WorkerResult`s (M succeeded) ≥ expected distinct-class count. |
| **Source** | NFR-RH2.5 |

#### 5.2.6 Backward compatibility

| Attribute | Detail |
|-----------|--------|
| **Requirement** | Existing reflect contract / verdict / runner tests pass **unchanged**; field names, the 4-state verdict map, and exit codes (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are preserved. The Tier-1 grounded pass and `run()` loop / write-back (`write_reflect_post`, `write_sidecar`) keep working with the seam routed only inside `_audit_once` (branch on `expected_tier`). |
| **Target** | `tests/cli/reflect` suite green with no modifications to existing tests. |
| **Measurement method** | `uv run pytest tests/cli/reflect -q` green. |
| **Source** | NFR-RH2.6 (realizes FR-RH2.7) |

#### 5.2.7 Observability

| Attribute | Detail |
|-----------|--------|
| **Requirement** | Headless Tier-2 runs are pollable: the `t2-swarm` subrun supports `--detached`/tmux, writes a `done.json` sentinel, and exposes `--tui`. (`superclaude swarm run --lens reflect-review` is the optional `--detached` observability variant of FR-001's in-process default.) |
| **Target** | A headless Tier-2 run can be polled mid-flight and its terminal state read from the sentinel. |
| **Measurement method** | Verify swarm `--detached`/tmux + `done.json` sentinel + `--tui` are available for the t2-swarm subrun. |
| **Source** | NFR-RH2.7 |

#### 5.2.8 Proxy contract respected

| Attribute | Detail |
|-----------|--------|
| **Requirement** | Workers use **only** the `:4000/cli` base + `T2Model01..NN` models per `~/.aienv`. No probing of `:4000/v1`, `:8317`, or the proxy API for models. |
| **Target** | All Tier-2 worker transports resolve base/model from `read_env` against `~/.aienv`; no other endpoint contacted. |
| **Measurement method** | `read_env` preflight (`swarm/transports/openai_compat.py` L159); assert no `:4000/v1` / `:8317` probe in the transport path. |
| **Source** | NFR-RH2.8 |

**NFR spec-trace coverage:** All 8 non-functional requirements (5.2.1..5.2.8) carry a NFR-RH2.N source with an explicit measurement method. **No `[NO SPEC TRACE]` gaps in §5.2.**

---

### 5.3 CLI Surface (input contract for §5.1)

> The FR-RH2 input-mutation surface is a three-file chain in `src/superclaude/cli/reflect/` (`commands.py` Click option → `config.py` `resolve_config` → `models.py` `ReflectConfig` dataclass tail), per `09-reflect-config-cli-surface.md`. `--depth` already exists; `--transport` / `--reviewers` are net-new.

```
superclaude reflect run <tasklist> --depth {standard|deep}
    [--transport {openai_compat|stub}]   # default: openai_compat (live proxy); stub = credit-free CI
    [--reviewers <N>]                     # clamp [2,4]; default 3; 1 => negative-witness degrade
    [--allow-single-vendor]               # unchanged FR-11 suppression
    [--fix] [--promote] [--resume] [--dry-run] [--print-command]
```

| Option | Type | Default | Behavior |
|--------|------|---------|----------|
| `--transport` | enum `{openai_compat, stub}` | `openai_compat` | Tier-2 worker transport. `openai_compat` = external proxy (`T2Model0N`); `stub` = deterministic, network-free, credit-free CI lane (FR-006). **Unknown value rejected at Click parse** before any dispatch (non-zero exit, no partial run). Net-new — copy the `--depth` `click.Choice` idiom. |
| `--reviewers` | int | `3` | Tier-2 reviewer slots; **clamped to `[2,4]`** in `resolve_config`. `1` is the negative-witness sentinel → degrade (FR-007); it MUST be branched **before** the clamp or it gets rewritten to `2`. Net-new. |
| `--depth` | enum `{standard, deep}` | `standard` | **Already exists** (`commands.py:101-106`); MUST NOT be re-added. Tier-2 expected for both; `quick` floors to `standard`. `expected_tier` derived at `runner.py:403` (both depths → 2). |

### 5.4 (M,N) Divergence Guard Table (verdict derivation)

> M = succeeded workers (`status=="success"` only), N = requested slots. Reproduced from spec §5.3 `mn_guard_table` via `00-prd-extraction.md §5`. Verdict ordering in `derive_verdict`: `blocked → degraded → halted → pass`.

| M-condition | verdict | exit-code | reason-slug |
|-------------|---------|-----------|-------------|
| `M==0` (all workers failed / no artifacts) | `blocked` | `2` | `ensemble-empty` |
| `M==1` (≥N−1 failed, or `--reviewers 1`) | `degraded` | `11` | `single-reviewer-fallback` |
| `M≥2` but `<2` distinct model classes | `degraded` | `11` | `degraded-model-diversity` |
| `M≥2` AND `≥2` distinct classes | `pass-eligible` | `0` | `pass` |

**Worker-status → M mapping:** `success` counts; `proxy_error` / `timeout` / `parse_error` do NOT (post-salvage status governs for `parse_error`).

**Path-confinement invariant:** TWO `return-contract.yaml` files exist — `<output_dir>/return-contract.yaml` (the ONLY file `reflect.derive_verdict` parses) and `<output_dir>/t2-swarm/return-contract.yaml` (swarm subrun, consumed by `ensemble.py` only). Reflect MUST NOT parse the `t2-swarm/` subdir contract directly.

---

**Status: Complete** — §5.1 (9 FRs, all spec-traced, priorities + GWT acceptance criteria), §5.2 (8 NFRs, all spec-traced with measurement methods), plus §5.3 CLI surface and §5.4 (M,N) guard table as supporting input/verdict contracts. No fabrication; no `[NO SPEC TRACE]` gaps.
