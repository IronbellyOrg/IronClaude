```yaml
---
title: "Drive sc:reflect Tier-2 reviewer ensemble through the swarm CLI (headless ensemble fix)"
version: "1.0.0"
status: draft
feature_id: FR-RH2
parent_feature: null
spec_type: infrastructure
complexity_score: 0.82
complexity_class: HIGH
target_release: 4.4.0
authors: [user, claude]
created: 2026-06-19
quality_scores:
  clarity: 9.0
  completeness: 9.0
  testability: 9.5
  consistency: 9.0
  overall: 9.1
---
```

## 1. Problem Statement

> What problem does this work solve? Why does it matter? What fails or is suboptimal today?

`superclaude reflect run` is supposed to deliver a real Tier-2 reflection: a heterogeneous reviewer
ensemble (2-3 reviewers on different model classes) merged via the `sc-adversarial-protocol` Mode A.
Today it cannot. The wrapper spawns exactly **one** `claude -p` subprocess running `/sc:reflect --mode
post … --tier 2` (`runner.py:341-366` `_build_prompt`; `runner.py:392-428` `_audit_once`) and relies on
**that** single headless agent to fan out the ensemble in-process via the Task tool.

Under `claude -p`, the top-level headless agent delegates `/sc:reflect` into a **Task worker** (a
subagent). That worker reaches the skill's Wave 3 ("spawn N reviewers via Task") and Wave 4
(`sc-adversarial-protocol`, itself Task-spawning) and attempts a second level of Task fan-out.
Subagent→agent nesting is not permitted, so the ensemble is uncollectable: the run degrades to
`merge_method: single-reviewer-fallback`, `tier_reached: 1`, and **zero** adversarial reviewers. The
user cannot produce a faithful adversarial post-execution audit from the headless wrapper at all.

Two structural facts make this not merely a bug but an **architecturally guaranteed** failure:

1. **NFR-7 forbids the only alternative the current design has.** The no-nesting guard
   (`tests/cli/reflect/test_no_nesting_guard.py`) forbids `runner.py` from spawning reviewers via
   `Task(`/`subagent_type`. So ensemble fan-out is **100% delegated** to the headless agent's own
   in-process Task calls — exactly the path that fails under `claude -p`. The defect is wired in, not
   incidental.

2. **The "Tier 2 works" claim is circular — never exercised by any test.** Every reflect runner test
   mocks `ClaudeProcess` (`tests/cli/reflect/conftest.py:98-138`): a `MagicMock` whose `.wait()` copies
   a pre-canned `fixtures/*.yaml` into `return-contract.yaml`. `pass.yaml` hard-codes `tier_reached: 2`.
   The in-process ensemble is **never run**, so the assertion `tier_reached == 2` proves only that the
   fixture says `2`. The benchmark reviewer outputs that *look* like proof
   (`reflect-opus-architect.md`, `reflect-haiku-analyst.md`, `adversarial-merge.md`) were produced by
   `roadmap validate` (`validate_executor.py:317-373`), a **separate-process-per-agent** execution model
   — a different mechanism entirely, which proves nothing about the in-process wrapper.

### 1.1 Evidence

> Concrete evidence that the problem exists. Links to issues, failing tests, user reports, forensic findings.

| Evidence | Source | Impact |
|----------|--------|--------|
| Single `claude -p` launch expecting in-process Task fan-out | `src/superclaude/cli/reflect/runner.py:341-366` (`_build_prompt`), `runner.py:392-428` (`_audit_once`) | The only ensemble path is in-process Task fan-out under `claude -p` |
| Subagent→agent nesting failure reproduced (L2d/T3) | User repro; `tier_reached:1`, `merge_method:single-reviewer-fallback`, 0 adversarial reviewers | Faithful Tier-2 audit unreachable from the wrapper |
| Ensemble never exercised — tests mock `ClaudeProcess` and copy a canned contract | `tests/cli/reflect/conftest.py:98-138`; `pass.yaml` hard-codes `tier_reached:2` | "Tier 2 works" is a fixture assertion, not behavior; the gap is invisible to CI |
| NFR-7 forbids `Task(`/`subagent_type` in `runner.py` | `tests/cli/reflect/test_no_nesting_guard.py:95-102` | The design has no permitted in-wrapper fan-out; failure is structural |
| Model-class diversity degrades by construction | `runner.py:36-41,254-261` counts ≤3 Claude aliases from `ANTHROPIC_DEFAULT_*_MODEL`; `contract.py:266-269` routes `t2_model_class_diversity != "full"` → `degraded` | Even a working in-process ensemble caps at ~3 Claude aliases → `degraded-model-diversity` |
| Benchmark reviewer outputs came from a different execution model | `src/superclaude/cli/roadmap/validate_executor.py:317-373` (separate-process-per-agent) | Cited "proof" is not evidence for the in-process wrapper path |

### 1.2 Scope Boundary

> What this spec addresses and explicitly does NOT address.

**In scope**: Re-route the reflect Tier-2 reviewer ensemble so it forms via the **swarm dispatch
library** (`ensemble.py` imports `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3`
in-process; the `superclaude swarm run --lens reflect-review` CLI is the optional `--detached`
observability variant, not the default inner-loop transport) — an external OpenAI-compatible proxy-model
fan-out that sidesteps the `claude -p` nesting failure; a new `reflect-review` swarm lens carrying per-reviewer
briefs; consumption of swarm's normalized per-reviewer artifacts by reflect's existing
`sc-adversarial-protocol` Mode A merge as the downstream scorer; a **non-mocked** integration test
(real wrapper, `--transport stub`) that proves the ensemble actually forms; a one-reviewer negative
witness; preservation of the `return-contract.yaml` shape; explicit reconciliation with NFR-7.

**Out of scope**: Rewriting `/sc:reflect`'s Tier-1 (single-agent grounded) pass; changing the 4-state
verdict map / exit-code contract (`contract.py`, `models.py`); changing the auto-fix loop (FR-1/FR-3)
beyond the audit-launch seam it calls; changing the swarm CLI's own merge boundary (`merge.py` stays a
mechanical concat, never an adversarial scorer); the UC-1 pre-execution path; building a new parallel
fan-out engine (swarm already provides one — this spec **adapts the shared seam**, it does not rebuild).

## 2. Solution Overview

> High-level description of the approach. What changes, what stays the same.

**Adapt the shared swarm seam; do not rebuild it.** The swarm CLI already implements the exact
per-reviewer parallel fan-out a hand-rolled "Option A" would reconstruct:

- `dispatch.dispatch_wave1(...)` (`dispatch.py:334`) fans a prompt across N worker slots through
  `ParallelExecutor`, recording one `WorkerResult` per slot with per-slot `model_id`/`model_label`,
  status (`success`/`timeout`/`parse_error`/`proxy_error`), and the full timeout/retry matrix.
- `commands._resolve_run_transport_factory(...)` (`commands.py:612`) binds **slot `i` to a distinct
  `T2Model0N`** external proxy model and raises `ModelPoolTooSmallError` (`commands.py:589-609`) rather
  than silently reusing a model when the pool is too small.

The reflect Tier-2 ensemble is driven **through swarm**, mirroring the `sc-bare-review` precedent
(`src/superclaude/skills/sc-bare-review/SKILL.md`): a thin caller over `swarm run --lens <lens>` that
hands normalized per-reviewer artifacts to `/sc:adversarial`. Two mismatches exist and are **resolved as
complementary, not competing**:

- **(a) Workers are OpenAI-compatible HTTP calls to proxy models, not `claude -p`.** This is the
  decisive win, not a problem: external proxy workers (a) cannot trigger the `claude -p` can't-nest-Task
  defect because there is no nested Task surface, and (b) draw from a pool of up to N **distinct**
  external models (`T2Model01..NN`, e.g. `kimi-k2.7-code`, `qwen3.6-plus`, `glm-5.1`, `deepseek-v4-pro`),
  fixing `t2_model_class_diversity:degraded` (today capped at ~3 Claude aliases). A new `reflect-review`
  lens supplies the per-reviewer reflection briefs as the swarm prompt.
- **(b) Swarm's merge is a mechanical concat, architecturally forbidden from scoring.** `merge.py:9-30`
  enumerates DISALLOWED operations (sort/rank/score/judge/dedup) and explicitly hands off scoring to
  `/sc:adversarial`. Reflect keeps its `sc-adversarial-protocol` Mode A merge as the **downstream
  consumer** of swarm's normalized artifacts. Swarm normalizes + concats; `/sc:adversarial` scores.

What stays the same: the `return-contract.yaml` shape downstream consumers parse; the verdict map and
exit codes (`contract.py`, `models.py`); the auto-fix loop; the `/sc:reflect` Tier-1 pass; the swarm
CLI internals.

### 2.1 Key Design Decisions

> Decisions made during brainstorming/design that shaped this spec. Each decision should have a rationale.

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Where the ensemble forms | Drive Tier-2 through `swarm run --lens reflect-review` (external proxy fan-out) | (A) Rebuild per-reviewer fan-out inside `runner.py`; (B) keep in-process Task fan-out | Swarm already owns heterogeneous per-slot model binding, the too-small-pool guard, and the uniform `WorkerResult`/contract surface; rebuilding duplicates a hardened seam, and in-process Task fan-out is the broken path |
| Who scores the reviews | Reflect's existing `sc-adversarial-protocol` Mode A consumes swarm's normalized artifacts | Use swarm's `merge.py` output as the verdict | `merge.py` is architecturally a mechanical concat (`merge.py:9-30`) and forbidden from scoring; adversarial scoring must remain in `/sc:adversarial`. Complementary, not competing |
| Model diversity source | External proxy pool `T2Model01..NN` via the `~/.aienv` contract | Keep counting `ANTHROPIC_DEFAULT_*_MODEL` (≤3 Claude aliases) | Proxy pool yields up to N distinct model classes → `t2_model_class_diversity:full`; the Claude-alias count tops out at ~3 and routes `degraded-model-diversity` |
| NFR-7 reconciliation | Confirm swarm/proxy workers are out of NFR-7's `Task(`/`subagent_type` scope; amend the guard's prose deliberately if needed | Silently add an exemption; ignore the guard | NFR-7 forbids in-process Agent/Task nesting (the failing path); external HTTP workers via `dispatch_wave1` are not that path. The guarantee must be preserved or amended on the record, never bypassed |
| Credit-free proof | `--transport stub` (`transports/stub.py`) integration test asserting ensemble formation | Live-proxy-only test; mock-only test | Stub is network-free + deterministic and exercises the **real** `dispatch_wave1`/`reduce_wave3` path; mock-only is the gap that hid this defect |
| Vacuous-pass guard | One-reviewer **negative witness** that must degrade to tier 1 | Single positive test | A positive-only test can pass even if the wrapper never distinguishes 1 from N reviewers; the negative witness makes the proof falsifiable |
| Contract compatibility | Preserve `return-contract.yaml` shape; map swarm `WorkerResult`s onto reflect's existing contract fields | Emit a new contract schema | Downstream consumers (`reflect_post:` write-back, sidecar, exit-code derivation) parse the existing shape; breaking it cascades |
| Swarm integration contract | **In-process library import** of `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3` from `ensemble.py` (primary path) | Shell out to `superclaude swarm run --lens reflect-review` (CLI subprocess, the sc-bare-review precedent) | Library import adds no second `claude`/proxy subprocess, keeps NFR-RH2.2 (no raw `Popen` in the reflect pkg) trivially true, and lets `derive_verdict` run in-process over the assembled contract. The CLI `--detached`/tmux path (§8.3, NFR-RH2.7) is retained as the **optional** long-headless-run observability mode, NOT the default inner-loop transport |

### 2.2 Workflow / Data Flow

> How the system works end-to-end after this change. Use ASCII diagrams for pipeline flows.

```
superclaude reflect run --depth deep|standard
  │
  ├─(1) preflight + _build_prompt (Tier-1 grounded pass via ClaudeProcess /sc:reflect, UNCHANGED)
  │
  ├─(2) Tier-2 ENSEMBLE  ── NEW PATH (replaces in-process Task fan-out) ──
  │       │
  │       │  reflect Tier-2 driver (thin caller; NO Task(), NO subagent_type)
  │       ▼
  │   ensemble.py (in-process import of the swarm dispatch library; CLI shell-out only for --detached)
  │       │   --lens reflect-review --transport openai_compat|stub
  │       │   per-reviewer briefs as prompt; output=<reflect_out>/t2-swarm/
  │       ▼
  │   _resolve_run_transport_factory(openai_compat)        commands.py:612
  │       │   slot i → T2Model0N  (distinct model per slot; ModelPoolTooSmallError guard)
  │       ▼
  │   dispatch_wave1(...) via ParallelExecutor             dispatch.py:334
  │       │   N WorkerResult {model_id, model_label, status, elapsed_ms, final_path}
  │       ▼
  │   normalize_wave2 → reduce_wave3 (normalize+merge)     reduce.py
  │       │   per-reviewer final_path artifacts + mechanical merged.md (NOT a verdict)
  │       │   swarm return-contract.yaml + done.json sentinel
  │       ▼
  ├─(3) /sc:adversarial  (sc-adversarial-protocol Mode A)  ── DOWNSTREAM SCORER ──
  │       │   consumes the N normalized per-reviewer artifacts (suspect-aware)
  │       ▼
  │   adversarial merge verdict + convergence score
  │
  ├─(4) reflect derive_verdict (contract.py, UNCHANGED) over the assembled return-contract.yaml:
  │        tier_reached=2 ; merge_method != single-reviewer-fallback ;
  │        reviewer_count>=2 ; t2_model_class_diversity=full
  │
  └─(5) write_reflect_post + wrapper-result.yaml sidecar (runner.py, UNCHANGED)
```

## 3. Functional Requirements

> Numbered requirements. Each must be testable and traceable.

### FR-RH2.1: Tier-2 ensemble forms via the swarm CLI, not in-process Task fan-out

**Description**: When `depth` is `standard` or `deep` (expected tier 2), the reflect Tier-2 reviewer
ensemble MUST be produced by driving `superclaude swarm run --lens reflect-review` (a thin caller over
`dispatch_wave1` + the per-slot transport factory), never by a single `claude -p` agent fanning out
reviewers via the Task tool.

**Acceptance Criteria**:

- [ ] The Tier-2 audit path invokes the swarm run surface (`dispatch_wave1` / `_resolve_run_transport_factory`); no `Task(` or `subagent_type` fan-out is introduced in `runner.py` or the new driver.
- [ ] A `depth=standard|deep` run binds each worker slot to a distinct external model (`T2Model0N`) via the per-slot factory.
- [ ] The reflect Tier-1 grounded pass (`/sc:reflect` via `ClaudeProcess`) is unchanged.

**Dependencies**: `dispatch.dispatch_wave1` (`dispatch.py:334`), `_resolve_run_transport_factory` (`commands.py:612`), the new `reflect-review` lens (FR-RH2.2).

### FR-RH2.2: A `reflect-review` swarm lens supplies per-reviewer reflection briefs

**Description**: Add a `reflect-review` lens to the bundled swarm-lens registry (mirroring
`lenses/bare_review.py`) that frames each external worker as a heterogeneous reflection reviewer with a
per-reviewer brief, `tier: "T2"`, `suspect: true`, and a `recommended_next_command_template` that hands
the normalized artifacts to `/sc:adversarial`.

**Acceptance Criteria**:

- [ ] `reflect-review` is registered and passes the swarm lens validator (same gate as `bare-review`).
- [ ] The lens emits `suspect: true` and a `recommended_next_command_template` containing `/sc:adversarial` with `{suspect_files}` substitution.
- [ ] `default_workers` is in `[2,4]`; the lens does not hard-code a Claude model (models come from the `T2Model0N` env pool, not `spec.workers.models`).

**Dependencies**: `superclaude.cli.swarm.models.LensEntry`, `schema.CANONICAL_INJECTION_GUARD_SENTENCE`.

### FR-RH2.3: Swarm normalized artifacts are scored by sc-adversarial-protocol Mode A (not swarm merge)

**Description**: Reflect MUST consume the N normalized per-reviewer artifacts (swarm `final_path`s) as
the input to its existing `sc-adversarial-protocol` Mode A merge. Swarm's `mechanical_merge`
(`merge.py`) output MUST NOT be treated as the adversarial verdict.

**Acceptance Criteria**:

- [ ] The downstream merge step consumes swarm's per-reviewer `final_path` artifacts (suspect-aware).
- [ ] No scoring/ranking/dedup logic is added to `swarm/merge.py` (the LOC ceiling + boundary tests stay green).
- [ ] The adversarial merge produces a convergence score recorded on the reflect contract.

**Dependencies**: `reduce_wave3` (`reduce.py`, `normalize+merge` mode), `sc-adversarial-protocol`.

### FR-RH2.4: A faithful Tier-2 run yields a real adversarial merge with ≥2 distinct model classes

**Description**: A non-mocked Tier-2 run MUST surface, in the reflect `return-contract.yaml`,
`tier_reached: 2`, `merge_method != single-reviewer-fallback`, `reviewer_count >= 2`, and
`t2_model_class_diversity: full`. **Diversity and reviewer_count are measured over the SUCCEEDED
workers (M), not the requested slots (N)** — see FR-RH2.9 for the N→M divergence contract.

**Acceptance Criteria**:

- [ ] On a successful Tier-2 run, `tier_reached == 2`.
- [ ] `merge_method != "single-reviewer-fallback"`.
- [ ] `reviewer_count == M >= 2`, where M = count of `WorkerResult`s with `status == "success"`.
- [ ] `t2_model_class_diversity == "full"` is computed over the **distinct `model_id`s of the M
      succeeded workers** (≥ the expected distinct-class count), NOT over the N requested slots — so two
      surviving workers that resolved to the same model class do NOT count as `full`.

**Dependencies**: FR-RH2.1, FR-RH2.2, FR-RH2.3, FR-RH2.9.

### FR-RH2.9: N→M divergence — partial-failure acceptance boundary is explicit

**Description**: The Tier-2 fan-out is a filtering pipeline: N requested slots reduce to M succeeded
workers (`proxy_error`/`timeout` failures drop count). The faithful-pass boundary, the partial-success
boundary, and the empty boundary MUST be defined so a reader can derive the verdict for any (M, N):

- **M ≥ 2 with ≥2 distinct succeeded model classes** → faithful Tier-2 (PASS-eligible; `status:success`,
  `t2_model_class_diversity:full` when distinct classes ≥ expected).
- **M ≥ 2 but < 2 distinct model classes** (survivors collapsed onto one class) → `degraded`
  (`degraded-model-diversity`), never PASS.
- **M == 1** → `degraded` via `merge_method: single-reviewer-fallback` and/or `tier_reached: 1` (this is
  the SAME path the `--reviewers 1` negative witness reaches; a 3-slot run that loses 2 workers lands
  here too — by design, not a special case).
- **M == 0** (all workers failed / no usable artifacts) → `blocked` (untrustworthy audit; ordered ahead
  of degraded in `derive_verdict`), NOT a silent degrade.

**Acceptance Criteria**:

- [ ] A `--reviewers 3` run with exactly one worker `proxy_error` (after retry) yields `M==2`; PASS-eligible **iff** the 2 survivors are ≥2 distinct model classes, else `degraded-model-diversity`.
- [ ] An M==1 outcome (whether from `--reviewers 1` or from N>1 with N−1 failures) yields `single-reviewer-fallback` and/or `tier_reached==1` — a non-PASS.
- [ ] An M==0 outcome routes `blocked` (exit 2), not `degraded`.

**Dependencies**: FR-RH2.4, `contract.derive_verdict` ordering (`blocked → degraded → halted → pass`).

### FR-RH2.5: Credit-free stub-transport path proves ensemble formation in CI

**Description**: A `--transport stub` (`transports/stub.py`) variant MUST drive the **real** wrapper
(unmocked `dispatch_wave1`/`reduce_wave3`) over a deterministic, network-free transport and assert the
FR-RH2.4 acceptance signals, so CI proves ensemble formation without burning proxy credits.

**Acceptance Criteria**:

- [ ] A test runs the real reflect Tier-2 driver with `--transport stub` and performs no network I/O.
- [ ] The test asserts `tier_reached==2`, `merge_method != single-reviewer-fallback`, `reviewer_count>=2`, `t2_model_class_diversity=="full"`.
- [ ] The test does **not** patch `ClaudeProcess` to copy a canned `tier_reached:2` fixture for the ensemble (it exercises the real fan-out → reduce path).

**Dependencies**: FR-RH2.4, `StubTransport`.

### FR-RH2.6: One-reviewer negative witness must degrade to Tier 1

**Description**: A run configured with a **single** reviewer MUST NOT satisfy the Tier-2 pass signals: it
MUST degrade (e.g. `merge_method: single-reviewer-fallback` and/or `tier_reached: 1`), proving the proof
in FR-RH2.5 is falsifiable and cannot pass vacuously.

**Acceptance Criteria**:

- [ ] A 1-reviewer stub run yields `merge_method == "single-reviewer-fallback"` and/or `tier_reached == 1` (a non-PASS Tier-2).
- [ ] The same assertions used in the positive FR-RH2.5 test FAIL for the 1-reviewer case (witness is genuinely negative).

**Dependencies**: FR-RH2.5.

### FR-RH2.7: Downstream return-contract consumers are unaffected

**Description**: The reflect `return-contract.yaml` shape and the derived `reflect_post:` write-back +
`wrapper-result.yaml` sidecar MUST remain compatible: existing fields keep their names/semantics; the
verdict map and exit codes (`contract.py`, `models.py`) are unchanged.

**Acceptance Criteria**:

- [ ] `derive_verdict` and the `Verdict` exit-code map (`pass→0`, `halted→10`, `degraded→11`, `blocked→2`) are unchanged.
- [ ] `write_reflect_post` produces the same `reflect_post:` field set/order; the sidecar keeps its fields.
- [ ] Existing reflect contract/verdict tests pass without modification.

**Dependencies**: `contract.derive_verdict`, `runner.write_reflect_post`, `runner.write_sidecar`.

### FR-RH2.8: NFR-7 no-in-process-Task guarantee is preserved (or amended on the record)

**Description**: The change MUST NOT introduce `Task(`/`subagent_type` fan-out into the reflect package.
The author MUST confirm whether spawning swarm/proxy workers is permitted by the exact scope of the
NFR-7 guard (`test_no_nesting_guard.py`); if the guard's scope needs to recognize the swarm-driven path,
NFR-7 is amended **deliberately and explicitly**, never silently bypassed.

**Acceptance Criteria**:

- [ ] `test_no_nesting_guard.py` (Layer B: no `Task(`/`subagent`/`anthropic` imports in `runner.py`) passes, including for the new driver module.
- [ ] If NFR-7's prose/scope is amended, the amendment is recorded in this spec (§9) and reflected in the guard's docstring/assertions with rationale.
- [ ] No raw `subprocess.run`/`Popen` is added to the reflect package (the swarm call goes through the swarm CLI surface / `ClaudeProcess`, not a hand-rolled `Popen`).

**Dependencies**: `tests/cli/reflect/test_no_nesting_guard.py`.

## 4. Architecture

### 4.1 New Files

> Files created by this work. Include purpose and dependencies.

| File | Purpose | Dependencies |
|------|---------|-------------|
| `src/superclaude/cli/swarm/lenses/reflect_review.py` | `reflect-review` lens entry: per-reviewer reflection brief, `tier:T2`, `suspect:true`, `/sc:adversarial` next-command (FR-RH2.2) | `swarm.models.LensEntry`, `swarm.schema.CANONICAL_INJECTION_GUARD_SENTENCE` |
| `src/superclaude/cli/swarm/lenses/templates/reflect-review-output.md` | Normalized per-reviewer output template for the lens | (template only) |
| `src/superclaude/cli/reflect/ensemble.py` | Thin Tier-2 driver: build per-reviewer briefs → call `swarm run --lens reflect-review` → collect normalized artifacts → hand to `/sc:adversarial`; map results onto the reflect contract (FR-RH2.1/2.3) | `swarm.dispatch.dispatch_wave1`, `swarm.commands._resolve_run_transport_factory`, `swarm.reduce.reduce_wave3` |
| `tests/cli/reflect/test_ensemble_stub_integration.py` | Non-mocked stub-transport integration proof (FR-RH2.5) + one-reviewer negative witness (FR-RH2.6) | `StubTransport`, real `ensemble.py` |

### 4.2 Modified Files

> Existing files changed. Include nature of change.

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/cli/reflect/runner.py` | `_audit_once` routes Tier-2 ensemble through `ensemble.py` (swarm-driven) instead of relying on the single `claude -p` agent's in-process Task fan-out; Tier-1 launch unchanged | FR-RH2.1 — replaces the broken in-process fan-out seam |
| `src/superclaude/cli/reflect/config.py` | Add resolved fields for transport (`openai_compat`/`stub`), reviewer count, and the proxy-pool source; surface `--transport`/`--reviewers` on the CLI | FR-RH2.1/2.5/2.6 — config plumbing for the swarm-driven path |
| `src/superclaude/cli/reflect/contract.py` | Source `t2_model_class_diversity` / `reviewer_count` / `merge_method` from the swarm-driven ensemble result (proxy model_ids), not the `ANTHROPIC_DEFAULT_*` alias count | FR-RH2.4 — fixes `degraded-model-diversity` at the source while keeping the verdict map intact |
| `src/superclaude/cli/swarm/lenses/__init__.py` (registry) | Register `reflect-review` | FR-RH2.2 |
| `tests/cli/reflect/test_no_nesting_guard.py` | If NFR-7 scope is amended for the swarm-driven path, update the guard docstring/assertions deliberately (Layer B still forbids `Task(`/`subagent` in `runner.py`/`ensemble.py`) | FR-RH2.8 — explicit, recorded amendment only |

### 4.3 Removed Files [CONDITIONAL: refactoring, portification]

> Files or sections removed. Include migration notes.

| File/Section | Reason | Migration |
|-------------|--------|-----------|
| `runner.py` Tier-2 in-process-Task-fan-out reliance (behavioral path inside `_audit_once`, not a file) | This is the broken path: the single `claude -p` agent can't nest Task to spawn reviewers | The audit's Tier-2 fan-out moves to `ensemble.py` (swarm-driven); the Tier-1 launch and the auto-fix loop stay |
| `runner.py:36-41,254-261` `ANTHROPIC_DEFAULT_*_MODEL` alias-count as the Tier-2 diversity source | Caps at ~3 Claude aliases → `degraded-model-diversity` | Diversity now derives from the distinct `T2Model0N` proxy model_ids in the swarm `WorkerResult`s; the alias-count helper may remain for telemetry/sidecar but is no longer the diversity gate input |

### 4.4 Module Dependency Graph

```
cli/reflect/runner.py
   └─ cli/reflect/ensemble.py            (NEW Tier-2 driver)
         ├─ cli/swarm/commands._resolve_run_transport_factory   (per-slot T2Model0N binding)
         ├─ cli/swarm/dispatch.dispatch_wave1                    (ParallelExecutor fan-out)
         ├─ cli/swarm/reduce.reduce_wave3                        (normalize+merge → artifacts + contract)
         ├─ cli/swarm/lenses/reflect_review.LENS                 (NEW lens; per-reviewer briefs)
         └─ /sc:adversarial (sc-adversarial-protocol Mode A)     (downstream scorer; NOT swarm/merge.py)
   └─ cli/reflect/contract.derive_verdict                        (UNCHANGED verdict map)
   └─ cli/reflect/runner.write_reflect_post / write_sidecar      (UNCHANGED write-back)

Boundary invariant: cli/swarm/merge.py stays a mechanical concat (no scoring) — merge.py:9-30.
Isolation invariant (NFR-1): no import of cli.sprint / cli.roadmap; no async/await; no Task( in reflect pkg.
```

### 4.6 Implementation Order

> Dependency-respecting order for implementation. Include parallelization opportunities.

```
1. reflect_review lens + output template        -- swarm-side; no reflect dependency yet
2. ensemble.py thin driver (swarm-driven fan-out + adversarial handoff)   -- depends on 1
   contract.py diversity-source change          -- [parallel with step 2]
3. runner.py _audit_once rewire to ensemble.py  -- depends on 1, 2
4. config.py --transport/--reviewers plumbing   -- depends on 3
5. stub integration test + negative witness     -- depends on 3, 4
6. NFR-7 reconciliation (confirm scope or amend guard deliberately)       -- depends on 3
```

## 5. Interface Contracts [CONDITIONAL: portification, new_feature]

> API contracts, gate criteria, prompt specifications, CLI surface changes.

### 5.1 CLI Surface [CONDITIONAL: new_feature, portification]

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

### 5.3 Phase Contracts [CONDITIONAL: portification, infrastructure]

> For multi-phase workflows. Define inter-phase contracts.

```yaml
# Phase A -> Phase B: reflect Tier-2 driver -> swarm dispatch
phase_a_to_b:
  integration: in_process_library_import  # ensemble.py imports dispatch_wave1 + _resolve_run_transport_factory + reduce_wave3
  cli_equivalent: "superclaude swarm run --lens reflect-review --transport {openai_compat|stub} --output <reflect_out>/t2-swarm"  # OPTIONAL --detached observability variant only (NOT the default inner-loop transport)
  prompt: per_reviewer_briefs            # supplied by the reflect-review lens; NOT a Claude model id
  preflight_openai_compat: [T2ProxyUrl, T2ProxyKey, "T2Model0N (>= reviewers slots)"]
  guard: ModelPoolTooSmallError          # raised eagerly if pool < workers_requested (commands.py:589-609)

# Phase B -> Phase C: swarm reduce output -> sc-adversarial Mode A
phase_b_to_c:
  artifacts: output_files[].final_path   # N normalized per-reviewer artifacts (reduce.py normalize+merge)
  swarm_merged_path: merged.md           # mechanical concat ONLY -- NOT the verdict (merge.py:9-30)
  swarm_contract: return-contract.yaml   # swarm DM-012 contract + done.json sentinel
  scorer: "/sc:adversarial (sc-adversarial-protocol Mode A)"  # consumes final_path artifacts (suspect-aware)

# Phase C -> Phase D: adversarial verdict -> reflect return-contract.yaml (shape PRESERVED)
phase_c_to_d:
  required_fields:
    tier_reached: 2
    merge_method: "<adversarial>"        # MUST NOT be "single-reviewer-fallback" on a faithful run
    reviewer_count: "M (succeeded workers); >=2 for pass"
    t2_model_class_diversity: "full"     # over distinct model_ids of the M SUCCEEDED workers (not N slots)
    adversarial_convergence_score: "<float; recorded TELEMETRY at tier 2, NOT a pass gate (a low score alone does not fail a PASS)>"
  consumed_by: [contract.derive_verdict, runner.write_reflect_post, runner.write_sidecar]
  verdict_map_unchanged: {pass: 0, halted: 10, degraded: 11, blocked: 2}

# Path-confinement invariant (Hohpe): TWO return-contract.yaml files exist.
path_confinement:
  reflect_contract: "<output_dir>/return-contract.yaml"          # the ONLY file reflect.derive_verdict parses
  swarm_subrun_contract: "<output_dir>/t2-swarm/return-contract.yaml"  # swarm DM-012; consumed by ensemble.py only
  rule: "reflect parses output_dir/return-contract.yaml; it MUST NOT parse the t2-swarm/ subdir's contract directly"

# (M, N) divergence guard table (FR-RH2.9) -- M = succeeded workers, N = requested slots.
mn_guard_table:
  - {condition: "M==0 (all workers failed / no artifacts)", verdict: blocked,  exit: 2,  slug: "ensemble-empty"}
  - {condition: "M==1 (>=N-1 failed, or --reviewers 1)",     verdict: degraded, exit: 11, slug: "single-reviewer-fallback"}
  - {condition: "M>=2 but <2 distinct model classes",        verdict: degraded, exit: 11, slug: "degraded-model-diversity"}
  - {condition: "M>=2 AND >=2 distinct classes",             verdict: "pass-eligible", exit: 0, slug: "pass"}

# Worker-status -> M mapping (swarm WorkerResult.status; reduce_wave3 counts success only).
worker_status_to_m:
  success: "counts toward M"
  proxy_error: "does NOT count (retry-once-then-drop per swarm §7 matrix)"
  timeout: "does NOT count"
  parse_error: "does NOT count (salvage may promote per swarm §7.4; post-salvage status governs)"

# --transport enum guard (Whittaker sentinel/divergence).
transport_enum:
  accepted: [openai_compat, stub]
  unknown_value: "rejected at CLI parse (Click enum), before any dispatch -- non-zero exit, no partial run"
```

## 6. Non-Functional Requirements

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

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| External proxy models produce lower-quality reflection reviews than Claude reviewers | Medium | Medium | `suspect: true` framing routes all reviews through `/sc:adversarial` scoring (never trusted raw); ≥2 distinct classes hedge single-model blind spots |
| `merge_method`/`reviewer_count`/`t2_model_class_diversity` not currently emitted by the swarm contract in reflect's expected shape | Medium | High | `ensemble.py` maps swarm `WorkerResult`/`ResultContract` fields onto the reflect contract; FR-RH2.7 + existing contract tests pin the shape |
| NFR-7 guard scope ambiguity (does it forbid the swarm-driven path?) | Medium | High | FR-RH2.8: confirm Layer-B scope (it forbids `Task(`/`subagent`/`anthropic` imports, not HTTP workers); amend the guard prose deliberately and record in §9 if needed |
| `ModelPoolTooSmallError` when `T2Model0N` pool < `--reviewers` | Medium | Low | Default `--reviewers 3` with a 4-slot pool; surface the guard's actionable message (add slots or reduce count) verbatim; preflight before dispatch |
| Stub transport diverges from live proxy behavior, hiding a real defect | Low | Medium | Stub proves *formation* (tier/merge_method/count/diversity), not review *content*; a live-proxy E2E (§8.3) covers content; negative witness guards vacuity |
| Adversarial scorer receives swarm `merged.md` instead of per-reviewer artifacts | Low | High | FR-RH2.3 + §5.3 phase contract: scorer consumes `output_files[].final_path`, never `merged.md`; boundary tests on `merge.py` stay green |
| Tier-2 latency increases (HTTP fan-out + adversarial pass) | Medium | Low | Parallel fan-out via `ParallelExecutor`; per-worker `timeout_sec` (NFR-010); `--detached`/tmux for long headless runs |
| Auto-fix loop cost multiplier — each re-audit re-runs the full ensemble | Medium | Low | The `--fix` loop calls the swarm-driven ensemble once per audit (idempotent re-verify, NFR-4): up to `(max_fix_iterations+1) × reviewers` proxy calls. Bounded by `max_fix_iterations` (default 2); `--transport stub` re-audits are free; surfaced so operators size proxy credits |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_reflect_review_lens_registered` | `tests/swarm/test_lenses.py` (or new) | `reflect-review` passes the lens validator; `suspect:true`; `/sc:adversarial` + `{suspect_files}` in next-command (FR-RH2.2) |
| `test_ensemble_binds_distinct_models` | `tests/cli/reflect/test_ensemble.py` | `ensemble.py` binds slot `i`→`T2Model0N`; distinct `model_id`s; `ModelPoolTooSmallError` when pool < reviewers (FR-RH2.1) |
| `test_diversity_from_proxy_modelids` | `tests/cli/reflect/test_contract.py` | `t2_model_class_diversity` derives from distinct swarm `model_id`s, not the Claude alias count (FR-RH2.4) |
| `test_verdict_map_unchanged` | `tests/cli/reflect/test_contract.py` (existing) | `pass→0/halted→10/degraded→11/blocked→2` intact (FR-RH2.7) |
| `test_no_nesting_guard` (extended) | `tests/cli/reflect/test_no_nesting_guard.py` | No `Task(`/`subagent`/`anthropic` import in `runner.py`/`ensemble.py`; no raw subprocess (FR-RH2.8) |
| `test_merge_mechanical_only` (existing, must stay green) | `tests/swarm/test_merge_mechanical_only.py` | `swarm/merge.py` gains no scoring logic (FR-RH2.3) |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_ensemble_stub_integration_positive` | Real wrapper + `--transport stub` (no network): `tier_reached==2`, `merge_method != single-reviewer-fallback`, `reviewer_count>=2`, `t2_model_class_diversity=="full"` (FR-RH2.5) — NOT a mocked `ClaudeProcess` canned-fixture path |
| `test_ensemble_one_reviewer_negative_witness` | 1-reviewer stub run degrades (`single-reviewer-fallback` and/or `tier_reached==1`); the positive assertions FAIL here (FR-RH2.6) |
| `test_ensemble_partial_failure_2_of_3` | N=3, one worker fails → M=2: PASS-eligible iff 2 distinct classes, else `degraded-model-diversity` (FR-RH2.9) |
| `test_ensemble_duplicate_survivor_classes_degrade` | M=2 survivors on the SAME model class → `degraded-model-diversity`, NOT `full` (FR-RH2.4 diversity-over-survivors) |
| `test_ensemble_all_fail_routes_blocked` | M=0 (all workers fail) → `blocked` (exit 2), not `degraded` (FR-RH2.9) |
| `test_return_contract_shape_preserved` | `reflect_post:` write-back + sidecar field set/order unchanged through the swarm-driven path (FR-RH2.7) |

### 8.3 Manual / E2E Tests [CONDITIONAL: infrastructure, portification]

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| Live proxy Tier-2 ensemble | `superclaude reflect run <tasklist> --depth deep --transport openai_compat --reviewers 3` with `~/.aienv` (`:4000/cli`, `T2Model01..04`) loaded | Real adversarial merge; `tier_reached:2`; `merge_method` non-fallback; ≥2 distinct proxy `model_id`s; `t2_model_class_diversity:full`; faithful (no single-reviewer-fallback) |
| Headless observability | Run the Tier-2 swarm subrun `--detached` (tmux); poll `<reflect_out>/t2-swarm/done.json` | `done.json` sentinel appears at terminal status; run pollable without attaching; durable artifacts under the output dir |
| Pool-too-small guard | Set `--reviewers 5` with a 4-slot `T2Model0N` pool | `ModelPoolTooSmallError` raised at preflight with the actionable "add slots or reduce count" message; no partial dispatch |
| `claude -p` regression check | Re-run the original L2d/T3 repro under the new path | Ensemble forms (no subagent→agent nesting); the original degrade-to-tier-1 no longer reproduces |

## 9. Migration & Rollout [CONDITIONAL: refactoring, portification]

> How to transition from current state to new state. Breaking changes, backwards compatibility.

- **Breaking changes**: None to the **public** contract. The `return-contract.yaml` shape, the
  `reflect_post:` write-back, the `wrapper-result.yaml` sidecar, and the verdict→exit-code map are
  preserved (FR-RH2.7). The internal Tier-2 audit *mechanism* changes (in-process Task fan-out →
  swarm-driven external fan-out); this is invisible to downstream consumers.
- **Backwards compatibility**:
  - Default transport is `openai_compat`; operators with the `~/.aienv` contract (`:4000/cli`,
    `T2Model01..NN`) get the faithful path with no flag changes.
  - `roadmap validate`'s separate-process-per-agent model (`validate_executor.py:317-373`) is the
    proven reference for external-fan-out reflection and remains untouched.
  - Existing reflect tests run unchanged (NFR-RH2.6); the mocked-`ClaudeProcess` suite still covers the
    Tier-1 launch + verdict/write-back paths.
- **NFR-7 reconciliation (explicit, on the record)**: Layer B of `test_no_nesting_guard.py` forbids
  `Task(`/`subagent`/`anthropic` imports in `runner.py`. The swarm-driven path uses **external HTTP
  workers via `dispatch_wave1`**, which is not the in-process Agent/Task surface NFR-7 targets, so the
  *guarantee* (no `claude -p` self-nesting) is preserved and in fact strengthened. The guard is extended
  to also scan `ensemble.py`. If the guard's prose needs to name the swarm-driven path as the sanctioned
  fan-out, that amendment is made deliberately here and mirrored in the guard docstring with rationale —
  never via `--no-verify`, `subagent_type`, or a silent exemption.
  - **OI-2/Q2 DECISION (2026-06-20): CONFIRM (no scope amendment).** Layer-B's existing intent — "no
    in-process Agent/Task self-nesting" — already covers the swarm-driven path, because the Tier-2
    ensemble fans out to **external HTTP workers** through `dispatch_wave1` (`ParallelExecutor` +
    `Transport`), not the Agent/Task tool surface. No NFR-7 prose change is required; the guarantee is
    unchanged (and strengthened — the broken `claude -p` double-nesting is removed). What changed is
    purely COVERAGE: `test_no_nesting_guard.py` now adds an `_ENSEMBLE_SRC` reader and asserts the same
    `Task(`/`subagent`/`anthropic`-import + raw-`subprocess.run`/`Popen` bans over `ensemble.py` as over
    `runner.py`, and asserts `ClaudeProcess` (the sole sanctioned inference launch) is present in
    `ensemble.py` for the adversarial Mode-A scorer (Phase 0.3 launch-site decision). The
    `_REFLECT_PY`-globbed sprint/roadmap-import + `async`/`await` bans already auto-covered `ensemble.py`.
    This decision and its rationale are mirrored verbatim in the guard's docstrings/assertions.
- **Rollback plan**: The change is gated behind the Tier-2 audit seam in `_audit_once`. If the
  swarm-driven ensemble regresses in production, revert `runner.py`'s `_audit_once` rewire (and config
  plumbing) to the prior single-`claude -p` launch; the `reflect-review` lens and `ensemble.py` are
  additive and inert when not wired. Because the contract shape is unchanged, rollback does not touch
  downstream consumers.

## 10. Downstream Inputs

> What this spec feeds into. How downstream consumers (sc:roadmap, sc:tasklist, etc.) use the output.

### For sc:roadmap

Themes: (1) **Swarm lens** — `reflect-review` lens + template + registry; (2) **Reflect Tier-2
driver** — `ensemble.py` (swarm fan-out + adversarial handoff) and the `_audit_once` rewire; (3)
**Diversity source migration** — `contract.py`/`runner.py` diversity from proxy `model_id`s; (4)
**Proof harness** — non-mocked stub integration test + negative witness; (5) **NFR-7 reconciliation**.
Milestones land in implementation order (§4.6): lens first (no reflect dependency), then driver +
contract change (parallelizable), then runner rewire, then config plumbing, then the proof harness, then
the guard reconciliation.

### For sc:tasklist

Suggested task granularity, each independently testable:
1. `reflect-review` lens + output template; lens-validator unit test.
2. `ensemble.py` driver: per-slot model binding + `ModelPoolTooSmallError` surfacing + adversarial
   handoff; unit test for distinct-model binding.
3. `contract.py` diversity-source change; unit test asserting diversity from proxy `model_id`s.
4. `runner.py` `_audit_once` rewire to `ensemble.py`; Tier-1 launch untouched.
5. `config.py` `--transport`/`--reviewers` plumbing; clamp `[2,4]`.
6. Non-mocked `--transport stub` integration test (positive) + one-reviewer negative witness.
7. Extend/reconcile `test_no_nesting_guard.py` for `ensemble.py`; record any NFR-7 amendment.
8. Live-proxy E2E + headless observability manual checks (§8.3).

## 11. Open Items

> Unresolved questions. Each should have an owner and deadline. Empty section means all questions resolved.

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OI-1 (**BLOCKING GATE**) | Does reflect's swarm contract already emit `reviewer_count`/`merge_method`/`t2_model_class_diversity` in the exact shape `contract.derive_verdict` reads, or must `ensemble.py` map them? Produce an explicit swarm-`ResultContract`-field → reflect-contract-field correspondence table. | High — load-bearing for FR-RH2.4/2.7; the asserted shape-preservation rests on it | **Resolve BEFORE any FR-RH2.3 code lands** (Newman): diff swarm DM-012 vs the fields `derive_verdict` reads; the mapping layer in `ensemble.py` is sized by this table |
| OI-2 | Exact NFR-7 amendment text (if any) — does Layer-B's intent already cover HTTP workers, or does the prose need updating? | Medium — touches the no-nesting guarantee wording | During FR-RH2.8; decide confirm-vs-amend, record in §9 |
| OI-3 | Should `--transport stub` be auto-selected in CI, or always opt-in? | Low — CI ergonomics | Before FR-RH2.5 lands |
| OI-4 | How does `/sc:adversarial` Mode A treat `suspect: true` reflect-review artifacts vs bare-review ones (any rubric difference)? | Low-Medium — scoring fidelity | During FR-RH2.3; confirm against `sc-adversarial-protocol` |

## 12. Brainstorm Gap Analysis

> Auto-populated by `sc:cli-portify` Phase 3c embedded brainstorm pass. For manually created specs, use `/sc:brainstorm` to identify gaps.

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G-1 | Swarm contract field parity with reflect's expected contract not yet byte-verified | High | §5.3, §11 OI-1 | architect |
| G-2 | NFR-7 guard scope vs swarm-driven path not yet adjudicated | High | §6, §9, §11 OI-2 | qa |
| G-3 | Review *content* quality of external proxy models is unproven by the stub path | Medium | §7, §8.3 | analyzer |
| G-4 | `suspect:true` rubric handoff symmetry between reflect-review and bare-review unconfirmed | Low | §11 OI-4 | analyzer |

Gap analysis summary: The two High-severity gaps (G-1 contract parity, G-2 NFR-7 scope) are both
resolvable before code lands — G-1 by diffing the swarm `ResultContract` against the fields
`contract.derive_verdict` reads, G-2 by adjudicating the guard's intent and recording the
confirm-or-amend decision in §9. Neither blocks the architecture; both are wiring/record-keeping. G-3 is
deliberately accepted: the stub proves *formation*, the live E2E (§8.3) proves *content*, and the
negative witness prevents vacuous passes.

---

## Appendix A: Glossary [CONDITIONAL: all types -- include if domain-specific terminology used]

| Term | Definition |
|------|-----------|
| Tier-2 ensemble | The reflect post-execution audit's heterogeneous reviewer fan-out (2-3 reviewers on different model classes) merged via `sc-adversarial-protocol` Mode A |
| In-process Task fan-out | A headless `claude -p` agent spawning reviewers via the Task tool inside its own process — the broken path that fails on subagent→agent nesting |
| Swarm-driven fan-out | Reviewer fan-out via `superclaude swarm run` → `dispatch_wave1` over `ParallelExecutor`, with external OpenAI-compatible HTTP workers |
| `single-reviewer-fallback` | The `merge_method` swarm/reflect records when the ensemble collapses to one reviewer; routes `degraded` (`contract.py:280-281`) |
| `t2_model_class_diversity` | Contract field: `full` when ≥ expected distinct model classes participate; non-`full` routes `degraded-model-diversity` (`contract.py:266-269`) |
| `T2Model0N` | Env-contract proxy model slots (`~/.aienv`, `T2Model01..NN` on base `:4000/cli`); one distinct model per worker slot |
| `ModelPoolTooSmallError` | Swarm guard (`commands.py:589-609`) raised when the `T2Model0N` pool is smaller than the worker count (prevents silent model reuse) |
| Negative witness | A 1-reviewer test that MUST fail the Tier-2 pass assertions, proving the positive proof is falsifiable |
| `suspect: true` | Reviewer-artifact flag meaning "never trust raw — route through `/sc:adversarial` scoring" |

## Appendix B: Reference Documents [CONDITIONAL: all types -- include if external references needed]

| Document | Relevance |
|----------|-----------|
| `src/superclaude/skills/sc-bare-review/SKILL.md` | Precedent: thin caller over `swarm run --lens bare-review` handing normalized artifacts to `/sc:adversarial` |
| `src/superclaude/cli/swarm/dispatch.py` (`dispatch_wave1`, ~L334) | Per-reviewer parallel fan-out over `ParallelExecutor`; per-slot `WorkerResult` recording |
| `src/superclaude/cli/swarm/commands.py` (`_resolve_run_transport_factory`, ~L612; `ModelPoolTooSmallError`, L589-609) | Per-slot `T2Model0N` binding + too-small-pool guard |
| `src/superclaude/cli/swarm/merge.py` (L9-30) | Boundary contract: mechanical concat only; scoring forbidden; hands off to `/sc:adversarial` |
| `src/superclaude/cli/swarm/reduce.py` (`reduce_wave3`) | `normalize+merge` mode → per-reviewer `final_path` artifacts + contract + `done.json` |
| `src/superclaude/cli/swarm/transports/stub.py` | Deterministic, network-free transport for the credit-free CI proof |
| `src/superclaude/cli/reflect/runner.py` (`_build_prompt` L341-366; `_audit_once` L392-428) | The single-`claude -p` launch + in-process-fan-out reliance being replaced |
| `src/superclaude/cli/reflect/contract.py` (`derive_verdict`; degraded triggers L249-304) | The verdict map + diversity/merge_method/single-reviewer degrade triggers (preserved) |
| `tests/cli/reflect/conftest.py` (L98-138) | The mocked-`ClaudeProcess` fixture path that hid the defect |
| `tests/cli/reflect/test_no_nesting_guard.py` | NFR-7 guard (Layer A skill shell-out, Layer B runner imports) |
| `src/superclaude/cli/roadmap/validate_executor.py` (L317-373) | Proven separate-process-per-agent reference for external-fan-out reflection |
