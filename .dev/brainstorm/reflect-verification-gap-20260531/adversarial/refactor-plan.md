# Refactoring Plan

## Overview

- **Base variant**: Proposal A — Outcome-Verification Manifest (OVM)
- **Incorporated variants**: Proposal B — Outcome-Verification Ledger (OVL)
- **Change count**: 9 incorporations + 5 mechanism-text additions (INV/A-NNN-driven) = 14 changes
- **Risk**: Low to Medium overall (additive merges; no replacements of load-bearing base sections)

## Planned Changes

### Change 1 — Extend taxonomy from 4 seats to 5 modes (INC-01, addresses C-002 merge)

- **Title**: Add V-Deferred-Logical as 5th verification mode
- **Source**: Proposal B §3.1 (lines 64-72, V-Deferred-Logical row in mode table)
- **Target location**: Base §2 (taxonomy table) and base §3.1 (Wave 1B.4 step)
- **Integration approach**: Augment — add 5th row to base §2 taxonomy table; add classification rule 5 to §3.1 enumeration; preserve base's 4 OVM seats verbatim
- **Rationale**: Debate point C-002 merged 90% confidence; Advocate-A explicitly conceded the V-Deferred-Logical gap in Round 2 ("OVM does not represent category-2 logical fidelity. B's V-Deferred-Logical is the correct representational home"); closes the docker case's logical-fidelity layer
- **Risk level**: Low — additive 5th category, does not modify the 4 base seats

### Change 2 — Add `outcome_verified` derived boolean field (INC-02)

- **Title**: Add single-axis derived field for consumer convenience
- **Source**: Proposal B §3.5 line 148 (`outcome_verified` field definition)
- **Target location**: Base §3.3 contract fields section, after the per-seat counters
- **Integration approach**: Append — add field with derivation rule (`true iff every actionable finding is V-Repo OR (V-Upstream-Available AND no contradiction)`)
- **Rationale**: Debate point C-005 merge 80% confidence; consumer-side parsing reduction is real value for sc:troubleshoot Wave 6 + sprint executor
- **Risk level**: Low — purely additive

### Change 3 — Merge cond 10 formulation (INC-03, addresses C-007 merge)

- **Title**: Combine failure-floor AND verification-or-runbook-present semantics
- **Source**: Proposal B §3.7 (cond 10 text)
- **Target location**: Base §3.5 (cond 10 definition)
- **Integration approach**: Replace base §3.5's `outcome_claims_failed == 0` with merged formulation: `outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)`
- **Rationale**: Debate point C-007 merged 85% confidence; A's strict-on-failure + B's permissive-on-deferred-with-runbook are complementary; neither alone is sufficient
- **Risk level**: Low — stricter gate is safer; only blocks promotion that base or B would also have blocked

### Change 4 — Extend evidence-validator with row-presence check (INC-04, addresses C-008 merge)

- **Title**: Add presence-check alongside schema validation
- **Source**: Proposal B §3.6 (presence check requirement)
- **Target location**: Base §3.4 (evidence-validator extension)
- **Integration approach**: Append second responsibility — base already extends evidence-validator with schema validation; add: "AND every actionable finding from REPORT.md MUST correspond to exactly one row in `outcome-claims.yaml`. Findings without a row are dropped per §11.1 third-bucket rule."
- **Rationale**: Debate point C-008 merge 85% confidence; complementary not exclusive
- **Risk level**: Low — additive enforcement; consistent with §11.2 drop-not-downgrade

### Change 5 — Replace cross-skill propagation mechanism (INC-05, addresses C-010)

- **Title**: Drop new shared-refs directory; sibling skills inherit by writing valid artifact
- **Source**: Proposal B §3.9 (artifact-shape cross-skill approach)
- **Target location**: Base §3.7 (cross-skill propagation)
- **Integration approach**: Replace — base's "shared ref under `/config/.claude/skills/_shared/outcome-verification/`" → B's "artifact shape is the contract; sibling skills participate by writing valid `outcome-claims.yaml`. `refs/claim-extraction-patterns.yaml` stays in `sc-reflect-protocol/refs/` (single-skill home)"
- **Rationale**: Debate point C-010 B wins 80% confidence; lighter-weight, no new infrastructure, mirrors §10.6 grounding-gaps which has no shared-refs directory either
- **Risk level**: Low — removes infrastructure, reduces protocol surface

### Change 6 — Add cross-service contract drift generalization (INC-06)

- **Title**: Add 6th generalization shape with recursive reflect-on-consumer pattern
- **Source**: Proposal B §4.5 (cross-service contract drift)
- **Target location**: Base §4 (generalization shapes)
- **Integration approach**: Append — base §4 currently has 5 shapes (4.1-4.5); add §4.6 cross-service contract drift with `next_actor: downstream-agent` runbook example
- **Rationale**: Unique contribution U-006 take from B 80% confidence; novel pattern, useful for multi-repo work
- **Risk level**: Low — purely additive; does not alter existing 5 shapes

### Change 7 — Append §19.2 INV-023 hardening integration (INC-07)

- **Title**: Connect OVM falsifier to existing v1.1 sufficiency-claim hardening
- **Source**: Proposal B §6 final paragraph
- **Target location**: Base §6 (backward-compat) — append paragraph
- **Integration approach**: Append — base §6 currently ends with migration-window discussion; add paragraph: "**v1.1 deferred-hardening integration.** OVM folds naturally into §19.2's INV-023 path: the iteration-2 evidence for the `T2-converges-on-wrong-answer` case can now include outcome-verification classification accuracy as a sub-criterion, and the v1.1 tightening from 'conditional' to 'demonstrated' gains a broader sufficiency surface."
- **Rationale**: Unique contribution U-009 take from B 85% confidence; connects to existing hardening trajectory
- **Risk level**: Low — additive cross-reference

### Change 8 — Add bonus generalization shape (INC-08)

- **Title**: Test-suite invariant violation as V-Deferred-Logical example
- **Source**: Proposal B §4 final bullet ("Bonus shape")
- **Target location**: Base §4 — append §4.7 (bonus)
- **Integration approach**: Append — short paragraph showing V-Deferred-Logical mode usage in test-suite context
- **Rationale**: Unique contribution U-008 take from B 60% confidence; reinforces V-Deferred-Logical mode usage
- **Risk level**: Low — purely additive

### Change 9 — Add supplementary deferred-runtime-config falsifier (INC-09)

- **Title**: V-Deferred-Outcome mode coverage falsifier as sibling case
- **Source**: Proposal B §7 ("companion falsifier `outcome-verification-deferred-runtime-config.yaml`")
- **Target location**: Base §7 (falsifier section) — append after iteration-1-active docker falsifier
- **Integration approach**: Append — base's docker falsifier remains `status: active`; add sibling falsifier for V-Deferred-Outcome coverage (sysctl tuning runbook from base §4.5)
- **Rationale**: Debate C-012 A wins on docker case; B's V-Deferred-Outcome falsifier is complementary, not competing
- **Risk level**: Low — additive eval case

### Change 10 — Specify `--no-install-recommends` parser scope (INV-002 addition)

- **Title**: Address invariant-probe MEDIUM warning on apt-flag detection
- **Source**: Invariant probe INV-002 (Round 2.5)
- **Target location**: Base §3.2 (Wave 5 outcome-verification pass — external-spec branch)
- **Integration approach**: Append — explicitly document the parser scope: "The orchestrator detects `--no-install-recommends` by literal-substring match on the install command line. Variants handled: `--no-install-recommends`, `--no-install-suggests`. Variants currently NOT handled (listed as known limitations in §5): `-o APT::Install-Recommends=false`, `Dpkg::Options::='--force-confdef'` overrides. Multi-line continuation: parser concatenates lines ending in `\\` before flag detection."
- **Rationale**: Invariant probe Round 2.5 flagged MEDIUM; mandatory to address in mechanism text per probe gate semantics
- **Risk level**: Low — clarifies existing mechanism, doesn't change behavior

### Change 11 — Specify per-package claim granularity (INV-003 addition)

- **Title**: Address invariant-probe LOW warning on claim-extraction granularity
- **Source**: Invariant probe INV-003
- **Target location**: Base §3.1 (Wave 1B.4 extraction step)
- **Integration approach**: Append — add rule: "One implicit claim per `(package, install-line)` pair. Example: `apt-get install -y --no-install-recommends docker.io git curl` emits 3 separate claims (one per package). Multi-line installs across `\\` continuations are concatenated first."
- **Rationale**: Invariant probe LOW; clarifies extraction semantics
- **Risk level**: Low — clarifies, doesn't change behavior

### Change 12 — Add multi-mode precedence rule (INV-005 addition)

- **Title**: Address invariant-probe MEDIUM warning on multi-mode claim classification
- **Source**: Invariant probe INV-005
- **Target location**: Base §3.1 (after step 3 in classification enumeration)
- **Integration approach**: Append — add precedence rule: "**Multi-mode precedence**: when a claim satisfies multiple modes, apply this order: V-Deferred-Logical > V-Deferred-Outcome > V-Upstream-Available > V-Repo. Rationale: V-Deferred-Logical signals tier-escalation; if Tier 2 resolves the logical question, the claim collapses to a stricter mode. Example: 'rebuild changes the install-list outcome' is V-Deferred-Logical at T1 (does the mechanism propagate?); if T2 traces the logical chain and confirms the install line is unchanged, the claim becomes V-Upstream-Available (verify against apt-cache show)."
- **Rationale**: Invariant probe MEDIUM; mandatory addition
- **Risk level**: Low — clarifies edge case

### Change 13 — Document WebFetch-addability assumption in §5 trade-offs (A-001 addition)

- **Title**: Surface shared-assumption A-001 explicitly
- **Source**: Invariant-probe Round 2.5 (A-001 promoted)
- **Target location**: Base §5 (trade-offs and risks) — append bullet
- **Integration approach**: Append — add: "**Assumption (A-001): WebFetch/WebSearch can be added to allowed-tools.** Both this proposal and v1.0's allowed-tools-frontmatter pattern assume the addition is purely a frontmatter edit. If a future policy gate (security review, capability scope) blocks the addition, the fallback is to route all `external-spec` claims to `V-Deferred-Outcome` with a runbook `next_actor: operator, next_instrument: <Bash with internet access>`. Honest degradation, no silent regression."
- **Rationale**: Shared-assumption A-001 surfaced as UNSTATED by invariant probe; mandatory documentation
- **Risk level**: Low — clarifies fallback semantics

### Change 14 — Document operator-execution assumption in §5 trade-offs (A-002 addition)

- **Title**: Surface shared-assumption A-002 explicitly
- **Source**: Invariant-probe Round 2.5 (A-002 promoted)
- **Target location**: Base §5 (trade-offs and risks) — append bullet
- **Integration approach**: Append — add: "**Assumption (A-002): operator / CI executes deferred runbooks.** The 'deferred-with-runbook = honest success' semantics depends on a downstream actor actually running the runbook. Reflect emits the runbook and exposes `promotion_deferred_outcomes_count > 0` in the contract; enforcement (CI gate that blocks subsequent merges until the count is reconciled, sprint phase that halts on open runbooks, etc.) is out of scope for the audit protocol. Operator-ignored runbooks remain a downstream-workflow responsibility. Recommendation: pair OVM landing with a separate proposal for CI/sprint enforcement hooks."
- **Rationale**: Shared-assumption A-002 surfaced as UNSTATED; mandatory documentation
- **Risk level**: Low — clarifies known limitation

## Changes NOT Being Made (transparency — debate-rejected)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|--------------------|----------------------------|
| C-001 (naming OVL) | Adopt "Ledger" name from B | Keep "OVM" for merged proposal's central name; mechanism is what matters, name is cosmetic; alternative name acceptable at task-builder time if user prefers. Confidence: 70% — could go either way. |
| C-004 (classifier-picks toolkit) | B's abstraction | A's enumerated toolkit wins 90% confidence; downstream /task agent must know exactly which tools to invoke |
| C-012 (skeleton-pending falsifier) | B's iteration-3 deferral | A's iteration-1 active fixture wins; docker miss is real, deserves immediate eval |
| A §3.7 shared-refs directory (originally in base) | (kept) | Overridden by Change 5 (INC-05); B's contract-is-shape is lighter |

## Risk Summary

| Change | Risk Level | Impact | Rollback |
|--------|-----------|--------|----------|
| 1-9 (B incorporations) | Low | Additive, complementary; no replacement of load-bearing base text | Drop the new addition; merged proposal degrades to base-A behavior |
| 5 (cross-skill replace) | Low | Removes new infrastructure (shared-refs dir); reduces surface | Restore base §3.7 shared-refs text |
| 10-12 (INV mechanism-text additions) | Low | Clarifies existing behavior; addresses invariant-probe MEDIUM warnings | Already implicit in base; explicit text is the only delta |
| 13-14 (shared-assumption docs) | Low | Surfaces UNSTATED assumptions in §5 trade-offs | Remove bullets; assumptions remain implicit (less honest but harmless) |

**Aggregate risk: Low.** All changes are additive merges or clarifications; no load-bearing text is replaced except the cross-skill propagation (Change 5), which removes infrastructure rather than adding.

## Review Status

- Default: **Auto-approved** (no --interactive flag in args)
- Timestamp: 2026-05-31T03:51:30Z
- Approver: orchestrator (debate-derived; per-change rationale cited)
