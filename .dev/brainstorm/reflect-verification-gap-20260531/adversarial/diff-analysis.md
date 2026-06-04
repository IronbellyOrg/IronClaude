# Diff Analysis: Verification-Gap Proposal Comparison

## Metadata
- Generated: 2026-05-31T03:51:00Z
- Variants compared: 2 (Proposal A "OVM" / Proposal B "OVL")
- Total differences found: 23 (3 structural, 12 content, 0 contradictions, 9 unique contributions, 5 shared assumptions; 3 promoted to A-NNN diff points)
- Categories: structural (3), content (12), contradictions (0), unique (9), shared assumptions (3 promoted of 5 surfaced)

## Structural Differences

| # | Area | Variant A (OVM) | Variant B (OVL) | Severity |
|---|------|-----------------|-----------------|----------|
| S-001 | §7 section structure | 8 sections, exact match to preamble §7 template | 8 sections, exact match to preamble §7 template | Low (none) |
| S-002 | Mechanism subsection count | §3 has 7 numbered amendments (3.1-3.7) | §3 has 9 numbered amendments (3.1-3.9) | Low (B has more granular sibling-propagation discussion) |
| S-003 | Generalization-section bug-count | §4 has exactly 5 bug shapes per spec | §4 has 5 + "(Bonus shape)" | Low (B exceeds minimum) |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Artifact naming metaphor | "Manifest" — list of declared claims | "Ledger" — append-only record (mirrors §10.6 ledger metaphor) | Low |
| C-002 | Verification taxonomy axis | 4 **seats** (in-repo / external-spec / runtime / cross-system) — "who can verify from where" | 4 **modes** (V-Repo / V-Upstream-Available / V-Deferred-Outcome / V-Deferred-Logical) — "what's the verification mode" | **Medium** — different categorization axis; B has an explicit "logical" deferral mode A lacks |
| C-003 | Wave 1B insertion point | Step 1B.4, after 1B.3 cross-task scan, before Wave 1C | Step 1B.4, after 1B.3 cross-task scan | Low (same) |
| C-004 | Wave 5 verification toolkit | **Explicit enumeration**: `apt-cache show`, `dpkg -L`, `pip show`, `npm view`, `gh api`, `WebFetch`, `Skill context7`, `Skill tavily`, with template URL derivation rule for vendor docs and 24h-cache `<output>/external-spec-cache/` | Abstract: classifier picks "a tool that resolves the artifact's contract" with one-lookup-per-distinct-artifact memoization; no enumerated toolkit | **Medium** — A is downstream-executable; B requires implementer to pick tools |
| C-005 | Contract field count | ~10 new top-level fields (more granular, separate counters per seat + promotion-companion fields) | 8 new top-level fields + 1 derived (`outcome_verified` boolean) | Low (both additive minor bump) |
| C-006 | Status-enum handling | Boolean pair: `status: success` AND `outcome_verification_complete: false` signals "implementation verified, outcome deferred" | Same boolean pair pattern + explicit derived `outcome_verified` field for consumers wanting single-axis route | Low (same pattern; B has tidier derived field) |
| C-007 | Promotion-gate cond 10 formulation | `outcome_claims_failed == 0` — strict, focuses on failures | `outcome_verified == true OR deferred_outcomes_runbook_present == true` — focuses on positive verification OR explicit deferral | **Medium** — different semantics; A is stricter on failures, B is more permissive for deferred-with-runbook |
| C-008 | evidence-validator extension scope | Runbook **schema validation** (4 required non-empty fields, `next_command` single-executable check); drop-on-failure → status:partial | **Presence check** — every actionable finding MUST have a row in `outcome-verification.yaml`; no schema policing | **Medium** — A polices runbook quality, B polices row presence; complementary not exclusive |
| C-009 | Contradiction-routing terminology | Failed external-spec → `§10.4` Regression with new `evidence_source: outcome-verification-pass` field | `§3.4` contradiction routing → "synthetic Regression candidate" → `§5.3` rule 3 escalation | Low (same effect, different naming) |
| C-010 | Cross-skill propagation mechanism | Shared ref under new `/config/.claude/skills/_shared/outcome-verification/` directory; sibling skills consume the ref | "Artifact shape is the contract" — sibling skills inherit by writing valid `outcome-verification.yaml`; no new shared-refs infrastructure | **Medium** — A introduces infrastructure (new dir); B is contract-only and lighter |
| C-011 | Allowed-tools frontmatter | Add `WebFetch, WebSearch` | Add `WebFetch, WebSearch` | Low (identical) |
| C-012 | Falsifier eval-case maturity | `status: active` — iteration-1 fixture, immediately runnable | `status: skeleton-pending-iteration-3-fixture` — follows §12.5 skeleton pattern, promoted in iteration-3 | **Medium** — A is more aggressive (real-world miss, deserves immediate eval); B is more conservative (follows existing §12.5 staging pattern) |

## Contradictions

| # | Point of Conflict | Variant A Position | Variant B Position | Impact |
|---|-------------------|-------------------|-------------------|--------|
| X-001 | (none) | — | — | — |

No architectural contradictions found. Both proposals converge on the same general direction (parallel artifact pattern from §10.6 + new contract fields + new gate condition + WebFetch addition). Differences are formulation choices, not opposing claims.

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|------------------|
| U-001 | A | `verifier_tool` field in `outcome-claims.yaml` records which tool produced verification evidence | Medium — useful for audit/debug but not load-bearing |
| U-002 | A | Per-claim deferred-outcomes files at `<output>/deferred-outcomes/<claim_id>.yaml`, **moved alongside work-unit** in Wave 7 promotion | **High** — concrete answer to preamble §5 "runbook a fresh agent can pick up"; promotion-alongside is novel |
| U-003 | A | External-spec cache directory `<output>/external-spec-cache/` with content-sha + timestamp + 24h staleness re-fetch rule | **High** — handles rate limits, repeatability, network failures |
| U-004 | A | Diff-implicit upstream-artifact claim extraction with **regenerable pattern table** `refs/claim-extraction-patterns.yaml` (apt-get, pip, npm, gem, cargo, go get, gh api, aws, terraform patterns) | **High** — concrete extraction mechanism; ref-driven so operators add patterns without SKILL.md edits |
| U-005 | B | **V-Deferred-Logical mode** — explicitly carves out "second-order reasoning the audit declines at current tier" as a distinct mode hooked into tier-escalation | **High** — addresses category-2 logical fidelity gap (which A explicitly lists as "out of scope" in §5); this IS the gap that masked the docker miss at logical layer ("does rebuilding change the install line?") |
| U-006 | B | Runbook field `next_actor: downstream-agent` with concrete example: `next_action: run sc:reflect --mode post against the consumer repo at HEAD, expected_witness: consumer's outcome-verification.yaml shows V-Repo for the new payload field` | Medium — recursive-verification handoff pattern is novel; useful for multi-repo contract drift |
| U-007 | B | `outcome_verified` **derived single-axis boolean** for consumers that don't want to parse the 4 per-seat counts | Medium — convenience layer; reduces consumer-side parsing complexity |
| U-008 | B | "(Bonus shape)" — test-suite invariant violation as `V-Deferred-Logical` | Low — bonus generalization; supports the V-Deferred-Logical case but not load-bearing |
| U-009 | B | Explicit §19.2 INV-023 hardening-path integration — OVL "strengthens the conditional language" from "conditional" to "demonstrated under these gates" once falsifier eval data lands | Medium — connects this proposal to the existing v1.1 hardening trajectory; gives the falsifier eval case a structural home |

## Shared Assumptions

5 implicit preconditions surfaced from convergence points. 3 promoted to A-NNN diff points (UNSTATED). 1 STATED. 1 CONTRADICTED-adjacent but not load-bearing.

| # | Assumption | Source Agreement | Classification | Promoted |
|---|-----------|------------------|----------------|----------|
| A-001 | WebFetch / WebSearch can be added to allowed-tools without further policy gate | Both proposals add these (A §3.6, B §3.8); preamble §6.4 notes "would need adding" but doesn't enumerate other gates | **UNSTATED** | Yes (A-001) |
| A-002 | Operator / CI will execute deferred runbooks; `promotion_deferred_outcomes_count > 0` is a signal not an enforced contract | Both rely on this for the "deferred with runbook = honest success" semantics; preamble §5 says "must define a clear next-actor / next-action" but does not address enforcement | **UNSTATED** | Yes (A-002) |
| A-003 | The §10.6 grounding-gaps parallel-artifact pattern is reusable for outcome verification | Both cite §10.6 explicitly; both note "exactly analogous" / "mirrors pattern exactly" | **STATED** (in both proposals' text) | No (already explicit) |
| A-004 | Orchestrator can correctly distinguish Depends vs Recommends in `apt-cache show` output AND `--no-install-recommends` is statically detectable in the Dockerfile | A's docker case in §4.1 relies on this; B's §4.1 also relies; neither proves the orchestrator's parser handles edge cases (multi-line continuations, version constraints) | **UNSTATED** | Yes (A-003) |
| A-005 | Inline orchestrator-class classification at Step 1B.4 is reliable enough for the gate to be meaningful, without spawning a dedicated `outcome-classifier` agent | A doesn't introduce a new agent (§3 amendments); B explicitly says "no new agents required" (§7.2 inherited) | **STATED** (in B §7.2 reference) | No (B explicit) |

### Promoted shared-assumption diff points (debate-mandatory)

| A-NNN | Assumption | Impact | Status |
|-------|-----------|--------|--------|
| A-001 | WebFetch/WebSearch addable to allowed-tools without further policy gate | Both proposals' external-spec verification depends on it | Surfaced for debate |
| A-002 | Operator/CI executes deferred runbooks | Determines whether the "deferred-with-runbook = success" semantics holds in practice | Surfaced for debate |
| A-003 | Orchestrator's apt-cache / package-metadata parser is robust enough to detect the docker.io→docker-cli split | The docker case (both proposals' §4.1) depends on it | Surfaced for debate |

## Summary

- Total structural differences: 3 (all Low severity — same §7 structure)
- Total content differences: 12 (5 Medium: C-002, C-004, C-007, C-008, C-010, C-012; rest Low)
- Total contradictions: 0
- Total unique contributions: 9 (4 High: U-002, U-003, U-004, U-005; 4 Medium, 1 Low)
- Total shared assumptions surfaced: 5 (UNSTATED: 3, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-002 (taxonomy axis), C-004 (toolkit), C-007 (gate cond), C-008 (validator), C-010 (cross-skill), C-012 (falsifier); U-002, U-003, U-004, U-005

**Similarity check**: total differences (23) substantially > 10% threshold; proposals are differentiated enough for debate to add value.

**Convergence direction (informal)**: both base proposals + most unique contributions can be merged complementarily. Genuine contention lies on C-002 (taxonomy axis) and C-010 (cross-skill mechanism); the rest is "take both."
