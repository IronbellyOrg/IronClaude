# Research 04 — Flag Plumbing, Precedence, Knob Reconciliation, Frontmatter, Advisory WARNING

**Status: Complete**

Research topic: Integration Points for the `--reflect auto|1|2` POST-gate refactor.
Spec: `.dev/brainstorms/20260608-191030-reflect-flag-post-gate/merged-requirements.md` (§5, §10)
Target file: `src/superclaude/skills/task-builder/SKILL.md` (2308 lines; absolute path
`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/src/superclaude/skills/task-builder/SKILL.md`)

> SoT note: edits land in `src/superclaude/skills/task-builder/SKILL.md`, then `make sync-dev`. NEVER stage `.claude/` mirrors.

---

## 0. Collision check (INV-005) — grep result (REQUESTED VERBATIM)

Grep over the **live** SKILL.md (case-insensitive, all variants):

```
$ grep -ni "post_reflect\|reflect_post\|--reflect\b\|reflect_gate" src/superclaude/skills/task-builder/SKILL.md
853:    POST_REFLECT_GATE: ENABLED
1423: ...(prose ref to A.9 `POST_REFLECT_GATE`)
1942:reflect_post: ""   # PENDING sentinel ...
1996: ...(/sc:reflect --mode post ... command, {DEPTH}/{SPEC_PATH} placeholders)
1997-1999: ...(reflect_post: PENDING item Output/Verification/Completion gate)
2051: ...(validation checklist: POST reflect item positioned penultimate when POST_REFLECT_GATE ENABLED)
2108: ...(Critical Rule #19: POST reflect gate in generated task files; POST_REFLECT_GATE: ENABLED)
```

Targeted grep for the two candidate-collision tokens:

```
$ grep -n "POST_REFLECT_MODE\|REFLECT_POST_MODE" src/superclaude/skills/task-builder/SKILL.md
(no output — neither token is present)
```

**FINDING (INV-005):**
- `POST_REFLECT_MODE` does **NOT** exist anywhere in this SKILL.md. The sibling wrapper task
  `TASK-RF-20260608-185553` (which the brief says proposed a `POST_REFLECT_MODE ∈ {wrapper, halt}`
  field) is **built but NOT merged into this SKILL.md** — there is no live `POST_REFLECT_MODE` field
  to collide with.
- `REFLECT_POST_MODE` (the new BUILD_REQUEST field this spec introduces) does NOT exist yet either.
- The only live POST gate field today is the **binary** `POST_REFLECT_GATE: ENABLED` at `:853`.
- Spec §10.1 (lines 818-826) confirms the design intent: `POST_REFLECT_MODE` is **retired as a
  live independent field** — it survives only as a **read-time alias** in the §5 map (precedence
  step 3). So even if the sibling later merges it, the spec resolves it deterministically (new
  `REFLECT_POST_MODE` wins; legacy ignored with a build-log note). **No live collision exists or
  is created.** The builder may implement `REFLECT_POST_MODE` as a fresh field with zero rename
  conflict.

---

## 1. The `--spec`/`SPEC_PATH` precedent — how a flag is parsed-and-threaded TODAY

This is the **model pattern** for `--reflect`/`REFLECT_POST_MODE`. Four touchpoints:

**(a) Flag declaration / input surface — `SKILL.md:41`:**
> 5. **--spec <path> — driving spec/PRD/TDD** (optional) — … When supplied it is threaded into
> the PRE reflect gate's coverage audit (the `--mode pre --spec <path>` call at A.10.7) and baked
> into the templated POST reflect item's command … **Resolved in priority order: explicit `--spec
> <path>` → an `@file` reference in the GOAL → a `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST
> file → none.** Written to the generated tasklist frontmatter as `spec_path:`.

**(b) Parse/resolve site — A.2 Parse & Triage, `SKILL.md:201`:**
> - **SPEC_PATH**: The driving spec/PRD/TDD path, resolved in priority order (explicit `--spec
> <path>` → an `@file` reference in GOAL → a `SPEC:`/`PRD:`/`TDD:` field in BUILD_REQUEST → none);
> written to the generated tasklist frontmatter as `spec_path:`, **threaded into the A.10.7 PRE
> call's `--spec` and the POST item's `{SPEC_PATH}` placeholder**

So SPEC_PATH is resolved ONCE in A.2 (the parse/triage stage), with an explicit 4-step priority order.

**(c) BUILD_REQUEST field — `SKILL.md:854`:** `SPEC_PATH: <spec_path or NONE>` (sub-field under the POST gate block).

**(d) Threading to consumers:**
- PRE consume site — **A.10.7 PRE Reflect Gate** (`SKILL.md:1407-1429`): `--mode pre --remediate`
  invocation; SPEC_PATH flows in as `--spec`.
- POST consume site — the templated POST item at `SKILL.md:1996`: `... [--spec {SPEC_PATH}] ...`
  placeholder resolved at A.9.
- Frontmatter write — `SKILL.md:1933`: `spec_path: "[driving spec/PRD/TDD path resolved at A.2, or empty if none]"`

**Generalized precedent shape (for `--reflect`):** declare flag at the input-surface section (`:35-41`)
→ resolve once at the parse stage with an explicit priority order → carry as a BUILD_REQUEST field
(`:853` block) → consume at A.9 (POST producer) → write a frontmatter field. The `--reflect` design
(spec §10.1) places the **resolve/parse at the flag-resolution stage** and the **consume at A.9**
(co-located with `:853`), which is the same shape with the consume site shifted from A.2/A.10.7 to A.9.

### Second precedent — `EXECUTION_CONTEXT_REQUIREMENTS` (API-001-M2), an OPTIONAL/defaulted/MALFORMED-guarded BUILD_REQUEST field

`SKILL.md:831-851`. Structural template the `REFLECT_POST_MODE` field should imitate:
- **Optional with an explicit default-on-omission:** "Omission of this field implies AUTO." → mirror:
  "default `2` when absent" (spec §10.2 line 833).
- **Closed value set:** `{AUTO, REQUIRED, SUPPRESS}` → mirror: `{none, 0, 1, 2, auto}`.
- **Strict additivity / back-compat:** "Strictly additive — when absent or AUTO, the M1-frozen
  15-field BUILD_REQUEST behavior is preserved byte-identical." → mirror NFR-2 byte-for-byte
  reversibility via the `halt` position.
- **MALFORMED guard with retry:** "Failure mode: MALFORMED retry max-2 (Critical Rule #12 and the
  MALFORMED flow at SKILL.md A.9 mediation)" → the new field's invalid/contradictory values route
  through the same A.9 MALFORMED max-2 retry flow (`:948`).

These two precedents give the builder a copy-pattern for BOTH the parse/precedence item (use `--spec`)
and the schema/MALFORMED item (use `EXECUTION_CONTEXT_REQUIREMENTS`).

---

## 2. Current BUILD_REQUEST POST gate block (verbatim) + §10.2 schema change

**CURRENT — `SKILL.md:853-856` (verbatim):**

```text
    POST_REFLECT_GATE: ENABLED
      SPEC_PATH: <spec_path or NONE>
      DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4 — never quick
      TASK_FILE: ${TASK_FILE}
```

**NEW — §10.2 schema change (spec lines 828-840, verbatim block to install at `:853`):**

```text
REFLECT_POST_MODE: 2          # one of: none | 0 | 1 | 2 | auto   (default 2 when absent)
  SPEC_PATH: <spec_path or NONE>     # threaded to Mode 1 inline / Mode 2 wrapper (§12)
  # DEPTH is no longer an author-settable POST sub-field: it is mode-derived
  # (1→standard, 2→deep, halt→max(TCS,standard)) — single producer, §7.
  TASK_FILE: ${TASK_FILE}
  # Accepts deprecated aliases POST_REFLECT_MODE: wrapper(≡2)|halt(→halt position)
  #   and POST_REFLECT_GATE: ENABLED|DISABLED(≡none) — §5 map, precedence step 3.
```

**Schema-edit-item delta (for the builder):**
1. Replace `POST_REFLECT_GATE: ENABLED` (primary) → `REFLECT_POST_MODE: 2` (value set `none|0|1|2|auto`, default 2).
2. **Retire the `DEPTH:` sub-field** — DEPTH is no longer author-settable; it is mode-derived
   (§7 table: 1→standard, 2→deep, halt/`2-degraded-halt`→`max(TCS-band, standard)`). Single producer.
3. Keep `SPEC_PATH:` and `TASK_FILE:` sub-fields unchanged.
4. Add the **deprecated-alias acceptance note** as a comment (the last two `#` lines above): legacy
   `POST_REFLECT_MODE: wrapper|halt` and `POST_REFLECT_GATE: ENABLED|DISABLED` are honored via the §5
   map at precedence step 3, then deprecated (spec lines 842-843).
5. Field name **deliberately mirrors** frontmatter `reflect_post_mode` (Change #6 / C-004, spec lines 818-826).

---

## 3. §5 Knob reconciliation — dial, old→new total map, retained `halt`

### §5.1 The dial (spec lines 405-414) — dial position → meaning → emitted item

| Dial position | Meaning | Emitted item (§6) |
|---|---|---|
| `none` (`0`) | gate disabled | none (§6.1 — NO item) |
| `1` | inline same-session, `--depth standard`, audit-only, NOT executor-disjoint | §6.2 |
| `2` (default) | wrapper shell-out, `--depth deep --remediate`, executor-disjoint | §6.3 |
| `auto` | builder resolves 1 or 2 per §4 | §6.2 or §6.3 (+ `auto-resolved-{1,2}` frontmatter) |
| `2-degraded-halt` | (derived only, §8 / §4.2 Stage 2) wrapper absent under resolved Mode 2 | §6.4 manual-HALT |
| `halt` | (derived only) retained manual-HALT via legacy `POST_REFLECT_MODE: halt` | §6.4 manual-HALT |

### §5.2 old→new total map (spec lines 416-429) — every legacy cell → one `m`

Legacy surface: `POST_REFLECT_GATE ∈ {ENABLED, DISABLED}` (`SKILL.md:853`; absence ⇒ ENABLED for built
tasks today) × sibling's `POST_REFLECT_MODE ∈ {wrapper, halt}` (default `halt`). Both are now
deprecated read-only aliases. Total map:

| Legacy `POST_REFLECT_GATE` | Legacy `POST_REFLECT_MODE` | New effective `m` | Emitted item | Notes |
|---|---|---|---|---|
| `DISABLED` | (any) | `none` | §6.1 (no item) | direct old→new; gate off, no item |
| (absent / `ENABLED`) | `halt` (or absent) | `halt` | §6.4 manual-HALT | **Back-compat anchor**: maps to **retained manual-HALT** (`reflect_post_mode: halt`), NOT wrapper Mode 2; preserves `SKILL.md:1994-1999` byte-for-byte (§5.3). |
| (absent / `ENABLED`) | `wrapper` | `2` | §6.3 shell-out | sibling's automated path == Mode 2 |
| explicit `--reflect <v>` present | (any legacy) | `<v>` | per `<v>` | **`--reflect` always wins**; legacy aliases ignored + one-line build-log note |

### §5.3 Retained `halt` position + REJECTED V2 alternative (spec lines 431-451)

- `halt` is a **derived** position, NOT selectable via the numeric `--reflect 1|2` surface; reachable via:
  (i) legacy `POST_REFLECT_MODE: halt` (sibling default), or (ii) a resolved Mode 2 (fixed `--reflect 2`
  OR `auto→2`) when the wrapper is **absent** (§8 → `2-degraded-halt`).
- `halt` emits the **current `SKILL.md:1994-1999` manual fresh-session item verbatim** with
  `reflect_post_mode: halt`.
- **REJECTED alternative (C-001/X-002):** V2 proposed `halt → Mode 1` (inline). REJECTED — semantically
  backwards: `halt` means "keep the manual *disjoint* gate," and Mode 1 is the one NON-disjoint mode.
  **Base mapping kept: `halt → byte-identical manual item`, NOT Mode 1.**

---

## 4. §10.1 Precedence — parse site, consume site, 4-step order, build-log note

**Parse site:** `--reflect` is parsed at the **BUILD_REQUEST / flag-resolution stage**.
**Consume site:** **A.9** (the POST gate logic site, co-located with the legacy gate field at
`SKILL.md:853`). Mode resolution (incl. `auto`→§4 and wrapper-probe→§8) happens **once** at A.9 (FR-9).

**Resolution order (highest wins, first match) — spec lines 808-812:**
1. explicit `--reflect <value>` flag on the build invocation (`value ∈ none|0|1|2|auto`);
2. `REFLECT_POST_MODE:` field in a BUILD_REQUEST file (new field, `none|0|1|2|auto`);
3. **legacy §5 alias map**: `POST_REFLECT_GATE × POST_REFLECT_MODE → m` (consulted only if 1–2 absent;
   both legacy fields are deprecated aliases, NOT surviving inputs);
4. **default `2`**.

**Build-log note (spec lines 814-815):** when a higher-precedence source is present, the lower legacy
alias fields are ignored and a one-line note is written to the build log:
`--reflect <v> wins; legacy POST_REFLECT_* ignored`.

> Note: spec §10.1 says consume at A.9; the precedent SPEC_PATH resolves at A.2. For `--reflect` the
> builder should DECLARE the flag at the input-surface section (mirroring `:41`) but PERFORM resolution
> at the A.9 producer (so the once-only `auto`/wrapper-probe resolution co-locates with item emission).

---

## 5. §10.3 Frontmatter field — `reflect_post_mode` + `reflect_post` sentinel

**Current frontmatter — `SKILL.md:1942` (verbatim):**

```yaml
reflect_post: ""   # PENDING sentinel set by the final-phase POST reflect item; operator records {verdict, run_id, report} in a fresh session
```

**New frontmatter block — §10.3 (spec lines 847-851, verbatim):**

```yaml
reflect_post_mode: none | 1 | 2 | auto-resolved-1 | auto-resolved-2 | halt | 2-degraded-halt
reflect_post: ""    # PENDING sentinel — ONLY for halt / 2-degraded-halt; written by
                    # inline run (mode 1) or wrapper (mode 2); ABSENT for mode none.
```

**Frontmatter value set (oracle — this is the value set researcher-03 CONSUMES):**

`{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt}` — 7 values per §10.3 line 848
AND validation V2 (spec line 725).

**IMPORTANT — 8th value from §8.2:** the §10.3 enumeration lists 7, but the unified fallback ladder
(§8.2, spec line 678) and V16 (line 739) / the active-assertion map (line 749) / the rf-qa MODE-MATCH
set (line 766) ALSO define **`auto-resolved-2-degraded-halt`** (auto→2 path degraded when wrapper
absent — spec lines 649-650). So the COMPLETE frontmatter value set the builder must accept/validate is:

**`{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt, auto-resolved-2-degraded-halt}`** (8 values).

> Discrepancy flagged for the builder/rf-qa oracle: §10.3 line 848 enumerates 7; §8.2/V16/V-active-map
> require the 8th (`auto-resolved-2-degraded-halt`). The validator (V2 line 725) currently lists 7 but
> V16 (line 739) and the active-assertion map (line 749) list the degraded-halt triplet incl. the
> auto variant. The builder's V2 assertion value set should be the 8-value union so V16 cases pass.

**`reflect_post` sentinel rules (per-mode):**
- `none` → `reflect_post` key **ABSENT** from frontmatter (§6.1 line 474-475); `reflect_post_mode: none`.
- `1` / `auto-resolved-1` → `reflect_post: {verdict, run_id, report, reviewed_at}` written from the
  inline reflect contract (§6.2 line 495-496).
- `2` / `auto-resolved-2` → `reflect_post` written from the wrapper contract (§6.3).
- `halt` / `2-degraded-halt` / `auto-resolved-2-degraded-halt` → `reflect_post: PENDING` sentinel
  (V11 line 734; deferred to fresh session).

**Authority + name-mirroring (spec lines 853-855):** `reflect_post_mode` is the **single recorded
artifact** of the mode decision (NFR-3), the oracle for all §9 rf-qa assertions, written ONCE at
tasklist generation by the A.9 producer. Its name **deliberately mirrors** the BUILD_REQUEST field
`REFLECT_POST_MODE` (§10.1) — one name, two surfaces, single-oracle story.

---

## 6. §10.4 Advisory WARNING (FR-13 / INV-003)

**Emission condition (spec lines 857-863):** resolved request is a **fixed** `--reflect 1` (NOT `auto`)
**AND** `S6 == 1 ∨ S5 > 0`.

- `S5` = distinct human-decision / OQ-blocked items (`SKILL.md:2126`, ×5 in TCS) — spec line 252.
- `S6` = file-level refactor/remediation class, 0 or 1 (`SKILL.md:2127`, ×4 in TCS) — spec line 253.
- (These signals are CONSUMED from researcher-02's TCS/auto-FER work; not re-derived here.)

**Exact message (spec lines 860-861, verbatim):**
> *"auto would have selected Mode 2; Mode 1 is not executor-disjoint — confirm intent"*

**Properties (spec lines 862-863, INV-003):**
- Written to the **build log** by the A.9 producer.
- **NON-blocking** — "a footgun guard, not a gate."
- Emitted **alongside** the §6.2 Mode-1 item, which is **still produced** (honors operator authority).
- Does **NOT** change the emitted item and does **NOT** change `reflect_post_mode: 1`.

**Testable (spec lines 200-201):** building with `--reflect 1` on a tasklist with `S6=1` (or `S5>0`)
emits the WARNING in the build log; the emitted item is still the §6.2 Mode-1 item, frontmatter still
`reflect_post_mode: 1`.

---

## Summary

**Collision check (INV-005):** `grep -n "POST_REFLECT_MODE\|REFLECT_POST_MODE"` on the live SKILL.md
returns **NOTHING** — neither token exists. The sibling task TASK-RF-20260608-185553 is NOT merged into
this SKILL.md, so there is **no live `POST_REFLECT_MODE` field** to collide with. The only live POST
gate field today is the binary `POST_REFLECT_GATE: ENABLED` (`:853`). Spec §10.1 retires
`POST_REFLECT_MODE` to a read-time alias only; the builder can add `REFLECT_POST_MODE` as a fresh field
with zero rename conflict.

**Precedent (`--spec`/`SPEC_PATH`):** declared at input surface `:41`, resolved once at parse stage
`:201` (A.2) with an explicit 4-step priority order, carried as BUILD_REQUEST sub-field `:854`, consumed
at A.10.7 PRE (`--spec`) + POST item `{SPEC_PATH}` (`:1996`), written to frontmatter `spec_path:`
(`:1933`). `EXECUTION_CONTEXT_REQUIREMENTS` (`:831-851`) is the second precedent for an
optional/defaulted/closed-value-set/MALFORMED-max-2-retry BUILD_REQUEST field.

**Three edit items the builder can write:**
1. **Flag-parse/precedence item** — declare `--reflect none|0|1|2|auto` at the input surface (mirror
   `:41`); resolve ONCE at A.9 with the 4-step order (`--reflect` > `REFLECT_POST_MODE` BUILD_REQUEST
   field > legacy §5 alias map > default 2); on override write build-log note
   `--reflect <v> wins; legacy POST_REFLECT_* ignored`.
2. **BUILD_REQUEST-schema item** — at `:853` replace `POST_REFLECT_GATE: ENABLED` → `REFLECT_POST_MODE: 2`
   (`none|0|1|2|auto`, default 2); **retire the author-settable `DEPTH:` sub-field** (mode-derived per §7);
   keep `SPEC_PATH`/`TASK_FILE`; add deprecated-alias acceptance comment (§5 map, precedence step 3);
   route invalid values through A.9 MALFORMED max-2 retry.
3. **Frontmatter-field item** — at `:1942` add `reflect_post_mode:` with value set
   `{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt, auto-resolved-2-degraded-halt}`
   (8 values — §10.3 lists 7; §8.2/V16 add the 8th `auto-resolved-2-degraded-halt`); apply per-mode
   `reflect_post` sentinel rules (absent for `none`; `{verdict,…}` for 1/2/auto-resolved-{1,2}; `PENDING`
   for halt/`2-degraded-halt`/`auto-resolved-2-degraded-halt`); name mirrors BUILD_REQUEST
   `REFLECT_POST_MODE`.

**Advisory WARNING (§10.4/FR-13/INV-003):** fixed `--reflect 1` AND `S6==1 ∨ S5>0` → write NON-blocking
build-log warning *"auto would have selected Mode 2; Mode 1 is not executor-disjoint — confirm intent"*;
Mode-1 item still emitted, `reflect_post_mode: 1` unchanged.

**Cross-researcher flag for the builder:** §10.3 frontmatter enumeration (7 values) is inconsistent with
§8.2/V16/active-map (8 values incl. `auto-resolved-2-degraded-halt`). Builder should use the 8-value
union as the validator (V2) oracle so degraded auto→2 cases (V16) pass; researcher-03 consumes this
8-value set.
