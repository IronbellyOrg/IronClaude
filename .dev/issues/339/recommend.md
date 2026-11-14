# /sc:recommend output for #339

- Recorded: 2026-11-07T11:55:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/339. Type: feature. Complexity: complex. Summary: .dev/issues/339/issue-summary.md. Suggested route (default row "Feature, complex" of the /sc:issue chains): /model claude-gw-tier1a; 1. /sc:brainstorm "Orchestrator mode: run and manage all sessions within a worktree @.dev/issues/339/issue-summary.md" --depth deep --research deep --codebase --blind; 2. /sc:design <merged-requirements.md> --type <architecture|api|component|database> --format spec; 3. /sc:workflow <design doc> --depth deep --handoff none; 4. /sc:implement <plan path>

The block below is the skill's output, copied verbatim.

````text
guide_status: matched (src/superclaude/core/HOW-WE-WORK.md, checkout copy read first)
routing rows: shape-idea (step 1, guide section 3.1), focused-design (step 2, section 3.13), feature-existing (steps 3-4, level 3, section 3.2)
auggie_status: skipped (matched mode)

Ordered workflow (level 3: checked implementation plan; changes files: yes)

/model claude-gw-tier1a

1. /sc:brainstorm "Orchestrator mode: run and manage all sessions within a worktree @.dev/issues/339/issue-summary.md" --depth deep --research deep --codebase --blind
   - Why: the requirements are not yet clear (accuracy check out_of_date; open questions in comment 3), so the spec is shaped first.
   - Verified options (src/superclaude/commands/brainstorm.md:34-62): --depth quick|standard|deep, --research light|deep|none, --codebase, --blind, --output DIR (default .dev/brainstorms/<ts>-<slug>/).
2. /sc:design <brainstorm folder>/merged-requirements.md --type architecture --format spec --output docs/designs/orchestrator-mode.md
   - Verified options (src/superclaude/commands/design.md:22-26): --type, --format, and a file-valued --output (a standalone run writes a file only when --output is passed).
3. /sc:workflow docs/designs/orchestrator-mode.md --depth standard --handoff none
   - Read the printed plan path and the advisory check result. standard is the guide default; deep is optional.
4. Only when execution is requested: /sc:implement <printed plan path>

Notes:
- Optional requirements review between steps 1 and 2: /sc:spec-panel @<merged-requirements.md> --mode critique --focus requirements,architecture (row critique-spec; --mode and --focus declared at src/superclaude/commands/spec-panel.md:22).
- Level 4 (/task-builder then /task, MDTM task files) needs explicit selection or the exceptional machinery need; nothing in the issue alone selects it. An explicit owner selection of /task-builder and /task is preserved; pass --spec <design path> to /task-builder.
- Shipping: /sc:pr-submit --monitor 3 only under requested full-loop authority (row review-pr, branch 6d).
````
