# Wave 1.6 Branch A — log-call inspection (returned by troubleshoot-analyst; persisted by parent on receipt)

degraded: true (auggie not in roster; codegraph not called; all cited files Read directly). captured_bytes: null for every hit (no failing-run capture).

query_target: user-visible output of `superclaude update` (src/superclaude/cli/main.py:340-429; update_notice in src/superclaude/cli/install_retired_mcp.py), `superclaude doctor` codegraph check (src/superclaude/cli/doctor.py:146-214 rendered by main.py:477-510), codegraph SessionStart hook (src/superclaude/hooks/scripts/codegraph-session-start.sh).

| file:line | call_type | level | richness | snippet |
|---|---|---|---|---|
| src/superclaude/cli/main.py:360 | click_echo | info | minimal | "🔄 Updating SuperClaude to version {__version__}..." |
| src/superclaude/cli/main.py:364 | click_echo | info | silent | phase banners 364/371/377/383/393/398/403; none for codegraph or retire |
| src/superclaude/cli/main.py:411 | click_echo | info | minimal | `notice = update_notice(); if notice: click.echo(...)` |
| src/superclaude/cli/main.py:414 | exception_handler | none | silent | `except Exception: pass` |
| src/superclaude/cli/main.py:417 | exit_code | — | silent | exit 1 only on framework phases; no codegraph term |
| src/superclaude/cli/install_retired_mcp.py:320 | return value | info | minimal | returns "legacy registration present: run `superclaude install`" only if a finding is removable, else None |
| src/superclaude/cli/install_retired_mcp.py:255 | exception_handler | none | silent | `_codegraph_ready_now` returns False on exception |
| src/superclaude/cli/install_retired_mcp.py:171 | classifier | none | silent | kind-B codebase-memory kept when binary present → no notice |
| src/superclaude/cli/install_retired_mcp.py:195 | classifier | none | silent | current-pin Serena kept when codegraph not ready → no notice |
| src/superclaude/cli/install_retired_mcp.py:327 | doctor warning | warning | minimal | "legacy registration present for ...; run `superclaude install` to retire it" (removable findings only) |
| src/superclaude/cli/doctor.py:158 | doctor_check | pass | silent | `passed = True`; flipped only at :171 |
| src/superclaude/cli/doctor.py:163 | doctor_check | detail | rich | "no codegraph registration; run `superclaude install`" (check still passes) |
| src/superclaude/cli/doctor.py:170 | doctor_check | fail | rich | registered command not executable → fail |
| src/superclaude/cli/doctor.py:182 | doctor_check | detail | rich | version differs from pin → run `superclaude install` (passes) |
| src/superclaude/cli/doctor.py:208 | doctor_check | detail | minimal | "Ready for Serena retirement: no (codegraph is not registered)" |
| src/superclaude/cli/doctor.py:149 | design note | — | rich | "Fails only when the registered command is not an executable ... ./update.sh runs doctor only after install exited 0" |
| src/superclaude/cli/doctor.py:217 | doctor_check | warning | minimal | `_check_retired_mcp` passes in every branch (:226, :232, :237) |
| src/superclaude/cli/main.py:494 | click_echo | info | minimal | ✅/❌ per check name |
| src/superclaude/cli/main.py:497 | click_echo | verbose-only | minimal | details printed only with --verbose |
| src/superclaude/cli/main.py:506 | click_echo | info | minimal | "✅ SuperClaude is healthy" |
| src/superclaude/hooks/scripts/codegraph-session-start.sh:19 | exit | none | silent | no binary → exit 0, nothing printed or logged |
| src/superclaude/hooks/scripts/codegraph-session-start.sh:31 | file log | — | minimal | init log written only when a binary exists |

## Answers

- **update_notice when codegraph is absent:** prints nothing unless a provably IronClaude-written legacy entry is removable; with codegraph absent, the current-pin Serena entry and a kind-B codebase-memory entry are kept, so still no notice. Update header/banners never mention codegraph; exit code ignores codegraph (update exits 0).
- **doctor when codegraph is absent:** passes. The "no codegraph registration; run `superclaude install`" detail prints only with `--verbose`; summary is "✅ SuperClaude is healthy". doctor.py:149-152 assumes doctor runs after a successful install (true for ./update.sh, false after `superclaude update`).
- **hook when codegraph is absent:** emits nothing; exits 0 at line 19 before any log file is created.
