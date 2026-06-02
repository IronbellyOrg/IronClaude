# Refactoring Plan — BRV-MG Merge

## Overview

- **Base variant:** Proposal B — Sibling Skill `sc:pr-bot-validate`
- **Incorporated variants:** Proposal A — Third Mode (contract field shapes + budget composition + status semantics + trigger flag enumeration)
- **Change count:** 5 incorporations from A + 5 mechanism-text additions from invariant probe = 10 changes
- **Risk:** Low overall (additive refinements to B's already-correct architecture; no replacement of load-bearing base text)

## Planned Changes

### Change 1 — Port A's `pr_bot_validation_*` contract field family into B's sibling-skill schema (INC-01)

- **Title:** Adopt A's enumerated contract field shapes, namespace-renamed to `pr_bot_validate_*` for sibling-skill consistency
- **Source:** Proposal A's contract field block (A §3 / §9.1 additions: 12 namespaced fields + derived `pr_bot_validated` boolean)
- **Target location:** B §3 sibling-skill return contract + §4 composition table
- **Integration approach:** Replace B's sketched field list with A's enumerated shapes, renaming the prefix from `pr_bot_validation_*` to `pr_bot_validate_*` (matches sibling skill name `sc:pr-bot-validate`). Preserve field semantics; preserve the derived-boolean pattern.
- **Rationale:** A's field family is downstream-executable; B's is sketched. Take from A 95% confidence per scoring matrix.
- **Risk level:** Low — additive within B's architecture; no displacement

### Change 2 — Adopt A's budget composition mechanics (INC-02)

- **Title:** `--max-prs` + `--budget-remaining` + §15 T2-midpoint ÷ 6 parallel PRs ≈ 8.7 turns/PR derivation
- **Source:** Proposal A §6 trade-offs (budget composition section)
- **Target location:** B §3.2 Wave 0 (where the budget check fires) + B §6 trade-offs
- **Integration approach:** Append A's numerics + derivation reasoning. Wave 0 routes per the same table OVM defines in `§4.0 Step 0.9` (reflect's existing budget pre-flight semantics, with `T1-midpoint=6` and `T2-midpoint=52`).
- **Rationale:** A's budget composition is well-thought-out and reuses reflect's existing §15 cost profile. Take from A 90%.
- **Risk level:** Low — additive

### Change 3 — Fold A's three-state PASS/FAIL/PENDING status semantics into B (INC-03)

- **Title:** Adopt A's enumerated status check semantics with PENDING-initial-state clarity
- **Source:** Proposal A §3 status check semantics block
- **Target location:** B §3.3 status check section
- **Integration approach:** Replace B's status check semantics block with A's three-state block VERBATIM (PASS / FAIL / PENDING with the explicit "PENDING posted at Wave 0 as initial state" clarification). Both proposals had similar shape; A's wording is more precise on the PENDING transition.
- **Rationale:** A's semantics are downstream-executable; B's are correct but slightly less explicit on PENDING.
- **Risk level:** Low — same primitive, better wording

### Change 4 — Adopt A's manual-invocation flag enumeration (INC-04)

- **Title:** Use A's enumerated flag set for the manual CLI invocation
- **Source:** Proposal A §3 trigger spec
- **Target location:** B §3.4 CLI section
- **Integration approach:** Append A's `--max-prs`, `--depth`, `--output-dir`, `--bot-source-filter`, etc. flag spec to B's CLI section. Triggers (`pull_request_review` + `pull_request.synchronize`) are identical in both; nothing to merge there.
- **Rationale:** A's flag enumeration is downstream-executable specification
- **Risk level:** Low — additive

### Change 5 — Add multi-bot disagreement as v1.2-deferred out-of-scope (INC-05)

- **Title:** Explicit v1.2-defer for multi-bot disagreement adjudication (INV-005 + A §6 partial mention)
- **Source:** Proposal A §6 brief mention + invariant probe INV-005
- **Target location:** B §9 out-of-scope items
- **Integration approach:** Add new bullet: "Multi-bot disagreement adjudication (e.g., Augment says CONFIRMED + CodeRabbit says FALSE_POSITIVE on the same file:line) — deferred to v1.2; v1.0 processes each bot independently and emits per-bot finding rows in `pr-bot-validation.yaml`, leaving operator to adjudicate."
- **Rationale:** Honest scoping; closes INV-005 + addresses A's partial mention
- **Risk level:** Low — out-of-scope declaration

### Change 6 — Add GitHub status-check idempotency note (INV-002 addition)

- **Title:** Document the `gh api .../statuses/<sha>` write idempotency assumption
- **Source:** Invariant probe INV-002 (Round 2.5)
- **Target location:** B §5 trade-offs and risks
- **Integration approach:** Append paragraph: "**Assumption (INV-002):** `gh api repos/{owner}/{repo}/statuses/{sha}` writes to the same `(sha, context)` are idempotent in effect — branch protection consumes only the most recent status. Cited from GitHub REST API spec (sha:refs/statuses endpoint). If this changes (rate-limit imposed, write-once semantics added), the sibling skill must track its own `last-posted-status.json` cache and skip redundant writes."
- **Rationale:** Invariant probe MEDIUM; mandatory addition
- **Risk level:** Low — clarifies assumption; provides fallback

### Change 7 — Specify `--max-prs` + `--budget-remaining` degradation (INV-003 addition)

- **Title:** Concrete degradation rule for budget-vs-PR-count interaction
- **Source:** Invariant probe INV-003
- **Target location:** B §3 (CLI flag specs section) + §5 trade-offs
- **Integration approach:** Add to §3 flag spec: "If `--budget-remaining` is provided AND the sum of estimated turns for `--max-prs` exceeds `--budget-remaining`, the skill degrades `--max-prs` to `floor((--budget-remaining - 5) / 8.7)` with a WARN message; the skill NEVER errors silently. Floor of 5 turns reserves headroom for Wave 0 + Wave 3 + Wave 4. If the degraded value is 0 (budget < 14 turns), the skill HALTs with `status: failed`, `failure_reason: budget-insufficient`."
- **Rationale:** Invariant probe LOW; clarifies behavior
- **Risk level:** Low — concrete spec where B was sketched

### Change 8 — Specify empty-PR-set behavior (INV-004 addition)

- **Title:** Concrete behavior for zero matching PRs
- **Source:** Invariant probe INV-004
- **Target location:** B §3.2 Wave 1 discovery section
- **Integration approach:** Append: "**Empty-PR-set behavior.** If `gh pr list` returns zero PRs matching the `refs/bot-review-sources.yaml` patterns, the skill exits cleanly with `status: success`, `prs_processed: 0`, `merge_gate_decision: not_applicable`. No status check is posted (there is no PR target). Audit log records the empty-set verdict. This is the explicit operational success state — distinct from `status: failed`."
- **Rationale:** Invariant probe LOW; mandatory clarification
- **Risk level:** Low — clarifies edge case

### Change 9 — Surface gh CLI status-check stability assumption (A-001 promotion)

- **Title:** Document the shared assumption with explicit fallback
- **Source:** Shared-assumption A-001 promoted by invariant probe
- **Target location:** B §5 trade-offs
- **Integration approach:** Append paragraph: "**Assumption (A-001):** `gh api repos/{owner}/{repo}/statuses/<sha>` remains the canonical GitHub merge-gate primitive consumed by branch protection (verified against GitHub REST API v2026.5 docs at proposal-authoring time). If a future GitHub change deprecates this endpoint or migrates branch-protection-status-check-binding to a different primitive (e.g., GitHub Checks API), the skill must update §3.3 mechanism and the workflow at §3.4 — but the protocol surface (a sibling skill emitting merge-gate verdicts) is unchanged. Fallback for transient `gh api` failures: post a retry after exponential backoff (max 3 retries); on persistent failure, emit `status: partial` with `merge_gate_decision: error` and surface to operator via WARN."
- **Rationale:** Promoted shared-assumption needs documentation + fallback
- **Risk level:** Low

### Change 10 — Add reflect §16 "Related Commands" one-line cross-reference (A's discoverability concession)

- **Title:** Low-cost discoverability bridge from reflect to the sibling skill
- **Source:** Round 2 Advocate-B concession to A's operator-cognitive-load argument
- **Target location:** B §3 mechanism — add a one-line edit to `sc-reflect-protocol/SKILL.md` §16 "Related Commands"
- **Integration approach:** Add a one-line addition to reflect's §16 Related Commands list: "**`/sc:pr-bot-validate`** — PR-layer audit sibling skill; consumes reflect's return contract read-only at its Wave 4 to validate external bot-review signal as a first-class merge-gate input. Use when the work-unit you'd reflect on is *spread across multiple PRs with bot reviews attached*."
- **Rationale:** A's operator-cognitive-load argument has merit. A one-line cross-reference adds discoverability without surface change to reflect. NOT a contract change; just a §16 cross-link.
- **Risk level:** Low — single-line addition to existing §16

## Changes NOT Being Made (transparency — debate-rejected)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|----------------------------|
| X-001 (third mode home) | A's `--mode pr-bot-validation` | Debate-decided 95% to B; conceded by Advocate-A under §17.7 Kill #3 + PR-vs-work-unit layer separation + `--recursive` anti-pattern |
| C-002 (reflect changes) | A's reflect contract field additions | Falls under X-001; B's "reflect unchanged" is the structurally-correct outcome |
| C-004 (gate layer) | A's cond 11 in reflect's §14.5.2 promotion gate | Falls under X-001; B's GitHub-status-check layer separation is correct |
| C-005 (combined version bump) | A's bumping reflect contract to 1.2 to incorporate `pr_bot_validation_*` | B's independent sibling-skill 1.0 is cleaner; reflect stays at 1.1 (OVM only) |
| Single-CLI-surface | A's full single-skill ergonomic | A's concern is real but addressed via Change 10 (one-line cross-reference in reflect §16); does not require a single skill |

## Risk Summary

| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1-5 (A incorporations) | Low | Additive refinements to B's already-correct architecture; downstream-executable improvements | Drop the addition; merged proposal degrades to base-B behavior |
| 6-9 (invariant-probe mechanism additions) | Low | Clarifies existing behavior; addresses MEDIUM warnings | Remove; assumptions remain implicit (less honest but harmless) |
| 10 (reflect §16 cross-reference) | Low | Single-line addition to reflect; does NOT change reflect contract or behavior | Trivial revert |

**Aggregate risk: Low.** All changes are additive merges or clarifications. The one reflect-side change (Change 10) is a §16 cross-reference, not a contract or behavior change.

## Review Status

- Default: **Auto-approved** (no `--interactive` flag)
- Timestamp: 2026-05-31T18:35:00Z
- Approver: orchestrator (debate-derived; per-change rationale cited)
