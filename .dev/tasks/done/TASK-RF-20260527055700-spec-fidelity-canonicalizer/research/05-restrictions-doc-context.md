# Documentation Context Card

Wave 1.5 output. Loaded by Wave 1.7, Wave 3, Wave 4, Wave 5.

## Release context

- **Release**: v3.05_DeterministicFidelityGates + v3.0_unified-audit-gating + roadmap-spec-fidelity-fix (backlog)
- **Artifacts**:
  - `/config/workspace/IronClaude/.dev/releases/complete/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md`,
  - `/config/workspace/IronClaude/.dev/releases/complete/v3.05_DeterministicFidelityGates/architecture-design.md`,
  - `/config/workspace/IronClaude/.dev/releases/complete/v3.0_unified-audit-gating/adversarial-design-review/fidelity-investigation/adversarial/debate-transcript.md`,
  - `/config/workspace/IronClaude/.dev/releases/backlog/roadmap-spec-fidelity-fix/RANKING.md`,
  - `/config/workspace/IronClaude/.dev/releases/backlog/roadmap-spec-fidelity-fix/adversarial/merged-solution.md`,
  - `/config/workspace/IronClaude/.dev/troubleshoot/spec-fidelity-deep-dive-20260527045400/historical-context.md`
- **Summary**: v3.05 introduced the 3-run convergence engine (FR-7), DeviationRegistry (FR-6/FR-10), and the 30% diff-size guard. Architecture spec assigns module responsibilities (structural_checkers.py = "5 checkers + severity rule tables") but specifies NO contract for spec↔roadmap ID reconciliation semantics. The most recent shipped remediation (S1+S2+S5, merged 2026-05-15) addressed a *prior* failure shape (10 HIGHs, `files_affected=[]`, parser noise) but did not add a phantom_id-specific fix-guidance template and did not normalize ID comparison. The v3.0 fidelity-investigation adversarial debate (`debate-transcript.md:127`) recorded the explicit consensus that **no shipped remediation has ever touched the spec-fidelity comparator itself** — only surrounding machinery.
- **Confidence**: 0.95

## Architectural docs consulted

- `/config/workspace/IronClaude/src/superclaude/skills/sc-roadmap-protocol/SKILL.md` — verdict: `current` — documents CLI step crosswalk including `spec-fidelity`, cosmetic-remediation lanes, and inference-only thresholds. Does NOT specify spec↔roadmap ID-normalization or MANUAL_TRIAGE escape policy.
- `/config/workspace/IronClaude/docs/generated/contributor-knowledge-base/architecture-guide.md` — verdict: `current` — four-layer contributor view; no spec-fidelity gate semantics.
- `/config/workspace/IronClaude/KNOWLEDGE.md` — verdict: `current` — most-recent entry (2026-05-25, "Fix B Merged — Anti-Instinct Gate Mechanism-Signature Refactor") establishes `_canonicalize_identifiers` in integration_contracts.py:445 as a project-level precedent for collapsing semantically-identical IDs. Direct precedent for the canonicalization pattern that the structural_checkers.py phantom_id comparator lacks.
- `/config/workspace/IronClaude/.dev/releases/complete/v3.05_DeterministicFidelityGates/architecture-design.md` — verdict: `current` — modules table at lines 27-33 is the authoritative module-responsibility contract; does not specify ID reconciliation semantics.

## Restrictions / decisions that constrain the fix

1. **Module ownership**: per `architecture-design.md:27-33`, `structural_checkers.py` owns the 5 checkers + severity rule tables (FR-1, FR-3). Any comparator change belongs HERE, not in `spec_parser.py` (which owns extraction, FR-2/FR-5) and not in `convergence.py` (which owns the 3-run budget loop, FR-7/FR-8).
2. **Pure-function contract**: per `bf4-final.md` and the deterministic-fidelity-gate-requirements.md, structural checkers are pure functions over `SpecData`/`RoadmapData` frozen dataclasses with zero shared mutable state (NFR-4). Any canonicalization must be a pure transformation, not stateful.
3. **30% diff guard is per-patch** (`remediate_executor.py:309-362`). A schema-migration-sized fix that touches all 54 roadmap rows would be rejected by default. The escape valve `--allow-regeneration` exists but is the BACKUP-WORKAROUND, not the default.
4. **Pass condition is strictly binary**: `active_highs == 0` (`convergence.py:539`). No allowlist, no MANUAL_TRIAGE bucket, no per-rule_id soft-pass. S6 (MANUAL_TRIAGE halt from backlog) was *deferred*, not merged.
5. **Spec is an input the agent cannot modify**: this is the long-standing remediation contract (referenced repeatedly across release docs and the S2 design — "additive edits to the roadmap, never the spec"). Any fix that requires editing the spec is out-of-scope for the in-loop remediation agent.
6. **`max_runs=3` is the default**, hard-coded in `convergence.py:440`. The executor passes 3. No flag promotes it to a runtime knob in convergence mode (per the BACKUP-WORKAROUND escape path's specific phrasing).
7. **Precedent for canonicalization exists locally** (`integration_contracts.py:445`, `KNOWLEDGE.md:156-205`). Extending it to `structural_checkers.py` is consistent with project pattern.

## Re-frame signals

1. **The Phase 0 history is unanimous: no shipped fix has touched the comparator.** The current S1/S2/S5 remediation lineage hardens the orchestration around `phantom_ids = roadmap_ids - spec_ids` but does not touch the comparison itself. The TUIBBS failure exposes the unaddressed core.
2. **The failure shape has shifted again** (now: schema-mismatch IDs; was: parser noise + files_affected=[]). This corroborates Pattern 2 from historical-context.md ("every prior failure shape has been distinct"). A surgical phantom_id fix without a structural escape (S6) leaves the next distinct failure shape unguarded.
3. **The chosen remediation surface is structural_checkers.py** (per restriction 1) — not the convergence engine, not the parser, not the remediation executor. A canonicalization step inside `check_signatures` is the minimum-change path that aligns with module ownership.
