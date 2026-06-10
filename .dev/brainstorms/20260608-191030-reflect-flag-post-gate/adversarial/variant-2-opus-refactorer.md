<!-- Variant 2 — persona: refactorer (opus). Lens: technical debt, simplification,
     minimal-risk transformation. Smallest reversible diff; byte-identical default
     restoration; clean old→new migration over new machinery. -->

# Spec — task-builder `--reflect auto|1|2`: a 3-mode POST-gate quality/cost dial (minimal-risk refactor)

> **Refactorer thesis.** This is a *template-selection* refactor, not a new feature. The
> builder already emits exactly one POST item and already bakes `--remediate --depth {DEPTH}`
> into it (`SKILL.md:1996`). The job is to widen a single emission site from "one fixed
> shape" to "one of three shapes selected by a pure function of inputs" — while keeping the
> **default path byte-identical to today** wherever the bytes can be preserved. The smallest
> safe diff is: (a) one new flag with default `2`, (b) one resolver function `RESOLVE_POST_MODE`,
> (c) three literal item templates where Mode 2's template is the current `:1994–1999` text
> with its Action swapped from "paste-ready manual command" to "Bash shell-out to the merged
> wrapper", (d) one frontmatter field, (e) two validation-assertion edits. Everything else —
> TCS, O1–O4, the PRE gate, `reflect_post` sentinel semantics, the HALT discipline — is left
> untouched and *reused*. No reflect logic is reauthored anywhere.

---

## 1. Problem

`task-builder/SKILL.md` emits ONE fixed post-execution reflect gate item (`SKILL.md:1994–1999`),
the penultimate item of the final phase. It writes `reflect_post: PENDING`, STOPs, and surfaces a
paste-ready `/sc:reflect --mode post --remediate … --depth {DEPTH} …` command for the operator to
run **manually in a fresh session**. That item is correct on the one property that matters —
**executor-disjoint** review (a NEW session that does not share the executor's representational
frame) — but it is one-size-fits-all and fully manual:

- A 4-item typo-fix tasklist and a 38-item cross-subsystem refactor both get the identical
  `--depth deep --remediate` fresh-session ceremony.
- Automation is now *possible*: the sibling wrapper spec (already merged, convergence 0.82,
  `.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md`) ships
  `superclaude reflect run <tasklist>` — a top-level `claude --print` subprocess that escapes the
  Agent-tool nesting limit so reflect's Tier-2 fan-out actually runs, with a 4-state fail-closed
  verdict `{pass, halted, degraded, blocked}`.

We want a `--reflect auto|1|2` dial (**default `2`**) that picks the POST item's *form* and *rigor*
at build time, collapsing **three overlapping knobs** (`POST_REFLECT_GATE: ENABLED` on/off at
`:853`, the sibling's proposed `POST_REFLECT_MODE: wrapper|halt`, and the new `--reflect`) into
**one coherent surface** without fragmenting the BUILD_REQUEST schema and without changing the
default operator experience more than is strictly necessary.

**The three modes are FIXED (not redefined here):**

| Mode | Form | Depth | `--remediate` | Executor-disjoint? | Nesting mechanic |
|---|---|---|---|---|---|
| **1** | inline `/sc:reflect --mode post` in the SAME `/task` session (top-level skill invocation) | `standard` | **NO** (audit-only) | **NO** (shares executor frame) | top-level skill call only |
| **2** (DEFAULT) | Bash shell-out to `superclaude reflect run {TASK_FILE}` | `deep` | **YES** (Tier-2 + Tier-3) | **YES** | Bash subprocess (never Agent/Task) |
| **auto** | builder deterministically resolves to 1 **or** 2 at build time | inherited from the resolved mode | inherited | inherited | inherited |

**Refactor invariant (TOP priority).** The **default-`2` path and the disabled path must restore
current behavior byte-for-byte where physically possible.** Default `2` is the *closest live
automation* of today's manual command (same depth `deep`, same `--remediate`, same HALT, same
`reflect_post` write-back) — and the **disabled** path re-emits the literal `:1994–1999` manual-HALT
text unchanged. A no-op upgrade (operators who set nothing and never used the sibling field) must see
a tasklist that differs from today only in the *form* of one item's Action, never in its gate
semantics.

---

## 2. Functional Requirements

- **FR-1 — One flag, one default.** Add `--reflect <auto|1|2>` to the task-builder invocation
  surface (`SKILL.md:36–48`, alongside `--spec`). **Default `2`.** Also accept a BUILD_REQUEST field
  `REFLECT_POST: auto|1|2|none` (FR-10) — `none` is the *disabled* value (no CLI equivalent; see FR-7).
  The flag/field governs **only** the POST template; it has **no** effect on the PRE gate (A.10.7,
  `SKILL.md:1407–1429`), which keeps its own Agent/Task spawn and `quick`-permitted depth.

- **FR-2 — Pure resolver, single emission site.** Introduce one deterministic resolver,
  `RESOLVE_POST_MODE(inputs) → {1, 2, disabled}`, evaluated once at A.9 BUILD_REQUEST assembly
  (`SKILL.md:853`). It is the *only* place the mode is decided. The downstream emitter (template
  selection at `:1994`) is a pure switch on the resolver's output. Two implementers feeding the same
  BUILD_REQUEST MUST compute the same emitted item (the spec's hard success criterion). The resolver
  is the refactor's single new piece of logic; everything else is template text.

- **FR-3 — Mode 1 emits inline audit-only.** Mode 1 emits a penultimate item whose **Action** has the
  *top-level* `/task` executor run `/sc:reflect --mode post --depth standard --diff <BASE>..HEAD
  --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --executor-model {EXECUTOR_CLASS}` **inline in the same
  session** — a top-level skill invocation, **NOT** Agent/Task, **NOT** shell-out, **NO** `--remediate`.
  The item still writes `reflect_post` and still HALTs on non-pass (FR-6, §6).

- **FR-4 — Mode 2 emits the wrapper shell-out (DEFAULT).** Mode 2 emits a penultimate item whose
  **Action** Bash-shells `superclaude reflect run {TASK_FILE}` — a top-level subprocess that the merged
  wrapper drives at `--depth deep --remediate` (its FR-3 passthrough + FR-9 promotion semantics). This
  is the byte-closest *live* equivalent of today's manual command (same depth, same remediate, same
  HALT). **Never** Agent/Task (`reference_subagent_cannot_nest_skill_fanout`; wrapper NFR-7).

- **FR-5 — `auto` resolves at build time, never defers.** Mode `auto` MUST resolve to a concrete `1`
  or `2` **at build time** via the §4 FER and stamp the resolved value (`reflect_post_mode:
  auto-resolved-1` / `auto-resolved-2`) into frontmatter. The emitted *item* is always a concrete Mode
  1 or Mode 2 template — the executor never sees the literal token `auto`, never re-derives the choice.
  (Determinism + auditability: the resolution is frozen in the artifact.)

- **FR-6 — Every emitted item HALTs on non-pass and writes `reflect_post`.** Unchanged invariant from
  today (`feedback_human_decision_items_must_halt`). All three concrete forms (1, 2, auto-resolved):
  write `reflect_post: PENDING` before running, capture the verdict, and **only** on `verdict: pass`
  may the downstream `Update task status to Done` item proceed. Non-pass → HALT + route reason/report
  into `### Open Questions`. No emitted item ever auto-proceeds.

- **FR-7 — `none`/disabled restores the literal manual-HALT item byte-for-byte.** When the resolver
  returns `disabled` (BUILD_REQUEST `REFLECT_POST: none`, or legacy `POST_REFLECT_GATE: DISABLED`),
  the builder emits the **exact** `:1994–1999` text in force today — the manual paste-ready
  `/sc:reflect --mode post --remediate … --depth {DEPTH} …` fresh-session item, character-for-character.
  This is the reversibility anchor: any operator who is wary of automation gets *exactly* the current
  behavior by passing one value.

- **FR-8 — Wrapper-absence degrades to the disabled (manual-HALT) item, never STOPs the build.** If
  Mode 2 is selected but `superclaude reflect run` is not detectable on PATH (FR-NFR detection, §8),
  the builder does **not** fail the build and does **not** silently downgrade to Mode 1. It emits the
  **disabled** template (FR-7 byte-identical manual-HALT) and records `reflect_post_mode:
  2-degraded-to-manual` + a one-line note in the item Context. This is the least-surprise fallback:
  the operator still gets a correct executor-disjoint gate (the manual fresh-session one they have
  today), just not the automated one. (Rationale §8.)

- **FR-9 — `--spec` threading preserved unchanged.** The resolved `spec_path` (`SKILL.md:41`) is
  baked into whichever template is emitted, exactly as today (`[--spec {SPEC_PATH}]`, omitted when no
  spec). No change to `--spec` resolution order or frontmatter write.

- **FR-10 — Frontmatter records the resolved mode.** Replace the `reflect_post: ""` sentinel line
  (`SKILL.md:1942`) semantics — *keep the field and its PENDING contract* — and **add** a sibling field
  `reflect_post_mode: <1 | 2 | auto-resolved-1 | auto-resolved-2 | 2-degraded-to-manual | manual>` (§10).
  `reflect_post` itself keeps its existing `{verdict, run_id, report}` write-back contract verbatim.

---

## 3. Non-Functional Requirements

- **NFR-1 — Maximal reversibility (TOP priority).** The default-`2` and disabled paths restore today's
  behavior to the maximum physically possible degree: disabled = byte-identical manual item; default
  `2` = same depth/`--remediate`/HALT/sentinel, differing only in *form* (live shell-out vs. paste-ready
  command). The entire change is a single-site template switch behind one flag; reverting the flag to
  `none` everywhere reproduces today's artifacts exactly.

- **NFR-2 — Zero reflect-logic duplication.** Emitted items only *invoke* reflect inline (Mode 1) or
  *shell out to* the wrapper (Mode 2). No deviation taxonomy, tier rubric, depth band, or verdict logic
  is reauthored in any emitted item or in the resolver. The resolver reads inputs and the TCS table
  (already in the file at `:2114+`); it computes no reflect semantics.

- **NFR-3 — Single TCS producer.** The TCS machinery (`SKILL.md:2114–2155`) remains the sole depth
  authority. Mode 1/2 fix depth (`standard`/`deep`) as a *floor consistent with O4*, not a competing
  computation (§7). `auto`'s mode choice *reads* the TCS the builder already computed — no second TCS.

- **NFR-4 — Fail-closed posture inherited, not reinvented.** The completion gate's pass/non-pass HALT
  is the wrapper's 4-state verdict (Mode 2) or reflect's own return contract (Mode 1) — both already
  fail-closed. The builder adds no new verdict logic; it only asserts the *shape* of the emitted item.

- **NFR-5 — SoT discipline.** All edits land in `src/superclaude/skills/task-builder/SKILL.md` (+ its
  `rf-qa` agent prompt under `src/superclaude/`), then `make sync-dev`; never stage `.claude/` mirrors
  (CLAUDE.md ABSOLUTE RULE).

- **NFR-6 — Nesting safety.** Mode 2 = Bash shell-out only. Mode 1 = inline top-level skill call only;
  if the `/task` executor is itself an Agent-tool subagent, Mode 1 silently loses Tier-2 — the item
  carries an explicit self-check that detects and disallows this (§8).

- **NFR-7 — No new machinery.** No new CLI, no new contract format, no new isolation/budget/poller. The
  wrapper already exists (sibling spec); reflect already exists; TCS already exists. This refactor adds
  one flag, one resolver, three templates, one field, two assertions. That is the whole footprint.

---

## 4. The `auto` FER (deterministic 1-vs-2 selection)

`auto` MUST resolve to `1` or `2` by a **pure function of already-computed integers** so two
implementers reach the identical choice. The refactorer choice is to **reuse the TCS the builder
already computes for the POST `--depth`** — introducing zero new scoring machinery — and gate it with
the two override signals that already flip reflect to mandatory Tier-2.

### `RESOLVE_POST_MODE` — the frozen extraction rule

```text
INPUTS (all already computed at A.9 / present in BUILD_REQUEST):
  flag        = --reflect value  (auto | 1 | 2 ; default 2)
  gate        = POST_REFLECT_GATE ENABLED|DISABLED  (default ENABLED)   # legacy on/off
  reflect_post_field = REFLECT_POST  (auto|1|2|none ; absent ⇒ derive from flag/gate)  # new field
  TCS         = the integer the POST-depth derivation already produced (:2131)
  S5          = human-decision/Open-Question-blocked item count (:2126)
  S6          = file-level refactor/remediation class, 0|1 (:2127)
  wrapper_ok  = (superclaude reflect run detectable on PATH) ? true : false   # §8

PRECEDENCE (first match wins):
  1. If gate == DISABLED  OR  reflect_post_field == none  → return disabled   # FR-7
  2. mode := (reflect_post_field if in {auto,1,2}) else (flag)                # field > flag default
  3. If mode == 1 → resolved := 1
  4. If mode == 2 → resolved := 2
  5. If mode == auto:
        # AUTO PREDICATE (deterministic, reuses existing O1/O2 signals + TCS band)
        if (S6 == 1)            → resolved := 2     # refactor/remediation class: force the
                                                     # executor-disjoint + Tier-2/3 path (mirrors O2)
        elif (S5 > 0)          → resolved := 2     # any human-decision halt-point: full audit
        elif (TCS >= 35)       → resolved := 2     # deep band: cross-subsystem/dependency-heavy
        else                   → resolved := 1     # TCS <= 34, no risk/human-decision: light inline
  6. If resolved == 2 AND wrapper_ok == false → return 2-degraded-to-manual    # FR-8 (emit disabled
                                                                                # template, note it)
  7. return resolved
```

### Why this predicate (refactorer defense)

- **It introduces no new score.** The auto predicate is `S6==1 ∨ S5>0 ∨ TCS≥35`. Every term already
  exists and already carries meaning in the file: `S6` and `S5` are the exact two signals that
  override the depth band to force Tier-2 (`O2`, `O1` at `:2150–2149`), and `TCS≥35` is the existing
  `deep`-band edge (`:2145`). So **"auto picks Mode 2 exactly when the existing machinery would have
  forced `--depth deep` or escalated to a halt-class audit."** That is the single most defensible
  mapping: the dial's high-rigor setting fires precisely where the codebase already says rigor is
  mandatory. No magic threshold is invented for this feature.
- **It is monotone and total.** Every input combination yields exactly one of `{1, 2, disabled,
  2-degraded-to-manual}`. No ±4 tiebreaker is admitted here (that bounded inference lives in TCS depth
  derivation only, `:2154`); the mode choice is fully arithmetic to avoid a second inference surface.
- **It degrades, never crashes.** Step 6 routes an unsatisfiable Mode 2 to the manual fallback rather
  than failing the build (FR-8).

### Fate of O4

`O4` (POST never `quick`, `:2152`) is **retained verbatim and is now structurally guaranteed**: Mode 1
fixes `standard`, Mode 2 fixes `deep`, the disabled template inherits the existing `--depth {DEPTH}`
which already floors at `standard` per O4. No mode can emit `quick`. O4 changes from "a floor the
emitter must remember to apply" to "an invariant the three templates make unreachable" — a net
simplification, not a new rule.

---

## 5. Knob Reconciliation + old→new Map

Three knobs collapse into one **precedence chain** with the new `--reflect`/`REFLECT_POST` as the
authority and the legacy `POST_REFLECT_GATE: ENABLED/DISABLED` retained as a *coarse on/off that maps
cleanly onto the new field*. The sibling's `POST_REFLECT_MODE: wrapper|halt` is **folded in as an
alias**, not a third independent knob.

### Resolution precedence (single coherent surface)

```text
REFLECT_POST (new field) | --reflect (CLI flag)   ── PRIMARY authority (FR-2/§4 step 2)
        ▲ alias-in:  POST_REFLECT_MODE: wrapper  ≡  REFLECT_POST: 2
        ▲ alias-in:  POST_REFLECT_MODE: halt     ≡  REFLECT_POST: 1   (inline audit-only)
POST_REFLECT_GATE: ENABLED|DISABLED               ── COARSE gate (FR-7 / §4 step 1)
        DISABLED  ⇒ disabled template (byte-identical manual-HALT)
        ENABLED   ⇒ defer to REFLECT_POST/--reflect (default 2 if neither set)
```

### old→new migration map (explicit, byte-for-byte where possible)

| Today (old) | New resolver result | Emitted item | Behavioral delta |
|---|---|---|---|
| `POST_REFLECT_GATE: ENABLED`, nothing else set | `2` (default) | **Mode 2** wrapper shell-out, `deep --remediate` | Same depth/remediate/HALT/sentinel as today's manual command; **form** changes paste-ready → live shell-out. Closest live automation. |
| `POST_REFLECT_GATE: DISABLED` | `disabled` | **byte-identical** `:1994–1999` manual-HALT item | **Zero delta.** Reversibility anchor. |
| (no `POST_REFLECT_GATE` field at all) | treated as `ENABLED` ⇒ `2` | Mode 2 | Matches today's "omission implies the gate is wanted" default; rigor preserved (default 2 ≡ today's `deep --remediate`). |
| `--reflect 1` / `REFLECT_POST: 1` | `1` | **Mode 1** inline audit-only `standard` | New lightweight option; opt-in only. |
| `--reflect 2` / `REFLECT_POST: 2` | `2` | Mode 2 | Explicit default. |
| `--reflect auto` / `REFLECT_POST: auto` | `1` or `2` per §4 | resolved concrete template | New; build-time resolved. |
| `REFLECT_POST: none` | `disabled` | byte-identical manual-HALT item | Explicit opt-out; same as `POST_REFLECT_GATE: DISABLED`. |
| sibling `POST_REFLECT_MODE: wrapper` | `2` (alias) | Mode 2 | Folded in — no separate field. |
| sibling `POST_REFLECT_MODE: halt` | `1` (alias) | Mode 1 | Folded in. (See note.) |

**Note on the `halt`-alias choice (decisive).** The sibling spec's `POST_REFLECT_MODE: halt` meant
"keep the manual fresh-session HALT item." A naïve mapping is `halt → disabled`. The refactorer
choice is `halt → Mode 1` **only if `POST_REFLECT_GATE` is still ENABLED**; the truly-manual path is
the explicit `none`/`DISABLED` value. Rationale: the sibling field is *proposed*, not yet shipped, so
folding it onto the new authoritative dial (rather than minting a 4th token) keeps the surface
minimal. The pure "give me exactly today's item" intent is served unambiguously by `none`/`DISABLED`
(FR-7), which is byte-identical and needs no alias gymnastics. If reviewers prefer `halt → disabled`,
that is a one-line change in the alias table with identical downstream machinery — both are reversible.

**Net knob count: ONE authoritative dial (`--reflect`/`REFLECT_POST`) + ONE coarse legacy on/off
(`POST_REFLECT_GATE`) that maps onto it.** The sibling's `POST_REFLECT_MODE` is absorbed as aliases
and does not survive as an independent field — the BUILD_REQUEST schema does not fragment.

---

## 6. Per-Mode Emitted-Item Templates (literal text + diff vs current)

All three concrete templates are **penultimate** (immediately before `Update task status to Done`),
all write `reflect_post`, all HALT on non-pass. `<BASE>` = frontmatter `start_commit`, else
`git merge-base HEAD <integration>`. `{DEPTH}` in the disabled template is the existing TCS-derived,
O4-floored value.

### 6.1 Mode 2 — wrapper shell-out (DEFAULT). Diff vs current `:1994–1999`.

This is the closest-to-today template, so it is shown as a unified diff against the **current** item.
Only the **Action**, **Output**, and **Verification** mechanism changes (paste-ready manual command →
live Bash shell-out); the **Context**, the HALT, the `reflect_post` write-back, the depth (`deep`) and
`--remediate` are preserved.

```diff
- - [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**
+ - [ ] **N.{X-1} — Independent post-execution reflection gate (wrapper subprocess, HALT)**
    - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran
      in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory
      `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches
      spec-literal-token, invariant-arithmetic, and integration/orphan blindspots same-frame QA misses.
-   - **Action**: Do NOT run reflect inside this session. Write `reflect_post: PENDING` to this file's
-     frontmatter, then STOP and surface this paste-ready command for the operator to run in a NEW
-     session: `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE}
-     [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` — where `<BASE>` is the
-     commit recorded at task start … and the spawned reflect agent uses the default subagent model.
-     The gate command uses `/sc:reflect` and never the `sc:task` execution command.
+   - **Action**: Write `reflect_post: PENDING` to this file's frontmatter, then run the executor-
+     disjoint audit as a **Bash shell-out** (NEVER via Agent/Task — that re-introduces the Tier-2
+     nesting bug, `reference_subagent_cannot_nest_skill_fanout`):
+     `superclaude reflect run {TASK_FILE}` — the wrapper launches `/sc:reflect --mode post
+     --remediate --diff <BASE>..HEAD [--spec {SPEC_PATH}] --depth deep --executor-model
+     {EXECUTOR_CLASS}` as a top-level `claude --print` subprocess (escaping the nesting limit so
+     Tier-2 fans out), then writes a 4-state verdict `{pass, halted, degraded, blocked}` back into
+     `reflect_post`. The wrapper owns depth/`<BASE>` passthrough — do NOT recompute them here.
-   - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready `/sc:reflect --mode post` command
-     surfaced for a fresh session.
+   - **Output**: Frontmatter `reflect_post: {verdict, run_id, report}` written by the wrapper;
+     wrapper exit code (0 only on `verdict: pass`).
-   - **Verification**: `reflect_post` is PENDING and the operator has the exact `/sc:reflect`
-     command. The item does NOT self-resolve.
+   - **Verification**: `superclaude reflect run` exited 0 AND `reflect_post.verdict == pass`. Any
+     other verdict (`halted`/`degraded`/`blocked`) means the gate did NOT pass.
    - **Completion gate**: `reflect_post.verdict == pass` (wrapper exit 0). On any non-pass verdict,
      HALT: append the wrapper's `report` + `reason` + deviation rollup to `### Open Questions` and do
      NOT proceed to `Update task status to Done` (HALT per `feedback_human_decision_items_must_halt`).
      Tier-3 remediation surfaced by the wrapper is recorded as an Open Question — NEVER auto-executed.
```

### 6.2 Mode 1 — inline audit-only (`standard`, no `--remediate`). Full literal text.

```text
- [ ] **N.{X-1} — Inline post-execution reflection gate (same session, audit-only, HALT)**
  - **Context**: All implementation/test/QA items above are complete. This tasklist resolved to
    Mode 1 (low TCS, no human-decision/refactor-class items) — a lightweight, audit-only check. NOTE:
    Mode 1 is NOT executor-disjoint; it runs in THIS executor's frame and shares its representational
    bias. It is acceptable here because the resolver classified this work as low-complexity/low-risk
    (§4). Reflect's Tier-2 reviewers remain heterogeneous-model even inline.
  - **Action**: FIRST self-check the nesting boundary: if THIS `/task` executor is running as an
    Agent-tool subagent (not a top-level session), STOP and HALT with reason
    `mode1-needs-top-level-executor` — an inline `/sc:reflect` from a subagent silently loses Tier-2
    fan-out (`reference_subagent_cannot_nest_skill_fanout`); the operator must re-run at top level or
    rebuild with `--reflect 2`. Otherwise: write `reflect_post: PENDING`, then run inline (top-level
    skill invocation, NOT Agent/Task, NOT shell-out):
    `/sc:reflect --mode post --depth standard --diff <BASE>..HEAD --tasklist {TASK_FILE}
    [--spec {SPEC_PATH}] --executor-model {EXECUTOR_CLASS}` — audit-only (NO `--remediate`).
  - **Output**: Frontmatter `reflect_post: {verdict, run_id, report}` from the inline reflect run.
  - **Verification**: Inline `/sc:reflect` returned a verdict; `reflect_post.verdict` recorded. The
    item does NOT auto-resolve to Done on a non-pass verdict.
  - **Completion gate**: `reflect_post.verdict == pass`. On any non-pass verdict, HALT: append
    reflect's `report` + deviation findings to `### Open Questions` and do NOT proceed to
    `Update task status to Done` (HALT per `feedback_human_decision_items_must_halt`). Because Mode 1
    is audit-only, any surfaced deviation routes to a fresh-session `--remediate` or a `--reflect 2`
    rebuild — NEVER auto-remediated inline.
```

### 6.3 `auto`-resolved.

`auto` emits **either** 6.1 (resolved-2) **or** 6.2 (resolved-1) verbatim — there is no third
template. The only auto-specific addition is a one-line provenance prefix in the item Context:
`Resolved by --reflect auto → Mode {N} (predicate: S6={s6}, S5={s5}, TCS={tcs}).` so the executor and
any auditor can see why this shape was chosen. The frontmatter stamps `reflect_post_mode:
auto-resolved-{N}` (§10).

### 6.4 Disabled — byte-identical to current (FR-7).

When `RESOLVE_POST_MODE → disabled` (or `2-degraded-to-manual`, FR-8), the builder emits the **exact**
current `:1994–1999` item — the manual paste-ready fresh-session HALT — with **no character change**.
For `2-degraded-to-manual`, a single `<!-- wrapper-absent: degraded from Mode 2 -->` comment is
appended to the item Context (the gate text itself is untouched).

---

## 7. Depth/TCS Reconciliation

**Decision: modes FIX depth; `auto` USES TCS to pick the mode (and thereby inherits the mode's fixed
depth). TCS stays the single producer.** This is the minimal-coupling choice.

- **Mode 1 → `--depth standard`** (fixed). **Mode 2 → `--depth deep`** (fixed, via wrapper). These are
  not new computations — they are the band edges O4 already enforces (`standard` floor) and the
  `deep`-band the existing table assigns to high-TCS tasklists.
- **`auto` reads the TCS the builder already computed** for POST-depth derivation (`:2131`) and the
  existing `S5`/`S6` signals — no second TCS pass. The mode choice and the depth are therefore
  *consistent by construction*: auto picks Mode 2 exactly on the inputs (`S6==1 ∨ S5>0 ∨ TCS≥35`) where
  the existing override machinery would have forced `--depth deep` anyway. There is no case where
  `auto` selects Mode 1 (`standard`) for a tasklist the TCS table would have run `deep`.
- **O4 retained, now structurally guaranteed** (see §4 "Fate of O4"): no template can emit `quick`.
- **O1/O2/O3 unchanged.** They continue to govern the *disabled* template's `{DEPTH}` placeholder
  exactly as today, and they feed the auto predicate (O1≈`S5>0`, O2≈`S6==1`) as read-only signals. No
  override is deleted or re-weighted.

**Why not "mode overrides TCS-derived depth in the disabled item too?"** Because the disabled item
must be byte-identical to today (FR-7), it keeps `--depth {DEPTH}` as the TCS-derived O4-floored value.
Only the live Mode 1/2 templates fix depth, and they fix it *to the same band the TCS would have
chosen for that complexity* — so there is no drift between "what mode says" and "what TCS would say."

---

## 8. Wrapper-Dependency Fallback

**Decision: Mode 2 wrapper-absent → emit the byte-identical disabled manual-HALT item (FR-7) tagged
`2-degraded-to-manual`. Never STOP the build; never silently drop to Mode 1.**

- **Detection (builder-time, cheap).** At A.9, the builder probes wrapper availability with a single
  read-only check — `superclaude reflect --help` exits 0 **and** its output advertises the `run`
  subcommand (equivalently `command -v superclaude` + a `reflect run` grep). Result → `wrapper_ok`
  boolean fed to §4 step 6. The probe is read-only and adds no state.
- **Why degrade to the *manual* item, not Mode 1?** Mode 1 sacrifices executor-disjointness (§ below);
  silently substituting it for an operator who asked for the rigorous default `2` would *weaken the
  gate without consent*. The manual fresh-session HALT item, by contrast, **preserves
  executor-disjointness** (it is literally today's behavior) — it just isn't automated. So the
  least-surprise degradation of "automated disjoint audit unavailable" is "the manual disjoint audit
  you have today," not "a weaker inline audit." This is the refactorer's reversibility principle
  applied to the failure path: **degrade to existing behavior, not to a new weaker behavior.**
- **Visibility.** The frontmatter records `reflect_post_mode: 2-degraded-to-manual` and the item
  Context carries the `wrapper-absent` comment, so the operator knows automation was unavailable and
  can install the wrapper + rebuild, or run the surfaced manual command.
- **Never STOP at build time.** A missing wrapper is an *environment* condition, not a malformed
  request; failing the whole build over it would be disproportionate and non-reversible (the operator
  loses the entire tasklist). Emitting a correct, manual gate item is strictly safer.

### Executor-disjointness trade-off (Mode 1) — what it sacrifices, when acceptable

| Property | Mode 2 / manual-HALT (disjoint) | Mode 1 (inline) |
|---|---|---|
| Executor-exclusion (anti-self-confirmation) | **Yes** — fresh session / subprocess never shared the executor's frame | **No** — runs in the executor's session, shares its representational bias |
| Reflect Tier-2 heterogeneous reviewers | Yes | Yes (still heterogeneous-model **iff** executor is top-level; §6.2 self-check) |
| `--remediate` (Tier-3 chain) | Yes (Mode 2) / Yes (manual) | **No** (audit-only) |
| Cost / latency | High (subprocess / fresh session, `deep`) | Low (inline, `standard`, no remediate) |

**Mode 1 is acceptable exactly when the resolver classifies the work low-complexity/low-risk**
(`S6==0 ∧ S5==0 ∧ TCS≤34`) — i.e., the cases where a same-frame audit is unlikely to be the marginal
catch and the cost of a full disjoint `deep --remediate` is disproportionate. For any
refactor/remediation-class or human-decision or deep-band tasklist, `auto` never selects Mode 1.

---

## 9. Validation + rf-qa Changes

The smallest correct change to the validation surface is to **generalize the two existing
mode-agnostic assertions to be mode-aware**, not to add a parallel checklist. Two edits.

### Edit A — present-and-penultimate assertion (`SKILL.md:2051`)

```diff
- - [ ] POST reflect item present and positioned penultimate (immediately before
-       Update-status-to-Done) when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted
+ - [ ] POST reflect item present and positioned penultimate (immediately before
+       Update-status-to-Done) whenever RESOLVE_POST_MODE ≠ disabled — and its SHAPE
+       MATCHES the resolved mode (Mode 1 ⇒ inline `/sc:reflect … --depth standard`, no
+       `--remediate`; Mode 2 ⇒ Bash `superclaude reflect run {TASK_FILE}`; disabled ⇒
+       byte-identical manual `/sc:reflect … --remediate` item). MALFORMED if omitted OR
+       if the emitted item's shape contradicts `reflect_post_mode`.
```

### Edit B — Critical Rule #19 (`SKILL.md:2108`)

```diff
- 19. **POST reflect gate in generated task files.** When the BUILD_REQUEST specifies
-     `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item …, a
-     fresh-session reflect handoff item. The item MUST NOT run reflect inline … it writes a
-     `reflect_post: PENDING` sentinel and HALTs … A generated task file that omits the POST
-     reflect item when `POST_REFLECT_GATE: ENABLED` is a MALFORMED output.
+ 19. **POST reflect gate in generated task files.** The builder resolves the POST gate mode via
+     `RESOLVE_POST_MODE` (§4): `1` (inline audit-only `standard`), `2` (Bash shell-out to
+     `superclaude reflect run`, `deep --remediate`; DEFAULT), `disabled`/`2-degraded-to-manual`
+     (byte-identical manual fresh-session HALT item). Unless the result is `disabled`, the builder
+     MUST emit, as the penultimate item, the template for the resolved mode (§6). EVERY mode writes
+     `reflect_post: PENDING`, HALTs on non-pass, and uses `/sc:reflect`/`superclaude reflect run`
+     for the gate and `/task` (never `/sc:task`) for any re-execution. The emitted item's shape MUST
+     match `reflect_post_mode` in frontmatter. Omitting the item (when ≠ disabled), or emitting an
+     item whose shape contradicts `reflect_post_mode`, is a MALFORMED output.
```

### Edit C — rf-qa (task-integrity) assertion (in `src/superclaude/.../rf-qa.md` prompt)

Add ONE task-integrity assertion (`MODE-MATCH`), mirroring how the existing rf-qa task-integrity mode
already checks "POST item present + penultimate + writes `reflect_post` + uses `/sc:reflect` not
`/sc:task`":

```text
MODE-MATCH (MALFORMED on fail): read frontmatter `reflect_post_mode`. Assert the penultimate
final-phase item's Action shape matches it:
  reflect_post_mode == 1                       ⇒ Action contains inline `/sc:reflect --mode post
                                                  --depth standard` AND does NOT contain `--remediate`
                                                  AND does NOT contain `superclaude reflect run`.
  reflect_post_mode ∈ {2, auto-resolved-2}     ⇒ Action contains Bash `superclaude reflect run
                                                  {TASK_FILE}` AND does NOT spawn Agent/Task.
  reflect_post_mode == auto-resolved-1         ⇒ same assertion as mode 1.
  reflect_post_mode ∈ {manual, 2-degraded-to-manual} ⇒ Action is the byte-identical manual
                                                  paste-ready `/sc:reflect --mode post --remediate …`
                                                  fresh-session item.
ALL modes: item writes `reflect_post: PENDING`, is penultimate, and HALTs on non-pass.
Mismatch between `reflect_post_mode` and the emitted Action shape = MALFORMED (retry max-2 per
Critical Rule #12 / A.9 MALFORMED mediation).
```

No other rf-qa logic changes. The existing penultimate/`reflect_post`/HALT/`/sc:reflect`-vs-`/sc:task`
checks are *reused*; only the mode-shape assertion is added.

---

## 10. Flag Plumbing + Frontmatter + BUILD_REQUEST

### Parse points & precedence

- **CLI flag** `--reflect <auto|1|2>` added at the invocation surface (`SKILL.md:36–48`), default `2`.
- **BUILD_REQUEST field** `REFLECT_POST: auto|1|2|none` (A.9, near `POST_REFLECT_GATE` at `:853`).
- **Sibling alias** `POST_REFLECT_MODE: wrapper|halt` accepted and mapped per §5 (not a surviving
  field).
- **Precedence** (highest first, §4 steps 1–2): `POST_REFLECT_GATE: DISABLED` / `REFLECT_POST: none`
  (→ disabled) > `REFLECT_POST` field > `--reflect` flag > default `2`. The legacy `ENABLED` is the
  permissive case that defers to the dial.

### Frontmatter

Keep `reflect_post` (the `:1942` sentinel) with its existing PENDING + `{verdict, run_id, report}`
contract **unchanged**. **Add** one sibling field:

```yaml
reflect_post: ""              # PENDING sentinel — UNCHANGED contract (verdict/run_id/report written
                              #   by the emitted gate item, inline (Mode 1) or by the wrapper (Mode 2))
reflect_post_mode: 2          # one of: 1 | 2 | auto-resolved-1 | auto-resolved-2 |
                              #         2-degraded-to-manual | manual
                              # the FROZEN resolver output (§4); rf-qa MODE-MATCH asserts the
                              # emitted item shape matches this value
```

### BUILD_REQUEST A.9 block (diff vs current `:853`)

```diff
  POST_REFLECT_GATE: ENABLED
    SPEC_PATH: <spec_path or NONE>
    DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4 — never quick
    TASK_FILE: ${TASK_FILE}
+   REFLECT_POST: <auto | 1 | 2 | none>   # default 2 when ENABLED and unset. Selects POST gate
+                                          #   form/rigor (§4 RESOLVE_POST_MODE). `none` ≡ DISABLED
+                                          #   (byte-identical manual-HALT item). Accepts sibling
+                                          #   alias POST_REFLECT_MODE: wrapper(≡2)|halt(≡1).
```

`SPEC_PATH`, `DEPTH`, `TASK_FILE` are retained — `DEPTH` still feeds the disabled template's
`{DEPTH}`; Mode 1/2 fix their own depth (§7). The block is strictly additive: omitting `REFLECT_POST`
under `POST_REFLECT_GATE: ENABLED` yields the default-`2` (Mode 2) item — the byte-closest live
automation of today's `--remediate --depth deep` manual command.

---

## 11. Scope Boundaries

**IN:** `src/superclaude/skills/task-builder/SKILL.md` — the `--reflect` flag (`:36–48`), the A.9
`REFLECT_POST` BUILD_REQUEST field + alias mapping (`:853`), the `RESOLVE_POST_MODE` resolver (§4),
the three concrete POST item templates replacing `:1994–1999` (§6), the disabled byte-identical
fallback (FR-7/§6.4), the TCS/O4 reconciliation note (`:2147–2152` — additive, no override removed),
validation edits A/B (`:2051`, `:2108`), `reflect_post_mode` frontmatter field (`:1942` neighbor), and
the rf-qa `MODE-MATCH` task-integrity assertion (rf-qa agent prompt under `src/superclaude/`). Then
`make sync-dev`.

**OUT (hard non-goals):**

- Building/modifying the thin wrapper `superclaude reflect run` (sibling spec, already merged — this
  spec only *emits a Bash call to it*).
- Modifying `sc-reflect-protocol` (Mode 1 *invokes* it; depth/tier/verdict semantics are reflect's).
- Changing the PRE gate A.10.7 (`:1407–1429`) — its Agent/Task spawn and `quick`-permitted depth are
  untouched; `--reflect` governs only POST.
- `sc:cli-portify` / any Python port of reflect logic.
- New CLI surfaces, new contract formats, new isolation/budget/poller machinery (NFR-7).

---

## 12. Risks

| # | Risk | Likelihood | Mitigation (refactorer = prefer the reversible one) |
|---|---|---|---|
| R-1 | **Default-2 changes operator habit silently** — operators who paste the manual command now get a live shell-out. | Med | Default `2` preserves *depth/remediate/HALT/sentinel* (only form changes); `none`/`DISABLED` restores the exact manual item byte-for-byte (FR-7). Migration map (§5) is explicit. Fully reversible per-build. |
| R-2 | **Mode 1 silently loses Tier-2** when the `/task` executor is itself a subagent. | Med | §6.2 Action begins with a mandatory nesting self-check that HALTs (`mode1-needs-top-level-executor`); rf-qa `MODE-MATCH` does not (and cannot) detect runtime nesting, so the check lives in the emitted item itself. |
| R-3 | **`auto` picks the wrong rigor** for a borderline tasklist. | Low | Predicate reuses the *exact* signals (`S5`,`S6`,`TCS≥35`) that already force `deep`/escalation — auto-2 fires precisely where the codebase already mandates rigor; no novel threshold. Borderline-low cases default to the cheaper Mode 1 by design, and the operator can override with explicit `1`/`2`. |
| R-4 | **Wrapper absent at execution time** (probed-OK at build, gone at run). | Low | Mode 2 item's completion gate treats a non-zero/`command not found` from `superclaude reflect run` as a non-pass verdict → HALT (FR-6), routing the operator to install + re-run or use the manual command. No false pass. |
| R-5 | **Three-knob schema fragmentation** (the thing we're trying to prevent). | Med→Low | `POST_REFLECT_MODE` is folded in as aliases, not a surviving field (§5); net surface is one dial + one coarse legacy on/off. rf-qa asserts a single `reflect_post_mode` value, so the artifact has one source of truth for the mode. |
| R-6 | **Wired via Agent/Task** (re-introduces the nesting bug for Mode 2). | Low | Template says "Bash shell-out … NEVER via Agent/Task" inline (§6.1); rf-qa `MODE-MATCH` asserts the Mode-2 Action does not spawn Agent/Task; matches wrapper NFR-7. |
| R-7 | **`reflect_post_mode` drifts from the emitted item** after a hand-edit. | Low | rf-qa `MODE-MATCH` (Edit C) is the gate; mismatch = MALFORMED (retry max-2). The field is the frozen resolver output, written once at build. |
| R-8 | **Reviewers prefer `halt → disabled` over `halt → Mode 1`.** | Low | §5 note: it's a one-line alias-table change with identical downstream machinery; both are reversible. Not load-bearing. |

---

<!-- End variant-2 (refactorer). Distinctive stance: the change is a single-emission-site template
     switch behind one flag + one pure resolver; default-2 and disabled paths restore today's
     behavior to the maximum physical degree (disabled = byte-identical; default-2 = same
     semantics, form-only delta); the auto predicate reuses the EXACT existing signals (S5/S6/TCS≥35)
     that already force deep/escalation, inventing no new threshold; wrapper-absence degrades to the
     EXISTING manual disjoint gate (not a new weaker inline one); POST_REFLECT_MODE is folded in as
     aliases so the schema collapses to one dial. -->
