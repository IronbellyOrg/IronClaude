# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent agent (opus), read-only. Upstream refs are files in `/tmp/ponytail-src-t14b/` (Ponytail v5.3.3, main 96608e07). Orchestrator re-verified INV-001 (`hooks_claude-codex-hooks.json:5` matcher `startup|resume|clear|compact`; `mode-tracker.js:143-148` sends only the header on Claude Code) and INV-003 (`instructions.js:19-40`; `skill.md:15`).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | After the bare-/ponytail fix, plan:80's "switches every session in that repo until a new session starts there" is true | UNADDRESSED | HIGH | SessionStart runs on startup/resume/clear/compact (`hooks_claude-codex-hooks.json:5`); every non-compact start resets to the default (`hooks_ponytail-activate.js:193,55`) on the shared per-project flag (`runtime.js:51-66,75-78`), so any new session, `/clear` or resume in that directory resets every running session there; other sessions' main thread gets no new ruleset (`mode-tracker.js:143-148`); scope is the project directory (sha256 of CLAUDE_PROJECT_DIR), so each worktree has its own mode |
| INV-002 | guard_conditions | "Bare /ponytail switches on at the default (lite)" covers every default | UNADDRESSED | MEDIUM | `mode-tracker.js:117`: with default `off`, bare /ponytail switches to `full` |
| INV-003 | state_variables | Quoting the lite row describes what lite injects | UNADDRESSED | MEDIUM | `instructions.js:19-40,87-88` drop only other levels' table rows and examples; every rule of `skill.md:15-44` is injected (incl. "End your reply with one or two lines", "leaves one small test", "grep every caller") |
| INV-004 | interaction_effects | `~/.claude/...` paths and "installed with lite" hold on every workspace | UNADDRESSED | MEDIUM | Ponytail follows CLAUDE_CONFIG_DIR (`hooks_ponytail-config.js:71-74`, `runtime.js:35`, `activate.js:28-29,113`); IronClaude always writes `$HOME/.claude` (`install_user_setup.py:145,263,267`; `docs/getting-started/installation.md:362-366`) |
| INV-005 | interaction_effects | Known Limitation risk is confined to Ponytail | UNADDRESSED | MEDIUM | Every marketplace add precedes every install (`install_user_setup.py:272-284`); the new clone consumes the shared 30 s budget before the six existing installs (`:35,290-293`) |
| INV-006 | interaction_effects | The one-time statusline note reaches a person or an Orca worker | UNADDRESSED | MEDIUM | First session may be a headless `claude -p` run (matcher includes `startup`), which uses up the nudge silently (`activate.js:133-134`); only the user settings file is read (`activate.js:29,77-84`); a parse error suppresses it (`:165-167`) |
| INV-007 | guard_conditions | Any flag file suppresses every statusline note; script copied once | UNADDRESSED | LOW | Stale-path "STATUSLINE BROKEN" note fires once per stale path (`activate.js:89-99,116,135-141`); script is refreshed every session once it exists (`:122-131`) |
| INV-008 | guard_conditions | `/ponytail <mode>` is the only in-session switch | UNADDRESSED | LOW | "stop ponytail" / "normal mode" as a whole message turn it off (`hooks_ponytail-config.js:40-43`; `mode-tracker.js:160-166`; `skill.md:17`) |
| INV-009 | guard_conditions | PONYTAIL_SUBAGENT_MATCHER strictly limits injection | UNADDRESSED | LOW | Unanchored, case-insensitive; fails open on bad regex, missing agent_type, or 100 ms timeout (`hooks_ponytail-subagent.js:32-40,61-78`) |
| INV-010 | collection_boundaries | Whatever env value exists is used | UNADDRESSED | LOW | Non-dict `env` is skipped (`install_user_setup.py:153-157`) while the plugin is still enabled; an invalid value resolves to `full` (`hooks_ponytail-config.js:16,20-24,85-88,103-104`) |
| INV-011 | collection_boundaries | T1 marketplace/source.repo invariant and the `ponytail@ponytail` id hold | ADDRESSED | LOW | `user_settings_defaults.json:36-48`; upstream marketplace and plugin both named `ponytail` |
| INV-012 | count_divergence | Task 1 diff is "three added lines plus commas/braces" | ADDRESSED | LOW | Consensus adopted the expanded JSON form (more lines); plan:47 read as intent, not a literal count |
| INV-013 | state_variables | "Set the ledger option to false" is actionable | UNADDRESSED | MEDIUM | `ledger` is a plugin userConfig option (`.claude-plugin/plugin.json:15-20`); the plan never says where a user sets it |
| INV-014 | guard_conditions | "Only running claude plugin uninstall gets reinstalled" | UNADDRESSED | LOW | Depends on uncited uninstall behaviour toward `enabledPlugins` (`install_user_setup.py:266`) |
| INV-015 | interaction_effects | Ponytail's subagent injection is harmless beside IronClaude's | UNADDRESSED | LOW | `src/superclaude/hooks/hooks.json:110-128` already injects Pragmatic; Ponytail's "end your reply with one or two lines" (`skill.md:15`) can conflict with strict output contracts; user decision stands (A-003), doc note only |
| INV-016 | state_variables | `env -u CLAUDE_CONFIG_DIR -u XDG_CONFIG_HOME` fully isolates the proof | UNADDRESSED | LOW | Exported `PONYTAIL_*` variables would leak (`hooks_ponytail-config.js:85`, `activate.js:66`, `subagent.js:35`); also unset PONYTAIL_DEFAULT_MODE, PONYTAIL_MAP, PONYTAIL_SUBAGENT_MATCHER |

## Summary

- **Total findings**: 16
- **ADDRESSED**: 2
- **UNADDRESSED**: 14
  - HIGH: 1 (INV-001)
  - MEDIUM: 6 (INV-002, INV-003, INV-004, INV-005, INV-006, INV-013)
  - LOW: 7 (INV-007, INV-008, INV-009, INV-010, INV-014, INV-015, INV-016)
- Sufficiency verdict: the consensus fixes alone do not make Task 3's docs true (INV-001..INV-004). Tasks 1, 2 and 4 hold as planned.

## Invariant Probe Gate

CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001
These invariant violations must be resolved before convergence can be declared.
Resolution path taken: depth is standard (no Round 3); INV-001 is carried into the merged verdict as a blocking implementation-time correction, and the adversarial run is reported `partial` with `unaddressed_invariants: [INV-001]`.

WARNING: 6 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-002, INV-003, INV-004, INV-005, INV-006, INV-013
These items do not block convergence but should be reviewed.
