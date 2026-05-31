# Web Research 01: Octocode Tools & Architecture

**Status:** Complete
**Date:** 2026-05-30
**Backend:** Tavily MCP (primary, all sources)

---

## Project Identity

- **Owner/Author:** Guy Bary (@bgauryy) — Software Architect, Tel Aviv
- **Canonical repo:** `github.com/bgauryy/octocode` (URL `bgauryy/octocode-mcp` permanently redirects to `bgauryy/octocode`)
- **License:** MIT, package name `octocode-mcp` on npm
- **Stars / forks at time of research:** 852 stars / 73 forks
- **Latest visible release surface date:** May 23, 2026 (skills/README.md last commit `033149c`)
- **Tagline:** "MCP server for semantic code research and context generation on real-time using LLM patterns | Search naturally across public & private repos based on your permissions | Transform any accessible codebase/s into AI-optimized knowledge on simple and complex flows | Find real implementations and live docs from anywhere"
- **Manifesto line:** "Code is Truth, but Context is the Map." — Research Driven Development philosophy in `MANIFEST.md`

---

## Monorepo Package Map

Octocode is a yarn-workspaces monorepo. The five packages:

| Package | Purpose |
|---|---|
| `octocode-mcp` | MCP server — **14 tools** across GitHub/GitLab/Bitbucket, local FS, LSP |
| `octocode-cli` | CLI — installer, tool runner, skills marketplace |
| `octocode-vscode` | VS Code extension — GitHub OAuth + multi-editor MCP install |
| `octocode-shared` | Shared utilities — credentials, session, platform |
| `octocode-security-utils` | Standalone security utilities |

Docs layout (all monorepo docs live in `docs/`, no per-package `docs/`):

- `docs/configuration/` — install, auth providers, MCP clients, env/config, troubleshooting
- `docs/dev/` — tool/API references, workflows, architecture, contributing, skills
- `docs/specs/` — design specs and RFCs

---

## Tool Inventory (14 tools total)

The MCP server exposes **14 tools** across **3 categories**: 7 code-host (GitHub/GitLab/Bitbucket) tools, 4 local filesystem tools, and 3 LSP semantic tools.

### Master Table

| # | Tool | Category | Purpose | Key Params | Output Shape | Typical Use Case |
|---|---|---|---|---|---|---|
| 1 | `githubSearchCode` | Code-host: Search | Keyword search for code patterns across repos | `keywordsToSearch[]` (1-5), `owner`, `repo`, `extension`, `filename`, `path`, `match` (file/path), `limit`, `page`, **+research context** | `results[]` of `{path, text_matches, lastModifiedAt}`; `repositoryContext.branch` when all hits from one repo | "Find `useState` hooks in TypeScript across React ecosystem"; pre-step before `githubGetFileContent` |
| 2 | `githubSearchRepositories` | Code-host: Search | Discover repos/projects by keywords or topics | `keywordsToSearch[]`, `topicsToSearch[]`, `owner`, `stars` (e.g. `>1000`), `size`, `created`, `updated`, `sort` (forks/stars/updated/best-match), `match` (name/description/readme), `limit`, `page` | Repo metadata list (stars, description, lastUpdated, etc.) | "Find popular TypeScript CLI tools with >1000 stars" |
| 3 | `githubSearchPullRequests` | Code-host: Search | Search GitHub PRs / GitLab MRs / Bitbucket PRs with extensive filters | `prNumber`, `owner`, `repo`, `query`, `state` (open/closed/merged/all), `author`, `assignee`, `label`, `created`, `updated`, `merged`, `draft`, `head`/`base` (or `source`/`target` for GitLab/BB), `type` (metadata/fullContent/partialContent), `withComments`, `withCommits`, `partialContentMetadata[]`, `sort`, `order`, `limit`, `page` | PR metadata/body/diff per `type`. Body auto-truncates at 2000ch (limit=2-3) or 800ch (limit=4+) | "Find merged PRs that changed auth"; targeted-file diff inspection |
| 4 | `githubGetFileContent` | Code-host: Content | Read a file OR fetch directory to disk for local analysis | `owner`, `repo`, `path`, `branch` (auto-`HEAD`), `type` (`file`/`directory`), `fullContent`, `startLine`/`endLine`, `matchString`, `matchStringContextLines`, `charOffset`, `charLength` | File mode: `{content, branch, matchLocations, pagination, isPartial, startLine, endLine}`. Directory mode: `{localPath, fileCount, totalSize, files}` | Read specific function via `matchString`; fetch a dir to disk before LSP analysis (GitHub-only, needs `ENABLE_LOCAL=true` + `ENABLE_CLONE=true`) |
| 5 | `githubViewRepoStructure` | Code-host: Content | Display repository directory tree | `owner`, `repo`, `branch`, `path` (`""` for root), `depth` (1-2), `entriesPerPage`, `entryPageNumber` | Tree with `summary.truncated` flag; ignores `.git`, `node_modules`, `dist` | First-pass codebase exploration; locate monorepo packages |
| 6 | `githubCloneRepo` | Code-host: Content | Clone (full or sparse) a GitHub repo to local FS — **GitHub-only** | `owner`, `repo`, `branch` (auto-detect default), `sparse_path` (partial fetch) | `{owner, repo, branch, localPath, sparse_path?}`. Cache 24h at `~/.octocode/repos/{owner}/{repo}/{branch}/` | Deep LSP analysis of an external repo; uses `git clone --depth 1` shallow clone. Requires `ENABLE_LOCAL=true` + `ENABLE_CLONE=true` |
| 7 | `packageSearch` | Code-host: Package | Lookup npm or PyPI packages → repo URL, version, deprecation | `name`, `ecosystem` (`npm`/`python`), `searchLimit`, `npmFetchMetadata`, `pythonFetchMetadata` | `{repoUrl, version, description, deprecated, alternatives?}` | "Get repo URL for `express`" before `githubViewRepoStructure` |
| 8 | `localSearchCode` | Local: Search | Fast pattern search via bundled ripgrep (`@vscode/ripgrep`) | `pattern`, `path`, `mode` (discovery/paginated/detailed), `filesOnly`, `contextLines`/`beforeContext`/`afterContext`, `type` (ts/js/py/…), `include`/`exclude`/`excludeDir`, `hidden`, `smartCase`, `fixedString`, `perlRegex`, `caseInsensitive`/`caseSensitive`, `wholeWord`, `invertMatch`, `noIgnore`, `followSymlinks`, `multiline`, `multilineDotall`, `count`/`countMatches`, `maxMatchesPerFile`, `maxFiles`, `filesPerPage`/`matchesPerPage`/`filePageNumber`, `sort` (path/modified/accessed/created), `includeStats`, `includeDistribution`, `jsonOutput`, `vimgrepFormat`, `threads`, `mmap`, `verbosity` | Matches with `{value, line (1-idx), column}`; `line` doubles as `lineHint` for LSP | Pre-step before any LSP tool; produces required `lineHint` |
| 9 | `localViewStructure` | Local: Discovery | List directory contents using `ls` with metadata | `path`, `depth` (1-5), `recursive`, `sortBy` (name/size/time/extension), `reverse`, `filesOnly`, `directoriesOnly`, `hidden`, `humanReadable`, `summary`, `pattern`, `extension`/`extensions`, `entriesPerPage`/`entryPageNumber`, `details`, `showFileLastModified`, `limit`, `verbosity` | `entries[]` of `{name, type (file/dir/link), size, modified, permissions}` + one-line summary | Top-down code exploration (`path=/`, `depth=1` → drill in) |
| 10 | `localFindFiles` | Local: Discovery | Find files/dirs via `find` with name + metadata filters | `path`, `name`/`iname`/`names`, `regex`, `regexType` (posix-egrep/extended/basic), `type` (f/d/l/b/c/p/s), `modifiedWithin`/`modifiedBefore`, `accessedWithin`, `sizeGreater`/`sizeLess`, `empty`, `permissions`, `executable`/`readable`/`writable`, `maxDepth`/`minDepth`, `pathPattern`, `excludeDir`, `sortBy` (modified/size/name/path), `limit`, `details`, `filesPerPage`/`filePageNumber`, `charOffset`/`charLength`, `showFileLastModified`, `verbosity` | File path list + metadata when `details=true` | "Find test files modified in last 24h"; locate files by name pattern |
| 11 | `localGetFileContent` | Local: Content | Read file content with targeted extraction — **LAST step** | `path`, `startLine`/`endLine` XOR `matchString` (with `matchStringContextLines`, `matchStringIsRegex`, `matchStringCaseSensitive`) XOR `fullContent`, `charOffset`/`charLength`, `verbosity` | File content slice + pagination metadata | After search + LSP narrow the exact lines; never use for flow analysis |
| 12 | `lspGotoDefinition` | LSP: Semantic | Jump to symbol definition site | `uri`, `symbolName`, `lineHint` (1-indexed, ±2 lines OK), `orderHint` (when symbol repeats), `page`, `charOffset`/`charLength`, `verbosity` | `locations[]` with ranges + snippets in compact mode; `lspMode` indicator | "Where is `handleRequest` defined?"; works on TS/JS bundled, others via PATH or `OCTOCODE_*_SERVER_PATH` |
| 13 | `lspFindReferences` | LSP: Semantic | All usages of a type/interface/variable/constant/function | `uri`, `symbolName`, `lineHint`, `includeDeclaration` (bool), `groupByFile` (force rollup), `referencesPerPage`, `page`, `charOffset`/`charLength`, `verbosity` | `locations[]` with `isDefinition` flag; flat list <500 refs or `topFiles` rollup ≥500 | "All usages of type `UserConfig`"; impact analysis. **Use this — not call hierarchy — for non-callable symbols** |
| 14 | `lspCallHierarchy` | LSP: Semantic | Trace function call relationships (incoming/outgoing) | `uri`, `symbolName`, `lineHint`, `direction` (`incoming`/`outgoing`), `callsPerPage`, `page`, `charOffset`/`charLength`, `verbosity`. Depth capped at 3 | Target item + incoming/outgoing calls + call ranges. Ultra mode → `A → B (×n)` edges | "Who calls `processData`?" (incoming); "what does `fetchData` call?" (outgoing) |

### Universal Conventions Across All Tools

- **Research context (required on every call):** `mainResearchGoal`, `researchGoal`, `reasoning` — required on GitHub/GitLab/Package tools; `researchGoal` + `reasoning` required on local + LSP tools. Used to track research intent and improve result quality.
- **Universal output pagination:** All tools support `charOffset` / `charLength` for response continuation, plus tool-specific paging (`page`, `limit`, `entriesPerPage`, `prNumber`). Default `output.pagination.defaultCharLength = 8000`.
- **Universal `verbosity` parameter** (local + LSP): `compact` (default), `verbose` (currently same as compact), `ultra` (counts + summaries + top hints — drops heavy arrays).
- **Provider parameter mapping (code-host tools):**

| Parameter | GitHub | GitLab | Bitbucket |
|---|---|---|---|
| `owner` | Organization/User | Group/Namespace | Workspace |
| `repo` | Repository | Project Name | Repository Slug |
| `branch` | Branch name | Ref (branch/tag) | Branch name |
| `prNumber` | PR # | MR IID | PR ID |

- **GitHub-only features:** `githubCloneRepo`, `githubGetFileContent` directory mode. GitLab/Bitbucket support file-mode `githubGetFileContent` only.
- **GitLab requires project scope** for `githubSearchCode` (must pass `owner` + `repo`).

### LSP Language Support

| Status | Languages |
|---|---|
| **Bundled** | TypeScript (`.ts`, `.tsx`), JavaScript (`.js`, `.jsx`, `.mjs`, `.cjs`) via bundled `typescript-language-server` |
| **Install required** | Python, Go, Rust, Java, Kotlin, C/C++, C#, Ruby, PHP, Swift, Dart, Lua, Zig, Elixir, Scala, Haskell, OCaml, Clojure, Vue, Svelte, YAML, TOML, JSON, HTML, CSS, Bash, SQL, GraphQL, Terraform |

Override paths via `OCTOCODE_TS_SERVER_PATH`, `OCTOCODE_PYTHON_SERVER_PATH`, `OCTOCODE_GO_SERVER_PATH`, `OCTOCODE_RUST_SERVER_PATH`, `OCTOCODE_JAVA_SERVER_PATH`, `OCTOCODE_CLANGD_SERVER_PATH`. Custom LSP server config via `OCTOCODE_LSP_CONFIG`.

### Canonical Research Flows

The Funnel Method (Core Principle):

```
DISCOVER → SEARCH → LOCATE/ANALYZE → READ
  ▼          ▼            ▼            ▼
Structure  Pattern    Semantic    Implementation
& Scope    Matching   Analysis    Details
```

Cost-stage table:

| Stage | Tools | Algorithm | Purpose |
|---|---|---|---|
| 1. DISCOVER | `localViewStructure`, `localFindFiles` | Tree O(d), Metadata O(1) | Narrow scope 80-90% |
| 2. SEARCH | `localSearchCode` | Inverted index O(1) | Find patterns; **get `lineHint`** |
| 3. LOCATE | `lspGotoDefinition` | Symbol table O(1) | Jump to definition |
| 3. ANALYZE | `lspFindReferences`, `lspCallHierarchy` | Graph DFS/BFS | Usage & call flow |
| 4. READ | `localGetFileContent` | I/O | Implementation (LAST!) |

Common flows:

- **"How does package X work?"** → `packageSearch` → `githubViewRepoStructure` → `githubSearchCode` → `githubGetFileContent`
- **"Why was code changed this way?"** → `githubSearchCode` → `githubSearchPullRequests` (metadata first, then partialContent) → `githubGetFileContent`
- **"Deep analysis of external repo with LSP"** → `githubCloneRepo(sparse_path=…)` → `localSearchCode` (gets `lineHint`) → `lspGotoDefinition` → `lspCallHierarchy`
- **"Impact analysis"** → `localSearchCode` → `lspGotoDefinition` → `lspFindReferences(includeDeclaration=false)` → `lspCallHierarchy(incoming, depth=2)`

### Critical Rules (from official docs)

1. **Local code → never use `github*` tools. Use `localSearchCode` → LSP.**
2. **Package first for external deps:** `packageSearch(name="express")` before `githubViewRepoStructure`, not `githubSearchRepositories(keywordsToSearch=["express"])`.
3. **Start lean with filters** — search APIs fail with too many combined filters.
4. **Metadata first for PRs/MRs** — `type="metadata"` before `partialContent` before `fullContent`.
5. **Prefer `matchString` for large files** over `fullContent=true`.
6. **GitLab code search needs scope** — must specify `owner` + `repo`.
7. **Clone & directory fetch are GitHub-only** — error on GitLab/Bitbucket.
8. **LSP tools require `lineHint`** (1-indexed); get it from `localSearchCode`.
9. **`localGetFileContent` is LAST** — only read after search + LSP narrow exact lines.
10. **Don't use `lspCallHierarchy` on types** — fails; use `lspFindReferences`.

---

## Architecture

### Authentication Model (zero-API-key path)

- **Three GitHub auth paths**, in priority order: `OCTOCODE_TOKEN` (highest), `GITHUB_TOKEN`, `GH_TOKEN` (GitHub CLI compatible).
- **Default user-facing flow:** `npx octocode-cli` triggers GitHub OAuth-style setup CLI to create the token. Alternative: `gh auth login` (GitHub CLI). Alternative: manual Personal Access Token at `github.com/settings/tokens` with scopes `repo`, `read:user`, `read:org`.
- **GitHub Enterprise:** `GITHUB_API_URL` env var.
- **GitLab:** `GITLAB_TOKEN` or `GL_TOKEN` (fallback), `GITLAB_HOST` for self-hosted (default `https://gitlab.com`).
- **Bitbucket:** `BITBUCKET_TOKEN` or `BB_TOKEN`, `BITBUCKET_USERNAME` (enables Basic auth; omit for Bearer), `BITBUCKET_HOST` (default `https://api.bitbucket.org/2.0`).
- **Provider auto-detection priority:** GitLab → Bitbucket → GitHub. **Single active provider per server instance**.
- **Read-only by design:** "Octocode is **read-only** — it never writes to GitHub."

### Local Execution Model

- **Distribution:** npm package `octocode-mcp`, run via `npx octocode-mcp@latest`.
- **Runtime:** Node.js ≥ v20.0.0 required.
- **Ripgrep:** Bundled via `@vscode/ripgrep` — works identically on macOS/Linux/Windows with no extra install.
- **LSP runtime:** Pure Node.js. Language servers managed by a per-project pool that keeps them warm across requests.
- **`localFindFiles` + `localViewStructure`** use POSIX `find` and `ls` — macOS/Linux out of the box; on Windows requires Git Bash or WSL.
- **Clone cache:** `~/.octocode/repos/{owner}/{repo}/{branch}/` — 24-hour TTL; shallow clones (`git clone --depth 1`); sparse-checkout for monorepo subdirs.

### Workspace & Security Boundaries

- **`WORKSPACE_ROOT`** env var (default: `cwd`) — root directory for local tools.
- **`ALLOWED_PATHS`** comma-separated whitelist restricting local FS access (default: all).
- **LSP workspace inference:** Files inside `WORKSPACE_ROOT` use it; external paths infer nearest project root (looks for `package.json`, `tsconfig.json`, `.git`, `Cargo.toml`, `go.mod`, `pyproject.toml`).
- **LSP security:** File reads stay inside allowed roots, symlinks resolved before access, paths redacted in errors, symbol length capped, call hierarchy depth capped at 3.
- **Local + LSP gated by:** `ENABLE_LOCAL=true`.
- **Cloning + directory mode gated by:** `ENABLE_CLONE=true` AND `ENABLE_LOCAL=true`.

### Tool Filtering & Hardening

- `TOOLS_TO_RUN` — strict whitelist; only listed tools available.
- `DISABLE_TOOLS` — comma-separated removal.
- `DISABLE_PROMPTS` — disables built-in prompt templates.

### Response Optimization (token efficiency)

Every response strips internal fields (`contentLength`, `cached`, `expiresAt`, `searchEngine` rollups, `milestone`/`review_comments` noise, `id`, `html_url`, `head_sha`, `base_sha` per record). PR body auto-truncates by batch size. Truncated bodies include a hint to fetch the full body by PR number.

---

## Setup & Install

### Quick install (recommended path)

Two steps:

**Step 1 — Connect GitHub:**

```bash
npx octocode-cli
```

(or `gh auth login` if GitHub CLI installed; or set `GITHUB_TOKEN=ghp_...` for manual PAT.)

**Step 2 — Add MCP server** (works with any MCP host):

```json
{
  "octocode": {
    "command": "npx",
    "args": ["octocode-mcp@latest"]
  }
}
```

### Host-specific installs

- **Cursor:** One-click `cursor.com/en-US/install-mcp?name=octocode&config=…`
- **Claude Code:** `claude mcp add -s user octocode npx 'octocode-mcp@latest'`
- **VS Code:** `vscode:mcp/install?…` URI or install the **Octocode VS Code extension** from marketplace (`AISideKick.octocode-mcp`)

### Environment variables (complete reference table)

| Variable | Description | Default |
|---|---|---|
| `GITHUB_TOKEN` | GitHub personal access token | — |
| `OCTOCODE_TOKEN` | Octocode-specific token (highest priority) | — |
| `GH_TOKEN` | GitHub CLI compatible token | — |
| `GITLAB_TOKEN` / `GL_TOKEN` | GitLab PAT (activates GitLab mode) | — |
| `BITBUCKET_TOKEN` / `BB_TOKEN` | Bitbucket app password / OAuth token | — |
| `BITBUCKET_USERNAME` | Bitbucket username (enables Basic auth) | — |
| `GITHUB_API_URL` | GitHub Enterprise API endpoint | `api.github.com` |
| `GITLAB_HOST` | Self-hosted GitLab URL | `gitlab.com` |
| `BITBUCKET_HOST` | Bitbucket API endpoint | `https://api.bitbucket.org/2.0` |
| `ENABLE_LOCAL` | Enable local FS & LSP tools | `true` |
| `ENABLE_CLONE` | Enable `githubCloneRepo` + directory-mode `githubGetFileContent` | — |
| `WORKSPACE_ROOT` | Root dir for local tools | `cwd` |
| `ALLOWED_PATHS` | Restrict local access (comma-separated) | all |
| `TOOLS_TO_RUN` | Strict tool whitelist | all |
| `DISABLE_TOOLS` | Remove specific tools | — |
| `DISABLE_PROMPTS` | Disable built-in prompt templates | `false` |
| `OCTOCODE_HOME` | Home dir for caches/stats | `~/.octocode` |
| `OCTOCODE_LSP_CONFIG` | Path to LSP-server config JSON | — |
| `OCTOCODE_TS_SERVER_PATH` | Override TS/JS language server binary | — |
| `OCTOCODE_PYTHON_SERVER_PATH` | Override Python LSP | — |
| `OCTOCODE_GO_SERVER_PATH` | Override Go LSP | — |
| `OCTOCODE_RUST_SERVER_PATH` | Override Rust LSP | — |
| `OCTOCODE_JAVA_SERVER_PATH` | Override Java LSP | — |
| `OCTOCODE_CLANGD_SERVER_PATH` | Override C/C++ LSP | — |

### Common troubleshooting

- **Node version:** ≥ v20.0.0 (`node --version`)
- **Auth not working:** Re-run `npx octocode-cli` and select "Login to GitHub". On Windows, prefer PAT in `GITHUB_TOKEN` env.
- **NPM cache:** `npm cache clean --force`. Diagnostic: `npx node-doctor info`.

---

## Skills Marketplace

Octocode bundles a **skills system** — 19 specialized AI agent skills under `skills/`, each in its own subdirectory following the `SKILL.md` format.

### Complete skill inventory (19 skills)

| Skill | Directory | Purpose |
|---|---|---|
| Install | `octocode-install/` | Set up OctoCode, auth, IDE MCP, and skills |
| CLI | `octocode-cli/` | Run Octocode tools from the shell (without wiring MCP) |
| Researcher | `octocode-researcher/` | Default targeted research skill — fast code search, symbol lookup, file discovery, local/GitHub exploration |
| Research | `octocode-research/` | Stateful **multi-phase** investigations with checkpoints + evidence synthesis |
| Brainstorming | `octocode-brainstorming/` | Evidence-first idea validation across GitHub, package ecosystems, web sources → decision brief |
| Plan | `octocode-plan/` | Turn researched context into implementation steps, risks, tests, execution order |
| RFC Generator | `octocode-rfc-generator/` | Technical decision docs — alternatives, trade-offs, recommendation, rollout plan |
| Engineer | `octocode-engineer/` | Architecture-aware engineering — exploration, coding, analysis, audits, refactors |
| PR Reviewer | `octocode-pull-request-reviewer/` | Holistic review of remote PRs or local diffs |
| Roast | `octocode-roast/` | Entertaining, severity-ranked critique with concrete fixes |
| Prompt Optimizer | `octocode-prompt-optimizer/` | Improve long prompts and agent instructions |
| Design | `octocode-design/` | UI/design-system guidance — dynamic `DESIGN.md` generator |
| Doc Writer | `octocode-documentation-writer/` | Documentation pipeline — onboarding, architecture, APIs, workflows |
| News | `octocode-news/` | Scan recent AI/devtools/web/security updates into a concise report |
| Search Skill | `octocode-search-skill/` | Search GitHub for `SKILL.md` files, score relevance, preview, download skill folders |
| Chrome DevTools | `octocode-chrome-devtools/` | CDP-level browser debugging |
| Agentic Flow Best Practices | `agentic-flow-best-practices/` | Design agentic workflow patterns |
| Slides | `octocode-slides/` | Polished multi-file HTML presentations via 6-phase design flow |
| Stats | `octocode-stats/` | Local HTML dashboard from `${OCTOCODE_HOME}/stats.json` |

### How Skills Ship

- **Format:** Each skill is a directory with a `SKILL.md` file
- **Composition:** Skills may include `references/`, `paths/`, sub-flows, and prompt templates
- **Install vectors:**
  1. **CLI:** `npx add-skill <name>` — direct install
  2. **Search Skill** (meta-skill): `octocode-search-skill` searches GitHub for `SKILL.md` files
  3. **VS Code extension** can wire MCP install across editors

---

## Differentiators

### vs plain GitHub MCP server

| Dimension | Octocode | Standard GitHub MCP |
|---|---|---|
| Tool surface | 14 tools across 3 categories (code-host + local FS + LSP) | Typically GitHub API mirrors (issues, PRs, repos) |
| **Semantic understanding** | LSP-backed | Text-only |
| **Local + remote unified** | One server handles both | Local FS not in scope |
| **Multi-provider** | GitHub + GitLab + Bitbucket | GitHub-only |
| **Token efficiency** | Body auto-truncation, `verbosity` levels, response field stripping | Returns raw API JSON |
| **Research context required** | `mainResearchGoal`/`researchGoal`/`reasoning` on every call | None |
| **Package discovery** | `packageSearch` resolves npm/PyPI → repo URL | Manual |

### vs GitHub CLI (`gh`)

| Dimension | Octocode | `gh` CLI |
|---|---|---|
| Surface | MCP tools + LLM-optimized output | Human-oriented terminal commands |
| Auth | Reuses `gh` token via `GH_TOKEN`, plus its own | Native |
| LSP | Yes | No |
| GitLab/Bitbucket | Yes (unified schema) | No |
| Local FS | Yes (`localSearchCode` etc.) | No |
| Cache | 24h repo cache | Per-command |

### Unique design choices

1. **"Research Driven Development" (RDD) manifesto** — `MANIFEST.md` codifies a philosophy: "Code is Truth, but Context is the Map." Tools enforce `researchGoal` + `reasoning` on every call.
2. **`open-docs` sibling repo** — bgauryy maintains `bgauryy/open-docs` which uses Octocode to reverse-engineer documentation for Claude Agent SDK, Gemini CLI, Codex CLI, OpenCode, Pi Coding Agent.
3. **19-skill marketplace + meta search** — `octocode-search-skill` searches GitHub for `SKILL.md` files. This is a discoverable, decentralized skill registry pattern.
4. **CLI-vs-MCP benchmark as a feature** — published benchmark comparing throughput between direct CLI execution and MCP routing.
5. **VS Code extension as multi-editor installer** — installs the MCP server automatically on Windsurf, Cursor forks, and other VS Code-based editors.

---

## Source URLs (Citation Table)

| # | URL | Title | Credibility |
|---|---|---|---|
| S1 | https://github.com/bgauryy/octocode-mcp | Main README | Primary (author) |
| S2 | https://github.com/bgauryy/octocode/blob/main/docs/README.md | Docs index | Primary |
| S3 | https://github.com/bgauryy/octocode-mcp/blob/main/docs/dev/reference/GITHUB_GITLAB_TOOLS_REFERENCE.md | GitHub/GitLab/Bitbucket tools reference | Primary (canonical) |
| S4 | https://github.com/bgauryy/octocode-mcp/blob/main/docs/dev/reference/LOCAL_TOOLS_REFERENCE.md | Local + LSP tools reference | Primary (canonical) |
| S5 | https://github.com/bgauryy/octocode-mcp/blob/main/skills/README.md | Skills marketplace index | Primary |
| S6 | https://octocode.ai/installation | Official install guide | Primary (vendor) |
| S7 | https://mcp.so/server/octocode/bgauryy | MCP.so directory listing | Tertiary catalog |
| S8 | https://glama.ai/mcp/servers/bgauryy/octocode | Glama MCP directory | Tertiary catalog |
| S9 | https://news.ycombinator.com/item?id=45796836 | HN launch thread by bgauryy | Author commentary |
| S10 | https://gist.github.com/bgauryy/216fb26205138f0b455a15d09f4fb22c | OCTOCODE_CURSOR_LOCAL_COMPARISON | Author benchmark |

---

## Open Questions / Suggested Follow-Up

1. **No exhaustive return-shape JSON schemas observed.** The docs describe response fields conversationally; precise types would require introspecting the actual MCP `tools/list` and `tools/call` JSON.
2. **`docs/specs/` RFCs not enumerated** in this pass.
3. **Privacy claims** — `PRIVACY.md` and `TERMS.md` were not directly fetched.
4. **Concrete version pin** — findings reflect the `main` branch as of May 23, 2026.

## Status: Complete
