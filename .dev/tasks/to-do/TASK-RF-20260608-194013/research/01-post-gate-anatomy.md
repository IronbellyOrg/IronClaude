# Research: POST Gate Anatomy

- **Topic type:** File Inventory — current POST Reflect Gate anatomy in task-builder/SKILL.md
- **Scope:** `src/superclaude/skills/task-builder/SKILL.md` — every target surface the `--reflect auto|1|2` POST-gate refactor touches.
- **Status:** In Progress
- **Date:** 2026-06-08

This file captures EXACT VERBATIM current text + precise line numbers per surface, so the builder can author surgical edits and the byte-for-byte back-compat anchor (NFR-2/V15) is exact.

> Note on spec-cited vs actual lines: the spec frontmatter cites line numbers (e.g. `:853`, `:1942`, `:1994-1999`, `:2051`, `:2108`, `:2114-2155`). Where the live file drifted, BOTH are recorded.

> **GOOD NEWS for the builder:** the live file's line numbers track the spec's citations almost exactly. Every spec-cited surface was found at (or within 1-2 lines of) its cited line. The only material divergence is the spec's `:2094` cite (see Surface 7), which maps to TWO live surfaces.

---

## Surface index (quick map for surgical-edit authoring)

| # | Surface | Spec cite | Live line(s) | Drift |
|---|---|---|---|---|
| 1a | `--spec` Input doc bullet | `:41` | `:41` | none |
| 1b | `SPEC_PATH` A.2 BUILD_REQUEST-component doc | `:201` | `:201` | none |
| 2 | BUILD_REQUEST `POST_REFLECT_GATE` block (A.9 schema) | `:853` / `~:848-856` | `:853-856` | none |
| 2b | EXECUTION_CONTEXT/MALFORMED mediation text above block | `~:848` | `:831-851` | none |
| 3 | A.10.7 PRE cross-ref to `POST_REFLECT_GATE` | `~:1423` | `:1423` | none |
| 4a | Frontmatter `spec_path:` | `:1933` | `:1933` | none |
| 4b | Frontmatter `reflect_post: ""` PENDING sentinel | `:1942` | `:1942` | none |
| 5 | **CURRENT POST ITEM (V15 byte-exact anchor)** | `:1994-1999` | `:1994-1999` | none |
| 5b | Following `Update task status to Done` item | — | `:2001-2006` | — |
| 6 | Validation-checklist POST-item assertion | `:2051` | `:2051` | none |
| 7a | Per-gate `task-integrity=2` cap (hard-cap check) | `~:2094` | `:1116` | spec cite is approximate |
| 7b | Per-gate caps in Critical Rule 12 | `~:2094` | `:2094` | exact (but it's Rule 12, not the cap table) |
| 8 | Critical Rule 19 (POST reflect gate in generated files) | `:2108` | `:2108` | none |
| 9 | `## Reflect Depth (Deterministic TCS)` heading + range (researcher-02 owns internals) | `:2114-2155` | `:2114-2156` | O1-O4 at `:2149-2152` |

---

## Surface 1a — `--spec` Input doc bullet (live `:41`, spec `:41`)

Verbatim (line 41, single logical line):

```text
5. **--spec <path> — driving spec/PRD/TDD** (optional) — The path to the driving specification, PRD, or TDD that the task implements. When supplied it is threaded into the PRE reflect gate's coverage audit (the `--mode pre --spec <path>` call at A.10.7) and baked into the templated POST reflect item's command, so the post-execution deviation audit can check the executed work against the original spec. Resolved in priority order: explicit `--spec <path>` → an `@file` reference in the GOAL → a `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST file → none. Written to the generated tasklist frontmatter as `spec_path:`. Examples: `--spec .dev/proposals/reflect-in-task-builder.md`, `--spec docs/specs/auth-system-prd.md`.
```

**How the spec changes it (FR-12):** `--spec` threading is *preserved* across all modes. Mode 1 inline command gets `[--spec {SPEC_PATH}]`; Mode 2 wrapper reads it from frontmatter `spec_path`; Mode `none` omits it. No edit strictly required here for `--reflect`, but the builder may add a sentence introducing the `--reflect auto|1|2` flag adjacent to this `--spec` doc (this is the natural home for the new flag's Input doc per §1/FR-1). Low-risk additive surface.

---

## Surface 1b — `SPEC_PATH` A.2 BUILD_REQUEST-component doc (live `:201`, spec `:201`)

Verbatim (line 201, single logical line):

```text
- **SPEC_PATH**: The driving spec/PRD/TDD path, resolved in priority order (explicit `--spec <path>` → an `@file` reference in GOAL → a `SPEC:`/`PRD:`/`TDD:` field in BUILD_REQUEST → none); written to the generated tasklist frontmatter as `spec_path:`, threaded into the A.10.7 PRE call's `--spec` and the POST item's `{SPEC_PATH}` placeholder
```

Context: this is the 5th bullet under `### A.2: Parse & Triage` (`## Stage A` pipeline), enumerating BUILD_REQUEST components GOAL/WHY/OUTPUTS/CONTEXT/SPEC_PATH (lines 197-201).

**How the spec changes it (FR-9, FR-1):** A.2 is the natural site to also resolve the **`--reflect` value** into the mode-resolution input. Per FR-9 the resolved `m` is computed "at A.9", but the raw `--reflect` token parse (`{none,0,1,2,auto}` → MALFORMED on unknown) and precedence vs legacy fields (researcher-04 owns §10) plausibly originate here at A.2 alongside SPEC_PATH. Builder will likely add a `REFLECT_POST_MODE` (or similar) component bullet mirroring this SPEC_PATH bullet.

---

## Surface 2 — BUILD_REQUEST `POST_REFLECT_GATE` block (live `:853-856`, spec `:853` / `~:848-856`)

This is the A.9 producer schema. The block sits inside the `### A.9: Spawn Builder` BUILD_REQUEST `text` fence (fence opens at `:791`, `## A.9` header at `:785`).

Verbatim (lines 853-856), **exact indentation preserved** (4-space base indent inside the fence, sub-fields at 6 spaces):

```text
    POST_REFLECT_GATE: ENABLED
      SPEC_PATH: <spec_path or NONE>
      DEPTH: <max(tcs-derived depth, standard)>   # POST floor per O4 — never quick
      TASK_FILE: ${TASK_FILE}
```

The block is immediately preceded by a blank line (`:852`) and the `EXECUTION_CONTEXT_REQUIREMENTS` field (`:831-851`), and followed by a blank line (`:857`) then `DOCUMENTATION STALENESS WARNINGS:` (`:858`).

**How the spec changes it (FR-6, §5, §10):** `POST_REFLECT_GATE: ENABLED` is **retired as an independent input** and replaced by `REFLECT_POST_MODE: <none|1|2|auto>` (spec target_surface comment at spec line 26: "REFLECT_POST_MODE BUILD_REQUEST field (was POST_REFLECT_GATE)"). The `SPEC_PATH`/`DEPTH`/`TASK_FILE` sub-fields are retained as passthrough. This is researcher-04's precedence/map territory; this inventory pins that the literal string `POST_REFLECT_GATE: ENABLED` lives at **`:853`** and is the rename anchor.

### Surface 2b — EXECUTION_CONTEXT / MALFORMED mediation text above the block (live `:831-851`)

Verbatim region (lines 831-851) — the `EXECUTION_CONTEXT_REQUIREMENTS` field, whose tail defines the MALFORMED-retry mediation referenced by Critical Rule 12 and the A.9 mediation flow:

```text
    EXECUTION_CONTEXT_REQUIREMENTS: [OPTIONAL signal (API-001-M2) controlling
      the `## Execution Context` block emission in the generated MDTM. Governs
      DM-001-frozen (T01.13 / D-0011 § 1) emitters defined in the EXECUTION
      CONTEXT BLOCK section below. Values:
      - AUTO (default) — builder emits the block when BUILD_REQUEST exposes
        rollup signal (≥3 distinct named source areas inferable from research
        findings). Fully-populated form renders all 3 labeled bullets
        (References, Source areas, Key constraints). Minimal form (GOAL-only
        BUILD_REQUEST) degenerates to References-only with Source areas and
        Key constraints bullets ABSENT (not blank-but-present).
      - REQUIRED — builder MUST emit the block. The degraded References-only
        form is permitted when only GOAL is populated; suppressing the block
        entirely is a MALFORMED output.
      - SUPPRESS — builder MUST NOT emit the block. Per-item Context fields
        remain unchanged regardless. Used for thin / throwaway task files.
      Omission of this field implies AUTO. Strictly additive — when absent
      or AUTO, the M1-frozen 15-field BUILD_REQUEST behavior is preserved
      byte-identical. Failure mode: MALFORMED retry max-2 (Critical Rule #12
      and the MALFORMED flow at SKILL.md A.9 mediation) applies when the
      builder violates this signal — e.g., emitting the block under SUPPRESS,
      or omitting the block under REQUIRED.]
```

**Note for builder:** line 847 says "the M1-frozen **15-field** BUILD_REQUEST behavior is preserved byte-identical." Renaming `POST_REFLECT_GATE` → `REFLECT_POST_MODE` and/or adding a mode value changes the BUILD_REQUEST field set. If `POST_REFLECT_GATE` counts among the "15 fields", this "15-field" claim and any "strictly additive / byte-identical" framing may need reconciliation (the refactor RETIRES one field and adds one → net-neutral count, per spec §5.4 "schema shrinks by one field net (retire two, add one)" — but that count math is about the legacy×sibling pair, not this M1-frozen 15). Flag for researcher-04 (plumbing) — the "15-field" invariant text is a back-compat tripwire.

The MALFORMED flow itself is also referenced at `:849` ("MALFORMED flow at SKILL.md A.9 mediation"). The full MALFORMED mediation loop is at `:1061-1071` (Stage A.10 retry handling) — NOT immediately above the gate block. The "mediation text immediately above it" the topic brief refers to is the EXECUTION_CONTEXT_REQUIREMENTS field's MALFORMED-failure-mode tail (`:848-851`), quoted above.

---

## Surface 3 — A.10.7 PRE cross-ref to `POST_REFLECT_GATE` (live `:1423`, spec `~:1423`)

Verbatim (line 1423):

```text
Do **NOT** pass `--executor-model` at PRE — no executor has run in `--mode pre`, so excluding an executor class is a category error (it is a POST-only concern, see A.9 `POST_REFLECT_GATE`).
```

**How the spec changes it:** This is a **PRE-behavior cross-reference only** — spec §1 + out_of_scope explicitly exclude changing the PRE gate (A.10.7). The literal token `` `POST_REFLECT_GATE` `` appears here as a backward pointer to A.9. If A.9's field is renamed to `REFLECT_POST_MODE`, this cross-ref string SHOULD be updated for consistency (cosmetic, non-behavioral) but the PRE logic is untouched. NOTE-ONLY per brief — do not change PRE behavior.

---

## Surface 4a — Frontmatter `spec_path:` (live `:1933`, spec `:1933`)

Verbatim (line 1933), inside the `## Output Structure` frontmatter template (frontmatter region `:1915`-ish opening `---` through closing `---` at `:1949`):

```text
spec_path: "[driving spec/PRD/TDD path resolved at A.2, or empty if none]"
```

Surrounding frontmatter context (lines 1932-1942):

```text
task_type: static
spec_path: "[driving spec/PRD/TDD path resolved at A.2, or empty if none]"
reflect_pre:
  verdict: pass | fail | skipped
  coverage_pct: <float | null>
  depth: quick | standard | deep
  tcs: <int>
  run_id: "[reflect run id]"
  report: "[TASK_DIR]reflect/pre/report.md"
  reviewed_at: "YYYY-MM-DDTHH:MM:SSZ"
reflect_post: ""   # PENDING sentinel set by the final-phase POST reflect item; operator records {verdict, run_id, report} in a fresh session
```

**How the spec changes it (FR-12, FR-2, FR-5, FR-10, NFR-3):** `spec_path:` is preserved unchanged (still threaded into Mode 1 `--spec` and read by Mode 2 wrapper). The frontmatter region is where the **new single-source-of-truth field `reflect_post_mode:`** must be added (NFR-3: "exactly one frontmatter field records the resolved mode"). Per spec it records one of `{none, 1, 2, auto-resolved-1, auto-resolved-2, halt, 2-degraded-halt}`. This block (`:1933-1942`) is the insertion site.

### Surface 4b — Frontmatter `reflect_post: ""` PENDING sentinel (live `:1942`, spec `:1942`)

Verbatim (line 1942):

```text
reflect_post: ""   # PENDING sentinel set by the final-phase POST reflect item; operator records {verdict, run_id, report} in a fresh session
```

**How the spec changes it (FR-2, FR-7):** Under `--reflect none`, this key is **omitted entirely** (FR-2: "`reflect_post:` is omitted entirely — no PENDING sentinel"). Under modes 1/2/halt the sentinel is retained but the inline comment's "in a fresh session" wording becomes mode-dependent (Mode 1 = same session; Mode 2 = wrapper writes it; halt = fresh session). The builder will likely add `reflect_post_mode:` adjacent (above or below) this line.

---

## Surface 5 — CURRENT POST ITEM (V15 byte-exact anchor) (live `:1994-1999`, spec `:1994-1999`)

**THIS IS THE NFR-2 / V15 BACK-COMPAT ANCHOR. Byte-for-byte exact. Reached verbatim via dial position `halt` / `2-degraded-halt` (§6.4).** It is the penultimate item of `## Phase N: [Final Phase ...]` (header at `:1992`), immediately before `Update task status to Done` (`:2001`). All 6 lines (item header + 5 fields):

```text
- [ ] **N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses.
  - **Action**: Do NOT run reflect inside this session. Write `reflect_post: PENDING` to this file's frontmatter, then STOP and surface this paste-ready command for the operator to run in a NEW session: `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}` — where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset), `{DEPTH}` is floored at `standard` per O4 (the POST gate NEVER runs `--depth quick`), and the spawned reflect agent uses the default subagent model. The gate command uses `/sc:reflect` and never the `sc:task` execution command.
  - **Output**: Frontmatter `reflect_post: PENDING`; paste-ready `/sc:reflect --mode post` command surfaced for a fresh session.
  - **Verification**: `reflect_post` is PENDING and the operator has the exact `/sc:reflect` command. The item does NOT self-resolve.
  - **Completion gate**: Operator has run `/sc:reflect --mode post` in a fresh session and recorded its verdict (`reflect_post: {verdict, run_id, report}`) in frontmatter. Only THEN may the Update-status-to-Done item proceed (HALT per `feedback_human_decision_items_must_halt`).
```

**Placeholders present (resolved at A.9 per spec §6 / `:1996`):** `{TASK_FILE}`, `{SPEC_PATH}` (inside optional `[--spec {SPEC_PATH}]`), `{DEPTH}`, `{EXECUTOR_CLASS}`. Plus the literal `<BASE>` resolution clause: *"where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset)"*. Note `<BASE>` is angle-bracket literal in the manual item (operator substitutes), whereas spec §6.3 Mode 2 uses `{BASE}` curly-brace (builder/wrapper resolves) — a meaningful distinction the builder must preserve.

**Byte-exactness requirements for V15 (NFR-2):**
- Item title: `**N.{X-1} — Independent post-execution reflection gate (fresh session, HALT)**` — note "reflection" (full word) here vs spec §6.3's "reflect gate" — the **manual/halt** template keeps "reflection gate (fresh session, HALT)"; only Mode 2 (§6.3) changes the title to "reflect gate (wrapper subprocess, HALT)". V15 anchor must keep "**reflection** gate (**fresh session**, HALT)".
- The em-dash `—` (U+2014) appears in the title and Action.
- `[--spec {SPEC_PATH}]` square-bracket-optional syntax.
- `{DEPTH}` floored-at-standard clause "per O4 (the POST gate NEVER runs `--depth quick`)".
- HALT clause cites `feedback_human_decision_items_must_halt`.

Per §6.4, `2-degraded-halt` appends exactly one `<!-- wrapper-absent: degraded from Mode 2 -->` comment to the Context; the gate text is otherwise byte-identical. The §6.3.1 unified diff (spec lines 545-578) is the implementer's authoritative byte-delta of Mode 2 vs this anchor.

### Surface 5b — Following `Update task status to Done` item (live `:2001-2006`) — proves "penultimate"

Verbatim (the item the POST gate sits immediately before):

```text
- [ ] **N.X — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter: status to "🟢 Done", set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows "🟢 Done".
  - **Completion gate**: Task marked complete.
```

**Preceding item:** The POST gate at `:1994` is the FIRST item in `## Phase N` (the template's final phase shows only these two items: POST gate then Update-Done). In a real generated tasklist the "immediately-preceding item" is the last QA/validation/test item of the final phase. The template proves the **structural invariant**: POST item = penultimate, Update-Done = last (Critical Rule 15 anti-orphaning, validation-checklist `:2051`). Under `--reflect none` (FR-2) the final phase goes straight from the last QA item to `Update task status to Done` with no POST item between.

---

## Surface 6 — Validation-checklist POST-item assertion (live `:2051`, spec `:2051`)

In `## Task File Validation Checklist` (header `:2024`, "QA agent (A.10) validates ... against these criteria" at `:2026`). Verbatim (line 2051):

```text
- [ ] POST reflect item present and positioned penultimate (immediately before Update-status-to-Done) when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted
```

Immediately preceded by TB-Add-8 (`:2050`) and the anti-orphaning checklist item at `:2040` (`- [ ] Task completion items inside final phase (anti-orphaning)`).

**How the spec changes it (FR-9.5 invariant, §9):** the literal `when POST_REFLECT_GATE is ENABLED` predicate must change to the dial-aware form (e.g. "when `reflect_post_mode != none`"). Per spec §9 / FR-9 the validation must mechanically prove "emitted item == selected mode" from `reflect_post_mode:` frontmatter alone. This is the present-and-penultimate assertion researcher-03 (rf-qa/validation) co-owns; this inventory pins the rename anchor at **`:2051`** and the literal predicate string `when POST_REFLECT_GATE is ENABLED`.

---

## Surface 7 — Per-gate `task-integrity` counter region (spec `~:2094`)

**DRIFT NOTE:** The brief/spec cite `~:2094` for "the per-gate `task-integrity` counter region". Live `:2094` is **Critical Rule 12** (retry counters), which *enumerates* the cap `task-integrity=2` but is not the cap-definition table. The actual per-gate caps appear at TWO live sites:

### 7a — Hard-cap check (live `:1116`, inside the Retry Monotonicity Protocol)

```text
3. **Hard-cap check.** If the per-gate cycle counter has reached the gate-specific cap (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3 — see the rf-task-builder.md per-gate cap table, with the global 3-cycle backstop at `rf-team-lead's Fix Cycles rule`), HALT per the gate's existing escalation path (HALT-and-escalate or Open Questions).
```

### 7b — Critical Rule 12 (live `:2094`) — the literal `:2094` the spec cited

```text
12. **Builder mediation has separate retry counters.** RESEARCH_NEEDED (max 2 rounds) and MALFORMED (max 2 rounds) are tracked independently. A builder that needs more research twice and then produces a bad file gets 4 total invocations, not 2. **Halt-precedence rule (FR-CONV.5 / API-004 — COMP-001-M5-r12 hard invariant).** Every retry counter — including these two and every per-gate counter in rf-task-builder/rf-qa — is governed by the strict 4-step ordering `regression → monotonicity → hard-cap → proceed`; the regression halt-message `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (byte-exact wire string) is emitted BEFORE the monotonicity halt-message `[HALT-MONOTONICITY] |F|=<n>` (byte-exact wire string) on every cycle transition `n → n+1`. Counters are NEVER collapsed across gates; the existing per-gate caps (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3) and the global 3-cycle backstop at `rf-team-lead's Fix Cycles rule` remain the fourth-precedence step.
```

**How the spec changes it:** The `--reflect` refactor does NOT add a new retry counter or gate (NFR-1: "the builder's only added logic is mode resolution + depth passthrough"). The `task-integrity=2` cap is the rf-qa structural-validation gate that re-checks the emitted POST item (Surface 6). So Surfaces 7a/7b are **read-only context** for the builder — the rf-qa task-integrity gate is the mechanism that will enforce the *new* dial-aware validation assertion (Surface 6) within its existing 2-cycle cap. No edit expected here; documented because the brief asked for it and because it explains WHERE the Surface-6 assertion gets enforced (and within what cycle budget). The "task-integrity counter" the brief means = this rf-qa gate, defined in `rf-task-builder.md` per-gate cap table and surfaced at `:1116`/`:2094`.

---

## Surface 8 — Critical Rule 19 (live `:2108`, spec `:2108`)

In `## Critical Rules (Non-Negotiable)` (header `:2070`). Verbatim (line 2108, single logical line):

```text
19. **POST reflect gate in generated task files.** When the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase (immediately before the `Update task status to Done` item, preserving anti-orphaning per the validation checklist), a fresh-session reflect handoff item. The item MUST NOT run reflect inline in the executor's biased context; it writes a `reflect_post: PENDING` sentinel and HALTs until the operator records the verdict in a fresh session. The handoff command uses `/sc:reflect` for the gate and `/task` (never `/sc:task`) for any re-execution. A generated task file that omits the POST reflect item when `POST_REFLECT_GATE: ENABLED` is a MALFORMED output.
```

**How the spec changes it (THE CORE BEHAVIORAL RULE):** This rule currently hard-codes the one-size-fits-all behavior the refactor replaces:
- `` `POST_REFLECT_GATE: ENABLED` `` → must become dial-aware (`REFLECT_POST_MODE` / resolved `m`).
- "a **fresh-session** reflect handoff item" → only true for `halt`/`2-degraded-halt`; Mode 1 = inline same-session, Mode 2 = wrapper shell-out.
- "The item **MUST NOT run reflect inline**" → directly **contradicted by FR-3 Mode 1** (which DOES run `/sc:reflect` inline same-session, audit-only). This sentence must be conditioned on mode (`MUST NOT run inline` applies to modes 2/halt, NOT mode 1).
- "writes a `reflect_post: PENDING` sentinel and HALTs until the operator records the verdict in a fresh session" → mode-specific (Mode 1 writes verdict inline; Mode 2 wrapper writes it; halt uses PENDING+fresh-session).
- The `/task` (never `/sc:task`) re-execution clause is preserved across modes.
- Final MALFORMED clause's predicate `when POST_REFLECT_GATE: ENABLED` → dial-aware (`when reflect_post_mode != none`).

This is the single richest behavioral edit surface. Likely rewritten substantially OR split into per-mode sub-clauses. Anchor: **`:2108`**, literal field token `` `POST_REFLECT_GATE: ENABLED` `` appears TWICE in this rule (open and the MALFORMED tail).

---

## Surface 9 — `## Reflect Depth (Deterministic TCS)` heading + range (NOTE-ONLY; researcher-02 owns internals)

- Heading: `## Reflect Depth (Deterministic TCS)` at live **`:2114`** (spec cite `:2114`).
- Section body runs **`:2114` through `:2156`** (closing `---` at `:2156`; next section `## Research Quality Signals` at `:2158`). Spec frontmatter cited `:2114-2155`.
- Intro paragraph at `:2116` (defines TCS as pure-arithmetic + single bounded ±4 tiebreaker).
- **O1-O4 overrides at `:2149-2152`** (spec cites O1 `:2149`, O2 `:2150`, O4 `:2152` — all confirmed exact):
  - O1 (`:2149`): `S5 > 0` ⇒ floor `--depth standard`.
  - O2 (`:2150`): `S6 = 1` ⇒ force `--depth deep`.
  - O3 (`:2151`): item-count cap ⇒ floor `standard`.
  - O4 (`:2152`): POST-gate depth floor HARD RULE — POST depth ∈ {standard, deep}, NEVER quick.
- **±4 TCS tiebreaker** at `:2154` (spec cites `:2154` — confirmed: `tcs_boundary_inference` recorded clause).

The spec's §4 `auto` predicate REUSES this machinery (S5/S6 signals + resolved TCS band) — researcher-02 owns the arithmetic (S5 `:2126`, S6 `:2127`, TCS formula `:2134` per spec; I did not re-verify those internal lines as they are 02's scope). NO edit to this section expected (NFR-1: no depth-derivation logic authored into emitted items; §7 O4 "preserved and strengthened, never deleted"). The §4 auto rule is a thin band-reading wrapper over it.

---

## Cross-cutting: where "A.9" concretely maps (the emission/resolution producer seam)

The spec repeatedly says the mode is computed by "exactly one producer (the builder, at A.9)" (§ thesis, FR-9, NFR-3). Concrete mapping in the live file:

- **`### A.9: Spawn Builder` header = live `:785`.** A.9 is the section where the orchestrator assembles the **BUILD_REQUEST** (the `text` fence `:791`-onward) and spawns the `rf-task-builder` agent via the Agent tool (`:787`, and execution-overview step 10 at `:160`: "Spawn the `rf-task-builder` agent via Agent tool with structured BUILD_REQUEST (A.9)").
- The `POST_REFLECT_GATE` block (Surface 2, `:853-856`) is the **A.9 schema field** the orchestrator populates → this is where `m` is *recorded into the BUILD_REQUEST* and handed to the builder.
- **Important nuance for the builder:** the *actual emission* of the POST item template into the generated MDTM is done by the **`rf-task-builder` agent** (`rf-task-builder.md`, not SKILL.md), driven by the `POST_REFLECT_GATE` BUILD_REQUEST field + Critical Rule 19 (`:2108`) + the Output-Structure template (`:1994-1999`). SKILL.md's A.9 is the **resolution + hand-off producer**; rf-task-builder is the **template emitter**. The spec's "A.9 single producer" = the SKILL.md orchestrator computing `m` once and passing it via the BUILD_REQUEST `POST_REFLECT_GATE`→`REFLECT_POST_MODE` field. The §4 RESOLVE_AUTO predicate, the §8 wrapper-availability probe (`W`), and the §10 precedence chain all execute at this A.9 site (`:785`-`:856`).
- Researcher-04 (plumbing) owns the precedence/map design that threads `--reflect` → A.2 parse (`:201`) → A.9 BUILD_REQUEST field (`:853`) → frontmatter `reflect_post_mode:` (insert near `:1942`) → emitted item.

**Consequence:** a complete refactor touches BOTH `SKILL.md` (orchestrator resolution + BUILD_REQUEST schema + frontmatter template + validation checklist + Critical Rule 19 + Input/A.2 docs) AND `rf-task-builder.md` (the per-mode template emitter). This inventory covers only SKILL.md per scope; the builder must NOT assume the emitted-item bodies (§6.2/§6.3/§6.4) live in SKILL.md — only the `halt`/V15 byte-anchor body (`:1994-1999`) does, as part of the Output-Structure *template*.

---

## Status: Complete

## Summary

All 9 brief surfaces inventoried byte-exact with confirmed live line numbers. **Key finding: the live file tracks the spec's cited line numbers almost perfectly** — every spec-cited surface was found at its cited line, so the byte-for-byte V15 anchor (`:1994-1999`) and all rename anchors are reliable.

Pinned anchors (live lines):
- `:41` `--spec` Input doc; `:201` SPEC_PATH A.2 component.
- `:853` `POST_REFLECT_GATE: ENABLED` (rename → `REFLECT_POST_MODE`); sub-fields `:854-856`; mediation context `:831-851`.
- `:1423` A.10.7 PRE cross-ref (cosmetic update only; PRE out of scope).
- `:1933` frontmatter `spec_path:`; `:1942` `reflect_post: ""` sentinel (insertion site for new `reflect_post_mode:`).
- **`:1994-1999` CURRENT POST ITEM — V15 byte-exact anchor** (reached via dial `halt`/`2-degraded-halt`; title keeps "reflection gate (fresh session, HALT)"; `<BASE>` angle-literal vs §6.3 `{BASE}` curly; placeholders `{TASK_FILE}`/`[--spec {SPEC_PATH}]`/`{DEPTH}`/`{EXECUTOR_CLASS}`). `:2001-2006` Update-Done item proves penultimate.
- `:2051` validation-checklist present-and-penultimate assertion (predicate `when POST_REFLECT_GATE is ENABLED` → dial-aware).
- `:2108` **Critical Rule 19** — richest behavioral edit; contains the load-bearing contradiction with FR-3 ("MUST NOT run reflect inline" vs Mode 1 inline); `POST_REFLECT_GATE: ENABLED` appears 2× in it.
- `:2114-2156` TCS section (O1-O4 at `:2149-2152`, ±4 tiebreaker at `:2154`) — researcher-02 owns; no edit expected.

Three drift/tripwire notes for the builder:
1. **Spec `:2094` per-gate counter** maps to live `:1116` (hard-cap check, the real cap enumeration) AND `:2094` (Critical Rule 12). The "task-integrity=2" cap is the rf-qa gate that *enforces* the Surface-6 validation assertion within a 2-cycle budget — read-only context, no edit.
2. **"M1-frozen 15-field BUILD_REQUEST ... byte-identical" claim at `:847`** is a back-compat tripwire when `POST_REFLECT_GATE` is renamed/retired — flag to researcher-04 (plumbing).
3. **A.9 is a resolution+hand-off producer in SKILL.md (`:785`-`:856`), but the per-mode item BODIES (§6.2/§6.3) are emitted by `rf-task-builder.md`, NOT SKILL.md.** Only the `halt`/V15 anchor body lives in SKILL.md's Output-Structure template. A complete refactor spans both files; this inventory is SKILL.md-only per scope.
