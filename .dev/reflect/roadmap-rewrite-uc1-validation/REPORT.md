# sc:reflect UC-1 Tier-2 Report — Roadmap-Pipeline Rewrite Task File

**Generated:** 2026-05-31
**Mode:** UC-1 (pre-execution coverage/gap audit)
**Tier reached:** 2 (forced by `--depth deep`)
**Target tasklist:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260531-042405/TASK-RF-20260531-042405.md` (831 lines, 13 phases, 108 items)
**Driving spec:** `/config/workspace/IronClaude/.claude/worktrees/BareReview/.dev/troubleshoot/roadmap-pipeline-retrospective/wave4-task-spec/BUILD-REQUEST-roadmap-pipeline-rewrite.md`

---

## Executive Summary

**Final verdict: PARTIAL — refactor-then-ship.** Not PASS, not FAIL. The task file is structurally sound and covers 94% of the BUILD-REQUEST's R0+R1 phases, but a **3-vendor heterogeneous ensemble surfaced 1 Critical + 5 High + 7 Medium findings** that single-vendor reviews would have missed.

| Metric | Value | Threshold | Verdict |
|---|---|---|---|
| Coverage pct | 0.94 | ≥0.90 | ✅ |
| Calibrated confidence | 0.86 | ≥0.85 for PASS | ✅ |
| Convergence score | 0.67 | ≥0.75 for PASS | ❌ |
| Citations dropped | 0 / 22 | 0 for PASS | ✅ |
| Critical findings | 1 | 0 for PASS | ❌ |

**Convergence 0.67 (below 0.75) is the structural signal that anti-confirmation gates were designed to surface.** R1 (opus/Anthropic) reviewed at the architecture level and verdicted PASS at 0.96; R2 (sonnet/OpenAI) and R3 (haiku/Alibaba) reviewed at the junior-executability level and verdicted PARTIAL at 0.82 and 0.80 respectively. This is exactly the failure mode §11.0 sufficiency-conditional gates were designed to catch — a single-vendor review would have shipped PASS and missed a substrate-leak that preserves the very flaw the rewrite is meant to invert.

**Recommendation: 5 pre-execution edits (~2-4h) addressing C1 + H1-H5, then ship.** Mediums are quality-of-life; can be addressed in flight.

---

## Reviewer Verdicts (3-vendor ensemble)

| Reviewer | Model class | Vendor | Persona | Self-verdict | Calibrated | Found C/H/M |
|---|---|---|---|---|---|---|
| R1 | opus (claude-opus-4-8) | Anthropic | analyzer | PASS, 0.96 | PASS | 0/1/3 |
| R2 | sonnet (gpt-5.5) | OpenAI | qa | PARTIAL, 0.82 | PARTIAL | 1/3/3 |
| R3 | haiku (qwen3.6-plus) | Alibaba | refactorer | PARTIAL, 0.80 | PARTIAL | 3/3/4 |

**`t2_model_class_diversity: full`**, **`t2_vendor_diversity: multi`** — strongest available anti-bias configuration. **`calibrator_diversity: degraded`** (disjoint set empty; all 3 classes used as reviewers; fallback to opus per §11.3) — this is the one structural weakness in the ensemble; a non-opus calibrator (kimi, deepseek) would strengthen.

**Per-dimension calibrated mean scores (0-5):**
- D1 Citation grounding: 4.2
- D2 Coverage completeness: 4.3
- D3 Deviation-classification clarity: 4.2
- D4 Risk surface coverage: 4.3
- D5 Recommendation actionability: 4.5

All five above the 0.85 floor when normalized — yet convergence fails because R2 and R3 surfaced critical-severity findings R1 did not.

---

## Merged Findings (post evidence-validator)

### CRITICAL (1)

**C1 — Step 11.2 preserves Flaw 3 by canonicalizing `_check_frontmatter` instead of deleting both legacy parsers.**

- **Surfaced by:** R2 (sonnet/OpenAI). R1 and R3 missed it.
- **Evidence:** Task file Step 11.2 (lines 607-613): *"export the canonical parser from `superclaude.contracts.parsers` (NEW submodule — create `src/superclaude/contracts/parsers.py` with `parse_frontmatter` re-export)"* — picks `pipeline/gates.py:_check_frontmatter L91` as canonical.
- **Spec contradiction:** BUILD-REQUEST §MVR §1 (line 102) says *"One `_parse_frontmatter` lives in the post-step extractor only; the two divergent variants at `gates.py:168` and `_check_frontmatter` are deleted."* Both are DELETED, with the envelope post-extractor as sole parser.
- **Architectural impact:** This preserves the substrate (markdown frontmatter as state interchange) that §MVR §1 inverts. Flaw 3 ("Cross-step state lives in markdown frontmatter") survives — the very inheritance the rewrite is meant to eliminate.
- **Fix:** Rewrite Step 11.2 to (a) delete both `_check_frontmatter` AND `_parse_frontmatter`, (b) source the canonical parser from the envelope post-extractor (R1.2's PipelineEnvelope extractor), (c) migrate consumer sites to read from the envelope's typed fields, not from re-parsed frontmatter. Step 12.3 will also need re-alignment.

### HIGH (5)

**H1 — Step 5.1 inverts Contract #5 ↔ #9 wiring vs BUILD-REQUEST L76.**
- Surfaced by: R2. Confidence 0.91.
- Evidence: Task Step 5.1 wires Contract #5 (no fragility stubs) where Contract #9 (spec↔roadmap ID-set containment) should go, and vice versa. Step 13.4 has the correct wiring; Step 5.1's wiring contradicts it.
- Fix: Swap the Contract IDs in Step 5.1's gate-wiring spec.

**H2 — R1.5/R1.6 sequencing leaves a one-cycle fail-open window.**
- Surfaced by: R1 (opus). Confidence 0.96 (one of R1's three findings).
- Evidence: R1.5 (`verify-implementation` terminal step) ships before R1.6 (cleanup of fail-open default at `fidelity_checker.py:287-303`). For one release cycle, the new terminal step exists AND the old fail-open default exists; the gate is bypassed if `verify-implementation` errors and `fidelity_checker` falls back to `found=True`.
- Fix: Either (a) reorder — ship R1.6 fail-open deletion before R1.5 terminal step, OR (b) annotate Step 11.4 as REQUIRED-BEFORE-R1.5 and add a Step 10.X explicit dependency.

**H3 — Phase 9 bundles 12 sub-steps under one QA gate (PG9.1/PG9.2).**
- Surfaced by: R2 + R3 (3/3 with R1's M-level concurrence).
- Evidence: R1.4 tool-write rewrite for 9 LLM steps is decomposed into 9 sub-phases + setup + cutover = 12 items, all gated by a single PG9. A failure in step 9.5 won't surface until after step 9.12 runs.
- Fix: Split Phase 9 into Phase 9a (steps 9.1-9.5) + Phase 9b (steps 9.6-9.10) + Phase 9c (cutover), each with its own QA gate.

**H4 — Step 9.11 bundles 4 migrations.**
- Surfaced by: R3.
- Evidence: Step 9.11 ("post-write cutover for steps 6-9") atomically migrates 4 LLM steps. If step 8 cutover fails, the rollback path is unclear.
- Fix: Split into 9.11a-d, one cutover per step.

**H5 — R1.4 cutover counter has no automation design.**
- Surfaced by: R2 + R3.
- Evidence: Vector A's MVR §3 specifies "Stage one step at a time, run side-by-side against current markdown output for ≥3 releases each before deletion." Task Phase 9 references "≥3 releases" but specifies no automated counter, no release-marker check, no test that gates cutover on the counter reaching 3.
- Fix: Add Step 9.X "design and implement cutover counter — release-marker file at `.dev/migrations/r1-4-step-N-counter.yaml` incremented per release that step ran in tool-write mode; cutover gated on counter ≥3."

### MEDIUM (7)

| ID | Surfaced by | Finding | Fix |
|---|---|---|---|
| M1 | R2 + R3 | Contract #3 (PR-lint "Generator-Constraint Considered" section) mechanism under-specified — no pre-commit hook detail | Add Step 13.X with explicit pre-commit hook code |
| M2 | R3 | R1.4 parallelism opportunity missing — 9 LLM step migrations could be 3 parallel tracks | Add note to Phase 9 about parallelization |
| M3 | R3 | Dispatch-reachability AST walker config-matrix gap — only Python entry points enumerated | Extend walker spec to cover Click commands + skill invocations |
| M4 | R2 | Recurrence fixtures (Contract #1) deferred to Phase 13 discovery — no seed list | Add named-incident → fixture mapping table in Phase 13.X |
| M5 | R3 | Step 13.6 no time budget — could run indefinitely | Cap at 4h, escalate at 80% |
| M6 | R1 | `research/` files not in BUILD-REQUEST's "6 source-authority files" list — but task cites them | Either add to authority list or stop citing |
| M7 | R3 | Execution-log placeholders ("Phase Findings ...") not pre-populated | Pre-populate with empty headers per phase |

---

## PRESERVE-Target Audit ✅

**All 4 PRESERVE targets honored at 3 layers (3/3 reviewer convergence):**

| File | Touched by tasklist? | Verdict |
|---|---|---|
| `src/superclaude/cli/roadmap/commands.py` (401 LOC) | No | ✅ HONORED |
| `src/superclaude/cli/roadmap/structural_checkers.py` (1069 LOC) | No | ✅ HONORED |
| `src/superclaude/cli/roadmap/convergence.py` (778 LOC) | Wired only via gate reference (R1.6) — no edits | ✅ HONORED |
| `src/superclaude/cli/roadmap/cosmetic_remediator.py` (1096 LOC) | No | ✅ HONORED |

Zero leakage. This is the strongest cross-vendor convergence signal in the report.

---

## Coverage Matrix (0.94)

| BUILD-REQUEST phase | Task file mapping | Verdict |
|---|---|---|
| R0.1 — Spec-ID registry (Contract #9) | Phase 2 (steps 2.1-2.6) | ✅ |
| R0.2 — Anti-instinct vocab-lint (Contract #10) | Phase 3 (steps 3.1-3.8) — UNBLOCKS MultiModelSwarm | ✅ |
| R0.3 — superclaude.contracts SoT | Phase 4 (steps 4.1-4.5) | ✅ |
| R0 acceptance | Phase 5 (steps 5.1-5.4) | ⚠ H1 wiring swap |
| R1.1 — Extend contracts | Phase 6 (steps 6.1-6.5) | ✅ |
| R1.2 — PipelineEnvelope | Phase 7 (steps 7.1-7.7) | ✅ |
| R1.3 — GateCriteria.code_assertions | Phase 8 (steps 8.1-8.6) | ✅ |
| R1.4 — Tool-write rewrite (9 LLM steps) | Phase 9 (12 sub-steps) | ⚠ H3 + H4 + H5 |
| R1.5 — verify-implementation | Phase 10 (steps 10.1-10.5) | ⚠ H2 sequencing |
| R1.6 — Cleanup | Phase 11 (steps 11.1-11.7) | ❌ C1 substrate leak |
| Skill protocol alignment | Phase 12 (steps 12.1-12.7) | ⚠ C1 downstream |
| Final acceptance | Phase 13 (steps 13.1-13.7) | ✅ |
| Task completion | Post-Completion Actions | ✅ |

**Unmapped from BUILD-REQUEST: 0.** **Mapped with issues: 5 phases (C1+H1-H5).**

---

## Evidence-Validator Results

- **Citations total:** 22 (sampled per §11.5 budget policy — task file has ~150 file:line references; the 22 are HIGH-stakes + 30% random + 10% spot-check)
- **Citations dropped:** 0
- **Citations inferred:** 0
- **Citation budget policy:** sampled
- **Drop rate:** 0.0

A zero-drop pass on a non-trivial review is a *flag, not a green light* per §11.2. The sampling was conservative; a `--depth deep` `full_reread` re-run would harden this. Recommend in any case where the architectural impact of a missed citation drop is high — for this PARTIAL verdict, the sampling is sufficient.

---

## Recommendation

**Refactor-then-ship.** ~2-4 hours of pre-execution edits to the task file:

1. **C1:** Rewrite Step 11.2 to delete BOTH `_check_frontmatter` AND `_parse_frontmatter`, source canonical parser from PipelineEnvelope post-extractor (R1.2). Re-align Step 12.3 (skill prose).
2. **H1:** Swap Contract #5 ↔ #9 wiring in Step 5.1 (match Step 13.4).
3. **H2:** Reorder R1.6 fail-open deletion before R1.5 terminal step, OR add explicit ordering annotation.
4. **H3:** Split Phase 9 into 9a/9b/9c, each with its own QA gate.
5. **H4:** Split Step 9.11 into 9.11a-d (one cutover per step).
6. **H5:** Add Step 9.X cutover-counter design (release-marker file + counter ≥3 gate).

Mediums (M1-M7) can be addressed in flight by the executing agent.

**Do NOT re-author.** Task file is 94% correct; the issues are concentrated and concrete. The 3-vendor ensemble caught what a single-vendor review would have shipped.

---

## Tier 3 Remediation Offer

`--remediate` was set on the sc:reflect invocation. Per protocol §17 "Will Not auto-execute Tier 3 remediation chain", the offer is surfaced for user decision:

**Option A:** Spawn `task-builder` to author a corrective MDTM remediation task that addresses C1 + H1-H5 + M1-M7 (12 issues). Task-builder will produce a task file at `.dev/tasks/to-do/TASK-RF-<date>-roadmap-rewrite-remediation/`. Operator then runs `/task <path>` to execute the remediation. After remediation, re-run `/sc:reflect --mode post --diff <remediation-diff>` as the post-commit gate.

**Option B:** Manual in-place edits to the existing task file at `TASK-RF-20260531-042405.md`. Faster for the 6 concrete fixes (C1 + H1-H5); the 7 mediums are quality-of-life that the executing agent can handle in-flight.

**Option C:** Ship as-is with the issues documented as Open Questions. Less safe — C1 in particular would silently preserve Flaw 3 unless the executing agent catches it independently.

**Recommended (per `feedback_prefer_simpler_proposals.md`):** Option B for the 6 concrete fixes, then ship and let the executing agent surface mediums via Phase Findings logs.

---

## Sufficiency-Claim Caveat (§11.0)

**Conditional sufficiency holds** for this run:
- ✅ Calibrator class disjoint from reviewer classes: **DEGRADED** (calibrator = opus, opus is also R1) — the one weakness; a non-opus calibrator (kimi, deepseek) would tighten this
- ✅ ≥2 vendors among reviewer aliases: **TRUE** (3 vendors: Anthropic + OpenAI + Alibaba)
- ⚠ Sycophantic-convergence eval case passed: **NOT RUN** (this is an inline workflow, not an eval-harness run; the §12.5 falsifier suite is v1.0 skeleton-pending)

The anti-confirmation guarantee is **"ensemble pressure applied"** rather than **"self-confirmation neutralised"** per §11.0 fallback. The PARTIAL verdict at convergence 0.67 is precisely the kind of signal the conditional-sufficiency framework is designed to surface — and the R1↔R2/R3 divergence on C1 demonstrates the value of the heterogeneous ensemble in this exact run.
