# Research: /sc:document recommendation coverage

- **Topic type:** Command-specific routing research.
- **Scope:** Six-month command history, current documentation contract, recommendation surfaces, plugin consequences, and regression requirements.
- **Status:** Research complete. No files changed. Report returned directly because worker instructions prohibit writing report files.
- **Date:** 2026-10-24.

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/document.txt`, worker `ad77923c8679370a7`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The command belongs in the requested inventory, but its only change during 2026-04-24 through 2026-10-24 was formatting. Commit `89df2c1105c01caff199288f949d5783f6594e70`, dated 2026-05-22, inserted blank lines around headings, lists, and fenced examples, and added a final newline. Inspection of the exact patch found no flag, trigger, output, or authorization change. There is no substantive command expansion to attribute to this window. Historical evidence: `git log` and `git show` for `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/document.md`.

### Current command contract

[CODE-VERIFIED] This is a self-contained documentation command, not a dispatcher to a protocol skill. Its usage declares a target plus `--type inline|external|api|guide` and `--style brief|detailed`. No default type or style is specified. Although the syntax brackets the target, the behavior requires examining target code and context before generation; the recommendation should preserve a supplied target rather than invent one. No `--output`, `--dry-run`, `--safe`, `--resume`, or review-panel flag is declared. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/document.md:19-38,88-100`.

[CODE-VERIFIED] The documented capability is broader than API references: inline JSDoc/docstrings, external component documentation, API references with examples, and focused user guides. It analyzes code, identifies audience needs, generates documentation, formats it, and integrates it with existing conventions. Documentation creation is a mutation, and inline mode expressly adds content inside source files. The command does not promise an approval checkpoint, a persistent ledger, independent reviewers, or resumable execution. These are verified prose contracts, not results from executing the command. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/document.md:25-85`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide already distinguishes focused documentation from template-led alternatives. Section 3.9 selects technical reference, operations guide, README, or specific-code reference; section 5 contrasts reviewed feature-wide documentation with `/sc:document`'s one-pass reference text. Preserve that useful boundary. However, the specific-code example shows only `--type api`, and the machine-readable `document-built` intent lists technical reference, operational guide, README, and API reference. It does not explicitly advertise inline comments/docstrings, external component documentation, or a focused feature guide, although the command supports all three. Evidence on both sides: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md:175-184,246,320`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/document.md:14-22,49-85`.

[CODE-CONTRADICTED] The recommendation flag-verification wording excludes a valid source format used by this command. Rule R1 permits flags only from a target's “flag table” or `argument-hint`; `/sc:document` has neither, declaring its flags in the Usage grammar instead. The cold-path runbook repeats the restriction, and the enumeration reference directs extraction from a flag table/Options section. Thus the guide's valid `--type api` recommendation conflicts with the literal verification rule. This is a contract contradiction, not evidence that a live model always rejects the flag. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:335-337`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:200-202`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/refs/surface-enumeration.md:58-60`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/document.md:19-22`.

[CODE-VERIFIED] Routing-guide coverage matters before cache behavior: a matched guide row bypasses both cache lookup and cold-path write-back and verifies the row's steps directly. Therefore expanding the existing documentation row is the smallest grounded intervention; no documentation-specific cache key or second fixed keyword table is justified. Checkout precedence already favors source over potentially older installed copies. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:39-61,112`.

### Proposed recommendation changes

[UNVERIFIED] **MUST: broaden the existing documentation route, not implementation scope.** Amend section 3.9, section 5's distinction, and `document-built` in `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`. Route focused inline comments/docstrings, external component documentation, API references, and focused user guides to `/sc:document` with the matching declared type. Retain the template-led alternatives for their existing deliverables. Explain that inline mode edits source, while external documentation writes documentation. This proposal follows the verified command capability; it is not current routing text.

[UNVERIFIED] **MUST: accept explicit Usage declarations as flag evidence.** Update Phase 0 extraction and R1 in `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`, the corresponding extraction reference, and `COLD_PATH_RUNBOOK` in `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`. Accept a directly read flag table, argument hint, or explicit Usage grammar, preserving exact enum values. Do not treat arbitrary prose mentions as authorization for a flag.

[UNVERIFIED] Paste-ready example shapes, grounded in the declared grammar, are `/sc:document <user-supplied-target> --type inline`, `/sc:document <user-supplied-target> --type api --style detailed`, `/sc:document <user-supplied-target> --type guide --style brief`, and `/sc:document <user-supplied-target> --type external`. Substitute only a verified target supplied by the user; do not fabricate an output flag. Flag evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/document.md:22,59-85`.

[UNVERIFIED] **SHOULD: preserve documentation intent during the wider workflow-policy refresh.** Reading many source files to produce external documentation must not alone become a task-builder recommendation. Actual inline source edits above the governing direct-edit limit still need a written plan. Under the user's desired policy, ordinary planned implementation should prefer workflow plus implement, reserving MDTM for the most complex, long-running work. Current source still says “larger, longer, or riskier” in the recommendation fallback, so policy alignment must change that wording rather than claim it already holds. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md:148-157`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py:160-175`.

### Acceptance/regression scenarios

[UNVERIFIED] Add scenarios covering: detailed API reference selects `api` plus `detailed`; limited docstring insertion selects `inline`; external component documentation selects `external`; a brief focused feature guide selects `guide` plus `brief`; a README retains the README route; an explanation-only request does not create documentation; undeclared `--output` is rejected; and extensive inline source editing receives the appropriate written-plan route.

[CODE-VERIFIED] Existing routing tests check source-token and flag existence, including flags in notes, rather than these semantic selections. Extend that coverage without replacing its anti-fabrication checks. Plugin parity also requires recommendation skill files to mirror source and its bundled guide to match the canonical guide. Evidence: `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py:243-255,286-304`; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py:27-36`.

## Gaps

[CODE-VERIFIED] Exact-token searches found no document-specific recommendation references in the recommendation command, skill/reference directory, classifier/runbook module, hooks, or command README; the guide supplies the positive routing references. The routing tests contain the stable `document-built` identifier, not document-specific semantic cases.

[UNVERIFIED] No recommendation invocation, generated documentation, cache replay, or test execution was performed. Runtime selection frequency, cache invalidation effects, output naming, overwrite behavior, and default type/style remain unproven. No delegated document protocol is named in the command, so adding one would exceed this research finding.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** expand the existing documentation route and repair Usage-based flag verification. **SHOULD:** add semantic regressions and preserve documentation-only work during workflow-policy alignment. **NONE:** command implementation changes, new fixed keyword tables, new cache categories, invented flags, or a new document protocol. The command's historical update was formatting-only; the actionable drift is incomplete routing coverage and contradictory verification wording.
