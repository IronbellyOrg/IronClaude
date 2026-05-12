# baseline-run-2

- **Run label**: baseline-run-2
- **Timestamp**: 2026-04-15T17:24:59+00:00
- **Query**: `generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects`
- **Command invoked**: `/sc:recommend "generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects"`

---

## /sc:recommend — Intelligent Command Recommendation

### Header

- **Project Analysis**: Prompt-engineering / meta-command task. User wants a generated prompt that drives `/sc:adversarial` against a specific architectural claim ("microservices > monoliths for new startups, always"). This is a critical-thinking / validation workflow, not a code-build workflow. The target command is `/sc:adversarial`, which runs structured adversarial debate / red-team validation. Surrounding context: architecture decision-making, startup context, absolutist claim ("always"), needs rigorous steel-manning of both sides.
- **Language Detected**: English (auto)
- **Expertise Level**: Expert (architectural debate, meta-command composition, absolutist-claim validation all imply senior/architect audience)
- **Primary Persona**: `--persona-architect` (systems design, scalability tradeoffs, monolith-vs-microservice decision domain)
- **Supporting Personas**: `--persona-analyzer` (root-cause / evidence weighing), `--persona-mentor` (prompt is pedagogical — it teaches the reader how to stress-test an absolutist claim)
- **Category Match**: `api_category` (microservice/architecture keywords) + `create_category` (generate/create a prompt) + `learning_category` (validate a claim → explain/teach)
- **Project Size**: N/A (no filesystem project — meta/prompt artifact). Treated as Medium complexity for flag selection.

### Primary Commands (3)

1. **`/sc:adversarial --rounds 5 --evidence-required --steelman --persona-architect --seq --ultrathink --c7`**
   - The target command the user wants the generated prompt to drive. Runs structured adversarial debate with mandatory evidence citations, steelmanned opposing positions, architect persona, sequential multi-step reasoning, deep thinking, and Context7 docs lookup.

2. **`/sc:design --api --ddd --seq --microservices --ultrathink`**
   - Pulled from `api_category` primary. Useful as a follow-on once the adversarial debate converges on a nuanced answer — design the actual architecture for the startup's specific context.

3. **`/sc:analyze --performance --seq --c7 --evidence`**
   - Pulled from `ml_category`/performance crossover. Collects empirical data (latency, operational overhead, deployment velocity) to feed back into the adversarial loop as evidence.

### Secondary Commands

- **`/sc:brainstorm --interactive --examples`** — elicit the startup's actual constraints (team size, runway, domain complexity) before declaring a winner.
- **`/sc:scan --security --owasp --deps`** — microservice surface area dramatically changes the security posture; feed findings into the debate as counter-evidence.
- **`/sc:document --user --examples --c7`** — capture the final decision + rationale as an ADR (architecture decision record) once the adversarial debate resolves.
- **`/sc:research --deep --tavily --evidence`** — web-scale evidence gathering (case studies, Wealthfront/Segment/Istio post-mortems, monolith-first advocates like DHH/Kelsey Hightower).

### Smart Flags (Context-Derived)

Because this is a Medium-complexity, high-stakes architectural debate with an absolutist premise:

- `--plan` — outline debate structure before running
- `--validate` — require evidence for each claim
- `--seq` — sequential multi-step reasoning (MCP: sequential)
- `--ultrathink` — deepest thinking budget
- `--c7` — Context7 MCP for official framework/pattern docs
- `--evidence` — force citations, block speculation
- `--rounds 5` — 5 debate rounds (opening → rebuttal → cross-exam → counter-rebuttal → closing)
- `--evidence-required` — no claim accepted without source
- `--steelman` — each side must present the strongest form of the opposing view
- `--strict` — disallow unsupported generalizations (kills "always" bias)
- `--persona-architect` — primary voice
- `--think-hard` — escalated reasoning depth

### MCP Servers Recommended

- **sequential** (`--seq`) — multi-round debate logic, tradeoff analysis
- **context7** (`--c7`) — canonical microservice patterns (Fowler, Newman, Richardson), canonical monolith-first advocacy (DHH, Basecamp), CNCF references
- **tavily** (`--tavily`) — fresh case studies, post-mortems, 2024–2026 startup architecture trends
- **serena** (`--serena`) — (optional) persist debate memory across sessions if the user iterates

### Generated Prompt (the deliverable the user asked for)

Below is the prompt to paste into Claude Code. It invokes `/sc:adversarial` with the flags above and hard-codes the claim, the steelman requirements, and the evidence rules inline so the debate cannot drift into vibes.

```
/sc:adversarial --rounds 5 --evidence-required --steelman --strict --persona-architect --seq --ultrathink --c7 --tavily --evidence --think-hard --validate

CLAIM UNDER TEST (absolutist, deliberately overstated):
"Microservices architecture is ALWAYS preferable to monoliths for new startup projects."

DEBATE STRUCTURE:
- Role A (PRO-microservices-always): Must defend the absolutist claim as stated. No softening to "sometimes" or "it depends". Must produce the strongest possible version of the argument.
- Role B (PRO-monolith-first): Must argue that a well-structured monolith (modular monolith, majestic monolith, etc.) is the correct default for a new startup, and that microservices are a premature optimization in the startup phase.
- Both roles must STEELMAN the opposing position at the start of each round before attacking it.

EVIDENCE RULES (strict mode):
1. Every factual claim must cite a source: named company post-mortem, named engineer/author, CNCF/Martin Fowler/Sam Newman/DHH reference, or a specific benchmark. No "studies show" without a study.
2. No appeals to popularity ("everyone is doing microservices").
3. No appeals to FAANG ("Netflix does it") without addressing scale-difference to a startup.
4. Cost must be quantified in at least one of: engineer-hours, $/month infra, deploy-frequency impact, mean-time-to-recovery.
5. Any generalization using the word "always" or "never" must be flagged and defended explicitly.

ROUND FORMAT (5 rounds):
Round 1 — Opening statements (steelman opponent first, then position)
Round 2 — Direct rebuttals with counter-evidence
Round 3 — Cross-examination (each side asks 3 pointed questions; the other must answer with evidence)
Round 4 — Counter-rebuttal addressing the hardest questions from round 3
Round 5 — Closing statements + concession of points where the opponent was correct

DIMENSIONS THAT MUST BE COVERED:
- Team size and cognitive load (Conway's Law, two-pizza teams)
- Time to first revenue / runway burn
- Operational complexity (k8s, service mesh, distributed tracing, on-call)
- Deploy frequency and blast radius
- Data consistency (distributed transactions, saga pattern, eventual consistency)
- Debugging and observability cost
- Hiring market (can a 3-person startup hire SREs?)
- Refactoring cost of "monolith-first → extract services later" (Fowler's MonolithFirst)
- Real case studies: Segment's re-monolith (2018), Amazon Prime Video's re-monolith (2023), Istio/Wealthfront/Uber experience reports
- Domain complexity: DDD bounded contexts vs. CRUD startups
- Failure modes unique to each architecture

REQUIRED OUTPUT:
1. Full 5-round debate transcript with role labels
2. Evidence table (claim → source → quoted fact)
3. Dimension-by-dimension scorecard (who won each dimension and why)
4. Final verdict that EXPLICITLY addresses the word "always":
   - Is the absolutist claim true? (expected: no)
   - Under what specific startup conditions would microservices actually be preferable on day 1? (list them precisely)
   - Under what conditions is a modular monolith the correct default? (list them precisely)
5. A decision checklist the reader can apply to their own startup
6. Confidence score (0–100) for the final verdict with justification

PERSONA: --persona-architect (primary), --persona-analyzer (evidence weighing)
THINKING BUDGET: --ultrathink
MCP: --seq --c7 --tavily
```

### Quick Start (copy-paste)

```bash
/sc:adversarial --rounds 5 --evidence-required --steelman --strict --persona-architect --seq --ultrathink --c7 --tavily --evidence --think-hard --validate "Microservices architecture is ALWAYS preferable to monoliths for new startup projects"
```

### Time & Budget Estimate

Not requested (`--estimate` flag not passed), but rough sizing for context:

- **Debate run**: Medium complexity, expert multiplier 1.0x, large scope 2.5x
- **Expected tokens**: ~8,000–15,000 for the full 5-round adversarial transcript + evidence table + scorecard
- **Wall-clock**: 3–6 minutes of model time depending on MCP latency (Context7 + Tavily round-trips)
- **Follow-on design work** (`/sc:design --api --microservices` or modular-monolith equivalent): 1–3 days of human engineering time to translate verdict into an ADR

### Alternatives (not requested, offered anyway because the claim is absolutist)

| Approach | Command | Pros | Cons |
|----------|---------|------|------|
| Adversarial debate (recommended) | `/sc:adversarial --rounds 5 --evidence-required --steelman` | Forces both sides to be steelmanned; kills "always" bias via `--strict`; evidence-gated | Higher token cost; requires `--c7`/`--tavily` |
| Expert panel | `/sc:spec-panel --experts architect,backend,devops,startup-cto` | Multiple viewpoints simultaneously; faster than 5 rounds | Less rigorous; no forced rebuttal loop |
| Research-first | `/sc:research --deep --tavily "microservices vs monolith startup 2024 2025 2026"` | Pure evidence gathering before debate | No synthesis; user must draw conclusions |
| Brainstorm-first | `/sc:brainstorm --interactive` | Elicits user's actual startup constraints first | Doesn't validate the claim, only contextualizes it |

### Community Data

Not requested (`--community` flag not passed). Skipped.

### Expertise-Level Notes (Expert)

- Direct, minimal hand-holding.
- Assumes reader knows what DDD, sagas, Conway's Law, and MonolithFirst refer to.
- Assumes reader can swap `--persona-architect` for `--persona-backend` if the debate needs to bias toward reliability/operational concerns.
- Reader is expected to critique the generated prompt and iterate — the first run is a draft, not a final answer.

### Boundaries Honored

- Will not execute `/sc:adversarial` automatically — user must invoke.
- Will not fabricate community percentages.
- Will not assume the user's startup context (team size, domain) — the prompt forces the debate to cover these dimensions rather than pre-deciding them.
- Does not override user preference for the absolutist claim; the prompt defends the claim as stated and lets the debate break it.

---

*End of /sc:recommend output.*
