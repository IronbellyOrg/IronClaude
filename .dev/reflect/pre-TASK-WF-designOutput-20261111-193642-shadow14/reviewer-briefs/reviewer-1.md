# Reviewer brief — reviewer-1 (persona: analyzer, model class: sonnet, model: claude-sonnet-5-5)

You audit a workflow-plan package (UC-1 pre-execution audit of a tasklist against its driving spec). The package is archived under `.dev/tasks/done/`; the change it planned already landed (commits 7764bb623, 930c5ebc8). Audit the PLAN's fitness against the SPEC. Repository root: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`.

## T1 card excerpt

(from `<output>/t1-card.md`, analyzer slice)

## Audit vantage (grounded)
The package is archived (done/) and the change is already on HEAD: design.md:51-74 carries the Code-graph grounding section; commits 7764bb623 (#511) and 930c5ebc8 (#513). progress.md:7 records FINAL: pass; artifacts/t2-checks.log:39 records pytest rc=0 (1167 passed), :9 sync rc=0, :36 verify rc=0. This is the archived-package corpus class: executor already acted; "no before-state baseline" findings are audit-vantage, discounted to advisory.

## Grounded observations
1. Pinned-phrase risk retired: tests/skills/test_worker_contract.py:550 pins `design-report.md`, `no gate`, `consent is never given` for design; all three survive in design.md:123-124 and :19.
2. AC4/spec-§5 grep constraint holds on HEAD: `grep -n 'src/superclaude' src/superclaude/commands/design.md` exits 1.
3. Shipped-file divergence (advisory): design.md:65 adds "codegraph_impact only if it was not already run for the same symbol in Plan or Design" — a refinement beyond spec §3.2 item 4's unconditional wording. The tasklist (line 28) is faithful to the spec, not the refinement.
4. Task 2 AC3 carries the escape-hatch shape: "or any failure is shown in ./artifacts/t2-checks.log and is not attributable to design.md" — attribution judgment makes the AC unable to fail mechanically. Latent only: the recorded run passed clean.
5. Task 2 AC1 "git diff ... shows no edit inside them" requires a baseline diff that no longer exists for an archived package. Contemporaneous artifacts substitute: t2-checks.log shows the four named test files green.
6. Spec §4 bullet 3 ("no agent is spawned... no brief carries it") is descriptive, restated nowhere in the tasklist; non-imperative, not counted as unmapped.

## T1 conclusion
Plan is a faithful, near-verbatim expansion of the spec with working checks that all recorded green at execution time. No blocking defect in the plan itself. Known latent AC weaknesses are documented classes, not live failures.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/done/TASK-WF-designOutput-20261111-193642/source.md:1-33 (spec goal, copied pattern, section 3.1-3.2)

```markdown
# Design spec: codegraph grounding for /sc:design (issue #504)

Target: `src/superclaude/commands/design.md` (the only file edited; no backing skill exists and none is created). Type: component. Format: spec.

## 1. Goal

`/sc:design` grounds designs in the real code through codegraph when the index is fresh, using it above the existing Glob/Grep/Read floor. Otherwise it runs on Glob/Grep/Read, records a `graph:*` note, and never halts. Every existing flag, behaviour, Unattended-mode rule and Boundary stays unchanged.

## 2. Existing pattern copied (verified)

- `reflect.md` frontmatter: `mcp-servers: [litellm, auggie, codegraph, context7, tavily]`; MCP Integration bullet "codegraph: ... above the native Grep/Read floor (guide `~/.claude/CODEGRAPH.md`)"; Tool Coordination bullet naming `mcp__codegraph__codegraph_status` / `_search` / `_node` / `_callers` / `_callees` / `_impact`, "one readiness check".
- `sc-troubleshoot-protocol` Wave 1: one readiness check per run, record `index_state`, `checked_at`, `worktree_root`, `projectPath`; use codegraph only when `index_state` is `fresh` and lookup tools are listed; otherwise run the native floor and add the matching `graph:*` token; graph rows are leads, Read before citing, empty never proves absence.
- `core/CODEGRAPH.md` (installed as `~/.claude/CODEGRAPH.md`): section 2 readiness check, section 3 closed token list, section 4 tool table, section 5 rules, section 7 Never list.

## 3. Changes to design.md

### 3.1 Frontmatter

Change `mcp-servers: []` to `mcp-servers: [codegraph]` (design.md names no other MCP server today; do not add servers it does not use). Leave `name`, `description`, `category`, `complexity`, `personas` unchanged. No `allowed-tools` key exists in this command's frontmatter and none is added (reflect.md has none either; it names tools in prose).

### 3.2 New section "Code-graph grounding" (between "Tool Coordination" and "Key Patterns")

Text requirements:

1. Guide pointer: one line, `~/.claude/CODEGRAPH.md` (installed path; no `src/superclaude/` path).
2. Exactly one readiness check per run, at the start of the Analyze step (Behavioral Flow step 1), following the guide's section 2. Record `index_state`, `checked_at`, `worktree_root` and the `projectPath` passed on every call.
3. Use codegraph only when `index_state` is `fresh` and the lookup tools are listed (`access: mcp`). Otherwise continue on Glob/Grep/Read (the existing floor, unchanged), add the matching `graph:*` token (`graph:absent`, `graph:not_initialized`, `graph:stale`, `graph:foreign_index`, `graph:disabled`, `graph:unlisted`, `graph:parse_failed`) and never stop the run.
```

### .dev/tasks/done/TASK-WF-designOutput-20261111-193642/TASK-WF-designOutput-20261111-193642.md:24-47 (both task bodies + all ACs)

```markdown
## Phase 1: Add the codegraph grounding rules

## Task 1: Add the frontmatter entry and the Code-graph grounding section

In `src/superclaude/commands/design.md`, change the frontmatter line `mcp-servers: []` to `mcp-servers: [codegraph]` and leave every other frontmatter key unchanged (no `allowed-tools` key is added). Insert a new `## Code-graph grounding` section between `## Tool Coordination` and `## Key Patterns` (source sections 3.1 and 3.2). It must contain a one-line pointer to `~/.claude/CODEGRAPH.md`; exactly one readiness check per run at the start of the Analyze step (guide section 2), recording `index_state`, `checked_at`, `worktree_root` and the `projectPath` passed on every call; the rule that codegraph is used only when `index_state` is `fresh` and the lookup tools are listed, otherwise the run continues on Glob/Grep/Read, adds the matching `graph:*` token (`graph:absent`, `graph:not_initialized`, `graph:stale`, `graph:foreign_index`, `graph:disabled`, `graph:unlisted`, `graph:parse_failed`) and never stops; and the tool-to-step map. [...] The section ends with the fallback note rule: record the `graph:*` token, or `index_state: fresh` with the tools used, on a `Grounding` line of the design document, and under `--unattended` also in the worker contract's existing degraded list only if that contract defines one.

Acceptance criteria:
- `grep -n 'mcp-servers' src/superclaude/commands/design.md` shows `mcp-servers: [codegraph]` and the other frontmatter keys are unchanged.
- The `## Code-graph grounding` section exists between `## Tool Coordination` and `## Key Patterns` and states exactly one readiness check per run, the fresh-only rule, the Glob/Grep/Read fallback with a recorded `graph:*` token that never halts, and the tool-to-step map for Analyze, Plan/Design and Validate.
- `grep -n 'src/superclaude' src/superclaude/commands/design.md` prints no line that tells an agent to read a `src/superclaude/...` path, and the section names no `codegraph_explore` call or mutating verb other than in a "never" rule.

## Phase 2: Wire the rules into the existing flow and tools

## Task 2: Point Behavioral Flow and Tool Coordination at the new section and run the checks

Depends on: Task 1

[...] add a short clause to Behavioral Flow step 1 (Analyze) and step 4 (Validate) that points to the `Code-graph grounding` section, keeping the five step names and the Key behaviors bullets. Add one bullet to `## Tool Coordination` naming the codegraph tools once (`mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`) as a tier above the floor, leaving the Read, Grep/Glob, Write and Bash bullets unchanged (source section 3.3). Leave Usage, Examples, Unattended mode and Boundaries unchanged. Then run `make sync-dev` and `make verify-sync` from the repository root [...] and run `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py -q`. Write the command output of the sync, verify and pytest runs to `./artifacts/t2-checks.log`.

Acceptance criteria:
- Behavioral Flow steps 1 and 4 and the Tool Coordination section each refer to the codegraph grounding rules, and the Usage flags, Unattended mode section and Boundaries match their text before this change (`git diff src/superclaude/commands/design.md` shows no edit inside them).
- `make sync-dev` and `make verify-sync` both exit 0, and the exit codes are recorded in `./artifacts/t2-checks.log`.
- The four named test files pass with `uv run pytest`, or any failure is shown in `./artifacts/t2-checks.log` and is not attributable to `design.md`.
- `git status --short` shows no staged path under `.claude/`, and `src/superclaude/commands/design.md` is the only source file modified by this plan.
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001: frontmatter mcp-servers: [codegraph] | Task 1 | covered | tasklist:28 |
| INF-002: Code-graph grounding section (7 text reqs) | Task 1 | covered | tasklist:28 |
| INF-003: Behavioral Flow step 1/4 clause | Task 2 | covered | tasklist:41 |
| INF-004: Tool Coordination bullet | Task 2 | covered | tasklist:41 |
