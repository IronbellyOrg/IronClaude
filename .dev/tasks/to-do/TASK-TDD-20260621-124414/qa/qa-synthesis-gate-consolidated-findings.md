# Synthesis-Gate Consolidated Findings

**Date:** 2026-06-21 | **Phase:** 5G synthesis gate | **Tier:** Heavyweight
**Source reports (5):** analyst-synthesis-gate-A (FAIL, 6 issues), analyst-synthesis-gate-B (PASS, 4 advisory),
qa-synthesis-gate-structure (PASS, 4 handoff), qa-synthesis-gate-content (PASS + 1 IMPORTANT), qa-synthesis-gate-coherence (PASS, 6 minor).

## Consolidated Verdict: FAIL → fix cycle 1

Four of five lenses PASS on substance; ~60 sampled citations independently re-verified exact. The FAIL is
driven by analyst-A's accuracy findings plus the content/coherence lenses' converging FR-006 concern. All
issues are surgically fixable in the synth files. The §27/§28 population and §5.3 numbering re-letter are
ASSEMBLER-handoff items (not synth fixes) — recorded separately for Phase 6.

## Synth-fix issues (apply in 5G.8)

| ID | Severity | Affected synth file(s) | Issue | Required fix | Lens(es) |
|----|----------|------------------------|-------|--------------|----------|
| S-1 | HIGH | synth-01 §4.1, synth-02 (FR-008 table), synth-05 §11.2 | Eval-case tables claim "5 cases (37–41)" but render only **4 rows** — case 37 (`unwired-surface-passes`) and case 41 (`test-only-ref`) collapsed into one. They are distinct fixtures (research/04); case 41 is the count-invariant host. | Split into 5 distinct rows in all three tables: 37 unwired-surface-passes, 38 positive-control, 39 dynamic-dispatch, 40 degraded-backend, 41 test-only-ref. | analyst-A |
| S-2 | HIGH | synth-01 §2.2 | Over-attributes the forbid-list: claims all three observed improvised names (`runtime_surface_reachable`, `surface_reachability_verdict`, `surface_production_reachable`) were the explicitly-forbidden set, but research/03 §1.1 lists a different explicitly-forbidden set. | Correct §2.2 to state the OBSERVED ad-hoc names (from spec §0 / research/00) separately from the SKILL's explicitly-forbidden examples; do not conflate. | analyst-A |
| S-3 | IMPORTANT | synth-02 (FR-006), synth-03 §6.3, synth-09 §23 (Phase 2 exit criterion) | FR-006 lists the **sprint executor reading deterministic scalars** as Must-Have with AC-4, and §6.3 phrases it as a live reader ("MUST consume"), but `cli/sprint/executor.py` reads no reflect contract today (research/03, SPEC-ONLY) and no rollout phase wires it. Contradicts synth-02 G2 / synth-04 SPEC-ONLY tag. | Split FR-006: the §5.3 forbid-STOP pre-filter read = in-scope Must-Have (it executes in-skill today); the sprint-executor read = DEFERRED/Non-Goal-for-v1 (explicitly note it is net-new and not delivered by this rollout). Align §6.3 wording to SPEC-ONLY/deferred. Fix synth-09 Phase 2 exit criterion to not claim sprint reads the scalars. | analyst-A (M3), content (IMPORTANT), coherence (#6) |
| S-4 | MEDIUM | synth-05 §11.1 | Exit-code mapping (`pass=0/halted=10/degraded=11/blocked=2`) asserted but uncited within the partition; cross-ref owner (§6) never defines it — dangling reference. | Cite the source (research/03 / models.py `Verdict` enum + exit-code mapping) inline, OR remove the dangling "see §6" cross-ref and self-contain it. | analyst-A, coherence (#1) |
| S-5 | MEDIUM | synth-03 §6.2 (mermaid) | Diagram labels `commands.py:254` as `reflect_group.run()`, but research/02 pins that line to `ReflectRunner(config).run()`. | Correct the symbol label to match research/02 (`ReflectRunner(config).run()` / `_audit_once` chokepoint). | analyst-A |
| S-6 | MINOR | synth-05, synth-03 (+others) | Orchestrator entry function named two ways across files (`run_runtime_surface_sweep` vs `run_sweep`). | Standardize to ONE name (use `run_sweep`) across all synth files for §8/§11/§15 consistency. | coherence (#2) |

## Assembler-handoff items (NOT synth fixes — for Phase 6 assembly)

| ID | Note |
|----|------|
| A-1 | §27 References and §28 Glossary are not produced in any synth file — the rf-assembler MUST populate them (structure lens O-3). |
| A-2 | synth-02's author-introduced `§5.3 PRD Trace` heading collides numerically with the SKILL's separate `§5.3 pre-filter` — re-letter/relabel on assembly to avoid confusion (structure O-1). |
| A-3 | The stale `ensemble.REFLECT_CONTRACT_VERSION="1.0"` vs SKILL 1.6.0 reconciliation is already surfaced in synth-04 §8.3 / synth-02 G3 / synth-08 §19.2 — ensure it lands in the assembled §19 + §22, not dropped. |
| A-4 | Add a one-line bridge at first co-occurrence of "7-step algorithm" vs "6 logical units" (coherence #4) — the 7 steps map to 6 units (tag+find+partition+oracle+rootwalk+reduce/emit). |

## Substance note
No fabrication, no coverage gap, no hallucinated path found across the 5 lenses. The synth corpus is sound;
the FAIL is accuracy/consistency polish (S-1..S-6). Apply S-1..S-6 in 5G.8; carry A-1..A-4 to the assembler.
