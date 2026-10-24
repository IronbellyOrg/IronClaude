# Research: retired `/sc:select-tool`

- **Topic type:** Command retirement and recommendation eligibility
- **Scope:** Six-month history, surviving installed command, recommendation discovery, cache validation, plugin consequences
- **Status:** Complete, static inspection only
- **Date:** 2026-10-24
- **Persistence:** Report returned directly because worker instructions prohibit writing report Markdown files. Intended destination: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/select-tool.md`.

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/select-tool.txt`, worker `a855aed9315871d8c`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The exact command has two changes in the research window. Commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, only adds blank lines around headings, lists and code fences. Its patch contains no semantic change. Commit `3ae238b178fb7c67ca02809d24745de620c2bd50`, dated 2026-09-30, deletes the entire 98-line command. The latter commit explicitly describes removing unused commands, including select-tool. Evidence: inspected exact-path `git log --follow` and both patches for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/select-tool.md`.

[CODE-VERIFIED] This is a retirement, not a rename or migration to a delegated skill in the inspected patch. The former command contains no Activation section. Its surviving installed copy retains the same substantive contract as the deleted text. [S1:19-58]

### Current command contract

[CODE-VERIFIED] There is no current source command to recommend. However, `/config/.claude/commands/sc/select-tool.md` still exists in this environment. Its presence is direct evidence of a stale installed artifact, not evidence that the current distribution supports the command. [S1:1-22]

[CODE-VERIFIED] Historically, its input was an operation description, with optional `--analyze` and `--explain`. It described selecting between Serena and Morphllm using operation type, scope, complexity and performance requirements. Examples included cross-file renaming, bulk pattern replacement and saving project context. [S1:19-83]

[CODE-VERIFIED] Historically, the output was a tool-selection explanation with confidence claims. There was no output-file contract, ledger, resume mechanism, delegated protocol, or documented authorization flow for subsequent edits. The text claimed automatic integration with editing commands, but that statement alone does not establish an executable integration. [S1:25-58]

[UNVERIFIED] The historical promises of sub-100ms selection and greater than 95% accuracy are unsupported by execution evidence in this investigation. They must not become current recommendation claims. [S1:86-98]

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide currently contains no select-tool route. Its routing table already distinguishes questions, small changes, planned implementation, diagnostics and memory-related resume limitations without needing this retired command. [S2:301-325]

[CODE-VERIFIED] The actual recommend activation target is `sc-recommend`, not `sc-recommend-protocol`. The command requires that skill before executing its recommendation procedure. [S3:52-58]

[CODE-VERIFIED] Nevertheless, current discovery can admit the installed obsolete command. Phase 0 enumerates installed commands on every invocation, including inside an IronClaude checkout. Checkout precedence only addresses names found in several places. With the source select-tool file deleted, there is no source copy competing with the installed copy. Step C accepts a candidate after reading the path recorded during enumeration; its ghost rule addresses missing files, not files belonging to retired distribution entries. [S4:96-135]

[CODE-VERIFIED] The same union-of-surfaces and duplicate-only precedence rules appear in both the source enumeration reference and its plugin counterpart. Therefore, this is a recommendation-source eligibility problem, not simply an outdated guide row. [S5:13-25; S6:13-25]

[CODE-VERIFIED] Cache behavior does not fully close that gap. Surface hashing includes source, installed and project command paths plus guide content. Deleting the source command changes that fingerprint and discards old rows. However, after a cold-path recommendation is generated from the surviving installed file, a newly cached row can validate against that file. Dispatch checks existence and byte hash before emitting the envelope; it does not establish current distribution membership. [S7:63-94,118-140; S8:103-137]

[CODE-VERIFIED] Matched guide routes bypass the recommendation cache. Consequently, the retirement guard must protect live enumeration and cold-path verification as well as cached hits. A cache-only fix leaves the installed-file discovery path open. [S4:58-65,128-135,300-304]

[CODE-VERIFIED] The hook is not a mechanical retirement guard. Its own header says it is fail-open and does not block invocation. Its legacy protocol-name match is explicitly transitional compatibility. The command's stronger claim that the gate cannot be silently skipped should not be treated as runtime proof. [S9:2-19,31-35; S3:60]

### Proposed recommendation changes

[UNVERIFIED] **MUST: make current framework membership distinct from file existence.** Extend Phase 0 Step A/Step C and the enumeration references so a verified retired framework command is not resurrected solely by an installed or project mirror. In this checkout, select-tool's removal is authoritative evidence. Preserve independently authored commands and third-party extensions; do not equate every installed-only name with retirement. Use shared provenance/current-distribution evidence rather than another keyword-to-command routing table. Grounding: the current guard accepts any resolving recorded path. [S4:104-135]

[UNVERIFIED] **MUST: apply the same eligibility decision before cold cache insertion and hot emission.** An unchanged stale installed file must not satisfy current-support validation merely because its hash matches. Keep existing deletion and source-byte invalidation protections. Grounding: current dispatch's final validation is file existence plus hash. [S7:73-94; S8:116-137]

[UNVERIFIED] **SHOULD: preserve intent when rejecting the retired command.** A request merely asking which editing tool fits an operation should receive a grounded explanation or native-tool recommendation, not automatic implementation. A request to perform a multi-file rename should use the current planning route. Under the user's desired new policy, most planned work should use workflow plus implement; reserve MDTM for the most complex, long-running work. This is a proposed policy change, not today's guide rule: the current guide still routes “many files” and “more than one session” to task-builder. [S2:303-307; S4:154-157]

[CODE-VERIFIED] A supported planning example, without copying retired flags, is:

```text
/sc:workflow "Plan the requested cross-file rename, preserving behavior and adding regression coverage." --depth standard
```

Then read the returned plan and invoke `/sc:implement` with that returned path. `--depth standard` is supported and is the workflow default; the command creates a plan and does not mutate product code. This example requires corresponding guide-policy alignment before becoming the new default recommendation. [S10:18-40,63-80]

[UNVERIFIED] **SHOULD: mirror the eligibility wording into the plugin enumeration reference and condensed cold-path runbook.** Otherwise one recommendation path can continue using existence-only verification after the main skill is corrected. No select-tool routing row or replacement skill is needed. [S6:13-25; S11:132-148]

### Acceptance/regression scenarios

[UNVERIFIED] Add these scenarios alongside the existing routing and cache tests:

1. Current source omits select-tool, but an installed legacy file remains: cold discovery must not recommend it.
2. A cache row names select-tool and hashes that surviving installed file correctly: current-support validation must still reject it.
3. Source command deletion changes the surface fingerprint and removes previous rows; preserve existing invalidation behavior.
4. A genuinely custom installed-only command remains eligible when it is not a retired framework artifact.
5. “Explain whether semantic or pattern editing fits this operation; change nothing” stays report-only.
6. “Perform this ordinary multi-file rename” selects workflow plus implement under the revised policy, not MDTM merely because several files are involved.

Existing inspected tests cover source-hash drift, surface resets, installed-path additions and guide changes, but not a retired command surviving in another discovery surface. No tests were executed during this research. [S12:45-115; S13:62-77,149-201]

## Gaps

[CODE-VERIFIED] Literal search across current source, plugins and tests found no select-tool references. The only `sc-recommend-protocol` hits were hook compatibility references. The tracked protocol directory is absent, while `/config/.claude/skills/sc-recommend-protocol/SKILL.md` exists and describes legacy keyword mapping and obsolete flags. The current command does not activate it. [S3:54-58; S9:15-19; S14:11-44]

[UNVERIFIED] No end-to-end recommendation was run, so the stale installed command's actual selection frequency is unknown. The admission path is established by source-contract inspection, not observed output.

[UNVERIFIED] Retirement/provenance behavior outside a checkout needs a shared design decision. Do not silently reject legitimate extensions or claim that installed artifact cleanup already occurs.

## Key Takeaways

[CODE-VERIFIED] **CHANGE:** retirement is correctly reflected in current source and guide, but installed-file enumeration can undermine it. File readability does not prove current support. [S2:301-325; S4:104-135]

[UNVERIFIED] **MUST:** prevent retired framework artifacts from passing discovery and cache eligibility. **SHOULD:** retain user intent, synchronize plugin/cold-path rules, and add cross-surface retirement scenarios. **NONE:** recreate select-tool, restore its flags, add a tool-selection keyword table, or repeat its unsupported accuracy claims.

### Evidence paths

- **S1:** `/config/.claude/commands/sc/select-tool.md`
- **S2:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **S3:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/recommend.md`
- **S4:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **S5:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md`
- **S6:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/surface-enumeration.md`
- **S7:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py`
- **S8:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py`
- **S9:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh`
- **S10:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md`
- **S11:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **S12:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/recommend/test_dispatch.py`
- **S13:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/recommend/test_cache.py`
- **S14:** `/config/.claude/skills/sc-recommend-protocol/SKILL.md`
