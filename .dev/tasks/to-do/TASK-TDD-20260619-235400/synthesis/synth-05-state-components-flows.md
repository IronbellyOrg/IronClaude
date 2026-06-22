# Synthesis 05 — §9 State Management / §10 Component Inventory / §11 User Flows (FR-RH2 Headless Ensemble Fix)

- **Feature:** FR-RH2 — drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library (headless ensemble fix)
- **Target release:** 4.4.0 | **Complexity:** HIGH (0.82)
- **Source research:** `research/00-prd-extraction.md` (the (M,N) table), `01-reflect-runner-seam.md`, `03-swarm-dispatch.md`, `05-swarm-reduce-merge-contract.md`, `08-precedents-adversarial-handoff.md`
- **Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`
- **Status:** Complete

> **Evidence rule:** Every flow step and verdict-branch value below is grounded in a `[CODE-VERIFIED]` finding from the research set (line numbers re-verified against shipped source). NET-NEW components (`ensemble.py`, the `reflect-review` lens) are marked as such; their behavior is grounded against verified precedents. The (M,N) branch values are reproduced verbatim from the spec's `mn_guard_table` (`00-prd-extraction.md` §5).

---

## 9. State Management

**N/A — backend CLI library, no client surface.**

**Rationale:** FR-RH2 is a Python CLI/library change inside `src/superclaude/cli/reflect/` (the new `ensemble.py` driver) composing the `src/superclaude/cli/swarm/` dispatch library in-process. There is no frontend, no browser/client runtime, and no UI state to manage (no TanStack Query / Redux / Zustand / URL / form state). The reflect package's hard isolation rules forbid even an event loop — `runner.py` L8-12 mandate zero `async def`/`await` and the ONLY launch path being a synchronous subprocess/in-process call (`01-reflect-runner-seam.md`). The TDD template marks §9 as conditional: *"This section applies to frontend/client-side components. Backend services, infrastructure, and libraries should skip this section entirely"* (`tdd_template.md` L580). What would loosely resemble "state" here — the reviewer fan-out result, the verdict, the deviation counts — is not client state; it is data serialized to two on-disk YAML artifacts (`return-contract.yaml` and the `reflect_post:` frontmatter block / `wrapper-result.yaml` sidecar) and consumed by `derive_verdict`. That data and its lifecycle are documented in §7 (Data Models) and §11 (User Flows), not here.

---

## 10. Component Inventory

**N/A — backend CLI library, no client surface.**

**Rationale:** There are no pages, routes, React/UI components, or component hierarchy in this feature. The deliverable units are Python modules and a swarm lens, not UI components: the NET-NEW in-process driver `cli/reflect/ensemble.py`, a NET-NEW `reflect-review` lens (mirroring `cli/swarm/lenses/bare_review.py`), and the existing reflect runner seam (`_audit_once`, `runner.py` L392-428) that routes Tier-2 through the driver. These are catalogued as code modules in §6 (Architecture / Component Diagram), with their public call contracts in §8 (API Specifications) — `dispatch_wave1(...) -> list[WorkerResult]` (`dispatch.py` L334), `reduce_wave3(...) -> ResultContract` (`reduce.py` L555). The TDD template scopes §10 to *"frontend/client-side components … Backend services, infrastructure, and libraries should skip this section entirely"* (`tdd_template.md` L624). A frontend component inventory (page/route table, shared-component table, App→Layout→Pages tree) has no referent in a headless CLI library.

---

## 11. User Flows & Interactions

The "user" here is an operator at the shell (or a CI lane) invoking `superclaude reflect run`. The flow is a headless pipeline; "interactions" are CLI-flag inputs and on-disk artifact outputs. There is exactly one primary flow (the faithful Tier-2 run) and a set of error/degradation branches driven entirely by **(M,N)** — M = succeeded reviewer workers, N = requested reviewer slots.

### 11.1 Primary User Flow: Faithful Tier-2 Reflection Run (`--depth deep`)

```mermaid
sequenceDiagram
    actor Op as Operator / CI
    participant CMD as reflect commands.py<br/>(CLI entry, L148-249)
    participant RUN as runner.py<br/>_audit_once (L392-428)
    participant T1 as ClaudeProcess<br/>(Tier-1 grounded pass)
    participant ENS as ensemble.py<br/>(NET-NEW driver)
    participant LENS as reflect-review lens<br/>(NET-NEW)
    participant DISP as swarm dispatch_wave1<br/>(dispatch.py L334)
    participant POOL as Per-slot transport<br/>T2Model01..0N (proxy / stub)
    participant RED as swarm reduce_wave3<br/>(reduce.py L555)
    participant ADV as /sc:adversarial<br/>Mode A (--compare)
    participant VRD as contract.py<br/>parse_contract + derive_verdict
    participant OUT as write_reflect_post (L117)<br/>+ write_sidecar (L188)

    Op->>CMD: superclaude reflect run <tasklist> --depth deep<br/>[--transport openai_compat|stub] [--reviewers N]
    CMD->>RUN: run() → loop calls _audit_once()
    Note over RUN: expected_tier = 2 (depth in {standard,deep}) @ L403

    rect rgb(235,245,255)
        Note over RUN,T1: Tier-1 grounded pass — UNCHANGED (FR-RH2.1 AC)
        RUN->>T1: ClaudeProcess(/sc:reflect, --tools default)
        T1-->>RUN: grounded baseline reflection (existing reviewer artifact)
    end

    rect rgb(235,255,235)
        Note over RUN,RED: Tier-2 ensemble — NET-NEW seam (expected_tier==2 branch @ L405)
        RUN->>ENS: ensemble.run(config, base, existing_artifact)
        ENS->>LENS: build per-reviewer reflection briefs<br/>(tier:T2, suspect:true)
        ENS->>DISP: dispatch_wave1(preflight, transport_for_slot=λi→T2Model0(i), prompt, worker_spec, logger)
        DISP->>POOL: fan N slots via ParallelExecutor (quiet=True)
        POOL-->>DISP: list[WorkerResult] length N<br/>(status ∈ success|timeout|parse_error|proxy_error)
        DISP-->>ENS: N WorkerResults (one per slot, index 0..N-1)
        Note over ENS: M = Σ(status=="success"); diversity over distinct<br/>model_id of the M survivors (NOT over N)
        ENS->>RED: reduce_wave3(worker_results, "normalize+merge",<br/>output_dir=<output>/t2-swarm, workers_requested=N)
        RED-->>ENS: ResultContract: workers_succeeded=M,<br/>output_files[].final_path, merged_path (M≥2)
    end

    rect rgb(255,250,235)
        Note over ENS,ADV: Mode A scoring — per-reviewer final_paths, NEVER merged.md (FR-RH2.3)
        ENS->>ADV: --compare <existing>,<final_path…M> --suspect-source <final_path…M>
        ADV-->>ENS: convergence_score, merged_output_path
    end

    ENS->>ENS: map swarm facts → reflect contract vocabulary<br/>(tier_reached, merge_method, t2_model_class_diversity,<br/>reviewer_count, adversarial_convergence_score)
    ENS-->>RUN: write reflect-shaped return-contract.yaml @ config.contract_path; return rc
    RUN->>VRD: parse_contract(config.contract_path) → derive_verdict(contract, expected_tier=2, child_rc=rc)
    VRD-->>RUN: ReflectResult (verdict via blocked→degraded→halted→pass)
    RUN->>OUT: write_reflect_post (frontmatter) + write_sidecar (wrapper-result.yaml)
    OUT-->>Op: exit code (pass→0 | degraded→11 | blocked→2 | halted→10)
```

**Diagram provenance:** every participant and edge is a `[CODE-VERIFIED]` symbol from the research set. Tier-1 unchanged + `expected_tier==2` seam at `_audit_once` L403/L405 (`01-reflect-runner-seam.md`); `dispatch_wave1` signature with `transport_for_slot` per-slot factory and `list[WorkerResult]` of length N (`03-swarm-dispatch.md` §1.1); M = `Σ(status=="success")` and diversity-over-M (`03-swarm-dispatch.md` §5, predicate matches `dispatch.py` L496); `reduce_wave3` `normalize+merge` emitting `output_files[].final_path` + `merged_path` when M≥floor (`05-swarm-reduce-merge-contract.md` §1.3/§1.4); Mode A `--compare`/`--suspect-source` handoff from succeeded `final_path`s, never `merged.md` (`08-precedents-adversarial-handoff.md` §4.3); the swarm→reflect contract translation in `ensemble.py` (`05-swarm-reduce-merge-contract.md` §7); `parse_contract`→`derive_verdict`→`write_reflect_post`/`write_sidecar` tail unchanged (`01-reflect-runner-seam.md` §(c)/(d)).

**Steps:**

1. **Invoke.** Operator runs `superclaude reflect run <tasklist> --depth deep` (optionally `--transport {openai_compat|stub}`, `--reviewers N` clamped to `[2,4]`, default 3). Unknown `--transport` value is rejected at Click parse before any dispatch (`00-prd-extraction.md` §5.2).
2. **Tier branch.** `run()` calls `_audit_once()`, which computes `expected_tier = 2` because `depth ∈ {standard, deep}` (`runner.py` L403).
3. **Tier-1 grounded pass (UNCHANGED).** The single `/sc:reflect --mode post` grounded reflection runs via `ClaudeProcess` (`--tools default`), producing the trusted baseline reviewer artifact. FR-RH2.1 AC: "the reflect Tier-1 grounded pass is unchanged."
4. **Per-reviewer briefs.** `ensemble.py` builds the `reflect-review` lens briefs — each external worker framed as a heterogeneous reflection reviewer (`tier: "T2"`, `suspect: true`), `default_workers ∈ [2,4]`, models drawn from the `T2Model0N` env pool (NOT `spec.workers.models`) (FR-RH2.2, `00-prd-extraction.md`).
5. **Fan-out (`dispatch_wave1`).** `ensemble.py` calls `dispatch_wave1(preflight, transport_for_slot=λ i → transport_for_model(T2Model0(i)), prompt=…, worker_spec=…, logger=…)`. The per-slot factory binds each slot to a distinct external model and **takes precedence** over a shared `transport` (`dispatch.py` L453-457). Fan-out routes strictly through `ParallelExecutor` (`quiet=True`, AC-004). Returns `list[WorkerResult]` of length **N** (one per slot, synthesized `proxy_error` backstop guarantees one-per-slot) (`03-swarm-dispatch.md` §1.4).
6. **Compute M + diversity (over survivors).** M = `Σ(1 for r in results if r.status == "success")` — the exact predicate dispatch uses at `dispatch.py` L496. Diversity is computed over the **distinct `model_id` of the M survivors, never over N** (FR-RH2.4/FR-RH2.9; `03-swarm-dispatch.md` §5).
7. **Reduce (`reduce_wave3`).** `ensemble.py` calls `reduce_wave3(worker_results, "normalize+merge", output_dir=<output>/t2-swarm, workers_requested=N)`. This stamps swarm `status` (IMM-5), writes each survivor's **`final_path`**, and writes `merged.md` only when M ≥ floor(2) (`05-swarm-reduce-merge-contract.md` §1.3/§1.4). The merge boundary (`merge.py`, ≤30 LOC) is a scoring-free mechanical concat — it does NOT score/rank/dedup.
8. **Mode A scoring.** `ensemble.py` collects the M succeeded `final_path`s and hands them to `/sc:adversarial` Mode A as `--compare <existing-Tier-1>,<final_path…M> --suspect-source <final_path…M>` — built from per-reviewer `final_path`s, **never** swarm's `merged.md` (FR-RH2.3; precedent `commands.py` L2066-2081, `08-precedents-adversarial-handoff.md` §4.3). Mode A returns a `convergence_score`.
9. **Contract translation.** `ensemble.py` maps swarm raw facts (`workers_succeeded`=M, `amalgamation_mode`, `merged_path`, distinct `output_files[].model_id`) into the **reflect** contract vocabulary (`tier_reached`, `merge_method`, `t2_model_class_diversity`, `reviewer_count`, `adversarial_convergence_score`) and lands a reflect-shaped `return-contract.yaml` at `config.contract_path` (the two contracts share only the key name `status`, with different semantics — disjoint schemas, `05-swarm-reduce-merge-contract.md` §6/§7). Path confinement: reflect parses `<output_dir>/return-contract.yaml`, NEVER the `t2-swarm/` subdir contract directly (`00-prd-extraction.md` §5.3).
10. **Verdict (UNCHANGED tail).** `_audit_once` runs `parse_contract(config.contract_path)` → `derive_verdict(contract, expected_tier=2, allow_single_vendor, child_rc=rc)`, ordering `blocked → degraded → halted → pass`. The wrapper never classifies deviations itself (NFR-1 thinness preserved) (`01-reflect-runner-seam.md` §(c)).
11. **Serialize + exit.** `run()` finalizes via `write_reflect_post` (atomic `reflect_post:` frontmatter replace, FR-6) and `write_sidecar` (`wrapper-result.yaml`, always written, carries the sidecar-only `env_alias_count`, FR-7). Exit code from the `Verdict` map: `pass→0`, `halted→10`, `degraded→11`, `blocked→2` (unchanged per FR-RH2.7).

**Success Criteria (faithful Tier-2 PASS — FR-RH2.4):**

- `tier_reached == 2`.
- `merge_method != "single-reviewer-fallback"`.
- `reviewer_count == M >= 2`, where M = count of `WorkerResult`s with `status == "success"`.
- `t2_model_class_diversity == "full"`, computed over the **distinct `model_id` of the M succeeded workers** (≥ expected distinct-class count) — two survivors of the same class do NOT count as `full`.
- Exit code `0` (`pass`).
- No `Task(` / `subagent_type` fan-out introduced in `runner.py` or `ensemble.py`; no raw `subprocess.run`/`Popen` added to the reflect package; no `async`/`await`; no `cli.sprint`/`cli.roadmap` import (NFR-RH2.1/.2, guarded by `test_no_nesting_guard.py`). Tier-1 grounded pass unchanged.
- The credit-free `--transport stub` lane reaches the SAME success signals over the REAL `dispatch_wave1`/`reduce_wave3` path with zero network I/O (FR-RH2.5), and the 1-reviewer witness genuinely FAILS those same assertions (FR-RH2.6).

### 11.2 Error Scenarios & Degradation Branches — the (M,N) divergence guard

The Tier-2 fan-out is a filtering pipeline: **N** requested slots reduce to **M** succeeded workers (`proxy_error`/`timeout`/`parse_error` failures drop the count; only `status=="success"` counts toward M — salvage may promote `parse_error→success` upstream, post-salvage status governs). The verdict for any **(M,N)** is fully determined by the table below, reproduced verbatim from the spec's `mn_guard_table` (`00-prd-extraction.md` §5). Values match the spec exactly.

| M-condition | verdict | exit-code | reason-slug |
|-------------|---------|-----------|-------------|
| `M==0` (all workers failed / no usable artifacts) | `blocked` | `2` | `ensemble-empty` |
| `M==1` (≥N−1 failed, or `--reviewers 1`) | `degraded` | `11` | `single-reviewer-fallback` |
| `M>=2` but `<2` distinct model classes (survivors collapsed onto one class) | `degraded` | `11` | `degraded-model-diversity` |
| `M>=2` AND `>=2` distinct classes | `pass-eligible` | `0` | `pass` |

**`derive_verdict` ordering:** `blocked → degraded → halted → pass` (blocked is ordered AHEAD of degraded, so M==0 wins over any degrade) (`00-prd-extraction.md` §5.4). Verdict→exit-code map unchanged (FR-RH2.7).

Mapping each branch to the flow above:

- **If M ≥ 2 AND ≥ 2 distinct succeeded model classes → faithful Tier-2 (PASS-eligible).** `status: success`, `t2_model_class_diversity: full`, `tier_reached: 2`, `merge_method != single-reviewer-fallback`, `reviewer_count = M`, exit `0`. This is the §11.1 happy path. The Mode A merge over the M survivors' `final_path`s yields the convergence score recorded on the contract.
- **If M ≥ 2 but < 2 distinct model classes → `degraded` (`degraded-model-diversity`), NEVER PASS.** The survivors ran but collapsed onto a single model class, so the ensemble lacks true heterogeneity. Diversity is measured over the M survivors' distinct `model_id`s, so two same-class survivors fail the `full` test → exit `11`. (Acceptance: a `--reviewers 3` run with exactly one `proxy_error` after retry → M==2; PASS-eligible iff the 2 survivors are ≥2 distinct classes, else `degraded-model-diversity`.)
- **If M == 1 → `degraded` via `merge_method: single-reviewer-fallback` and/or `tier_reached: 1`.** This is the SAME path the `--reviewers 1` negative witness reaches; a 3-slot run that loses 2 workers lands here too — by design, not a special case. Exit `11`. A single reviewer cannot produce an adversarial merge (`reduce_wave3` merge gate is `M < floor(2) → merged_body None`, `05-swarm-reduce-merge-contract.md` §1.3), so the run degrades rather than emitting a vacuous Tier-2 pass. (Acceptance FR-RH2.6: the same assertions that pass in the positive FR-RH2.5 test MUST FAIL here.)
- **If M == 0 (all workers failed / no usable artifacts) → `blocked` (`ensemble-empty`), NOT a silent degrade.** The audit is untrustworthy (zero reviewers), so `blocked` is ordered ahead of `degraded` in `derive_verdict` and the run routes exit `2`. This is distinct from `degraded`: a blocked audit asserts nothing about the work, whereas a degraded audit asserts a low-confidence result.
- **If `--transport` is an unknown enum value → rejected at Click parse**, before any dispatch — non-zero exit, no partial run (`00-prd-extraction.md` §5.2). Accepted values: `[openai_compat, stub]` only.
- **If the swarm dispatch backstop fires** (a worker callable raises and `ParallelExecutor` returns `None` for that slot), dispatch synthesizes a `WorkerResult(status="proxy_error")` for the slot (`dispatch.py` L487-490) — that slot does NOT count toward M, so it folds cleanly into the (M,N) table above without a separate code path.
- **If `write_reflect_post` cannot write on an otherwise-PASS run** (frontmatter stale/missing → status not `"written"`), the FR-6 fail-closed rule flips the verdict PASS→`BLOCKED` (`runner.py` L588-590) — a serialization failure is never silently swallowed as success.

**Falsifiability guarantee (NFR-RH2.3):** the positive proof (M≥2, faithful Tier-2) and the falsifying witness (M==1, degrades) BOTH run the real `dispatch_wave1`/`reduce_wave3` path — the stub transport is deterministic and network-free but NOT a canned `tier_reached:2` fixture (FR-RH2.5 AC), so the ensemble proof is non-vacuous.

---

## Cross-cutting notes for the TDD author

- **§9/§10 are genuinely N/A**, not skipped for convenience: the reflect package is a synchronous backend library with two on-disk YAML artifacts as its only "state surface," documented in §7/§11. The template explicitly scopes both sections to frontend/client components.
- **The only NET-NEW participants in §11.1 are `ensemble.py` and the `reflect-review` lens.** Everything downstream of step 5 (`dispatch_wave1` → `reduce_wave3`) and everything in step 10-11 (`parse_contract` → `derive_verdict` → `write_reflect_post`/`write_sidecar`) is existing, verified, unchanged code that `ensemble.py` composes.
- **The (M,N) table is the load-bearing contract** for §11.2 and for FR-RH2.4/FR-RH2.9 — every value (`blocked/2/ensemble-empty`, `degraded/11/single-reviewer-fallback`, `degraded/11/degraded-model-diversity`, `pass-eligible/0/pass`) is reproduced verbatim from the spec; the TDD's §12 (Error Handling) should re-cite it rather than re-derive it.

---

**Status: Complete**
