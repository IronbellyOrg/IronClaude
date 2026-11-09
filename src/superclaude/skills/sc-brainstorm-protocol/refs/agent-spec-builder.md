<!-- markdownlint-disable MD013 MD040 -->

# Agent-Spec Builder — Persona Selection + Model Rotation + Sanitization

## §Persona-Matrix

Default persona selection per domain (used when `--personas` not provided and `--strategy` is NOT `enterprise`).

| Domain | Default personas (priority order — truncate/pad to --proposals count) |
|--------|----------------------------------------------------------------------|
| `code` | `architect`, `refactorer`, `qa`, `backend`, `frontend`, `analyzer` |
| `architecture` | `architect`, `analyzer`, `backend`, `devops`, `performance`, `scribe` |
| `incident` | `analyzer`, `devops`, `qa`, `architect`, `backend`, `performance` |
| `product` | `architect`, `frontend`, `scribe`, `analyzer`, `backend`, `qa` |
| `process` | `scribe`, `analyzer`, `architect`, `qa`, `mentor`, `devops`, `refactorer` |
| `research` | `analyzer`, `architect`, `scribe`, `performance`, `backend`, `devops` |

**Enterprise strategy override** (any domain, when `--strategy enterprise`):
`architect`, `analyzer`, `devops`, `scribe`, `qa` (in this order; truncate/pad to --proposals).
(`analyzer` replaces the former `security` advocate — security is auto-excluded per §Auto-Exclusion; request it explicitly with `--personas …,security` to restore it, even in enterprise mode.)

**Truncation/padding rules**:

- If `proposals < len(default-list)`: truncate from the right (keep highest-priority personas).
- If `proposals > len(default-list)`: cycle the list (e.g., for proposals=10 in code domain, add `architect, refactorer, qa` again starting from position 8).

**Persona availability**: Verify each selected persona has a corresponding agent file at `.claude/agents/<persona>.md` (project) or `~/.claude/agents/<persona>.md` (installed); either satisfies (or known persona alias). If a persona is unknown, substitute the next from the priority list and emit INFO log.

## §Auto-Exclusion

```
auto_excluded_personas = { security }
```

Personas in `auto_excluded_personas` are **NEVER auto-selected** — not from a domain default, not from the enterprise override, and not from pad/cycle backfill. They are reachable **only** when named explicitly in `--personas`. This makes the brainstorm refuse to apply a security lens unless the user specifically asks for it.

Apply this filter **AFTER** persona selection (the §Persona-Matrix / enterprise / `--personas` branch) and **BEFORE** §Model-Rotation:

```
explicit  = set(--personas)  if --personas is non-empty  else {}
selected  = [p for p in selected if (p not in auto_excluded_personas) or (p in explicit)]
# Backfill to --proposals from the SAME priority list (domain default or enterprise override),
#   skipping any p in auto_excluded_personas UNLESS p in explicit.
for each dropped persona p:
    INFO: "Persona '<p>' excluded from auto-selection (not named in --personas). Substituted '<next>'."
```

Notes:

- `--personas architect,security` (or any list naming `security`) keeps `security` — `explicit` contains it, so the filter does not drop it.
- The guard is a runtime backstop: even if a future edit re-adds `security` to a §Persona-Matrix row or the enterprise override, it is still stripped from auto-selection here.

## §Model-Rotation

**Omitted `--models`**: assign `default` to every selected persona at quick, standard and deep depths. `default` is a reserved protocol marker, not a native model alias. Preserve it until native dispatch, where it means omit the model parameter and use the user's role-permitted configured default.

**Explicit `--models`**: accept `default`, `opus`, `sonnet`, `haiku`, `fable`; reject empty entries, `inherit`, full backend IDs and arbitrary gateway aliases. Preserve list order and round-robin assign `(persona_i, models[i mod len(models)])`. Mixed default/explicit lists are legal. Depth never promotes or replaces a selection. Alias resolution is environment-dependent, not proof of a served backend or role permission; the shared ccsession shim checks destinations.

**Example assignments** (selection:persona, requested labels only):

| proposals | depth | selection input | assignment |
|-----------|-------|-----------------|------------|
| 2 | quick | omitted | default:architect, default:refactorer |
| 3 | standard | omitted | default:architect, default:refactorer, default:qa |
| 5 | deep | omitted | default:architect, default:refactorer, default:qa, default:backend, default:frontend |
| 5 | deep | explicit --models sonnet,haiku | sonnet:architect, haiku:refactorer, sonnet:qa, haiku:backend, sonnet:frontend |
| 3 | deep | explicit --models default,opus | default:architect, opus:refactorer, default:qa |

## §Instruction-Templates

Per-persona, parameterized by `{domain}` and `{strategy}`. **NEVER reference the raw user topic** — injection risk.

Templates use single-quoted strings to allow shell-style serialization downstream.

| Persona | Template |
|---------|----------|
| `architect` | `prioritize maintainability and extension scaffolding for {domain} domain` |
| `analyzer` | `focus on root-cause analysis and evidence-based reasoning for {domain}` |
| `security` | `focus on OWASP Top 10, supply-chain risks, and least-privilege; assume hostile environment` <!-- applied ONLY when security is explicitly requested via --personas; never auto-selected (see §Auto-Exclusion) --> |
| `backend` | `focus on API contracts, data integrity, idempotency, and operational concerns` |
| `frontend` | `focus on user experience, accessibility, error states, and responsive behavior` |
| `qa` | `focus on test surface, edge cases, regression risk, and acceptance criteria` |
| `devops` | `focus on deployment, observability, runbooks, and SLO impact for {strategy} delivery` |
| `refactorer` | `focus on technical debt, simplification, and minimal-risk transformation paths` |
| `performance` | `focus on bottlenecks, scaling behavior, and cost-to-serve` |
| `scribe` | `focus on documentation clarity, decision rationale, and audit trail` |
| `mentor` | `focus on team uplift, knowledge transfer, and pattern adoption` |

**Parameter sanitization rule** (mandatory before substitution):

- For each placeholder `{X}` in template:
  - Strip these characters from the substituted value: `,`, `:`, `'`, `"`, newline, tab, control chars
  - If sanitized value becomes empty → use the placeholder literal as-is (e.g., template becomes `... for code domain` if `{domain}` was somehow empty)

**Custom-instruction omission**: If `--proposals == 2`, omit custom instructions entirely (use bare `model:persona` syntax) to maximize variance from default agent behavior. This is a deliberate diversity heuristic.

## §Serialization

Build the agent-spec string from the list of `(persona, model, instruction)` tuples.

**Format per agent**:

- No instruction: `<model>:<persona>` (e.g., `default:architect`)
- With instruction: `<model>:<persona>:'<instruction>'` (e.g., `default:architect:'prioritize maintainability'`)

**Escaping**: Escape backslashes first (`\` becomes `\\`), then replace `'` in instructions with `\'`. (Example: `don't break the API` → `don\'t break the API`.) Decode escapes once in the consumer, never through a shell.

**Agent separator**: `,` between agents.

**Final string example**:

```
default:architect:'prioritize maintainability and extension scaffolding for code domain',default:refactorer:'focus on technical debt, simplification, and minimal-risk transformation paths',default:qa:'focus on test surface, edge cases, regression risk, and acceptance criteria'
```

## §Validation

Round-trip the serialized agent-spec through the adversarial parser to verify:

1. **Split on `,` only outside quotes**: count of agents == expected proposal count; no empty entries.
2. **Per agent split on `:` only outside matching single or double quotes**:
   - Builder emits 2 or 3 segments (selection:persona OR selection:persona:instruction); the consumer also accepts a selection alone.
   - Segment 1 is `default`, `opus`, `sonnet`, `haiku` or `fable`.
   - Segment 2 is a nonempty recognized persona name.
   - Segment 3 (if present) occupies the entire quoted field. Builder emits single quotes; consumer also accepts matching double quotes for existing explicit specifications. Inside a quoted field, backslash escapes only a matching quote or another backslash; preserve other backslashes. Escape backslashes before matching quotes when serializing, then decode once when parsing. Reject unmatched quotes, dangling escapes, extra segments and trailing text outside a closing quote. Commas, colons and the other quote character inside the field are instruction data, never structure.
   - Never evaluate or shell-execute the serialized string; pass the parsed instruction as prompt data. A structural `default` token is accepted only in segment 1, never interpolated into instructions.
3. **No duplicate (persona, model) pairs** — emit INFO if duplicate detected (not a STOP, since duplicate combos are sometimes intentional in deep mode)

**Validation failure**: STOP with `"Agent-spec serialization produced invalid output. This is a bug — please report. Spec: <serialized>"`

## §Token-Budget-Estimation

Token estimate per Wave 3:

```
estimate = proposals × depth_multiplier × persona_weight_avg
```

Where:

- `depth_multiplier`: quick=8000, standard=15000, deep=35000 (tokens per proposal)
- `persona_weight`: 1.0 default; 1.3 for `architect` and `analyzer` (heavier reasoning)
- `persona_weight_avg`: mean of per-persona weights in the agent list

**Auto-downgrade triggers** (in Wave 2B):

- `estimate > 250000` AND `depth == deep` → downgrade `proposals` to 3, re-validate
- `estimate > 350000` post-downgrade → STOP

**Hard kill threshold** (Wave 3 mid-execution):

- Cumulative measured tokens > `1.25 × estimate` → abort with partial-state preservation

## §Round-Trip Test Vectors

For unit/integration testing of the builder, the following inputs MUST produce these outputs:

| Input | Output |
|-------|--------|
| domain=code, proposals=2, depth=quick, strategy=systematic, default models | `default:architect,default:refactorer` |
| domain=code, proposals=3, depth=standard, default | `default:architect:'prioritize maintainability and extension scaffolding for code domain',default:refactorer:'focus on technical debt, simplification, and minimal-risk transformation paths',default:qa:'focus on test surface, edge cases, regression risk, and acceptance criteria'` |
| domain=incident, proposals=5, depth=deep, default | `default:analyzer:'focus on root-cause analysis and evidence-based reasoning for incident',default:devops:'focus on deployment, observability, runbooks, and SLO impact for systematic delivery',default:qa:'focus on test surface, edge cases, regression risk, and acceptance criteria',default:architect:'prioritize maintainability and extension scaffolding for incident domain',default:backend:'focus on API contracts, data integrity, idempotency, and operational concerns'` |
| --strategy=enterprise, proposals=5, default models | `default:architect:'prioritize maintainability and extension scaffolding for {domain} domain',default:analyzer:'focus on root-cause analysis and evidence-based reasoning for {domain}',default:devops:'focus on deployment, observability, runbooks, and SLO impact for enterprise delivery',default:scribe:'focus on documentation clarity, decision rationale, and audit trail',default:qa:'focus on test surface, edge cases, regression risk, and acceptance criteria'` |

(Note: `{domain}` literal in row 4 is the post-sanitization fallback when domain happens to be empty/unsanitizable; in practice this shouldn't happen because Wave 1 classification always produces a value.)
