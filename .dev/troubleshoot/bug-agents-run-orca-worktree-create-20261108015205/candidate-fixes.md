# Candidate fixes (Wave 3 step 4)

Shared diagnosis (all four cards, calibrated 0.67 / 0.58 / 0.67 / 0.50): a bare `orca worktree create` makes Orca open a plain first terminal (P1), and no instruction says what to do with it. All cards cite P1 and behaviour-definition row 1 and assert the same mechanism, so no split-pending cluster (Wave 3 step 4.5 does not apply).

| # | Fix | Supporting cards (calibrated) | Verdict |
|---|---|---|---|
| fix-1 | Installed core rule (src/superclaude/core/CLAUDE.md + ccsession-tag/README.md), own-use close with `--all` right after create, hand-off → `worktree create --agent`; reinstall | root-cause-analyst T2 (0.58); tier1 (0.67) proposed the same location plus a project bullet | competing |
| fix-2 | Both installed copies + project bullet; list terminals then close the one seeded handle with `--terminal`; never `--all`; never in a worktree you did not just create | quality-engineer T2 (0.67) | competing |
| fix-3 | Project CLAUDE.md only (bullet after :310 + example), `--all` before anything is started there | system-architect T2 (0.50) | competing |

Differences are fix location (installed core vs project) and closing command (`--all` vs single handle). Same diagnosis, different fix mechanism → Wave 4 `/sc:adversarial --compare` at `--depth quick`.

Facts the debate must weigh (tier1-observation.md): N12 (creates span IronClaude, Coder, IronOrca; installed ~/.claude/CLAUDE.md lacks the section), N13 (rule added 2026-11-06, after the hand-off creates; create reply carries no seeded handle; create awaits terminal startup), N3 (`--all` stops every terminal in the workspace), QE calibration note (fix-2 wording "Never use `--all`" contradicts its own `"--all" not in section` test).
