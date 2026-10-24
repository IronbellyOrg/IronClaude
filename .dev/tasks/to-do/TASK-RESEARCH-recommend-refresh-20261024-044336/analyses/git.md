# Research: /sc:git recommendation coverage

- **Topic type:** Command contract and recommendation alignment
- **Scope:** Six-month history ending 2026-10-24; current command, recommendation primitives, plugin copies, and routing tests
- **Status:** Research complete; proposed changes only. No files written or repository state changed.
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/git.txt`, worker `a79fd3ab84a6e6e1d`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The command qualifies for the requested inventory because commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, touched it during the research window. The exact patch adds blank lines around headings, lists, and fenced examples, plus a final newline. It introduces **no semantic change**. Read-only history inspection found no other change to this exact command in the window. Evidence: that commit’s patch for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md`.

### Current command contract

[CODE-VERIFIED] `/sc:git` is a self-contained command, not a dispatcher to a separately named protocol skill. Its syntax accepts an operation and operation arguments, with optional `--smart-commit` and `--interactive`. Triggers explicitly include status, add, commit, push, pull, branch management, and merges. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md:12-38`.

[CODE-VERIFIED] Its useful specialization is interpreting repository state, generating conventional commit messages from changes, applying branch conventions, and guiding conflict resolution. The documented examples are `/sc:git status`, `/sc:git commit --smart-commit`, and `/sc:git merge feature-branch --interactive`. These are verified documentation contracts, not proof that this research executed those operations. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md:47-76`.

[CODE-VERIFIED] Mutation depends on the selected operation. The command promises not to modify repository configuration without explicit authorization or execute destructive operations without confirmation. It excludes complex merges requiring manual intervention. It documents no durable ledger, resume token, output artifact, structured return schema, default operation, or post-operation implementation handoff. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md:19-31,79-91`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The governing guide underrepresents this command. Its “Other commands” entry describes only “Commit with a generated message,” while the command explicitly supports status interpretation, branches, and guided merges. That entry also correctly preserves push approval. This is incomplete capability coverage, not evidence that every simple Git operation should invoke a command. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:264-272` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md:12-38,54-76`.

[CODE-VERIFIED] The omission matters to discovery: the cold-path runbook explicitly uses the guide’s “Other commands” descriptions to seed candidates before enumeration and semantic ranking. A commit-only description therefore supplies less evidence for a branch or merge request, although live enumeration can still recover the command. This is a documented discovery weakness, not a demonstrated runtime misroute. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:125-148`.

[CODE-CONTRADICTED] Recommendation Rule R1 permits flags only from a target’s flag table or `argument-hint`, but `/sc:git` defines its supported options in **Usage and Examples**, without either structure. Consequently, its real `--smart-commit` and `--interactive` options do not satisfy R1’s literal permitted evidence locations. The cold-path runbook repeats the restriction. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:335-337`, `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:200-202`, and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md:19-23,64-76`.

[CODE-VERIFIED] The existing guide keeps PR submission distinct: its `review-pr` route includes local commits, reviews, approved pushing, and `/sc:pr-submit`. Broad Git support should not replace that dedicated sequence when the user actually requests PR preparation and submission. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:323`.

[CODE-VERIFIED] Existing routing tests require `/sc:git` to remain discoverable in “Other commands,” but their presence check verifies names and resolvable files, not capability completeness or successful recommendations for generated messages and interactive merges. Mandatory-flag tests inspect whether flag text exists anywhere in command source, which is broader than R1’s wording. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:275-304`.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed:** Resolve the flag-evidence contradiction in the recommendation skill, its surface-enumeration reference, and the cold-path runbook. Permit directly read, affirmative Usage syntax and Examples as supporting evidence when a command lacks a flag table or argument hint. Continue rejecting flags appearing only as forbidden examples or quoted third-party commands. This preserves verification rather than weakening it. Verified motivating sources are the R1 and command citations above.

[UNVERIFIED] **SHOULD, proposed:** Expand the guide’s existing `/sc:git` “Other commands” entry to cover intelligent status interpretation, conventional commit generation, branch guidance, and supported guided merges. Preserve native tooling for straightforward operations, push approval, destructive-operation confirmation, and the complex-merge boundary. Do not add another keyword-routing table. Target: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:272`.

[UNVERIFIED] **SHOULD, proposed:** Use these source-grounded handoffs when delegation adds value:

```text
/sc:git commit --smart-commit
```

```text
/sc:git merge feature-branch --interactive
```

The branch value must come from the user or verified repository state, not this illustrative example. Recommendation must not execute either handoff. Supported syntax: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/git.md:64-76`.

[UNVERIFIED] **SHOULD, proposed:** Carry the guide and recommendation-contract changes into the applicable plugin copies, including `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`. The existing plugin parity contract requires the recommendation skill tree to mirror source, with the guide as its additional bundled reference. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py:27-36`.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed scenarios, grounded in the contracts above:

1. **Generated commit:** A request to commit existing changes with a conventional message can recommend `--smart-commit`; the verifier accepts its affirmative Usage/Example evidence.
2. **Guided merge:** A request for interactive help merging a named branch discovers `/sc:git`, preserves `--interactive`, and does not promise automatic resolution of complex merges.
3. **Simple status:** A request only to show repository status may recommend native Bash when delegation adds no value.
4. **Authorization:** A recommendation to inspect status never silently becomes commit, push, configuration changes, or destructive recovery.
5. **PR request:** PR preparation retains the dedicated review/submission route rather than stopping at `/sc:git`.
6. **Implementation boundary:** Committing already completed changes across many files does not become an implementation-planning request merely because many files are present.
7. **False-positive flag:** A fabricated Git-command option remains rejected even after Usage/Example verification is supported.

## Gaps

[CODE-VERIFIED] Searches found no explicit `/sc:git` or `--smart-commit` coverage in the inspected recommendation skill, its references, classifier/runbook, and recommendation-specific tests. The relevant direct guide reference is its “Other commands” entry. This negative evidence is limited to those inspected surfaces.

[UNVERIFIED] No recommendation runtime, merge, commit, or test execution occurred. Cache classification quality for Git requests is therefore unmeasured. This analysis does not justify adding a Git-specific classification key or fixed synonym table.

[UNVERIFIED] The user’s desired workflow-first policy is separate from this command’s unchanged contract. Git operations should remain supporting tasks. Broader changes favoring `/sc:workflow` plus `/sc:implement` belong in the consolidated specification; this analysis supplies no evidence that file count, existing specifications, auditability, or resume needs alone require MDTM.

## Key Takeaways

[CODE-VERIFIED] **CHANGE:** Recommendation discovery undersells `/sc:git`, and literal flag-verification rules exclude its documented options. **NO CHANGE:** Its six-month command update was formatting-only; no new semantic capability or protocol skill should be invented.

[UNVERIFIED] **MUST:** Reconcile affirmative Usage/Example evidence with flag verification and add regressions. **SHOULD:** Expand the existing guide entry and preserve plugin parity. **NONE:** No Git-specific cache category, replacement command, implementation escalation, or new keyword-routing table is warranted.
