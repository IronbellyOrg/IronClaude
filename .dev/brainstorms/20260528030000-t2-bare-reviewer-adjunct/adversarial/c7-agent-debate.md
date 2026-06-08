# Adversarial Debate — Should c7 Enrichment Be Extracted Into A Standalone Agent?

```yaml
debate_metadata:
  date: 2026-05-28T04:07Z
  depth: standard (2 rounds + invariant probe)
  focus_areas: [modularity, reusability, separation_of_concerns, agent_vs_skill_semantics, operational_complexity, debugging_surface]
  question: |
    Given v1.1's c7-enrichment logic is currently embedded as Wave B.5 inside sc-bare-review,
    and the user wants to make things modular: should c7 enrichment become its own
    standalone *agent* (per user's literal phrasing), a callable utility *skill*, or
    remain embedded in sc-bare-review?
  variants_count: 3
  delegation: in-context (not Task-spawned; question is self-contained and bounded)
  ground_truth_constraint: |
    User explicitly used the word "agent" — twice. We must give Variant A a genuinely
    fair hearing rather than steering toward the easier "skill" answer.
```

---

## Variant Synopses

### Variant A — Standalone `c7-context-analyst` agent

A dedicated agent definition at `src/superclaude/agents/c7-context-analyst.md` (synced to `.claude/agents/`). Has tools: `Read, Glob, Grep, mcp__context7__*, mcp__auggie__codebase-retrieval, Write`. Spawnable via Task tool by any caller. Operates with its own context window. Receives: target file, challenge-context (what the parent pipeline is trying to accomplish), output dir. Returns: synthesis artifact path + structured findings.

**Cost estimate:** ~600 LOC new agent file + 50 LOC caller-integration template + agent registration. Extracts Wave B.5 from sc-bare-review entirely.

### Variant B — Callable `c7-enrichment` skill

A skill at `src/superclaude/skills/c7-enrichment/SKILL.md`. Invoked via `Skill c7-enrichment` with parameters (target, challenge_label, output_dir, query_cap). Executes the 7-step pipeline deterministically. Returns: synthesis path. Lives in the caller's context window — no separate spawn.

**Cost estimate:** ~400 LOC new skill file + 30 LOC caller-integration. Extracts Wave B.5 from sc-bare-review.

### Variant C — Keep embedded in `sc-bare-review` (status quo)

No extraction. v1.1 spec Wave B.5 stays inside sc-bare-review as-is. Future re-evaluation when a second caller actually needs it.

**Cost estimate:** 0 LOC delta. Current state.

---

## Round 1 — Parallel Advocacy

### Variant A — Standalone Agent Advocate

> *Steelman of B (Skill).* A skill is the right abstraction *when* the work is deterministic execution of a known pipeline. The 7-step recipe in §16.2 looks deterministic on the page. If we treat c7 enrichment as "fetch some docs, paste them into a prompt," a skill is genuinely sufficient. Lower invocation overhead, simpler test surface, fits SuperClaude's existing skill/agent convention where skills = logic and agents = orchestration roles.
>
> *Steelman of C (Status quo).* Premature abstraction has a cost. The Wave B.5 boundary is already a clean refactor target IF needed later. Extracting before a second caller exists invents complexity. YAGNI.

**Position summary.** Variant A is the right answer because the user's actual ask is wrong-shaped for a skill. The user said "evaluate the project or the issue at hand or a particular system and pull the relevant context7 docs, **analyze them through the lens of the challenge at hand** and provide as much relevant context to the other agents working on the problem." That phrase — *analyze them through the lens of the challenge at hand* — is **reasoning work**, not execution work. A skill is bad at adaptive reasoning; an agent excels at it.

**Strengths claimed:**
1. **Lens-aware query derivation.** Different pipelines have different lenses. /sc:troubleshoot's challenge = "why is this broken"; /sc:reflect's challenge = "is the implementation complete + sound"; /sc:tech-research's challenge = "what does it take to build X." A *skill* hardcodes query templates (`"What are the public APIs of X?"`); an *agent* reads the parent's challenge_context, decides what queries actually matter, and synthesizes accordingly. The lens-awareness is the value.
2. **Own context window.** Agents don't pollute the caller's context with raw c7 docs (which can be 30K tokens). They synthesize internally and return a compact summary. The caller stays clean.
3. **Tool-set fit.** Agents naturally compose tools: Read target → Grep for imports → mcp__context7__resolve-library-id → mcp__context7__query-docs → mcp__auggie__codebase-retrieval → Write synthesis. This is exactly what agents are for.
4. **Reuse breadth.** sc-bare-review today; troubleshoot, reflect, auggie-review, code-review, tech-research, brainstorm, tasklist tomorrow. Each gets ONE Task spawn, no caller-side pipeline plumbing.
5. **Failure isolation.** Agent crashes don't kill the parent pipeline. Parent gets a failed Task result and can fall back to no-enrichment.
6. **Aligns with existing pattern.** Look at existing agents: `debate-orchestrator`, `merge-executor`, `evidence-validator`, `confidence-calibrator`, `repo-index`. These are all "do focused work autonomously and return a structured result." c7-context-analyst fits.

**Weaknesses of B (Skill):**
1. Hardcoded query templates can't adapt to "the lens of the challenge at hand" — exactly the user's stated requirement.
2. Skills live in the caller's context. Loading the c7 enrichment skill into every caller's context is expensive at scale.
3. Skills don't ergonomically batch multiple MCP calls + subsequent reasoning. They're closer to function calls than to workers.

**Weaknesses of C (Status quo):**
1. The user just asked to make it modular. C is the "no" answer to a direct ask.
2. Embedded means: when context7's API changes, sc-bare-review needs editing. With extraction, one component changes.

**Concessions:**
- Agent invocation overhead (Task spawn + own context window seeding) is real. ~3-5s per spawn. For small-target reviews, this is a noticeable tax.
- 600 LOC for one component is heavyweight if it ends up with only one caller.

### Variant B — Callable Skill Advocate

> *Steelman of A (Agent).* If the work is genuinely adaptive reasoning, an agent is the right tool. The user's "analyze through the lens of the challenge at hand" phrase points that way. And the existing-agent-pattern argument is real — `debate-orchestrator`, `merge-executor`, etc., do scoped autonomous work. A c7-context-analyst would slot naturally into that lineup.
>
> *Steelman of C (Status quo).* Refactoring later is cheap given the clean Wave B.5 boundary. Premature extraction risks over-engineering.

**Position summary.** Variant B is the right answer because the c7 work is **bounded execution with light synthesis**, not deep reasoning. It deserves modularity (B beats C) but not agent overhead (B beats A). A skill captures the pipeline cleanly, lives in the caller's context (so callers can introspect / debug), and avoids the Task-spawn tax that agents impose on small-target reviews.

**Strengths claimed:**
1. **The pipeline is deterministic in shape.** §16.2 spells out 7 ordered steps. There's branching (auggie_mode = enabled vs direct_inline) but no genuine reasoning — every branch is a heuristic threshold check. Skills handle this fine.
2. **"Lens-aware query derivation" can be parameterized.** Pass `challenge_label` to the skill (e.g., `"troubleshooting"`, `"completeness-audit"`, `"feasibility-study"`); skill picks query templates from a lens→queries map. Adaptive enough; no agent autonomy needed.
3. **Lower overhead.** No Task spawn, no context seeding, no separate window. Wall-clock and token cost both lower than Variant A.
4. **Easier to test.** Functional input/output. Fixture in, expected SYNTHESIS.md out. Agents need integration tests or behavioral mocking; skills need pure-function fixtures.
5. **Easier to debug.** Skill runs in the caller's window — caller sees every tool call. Agent runs in a separate window — caller sees only the final Task result.
6. **Skill-vs-agent convention.** SuperClaude's pattern: skills = reusable logic, agents = roles/orchestrators. c7-enrichment is logic ("fetch docs, query, synthesize"), not a role.
7. **Cost is lower.** ~400 LOC vs ~600 LOC. New skill file vs new agent file + integration template.

**Weaknesses of A (Agent):**
1. Over-rotation on "reasoning." The c7 pipeline doesn't have novel decisions per call — it has parameterized heuristics. Wrapping a parameterized pipeline in an autonomous agent is gilding.
2. Context-window proliferation. Every Task spawn = a fresh window with its own seeding cost. For a 6-query, 45s pipeline, the agent's own context window is mostly unused.
3. Failure semantics are worse, not better. Agents can wander off-task; skills can't (no autonomous tool calls beyond the spec). Whittaker-style attack surface is wider on agents.
4. The "richer reasoning" hypothesis is untested. Show me a concrete case where lens-aware reasoning produces meaningfully different output than a parameterized skill, and I'll concede.

**Weaknesses of C (Status quo):**
1. Same as Variant A's complaint about C: user asked for modularity; C is the "no" answer.
2. Wave B.5 in sc-bare-review couples a 250-LOC pipeline to a skill whose primary responsibility is bare-review orchestration. SRP violation, even if mild.

**Concessions:**
- Hardcoded query templates (lens→queries map) is less flexible than agent reasoning. If lens taxonomy expands, the map needs maintenance. Variant A handles that automatically via reasoning.
- Skills don't get their own context window. For very large c7 doc sets, polluting the caller's window is a real concern (mitigated by SYNTHESIS.md being compact).

### Variant C — Status Quo Advocate

> *Steelman of A (Agent).* If c7 enrichment ends up being used by 5+ callers, extraction is genuinely valuable. Agent semantics is the cleanest extraction shape if the work is adaptive.
>
> *Steelman of B (Skill).* Skill is a cheaper extraction. If we MUST extract, B beats A on cost.

**Position summary.** Variant C is the right answer because both A and B are premature. The v1.1 spec literally just landed. There is exactly ONE caller right now (sc-bare-review). Extracting before a second caller actually requires reuse is the textbook over-engineering anti-pattern. Wave B.5 is already a clean boundary; refactor later is cheap.

**Strengths claimed:**
1. **YAGNI.** Single-caller logic should not be extracted. Wait for the second caller. Premature extraction creates abstractions that calcify wrong.
2. **The spec just landed.** v1.1 was published 7 minutes ago. The cost of stability is real; constant amendment churn is its own anti-pattern.
3. **Clean refactor boundary exists.** §16.2 is explicitly a Wave (B.5) — exactly the kind of clean separation that makes future extraction cheap. The cost of waiting is near-zero.
4. **The IMM-blocker list is unaddressed.** Six items still block Phase 1 implementation. Adding architectural debate before fixing blockers is yak shaving.
5. **Skill/agent count discipline.** SuperClaude already has ~100 skills + ~30 agents. Each addition has discoverability cost. New components must clear a real-utility bar.
6. **Single-pipeline coupling reflects reality.** c7 enrichment for bare reviewers is the empirically-motivated use case. Generalizing to "any pipeline can enrich" assumes use cases that haven't been observed.

**Weaknesses of A (Agent) and B (Skill):**
1. Both A and B claim future-caller benefits that aren't grounded in real demand. "Could be used by troubleshoot, reflect, ..." — name the actual workflow that needs it.
2. Both A and B add cost NOW (600 or 400 LOC, plus integration plumbing) for hypothetical benefits LATER.
3. Both A and B distract from the IMM-blocker list.

**Concessions:**
- The user explicitly asked for modularity, and Variant C is the "no" answer. Ignoring that is dismissive.
- If the user has concrete plans for 3+ callers, the YAGNI argument weakens substantially.
- If extraction happens later, there's a small but non-zero migration cost (sc-bare-review's Wave B.5 + new component + caller updates).

---

## Round 2 — Rebuttals

### Variant A — Rebuttal

**On B's "parameterize the lens" argument.** This is the strongest B point, and it conditionally concedes the agent advantage. Yes, you can pass `challenge_label="troubleshooting"` and have the skill pick query templates. But this only works for *anticipated* challenge taxonomies. The first time a caller passes `challenge_label="post-incident-blameless-RCA"` or `challenge_label="library-deprecation-impact-analysis"`, the skill falls back to a default template or errors. An agent doesn't have this brittleness — it derives queries from the actual challenge text. The maintenance burden on the lens→queries map grows over time and lags real use.

**On B's "agents can wander off-task" attack-surface critique.** This is a real concern, but mitigable: agent definition spec constrains tool set + emphasizes single-purpose protocol. Agents like `merge-executor` and `evidence-validator` don't wander; they execute their spec. The wander risk is a function of how the agent is defined, not an intrinsic agent property.

**On C's "YAGNI" / "single caller" argument.** Conceded *if* sc-bare-review is genuinely the only caller. But the user's framing — "provide as much relevant context to the other agents working on the problem" — explicitly names multiple consumers. The user is signaling: "I want c7 to enrich any agent working on any problem." That's the multi-caller world by direct statement, not hypothetical extrapolation.

**On C's "IMM-blockers first" argument.** This is a valid scheduling objection but doesn't change the architectural answer. Resolving IMM-1..IMM-6 is Phase 1 prep; deciding c7 architecture is Phase 1.5 prep. They can be sequenced; they're not in conflict.

**Standing position.** Variant A wins on:
- Lens-aware reasoning (the user's explicit requirement)
- Multi-caller reuse (the user's explicit framing)
- Context-window hygiene (compact synthesis returned, not raw docs)
- Convention alignment with existing agents (debate-orchestrator, merge-executor, etc.)

### Variant B — Rebuttal

**On A's "lens-aware reasoning is genuine" claim.** Show me the worked example. The user's two challenge examples — "troubleshooting" and "completeness audit" — have very similar c7-query needs: pull docs on relevant libs, look at API surface, look at common pitfalls. The query *templates* differ in emphasis (troubleshooting cares about error modes; completeness audit cares about API coverage), but the *queries themselves* are bounded by what context7 can usefully answer. Three query templates handle 90% of cases. The remaining 10% don't need an agent — they need a `--c7-custom-queries` flag on the skill.

**On A's "context-window hygiene" argument.** Half-conceded. Compact synthesis vs raw docs is a real difference. But the synthesis can be produced just as cleanly by a skill (it's a deterministic prioritization-and-truncation step). The agent's "own context window" advantage is real but expensive: every Task spawn costs ~3-5s + ~3K tokens of seeding. For a 30s pipeline, that's a 10-15% overhead. For a 5s "skip c7, no candidates detected" pipeline, that's >100% overhead.

**On A's "multi-caller reuse" reading of the user prompt.** The user said "provide as much relevant context to the **other agents working on the problem**." This phrase refers to OTHER agents being CONSUMERS of c7's output — not to c7 itself being an agent. The user's sentence parses as: c7 [thing] does work and feeds context to other agents (which are already agents). A skill is a perfectly fine "thing" that does work and feeds output to agents.

**On C's status-quo defense.** C is wrong because the user explicitly asked for modularity. But "modularity" doesn't necessarily mean "agent." A skill IS modular — it's a discrete component invokable by multiple callers. The C critique applies to C, not to B vs A.

**Standing position.** Variant B wins on:
- Cost (~400 LOC vs ~600; ~5s vs ~10s wall-clock; fewer tokens)
- Testability (functional fixtures)
- Debuggability (caller-window visibility)
- Convention fit (skills are SuperClaude's logic abstraction)
- Adequate adaptiveness via parameterized lens→queries map

### Variant C — Rebuttal

**On A's "user explicitly named multi-caller world."** Re-read the user prompt: "provide as much relevant context to **the other agents working on the problem**." The "other agents" are the bare reviewers AND/OR other downstream consumers in the SAME pipeline invocation. This is single-call multi-consumer, not multi-call. The single-pipeline-coupling argument stands.

**On A's "convention alignment with existing agents."** Look at the existing agents in detail. `debate-orchestrator` exists because adversarial protocol has genuine orchestration logic (coordinating advocates, managing rounds, computing convergence). `merge-executor` exists because refactor-plan execution is genuinely autonomous (apply changes, validate integrity, produce log). `evidence-validator` exists because validation is genuinely independent (re-Read citations, drop unfounded). What's the comparable autonomy claim for c7-context-analyst? Detect imports, fetch docs, query, synthesize. That's a pipeline, not a role.

**On B's "skill captures it cleanly."** Yes, but the user asked for modularity, not just code reuse. The question is whether to extract — and extraction has a cost regardless of A vs B shape. Defer until a second caller materializes.

**On both A and B's "we should make it modular because the user asked."** The user's modularity ask is correct in principle. But "make it modular" doesn't mean "extract immediately." It can mean "design the boundary so extraction is cheap when needed." That's what Wave B.5 already is. Extract-when-needed beats extract-now.

**Standing position.** Variant C wins on:
- Schedule (IMM-blockers first)
- Empirical demand (one caller, not multiple)
- Cost (zero LOC delta)
- Real engineering discipline (premature abstraction is a known anti-pattern)

---

## Round 2.5 — Invariant Probe (Sufficiency Challenge)

| INV-ID | Category | Probed Assumption | Status |
|--------|----------|-------------------|--------|
| INV-01 | sufficiency_challenge | A's claim: "lens-aware reasoning is the load-bearing value" — name one concrete case where a parameterized skill provably degrades the output | ADDRESSED by A: "first time a caller passes `challenge_label='library-deprecation-impact-analysis'`, the skill falls back to a default template or errors" — concrete enough; counter: skill can add `--c7-custom-queries` |
| INV-02 | guard_conditions | B's claim: "3 query templates handle 90% of cases" — what's the falsifier? | UNADDRESSED — B asserts but doesn't enumerate the 3 templates or measure the 90%. Pure assertion. |
| INV-03 | count_divergence | C's claim: "single caller" — does the user's prompt commit to multi-caller or not? | CONTRADICTED across A/C. Sentence is parseable both ways. User must disambiguate. |
| INV-04 | sufficiency_challenge | All variants' assumption: c7 enrichment is valuable enough to justify any extraction effort | UNADDRESSED — no variant probes whether v1.1's embedded c7 actually moves the needle on bare-review quality. Could be: extract whatever shape; could be: it's not worth either A or B. |
| INV-05 | interaction_effects | A's claim: "context-window hygiene" — does this matter if c7 enrichment is the LAST thing before bare-review dispatch? | ADDRESSED-conditionally — matters only when caller does additional reasoning after the synthesis. For the sc-bare-review flow specifically, the synthesis is immediately consumed by the next wave; window hygiene gain is small. |
| INV-06 | state_variables | C's claim: "Wave B.5 is already a clean boundary; refactor later is cheap" — what's the actual migration cost when a second caller materializes? | ADDRESSED: ~150 LOC delta (extract wave + update sc-bare-review caller + create new component file + write integration template). Non-zero but not large. Variant C's "cheap later" claim holds. |
| INV-07 | guard_conditions | A's claim: "agents like merge-executor don't wander" — name one operational metric proving this | UNADDRESSED. A asserts but doesn't cite incident data. Could be true or false; debate-orchestrator agents in particular have wandered in past pipelines per project memory. |

**Probe summary.** Three UNADDRESSED items (INV-02, INV-04, INV-07). One CONTRADICTED (INV-03). None HIGH-severity blocking, but INV-04 in particular suggests the whole debate may be premature: if v1.1's embedded c7 doesn't demonstrably improve bare-review quality, neither extraction is justified.

---

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence |
|------------|--------|------------|----------|
| Lens-awareness | A | 65% | A's argument is genuine; B's lens→queries map handles common cases but degrades on novel taxonomies. NOT high confidence because B's `--c7-custom-queries` flag mitigates substantially. |
| Cost (LOC + tokens + wall-clock) | B | 85% | Clear quantitative win: ~400 vs ~600 LOC, no Task-spawn overhead, no extra context-window seeding |
| Testability | B | 80% | Functional input/output for skills; agents need integration mocks |
| Debuggability | B | 75% | Skill tool calls visible to caller; agent runs opaque |
| Multi-caller fit | A | 55% | A wins IF multi-caller is true. Ambiguous in user prompt (INV-03 contradicted). |
| Convention alignment | A | 55% | Existing agents (debate-orchestrator, merge-executor, evidence-validator) ARE roles, not pipelines. c7-context-analyst is more pipeline-shaped. Mixed signal. |
| Schedule fit | C | 75% | IMM-blockers truly should come first. A and B both add scope ahead of unblocking Phase 1. |
| Future-proofing (if multi-caller materializes) | A | 60% | A is the right shape if c7 needs to compose with diverse pipelines. Migration B→A is harder than A→B. |
| YAGNI compliance | C | 70% | Single confirmed caller today. Both A and B speculate forward. |
| Failure isolation | A | 70% | Agent crash bounded; skill failure propagates to caller window |

**Aggregate (50% quant + 50% qual):**

| Variant | Quant proxy (cost+test+debug) | Qual proxy (lens+multi+convention+future) | Combined | Notes |
|---------|-------------------------------|-------------------------------------------|----------|-------|
| A | 0.45 (loses cost; ties testability/debug) | 0.65 (wins lens, multi, future; ties convention) | **0.55** | High-ceiling, high-cost |
| B | 0.85 (wins cost+test+debug) | 0.55 (loses lens-ceiling; wins parameterization) | **0.70** | Practical, adequate |
| C | 0.75 (zero cost) | 0.30 (loses on modularity ask) | **0.525** | Schedule-correct, modularity-wrong |

---

## Base Selection

**Variant B — Callable `c7-enrichment` skill — wins by 15-point margin over A and 17.5 over C.**

**Rationale.** B captures the modularity ask (beats C) without paying the agent-overhead tax (beats A). The strongest A-favorable arguments (lens-aware reasoning, multi-caller reuse) are conditional — they win IF the user's challenge taxonomy outgrows 3-5 templates AND multi-caller demand materializes. Currently neither is empirically demonstrated. B with a `--c7-custom-queries` escape hatch (and a documented lens→queries map) captures 90% of A's value at 60% of A's cost.

**However, this is a 0.70 vs 0.55 win — not a slam dunk.** Two scenarios flip the answer:

1. **If the user's "agents working on the problem" phrase committed to multi-caller world** (which is ambiguous), A's multi-caller-fit score climbs and the margin narrows or inverts.
2. **If c7 enrichment ends up needing genuinely adaptive synthesis** (which is testable: ship B first, watch where the lens→queries map breaks), A becomes the right Phase 2 evolution.

---

## Refactoring Plan (toward Variant B)

**Phase 1.6 (after IMM-blockers and Phase 1 implementation):**
1. Extract Wave B.5 from `sc-bare-review` into new skill `src/superclaude/skills/c7-enrichment/SKILL.md`.
2. Skill API:
   ```
   Skill c7-enrichment
     --target <path>           # file to enrich context for
     --challenge-label <str>   # parameterized lens: "troubleshooting" | "completeness-audit" |
                               #   "feasibility-study" | "code-review" | "spec-review" | "custom"
     --custom-queries <list>   # only when --challenge-label=custom
     --output <dir>            # writes <output>/c7-context/
     --query-cap <N>           # default 6
     --timeout-sec <N>         # default 45
   ```
3. Update `sc-bare-review`'s Wave B.5: replace embedded logic with `Skill c7-enrichment` invocation. Pass `--challenge-label="code-review"` as the sc-bare-review-specific lens.
4. Document the lens→queries map in `refs/lens-queries.md` so additions don't require skill-source edits.
5. Add ACs for skill independence: skill runs cleanly when target is non-code (docs, specs); skill returns clean SYNTHESIS.md regardless of caller.

**Phase 1.7 (conditional, if multi-caller demand materializes):**
6. Plumb `Skill c7-enrichment` invocation into `/sc:troubleshoot`, `/sc:reflect`, `/sc:auggie-review`, `/sc:code-review`, `/sc:tech-research`.
7. Add lens labels to the documented map as needed.

**Phase 2 (conditional, if Variant B breaks):**
8. If the lens→queries map grows beyond ~8 distinct lenses OR if `--custom-queries` usage exceeds 30% of calls, **re-open this debate and promote to Variant A (agent extraction).** The skill is intentionally designed so this promotion is mechanical: agent wraps the skill's API as the autonomous-equivalent.

---

## Changes Not Being Made

1. **Not adopting Variant A (agent) now.** Lens-aware reasoning is a genuine A advantage but not load-bearing for current callers. Premature.
2. **Not adopting Variant C (status quo) now.** The user's modularity ask deserves a yes-shaped answer; declining is dismissive. The IMM-blocker scheduling concern is real but doesn't preclude small Phase 1.6 work.
3. **Not running this through /sc:adversarial Mode B with model variance.** This debate is self-contained and bounded. Spinning up 3 Task-spawned agents with different models would burn tokens for marginal added perspective. Documented in `delegation: in-context` in metadata.

---

## Open Question for User

The decisive ambiguity is **INV-03**: when you said "the other agents working on the problem," did you mean:

- **Interpretation 1 (B-favorable):** c7 is a thing that does work and feeds context to *bare reviewers* (which are already loosely-called agents). Single-pipeline, multi-consumer. Variant B is correct.
- **Interpretation 2 (A-favorable):** c7 is itself an agent, peer to other agents (troubleshoot, reflect, etc.), each of which is independently working on the problem and consuming c7's context. Multi-pipeline, agent-mesh. Variant A is correct.

If your answer is Interpretation 2, the debate inverts: A wins by ~10 points (multi-caller-fit score climbs from 0.55 to 0.85, lens-aware-reasoning premium becomes load-bearing). **One sentence from you flips the outcome.**

If you don't have a strong preference, **default to Variant B** (extract as skill, design for future promotion to agent if demand materializes). It's the smallest-cost win on the user's stated modularity goal, and it preserves the upgrade path.

---

## Spec Impact

If the user picks Variant B (default recommendation):
- v1.2 amendment to `merged-requirements.md`: replace §16.2 Wave B.5 detail with `Skill c7-enrichment` invocation
- New file: `src/superclaude/skills/c7-enrichment/SKILL.md` (~400 LOC)
- LOC delta: roughly net-zero (Wave B.5 contents move from spec inline to skill file; spec gets ~30 LOC of invocation glue)

If the user picks Variant A:
- v1.2 amendment to `merged-requirements.md`: replace §16.2 Wave B.5 with `Task c7-context-analyst` agent spawn
- New file: `src/superclaude/agents/c7-context-analyst.md` (~600 LOC)
- LOC delta: +200 above v1.1 estimate

If the user picks Variant C:
- No spec change.

---

*Debate authored in-context (no Task agents spawned) per the bounded nature of the question. Three variants, two rounds, sufficiency-challenge invariant probe, scoring matrix, base selection, refactor plan. Recommendation: Variant B (skill), with explicit upgrade path to Variant A (agent) if/when empirical demand justifies.*
