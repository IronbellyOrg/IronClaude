# The Orca observer (`superclaude observe`)

Date: 2026-11-17. Source: origin/master, read with read-only git (local checkout is an old branch). Companion file: `/home/coder/workspaces/IronClaude/.dev/analysis/20261117-new-systems/observe-explain.md`.

## 1. What it is

The observer is a read-only terminal screen for people who run Orca (the multi-agent worktree tool). Every 15 seconds it asks Orca for its worker list and shows one row per worker: state, next action, how fresh the data is, and how many rows were collected versus reported. With `--run <id> --questions` it also lists the coordinator questions (Orca messages of type `question`) of one named Run. It never writes to Orca. Where the data is missing, old or contradictory it says so ("UNKNOWN", "STALE", "PARTIAL") instead of guessing. It can also print a plain-text record and write a versioned JSON snapshot.

**Entry points.** `superclaude observe` (click group in `src/superclaude/cli/observe/commands.py`, registered at `src/superclaude/cli/main.py:580-582`). Flags: `--once`, `--width 160|116|80`, `--ascii`, `--fixture <variant>`, `--run <id>`, `--snapshot <file>`, `--questions` (`commands.py:410-455`). No slash command or skill exists for it (a grep of `src/superclaude/{commands,skills,hooks}` for "observe" found only unrelated prose). Package files: `adapter.py` (the only Orca edge), `collector.py` (polling loop), `parse.py`, `questions.py`, `view.py`, `render.py`, `terminal.py`, `export.py`, `keys.py`, `sanitize.py`, `snapshot.schema.json`, 16 synthetic fixtures. Tests: `tests/observe/` (27 files).

**History (which parts are new).**

| PR | Merged | What |
|---|---|---|
| #503 | 2026-11-11 | Release 1: worker ledger, `--once`, snapshot (older than the window) |
| #514 | 2026-11-12 | Release 2: question panel and retention, live read switched off (older) |
| #577 | 2026-11-16 | NEW in window: flipped `QUESTION_GATE_PASSED` to True (`commands.py:67`), applied the 11 EXECUTE-NOW cuts (-208 lines net, 684 observe tests pass, per the PR body), archived the plan, recorded the owner's DIRECTION-SELECTED decision in `.dev/issues/409/owner-direction-record-20261116.md` |
| #586 | 2026-11-17 | NEW in window, docs only: live questions test and synthetic load test in `.dev/issues/409/bmad/spec-orca-observer/release-gates.md` |
| #587, #589 | 2026-11-17 | Alignment records only (context; not read in depth) |

The design material lives in `.dev/design/orca-observer-20261106/` on origin/master (last touched by #503). Commit 495eb96d1 "docs: publish Orca dashboard design collaboration package (#409)" (README, PLAN, PREVIEWS, QA, mockups) is NOT an ancestor of origin/master; it sits on branch `origin/docs/409-orca-dashboard-designs`, so that package is not merged. I did not read the mockups.

## 2. How it works

**Data flow.** One direction, no cycles:

`Orca CLI` -> `adapter.LiveSource` (argv check, subprocess, size and time caps) -> `collector.Collector` (one cycle, publishes a frozen `CycleResult`) -> `parse.parse_page / merge` and `parse.parse_questions + questions.merge_questions` -> `view.build_view` (pure) -> `render.render` (screen) or `export.record_text / snapshot_json` (files). `sanitize.sanitize` is applied to every untrusted string on the way in.

**Components.**

- Adapter (`adapter.py`). Three argv shapes only: worker-list, a discovery probe, and the question read (`adapter.py:29-32`). The question read is `orchestration check --all --types question --run <id> --json`, exactly 8 tokens (`:111-118`). A forbidden-prefix list (`check`, `--ack`, `--wait`, `--peek`, `send`, `reply`, `run-use`, ...) is checked at every verb and flag position (`:34-50`, `:135-170`); the allow-list only ever grows. Run ids must match a regex (marked PROPOSED, not an Orca format) and cursors are bounded to 2,048 bytes (`:52-55`, `:92-108`). The runner uses no shell, its own session, kills and reaps the whole process group on timeout, stops stdout at 8 MiB and keeps 2 KiB of stderr (`:196-312`). `cancel_active` kills in-flight calls on quit (`:216-221`).
- Binary discovery reuses `_find_orca` (`src/superclaude/cli/install_user_setup.py:247-270`), which proves a candidate is Orca by running `skills list --json` and looking for the `orca-cli` topic (this matters because a bare `orca` on Linux is often the GNOME screen reader).
- Collector (`collector.py`). Interval 15 s, cycle budget 15 s, backoff doubles to 60 s on failure (`:28-34`, `:304`). Paging is capped at 5 calls per cycle, or 4 plus one message call when questions are on (`adapter.py:57`, `collector.py:32-34`, `:271`). A failed first page keeps the previous snapshot (`:302-315`). The question read runs inside the same budget and a failure touches nothing else (`:203-243`, `:288-291`).
- Parse (`parse.py`). Strict envelope (`ShapeError` if `result.workers`, `result.page` or `hasMore` is wrong, `:365-407`), lenient rows reading only 30 known keys (`:58-90`). Missing values are the `UNKNOWN` sentinel (`:25-43`). `merge` dedupes inside a cycle, keeps rows not re-seen (`reobserved=False`) and computes `Coverage` (COMPLETE, PARTIAL or MISMATCH; `:179-218`, `:588-678`).
- Questions (`parse.py:415-541`, `questions.py`). Only rows of type `question` for the named Run are kept; body, payload and recipient are never kept. Identity is (Run, `message.id`). Retention is bounded at 1,000. A question that leaves Orca's 100-row window stays, marked "no longer in source window"; a read of exactly 100 rows sets "window full" (`questions.py:21-23`, `:81-142`). Nothing is ever marked closed because no closure source exists (`questions.py:1-12`).
- View (`view.py`). Pure function of (cycle result, session, clock). STALE is computed at 45 s on the monotonic clock, never stored (`:32-34`, `:352-359`). Keys change only the `Session` (selection, filter, historical toggle, mark, inspector scroll; `:114-127`). Fixture mode shows "SYNTHETIC FIXTURE <name>, not Orca data" (`:777-781`).
- Render and terminal. Three layouts (160, 116, 80 columns), `--ascii`, NO_COLOR, too-narrow and too-small messages (`terminal.py:21-27`).
- Export (`export.py`). Plain-text record and JSON snapshot (`schemaVersion` 1, `sort_keys`, every row regardless of filter, optional `questions` group with ids, times and counts but never subjects; `:148-214`). Written atomically with mode 0600 to `$XDG_STATE_HOME/superclaude/observe` or `~/.local/state/superclaude/observe` (`:226-264`).
- Keys (`keys.py`). POSIX cbreak reader, restores the terminal on exit and on SIGINT, SIGTERM, SIGHUP, SIGTSTP and SIGCONT (`keys.py:1-8`), imported lazily so `--once` works elsewhere (`commands.py:342`).

**The gate.** `--questions` is refused before any Orca call, discovery included, if `--run` is missing, `--fixture` is used, the run id is malformed, or `QUESTION_GATE_PASSED` is False (`commands.py:173-187`, `:375-378`). It is now True (`commands.py:67`), citing the owner's pass record `.dev/issues/409/owner-pass-record-20261112.md`. This is the live-read switch PR #577 turned on.

**Safety limits (summary).** No Orca write path; no `run-use`; 5 calls per cycle; 10 s per call (UNVERIFIED value, `adapter.py:60-62`); 8 MiB output; 15 s cycle; 1,000 retained questions; sanitizer strips every escape form and control/format character (`sanitize.py:15-48`).

**What PR #577 cut and why** (`.dev/issues/409/ponytail-review-20261116/cuts-debate/final-cut-list.md`). A "ponytail" review of the runtime found about 300 of roughly 4,280 lines with no verifiable return (`runtime-code.md`). A quick-depth three-variant adversarial debate scored 39 items: 15 CUT-SMALLER, 15 KEEP, 9 DEFER-OWNER; 11 passed the survival rule (CUT-SMALLER, confidence at least 70 percent, no open factual contradiction). Applied:

- R1+T9: code only tests called (an always-empty palette and its helpers, unused glyphs, `box_style`, the `CODES` set, `Fixture.parse`, closure-evidence helpers, `Deps.extra`, the fixture question replay in `collector.py`, replaced by a 2-line stub at `collector.py:125-129`).
- R3 and R2: the "unrecognised keys" counters and `QuestionsPanel.count_text`.
- S2: the schema load moved from `export.py` into the test conftest.
- T5, T7, T8, T9: duplicated test scans and a vacuous `or True` assertion fixed.
- D1, D2, D13: stale "not passed" wording and open-decision labels updated in documents and help text.

Explicitly kept: sanitizer, argv allow-list, process-group kill, terminal restore, snapshot redaction, the disclosure label, the three layouts, the inspector scroll (R4, an owner question because the written spec says "no per-panel scrolling"). Nine items (snapshot `questions` group, default snapshot writing, archiving review evidence, and so on) wait for the owner.

## 3. Where it could be integrated in future

The reusable idea is a pattern, not an Orca feature: a read-only observer behind an exact-template command allow-list, which publishes immutable cycle results and renders an honest "unknown" status. Types of system it suits:

1. **Other read-only status screens for CLI-driven tools** (sprint runs, issue watcher, cleanup audits). Same shape: bounded poll, merge, stale-by-clock, text record plus versioned JSON. Why: the adapter, sanitizer, collector and terminal-policy modules have no Orca knowledge beyond `adapter.py` and `parse.py`.
2. **A monitoring feed for the Orca coordinator or a supervising agent**, using the JSON snapshot as the input. Why: the snapshot is versioned, additive-only, redacted (no subjects or bodies) and has a JSON Schema (`snapshot.schema.json`).
3. **Safe-observation wrappers for any external CLI an agent may call** (a read-only edge with a grown-only forbidden list). Why: `assert_allowed` plus process-group kill plus output cap is a small, tested pattern.
4. **Future observer releases already named in the gates**: R3 question-to-session links, R4 remote fleet rows, closure evidence, message history, write-back (`release-gates.md` table). Each is blocked on a data source Orca does not yet give (for example a reply row linked to a question id).

## 4. Integration guide

**Best way in: consume the JSON snapshot, or import the layers you need; do not add Orca calls.**

Steps:
1. Decide the need. Only reading the output? Run `superclaude observe --once --snapshot <file>` and read the file (schema: `src/superclaude/cli/observe/snapshot.schema.json`; additive-only, `schemaVersion` 1, `export.py:20`). In a live session the loop writes `snapshot.json` once per cycle to the state directory (`commands.py:294-301`, `export.py:226-244`).
2. Need a new data source (a different Orca read)? Add a new fixed template in `adapter.py` next to `QUESTION_TEMPLATE`, extend `_is_question_shape`-style exact-shape checks, add a `read_<x>` method on `LiveSource` and the `CycleSource` protocol (`collector.py:71-89`), and a `FixtureSource` stub. Never loosen `assert_allowed`; the forbidden set only grows.
3. Parse with a strict envelope and lenient rows into frozen dataclasses with `UNKNOWN` for missing values (`parse.py`). Sanitize every string.
4. Keep the view pure: put every status word in `view.py`, take time only from the injected clock.
5. Registration: one import and `main.add_command` in `main.py` (`:580-582`).

Reuse: `sanitize.py`, `adapter.production_runner`/`cancel_active`, `terminal.py`, `export.write_atomic`, the injected `Clock` and `Deps` test seams (`commands.py:100-143`).

Pitfalls:
- The question read only works from the terminal that holds the Run; elsewhere it fails `consumer-fenced` (`adapter.py:66-69`). Do not work around it with `run-use`.
- `QUESTION_GATE_PASSED` is a hand-edited constant tied to an owner record. A new gated source needs the same record discipline.
- Every observer process polls independently, so N observers multiply Orca load (`commands.py:84-85`).
- A handled question stays listed; "seen" is not "resolved" (`questions.py:9-12`).
- The 10 s per-call timeout is UNVERIFIED (`adapter.py:60-62`).
- Windows: interactive mode is refused, only `--once` works (`commands.py:339-341`).

Tests to add: for any new argv, a forbidden-token and exact-shape test next to `tests/observe/test_adapter.py`; question-path error tests for output-cap, OSError and budget overrun (the cut list says only one question-path error test exists, R9); a golden contract test with success, missing, stale and contradictory samples (the data-gate rule in `release-gates.md`); `uv run pytest tests/observe -q` and `uv run ruff check src/superclaude/cli/observe tests/observe` after each change.

## 5. IronClaude fit

Overlap check done on origin/master. Orca is already called read-only from three other places, each with its own allow-list: `src/superclaude/cli/sweep/probes.py` (its own `ALLOWED_ORCA` and `check_orca_argv`, `subprocess.run`, :226-238, :266-290), `src/superclaude/cli/issue_watch/` (an `OrcaLauncher`, which writes), and `src/superclaude/cli/issue_pipeline/approval_record.py` and two hook scripts that mention worker-list or orchestration verbs (not read in depth). The sprint TUI (`src/superclaude/cli/sprint/tui.py`) also uses `rich.live.Live`.

Ranked proposals:

1. **Share the Orca process runner between `sweep` and `observe`.**
   - Target: `src/superclaude/cli/sweep/probes.py` `_orca` (:266-300) and `observe/adapter.py` `production_runner` (:224-312).
   - Change: sweep adopts the observer's Popen runner (process-group kill, 8 MiB stop while streaming, stderr cap). Keep each tool's own allow-list.
   - Value: it closes a limit sweep states itself: its `subprocess.run` checks the 8 MiB limit only after the child exits, with a "shortcut ... upgrade to Popen only if a call is seen to exceed" comment (:270-272). The runner exists, is tested and has `cancel_active`.
   - Effort: small to medium (about a day, needs sweep tests re-run). Risk: low to medium; sweep has an owner ruling D-01 (2026-11-12) choosing the simpler form, so ask the owner first.

2. **Have `sweep` or the coordinator read the observer's JSON snapshot instead of re-polling `worker-list`.**
   - Target: `src/superclaude/cli/sweep/classify.py` and `probes.py` (they already read `worker-list`).
   - Change: optional input from the snapshot file with its `source.status` and `observedAt` used to refuse stale data.
   - Value: one fewer Orca poller (the observer help warns that several observers multiply load). Effort: medium. Risk: medium. The snapshot is written only in live interactive mode or with `--snapshot`, so a reader must handle a missing or stale file; the schema is also not guaranteed to carry fields sweep needs (UNVERIFIED, I did not diff the field sets).

3. **Point the sprint TUI and any future live screens at the observer's terminal policy.**
   - Target: `src/superclaude/cli/sprint/tui.py` and `observe/terminal.py` (`resolve_policy`, `clip`, ASCII and NO_COLOR handling).
   - Change: reuse width classes and display-cell truncation.
   - Value: consistent NO_COLOR and ASCII behaviour. Effort: medium. Risk: medium, because `terminal.py` says no other module may build a `Console` (docstring, `terminal.py:1-6` region) and the sprint TUI predates it. Low priority.

4. **Add a short `/sc:` command or help entry that documents `superclaude observe`.**
   - Target: `src/superclaude/commands/` (none today). Value: discoverability; the live test guide (`.dev/issues/409/live-test-guide.md`) says it must be run from a real terminal, not inside Claude Code, so a slash command cannot run it. A docs-only entry is the honest form. Effort: small. Risk: low.

No good fit exists for the retention store (`questions.py`), the question parser or the snapshot schema outside the observer: they encode Orca message semantics and an owner-decided "coordinator questions only" meaning, so reuse elsewhere would be forced.

## 6. Limits, open questions, UNVERIFIED items

**Verified live evidence (from `release-gates.md`, as recorded by PR #586; I read the document, not the runs).** Live test 2026-11-17 on a new throwaway Run: two hand-sent questions were listed as "seen, not resolved: 2", were still listed by `check --peek` afterwards (not consumed), terminal restored after Ctrl-C. Synthetic steady load: 181 sent, 181 retained, 0 lost; 81 had scrolled out of the 100-row window and stayed listed. Burst test: 30 of about 415 lost, 4 of them among 130 burst messages, 26 unattributed (the script logged no message ids); the panel read "385+ (window full)".

**Limits.**
- Bursts over 100 rows between reads can be lost; label is "bounded best effort; coverage unknown" (`commands.py:87-93`).
- Question read works only from the terminal that holds the Run (Q-1 FAIL, accepted by the owner 2026-11-12). Non-consumption was shown as the Run owner only.
- No read marker: answered questions look open. No closure source, no history older than 100 rows.
- Question ids and field names were seen on probe Runs only; real traffic rate and identity are unmeasured.
- Live mode only; interactive needs POSIX and a terminal.
- Output numbers such as 684 passing tests come from the PR body; I did not run the tests.

**Open owner questions after the cuts** (Q1-Q11 in `final-cut-list.md`): keep the `questions` group in the snapshot (S1); default snapshot write in live mode (S5); archive review evidence and PRD scaffolding (D3-D9); who writes DIRECTION-SELECTED acceptance (D12; the record of 2026-11-16 now exists, but I did not check whether it settled Q9); inspector scroll versus the spec's "no per-panel scrolling" (R4/Q11).

**UNVERIFIED.**
- Whether the design package commit 495eb96d1 will merge; its content not read.
- The 10 s per-call timeout (`adapter.py:60-62` says so itself).
- The run-id regex and cursor bound are PROPOSED, not Orca formats (`adapter.py:52-55`).
- Whether `view.py` and `render.py` behave as documented in every width: I read the structure and key literals, not every branch (`view.py` is 1,038 lines; I read about 150 of them in detail).
- Exact file:line of the cut items after PR #577: the cut list's line numbers describe the pre-cut tree.
- Whether PRs #587 and #589 change observer behaviour (treated as records only).
- Real-traffic behaviour of `check --all --types question` for any Run other than the probes and the 2026-11-17 throwaway.

---
Footer: graph:stale (codegraph index does not cover origin/master; not used). All file:line cites were read from origin/master on 2026-11-17.
