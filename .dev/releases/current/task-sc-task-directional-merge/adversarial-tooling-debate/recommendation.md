<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (sc:tasklist) — selected per adversarial/base-selection.md -->
<!-- Merge date: 2026-05-17T02:56:00+00:00 -->
<!-- Source: Adapted merge — strategic recommendation, not artifact merge -->

# Recommendation — Tasklist Generation Tool for `docs/docs-product/tech/task-merge/roadmap.md`

## Verdict

<!-- Source: Adversarial scoring (base-selection.md) -->
**Use `/sc:tasklist`** for the current roadmap. Combined score 0.902 vs `/task-builder` 0.871; debate decided 16-6 across 25 diff points (88% convergence, exceeds 80% threshold).

## Why `/sc:tasklist` Wins for This Specific Roadmap

<!-- Source: Variant A (sc:tasklist), debate Round 1 strengths #1-5, refined by Round 2 rebuttals -->

1. **The roadmap *is* the deterministic input the skill was built to transform.** It has just passed `extract → generate → debate → score → merge → anti-instinct (57/57 contracts covered) → test-strategy → spec-fidelity → wiring-verification → deviation-analysis → remediate → certify` and the validator reports `tasklist_ready: true`. The pipeline contract reads exactly: roadmap → tasklist → sprint-CLI → /sc:task. `/sc:tasklist` is the load-bearing step here.

2. **Compliance-tier integration is load-bearing.** Every task gets STRICT/STANDARD/LIGHT/EXEMPT classified at generation time with verification routing per tier (skill spec Section 4.10). This is what `/sc:task` consumes downstream. `/task-builder` produces MDTM tasks with no tier field; the executor would have no per-task compliance signal.

3. **Sprint-CLI orchestration requires the multi-file bundle.** `phase-N-tasklist.md` naming is a regex-discovery contract with `superclaude sprint run`. A single MDTM file from `/task-builder` cannot be sprint-orchestrated — it would have to execute monolithically via `/task`, surrendering phase-level checkpoints.

4. **Atomicity bindings (ME-6/S-2/S-3) demand compound-row preservation.** The roadmap's validator already documented 25+ compound deliverables as intentional atomic-by-design clusters. `/sc:tasklist`'s deterministic transform preserves them. `/task-builder`'s parallel-researcher pattern would naturally decompose compound rows into "independently testable" items — which is exactly the violation the validator flagged as `[WARNING] Decomposition` and which the invariant probe (INV-007, HIGH severity) identified as the dominant fault mode.

5. **Determinism matters at 132 tasks.** Two engineers running `/sc:tasklist` on this roadmap get byte-identical output. `/task-builder`'s parallel-research design cannot promise this — different agent samples produce different research summaries, which produce different task files.

## Why Not `/task-builder` Here (Despite Its Real Strengths)

<!-- Source: Variant B (task-builder), debate Round 1 + Variant A rebuttals -->

`/task-builder` is genuinely the better tool when:
- Input is a vague free-form request, not a validated roadmap.
- Codebase-fidelity is the binding constraint (will the proposed work touch real files at real paths?).
- The work decomposes into independent multi-track deliverables.
- External-standard documentation lookups are required.

None of those conditions describe the current roadmap. The upstream pipeline already verified spec-fidelity, contract coverage, and wiring. Re-doing that work via `/task-builder`'s rf-analyst + rf-qa + rf-qa-qualitative gates would duplicate ~30 minutes of pipeline work and produce output the Sprint CLI cannot consume.

## How to Invoke

<!-- Source: Variant A spec, line 11 of /sc:tasklist command file -->
```
/sc:tasklist docs/docs-product/tech/task-merge/roadmap.md
```

- `TASKLIST_ROOT` will auto-derive to `.dev/releases/current/task-sc-task-directional-merge/` (verified by grep of the roadmap content — first match of `.dev/releases/current/<segment>/`).
- `.roadmap-state.json` will auto-wire `tdd_file` and `prd_file` for TDD/PRD enrichment (verified in current state-file inspection).
- Post-generation validator runs automatically; expect `tasklist_ready: true` if the upstream roadmap passes through cleanly.

## What to Watch For After Generation

<!-- Source: Variant A spec Section 5.1 + validation-report.md WARNINGs from prior turn -->

The roadmap carries 3 non-blocking WARNINGs that the tasklist will inherit:
1. **NFR-ME-5/-7/-8 absent** — authorized by extraction as "HELD-no-deltas." Tasklist will reflect this. No action required.
2. **M5 test concentration** — structural to AC-SM audit semantics. Tasklist will reflect this. No action required.
3. **25+ compound deliverables joined by `+`** — atomic-by-design under ME-6/S-2/S-3 bindings. `/sc:tasklist` should preserve these via deterministic clause-splitting rule (skill spec Section 4.4: "Split into multiple tasks **only** if the item contains two or more independently deliverable outputs"). Compound rows annotated as ME-6/S-2/S-3-atomic should NOT split.

If the generated tasklist incorrectly splits an atomicity-bound compound row, the post-generation `superclaude tasklist validate` should catch it as a fidelity drift and auto-patch. If auto-patch fails on this, that's a real bug in the splitter — not a reason to fall back to `/task-builder`.

## Reserved for Future Use

<!-- Source: Variant B (task-builder) strengths, refactor-plan.md Decision #2 -->

`/task-builder` is the right tool when the next request is something like:
- "Build a task to refactor X" (no roadmap)
- "Build a task to document Y" (no upstream validation)
- "Create a task file for the auth middleware compliance work" (codebase-verification critical)

Reaching for it for *this* roadmap would discard the entire validate-roadmap → /sc:tasklist → sprint-CLI pipeline the project's own CLAUDE.md describes.

---

## Return Contract

```yaml
return_contract:
  merged_output_path: ".dev/releases/current/task-sc-task-directional-merge/adversarial-tooling-debate/recommendation.md"
  convergence_score: 0.88
  artifacts_dir: ".dev/releases/current/task-sc-task-directional-merge/adversarial-tooling-debate/adversarial/"
  status: "success"
  base_variant: "sc:tasklist"
  unresolved_conflicts: 0
  fallback_mode: false
  failure_stage: null
  invocation_method: "skill-direct"
  unaddressed_invariants:
    - id: "INV-007"
      category: "interaction_effects"
      assumption: "task-builder's researcher pattern decomposes atomic-by-design compound rows, violating ME-6/S-2/S-3"
      severity: "HIGH"
      note: "Asymmetric — disqualifies Variant B for the current scenario; not a defect of Variant A. Recorded for transparency."
```
