 Codebase Context

  Relevant Existing Code:
  - src/superclaude/commands/task-unified.md — The unified command (name: task), invokes
  sc:task-unified-protocol skill for STANDARD/STRICT tiers
  - .claude/commands/sc/task.md — Legacy deprecated command, still present with deprecated: true
  - src/superclaude/skills/sc-task-unified-protocol/SKILL.md — Protocol skill for execution
  (STANDARD/STRICT flows)
  - src/superclaude/cli/sprint/process.py:170 — Sprint CLI constructs prompts with /sc:task-unified
  - src/superclaude/cli/cleanup_audit/prompts.py — 5 prompt builders also use /sc:task-unified

  Architecture & Patterns:
  - Sprint pipeline: execute_sprint() → per-phase ClaudeProcess → build_prompt() → spawns claude -p
  subprocess with /sc:task-unified prefix
  - Pipeline executor: Generic execute_pipeline() with sequential/parallel step groups and gate
  checking
  - Tasklist format (example: .dev/releases/current/turnledger-integration/v3.05/tasklist.md):
  Wave-based with ### Task W{n}-{nn}: entries, each with
  Type/Target/Section/Description/Depends/Acceptance/Risk/Wave fields

  Integration Points:
  - sc:tasklist-protocol references sc:task-unified heavily (12+ mentions for patch execution,
  compliance tiers)
  - sc:cli-portify-protocol references it as the subprocess prompt pattern
  - sc:roadmap-protocol shows the pipeline position chain ending at sc:task-unified

  Key Constraint: 416 files match sc:task — but most are in .dev/releases/complete/ (historical
  output files). Only ~15-20 are live source files that need updating.