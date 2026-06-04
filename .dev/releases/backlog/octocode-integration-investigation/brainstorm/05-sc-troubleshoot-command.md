# Brainstorm — Target #5: /sc:troubleshoot Command

**Date:** 2026-05-30
**Stage:** 3 of 3 (parallel brainstorm; agent 5 of 5)
**Target file:** `src/superclaude/commands/troubleshoot.md`
**Target protocol:** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md`
**Question:** What is the most beneficial way to integrate octocode into `/sc:troubleshoot`?

---

## Target Context

### Current command surface

`/sc:troubleshoot` is the framework's tiered debugging command — auto-fires whenever a user reports an error, regression, flake, build failure, deployment problem, or pasted stack trace. It is intentionally "pushy" because the failure mode it fights against is users skipping the debugger because they don't realize it would help.

Its mcp-server roster declared in the command frontmatter:
- `auggie` — in-repo retrieval (free / low-cost; tagged HIGHEST PRIORITY in repo CLAUDE.md)
- `serena` — symbol navigation + project memory
- `context7` — official library/framework docs (Tier 2 only)
- `tavily` — web search, rate-capped at **≤ 2 queries per invocation** (Tier 2 only)
- `sequential` — multi-step reasoning for synthesis (Tier 2 only)

### Tier-by-tier tool allocation (from protocol §"Tool Coordination Summary")

| Tool | Tier 1 | Tier 2 | Tier 3 |
|------|--------|--------|--------|
| auggie | ✓ (focused query + Wave 1.5 doc-grounding fan-out) | ✓ (per-hypothesis queries) | — |
| serena | ✓ | ✓ | — |
| context7 | — | ✓ when framework/library named | — |
| **tavily** | — | ✓ **rate-limited (≤ 2 queries)** | — |
| sequential | — | ✓ (synthesis) | — |

### Wave structure (where octocode could plug in)

```
Wave 0: Parse + Validate
Wave 1: Tier 1 — Real-Code Grounding (auggie + serena)
Wave 1.5: Documentation Grounding (3 parallel auggie branches: release / arch / restrictions)
Wave 1.7: Tier 1 — Hypothesis Formation (root-cause-analyst + confidence-calibrator)
Wave 2: Confidence Gate (escalate or stop)
Wave 3: Tier 2 — Parallel Hypotheses (2-4 specialist agents in parallel; context7 + tavily here)
Wave 4: Tier 2 — Adversarial Fix Debate (sc:adversarial --compare fix-1.md,fix-2.md...)
Wave 5: Synthesis + Report (evidence-validator)
Wave 6: Tier 3 — Remediation Chain (task-builder + /sc:reflect)
```

### Escalation triggers (from `refs/escalation-rubric.md`, summarised)
- `confidence < 0.85` → escalate
- Multi-domain symptom → escalate (one hypothesis can't cover two domains)
- "intermittent" / reproducibility unclear → escalate
- `security < 0.95` → escalate (raised bar)
- `--depth deep` → always escalate

### What troubleshoot does WELL today (where octocode adds nothing)
- Local code grounding — auggie + serena saturate this
- Per-file:line evidence validation — `evidence-validator` enforces real-file citations
- Doc-grounding against the **local** codebase (release artifacts, architectural docs, semantic restrictions) — Wave 1.5

### What troubleshoot does POORLY today (octocode's wedge)
- **Cross-repo precedent finding.** "Has anyone else hit `TypeError: cannot read property 'X' of undefined` in framework Z's middleware?" — currently goes through Tavily, which returns blog noise (LeetCode wrappers, low-effort "fix this error" SEO posts) and is rate-capped at 2 queries.
- **Package-version archaeology.** "Did this break between `pydantic 2.5.0` and `2.6.0`?" — currently no native tool resolves package → repo → changelog/diff.
- **Real-error-string fingerprinting.** Tavily semantic search hits SEO blogs first; GitHub Issues/PRs that contain the *literal* error message are buried behind general web rankings.
- **Stack-trace site matching.** "Which OSS projects have a file at path `src/auth/middleware.ts:142`-shape that calls into a function with this signature?" — no existing tool answers this.
- **Regression archaeology in upstream deps.** "What was the last upstream PR that touched this code path?" — `gh` CLI works but agents rarely chain through it correctly.

These are exactly octocode's killer features (per fit-analysis §5: cross-repo GitHub search + `packageSearch` + cross-repo PR archaeology = "~3 genuinely unique capabilities").

### Why troubleshoot is rated #6 in fit-analysis (score: 28)
The fit-analysis (line 167-168) called troubleshoot "marginal value-add" because the existing 4-tool stack already covers most cases. **The brainstorm question here is: is that ranking right, or does it under-weight Tavily's failure mode on this specific surface?** Tavily noise on error-string lookup is a known sharp edge — octocode's repo-grounded search would replace SEO blogs with first-party reports.

---

## The Integration Question

> **What is the most beneficial way to integrate octocode into `/sc:troubleshoot` such that (a) it sharpens the worst part of the current pipeline (Tavily noise on error-string search at Tier 2), (b) it never bloats Tier 1 (which must stay in the 3-6k Claude-token band for the "quick first option" contract), (c) it respects the hallucination contract (every cited fix from another repo must include a permalink and be flagged as precedent, not evidence), and (d) it composes cleanly with the existing 6-wave structure rather than introducing a new wave?**

The interesting tension: **Tier 1 must stay cheap** (auggie + serena are free / low-cost; octocode burns GitHub Search API budget at 30 req/min and adds latency). But **Tier 2 is where octocode wins biggest** (the failing 1-in-5 flaky test, the regression after refactor, the security finding — all benefit from "has anyone else seen this in $similar_repo").

There's a second tension on the Tier-1 side: **package-version archaeology** is *not* expensive (one `packageSearch` call) and is *especially* valuable when the symptom names a third-party library. Forcing every package-archaeology question through Tier 2 escalation costs the user time on cases that should be Tier-1-fast.

---

## Wave 1: Divergent Ideation

### Candidate A — Tier-2-only PR archaeology agent (precedent-as-evidence, NOT as fix)

**Where it plugs in:** Wave 3, parallel to the existing 2-4 hypothesis agents.

**What it does:** Spawn a new `precedent-finder` agent that uses `githubSearchPullRequests` + `githubSearchCode` to find the *same error signature* (exact error string, exception class + relevant frame) in OSS repos. Returns a **Precedent Card** at `<output-dir>/tier2-precedent-finder.md` listing 1-5 hits with:
- Permalink to the PR or issue
- Brief diagnosis quoted from the PR description (or commit message)
- The fix applied (one-line summary, links to the diff)
- Confidence in similarity (signature match, framework version match, error-frame match)

**Critical contract:** the Precedent Card flows into the report as a **separate "Precedent from other repos" section**, NEVER as evidence. The fix is whatever Wave 4 chose; precedents are advisory context that may inform the debate but cannot ground a file:line citation in the *local* repo.

**Variant A1 — type-gated:** Only spawn precedent-finder when `--type ∈ {bug, build, test}` (not `performance`, `deployment`, `security` — those rarely have clean cross-repo signatures).
**Variant A2 — confidence-gated:** Only spawn when Tier 1 confidence falls in `[0.50, 0.85]` (the "ambiguous middle"; below 0.50 the hypothesis is too weak to anchor a search; above 0.85 Tier 2 doesn't fire anyway).

---

### Candidate B — Replace Tavily entirely on troubleshoot (the "Tavily noise is the bug" approach)

**Where it plugs in:** Strike `mcp__tavily__tavily-search` from troubleshoot's frontmatter and Tier 2 enrichment list. Replace with octocode `githubSearchCode` + `githubSearchPullRequests`.

**What it does:** Every Wave 3 step-1 enrichment that today fires `tavily_search("<exact error string> github issue")` instead fires `githubSearchCode(<exact error string>)` and `githubSearchPullRequests(<error keywords>)` against the same 2-query cap.

**Rationale:** The Tavily query template in the protocol *literally* targets `github issue` strings. Going direct to GitHub Search API removes the SEO-blog layer that wraps Tavily's web search. The 2-query cap remains for rate-limit discipline (GitHub Search is 30/min — well within reach for 2 queries per invocation).

**Risk:** Some error symptoms have *no* GitHub presence but DO have a Stack Overflow / Django Forum / Discourse answer that Tavily would find. Stripping Tavily loses that long tail.

---

### Candidate C — Tier-1 `packageSearch` lookup, gated on third-party-name detection

**Where it plugs in:** Wave 1 step 1 (real-code grounding), as a 3rd parallel call alongside auggie + serena, conditional on signal.

**What it does:** When the issue description contains a package name (regex on `pip`, `npm`, `pydantic`, `langchain`, `fastapi`, `react`, etc., or stack frame names a module path that maps to an installed package), fire **one** `mcp__octocode__packageSearch` call. Returns: canonical repo URL, current version vs installed version, deprecation status, link to changelog.

**This is cheap (1 API call) and Tier-1-appropriate because:**
- It's a *retrieval* call, not a reasoning step
- Output enriches the `root-cause-analyst` brief in Wave 1.7 (passed alongside Documentation Context Card)
- Catches the "wrong version" / "deprecated method" diagnoses at Tier 1 instead of escalating

**Skip when:** no package name in issue description AND stack trace is purely first-party.

---

### Candidate D — Wave 1.5 Branch D (octocode-as-fourth-doc-source)

**Where it plugs in:** Wave 1.5 currently runs 3 parallel auggie branches (release-doc, architectural-doc, semantic-restrictions). Add a 4th branch: `Branch D — Upstream changelogs + RFCs from cross-repo`.

**What it does:** When the issue description names a third-party library OR the stack trace ends in a non-`src/superclaude/` module, Branch D fires `packageSearch` + `githubGetFileContent(CHANGELOG.md)` + `githubSearchPullRequests(label:breaking-change ...)` against the named library's repo. Output flows into the Documentation Context Card as a "**External upstream context**" section.

**Rationale:** Wave 1.5 is doc-grounding. Today it only grounds against *local* docs. But "the symptom is caused by an upstream API change" is a frequent diagnosis pattern — and the *upstream* changelog is the documented contract for that case.

**Risk:** Adds Wave 1.5 latency and token cost. The wave is targeted at ≤ 2k Claude tokens; a 4th branch with cross-repo calls pushes that. Requires conditional firing (only when third-party signal present).

---

### Candidate E — Hybrid: octocode at Tier 1 for fast lookup; escalate to Tier 2 hypothesis fan-out only if no precedent found

**Where it plugs in:** New step at end of Wave 1.7, before the Wave 2 confidence gate.

**What it does:** After the Tier 1 hypothesis is calibrated, before deciding to escalate, fire ONE focused `githubSearchPullRequests(<exact exception class> <key-frame-symbol>)` call. If a strong match (a PR titled "Fix `TypeError: ...`" with merged status, in a popular repo) is found → surface as Tier-1-precedent and bias the Wave 2 confidence gate UPWARD (stop at Tier 1, octocode confirms the diagnosis). If no hit → bias downward (escalate, octocode found no precedent so the bug is rarer / more local).

**This is the most operationally novel of the candidates** — it treats octocode hits as a *meta-signal* on confidence rather than as evidence in the report. But it complicates the escalation rubric.

---

### Candidate F — Per-error-class routing (the "right tool for each signature" approach)

**Where it plugs in:** Wave 3 step 1 (MCP enrichment in parallel with agent spawn). Replaces the current Tavily call with a routing matrix:

| Error class | Trigger keywords | Octocode tool | Why |
|-------------|------------------|---------------|-----|
| Stack trace with exception class | `NameError`, `TypeError`, `AttributeError`, `ImportError`, traceback formatting | `githubSearchPullRequests(<exception class> <symbol>)` | PRs that fixed this exact error in OSS |
| Deprecation warning | `DeprecationWarning`, "is deprecated", "will be removed" | `packageSearch(<package>)` → `githubGetFileContent(CHANGELOG.md)` | Find the version where deprecation began + the replacement API |
| Build failure | `tsc`, `webpack`, `vite`, `babel`, build-log fragment | `githubSearchCode(<exact error message>)` | Build errors often match config-file copy-paste; cross-repo search finds the right config snippet |
| Test failure | `pytest`, `jest`, `vitest`, "flaky" | `githubSearchPullRequests(label:flaky <fixture or symbol>)` | OSS communities have specific flaky-test conventions; PR labels surface them |
| Performance regression | `slow`, `p99`, `memory leak` | (skip octocode, stay on auggie + sequential) | Perf is rarely cross-repo-transferable |
| Security | `CVE`, `IDOR`, `XSS` | `githubSearchPullRequests(<CVE-id>)` + `githubSearchCode(<vuln pattern>)` | CVE PRs are well-tagged; cross-repo pattern matching shines |

**Token cost:** 2-3 octocode calls per invocation (within rate limit). Replaces 2 Tavily calls 1:1 on the affected error classes, supplements on others.

---

### Candidate G — `precedent-finder` as standalone Tier-2 agent (the lightweight version of Candidate A)

**Where it plugs in:** Wave 3, parallel to existing agents, but as a thinner agent than Candidate A.

**What it does:** A single-purpose agent whose ONLY job is `githubSearchPullRequests(<exact error string>) → top-3 PRs → quote first 200 chars of each PR description + permalink`. No diagnosis, no fix proposal. Pure precedent retrieval, dropped into the report's "Precedent" section.

**Difference from A:** Candidate A has the precedent-finder produce a structured Precedent Card competing with hypothesis cards. Candidate G keeps it as a retrieval helper — no hypothesis, no calibration, no debate participation. Lower complexity, lower upside.

---

## Wave 2: Adversarial Evaluation

### Evaluation criteria (the 6 axes the design must perform on)

1. **Cost discipline** — Tier 1 must stay in 3-6k Claude tokens / 1-3 min; Tier 2 octocode must not blow the rate limit.
2. **Hallucination resistance** — cross-repo findings must be flagged as "precedent" not "evidence" because they CANNOT be file:line-validated against the local repo.
3. **Composability** — does the change require restructuring existing waves, or does it slot in?
4. **Failure isolation** — if octocode is down (rate limited, network), does the existing pipeline degrade gracefully?
5. **Coverage** — does the integration address the *known weakness* (Tavily noise on error strings)?
6. **Operational complexity** — how much new code/config/branching does the user encounter?

### Candidate scoring table

| Candidate | Cost discipline | Hallucination resistance | Composability | Failure isolation | Coverage | Op complexity | Score |
|-----------|----------------|--------------------------|---------------|-------------------|----------|---------------|-------|
| **A** (Tier-2 precedent agent, gated) | 5 — Tier 2 only; one agent | 5 — Precedent section is separate from Evidence by contract | 4 — adds agent slot in Wave 3, fits existing parallel-spawn pattern | 5 — agent failure = "no precedent found", pipeline unaffected | 4 — covers Tier 2 cases (where Tavily noise is worst) | 4 — one new agent persona + section in report | **27** |
| **B** (Tavily replacement) | 4 — same 2-query budget, different API | 3 — same risk (search results, not file:line evidence) | 3 — surface-level frontmatter swap but loses Tavily long-tail | 2 — if octocode is down, no fallback retained for Tier 2 enrichment | 5 — directly addresses the Tavily-noise wedge | 3 — clean but removes a working tool | **20** |
| **C** (Tier 1 `packageSearch`, gated) | 4 — one cheap call; gated on signal | 5 — packageSearch returns metadata, not code claims | 5 — slots into Wave 1 step 1 cleanly | 5 — degrade = skip, no functional impact | 3 — addresses package-version cases only | 5 — minimal | **27** |
| **D** (Wave 1.5 Branch D) | 2 — extra branch pushes Wave 1.5 over budget | 4 — flows into Doc Context Card which IS evidentiary; mixed | 3 — symmetric with existing 3 branches but lengthens wave | 4 — branch failure handled by existing fall-through | 4 — catches upstream-changelog cases | 2 — adds a 4th branch + new query template | **19** |
| **E** (octocode as confidence meta-signal) | 4 — one call at end of Wave 1.7 | 4 — uses octocode hit as signal, not as quoted evidence | 1 — modifies escalation rubric, ripple effects to refs/escalation-rubric.md | 3 — rubric depends on octocode answer; ambiguous when it fails | 3 — novel but unproven; could over/under-escalate | 1 — most operationally complex | **16** |
| **F** (per-error-class routing) | 4 — 2-3 calls within rate limit; 1:1 with Tavily today | 4 — search results, with routing reducing noise per class | 3 — significant matrix added to Wave 3 step 1 | 4 — each class can independently fall back to Tavily | 5 — surgical per error class; highest coverage | 2 — most rules, biggest doc surface | **22** |
| **G** (lightweight precedent-finder) | 5 — single agent, single tool call | 4 — explicit precedent-only contract; no fix proposal | 5 — drop-in agent; no rubric changes | 5 — agent failure = no precedent section | 3 — covers Tier 2 only, less rich than A | 5 — simplest of all | **27** |

### Critical observations from the table

- **Candidate B (Tavily replacement)** scores worst on failure isolation. Removing Tavily entirely means an octocode outage = no Tier 2 external enrichment AT ALL. That is a regression against the current pipeline (which today has Tavily as the only external-source layer). The right move with Tavily is **complement, not replace**.

- **Candidate E (meta-signal)** scores worst on composability. Modifying the escalation rubric to take octocode's answer as input is a meaningful contract change — and the rubric is one of the most carefully calibrated parts of the protocol. The risk of mis-calibration (octocode false positive → don't escalate → bad diagnosis ships) is high.

- **Candidate D (Wave 1.5 Branch D)** scores worst on cost discipline. Wave 1.5 already runs 3 auggie branches at a target of ≤ 2k Claude tokens. Adding a 4th branch with cross-repo octocode calls realistically lands at 3-5k. The wave was deliberately designed as "retrieval-offload, not Claude reasoning"; expanding it muddies that.

- **Candidates A, C, G tie at 27.** They each address a *different* sliver of the wedge:
  - A — Tier 2 precedent enrichment (richer cards, debate participation)
  - C — Tier 1 package-version fast-path (cheap retrieval, no agent)
  - G — Tier 2 precedent retrieval (lighter than A, no diagnosis claim)

- **Candidate F (per-error-class routing)** scores well on coverage (5) but worst on op complexity. The routing matrix is right, but encoding it in the protocol creates a lot of branching logic the user must mentally model. It also encodes domain expertise that may go stale as octocode evolves.

### The synthesis question

> The strongest candidates either (1) act at Tier 2 with a precedent-only contract (A or G), (2) act at Tier 1 with a metadata-only call (C), or (3) replace Tavily entirely (B). Which combination, if any, maximizes value while staying inside the cost / hallucination / composability envelope?

---

## Wave 3: Convergence

**Best design = Hybrid C + A (NOT C + G, NOT B alone, NOT E).**

### Rationale

1. **C (Tier 1 `packageSearch` gated on third-party signal)** is the lowest-cost, highest-frequency win. Many bugs name a third-party library by URL or import path; a one-call lookup at Tier 1 catches the "version mismatch" / "deprecated method" / "wrong package" diagnoses *before* the user pays the Tier 2 escalation cost. This is the package-version archaeology wedge from the analysis. It composes cleanly with Wave 1 (parallel call alongside auggie + serena) and degrades gracefully (skip on failure).

2. **A (Tier 2 precedent agent, gated on `--type ∈ {bug, build, test}`)** is the higher-cost, higher-value win for the cases where Tier 1 *did* escalate. When the rubric says "this needs multiple perspectives," the addition of a cross-repo precedent perspective genuinely adds something the existing agents cannot — none of them have visibility into "has another OSS repo solved this exact symptom." The Precedent Card with permalinks gives the adversarial debate (Wave 4) a real-world anchor that the local-code-only hypotheses lack.

3. **Choosing A over G** because Wave 4's adversarial debate benefits from a structured perspective, not just a list of links. A precedent agent that *interprets* the linked PRs ("PR #4521 in `fastapi/fastapi` was the same NameError-on-imported-`Path` pattern; their fix was to add `from pathlib import Path` to the affected module") gives the debate something to weigh. G's raw link list is too thin to participate.

4. **Choosing C over D** because Wave 1.5 is deliberately a retrieval-offload wave. Adding a 4th branch inside it conflicts with its design contract. C runs at Wave 1 step 1, parallel to the existing auggie + serena calls — that's the natural place for a cheap retrieval call.

5. **NOT replacing Tavily (B)** because Tavily has a long tail (Stack Overflow, Discourse, GitHub Discussions outside the search API surface). The failure mode here is *complement, not replace*. Keep Tavily at 1 query (down from 2), allocate the other slot to octocode `searchPullRequests` for the GitHub-native case.

6. **NOT meta-signal (E)** because the escalation rubric is too carefully calibrated to take a novel external signal as input. If octocode adoption proves out, *then* consider rubric integration in a future iteration.

7. **NOT per-error-class routing (F) as the full design** because the operational complexity overhead is too high for v1. The Candidate A precedent agent can internally apply some of F's routing (which octocode tool to call per signal) without externalizing it into the protocol. F's matrix is a refinement to add inside the precedent-finder agent's brief, not a separate top-level concern.

8. **Composability check.** Hybrid C+A requires:
   - **2 lines** added to Wave 1 step 1 (conditional `packageSearch` call)
   - **~20 lines** added to Wave 3 (new agent in selection matrix + Precedent Card output path)
   - **New agent file** `precedent-finder.md` (~100 lines)
   - **1 row** added to the protocol's Tool Coordination Summary
   - **1 new report section** ("Precedent from other repos") in `refs/report-template.md`
   - **0 changes** to the escalation rubric, the file:line validation contract, or the hallucination contract
   - Hybrid C+A composes cleanly because it operates *additively* — every existing path still works if octocode is unavailable.

---

## Recommended Design (Deep Dive)

### Full description

**Name:** Octocode dual integration for `/sc:troubleshoot` — `packageSearch` at Tier 1, `precedent-finder` agent at Tier 2.

**Tier-1 path (Wave 1 step 1):**
- When the issue description OR stack trace OR scope path mentions a third-party package name (regex match on `pip install <X>`, `import <X>`, `from <X> import`, `<X>@<version>`, a top 1000 npm/PyPI package list, or the user passes `--package <name>`), fire ONE `mcp__octocode__packageSearch` call in parallel with auggie + serena.
- Capture: repo URL, current released version, installed version (parsed from `requirements.txt` / `package.json` / lockfile if accessible), deprecation status, link to most recent CHANGELOG entry.
- Persist to `<output-dir>/tier1-package-context.md`.
- Pass this artifact to the `root-cause-analyst` agent in Wave 1.7 as an additional input alongside the Documentation Context Card.
- No file:line claims are sourced from this artifact — it's metadata only.

**Tier-2 path (Wave 3):**
- The `precedent-finder` agent is added to the Wave 3 selection matrix for `--type ∈ {bug, build, test}`. It runs in parallel with the existing 2-4 specialist agents, increasing the cap from 4 to 5 *only when precedent-finder is selected*.
- The agent's brief: "Given symptom `<X>` and Tier 1 hypothesis `<Y>`, find up to 5 cross-repo PRs that addressed the same error signature. Return a Precedent Card with permalinks, quoted PR-description excerpts, and a confidence-in-similarity score for each."
- The agent uses (in this order): `githubSearchPullRequests` (primary), `githubSearchCode` (fallback for symptoms without clean PR titles), `githubGetFileContent` (to quote the fix diff from a winning PR).
- Output: `<output-dir>/tier2-precedent-finder.md` — a **Precedent Card** (template added to skill `refs/`).
- The Precedent Card does NOT compete in the Wave 4 adversarial fix debate as a *fix proposal*. Instead, it is appended to each `fix-<N>.md` proposal in Wave 4 step 1 as a `## Cross-repo precedent` section, so the debate agents can weigh "does this fix align with how `fastapi/fastapi#4521` solved the same problem?" — but they remain bound to file:line evidence in the *local* repo.
- Tavily's 2-query budget is reduced to 1 query (saved for the long-tail non-GitHub case); octocode `searchPullRequests` takes the other slot.

### Concrete diff sketch

**`src/superclaude/commands/troubleshoot.md` frontmatter:**

```diff
- mcp-servers: [auggie, serena, context7, tavily, sequential]
+ mcp-servers: [auggie, serena, context7, tavily, sequential, octocode]
```

```diff
- /sc:troubleshoot "API p99 jumped 10x after the widget refactor" --type performance
+ /sc:troubleshoot "API p99 jumped 10x after the widget refactor" --type performance
+ /sc:troubleshoot "DeprecationWarning from pydantic 2.6" --package pydantic
```

```diff
  | `--no-mcp` | `false` | Run in native-tools-only mode (skip auggie/serena/context7/tavily). Tier 1 quality degrades; surfaced in the report. |
+ | `--package` | (auto-detect) | Force a `packageSearch` call at Tier 1 even when no package name is auto-detected in the symptom. |
+ | `--no-precedent` | `false` | Skip the Tier 2 `precedent-finder` agent (saves octocode rate-limit budget on cases where cross-repo precedent is irrelevant, e.g. internal-only error). |
```

```diff
  ## MCP Integration

  - **Auggie** (primary, free retrieval): Tier 1, Wave 1.5 (documentation grounding fan-out across release artifacts + architectural docs + semantic restrictions), and Tier 2 codebase grounding via `mcp__auggie__codebase-retrieval`. ...
  - **Serena**: Tier 1 + Tier 2 symbol-level navigation via `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`. ...
  - **Context7**: Tier 2 only, when the symptom mentions a framework or library by name or the stack trace ends in third-party code.
- - **Tavily**: Tier 2 only, rate-limited to ≤ 2 queries per invocation. Used for `<exact error string> github issue` and `<library> <version> <symptom>` lookups.
+ - **Tavily**: Tier 2 only, rate-limited to ≤ 1 query per invocation (down from 2; one slot reallocated to octocode). Used for non-GitHub long-tail lookups (Stack Overflow, Discourse, GitHub Discussions outside the Search API surface).
+ - **Octocode**: Tier 1 (one `packageSearch` call gated on third-party-name signal in the symptom; auto-fired when the issue mentions a package by name, or forced via `--package <name>`) and Tier 2 (one `precedent-finder` agent that searches GitHub Issues/PRs for cross-repo precedents matching the symptom). Cross-repo data flows into the report as **precedent**, never as evidence — every Precedent Card hit carries a permalink and is rendered in a separate "Precedent" section.
  - **Sequential**: Tier 2 synthesis when reconciling competing hypotheses.
```

**`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 1 step 1:**

```diff
  1. **Ground the symptom in real code** — issue two parallel MCP calls (or fall back to native tools):
     - `mcp__auggie__codebase-retrieval` with query: "Find the code involved in: `<issue description, capped at ~300 chars>`. ..."
     - `mcp__serena__get_symbols_overview` on the target file or `mcp__serena__find_symbol` on a specific function if the issue names one.
+    - **If a third-party package name is detected** in the symptom (regex match on `pip install <X>`, `import <X>`, `from <X> import`, `<X>@<version>`, a top-1000 npm/PyPI package signal, OR `--package <name>` was passed): also issue `mcp__octocode__packageSearch` with `query=<package>`. Capture `repo_url`, `latest_version`, `installed_version` (parsed from `requirements.txt` / `package.json` / lockfile when accessible), `is_deprecated`, `recent_changelog_link`. Persist to `<output-dir>/tier1-package-context.md`. **Skip silently** if no package name detected (no escalation, no warning).
     - If `--no-mcp` or both MCPs are unavailable: fall back to `Glob` + `Grep` on the issue keywords; note the fallback in the audit log.
```

**`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 1.7 step 1 brief:**

```diff
- 1. **Form one hypothesis** — spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from Wave 1 step 1, the observation from Wave 1 step 2, the Documentation Context Card path ..., and `--scope` if any.
+ 1. **Form one hypothesis** — spawn the `root-cause-analyst` agent via `Task` with a focused brief: the symptom, the grounding from Wave 1 step 1, the observation from Wave 1 step 2, the Documentation Context Card path ..., **the Tier 1 Package Context at `<output-dir>/tier1-package-context.md` (or `null` if no package signal was detected at Wave 1 step 1)**, and `--scope` if any.
```

**`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 agent selection matrix:**

```diff
  | Signal / type | Agents to spawn |
  |---------------|------------------|
- | `bug` (default) | `root-cause-analyst`, `quality-engineer` (edge cases), + 1 of {`refactoring-expert` if recent refactor signals, `system-architect` if multi-component} |
+ | `bug` (default) | `root-cause-analyst`, `quality-engineer` (edge cases), + 1 of {`refactoring-expert` if recent refactor signals, `system-architect` if multi-component}, + `precedent-finder` (unless `--no-precedent`) |
  | `performance` | `performance-engineer`, `root-cause-analyst`, `system-architect` (if cross-component) |
  | `security` | `security-engineer`, `root-cause-analyst`, `quality-engineer` |
- | `build` | `root-cause-analyst`, `devops-architect`, `refactoring-expert` |
+ | `build` | `root-cause-analyst`, `devops-architect`, `refactoring-expert`, + `precedent-finder` (unless `--no-precedent`) |
  | `deployment` | `devops-architect`, `root-cause-analyst`, `system-architect` |
- | `test` | `quality-engineer`, `root-cause-analyst`, `refactoring-expert` (if test is brittle by structure) |
+ | `test` | `quality-engineer`, `root-cause-analyst`, `refactoring-expert` (if test is brittle by structure), + `precedent-finder` (unless `--no-precedent`) |

- Cap at 4 agents. If `--type` is unset and signals point in multiple directions, spawn 3 from the union of relevant rows.
+ Cap at 4 agents for the hypothesis tier; the precedent-finder is additive (cap → 5 when fired). If `--type` is unset and signals point in multiple directions, spawn 3 from the union of relevant rows, plus precedent-finder if any selected row is `bug|build|test`.
```

**`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 3 step 1 enrichment list:**

```diff
  1. **MCP enrichment in parallel with agent spawn** — issue any of the following that match the signals (parallel calls, all kicked off in the same turn):
     - `mcp__context7__resolve-library-id` + `mcp__context7__query-docs` when the issue mentions a framework / library by name or the stack trace is in third-party code
-    - `mcp__tavily__tavily-search` for the exact error message string + "github issue", or for `<library> <version> <symptom>` (rate-limited — at most 2 queries in this wave)
+    - `mcp__tavily__tavily-search` for non-GitHub long-tail lookups (Stack Overflow, Discourse, GitHub Discussions outside the Search API surface), rate-limited to ≤ 1 query in this wave
+    - `mcp__octocode__githubSearchPullRequests` for the exact error signature (exception class + key frame symbol), rate-limited to ≤ 2 queries in this wave; results pass to the `precedent-finder` agent as enrichment
     - `mcp__auggie__codebase-retrieval` with a more targeted query than Tier 1 ...
```

**`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` Wave 4 step 1 (fix proposal materialisation):**

```diff
- 1. **Materialise each candidate fix as a standalone file** — write `<output-dir>/fix-proposals/fix-<N>.md` for each, structured as a self-contained proposal (problem statement, proposed change, evidence, risks, test plan). **When a Documentation Context Card exists at `<output-dir>/doc-context.md`** ...
+ 1. **Materialise each candidate fix as a standalone file** — write `<output-dir>/fix-proposals/fix-<N>.md` for each, structured as a self-contained proposal (problem statement, proposed change, evidence, risks, test plan). **When a Documentation Context Card exists at `<output-dir>/doc-context.md`** ... [as today]. **When a Precedent Card exists at `<output-dir>/tier2-precedent-finder.md`** (i.e., the `precedent-finder` agent ran successfully): append a `## Cross-repo precedent` section to every fix-<N>.md containing a verbatim copy of the Precedent Card's hits. The debate weighs proposals against precedent, but the precedent is advisory — a fix that diverges from precedent is not automatically wrong (precedent may be wrong, or the local codebase may legitimately differ).
```

**New agent file: `src/superclaude/agents/precedent-finder.md`** (~100 lines, structured like other Wave-3 hypothesis agents):
- Purpose: cross-repo precedent retrieval ONLY; does not propose a fix, does not produce a hypothesis card
- Inputs: symptom, Tier 1 hypothesis card, `--scope`
- Tools: `mcp__octocode__githubSearchPullRequests`, `mcp__octocode__githubSearchCode`, `mcp__octocode__githubGetFileContent`, `mcp__octocode__packageSearch`
- Output: Precedent Card at `<output-dir>/tier2-precedent-finder.md` per `refs/precedent-card-template.md`
- Strict contract: every hit has (a) permalink to a specific PR or commit on github.com, (b) ≤ 200-char quoted excerpt, (c) similarity confidence score `[0.0, 1.0]`, (d) repo `stars` count for downstream trustworthiness weighting
- Filtering: drop hits with `stars < 50` OR `merged_at older than 18 months` OR `similarity_confidence < 0.5`
- Failure modes: rate limit → return partial card with `degraded: true`; zero hits → return card with `status: no_precedent_found`

**New ref: `src/superclaude/skills/sc-troubleshoot-protocol/refs/precedent-card-template.md`** — defines the Precedent Card schema.

**Updated `refs/report-template.md`** — add `## Precedent (cross-repo)` section between `## Evidence` and `## Risk + Rollback`, populated from the Precedent Card or marked `_None._` if not run / no hits.

**New MCP registry entry in `src/superclaude/cli/install_mcp.py`** (per fit-analysis §6, this is the prereq):

```python
"octocode": {
    "name": "octocode",
    "description": "GitHub/GitLab/Bitbucket semantic code research (used by /sc:troubleshoot + /sc:research)",
    "transport": "stdio",
    "command": "npx -y octocode-mcp@14.2.0",  # pinned per fit-analysis recommendation
    "required": False,
    "api_key_env": "GITHUB_TOKEN",
    "api_key_description": "GitHub PAT (or `gh auth login` reuse). Set LOG=false to opt out of telemetry. TOOLS_TO_RUN whitelist restricts to cross-repo tools only.",
    "env_extras": {
        "LOG": "false",
        "TOOLS_TO_RUN": "githubSearchCode,githubGetFileContent,githubSearchPullRequests,packageSearch,githubViewRepoStructure",
    },
},
```

### Tool subset used

| Octocode tool | Used by | When |
|---------------|---------|------|
| `packageSearch` | Wave 1 step 1 | When package name detected in symptom OR `--package` set |
| `githubSearchPullRequests` | Wave 3 enrichment + precedent-finder agent | Tier 2 only, `--type ∈ {bug, build, test}` |
| `githubSearchCode` | precedent-finder agent (fallback) | When PR-title search returns < 2 hits |
| `githubGetFileContent` | precedent-finder agent | To quote the fix diff from a winning PR |
| `githubViewRepoStructure` | precedent-finder agent (optional, rare) | When the precedent repo's layout matters for similarity scoring |

**Explicitly NOT used:** `localGetFileContent`, `localSearchCode`, `localFindFiles`, `localViewStructure`, `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`. These overlap with `Read`/`Grep`/serena/auggie and add no value.

### Error-class routing rules (which signatures trigger octocode)

| Symptom signature | Tier 1 packageSearch? | Tier 2 precedent-finder? |
|-------------------|----------------------|-------------------------|
| Stack trace, named exception class (`TypeError`, `NameError`, etc.) | NO (unless package name also present) | YES if `--type bug` |
| `DeprecationWarning`, "X is deprecated" | YES (package likely named) | YES if `--type bug` |
| `pip install` failed / dependency conflict | YES | YES if `--type build` |
| Build failure: `tsc`, `webpack`, `vite`, `babel`, `make` | NO | YES if `--type build` |
| Flaky test, intermittent CI fail | NO | YES if `--type test` |
| Performance regression (p99, memory leak) | NO | NO (precedent rarely transfers across infra) |
| Deployment / env-var / container | NO | NO (too local to the user's infra) |
| Security: CVE-named, XSS, IDOR | NO | NO (security precedent through CVE channels, not OSS PRs — handled by context7 + tavily today, no change) |

This routing lives inside the precedent-finder agent's brief (which `--type` it accepts) and inside Wave 1 step 1's "third-party package name detected" regex.

### Evidence contract: how octocode-sourced info flows into the report

**The bright line — precedent is NOT evidence.** Every octocode-sourced finding lands in a labeled "Precedent" section, never in the "Evidence" section. The distinction:

- **Evidence (existing contract)** — cited `file:line` in the *local* repo, validated by `evidence-validator` against the actual file. Drives the diagnosis and fix.
- **Precedent (new section)** — permalink to a PR/issue/commit on github.com (or gitlab.com / bitbucket.org), with a ≤ 200-char quoted excerpt, a similarity score, and the source repo's star count. Advisory context; informs but does not ground the diagnosis.

**Wave 5 step 2 of the protocol** — the report template gets a new `## Precedent (cross-repo)` section, rendered as:

```markdown
## Precedent (cross-repo)

The `precedent-finder` agent surfaced 3 cross-repo PRs that addressed the same error signature:

1. **[fastapi/fastapi#4521](https://github.com/fastapi/fastapi/pull/4521)** (★ 78k stars, merged 2024-08-15, similarity 0.86) — _"Fix NameError on `Path` when not explicitly imported in middleware."_ Fix: added `from pathlib import Path` to `fastapi/middleware/cors.py`.
2. **[encode/starlette#1839](https://github.com/encode/starlette/pull/1839)** (★ 10k stars, merged 2024-03-22, similarity 0.71) — _"Resolve `Path` typing namespace clash with `pathlib.Path`."_ Fix: alias import.
3. **[tiangolo/sqlmodel#823](https://github.com/tiangolo/sqlmodel/pull/823)** (★ 14k stars, merged 2025-01-10, similarity 0.58) — _"Add missing pathlib import."_ Fix: imports section update.

These are advisory. The diagnosis and fix below are grounded in the local repo's evidence (see §Evidence).
```

**`evidence-validator` does NOT validate precedent links** — those are external URLs, not file:line citations. The agent's own filtering (star count, age, similarity threshold) is the only QC. The protocol's hallucination contract holds because precedents are explicitly labeled as not-evidence.

### Hallucination safeguards

Troubleshoot reports get acted on. Precedent surfaces from other repos could mislead. Safeguards:

1. **Mandatory permalinks** — every Precedent Card hit must include a `github.com/<owner>/<repo>/pull/<N>` or `/commit/<sha>` URL. No prose-only references. The agent's output schema enforces this.
2. **Quoted excerpts ≤ 200 chars** — precedent-finder cannot paraphrase the PR description; it quotes a literal substring. This prevents the agent from "interpreting" a PR into something it isn't.
3. **Similarity score required** — every hit has a score `[0.0, 1.0]` based on exception class match, framework version match, error frame match. Scores < 0.5 are dropped at the agent level.
4. **Stars threshold + age threshold** — hits from repos with < 50 stars or PRs older than 18 months are dropped. (Tunable; starts conservative.)
5. **Report separation contract** — the "Precedent" section header explicitly reads "These are advisory. The diagnosis and fix below are grounded in the local repo's evidence." The user cannot read a precedent and mistake it for evidence.
6. **Wave 4 debate weighting** — when fix proposals are debated in `/sc:adversarial`, the prompt template explicitly says "weigh precedent as informative but not authoritative; a fix that diverges from precedent is not automatically wrong."
7. **`evidence-validator` boundary** — the validator runs over the Evidence section only. The Precedent section is excluded from its grounding check (correctly — those are external URLs). The audit log records `precedent_validated: false` to make this explicit.

### Rate-limit / failure handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| Octocode MCP not installed | Skip all octocode calls; existing pipeline runs unchanged; audit logs `octocode_available: false` | Tavily 2-query budget restored |
| `packageSearch` 403 (rate limit) at Tier 1 | Skip; do not block Tier 1; audit logs `packageSearch: rate_limited` | None — Tier 1 was always optional |
| `githubSearchPullRequests` 403 at Tier 2 | precedent-finder returns partial card with `status: rate_limited`; debate proceeds without precedent | Tavily 1-query slot still fires |
| All octocode calls fail | precedent-finder agent fails; existing 2-4 hypothesis agents complete normally; Precedent section in report reads "_None._ (octocode unavailable)" | None |
| Octocode response includes deleted/private repo | precedent-finder skips that hit; surfaces remaining hits | None |
| Telemetry leak concern | Mitigated at install via `LOG=false` env var in MCP registry config | None — opt-out is permanent |
| GitHub Search 30/min hit globally (multiple `/sc:troubleshoot` runs in parallel) | First request returns; second waits + retries once; on second failure surfaces partial | Cached at `~/.octocode/repos/` for 24h reduces duplicate cost |
| GitHub Enterprise needed | precedent-finder respects `GITHUB_HOST` env var; falls back to public if not set | Documented in install-time README |

### Test plan: 5 error signatures and how octocode handles each

**1. `NameError: name 'Path' is not defined at eval_run.py:142`**
- Wave 1 packageSearch: SKIP (no package named in symptom; pathlib is stdlib)
- Wave 3 precedent-finder: FIRE (`--type bug`, `searchPullRequests("NameError Path not defined" + label:bug)`)
- Expected hits: PRs in fastapi, starlette, sqlmodel, pydantic-ai that added `from pathlib import Path` after refactors
- Value-add: confirms diagnosis ("missing import") with 3-5 OSS PRs that took the same fix; debate weights this as supporting the import-fix proposal vs. alternative (rename collision)

**2. `pydantic 2.6 DeprecationWarning: Field 'description' is deprecated`**
- Wave 1 packageSearch: FIRE (pydantic named; resolves to pydantic-org/pydantic v2.6.0; CHANGELOG link)
- Wave 3 precedent-finder: FIRE (`--type bug`; `searchPullRequests("Field description deprecated", repo:pydantic/pydantic)`)
- Expected: the actual deprecation PR in pydantic that introduced it (provides the migration path verbatim)
- Value-add: Tier 1 may resolve without escalation if packageSearch's changelog link shows the fix; saves Tier 2 escalation cost

**3. Flaky pytest: `test_session_pool fails 1/5 runs since asyncio refactor`**
- Wave 1 packageSearch: SKIP (no package name)
- Wave 3 precedent-finder: FIRE (`--type test`; `searchPullRequests("flaky asyncio session pool" + label:flaky)`)
- Expected: SQLAlchemy, aiopg, asyncpg PRs labeled `flaky` that fixed similar race conditions
- Value-add: debate sees "3 other repos fixed this with a specific async-context teardown pattern"; biases toward that fix shape

**4. Build failure: `webpack: Module not found: Error: Can't resolve '@/components/Foo'`**
- Wave 1 packageSearch: FIRE (`@/components/Foo` indicates webpack alias; packageSearch on `webpack` to confirm version)
- Wave 3 precedent-finder: FIRE (`--type build`; `searchPullRequests("webpack Module not found alias")`)
- Expected: vercel/next.js, vitejs/vite, vuejs/core PRs that fixed alias-resolution config
- Value-add: surfaces config snippets from real production projects (PR diffs are gold for build config)

**5. Performance: `API p99 jumped 10x after the widget refactor`**
- Wave 1 packageSearch: SKIP (no package name)
- Wave 3 precedent-finder: SKIP (`--type performance` — routing matrix says perf precedents rarely transfer; skip to save rate budget)
- Behavior: octocode is a no-op for this case; existing tier 2 (sequential + performance-engineer + tavily) handles it
- Value-add: NEGATIVE here — and that's correct. The routing matrix's job is to skip octocode where it'd add noise.

### Why this is the right design (and what it costs)

**Wins:**
- Sharpens the worst part of the current pipeline (Tavily noise on error-string search) by giving Tier 2 a structured precedent perspective
- Adds a cheap Tier 1 fast-path for package-version archaeology (a real common case today escalated needlessly)
- Composes additively — every existing path still works if octocode is unavailable
- Respects the hallucination contract — precedent is rigidly separated from evidence
- Stays inside the cost envelope — Tier 1 stays in 3-6k Claude tokens (packageSearch is offloaded); Tier 2 adds ~5-10k for precedent-finder
- Uses octocode's strongest tools (`searchPullRequests`, `packageSearch`) which are also its highest signal-to-noise

**Costs:**
- 1 new agent file (precedent-finder), 1 new ref template (precedent-card-template), ~70 lines of protocol changes
- Adds octocode supply-chain risk (mitigated by pinned version, `LOG=false`, `TOOLS_TO_RUN` whitelist per fit-analysis §6)
- Reduces Tavily budget by 1 query (acceptable — the GitHub-issue lookup was Tavily's noisiest use)
- Tier 2 token cost increases by ~5-10k when precedent-finder runs (within stated budget; protocol already cites 15-30k for Tier 2)

---

## What This Cannot Do

- **Cannot replace Tavily for non-GitHub long-tail.** Stack Overflow, Discourse, GitHub Discussions outside the Search API surface still benefit from Tavily. The 1-query Tavily slot stays.
- **Cannot help when the bug is fully internal.** A bug in proprietary code with no OSS analog returns zero precedent hits. The pipeline is unaffected (no precedent section rendered), but octocode adds zero value.
- **Cannot validate cross-repo precedents against the local repo.** `evidence-validator` only checks file:line citations in the local repo. Precedent permalinks are taken on trust (the agent enforces the schema; the user enforces the verdict).
- **Cannot run on GitHub Enterprise without explicit `GITHUB_HOST` config.** Default config targets github.com; GHE users need to set `GITHUB_HOST` at MCP install time.
- **Cannot prevent supply-chain compromise of octocode itself.** Pinned version mitigates `@latest` install vector, but if v14.2.0 itself is compromised, the integration is compromised. Risk is contained by `TOOLS_TO_RUN` whitelist (cross-repo tools only — no local filesystem write capability surfaced to the LLM via octocode).
- **Cannot operate without a `GITHUB_TOKEN`.** Anonymous GitHub Search API limits (10/min) are too tight; the install path requires `GITHUB_TOKEN` or `gh auth login` reuse.
- **Cannot help with security-typed troubleshoots.** Security routing matrix says skip — CVE context comes from context7 + tavily, not OSS PRs (CVE workflow has its own channels).
- **Cannot accelerate Tier 1 when the package signal is absent.** If the symptom is pure first-party code with no library named, Tier 1 packageSearch skips, no acceleration.

---

## Cross-Target Dependencies

### Does troubleshoot go through deep-research, or directly?

**Directly.** `/sc:troubleshoot` does NOT invoke `/sc:research` or the `deep-research` agent. It uses MCP tools directly (auggie, serena, context7, tavily, sequential) and spawns specialist agents (`root-cause-analyst`, `quality-engineer`, etc.) via `Task`. Adding octocode to `deep-research` (Target #1's likely focus) does NOT propagate to troubleshoot.

**This means troubleshoot's octocode integration is independent of Target #1's outcome.** They can ship in either order or together.

### Can this ship standalone?

**Yes, with one prerequisite: the MCP server registration.** Fit-analysis §6 calls out `install_mcp.py:29` as the foundational PR — without it, octocode isn't available as an MCP server in the framework's install path, and the troubleshoot integration would have nothing to call.

**Shipping order:**
1. **Prereq PR:** MCP server registration in `install_mcp.py` (5-line dict entry; per fit-analysis Phase A)
2. **This PR:** troubleshoot dual integration (Tier 1 `packageSearch` + Tier 2 `precedent-finder` agent)

The two PRs are independent of Target #1 (deep-research), Target #2 (tech-research), Target #3 (sc:research command), and Target #4 (sc-brainstorm-protocol). All five targets share only the MCP registration prereq.

### Compatibility with downstream consumers

`/sc:troubleshoot`'s output contract (`status`, `tier_reached`, `report_path`, etc.) is consumed by:
- The Tier 3 `task-builder` chain (uses `report_path` to BUILD_REQUEST a fix)
- Fleet auto-apply wrappers (use `test_is_wrong` + `behavior_is_documented` flags)
- Telemetry (records `tier_reached` + `escalation_reason`)

**The integration adds NO new output contract fields.** Precedent Card is an internal artifact at `<output-dir>/tier2-precedent-finder.md` and an embedded section in `REPORT.md`. Downstream consumers see the same contract. **Zero breaking changes.**

Optional: add a `precedent_card_path` field (analogous to existing `doc_context_card_path`) for completeness — non-breaking addition.

---

## Effort Estimate

| Work item | LoC | Tokens (development) | Calendar |
|-----------|-----|---------------------|----------|
| MCP registry entry in `install_mcp.py` (prereq) | ~15 | ~2k | 0.5h |
| New `precedent-finder.md` agent file | ~100 | ~6k | 2h |
| New `refs/precedent-card-template.md` | ~40 | ~2k | 0.5h |
| `troubleshoot.md` command frontmatter + MCP Integration section update | ~25 | ~2k | 0.5h |
| `sc-troubleshoot-protocol/SKILL.md` Wave 1 step 1 + Wave 1.7 step 1 + Wave 3 selection matrix + Wave 3 step 1 + Wave 4 step 1 + Tool Coordination Summary updates | ~70 | ~6k | 2h |
| `refs/report-template.md` — add Precedent section | ~20 | ~1k | 0.25h |
| Tests: 5 error-signature scenarios from the Test Plan section | ~200 (pytest fixtures + recorded MCP responses) | ~10k | 3h |
| Docs: update `docs/user-guide/sc-troubleshoot.md` | ~30 | ~2k | 0.5h |
| Sync: `make sync-dev` + `make verify-sync` | 0 | ~0.5k | 0.25h |
| **Total** | **~500 LoC** | **~31.5k tokens** | **~9.5h** (one focused day) |

**Risk reserve:** +2-3h for integration debugging (octocode response shape surprises, rate-limit edge cases, agent template iteration).

**Total realistic estimate:** 1 focused engineering day for the dual integration (Tier 1 packageSearch + Tier 2 precedent-finder), plus the prereq MCP registration PR.

---

**Status:** Brainstorm complete for Target #5.
**Recommended design:** Hybrid C+A (Tier 1 packageSearch + Tier 2 precedent-finder agent).
**Composes cleanly with:** Targets #1-#4 (no overlap, shared prereq only). Can ship in any order after MCP registration lands.
