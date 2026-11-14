# QA Report - Conventions Lens (T250)

**Date:** 2026-11-12
**Reviewer stance:** adversarial, report-only (fix_authorization: false)
**Scope:** sweep.md, sc-sweep-protocol/SKILL.md, test_sweep_command.py compared against graph.md, issue.md, sc-graph-protocol/SKILL.md, test_graph_command.py

## Method

Read from disk now, in chunks of at most 150 lines: `sweep.md`, `sc-sweep-protocol/SKILL.md`, `test_sweep_command.py` (572 lines), `graph.md`, `issue.md`, `sc-graph-protocol/SKILL.md`, `test_graph_command.py`, `pragmatic.md` lines 1-60, `WORKER-CONTRACT.md` lines 14-27, DESIGN 7.6 (`docs/designs/orchestrator-mode.md:649-666`). Ran `uv run pytest tests/commands tests/recommend` (628 passed), `ruff check` and `ruff format --check` (clean). No file edited, no live Orca command. No other lens report was read.

## Findings

All findings are MINOR. None is BLOCKING or MAJOR.

### F1 (MINOR) Test file does not pin three things the house tests pin
- Pattern broken: `tests/commands/test_graph_command.py:113-124` (frontmatter `name`, `argument-hint` tokens, `> Skill sc:graph-protocol` in the command); the same pins sit at `test_impact_command.py:147-162` and `test_issue_command.py:75-77,184`.
- Evidence: `tests/commands/test_sweep_command.py:106-168` pins `allowed-tools`, the two surface paths, step order, timeout, the Unattended heading and the `src/superclaude/` path, but nothing asserts `> Skill sc:sweep-protocol` (`sweep.md:45`), `name: sweep` (`sweep.md:2`) or the `argument-hint` (`sweep.md:8`). A grep of `tests/`, `src/` and `plugins/` for `sc:sweep-protocol` finds only the skill itself and `sweep.md:45`.
- Not required by the DESIGN 7.6 test bullet (`orchestrator-mode.md:666`), so this is a convention gap, not a spec gap.
- Smallest fix: add one test asserting `"> Skill sc:sweep-protocol" in _section(_text(_COMMAND), "## Activation")` plus `_frontmatter(_COMMAND)["name"] == "sweep"`.

### F2 (MINOR) Test docstring departs from the house first line
- Pattern: `test_graph_command.py:1` and `test_impact_command.py:1`: `"""Drift guards for /sc:X and sc:X-protocol (issue #323, Phase 3).`, then a purpose paragraph, then `CI-safe: pure file-content assertions.`
- Evidence: `test_sweep_command.py:1` says `Static drift guards for /sc:sweep, sc-sweep-protocol ...`: it uses the directory form `sc-sweep-protocol`, not the skill name `sc:sweep-protocol` (`SKILL.md:2`), and cites no issue number (this branch is issue 339). The CI-safe closing paragraph (lines 13-17) is present.
- Fix: `"""Drift guards for /sc:sweep and sc:sweep-protocol (issue #339, Phase 1) ...`.

### F3 (MINOR) Activation sentence is shortened
- Pattern: `graph.md:46` and `issue.md:103`: "Do NOT proceed with protocol execution using only this command file."
- Evidence: `sweep.md:47`: "Do NOT proceed using only this command file." The `**MANDATORY**` line and the `> Skill ...` line (`sweep.md:44-45`) match `graph.md:43-44` in form.
- Fix: restore the house wording.

### F4 (MINOR, intentional) `Bash(cmd:*)` prefix syntax
- Pattern: `graph.md:9` and `sc-graph-protocol/SKILL.md:4` use `Bash(cmd *)` (space star). Only `help.md:6` also uses `:*`.
- Evidence: sweep `SKILL.md:4` uses `Bash(superclaude sweep run:*)`. DESIGN 7.6 (`orchestrator-mode.md:661`) and the test (`test_sweep_command.py:30-33`) pin this exact literal, so it is a deliberate spec choice. Recorded only as a departure from the named house files.

### F5 (MINOR, note) Closing section name of the skill
- Pattern: `sc-graph-protocol/SKILL.md:160` has `## Will Not` only; `sc-issue-protocol/SKILL.md:164,172` has `## Will` and `## Will Not`.
- Evidence: `sc-sweep-protocol/SKILL.md:51` uses `## Boundaries` with bold `**Will:**` / `**Will Not:**`. Seven other skills (validate-tests, adversarial, post-release, cli-portify, init-lite, task, cleanup-audit) use `## Boundaries`, and the sweep command follows `graph.md:70-81`. No fix needed.

### F6 (MINOR) No "no other skill calls this one" guard
- Pattern: `test_graph_command.py:219-225` (`test_graph_no_skill_callers`) backs `sc-graph-protocol/SKILL.md:15`.
- Evidence: `sc-sweep-protocol/SKILL.md:15` makes the same claim ("No other skill calls this one."); no sweep test checks it. The claim is true today (grep above).

### F7 (MINOR) Test docstring cites line numbers
- Evidence: `test_sweep_command.py:73` says "style lines 22 to 26". Read now: `pragmatic.md:22` is the primary rule and `:23-26` are the four sub-bullets, so it is correct today but will drift. Fix: say "the primary rule and its four sub-bullets".

### F8 (MINOR, out of lens, hand to the claims lens) Never-as-worker claim is not yet true on disk
- Evidence: `sweep.md:16` says `/sc:sweep` "is on the never-as-worker list in `~/.claude/WORKER-CONTRACT.md`". `src/superclaude/core/WORKER-CONTRACT.md:23` lists `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard` and `/sc:pr-submit`; no `/sc:sweep`, and the file is unmodified in `git status`. DESIGN section 8 (`orchestrator-mode.md:670-690`) makes adding it a gated step (1.17 to 1.19) of the same PR.
- Graded MINOR here only because the fix is a planned later step. At the final gate it must be re-read; if step 1.18 has not landed, the sentence is a false claim and becomes blocking.

## Checks

| Id | Check | Result |
|---|---|---|
| C1 | Command frontmatter key order equals `graph.md:2-9` (name, description, category, complexity, mcp-servers, personas, argument-hint, allowed-tools) | PASS |
| C2 | Skill frontmatter order and the `<!-- Extended metadata (for documentation, not parsed): ... -->` comment equal `sc-graph-protocol/SKILL.md:1-11` | PASS |
| C3 | Command heading names and order follow `issue.md` (title, Triggers, Usage, Options) plus `graph.md` (Activation before Boundaries), as DESIGN 7.6 says; no Unattended heading | PASS |
| C4 | Activation block wording equals `graph.md:41-46` | FAIL (MINOR, F3) |
| C5 | Boundaries block uses bold Will / Will Not as `graph.md:70-81` | PASS |
| C6 | Skill H1, "Backs `/sc:x` (...)" intro and "No other skill calls this one" as `sc-graph-protocol/SKILL.md:13-15` | PASS |
| C7 | Skill closing section name vs graph and issue skills | PASS (note F5) |
| C8 | `allowed-tools` syntax vs graph | PASS (spec-mandated, note F4) |
| C9 | Test helpers (`_REPO`, `_COMMAND`, `_SKILL`, `_text`, `_frontmatter`, `_section`) and `test_<cmd>_*` naming equal `test_graph_command.py:16-111` | PASS |
| C10 | Test docstring style equals `test_graph_command.py:1-9` | FAIL (MINOR, F2, F7) |
| C11 | Test pins the same kinds of facts as graph, impact and issue tests (name, argument-hint, `> Skill` invoke, no-callers) | FAIL (MINOR, F1, F6) |
| C12 | `uv run pytest tests/commands tests/recommend`: 628 passed; `ruff check` and `ruff format --check` clean | PASS |
| C13 | `tests/recommend/test_routing_refresh.py:33` adds `"sweep"` to `_POST_REFRESH_ADDITIONS` the same way as graph, impact, issue (one-line diff) | PASS |
| C14 | Options table defaults (`6h`, 720h or 30d, root, output) agree with `src/superclaude/cli/sweep/commands.py:27-28,44-51,226-240` | PASS |
| C15 | No plugin mirror for graph, issue, impact or sweep under `plugins/superclaude/commands` or `skills` | PASS |
| C16 | No em dash, en dash, tab or trailing space in `sweep.md` or `SKILL.md`; both end with one newline like `graph.md` | PASS |
| C17 | Out-of-lens claim `sweep.md:16` against `WORKER-CONTRACT.md:23` | FAIL (MINOR, F8) |

## Self-audit

- Checks run: 17. Every FAIL is MINOR (convention gaps and one forward-dependent claim); none changes behaviour.
- I did not rely on earlier reviews or on the other lens reports.
- Not verified: live behaviour of the skill, the Orca reads, and whether step 1.18 will land (F8).

Verdict: PASS
Blocking count: 0
