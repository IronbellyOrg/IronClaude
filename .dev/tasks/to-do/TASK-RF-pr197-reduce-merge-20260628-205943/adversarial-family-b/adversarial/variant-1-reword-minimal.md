# Variant A — Reword minimal Family-B descriptive claims

## Position

The tasklist should instruct the executor to reword only the stale **descriptive** Family-B claims in `src/superclaude/skills/task-builder/SKILL.md` while preserving PRE/skill-mode **behavior**.

## Exact scope

- Flip Family A / CLI POST cluster to executor-class exclusion as already researched by R3.
- Preserve A.10.7 PRE action: do not pass `--executor-model` at PRE because no executor exists yet.
- Preserve skill-mode behavior if it intentionally does not forward an executor class.
- Reword only blanket descriptive assertions that become false after Step 3 restores `sc-reflect-protocol` to executor-class exclusion:
  - line 1678-style: "The skill no longer excludes any model class in any case..."
  - line 2223–2224-style: "the skill no longer excludes any model class from its reviewer panel..."
  - line 2371-style: "the skill no longer excludes any model class..."

## Rationale

Correctness wins: after Step 3, `sc-reflect-protocol` is executor-class excluding again. Leaving prose that says it never excludes any model class ships a known contradiction. The PRE action remains orthogonal; only its blanket explanatory prose is stale.

## Guardrails

- Do not change PRE command semantics.
- Do not add `--executor-model` to PRE.
- Do not alter EV-3/EV-4 / reflect_post_mode / CLI_MODE machinery except the already-required exclusion wording.
- Keep changes content-anchored, not line-number hardcoded.
- Validate with greps proving no blanket "skill no longer excludes any model class" claims remain in `task-builder/SKILL.md` after Step 4.
