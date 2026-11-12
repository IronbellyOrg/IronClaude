# Wave 2B: agent-spec composition

Persona source: refs/agent-spec-builder.md §Persona-Matrix, domain `architecture`, strategy `systematic` (not enterprise), proposals 3: `architect`, `analyzer`, `backend` (first 3 of architect, analyzer, backend, devops, performance, scribe). `security` auto-excluded (not in list, not named by user).
Models: default rotation `opus,sonnet,haiku` (skill-pinned). No Fable, no Tier 0. Opus (Tier 1a) is the ceiling and is used once, for the architect proposal.
Persona availability: agent files `system-architect`, `root-cause-analyst`/`backend-architect` exist in the installed agent list; the personas `architect`, `analyzer`, `backend` are recognised persona names in the builder (refs/agent-spec-builder.md:11-16, 81-92). Existence of `~/.claude/agents/<persona>.md` for the bare names is UNVERIFIED; the adversarial protocol accepts persona names as lenses.
Instructions use only `{domain}`=architecture and `{strategy}` (sanitized: no `, : ' "`). The raw topic is never referenced.

## Composed spec

```
opus:architect:'prioritize maintainability and extension scaffolding for architecture domain',sonnet:analyzer:'focus on root-cause analysis and evidence-based reasoning for architecture',haiku:backend:'focus on API contracts, data integrity, idempotency, and operational concerns'
```

## Round-trip validation (done by hand against §Validation, refs/agent-spec-builder.md:122-134)

1. Split on `,` outside single quotes: 3 agents == proposals 3. (The backend instruction holds commas inside its quotes; same shape as test vector row 2/3 at lines 166-167.)
2. Per agent split on `:` respecting quotes: segments = 3 each; segment 1 in {opus, sonnet, haiku}; segment 2 in {architect, analyzer, backend}; segment 3 single-quoted with no embedded `'`.
3. No duplicate (persona, model) pairs.
Result: valid.

## Token-budget pre-flight (refs/agent-spec-builder.md; SKILL.md Wave 2B step 5)

SKILL.md figures: standard depth multiplier 150K per proposal; weights architect 1.3, analyzer 1.3, backend 1.0, mean 1.2.
estimate = 3 x 150,000 x 1.2 = 540,000. Depth is standard, so the deep auto-downgrade (>500K at deep) does not apply; 540,000 is below the 650,000 STOP line. Hard kill at 1.25 x estimate = 675,000.
Note: the ref file's own figures (15K per proposal, STOP at 350K) differ from SKILL.md's (150K, STOP at 650K) by a factor of 10; SKILL.md is the protocol of record, the ref's lower figures would give 54,000, also passing. Recorded as a protocol inconsistency, not acted on.
Preflight: PASS.
