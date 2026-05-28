# Base Selection

## Note on this debate's mode

This is a **differences-only debate** (Focus: `differences`). The job is not to declare one design superior — it is to produce a comprehensive, ranked catalogue of divergences. "Base selection" here means: which advocate card supplies the best **framing and scaffolding** for the merged catalogue.

## Combined scoring

All three advocates produced internally consistent cards and converged on the substantive divergence set. Scoring is therefore about *scaffolding strength for the merged output*, not about which advocate "won."

| Advocate | Quant (structural completeness) | Qual (framing for merge) | Combined | Notes |
|----------|---------------------------------|--------------------------|----------|-------|
| Variant 1 — Architect | 0.85 | 0.85 | 0.85 | Strong on L3 (state-mechanics) divergences; explicitly identifies pairing of U-003 ↔ U-005; cluster framing introduced in Round 2 |
| Variant 2 — QE | 0.85 | 0.80 | 0.82 | Strong on evidence/test/falsifiability divergences; explicit on testability framing for U-005; reframes C-013 long-term impact |
| Variant 3 — Analyzer | 0.90 | 0.90 | 0.90 | Strongest *ranking* framing — Tier 1/2/3/4 by behavior-shaping impact; explicit cluster note; accepted as scaffolding by both other advocates in Round 2 |

## Selected Base: Variant 3 — Analyzer

Rationale:

- **Ranking framework is what the merged output needs.** A "comprehensive list of substantive divergences" with no ordering is not useful — the user explicitly asked for the top-10 to be ranked by significance. The Analyzer card is the only one that provides a full 4-tier ranking with named tiers (behavior-shaping, integration, infrastructure, instrumentation).
- **Cluster framing was introduced by the Analyzer and adopted by Architect in Round 2.** "C-004 + C-005 + C-015 + U-002 + U-003 are downstream of one design choice" is the most useful synthesis observation in the debate.
- **Steelman is balanced.** The Analyzer card steelmans both designs explicitly and refuses to declare a winner — exactly the differences-only stance the debate requires.

Runner-up Architect (0.85) supplies L3 invariant framing (U-003 ↔ U-005 pairing); incorporate into base.

QE (0.82) supplies evidence-rigor framing (schema-up-front vs validator-at-end); incorporate into base for the hallucination-contract entry.

## Eligibility floor check

This debate is about differences (not engineering quality), so the standard Invariant & Edge-Case Coverage floor does not directly apply. As a proxy: each advocate's "If my framing is wrong, it's probably because…" section serves the same role. All three populated it substantively. Floor satisfied.

## What gets carried forward into the merged output

From Analyzer (base):
- 4-tier ranking framework (behavior-shaping / integration / infrastructure / instrumentation)
- Explicit cluster annotation
- Steelman of both designs in introduction
- Differences-only stance throughout

From Architect (incorporated):
- L3 state-mechanics labelling of execution model + orchestrator role
- U-003 ↔ U-005 paired-difference framing for the hallucination contract
- Cluster names (C-004 cluster = "subprocess pipeline + dispatcher orchestrator + sprint integration")

From QE (incorporated):
- Schema-up-front vs validator-at-end framing for C-016
- "Withhold access vs post-hoc validation" wording (originated in Architect's Round 2, refined by QE)
- Test-strategy framing as long-term behavior-shaping (elevated from infrastructure tier to its own line item)

From Round 2.5 invariant probe:
- The merged output must preserve pairing and clustering, not flatten them
- The "shared assumptions" section (A-001, A-002) must remain in the merged output
