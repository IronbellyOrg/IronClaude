# Wave 2B: agent spec and token pre-flight

- Personas: architect, analyzer, backend (architecture-domain default, no `--personas`; security auto-excluded, not requested).
- Models: deep tier puts opus on the first two personas, then rotation gives haiku (opus, sonnet, haiku list; slot 3 = haiku per the ref's deep-tier rule).
- Spec (round-trip checked: 3 agents, 3 segments each, quotes balanced):

```
opus:architect:'prioritize maintainability and extension scaffolding for architecture domain',opus:analyzer:'focus on root-cause analysis and evidence-based reasoning for architecture',haiku:backend:'focus on API contracts, data integrity, idempotency, and operational concerns'
```

- Estimate: 126,000 tokens, from `refs/agent-spec-builder.md` (35K per deep proposal x weights 1.3 + 1.3 + 1.0 = 3.6 x 35K). Under its 250K downgrade and 350K stop thresholds: PASS.
- Conflict recorded: `SKILL.md` Wave 2B uses 350K per deep proposal with 500K/650K thresholds; that would give 1,260,000 and force a STOP even at 3 proposals, the minimum the downgrade allows, so the two are not consistent. The ref's internally consistent figures were used. Hard-kill threshold (1.25 x estimate = 157,500) cannot be measured from inside the session.
- Adversarial skill: `~/.claude/skills/sc-adversarial-protocol/SKILL.md`, no `version:` field (legacy-compatible, INFO).
