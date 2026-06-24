# Research 02 — Data Flow Tracer: TCS machinery + `auto` FER + depth reconciliation

**Status: Complete**
**Track:** `--reflect auto|1|2` POST-gate refactor (single-track)
**Topic:** TCS internals + how the `auto` predicate (§4) and depth reconciliation (§7) REUSE them (single-producer guarantee — FR-9 / NFR-3 / NFR-5)
**Spec:** `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md`
**Primary code surface:** `src/superclaude/skills/task-builder/SKILL.md` `## Reflect Depth (Deterministic TCS)` — actual content span **`:2114-2154`** (spec `target_surfaces` cites `:2114-2155`; the section ends at `:2154` with the next `---` separator at `:2155`).

> **Citation-line note (S1 freshness):** all `SKILL.md:NNNN` citations below were re-Read/grepped this turn against the live worktree file. The spec's own `:2114-2155` / `:2155` references are 1 line off the actual content (section body ends at `:2154`). The spec inline cites `SKILL.md:2126` for S5, `:2127` for S6, `:2134` for the formula, `:2152` for O4, `:2154` for the tiebreaker — **all confirmed exact** against the live file (see below). Only the section's closing boundary differs.

---

## Topic 1 — The exact S1–S6 frozen-extraction rules (FERs), verbatim

Source: `SKILL.md:2122-2127` (table rows). Quoted verbatim (the FER is the 3rd table column):

- **S1 — Distinct files touched (×3)** — `SKILL.md:2122`
  > "Apply regex `(?:[\w.-]+/)+[\w.-]+\.[\w]+` to the MDTM body, **excluding fenced code blocks and the `### Open Questions` section**; lowercase, strip a trailing `:\d+` line suffix, dedupe by exact string. S1 = size of the deduped set."

- **S2 — Distinct subsystems (×4)** — `SKILL.md:2123`
  > "From the S1 deduped set, take **exactly the first 2 path segments** (or all segments if the path has <2 dir segments) as the subsystem key; dedupe. S2 = count of distinct keys."

- **S3 — FR/NFR count in spec (×2)** — `SKILL.md:2124`
  > "If `--spec` known: count **distinct** `FR-\d+`/`NFR-\d+` IDs in the spec file (an `FR-1` cited 5× counts once). Else 0."

- **S4 — Inter-task dependencies (×2)** — `SKILL.md:2125`
  > "Count occurrences of the fixed dependency-token set `{after Phase \d+, depends_on:}` (case-insensitive, those literal forms only — no open-ended "explicit item ref" inference) across all items."
  > (Trim note at `SKILL.md:2129`: live set is exactly `{after Phase \d+, depends_on:}`; `blockedBy:` and `after N\.\d+` dropped as inert.)

- **S5 — Human-decision / Open-Question-blocked items (×5)** — `SKILL.md:2126`  ← **READ BY THE AUTO PREDICATE**
  > "Count **distinct** `OQ-\d+` (or `Open Question \d+`) tokens that appear in a checklist item's Context line AND have a matching entry under the tasklist's `### Open Questions` section. If a `### Open Questions` section exists but no in-Context index references, fall back to the count of non-empty `### Open Questions` entries."

- **S6 — Risk/refactor class (file-level, 0 or 1) (×4)** — `SKILL.md:2127`  ← **READ BY THE AUTO PREDICATE**
  > "Read the single frontmatter `type:` field, **first stripping any surrounding quotes and leading emoji + whitespace before matching** (so `type: "🔧 Refactor"` normalizes to `Refactor`); S6 = **1 if the normalized value matches a refactor/remediation-class token** (`Refactor`, `Remediation`, or `Code Remediation`, case-insensitive — covering the `🔧`/`♻️`/`🔨 Refactor` and `🔧 Remediation` quoted-emoji variants), **else 0**. A 0-or-1 file-level signal, not a per-item count."

**Signals the `auto` predicate reads (no new extraction — spec §4.1 `merged-requirements.md:247-254`):**
- **S5** (`SKILL.md:2126`) — distinct human-decision/OQ-blocked items, ×5 in TCS.
- **S6** (`SKILL.md:2127`) — file-level refactor/remediation class, 0/1, ×4 in TCS.
- **`TCS` aggregate** (`SKILL.md:2134`) — the full weighted sum (used for the `TCS≥35` band term).
- **`W`** — wrapper-availability boolean (§8 probe; NOT a TCS signal — see Topic 7).

These are the only four inputs to `RESOLVE_AUTO` (spec §4.1 table). All three of S5/S6/TCS are **already extracted today** by the existing depth machinery — the auto rule adds NO new extraction (NFR-1 / NFR-5).

---

## Topic 2 — TCS formula + weights; S2's ×4 confirmed

Source: `SKILL.md:2134` (verbatim):

```text
TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6
```

Weight map (from the table `Weight` column `:2122-2127` AND the formula `:2134` — cross-checked, consistent):

| Signal | Weight | Confirmed at |
|---|---|---|
| S1 (files) | ×3 | `:2122` + `:2134` |
| **S2 (subsystems)** | **×4** | `:2123` + `:2134` |
| S3 (FR/NFR) | ×2 | `:2124` + `:2134` |
| S4 (deps) | ×2 | `:2125` + `:2134` |
| S5 (human-decision) | ×5 | `:2126` + `:2134` |
| S6 (refactor class) | ×4 | `:2127` + `:2134` |

**S2's ×4 weight is confirmed** at `SKILL.md:2123` (table Weight column) and `SKILL.md:2134` (the `4·S2` term). This is the load-bearing fact behind spec **Change #1 / C-002** (`merged-requirements.md:258, 290-294`): V1's standalone `S2 ≥ 3` standard-band auto-gate was **dropped** because S2's ×4 weight in TCS already captures breadth — a genuinely broad tasklist crosses `TCS ≥ 35` and resolves to Mode 2 via the band, so a separate `S2≥3` branch would double-count breadth and is "the only place two implementers could disagree." **The trace confirms the rationale is sound: there is no surviving standalone S2 term in the merged predicate** (§4.2 `merged-requirements.md:266-286` has only the 3-term `S6==1 ∨ S5>0 ∨ TCS≥35`).

Rationale note at `SKILL.md:2137`: "Human-decision (S5) and risk (S6) carry the highest weights because they are exactly the classes that flip reflect to Tier 2" — this is why S5/S6 are ALSO the standalone Mode-2 terms in the auto predicate (not just contributors to TCS).

---

## Topic 3 — Threshold table + the `TCS≥35 → deep` band edge

Source: `SKILL.md:2143-2145` (verbatim band rows):

| TCS range | `--depth` | tier | line |
|---|---|---|---|
| **TCS ≤ 12** | `quick` | Tier 1 only | `:2143` |
| **13 ≤ TCS ≤ 34** | `standard` | Tier 1, escalate-by-rubric | `:2144` |
| **TCS ≥ 35** | `deep` | Tier 2 (forced) | `:2145` |

**Band edges (integer):** `quick` = `[0,12]`; `standard` = `[13,34]`; `deep` = `[35,∞)`.

**The auto predicate's `TCS ≥ 35` term reads EXACTLY the `deep`-band lower edge** (`SKILL.md:2145`). `TCS ≥ 35 ⟺ resolved-depth == deep` (modulo overrides/tiebreaker — see Topics 4, 5). The `quick`/`standard` boundary at 12/13 is **NOT** read by the auto predicate as a mode decision: spec §4.2 (`merged-requirements.md:305-306`) states "There is no separate `quick`/`standard` sub-decision: the dial is monotone with TCS." Everything below 35 (with clean S5/S6) → Mode 1; at/above 35 → Mode 2.

> **Builder note:** the auto predicate collapses BOTH the `quick` and `standard` bands into "Mode 1 → `--depth standard`". So `quick`-band work (TCS≤12) under auto→1 still gets `--depth standard`, NOT `quick` (O4 satisfied by construction — Topic 6). The band table's `quick` row is consumed by the auto path ONLY as "below the deep edge".

---

## Topic 4 — Overrides O1–O4 (verbatim) + alignment with auto Stage-1 risk-mode

Source: `SKILL.md:2149-2152` (verbatim):

- **O1** (`:2149`):
  > "**O1 — Any `S5 > 0` (human-decision item) ⇒ floor `--depth standard`.** A halt-point must get at least the rubric-escalation path (honors `feedback_human_decision_items_must_halt`)."

- **O2** (`:2150`):
  > "**O2 — `S6 = 1` (file-level refactor/remediation `type:`) ⇒ force `--depth deep`.** Matches reflect's own unconditional-T2 rule for regression-class surfaces."

- **O3** (`:2151`):
  > "**O3 — Item-count cap:** if checklist item count > 40 (single-track > 50) ⇒ floor `--depth standard` even if TCS is low (a large tasklist is never "quick" to audit)."

- **O4** (`:2152`):
  > "**O4 — POST-gate depth floor (HARD RULE, no exceptions):** the POST gate depth ∈ {`standard`, `deep`} — it may **NEVER** be `quick`. `--depth quick` disables reflect's regression-escalation rubric, and the POST gate audits executed code, which is exactly where that escalation matters most. When the band yields `quick`, the POST command is emitted with `--depth standard` (the PRE call may still use `quick`, since no diff exists pre-execution)."

**Mapping O1/O2 → auto Stage-1 risk-mode (`S6==1 ∨ S5>0 → Mode 2`), "by construction" (spec §7, `merged-requirements.md:628-631`):**

| Override (depth layer) | Auto Stage-1 term (mode layer) | Alignment |
|---|---|---|
| **O2** `S6=1 ⇒ force deep` (`:2150`) | `if S6==1: risk_mode := 2` (`merged-requirements.md:271`) → Mode 2 → `deep` (§7 row, `:612`) | **Agree by construction**: O2 forces `deep`; auto forces Mode 2 whose fixed depth IS `deep`. Same outcome, two layers. |
| **O1** `S5>0 ⇒ floor standard` (`:2149`) | `elif S5>0: risk_mode := 2` (`merged-requirements.md:272`) → Mode 2 → `deep` (§7) | Auto is **STRICTLY STRONGER** than O1 for the auto path: O1 only floors to `standard`, but auto sends S5>0 to Mode 2 = `deep`. Not a contradiction — O1 is a *floor* (≥ standard); `deep` satisfies it. (Spec §7 `:628-631`: "O1/O2 and the auto FER agree by construction.") |
| **O3** item-count cap (`:2151`) | (no direct auto term) | O3 still governs the **baked `{DEPTH}` passthrough** for `halt` mode and the wrapper-passthrough value (spec §7 `:631`: "O1/O2/O3 are NOT removed"). It does NOT change the auto mode choice (auto reads only S5/S6/TCS). |
| **O4** POST never `quick` (`:2152`) | structurally satisfied for modes 1/2 (Topic 6) | See Topic 6 — "fate of O4". |

**Key trace finding:** O2 (`S6=1 ⇒ deep`) and the auto `S6==1 → Mode 2` are the SAME decision expressed at two layers (depth-layer vs mode-layer); since Mode 2's fixed depth IS `deep` (§7 `:612`), they produce the identical `--depth`. Likewise O1's `S5>0` floor is subsumed by auto's stronger `S5>0 → Mode 2 → deep`. This is the structural basis for the single-producer guarantee: the auto rule is "a thin band-reading wrapper over [the depth machinery], never a competing model" (spec §7 `:630`).

---

## Topic 5 — The ±4 tiebreaker + §4.4 "auto reads the RESOLVED band" (INV-004 single-producer property)

Source: `SKILL.md:2154` (verbatim):
> "Within ±4 TCS of a band edge (the span an S2 ±1 disagreement can traverse), the orchestrator may apply one bounded inference — "are these N FER-distinct dirs truly distinct *logical* subsystems?" — recorded as `tcs_boundary_inference: {applied, from, to, reason}` in the sign-off block for auditability. Outside the ±4 windows, no inference is permitted."

**What ±4 means concretely:** within ±4 of an edge (e.g. for the `deep` edge at 35, the window is TCS ∈ [31, 39]), the orchestrator MAY apply ONE bounded inference about whether N FER-distinct dirs are truly distinct logical subsystems (i.e., it can nudge S2, which has ×4 weight — a ±1 S2 change = ±4 TCS, exactly the window width). The adjustment is recorded as `tcs_boundary_inference`. Outside the window, NO inference — pure arithmetic.

**§4.4 — auto reads the RESOLVED band (spec `merged-requirements.md:359-375`, INV-004):**
> "The auto predicate's `TCS ≥ 35` term reads the **resolved** depth band — i.e., the band after the overrides (O1/O2/O3) and after the existing bounded **±4 TCS tiebreaker** (`SKILL.md:2154`) have been applied — **not** the raw arithmetic TCS."

Equivalence baked by §4.4 (`merged-requirements.md:368`):
```text
auto → 2  ⟺  resolved-depth == deep  ∨  S5 > 0  ∨  S6 == 1
```

**Why the auto mode choice and the baked `--depth` CANNOT diverge at the band edge (INV-004 single-producer property):**

The naïve risk is a count-divergence at the edge: suppose raw `TCS = 33`, and the tiebreaker (an S2 +1 logical-subsystem judgement) nudges it to `37`. If the **depth derivation** used the *resolved* 37 (→ `deep`) but the **auto predicate** read the *raw* 33 (→ below 35 → Mode 1 → `standard`), you'd get `reflect_post_mode: auto-resolved-1` (depth `standard`) emitted alongside a depth machinery that thinks `deep` — TWO producers, drift, FR-9 violation.

§4.4 closes this by **forcing the auto predicate to read the SAME resolved number the depth derivation produces** (post-O1/O2/O3, post-±4 tiebreaker). Both the mode choice and the baked `--depth` then consume ONE resolved band value. Result (spec `:371-375`): "there is no input where the tiebreaker nudges TCS across 35 for the depth derivation but leaves the auto choice on the other side." This is the single-producer property (FR-9 `merged-requirements.md:159-164`; NFR-5 `:225-229`): one arithmetic source (resolved TCS), one decision point (A.9), consumed by mode AND depth identically.

**Builder implication (depth-reconciliation edit item):** the edit must specify that `RESOLVE_AUTO`'s `TCS` input is the **post-tiebreaker, post-override resolved TCS/band**, NOT the raw `3·S1+...` sum. If the builder feeds raw TCS to the auto predicate but resolved TCS to the depth derivation, INV-004 is violated. The single producer at A.9 must compute the resolved band ONCE, then feed it to both.

---

## Topic 6 — §7 depth table mapped onto current derivation; "fate of O4"

§7 depth table (spec `merged-requirements.md:609-615`):

| Mode | POST `--depth` | Source | Maps to current derivation as |
|---|---|---|---|
| `1` (fixed) | `standard` | fixed by mode | **MODE-derived** — bypasses the TCS band entirely; pinned `standard`. |
| `2` (fixed) | `deep` | fixed by mode | **MODE-derived** — pinned `deep`. |
| `auto→1` | `standard` | inherited from resolved Mode 1 | **MODE-derived** (mode resolved from TCS, but depth then fixed by the mode). |
| `auto→2` | `deep` | inherited from resolved Mode 2 | **MODE-derived**. |
| `halt` / `2-degraded-halt` | `max(TCS-band, standard)` | retained manual item keeps the **existing** TCS-derived depth (`SKILL.md:1996, 2152`) | **TCS-derived** — the ONLY mode that runs the current `:2143-2145` band + O4 floor at runtime. |

**Key trace finding for the builder:** depth is **MODE-derived for fixed `1`/`2` and `auto→{1,2}`** (the mode pins it: 1→standard, 2→deep), and **TCS-derived ONLY for `halt` / `2-degraded-halt`** (which preserves the current `:1996` baked-`{DEPTH}` behavior = `max(TCS-band, standard)` via O4). The current TCS→depth band table (`:2143-2145`) and the ±4 tiebreaker (`:2154`) continue to compute the **value baked into `{DEPTH}`** for the `halt` path and the wrapper passthrough; for modes 1/2 the band is consumed ONLY to pick the mode (via the `TCS≥35` term), after which the depth is the mode's fixed value.

**Fate of O4 (`SKILL.md:2152`) — preserved + strengthened (spec §7 `merged-requirements.md:617-625`):**

1. **Fixed `1`/`2` and `auto→{1,2}` — O4 structurally satisfied / unreachable as a live floor** (`:619-621`): depth is `standard` or `deep` "by construction — O4's 'never `quick`' floor is automatically satisfied (no mode yields `quick`). O4 becomes a redundant-but-true invariant for these paths; rf-qa still asserts it (a `quick` POST depth on any non-`halt` mode = MALFORMED)." So O4 is NOT deleted — it's structurally unreachable for these modes but still ASSERTED by rf-qa as an invariant.
2. **Retained `halt` / `2-degraded-halt` — O4 applies exactly as today** (`:622-623`): "the manual command floors at `standard` when the band yields `quick`." This is the live `SKILL.md:1996` behavior (`{DEPTH}` floored at `standard` per O4) preserved byte-for-byte.
3. **O1/O2 expressed at the mode layer for `auto`** (`:624-625`): Stage-1 returns 2 for S5>0 or S6=1, and Mode 2 is `deep` — so O1/O2 and the auto FER "agree by construction; the depth machinery remains the single producer and the auto rule is a thin band-reading wrapper over it."
4. **O1/O2/O3 NOT removed** (`:631`): they "continue to govern the baked `{DEPTH}` passthrough for the `halt` mode and the wrapper-passthrough depth value."

**Summary of O4 fate (verbatim spec phrasing, `:617`):** O4 is "**preserved and strengthened**, never deleted." Strengthened because for modes 1/2 it's now *structurally* impossible to emit `quick` (the mode fixes the depth above `quick`), AND rf-qa asserts it as a MALFORMED check; for `halt` it's the same floor as today.

---

## Topic 7 — §8.1 wrapper-availability probe `W` (build-time boolean feeding RESOLVE_AUTO Stage 2)

Source: spec §8.1 (`merged-requirements.md:655-660`):
> "The builder probes wrapper availability with a frozen check: the `reflect` subcommand is registered (`superclaude reflect --help` exits 0 / `superclaude --help` lists `reflect`). The probe result `W ∈ {true,false}` is computed once and reused by §4 (`auto`) and §8. The probe is read-only and adds no state."

**`W` definition (build-time boolean):**
- `W = true` ⟺ `superclaude reflect --help` exits 0 (equivalently `reflect` subcommand registered / listed by `superclaude --help`).
- `W = false` otherwise.

**Where `W` feeds RESOLVE_AUTO (spec §4.2 Stage 2, `merged-requirements.md:276-285`):** Stage 1 resolves the *risk-mode* purely from S5/S6/TCS (wrapper-independent). Stage 2 then applies `W`:
- `risk_mode == 1` → return `1` (Mode 1 needs no wrapper — emitted unchanged regardless of `W`).
- `risk_mode == 2 ∧ W == true` → return `2` (shell-out).
- `risk_mode == 2 ∧ W == false` → return `"2-degraded-halt"` (manual-HALT, preserves executor-disjointness, NEVER silent inline Mode 1 — the INV-002 fix).

`W` is computed ONCE at A.9 and reused by both the auto resolver (§4) and the fixed-`2` fallback ladder (§8.2 `merged-requirements.md:670-679`) — so fixed-`2`+`W=false` and `auto→2`+`W=false` degrade identically (unified ladder, INV-002).

**OUT OF SCOPE (sibling spec):** the `superclaude reflect run` **wrapper itself** is out of scope for this track (spec `out_of_scope:` `merged-requirements.md:19`, and §11 `:883`). This track only (a) PROBES `W` at build time and (b) consumes it in RESOLVE_AUTO / the fallback ladder. The builder edit must NOT attempt to build/modify the wrapper — only emit the probe + consume the boolean.

---

## Topic 8 — Reproduce §4.3 worked examples A/B/C; CHECK against the traced formula/table

The formula used (`SKILL.md:2134`): `TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6`.
The band edge (`SKILL.md:2145`): `TCS ≥ 35 → deep`.
The predicate (spec §4.2): Stage 1 `S6==1 → 2; elif S5>0 → 2; elif TCS≥35 → 2; else 1`. Stage 2 applies `W`.

### Example A — high TCS, clean signals (spec `merged-requirements.md:312-327`)
Inputs: S1=6, S2=2, S3=4, S4=3, S5=0, S6=0, W=true.

**Independent recompute against `:2134`:**
```
TCS = 3·6 + 4·2 + 2·4 + 2·3 + 5·0 + 4·0
    = 18 + 8 + 8 + 6 + 0 + 0
    = 40
```
✅ **Matches spec's 40** (`:317-318`).
RESOLVE_AUTO(40,0,0,true): Stage 1 → S6==0, S5==0, **40 ≥ 35** → risk_mode=2. Stage 2 → W=true → **return 2**.
✅ **Matches spec** (`auto-resolved-2`, `:319-324`).
**Band cross-check (`:2145`):** TCS=40 → `deep`. Mode 2 fixed depth = `deep` (§7). **Auto-mode and baked depth agree** — single-producer holds. ✅ No discrepancy.

### Example B — low TCS but a human-decision item (spec `merged-requirements.md:329-344`)
Inputs: S1=3, S2=1, S3=1, S4=0, S5=1, S6=0, W=true.

**Independent recompute:**
```
TCS = 3·3 + 4·1 + 2·1 + 2·0 + 5·1 + 4·0
    = 9 + 4 + 2 + 0 + 5 + 0
    = 20
```
✅ **Matches spec's 20** (`:334-335`).
RESOLVE_AUTO(20,1,0,true): Stage 1 → S6==0, **S5==1 > 0** → risk_mode=2 (S5 fires BEFORE the band). Stage 2 → W=true → **return 2**.
✅ **Matches spec** (`auto-resolved-2`, `:336-344`), even though TCS=20 < 35.
**Band cross-check:** raw TCS=20 → `standard` band; BUT S5>0 triggers O1 (floor standard) AND auto Stage-1 S5 term → Mode 2 → `deep`. The auto path's depth is MODE-derived (`deep`), NOT band-derived — this is the intended divergence between *band* and *mode-fixed depth* for the S5 case, and it is consistent: Mode 2 ⟹ `deep`, which satisfies O1's `≥ standard` floor. ✅ No discrepancy (the depth value comes from the mode, not the band, per §7).

### Example C — clean low-everything (spec `merged-requirements.md:346-357`)
Inputs: S1=3, S2=1, S3=0, S4=1, S5=0, S6=0, W=true.

**Independent recompute:**
```
TCS = 3·3 + 4·1 + 2·0 + 2·1 + 5·0 + 4·0
    = 9 + 4 + 0 + 2 + 0 + 0
    = 15
```
✅ **Matches spec's 15** (`:350`). (Note: spec writes the line as `3·3 + 4·1 + 0 + 2·1 + 0 + 0 = 9 + 4 + 2 = 15`, omitting the zero terms — arithmetic identical.)
RESOLVE_AUTO(15,0,0,true): Stage 1 → S6==0, S5==0, **15 not≥35** → risk_mode=1. Stage 2 → risk_mode==1 → **return 1**.
✅ **Matches spec** (`auto-resolved-1`, `:351-357`).
**Band cross-check (`:2143-2144`):** raw TCS=15 → `standard` band (13≤15≤34). Mode 1 fixed depth = `standard` (§7). **Agree** — and note TCS=15 is NOT in the `quick` band, but even if it were (≤12), auto→1 still pins `standard`, satisfying O4. ✅ No discrepancy.

**DISCREPANCY SCAN RESULT:** All three worked examples reproduce **exactly** against the live formula (`SKILL.md:2134`) and band table (`SKILL.md:2143-2145`). No arithmetic or resolution discrepancies found. FR-5 determinism is de-risked: a second implementer using the traced FERs computes identical TCS and identical mode for A/B/C.

---

## Summary (for the builder)

**Single-producer guarantee — the spine of this track.** The auto predicate introduces NO second
complexity model: it reuses the SAME S5 (`SKILL.md:2126`), S6 (`SKILL.md:2127`), and resolved
TCS (`SKILL.md:2134`) the depth machinery already computes. One arithmetic source, one decision
point (A.9), consumed by both the mode choice AND the baked `--depth` (FR-9, NFR-3, NFR-5).

**Exact facts the builder needs for the two edit items:**

1. **Formula (`:2134`):** `TCS = 3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6`. **S2's ×4 weight**
   (`:2123`, `:2134`) is the verified basis for dropping V1's standalone `S2≥3` auto-gate
   (Change #1 / C-002) — breadth is already counted; the merged predicate is the 3-term form
   only.
2. **Band edge (`:2145`):** `TCS ≥ 35 → deep`. This is the exact threshold the auto `TCS≥35`
   term reads. (`quick` ≤12 `:2143`; `standard` 13-34 `:2144`.)
3. **Auto predicate (spec §4.2):** Stage 1 `S6==1 ∨ S5>0 ∨ TCS≥35 → Mode 2; else Mode 1`
   (S5/S6 before the band, mirroring O2/O1). Stage 2 applies `W`: risk-mode 1 → Mode 1
   regardless of `W`; risk-mode 2 + `W` → Mode 2 (shell-out); risk-mode 2 + ¬`W` →
   `2-degraded-halt` (manual-HALT, never silent inline Mode 1 — INV-002).
4. **Depth is MODE-derived for fixed `1`/`2` + `auto→{1,2}`** (1→standard, 2→deep), and
   **TCS-derived ONLY for `halt`/`2-degraded-halt`** (`max(TCS-band, standard)`, the live
   `:1996` baked-`{DEPTH}` behavior). **O4 fate (`:2152`):** preserved + strengthened —
   structurally unreachable (no `quick`) for modes 1/2 but still rf-qa-asserted; applies
   as-today for `halt`. **O1/O2/O3 NOT removed** — they govern the `halt`/wrapper-passthrough
   `{DEPTH}` and align with the auto FER by construction (O2≡auto-S6, O1 subsumed by stronger
   auto-S5→deep).
5. **INV-004 (depth-reconciliation edit item — CRITICAL):** RESOLVE_AUTO's `TCS` input MUST be
   the **resolved** band — post-O1/O2/O3, post-±4 tiebreaker (`:2154`) — NOT raw arithmetic
   TCS. `auto→2 ⟺ resolved-depth==deep ∨ S5>0 ∨ S6==1`. Feeding raw TCS to the predicate but
   resolved TCS to the depth derivation is the one way to create two producers / band-edge
   drift. The builder must compute the resolved band ONCE and feed BOTH consumers.
6. **`W` probe (§8.1):** build-time boolean = `superclaude reflect --help` exits 0 / `reflect`
   subcommand registered. Computed once at A.9, reused by §4 + §8. The wrapper ITSELF is OUT OF
   SCOPE (sibling spec); this track only probes + consumes `W`.

**Worked-example verification (FR-5 de-risk):** Examples A (TCS=40→Mode 2), B (TCS=20, S5=1→
Mode 2 via S5), C (TCS=15→Mode 1) all **reproduce exactly** against the live `:2134` formula and
`:2143-2145` band. **No discrepancies.** Each cross-checks clean against the §7 mode→depth table
(auto-mode and baked depth agree by construction in all three).

**Citation hygiene note for downstream researchers:** the spec's `target_surfaces` cites the TCS
section as `:2114-2155`; the live content span is `:2114-2154` (next `---` at `:2155`). All
inline spec citations (S5 `:2126`, S6 `:2127`, formula `:2134`, O4 `:2152`, tiebreaker `:2154`)
are exact against the live worktree file.
