# synth-01 — Executive Summary, Problem Statement, Goals, Success Metrics

> **TDD sections 1–4** for **FR-RH2 — Headless Ensemble Fix** (drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library).
> **Parent spec:** `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (feature_id `FR-RH2`, target release 4.4.0, complexity HIGH 0.82).
> **Provenance:** every fact below traces to a research file under `.dev/tasks/to-do/TASK-TDD-20260619-235400/research/` (cited inline). `[CODE-VERIFIED]` findings are asserted as current architecture; `[UNVERIFIED]`/`[CODE-CONTRADICTED]` items are deferred to §22 Open Questions (handled by another synth file) and are NOT asserted here as fact.

---

## 1. Executive Summary

`superclaude reflect run` is the headless wrapper for the post-execution reflection gate (`/sc:reflect --mode post`). At `--depth standard|deep` it is contracted to deliver a **Tier-2 reviewer ensemble** — 2–3 heterogeneous reviewers on distinct model classes, merged adversarially — whose convergence is the evidence that the audit is trustworthy. Today it cannot. The wrapper launches **one** `claude --print` subprocess (`_audit_once`, `runner.py:392-428`) and relies on *that single child's own in-process Task fan-out* to spawn the reviewers (research/01 §a). Subagent→agent nesting is forbidden, so the inner fan-out never forms: the run degrades to `single-reviewer-fallback` / `tier_reached:1` with zero adversarial reviewers. NFR-7 forbids the only in-process alternative (`Task(`/`subagent_type` inside the reflect package), which makes the failure **architecturally guaranteed, not incidental** (research/00 §7). The defect was invisible to CI because the test harness mock (`conftest.py:98-138`) makes a stubbed `ClaudeProcess.wait()` copy a hand-authored `pass.yaml` — whose line 4 literally reads `tier_reached: 2` — into `return-contract.yaml`; "Tier 2 works" was a fixture constant validated against itself, never a computed result (research/07 Part 3).

This TDD re-routes the Tier-2 ensemble through the **swarm dispatch library**, reused in-process (`dispatch_wave1` at `swarm/dispatch.py:334`, the per-slot transport factory at `swarm/commands.py:612`, `reduce_wave3` at `swarm/reduce.py:555` — all plain synchronous `def`s that route through `ParallelExecutor` + `Transport`, never `Task(`/`subprocess`; research/01 reuse-audit). A new `cli/reflect/ensemble.py` driver imports and composes these to fan out N external OpenAI-compatible proxy workers (`T2Model0N`), which sidestep the nesting defect and provide genuine model-class diversity. A new `reflect-review` swarm lens (mirroring `lenses/bare_review.py`) supplies per-reviewer reflection briefs with `tier:"T2"`, `suspect:true`, and a `recommended_next_command_template` that hands the normalized artifacts to `/sc:adversarial`. Swarm normalizes and mechanically concatenates the per-reviewer artifacts; reflect's existing `sc-adversarial-protocol` Mode A scores them (swarm's `merge.py` stays a mechanical concat and is never treated as the adversarial verdict). The seam is narrow: `_audit_once` branches on the already-computed `expected_tier` (`runner.py:403`) — route `expected_tier==2` into `ensemble.py`, leave the L420-427 parse+derive tail and the Tier-1 single-`ClaudeProcess` path untouched (research/01 §c).

The key deliverables are: (1) `cli/reflect/ensemble.py` — the in-process driver that fans out reviewers via swarm and translates the swarm `ResultContract` into the reflect `return-contract.yaml` shape at `config.contract_path`; (2) the `reflect-review` swarm lens + per-reviewer output template; (3) a **non-mocked** `--transport stub` integration test that drives the **real** `dispatch_wave1`→`reduce_wave3`→`derive_verdict` path over a deterministic, network-free `StubTransport` and asserts the FR-RH2.4 ensemble signals — plus a **one-reviewer negative witness** proving the proof is falsifiable. What deliberately stays the same: the 4-state verdict map and exit codes (`pass→0, halted→10, degraded→11, blocked→2`), the `return-contract.yaml` shape and the `reflect_post:`/`wrapper-result.yaml` write-back, Tier-1's grounded single-agent pass, and swarm's merge boundary (research/00 §1, research/02 §1).

**Key Deliverables:**

- **`cli/reflect/ensemble.py`** — in-process Tier-2 driver: imports/composes swarm `dispatch_wave1` + per-slot transport factory + `reduce_wave3`, fans out N `T2Model0N` proxy workers (or `StubTransport`), and translates the swarm reduction into the reflect contract shape landed at `config.contract_path` (FR-RH2.1, FR-RH2.3).
- **`reflect-review` swarm lens + per-reviewer output template** — registered in the bundled swarm-lens registry, passing the same validator as `bare-review`; emits `suspect:true` + a `/sc:adversarial` `recommended_next_command_template`; `default_workers ∈ [2,4]`; no hard-coded Claude model (FR-RH2.2).
- **`tests/cli/reflect/test_ensemble_stub_integration.py`** — non-mocked `--transport stub` positive witness (≥2 reviewers → real fan-out→reduce→derive) + one-reviewer negative witness; runs offline, asserts the FR-RH2.4 signals are *computed*, not fixture constants (FR-RH2.5, FR-RH2.6).
- **NFR-7 guard extension** — `test_no_nesting_guard.py` extended so its Layer-B agent-import + raw-subprocess bans cover `ensemble.py` as well as `runner.py` (FR-RH2.8).

---

## 2. Problem Statement & Context

### 2.1 Background

The reflect Tier-2 protocol exists specifically to neutralize the representational bias of single-agent self-review: instead of one agent grading its own work, Tier 2 fans out 2–3 heterogeneous reviewers on **different model classes**, then merges them through `sc-adversarial-protocol` Mode A; the convergence of independent reviewers is what makes the audit trustworthy (research/00 §7). The `superclaude reflect run` CLI is the **headless wrapper** that drives this gate non-interactively. At `--depth standard|deep` it computes `expected_tier = 2` (`runner.py:403`) and is contracted to surface, in `return-contract.yaml`, evidence that a real ensemble formed (research/01 §a).

In the shipped architecture there is **no ensemble driver**. `cli/reflect/ensemble.py` does not exist; the reflect package is exactly `commands.py, config.py, contract.py, __init__.py, models.py, runner.py` (research/01 §c, research/07 inventory). Tier 2 is launched as **one** headless `claude --print` subprocess running `/sc:reflect --mode post` (`_audit_once`, `runner.py:392-428`; prompt built by `_build_prompt`, `runner.py:341-366`). The wrapper sees only that single child and the one `return-contract.yaml` it pins; the fan-out of the 2–3 reviewers is delegated to *that child's own in-process Task tool*. The `reflect_group` docstring (`commands.py:49-61`) states this design literally — it launches the slash command "as a top-level `claude --print` subprocess (**so Tier 2 fans out**)" — i.e. fan-out is the child's job, not the wrapper's (research/01 §a).

### 2.2 Problem Statement

**The core problem:** the headless Tier-2 ensemble is architecturally unreachable — the single `claude -p` child cannot nest a second level of Task fan-out (subagent→agent nesting is forbidden), so the run degrades to a single reviewer, and NFR-7 forbids the only in-process alternative, making the failure guaranteed rather than incidental (research/00 §7, research/01 §a).

Expanded with specifics:

- **What is broken:** the only Tier-2 launch surface (`_audit_once`) builds *one* `ClaudeProcess` with `--tools default` and trusts the `/sc:reflect` skill protocol inside it to fan out reviewers. That inner fan-out is a subagent→agent nesting, which does not form. The result degrades to `merge_method: single-reviewer-fallback` and/or `tier_reached: 1` with zero adversarial reviewers (research/00 §7; the `single-reviewer-fallback` path routes `degraded`/exit 11 via `_degraded_reason` trigger 10, research/02 §3).
- **Why it cannot simply be fixed in place:** the reflect package's isolation guardrails (`runner.py:8-12`) forbid `async`/`await` and any Agent/Task surface — the ONLY launch path may be `ClaudeProcess`/subprocess (NFR-7). So the wrapper cannot itself spawn per-model reviewers via `Task(`/`subagent_type`; the in-process alternative is closed by design (research/01 §a, research/07 Part 1).
- **Why CI never caught it (the mock gap):** `tests/cli/reflect/conftest.py:98-138` (`make_claude_process_stub`) makes the stubbed `ClaudeProcess.wait()` copy a hand-authored fixture into `return-contract.yaml`. `tests/cli/reflect/fixtures/pass.yaml:4` literally hard-codes `tier_reached: 2` (with `t2_model_class_diversity: full`, `merge_method: adversarial`, `adversarial_convergence_score: 0.86`). No real subprocess runs, no reviewer is dispatched, no merge happens — every "Tier 2 succeeded" field is a typed fixture constant the existing e2e suite validates against itself (research/07 Part 3).
- **Who/what is affected:** every headless reflection gate (sprint/task post-execution audits invoking `superclaude reflect run --depth deep`). A degraded audit that should fail loud can instead read as a less-trustworthy degrade, undermining the anti-bias guarantee the Tier-2 ensemble was built to provide.
- **Cost of not solving:** the post-execution trust gate runs without real adversarial cross-checking; the protective property of heterogeneous reviewers + adversarial convergence is silently absent in headless mode.

**Evidence Table**

| Evidence | Source (file:line) | Impact |
|----------|--------------------|--------|
| No ensemble driver exists; reflect pkg is 6 files, `ensemble.py` absent | research/01 §c; research/07 inventory (`ls` of `src/superclaude/cli/reflect/`) | Tier-2 fan-out has no in-process owner — it is delegated to the single child |
| Tier 2 = one `claude --print` child; fan-out delegated to that child's Task tool | `runner.py:392-428` (`_audit_once`); `commands.py:49-61` docstring ("so Tier 2 fans out") — research/01 §a | Subagent→agent nesting never forms → degrade to single reviewer |
| Isolation guardrails forbid the in-process alternative (NFR-7) | `runner.py:8-12`; `test_no_nesting_guard.py` Layer B (research/07 Part 1) | Cannot fix by adding `Task(`/`subagent_type` in-runner → failure is architecturally guaranteed |
| Mock copies a canned fixture into `return-contract.yaml` | `conftest.py:98-138` (`make_claude_process_stub`); research/07 Part 3 | No real dispatch/reduce ever runs in CI |
| `pass.yaml` hard-codes the Tier-2 success fields | `tests/cli/reflect/fixtures/pass.yaml:4` (`tier_reached: 2`), L12/L15/L16 — research/07 Part 3 | "Tier 2 works" is a fixture constant validated against itself, hiding the defect |
| `single-reviewer-fallback` already routes degraded/exit 11 | `contract.py:280-281` (`_degraded_reason` trigger 10) — research/02 §3 | The degrade path the broken run lands on is real verdict logic, not noise |

### 2.3 Business / Engineering Context

This work hardens the SuperClaude reflection-gate reliability surface; it has no external product PRD — the driving requirement document is the FR-RH2 release spec (`.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`).

- **Driving spec reference:** FR-RH2 (`spec.md`), target release **4.4.0**, complexity **HIGH (0.82)** — FRs FR-RH2.1…FR-RH2.9 + NFRs NFR-RH2.1…NFR-RH2.8 (research/00 §2, §3).
- **Engineering impact:** restores a faithful, model-diverse adversarial Tier-2 audit in headless mode by **adapting an existing shared seam** (swarm dispatch) rather than building a new fan-out engine — the reuse-by-import verdict is grounded in the three swarm symbols all being importable synchronous `def`s that route through `ParallelExecutor`+`Transport` (research/01 reuse-audit).
- **User impact:** consumers of `superclaude reflect run` (sprint/task pipelines, the task-builder terminal gate) get a Tier-2 verdict backed by a real ≥2-reviewer adversarial merge, and a credit-free CI lane (`--transport stub`) that proves the ensemble forms without burning proxy credits (research/00 §4, NFR-RH2.4).

---

## 3. Goals & Non-Goals

### 3.1 Goals

What this component WILL accomplish (derived from spec §1.2 in-scope + FR-RH2.1–.9; research/00 §1, §2):

| ID | Goal | Success Criteria |
|----|------|------------------|
| G1 | Form the Tier-2 ensemble via the swarm dispatch library, not in-process Task fan-out | `_audit_once` (`expected_tier==2`) drives `dispatch_wave1` + per-slot transport factory; **no** `Task(`/`subagent_type` in `runner.py` or the new `ensemble.py`; each `--depth standard\|deep` worker slot binds a distinct external `T2Model0N` (FR-RH2.1) |
| G2 | Add a `reflect-review` swarm lens with per-reviewer reflection briefs | Lens registered and passes the same swarm lens validator as `bare-review`; emits `suspect:true` + a `recommended_next_command_template` containing `/sc:adversarial` with `{suspect_files}`; `default_workers ∈ [2,4]`; no hard-coded Claude model (FR-RH2.2) |
| G3 | Score the normalized per-reviewer artifacts via `sc-adversarial-protocol` Mode A, not swarm merge | Downstream merge consumes swarm per-reviewer `final_path` artifacts; no scoring/ranking/dedup added to `swarm/merge.py`; the adversarial merge records a convergence score on the reflect contract (FR-RH2.3) |
| G4 | Make a faithful Tier-2 run yield a real adversarial merge with ≥2 distinct model classes | On a successful run: `tier_reached==2`, `merge_method != "single-reviewer-fallback"`, `reviewer_count == M ≥ 2` (M = `WorkerResult`s with `status=="success"`), `t2_model_class_diversity == "full"` computed over the **distinct `model_id`s of the M survivors** (FR-RH2.4, FR-RH2.9) |
| G5 | Define the N→M divergence (partial-failure) acceptance boundary explicitly | A reader can derive the verdict for any (M,N): M≥2 ∧ ≥2 distinct classes → pass-eligible; M≥2 but <2 classes → `degraded-model-diversity`; M==1 → `single-reviewer-fallback`/tier 1; M==0 → `blocked` (ordered ahead of degraded) (FR-RH2.9, research/00 §5) |
| G6 | Prove ensemble formation in CI credit-free, with a falsifiable witness | `--transport stub` test drives the **real** wrapper (unmocked `dispatch_wave1`/`reduce_wave3`), performs zero network I/O, does NOT patch `ClaudeProcess` to copy a canned `tier_reached:2` fixture, and asserts the FR-RH2.4 signals; a **1-reviewer** run degrades and the positive assertions FAIL on it (FR-RH2.5, FR-RH2.6) |
| G7 | Preserve downstream return-contract consumers | `return-contract.yaml` shape, `reflect_post:` write-back, and `wrapper-result.yaml` sidecar keep field names/semantics; existing reflect contract/verdict/runner tests pass unmodified (FR-RH2.7, NFR-RH2.6) |
| G8 | Preserve (or deliberately amend on the record) the NFR-7 no-nesting guarantee | `test_no_nesting_guard.py` Layer-B passes for the new driver (extended to `ensemble.py`); no raw `subprocess.run`/`Popen` added to the reflect package; any NFR-7 prose amendment is recorded in the spec + guard docstring (FR-RH2.8) |

### 3.2 Non-Goals

What this component will NOT do (spec §1.2 out-of-scope; research/00 §1):

| ID | Non-Goal | Rationale |
|----|----------|-----------|
| NG1 | Change the 4-state verdict map or exit codes | `pass→0, halted→10, degraded→11, blocked→2` in `contract.py`/`models.py` are the safety contract; shape-preservation (FR-RH2.7) depends on them staying byte-identical (research/02 §1) |
| NG2 | Rewrite the Tier-1 single-agent grounded pass | Tier-1 (`/sc:reflect` via `ClaudeProcess`) is unchanged; the fix is scoped to the `expected_tier==2` branch only (FR-RH2.1 AC) |
| NG3 | Change swarm's merge boundary | `swarm/merge.py` stays a mechanical concat, never an adversarial scorer; no scoring/ranking/dedup is added (its LOC ceiling + boundary tests stay green) (FR-RH2.3) |
| NG4 | Build a new parallel fan-out engine | Swarm already provides one; this spec **adapts the shared seam** (reuse-by-import of `dispatch_wave1`/factory/`reduce_wave3`), it does not rebuild (research/01 reuse-audit) |
| NG5 | Touch the UC-1 pre-execution path or roadmap's `validate_executor.py` | The change is confined to the UC-2 post-execution Tier-2 launch seam; UC-1 is explicitly out of scope (research/00 §1) |
| NG6 | Change the auto-fix loop (FR-1/FR-3) beyond the audit-launch seam it calls | The bounded fix loop in `run()` consumes the returned `ReflectResult` verdict/`remediation_task_path` unchanged; routing T2 inside `_audit_once` leaves the loop launch-agnostic (research/01 §c) |

### 3.3 Future Considerations

Items flagged by research but deferred (open items / coupling decisions; research/00 §6, research/01 caveats):

| Item | Target Phase | Notes |
|------|--------------|-------|
| Promote a public swarm transport-factory API | Post-FR-RH2 | Both `_resolve_run_transport` (`commands.py:510`) and `_resolve_run_transport_factory` (`commands.py:612`) are private; reuse-by-import imports a private cross-package symbol (coupling smell) — `[CODE-CONTRADICTED]` that a public equivalent exists (research/01 caveat #1, Gaps) → §22 |
| Reconcile `count_model_aliases`/`env_alias_count` with the proxy `T2Model0N` pool | During FR-RH2.1 | Today reflect diversity = 3 `ANTHROPIC_DEFAULT_*` Claude aliases; swarm fan-out diversity = `T2Model0N` proxy pool — the driver must populate the contract diversity fields honestly from whichever pool it used (research/01 §d caveat #3) |
| `--transport stub` auto-select in CI vs always opt-in (OI-3) | Before FR-RH2.5 lands | CI ergonomics decision (research/00 §6) |

---

## 4. Success Metrics

### 4.1 Technical Metrics

How we will measure success (FR-RH2.4/.5/.6/.9 acceptance signals + (M,N) guard table; research/00 §2, §5; research/07 Parts 4–5). M = succeeded workers (`WorkerResult.status=="success"`); N = requested reviewer slots.

| Metric | Current State | Target | Measurement Method |
|--------|---------------|--------|--------------------|
| Tier reached on a faithful `--depth standard\|deep` run | `tier_reached: 1` (single-reviewer degrade; the inner Task fan-out never forms) | `tier_reached == 2` | `derive_verdict` over the `return-contract.yaml` produced by the **real** `reduce_wave3` (FR-RH2.4 AC) |
| Merge method | `single-reviewer-fallback` (degraded/exit 11) | `merge_method != "single-reviewer-fallback"` (e.g. `adversarial`) | `_degraded_reason` trigger 10 keys on this exact field (`contract.py:280-281`); asserted in the stub integration test (research/02 §3, research/07 Part 4) |
| Reviewer count | effectively 1 (degraded) | `reviewer_count == M ≥ 2` (count of `success` `WorkerResult`s; `proxy_error`/`timeout`/`parse_error` do NOT count) | Distinct succeeded-worker count in the swarm `WorkerResult`s; "results == workers" witness mirroring `tests/swarm/test_commands_run.py:507-568` (research/00 §5.1, research/07 Part 5) |
| Model-class diversity | absent / fixture-only `full` | `t2_model_class_diversity == "full"`, computed over the **distinct `model_id`s of the M survivors** (≥ expected distinct-class count) — two survivors on the same class do NOT count as full | Assert distinct `model_id` count in the `WorkerResult`s (NFR-RH2.5); degraded routing via `_degraded_reason` trigger 7 when set and `!= "full"` (FR-RH2.4 AC, research/02 §3) |
| Ensemble-proof faithfulness (mock gap closed) | "Tier 2" is a `pass.yaml:4` `tier_reached:2` fixture constant copied by `conftest.py:98-138` | The proof runs the real `dispatch_wave1`→`reduce_wave3`→`derive_verdict` path; signals are **computed**, not pre-written; the test does NOT patch `ClaudeProcess` to copy a canned contract | `test_ensemble_stub_integration.py` exercises real fan-out under `StubTransport`, zero network I/O (FR-RH2.5 AC, NFR-RH2.3/.4, research/07 Parts 3–4) |
| Negative-witness falsifiability | no falsifying witness (defect hidden) | A **1-reviewer** stub run yields `merge_method == "single-reviewer-fallback"` and/or `tier_reached == 1`, and the FR-RH2.5 positive assertions FAIL on it | Same harness, single reviewer → `Verdict.DEGRADED`/exit 11; grounded in real verdict logic, not a fixture (FR-RH2.6 AC, research/07 Part 4) |
| Backward compatibility | existing reflect contract/verdict/runner/writeback suites green | All still green unchanged; verdict map + exit codes unchanged | `uv run pytest tests/cli/reflect -q` (NFR-RH2.6); regression floor = `test_verdict_mapping.py`, `test_runner_e2e.py`, `test_writeback.py` (research/07 Gaps) |

**(M,N) divergence → verdict mapping** (spec §5.3, reproduced verbatim; research/00 §5) — the metric thresholds above resolve to:

| M-condition | verdict | exit-code | reason-slug |
|-------------|---------|-----------|-------------|
| `M==0` (all workers failed / no artifacts) | `blocked` | `2` | `ensemble-empty` |
| `M==1` (≥N−1 failed, or `--reviewers 1`) | `degraded` | `11` | `single-reviewer-fallback` |
| `M≥2` but <2 distinct model classes | `degraded` | `11` | `degraded-model-diversity` |
| `M≥2` AND ≥2 distinct classes | `pass-eligible` | `0` | `pass` |

### 4.2 Business Metrics

Not applicable — this is an internal engineering reliability fix with no external product KPI. The "business" value is the restored anti-bias guarantee of the headless Tier-2 audit (real heterogeneous reviewers + adversarial convergence), measured entirely by the technical metrics in §4.1.

---

> **Provenance note:** Every fact in this synthesis traces to a research file under `.dev/tasks/to-do/TASK-TDD-20260619-235400/research/` (`00-prd-extraction.md`, `01-reflect-runner-seam.md`, `02-reflect-contract-verdict.md`, `07-nfr7-guard-test-harness.md`) and the parent spec `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`. Per the staleness rule, only `[CODE-VERIFIED]` findings are asserted here as current architecture; `[UNVERIFIED]`/`[CODE-CONTRADICTED]` items (swarm `ResultContract` exact schema, the public-transport-factory contradiction, diversity-pool reconciliation) are flagged for §22 Open Questions and are NOT asserted as fact. No facts were invented.
