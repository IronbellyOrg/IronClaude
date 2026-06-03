Goal: Research 3 protocol SKILL.md files in parallel and synthesize the findings into a single workflow-design deliverable.

Recommended delegation: **Parallel Agent fan-out** — a single message spawning 3 `Agent` calls (one per file), followed by a synthesis step in the parent. This wins on wall-clock and context-isolation over a sequential `/sc:research` chain; each agent gets a clean window to deeply read one protocol without cross-contamination, and the parent does the cross-cutting synthesis. A sequential 3x `/sc:research` chain would serialize the work and bleed context between targets. A single `tech-research` invocation would compress all three protocols into one context window and lose fidelity. See `refs/delegation-vs-native-heuristics.md` → "Special case — parallel agent fan-out".

Paste-ready prompt:

```text
Use the Agent tool to spawn 3 parallel research agents in a SINGLE message (not sequentially):

  - Agent 1 (deep-research): Read src/superclaude/skills/sc-adversarial-protocol/SKILL.md end-to-end. Return: purpose, activation surface, inputs/outputs, phase structure, return contract, integration touchpoints (which other skills/commands invoke or are invoked by it), and any caveats or known limits called out in the file. Include verbatim citations of load-bearing sections.

  - Agent 2 (deep-research): Same brief, applied to src/superclaude/skills/sc-reflect-protocol/SKILL.md. Pay particular attention to UC-1 vs UC-2 modes, the tier structure (Tier 1/2/3), the heterogeneous-reviewer ensemble, and the evidence-validator gate.

  - Agent 3 (deep-research): Same brief, applied to src/superclaude/skills/sc-tasklist-protocol/SKILL.md. Pay particular attention to the roadmap-validation integration, the Sprint CLI bundle format, and the /sc:task compliance tier handoff.

After all 3 agents return, synthesize into a single workflow design that answers:
  1. How these 3 protocols compose in practice (which one feeds which).
  2. The natural ordering(s) for a workflow that uses all three.
  3. Hand-off contracts between them (what artifact one produces that the next consumes).
  4. Gaps, overlaps, or conflicts between the three protocols.
  5. A recommended end-to-end workflow with concrete invocation commands.

Deliverable: a single markdown document with one section per agent's findings plus a final "Composed Workflow" section. Cite file paths and section headings, not line numbers (line numbers drift).
```

Sources verified:

- /config/workspace/IronClaude/.claude/worktrees/recommendv2/src/superclaude/skills/sc-adversarial-protocol/SKILL.md (exists)
- /config/workspace/IronClaude/.claude/worktrees/recommendv2/src/superclaude/skills/sc-reflect-protocol/SKILL.md (exists)
- /config/workspace/IronClaude/.claude/worktrees/recommendv2/src/superclaude/skills/sc-tasklist-protocol/SKILL.md (exists)
- /config/workspace/IronClaude/.claude/worktrees/recommendv2/.claude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md (Read — "Special case — parallel agent fan-out" section)
- auggie semantic rank: skipped — the delegation pattern is determined by the request shape (3 independent files, synthesize), which the refs file explicitly names as the parallel-fan-out trigger; auggie ranking against the local skill surface would surface `tech-research` / `deep-research` but would not change the fan-out vs. sequential decision.
