<!-- markdownlint-disable MD013 MD040 -->

# Socratic Templates — Depth-Tiered Question Banks + Domain Taxonomy

## §Domain-Taxonomy

Classify a brainstorm topic into exactly one of six domains. Apply signals top-down; first matching domain wins.

| Domain | Signals (any 1 match → classify) | Examples |
|--------|----------------------------------|----------|
| `incident` | post-mortem, root cause, outage, broke, regression, incident, debugging, hotfix, p0/p1, paged, woke me up | "deployment broke staging", "payment webhook delivery failures Q1" |
| `code` | file paths, language extensions (`.py`/`.ts`/etc.), function/class/module/endpoint references, dev verbs (implement, refactor, migrate, optimize, fix, add) WHEN paired with code entities | "add rate limiting to API endpoints", "migrate from pytest to vitest" |
| `architecture` | system design verbs (redesign, restructure, decompose), cross-component scope, scalability/integration/topology language, "across", "between services" | "redesign error handling across worker pool", "explore GraphQL for public API" |
| `product` | feature, user-facing, customer, market, monetization, pricing, persona, jobs-to-be-done, MVP, GTM | "AI-powered changelog summarizer feature", "mobile app monetization strategy" |
| `process` | workflow, methodology, team, hiring, onboarding, sprint, ceremony, retrospective, organizational | "improve onboarding workflow for new contributors", "redesign sprint retros" |
| `research` | evaluate, compare, vs, options, choose between, decision, investigate, explore (without code entities), best practices | "evaluate Bun vs Node for backend", "best practices for distributed tracing" |

**Edge cases**:

- Ambiguous code-vs-architecture: if topic mentions ≥3 components or "across", lean `architecture`. Single-component code work is `code`.
- Topic with mixed signals: priority order is `incident > code > architecture > product > process > research`.
- Multi-domain topics (rare): pick primary domain; surface ambiguity as an open question in the seed brief.

## §Strategy-Detection

Apply when `--strategy auto`:

| Signal | Strategy |
|--------|----------|
| Topic mentions compliance, audit, regulation, enterprise, SOC2, SOX, HIPAA, large customers | `enterprise` |
| Topic mentions MVP, prototype, quick, experiment, iterate, ship fast, validate | `agile` |
| Default | `systematic` |

## §Domain-Questions — Depth-Tiered Question Banks

Each domain has 3 tiers: quick (3-5 Qs), standard (6-10 Qs), deep (10-20 Qs). Questions are organized in batches: **Clarify** (always), **Validate** (standard + deep), **Probe** (deep only).

### Domain: `code`

**Clarify batch** (all depths):

1. What's the entry point — a specific file/function, or a feature you want to introduce?
2. What's the scope: single-module change, cross-module refactor, or new subsystem?
3. What's the failure mode you're trying to prevent / behavior you're trying to add?
4. (standard+) Any non-negotiable constraints from existing code (API stability, backward compat, performance SLO)?
5. (standard+) What does "done" look like — a passing test? a deployed feature? a code review?

**Validate batch** (standard + deep):
6. Are there existing implementations in the codebase that this should align with or replace?
7. Who consumes this — internal callers, external API users, or both?
8. What's the test surface — unit, integration, e2e, or all three?
9. Is there a deadline or other forcing function?
10. What's the rollback plan if this change misbehaves in prod?

**Probe batch** (deep only):
11. What's the simplest version that could work? Why isn't that enough?
12. What's the riskiest assumption baked into the topic?
13. If I gave you 2x the time, what would you change? If I gave you 0.5x, what would you cut?
14. What would a security reviewer ask about this?
15. What would a future maintainer curse you for missing?
16. Is there an existing pattern in adjacent code that we should mirror or deliberately break from?
17. What metric would prove this worked in prod?
18. What's the worst-case behavior under load / failure / partial rollout?
19. Any vendor / library / framework constraints I should know?
20. What does this conflict with on the roadmap?

### Domain: `incident`

**Clarify batch**:

1. When did it start? When was it detected? When was it resolved (if it is)?
2. What's the user-visible impact — error rate, latency, data loss, total outage?
3. Was this a single event or a pattern (recurring)?
4. (standard+) Did anything change in the system recently — deploy, config, traffic, vendor?
5. (standard+) Who first noticed, and how?

**Validate batch**:
6. What's the current hypothesis for root cause? How confident are you?
7. What evidence supports it? What evidence contradicts it?
8. Are there parallel hypotheses worth probing?
9. What's the blast radius — single service, region, all users?
10. What's the mitigation currently in place?

**Probe batch**:
11. What detection would have caught this earlier?
12. What runbook step did the on-caller miss or not have?
13. What's the structural prevention vs. tactical patch tradeoff?
14. Has this category of failure happened before — same system or different?
15. What's the cost of full fix vs. ongoing operational burden?
16. Who needs to sign off on the post-mortem?
17. What policy / SLO / compliance angle does this touch?
18. What's the comms plan for affected users?
19. What's the simplest test that could have caught this in CI?
20. If the on-caller had perfect knowledge, what would they have done in the first 5 minutes?

### Domain: `architecture`

**Clarify batch**:

1. What problem is the current architecture causing? (not "what's wrong" but "what hurts")
2. What's the scope of change — single service, service boundary, cross-system, or paradigm shift?
3. What's the constraint hierarchy — performance, cost, complexity, time-to-market, vendor lock-in?
4. (standard+) Who maintains the affected systems? Any cross-team coordination required?
5. (standard+) What's the migration tolerance — bulk rewrite, parallel run, gradual cutover?

**Validate batch**:
6. What architectural patterns are already in use in this codebase / org? Adopt or break from?
7. What's the data model impact? Schema migration? Backfill?
8. What's the API/contract impact? Versioning strategy?
9. What's the operational impact — new monitoring, alerts, runbooks?
10. What's the rollback story?

**Probe batch**:
11. What's the 10x scale stress on this design? What's the 0.1x?
12. What does this conflict with in the existing system?
13. What's the alternative we're rejecting and why?
14. What's the prior art — what have similar orgs done?
15. What's the failure-mode taxonomy at the new architecture?
16. Where are the new coupling points? Where are the new isolation points?
17. What's the cost in dollars + engineering-time + cognitive load?
18. Who has veto authority on this? Have they bought in?
19. What metric would prove the new design works better?
20. What's the 2-year reversibility cost if we're wrong?

### Domain: `product`

**Clarify batch**:

1. Who is the user? Specifically — one persona, not "everyone".
2. What job-to-be-done does this feature address?
3. What's the success metric (north-star, not vanity)?
4. (standard+) What's the MVP scope vs. the full vision?
5. (standard+) What does the user do today instead of using this feature?

**Validate batch**:
6. What's the competitive landscape? Direct competitors, indirect substitutes?
7. What's the pricing/monetization angle (if any)?
8. What's the build-vs-buy-vs-partner analysis?
9. What's the GTM motion — viral, sales-led, product-led?
10. What's the deprecation/sunset criteria if this fails?

**Probe batch**:
11. What's the riskiest assumption — usage, willingness-to-pay, retention, viral coefficient?
12. What's the leading indicator we'd see in week 1, week 4, week 12?
13. What's the support / docs / training burden?
14. Who's the internal champion? What stakes do they have?
15. What policy / legal / privacy considerations?
16. What's the international / accessibility / a11y scope?
17. What does an unhappy user post on social media about this feature?
18. Where does this conflict with existing roadmap?
19. What other features does this unlock or block?
20. What's the smallest experiment that would tell us this works?

### Domain: `process`

**Clarify batch**:

1. What's the current process — concretely, step by step?
2. What hurts about it — friction, gaps, redundancies, missed signal?
3. Who is affected — by role, not by name?
4. (standard+) What's been tried before? Why didn't it stick?
5. (standard+) What's the current measure of process health?

**Validate batch**:
6. What's the change scope — tooling, behavior, both?
7. Who owns the new process?
8. What's the adoption strategy — top-down, bottom-up, opt-in?
9. What's the training / documentation gap?
10. What's the success metric after 30/60/90 days?

**Probe batch**:
11. What process is this replacing? What ceremony will be missed?
12. What's the cultural fit — does this match how this team actually works?
13. What's the failure mode if half the team adopts and half doesn't?
14. What does this look like in 6 months when the initial enthusiasm fades?
15. What's the bus-factor of the process owner?
16. What's the integration with existing tooling?
17. What's the audit / compliance angle?
18. What's the org-wide replicability if this works?
19. What's the worst critique a senior engineer would give?
20. What's the smallest pilot we could run?

### Domain: `research`

**Clarify batch**:

1. What decision does this research need to inform?
2. What are the candidate options — name them.
3. What evaluation criteria matter most? Rank them.
4. (standard+) What's the decision deadline? What's the cost of delay?
5. (standard+) Who decides, and what evidence do they need?

**Validate batch**:
6. What's already known vs. what needs to be researched?
7. What sources are authoritative — official docs, blog posts, papers, benchmarks?
8. What's the depth — survey of options or deep dive on top 2?
9. What's the reversibility cost of each option?
10. What's the proof-of-concept threshold for a real bake-off?

**Probe batch**:
11. What option are you implicitly biased toward? Why?
12. What option would a skeptic pick?
13. What's the 1-year reversibility cost of each option?
14. What's the ecosystem health of each option?
15. What's the talent / hiring impact?
16. What internal stakeholders need to weigh in?
17. What other decisions does this lock in?
18. What constraint hierarchy reveals different winners?
19. Is there a 'none of the above' / 'wait' option?
20. What's the smallest experiment to falsify the top candidate?

## §Synthesis-Rules

After collecting dialogue answers, synthesize the seed brief by:

1. **Problem Statement**: 2-4 sentences answering "what hurts and why now". Pull from Clarify batch answers.
2. **Known Context**: bullet list of established facts from dialogue (and enrichment context if Wave 2A ran).
3. **Constraints**: bullets covering all hard limits (technical, organizational, temporal). Always make explicit even if obvious.
4. **Success Criteria**: bullets that are concrete and verifiable. "Done" must be observable.
5. **Open Questions**: bullets the user could not answer (or partially answered). These become the adversarial debate seeds.

**Token budget for synthesis**: ~1500 tokens max in seed-brief.md body. Reference enrichment artifacts by path rather than inlining.
