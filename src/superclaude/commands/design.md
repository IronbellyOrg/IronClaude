---
name: design
description: "Design system architecture, APIs, and component interfaces with comprehensive specifications"
category: utility
complexity: basic
mcp-servers: [codegraph]
personas: []
---

# /sc:design - System and Component Design

## Triggers

- Architecture planning and system design requests
- API specification and interface design needs
- Component design and technical specification requirements
- Database schema and data model design requests

## Usage

```
/sc:design [target] [--type architecture|api|component|database] [--format diagram|spec|code]
/sc:design [target] [--output <file>] [--unattended] [--report-dir <dir>]
```

`--output <file>` writes the design document to that file. A standalone run writes a file only when you pass it.

## Behavioral Flow

1. **Analyze**: Examine target requirements and existing system context (run the once-per-run readiness check and ground the design in the real code, see Code-graph grounding)
2. **Plan**: Define design approach and structure based on type and format
3. **Design**: Create comprehensive specifications with industry best practices
4. **Validate**: Ensure design meets requirements and maintainability standards (confirm names, signatures and consumers against the existing code, see Code-graph grounding)
5. **Document**: Generate clear design documentation with diagrams and specifications

Key behaviors:

- Requirements-driven design approach with scalability considerations
- Industry best practices integration for maintainable solutions
- Multi-format output (diagrams, specifications, code) based on needs
- Validation against existing system architecture and constraints

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

## Key Patterns

- **Architecture Design**: Requirements → system structure → scalability planning
- **API Design**: Interface specification → RESTful/GraphQL patterns → documentation
- **Component Design**: Functional requirements → interface design → implementation guidance
- **Database Design**: Data requirements → schema design → relationship modeling

## Examples

### System Architecture Design

```
/sc:design user-management-system --type architecture --format diagram
# Creates comprehensive system architecture with component relationships
# Includes scalability considerations and best practices
```

### API Specification Design

```
/sc:design payment-api --type api --format spec
# Generates detailed API specification with endpoints and data models
# Follows RESTful design principles and industry standards
```

### Component Interface Design

```
/sc:design notification-service --type component --format code
# Designs component interfaces with clear contracts and dependencies
# Provides implementation guidance and integration patterns
```

### Database Schema Design

```
/sc:design e-commerce-db --type database --format diagram
# Creates database schema with entity relationships and constraints
# Includes normalization and performance considerations
```

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:design` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** `--report-dir <dir>` only (`--output` is file-valued). Without it the run is refused before any work and the refusal is printed in chat only. A directory inside `.git/` or `.codegraph/`, one under the distributable skill, agent or command folders of a `.claude/` folder, or one that cannot be created or written, counts as no report directory known (refusal printed in chat only).
- **Contract.** `<report-dir>/return-contract.yaml` is written on every outcome. `report_path` is the `--output` file, or `<report-dir>/design-report.md` when `--output` is absent. The run is succeeded when the design document is written, and failed otherwise.
- **Gates.** There is no gate, and no person-mode flag. Under `--unattended` consent is never given: the rule "without explicit design approval" is not answered by assuming approval, so the command changes no existing architecture, and it still generates no implementation code.
- **Nested invocations.** None.
- **Outward actions.** It pushes, commits and stages nothing.

## Boundaries

**Will:**

- Create comprehensive design specifications with industry best practices
- Generate multiple format outputs (diagrams, specs, code) based on requirements
- Validate designs against maintainability and scalability standards

**Will Not:**

- Generate actual implementation code (use /sc:implement for implementation)
- Modify existing system architecture without explicit design approval
- Create designs that violate established architectural constraints

**Output**: Architecture documents containing:

- System diagrams (component, sequence, data flow)
- API specifications
- Database schemas
- Interface definitions

**Next Step**: After design is approved, use `/sc:implement` to build the designed components.
