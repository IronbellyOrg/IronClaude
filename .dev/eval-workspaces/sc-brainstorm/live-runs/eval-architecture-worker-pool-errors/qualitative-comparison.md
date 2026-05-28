# Qualitative Comparison: architecture-worker-pool-errors

**Baseline:** `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/iterations/iteration-2/eval-architecture-worker-pool-errors/with_skill/outputs/merged-requirements.md`

**Live:** `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/.dev/eval-workspaces/sc-brainstorm/live-runs/eval-architecture-worker-pool-errors/merged-requirements.md`

**Winner:** Baseline

## Score Table

| Dimension | Baseline | Live |
|---|---:|---:|
| Concreteness | 9 | 6 |
| Coverage | 9 | 8 |
| Actionability | 9 | 7 |
| Provenance | 9 | 5 |
| Adversarial synthesis | 8 | 6 |
| Fit to eval intent | 10 | 7 |
| **Total** | **54** | **39** |

## Critique-First Scoring Notes

### Concreteness

**Baseline: 10 - 1 = 9**

- Penalty -1: A few sources are cited by proposal section labels rather than independently verifiable source lines.
- Strength: Names concrete fleet classes, old DLQ files, a target subsystem, exact envelope fields, CLI syntax, IAM verbs, latency budgets, cost targets, migration ordering, and rollback mechanics.

**Live: 10 - 4 = 6**

- Penalty -2: Requirements are mostly generic contract language with no concrete fleets, files, deadlines, migration chunks, SLO thresholds, or cost targets.
- Penalty -1: Durable store, overhead budget, ownership, and compatibility-window decisions are deferred to open questions.
- Penalty -1: Replay, redaction, and quarantine controls are expressed as properties but not as implementable mechanisms.

### Coverage

**Baseline: 10 - 1 = 9**

- Penalty -1: It does not emphasize pool-level mixed result preservation and rollback policy variants as explicitly as live does.
- Strength: Covers taxonomy, DLQ, replay, audit, redaction, chaos tests, feature flags, observability, migration order, async refactor, performance, security, cost, and operational runbooks.

**Live: 10 - 2 = 8**

- Penalty -1: Misses seed-specific fleet migration details, Q1 incident economics, and billing-critical no-loss guarantees.
- Penalty -1: Lacks concrete DLQ implementation choices and chaos-harness content.
- Strength: Covers cancellation, timeout, rollback-failed, unknown states, mixed outcomes, compatibility adapters, and rollback semantics better than baseline.

### Actionability

**Baseline: 10 - 1 = 9**

- Penalty -1: Some open questions remain around per-message-type overrides and future UI/correlation work.
- Strength: A team could sequence work directly from the requirements because it gives concrete subsystem paths, feature flags, test gates, benchmark gates, migration order, and acceptance criteria.

**Live: 10 - 3 = 7**

- Penalty -1: Multiple key decisions are open, including durable store, overhead budget, compatibility window, idempotency classes, and ownership.
- Penalty -1: Acceptance criteria are testable but do not map to specific rollout slices, code locations, or measurable budgets.
- Penalty -1: Requirements say to define many policies rather than specifying the chosen policy.

### Provenance

**Baseline: 10 - 1 = 9**

- Penalty -1: Provenance references proposal sections and research sections, not immutable line-level evidence.
- Strength: Has frontmatter, source proposal list, debate transcript pointer, seed pointer, and a per-requirement provenance table mapping each requirement/risk/open question to sources.

**Live: 10 - 5 = 5**

- Penalty -2: Provenance is five coarse bullets only, grouped by persona rather than mapped per requirement.
- Penalty -1: No source-specific trace for individual functional requirements or acceptance criteria.
- Penalty -1: No explicit seed-brief references for preserving key scenario facts.
- Penalty -1: No indication which items came from adversarial debate versus initial proposal synthesis.

### Adversarial Synthesis

**Baseline: 10 - 2 = 8**

- Penalty -1: Uses adversarial debate outputs, but the final artifact has limited explanation of rejected alternatives.
- Penalty -1: A few compromises are carried as open questions instead of resolved decisions.
- Strength: It visibly integrates architect/devops/QA/security/performance tensions, e.g. PII redaction with performance constraints, replay safety with operational rate limits, chaos coverage, throughput and latency gates.

**Live: 10 - 4 = 6**

- Penalty -2: Multi-perspective synthesis is mostly implicit; the artifact reads like a normalized generic spec rather than a negotiated merge.
- Penalty -1: Tradeoffs are not surfaced with concrete accepted/rejected positions.
- Penalty -1: High-stakes replay, rollback, and store choices are deferred rather than adversarially resolved.

### Fit to Eval Intent

**Baseline: 10 - 0 = 10**

- No penalty: It is tightly tailored to the architecture worker-pool error scenario, including the 12-fleet context, incident-driven migration, billing-critical constraints, retry-cost target, and shared worker error subsystem.

**Live: 10 - 3 = 7**

- Penalty -2: It fits a generic worker-pool error contract problem but loses much of the case-specific architecture evaluation intent.
- Penalty -1: It omits several high-signal seed details that distinguish this eval from any other error-handling redesign.

## Top 3 Regressions in Live vs Baseline

1. **Major loss of scenario specificity.** Live removes the 12 worker fleets, Q1 incidents, roughly $40k retry cost, Q3 cost target, billing-critical fleets, concrete fleet migration order, old DLQ names, and target subsystem path that made the baseline architecture-specific.
2. **Weaker measurable implementation plan.** Live keeps broad requirements but drops the baseline's ≤2-week chunks, 100µs p99/5% latency gate, 13M messages/hour floor, 100 msg/sec replay default, 2-week canary soak, quarterly chaos/access reviews, and no-message-loss verification method.
3. **Substantially weaker provenance and debate traceability.** Live provenance only attributes broad proposal themes, while baseline maps requirements, NFRs, ACs, risks, open questions, and out-of-scope items to persona/debate/research origins.

## Top 3 Improvements in Live vs Baseline

1. **Better explicit pool-result semantics.** Live directly requires mixed outcomes to be preserved and prevents pool-level failure from erasing successful, failed, cancelled, or unknown item states.
2. **Broader terminal-state taxonomy.** Live adds explicit cancellation, timeout, rollback-failed, skipped, and unknown handling, which strengthens correctness for generic worker-pool execution contracts.
3. **Clearer migration compatibility concept.** Live's compatibility adapters for legacy ambiguous `None`/exception patterns and dual legacy/new envelope emission are a useful bridge that baseline only implies through per-fleet migration and flags.

## Structural Failure Interpretation

For this case, the comparison JSON reports **27/27 live assertions passing** and a baseline pass rate of 1.0. There is no structural failure in this eval case to explain away. The unavailable timing/token/strict-quality telemetry is a metadata coverage limitation, not a content quality failure. The live artifact's weaknesses are real qualitative regressions in specificity, actionability, and provenance, not parser or parameter mismatches.

## Adversarial Warrant

**/sc:adversarial --depth quick warranted:** No.

Reason: There is no unresolved tie or contradictory evidence. Baseline wins clearly on total score and on the most eval-relevant dimensions. Live has real improvements in mixed-result and rollback semantics, but those can be incorporated as targeted feedback; they do not create high-stakes ambiguity requiring a new adversarial pass.
