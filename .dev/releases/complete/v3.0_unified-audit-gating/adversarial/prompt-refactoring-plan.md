---
title: Prompt Refactoring Plan — Synthesis of 6 Adversarial Debates
date: 2026-03-19
status: ready-for-execution
total_findings: 31 (18 converged, 6 contested, 7 cross-cutting)
---

# Prompt Refactoring Plan

## Cross-Cutting Findings (affect multiple prompts)

| ID | Finding | Affected Prompts | Severity |
|----|---------|-----------------|----------|
| X-1 | Pipeline has 12 steps, not 13. deviation-analysis is not a discrete pipeline Step — it runs inside validate_executor, not through _build_steps()/roadmap_run_step() | P1, P2, P5, P6 | HIGH |
| X-2 | remediate/certify are conditional — they only run if spec-fidelity FAILS. Without guaranteed failures, 3 of 5 new v3.0 stages are untested | P1, P2 | HIGH |
| X-3 | No precondition checks between prompts — P2 assumes eval-spec.md exists (from P1), P5 assumes eval designs exist (from P3), P6 assumes eval-runs exist (from P5) | P2, P4, P5, P6 | MEDIUM |
| X-4 | Scoring framework authority — P5 creates and adversarially reviews the framework, but P6 partially overrides it with hardcoded formulas | P5, P6 | HIGH |
| X-5 | "Build" gap — P3 designs evals but never produces executable scripts. P5 assumes scripts exist or runs raw pipeline instead | P3, P5 | MEDIUM |

## Per-Prompt Refactoring Tasks

### Prompt 1: Spec Generation (Score: 6.5/10 → target 8.5/10)

| # | Task | Source | Priority |
|---|------|--------|----------|
| P1-1 | Tag intentional ambiguities with `<!-- EVAL-SEEDED-AMBIGUITY -->` and instruct spec-panel to preserve them | Debate 1 §2 | CRITICAL |
| P1-2 | Add `spec_type: new_feature` explicitly | Debate 1 §3 | CRITICAL |
| P1-3 | Add eval-fitness context to spec-panel invocation: "This spec is an eval harness. Preserve EVAL-SEEDED-AMBIGUITY tags." | Debate 1 §2 | CRITICAL |
| P1-4 | Replace "all 13 stages" with "all 12 pipeline steps + deviation-analysis logical phase" | X-1 | HIGH |
| P1-5 | Require ambiguities to produce BLOCKING/WARNING findings, not INFO | Debate 1 §4, X-2 | HIGH |
| P1-6 | Provide explicit file paths: executor.py, commands.py, gates.py, main.py | Debate 1 §5 | IMPORTANT |
| P1-7 | Add dry-run smoke test after sentinel check | Debate 1 §6 | NICE |

### Prompt 2: Per-Stage Adversarial Review (Score: ~6/10 → target 8/10)

| # | Task | Source | Priority |
|---|------|--------|----------|
| P2-1 | Reduce from 13 to 12 agents. Fold deviation-analysis into spec-fidelity agent's scope or note its distinct architecture | X-1, Debate 2 §4 | CRITICAL |
| P2-2 | Embed `/sc:adversarial --depth quick` literally in each agent's prompt block, not just as top-level instruction | Debate 2 §2 | CRITICAL |
| P2-3 | Add bridging question: "How does v3.0's change to this stage alter what the eval spec must exercise?" | Debate 2 §1 | HIGH |
| P2-4 | Add gate-reading instruction: "Read your gate's SemanticCheck functions from gates.py before debating" | Debate 2 §6 | HIGH |
| P2-5 | Add precondition: verify eval-spec.md exists before spawning | X-3, Debate 2 §6 | HIGH |
| P2-6 | Differentiate v3.0-changed vs unchanged stages with distinct debate expectations | Debate 2 §6 | IMPORTANT |
| P2-7 | Provide master diff context or instruct agents to generate git diff | Debate 2 §6 | IMPORTANT |

### Prompt 3: Impact Analysis + Eval Design (Score: ~7/10 → target 8.5/10)

| # | Task | Source | Priority |
|---|------|--------|----------|
| P3-1 | Restore distinct "3 issues it mitigates" deliverable separate from "3 impacts" — problem-framing alongside solution-framing | Debate 3 §2 | HIGH |
| P3-2 | Address build gap: add requirement that /sc:design output includes complete pseudocode sufficient for direct implementation | X-5, Debate 3 §4 | HIGH |
| P3-3 | Add specificity constraint to /sc:analyze: "Each impact must cite specific function names, file paths, and line numbers" | Debate 3 §6 | HIGH |
| P3-4 | Add intermediate checkpoint between analyze and brainstorm: verify each impact has concrete code reference | Debate 3 §6 | IMPORTANT |
| P3-5 | Add eval-spec.md as additional @ reference to /sc:reflect | Debate 3 §5 | IMPORTANT |

### Prompt 4: Eval Validation Gate (Score: ~6.5/10 → target 9/10)

| # | Task | Source | Priority |
|---|------|--------|----------|
| P4-1 | Add Criterion 7: ARTIFACT PROVENANCE — artifacts must be in clean dir, timestamps post-date eval start | Debate 4 §4 | CRITICAL |
| P4-2 | Add blocking gate: "If criteria 1, 2, 3, or 7 FAIL → BLOCKED. Do not proceed to Prompt 5." | Debate 4 §5 | CRITICAL |
| P4-3 | Add severity tiering: criteria 1-3,7 are CRITICAL; criteria 4-6 are REQUIRED | Debate 4 §5 | HIGH |
| P4-4 | Add Criterion 8: EXECUTION PATH — trace main() to confirm pipeline invocation is reachable | Debate 4 §3 | IMPORTANT |
| P4-5 | Strengthen Criterion 6: timing alone is insufficient; require at least one quality metric | Debate 4 §6 | IMPORTANT |

### Prompt 5: Parallel Execution + Scoring (Score: ~7/10 → target 8.5/10)

| # | Task | Source | Priority |
|---|------|--------|----------|
| P5-1 | Specify distinct worktree paths: global-A uses `../IronClaude-eval-global-A`, global-B uses `../IronClaude-eval-global-B` | Debate 5 §6 | CRITICAL |
| P5-2 | Add partial-failure policy: "Minimum 1 local + 1 global required to proceed. Report any failed runs." | Debate 5 §6 | HIGH |
| P5-3 | Add eval-spec.md and convergence.py to adversarial agent context | Debate 5 §4 | HIGH |
| P5-4 | Reorder scoring framework requirements: lead with delta-focused requirements, make per-stage metrics supporting | Debate 5 §3 | IMPORTANT |
| P5-5 | Add note about expected global failures: master lacks 5 stages, score as "not available" not "failed" | Debate 5 §9 | IMPORTANT |
| P5-6 | Clarify eval target: reference P3 eval scripts if they exist, otherwise justify raw pipeline run | Debate 5 §2 | IMPORTANT |

### Prompt 6: Scoring + Proposals (Score: 7.5/10 → target 9/10)

| # | Task | Source | Priority |
|---|------|--------|----------|
| P6-1 | Rewrite Step 2 to defer to scoring framework methodology instead of prescribing "Local avg vs Global avg = delta" | X-4, Debate 6 F1 | CRITICAL |
| P6-2 | Replace hardcoded thresholds (80% reproducibility, any negative delta) with references to scoring-framework.md | X-4, Debate 6 F2 | HIGH |
| P6-3 | Expand code proposal scope from 2 directories to "superclaude package, particularly cli/roadmap/ and cli/audit/" | Debate 6 F3 | HIGH |
| P6-4 | Add Step 0: precondition validation — verify eval-runs dirs and scoring-framework.md exist | X-3, Debate 6 F4 | HIGH |
| P6-5 | Add required report sections: errors/partial failures, wall-clock timing | Debate 6 F5 | IMPORTANT |
| P6-6 | Strengthen happy-path to cite specific evidence (delta values, reproducibility %) | Debate 6 F6 | NICE |

## Execution Order

All tasks applied to eval-prompts.md in a single edit pass, ordered by prompt number.
Total: 31 tasks (8 CRITICAL, 12 HIGH, 9 IMPORTANT, 2 NICE).
