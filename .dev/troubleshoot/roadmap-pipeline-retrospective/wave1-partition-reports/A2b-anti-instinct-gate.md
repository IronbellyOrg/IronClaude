# Partition A2b — Anti-Instinct Gate Full History

**Source release:** `.dev/releases/complete/v3.1_Anti-instincts__/`
**Files Read:** 8 (of ~126 in partition)
**Method:** Focused-budget retrospective. Prioritised the unified spec, post-execution gap analyses, pipeline-weakness analysis, QA reflection, tasklist-reflection, validation report, debate transcript opener, and phase-4 result. Skipped per-task tasklists, the 27 D-NNNN artifact dirs, all 5 adversarial proposal docs in full (sampled only the debate transcript opener), turnledger-integration sub-history, and the err logs.

---

## Direct relevance to current MultiModelSwarm stub-as-component-name false positive

The anti-instinct gate's **`obligation_scanner.py`** (Module 1 in `anti-instincts-gate-unified.md` §4) is the upstream ancestor of the regex stack now firing at MultiModelSwarm roadmap line 207/211/213. The original V2-A vocabulary defines:

```
SCAFFOLD_TERMS = [
    r"\bmocked?\b", r"\bstub(?:bed|s)?\b", r"\bskeleton\b",
    r"\bplaceholder\b", r"\bscaffold(?:ing|ed)?\b", r"\btemporary\b",
    r"\bhardcoded\b", r"\bhardwired\b", r"\bno-?op\b", r"\bdummy\b", r"\bfake\b",
]
```

(`anti-instincts-gate-unified.md` §4, lines 143–155.)

The current false positive (stub appearing inside what is actually a component/section descriptor noun) is a direct consequence of the V2-A architectural choice: **pure regex + word boundaries, no syntactic context awareness**. The unified spec explicitly states this is intentional (§3, line 101): *"All four detection modules are pure Python with zero LLM calls. This is deliberate — LLM-on-LLM review shares the same blindspots that caused the original bug. The deterministic floor cannot be bypassed by completion bias."* The brittleness driver is therefore baked into the design contract, not a layer that drifted away from intent.

---

## Findings

### F-A2b-001: V2-A obligation scanner shipped as pure-regex by deliberate design decision
- **Type:** FAILURE (latent — manifests later as false-positive volume)
- **Pipeline step:** anti-instinct (post-merge)
- **Symptom:** Scanner flags any line containing `\bstub\b`, `\bmock\b`, `\bskeleton\b`, `\bplaceholder\b`, etc., with only word-boundary disambiguation — no part-of-speech check, no structural-role check, no quoted-string check.
- **Root cause (claimed):** Intentional. The unified spec frames "no LLM calls" as the *defining property* of the gate, on the theory that any LLM-mediated check would share the bug it is meant to catch.
- **Remediation applied:** NONE in v3.1. The five adversarial variant docs (`adversarial/01-*.md`–`05-*.md`) explored alternatives (coherence graph, fingerprints, integration-contract extractor, negative-space prompting) but the merged spec landed on regex + discharge-vocabulary as the obligation-axis module.
- **Outcome:** v3.1 shipped with this design. Subsequent false-positive pressure (the present MultiModelSwarm issue) is the predictable consequence of the design contract, not a regression against it.
- **Still possible today (Auggie check):** NOT CHECKED — surfaced in current session traffic, treated as known-current.
- **Source artifacts:** `anti-instincts-gate-unified.md` §3 line 101, §4 lines 107–172; `adversarial/debate-transcript.md` Rounds 1.

### F-A2b-002: Wiring-verification step scanned the wrong directory (markdown release dir, not src/)
- **Type:** FAILURE
- **Pipeline step:** wiring-verification
- **Symptom:** Step ran `run_wiring_analysis()` against `config.output_dir.parent` — the release artifact dir containing only `.md` files. Reported `files_analyzed: 0`, `total_findings: 0`. Gate passed vacuously.
- **Root cause (claimed):** `roadmap/executor.py:429`: `source_dir = config.output_dir.parent if hasattr(config, 'output_dir') else Path(".")`. Resolved to release dir, not Python source tree.
- **Remediation applied:** Identified as Weakness 2 (CRITICAL) in v3.1 pipeline-weakness-analysis. Proposed fix: add `source_root` field to `RoadmapConfig` or auto-discover via walking up to `src/` / `pyproject.toml`; treat 0-files-analyzed as WARNING, not silent PASS.
- **Outcome:** UNKNOWN — the v3.1 gap-remediation tasklist did not include this fix; it targeted sprint-side wiring (T01-T14) only. The wiring-verification dir bug may still be live.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v3.1/pipeline-weakness-analysis.md` Weakness 2, lines 30–40; `v3.1/roadmap-gap-analysis-merged.md` BUG-008 context.

### F-A2b-003: Anti-instinct components built, tested, and gated — but unreachable from production `execute_sprint()`
- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint-side integration; downstream consumer of anti-instinct outputs)
- **Symptom:** All four detection modules (`obligation_scanner.py`, `integration_contracts.py`, `fingerprint.py`, `spec_structural_audit.py`) exist; `ANTI_INSTINCT_GATE` defined in `gates.py:995` with `enforcement_tier="STRICT"`; `run_post_task_anti_instinct_hook()` correctly wired into `execute_phase_tasks()`. But `execute_sprint()` (the production entry point) **never calls `execute_phase_tasks()`** — uses per-phase `ClaudeProcess` subprocess model exclusively. TurnLedger, ShadowGateMetrics, DeferredRemediationLog: all defined, none instantiated in production path.
- **Root cause (claimed):** Architectural mismatch between two execution models. `execute_sprint()` = per-phase subprocess; `execute_phase_tasks()` = per-task with hooks. v3.1 implementation targeted the per-task path; never wired sprint loop to delegate to it.
- **Remediation applied:** v3.1 gap-remediation tasklist T01-T14. **PARTIAL EXECUTION**: T01 (TurnLedger), T02 (ShadowGateMetrics), T03 (DeferredRemediationLog), T06 (SprintGatePolicy), T07 (KPI report call), T08-T10 (deviation comments) DONE. **T04 (the critical bridge from `execute_sprint()` to `execute_phase_tasks()`) SKIPPED**. T05-A/B (TrailingGateResult wrapping & accumulation) SKIPPED. T11-T14 (tests) SKIPPED. Smoke 5/8 checks pass.
- **Outcome:** Objects instantiated but dead in production. KPI report emits structurally valid but vacuous (`all_gate_results` always `[]`). The bug the anti-instinct gate was designed to catch (components built, never wired) was committed by the anti-instinct gate's own remediation tasklist. The execution-qa-reflection labels this *"the irony"* (roadmap-gap-analysis-merged.md §Agreement Summary item 6).
- **Still possible today (Auggie check):** NOT CHECKED — but the QA reflection explicitly enumerates T04 + T05-A/B as still unimplemented at v3.1 close.
- **Source artifacts:** `v3.1/roadmap-gap-analysis-merged.md` lines 130–172 (CRITICAL BUG-001/002/003 table + TurnLedger Wiring Status); `v3.1/execution-qa-reflection.md` lines 31–45 (T04 SKIPPED) and lines 98–103 (smoke check 4 FAIL).

### F-A2b-004: Validation report declared CLEAN while implementation was 72% complete with 3 CRITICAL bugs
- **Type:** FAILURE
- **Pipeline step:** spec-fidelity / validation
- **Symptom:** `validation/ValidationReport.md` (2026-03-20): *"Result: CLEAN — no drift detected across 4 phases and 20 tasks. Total findings: 0 (High: 0, Medium: 0, Low: 0)."* Generated by 8 sub-agents across 4 phases, all PASS. The *next day*, the merged gap analysis found 3 CRITICAL, 2 HIGH, 3 MEDIUM, 3 LOW bugs (11 total) and rated implementation 72% complete.
- **Root cause (claimed):** v3.1 pipeline-weakness-analysis Weakness 4 — spec-fidelity compares roadmap-vs-spec, never implementation-vs-spec. The 8 validator agents checked tasklist tasks for drift from the roadmap, not for whether the code those tasks produced actually wired into the production dispatch path.
- **Remediation applied:** Documented as W4. Proposed fix: add post-implementation spec-fidelity mode invoked separately after sprint execution; or sprint-self-check via existing `run_wiring_analysis()` (blocked by F-A2b-002).
- **Outcome:** Bug class still latent — validation produced a false-clean signal that would have masked the 3 CRITICAL bugs indefinitely if the human had not also commissioned an independent gap analysis.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `validation/ValidationReport.md` (full file); `v3.1/roadmap-gap-analysis-merged.md` §Final Verdict line 240–248; `v3.1/pipeline-weakness-analysis.md` Weakness 4 lines 58–68.

### F-A2b-005: Gap-remediation tasklist itself contained 3 code-snippet bugs caught only by adversarial reflection
- **Type:** REMEDIATION (caught) / SUCCESS (of the reflection layer)
- **Pipeline step:** remediate
- **Symptom:** The tasklist authored to fix v3.1's wiring bugs contained: (a) T07 `str(kpi_report)` would emit dataclass repr — `GateKPIReport` has no `__str__`, requires `.format_report()`; (b) T05 shadow-mode early return loses the evaluated `TrailingGateResult`, breaking shadow metrics; (c) T08 Option A code snippet called `attempt_remediation(gate_result=..., policy=..., ledger=...)` — actual signature is 6 positional callables/values, so the snippet would fail at runtime; (d) T04's `_parse_phase_tasks()` helper referenced but never specified.
- **Root cause (claimed):** Tasklist generated from gap analysis without round-trip API verification against actual function signatures.
- **Remediation applied:** `v3.1/gap-remediation-reflection.md` ran a per-task fidelity + approach validation pass and produced 5 refactoring recommendations (RR-1 through RR-5). RR-1 (`format_report()`) was applied during execution (confirmed in `execution-qa-reflection.md` T07 entry: "Amendment A1 applied correctly").
- **Outcome:** Caught before execution — reflection layer worked. But the reflection layer is **separate from the pipeline gates**: it only ran because a human explicitly invoked it.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v3.1/gap-remediation-reflection.md` lines 64–80 (T07/T08 bugs), lines 110–127 (RR-1 through RR-5).

### F-A2b-006: Adversarial debate converged on a single hard-coded vocabulary instead of layered detection axes
- **Type:** FAILURE (architectural-decision residue)
- **Pipeline step:** debate / merge
- **Symptom:** Five variants attacked the same `cli-portify` bug from genuinely distinct axes: V1 = ID cross-reference + structural audit; V2 = scaffold-discharge obligation scanner (regex); V3 = producer-consumer coherence graph; V4 = backtick/code-block fingerprint coverage; V5 = integration-contract extractor with 7-category dispatch taxonomy. The merge (`anti-instincts-gate-unified.md`) cherry-picked V2-A (obligation scanner), V4-2 (fingerprints), V1-C (structural audit), V1-D+V5-2 (prompt constraint). V3's coherence-graph approach (the only one that modeled the bug as a graph-theoretic disconnected pair) was dropped.
- **Root cause (claimed):** Optimisation toward `Pipeline latency added: <1s, LLM calls added: 0` (line 11 of unified spec). Coherence-graph + integration-contract extractor required either LLM extraction of producers/consumers from prose, or significant heuristic infrastructure. Regex won on cost.
- **Remediation applied:** NONE — this is the merged design, not a regression.
- **Outcome:** The gate ships with a high-recall, low-precision regex layer. The orthogonal axes V3/V5 covered — relationship-modelling and mechanism-typing — are absent. Result: false positives on lines that mention scaffold *vocabulary as a noun describing a section/component* rather than scaffold *behavior*, exactly what the present MultiModelSwarm issue exhibits.
- **Still possible today (Auggie check):** YES — by construction of the merged design.
- **Source artifacts:** `anti-instincts-gate-unified.md` lines 8–13 (cherry-pick list, latency/LLM cost claim); `adversarial/debate-transcript.md` Round 1 openings (V3 coherence-graph thesis, V5 mechanism-aware thesis).

### F-A2b-007: Validation harness emitted CLEAN with 0 findings while smoke produced 3/8 fail
- **Type:** FAILURE
- **Pipeline step:** test-strategy / certify
- **Symptom:** Phase 4 result: `pass`, exit 0, 720s, 0 files changed (`results/phase-4-result.md`). Validation report: CLEAN, 0 findings. Yet `execution-qa-reflection.md` T14 smoke check enumerates checks #4, #7, #8 as **FAIL**: `execute_phase_tasks(` not present in `execute_sprint`, hook returns `TaskResult` only (not tuple with `TrailingGateResult`), `DeferredRemediationLog.append()` never reached from anti-instinct hook.
- **Root cause (claimed):** Phase 4 produced 0 file changes (line 18 of phase-4-result.md). Validation reads tasklist task completion as proxy for production-path wiring. No gate connects "tasklist tasks marked done" with "the artifacts those tasks promised actually exist in src/".
- **Remediation applied:** NONE in v3.1.
- **Outcome:** Two compounding false-clean signals: phase-4 result and validation report. Only the post-hoc gap-analysis + QA-reflection exercise (manually commissioned) surfaced the truth.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `results/phase-4-result.md` lines 1–20; `validation/ValidationReport.md`; `v3.1/execution-qa-reflection.md` Smoke Verification table lines 91–104.

---

## Cross-cutting patterns within this partition

1. **The defense-in-depth gate caught design-time omissions but missed integration-time wiring.** F-A2b-003 + F-A2b-004 + F-A2b-007: the anti-instinct gate was applied to roadmap-vs-spec content, but its own remediation tasklist (gap-remediation) shipped infrastructure objects that were never reached from `execute_sprint()`. The gate cannot inspect the path it is *not yet wired into*.

2. **Determinism-bias-as-design-philosophy creates downstream false-positive load.** F-A2b-001 + F-A2b-006: the unified spec explicitly elevates "zero LLM calls" to a design property. Adversarial variants offering more semantic context (V3 graph, V5 mechanism taxonomy) were merge-rejected on cost grounds. The result is precisely the brittleness now manifesting.

3. **Multiple-validator-agreement does not buy you correctness when validators share the validation contract.** F-A2b-004 + F-A2b-007: 8 validator agents + 4 phase results all said PASS / CLEAN with 0 findings, while implementation was 72% complete with 3 CRITICAL bugs. Adding more agents to the same shallow check does not deepen the check.

4. **Tasklist authoring drift — code snippets in remediation tasklists are not API-verified.** F-A2b-005: 3 of 14 task snippets had API bugs (T07 `str()`, T05 shadow return, T08 wrong signature). Only the *post-hoc reflection layer* (an extra, human-invoked pass) caught them. The pipeline itself has no contract that tasklist code snippets must be type-checked against actual imports.

5. **Roadmap pipeline scope ends at roadmap; nothing closes the loop to implementation.** F-A2b-002 + F-A2b-003 + F-A2b-004: the wiring-verification step points at markdown artifacts; the spec-fidelity step compares roadmap-vs-spec, never implementation-vs-spec; the anti-instinct gate operates pre-implementation. There is **no pipeline-native gate that runs after sprint execution and verifies code-artifact-reaches-production-entry-point**. v3.1 surfaced this gap (Weaknesses 1-5) but did not fix it.

6. **Scaffolding-vocabulary regex is symmetric across "scaffold-as-behavior" and "scaffold-as-noun".** F-A2b-001 + F-A2b-006: `\bstub\b` matches both "we will stub this method" (real obligation) and "the Stub Layer is a structural noun describing the component being designed" (no obligation). Discharge-term scanning cannot disambiguate, because discharge of a nominal use is undefined.

---

## Brittleness drivers identified

- **D-1 (architectural):** Anti-instinct gate's vocabulary layer is pure word-boundary regex by *design contract* (not by drift). Any disambiguation upgrade must amend the spec-level "zero LLM calls" promise.
- **D-2 (architectural):** Adversarial merge optimised toward latency/LLM-cost minima, dropping the two variants (V3 coherence graph, V5 mechanism taxonomy) that would have given the gate the relational context it now lacks.
- **D-3 (process):** No pipeline gate connects "tasklist task marked complete" with "src/ tree actually contains the wired artifact". Spec-fidelity, wiring-verification, and the validation harness all operate on documents.
- **D-4 (process):** Wiring-verification's `source_dir` defaults to the release output dir, so it analyses 0 Python files and silently passes — and 0-files-analyzed is not promoted to a warning.
- **D-5 (process):** Validation harness fan-out (8 sub-agents) operates on roadmap text. Multiplying agents on the same shallow check yields false confidence (CLEAN, 0 findings) at higher token cost.
- **D-6 (process):** Gap-remediation tasklists are authored from gap analyses without API-signature verification against the actual codebase; bugs caught only when an additional reflection pass is manually invoked.

## Budget note
- Files Read: 8 (`anti-instincts-gate-unified.md`, `v3.1/pipeline-weakness-analysis.md`, `v3.1/execution-qa-reflection.md`, `v3.1/roadmap-gap-analysis-merged.md`, `v3.1/gap-remediation-reflection.md`, `validation/ValidationReport.md`, `adversarial/debate-transcript.md`, `results/phase-4-result.md`).
- Files Skipped (over budget): ~118 (per-task tasklists phase-1..4, 27 D-NNNN artifact dirs, 5 adversarial proposal full bodies, turnledger-integration sub-history, err logs, checkpoints, phase-1/2/3 result files, refactor-plan, scoring-framework, return-contract, merge-log, diff-analysis, base-selection, debate-transcript err pairs, pipeline-weakness sections beyond the validated-weaknesses summary).
- Auggie lookups: 0 (no in-scope failure rose to "still-possible today, need codebase corroboration"; the live MultiModelSwarm false-positive is already known-current and is not what this partition is auditing).
