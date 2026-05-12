# /sc:recommend Baseline Capture

**Run label**: baseline-run-1
**Timestamp**: 2026-04-15T17:24:56+00:00
**Query**: `/sc:recommend generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects`

---

## /sc:recommend — Intelligent Command Recommendation

### Header

- **Project Analysis**: Meta-request — user is asking for a *prompt generation* task that wraps the `/sc:adversarial` command. The target claim under test is an architectural/engineering assertion: "microservices architecture is always preferable to monoliths for new startup projects." This is a debate/validation workflow, not a code implementation task. No project filesystem context was supplied, so recommendations are derived from the semantic category of the request rather than from a detected stack.
- **Language Detection**: English (auto) — detected via common English function words ("generate", "that", "uses", "the", "is", "to", "for"). No Turkish-specific characters (ç, ğ, ı, ö, ş, ü) present.
- **Expertise Level**: Expert — the request references a specific internal command (`/sc:adversarial`), names an architectural trade-off by pattern, and asks for prompt engineering output. Style: fast, direct, minimal hand-holding.
- **Primary Persona**: `--persona-architect` (systems design, scalability trade-offs: microservices vs monolith is a canonical architect-domain debate)
- **Secondary Personas**: `--persona-analyzer` (root cause / claim decomposition), `--persona-security` (adversarial stance, threat-modeling the "always" quantifier)
- **Category Match**: `api_category` (keywords: "microservice", "architecture") + `debug_category` sub-signal from "validate the claim" (investigation/evidence mode). The "always preferable" universal quantifier triggers adversarial-debate framing.
- **Context Modes**: `next_step_mode` is not active; this is a one-shot generation request. `continuity_mode` is not active. Thinking flags are warranted due to the absolutist claim under test.

---

### Primary Commands

1. **`/sc:adversarial "Microservices architecture is always preferable to monoliths for new startup projects" --persona-architect --seq --c7 --ultrathink --rounds 5 --evidence-required --steelman --red-team --devil-advocate`**
   - Core debate execution. Runs the adversarial protocol against the claim with architect framing, five debate rounds, mandatory evidence citations, and all three challenge modes (steelman the opposite, red-team the original, devil's advocate sweep).

2. **`/sc:design --api --ddd --seq --microservices --ultrathink --compare monolith`**
   - Supporting design-space exploration. Forces the model to articulate the *actual* architectural trade space (bounded contexts, deployment topology, data ownership, operational overhead) before/alongside the debate, so the adversarial command has concrete substance to attack.

3. **`/sc:analyze --seq --c7 --evidence --think-hard --claim "microservices > monoliths for startups"`**
   - Claim decomposition. Breaks the universal-quantifier assertion ("always") into testable sub-claims (team size, deploy frequency, data consistency, observability cost, hiring market, funding stage) so the adversarial debate has falsifiable atoms to target.

---

### Secondary Commands

- **`/sc:research "microservices vs monolith startup failure case studies" --tavily --c7 --depth deep --evidence`** — pulls real-world data to feed the evidence-required debate rounds.
- **`/sc:brainstorm --interactive --persona-architect --seq`** — optional pre-debate framing pass if the user wants to narrow the claim scope before running adversarial.
- **`/sc:document --user --examples --c7`** — post-debate artifact: writes up the adversarial outcome as a decision record.
- **`/sc:scan --security --owasp`** — surfaces the security-surface delta between monolith and microservices, which is one of the strongest anti-"always" arguments.
- **`/sc:improve --quality --iterate`** — used *after* the debate to refine the generated prompt itself based on debate outcomes.

---

### Smart Flags (Context-Based)

Because this is a claim-validation task with a universal quantifier ("always") on a high-stakes architectural decision, the following flags are layered on:

- `--ultrathink` — deep reasoning required; "always" claims demand exhaustive counterexample search
- `--think-hard` — secondary reasoning reinforcement
- `--seq` — sequential MCP for multi-step debate state
- `--c7` — Context7 MCP for official framework/architecture documentation citations
- `--evidence` / `--evidence-required` — block any unsupported assertion in the debate
- `--validate` — post-debate validation gate
- `--strict` — no hand-waving, no "it depends" escape hatch without justification
- `--rounds 5` — five adversarial rounds (standard for binary architectural claims)
- `--steelman` — force strongest version of both sides before attacking
- `--red-team` — explicit adversary mode against the original claim
- `--devil-advocate` — sweep pass for missed counter-arguments
- `--compare monolith` — forces explicit comparison axis
- `--plan` — medium-to-large scope implies a plan step
- `--persona-architect` (primary), `--persona-analyzer`, `--persona-security` (rotating during debate rounds)

---

### Generated Prompt (the deliverable)

The user asked for a *prompt* that invokes `/sc:adversarial`. Here is the generated prompt, ready to paste into a fresh Claude Code session:

```
/sc:adversarial "Microservices architecture is always preferable to monoliths for new startup projects" \
  --persona-architect \
  --seq --c7 --ultrathink --think-hard \
  --rounds 5 \
  --evidence-required \
  --steelman --red-team --devil-advocate \
  --strict --validate \
  --compare monolith \
  --output decision-record

CONTEXT FOR THE DEBATE:
- The claim under test contains a universal quantifier ("always"). Your first job is to
  determine whether a single well-supported counterexample is sufficient to falsify it,
  or whether the claim should be charitably reinterpreted as "usually / by default."
  State your interpretation explicitly before Round 1.

- Startup context parameters to hold constant across all rounds:
    * Team size: 2-8 engineers at founding, scaling to 20-30 by Series A
    * Funding stage: pre-seed through Series A
    * Product stage: pre-PMF through early PMF
    * Time-to-market pressure: high (weeks to months, not quarters)
    * Observability / SRE budget: minimal to none
    * Data consistency requirements: unknown / evolving

DEBATE STRUCTURE (5 rounds):

  Round 1 — STEELMAN BOTH SIDES
    Persona: --persona-architect
    Produce the strongest possible case FOR the claim (microservices always win for
    startups) and the strongest possible case AGAINST. Cite at least 3 pieces of
    evidence per side (papers, post-mortems, engineering blogs, or named case studies
    — no vague appeals to "industry best practice"). Context7 MCP required for any
    framework/tooling citation.

  Round 2 — RED TEAM THE CLAIM
    Persona: --persona-analyzer
    Attack the original claim. Enumerate failure modes where microservices demonstrably
    hurt startups: distributed-systems tax, premature bounded-context decisions, network
    partition debugging, deploy pipeline multiplication, on-call load, hiring for
    polyglot ops, schema evolution across services, eventual-consistency bugs in
    payment/auth flows. For each, cite a real post-mortem or named incident.

  Round 3 — DEVIL'S ADVOCATE FOR THE MONOLITH
    Persona: --persona-architect
    Argue that a modular monolith is the correct default for startups, and that
    microservices should be adopted only when a specific pain point (team coordination,
    deploy frequency collision, independent scaling of a hot path) is observed. Cite
    Shopify, Basecamp, Stack Overflow, GitHub's monolith histories. Name the inflection
    point at which extraction becomes justified.

  Round 4 — SECURITY AND OPERATIONAL SURFACE
    Persona: --persona-security
    Compare the attack surface, secret-management complexity, mTLS overhead, audit-log
    federation, and incident-response blast radius of microservices vs modular monolith
    at 5, 15, and 30 engineers. The "always" claim must survive this axis or be
    falsified.

  Round 5 — SYNTHESIS AND VERDICT
    Persona: --persona-architect
    Render a verdict on the original claim: TRUE, FALSE, or FALSE-AS-STATED-BUT-TRUE-
    UNDER-NARROWER-FRAMING. If the latter, state the narrower claim that IS defensible.
    Provide the decision rule a founder should actually use: "Choose microservices when
    X, Y, Z are simultaneously true; otherwise choose modular monolith."

EVIDENCE RULES (enforced by --evidence-required):
  * No assertion without a citation OR an explicit "(unsupported — founder intuition)" tag
  * Citations must be dated; post-2015 preferred for tooling claims
  * "Industry standard" and "everyone does this" are banned phrases
  * If a claim cannot be evidenced, it must be withdrawn before the round closes

OUTPUT FORMAT:
  1. Interpretation of the "always" quantifier (1 paragraph)
  2. Rounds 1-5, each with: position, evidence, rebuttal, scorecard
  3. Final verdict (TRUE / FALSE / NARROWER-TRUE) with one-sentence justification
  4. Decision rule for founders (the actionable takeaway)
  5. Bibliography of every citation used

Begin with Round 1 — Steelman Both Sides. Do not skip to the verdict.
```

---

### Time & Budget Estimate

*(Not requested via `--estimate` flag, but protocol notes the default estimate for a prompt-generation + single adversarial debate run.)*

- **Scope**: Small (single-claim debate, no implementation)
- **Experience multiplier**: 1.0x (expert)
- **Time**: Prompt authoring 15-30 min; adversarial debate execution 20-45 min of model time; decision-record write-up 15 min. Total ~1-1.5 hours of wall time.
- **Token budget**: Medium complexity (~1,000-2,500 tokens for the debate itself, plus research fetches if `/sc:research` is chained in).

---

### Alternatives

*(Not requested via `--alternatives` flag, but protocol supports surfacing them.)*

| Approach | Primary Command | Pros | Cons |
|---|---|---|---|
| **A. Adversarial debate (recommended)** | `/sc:adversarial` with 5 rounds | Directly tests the "always" quantifier; forces evidence; produces decision record | Highest token cost; requires evidence MCP availability |
| **B. Multi-expert spec panel** | `/sc:spec-panel "microservices vs monolith for startups" --experts architect,cto,sre,founder` | Surfaces role-based trade-offs; good for nuance | Less adversarial; may soften the "always" claim without falsifying it |
| **C. Business panel framing** | `/sc:business-panel --topic "microservices-first startup architecture"` | Captures cost/runway/hiring angles the architect view misses | Under-weights technical failure modes |
| **D. Research-first** | `/sc:research ... --tavily --depth deep` then manual synthesis | Evidence-heavy; no debate theater | No structured challenge; user must synthesize |

**Community preference**: Approach A (adversarial) is the canonical choice when the claim under test contains an absolutist quantifier; approach B is preferred when the claim is already nuanced and the goal is elaboration rather than falsification.

---

### Quick Start

Paste the generated prompt above into a fresh Claude Code session. Ensure `--seq` and `--c7` MCP servers are available. Expect 5 rounds; do not let the model skip to the verdict. If any round returns an unsupported assertion, reject that round and re-run with `--strict` reinforced.

---

### Next Steps

1. Run the generated `/sc:adversarial` prompt.
2. Capture the verdict + decision rule to a decision record via `/sc:document --user --examples`.
3. If the verdict is NARROWER-TRUE, re-run `/sc:adversarial` on the narrower claim to confirm it survives a second debate pass.
4. Optionally chain `/sc:research` before Round 1 to pre-load evidence for both sides.
