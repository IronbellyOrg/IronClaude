<!-- Variant 1 — opus:architect — adversarial spec generation -->
<!-- Lens: maintainability + extension scaffolding; collapse three overlapping config knobs into one coherent surface -->
<!-- Domain: code | Strategy: systematic | Depth: deep -->

---
spec_id: task-builder-reflect-flag-post-gate
title: "task-builder `--reflect auto|1|2` — 3-mode POST reflect gate dial"
variant: "1 (opus:architect)"
lens: maintainability + single-source-of-truth + extensibility
domain: code
default_mode: 2
out_of_scope:
  - building the `superclaude reflect run` wrapper (sibling spec, already merged)
  - modifying sc-reflect-protocol
  - changing the PRE gate (A.10.7)
  - any sc:cli-portify
created: 2026-06-08T19:10:30Z
target_surfaces:
  - src/superclaude/skills/task-builder/SKILL.md:41        # --spec threading
  - src/superclaude/skills/task-builder/SKILL.md:853        # POST_REFLECT_GATE BUILD_REQUEST field
  - src/superclaude/skills/task-builder/SKILL.md:1942        # reflect_post sentinel
  - src/superclaude/skills/task-builder/SKILL.md:1994-1999   # current POST item template
  - src/superclaude/skills/task-builder/SKILL.md:2051        # present-and-penultimate assertion
  - src/superclaude/skills/task-builder/SKILL.md:2108        # validation checklist item 19
  - src/superclaude/skills/task-builder/SKILL.md:2114-2155   # Reflect Depth (TCS) + O1-O4
---

# Spec — task-builder `--reflect auto|1|2`: a 3-mode POST reflect gate dial

> **Architect thesis (load-bearing).** Today three knobs each touch the POST gate from a
> different angle: `POST_REFLECT_GATE: ENABLED` (on/off, `SKILL.md:853`), the sibling
> wrapper's proposed `POST_REFLECT_MODE: wrapper|halt`
> (`.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md` §7 Q7),
> and the new `--reflect auto|1|2`. If they remain three fields the BUILD_REQUEST schema
> fragments and a `verify-sync` reader cannot tell which knob wins. The clean long-term
> surface is **one dial** — `--reflect` — that **subsumes** both predecessors and exposes a
> single ordinal value `{none, 1, 2, auto}`. Every legacy field maps onto a position on this
> dial via a frozen, total old→new function (§5). The mode choice has **exactly one
> producer** (the builder, at A.9) and exactly one recorded artifact
> (`reflect_post_mode:` in frontmatter). Extension to a future `--reflect 3` is a new row in
> one table, not a fourth knob.

---

## 1. Problem

`task-builder/SKILL.md` emits ONE fixed POST reflect item as the penultimate item of the
final phase (`SKILL.md:1994-1999`). Its Action already bakes the heavyweight
`/sc:reflect --mode post --remediate … --depth {DEPTH}` fresh-session command, writes
`reflect_post: PENDING`, STOPs, and HALTs until an operator records the verdict in a new
session (`SKILL.md:1999`, honoring `feedback_human_decision_items_must_halt`). The item is
**correct on the property that matters** — executor-disjoint review — but it is
**one-size-fits-all and fully manual**: a 4-item typo-fix tasklist and a 12-subsystem
refactor both get the identical `--depth deep --remediate` fresh-session ceremony.

Two adjacent facts make this ripe for a dial:

1. The **sibling wrapper** (`superclaude reflect run`, already merged, convergence 0.82)
   turns the manual HALT into an **unattended** top-level subprocess that escapes the
   Agent-tool nesting limit so reflect's Tier 2 actually fans out, captures the contract,
   and writes `reflect_post` back fail-closed. This is the automation target for the
   heavyweight mode.
2. For **low-complexity / low-risk** tasklists, a full executor-disjoint deep audit is
   over-spend; a lighter **inline `/sc:reflect --mode post --depth standard`** run in the
   executor's own session — audit-only, no remediation — is a defensible cheaper tier when
   the tasklist carries no human-decision (S5) or refactor-class (S6) signal.

We want `--reflect auto|1|2` (**default 2**) to pick the POST item's *form* and *rigor* at
**build time**, deterministically, so two implementers compute the identical emitted item
from the same BUILD_REQUEST. The flag governs **only the POST template** — it does NOT touch
the PRE gate (A.10.7, `SKILL.md:1407-1429`), which runs inside the builder via Agent/Task at
build time and is out of scope.

**Why an architect leads this.** The hard part is not the three item bodies; it is making
the three pre-existing knobs collapse without breaking back-compat and without leaving a
schema where a reader must consult two fields to know the gate's behavior. The variant that
wins is the one whose reconciliation is a **total function** with a **single winner rule**,
whose `auto` selection is a **pure arithmetic predicate reusing the TCS machinery that
already exists** (no second complexity model), and whose validation can mechanically prove
"emitted item == selected mode" from the frontmatter alone.

---

## 2. Functional Requirements

Each FR is independently testable. "Emitted item" = the penultimate final-phase item the
builder writes. "Selected mode" = the resolved `m ∈ {none,1,2}` (auto resolves to 1 or 2).

- **FR-1 — One dial, ordinal domain.** The builder accepts `--reflect <value>` with
  `value ∈ {none, 0, 1, 2, auto}`, where `0` is an accepted alias of `none`. The resolved
  *effective mode* is `m ∈ {none, 1, 2}` (auto → 1 or 2 per §4). Default = `2`. No other
  flag and no other BUILD_REQUEST field may independently set the POST gate's form (FR-9
  enforces this). **Testable:** parsing each of the 5 tokens yields the documented `m`;
  unknown token → MALFORMED-input STOP (§10).

- **FR-2 — `--reflect none|0` disables the gate (= old `POST_REFLECT_GATE: DISABLED`).** When
  `m == none`, the builder emits **no** POST reflect item; the final phase goes straight from
  the last QA/validation item to `Update task status to Done`. Frontmatter records
  `reflect_post_mode: none` and `reflect_post:` is **omitted entirely** (no PENDING sentinel,
  since there is no gate to resolve). **Testable:** generated tasklist has zero
  `/sc:reflect`/`reflect run` tokens in the final phase and no `reflect_post:` key.

- **FR-3 — `--reflect 1` emits an INLINE same-session audit-only item.** Action runs
  `/sc:reflect --mode post --depth standard` as a **top-level skill invocation by the `/task`
  executor in the SAME session** — NOT Agent/Task, NOT a shell-out, NO `--remediate`. Depth
  is fixed at `standard` (§7). The item HALTs on non-pass and writes `reflect_post` back
  (FR-7, FR-8). **Testable:** emitted Action contains literal `/sc:reflect --mode post
  --depth standard`, contains neither `--remediate` nor `superclaude reflect run` nor any
  `Agent`/`Task`/`subagent` token, and is penultimate.

- **FR-4 — `--reflect 2` (DEFAULT) emits a Bash shell-out to the wrapper (= old
  `POST_REFLECT_MODE: wrapper`).** Action Bash-shells `superclaude reflect run {TASK_FILE}`
  as a top-level subprocess (never Agent/Task, per `reference_subagent_cannot_nest_skill_fanout`
  and the sibling NFR-7). The wrapper internally runs reflect `--depth deep --remediate`
  executor-disjoint with the full Tier-2 + Tier-3 chain. The builder bakes the
  TCS-derived `--depth` and `<BASE>` as passthrough (single TCS producer — sibling FR-3).
  **Testable:** emitted Action contains literal `superclaude reflect run`, is a Bash
  shell-out (not Agent/Task), and is penultimate.

- **FR-5 — `--reflect auto` resolves to 1 or 2 deterministically (§4 FER).** The resolved
  value is recorded as `reflect_post_mode: auto-resolved-1` or `auto-resolved-2` in
  frontmatter (FR-10); the emitted item is byte-identical to the corresponding fixed-mode
  item (FR-3 or FR-4). **Testable:** two implementers given the same finished MDTM +
  BUILD_REQUEST + wrapper-availability compute the same resolution and the same item bytes.

- **FR-6 — `--reflect` subsumes `POST_REFLECT_GATE` and `POST_REFLECT_MODE` (total old→new
  map, §5).** The legacy `POST_REFLECT_GATE: ENABLED|DISABLED` field and the sibling's
  proposed `POST_REFLECT_MODE: wrapper|halt` field are **retired as independent inputs** and
  reinterpreted as positions on the dial via the §5 map. When BOTH a `--reflect` value and a
  legacy field are present, **`--reflect` wins** (precedence §10); when only legacy fields are
  present, the §5 map computes `m`; when neither is present, `m = 2` (default). The
  reconciliation is a **total function** — every legacy combination maps to exactly one `m`.
  **Testable:** the §5 truth table round-trips: each legacy combination → one `m` → one
  emitted item.

- **FR-7 — Every emitted item (modes 1, 2) HALTs on non-pass and writes `reflect_post`
  back.** Regardless of mode, the item's Completion-gate requires a `pass`/`success` verdict
  before `Update task status to Done` may proceed; any non-pass verdict HALTs and routes the
  report + reason into the tasklist `### Open Questions` (never auto-execute, never
  auto-proceed — `feedback_human_decision_items_must_halt`). Mode 1 captures the inline
  reflect verdict into `reflect_post`; Mode 2 reads the verdict the wrapper already wrote
  (sibling FR-6/FR-8). **Testable:** each emitted item's Completion-gate text contains a HALT
  clause and a `reflect_post` write-back clause; no item self-resolves to Done on non-pass.

- **FR-8 — `--remediate` scope is mode-fixed.** Mode 1 is **audit-only** (no `--remediate`);
  Mode 2 runs `--remediate` (inside the wrapper). When Mode 2's remediation surfaces a Tier-3
  corrective task, the completion-gate **HALTs and routes the Tier-3 task into `### Open
  Questions`; it NEVER auto-executes** the corrective tasklist (the wrapper's `--no-promote`
  default and fail-closed verdict enforce this — sibling FR-8/FR-9). **Testable:** Mode 1
  Action has no `--remediate`; Mode 2 completion-gate text states Tier-3 → Open Questions +
  HALT, no auto-exec.

- **FR-9 — Single producer of the mode choice.** The resolved `m` is computed **once**, at
  A.9 (the BUILD_REQUEST/flag-parse + POST gate logic site), and consumed by (a) the emitted
  item template, (b) the `reflect_post_mode:` frontmatter write, and (c) the validation
  assertions. No downstream surface recomputes `m`. **Testable:** `reflect_post_mode:` in the
  generated frontmatter and the emitted item's command shape are always mutually consistent
  (the FR-9.5 invariant validation, §9, asserts exactly this).

- **FR-10 — Mode 2 wrapper-availability is detected at build time with a frozen fallback
  ladder (§8).** Before emitting a Mode-2 (or auto→2) item, the builder probes wrapper
  availability (`superclaude reflect --help` resolves / the `reflect` subcommand is
  registered). If absent, it applies the §8 fallback (degrade to the manual-HALT item, NOT to
  Mode 1, NOT a build STOP) and records the degradation in frontmatter. **Testable:** with
  wrapper absent + `--reflect 2`, the emitted item is the manual-HALT shape (§6.4) and
  `reflect_post_mode: 2-degraded-halt` is recorded.

- **FR-11 — Mode 1 nesting-boundary guard.** The Mode-1 emitted item carries an explicit
  precondition: the `/task` executor must be **top-level** (not itself an Agent-tool
  subagent), because an inline `/sc:reflect` inside an Agent-tool subagent silently loses
  reflect's Tier-2 fan-out (`reference_subagent_cannot_nest_skill_fanout`). The item's
  Verification checks the executor frame and, if the executor is a subagent, **HALTs with a
  `reflect_post: BLOCKED reason: mode1-nested-executor` write-back** rather than producing a
  silently-degraded audit (§6.2, §6.5). **Testable:** Mode-1 item Verification text contains
  the top-level-executor precondition and the nested-executor HALT branch.

- **FR-12 — `--spec` threading preserved across all modes.** The `spec_path` resolved at A.2
  (`SKILL.md:41`) is threaded into the Mode-1 inline command (`[--spec {SPEC_PATH}]`) and is
  available to the Mode-2 wrapper via frontmatter `spec_path` (sibling FR-3). Mode `none`
  omits it (no gate). **Testable:** when `spec_path` resolves, Mode-1 Action contains `--spec
  {SPEC_PATH}`; when it does not, the optional token is absent.

---

## 3. Non-Functional Requirements

- **NFR-1 — No reflect-logic duplication.** Emitted items only *invoke* (`/sc:reflect`,
  Mode 1) or *shell out to the wrapper* (`superclaude reflect run`, Mode 2). No
  deviation-taxonomy, tier-rubric, depth-derivation, or verdict-classification logic is
  authored into any emitted item. The builder's only added logic is mode resolution + depth
  passthrough (it already owns TCS at `SKILL.md:2114+`).
- **NFR-2 — Back-compat / reversibility.** Default `2`. The §5 map is total and lossless for
  the two behaviors that exist today (ENABLED-wrapper, ENABLED-halt, DISABLED). The
  manual-HALT path (`m=2` degraded, and the retained-HALT position) restores
  `SKILL.md:1994-1999`'s text **byte-for-byte** so a downstream diff of "old behavior" is
  empty.
- **NFR-3 — Single source of truth for the mode.** Exactly one frontmatter field
  (`reflect_post_mode:`) records the resolved mode; exactly one builder site (A.9) computes
  it. `verify-sync` and rf-qa read that field, never re-derive.
- **NFR-4 — Extensibility.** Adding a future tier (e.g. `--reflect 3` = inline-deep, or a
  vendor-diverse variant) is **one new row** in the §4 resolution table + §5 map + §6
  templates + §9 validation matrix — never a new top-level knob. The ordinal domain
  `{none,1,2,auto}` is designed to widen monotonically.
- **NFR-5 — Determinism.** Mode resolution (including `auto`) is pure arithmetic over signals
  already extracted by the TCS machinery + a boolean wrapper-availability probe. No
  free-inference except the existing bounded ±4 TCS tiebreaker, which is recorded.
- **NFR-6 — SoT discipline.** All edits land in `src/superclaude/skills/task-builder/SKILL.md`
  → `make sync-dev` → `.claude/`; never stage `.claude/` mirrors (CLAUDE.md ABSOLUTE RULE,
  `feedback_claude_dir_gitignored`).
- **NFR-7 — No-nesting guard is testable.** Mode 2 = Bash shell-out only; Mode 1 = inline by a
  top-level executor only. rf-qa asserts the command shape and the nesting precondition (§9).
- **NFR-8 — Fail-closed default posture.** Wrapper-absent (§8) and Mode-1-nested-executor
  (FR-11) both route to a HALT, never to a silent auto-proceed or a silently-weaker audit.

---

## 4. The `auto` Frozen-Extraction Rule

> **Design principle:** `auto` must NOT introduce a second complexity model. It **reuses the
> TCS already computed** for the POST `--depth` (`SKILL.md:2114-2155`) and the same S5/S6
> signals that already drive overrides O1/O2. This guarantees the auto choice and the depth
> choice are derived from one arithmetic source — no drift, one producer (NFR-3, NFR-5).

### 4.1 Inputs (all already extracted by the builder; no new extraction)

| Symbol | Source | Definition |
|---|---|---|
| `TCS` | `SKILL.md:2134` | `3·S1 + 4·S2 + 2·S3 + 2·S4 + 5·S5 + 4·S6` (computed on the finished MDTM file) |
| `S5` | `SKILL.md:2126` | distinct human-decision / OQ-blocked items (×5 in TCS) |
| `S6` | `SKILL.md:2127` | file-level refactor/remediation class (0 or 1, ×4 in TCS) |
| `W` | §8 probe | wrapper-available boolean (`superclaude reflect run` resolvable) |

### 4.2 The selection predicate (frozen, total, first-match-wins)

```text
RESOLVE_AUTO(TCS, S5, S6, W):
  # Gate 0 — wrapper availability is a hard precondition for Mode 2.
  if W == false:
      return 1            # auto can only pick 1 when the wrapper is absent
                          # (Mode 1 needs no wrapper); the §8 ladder does NOT
                          # apply to auto — auto simply selects the available tier.

  # Gate 1 — risk/human-decision forces the executor-disjoint heavyweight tier.
  if S6 == 1:  return 2   # refactor/remediation class — regression risk → Mode 2
  if S5 >  0:  return 2   # any human-decision/halt-point item → Mode 2

  # Gate 2 — complexity band on the SAME TCS used for depth.
  if TCS >= 35: return 2  # 'deep' band (forced Tier-2) → executor-disjoint Mode 2
  if TCS <= 12: return 1  # 'quick' band → inline standard audit is proportionate

  # Gate 3 — the 'standard' band (13..34): proportionality default.
  #   Mode 1 (inline standard, audit-only) is the proportionate choice unless a
  #   secondary breadth signal pushes it up. Breadth signal = distinct subsystems S2.
  if S2 >= 3:  return 2   # ≥3 subsystems → cross-cutting → executor-disjoint Mode 2
  return 1                # otherwise inline standard audit
```

**Why these cut-points (architect defense):**

- **Gate 0 first** because Mode 2 is *physically impossible* without the wrapper; auto must
  never resolve to an un-runnable item. (This differs from the fixed `--reflect 2` fallback
  ladder in §8: a fixed `2` request degrades to *manual-HALT*; an `auto` request simply
  *selects 1*, because the operator asked the builder to choose and 1 is choosable.)
- **S6/S5 before the band** mirrors overrides O2/O1 (`SKILL.md:2150,2149`): refactor-class
  and human-decision items are *exactly* the classes that flip reflect to Tier 2, so they
  must get the executor-disjoint mode regardless of raw TCS.
- **TCS band reuse** means `auto` and the depth derivation read one number. The `deep` band
  (≥35) → Mode 2; the `quick` band (≤12) → Mode 1. The middle `standard` band (13..34) is the
  only place a genuine choice is made, and it is resolved by **breadth (S2 ≥ 3)** — the same
  signal that S2's ×4 weight already privileges — keeping the dial monotone with TCS.

### 4.3 Worked example

A tasklist with: S1 = 6 files, S2 = 2 subsystems, S3 = 4 FRs, S4 = 3 deps, S5 = 0
human-decision items, S6 = 0 (type `Feature`), wrapper available `W = true`.

```text
TCS = 3·6 + 4·2 + 2·4 + 2·3 + 5·0 + 4·0
    = 18 + 8 + 8 + 6 + 0 + 0 = 40
RESOLVE_AUTO(TCS=40, S5=0, S6=0, W=true):
  Gate 0: W==true        → continue
  Gate 1: S6==0, S5==0   → continue
  Gate 2: TCS=40 >= 35   → return 2
```

→ **auto resolves to 2** (`reflect_post_mode: auto-resolved-2`), emitting the §6.3 (= §6.2
Mode-2) shell-out item with `--depth deep` baked as passthrough. Cross-check: the §7 depth
derivation independently bands TCS=40 → `deep`, so the auto-mode and the baked depth agree by
construction — the single-producer guarantee.

A contrasting example — S1 = 3, S2 = 1, S3 = 0, S4 = 1, S5 = 0, S6 = 0, `W = true`:

```text
TCS = 3·3 + 4·1 + 0 + 2·1 + 0 + 0 = 9 + 4 + 2 = 15
Gate 0: continue; Gate 1: continue; Gate 2: 15 not≥35, 15 not≤12 → continue;
Gate 3: S2=1 (<3) → return 1
```

→ **auto resolves to 1** (`reflect_post_mode: auto-resolved-1`), inline `--depth standard`
audit-only.

---

## 5. Knob Reconciliation + old→new Map

> The three knobs collapse onto **one ordinal dial**. `--reflect` is the **sole input**;
> the two legacy fields become *derived* inputs consulted only when `--reflect` is absent.
> Precedence (highest first): explicit `--reflect` flag → `--reflect` BUILD_REQUEST field →
> §5 legacy-field map → default `2`.

### 5.1 The dial

| Dial position | Meaning | Emitted item |
|---|---|---|
| `none` (`0`) | gate disabled | none (§6.1) |
| `1` | inline same-session, `--depth standard`, audit-only, NOT executor-disjoint | §6.2 |
| `2` (default) | wrapper shell-out, `--depth deep --remediate`, executor-disjoint | §6.3 |
| `auto` | builder resolves 1 or 2 per §4 | §6.2 or §6.3 (+ `auto-resolved-{1,2}`) |
| `2-degraded-halt` | (derived only, §8) wrapper absent under fixed `2` | §6.4 manual-HALT |

### 5.2 old→new total map

The legacy surface had `POST_REFLECT_GATE ∈ {ENABLED, DISABLED}` (`SKILL.md:853`; absence ⇒
ENABLED for built tasks today) crossed with the sibling's proposed
`POST_REFLECT_MODE ∈ {wrapper, halt}` (default `halt`). Every cell maps to one dial position:

| Legacy `POST_REFLECT_GATE` | Legacy `POST_REFLECT_MODE` | New effective `m` | Emitted item | Notes |
|---|---|---|---|---|
| `DISABLED` | (any) | `none` | §6.1 (no item) | direct old→new |
| (absent / `ENABLED`) | `halt` (or absent) | `2` then **§8 manual-HALT if you want byte-identical old behavior** → see note | §6.4 manual-HALT | **Back-compat anchor**: this is today's `SKILL.md:1994-1999`. To preserve it byte-for-byte under the new schema, `POST_REFLECT_MODE: halt` maps to the **retained manual-HALT position** (`reflect_post_mode: halt`), NOT to wrapper Mode 2. See §5.3. |
| (absent / `ENABLED`) | `wrapper` | `2` | §6.3 shell-out | sibling's automated path == Mode 2 |
| explicit `--reflect <v>` present | (any legacy) | `<v>` | per `<v>` | **`--reflect` always wins**; legacy fields ignored with a one-line note in build log |

### 5.3 The retained manual-HALT position (`halt`)

To honor NFR-2 (byte-for-byte reversibility) and the sibling's `POST_REFLECT_MODE: halt`
default, the dial carries a **fifth ordinal-adjacent position `halt`** that is *not*
selectable via the numeric `--reflect 1|2` surface but **is** reachable via:

- legacy `POST_REFLECT_MODE: halt` (the sibling default), or
- `--reflect 2` when the wrapper is **absent** (§8 degradation → `2-degraded-halt`).

`halt` emits the **current** `SKILL.md:1994-1999` manual fresh-session item verbatim
(`reflect_post_mode: halt`). This keeps three truths simultaneously: (a) the **numeric dial**
is the clean forward surface (`1`/`2`/`auto`); (b) the **manual-HALT behavior survives**
unchanged for callers who want it or whose wrapper is missing; (c) there is still exactly one
field (`reflect_post_mode`) telling a reader which of `{none,1,2,auto-resolved-1,
auto-resolved-2,halt,2-degraded-halt}` is in force. **No second knob.**

### 5.4 Why subsume rather than coexist (architect rationale)

Keeping `POST_REFLECT_GATE` + `POST_REFLECT_MODE` + `--reflect` as three live fields would
require a reader to evaluate a 3-input precedence lattice at every gate. Collapsing to one
dial with a total old→new map means: (1) the BUILD_REQUEST schema shrinks by one field net
(retire two, add one); (2) the precedence is a single linear order; (3) `reflect_post_mode`
is the lone authority both at write-time and at rf-qa-time. This is the SoT win the lens
demands.

---

## 6. Per-Mode Emitted-Item Templates

> Literal Action/Output/Verification/Completion-gate text. Placeholders `{TASK_FILE}`,
> `{SPEC_PATH}`, `{DEPTH}`, `{BASE}`, `{EXECUTOR_CLASS}` are resolved at A.9 exactly as the
> current template resolves them (`SKILL.md:1996`). All non-`none` items are **penultimate**
> (immediately before `Update task status to Done`), preserving anti-orphaning
> (`SKILL.md:2100`, Critical Rule 15).

### 6.1 `none` — no item

The final phase contains no reflect item. `reflect_post:` key is omitted from frontmatter;
`reflect_post_mode: none` is written. (Restores old `POST_REFLECT_GATE: DISABLED`.)

### 6.2 Mode 1 — inline same-session, audit-only

```markdown
- [ ] **N.{X-1} — Inline post-execution reflect audit (same session, audit-only, HALT)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates
    ran in THIS executor's frame; this item adds a `/sc:reflect --mode post` audit at
    `--depth standard`. NOTE: this audit runs in the SAME session as the executor, so it is
    NOT executor-disjoint — it shares the executor's representational frame (see §4 of the
    spec for when Mode 1 is acceptable: low TCS, no human-decision/refactor signal). It is
    audit-only (no remediation). PRECONDITION: this `/task` executor MUST be top-level. If
    this executor is itself an Agent-tool subagent, an inline `/sc:reflect` silently loses
    reflect's Tier-2 fan-out (`reference_subagent_cannot_nest_skill_fanout`) — in that case do
    NOT run a degraded audit; HALT per the Verification branch below.
  - **Action**: Confirm this executor is top-level (not an Agent/Task subagent). Then, in
    THIS session, run the skill `/sc:reflect --mode post --depth standard --diff {BASE}..HEAD
    --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --executor-model {EXECUTOR_CLASS}` as a
    top-level skill invocation (NOT via Agent/Task, NOT a shell-out, and WITHOUT
    `--remediate`). Capture reflect's return contract.
  - **Output**: Frontmatter `reflect_post: {verdict, run_id, report, reviewed_at}` written
    from the inline reflect contract; `reflect_post_mode: 1` (or `auto-resolved-1`).
  - **Verification**: If the executor is an Agent-tool subagent → write `reflect_post:
    {verdict: blocked, reason: mode1-nested-executor}` and HALT (do NOT proceed to Done).
    Else, `reflect_post.verdict` is recorded from the inline run and the report path exists.
  - **Completion gate**: `reflect_post.verdict == pass` (clean, full audit) → the
    Update-status-to-Done item may proceed. ANY other verdict (or a `blocked` nested-executor
    result) HALTs; append the report + reason to `### Open Questions` and STOP (HALT per
    `feedback_human_decision_items_must_halt`). The item NEVER auto-proceeds on non-pass.
```

### 6.3 Mode 2 (DEFAULT) — wrapper shell-out, remediate

```markdown
- [ ] **N.{X-1} — Independent post-execution reflect gate (wrapper subprocess, HALT)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates
    ran in THIS executor's frame and cannot perform an executor-disjoint audit. This item
    shells out to the `superclaude reflect run` wrapper, which launches `/sc:reflect --mode
    post` as a TOP-LEVEL subprocess (escaping the Agent-tool nesting limit so reflect's Tier-2
    heterogeneous-reviewer fan-out actually runs), at `--depth deep --remediate`,
    executor-disjoint. Per `feedback_sc_reflect_vs_inline_rfqa`, this catches spec-literal,
    invariant-arithmetic, and orphan blindspots that same-frame QA misses.
  - **Action**: Run, as a Bash shell-out (NEVER via Agent/Task, per
    `reference_subagent_cannot_nest_skill_fanout`): `superclaude reflect run {TASK_FILE}`. The
    wrapper derives `--diff {BASE}..HEAD`, `--depth {DEPTH}` (TCS-passthrough, floored
    `standard` per O4; `deep` for this default mode), `--spec` (from frontmatter `spec_path`),
    and `--executor-model {EXECUTOR_CLASS}`, runs reflect with `--remediate`, and writes the
    `reflect_post:` verdict block back fail-closed. Do NOT run reflect inline.
  - **Output**: Frontmatter `reflect_post: {verdict, status, run_id, tier_reached, report,
    contract, reason, deviations, head, reviewed_at}` written by the wrapper;
    `reflect_post_mode: 2` (or `auto-resolved-2`).
  - **Verification**: The wrapper exited and `reflect_post.verdict ∈ {pass, halted, degraded,
    blocked}` is recorded. Only `pass` (exit 0) clears the gate.
  - **Completion gate**: `reflect_post.verdict == pass` → the Update-status-to-Done item may
    proceed. ANY of `halted | degraded | blocked` HALTs. If remediation surfaced a Tier-3
    corrective task, append it (report + reason + deviations) to `### Open Questions` and STOP
    — NEVER auto-execute the corrective tasklist (the wrapper's `--no-promote` default
    enforces audit-only; `feedback_human_decision_items_must_halt`).
```

### 6.4 `halt` / `2-degraded-halt` — retained manual fresh-session item

This is the **current** `SKILL.md:1994-1999` item, emitted **verbatim** (byte-for-byte), with
the sole addition of `reflect_post_mode: halt` (or `2-degraded-halt`) in frontmatter. Reached
via legacy `POST_REFLECT_MODE: halt` or §8 wrapper-absent degradation under fixed `--reflect
2`. (Action: write `reflect_post: PENDING`, STOP, surface the paste-ready `/sc:reflect --mode
post --remediate …` fresh-session command; Completion-gate: operator runs reflect in a fresh
session and records the verdict — HALT.)

### 6.5 auto-resolved

`auto` emits **either §6.2 or §6.3 verbatim** depending on §4's resolution, and writes
`reflect_post_mode: auto-resolved-1` or `auto-resolved-2`. No third template body exists —
this is the extensibility property (NFR-4): the resolved mode reuses the fixed-mode bodies.

---

## 7. Depth/TCS Reconciliation

**Decision: mode fixes depth for fixed `1`/`2`; `auto` USES TCS to pick the mode and the mode
inherits its fixed depth — there is never a contradiction because the auto cut-points are
aligned to the TCS bands.**

| Mode | POST `--depth` | Source |
|---|---|---|
| `1` (fixed) | `standard` | fixed by the mode (inline tier never deep) |
| `2` (fixed) | `deep` | fixed by the mode (wrapper heavyweight tier) |
| `auto→1` | `standard` | inherited from resolved Mode 1 |
| `auto→2` | `deep` | inherited from resolved Mode 2 |
| `halt` | `max(TCS-band, standard)` | the retained manual item keeps the **existing** TCS-derived depth (`SKILL.md:1996,2152`) |

**Fate of override O4 (`SKILL.md:2152`, "POST never `quick`").** O4 is **preserved and
strengthened**, never deleted:

- For fixed `1`/`2` and `auto→{1,2}`, depth is `standard` or `deep` by construction — O4's
  "never `quick`" floor is **automatically satisfied** (no mode yields `quick`). O4 becomes a
  redundant-but-true invariant for these paths; rf-qa still asserts it (a `quick` POST depth
  on any non-`halt` mode = MALFORMED).
- For the **retained `halt` mode**, O4 applies exactly as today: the manual command floors at
  `standard` when the band yields `quick`.
- Overrides **O1** (S5>0 ⇒ floor standard) and **O2** (S6=1 ⇒ force deep) are now *also*
  expressed at the mode layer for `auto` (Gate 1 of §4 returns 2 for S5>0 or S6=1, and Mode 2
  is `deep`). So O1/O2 and the auto FER **agree by construction**; the depth machinery remains
  the single producer and the auto rule is a thin band-reading wrapper over it, never a
  competing model. **O1/O2/O3 are NOT removed** — they continue to govern the baked `{DEPTH}`
  passthrough for the `halt` mode and the wrapper-passthrough depth value.

**Why mode-fixes-depth rather than depth-fixes-mode (architect call):** depth is a *property
of the chosen tier*, not an independent dial. Letting depth drift independently of mode would
re-introduce two producers. By making `auto` read TCS to pick the mode and the mode then
dictate its own depth, there is exactly one arithmetic source (TCS) and one decision point
(A.9). Fixed `1`/`2` simply pin the tier (and thus the depth) explicitly.

---

## 8. Wrapper-Dependency Fallback

**Decision: wrapper absent under fixed `--reflect 2` → degrade to the retained manual-HALT
item (§6.4), record `reflect_post_mode: 2-degraded-halt`. Do NOT degrade to Mode 1; do NOT
STOP the build.**

### 8.1 Detection (build time, at A.9)

The builder probes wrapper availability with a frozen check: the `reflect` subcommand is
registered (`superclaude reflect --help` exits 0 / `superclaude --help` lists `reflect`). The
probe result `W ∈ {true,false}` is computed once and reused by §4 (`auto`) and §8.

### 8.2 The fallback ladder (frozen, deterministic)

| Requested | `W` | Emitted item | `reflect_post_mode` |
|---|---|---|---|
| `none` | (any) | none | `none` |
| `1` | (any) | §6.2 inline (no wrapper needed) | `1` |
| `2` | true | §6.3 shell-out | `2` |
| `2` | **false** | **§6.4 manual-HALT** | `2-degraded-halt` |
| `auto` | true | §4 → §6.2 or §6.3 | `auto-resolved-{1,2}` |
| `auto` | **false** | §4 Gate-0 → §6.2 inline Mode 1 | `auto-resolved-1` |

### 8.3 Rationale for the asymmetry (architect defense)

- A **fixed `2`** request is an explicit operator demand for the *executor-disjoint*
  property. Silently downgrading to **Mode 1** would **break the very property the operator
  asked for** (inline Mode 1 is NOT executor-disjoint — FR-3) without surfacing it. The
  honest fallback is the **manual HALT**, which *preserves* executor-disjointness (the
  operator runs reflect in a fresh session) at the cost of automation — fail-closed, never a
  silent weakening (NFR-8). A build-time STOP is rejected because it would block task delivery
  on a missing *optional automation*; the manual gate is the long-standing, correct default.
- An **`auto`** request delegates the choice to the builder; when the wrapper is absent, the
  builder may legitimately *choose* the available automated tier — Mode 1 — because the
  operator did not demand executor-disjointness (§4 Gate 0). This is the principled split:
  *fixed* request preserves its demanded property via HALT; *auto* request adapts its choice.

The degradation is always recorded in frontmatter (`*-degraded-halt` / `auto-resolved-1`) so
rf-qa and the operator can see the wrapper was unavailable.

---

## 9. Validation + rf-qa Changes

> All changes assert **emitted item == `reflect_post_mode`** mechanically. The single
> frontmatter field is the oracle; rf-qa never re-derives the mode.

### 9.1 Replace present-and-penultimate assertion (`SKILL.md:2051`)

Old: *"POST reflect item present and positioned penultimate … when POST_REFLECT_GATE is
ENABLED — MALFORMED if omitted."*

New:

```text
- [ ] POST reflect item presence + penultimate position MATCH `reflect_post_mode`:
      - mode `none` → NO reflect item in the final phase; `reflect_post:` key absent.
      - mode `1` / `auto-resolved-1` → exactly one inline `/sc:reflect --mode post
        --depth standard` item (no `--remediate`, no `superclaude reflect run`, no
        Agent/Task token), positioned penultimate (immediately before Update-status-to-Done).
      - mode `2` / `auto-resolved-2` → exactly one `superclaude reflect run {TASK_FILE}`
        Bash shell-out item (no inline `/sc:reflect`, no `--depth quick`), penultimate.
      - mode `halt` / `2-degraded-halt` → the manual fresh-session `/sc:reflect --mode post
        --remediate` HALT item, penultimate, writing `reflect_post: PENDING`.
      Any mismatch between the emitted item's command shape and `reflect_post_mode` =
      MALFORMED. Item omitted for a non-`none` mode = MALFORMED.
```

### 9.2 Rewrite validation Critical Rule 19 (`SKILL.md:2108`)

Old rule 19 keys off `POST_REFLECT_GATE: ENABLED` and asserts a single fresh-session shape.
New rule 19 keys off the resolved `reflect_post_mode` and asserts the §9.1 mode-specific
shape, plus:

- Every non-`none` emitted item **HALTs on non-pass and writes `reflect_post` back** (FR-7) —
  a Completion-gate lacking the HALT + `reflect_post` write-back = MALFORMED.
- Mode 1 item **carries the top-level-executor precondition + nested-executor HALT branch**
  (FR-11); absence = MALFORMED.
- Mode 2 item is a **Bash shell-out, never Agent/Task** (NFR-7); an Agent/Task-wrapped
  `reflect run` = MALFORMED.
- Re-execution, when present, uses `/task` (never `/sc:task`) — unchanged.

### 9.3 New rf-qa task-integrity assertion (the FR-9 invariant)

Add a task-integrity check (the per-gate `task-integrity` counter at `SKILL.md:2094`):

```text
- [ ] reflect_post_mode invariant: the frontmatter `reflect_post_mode` value is one of
      {none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt} AND the emitted
      final-phase reflect item's command shape (per §9.1) is consistent with it. A
      `reflect_post_mode: 2` with an inline `/sc:reflect` body (or vice-versa) = MALFORMED.
      `reflect_post_mode: none` with any reflect item present = MALFORMED.
```

This is the rf-qa expression of FR-9's single-producer guarantee: the frontmatter field and
the item body cannot disagree.

### 9.4 Wire-string / sentinel preservation

The `reflect_post: ""` PENDING sentinel (`SKILL.md:1942`) is retained **only** for the `halt`
/ `2-degraded-halt` modes (which still defer to a fresh session). For modes 1 and 2 the
`reflect_post:` block is written by the inline run / wrapper respectively; for mode `none` the
key is absent. rf-qa asserts the sentinel's presence/absence matches the mode.

---

## 10. Flag Plumbing + Frontmatter + BUILD_REQUEST

### 10.1 Parse site + precedence

`--reflect` is parsed at the BUILD_REQUEST / flag-resolution stage and consumed at **A.9**
(the POST gate logic site, co-located with `POST_REFLECT_GATE` at `SKILL.md:853`). Resolution
order (highest wins, first match):

1. explicit `--reflect <value>` flag on the build invocation;
2. `REFLECT:` field in a BUILD_REQUEST file (new field, value `none|0|1|2|auto`);
3. **legacy §5 map**: `POST_REFLECT_GATE` × `POST_REFLECT_MODE` → `m` (consulted only if 1–2
   absent);
4. **default `2`**.

When a higher-precedence source is present, lower legacy fields are ignored and a one-line
note is written to the build log (`--reflect <v> wins; legacy POST_REFLECT_* ignored`). Mode
resolution (including `auto` → §4 and wrapper-probe → §8) happens **once** at A.9 (FR-9).

### 10.2 BUILD_REQUEST schema change (at `SKILL.md:853`)

Retire `POST_REFLECT_GATE: ENABLED` + sub-fields as the *primary* surface; introduce:

```text
REFLECT: 2            # one of: none | 0 | 1 | 2 | auto   (default 2 when absent)
  SPEC_PATH: <spec_path or NONE>     # threaded to Mode 1 inline / Mode 2 wrapper (§12)
  # DEPTH is no longer an author-settable POST sub-field: it is mode-derived
  # (1→standard, 2→deep, halt→max(TCS,standard)) — single producer, §7.
  TASK_FILE: ${TASK_FILE}
```

Legacy `POST_REFLECT_GATE` / `POST_REFLECT_MODE`, if present in an older BUILD_REQUEST, are
honored via the §5 map (precedence step 3) for back-compat, then deprecated.

### 10.3 Frontmatter field (replaces / augments `SKILL.md:1942`)

```yaml
reflect_post_mode: none | 1 | 2 | auto-resolved-1 | auto-resolved-2 | halt | 2-degraded-halt
reflect_post: ""    # PENDING sentinel — ONLY for halt / 2-degraded-halt; written by
                    # inline run (mode 1) or wrapper (mode 2); ABSENT for mode none.
```

`reflect_post_mode` is the **single recorded artifact** of the mode decision (NFR-3) — the
oracle for all of §9. It is written once, at tasklist generation, by the A.9 producer.

---

## 11. Scope Boundaries

**In scope (this spec):**
- `task-builder/SKILL.md`: `--reflect` flag parse + precedence (A.9 / `:853`); the per-mode
  POST item templates (replace `:1994-1999`); the `auto` FER (§4); the `POST_REFLECT_GATE` +
  `POST_REFLECT_MODE` reconciliation / old→new map (§5); depth/TCS reconciliation incl. O4
  fate (§7, `:2114-2155`); wrapper-availability probe + fallback ladder (§8); validation
  rewrites (`:2051`, `:2108`) + new rf-qa task-integrity invariant (§9); BUILD_REQUEST
  `REFLECT:` field (`:853`) + `reflect_post_mode:` frontmatter field (`:1942`); `--spec`
  threading preservation (`:41`).
- `make sync-dev` after every `src/` edit; never stage `.claude/` mirrors.

**Out of scope (hard non-goals):**
- Building or modifying the `superclaude reflect run` wrapper (sibling spec, already merged).
- Modifying `sc-reflect-protocol` (the reflect skill itself).
- Changing the PRE gate (A.10.7, `:1407-1429`) — `--reflect` governs the POST template only;
  the PRE gate's internal Agent/Task spawn is untouched.
- Any `sc:cli-portify` work.
- Emitted items duplicating reflect logic — they only invoke (Mode 1) or shell out (Mode 2).

---

## 12. Risks

- **R1 — Three-knob precedence confusion (the core risk this design targets).** Mitigated by
  the §5 total old→new map + a single linear precedence order (§10.1) + the single
  `reflect_post_mode` artifact. Falsifier: a BUILD_REQUEST with `--reflect 1` + legacy
  `POST_REFLECT_MODE: wrapper` must deterministically emit Mode 1 — the rf-qa invariant (§9.3)
  catches any disagreement.
- **R2 — `auto` drift from depth machinery.** Mitigated by reusing the *same* TCS + S5/S6
  already computed for depth (§4, §7); the worked example (§4.3) shows auto-mode and baked
  depth agree by construction. Falsifier: an `auto→2` item with `--depth standard` would prove
  drift; §7's table forbids it and §9.1 flags `--depth quick`/mismatch as MALFORMED.
- **R3 — Mode 1 silent Tier-2 loss under a subagent executor.** This is the genuinely
  dangerous case (`reference_subagent_cannot_nest_skill_fanout`). Mitigated by FR-11's
  top-level precondition + nested-executor HALT branch (§6.2 Verification) and the §9.2
  assertion that the precondition text is present. Residual risk: detection of "am I a
  subagent" relies on the executor honoring the precondition; documented as a known limit and
  the reason Mode 1 is reserved for low-TCS/low-risk tasklists.
- **R4 — Wrapper-absent surprise.** Mitigated by the build-time probe (§8.1) + the frozen
  fallback ladder (§8.2) + the recorded `*-degraded-halt` / `auto-resolved-1` frontmatter, so
  the degradation is never silent and never weakens executor-disjointness for a fixed `2`.
- **R5 — Back-compat regression.** Mitigated by NFR-2: the `halt` position reproduces
  `:1994-1999` byte-for-byte, the §5 map is total over the legacy cells, and default `2`
  matches the sibling's automated intent. Falsifier: a diff of a `POST_REFLECT_MODE: halt`
  tasklist against today's output must be empty.
- **R6 — Extension pressure (a future `--reflect 3`).** Designed-for via NFR-4: the ordinal
  domain widens monotonically; a new tier is one row in §4/§5/§6/§9. Risk is that a future
  tier breaks the "mode fixes depth" invariant — mitigated by requiring any new tier to pin
  its own depth at definition time (the §7 contract).
