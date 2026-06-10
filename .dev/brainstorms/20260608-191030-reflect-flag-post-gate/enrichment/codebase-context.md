# Codebase Context — task-builder `--reflect auto|1|2` POST-gate refactor

> Enrichment source: direct Read of cited surfaces (quality_tier: primary). All
> file:line anchors verified 2026-06-08 against
> `src/superclaude/skills/task-builder/SKILL.md` and the sibling wrapper spec.

## Surface map (verified anchors)

| Surface | Anchor | Current behavior |
|---|---|---|
| `POST_REFLECT_GATE` BUILD_REQUEST field | SKILL.md:853 | `ENABLED` binary switch + sub-fields `SPEC_PATH`, `DEPTH: max(tcs, standard)`, `TASK_FILE`. On/off only — no mode dial. |
| `reflect_post` frontmatter sentinel | SKILL.md:1942 | `reflect_post: ""` PENDING sentinel; operator records `{verdict, run_id, report}` in a fresh session. |
| Current POST item (HALT/fresh-session) | SKILL.md:1994–1999 | Penultimate item. **Action already bakes `/sc:reflect --mode post --remediate --diff <BASE>..HEAD --tasklist {TASK_FILE} [--spec {SPEC_PATH}] --depth {DEPTH} --executor-model {EXECUTOR_CLASS}`** for a NEW session. Writes `reflect_post: PENDING`, STOPs, does NOT self-resolve. Completion-gate: operator runs reflect in fresh session, records verdict, only THEN Update-status-to-Done proceeds (HALT per `feedback_human_decision_items_must_halt`). |
| Present-and-penultimate validation assertion | SKILL.md:2051 | "POST reflect item present and positioned penultimate … when POST_REFLECT_GATE is ENABLED — MALFORMED if omitted." |
| Validation checklist item 19 | SKILL.md:2108 | Asserts: emitted when `POST_REFLECT_GATE: ENABLED`; penultimate; NOT inline in executor's biased context; writes `reflect_post: PENDING`; HALTs; uses `/sc:reflect` (gate) + `/task` (re-exec, never `/sc:task`). Omission = MALFORMED. |
| Reflect Depth (Deterministic TCS) | SKILL.md:2114–2155 | TCS = 3·S1+4·S2+2·S3+2·S4+5·S5+4·S6. Bands: ≤12 quick / 13–34 standard / ≥35 deep. Overrides: **O1** S5>0→floor standard; **O2** S6=1→force deep; **O3** item-count>40 (single-track>50)→floor standard; **O4** POST never `quick` (floor standard). ±4 boundary tiebreaker only. |
| `--spec` threading | SKILL.md:41 | Resolved explicit→@file→BUILD_REQUEST field→none; written to frontmatter `spec_path:`; baked into POST item command + PRE gate. |
| PRE reflect gate (A.10.7) | SKILL.md:1409–1429 | **Builder-time** gate: `Skill sc:reflect-protocol` via Agent/Task, default subagent model, advisory-blocking, `quick` permitted at PRE (no diff yet). NOT a templated item. **OUT of scope to change** but `--reflect` naming must not collide. |

## The asymmetry that shapes the design

- **PRE gate** = runs *inside the builder* (Agent/Task subagent spawn of reflect) at build time. Advisory. Already nests one allowed level (builder is top-level → reflect's Tier-2 fan-out works).
- **POST gate** = a *templated item* the builder writes into the tasklist's final phase; the **`/task` executor** runs it *later*. The `--reflect` flag changes ONLY this POST template's form + rigor.

This asymmetry is why Option 1 (inline same-session) has a nesting hazard the PRE gate does not: if the `/task` executor is itself ever an Agent-tool subagent, an inline `/sc:reflect` loses Tier-2 fan-out (`reference_subagent_cannot_nest_skill_fanout`). The PRE gate is immune because the builder is reliably top-level.

## Sibling wrapper spec (Option 2's target) — already merged, convergence 0.82

`.dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md` specifies
`superclaude reflect run <tasklist>`:

- **FR-1/FR-10**: top-level `claude --print` subprocess via `ClaudeProcess` (NOT Agent-tool, NOT `HomeIsolation`) — the sole reason Tier-2 fan-out succeeds; inherits real env (MCP + `ANTHROPIC_DEFAULT_*` aliases).
- **FR-3 passthrough**: builder bakes `--depth`(TCS, floored standard) + `<BASE>`; wrapper is passthrough → **single TCS producer**, no builder/wrapper drift.
- **FR-5/FR-8 verdict**: 4-state `{pass, halted, degraded, blocked}`; only `pass` exits 0; everything else HALTs. Fail-closed.
- **FR-9**: default `--no-promote` (audit-only as a *hard* prompt flag); `--promote` opt-in delegates to reflect's gated Wave 7.
- **FR-11 degradation detection**: stricter than reflect's interactive fail-open — HALTs on lost Tier-2 grounding/diversity/adversarial-merge.
- **§7 Q7 template hook**: proposes `POST_REFLECT_MODE: wrapper|halt` (default `halt`) in BUILD_REQUEST; when `wrapper`, Phase-N Action shells `superclaude reflect run {TASK_FILE}` (Bash); HALT text byte-identical when unset.
- **NFR-7 no-nesting guard**: item invokes wrapper as **Bash shell-out**, never Agent/Task.

**Critical reconciliation flag**: the wrapper spec already proposes a `POST_REFLECT_MODE: wrapper|halt` field. The `--reflect auto|1|2` flag MUST explicitly reconcile with BOTH `POST_REFLECT_GATE: ENABLED` (the on/off switch) AND `POST_REFLECT_MODE: wrapper|halt` (the sibling's mode field) — three overlapping knobs that must collapse into one coherent surface, or the BUILD_REQUEST schema fragments.

## Anchors the design must touch (IN scope)

1. BUILD_REQUEST schema: `POST_REFLECT_GATE` (A.9 / :853) + new `--reflect` flag + frontmatter field.
2. Per-mode POST item template (replaces :1994–1999) — three shapes (inline / shell-out / auto-resolved).
3. The `auto` FER (deterministic 1-vs-2 selection — open question 1).
4. Reflect-Depth/TCS reconciliation (:2114+) — O4 floor, mode-fixes-depth vs auto-uses-TCS (open question 3).
5. Validation item 19 (:2108) + present-and-penultimate (:2051) — must assert the emitted item MATCHES the selected mode (open question 9).
6. `reflect_post` sentinel (:1942) + new `reflect_post_mode` frontmatter field (open question 10).
7. `--spec` threading preservation (:41).

## Constraints (from brief + project memory)

- SoT: edit `src/superclaude/` → `make sync-dev`; never stage `.claude/` (CLAUDE.md ABSOLUTE RULE).
- Back-compat: default 2; clean old→new map for `POST_REFLECT_GATE`/HALT.
- No reflect-logic duplication in emitted items — they only *invoke* (inline) or *shell out to* the wrapper.
- Human-decision HALT: every emitted item HALTs on non-pass + writes `reflect_post` back (`feedback_human_decision_items_must_halt`).
- Nesting: Option 2 = Bash shell-out (never Agent/Task); Option 1 = inline `/sc:reflect` by a top-level executor only (`reference_subagent_cannot_nest_skill_fanout`).
