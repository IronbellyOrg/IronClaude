# Refactoring Plan — merge into base V1 (opus:architect)

## Overview
- **Base**: variant-1-opus-architect.md
- **Incorporated**: V2 (presentation + trade-off table), V3 (validation matrix + acceptance tests)
- **Change count**: 7 | **Overall risk**: Low (additive + 2 corrective)

## Planned Changes

### Change #1 — Adopt the 3-term `auto` predicate (CORRECTIVE, from debate C-002)
- **Source**: V2 §4 / V3 §4
- **Target**: base §4.2 `RESOLVE_AUTO`
- **Action**: Remove V1's "Gate 3 / `S2 >= 3 → 2`" standard-band branch. Final predicate: `S6==1 ∨ S5>0 ∨ TCS≥35 → Mode 2; else Mode 1`. Keep S5/S6-before-band ordering (mirrors O1/O2). Update the §4.3 worked examples accordingly (the TCS=40 example still → 2 via the band; add a low-TCS S5>0 example → 2).
- **Rationale**: unanimous debate resolution; S2's ×4 TCS weight already captures breadth. Risk: Low.

### Change #2 — Unify the wrapper-availability fallback ladder (CORRECTIVE, from INV-002 HIGH)
- **Source**: invariant-probe INV-002; V2 §8 / V3 §8
- **Target**: base §4.2 Gate-0 and §8.2 ladder
- **Action**: Resolve the **risk-mode first** (`S6∨S5∨TCS≥35`), THEN apply wrapper availability: a resolved **Mode 2** (fixed `2` OR `auto→2`) with wrapper absent → **manual-HALT (`*-degraded-halt`)**, never inline Mode 1. A resolved **Mode 1** needs no wrapper → Mode 1. Replace V1's coarse "Gate-0: W==false → return 1". Update §8.2 ladder rows for `auto` + `W=false` to mirror the fixed-2 degradation.
- **Rationale**: closes the HIGH finding — high-risk tasklists never silently get the weakest audit. Risk: Low (strictly safer).

### Change #3 — Replace §9 with V3's exhaustive validation matrix (from U-001)
- **Source**: V3 §9 (V1–V16) + §9 mode→assertion map
- **Target**: base §9
- **Action**: Replace V1's prose §9.1–§9.4 with V3's **V1–V16 assertion table** (each pass/fail), the **per-mode active-assertion map** (none: V1–V3; mode1: V1–V6,V9,V11–V14; mode2: V1–V4,V7–V8,V10–V14; degraded: V1,V2,V15,V16), and the rf-qa `task-integrity` integration. Preserve V1's framing that `reflect_post_mode` is the single oracle and the §9.1 mode-specific shape rules (fold into the table). Reconcile field name to `reflect_post_mode` (frontmatter) / `REFLECT_POST_MODE` (BUILD_REQUEST) and the value set to include `halt`, `auto-resolved-1|2`, `2-degraded-halt` per base.
- **Rationale**: V3's matrix is the strongest validation artifact; mechanically testable. Risk: Low.

### Change #4 — Add V2's unified-diff template presentation + trade-off table (from U-002)
- **Source**: V2 §6.1 diff; V2 §8 executor-disjointness table
- **Target**: base §6 (Mode-2 template) + §8
- **Action**: Keep V1's full literal templates (§6.2 Mode-1, §6.3 Mode-2, §6.4 manual, §6.5 auto). ADD V2's unified-diff view of the Mode-2 template vs current `:1994–1999` as a sub-block (implementer aid). ADD V2's 4-row executor-disjointness trade-off table into §8/§4.
- **Rationale**: implementer-friendly; shows the byte-level delta. Risk: Low (additive).

### Change #5 — Add the fixed-1 advisory warning (from INV-003 MEDIUM)
- **Source**: invariant-probe INV-003
- **Target**: base §4 / §10
- **Action**: When fixed `--reflect 1` is selected AND (`S6==1 ∨ S5>0`), emit an advisory build WARNING ("auto would have selected Mode 2; Mode 1 is not executor-disjoint — confirm intent"). Non-blocking; honored.
- **Rationale**: footgun guard without removing operator authority. Risk: Low.

### Change #6 — Reconcile field naming (from C-004)
- **Source**: V3 naming
- **Target**: base §10
- **Action**: BUILD_REQUEST field = `REFLECT_POST_MODE` (mirrors frontmatter `reflect_post_mode`); CLI flag `--reflect`; legacy `POST_REFLECT_GATE` + sibling `POST_REFLECT_MODE` read as deprecated aliases (precedence §10.1). Note the deliberate retirement so no live collision with `POST_REFLECT_MODE`.
- **Rationale**: build/frontmatter symmetry strengthens the single-oracle story. Risk: Low.

### Change #7 — Add INV-004 boundary clarification (from invariant probe)
- **Source**: invariant-probe INV-004
- **Target**: base §4 / §7
- **Action**: State that the auto predicate reads the **resolved** depth band (post-override, post-±4-tiebreaker), so `auto→2 ⟺ resolved-depth==deep ∨ S5>0 ∨ S6==1`, preserving single-producer consistency at the band edge.
- **Rationale**: closes the count_divergence boundary case. Risk: Low.

## Changes NOT Being Made (rejected alternatives)
- **V2 `halt → Mode 1` alias** — REJECTED (C-001/X-002): semantically backwards; base's `halt → byte-identical manual item` retained.
- **V2 `none`/`DISABLED → manual item`** — REJECTED (X-001): contradicts today's behavior; base's `none = no item` retained.
- **V3 build-time `agent_tool_depth` as PRIMARY subagent detection** — REJECTED (C-003/A-002): frame unknown at build; kept only as best-effort defense-in-depth behind the runtime self-check.
- **V3 `TCS≥35 ∨ S6` auto (drops S5)** — REJECTED (C-002): under-audits low-TCS human-decision tasklists.

## Review Status
Auto-approved (non-interactive). Risk summary: 5 additive/clarifying + 2 corrective; no high-risk restructures.
