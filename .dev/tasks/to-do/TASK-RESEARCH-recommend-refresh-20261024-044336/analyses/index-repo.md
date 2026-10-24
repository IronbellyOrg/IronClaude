# Research: /sc:index-repo

- **Topic type:** Command and recommendation-contract comparison
- **Scope:** Six-month history, live command, recommendation discovery/cache, guide, plugin mirror, and relevant tests
- **Status:** Research complete; no implementation or runtime command execution
- **Date:** 2026-10-24

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/index-repo.txt`, worker `a5c33d8bd22a9ec4b`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] The command has one reachable change in the specified 2026-04-24 through 2026-10-24 window: `89df2c1105c01caff199288f949d5783f6594e70`, authored 2026-05-22, “chore: apply markdownlint MD022/MD031/MD032/MD034 auto-format repo-wide (#74).” Its actual patch adds blank lines before fenced blocks and lists. It changes no inputs, output, activation, or indexing behavior. This is a formatting-only command in scope, not evidence of a recent semantic upgrade. Current content: [C], lines 15-173.

### Current command contract

[CODE-VERIFIED] `/sc:index-repo` is self-contained Markdown, not a dispatcher to a protocol skill. It describes five concurrent repository searches, extraction of entry points, public interfaces and dependencies, index generation, and validation. Its output contract names both `PROJECT_INDEX.md` and `PROJECT_INDEX.json`. The Markdown includes structure, modules, configuration, documentation, tests, dependencies, and quick-start information. [C], lines 15-128 and 168-173.

[CODE-VERIFIED] The documented invocations are a bare creation request, `mode=update`, and `mode=quick`, with quick explicitly described as skipping tests. These are keyword arguments, not `--mode`, `--quick`, or `--depth` flags. No explicit target-path argument, output-directory argument, parser, formal default-mode identifier, resume ledger, or execution handoff is defined. [C], lines 132-173.

[CODE-VERIFIED] Creating the two index files is a mutation. The command does not define an update-confirmation gate or preservation rule for existing manual index content. Recommendation must describe it as writing repository artifacts, not as a read-only investigation. [C], lines 70-72 and 168-173.

[UNVERIFIED] The advertised “94% token reduction,” fixed token costs, break-even point, and output-size figures are assertions in the command, not measurements established by this research. Recommendation should describe compact reusable repository context without promising numerical savings. [C], lines 3, 10-13, and 154-173.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide already discovers this command correctly in its “Other commands” block: “Write `PROJECT_INDEX.md` and `.json` so later sessions read less.” It separately lists `/sc:index` as building a documentation index. However, the index-repo entry omits update and quick modes and their distinguishing purpose. [G], lines 260-275. The command supplies those missing capabilities. [C], lines 132-150.

[CODE-VERIFIED] The recommendation skill consumes “Other commands” only when no routing row matches. It passes that block to cold-path discovery, verifies candidates against their source, and prefers checkout source over development mirrors inside this repository. A matched guide row bypasses cache and semantic ranking. Consequently, placing the command in “Other commands” makes it discoverable but does not make it an authoritative route when a broader intent matches first. [R], lines 39-61 and 96-135.

[CODE-VERIFIED] Two similar surfaces must remain distinct. `/sc:index` accepts a target, documentation type, and output format and describes comprehensive documentation generation and maintenance. The `repo-index` agent instead includes an age gate: it stops when an index is younger than seven days. Neither its seven-day threshold nor `/sc:index` flags belong to `/sc:index-repo`. [I], lines 19-38; [A], lines 9-32; [C], lines 132-150.

[CODE-VERIFIED] The recommendation skill’s blanket statement that commands are thin skill dispatchers is inaccurate for this command. Its verification step should recognize a self-contained command rather than infer a missing protocol skill. [R], lines 112-132; [C], lines 1-177.

[CODE-VERIFIED] The classifier has no repository-index-generation category. Its closest category, `codebase-research`, means understanding a codebase; it explicitly permits `unknown` for requests outside its vocabulary. A cache hit emits a saved recommendation rather than running candidate discovery again. Source validation checks the selected target’s bytes, not whether a different user goal belongs to that target. [P], lines 50-92; [R], lines 63-88; [D], lines 116-137.

[UNVERIFIED] A repository-index request could therefore be mistaken for conceptual codebase research and reuse an unsuitable cached target. This is a source-grounded risk, not a reproduced failure. No classifier or recommendation execution was performed.

[CODE-VERIFIED] The plugin command contains the same creation, update, quick, and two-file output contract. Its bundled guide repeats the same abbreviated index-repo entry. Updating only the source guide would leave plugin recommendations without the clarified capability description. [PC], lines 132-173; [PG], lines 260-275.

### Proposed recommendation changes

[UNVERIFIED] **MUST, proposed routing policy:** Expand the existing index-repo entry in [G] and its plugin copy [PG]. Describe creation or refresh of the compact repository map, both generated filenames, `mode=update` for refresh, and `mode=quick` when the user explicitly wants tests omitted. Keep this in the existing governing guide rather than adding a second keyword-routing table.

[UNVERIFIED] **MUST, proposed discovery rule:** In [R] Step 0 and Phase 0 verification, distinguish explicit requested artifacts from broad “understand code” intents. A request to generate or refresh `PROJECT_INDEX` artifacts must not be satisfied with an explanation, research report, documentation index, or implementation plan merely because it includes the words “understand the repository.” Verify documented keyword arguments from Usage/examples as well as flag tables.

[UNVERIFIED] **SHOULD, proposed classifier regression:** In [P], add a negative example distinguishing repository-map generation from `codebase-research`. Preserve the existing `unknown` fallback when no category fits; do not invent a cache category or force indexing into a research bucket. Check behavior with an existing research cache entry.

[UNVERIFIED] **SHOULD, proposed activation correction:** Qualify [R]’s thin-dispatcher statement: some commands are self-contained. Follow an activation target only when the verified command actually names one.

[UNVERIFIED] Paste-ready handoffs, grounded in the command’s canonical frontmatter name and documented argument spellings, are:

- Create: `/sc:index-repo`
- Refresh: `/sc:index-repo mode=update`
- Quick, omitting tests: `/sc:index-repo mode=quick`

These are proposed recommendation outputs, not evidence that all variants were executed. [C], lines 2 and 132-150.

[UNVERIFIED] Preserve this dedicated artifact-generation command while adopting the user’s broader preference for workflow/implement on planned implementation work. Index creation alone should not acquire task-builder or workflow overhead. No change to either executor’s capacity is established by this command analysis.

### Acceptance/regression scenarios

[UNVERIFIED] Future validation should cover:

1. “Create a compact repository map for later sessions” recommends index-repo and names both output files without promising 94% savings.
2. “Refresh our existing PROJECT_INDEX” preserves `mode=update`.
3. “Quick repository index, omit tests” preserves `mode=quick`, not an invented flag.
4. “Generate API documentation as JSON” remains eligible for `/sc:index`, not index-repo.
5. A request to refresh a recently generated index does not inherit the agent’s seven-day early-stop rule.
6. An existing codebase-research cache entry does not replace an explicit repository-index artifact request.
7. Checkout and plugin guide variants retain equivalent descriptions.

[CODE-VERIFIED] Existing guide tests ensure index-repo appears in “Other commands” and resolves to a real source file. They do not validate these semantic distinctions or mode-preserving recommendations. [T], lines 26-41 and 275-283.

## Gaps

[CODE-VERIFIED] Searching recommendation source, references, classifier/cache modules, hooks, plugin surfaces, and tests found index-repo’s explicit recommendation description in the guide and plugin guide, but no command-specific mode-selection regression.

[CODE-VERIFIED] The command’s Usage examples use `/index-repo`, while frontmatter and the guide use the canonical `sc:index-repo` name. This is a documentation inconsistency; recommendation should retain the verified canonical name. [C], lines 2 and 132-150; [G], line 275.

[UNVERIFIED] Update merging semantics, exact overwrite behavior, JSON schema, measured savings, and actual invocation results remain unverified. Do not invent guarantees to fill these omissions.

## Key Takeaways

**CHANGE:** Improve capability discovery, preserve documented keyword arguments, and test cache-related intent separation. The history itself warrants **NO semantic migration** because its sole in-window patch is formatting-only.

**MUST:** Clarify the existing guide entry and protect explicit artifact intent from broader routes.

**SHOULD:** Add classifier/cache regressions and correct the self-contained-command assumption.

**NONE:** No new protocol, fixed keyword table, index implementation rewrite, executor expansion, or automatic task-builder handoff.

## Evidence paths

- **[C]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/index-repo.md`
- **[G]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **[R]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **[I]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/index.md`
- **[A]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/agents/repo-index.md`
- **[P]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/prompts.py`
- **[D]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/cli/recommend/dispatch.py`
- **[PC]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/commands/index-repo.md`
- **[PG]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
- **[T]** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py`
