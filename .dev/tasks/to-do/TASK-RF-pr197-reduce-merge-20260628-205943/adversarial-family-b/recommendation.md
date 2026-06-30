# Family-B Prose Decision — Adversarial Recommendation (RESOLVED)

**Date:** 2026-06-28
**Method:** sc:adversarial Mode A — 3 variants, 3 advocates (steelman), 1 neutral judge.
**Decision authority:** User explicitly requested the adversarial debate and to "move forward with Variant A."

## WINNER: Variant A — minimal Family-B descriptive reword (judge confidence 0.87)

Scores (judge, 1–5 per axis):

| Variant | Correctness | Scope discipline | Over-edit risk control | Executability | Total |
|---------|-------------|------------------|------------------------|---------------|-------|
| **A — minimal Family-B descriptive reword** | 5 | 4 | 4 | 5 | **18/20** |
| B — leave + document/gate | 3 | 5 | 5 | 3 | 16/20 |
| C — CLI-only, ignore Family-B | 1 | 4 | 5 | 2 | 12/20 |

## Rationale

Once Step 3 restores `sc-reflect-protocol/SKILL.md` to master's **executor-class EXCLUSION** model, the Family-B blanket descriptive claims in `task-builder/SKILL.md` — "the skill no longer excludes any model class in any case", "reviewer-panel independence is guaranteed at the instance level" (as a *global* claim about the reflect skill) — become **factually false**. Variant C ships that contradiction silently (fails shared-assumption A-003). Variant B preserves it but gates on a human halt; the judge found the halt **unnecessary now** because the user's explicit adversarial-advice request supplies the decision surface. Variant A is the smallest edit that makes the prose truthful **without changing behavior**.

## What Variant A changes vs preserves

**CHANGE (truthfulness only):** reword the blanket descriptive claims in Family B (the A.10.7 PRE rationale prose + skill-mode runner prompt + Rule 20 skill-arm disclosure) so they no longer assert a *global* "reflect never class-excludes / instance-level-only" property. Re-anchor each to its **path-specific** reason:
- PRE: "do NOT pass `--executor-model` at PRE **because no executor has run yet** (no executor class exists to forward)" — NOT "because the skill no longer excludes any class".
- skill-mode runner / Rule 20: phrase as the skill-mode arm's own behavior, not a blanket claim that the reflect skill is non-excluding.

**PRESERVE (behavior — DO NOT change):**
- PRE action: still no `--executor-model` at PRE.
- skill-mode runner architecture / invocation mechanics.
- EV-3/EV-4 on-disk verification machinery.
- `reflect_post_mode` / `--cli` / `CLI_MODE` mechanics.
- Family A / CLI POST cluster flip (the primary Step-4 edit) lands as R3 specified.

## Exact guardrails to encode in the Step-4 tasklist item

1. Edit target is ONLY `src/superclaude/skills/task-builder/SKILL.md`.
2. Preserve PRE behavior: no `--executor-model` at PRE; keep the "no executor has run yet" rationale.
3. Do NOT make skill-mode forward an executor class; do not change skill-mode/PRE invocation architecture.
4. Reword ONLY blanket descriptive claims equivalent to "the skill no longer excludes any model class" / global "instance-level independence" — re-anchor to path-specific reasons. Do NOT rewrite broad sections for style.
5. Keep Family A CLI POST flip intact (R3 Task-3 rewordings) — clause 5 may name `executor_class_resolved`/`executor_exclusion_degraded` ONLY because Step 3 restores those reflect-contract fields.
6. Do NOT touch EV-3/EV-4, `reflect_post_mode`, `--cli`, `CLI_MODE`, TCS, rf-* gates except the required polarity wording.
7. Content-anchored edits (locate by exact stale phrase / note heading), NOT hardcoded line numbers.
8. Validation:
   - Positive: CLI POST note now contains executor-class-exclusion wording (`grep "canonical executor-class-exclusion model"`).
   - Negative (Family A): the CLI POST note body no longer contains "instance-level independence".
   - Negative (Family B blanket-claim sweep): `grep -c "no longer excludes any model class" src/superclaude/skills/task-builder/SKILL.md` → expect `0` after the reword.
   - PRE behavior preserved: a PRE instruction still says do-not-pass-`--executor-model` and its rationale is "no executor has run", not "skill never excludes".
   - `make sync-dev` then `make verify-sync`.

## Invariants that would INVALIDATE Variant A (halt + escalate if any are true)

1. Step 3 does NOT actually restore reflect to executor-class exclusion (then Family-B instance-level prose may not be false → A's premise collapses).
2. The edit adds `--executor-model` to PRE or otherwise changes PRE/skill-mode behavior (→ became A-wide, over-edit).
3. The edit broadens into a full Family-B behavioral rewrite rather than surgical truthfulness fix.
4. Post-edit validation cannot prove the blanket stale claims are gone.

## Artifacts

- Variants: `adversarial/variant-{1,2,3}-*.md`
- Diff analysis: `adversarial/diff-analysis.md`
- Advocate transcripts + judge: captured in the task-builder orchestration log (this recommendation is the merged base-selection).
