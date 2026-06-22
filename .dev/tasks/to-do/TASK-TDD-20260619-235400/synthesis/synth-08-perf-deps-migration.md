# Synthesis 08 — Performance, Dependencies & Migration (TDD §§16-19)

**Feature**: FR-RH2 — Headless Ensemble Fix (drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library)
**Target release**: 4.4.0 | **Complexity**: HIGH (0.82)
**Covers TDD sections**: §16 Accessibility, §17 Performance Budgets, §18 Dependencies, §19 Migration & Rollout Plan
**Source research**: 00-prd-extraction, 01-reflect-runner-seam, 03-swarm-dispatch, 07-nfr7-guard-test-harness, 08-precedents-adversarial-handoff, 09-reflect-config-cli-surface
**Binding directives**: D4 (recipe binding + net-new lens module), D7 (3-file ReflectConfig edit; `--depth` exists; `expected_tier` at runner.py:403)
**Date**: 2026-06-20
**Status**: Complete

> All facts are derived from the cited research files (which carry `[CODE-VERIFIED]` tags against the shipped source). No fabrication. Where a value is a design obligation rather than an observed fact, it is marked as such.

---

## 16. Accessibility Requirements

**N/A — backend CLI library, no client surface.**

**Rationale:** FR-RH2 modifies the `superclaude reflect` CLI package (`src/superclaude/cli/reflect/`) and the in-process swarm dispatch library (`src/superclaude/cli/swarm/`). The component type is **Library / Backend** — its entire surface is a Click command (`superclaude reflect run`), an in-process Python driver module (`ensemble.py`), a swarm lens module (`lenses/reflect_review.py`), and YAML/markdown artifacts (`return-contract.yaml`, normalized reviewer `final_path` bodies). There is **no rendered UI, no DOM, no screen-reader target, no color/contrast surface, and no keyboard-navigable client**. WCAG 2.1 AA criteria (keyboard navigation, ARIA, contrast ratios, focus management, alt text, form labels) have no applicable artifact here.

The template's §16 conditional applicability matches the frontend-only markers on §§9-10: this TDD is a backend/library spec, so the template's "Backend services, infrastructure, and libraries should skip this section entirely" guidance applies.

**The closest analogue to an accessibility concern — operator legibility of CLI output — is covered elsewhere, not here:**

- Terminal output legibility and the `--tui` dashboard live under §14 Observability (the swarm `--tui` / `--detached` / tmux + `done.json` sentinel surface, NFR-RH2.7).
- Exit-code and verdict legibility (the `pass→0 / halted→10 / degraded→11 / blocked→2` contract) is an API/contract concern under §8 / §12, not an accessibility one.

No accessibility testing tools (axe, Lighthouse a11y, screen readers) are in scope.

---

## 17. Performance Budgets

> **Scope note:** This is a CLI-infrastructure feature, not a latency-SLO web service. There is no FCP/LCP/CLS surface (§17.1 frontend table is N/A — see §16). The performance envelope is dominated by **N parallel external proxy calls** (the Tier-2 reviewer fan-out) and the **auto-fix loop multiplier**. The budgets below are about *how many proxy calls happen, how long each is allowed to take, and how failures bound the wall-clock*, not about p50/p95 of an HTTP endpoint.

### 17.1 Frontend Performance

**N/A** — no client/browser surface (see §16). FCP/LCP/FID/CLS/TTI/bundle-size budgets do not apply.

### 17.2 Reviewer Fan-Out & Loop Cost (the real budget)

The Tier-2 ensemble fans `prompt` across `workers_requested` (= N) reviewer slots **strictly through `ParallelExecutor`** — `dispatch_wave1` is forbidden from instantiating `ThreadPoolExecutor` directly (AC-004), and sets `executor.quiet = True` (FR-1 single-writer discipline). All N reviewer HTTP calls run concurrently, so the wall-clock floor of one audit is **one worker's latency, not N×**; the ceiling is governed by the per-worker timeout matrix below. [03-swarm-dispatch §1, §4]

| Budget dimension | Value | Source / measurement |
|---|---|---|
| Reviewer slots per audit (N) | `--reviewers`, clamped `[2,4]`, default **3** (1 = negative-witness degrade) | CLI surface, 00-prd-extraction §4; 09 §1c |
| Fan-out concurrency | All N slots in **one** parallel group (`depends_on=[]`), via `ParallelExecutor(max_workers=N)` | 03-swarm-dispatch §4 |
| Per-worker default timeout | **180s** (`_DEFAULT_TIMEOUT_SEC = 180`, NFR-010), forwarded to `transport.send(prompt, timeout_sec)` so httpx timeout == dispatcher budget | 03-swarm-dispatch §2 |
| 5xx retry | **once** (`on_5xx=True`, `on_5xx_backoff_sec=2`); `elapsed_ms` cumulative across attempts, **backoff sleep excluded** | 03-swarm-dispatch §2 |
| 4xx / timeout / network retry | **none** (`on_4xx=False`, `on_timeout=False`, no `on_network` flag) | 03-swarm-dispatch §2 |
| Worst-case single-worker wall-clock | `180s` (timeout) `+ 2s` (backoff) `+ 180s` (one 5xx retry) ≈ **362s** for a slot that 5xx-retries then times out | derived from the §2 matrix (timeout 180 + retry path) |
| Per-audit wall-clock (parallel) | ≈ **max over surviving slots** of the above (not sum) — the slowest reviewer paces the audit | `ParallelExecutor` `as_completed` semantics, 03-swarm-dispatch §4 |

#### Per-worker timeout / retry matrix (NFR-010 / §7 swarm matrix)

| Outcome | `http_code` | Retry? | `attempts` | Cost impact |
|---|---|---|---|---|
| `success` | 200 | no | 1 | 1 proxy call |
| `proxy_error` 4xx | 400-499 | no | 1 | 1 proxy call, drops from M |
| `proxy_error` 5xx | 500-599 | **yes, once** | 1 or 2 | up to 2 proxy calls |
| `timeout` | `None` | no | 1 | 1 proxy call (≤180s), drops from M |
| network/other | `None` | no | 1 | 1 proxy call, drops from M |
| `parse_error` | 200 | no | 1 | 1 proxy call; salvage may promote (Wave-2) |

### 17.3 M-Survivor Reduction (N→M filtering)

The fan-out is a **filtering pipeline**: N requested slots reduce to M succeeded workers. Only `WorkerResult.status == "success"` counts toward M; `proxy_error` / `timeout` / `parse_error` slots are excluded (the success predicate dispatch itself uses at `dispatch.py` L496). This is a **performance-relevant correctness budget**, not just a verdict rule: diversity and `reviewer_count` are measured over **M, never N**, so a run that requested 3 reviewers but had 1 fail still pays for 3 proxy calls while only crediting 2 toward the merge. [03-swarm-dispatch §5; 00-prd-extraction §5]

| M outcome | Verdict | Cost note |
|---|---|---|
| M ≥ 2, ≥2 distinct model classes | pass-eligible | full merge over M artifacts |
| M ≥ 2, <2 distinct classes | degraded (`degraded-model-diversity`) | proxy calls spent, no PASS |
| M == 1 | degraded (`single-reviewer-fallback`) | N proxy calls spent, no real ensemble |
| M == 0 | blocked (`ensemble-empty`) | N proxy calls spent, untrustworthy audit |

### 17.4 Auto-Fix Loop Cost Multiplier

The bounded auto-fix loop (FR-1/FR-3) calls `_audit_once()` once per cycle (`runner.py` L536-537), with **`--max-fix-iterations` default 2** (D3). Each Tier-2 `_audit_once` invocation drives a **fresh N-reviewer fan-out**. The proxy-call ceiling for one `superclaude reflect run --fix` is therefore:

```
total reviewer proxy calls  ≤  (max_fix_iterations + 1) × reviewers × (1 + 5xx-retry factor)
                            =   (2 + 1) × N            × (up to 2 on all-5xx)
```

- **Live path (`--transport openai_compat`):** up to `(max_fix_iterations+1) × reviewers` = **3 × N** ensemble fan-outs of real proxy calls (default N=3 → up to **9** base reviewer calls, up to ~18 if every slot 5xx-retries). Each fan-out also feeds one `/sc:adversarial` Mode A merge.
- **Stub path (`--transport stub`):** re-audits are **free** — `StubTransport` is deterministic and network-free (FR-RH2.5/NFR-RH2.4), so the loop multiplier carries **zero proxy/credit cost** in CI. The multiplier still exercises the real dispatch→reduce→derive path, just without wire I/O. [07-nfr7-guard §4-5]

> **CRITICAL budget guardrail:** the multiplier is bounded by `max_fix_iterations` (terminal HALT at the cap, D3). Without the cap, a non-converging fix loop would multiply proxy spend unboundedly. The cap is the cost ceiling.

### 17.5 Measurement Methods

| What to measure | Method |
|---|---|
| Per-worker latency / attempts / status | `WorkerResult.elapsed_ms`, `.attempts`, `.status`, `.model_id` (12-field DM-013 dataclass) | 
| Reviewer fan-out actually happened (not no-op) | `execution-log.jsonl` `worker_done` event count == N (swarm behavioral-artifact witness, `test_commands_run.py` L559-568) |
| M-survivor count / diversity | `reduce_wave3` `ResultContract` `workers_succeeded` (M) + distinct `model_id` over succeeded set |
| Loop multiplier / convergence | `ReflectResult.fix_iterations` (= `iteration-1`, `runner.py` L575), `fix_converged` (L576) |
| Credit-free proof | `--transport stub` test asserts zero network I/O (imports no httpx wire path, NFR-RH2.4) |

> **Note:** No new APM / load-test / soak-test tooling is introduced. Performance is observed off the existing swarm artifacts (`WorkerResult`, `ResultContract`, `execution-log.jsonl`) and the reflect sidecar (`wrapper-result.yaml`). The §17.3 frontend/load-test rows of the template are N/A.

---

## 18. Dependencies

> FR-RH2 is, by design, a **reuse-by-import** feature: it adds no new third-party package — it composes already-shipped in-process swarm functions and an existing external proxy contract. The dependency surface is therefore almost entirely *internal* + *infrastructure*, not external PyPI packages. [01-reflect-runner-seam reuse-audit; 08-precedents §1]

### 18.1 External Dependencies

| Dependency | Version | Purpose | Risk | Fallback |
|---|---|---|---|---|
| T2Model0N proxy (OpenAI-compatible) | N/A (service) — base `:4000/cli`, models `T2Model01..NN` per `~/.aienv` (`T2ProxyUrl` / `T2ProxyKey`) | The live Tier-2 reviewer fan-out transport (`--transport openai_compat`); supplies true cross-vendor model-class diversity | **H** — external network service; if down/credit-exhausted, all N workers `proxy_error`/`timeout` → M==0 → `blocked` (exit 2) | `--transport stub` (deterministic, network-free) for CI/offline; live proxy failure is an honest `blocked`, not a silent degrade. Proxy contract is **fixed**: only `:4000/cli` base + `T2Model01..NN` (NFR-RH2.8); never probe `:4000/v1` / `:8317` |
| `httpx` (transitive, via swarm `openai_compat` transport) | existing pin (no change) | Wire transport for proxy calls; timeout bound to the 180s dispatcher budget | **L** — already a shipped swarm dependency, not new | `StubTransport` imports no httpx wire path (NFR-RH2.4) |

> No new PyPI dependency is added by FR-RH2. `pytest` / `click` / `rich` (existing project deps) are unchanged.

### 18.2 Internal Dependencies

| Dependency | Symbol / Location | Status | Interface | Risk |
|---|---|---|---|---|
| Swarm Wave-1 fan-out | `dispatch_wave1` (`swarm/dispatch.py` L334) | Shipped, stable, **sync** | `(preflight_result, transport=None, *, transport_for_slot=None, prompt="", parallel_executor=None, worker_spec=None, logger=None) -> list[WorkerResult]` | **L** — public, stable, all-sync; one `WorkerResult` per slot guaranteed |
| Per-slot transport factory | `_resolve_run_transport_factory` (`swarm/commands.py` L612) | Shipped — **PRIVATE symbol** (`_`-prefixed) | `(transport_kind, *, models=None, env=None, workers_requested=None) -> Callable[[int], Transport]`; binds slot `i` → `T2Model0N` (openai_compat) or shared `StubTransport` (stub) | **M** — **cross-package import of a private symbol is a coupling smell.** No public swarm transport-factory API exists (both `_resolve_run_transport` L510 and `_resolve_run_transport_factory` L612 are private — `[CODE-CONTRADICTED]` that a public equivalent exists). The TDD must either import the private factory (and record the coupling) or recompose the public `read_env` (`transports/openai_compat.py` L159) + transport classes directly |
| Swarm Wave-3 reduce | `reduce_wave3` (`swarm/reduce.py` L555) | Shipped, **sync** | `(worker_results, mode="normalize+merge", *, output_dir=None, workers_requested=None, ...) -> ResultContract`; can write `merged.md` + `return-contract.yaml` to a caller-supplied `output_dir` | **L** — public, sync. Emits **swarm** `ResultContract` (`swarm/models.py` L877), which `ensemble.py` must **translate** into the **reflect** contract shape before landing it at `config.contract_path` (OI-1, the BLOCKING gate) |
| `WorkerResult` shape (DM-013) | `swarm/models.py` L1026 | Shipped | 12-field dataclass; load-bearing: `status` (`WorkerStatus` Literal), `model_id`, `model_label`, `final_path`, `elapsed_ms` | **L** — stable; `__post_init__` validates `status` enum |
| `ParallelExecutor` | `execution/parallel.py` L80 | Shipped | The single sanctioned parallelism seam (AC-004); `quiet=True` under dispatch | **L** |
| `/sc:adversarial` Mode A | `sc-adversarial-protocol/SKILL.md` (`--compare`, L24-69, L527-656) | Shipped | `--compare file1,…file10` (2-10 files); returns `convergence_score` / `merged_output_path` → recorded as reflect `adversarial_convergence_score` | **M** — see OI-4 / §18.4 risk: **`--suspect-source` is emitted by the swarm/bare-review side but is NOT documented or parsed in the adversarial SKILL** (`[CODE-CONTRADICTED]`). Reflect's handoff must rely on `--compare` (suspect handling advisory) or the protocol must be taught the flag |
| `reflect-review` lens recipe binding | `recipes/__init__.py` `REGISTRY` L182 / `STRATEGIES` L209 — reuse **`bare-review-v1`** | Shipped (reused) | Lens validator assertions 2 (`_validate.py` L357-391) & 6 (L493-532) satisfied with **zero recipe-package edits** by reusing `bare-review-v1` (Path A, D4) | **L** — reuse path adds no recipe code; only valid if reflect-review prompt emits the same findings-table-with-`suspect` shape `BareReviewV1` normalizes |
| Reflect verdict/contract core | `contract.derive_verdict`, `models.Verdict`, `runner.write_reflect_post` / `write_sidecar` | Shipped — **unchanged** by FR-RH2 | Verdict map + exit codes preserved (FR-RH2.7); `ensemble.py` only feeds the pinned `return-contract.yaml` these already consume | **L** — explicitly out-of-scope to change |

### 18.3 Infrastructure Dependencies

| Resource | Type | Environment | Configuration |
|---|---|---|---|
| `~/.aienv` proxy env | Env-file contract | Live (openai_compat) | Provides `T2ProxyUrl` (`:4000/cli`), `T2ProxyKey`, `T2Model01..NN`. Read via swarm `read_env` (`transports/openai_compat.py` L159) preflight. **Only** these endpoints/models — no `:4000/v1`, `:8317` probing (NFR-RH2.8) |
| `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` aliases | Env vars | Tier-1 grounded pass (unchanged) | Reflect Tier-1 / `count_model_aliases` diversity source (cap 3 Claude classes), recorded as sidecar-only `env_alias_count`. **Note the reconciliation work**: Tier-2 ensemble now sources diversity from the `T2Model0N` proxy pool, a *different* pool than these aliases — the ensemble must populate `t2_model_class_diversity` honestly from whichever pool it actually used [01 §d caveat 3] |
| `<output_dir>/return-contract.yaml` | Pinned artifact path | All | The single integration contract: `config.contract_path = output_dir / "return-contract.yaml"` (`models.py` L88-91). **Path-confinement invariant**: reflect parses ONLY this file; the swarm subrun's `<output_dir>/t2-swarm/return-contract.yaml` is consumed by `ensemble.py` only, never parsed directly by `reflect.derive_verdict` (00-prd-extraction §5.3) |
| `StubTransport` | In-process fake | CI / `--transport stub` | Deterministic, network-free reviewer responses; drives the **real** dispatch→reduce path (not a canned-fixture copy) |
| tmux + `done.json` sentinel + `--tui` | Observability infra | Optional `--detached` variant | NFR-RH2.7 pollability for headless Tier-2 runs; **observability only, not the default inner-loop transport** (08 §4.4) |

### 18.4 Dependency Risk Callouts

- **`_resolve_run_transport_factory` private-symbol coupling (M):** the cleanest reuse path imports a `_`-prefixed cross-package symbol. There is provably no public equivalent. The TDD should record this coupling explicitly (§20 Risks) and decide import-private vs recompose-from-`read_env`.
- **swarm `ResultContract` → reflect contract translation (OI-1, BLOCKING):** the real integration work; the mapping layer in `ensemble.py` is sized by the field-correspondence table OI-1 must produce **before** FR-RH2.3 code lands.
- **`--suspect-source` seam gap (M):** emitted by the lens, unparsed by `/sc:adversarial`. Reflect must hand off via `--compare` with suspect handling advisory (OI-4 resolves to "no rubric difference today, because Mode A doesn't read `suspect` at all"), or the protocol is taught the flag (out of FR-RH2 scope).

---

## 19. Migration & Rollout Plan

> **What is migrating:** the Tier-2 reviewer-ensemble launch mechanism — **from** the broken single-`claude -p` in-process Task fan-out **to** the in-process swarm-driven external-proxy ensemble. This is a *mechanism swap behind a preserved contract*, not a data migration. There is no persisted state, no schema version bump, no user data to move. The `return-contract.yaml` shape and the verdict→exit-code map are unchanged (FR-RH2.7), so downstream consumers (`reflect_post:` write-back, `wrapper-result.yaml` sidecar) are unaffected.

### 19.1 Migration Strategy

| Phase | Description | Duration | Rollback Plan |
|---|---|---|---|
| Phase 0 — OI-1 gate (BLOCKING) | Produce the swarm `ResultContract` → reflect-contract field-correspondence table. Sizes the `ensemble.py` mapping layer. **Must land before any FR-RH2.3 code.** | — | N/A (analysis gate; nothing to roll back) |
| Phase 1 — Additive scaffolding (inert) | Add `cli/reflect/ensemble.py` (in-process swarm driver) + `lenses/reflect_review.py` (net-new lens, D4) + reuse `bare-review-v1` recipe binding. **Not yet wired into `_audit_once`.** | 1 sprint | Delete the two new files; nothing references them |
| Phase 2 — Config plumbing (3-file edit, D7) | Add `transport` + `reviewers` to `ReflectConfig` (`models.py` tail), `resolve_config` (`config.py`), Click options (`commands.py`). `--depth` already exists — do NOT re-add. | within Phase 1 | Revert the 3-file diff; new fields are unreferenced until Phase 3 |
| Phase 3 — Rewire `_audit_once` | Branch `_audit_once` on `expected_tier`: route `expected_tier==2` into `ensemble.py`; keep `expected_tier==1` on the single `ClaudeProcess` path. Parse+derive tail (`runner.py` L420-427) untouched. | within Phase 1 | Revert the `_audit_once` branch (one method); ensemble.py + lens become inert again |
| Phase 4 — Guard extension + proof | Extend NFR-7 guard to `ensemble.py` (§19.5); land FR-RH2.5 stub-integration test (positive ≥2 + negative 1-reviewer witnesses). | within Phase 1 | Revert guard/test additions |

### 19.2 The 3-File ReflectConfig Edit (D7 migration mechanics)

`ReflectConfig` is a dataclass in **`models.py:57-91`** (NOT `config.py` — `config.py` imports it via `from .models import ReflectConfig`). Adding each new resolved field is a **strict 3-file chain**:

1. **`models.py`** — append the field at the **tail** of the dataclass, after `max_fix_iterations` (line 86), per the documented "append at tail to respect field-ordering" rule: `transport: str` then `reviewers: int`.
2. **`config.py` `resolve_config()`** — add the keyword param (`transport: str = "openai_compat"`, `reviewers: int = 3`), the resolution/validation logic (transport-validate + reviewers clamp/branch in the `config.py:190` depth-floor region), and the constructor kwarg in the `ReflectConfig(...)` call.
3. **`commands.py`** — add the `@click.option` (after `--depth` at L106; `--transport` uses the `click.Choice` idiom, `--reviewers` is `type=int, default=3`), the `run()` signature param, and the `resolve_config(...)` kwarg.

**Do NOT re-add `--depth`** — it already exists fully wired (`commands.py:101-106` → `config.py:190` floor → `models.py:71`), `Choice(["standard","deep"])`, default `standard`, `quick`→`standard` floor. [09 §1a, D7]

**`expected_tier` is derived, not a config field** — at **`runner.py:403`**: `expected_tier = 2 if config.depth in {"standard","deep"} else 1` (both depths collapse to tier 2). If `deep` must map to a different expected tier, `runner.py:403` is the single mutation point; the `derive_verdict(expected_tier=...)` plumbing needs no change. [09 §1b, D7]

**`--reviewers` clamp/sentinel ordering (design obligation):** the `1`→negative-witness sentinel MUST be branched **before** any `max(2, min(4, n))` clamp, or the clamp rewrites `1`→`2` and erases negative-witness mode. Clamp lives in `resolve_config` (house convention: all resolution in `config.py`), not a Click callback.

### 19.3 Net-New Lens Module + Recipe Binding (D4 migration mechanics)

- **Net-new LENS module required:** add `src/superclaude/cli/swarm/lenses/reflect_review.py` exporting `LENS: LensEntry`, mirroring `lenses/bare_review.py`. Register it in `lenses/__init__.py` (import block, `LENSES` dict, `LENS_NAMES` tuple). This is **additive** — a new lens file, not a modification of `bare_review.py`. [09 Gaps; D4]
- **Recipe binding reuses `bare-review-v1` (zero recipe edits):** set the lens's `recipe_name="bare-review-v1"` and `normalizer_strategy="bare-review-v1"`. Both keys already exist in `recipes/__init__.py` `REGISTRY` (L182) and `STRATEGIES` (L209), so lens-validator **assertions 2 & 6 pass with zero recipe-package edits** (Path A, D4). A net-new `reflect-review-v1` recipe (Path B) is required **only** if the reflect-review output shape differs from the bare-review findings-table-with-`suspect` shape — confirm prompt output shape before committing to Path A.
- The lens must emit `suspect: true`, `tier: "T2"`, `default_workers` ∈ `[2,4]`, a `recommended_next_command_template` containing `/sc:adversarial` with `{suspect_files}` substitution, and **must not hard-code a Claude model** (models come from the `T2Model0N` env pool, not `spec.workers.models`). [00-prd-extraction FR-RH2.2]

### 19.4 Feature-Gating & Rollout

| Flag | Description | Default | Rollout Plan | Cleanup Date | Owner |
|---|---|---|---|---|---|
| `--transport {openai_compat\|stub}` | Gates the Tier-2 worker transport. `openai_compat` = live proxy ensemble; `stub` = deterministic, network-free, credit-free CI lane | **`openai_compat`** (live) | Live proxy is the GA default; CI runs the stub lane. Unknown enum value rejected at Click parse (no partial run) | Permanent flag (not a temporary gate — it is the transport selector) | Reflect/swarm maintainers |
| `--reviewers <N>` | Tier-2 reviewer slots, clamped `[2,4]`, default 3; `1` = negative-witness degrade | **3** | n/a — operational knob, not a rollout gate | Permanent | — |

**Progressive delivery posture:** there is no percentage-traffic canary — this is a CLI tool, not a fleet service. The "canary" is the **stub lane proving ensemble formation in CI before the live path is trusted** (FR-RH2.5): the credit-free `--transport stub` test exercises the real dispatch→reduce→derive path offline, so the live `openai_compat` path is only ever exercised against a mechanism already proven by the stub witness pair.

### 19.5 Rollback Procedure

The change is engineered for **cheap, surgical rollback** because the new components are additive/inert until the single rewire point activates them:

1. **Revert the `_audit_once` rewire** (`runner.py` — the `expected_tier==2` branch). This alone restores the prior single-`ClaudeProcess` launch for Tier-2.
2. **Revert the config plumbing** (the 3-file `transport`/`reviewers` edit). New fields become unreferenced.
3. **Leave `ensemble.py` + `lenses/reflect_review.py` in place or delete** — they are **additive and inert when not wired**; nothing else imports them once the `_audit_once` branch is reverted.
4. **No downstream touch required:** the `return-contract.yaml` shape is unchanged (FR-RH2.7), so `reflect_post:` write-back, the `wrapper-result.yaml` sidecar, `derive_verdict`, and the verdict→exit-code map are all untouched by rollback. Existing reflect contract/verdict tests stay green throughout.

**Rollback decision criteria:** live proxy fan-out producing systematic `blocked`/`degraded` verdicts traceable to the ensemble path (not genuine audit findings); the private-symbol coupling breaking on a swarm refactor; or the OI-1 contract translation proving incorrect in production.

### 19.6 NFR-7 Reconciliation (OI-2) — recorded as a migration concern

> This is the explicit NFR-7 amendment-or-confirm decision the migration must record. **OI-2 resolves to: CONFIRM-with-scope-extension, not a silent bypass.**

**The guarantee (Layer B of `test_no_nesting_guard.py`):** the reflect launch path must contain **no** `Task(` / `subagent` / `import anthropic` / `from anthropic` (no in-process Task/Agent fan-out), and **no raw `subprocess.run`/`Popen`** in the no-nest modules.

**Why HTTP workers are NOT the forbidden surface (guarantee preserved/strengthened):** Layer B forbids *in-process Task/subagent nesting* and *raw subprocess fan-out* inside the reflect package. The swarm-driven ensemble fans out via **`dispatch_wave1` → `ParallelExecutor` → `Transport` (HTTP/proxy or stub)** — **not** via `Task(`, `subagent_type`, or `subprocess.run`/`Popen`. Importing and composing the (all-sync) swarm functions adds zero `Task(`/`subprocess`/`async` to the reflect launch path. So the no-nesting guarantee is **preserved**; the ensemble is genuinely a different mechanism (in-process HTTP fan-out) than the one NFR-7 bans (Task/subagent nesting). The guarantee is arguably **strengthened**: the previously-broken path *relied on* in-process Task nesting inside the child `claude -p`; the new path removes that reliance entirely. [01 §c; 07 Part 2; 08 §4.4]

**Guard scope extension (the recorded amendment mechanics):**

- Add constant `_ENSEMBLE_SRC = _REFLECT_PKG / "ensemble.py"` next to `_RUNNER_SRC`.
- Define `_NO_NEST_SRCS = [_RUNNER_SRC, _ENSEMBLE_SRC]` and **loop the Layer-B agent-import test AND the raw-subprocess test over both modules** (the existing `_RAW_SUBPROCESS_CALL_RE` and `_IMPORT_SUBPROCESS_RE` regexes are reused — **no new regex**). [07 Part 2]
- The package-wide async/await + sprint/roadmap-import guards **already auto-cover `ensemble.py`** via the `_REFLECT_PY` `*.py` glob — no change needed (a free future-proofing win).
- **The raw-subprocess ban stays scoped to the two no-nest modules, NOT package-wide** — because `reflect/commands.py` keeps a legitimate `--tmux` `subprocess.run` in `_launch_tmux` (`reflect/commands.py:320`, the `subprocess.run(["tmux", "new-session", -d, …])` launch; the same function also runs `tmux attach-session`/`kill-session` at `reflect/commands.py:325,327`). Extending the ban package-wide would false-fail on that sanctioned tmux launch. So the ban is precisely `{runner.py, ensemble.py}`, no longer single-file but not package-wide.

**Recorded amendment text (for the guard docstring / spec §9):** "NFR-7 Layer B is extended to scan both `runner.py` and `ensemble.py` for `Task(`/`subagent`/`anthropic` imports and raw `subprocess.run`/`Popen`. The swarm-driven Tier-2 ensemble forms via in-process `dispatch_wave1`→`ParallelExecutor`→`Transport` (HTTP/stub), which is NOT the in-process Task/subagent nesting NFR-7 forbids; the no-nesting guarantee is preserved. The raw-subprocess ban is scoped to these two no-nest modules only; `reflect/commands.py` retains its sanctioned `--tmux` `subprocess.run` in `_launch_tmux` (`reflect/commands.py:320`)."

**The stub-integration test must inject `StubTransport`, not monkeypatch `subprocess`** — because the guard forbids raw subprocess in `ensemble.py`, the FR-RH2.5 proof exercises the real dispatch under an injected stub transport, never a subprocess monkeypatch (which would also re-create the mock gap that hid the original defect). [07 Part 4]

---

## Cross-Section Notes (provenance)

- §16 N/A rationale: component type is Library/Backend (01, 09); no client surface anywhere in `cli/reflect/` or `cli/swarm/`.
- §17 budgets: 03-swarm-dispatch (§1 fan-out, §2 timeout/retry matrix, §4 ParallelExecutor, §5 M-vs-N); runner loop multiplier from 01 (`runner.py` L536-537, L575-576) + D3 default `max_fix_iterations=2`; stub free re-audit from 07 Part 4-5.
- §18 dependencies: in-process swarm imports + private-symbol coupling (01 reuse-audit, 03 signatures); proxy contract (00 NFR-RH2.8, 01 §d caveat 3); Mode A + `--suspect-source` gap (08 §4.2/OI-4); recipe binding (09 §3, D4).
- §19 migration: 3-file edit (09 §1/D7), net-new lens (09 Gaps/D4), NFR-7 reconciliation/OI-2 (07 Part 2, 01 §c, 08 §4.4), contract-shape preservation (00 FR-RH2.7).

**Status: Complete**
