# sc:reflect UC-1 report: Phase 3 codegraph adoption plan

- Plan: `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` (cited `plan:N`); spec: `source.md` in the same package (cited `source.md:N`).
- Mode pre (UC-1); tier reached 2 (forced by `coverage_degraded: parsed-sparse`; calibrated T1 C = 0.60 also escalates by rule 6).
- Reviewers: sonnet/analyzer (calibrated 0.73), haiku = glm-5.3/qa (calibrated 0.67); executor opus excluded; calibrator opus (disjoint from reviewers).
- Merge: `/sc:adversarial` (`adversarial/merged-verdict.yaml`), convergence 1.00, verdict refactor, 19 findings (0 critical, 9 important, 10 minor).
- Coverage: 119 inferred requirement rows, 72 matched by containment (`coverage_pct_union` 0.605), 47 covered by reference (`artifacts/unmapped-triage.yaml`), 0 unmapped after triage.

## Deviations

### Deviation M-01 (Necessary deviation, important, inherited-from-spec)

- Plan: plan:218, :221; spec: source.md:288; merged from R1-01, INV-001.
- Claim: `/sc:pr-submit` has no `--body-file` flag. It takes `--body` only (`src/superclaude/commands/pr-submit.md:8,26,54`). Its skill puts that value in double quotes in `gh pr create … --body "…"` (`sc-pr-submit-protocol/SKILL.md:189`), so a Markdown body passed inline would shell-expand backticks and `$`.
- Fix: Task 14 passes a plain placeholder, `--body "Phase 3 codegraph adoption for issue 323; full description follows."` (no backtick, `$`, `"` or `\`). After `/sc:pr-submit` returns, run `gh pr edit <n> --repo IronbellyOrg/IronClaude --body-file .dev/codegraph-migration/progress/P3-pr-body.md`. Add the acceptance check `gh pr view <n> --repo IronbellyOrg/IronClaude --json body -q .body \| diff - .dev/codegraph-migration/progress/P3-pr-body.md` prints nothing. Log the departure from source.md:288.

### Deviation M-02 (Drift, important, plan-only)

- Plan: plan:218, :223, :26; spec: source.md:288 (`<body>`); `~/.claude/CLAUDE.md` Core rule 4; merged from R1-02.
- Claim: `./artifacts/pr-body.md` is in the project-root `artifacts/` folder, which is never staged and not gitignored (`git check-ignore` exits 1). It leaves a stray `??` file that breaks plan:26's "only that task's files" rule.
- Fix: Write the body to `.dev/codegraph-migration/progress/P3-pr-body.md` and stage it in the Task 14 commit.

### Deviation M-03 (Regression, important, inherited-from-spec)

- Plan: plan:187, :190; spec: source.md:286; merged from R1-03, INV-012.
- Claim: Task 12 adds `/sc:graph` and `/sc:impact` rows to the `other-commands` table. `tests/core/test_how_we_work_routing_table.py:294` asserts `members == _OTHER_COMMANDS`, a fixed set of 9 names (`:27-37`), and no task edits it. The same file requires ASCII-only guide lines (`:339-344`).
- Fix: Task 12 adds `"sc:graph"` and `"sc:impact"` to `_OTHER_COMMANDS` in the same commit and lists that test file. Write both rows in ASCII only.

### Deviation M-04 (Necessary deviation, important, inherited-from-spec)

- Plan: plan:37, :43, :210; spec: source.md:271, :287; merged from R1-04, R2 advisory note, INV-007.
- Claim: Baseline (b) runs fewer paths than the Task 13 (8) union. It omits `tests/recommend/test_routing_refresh.py`, `tests/sc-roadmap`, `tests/roadmap/test_threshold_registry.py` and `tests/cli/test_how_we_work_install.py`. An existing failure there reads as new, which sends the run into the plan:202 fix loop and then H3.
- Fix: In Constraints, define one test-path set: baseline (b) paths plus those four. Task 1 (b) and Task 13 (8) both run it through the source.md:271 pipeline. Task 1 also asserts the baseline (b) pass count is above 0. Log the departure.

### Deviation M-05 (Drift, important, plan-only)

- Plan: plan:22 vs :67; spec: source.md:237, :337; merged from R1-05.
- Claim: The stop-and-escalate "Never" list forbids changing "any installer". Task 3 must edit `KNOWN_CORE_FILES` in `src/superclaude/cli/install_core.py`. source.md:337 has no such ban.
- Fix: Reword plan:22 to "never change `src/superclaude/cli/install_codegraph.py` or other Phase 2 installer modules; Task 3's `KNOWN_CORE_FILES` entry in `install_core.py` is the one exception".

### Deviation M-06 (Necessary deviation, important, inherited-from-spec)

- Plan: plan:20, :21, :37, :44, :45; spec: source.md:319-321; merged from R1-06, INV-002, INV-003.
- Claim: `git ls-files .dev/codegraph-migration` prints nothing and the plan package is untracked, so an `origin/master` worktree lacks the plan, `source.md` and every reference input. Creating the worktree inside Task 1 also splits `/sc:implement` state: the ledger `<package>/progress.md` and the Q0/Q2 snapshots stay in the starting checkout (`sc-implement-protocol/SKILL.md:64, :110-121`).
- Fix: Add a setup step before `/sc:implement` starts: (1) create the worktree per plan:20; (2) bring in the package and the `.dev/codegraph-migration/` inputs, either committed to `master` first or copied in; (3) start `/sc:implement <worktree>/.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md` from the worktree root. Task 1 then asserts that `git rev-parse --show-toplevel` is that worktree and that the package's realpath is inside it. It checks that the package, `source.md` and the inputs exist; if any is missing, escalate and never reconstruct. Its commit stages every copied-in path by exact path.

### Deviation M-07 (Necessary deviation, important (R2 dissent: minor), inherited-from-spec)

- Plan: plan:202, :211; spec: source.md:287 (9), :349 (H5); merged from R1-07.
- Claim: Check (9) runs the new `/sc:graph` and `/sc:impact` in the executor's running session, which may not load commands added mid-session by `make sync-dev`. Spec T11 requires "all of (1)-(9) pass", so a miss lands in the fix loop and then H3. The guide itself still resolves through the labelled fallback (source.md:247).
- Fix: Run check (9) in a fresh `claude` session started in the worktree after `make sync-dev`. Record that `~/.claude/CODEGRAPH.md` is absent and the guide resolved through the labelled fallback. If no fresh session can start, use H5 (extend H5 to T11 (9)) and log it.

### Deviation M-08 (Drift, important, plan-only)

- Plan: plan:218, :221, :223, :224, :27; spec: source.md:269, :288, :296-300, :307; merged from R1-08 (part 1), R2-05, INV-008, INV-009.
- Claim: Task 14 commits and then requires "no tracked change afterwards". It then posts comment G and logs the URL in the tracked decision log, so that check cannot pass. The push after the monitor finishes is not watched by CI or review. A pre-PR rebase rewrites the SHAs that comments 0-F cite and makes Task 13's results stale. The commit itself departs from source.md:288, but :269 requires it.
- Fix: Task 14 order: (1) Pre-PR checks; if a rebase happens, re-run Task 13 checks (1)-(8) and note old→new SHA pairs for comment G. (2) `/sc:pr-submit` (M-01), then `gh pr edit` with the body file. (3) Write and post the addendum. (4) Write `P3-G.md` and post comment G with the PR and addendum links. (5) Record all URLs in the decision log. (6) Make one commit, `docs(codegraph): record PR and Coder addendum links`, with the addendum, `P3-G.md`, `P3-pr-body.md`, the decision log and `.dev/tasks`. (7) `git push origin feat/codegraph-adoption`. (8) Run `/sc:pr-submit --monitor 3 --pr <n>` and apply the plan:221 checks criterion to that run. (9) `git status --short` prints nothing. Log the commit as a departure from source.md:288, justified by :269.

### Deviation M-09 (Drift, minor, plan-only)

- Plan: plan:26, :58; spec: source.md:269; merged from R1-08 (part 2), R1-14.
- Claim: plan:26 drops the spec's `git add .dev/codegraph-migration/progress .dev/codegraph-migration/decisions`. No commit list names the group-comment bodies or the URL rows written after each group commit. Task 2's "only" list also omits `.dev/tasks`.
- Fix: Add `git add .dev/codegraph-migration/progress .dev/codegraph-migration/decisions` to the per-task commit rule in Constraints. Task 2's commit says "plus `.dev/tasks`".

### Deviation M-10 (Necessary deviation, minor, inherited-from-spec)

- Plan: plan:122; spec: source.md:129, :281; merged from R1-09.
- Claim: Task 7 lists `commands/task.md` and its twin as "(metadata only)", but row 40 adds `codegraph` to no task file, so the change is undefined. `task.md:6` `mcp-servers:` gets only Phase 1's `serena` strip.
- Fix: Task 7 marks `commands/task.md` and its twin as verify-only (`serena` gone, nothing added), or drops them.

### Deviation M-11 (Necessary deviation, minor, inherited-from-spec)

- Plan: plan:122, :187; spec: source.md:123, :210, :286; merged from R1-10.
- Claim: sc-task-protocol STRICT step 7 is edited twice: Task 7 adds an inline `codegraph_impact` (row 34) and Task 12 adds a `/sc:impact` call (T10). No rule says which wins. Task 7 also never adds the codegraph names it calls to `allowed-tools` (source.md:63).
- Fix: Task 12's `/sc:impact` call replaces Task 7's inline STRICT step 7 text. Task 7 adds the exact `mcp__codegraph__codegraph_*` names its STANDARD and STRICT text calls to sc-task-protocol `allowed-tools`.

### Deviation M-12 (Authorized expansion, minor, plan-only)

- Plan: plan:177; spec: source.md:285; merged from R1-11, INV-013.
- Claim: The plan's added check `git diff --name-only HEAD -- src/superclaude/cli/reflect/contract.py` sees only uncommitted edits. It misses a `contract.py` change committed earlier in Phase 3.
- Fix: Use `git diff --name-only "$(git merge-base HEAD origin/master)" -- src/superclaude/cli/reflect/contract.py`; it must print nothing.

### Deviation M-13 (Necessary deviation, minor, inherited-from-spec)

- Plan: plan:67, :71; spec: source.md:255, :257, :277; merged from R1-12, INV-011.
- Claim: The sentinel scan covers `plugins/superclaude`, where the guide's byte copy holds the sentinel. Spec guide text such as "no primitive runs `codegraph sync`" (source.md:255) and prose such as "codegraph index" put a banned verb after `codegraph ` outside the "Never" section.
- Fix: Exclude both guide copies from the sentinel scan. Outside "Never", never put `index`, `sync`, `uninit`, `unlock`, `upgrade`, `install` or `uninstall` after `codegraph `, even as a noun (write, for example, "the index" or "no primitive syncs the index, see Never").

### Deviation M-14 (Authorized expansion, minor, inherited-from-spec)

- Plan: plan:207; spec: source.md:287 (2); merged from R1-15, INV-010.
- Claim: `<baseline (a) from the decision log>` cannot be copied and run as written, and `-eq` fails on a harmless decrease. The `grep -v` filter correctly drops the labelled fallback lines.
- Fix: Use `N=<baseline (a) value>; test "$(…)" -le "$N"`, log any decrease, and add one note that the filter drops the labelled fallback lines.

### Deviation M-15 (Necessary deviation, minor, inherited-from-spec)

- Plan: plan:67; spec: source.md:224, :197; DES:478, :144, :456; merged from R2-01 (fix corrected).
- Claim: No task carries source.md:224's rule for primitives' `graph:not_initialized` message. The spec says the message names `/sc:graph init`; DES:478 says `/sc:graph status`. DES wins (source.md:197; overrides (a)-(e) do not cover it).
- Fix: In Task 3's degraded-token section, write: "On `graph:not_initialized`, tell the user to run `/sc:graph status`; it reports `next_action: run_graph_init`." Add one assertion to `tests/core/test_codegraph_guide.py`.

### Deviation M-16 (Drift, minor, inherited-from-spec)

- Plan: plan:122, :162; spec: source.md:129, :281, :284; merged from R2-02 (narrowed).
- Claim: Row 40 adds `codegraph` to reflect's `mcp-servers:`. Neither spec T5/T8 nor plan Tasks 7/10 assigns `src/superclaude/commands/reflect.md:6` or `plugins/superclaude/commands/reflect.md:6`, and Task 7 names reflect without holding that file. Troubleshoot is covered by row 13 (Task 6). The new commands get it from DES:88, :110, :274, :292.
- Fix: Task 10 adds `codegraph` to `mcp-servers:` in both reflect.md files, after Phase 1's `serena` strip. Task 7 limits row 40 to its own files.

### Deviation M-17 (Drift, minor, plan-only)

- Plan: plan:37, :41; spec: source.md:27, :30, :32; merged from R1 calibrator note (U-012), INV-004, INV-005.
- Claim: plan:37 sends G1-G4 failures to H1 and silently drops source.md:30's rule that T1-T10 may continue while G3 fails. Stopping is the safe reading: E-6 and the MCP part of E-1 would measure the wrong registration, and Tasks 3 and 5 consume them. A G5 failure has no route.
- Fix: On a G3 failure, Task 1 runs E-2, E-3, E-7 and the CLI part of E-1, then stops at H1, and logs the departure from source.md:30. On a G5 failure, restart once in a fresh session in the worktree, then H1.

### Deviation M-18 (Drift, minor, plan-only)

- Plan: plan:142, :212; spec: source.md:282, :287; merged from R2-06, R2 calibrator note (U-016).
- Claim: Two commit messages differ from the spec. Task 8 says "manual init" where the spec says "user-typed init". Task 13 says "changelog, docs, sync and Phase 3 smoke results" where the spec says "sync dev copies and record Phase 3 smoke results". The plan's wider Task 13 commit list (`CHANGELOG.md`, `docs/`) is a correct necessary deviation, because the spec's T11 list omits files T11 edits.
- Fix: Use the spec's commit messages verbatim, or log the rewording as a self decision. Keep the widened Task 13 file list and log it.

### Deviation M-19 (Necessary deviation, important, inherited-from-spec)

- Plan: plan:82, :99, :114, :125, :165, :176, :190; spec: source.md:271, :278-286; merged from INV-006 (fault-finder; both advocates ACCEPT).
- Claim: Existing failures are "recorded, not fixed" (source.md:271), yet per-task criteria require whole directories to pass (`tests/core`, `tests/agents`, `tests/troubleshoot`, `tests/commands`, `tests/sc-roadmap`, `tests/skills`, `tests/cli/reflect`). One existing failure there makes Tasks 4-7 and 10-12 impossible, and each ends at H3.
- Fix: Each task's pytest criterion reads: "passes, or the failing ids from the source.md:271 pipeline on the same paths give no output from `comm -13 .dev/codegraph-migration/experiments/P3-baseline-failures.txt <task failures file>`". The baseline is taken over M-04's single path set.

## Inferred requirements (Pass 2)

| id | citation | match | quote |
|---|---|---|---|
| INF-001 | source.md:23 | by reference: Task 1 | \| G1 \| CLI on PATH at the pinned version \| `command -v codegraph && codegraph --version` and `PIN=$(uv run --no-sync python -c 'from superclaude.cli.install_ |
| INF-002 | source.md:24 | Task 2 (0.6316) | \| G2 \| MCP server registered at user scope \| `claude mcp list 2>/dev/null \\| rg -n '^codegraph:'` \| one line ending in `Connected` \| |
| INF-003 | source.md:25 | Task 1 (0.9455) | \| G3 \| The registered tool list equals Phase 2's constant \| `MT=$(uv run --no-sync python -c 'from superclaude.cli.install_codegraph import MCP_TOOLS; print( |
| INF-004 | source.md:26 | by reference: Task 1 | \| G4 \| This worktree is indexed \| if `mcp__codegraph__codegraph_status` is in the session's tool list, call it with `projectPath` = realpath of `git rev-pars |
| INF-005 | source.md:27 | by reference: Task 1 | \| G5 \| Session sees the tools \| in the executor's own Claude session's tool list \| seven-tool branch: contains `mcp__codegraph__codegraph_callers` and `mcp_ |
| INF-006 | source.md:28 | Task 1 (0.8718) | \| G6 \| Phase 1 landed and its slots ledger exists \| `rg -n 'mcp__serena__' src/superclaude plugins/superclaude commands agents` and `test -s .dev/codegraph-m |
| INF-007 | source.md:70 | Constraints (0.6) | 1. **Read before cite or edit.** A codegraph answer locates code; it is not a citation. |
| INF-008 | source.md:71 | Constraints (0.6579) | 2. **Fail open to the Phase 1 floor.** codegraph missing, unlisted, index missing, foreign or stale → use the step's Phase 1 floor (Grep/Glob/Read, `P1 §4.1` G2 |
| INF-009 | source.md:72 | by reference: Constraints | 3. **Empty is not absence.** Files over 1 MB, ignored files, dependency dirs and Markdown are not indexed (`EVAL §4`, §5.4), and callers are call edges only. |
| INF-010 | source.md:73 | by reference: Constraints | 4. **Agents get exact names and the run's state.** A read-only agent lists exact `mcp__codegraph__codegraph_<tool>` names (never `mcp__codegraph__*`) and only f |
| INF-011 | source.md:74 | Task 13 (0.7222) | 5. **No `explore`, no mutating CLI verb in a skill or agent.** No primitive names `codegraph_explore`, `codegraph explore` or `codegraph context`; no allowlist  |
| INF-012 | source.md:75 | Constraints (0.6429) | 6. **Both tool-list branches.** Primitive text is the same whichever value Phase 2 shipped (section 0 G3). |
| INF-013 | source.md:76 | Task 8 (0.7273) | 7. **Guard every CLI `status`.** Run CLI `codegraph status` only when `pgrep -f 'codegraph\.js (init\|index)'` prints nothing; when it prints a line, skip `stat |
| INF-014 | source.md:77 | Task 2 (0.6) | 8. **CLI binary.** A primitive calls the CLI as bare `codegraph` (that is what its exact `Bash(codegraph <verb> …)` allowlist entries match). |
| INF-015 | source.md:78 | Constraints (0.6333) | 9. **Tier above the floor.** Where Phase 1 left a floor (ledger action `floor`), the codegraph step is inserted before it and the floor text stays unchanged bel |
| INF-016 | source.md:90 | Task 4 (0.6203) | \| 1 \| `src/superclaude/core/CLAUDE.md` `## MCP Servers` table row and the `SUPERCLAUDE_CODEGRAPH_BEGIN/END` block \| `## MCP Servers` table; marked block \| P |
| INF-017 | source.md:91 | by reference: Task 4 | \| 2 \| `src/superclaude/core/CLAUDE.md:90` \| `S2.` trigger \| `Edit / Write / replace_content / replace_symbol_body / insert_*_symbol` \| `Edit / Write` \| de |
| INF-018 | source.md:92 | Task 4 (0.697) | \| 3 \| `src/superclaude/core/CLAUDE.md:112` \| `### Refresh-tool selection` \| Phase 1 G10 text: "Grep for the definition and references, then Read" \| "`codeg |
| INF-019 | source.md:93 | Task 4 (0.6) | \| 4 \| `src/superclaude/modes/MODE_Orchestration.md:24` \| `## Tool Selection Matrix` \| `\\| Symbol operations \\| Serena MCP \\| Manual search \\|` \| `\\| S |
| INF-020 | source.md:94 | by reference: Task 5 | \| 5 \| `src/superclaude/agents/troubleshoot-analyst.md:5` \| frontmatter `tools:` \| 4 `mcp__serena__*` names \| `mcp__codegraph__codegraph_search, mcp__codegr |
| INF-021 | source.md:95 | Task 5 (0.7241) | \| 6 \| `src/superclaude/agents/troubleshoot-analyst.md:27` \| `## Working rules` 1 \| "Use native search and the individually allowed read-only retrieval tools |
| INF-022 | source.md:96 | Task 10 (0.8) | \| 7 \| `src/superclaude/agents/reflect-reviewer.md:5` \| frontmatter `tools:` \| 4 `mcp__serena__*` names \| same 4 codegraph names as row 5 \| deleted, then f |
| INF-023 | source.md:97 | by reference: Task 5 | \| 8 \| `src/superclaude/agents/reuse-auditor.md:5` \| frontmatter `tools:` \| `find_symbol, get_symbols_overview, find_referencing_symbols` \| `mcp__codegraph_ |
| INF-024 | source.md:98 | Task 5 (0.6818) | \| 9 \| `src/superclaude/agents/reuse-auditor.md:54` \| `### 1. Capability Fingerprint` F1 \| `get_symbols_overview + Read body` \| `codegraph_node {file, symbo |
| INF-025 | source.md:99 | by reference: Task 5 | \| 10 \| `src/superclaude/agents/reuse-auditor.md:57` \| F4 call-graph role \| `find_referencing_symbols` \| `codegraph_callers` (definition lines; re-Read for  |
| INF-026 | source.md:100 | Task 5 (0.775) | \| 11 \| `src/superclaude/agents/reuse-auditor.md:131` \| `### 8. Cost control` auggie-unavailable \| Phase 1 G6 text: "Grep by capability tokens + skeleton gre |
| INF-027 | source.md:101 | by reference: Task 5 | \| 12 \| `src/superclaude/agents/auggie-reviewer.md:5,36,81,115` \| `tools:`, Responsibilities 2, tool list, freely-use list \| `mcp__serena__find_symbol`, `fin |
| INF-028 | source.md:102 | Task 6 (0.6226) | \| 13 \| `src/superclaude/commands/troubleshoot.md:3,6,52,75,89,96,173` \| description, `mcp-servers`, `--scope` row, Tier table, `## MCP Integration`, `## Tool |
| INF-029 | source.md:103 | Task 6 (0.6552) | \| 14 \| `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:4` \| frontmatter `allowed-tools` \| 3 `mcp__serena__*` names \| add `mcp__codegraph__codegra |
| INF-030 | source.md:104 | Task 6 (0.6562) | \| 15 \| same `:193` \| `### Wave 1` step 1, second bullet \| "`mcp__serena__get_symbols_overview` on the target file or `mcp__serena__find_symbol` on a specifi |
| INF-031 | source.md:105 | Task 6 (0.7436) | \| 16 \| same `:156,168,216,439,606,620` \| Wave 0 step 3, TARGET header, Wave 1 exit, failure table, tool matrix, Will-do \| "auggie/serena" \| "auggie/codegra |
| INF-032 | source.md:106 | by reference: Task 6 | \| 17 \| `.../sc-troubleshoot-protocol/refs/triage-checklist.md:11` \| `## Pre-investigation grounding` \| "The serena symbol overview / surrounding function de |
| INF-033 | source.md:107 | by reference: Task 6 | \| 18 \| `.../sc-troubleshoot-protocol/refs/diagnosability-audit.md:11` \| first paragraph \| mentions serena \| drop the word (auggie call stays) \| deleted \| |
| INF-034 | source.md:108 | Task 10 (0.8148) | \| 19 \| `src/superclaude/skills/sc-reflect-protocol/SKILL.md:5` \| frontmatter `allowed-tools` \| 20 `mcp__serena__*` names \| `mcp__codegraph__codegraph_statu |
| INF-035 | source.md:109 | by reference: Task 10 | \| 20 \| same `:340-345` \| `Step 1B.3` steps 1a, 1, 3, 3a \| `find_declaration`, `find_symbol`, `find_referencing_symbols`, `type_hierarchy` \| 1a `codegraph_n |
| INF-036 | source.md:110 | by reference: Task 10 | \| 21 \| same `:500-531` \| `## 6. Modern Serena Tool Usage` → rename `## 6. |
| INF-037 | source.md:111 | by reference: Task 10 | \| 22 \| same `:534-565` \| explanatory notes per step \| Serena-specific notes (`include_info`, LSP backends) \| rewrite each note to the new tool; delete note |
| INF-038 | source.md:112 | by reference: Task 10 | \| 23 \| same `:567-585` \| `### 6.1.1 execute_shell_command safety envelope` \| envelope for the Serena shell tool \| already retitled and applied to `Bash` by |
| INF-039 | source.md:113 | Constraints (0.6296) | \| 24 \| same `:634-636` \| `### 6.5 Fail-open policy` \| "Every Serena call is fail-open … `degraded: true`" \| "Every codegraph call is fail-open … add the ma |
| INF-040 | source.md:114 | by reference: Task 10 | \| 25 \| same `:1492` \| error table \| "Serena unavailable … `degraded: ["serena"]`" \| "codegraph unavailable, unlisted or index missing → Grep/Glob; add the  |
| INF-041 | source.md:115 | Task 10 (0.7143) | \| 26 \| same `:92`, `commands/reflect.md:109` \| `--with-hierarchy` flag \| opt-in `type_hierarchy` \| flag removed (P3-D6; no test or CLI pins it: `rg -n 'wit |
| INF-042 | source.md:116 | Task 11 (0.6111) | \| 27 \| `src/superclaude/cli/reflect/contract.py:32-34` (+ `tests/cli/reflect/test_verdict_mapping.py`) \| `_DEGRADED_COMPONENTS_HALT_SET` \| Phase 1 drops `se |
| INF-043 | source.md:117 | by reference: Task 10 | \| 28 \| `.../sc-reflect-protocol/refs/runtime-surface.md:21`, `coverage-mapping.md:173-195`, `reviewer-spec.md:14-55`, `deviation-taxonomy.md:50-83`, `reflecti |
| INF-044 | source.md:118 | by reference: Task 10 | \| 29 \| `src/superclaude/commands/reflect.md:144,158,166-172` \| Tier table, `## MCP Integration`, tool list \| Serena navigation + verification triangle tools |
| INF-045 | source.md:119 | by reference: Task 7 | \| 30 \| `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:4,129-130` and `commands/validate-roadmap.md:6` \| `allowed-tools`, MCP glossary \| `find |
| INF-046 | source.md:120 | by reference: Task 7 | \| 31 \| same `:318-349` \| `#### Step 0.5 — Symbol Context Supplement` \| activate + `find_symbol include_body=False` + `get_symbols_overview` \| step 2 delete |
| INF-047 | source.md:121 | by reference: Task 7 | \| 32 \| `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md:24-30`, `SKILL.md:57,193,387` \| `**Tier 2 (fallback_1)**` \| Serena `get_symbol |
| INF-048 | source.md:122 | Task 6 (0.6667) | \| 33 \| `src/superclaude/skills/sc-task-protocol/SKILL.md:103,309` \| STANDARD step 2, Tool Coordination execution 3 \| `find_referencing_symbols OR grep` \| ` |
| INF-049 | source.md:123 | by reference: Task 7 | \| 34 \| same `:88,91,287,303,315,319-320` \| STRICT steps 1, 4; `## MCP Integration`; Tool Coordination \| activate, memory, "STRICT: Serena (fallback not allo |
| INF-050 | source.md:124 | Task 7 (0.697) | \| 35 \| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:683` \| `### 5.5 MCP Tool Requirements` \| `\\| STRICT \\| Serena \\| Context7 \\| No \\|` \| `\\ |
| INF-051 | source.md:125 | by reference: Task 4 | \| 36 \| `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md:28` \| `### 1. Specialized capability` \| "YES (auggie/serena beats brute  |
| INF-052 | source.md:126 | by reference: Task 7 | \| 37 \| `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md:6,83` \| `mcp-servers`, `## MCP Integration` \| "Serena MCP: Import chain tracing during Ste |
| INF-053 | source.md:127 | Task 7 (0.6) | \| 38 \| `src/superclaude/commands/auggie-review.md:6,78`, `skills/sc-auggie-review-protocol/SKILL.md:10` \| `mcp-servers`, `## MCP Integration` \| "Serena: Sym |
| INF-054 | source.md:128 | by reference: Task 4 | \| 39 \| `src/superclaude/mcp/MCP_Auggie.md:16-37` \| comparison prose \| "Over Serena: broad recall, not symbol navigation" \| "Over codegraph: broad semantic  |
| INF-055 | source.md:129 | by reference: Task 7 | \| 40 \| `src/superclaude/commands/{cli-eval,brainstorm,release-split,adversarial,task,cleanup-audit,post-release,init-lite,cli-portify,pr-submit,review-transla |
| INF-056 | source.md:130 | by reference: Task 1 (G6) + Task 13 check (3) | \| 41 \| memory, activation and nudge rows (`PU` jobs `MEM`, `ACT`, `NUDGE`: pm-agent, `/sc:save`, `/sc:load`, `/sc:pm`, sc-pm-protocol, MODE_Task_Management, s |
| INF-057 | source.md:131 | by reference: Task 1 (G6) + Task 13 check (3) | \| 42 \| `src/superclaude/hooks/hooks.json:47`, `hooks/scripts/freshness-pre-edit.sh:25,36` \| PreToolUse matcher \| 4 `mcp__serena__*` edit tools \| `Edit\\|Wr |
| INF-058 | source.md:133 | Constraints (0.7073) | **Mirror rule.** For every row, apply the identical change to the tracked plugin twin under `plugins/superclaude/` when that file exists (`PU §5.7` lists which  |
| INF-059 | source.md:203 | Task 10 (0.7568) | \| Name and files \| `/sc:impact`; `src/superclaude/commands/impact.md` (thin; `## Activation` says `> Skill sc:impact-protocol`); `src/superclaude/skills/sc-im |
| INF-060 | source.md:205 | by reference: Task 9 | \| Inputs and flags \| `<symbol>...` (1-30 bare names) or `--diff [<base>]` (default `HEAD`; with a base, `git diff --merge-base <base>`); `--depth 1-3` (defaul |
| INF-061 | source.md:206 | by reference: Task 9 | \| Steps \| (1) validate; (2) readiness check (guide §2: kill switch, worktree root, `codegraph --version`, `codegraph_status` or guarded CLI `status`, listed-t |
| INF-062 | source.md:207 | Task 9 (0.6792) | \| Allowed tools (skill) \| `Read, Grep, Glob, Write, Bash(printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES), Bash(pgrep -f *), Bash(git rev-parse *), Bash(realpath *) |
| INF-063 | source.md:208 | by reference: Task 9 | \| Outputs \| `<output-dir>/impact.md` (12 fixed sections, `DES §4.e`) and `<output-dir>/return-contract.yaml`: `schema_version: 1`, `command: impact`, `status: |
| INF-064 | source.md:209 | by reference: Task 9 | \| Failure behaviour \| Never stops the caller. codegraph absent, switched off, not initialized, foreign index, or lookup tools unlisted with no usable CLI → Gr |
| INF-065 | source.md:210 | by reference: Task 12 | \| Callers (Phase 3 wires them in T10) \| sc-implement-protocol Q1 (rename/delete/signature tasks; warning and QA package input, never widens edits) and Q6 (`-- |
| INF-066 | source.md:217 | Task 8 (0.871) | \| Name and files \| `/sc:graph`; `src/superclaude/commands/graph.md` (thin; activates `> Skill sc:graph-protocol`; holds the only literal `codegraph init` call |
| INF-067 | source.md:219 | Task 8 (0.625) | \| Inputs and flags \| positional `status` (default) or `init`; `--worktree-local` (only with `init`, for a nested worktree that answers from the parent index,  |
| INF-068 | source.md:220 | by reference: Task 8 | \| Steps \| `status`: readiness check (guide §2), `codegraph telemetry status`, counts and pending list, `next_action` from a 9-row first-match table (`DES §2.c |
| INF-069 | source.md:221 | Task 8 (0.725) | \| Allowed tools \| command: `Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)`; skill: `Read, Write, Bash(codegraph --version), Bash(codegraph stat |
| INF-070 | source.md:222 | by reference: Task 8 | \| Outputs \| an 8-line screen report (`DES §2.e`); with `--output-dir`, `return-contract.yaml`: `schema_version`, `command: graph`, `subcommand`, `status`, abs |
| INF-071 | source.md:223 | by reference: Task 8 | \| Failure behaviour \| Never stops anything (no skill callers). codegraph absent → `index_state: absent`, `next_action: install_codegraph` ("run `./update.sh`" |
| INF-072 | source.md:224 | Task 12 (0.6087) | \| Callers \| Users. `/sc:load` prints one readiness line pointing to `/sc:graph status` (T10), and every primitive's `graph:not_initialized` fallback message n |
| INF-073 | source.md:229 | Task 9 (0.6087) | Following `tests/commands/test_research_command.py` style (content assertions, no network), the executor adds `tests/commands/test_impact_command.py` (18 tests, |
| INF-074 | source.md:233 | Task 13 (0.76) | **Decision (P3-D2): one core doc, `src/superclaude/core/CODEGRAPH.md`, installed to `~/.claude/CODEGRAPH.md`.** Every primitive points to it by the installed pa |
| INF-075 | source.md:254 | Constraints (0.7857) | 1. *What it is*: a read-only code graph of the current worktree, one SQLite index per worktree in `.codegraph/` (`EVAL §1`, §4). |
| INF-076 | source.md:255 | Constraints (0.7059) | 2. *Readiness check, once per run*: detect MCP from whether `mcp__codegraph__codegraph_status` is in the tool list (never from the kind of run); call it, or CLI |
| INF-077 | source.md:256 | by reference: Task 3 | 3. *Degraded tokens* (closed list; consumers invent none): `graph:absent`, `graph:unlisted`, `graph:disabled` (user set `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`;  |
| INF-078 | source.md:257 | Task 2 (0.7193) | 4. *Tool table*: section 1.1's job → tool rows, condensed to the seven MCP tools (`node`, `search`, `callers`, `callees`, `impact`, `files`, `status`; only `sta |
| INF-079 | source.md:258 | by reference: Task 3 | 5. *Standing rules*: the nine standing rules at the end of section 1.1, plus the call-site procedure: for a caller row that will be cited, Grep `\b<callee>\s*\( |
| INF-080 | source.md:259 | by reference: Task 3 | 6. *Known gaps and fallbacks*: no text search, no diagnostics, no type hierarchy, no implementations tool, no edits, no memory; caller lists are truncated at 20 |
| INF-081 | source.md:260 | by reference: Task 3 | 7. *Never* (the only section of the guide that may name these verbs; a T1 test checks it): call `explore` or `codegraph context`; use `codegraph_node` file mode |
| INF-082 | source.md:262 | by reference: Task 3 | Primitives then carry exactly one line, for example in `troubleshoot-analyst.md` Working rule 1: "For symbols and callers use the codegraph tools per `~/.claude |
| INF-083 | source.md:268 | Constraints (0.92) | - Run from the Phase 3 worktree root (section 7). Every `pytest` call names files or small directories and adds `-q -p no:cacheprovider`; never the whole suite  |
| INF-084 | source.md:269 | Constraints (0.9697) | - After every task: `git status --short` shows only the task's files (plus `.dev/` progress and decision files). Then `git add <those files> .dev/codegraph-migr |
| INF-085 | source.md:270 | Constraints (0.8182) | - Mirror rule (section 1.2) applies to every task: the plugin twin changes in the same commit. |
| INF-086 | source.md:271 | Task 1 (0.6933) | - Before T1, record two baselines in the decision log: (a) `grep -rIn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks} \| wc -l` (157 at HE |
| INF-087 | source.md:272 | Task 3 (0.6774) | - New tests follow the existing content-test style: a module docstring saying what drifts it guards, `_REPO = Path(__file__).resolve().parents[2]`, plain `read_ |
| INF-088 | source.md:276 | Task 2 (0.8152) | \| **T0** prerequisite experiments (no source edit) \| new `.dev/codegraph-migration/experiments/P3-T0/{E1-freshness,E2-help,E3-allowlist,E6-agent-matrix,E7-slo |
| INF-089 | source.md:277 | Task 3 (0.8667) | \| **T1** shared guide \| new `src/superclaude/core/CODEGRAPH.md`; new `plugins/superclaude/core/CODEGRAPH.md` (byte copy); `src/superclaude/cli/install_core.py |
| INF-090 | source.md:278 | Task 4 (0.8941) | \| **T2** core docs and routing hints \| `src/superclaude/core/CLAUDE.md` (rows 1, 3: Phase 2's codegraph row and marked block edited in place, the refresh-tool |
| INF-091 | source.md:279 | Task 5 (0.8933) | \| **T3** agents \| `src/superclaude/agents/{troubleshoot-analyst,reflect-reviewer,reuse-auditor,auggie-reviewer}.md` (no plugin twins exist: `ls plugins/superc |
| INF-092 | source.md:280 | Task 6 (0.9552) | \| **T4** troubleshoot \| `src/superclaude/commands/troubleshoot.md` + `plugins/superclaude/commands/troubleshoot.md`; `src/superclaude/skills/sc-troubleshoot-p |
| INF-093 | source.md:281 | Task 7 (1.0) | \| **T5** other skills and commands \| rows 30-38 and 40: `commands/validate-roadmap.md`, `skills/sc-validate-roadmap-protocol/SKILL.md`, `skills/sc-brainstorm- |
| INF-094 | source.md:282 | Task 8 (0.8143) | \| **T6** `/sc:graph` \| new `src/superclaude/commands/graph.md`; new `src/superclaude/skills/sc-graph-protocol/SKILL.md`; `tests/unit/test_cli_install.py` (bot |
| INF-095 | source.md:283 | Task 9 (0.9054) | \| **T7** `/sc:impact` \| new `src/superclaude/commands/impact.md`; new `src/superclaude/skills/sc-impact-protocol/SKILL.md`; `tests/unit/test_cli_install.py` ( |
| INF-096 | source.md:284 | Task 10 (0.9583) | \| **T8** reflect skill and command \| `src/superclaude/skills/sc-reflect-protocol/SKILL.md` and the 6 refs of row 28; `src/superclaude/commands/reflect.md` + ` |
| INF-097 | source.md:285 | Task 11 (0.9661) | \| **T9** reflect contract pin \| `tests/cli/reflect/test_verdict_mapping.py` (new `test_graph_tokens_do_not_halt`); new fixture `tests/cli/reflect/fixtures/deg |
| INF-098 | source.md:286 | Task 12 (0.9775) | \| **T10** wire callers and routing \| `src/superclaude/skills/sc-implement-protocol/SKILL.md` (+ byte-identical plugin twin `plugins/superclaude/skills/sc-impl |
| INF-099 | source.md:287 | Task 13 (0.76) | \| **T11** changelog, docs, sync, full verification, live smoke \| `CHANGELOG.md` (one entry for `/sc:impact`, `/sc:graph` and `~/.claude/CODEGRAPH.md`, review  |
| INF-100 | source.md:288 | Task 14 (0.875) | \| **T12** PR \| none \| Pre-PR checks from repo `CLAUDE.md` "PR Target = Fork" (remote and `gh repo view` show `IronbellyOrg/IronClaude`; rebase onto `origin/m |
| INF-101 | source.md:298 | Constraints (0.7895) | 1. Writes the comment body to `.dev/codegraph-migration/progress/P3-<group-letter>.md` (create the folder if absent; overwrite on a retry so the file is idempot |
| INF-102 | source.md:299 | Constraints (0.9474) | 2. Posts it: `gh issue comment 323 --repo IronbellyOrg/IronClaude --body-file .dev/codegraph-migration/progress/P3-<group-letter>.md` |
| INF-103 | source.md:300 | Constraints (0.8889) | 3. Records the returned comment URL in the decision log (section 7). |
| INF-104 | source.md:321 | Constraints (0.9429) | **Branch and worktree.** Start only after Phase 1 and Phase 2 are merged to `master` on `origin`. Create `git worktree add .dev/worktrees/codegraph-adoption -b  |
| INF-105 | source.md:325 | by reference: Constraints | - wording of replacement text, as long as it keeps the meaning in section 1.2 and stays within the row's anchor; |
| INF-106 | source.md:326 | Constraints (0.7857) | - which section 1.2 row a slots-ledger row maps to (T0 E-7), when the anchor makes it plain; |
| INF-107 | source.md:327 | Task 1 (0.6667) | - which tool-list branch applies (section 0 G3), read from Phase 2's constant; |
| INF-108 | source.md:328 | Constraints (0.8) | - adding a `codegraph` mention to a mirror file that differs from src (change the matching sentence only); |
| INF-109 | source.md:329 | by reference: Constraints | - fixing a test that pins old Serena text, when the fix only swaps the pinned token for the new one written in this spec; |
| INF-110 | source.md:330 | Task 2 (0.7778) | - running `codegraph init --yes` in its own worktree (gitignored `.codegraph/`, `EVAL §2`); |
| INF-111 | source.md:331 | by reference: Constraints | - an extra fallback line when a live codegraph answer is wrong in the T11 smoke (for example a missing caller), as long as the fallback is Grep/Read. |
| INF-112 | source.md:333 | Constraints (0.9242) | A mid-level choice (two or more viable options with real trade-offs that this spec does not settle) follows the orchestration README rule: write each option to  |
| INF-113 | source.md:335 | Constraints (0.9773) | **Decision log.** Append one row per decision to `.dev/codegraph-migration/decisions/P3X-execution-log.md` (create it as a header stub first): date, task, decis |
| INF-114 | source.md:337 | Constraints (0.9437) | **Never do (stop and escalate instead):** edit `~/.claude`, `~/.claude.json` or any MCP registration; run `superclaude install`, `./update.sh`, `claude mcp add/ |
| INF-115 | source.md:345 | by reference: Constraints | \| H1 \| Section 0 gate G1, G2, G3 or G4 fails after one `codegraph init` \| Fix the Phase 2 install or registration (for G3: make the registered `CODEGRAPH_MCP |
| INF-116 | source.md:346 | Task 14 (0.75) | \| H2 \| T12 (open the PR) \| Review and merge the PR on `IronbellyOrg/IronClaude`; the executor never merges \| |
| INF-117 | source.md:347 | by reference: Constraints | \| H3 \| A section 5 acceptance command still fails after two fix attempts and an adversarial-quick decision did not resolve it \| Read the logged failure and c |
| INF-118 | source.md:348 | Constraints (0.6) | \| H4 \| Phase 1 changed a primitive in a way that contradicts section 1.2 (for example it deleted a whole step this spec rewrites), section 0 G6 fails (Serena  |
| INF-119 | source.md:349 | Task 2 (0.72) | \| H5 \| T0 experiments E-3 or E-6 need a fresh or headless Claude session the executor cannot start \| Run the command written in the T0 row and paste the outp |

## Inferred-claim audit

No finding is tagged [INFERRED]; every claim cites plan or spec lines re-checked by the calibrators and the merge.

## Recommendations

Apply every merged finding's fix to the plan (the workflow brief says to fix plan defects by editing the generated plan); apply the inherited-from-spec fixes to the spec as well.

## Grounding Gaps (evidence-validator)

The evidence-validator re-read 105 of 107 citations and dropped 2; all 119 inferred-requirement rows matched their cited lines (0 dropped).

- **M-10, `task.md:6`, dropped (line mismatch).** `mcp-servers:` is on line 7 of `src/superclaude/commands/task.md` and of its plugin twin; line 6 is `allowed-tools:`. The finding still holds at line 7.
- **M-15, `DES:456`, dropped (snippet mismatch).** DES:456 says `/sc:impact`'s report names `/sc:graph init` for `not_initialized`, while DES:478 says the guide's message names `/sc:graph status` and DES:144 maps `not_initialized` to `run_graph_init`. The two DES lines govern different surfaces (the command report vs the guide); the fix keeps both.

## Input drift

None: the input tree hash recomputed at Wave 5 equals the Wave 0 snapshot (`artifacts/input-snapshot.yaml`).
