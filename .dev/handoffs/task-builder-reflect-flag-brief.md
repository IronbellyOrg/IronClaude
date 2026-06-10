# Brainstorm brief — task-builder `--reflect auto|1|2` POST-gate refactor

Design the spec for a task-builder skill refactor that adds a `--reflect auto|1|2` flag (**default 2**) controlling WHICH post-execution reflect gate item the builder emits into the generated tasklist's final phase. This replaces today's single always-HALT POST item with a 3-mode quality/cost dial.

## Problem / goal

task-builder currently emits one fixed POST reflect gate (the HALT/fresh-session design: write `reflect_post: PENDING`, STOP, operator runs `/sc:reflect` manually in a new session). We want a `--reflect` dial that picks the POST gate's *form* and *rigor* at build time.

## The three modes (caller-specified — treat as fixed requirements)

- **`--reflect 1`** — the builder emits a final-phase item that runs `/sc:reflect --mode post --depth standard` **in the SAME session as the `/task` executor** that executed the tasklist (inline `/sc:reflect` skill invocation by the executor; top-level within the executor session; NOT an Agent-tool subagent, NOT a shell-out). Lightweight / faster / cheaper, **audit-only (no `--remediate`)**, but **NOT executor-disjoint** — it shares the executor's conversation/representational frame.
- **`--reflect 2`** (DEFAULT) — the builder emits a final-phase item that invokes a **bash/shell session executing the thin CLI reflect wrapper** (`superclaude reflect run`, per the sibling spec) to run reflect **`--depth deep --remediate`** — a top-level subprocess: executor-disjoint, full Tier 2 + Tier-3 remediation chain.
- **`--reflect auto`** — the builder deterministically selects 1 or 2 (the selection rule is an open question to resolve).

## Existing surfaces to REFACTOR (cite these; do NOT reinvent)

All in `src/superclaude/skills/task-builder/SKILL.md`:
- A.9 `POST_REFLECT_GATE: ENABLED` BUILD_REQUEST field (SKILL.md:853) — the current on/off switch.
- The current POST item = HALT/fresh-session design (SKILL.md:1996-1999); `reflect_post: ""`/PENDING frontmatter sentinel (:1942).
- Validation: checklist item 19 (:2108) "POST reflect gate in generated task files" + present-and-penultimate assertion (:2051) — both currently assert the HALT item.
- `## Reflect Depth (Deterministic TCS)` (:2114+) — currently derives POST `--depth` (floored at `standard`, override O4: POST never `quick`).
- `--spec` threading (:41) — baked into the POST item command; preserve.
- A.10.7 PRE reflect gate (:1409+) — OUT of scope to change, but `--reflect` naming/semantics must not collide with the PRE gate.
- Sibling thin-wrapper spec (Option 2's target): `.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md` — Option 2's emitted item shells `superclaude reflect run`.

## Open questions for the brainstorm to resolve

1. **`auto` selection FER.** A deterministic frozen-extraction rule for picking 1 vs 2: TCS band (low→1, medium/high→2)? frontmatter risk/refactor-class → 2? wrapper-availability? Define it so two implementers compute the same choice.
2. **Reconciliation with `POST_REFLECT_GATE`.** Does `--reflect` subsume the existing ENABLED/disabled field? Is there a `--reflect none`/`0` (disabled) and/or a retained HALT mode (today's manual fresh-session)? Map old→new explicitly. Does `--reflect` also fold in the wrapper-brainstorm's proposed `POST_REFLECT_MODE: wrapper|halt` (so Option 2 == wrapper)?
3. **Depth vs TCS.** Modes fix depth (1=standard, 2=deep). Does the mode OVERRIDE the TCS-derived POST depth, or does `auto` USE the TCS to pick the mode (and inherit its depth)? What becomes of override O4 (POST never `quick`)?
4. **Executor-disjointness trade-off (Option 1).** Same-session reflect is NOT executor-disjoint (shares the executor's context frame; reflect's anti-self-confirmation executor-exclusion is weakened even though Tier-2 reviewers are still heterogeneous models). Specify exactly what Option 1 sacrifices vs Option 2, and document when Option 1 is acceptable (low-complexity/low-risk).
5. **Option 2 wrapper dependency + fallback.** Option 2 requires the thin wrapper installed (`superclaude reflect run`). Fallback when absent: degrade to HALT (current behavior)? to Option 1? STOP at build time with a clear message? The builder should detect/validate availability.
6. **`--remediate` scope.** Option 2 = `--remediate` (Tier-3 chain). Confirm Option 1 = audit-only. Define what the emitted item's completion-gate does when remediation surfaces a Tier-3 task (HALT + route to Open Questions; never auto-execute).
7. **Per-mode emitted item template.** The exact Action / Output / Verification / Completion-gate text the builder writes for 1, for 2, and for auto's resolved mode. Each MUST HALT on non-pass (`feedback_human_decision_items_must_halt`) and write `reflect_post` back. Option 2 = Bash shell-out to the wrapper (never Agent/Task — the nesting limit, memory `reference_subagent_cannot_nest_skill_fanout`); Option 1 = inline `/sc:reflect` invocation by the executor.
8. **Option 1 same-session mechanics + nesting boundary.** How does a tasklist *item* make the `/task` executor run `/sc:reflect` inline and capture the verdict into `reflect_post`? The executor is top-level, so reflect's Tier-2 fan-out is one allowed nesting level — BUT if the `/task` executor is itself ever a subagent, Option 1 silently loses Tier 2. Specify detection / disallow.
9. **Validation (rf-qa) updates.** Update SKILL.md validation item 19 / :2051 and the rf-qa task-integrity checks so they assert the emitted item MATCHES the selected `--reflect` mode (inline vs shell-out command shape; penultimate position; `reflect_post` sentinel present). A mode/item mismatch = MALFORMED output.
10. **Flag plumbing + frontmatter.** Where `--reflect` is parsed (CLI flag + BUILD_REQUEST field), its precedence order, default (2), and the tasklist frontmatter field it writes (e.g. `reflect_post_mode: 1|2|auto-resolved`).

## Scope

**IN:** task-builder `SKILL.md` (flag parse, A.9 gate logic, per-mode POST item template, the `auto` FER, reconciliation with `POST_REFLECT_GATE`, Reflect-Depth reconciliation, validation-checklist + rf-qa updates, frontmatter field); the BUILD_REQUEST schema; rf-qa checks; MDTM templates if the emitted item shape requires it.

**OUT (hard non-goals):** building the thin wrapper itself (sibling spec); modifying the `sc-reflect-protocol` skill; changing the PRE gate; any `sc:cli-portify`. The emitted items only *invoke* reflect (inline, Option 1) or *shell out to the wrapper* (Option 2) — they never duplicate reflect logic.

## Constraints

- SoT discipline: edit `src/superclaude/` → `make sync-dev` → `.claude/`; never stage `.claude/` mirrors (CLAUDE.md ABSOLUTE RULE).
- Back-compat + reversibility: default 2; provide a clean old→new mapping for the current `POST_REFLECT_GATE`/HALT behavior.
- No reflect-logic duplication in the generated items.

## Desired output

`merged-requirements.md` — a unified spec for the `--reflect auto|1|2` task-builder refactor (flag semantics, the 3 emitted-item templates, the `auto` FER, the `POST_REFLECT_GATE` reconciliation + old→new map, depth/TCS reconciliation, wrapper-fallback, validation/rf-qa changes, frontmatter + BUILD_REQUEST plumbing), ready to feed `sc:tasklist` or `sc:implement`. Stop at merged requirements (`--handoff none`).
