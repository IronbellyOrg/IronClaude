# TurnLedger Integration — Parallel Refactoring Prompt

## Objective

3 agents independently analyze each spec+design pair and produce a refactoring proposal. Their proposals are then consolidated via `sc:adversarial --compare` to cover the ~20-30% each agent misses individually.

---

## Phase 1: Parallel Agent Execution (9 agents — 3 per version)

Run 3 agents per version simultaneously. Each agent receives the **same prompt** for its version — natural variance in reasoning produces distinct proposals.

### v3.05 — Deterministic Fidelity Gates

> Run this prompt 3 times in parallel sessions. Change `AGENT_ID` to `A`, `B`, `C`.

```
/sc:improve @.dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md \
  --type maintainability --interactive

CONTEXT:
- Authoritative spec: .dev/releases/current/v3.05_DeterministicFidelityGates/deterministic-fidelity-gate-requirements.md
- TurnLedger addendum: .dev/releases/current/turnledger-integration/v3.05/design.md
- The addendum answers: "How should FR-7/8/9 consume TurnLedger instead of building a parallel budget/remediation system?"

TASK:
1. Read BOTH files completely.
2. Identify every place the design.md proposes TurnLedger consumption that replaces, modifies, or supplements existing requirements.
3. Produce a REFACTORING PLAN (do NOT modify the original spec).

OUTPUT FILE:
  .dev/releases/current/v3.05_DeterministicFidelityGates/turnledger-refactor-proposal-{AGENT_ID}.md

REQUIRED SECTIONS IN THE PROPOSAL:
- **Diff Summary**: Section-by-section — what changes, what stays, what's new.
- **Affected Requirements**: Exact requirement IDs with before/after text.
- **New Requirements**: Requirements introduced by TurnLedger integration.
- **Conflicts**: Risks or contradictions between the original spec and the design addendum.
- **Resolutions**: Recommended resolution for each conflict.
```

---

### v3.1 — Anti-Instincts Gate

> Run this prompt 3 times in parallel sessions. Change `AGENT_ID` to `A`, `B`, `C`.

```
/sc:improve @.dev/releases/backlog/v3.1_Anti-instincts__/anti-instincts-gate-unified.md \
  --type maintainability --interactive

CONTEXT:
- Authoritative spec: .dev/releases/backlog/v3.1_Anti-instincts__/anti-instincts-gate-unified.md
- TurnLedger addendum: .dev/releases/current/turnledger-integration/v3.1/design.md
- The addendum answers: "How should the gate pipeline consume TurnLedger instead of building a parallel budget/remediation system?"

TASK:
1. Read BOTH files completely.
2. Identify every place the design.md proposes TurnLedger consumption that replaces, modifies, or supplements existing gate pipeline definitions.
3. Produce a REFACTORING PLAN (do NOT modify the original spec).

OUTPUT FILE:
  .dev/releases/backlog/v3.1_Anti-instincts__/turnledger-refactor-proposal-{AGENT_ID}.md

REQUIRED SECTIONS IN THE PROPOSAL:
- **Diff Summary**: Section-by-section — what changes, what stays, what's new.
- **Affected Sections**: Exact section/requirement IDs with before/after text.
- **New Sections**: Sections introduced by TurnLedger integration.
- **Conflicts**: Risks or contradictions between the original spec and the design addendum.
- **Resolutions**: Recommended resolution for each conflict.
```

---

### v3.2 — Wiring Verification Gate

> Run this prompt 3 times in parallel sessions. Change `AGENT_ID` to `A`, `B`, `C`.

```
/sc:improve @.dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md \
  --type maintainability --interactive

CONTEXT:
- Authoritative spec: .dev/releases/backlog/v3.2_fidelity-refactor___/wiring-verification-gate-v1.0-release-spec.md
- TurnLedger addendum: .dev/releases/current/turnledger-integration/v3.2/design.md
- The addendum answers: "How should the wiring hook consume TurnLedger instead of building a parallel budget/remediation system?"

TASK:
1. Read BOTH files completely.
2. Identify every place the design.md proposes TurnLedger consumption that replaces, modifies, or supplements existing wiring hook definitions.
3. Produce a REFACTORING PLAN (do NOT modify the original spec).

OUTPUT FILE:
  .dev/releases/backlog/v3.2_fidelity-refactor___/turnledger-refactor-proposal-{AGENT_ID}.md

REQUIRED SECTIONS IN THE PROPOSAL:
- **Diff Summary**: Section-by-section — what changes, what stays, what's new.
- **Affected Sections**: Exact section/requirement IDs with before/after text.
- **New Sections**: Sections introduced by TurnLedger integration.
- **Conflicts**: Risks or contradictions between the original spec and the design addendum.
- **Resolutions**: Recommended resolution for each conflict.
```

---

## Phase 2: Adversarial Consolidation (3 compares — 1 per version)

After all Phase 1 agents complete, run one `sc:adversarial --compare` per version. These 3 can run in parallel.

### v3.05
```
/sc:adversarial --compare \
  .dev/releases/current/v3.05_DeterministicFidelityGates/turnledger-refactor-proposal-A.md,\
  .dev/releases/current/v3.05_DeterministicFidelityGates/turnledger-refactor-proposal-B.md,\
  .dev/releases/current/v3.05_DeterministicFidelityGates/turnledger-refactor-proposal-C.md \
  --depth deep --convergence 0.85 \
  --output .dev/releases/current/v3.05_DeterministicFidelityGates/adversarial/
```

### v3.1
```
/sc:adversarial --compare \
  .dev/releases/backlog/v3.1_Anti-instincts__/turnledger-refactor-proposal-A.md,\
  .dev/releases/backlog/v3.1_Anti-instincts__/turnledger-refactor-proposal-B.md,\
  .dev/releases/backlog/v3.1_Anti-instincts__/turnledger-refactor-proposal-C.md \
  --depth deep --convergence 0.85 \
  --output .dev/releases/backlog/v3.1_Anti-instincts__/adversarial/
```

### v3.2
```
/sc:adversarial --compare \
  .dev/releases/backlog/v3.2_fidelity-refactor___/turnledger-refactor-proposal-A.md,\
  .dev/releases/backlog/v3.2_fidelity-refactor___/turnledger-refactor-proposal-B.md,\
  .dev/releases/backlog/v3.2_fidelity-refactor___/turnledger-refactor-proposal-C.md \
  --depth deep --convergence 0.85 \
  --output .dev/releases/backlog/v3.2_fidelity-refactor___/adversarial/
```

---

## Phase 3 (Optional): Validation

Run `sc:spec-panel` on each merged proposal to validate correctness before applying.

```
/sc:spec-panel @.dev/releases/current/v3.05_DeterministicFidelityGates/adversarial/merged-output.md \
  --mode critique --focus correctness

/sc:spec-panel @.dev/releases/backlog/v3.1_Anti-instincts__/adversarial/merged-output.md \
  --mode critique --focus correctness

/sc:spec-panel @.dev/releases/backlog/v3.2_fidelity-refactor___/adversarial/merged-output.md \
  --mode critique --focus correctness
```

---

## Execution Summary

| Phase | What | Agents | Parallelism | Outputs |
|-------|------|--------|-------------|---------|
| 1 | `/sc:improve` per pair | 9 (3×3) | 3 parallel per version | 9 refactoring proposals |
| 2 | `/sc:adversarial --compare` | 3 (1 per version) | All 3 in parallel | 3 merged proposals |
| 3 | `/sc:spec-panel --focus correctness` | 3 (1 per merged) | All 3 in parallel | 3 validation reports |
