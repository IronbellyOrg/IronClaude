---
variant: 3
author_persona: "qa"
provenance: "/sc:adversarial via /sc:brainstorm — QA-focused variant"
distinctive_claim: "Every requirement is a test surface: each FR carries an acceptance test, each open question resolves to an assertion, and the rf-qa checklist is enumerated exhaustively with pass/fail criteria. The auto FER is the simplest deterministic rule (TCS + S6) that two implementers cannot disagree on."
created: 2026-06-08T19:30:00Z
---

# Spec — task-builder `--reflect auto|1|2` POST-gate refactor (Variant 3: QA)

> **Distinctive design choices:** (1) `auto` FER uses the TCS band + S6 refactor-class as the sole selector — TCS >= 35 or S6=1 -> Mode 2; otherwise Mode 1. No additional heuristics, no wrapper-availability probe (that belongs in Section 8 fallback). (2) `--reflect` subsumes both `POST_REFLECT_GATE` (on/off) and the sibling's `POST_REFLECT_MODE` into one enum; the old fields map 1:1. (3) Validation is an exhaustive, enumerated assertion list — 14 checks with explicit pass/fail — replacing the single item-19 string with a mode-aware checklist. (4) Mode 1 subagent-detection is a frontmatter signal check (`agent_tool_depth`), not a runtime probe, so the builder catches it at build time.

## 1. Problem

`src/superclaude/skills/task-builder/SKILL.md` currently emits a single fixed post-execution reflect gate item (lines 1994–1999): a HALT/fresh-session design that writes `reflect_post: PENDING`, stops, and requires the operator to manually run `/sc:reflect --mode post --remediate` in a new session. Every tasklist — trivial refactor or cross-subsystem rewrite — gets the same heavyweight ceremony.

The refactor adds a `--reflect auto|1|2` flag (**default 2**) that replaces this single item with a 3-mode quality/cost dial:

- **Mode 1** — lightweight inline audit, no remediation, same session
- **Mode 2** — full shell-out to the wrapper, remediation, executor-disjoint
- **Mode 2** is default so existing behavior is byte-identical (when the wrapper is present)

Three overlapping knobs (`POST_REFLECT_GATE: ENABLED`, sibling's `POST_REFLECT_MODE: wrapper|halt`, and `--reflect auto|1|2`) must reconcile into one coherent surface.

**QA lens:** every requirement below carries a test that a CI harness or manual checker can run and get a yes/no answer.

## 2. Functional Requirements

### FR-1 — `--reflect` flag is parsed by the orchestrator at A.2 (parse & triage)

The orchestrator accepts `--reflect auto|1|2` as a CLI-style flag. Default is `2`. Values are validated: any other token is MALFORMED (retry max-1, then halt).

**Acceptance test:** Given invocation `/task-builder "..." --reflect 1`, the BUILD_REQUEST must contain `REFLECT_POST_MODE: 1`. Given `--reflect foo`, the builder must emit `verdict: MALFORMED` within one retry cycle.

### FR-2 — `--reflect` writes a BUILD_REQUEST field `REFLECT_POST_MODE`

The resolved value (after `auto` resolution per Section 4) is written as `REFLECT_POST_MODE: 1|2` in the BUILD_REQUEST block at A.9, replacing the legacy `POST_REFLECT_GATE: ENABLED` block.

**Acceptance test:** Parse the BUILD_REQUEST block of any generated tasklist; `REFLECT_POST_MODE` must be present and match the selected mode integer. Absence when `--reflect` was specified (explicitly or by default) = MALFORMED.

### FR-3 — Builder emits per-mode POST item template

Based on `REFLECT_POST_MODE`, the builder emits exactly one of the three templates in Section 6 as the penultimate item of the final phase. The emitted item always has the 5-field schema (Context/Action/Output/Verification/Completion-gate).

**Acceptance test:** For `--reflect 1`, the final-phase item Action contains `/sc:reflect --mode post --depth standard` (inline invocation, no `--remediate`, no Bash shell-out). For `--reflect 2`, the Action contains `superclaude reflect run` as a Bash command (no inline `/sc:reflect`). The item is always positioned immediately before the `Update task status to Done` item.

### FR-4 — Every emitted item HALTs on non-pass and writes `reflect_post`

All three mode templates write `reflect_post: PENDING` to frontmatter when the reflect step does not return a clean pass. On non-pass, the item STOPs and does NOT proceed to the Done item. This honors `feedback_human_decision_items_must_halt`.

**Acceptance test:** The emitted item text for each mode contains: (a) instruction to write `reflect_post: PENDING`, (b) a STOP/HALT instruction on non-pass, (c) explicit prohibition on self-resolving.

### FR-5 — `--spec` threading is preserved across all modes

The `{SPEC_PATH}` placeholder from A.2 (resolved per `--spec` → `@file` → BUILD_REQUEST → none) is threaded into the emitted item's command for both Mode 1 and Mode 2.

**Acceptance test:** When `--spec path/to/spec.md` is passed, both Mode 1 and Mode 2 emitted items contain `--spec path/to/spec.md` in their Action. When no spec is provided, neither mode includes `--spec`.

### FR-6 — Frontmatter gains `reflect_post_mode: 1|2|auto-resolved`

The tasklist frontmatter gains a new field `reflect_post_mode` recording which mode was selected. When `auto` was the input, this records `auto-resolved` followed by the resolved integer in parentheses (e.g., `auto-resolved (2)`).

**Acceptance test:** Parse frontmatter; `reflect_post_mode` must be a string matching `^(1|2|auto-resolved \([12]\))$`. Must be consistent with the emitted item's Action.

### FR-7 — `--reflect none` disables the POST reflect item

`--reflect none` (alias: `0`, `off`) suppresses the POST reflect item entirely. The `reflect_post` frontmatter sentinel is set to `reflect_post: null`. Validation checklist item 19 and :2051 are skipped.

**Acceptance test:** Given `--reflect none`, the generated tasklist has no POST reflect item in any phase, frontmatter `reflect_post` is null, and validation does not assert its presence.

### FR-8 — Mode 2 item uses Bash shell-out, never Agent/Task

The Mode 2 emitted item's Action instructs the executor to run the wrapper via Bash (e.g., `Run: superclaude reflect run {TASK_FILE} ...`). It must NOT use Agent/Task spawning or skill invocation.

**Acceptance test:** The Mode 2 item Action text contains the word `Bash` or a shell-execution marker (`Run:`, `$ `, `bash -c`) and does NOT contain `Agent`, `Task`, `Skill`, or `/sc:`.

### FR-9 — Mode 1 item detects subagent-executor and degrades to HALT

If the builder can determine the `/task` executor will be an Agent-tool subagent (frontmatter `agent_tool_depth: >0` or equivalent signal), Mode 1 degrades to the legacy HALT form (same as current :1994–1999). The item records `reflect_post_mode: 1(degraded)`.

**Acceptance test:** When `agent_tool_depth > 0` is detected in the BUILD_REQUEST or frontmatter context, the emitted item is byte-identical to the current HALT template (:1994–1999), NOT the Mode 1 inline template.

## 3. Non-Functional Requirements

### NFR-1 — No reflect-logic duplication

Emitted items invoke or shell out to reflect; they never contain reflect's tier rubric, deviation taxonomy, or promotion logic. The item text is a handoff only.

### NFR-2 — Back-compat default is 2

When `--reflect` is not specified, the builder behaves as if `--reflect 2` was passed (Mode 2 shell-out). This is the current behavior when the wrapper is present.

### NFR-3 — SoT discipline

All edits to `src/superclaude/skills/task-builder/SKILL.md`; then `make sync-dev`. Never stage `.claude/` mirrors.

### NFR-4 — Deterministic emission

Two builders given the same inputs (BUILD_REQUEST, `--reflect` value, TCS signals) must produce byte-identical emitted items. No randomness, no model-dependent inference.

### NFR-5 — Test-surface-first design

Every FR above has an acceptance test. Section 13 provides a matrix mapping each FR to its test.

## 4. The `auto` FER (Frozen Extraction Rule)

### Selection predicate

```
auto_select(tasklist, build_request) -> mode_integer:
  tcs    = compute_TCS(tasklist, build_request)    # per :2133–2155
  s6     = extract_S6(build_request)               # per :2127, normalized type: field

  if tcs >= 35:          return 2   # TCS deep band -> wrapper, full Tier-2
  if s6 == 1:            return 2   # refactor/remediation class -> wrapper
  return 1                          # everything else -> inline audit
```

**Rationale:** TCS >= 35 means the tasklist is cross-subsystem/dependency-heavy — exactly where executor-disjointness (Mode 2's defining property) matters. S6=1 means the task is a refactor/remediation class — exactly where regression detection (Mode 2's `--remediate`) matters. Everything else is low-risk enough that Mode 1's audit-only inline check is sufficient.

**Two-implementer worked example:**

Tasklist A: S1=3, S2=1, S3=2, S4=1, S5=0, S6=0.
TCS = 3*3 + 4*1 + 2*2 + 2*1 + 5*0 + 4*0 = 9 + 4 + 4 + 2 = 19.
S6 = 0 (type: "Feature", not refactor/remediation).
TCS 19 < 35 and S6 = 0 -> **Mode 1**. Both implementers agree.

Tasklist B: S1=8, S2=4, S3=6, S4=3, S5=2, S6=1.
TCS = 3*8 + 4*4 + 2*6 + 2*3 + 5*2 + 4*1 = 24 + 16 + 12 + 6 + 10 + 4 = 72.
TCS 72 >= 35 -> **Mode 2**. Both implementers agree. (S6 also = 1, redundant signal.)

Tasklist C: S1=2, S2=1, S3=0, S4=0, S5=0, S6=1 (type: "Refactor", low breadth but regression class).
TCS = 3*2 + 4*1 + 0 + 0 + 0 + 4*1 = 6 + 4 + 4 = 14.
TCS 14 < 35, but S6 = 1 -> **Mode 2**. Both implementers agree.

### Acceptance test for auto FER (AT-AUTO-1)

Given two tasklists with known frontmatter and item content, compute TCS and S6 per the FER. Assert: (a) implementer A's mode == implementer B's mode for all three worked examples, (b) the resolved mode is written to `REFLECT_POST_MODE` in BUILD_REQUEST, (c) frontmatter `reflect_post_mode` is `auto-resolved (1)` or `auto-resolved (2)` accordingly.

## 5. Knob Reconciliation + old->new Map

### Single unified knob

`REFLECT_POST_MODE` replaces both `POST_REFLECT_GATE` (on/off) and the sibling's `POST_REFLECT_MODE` (wrapper/halt). The enum is:

| Value | Semantics | Old `POST_REFLECT_GATE` | Old `POST_REFLECT_MODE` |
|-------|-----------|------------------------|------------------------|
| `1` | Inline audit, no remediation | ENABLED | (new) |
| `2` | Wrapper shell-out, full remediation | ENABLED | wrapper |
| `none` | Disabled | DISABLED | (n/a) |

### old->new map

| Old BUILD_REQUEST | New `REFLECT_POST_MODE` | Notes |
|---|---|---|
| `POST_REFLECT_GATE: DISABLED` (or absent) | `none` | Back-compat: no POST item emitted |
| `POST_REFLECT_GATE: ENABLED` + `POST_REFLECT_MODE: wrapper` (or absent, since halt was default) | `2` (default) | Current behavior maps to Mode 2 |
| `POST_REFLECT_GATE: ENABLED` + `POST_REFLECT_MODE: halt` (legacy manual HALT) | `2` | The wrapper's HALT text is preserved on non-pass via FR-4 |

### Reconciliation with `POST_REFLECT_GATE` semantics

`POST_REFLECT_GATE: ENABLED` was a binary on/off. The new surface is a 4-value enum (`1|2|auto|none`). `none` is the direct replacement for `DISABLED`. The `auto` value is a builder-time computation that resolves to 1 or 2 — it is not a third runtime behavior.

**Acceptance test (AT-KNOB-1):** A tasklist built with the old `POST_REFLECT_GATE: DISABLED` and a tasklist built with `--reflect none` are structurally identical: no POST reflect item, `reflect_post: null` in frontmatter.

## 6. Per-Mode Emitted-Item Templates

Each template is a 5-field checklist item. The item number is `N.{X-1}` (penultimate, immediately before `N.X` = Update-status-to-Done). `{TASK_FILE}`, `{SPEC_PATH}`, `<BASE>`, `{DEPTH}`, and `{EXECUTOR_CLASS}` are resolved placeholders.

### Mode 1 — Inline audit (`--reflect 1`)

```
- [ ] **N.{X-1} — Independent post-execution reflection gate (inline audit, HALT on non-pass)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent `/sc:reflect --mode post` ensemble catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots that same-frame QA misses. This item runs reflect INLINE in the SAME session via a top-level skill invocation (NOT Agent/Task, NOT shell-out). It is audit-only: NO `--remediate` flag. If the reflect verdict is not `pass`, this item HALTs.
  - **Action**: Invoke `Skill sc:reflect-protocol` directly (top-level skill invocation by the executor, NOT via Agent/Task tool) with the flag string:
    `/sc:reflect --mode post --depth standard --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --executor-model {EXECUTOR_CLASS}`.
    Do NOT pass `--remediate`. Capture the return contract's verdict.
    - If verdict is `pass`: write `reflect_post: {verdict: pass, run_id, report}` to this file's frontmatter and proceed.
    - If verdict is NOT `pass`: write `reflect_post: PENDING` to frontmatter, STOP, and surface the report path for the operator. Do NOT self-resolve.
  - **Output**: Frontmatter `reflect_post` updated with `{verdict, run_id, report}` on pass, or `PENDING` on halt.
  - **Verification**: `reflect_post` field is populated (not empty string, not PENDING on pass path). The reflect skill was invoked as a top-level Skill, not via Agent/Task.
  - **Completion gate**: Reflect returned `pass` verdict recorded in frontmatter, OR the item is HALTed with `reflect_post: PENDING` and the operator has the report path. Only THEN may the Update-status-to-Done item proceed (HALT per `feedback_human_decision_items_must_halt`).
```

### Mode 2 — Wrapper shell-out (`--reflect 2`, DEFAULT)

```
- [ ] **N.{X-1} — Independent post-execution reflection gate (wrapper subprocess, HALT on non-pass)**
  - **Context**: All implementation/test/QA items above are complete. The inline rf-qa gates ran in THIS executor's frame and cannot perform an executor-disjoint audit. Per project memory `feedback_sc_reflect_vs_inline_rfqa`, an independent reflect audit catches spec-literal-token, invariant-arithmetic, and integration/orphan blindspots. This item shells out to the `superclaude reflect run` CLI wrapper as a top-level subprocess via Bash (NOT Agent/Task, NOT inline skill invocation), providing executor-disjoint review with full Tier-2 + Tier-3 remediation.
  - **Action**: Run the following command via **Bash shell-out** (execute in a shell subprocess, NOT via Agent/Task, NOT via Skill tool):
    `superclaude reflect run {TASK_FILE} --diff <BASE>..HEAD [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`
    where `<BASE>` is the commit recorded at task start (frontmatter `start_commit`, or `git merge-base HEAD <integration>` if unset), `{DEPTH}` is `max(tcs-derived depth, standard)` per O4, and `{EXECUTOR_CLASS}` is the executor's model class from frontmatter.
    - If the wrapper exits 0 (verdict `pass`): proceed. The wrapper has already written `reflect_post: {verdict: pass, ...}` to frontmatter.
    - If the wrapper exits non-zero (verdict `halted`/`degraded`/`blocked`): the item HALTs. The wrapper has written `reflect_post: {verdict, reason, report}`. Do NOT self-resolve. Route the `report` path + `reason` + `deviations` into the tasklist `### Open Questions`.
  - **Output**: Frontmatter `reflect_post` updated by the wrapper with `{verdict, status, run_id, tier_reached, report, contract, reason, deviations, head, reviewed_at}`.
  - **Verification**: `reflect_post.verdict` is `pass` (wrapper exited 0) and frontmatter block is populated. The command was executed via Bash shell-out, not Agent/Task.
  - **Completion gate**: Wrapper exited 0 with `reflect_post.verdict == pass`, OR the item is HALTed with a non-pass verdict and deviations routed to Open Questions. Only THEN may the Update-status-to-Done item proceed (HALT per `feedback_human_decision_items_must_halt`).
```

### Mode auto — Resolved by builder

The builder resolves `auto` to 1 or 2 per Section 4 at build time. The emitted item is byte-identical to the resolved mode's template. The frontmatter records `reflect_post_mode: auto-resolved (N)`.

**Acceptance test (AT-TEMPLATE-1):** The emitted item for Mode 1 contains `Skill sc:reflect-protocol` and `--depth standard` and does NOT contain `superclaude reflect run` or `Bash`. The emitted item for Mode 2 contains `Bash` and `superclaude reflect run` and does NOT contain `Skill` or `/sc:`. Both items contain `reflect_post: PENDING` in their HALT path.

## 7. Depth/TCS Reconciliation

### Mode fixes depth

Mode 1 always uses `--depth standard`. This is intentional: it is an audit-only inline check; `deep` would be disproportionate for same-session execution, and `quick` is forbidden by O4. `standard` is the minimum POST depth.

Mode 2 passes `{DEPTH}` which is `max(tcs-derived depth, standard)` — preserving O4's POST floor. The wrapper is passthrough (per sibling spec FR-3): it does not recompute TCS.

### Fate of O4

O4 (POST never `quick`) is preserved for both modes. Mode 1 achieves this by fixing depth to `standard`. Mode 2 achieves this by passing the TCS-derived depth floored at `standard` via the wrapper.

### Acceptance test (AT-DEPTH-1)

For a tasklist with TCS = 8 (band would yield `quick`), Mode 1 item contains `--depth standard` and Mode 2 item contains `--depth standard` (O4 floor applied). For TCS = 40 (band yields `deep`), Mode 2 item contains `--depth deep`. Mode 1 always contains `--depth standard` regardless of TCS.

## 8. Wrapper-Dependency Fallback (Mode 2)

### Builder detection mechanism

At build time, the builder checks whether the `superclaude reflect run` subcommand is available by running:
```bash
superclaude reflect run --dry-run 2>/dev/null && echo "available" || echo "absent"
```
This is a simple CLI probe — if exit 0, wrapper is present; otherwise absent.

**Acceptance test (AT-WRAPPER-1):** The detection command exits 0 when the wrapper subcommand is registered in `cli/main.py` (the `reflect run` Click group exists); exits non-zero when it is not.

### Fallback rule

If the wrapper is absent and `REFLECT_POST_MODE` resolves to 2 (either explicitly or via `auto`), the builder **degrades to the legacy HALT item** (byte-identical to current :1994–1999). The frontmatter records `reflect_post_mode: 2(degraded)`. The item text is the current manual HALT command.

This is NOT Mode 1 — Mode 1 sacrifices executor-disjointness, which is the core property of Mode 2. When Mode 2's dependency is missing, we preserve executor-disjointness by reverting to the manual HALT (which is executor-disjoint by construction: the operator runs in a fresh session).

**Acceptance test (AT-FALLBACK-1):** When the wrapper probe returns "absent" and `--reflect 2` was specified, the emitted item is byte-identical to the current HALT template (:1994–1999), with frontmatter `reflect_post_mode: 2(degraded)`. The item contains the manual `/sc:reflect --mode post --remediate` command for a fresh session.

## 9. Validation + rf-qa Changes

### Replacement of Critical Rule 19 and checklist item :2051

The current single-string validation (Critical Rule 19 at :2108 and checklist item at :2051) is replaced with a mode-aware checklist of 14 assertions. The builder's validation phase (A.10) and rf-qa's `task-integrity` mode each run these assertions.

### Exhaustive assertion list

Each assertion has a pass/fail test. Fail = MALFORMED (retry max-2, then halt).

| # | Assertion | Pass condition | Fail condition |
|---|-----------|---------------|----------------|
| V1 | `REFLECT_POST_MODE` field present in BUILD_REQUEST | Field exists with value `1`, `2`, `auto`, or `none` | Field absent or value not in valid set |
| V2 | `reflect_post_mode` frontmatter field present | Field matches regex `^(1|2|none|auto-resolved \([12]\)|1\(degraded\)|2\(degraded\))$` | Field absent or malformed |
| V3 | POST item count matches mode | Mode `none` -> 0 items; modes `1`/`2`/`auto-resolved` -> exactly 1 item | Mismatch (item present when none, or absent when mode != none) |
| V4 | Item position is penultimate | Item at position N.{X-1}, immediately before Update-status-to-Done at N.X | Item is last, or not in final phase, or >1 item before Done |
| V5 | Mode 1 Action contains inline skill invocation | Action contains `Skill sc:reflect-protocol` and `/sc:reflect --mode post --depth standard` | Action missing skill invocation or wrong depth |
| V6 | Mode 1 Action does NOT contain shell-out markers | Action does NOT contain `Bash`, `superclaude reflect run`, `shell`, `Run:` | Shell-out markers found in Mode 1 |
| V7 | Mode 2 Action contains Bash shell-out | Action contains `Bash` or explicit shell-execution instruction and `superclaude reflect run` | Missing Bash or missing wrapper command |
| V8 | Mode 2 Action does NOT contain inline skill invocation | Action does NOT contain `Skill`, `/sc:reflect`, `Skill sc:reflect-protocol` | Skill invocation found in Mode 2 |
| V9 | Mode 1 Action does NOT contain `--remediate` | `--remediate` absent from the reflect invocation string | `--remediate` present in Mode 1 |
| V10 | Mode 2 Action contains remediation (via wrapper) | Wrapper command present (FR-8); wrapper spec FR-9 confirms `--no-promote` default | N/A — remediation is the wrapper's responsibility; assertion is that the wrapper command is present |
| V11 | Both modes contain `reflect_post: PENDING` in HALT path | Item text instructs writing `reflect_post: PENDING` on non-pass | HALT path missing PENDING write instruction |
| V12 | Both modes contain explicit HALT/STOP instruction | Item text contains STOP or HALT language on non-pass, with prohibition on self-resolve | No HALT instruction, or self-resolve permitted |
| V13 | `{SPEC_PATH}` threading matches resolved spec | When spec_path is set, item contains `--spec {SPEC_PATH}`; when unset, no `--spec` flag | Mismatch between resolved spec and item command |
| V14 | `<BASE>` resolution instruction present | Item Action contains `<BASE>` resolution guidance (frontmatter `start_commit` or `git merge-base`) | Missing BASE resolution |

### Degraded-mode assertions (wrapper absent or subagent-executor)

| # | Assertion | Pass condition | Fail condition |
|---|-----------|---------------|----------------|
| V15 | Degraded item is byte-identical to legacy HALT | Item matches :1994–1999 exactly (after placeholder substitution) | Item differs from legacy template |
| V16 | Degraded frontmatter records degradation | `reflect_post_mode` ends with `(degraded)` | No degradation marker in frontmatter |

### rf-qa task-integrity mode integration

rf-qa's `task-integrity` mode (currently item 19 at :2108) is updated to run assertions V1–V14 (plus V15–V16 when degraded). The assertion set is parameterized by `REFLECT_POST_MODE`:

- Mode `none`: only V1, V2, V3 are active
- Mode `1`: V1–V6, V9, V11–V14 active
- Mode `2`: V1–V4, V7–V8, V10–V14 active
- Mode `1(degraded)` or `2(degraded)`: V1, V2, V15, V16 active

**Acceptance test (AT-VALIDATION-1):** A tasklist with `REFLECT_POST_MODE: 1` that contains `superclaude reflect run` in its POST item fails V6. A tasklist with `REFLECT_POST_MODE: 2` that contains `Skill sc:reflect-protocol` in its POST item fails V8. A tasklist with `REFLECT_POST_MODE: 1` that contains `--remediate` fails V9.

### Mode/item mismatch detection

Any assertion failure (V1–V16) is classified as MALFORMED. This is the mode/item mismatch check: if the emitted item's content does not match the declared mode, the tasklist is rejected.

**Acceptance test (AT-MISMATCH-1):** Intentionally swap Mode 1 and Mode 2 templates in a test tasklist. rf-qa task-integrity must catch the mismatch and return MALFORMED with the specific failing assertion number.

## 10. Flag Plumbing + Frontmatter + BUILD_REQUEST

### Parse points

1. **CLI flag**: `--reflect auto|1|2|none|0|off` parsed at A.2 (Parse & Triage) alongside `--spec`.
2. **BUILD_REQUEST file**: `REFLECT_POST_MODE: 1|2|auto|none` field in the BUILD_REQUEST block at A.9.
3. **Precedence**: explicit CLI flag > BUILD_REQUEST file field > default (2).

### BUILD_REQUEST field addition

Add to the A.9 BUILD_REQUEST schema (after `POST_REFLECT_GATE` block at :853, replacing it):

```text
REFLECT_POST_MODE: 1|2|auto|none
  [Controls which post-execution reflect gate item the builder emits as
   the penultimate item of the final phase.
   1 = inline audit (same session, --depth standard, no --remediate)
   2 = wrapper shell-out (executor-disjoint, --remediate, full Tier-2+3)
   auto = builder selects 1 or 2 per TCS+S6 FER (Section 4)
   none = suppress POST reflect item entirely
   Default: 2 (back-compat with current HALT behavior via wrapper).]
```

### Frontmatter fields

Add to the frontmatter template (:1920–1949):

```yaml
reflect_post_mode: 1|2|none|auto-resolved (N)|N(degraded)   # N = 1 or 2
reflect_post: ""   # PENDING sentinel (unchanged from :1942)
```

### Acceptance test (AT-PLUMBING-1)

Given `--reflect 1 --spec docs/spec.md`: BUILD_REQUEST contains `REFLECT_POST_MODE: 1`; frontmatter `reflect_post_mode: 1`; `spec_path: docs/spec.md`. Given no `--reflect` flag: BUILD_REQUEST contains `REFLECT_POST_MODE: 2` (default); frontmatter `reflect_post_mode: 2`.

## 11. Scope Boundaries

### IN scope
- `src/superclaude/skills/task-builder/SKILL.md`: A.2 parse, A.9 BUILD_REQUEST schema, A.10 validation checklist, per-mode emitted-item templates (replacing :1994–1999), Critical Rule 19 update, frontmatter template update
- `src/superclaude/agents/rf-qa.md` (or wherever rf-qa task-integrity assertions live): V1–V16 assertion integration
- BUILD_REQUEST schema documentation

### OUT of scope (hard non-goals)
- Building the `superclaude reflect run` wrapper (sibling spec)
- Modifying `sc-reflect-protocol` SKILL.md
- Changing the PRE reflect gate (A.10.7)
- Any `sc:cli-portify`
- Emitted items duplicating reflect logic (they invoke or shell out only)

## 12. Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Mode 1 silent Tier-2 loss (subagent executor) | Medium | High | FR-9 + V15/V16 degrade to HALT; builder detects `agent_tool_depth > 0` |
| Wrapper absent -> automation gap | Medium | Medium | Section 8 fallback to legacy HALT preserves executor-disjointness |
| Auto FER misclassifies edge case | Low | Medium | TCS+S6 are conservative: S6=1 always forces Mode 2; TCS>=35 always forces Mode 2. Only low-S6, low-TCS cases get Mode 1, which is exactly the safe zone |
| Validation checklist bloat | Low | Low | 14 assertions is more than the current single string, but each is a one-line regex/string match. rf-qa already handles larger assertion sets |
| Depth mismatch between builder and wrapper | Low | Medium | Mode 2 passes `{DEPTH}` as passthrough; wrapper never recomputes TCS (sibling FR-3). Mode 1 fixes depth, no passthrough needed |
| `auto` non-determinism | Very Low | High | FER is pure arithmetic on observable signals. No inference except the existing +/-4 TCS boundary tiebreaker (which does not affect the auto FER because TCS>=35 is far from the 13/34 boundary, and S6=1 is binary) |

## 13. Acceptance Test Matrix

| FR | Test ID | Test description | Pass criteria |
|----|---------|-----------------|---------------|
| FR-1 | AT-FR1 | Parse `--reflect 1` and `--reflect foo` | BUILD_REQUEST has `REFLECT_POST_MODE: 1`; `foo` triggers MALFORMED |
| FR-2 | AT-FR2 | BUILD_REQUEST field presence | `REFLECT_POST_MODE` present, matches resolved mode |
| FR-3 | AT-FR3 | Per-mode template emission | Mode 1 -> inline skill; Mode 2 -> Bash shell-out; penultimate position |
| FR-4 | AT-FR4 | HALT on non-pass | Item text contains PENDING write + STOP on non-pass + no self-resolve |
| FR-5 | AT-FR5 | `--spec` threading | Spec path in item Action when present; absent when not |
| FR-6 | AT-FR6 | Frontmatter `reflect_post_mode` | Field matches regex; consistent with emitted item |
| FR-7 | AT-FR7 | `--reflect none` suppresses item | No POST item; frontmatter `reflect_post: null` |
| FR-8 | AT-FR8 | Mode 2 Bash-only | Action contains Bash/shell-out; no Agent/Task/Skill |
| FR-9 | AT-FR9 | Mode 1 subagent degradation | `agent_tool_depth > 0` -> legacy HALT item |
| auto | AT-AUTO-1 | FER determinism | Two implementers agree on all three worked examples |
| knob | AT-KNOB-1 | Old->new equivalence | `POST_REFLECT_GATE: DISABLED` == `--reflect none` structurally |
| depth | AT-DEPTH-1 | O4 preservation | Mode 1 always `standard`; Mode 2 respects TCS floored at `standard` |
| wrapper | AT-WRAPPER-1 | Wrapper detection | Probe exits 0 when wrapper registered; non-zero when absent |
| fallback | AT-FALLBACK-1 | Wrapper-absent fallback | Mode 2 + absent wrapper -> legacy HALT item + `2(degraded)` |
| template | AT-TEMPLATE-1 | Mode 1/2 content divergence | Mode 1 has skill+no-shell; Mode 2 has shell+no-skill |
| validation | AT-VALIDATION-1 | Mode/item mismatch detection | Swapped templates fail V6 or V8 respectively |
| mismatch | AT-MISMATCH-1 | MALFORMED on assertion failure | Intentionally malformed tasklist fails with specific V# |
| plumbing | AT-PLUMBING-1 | Flag precedence + defaults | CLI flag > BUILD_REQUEST > default(2) |
