# Tier 1 observation

Captured 2026-11-02T19:06:24Z by the orchestrator (static read; no command executed against a user install).

## Grounding (Read/Grep floor; auggie MCP tools not listed in this session, codegraph index_state: not_initialized for this worktree)

- docs/releases/v5.0.0.md:146-147 instruct `pipx install --force git+https://github.com/IronbellyOrg/IronClaude` then `superclaude update`.
- docs/releases/v5.0.0.md:150 says "From a clone, `./update.sh` does the same".
- docs/releases/v5.0.0.md:3 (front-matter description) says "Upgrade with superclaude update."
- docs/releases/v5.0.0.md:69 (Impact) says "An upgrade needs `superclaude update` (not a plain `superclaude install`)".
- src/superclaude/cli/main.py:340-429 `update()` calls install_core_files, install_commands, install_agents, install_all_skills, wire_ccsession, install_hooks, install_templates, install_user_setup (all force=True, lines 365-404); line 407 comment "Read-only: update never touches MCP registrations."; lines 408-415 only print update_notice().
- src/superclaude/cli/main.py:242-253 `install()` runs install_codegraph_mcp(scope="user"); :257-267 runs run_retire_step(codegraph_success and codegraph_ready()[0]).
- update.sh:7-8 run `pipx install --force ./` then `superclaude install --force`.
- src/superclaude/hooks/scripts/codegraph-session-start.sh:15-19 exit 0 when no codegraph binary is found; it only starts `codegraph init` (lines 1-4).
- docs/user-guide/mcp-installation.md:70 already documents: "`superclaude update` ... never touches MCP registrations; it only prints a notice telling you to run `superclaude install`".

## Reproduction

No repro run: the defect is documentation text contradicting code; reading both is the observation. Running an upgrade would mutate ~/.claude and is outside a read-only diagnosis.

## Related (out of scope for this finding, logged for follow-up)

- docs/getting-started/installation.md:56, :329, :333 also tell upgraders to run `superclaude update`; for a pre-codegraph install that also skips the codegraph and retire phases.

## Runtime evidence (parent-collected 2026-11-02T19:14:22Z)

Command (Bash diagnostics envelope: fixed template, first token uv, timeout 120s, cwd worktree root, read-only): `timeout 120 uv run pytest tests/cli/test_update_command.py -q -p no:cacheprovider -k codegraph`
Run: local, arm: release-v5.0.0 worktree at c0270283. Output: "9 passed, 11 deselected in 0.46s". Includes test_update_never_runs_the_codegraph_phase (tests/cli/test_update_command.py:329-333) and test_install_force_is_not_forwarded_to_codegraph (:318-326).

## Behaviour definitions

Row 1: src/superclaude/cli/main.py:340-429 (update) and :242-267 (install codegraph + retire), read directly this run; source coordinates as cited.
