# Synthesis 09 — §20–28: Risks, Alternatives, Open Questions, Timeline, Release, Ops, Cost, References, Glossary

- **Feature**: FR-RH2 — Headless Tier-2 Ensemble Fix (drive sc:reflect Tier-2 reviewer ensemble through the swarm dispatch library)
- **Target release**: 4.4.0 | **Complexity**: HIGH (0.82)
- **Template anchor**: `src/superclaude/examples/tdd_template.md` §20–28
- **Source spec**: `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` (feature_id FR-RH2)
- **Status**: Complete
- **Date**: 2026-06-20

> Every row below is derived from the research notes (00, 02, 05, 08, web-01) and the spec. No fabrication. `[CODE-VERIFIED]`/`[UNVERIFIED]`/`[CODE-CONTRADICTED]` tags are carried forward from research provenance. The two research-gate binding directives **D3** (`ensemble-empty` slug absent from `contract.py`) and **D5** (`--suspect-source` emitted but unparsed by Mode A) are surfaced as Open Questions in §22.

---

## 20. Risks & Mitigations

| ID | Risk | Probability | Impact | Mitigation | Contingency |
|----|------|-------------|--------|------------|-------------|
| R1 | External proxy models (`T2Model0N`) produce lower-quality reflection reviews than Claude reviewers would | M | M | `suspect: true` framing on every reflect-review artifact routes all reviews through `/sc:adversarial` Mode A scoring — never trusted raw (lens mirrors `bare_review.py` L63–64); require **≥2 distinct model classes** so single-model blind spots are hedged (FR-RH2.4 / `t2_model_class_diversity` over distinct succeeded `model_id`s) | Live-proxy E2E (§8.3) covers review *content*; if a model class is consistently weak, drop its slug from the `T2Model0N` pool and re-run |
| R2 | `merge_method` / `reviewer_count` / `t2_model_class_diversity` are **not** emitted by the swarm DM-012 contract in reflect's expected shape (the OI-1 schema-disjointness finding) | M | **H** | `ensemble.py` mapping layer synthesizes reflect verdict vocabulary from swarm raw facts (`workers_succeeded`, `amalgamation_mode`, `merged_path`, distinct `output_files[].model_id`) — the two `return-contract.yaml` schemas share only the key name `status`, with different semantics (synth-05 §6–7); the OI-1 field-correspondence table (synth-04) sizes this layer; FR-RH2.7 + existing contract tests pin the shape | If a field cannot be derived from swarm facts, route the audit to `blocked` (fail-loud) rather than emit a guessed value; OI-1 is BLOCKING (§22 Q1) |
| R3 | NFR-7 guard-scope ambiguity — does `test_no_nesting_guard.py` Layer B forbid the swarm-driven HTTP-worker path? | M | **H** | FR-RH2.8: Layer B forbids `Task(`/`subagent`/`anthropic` imports, **not** HTTP workers; confirm the guard's intent already covers the new path, else amend the guard prose **deliberately** and record in spec §9 with rationale (OI-2, §22 Q2) | If scope must change, the amendment is a recorded, reviewed event in the guard docstring/assertions — never a silent bypass |
| R4 | `ModelPoolTooSmallError` raised when the `T2Model0N` pool < `--reviewers` slots | M | L | Default `--reviewers 3` against a ≥4-slot pool; preflight (`read_env`, `T2Model0N >= reviewers`) fires the guard **eagerly before dispatch** (`commands.py:589–609`); surface the guard's actionable message verbatim (add slots or reduce count) | Operator reduces `--reviewers` or adds proxy model slugs to `~/.aienv`; runbook §25.1 entry |
| R5 | Stub transport diverges from live proxy behavior, hiding a real defect (stub-vs-live divergence) | L | M | Stub proves **formation** (`tier_reached`/`merge_method`/`reviewer_count`/`diversity`), not review **content**; the stub test drives the **real** unmocked `dispatch_wave1`/`reduce_wave3` (FR-RH2.5 AC: must NOT patch `ClaudeProcess` to copy a canned `tier_reached:2` fixture); a live-proxy E2E (§8.3) covers content; the one-reviewer negative witness guards against vacuous pass (FR-RH2.6) | Live-proxy E2E catches transport-specific regressions; if stub and live diverge on formation signals, treat as a stub-fidelity bug and fix the stub |
| R6 | Adversarial scorer receives swarm `merged.md` (mechanical concat) instead of the per-reviewer `final_path` artifacts | L | **H** | FR-RH2.3 + §5.3 phase contract: Mode A consumes `output_files[].final_path` (filtered `status == "success"`, mirroring `commands.py` L2066–2070), **never** `merged.md`; no scoring/ranking/dedup may be added to `swarm/merge.py` (4 boundary guards: docstring + ≤30-LOC ceiling test + PR-touch check + 3-worker boundary test, synth-05 §2) | `merge.py` boundary tests fail loud if scoring leaks in; code review on the `ensemble.py` handoff confirms `final_path`-only input |
| R7 | Tier-2 latency increases (HTTP fan-out + adversarial pass on top of Tier-1) | M | L | Parallel fan-out via swarm `ParallelExecutor` (I/O-bound thread-pool, web-01 B1/B4); per-worker `timeout_sec` (NFR-010); `--detached`/tmux + `done.json` sentinel for long headless runs (NFR-RH2.7) | `--detached` observability path lets operators poll instead of blocking; raise `timeout_sec` for slow proxies |
| R8 | Auto-fix loop cost multiplier — each `--fix` re-audit re-runs the full ensemble | M | L | `--fix` calls the swarm-driven ensemble once per audit (idempotent re-verify, NFR-4): up to `(max_fix_iterations + 1) × reviewers` proxy calls; bounded by `max_fix_iterations` (default 2); `--transport stub` re-audits are free; cost surfaced so operators size proxy credits (§26) | Cap `max_fix_iterations`; use `--transport stub` in CI; operator monitors proxy spend |
| R9 | **NFR-7 scope ambiguity is also an acceptance-boundary ambiguity** — the spec leaves OI-2 (exact amendment text) open, so the guard could pass-by-accident if Layer B never anchored on `ensemble.py` | M | M | NFR-RH2.1 explicitly extends Layer B to `ensemble.py`; the extended `test_no_nesting_guard.py` must anchor regexes on the new module, not just `runner.py`; resolve OI-2 confirm-vs-amend during FR-RH2.8 | If the extension is forgotten, the new driver could harbor `Task(` undetected — make the `ensemble.py` anchor a required assertion, not optional |

> **Risk-source provenance:** R1, R2, R3, R4, R5, R6, R7, R8 transcribe the spec §7 risk table (`spec.md` L481–490). R9 is a synthesis-derived elaboration of the NFR-7 / OI-2 scope ambiguity flagged across PRD-extraction (FR-RH2.8) and synth-08, surfaced here because "NFR-7 scope ambiguity" is both a risk and an open question (cross-referenced to §22 Q2).

---

## 21. Alternatives Considered

> Reviewers should verify these alternatives were genuinely evaluated, not reverse-engineered to justify a predetermined choice. The reuse-audit (`reuse-audit.yaml`, max_overlap 0.81, verdict `reuse-by-import`) and the external grounding (web-01 A1/A2/A3) independently point at the chosen design.

### Alternative 0: Do Nothing *(mandatory)*

**Description:** Ship nothing. `superclaude reflect run --depth standard|deep` continues to spawn one `claude -p` subprocess that delegates `/sc:reflect` into a Task worker, which then **cannot nest a second level of Task fan-out** (subagent→agent nesting is forbidden under `claude -p`). The headless Tier-2 path stays broken.

**Pros:**

- No engineering cost.
- No operational burden (no proxy dependency, no `T2Model0N` pool to maintain).
- No risk of introducing regressions into the reflect verdict/exit-code contract.

**Cons:**

- Headless Tier-2 is **architecturally guaranteed to be broken**: the run degrades to `single-reviewer-fallback`, `tier_reached: 1`, **zero adversarial reviewers** (PRD-extraction L256). The ensemble — the entire reason Tier-2 exists — never forms.
- The defect is not incidental: **NFR-7 forbids the only in-process alternative** (in-runner `Task(`/`subagent_type`), so the failure cannot be fixed by tweaking the existing path. Doing nothing locks in a permanently degraded headless audit.
- Every `--depth deep` headless reflect silently produces a degraded/untrustworthy verdict instead of a real multi-model ensemble — the calibration-bias defense the ensemble was built for is unavailable exactly when it is most needed (unattended CI runs).

**Why Not Chosen:** "Do nothing" leaves a load-bearing capability (heterogeneous Tier-2 reviewer ensemble) non-functional in headless mode, and the defect is **architecturally guaranteed** rather than transient — there is no in-process path that both forms the ensemble and satisfies NFR-7. Not viable.

---

### Alternative 1: Rebuild per-reviewer fan-out inside `runner.py`

**Description:** Implement a new parallel fan-out engine directly in the reflect package (a `runner.py`-local thread pool / dispatcher) that binds each reviewer slot to a distinct external `T2Model0N` model over the OpenAI-compatible proxy, collects per-reviewer results, guards a too-small pool, and hands artifacts to Mode A — without importing swarm.

**Pros:**

- No cross-package coupling to swarm's public dispatch API; reflect owns its fan-out end-to-end.
- Freedom to shape the result objects exactly to reflect's verdict vocabulary (no mapping layer).

**Cons:**

- **Duplicates swarm's already-hardened seam.** The reuse-audit fingerprints `ensemble.py`'s capability ("in-process parallel heterogeneous reviewer fan-out with normalized-artifact adversarial handoff") at **max_overlap 0.81 / S_reuse 0.81 / verdict `reuse-by-import`** against `dispatch.py:344` (`ParallelExecutor` fan-out), `commands.py:619` (per-slot transport factory), and `reduce.py:578` (status + merge + `ResultContract` emission). Rebuilding re-implements: per-slot model binding, the `ModelPoolTooSmallError` too-small-pool guard, the `WorkerResult`/`ResultContract` surface, retry-once-then-drop, and the salvage path.
- Reproducing the retry/timeout/salvage matrix (swarm §7) correctly is non-trivial; a hand-rolled copy is a fresh bug surface.
- Violates the spec's explicit out-of-scope: "Building a new parallel fan-out engine (swarm already provides one — this spec **adapts the shared seam**, it does not rebuild)" (PRD-extraction L32).

**Why Not Chosen:** Reuse-by-import wins decisively (S_reuse 0.81). Rebuilding duplicates a hardened, tested seam and re-opens guard/retry/salvage bugs the swarm path has already closed — against the spec's stated intent.

---

### Alternative 2: Keep the in-process Task fan-out (status quo mechanism)

**Description:** Retain the current mechanism — the single `claude -p` reflect subprocess uses the Task tool to fan out reviewer sub-agents in-process — and attempt to make nesting work (e.g. by restructuring prompts or sub-agent definitions).

**Pros:**

- Zero new dependency surface; no proxy, no swarm import.
- Conceptually the simplest — it is the path already wired.

**Cons:**

- **This IS the broken root cause.** Subagent→agent nesting under `claude -p` fails — and fails *silently* (web-01 A1: the nested spawn "silently fail[s] / silently halt[s] at runtime," behaving as if the tool was never requested; A2: in-process team agents "lack the Agent tool (cannot spawn subagents)"; A4: an independent 16-agent run lists "Nested execution failed in practice"). No prompt restructuring fixes a primitive that is not exposed in the nested context.
- **NFR-7 forbids the alternative in-runner mechanism** (`Task(`/`subagent_type` in `runner.py`), so even if nesting could be coaxed to work it would violate the no-nesting guarantee the guard enforces.
- Produces exactly the degraded `single-reviewer-fallback`/`tier_reached:1` outcome that motivated the spec.

**Why Not Chosen:** It is the defect, not a fix. The failure mode is a documented, silent, primitive-level limitation; the field-tested remedy is a flat / in-process-library model with file-based handoffs (web-01 A1/A2/A4), which is precisely the chosen design.

---

### Integration sub-decision: in-process library import vs CLI-subprocess shell-out

> This is the decision that distinguishes the chosen design from the **proven prior art** in Precedent B. Both fan out one reviewer per distinct model and merge adversarially over the per-reviewer artifacts; they differ only in *how* each reviewer is invoked.

**Prior art (untouched, cited as the subprocess-per-agent option):** `roadmap/validate_executor.py` `_build_multi_agent_steps` (**L317–373/378**, `[CODE-VERIFIED]`, synth-08 §2) is shipped, tested separate-process-per-agent fan-out: one `Step` per `config.agents` entry, each binding a **distinct `model`** (heterogeneity from model binding, not prompt), returned as a parallel group `[reflect_steps, merge_step]`, with the adversarial-merge step fed the **list of per-agent reflection output files** (`reflect_outputs`) — the same "merge consumes per-reviewer artifacts, not a pre-merged blob" contract. **But each `Step` becomes its own `claude -p` subprocess**, which for reflect's *inner* Tier-2 loop re-introduces the exact `claude -p` nesting failure (synth-08 §2.2).

**Chosen — in-process library import (NFR-RH2.2):** `ensemble.py` imports `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3` and calls them **in-process** — no second `claude -p` subprocess for the inner loop. NFR-RH2.2 forbids `cli.sprint`/`cli.roadmap` imports, `async`/`await`, and any raw `subprocess.run`/`Popen` in the reflect package, anchored by `test_no_nesting_guard.py` import/async/subprocess regexes.

- **Pros:** sidesteps the nesting failure entirely (web-01 A1/A2); "import is generally vastly preferable to spawning a separate process… in the absence of factors which force the other choice" (web-01 A3); avoids the per-process startup + serialization/IPC tax a subprocess fan-out pays per reviewer (web-01 A5); reuses swarm's hardened `ParallelExecutor` (I/O-bound thread-pool, the idiomatic fit per web-01 B1/B4).
- **Cons:** couples reflect to swarm's public dispatch API stability (`[UNVERIFIED that the planned import shape compiles — depends on swarm dispatch public API stability]`, synth-08 §gaps); couples to a private symbol `_resolve_run_transport_factory` (leading underscore — §22 surfaces this as a coupling-to-private-API question).

**Retained for observability ONLY (NFR-RH2.7):** the `superclaude swarm run --lens reflect-review` CLI surface (`--detached`/tmux + `done.json` sentinel + `--tui`) is the optional pollability variant for long headless runs — **NOT** the default inner-loop transport (PRD-extraction L17). If it ever shells out, it goes through the swarm CLI surface / `ClaudeProcess` (sanctioned), never a hand-rolled `Popen` (FR-RH2.8 AC). **Net: library import is the transport; CLI `--detached`/tmux is the telescope** (synth-08 §4.4).

**Why subprocess-per-agent not chosen for the inner loop:** `validate_executor`'s model spawns `claude -p` children → re-introduces the nesting failure mode the whole spec exists to avoid (synth-08 §2.2), plus the startup+IPC tax (web-01 A5). It remains the §21 "subprocess-per-agent" alternative and is left **untouched** as proven prior art for the *roadmap* path, where the subprocess level is the outer loop and nesting does not arise.

---

## 22. Open Questions

| ID | Question | Owner | Target | Status | Resolution |
|----|----------|-------|--------|--------|------------|
| **Q1 (OI-1, BLOCKING GATE)** | Does the swarm DM-012 `ResultContract` already emit `reviewer_count` / `merge_method` / `t2_model_class_diversity` in the exact shape `contract.derive_verdict` reads, or must `ensemble.py` map them? Produce + validate the swarm-`ResultContract`-field → reflect-contract-field correspondence table. | Eng (TDD author / FR-RH2.3 implementer) | **BEFORE any FR-RH2.3 code lands** | 🟡 Investigating | **Research answer (synth-05 §6–7):** the two `return-contract.yaml` schemas are **disjoint** — they share only the key name `status`, with different semantics. `tier_reached`, `merge_method`, `t2_model_class_diversity`, `reviewer_count`, `adversarial_convergence_score`, `deviation_count_by_class` are **all absent** from swarm DM-012 and must be SYNTHESIZED by `ensemble.py` from raw swarm facts (`workers_succeeded`, `amalgamation_mode`, `merged_path`, distinct `output_files[].model_id`). synth-04 has produced the correspondence table; **it must still be validated against the shipped diff at implementation** before this gate closes. |
| Q2 (OI-2) | Exact NFR-7 amendment text (if any) — does Layer B's intent already cover HTTP workers, or does the guard prose need updating to recognize the swarm-driven path? | Eng (FR-RH2.8) | During FR-RH2.8 | 🔴 Open | Decide confirm-vs-amend; if amended, record in spec §9 and in the guard docstring/assertions with rationale. (Cross-ref R3/R9.) |
| Q3 (OI-3) | Should `--transport stub` be auto-selected in CI, or always opt-in? | Eng (FR-RH2.5) | Before FR-RH2.5 lands | 🟡 Investigating | **Recommendation: opt-in.** Auto-selecting stub in CI risks masking a live-transport regression and couples CI config to transport internals; an explicit `--transport stub` in the CI invocation keeps the credit-free lane intentional and visible (NFR-RH2.4). Low-impact (CI ergonomics). |
| Q4 (OI-4 / **D5**) | How does `/sc:adversarial` Mode A treat `suspect: true` reflect-review artifacts vs bare-review ones — any rubric difference? | Eng (FR-RH2.3) | During FR-RH2.3 | 🟡 Investigating | **Research answer (synth-08 §4.2, §5):** *no rubric difference today, because Mode A does not read `suspect` at all.* Both lenses set `suspect:true/tier:T2` identically; Mode A's hybrid-scoring rubric has **no `suspect`-conditional branch** (grep over all 3002 SKILL lines: zero `suspect` hits). The symmetry is real but **vacuous**. Recommend **option (a): keep the suspect flag advisory/caller-side** (lowest risk; preserves FR-RH2.3 AC "no scoring/ranking/dedup added to `merge.py`" and backward-compat). Option (b) — teach Mode A a suspect rubric — is an out-of-scope protocol change. |
| Q5 (**D5**, `[CODE-CONTRADICTED]`) | `--suspect-source` is emitted by the `bare-review` lens + bare-review SKILL (`bare_review.py` L65–68) but is **NOT documented or parsed anywhere in `sc-adversarial-protocol/SKILL.md`** (0 hits over 3002 lines; Mode A's input parser L551–610 lists `--compare`, `--source`, `--generate`, `--agents`, `--pipeline`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau` — never `--suspect-source`). Does reflect's handoff rely on a flag the consumer doesn't formally parse, or pass suspect files via `--compare` with suspect handling advisory? | Eng (FR-RH2.3) | During FR-RH2.3 | 🔴 Open | Decide: (i) pass suspect files via `--compare` and treat `--suspect-source` as advisory caller-side metadata (no Mode A change — recommended, consistent with Q4(a)), OR (ii) teach Mode A to parse `--suspect-source` (out-of-scope protocol change, must be applied symmetrically to both lens families). |
| Q6 (**D3**, `[CODE-VERIFIED]` absence) | The (M,N) guard table (spec §5.3) assigns `M==0 → blocked / exit 2 / reason-slug **`ensemble-empty`**`, but `grep ensemble-empty src/superclaude/cli/reflect/` returns **zero hits** — the slug does not exist in `contract.py` today; the existing M==0→BLOCKED path uses structural slugs (`contract-missing`, `child-crash`, `malformed-*`, synth-02 §2). Reconcile against FR-RH2.7 "verdict map unchanged." | Eng (FR-RH2.3 / FR-RH2.9) | During FR-RH2.9 wiring | 🔴 Open | Decide: (i) **Option B (preserves FR-RH2.7 literally)** — `ensemble.py` maps the empty-ensemble condition onto an **existing** BLOCKED trigger/slug (e.g. emit no usable contract → existing `contract-missing`/`malformed-*` Stage-1 guard fires) so the verdict→exit-code map (`blocked→2`) stays byte-identical **and `derive_verdict` itself is not touched** — FR-RH2.7's "`derive_verdict` … unchanged" (spec §FR-RH2.7, L303) holds exactly; the cost is a less-specific slug; OR (ii) **Option A (deliberate, recorded scope call)** — add `ensemble-empty` as a new M==0 BLOCKED branch in `derive_verdict`. **This modifies the verdict-derivation path** (a new branch inside `derive_verdict`), so although the exit-code map and 4-state vocabulary stay intact, it **must be called out as a deliberate amendment against FR-RH2.7's "`derive_verdict` unchanged" claim** — it is NOT a no-cost slug rename. This is the same FR-RH2.7 tension synth-06 §12 D3 Option A flags: only the exit-code map is mechanically pinned; a new `derive_verdict` branch is a recorded change, not a free one. Either way the verdict/exit-code is identical (`blocked`/exit 2); only slug fidelity and the FR-RH2.7 scope-impact differ. **Must be explicitly chosen and recorded so the spec's §5.3 table and the code agree, and so any `derive_verdict` change is an acknowledged FR-RH2.7 amendment, not a silent one.** |
| Q7 | `ensemble.py` imports **`_resolve_run_transport_factory`** (`commands.py:612/619`) — a **private** symbol (leading underscore). Reflect would couple to swarm's private API; the import shape compiling depends on swarm dispatch public-API stability (`[UNVERIFIED]`, synth-08 §gaps). Should this be promoted to a public swarm entrypoint, or is the private coupling accepted? | Eng (FR-RH2.1) | During FR-RH2.1 (driver) | 🔴 Open | Recommend promoting the per-slot transport-factory resolver to a documented public swarm function (or a thin public wrapper) so reflect does not depend on a private `_`-prefixed symbol that may change without notice. If accepted as-is, pin a swarm contract test that fails if the private signature drifts. |
| Q8 | `--reviewers` is documented as **clamped to `[2,4]`** (CLI surface) yet **rejected at Click parse** for unknown `--transport` values. Is `--reviewers 1` *clamped* up to 2, or accepted as the negative-witness value (`1` → degrade)? The spec says both "clamped to `[2,4]`" AND "`1` is the negative-witness case." | Eng (FR-RH2.6 / config plumbing) | During config.py plumbing | 🟡 Investigating | **Reconciliation:** `1` must be **accepted (not clamped to 2)** so the FR-RH2.6 negative witness can reach `single-reviewer-fallback`/`tier_reached:1`; values `>4` clamp down to 4 and `0`/negative reject or floor. The "clamp `[2,4]`" applies to the *normal operating range*; `1` is the deliberate sub-range negative-witness escape. Confirm the clamp predicate treats `1` as pass-through-to-degrade, not clamp-to-2 — otherwise FR-RH2.6 cannot be satisfied. |

> **Blocking note:** **Q1 (OI-1) is the load-bearing BLOCKING GATE** — it must be resolved (table produced AND validated against the shipped diff) before any FR-RH2.3 code lands. The `ensemble.py` mapping layer is *sized* by this table. synth-04 has produced the table from the disjoint-schema finding (synth-05 §7); the remaining gate action is validation against the implementation diff.
>
> **`[UNVERIFIED]` / `[CODE-CONTRADICTED]` items carried from research → all land here:** Q5/Q6 are `[CODE-CONTRADICTED]` (`--suspect-source` undocumented; `ensemble-empty` slug absent). Q7 carries the `[UNVERIFIED]` import-shape-compiles caveat. The producer-side reflect contract emission (`02-reflect-contract-verdict.md` §gaps), the `t2_model_class_diversity`/`t2_vendor_diversity` enum domains, and the `adversarial_convergence_score` numeric type are `[UNVERIFIED]` from the consumer side and must be cross-checked against the producer at implementation (folded into Q1's validation step).

---

## 23. Timeline & Milestones

> Ordering transcribes the spec §4.6 dependency-respecting implementation order (`spec.md` L375–387). This is a CLI-infrastructure change inside a single package; phases are work units, not calendar weeks. **Q1 (OI-1) must close before Milestone M3 (FR-RH2.3) begins.**

### 23.1 High-Level Milestones

| Milestone | Work unit | Status | Dependencies |
|-----------|-----------|--------|--------------|
| M0 | OI-1 field-correspondence table validated against shipped diff (Q1 BLOCKING) | ⬜ | synth-04 table (produced) |
| M1 | `reflect-review` lens + output template (swarm-side; no reflect dependency) | ⬜ | — |
| M2 | `ensemble.py` thin driver + `contract.py` diversity-source change *(parallel)* | ⬜ | M1 |
| M3 | `runner.py` `_audit_once` rewire to `ensemble.py` | ⬜ | M1, M2, **M0 (FR-RH2.3 gate)** |
| M4 | `config.py` `--transport`/`--reviewers` plumbing | ⬜ | M3 |
| M5 | Stub integration test (positive ≥2) + one-reviewer negative witness | ⬜ | M3, M4 |
| M6 | NFR-7 reconciliation (confirm scope or amend guard deliberately) | ⬜ | M3 |

### 23.2 Implementation Phases (from spec §4.6)

#### Phase 1 — Lens + template (step 1)

**Deliverables:**

- [ ] `reflect-review` `LensEntry` (mirrors `lenses/bare_review.py`): `suspect: true`, `tier: "T2"`, `recommended_next_command_template` containing `/sc:adversarial` + `{suspect_files}`, `default_workers ∈ [2,4]`, no hard-coded Claude model (FR-RH2.2).
- [ ] `reflect-review-output.md` normalized per-reviewer template (pinned frontmatter: `schema_version`, `tier`, `suspect`, `lens`).

**Exit Criteria:** `reflect-review` passes the swarm lens validator (same gate as `bare-review`); `test_reflect_review_lens_registered` green; no reflect-package change yet.

#### Phase 2 — `ensemble.py` driver + diversity source (steps 2, parallel)

**Deliverables:**

- [ ] `ensemble.py` imports `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3`; binds slot `i` → `T2Model0N`; collects succeeded `final_path`s; hands `--compare <existing>,<final_path…>` to Mode A; **never** passes `merged.md` (FR-RH2.1, FR-RH2.3).
- [ ] `contract.py` diversity-source change: `t2_model_class_diversity` derives from distinct succeeded swarm `model_id`s, not a Claude-alias count (FR-RH2.4).

**Exit Criteria:** `test_ensemble_binds_distinct_models` (distinct `model_id`s; `ModelPoolTooSmallError` when pool < reviewers); `test_diversity_from_proxy_modelids` green; **OI-1 table validated (M0/Q1 closed) before this phase's FR-RH2.3 portion merges.**

#### Phase 3 — Runner rewire (step 3)

**Deliverables:**

- [ ] `runner.py` `_audit_once` calls `ensemble.py` for the Tier-2 path; Tier-1 grounded pass (single `ClaudeProcess`) unchanged (FR-RH2.1 AC).

**Exit Criteria:** `tests/cli/reflect` green unchanged (NFR-RH2.6); no `Task(`/`subagent_type`/raw subprocess in `runner.py` or `ensemble.py`.

#### Phase 4 — Config plumbing (step 4)

**Deliverables:**

- [ ] `--transport {openai_compat|stub}` (default `openai_compat`; unknown value rejected at Click parse), `--reviewers <N>` (clamp `[2,4]`, default 3, `1` → negative-witness degrade per Q8), `--depth {standard|deep}` (quick floors to standard).

**Exit Criteria:** `test_transport_enum_rejects_unknown`; `--reviewers 1` reaches degrade (does not clamp to 2).

#### Phase 5 — Proof tests (step 5)

**Deliverables:**

- [ ] `test_ensemble_stub_integration.py` positive (≥2, real unmocked `dispatch_wave1`/`reduce_wave3`, zero network I/O) asserts `tier_reached==2`, `merge_method != single-reviewer-fallback`, `reviewer_count>=2`, `t2_model_class_diversity=="full"` (FR-RH2.5).
- [ ] One-reviewer negative witness: same assertions FAIL for `--reviewers 1` (FR-RH2.6).

**Exit Criteria:** Both witnesses run the real path; positive passes, negative fails the positive assertions (non-vacuous, NFR-RH2.3).

#### Phase 6 — NFR-7 reconciliation (step 6)

**Deliverables:**

- [ ] `test_no_nesting_guard.py` Layer B extended to anchor on `ensemble.py`; OI-2 confirm-vs-amend decided and recorded in spec §9 + guard docstring (FR-RH2.8, Q2).

**Exit Criteria:** Guard passes including the `ensemble.py` anchor; if amended, the amendment is on the record with rationale.

---

## 24. Release Criteria

### 24.1 Definition of Done

A feature is complete (4.4.0-ready) when:

- [ ] **FR-RH2.1** — Tier-2 audit invokes the swarm run surface (`dispatch_wave1` / `_resolve_run_transport_factory`); no `Task(`/`subagent_type` fan-out in `runner.py` or the new driver; each slot binds a distinct `T2Model0N`; Tier-1 grounded pass unchanged.
- [ ] **FR-RH2.2** — `reflect-review` lens registered + passes the lens validator; emits `suspect: true` + `recommended_next_command_template` with `/sc:adversarial` and `{suspect_files}`; `default_workers ∈ [2,4]`; no hard-coded Claude model.
- [ ] **FR-RH2.3** — downstream merge consumes succeeded `output_files[].final_path`; no scoring added to `swarm/merge.py` (LOC ceiling + boundary tests green); adversarial merge produces a convergence score recorded on the reflect contract. **(Gated on Q1/OI-1.)**
- [ ] **FR-RH2.4** — a successful Tier-2 run yields `tier_reached==2`, `merge_method != single-reviewer-fallback`, `reviewer_count == M >= 2`, `t2_model_class_diversity == "full"` computed over distinct succeeded `model_id`s.
- [ ] **FR-RH2.9** — (M,N) divergence boundaries hold: `M==0 → blocked/exit 2`; `M==1 → degraded` (`single-reviewer-fallback` and/or `tier_reached:1`); `M>=2 but <2 distinct classes → degraded-model-diversity`; `M>=2 ∧ >=2 classes → pass-eligible`. (Slug reconciliation Q6 closed.)
- [ ] **FR-RH2.5** — stub-transport test drives the real wrapper, zero network I/O, asserts the FR-RH2.4 signals; does NOT patch `ClaudeProcess` to copy a canned `tier_reached:2` fixture.
- [ ] **FR-RH2.6** — one-reviewer negative witness degrades; the positive-test assertions FAIL for it.
- [ ] **FR-RH2.7** — `derive_verdict` + verdict→exit-code map (`pass→0/halted→10/degraded→11/blocked→2`) unchanged; `write_reflect_post` field set/order + sidecar unchanged; existing reflect contract/verdict tests pass without modification.
- [ ] **FR-RH2.8** — `test_no_nesting_guard.py` passes (incl. `ensemble.py`); any NFR-7 amendment recorded in spec §9 + guard docstring; no raw `subprocess.run`/`Popen` in the reflect package.
- [ ] **NFR-RH2.1–.8** all met: no in-process Task fan-out; thinness/isolation (no `cli.sprint`/`cli.roadmap` import, no `async`/`await`); non-vacuous proof; credit-free CI (zero network I/O); model-class diversity assertion; backward compatibility (`uv run pytest tests/cli/reflect -q` green); observability (`--detached`/tmux/`done.json`/`--tui`); proxy contract (`:4000/cli` + `T2Model01..NN` per `~/.aienv`, no `:4000/v1`/`:8317` probing).
- [ ] OI-1 (Q1) resolved + table validated against shipped diff; OI-2/OI-3/OI-4 (Q2/Q3/Q4) closed; D3 (Q6) and D5 (Q5) reconciled on the record.
- [ ] `make verify-sync` green (lens/skill source-of-truth synced); `uv run ruff format --check src/ tests/` green.

### 24.2 Release Checklist

- [ ] All nine FRs + eight NFRs satisfied per DoD.
- [ ] No open BLOCKING question (Q1).
- [ ] Positive + negative stub witnesses green; live-proxy E2E (§8.3) run once against the real proxy.
- [ ] `swarm/merge.py` boundary tests + LOC ceiling green (no scoring leaked).
- [ ] Rollback = revert to the in-process path is a no-op behavioral change (it was already degraded); document in §19.

---

## 25. Operational Readiness *(light — CLI infrastructure)*

> This is a local CLI pipeline, not a hosted service. "Operational readiness" = the operator running `superclaude reflect run --depth deep` headlessly can diagnose a failed/degraded Tier-2 run without reading source.

### 25.1 Runbook

| Scenario | Symptoms | Diagnosis Steps | Resolution | Escalation |
|----------|----------|-----------------|------------|------------|
| **Pool too small** | `ModelPoolTooSmallError` raised before any reviewer dispatches; run exits non-zero at preflight | Check `~/.aienv` for `T2Model01..NN` count vs `--reviewers`; the guard message names the deficit (`commands.py:589–609`) | Add `T2Model0N` slugs to `~/.aienv` until pool ≥ `--reviewers`, OR lower `--reviewers` (min 2 for a real ensemble) | If `~/.aienv` is correct but the guard still fires, the proxy contract (`:4000/cli`) may be misread — verify `read_env` preflight |
| **All workers fail (M==0)** | Verdict `blocked`, exit `2`; reason slug (Q6: `ensemble-empty` or mapped BLOCKED slug); no usable per-reviewer artifacts | Read `<output_dir>/t2-swarm/return-contract.yaml` → `output_files[].status` (all `proxy_error`/`timeout`); check proxy reachability | This is fail-loud by design (M==0 → blocked, never silent degrade). Fix proxy/network, re-run | If proxy is healthy but every worker `proxy_error`s, escalate as a transport/auth defect — do NOT probe `:4000/v1` or `:8317` |
| **Proxy unreachable** | Workers `proxy_error` after retry-once; M drops; verdict degrades (`degraded-model-diversity`/`single-reviewer-fallback`) or `blocked` if M==0 | Confirm `:4000/cli` base + `T2ProxyUrl`/`T2ProxyKey` in `~/.aienv`; check the proxy is up | Restore proxy; re-run. For CI, use `--transport stub` (network-free) to keep proving *formation* while the live proxy is down | Page proxy owner; meanwhile CI stays green on `--transport stub` |
| **Degraded to single-reviewer (M==1)** | `merge_method: single-reviewer-fallback`, `tier_reached:1`, exit `11` | Distinguish intended (`--reviewers 1` negative witness) from N>1 with N−1 failures: read `workers_requested` vs `workers_succeeded` in the swarm subrun contract | If unintended: investigate which workers failed (proxy/timeout) and re-run; if `--reviewers 1`: expected (negative witness) | — |
| **Diversity collapse (M≥2, <2 classes)** | `t2_model_class_diversity != "full"`, reason `degraded-model-diversity`, exit `11` | Survivors resolved onto the same model class; read distinct `output_files[].model_id` of succeeded workers | Widen the `T2Model0N` pool to span ≥2 classes, or accept degrade; never PASS | — |

### 25.2 On-Call Expectations

| Aspect | Detail |
|--------|--------|
| Surface | Developer/CI tool; no production rotation. "On-call" = the engineer who ran the reflect audit. |
| Pollability | `--detached`/tmux + `done.json` sentinel + `--tui` for long headless Tier-2 subruns (NFR-RH2.7). |
| Knowledge prereqs | `~/.aienv` proxy contract (`:4000/cli`, `T2Model0N`); the (M,N) divergence table; verdict→exit-code map. |

---

## 26. Cost & Resource Estimation *(light)*

> The cost driver is proxy token spend for external `T2Model0N` reviewer calls. No infra/hosting cost (local CLI).

### 26.1 Per-Run Proxy Call Budget

| Scenario | Reviewer calls (worst case) | Formula | Notes |
|----------|-----------------------------|---------|-------|
| Single audit, no `--fix` | `N` (= `--reviewers`, default 3) | `reviewers` | One fan-out of N proxy calls + one adversarial (Mode A) pass |
| `--fix` loop | up to `(max_fix_iterations + 1) × reviewers` | `(max_fix_iterations + 1) × reviewers` | Each re-audit re-runs the full ensemble (idempotent re-verify, NFR-4); `max_fix_iterations` default 2 → up to `3 × 3 = 9` proxy reviewer calls (R8) |
| CI proof | `0` proxy calls | `--transport stub` | Stub is deterministic + network-free (NFR-RH2.4); re-audits under stub are free |

### 26.2 Cost Notes

- The auto-fix multiplier is **bounded** by `max_fix_iterations` (default 2); surfaced so operators can size proxy credits before a long `--fix` run (R8 mitigation).
- `--transport stub` re-audits cost zero proxy tokens — use it in CI and for formation regression tests.
- Adversarial Mode A scoring is one pass per audit (Claude-side, not a `T2Model0N` proxy call); the convergence score is **telemetry recorded at tier 2, NOT a pass gate** (a low score alone does not fail a PASS — spec §5.3 `phase_c_to_d`).

---

## 27. References & Resources

### 27.1 Related Documents

| Document | Type | Path |
|----------|------|------|
| FR-RH2 release spec | Spec (source of truth) | `.dev/reflect-hardening/issue-2-headless-ensemble/spec.md` |
| PRD extraction | Research | `.dev/tasks/.../research/00-prd-extraction.md` |
| Reflect contract verdict derivation (OI-1 reflect half) | Research | `.dev/tasks/.../research/02-reflect-contract-verdict.md` |
| Swarm reduce/merge/contract (OI-1 swarm half) | Research | `.dev/tasks/.../research/05-swarm-reduce-merge-contract.md` |
| Precedents + adversarial handoff | Research | `.dev/tasks/.../research/08-precedents-adversarial-handoff.md` |
| Web grounding (import vs subprocess fan-out) | Research | `.dev/tasks/.../research/web-01-inprocess-import-vs-subprocess-fanout.md` |
| Reuse audit (S_reuse 0.81, reuse-by-import) | Research | `.dev/tasks/.../research/reuse-audit.yaml` |

### 27.2 Key Source Files

| File | Role |
|------|------|
| `src/superclaude/cli/reflect/runner.py` | reflect wrapper; `_audit_once` rewire target (M3) |
| `src/superclaude/cli/reflect/contract.py` | `derive_verdict` (L130–246); 4-state ordering `blocked→degraded→halted→pass`; diversity-source change |
| `src/superclaude/cli/reflect/models.py` | `Verdict` enum + exit-code map (`pass→0/halted→10/degraded→11/blocked→2`, L44–49) |
| `src/superclaude/cli/reflect/ensemble.py` | **to-be-created** thin driver (imports `dispatch_wave1`/`_resolve_run_transport_factory`/`reduce_wave3`) |
| `src/superclaude/cli/reflect/config.py` | `--transport`/`--reviewers` plumbing (M4) |
| `src/superclaude/cli/swarm/dispatch.py` | `dispatch_wave1` fan-out via `ParallelExecutor` (L334/344) |
| `src/superclaude/cli/swarm/commands.py` | `_resolve_run_transport_factory` (L612/619); next-command build (L2058–2081); `ModelPoolTooSmallError` (L589–609) |
| `src/superclaude/cli/swarm/reduce.py` | `reduce_wave3` (L555); M-count (L648); `emit_contract` DM-012 (L369) |
| `src/superclaude/cli/swarm/merge.py` | `mechanical_merge` (8 LOC, L50–57); scoring-free boundary wall |
| `src/superclaude/cli/swarm/lenses/bare_review.py` | the lens `reflect-review` mirrors (`suspect=True`, `tier="T2"`, L63–66) |
| `src/superclaude/cli/roadmap/validate_executor.py` | **§21 prior art** — `_build_multi_agent_steps` separate-process-per-agent fan-out (L317–373/378), untouched |
| `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` | Mode A `--compare` scorer (no `--suspect-source` parse — D5/Q5) |
| `tests/cli/reflect/test_no_nesting_guard.py` | NFR-7 Layer B guard (extend to `ensemble.py`, M6) |

### 27.3 External References (web-01, supplementary)

| Resource | Why relevant | Link |
|----------|--------------|------|
| Claude Code issue #61993 | nested sub-agent spawning silently fails; flat in-process workaround (Alt 2 / Alt 0 root cause) | https://github.com/anthropics/claude-code/issues/61993 |
| Claude Code issue #31977 | in-process team agents lack the Agent tool (corroborates import-don't-nest) | https://github.com/anthropics/claude-code/issues/31977 |
| SO: subprocess vs import | "import is generally vastly preferable to spawning a separate process" (integration sub-decision) | https://stackoverflow.com/questions/48862112/subprocess-or-import-to-invoke-a-script-in-python |
| ricardoanderegg: replace FFI CLI subprocess | subprocess fan-out's honest cost: startup + serialization tax (Alt rejection) | https://ricardoanderegg.com/posts/replace-ffi-cli-subprocess-call |

---

## 28. Glossary

| Term | Definition |
|------|------------|
| **Tier-2 ensemble** | sc:reflect's heterogeneous multi-reviewer pass: 2–4 reviewers on distinct model classes whose outputs are adversarially merged (Mode A). The capability this spec restores in headless mode. |
| **In-process Task fan-out** | The broken status-quo mechanism: a single `claude -p` reflect subprocess uses the Task tool to spawn reviewer sub-agents in-process. Fails because subagent→agent nesting is not exposed under `claude -p` (Alt 2). |
| **Swarm-driven fan-out** | The chosen mechanism: `ensemble.py` imports the swarm dispatch library (`dispatch_wave1`/`_resolve_run_transport_factory`/`reduce_wave3`) in-process and fans out to external `T2Model0N` proxy workers — no second `claude -p`. |
| **single-reviewer-fallback** | A `merge_method` value (and reflect reason slug) signalling M==1: only one reviewer survived/was requested. Maps to `degraded` / exit 11. Reached by `--reviewers 1` (negative witness) OR N>1 with N−1 failures. |
| **t2_model_class_diversity** | Reflect contract field: `"full"` when the **distinct `model_id`s of the M succeeded workers** span ≥ the expected distinct-class count. Computed over succeeded M, not requested N — two survivors on the same class do NOT count as `full`. |
| **T2Model0N** | The external proxy model pool from `~/.aienv` (`T2Model01..NN`), reachable only via the `:4000/cli` base. Each reviewer slot binds a distinct `T2Model0N` (no Claude model id, no `:4000/v1`/`:8317` probing). |
| **ModelPoolTooSmallError** | Eager preflight guard (`commands.py:589–609`) raised before dispatch when the `T2Model0N` pool < `--reviewers`. Surfaces an actionable message (add slots or reduce count). |
| **Negative witness** | The one-reviewer test proving the ensemble proof is falsifiable: a `--reviewers 1` run MUST fail the positive Tier-2 assertions (degrade), so FR-RH2.5's positive proof cannot pass vacuously (FR-RH2.6 / NFR-RH2.3). |
| **suspect:true** | Lens/caller metadata stamped on every reflect-review (and bare-review) artifact, marking it as an unscaffolded external review to be scored — never trusted raw — by `/sc:adversarial` Mode A. Today Mode A's rubric has no `suspect` branch (advisory; D5/Q4/Q5). |
| **M / N** | M = succeeded workers (`WorkerResult.status == "success"`); N = requested reviewer slots. The Tier-2 fan-out is a filtering pipeline N→M; the verdict is derived over M (the (M,N) divergence guard table). |
| **DM-012** | The swarm `ResultContract` data model (`models.py` L876, 19 keys) serialized as `to_dict()` → `<output_dir>/t2-swarm/return-contract.yaml`. Disjoint from the reflect contract schema (shares only the `status` key name). |
| **Mode A** | `/sc:adversarial`'s "Compare Existing Files" mode (`--compare file1,…,file10`): the meta-model adversarial scorer that consumes the per-reviewer `final_path` artifacts and emits a convergence score. The aggregator for the Tier-2 ensemble (not statistical voting). |
| **`final_path`** | The per-reviewer post-normalization artifact pointer on each `WorkerResult` in `output_files`. Both `mechanical_merge` and reflect's Mode A handoff consume `final_path` (succeeded workers only) — **never** `merged.md`. |
| **`merged.md` / mechanical_merge** | Swarm's scoring-free verbatim concat of per-reviewer `final_path`s (8 LOC, `merge.py`). Explicitly NOT the adversarial verdict — must never flow into Mode A as the merged input (FR-RH2.3). |

---

*Status: Complete*
