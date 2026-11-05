reviewer: analyzer
model: sonnet
verdict: refactor
findings:
  - id: R1-F1
    severity: IMPORTANT
    class: plan-defect
    claim: "Task 12's repo-wide memory-name search fails at Task 12 on many more files than T1's two hits. The pattern includes tool-part tokens (think_about_, summarize_changes, get_current_config, prepare_for_new_conversation, check_onboarding_performed, activate_project). Task 13 owns those tokens, so the rg cannot print nothing at Task 12. T1's proposed fix (exclude the rubric file, reword the contract.py comment) is too narrow."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:172", "src/superclaude/skills/sc-reflect-protocol/SKILL.md:5", "src/superclaude/skills/sc-reflect-protocol/SKILL.md:147", "src/superclaude/skills/sc-reflect-protocol/SKILL.md:550", "src/superclaude/commands/reflect.md:169", "src/superclaude/commands/reflect.md:171", "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127", "src/superclaude/cli/reflect/contract.py:30"]
    grounded: true
    fix: "Task 12: scope the repo-wide rg to exclude the files whose tool parts Task 13 owns. Those are the sc-reflect-protocol directory, the three reflect command copies, and contract.py (or Task 7 rewords that comment). Alternatively, restrict the Task 12 rg to memory-only tokens and run the full pattern repo-wide in Task 13 or 15. Task 7 should also remove get_current_config from the contract.py:28-31 comment and check for it."
  - id: R1-F2
    severity: IMPORTANT
    class: plan-defect
    claim: "Task 10's third acceptance command (rg 'mcp-servers:.*serena' across src/superclaude, plugins, commands and agents) fails at Task 10. Task 10 edits only the T9 rows, but single-line `mcp-servers: [..., serena]` frontmatter also sits in files owned by Tasks 11-15."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:145", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:150", "src/superclaude/commands/troubleshoot.md:6", "src/superclaude/commands/validate-roadmap.md:7", "src/superclaude/commands/auggie-review.md:6", "src/superclaude/commands/save.md:6", "src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:15", "src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:6", "commands/sc-brainstorm.md:6"]
    grounded: true
    fix: "Task 10: say explicitly that it drops `serena` from the `mcp-servers:` line of every file, listing the non-T9 ones (G5 says these lists carry no coupling). Otherwise scope the rg to the T9 row files and run the repo-wide form in Task 15."
  - id: R1-F3
    severity: IMPORTANT
    class: plan-defect
    claim: "Task 4 says the new remover replaces `_cleanup_user_native_registration`, but that function is still called by `uninstall_codebase_memory_mcp` (kept until Task 5), which the tavily tests at about :888-1050 exercise; Task 4's acceptance runs the whole tavily file, so removing it in Task 4 breaks that acceptance."
    evidence: ["src/superclaude/cli/install_mcp.py:916", "src/superclaude/cli/install_mcp.py:993", "src/superclaude/cli/install_mcp.py:999", "tests/cli/test_install_mcp_tavily.py:888", "tests/cli/test_install_mcp_tavily.py:1050"]
    grounded: true
    fix: "Task 4: add `_remove_exact_user_entry` alongside the old function and do not delete `_cleanup_user_native_registration`. Task 5 deletes it together with `uninstall_codebase_memory_mcp` (row C2). Add that deletion to Task 5's rg pattern."
  - id: R1-F4
    severity: IMPORTANT
    class: plan-defect
    claim: "Task 18's sandbox fresh/existing checks require `rg -i 'serena|codebase-memory' <HOME>` to print nothing, but the installed copies keep allowlisted text (the `/sc:load` `.serena/memories` read-only sentence, the `.serena/` ignore line in cleanup-audit, the ccsession-tag install.sh comment); the sandbox rg has no allowlist, so it cannot pass."
    evidence: ["src/superclaude/skills/ccsession-tag/install.sh:41", "src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:57", "src/superclaude/commands/load.md:27", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:156", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:247", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:248"]
    grounded: true
    fix: "Task 18: apply the same allowlist to the sandbox rg (exclude `skills/ccsession-tag/install.sh`, `commands/sc/load.md`, the `.serena/` ignore line of the cleanup-audit skill), and exclude `claude-calls.log` from the fresh-HOME search."
  - id: R1-F5
    severity: IMPORTANT
    class: plan-defect
    claim: "Task 18's sandbox commands set only HOME and omit CLAUDE_CONFIG_DIR; `read_user_mcp_entry` reads CLAUDE_CONFIG_DIR first and the stub's jq edit targets `${CLAUDE_CONFIG_DIR:-$HOME}`, so an executor environment that sets it would read and mutate the real user config."
    evidence: ["src/superclaude/cli/install_mcp.py:731", "src/superclaude/cli/install_mcp.py:735", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:268", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:247"]
    grounded: true
    fix: "Task 18: add CLAUDE_CONFIG_DIR=$T/fresh, $T/old and $T/ci to every `env` invocation, including the ./update.sh run and the Tier K repeat."
  - id: R1-F6
    severity: IMPORTANT
    class: plan-defect
    claim: "Task 13 deletes reflection-rubric.md lines 124-127, but line 128 (`find_implementations`) and line 130 (`type_hierarchy`) still match the SER pattern, and Task 13's own acceptance runs `acceptance-search.sh serena` over the whole sc-reflect-protocol directory; line 130 is in no row."
    evidence: ["src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:127", "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:128", "src/superclaude/skills/sc-reflect-protocol/refs/reflection-rubric.md:130", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:179", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md:235"]
    grounded: true
    fix: "Task 13: widen the rubric target to lines 124-130; delete 124-127 and reword 128 and 130 so no SER token remains."
  - id: R1-F7
    severity: MINOR
    class: plan-defect
    claim: "Task 8's real.yaml comment list misses line 721 (`Edit|Write|mcp__serena__*`), so Task 8's own rg over src/superclaude/cli/eval would fail."
    evidence: ["src/superclaude/cli/eval/suites/real.yaml:721", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:121"]
    grounded: true
    fix: "Task 8: add real.yaml:721 to the comments to reword."
  - id: R1-F8
    severity: MINOR
    class: plan-defect
    claim: "Task 12 `git mv`s into docs/memory/reflect/, which does not exist, and Tasks 1 and 18 tee into $PKG/artifacts/baseline/ and final/ without creating them."
    evidence: [".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:167", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:37", "docs/memory/README.md"]
    grounded: true
    fix: "Add `mkdir -p docs/memory/reflect` (Task 12), `mkdir -p $PKG/artifacts/baseline` (Task 1), `mkdir -p $PKG/artifacts/final` (Task 18)."
  - id: R1-F9
    severity: MINOR
    class: plan-defect
    claim: "Task 12 edits reflect refs, SKILL.md and commands but runs no tests/cli/reflect; tests/cli/reflect/test_remediation_route_table.py reads remediation-handoff.md directly."
    evidence: ["tests/cli/reflect/test_remediation_route_table.py:13", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:170"]
    grounded: true
    fix: "Task 12 acceptance: add `tests/cli/reflect` to the pytest list."
  - id: R1-F10
    severity: MINOR
    class: plan-defect
    claim: "The slots ledger and Phase 2 handoff notes live under untracked .dev/codegraph-migration/ and the plan stages only .dev/tasks, so they are never committed; Task 5's rg does not pin the 'Codebase Memory' help text at main.py:292/313."
    evidence: ["src/superclaude/cli/main.py:292", "src/superclaude/cli/main.py:313", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:21", ".dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md:91"]
    grounded: false
    fix: "Tasks 13 and 19: also `git add` the ledger and handoff files, or state they stay untracked; Task 5: add `rg -i 'codebase.memory'` over main.py and install_mcp.py to its acceptance."
plan_line_remap: "plan-file line refs shifted by -33 (reviewer counted brief lines; brief embeds the plan from line 34)"
self_confidence: 0.8
self_audit: "Refutes T1 R-2: install_mcp.py:1319's 'Unknown MCP server selection' message is generic and survives Task 5. Unfinished checks (marked): Task 2 port fixtures, exact S58-S82 fixture count, ccsession-tag install path, git index (R1-F10 grounded: false)."
calibrated_C: 0.75
