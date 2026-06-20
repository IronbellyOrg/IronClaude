# `--plugin` Mode — Ecosystem Search Targets

Reference for SKILL.md Phase 3. When `--plugin` is set, the skill ignores the local surface and searches the plugin / community-skill ecosystem instead.

## Scope (this configuration)

In-scope:

- **Claude Code plugin marketplaces** — `claude-plugins-official` (Anthropic-curated marketplace), other listed Claude Code plugin marketplaces the user has installed.
- **Community skill repositories** — `anthropic/skills` (Anthropic's reference skill collection), `sammcj/agentic-tools`, `obra/skills` and similar known community skill catalogs surfaced by web search.

Out-of-scope (this configuration):

- Raw MCP server marketplaces (`mcpservers.org`, `mcp.directory`, `lobehub`, `smithery`). MCP servers are a different abstraction from Claude Code plugins / skills; the user did not opt in. Do **not** surface MCP servers under `--plugin` unless the user explicitly asks for one in their original request, in which case label them clearly as MCP servers (not as plugins or skills) in the output.

If the user changes their mind mid-session and says "actually include MCP servers", add `mcpservers.org` and `mcp.directory` to the next invocation's scope without prompting.

## Search priority

Use, in order:

1. **`tech-research` skill** — preferred when the user wants depth (compatibility checks, version pinning, multiple candidates compared). Hand off via a refined prompt; do not run it inline.
2. **`deep-research` agent** — when the user wants a single focused answer (e.g., "find one good Notion plugin"). One `Agent` call.
3. **Tavily MCP directly** (`mcp__tavily__tavily-search`, `mcp__tavily__tavily-extract`) — when the search is shallow and `tech-research` overhead is not justified.
4. **WebFetch / WebSearch** — last-resort fallback. Tavily generally has better signal-to-noise for plugin discovery.

The skill itself does **not** run the search inline. It generates the refined prompt that delegates the search, following the same hand-off discipline as Phase 2.

## Query patterns

Shape the search query around what makes a plugin recommendation actionable: install command, repo URL, version, last activity, integration cost.

Example queries the recommended prompt can use:

- `Claude Code plugin marketplace <capability>` — for marketplace plugins.
- `site:github.com/anthropics/skills <capability>` — for Anthropic-published skills.
- `claude-plugins-official <capability>` — for the curated marketplace.
- `<capability> claude code skill OR plugin` — general fallback.

For a Notion-integration example (`--plugin: find an MCP server for Notion` — user explicitly asked for an MCP server, so the scope opens):

- `notion mcp server claude code` → ranks notion-mcp servers
- `notion integration claude code plugin` → ranks plugins
- `site:github.com notion-mcp-server` → finds the canonical repo

## Result format (per candidate)

Every plugin / skill returned to the user must include:

| Field | Source | Notes |
|---|---|---|
| Name | repo / marketplace listing | Canonical name |
| Capability summary | repo README first paragraph | One sentence, in the user's terms |
| Install command | repo README / marketplace listing | **Single-line bash** (project memory: no heredocs) |
| Repo URL | search result | Direct link to the source |
| Stars | GitHub repo metadata / API | Own-repo GitHub star count + its source URL. Drives the `--minstar` floor + star-descending sort. `n/a — <curated\|non-github\|nested>` for bonus candidates with no own-repo count. |
| Integration notes | README / docs | What the user needs to configure (auth, env vars, manifest entries) |
| Version / last commit | repo metadata | Stale repos > 1 year without commits → flag explicitly |
| Compatibility caveats | issues, README disclaimers | Known breakages, Claude Code version pins |
| Citation | source URL | Where the claim came from |

If the search returns multiple credible candidates, list the top 3 with a one-line "pick this if..." disambiguator. Do not flatten them into a vague list.

If the search finds nothing credible:

- For marketplace plugins: say so; recommend the user check the official marketplace browser (or invoke `tech-research` with a wider query).
- For community skills: say so; suggest building a custom skill via `skill-creator`.

## Output template (per candidate)

```text
Plugin: <name>
Stars: <count> (<source URL>)
Capability: <one-sentence summary>
Install: `<single-line bash command>`
Repo: <URL>
Version / activity: <last commit date or version pin>
Integration notes: <what to wire up>
Caveats: <any>
Source: <citation URL>
```

For a bonus (unranked) candidate, the `Stars` line reads `Stars: n/a — <curated|non-github|nested>` and the candidate appears under the bonus section (see below), not the primary list.

For multi-candidate output:

```text
Top picks for "<user request>":

1. <name> — pick this if <one-line disambiguator>.
   [full record block above]

2. <name> — pick this if <one-line disambiguator>.
   [full record block above]

3. <name> — pick this if <one-line disambiguator>.
   [full record block above]
```

## `--minstar` floor + two-tier output

`--minstar <N>` (default **500**, applied even when omitted; `--minstar 0` disables) sets a minimum GitHub-star floor on `--plugin` candidates. The delegated search MUST be instructed to capture each candidate's own-repo star count + source URL so the floor and sort can be enforced on the returned set.

Split the returned candidates into two sections:

1. **Primary** — candidates whose own-repo GitHub star count is `>= N`. Sort **by stars descending**. Apply the existing top-3 discipline. Each record shows the `Stars` field with its source URL.
2. **Bonus — not ranked by GitHub stars** — credible candidates with **no own-repo star count**. These are **never filtered by the floor** (the floor only applies to candidates that have a GitHub star count). Label each with the reason it is unranked:
   - `curated` — Anthropic-curated marketplace entry (no GitHub stars by design)
   - `non-github` — the source is not a GitHub repo (or its star count was unreachable at lookup time)
   - `nested` — the skill/plugin lives inside a larger repo; the repo's stars are not attributable to this component (e.g. a single skill inside `anthropic/skills`)

   Apply the same top-3 discipline to the bonus list.

Output layout:

```text
Top picks for "<user request>" (>= <N> stars, sorted by stars):

1. <name> — <stars> stars — pick this if <disambiguator>.
   [full record block]
...

Bonus — not ranked by GitHub stars (curated / non-GitHub / nested-in-larger-project):

1. <name> — unranked: <curated|non-github|nested> — pick this if <disambiguator>.
   [full record block, Stars: n/a — <reason>]
...
```

If the floor removes every GitHub candidate but bonus candidates remain, show the bonus section with a one-line note: `"No candidate met the >= N star floor; showing unranked credible matches below. Lower the floor with --minstar <smaller>."` If nothing credible survives at all, fall back to the "found nothing credible" guidance above.

## Citation discipline

Every claim about a plugin (capability, install command, version) must include the URL it came from. Do not synthesize plausible-sounding install commands. If the README does not give an install command, say "install instructions unclear from README; check repo directly: <URL>" — the user prefers an honest gap over an invented command that does not work.

## Anti-bleed

`--plugin` mode never surfaces local skills, commands, or agents in its output. The user opted out of the local surface for this invocation. Conversely, default-mode output never surfaces plugin candidates. The two modes are mutually exclusive.
