# Brainstorm — Target #6: /tdd Skill

**Date:** 2026-05-30
**Status:** Complete

**Target file:** `src/superclaude/skills/tdd/SKILL.md` (433 lines read)
**Sibling brainstorm:** `brainstorm/02-tech-research-phase4.md` (Phase 4 routing pattern, T2)
**Source documents read:**
- `src/superclaude/skills/tdd/SKILL.md` (lines 1–433)
- `brainstorm/02-tech-research-phase4.md` (recommended W1-B router pattern for tech-research)
- `octocode-research.md` §2 Tool Surface, §3 Strengths (skimmed via headers + prior context)

---

## Section 1: Target Context

The `/tdd` skill (SKILL.md:1–433) is the higher-stakes cousin of `tech-research`. Where tech-research produces a research report, `/tdd` produces a **Technical Design Document** — a normative engineering spec that downstream teams build from. The cost of a wrong claim is materially higher: a hallucinated architectural pattern in a TDD becomes implementation guidance.

### Tier table (SKILL.md:69–73)

| Tier | When | Codebase Agents | Web Agents | Target Lines |
|------|------|-----------------|------------|-------------|
| **Lightweight** | Single service or component, <5 relevant files | 2–3 | **0–1** | 300–600 |
| **Standard** | Full component or subsystem, 5–20 files | 4–6 | **1–2** | 800–1,400 |
| **Heavyweight** | Platform-scale design, 20+ files | 6–10+ | **2–4** | 1,400–2,200 |

**Critical observation:** Web Agent capacity is **smaller than tech-research's** at every tier. Lightweight TDDs may have **zero** web agents (vs. tech-research Quick which has 1–2). This means any per-agent integration design must work with as few as zero web agents at the small end and as many as four at the large end.

### Phase structure (SKILL.md:140–148)

The phases inside the MDTM task file:

- Phase 1: Preparation — Scope confirmation, template read, tier selection
- Phase 2: Deep Investigation — Parallel codebase subagents
- Phase 3: Completeness Verification — rf-analyst + rf-qa research gate
- **Phase 4: Web Research — Optional external research for design patterns, framework docs, API references** (SKILL.md:144)
- Phase 5: Synthesis + Analyst + QA Synthesis Gate
- Phase 6: Assembly — rf-assembler + rf-qa structural + rf-qa-qualitative content review
- Phase 7: Present to User & Complete Task

**Phase 4 position:** Optional, between completeness verification (3) and synthesis (5). The word "Optional" at SKILL.md:144 is load-bearing — Lightweight tier may skip Phase 4 entirely. This is a structural difference from tech-research where Phase 4 is mandatory.

### PRD-as-input mechanic (SKILL.md:36–48, 210, 264–266)

The PRD ingestion path is the unique aspect of `/tdd`:

- SKILL.md:44 — "PRD reference (optional but strongly recommended)... The PRD feeds the TDD the same way tech-research feeds a tech-reference"
- SKILL.md:210 — Scope discovery extracts from PRD: epics, user stories, acceptance criteria, technical requirements, technology stack, success metrics/KPIs, scope boundaries
- SKILL.md:264–266 — `PRD_CONTEXT` is a required section of research-notes.md; written as a structured extract of the PRD
- SKILL.md:104 — PRD extraction file lives at `${TASK_DIR}research/00-prd-extraction.md`

The PRD path is the natural injection site for "what have other projects built that resembles this requirement?" — a question Tavily cannot answer well but octocode's `githubSearchPullRequests` + `packageSearch` can.

### Output destination (SKILL.md:111)

Final TDD: `docs/[domain]/TDD_[COMPONENT-NAME].md`. Research artifacts persist at `.dev/tasks/to-do/TASK-TDD-*/`. Template schema is `src/superclaude/examples/tdd_template.md`.

### Anti-hallucination posture (SKILL.md:28)

> "Hallucinated design details — By separating research (what exists) from synthesis (what it means for the design) from assembly (the final TDD), each phase can be verified independently."

This is the key differentiator vs tech-research: every claim in a TDD is supposed to trace to verified codebase evidence. **External (octocode) evidence in a TDD is a special case** — it's *precedent*, not *truth*. The design must be careful that octocode findings don't get treated as gospel by Phase 5 synthesis or Phase 6 assembly.

### Refs file loading contract (SKILL.md:412–430)

The Phase Loading Contract is structurally important: refs files (`agent-prompts.md`, `synthesis-mapping.md`, `validation-checklists.md`, `operational-guidance.md`) are loaded by specific actors at specific phases. **Agent prompts live in `refs/agent-prompts.md`** — not in SKILL.md directly. This means any new octocode-aware prompt template must be added to `refs/agent-prompts.md`, not pasted into SKILL.md.

This is a meaningful architectural difference from `tech-research`, where prompt templates are inline in SKILL.md. The `/tdd` integration must respect the refs/ split.

---

## Section 2: Wave 1 — Divergent Ideation

Eight candidates, deliberately heterogeneous in *where* in the SKILL they intervene and *how much* structural change they impose. Ordered roughly from "lowest touch" to "largest restructure."

### Candidate A — Mirror T2's build-time routed buckets exactly

**Description:** Port the W1-B winner from tech-research's brainstorm directly into `/tdd` Phase 4. Add the same github-flavored / open-web classification heuristic to the BUILD_REQUEST; add a GitHub Research Agent Prompt to `refs/agent-prompts.md`; keep Phase 4 a single parallel batch.

**How it works:** rf-task-builder classifies each web-research topic from `SUGGESTED_PHASES.web_research_topics` into one of two buckets using the same trigger words T2 uses. Each Phase 4 checklist item embeds the appropriate prompt. The classification is deterministic and lives in the task file at build time.

**Octocode tools used:** `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch` (for github-flavored items); `packageSearch` + `githubGetFileContent` as fallback for open-web items.

**Where in SKILL.md it touches:**
- Phase 4 description in BUILD_REQUEST (the analog of tech-research's SKILL.md:415–419 — in `/tdd` this lives in `refs/agent-prompts.md` per the loading contract)
- New GitHub Research Agent Prompt template in `refs/agent-prompts.md`
- Tier table notes — no change to web agent counts at 69–73

### Candidate B — NEW dedicated Phase 3.5 "External Reference Architecture Discovery"

**Description:** Don't touch Phase 4 (Tavily web research) at all. Insert a new **Phase 3.5: External Reference Architecture Discovery** between completeness verification (3) and web research (4). Phase 3.5 spawns N parallel octocode agents whose sole job is to find 2–3 real-world reference implementations of the architectural patterns identified in Phase 2 codebase research.

**How it works:** For each major architectural pattern identified in Phase 2 (e.g., "agent registration system", "event sourcing", "wizard state machine"), Phase 3.5 spawns one octocode agent that runs `githubSearchCode` + `githubSearchPullRequests` + `packageSearch` to find canonical implementations in 2–3 reference repos. Output lands at `${TASK_DIR}research/precedent-NN-*.md`. Phase 5 synthesis reads both `web-*` and `precedent-*` files. The classification is structural (precedents = code; web = narrative), not heuristic.

**Octocode tools used:** Full primary toolset for Phase 3.5; Phase 4 unchanged (Tavily-only).

**Where in SKILL.md it touches:**
- Phase structure list at SKILL.md:140–148 (add Phase 3.5)
- BUILD_REQUEST phase enumeration in `refs/agent-prompts.md`
- New "External Reference Architect Agent Prompt" template in `refs/agent-prompts.md`
- `refs/synthesis-mapping.md` — synthesis agents must learn the new `precedent-*` file class
- Tier table — adds 0/1/2 precedent agents per tier (Lightweight/Standard/Heavyweight)

### Candidate C — Augment ALL web research agents uniformly

**Description:** No new phase, no routing, no new prompt template. Just add octocode tools to every Phase 4 agent's available toolset and add one paragraph to the existing Web Research Agent Prompt telling the agent "you have octocode; use it when the topic touches code-on-GitHub."

**How it works:** Pure capability injection — the BUILD_REQUEST adds octocode tools to the tool whitelist for every Phase 4 spawned agent. The prompt gets one routing-hint paragraph. The LLM decides per-call which tool to use.

**Octocode tools used:** All 5 cross-repo tools, available to every Phase 4 agent; usage is LLM-discretionary.

**Where in SKILL.md it touches:**
- Web Research Agent Prompt in `refs/agent-prompts.md` (one paragraph addition)
- BUILD_REQUEST tool whitelist for Phase 4 items

### Candidate D — Per-TDD-section routing (Architecture → octocode; Implementation → Tavily)

**Description:** Route Phase 4 agents not by topic-class but by **which TDD template section they will eventually feed**. The TDD template (`src/superclaude/examples/tdd_template.md`) has sections like "Architecture", "Components", "Data Model", "API Surface", "Implementation Notes", "Testing Strategy". Architecture-shaped sections → octocode; Implementation/Testing-shaped → Tavily.

**How it works:** `refs/synthesis-mapping.md` already maps research files to template sections. Inverse-map at build time: for each template section that will need synthesis input, decide which tool best serves it, then choose the matching prompt template. Architecture/Components/API Surface → GitHub Research Agent Prompt. Implementation Notes/Testing Strategy → Web Research Agent Prompt.

**Octocode tools used:** All 5 primary, routed by section semantics rather than topic keywords.

**Where in SKILL.md it touches:**
- `refs/synthesis-mapping.md` (inverse routing table)
- `refs/agent-prompts.md` (both prompts available)
- BUILD_REQUEST Phase 4 emission logic

### Candidate E — PRD-driven precedent pre-pass BEFORE Phase 2

**Description:** Insert a new **Phase 1.5: PRD Precedent Discovery** between Preparation (1) and Deep Investigation (2). When a PRD is provided, this phase spawns 1–3 octocode agents that read `${TASK_DIR}research/00-prd-extraction.md` and for each major epic/requirement search GitHub for projects that implemented something similar. Findings go into a `prd-precedents.md` file that **becomes part of the input context for Phase 2 codebase agents** — "before you investigate our code, here's what comparable projects look like."

**How it works:** PRD epics + acceptance criteria are queried against `githubSearchPullRequests` ("added X feature", "implemented Y") and `githubSearchCode`. Results inform the codebase investigation by surfacing "what to look for" in Phase 2.

**Octocode tools used:** `githubSearchPullRequests`, `githubSearchCode`, `packageSearch`.

**Where in SKILL.md it touches:**
- Phase structure list at SKILL.md:140–148 (insert Phase 1.5)
- New "PRD Precedent Agent Prompt" in `refs/agent-prompts.md`
- Scope discovery A.3 (SKILL.md:192–236) — add precedent discovery as a sub-step
- Skip-if-no-PRD logic; tier-gated to Standard+ only

### Candidate F — Tier-gated (Heavyweight only)

**Description:** Restrict octocode usage to Heavyweight TDDs only. Lightweight (0–1 web agents) and Standard (1–2 web agents) keep Tavily-only Phase 4. Heavyweight (2–4 web agents) gets the W1-B routing pattern.

**How it works:** rf-task-builder checks the tier flag. If `tier == heavyweight`, emit routed Phase 4 items (Candidate A behavior). Otherwise, emit standard Tavily-only items. The rationale is rate-limit safety: Heavyweight runs have the largest agent budget and the most justifiable need for cross-repo precedent.

**Octocode tools used:** Full primary toolset, but only at Heavyweight tier.

**Where in SKILL.md it touches:**
- Tier table at SKILL.md:69–73 (add octocode column or footnote)
- BUILD_REQUEST tier-conditional logic
- `refs/agent-prompts.md` (both prompts available)

### Candidate G — Hybrid: routed Phase 4 + new packageSearch mini-phase

**Description:** Combine A (routed Phase 4) with a small additive **Phase 4.5: Package Source Verification** that runs only when Phase 2 codebase research identified third-party packages whose behavior matters to the design. This mini-phase uses ONLY `packageSearch` + `githubGetFileContent` to read the actual source of those packages.

**How it works:** rf-task-builder scans Phase 2 research files for third-party package mentions. For each "load-bearing" package (heuristic: mentioned in 2+ research files OR mentioned in `PRD_CONTEXT` technical requirements), emit a Phase 4.5 item that reads the package source. Phase 4 itself uses the W1-B routing. Phase 4.5 outputs feed Phase 5 synthesis.

**Octocode tools used:** `packageSearch` + `githubGetFileContent` for Phase 4.5; full toolset for Phase 4 github-flavored items.

**Where in SKILL.md it touches:**
- Phase structure list at SKILL.md:140–148 (insert Phase 4.5)
- BUILD_REQUEST gets package-mention scanner + Phase 4.5 emission logic
- `refs/agent-prompts.md` gets two new prompts (GitHub Research + Package Source Reader)

### Candidate H — PRD → octocode precedent map fed into Phase 2 scope

**Description:** Lighter-weight cousin of E. No new phase. Instead, **Stage A.3 (Scope Discovery, SKILL.md:192–236)** itself runs octocode queries when a PRD is provided, and adds an `EXTERNAL_PRECEDENTS` section to `research-notes.md`. Phase 2 codebase agents then receive this precedent context as part of their assignment.

**How it works:** During Stage A.3, if PRD is present, the orchestrator (or an `rf-task-researcher` subagent if spawned) runs `packageSearch` on PRD-mentioned technologies and `githubSearchPullRequests` for PRD-described features. The findings are summarized in `research-notes.md` under a new `EXTERNAL_PRECEDENTS` section. Phase 4 stays unchanged.

**Octocode tools used:** `packageSearch`, `githubSearchPullRequests`, `githubSearchCode` — invoked from Stage A (orchestrator or researcher subagent), not from Phase 4 agents.

**Where in SKILL.md it touches:**
- Stage A.3 description at SKILL.md:192–236 (add precedent discovery sub-step)
- Stage A.4 research notes structure at SKILL.md:243–286 (add EXTERNAL_PRECEDENTS section to the 8-category template, making it 9)
- No Phase 4 changes

---

## Section 3: Wave 2 — Adversarial Evaluation

Scoring rubric (1–5, higher is better; total /25):

- **Architectural Fit** — does it respect /tdd's refs/ split, phase contract, and PRD-as-input flow?
- **Value Add** — does it actually exploit octocode's unique cross-repo capability for TDD-relevant questions?
- **Token Efficiency** — token + wall-clock cost per run (inverted; lower cost → higher score)
- **Risk** — hallucination, rate-limit, drift surface (inverted)
- **Effort** — LoC + reviewer cognitive load (inverted)

| Candidate | Arch Fit | Value Add | Token Eff | Risk⁻¹ | Effort⁻¹ | Total |
|---|---|---|---|---|---|---|
| **A** Mirror T2 build-time routing | 5 | 4 | 4 | 4 | 4 | **21** |
| **B** New Phase 3.5 precedent discovery | 4 | 5 | 2 | 3 | 2 | **16** |
| **C** Augment all agents uniformly | 3 | 2 | 4 | 3 | 5 | **17** |
| **D** Per-TDD-section routing | 4 | 4 | 3 | 3 | 2 | **16** |
| **E** PRD-driven precedent pre-pass (Phase 1.5) | 5 | 5 | 2 | 3 | 2 | **17** |
| **F** Tier-gated (Heavyweight only) | 4 | 3 | 5 | 5 | 4 | **21** |
| **G** Hybrid routed + packageSearch mini-phase | 4 | 5 | 2 | 3 | 1 | **15** |
| **H** PRD → octocode in Stage A scope discovery | 5 | 4 | 4 | 4 | 4 | **21** |

### Adversarial critique per candidate

**A (21):** The known-good design. Carries over T2's homework. Architectural Fit 5 — the routing pattern is already validated by the T2 brainstorm and respects the refs/ split (prompt goes in `refs/agent-prompts.md`, not SKILL.md). Value Add 4 (not 5) because TDDs may *want* precedent that the heuristic misses — Tavily-classified topics won't get octocode treatment even when they should. **Risk:** copy-paste convergence — by mirroring T2, /tdd loses any opportunity to do something better-suited to TDDs specifically (e.g., precedent for PRD epics).

**B (16):** The "do it right" version that pays for it. Value Add 5 (precedent discovery is structurally separate, can't be missed). Token Efficiency 2 — adds a whole new phase with N parallel agents per run; Heavyweight runs balloon by 2 more agents. Risk⁻¹ 3 — new phase = new synthesis input class = new opportunity for QA misses. Effort⁻¹ 2 — touches SKILL.md phase enumeration, refs/agent-prompts.md, refs/synthesis-mapping.md, tier table. Worth pursuing as a *follow-up* to A, not as the first integration.

**C (17):** The cheap-and-cheerful version. Effort 5. But Value Add 2 — same fallback-to-familiar bias T2's brainstorm identified at scale (~70% Tavily preference). Architectural Fit 3 — does not respect the refs/ split clearly (where does the routing hint go — SKILL.md or refs/?). Risk 3 — silent under-use is hard to QA.

**D (16):** Conceptually clean — route by destination not source. But the routing logic now lives in two places (synth-mapping inverse table + BUILD_REQUEST emitter) which doubles the drift surface. Effort 2 because the inversion of synth-mapping is non-trivial. Value Add 4 because Architecture sections genuinely benefit from cross-repo precedent. Worth exploring later if we ship A and find that topic-keyword classification misroutes too often.

**E (17):** The PRD-native design. Value Add 5 — PRD precedent is the killer use case octocode was built for, and TDDs are the *only* SuperClaude skill that ingests PRDs. Architectural Fit 5 because it leverages an existing structural feature (PRD ingestion) rather than fighting it. Token Efficiency 2 — adds an entire pre-pass phase before Phase 2 even runs; Phase 2 codebase agents now have larger context windows. Risk⁻¹ 3 — precedent context risks biasing Phase 2 codebase investigation toward what other projects do rather than what *our* code does. Effort⁻¹ 2 — touches Phase enumeration, new prompt template, new agent type or new scope-discovery sub-step. **Strong candidate for runner-up or combination with A.**

**G (15):** Hybrid is the maximalist version. Lowest total because the cost of two new prompts + a new phase + the routing scanner exceeds the marginal value over A. Useful as a vision of where the integration could end up after 2–3 PRs of evolution.

**F (21):** The conservative-deploy approach. Tier-gating eliminates the rate-limit risk for the bulk of runs (Lightweight + Standard are the majority of TDD invocations). Risk⁻¹ 5 because Lightweight runs literally can't trigger octocode. Token Efficiency 5 because most runs see no change. Value Add 3 because Standard tier (the most common!) doesn't get the benefit. Useful as a **deployment-strategy modifier** more than a standalone candidate — i.e., "ship A, but gate it to Heavyweight first as a rollout."

**H (21):** The upstream-routing approach, tied with A and F. Architectural Fit 5 because it cleanly leverages the existing Stage A → research-notes → BUILD_REQUEST data flow. Value Add 4 — precedent context informs all of Phase 2/4/5 rather than just Phase 4. Token Efficiency 4 because work happens in serial (orchestrator main thread or one researcher subagent) so wall-clock is smaller than B/E even if octocode calls happen. Risk⁻¹ 4 — failure is bounded to Stage A; Phase 4 unaffected. Effort⁻¹ 4 — single section addition to research-notes + small Stage A.3 change. **Strong runner-up.**

### Crossover combinations

- **A + F (deployment strategy)** — Ship A's design but gate it behind tier=Heavyweight initially; expand to Standard after rollout validates the classifier. This is the lowest-risk first deployment.
- **A + H** — Ship A for Phase 4 routing AND H's Stage A precedent map. The two integrations are non-overlapping: A handles in-phase web research; H handles upstream PRD-driven context. Together they hit both natural injection points without inflating Phase count.
- **A + E** — Heavier version of A + H. E adds a whole new phase (1.5) where H just adds a section to research-notes. Defer E in favor of H for now.
- **B + G** — Maximalist. Defer to v3 of the integration.

---

## Section 4: Wave 3 — Convergence + Recommended Design

### Winner: **A + H + F-as-rollout-gate**

The recommended design composes three of the high-scoring candidates:

1. **A — Mirror T2's build-time routed buckets** for Phase 4 (the in-phase integration)
2. **H — PRD → octocode in Stage A scope discovery** as an `EXTERNAL_PRECEDENTS` section in research-notes.md (the upstream integration)
3. **F — Tier-gated rollout** as a *deployment strategy*, not a permanent restriction (Heavyweight first → Standard after validation)

**Runner-up: A alone** (if effort budget is tight, ship A by itself; H can come in a follow-up PR).

### Rationale

- **A is the proven pattern.** The T2 brainstorm did the analytical work — copying the design across to /tdd avoids re-litigating the routing question and preserves a consistent mental model for users of both skills.
- **H adds the PRD-specific value** that T2 didn't have to consider. /tdd is the only SuperClaude skill that ingests PRDs, and PRD epics are the textbook use case for `githubSearchPullRequests` precedent discovery. Putting that work in Stage A (research-notes) rather than a new Phase 1.5 (Candidate E) avoids inflating the phase count and respects the "Stage A discovers, Stages B execute" boundary.
- **F as rollout strategy** addresses the genuine concern that Lightweight TDDs (0–1 web agents) don't need cross-repo precedent and Standard TDDs may not justify the rate-limit risk on day 1. Ship Heavyweight-only first; validate; widen to Standard.

### Concrete BEFORE/AFTER diffs

**Diff 1 — Phase 4 description in `refs/agent-prompts.md` (the analog of tech-research's SKILL.md:415–419).**

The current /tdd Phase 4 description is encoded in `refs/agent-prompts.md` (per the Phase Loading Contract at SKILL.md:412–430). The change mirrors T2:

```diff
 Phase 4 — Web Research (PARALLEL SPAWNING; OPTIONAL FOR LIGHTWEIGHT):
 - One checklist item PER web research topic from research notes SUGGESTED_PHASES
-- Each item spawns an Agent subagent with the Web Research Agent Prompt
+- Each item spawns an Agent subagent with one of two embedded prompts based on topic classification:
+    - **github-flavored** (cross-repo source archaeology, package implementations, GitHub issues/PRs/discussions,
+      "how do real projects solve X", "community solutions") → embed the GitHub Research Agent Prompt
+    - **open-web** (blog posts, conference talks, vendor whitepapers, tutorials, framework documentation sites)
+      → embed the existing Web Research Agent Prompt
+- The task builder classifies each topic using the heuristic in the BUILD_REQUEST.
+- TIER GATE (rollout phase 1): github-flavored items are emitted ONLY when tier == Heavyweight.
+  Lightweight and Standard tiers receive Tavily-only Phase 4 items.
+  When tier-gating is later relaxed to Standard, this gate becomes: tier ∈ {Standard, Heavyweight}.
+- Octocode rate-limit caps: Heavyweight ≤ 4 github-flavored items per Phase 4.
```

**Diff 2 — Tier table at SKILL.md:69–73.** Add a footnote:

```diff
 | Tier | When | Codebase Agents | Web Agents | Target Lines |
 |------|------|-----------------|------------|-------------|
 | **Lightweight** | Single service or component, narrow scope, <5 relevant files | 2–3 | 0–1 | 300–600 |
 | **Standard** | Full component or subsystem, 5-20 files, moderate complexity | 4–6 | 1–2 | 800–1,400 |
 | **Heavyweight** | Platform-scale design, multiple services/layers, 20+ files | 6–10+ | 2–4 | 1,400–2,200 |
+
+**Octocode-routed web agents (rollout phase 1):** Heavyweight tier only. Up to 4 of the
+2–4 web agents are emitted as github-flavored (octocode-driven) cross-repo precedent agents
+via the routed Phase 4 protocol. Lightweight and Standard tiers keep Tavily-only Phase 4
+until classifier validation completes.
```

**Diff 3 — Stage A.3 Discovery steps at SKILL.md:201–224.** Insert step 2.5:

```diff
 2. **Map the component's files and directories** — enumerate:
    - ...
    - **If PRD_REF is provided**, read the PRD and extract: relevant epics, user stories,
      acceptance criteria, technical requirements, technology stack, success metrics/KPIs,
      scope definition (in/out/deferred), performance/security/scalability requirements.
+
+2.5. **PRD-driven precedent discovery (if PRD_REF provided AND tier == Heavyweight)** —
+    For each major epic or technical requirement from the PRD, run octocode queries to
+    surface 1–2 real-world reference implementations:
+    - `mcp__octocode__packageSearch` on technologies named in the PRD's technology stack
+    - `mcp__octocode__githubSearchPullRequests` for "implemented [epic-name]" or
+      "added [feature-name]" patterns
+    - `mcp__octocode__githubSearchCode` with repo: qualifier when the PRD references a
+      specific OSS project as inspiration
+    Cap: max 6 octocode calls during Stage A scope discovery to keep wall-clock bounded.
+    Findings feed the EXTERNAL_PRECEDENTS section of research-notes.md (see A.4).
```

**Diff 4 — Stage A.4 research-notes template at SKILL.md:243–286.** Add a 9th category between SOLUTION_RESEARCH and RECOMMENDED_OUTPUTS:

```diff
 ## SOLUTION_RESEARCH
 [If the design involves evaluating multiple approaches: ...]
+
+## EXTERNAL_PRECEDENTS
+[If Stage A.3 step 2.5 ran (PRD + Heavyweight): for each PRD epic or technical
+requirement, list 1–2 reference repos discovered via octocode. Per finding: owner/repo,
+star count, last-commit date, the PRD epic this relates to, and a 1–2 sentence
+description of how the reference repo implemented the analogous capability. If step 2.5
+did not run, write "N/A — Stage A precedent discovery not triggered (no PRD or non-Heavyweight tier)."]
 
 ## RECOMMENDED_OUTPUTS
```

**Diff 5 — New GitHub Research Agent Prompt in `refs/agent-prompts.md`.** Add the same prompt the T2 brainstorm specified (lines 307–376 of `02-tech-research-phase4.md`), with **one TDD-specific addition** to the closing IMPORTANT paragraph:

```
IMPORTANT: Our codebase is the source of truth. Cross-repo evidence shows what others
have done — it does not dictate what we should do. Findings from this phase are
**PRECEDENT, not specification**. The synthesis phase must explicitly mark precedent-
derived design choices with a [PRECEDENT: owner/repo@path] tag so the assembly phase
and QA can distinguish "design we chose because the codebase requires it" from "design
we adopted because other projects do it this way."
```

**Diff 6 — New BUILD_REQUEST classification block** (octocode classification heuristic) — same shape as T2's W1-B classifier, added to the BUILD_REQUEST section of `refs/agent-prompts.md`.

**Diff 7 — Synthesis-mapping update in `refs/synthesis-mapping.md`.** Add a rule:

```
PRECEDENT TAGGING:
When synthesizing from a web-NN-github-*.md file, any design claim derived from a
cross-repo finding MUST be marked in the synthesis output as:
  [PRECEDENT: owner/repo@branch:path:line]
This tag is preserved through assembly into the final TDD's "Design Rationale" or
"Alternatives Considered" subsections. Rationale: TDDs are normative; precedent is
informative. The reader of the final TDD must be able to distinguish the two.
```

### Tool subset used (recommended design)

| Use site | Required octocode tools | Allowed octocode fallback | Required other tools |
|---|---|---|---|
| Stage A.3 PRD precedent (Heavyweight + PRD only) | `packageSearch`, `githubSearchPullRequests`, `githubSearchCode` | n/a | n/a |
| Phase 4 github-flavored | `githubSearchCode`, `githubSearchPullRequests`, `githubGetFileContent`, `githubViewRepoStructure`, `packageSearch` | n/a | Tavily + WebFetch (rate-limit fallback) |
| Phase 4 open-web | (none required) | `packageSearch`, `githubGetFileContent` (read-only fallback) | Tavily, WebFetch, WebSearch, Context7 |

**Explicitly NOT used:** `localSearchCode`, `localViewStructure`, `localFindFiles`, `localGetFileContent`, `lspGotoDefinition`, `lspFindReferences`, `lspCallHierarchy`, `githubCloneRepo` — same restriction as T2.

### Anti-trigger rules

A /tdd agent (Stage A or Phase 4) MUST NOT use octocode tools when:

1. **The topic is about the local codebase** — Phase 2 codebase research handles this.
2. **The topic is about canonical library API surface** — use `context7` instead.
3. **The topic is about news, current events, vendor announcements, or pricing** — Tavily/web only.
4. **The topic is about non-code artifacts** (RFC PDFs, conference videos, sociotechnical discussions) — Tavily/web only.
5. **The tier is Lightweight or Standard** (rollout phase 1 restriction) — falls back to Tavily-only Phase 4 and skips Stage A.3 step 2.5.
6. **No PRD was provided** — skip Stage A.3 step 2.5 (precedent discovery requires PRD context).
7. **The agent has hit its octocode call budget.**
8. **Octocode returns HTTP 403 rate-limit twice in the same agent run** — fall back permanently for that agent.

### Rate-limit / failure handling

- **Per-Phase-4-agent budget:** 5 `githubSearchCode` + 3 `githubSearchPullRequests` + unlimited `githubGetFileContent` + unlimited `packageSearch`. Same as T2.
- **Per-Stage-A precedent-discovery budget:** 6 octocode calls total (across all PRD epics). Stage A runs in the orchestrator's main thread — there is no parallelism here, and wall-clock matters.
- **Phase 4 cap (Heavyweight only during rollout phase 1):** 4 github-flavored items max per Phase 4. With Heavyweight's 2–4 web agent budget, this means up to all 4 web agents may be octocode-driven — but the cap also means no run exceeds 4 × 5 = 20 GitHub Search calls in the Phase 4 window.
- **Phase 1 availability check:** Same as T2 — verify `mcp__octocode__githubSearchCode` is available; if not, set `OCTOCODE_AVAILABLE=false` and emit Tavily-only Phase 4 plus skip Stage A.3 step 2.5.

### Hallucination safeguards (TDDs are high-stakes)

TDDs become implementation guidance. Cross-repo evidence is *precedent*, not *truth*. Three safeguards:

1. **Precedent tagging in synthesis** (Diff 7). Every design claim sourced from octocode is marked `[PRECEDENT: owner/repo@branch:path:line]`. The tag survives assembly and lands in the final TDD's "Design Rationale" / "Alternatives Considered" sections — never in normative "Architecture" or "Components" sections without explicit codebase corroboration.

2. **rf-qa-qualitative gate at Phase 6.** The qualitative QA agent already exists (SKILL.md:146). Add a check: every `[PRECEDENT: ...]` tag must trace to a `web-NN-github-*.md` file with a `repo@branch:path:line` citation, AND the QA agent should spot-check 1–2 citations via `mcp__octocode__githubGetFileContent` to verify the citation exists. This catches octocode hallucination (stale or fabricated repo coordinates).

3. **Synthesis Agent Prompt rule addition.** Add to the existing Synthesis Agent Prompt in `refs/agent-prompts.md`:
   > "Cross-repo precedent findings (from web-NN-github-*.md files) describe what other projects have done. They are NOT design specifications for this component. Use precedent to inform 'Design Rationale' and 'Alternatives Considered' sections. Do NOT use precedent as evidence in 'Architecture', 'Components', 'Data Model', or 'API Surface' sections without a corroborating codebase finding."

### Test plan: three example TDDs, one per tier

**Test 1 — Lightweight TDD: "TDD for the wizard step-validator service"**

| Aspect | Behavior |
|---|---|
| PRD provided? | No (Lightweight typically has feature description, not PRD) |
| Tier | Lightweight (0–1 web agents) |
| Stage A.3 step 2.5 fires? | No (Lightweight + no PRD) |
| Phase 4 routing? | No (Lightweight tier-gated out in rollout phase 1) |
| Octocode invocations | **Zero** |
| What this proves | The null-test: Lightweight runs are completely unaffected by the integration. |

**Test 2 — Standard TDD: "TDD for the agent orchestration system"** (run twice: before classifier-widening, and after)

| Aspect | Before classifier widening | After classifier widening |
|---|---|---|
| PRD provided? | Yes (`docs/.../PRD_AGENT_SYSTEM.md`) | Yes (same) |
| Tier | Standard | Standard |
| Stage A.3 step 2.5 fires? | No (Standard tier-gated) | No (still Standard-gated for Stage A precedent — keep this restriction even in rollout phase 2) |
| Phase 4 routing? | No (Standard tier-gated in rollout phase 1) | Yes (rollout phase 2 widens to Standard) |
| Phase 4 web agents | 2 Tavily | 1 Tavily + 1 octocode |
| What this proves | Rollout phase 1 keeps Standard untouched. Rollout phase 2 introduces routing to Standard. |

**Test 3 — Heavyweight TDD: "TDD for the pixel streaming infrastructure"**

| Aspect | Behavior |
|---|---|
| PRD provided? | Yes (`docs/.../PRD_PIXEL_STREAMING.md` with epics like "low-latency video delivery", "session management", "load balancing") |
| Tier | Heavyweight (2–4 web agents) |
| Stage A.3 step 2.5 fires? | Yes — PRD + Heavyweight |
| Stage A precedent calls | 5 octocode calls: 2 `packageSearch` (WebRTC, ICE libraries), 2 `githubSearchPullRequests` ("session affinity load balancer", "pixel streaming WebRTC"), 1 `githubSearchCode` (target a known OSS pixel streamer like Owncast) |
| `EXTERNAL_PRECEDENTS` in research-notes.md | Populated with 4–6 reference repos, star counts, dates |
| Phase 4 routing? | Yes — Heavyweight tier triggered |
| Phase 4 web agents (4 total) | 2 github-flavored (octocode-driven: "WebRTC session management patterns", "production pixel streamer architectures") + 2 open-web (Tavily: blog posts on latency, conference talks on streaming) |
| `[PRECEDENT: ...]` tags in final TDD | ~4–8 tags in "Design Rationale" and "Alternatives Considered" sections of `docs/streaming/TDD_PIXEL_STREAMING.md` |
| What this proves | Full integration path activates; rate-limit cap (4 github-flavored) respected; hallucination safeguard (tagging + QA spot-check) operates end-to-end. |

---

## Section 5: Limits, Dependencies, Effort

### What this cannot do

1. **Cannot prevent precedent-bias in synthesis.** Even with `[PRECEDENT: ...]` tagging, a Phase 5 synthesis agent that reads compelling reference-repo evidence may unconsciously weight it heavily. The QA gate catches the *tag presence*, not the *weight* — a TDD could still over-rely on precedent. Mitigation: the rf-qa-qualitative content review (Phase 6) is the human-style critique gate that must catch this.

2. **Cannot help Lightweight tier in rollout phase 1.** By design — the rate-limit and complexity trade-off doesn't favor Lightweight. Lightweight TDDs remain Tavily-only.

3. **Cannot help PRD-less TDDs in Stage A.** Stage A precedent discovery (Diff 3) requires a PRD. Feature-description-only TDDs skip step 2.5. Their Phase 4 still gets routing (if Heavyweight tier).

4. **Cannot retroactively validate octocode findings.** Same limit as T2 — rf-qa-qualitative spot-checks 1–2 citations but cannot re-execute the search at scale. If octocode returns stale `repo@branch:path:line` coordinates, only spot-checks catch it.

5. **Cannot replace Context7 for API specs.** Octocode reads implementations; Context7 reads docs. Both needed; both have explicit anti-trigger rules separating them.

### Cross-target dependencies

**Depends on T1 (deep-research agent integration)?** **No.** /tdd Phase 4 agents spawn as general-purpose Agents with embedded prompts, not as `deep-research` subagents. The T1 work is orthogonal.

**Depends on T2 (tech-research Phase 4)?** **Soft dependency, not blocking.** The recommended design mirrors T2's W1-B routing pattern. If T2 ships first, /tdd can copy the proven GitHub Research Agent Prompt verbatim and avoid relitigating the heuristic. If /tdd ships first, T2 inherits /tdd's prompt template. Either order works; shipping T2 first is mildly preferred because T2 has simpler downstream consumers (synthesis + assembly) than /tdd (which adds precedent tagging + qualitative QA spot-checking).

**Depends on MCP registration?** **Hard prerequisite.** Octocode MCP server must be registered with `LOG=false` and the 5-tool whitelist (`TOOLS_TO_RUN=githubSearchCode,githubSearchPullRequests,githubGetFileContent,githubViewRepoStructure,packageSearch`) before any integration tests can run.

### Difference from T2 — explicit justification

The /tdd integration **adds two things T2 does not have**:

1. **Stage A precedent discovery (Diff 3 + 4)** — leverages /tdd's unique PRD-as-input mechanic. T2 has no PRD path, so the only injection point is Phase 4. /tdd has two injection points (Stage A research-notes + Phase 4), and using both is justified by the PRD-driven precedent use case.

2. **`[PRECEDENT: ...]` tagging + rf-qa-qualitative spot-check (Diff 5 + 7 + safeguard 2)** — TDDs are normative engineering specs; precedent is informative. The tagging discipline preserves this distinction through synthesis and assembly. T2 produces research reports, which are inherently informative; the tagging would add unjustified overhead there. **This is the structural reason /tdd diverges from T2 rather than purely mirroring it.**

The /tdd integration **mirrors T2 on**:

- Build-time routed buckets (W1-B classification heuristic)
- GitHub Research Agent Prompt structure (same funnel method, same rate-limit budget, same fallback)
- Tool subset (same 5 cross-repo tools; same prohibitions on local* and clone)
- Open-web prompt's fallback access to `packageSearch` + `githubGetFileContent`

### Effort estimate

| Workstream | Files touched | LoC | Reviewer load | Risk |
|---|---|---|---|---|
| 1. SKILL.md tier table footnote (Diff 2) | `src/superclaude/skills/tdd/SKILL.md` | ~5 | Low | Low |
| 2. SKILL.md Stage A.3 step 2.5 (Diff 3) | same | ~15 | Medium | Medium (new orchestrator behavior) |
| 3. SKILL.md A.4 research-notes EXTERNAL_PRECEDENTS (Diff 4) | same | ~6 | Low | Low |
| 4. refs/agent-prompts.md Phase 4 routing (Diff 1) | `refs/agent-prompts.md` | ~12 | Medium | Medium |
| 5. refs/agent-prompts.md new GitHub Research Agent Prompt (Diff 5) | same | ~75 | Medium | Low (additive) |
| 6. refs/agent-prompts.md BUILD_REQUEST classification block (Diff 6) | same | ~40 | Medium | Medium (classifier drift) |
| 7. refs/agent-prompts.md Synthesis Agent Prompt rule addition | same | ~6 | Low | Low |
| 8. refs/synthesis-mapping.md precedent tagging rule (Diff 7) | `refs/synthesis-mapping.md` | ~10 | Low | Low |
| 9. refs/validation-checklists.md rf-qa-qualitative spot-check rule | `refs/validation-checklists.md` | ~8 | Medium | Low |
| 10. Phase 1 octocode availability check | `refs/agent-prompts.md` | ~3 | Trivial | Trivial |
| 11. `make sync-dev` + `make verify-sync` | n/a | n/a | n/a | n/a |
| 12. Test 1 (Lightweight null-test) | manual run | n/a | Low | Low |
| 13. Test 3 (Heavyweight full integration) | manual run | n/a | High | High (first integration test) |

**Total LoC:** ~180 lines across 4 files (SKILL.md + 3 refs files). One PR.

**Total effort:** ~5 hours active editing + 3 hours manual test runs = **~1 working day**. Slightly larger than T2 (~1 day) because /tdd touches 4 files instead of 1 and adds the precedent-tagging machinery.

**Pre-merge gates:**

1. `make verify-sync` passes.
2. Manual Test 3 (Heavyweight TDD) produces at least one `web-NN-github-*.md` file with ≥3 `owner/repo@branch:path:line` citations AND a populated `EXTERNAL_PRECEDENTS` section in research-notes.md.
3. Manual Test 1 (Lightweight TDD) produces zero `web-NN-github-*.md` files and no octocode invocations (rollout phase 1 null-test).
4. The final TDD from Test 3 contains at least one `[PRECEDENT: owner/repo@path]` tag in a "Design Rationale" or "Alternatives Considered" section AND zero precedent tags in normative "Architecture" / "Components" / "Data Model" / "API Surface" sections.
5. The rf-qa-qualitative gate produces a spot-check log showing ≥1 verified precedent citation via `githubGetFileContent`.

**Out-of-scope for this PR (deferred):**

- Candidate B (Phase 3.5 precedent discovery) — defer until A+H ships and we see whether Stage A precedent + Phase 4 routing covers the precedent use case adequately.
- Candidate D (per-TDD-section routing) — defer; revisit if topic-keyword classification (A) misroutes too often in practice.
- Candidate E (Phase 1.5 PRD precedent pre-pass) — superseded by H (Stage A integration is lighter-weight and covers the same use case).
- Rollout phase 2 (widening Phase 4 routing to Standard tier) — separate PR after rollout phase 1 validates the classifier.
- `rf-tdd-octocode-researcher` dedicated agent type (analog of T2's deferred W1-E) — far-future iteration.

---

**Status:** Complete
**Recommendation:** Ship A + H with F-as-rollout-gate (Heavyweight only, rollout phase 1). T2 mirror with two TDD-specific additions: Stage A precedent discovery and `[PRECEDENT: ...]` tagging.
**Sibling alignment:** Synchronize with T2 brainstorm before implementation — share the GitHub Research Agent Prompt template across both skills.
