# Agent 5 — CLI Tools Eval Proposals

## Proposal 1 (one-off): `eval_real_no_pty_smoke`

- **Targets:** `eval doctor`/`list`/`describe`/`run`
- **Hypothesis:** Suite discovery/schema valid, real suite skip path works, report artifacts emitted.
- **Cadence:** one-off.
- **Inputs:** `superclaude eval doctor --json --no-mcp`; `eval describe --suite real --eval E3 --json`; `eval run --suite real --no-pty --no-mcp --junit --json`.
- **Assertions:** exit 0; 15 skipped; `summary.md/json/yaml`; `junit.xml` produced.
- **Requires:** claude, jq, make, git; no MCP.
- **Complexity:** simple.
- **Value:** Catches CLI harness/report/schema regressions.
- **Evidence:** `src/superclaude/cli/eval/commands.py:769`, `:928`, `:1211`, `:1554`, `:1679`; `src/superclaude/cli/eval/suites/real.yaml:5`; `src/superclaude/cli/eval/reporter.py:168`.

## Proposal 2 (one-off): `roadmap_tasklist_validation_pipeline`

- **Targets:** `roadmap run`/`validate`, `tasklist validate`
- **Hypothesis:** Artifact gates and HIGH-severity exit behavior enforced.
- **Cadence:** one-off.
- **Inputs:** prompt Bash to run minimal spec through roadmap then tasklist validate.
- **Assertions:** exit 0; `roadmap.md`, `test-strategy.md`, `extraction.md`, `tasklist-fidelity.md` produced.
- **Requires:** claude.
- **Complexity:** complex.
- **Value:** Catches LLM pipeline contract drift.
- **Evidence:** `src/superclaude/cli/roadmap/commands.py:32`, `:262`, `:323`; `src/superclaude/cli/tasklist/commands.py:173`.

## Proposal 3 (recurring): `installer_idempotence_release_gate`

- **Targets:** `install`, `install-skill`, agents/skills installers.
- **Hypothesis:** Isolated-HOME install is repeatable and prevents duplicates.
- **Cadence:** recurring — on release/merge events.
- **Inputs:** install, then re-install, then `--force` install.
- **Assertions:** first install success; repeat skip/fails as documented; `--force` succeeds.
- **Requires:** claude, uv, pipx.
- **Complexity:** medium.
- **Value:** Catches packaging regressions.
- **Evidence:** `src/superclaude/cli/main.py:46`, `:313`; `src/superclaude/cli/install_skill.py:40`; `src/superclaude/cli/install_skills.py:58`.
