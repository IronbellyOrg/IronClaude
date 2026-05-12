# baseline-run-3

**Run label:** baseline-run-3
**Timestamp:** 2026-04-15T17:25:10+00:00
**Query:** `/sc:recommend "generate a prompt that uses /sc:adversarial to validate the claim that microservices architecture is always preferable to monoliths for new startup projects"`

---

## /sc:recommend — Intelligent Command Recommendation

### Header

- **Project Analysis:** Meta-request — user is asking for a prompt artifact (not direct code execution). Target command is `/sc:adversarial`, the subject is an architectural claim ("microservices always preferable to monoliths for new startup projects"), and the goal is structured validation/invalidation of an absolutist claim. No filesystem project context is in play for this request; this is a prompt-engineering + architectural-debate task.
- **Language Detection:** English (auto-detected; no Turkish diacritics or mixed-language markers present)
- **Expertise Level:** Expert (the request references an internal SuperClaude command `/sc:adversarial`, uses precise architectural terminology, and asks for prompt composition — all expert-level signals). Style: fast, direct, minimal hand-holding.
- **Primary Persona:** `--persona-architect` (systems design, scalability tradeoffs — the core subject matter)
- **Supporting Personas:** `--persona-analyzer` (claim decomposition, evidence weighting), `--persona-backend` (microservices/monolith operational reality)
- **Category Match:** `api_category` (microservice/architecture keywords) + `create_category` (generate/build a prompt) + implicit `learning_category` undertone (validate a claim → evidence-seeking)
- **MCP Servers:** `--seq` (multi-step adversarial reasoning), `--c7` (official architectural guidance — Fowler, Newman, Richardson), `--tavily` (recent startup post-mortems and industry data)

---

### Primary Commands (Top 3)

1. **`/sc:adversarial --persona-architect --seq --c7 --ultrathink --rounds 3 --evidence-required --steelman --red-team`**
   Core command that will actually run the adversarial debate against the claim. Uses sequential reasoning for structured rounds, Context7 for authoritative architectural sources, ultrathink depth for the full tradeoff space, three debate rounds, mandatory evidence per assertion, steelmanning of the pro-microservices side, and red-teaming to surface failure modes.

2. **`/sc:design --api --ddd --seq --ultrathink --microservices --compare-monolith`**
   Secondary framing command that produces the architectural comparison surface the adversarial debate will judge against. Generates a side-by-side design contract (bounded contexts, deployment unit, data ownership, team topology) so the adversarial rounds have concrete decision criteria rather than hand-waving.

3. **`/sc:analyze --seq --c7 --evidence --think-hard --domain architecture --claim-validation`**
   Evidence-gathering command to back the adversarial rounds with citations: known startup failure patterns (distributed monolith, premature decomposition), success patterns (Shopify's majestic monolith, Basecamp, Segment's re-monolithing), and the conditions under which each applies.

---

### Secondary Commands

- **`/sc:brainstorm --interactive --alternatives`** — surface hidden assumptions in the claim ("always", "preferable", "new startup") before debate begins
- **`/sc:research --tavily --depth deep --recency 2y --topic "startup microservices vs monolith"`** — pull recent post-mortems (2024-2026) on startups that migrated in either direction
- **`/sc:document --user --examples --format prompt-template`** — package the final prompt as a reusable template
- **`/sc:reflect --validate --evidence`** — post-debate sanity check that the adversarial output actually addressed the absolutist framing

---

### Smart Flag Recommendations

**Context-based (medium complexity, expert user, architecture domain):**
- `--plan --validate --seq --ultrathink`
- `--evidence` (required for claim validation)
- `--think-hard` (multi-perspective tradeoff reasoning)

**Debate-specific (adversarial command enhancers):**
- `--rounds 3` (opening / rebuttal / closing)
- `--steelman` (strongest pro-microservices case before attacking it)
- `--red-team` (explicit adversary role)
- `--evidence-required` (no bare assertions)
- `--scoring weighted` (tradeoff-aware, not binary)
- `--persona-architect` primary, `--persona-analyzer` as judge

**Quality / safety:**
- `--strict` (reject hand-waved claims)
- `--validate` (post-hoc check of conclusions against evidence)
- `--dry-run` (preview prompt before committing)

**Do NOT use:**
- `--magic` (no UI component output)
- `--pup` / `--play` (no browser automation)
- `--quick --simple` (this is not a small task)

---

### Generated Prompt (Primary Deliverable)

```text
/sc:adversarial \
  --persona-architect \
  --seq --c7 --tavily \
  --ultrathink --think-hard \
  --rounds 3 \
  --evidence-required \
  --steelman \
  --red-team \
  --scoring weighted \
  --strict --validate \
  "Validate the absolutist claim: 'Microservices architecture is ALWAYS
   preferable to monoliths for new startup projects.'

   === DEBATE CONTRACT ===

   Subject under test: The word 'always' in the claim. The debate is not
   whether microservices are ever correct for a startup — it is whether
   they are universally correct regardless of team size, domain,
   funding stage, product maturity, or operational capacity.

   Roles:
     - PROPONENT (steelman): Argue the strongest possible version of the
       claim. Cite Netflix, Amazon, Uber-scale success stories. Invoke
       independent deployability, polyglot freedom, fault isolation,
       team autonomy (Conway's Law), and horizontal scaling.
     - ADVERSARY (red team): Attack the 'always' universal quantifier.
       Cite Segment's re-monolithing (2018), Istio/Amazon Prime Video's
       2023 move back to monolith, Shopify's majestic monolith,
       Basecamp/HEY, and the distributed-monolith antipattern.
       Reference Fowler's 'MonolithFirst' (2015), Sam Newman's 'Building
       Microservices' (2nd ed.) caveats, and Richardson's decomposition
       prerequisites.
     - JUDGE (--persona-analyzer): Score each round on (a) evidence
       quality, (b) logical validity, (c) whether the argument actually
       addresses 'always' vs 'sometimes'.

   === ROUND STRUCTURE ===

   ROUND 1 — OPENING STATEMENTS
     Proponent: Strongest 3 arguments for universal microservices
       preference. Must cite at least 2 primary sources (blog posts,
       conference talks, books, post-mortems).
     Adversary: Strongest 3 counterexamples where monoliths beat
       microservices for startups. Must cite at least 2 primary sources.

   ROUND 2 — CROSS-EXAMINATION
     Adversary attacks the specific conditions Proponent assumed
       (team size ≥ 50? Series B+ funding? Known bounded contexts?
       SRE headcount?). Surface hidden assumptions.
     Proponent rebuts with scaling-cliff arguments and migration-cost
       data.

   ROUND 3 — CLOSING + VERDICT
     Each side delivers a closing statement constrained to ≤ 200 words.
     Judge renders a verdict on the 'always' claim specifically, using
     this rubric:
       - UPHELD: Evidence shows microservices dominate across ALL
         reasonable startup contexts.
       - REJECTED: At least one common startup context exists where
         monoliths are demonstrably preferable.
       - REFINED: The claim is salvageable only with explicit
         qualifiers — enumerate them.

   === EVIDENCE REQUIREMENTS ===

   Every assertion must be tagged with one of:
     [EMPIRICAL]  — measured data, post-mortem, benchmark
     [EXPERT]     — named authority (Fowler, Newman, Richardson, DHH,
                    Tobi Lütke, Kelsey Hightower, Gregor Hohpe)
     [REASONED]   — first-principles argument, explicitly labeled as
                    such
     [ANECDOTAL]  — single-case story; judge must discount

   Unsupported assertions are struck from the record.

   === TRADEOFF DIMENSIONS (must be addressed) ===

   1. Team size & Conway's Law (2-person founding team vs 50-person org)
   2. Operational overhead (k8s, service mesh, observability, on-call)
   3. Data consistency (distributed transactions, saga complexity)
   4. Deployment velocity (monolith CI/CD can be faster early)
   5. Cognitive load on founding engineers
   6. Time-to-first-revenue (pre-PMF vs post-PMF)
   7. Premature decomposition risk (wrong bounded contexts locked in)
   8. Cost of migration in either direction
   9. Hiring market (microservice ops expertise is expensive)
   10. Failure domain (blast radius of a bad deploy)

   === OUTPUT FORMAT ===

   # Verdict on 'Microservices Always Preferable for Startups'
   ## Round 1 — Opening
     ### Proponent
     ### Adversary
   ## Round 2 — Cross-Examination
     ### Adversary attacks
     ### Proponent rebuts
   ## Round 3 — Closing
     ### Proponent closing
     ### Adversary closing
   ## Judge's Verdict
     - Ruling: UPHELD | REJECTED | REFINED
     - Confidence: 0-100%
     - Required qualifiers (if REFINED)
     - Evidence tally: [EMPIRICAL] N, [EXPERT] N, [REASONED] N,
       [ANECDOTAL] N (discounted)
   ## Recommended Decision Framework for Startup Founders
     A short checklist founders can run against their own context to
     decide which architecture applies to THEM.

   Begin Round 1 now."
```

---

### Quick Start

```bash
# 1. Preview the prompt
/sc:recommend "..." --dry-run

# 2. Run the adversarial debate
/sc:adversarial --persona-architect --seq --c7 --ultrathink \
  --rounds 3 --evidence-required --steelman --red-team \
  "Validate: microservices always preferable to monoliths for startups"

# 3. Validate the output
/sc:reflect --validate --evidence
```

---

### Time & Budget Estimate

*(not requested via `--estimate`, shown as courtesy default for expert-level architectural requests)*

- **Prompt authoring:** 10–15 min (expert multiplier 1.0x)
- **Adversarial debate runtime:** ~2,500 tokens (complex task budget)
- **Evidence lookup (Context7 + Tavily):** 3 rounds × ~500 tokens = 1,500 tokens
- **Total token budget:** ~4,000 tokens for the full adversarial run
- **Confidence-check ROI:** spending 200 tokens on this recommendation saves re-running the debate with a broken prompt (5,000+ tokens)

---

### Alternatives

*(not requested via `--alternatives`, shown abbreviated)*

| Approach | When to use | Tradeoff |
|---|---|---|
| `/sc:adversarial` structured debate (PRIMARY) | Claim has a clear absolutist framing to attack | Heaviest, most rigorous |
| `/sc:spec-panel --experts "fowler,newman,dhh"` | You want named-persona multi-expert panel instead of red/blue team | Less adversarial, more consensus-oriented |
| `/sc:analyze --claim-validation --evidence` | You only want evidence gathering, not debate theatre | Faster, less persuasive output |
| `/sc:brainstorm --devils-advocate` | Early exploration, not final verdict | Too informal for validating absolutist claims |

---

### Community Data

*(not requested via `--community`; skipped per protocol — no fake metrics)*

---

### Notes

- The claim contains "always" — this is the load-bearing word. The adversarial prompt is explicitly structured to attack the universal quantifier, not microservices-vs-monoliths in general.
- The `--steelman` flag is non-negotiable here: without it, the debate collapses into a strawman beat-down and the verdict loses credibility.
- Judge persona (`--persona-analyzer`) is deliberately separated from debater personas to avoid self-scoring bias.
- If running in an actual SuperClaude session, precede with `/sc:load` to ensure session context, and follow with `/sc:save` to persist the verdict.

---

**Recommended next action:** Run the generated prompt above via `/sc:adversarial`. If the verdict comes back `REFINED`, capture the qualifier list as a reusable decision framework in `KNOWLEDGE.md`.
