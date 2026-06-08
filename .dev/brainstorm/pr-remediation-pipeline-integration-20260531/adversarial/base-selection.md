# Base Selection — BRV-MG

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A | Variant B | Computation |
|--------|--------|-----------|-----------|-------------|
| Requirement coverage (RC) | 0.30 | 0.92 | 0.95 | Both map to all preamble §6 sections + answer the 10 §4 structural questions. B's answers more directly satisfy preamble §5 constraints (zero reflect changes = lower v1.1 risk; layer separation explicit). |
| Internal consistency (IC) | 0.25 | 0.88 | 0.95 | A has a real internal tension: it argues identity-consolidation in §2 but the §17.7 Kill #3 argument (cited even in A's steelman of B) cuts against this. B is consistent throughout. |
| Specificity ratio (SR) | 0.15 | 0.93 | 0.88 | A has more enumerated contract fields, more numeric concretes (turn budgets, cost bands); B is more architecturally argued. |
| Dependency completeness (DC) | 0.15 | 0.90 | 0.92 | Both cite reflect SKILL.md sections and OVM merged proposal sections; B more explicitly cites §17.7 Kill #3 + §17 anti-recursion + §14.5.1 adapter table. |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Both have all 9 §6 sections |
| **quant_score** | | **0.917** | **0.937** | A: (0.92×0.30)+(0.88×0.25)+(0.93×0.15)+(0.90×0.15)+(1.00×0.15) = 0.917 / B: (0.95×0.30)+(0.95×0.25)+(0.88×0.15)+(0.92×0.15)+(1.00×0.15) = 0.937 |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Covers all preamble §6 sections | MET | MET |
| 2 | Addresses edge cases (force-push, empty PR set, multi-bot disagreement) | NOT MET (force-push addressed; empty set and multi-bot disagreement absent) | NOT MET (force-push addressed via GitHub `synchronize`; multi-bot disagreement absent; empty set absent — both proposals miss INV-004 + INV-005) |
| 3 | Dependencies + prerequisites named | MET | MET |
| 4 | Success/completion criteria | MET (PASS/FAIL/PENDING status check semantics) | MET (PASS/FAIL/PENDING status check semantics) |
| 5 | Specifies out-of-scope | MET | MET |

**Completeness subtotal: A 4/5, B 4/5**

### Correctness (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | No factual errors | MET | MET |
| 2 | Technical approaches feasible | MET | MET |
| 3 | Terminology consistent | MET | MET |
| 4 | No internal contradictions | NOT MET — A argues identity-consolidation but its own steelman concedes §17.7 Kill #3 applies | MET |
| 5 | Claims supported by evidence | MET | MET |

**Correctness subtotal: A 4/5, B 5/5** (A's internal-contradiction loses one point)

### Structure (5 criteria)

All 5 met by both. **Subtotal: A 5/5, B 5/5**

### Clarity (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Unambiguous language | MET | MET |
| 2 | Concrete vs abstract | MET — concrete contract fields, numeric budgets | NOT MET — more abstract architectural argument; less enumerated detail |
| 3 | Clear section purpose | MET | MET |
| 4 | Acronyms defined | MET | MET |
| 5 | Actionable next steps | MET | MET |

**Clarity subtotal: A 5/5, B 4/5** (B loses on Concrete-vs-Abstract)

### Risk Coverage (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | ≥3 risks with probability/impact | MET | MET |
| 2 | Mitigation strategy each | MET | MET |
| 3 | Failure modes + recovery | MET | MET |
| 4 | External dependencies + failure | MET (auggie-review unavailability addressed) | MET (gh CLI unavailability + branch-protection-rule mismatch addressed) |
| 5 | Monitoring/validation mechanism | MET (falsifier eval case) | MET (falsifier eval case) |

**Risk Coverage subtotal: A 5/5, B 5/5**

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Collection boundaries (empty / single / max) | NOT MET (empty PR set absent; max enforced via `--max-prs` cap) | NOT MET (same — INV-004 fires on both) |
| 2 | State variable interactions across boundaries | MET — reflect contract field interactions documented | MET — sibling skill's read-only consumption of reflect contract documented |
| 3 | Guard condition gaps | NOT MET — INV-002 status-check idempotency not addressed | NOT MET — INV-002 status-check idempotency not addressed |
| 4 | Count divergence scenarios | NOT MET — INV-003 `--max-prs` + budget interaction not fully specified | NOT MET — INV-003 same |
| 5 | Interaction effects | NOT MET — INV-005 multi-bot disagreement not addressed | NOT MET — INV-005 multi-bot disagreement not addressed |

**Invariant Edge Case subtotal: A 1/5, B 1/5** (both meet the §1/5 floor; both need mechanism-text additions to address INV-002/003/004/005)

### Qualitative Summary

| Dimension | A | B |
|-----------|---|---|
| Completeness | 4/5 | 4/5 |
| Correctness | 4/5 | 5/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case | 1/5 | 1/5 |
| **Total** | **24/30 = 0.800** | **24/30 = 0.800** |

**Tie on qualitative.** A's clarity advantage (+1) is canceled by B's correctness advantage (+1).

### Edge Case Floor Check

- A: 1/5 → meets floor → eligible
- B: 1/5 → meets floor → eligible

## Combined Scoring

| Variant | quant × 0.50 | qual × 0.50 | **Combined** |
|---------|--------------|--------------|--------------|
| **A** | 0.917 × 0.50 = 0.459 | 0.800 × 0.50 = 0.400 | **0.859** |
| **B** | 0.937 × 0.50 = 0.469 | 0.800 × 0.50 = 0.400 | **0.869** |

**Margin: 0.010 (1.0%) — within 5% tiebreaker zone.**

## Tiebreaker Protocol

**Level 1 — Debate performance (Step 2 scoring matrix):**

X-001 architectural contradiction adjudicated to B at 95% confidence after Advocate-A's explicit concession in Round 2 on §17.7 Kill #3, PR-vs-work-unit layer separation, and `--recursive` anti-pattern. The X-001 result is the LOAD-BEARING decision — every downstream content-level decision (C-001 through C-010) flows from it. **Level 1 wins decisively to B.**

A wins on: U-001 (contract field shapes, take from A), U-002 (budget composition, take from A). These are downstream details that port into B's architecture.

**Level 1 outcome: B wins debate performance.**

## Selected Base: Variant B (Sibling Skill — `sc:pr-bot-validate`)

**Selection rationale (combined evidence):**

- Marginally higher combined score (0.869 vs 0.859), within tiebreaker zone
- Decisive debate-performance win on X-001 (95% confidence) with Advocate-A's explicit concessions
- Higher quant_score driven by Internal Consistency (0.95 vs 0.88) — A has an unresolved internal contradiction between its consolidation argument and its acknowledgment of §17.7 Kill #3
- Higher Correctness qualitative score (5/5 vs 4/5) for the same reason

The decision is not purely numeric — it's debate-decisive. B's architectural arguments structurally cut against A's framing, and A's advocate conceded in Round 2.

**Strengths to preserve (from base B):**

1. **Sibling skill architecture** at `src/superclaude/skills/sc-pr-bot-validate-protocol/SKILL.md` (§3.1)
2. **PR-layer / work-unit-layer separation** (§1 line 21-23 + §4 composition table)
3. **`gh api .../statuses/<sha>` status check as merge-gate primitive** (§3.3)
4. **Reflect ships unchanged** as v1.0 → v1.1 = OVM alone (§3 zero reflect changes)
5. **4-wave pipeline mapping** of preamble §3 Phases 1-4 (§3.2)
6. **`refs/bot-review-sources.yaml`** in the sibling skill's own refs (§3 ref location)
7. **GitHub Actions workflow** `.github/workflows/pr-bot-validate.yml` (§3.4)
8. **Operator-driven Phase 5** — sibling stops at Wave 4 (§3.2 table + §9 out-of-scope)
9. **§17.7 Kill #3 framing** in §1 problem framing — the load-bearing structural argument
10. **Independent sibling-skill version** `pr_bot_validate_contract_version: 1.0` independent of reflect's 1.1 (§3.5 + §7 backward-compat)

**Strengths to incorporate from non-base A:**

| ID | From A section | What to incorporate | Where in merged base |
|----|---------------|--------------------|----------------------|
| INC-01 | A §3 contract field family | Port the 12 `pr_bot_validation_*` field shapes verbatim into B's `merge-gate-decision.yaml` schema (rename prefix to `pr_bot_validate_*` for sibling-skill namespace consistency) | B §3 / §4 composition table — replace B's sketched field list with A's enumerated shapes |
| INC-02 | A §6 budget composition | `--max-prs` + `--budget-remaining` + §15 T2-midpoint ÷ 6 parallel PRs ≈ 8.7 turns/PR derivation | B §3.2 Wave 0 + §6 trade-offs — adopt A's numerics |
| INC-03 | A §3 PASS/FAIL/PENDING status semantics | A's three-state status check semantics (PASS / FAIL / PENDING) are well-defined; B has same shape but A has more detail on PENDING-initial-state semantics | B §3.3 status check section — fold A's three-state semantics block in |
| INC-04 | A §3 trigger spec | A's CI workflow trigger spec (`pull_request_review` + `pull_request.synchronize`) is identical to B's; A's manual-invocation flag set (`--max-prs`, `--depth`, `--output-dir`) is more enumerated | B §3.4 workflow + §3 CLI flags — adopt A's flag enumeration |
| INC-05 | A §6 trade-off on multi-bot disagreement (partial) | A briefly mentions cross-bot disagreement; merge into a §9 out-of-scope item per INV-005 | B §9 out-of-scope — add "Multi-bot disagreement adjudication (v1.2 scope)" with one-line rationale |

**Changes NOT being made (transparency — debate-rejected):**

| Diff | Non-base Approach | Rationale for Keeping Base |
|------|-------------------|----------------------------|
| X-001 (third mode home) | A's "extend sc:reflect with a third mode" | Debate-decided 95% to B; A conceded under §17.7 Kill #3, PR-vs-work-unit layer separation, and `--recursive` anti-pattern |
| C-002 (reflect changes) | A's reflect contract additions | Falls under X-001 |
| C-004 (gate layer) | A's cond 11 in reflect's §14.5.2 | Falls under X-001; B's GitHub-status-check layer is the structurally-correct gate |
| C-005 (version bump model) | A's bumping reflect contract to incorporate `pr_bot_validation_*` | B's independent sibling versioning is cleaner |
| Single-CLI-surface argument | A's argument that operators learn fewer skills | A's argument has merit; merged proposal adds a one-line cross-reference in reflect's §16 "Related Commands" (low-cost discoverability bridge without surface change) |

**Mechanism-text additions required (from invariant probe warnings):**

| Source | Issue | Required addition |
|--------|-------|-------------------|
| INV-002 | `gh api .../statuses/<sha>` write idempotency across `synchronize` events | Merged §5 must note: GitHub's status API allows multiple writes; only the latest is consumed by branch protection. Repeated writes to the same (sha, context) are idempotent in effect. Cite GitHub REST API spec. |
| INV-003 | `--max-prs` + `--budget-remaining` interaction | Merged §3 must specify: if `--budget-remaining` is below `(--max-prs × 8.7 turns/PR × per-turn-cost-estimate)`, the skill degrades to `--max-prs floor((budget - 5) / 8.7)` with WARN; never errors silently |
| INV-004 | Empty PR set | Merged §3 must specify: zero matching PRs → `status: success`, `prs_processed: 0`, `merge_gate_decision: not_applicable`; NO status check posted (no PR to attach to) |
| INV-005 | Multi-bot disagreement | Merged §9 must list as out-of-scope: "Multi-bot disagreement adjudication (e.g., Augment says CONFIRMED + CodeRabbit says FALSE_POSITIVE on the same file:line) — deferred to v1.2 of the sibling skill; v1.0 processes each bot independently and emits per-bot finding rows in `pr-bot-validation.yaml`, leaving operator to adjudicate" |
| A-001 | gh CLI status-check stability assumption | Merged §5 must surface as a stated assumption + fallback runbook if `gh api .../statuses/` becomes rate-limited or schema-drifts |

## Position-Bias Mitigation

Per the protocol, evaluated both passes (A→B order and B→A order). Both passes agree on the verdict (B wins by margin 1.0%, debate decisive). No criteria disagreements requiring re-evaluation.
