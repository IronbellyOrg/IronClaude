# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent agent (model class opus), read-only; ran bash/awk/jq experiments in a private /tmp directory with a fake `python3` that prints `RAN-python3`. Bash ground truth is quoted per finding.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | guard_conditions | Narrowing the pinned test to "no Bash registration whose command contains freshness-" keeps its invariant | UNADDRESSED | MEDIUM | Assertion came from commit a5e9df4b (bash batching policy: "no hard Bash counter is installed", docs/user-guide/freshness-hooks.md:22); no freshness- Bash hook ever existed (`git log --all -G 'matcher.*Bash' -- src/superclaude/hooks/hooks.json` empty); a future counter can have any name. Invariant holds only as an allowlist: Bash-matcher PreToolUse commands == {block-bare-python.sh} |
| INV-002 | state_variables | The command reaches the awk scanner byte-for-byte | UNADDRESSED | MEDIUM | `awk -v` processes escapes: raw `printf "a\\nb"` becomes `printf "a\nb"` (mawk 1.3.4); ENVIRON/stdin keep bytes. Pass on stdin |
| INV-003 | collection_boundaries | The 100 KB timing case proves large commands are handled | UNADDRESSED | MEDIUM | MAX_ARG_STRLEN 128 KB: 140 KB via awk -v or env fails `Argument list too long` rc=126 -> fail-open allows trailing `; python3 x`; via stdin rc=0. Add ~200 KB case |
| INV-004 | state_variables | Exempting only quoted-delimiter heredoc bodies from quote tracking prevents desync | UNADDRESSED | HIGH | Unquoted-delimiter heredoc: quotes literal, `$(` and backticks still expand. `cat <<EOF / don't / EOF / python3 E3` -> RAN-python3 E3; `cat <<EOF / v=$(python3 E4) / EOF` -> runs |
| INV-005 | interaction_effects | Continuation join and comment strip are cheap pre-passes | UNADDRESSED | MEDIUM | No continuation after a comment (`echo a # C:\` + `python3 E1` runs); `echo a \` + `EOF` still terminates a quoted heredoc (E2); unquoted heredoc joins. Join must live inside the scanner, per state |
| INV-006 | collection_boundaries | A heredoc terminator is a line equal to the delimiter | UNADDRESSED | MEDIUM | `<<-'EOF'` strips leading tabs: tab+EOF terminates; `python3 E5` after it runs |
| INV-007 | guard_conditions | `<<` always starts a heredoc | UNADDRESSED | MEDIUM | `<<<` here-string has no body: `cat <<< '{}' / python3 E6` runs; `$((1<<4))` also not a heredoc |
| INV-008 | state_variables | `)` closing `$(...)` starts a new simple command | UNADDRESSED | MEDIUM | FP: `ls -d $(pwd)/bin/python3` only prints a path; FN: `PYTHONPATH=$(pwd)/src python3 E13` runs. Resume the outer word |
| INV-009 | count_divergence | Every `(`/`)` pushes/pops one level | UNADDRESSED | LOW | `$((1+2))`, case patterns `a)`; `echo "$(echo $((1+2)) )"; python3 E15` runs |
| INV-010 | guard_conditions | Quoted text is never a command word, even in command-word position | UNADDRESSED | MEDIUM | `"python3" E9`, `'python3' E9b`, `\python3 E9c`, `"$PWD/bin/python3" E10` all run. Dequote the command word before the basename check |
| INV-011 | guard_conditions | Command word follows only assignments, keywords and wrappers | UNADDRESSED | LOW | Leading redirections: `< in.json python3 E7`, `>out.txt python3 E8` run |
| INV-012 | interaction_effects | Heredoc body runs only if its own command word is a shell | UNADDRESSED | LOW | `cat <<'EOF' | bash / python3 E14 / EOF` runs; `sudo bash`, `/bin/bash`, partly quoted delimiters unspecified |
| INV-013 | state_variables | Every `'` outside double quotes toggles a plain single-quoted string | UNADDRESSED | LOW | `$'don\'t'` then `python3 E11` runs |
| INV-014 | guard_conditions | Wrappers recognised by exact name | UNADDRESSED | LOW | `/usr/bin/env python3`, `coproc python3`, `command -p python3`, `time -p` |
| INV-015 | count_divergence | Dropping C-016 costs nothing | UNADDRESSED | LOW | `arr=(python3 pip)` runs nothing; split at `(` blocks it |
| INV-016 | interaction_effects | Task 7's fresh session will send bare python3 to Bash | UNADDRESSED | MEDIUM | Live ~/.claude/CLAUDE.md lines 7 and 34 forbid it; model may refuse or rewrite; `--bare` skips settings hooks. Use --append-system-prompt; record refusal as blocked |
| INV-017 | sufficiency_challenge | Fresh-session block holds wherever superclaude install ran | UNADDRESSED | MEDIUM | Hook fails open without jq (plan L21); install_hooks.py:16 "no jq shell-out"; only docs/user-guide/freshness-hooks.md:133-135 names jq. Warn at install or state precondition |
| INV-018 | sufficiency_challenge | Block message names uv run python and jq | ADDRESSED | LOW | Plan L43, L47, L56 |
| INV-019 | interaction_effects | Fixing read-parse.md:8 removes every bare-python instruction in shipped primitives | UNADDRESSED | LOW | templates/workflow/02_mdtm_template_complex_task.md:965 tells agents to run `python -m pytest` via Bash |
| INV-020 | state_variables | HOME monkeypatch redirects install_hooks() with no target | ADDRESSED | LOW | install_hooks.py:135-136 resolves Path.home() at call time |
| INV-021 | guard_conditions | A PATH shim without jq proves the jq branch caused exit 0 | UNADDRESSED | LOW | Any missing tool exits 0; shim must provide bash; assert a jq-branch-only stderr marker |
| INV-022 | sufficiency_challenge | Bash is the only tool that runs shell commands | UNADDRESSED | LOW | Monitor tool takes a shell `command`; outside the Bash matcher; list as ceiling |
| INV-023 | count_divergence | Splitting at `&` is safe with `2>&1`, `&>` | ADDRESSED | LOW | Post-split piece starts with fd or filename |
| INV-024 | interaction_effects | Process substitution `<(python3 ...)` caught | ADDRESSED | LOW | Split at `(` makes python3 a command word |
| INV-025 | state_variables | Nested `"$(echo "$(python3 -c 1)")"` handled | ADDRESSED | LOW | Context stack; holds only with INV-008 and INV-009 |
| INV-026 | collection_boundaries | ~12 ms awk timing carries to every awk | UNADDRESSED | LOW | only mawk measured; run scanner with LC_ALL=C |
| INV-027 | sufficiency_challenge | The consensus scanner satisfies every Done-when bullet | UNADDRESSED | HIGH | Falsified by INV-003, 004, 006, 007, 008, 010 (runs bare python, not blocked), INV-008 E12 (path blocked), INV-016/017 (fresh session) |

## Summary

- **Total findings**: 27
- **ADDRESSED**: 5
- **UNADDRESSED**: 22
  - HIGH: 2 (INV-004, INV-027)
  - MEDIUM: 10 (INV-001, INV-002, INV-003, INV-005, INV-006, INV-007, INV-008, INV-010, INV-016, INV-017)
  - LOW: 10

CONVERGENCE BLOCKED: 2 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-004, INV-027
These invariant violations must be resolved before convergence can be declared.
Action: carried into the merged verdict as implement-time amendments (the plan file is not edited, A-002).

WARNING: 10 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-002, INV-003, INV-005, INV-006, INV-007, INV-008, INV-010, INV-016, INV-017
