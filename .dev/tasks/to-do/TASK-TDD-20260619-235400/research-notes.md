# Research Notes: sc:reflect Tier-2 Reviewer Ensemble → Swarm-Driven Fan-Out (headless ensemble fix)

**Date:** 2026-06-19
**Scenario:** A (explicit request — full release spec + named source files + design directives)
**Tier:** Heavyweight (HIGH complexity_score 0.82; cross-subsystem: `cli/reflect` + `cli/swarm` + `/sc:adversarial` boundary + reflect test harness; 4 new files + 5 modified files + ~20 referenced files)
**Status:** Complete

**Driving spec (PRD-equivalent source of requirements):**
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-2-headless-ensemble/spec.md`
(feature_id FR-RH2, infrastructure, target_release 4.4.0, 8 FRs + 8 NFRs + (M,N) divergence contract)

**Final TDD output (MANDATORY destination):**
`/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`
(NOT `docs/` — user pinned this exact path. This is a worktree; all paths resolve to the worktree absolute root.)

**Template schema:** `src/superclaude/examples/tdd_template.md` (v1.2, 28 sections). This is an
infrastructure/CLI-library component → frontend-only sections (§9 State Management, §10 Component
Inventory, §16 Accessibility) are marked **N/A with rationale**; §17/§25/§26 are light (CLI infra, no
prod service surface). All other sections fully completed (Heavyweight).

---

## EXISTING_FILES

### Reflect package — `src/superclaude/cli/reflect/` (the component being re-wired)
- `runner.py` (597 L) — Tier-2 launch seam. **VERIFIED citations:** `_build_prompt` def L341; `_audit_once` def L392 (calls `_build_prompt` L406); `count_model_aliases` L254 reads `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` (alias list L38-40); `write_reflect_post` L117; `write_sidecar` L188; `preflight` L264; `run` L453 (re-audit loop L537 reuses `--base`, NFR-4); `_apply_remediation` L430. `_child_env` L238 preserves `ANTHROPIC_DEFAULT_*`. Spec's "L36-41,254-261" + "L341-366/L392-428" confirmed accurate.
- `contract.py` (366 L) — verdict map. **VERIFIED:** `derive_verdict` L130; ordering "blocked → degraded → halted → pass" first-match-wins (L12, L139); `_degraded_reason` L249; triggers — `degraded-components` L259, `degraded-tier1` L264, `t2_model_class_diversity != full` → `degraded-model-diversity` L267-269, `merge_method == single-reviewer-fallback` → L280-281. Spec's "L249-304 / L266-269 / L280-281" confirmed.
- `config.py` (240 L) — `ReflectConfig`; add `--transport`/`--reviewers` resolved fields (FR-RH2.1/2.5/2.6).
- `models.py` (3954 B) — `Verdict` enum + exit-code map (`pass→0 / halted→10 / degraded→11 / blocked→2`); `ReflectResult` dataclass (fields incl. `tier_reached`, `merge_method`, `reviewer_count`, `t2_model_class_diversity`).
- `commands.py` (12.5 KB) — reflect CLI entry (Click); `--transport`/`--reviewers` surfaced here.
- `__init__.py`.

### Swarm package — `src/superclaude/cli/swarm/` (the shared seam reflect drives, in-process import)
- `dispatch.py` (508 L) — `dispatch_wave1` def ~L344 ("Fan prompt across N workers via ParallelExecutor"); records one `WorkerResult` per slot (`model_id`/`model_label`/`status`/`elapsed_ms`/`final_path`).
- `commands.py` (3806 L) — `_resolve_run_transport_factory` ~L619 ("Build a per-slot transport factory `(slot_index) -> Transport`"); `ModelPoolTooSmallError` (spec L589-609) raised eagerly when pool < workers.
- `reduce.py` (724 L) — `reduce_wave3` ~L578 ("Compute status, trigger merge, emit final ResultContract"); `normalize+merge` mode → per-reviewer `final_path` artifacts + swarm `return-contract.yaml` (DM-012) + `done.json` sentinel.
- `merge.py` (57 L) — **mechanical concat boundary** L9-30 enumerates DISALLOWED ops (sort/rank/score/judge/dedup) and hands scoring to `/sc:adversarial`. MUST stay scoring-free.
- `transports/` — `__init__.py` (Transport protocol), `openai_compat.py` (17 KB, live `:4000/cli` proxy), `stub.py` (7.4 KB, deterministic network-free transport for FR-RH2.5).
- `lenses/bare_review.py` (2762 B) — **the precedent.** `LENS: LensEntry = LensEntry(` L40; `suspect=True` L63; `tier="T2"` L64; `recommended_next_command_template=` L65 → `/sc:adversarial --compare {compare_files}` L66.
- `lenses/__init__.py` (5974 B) — lens registry (where `reflect-review` registers).
- `lenses/_validate.py` (29.6 KB) — lens validator (same gate `reflect-review` must pass).
- `lenses/templates/` — per-lens output templates (e.g. `feasibility-probe-output.md` mirrors the frontmatter convention: `schema_version`/`tier`/`suspect`/`lens` pinned, `reviewer_model_id` substitution).
- `models.py` (87.5 KB) — `LensEntry`, `WorkerResult`, `ResultContract` dataclasses (OI-1 swarm-side source).
- `schema.py` (32 KB) — `CANONICAL_INJECTION_GUARD_SENTENCE` (lens FR-RH2.2 dependency).
- `state.py`, `tmux.py`, `tui.py` — `--detached`/observability (NFR-RH2.7).

### Roadmap reference — `src/superclaude/cli/roadmap/validate_executor.py` (558 L)
- L317-373 — the **separate-process-per-agent** external-fan-out reflection reference (proven model; produced the benchmark reviewer outputs; remains untouched, cited as prior art in §21).

### Pipeline — `src/superclaude/cli/pipeline/process.py` (353 L)
- User-named file. Investigate how the pipeline orchestrates multi-agent passes and whether reflect's audit seam or `/sc:adversarial` Mode A touches it; document the actual connection (or confirm it is orthogonal) — do NOT assume.

### Test harness — `tests/cli/reflect/`
- `conftest.py` (6003 B) — **the mock gap (spec L98-138).** `ClaudeProcess` MagicMock whose `.wait()` copies a canned `fixtures/*.yaml` into `return-contract.yaml`; `fixtures/pass.yaml` hard-codes `tier_reached: 2`. This is why "Tier 2 works" was a fixture assertion, never behavior.
- `test_no_nesting_guard.py` (6760 B) — **NFR-7 guard.** Layer A (skill shell-out) + Layer B (no `Task(`/`subagent`/`anthropic` imports in `runner.py`); FR-RH2.8 extends scan to `ensemble.py`).
- `test_verdict_mapping.py`, `test_runner_e2e.py`, `test_writeback.py`, `test_fix_loop.py`, `test_marker_suppression.py`, `test_classify_fix.py`, `test_base_precedence.py`, `test_cli_smoke.py`, `test_docs_cli_parity.py`, `test_promote_plumbing.py` — must stay green (NFR-RH2.6).
- `tests/swarm/` — `test_dispatch.py`, `test_commands_run.py` (stub-transport integration precedent, L516/548/551 `results==workers`), `test_inv005_pool_guard.py`/`test_inv007_empty_pool.py` (pool guard), `test_merge_mechanical_only`-style boundary tests, `test_bundled_lenses.py`/`test_cli_registration.py` (lens registration).

### Precedent skill — `src/superclaude/skills/sc-bare-review/SKILL.md` (5225 B)
- The thin-caller-over-swarm precedent reflect's `ensemble.py` mirrors: dispatch `swarm run --lens bare-review` → hand normalized artifacts to `/sc:adversarial --suspect-source`.

---

## PATTERNS_AND_CONVENTIONS
- **In-process library import (NOT CLI shellout) is the PRIMARY integration** (spec Decision §2.1 last row; §5.3 `integration: in_process_library_import`). `ensemble.py` imports `dispatch_wave1` + `_resolve_run_transport_factory` + `reduce_wave3` directly. This keeps NFR-RH2.2 (no raw `Popen`/`subprocess.run` in reflect pkg) trivially true and lets `derive_verdict` run in-process. The `superclaude swarm run --lens reflect-review` CLI is retained ONLY as the optional `--detached`/tmux observability variant (§8.3, NFR-RH2.7) — NOT the default inner-loop transport.
- **Boundary invariant:** `swarm/merge.py` is a mechanical concat (merge.py:9-30); scoring lives in `/sc:adversarial` Mode A. Reflect consumes `output_files[].final_path` per-reviewer artifacts, NEVER `merged.md`, as the adversarial input.
- **Path-confinement (two contracts):** reflect parses `<output_dir>/return-contract.yaml` only; the swarm subrun's `<output_dir>/t2-swarm/return-contract.yaml` (DM-012) is consumed by `ensemble.py` only — reflect.derive_verdict MUST NOT parse the subdir contract directly.
- **Diversity & reviewer_count measured over SUCCEEDED workers M, not requested slots N** (FR-RH2.4/2.9). `success` counts toward M; `proxy_error`/`timeout`/`parse_error` do not.
- **Verdict ordering is load-bearing:** `blocked → degraded → halted → pass`, first-match-wins (contract.py:12,139). M==0 → blocked (exit 2), ordered ahead of degraded.
- **Proxy contract (`~/.aienv`):** base `:4000/cli` + models `T2Model01..NN` only. NEVER probe `:4000/v1` / `:8317`. (mem: aienv_only_proxy_contract.) `read_env` preflight; `ModelPoolTooSmallError` if pool < `--reviewers`.
- **Lens convention:** `LensEntry` literal mirroring `bare_review.py`; `suspect:true`, `tier:"T2"`, `default_workers ∈ [2,4]`, NO hard-coded Claude model (models come from `T2Model0N` env pool, not `spec.workers.models`); `recommended_next_command_template` carries `/sc:adversarial` + `{suspect_files}` substitution; passes `_validate.py`.

## PRD_CONTEXT
Source is the FR-RH2 release spec (PRD-equivalent). Extracted requirements:
- **8 FRs:** RH2.1 (ensemble via swarm not in-process Task), RH2.2 (`reflect-review` lens), RH2.3 (swarm artifacts scored by sc-adversarial Mode A, not swarm merge), RH2.4 (faithful run → tier 2 / merge≠fallback / reviewer_count≥2 / diversity=full over M survivors), RH2.5 (credit-free `--transport stub` proof), RH2.6 (one-reviewer negative witness degrades), RH2.7 (return-contract shape unaffected), RH2.8 (NFR-7 preserved or amended on the record), RH2.9 (N→M divergence boundary table).
- **8 NFRs:** RH2.1 no in-process Task fan-out; RH2.2 thinness/isolation (no `cli.sprint`/`cli.roadmap` import, no async, no raw subprocess); RH2.3 non-vacuous proof (positive+negative witness); RH2.4 credit-free CI (zero network I/O); RH2.5 model-class diversity full when pool≥reviewers; RH2.6 backward-compat (existing tests unchanged); RH2.7 observability (`--detached`/done.json/`--tui`); RH2.8 proxy contract respected.
- **CLI surface:** `--transport {openai_compat|stub}` (default openai_compat), `--reviewers <N>` (clamp [2,4], default 3, 1=negative witness), `--depth {standard|deep}`.
- **(M,N) guard table** (§5.3): M==0→blocked/exit2/`ensemble-empty`; M==1→degraded/exit11/`single-reviewer-fallback`; M≥2 but <2 classes→degraded/exit11/`degraded-model-diversity`; M≥2 ∧ ≥2 classes→pass-eligible/exit0.
- **4 Open Items:** OI-1 (**BLOCKING GATE** — swarm ResultContract→reflect contract field correspondence table; resolve BEFORE FR-RH2.3 code), OI-2 (NFR-7 amendment text), OI-3 (stub auto-select in CI), OI-4 (sc-adversarial suspect rubric symmetry reflect-review vs bare-review).

## SOLUTION_RESEARCH
Three alternatives the spec evaluated (feed TDD §21 Alternatives Considered):
- **Alt 0 (Do Nothing):** headless Tier-2 stays broken (degrades to tier 1, 0 adversarial reviewers, single-reviewer-fallback). Not viable — defect is architecturally guaranteed (NFR-7 forbids the only in-process alternative).
- **Alt A (rebuild per-reviewer fan-out inside `runner.py`):** duplicates swarm's hardened seam (per-slot model binding, too-small-pool guard, WorkerResult/contract surface). Rejected — reuse-by-import wins (reuse-audit S_reuse 0.81).
- **Alt B (keep in-process Task fan-out):** the broken path; fails on subagent→agent nesting under `claude -p`. Rejected — root cause.
- **Integration sub-decision:** in-process library import (chosen) vs CLI subprocess shellout (sc-bare-review precedent). Library import chosen for NFR-RH2.2 (no second subprocess) + in-process `derive_verdict`; CLI path kept for `--detached` observability only.

## RECOMMENDED_OUTPUTS
- Research files: `research/01..08-*.md` (see SUGGESTED_PHASES).
- Reuse audit: `research/reuse-audit.yaml` (DONE — orchestrator step-2a).
- Web research (optional, 1): `research/web-01-inprocess-import-vs-subprocess-fanout.md`.
- Synthesis files: `synthesis/synth-01..09-*.md` (template-section-aligned).
- Final TDD: `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md`.

## SUGGESTED_PHASES

**Phase 2 — Deep Investigation (8 parallel codebase agents + 1 optional web agent):**

- **R01 — Reflect runner Tier-2 seam (Code Tracer).** Files: `cli/reflect/runner.py` (`_build_prompt` L341, `_audit_once` L392, `run` L453, re-audit loop L537, `count_model_aliases` L254, `write_reflect_post` L117, `write_sidecar` L188, `_apply_remediation` L430, `_child_env` L238), `cli/reflect/commands.py`. Document the EXACT current Tier-2 launch (single `claude -p` + in-process Task fan-out reliance), what `_audit_once` returns (`ReflectResult`), and the precise seam where `ensemble.py` is wired in (FR-RH2.1 §4.2). Output: `research/01-reflect-runner-seam.md`.
- **R02 — Reflect contract + verdict map [OI-1 reflect side] (Data Model Analyst).** Files: `cli/reflect/contract.py` (`derive_verdict` L130, `_degraded_reason` L249, all triggers L259-281), `cli/reflect/models.py` (`Verdict` enum + exit map, `ReflectResult` fields). Enumerate EVERY field `derive_verdict` reads from `return-contract.yaml` with type + semantics (`tier_reached`, `merge_method`, `reviewer_count`, `t2_model_class_diversity`, `degraded_components`, ...). This is half of the OI-1 BLOCKING table. Output: `research/02-reflect-contract-verdict.md`.
- **R03 — Swarm dispatch seam (API Surface Mapper).** Files: `cli/swarm/dispatch.py` (`dispatch_wave1` ~L344), `cli/swarm/models.py` (`WorkerResult`). Document `dispatch_wave1` full signature (params, return), the `WorkerResult` shape (model_id/model_label/status enum/elapsed_ms/final_path), and the `ParallelExecutor` fan-out + timeout/retry matrix. Output: `research/03-swarm-dispatch.md`.
- **R04 — Swarm transport factory + pool guard + proxy contract (API Surface Mapper).** Files: `cli/swarm/commands.py` (`_resolve_run_transport_factory` ~L619, `ModelPoolTooSmallError` L589-609), `cli/swarm/transports/__init__.py`, `transports/openai_compat.py`, `transports/stub.py`, the `~/.aienv` `read_env` preflight. Document how slot i → distinct `T2Model0N`, the Transport protocol, the StubTransport interface (how it yields deterministic per-slot results offline), and the exact `ModelPoolTooSmallError` message/raise condition. Output: `research/04-swarm-transport-pool.md`.
- **R05 — Swarm reduce + merge boundary + contract emission [OI-1 swarm side] (Code Tracer).** Files: `cli/swarm/reduce.py` (`reduce_wave3` ~L578, normalize+merge mode), `cli/swarm/merge.py` (L9-30 boundary), `cli/swarm/models.py` (`ResultContract`). Enumerate EVERY field the swarm `ResultContract` / `return-contract.yaml` (DM-012) emits, the `done.json` sentinel, how M (success count) is computed, and `output_files[].final_path`. This is the other half of OI-1 — produce the swarm-field → reflect-field correspondence table (the BLOCKING GATE deliverable). Output: `research/05-swarm-reduce-merge-contract.md`.
- **R06 — Swarm lens registry + bare_review precedent (Integration Mapper).** Files: `cli/swarm/lenses/bare_review.py`, `lenses/__init__.py` (registry), `lenses/_validate.py` (validator gate), `lenses/templates/feasibility-probe-output.md` (+ bare-review template), `cli/swarm/models.py` (`LensEntry`), `schema.py` (`CANONICAL_INJECTION_GUARD_SENTENCE`). Document the LensEntry field set, how registration + validation work, the template frontmatter convention, and the exact shape the `reflect-review` lens + output template must take (FR-RH2.2). Output: `research/06-swarm-lens-registry.md`.
- **R07 — NFR-7 guard + test harness mock gap (Code Tracer + Doc Analyst).** Files: `tests/cli/reflect/test_no_nesting_guard.py` (Layer A/B regexes — what exactly each scans), `tests/cli/reflect/conftest.py` L98-138 (`ClaudeProcess` mock + `fixtures/pass.yaml`), `tests/cli/reflect/test_verdict_mapping.py`, `test_runner_e2e.py`, `test_writeback.py`, plus `tests/swarm/test_commands_run.py` (stub integration precedent) + `test_inv005_pool_guard.py`. Document precisely how to extend the guard to `ensemble.py` (FR-RH2.8), the mock gap (FR-RH2.5 must NOT reuse the canned-fixture path), and the stub-integration test template (positive ≥2 + negative 1-reviewer witness). Output: `research/07-nfr7-guard-test-harness.md`.
- **R08 — Precedents: sc-bare-review + sc-adversarial Mode A handoff + roadmap-validate + pipeline/process (Doc Analyst).** Files: `skills/sc-bare-review/SKILL.md` (thin-caller precedent + `--suspect-source` handoff), `cli/roadmap/validate_executor.py` L317-373 (separate-process-per-agent reference), `cli/pipeline/process.py` (document its actual role / whether it is orthogonal — do not assume), and the sc-adversarial-protocol Mode A `--compare`/`--suspect-source` interface. Document how `ensemble.py` should hand `final_path` artifacts to `/sc:adversarial` Mode A and OI-4 (suspect rubric symmetry). Output: `research/08-precedents-adversarial-handoff.md`.
- **WEB-01 (optional, 1 agent) — In-process library import vs CLI-subprocess fan-out; OpenAI-compatible multi-model parallel review patterns.** Light external grounding for §21 Alternatives + §6 design-decision rationale (avoiding nested-subprocess; concurrent.futures fan-out idioms). Output: `research/web-01-inprocess-import-vs-subprocess-fanout.md`.

**Phase 3 — Completeness Verification:** rf-analyst (research completeness, incl. OI-1 table fully populated from R02+R05) ∥ rf-qa (evidence quality — every file:line cited must be Read-verified).

**Phase 4 — Web Research:** WEB-01 above (or fold into Phase 2; keep minimal — internal infra).

**Phase 5 — Synthesis + Analyst + QA gate.** Synthesis files mapped to template sections (see TEMPLATE_NOTES / SYNTHESIS_MAPPING below).

**Phase 6 — Assembly (rf-assembler) → rf-qa structural → rf-qa-qualitative content review.**

**Phase 7 — Present + complete task.**

### SYNTHESIS_MAPPING (research → synthesis → TDD template section)
- `synth-01` → §1 Executive Summary + §2 Problem Statement & Context ← spec §1+§1.1 evidence table, R01, R02, R07 (mock gap).
- `synth-02` → §3 Goals & Non-Goals + §4 Success Metrics + §5 Technical Requirements ← spec §3 FRs (FR-001.. mapping to FR-RH2.1-2.9), §6 NFRs, §1.2 scope boundary.
- `synth-03` → §6 Architecture (high-level diagram, module dependency graph, §6.4 key design decisions) ← spec §2+§2.1+§2.2+§4.4, R01-R06.
- `synth-04` → §7 Data Models + §8 API Specifications (CLI surface + phase contracts + **OI-1 swarm→reflect field-correspondence table** + WorkerResult/ResultContract shapes) ← spec §5.1/§5.3, R02+R03+R05.
- `synth-05` → §12 Error Handling & Edge Cases ((M,N) divergence table, ModelPoolTooSmallError, transport-enum guard, path-confinement) + §9/§10 marked N/A ← spec §5.3, R04, FR-RH2.9.
- `synth-06` → §13 Security + §14 Observability ← proxy contract NFR-RH2.8, `done.json`/`--detached`/`--tui` NFR-RH2.7, suspect:true framing, R04+R06.
- `synth-07` → §15 Testing Strategy ← spec §8.1/8.2/8.3, R07 (stub integration positive + negative witness + partial-failure + duplicate-survivor + all-fail tests).
- `synth-08` → §18 Dependencies + §19 Migration & Rollout + §20 Risks ← spec §4.4 dep graph, §9 migration/rollback/NFR-7 reconciliation, §7 risks.
- `synth-09` → §21 Alternatives Considered (Alt 0/A/B + integration sub-decision) + §22 Open Questions (OI-1..4 → Q1..Q4) + §23-27 (timeline=impl order §4.6; release criteria=FR/NFR acceptance; operational readiness light) + §28 Glossary ← spec §2.1, §11, §4.6, Appendix A.

## TEMPLATE_NOTES
Use **Template 02 (Complex Task)** — discovery + parallel investigation + completeness gate + synthesis + assembly with double QA. Final document conforms to `tdd_template.md` v1.2 (28 sections). Heavyweight line budget 1,200-1,800. TDD discipline: describe HOW (architecture/contracts/data) NOT WHAT (the spec's FRs are the WHAT) — but a TDD legitimately restates requirements as §5 Technical Requirements traced to the architecture. Do NOT reproduce full implementations; show key interfaces (`dispatch_wave1` signature, `WorkerResult`/`ResultContract`/`LensEntry` shapes, the OI-1 correspondence table, the CLI surface). Frontend-only §9/§10/§16 → "N/A — backend CLI library, no client surface." The **OI-1 swarm→reflect contract field-correspondence table is the single most load-bearing deliverable** (§8 / §7) — it is the BLOCKING GATE that sizes `ensemble.py`'s mapping layer.

## REUSE_AUDIT
(Full grounded findings in `research/reuse-audit.yaml`. Pre-stage = advisory; no code shipped.)
- **`cli/reflect/ensemble.py`** — capability "in-process parallel heterogeneous reviewer fan-out + normalized-artifact adversarial handoff." Neighbours: `swarm/dispatch.py:344` (dispatch_wave1), `swarm/commands.py:619` (transport factory), `swarm/reduce.py:578` (reduce_wave3), `swarm/lenses/bare_review.py:65` (next-command). Scores C_cap 0.86 / C_shape 0.72 / C_aug 0.86 / S_reuse 0.81. Tier maybe-related. **Verdict: reuse-by-import.** Directive: import & compose `dispatch_wave1` + `_resolve_run_transport_factory` + `reduce_wave3`; do NOT rebuild fan-out or contract reduction. (Confirms spec Decision §2.1 "adapt the shared seam; do not rebuild.")
- **`cli/swarm/lenses/reflect_review.py`** — neighbours `bare_review.py:40/63/64/66`. S_reuse 0.80. **Verdict: mirror-shape.** Directive: follow `LensEntry` convention; keep a separate lens (reflection-review domain is distinct). No dependency-boundary ban.
- **`cli/swarm/lenses/templates/reflect-review-output.md`** — neighbour `feasibility-probe-output.md` frontmatter convention. S_reuse 0.74. **Verdict: mirror-shape.** Directive: mirror the per-lens template/frontmatter; bind to a recipe; do not invent a new normalized format.
- **`tests/cli/reflect/test_ensemble_stub_integration.py`** — neighbour `tests/swarm/test_commands_run.py:516/548/551` (results==workers stub pattern). S_reuse 0.76. **Verdict: mirror-shape.** Directive: model the non-mocked stub path on existing swarm stub integration tests; keep reflect-specific verdict/contract assertions local.

No `confident-duplicate`/`extract-shared` verdicts. No component is a full duplicate — all four are net-new with strong prior-art shape to mirror or import.

## AMBIGUITIES_FOR_USER
None blocking. Resolved-by-design notes for the TDD to surface rather than ask:
1. **OI-1 (contract field parity)** is a code-grounded investigation, not a user decision — R02+R05 produce the correspondence table; flag as the §22 Q1 BLOCKING gate to resolve before FR-RH2.3 code.
2. **OI-2 (NFR-7 amendment text)** — TDD recommends "confirm scope (Layer B forbids `Task(`/`subagent`/`anthropic` imports + raw subprocess; HTTP workers via in-process `dispatch_wave1` are out of scope) + extend the guard scan to `ensemble.py`"; record as §19 reconciliation. Not a user blocker.
3. **OI-3 (stub auto-select in CI)** and **OI-4 (suspect rubric symmetry)** — low-severity; carry into §22 Open Questions with recommended defaults (OI-3: opt-in `--transport stub`, not auto; OI-4: confirm against sc-adversarial-protocol Mode A `--suspect-source`).
4. **`pipeline/process.py` relevance** — user named it; R08 must establish its actual role (likely orthogonal to the reflect seam) rather than force-fit it. If orthogonal, note that explicitly in the TDD dependency section.
