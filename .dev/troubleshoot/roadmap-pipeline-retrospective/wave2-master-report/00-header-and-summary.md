# Roadmap Pipeline Retrospective — Master Report

**Generated:** 2026-05-31
**Source:** 14 partition retrospectives synthesizing 64 releases (`.dev/releases/complete/`) + 77 tasks (`.dev/tasks/done/`)
**Wave-1 totals:** 262 findings — 159 failures, 61 remediations, 51 successes, 113 brittleness drivers identified
**Driver question:** *What recurring failures in the roadmap pipeline reveal architectural flaws so deep that targeted patches will keep losing — and what would a ground-up rewrite or refactor have to look like to make the brittleness go away permanently?*

---

## Executive Summary

The retrospective produces one architectural conclusion that the evidence chain forces: **the roadmap pipeline is brittle by substrate, not by bug**. Five deep structural flaws (Section 6) account for the overwhelming majority of failures across 9 release generations, and four of the five are classified INHERENT — they cannot be fixed without changing the pipeline's interchange primitives. The pipeline has grown monotonically from 9 steps (v4) → 11 (v2.22) → 13 (v5) → 14 (current) because each new failure class triggers a new validator rather than a constraint on the generator that produced it. The validator/generator asymmetry (Flaw 2) guarantees the next failure shape will arrive faster than the next validator can be authored, which is the operational signature of substrate-level brittleness.

**The three most-confident recurrence patterns** (Section 4) carry this thesis on their own:

1. **Spec-fidelity gate (~12 fix attempts across 8 partitions, A1a→A12).** Every redesign — LLM-only → 5-vote consensus → deterministic structural checkers → convergence engine → DeviationRegistry → canonicalizing comparator — closed the *previous* failure shape by adding machinery *around* the comparator. (A12:F-A12-03) names this the "multi-release harden-orchestration-around-broken-comparator" anti-pattern explicitly.

2. **"Written but not wired" (~8 attempts, A2b→A12).** Every release ships infrastructure (`TurnLedger`, `_resolve_wiring_mode()`, `build_certify_step()`, `tasklist generate` CLI subcommand, `_format_wiring_failure()`) that production entry points never reach. The pipeline has no terminal verification link from Tasklist → Code; spec-fidelity validates *roadmap-against-spec*, never *implementation-against-spec*.

3. **Roadmap fabricates / renumbers identifiers (~7 attempts, A1b→A12).** Roadmaps invent FR/NFR/SC/D-### identifiers absent from the spec on every release with >5 requirements, because the LLM's tabular-formatting bias produces IDs to fill columns and no gate enforces "every roadmap ID ∈ spec ID set ∪ accepted deviations". Each fix is per-instance; none install a bidirectional registry.

**Decision verdict — REWRITE.** Four of five flaws are INHERENT (Flaws 1, 2, 3, 5 in whole; Flaw 4's silent-skip half), and three of those four scope to *cross-cutting state* — the artifact-centric gate model (Flaw 1), markdown-frontmatter state (Flaw 3), and the missing contract-schema layer (Flaw 5) — none of which are subsystem boundaries that can be replaced independently. A REWRITE should preserve the working mechanisms (adversarial debate per Section 4's #18 RESOLVED-FOR-NOW pattern, the v3.05 deterministic structural-checker layer) but invert the substrate: typed cross-step state (sidecar JSON + dataclass), tool-write structured-output enforcement at every LLM step, a code-reaching terminal fidelity link (Tasklist → AST), and a central contract registry with bidirectional drift detection in CI.

The user's currently-blocking failure (anti-instinct halts on the MultiModelSwarm roadmap due to `stub`-as-component-name false positives at lines 207/211/213) is a *direct manifestation* of Flaw 2: a deterministic regex gate operating on LLM-generated text with no allowlist escape valve. Section 4 row #6 documents 4 prior remediations of this exact class. Per the verdict, patching this instance individually will *not* prevent the next.

---
