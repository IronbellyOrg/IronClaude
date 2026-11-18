# Reviewer brief — reviewer-3 (persona: refactorer, model class: opus, model: claude-opus-5-5)

You audit a workflow-plan package (UC-1 pre-execution audit of a tasklist against its driving spec). Repository root: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel`. The package is archived; the planned change already landed. Your lens: structural quality of the plan — spec-to-task traceability, AC verifiability, drift between plan and shipped state.

## T1 card excerpt

(from `<output>/t1-card.md`, refactorer slice)

## Grounded observations (structural)
3. Shipped-file divergence (advisory): design.md:65 adds "codegraph_impact only if it was not already run for the same symbol in Plan or Design" — a refinement beyond spec §3.2 item 4's unconditional "callers and impact". The tasklist (line 28) is faithful to the spec, not the refinement; commit 930c5ebc8 landed after the plan. Amendment-propagation class (2nd sighting per shadow11).
4. Task 2 AC3 escape-hatch ("or any failure ... is not attributable to design.md"): attribution judgment makes the AC unable to fail mechanically. Latent only.
5. Task 2 AC1 baseline-diff requirement vs archived package: no before-state exists; contemporaneous artifacts substitute.

## T1 conclusion
Plan is a faithful, near-verbatim expansion of the spec. Known latent AC weaknesses are documented classes, not live failures.

End your card with a ## Findings block holding one fenced findings-v2 block: JSON lines, one object per line, never a table. Fields: id (F1, F2, ...), severity (CRITICAL, MAJOR or MINOR), blocking (true or false; a MINOR finding is never blocking), category (one of contradiction, data-loss, missing-requirement, other, safety, unpassable-check), lens "reflect-pre", claim (one line, at most 300 characters), refs (requirement ids, may be empty) and citations (1 to 8 objects, each with role plan or spec, a repo-relative path, line_start, line_end and an optional quote). Example line: {"id":"F1","severity":"MAJOR","blocking":false,"category":"contradiction","lens":"reflect-pre","claim":"Task 3 says X but task 5 says Y.","refs":["R-1"],"citations":[{"role":"plan","path":"plan.md","line_start":10,"line_end":12}]}. After the block add a reviewer_model_self_report line stating the model you are running as in one line.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-13T01:59:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### src/superclaude/commands/design.md:43-74 (shipped Tool Coordination bullet + full Code-graph grounding section)

```markdown
## Tool Coordination

- **Read**: Requirements analysis and existing system examination
- **Grep/Glob**: Pattern analysis and system structure investigation (the floor for every step)
- **codegraph** (`mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`): one readiness check, then symbol, caller and impact lookups above the Grep/Glob/Read floor when `index_state` is `fresh` (guide `~/.claude/CODEGRAPH.md`, read before the first codegraph call)
- **Write**: Design documentation and specification generation
- **Bash**: External design tool integration when needed

## Code-graph grounding

Rules: read `~/.claude/CODEGRAPH.md` before the first codegraph call. Glob, Grep and Read stay the floor for every step; codegraph is a tier above that floor, never a replacement.

**Readiness check, once per run.** At the start of Analyze, run the readiness check of that guide (its section 2) exactly once: on the MCP path it first waits up to 60 s for a running `init` or `index` (guide step 3), and `checked_at` comes from one `date -u +%Y-%m-%dT%H:%M:%SZ` Bash run right after the single `codegraph_status` call. Record `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass on every codegraph call. No later step repeats the check: the run reads code and writes only the design document.

**Use codegraph only when `index_state` is `fresh`** and the lookup tools are listed. For any other state (`stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`, or lookup tools not listed), continue every step on Glob, Grep and Read and record the matching token from the guide's section 3 (`graph:stale`, `graph:not_initialized`, `graph:foreign_index`, `graph:absent`, `graph:disabled`, `graph:unlisted`, `graph:parse_failed`) in the Grounding line below. The run never stops and never asks the user because of codegraph. A single lookup that fails or returns nothing falls back to the floor for that lookup in the same way, and the matching token (`graph:empty`, `graph:truncated` for a short caller list, or `graph:unresolved` for a row you could not confirm) goes in the Grounding line.

| Step | Design question | Codegraph tool (each call passes `projectPath`) |
|------|-----------------|--------------------------------------------------|
| Analyze | What structure already exists? | `codegraph_files {format:"grouped", maxDepth:2, path}` with `path` set to the target's directory when it is narrower than the repo |
| Analyze | Which existing interfaces, types and symbols should the design reuse? | `codegraph_search {query, kind?}`, `codegraph_node {symbol, includeCode:true}`, `codegraph_node {file, symbolsOnly:true}` for a file outline |
| Plan, Design | Who uses the component or API being designed or changed, and what does it use? | `codegraph_callers {symbol, limit:20}`, `codegraph_callees {symbol}` |
| Plan, Design | What does a change to an existing interface reach (blast radius)? | `codegraph_impact {symbol, depth:2}` before the design proposes the change |
| Validate | Do the names, layering and signatures in the design exist and match the current structure, and does no consumer break? | `codegraph_search`, `codegraph_node`, then `codegraph_callers` for the consumers, and `codegraph_impact` only if it was not already run for the same symbol in Plan or Design |

Rules for graph answers:

- A graph answer locates code; it is not a citation. Read the file range before the design quotes a `file:line`.
- An empty result never proves absence: no "no callers" or "nothing reuses this" conclusion comes from a graph result alone.
- Caller rows give the caller's definition line; confirm the call site (guide section 5) before citing it.
- Never call `codegraph_explore`, never use `codegraph_node` in file mode without `symbolsOnly:true`, and never run a mutating codegraph verb or `codegraph init`.

**Grounding line.** The design document carries one `Grounding:` line: `index_state: fresh` with the codegraph tools used, or the `graph:*` token that sent the run to the floor; with `--format code` or `--format diagram` it is the first comment line or a caption line of the output. Under `--unattended` the line stays in the design report and the worker contract gets no new field.
```

### .dev/tasks/done/TASK-WF-designOutput-20261111-193642/TASK-WF-designOutput-20261111-193642.md:15-47 (full tasklist)

```markdown
Source: ./source.md
Goal: `src/superclaude/commands/design.md` runs one codegraph readiness check per run, uses codegraph above the Glob/Grep/Read floor only when `index_state` is `fresh`, and otherwise falls back to Glob/Grep/Read with a recorded `graph:*` note, without changing any existing flag, behaviour or Boundary.

## Constraints

- Edit only `src/superclaude/commands/design.md`. No backing skill is created. Tests that pin that file change only if they must. Do not edit `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or anything under `.claude/`.
- The installed command must not tell an agent to read a `src/superclaude/...` path; the guide is named `~/.claude/CODEGRAPH.md`.
- No commit, no push, no PR, and no `git add` of `.claude/` contents. Staging and committing are left to the coordinator.
- The Unattended mode section (including its `.codegraph/` report-directory exclusion), the Usage flags and the Boundaries stay as they are. `tests/skills/test_worker_contract.py` pins the phrases `design-report.md`, `no gate` and `consent is never given` for design; they must remain.

[Task 1 and Task 2 bodies and acceptance criteria as materialized in reviewer-1's brief]
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-002: Code-graph grounding section (7 text reqs) | Task 1 | covered | tasklist:28 |
| INF-005: edit-only-design.md constraint | Task 1+2 | covered | tasklist:19-22 |
| INF-006: one readiness check, fresh-only, fallback tokens | Task 1 | covered | tasklist:28 |
| INF-008: sync/verify/pytest checks | Task 2 | covered | tasklist:41-46 |
