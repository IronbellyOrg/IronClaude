# PRD Extraction — FR-RH2 (Headless Ensemble Fix)

**Topic**: Drive sc:reflect Tier-2 reviewer ensemble through the swarm CLI (headless ensemble fix)
**Source spec**: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`
**Feature ID**: FR-RH2 | **Target release**: 4.4.0 | **Complexity**: HIGH (0.82)
**Date**: 2026-06-20
**Status**: Complete

This document transcribes the complete requirements set from the FR-RH2 release spec faithfully (no fabrication). All FR/NFR/OI IDs, acceptance criteria, the CLI surface, and the (M,N) divergence guard table are reproduced from the spec.

---

## 1. Scope Boundaries (spec §1.2)

**In scope**:

- Re-route the reflect Tier-2 reviewer ensemble so it forms via the **swarm dispatch library** (`ensemble.py` imports `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3` in-process; the `superclaude swarm run --lens reflect-review` CLI is the optional `--detached` observability variant, not the default inner-loop transport) — an external OpenAI-compatible proxy-model fan-out that sidesteps the `claude -p` nesting failure.
- A new `reflect-review` swarm lens carrying per-reviewer briefs.
- Consumption of swarm's normalized per-reviewer artifacts by reflect's existing `sc-adversarial-protocol` Mode A merge as the downstream scorer.
- A **non-mocked** integration test (real wrapper, `--transport stub`) that proves the ensemble actually forms.
- A one-reviewer negative witness.
- Preservation of the `return-contract.yaml` shape.
- Explicit reconciliation with NFR-7.

**Out of scope**:

- Rewriting `/sc:reflect`'s Tier-1 (single-agent grounded) pass.
- Changing the 4-state verdict map / exit-code contract (`contract.py`, `models.py`).
- Changing the auto-fix loop (FR-1/FR-3) beyond the audit-launch seam it calls.
- Changing the swarm CLI's own merge boundary (`merge.py` stays a mechanical concat, never an adversarial scorer).
- The UC-1 pre-execution path.
- Building a new parallel fan-out engine (swarm already provides one — this spec **adapts the shared seam**, it does not rebuild).

---

## 2. Functional Requirements (spec §3)

### FR-RH2.1: Tier-2 ensemble forms via the swarm CLI, not in-process Task fan-out

**Description**: When `depth` is `standard` or `deep` (expected tier 2), the reflect Tier-2 reviewer ensemble MUST be produced by driving `superclaude swarm run --lens reflect-review` (a thin caller over `dispatch_wave1` + the per-slot transport factory), never by a single `claude -p` agent fanning out reviewers via the Task tool.

**Acceptance Criteria**:

- [ ] The Tier-2 audit path invokes the swarm run surface (`dispatch_wave1` / `_resolve_run_transport_factory`); no `Task(` or `subagent_type` fan-out is introduced in `runner.py` or the new driver.
- [ ] A `depth=standard|deep` run binds each worker slot to a distinct external model (`T2Model0N`) via the per-slot factory.
- [ ] The reflect Tier-1 grounded pass (`/sc:reflect` via `ClaudeProcess`) is unchanged.

**Dependencies**: `dispatch.dispatch_wave1` (`dispatch.py:334`), `_resolve_run_transport_factory` (`commands.py:612`), the new `reflect-review` lens (FR-RH2.2).

### FR-RH2.2: A `reflect-review` swarm lens supplies per-reviewer reflection briefs

**Description**: Add a `reflect-review` lens to the bundled swarm-lens registry (mirroring `lenses/bare_review.py`) that frames each external worker as a heterogeneous reflection reviewer with a per-reviewer brief, `tier: "T2"`, `suspect: true`, and a `recommended_next_command_template` that hands the normalized artifacts to `/sc:adversarial`.

**Acceptance Criteria**:

- [ ] `reflect-review` is registered and passes the swarm lens validator (same gate as `bare-review`).
- [ ] The lens emits `suspect: true` and a `recommended_next_command_template` containing `/sc:adversarial` with `{suspect_files}` substitution.
- [ ] `default_workers` is in `[2,4]`; the lens does not hard-code a Claude model (models come from the `T2Model0N` env pool, not `spec.workers.models`).

**Dependencies**: `superclaude.cli.swarm.models.LensEntry`, `schema.CANONICAL_INJECTION_GUARD_SENTENCE`.

### FR-RH2.3: Swarm normalized artifacts are scored by sc-adversarial-protocol Mode A (not swarm merge)

**Description**: Reflect MUST consume the N normalized per-reviewer artifacts (swarm `final_path`s) as the input to its existing `sc-adversarial-protocol` Mode A merge. Swarm's `mechanical_merge` (`merge.py`) output MUST NOT be treated as the adversarial verdict.

**Acceptance Criteria**:

- [ ] The downstream merge step consumes swarm's per-reviewer `final_path` artifacts (suspect-aware).
- [ ] No scoring/ranking/dedup logic is added to `swarm/merge.py` (the LOC ceiling + boundary tests stay green).
- [ ] The adversarial merge produces a convergence score recorded on the reflect contract.

**Dependencies**: `reduce_wave3` (`reduce.py`, `normalize+merge` mode), `sc-adversarial-protocol`.

### FR-RH2.4: A faithful Tier-2 run yields a real adversarial merge with ≥2 distinct model classes

**Description**: A non-mocked Tier-2 run MUST surface, in the reflect `return-contract.yaml`, `tier_reached: 2`, `merge_method != single-reviewer-fallback`, `reviewer_count >= 2`, and `t2_model_class_diversity: full`. **Diversity and reviewer_count are measured over the SUCCEEDED workers (M), not the requested slots (N)** — see FR-RH2.9 for the N→M divergence contract.

**Acceptance Criteria**:

- [ ] On a successful Tier-2 run, `tier_reached == 2`.
- [ ] `merge_method != "single-reviewer-fallback"`.
- [ ] `reviewer_count == M >= 2`, where M = count of `WorkerResult`s with `status == "success"`.
- [ ] `t2_model_class_diversity == "full"` is computed over the **distinct `model_id`s of the M succeeded workers** (≥ the expected distinct-class count), NOT over the N requested slots — so two surviving workers that resolved to the same model class do NOT count as `full`.

**Dependencies**: FR-RH2.1, FR-RH2.2, FR-RH2.3, FR-RH2.9.

### FR-RH2.9: N→M divergence — partial-failure acceptance boundary is explicit

**Description**: The Tier-2 fan-out is a filtering pipeline: N requested slots reduce to M succeeded workers (`proxy_error`/`timeout` failures drop count). The faithful-pass boundary, the partial-success boundary, and the empty boundary MUST be defined so a reader can derive the verdict for any (M, N):

- **M ≥ 2 with ≥2 distinct succeeded model classes** → faithful Tier-2 (PASS-eligible; `status:success`, `t2_model_class_diversity:full` when distinct classes ≥ expected).
- **M ≥ 2 but < 2 distinct model classes** (survivors collapsed onto one class) → `degraded` (`degraded-model-diversity`), never PASS.
- **M == 1** → `degraded` via `merge_method: single-reviewer-fallback` and/or `tier_reached: 1` (this is the SAME path the `--reviewers 1` negative witness reaches; a 3-slot run that loses 2 workers lands here too — by design, not a special case).
- **M == 0** (all workers failed / no usable artifacts) → `blocked` (untrustworthy audit; ordered ahead of degraded in `derive_verdict`), NOT a silent degrade.

**Acceptance Criteria**:

- [ ] A `--reviewers 3` run with exactly one worker `proxy_error` (after retry) yields `M==2`; PASS-eligible **iff** the 2 survivors are ≥2 distinct model classes, else `degraded-model-diversity`.
- [ ] An M==1 outcome (whether from `--reviewers 1` or from N>1 with N−1 failures) yields `single-reviewer-fallback` and/or `tier_reached==1` — a non-PASS.
- [ ] An M==0 outcome routes `blocked` (exit 2), not `degraded`.

**Dependencies**: FR-RH2.4, `contract.derive_verdict` ordering (`blocked → degraded → halted → pass`).

### FR-RH2.5: Credit-free stub-transport path proves ensemble formation in CI

**Description**: A `--transport stub` (`transports/stub.py`) variant MUST drive the **real** wrapper (unmocked `dispatch_wave1`/`reduce_wave3`) over a deterministic, network-free transport and assert the FR-RH2.4 acceptance signals, so CI proves ensemble formation without burning proxy credits.

**Acceptance Criteria**:

- [ ] A test runs the real reflect Tier-2 driver with `--transport stub` and performs no network I/O.
- [ ] The test asserts `tier_reached==2`, `merge_method != single-reviewer-fallback`, `reviewer_count>=2`, `t2_model_class_diversity=="full"`.
- [ ] The test does **not** patch `ClaudeProcess` to copy a canned `tier_reached:2` fixture for the ensemble (it exercises the real fan-out → reduce path).

**Dependencies**: FR-RH2.4, `StubTransport`.

### FR-RH2.6: One-reviewer negative witness must degrade to Tier 1

**Description**: A run configured with a **single** reviewer MUST NOT satisfy the Tier-2 pass signals: it MUST degrade (e.g. `merge_method: single-reviewer-fallback` and/or `tier_reached: 1`), proving the proof in FR-RH2.5 is falsifiable and cannot pass vacuously.

**Acceptance Criteria**:

- [ ] A 1-reviewer stub run yields `merge_method == "single-reviewer-fallback"` and/or `tier_reached == 1` (a non-PASS Tier-2).
- [ ] The same assertions used in the positive FR-RH2.5 test FAIL for the 1-reviewer case (witness is genuinely negative).

**Dependencies**: FR-RH2.5.

### FR-RH2.7: Downstream return-contract consumers are unaffected

**Description**: The reflect `return-contract.yaml` shape and the derived `reflect_post:` write-back + `wrapper-result.yaml` sidecar MUST remain compatible: existing fields keep their names/semantics; the verdict map and exit codes (`contract.py`, `models.py`) are unchanged.

**Acceptance Criteria**:

- [ ] `derive_verdict` and the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged.
- [ ] `write_reflect_post` produces the same `reflect_post:` field set/order; the sidecar keeps its fields.
- [ ] Existing reflect contract/verdict tests pass without modification.

**Dependencies**: `contract.derive_verdict`, `runner.write_reflect_post`, `runner.write_sidecar`.

### FR-RH2.8: NFR-7 no-in-process-Task guarantee is preserved (or amended on the record)

**Description**: The change MUST NOT introduce `Task(`/`subagent_type` fan-out into the reflect package. The author MUST confirm whether spawning swarm/proxy workers is permitted by the exact scope of the NFR-7 guard (`test_no_nesting_guard.py`); if the guard's scope needs to recognize the swarm-driven path, NFR-7 is amended **deliberately and explicitly**, never silently bypassed.

**Acceptance Criteria**:

- [ ] `test_no_nesting_guard.py` (Layer B: no `Task(`/`subagent`/`anthropic` imports in `runner.py`) passes, including for the new driver module.
- [ ] If NFR-7's prose/scope is amended, the amendment is recorded in this spec (§9) and reflected in the guard's docstring/assertions with rationale.
- [ ] No raw `subprocess.run`/`Popen` is added to the reflect package (the swarm call goes through the swarm CLI surface / `ClaudeProcess`, not a hand-rolled `Popen`).

**Dependencies**: `tests/cli/reflect/test_no_nesting_guard.py`.

> **Spec ordering note**: The spec presents the FRs in the order FR-RH2.1, .2, .3, .4, **.9**, .5, .6, .7, .8 (FR-RH2.9 is documented immediately after FR-RH2.4 because the N→M divergence contract is load-bearing for FR-RH2.4's diversity/reviewer_count semantics). All nine FRs (.1–.9) are transcribed above.

---

## 3. Non-Functional Requirements (spec §6)

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-RH2.1 | No in-process Task/Agent fan-out in the reflect package (NFR-7 preserved) | Zero `Task(`/`subagent_type` in `runner.py`/`ensemble.py` | `test_no_nesting_guard.py` Layer B (extended to `ensemble.py`) |
| NFR-RH2.2 | Thinness/isolation (NFR-1) preserved | No `cli.sprint`/`cli.roadmap` import, no `async`/`await`, no raw `subprocess.run`/`Popen` in reflect pkg | `test_no_nesting_guard.py` (import/async/subprocess anchored regexes) |
| NFR-RH2.3 | Ensemble proof is non-vacuous | A positive (≥2) and a falsifying (1) witness, both run the real path | `test_ensemble_stub_integration.py` (positive + negative) |
| NFR-RH2.4 | Credit-free CI | Tier-2 ensemble proof performs zero network I/O | `--transport stub` test imports no httpx wire path; runs offline |
| NFR-RH2.5 | Model-class diversity | `t2_model_class_diversity == "full"` whenever pool ≥ `--reviewers` distinct models | Assert distinct `model_id` count in the swarm `WorkerResult`s |
| NFR-RH2.6 | Backward compatibility | Existing reflect contract/verdict/runner tests pass unchanged | `uv run pytest tests/cli/reflect -q` green |
| NFR-RH2.7 | Observability | Headless Tier-2 runs are pollable | Swarm `--detached`/tmux + `done.json` sentinel + `--tui` available for the t2-swarm subrun |
| NFR-RH2.8 | Proxy contract respected | Workers use only `:4000/cli` base + `T2Model01..NN` per `~/.aienv` | `read_env` preflight; no `:4000/v1` / `:8317` probing |

---

## 4. CLI Surface (spec §5.1)

```
superclaude reflect run <tasklist> --depth {standard|deep}
    [--transport {openai_compat|stub}]   # default: openai_compat (live proxy); stub = credit-free CI
    [--reviewers <N>]                     # 2-4; default 3 (one-reviewer => negative-witness degrade)
    [--allow-single-vendor]               # unchanged FR-11 suppression
    [--fix] [--promote] [--resume] [--dry-run] [--print-command]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--transport` | enum `{openai_compat, stub}` | `openai_compat` | Tier-2 worker transport. `openai_compat` = external proxy (`T2Model0N`); `stub` = deterministic, network-free, credit-free CI lane (FR-RH2.5) |
| `--reviewers` | int | `3` | Tier-2 reviewer slots; clamped to `[2,4]`. `1` is the negative-witness case (degrades, FR-RH2.6) |
| `--depth` | enum `{standard, deep}` | `standard` | Tier-2 expected for both; `quick` floors to `standard` (existing behavior) |

**Key behavioral notes**:

- `--transport` default is `openai_compat` (live proxy); `stub` is the credit-free CI lane. Unknown enum value is rejected at Click parse (see §5 below).
- `--reviewers` is clamped to `[2,4]`, default `3`. `1` is the negative-witness case → degrade.
- `--depth` enum is `{standard, deep}` (default `standard`); Tier-2 is expected for both. `quick` floors to `standard` (existing behavior).

---

## 5. (M,N) Divergence Guard Table (spec §5.3)

> M = succeeded workers, N = requested slots. Reproduced verbatim from the spec's `mn_guard_table` phase contract.

| M-condition | verdict | exit-code | reason-slug |
|-------------|---------|-----------|-------------|
| `M==0 (all workers failed / no artifacts)` | `blocked` | `2` | `ensemble-empty` |
| `M==1 (>=N-1 failed, or --reviewers 1)` | `degraded` | `11` | `single-reviewer-fallback` |
| `M>=2 but <2 distinct model classes` | `degraded` | `11` | `degraded-model-diversity` |
| `M>=2 AND >=2 distinct classes` | `pass-eligible` | `0` | `pass` |

### 5.1 Worker-status → M mapping (spec §5.3 `worker_status_to_m`)

> Swarm `WorkerResult.status`; `reduce_wave3` counts `success` only.

| WorkerResult.status | Counts toward M? |
|---------------------|------------------|
| `success` | counts toward M |
| `proxy_error` | does NOT count (retry-once-then-drop per swarm §7 matrix) |
| `timeout` | does NOT count |
| `parse_error` | does NOT count (salvage may promote per swarm §7.4; post-salvage status governs) |

### 5.2 `--transport` enum guard (spec §5.3 `transport_enum`)

> Whittaker sentinel/divergence.

- **accepted**: `[openai_compat, stub]`
- **unknown_value**: rejected at CLI parse (Click enum), before any dispatch — non-zero exit, no partial run.

### 5.3 Path-confinement invariant (spec §5.3 `path_confinement`, Hohpe)

> TWO `return-contract.yaml` files exist.

- `reflect_contract`: `<output_dir>/return-contract.yaml` — the ONLY file `reflect.derive_verdict` parses.
- `swarm_subrun_contract`: `<output_dir>/t2-swarm/return-contract.yaml` — swarm DM-012; consumed by `ensemble.py` only.
- **rule**: reflect parses `output_dir/return-contract.yaml`; it MUST NOT parse the `t2-swarm/` subdir's contract directly.

### 5.4 `derive_verdict` ordering (per FR-RH2.9 dependency)

`blocked → degraded → halted → pass` (blocked is ordered ahead of degraded). Verdict→exit-code map (unchanged, FR-RH2.7): `pass→0`, `halted→10`, `degraded→11`, `blocked→2`.

---

## 6. Open Items (spec §11)

> ⚠️ **OI-1 is the BLOCKING GATE.** It must be resolved BEFORE any FR-RH2.3 code lands.

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| **OI-1 (BLOCKING GATE)** | Does reflect's swarm contract already emit `reviewer_count`/`merge_method`/`t2_model_class_diversity` in the exact shape `contract.derive_verdict` reads, or must `ensemble.py` map them? Produce an explicit **swarm-`ResultContract`-field → reflect-contract-field correspondence table**. | High — load-bearing for FR-RH2.4/2.7; the asserted shape-preservation rests on it | **Resolve BEFORE any FR-RH2.3 code lands** (Newman): diff swarm DM-012 vs the fields `derive_verdict` reads; the mapping layer in `ensemble.py` is sized by this table |
| OI-2 | Exact NFR-7 amendment text (if any) — does Layer-B's intent already cover HTTP workers, or does the prose need updating? | Medium — touches the no-nesting guarantee wording | During FR-RH2.8; decide confirm-vs-amend, record in §9 |
| OI-3 | Should `--transport stub` be auto-selected in CI, or always opt-in? | Low — CI ergonomics | Before FR-RH2.5 lands |
| OI-4 | How does `/sc:adversarial` Mode A treat `suspect: true` reflect-review artifacts vs bare-review ones (any rubric difference)? | Low-Medium — scoring fidelity | During FR-RH2.3; confirm against `sc-adversarial-protocol` |

**OI-1 explicit gating statement (verbatim intent from spec)**: OI-1 is the load-bearing blocking gate. The deliverable is a swarm `ResultContract` field → reflect contract field correspondence table (the swarm ResultContract → reflect contract field-correspondence table referenced in the task). It must be resolved before FR-RH2.3 code; the `ensemble.py` mapping layer is sized by this table.

---

## 7. Summary

This extraction faithfully transcribes the complete FR-RH2 requirements set from the headless-ensemble-fix release spec (`spec.md`, feature_id `FR-RH2`, target release 4.4.0, HIGH complexity 0.82).

**Core problem**: `superclaude reflect run` cannot deliver a real Tier-2 reviewer ensemble because the wrapper spawns one `claude -p` subprocess that delegates `/sc:reflect` into a Task worker, which then cannot nest a second level of Task fan-out (subagent→agent nesting is forbidden). The run degrades to `single-reviewer-fallback`, `tier_reached:1`, zero adversarial reviewers. NFR-7 forbids the only alternative (in-runner `Task(`/`subagent_type`), making the failure architecturally guaranteed, not incidental.

**Solution**: Re-route the Tier-2 ensemble through the swarm dispatch library (in-process import of `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3`), fanning out to external OpenAI-compatible proxy workers (`T2Model0N`) that sidestep the nesting defect and provide true model-class diversity. A new `reflect-review` lens supplies per-reviewer briefs; swarm normalizes + mechanically concats; `/sc:adversarial` Mode A scores; the `return-contract.yaml` shape and verdict→exit-code map are preserved.

**Coverage of this document**:

- **9 Functional Requirements** (FR-RH2.1 through FR-RH2.9), each with full description, acceptance criteria, and dependencies. (Note the spec sequences FR-RH2.9 immediately after FR-RH2.4.)
- **8 Non-Functional Requirements** (NFR-RH2.1 through NFR-RH2.8) — ID, requirement, target, measurement.
- **CLI surface**: `--transport {openai_compat|stub}` (default openai_compat; stub = credit-free CI), `--reviewers <N>` (clamp `[2,4]`, default 3, 1 = negative-witness degrade), `--depth {standard|deep}` (quick floors to standard).
- **(M,N) divergence guard table** reproduced verbatim: M==0 → blocked/exit2/`ensemble-empty`; M==1 → degraded/exit11/`single-reviewer-fallback`; M≥2 but <2 distinct classes → degraded/exit11/`degraded-model-diversity`; M≥2 ∧ ≥2 distinct classes → pass-eligible/exit0/`pass`. Plus worker-status→M mapping (only `success` counts), the `--transport` enum guard (unknown value rejected at Click parse), the path-confinement invariant (two `return-contract.yaml` files), and `derive_verdict` ordering.
- **4 Open Items** (OI-1..OI-4), with **OI-1 explicitly flagged as the BLOCKING GATE** (swarm ResultContract → reflect contract field-correspondence table; resolve before FR-RH2.3 code).
- **Scope Boundaries** (in-scope vs out-of-scope per spec §1.2).

**Status**: Complete
