# A3 / G8 post-merge codegraph check: RESULT

**Verdict:** PASS

Checked 2026-10-31T23:46Z to 2026-11-01T00:00Z (UTC, from `date -u`) on the install the coordinator upgraded from master f90877be at 23:43 UTC. This session started at 23:44:56 UTC, after the upgrade.

## Criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Installed skills match master | PASS | `cmp` of ~/.claude/skills/sc-troubleshoot-protocol/SKILL.md and ~/.claude/CODEGRAPH.md against master: identical. `diff -rq` of ~/.claude/skills, ~/.claude/commands/sc and ~/.claude/agents against src/superclaude/: no file differs (only `__pycache__`, `__init__.py`, `README.md` and Orca's own `computer-use`, `orca-cli`, `orchestration` skills, which explain "38 available, 41 installed"). All 9 core files byte-identical. `superclaude doctor`: healthy. See a3-check/install-state.md sections 3-5. |
| 2 | The troubleshoot run used the NEW skill | PASS | The run executed the new skill's codegraph readiness step (installed SKILL.md:195): audit.log records `index_state: fresh`, `checked_at`, `worktree_root`, `projectPath`, token `graph:telemetry_on`. It ran the codegraph tier (`codegraph_search`, `codegraph_node` with code, `codegraph_callers`) and wrote `troubleshoot/tier1-callers.md`. It dispatched the `troubleshoot-analyst` worker, whose roster lists the codegraph tools. Discriminator: the pre-codegraph skill (git `2f10a0e1^`) has 0 "codegraph" mentions and 11 Serena/codebase-memory mentions; the installed skill has 15 and 0. `/sc:graph status` also worked: index fresh (own), pin 1.6.2 match, MCP lookup tools listed (install-state.md section 8). |
| 3 | No install defect that would ship broken in 5.0.0 | PASS | troubleshoot REPORT.md (status partial, confidence 0.75, Tier 1 under `--depth quick`): the skip at install_core.py:66 is documented (installation.md:363) and test-pinned (test_how_we_work_install.py:54) behaviour, reachable only from a plain `superclaude install`. `update` hardcodes `force=True` (main.py:365) and update.sh runs `install --force` (update.sh:8). After the forced upgrade no core file is stale (9/9 `cmp` identical). |

Why "partial" in the troubleshoot report does not fail criterion 3: the partial status comes from a pending pytest measurement (no .venv in this worktree; creating one was forbidden), degraded retrieval (auggie unavailable) and the Tier 1 confidence cap. None is an install defect; the live install state was verified directly.

### Non-blocking findings (do not change the verdict)

- **Stale troubleshooting doc:** docs/reference/common-issues.md:18-28 tells users to `pipx upgrade SuperClaude` (the upstream package), run `python3 -m SuperClaude install` without `--force`, and expect version 4.1.5. A user who follows it keeps old core files. Docs fix only: replace it with installation.md:326-329.
- **Version string:** `superclaude --version` prints 4.3.5 on master f90877be. The 5.0.0 bump has not landed; the release gate must do it before tagging.
- **`--list` is name-only:** install_core.py:153 counts core files by name, so `superclaude install --list` cannot reveal a stale file.
- **codegraph server text:** the codegraph 1.6.2 server's instructions describe a single `codegraph_explore` tool, which this session does not list. This session lists the 7 tools IronClaude documents. That mismatch is upstream text, not an IronClaude install defect.

## update.sh without pipx (separate note)

**Classification: environment issue on this image, not a 5.0.0 release defect. update.sh has a hardening gap worth fixing.**

What fails: update.sh runs under `set -euo pipefail` (update.sh:2) and its first command is `pipx install --force ./` (update.sh:7). On this image there is no pipx binary: `command -v pipx` finds nothing, `/usr/bin`, `/usr/local/bin` and `~/.local/bin` have no `pipx`, Python has no `pipx` module, and `bash -c 'set -euo pipefail; pipx --version'` exits 127 with `pipx: command not found`. So update.sh stops at line 7 before `superclaude install --force`.

Why it is an environment issue:
- The documented install methods assume pipx is present or tell the user to install it: README.md:60 and docs/getting-started/installation.md:126-138 ("Method 1: pipx (Recommended)", with `python3 -m pip install --user pipx`). The documented update procedure, installation.md:326-333, gives a pipx line and a pip alternative.
- This image used pipx's layout without a pipx binary: superclaude resolves to ~/.local/share/pipx/venvs/superclaude/bin/superclaude, installed through `uvx pipx` (per the brief). A user who installed by the documented pipx method has pipx and is not affected.

Why it is still a gap:
- update.sh hard-requires pipx with no check or fallback, and fails with a bare exit 127.
- installation.md:94 lists pipx as "Optional", which contradicts update.sh's hard dependency.
- update.sh is referenced as the upgrade path in docs/user-guide/mcp-installation.md:7 and :23 and CHANGELOG.md:51.

Recommended follow-up (no change made here): have update.sh check `command -v pipx` first and print the install command (or fall back to `uvx pipx`), and stop listing pipx as optional for the update.sh path.

## Evidence files

- .dev/release-readiness/a3-check/install-state.md (version, doctor, `install --list`, cmp, diff -rq, session codegraph tools, `/sc:graph status`)
- .dev/release-readiness/a3-check/troubleshoot/REPORT.md (troubleshoot report)
- .dev/release-readiness/a3-check/troubleshoot/audit.log (wave log, codegraph readiness, summary footer)
- .dev/release-readiness/a3-check/troubleshoot/tier1-callers.md, tier1-observation.md, tier1-hypothesis.md, tier1-calibration.md, evidence-validation.md, doc-context.md, diagnosability-context.md, diagnosability-tasklist.md, hc0-boundary-scan.md, wave1_5-branch-{A,B,C}.md, wave1_6-branch-{A,B}.md, execution-locus.md, producers.md
