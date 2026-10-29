# FINAL-SUMMARY: independent final check of the three phase plans (task Q, issue #323)

Status: COMPLETE (task Q, 2026-10-29). Reviewer: task Q (did not produce any of the reviewed work). HEAD `55d40308`, branch `ironbelly/feat-codememory-codegraph-init`. Planning only: no source, test, doc or environment change; nothing staged or committed. The only files I changed are untracked planning files: this summary, the Phase 1 `source.md` snapshot, one sentence in the Phase 3 plan, and the two `progress.md` ledger pins.

**Result (after the Q2 re-check, 2026-10-29): Phase 1 PASS, Phase 2 PASS, Phase 3 PASS, Coder handoff PASS.** 0 findings open. Q-I1 and Q-I2 (IMPORTANT) were fixed by task X and independently re-verified by task Q2 (section "Re-check (Q2)" at the end); Q-M1 and Q-M2 (MINOR) were fixed in the first pass; 0 CRITICAL. Original first-pass result for the record: Phase 1 FAIL (Q-I1), Phase 3 FAIL (Q-I2), Phases 2 and handoff PASS. Coverage: all 205 files with a codebase-memory or Serena hit map to a Phase 1 row and plan task; 0 orphans.

## 0. Scope and method

Read in full: `orchestration/README.md`, `orchestration/task-specs/Q-final-check.md`, `review/review.md`, `review/F1-result.md`, `F2-result.md`, `F3-result.md`, the three task plans (271, 335 and 236 lines), both handoff files, the Phase 1 spec sections 1.0-1.2, 2, 4, 8, 9, 10 and its Decisions and Review resolution, the Phase 2 spec sections 2.4, 2.12, 3, 5 (task heads), 6-9 and its Decisions and Review resolution, the Phase 3 spec sections 0-7 and its Decisions and Review resolution, and every `## Decisions` section named in section 4. Not read line by line: the adversarial scratch folders under `decisions/*/adversarial/` (only their merged recommendations were opened), `brainstorm/`, and the Phase 1 spec rows S20-S100 / P1-P98 (checked mechanically, section 3).

Commands I ran (all read-only; `git status --short` showed no tracked file changed by me):
- the inventory searches of section 3 (`rg`, one `uv run --no-project python -I` script);
- `bash -n` on every fenced `bash` block of the three plans (12 blocks, all in Phase 2: 0 syntax failures);
- the Phase 2 T0b acceptance regexes against the Phase 1 spec (all four pass; `rg -c codegraph_ready` = 14);
- `cmp` of each package `source.md` against its spec, `sha256sum` of plans and snapshots;
- existence checks of every `tests/...` path the plans cite (only files the plans create are missing, as expected), of every plugin twin the Phase 3 plan names, and of the `Makefile` targets and `/sc:pr-submit` flags the plans use;
- `make verify-sync` once, to learn the baseline: it exits 1 here because this worktree's `.claude/` mirror is stale (untracked, gitignored). That is not a plan defect: every plan task that runs `make verify-sync` runs `make sync-dev` first.

Fixes I made (MINOR only, section 6): refreshed the Phase 1 `source.md` snapshot, added one clarifying sentence to the Phase 3 plan Task 9, and re-pinned the two `progress.md` ledgers. No IMPORTANT or CRITICAL defect was fixed.

## 1. Verdict table

| Phase | Spec | Tasklist package | Tasks | Verdict |
|---|---|---|---|---|
| 1. Remove codebase-memory-mcp and Serena | `.dev/codegraph-migration/specs/phase-1-removal-spec.md` | `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/` (plan `TASK-WF-phase1RemovalSpe-20261029-185100.md`) | 19 (6 groups G0-G5) | **PASS** (Q-I1 fixed and re-verified by Q2; first pass was FAIL) |
| 2. Install codegraph by default | `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md` | `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/` (plan `TASK-WF-phase2CodegraphI-20261029-192001.md`) | 16 (7 groups G0-G6) | **PASS** (zero findings; Self-Audit below) |
| 3. Adopt codegraph in primitives | `.dev/codegraph-migration/specs/phase-3-codegraph-adoption-spec.md` | `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/` (plan `TASK-WF-phase3CodegraphA-20261029-204913.md`) | 14 (8 groups 0, A-G) | **PASS** (Q-I2 fixed and re-verified by Q2; first pass was FAIL) |
| Coder handoff (Phase 2 companion) | `.dev/codegraph-migration/handoff/coder-handoff-prompt.md` and `coder-handoff-context.md` | not a tasklist (given to a Coder agent) | n/a | **PASS** (Self-Audit below) |

Total 49 tasks. Rule applied: any unfixed finding of any severity is FAIL. In the first pass, Phases 1 and 3 each had exactly one unfixed IMPORTANT defect, both in an acceptance command that cannot print "nothing" when the plan is followed (section 6). Task X fixed both without a design change; the Q2 re-check confirmed the fixes and found no new defect, so all verdicts are PASS.

## 2. Checks per tasklist

Legend: OK = verified by me against the file or tree named; the text says how.

| # | Check | Phase 1 (19 tasks) | Phase 2 (16 tasks) | Phase 3 (14 tasks) |
|---|---|---|---|---|
| 1 | Every review finding resolved (applied, or rejected with evidence) | OK: X-4, X-12, X-15, X-16, X-17, X-24 applied; X-5/X-9/X-6/X-7 pointer-only. Spec `## Review resolution` (lines 870-886) matches the plan: T10/T11 split = Tasks 11-15; CI step kept (Task 16 YAML check); sandbox `HOME` for `install --list` (Task 4); `-g` excludes (Task 6) | OK: X-1, X-2, X-5, X-9, X-10, X-11, X-14, X-15, X-21, X-25 applied, plus F2-1..3 and reflect M-02..M-19 (spec lines 863-899). `CODEGRAPH_MCP_TOOLS` is in spec line 91 and plan Tasks 3, 5, 16; marker block in Task 10; live check is Task 16; baseline diff in Task 9 | OK: X-1, X-2, X-3, X-6..X-10, X-13, X-14, X-18..X-20, X-22, X-23, X-25 applied, plus F3-1..3 and M-01..M-19 (spec lines 380-424). G3 `jq` against `MCP_TOOLS` (spec line 25), `_POST_REFRESH_ADDITIONS` (Tasks 8-9), `_OTHER_COMMANDS` (Task 12), `! git worktree list \| rg -q` (Task 2), CHANGELOG (Task 13), Coder addendum (Task 14). None of the 25 findings was rejected |
| 2 | Every task has a runnable acceptance command and a commit point | Mostly OK: 19/19 have an Acceptance block with commands and a named commit. **One command cannot pass: Task 12 criterion 3 (Q-I1)** | OK: 16/16 have a block (12 fenced blocks pass `bash -n`). Commit points: Task 3 commits together with Task 4 (declared in Task 4 and spec T2 step 0); Tasks 15 (PR only) and 16 (post-merge, nothing in the repo) have none by design, their commit point is the group comment | Mostly OK: 14/14 have a block and a commit. **Task 13 criterion 4 ("no wildcard" and "no explore" searches) cannot pass (Q-I2)** |
| 3 | Tests run after each task group | OK: G0 Task 1 (baseline runs), G1 Task 6, G2 Task 9, G3 Task 15, G4 Task 17, G5 Tasks 18-19. Failures judged against `baseline/full.txt` with `comm -13` | OK: G0 Task 1 baseline (Task 2 is a doc check only), G1 Task 5, G2 Task 8, G3 Task 9, G4 Tasks 10-13, G5 Task 14 (full suite vs baseline), G6 Task 16 (live read-only checks). Baseline file `P2-baseline-failures.txt` | OK: groups A, B, C, D, E, F run named test files (Tasks 4, 5, 7, 9, 11, 12); Task 13 runs the whole `$TESTSET` against `P3-baseline-failures.txt`; group 0 (Task 2) edits no code |
| 4 | Issue #323 comment steps | OK: G0-G5 comments at Tasks 1, 6, 9, 15, 17, 19, with the `gh repo view` check and `--repo IronbellyOrg/IronClaude` (Constraints line 27) | OK: G0-G6 at Tasks 2, 5, 8, 9, 13, 15, 16 (plus Task 1's handoff request); `--body-file /tmp/p2-progress.md` | OK: groups 0, A-G at Tasks 2, 4, 5, 7, 9, 11, 12, 14, template in spec section 6; URLs recorded in `P3X-execution-log.md` |
| 5 | Decision rules (simple / mid = adversarial quick / complex = adversarial standard, logged) | OK: Constraints line 28; log in `$PKG/decisions.md` | OK: Constraints line 27; log `decisions/P2X-log.md` | OK: Constraints lines 30-31; log `decisions/P3X-execution-log.md` |
| 6 | Cross-phase ordering (Phase 1, then 2, then 3, plus Coder pin ordering) | OK: Phases 1+2 are one `master` merge (Constraints line 19, spec 2.2 and D9); no Phase 1-only PR | OK: precondition "Phase 1 committed first"; Task 1 pushes the branch and asks for the Coder work; Task 15 merge gate checks Coder steps 1-2 on Coder `main`; Task 16 runs after the human merge and `./update.sh`. Matches spec section 8 table and handoff prompt "Ordering constraints" 1-5 | OK: starts only after Phases 1+2 are merged (Constraints line 20); needs Phase 1's slots ledger (written by Phase 1 Task 13, checked by Phase 3 Task 1 gate G6); its `master` merge triggers a Coder pin bump, and the marker re-sync plus the Task 14 addendum carry the new block to Coder |
| 7 | No task edits `.claude/` mirrors directly (only `make sync-dev`) | OK: every mirror step is `make sync-dev`; `.claude/` appears only as sandbox `HOME` content in Task 18 | OK: none | OK with one note: Task 2 (E-6) creates temporary, untracked `.claude/agents/cg-smoke-<agent>.md` test agents and deletes them (`ls .claude/agents/cg-smoke-*` must print nothing). They are not mirrors of `src/`; recorded as observation O-2, not a defect |
| 8 | No primitive references `src/superclaude/...` paths | OK: memory paths are project-relative (`.superclaude/memory`, `docs/memory/reflect`); no new `src/superclaude` text in primitives | OK: hook script and core block (spec lines 236-268) carry none | OK: the only allowed form is the labelled fallback after the global path (`~/.claude/CODEGRAPH.md`, fallback `src/superclaude/core/CODEGRAPH.md`), enforced by Task 13 criterion 3 (count not above baseline (a), 157 today) and by `test_impact_guide_lookup_line`. One residual risk fixed as Q-M2 (the design example names `src/superclaude/cli/...`) |
| 9 | No task would stage `.claude/` paths | OK: Constraints line 21 (never stage, never `git add -f`) | OK: Constraints line 24 and a mechanical `git diff --name-only` guard in Task 1 | OK: Constraints line 28; commits stage exact paths plus `.dev/...` only |
| 10 | `.dev/tasks/` staged at every commit | OK (Constraints line 21) | OK (line 25) | OK (line 28) |

### 2.1 Phase 1 detail

- Snapshot: `source.md` was stale against the spec (the spec gained section 8.1 and a reworded section 3.3 after the snapshot). The plan says task text wins, so execution was safe, but the snapshot and the ledger pin disagreed with the spec. Fixed as Q-M1; ledger re-pinned.
- Verified true: the T10/T11 split matches X-12; the retire step's Tier R/Tier K wording carries "absent or `{}`" and `serena-local` (Task 4); `_cleanup_user_native_registration` stays until Task 5 (no red commit between Tasks 4 and 5); Task 6's search excludes the two allowlisted retire-step files.
- Defect: Q-I1 (section 6).

### 2.2 Phase 2 detail

- The user requirement (README line 36) holds across the combined plan: IronClaude removes the current-pin `serena` entry once `codegraph_ready()` is true in the same `superclaude install` run (spec 2.12; plan Task 7), Coder stops re-adding it and runs a guarded backstop (handoff prompt ordering step 2), and Task 16 checks the real `~/.claude.json` with the two `jq -e` lines of spec 2.12 and posts the outputs on #323. Residuals have owners and checks: baked `/usr/local/bin/codebase-memory-mcp` (Coder step 5 image; `! command -v codebase-memory-mcp`), kind-B `~/.local/bin/codebase-memory-mcp` (user; printed `uninstall -y`; sandbox step 6 asserts the print).
- Tool-list key: `MCP_TOOLS` is one constant, chosen by the schema-cost check (Task 3) before the registration code (Task 5). The expected outcome today is `status` only, unless a logged-in `claude` completes Leg B (F2 measured +7,597 B, inside the 6,000-8,000 B undecided band). Phase 3 is written for both outcomes.

### 2.3 Phase 3 detail

- Verified true: all 42 rows of section 1.2 reach a task; the plan's twin-file claims match the tree (`commands/validate-roadmap.md`, `skills/sc-reflect-protocol/SKILL.md` and `core/HOW-WE-WORK.md` have no plugin twin; the `sc-implement-protocol` and `delegation-vs-native-heuristics.md` twins are byte-identical); `_OTHER_COMMANDS` (`tests/core/test_how_we_work_routing_table.py:27,294`) and `shipped == active` (`tests/recommend/test_routing_refresh.py:639-640`) exist as described.
- Defects: Q-I2 and Q-M2 (section 6).

## 3. Coverage: re-run of the inventory searches

Run from the worktree root on 2026-10-29 at HEAD `55d40308`, with the inventories' own patterns (`inventory/codebase-memory.md` section 1.0, `inventory/serena.md` section 0.1) and the Phase 1 acceptance pattern (`specs/phase-1-removal-spec.md` section 8.0). Shell variables:

```bash
EX=(--no-ignore --hidden -g '!.git' -g '!.dev/**' -g '!.claude/**' -g '!.specstory/**' -g '!.venv/**')
W1EX=(--hidden --no-ignore -g '!.dev/**' -g '!.claude/**' -g '!.git/**' -g '!.venv/**' -g '!.specstory/**')
W1='codebase-memory|codebase_memory|CodebaseMemory|Codebase Memory|cbm|CBM_|DeusData|search_graph|trace_path|get_code_snippet|query_graph|index_repository|get_architecture|detect_changes|search_code|list_projects|\.superclaude-codebase-memory'
PAT='serena|Serena|SERENA|mcp__serena|serena-agent|\.serena|MCP_Serena|--serena|find_symbol|find_referencing_symbols|get_symbols_overview|replace_symbol_body|insert_after_symbol|insert_before_symbol|write_memory|read_memory|list_memories|onboarding'
SER=<the SER pattern of acceptance-search.sh, spec section 8.0 line 620, copied verbatim>
```

| # | Command | Inventory figure | Result today |
|---|---|---|---|
| R1 | `rg -n -i "${W1EX[@]}" -e "$W1" . \| wc -l` and `rg -l -i ...` (codebase-memory) | 300 hits, 12 files | **300 hits, 12 files** |
| R2 | `rg -il serena "${EX[@]}" . \| wc -l` | 168 files | **168 files** |
| R3 | `rg -l "${EX[@]}" -e "$PAT" . \| wc -l` and `rg -n ... \| wc -l` | 193 files, 981 lines | **193 files, 981 lines** |
| R4 | `rg -l -i "${EX[@]}" -e "$SER" .` and `rg -n -i ...` (Phase 1 DoD-1 pattern) | not in an inventory | **178 files, 1042 lines** |
| R5 | `git ls-files .serena \| wc -l` | 4 | **4** |
| R6 | `rg -il codegraph "${EX[@]}" . \| wc -l` | 0 (Phase 2 section 0) | **0** (Phases 2-3 not executed yet) |
| R7 | `rg -n -i 'serena\|codebase' .claude/settings.json .github src/superclaude/cli/user_settings_defaults.json` | CI only | **2 hits**: `.github/workflows/test.yml:133` and `:155` (Phase 1 row C12, Task 16) |

Every inventory figure is reproduced exactly: no drift since the specs were written.

Mapping (one `uv run --no-project python -I` script, scratch copy in `/tmp`, nothing written to the repo):
- Union of the hit file sets of R1-R5: **205 files** (R's review reported 203 for R1+R3+R4; my union also includes the R2 and R5 sets).
- Phase 1 spec rows parsed from sections 1.1-1.2: **218** (C 15, S 100, P 98, D 5), of which **31** are "none (keep)" and **187** have a removal action.
- Hit files with no Phase 1 row: **0**. (Brace shorthand such as `{load,pm,save}.md` and directory rows were expanded before matching.)
- Non-keep rows whose id is not named in any Phase 1 plan task (ranges such as `S58-S82` expanded): **0**. So every file with a hit maps to a Phase 1 task through its row.
- Orphans: **none**.

Phase 3 coverage of the primitives that used Serena for code lookups (the files with `find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `find_declaration`, `type_hierarchy`, `search_for_pattern` or `get_diagnostics_for_file`): 20 files, all reached by a Phase 3 section 1.2 row (rows 1-42; the six reflect refs are one combined row 28 and the brainstorm `SKILL.md` lines are in row 32). codebase-memory has no primitive references (`inventory/primitive-usage.md` search C4: 0), so no Phase 3 row is needed for it. Allowlist consistency, re-run with the spec's own `CBM`, `SER` and `ALLOW` patterns (the repo-wide `acceptance-search.sh all` logic, baseline today): 1,341 distinct hit lines; 23 are allowlisted, in 10 files (`CHANGELOG.md`, `POST-REFLECT-TASK.md`, `docs/memory/patterns_learned.jsonl`, `docs/memory/pm_context.md`, `.gitignore`, `ccsession-tag/install.sh`, `sc-cleanup-audit-protocol/SKILL.md`, `tests/cli/test_install_mcp_registry.py`, `tests/skills/test_implement_severity_replay.py`, the `Fable-D3/REPORT.md` fixture); the other 1,318 lines in 176 files all belong to non-keep rows (none of the residual files is a "none (keep)" row). So DoD-1 is reachable on file coverage. Not re-checked by me: whether line-level edits in each row remove every line (that is what the Task 18 `acceptance-search.sh all` run proves at execution time).

## 4. Consolidated autonomous-decisions log

One row per decision, collected from every `## Decisions` section of the inventories, research, specs, F-results and the review, plus the adversarial records under `decisions/`. Method values: self; adversarial quick; adversarial full; protocol-forced. "Superseded" means a later row changed the outcome; the later row is the one in force. The seven `decisions/P2-review/*-report.md` files are review reports, not decisions (their fixes are P2 D23, D24 and the second-pass rows). Not collected: the brainstorm's "Classification decisions" (`brainstorm/.../socratic-answers.md`) and the design doc's D-1..D-9, which P3-D11 accepts as one row.

### 4.1 Inventories and research (wave 1)

| ID | Decision | Choice | Method | Source |
|---|---|---|---|---|
| CBM-D1 | Which installer file to delete | Keep `install_mcp.py` (other servers use it), delete only `install_codebase_memory.py` | self | `inventory/codebase-memory.md` |
| CBM-D2 | `superclaude mcp --uninstall` and `--yes` | Remove both (no valid target left) | self | same |
| CBM-D3 | Menu after removal | "1. Install MCP servers (default)" and "2. Cancel" | self | same |
| CBM-D4 | CI `Install Claude CLI` step | Delete it. **Superseded** by P1 D20 / X-15: keep the step, rewrite comments | self | same |
| CBM-D5 | `.specstory/` history (365 hits) | Out of scope, keep | self | same |
| CBM-D6 | Who cleans existing workspaces (left OPEN) | Recommended a retire step inside `superclaude install`. **Closed by** P1 D2 | self recommendation, then adversarial full | same |
| CBM-D7 | Generic `mcp` tests in the cbm test file | Port first, then delete the file | self | same |
| CBM-D8 | Definition of "green" | No more failures than the recorded baseline | self | same |
| CBM-D9 | `~/.cache/codebase-memory-mcp` | Leave alone | self | same |
| CBM-D10 | Reading live state | `jq` reads only, no `claude mcp list` or `uninstall` | self | same |
| SER-D1 | Replacement for Serena memory | `.superclaude/memory/` plain files (option A, scores 0.6664 vs C 0.6540 vs B 0.5825, debate 9-1-1); reflect calibration to `docs/memory/reflect/`; per-worktree store | adversarial quick (`decisions/W2-serena-memory-replacement/`) | `inventory/serena.md` |
| SER-D2 | Reflect halt tokens and `serena_summary_corroboration` | Remove the two tokens, the field, 24 fixture lines, `degraded_serena.yaml`, two tests | self | same |
| SER-D3 | Retire Serena on existing machines | Installer retire step matching `serena-agent`; print (never run) data-removal commands. **Refined by** P1 D2, P2 D22 | self | same |
| SER-D4 | `.gitignore:113` and the audit-skill `.serena/` line | Keep; delete the four tracked `.serena/` files | self | same |
| SER-D5 | 19 files matching only `onboarding` | False positives, keep | self | same |
| SER-D6 | Files that use the word as history or a label | Keep (`CHANGELOG.md` gets a new entry) | self | same |
| SER-D7 | Serena tool gaps in Phase 1 | Drop Serena tools, fall back to Read/Grep, codegraph in Phase 3. **Refined by** P1 D1 | self | same |
| SER-D8 | Mirror trees | Hand-edit `plugins/superclaude/` and root `commands/`, `agents/` in the same commit | self | same |
| SER-D9 | Eval E8 and `mcp_server.serena` | Delete, do not rewrite | self | same |
| SER-D10 | Test count impact | About 5 deleted, 4 added (assumption, UNVERIFIED) | self | same |
| PU-1 | Count bare Serena tool names as references | Search names and tool names | self | `inventory/primitive-usage.md` |
| PU-2 | Decorative vs load-bearing | Decorative when the same place names a native fallback | self | same |
| PU-3 | Plugin copies | One whole-file row per plugin file | self | same |
| PU-4 | `mcp-servers:` frontmatter | Decorative; Phase 1 still strips it | self | same |
| ORG-1..8 | Org-repo inventory outline, historical-record handling, live-config labels, caps stated, ownership per repo (8 rows) | Brief's outline; keep `.dev`/`claudedocs` history; label project-local commands/skills/agents as live; state result caps; owner = repository | self (all 8) | `inventory/org-repos.md` |
| EV-1 | Which codegraph to evaluate | Main project `colbymchenry/codegraph`, not the Rust fork | self | `research/codegraph-evaluation.md` |
| EV-2 | Version to test | Pin v1.6.2 | self | same |
| EV-3 | Integrity check | `sha256sum` and `gh attestation verify` before running upstream `install.sh` | self | same |
| EV-4 | Token for attestation check | `GH_TOKEN` read-only under sandbox `HOME` | self | same |
| EV-5 | `codegraph install` test | Run only against a sandbox `HOME` | self | same |
| EV-6 | Install strategy | Merged C+A: bake in image, IronClaude verifies and registers, one pin (`decisions/W4-install-strategy/`) | adversarial quick | same |
| EV-7 | Registration form | `claude mcp add-json` with `alwaysLoad` | self | same |
| EV-8 | Telemetry and update check | Disable via env in the MCP entry and the image | self | same |
| FLOW-1 | Where codegraph installs | A phase in `superclaude install`; `update`/`update.sh` unchanged. Became P2 D7 | self | `research/install-update-flow.md` |
| FLOW-2 | Phase model | Reuse a PATH executable first (modelled on the codebase-memory phase) | self | same |
| FLOW-3 | Registration helpers | Parameterise by server name | self | same |
| FLOW-4 | Cleanup trigger | Inside `superclaude install`, narrow registration-only. **Refined by** P1 D2 | self | same |
| FLOW-5 | Coder's `/usr/local/bin/codebase-memory-mcp` | External; IronClaude never deletes it, the image does | self | same |
| FLOW-6 | Release order | Coder bake, then IronClaude merge as one unit, then Coder removal | self | same |
| FLOW-7 | How Coder was read | `gh api .../tarball/main` into `/tmp` | self | same |

### 4.2 Phase 1 spec (`specs/phase-1-removal-spec.md`, Decisions D1-D20)

| ID | Decision | Choice | Method | Source |
|---|---|---|---|---|
| P1-D1 | Load-bearing Serena steps | Triage; delete or rewrite to a Grep/Read floor now; slots ledger for Phase 3 (A 0.841, B 0.778, C 0.735; convergence 1.00) | adversarial quick (`decisions/P1-primitive-gap-policy/`) | spec 843-849 |
| P1-D2 | Existing-workspace cleanup | Non-fatal retire step in `superclaude install`, removes only provable IronClaude entries; current-pin Serena kept until Phase 2's gate (A 0.877, C 0.730, B 0.717) | adversarial full (`decisions/P1-existing-workspace-cleanup/`) | same |
| P1-D3 | Serena memory | Apply SER-D1 unchanged incl. one release of read-only `/sc:load` legacy read | self | same |
| P1-D4 | `serena_summary_corroboration` | Delete the field (code shows no reader) | self | same |
| P1-D5 | Task order | Retire step (T3) before detaching `mcp` (T4) | self | same |
| P1-D6 | Native registration helpers | Delete the three unused ones; Phase 2 restores parameterised versions | self | same |
| P1-D7 | "Retired servers" doc section | None; CHANGELOG and printed output carry the commands | self | same |
| P1-D8 | Environment checks | Sandbox `HOME` only; no live `./update.sh` in Phase 1 | self | same |
| P1-D9 | Merge | Phase 1 never merges alone | self (forced by Coder monitor) | same |
| P1-D10 | Reflect refs and calibration move | Refs to T11, calibration to T10 | self | same |
| P1-D11 | Acceptance search | W2 pattern minus `onboarding`/`sc:save`, plus Serena-only names; line-level allowlist | self | same |
| P1-D12 | Full-suite runs | `T02_15_PERF_REPORT=/tmp/p1-perf.json` | self | same |
| P1-D13 | `relative_path` hook branch | Delete | self | same |
| P1-D14 | CI proof | Local no-CLI simulation; CI proves in the Phase 1+2 PR; step kept (X-15) | self | same |
| P1-D15 | Mirror trees | Hand-edit in the same commit | self | same |
| P1-D16 | Retired primitive files | No delete list needed (no shipped name removed) | self | same |
| P1-D17 | Other-repo work | Handoff notes only | self | same |
| P1-D18 | T10/T11 size | Split into T10a/T10b and T11a/T11b/T11c (X-12), reflect agents to T11a, pm protocol to T10a | self (forced by rule G5) | same |
| P1-D19 | Phase 2 Serena gate | Apply Phase 2 T0b now (X-4): `env`/`headers` absent or `{}`, hint `serena-local` | self | same |
| P1-D20 | CI Claude CLI step | Keep it, rewrite comments only (X-15) | self | same |

### 4.3 Phase 2 spec (`specs/phase-2-codegraph-install-spec.md`, Decisions D1-D30)

| ID | Decision | Choice | Method | Source |
|---|---|---|---|---|
| P2-D1 | Installer contract | Required phase (exit 1 on failure); doctor fails only on a dangling command; receipt-gated documented removal (C 0.896, B 0.859, A 0.839) | adversarial full (`decisions/P2-installer-contract/`) | spec 828-861 |
| P2-D2 | Indexing | Fail-open SessionStart hook indexes each checkout once in the background plus a core CLAUDE.md fallback; no global git config (B 0.886, A 0.756, C 0.736) | adversarial quick (`decisions/P2-indexing-sync/`) | same |
| P2-D3 | Rebuild rule | Superseded by D21 | self (probes) | same |
| P2-D4 | Pin | v1.6.2, four-asset SHA-256 table; no Windows | self | same |
| P2-D5 | Permission rule | No `mcp__codegraph__*` rule | self | same |
| P2-D6 | MCP config/doc files | No `MCP_Codegraph.md` or `configs/codegraph.json` | self | same |
| P2-D7 | `update.sh` and `superclaude update` | Unchanged | self | same |
| P2-D8 | Registration helpers | Adapt mechanically to what Phase 1 left | self | same |
| P2-D9 | CI Claude CLI step | Keep or restore | self | same |
| P2-D10 | Download | Stdlib (`urllib`, `hashlib`, `tarfile`), no `curl` | self | same |
| P2-D11 | Coder bake not ready | PR waits; phase never made optional | self | same |
| P2-D12 | Merge unit | Phases 1+2 one PR, one merge | self (forced) | same |
| P2-D13 | `/sc:design` | Not run | self | same |
| P2-D14 | Coder decision records | Coder `.dev/decisions/`, fallback comparison | self | same |
| P2-D15 | Hook PID-file design | Superseded by D21 | self (probes) | same |
| P2-D16 | Subprocess calls | Bounded argv runner, own process group | self | same |
| P2-D17 | Binary pointer | `~/.codegraph/.superclaude-bin` | self | same |
| P2-D18 | `add-json` stored shape | Verify in a sandbox first (T2 step 1) | self | same |
| P2-D19 | Core CLAUDE.md on Coder | Coder carries the rule; IronClaude does not work around the restore | self | same |
| P2-D20 | Planning files | New task T0 commits and pushes them and triggers the Coder handoff | self | same |
| P2-D21 | Hook behaviour | Run `init --yes` only when `<top>/.codegraph/codegraph.db` is absent; no marker, PID file, `status`, `index`, `sync` | self (probe rows 6-9) | same |
| P2-D22 | Serena entry removal | Remove every user-scope Serena launcher entry and the kind-B cbm registration once `codegraph_ready()` holds in the same run (B 0.898, C 0.853, A 0.835; contract partial) | adversarial full (`decisions/P2-serena-entry-removal/`) | same |
| P2-D23 | Third-review fixes | `env`/`headers` absent or `{}`; hook keys on the database file; `.codegraph/` in `.gitignore`; T0b owns Phase 1 amendment | self (forced by evidence) | same |
| P2-D24 | Fourth/fifth-review fixes | Match Serena by shape except `serena-local`; Coder backstop in `startup.sh`; one `codegraph_ready()`; split acceptance | self (forced) | same |
| P2-D25 | Owner of `CODEGRAPH_MCP_TOOLS` | Phase 2, one `MCP_TOOLS` constant; seven tools on pass, `status` on fail | self (forced by X-1) | same |
| P2-D26 | Guidance block | Between `SUPERCLAUDE_CODEGRAPH_BEGIN/END` markers; Coder re-syncs on every pin bump | self (forced by X-2, X-10) | same |
| P2-D27 | Post-merge live check | Task T12; results only in the #323 comment, no commit | self (X-5) | same |
| P2-D28 | Baseline-diff command | Use a `pipefail`-safe form, not the review's one-liner | self | same |
| P2-D29 | CI step | Re-add only if Phase 1 deleted it | self (X-15) | same |
| P2-D30 | Schema-cost method | Byte measurement over stdio as the gate with 6,000/8,000 B bands; session leg only inside the band, never blocking (A 0.870, C 0.829, B 0.701) | adversarial quick (`decisions/F2-schema-cost-method/`) | same |

### 4.4 Phase 3 spec (`specs/phase-3-codegraph-adoption-spec.md`, Decisions P3-D1..D20)

| ID | Decision | Choice | Method | Source |
|---|---|---|---|---|
| P3-D1 | Access model | MCP with exact tool names, Phase 2 sets the tool list, CLI only for named read verbs, explore blocked (B 0.912, C 0.871, A 0.810; C won the tiebreak; INV-002/003/011 carried as accepted risks) | adversarial full (`decisions/P3-access-model/`) | spec 351-376 |
| P3-D2 | Shared guidance | One core doc `CODEGRAPH.md` installed to `~/.claude/`, not `@`-imported | self | same |
| P3-D3 | Start from Phase 1's text | Map every ledger row to a section 1.2 row; codegraph tier above the floor (revised by X-6) | self | same |
| P3-D4 | Memory | Not a codegraph job | self (inherits SER-D1) | same |
| P3-D5 | Diagnostics | Bash in the orchestrator under reflect's envelope | self | same |
| P3-D6 | `type_hierarchy` and `--with-hierarchy` | Drop | self | same |
| P3-D7 | `graph:*` tokens | Informational, not halt tokens; a test pins it | self | same |
| P3-D8 | STRICT tier | codegraph preferred, Grep fallback recorded; `Skill` added to `sc-task-protocol` | self | same |
| P3-D9 | `explore` | No primitive names it | self | same |
| P3-D10 | New commands | Two: `/sc:impact`, `/sc:graph` (C 0.781, A 0.748, B 0.727) | adversarial quick (`decisions/P3-command-set/`) | same |
| P3-D11 | Design decisions DES D-1..D-9 | Accept all nine (pin and E-1 lines in guide; `init` literal only in `graph.md`; own allowlist for `/sc:impact`; caps of 30; `--diff` default `HEAD`; telemetry only in `/sc:graph`; `partial` when not ready; `init` refuses an existing index; direct Skill calls) | self | same |
| P3-D12 | Command name | `/sc:graph`, not `/sc:codegraph` | self | same |
| P3-D13 | Gated ideas | Ship only advisory forms; defer gates | self | same |
| P3-D14 | Debate depth | Access model standard; command set quick | self | same |
| P3-D15 | How debates ran | In subagents, outputs on disk | self | same |
| P3-D16 | Prerequisite experiments | Add T0 (E-1, E-2, E-3, E-6, E-7); E-5 moved to Phase 2 | self | same |
| P3-D17 | Indexing ownership | Adopt Phase 2's hook model; `/sc:graph init` is the manual path (X-3) | self | same |
| P3-D18 | Kill switch | `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` (X-14) | self | same |
| P3-D19 | CLI `status` | Guard with `pgrep -f 'codegraph\.js (init\|index)'` (F3-1) | self | same |
| P3-D20 | Status-only branch | Same primitive text; `graph:unlisted`; orchestrators use CLI read verbs | self | same |

### 4.5 Finalizer and review results

| ID | Decision | Choice | Method | Source |
|---|---|---|---|---|
| F1-1 | Apply X-4 | Exactly as Phase 2 T0b lists; Tier K message "kept until codegraph is ready"; hint `serena-local` | self | `review/F1-result.md` |
| F1-2 | X-12 split | T11a takes `reflect-reviewer` and `reuse-auditor`; T10a takes `sc-pm-protocol` | self (forced by rule G5) | same |
| F1-3 | X-15 | Keep the CI step, rewrite comments | self | same |
| F1-4 | X-24 | Keep `pm_context.md:77` unchanged | self | same |
| F1-5 | Cross-phase findings | Only the Phase 1 hunk; no edit to other specs or handoff | self (brief) | same |
| F1-6 | G0 issue comment | Add one so every group commit has a comment | self | same |
| F1-7 | `source.md` | `cp` plus `cmp`, not the Write tool | self (deviation, recorded) | same |
| F1-8 | Reflect output location | Default `.dev/reflect/...` | self | same |
| F1-9 | Reflect without Serena | Fail open to Read/Grep, recorded degraded | self | same |
| F1-10 | Post-reflect plan edits | Edit the generated plan; "task text wins over `source.md`"; mirror in spec 8.1 | self | same |
| F1-11 | Reflect `partial` | Accept without rerun | self | same |
| F1-12 | `progress.md` | Seed ledger header and `PLAN:` pin | self | same |
| F1-13 | Stray `/tmp/x` | Removed (empty, created by the run) | self | same |
| F2-1 | Schema-cost method (T2 step 0) | A's byte measurement as gate, three bands; B decides only in band; never blocks | adversarial quick (`decisions/F2-schema-cost-method/`) | `review/F2-result.md` |
| F2-2 | `CODEGRAPH_MCP_TOOLS` owner | Phase 2, one constant (= P2-D25) | self | same |
| F2-3 | Guidance block | Markers, re-sync every pin bump (= P2-D26) | self | same |
| F2-4 | Post-merge check T12 | No commit; issue comment is the record (= P2-D27) | self | same |
| F2-5 | Review's X-11 command | Corrected form (= P2-D28) | self | same |
| F2-6 | T8 | Re-add CI step only if deleted (= P2-D29) | self | same |
| F2-7 | X-14 | Phase 2 states scope and prefix only | self | same |
| F2-8 | Applying review findings | No adversarial run (each settled by source) | self | same |
| F2-9 | `source.md` | `cp` plus `cmp` | self (deviation) | same |
| F2-10 | Refresh `source.md` after spec fixes | Yes | self | same |
| F2-11 | Edit plan after reflect | Yes (brief step 2) | self | same |
| F2-12 | Task 14 | Keep final verification task | self (brief) | same |
| F2-13 | `progress.md` | Seed header and pin | self | same |
| F2-14 | Reflect `partial`; two reviewers; artifact path glob | Accept; protocol-forced; `$(echo .dev/tasks/*/<id>)/artifacts` | self / protocol-forced | same |
| F3-1 | X-3 | Phase 3 adopts Phase 2's hook model | self | `review/F3-result.md` |
| F3-2 | Status-only branch | Same text; CLI lookup verbs in orchestrators, floor elsewhere | self | same |
| F3-3 | CLI `status` guard | `pgrep` guard everywhere | self | same |
| F3-4 | Kill switch | `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` | self | same |
| F3-5 | X-6 mapping | Count check, not verbatim anchor match | self | same |
| F3-6 | Spec vs design doc | Spec wins for overrides (a)-(e) | self | same |
| F3-7 | Group comments | At the eight group-closing tasks | self | same |
| F3-8 | `source.md` | `cp` plus `cmp`, refreshed after second pass | self (deviation) | same |
| F3-9 | Edit plan after reflect | Yes | self | same |
| F3-10 | Inherited spec findings | Fixed in spec and plan | self | same |
| F3-11 | Reflect `partial` | Accept | self | same |
| F3-12 | Reviewers | Two (protocol-forced) | protocol-forced | same |
| F3-13 | `progress.md`; no adversarial run for findings | Seed header and pin; none needed | self | same |
| R-1 | X-3 contradiction | No adversarial run; Phase 2's hook model wins on evidence | self | `review/review.md` |
| R-2 | Severity of X-4 | IMPORTANT, not CRITICAL (the combined plan does remove the entry) | self | same |
| R-3 | Severity of X-3 and X-1 | CRITICAL | self | same |
| R-4 | File coverage | Pass instead of per-file findings (scripted `comm` printed nothing) | self | same |
| R-5 | Test runs | Two specific test files only | self | same |

### 4.6 Adversarial records under `decisions/` (same decisions as above, with the folder that proves them)

| Folder | Decision | Result | Method |
|---|---|---|---|
| `decisions/W2-serena-memory-replacement/` | Serena memory replacement | Option A amended (SER-D1) | adversarial quick |
| `decisions/W4-install-strategy/` | Install strategy | Variant C base, merged with A (EV-6) | adversarial quick |
| `decisions/P1-primitive-gap-policy/` | Primitive gap policy | Option A with C's triage rule (P1-D1) | adversarial quick |
| `decisions/P1-existing-workspace-cleanup/` | Existing-workspace cleanup | Amended Option A (P1-D2) | adversarial full |
| `decisions/P2-installer-contract/` | Installer contract | Variant C base plus parts of A and B (P2-D1) | adversarial full |
| `decisions/P2-indexing-sync/` | Indexing | Variant B, SessionStart hook (P2-D2), narrowed by `probe-results.md` | adversarial quick |
| `decisions/P2-serena-entry-removal/` | Serena entry removal | Option B corrected in debate (P2-D22) | adversarial full |
| `decisions/F2-schema-cost-method/` | Schema-cost method | Option A base plus B's session leg (P2-D30, F2-1) | adversarial quick |
| `decisions/P3-access-model/` | Access model | Hybrid C (P3-D1) | adversarial full |
| `decisions/P3-command-set/` | Command set | Option C, two commands (P3-D10) | adversarial quick |

Count: 10 adversarial runs (6 quick: W2, W4, P1 gap policy, P2 indexing, F2 schema cost, P3 command set; 4 full: P1 cleanup, P2 installer contract, P2 Serena removal, P3 access model). Every other row is self or protocol-forced. No decision blocked on the user; the F2 proposals that still need the user's confirmation are listed in section 5. Two earlier outcomes were overturned by later, better-informed rows and must be read as superseded: CBM-D4 (CI step) by P1-D20, and CBM-D6 (cleanup left open) by P1-D2.

## 5. Human-intervention points that remain

Phase 1 needs no human during execution (spec section 10). Everything below is what remains across the three phases and the Coder side.

| # | Point | Where | Why it cannot be automated |
|---|---|---|---|
| H1 | `gh` is not authenticated | Phase 1 (non-blocking, error recorded), Phase 2 item 1, Phase 3, Coder | The executor cannot log in as the user |
| H2 | `SHA256SUMS` of codegraph v1.6.2 differs from the pinned hashes | Phase 2 item 2, Coder prompt | Possible tampering; changing a hash is a trust decision |
| H3 | Hand `coder-handoff-prompt.md` to an agent working in `IronbellyOrg/Coder` | Phase 2 item 5 | Cross-repo edits are forbidden for this run and for the IronClaude executor |
| H4 | Merge the Coder PRs to Coder `main`, then deploy the template to live workspaces; Coder steps 1-2 must be on `main` before IronClaude merges | Coder prompt "Ask a human only for" | Coder repo owner's call; deployment mutates live workspaces |
| H5 | Merge the Phase 1 + 2 PR to `master` | Phase 2 item 3, Task 15 merge gate | The merge order depends on the Coder bake; the monitor bumps Coder's pin on every `master` commit |
| H6 | Run the real `./update.sh` on the workspace, then restart every Claude session | Phase 2 item 4, Task 16 | It mutates the live environment (`pipx install --force`); a sandbox cannot prove it; sessions load MCP registrations only at start |
| H7 | Merge the Phase 3 PR | Phase 3 H2 | Merge is always human; the merge also triggers a Coder pin bump |
| H8 | Phase 3 gate G1-G4 fails (codegraph missing, unregistered, wrong tool list, no index) | Phase 3 H1 | Phase 3 may not run `superclaude install`, `./update.sh` or `claude mcp add`; the Phase 2 install must be fixed and `./update.sh` rerun |
| H9 | A Phase 3 acceptance command still fails after two fix attempts and a quick adversarial decision | Phase 3 H3 | Accepting a documented skip is a scope decision |
| H10 | Phase 1 left a step that contradicts Phase 3 section 1.2, the slots ledger is missing, or a ledger row fits no section 1.2 row | Phase 3 H4 | Whether a deleted step should return is a design call |
| H11 | A fresh or headless `claude` session is needed (experiments E-3, E-6, the live smoke) and the executor cannot start one | Phase 3 H5 | A running session does not load new commands or agent files |
| H12 | The tool-list schema cost lands in the undecided band and no valid session measurement exists, so `MCP_TOOLS` ships as `status` (the expected outcome today: +7,597 B against bands of 6,000/8,000 B); a person with a logged-in `claude` later runs the printed Leg B commands and may flip the constant back to seven tools | Phase 2 item 6; `decisions/F2-schema-cost-method/recommendation.md` "Items for the user" | The 2K-token threshold, the byte edges, the 50-token tolerance and the `D/5` floor are proposals the user has not confirmed. Until then Phase 3 primitives reach codegraph only through the CLI in orchestrators and the Grep/Read floor elsewhere |
| H13 | Run the printed removal commands for registrations IronClaude keeps: a Serena launcher with non-empty `env`/`headers`, local-scope entries (`claude mcp remove <name> --scope local`), the kind-B upstream `codebase-memory-mcp uninstall -y --dir=~/.local/bin`, `rm ~/.local/bin/install.sh` and the receipt, `uv tool uninstall serena-agent` off Coder | Phase 2 item 7, spec 2.12 | They are not provably IronClaude's, or they are account-wide and prompt-free; Phase 1 D2 rejected automatic removal |
| H14 | Delete user data: `~/.serena` (62 MB), 12 project `.serena/` folders, `~/.cache/codebase-memory-mcp`, uv cache entries | Phase 1 section 2.3, CHANGELOG entry | Memories and logs are user content; deletion needs consent |
| H15 | Remove the root-owned `/usr/local/bin/codebase-memory-mcp` and the Coder `uv tool` copy of Serena | Coder steps 2 and 5 | Only a new Coder image or Coder's migration can; no user-level step can remove a root-owned bake |
| H16 | The owners of 11 other IronbellyOrg repos apply the handoff notes (`$PKG/handoffs/<repo>.md`, written by Phase 1 Task 19) | Phase 1 section 6 | Cross-repo edits are forbidden here; each owner decides |
| H17 | RESOLVED: Q-I1 and Q-I2 were fixed by task X and re-verified by task Q2 (see "Re-check (Q2)"); nothing left to route | Section 6 | n/a |
| H18 | Decide whether to stage the three `.dev/reflect/pre-phase*` report folders (1.5 MB, cited by the specs and return contracts, never read by a task). Phase 2 Task 1 stages `.dev/codegraph-migration` and `.dev/tasks` only | Observation O-3 | Not required by any rule; repository hygiene choice |

Unavoidable-by-design residual: after `./update.sh` alone, a Coder workspace keeps the root-owned codebase-memory binary and the Serena `uv tool` until Coder ships its new image, and the bundle on the old image re-adds the Serena registration at the next workspace start. The user's "completely absent after `./update.sh`" therefore holds for registrations at that moment and for programs only after Coder steps 2 and 5. This is documented in Phase 2 spec 2.12 with owners and checks (README concern 1 is met: who, when and a check exist).

## 6. Defects found

Severity scale (same as `review/review.md`): CRITICAL = the plan cannot meet a stated requirement; IMPORTANT = an acceptance check cannot pass as written, a red commit, or a missing owner; MINOR = stale fact, wording or fragile check. No CRITICAL defect found.

| ID | Severity | File | Defect | Fix | Status |
|---|---|---|---|---|---|
| Q-I1 | IMPORTANT | Plan `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/TASK-WF-phase1RemovalSpe-20261029-185100.md`, Task 12, criterion 3 (line 174); same command in `specs/phase-1-removal-spec.md` T10b acceptance (line 736) and in `source.md` | The repo-wide search for `write_memory\|read_memory\|list_memories\|edit_memory\|delete_memory\|think_about_\|summarize_changes\|activate_project\|check_onboarding_performed\|prepare_for_new_conversation\|get_current_config` must print nothing at Task 12, but files whose tool steps belong to Tasks 13 and 15 still carry those tokens. Today it hits `sc-reflect-protocol/SKILL.md` (59 lines, among them 12 `think_about_`, 8 `prepare_for_new_conversation`, 9 `get_current_config`, 4 `activate_project`), `commands/reflect.md` and its two copies, `commands/validate-roadmap.md:6` (`allowed-tools`), `sc-validate-roadmap-protocol/SKILL.md` (`activate_project`) and `sc-task-protocol/SKILL.md` (`think_about_`). Even the five memory names alone still hit the reflect `--onboard` bootstrap (SKILL.md lines 91-309), which Task 13 deletes. The plan's own rule says a task may not need a later task to go green | In plan Task 12 and spec T10b: keep only the five memory names, add `-g '!src/superclaude/skills/sc-reflect-protocol/SKILL.md' -g '!**/reflect.md' -g '!commands/sc-reflect.md' -g '!src/superclaude/commands/validate-roadmap.md'`, and leave the full-token repo-wide check to Task 15, whose `acceptance-search.sh serena src/superclaude plugins/superclaude commands agents` already covers it. Owner: F1 (Phase 1 finalizer) | **FIXED** (Phase 1 plan Task 12 criterion 3, `specs/phase-1-removal-spec.md` T10b acceptance, package `source.md` and `progress.md` PLAN pin changed; see `review/X-fixes-result.md`); **re-verified by Q2** (section "Re-check (Q2)", step 1) |
| Q-I2 | IMPORTANT | Plan `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md`, Task 13, criterion 4 (the "no wildcard" and "no explore" searches, line 212); same commands as T11 (5) and (6) in `specs/phase-3-codegraph-adoption-spec.md` (line 287) and in `source.md` | Search (5) scans `src/superclaude/core` and `plugins/superclaude`; search (6) scans `plugins/superclaude`. Both therefore scan the guide (`src/superclaude/core/CODEGRAPH.md` and its byte copy `plugins/superclaude/core/CODEGRAPH.md`), whose "Never" section is required by spec section 4 item 7 and plan Task 3 to name `Bash(codegraph *)`, `explore` and `codegraph context`, the exact strings the searches reject. The spec exempts "the guide in `core/`" only by leaving `src/superclaude/core` out of (6); the plugin copy is not exempt. Following the spec makes both searches print hits | Add `-g '!**/core/CODEGRAPH.md'` to both `rg` commands in plan Task 13 criterion 4 and in spec T11 (5) and (6); the Task 3 test already confines those strings to the guide's "Never" section. Owner: F3 (Phase 3 finalizer) | **FIXED** (Phase 3 plan Task 13 criterion 4, `specs/phase-3-codegraph-adoption-spec.md` T11 (5) and (6), package `source.md` and `progress.md` PLAN pin changed; see `review/X-fixes-result.md`); **re-verified by Q2** (section "Re-check (Q2)", step 2) |
| Q-M1 | MINOR | `.dev/tasks/to-do/TASK-WF-phase1RemovalSpe-20261029-185100/source.md` and `progress.md` | The snapshot was byte-exact at generation but the spec changed afterwards (new section 8.1, section 3.3 "replaces" became "succeeds", one new review row). `cmp` differed at line 334; the ledger pinned the stale hash. Phase 2 and Phase 3 snapshots were already identical to their specs | `cp` spec to `source.md` and verify with `cmp`; rewrite the `PLAN:` pin: plan sha256 `49605f30...` unchanged, `source_sha256=f2f1f48919811400d7c87c391b4b6af5f2e2c74910100aff893fc782d5c87037` | **FIXED** (cmp now identical) |
| Q-M2 | MINOR | `.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/TASK-WF-phase3CodegraphA-20261029-204913.md`, Task 9; source `.dev/codegraph-migration/design/P3-commands/interface-design.md` lines 381-426 | The `/sc:impact` contract example names `install_codebase_memory_mcp` (deleted by Phase 1) and `src/superclaude/cli/...` paths. Copying it into the skill or `impact.md` would fail `test_impact_guide_lookup_line` and raise the installed-path count above baseline (a) | Added one sentence to Task 9 telling the executor to use neutral placeholder symbols and paths; ledger `PLAN:` pin updated: plan sha256 `04191a306982f8d60480d2225921a87fae6be4a7b395d0377f383ff473303cce`, `source.md` unchanged (`c4159819...`, still equal to the spec) | **FIXED** (plan only; the spec is unchanged) |

### 6.1 Observations (no defect, no change made)

- **O-1** Phase 2 Task 3 has no commit of its own: its client script, evidence files and `t3-run*.json` are committed with Task 4 (declared in Task 4 and in spec T2 step 0). Tasks 15 and 16 have no repository commit by design.
- **O-2** Phase 3 Task 2 (E-6) writes temporary untracked `.claude/agents/cg-smoke-<agent>.md` files and removes them; `ls .claude/agents/cg-smoke-*` must print nothing. Gitignored, never staged.
- **O-3** `.dev/reflect/pre-phase*` reports are untracked and not staged by any plan (see H18).
- **O-4** Phase 2 Task 11 adds `serena-local` text to `docs/user-guide/mcp-installation.md` on purpose (the printed hint names it). After the merge that file mentions Serena, which Phase 1's wording of DoD-1 ("no repo file outside `.dev/` references either server except section 2.4") does not list. No check fails because Phase 1's gate runs before Phase 2; worth one sentence in the release notes.
- **O-5** Phase 3 E-7 counts Markdown table rows in the slots ledger; Phase 1 rule G9 and plan Task 13 do not fix the ledger format. The plan has a hand-count fallback, so it works. Cheap hardening for F1: state "one Markdown table with one header row, rows appended".
- **O-6** Phase 3 Task 5 says `Depends on: Task 2` although the agent bodies cite the guide written in Task 3. Harmless in the linear order; matters only for a partial resume.
- **O-7** `make verify-sync` fails in this worktree until `make sync-dev` runs (stale untracked `.claude/`). Every plan task runs `make sync-dev` first.
- **O-8** Phase 2 uses `git checkout -- .../perf.json` after full-suite runs; Phase 1 uses `T02_15_PERF_REPORT`. Both are valid (the override exists at `tests/cli/eval/test_perf_home_setup.py:122`).

## Self-Audit (zero-finding targets)

Required for targets with zero findings: Phase 2 and the Coder handoff. What I actively tried, and why I concluded there is no defect.

### Phase 2 (spec + 16-task plan): PASS

1. **Review coverage.** I traced every finding assigned to Phase 2 (X-1, X-2, X-5, X-9, X-10, X-11, X-14, X-15, X-21, X-25, F2-1..3, M-02..M-19) from the spec's Review resolution to the sentence in spec and plan that implements it, not just to the table row. Examples read in the text: `CODEGRAPH_MCP_TOOLS` in the registration JSON (spec line 91) and the `jq -e` equality in plan Task 5 and Task 16; markers in the guidance block (spec 264-268) and the one-row and marker-count asserts in Task 10; Task 16 exists; `if cmd; then exit 1; fi` form in Tasks 1, 10, 11, 14.
2. **Tried to make each acceptance block fail by construction.** `bash -n` on all 12 blocks (0 failures). Task 2 regexes run against the real Phase 1 spec: all pass. Task 10's `rg` searches do not match the block text itself (the block names no `codegraph_explore` and not upstream's `CODEGRAPH_START`). Task 5's expected-entry JSON equals spec line 534. Task 7's `rg -l -g '*.py' install_retired_mcp tests` is empty today, but the plan asserts it non-empty and Phase 1 Task 4 creates `tests/cli/test_install_retired_mcp.py` first. Task 9 and Task 14 judge known failures by baseline diff in a `pipefail`-safe form; the baseline file is created in Task 1 and checked to exist. Task 16 records both scope results before it gates.
3. **Ownership and ordering across phases.** `install_retired_mcp.py` (Phase 1 creates, Phase 2 Task 7 extends), the CI step (Phase 1 Task 16 keeps it, Phase 2 Task 12 checks), the core CLAUDE.md row and block (Phase 2 adds, Phase 3 edits in place), `codegraph_ready()` (Task 6 prints three `--list` lines, Task 7 adds the fourth). Merge order agrees with the handoff prompt, Phase 1 section 2.2 and Phase 3 section 7.
4. **User requirement.** Removal of the current-pin Serena registration: who (IronClaude retire step once codegraph is ready; Coder step 2 stops re-adding; guarded backstop), when (same `superclaude install` run), checks (sandbox step 6, Task 16 `jq`). Residuals have owners (H13, H15).
5. **Not verifiable by me, and why that is not a defect.** The stored shape of `claude mcp add-json` (Task 5 probes it before code is written), codegraph behaviour on darwin/arm64, hook process-group survival inside Claude Code (spec marks it UNVERIFIED and records the outcome), Leg B (expected to ship `status`; plan and Phase 3 handle both), Coder's `timeout 60` interaction (the handoff asks the Coder agent to confirm). Each has a task that measures it or a stated fallback.

### Coder handoff (prompt + context): PASS

Checked: self-contained (goal, IronClaude contract, inline fallback facts with both SHA-256 values, leads marked as leads, hard ordering 1-5, cleanup scope, working rules, decision rules, done-means); the research instruction about keeping new worktrees and projects indexed is present and tells Coder to check IronClaude's hook first; PR target `IronbellyOrg/Coder` with `--repo` and URL check; progress comments on #323 with `--repo IronbellyOrg/IronClaude`. The guidance block in the context file (line 61) is identical to Phase 2 spec line 266 (`diff` printed nothing); the registration JSON equals spec line 91 except the placeholder wording; both files carry the markers and the "re-sync on every pin bump, do not append once" rule, the `MCP_TOOLS`-from-source rule and the two new `jq` done-means checks; `codegraph_explore` appears only to say it is hidden. Not verifiable: the Coder paths at commit `e25f787c` (the handoff itself says to re-check on current `main`).

### Scope note

Phases 1 and 3 each have a Self-Audit-worthy amount of correct work (coverage 205/205 files, 25/25 findings applied), but each also had one IMPORTANT defect in the first pass. Task X applied the two fixes in section 6 and task Q2 re-ran the check (section "Re-check (Q2)"): both phases are now PASS.

## Re-check (Q2)

Status: COMPLETE (task Q2, 2026-10-29). Reviewer: Q2 (did not produce the plans, the specs or the task X fixes). HEAD `55d40308`. Read-only: no source, plan, spec or ledger file was edited by Q2; the only file changed is this summary. `git status --short` still shows exactly the same seven untracked paths as at the start and no modified tracked file.

**Result: Phase 1 PASS, Phase 2 PASS, Phase 3 PASS, Coder handoff PASS. 0 findings (0 CRITICAL, 0 IMPORTANT, 0 MINOR).** Four observations (O-9 to O-12) need no change.

Read before checking: `orchestration/README.md`, `review/X-fixes-result.md`, this summary (sections 1 and 6), Phase 1 plan Tasks 11-15 and spec T10b (line 736) and the `acceptance-search.sh` block (spec lines 612-640), Phase 3 plan Task 3 (lines 70-75) and Task 13 (line 212) and spec T11 (line 287).

### Step 1. Q-I1 (Phase 1 Task 12 criterion 3 and spec T10b): PASS

The revised command (plan line 174, spec line 736, identical text):

```bash
rg -n --no-ignore 'write_memory|read_memory|list_memories|edit_memory|delete_memory' src/superclaude plugins/superclaude commands agents -g '!src/superclaude/skills/sc-reflect-protocol/SKILL.md' -g '!**/reflect.md' -g '!commands/sc-reflect.md' -g '!src/superclaude/commands/validate-roadmap.md'
```

I ran it with `-c` against today's tree (the plan has not run, so hits are expected). Output, 16 files:

```text
agents/sc-pm-agent.md:21                                               commands/sc-load.md:1
commands/sc-pm.md:20                                                   commands/sc-save.md:1
plugins/superclaude/agents/pm-agent.md:21                              plugins/superclaude/commands/load.md:1
plugins/superclaude/commands/save.md:1                                 plugins/superclaude/modes/MODE_Task_Management.md:24
src/superclaude/agents/pm-agent.md:21                                  src/superclaude/commands/load.md:1
src/superclaude/commands/save.md:1                                     src/superclaude/modes/MODE_Task_Management.md:24
src/superclaude/skills/sc-pm-protocol/SKILL.md:12                      src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:2
src/superclaude/skills/sc-task-protocol/SKILL.md:3                     src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:15
```

Every hit file, who clears it, and when (read from plan Tasks 11 and 12 and spec rows P85, P91, P96):

| Hit files | Cleared by | Before Task 12's check? |
|---|---|---|
| the 13 pm-family files (root `agents/sc-pm-agent.md`, `commands/sc-{load,pm,save}.md`; the plugin and `src/` copies of `pm-agent.md`, `load.md`, `save.md`, `MODE_Task_Management.md`; `sc-pm-protocol/SKILL.md`) | Task 11 (rows P1, P4, P5, P8, P11-P23, P27-P73); Task 11 criterion 2 requires these exact files clean with the longer 11-token pattern | yes (Task 11 runs first) |
| `sc-reflect-protocol/refs/remediation-handoff.md` (lines 179, 232) | Task 12, row P85 | yes (Task 12 itself) |
| `sc-task-protocol/SKILL.md` (91, 303, 319) | Task 12, row P91 ("STRICT-tier memory and `activate_project` steps") | yes |
| `sc-validate-roadmap-protocol/SKILL.md` (line 4 `allowed-tools`, 126-127, 138, 147, 155, 165, 980, 1005-1071) | Task 12, row P96 (ledger, terminology map, pattern log move to `.superclaude/memory/validate-roadmap/`) | yes (see O-9 for line 4) |

Excluded files and their five-name hit counts today: `sc-reflect-protocol/SKILL.md` 34, `src/superclaude/commands/reflect.md` 2, `plugins/superclaude/commands/reflect.md` 2, `commands/sc-reflect.md` 1, `src/superclaude/commands/validate-roadmap.md` 1. They are rewritten by Task 13 (reflect: `--onboard` bootstrap deleted, tool table rewritten) and Task 15 (validate-roadmap `allowed-tools`). `**/reflect.md` matches only three files under the search roots (`find`: `commands/sc-reflect.md`, `plugins/superclaude/commands/reflect.md`, `src/superclaude/commands/reflect.md`; the fourth name `src/superclaude/cli/roadmap/templates/reflect.md.j2` does not match), so the glob exempts nothing else. No unexcluded file owned only by Tasks 13-15 carries a hit.

Conclusion on the three questions:
- Correct: it is a valid `rg`, exit 0 with hits today, 0 hits only if Tasks 11 and 12 finish their rows. All 16 hit files are cleared by Task 11 or Task 12 itself, so the check does not depend on a later task.
- Cannot hit files that Task 12 is meant to leave for later: the only files Tasks 13 and 15 own for these names are exactly the five excluded ones (list above).
- The full-token check is still covered by Task 15. The `SER` pattern of `acceptance-search.sh` (spec line 620) contains all of `write_memory|read_memory|list_memories|edit_memory|delete_memory`, `activate_project`, `check_onboarding_performed`, `\bsummarize_changes\b`, `get_current_config`, `think_about_`, `prepare_for_new_conversation`, so Task 15 criterion 5 (`bash $PKG/artifacts/acceptance-search.sh serena src/superclaude plugins/superclaude commands agents`, plan line 212, same four roots, case-insensitive, `--no-ignore --hidden`) covers every token in every excluded file; the allowlist `ALLOW` exempts none of them (only `.serena/memories` text in the three `load.md` copies). Task 13 criterion 2 (plan line 185) already runs it over the reflect files. Task 12's old `-g '!.../refs/reflection-rubric.md'` exclusion is gone; the rubric has zero five-name hits (not in the output above), so nothing was hidden.
- Spec and plan agree: the spec says "T11a and T11c", the plan says "Tasks 13 and 15" (T11a = Task 13, T11b = Task 14, T11c = Task 15).

### Step 2. Q-I2 (Phase 3 Task 13 criterion 4 and spec T11 (5) and (6)): PASS

Revised commands (plan line 212; spec line 287 carries the same text, with the pipe written `\|` because the spec line is a table row, see O-10):

```bash
rg -n 'Bash\(codegraph \*\)|mcp__codegraph__\*' src/superclaude/{commands,skills,agents,core,hooks,modes} plugins/superclaude -g '!**/core/CODEGRAPH.md'
rg -n 'codegraph_explore|codegraph explore|codegraph context' src/superclaude/{commands,skills,agents,hooks,modes} plugins/superclaude -g '!**/core/CODEGRAPH.md'
```

Reasoning over the glob (ripgrep `-g` uses gitignore syntax; `!` makes it an exclusion; a pattern with no leading slash whose only slashes come from a leading `**/` matches at any depth):
- `**/core/CODEGRAPH.md` matches exactly the path suffix `core/CODEGRAPH.md`, so it covers `src/superclaude/core/CODEGRAPH.md` and its byte copy `plugins/superclaude/core/CODEGRAPH.md` (both created by Task 3 per plan lines 70 and 74; both directories already exist today).
- It does not match any other file name in `core/` (`CLAUDE.md`, `HOW-WE-WORK.md`, and so on), nor a `CODEGRAPH.md` outside a directory named `core`, nor `CODEGRAPH.md.bak`.
- Search (5) scans `src/superclaude/core`, so the `src/` guide needs the exemption; search (6) does not scan `src/superclaude/core` but scans all of `plugins/superclaude`, so the plugin copy needs it. The one glob serves both.

Proof by a throwaway fixture in `/tmp` (created with `mktemp -d`, removed afterwards; no repo file touched). Both guide copies held `Bash(codegraph *), mcp__codegraph__*, codegraph_explore, codegraph explore, codegraph context`:

```text
A. guide copies only, with the -g:     search (5) exit 1, search (6) exit 1      (print nothing)
B. same tree, without the -g:          src/.../core/CODEGRAPH.md:1, plugins/.../core/CODEGRAPH.md:1 (5), plugins/.../core/CODEGRAPH.md:1 (6)   (original defect reproduces)
C. stray strings added elsewhere, with the -g, all still reported:
   (5) plugins/superclaude/core/OTHER.md, plugins/superclaude/skills/y/CODEGRAPH.md, src/superclaude/commands/a.md,
       src/superclaude/core/OTHER.md, src/superclaude/hooks/h.sh, src/superclaude/modes/m.md, src/superclaude/skills/x/SKILL.md
   (6) plugins/superclaude/commands/c.md, plugins/superclaude/core/OTHER2.md, plugins/superclaude/skills/y/core_CODEGRAPH.md,
       src/superclaude/agents/ag.md
```

So only the guide copies are exempt: a wildcard or `explore` in any command, skill, agent, hook, mode, other `core/` file, or a `CODEGRAPH.md` outside `core/` is still caught. Real tree today: neither guide exists yet, so both commands print nothing (correct before Task 3). The guide itself stays guarded by its Task 3 test (plan line 74: `explore` and the mutating verbs only inside "Never", sentinel only in the two guide copies, byte-identical copy).

### Step 3. Package pins: PASS (all three packages)

```text
$ cmp specs/phase-1-removal-spec.md       TASK-WF-phase1RemovalSpe-.../source.md   -> (nothing)
$ cmp specs/phase-3-codegraph-adoption-spec.md TASK-WF-phase3CodegraphA-.../source.md -> (nothing)
$ cmp specs/phase-2-codegraph-install-spec.md  TASK-WF-phase2CodegraphI-.../source.md -> (nothing)

sha256sum (plan, source.md)                                                              progress.md line 2 (PLAN:)
P1 plan   374613e7427abfb6b85a84778f79e30cd8b24a24367bffd345a98d50ab8ed23c   == sha256=374613e7...ed23c
P1 source 9e30a216ebba4c63a6169f898b6084cf1cdafdabc04d6a010f8fa6981f72b82d   == source_sha256=9e30a216...b82d
P2 plan   15706bf97c1d78d69fdd76c74c4caac06e249a3894394c83bf3b2aa603c1d0e6   == sha256=15706bf9...d0e6
P2 source c21d42222b980c907a3578cde95e7c30dc177db0105e18e9587e9ea14e0f964f   == source_sha256=c21d4222...964f
P3 plan   bfc3635192de31cb2e6b3ce40ca12ae4cf17e2f79a546eca9755d6ca9e24c9a3   == sha256=bfc36351...c9a3
P3 source 71bd93e21b6e3277dfed1b5fb4cdebb66697818d90ad11d91722397aa90ef326   == source_sha256=71bd93e2...ef326
```

All six hashes equal the `PLAN:` pins (I compared the full values, not only the abbreviations shown). Phase 2 spec and plan were last modified at 20:35-20:36, while the Phase 1 and Phase 3 plans and specs carry the later 22:06 modification time of task X's fixes, so task X did not touch Phase 2.

### Step 4. Regressions from the fixes: none found

- Searched the Phase 1 plan, spec and `return-contract.yaml` for other copies of the five-name pattern: lines 162 (Task 11, correct 11-token form on 14 named files), 174 (revised), spec 620 (`SER`), 730 (T10a), 736 (revised). No stale copy of the old 11-token repo-wide command remains in Task 12 or T10b.
- Searched the Phase 3 plan and spec for the wildcard and `explore` patterns: plan lines 88, 104, 143, 155, 212 and spec lines 74, 287 use the patterns; lines 88 (core `CLAUDE.md` only), 104 (`src/superclaude/agents`), 143 (`{commands,skills,agents}`), 155 (the two new impact files) never scan `core/`, so the guide never trips them. Only line 212 needed the exemption.
- The plan's Task 12 criterion still says what it does (repo-wide, five names), and its closing note now names the exact later check (Task 15 `acceptance-search.sh serena ...`), which exists at plan line 212. Spec T10b names T11a/T11c; both exist in the spec table.
- `git status --short`: same seven untracked paths, no modified tracked file; fixes touched untracked planning files only.

### Findings

None. Observations (no change made, no verdict effect):

- **O-9** Task 12 does not name the `allowed-tools` line 4 of `sc-validate-roadmap-protocol/SKILL.md` (it carries `mcp__serena__read_memory` and `mcp__serena__write_memory`, plus find_symbol-style tools that belong to Task 15). Task 12 criterion 3 requires the two memory names to be gone, so an executor who leaves them sees the check fail, edits the line, and passes; a second pass, not an impossible check. Cheap hardening if F1 reopens the plan: add "and the memory entries of its `allowed-tools` line" to the P96 clause of Task 12.
- **O-10** Spec T11 (5)/(6) sit in a Markdown table row, so the pipe is written `\|`; `rg` would read `\|` as a literal pipe. The executed text is the plan bullet (plain `|`), and the plan says task text wins over `source.md`, so the executor uses the correct form. Same as before the fix.
- **O-11** `-g '!**/core/CODEGRAPH.md'` would also exempt a stray `core/CODEGRAPH.md` at some other depth under the search roots. None exists, and the Task 3 test confines the guide sentinel to the two real paths. Accepted.
- **O-12** The Task 12 check is deliberately blind to five-name residue in the excluded reflect and validate-roadmap files; Task 13 criterion 2 and Task 15 criterion 5 are the checks that see it (Step 1). Between Task 12 and Task 13 the repo can legitimately carry that residue; no commit in between is claimed green on the full-token search.

### Self-Audit (zero findings)

What I tried in order to break each fix, and why I conclude there is no defect:

1. **Q-I1 can still fail by construction?** I ran the command and mapped all 16 hit files to a plan task that runs at or before Task 12, reading Tasks 11-15 and spec rows P85, P91, P96 rather than the X report's table. The one place a hit could have no clear owner (validate-roadmap `SKILL.md` line 4) is covered by the criterion itself, so I logged it as O-9, not as an impossible check.
2. **Did the exclusions hide a real gap?** I checked what each excluded file's later owner proves: Task 13 criterion 2 (reflect files, full `SER` pattern) and Task 15 criterion 5 (all four roots). `SER` contains all eleven old tokens, and `ALLOW` exempts none of them. I also checked that `**/reflect.md` matches only the three intended files and that dropping the rubric exclusion hides nothing (zero rubric hits).
3. **Q-I2 can still hit the guide, or hide a real violation?** I tested the exact commands on a fixture: guide-only tree prints nothing; the same tree without the `-g` reproduces the original defect; seven wildcard files and four `explore` files placed in every other root, including a `CODEGRAPH.md` outside `core/` and a `core/OTHER.md`, are all still reported.
4. **Stale pins or stale snapshot?** `cmp` silent for all three packages and all six full SHA-256 values equal the `PLAN:` lines; Phase 2 files predate the Q review.
5. **Fix-introduced regressions?** I searched plan, spec and contract for stale copies of both commands, and checked the other Phase 3 `rg` searches for the same exposure (none scan `core/`). No other file changed; git shows the same seven untracked paths.
6. **Not verifiable by me, and why that is not a defect:** that Tasks 11 and 12 actually clear every listed row when an executor runs them (that is what the criterion proves at execution time), and ripgrep's behaviour on other versions (verified on this machine's `rg` only, with the exact flags the plan uses).
