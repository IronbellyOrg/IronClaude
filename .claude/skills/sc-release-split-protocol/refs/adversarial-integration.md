# Adversarial Integration Reference — Release Split Protocol

Reference document for sc:adversarial integration within sc:release-split.
Contains invocation patterns, return contract consumption, convergence routing,
and error handling specific to the release-split context.

**Loaded in**: Part 2 (when adversarial variant generation executes).

---

## Agent Specification Parsing

Follow the canonical Agent Specification Parsing algorithm defined in
sc:adversarial-protocol SKILL.md under "Dual Input Modes > Mode B".

The format is `model[:persona[:"instruction"]]`:
- Split `--agents` value on `,` for individual specs
- Per agent: split on `:` (max 3 segments) → model, persona, instruction
- Quoted second segment = instruction (no persona)
- Validation: 2-10 agents, all models recognized

For full parsing rules, edge cases, and validation error messages, refer to
the canonical source. Do NOT duplicate the algorithm here.

## Default Agent Configuration

When `--agents` is not provided:

| Agent | Model | Persona | Analytical Focus |
|-------|-------|---------|-----------------|
| 1 | opus | architect | Structural boundaries, dependency chains, foundation-vs-application seams, integration points |
| 2 | haiku | analyzer | Risk assessment, cost-benefit analysis, validation feasibility, coordination overhead |

These defaults are chosen because:
- **opus:architect** brings deep structural reasoning — it excels at identifying
  natural seams in complex systems and evaluating dependency chains
- **haiku:analyzer** brings fast, focused risk analysis — it challenges assumptions
  and evaluates whether the split actually enables better testing

## Invocation Pattern

Mode B invocation for split proposal generation:

```
Invoke Skill `sc:adversarial-protocol` with args:
  --source <original-spec-path>
  --generate spec
  --agents <agent-spec-1>,<agent-spec-2>[,...]
  --depth <propagated>
  --interactive <propagated if set>
```

**Important**: Use `--generate spec` (not `--generate split-proposal`). The artifact
type `spec` is a recognized sc:adversarial type. The agent instruction context
(below) shapes the output as a split proposal — the `--generate` value only
controls artifact labeling.

## Context Injection Template

Each agent receives this preamble prepended to their instruction:

```
You are analyzing a release spec to determine if and where it should
be split into two sequential releases. A prior discovery analysis
produced this proposal:

---
[Part 1 proposal summary]
---

You may agree or disagree. Generate your own independent analysis.
Your output MUST include:
1. Recommendation: Split or Don't Split (with confidence 0.0-1.0)
2. If split: Release 1 scope, Release 2 scope, seam rationale,
   real-world validation plan
3. If don't split: rationale, alternative strategies
4. Risks of your recommendation

Global constraints that apply regardless of your recommendation:
- Release 1 defaults to planning fidelity and schema hardening
  unless you provide compelling evidence otherwise
- Smoke gate belongs in Release 2 by default
- All validation must be real-world (no mocks, no synthetic tests)
- "Don't split" is always a valid conclusion
```

## Return Contract Consumption

Parse all 9 fields from the sc:adversarial return contract:

| Field | Type | Consumer Default | Usage in sc:release-split |
|-------|------|-----------------|--------------------------|
| `status` | `success` \| `partial` \| `failed` | `"failed"` | Routes to convergence handling or fallback |
| `merged_output_path` | `string\|null` | `null` | Read merged proposal for verdict extraction |
| `convergence_score` | `float 0.0-1.0\|null` | `0.5` (forces Partial path) | Report in checkpoint; drives convergence routing |
| `artifacts_dir` | `string` | (inferred from `--output`) | Location of debate transcript and scoring artifacts |
| `base_variant` | `string\|null` | `null` | Recorded in split-proposal-final.md frontmatter |
| `unresolved_conflicts` | `integer` | `0` | If > 0, logged as warning |
| `fallback_mode` | `boolean` | `false` | If true, emit differentiated warning |
| `failure_stage` | `string\|null` | `null` | Logged for debugging when status is failed |
| `invocation_method` | `enum` | `"skill-direct"` | Logged for observability |

**Missing-file guard**: After extracting `merged_output_path`, verify the file exists
on disk (Read tool). If missing, treat as `status: failed, failure_stage: transport`.

## Convergence Routing

Thresholds aligned with sc:roadmap for cross-skill consistency:

| Score | Action |
|-------|--------|
| >= 0.6 | PASS — proceed with merged proposal |
| 0.5 - 0.59 | PARTIAL — if `--interactive`, prompt user to confirm or abort. If not `--interactive`, abort: "Convergence XX% below 60% threshold." |
| < 0.5 | FAIL — abort: "Agent proposals too divergent (convergence: X.XX)." |

## Fallback Mode Warning

When `fallback_mode == true` (regardless of status), emit:
```
> **Warning**: Adversarial result produced via fallback path (not primary Skill invocation).
> Quality may be reduced. Review the merged output manually before proceeding.
```

## Error Handling

| Failure | Action |
|---------|--------|
| sc:adversarial Skill tool error | Retry once with --depth quick. If retry fails, fall back to Mode A |
| Agent model unavailable | Fall back to Mode A with warning |
| Return contract unparseable | Use fallback convergence_score: 0.5, route to PARTIAL |
| Merged output file missing | Treat as failed, fall back to Mode A |
| convergence_score < 0.5 | Abort regardless of --interactive flag |
