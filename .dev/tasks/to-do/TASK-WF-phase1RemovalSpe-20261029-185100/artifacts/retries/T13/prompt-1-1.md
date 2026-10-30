46eebdaa0442e2b73e49fccb6e01064889f5aa84
Review one task for spec compliance.

Task brief: ## Task 13: Replace reflect's Serena symbol, reference and diagnostics steps with a Grep/Read floor

Depends on: Task 12

Implements ./source.md §4 rules G1-G9 and §8 T11a. Tool parts of rows P6, P15, P43 (the three reflect command copies: rewrite the tool table, delete the `--onboard` Serena bootstrap rows) and P77 (`src/superclaude/skills/sc-reflect-protocol/SKILL.md`: delete Serena probes and telemetry, symbol chain to the Grep-definition-then-Read floor, step 4.5 deleted, Step 7 `search_deps` skipped with its claim `[INFERRED]`, section 6.1.1 envelope retitled for the Bash linter/type-checker call, `serena` degraded tokens and the section 6.5 and section 10 fallback rows removed); rows P78, P79, P80, P81, P83, P84, P86, P87 (reflect refs `cost-profile.yaml`, `coverage-mapping.md`, `deviation-taxonomy.md`, `grader-extensions.md`, `ops-integration.md` Serena WARN catalog, `reflection-rubric.md`, `reviewer-spec.md`, `runtime-surface.md`), with these per-line actions where the row line lists fall short: `refs/reflection-rubric.md` line 124 reword the "V3 Serena adoptions" heading, lines 126-127 delete (FR-6 onboarding weight and FR-7 `get_current_config` up-weight die with rule M8), line 128 reword the missing-implementor term to the G2 "Grep for `class .*\(<Base>\)` best effort" floor, line 129 keep (retitle its step reference if the section 6.1.1 heading changes), line 130 delete (step 4.5 `type_hierarchy` is gone; `type_hierarchy_invoked: false` stays per G8); `refs/cost-profile.yaml:74` and `refs/deviation-taxonomy.md:80`, `:83` rewrite `execute_shell_command` to the Bash verification run under the retitled envelope; `refs/deviation-taxonomy.md:79` rewrite `get_diagnostics_for_file` to the project's own linter or type-checker run (rule G4); `refs/coverage-mapping.md:195` delete the hierarchy-gap weight paragraph; `refs/reviewer-spec.md:14` drop the `execute_shell_command` token (keep "no `Bash`"), `refs/reviewer-spec.md:55` delete the hierarchy-slice hunk paragraph. Keep the section 6.1.1 "No-mutation gate." paragraph that `tests/cli/reflect/test_verify_denylist_git_mutations.py` pins; P28 (`src/superclaude/agents/reflect-reviewer.md`: drop the four tools, rewrite line 147) and P29 (`src/superclaude/agents/reuse-auditor.md`: drop the three tools, `:54`, `:57` F4 to a Grep reference search, `:131` to "Grep by capability tokens + skeleton grep"); D3 (`tests/cli/reflect/test_marker_suppression.py:101-130` follows the retitled 6.1.1 heading), D4 and D5 (drop `execute_shell_command` from the denylist sets in `tests/cli/reflect/test_reviewer_readonly_tools.py:7,31` and `tests/cli/reflect/test_reviewer_finding_parity.py:33`). Keep the stable contract fields of rule G8 (`find_declaration_no_match`, `type_hierarchy_invoked: false`, `summarize_changes_invoked: false`, `references_extended_info_used: false`). Closed rosters lose only `mcp__serena__*` names and never gain Bash. Create `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` if absent and append one row per touched step: file, step heading or anchor (not a line number), former Serena tool, action (deleted / floor), floor used, contract fields touched; `git add .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` with the commit. Commit `refactor(reflect): replace Serena symbol, reference and diagnostics steps with a native Grep/Read floor (#323)`.

Acceptance criteria:
- T13.AC1: `make sync-dev && make verify-sync` passes and `uv run pytest tests/cli/reflect tests/skills tests/commands -q -p no:cacheprovider` passes.
- T13.AC2: `bash $PKG/artifacts/acceptance-search.sh serena src/superclaude/skills/sc-reflect-protocol src/superclaude/commands/reflect.md plugins/superclaude/commands/reflect.md commands/sc-reflect.md src/superclaude/agents/reflect-reviewer.md src/superclaude/agents/reuse-auditor.md` prints `ACCEPTANCE_SEARCH_OK serena`.
- T13.AC3: `comm -13 <(sort $PKG/artifacts/baseline/rosters.txt) <(uv run --no-project python -I $PKG/artifacts/check_rosters.py | sort)` prints nothing.
- T13.AC4: `test -s .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` succeeds and the ledger has rows for `sc-reflect-protocol/SKILL.md`, `reflect-reviewer.md` and `reuse-auditor.md`.

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
Start sha: 46eebdaa0442e2b73e49fccb6e01064889f5aa84
Diff against the start snapshot: Touched files: see the stat (uncommitted working tree), plus the new untracked file .dev/codegraph-migration/handoffs/phase3-codegraph-slots.md (read it from disk). Spec: the plan's Task 13 text (it carries per-line actions) and $PKG/source.md section 4 (lines 378-406), section 8 T11a (grep 'T11a' in source.md) and section 8.1. The edits were made by a helper agent; judge the files on disk. Scope: Task 13 does the reflect TOOL parts (symbol, reference, diagnostics, allowlist, onboarding, degraded tokens); memory parts were Task 12 (done earlier); troubleshoot, validate-roadmap, auggie-reviewer and the rest are Tasks 14 and 15. Observed by the implementer (verify yourself): make sync-dev && make verify-sync passes; uv run pytest tests/cli/reflect tests/skills tests/commands gives 811 passed, 1 xpassed; acceptance-search.sh serena on the six listed path groups prints ACCEPTANCE_SEARCH_OK serena; the comm -13 roster check prints nothing; the slots ledger has 97 lines and rows for the three named files. Known judgment calls: Step 0.7 kept as a hydrate-only step; ops-integration.md keeps the generic mutation-denied and metachar-denied WARNs and was retitled; contract_version left at 1.8.0 with a comment; 'verification triangle' renamed 'verification run'.

 commands/sc-reflect.md                             |  21 +-
 plugins/superclaude/commands/reflect.md            |  16 +-
 src/superclaude/agents/reflect-reviewer.md         |   6 +-
 src/superclaude/agents/reuse-auditor.md            |   8 +-
 src/superclaude/commands/reflect.md                |  16 +-
 .../skills/sc-reflect-protocol/SKILL.md            | 213 +++++++--------------
 .../sc-reflect-protocol/refs/cost-profile.yaml     |   4 +-
 .../sc-reflect-protocol/refs/coverage-mapping.md   |  14 +-
 .../sc-reflect-protocol/refs/deviation-taxonomy.md |  11 +-
 .../sc-reflect-protocol/refs/grader-extensions.md  |   2 +-
 .../sc-reflect-protocol/refs/ops-integration.md    |  44 +----
 .../sc-reflect-protocol/refs/reflection-rubric.md  |   9 +-
 .../sc-reflect-protocol/refs/reviewer-spec.md      |  10 +-
 .../sc-reflect-protocol/refs/runtime-surface.md    |   2 +-
 tests/cli/reflect/test_marker_suppression.py       |   8 +-
 tests/cli/reflect/test_reviewer_finding_parity.py  |   4 +-
 tests/cli/reflect/test_reviewer_readonly_tools.py  |   6 +-
 17 files changed, 121 insertions(+), 273 deletions(-)

diff --git a/src/superclaude/agents/reflect-reviewer.md b/src/superclaude/agents/reflect-reviewer.md
--- a/src/superclaude/agents/reflect-reviewer.md
+++ b/src/superclaude/agents/reflect-reviewer.md
@@ -2,7 +2,7 @@
 name: reflect-reviewer
 description: Restricted read-only deviation-audit agent for sc:reflect Wave-3. Audits completed work against its driving spec/tasklist and classifies every divergence under the 4-category deviation taxonomy (Authorized expansion / Necessary deviation / Drift / Regression). Spawned as one of N heterogeneous Tier-2 reviewers; carries a read-only tool allowlist (no Bash/Edit/Write/Task) so a reviewer can never mutate the repository it is auditing. Returns structured deviation findings; the orchestrator persists them.
 category: quality
-tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__find_referencing_symbols, mcp__serena__get_symbols_overview, mcp__serena__get_diagnostics_for_file
+tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval
 model: sonnet
 maxTurns: 50
 permissionMode: plan
@@ -126,7 +126,7 @@ These findings are RAISED FOR TRIAGE by the orchestrator; they MUST NOT set `reg
 **Will Not:**
 
 - Edit, write, move, rename, or delete ANY file.
-- Run shell commands (no Bash) or git verbs.
+- Run shell commands (no Bash) or git verbs. Diagnostics (the project's own linter or type-checker) are run by the orchestrator's verification leg and reach you as a verification-results grounding hunk; you never run them.
 - Spawn sub-agents (no `Task`).
 - Audit the live shared worktree instead of the supplied snapshot.
 - Soften a real deviation to "close enough" — classify it or drop it with a reason.
@@ -144,7 +144,7 @@ This agent (L1) is one of six defense-in-depth layers hardening `/sc:reflect` Wa
 1. **L1b (ClaudeProcess restricted profile) — ranked ABOVE L1.** L1b is the only **unattended / no-operator** surface: the Tier-1 audit child and the adversarial scorer are launched headless via `ClaudeProcess --dangerously-skip-permissions --tools default`, so a mutation there happens with no human in the loop to catch it. It is the residual risk #2 surface and therefore the highest-blast-radius layer.
 2. **L1 (this agent — restricted read-only `tools:` allowlist).** Closes the original incident vector: the Wave-3 reviewer personas (`quality-engineer`/`root-cause-analyst`/`refactoring-expert`) carry no `tools:` line and inherit Bash/Edit/Write/Task. This agent's allowlist makes mutation mechanically impossible for the heterogeneous reviewers.
 3. **L2 (reviewer-isolation snapshot gate)** — grounds reviewers in an isolated `git worktree` snapshot so even an unexpected write lands in a throwaway, not the audit target.
-4. **L3 (§6.1.1 no-mutation denylist)** — defense-in-depth on the `execute_shell_command`/serena path (NOT the incident vector, which traveled the Bash-tool/L1 path).
+4. **L3 (§6.1.1 no-mutation denylist)** — defense-in-depth on the orchestrator's own Bash verification call (NOT the incident vector, which traveled the reviewer-persona Bash-tool/L1 path).
 5. **L4 (advisory READ-ONLY brief + rotation repoint)** — human-readable backstop documenting the read-only contract and pointing the rotation at this fixed restricted agent.
 6. **L5 (static + dynamic graders)** — regression guards proving the allowlist holds and (deferred) that no reviewer emits a mutation.
 
diff --git a/src/superclaude/agents/reuse-auditor.md b/src/superclaude/agents/reuse-auditor.md
--- a/src/superclaude/agents/reuse-auditor.md
+++ b/src/superclaude/agents/reuse-auditor.md
@@ -2,7 +2,7 @@
 name: reuse-auditor
 description: Independent reuse/consolidation auditor. For each new or proposed component, fingerprints its behaviour, searches the repo for prior art (name-agnostic), scores a composite similarity signal, and returns reuse findings with a verdict (reuse-by-import | mirror-shape | extract-shared | distinct) + consolidation recommendation. Detection only — never classifies deviations or gates. Reusable by any skill (sc:reflect, /tdd, cleanup-audit, analyze, code-review).
 category: analysis
-tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval, mcp__serena__find_symbol, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols
+tools: Read, Grep, Glob, mcp__auggie__codebase-retrieval
 model: sonnet
 maxTurns: 50
 permissionMode: plan
@@ -51,10 +51,10 @@ For each candidate, build a six-facet fingerprint:
 
 | Facet | Captures | Extracted via |
 |---|---|---|
-| F1 I/O skeleton | read→transform→write data-flow shape | `get_symbols_overview` + Read body |
+| F1 I/O skeleton | read→transform→write data-flow shape | Grep for the file's definitions + Read body |
 | F2 idempotency idiom | guard-then-mutate pattern (`dedup`, `not in`, `startswith("---`) | Grep body |
 | F3 persistence target | artifact read/written | Read body, resolve path |
-| F4 call-graph role | when in the pipeline it fires | `find_referencing_symbols` |
+| F4 call-graph role | when in the pipeline it fires | Grep with a word-boundary pattern for the symbol, then Read the call sites |
 | F5 trust rationale | *why* it exists | docstring / lead comment |
 | F6 domain nouns | entities operated on (verbs stop-listed out) | tokenize identifiers |
 
@@ -128,7 +128,7 @@ For each candidate build a **capability-keyed** auggie query from F1/F4/F5 — d
 ### 8. Cost control + graceful degradation
 
 - **Scope:** candidates only (caller-scoped, ≤12/run incl. new files/modules), never the whole tree. Overflow → `sampled: true`.
-- **auggie-unavailable (fail-open, NEVER STOP):** fall back to serena `find_symbol` by capability tokens + ripgrep skeleton grep; compute C_cap/C_shape from structure only (renormalize, drop C_aug); **cap every finding at advisory (tier ≤ maybe-related — a weaker substrate may never produce a hard `confident-duplicate`)**; set `degraded: ["neighbour-search:auggie_unavailable"]`.
+- **auggie-unavailable (fail-open, NEVER STOP):** fall back to Grep by capability tokens + skeleton grep; compute C_cap/C_shape from structure only (renormalize, drop C_aug); **cap every finding at advisory (tier ≤ maybe-related — a weaker substrate may never produce a hard `confident-duplicate`)**; set `degraded: ["neighbour-search:auggie_unavailable"]`.
 - **Evidence discipline:** re-Read every neighbour at its `file:line` before citing it. A hit that does not survive re-Read is discarded (`reuse_hit_unverified`) and routed to Grounding Gap. **No finding without a live citation.**
 
 ## Output Format — `reuse-audit.yaml`
diff --git a/src/superclaude/commands/reflect.md b/src/superclaude/commands/reflect.md
--- a/src/superclaude/commands/reflect.md
+++ b/src/superclaude/commands/reflect.md
@@ -103,10 +103,8 @@ This path calls `superclaude.pr_submit.contract_setup`, prints readiness/blocker
 | `--no-mcp` | `false` | Native-tools-only mode; warns and auto-degrades grounding quality. |
 | `--no-evidence-validator` | `false` | Skip the final evidence-validator gate (debug only — auto-warns; report records the skip in Grounding Gaps). |
 | `--no-doc-discovery` | `false` | Skip Wave 1.5 documentation grounding (records the skip in Grounding Gaps). |
-| `--no-verify` | `false` (UC-2) | Disable the UC-2 verification triangle (`execute_shell_command` scoped non-mutating tests/linters/type-checkers/build, §6.1 step 5.5). Default-on; when set, degrades §10.4 Regression detection to the task-log claim with a Grounding Gap entry. Subsumes the deprecated `--rerun-tests` alias. |
+| `--no-verify` | `false` (UC-2) | Disable the UC-2 verification run (Bash, scoped non-mutating linters/type-checkers/tests/build under the §6.1.1 envelope, §6.1 steps 5 and 5.5). Default-on; when set, degrades §10.4 Regression detection to the task-log claim with a Grounding Gap entry. Subsumes the deprecated `--rerun-tests` alias. |
 | `--no-reachability` | `false` (UC-2) | Disable the §6.1 step-5.6 contracted-sink reachability & oracle-admissibility gate (the operator rollback path). Default-on; when set, records telemetry-only skip state (`reachability_gate_ran: false`, `reachability_skip_reason: --no-reachability`); it does NOT write a Grounding Gap, set needs_human_decision, or force status: partial. |
-| `--onboard` | `false` | Opt-in one-shot Serena `onboarding` bootstrap at Wave 0.7b — runs ONLY when `list_memories` is empty for the project slug; seeds the §6.3 cold-start calibration baseline. Never creates `.serena/` implicitly. |
-| `--with-hierarchy` | `false` | Opt-in `type_hierarchy` transitive supertype/subtype retrieval (§6.1 step 4.5, Wave 1B.3). Backend-gated (`jetbrains` only; default OFF on `lsp`, unavailable on `none`); non-OO codebases see zero change. |
 | `--remediate` | `false` | After the audit ships, offer the Tier 3 remediation chain. Default (plan route): `sc:workflow` builds the tasklist package `.dev/tasks/to-do/<slug>/<slug>.md` (its built-in `--mode pre` review is surfaced) → operator runs `/sc:implement <pkg>/<slug>.md` → `/sc:reflect --mode post` re-runs as the post-commit gate. With `--depth deep` (MDTM route): `task-builder` → operator runs `/task` → `/sc:reflect --mode post`. `--depth deep` alone does NOT remediate; the route follows the depth you requested, not the tier reached. |
 | `--budget-remaining` | (none) | Caller-side budget hint (typically `TurnLedger.available()` from a sprint context). When provided, reflect cross-checks against the §15 cost profile and may auto-degrade tier; emits `budget_forced_tier_downgrade: true` in the contract. |
 | `--no-promote` | `false` (UC-2) | Suppress Wave 7 promotion. Default behavior: when the §14.5.2 strict gate passes, the validated work-unit folder moves to its `done` destination. |
@@ -141,7 +139,7 @@ The full multi-wave protocol lives in the skill. The command file performs only:
 
 | Tier | When | What it does | Approx cost |
 |------|------|--------------|------------|
-| Tier 1 | Always (unless STOP) | Single grounded card from `root-cause-analyst` + `confidence-calibrator`, with auggie/serena grounding. | ~3-6k Claude tokens, 1-3 min |
+| Tier 1 | Always (unless STOP) | Single grounded card from `root-cause-analyst` + `confidence-calibrator`, with auggie plus native Grep/Read grounding. | ~3-6k Claude tokens, 1-3 min |
 | Tier 2 | Auto-escalate on calibrated confidence < threshold, multi-domain, or `--depth deep` / `--tier 2` | 2-3 heterogeneous reviewers (different model classes) fan out in parallel; each card is independently calibrated; competing verdicts merged via `sc:adversarial-protocol`; `evidence-validator` drops unfounded citations. | +15-60k tokens, +4-15 min |
 | Tier 3 | Opt-in via `--remediate` AND user accepts | `--remediate`: `sc:workflow` produces the tasklist package `<slug>.md`; operator runs `/sc:implement <pkg>/<slug>.md` themselves; `/sc:reflect --mode post` re-runs as the post-commit gate. `--remediate --depth deep`: `task-builder` produces an MDTM remediation task file; operator runs `/task` themselves; `/sc:reflect --mode post` re-runs as the gate. | +20-40k tokens, +5-10 min |
 
@@ -155,7 +153,6 @@ Do NOT proceed with protocol execution using only this command file. The full be
 ## MCP Integration
 
 - **Auggie** (primary, free retrieval): Wave 0-2 codebase grounding via `mcp__auggie__codebase-retrieval`. Offloads heavy retrieval to the free tier, keeping Claude tokens tight.
-- **Serena**: Wave 0-6 symbol-level navigation (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, plus `find_declaration` / `find_implementations` / `type_hierarchy` for declaration-anchored and polymorphic grounding), the UC-2 §6.1 step-5.5 verification triangle (`get_diagnostics_for_file` / `execute_shell_command` / `summarize_changes`; `--no-verify` disables), opt-in `onboarding` cold-start bootstrap (`--onboard`), and the `think_about_*` checkpoint triad as one of several signals (NOT the sole reflection mechanism — see §6.4 fail-open policy).
 - **Context7**: Tier 2 only; consulted when the spec/diff references a framework or library by name.
 - **Tavily**: Tier 2 only; rate-limited; used for external-symptom lookups when documentation grounding can't resolve a deviation.
 - **Native reasoning**: Tier 2 synthesis when reconciling competing reviewer verdicts before the merge.
@@ -163,12 +160,8 @@ Do NOT proceed with protocol execution using only this command file. The full be
 ## Tool Coordination
 
 - **`mcp__auggie__codebase-retrieval`**: in-repo grounding (all waves)
-- **`mcp__serena__find_symbol` / `find_referencing_symbols` / `get_symbols_overview`**: symbol navigation
-- **`mcp__serena__find_declaration` / `find_implementations`**: diff-hunk → canonical declaration site (§6.1 step 2a, FR-2) and polymorphic implementor surface (§6.1 step 3b, FR-1)
-- **`mcp__serena__type_hierarchy`**: transitive supertype/subtype family (§6.1 step 4.5, Wave 1B.3) — backend- and `--with-hierarchy`-gated; fail-open when unavailable
-- **`mcp__serena__get_diagnostics_for_file` / `execute_shell_command` / `summarize_changes`**: UC-2 §6.1 step-5.5 verification triangle (LSP issues + scoped non-mutating tests/linters/type-checkers + change summary) feeding §10.4 Regression detection; `--no-verify` disables
-- **`mcp__serena__onboarding`**: opt-in cold-start memory bootstrap at Wave 0.7b (`--onboard`, default OFF)
-- **`mcp__serena__think_about_*`**: checkpoint signals (§6.4) — three-row table feeds the merge, never the sole verdict
+- **`Grep` then `Read`**: symbol navigation floor — Grep for the definition (`def <name>|class <name>|function <name>`) then Read the range (§6.1 steps 2a/3, FR-2); Grep with a word-boundary pattern for references, then Read the call sites (step 4); best-effort Grep for `class .*\(<Base>\)` / `implements <Iface>` for the polymorphic implementor surface (step 3b, FR-1)
+- **`Bash` (verification run)**: UC-2 §6.1 step 5 / 5.5 — the project's own linter or type-checker plus scoped non-mutating tests/build, run under the §6.1.1 safety envelope (timeout, output cap, verb allowlist, mutation denylist) and feeding §10.4 Regression detection; `--no-verify` disables
 - **Read / Write / Edit on `docs/memory/reflect/deviation-patterns-<slug>.md`**: cross-session learning capture (§6.3 — 20-entry, 90-day retention); a tracked project file, no MCP server needed
 - **`mcp__context7__resolve-library-id` / `query-docs`**: external library grounding (Tier 2)
 - **`mcp__tavily__tavily_search`**: targeted web search (Tier 2, rate-limited)
@@ -278,7 +271,6 @@ Do NOT proceed with protocol execution using only this command file. The full be
 - Trust agent-reported confidence without re-grading via `confidence-calibrator` (single-model self-grading is structurally biased per Mehta, Towards-AI Mar-2026)
 - Ship a REPORT.md whose `file:line` citations have not passed through `evidence-validator` (or its documented fallback when `--no-evidence-validator` is set)
 - Seat a reviewer whose model class collides with the calibrator's model class (Khan ICML 2024 disjoint-set rule — enforced by the `refs/reviewer-spec.md` rotation logic)
-- Use the Serena `think_about_*` triad as the sole reflection mechanism (the v1 failure mode) — they are checkpoint signals only; the protocol applies §6.4 fail-open policy
 - Auto-execute the Tier 3 remediation chain on either route — `sc:workflow` produces a tasklist package and the operator runs `/sc:implement` themselves; `task-builder` (`--depth deep`) produces a task file and the operator runs `/task` themselves; the skill never runs `/sc:implement` or `/task`
 - Auto-commit after Tier 3 — `/sc:reflect --mode post` is the post-commit gate the operator re-runs
 - Mutate filesystem for promotion when `--promote-dry-run` is set
diff --git a/tests/cli/reflect/test_marker_suppression.py b/tests/cli/reflect/test_marker_suppression.py
--- a/tests/cli/reflect/test_marker_suppression.py
+++ b/tests/cli/reflect/test_marker_suppression.py
@@ -98,13 +98,13 @@ def test_marker_two_does_not_suppress(
     _assert_not_suppressed(cli_runner, temp_tasklist, make_claude_process_stub)
 
 
-def _extract_execute_shell_command_envelope(text: str) -> str:
-    """Extract the §6.1.1 execute_shell_command safety-envelope section.
+def _extract_verification_envelope(text: str) -> str:
+    """Extract the §6.1.1 Bash verification safety-envelope section.
 
     Uses stable heading anchors: the section starts at the §6.1.1 heading and
     ends at the next §6.2 heading.
     """
-    start = text.index("### 6.1.1 `execute_shell_command` safety envelope")
+    start = text.index("### 6.1.1 Bash verification safety envelope")
     end = text.index("### 6.2", start)
     return text[start:end]
 
@@ -127,7 +127,7 @@ def test_verification_envelope_strips_reflect_wrapper_marker() -> None:
     an env dict that omits the marker).
     """
     text = _REFLECT_SKILL_SRC.read_text(encoding="utf-8")
-    envelope = _extract_execute_shell_command_envelope(text)
+    envelope = _extract_verification_envelope(text)
     # The envelope must explicitly account for the recursion-breaker marker...
     assert _MARKER in envelope
     # ...as a concrete env-strip command prefix, not vague prose.
diff --git a/tests/cli/reflect/test_reviewer_finding_parity.py b/tests/cli/reflect/test_reviewer_finding_parity.py
--- a/tests/cli/reflect/test_reviewer_finding_parity.py
+++ b/tests/cli/reflect/test_reviewer_finding_parity.py
@@ -29,9 +29,7 @@ _CONTROL = _CASES / "uc2-surface-positive-control"
 
 # The restricted reviewer tool set under test.
 _RESTRICTED_TOOLS = frozenset({"Read", "Grep", "Glob"})
-_REMOVED_TOOLS = frozenset(
-    {"Bash", "Edit", "Write", "NotebookEdit", "Task", "execute_shell_command"}
-)
+_REMOVED_TOOLS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})
 
 
 def _expected(case_dir: Path) -> dict:
diff --git a/tests/cli/reflect/test_reviewer_readonly_tools.py b/tests/cli/reflect/test_reviewer_readonly_tools.py
--- a/tests/cli/reflect/test_reviewer_readonly_tools.py
+++ b/tests/cli/reflect/test_reviewer_readonly_tools.py
@@ -4,7 +4,7 @@ Static guard for the reflect-reviewer agent (L1). Reads the SOURCE agent file
 ``src/superclaude/agents/reflect-reviewer.md`` (never the ``.claude/`` mirror, per
 SoT discipline) and asserts its ``tools:`` allowlist is present, non-empty,
 contains the read-only core (Read/Grep/Glob), and intersects the mutator set
-{Bash, Edit, Write, NotebookEdit, Task, execute_shell_command} EMPTY.
+{Bash, Edit, Write, NotebookEdit, Task} EMPTY.
 
 A negative fixture (a reviewer persona with the ``tools:`` line stripped, under
 ``tests/cli/reflect/fixtures/reviewer-personas/``) proves the SAME guard helper
@@ -27,9 +27,7 @@ _FIXTURE_DIR = Path(__file__).resolve().parent / "fixtures" / "reviewer-personas
 _NO_TOOLS_FIXTURE = _FIXTURE_DIR / "reviewer-persona-no-tools.md"
 
 # Mutator tools that MUST NOT appear in a read-only reviewer allowlist.
-_MUTATORS = frozenset(
-    {"Bash", "Edit", "Write", "NotebookEdit", "Task", "execute_shell_command"}
-)
+_MUTATORS = frozenset({"Bash", "Edit", "Write", "NotebookEdit", "Task"})
 # Read-only core that MUST be present.
 _REQUIRED_READONLY = frozenset({"Read", "Grep", "Glob"})
 
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
