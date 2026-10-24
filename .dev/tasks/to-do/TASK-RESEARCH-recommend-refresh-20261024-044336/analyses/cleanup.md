# Research: /sc:cleanup

- **Topic type:** Command and recommendation-contract comparison
- **Scope:** Six-month history ending 2026-10-24; current cleanup contract; recommendation routing, cache, plugin and test consequences
- **Status:** Research complete; returned inline because worker instructions prohibit writing report files
- **Date:** 2026-10-24

## Evidence index

All numbered references below identify these absolute paths and their live line numbers.

- **C:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/cleanup.md`
- **G:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **R:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **P:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **T:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py`
- **PC:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/cleanup.md`
- **PG:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
- **PT:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py`
- **H:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh`
- **CA:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/cleanup-audit.md`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/cleanup.txt`, worker `a2bbecf72de98c08d`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-command git history contains three changes within the inventory window:

1. `89df2c1105c01caff199288f949d5783f6594e70`, 2026-05-22: formatting only. Added blank lines around headings, lists and fences, plus a final newline. No routing or capability change.
2. `3ae238b178fb7c67ca02809d24745de620c2bd50`, 2026-09-30: substantive dependency-contract change. Removed Sequential from `mcp-servers` and replaced Sequential-based analysis with native reasoning. Context7 remained.
3. `046a03ab41ac98c39a11d940794c6e96cfab6ceb`, 2026-10-03: removed the remaining example comment promising Sequential analysis.

Evidence: read-only `git log -p` for C; the resulting current contract appears at C:6,33-44,86-91. None of these patches added a planning pipeline, protocol-skill activation or new flags.

### Current command contract

[CODE-VERIFIED] Cleanup is a self-contained, mutating command. Its usage accepts an optional target, `--type code|imports|files|all`, `--safe|--aggressive`, and `--interactive`. It describes analysis, planning, execution, validation and a cleanup-summary report. It has no `## Activation` delegation, structured return contract, checkpoint or resume interface. Omitted-target scope and option defaults are not explicitly defined. Evidence: C:19-31,46-58,93-127.

[CODE-VERIFIED] Authorization is narrower than “interactive means approve every edit.” Unused imports, zero-reference dead code, empty blocks and redundant annotations apply automatically. Indirect references, potentially external exports, test fixtures/utilities and configuration values require approval; any usage path, public-API effect or uncertainty prompts the user. Evidence: C:107-127. Recommendations must disclose mutation and must not promise a fully approval-gated dry run.

[UNVERIFIED] Backup/rollback and intelligent detection are documentation promises, not demonstrated runtime mechanisms in this analysis. The command asserts them but supplies no concrete rollback interface. Evidence: C:38,95-105.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide correctly distinguishes audit from cleanup and accurately warns about automatic changes. However, its machine-read `cleanup` row mandates a five-step chain: audit, commit, cleanup, improve, diff review. The recommendation skill must emit every matched-row step and cannot replace the route with a lighter command. Consequently, a narrow import-cleanup request receives an additional quality-improvement operation it did not necessarily request. Evidence on both sides: C:14-17,55-58; G:157-168,248,318; R:150,236.

[CODE-CONTRADICTED] Valid cleanup safety flags are vulnerable to rejection by the recommendation contract. Cleanup documents them in its Usage syntax, not a flag table or `argument-hint`. Recommendation requires those particular locations and explicitly drops mandatory guide flags absent from them. The guide nevertheless mandates `--type code --safe --interactive`. This is a textual contract contradiction, not a demonstrated execution failure. Evidence on both sides: C:19-23; G:318; R:237,335-337.

[CODE-VERIFIED] Current policy sends large or structural refactors to the feature-existing MDTM path. The same boundary appears in recommendation’s fallback prose and the cold-worker runbook: level 3 for a few clear files, level 4 for anything larger, longer or riskier. This differs from the user’s desired new policy. Evidence: G:168,305-307,318; R:155-157; P:160-168. File count, multiple sessions, an existing spec or auditability alone must cease being sufficient MDTM triggers.

[CODE-VERIFIED] A matched cleanup row bypasses both cache lookup and cold-path write-back. Fixing classifier wording alone therefore cannot repair its ordered workflow. For unmatched requests, the classifier’s `cleanup-audit` description combines repository cleanup, dead-code and sprawl audit concepts, so evaluation should distinguish inspection from authorized removal rather than infer execution from “cleanup.” Evidence: R:58-67; P:55-67.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Revise G section 3.7 and its existing `cleanup` row to separate three intents without adding another independent keyword-routing table:

- Report-only investigation: preserve `/sc:cleanup-audit` and stop after reporting.
- Authorized contained cleanup: preserve the commit/checkpoint prerequisite and final diff review; recommend cleanup without automatically adding improve.
- Planned structural refactoring: default to workflow plus implement; reserve MDTM for the most complex, long-running work or explicit MDTM inputs.

These are desired routing changes, grounded in the current boundaries at G:157-168,318 and CA:95-99, not claims that the source already behaves this way.

[UNVERIFIED] **MUST, proposed policy:** Allow flags verified in a command’s formal Usage grammar when no flag table or argument hint exists. Apply the same rule in R’s ordered-output/R1 sections and P’s cold-worker R1. Do not accept example-only flags indiscriminately. Cleanup’s `--preview` appears only in an example and conflicts with its formal interface; exclude it pending clarification. Evidence: C:22,70-75; R:237,335-337; P:200-202.

[UNVERIFIED] **MUST, proposed policy:** Align R:155-157 and P:160-168 with the new workflow-first boundary. Preserve the contained folder-cleanup exception, but do not let the word “folder” exempt arbitrary architectural migrations from planning.

[CODE-VERIFIED] Grounded cleanup handoff example, after the prerequisite checkpoint is separately authorized:

`/sc:cleanup <folder> --type code --safe --interactive`

Its safety flags come from C:22 and the existing guide example G:164. Output must identify that files change and explain automatic versus approval-required classes, without reproducing the command’s entire procedure.

[CODE-VERIFIED] Grounded planned-refactor handoff shape:

`/sc:workflow "<refactor goal, constraints and affected code>" --depth standard`

Then read the printed plan and invoke `/sc:implement <printed-plan-path>`. Workflow accepts inline prompts and this depth; no invented cleanup-to-plan flag is needed. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md`:20,35-40,78-80.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed regression cases:

1. “Audit unused code; change nothing”: audit-only output, no cleanup/improve/commit steps.
2. “Remove unused imports in this folder”: disclose mutation, preserve safety/checkpoint/diff steps, do not append unrelated improvement.
3. “Refactor this subsystem across many files with a spec”: workflow/implement by default, not MDTM solely because of breadth or spec presence.
4. Explicit MDTM task execution remains `/task`.
5. Formal cleanup safety flags survive verification; example-only `--preview` does not.
6. `--interactive` never becomes “every change needs approval.”
7. Matched-row and no-guide/cold-path answers share the new policy.

[CODE-VERIFIED] Existing table tests check that mandatory flag strings occur somewhere in command text, not that recommendation’s stricter flag-location rule accepts them. They do not prove these semantic cases. Evidence: T:286-304. Tests were read, not executed.

## Gaps

[CODE-VERIFIED] Tracked-file inspection found no cleanup protocol skill and no tracked legacy `sc-recommend-protocol` directory. Cleanup runs from C; recommendation activates the newer skill. An installed legacy protocol nevertheless exists at `/config/.claude/skills/sc-recommend-protocol/SKILL.md`:11-16,29-44 and still carries old flags and keyword mapping. It is not authoritative for this analysis.

[CODE-VERIFIED] Plugin cleanup retains the deleted Sequential example comment at PC:91. Treat this as a stale capability-description follow-up, not justification for changing cleanup routing. Recommendation plugin guide changes must mirror G; parity requirements are explicit at PT:27-36.

[CODE-VERIFIED] The hook is reminder-only and fail-open, not mechanical routing enforcement: H:4-13,85. No runtime recommendation run was performed.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Make cleanup recommendations intent-specific, repair Usage-only flag verification, and move ordinary planned refactors to workflow/implement across guide and fallback prose.

[UNVERIFIED] **SHOULD:** Add semantic regression cases and keep plugin documentation aligned.

[CODE-VERIFIED] **NONE:** No new cleanup capability or mandatory dependency is justified by the history. Sequential was removed; the formatting patch introduced no semantic delta.
