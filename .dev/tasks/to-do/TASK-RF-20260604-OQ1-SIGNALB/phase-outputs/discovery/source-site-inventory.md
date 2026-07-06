# Source Site Inventory (Step 2.1)

**Date:** 2026-06-04
**Source read from worktree:** `/config/workspace/IronClaude/.dev/worktrees/fix-sprint-integrity-signalb-pass-recovered/src/superclaude/cli/sprint/resume/integrity.py`
**Research basis:** `research/01-integrity-signalb-edit.md`

## File presence confirmed

`src/superclaude/cli/sprint/resume/integrity.py` **is present** on branch `fix/sprint-integrity-signalb-pass-recovered` (base `origin/master` @ `02949fb3`). The research note flagged that the file was absent on the *previously-checked-out* branch; on this fresh worktree from `origin/master` it exists and matches the researched content line-for-line.

## Current Signal B block — exact worktree lines

`_validate_last_completed` spans **integrity.py:92–154**. The Signal B block is at **integrity.py:127–131**:

```python
        # Signal B — independent re-derivation from the transcript (under lc_phase).
        transcript = self._read_transcript(results_dir, lc_phase, lc.task_id)
        derived = _classify_transcript(transcript)
        lc.derived_status = derived
        signal_b_pass = derived is TaskStatus.PASS
```

Stable-text anchors (all present, verified in worktree):
- `derived = _classify_transcript(transcript)` — line 129
- `lc.derived_status = derived` — line 130
- `signal_b_pass = derived is TaskStatus.PASS` — line 131

Surrounding unchanged context:
- Signal A: **integrity.py:122–125** (`signal_a_pass = lc.persisted_status is not None and lc.persisted_status.is_success`)
- Artifacts block: **integrity.py:133–148** (unchanged)
- Verdict: **integrity.py:150–154** (`validated = signal_a_pass and signal_b_pass and artifacts_ok`; unchanged)

## Intended replacement shape (Opt-2a)

Replace **only** lines 127–131 (the Signal B block) so the transcript read stays, then branch:

```python
        # Signal B — independent re-derivation from the transcript (under lc_phase).
        transcript = self._read_transcript(results_dir, lc_phase, lc.task_id)
        if lc.persisted_status is TaskStatus.PASS_RECOVERED:
            # PASS_RECOVERED is already transcript-evidence-based in the executor
            # (error_max_turns after completion evidence). Preserve that recovery
            # basis for report transparency instead of forcing the clean-PASS
            # classifier path, which structurally cannot emit PASS_RECOVERED.
            derived = TaskStatus.PASS_RECOVERED
            lc.derived_status = derived
            signal_b_pass = True
        else:
            derived = _classify_transcript(transcript)
            lc.derived_status = derived
            signal_b_pass = derived is not None and derived.is_success
```

Properties of the replacement:
- **Narrow guard:** exemption applies **only** when `lc.persisted_status is TaskStatus.PASS_RECOVERED`. Ordinary `PASS` falls to the `else` branch and is still transcript-rechecked.
- **Transparency:** the recovered branch assigns `lc.derived_status = TaskStatus.PASS_RECOVERED` (report shows recovered basis, not a fabricated clean PASS).
- **Future-proof non-recovered path:** `else` uses Opt-1 widening `derived is not None and derived.is_success` (behaviorally identical to `derived is TaskStatus.PASS` for ordinary PASS today, since `TaskStatus.PASS.is_success` is True and other statuses are not — confirmed in Step 2.3).
- **No edit to verdict/artifacts:** `artifacts_ok` and `validated = signal_a_pass and signal_b_pass and artifacts_ok` remain byte-for-byte unchanged.

## No-edit constraint

`_classify_transcript` (defined in `src/superclaude/cli/sprint/rerun_tasks.py`) **MUST remain untouched**. It is imported locally inside `_validate_last_completed` and is also consumed by `discover_failed_tasks_from_transcripts` (rerun discovery). Widening the classifier (Opt-2b) is rejected; the blast radius stays inside `integrity.py`.

## Verification statements

- Inventory is based on the **worktree** file, not stale `/tmp` extraction.
- `src/superclaude/cli/sprint/resume/integrity.py` confirmed present on the branch.
- **No source edit has been applied yet** — this is discovery only.
- No line numbers or code were fabricated; all anchors verified against the worktree Read.
