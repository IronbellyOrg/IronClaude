# Phase 0 - Surface Enumeration and Auggie Sweep

SKILL.md owns when to enumerate, match and emit. This reference owns source resolution and the per-invocation verification record. The routing guide remains the only fixed routing authority; do not copy it into a keyword/synonym registry.

## Live surface enumeration

List installed locations with `find` or absolute-path Glob calls, not unmatched shell globs. Never put `~` in a Glob pattern. Resolve the home directory first. Run independent project/checkout discovery in parallel and record every candidate's provenance.

| Surface | Location | When |
|---|---|---|
| Installed commands | `$HOME/.claude/commands/sc/*.md` | Always |
| Installed skills | `$HOME/.claude/skills/*/SKILL.md` | Always |
| Installed agents | `$HOME/.claude/agents/*.md` | Always |
| Installed templates | `$HOME/.claude/templates/**/*.md` | Always |
| Project primitives | `.claude/commands/**/*.md`, `.claude/skills/*/SKILL.md`, `.claude/agents/*.md` | Always |
| Plugin primitives | `${CLAUDE_PLUGIN_ROOT}/commands/*.md`, `${CLAUDE_PLUGIN_ROOT}/skills/*/SKILL.md`, `${CLAUDE_PLUGIN_ROOT}/agents/*.md` | Only for a resolved plugin root |
| In-checkout research fallback | `src/superclaude/commands/*.md`, `src/superclaude/skills/*/SKILL.md`, `src/superclaude/agents/*.md`, `src/superclaude/templates/**/*.md`, `src/superclaude/examples/*-template.md` | Only when these exist under the current IronClaude git root |

The current worktree is the repository root returned by `git rev-parse --show-toplevel`, including when cwd is under `.dev/worktrees/<name>/`. Never redirect lookups to another checkout by assumption.

### Research authority versus actual callable copy

Inside an IronClaude checkout, source is authoritative for the intended current contract. That does not prove the same bytes or backing skill will run. Identify the actual callable copy separately:

- Commands: project `.claude/commands/` before installed `~/.claude/commands/`.
- Skills: installed `~/.claude/skills/<name>/SKILL.md` first, then project `.claude/skills/<name>/SKILL.md`.
- Agents: project `.claude/agents/<name>.md` first, then installed `~/.claude/agents/<name>.md`.
- Plugin-qualified invocations: preserve the resolved plugin namespace and inspect its actual primitive; do not silently strip the namespace or substitute an unrelated global copy.

Both installed and project surfaces are valid existence-check locations. When one file must be read, use the kind-specific precedence above. Record duplicates. If canonical and active copies disagree materially, disclose the disagreement as a contract gap instead of certifying intended source behavior as available execution. Do not install/update or edit user configuration to remove the gap.

## Auggie semantic ranking (Step B)

Matched guide rows skip ranking and set `auggie_status: skipped`; enumeration and verification still run. Otherwise issue one semantic query, with the literal enumerated candidate names and the verbatim request:

```text
Rank the top 3-5 enumerated candidates by fit to this request's complete
objective, explicit selection, inputs, deliverable and authorization ceiling.
For each, identify its actual capability, required inputs, useful options,
side effects, relevant dependencies and recent caveats. Do not invent a target
outside the enumerated surface or treat broad wording as implementation intent.
```

Use the current worktree as `directory_path`. No per-candidate Auggie calls. Unavailable or empty ranking degrades transparently to direct file inspection; neither makes an unread target verified.

## Per-candidate verification (Step C)

Apply this gate to each selected matched-row step and each unmatched candidate before output. A cached target is not exempt.

- **Read the interface.** Read the candidate and actual callable copy. Accept option/argument tables, argument hints, formal Usage/trigger signatures and documented positional/keyword syntax. Extract allowed values, required inputs, output/resume behavior, side effects and stopping boundary, not merely flag-looking tokens. Keyword forms such as `mode=update` and `mode=quick` are not invented `--mode` flags.
- **Resolve activation.** Commands may be self-contained or skill-indirected. Follow mandatory skill instructions wherever documented, including `Skill Invocation`, not only `## Activation`. Resolve actual names/frontmatter, including `tdd`; never construct a hypothetical `sc-*-protocol` from a filename.
- **Read relevant dependencies.** Read the backing skill and only references/configuration bearing on the advertised capability, mode, prerequisites or authority. Inspect both installed/project lookup surfaces using the precedence above. Do not recursively audit unrelated dependencies or require an unconditional checkout-only path in a consumer project.
- **Verify lifecycle/provenance.** Reject `deprecated: true` and proven retired framework remnants using current guide lifecycle guidance or verified canonical retirement evidence. A readable installed remnant or matching cached hash does not establish support. Source absence alone is not retirement evidence: legitimate installed-only/custom extensions remain eligible. Uncertain same-name custom ownership needs clarification, not blanket rejection/deletion. Verify replacements independently instead of trusting stale migration metadata.
- **Keep evidence narrow.** Examples corroborate formal declarations. An example-only flag missing from or conflicting with the declared interface is not supported. Ambiguous prose-only controls remain unverified; retain natural-language intent if the verified target supports it, or disclose the limitation. Read prerequisite inputs before promising a runnable handoff.

### Outcomes

| Evidence | Output treatment |
|---|---|
| Interface, actual copy and relevant dependencies agree | Eligible candidate; ranking can still be degraded |
| Command or required backing skill is missing | Unavailable; keep a matched step visible as `not installed: <name>`, never an unqualified runnable claim |
| Required input, mode, authority or canonical/active-copy contracts materially disagree | Contract gap; state the incompatible claim, withhold the unsupported invocation and never union conflicting interfaces |
| Proven shipped retirement or explicit deprecation | Not a current-framework runnable target; explicit questions receive an intent-preserving retirement explanation |
| Custom override ownership is uncertain | Ask one targeted clarification; do not delete, reinstall or silently substitute |
| Irrelevant unmatched source is missing | Drop the ghost without noisy warnings |

A resolvable file alone is not success. Never authenticate, execute the recommended command, delete remnants or expand plugin packaging to conceal a limitation.

## Verified candidate record

This record is local to one invocation, keyed by target. It is not a durable ownership database or a cache-schema change.

```yaml
target: "sc:spec-panel"
kind: command
source_path: "<resolved research source>"
active_source_path: "<resolved callable copy>"
source_provenance: "<installed, project, plugin, or checkout research fallback>"
activation_style: self-contained
protocol_skill: null
dependency_paths: []
interface_evidence: "<table, argument hint, formal Usage, or declared keyword syntax>"
flags: ["--mode", "--focus"]
required_inputs: ["<existing specification>"]
requested_scope: "<deliverable, compatible selected controls and authority ceiling>"
side_effects: "<source/report/memory/external effects and explicit stop>"
lifecycle_status: current
availability: eligible
contract_gap: null
auggie_summary: "<verified rank notes, skipped, unavailable, or empty>"
```

Include only verified fields and exact interface values. Current source/dependency reads must precede emission; if a relevant file changes, invalidate its local record and reread it. No record survives into another invocation as authority.

## Cardinality and clarification

Carry at most three candidates into output construction: one primary, at most two genuinely distinct net-value alternatives. A matched routing row is one candidate, but every selected step is verified. Do not add alternatives merely for option variations.

If the complete objective remains ambiguous, ask one useful question about the desired deliverable or input format. Artifact labels alone do not choose the evaluation objective. Never send a user already inside recommendation back to recommend, or choose heavier MDTM process to avoid resolving ambiguity.
