---
dd: DD-3
verdict: REFACTOR
confidence: 0.86
---

## Adversarial findings

DD-3's **intent** is sound and upheld: cleanup must be non-destructive (move/copy, never
delete), restorable, audit-logged, and reuse the recovery infrastructure. But three of its
**mechanism citations are factually wrong**, and as written the decision depends on code that
either does not exist or does not do what the design says.

**F1 — "Reuse the recovery engine's `.failed-<ts>` rename (recovery.py:445-492)" — NOT reusable as-is.**
Lines 445-492 are **inlined three times inside `merge_recovery_bundle`** (recovery.py:381),
once each for `-output.txt` (445-451), `phase-N-cp*.md` checkpoints (466-472), and
`-errors.txt` (487-494). There is no standalone helper to import. The `.failed-<ts>` rename
also mutates `bundle.artifacts_replaced[canonical] = preserved` (449/471/492) — a map that
lives on a **RecoveryBundle** object that only `merge_recovery_bundle` constructs. The
BoundaryIntegrityGate is not running a bundle merge, so it has no bundle to record into.
DD-3 therefore requires a **non-trivial extraction/refactor** (a `quarantine_artifact(path,
audit_log) -> preserved_path` helper independent of RecoveryBundle), which the design does
not acknowledge as work.

**F2 — "Mirrors `rerun-tasks --restore` / a future `sprint resume --restore` reverses it" — the reversal path does not exist.**
The existing `--restore` (commands.py:481, dispatched at rerun_tasks.py:1261-1268) calls
`restore_from_bundle` (rerun_tasks.py:1039), which copies files back from
`<bundle_dir>/preserved/` using `preserved/manifest.json`. That `preserved/` dir is created
by `stash_and_restore_deliverables` (rerun_tasks.py:961) as a **`shutil.copy2` COPY-stash** —
a completely different mechanism from the `.failed-<ts>` **rename** in `merge_recovery_bundle`.
**No existing code reverses a `.failed-<ts>` rename.** And there is **no `resume` subcommand**
in `commands.py` (commands at lines 72/294/306/318/343/361/419; none named `resume`), so
`sprint resume --restore` is vaporware. The design's §4 "Non-destructive guarantee" leans on
a command that does not exist and a reversal that no code performs.

**F3 — Gate quarantine is redundant with (and races) the dispatched rerun engine.**
On the TASK-granularity path the gate dispatches to `run_rerun_tasks` (design §6), which
**already** stashes the boundary task's `phase-{phase}-task-{id}-*` artifacts via
`stash_and_restore_deliverables` (called in the run flow; glob at rerun_tasks.py:988) and
then renames them in merge steps 1-3. A gate that pre-renames the same canonical files to
`.failed-<ts>` either (a) duplicates that work or (b) corrupts the engine's stash glob (the
engine would stash the `.failed-<ts>` sibling or miss the canonical). Position A's strongest
steelman — "rename removes the half-written file from the rerun glob" — therefore backfires:
the rerun engine *wants* the canonical name present so it can stash it first.

**F4 — Detection coverage gap (guard_conditions, HIGH).** The gate's "partial" predicate
(design §4(b)) is `transcript exists but derived_status in {INCOMPLETE, FAIL_*}`. A
next task that **never started** has no `phase-N-task-<id>-output.txt`, so
`_classify_transcript` (rerun_tasks.py:550, returns INCOMPLETE only when a transcript body
exists) is never reached — and half-written **deliverable files** (declared under
`**Artifacts (Intended Paths):**`, surfaced only by `_declared_deliverables`,
rerun_tasks.py:924) are not transcripts and are not covered by the gate's transcript-based
detection. The design conflates "quarantine canonical [transcript]" with "quarantine partial
deliverables"; these are different file classes.

**F5 — Lock omission (collection_boundaries, MEDIUM).** The recovery engine guards results/
mutations with `.recovery-locks/phase-{phase}.lock` (`acquire_recovery_lock`,
recovery.py:275-345). DD-3 has the **gate** mutate results/ (rename + audit append) but never
takes that lock, so a gate quarantine races a concurrent `rerun-tasks` on the same phase.

**F6 — Imprecise git-tracking rationale.** DD-3 dismisses git-stash because "results
artifacts aren't necessarily tracked." Verified nuance: `.gitignore:230` ignores
`phase-*-task-*-output.txt` (per-task transcripts — the gate's main target), but
`execution-log.jsonl`, `phase-N-result.json`, and phase-level `phase-N-output.txt` **are
tracked**. The anti-git-stash conclusion still holds (you cannot `git stash` ignored files,
and the operator's tree may hold unrelated changes), but the stated reason is half-wrong.

**Round 2.5 invariant probe:** 4 HIGH UNADDRESSED (F1/F2 sufficiency+interaction, F3 state,
F4 guard) → convergence **BLOCKED** for DD-3 as written. Debate outcome: report-only default
+ reuse the existing `preserved/`+`manifest.json` COPY shape (reversible by the
`restore_from_bundle` code that exists today) dominates rename-in-place on correctness, risk,
and reversibility; rename's only edge (O(1)) is nullified by F3.

## Code verification (file:line)

- `merge_recovery_bundle`: `recovery.py:381`. `.failed-<ts>` rename **inlined ×3**:
  output `:445-451`, checkpoints `:466-472`, errors `:487-494`; each sets
  `bundle.artifacts_replaced[...] = preserved` (`:449,:471,:492`). Bundle-scoped, no
  standalone helper.
- `write_recovery_audit_log`: `recovery.py:250-267` — real reusable append-only helper
  (the audit-log half of DD-3 IS reusable as-is).
- `.recovery-locks` lock: `acquire_recovery_lock` `recovery.py:275-345`;
  `release_recovery_lock` `:348-353`. Gate path does not acquire it.
- `--restore` reverses a COPY-stash, NOT the rename: dispatch `rerun_tasks.py:1261-1268` →
  `restore_from_bundle` `:1039-1081` (reads `preserved/manifest.json`, `shutil.copy2` back);
  stash author `stash_and_restore_deliverables` `:961-1036` (glob `:988`, copy `:1004`).
  `--restore` CLI option `commands.py:481-498`.
- No `resume` subcommand: `commands.py` commands at `:72,:294,:306,:318,:343,:361('verify-checkpoints'),:419('rerun-tasks')`. `sprint resume --restore` does not exist.
- Detection classifier: `_classify_transcript` `rerun_tasks.py:550-598` (INCOMPLETE requires a
  transcript body); `discover_failed_tasks_from_transcripts` `:601`; `_declared_deliverables`
  (deliverable files, separate class) `:924-948`.
- Artifact naming: `task_output_file` `models.py:561-562`
  (`phase-{n}-task-{id}-output.txt`), `task_errors_file` `:565`, `phase_result_json` `:570`.
- Git tracking: `.gitignore:230` ignores `phase-*-task-*-output.txt`; `execution-log.jsonl`,
  `phase-N-result.json`, `phase-N-output.txt` are tracked (`git ls-files`).

## Proposed spec changes

### Change 1 — DD-3 table row (design.md line 25). Replace EXACTLY:

```
| **DD-3** | Cleanup mechanism | **Preserve-rename quarantine, never delete.** Reuse the recovery engine's `.failed-<ts>` rename + `artifacts_replaced` map + `recovery-audit.log` (`recovery.py:445-492`). Restorable, mirrors `rerun-tasks --restore`. Not git-stash (results artifacts aren't necessarily tracked). Report-only when classification is uncertain. | `recovery.py:445-492`, `recovery-audit.log` |
```

with:

```
| **DD-3** | Cleanup mechanism | **Report-only by default; opt-in copy-to-quarantine, never rename-in-place, never delete.** Default gate behavior is detect + print suspect paths + STOP (honors NFR-1 literally; the STOP already forces the operator decision FR-2.4 requires). When the operator opts into cleanup, COPY (`shutil.copy2`) suspect artifacts into `<results>/.resume-quarantine-<ts>/` with a `manifest.json` of the SAME shape `stash_and_restore_deliverables` writes (`rerun_tasks.py:961-1036`), so the EXISTING `restore_from_bundle` (`rerun_tasks.py:1039`) reverses it — no new restore verb. Reuse only `write_recovery_audit_log` (`recovery.py:250`, append a `resume_quarantine` line). Do NOT reuse the `.failed-<ts>` rename: it is inlined inside `merge_recovery_bundle` (not a callable helper), is bundle-scoped via `artifacts_replaced`, is NOT reversed by `rerun-tasks --restore`, and would race/duplicate the rerun engine's own stash on the TASK path. Acquire `.recovery-locks/phase-{phase}.lock` (`recovery.py:275`) before any results/ mutation. Not git-stash: per-task transcripts are gitignored (`.gitignore:230`) and the working tree may hold unrelated changes. | `recovery.py:250`, `rerun_tasks.py:961-1081`, `.recovery-locks` `recovery.py:275` |
```

### Change 2 — §4(b) gate body (design.md lines 159-165). Replace EXACTLY:

```
  # (b) next-unfinished partial-work quarantine (DD-3, FR-2.2 / FR-2.3)
  nu = plan.boundary_tasks.role==next_unfinished  (or whole-phase set when granularity=PHASE)
  partial = transcript exists but derived_status in {INCOMPLETE, FAIL_*}, or stray output files
  if partial:
      preserve_rename canonical → canonical.with_suffix(.failed-<ts>)    # recovery.py:445-492 pattern
      append recovery-audit.log {event: "resume_quarantine", task, preserved}
      quarantined[canonical] = preserved
```

with:

```
  # (b) next-unfinished partial-work detection + opt-in quarantine (DD-3, FR-2.2 / FR-2.3)
  nu = plan.boundary_tasks.role==next_unfinished  (or whole-phase set when granularity=PHASE)
  # Cover BOTH file classes: transcript (phase-N-task-<id>-output.txt) AND declared
  # deliverables (_declared_deliverables, rerun_tasks.py:924) — a never-started task has
  # no transcript, so transcript-only detection misses half-written deliverables.
  partial = (transcript exists and derived_status in {INCOMPLETE, FAIL_*})
            or any declared-deliverable path for nu exists on disk
            or stray phase-N-task-<id>-* output files exist
  if partial:
      report suspect paths in BoundaryReport (always)                     # FR-2.2 surface
      if cleanup_opted_in:                                                # default: report-only
          acquire .recovery-locks/phase-{phase}.lock                      # recovery.py:275
          qdir = results_dir/(".resume-quarantine-" + ts)
          copy suspect paths → qdir preserving structure; write qdir/manifest.json
                                                                          # same shape as rerun_tasks.py:961
          append recovery-audit.log {event:"resume_quarantine", task, manifest: qdir/manifest.json}
          quarantined[canonical] = qdir-copy                              # reversible via restore_from_bundle
      # NOTE: on granularity==TASK the dispatched run_rerun_tasks ALREADY stashes these via
      # stash_and_restore_deliverables — the gate must NOT also rename them (glob collision).
```

### Change 3 — §4 Non-destructive guarantee (design.md lines 172-174). Replace EXACTLY:

```
**Non-destructive guarantee (NFR-1, DD-3):** the only filesystem mutation is the
preserve-rename (move, not delete) + an append to `recovery-audit.log`. A future
`sprint resume --restore` (parallel to `rerun-tasks --restore`) reverses it.
```

with:

```
**Non-destructive guarantee (NFR-1, DD-3):** by default the gate performs NO results/
mutation — it detects, prints, and STOPs. When cleanup is opted into, the only mutations are
a `shutil.copy2` into `<results>/.resume-quarantine-<ts>/` (the canonical original is left
untouched) plus a `recovery-audit.log` append, both under `.recovery-locks/phase-{phase}.lock`.
Because the quarantine dir reuses the `preserved/`+`manifest.json` shape, the EXISTING
`restore_from_bundle` (`rerun_tasks.py:1039`) reverses it as-is — no new `sprint resume
--restore` verb is required (and none exists today).
```

### Change 4 — §12 risk note (design.md line 322, R4 line in merged-requirements is fine; design §12 has no R4 — add one line after line 325). INSERT after:

```
- New micro-risk: the single write-path change (DD-4 `tasklist_sha256`) must stay
  backward-compatible — absent field ⇒ planner falls back to Tier-1/2 drift, never crashes.
```

the line:

```
- DD-3 reuse-surface corrected: the `.failed-<ts>` rename is NOT a reusable helper and is NOT
  reversed by any existing `--restore`; the gate instead reuses `write_recovery_audit_log`
  + the `preserved/`-shaped COPY quarantine that `restore_from_bundle` already reverses, and
  takes `.recovery-locks` before mutating results/.
```
