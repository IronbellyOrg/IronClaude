# Build task: `src/superclaude/cli/sweep/classify.py` (plan item 8.4, step 1.3)

You are the implementer for one task in a larger build. Work in the git worktree `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` (run every command from that directory). Use UV for all Python: `uv run ...`; never bare `python`, `pip` or `python -m`. Do not commit, push or stage anything. Create or edit exactly ONE file: `src/superclaude/cli/sweep/classify.py`. Do not edit `models.py`, add tests, or touch any other file. If `models.py` lacks something you need, say so in your final reply instead of editing it.

## What to build

The item text (verbatim):

> Create `src/superclaude/cli/sweep/classify.py` as pure functions over `models` types, one `Rule` per DESIGN rule, the joins and notes with their exact DESIGN strings, and `classify_all` returning `SweepResult` whose `rows` are `ClassifiedRow(row, classification, policy_of(row), safe_to_close(...))`. Fill the nine `SessionRow` dimension fields only from the sources research/09 Gap 2 lists (REPORT:1248) that the row already carries; a dimension with no Phase 1 source (`phase`, `approval`, `admission`, `tests_review`) keeps its default. No clock read: every time comes from `SweepContext.now`.

Signatures (DESIGN section 7.1): `Rule(name, match)`; `RULES` in the order `blocked_contract`, `orca_exit_proof`, `fenced`, `waiting_signal`, `working`, `finished`, `idle`, `person_active`, `fallback`; `classify`, `policy_of`, `package_state`, `mark_shared_packages`, `safe_to_close`, `removable`, `classify_all`. Read the exact signatures in DESIGN 7.1 and implement them as written.

Hard constraints (the verification will check them):
- Imports: only the standard library and `.models`. The file must NOT import `subprocess`, `click`, `os`, `shutil` or `time` (NFR-004, checked by `grep -nE '^(import|from) '`). No file or network access, no clock read: every time comes from `SweepContext.now` or from the data passed in.
- The rule names in `RULES` appear in exactly the order above.
- Every note string and reason string that DESIGN section 7.2 (and the R3 fixes quoted there) gives in backticks must appear BYTE-EXACT in the file (`grep -F`). Collect them by reading DESIGN 7.2 closely; examples: `Dispatch time window not observable`, `conflict: one pane session matches several Dispatch rows`, `pane moved to a later session`, `session started before this Dispatch window`, `session start not observable: transcript tail only`, `joined by pane: latest session of the pane`, `tab map join not observable`, `Orca pane session, not in scoped Runs`, `earlier pane session not joinable (tab map keeps only the latest session)`, `origin not proved: no tab-map entry; may be a worker of a Run outside the scope`, the five `origin unknown: ...` notes, `conflict: duplicate Dispatch rows disagree`, `conflict: inconsistent observation`, `WC-13 violation, review`, `blocked contract under ask the coordinator; may be re-running`, `blocked contract; Orca state not observed`, `Orca: exited; fenced evidence not readable`, `timestamp in the future`, `unscanned: transcript not readable`, `unscanned: contract not readable`, `partial: usable not yet judged`, `could not join Orca workers to transcripts (tab map empty or stale)`. Use the DESIGN spelling, not these examples, wherever they differ.
- `uv run ruff check src/superclaude/cli/sweep/classify.py` must exit 0 and `uv run ruff format --check` must pass.

## What to read first (in chunks of at most 150 lines)

1. `docs/designs/orchestrator-mode.md`: section 7.1 (from line 353; classify signatures, `policy_of` near line 413, `removable` near line 419), section 7.2 (lines 449-517: data model, time parsing, RULES table, the three rule readings, the joins path A and path B, D9, the list-incomplete cases, the four guard cases, the observation rules), section 7.4 (JSON schema, to know what `SweepResult` must carry), section 9 (Waiting (a) and (b)), section 2.2 (join paths), section 13 row D9 (line 836), section 17 open items 1, 22, 23.
2. SPEC `.dev/brainstorms/20261108-024258-orchestrator-mode-phase1/merged-requirements.md`: lines 222-300 (types, rules, package states, policy), FR-010, FR-013, FR-014, FR-015 and section 5.2 for the summary.
3. `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/discovery/1.0a-facts.md` (live facts: `session_join` is `result.dispatch.assigneeHandle`, compared by equality with `TabMapEntry.terminal_handle`; a tab-map `file_name` is the pane key with `:` written as `+`; time forms; what is UNVERIFIED keeps the DESIGN "behaviour until closed").
4. `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/research/09-gap-fill.md` (Gap 2: the ten #409 dimensions and the column sources in REPORT:1248) and `research/01*.md`, `research/04*.md` as needed (R3-B1 time window at research/04:87-90; R3-B2, R3-B3).
5. `src/superclaude/cli/sweep/models.py` (the types; frozen dataclasses with defaults; read it fully first) and `src/superclaude/cli/sweep/__init__.py`.

## How to work

- Write the module in sections and re-read it. Keep it pure and deterministic; the result must not depend on input order (DESIGN says "no row wins by position").
- Implement the joins exactly as DESIGN 7.2 describes (path A, path B with the time window, whole-second cut of `first_record_ts`, window both ends included, `collected_start` for open windows, `tail_complete` False handling, several-rows rule, D9 residual cases, the four guard cases, the five list-incomplete cases, the observation rules for duplicate Dispatch rows, WC-13, unreadable transcript or contract, future timestamps).
- Fill dimension fields only from row data that exists; `phase`, `approval`, `admission` and `tests_review` keep their defaults.
- After writing, run: `uv run ruff check src/superclaude/cli/sweep/classify.py`, `uv run ruff format --check src/superclaude/cli/sweep/classify.py`, `uv run python -c "import superclaude.cli.sweep.classify"`, and the import grep. Then run a small throwaway smoke script of your own (not saved in the repo; keep it under `/tmp`) that builds a few rows from `models` types and calls `classify_all`, to check that each of the nine rules can match and that the joins behave. Do NOT leave scripts or tests in the repository.
- Final reply: (1) the file path; (2) the output of the verification commands; (3) a list of every place where DESIGN was ambiguous or silent and what you chose; (4) any needed change to `models.py` that you did not make. Keep it short.
