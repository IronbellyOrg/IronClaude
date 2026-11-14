# Research: Integration Points

**Topic type:** Integration points (contract rules, routing docs, sync copies, tests that pin them)
**Scope:** `src/superclaude/core/WORKER-CONTRACT.md`, `tests/skills/test_worker_contract.py`, design section 9 rows R1-R8, HOW-WE-WORK copy/level-table sync and its tests, `.gitignore` `.dev/` rules, Makefile `sync-dev` / `verify-sync`
**Status:** Complete
**Date:** 2026-11-08

---

## IP-1. `src/superclaude/core/WORKER-CONTRACT.md` (WC-14 + never-as-worker list)

### Current rule list and the free ID

- Terms section `## 1. Terms` at `WORKER-CONTRACT.md:9`; command-side rules `## 2.` at :26 (WC-2 :30, WC-4 :31, WC-8 :39, WC-9 :40, WC-10 :45, WC-11 :46); worker duties `## 3.` at :48 (WC-3 :52, WC-5 :58, WC-7 :59, WC-12 :60, WC-13 :61); coordinator rules `## 4.` at :64 (`### WC-6` :68).
- Highest existing ID is WC-13 (`WORKER-CONTRACT.md:61`). No WC-1 rule exists in the file. **Free next ID: WC-14** (matches design `docs/designs/orchestrator-mode.md:668`).

### Never-as-worker term line (line 23)

- `WORKER-CONTRACT.md:23` today: `` `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while ... ``
- Target (design `orchestrator-mode.md:684`): `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard` ``. Only the list changes; the line must stay ONE line (`tests/skills/test_worker_contract.py:399-400` asserts exactly one line contains `**Never-as-worker list**`).

### Section 4 insertion point for WC-14

- `### Fan-in rule (several workers, then one merge)` at `WORKER-CONTRACT.md:154`, paragraph :156; `### Worked example: gate hit, answer, new Task` at :158. WC-14 goes between :156 and :158 (design `orchestrator-mode.md:663`). Final text: fenced block at `orchestrator-mode.md:668-670` (heading `### WC-14. Coordinator loop` + one paragraph).
- Interaction check: `_check_repo_setup_gated` (`test_worker_contract.py:446-461`) fails on any contract line carrying a code span that starts `make|bash|sh|uv|python|...` (regex :430-436) or `--setup run/--run-hooks/--setup inherit` without the gate phrases. The WC-14 paragraph (`orchestrator-mode.md:670`) has only the span `` `/sc:sweep` `` -> no hit. Do not add a `uv run ...` or `make ...` span to WC-14.
- No test checks the order or count of `###` headings in section 4. `_template_lines` (`test_worker_contract.py:407-410`) splits on `## 5. Coordinator brief template` (:381), so a new `###` before section 5 does not affect the guard-line check.

## IP-2. `tests/skills/test_worker_contract.py` (pins)

This is the only file under `tests/` that references `WORKER-CONTRACT`, `WC-13`/`WC-14` or the never-as-worker list (Grep over `tests/`, 1 file).

| Pin | Location today | Edit | Test that fails if wrong |
|---|---|---|---|
| `RULE_PHRASES` | dict starts `test_worker_contract.py:25`; WC-13 entry :155; closes :237 | Add `"WC-14": ("WC-14", ["WC-14. Coordinator loop", "On every coordinator wake", "it is never posted", "It never stops watching on its own"])` (design `orchestrator-mode.md:677`) | `test_contract_states_rule[WC-14]` (:540-542) via `_check_rule` (:388-395): every phrase present AND `WC-14` on the line of the first phrase (the heading satisfies it). `test_rule_check_fails_when_rule_removed[WC-14]` (:587-594) is auto-parametrized from the dict. |
| `NEVER_AS_WORKER` | tuple `:245-254`, 8 entries, `/sc:pr-submit` last | Append `"/sc:sweep"` -> 9 entries (design :678) | `test_never_as_worker_list_names_all_seven_commands` (:545-546) via `_check_never_as_worker` (:398-404, regex `` `<cmd>` `` on the single term line); `test_never_as_worker_check_fails_when_command_removed[/sc:sweep]` (:624-633) auto-parametrized. |
| **The rename** | `def test_never_as_worker_list_names_all_seven_commands():` at :545 | Rename to `test_never_as_worker_list_names_every_listed_command`; body unchanged (design :679). The old name is already stale (8 entries). No other file under `tests/` names it. | Rename only; no assertion changes. |
| `UNATTENDED_COMMANDS` negative | `assert "load" not in UNATTENDED_COMMANDS` at :865 inside `test_load_usage_line_declares_checkpoint_and_load_is_not_converted` (:861) | Add `assert "sweep" not in UNATTENDED_COMMANDS` after :865 (design :680) | Itself. |
| Set-equality (no edit) | `_check_no_unattended_sections` :464-472; test :553-554 | None. Globs `COMMANDS_DIR` (:20) for `^## Unattended mode` and requires set == `UNATTENDED_COMMANDS` (:379) | Fails if `sweep.md` ever gets a `## Unattended mode` heading. |
| Optional (not in design) | `NOT_CONVERTED_IN_P1` :878-888 parametrizes :1015-1017 | Design does not add `"sweep"`; redundant with the set-equality test. Builder decision, not a requirement. | - |

No test counts WC rules: no `len(RULE_PHRASES)`; `len(` in the file is only the P1 set count (:899-900) and line helpers (:496-497).

**Ordering:** WC-14 text, line-23 change and the four pins land in one step/commit; a pin without its text fails `test_contract_states_rule[WC-14]` / `test_never_as_worker_list_names_*`. Design gate: steps 1.17-1.19 only after GQ-11 (step 1.0b) and the PR #422 overlap check (step 1.16a) (`orchestrator-mode.md:661`).

### DESIGN GAP: a fifth pin the design misses (`RULE_PHRASES["never-as-worker"]`)

- `test_worker_contract.py:86-92` pins the never-as-worker term line by its exact text: `` "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, " "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers" `` (ident `**Never-as-worker list**`, :87).
- The design's new line 23 (`orchestrator-mode.md:684`) reads `` `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard` ``, so this phrase no longer occurs -> **`test_contract_states_rule[never-as-worker]` fails**. Design section 8 (`orchestrator-mode.md:675-680`) lists only four pin edits and does not mention this one.
- Required edit (same commit as line 23): change :89 to `` "`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:sweep` and `/sc:swarm-wizard`, " ``. `test_rule_check_fails_when_rule_removed[never-as-worker]` (:587-594) then keeps working unchanged.
- Researcher 4 (R3 design fixes) may want this as a design fix; flagged here because it is an integration break.

## IP-3. Write-verb audit (AC-0.9) reaches the new command and skill

- `test_worker_contract.py:1090-1094` `AUDIT_ROOTS` = `src/superclaude/{skills,commands,agents}`; `WRITE_VERB_RE` (:1098-1101) matches `git [-C x] add|commit|push|merge|stash|update-ref|worktree add|worktree remove` and `gh pr|gh api` as whole words. Every hit line, keyed by (repo-relative path, verb, stripped line) (:1131-1152), must be a key of `WRITE_VERB_CLASSIFICATION` (:1166) or `test_every_write_verb_hit_is_classified` (:2199) fails; stale keys fail `test_classification_table_has_no_stale_entries` (:2203). Categories (:1103-1105): `wc9-allowed`, `deferred:P1-4`, `never-worker`, `no-command`, `read-only`.
- Impact: any line in the new `src/superclaude/commands/sweep.md` or `src/superclaude/skills/sc-sweep-protocol/**` that names e.g. `git stash`, `git worktree remove`, `git merge` or `gh pr` (even in a "never" sentence) needs a classification entry (`read-only` for prose that forbids, per :1086-1087; or `never-worker`, since sweep joins the list). Cheapest path: word the skill so no such literal appears ("no stop, retry, release, merge or removal" has no `git ` prefix, so no hit). `src/superclaude/core/` (WC-14) and `src/superclaude/cli/` (the sweep Python) are not in `AUDIT_ROOTS`.
- Order: classify in the same step that writes `sweep.md` / the skill.

## IP-4. Routing rows R1-R8 (design `orchestrator-mode.md:688-708`)

Anchors re-verified today:

| # | Target and exact location (verified) | Test that checks it and what it asserts | Ordering |
|---|---|---|---|
| R1 | `src/superclaude/core/HOW-WE-WORK.md`: `<!-- other-commands:v1 -->` :318, header :320-321, `/sc:spawn` row :333, closing prose :335, `<!-- /other-commands -->` :337. New row goes after :333. | `tests/core/test_how_we_work_routing_table.py::test_other_commands_membership_and_live_references` (:291-311): exactly one of each marker; order level-end < other-begin < route-begin; the set of first-cell `` `/sc:x` `` tokens in rows after the header **equals** `_OTHER_COMMANDS` (:296-297); members exclude a fixed set (:299-309, sweep not in it); every `` `/` `` token in the block resolves to `src/superclaude/commands/<name>.md` (:310-311 via `_command_text` :142-154). Also `test_guide_is_ascii_except_the_ruling_example` (:342-347): every new line ASCII. | Needs `src/superclaude/commands/sweep.md` to exist first (live reference). Needs R4 in the same commit (set equality). Needs R3 in the same commit (parity). |
| R2 | Same file, `## Orca coordination` :396; never-workers bullet :403; next bullet (`Orca creates the worktrees`) :404. New bullet between :403 and :404. | No test reads this section by content (grep of tests for `Orca coordination` found none). Checked only by ASCII test (:342) and by R3 parity. | Same commit as R3. |
| R3 | `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` = byte copy of the src guide after R1+R2. | `tests/commands/test_routing_plugin_parity.py:38` `filecmp.cmp(_GUIDE, _PLUG_SKILL / "refs/HOW-WE-WORK.md", shallow=False)`; same test (:29-37) also asserts the plugin skill tree == src `sc-recommend` tree + `refs/HOW-WE-WORK.md`, byte-equal. | Same commit as R1/R2 (design rule `orchestrator-mode.md:705`). |
| R4 | `tests/core/test_how_we_work_routing_table.py` `_OTHER_COMMANDS` set :27-40 (`"sc:spawn"` at :33). Add `"sc:sweep"`. | Itself (:297). | With R1. |
| R5 | `tests/recommend/test_routing_refresh.py:33` `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` -> add `"sweep"`; comment :29-32 names the issues that added each (add issue #339 for sweep). | `test_command_dispositions_trace_appendix_c_and_inventory` (:617-665): `shipped = {stems of src/superclaude/commands/*.md minus README}` and asserts `shipped - _POST_REFRESH_ADDITIONS == active` (:647-648), where `active` is the 43 Active commands of the frozen package `.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/SPEC-sc-recommend-refresh.md` (present, Glob verified). | **Triggered by creating `sweep.md`, not by the guide.** Must land no later than the step that creates `sweep.md`; landing earlier is safe (a set difference with a non-member is a no-op). |
| R6 | `docs/user-guide/commands.md` `### 8. UTILITIES` :105; table header :107-108; `/sc:issue` row :115; `/sc:recommend` row :116. New row between :115 and :116. Row format is `` | `/sc:x` or [`/sc:x`](#anchor) | Purpose | `x.md` | Changes files? | `` (:109-118). | None (no test under `tests/` reads `docs/user-guide/commands.md`; grep for `user-guide` hits only unrelated files). Manual review. | Any time after `sweep.md` exists. |
| R7 | `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md:991`: `` ... `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` ... `` -> insert `` `/sc:sweep` `` as in line 23. | None (no test reads the developer guide). Manual review against `WORKER-CONTRACT.md:23`. | Same step as the line-23 edit, so the copy never disagrees. |
| R8 | `CHANGELOG.md` `## [Unreleased]` :5. **Format note:** `[Unreleased]` entries use a feature heading `### <title>` (e.g. :7) with `#### Added (<topic>)` sub-headings (:19, :33, ... :131); there is no bare `### Added` under `[Unreleased]`. The design's "one `### Added` entry" (`orchestrator-mode.md:701`) should follow the file's form: `### <sweep title>` + `#### Added (sweep)`. | None (only `tests/audit/test_full_docs_audit.py:60` uses a synthetic `CHANGELOG.md`). Manual review. | Last, any step. |

R1/R6 word rule: avoid stop, retry, release, merge, removal (`orchestrator-mode.md:707`). The R1 text at `orchestrator-mode.md:694` contains none and is ASCII.

## IP-5. HOW-WE-WORK copies: plugin byte copy and the CLAUDE.md level-table copy

- **No script or make target does either copy.** Grep of `Makefile`, `scripts/**`, `src/superclaude/cli/**/*.py`, `.pre-commit-config.yaml`, `.github/**` for `level-table|HOW-WE-WORK|sc-recommend/refs` found only `install_core.py:21` (ships the guide to `~/.claude/`) and `cli/recommend/cache.py:35,72,75` (hashes the guide as a cache key). The project CLAUDE.md rule (Key Documentation Files) is a manual step: `cp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, then hand-copy the `<!-- level-table:v1 -->`...`<!-- /level-table -->` block into `src/superclaude/core/CLAUDE.md`.
- Tests for each copy:
  - plugin byte copy: `tests/commands/test_routing_plugin_parity.py:29-38` (above).
  - level-table copy: `tests/core/test_claude_md_routing_block.py:28-32` `test_level_table_copy_matches_guide` asserts the text between the level-table markers in `core/CLAUDE.md` == the same block in the guide. Plus `tests/core/test_how_we_work_routing_table.py:172-183` pins the level table's shape (6 rows, header).
  - install copy: `tests/cli/test_how_we_work_install.py:31` asserts the installed `HOW-WE-WORK.md` bytes == src.
- R1 and R2 are outside the level-table block (level table ends before `<!-- other-commands:v1 -->`, asserted at `test_how_we_work_routing_table.py:294`), so **no CLAUDE.md re-copy is needed**; the plugin copy is needed.
- The recommend cache key changes when the guide bytes change (`cache.py:72`): cached `/sc:recommend` rows are invalidated at runtime. No test pins the real guide's hash (`tests/recommend/test_cache.py:146,152` use `tmp_path` guides).

## IP-6. `.gitignore` and `.dev/sweeps/`

- Current `.dev/` ignore entries: `.dev/eval-runs/` :239, `.dev/worktrees/` :242, `.dev/pr-monitor/` :250, `.dev/sprint-state/` :254, `.dev/e2e-reflect/**/sprint-state/` :257, `.dev/releases/**/results/phase-*-task-*-output.txt` :261; negations keeping task evidence `!.dev/tasks/**/logs/` :84, `!.dev/tasks/**/*.log` :85 (comment :83). No `sweeps` entry exists.
- Placement per design (`orchestrator-mode.md:712-717`): two lines (comment + `.dev/sweeps/`) after :254. Note :255-257 continue the sprint-state block, so the cleaner spot is after :257 (still "after the `.dev/sprint-state/` entry"); either is valid, the design names :254.
- Test: the NFR-002 `integration`-marked real-git test in `tests/sweep/test_readonly.py` copies the repo `.gitignore` into a `tmp_path` repo and asserts `git check-ignore .dev/sweeps/x.md` succeeds and `git check-ignore .dev/tasks/to-do/x.md` fails (`orchestrator-mode.md:720`, :737). **Ordering:** the `.gitignore` edit must land no later than the step that adds that test (step 1.4a per :737).
- `.dev/sweeps/` does not overlap `.dev/tasks/`; the `!.dev/tasks/**` negations (:84-85) are unaffected.

## IP-7. `make sync-dev` / `make verify-sync`

- `sync-dev` (`Makefile:109-163`) copies `src/superclaude/skills/*/` (dirs with `SKILL.md`, excluding `__init__.py`, `__pycache__`) -> `.claude/skills/<name>/` (:112-125); `agents/*.md` -> `.claude/agents/` (:126-130); `commands/*.md` (not README) -> `.claude/commands/sc/` (:131-136); `hooks/scripts/*.sh|*.js` -> `.claude/hooks/` (:137-143); `scripts/session-init.sh` (:144-147); `templates/**` (:148-157). **It does not copy `src/superclaude/core/`**, so `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` reach `~/.claude/` only via `superclaude install` (`install_core.py:14-29` lists both in `KNOWN_CORE_FILES`).
- `verify-sync` (`Makefile:166-353`) diffs the same five classes both ways and checks `_FRESHNESS_SCRIPTS` registration (:307-326) and the auggie hook matcher (:328-346); exits 1 on drift.
- For Phase 1: after creating `src/superclaude/commands/sweep.md` and `src/superclaude/skills/sc-sweep-protocol/`, run `make sync-dev` then `make verify-sync` (design step 1.25, `orchestrator-mode.md:708`). The `.claude/` copies are never staged (project CLAUDE.md rule). The brief guard reads the project `.claude/commands/sc/sweep.md` copy (`WORKER-CONTRACT.md:16`), so sync-dev must run before any Orca use in this checkout; guard case 3 refuses `/sc:sweep` by name alone (`WORKER-CONTRACT.md:16,20`), so the copy's content does not change that outcome.

## IP-8. Other test files checked and found unaffected

- `tests/unit/test_cli_install.py:53` `_PACKAGE_RESOURCES` is a baseline-wheel member list checked as presence only (`_assert_present` :502-505), so new files do not fail it.
- `tests/cli/test_issue_body_templates.py:78-97` is scoped to `issue*` names; not affected by `sweep`.
- `tests/commands/test_routing_plugin_parity.py:41-47` mirrors only `help`, `recommend`, `workflow`, `implement`; `sweep.md` needs no plugin mirror.
- `tests/core/test_claude_md_routing_block.py` checks only the level table and `core/CLAUDE.md` pointers; untouched by R1/R2.
- Unverified: whether other tests outside the files read here enumerate `src/superclaude/skills/*` by exact set (researcher 5's scope).

## Consolidated ordering constraints

1. `.gitignore` `.dev/sweeps/` lands no later than the real-git test step (1.4a).
2. R5 lands no later than the step that creates `src/superclaude/commands/sweep.md` (earlier is safe).
3. Creating `sweep.md` / `sc-sweep-protocol`: same step adds any `WRITE_VERB_CLASSIFICATION` entries (IP-3); `sweep.md` has no `## Unattended mode` heading (`test_worker_contract.py:470`).
4. R1 + R4 + R3 (and R2) in one commit, after `sweep.md` exists.
5. `WORKER-CONTRACT.md` line 23 + WC-14 + five pins (four from the design + the `RULE_PHRASES["never-as-worker"]` phrase at :89) + R7 in one step, after GQ-11 and the #422 check.
6. `make sync-dev` then `make verify-sync` after all `src/superclaude/{commands,skills}` edits; stage no `.claude/` path.
7. R6, R8: any time after `sweep.md` exists; manual review only.

## Summary

- WC-14 is the free next rule ID (highest is WC-13, `WORKER-CONTRACT.md:61`); it goes between `:156` and `:158`, and `/sc:sweep` joins the one-line list at `:23`. The design's four pins in `tests/skills/test_worker_contract.py` are right (RULE_PHRASES :25/:155, NEVER_AS_WORKER :245-254, the rename of :545 from "all_seven" to "every_listed", the sweep assertion after :865). **They are not enough:** `RULE_PHRASES["never-as-worker"]` at :86-92 pins the old list text word for word, so changing line 23 breaks `test_contract_states_rule[never-as-worker]` unless :89 is updated in the same commit.
- R1-R5 are covered by tests: R1+R4 by `test_other_commands_membership_and_live_references` (set equality, and `sweep.md` must exist); R3 by `test_routing_plugin_parity.py:38`; R5 by `test_routing_refresh.py:648`, which is triggered by the new `sweep.md` file, not by the guide. R2, R6, R7 and R8 have no test. R8 must follow the CHANGELOG's `### <title>` + `#### Added (...)` form. No script does the HOW-WE-WORK copies; both are manual, and the level-table copy into `core/CLAUDE.md` is not needed because R1 and R2 sit outside the level table.
- Two further integration points: the AC-0.9 write-verb audit (`test_worker_contract.py:1090-1166`, :2199) scans the new command and skill files for git/gh write verbs. `.dev/sweeps/` goes after `.gitignore:254`, no later than the real-git test step. `make sync-dev` does not copy `core/`; `WORKER-CONTRACT.md` and `HOW-WE-WORK.md` reach `~/.claude/` only through `superclaude install`.
