# Tasklist: workflow v3 (from SPEC.md)

Walk with `/sc:implement` in order. AC = SPEC.md.

- [ ] T1 Rewrite `src/superclaude/commands/workflow.md` thin command + Activation (SPEC §3)
- [ ] T2 Add `src/superclaude/skills/sc-workflow-protocol/SKILL.md` waves 0–4 (SPEC §4)
- [ ] T3 Add five refs (SPEC §2)
- [ ] T4 Pytest: Activation, refs exist, no Execute step (SPEC §8)
- [ ] T5 `make sync-dev` (do not stage `.claude/` mirrors)

Done when T4 passes and T5 verify-sync is clean.
