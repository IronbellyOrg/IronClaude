# Research: Checkpoint gate plumbing

Status: Complete

Scope: integration points / data flow for Defect 2 — gated end-of-phase checkpoint stays FAIL/BLOCKED after successful task recovery. Determine whether Fix-2 PRIMARY (re-run the checkpoint task) is feasible or whether FALLBACK (re-stamp stale FAIL/BLOCKED -> UNKNOWN) is required.

All paths are absolute. Code citations are `file:line`.

---

## FIX-2 FEASIBILITY VERDICT (up front)

**PRIMARY (re-run the gated checkpoint TASK after a successful merge) IS FEASIBLE in this codebase.**

The end-of-phase checkpoint is a **first-class, selectable, runnable task** in generated tasklists — not a passive verification block. In the real generated tasklist `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/tasklists/phase-12-tasklist.md`, the end-of-phase gate appears as:

```
783:### T12.17 -- Checkpoint: End of Phase 12
...
802:**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P12-END.md
...
816:**Steps:**
817:1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
818:2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
819:3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.
...
822:- File `TASKLIST_ROOT/checkpoints/CP-P12-END.md` exists and contains `status: PASS`.
```

`T12.17` carries a `### T<PP>.<NN>` heading, an executable `**Steps:**` block that ends in "Write the checkpoint report", and a `**Checkpoint Report Path:**` that resolves to `CP-P12-END.md` — exactly the file `_check_checkpoint_pass` reads. Because `rerun-tasks` selects task blocks **by T-ID heading** (`TASK_BLOCK_PATTERN = ^### (T\d{2}\.\d{2})\b`, rerun_tasks.py:61-63), `T12.17` is a valid rerun target. Re-running it produces a **real verdict** by re-writing `CP-P12-END.md` with `status: PASS`.

**FALLBACK (re-stamp stale FAIL/BLOCKED -> UNKNOWN) is still required as a guard** for tasklists where no runnable end-of-phase checkpoint task exists. Critically, the *existing* `recover_missing_checkpoints` machinery does **NOT** cover the stale-FAIL case — it only writes when the file is **missing** (`entry.exists == False`, checkpoints.py:262) and is idempotent against any existing file (checkpoints.py:249-260). A FAIL/BLOCKED `CP-P12-END.md` already exists on disk, so recover leaves it untouched. The fallback re-stamp is therefore net-new behavior, not a reuse of recover.

Detail and evidence below.

---

## 1. `checkpoint_gate_mode` — definition, default, read sites, `--no-verify-checkpoints` interaction

### Definition + default
`src/superclaude/cli/sprint/models.py:566`
```python
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```
Comment block (models.py:563-565): `off=disabled, shadow=log JSONL only, soft=log + stdout warning, full=log + downgrade PASS to PASS_MISSING_CHECKPOINT on missing files`. **Default = `shadow`** (JSONL event only, never alters status).

### Every read site under `src/superclaude/cli/sprint/`
- `executor.py:2449` — `mode = getattr(config, "checkpoint_gate_mode", "shadow")` inside `_verify_checkpoints(...)` (executor.py:2427-2507). This is the **only** behavioral consumer.
- `executor.py:2004` and `models.py:399` — comments/docstrings only, no logic.

### What `_verify_checkpoints` does with the mode (executor.py:2449-2507)
- `off` -> returns status unchanged (2450-2451).
- `shadow` (default) -> emits `checkpoint_verification` JSONL event only (2472-2478), returns status unchanged (2486-2487 if nothing missing, else falls through but neither soft nor full -> returns status).
- `soft` -> JSONL + stdout warning (2499-2503), status unchanged.
- `full` -> returns `PhaseStatus.PASS_MISSING_CHECKPOINT` only when a **declared `Checkpoint Report Path:` file is missing** (2504-2505).

**Crucial scoping fact:** `_verify_checkpoints` is gated on `status == PhaseStatus.PASS` (executor.py:2008) and reacts ONLY to *missing* declared files. It does NOT read PASS/FAIL content of the checkpoint report and does NOT participate in the recovery/`_check_checkpoint_pass` path. So `checkpoint_gate_mode` is **orthogonal to Defect 2** — it cannot be the lever that re-clears a stale FAIL/BLOCKED report.

### `--no-verify-checkpoints` interaction with `checkpoint_gate_mode`
They are **unrelated**. `--no-verify-checkpoints` is a `rerun-tasks` CLI flag (commands.py:755-759):
```
--no-verify-checkpoints : "Skip the post-merge verify-checkpoints --recover auto-invoke."
```
It only toggles the Step-14 subprocess call to `superclaude sprint verify-checkpoints --recover` (rerun_tasks.py:1508-1532). It does **not** touch `config.checkpoint_gate_mode` and does not influence the executor gate. Default in the programmatic path is `no_verify_checkpoints=False` (commands.py:526), i.e. the post-merge recover pass runs by default.

---

## 2. How the executor evaluates a checkpoint verdict — `_check_checkpoint_pass`

`src/superclaude/cli/sprint/executor.py:2510-2521` (quoted verbatim):
```python
def _check_checkpoint_pass(config: SprintConfig, phase: Phase) -> bool:
    """Return True if the end-of-phase checkpoint file exists with status PASS."""
    checkpoint_path = (
        config.release_dir / "checkpoints" / f"CP-P{phase.number:02d}-END.md"
    )
    if not checkpoint_path.exists():
        return False
    try:
        content = checkpoint_path.read_text(errors="replace").upper()
        return "STATUS: PASS" in content or "**RESULT**: PASS" in content
    except OSError:
        return False
```

### Path derivation
`CP-Pxx-END.md` is derived as `config.release_dir / "checkpoints" / f"CP-P{phase.number:02d}-END.md"` (executor.py:2512-2514). Note: this is `config.release_dir`, the executor's work dir, **not** `config.index_path.parent` (see §4 for why that distinction matters for the rerun subprocess).

### Strings read from the report
After `.upper()`, the function returns True iff the content contains either:
- `"STATUS: PASS"` (matches `status: PASS` frontmatter — the form generated tasklists require, see phase-12 line 822), OR
- `"**RESULT**: PASS"` (matches a bolded `**Result**: PASS` line).

### Where the verdict is consumed (crash-recovery inference path)
`_check_checkpoint_pass` is called from `_determine_phase_status` (executor.py:2788), only on the **non-zero exit** branch (executor.py:2774+), as "Path 2 — General: checkpoint inference (Spec A SOL-C)" (2785-2792). If the checkpoint reads PASS and no cross-phase contamination is found, the phase is upgraded to `PhaseStatus.PASS_RECOVERED` (2792). Implication for Fix-2: a checkpoint that reads `UNKNOWN` (the recover/re-stamp form) will return False here and will NOT be treated as PASS — which is the intended safety property (never auto-PASS).

---

## 3. Is the end-of-phase checkpoint a RUNNABLE TASK or a passive block? — RUNNABLE TASK

**Answer: RUNNABLE TASK.** Evidence from the real generated tasklist `/config/workspace/TUIBBS-scp/.dev/releases/current/v1-MVP/tasklists/phase-12-tasklist.md`:

- Mid-phase checkpoints are tasks: `T12.06 -- Checkpoint: Phase 12 / Tasks T12.01-T12.05` (line 249), `T12.16 -- Checkpoint: Phase 12 / Tasks T12.07-T12.15` (line 732).
- End-of-phase checkpoint is a task: `### T12.17 -- Checkpoint: End of Phase 12` (line 783), with:
  - `**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P12-END.md` (line 802),
  - an executable `**Steps:**` block whose step 3 is "Write the checkpoint report to the Checkpoint Report Path above" (lines 816-819),
  - acceptance criterion "File ... `CP-P12-END.md` exists and contains `status: PASS`" (line 822),
  - `**Dependencies:** T12.01..T12.15` (line 831).

The heading form matches BOTH parser patterns:
- `rerun-tasks` selection: `TASK_BLOCK_PATTERN = re.compile(r"^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}|\Z)", ...)` (rerun_tasks.py:61-63) — `### T12.17 -- Checkpoint:` matches `^### (T12.17)\b`. So `T12.17` is extractable/selectable as a rerun target.
- checkpoints.py heading pattern: `CHECKPOINT_HEADING_PATTERN = re.compile(r"^#{2,5}\s*(?:T\d{2}\.\d{2}\s*--\s*)?Checkpoint:\s*(.+?)\s*$", ...)` (checkpoints.py:34-37) — same heading also recognized as a named checkpoint for path extraction.

So the executor reads `CP-P12-END.md` passively via `_check_checkpoint_pass`, but the **report itself is produced by an agent running the runnable task `T12.17`**. Re-running `T12.17` regenerates `CP-P12-END.md` with a real verdict. This is the structural basis that makes Fix-2 PRIMARY feasible.

Caveat for the builder: rerun selection is purely heading/T-ID based; sprint phase tasklists carry **no per-task checkboxes** (rerun_tasks.py:356-358, 642-651 — the `[x]/[ ]` flip is a defensive no-op when absent). The checkpoint task is selected by T-ID, not by a checkbox, so absence of a checkbox is not a blocker. The builder must, however, target the correct end-of-phase T-ID (e.g. `T12.17`) for the affected phase — that T-ID is discoverable by scanning the phase tasklist for the `### T<PP>.<NN> -- Checkpoint:` heading whose name matches `End of Phase` and/or whose `Checkpoint Report Path:` resolves to `CP-P{phase:02d}-END.md`.

---

## 4. `recover_missing_checkpoints` reachability from rerun Step-14 + canonical-dir confirmation

### Data flow (confirmed)
rerun_tasks.py Step-14 (rerun_tasks.py:1508-1532): after a successful run + merge-back (`exit_code == 0 and merge_back and not no_verify_checkpoints`), it shells out:
```python
subprocess.run(["uv","run","superclaude","sprint","verify-checkpoints",
                str(config.index_path.parent), "--recover"], check=False)
```
The `verify-checkpoints` command (commands.py:647-702) then:
1. resolves `index_path = output_dir / "tasklist-index.md"` (commands.py:680),
2. builds the manifest from declared checkpoints (commands.py:684),
3. with `--recover`: discovers phases, maps phase->tasklist, and calls `recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists)` (commands.py:686-693),
4. writes `manifest.json` (commands.py:695-696).

### Canonical release dir confirmation
Step-14 deliberately passes `str(config.index_path.parent)` (rerun_tasks.py:1526), NOT `config.release_dir`. The inline comment (rerun_tasks.py:1518-1525) states `index_path` is absolute (resolved in `load_sprint_config`), so `.parent` is cwd-independent and is the directory that actually contains `tasklist-index.md`; passing `config.release_dir` would resolve to the grandparent in the `sc:tasklist` subdir layout where `tasklist-index.md` does not live. **This confirms the recover pass operates on the canonical release dir (`config.index_path.parent`).**

Note a path asymmetry the builder must reconcile: `_check_checkpoint_pass` derives the checkpoint file from `config.release_dir / "checkpoints"` (executor.py:2512-2514), whereas verify-checkpoints derives it from `index_path.parent` (= the OUTPUT_DIR positional). For a Fix-2 PRIMARY re-run of the checkpoint task to clear the executor's view, the regenerated `CP-Pxx-END.md` must land where `_check_checkpoint_pass` looks. Whether `config.release_dir == config.index_path.parent` depends on layout; in the flat layout they coincide, in the `sc:tasklist` subdir layout they differ. The builder should pin the write target explicitly rather than assume equality.

### Why recover does NOT solve Defect 2 (the stale-FAIL gap)
`recover_missing_checkpoints` (checkpoints.py:213-321) writes a report ONLY when the entry is **missing**:
- It refreshes existence first; if `entry.expected_path.is_file()` it returns the entry unchanged (checkpoints.py:248-260).
- It skips entries where `entry.exists` is already True (checkpoints.py:262-264).
- The report it writes carries ``## Result\n\n`UNKNOWN``` (checkpoints.py:435-438) and frontmatter `recovered: true` (checkpoints.py:419) — never `status: PASS`.

A stale FAIL/BLOCKED `CP-Pxx-END.md` is a file that **exists**, so recover never overwrites it. Therefore Defect 2 (a *present* FAIL/BLOCKED report) is outside recover's contract. The Fix-2 FALLBACK (re-stamp existing stale FAIL/BLOCKED -> UNKNOWN) is genuinely new logic; the only reusable asset from recover is the `UNKNOWN`/`recovered: true` reporting shape and the `_render_recovered_checkpoint` template (checkpoints.py:398-439), which the builder can mirror so a re-stamped report is visually consistent.

---

## Summary for the builder

- **Fix-2 PRIMARY is feasible**: the end-of-phase checkpoint is a runnable T-ID task (`T12.17 -- Checkpoint: End of Phase 12`) with executable steps that write `CP-Pxx-END.md`; `rerun-tasks` can select it by heading (`TASK_BLOCK_PATTERN`, rerun_tasks.py:61-63). Re-running it yields a real `status: PASS`/`**Result**: PASS` verdict that `_check_checkpoint_pass` (executor.py:2510-2521) reads.
- **Discovery hook for the checkpoint T-ID**: scan the phase tasklist for `### T<PP>.<NN> -- Checkpoint:` whose `**Checkpoint Report Path:**` resolves to `CP-P{phase:02d}-END.md` (patterns at checkpoints.py:26-37).
- **FALLBACK still needed** for tasklists lacking a runnable end-of-phase checkpoint task; it must re-stamp an EXISTING stale FAIL/BLOCKED report to UNKNOWN — net-new, since `recover_missing_checkpoints` only handles missing files (checkpoints.py:248-264) and never overwrites or auto-PASSes (writes `UNKNOWN`, checkpoints.py:435-438).
- **`checkpoint_gate_mode` is orthogonal** to Defect 2 (default `shadow`, models.py:566; only consumer `_verify_checkpoints` reacts to *missing* declared files in `full` mode, executor.py:2449-2507). Do not use it as the fix lever.
- **`--no-verify-checkpoints`** only toggles the Step-14 `verify-checkpoints --recover` subprocess (commands.py:755-759; rerun_tasks.py:1508-1532); unrelated to the gate mode.
- **Path-asymmetry watch-out**: `_check_checkpoint_pass` reads `config.release_dir/checkpoints/...` (executor.py:2512-2514); the rerun recover subprocess operates on `config.index_path.parent` (rerun_tasks.py:1526). The Fix-2 regenerated/re-stamped report must land where `_check_checkpoint_pass` looks; pin the target explicitly.
