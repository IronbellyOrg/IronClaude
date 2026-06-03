# Recommendation: Research Freshness Hook System

## Framing

This is a codebase research task in a SuperClaude project — a focused investigation of an existing subsystem (hooks). The SuperClaude framework has a dedicated `tech-research` skill for exactly this kind of work: deep technical investigation that produces a structured report with findings, gap analysis, and citations grounded in real files. The hook layer is also referenced in CLAUDE.md (`freshness-pre-edit` enforcement, `UserPromptSubmit` session-context injection, `verify-sync` pre-commit) so there is concrete code to ground the investigation in.

Auggie MCP should drive the initial discovery sweep (highest-priority server per CLAUDE.md, low token cost, broad semantic recall), with Serena for symbol-level follow-up and Read for precise file:line citations. The output should be a structured tech-research report covering: what the freshness hook is, where it lives, what events trigger it, what it enforces, how it interacts with the session-context envelope and the five content-signal triggers (S1-S5), and any gaps or extension points.

## Paste-Ready Prompt

```
/sc:research Research how the freshness hook system works in this codebase.

Scope:
- Locate all freshness-related hooks (likely PreToolUse / UserPromptSubmit / PostToolUse) in .claude/settings.json and src/superclaude/hooks/ (or wherever hook implementations live).
- Document the trigger conditions, inputs, exit codes, and blocking behavior for each freshness hook.
- Map the hook layer to the "Context freshness discipline" section in CLAUDE.md — specifically the S1-S5 content-signal triggers and the session-context envelope (turn=, Δ=, git=dirty=, changed_since_last_turn=).
- Identify how Read freshness is tracked (mtime? hash? turn counter?) and what causes a re-Read to be required.
- Note interactions with verify-sync, freshness-pre-edit, and any related markdownlint / sync-dev enforcement.
- Surface gaps: hook coverage holes, bypass vectors (e.g., chat-only citations the hook can't catch), and extension points.

Deliverables:
- Structured tech-research report under .dev/releases/ or .dev/research/ with file:line citations to every claim.
- Architecture diagram (text/mermaid) of hook event flow.
- Gap analysis and recommended next steps.

Use auggie MCP first for broad discovery, then serena for symbol-level navigation, then Read for exact citations. Ground every claim in a real file path + line range.
```

## Why this approach

- `/sc:research` (backed by the `tech-research` skill) is purpose-built for "research how X works and figure out what we'd need to change" — the exact shape of the request.
- Auggie-first is mandated by CLAUDE.md for broad codebase context; freshness hooks are spread across `.claude/settings.json`, `src/superclaude/hooks/`, and the CLAUDE.md discipline section, so semantic recall beats grepping.
- Produces a citable, structured artifact (not just a chat answer) that downstream work — task-builder, confidence-check, TDD — can consume.

## Alternatives considered

- Plain `codebase-retrieval` + Read loop — works for a quick answer but produces no durable artifact and no gap analysis.
- `/sc:analyze` — too broad; targets quality/security/perf/architecture across a whole codebase, not a focused subsystem investigation.
- `/sc:explain` — good for "explain this to me" but doesn't produce a research report with findings/gaps/recommendations.
