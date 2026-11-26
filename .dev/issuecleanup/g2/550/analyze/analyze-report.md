# Shared review architecture analysis
## Scope and grounding
- Command: `/sc:analyze src/superclaude/cli/review --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/550/analyze`.
- Assessed on 2026-11-24 at checkout HEAD `a7ae3dd30`; target is the smallest shared package covering panel selection, findings processing and telemetry.
- Codegraph: index_state=fresh, checked_at=2026-11-24T02:47:40Z; degraded: graph:truncated. Access: mcp. Root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`.
- Readiness ran once; grouped layout, main-file outlines, a function body, resolver callers/callees and load-panel impact preceded direct source reads. Resolver callers were capped at 5 of 29, so no exhaustive caller claim is made.
- Static architecture check only, not an experiment rerun or implementation.
## Architecture and metrics
- Layout: 20 Python modules in the target, plus 11 packaged JSON configuration files. The package separates Click command adapters from panel resolution, findings/ledger processing, telemetry, safety checks and fix checking. Registration tolerates absent optional adapters: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/__init__.py:19-38`.
- Current selection flow: the command loads panel and tier data, validates it and resolves reviewers at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/panel_cmd.py:77-122`. The packaged default is selected by a pointer at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/panel.py:447-487`; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-default.json:1` selects wonsol.
- The packaged wonsol panel defines three reviewer slots and says only its model mix ships, not the evaluation seat lenses: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/data/review-panel.wonsol.json:5-11`.
- Deterministic findings/fix-map helpers remain a separate layer: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/findings.py:1-24`. Telemetry distinguishes three truth bases and records panel version/hash: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/review/telemetry.py:17-39`. Those are reusable measurement primitives, not an experiment qualification inventory.
- Graph impact returned the panel command and default-panel regression tests for load_panel; their presence was inspected, not executed.
## Severity-rated findings
### Important
- No experiment qualification surface exists in the shared review package. A source search for inventory, proven-design, Recipe Ledger and 16-defect terms returned no matches. The architecture can resolve panels and record telemetry, but it does not represent experiment result classes or carry the tasklist designs into the shared panel.
- The current default panel is a model-selection configuration only. Its description and three-slot layout provide no field for collaboration behavior, Recipe Ledger instructions or measured adoption status.

### Medium
- The shared findings and telemetry contracts are reusable, but their fields describe individual review records rather than an experiment inventory. Reusing them does not by itself satisfy the issue's qualification and retest criteria.

### Note
- The resolver caller lookup was truncated at 5 of 29 rows, so the command adapter and inspected tests are known consumers, not a complete blast radius.
## Recommendations and roadmap
- First complete the experiment qualification inventory from the retained branch evidence and existing value inventory. Do not add experiment designs to the shared panel before that classification and the parent unification plan.
- Reuse the existing panel pointer, findings contract and telemetry rather than creating another review subsystem. Add only the fields or caller path that the accepted design actually needs.
- Keep the current wonsol default provisional and model-only until its confirming test or a replacement design meets the stated adoption bar.
## Verification limits
- Static quick pass only; no tests were executed and no experiment statistics were recomputed.
- Resolver caller evidence is truncated at 5 of 29 rows. The command adapter and default tests were directly inspected.
- Experiment reports were read through cached git objects and bounded excerpts. Worktree deletion state, uncommitted branch work and full raw scoring evidence were not verified.
