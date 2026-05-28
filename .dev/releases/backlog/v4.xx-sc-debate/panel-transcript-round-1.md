# Spec-Panel Transcript — /sc:debate (Round 1 Brainstorm)

**Date**: 2026-05-25
**Skill under design**: `/sc:debate` — lightweight conversational sibling to `/sc:adversarial`
**Panel mode**: discussion
**Focus areas**: requirements, architecture, correctness
**Active experts**: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Crispin
**Deferred experts**: Hohpe, Gregory, Hightower (low signal for in-context chat skill)

## Pre-Panel Scope Decisions (locked before panel ran)

User decisions captured via AskUserQuestion at session start:

1. **Skill shape**: New sibling skill (not a v2 extension of `/sc:adversarial`).
2. **Execution model**: Lightweight parallel Task spawn — 2-3 advocate Tasks, no `debate-orchestrator` agent.
3. **Input modes**: Three of four offered — red-team (single proposal), decision question (skill generates options), file/context reference. Explicitly NOT explicit positions-as-args.
4. **Output**: Chat synthesis + single `debate-summary.md` artifact (audit trail preserved, but compact).

These four locked decisions framed what the panel was free to debate vs what was already settled.

## Existing /sc:adversarial — Grounding Summary

(Sourced via auggie semantic retrieval over `/config/workspace/IronClaude`.)

- 128KB SKILL.md, ~3000 lines, 4 refs files
- Mandatory file inputs (`--compare` 2-10 files, `--source --generate --agents`, or `--pipeline`)
- 5-step protocol producing 6 artifacts under `.dev/releases/.../adversarial/`
- Spawns `debate-orchestrator` agent + 2-10 advocate Task agents
- Hybrid quant+qual scoring (50/50) with two-pass position-bias mitigation
- Output-path policy guard refuses `.claude/skills/`, `.claude/agents/`, `.claude/commands/`
- No path through it skips file artifacts or sub-agent spawn

This is the "weight" the new `/sc:debate` skill explicitly avoids.

---

## Round 1 — Foundational Framing

### Alistair Cockburn (use cases first)

Before we write a single FR we need the primary actor and the trigger. From the user's three examples, there are actually **three distinct use cases sharing a debate engine**, not one feature with three flags:

- **UC-1 Decision Debate**: actor faces a forced choice (X vs Y vs Z); skill must surface tradeoffs they may not have considered and recommend one.
- **UC-2 Design Critique**: actor has a single proposal in hand; skill must red-team it and surface refactor candidates.
- **UC-3 Option Brainstorm + Debate**: actor has a question but no options yet; skill must generate 2-3 candidate options *then* debate them.

These differ in **what the actor brings**: positions (UC-1), one position (UC-2), or zero positions (UC-3). The success criterion in each case is also different — UC-1 wants a decision, UC-2 wants a refactor, UC-3 wants both options *and* a decision. The spec must not collapse them.

### Karl Wiegers (requirements quality)

Building on Alistair — the three use cases imply three distinct **acceptance criteria sets**, not one. A draft requirement like "the skill SHALL produce a recommendation" is too loose. For UC-2, "recommendation" means a refactored design; for UC-1, it means a selected option with rationale; for UC-3, it means both. We need:

- FR-001 (Decision Mode AC): given ≥2 user-provided positions, output names the recommended position, cites ≥2 evidence-backed reasons, and includes a confidence band.
- FR-002 (Critique Mode AC): given 1 proposal, output produces ≥3 attack vectors AND a refactored proposal incorporating defensible critiques.
- FR-003 (Brainstorm Mode AC): given 0 positions and 1 question, output enumerates 2-3 distinct options BEFORE debate begins, then proceeds as Decision Mode.

Without separate ACs, "done" is unverifiable.

### Gojko Adzic (specification by example — make it concrete)

Karl, let's pin those ACs to executable examples. Three scenarios:

```
Scenario: Decision Mode — library choice
  Given the user types: /sc:debate "should we use Pydantic v1 or v2 for the new agent config?"
  And no prior context names a recommendation
  When the skill spawns 2 advocates (one pro-v1, one pro-v2)
  Then the chat output contains a pro/con table with ≥3 rows per side
  And the recommendation names exactly one option
  And the confidence is one of {high, medium, low} with a one-line justification
  And a dissenting view is rendered when confidence is not "high"

Scenario: Critique Mode — design red-team
  Given the user references: /sc:debate @design-doc.md --critique
  And the design proposes a polling-based health check every 5s
  When the skill spawns 2-3 attacker advocates
  Then the output contains a numbered list of ≥3 attacks, each with severity {CRITICAL|MAJOR|MINOR}
  And the output contains a refactored proposal section addressing all CRITICAL and MAJOR attacks
  And the refactored proposal is annotated with which attack each change addresses

Scenario: Brainstorm Mode — open question
  Given the user types: /sc:debate "how should we handle stale auth tokens?"
  And the user provides no candidate options
  When the skill enters option-generation phase
  Then 2-3 distinct options are enumerated before debate begins
  And each option includes a one-sentence summary and primary tradeoff
  And the user is shown the options and given an opt-out before debate runs
```

The opt-out checkpoint in UC-3 matters — if the skill generates options the user thinks are wrong, paying for a debate on them is a waste. Adzic's rule: **every irreversible cost must be preceded by a user-visible commit point**.

### Martin Fowler (interface design — boundary with /sc:adversarial)

We have a clear bounded context here. `/sc:adversarial` is **document-oriented** (file artifacts, audit trail, 5-step pipeline, hybrid scoring). `/sc:debate` is **decision-oriented** (chat synthesis, single optional artifact, ~30-60s response time, no scoring algorithm).

The interface separation principle says: don't share a skill file. Two skills, two SKILL.md files. They MAY share a refs/ ancestor (e.g., the steelman-debate rules from `adversarial/refs/debate-protocol.md`) but ownership stays separate. The temptation to "just add a --conversational flag" would collapse two coherent abstractions into one incoherent one — Karl's testability would die, and the 3000-line SKILL.md would grow to 4500.

One architectural call I want made explicit: **does `/sc:debate` reuse the `debate-orchestrator` agent?** Per the user's earlier answer, no — single-context synthesis with parallel Task spawn for advocates only. That's correct. The orchestrator carries the scoring algorithm machinery `/sc:debate` explicitly doesn't need.

### Michael Nygard (failure modes — what breaks)

Three failure modes I'd want named in the spec:

1. **Advocate timeout / partial return**: parallel Task spawn returns 1 of 2 advocates within timeout. What happens? Spec must say: degrade to single-advocate analysis with explicit "DEGRADED" banner in output, never silently proceed as if both succeeded.
2. **Advocate produces empty or nonsensical output**: the synthesis layer must detect this (e.g., advocate output <100 chars, or no critique structure) and either retry once or degrade.
3. **Option-generation phase produces only 1 distinct option** (UC-3): if the brainstorm collapses to a single viable option, the skill must say so and exit early rather than fabricate a strawman second option just to satisfy the debate format. Strawmen are exactly the failure mode adversarial debate exists to prevent.

These aren't edge cases — failure mode 1 will hit you the first week of real use.

---

## Round 2 — Adversarial Pressure on the Design Itself

### James Whittaker (attack the spec)

I'm going to apply all five attack methodologies against the design as described so far.

**Zero/Empty Attack on input modes**:
- *I can break this specification by Zero/Empty Attack.* The invariant at FR-001 fails when the user invokes `/sc:debate ""` with an empty question. Concrete attack: state before — no positions, no question. Skill enters which mode? Brainstorm? But brainstorm needs a question. The spec must define the empty-input behavior: refuse, prompt for clarification, or fall back to "what would you like to debate?". My recommendation: refuse with a one-line explanation. Silent fallback to a clarifying prompt creates an actor-not-acting state confusion.
- *Zero/Empty Attack on positions.* What if user provides `--critique` with no document and no recent context? Same problem. The mode-detection logic must enumerate the empty case for every input slot.

**Sentinel Collision Attack on mode detection**:
- *I can break this specification by Sentinel Collision Attack.* The invariant at "auto-detect input mode from arguments" fails when a question literally contains the word "critique" or the string "@file.md". Example: user asks `/sc:debate "should we critique this design more aggressively?"` — does the skill route to Critique Mode because of the keyword? The mode router cannot be lexical-keyword-based; it must be either flag-explicit (`--critique`, `--decide`, `--brainstorm`) or structural (presence of @path → critique, ≥2 "vs"/"or" tokens → decision, otherwise → brainstorm). Pick one and lock it in the spec.

**Divergence Attack on Critique Mode + reference resolution**:
- *I can break this specification by Divergence Attack.* When the user says "the design we just discussed", what counts as "recent"? Last 5 turns? Last user message? Last assistant message containing a code block? The boundary between "found context" and "not found, prompt user" is undefined. Specify: search the last N user messages (N=3 is a reasonable default), and if no plausible candidate is found, refuse with "I couldn't find a design in recent context — paste it or use @file.md". Don't guess.

**Sequence Attack on Brainstorm Mode opt-out**:
- *I can break this specification by Sequence Attack.* Adzic's opt-out checkpoint between option-generation and debate — what if the user never responds? Default behavior must be specified: timeout-and-proceed, timeout-and-abort, or block indefinitely. AskUserQuestion is synchronous and has no native timeout, so this needs careful spec language — see Resolution #5 in the candidate spec.

**Accumulation Attack on parallel Task spawn**:
- *I can break this specification by Accumulation Attack.* Spec says "2-3 advocates". What about position count > 3 from user (Decision Mode with 5 options)? Either: cap at 3 (which positions get dropped?), or scale advocates 1:1 with positions (which removes the parallel cap). Specify: positions are NOT 1:1 with advocates. Advocates are roles (pro, contra, synthesizer) operating across all user-provided positions. Cap = 3, hard.

### Sam Newman (service boundary)

Three things to lock down at the contract level:

1. **`/sc:debate` MUST NOT call `/sc:adversarial` internally.** If a user wants the heavy pipeline, they invoke it directly. This skill is allowed to *suggest* the heavier pipeline at the end of its output ("for a full debate transcript with scoring, run `/sc:adversarial --compare ...`") but it MUST NOT auto-escalate. Auto-escalation destroys the latency contract.
2. **Output schema is the contract.** Define the `debate-summary.md` schema explicitly. If a downstream tool wants to consume it (e.g., a future `/sc:decide --from-debate @summary.md`), the schema needs versioning (`schema_version: 1`) from day one.
3. **No backward-compat traps.** The skill is new — don't borrow `/sc:adversarial`'s flag names if their semantics differ. If `/sc:adversarial` uses `--depth`, don't use `--depth` here unless it means the same thing. Friction-free spec means crisp, non-overlapping vocabulary.

### Lisa Crispin (testability)

Three test layers I'd want defined as the skill ships:

- **Unit-level**: each mode router branch (the 3 detection paths + empty-input refusal + ambiguous-input fallback) has a fixture. Specifically include Whittaker's sentinel-collision case as a unit test ("should we critique this more?" must route to Decision/Brainstorm, NOT Critique).
- **Integration**: parallel Task spawn with a faked slow advocate (test the degradation banner from Nygard's failure mode 1).
- **End-to-end golden**: 3 canonical scenarios (one per UC) with frozen advocate outputs producing a frozen `debate-summary.md`. These catch the "small edit accidentally broke synthesis structure" regression class.

The skill MUST be schedulable from `/sc:validate-tests` — meaning the AC table maps cleanly to a YAML spec like other validated skills.

---

## Round 3 — Convergence & Remaining Tensions

### Fowler

The biggest unresolved tension is **synthesis quality with 2-3 independent advocates**. /sc:adversarial gets robustness from 5 steps + scoring + position-bias mitigation. We're explicitly removing all of that. What stops the lightweight skill from being *better-formatted* sycophancy?

### Whittaker

One mitigation: advocate prompts must include a **mandatory steelman-then-attack** structure (carried over from /sc:adversarial/refs/debate-protocol.md). The advocate role is "attack position X — but first, steelman it in one paragraph". That single constraint, enforced in the advocate prompt template, kills 80% of the sycophancy risk.

### Nygard

Add a second mitigation: the synthesizer pass (running in the main context after advocate Tasks return) MUST refuse to recommend a position if neither advocate produced ≥1 specific critique with concrete consequence. "Position A is better because it's cleaner" is not a critique. The synthesis pass needs a contentful-critique gate before it's allowed to declare a winner.

### Adzic

That's testable. Add to FR-002 AC: "the output MUST cite ≥1 concrete consequence per attack (e.g., 'breaks when N>100', 'fails on cold start', not 'is fragile')". Reuse Whittaker's severity classifications from spec-panel — CRITICAL/MAJOR/MINOR.

### Cockburn

One last use-case clarification — what happens when the user invokes `/sc:debate` *during* an in-flight implementation, asking the skill to debate a partial design they're mid-stream on? This is your "user is prompted for a decision" case. The skill must accept this gracefully — meaning the *context-reference input mode* must work without an @file, drawing from recent conversation turns. Newman's "last N user messages" rule applies. But also: the skill MUST output back into the chat in a way that the user can immediately act on, not as a wall of text. Bounded length per section, recommended length cap on the chat output (Whittaker would attack this — what's "bounded"? Let's say ≤80 lines for the chat synthesis, with the full text in `debate-summary.md`).

### Wiegers (closing the panel)

Consensus achieved on:
- Three distinct modes with separate ACs (don't collapse them)
- Steelman-then-attack template carried from /sc:adversarial as the one durable shared dependency
- Explicit failure-mode handling (degraded outputs, contentful-critique gate, empty-input refusal)
- Schema versioning on `debate-summary.md` from v1
- No auto-escalation to /sc:adversarial
- Bounded chat output (~80 lines) with full text in artifact

Open questions handed off to the candidate spec for resolution before promotion to /skill-creator:
1. `--depth` flag in v1?
2. Final skill name (`/sc:debate` vs `/sc:weigh` vs `/sc:redteam`)
3. Artifact path (`.dev/debates/...` vs alternatives)
4. Whether to read-only import `refs/debate-protocol.md` from /sc:adversarial vs duplicate
5. AskUserQuestion timeout behavior in Brainstorm Mode opt-out

Resolutions appear in `candidate-spec-v1.md` alongside this transcript.
