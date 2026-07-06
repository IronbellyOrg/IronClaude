# HD-1 — Default POST-reflect mode resolution

**STATUS: PENDING — awaiting RyanW (maintainer design decision)**

## The question

PR #197's `task-builder` skill ships the **skill-only POST-reflect gate as the DEFAULT**
(`reflect_post_mode: skill`, i.e. `--cli` absent). That default's executor-independence
guarantee rests on nested Skill-tool fan-out from a dedicated subagent — a path the PR body
itself admits is "NOT yet validated end-to-end," and which project memory
`reference_subagent_cannot_nest_skill_fanout` records degrading to a hand-rolled fixture.

**What was applied by this task (R2a, unconditional, already done):** an in-SKILL disclosure
at the `#6 --cli` definition and on Rule 20's default arm, plus softening of all three bare
"capability are confirmed" assertions to "expected … not yet session-validated." The
`--cli` wrapper path remains the validated one.

**What is HALTED (this decision):** whether to change the DEFAULT behavior. This is RyanW's
call and was NOT auto-resolved.

## Options (choose one)

- **(i) Keep skill-mode default + cite a validating run.** Keep `reflect_post_mode: skill` as
  default; attach a concrete validating run id / artifact proving nested Skill-tool fan-out
  works from an Agent-tool subagent, and restore firmer wording at the three sites.
  *Follow-up:* run a real end-to-end skill-mode POST on a throwaway tasklist, capture the
  run_id + reviewer-cards artifacts, cite them in SKILL.md.

- **(ii) Invert the default to `--cli`.** Make the validated wrapper path the default; skill-mode
  becomes an opt-in flag (e.g. `--skill-post` / `--experimental-skill-post`) until nesting is
  re-proven. *Follow-up:* flip the `#6` default + `reflect_post_mode` resolution order + Rule 20
  "(default)" labels + the O4 depth-floor default (O4 CLI=deep vs skill=standard) + the
  validation-checklist default branch. **This is a multi-site behavioral change — NOT applied here.**

- **(iii) Keep skill default, mark EXPERIMENTAL.** Leave the default as-is with the R2a disclosure
  as the only guard, explicitly labeling the skill-mode POST path EXPERIMENTAL.
  *Follow-up:* add an `EXPERIMENTAL` tag at the `#6` definition + Rule 20 default arm.

## Guarantees of this HALT

- **NO default was flipped.** `--cli` remains `default OFF`; `reflect_post_mode: skill` remains
  the default. Verified: `grep "default OFF"` + "Default (flag absent) = skill-only mode" unchanged.
- **NO O4 depth floor was edited.** The O4 CLI=deep / skill=standard rule is untouched.
- The only R2 change applied to `SKILL.md` is the R2a disclosure + softening (Steps 4.1–4.2).

## Resolution

When RyanW picks (i) / (ii) / (iii), apply the named follow-up as a separate change. Until then,
this item is the correct terminal state — it does NOT block marking the mechanical task Done.
