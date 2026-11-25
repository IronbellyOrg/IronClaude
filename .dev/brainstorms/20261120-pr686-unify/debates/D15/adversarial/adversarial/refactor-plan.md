# Refactoring Plan: D15

## Overview
- Base: Variant 1 (OURS position paper) plus the Round 1 and Round 2 texts as the evidence of the debate.
- Incorporated: Variant 2 strengths (listed in base-selection.md), the gap decisions G-1 to G-9 from `rounds/round2-rebuttal-1-ours.md` and `rounds/round2-rebuttal-2-clay.md`, and the fault-finder conditions from `invariant-probe.md`.
- Output: one merged position `merged-d15-position.md` (principles, build order, gap decisions, invariant conditions, open owner decisions). The element-by-element table with carrier PRs is written in `VERDICT.md` (single authoring location).
- Risk: Low (document merge).
- Approval: auto-approved.

## Planned Changes
1. **Build order (incorporate CLAY substrate).** Source: `rounds/round2-rebuttal-2-clay.md` A3.1. Add: substrate (runner, `refuse(argv)`, JSON contract, state lock, state-folder path map INV-006), then merge path as one tested unit, then other verbs in any order. Risk Low.
2. **Test plan (incorporate CLAY T1-T13).** Source: CLAY A3.2, OURS A1 W3, INV-009. Add: base plan T1-T13 with U and K registers; six logic rewrites (T1, T3, T4, T8, T10, T11); T12 rewritten for hand-back; setup step approving the throwaway issue on the rows that start a worker; counts stated from the design (13 T, 60 U, 28 K rows per INV-009). Risk Low.
3. **Gap decisions G-1 to G-9.** Source: both Round 2 files. Record per gap the agreed outcome and the open owner decisions: plan_depth default (G-2), hand-back round-start mechanism (G-3), naming scope (G-4), audit escalation channel (G-9 part 1), N6 and interrupt confirmations. Risk Low.
4. **Invariant conditions.** Source: `invariant-probe.md` HIGH items. Add as mandatory conditions: C-INV-1 (INV-001, INV-002) a hand-back waiting step is excluded from the in-flight count or has an expiry, and something wakes the coordinator after a re-approval; C-INV-2 (INV-003) the per-repo config is made tamper-protected or the controls it shapes fail closed on weakening values; C-INV-3 (INV-004) the post-merge close needs a stated authority (per-PR go or an explicit closeout grant) and the `Fixes` line bypass is stated; plus MEDIUM items as spec lines (INV-005 to INV-014, INV-016, INV-017). Risk Medium (new requirements, no source rule).
5. **Wording rule.** Source: D06 item 10, A-004. Every control is written "narrows", with the falsifiers of INV-015, INV-016, INV-018, INV-019. Risk Low.

## Changes NOT Being Made
- Adopt the Clay set as the base "as built" (CLAY Round 1): withdrawn by CLAY; the base carries contested rules (C-006).
- Keep `plan_tier` (Clay's 5.8): replaced by a plain `plan_depth` key (CLAY G-2), not dropped (OURS) and not kept as a tier-to-depth table.
- A new chat "go" per hand-back round (OURS G-3): rejected as a second mechanism with no source; the start gate (approval) decides, owner picks option (a) or (b).
- Report-line-only audit escalation (OURS G-9): replaced by the notice step as D11 adopts it, cap key default 0.

## Risk Summary
All changes are text; main risk is that the four HIGH conditions are new requirements with no owner or Clay source (marked as recommendations).

## Review Status
auto-approved (unattended)
