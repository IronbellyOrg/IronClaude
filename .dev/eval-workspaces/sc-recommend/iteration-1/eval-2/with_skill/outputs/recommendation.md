Goal: Research how the freshness hook system works in this codebase — what the 7 freshness-*.sh scripts do, how they are wired into Claude Code via settings.json, and what behavior they enforce.

Recommended delegation: **auggie MCP `codebase-retrieval` (one semantic sweep) → native Read on the verified files**. The scope is one bounded subsystem (~7 scripts + hook registration + any Python helpers) that already has known entry points on disk. Auggie wins the conceptual / cross-file ranking step that brute Grep would multi-call for. Beyond that, the work is read-and-explain — native Read/Grep finishes it. tech-research is overkill (it builds an MDTM task folder, spawns parallel rf-task-researcher / rf-analyst / rf-qa-qualitative subagents, and produces a synthesis-gated report — those guarantees buy nothing when the surface is 7 files in one directory). deep-research(-agent) is web-focused (Tavily / WebSearch / Playwright / Context7) and would not even read the local scripts — wrong tool for a codebase question.

Paste-ready prompt:

```text
Research the freshness hook system in this codebase. Scope is bounded — ~7 shell scripts plus their registration site plus any Python helpers they call.

Step 1 — Single semantic sweep with auggie. Run one mcp__auggie__codebase-retrieval call with information_request: "Explain the freshness hook subsystem in this repo. Cover (1) what each of the 7 freshness-*.sh scripts in .claude/hooks/ does — pre-edit, post-read, session-start, subagent-start, subagent-stop, user-prompt, file-changed; (2) how they are registered as Claude Code hooks (look at .claude/settings.json and any documented hook event mappings); (3) any Python helpers they shell out to under src/superclaude/hooks/; (4) what behavior they enforce (freshness re-reads, file-modified detection, session-context envelope injection); (5) how src/superclaude/hooks/scripts/ relates to the deployed .claude/hooks/ copies (sync-dev source-of-truth)." Use directory_path = current worktree absolute path.

Step 2 — Read the actual files auggie surfaces. At minimum:
  - .claude/settings.json (hook event registrations)
  - The 7 scripts: .claude/hooks/freshness-{pre-edit,post-read,session-start,subagent-start,subagent-stop,user-prompt,file-changed}.sh
  - Any Python helper they invoke under src/superclaude/hooks/

Step 3 — Synthesize into a short writeup with these sections:
  - Event → hook → script map (which Claude Code event triggers which script)
  - Per-script purpose (1-2 lines each, citing the file)
  - Enforcement behavior (what each blocks, warns about, or injects)
  - Sync model (src/superclaude/hooks/scripts/ is source-of-truth; .claude/hooks/ is sync-dev output)
  - Open questions or gaps surfaced during reading

Do NOT spawn a tech-research MDTM task or a deep-research-agent — the surface is small and local. Use auggie for the conceptual sweep and Read for the file-level detail.
```

Sources verified:

- src/superclaude/skills/sc-recommend/SKILL.md (Read — protocol followed: Phase 0 → 1 → 2)
- src/superclaude/skills/sc-recommend/refs/surface-enumeration.md (Read — Phase 0 algorithm)
- src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md (Read — net-value rubric)
- src/superclaude/skills/tech-research/SKILL.md (Read — verified MDTM-heavy, scope-mismatched for this request)
- src/superclaude/agents/deep-research-agent.md (Read — verified web-focused, wrong tool for codebase scope)
- src/superclaude/mcp/MCP_Auggie.md (auggie ranking returned this — verified MCP primitive)
- src/superclaude/commands/*.md, src/superclaude/skills/*/SKILL.md, src/superclaude/agents/*.md (Glob — full surface enumeration)
- .claude/hooks/freshness-*.sh and src/superclaude/hooks/scripts/freshness-*.sh (Bash ls — confirmed 7 scripts exist at both locations as the user stated)
- auggie semantic rank: confirmed auggie (semantic codebase) and tech-research (MDTM investigation) as the on-surface candidates; deep-research-agent verified web-only; "Explore agent" returned no source file in this repo — dropped as a ghost candidate per Rule R2.

Candidates considered and rejected:

- **tech-research skill** — verified, real, but its MDTM + multi-agent synthesis machinery is sized for cross-subsystem investigations (5-20 files across multiple domains). For 7 scripts in one directory, it loads ~2-3K tokens of protocol to do what auggie + 8 Reads do directly. Rejected on net-value axis 4 (token budget vs. value).
- **deep-research / deep-research-agent** — verified, real, but tooled for *external* knowledge (Tavily, WebSearch, Context7, Playwright). The user's request is explicitly "research the codebase" — no web component. Rejected on capability mismatch.
- **"Explore agent"** — no source file under `src/superclaude/agents/` or `.claude/agents/`. Ghost candidate per Rule R2 — dropped silently from the recommendation (mentioned here only because the eval request named it).
