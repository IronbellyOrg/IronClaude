# Task R: adversarial review of the Phase 1-3 specs and the Coder handoff (issue #323)

Status: COMPLETE (task R, 2026-10-29). Review only; no spec was edited. Result: 25 findings (3 CRITICAL, 10 IMPORTANT, 12 MINOR); every target FAILS (section 4).

## 0. Scope and method

Targets (read in full, 2026-10-29): `specs/phase-1-removal-spec.md` (827 lines), `specs/phase-2-codegraph-install-spec.md` (737), `specs/phase-3-codegraph-adoption-spec.md` (367), `handoff/coder-handoff-prompt.md` (79), `handoff/coder-handoff-context.md` (139). Evidence: `orchestration/README.md`, `inventory/{codebase-memory,serena}.md`, `research/codegraph-evaluation.md` (cited `EVAL`), and the source tree at HEAD `55d40308`.

Stance: adversarial. I assumed every spec has mistakes and looked for them. All paths below are relative to `.dev/codegraph-migration/` unless they start with `src/`, `tests/`, `plugins/` or `.github/`.

Commands I ran besides the searches in section 1 (all read-only):
- `uv run pytest tests/recommend/test_routing_refresh.py -q -p no:cacheprovider` → `248 passed` (used for finding X-8).
- `uv run pytest tests/cli/test_verify_sync_hooks.py -q -p no:cacheprovider` → `3 failed, 4 passed` (`test_V1_clean_tree_exits_zero`, `test_V2_missing_claude_hook_detected`, `test_V7_regression_to_master`; used for X-11).
- `printf 'a\n' | rg -c zzz; echo $?` → no output, `exit=1` (used for X-13).
- `jq` reads of `~/.claude.json` and `~/.claude/settings.json` (keys only), listings of `~/.codex`, `~/.config/opencode`, `~/.augment`, `~/.agents`, `~/.claude/{skills,agents}`.
- After every command `git status --short` printed only `?? .dev/codegraph-migration/`. No tracked file changed.

## 1. Re-run searches (rg commands and hit counts)

Run from the worktree root on 2026-10-29, HEAD `55d40308`.

```bash
EX=(--no-ignore --hidden -g '!.git' -g '!.dev/**' -g '!.claude/**' -g '!.specstory/**' -g '!.venv/**')
W1='codebase-memory|codebase_memory|CodebaseMemory|Codebase Memory|cbm|CBM_|DeusData|search_graph|trace_path|get_code_snippet|query_graph|index_repository|get_architecture|detect_changes|search_code|list_projects|\.superclaude-codebase-memory'
PAT='serena|Serena|SERENA|mcp__serena|serena-agent|\.serena|MCP_Serena|--serena|find_symbol|find_referencing_symbols|get_symbols_overview|replace_symbol_body|insert_after_symbol|insert_before_symbol|write_memory|read_memory|list_memories|onboarding'
SER=<the SER pattern of Phase 1 §8.0 acceptance-search.sh, copied verbatim>
```

| # | Command | Inventory figure | My result |
|---|---|---|---|
| R1 | `rg -n -i --hidden --no-ignore -g '!.dev/**' -g '!.claude/**' -g '!.git/**' -g '!.venv/**' -g '!.specstory/**' -e "$W1" . \| wc -l` (and `-l`) | 300 hits, 12 files (W1) | **300 hits, 12 files** |
| R2 | `rg -il serena "${EX[@]}" . \| wc -l` | 168 files (W2 A) | **168** |
| R3 | `rg -l "${EX[@]}" -e "$PAT" . \| wc -l`; `rg -n … \| wc -l` | 193 files, 981 lines (W2 B) | **193 files, 981 lines** |
| R4 | `rg -l -i "${EX[@]}" -e "$SER" .` (Phase 1 DoD-1 acceptance pattern) | not reported | **178 files, 1042 lines** |
| R5 | `git ls-files .serena \| wc -l` | 4 | **4** |
| R6 | `rg -il codegraph "${EX[@]}" . \| wc -l` | 0 (Phase 2 §0) | **0** |
| R7 | `rg -n -i 'serena\|codebase' .claude/settings.json .github src/superclaude/cli/user_settings_defaults.json` | `.claude/settings.json` no hit; CI hits in `test.yml` | **only `.github/workflows/test.yml:133` and `:155`** (both Phase 1 row C12) |

Coverage check (script): the union of the R1, R3 and R4 file sets is **203 files**; Phase 1 §1.1/§1.2 tables name **212 distinct paths**. `comm -23 union rows` printed **nothing**: every file with a hit is a Phase 1 row. The 9 row paths with no hit are expected (`.serena/.gitignore`, the moved calibration file, `.specstory/…`, `update.sh`, the C15 combined row, both `core/RULES.md`, both `freshness-pre-edit.sh`, which match only `relative_path` or `/sc:save`). Of the 31 rows marked "none (keep)", 7 hit R1 or R4, and all 7 are in the §2.4 allowlist regex (`CHANGELOG.md`, `POST-REFLECT-TASK.md`, `docs/memory/patterns_learned.jsonl`, `docs/memory/pm_context.md`, `src/superclaude/skills/ccsession-tag/install.sh`, `tests/skills/test_implement_severity_replay.py`, `tests/troubleshoot/fixtures/regression/sysbox-20260918/Fable-D3/REPORT.md`). So DoD-1 is reachable on file coverage. **No missing-file finding.**

User environment checked (read-only): `~/.claude/settings.json` `permissions.allow` has no `serena` or `codebase` entry; `~/.codex`, `~/.config/opencode`, `~/.augment`, `~/.agents` contain no `codebase-memory` or `serena` file; `~/.claude/skills` and `~/.claude/agents` have no such companion; `~/.claude.json` user `mcpServers` keys are `auggie,codebase-memory-mcp,context7,serena,tavily`; the live `serena` entry carries `"env":{}` (confirms Phase 2 D23); no local-scope (`projects.*.mcpServers`) `serena` or `codebase-memory-mcp` entry exists (count 0).

## 2. Findings

Severity: CRITICAL = the plan cannot meet a stated requirement or an acceptance check cannot pass as written; IMPORTANT = wrong result, red commit, or missing owner that an executor would hit; MINOR = wording, stale fact or fragile check. "Owner" names who should apply the fix (F1/F2/F3 are the run's finalizers for Phases 1/2/3).

### CRITICAL

**X-1. `CODEGRAPH_MCP_TOOLS` is not in Phase 2, and Phase 2 and Phase 3 depend on each other for it (cycle).**
- Where: Phase 2 §2.4 (registration JSON, line 91), §4.1 U12, §4.2 step 1; Phase 3 §0 G3 and "Gap rule" (lines 19, 24), T0 E-5 (line 269), H1 (line 337), P3-D1; handoff prompt line 16; handoff context §2.2 (line 41).
- Problem: `rg -n CODEGRAPH_MCP_TOOLS specs/phase-2-codegraph-install-spec.md` hits only line 102 (the "owned entry" env-key whitelist). The registered JSON sets only `CODEGRAPH_TELEMETRY` and `CODEGRAPH_NO_UPDATE_CHECK`. Without the key, codegraph lists only `codegraph_explore` (EVAL line 94: `DEFAULT_MCP_TOOLS = new Set(['explore'])`), so every Phase 3 primitive that names `codegraph_search`, `_node`, `_callers`, `_impact` names a tool the session never sees. Phase 3 makes the key conditional on its own T0 E-5 schema-cost experiment, which runs only after Phase 1+2 are merged (Phase 3 §7 "Start only after Phase 1 and Phase 2 are merged"), and then escalates to a human (H1) to change Phase 2's installer. No task in any phase edits the registration after Phase 2 ships. The coordinator brief (README line 40) assigns this to F2; it is not done. The Coder handoff tells Coder to "use exactly this JSON" (context line 44) and its contract test will pin today's shape, so a later env change also breaks the next pin bump.
- Fix (owner F2, with F3): move E-5 (the schema-cost check) into Phase 2: run it in the T9 layer-2 sandbox (two `tools/list` runs over stdio with the W4 client `/tmp/codegraph-eval.fQfO/scripts/mcp-client.mjs` pattern, with and without the key, compare schema bytes; pass ≤ 2K tokens per P3-D1). Add `"CODEGRAPH_MCP_TOOLS":"node,search,callers,callees,impact,files,status"` to the §2.4 JSON, the expected-entry compare, U12, and layer-2 step 1 (`jq -e '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS == "node,search,callers,callees,impact,files,status"' "$HOME/.claude.json"`), and a layer-2 `tools/list` assertion that `codegraph_explore` is absent and `codegraph_callers` present. Update handoff prompt line 16, context §2.2 and the prompt's "Done means" with the same `jq -e`. Phase 3: G3 becomes a plain check, delete the H1 path for G3 and the E-5 part of T0.

**X-2. Phase 2's core guidance (and the text Coder will seed forever) tells agents to start with `codegraph_explore`, which Phase 3 blocks and bans.**
- Where: Phase 2 §3.4 block (line 259); handoff context §2.3 (line 57) and prompt line 20; Phase 3 §1.1 rule 5, P3-D1, P3-D9, T11 check (6).
- Problem: Phase 2: "Start code-structure questions with `codegraph_explore`." Phase 3: explore is blocked by the tool list and no primitive may name it; T11 check (6) exempts `core/`, so this sentence survives Phase 3 and then points every main session at a tool that is not listed. Coder is told to append the block once, "guarded by its first line" (context line 55), so Coder workspaces keep the explore sentence even after IronClaude changes it.
- Fix (owner F2 for Phase 2 text, F3 for Phase 3 ownership): rewrite the block to start with `codegraph_search` / `codegraph_node` / `codegraph_callers` (the tools X-1 lists) and drop explore; Phase 3 T2 owns any later wording change of this block (add it to T2's Files and acceptance: `! rg -n codegraph_explore src/superclaude/core/CLAUDE.md`). In the handoff, replace "append once, guarded by its first line" with "replace the block between fixed begin/end markers from IronClaude `src/superclaude/core/CLAUDE.md` at the pinned SHA on every pin bump", and give the markers.

**X-3. Phase 2 and Phase 3 contradict each other on who runs `codegraph init`, and Phase 3's own mutating-verb check cannot pass.**
- Where: Phase 2 §3 (SessionStart hook, D2, D21) and §3.4 block; Phase 3 §1.1 rule 5 ("`init` runs only in user-typed `/sc:graph init`"), §2.1 item 6, §2.4 (drops "SessionStart init" hook, D-03), §3.2 Purpose ("nothing upstream indexes a new worktree"), §4 guide items 2 and 7, T6 and T11 (4) acceptance.
- Problem: Phase 2 ships a hook that runs `codegraph init --yes` on every new checkout, and its core-CLAUDE.md block tells the agent to run `codegraph init --yes` itself. Phase 3 was written as if neither exists. The T6/T11(4) command `rg -n 'codegraph (init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (on|off))' src/superclaude/{commands,skills,agents,core,hooks} | rg -v '^src/superclaude/commands/graph.md:'` must print nothing, but it will match (a) Phase 2's `src/superclaude/core/CLAUDE.md` text "run `codegraph init --yes`" and "Never run `codegraph status`, `codegraph index` or `codegraph sync`", and (b) Phase 3's own `src/superclaude/core/CODEGRAPH.md` §2 ("Who may run `codegraph init --yes`") and §7 ("run `codegraph install`, `upgrade` …"). The check fails deterministically.
- Evidence settles the conflict, so no adversarial run was spawned: Phase 2 merges first, its hook was chosen by `/sc:adversarial` (`decisions/P2-indexing-sync/adversarial/P2-indexing-sync-merged.md`) and narrowed by sandbox probes (`decisions/P2-indexing-sync/probe-results.md`), and it runs `init` detached with a sub-second hook return (Phase 2 §3.2 test list), which answers Phase 3's stated objection (1 s hook timeout, 4.5 s / 1 GB init in the foreground).
- Fix (owner F3): Phase 3 adopts Phase 2's model: the hook is the default indexer; `/sc:graph init` is the manual path (nested `-i`, hook disabled, failed init); rewrite rule 5, §2.1 item 6, §2.4 D-03 line, §3.2 Purpose, guide §2. Restrict the mutating-verb check to invocation forms in primitives, for example `rg -n 'Bash\(codegraph (init|index|sync|uninit|unlock|upgrade|install|uninstall|telemetry (on|off))' src/superclaude/{commands,skills,agents} plugins/superclaude/{commands,skills,agents} | rg -v '^src/superclaude/commands/graph.md:'`, and test the prose ban separately inside `CODEGRAPH.md`'s "Never" section only. Also align the guidance with Phase 2: use the binary in `~/.codegraph/.superclaude-bin` when present (see X-19).

### IMPORTANT

**X-4. The Phase 1 spec is not amended to Phase 2's Serena gate (T0b).**
- Where: Phase 1 DoD-3 (line 269), §2.3 row "Current-pin `serena` user registration" (line 290), §3.2 Tier R/Tier K (lines 315, 325), §3.4 re-register hint (line 354), §3.6 first row (line 368), T14 step 5 last sentence (line 760), §6.2 item (1) (line 453), D2 (line 811).
- Problem: `rg -c 'codegraph_ready|serena-local' specs/phase-1-removal-spec.md` prints nothing (0). Phase 1 still says the current-pin entry "is kept on every workspace", its Tier R matcher says "no `env`/`headers`" (the live entry has `"env":{}`, so `claude mcp add`-written Tier R shapes would be kept), and its hint registers under the name `serena`, which Phase 2's rule would then remove on the next run. If Phase 1 is executed from this text, its tests (§3.5) and CHANGELOG pin the opposite of Phase 2 §2.12, and T3b has to rewrite them. The combined plan still removes the entry (Phase 2 §2.12 + T3b + layer-2 step 6 + Coder step 2), so this is not CRITICAL, but the specs disagree.
- Fix (owner F1): apply Phase 2 T0b now, before Phase 1 runs, to every location listed above, and add to Phase 1 T3's test list: "`env: {}` and `headers: {}` count as absent" and "hint names `serena-local`". Phase 2 T0b's own acceptance lines (Phase 2 lines 437-441) are the check.

**X-5. Nobody owns the real-workspace "completely absent" check.**
- Where: Phase 2 §2.12 Acceptance (lines 204-207), §7 human item 4, §8 step 6; Phase 1 §10 last paragraph.
- Problem: the `jq` checks for user scope and local scope are written, but only the sandbox (layer 2 step 6) runs anything. After the merge, the human runs `./update.sh` (Phase 2 §7 item 4) with no command list, no expected output and no issue-#323 report. The user requirement in README line 36 is about the real workspace.
- Fix (owner F2): add Phase 2 task T12 "post-merge live verification" (human-triggered, executor-checked): `./update.sh`; restart Claude sessions; the two §2.12 `jq -e` commands; `jq -e '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS' ~/.claude.json` (X-1); `claude mcp get codegraph`; `superclaude install --list | rg 'Ready for Serena retirement: yes'`; post the outputs on #323. Coder's equivalent stays in the handoff "Done means".

**X-6. Phase 3 ignores Phase 1's actual gap policy and slots ledger.**
- Where: Phase 3 status line 7 ("still an empty stub"), §1.2 intro (line 72, "UNVERIFIED"), P3-D3; Phase 1 §4 G9 (line 396), T11, T15.
- Problem: `rg -n slots specs/phase-3-codegraph-adoption-spec.md` prints nothing. Phase 1 writes `.dev/codegraph-migration/handoffs/phase3-codegraph-slots.md` (one row per rewritten step, by anchor) exactly so Phase 3 can find each Grep/Read floor; Phase 3 never reads it and still designs for a "case B" that Phase 1's rule ("no step names a tool absent after Phase 1, at any commit", §4 decision) rules out. The README (line 39) assigns this reconciliation to F3.
- Fix (owner F3): make the ledger a Phase 3 input; drop case B; add a T0-style check that every ledger row maps to one §1.2 row: a short script listing ledger anchors not present in the §1.2 Anchor column must print nothing; and change §1.2's P1 column to cite the ledger row.

**X-7. Phase 3 row 31 regresses Phase 1's validate-roadmap floor to "skip".**
- Where: Phase 3 §1.2 row 31 (line 113); Phase 1 §4 G6 (line 393) and §4 decision ("the floor stays permanently").
- Problem: Phase 3: "If codegraph is unavailable or no symbols are found, skip — write no artifact". Phase 1 G6 replaced exactly that "skip" with a Grep-definition floor with the same 30-lookup cap. Applying row 31 deletes the floor.
- Fix (owner F3): row 31 = "codegraph tier first; if unavailable or empty, the Phase 1 Grep-definition floor (unchanged); never skip"; add to T5's test: Step 0.5 names both `codegraph_search` and `Grep`. Check rows 11 (reuse-auditor :131) and 17 the same way: the codegraph tier goes above the Phase 1 floor, it does not replace it.

**X-8. Phase 3's new commands turn an existing test red, and no task fixes it.**
- Where: Phase 3 T6, T7, T10 (T10 runs `tests/recommend/test_routing_refresh.py`).
- Problem: `tests/recommend/test_routing_refresh.py:639-640` asserts `shipped == active` where `shipped` is every `src/superclaude/commands/*.md` (`_COMMANDS`, line 26) and `active` comes from the frozen research package `.dev/tasks/*/TASK-RESEARCH-recommend-refresh-20261024-044336/` (line 28, 114), with `(len(active), …) == (43, 4)` at line 638. It passes today (248 passed). Adding `graph.md` (T6) and `impact.md` (T7) makes `shipped` 45, so the test fails from T6 until someone edits it; T10's acceptance then fails.
- Fix (owner F3): T6 and T7 each update that test in the same commit (add the new command to a "post-refresh additions" set the test subtracts, rather than editing the historical `.dev/tasks` package), and add `tests/recommend/test_routing_refresh.py` to T6's and T7's acceptance commands.

**X-9. Two phases write the codegraph row of the `core/CLAUDE.md` MCP table.**
- Where: Phase 2 F6 / §3.4 / T6; Phase 3 §1.2 row 1 and T2.
- Problem: Phase 2 adds `| codegraph | Code graph: symbols, callers, impact, file outlines | (auto) |`. Phase 3 row 1 treats the row as absent ("gap (row deleted)") and inserts its own, giving two codegraph rows. Phase 2 §9 says Phase 3 only maps the "Symbolic queries" refresh row.
- Fix (owner F3): hunk ownership is: Phase 1 deletes the `serena` row (`:21`), the `replace_symbol_body` item (`:90`) and rewrites `:112` to Grep/Read; Phase 2 adds the codegraph row and the guidance block; Phase 3 edits Phase 2's row in place (adds the `~/.claude/CODEGRAPH.md` path) and rewrites `:112` to codegraph. T2's test asserts exactly one table row starting `| codegraph`.

**X-10. Phase 3 has no Coder follow-up, so its guidance never reaches Coder users.**
- Where: Phase 3 §4 (lookup via the `core/CLAUDE.md` MCP row), §7; Phase 2 §3.4 "Coder gap"; handoff context §2.3.
- Problem: Coder's `ironclaude` slug restores the user's `~/.claude/CLAUDE.md` after install (context line 55), so the MCP-table row that tells a main session where `~/.claude/CODEGRAPH.md` is, and any Phase 3 change to the guidance block, never land on Coder. Phase 3 also merges to `master`, which the monitor turns into a Coder pin bump automatically (Phase 2 §8 facts).
- Fix (owner F3): add a Phase 3 task (with T12) that posts an addendum on issue #323 for the Coder agent with the new block text and the guide path, and, together with X-2's marker-based re-sync, makes Coder pick it up at the next pin bump. Acceptance: the comment URL is recorded in the decision log.

**X-11. Phase 2 T5's acceptance block can never exit 0.**
- Where: Phase 2 T5 acceptance (line 534) and the rule at line 429 ("every line must exit 0").
- Problem: the command includes `tests/cli/test_verify_sync_hooks.py`, which fails 3 tests at HEAD (observed: `3 failed, 4 passed`). The parenthetical says "check them against the baseline", but the block as written fails.
- Fix (owner F2): remove that file from the pytest line and add a baseline-diff line: `uv run pytest tests/cli/test_verify_sync_hooks.py -q -p no:cacheprovider -rfE --tb=no | grep -E '^(FAILED|ERROR) ' | sed 's/ - .*//' | sort | comm -13 .dev/codegraph-migration/evidence/P2-baseline-failures.txt -` prints nothing.

**X-12. Phase 1 T10 and T11 are too big for one commit and one acceptance gate each.**
- Where: Phase 1 T10 (memory rewrite, about 30 files with twins) and T11 (load-bearing tools: reflect SKILL.md with roughly 150 hit lines, troubleshoot skill + analyst + its worker test, validate-roadmap, reuse-auditor, auggie-reviewer, reflect-reviewer, rows D3-D5, `core/CLAUDE.md:112`, the slots ledger).
- Problem: one failing acceptance line blocks the whole set, a QA pass cannot review it in one context, and the §10 rule "fix within the task's files" becomes meaningless for a task that owns most primitives.
- Fix (owner F1): split T11 into T11a reflect (SKILL.md, refs, `commands/reflect.md` twins, D3-D5), T11b troubleshoot (skill, refs, command twins, `troubleshoot-analyst.md`, `test_diagnostic_worker_contract.py`), T11c validate-roadmap + reuse-auditor + auggie-reviewer + reflect-reviewer + `core/CLAUDE.md:112` + ledger completion; split T10 into T10a commands/agents/modes/pm (save, load, pm, pm-agent, MODE_Task_Management) and T10b skills (pm-protocol, task-protocol, validate-roadmap memory, reflect memory, crash-recovery, HOW-WE-WORK and copies, calibration `git mv`). Keep each piece's acceptance as the matching subset of today's command, and run `acceptance-search.sh serena` only on the last piece.

**X-13. Phase 3 T0's acceptance uses `rg -c` expecting "0".**
- Where: Phase 3 T0 acceptance (line 269), last command `git worktree list | rg -c cg-sandbox` "(last command must print `0`)".
- Problem: `rg -c` prints nothing and exits 1 when nothing matches (observed). The `&&` chain therefore fails exactly when cleanup succeeded.
- Fix (owner F3): replace with `! git worktree list | rg -q cg-sandbox`.

### MINOR

**X-14. Two kill switches with different names.** Phase 2 hook: `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0` (line 236); Phase 3 primitives: `IRONCLAUDE_CODEGRAPH=off` (lines 200, 214, 249). A user who sets one expects both. Fix (F3): Phase 3 reuses the `SUPERCLAUDE_CODEGRAPH_*` prefix (for example `SUPERCLAUDE_CODEGRAPH=off` disables primitives and the hook), or the guide and `docs/user-guide/mcp-installation.md` name both with what each does.

**X-15. Phase 1 deletes a CI step that Phase 2 re-adds in the same merge unit.** Phase 1 row C12 / T12 delete `.github/workflows/test.yml:155-159` ("Install Claude CLI"); Phase 2 F12 / T8 restore it from `55d40308`. Fix (F1): Phase 1 keeps the step and only rewrites its comments (`:133-134`, `:155`); drop Phase 1 T14 step 6 or keep it as a local simulation; Phase 2 T8 then only renames comments.

**X-16. Phase 1 T3 acceptance runs `uv run superclaude install --list` on the real HOME,** while Phase 1 §10 says "Never run … `superclaude install` … against the real `HOME`". Fix (F1): run it with `HOME=$(mktemp -d)` and a stub `claude`, or state in §10 that `--list` is the one read-only exception.

**X-17. Phase 1 T5's first acceptance search does not exclude the allowlisted retire-step files.** `rg -n "install_codebase_memory|codebase_memory" src tests` will hit any `codebase_memory` identifier in `install_retired_mcp.py` or its test, which §2.4 allows. Fix (F1): add `-g '!src/superclaude/cli/install_retired_mcp.py' -g '!tests/cli/test_install_retired_mcp.py'`, or rely on the `acceptance-search.sh cbm src tests` line alone.

**X-18. Phase 3 carries stale UNVERIFIED notes and an unverified read method.** §0 G1 says the pin file is unknown (Phase 2 defines `VERSION = "1.6.2"` in `src/superclaude/cli/install_codegraph.py`, Phase 2 F1); G3 reads env through `claude mcp get codegraph | rg CODEGRAPH_MCP_TOOLS` (whether `mcp get` prints env is UNVERIFIED; Phase 2 §4.2 notes also mark `mcp get` UNVERIFIED). Fix (F3): cite the pin file; G3 = `jq -r '.mcpServers.codegraph.env.CODEGRAPH_MCP_TOOLS' ~/.claude.json`.

**X-19. Phase 3 calls bare `codegraph` where Phase 2 says the registered binary may not be on PATH.** Phase 2 §2.2 writes `~/.codegraph/.superclaude-bin` because `~/.local/bin` may be off PATH (macOS); Phase 3 allowlists `Bash(codegraph --version)` etc. Fix (F3): the guide says CLI access requires `command -v codegraph` to resolve, else record `graph:absent` for CLI access (MCP still works).

**X-20. Phase 3 has no `CHANGELOG.md` entry** for `/sc:impact`, `/sc:graph` and `CODEGRAPH.md` (Phases 1 and 2 each add one). Fix (F3): add `CHANGELOG.md` to T11 Files with `rg -q 'sc:impact' CHANGELOG.md && rg -q 'sc:graph' CHANGELOG.md`.

**X-21. Phase 2 §3.1 overstates what `alwaysLoad` does.** "registered with `alwaysLoad`, so every session connects" (line 223); EVAL line 77 says `alwaysLoad` stops Claude Code deferring the tools behind tool search, not that it causes connection. Fix (F2): reword to "every session that loads MCP servers connects; `alwaysLoad` keeps the tools listed rather than deferred".

**X-22. Phase 3 T3's Files column contradicts row 5.** It says the `TOOLS` set "becomes the 4 native tools + the 4 codegraph names", while row 5 makes the codegraph names conditional on T0 E-6. Fix (F3): "becomes the roster E-6 selected for `troubleshoot-analyst`".

**X-23. Phase 3 T11 (8) has no baseline comparison.** "Targeted tests: the union of every task's pytest command" must pass, but baseline (b) before T1 records existing failures. Fix (F3): "no failing test id outside baseline (b)", with the `comm -13` form Phase 1 T14 step 2 uses.

**X-24. Phase 1 row S19 contradicts itself.** `docs/memory/pm_context.md`: action "reword the Serena clause only", Task "none (keep)", and the file is allowlisted in §2.4. Fix (F1): either keep it unchanged (history) or give it to T12 and remove it from the allowlist regex.

**X-25. "An explicit list blocks every tool it does not name" is source-cited, not observed.** Phase 3 G3 and P3-D1 rely on it; EVAL line 94 cites `tools.ts:2926-2929`, but the only hands-on run with `CODEGRAPH_MCP_TOOLS` (EVAL lines 212-213) included `explore` in the list. Phase 3 G5 does check the session tool list, so it is falsifiable. Fix (F2/F3): mark it UNVERIFIED in P3-D1 and make the X-1 layer-2 `tools/list` assertion (explore absent) the proof.

## 3. Checks by review question

### 3.1 Coordinator concerns (README lines 35-41)

| Concern | Result | Finding |
|---|---|---|
| Current-pin Serena registration removed on existing workspaces after update: who, when, acceptance | Removed by IronClaude's retire step once `codegraph_ready()` holds in the same `superclaude install` run (Phase 2 §2.12, task T3b), reached by `./update.sh` (`update.sh:8`) and by Coder's SHA-change slug run; Coder step 2 stops the bundle re-adding it, with a guarded backstop in `T/scripts/startup.sh` (handoff prompt line 48). Sandbox acceptance exists (Phase 2 layer 2 step 6 seeds the exact live shape with `"env":{}` and asserts removal). Real-workspace acceptance has no owner. | not CRITICAL; X-4, X-5 |
| Phase 1 amended to the Serena gate (T0b) and the two specs agree | Not amended (0 hits for `codegraph_ready`/`serena-local` in Phase 1) | X-4 |
| Residuals `./update.sh` cannot remove | `/usr/local/bin/codebase-memory-mcp`: owner Coder step 5 image, acceptance `! command -v codebase-memory-mcp` (Phase 2 §2.12, prompt "Done means"). Kind-B `~/.local/bin/codebase-memory-mcp` + companions: owner the user via the printed absolute `uninstall -y` command; acceptance: layer 2 step 6 asserts the binary is left and `uninstall -y` is printed. Both have an owner and a check. | none |
| Phase 3 reconciled to Phase 1's floor + slots ledger | Not done | X-6, X-7 |
| `CODEGRAPH_MCP_TOOLS` present in Phase 2 | Absent | X-1 |
| Every "tests stay green" check compares to a recorded baseline | Phase 1 T0/T14 yes; Phase 2 baseline + T10 yes, but T5 no (X-11); Phase 3 baseline (b) recorded but T11 (8) does not compare (X-23) | X-11, X-23 |

### 3.2 Task boundaries
Too big: Phase 1 T10, T11 (X-12); Phase 3 T8 (reflect rebuild) is large but has one owner file set and a specific test list, so not flagged. Wrongly split across phases: the CI step (X-15), the core MCP row (X-9), indexing ownership (X-3), the tool-list env key (X-1). Overlaps that are fine because the later phase edits in place by anchor: tasklist §5.5 STRICT row (Phase 1 P92, Phase 3 row 35), reflect §6.1.1 envelope retitle (Phase 1 G4, Phase 3 row 23), `--with-hierarchy` (Phase 1 deletes the step, Phase 3 row 26 deletes the flag; a dead flag exists only between the two merges, accepted).

### 3.3 Dependencies, ordering, green at each commit
- Cross-phase order is consistent in all three specs and the handoff: Coder steps 1-2 on Coder `main` → IronClaude Phase 1+2 as one `master` merge (Phase 1 §2.2, Phase 2 §8 and T11 merge gate) → Coder pin bump → Coder step 5 → Phase 3 from `origin/master` (Phase 3 §7). Phase 3 changes no installer, so its merge (auto pin bump) is safe for Coder unless X-1 is fixed in Phase 3 instead of Phase 2; it must not be.
- Cycle: Phase 2 registration ↔ Phase 3 T0 E-5 (X-1).
- Phase 1 within-phase: I traced T1→T5 (tests ported before deletion, fixture and `main.py` in one commit, retire step before the helpers' other callers are deleted) and T6→T11 (halt-set change first is safe per G7) and found no red commit beyond the fragile T5 search (X-17).
- Phase 2 within-phase: T5 acceptance red by construction (X-11). Between T3 (required phase) and T8 (CI step restored) the `doctor-check` CI job would fail, but CI runs only on `master`/`integration` pushes and PRs (Phase 1 D14), and the PR is opened in T11, so no red CI run occurs.
- Phase 3 within-phase: red from T6 to the fix (X-8); T6/T11(4) check cannot pass (X-3); T0 check cannot pass (X-13).

### 3.4 Shared files: hunk ownership

| File | Phase 1 owns | Phase 2 owns | Phase 3 owns | Conflict |
|---|---|---|---|---|
| `src/superclaude/cli/install_mcp.py` | deletes cbm/Serena registry entries, native functions, `--uninstall/--yes`; adds `_remove_exact_user_entry` + direct-exec `claude` wrapper | adds `codegraph` entry, dispatch, `install_codegraph_mcp`, re-created add/restore helpers, `codegraph_ready()` | none | none (Phase 2 T2 step 2 adapts mechanically) |
| `src/superclaude/cli/main.py` | deletes cbm phase, `--list` block, `native_success`; adds retire-step call, retired `--list` lines, `update` notice | adds codegraph phase before the retire step, exit term, `--list` block, passes `codegraph_ready()` | none | none |
| `src/superclaude/cli/install_retired_mcp.py` + test | creates (Tier R/K, receipt cleanup) | adds the §2.12 gate (T3b) | none | X-4 (Phase 1 text not amended) |
| `docs/user-guide/mcp-installation.md` | deletes cbm sections `:5-26`, `:206-242`, `:309-324`, Serena rows | adds "Default setup: codegraph" where `:5-26` was, opt-out, removal, `serena-local` | none (could add the two commands; not planned) | none |
| `src/superclaude/core/CLAUDE.md` | deletes `:21` row, `replace_symbol_body` at `:90`; `:112` → Grep/Read | adds codegraph MCP row + guidance block | edits Phase 2's row in place; `:112` → codegraph | X-2, X-9 |
| `src/superclaude/core/HOW-WE-WORK.md` + `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (byte copy) | lines 237, 327, 329 (memory wording), outside the level table | none | `other-commands` table rows for `/sc:graph`, `/sc:impact` (T10), byte copy | none; neither touches the level table, so `src/superclaude/core/CLAUDE.md:50-67` copy is unaffected |
| `src/superclaude/hooks/hooks.json` + plugin twin | matcher `Edit\|Write` | new SessionStart entry | none | none |
| `plugins/superclaude/` mirror | hand edits in the same commit (Phase 1 D15) | hook script + hooks.json copy (`cmp` in T5) | mirror rule §1.2, `core/CODEGRAPH.md` byte copy | none |
| `tests/cli/test_update_command.py`, `tests/cli/test_install_mcp_registry.py`, `tests/unit/test_cli_install.py`, `tests/cli/test_install_hooks.py` | removal edits | codegraph additions | `test_cli_install.py` lists gain new commands/skills/core file | none |
| `.github/workflows/test.yml` | deletes Claude CLI step | restores it | none | X-15 |
| `CHANGELOG.md` | removal entry | codegraph entry; T7 checks Phase 1 entry wording | none | X-20 |

### 3.5 Missing work (question 4)
File coverage: complete (section 1). Environment items: user-scope registrations (Phase 1 §3 + Phase 2 §2.12), local-scope (reported, printed command; none live here), settings.json permissions (none live; Phase 2 D5 adds none), project `.claude/settings.json` (no hit, untouched), CI (`test.yml` only), CHANGELOG (Phases 1-2 yes, Phase 3 no: X-20), plugin mirror (all phases), `make verify-sync` (Phase 1 T9-T11/T14, Phase 2 T5/T10, Phase 3 T11; note `verify-sync` checks only `src/` ↔ `.claude/`, not `plugins/`, `Makefile:166-178`; each phase compensates with `cmp`/parity tests), installed-path rule (Phase 3 lookup line with the labelled fallback; Phase 1 memory paths are project-relative), Serena memory replacement (Phase 1 §5, T10), codex/opencode companions (none on this workspace; kind-B workspaces get the printed upstream `uninstall`, Phase 1 §2.3). No further missing-work finding beyond X-5, X-8, X-10, X-20.

### 3.6 Acceptance checks (question 5)
Every task in all three specs has a concrete command. Broken or unfalsifiable ones: X-3 (Phase 3 T6/T11(4)), X-11 (Phase 2 T5), X-13 (Phase 3 T0), X-17 (Phase 1 T5, fragile), X-23 (Phase 3 T11(8)). Phase 2 T6 acceptance `grep -n 'codegraph' src/superclaude/core/CLAUDE.md # expect: …` passes on any single mention; tightening it is folded into X-2's fix (assert the row and `! rg codegraph_explore`).

### 3.7 Feasibility against EVAL (question 6)
Tool names (`codegraph_search/node/callers/callees/impact/files/status/explore`), `serve --mcp`, `init --yes`, telemetry and update-check env names, the four SHA-256 values, `add-json` with `alwaysLoad`, default tool listing: all match EVAL lines 59-96 and Phase 2 §0. Unverified claims driving tasks: `CODEGRAPH_MCP_TOOLS` hiding explore (X-25), `alwaysLoad` meaning (X-21), `claude mcp get` printing env (X-18). Phase 2 already gates `add-json` stored shape (T2 step 1) and `claude mcp get` in a sandbox (§4.2 notes), which is correct.

### 3.8 Handoff quality (question 7)
Self-contained: yes (goal, IronClaude contract, inline fallback facts with hashes, leads, ordering, cleanup scope, working rules, decision rules, done-means). Research instruction about new worktrees/projects: yes (prompt lines 41-43, including "check IronClaude's hook first"). Ordering with the pin: yes (lines 45-53, matches Phase 2 §8). PR target `IronbellyOrg/Coder` with `--repo` and URL check: yes (line 63). Progress comments on #323 with `--repo IronbellyOrg/IronClaude`: yes (line 64). Defects: X-1 (registration JSON), X-2 (explore guidance, append-once), X-10 (no channel for Phase 3 updates).

### 3.9 Autonomy (question 8)
Decision rules (simple / mid → adversarial quick / complex → adversarial standard, with logs): present in Phase 1 §10, Phase 2 §7, Phase 3 §7 and the handoff. Issue-#323 comments with `--repo IronbellyOrg/IronClaude`: Phase 1 §9 (per group), Phase 2 §6 (per group, `--body-file`), Phase 3 §6 (per marked group), handoff line 64. Human points: Phase 1 none during execution (merge and live `./update.sh` listed as user actions); Phase 2 five, all justified (auth, hash mismatch, merge, live update, giving the prompt to a Coder agent); Phase 3 H1 is avoidable once X-1 is fixed in Phase 2 (G1/G2/G4 failures would remain as H1), H5 is justified only if a headless session cannot be started, H3/H4 are reasonable. No further finding.

## 4. Verdicts

Rule: any finding of any severity is FAIL.

| Target | Findings | Verdict |
|---|---|---|
| `specs/phase-1-removal-spec.md` | X-4, X-12 (IMPORTANT); X-15, X-16, X-17, X-24 (MINOR) | **FAIL** |
| `specs/phase-2-codegraph-install-spec.md` | X-1, X-2 (CRITICAL); X-5, X-11 (IMPORTANT); X-14 (shared), X-15 (shared), X-21, X-25 (MINOR) | **FAIL** |
| `specs/phase-3-codegraph-adoption-spec.md` | X-1 (shared), X-3 (CRITICAL); X-6, X-7, X-8, X-9, X-10, X-13 (IMPORTANT); X-14, X-18, X-19, X-20, X-22, X-23, X-25 (MINOR) | **FAIL** |
| `handoff/coder-handoff-prompt.md` | X-1, X-2 (CRITICAL); X-10 (IMPORTANT) | **FAIL** |
| `handoff/coder-handoff-context.md` | X-1, X-2 (CRITICAL); X-10 (IMPORTANT) | **FAIL** |

No target has zero findings, so no Self-Audit is required. For the record, what passed: Phase 1 file coverage (0 hit files without a row; all 7 hitting keep-rows allowlisted), the cross-phase merge order and Coder ordering, the residual-owner table, PR targets, issue-#323 reporting and decision rules in every phase.

Fix order for the finalizers: F2 first (X-1, X-2, X-5, X-11, X-21, X-25 and the handoff), because F3's reconciliation (X-3, X-6 to X-10, X-13, X-14, X-18 to X-20, X-22, X-23) depends on Phase 2's final registration and guidance text; F1 (X-4, X-12, X-15 to X-17, X-24) is independent and can run in parallel.

## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| Do not spawn `/sc:adversarial` for the Phase 2 vs Phase 3 indexing contradiction (X-3) | spawn one run; settle from evidence | self | The task allows a run only when evidence cannot settle a contradiction. Here it can: Phase 2 merges first, its hook came from an adversarial run plus sandbox probes, and its detached design answers Phase 3's stated objection; Phase 3 was written without the Phase 2 spec (its §0 G1 says so) |
| Rate X-4 IMPORTANT, not CRITICAL | CRITICAL per README line 36; IMPORTANT | self | README makes it CRITICAL only if the combined plan fails to remove the registration. It does remove it (Phase 2 §2.12, T3b, layer-2 step 6, Coder step 2); the defect is the disagreeing Phase 1 text and the missing live check (X-5) |
| Rate X-3 and X-1 CRITICAL | IMPORTANT | self | X-3's acceptance cannot pass as written; X-1 leaves every Phase 3 primitive naming unlisted tools, with no task in any phase that can fix the registration |
| Count file coverage as passing instead of raising per-file findings | list every row | self | The scripted `comm` of fresh results against Phase 1 rows printed nothing (section 1) |
| Run two specific test files (`tests/recommend/test_routing_refresh.py`, `tests/cli/test_verify_sync_hooks.py`) | rely on reading the code | self | README allows specific files to confirm a claim; both runs left `git status` clean |
