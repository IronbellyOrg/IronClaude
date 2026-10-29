# Invariant Probe Results

## Round 2.5: Fault-Finder Analysis

Independent fault-finder, read-only. The orchestrator re-verified INV-001 and INV-002 against real files before the resolution round. The Status column shows the state at the end of the probe; the resolution round's outcome is recorded in `debate-transcript.md`.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | Task 18's `rg -n -i 'serena\|codebase-memory\|codebase_memory' $T/fresh` searches what install wrote | UNADDRESSED | HIGH | plan:247, spec:268. rg skips hidden entries under a given root unless `--hidden` is passed. Orchestrator check: `rg -l --no-ignore -i serena .` lists 0 `/.serena/` paths, with `--hidden` it lists 2, and with the explicit root `.serena` it lists 2. So `$T/fresh/.claude/`, `.claude.json` and `.local/` are never searched, and DoD-2's check passes vacuously. |
| INV-002 | sufficiency_challenge | After the C-004, C-005 and C-012 fixes nothing under `$T/old/.claude` says `serena` | UNADDRESSED | HIGH | `install_hooks.py:293-297` copies the seeded `settings.json` to `settings.json.bak.<stamp>` (stamp `:491-494`, one-second resolution); `install_user_setup.py:81-89` does the same. The backup keeps the seeded `mcp__serena__*` matcher, and whether it survives depends on a same-second overwrite. |
| INV-003 | sufficiency_challenge | Only the three allowlisted installed files match legitimately; stale seeds get overwritten | ADDRESSED | LOW | Every installed source enumerated: `install_core.py:55,65-70`; `install_commands.py:55-61` (`copy2` under force, target `~/.claude/commands/sc`, `main.py:32`); `install_skill.py:52` copytree, so `ccsession-tag` lands at `~/.claude/skills/ccsession-tag/install.sh` (only hit `:41`); cleanup-audit protocol installs because it has no command twin (`install_skills.py:52-58`); hooks only `hooks.json:47` (Task 8); templates, rules, output-styles and `user_settings_defaults.json` have no hits. |
| INV-004 | guard_conditions | Any non-empty `CLAUDE_CONFIG_DIR` works | ADDRESSED | LOW | `install_mcp.py:731-736` reads `<dir>/.claude.json`; an empty value returns "unknown" while the stub's `${CLAUDE_CONFIG_DIR:-$HOME}` falls back to `$HOME`. Write it as `"$T/old"` etc., equal to HOME, never `$HOME/.claude`. |
| INV-005 | collection_boundaries | Spec rows list every SER-token line in the reflect refs | UNADDRESSED | MEDIUM | Not in any row's line list (source.md:229-237): `cost-profile.yaml:74` (`execute_shell_command`), `coverage-mapping.md:195` (`type_hierarchy`), `deviation-taxonomy.md:79,80,83`, `reviewer-spec.md:14,55`. `test_verify_denylist_git_mutations.py:1-67` pins the §6.1.1 "No-mutation gate." paragraph. |
| INV-006 | state_variables | The widened rubric range 124-130 can be handled as one deletion | UNADDRESSED | MEDIUM | `:124` header reword; `:126` FR-6 `onboarding_status` depends on Step 0.7, which M8 deletes (`SKILL.md:295-301`; field at `:747`, `:970`, not in G8); `:127` delete; `:128` step 3b gets the G2 Grep floor (reword); `:129` keep (G4); `:130` step 4.5 deleted (G8), so delete. |
| INV-007 | interaction_effects | The C-011 "historical `.dev/`" bullet fits the plan's own `.dev` writes | UNADDRESSED | LOW | Tasks 13-15 and 19 write new files under `.dev/codegraph-migration/handoffs/`; `git add .dev/tasks` (plan:21) also stages the Phase 2 package; a singular `handoff/` folder exists while Phase 2 reads `handoffs/`. |
| INV-008 | interaction_effects | C-002's pull-forward breaks G5's one-commit rule; C-001's fix is incomplete | ADDRESSED | LOW | G5 exempts `mcp-servers:` lists (source.md:392); all 48 files use single-line lists; Task 7's `rg -i serena` already forces the `serena:` tokens out of the `contract.py:30` comment. |
| INV-009 | guard_conditions | `git mv` into `docs/memory/reflect/` works | ADDRESSED | LOW | `docs/memory/reflect/` is absent; C-008's `mkdir -p` covers it; the moved file needs no allowlist entry. |

## Summary

- **Total findings**: 9
- **ADDRESSED**: 4 (INV-003, INV-004, INV-008, INV-009)
- **UNADDRESSED**: 5
  - HIGH: 2 (INV-001, INV-002), which block convergence
  - MEDIUM: 2 (INV-005, INV-006), a warning
  - LOW: 1 (INV-007)

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002
Action taken: a resolution round with both advocates (see `debate-transcript.md`, "Invariant-gate resolution").
