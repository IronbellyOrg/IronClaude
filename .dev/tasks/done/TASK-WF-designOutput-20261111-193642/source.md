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
4. Which tool for which step (all calls above the floor, with `projectPath`):
   - Analyze (step 1), existing system context: `codegraph_files {format:"grouped", maxDepth:2}` for structure; `codegraph_search {query, kind?}` to find existing interfaces, types and symbols the design should reuse; `codegraph_node {file, symbolsOnly:true}` for a file outline; `codegraph_node {symbol, includeCode:true}` for a signature to reuse.
   - Plan/Design (steps 2-3), blast radius of the component or API being designed or changed: `codegraph_callers {symbol, limit:20}` and `codegraph_callees {symbol}` for who depends on it and what it depends on; `codegraph_impact {symbol, depth:2}` before proposing any change to an existing interface.
   - Validate (step 4), conformance to existing structure: `codegraph_search` and `codegraph_node` to confirm names, layering and signatures in the design exist and match; callers and impact to confirm no consumer is broken.
5. Rules: a graph answer is a lead, not a citation: Read the file range before quoting a `file:line` in the design. Empty result is not absence (no "no callers" conclusion from the graph). Caller rows give the definition line: confirm the call site before citing it (guide section 5). Never `codegraph_explore`, never `codegraph_node` file mode without `symbolsOnly:true`, never a mutating verb, never `codegraph init` (guide section 7). Design is read-only against the index, so no re-check after writing the design document.
6. Fallback note: record the `graph:*` token (or `index_state: fresh` with the tools used) in a `Grounding` line of the design document. Under `--unattended`, also add it to `return-contract.yaml` as the existing `degraded` list the worker contract defines, only if the contract has that field; otherwise only the `Grounding` line.
7. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` yields `graph:disabled` via the guide's check.

### 3.3 Edits to existing sections

- Behavioral Flow step 1 and step 4: add a short clause pointing to the Code-graph grounding section. Keep the five step names and the "Key behaviors" bullets.
- Tool Coordination: add one bullet for the codegraph tools (names listed once: `mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`) and keep the Read, Grep/Glob, Write, Bash bullets unchanged.
- Boundaries: unchanged except the existing "Will" list gains nothing; add no new Will Not.
- Unattended mode: unchanged. The `.codegraph/` report-directory exclusion stays.

## 4. Interfaces and contracts

- Input: unchanged (`[target] [--type ...] [--format ...] [--output <file>] [--unattended] [--report-dir <dir>]`). No new flag.
- Output: the design document gains one `Grounding` line (index_state or `graph:*` token). Nothing else changes.
- Readiness state flows only within the run; no agent is spawned by this command, so no brief carries it.

## 5. Constraints

- Edit only `src/superclaude/commands/design.md`. A test that pins it may change only if it must (`tests/skills/test_worker_contract.py` pins the phrases `design-report.md`, `no gate`, `consent is never given`; all stay).
- `grep -n 'src/superclaude' src/superclaude/commands/design.md` must show no read-instruction hit.
- Then `make sync-dev` and `make verify-sync` pass; never stage `.claude/`.

## 6. Acceptance criteria

1. design.md instructs exactly one codegraph readiness check per run and maps tools to steps (section 3.2 item 4).
2. Codegraph used only when `index_state: fresh`; otherwise Glob/Grep/Read with a recorded `graph:*` note; never halts.
3. Frontmatter lists `codegraph` in `mcp-servers`; Tool Coordination names the codegraph tools as reflect.md does.
4. No new `src/superclaude` read-instruction in design.md.
5. `make sync-dev` and `make verify-sync` pass.
6. The related tests pass (`tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`, `tests/core/test_how_we_work_routing_table.py`, `tests/recommend/test_routing_refresh.py`).

## 7. Risks

- Other sessions edit the same checkout: `verify-sync` may name files this change does not own; re-run `make sync-dev` once and never edit them.
- A worker-contract test may pin frontmatter or section order; run it after the edit.
