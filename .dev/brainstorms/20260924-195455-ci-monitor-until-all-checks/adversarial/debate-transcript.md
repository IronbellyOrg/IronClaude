# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2
- Convergence achieved: 92%
- Convergence threshold: 75%
- Advocate count: 3

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect)
Steelmans V2: wait≠fix is the right invariant — a wait is not a fix cycle, so HALT should not skip it. Steelmans V3: untestable FRs are debt.

Strengths: entry table makes the gate reviewable; empty+polling payload is an explicit contract.

Concession: extra spec FM-CI-7 rewrite is optional if SKILL.md is the SoT.

A-002 QUALIFY: `--required` nonempty is the product filter; document it so operators are not surprised.

### Variant 2 Advocate (sonnet:refactorer)
Steelmans V1: a table is documentation, not a machine — acceptable if it lives in existing `ci-poll.md`. Steelmans V3: mix-pending test is the one missing unit.

Strengths: fewest files; findings after halt stay REPORT_ONLY (no silent extra pushes).

Concession: `incomplete` flag on JSON is optional if `state:polling` + non-empty-or-omitted checks is enough. Prefer `state:polling` with `checks:[]` only when parse failed AND we set state polling in the **script**, so classify is not the source of truth for crash — script is.

### Variant 3 Advocate (haiku:qa)
Steelmans V2: wait-only is the smallest behavior that greens “until ALL come back.” Steelmans V1: entry table is how reviewers verify G-3.

Strengths: T-CI-CLS-MIX; poller empty-stdout test; do not call classify on crashed stdout.

Concession: FC-1–FC-12 is a catalog, not all must become tests — MIX + empty-as_array + halt-then-wait are the three that fail today.

## Round 2: Rebuttals

All three accept: (1) Wave 8 wait after HALT_MAX_ROUNDS; (2) auto-fix still shared max_rounds; (3) as_array never empty; (4) pending wins mix; (5) no fsm.py.

Unresolved (cosmetic): whether `incomplete` is a JSON field vs script `state:polling`. Majority: script sets `state:polling` on parse miss; no new EventType.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence |
|------------|--------|------------|----------|
| C-001 wait after halt | V2 (shared) | 95% | All three; V2 names FM-CI-7 as the debt |
| C-002 as_array | V2 | 90% | Smallest mechanical fix |
| C-003 parse≠empty | V3+V1 | 85% | Script must not feed fake [] as success |
| C-004 timeout flag | V2 | 92% | Defer |
| U-001 entry table | V1 | 80% | Merge into SKILL + ci-poll, not a new file |
| U-002 wait≠fix | V2 | 95% | Core invariant |
| U-003 MIX test | V3 | 90% | Missing unit |
| A-002 required filter | QUALIFY | 80% | Document E9; not a false-clean |

## Convergence Assessment
- Points resolved: 8 of 8 material
- Alignment: 92%
- Status: CONVERGED
- Taxonomy: L1 style, L2 wait≠fix split, L3 pending-guard / empty-stdout / HALT entry
- HIGH unaddressed invariants: 0
