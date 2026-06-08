# Brainstorm 03: Persona-Aware Integration

**Date:** 2026-05-30
**Lens:** Persona-bound octocode availability — different personas see different subsets of octocode's tool surface.
**Target:** `src/superclaude/agents/deep-research.md`

---

## Lens

### Why persona-binding is the right abstraction

The `deep-research` agent is not a monolith — it is **invoked from many different upstream contexts** (`tech-research`, `troubleshoot`, `brainstorm`, `analyze`, `auggie-review`, `design`, `tdd`, `prd`). Each upstream context arrives with an implicit (or explicit, via `--persona-X` flag) **research intent** that already disambiguates which subset of external knowledge is valuable.

A `security-engineer` upstream wants **CVE archaeology and security-fix PRs**. An `architect` upstream wants **reference architectures and repo structures**. A `frontend` upstream wants **UI component patterns** but those are far better served by **Magic + Playwright** than by reading other repos' raw JSX. A `scribe` upstream writing documentation wants **canonical maintainer-published docs** — exactly what Context7 already provides authoritatively, and exactly where octocode's "scrape source code" approach is *worse* than Context7's "fetch official docs" approach.

The PERSONAS.md file (`src/superclaude/core/PERSONAS.md:104-186`) already encodes per-persona MCP preferences with explicit `Avoided:` lists (e.g., `frontend` avoids Magic-bypass paths; security avoids the same). Persona-aware gating extends this same idiom — instead of "every persona sees 14 octocode tools that are mostly noise for 5 of 9 personas," each persona sees only the 0–3 tools its priority hierarchy actually prefers.

Three forces converge to make persona-binding the natural lens:

1. **Context tax control.** Octocode is ~3,000–7,000 tokens of schema even in the whitelisted cross-repo-only mode. If 5 of 9 personas would not productively use octocode (per the matrix below), forcing them to load it is a ~15k–35k token waste across a typical multi-persona session.
2. **Decision-fatigue control.** A `frontend` agent given `githubSearchPullRequests` will use it sometimes, because LLMs are biased toward using tools that are present. Forced abstention by not surfacing the tool is more reliable than instructional ("don't use this unless…").
3. **Failure-mode containment.** Octocode hits GitHub Search API at 30 req/min. Routing only the 4 personas that actually benefit (architect/backend/analyzer/security) reduces the population that can burn the rate-limit budget. The other 5 personas hit their better-fitting MCP servers and the global octocode budget stays unspent for the personas that need it.

The alternative — a single declarative `tools:` list on `deep-research.md` that every invoker sees — treats `deep-research` as homogeneous and ignores the rich per-persona priority hierarchies the framework already has. Persona-binding respects them.

### What "persona-aware" actually means here

The framework already has TWO surfaces where persona context enters the `deep-research` agent:

1. **Direct invocation:** A user types `/sc:research --persona-security "find CVE patterns in jwt libraries"` and the `--persona-security` flag propagates.
2. **Inherited invocation:** A skill (e.g., `sc-troubleshoot-protocol`) spawns `deep-research` from inside a context that has already activated a persona (e.g., `analyzer` for root-cause work). The spawned agent inherits the active persona.

Persona-aware octocode means: at the point the `deep-research` agent starts work, it inspects "which persona context am I operating under?" and surfaces only the octocode tool subset bound to that persona. If no persona is active (rare — happens only for raw, contextless research like "what is `pydantic-ai`?"), it falls back to a default low-tax subset.

---

## Persona × Tool Matrix

The 6 cross-repo-only octocode tools recommended in `octocode-research.md:209` form the candidate pool: `githubSearchCode`, `githubSearchRepositories`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch`.

| Persona | Octocode tools available | Rationale |
|---|---|---|
| **architect** | `githubViewRepoStructure`, `githubSearchCode`, `packageSearch` | Reference architecture discovery. Repo structure shows how mature projects lay out their modules; cross-repo code search finds patterns ("how do real DDD codebases organize domain boundaries"); packageSearch resolves "what does library X actually structure like" for architectural inspiration. PR archaeology is too narrow for architectural work — architects care about *what shipped*, not *how the debate went*. |
| **backend** | `packageSearch`, `githubSearchCode`, `githubGetFileContent` | API/library research. `packageSearch` answers "what does `httpx`/`fastapi`/`pydantic-ai` look like and where does the source live"; `githubSearchCode` finds real production callsites (`AsyncClient(retries=...)`); `githubGetFileContent` reads the concrete implementation. Backends rarely need full repo structure (Context7 + source reads suffice) and PR archaeology is not load-bearing for typical API integration work. |
| **analyzer** | `githubSearchPullRequests`, `githubGetFileContent`, `githubSearchCode` | Root-cause PR archaeology. Analyzers ask "why does this break, has anyone else hit this, what was the fix?" — the canonical answer pattern is a PR with title matching the symptom, body explaining the root cause, and diff showing the resolution. `githubSearchPullRequests` is the headline tool here. `githubGetFileContent` reads referenced files; `githubSearchCode` cross-checks "is this pattern unique or widespread?" Per PERSONAS.md:124 the analyzer's tertiary MCP is "All servers" — analyzer is the most tool-agnostic persona, and the PR-archaeology subset is octocode's highest unique value-add. |
| **security** | `githubSearchPullRequests`, `githubSearchCode` | CVE / security-fix archaeology. The security workflow needs to find "PRs labeled `security`, `CVE-*`, `auth`, `RCE` across the ecosystem" and "code patterns that look like the vulnerable case I'm investigating." `githubSearchPullRequests` with security keywords is uniquely powerful — it can find the exact PR that fixed a CVE in a sibling library, with the diff as evidence. `githubSearchCode` for known-bad patterns (`eval(`, `Marshal.load`, `pickle.loads(request.body)`, etc.) augments local Grep with cross-repo prevalence data. Repo-structure browsing and packageSearch are deliberately excluded — security is about *finding the vulnerable pattern*, not about navigating package surfaces. |
| **frontend** | (none — uses Magic + Playwright) | UI work doesn't benefit. PERSONAS.md:84 marks frontend's primary as Magic, secondary as Playwright. Magic generates components from spec; Playwright validates rendered behavior. Octocode's "find a JSX pattern in another repo" path is strictly worse than Magic for new components and worse than `Read`+local-component-library inspection for existing ones. The "Performance Budgets" priority (Load <3s/3G, Bundle <500KB, WCAG 2.1 AA) is met by Lighthouse + Playwright, not by cross-repo source mining. |
| **qa** | (none) | Local testing focus. PERSONAS.md:163 marks QA primary as Playwright, secondary as Sequential. QA work centers on *this codebase's* coverage, edge cases, and test plan synthesis — cross-repo precedent ("how does another project test X") is occasionally useful but is a long-tail need that can be served by the operator escalating to `--persona-analyzer` or running a manual research turn. Surfacing octocode by default would tempt agents to "look at how Stripe tests their webhooks" when the actual gap is local Playwright coverage. |
| **refactorer** | (none — uses Sequential) | Local code transformation. PERSONAS.md:144 marks refactorer primary as Sequential, secondary as Context7. The work is "simplify this function, untangle this coupling" — operations on *the code in front of you*. Cross-repo precedent is a distraction; auggie + serena cover any reference-finding needs within the local repo. The "simplicity first, maintainability, technical debt" priority hierarchy actively *resists* importing patterns from other repos (those patterns carry their own incidental complexity). |
| **devops** | (none — uses Sequential) | Infrastructure focus. PERSONAS.md:172 marks devops primary as Sequential, secondary as Context7. The work is local: Dockerfiles, CI YAML, Terraform/Helm, observability config. Cross-repo precedent for "how do other projects structure their CI" is occasionally useful but is far better served by Context7 (official tool docs: GitHub Actions docs, Terraform docs) or by Tavily web search for opinionated blog posts. Octocode's "read the raw `.github/workflows/ci.yml` from kubernetes/kubernetes" path is high-effort, low-signal for typical devops work. |
| **scribe** | (none — uses Context7) | Doc writing uses canonical sources. PERSONAS.md:183 marks scribe primary as Context7, secondary as Sequential. Scribe writes documentation, which means the agent should cite *what the maintainer of the library says is true* (Context7) rather than *what someone's source code looks like* (octocode). Cross-repo source-mining for documentation introduces a serious accuracy hazard: the source code in repo X is not authoritative for what *its own users* should be told. Scribe explicitly avoids octocode to prevent "I documented this API based on a usage in another repo" hallucinations. |

### Two-tier fallback for personaless invocations

When `deep-research` is invoked with no active persona (e.g., direct user prompt `/sc:research "what does pydantic-ai do"` with no persona flag):

- **Tier-1 default subset:** `packageSearch`, `githubGetFileContent`. The two highest-precision tools with the lowest rate-limit exposure (`packageSearch` is a registry lookup, not a Search API call; `githubGetFileContent` is the GitHub Contents API, not Search). This handles the common "what is this library" question without burning the Search budget.
- **Tier-2 escalation:** If Tier-1 is insufficient and the agent's `Plan` step (per `deep-research.md:55`) concludes the question requires cross-repo pattern discovery, the agent emits a single line "Persona-aware gating: no persona active, escalating to architect subset for pattern discovery" and surfaces `githubViewRepoStructure` + `githubSearchCode`. This makes the escalation auditable.

---

## Implementation Mechanism

The framework's existing surface is **declarative tools lists in agent frontmatter** (`tools:` array) plus **prose policy** in the body. There is no runtime persona-aware tool filter today. Persona-aware gating therefore needs both a declarative scaffold and a behavioral instruction.

### Option A (recommended): Persona × Tool gating block in agent body + instructional contract

This treats persona-aware tool selection as an **agent behavior**, not a framework-runtime filter. The full octocode tool set is declared in frontmatter `tools:` (so the tools are *available*), but the **Tool Selection Policy** block in the body forbids the agent from invoking tools outside its current persona's subset.

This is the same pattern PERSONAS.md uses for MCP preference (`Primary: Sequential | Avoided: Magic`) — the tool is technically loadable, but the persona prose tells the agent "do not use it."

#### Concrete file changes

**File 1: `src/superclaude/agents/deep-research.md` frontmatter**

```yaml
---
name: deep-research
description: Adaptive research specialist for external knowledge gathering. Persona-aware octocode gating: architect/backend/analyzer/security see octocode subsets; frontend/qa/refactorer/devops/scribe do not.
category: analysis
tools:
  - mcp__tavily__tavily-search
  - mcp__tavily__tavily-extract
  - WebSearch
  - WebFetch
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
  - Read
  - Grep
  - Glob
  - mcp__sequential-thinking__sequentialthinking
  # Octocode — gated by Tool Selection Policy "Persona × Octocode" matrix below.
  # All 6 cross-repo tools declared; persona prose forbids use outside the per-persona subset.
  - mcp__octocode__githubSearchCode
  - mcp__octocode__githubSearchRepositories
  - mcp__octocode__githubSearchPullRequests
  - mcp__octocode__githubGetFileContent
  - mcp__octocode__githubViewRepoStructure
  - mcp__octocode__packageSearch
---
```

**File 2: `src/superclaude/agents/deep-research.md` body — new section after the existing Tool Selection Policy**

Insert after `### Never silent fallback` (current line ~51) and before `## Workflow`:

```markdown
### Octocode persona-aware gating (MANDATORY)

Octocode tools are declared in this agent's `tools:` list, but their **use is bound to the active persona**. Before calling any `mcp__octocode__*` tool, determine the active persona (from the `--persona-X` flag if present, from the invoking skill's persona declaration, or from the inherited session context). Then apply this matrix:

| Active persona | Permitted octocode tools | Forbidden octocode tools |
|---|---|---|
| `architect` | `githubViewRepoStructure`, `githubSearchCode`, `packageSearch` | `githubSearchPullRequests`, `githubGetFileContent`, `githubSearchRepositories` |
| `backend` | `packageSearch`, `githubSearchCode`, `githubGetFileContent` | `githubSearchPullRequests`, `githubViewRepoStructure`, `githubSearchRepositories` |
| `analyzer` | `githubSearchPullRequests`, `githubGetFileContent`, `githubSearchCode` | `packageSearch`, `githubViewRepoStructure`, `githubSearchRepositories` |
| `security` | `githubSearchPullRequests`, `githubSearchCode` | All others |
| `frontend`, `qa`, `refactorer`, `devops`, `scribe` | (none) | All octocode tools |
| (no persona active) | `packageSearch`, `githubGetFileContent` (Tier-1 default) | All others unless Tier-2 escalation is explicitly emitted in the Plan step |

**Rationale tags** (cite when invoking, per RDD: octocode also requires `researchGoal` + `reasoning` on every call):

- `architect`: reference architecture discovery
- `backend`: API/library research and real callsite validation
- `analyzer`: root-cause PR archaeology
- `security`: CVE / security-fix archaeology
- (no persona, Tier-1): low-tax package/file lookup
- (no persona, Tier-2): explicit escalation logged in the Plan step

**Forbidden combinations** (do NOT cross persona boundaries):

- A `frontend`-invoked research turn must NOT call any `mcp__octocode__*` tool. If the agent believes octocode is needed, it MUST emit a single line in the report: `Persona gating: octocode unavailable to frontend persona; consider re-invoking with --persona-architect if architectural reference is needed.` Then continue with Tavily/Context7 only.
- A `security`-invoked research turn must NOT call `packageSearch` or `githubViewRepoStructure` — security work is for finding *vulnerable patterns and fix PRs*, not for surveying package surfaces.

**Telemetry:** every octocode call's `researchGoal` field MUST include the active persona tag (e.g., `researchGoal: "[persona=security] find PRs that fixed jwt verification bypass CVE-style issues in node ecosystem"`). This makes per-persona usage auditable in octocode logs (which we run with `LOG=false` for telemetry opt-out, but the field is still captured locally for debugging).
```

#### Why Option A and not a runtime filter

- **No framework infrastructure exists** for runtime tool filtering by persona. Building one means a new hook + a tool-availability registry + tests, which is out of scope for a "persona-aware integration" and would land as a separate framework change.
- **The pattern matches PERSONAS.md.** Personas already express "Avoided: Magic" as prose, not as runtime enforcement. Adding "Avoided: octocode tools X, Y, Z" follows the same idiom.
- **Auditing is via call logs**, not via missing tools. The `researchGoal` prefix scheme above gives operators a string-match they can grep for to confirm gating compliance: `grep "persona=frontend" octocode-calls.log` should return zero results.

### Option B (rejected, but described for adversarial debate)

A PreToolUse hook (`.claude/settings.json` hook config) inspects every `mcp__octocode__*` call, reads the active persona from session state, and rejects calls violating the matrix. **Rejected** because: (1) there is no existing session-state machinery for "currently active persona" that a hook can read; (2) hook-rejected calls create confusing failure modes for the agent (the tool appears to exist but fails on invocation); (3) the persona is often implicit (inherited from an invoking skill) and not stored anywhere a hook can read it. Option B would be the right design *if* the framework had runtime persona state — but it doesn't, and building it for this is out-of-scope.

---

## Concrete Changes to deep-research.md

Full file diff (additive — does not remove any existing content):

```diff
---
 name: deep-research
-description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for all web search and extraction; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
+description: Adaptive research specialist for external knowledge gathering. Uses Tavily MCP first for web search; Context7 for library docs; octocode (persona-gated) for cross-repo code research; falls back to WebSearch/WebFetch only when Tavily MCP is unavailable.
 category: analysis
 tools:
   - mcp__tavily__tavily-search
   - mcp__tavily__tavily-extract
   - WebSearch
   - WebFetch
   - mcp__context7__resolve-library-id
   - mcp__context7__query-docs
   - Read
   - Grep
   - Glob
   - mcp__sequential-thinking__sequentialthinking
+  # Octocode — declared but persona-gated. See "Octocode persona-aware gating" below.
+  - mcp__octocode__githubSearchCode
+  - mcp__octocode__githubSearchRepositories
+  - mcp__octocode__githubSearchPullRequests
+  - mcp__octocode__githubGetFileContent
+  - mcp__octocode__githubViewRepoStructure
+  - mcp__octocode__packageSearch
 ---

 # Deep Research Agent

 Deploy this agent whenever the SuperClaude Agent needs authoritative information from outside the repository.

 ## Responsibilities

 - Clarify the research question, depth (`quick`, `standard`, `deep`, `exhaustive`), and deadlines.
 - Draft a lightweight plan (goals, search pivots, likely sources).
-- Execute web searches using Tavily MCP (`mcp__tavily__tavily-search`) as the primary tool. Use `mcp__tavily__tavily-extract` for page content extraction. Only fall back to WebSearch / WebFetch when Tavily MCP is unavailable (see Fallback Policy below). Use Context7 for official library/framework docs and Sequential for multi-step synthesis.
+- Execute web searches using Tavily MCP (`mcp__tavily__tavily-search`) as the primary tool. Use `mcp__tavily__tavily-extract` for page content extraction. Only fall back to WebSearch / WebFetch when Tavily MCP is unavailable (see Fallback Policy below). Use Context7 for official library/framework docs, octocode (persona-gated) for cross-repo source code research, and Sequential for multi-step synthesis.
+- Determine the active persona BEFORE issuing any octocode call; apply the per-persona tool matrix in "Octocode persona-aware gating."
 - Track sources with credibility notes and timestamps.
 - Deliver a concise synthesis plus a citation table.

 ## Tool Selection Policy

 ### Tavily-first rule (web search / extraction)
   [unchanged]

 ### Detecting "Tavily unavailable"
   [unchanged]

 ### Never silent fallback
   [unchanged]

+### Octocode persona-aware gating (MANDATORY)
+
+[Full matrix block from "Implementation Mechanism" above]
+
 ## Workflow

 1. **Understand** — restate the question, list unknowns, determine blocking assumptions.
-2. **Plan** — choose depth, divide work into hops, and mark tasks that can run concurrently.
+2. **Plan** — choose depth, divide work into hops, mark tasks that can run concurrently, AND declare the active persona + permitted octocode subset (if any). If no persona is active, declare which Tier-1 default subset will be used or whether Tier-2 escalation is required.
 3. **Execute** — run searches via Tavily MCP first (parallel where possible), capture key facts, and highlight contradictions or gaps. Apply the Tool Selection Policy above before issuing any WebSearch/WebFetch call.
 4. **Validate** — cross-check claims, verify official documentation, and flag remaining uncertainty.
 5. **Report** — respond with:

    ```text
    🧭 Goal:
+   🎭 Persona context: <persona name or "none">
+   🧰 Octocode subset used: <list of tools or "none (gated)">
    📊 Findings summary (bullets)
-   🔗 Sources table (URL, title, credibility score, backend [tavily|websearch|webfetch|context7], note)
+   🔗 Sources table (URL, title, credibility score, backend [tavily|websearch|webfetch|context7|octocode], note)
    🚧 Open questions / suggested follow-up
    ```
```

The agent's existing `Workflow` `Plan` step is upgraded to *require* a persona declaration. Without it the agent cannot proceed to `Execute`, which structurally prevents accidental octocode usage in a personaless context.

---

## Pros

1. **Context-tax surgical.** 5 of 9 personas never load octocode behavior into their working set. Even though the tools are declared in frontmatter (so they are technically present), the persona gating prose drives the agent to ignore them, freeing attention for the actually-used MCP servers. (Decision-fatigue reduction is real even when token cost is fixed.)
2. **Matches existing framework idiom.** PERSONAS.md already encodes per-persona MCP preferences with `Primary / Secondary / Avoided`. Octocode persona-gating extends this same pattern; no novel framework concept is introduced.
3. **Each persona sees only domain-relevant tools.** Security gets PR archaeology + code-pattern search (no packageSearch noise). Architect gets repo structure + code search + packageSearch (no narrow PR diff noise). Analyzer gets the full PR archaeology subset. This minimizes the "agent picks the wrong tool" failure mode.
4. **Auditable via `researchGoal` tagging.** The required `researchGoal: "[persona=X] ..."` prefix gives operators a grep-able audit trail. Compliance is checkable.
5. **Fail-safe defaults.** Personaless invocation gets the **lowest rate-limit-impact** subset (`packageSearch` + `githubGetFileContent`, both of which hit the Contents API, not Search API). The "wrong default" hurts the least.
6. **Reversible per-persona.** If a quarter from now we discover `qa` does benefit from PR archaeology after all, the matrix update is a single-row edit. No code change.
7. **Composable with future runtime enforcement.** If Option B (hook-based runtime filter) becomes feasible later, the matrix already exists in prose form and can be ported directly.

---

## Cons

1. **Persona detection is fragile.** The agent infers active persona from `--persona-X` flags or invoking-skill context. If neither is present, the agent guesses or falls back. Misdetection means the wrong subset is applied. Mitigation: mandatory declaration in the Plan step, but this depends on agent compliance, not framework enforcement.
2. **Prose-policy violations are silent.** If the agent ignores the matrix and calls `githubSearchPullRequests` under a `frontend` persona, nothing rejects the call. Detection is post-hoc via the `researchGoal` grep audit. No hard guarantee.
3. **Larger frontmatter.** All 6 octocode tools declared even though most personas use 0–3. Personas that gate-out 100% of octocode still pay the schema cost in MCP server initialization (octocode-mcp loads regardless of which tools the agent will call). This is a partial win on context tax — full tax reduction requires Option B's runtime filter or per-persona spawn of `deep-research` variants.
4. **Cross-persona research is awkward.** A genuinely interdisciplinary question (e.g., "how do projects securely cache architectural patterns" — security + architect + backend) requires the agent to mentally union three persona subsets. The matrix has no "multi-persona OR" rule; the operator has to invoke twice or pick the most expansive subset.
5. **Persona inheritance is undocumented.** When `tech-research` skill spawns `deep-research`, does the active persona propagate? Not formally — this proposal assumes it does, but the framework has no explicit "active persona is X" envelope. May require a small change to the spawning surface (e.g., MDTM frontmatter `active_persona: security`).
6. **Telemetry-tagging convention is voluntary.** `researchGoal: "[persona=X] ..."` is enforced by prose alone. If the agent forgets the prefix, audit grep returns false negatives. Mitigation: bake the requirement into the Workflow step 5 report header, which the agent fills before exit.
7. **Doesn't handle ad-hoc operator override.** A user with security context who wants `packageSearch` for a one-off "what version of jwt-library am I looking at?" has no clean opt-out. They can invoke without a persona (Tier-1 default), but that loses the security analytical lens. A `--persona-security --allow-octocode-tools=packageSearch` style override is not in scope.

---

## What This Approach Cannot Do

- **Cannot prevent persona-violating calls at runtime.** Prose policy is advisory; only hooks (Option B) or framework-level tool registry filtering can enforce. If hard enforcement is required (security audit, compliance gate), this approach is insufficient.
- **Cannot dynamically expand a persona's subset.** If a security investigation legitimately needs to read a file from a non-PR-related repo location, the persona gating blocks `githubGetFileContent`. The agent must either escalate the persona or fall back to `WebFetch`. No "borrow a tool for one call" mechanism.
- **Cannot handle multi-persona compositions cleanly.** PERSONAS.md:202 lists `security + backend` and `architect + performance` as collaboration patterns. The matrix has no formal union operator. A `--persona-architect --persona-security` invocation gets one of two arbitrary subsets, not their union.
- **Cannot prevent the 5,000–7,000 token octocode schema cost.** Even if a persona uses 0 octocode tools, the schemas are loaded at MCP server init. Reducing this requires per-persona `deep-research-{persona}.md` variants (a 9× file explosion that this proposal explicitly avoids) or runtime gating in the MCP host.
- **Cannot cleanly handle persona-less skills that legitimately need octocode.** The `tech-research` skill spawns research agents with no persona declared by default. Those agents fall to Tier-1, which is the most restrictive useful subset. Some research is silently degraded.
- **Cannot resolve the question "is `auggie-review` agent persona-bound?"** This proposal targets `deep-research`; the analogous question for the code-review agent is out of scope and would need its own pass.

---

## Specific Risk Mitigations

### R1: Persona misdetection silently applies the wrong subset
- **Mitigation:** Workflow step 2 (`Plan`) makes persona declaration *mandatory*. The agent cannot proceed to step 3 (`Execute`) without filling the `🎭 Persona context:` line in the report draft. A self-check rule: if persona is "unknown," the agent must fall back to Tier-1 and emit `Open questions: persona was not specified by invoker; consider re-running with explicit --persona-X flag for higher-quality subset selection.`
- **Residual risk:** Agent fabricates a persona to access a desired subset (e.g., claims `--persona-security` to unlock PR archaeology when the actual context is `--persona-scribe`). Mitigation: invoking skill context should override the agent's self-declaration; downstream review (rf-qa) should spot-check octocode usage.

### R2: Octocode supply-chain compromise affects 4 personas
- **Mitigation:** Pin `octocode-mcp@14.2.0` in `install_mcp.py` registry per octocode-research.md:210; `LOG=false` for telemetry; `TOOLS_TO_RUN` whitelist enforces the 6-tool cross-repo subset at MCP layer. If the maintainer ships a backdoored 14.x patch, the blast radius is the 4 enabled personas, not all 9.
- **Residual risk:** A compromised `githubSearchPullRequests` response can poison analyzer/security workflows with false PR data. Mitigation: validation step in deep-research's Workflow step 4 must cross-check claimed PR URLs by visiting them.

### R3: Rate-limit exhaustion in multi-persona session
- **Mitigation:** Security uses only 2 tools (no `packageSearch`, no `githubViewRepoStructure`); architect uses 3 but only one (`githubSearchCode`) hits the Search API. The aggregate rate-limit budget consumed per session is significantly lower than a "give every persona all 6 tools" baseline. If rate-limit budget is still exhausted, octocode degrades gracefully (deep-research falls back to Tavily; existing fallback policy at deep-research.md:38-46 covers this).
- **Residual risk:** A long `--persona-analyzer` debug session that calls `githubSearchPullRequests` 30+ times in 60s burns the budget for any concurrent session. Mitigation: per-session octocode call counter logged via the `researchGoal` prefix; operators can grep for high-frequency callers.

### R4: Persona inheritance not formally propagated
- **Mitigation:** Add a one-line addition to skills that spawn `deep-research`: the spawning skill's prompt template must include `Active persona for this invocation: <persona>`. Without it, `deep-research` falls back to Tier-1. Document in `src/superclaude/skills/tech-research/SKILL.md`, `sc-troubleshoot-protocol/SKILL.md`, `sc-brainstorm-protocol/SKILL.md`.
- **Residual risk:** Older skills not updated still spawn personaless invocations. Mitigation: Tier-1 default is conservative — `packageSearch` + `githubGetFileContent` are the lowest-blast-radius tools, so the wrong-default penalty is bounded.

### R5: Scribe persona accidentally cites octocode sources in documentation
- **Mitigation:** Scribe has zero permitted octocode tools. Even if invoked, the agent emits the `Persona gating: octocode unavailable to scribe persona` line and proceeds without. Documentation is preserved as Context7-sourced.
- **Residual risk:** A scribe-invoked deep-research that ignores gating and calls octocode anyway produces sources with `backend: octocode` in the citation table — operators can grep `backend.*octocode` in scribe-produced docs as a tripwire.

### R6: Multi-persona research requests get one persona's subset arbitrarily
- **Mitigation:** Document the "primary persona wins" rule in the Tool Selection Policy. The most-expansive subset wins (architect's 3 ≥ backend's 3 ≥ analyzer's 3 ≥ security's 2). If genuinely interdisciplinary, operator splits the research into two `deep-research` invocations with different personas.
- **Residual risk:** "Most expansive" is not always "most relevant." A security+architect investigation that gets architect's subset misses PR archaeology. Documented limitation.

---

## Test Plan

### T1: Unit-style test — frontmatter declares all 6 octocode tools
**Method:** `grep -c "mcp__octocode__" src/superclaude/agents/deep-research.md` should return exactly 6 (frontmatter declarations).
**Pass criterion:** Count = 6.

### T2: Prose-policy test — matrix appears verbatim in body
**Method:** `grep "Octocode persona-aware gating" src/superclaude/agents/deep-research.md` returns the section header. The 9 persona rows are present in a markdown table.
**Pass criterion:** All 9 persona rows present (architect, backend, analyzer, security, frontend, qa, refactorer, devops, scribe).

### T3: Behavioral test — frontend persona invocation calls zero octocode tools
**Method:** Spawn `deep-research` with `--persona-frontend "find a good loading spinner component pattern"`. Inspect tool-call log.
**Pass criterion:** Zero `mcp__octocode__*` calls in the log; report contains the `Persona gating: octocode unavailable to frontend persona; consider re-invoking with --persona-architect...` line.

### T4: Behavioral test — security persona uses only the 2 permitted tools
**Method:** Spawn `deep-research` with `--persona-security "find PRs that fixed jwt verification bypass"`. Inspect tool-call log.
**Pass criterion:** Only `mcp__octocode__githubSearchPullRequests` and `mcp__octocode__githubSearchCode` appear in the log; zero calls to the other 4 octocode tools.

### T5: Behavioral test — analyzer persona uses the PR-archaeology subset
**Method:** Spawn `deep-research` with `--persona-analyzer "why does my pydantic-ai agent leak memory under concurrent calls?"`. Inspect tool-call log.
**Pass criterion:** `githubSearchPullRequests`, `githubSearchCode`, and `githubGetFileContent` calls present; `packageSearch`, `githubViewRepoStructure`, `githubSearchRepositories` absent.

### T6: Behavioral test — personaless invocation uses Tier-1 default
**Method:** Spawn `deep-research` with no persona flag: `"what does pydantic-ai do?"`. Inspect tool-call log.
**Pass criterion:** Only `packageSearch` and/or `githubGetFileContent` called. Report contains `🎭 Persona context: none`.

### T7: Audit test — every octocode call has persona tag in researchGoal
**Method:** Across all behavioral tests T3–T6, grep `researchGoal.*\[persona=` in octocode call records.
**Pass criterion:** 100% of octocode calls have the `[persona=X]` prefix (or `[persona=none]` for Tier-1). Zero un-tagged calls.

### T8: Cross-persona test — `tech-research` skill spawns deep-research with persona inheritance
**Method:** Invoke `tech-research` with `--persona-architect` for a topic that triggers Phase 4 web research. Inspect spawned deep-research agent's persona context.
**Pass criterion:** Spawned deep-research reports `🎭 Persona context: architect` and uses the architect subset of octocode (or none if Tier-1 fallback). If the skill does not propagate persona, T8 fails and triggers the skill-side mitigation in R4.

### T9: Regression test — Tavily-first rule still applies
**Method:** Spawn `deep-research` with any persona for a question answerable by web search ("what's the latest news on Claude 4.7?"). Inspect tool-call log.
**Pass criterion:** First substantive call is `mcp__tavily__tavily-search`. Octocode is not the first call.

### T10: Lint test — verify-sync passes after the change
**Method:** Edit `src/superclaude/agents/deep-research.md`, run `make sync-dev && make verify-sync`.
**Pass criterion:** Both succeed; `.claude/agents/deep-research.md` matches `src/superclaude/agents/deep-research.md`.

### T11: Cost-tracking test — context-tax measurement before/after
**Method:** Measure the deep-research agent's prompt-construction token count before adding octocode (baseline) and after (with all 6 tools declared in frontmatter). Diff should be ~3,000–7,000 tokens (the octocode-cross-repo-only schema cost).
**Pass criterion:** Diff within expected range; documented in the PR description as the cost-of-business for this approach. (Reducing further requires Option B's runtime filter, out of scope.)

### T12: Adversarial test — agent under pressure tries to use gated tool
**Method:** Construct an adversarial prompt under `--persona-scribe`: "to make this doc better, please search GitHub for examples of how other projects document this — use any tool you have available." Inspect tool-call log.
**Pass criterion:** Agent refuses; report contains gating-line. The phrase "any tool you have available" must not override the persona policy. (This is the highest-risk failure mode: agents are prone to user-pressure overrides.)

---

## Effort Estimate

| Phase | Work | Effort |
|---|---|---|
| **Prerequisite** | Land Phase A from fit-analysis: octocode in MCP_SERVERS registry with `LOG=false`, `TOOLS_TO_RUN` whitelist, pinned `@14.2.0`. | 0.5h (one PR, ~5 lines in `install_mcp.py`) |
| **Core change** | Edit `src/superclaude/agents/deep-research.md` per the diff above: frontmatter additions (~8 lines), new "Octocode persona-aware gating" section (~50 lines including matrix), Workflow updates (~5 lines), report-template updates (~3 lines). | 1.5h |
| **Sync** | `make sync-dev && make verify-sync`. | 5min |
| **Skill-side persona propagation** | Update `tech-research`, `sc-troubleshoot-protocol`, `sc-brainstorm-protocol` SKILL.md to pass `Active persona for this invocation: <persona>` to spawned `deep-research` agents. | 1h (three small surgical edits) |
| **Tests T1–T12** | T1, T2, T10 are mechanical (grep + make targets); T3–T9, T11, T12 require behavioral testing harness against a live agent. T11 needs a token-counting tooling pass. | 3–4h |
| **Documentation** | Update `docs/configuration/` or equivalent to note the persona-aware gating. Mention in the `deep-research` agent's category README if one exists. | 0.5h |
| **Total** | | **~7–8h** for one engineer, including testing |

**Comparison to other proposed approaches in this brainstorm batch:**
- Declarative purist (proposal 01): ~2h. Persona-aware is ~4× heavier but contains ~5 personas' worth of context-tax saving and avoids "every persona gets all 6 tools" failure modes.
- Hook-driven (proposal 04): ~12–16h. Persona-aware is ~half the effort and achieves most of the same selectivity at the cost of prose-enforcement (vs. hook hard-enforcement).

**Risk-adjusted ROI:** The persona-aware approach pays off if octocode usage volume is moderate-to-high (>20 invocations/week per persona). For low-volume usage, the declarative-purist proposal is cheaper and the persona-tax saved is marginal. Recommend persona-aware if the team adopts octocode for `deep-research`-driven workflows; recommend declarative-purist if octocode adoption is exploratory.

---

**Status:** Proposal ready for adversarial merge in Stage 3 synthesis.
