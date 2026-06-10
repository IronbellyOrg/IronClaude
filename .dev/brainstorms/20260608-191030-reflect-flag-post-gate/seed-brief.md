---
topic: "Design the spec for a task-builder skill refactor that adds a --reflect auto|1|2 flag (default 2) controlling WHICH post-execution reflect gate item the builder emits into the generated tasklist's final phase, replacing today's single always-HALT POST item with a 3-mode quality/cost dial."
domain: code
strategy: systematic
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-06-08T19:10:30Z
source_brief: .dev/handoffs/task-builder-reflect-flag-brief.md
sibling_spec: .dev/brainstorms/20260608-182553-reflect-cli-wrapper/merged-requirements.md
---

# Seed Brief: task-builder `--reflect auto|1|2` POST-gate refactor

## Problem Statement

`task-builder/SKILL.md` currently emits ONE fixed post-execution reflect gate item
(SKILL.md:1994–1999): the HALT/fresh-session design — write `reflect_post: PENDING`,
STOP, operator runs `/sc:reflect --mode post --remediate …` manually in a new session.
That item is correct on the property that matters (executor-disjoint review) but is
fully manual and one-size-fits-all: every tasklist, trivial or cross-subsystem, gets the
same heavyweight `--depth deep --remediate` fresh-session ceremony.

We want a `--reflect auto|1|2` dial (**default 2**) that picks the POST gate item's
*form* and *rigor* at build time, turning a single always-HALT item into a 3-mode
quality/cost trade. The spec must be implementable such that two implementers compute
the same emitted item from the same BUILD_REQUEST.

## Known Context (verified — see enrichment/codebase-context.md)

- **Current POST item already bakes `--remediate --depth {DEPTH}`** (SKILL.md:1996). The refactor
  ADDS a lighter Mode 1 and AUTOMATES Mode 2 (via the sibling wrapper); it does not introduce
  remediation from scratch.
- **PRE/POST asymmetry**: PRE gate (A.10.7) runs *inside the builder* via Agent/Task; POST is a
  *templated item the `/task` executor runs later*. `--reflect` governs only the POST template.
- **Sibling wrapper spec is already merged** (convergence 0.82): `superclaude reflect run` is a
  top-level `claude --print` subprocess (escapes the Agent-tool nesting limit so Tier-2 fans out),
  with a 4-state fail-closed verdict `{pass, halted, degraded, blocked}` and a proposed
  `POST_REFLECT_MODE: wrapper|halt` BUILD_REQUEST field.
- **THREE overlapping knobs** must reconcile into one coherent surface: `POST_REFLECT_GATE: ENABLED`
  (on/off, :853), the sibling's `POST_REFLECT_MODE: wrapper|halt`, and the new `--reflect auto|1|2`.
- **TCS depth machinery** (:2114+) already derives POST `--depth` (O4: POST never `quick`).

## The three modes (caller-specified — FIXED requirements)

- **`--reflect 1`** — emit a final-phase item that runs `/sc:reflect --mode post --depth standard`
  INLINE in the SAME session as the `/task` executor (top-level skill invocation by the executor;
  NOT Agent/Task, NOT shell-out). Lightweight/faster/cheaper, **audit-only (no `--remediate`)**, but
  **NOT executor-disjoint** (shares the executor's representational frame).
- **`--reflect 2`** (DEFAULT) — emit a final-phase item that Bash-shells the thin CLI wrapper
  (`superclaude reflect run`) to run reflect `--depth deep --remediate` as a top-level subprocess:
  executor-disjoint, full Tier-2 + Tier-3 remediation chain.
- **`--reflect auto`** — builder deterministically selects 1 or 2 (selection rule = open question 1).

## Constraints

- SoT discipline: edit `src/superclaude/` → `make sync-dev`; never stage `.claude/` mirrors.
- Back-compat + reversibility: default 2; clean old→new map for `POST_REFLECT_GATE`/HALT behavior.
- No reflect-logic duplication in emitted items (invoke/shell-out only).
- Every emitted item HALTs on non-pass and writes `reflect_post` back (`feedback_human_decision_items_must_halt`).
- Nesting boundary: Mode 2 = Bash shell-out (never Agent/Task); Mode 1 = inline `/sc:reflect` by a
  TOP-LEVEL executor only (`reference_subagent_cannot_nest_skill_fanout`).

## Success Criteria (desired output)

`merged-requirements.md` — a unified spec covering: flag semantics + precedence + default(2);
the 3 emitted-item templates (Action/Output/Verification/Completion-gate text for 1, 2, auto-resolved);
the `auto` FER (deterministic 1-vs-2); the `POST_REFLECT_GATE` reconciliation + old→new map (incl. a
disabled/`none` mode and the retained-HALT question, and folding in `POST_REFLECT_MODE: wrapper|halt`);
depth/TCS reconciliation (mode-fixes-depth vs auto-uses-TCS; fate of O4); wrapper-dependency fallback
(absent wrapper → HALT? Option 1? STOP?); validation item 19 / :2051 + rf-qa updates asserting
item-matches-mode; frontmatter field (`reflect_post_mode`) + BUILD_REQUEST plumbing. Ready to feed
`sc:tasklist` or `sc:implement`. STOP at merged requirements (`--handoff none`).

## Open Questions (the 10 the debate must resolve)

1. **`auto` selection FER** — deterministic 1-vs-2 rule (TCS band? frontmatter risk/refactor-class S6?
   wrapper-availability?). Two implementers must compute the same choice.
2. **Reconciliation with `POST_REFLECT_GATE`** — does `--reflect` subsume the ENABLED switch? Is there
   `--reflect none|0` (disabled)? A retained manual-HALT mode? Map old→new explicitly. Fold in the
   sibling's `POST_REFLECT_MODE: wrapper|halt` (so Mode 2 == wrapper)?
3. **Depth vs TCS** — modes fix depth (1=standard, 2=deep). Does the mode OVERRIDE TCS-derived POST
   depth, or does `auto` USE TCS to pick the mode (and inherit its depth)? Fate of override O4?
4. **Executor-disjointness trade-off (Mode 1)** — specify exactly what Mode 1 sacrifices vs Mode 2
   (anti-self-confirmation executor-exclusion weakened; Tier-2 reviewers still heterogeneous); document
   when Mode 1 is acceptable (low-complexity/low-risk).
5. **Mode 2 wrapper dependency + fallback** — wrapper absent → degrade to HALT (current)? to Mode 1?
   STOP at build time? Builder must detect/validate availability.
6. **`--remediate` scope** — confirm Mode 1 = audit-only, Mode 2 = `--remediate`. Define what the emitted
   item's completion-gate does when remediation surfaces a Tier-3 task (HALT + route to Open Questions;
   never auto-execute).
7. **Per-mode emitted-item template** — exact Action/Output/Verification/Completion-gate text for 1, 2,
   auto-resolved. Each HALTs on non-pass + writes `reflect_post`. Mode 2 = Bash shell-out; Mode 1 = inline.
8. **Mode 1 same-session mechanics + nesting boundary** — how a tasklist *item* makes the `/task` executor
   run `/sc:reflect` inline and capture the verdict into `reflect_post`. Executor top-level → reflect's
   Tier-2 fan-out is the one allowed nesting level; if the executor is itself a subagent, Mode 1 silently
   loses Tier 2 — specify detection/disallow.
9. **Validation (rf-qa) updates** — item 19 / :2051 + rf-qa task-integrity must assert the emitted item
   MATCHES the selected mode (inline vs shell-out command shape; penultimate; `reflect_post` sentinel).
   Mode/item mismatch = MALFORMED.
10. **Flag plumbing + frontmatter** — where `--reflect` is parsed (CLI flag + BUILD_REQUEST field), its
    precedence order, default (2), and the frontmatter field it writes (`reflect_post_mode: 1|2|auto-resolved`).

## Scope

**IN:** task-builder `SKILL.md` (flag parse, A.9 gate logic, per-mode POST item template, the `auto` FER,
`POST_REFLECT_GATE` reconciliation, Reflect-Depth reconciliation, validation-checklist + rf-qa updates,
frontmatter field); BUILD_REQUEST schema; rf-qa checks; MDTM templates if the emitted item shape requires it.

**OUT (hard non-goals):** building the thin wrapper (sibling spec); modifying `sc-reflect-protocol`;
changing the PRE gate; any `sc:cli-portify`. Emitted items only invoke reflect (inline, Mode 1) or shell out
to the wrapper (Mode 2) — never duplicate reflect logic.
