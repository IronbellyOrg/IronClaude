# v3.7-task-unified-v2 — Correctness Test Scenario

Follow these sections in order. Every test item shows **what to do**,
**what to expect**, and the **code under test** (file:line / symbol)
so you can trace any failure back to the implementation.

All paths are relative to the repo root. All commands assume the UV
toolchain (`uv run`, `uv pip`) per `CLAUDE.md`. When a section says
"terminal A" / "terminal B", open two shells; otherwise a single shell
is sufficient.

---

## 0. Prerequisites

Run these once to confirm your environment is clean.

### 0.1 Install in editable mode

    make dev

- **Expected:** `Successfully installed superclaude-<version>`.
- **Code under test:** `pyproject.toml`, `src/superclaude/cli/main.py`.

### 0.2 Verify the full unit-test baseline matches the release

    uv run pytest tests/sprint/ --no-header -q 2>&1 | tail -3

- **Expected:** `921 passed, 57 failed`. The 57 failures are
  pre-existing mock-`Popen`-stdin issues and are **orthogonal to this
  release** — they must not grow.
- **Code under test:** every module under `src/superclaude/cli/sprint/`.

### 0.3 Confirm `/sc:task-unified` no longer appears in live source

    grep -rln 'sc:task-unified\|sc-task-unified\|/sc:task-unified' \
        src/superclaude/ .claude/ 2>/dev/null | grep -v __pycache__

- **Expected:** empty output.
- **Code under test:** Naming Consolidation (commit `de04670`),
  §4.3 tasks N1–N11 of the merged spec.

---

## 1. Naming Consolidation (Spec §3.3, §4.3 — commit `de04670`)

### 1.1 `/sc:task` command resolves; legacy is gone

    ls src/superclaude/commands/task*.md
    head -5 src/superclaude/commands/task.md
    ls -d src/superclaude/skills/sc-task-protocol src/superclaude/skills/sc-task-unified-protocol 2>/dev/null

- **Expected:**
  - Only `task.md` and `task-mcp.md` appear — **no** `task-unified.md`.
  - `task.md` frontmatter shows `name: task` (not `task-legacy`).
  - `sc-task-protocol/` exists; `sc-task-unified-protocol/` does not.
- **Code under test:** Naming N1–N4.

### 1.2 Sprint CLI emits the canonical prompt

    uv run python -c "
    from pathlib import Path
    from superclaude.cli.sprint.models import Phase, SprintConfig
    from superclaude.cli.sprint.process import ClaudeProcess

    phase = Phase(number=1, file=Path('/tmp/phase-1-tasklist.md'), name='Foundation')
    cfg = SprintConfig(index_path=Path('/tmp/idx.md'), release_dir=Path('/tmp'), phases=[phase])
    proc = ClaudeProcess(cfg, phase)
    prompt = proc.build_prompt()
    print('FIRST_LINE:', prompt.splitlines()[0])
    assert prompt.startswith('/sc:task '), 'prompt must start with /sc:task '
    assert '/sc:task-unified' not in prompt, 'old name still present'
    print('PASS')
    "

- **Expected:** first line `FIRST_LINE: /sc:task Execute all tasks ...`,
  ending with `PASS`.
- **Code under test:** `src/superclaude/cli/sprint/process.py`
  `ClaudeProcess.build_prompt` (docstring + line 170).

### 1.3 `cleanup_audit` prompt builders use the new name

    grep -c '/sc:task ' src/superclaude/cli/cleanup_audit/prompts.py
    grep -c '/sc:task-unified' src/superclaude/cli/cleanup_audit/prompts.py

- **Expected:** first count `5`, second count `0`.
- **Code under test:**
  `src/superclaude/cli/cleanup_audit/prompts.py` — all 5 prompt builders.

---

## 2. Build the fixture via the skill pipeline (spec → roadmap → tasklist)

The fixture for Sections 3–6 is **generated**, not hand-crafted. This
is the realistic end-to-end shape and it exercises:

- `/sc:roadmap` — spec-to-roadmap pipeline.
- `/sc:tasklist` — roadmap-to-tasklist bundle (including the Wave 4
  checkpoint normalisation rules in `sc-tasklist-protocol/SKILL.md`).
- `superclaude tasklist validate` — post-generation validator.
- The generated `tasklist-index.md` + `phase-*-tasklist.md` become the
  input for `superclaude sprint run` in Section 4.

> **Environment:** `/sc:tasklist` and `/sc:roadmap` are Claude Code
> skill commands — you run them inside a Claude Code session, not in a
> plain shell. The pre/post-generation commands (`superclaude roadmap
> run`, `superclaude tasklist validate`) are plain-shell CLIs.

### 2.1 Author a minimal spec

Pick a workspace for the run:

    export TEST_RELEASE=/tmp/v37-correctness-run
    rm -rf "$TEST_RELEASE"
    mkdir -p "$TEST_RELEASE"

Write the minimal spec (a 3-feature product brief is enough for the
generator to produce multiple phases):

    cat > "$TEST_RELEASE/spec.md" <<'EOF'
    # Minimal Widget Service — Specification

    ## Overview
    Small internal service that stores, retrieves, and summarises
    "widgets". Used only as a test fixture for the v3.7 release
    correctness run.

    ## Goals
    - G1: Provide a persistent model for a Widget record.
    - G2: Provide HTTP endpoints for create / read / list.
    - G3: Provide a short narrative summary of the current widget
      inventory.

    ## Functional Requirements
    - FR-1: `Widget` has `id: str`, `name: str`, `created_at: datetime`.
    - FR-2: `POST /widgets` creates a widget.
    - FR-3: `GET /widgets/{id}` returns a widget by id.
    - FR-4: `GET /widgets` lists all widgets.
    - FR-5: `GET /widgets/summary` returns a one-paragraph narrative
      of the inventory.

    ## Non-Functional Requirements
    - NFR-1: All endpoints have contract tests.
    - NFR-2: Persistence layer is a single JSON file at `data/widgets.json`.

    ## Out of scope
    - Authentication, multi-tenancy, UI.
    EOF

- **Code under test:** this is input only — the goal is to feed the
  skill pipeline with something stable and minimal.

### 2.2 Generate the roadmap from the spec

    superclaude roadmap run "$TEST_RELEASE/spec.md" \
        --output "$TEST_RELEASE/roadmap-out"

- **Expected:** `roadmap-out/` contains a roadmap markdown plus
  validation artifacts (fingerprint, convergence, coverage matrix).
- **Code under test:**
  `src/superclaude/cli/roadmap/commands.py::run` +
  `src/superclaude/cli/roadmap/executor.py`.
- **Skip path:** if you want a faster run, skip to §2.3 and hand-author
  a 3-phase roadmap directly — the tasklist generator only needs a
  roadmap on disk; it does not care how the roadmap was produced.

### 2.3 Generate the tasklist using the `/sc:tasklist` skill

Inside your Claude Code session (not in a plain shell), invoke:

    /sc:tasklist @$TEST_RELEASE/roadmap-out/roadmap.md \
        --spec @$TEST_RELEASE/spec.md \
        --output $TEST_RELEASE/tasklists

- **Expected:**
  - `$TEST_RELEASE/tasklists/tasklist-index.md` exists.
  - One `phase-N-tasklist.md` per phase the roadmap defines.
  - Each `phase-N-tasklist.md` ends with a checkpoint task heading of
    the form `### T<NN>.<MM> -- Checkpoint: End of Phase <NN>` and
    includes a `**Checkpoint Report Path:** checkpoints/CP-P<NN>-END.md`
    line inside the checkpoint body.
- **Code under test:**
  - `src/superclaude/commands/tasklist.md` (the command shell).
  - `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` — full
    generation algorithm + Wave 4 checkpoint normalisation rules
    (§4.1 Phase 4 T04.01–T04.03 of the merged spec).
  - Post-generation validator auto-runs: see §2.5.

### 2.4 Inspect the generated checkpoint structure (Wave 4 proof)

The interesting Wave-4 property is that every checkpoint appears as a
**numbered task**, not as a free-standing `### Checkpoint:` heading
outside the task scanner. Confirm that:

    for f in "$TEST_RELEASE/tasklists"/phase-*-tasklist.md; do
      echo "=== $(basename "$f") ==="
      grep -nE '^### T[0-9]{2}\.[0-9]{2}.*Checkpoint' "$f"
    done

- **Expected:** each phase file prints at least one checkpoint task
  heading (usually the last task of the phase). The end-of-phase
  checkpoint's task id follows the phase's regular numbering — no gap,
  no collision.
- **Also check** the deliverable registry entries:

      grep -nE 'D-CP[0-9]{2}' "$TEST_RELEASE/tasklists"/phase-*-tasklist.md | head -10

- **Expected:** checkpoint deliverables use the `D-CP<PP>[-MID]`
  format documented in Wave 4.
- **Code under test:** `sc-tasklist-protocol/SKILL.md`:
  - Checkpoint generation rules (T04.01).
  - Sprint Compatibility Self-Check — the new rules added in T04.02.
  - Deliverable registry guidance for `D-CP<PP>` ids (T04.03).

### 2.5 Validate the tasklist against the roadmap

    superclaude tasklist validate "$TEST_RELEASE/tasklists" \
        --roadmap-file "$TEST_RELEASE/roadmap-out/roadmap.md"

- **Expected:** exit code 0; report shows zero fabricated traceability
  ids and zero missing deliverables.
- **Code under test:**
  `src/superclaude/cli/tasklist/commands.py::validate` +
  `src/superclaude/cli/tasklist/executor.py`.

### 2.6 Sanity-check `count_tasks_in_file` and `load_sprint_config` on the generated bundle

    export TEST_TASKLIST="$TEST_RELEASE/tasklists"
    uv run python -c "
    import os, sys
    from pathlib import Path
    from superclaude.cli.sprint.config import count_tasks_in_file, load_sprint_config

    tl = Path(os.environ['TEST_TASKLIST'])
    index = tl / 'tasklist-index.md'
    phase_files = sorted(tl.glob('phase-*-tasklist.md'))
    assert phase_files, 'no phase files found — did /sc:tasklist succeed?'

    per_phase = {p.name: count_tasks_in_file(p) for p in phase_files}
    print('per-phase task counts:', per_phase)

    cfg = load_sprint_config(index)
    assert cfg.total_tasks == sum(per_phase.values()), \
        f'SprintConfig.total_tasks={cfg.total_tasks} != sum(per_phase)={sum(per_phase.values())}'
    assert cfg.phases and cfg.phases[0].prompt_preview, \
        'Phase.prompt_preview was not populated by load_sprint_config'
    print('PASS — total_tasks =', cfg.total_tasks,
          '| phase[0].prompt_preview =', cfg.phases[0].prompt_preview[:60])
    "

- **Expected:** `PASS — total_tasks = <N> | phase[0].prompt_preview = ...`,
  where `<N>` equals the sum of the per-phase task counts (each
  counts its own `### T<PP>.<NN>` headings, **including** the
  Wave-4-style checkpoint tasks).
- **Code under test:**
  - `src/superclaude/cli/sprint/config.py`: `count_tasks_in_file`,
    `_extract_phase_prompt_preview`, `load_sprint_config` (active-phase
    pre-scan).
  - `src/superclaude/cli/sprint/models.py`: `SprintConfig.total_tasks`,
    `Phase.prompt_preview`.

### 2.7 Export the sprint entry-point path

Subsequent sections use `$TEST_INDEX` as the sprint entry-point:

    export TEST_INDEX="$TEST_RELEASE/tasklists/tasklist-index.md"
    ls -1 "$TEST_INDEX"

---

## 3. Checkpoint Enforcement — W1 (Prompt)  — commits `183f8f8` + `de04670` (N5)

### 3.1 Prompt contains the `## Checkpoints` section

The prompt built for any phase generated by `/sc:tasklist` must carry
both the W1 checkpoint instructions and the post-Naming `/sc:task`
command name. Use whichever phase file `$TEST_INDEX` references — the
snippet below picks the first one automatically:

    uv run python -c "
    import os
    from superclaude.cli.sprint.config import load_sprint_config
    from superclaude.cli.sprint.process import ClaudeProcess

    cfg = load_sprint_config(os.environ['TEST_INDEX'])
    phase = cfg.phases[0]
    prompt = ClaudeProcess(cfg, phase).build_prompt()
    assert prompt.startswith('/sc:task '), 'prompt must start with /sc:task '
    assert '/sc:task-unified' not in prompt
    assert '## Checkpoints' in prompt
    assert 'Checkpoint Report Path:' in prompt
    scope = prompt.lower().split('## scope boundary', 1)
    assert len(scope) == 2 and 'checkpoint' in scope[1][:400], \
        'Scope Boundary must mention checkpoints'
    print('PASS')
    " 2>&1 | tail -5

- **Expected:** `PASS`.
- **Code under test:**
  `src/superclaude/cli/sprint/process.py` — `ClaudeProcess.build_prompt`
  (the `## Checkpoints` block from W1 plus the `/sc:task` rename from
  Naming N5).

---

## 4. Execute the sprint (drives TUI v2 + Wave 2 gate + Wave 3 manifest)

### 4.1 Run with `--no-tmux` so you can see the TUI directly

    superclaude sprint run "$TEST_INDEX" --no-tmux --dry-run

> The `--dry-run` flag short-circuits the actual subprocess; if your
> build does not support it, skip to Section 4.2 and point the
> `claude` binary at a stub.

- **Expected during run:**
  1. Outer panel title reads
     `SUPERCLAUDE SPRINT RUNNER == v37-correctness-run` (or whatever
     `release_dir.name` resolves to; `load_sprint_config` derives this
     automatically from the parent of the `tasklists/` directory).
  2. Phase table columns are `#  Phase  Status  Duration  Turns  Output`
     (no `Tasks` column; `Gate` column absent unless `grace_period>0`).
  3. Dual progress bar prints `Phases [...] X% i/N    Tasks [...] Y% j/M`
     using `█`/`░` block characters, where `N` is the number of active
     phases and `M = SprintConfig.total_tasks` from §2.6.
  4. Active panel shows `Prompt:` (from `phase.prompt_preview` — this
     should match the `**Goal:**` or first body line of the generated
     phase file) and `Agent:` (live) lines; a 3-line `Activity:` tail;
     `[thinking... Ns]` indicator after 2 s of idle.
  5. When a phase finishes, a `Summary: Phase N summary ready:
     results/phase-N-summary.md` line appears beneath the phase table
     (because `--no-tmux`).
  6. Success terminal panel shows `Turns`, `Tokens in/out` (K/M
     suffixes), `Output`, `Files`, `Log`.
- **Code under test:**
  - `src/superclaude/cli/sprint/tui.py`: `SprintTUI._render`,
    `_build_phase_table`, `_build_progress`, `_build_active_panel`,
    `_render_activity_stream`, `_build_success_panel`,
    `_format_tokens`.
  - `src/superclaude/cli/sprint/executor.py`: `_summary_fanout`
    closure when `config.tmux_session_name` is empty.
  - `src/superclaude/cli/sprint/monitor.py`: `_extract_signals_from_event`,
    `_handle_assistant_event`, `_handle_user_event`,
    `_append_activity`, `_append_error`.

### 4.2 Per-phase JSONL telemetry (Checkpoint W2 shadow mode)

Execution-log lives in the **release dir**, which
`load_sprint_config._resolve_release_dir` derives as the parent of the
`tasklists/` subdir — i.e. `$TEST_RELEASE`:

    grep '"event":"checkpoint_verification"' "$TEST_RELEASE/execution-log.jsonl" | head -5

- **Expected:** exactly one line per completed phase with fields
  `event`, `phase`, `mode`, `expected`, `found`, `missing`. In default
  shadow mode `missing` may be non-zero without altering the phase
  status.
- **Code under test:**
  - `src/superclaude/cli/sprint/executor.py`: `_verify_checkpoints`
    call site (around line 1409 / after `_determine_phase_status`).
  - `src/superclaude/cli/sprint/checkpoints.py`:
    `extract_checkpoint_paths`, `verify_checkpoint_files`.
  - `src/superclaude/cli/sprint/logging_.py`:
    `SprintLogger.write_checkpoint_verification`.
  - `src/superclaude/cli/sprint/config.py`: `_resolve_release_dir`
    (resolves to the grandparent when the index is inside a
    `tasklists/` subdir — as produced by `/sc:tasklist`).

### 4.3 Force `full` gate mode and observe status downgrade

Pick any end-of-phase checkpoint file that the sprint just wrote and
delete it, then re-run that phase with `--checkpoint-gate-mode full`:

    # Pick one end-of-phase checkpoint that exists and delete it.
    ls "$TEST_RELEASE/checkpoints/"CP-P*-END.md 2>/dev/null | head -1 | xargs rm -f

    # Re-run the affected phase with gate mode "full".
    superclaude sprint run "$TEST_INDEX" \
        --no-tmux --start 1 --end 1 --checkpoint-gate-mode full 2>&1 | tail -20

- **Expected:** the phase-2 row shows status `PASS⚠` (yellow) instead
  of `PASS`. The `is_success` property still returns True, so the
  sprint continues.
- **Code under test:**
  - `src/superclaude/cli/sprint/models.py`: `PhaseStatus.PASS_MISSING_CHECKPOINT`,
    `PhaseStatus.is_failure`, `PhaseStatus.is_success`.
  - `src/superclaude/cli/sprint/tui.py`: `STATUS_STYLES` and
    `STATUS_ICONS` entries for `PASS_MISSING_CHECKPOINT` (yellow,
    `PASS⚠`).
  - `src/superclaude/cli/sprint/executor.py`: gate-mode branching in
    `_verify_checkpoints`.

---

## 5. Post-sprint artifacts — TUI v2 Wave 3 + Checkpoint W3

### 5.1 Per-phase summary files

    ls "$TEST_RELEASE/results/"phase-*-summary.md
    head -20 "$TEST_RELEASE/results/"$(ls "$TEST_RELEASE/results/" | grep '^phase-.*-summary.md$' | head -1)

- **Expected:** one file per executed phase; each file has `#
  Phase N Summary — <name>` header, `**Status:**`, `**Turns:**`,
  `**Tokens:**`, sections `## Tasks`, `## Files Changed`, `##
  Validation Evidence`, `## Errors`, and a `## Narrative` that is
  either Haiku-generated prose or `_Narrative unavailable..._` when
  the Haiku binary is absent.
- **Code under test:**
  - `src/superclaude/cli/sprint/summarizer.py`:
    `PhaseSummarizer.summarize`, `_render_phase_summary_markdown`,
    `SummaryWorker._run` (plus the `on_summary_ready` callback).
  - `src/superclaude/cli/sprint/executor.py`: `_summary_worker.submit`
    call site after each phase completion.

### 5.2 Release retrospective

    ls "$TEST_RELEASE/results/release-retrospective.md"
    head -25 "$TEST_RELEASE/results/release-retrospective.md"

- **Expected:** a single `release-retrospective.md` with aggregate
  header (Outcome, Duration, Phases, Turns, Tokens, Files Changed),
  narrative section, `## Phase Outcomes` table, `## Files Changed`
  table with `Multi-phase` column, `## Validation Matrix`, `## Errors`.
- **Code under test:**
  - `src/superclaude/cli/sprint/retrospective.py`:
    `RetrospectiveGenerator.generate`, `_render_retrospective_markdown`,
    `_aggregate_*` helpers.
  - `src/superclaude/cli/sprint/executor.py`: blocking
    `RetrospectiveGenerator.generate` call at sprint end (before the
    terminal panel).

### 5.3 Checkpoint manifest

    test -f "$TEST_RELEASE/manifest.json" && \
        uv run python -c "
    import json
    m = json.load(open('$TEST_RELEASE/manifest.json'))
    print('total=%d found=%d missing=%d' % (m['total'], m['found'], m['total']-m['found']))
    "

- **Expected:** `total` equals the number of `Checkpoint Report Path:`
  entries the generator wrote across all phases (one per phase if the
  generator only emits end-of-phase checkpoints). After §4.3 the
  deleted file shows up as `missing ≥ 1`.
- **Code under test:**
  - `src/superclaude/cli/sprint/checkpoints.py`: `build_manifest`,
    `write_manifest`.
  - `src/superclaude/cli/sprint/executor.py`: manifest write block at
    sprint end.

### 5.4 SprintResult aggregates

    grep -E '"event":"sprint_summary"' "$TEST_RELEASE/execution-log.jsonl" | head -1

- **Expected:** the event includes `total_turns`, `total_tokens_in`,
  `total_tokens_out`, `total_output_bytes`, `total_files_changed` (all
  integers; values may be 0 for `--dry-run`).
- **Code under test:** `SprintResult` properties
  (`total_turns`/`total_tokens_in`/…/`total_files_changed`) in
  `src/superclaude/cli/sprint/models.py`.

---

## 6. Retroactive validation — Checkpoint W3 CLI  (commit `965213b`)

### 6.1 `verify-checkpoints` table output

    superclaude sprint verify-checkpoints "$TEST_RELEASE"

- **Expected:** A table row per checkpoint with `PHASE`, `NAME`,
  `EXISTS`, and `PATH`. After §4.3 the `CP-P02-MID.md` row reads
  `no` under `EXISTS`.
- **Code under test:** `src/superclaude/cli/sprint/commands.py`
  `verify_checkpoints` Click subcommand.

### 6.2 Machine-readable output

    superclaude sprint verify-checkpoints "$TEST_RELEASE" --json | \
        uv run python -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for e in d['entries'] if not e['exists']))"

- **Expected:** integer count of missing checkpoints (≥ 1 after §4.3).
- **Code under test:** `commands.py` → `verify-checkpoints --json`.

### 6.3 Auto-recovery

    # Recover the deleted checkpoint from §4.3.
    superclaude sprint verify-checkpoints "$TEST_RELEASE" --recover

    # Pick the checkpoint that was regenerated and read the first few lines.
    RECOVERED=$(superclaude sprint verify-checkpoints "$TEST_RELEASE" --json | \
        uv run python -c "import json,sys; d=json.load(sys.stdin); \
        print(next(e['expected_path'] for e in d['entries'] if e.get('recovered')))")
    echo "recovered: $RECOVERED"
    head -8 "$RECOVERED"

    # Idempotency: re-run must not overwrite
    cksum1=$(md5sum "$RECOVERED" | awk '{print $1}')
    superclaude sprint verify-checkpoints "$TEST_RELEASE" --recover
    cksum2=$(md5sum "$RECOVERED" | awk '{print $1}')
    test "$cksum1" = "$cksum2" && echo "IDEMPOTENT"

- **Expected:** file is regenerated, contains `## Note: Auto-Recovered`
  and `recovered: true` frontmatter; second `--recover` leaves it
  untouched (`IDEMPOTENT`).
- **Code under test:** `src/superclaude/cli/sprint/checkpoints.py`
  `recover_missing_checkpoints`.

---

## 7. Tmux 3-pane layout — TUI v2 Wave 4 (commit `08addac`)

> Skip this section if tmux is not installed. The `--no-tmux` fallback
> is already covered in §4.1.

### 7.1 Launch the sprint inside tmux

    superclaude sprint run "$TEST_INDEX"

Then, in a second terminal while the sprint is still running:

    tmux list-panes -t $(tmux list-sessions -F '#{session_name}' | grep sc-sprint-)

- **Expected:** exactly **3** panes. From top to bottom:
  1. `0.0` — TUI (50% of height).
  2. `0.1` — summary pane (25%), initially shows
     `Phase summaries will appear here...`.
  3. `0.2` — tail pane (25%) following the current phase's stream-json.
- **Code under test:** `src/superclaude/cli/sprint/tmux.py`
  `launch_in_tmux` (two `split-window` calls + `select-pane`),
  `TUI_PANE`/`SUMMARY_PANE`/`TAIL_PANE` constants.

### 7.2 Summary pane fan-out

After phase 1 completes, the summary pane content should update.

- **Expected:** Pane `:0.1` shows the rendered `phase-1-summary.md`
  after the `SummaryWorker` thread finishes.
- **Code under test:**
  - `src/superclaude/cli/sprint/tmux.py` `update_summary_pane`.
  - `src/superclaude/cli/sprint/summarizer.py`
    `SummaryWorker.on_summary_ready` callback (invoked from the
    daemon thread after commit).
  - `src/superclaude/cli/sprint/executor.py` `_summary_fanout`
    closure in tmux mode.

### 7.3 Tail pane migration guard

    grep -n '":0\.1"' src/superclaude/cli/sprint/tmux.py

- **Expected:** No hardcoded `:0.1` referring to the tail pane — every
  legacy reference goes through the `SUMMARY_PANE` / `TAIL_PANE`
  constants or `update_summary_pane` / `update_tail_pane`.
- **Code under test:** pane-index migration (`:0.1` → `:0.2`) in
  `tmux.py`.

---

## 8. Tasklist-protocol self-check — Checkpoint W4 (commit `8eba113`)

The tasklist skill emits deterministic task IDs and its Sprint
Compatibility Self-Check validates checkpoint structure. Because the
fixture in §2 was generated by the skill, we can assert those
invariants on the actual output rather than on a canned example.

### 8.1 Confirm skill frontmatter

    head -10 src/superclaude/skills/sc-tasklist-protocol/SKILL.md

- **Expected:** frontmatter `name: sc:tasklist-protocol`; body
  contains no `/sc:task-unified` references (verified by §0.3).

### 8.2 Checkpoint normalisation on the generated fixture

The Wave-4 contract is: every checkpoint is a numbered task
(`### T<PP>.<NN> -- Checkpoint: …`), never a bare `### Checkpoint:`
heading that the task scanner would miss.

    # 1. Every phase file must have at least one T<PP>.<NN> Checkpoint task.
    MISSING=0
    for f in "$TEST_RELEASE/tasklists"/phase-*-tasklist.md; do
      if ! grep -qE '^### T[0-9]{2}\.[0-9]{2}.*Checkpoint' "$f"; then
        echo "MISSING checkpoint task in: $f"
        MISSING=$((MISSING+1))
      fi
    done
    test "$MISSING" -eq 0 && echo "PASS — every phase has a checkpoint task"

    # 2. No legacy unmarked `### Checkpoint:` headings should remain.
    LEGACY=$(grep -rnE '^### Checkpoint:' "$TEST_RELEASE/tasklists" | wc -l)
    test "$LEGACY" -eq 0 && echo "PASS — no legacy checkpoint headings"

    # 3. Every phase's final checkpoint task should sit last in the file.
    for f in "$TEST_RELEASE/tasklists"/phase-*-tasklist.md; do
      LAST_TASK=$(grep -nE '^### T[0-9]{2}\.[0-9]{2}' "$f" | tail -1)
      echo "$(basename "$f"): last task = $LAST_TASK"
    done

- **Expected:**
  - Both `PASS …` lines appear.
  - Each phase file's last `T<PP>.<NN>` task contains `Checkpoint`
    (W4 contract: end-of-phase checkpoint is always the last task).
- **Code under test:** Wave 4 edits in
  `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (T04.01–T04.03
  from spec §4.1): generation rules, self-check rules, deliverable
  registry guidance.

### 8.3 Sprint CLI reads the Wave-4 shape without warnings

    uv run python -c "
    import os, re
    from pathlib import Path
    from superclaude.cli.sprint.config import load_sprint_config
    from superclaude.cli.sprint.checkpoints import extract_checkpoint_paths

    cfg = load_sprint_config(os.environ['TEST_INDEX'])
    for p in cfg.phases:
        paths = extract_checkpoint_paths(p.file, cfg.release_dir)
        assert paths, f'phase {p.number} has no checkpoint paths — Wave 4 generation bug'
        for name, path in paths:
            assert re.match(r'CP-P\d{2}(-\w+)?', Path(path).name), \
                f'unexpected checkpoint name: {path}'
    print('PASS — checkpoint paths extracted cleanly from every phase')
    "

- **Expected:** `PASS — checkpoint paths extracted cleanly from every phase`.
- **Code under test:**
  - `src/superclaude/cli/sprint/checkpoints.py::extract_checkpoint_paths`
    (accepts both the legacy `### Checkpoint:` heading and the Wave-4
    `### T<PP>.<NN> -- Checkpoint:` task form).
  - `src/superclaude/cli/sprint/config.py::load_sprint_config`.

---

## 9. Unit + regression suite

### 9.1 Full sprint suite

    uv run pytest tests/sprint/ --no-header -q 2>&1 | tail -3

- **Expected:** `921 passed, 57 failed`. Zero net-new failures vs
  baseline.
- **Code under test:** every module under `src/superclaude/cli/sprint/`.

### 9.2 TUI waves

    uv run pytest \
        tests/sprint/test_tui_v2_wave1.py \
        tests/sprint/test_tui_v2_wave2.py \
        tests/sprint/test_tmux.py \
        tests/sprint/test_summarizer.py \
        tests/sprint/test_retrospective.py \
        -v --no-header 2>&1 | tail -20

- **Expected:** all pass.
- **Code under test:** TUI Waves 1–4 + summarizer + retrospective.

### 9.3 Naming regression

    uv run pytest tests/sprint/test_process.py::TestClaudeProcess -v --no-header 2>&1 | tail -10

- **Expected:** `test_build_prompt_contains_task_command` passes.
- **Code under test:** `process.ClaudeProcess.build_prompt`.

### 9.4 Ruff sanity

    uv run ruff check src/superclaude/cli/sprint/ 2>&1 | tail -5

- **Expected:** `All checks passed!` OR the same set of pre-existing
  findings that were present before the release (`F401 StepStatus`,
  `N806 _OLD_TO_NEW`, `F541` on redundant f-strings in `models.py`).

---

## 10. Destructive teardown (optional)

Removes the fixture so it does not clutter `/tmp`.

    rm -rf "$TEST_RELEASE"

---

## Mapping index — find "which test covers what I just changed"

| Change area | Scenario section(s) | Entry-point symbol(s) |
|---|---|---|
| Naming rename                         | 1.1, 1.2, 1.3, 9.3     | `task.md` / `sc-task-protocol` / `build_prompt` |
| Spec-to-roadmap pipeline              | 2.2                    | `superclaude roadmap run` |
| Roadmap-to-tasklist generator (skill) | 2.3, 2.4, 8.2          | `sc-tasklist-protocol/SKILL.md`, `tasklist.md` command shell |
| Tasklist validator                    | 2.5                    | `superclaude tasklist validate` |
| Release-dir resolution (tasklists/ subdir) | 2.6, 4.2             | `config._resolve_release_dir` |
| Prompt checkpoint block (W1)          | 3.1                    | `ClaudeProcess.build_prompt` |
| Post-phase checkpoint gate (W2)       | 4.2, 4.3               | `_verify_checkpoints`, `SprintLogger.write_checkpoint_verification` |
| Checkpoint manifest + CLI (W3)        | 5.3, 6.1, 6.2, 6.3     | `build_manifest`, `recover_missing_checkpoints`, `commands.verify_checkpoints` |
| Tasklist-level checkpoints (W4)       | 2.4, 8.2, 8.3          | `sc-tasklist-protocol/SKILL.md`, `extract_checkpoint_paths` |
| MonitorState / PhaseResult / SprintResult fields (Wave 1) | 2.6, 4.1, 5.4          | `monitor._extract_signals_from_event`, model field defaults |
| SprintConfig.total_tasks + count_tasks_in_file | 2.6                    | `config.count_tasks_in_file`, `config.load_sprint_config` |
| Phase table / dual progress / terminal panels (Wave 2) | 4.1                    | `tui._build_phase_table`, `tui._build_progress`, `tui._build_success_panel` |
| Prompt / Agent / activity stream (Wave 2) | 4.1                    | `tui._build_active_panel`, `tui._render_activity_stream` |
| Conditional error panel (Wave 2)      | 4.1 (with induced errors) | `tui._build_error_panel` |
| Phase summary files (Wave 3)          | 5.1                    | `PhaseSummarizer.summarize`, `SummaryWorker._run` |
| Release retrospective (Wave 3)        | 5.2                    | `RetrospectiveGenerator.generate` |
| Haiku subprocess convention           | 5.1 narrative fallback | `summarizer.invoke_haiku` |
| 3-pane tmux layout (Wave 4)           | 7.1, 7.3               | `tmux.launch_in_tmux`, pane constants |
| Summary pane fan-out (Wave 4)         | 7.2                    | `tmux.update_summary_pane`, `SummaryWorker.on_summary_ready`, `executor._summary_fanout` |
| `--no-tmux` summary notification      | 4.1 (§6)               | `SprintTUI.latest_summary_notification`, `tui._render` |
