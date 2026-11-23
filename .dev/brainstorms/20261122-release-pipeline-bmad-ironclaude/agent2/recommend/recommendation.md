# /sc:recommend result (run by ic-planner on 2026-11-22, `--unattended`, local mode)

Goal: a release planning and execution pipeline in which BMAD plans upfront (epics and user stories as GitHub issues) and hands each user story to IronClaude for design brainstorming, tasklist generation and execution, with a coordinator session driving both and GitHub issues kept current.

Return contract fields: status `success`; mode `local`; recommendation_kind `multi_path`; guide_status `no_match`; routing_row_id empty; auggie_status `ok`.

## How the skill decided

- Step 0: read `~/.claude/HOW-WE-WORK.md` (installed copy; this checkout's `src/superclaude/core/HOW-WE-WORK.md` was not read, because the working tree is behind origin/master, see degradation notes). No single routing row fits the whole outcome. Closest rows were `shape-idea` (brainstorm), `simple-plan` (workflow then implement), `compare-options` (adversarial) and `critique-spec` (spec-panel); each covers one step, none covers a coordinator-run pipeline across two toolsets. So `no_match`.
- Hot-path cache: not run. Under `--unattended` the skill never writes `.claude/cache/`, and the availability gate needs `uv run superclaude recommend`, which can create a virtual environment outside the allowed folder. The live path (Phase 0 to 2) was used instead, as the skill allows.
- Phase 0 Step A: enumerated `~/.claude/commands/sc/*.md`, `~/.claude/skills/*`, `~/.claude/agents/*.md`, `~/.claude/templates/**`, project `.claude/skills/bmad-*` (BMAD skills live only in the project copy, not in `~/.claude/skills`).
- Step B: one `mcp__litellm__augment_code-augment_code_search` query on `IronbellyOrg/IronClaude` branch `master` ranked: `/sc:issue` and the `issue_pipeline` CLI group, `/sc:brainstorm`, `/sc:workflow`, `/sc:implement`, the issue watcher design; it found no BMAD integration in `src/` (BMAD appears only as an exclusion in cleanup-audit and in a design note on a PRD flag).
- Step C: read the command file of each candidate: brainstorm, adversarial, spec-panel (first 150 lines), workflow, implement, issue; plus `sc-implement-protocol` (SKILL.md first 110 lines, `refs/ledger.md` first 120, `refs/managed-workspace.md` first 60), `sc-workflow-protocol/refs/input-parse.md` and `overlap-routing.md`, `sc-issue-protocol/refs/chains.md` and `refs/claim.md`, `WORKER-CONTRACT.md` in full.

## Recommended delegation: three layers, smallest first

1. Per-story chain, run by IronClaude workers under a coordinator. It reuses existing commands and adds no new command.
2. The coordinator rules that already exist (`WORKER-CONTRACT.md`, the `issue-pipeline` CLI, `/sc:sweep`, `/sc:closeout`). Reused, with one gap (below).
3. A small set of new templates and two scripts (progress read, BMAD status write). Named in IRONCLAUDE-SIDE.md section 9.

### Paste-ready: per-story chain, default arm (BMAD story is the spec)

```text
Goal: take BMAD story <epic>-<story> (status ready-for-dev) from its story file to merged code.
1. /sc:spec-panel @<story file or copy> --mode critique --focus requirements,testing,correctness --unattended --report-dir <story run dir>/panel
2. /sc:workflow <story file or copy> --depth <quick for simple, standard for medium> --handoff none --unattended --report-dir <story run dir>/wf
3. read the printed plan .dev/tasks/to-do/<id>/<id>.md and its advisory check result; then /sc:implement <that plan path>
```

### Paste-ready: alternate arm (a trigger fired, IronClaude also writes a code-grounded spec)

```text
1. /sc:brainstorm "code-grounded spec for story <epic>.<story> @<story file or copy>" --codebase --blind --depth quick --proposals 2 --unattended --output <story run dir>/bs
2. /sc:adversarial --compare <story file or copy>,<story run dir>/bs/merged-requirements.md --depth quick --focus correctness,architecture --unattended --output <story run dir>/adv
3. /sc:spec-panel @<merged spec> --mode critique --focus requirements,testing,correctness --unattended --report-dir <story run dir>/panel
4. /sc:workflow <merged spec> --depth standard --handoff none --unattended --report-dir <story run dir>/wf
5. read the printed plan and check result; then /sc:implement <that plan path>
```

Changes files: steps 1 to 4 write only report folders and a plan package under `.dev/tasks/to-do/`; step 5 (`/sc:implement`) edits product code and writes the ledger `progress.md`; none commits, pushes, opens a PR or posts to GitHub.

Notes (each is a verified contract fact, not advice):
- `--unattended` is valid on spec-panel, workflow, brainstorm and adversarial (each has an `## Unattended mode` section in `~/.claude/commands/sc/`). `/sc:implement` has none (its command file and skill contain no `unattended` text, also on origin/master), so step 5 has no worker mode: see the gap in IRONCLAUDE-SIDE.md section 6.
- `~/.claude/WORKER-CONTRACT.md` says the P2 commands (including spec-panel) get `--unattended` on a `Command:` line only after a phase 2 live check passes, or when the user's instruction names the command. The owner's text names spec-panel, which is the instruction the coordinator quotes. UNVERIFIED whether the phase 2 check has passed.
- brainstorm and adversarial take their own `--output <dir>` as the report directory; spec-panel and workflow take `--report-dir <dir>`; never both on one line.

## Degradation notes

- `src/superclaude/core/HOW-WE-WORK.md` not read from the checkout (the checkout is behind origin/master); the installed guide was used. Read-only comparison of the two copies was not done: UNVERIFIED that they are equal.
- Auggie ranking saw pushed master code only.
- `--eval` and cache writes: not applicable under `--unattended`.

Sources verified:
- /home/coder/.claude/HOW-WE-WORK.md (routing table, no row matched)
- /home/coder/.claude/commands/sc/brainstorm.md, adversarial.md, spec-panel.md, workflow.md, implement.md, issue.md (Read)
- /home/coder/.claude/WORKER-CONTRACT.md (Read in full)
- /home/coder/.claude/skills/sc-implement-protocol/SKILL.md, refs/ledger.md, refs/managed-workspace.md; sc-workflow-protocol/refs/input-parse.md, refs/overlap-routing.md; sc-issue-protocol/refs/chains.md, refs/claim.md (Read)
- origin/master: docs/designs/issue-watcher-status-pipelines.md, docs/user-guide/orchestrator-mode.md, docs/user-guide/observer.md, src/superclaude/cli/issue_pipeline/cli.py and templates/worker-brief.txt (git show, read-only)
- auggie semantic rank: ok
