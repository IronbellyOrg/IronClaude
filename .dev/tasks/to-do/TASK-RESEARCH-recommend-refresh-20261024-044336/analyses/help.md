# Research: /sc:help recommendation alignment

- **Topic type:** Command-history and routing-contract research.
- **Scope:** Six-month command history, current help contract, recommendation routing, plugin parity, hooks, cache, and existing tests.
- **Status:** Complete, source inspection only. No commands executed, files changed, or tests run.
- **Date:** 2026-10-24.
- **Delivery:** Returned directly because developer instructions prohibit writing report Markdown files.

## Evidence key

All paths resolve within the assigned worktree.

- **H:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/help.md`
- **G:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **R:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **P:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **C:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py`
- **K:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh`
- **T:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_help_command.py`
- **PT:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py`
- **PG:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
- **PH:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/help.md`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/help.txt`, worker `a7eda596586b96c03`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-path Git patches for H show seven changes in the requested window:

| Commit | Date | Observed change |
|---|---|---|
| `89df2c11` | 2026-05-22 | Formatting only: added blank lines around headings and lists. No semantic change. |
| `3ae238b1` | 2026-09-30 | Removed retired command entries and obsolete MCP flags from the former static reference. |
| `046a03ab` | 2026-10-03 | Removed remaining Sequential activation claims from analysis-depth descriptions. |
| `051f39fe` | 2026-10-14 | Substantive rewrite: replaced the static command/flag reference with live installed inventories, routing-guide extraction, built-in descriptions, and handoff pointers. |
| `8278a84b` | 2026-10-14 | Restricted Bash access from unrestricted Bash to named read-oriented commands. |
| `1367c8c6` | 2026-10-14 | Removed `head`/`cat` permissions and tightened the instruction to run only the specified listings. |
| `070399eb` | 2026-10-23 | Changed the guide pointer from “safe flags” to “required flags”; no new help capability. |

The current replacement behavior is visible at H:19-93. Historical claims above were verified from actual patches, not inferred from commit subjects.

### Current command contract

[CODE-VERIFIED] Help is a self-contained command, not a protocol-skill dispatcher. Its inputs are the invocation and local installation context; it defines no argument syntax, flag table, task artifact, or resume workflow. Existing tests explicitly require absence of `## Activation` (H:13-21,95-119; T:44-48).

[CODE-VERIFIED] Its useful capabilities are broader than “list `/sc:` commands”: it lists installed commands, installed skills, project-local commands/skills, and plugin commands/skills where plugin context is available. It skips README entries, displays descriptions, separates protocol skills, and preserves actual command namespaces (H:23-63).

[CODE-VERIFIED] Help reads the routing guide with checkout-first precedence inside IronClaude, otherwise installed then plugin fallback. It prints the marked six-level table and hard limit verbatim. Missing guide and missing marker cases have explicit degradation messages (H:65-81).

[CODE-VERIFIED] The output ends with built-in review commands and pointers to the guide, recommend, and individual command files. Help must not edit files, execute listed commands, invent installed entries, or choose a workflow. Therefore installation checking means inspecting what exists, not performing installation or repair (H:83-93,121-135).

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide already describes help accurately under “Other commands”: installed commands and skills, six process levels, and the guide pointer. The plugin guide carries the same entry (G:273; PG:273). A blanket conclusion that recommend has no help reference would be wrong.

[CODE-VERIFIED] The recommendation skill considers “Other commands” only after **no routing row matches**. Once a row matches, it bypasses cache and cold-path discovery and verifies only the matched row’s steps. Meanwhile, the guide’s broad `ask` row includes “no changes wanted,” and `unsure` includes “which tool; how to start” (R:54-61; G:303,325).

[UNVERIFIED] This creates a plausible misrouting case: “Show my installed commands; do not change anything” can be interpreted through generic `ask`, preventing help’s more specific fallback entry from being considered. No live model-routing execution was performed, so this is a contract-level ambiguity, not a demonstrated runtime failure.

[CODE-VERIFIED] The cold-path prompt already accepts the guide’s other-command entries as candidates before enumeration. It does not need another hand-maintained help keyword table. The classifier’s closed key set has no installed-inventory category; unmatched requests may use `unknown` and proceed to cold discovery (P:28-39,50-68,125-148).

[CODE-CONTRADICTED] R:114 generalizes commands as thin skill dispatchers, but help has no activation handoff and runs directly from its own text. Candidate verification must preserve that distinction rather than inventing a help protocol (H:19-21; T:44-48).

### Proposed recommendation changes

[UNVERIFIED] **MUST: preserve installed-inventory intent separately from workflow selection.** In G’s existing governing routing table, add a specific supporting route for listing installed commands/skills or checking installation visibility. Its single step should be `/sc:help`, with `mandatory_flags: -`, `changes_files: no`, and a section explaining inventory versus choosing a workflow. Remove or qualify the corresponding “no workflow routes here” Other commands entry. This uses the existing authoritative table, not an extra fixed keyword router (G:260-273,295-303; H:13-17,130-135).

Paste-ready target:

```text
/sc:help
```

[UNVERIFIED] **SHOULD: correct activation generalization.** In R’s Phase 0 discovery description, say commands may be self-contained or skill-indirected; follow an activation target only when the verified command names one. Preserve direct command-file execution for help (R:112-114; H:19-21).

[UNVERIFIED] **MUST: propagate the user’s revised implementation policy through the shared guide, not help-specific prose.** Help deliberately prints the guide unchanged. The current `task-file` route still treats many files, multiple sessions, or avoiding drift as sufficient for MDTM. Revising recommend alone would leave help displaying contradictory policy. Update the governing level table, related explanations, and routes so workflow plus implement is the normal planned-work path; reserve task-builder plus task for the most complex, long-running workloads while retaining explicit MDTM execution (H:73,125-126; G:305-308; PG:305-308). This is desired policy, not current behavior or a measured capacity claim.

[CODE-VERIFIED] Plugin consequences are already bounded by parity requirements: the plugin skill mirrors source plus a byte-identical guide. The help command mirror currently carries the same live-listing contract. A guide-based change therefore belongs in PG as well; no duplicate help routing table is needed (PT:1-5,27-36; PH:23-93).

[CODE-VERIFIED] A guide edit changes the cache surface hash, and mismatched hashes discard stored rows. A matched installed-inventory route would bypass cache entirely under the existing skill contract. No dedicated inventory cache or classifier key is necessary for this proposal (C:63-94,118-140; R:60-67).

### Acceptance/regression scenarios

[UNVERIFIED] Add these scenarios to the routing regression coverage:

1. “List the commands and skills installed here; change nothing” recommends bare `/sc:help`, not explanation, research, planning, or recursive recommend.
2. “Did my command installation appear?” recommends read-only inventory without promising repair.
3. “Which command should implement this feature?” selects the appropriate implementation route, not help merely because it mentions commands.
4. Help is treated as self-contained, with no fabricated protocol or unsupported flags.
5. A checkout with a stale installed guide displays the checkout guide’s revised implementation policy.
6. Plugin-only and missing-guide installations preserve namespace and degradation behavior.
7. Cached old routing cannot override the revised guide; matched inventory bypasses cache.

## Gaps

[CODE-VERIFIED] Existing help tests cover live locations, no static table, marker extraction instructions, built-ins, and absence of activation. They do not exercise natural-language recommendation decisions or execute the listing workflows (T:16-62).

[CODE-VERIFIED] The hook is explicitly fail-open and injects reminders; it cannot mechanically guarantee correct help selection or source verification. Its legacy protocol-name matcher is compatibility handling, not evidence of a current help protocol (K:4-19).

[UNVERIFIED] No runtime install, plugin loading, model classification, or test execution was performed. Missing files encountered at initially assumed hook/test paths were resolved through file discovery; those misses are not product defects.

## Key Takeaways

[UNVERIFIED] **CHANGE:** make installed-inventory requests an explicit supporting route in the existing governing guide and regression-test the distinction from workflow selection.

[CODE-VERIFIED] **NO CHANGE to help’s core contract:** live read-only listing, guide extraction, direct execution, and non-execution boundaries already fit the requested role (H:121-135).

[UNVERIFIED] **MUST:** align the shared guide and plugin guide with the user’s revised planned-work policy. **SHOULD:** correct recommend’s universal dispatcher wording. **NONE:** new help flags, a help protocol, an inventory cache category, automatic installation repair, or another fixed keyword routing table.
