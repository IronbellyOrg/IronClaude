<!-- Provenance: produced by /sc:adversarial via /sc:brainstorm -->
<!-- Base: Variant 1 (opus:architect) -->
<!-- Merge date: 2026-06-08 -->
<!-- Non-base sources incorporated: V2 (opus:refactorer) §6 diff + §8 table; V3 (haiku:qa) §9 V1–V16 + §13 ATs -->
<!-- Convergence: 0.82 (PASS) -->

<!-- Backbone: Variant 1 — opus:architect — adversarial spec generation -->
<!-- Lens: maintainability + extension scaffolding; collapse three overlapping config knobs into one coherent surface -->
<!-- Domain: code | Strategy: systematic | Depth: deep -->

---
spec_id: task-builder-reflect-flag-post-gate-merged
title: "task-builder `--reflect auto|1|2` — 3-mode POST reflect gate dial (merged requirements)"
variant: "merged (base: 1 opus:architect; sources: V2 opus:refactorer, V3 haiku:qa)"
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
  - src/superclaude/skills/task-builder/SKILL.md:41         # --spec threading
  - src/superclaude/skills/task-builder/SKILL.md:853        # REFLECT_POST_MODE BUILD_REQUEST field (was POST_REFLECT_GATE)
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

- **FR-11 — Mode 1 nesting-boundary guard (runtime self-check PRIMARY).** The Mode-1 emitted
  item carries an explicit precondition: the `/task` executor must be **top-level** (not
  itself an Agent-tool subagent), because an inline `/sc:reflect` inside an Agent-tool
  subagent silently loses reflect's Tier-2 fan-out
  (`reference_subagent_cannot_nest_skill_fanout`). The item's Verification checks the executor
  frame **at runtime** and, if the executor is a subagent, **HALTs with a `reflect_post:
  BLOCKED reason: mode1-nested-executor` write-back** rather than producing a silently-degraded
  audit (§6.2, §6.5). The **runtime self-check is the PRIMARY guard**; a build-time
  `agent_tool_depth` frontmatter signal MAY be consulted as best-effort defense-in-depth, but
  the executor frame is generally unknown at build time, so it can never be the sole gate.
  **Testable:** Mode-1 item Verification text contains the top-level-executor precondition and
  the nested-executor HALT branch.

- **FR-12 — `--spec` threading preserved across all modes.** The `spec_path` resolved at A.2
  (`SKILL.md:41`) is threaded into the Mode-1 inline command (`[--spec {SPEC_PATH}]`) and is
  available to the Mode-2 wrapper via frontmatter `spec_path` (sibling FR-3). Mode `none`
  omits it (no gate). **Testable:** when `spec_path` resolves, Mode-1 Action contains `--spec
  {SPEC_PATH}`; when it does not, the optional token is absent.

- **FR-13 — Advisory warning on under-rigorous fixed-1 (footgun guard).**
  <!-- Source: invariant-probe INV-003, merged per Change #5 -->
  When a **fixed** `--reflect 1` is selected (not auto-resolved) AND the tasklist carries a
  risk signal (`S6 == 1 ∨ S5 > 0`), the builder emits a **non-blocking advisory build
  WARNING**: *"auto would have selected Mode 2; Mode 1 is not executor-disjoint — confirm
  intent"*. The fixed-1 request is **honored** (no STOP, no override of operator authority);
  the warning is recorded in the build log and does not change the emitted item or the
  frontmatter mode. **Testable:** building with `--reflect 1` on a tasklist with `S6=1` (or
  `S5>0`) emits the WARNING in the build log; the emitted item is still the §6.2 Mode-1
  inline item with `reflect_post_mode: 1`.

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
  free-inference except the existing bounded ±4 TCS tiebreaker, which is recorded; the auto
  predicate reads the **resolved** depth band (post-tiebreaker), so the mode choice never
  diverges from the baked depth at the band edge (§4.4, INV-004).
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

### 4.2 The selection predicate (frozen, total, 3-term, first-match-wins)

<!-- Source: V2 §4 / V3 §4 auto predicate (3-term), merged per Change #1 (drops V1's S2≥3 standard-band gate) -->
<!-- Source: invariant-probe INV-002, merged per Change #2 (risk-mode resolved FIRST, then wrapper availability) -->

The mode is resolved in **two stages**: (1) determine the *risk-mode* purely from the signals
(`S6 ∨ S5 ∨ TCS≥35`), then (2) apply wrapper availability to the resolved risk-mode. This
ordering is the INV-002 fix: a high-risk tasklist with the wrapper absent degrades to the
**manual-HALT** disjoint gate, **never** to the weakest inline Mode 1.

```text
RESOLVE_AUTO(TCS, S5, S6, W):

  # ── Stage 1 — risk-mode from the signals (wrapper-independent).
  #    S5/S6 are evaluated BEFORE the band (mirrors overrides O1/O2).
  if S6 == 1:        risk_mode := 2   # refactor/remediation class — regression risk → Mode 2
  elif S5 > 0:       risk_mode := 2   # any human-decision/halt-point item → Mode 2
  elif TCS >= 35:    risk_mode := 2   # 'deep' band (forced Tier-2) → executor-disjoint Mode 2
  else:              risk_mode := 1   # everything else → proportionate inline standard audit

  # ── Stage 2 — apply wrapper availability to the resolved risk-mode.
  if risk_mode == 1:
      return 1                        # Mode 1 needs no wrapper → inline standard audit
  # risk_mode == 2 here:
  if W == true:
      return 2                        # wrapper present → executor-disjoint shell-out
  else:
      return "2-degraded-halt"        # wrapper ABSENT but risk demanded Mode 2 →
                                      # manual-HALT (preserves executor-disjointness),
                                      # NEVER silently inline Mode 1 (INV-002 fix)
```

**Why these cut-points (architect + debate defense):**

- **The predicate is exactly the 3-term form `S6==1 ∨ S5>0 ∨ TCS≥35 → Mode 2; else Mode 1`.**
  V1's original standalone `S2 ≥ 3` standard-band gate is **removed** (Change #1, unanimous
  debate resolution C-002): `S2`'s ×4 weight in TCS **already** captures breadth, so a genuinely
  broad tasklist already crosses `TCS ≥ 35` and resolves to Mode 2 via the band. A separate
  `S2 ≥ 3` branch double-counts breadth and is the only place two implementers could disagree.
- **S6/S5 before the band** mirrors overrides O2/O1 (`SKILL.md:2150,2149`): refactor-class and
  human-decision items are *exactly* the classes that flip reflect to Tier 2, so they must get
  the executor-disjoint mode regardless of raw TCS.
- **Risk-mode resolved before wrapper availability** (Change #2 / INV-002). A high-risk
  (would-be-Mode-2) tasklist with the wrapper missing must NOT silently get the weakest inline
  audit. Resolving the risk-mode first lets the §8 ladder degrade a resolved Mode 2 to the
  **manual-HALT** disjoint gate identically to a *fixed* `--reflect 2` (§8.2) — the honest
  fallback that preserves the disjointness the risk profile demanded. A resolved Mode 1 needs
  no wrapper and is returned unchanged.
- **TCS band reuse** means `auto` and the depth derivation read one number. The `deep` band
  (≥35) → Mode 2; everything below → Mode 1. There is no separate `quick`/`standard`
  sub-decision: the dial is monotone with TCS.

### 4.3 Worked examples

<!-- Source: V1 §4.3 TCS=40 example retained; low-TCS S5>0 example added per Change #1 -->

**Example A — high TCS, clean signals → Mode 2 via the band.** A tasklist with: S1 = 6 files,
S2 = 2 subsystems, S3 = 4 FRs, S4 = 3 deps, S5 = 0 human-decision items, S6 = 0
(type `Feature`), wrapper available `W = true`.

```text
TCS = 3·6 + 4·2 + 2·4 + 2·3 + 5·0 + 4·0
    = 18 + 8 + 8 + 6 + 0 + 0 = 40
RESOLVE_AUTO(TCS=40, S5=0, S6=0, W=true):
  Stage 1: S6==0, S5==0, TCS=40 >= 35   → risk_mode = 2
  Stage 2: risk_mode==2, W==true        → return 2
```

→ **auto resolves to 2** (`reflect_post_mode: auto-resolved-2`), emitting the §6.3 (= §6.2
Mode-2) shell-out item with `--depth deep` baked as passthrough. Cross-check: the §7 depth
derivation independently bands TCS=40 → `deep`, so the auto-mode and the baked depth agree by
construction — the single-producer guarantee.

**Example B — low TCS but a human-decision item → Mode 2 via S5.** A tasklist with: S1 = 3,
S2 = 1, S3 = 1, S4 = 0, S5 = 1 (one human-decision/OQ-blocked item), S6 = 0, wrapper available
`W = true`.

```text
TCS = 3·3 + 4·1 + 2·1 + 2·0 + 5·1 + 4·0
    = 9 + 4 + 2 + 0 + 5 + 0 = 20
RESOLVE_AUTO(TCS=20, S5=1, S6=0, W=true):
  Stage 1: S6==0, but S5==1 > 0          → risk_mode = 2  (S5 fires BEFORE the band)
  Stage 2: risk_mode==2, W==true         → return 2
```

→ **auto resolves to 2** (`reflect_post_mode: auto-resolved-2`) even though `TCS = 20 < 35`,
because the single human-decision item is exactly the class that must get the executor-disjoint
audit. This is the case the rejected `TCS≥35 ∨ S6` predicate (which drops S5) would have
under-audited — the 3-term predicate catches it.

**Example C — clean low-everything → Mode 1.** A tasklist with: S1 = 3, S2 = 1, S3 = 0,
S4 = 1, S5 = 0, S6 = 0, `W = true`.

```text
TCS = 3·3 + 4·1 + 0 + 2·1 + 0 + 0 = 9 + 4 + 2 = 15
RESOLVE_AUTO(TCS=15, S5=0, S6=0, W=true):
  Stage 1: S6==0, S5==0, TCS=15 not≥35   → risk_mode = 1
  Stage 2: risk_mode==1                  → return 1
```

→ **auto resolves to 1** (`reflect_post_mode: auto-resolved-1`), inline `--depth standard`
audit-only — the proportionate cheap tier for genuinely low-complexity, low-risk work.

### 4.4 Boundary clarification — auto reads the *resolved* depth band (INV-004)

<!-- Source: invariant-probe INV-004, merged per Change #7 -->

The auto predicate's `TCS ≥ 35` term reads the **resolved** depth band — i.e., the band after
the overrides (O1/O2/O3) and after the existing bounded **±4 TCS tiebreaker** (`SKILL.md:2154`)
have been applied — **not** the raw arithmetic TCS. Equivalently:

```text
auto → 2  ⟺  resolved-depth == deep  ∨  S5 > 0  ∨  S6 == 1
```

Because the same resolved band feeds both the auto mode choice and the baked `--depth`
passthrough, the two **cannot diverge at the band edge**: there is no input where the
tiebreaker nudges TCS across 35 for the depth derivation but leaves the auto choice on the
other side. This preserves the single-producer property (FR-9, NFR-5) even in the count-divergence
boundary case the probe flagged.

### 4.5 Executor-disjointness trade-off (Mode 2 / manual vs Mode 1)

<!-- Source: V2 §8 executor-disjointness trade-off table, merged per Change #4 -->

This 4-row table makes explicit exactly what Mode 1 sacrifices relative to the executor-disjoint
modes (Mode 2 shell-out and the manual-HALT item), and when Mode 1 is acceptable.

| Property | Mode 2 / manual-HALT (disjoint) | Mode 1 (inline) |
|---|---|---|
| Executor-exclusion (anti-self-confirmation) | **Yes** — fresh session / subprocess never shared the executor's frame | **No** — runs in the executor's session, shares its representational bias |
| Reflect Tier-2 heterogeneous reviewers | Yes | Yes (still heterogeneous-model **iff** executor is top-level; §6.2 self-check) |
| `--remediate` (Tier-3 chain) | Yes (Mode 2) / Yes (manual) | **No** (audit-only) |
| Cost / latency | High (subprocess / fresh session, `deep`) | Low (inline, `standard`, no remediate) |

**Mode 1 is acceptable exactly when the resolver classifies the work low-complexity/low-risk**
(`S6 == 0 ∧ S5 == 0 ∧ TCS < 35`) — the cases where a same-frame audit is unlikely to be the
marginal catch and the cost of a full disjoint `deep --remediate` is disproportionate. For any
refactor/remediation-class, human-decision, or deep-band tasklist, `auto` never selects Mode 1.

---

## 5. Knob Reconciliation + old→new Map

> The three knobs collapse onto **one ordinal dial**. `--reflect` is the **sole input**;
> the two legacy fields become *derived* inputs consulted only when `--reflect` is absent.
> Precedence (highest first): explicit `--reflect` flag → `REFLECT_POST_MODE` BUILD_REQUEST
> field → §5 legacy-alias map → default `2`.

### 5.1 The dial

| Dial position | Meaning | Emitted item |
|---|---|---|
| `none` (`0`) | gate disabled | none (§6.1) |
| `1` | inline same-session, `--depth standard`, audit-only, NOT executor-disjoint | §6.2 |
| `2` (default) | wrapper shell-out, `--depth deep --remediate`, executor-disjoint | §6.3 |
| `auto` | builder resolves 1 or 2 per §4 | §6.2 or §6.3 (+ `auto-resolved-{1,2}`) |
| `2-degraded-halt` | (derived only, §8 / §4.2 Stage 2) wrapper absent under resolved Mode 2 | §6.4 manual-HALT |
| `halt` | (derived only) retained manual-HALT via legacy `POST_REFLECT_MODE: halt` | §6.4 manual-HALT |

### 5.2 old→new total map

The legacy surface had `POST_REFLECT_GATE ∈ {ENABLED, DISABLED}` (`SKILL.md:853`; absence ⇒
ENABLED for built tasks today) crossed with the sibling's proposed
`POST_REFLECT_MODE ∈ {wrapper, halt}` (default `halt`). Both legacy fields are now **deprecated
aliases** read only when no `--reflect`/`REFLECT_POST_MODE` value is present (§10). Every cell
maps to one dial position:

| Legacy `POST_REFLECT_GATE` | Legacy `POST_REFLECT_MODE` | New effective `m` | Emitted item | Notes |
|---|---|---|---|---|
| `DISABLED` | (any) | `none` | §6.1 (no item) | direct old→new; gate off, no item |
| (absent / `ENABLED`) | `halt` (or absent) | `halt` | §6.4 manual-HALT | **Back-compat anchor**: maps to the **retained manual-HALT position** (`reflect_post_mode: halt`), NOT to wrapper Mode 2, preserving `SKILL.md:1994-1999` byte-for-byte. See §5.3. |
| (absent / `ENABLED`) | `wrapper` | `2` | §6.3 shell-out | sibling's automated path == Mode 2 |
| explicit `--reflect <v>` present | (any legacy) | `<v>` | per `<v>` | **`--reflect` always wins**; legacy alias fields ignored with a one-line build-log note |

### 5.3 The retained manual-HALT position (`halt`)

To honor NFR-2 (byte-for-byte reversibility) and the sibling's `POST_REFLECT_MODE: halt`
default, the dial carries a **derived position `halt`** that is *not* selectable via the
numeric `--reflect 1|2` surface but **is** reachable via:

- legacy `POST_REFLECT_MODE: halt` (the sibling default), or
- a resolved Mode 2 (fixed `--reflect 2` OR `auto→2`) when the wrapper is **absent**
  (§8 degradation → `2-degraded-halt`).

`halt` emits the **current** `SKILL.md:1994-1999` manual fresh-session item verbatim
(`reflect_post_mode: halt`). This keeps three truths simultaneously: (a) the **numeric dial**
is the clean forward surface (`1`/`2`/`auto`); (b) the **manual-HALT behavior survives**
unchanged for callers who want it or whose wrapper is missing; (c) there is still exactly one
field (`reflect_post_mode`) telling a reader which of `{none, 1, 2, auto-resolved-1,
auto-resolved-2, halt, 2-degraded-halt}` is in force. **No second knob.**

> **REJECTED alternative (kept for the record).** V2 proposed `halt → Mode 1` (inline). This is
> **rejected** (C-001/X-002): it is semantically backwards — `halt` means "keep the manual
> *disjoint* gate," and Mode 1 is the one NON-disjoint mode. The base mapping `halt →
> byte-identical manual item` is retained.

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

#### 6.3.1 Mode 2 template as a unified diff vs current `:1994–1999` (implementer aid)

<!-- Source: V2 §6.1 unified-diff presentation, merged per Change #4 (additive implementer aid) -->

Mode 2 is the closest-to-today template, so the byte-level delta against the **current**
`SKILL.md:1994-1999` manual item is shown as a unified diff. Only the **Action**, **Output**,
and **Verification** mechanism changes (paste-ready manual command → live Bash shell-out); the
**Context**, the HALT, the `reflect_post` write-back, the depth (`deep`) and `--remediate` are
preserved.

```diff
- - [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**
+ - [ ] **N.{X-1} — Independent post-execution reflect gate (wrapper subprocess, HALT)**
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
+   - **Action**: Run, as a Bash shell-out (NEVER via Agent/Task — that re-introduces the Tier-2
+     nesting bug, `reference_subagent_cannot_nest_skill_fanout`):
+     `superclaude reflect run {TASK_FILE}` — the wrapper launches `/sc:reflect --mode post
+     --remediate --diff {BASE}..HEAD [--spec {SPEC_PATH}] --depth deep --executor-model
+     {EXECUTOR_CLASS}` as a top-level subprocess (escaping the nesting limit so Tier-2 fans out),
+     then writes a 4-state verdict `{pass, halted, degraded, blocked}` back into `reflect_post`.
+     The wrapper owns depth/`{BASE}` passthrough — do NOT recompute them here.
-   - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready `/sc:reflect --mode post` command
-     surfaced for a fresh session.
+   - **Output**: Frontmatter `reflect_post: {verdict, status, run_id, tier_reached, report,
+     contract, reason, deviations, head, reviewed_at}` written by the wrapper; wrapper exit 0 only on
+     `verdict: pass`.
-   - **Verification**: `reflect_post` is PENDING and the operator has the exact `/sc:reflect`
-     command. The item does NOT self-resolve.
+   - **Verification**: `superclaude reflect run` exited 0 AND `reflect_post.verdict == pass`. Any
+     other verdict (`halted`/`degraded`/`blocked`) means the gate did NOT pass.
    - **Completion gate**: `reflect_post.verdict == pass` (wrapper exit 0). On any non-pass verdict,
      HALT: append the wrapper's `report` + `reason` + deviation rollup to `### Open Questions` and do
      NOT proceed to `Update task status to Done` (HALT per `feedback_human_decision_items_must_halt`).
      Tier-3 remediation surfaced by the wrapper is recorded as an Open Question — NEVER auto-executed.
```

### 6.4 `halt` / `2-degraded-halt` — retained manual fresh-session item

This is the **current** `SKILL.md:1994-1999` item, emitted **verbatim** (byte-for-byte), with
the sole addition of `reflect_post_mode: halt` (or `2-degraded-halt`) in frontmatter. Reached
via legacy `POST_REFLECT_MODE: halt` or §8 wrapper-absent degradation under a resolved Mode 2
(fixed `--reflect 2` or `auto→2`). (Action: write `reflect_post: PENDING`, STOP, surface the
paste-ready `/sc:reflect --mode post --remediate …` fresh-session command; Completion-gate:
operator runs reflect in a fresh session and records the verdict — HALT.) For
`2-degraded-halt`, a single `<!-- wrapper-absent: degraded from Mode 2 -->` comment is appended
to the item Context; the gate text itself is untouched (byte-identical).

### 6.5 auto-resolved

`auto` emits **either §6.2 or §6.3 verbatim** depending on §4's resolution, and writes
`reflect_post_mode: auto-resolved-1` or `auto-resolved-2`. (When `auto→2` and the wrapper is
absent, §4.2 Stage 2 returns `2-degraded-halt` → §6.4 manual-HALT instead.) No third template
body exists — this is the extensibility property (NFR-4): the resolved mode reuses the
fixed-mode bodies. An optional one-line provenance prefix MAY be added to the item Context:
`Resolved by --reflect auto → Mode {N} (predicate: S6={s6}, S5={s5}, TCS={tcs}).` so an auditor
can see why the shape was chosen.

---

## 7. Depth/TCS Reconciliation

**Decision: mode fixes depth for fixed `1`/`2`; `auto` USES TCS to pick the mode and the mode
inherits its fixed depth — there is never a contradiction because the auto cut-points are
aligned to the TCS bands (and read the RESOLVED band, §4.4).**

| Mode | POST `--depth` | Source |
|---|---|---|
| `1` (fixed) | `standard` | fixed by the mode (inline tier never deep) |
| `2` (fixed) | `deep` | fixed by the mode (wrapper heavyweight tier) |
| `auto→1` | `standard` | inherited from resolved Mode 1 |
| `auto→2` | `deep` | inherited from resolved Mode 2 |
| `halt` / `2-degraded-halt` | `max(TCS-band, standard)` | the retained manual item keeps the **existing** TCS-derived depth (`SKILL.md:1996,2152`) |

**Fate of override O4 (`SKILL.md:2152`, "POST never `quick`").** O4 is **preserved and
strengthened**, never deleted:

- For fixed `1`/`2` and `auto→{1,2}`, depth is `standard` or `deep` by construction — O4's
  "never `quick`" floor is **automatically satisfied** (no mode yields `quick`). O4 becomes a
  redundant-but-true invariant for these paths; rf-qa still asserts it (a `quick` POST depth
  on any non-`halt` mode = MALFORMED).
- For the **retained `halt` / `2-degraded-halt` mode**, O4 applies exactly as today: the manual
  command floors at `standard` when the band yields `quick`.
- Overrides **O1** (S5>0 ⇒ floor standard) and **O2** (S6=1 ⇒ force deep) are now *also*
  expressed at the mode layer for `auto` (Stage 1 of §4 returns 2 for S5>0 or S6=1, and Mode 2
  is `deep`). So O1/O2 and the auto FER **agree by construction**; the depth machinery remains
  the single producer and the auto rule is a thin band-reading wrapper over it, never a
  competing model. **O1/O2/O3 are NOT removed** — they continue to govern the baked `{DEPTH}`
  passthrough for the `halt` mode and the wrapper-passthrough depth value.

**Boundary consistency (INV-004, §4.4).** Because the auto predicate reads the **resolved**
depth band — after O1/O2/O3 and the bounded ±4 tiebreaker (`SKILL.md:2154`) — the mode choice
and the baked depth cannot diverge at the band edge: `auto→2 ⟺ resolved-depth == deep ∨ S5>0 ∨
S6==1`.

**Why mode-fixes-depth rather than depth-fixes-mode (architect call):** depth is a *property
of the chosen tier*, not an independent dial. Letting depth drift independently of mode would
re-introduce two producers. By making `auto` read TCS to pick the mode and the mode then
dictate its own depth, there is exactly one arithmetic source (TCS) and one decision point
(A.9). Fixed `1`/`2` simply pin the tier (and thus the depth) explicitly.

---

## 8. Wrapper-Dependency Fallback

**Decision: a RESOLVED Mode 2 (fixed `--reflect 2` OR `auto→2`) with the wrapper absent →
degrade to the retained manual-HALT item (§6.4), record `reflect_post_mode: 2-degraded-halt`
(or `auto-resolved-2-degraded-halt`). Do NOT degrade to Mode 1; do NOT STOP the build. A
resolved Mode 1 needs no wrapper → Mode 1.**

<!-- Source: invariant-probe INV-002, merged per Change #2 — unified ladder: risk-mode resolved FIRST, then wrapper availability applied identically to fixed-2 and auto-2 -->

### 8.1 Detection (build time, at A.9)

The builder probes wrapper availability with a frozen check: the `reflect` subcommand is
registered (`superclaude reflect --help` exits 0 / `superclaude --help` lists `reflect`). The
probe result `W ∈ {true,false}` is computed once and reused by §4 (`auto`) and §8. The probe is
read-only and adds no state.

### 8.2 The fallback ladder (frozen, deterministic, unified)

The ladder applies the **resolved risk-mode** (not the raw request) against wrapper
availability. `auto` + `W=false` now **mirrors** fixed-`2` + `W=false`: both degrade to the
manual-HALT disjoint gate when the resolved risk-mode is 2, and both go to Mode 1 only when the
resolved risk-mode is 1. This is the INV-002 unification — there is no row where a high-risk
tasklist silently gets the weakest inline audit.

| Requested | Resolved risk-mode | `W` | Emitted item | `reflect_post_mode` |
|---|---|---|---|---|
| `none` | — | (any) | none (§6.1) | `none` |
| `1` (fixed) | — | (any) | §6.2 inline (no wrapper needed) | `1` |
| `2` (fixed) | 2 | true | §6.3 shell-out | `2` |
| `2` (fixed) | 2 | **false** | **§6.4 manual-HALT** | `2-degraded-halt` |
| `auto` | 1 | (any) | §6.2 inline (no wrapper needed) | `auto-resolved-1` |
| `auto` | 2 | true | §6.3 shell-out | `auto-resolved-2` |
| `auto` | 2 | **false** | **§6.4 manual-HALT** (mirrors fixed-2 degradation) | `auto-resolved-2-degraded-halt` |
| `halt` (legacy) | — | (any) | §6.4 manual-HALT | `halt` |

> **Changed from base V1.** V1's row `auto + W=false → §6.2 inline Mode 1 (auto-resolved-1)`
> is **replaced**: under the unified ladder, `auto + W=false` degrades to the manual-HALT
> **only when the resolved risk-mode is 2**; when the resolved risk-mode is 1 it returns Mode 1
> (which never needed the wrapper). The dangerous V1 case — a TCS=72/S6=1 tasklist with the
> wrapper missing silently getting inline Mode 1 — is closed.

### 8.3 Rationale for the asymmetry (architect defense)

- A **resolved Mode 2** request (whether fixed `2` or `auto→2`) is a determination that the
  tasklist needs the *executor-disjoint* property. Silently downgrading to **Mode 1** would
  **break the very property the risk profile demanded** (inline Mode 1 is NOT
  executor-disjoint — FR-3) without surfacing it. The honest fallback is the **manual HALT**,
  which *preserves* executor-disjointness (the operator runs reflect in a fresh session) at the
  cost of automation — fail-closed, never a silent weakening (NFR-8). A build-time STOP is
  rejected because it would block task delivery on a missing *optional automation*; the manual
  gate is the long-standing, correct default.
- A **resolved Mode 1** needs no wrapper, so wrapper-absence is irrelevant — it is emitted
  unchanged.

The degradation is always recorded in frontmatter (`*-degraded-halt`) so rf-qa and the operator
can see the wrapper was unavailable.

---

## 9. Validation + rf-qa Changes

<!-- Source: V3 §9 (V1–V16 assertion table) + per-mode active-assertion map + §13 ATs, merged per Change #3 (replaces V1's prose §9.1–§9.4) -->

> All changes assert **emitted item == `reflect_post_mode`** mechanically. The single
> frontmatter field is the **oracle** (V1 framing, retained); rf-qa never re-derives the mode.
> V1's prose §9.1–§9.4 is **replaced** by V3's exhaustive enumerated assertion matrix below,
> reconciled to the base field names (`reflect_post_mode` frontmatter / `REFLECT_POST_MODE`
> BUILD_REQUEST) and the base value set `{none, 1, 2, auto-resolved-1, auto-resolved-2, halt,
> 2-degraded-halt}`.

### 9.1 Exhaustive assertion table (V1–V16)

Each assertion has a pass/fail test. Fail = MALFORMED (retry max-2 per Critical Rule #12 / A.9
MALFORMED mediation, then halt). These replace the legacy single-string checklist item at
`SKILL.md:2051` and Critical Rule 19 at `SKILL.md:2108`.

| # | Assertion | Pass condition | Fail condition |
|---|-----------|---------------|----------------|
| V1 | `REFLECT_POST_MODE` field present in BUILD_REQUEST | Field exists with value `1`, `2`, `auto`, or `none` | Field absent or value not in valid set |
| V2 | `reflect_post_mode` frontmatter field present | Field ∈ `{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt}` | Field absent or not in the value set |
| V3 | POST item count matches mode | Mode `none` → 0 items; modes `1`/`2`/`auto-resolved-{1,2}`/`halt`/`2-degraded-halt` → exactly 1 item | Mismatch (item present when `none`, or absent when mode ≠ `none`) |
| V4 | Item position is penultimate | Item at position N.{X-1}, immediately before Update-status-to-Done at N.X | Item is last, not in final phase, or >1 item before Done |
| V5 | Mode 1 Action contains inline skill invocation | Action contains `/sc:reflect --mode post --depth standard` as a top-level skill invocation | Action missing inline invocation or wrong depth |
| V6 | Mode 1 Action does NOT contain shell-out / wrapper markers | Action does NOT contain `superclaude reflect run`, `Bash`, `shell-out`, `Run:` | Shell-out / wrapper markers found in Mode 1 |
| V7 | Mode 2 Action contains Bash shell-out to the wrapper | Action contains `superclaude reflect run {TASK_FILE}` as a Bash shell-out | Missing Bash shell-out or missing wrapper command |
| V8 | Mode 2 Action does NOT contain inline skill invocation / Agent/Task | Action does NOT contain inline `/sc:reflect`, nor any `Agent`/`Task`/`subagent` spawn | Inline invocation or Agent/Task spawn found in Mode 2 |
| V9 | Mode 1 Action does NOT contain `--remediate` | `--remediate` absent from the Mode-1 reflect invocation | `--remediate` present in Mode 1 |
| V10 | Mode 2 remediation is delegated to the wrapper | Wrapper command present; remediation (`--remediate`, `--no-promote` default) is the wrapper's responsibility (sibling FR-8/FR-9) | Mode-2 item re-authors remediation/tier logic inline |
| V11 | Non-`none` items write `reflect_post` back / sentinel discipline | Mode 1/2 capture `reflect_post: {verdict,…}`; `halt`/`2-degraded-halt` write `reflect_post: PENDING` | Write-back / PENDING sentinel missing for the mode |
| V12 | Both active modes contain explicit HALT/STOP on non-pass | Item Completion-gate contains HALT/STOP language with prohibition on self-resolve | No HALT instruction, or self-resolve permitted |
| V13 | `{SPEC_PATH}` threading matches resolved spec | When `spec_path` set, Mode-1 item contains `--spec {SPEC_PATH}`; when unset, no `--spec` | Mismatch between resolved spec and item command |
| V14 | `{BASE}` resolution instruction present | Item Action contains `{BASE}` resolution guidance (frontmatter `start_commit` or `git merge-base`) | Missing BASE resolution |
| V15 | Degraded/manual item is byte-identical to legacy HALT | `halt` / `2-degraded-halt` item matches `SKILL.md:1994-1999` exactly (after placeholder substitution) | Item differs from the legacy template |
| V16 | Degraded frontmatter records degradation / manual state | `reflect_post_mode` ∈ `{halt, 2-degraded-halt, auto-resolved-2-degraded-halt}` and (for degraded) carries the wrapper-absent marker | No degradation/manual marker when the mode is a manual/degraded state |

### 9.2 Per-mode active-assertion map

rf-qa's `task-integrity` mode (currently item 19 at `SKILL.md:2108`) runs the subset of
V1–V16 active for the resolved `reflect_post_mode`. The set is parameterized by the field:

- **`none`** → V1, V2, V3 active.
- **`1` / `auto-resolved-1`** → V1, V2, V3, V4, V5, V6, V9, V11, V12, V13, V14 active.
- **`2` / `auto-resolved-2`** → V1, V2, V3, V4, V7, V8, V10, V11, V12, V13, V14 active.
- **`halt` / `2-degraded-halt` / `auto-resolved-2-degraded-halt`** → V1, V2, V15, V16 active
  (the manual/degraded rows; plus V3/V4 for presence + penultimate position).

### 9.3 rf-qa task-integrity integration (the FR-9 invariant)

The per-gate `task-integrity` counter at `SKILL.md:2094` gains a single **MODE-MATCH**
assertion that is the rf-qa expression of FR-9's single-producer guarantee — the frontmatter
field and the item body cannot disagree:

```text
MODE-MATCH (MALFORMED on fail): read frontmatter `reflect_post_mode`. Assert the penultimate
final-phase item's Action shape matches it, per the §9.1 table:
  reflect_post_mode == 1 / auto-resolved-1   ⇒ V5 ∧ V6 ∧ V9 (inline /sc:reflect --depth standard,
                                                no --remediate, no `superclaude reflect run`).
  reflect_post_mode == 2 / auto-resolved-2   ⇒ V7 ∧ V8 ∧ V10 (Bash `superclaude reflect run
                                                {TASK_FILE}`, no inline, no Agent/Task).
  reflect_post_mode == none                  ⇒ V3 (no reflect item present; `reflect_post:` absent).
  reflect_post_mode ∈ {halt, 2-degraded-halt, auto-resolved-2-degraded-halt}
                                             ⇒ V15 ∧ V16 (byte-identical manual paste-ready
                                                `/sc:reflect --mode post --remediate …` item;
                                                degradation/manual marker recorded).
Mismatch between `reflect_post_mode` and the emitted Action shape = MALFORMED.
```

The existing penultimate / `reflect_post` / HALT / `/sc:reflect`-vs-`/sc:task` checks are
**reused**; only the mode-shape assertion set is added.

### 9.4 Mismatch acceptance tests

<!-- Source: V3 §9 acceptance tests AT-VALIDATION-1 / AT-MISMATCH-1, merged per Change #3 -->

- **AT-VALIDATION-1.** A tasklist with `reflect_post_mode: 1` whose POST item contains
  `superclaude reflect run` fails **V6**. A tasklist with `reflect_post_mode: 2` whose POST item
  contains an inline `/sc:reflect` fails **V8**. A tasklist with `reflect_post_mode: 1` whose
  POST item contains `--remediate` fails **V9**.
- **AT-MISMATCH-1.** Intentionally swap the Mode-1 and Mode-2 templates in a test tasklist.
  rf-qa `task-integrity` MUST catch the mismatch and return MALFORMED naming the specific
  failing assertion number (V6 or V8).

### 9.5 Wire-string / sentinel preservation

The `reflect_post: ""` PENDING sentinel (`SKILL.md:1942`) is retained **only** for the `halt` /
`2-degraded-halt` modes (which still defer to a fresh session — V11/V15/V16 cover these). For
modes 1 and 2 the `reflect_post:` block is written by the inline run / wrapper respectively; for
mode `none` the key is absent. rf-qa (V11) asserts the sentinel's presence/absence matches the
mode.

---

## 10. Flag Plumbing + Frontmatter + BUILD_REQUEST

<!-- Source: field naming reconciled to REFLECT_POST_MODE per Change #6 (C-004); precedence per INV-005 -->

### 10.1 Parse site + precedence

`--reflect` is parsed at the BUILD_REQUEST / flag-resolution stage and consumed at **A.9**
(the POST gate logic site, co-located with the legacy gate field at `SKILL.md:853`). Resolution
order (highest wins, first match):

1. explicit `--reflect <value>` flag on the build invocation (`value ∈ none|0|1|2|auto`);
2. `REFLECT_POST_MODE:` field in a BUILD_REQUEST file (new field, value `none|0|1|2|auto`);
3. **legacy §5 alias map**: `POST_REFLECT_GATE` × `POST_REFLECT_MODE` → `m` (consulted only if
   1–2 absent; both legacy fields are **deprecated aliases**, not surviving inputs);
4. **default `2`**.

When a higher-precedence source is present, the lower legacy alias fields are ignored and a
one-line note is written to the build log (`--reflect <v> wins; legacy POST_REFLECT_* ignored`).
Mode resolution (including `auto` → §4 and wrapper-probe → §8) happens **once** at A.9 (FR-9).

> **Field naming (Change #6 / C-004).** The BUILD_REQUEST field is **`REFLECT_POST_MODE`**,
> deliberately mirroring the frontmatter field `reflect_post_mode` for build/frontmatter
> symmetry — this strengthens the single-oracle story (one name, two surfaces). The CLI flag is
> **`--reflect`**. The legacy `POST_REFLECT_GATE` and the sibling-proposed `POST_REFLECT_MODE`
> are **deprecated aliases** read only at precedence step 3. **`POST_REFLECT_MODE` is retired as
> a live independent field** — it survives only as a read-time alias in the §5 map — so there is
> **no live collision** between the sibling's `POST_REFLECT_MODE` and the new
> `REFLECT_POST_MODE`. (INV-005: setting the new field AND a legacy alias resolves
> deterministically — new field wins, legacy ignored with a build-log note.)

### 10.2 BUILD_REQUEST schema change (at `SKILL.md:853`)

Retire `POST_REFLECT_GATE: ENABLED` + sub-fields as the *primary* surface; introduce:

```text
REFLECT_POST_MODE: 2          # one of: none | 0 | 1 | 2 | auto   (default 2 when absent)
  SPEC_PATH: <spec_path or NONE>     # threaded to Mode 1 inline / Mode 2 wrapper (§12)
  # DEPTH is no longer an author-settable POST sub-field: it is mode-derived
  # (1→standard, 2→deep, halt→max(TCS,standard)) — single producer, §7.
  TASK_FILE: ${TASK_FILE}
  # Accepts deprecated aliases POST_REFLECT_MODE: wrapper(≡2)|halt(→halt position)
  #   and POST_REFLECT_GATE: ENABLED|DISABLED(≡none) — §5 map, precedence step 3.
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
oracle for all of §9. It is written once, at tasklist generation, by the A.9 producer. Its
name deliberately mirrors the `REFLECT_POST_MODE` BUILD_REQUEST field (§10.1).

### 10.4 Advisory warning emission point (Change #5 / INV-003, FR-13)

When the resolved request is a **fixed** `--reflect 1` (not `auto`) AND `S6 == 1 ∨ S5 > 0`, the
A.9 producer writes a **non-blocking** advisory WARNING to the build log: *"auto would have
selected Mode 2; Mode 1 is not executor-disjoint — confirm intent"*. This is emitted alongside
the §6.2 Mode-1 item (which is still produced, honoring operator authority); it does not change
the emitted item or `reflect_post_mode: 1`. The warning is a footgun guard, not a gate.

---

## 11. Scope Boundaries

**In scope (this spec):**
- `task-builder/SKILL.md`: `--reflect` flag parse + precedence (A.9 / `:853`); the per-mode
  POST item templates (replace `:1994-1999`); the `auto` FER (§4); the `POST_REFLECT_GATE` +
  `POST_REFLECT_MODE` reconciliation / old→new map (§5); depth/TCS reconciliation incl. O4
  fate (§7, `:2114-2155`); wrapper-availability probe + unified fallback ladder (§8); validation
  rewrites (`:2051`, `:2108`) replaced by the V1–V16 matrix + per-mode active-assertion map +
  rf-qa MODE-MATCH task-integrity assertion (§9); BUILD_REQUEST `REFLECT_POST_MODE:` field
  (`:853`) + `reflect_post_mode:` frontmatter field (`:1942`); `--spec` threading preservation
  (`:41`); the fixed-1 advisory warning (§10.4 / FR-13).
- `src/superclaude/agents/rf-qa.md` (or wherever the rf-qa task-integrity assertions live):
  V1–V16 assertion integration + MODE-MATCH.
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
  `POST_REFLECT_MODE: wrapper` must deterministically emit Mode 1 — the rf-qa MODE-MATCH
  invariant (§9.3) catches any disagreement.
- **R2 — `auto` drift from depth machinery.** Mitigated by reusing the *same* TCS + S5/S6
  already computed for depth (§4, §7) AND reading the **resolved** band (§4.4, INV-004); the
  worked examples (§4.3) show auto-mode and baked depth agree by construction. Falsifier: an
  `auto→2` item with `--depth standard` would prove drift; §7's table forbids it and V5/V9 flag
  `--depth quick`/mismatch as MALFORMED.
- **R3 — Mode 1 silent Tier-2 loss under a subagent executor.** This is the genuinely
  dangerous case (`reference_subagent_cannot_nest_skill_fanout`). Mitigated by FR-11's
  **runtime** top-level precondition + nested-executor HALT branch (§6.2 Verification) and the
  §9 assertion that the precondition text is present; a build-time `agent_tool_depth` signal is
  only best-effort defense-in-depth behind the runtime self-check (the frame is generally
  unknown at build time). Residual risk: detection relies on the executor honoring the
  precondition; documented as a known limit and the reason Mode 1 is reserved for
  low-TCS/low-risk tasklists.
- **R4 — Wrapper-absent surprise.** Mitigated by the build-time probe (§8.1) + the **unified**
  frozen fallback ladder (§8.2, INV-002) + the recorded `*-degraded-halt` frontmatter, so the
  degradation is never silent and never weakens executor-disjointness for any resolved Mode 2
  (fixed or auto).
- **R5 — Back-compat regression.** Mitigated by NFR-2: the `halt` position reproduces
  `:1994-1999` byte-for-byte (V15), the §5 map is total over the legacy cells, and default `2`
  matches the sibling's automated intent. Falsifier: a diff of a `POST_REFLECT_MODE: halt`
  tasklist against today's output must be empty.
- **R6 — Under-rigorous fixed-1 footgun.** A fixed `--reflect 1` on a regression-class (S6=1)
  or human-decision (S5>0) tasklist silently gets a non-disjoint audit. Mitigated by FR-13's
  advisory build WARNING (§10.4, INV-003) — operator authority is honored but the risk is
  surfaced, non-blocking.
- **R7 — Extension pressure (a future `--reflect 3`).** Designed-for via NFR-4: the ordinal
  domain widens monotonically; a new tier is one row in §4/§5/§6/§9. Risk is that a future tier
  breaks the "mode fixes depth" invariant — mitigated by requiring any new tier to pin its own
  depth at definition time (the §7 contract).

---

## 13. Acceptance Test Matrix

<!-- Source: V3 §13 FR→acceptance-test matrix, merged per Change #3 (reconciled to base field names + mode set) -->

| FR | Test ID | Test description | Pass criteria |
|----|---------|-----------------|---------------|
| FR-1 | AT-FR1 | Parse each of `none|0|1|2|auto`; parse `--reflect foo` | Each valid token → documented `m`; `foo` → MALFORMED within one retry |
| FR-2 | AT-FR2 | `--reflect none` suppresses item | No POST item; `reflect_post:` key absent; `reflect_post_mode: none` |
| FR-3 | AT-FR3 | Mode 1 inline emission | Action has `/sc:reflect --mode post --depth standard`, no `--remediate`, no `superclaude reflect run`, no Agent/Task; penultimate |
| FR-4 | AT-FR4 | Mode 2 wrapper emission (default) | Action has Bash `superclaude reflect run {TASK_FILE}`, not Agent/Task; penultimate |
| FR-5 | AT-FR5 | `auto` determinism (Examples A/B/C) | Two implementers agree on all three worked examples; `reflect_post_mode: auto-resolved-{1,2}` stamped |
| FR-6 | AT-FR6 | old→new total map round-trip | Each legacy cell → one `m` → one emitted item; `--reflect` wins over legacy |
| FR-7 | AT-FR7 | HALT + write-back | Each non-`none` item's Completion-gate has HALT + `reflect_post` write-back; no self-resolve |
| FR-8 | AT-FR8 | `--remediate` scope | Mode 1 has no `--remediate`; Mode 2 completion-gate routes Tier-3 → Open Questions, no auto-exec |
| FR-9 | AT-FR9 | Single-producer consistency | `reflect_post_mode` and emitted item shape mutually consistent (MODE-MATCH) |
| FR-10 | AT-FR10 | Wrapper-absent fallback | `--reflect 2` + `W=false` → §6.4 manual-HALT + `reflect_post_mode: 2-degraded-halt` |
| FR-11 | AT-FR11 | Mode 1 nesting guard | Mode-1 Verification has top-level precondition + nested-executor HALT (`mode1-nested-executor`) |
| FR-12 | AT-FR12 | `--spec` threading | `--spec {SPEC_PATH}` present iff `spec_path` resolves |
| FR-13 | AT-FR13 | Fixed-1 advisory | `--reflect 1` + (`S6=1 ∨ S5>0`) → build-log WARNING; item still §6.2 Mode-1, `reflect_post_mode: 1` |
| auto | AT-AUTO-1 | 3-term predicate determinism | Examples A/B/C resolve identically across implementers; INV-002 ladder honored for `W=false` |
| knob | AT-KNOB-1 | old→new equivalence | `POST_REFLECT_GATE: DISABLED` ≡ `--reflect none` structurally (no item, no `reflect_post:` key) |
| depth | AT-DEPTH-1 | O4 preservation | Mode 1 always `standard`; Mode 2 respects TCS floored at `standard`; no mode yields `quick` |
| wrapper | AT-WRAPPER-1 | Wrapper detection | Probe exits 0 when `reflect` subcommand registered; non-zero when absent |
| fallback | AT-FALLBACK-1 | Unified ladder (INV-002) | resolved Mode 2 + `W=false` → manual-HALT (`*-degraded-halt`); resolved Mode 1 + `W=false` → Mode 1 |
| validation | AT-VALIDATION-1 | Mode/item mismatch | `mode:1` w/ wrapper fails V6; `mode:2` w/ inline fails V8; `mode:1` w/ `--remediate` fails V9 |
| mismatch | AT-MISMATCH-1 | MALFORMED on swap | Swapped Mode-1/Mode-2 templates fail with the specific V# (V6 or V8) |
| plumbing | AT-PLUMBING-1 | Precedence + defaults | `--reflect` flag > `REFLECT_POST_MODE` field > legacy alias map > default 2 |

---

## Resolved Open Questions

The 10 open questions from the seed brief (`seed-brief.md`), each mapped to its resolution in
this merged spec:

| # | Open Question | Resolution |
|---|---------------|------------|
| 1 | **`auto` selection FER** — deterministic 1-vs-2 rule | §4.2 **3-term predicate** `S6==1 ∨ S5>0 ∨ TCS≥35 → Mode 2; else Mode 1`, S5/S6 evaluated before the band, reading the **resolved** depth band (§4.4). V1's `S2≥3` gate dropped (C-002) — S2's ×4 TCS weight already captures breadth. Two implementers compute the same choice (Examples A/B/C). |
| 2 | **Reconciliation with `POST_REFLECT_GATE`** — subsume? `none`? retained HALT? fold in `POST_REFLECT_MODE`? | §5 total old→new map. `--reflect` **subsumes** both legacy fields as deprecated aliases. `--reflect none|0` = disabled (no item). `halt` retained as a derived manual-disjoint position (`POST_REFLECT_MODE: halt → halt`, NOT Mode 1 — C-001). `POST_REFLECT_MODE: wrapper ≡ Mode 2`. |
| 3 | **Depth vs TCS** — modes fix depth; auto uses TCS; fate of O4? | §7: **mode fixes depth** (1→standard, 2→deep); `auto` **uses TCS** to pick the mode and inherits its depth. O4 (POST never `quick`) **preserved and strengthened** — structurally unreachable for modes 1/2; applies as today for `halt`. O1/O2/O3 retained. |
| 4 | **Executor-disjointness trade-off (Mode 1)** — what it sacrifices, when acceptable | §4.5 4-row trade-off table (V2): Mode 1 loses executor-exclusion + `--remediate`; keeps heterogeneous Tier-2 reviewers iff top-level. Acceptable exactly when `S6==0 ∧ S5==0 ∧ TCS<35` (low-complexity/low-risk). |
| 5 | **Mode 2 wrapper dependency + fallback** — absent → HALT? Mode 1? STOP? | §8 unified ladder (INV-002): resolved Mode 2 + wrapper absent → **manual-HALT** (`*-degraded-halt`), preserving executor-disjointness; never Mode 1, never build STOP. Build-time probe (§8.1). |
| 6 | **`--remediate` scope** — Mode 1 audit-only, Mode 2 remediate; Tier-3 handling | FR-8: Mode 1 = audit-only (no `--remediate`); Mode 2 = `--remediate` via wrapper. Tier-3 corrective task → routed to `### Open Questions` + HALT, **never auto-executed** (wrapper `--no-promote` default). |
| 7 | **Per-mode emitted-item template** — exact text for 1, 2, auto-resolved | §6 literal templates: §6.2 Mode 1 (inline), §6.3 Mode 2 (shell-out) + §6.3.1 unified diff vs `:1994-1999`, §6.4 manual/halt, §6.5 auto-resolved (reuses 1/2 bodies). Each HALTs + writes `reflect_post`. |
| 8 | **Mode 1 same-session mechanics + nesting boundary** | FR-11 + §6.2: inline top-level skill invocation captures the verdict into `reflect_post`; **runtime self-check** is the PRIMARY guard — if the executor is a subagent → HALT with `reflect_post: blocked, reason: mode1-nested-executor`. Build-time `agent_tool_depth` only best-effort defense-in-depth. |
| 9 | **Validation (rf-qa) updates** — item matches mode; mismatch = MALFORMED | §9: V3's exhaustive **V1–V16** assertion matrix + per-mode active-assertion map + rf-qa **MODE-MATCH** task-integrity assertion. Replaces `:2051` + Critical Rule 19 (`:2108`). Any mismatch = MALFORMED (retry max-2). ATs: AT-VALIDATION-1, AT-MISMATCH-1. |
| 10 | **Flag plumbing + frontmatter** — parse site, precedence, default, field | §10: parsed at flag-resolution, consumed at A.9. Precedence: explicit `--reflect` > `REFLECT_POST_MODE` field > legacy alias map > default `2`. Frontmatter field `reflect_post_mode` (mirrors BUILD_REQUEST `REFLECT_POST_MODE`); single oracle. |

---

<!-- End merged spec. Base V1 (opus:architect) backbone + 7 applied changes from refactor-plan.md.
     Convergence 0.82 (PASS). Consistency re-scan confirmed: (1) `none` ≠ manual item;
     (2) auto predicate is the 3-term form everywhere; (3) fallback ladder unified (risk-mode
     first, then wrapper availability); (4) field name `REFLECT_POST_MODE`/`reflect_post_mode`
     consistent throughout. -->
