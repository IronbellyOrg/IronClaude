# Research: /sc:roadmap recommendation accuracy

- **Topic type:** Command-history and routing-contract research
- **Scope:** `/sc:roadmap`, its delegated protocol, recommendation guide, classifier, cache, plugin consequences, and regression coverage
- **Status:** Complete source analysis; no implementation or runtime execution
- **Date:** 2026-10-24
- **Intended report destination:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/analyses/roadmap.md`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/roadmap.txt`, worker `ad191c98563a7dfb9`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Two commits changed the exact command during the specified six-month window. Commit `d9901d870b779ab10fa9ecee4f79a35f6cd58a60`, dated 2026-05-26, substantially replaced its inference-oriented interface with the CLI-facing contract: one to three positional Markdown inputs, source enrichment, gate-based resume, dry-run, convergence, compression, and cosmetic-remediation controls. It explicitly retired `--specs`, `--template`, `--multi-roadmap`, `--interactive`, `--compliance`, and `--persona`. This was semantic change, not formatting. Commit `70ef6486ef878975fc61569292c340c6a79fccd9`, dated 2026-05-30, changed the default agent pairing and example from Haiku to Sonnet, also semantic rather than formatting. Evidence: exact-path `git log` and both patches; current contract at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/roadmap.md:19-48`.

[CODE-VERIFIED] Delegated-protocol history continued after those command changes. The October 22 commits `5c6a7d91` and `3fcb5417` changed prerequisite lookup from source-checkout paths to installed and project copies; they did not reconcile the old flag grammar. The live prerequisite still checks legacy `--specs` and `--multi-roadmap` modes. Evidence: exact protocol patches and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:176-185`.

### Current command contract

[CODE-VERIFIED] The command accepts one to three Markdown inputs in any order, at most one each of specification, TDD, and PRD. Default output is the first input’s parent directory, unless `--output` is supplied. Default depth is `standard`; default agents are `opus:architect,sonnet:architect`. Useful controls include `--resume`, `--dry-run`, `--tdd-file`, `--prd-file`, and `--strict-no-remediation`. These are documented contracts, not evidence that an invocation was executed successfully. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/roadmap.md:19-44`.

[CODE-VERIFIED] It generates roadmap-pipeline artifacts, not implementation or tasklists. Source specification, TDD, and PRD files must remain unchanged. Downstream commands are not triggered automatically. It must hand all arguments to `Skill sc:roadmap-protocol`; the directory containing that skill is named `sc-roadmap-protocol`, while its frontmatter name uses the colon. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/roadmap.md:78-104` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:1-5`.

[CODE-CONTRADICTED] Reading only the command does not establish a consistent end-to-end contract. Its mandatory target still advertises comma-separated specifications, template selection, interactive operation, a release-directory default, and `--resume-from`; its dry-run describes executing analysis waves rather than merely printing the pipeline step plan. This directly affects recommendation accuracy because a verified outer command can delegate into contradictory instructions. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/roadmap.md:19-48,84-98` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:54-82`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide distinguishes `/roadmap` from `/sc:roadmap`, but says to use `/roadmap` unless a lead says otherwise. Its full-specification route always proceeds through `/roadmap` and phase MDTM execution. There is no dedicated `/sc:roadmap` row in the machine-readable routing table, nor a direct entry for it in “Other commands.” Consequently, artifact-only pipeline requests receive weaker discovery support than the MDTM composer. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:245,264-289,303-325`; the command’s narrower output boundary is `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/roadmap.md:96-104`.

[CODE-VERIFIED] Recommendation reads the guide before classification. A matched row bypasses both cache paths and semantic ranking; the row decides the answer. Therefore, classifier improvements alone cannot fix an overbroad guide match. Source-checkout copies take precedence inside this worktree; outside a checkout, candidate precedence is project, installed, then plugin. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:39-61,112-116,148-155`.

[CODE-VERIFIED] For unmatched requests, the classifier defines `roadmap-generation` exclusively as “phased roadmap plus phase task files” through `/roadmap`. Its example, “Generate a roadmap from this TDD,” carries no artifact-only distinction. This is a false-positive risk for `/sc:roadmap` requests, not measured classifier failure. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:58-62,78-82`.

[CODE-VERIFIED] Cache dispatch selects one row by classification key, verifies only that row’s source bytes, and returns its envelope. Surface hashing includes path membership and guide content, not every protocol/ref’s content. Thus one roadmap key must not silently serve incompatible artifact contracts; a protocol-only correction is also not guaranteed to invalidate a command-backed row. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:103-136` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/cache.py:63-103`.

[CODE-VERIFIED] The plugin guide reproduces the same `/roadmap` preference. The Phase-0 hook is explicitly advisory and fail-open, so it cannot mechanically guarantee that artifact distinctions or fresh verification occur. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:243-245` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/hooks/scripts/sc-recommend-phase0.sh:4-13`.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed policy:** Update the governing guide’s process boundary and section 5 distinction. Most planned implementation should use `/sc:workflow` followed by `/sc:implement`; file count, existing specifications, multiple sessions, auditability, and resume are not sufficient MDTM triggers. Preserve `/sc:roadmap` for requested release-pipeline artifacts and `/roadmap` for explicitly wanted MDTM roadmap/task packages. This changes current policy rather than describing current behavior. Targets: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:243-245,305-309`.

[UNVERIFIED] **MUST, proposed routing condition:** In that guide, express artifact intent explicitly: generating roadmap-pipeline artifacts from supplied documents should select `/sc:roadmap` and stop after the requested deliverable. Do not append tasklist generation, Sprint execution, or implementation without a request. Use the existing guide mechanism, not another keyword routing table. Illustrative paste-ready envelope, assuming these are user-supplied inputs: `/sc:roadmap <spec.md> <tdd.md> <prd.md> --output <requested-output-directory> --dry-run`. Supported grammar: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/roadmap.md:19-44,59-69,98`.

[UNVERIFIED] **MUST, proposed verification rule:** Extend candidate verification to inspect the actual activation target for material input/output contradictions. Report this roadmap mismatch rather than importing retired flags into recommendations or claiming verified parity. Command/protocol alignment is a directly relevant dependency, not permission for general roadmap implementation work. Targets: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:128-135` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-roadmap-protocol/SKILL.md:54-82`.

[UNVERIFIED] **SHOULD:** Correct classifier examples and prevent a shared cached roadmap classification from overriding output intent. Where existing cache semantics cannot distinguish the requests, bypass reuse and perform live verification. Mirror the guide and recommendation-reference changes in the plugin package. Evidence motivating these changes: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:58-82` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py:103-136`.

### Acceptance/regression scenarios

[UNVERIFIED] Add behavioral cases beside the existing textual routing tests at `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/skills/test_sc_recommend_routing_contract.py:35-80`:

1. Artifact-only spec/TDD/PRD request selects `/sc:roadmap`, with positional inputs and no automatic execution.
2. Ordinary planned implementation selects workflow/implement despite many files or several sessions.
3. Explicit MDTM roadmap/task-package request preserves `/roadmap`; an existing MDTM task remains `/task`.
4. Gate-based resume retains `/sc:roadmap ... --resume`, never substitutes `--resume-from`.
5. A warm `/roadmap` cache entry cannot answer an incompatible artifact-only request.
6. Command/protocol disagreement is surfaced; retired flags are never emitted as supported.

## Gaps

[CODE-VERIFIED] Targeted searches found no `/sc:roadmap`-specific recommendation scenario in the inspected recommendation, core-routing, or skill-routing tests. Existing tests primarily pin text, markers, source existence, and generic cache behavior; they do not establish semantic routing accuracy.

[UNVERIFIED] No roadmap or recommendation workflow was executed. Actual slash-command behavior under the contradictory protocol remains unresolved. Runtime capacity claims and automatic convergence guarantees are intentionally not inferred from prose.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Separate requested artifacts from execution-system selection, implement the user’s workflow-first policy in the governing guide, and expose the roadmap command/protocol mismatch.

[UNVERIFIED] **SHOULD:** Add roadmap-specific cold/warm recommendation regressions and keep plugin mirrors aligned.

[UNVERIFIED] **NONE:** No new fixed keyword table, automatic downstream execution, source edits, or general roadmap refactor is warranted by this research.
