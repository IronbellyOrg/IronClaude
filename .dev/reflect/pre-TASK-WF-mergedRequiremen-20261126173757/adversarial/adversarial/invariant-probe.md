# Invariant Probe Results (Round 2.5, fault-finder: sonnet, read-only)

Raw fault-finder output below, verbatim. Summary: 16 entries (INV-001 to INV-016): 3 HIGH UNADDRESSED (INV-001, INV-002, INV-006), 6 MEDIUM UNADDRESSED, 6 LOW UNADDRESSED, 1 LOW ADDRESSED (INV-015). The fault-finder's own summary line miscounts; this count is from the entries.

Nine of the 15 entries below are UNADDRESSED at MEDIUM or higher; I read the repo source and tests, not only the cards. The consensus classifications look right, but the agreed repairs alone do not leave the plan executable. Two existing test files would fail as the plan is written (INV-001 and INV-002).

**Category 6, sufficiency challenge (read first)**

- **INV-001; SUFFICIENCY CHALLENGE**
  - ASSUMPTION: Task 6 can change the missing-ledger message and "the exit-2 cases of `tests/sweep/test_cli_contract.py` still pass".
  - STATUS: UNADDRESSED; SEVERITY: HIGH.
  - EVIDENCE: Plan `:82` appends ` run "superclaude sweep ledger" first` to the BindingError text. Plan `:86` says the exit-2 cases still pass.
    - `tests/sweep/test_cli_contract.py:190-192` (`_failed`) asserts the exit code, stdout and stderr byte for byte.
    - `:375-389` expects exactly `Orca unavailable (binary not found: orca-ide); no Run binding could be established: pass --run <id>\n`.
    - `:478-490` expects exactly `no Run bound: pass --run <id>\n`.
    - The autouse fixture the plan adds in `tests/sweep/conftest.py` (`:82`) points the ledger at a missing file, so both tests hit the new message and fail.
    - Plan `:86` is therefore unsatisfiable as written. Neither card nor any agreed repair mentions it. Spec `:83` asks for the same wording, so the spec and the existing tests conflict.

- **INV-002; SUFFICIENCY CHALLENGE**
  - ASSUMPTION: Adding `run-ledger-record.sh` to `_FRESHNESS_SCRIPTS` leaves `tests/cli/test_install_hooks.py` passing (plan `:115`).
  - STATUS: UNADDRESSED; SEVERITY: HIGH.
  - EVIDENCE: `src/superclaude/cli/install_hooks.py:267-280` loops over `_FRESHNESS_SCRIPTS` and records `failed` for any script whose source file is missing. `:245` sets `overall = success_settings and not failed`.
    - The fixture at `tests/cli/test_install_hooks.py:89-108` seeds a hard-coded list of 17 script names that does not include the new one.
    - Existing tests do `ok, msg = install_hooks(...); assert ok, msg` (`:154-155`, `:175-176`, `:210-211`, `:252-253`).
    - So many existing tests fail unless Task 9 also edits that seed list. Plan `:112` mentions only a new test and a `hooks.json` assertion.

**Category 1, state variables**

- **INV-003; STATE VARIABLES**
  - ASSUMPTION: Task 11 can run `sweep run` "from a terminal with no Run bound" after Task 8 ran `run-create`.
  - STATUS: UNADDRESSED; SEVERITY: MEDIUM.
  - EVIDENCE: Plan `:102` only asks to "note whether this terminal is now bound". Plan `:136` has no way to unbind. Plan `:22` forbids `orchestration reset`.
    - `commands.py:264-266` and the plan's Task 6 order try `bind_run` first. If the scratch Run is bound, the ledger path is never exercised.
    - The Task 11 claim "ran without `no Run bound`" would then pass without testing the ledger.
    - The C-002 repair (an owner go) does not touch this side effect.
    - The repair should run the Task 11 sweep from a different terminal or checkout, or assert which path was taken from the `run_source` header line.

- **INV-004; STATE VARIABLES**
  - ASSUMPTION: `./artifacts/` and `./source.md` resolve to the package folder, and the C-006 repair (stage `.dev/tasks`) can be placed anywhere.
  - STATUS: UNADDRESSED; SEVERITY: LOW.
  - EVIDENCE: Plan `:102`, `:136` and `:140` write `./artifacts/hook-decision.md`, `pytest.log` and `ledger.json`. Tasks 8 to 11 write fixtures repo-relative.
    - The user's CLAUDE.md says the package-level `artifacts/` is staged and the project-root `artifacts/` never is. An executor whose cwd is the repo root would write to the wrong one.
    - The staging step must also run after Task 11, the last writer. A step placed earlier would leave the later artifacts unstaged.
    - Staging does not conflict with "no file was committed" at `:140`.

- **INV-005; STATE VARIABLES**
  - ASSUMPTION: Widening Task 6 to any `BindingError`, including "Orca unavailable", is within the spec.
  - STATUS: UNADDRESSED; SEVERITY: LOW.
  - EVIDENCE: Spec `:81` says "no Run is bound". Plan `:82` reads the ledger on every `BindingError`.
    - `probes.py:404` raises `BindingError` with Orca down.
    - `_call` (`:374-393`) treats only the first Orca call's failure as "unavailable". `bind_run` has already used that first call, so the later `collect` failures are classified differently from the old exit-2 behaviour.
    - The plan makes no decision here.

**Category 2, guard conditions**

- **INV-006; GUARD CONDITIONS**
  - ASSUMPTION: The rules `new`, `NEW_FALLBACK_HOURS`, the hook `added_at >= generated_at` and Task age can compare timestamps as plain values.
  - STATUS: UNADDRESSED; SEVERITY: HIGH.
  - EVIDENCE: Plan `:30` and `:40` never say how to parse timestamps. `probes.py:413-437` (`parse_time`) shows Orca emits two forms: SQLite `YYYY-MM-DD HH:MM:SS` and ISO with `Z` or an offset.
    - A string compare of a SQLite-form `created_at` against the ledger's `…T…Z` `generated_at` is wrong, because ' ' sorts before 'T'. A `.123Z` value also sorts before `Z`.
    - The Run-detection tests use plain dicts with a format the author picks, so they pass. Task 11 would likely show `new=0` and hide it.
    - The C-001 repair forbids importing `probes`, so the executor has no sanctioned `parse_time`.

- **INV-007; GUARD CONDITIONS**
  - ASSUMPTION: `make lint` and the repo style pass after Task 4's placement.
  - STATUS: UNADDRESSED; SEVERITY: LOW.
  - EVIDENCE: Plan `:60` puts an import "directly after the `sweep_group` definition (:215)", a mid-module import. `pyproject.toml:185` selects `"E"` and the ignore list (`:186-194`) omits E402. No task runs lint.

- **INV-008; GUARD CONDITIONS**
  - ASSUMPTION: Task 7's retained pinned phrase stays true.
  - STATUS: UNADDRESSED; SEVERITY: LOW.
  - EVIDENCE: `tests/commands/test_sweep_command.py:497` pins "adds no flag, reads no environment variable and has no worker mode". Plan `:82` makes `sweep run` read `SUPERCLAUDE_RUN_LEDGER`. The test passes but the skill text becomes inaccurate.

- **INV-009; GUARD CONDITIONS**
  - ASSUMPTION: Guard 3 needs no override.
  - STATUS: UNADDRESSED; SEVERITY: LOW.
  - EVIDENCE: Plan `:40` and spec `:66-67` allow `accept_empty` only for guard 4.
    - After an Orca reset or a fresh Orca database, `run-list` returns 0 while the old ledger exists. Every build then fails `implausible:` until someone deletes the file by hand.
    - This is spec-faithful but undocumented in Task 10.

**Category 3, count divergence**

- **INV-010; COUNT DIVERGENCE**
  - ASSUMPTION: The agreed F2 fix, "dedupe by id and leave `counts` as built", is sufficient.
  - STATUS: UNADDRESSED; SEVERITY: MEDIUM.
  - EVIDENCE: Spec `:34-36` defines `counts.hook_added` as a ledger field. Plan `:50` merges hook entries after the build, and plan `:60` writes them without recomputing counts.
    - If the Task 1 `hook_entries` path is removed as dead (conceded F1), the built `counts.hook_added` is always 0, while `runs` contains `hook_added` entries.
    - The repair also does not say which entry wins on a duplicate id. The hook entry would drop `live_worktree_ids` and `unfinished_task_count`.
    - Counts should be recomputed after the merge, and the winner and the reason union should be named.

- **INV-011; COUNT DIVERGENCE**
  - ASSUMPTION: Plan `:23` says the only real Orca calls are one `run-create` and Task 11.
  - STATUS: UNADDRESSED; SEVERITY: LOW.
  - EVIDENCE: Plan `:30` requires a real `orca orchestration task-list --run <id> --json` call in Task 1, which also needs a `run-list` call for an id. Plan `:102` runs `run-current` twice. A literal checker flags at least 3 more real calls.
    - The C-007 repair (use the Task field) keeps this contradiction unless it removes the "verified against one real call" clause or amends `:23`.

- **INV-012; COUNT DIVERGENCE**
  - ASSUMPTION: Fixing C-004 by defining the `Decision:` line for the UNVERIFIED case is enough.
  - STATUS: UNADDRESSED; SEVERITY: MEDIUM.
  - EVIDENCE: Plan `:102` requires the file to state "exactly one scratch Run was created". Plan `:106` requires `run_create_stdout.json` to exist and "no other Run was created". In the UNVERIFIED case zero Runs are created and nothing is captured.
    - Spec `:151` says that on "no" the hook is built from the documented shape, so the decision is deliver, not drop. Plan `:105` allows only `deliver` or `drop`.
    - The repair must also define the scratch-Run count (zero), the fixture source, and an `UNVERIFIED` marker kept separate from the `Decision:` line.

**Category 4, collection boundaries**

- **INV-013; COLLECTION BOUNDARIES**
  - ASSUMPTION: C-009 (empty `runs`) is an edge case that can be graded Medium with no stated direction.
  - STATUS: UNADDRESSED (direction); SEVERITY: MEDIUM.
  - EVIDENCE: An empty `runs` list is a normal state. It is the product of `--accept-empty` (guard 4) and of any first build on a quiet host, since guard 4 needs `previous.runs >= 1`.
    - If the repair treats an empty ledger as unusable (exit 2 "run sweep ledger first"), a valid fresh ledger sends the user round in a circle.
    - Downstream already copes: `report.py:194` renders `or 'none'`, and `Budget.share_shows` (`probes.py:155`) returns early on empty `runs`.
    - The repair should be: sweep proceeds with an empty Scope and the header line, exit 0. Task 6 needs a named test.

- **INV-014; COLLECTION BOUNDARIES**
  - ASSUMPTION: Task 6 "validate every id with `probes.RUN_ID_RE`" is enough.
  - STATUS: UNADDRESSED; SEVERITY: MEDIUM.
  - EVIDENCE: `probes.py:46` is an unanchored pattern, used with `re.fullmatch` at `commands.py:90`. Plan `:50` and `:82` do not say `fullmatch`; `re.match` would accept trailing junk.
    - `_check_run_ids` (`commands.py:87-92`) collapses duplicates. A hand-rolled loop in Task 6 skips that. A duplicate hook/build id (the C-003 defect) would then put the same Run into `ctx.runs` twice.
    - The repair should be to reuse `_check_run_ids`, or to say `fullmatch` and dedupe in `read_ledger`.

- **INV-015; COLLECTION BOUNDARIES (checked, addressed)**
  - ASSUMPTION: C-008, `main_checkout_only` for a Run with no matched worktree.
  - STATUS: ADDRESSED; SEVERITY: LOW.
  - EVIDENCE: Both advocates fixed the empty-set case: "admitted only through a main-checkout worktree, with the empty case excluded".
    - Wording check for the repair: it must also require that the Run's only reason is `live_worktree`, per spec `:59` and plan `:60`. Plan `:30` omits "only".
    - Single-element boundary checked: a one-Run ledger passes through the `runs` tuple at `models.py:80` unchanged.

**Category 5, interaction effects**

- **INV-016; INTERACTION EFFECTS**
  - ASSUMPTION: The C-001 repair is a one-name exception (`RUN_ID_RE`), or a copied regex, and nothing else in `ledger.py` needs `probes`.
  - STATUS: UNADDRESSED; SEVERITY: MEDIUM.
  - EVIDENCE: INV-006 needs `parse_time`, which lives in `probes.py`. Task 2's check (`:44`) is a blanket "not imported". Task 3 (`:50`) imports exactly one name.
    - If the repair is an exact-name allowlist, the time parser must be duplicated or moved.
    - Copying the regex also splits it into three copies: `probes.py`, `ledger.py` and the hook's shell pattern at `:112`.
    - The repair should state the permitted names and a test that checks them, such as an AST check of the `from .probes import` names.

**Category 6, other items checked**

- The consensus grades were re-verified. `:128` against `:124` is unsatisfiable (C-005). A grep of the plan for "stage" finds only `:20` and `:96` (C-006). Task 1 `:30` sets `main_checkout_only` as vacuous and the `decide(..., hook_entries)` branch is dead (C-001, C-003).
- Citation checks passed for Round 2: `:30`, `:33`, `:60`, `:102`, `:128`, `:136` and spec `:59`, `:133`.
- `src/superclaude/commands/sweep.md` exists, so the plan's path is right and the spec's `commands/sc/sweep.md` is wrong.

**Summary:** 16 findings: 2 HIGH (INV-001, INV-002) plus 1 more HIGH (INV-006), 6 MEDIUM (INV-003, INV-010, INV-012, INV-013, INV-014, INV-016), 7 LOW, of which 1 ADDRESSED (INV-015) and 15 UNADDRESSED.

Files read:
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/diff-analysis.md
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/round2-advocate-v1.md
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/adversarial/round2-advocate-v2.md
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/source.md
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/src/superclaude/cli/sweep/commands.py
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/src/superclaude/cli/sweep/probes.py
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/src/superclaude/cli/install_hooks.py
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/tests/sweep/test_cli_contract.py
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/tests/cli/test_install_hooks.py
- /home/coder/workspaces/worktrees/IronClaude/run-ledger/pyproject.toml

I did not re-read the two round-1 advocate files; I relied on the Round 2 files and the diff analysis for their content.
