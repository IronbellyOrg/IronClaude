# Research 03 — rf-qa.md task-integrity + §9 V1–V16 validation matrix + MODE-MATCH integration

**Status: Complete**
**Topic:** Integration design for the V1–V16 assertion matrix, per-mode active-assertion map, and the MODE-MATCH task-integrity assertion into `rf-qa.md`, plus the two SKILL.md validation-surface rewrites (:2051, :2108).
**Date:** 2026-06-08

This file is built incrementally per the task-builder research protocol.

All file:line citations below are against the worktree
`/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/`, files
`src/superclaude/agents/rf-qa.md` (552 lines) and
`src/superclaude/skills/task-builder/SKILL.md`.

---

## §A. rf-qa.md structure map (read fully, 552 lines)

rf-qa.md is a flat agent-definition file organized as: frontmatter (`:1-33`) →
intro/philosophy (`:35-39`) → "What You Receive" (`:41-50`) → "Parallel
Partitioning" incl. the giant DNSP/PR-03 orchestrator paragraph (`:52-84`) →
"Verification Principles" (`:88-99`) → "Web Research Tooling (Tavily-first)"
(`:103-121`) → then the **five QA-phase sections**, each a `## QA Phase: …`
heading:

| QA Phase section | rf-qa.md lines | Checklist size |
|---|---|---|
| Research Gate (pre-synthesis) | `:125-171` | 10 items (`#### Checklist (10 items)` `:138`) |
| Synthesis Gate (pre-assembly) | `:175-243` | 12 items (`#### Checklist (12 items)` `:184`) |
| Report Validation (post-assembly) | `:246-288` | 19 items (`#### Validation Checklist (19 items …)` `:255`) |
| **Task Integrity Check** | **`:291-379`** | **28 items (`#### Checklist (28 items)` `:298`)** |
| Fix Cycle | `:382-418` | (process, not a numbered checklist) |

Then shared tails: "Output Format (All Phases)" (`:422-461`), "Completion
Protocol" (`:465-481`), "Confidence Gate Protocol" (`:484-535`), "Critical
Rules" (`:539-552`, 12 rules).

**The Task Integrity Check section (`:291-379`) is the integration target.** Its
internal structure:

- `## QA Phase: Task Integrity Check` heading at `:291`, with When/Purpose
  (`:293-294`) and `### What You Verify (Task Integrity)` (`:296`).
- `#### Checklist (28 items)` at `:298`. Items **1–20** (`:300-328`) are the
  base task-integrity checks.
- `#### Structural Gate Additions (TB-Add-1 through TB-Add-7, imported from
  sc:tasklist 17-point gate per CB-3 per-check classification)` at **`:330`**,
  followed by a 2-line rationale (`:332`), then items **21–28** = TB-Add-1
  through TB-Add-8 (`:334-378`).

> NOTE on the heading vs. body count drift: the heading at `:330` literally says
> "TB-Add-1 through TB-Add-7" but the body actually runs through **TB-Add-8**
> (item 28, `:369-378`). This is a pre-existing cosmetic drift in the source —
> the builder adding TB-Add-9 should update this heading to "TB-Add-1 through
> TB-Add-9" (or, cleaner, "TB-Add-1 through TB-Add-N") to avoid compounding it.

---

## §B. The TB-Add entry format (verbatim, byte-stylistic template)

The new assertion block must match this format exactly. The TB-Add region uses
**top-level ordered-list numbering continuous with the base checklist** (the
base checklist ends at item 20; TB-Add-1 is item **21**, TB-Add-8 is item
**28**). Each entry's bold token is `**TB-Add-N: <name> (source).**` followed by
the body on continuation lines indented 4 spaces.

Verbatim first entry (`:334-339`), shortest exemplar of the format:

```text
21. **TB-Add-1: Placeholder scan (sc:tasklist check 11).** No checklist item contains the literal
    tokens `TBD`, `TODO`, or `FIXME` in its description or body, and no item is title-only
    (it MUST have a Context, Action, Output, Verification, and Completion-gate body).
    Title-only or placeholder-only items reinforce the self-contained-item invariant by failing the
    5-field schema. Error message format: "Item X.Y contains 'TBD'/'TODO' on line N — replace with
    concrete description". Use Grep on the task file to detect.
```

Verbatim last entry (`:369-378`, TB-Add-8 — shows the multi-clause body shape
with a parenthetical sub-clause in the bold token):

```text
28. **TB-Add-8: Per-item Context evidence binding (PR-01 REVISE acceptance criterion — INV-015
    scope-confinement).** Every per-item Context field that references a code surface
    (a function, class, module, config field, or specific file) MUST include at least one file:line
    citation OR a `<!-- evidence-absence: ... -->` justified-absence comment explaining why no
    file:line is given (e.g., "this item creates a new file; no source line yet").
    ...
    Use Read + Grep on each item's Context paragraph to verify a file:line pattern or evidence-absence
    comment is present. Error message format: "Item X.Y Context references `[surface]` but contains no
    file:line citation and no evidence-absence justification — add either".
```

**Byte-stylistic rules a TB-Add-9 must obey:**

1. Number is `29.` (continues the ordered list; the heading count in
   `#### Checklist (28 items)` at `:298` must bump to `(29 items)`).
2. Bold token shape: `**TB-Add-9: <name> (<source citation>).**` — name in
   Title-ish case, source in parentheses ending the bold span, period **inside**
   the `**…**`. (Existing sources cite `sc:tasklist check N` or a `PR-01 …`/`INV-…`
   token; this one would cite the spec, e.g. `(spec §9.3 MODE-MATCH / FR-9)`.)
3. Body lines indented exactly **4 spaces** under the number.
4. Pattern of the body: one or more declarative MUST sentences, an "Error message
   format:" clause, and a "Use Grep/Read …" detection-method clause (every TB-Add
   names its detection tool — TB-Add-1 "Use Grep", TB-Add-8 "Use Read + Grep").

---

## §C. INV-010 auto-richening consequence of adding a TB-Add-9 (CRITICAL)

The SKILL.md A.10.5 procedure **dynamically reads rf-qa.md's `#### Structural Gate
Additions` region at runtime** and pulls the TB-Add catalogue via regex — it does
NOT hand-maintain the list. Evidence (verbatim from SKILL.md):

- `SKILL.md:1335` — "The TB-Add-* catalogue is sourced from `rf-qa.md`'s live
  'Structural Gate Additions' section at runtime — never from a hand-maintained
  list inside this skill."
- `SKILL.md:1338` — bounds the region: "Identify the `#### Structural Gate
  Additions` heading and treat the catalogue region as the span from that heading
  to the next `####`, `###`, or `##` heading (whichever comes first)."
- `SKILL.md:1339` — the extraction regex: "match the regex
  `^[0-9]+\. \*\*TB-Add-([0-9]+):` (Python `re` flavour, MULTILINE) against the
  span. Each match yields one TB-Add-N ID via the captured integer N."
- `SKILL.md:1346` — the TEST-010 / T03.15 structural-diff fixture "adding a
  synthetic TB-Add-N+1 stub to `rf-qa.md`'s bounded region and asserting the
  cycle-2 spawn prompt auto-richens by exactly one TB-Add-N+1 row."
- `SKILL.md:1393` (DM-005 phase contract) — `enumeration_rule:
  INV-010-auto-pick-TB-Add`: "Future structural additions to rf-qa.md auto-extend
  the verdict passthrough."

**Consequence (load-bearing for the integration-shape recommendation):** if the
V1–V16 + MODE-MATCH assertion is authored as a **new numbered TB-Add-9 entry
inside the bounded `#### Structural Gate Additions` region**, matching the
`^[0-9]+\. \*\*TB-Add-([0-9]+):` regex shape (i.e., `29. **TB-Add-9: …**`), it is
**automatically picked up** by:

1. The A.10.5 `LIVE_TB_ADD` enumeration (`SKILL.md:1335-1343`) — handed to
   rf-qa-qualitative on every spawn and every fix-cycle re-entry (`:1328`,
   `:1341`).
2. The INV-010 cross-check (`SKILL.md:1341`) — the producer (rf-qa) report's
   "Items Reviewed" TB-Add rows are cross-checked against `LIVE_TB_ADD`; a
   TB-Add-9 row will be expected once it exists in rf-qa.md.
3. The structured log line (`SKILL.md:1343`) — `size=K ids=[TB-Add-1,...,TB-Add-K]`
   bumps from K=8 to K=9 automatically.

**This is the lowest-friction property.** A standalone subsection or a
parameterized sub-block placed OUTSIDE the bounded region would NOT match the
regex and would NOT auto-richen — it would have to be wired in by hand
elsewhere, defeating INV-010. Therefore the regex shape is the single most
important constraint on the integration design.

**Caveat the builder must encode:** the heading-count bump (`#### Checklist (28
items)` → `(29 items)` at `:298`) and the `#### Structural Gate Additions
(TB-Add-1 through TB-Add-7 …)` heading text at `:330` are NOT read by the regex,
so they don't break enumeration — but they should still be corrected for
honesty (the existing heading already lags the body; see §A note). The TB-Add-9
entry itself MUST live between the `#### Structural Gate Additions` heading
(`:330`) and the next heading (`## QA Phase: Fix Cycle` at `:382`) so the bounded
span (`SKILL.md:1338`) contains it. Item 28 (TB-Add-8) ends at `:378`, then a
`---` rule at `:380`, then `## QA Phase: Fix Cycle` at `:382` — so the TB-Add-9
entry must be inserted **after `:378` and before the `---` at `:380`** to stay
inside the bounded region (the `---` thematic break does not close the span — the
span closes at the next `##`/`###`/`####` heading per `:1338`, which is `:382`;
but placing it before the `---` keeps it visually grouped with the other TB-Adds
and unambiguously inside the catalogue).

---

## §D. task-integrity QA-mode description + division of labor

**How task-integrity is described in rf-qa.md:** It is one of the five QA phases.
The spawn prompt selects it via the `QA_PHASE` field ("Which QA phase:
research-gate, synthesis-gate, report-validation, task-integrity, or fix-cycle" —
rf-qa.md `:45`). The phase's own spec is the `## QA Phase: Task Integrity Check`
section (`:291-379`), whose When is "After task file creation (A.8 in
tech-research), to verify the task file is well-formed" (`:293`) and whose
Purpose is "Ensure the MDTM task file follows template rules and will execute
correctly" (`:294`). The agent's checks ARE the 28-item checklist; the agent
applies them and emits a `VERDICT: PASS/FAIL` report.

**Division of labor (rf-qa.md vs SKILL.md):**

| Surface | Role | Evidence |
|---|---|---|
| **rf-qa.md `:298-379`** | The agent's **authoritative check definitions** — the full prose of each of the 28 items (1–20 base + TB-Add-1..8). This is what the rf-qa agent reads and executes. | rf-qa.md `:298-379` |
| **SKILL.md `:2030-2051`** | The orchestrator-side **validation checklist** (a `- [ ]` bullet list the builder self-applies / hands as a summary). Items TB-Add-1..8 appear here as one-line summaries (`:2043-2050`); item `:2051` is the POST-reflect-presence check. | SKILL.md `:2030-2051` |
| **SKILL.md Critical Rule 19 (`:2108`)** | The orchestrator-side **MALFORMED rule** that obliges the builder to EMIT the POST item and FAIL the build if it is omitted. | SKILL.md `:2108` |
| **SKILL.md A.10 / A.10.5 (`:1174`, `:1194`, `:1335-1346`)** | The orchestrator **runs** rf-qa in task-integrity mode (A.10) and dynamically enumerates rf-qa.md's TB-Add catalogue (A.10.5 / INV-010). | SKILL.md `:161`, `:1174`, `:1335` |

So: **the agent's checks live in rf-qa.md; the orchestrator's summary checklist +
MALFORMED obligations live in SKILL.md.** The V1–V16 *check definitions* belong in
**rf-qa.md** (as the new TB-Add-9 body + the per-mode active map). The SKILL.md
`:2051` checklist bullet and Critical Rule 19 (`:2108`) are the orchestrator-side
**obligation + summary** that must be rewritten to reference the dial and the new
assertion set rather than the legacy single `POST_REFLECT_GATE: ENABLED` string.

**Where MODE-MATCH (§9.3) should be authored:** Spec §9.3 says MODE-MATCH is added
to "the per-gate `task-integrity` counter at `SKILL.md:2094`". **This is a spec
imprecision** — `SKILL.md:2094` is actually **Critical Rule #12 (retry counters:
"Builder mediation has separate retry counters")**, NOT a task-integrity check
surface (verified: SKILL.md `:2094` verbatim begins "12. **Builder mediation has
separate retry counters.**"). The phrase "per-gate task-integrity counter" maps to
the **per-gate cap `task-integrity=2`** that appears at `SKILL.md:1116` and
`:2094` (the cap list `research-gate=3, synthesis-gate=2, report-validation=3,
task-integrity=2, qualitative=3`). MODE-MATCH is a *check*, not a *counter*, so it
should NOT be authored into the retry-counter rule. The correct home for the
**MODE-MATCH assertion body is rf-qa.md's Task Integrity Check section** (as part
of, or immediately following, the TB-Add-9 entry), because §9.3 itself states
MODE-MATCH "is the rf-qa expression of FR-9's single-producer guarantee" and that
"rf-qa's `task-integrity` mode … runs the subset of V1–V16" (spec §9.2). The
SKILL.md side gets the MALFORMED obligation (rewrite of Critical Rule 19, `:2108`)
and the checklist bullet (rewrite of `:2051`). The builder should treat the spec's
`:2094` citation as "the task-integrity gate," realized as an rf-qa.md check, not
as an edit to Critical Rule #12.

---

## §E. §9.1 V1–V16 table + replace/extend/reuse mapping

The 16 assertions (spec §9.1, merged-requirements `:722-739`). For each, what
existing rf-qa.md / SKILL.md check it REPLACES, EXTENDS, or REUSES. Per spec
`:720`: "These replace the legacy single-string checklist item at `SKILL.md:2051`
and Critical Rule 19 at `SKILL.md:2108`." Per spec §9.3 `:773`: "The existing
penultimate / `reflect_post` / HALT / `/sc:reflect`-vs-`/sc:task` checks are
**reused**; only the mode-shape assertion set is added."

| # | Assertion (short) | Pass condition (spec) | Replaces / Extends / Reuses |
|---|---|---|---|
| V1 | `REFLECT_POST_MODE` field in BUILD_REQUEST present | value ∈ `{1,2,auto,none}` | NEW (replaces the legacy `POST_REFLECT_GATE: ENABLED` presence assumption baked into `:2051`/`:2108`) |
| V2 | `reflect_post_mode` frontmatter field present | ∈ `{none,1,2,auto-resolved-1,auto-resolved-2,halt,2-degraded-halt}` | NEW (the oracle field; no prior equivalent) |
| V3 | POST item count matches mode | `none`→0; else→exactly 1 | EXTENDS the existing "POST reflect item present … when POST_REFLECT_GATE is ENABLED" check (`:2051`) — now count is mode-parameterized incl. the 0-item `none` case |
| V4 | Item position penultimate | at N.{X-1}, immediately before Update-status-to-Done | **REUSE** of the existing penultimate/anti-orphaning check (`:2051` "positioned penultimate"; Critical Rule 15 `:2100`) |
| V5 | Mode 1 Action has inline `/sc:reflect --mode post --depth standard` | top-level skill invocation | NEW (no Mode-1 form existed) |
| V6 | Mode 1 Action lacks shell-out/wrapper markers | no `superclaude reflect run`/`Bash`/`Run:` | NEW |
| V7 | Mode 2 Action has Bash `superclaude reflect run {TASK_FILE}` | shell-out present | NEW (wrapper form is new) |
| V8 | Mode 2 Action lacks inline `/sc:reflect` / Agent/Task | no inline, no subagent | NEW (encodes NFR-7 no-nesting) |
| V9 | Mode 1 Action lacks `--remediate` | absent | NEW (FR-8 audit-only) |
| V10 | Mode 2 remediation delegated to wrapper | wrapper owns `--remediate`/`--no-promote` | NEW (NFR-1 no-duplication) |
| V11 | Non-`none` write-back / sentinel discipline | 1/2 write `reflect_post:{verdict…}`; halt/2-degraded-halt write `reflect_post: PENDING` | **REUSE+EXTEND** of the existing `reflect_post: PENDING` sentinel rule (Critical Rule 19 `:2108`; frontmatter sentinel `:1942`) — extended so PENDING is now mode-conditional (§9.5) |
| V12 | Both active modes HALT/STOP on non-pass | HALT language + no self-resolve | **REUSE** of the existing HALT rule (Critical Rule 19 `:2108` "writes a `reflect_post: PENDING` sentinel and HALTs"; `feedback_human_decision_items_must_halt`) |
| V13 | `{SPEC_PATH}` threading matches resolved spec | `--spec {SPEC_PATH}` iff `spec_path` set | EXTENDS existing `--spec` threading (SKILL.md `:41`, FR-12) into a validation assertion |
| V14 | `{BASE}` resolution instruction present | Action has BASE guidance | EXTENDS (current item `:1994-1999` already bakes `<BASE>`; now asserted) |
| V15 | Degraded/manual item byte-identical to legacy HALT | matches `SKILL.md:1994-1999` after placeholder subst | NEW assertion enforcing NFR-2 byte-for-byte reversibility |
| V16 | Degraded frontmatter records degradation | mode ∈ `{halt,2-degraded-halt,auto-resolved-2-degraded-halt}` + wrapper-absent marker | NEW (records §8 degradation) |

**Net replace/extend/reuse summary:**

- **REPLACED:** the single-string `:2051` checklist bullet and the
  `POST_REFLECT_GATE: ENABLED`-keyed Critical Rule 19 (`:2108`) — superseded by
  the V1–V16 matrix keyed on `reflect_post_mode`.
- **REUSED verbatim (per §9.3 `:773`):** penultimate position (V4),
  `reflect_post` write-back / HALT (V11/V12), and the `/sc:reflect`-vs-`/sc:task`
  command-surface check (currently in Critical Rule 19 `:2108`: "uses
  `/sc:reflect` … and `/task` (never `/sc:task`)"). The "never `/sc:task`" check
  is NOT a numbered V-assertion but is explicitly listed in §9.3 as reused — the
  TB-Add-9 body should restate it as a per-mode invariant.
- **NEW:** the mode-shape assertions V5–V10, V15, V16 + the oracle fields V1/V2.

---

## §F. §9.2 per-mode active-assertion map (reproduced)

From spec §9.2 (merged-requirements `:741-750`). rf-qa's task-integrity mode runs
**only the subset active for the resolved `reflect_post_mode`**:

| `reflect_post_mode` value | Active assertions |
|---|---|
| `none` | V1, V2, V3 |
| `1` / `auto-resolved-1` | V1, V2, V3, V4, V5, V6, V9, V11, V12, V13, V14 |
| `2` / `auto-resolved-2` | V1, V2, V3, V4, V7, V8, V10, V11, V12, V13, V14 |
| `halt` / `2-degraded-halt` / `auto-resolved-2-degraded-halt` | V1, V2, V15, V16 (+ V3, V4 for presence + penultimate position) |

This map MUST be reproduced inside the TB-Add-9 body (or a tight sub-table
immediately under it) so the rf-qa agent knows which subset to apply. It is
parameterized by the single oracle field — the agent reads `reflect_post_mode`
first, then runs the row.

---

## §G. §9.3 MODE-MATCH assertion (reproduced) + §9.5 sentinel → V11

**MODE-MATCH** (spec §9.3, merged-requirements `:758-771`) is the rf-qa expression
of FR-9 single-producer. Verbatim pseudocode block to embed:

```text
MODE-MATCH (MALFORMED on fail): read frontmatter `reflect_post_mode`. Assert the penultimate
final-phase item's Action shape matches it, per the §9.1 table:
  reflect_post_mode == 1 / auto-resolved-1   ⇒ V5 ∧ V6 ∧ V9
  reflect_post_mode == 2 / auto-resolved-2   ⇒ V7 ∧ V8 ∧ V10
  reflect_post_mode == none                  ⇒ V3 (no reflect item; `reflect_post:` absent)
  reflect_post_mode ∈ {halt, 2-degraded-halt, auto-resolved-2-degraded-halt}
                                             ⇒ V15 ∧ V16
Mismatch between `reflect_post_mode` and the emitted Action shape = MALFORMED.
```

**Mismatch ATs to encode in the body** (spec §9.4, `:780-786`):
AT-VALIDATION-1 (`mode:1` + `superclaude reflect run` ⇒ fail V6; `mode:2` +
inline `/sc:reflect` ⇒ fail V8; `mode:1` + `--remediate` ⇒ fail V9) and
AT-MISMATCH-1 (swapped Mode-1/Mode-2 templates ⇒ MALFORMED naming the specific
V# — V6 or V8).

**§9.5 sentinel preservation → V11 (spec `:788-794`):** confirmed mapping:

| Mode | `reflect_post:` sentinel state | V11 assertion |
|---|---|---|
| `none` | key **absent** entirely | V11: no `reflect_post:` key |
| `1` / `auto-resolved-1` | written by the **inline run** (verdict block) | V11: `reflect_post:{verdict,…}` present |
| `2` / `auto-resolved-2` | written by the **wrapper** (verdict block) | V11: `reflect_post:{verdict,…}` present |
| `halt` / `2-degraded-halt` / `auto-resolved-2-degraded-halt` | `reflect_post: ""` **PENDING retained** (defers to fresh session) | V11: PENDING sentinel present |

The `reflect_post: ""` PENDING sentinel (`SKILL.md:1942`) is **retained ONLY for
halt / 2-degraded-halt** (and the auto-resolved-2-degraded-halt variant); ABSENT
for `none`; written-by-run/wrapper for 1/2. This is exactly the spec §9.5 wording
and is asserted by V11 (rf-qa.md `:734`). The frontmatter declaration to update is
`SKILL.md:1942` / `:847-851` (researcher-04 owns the value-set + sentinel
frontmatter edit; this file only maps it to V11 for the rf-qa side).

---

## §H. SKILL.md :2051 + :2108 verbatim + recommended rewrite shapes

### H.1 SKILL.md `:2051` (validation checklist bullet) — VERBATIM

```text
- [ ] POST reflect item present and positioned penultimate (immediately before Update-status-to-Done) when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted
```

Context: it is the last bullet of the `## …Validation Checklist`-style block at
`:2030-2051`, immediately following the TB-Add-1..8 summary bullets
(`:2043-2050`).

**Recommended rewrite shape (raw material, NOT the final edit):** key the bullet
on the dial, not on `POST_REFLECT_GATE: ENABLED`, and point at the V1–V16
matrix + MODE-MATCH:

```text
- [ ] POST reflect item shape matches `reflect_post_mode` per the V1–V16 matrix + per-mode active-assertion map + MODE-MATCH (rf-qa Task Integrity TB-Add-9): mode `none` → 0 items; modes `1`/`2`/`auto-resolved-{1,2}`/`halt`/`2-degraded-halt` → exactly 1 penultimate item (immediately before Update-status-to-Done) whose Action shape matches the mode — MALFORMED on count, position, or mode/shape mismatch
```

Rationale: a single bullet must (a) replace the legacy ENABLED keying with the
oracle field, (b) keep the penultimate + count obligations (V3/V4), and (c) name
the rf-qa authority so the orchestrator summary stays a *summary* (the full
definitions live in rf-qa.md TB-Add-9, not duplicated here — SoT discipline).

### H.2 SKILL.md `:2108` (Critical Rule 19) — VERBATIM

```text
19. **POST reflect gate in generated task files.** When the BUILD_REQUEST specifies `POST_REFLECT_GATE: ENABLED`, the builder MUST emit, as the penultimate item of the final phase (immediately before the `Update task status to Done` item, preserving anti-orphaning per the validation checklist), a fresh-session reflect handoff item. The item MUST NOT run reflect inline in the executor's biased context; it writes a `reflect_post: PENDING` sentinel and HALTs until the operator records the verdict in a fresh session. The handoff command uses `/sc:reflect` for the gate and `/task` (never `/sc:task`) for any re-execution. A generated task file that omits the POST reflect item when `POST_REFLECT_GATE: ENABLED` is a MALFORMED output.
```

**Recommended rewrite shape (raw material, NOT the final edit):** re-key on the
dial, make the emitted *form* mode-dependent (it is no longer always
"fresh-session … `reflect_post: PENDING`"), preserve the reused invariants
(penultimate, HALT, write-back, `/sc:reflect`-not-`/sc:task`), and delegate the
shape definitions to rf-qa.md MODE-MATCH:

```text
19. **POST reflect gate in generated task files.** The resolved `reflect_post_mode` (from `REFLECT_POST_MODE`/`--reflect`, default `2`; §10 precedence) governs the POST item the builder MUST emit. Mode `none` → no item (and no `reflect_post:` key). Modes `1`/`auto-resolved-1` → an INLINE same-session `/sc:reflect --mode post --depth standard` audit-only item (no `--remediate`, no wrapper). Modes `2`/`auto-resolved-2` → a Bash shell-out to `superclaude reflect run {TASK_FILE}` (never Agent/Task). Modes `halt`/`2-degraded-halt`/`auto-resolved-2-degraded-halt` → the byte-identical legacy fresh-session manual-HALT item writing `reflect_post: PENDING`. In every non-`none` mode the item is the penultimate item of the final phase (immediately before `Update task status to Done`, preserving anti-orphaning), HALTs on non-pass, writes `reflect_post` back, and uses `/sc:reflect` for the gate and `/task` (never `/sc:task`) for any re-execution. The emitted Action shape MUST match `reflect_post_mode` per the rf-qa Task Integrity V1–V16 matrix + MODE-MATCH (§9); any mode/shape mismatch, wrong count, or wrong position is a MALFORMED output (retry max-2 per Critical Rule #12, then halt).
```

Rationale: Critical Rule 19 is the orchestrator's MALFORMED contract; it must
enumerate the per-mode emitted form (since "fresh-session PENDING" is now only the
halt/degraded form) and route validation to the V1–V16/MODE-MATCH authority.
Legacy `POST_REFLECT_GATE: ENABLED` keying is dropped (now a deprecated alias per
§5/§10, consulted only at precedence step 3).

> Cross-track note: researcher-01 owns the verbatim current-state of `:2051`/`:2094`/`:2108`;
> the verbatim quotes above are re-confirmed from this session's Read of SKILL.md
> at those exact lines and are provided so the builder can author the rewrite
> items without a second lookup. The exact final wording is the builder's call;
> these are recommended shapes, not prescriptions.

---

## §I. RECOMMENDATION — integration shape

**Recommendation: author V1–V16 + per-mode active map + MODE-MATCH as a SINGLE new
`TB-Add-9` entry (item 29) inside rf-qa.md's `#### Structural Gate Additions`
bounded region.** NOT a standalone subsection; NOT a free-floating parameterized
sub-block outside the region.

**Rationale (3 grounds):**

1. **INV-010 auto-enumeration (decisive).** A `29. **TB-Add-9: …**` entry inside
   the `#### Structural Gate Additions` span matches the `^[0-9]+\. \*\*TB-Add-([0-9]+):`
   regex (`SKILL.md:1339`) and is therefore auto-picked-up by the A.10.5
   `LIVE_TB_ADD` enumeration, the INV-010 producer cross-check (`:1341`), and the
   structured log line (`:1343`) — zero hand-wiring. The TEST-010 fixture
   (`:1346`) already proves this auto-richening behavior for an added TB-Add stub.
   A subsection or out-of-region sub-block would NOT match the regex and would
   silently fail to propagate — the single worst integration outcome.

2. **Style consistency.** Every other structural assertion in this region is a
   numbered `**TB-Add-N: name (source).**` entry with a MUST body, an
   "Error message format:" clause, and a "Use Grep/Read" detection clause
   (§B). The V-matrix is exactly the same *kind* of structural assertion, so it
   belongs in the same list, numbered continuously (29), and bumping the
   `#### Checklist (28 items)` heading to `(29 items)`.

3. **Division of labor / SoT.** rf-qa.md is the authoritative home for the agent's
   check definitions (§D); SKILL.md `:2051`/`:2108` become thin
   summary+obligation pointers to TB-Add-9. One definition, two pointers — no
   duplication, no drift.

**Body composition for TB-Add-9** (so the single entry carries everything):

- Lead bold token: `**TB-Add-9: POST reflect mode/shape match (spec §9 V1–V16 +
  MODE-MATCH / FR-9 single-producer).**`
- Para 1: read the oracle `reflect_post_mode`; run the §9.2 active subset (embed
  the per-mode active-assertion **sub-table** from §F).
- Para 2: the V1–V16 **assertion sub-table** (from §E / spec §9.1) — kept as a
  compact table inside the entry.
- Para 3: the **MODE-MATCH** pseudocode block (from §G) + the "never `/sc:task`"
  reused invariant + the §9.5 sentinel discipline (V11 mapping table).
- Closing: "Error message format:" naming the specific failing V# (e.g. "Item
  N.{X-1} has `reflect_post_mode: 2` but Action contains inline `/sc:reflect` —
  fails V8 (MODE-MATCH mismatch)"), and a "Use Read + Grep on the frontmatter
  `reflect_post_mode` field and the penultimate item Action" detection clause.
- Verdict on fail: **MALFORMED** (retry max-2 per Critical Rule #12 / A.9
  MALFORMED mediation, then halt) — spec §9.1 `:718`.

**Builder must also (within the rf-qa.md edit item):**

- Bump `#### Checklist (28 items)` → `(29 items)` (`:298`).
- Fix the region heading `#### Structural Gate Additions (TB-Add-1 through
  TB-Add-7 …)` (`:330`) → "TB-Add-1 through TB-Add-9" (corrects the pre-existing
  `7`-vs-`8` drift while bumping to 9).
- Insert the new entry after item 28 (TB-Add-8, ends `:378`) and before the `---`
  at `:380`, keeping it inside the bounded catalogue span (closes at `## QA Phase:
  Fix Cycle`, `:382`).

This yields exactly the **two SKILL.md validation-rewrite items** (H.1 `:2051`,
H.2 `:2108`) + **one rf-qa.md TB-Add-9 edit item** the builder needs.

---

## Summary

**Status: Complete**

**Integration shape — RECOMMENDED:** Author V1–V16 + the §9.2 per-mode
active-assertion map + the §9.3 MODE-MATCH assertion as a **single new `TB-Add-9`
entry (item 29)** inside rf-qa.md's `#### Structural Gate Additions` bounded
region (`:330-378`), inserted after TB-Add-8 (`:378`) and before the `---`
(`:380`). This is the lowest-friction, style-consistent option **because the
SKILL.md A.10.5 procedure auto-enumerates the TB-Add catalogue via regex
`^[0-9]+\. \*\*TB-Add-([0-9]+):` (`SKILL.md:1339`, bounded at `:1338`), so a
correctly-shaped `29. **TB-Add-9: …**` entry auto-richens the verdict passthrough,
the INV-010 cross-check, and the log line with zero hand-wiring** (TEST-010 /
T03.15 already exercises this). A standalone subsection or out-of-region sub-block
would NOT match the regex and would fail to propagate.

**Key facts for the builder:**

1. **rf-qa.md structure:** Task Integrity Check section `:291-379`; `#### Checklist
   (28 items)` heading `:298`; base items 1–20 (`:300-328`); `#### Structural Gate
   Additions` heading `:330`; TB-Add-1..8 = items 21–28 (`:334-378`). Region
   closes at `## QA Phase: Fix Cycle` (`:382`).

2. **TB-Add entry format (verbatim §B):** `N. **TB-Add-N: <name> (<source>).**`
   bold token (period inside the `**…**`), 4-space-indented body, a MUST body + an
   "Error message format:" clause + a "Use Grep/Read…" detection clause. TB-Add-9
   = item `29.`; bump heading to `(29 items)` and the region heading to "TB-Add-1
   through TB-Add-9".

3. **INV-010 consequence (CRITICAL):** the regex shape is the binding constraint —
   match it and the entry auto-propagates (`SKILL.md:1335-1346`); miss it and it
   silently doesn't.

4. **Division of labor:** check *definitions* → rf-qa.md (TB-Add-9 body);
   orchestrator *summary + MALFORMED obligation* → SKILL.md `:2051` + Critical
   Rule 19 `:2108`.

5. **MODE-MATCH authoring location:** the spec's "`SKILL.md:2094`" citation is
   imprecise — `:2094` is Critical Rule #12 (retry counters), NOT a check surface.
   MODE-MATCH is a *check*, so author it in rf-qa.md (as part of TB-Add-9), not as
   an edit to the retry-counter rule. The "per-gate task-integrity counter" phrase
   refers to the `task-integrity=2` cap (`:1116`, `:2094`), which is untouched.

6. **V1–V16 replace/extend/reuse (§E):** REPLACES the `:2051` single-string bullet
   + `POST_REFLECT_GATE: ENABLED`-keyed Critical Rule 19 (`:2108`); REUSES (per
   §9.3 `:773`) penultimate (V4), `reflect_post`/HALT (V11/V12), and
   `/sc:reflect`-vs-`/sc:task` (currently in Rule 19); NEW = mode-shape V5–V10,
   V15, V16 + oracle V1/V2.

7. **§9.5 sentinel → V11:** `reflect_post: ""` PENDING retained ONLY for
   halt/2-degraded-halt(/auto-resolved-2-degraded-halt); ABSENT for `none`;
   written-by-run/wrapper for 1/2. Asserted by V11 (rf-qa.md `:734`). Frontmatter
   declaration at `SKILL.md:1942` / `:847-851` (researcher-04 owns that edit).

8. **Two SKILL.md rewrite items (raw material in §H):** `:2051` checklist bullet →
   key on `reflect_post_mode` + point at V1–V16/MODE-MATCH; Critical Rule 19
   (`:2108`) → enumerate the per-mode emitted form, drop ENABLED keying, route to
   the V-matrix authority, MALFORMED on mismatch.

**Cross-track consumption (no duplication):** consumed researcher-02 TCS/depth
facts indirectly (V5/V9 depth = `standard`); consumed researcher-04's value-set
`{none,1,2,auto-resolved-1,auto-resolved-2,halt,2-degraded-halt}` as the V2/
MODE-MATCH oracle; researcher-01 owns verbatim `:2051`/`:2094`/`:2108` current
state (re-quoted here for builder convenience).
