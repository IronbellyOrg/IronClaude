# Diff Analysis — BRV-MG Proposals A vs B

## Metadata
- Generated: 2026-05-31T18:25:00Z
- Variants compared: 2 (Proposal A "Third mode" / Proposal B "Sibling skill")
- Total differences found: 19 (2 structural, 11 content, 1 contradiction, 5 unique contributions, 4 shared assumptions; 2 promoted to A-NNN diff points)
- Categories: structural (2), content (11), contradictions (1 — architectural), unique (5), shared assumptions (4 surfaced, 2 promoted)

## Structural Differences

| # | Area | Variant A (Third Mode) | Variant B (Sibling Skill) | Severity |
|---|------|------------------------|---------------------------|----------|
| S-001 | §6/§7 section structure | All 9 §7 sections present | All 9 §7 sections present | Low (none) |
| S-002 | §3 mechanism subsection density | §3.1-§3.? (extends reflect across multiple sections) | §3.1-§3.6 (one new skill + 1 workflow + 1 ref + cross-skill notes) | Low |

## Content Differences

| # | Topic | Variant A | Variant B | Severity |
|---|-------|-----------|-----------|----------|
| C-001 | **Where the surface lives** | Extends `sc:reflect` with `--mode pr-bot-validation` (third mode alongside `--mode pre` / `--mode post`) | Brand-new sibling skill `sc:pr-bot-validate` at `src/superclaude/skills/sc-pr-bot-validate-protocol/`; reflect unchanged | **HIGH — architectural contradiction (see X-001)** |
| C-002 | Reflect protocol changes | Adds wave step(s), contract fields with `pr_bot_validation_*` prefix, gate cond 11 (mode-conditional), new ref `refs/bot-review-sources.yaml` inside reflect | **Zero changes to reflect**. Reflect ships as v1.0 → v1.1 = OVM alone. | HIGH (downstream consequence of C-001) |
| C-003 | Merge-gate primitive | `gh api .../statuses/...` status check `sc-reflect/pr-bot-validation` posted by reflect | `gh api .../statuses/...` status check `sc-pr-bot-validate / merge-gate` posted by sibling skill | Low (same primitive, different posting agent) |
| C-004 | Gate condition layer | Adds cond 11 to reflect's §14.5.2 promotion gate (mode-conditional / vacuous on UC-1/UC-2) | Does NOT touch reflect's §14.5.2 gate. Sibling has its OWN PR-layer gate via GitHub status check (decoupled). | **HIGH (architectural)** |
| C-005 | Contract version bump | Reflect bumps 1.0 → 1.1 (composing with OVM's bump); new mode is additive per §9.4 | Reflect bumps 1.0 → 1.1 from OVM ONLY. Sibling ships at its own 1.0 (independent versioning). | Medium |
| C-006 | Bot-source ref file location | `refs/bot-review-sources.yaml` inside `sc-reflect-protocol/refs/` | `refs/bot-review-sources.yaml` inside `sc-pr-bot-validate-protocol/refs/` | Low (same shape, different skill) |
| C-007 | Triggers | Reflect's third mode auto-triggers via CI workflow `sc-reflect-pr-bot-validation.yml` on PR sync/open/bot-review-submitted; manual via `/sc:reflect --mode pr-bot-validation` | Sibling auto-triggers via `.github/workflows/pr-bot-validate.yml` on `pull_request_review` + `pull_request.synchronize`; manual via `/sc:pr-bot-validate <N>` | Low (same mechanism, different skill names) |
| C-008 | Cost envelope | T2 (~35-70k Claude) per invocation; 6-way fan-out dominates | Same; sibling inherits reflect's cost profile by invoking it at Wave 4 | Low |
| C-009 | OVM composition mechanism | New fields `pr_bot_validation_*` added to reflect's contract alongside OVM's fields | Sibling READS reflect's OVM-extended contract (`outcome_verified`, `deferred_outcomes_runbook_present`, `outcome_claims_failed`) read-only; emits own `merge-gate-decision.yaml` + own return-contract.yaml | **Medium (different composition model)** |
| C-010 | task-builder + /task handoff | Reflect's third mode hands off to task-builder + /task within Phase 5 of its own pipeline | Sibling skill stops at Wave 4 (Phase 4 in pipeline); surfaces `remediation_handoff` field in own return contract for operator to invoke task-builder themselves | Medium |
| C-011 | Force-push handling | Reflect's third mode re-runs the bucket logic against the new HEAD; emits `sha_changed` field | GitHub's `synchronize` event re-triggers the sibling's Wave 1-4 automatically; per-SHA status check semantics handle force-push natively | Low (B leverages existing GitHub infrastructure more directly) |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | **Architectural home of the pipeline** | The 6-way pipeline IS a reflect mode — extending reflect to cover PR-scoped audits is consistent with reflect's identity as the canonical audit-class skill | The 6-way pipeline is NOT a reflect mode — extending reflect dilutes its identity (cf. §17.7 Kill #3); the pipeline is an *orchestrator over reflect* (it calls reflect twice as a sub-step at Phases 4-5), and putting an orchestrator inside the thing it orchestrates inverts the dependency arrow | **HIGH — Architectural; cannot be averaged away** |

This contradiction is structurally load-bearing. The two proposals cannot both be right. The debate (§Round 1+2 below) adjudicates which framing wins.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|------------------|
| U-001 | A | Full enumerated `pr_bot_validation_*` contract field family (12 fields + derived `pr_bot_validated` boolean) with detailed semantics — usable verbatim in either architecture | **High** — well-thought-out field shapes; reusable in B's `merge-gate-decision.yaml` schema |
| U-002 | A | `--max-prs` budget composition with OVM's `--budget-remaining` and reflect's §15 cost profile — concrete numerics ("~9 turns/PR derived from §15 T2-midpoint 52 ÷ 6 parallel PRs ≈ 8.7") | Medium-High — useful for either architecture |
| U-003 | B | **§17.7 Kill #3 identity-dilution argument** — cites reflect's own kill-list as the structural precedent for refusing to add another orchestration surface | **HIGH — load-bearing for X-001 adjudication** |
| U-004 | B | **PR-layer vs work-unit-layer separation principle** — explicitly distinguishes the two lifecycles and argues OVM's cond 10 (work-unit) and a PR-layer gate are categorically different; one moves a tasklist folder, the other gates `gh pr merge` | **HIGH — structurally correct framing** |
| U-005 | B | **GitHub status check as the canonical first-class merge gate** primitive — branch protection literally consumes status checks; arguing this is "the canonical mechanism" closes the merge-gate-objective with mechanism native to GitHub, not invented by us | High — answers preamble §4 Q3 with platform-native primitive |

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Promoted |
|---|-----------|------------------|----------------|----------|
| A-001 | The 6-way parallel orchestration in preamble §3 IS the right structural shape (don't serialize it; don't reduce to ≤2 PRs) | Both proposals preserve the 6-way fan-out | STATED (preamble §5 explicit) | No |
| A-002 | `gh` CLI's `gh api .../statuses/<sha>` endpoint is the canonical first-class GitHub merge-gate primitive that branch protection consumes | Both proposals use this | UNSTATED in either proposal as a load-bearing assumption (B more explicit at line 8 inferred) | Yes (A-001) |
| A-003 | `sc:auggie-review` with `--no-post-pr --no-remediation-offer --depth standard --output-dir /tmp/pr-<N>-auggie-fresh/` is the right validation primitive at the per-PR level | Both reuse this verbatim | STATED (preamble §3 explicit) | No |
| A-004 | Operator-driven Phase 5 (task-builder + /task + reflect --mode post) remains operator-driven; no auto-execution | Both honor preamble §5 + reflect's §boundaries explicitly | STATED (preamble §5 + §9 explicit) | No |

### Promoted shared-assumption diff points (debate-mandatory)

| A-NNN | Assumption | Impact | Status |
|-------|-----------|--------|--------|
| A-001 | `gh api .../statuses/<sha>` is the canonical first-class merge-gate primitive consumed by GitHub branch protection (stable in May 2026 CLI; no rate-limit on per-PR per-SHA writes; status check name is stable enough for branch protection rules) | Both proposals depend on this; if it breaks (rate limits, API changes, branch-protection-status-check binding semantics drift), the entire mechanism fails | Surfaced for debate |

## Summary

- Total structural differences: 2 (both Low — same §7 structure preserved by both)
- Total content differences: 11 (3 HIGH: C-001 architectural home + C-002 reflect untouched + C-004 gate-condition layer; 4 Medium: C-005, C-009, C-010, C-011; 4 Low)
- Total contradictions: 1 (X-001 — architectural; load-bearing)
- Total unique contributions: 5 (3 High: U-001 A's contract fields, U-003 B's kill-list argument, U-004 B's layer separation; 1 Medium-High: U-002 A's budget composition; 1 High: U-005 B's status-check primitive)
- Total shared assumptions surfaced: 4 (3 STATED, 1 UNSTATED promoted as A-001)
- Highest-severity items: X-001 architectural contradiction; U-003 + U-004 + U-005 from B; U-001 from A

**Similarity check:** 19 differences substantially > 10% threshold; proposals are differentiated enough for debate to add value.

**Convergence direction (informal):** This is NOT a "take both" merge. The architectural contradiction X-001 must be adjudicated, and the resulting merge will pick ONE direction and incorporate the other's reusable strengths. Based on the U-003 + U-004 structural arguments from B (kill-list identity dilution + PR-vs-work-unit layer separation), the strongly-defensible direction is B's sibling-skill approach. A's contract field shapes (U-001) and budget composition (U-002) port cleanly into B's contract.
