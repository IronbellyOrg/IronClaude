# QA Report — Research Gate (Gap-Detection Lens)

**Topic:** FR-RH2 Headless Ensemble (issue-2-headless-ensemble)
**Date:** 2026-06-20
**Phase:** research-gate
**Lens:** gap-detection (find implementation surface the spec/TDD require that no research file covers)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Assigned files:** research/01..06 (sole instance — full scope, not a partition)

---

## Overall Verdict: FAIL

Two gaps found. One CRITICAL (blocks the builder from writing a faithful FR-RH2.3 checklist item),
one MINOR. Per research-gate rules, **ANY gap regardless of severity = FAIL** — all gaps must be
resolved before synthesis/task-build proceeds.

The research set is, on the whole, **unusually strong**: dense, zero-trust, code-verified, with exact
`file:line` anchors, verbatim signatures, OI-1 fully mapped (left + right columns), drift surfaced
(done.json emitter, Literal-vs-enum, LensEntry field count, the `test_inv005` vs `test_model_pool_guard`
pool-guard correction). The two gaps below are *seams the research never opened*, not quality defects in
what it covered.

---

## Items Reviewed (8-point gap-detection checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Each FR-RH2.N acceptance criterion has a research-backed implementation anchor | PARTIAL → **FAIL on FR-RH2.3** | FR-RH2.1/.2/.4/.5/.6/.7/.8/.9 are anchored (R1 seam, R4 lens, R2 verdict, R6 stub/mock, R3 dispatch). FR-RH2.3's adversarial-scoring half is NOT anchored — see Gap G1. |
| 2 | Adversarial-merge integration (how ensemble.py invokes /sc:adversarial Mode A and gets `adversarial_convergence_score`) is covered | **FAIL** | Grep of all 6 research files for the ensemble→adversarial bridge mechanism = ZERO hits. `/sc:adversarial` is a Claude-inference SKILL (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md`); there is NO `cli/adversarial` Python module. No research file investigates how an in-process, NFR-7-constrained Python module obtains a return-contract from a skill. Gap G1. |
| 3 | §4.6 ordering + M0/M3 gate (OI-1 closes before FR-RH2.3) derivable from research | PASS | R2 §7 maps the full OI-1 left column (every field `derive_verdict` reads); R3 §7 confirms the right column (all reflect verdict fields absent from swarm `ResultContract`). The disjointness that makes OI-1 a blocking gate is fully evidenced. Builder can derive M0-before-M3. |
| 4 | (M,N) guard-table behaviors (I3-I6: 2-of-3, dup-survivor, M==1, M==0) each have a verdict-compute anchor | PASS | R2 §2 verifies every degraded trigger by line (trigger 7 diversity 267-269; trigger 10 single-reviewer-fallback 280-281; trigger 6 tier1 263-264); R3 §4 gives M=`workers_succeeded` (reduce.py:648) and the success-only count. M==0→blocked is anchored to the existing structural BLOCKED slugs (R2 §6) + the Q6 `ensemble-empty`-absent finding. |
| 5 | `make sync-dev`/`make verify-sync` DoD requirement captured (lens is a src/ component) | PASS (DoD-level) | All research correctly scopes new files to `src/superclaude/cli/...` (R4 registry edits, R1 ensemble.py). The lens + template are src/ components → DoD must run `make sync-dev`/`make verify-sync`. TDD §24.1 already lists `make verify-sync` green. Builder has enough; not a research gap. |
| 6 | Path-confinement (two return-contract.yaml; reflect parses only output_dir/return-contract.yaml) researched for I8 | PASS | R3 §4 anchors swarm's `emit_contract` → `<output_dir>/return-contract.yaml` (reduce.py:721-722, CONTRACT_FILENAME reduce.py:139); R1 §4 anchors reflect's `contract_path` property → `output_dir / "return-contract.yaml"` (models.py:88-91). The two-file design + the `t2-swarm/` subdir confinement is derivable. |
| 7 | Integration points between cli/reflect and cli/swarm (PreflightResult build for dispatch_wave1; lens prompt/briefs supply) | PARTIAL → **MINOR FAIL** | The lens-prompt/briefs supply IS covered (R4 §1 full crib + R3 dispatch `prompt=` kwarg). The `PreflightResult` *construction* that ensemble.py must build to feed `dispatch_wave1` is NOT — R3 only reads N *from* `preflight_result.manifest.preflight.workers_requested`, never documents how to build one. Gap G2. |
| 8 | Findings are actionable (specific file + line + action) | PASS | Every research file is anchored to exact `file:line` with verbatim signatures. Drift is explicitly flagged with corrected anchors. This is exemplary. |

---

## Confidence Gate

Per-item categorization (8 checklist items, each verified with tool evidence):

- [x] VERIFIED 1 — read all 9 FR-RH2 ACs in spec §3 + cross-checked each against the 6 research files (Read + Grep).
- [x] VERIFIED 2 — grepped all 6 research files for the bridge mechanism (zero hits); confirmed `/sc:adversarial` is a SKILL not a CLI module (`ls src/superclaude/skills/sc-adversarial-protocol/` + `ls src/superclaude/cli/ | grep advers` → none); read SKILL.md Mode A return-contract (convergence_score is an inference-produced YAML field, L433-434/451-452).
- [x] VERIFIED 3 — read R2 §7 (OI-1 left col) + R3 §7 (right col).
- [x] VERIFIED 4 — read R2 §2 trigger table + R3 §4 M-count line.
- [x] VERIFIED 5 — confirmed src/ scoping across R1/R4; DoD-level, not a research gap.
- [x] VERIFIED 6 — read R3 §4 + R1 §4 contract-path anchors.
- [x] VERIFIED 7 — grepped research for `PreflightResult(` construction (only read-from hits, no build recipe).
- [x] VERIFIED 8 — inspected anchor density across all 6 files.

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 (spec, tdd ×3 page-reads, research 01-06, sc-adversarial SKILL grep) | Grep: 6 | Glob: 0 | Bash: 5 (greps/ls batched)
- No web research performed (all claims are repo-internal source-truth; Principle 6).
- Tool-call count (Read 11 + Grep 6 = 17) ≥ checklist items (8): not suspect.

---

## Issues Found (severity-rated gaps)

| # | Severity | Location (FR/test/phase affected) | Gap | Required remediation |
|---|----------|-----------------------------------|-----|----------------------|
| G1 | **CRITICAL** | FR-RH2.3 (Phase 2 / M3 in TDD §23.2); FR-RH2.4's `adversarial_convergence_score`/`merge_method` fields; tests I1, U8; OI-1 right-hand synthesis | **The ensemble.py → /sc:adversarial bridge mechanism is uncovered.** `/sc:adversarial` is a Claude-inference SKILL (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md`); there is NO importable `cli/adversarial` Python entrypoint (`ls src/superclaude/cli/` → no adversarial module). Mode A's `convergence_score` + `merged_output_path` are produced by Claude reading a return-contract via inference (SKILL.md L433-434/451-452), NOT by a synchronous Python function. Yet `ensemble.py` is, per NFR-7/NFR-RH2.1/.2, forbidden from `Task(`, `subagent_type`, AND raw `subprocess.run`/`Popen`. The TDD asserts "Mode A returns a convergence_score" (§6 step 8, L893; sequence diagram L870) and synthesizes `adversarial_convergence_score` onto the reflect contract — but **no research file investigates HOW an in-process, agent-surface-free, subprocess-free Python module legally obtains that score.** Worse: the TDD's own cited prior art, `roadmap/validate_executor.py`, performs its adversarial merge **via a `ClaudeProcess` subprocess Step** (`build_merge_prompt`→`ClaudeProcess`, validate_executor.py:365-369) — the exact `claude -p` mechanism the chosen design rejects for the inner loop and that NFR-7 bans in `ensemble.py`. The one concrete precedent therefore uses a forbidden mechanism, and no research file surfaces this contradiction. This directly blocks a builder from writing a faithful, executable FR-RH2.3 checklist item: the item would have to specify the invocation seam, and the research provides none. | Add a 7th research file (or extend R1/R2) that resolves the bridge: (a) confirm whether `/sc:adversarial` Mode A has ANY in-process/CLI entrypoint reflect can call without `Task(`/subprocess, or whether the bridge must be the **already-sanctioned Tier-1 `ClaudeProcess` launch** (the `/sc:reflect` child still runs the adversarial merge over the swarm-produced `final_path` artifacts, with `ensemble.py` only doing fan-out+reduce and the convergence score arriving via the SAME `return-contract.yaml` the Tier-1 child already writes); (b) if so, document that `adversarial_convergence_score`/`merge_method` are emitted by the audit child reading the swarm artifacts — NOT synthesized by `ensemble.py` from swarm facts; (c) reconcile against the TDD's claim that `ensemble.py` itself "hands `--compare` to Mode A and Mode A returns a score." Cite `file:line` for whatever entrypoint is chosen. Until this seam is pinned, FR-RH2.3 is not buildable. |
| G2 | **MINOR** | FR-RH2.1 (Phase 2/3); test I1/I3 setup; `dispatch_wave1` call | **`PreflightResult` construction recipe is missing.** `dispatch_wave1(preflight_result, ...)` requires a `PreflightResult` whose `.manifest.preflight.workers_requested` drives N (R3: dispatch.py:412). R3 documents reading N *from* it and that the run path passes `workers_requested=preflight_result.manifest.preflight.workers_requested` (commands.py:1833-1838), but **never documents how `ensemble.py` constructs/obtains a `PreflightResult`** — its dataclass shape, required fields, or whether a `run_preflight(...)`/builder must be invoked first. A builder writing the `ensemble.py` driver item cannot specify the first call (`preflight = ...`) without this. | Extend R3 (or the new bridge research file) with the `PreflightResult` / `manifest.preflight` dataclass shape + the minimal construction `ensemble.py` needs (which fields are load-bearing for `dispatch_wave1`, and whether `run_preflight` must be called or a lightweight `PreflightResult` can be hand-built for the reflect-review lens). Anchor to `file:line` in `cli/swarm/preflight.py` / `models.py`. |

---

## Non-gaps explicitly cleared (adversarial-stance audit trail)

To justify that "0 issues" would NOT have been believable, here is what I checked and cleared so the
two real gaps stand out:

- **Q4/Q5 (`suspect:true` rubric, `--suspect-source` parsing):** NOT a gap. R4 + TDD Q4/Q5 already
  resolve these — Mode A reads no `suspect` at all (zero SKILL hits), so the handoff is `--compare`
  with suspect advisory. Research is sufficient.
- **Q6 (`ensemble-empty` slug absent):** NOT a gap. R2 §0/§6 gives the `[CODE-VERIFIED]` confirmed-absence
  + the full existing BLOCKED-slug set + both reconciliation options. Builder has enough.
- **Q7 (`_resolve_run_transport_factory` private-symbol coupling):** NOT a gap. R3 §2 flags it CONFIRMED
  PRIVATE with the coupling-smell call-out.
- **Q8 (`--reviewers 1` clamp-vs-passthrough):** NOT a gap. TDD §19.2 resolves it; R1 documents the
  `config.py` clamp seam.
- **done.json drift:** NOT a gap — R3 §4(c) explicitly corrects the TDD (emitter is `emit_done_sentinel`,
  not `reduce_wave3`). This is research catching a TDD error; commendable.
- **File inventory / Status / Summary:** All 6 files are `Status: Complete` with a Summary section
  (verified). 01 carries an early "In Progress" header line but its terminal `## Status: Complete` governs.
- **NFR-RH2.8 proxy-literal grep:** R5 §4 fully grounds U9 (no `:4000`/`:8317`/`/cli`/`/v1` in executable code).

---

## Summary

- Checks passed: 6 / 8 (full pass)
- Checks with gaps: 2 (one CRITICAL, one MINOR)
- Critical issues: 1 (G1 — adversarial bridge mechanism)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Recommendations (before synthesis / task-build proceeds)

1. **Resolve G1 (CRITICAL) first** — it is load-bearing for FR-RH2.3 and the synthesized
   `adversarial_convergence_score`/`merge_method` fields. Spawn one targeted research pass on the
   `ensemble.py → /sc:adversarial` invocation seam (the NFR-7-legal entrypoint), and reconcile the
   TDD's "Mode A returns a score" claim against the fact that no in-process Python adversarial
   entrypoint exists and the cited prior art uses a forbidden `ClaudeProcess` subprocess.
2. **Resolve G2 (MINOR)** — add the `PreflightResult` construction recipe to R3 (or the new file).
3. Re-run this research gate after both gaps close (fix cycle).

## QA Complete
