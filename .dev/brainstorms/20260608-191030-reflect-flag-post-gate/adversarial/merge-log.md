# Merge Log — task-builder `--reflect` POST-gate merged spec

- **Base variant**: Variant 1 (opus:architect) — `variant-1-opus-architect.md`
- **Refactor plan**: `refactor-plan.md` (7 changes, authoritative)
- **Non-base sources**: V2 (opus:refactorer) §6 diff + §8 trade-off table; V3 (haiku:qa) §9 V1–V16 matrix + §13 acceptance tests
- **Merged artifact**: `merged-output.md`
- **Merge date**: 2026-06-08
- **Convergence**: 0.82 (PASS)
- **Overall**: 7/7 changes applied; 0 escalations; structural integrity, internal references, and contradiction re-scan all PASS.

---

## Per-Change Execution Log

### Change #1 — Adopt the 3-term `auto` predicate — **APPLIED**

- **Status**: applied
- **Target**: base §4.2 `RESOLVE_AUTO`, §4.3 worked examples
- **Before**: V1's `RESOLVE_AUTO` had a `Gate 3` standard-band branch with a standalone `S2 >= 3 → return 2` rule plus a `TCS <= 12 → 1` quick-band cut. The middle band (13..34) made a separate breadth decision.
- **After**: Predicate collapsed to the 3-term form `S6==1 ∨ S5>0 ∨ TCS≥35 → Mode 2; else Mode 1`, with S5/S6 evaluated **before** the band (mirrors O1/O2). The `S2≥3` branch and the `TCS≤12` sub-band are removed (S2's ×4 TCS weight already captures breadth, so a broad tasklist already crosses TCS≥35). §4.3 examples updated: Example A (TCS=40 → 2 via band) retained; **Example B added** (S1=3,S2=1,S3=1,S4=0,S5=1,S6=0 → TCS=20 but S5>0 → Mode 2); Example C (clean low-everything TCS=15 → Mode 1) retained.
- **Provenance tag**: `<!-- Source: V2 §4 / V3 §4 auto predicate (3-term), merged per Change #1 (drops V1's S2≥3 standard-band gate) -->`
- **Validation**: re-scan confirmed `S2 ?>= ?3` is **absent** as a predicate term; the 3-term form appears in §4.2, the §4.3 worked-example prose, and the Resolved-Open-Questions row 1. Example B arithmetic verified: `3·3+4·1+2·1+0+5·1+0 = 20`.

### Change #2 — Unify the wrapper-availability fallback ladder (INV-002 HIGH) — **APPLIED**

- **Status**: applied (corrective)
- **Target**: base §4.2 Gate-0 + §8.2 ladder
- **Before**: V1 §4.2 opened with a coarse `Gate 0 — if W == false: return 1` (auto always picked Mode 1 when the wrapper was absent, regardless of risk). V1 §8.2 ladder row: `auto + W=false → §6.2 inline Mode 1 (auto-resolved-1)`.
- **After**: Resolution is now **two-stage**: Stage 1 resolves the *risk-mode* purely from signals (`S6 ∨ S5 ∨ TCS≥35`); Stage 2 applies wrapper availability to the resolved risk-mode. A resolved Mode 2 (fixed `2` OR `auto→2`) with `W=false` → **manual-HALT** (`2-degraded-halt` / `auto-resolved-2-degraded-halt`), **never** inline Mode 1. A resolved Mode 1 needs no wrapper → Mode 1. §8.2 ladder table rewritten with a `Resolved risk-mode` column so `auto`+`W=false` mirrors fixed-2 degradation; the dangerous V1 row is explicitly flagged as replaced in a callout.
- **Provenance tag**: `<!-- Source: invariant-probe INV-002, merged per Change #2 — unified ladder: risk-mode resolved FIRST, then wrapper availability applied identically to fixed-2 and auto-2 -->`
- **Validation**: §4.2 Stage-2 returns `2-degraded-halt` for risk-mode 2 + `W=false`; §8.2 ladder rows for fixed-2 and auto-2 both route to §6.4 manual-HALT under `W=false`. The HIGH finding (high-risk + wrapper-absent → weakest inline audit) is closed. Strictly safer; no regression to the Mode-1 / no-wrapper path.

### Change #3 — Replace §9 with V3's exhaustive V1–V16 validation matrix — **APPLIED**

- **Status**: applied
- **Target**: base §9 (§9.1–§9.4 prose)
- **Before**: V1's §9 was prose: §9.1 replace present-and-penultimate assertion, §9.2 rewrite Critical Rule 19, §9.3 a single FR-9 invariant assertion, §9.4 sentinel preservation.
- **After**: §9 now carries V3's exhaustive **V1–V16 assertion table** (each with pass/fail conditions), the **per-mode active-assertion map** (none: V1–V3; mode1: V1–V6,V9,V11–V14; mode2: V1–V4,V7–V8,V10–V14; degraded/halt: V1,V2,V15,V16 + V3/V4), the rf-qa **MODE-MATCH** `task-integrity` integration, and V3's mismatch acceptance tests (AT-VALIDATION-1, AT-MISMATCH-1). Reconciled to base field names (`reflect_post_mode` frontmatter / `REFLECT_POST_MODE` BUILD_REQUEST) and the base value set `{none,1,2,auto-resolved-1,auto-resolved-2,halt,2-degraded-halt}`. V1's "single oracle" framing kept as the section preamble; V15/V16 + the active-assertion map cover the `halt` / `2-degraded-halt` manual states.
- **Provenance tag**: `<!-- Source: V3 §9 (V1–V16 assertion table) + per-mode active-assertion map + §13 ATs, merged per Change #3 (replaces V1's prose §9.1–§9.4) -->`
- **Validation**: §9 covers all merged-spec modes including `halt`/degraded; the §13 FR→AT matrix added (also Change #3) reconciled to base field names; legacy `:2051` + Critical Rule 19 (`:2108`) anchors retained as the surfaces the matrix replaces.

### Change #4 — Add V2's unified-diff template + executor-disjointness trade-off table — **APPLIED**

- **Status**: applied (additive)
- **Target**: base §6 (Mode-2 template) + §8/§4
- **Before**: V1 §6 had full literal templates (§6.1 none, §6.2 Mode 1, §6.3 Mode 2, §6.4 manual/halt, §6.5 auto) but no byte-level diff view and no trade-off table.
- **After**: V1's full literal templates are **kept verbatim**. Added §6.3.1 — V2's **unified-diff** view of the Mode-2 item vs current `:1994–1999` (implementer aid; shows the Action/Output/Verification delta while Context/HALT/`reflect_post`/depth/`--remediate` are preserved). Added §4.5 — V2's **4-row executor-disjointness trade-off table** (Mode 2/manual vs Mode 1) with the "Mode 1 acceptable when `S6==0 ∧ S5==0 ∧ TCS<35`" note (placed in §4 per the plan's "§8 or §4" option, co-located with the auto FER it justifies).
- **Provenance tags**: `<!-- Source: V2 §6.1 unified-diff presentation, merged per Change #4 (additive implementer aid) -->`; `<!-- Source: V2 §8 executor-disjointness trade-off table, merged per Change #4 -->`
- **Validation**: additive only — no base template text removed; diff block is fenced ```diff and references the retained `:1994-1999` anchor.

### Change #5 — Add the fixed-1 advisory warning (INV-003 MEDIUM) — **APPLIED**

- **Status**: applied
- **Target**: base §4 / §10
- **Before**: V1 honored fixed `--reflect 1` silently, even on regression-class (S6=1) / human-decision (S5>0) tasklists.
- **After**: Added **FR-13** (advisory warning on under-rigorous fixed-1) in §2 and its emission point in **§10.4**: a fixed `--reflect 1` with `S6==1 ∨ S5>0` emits a **non-blocking** build WARNING ("auto would have selected Mode 2; Mode 1 is not executor-disjoint — confirm intent"). Honored (no STOP, no override of operator authority); the §6.2 Mode-1 item and `reflect_post_mode: 1` are unchanged. Added risk **R6** documenting the footgun guard. AT-FR13 added to §13.
- **Provenance tag**: `<!-- Source: invariant-probe INV-003, merged per Change #5 -->`
- **Validation**: warning is scoped to **fixed** `1` only (auto-resolved-1 is exempt since the resolver already chose it); non-blocking; recorded in the build log, not the emitted item.

### Change #6 — Reconcile field naming to `REFLECT_POST_MODE` (C-004) — **APPLIED**

- **Status**: applied
- **Target**: base §10 (and `REFLECT:` references throughout)
- **Before**: V1's BUILD_REQUEST field was `REFLECT:` (precedence step 2 referenced "`REFLECT:` field"; §10.2 schema block used `REFLECT: 2`).
- **After**: BUILD_REQUEST field is **`REFLECT_POST_MODE`** (mirrors frontmatter `reflect_post_mode` for build/frontmatter symmetry). CLI flag remains `--reflect`. Legacy `POST_REFLECT_GATE` + sibling `POST_REFLECT_MODE` are **deprecated aliases** (precedence: explicit `--reflect` flag > `REFLECT_POST_MODE` field > legacy alias map > default 2). §10.1 adds an explicit note that `POST_REFLECT_MODE` is **retired as a live independent field** (survives only as a read-time alias) so there is **no live collision** with the new `REFLECT_POST_MODE`. All V1 `REFLECT:`-field references updated to `REFLECT_POST_MODE:` (frontmatter target comments, §10.1, §10.2, §11 scope).
- **Provenance tag**: `<!-- Source: field naming reconciled to REFLECT_POST_MODE per Change #6 (C-004); precedence per INV-005 -->`
- **Validation**: re-scan confirmed **0** bare `REFLECT:` fields remain; `REFLECT_POST_MODE` appears 15× and `reflect_post_mode` 49×; the retirement note resolves the `POST_REFLECT_MODE` collision (INV-005 deterministic precedence).

### Change #7 — Add INV-004 boundary clarification — **APPLIED**

- **Status**: applied
- **Target**: base §4 / §7
- **Before**: V1's auto predicate read `TCS >= 35` without specifying whether it was raw TCS or the resolved (post-override, post-±4-tiebreaker) band, leaving a count-divergence boundary case at the band edge.
- **After**: Added **§4.4** stating the auto predicate reads the **resolved** depth band, so `auto→2 ⟺ resolved-depth==deep ∨ S5>0 ∨ S6==1`, preserving single-producer consistency at the band edge. Reinforced in §7 ("Boundary consistency (INV-004)") and NFR-5. R2 updated to cite §4.4.
- **Provenance tag**: `<!-- Source: invariant-probe INV-004, merged per Change #7 -->`
- **Validation**: the resolved-band reading guarantees the mode choice and the baked `--depth` cannot diverge at the ±4 tiebreaker edge; consistent with §7's mode-fixes-depth table.

---

## Rejected Changes (base retained — confirmed NOT applied)

| Rejected alternative | Debate ref | Base behavior retained in merge |
|---|---|---|
| `none`/`DISABLED → manual item` (V2) | X-001 | `none` = **no item** (§6.1); `reflect_post:` key omitted. Confirmed: §5.1, §6.1, Resolved-OQ row 2. |
| `halt → Mode 1` alias (V2) | C-001/X-002 | `halt → byte-identical manual item` (§6.4); explicit REJECTED callout in §5.3. |
| Build-time `agent_tool_depth` as PRIMARY subagent detection (V3) | C-003/A-002 | **Runtime self-check** is PRIMARY (FR-11, §6.2, R3); `agent_tool_depth` kept only as best-effort defense-in-depth. |
| `TCS≥35 ∨ S6` auto dropping S5 (V3) | C-002 | S5 retained as a first-class term; Example B demonstrates S5>0 → Mode 2 at low TCS. |

---

## Post-Merge Validation Results

### Structural integrity — PASS

- Heading hierarchy monotonic and well-formed: one `#` title; §1–§13 + `## Resolved Open Questions` at `##`; subsections at `###`; the new diff block at `#### 6.3.1`. No skipped levels.
- Frontmatter retained and updated (`spec_id: …-merged`, merged title, merged `variant:`); `target_surfaces` updated to name `REFLECT_POST_MODE` at `:853`.
- All five provenance header comments present at the top (Provenance / Base / Merge date / Non-base sources / Convergence 0.82 PASS).
- Per-section provenance HTML comments present where non-base strengths were incorporated (§4.2 ×2, §4.3, §4.4, §4.5, §6.3.1, §9, §13, §10).

### Internal references — PASS

- All required real `file:line` anchors retained: `SKILL.md:41` (2×), `:853` (5×), `:1942` (3×), `:1994-1999` (8×), `:2051` (2×), `:2108` (3×), `:2114-2155` (2×).
- Cross-section references resolve: §4.2 → §8.2 ladder; §4.4/§7 ↔ INV-004; §6.5 → §4.2 Stage 2; §9.3 MODE-MATCH → §9.1 V-rows; §10.4 → FR-13/§6.2; §13 AT rows → their FRs.
- Worked-example arithmetic verified independently: Example A=40, B=20, C=15 (all match the spec text).

### Contradiction re-scan (the 4 mandatory consistency checks) — PASS

1. **`none` ≠ manual item** — PASS. `none` is "gate disabled / no item" everywhere (§5.1, §6.1, FR-2); the manual disjoint item is exclusively `halt` / `2-degraded-halt` (§6.4). No conflation; the two grep hits on "none…manual" are the OQ-2 summary and the re-scan note, both stating the distinction, not violating it.
2. **auto predicate is the 3-term form everywhere** — PASS. `S6==1 ∨ S5>0 ∨ TCS≥35` in §4.2 pseudocode, §4.2 defense prose, §4.4 boundary form, and Resolved-OQ row 1. No surviving `S2≥3` predicate term.
3. **fallback ladder is unified** — PASS. §4.2 Stage 1 (risk-mode) precedes Stage 2 (wrapper availability); §8.2 ladder routes both fixed-2 and auto-2 to manual-HALT under `W=false`; the old V1 `auto+W=false→Mode 1` row is explicitly replaced.
4. **field name `REFLECT_POST_MODE` consistent** — PASS. 0 bare `REFLECT:` fields; `REFLECT_POST_MODE` (BUILD_REQUEST) and `reflect_post_mode` (frontmatter) used consistently; `POST_REFLECT_MODE` appears only as a named deprecated alias with an explicit retirement note (no live collision).

### Open-question coverage — PASS

All 10 seed-brief open questions mapped to resolutions in the `## Resolved Open Questions` table (rows 1–10), each citing the merged-spec section that resolves it.

**Verdict: MERGE SUCCESSFUL — 7/7 changes applied, 0 escalations, all structural/reference/contradiction checks PASS.**
