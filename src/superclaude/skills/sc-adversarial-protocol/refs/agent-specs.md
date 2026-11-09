# Agent Specifications Reference

Agent specification format, advocate behavior rules, and dynamic agent instantiation for the adversarial pipeline.

---

## Agent Specification Format

Agents are specified using a hybrid format combining model selection with optional persona and instruction:

```
<selection>                              # default or explicit supported alias
<selection>:<persona>                    # Selection + persona
<selection>:<persona>:'<instruction>'    # Canonical single-quoted instruction
<selection>:<persona>:"<instruction>"    # Compatible double-quoted instruction
```

### Components

#### Model (Required)

The requested selection for this agent: `default`, `opus`, `sonnet`, `haiku` or `fable`. `default` is a reserved protocol marker, not a native model alias: preserve it through parsing, then omit the native model parameter. This uses the user's role-permitted configured default bound by ccsession. Explicit supported aliases stay explicit, subject to administrative force semantics and the shared shim's destination check. Never pass `default`, `inherit`, full backend IDs or arbitrary gateway aliases as a native model.

Lists may mix default and explicit selections and may repeat `default`. Preserve list order. Selection labels are not evidence of a served backend or role permission; resolution depends on the active environment.

#### Persona (Optional)

Maps to SuperClaude persona system for specialized behavior.

| Persona | Specialization | Debate Focus |
|---------|---------------|--------------|
| `architect` | Systems design, scalability | Structure, dependencies, long-term impact |
| `security` | Threat modeling, compliance | Vulnerabilities, attack surface, compliance |
| `analyzer` | Root cause, investigation | Evidence quality, logical consistency |
| `frontend` | UI/UX, accessibility | User experience, accessibility, performance |
| `backend` | Reliability, APIs | Data integrity, scalability, fault tolerance |
| `performance` | Optimization, metrics | Efficiency, bottlenecks, resource usage |
| `qa` | Testing, quality | Edge cases, test coverage, failure scenarios |
| `scribe` | Documentation, clarity | Writing quality, audience fit, completeness |

When no persona is specified, the agent uses the model's default behavior.

#### Instruction (Optional)

Custom instruction string that further shapes agent behavior within the debate.

```
opus:architect:"focus on scalability and backward compatibility"
sonnet:security:"zero-trust architecture, assume hostile environment"
opus:analyzer:"prioritize evidence-based claims over theoretical arguments"
```

Instructions are injected into the agent's system prompt alongside persona directives.

### Parsing Rules

1. Split agents on commas only outside quotes, then split fields on colons only outside quotes. Accept 1-3 nonempty segments: selection alone, selection:persona, or selection:persona:quoted-instruction. Reject empty agents/fields and extra segments.
2. Accept only `default`, `opus`, `sonnet`, `haiku`, `fable` as selection. Unknown selection: STOP `Unknown model: <model>`. Keep the default marker in the parsed model field until dispatch.
3. Map a provided persona to SuperClaude behavior. Unknown persona: WARN `Unknown persona '<persona>', using model defaults`; retain its requested label. The builder's recognized personas remain valid.
4. Instructions must occupy an entire field inside matching single or double quotes. Single quotes are the builder's canonical form; existing double-quoted explicit specs remain accepted. Inside quotes, backslash escapes only the matching quote or another backslash; preserve other backslashes. Decode once. Commas, colons and the other quote character inside quotes are data. Reject unmatched quotes, dangling escapes and trailing text after a closing quote. Missing quotes: STOP `Instruction must be quoted: <spec>`.
5. Never evaluate or shell-execute a serialized specification. Keep parsed instructions as prompt data. Structural tokens must not become instructions. Native generation dispatch omits model for `default` and passes only a validated explicit supported alias otherwise. Agent count remains 2-10.

### Examples

```bash
# Single model
--agents opus,sonnet

# Model + persona
--agents opus:architect,sonnet:security,opus:analyzer

# Full specification
--agents opus:architect:"prioritize backward compatibility",sonnet:security:"zero-trust"

# Mixed specifications
--agents opus:architect,sonnet,haiku:qa:"focus on edge cases"
```

---

## Advocate Agent Behavior

Advocate agents are NOT pre-defined. They are instantiated dynamically from the `--agents` specification for each adversarial debate session.

### Advocate Role

Each advocate:

1. **Receives**: Their variant + all other variants + diff-analysis.md
2. **Argues for**: Their variant's strengths in the specified focus areas
3. **Critiques**: Weaknesses in other variants with evidence
4. **Responds**: To rebuttals in subsequent rounds

### Steelman Requirement

Advocates MUST follow the steelman debate strategy:

```yaml
steelman_protocol:
  before_critiquing:
    action: "Construct the strongest possible version of opposing positions"
    purpose: "Demonstrate understanding before disagreement"
    format: |
      ## Steelman: Variant [X]
      The strongest argument for Variant X's approach is: [steelman]
      This addresses: [what it gets right]
      However, I believe Variant [mine] improves upon this because: [critique]

  evidence_requirement:
    - "Every strength claim must cite specific section/content from the variant"
    - "Every weakness claim must cite specific evidence or absence of evidence"
    - "Speculative claims must be labeled as such"
```

### Advocate Prompt Template

When instantiating an advocate via Task tool:

```yaml
advocate_prompt_template:
  system_context: |
    You are an advocate agent in a structured adversarial debate.
    Your variant: [variant name]
    Requested selection: [model] (not an observed backend)
    Persona: [persona or 'default']
    Custom instruction: [instruction or 'none']

    RULES:
    1. Argue for your variant's strengths with evidence
    2. STEELMAN opposing variants before critiquing them
    3. Cite specific sections, quotes, or content as evidence
    4. Acknowledge genuine weaknesses in your variant honestly
    5. Focus on these areas: [focus areas from --focus flag]

  round_1_input:
    - "Your variant content"
    - "All other variant contents"
    - "diff-analysis.md"

  round_2_input:
    - "All Round 1 transcripts"
    - "Specific criticisms of your variant to address"

  round_3_input:
    - "All Round 1 and Round 2 transcripts"
    - "Remaining unresolved disagreements"
```

### Advocate Output Format

```markdown
## Advocate: [Variant Name] ([agent-spec])

### Position Summary
[1-3 sentence summary of overall argument]

### Steelman: [Other Variant Name]
[Strongest version of opposing argument before critique]

### Key Strengths Claimed
1. [Strength with evidence citation]
2. [Strength with evidence citation]

### Weaknesses in [Other Variant]
1. [Critique with evidence citation]

### Concessions
- [Any genuine weaknesses acknowledged in own variant]
```

---

## Agent Instantiation Protocol

### Mode A (Compare)

- One advocate per input file
- Without `--agents`, assign `default` to each file's advocate and omit the native model parameter, using the role-permitted configured child default rather than the current parent model.
- When `--agents` is explicitly supplied, preserve its validated selections, personas, instructions and order through every debate round and retry.
- Advocates named: `Advocate for Variant 1`, `Advocate for Variant 2`, etc.

### Mode B (Generate + Compare)

- Each `--agents` spec generates one variant AND provides one advocate
- The generating agent becomes the advocate for its own variant
- Agent spec explicitly provided via `--agents` flag

### Agent Count Validation

```yaml
agent_validation:
  minimum: 2
  maximum: 10
  mode_a:
    count: "Number of files in --compare list"
    agents: "Auto-assigned (one per file)"
  mode_b:
    count: "Number of specs in --agents list"
    agents: "As specified"
  error:
    too_few: "STOP: 'Adversarial comparison requires at least 2 variants'"
    too_many: "STOP: 'Maximum 10 variants supported'"
```

---

## Agent Coordination

### Parallel Execution (Round 1)

All advocate agents run simultaneously via parallel Task tool calls.

### Sequential Execution (Rounds 2-3)

Each advocate receives all previous round transcripts before responding. Order follows input order (Variant 1 first, then 2, etc.).

### Failure Handling

- Single agent failure: Retry once with the same selection/persona/instruction and model omission or explicit alias, then proceed with N-1 advocates
- Multiple failures: If fewer than 2 advocates remain, abort debate
- Timeout: Agent-level timeout inherits from Task tool defaults

---

*Reference document for sc:adversarial skill*
*Source: SC-ADVERSARIAL-SPEC.md Sections 5.1-5.3, FR-001*
