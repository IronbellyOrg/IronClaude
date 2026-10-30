2ccb20795b5316aebf0d81de3cf344de662e9bbc
Review one task for spec compliance.

Task brief: ## Task 15: Replace the remaining Serena tool steps, rewrite the core refresh row and complete the slots ledger

Depends on: Task 14

Implements ./source.md §4 rules G1-G10 and §8 T11c. Tool parts of rows P50 and P96 (`src/superclaude/commands/validate-roadmap.md` `allowed-tools` and `mcp-servers`; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md` Step 0.5 `:320-349` gets a Grep-definition floor with the same 30-lookup cap and the same INFORMATIONAL ONLY artifact, never "skip") and P91 (`src/superclaude/skills/sc-task-protocol/SKILL.md` STRICT prerequisites); rows P92 (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:683`, STRICT no longer needs Serena), P26 (`src/superclaude/agents/auggie-reviewer.md`: drop the two tools, rewrite `:36`, `:81`, `:115`), P33 (`src/superclaude/commands/auggie-review.md:6,78`), P2 (`commands/sc-brainstorm.md`), P62 and P63 (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` and `refs/handoff-routing.md`, tier-2 block deleted and renumbered), P65 (`src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md`: frontmatter and line 83; the `.serena/` ignore at `:57` stays, allowlisted), P22 and P56 (`MODE_Orchestration.md` in `plugins/superclaude/modes/` and `src/superclaude/modes/`), P25 and P76 (`delegation-vs-native-heuristics.md` in `plugins/superclaude/skills/sc-recommend/refs/` and `src/superclaude/skills/sc-recommend/refs/`), P51 line 112 (`src/superclaude/core/CLAUDE.md` "Symbolic queries" refresh row becomes "Grep for the definition and references, then Read"). Append the touched steps to the slots ledger, make it cover every load-bearing file of ./source.md §4.2, and `git add .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` with the commit. Commit `refactor(primitives): replace the remaining Serena symbol tools with a native Grep/Read floor (#323)`, then post the G3 issue-#323 comment.

Acceptance criteria:
- T15.AC1: `make sync-dev && make verify-sync` passes and `uv run pytest tests/troubleshoot tests/cli/reflect tests/skills tests/commands tests/core tests/roadmap/test_threshold_registry.py -q -p no:cacheprovider` passes.
- T15.AC2: `rg -n --no-ignore 'mcp__serena__' src/superclaude plugins/superclaude commands agents` prints nothing.
- T15.AC3: `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing.
- T15.AC4: `for f in commands/troubleshoot.md skills/sc-reflect-protocol/SKILL.md skills/sc-troubleshoot-protocol/SKILL.md skills/sc-validate-roadmap-protocol/SKILL.md agents/reuse-auditor.md; do rg -qF "$f" .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md || echo "ledger missing $f"; done` prints nothing.
- T15.AC5: `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude plugins/superclaude commands agents` prints `ACCEPTANCE_SEARCH_OK serena`.
- T15.AC6: The G3 issue comment URL (or the recorded `gh` error) is in `$PKG/progress.md`.

`$PKG` = /home/coder/workspaces/worktrees/IronClaude/feat-codememory-codegraph-init/.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100 (repo root: the git top-level of that directory). The source spec for anything the brief says is in `$PKG/source.md`; the plan is `$PKG/TASK-WF-phase1RemovalSpe-20261029-185100.md`.

Global constraints (plan `## Constraints`, verbatim):
- Work on branch `ironbelly/feat-codememory-codegraph-init`, base commit `55d40308`. Do not open a pull request to `master` for Phase 1 alone and do not push to `upstream`; Phases 1 and 2 merge as one unit (./source.md §2.2, D9).
- `$PKG` in every command below means this package's directory as the executor resolves it at run time (the folder that holds this plan); never hardcode it. Evidence goes under `$PKG/artifacts/`; handoff notes for other repos go under `$PKG/handoffs/`.
- One commit per task, conventional commit message as given in each task, ending with the attribution line the executor's session requires. Every commit stages the task package with `git add .dev/tasks` (package, `progress.md` and `artifacts/` included). Never stage or commit `.claude/` content (only `.claude/settings.json` is tracked, and Phase 1 does not touch it). Never use `git add -f` on a `.claude/` path.
- Every edit to a `src/superclaude/...` primitive is mirrored by hand, in the same commit, in its `plugins/superclaude/...` twin and its root `commands/sc-*.md` / `agents/sc-*.md` copy where ./source.md §1.2 lists one (D15).
- After editing `src/superclaude/core/HOW-WE-WORK.md`, copy it byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`; if the edit touches the block between `<!-- level-table:v1 -->` and `<!-- /level-table -->`, re-copy that block into `src/superclaude/core/CLAUDE.md`.
- Use `uv run` for Python; standalone scripts run with `uv run --no-project python -I`. Every pytest run uses `-p no:cacheprovider`. Full-suite runs always set `T02_15_PERF_REPORT=/tmp/p1-perf.json` so the tracked `.dev/releases/current/cliEval/evidence/T02.15/perf.json` is not rewritten. After every test run, `git status --short` must list only files the task intends to change; restore any tracked file a test changed.
- Test baseline: the full suite already has failures at the base (W1 saw 27 failed and 16 errors). "Passes" for a targeted command means no failing test id that is not in `$PKG/artifacts/baseline/full.txt` (compare with the `comm -13` form in Task 18); never assume a clean suite.
- Never run the real `./update.sh`, `superclaude install` (including `--list`) or `claude mcp add/remove` against the real `HOME`; every environment check runs in a sandbox `HOME` made with `mktemp -d` (./source.md §10, D8). Never delete user data (`~/.serena`, project `.serena/` folders outside this repo, `~/.cache/codebase-memory-mcp`). Never edit another repository.
- Progress reporting (./source.md §9): at the end of each task group (Phases 1-6 below, i.e. groups G0-G5) post exactly one comment on issue #323 of the fork, and only there. First run `gh repo view --json nameWithOwner -q .nameWithOwner` (must print `IronbellyOrg/IronClaude`; otherwise run `gh repo set-default IronbellyOrg/IronClaude`), then `gh issue comment 323 --repo IronbellyOrg/IronClaude --body "Phase 1 progress: <group id and name> committed on ironbelly/feat-codememory-codegraph-init at <short sha>. Tasks: <task ids>. Checks: <exact commands> -> <result>. Decisions logged: <count, path in task package>. Next: <next group>."`. Never use a bare `gh issue comment` and never `--repo SuperClaude-Org/...`. If `gh` is unauthenticated or fails, record the exact error and the intended body in `$PKG/progress.md` and continue (not a blocker).
- Decision rules (./source.md §10), never stop to ask the user: a simple decision (one obvious option, or one the source already constrains) is made by the executor and logged as one line in `$PKG/decisions.md` (decision, options, method `self`, rationale). A mid-level decision (two or more viable options with real trade-offs inside one task) writes each option to `$PKG/decisions/<task>-<slug>/option-<x>.md`, spawns an agent that runs `/sc:adversarial --compare <option files> --depth quick`, follows its recommendation and logs method `adversarial quick` with the merged-recommendation path. A complex decision (an architectural change to the source's design: retire-step scope, memory store layout, merge order, deleting a file the source keeps) does the same with `/sc:adversarial --compare <option files>` (standard depth) and logs method `adversarial full`.
- A blocked task stays blocked with its reason in `$PKG/progress.md`; continue with tasks that do not depend on it. If a task's acceptance fails, fix it within the task's files; if the fix needs a file another task owns, pull that edit forward and log it in `$PKG/decisions.md`. A task may not need a later task to go green.
- Scope limits (./source.md §2.1, §2.3): existing `.dev/` files outside `$PKG` are never edited; the only other `.dev/` writes are the new files `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` and `.dev/codegraph-migration/handoffs/phase2-facts-from-phase1.md`, and each task that writes one stages that exact file (`git add <path>`, never the folder). No task uninstalls the `serena-agent` uv tool or removes `~/.local/bin/{serena,serena-agent,serena-hooks}`, the Coder `/usr/local/bin/codebase-memory-mcp` binary, bundle markers, upstream companions or `~/.local/bin/install.sh`; those are handed off, not removed by Phase 1.
- This plan was corrected after an advisory `/sc:reflect --mode pre` review (`.dev/codegraph-migration/review/F1-result.md`). Where a task's text here differs from `./source.md`, the task text wins.
- Human actions the executor must not attempt: merging Phases 1 and 2 to `master` (Phase 2's PR via `/sc:pr-submit`) and running the real `./update.sh` on a live workspace after that merge (Phase 2 owns that live check).
Start sha: 2ccb20795b5316aebf0d81de3cf344de662e9bbc
Diff against the start snapshot: Work is already committed as HEAD c42758e1 (git show --stat HEAD; diff vs the start is git diff 2ccb20795b5316aebf0d81de3cf344de662e9bbc HEAD). Touched files: see the stat. The edits were made by a helper agent; judge the files on disk. Spec: the plan's Task 15 text and $PKG/source.md section 4 (lines 378-406) and section 8 T11c. Observed by the implementer (verify yourself): make sync-dev && make verify-sync passes; the Task 15 pytest command gives 1321 passed, 1 xpassed; rg 'mcp__serena__' over src/superclaude plugins/superclaude commands agents prints nothing; the roster comm -13 prints nothing; the ledger loop prints nothing; acceptance-search.sh serena prints ACCEPTANCE_SEARCH_OK serena. The G3 comment is https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6511773360, recorded at $PKG/artifacts/issue-comments.md:6. PENDING LEDGER WRITE appended to $PKG/progress.md only if this review passes (append-only ledger): 'T15: complete verdict=compliant ac=T15.AC1,...,T15.AC6 evidence=...,https://github.com/IronbellyOrg/IronClaude/issues/323#issuecomment-6511773360,T15.AC6@./artifacts/issue-comments.md:6 ...' (the URL goes in the complete line evidence because the ledger accepts no free text; decision 1). Decisions 8 and 9 in $PKG/decisions.md record two judgment calls (STRICT row value in sc-tasklist-protocol, deleting the MODE_Orchestration Symbol operations row).

 commands/sc-brainstorm.md                          |  7 +++----
 plugins/superclaude/modes/MODE_Orchestration.md    |  1 -
 .../refs/delegation-vs-native-heuristics.md        |  2 +-
 src/superclaude/agents/auggie-reviewer.md          |  9 ++++----
 src/superclaude/commands/auggie-review.md          |  2 +-
 src/superclaude/commands/validate-roadmap.md       |  2 +-
 src/superclaude/core/CLAUDE.md                     |  2 +-
 src/superclaude/modes/MODE_Orchestration.md        |  1 -
 .../skills/sc-brainstorm-protocol/SKILL.md         |  9 ++++----
 .../sc-brainstorm-protocol/refs/handoff-routing.md | 16 ++++-----------
 .../skills/sc-cleanup-audit-protocol/SKILL.md      |  2 +-
 .../refs/delegation-vs-native-heuristics.md        |  2 +-
 src/superclaude/skills/sc-task-protocol/SKILL.md   |  4 ++--
 .../skills/sc-tasklist-protocol/SKILL.md           |  2 +-
 .../skills/sc-validate-roadmap-protocol/SKILL.md   | 24 +++++++++-------------
 15 files changed, 34 insertions(+), 51 deletions(-)
diff --git a/src/superclaude/agents/auggie-reviewer.md b/src/superclaude/agents/auggie-reviewer.md
--- a/src/superclaude/agents/auggie-reviewer.md
+++ b/src/superclaude/agents/auggie-reviewer.md
@@ -2,7 +2,7 @@
 name: auggie-reviewer
 description: Independent code-review specialist that performs a Claude-side review pass alongside Auggie's deep retrieval pass, used in /sc:auggie-review --depth deep for cross-validation
 category: analysis
-tools: [Read, Grep, Glob, Bash, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols]
+tools: [Read, Grep, Glob, Bash, mcp__auggie__codebase-retrieval]
 model: opus
 ---
 
@@ -33,7 +33,7 @@ The orchestrator passes you:
 ## Responsibilities
 
 1. **Read the diff (or file list) end-to-end before forming any findings.** Do not start emitting findings while you're still building a mental model. A premature pass produces shallow, scattered findings.
-2. **For each non-trivial change, pull adjacent context** with `Read` (or `mcp__serena__find_symbol`): the surrounding function, the callers, the callees. Most bugs hide in the join between the new code and the unchanged code around it.
+2. **For each non-trivial change, pull adjacent context** with `Read` (use Grep for the definition first when you only know the name): the surrounding function, the callers, the callees. Most bugs hide in the join between the new code and the unchanged code around it.
 3. **Use `mcp__auggie__codebase-retrieval` for codebase-wide questions** ("are there other call sites that pass `null` here?", "what's the existing convention for this kind of error handling?"). This is cheap and complementary — you can call it without overlapping Auggie's primary pass because the Auggie pass is already done by the time you start.
 4. **Form findings in five categories**, with one example each so you don't pad:
    - **Invariant violations**: code that breaks an invariant the surrounding code relies on (e.g., a method that promises sorted output but no longer guarantees it).
@@ -75,10 +75,9 @@ If you have no findings, return `findings: []` with an honest note in `notes_for
 ## Tools
 
 - **Read**: pull diff bodies and adjacent context
-- **Grep / Glob**: find related call sites, similar patterns, prior conventions
+- **Grep / Glob**: find related call sites, similar patterns, prior conventions. To locate a definition, Grep for `def <name>|class <name>|function <name>` and Read the range; to confirm who calls what, Grep with a word-boundary pattern for the symbol and Read the call sites
 - **Bash**: `git log -p --follow <file>` for blame-style context when an unfamiliar pattern needs justification; `wc -l`, `find` for sizing
 - **mcp__auggie__codebase-retrieval**: codebase-wide semantic queries (not the same as Auggie's deep pass — this is in-session, cheap, and you can use it freely)
-- **mcp__serena__find_symbol** / **find_referencing_symbols**: precise symbol-level cross-reference when you need to confirm who calls what
 
 ## Focus Areas
 
@@ -112,7 +111,7 @@ You focus on what indexed-retrieval is bad at:
 **Will:**
 
 - Produce independent findings focused on what indexed-retrieval misses
-- Use cheap codebase queries (mcp__auggie__codebase-retrieval, Serena symbol tools) freely
+- Use cheap codebase queries (`mcp__auggie__codebase-retrieval`, Read, Grep) freely
 - Honestly report coverage gaps in `notes_for_orchestrator`
 
 **Will Not:**
diff --git a/src/superclaude/commands/auggie-review.md b/src/superclaude/commands/auggie-review.md
--- a/src/superclaude/commands/auggie-review.md
+++ b/src/superclaude/commands/auggie-review.md
@@ -75,7 +75,7 @@ Do NOT proceed with protocol execution using only this command file. The full be
 ## MCP Integration
 
 - **Native reasoning**: Multi-step synthesis when reconciling Auggie findings with Claude's diff-level checks
-- **Serena**: Symbol-level cross-reference when validating Auggie's file:line citations against actual code
+- **Native Read / Grep floor**: Cross-reference when validating Auggie's file:line citations against actual code (Grep for the definition, then Read the range; Grep with a word-boundary pattern for references, then Read the call sites)
 
 External tool (not MCP, but central): **`auggie` CLI** is the primary review engine. The skill shells out to `auggie --print --output-format json --ask` to offload deep analysis to Auggie's indexed codebase context, dramatically reducing Claude token consumption.
 
diff --git a/src/superclaude/commands/validate-roadmap.md b/src/superclaude/commands/validate-roadmap.md
--- a/src/superclaude/commands/validate-roadmap.md
+++ b/src/superclaude/commands/validate-roadmap.md
@@ -3,7 +3,7 @@ name: sc:validate-roadmap
 description: "Validate roadmap pipeline outputs (roadmap.md, test-strategy.md, extraction.md) produced by `superclaude roadmap run`. Mirrors the CLI `roadmap validate` surface: single-agent reflection by default, adversarial merge when N≥2 agents; always exits 0 per NFR-006 with findings surfaced as console output."
 category: analysis
 complexity: advanced
-allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__read_memory, mcp__serena__write_memory, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern, mcp__serena__activate_project
+allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval
 mcp-servers: [auggie]
 personas: [analyzer, architect, qa]
 ---
diff --git a/src/superclaude/core/CLAUDE.md b/src/superclaude/core/CLAUDE.md
--- a/src/superclaude/core/CLAUDE.md
+++ b/src/superclaude/core/CLAUDE.md
@@ -108,7 +108,7 @@ Pick the refresh tool by the content type of the claim:
 | Content | Tool |
 |---|---|
 | Exact line numbers / file content | `Read` |
-| Symbolic queries (which function, where defined, what references) | `mcp__serena__find_symbol` / `find_referencing_symbols` |
+| Symbolic queries (which function, where defined, what references) | `Grep` for the definition and references, then `Read` |
 | Semantic / cross-cutting ("is there an X anywhere") | `mcp__auggie__codebase-retrieval` |
 | Runtime state (permissions, mounts, sockets) | `Bash` (user-executed read-only command) |
 
diff --git a/src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md b/src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md
--- a/src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md
@@ -1,7 +1,7 @@
 ---
 name: sc-validate-roadmap-protocol
 description: "Full behavioral protocol for sc:validate-roadmap — multi-agent roadmap-to-spec fidelity validation with adversarial review, coverage matrix, gap registry, and remediation planning. Use this skill whenever verifying roadmap completeness against specifications, auditing coverage before tasklist generation, or checking for requirement gaps between specs and roadmaps."
-allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__search_for_pattern, mcp__serena__activate_project
+allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, mcp__auggie-mcp__codebase-retrieval
 argument-hint: "<roadmap-path> --specs <spec1.md,...> [--output dir] [--depth quick|standard|deep] [--exclude domains] [--max-agents N]"
 ---
 
@@ -19,10 +19,10 @@ version: 2.0.0
 
 **This skill is an inference-only deep-validation protocol.** It is NOT a behavioural mirror of the `superclaude roadmap validate` CLI command, and it is not invoked by that CLI. Treat the two surfaces as **complementary, not equivalent**:
 
-- **Use this skill** for thorough investigative validation — when a human reviewer wants a multi-phase coverage matrix, gap registry, adversarial review, and remediation plan grounded in Auggie/Serena enrichment. This is the right tool when the goal is to *understand* roadmap quality and decide whether the roadmap is ready for tasklist generation.
+- **Use this skill** for thorough investigative validation — when a human reviewer wants a multi-phase coverage matrix, gap registry, adversarial review, and remediation plan grounded in Auggie enrichment. This is the right tool when the goal is to *understand* roadmap quality and decide whether the roadmap is ready for tasklist generation.
 - **Use the CLI** (`superclaude roadmap validate`) for **automated CI/CD gating**. The CLI runs a simpler **reflect + adversarial-merge** flow: it builds reflect/merge prompts (`src/superclaude/cli/roadmap/validate_prompts.py:7,68`), executes the pipeline, and parses report counts to emit a pass/fail verdict against a fixed set of validation dimensions. It is fast, deterministic, and non-interactive — appropriate for pre-merge or pre-tasklist hooks, not for human investigation.
 
-The deep protocol below (phases, CC-agents, GO / CONDITIONAL_GO / NO_GO verdict matrix, Auggie/Serena enrichment) is preserved intentionally: it carries inference value that the single-pass CLI flow does not attempt to reproduce. The CLI does **not** delegate into this skill, and this skill does **not** wrap the CLI; they are two separate validation surfaces operating at different levels of rigour and automation.
+The deep protocol below (phases, CC-agents, GO / CONDITIONAL_GO / NO_GO verdict matrix, Auggie enrichment) is preserved intentionally: it carries inference value that the single-pass CLI flow does not attempt to reproduce. The CLI does **not** delegate into this skill, and this skill does **not** wrap the CLI; they are two separate validation surfaces operating at different levels of rigour and automation.
 
 ### CLI validation dimensions (crosswalk)
 
@@ -44,7 +44,7 @@ The CLI's reflect prompt validates the roadmap against **7 baseline dimensions**
 
 | Skill phase | Closest CLI dimensions | Notes |
 |---|---|---|
-| Phase 1 — Extraction & taxonomy | Coverage (#6, input-aware) | Skill extracts requirements via Auggie/Serena enrichment; CLI relies on caller-supplied input files. |
+| Phase 1 — Extraction & taxonomy | Coverage (#6, input-aware) | Skill extracts requirements via Auggie enrichment; CLI relies on caller-supplied input files. |
 | Phase 2 — Coverage matrix | Traceability (#3), Coverage (#6) | Skill builds an explicit matrix; CLI emits findings against the dimensions but does not persist a matrix artifact. |
 | Phase 3 — Gap registry | Traceability (#3), Coverage (#6), Proportionality (#7) | Skill itemises and severity-sorts gaps; CLI returns BLOCKING/WARNING findings with `file:line` citations. |
 | Phase 4 — Adversarial review | (none direct) | Skill runs CC1–CC4 adversarial agents; CLI runs a single-shot `build_merge_prompt` adversarial merge pass. |
@@ -125,9 +125,6 @@ Every verb maps to exactly one Claude Code tool. Never use bare verbs without th
 | Query codebase (semantic) | `mcp__auggie-mcp__codebase-retrieval` | Codebase-grounded enrichment (Steps 0.2b, 5.1b) — orchestrator only, fail-open |
 | Read session memory | `Read` | `.superclaude/memory/validate-roadmap/<key>.md` — load validation ledger, terminology, patterns (Pre-Phase 0) — fail-open |
 | Write session memory | `Write` | `.superclaude/memory/validate-roadmap/<key>.md` — persist ledger, terminology, patterns (Post-Phase 6); create `.superclaude/.gitignore` containing `*` first if absent — fail-open |
-| Activate project | `mcp__serena__activate_project` | Initialize Serena project context (Step 0.5) — fail-open |
-| Find symbol | `mcp__serena__find_symbol` | Symbol lookup for context supplement (Step 0.5, deep only) — fail-open |
-| Get symbols overview | `mcp__serena__get_symbols_overview` | File-level symbol map (Step 0.5, deep only) — fail-open |
 
 **Rule**: All verbs in phase instructions MUST resolve to an entry in this glossary. MCP tools marked "fail-open" are optional — their unavailability never blocks validation.
 
@@ -316,7 +313,7 @@ Write artifact: `{OUTPUT_DIR}/00-domain-taxonomy.md`
 
 #### Step 0.5 — Symbol Context Supplement (`--depth deep` only)
 
-**Requires**: `mcp__serena__find_symbol`, `mcp__serena__get_symbols_overview` (fail-open — skip entirely if Serena is unavailable or depth is not `deep`).
+**Requires**: `Grep` and `Read` only (native floor; always available).
 
 **Gate**: Skip this step unless `--depth deep` is set.
 
@@ -325,11 +322,10 @@ At deep depth, produce a supplemental artifact documenting the structural contex
 **Procedure**:
 
 1. **Identify code-referenced requirements**: From the requirement universe, collect requirements whose text contains backtick-wrapped identifiers (class names, function names, module paths).
-2. **Activate Serena project**: Call `mcp__serena__activate_project` (if not already activated in Pre-Phase 0).
-3. **Look up symbols** (hard cap: **30 symbol lookups**):
-   - For each code identifier, call `mcp__serena__find_symbol` with `include_body=False` to locate the symbol's file, type (class/function/method), and parent hierarchy.
-   - For files with multiple related symbols, call `mcp__serena__get_symbols_overview` once per file to capture the structural context.
-4. **Write supplemental artifact**: `{OUTPUT_DIR}/00-symbol-context-supplement.md`
+2. **Look up symbols** (hard cap: **30 symbol lookups**):
+   - For each code identifier, call `Grep` for its definition (`def <name>|class <name>|function <name>`) to locate the symbol's file and type (class/function/method); `Read` the matched range only when the parent hierarchy is needed. A Grep with no match records the symbol as `NOT_FOUND`.
+   - For files with multiple related symbols, `Read` the file once to capture the structural context.
+3. **Write supplemental artifact**: `{OUTPUT_DIR}/00-symbol-context-supplement.md`
 
 ```markdown
 # Symbol Context Supplement (Step 0.5, deep only)
@@ -345,7 +341,7 @@ At deep depth, produce a supplemental artifact documenting the structural contex
 Symbols found: {N} / {N} attempted
 ```
 
-5. **Failure handling**: If Serena is unavailable or no symbols are found, skip entirely — write no artifact. This is non-blocking.
+4. **Failure handling**: Grep and Read are always available, so the artifact is always written at `--depth deep`. Symbols with no definition match are listed as `NOT_FOUND`; when no code-referenced requirement exists, write the artifact with `Symbols found: 0 / 0 attempted`. A failed Grep or Read for one symbol records that row as `NOT_FOUND` and continues. This is non-blocking.
 
 **Constraints**:
 
Delta diff from the previous reviewed tree (empty on the first review): (empty)
Earlier blocking findings of this start (empty on the first review): (empty)
Saved-probe re-check hit locations (may be empty): (none)

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
