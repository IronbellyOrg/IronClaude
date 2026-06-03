---
title: "Technical Design — Auto-Resume as Default for Sprint Pipeline"
feature_slug: sprint-auto-resume-default
domain: architecture
type: component-design
status: design
created: 2026-06-02
source_requirements: ./merged-requirements.md
target_version: v4.3.5
---

# Design: Auto-Resume as the Default for `sprint run` / `rerun-tasks`

Turns `merged-requirements.md` (FR-1..5) into engineering contracts. All file/symbol/path
references below were re-verified against the worktree on 2026-06-02 (see §11 Evidence).

## 0. Design Decisions (resolves OQ1–OQ5)

Each resolution is grounded in existing code. **Veto any of these before `/sc:tasklist`.**

| # | Open question | Decision | Grounding |
|---|---------------|----------|-----------|
| **DD-1** | Resume cursor: derive vs. new breadcrumb | **Derive-only. No new state file.** Recovery rests on **two** on-disk signals, not the ledger alone: (a) `results/phase-N-result.json`, written **atomically** via tmp+rename (`executor.py:2070-2072`) so a crash never truncates it; (b) the `execution-log.jsonl` ledger (`phase_start` at phase entry — `executor.py:1267` per-task, and just after subprocess spawn at `:1335` single-process — closed by `phase_complete` `logging_.py:89-107` or `phase_interrupt` `logging_.py:71-87`@`executor.py:1488`). NOTE the ledger append (`logging_.py:265-267`) is non-atomic/non-durable (no fsync/rename), so a hard crash MAY torn or drop the last line; the planner therefore treats **result.json presence as the authoritative phase-completion signal** and the ledger as corroboration. A breadcrumb file is unnecessary because result.json already provides the atomic anchor. R2 downgrades to "known phase (from result.json), unknown intra-phase progress" — handled by the integrity gate. | `logging_.py:59-107,265-267`, `executor.py:1267,1335,1488,2070-2072` |
| **DD-2** | "Doubly validated" definition | **Deterministic-only gate verdict, plus an advisory Haiku coherence read.** Signal A = persisted `task_results[].status` in `phase-N-result.json`. Signal B = independent re-derivation: `_classify_transcript()` over the task transcript **AND** checkpoint/deliverable file existence (`_verify_checkpoints` logic). Deterministic reconciliation alone sets `validated_last`/`passed`. **Scoped only to `granularity==TASK`** (a per-task last-completed object with a non-empty transcript + declared deliverables exists — see the §0 note below), a cheap Haiku agent then performs an **advisory** coherence read of that task: if it flags incoherence it appends a `coherence_warning` to the report and lists the task for operator review, but it **never** flips `validated_last`/`passed` (NFR-3). When `granularity==PHASE` (single-process path, empty `task_results[]`), the Haiku read is **skipped** and the deterministic checkpoint/deliverable existence checks carry the gate. Disagreement in the **deterministic** layer ⇒ suspect ⇒ gate STOP/quarantine. | `rerun_tasks.py:550-598`, `executor.py:1264-1307` (per-task) vs `1309+` (single-process), `executor.py:1844`, `checkpoints.py`, `summarizer.py:305` (advisory Haiku) |
| **DD-3** | Cleanup mechanism | **Report-only by default; opt-in copy-to-quarantine, never rename-in-place, never delete.** Default gate behavior is detect + print suspect paths + STOP (honors NFR-1 literally; the STOP already forces the operator decision FR-2.4 requires). When the operator opts into cleanup, COPY (`shutil.copy2`) suspect artifacts into `<results>/.resume-quarantine-<ts>/` with a `manifest.json` of the SAME shape `stash_and_restore_deliverables` writes (`rerun_tasks.py:961-1036`), so the EXISTING `restore_from_bundle` (`rerun_tasks.py:1039`) reverses it — no new restore verb. Reuse only `write_recovery_audit_log` (`recovery.py:250`, append a `resume_quarantine` line). Do NOT reuse the `.failed-<ts>` rename: it is inlined inside `merge_recovery_bundle` (not a callable helper), is bundle-scoped via `artifacts_replaced`, is NOT reversed by `rerun-tasks --restore`, and would race/duplicate the rerun engine's own stash on the TASK path. Acquire `.recovery-locks/phase-{phase}.lock` (`recovery.py:275`) before any results/ mutation. Not git-stash: per-task transcripts are gitignored (`.gitignore:230`) and the working tree may hold unrelated changes. | `recovery.py:250`, `rerun_tasks.py:961-1081`, `.recovery-locks` `recovery.py:275` |
| **DD-4** | Drift assessment algorithm | **Deterministic tiered scoring**, LLM optional explainer. Tier 0: per-phase normalized-content hash equal (`_content_sha256_excluding_rerun_block(phase_obj.file)`, same function on both stored and current side) ⇒ 1.0 — **exact-match only, NOT whitespace-tolerant**. Tier 1 delivers AC-4: a whitespace-insensitive comparator (`git diff --ignore-all-space` when tracked, else normalize-then-rehash) classifies trailing/format/comment-only deltas in completed `phase_obj.file` regions ⇒ ≥0.8; structural diff composes `parse_tasklist` (task IDs) + `extract_checkpoint_paths` (checkpoint paths), with deliverable-path diff best-effort over `description`; identifier/checkpoint/deliverable changes ⇒ <0.8. Tier 2: `git diff` annotation when tracked+online (skip gracefully on detached-HEAD / no upstream). Only the 0.8 value gates; other confidences are advisory. | `rerun_tasks.py:688-701,1306,1387`; `config.py:405`; `checkpoints.py:40` |
| **DD-5** | Opt-out flag name | **`--fresh` canonical, `--restart` alias.** Defined as "ignore prior on-disk state; run from phase 1 with auto-detect disabled." Explicit `--start/--end` (run) and `--phase/--tasks` (rerun-tasks) remain the *positional* bypass — detected via Click `ParameterSource.COMMANDLINE` (run() takes `@click.pass_context`) or a `None` sentinel default, **never** by value comparison such as `start_phase != 1` (an explicit `--start 1` must still bypass auto-resume; FR-4.4/AC-7). Avoid `--no-resume` as canonical (Click would imply a `--resume` toggle that doesn't fit a default-on feature). | new flag |

## 1. Component Overview

Three new **read-first** modules in `src/superclaude/cli/sprint/`, wired into the two CLI
entrypoints. Nothing about phase execution itself changes (NG1).

```
resume/
  planner.py        # ResumePlanner  → ResumePlan          (FR-1)
  integrity.py      # BoundaryIntegrityGate → BoundaryReport (FR-2)
  drift.py          # DriftAssessor → DriftAssessment       (FR-3)
  models.py         # ResumePlan, BoundaryReport, DriftAssessment, ResumeDecision dataclasses
```

Wiring points (existing): `cli/sprint/commands.py::run()` and `::rerun_tasks()`.

## 2. Data Structures

```python
# resume/models.py
class Granularity(Enum):
    TASK = "task"        # boundary phase has clean per-task data → rerun-tasks engine
    PHASE = "phase"      # no per-task data (hard crash) → executor loop re-runs phase
    NONE = "none"        # nothing to resume / fresh

@dataclass
class BoundaryTask:
    task_id: str
    persisted_status: TaskStatus | None        # Signal A (from phase-N-result.json)
    derived_status: TaskStatus | None          # Signal B (from _classify_transcript)
    artifacts_present: bool                     # declared deliverables/checkpoints exist
    role: str                                   # "last_completed" | "next_unfinished" | "pending"
    suspect: bool                               # A/B disagree OR artifacts missing
    phase: int | None = None                    # owning phase; None ⇒ interrupted phase. Set to a PRIOR phase for the hard-crash prior-tail last_completed so integrity resolves phase-{phase}-... (F-4/CG-3)

@dataclass
class ResumePlan:
    index_path: Path
    release_dir: Path
    completed_phases: list[int]
    interrupted_phase: int | None               # dangling phase_start, or first non-complete
    interrupt_kind: str                         # "complete" | "interrupt" | "crash" | "none"
    start_phase: int
    end_phase: int
    granularity: Granularity
    boundary_tasks: list[BoundaryTask]          # only for the interrupted phase
    rerun_task_ids: list[str]                   # task-level dispatch set (granularity=TASK)
    ambiguous: bool                             # FR-5 → list + STOP
    ambiguity_reasons: list[str]

@dataclass
class DriftAssessment:
    confidence: float                           # [0,1] safety-of-resume
    tier: str                                   # "hash" | "structural" | "git"
    changed_paths: list[str]
    explanation: str                            # FR-3.5 (why score is what it is)
    cosmetic_only: bool

@dataclass
class BoundaryReport:
    validated_last: bool
    suspects: list[BoundaryTask]
    quarantined: dict[Path, Path]               # canonical → quarantine copy
    passed: bool                                # gate verdict (FR-2.4) — deterministic only
    blocking_reasons: list[str]
    coherence_warnings: list[tuple[BoundaryTask, str]]  # advisory Haiku flags; NOT part of `passed` (NFR-3)
    partial_paths: list[Path] = field(default_factory=list)  # report-only suspect paths (FR-2.2 / §4(b) "always"); populated regardless of cleanup_opted_in (F-2/CG-1)
```

**Persisted `phase-N-result.json` hash fields (F-3/CG-2).** The result.json written by
`_write_phase_result_json` (`executor.py:2053-2095`, payload dict `:2079-2090`,
`tasklist_sha256` at `:2087` and `tasklist_sha256_ws` at `:2089`) carries two content-hash
fields the DriftAssessor reads on resume:

- `tasklist_sha256` — exact normalized-content hash (rerun-block stripped, NOT whitespace-tolerant);
  drives Tier-0 exact match (1.0). INV-001: produced by the SAME function over the SAME per-phase
  file the DriftAssessor hashes on the current side.
- `tasklist_sha256_ws` — **whitespace-normalized** hash of the same block-stripped content (F-3/CG-2);
  used by Tier 1 to prove a same-ID change after a Tier-0 miss is whitespace-only (keep 0.9 cosmetic,
  AC-4) versus material (<0.8 STOP, AC-5). **Backward-compatible:** a result.json lacking this field
  (pre-F-3) ⇒ drift's conservative <0.8 fallback. See §5 DD-4 amendment.

## 3. ResumePlanner (FR-1)

**Input:** `index_path`. **Effect:** pure read; no writes. **Output:** `ResumePlan`.

```
plan(index_path) -> ResumePlan:
  release_dir = _resolve_release_dir(index_path)            # config.py (existing)
  phases      = discover_phases(index_path)                  # config.py (existing)
  jsonl       = release_dir / "execution-log.jsonl"          # models.py:543 (ROOT, not results/)
  results_dir = release_dir / "results"                      # models.py:539

  events = read_jsonl(jsonl)                                 # tolerant: skip malformed lines
  # 1. classify each phase from the balanced ledger (DD-1)
  for each phase p:
     starts   = events where event==phase_start  and phase==p
     closed   = events where event in {phase_complete, phase_interrupt} and phase==p
     if results_dir/phase-p-result.json exists with PASS-family status → COMPLETED  (phase_complete event is corroboration, NOT required — a torn/dropped phase_complete line must not demote a phase whose atomic result.json proves completion)
     elif phase_start without any close                                   → CRASH (interrupted_phase=p)
     elif phase_interrupt                                                 → INTERRUPT (interrupted_phase=p)
     elif phase-p-result.json non-passing                                → INTERRUPT (recoverable)
     else                                                                 → PENDING

  interrupted_phase = lowest non-COMPLETED phase with any start/result, else None
  if interrupted_phase is None and all phases COMPLETED → granularity=NONE (nothing-to-resume)   # FR-1.6/AC-6
  if no phase ever started                              → fresh start_phase=1                     # FR-1.6
  start_phase = interrupted_phase ; end_phase = max(phase numbers) unless overridden            # FR-1.3

  # 2. boundary disposition for interrupted_phase (FR-1.4)
  rj = load(results_dir/phase-{interrupted}-result.json)    # schema: executor.py:2079-2090
  if rj and rj.task_results:                                # per-task data present
       granularity = TASK
       for tr in rj.task_results: build BoundaryTask(persisted_status=tr.status, ...)
       rerun_task_ids = [t.id for t in boundary_tasks if t.persisted_status != PASS]
  else:                                                     # hard crash / pre-v4.3.0
       derived = discover_failed_tasks_from_transcripts(results_dir, interrupted)   # rerun_tasks.py:601
       granularity = TASK if derived else PHASE
       rerun_task_ids = [tid for tid,_ in derived]
  mark last_completed (highest-index PASS) and next_unfinished (first non-PASS) roles            # user req

  # 3. ambiguity (FR-5): >1 release dir candidate, conflicting ledger, or unreadable core files
  if ambiguous: set ambiguous=True, ambiguity_reasons=[...]
```

**Reused symbols:** `_resolve_release_dir`, `discover_phases` (config.py);
`discover_failed_tasks_from_transcripts`, `_classify_transcript` (rerun_tasks.py:601,550);
`phase_result_json` path (models.py:570); result JSON schema (executor.py:2053-2095).

## 4. BoundaryIntegrityGate (FR-2)

Runs **after** the planner, **before** dispatch. Read-only until it decides to quarantine.

```
run(plan) -> BoundaryReport:
  # (a) doubly-validate last completed task (DD-2, FR-2.1)
  # F-4/CG-3 + AC-3 (merged-requirements.md:141-143): the last_completed may be the
  # PRIOR completed phase's tail when granularity==PHASE (hard crash, interrupted phase
  # has no per-task boundary). The planner emits that prior-tail BoundaryTask with a
  # `phase` field (the prior phase number); the gate resolves signalB's transcript AND
  # the declared deliverables under `lc.phase` (phase-{lc.phase}-...), NOT the interrupted
  # phase — else the prior tail's transcript/deliverables read from the wrong phase and
  # the check is vacuously True. `lc.phase is None` ⇒ interrupted phase (backward-compat).
  lc = plan.boundary_tasks.role==last_completed                          # may be prior-phase tail (PHASE hard crash)
  lc_phase = lc.phase if lc.phase is not None else plan.interrupted_phase
  signalA = lc.persisted_status
  signalB = _classify_transcript(read(task_output_file(lc_phase, lc.id)))   # rerun_tasks.py:550
  artifacts_ok = all declared checkpoint/deliverable paths for lc exist (resolved under lc_phase's tasklist)
  validated_last = (signalA==PASS and signalB==PASS and artifacts_ok)
  if not validated_last: suspects += [lc]   # over-claim caught (R1)
  # AC-3 :141-143 realized: on a PHASE-granularity hard crash (no last_completed in the
  # interrupted phase) the planner reaches into the HIGHEST completed phase and emits ITS
  # tail as `last_completed`, so this block double-validates the prior phase's tail BEFORE
  # the phase re-run — no longer vacuously True (DD-2 is no longer "Vacuously True on hard
  # crash"; it is vacuous ONLY when there is no completed phase below the interrupted one).
  # DD-2 ADVISORY Haiku coherence read — scoped to granularity==TASK, NEVER changes the verdict.
  # Skipped entirely for granularity==PHASE (no per-task last-completed object: executor.py:1309+).
  if validated_last and plan.granularity == Granularity.TASK \
          and lc is not None and transcript_nonempty(lc) and lc_declared_deliverables:
      verdict = haiku_coherence_read(lc, truncate(transcript), declared_artifacts)  # bounded ~1 call; "" on failure
      if verdict.suspect:
          coherence_warnings += [(lc, verdict.reason)]   # ADVISORY: annotate report + operator review
          # NOTE: validated_last / passed are NOT modified here (NFR-3, §8).

  # (b) next-unfinished partial-work detection + opt-in quarantine (DD-3, FR-2.2 / FR-2.3)
  nu = plan.boundary_tasks.role==next_unfinished  (or whole-phase set when granularity=PHASE)
  # Cover BOTH file classes: transcript (phase-N-task-<id>-output.txt) AND declared
  # deliverables (_declared_deliverables, rerun_tasks.py:924) — a never-started task has
  # no transcript, so transcript-only detection misses half-written deliverables.
  partial = (transcript exists and derived_status in {INCOMPLETE, FAIL_*})
            or any declared-deliverable path for nu exists on disk
            or stray phase-N-task-<id>-* output files exist
  if partial:
      report suspect paths in BoundaryReport.partial_paths (always, regardless of   # FR-2.2 surface; F-2/CG-1
        cleanup_opted_in); quarantined additionally holds the copy mapping when cleanup is opted-in
      if cleanup_opted_in:                                                # default: report-only
          acquire .recovery-locks/phase-{phase}.lock                      # recovery.py:275
          qdir = results_dir/(".resume-quarantine-" + ts)
          copy suspect paths → qdir preserving structure; write qdir/manifest.json
                                                                          # same shape as rerun_tasks.py:961
          append recovery-audit.log {event:"resume_quarantine", task, manifest: qdir/manifest.json}
          quarantined[canonical] = qdir-copy                              # reversible via restore_from_bundle
      # NOTE: on granularity==TASK the dispatched run_rerun_tasks ALREADY stashes these via
      # stash_and_restore_deliverables — the gate must NOT also rename them (glob collision).

  # (c) gate verdict (FR-2.4 — hard gate). PURE function of deterministic signals; Haiku
  # coherence_warnings are surfaced in print_plan for the operator but are NOT in `passed` (NFR-3).
  # CG-4 RULING (YES, operator Ryan W 2026-06-02): §7 governs the non-interactive path. The partial
  # conjunct is "(partial reported AND (quarantined OR --yes/assented))" — on the report-only path the
  # partial work is REPORTED (its paths surfaced in BoundaryReport.partial_paths, F-2/CG-1) and a
  # standing --yes / interactive assent counts as "accepted", so re-running the boundary task is the
  # disposition. This reconciles §4(c) with §7:293 (which the implementation already followed). The
  # informedness prerequisite is F-2 (partial paths must be printed), which has LANDED.
  passed = validated_last and (no unresolved suspects) and (partial reported AND (quarantined OR --yes/assented))
  if not passed: blocking_reasons explain exactly what must be resolved → caller STOPs
  # coherence_warnings (advisory) are reported regardless of `passed`; an empty Haiku verdict
  # (claude absent / timed out) yields a BoundaryReport identical to the no-Haiku path (CI-safe).
```

**Non-destructive guarantee (NFR-1, DD-3):** by default the gate performs NO results/
mutation — it detects, prints, and STOPs. When cleanup is opted into, the only mutations are
a `shutil.copy2` into `<results>/.resume-quarantine-<ts>/` (the canonical original is left
untouched) plus a `recovery-audit.log` append, both under `.recovery-locks/phase-{phase}.lock`.
Because the quarantine dir reuses the `preserved/`+`manifest.json` shape, the EXISTING
`restore_from_bundle` (`rerun_tasks.py:1039`) reverses it as-is — no new `sprint resume
--restore` verb is required (and none exists today).

## 5. DriftAssessor (FR-3)

```
assess(index_path, plan) -> DriftAssessment:
  phase_file  = plan boundary phase's phase_obj.file        # per-phase, NOT index_path
  current_sha = _content_sha256_excluding_rerun_block(phase_file)        # rerun_tasks.py:688
  recorded_sha = tasklist_sha256 stored in phase-N-result.json for that phase  # DD-4 note below
               # MUST be produced by the SAME function (_content_sha256_excluding_rerun_block)
               # over the SAME file, or Tier 0 can never match (invariant INV-001).
  # Tier 0 — exact normalized-hash match only (block stripped; NOT whitespace-tolerant).
  if recorded_sha and current_sha == recorded_sha: return Drift(confidence=1.0, tier="hash", cosmetic_only=True)
  # AC-4 (trailing whitespace) is handled in Tier 1, not here.
  # Tier 1 — structural diff limited to COMPLETED-phase regions
  cosmetic = (recorded tasklist_sha256_ws == current whitespace-normalized hash)     # AC-4 path; F-3/CG-2
  changed  = structural_diff(parse_tasklist(phase_file)+extract_checkpoint_paths(phase_file),
                             recorded_completed_task_ids/checkpoints)                 # deliverables best-effort
  if changed touches completed task IDs / checkpoints / deliverables: confidence≈0.3   # AC-5 (ID removal)
  elif changes only in not-yet-run phases:                confidence≈0.85
  # Same-ID fall-through after a Tier-0 MISS (content provably changed):  F-3/CG-2
  elif cosmetic:                                          confidence≈0.9  (≥0.8 ⇒ AC-4 passes; WS hashes match)
  else:                                                   confidence <0.8 (AC-5 STOP; same-ID material edit OR
                                                          no recorded tasklist_sha256_ws ⇒ cannot prove cosmetic)
  # Tier 2 — git characterization when tracked+online
  if git_available: annotate changed_paths with `git diff @{upstream}` summary
  return Drift(confidence, tier, changed_paths, explanation)
```

**DD-4 storage note:** today `source_tasklist_sha256` is only persisted inside a
`RecoveryBundle` after a rerun (`recovery.py:111`). For fresh-run drift detection we need a
baseline hash captured at **each phase_complete**. Minimal addition: write
`tasklist_sha256 = _content_sha256_excluding_rerun_block(phase_obj.file)` into
`phase-N-result.json` (extend `_write_phase_result_json`, `executor.py:2053-2095`, payload dict
`:2079-2090`) — one field, backward-compatible (absent ⇒ Tier-1/2 only, no Tier-0 shortcut).
**The stored hash MUST use `_content_sha256_excluding_rerun_block` over the per-phase
`phase_obj.file`** — the identical function/file the DriftAssessor uses on the current side, or
Tier 0 can never match (INV-001). Pre-v4.3.5 phases carry no stored hash, so their first
post-upgrade resume skips Tier 0 by design. This is the **only change to the write path** in the
whole feature.

**DD-4 amendment (F-3/CG-2) — second persisted hash `tasklist_sha256_ws`.** Alongside
`tasklist_sha256`, `_write_phase_result_json` ALSO persists `tasklist_sha256_ws` — a
**whitespace-normalized** hash of the same block-stripped content
(`_content_sha256_ws_excluding_rerun_block`, which collapses intra-line whitespace runs, strips
per-line leading/trailing whitespace, and drops trailing blank lines before hashing). It differs
from `tasklist_sha256` ONLY in whitespace tolerance. The DriftAssessor uses it to resolve the
same-ID fall-through after a Tier-0 MISS: the change is deemed **cosmetic (keep 0.9, AC-4)** ONLY
when the recorded `tasklist_sha256_ws` exists AND equals the current whitespace-normalized hash;
otherwise — a same-ID body/checkpoint/deliverable edit (AC-5/F-3) OR a recorded baseline lacking
the field (pre-F-3 result.json) — it scores **<0.8 (STOP)** with `cosmetic_only=False`. This keeps
the gate fully deterministic (Tier-0/1 only, never git — NFR-3) and backward-compatible (absence ⇒
conservative <0.8 fallback, never a crash).

## 6. CLI Wiring & Control Flow

```
# commands.py::run(index_path, start_phase, end_phase, ..., fresh)
# explicit-window detection MUST use Click parameter source, NOT value comparison:
# `--start 1` is a valid EXPLICIT window and must NOT be misread as "no flag" (FR-4.4/AC-7).
# `run()` therefore takes @click.pass_context; the value-comparison form is a known bug
# because `--start` default=1 (commands.py:78) makes `start_phase != 1` indistinguishable
# from an explicit `--start 1`.
src = ctx.get_parameter_source
position_explicit = src("start_phase") == ParameterSource.COMMANDLINE \
                 or src("end_phase")   == ParameterSource.COMMANDLINE   # user supplied a window
# Alt (no ctx): set --start/--end default=None (mirrors rerun-tasks --phase/--tasks),
# detect `is not None`, then map None→(1, last) at the load_sprint_config boundary.
if fresh:           → clean run from phase 1, auto-detect OFF (DD-5)
elif position_explicit:  → TODAY's exact path, auto-detect OFF (FR-4.4 / AC-7)
else:                    → AUTO-RESUME:
    plan  = ResumePlanner().plan(index_path)
    if plan.granularity == NONE:   print "nothing to resume"; exit 0           # AC-6
    if plan.ambiguous:             print candidates; STOP (exit non-zero)      # FR-5 / AC-8
    drift = DriftAssessor().assess(index_path, plan)
    report= BoundaryIntegrityGate().run(plan)
    print_plan(plan, drift, report)                                            # FR-4.2 (detect→print)
    if not report.passed:          STOP with blocking_reasons                  # FR-2.4
    if drift.confidence < 0.8:     STOP → guide to --start/--fresh             # FR-3.4 / AC-5
    else:                          prompt_user(unless --yes/CI env); proceed   # FR-3.4 / NFR-4
    dispatch(plan)

dispatch(plan):
    if plan.granularity == TASK:   run_rerun_tasks(index_path, phase=plan.interrupted_phase,
                                                   tasks=plan.rerun_task_ids, merge_back=True)  # AC-2
    else:                          config.start_phase=plan.start_phase; config.end_phase=plan.end_phase
                                   execute_sprint(config)   # existing active_phases loop (executor.py:1239)
```

`rerun_tasks()` gets the symmetric treatment (FR-4.1 / AC-9): when
`--phase`/`--tasks`/`--from-reflect-report` are all absent, call the planner, take
`interrupted_phase` + `rerun_task_ids`, and proceed as if specified.

### New flags (both subcommands)
| Flag | Type | Meaning |
|------|------|---------|
| `--fresh` / `--restart` | bool | Ignore prior state; clean run from phase 1; auto-detect OFF (DD-5) |
| `--yes` | bool | Non-interactive assent for the ≥0.8 drift prompt (NFR-4 / CI) |
| `--dry-run` (run: extend existing) | bool | Print `ResumePlan` + `BoundaryReport` + `DriftAssessment`, no execution (FR-4.5) |

`--yes` also honored via env (e.g. `SUPERCLAUDE_SPRINT_ASSUME_YES=1`) for unattended CI.

## 7. Sequence (happy path, AC-1/AC-2)

```
user: superclaude sprint run index.md
 └─ run(): no explicit position, no --fresh
     ├─ ResumePlanner.plan → {completed:[1,2], interrupted:3, kind:interrupt,
     │                         granularity:TASK, rerun_task_ids:[T03.4]}
     ├─ DriftAssessor.assess → {confidence:1.0, tier:hash}            (no edits since run)
     ├─ BoundaryIntegrityGate.run → validate T03.3 (last PASS, artifacts ok) ✓;
     │     report half-written T03.4 outputs (copy→.resume-quarantine-<ts>/ if opted in); passed=True
     ├─ print_plan(...)  "Resuming phase 3 · phases 1-2 complete · re-running T03.4 · drift 1.0"
     ├─ prompt (skipped: --yes / interactive assent)
     └─ dispatch → run_rerun_tasks(phase=3, tasks=[T03.4]) → merge_back refreshes result.json
```

## 8. Module Interfaces (signatures)

```python
# resume/planner.py
class ResumePlanner:
    def plan(self, index_path: Path, *, end_override: int | None = None) -> ResumePlan: ...

# resume/integrity.py
class BoundaryIntegrityGate:
    def run(self, plan: ResumePlan, *, accept_suspect: bool = False) -> BoundaryReport: ...

# resume/drift.py
class DriftAssessor:
    def assess(self, index_path: Path, plan: ResumePlan) -> DriftAssessment: ...

# commands.py (internal helper)
def _auto_resume(index_path, *, assume_yes: bool, dry_run: bool) -> ResumeDecision: ...
```

All three classes are pure w.r.t. canonical results except the gate's opt-in quarantine COPY
(audit-logged; report-only by default). Deterministic cores; the two isolated LLM hooks are
(1) the gate's **advisory** Haiku coherence read on the last-completed task (DD-2, TASK-granularity
only) and (2) `DriftAssessor`'s explanation tier — both advisory, neither can change a
deterministic verdict (NFR-3).

## 9. Test Plan (maps 1:1 to acceptance criteria)

| Test | AC | Fixture |
|------|----|---------|
| `test_resume_planner_phase_boundary` | AC-1 | result.json for P1,P2; P3 dangling `phase_start` |
| `test_resume_task_level_recoverable` | AC-2 | P3 result.json with one `fail_recoverable` task |
| `test_resume_hard_crash_phase_level` | AC-3 | P3 `phase_start`, no result.json, partial transcripts |
| `test_drift_trailing_whitespace_high_conf` | AC-4 | tasklist + " " appended; assert confidence ≥0.8 |
| `test_drift_material_edit_low_conf` | AC-5 | completed-phase task body edited; assert <0.8, STOP |
| `test_nothing_to_resume` | AC-6 | all phases result.json PASS |
| `test_explicit_start_bypasses_autodetect` | AC-7 | `--start 4`; assert planner not called |
| `test_ambiguous_release_dirs_stop` | AC-8 | two candidate release dirs |
| `test_rerun_tasks_autodetect_parity` | AC-9 | bare rerun-tasks == explicit `--phase --tasks` |
| `test_boundary_quarantine_nondestructive` | FR-2.5 | default: report-only, NO results/ mutation. Opt-in cleanup: assert copy exists under `.resume-quarantine-<ts>/` with manifest, ORIGINAL untouched, audit line written, `.recovery-locks` taken |
| `test_haiku_coherence_advisory_only` | DD-2 | (a) mock Haiku verdict=suspect on a deterministically-validated TASK ⇒ `coherence_warnings` populated but `passed`/`validated_last` UNCHANGED; (b) `granularity==PHASE` or empty transcript ⇒ Haiku NOT invoked; (c) claude absent (empty verdict) ⇒ `BoundaryReport` identical to the no-Haiku path |
| e2e over real-subprocess harness | AC-1/2/3 | reuse `344a754a` harness |

## 10. Implementation Phasing

1. **P1 — `resume/models.py` + `ResumePlanner`** (read-only; unblocks everything). Add
   `tasklist_sha256` to `_write_phase_result_json` (DD-4, the one write-path change).
2. **P2 — `DriftAssessor`** (deterministic tiers 0/1; git tier behind capability check).
3. **P3 — `BoundaryIntegrityGate`** (reuses recovery preserve/audit).
4. **P4 — CLI wiring** in `run()` + `rerun_tasks()`, new flags, `--dry-run` extension.
5. **P5 — tests** (table §9) + docs/changelog (R5 behavior-change note).

## 11. Evidence (re-verified 2026-06-02, this session)

- Balanced ledger: `logging_.py:59-107` (`phase_start`/`phase_interrupt`/`phase_complete`),
  callers `executor.py:1267,1335,1488`.
- Paths: `execution-log.jsonl` at release root (`models.py:543`); `results/` (`:539`);
  `phase-N-result.json` (`:570`); task transcripts (`:561-565`).
- Result JSON schema + writer: `executor.py:2053-2095`.
- Classifiers: `_classify_transcript` (`rerun_tasks.py:550`),
  `discover_failed_tasks_from_transcripts` (`:601`).
- Normalized hash: `_content_sha256_excluding_rerun_block` (`rerun_tasks.py:688`).
- Quarantine/audit pattern: `recovery.py:445-492`; `RecoveryStatus`/`RecoveryBundle` (`:58,77`).
- Status vocab: `TaskStatus` (`models.py:45-52`), `PhaseStatus` (`:270`).
- Executor loop + window: `active_phases` (`models.py:550`), loop (`executor.py:1239`).

## 12. Updated Risk Posture
- R2 (crash blind spot) **largely closed** by DD-1 — phase identity is recovered from the
  atomically-written result.json (executor.py:2070-2072), NOT from the non-durable ledger
  append (logging_.py:265-267 has no fsync/rename, so the last phase_start may be torn/dropped
  on hard crash). Only intra-phase progress is unknown, which the gate handles. Residual
  concurrency caveat: `_resolve_release_dir` (config.py:242) is deterministic from index_path
  with no lock, so concurrent `sprint run <same index>` share one ledger; the planner's
  event-pairing must tolerate interleaved phase_start events or FR-5 must flag it as ambiguous.
- R1/R3 mitigated by deterministic-first DD-2/DD-4; LLM is advisory (coherence read / explainer), never on the gate-verdict path.
- New micro-risk: the single write-path change (DD-4 `tasklist_sha256`) must stay
  backward-compatible — absent field ⇒ planner falls back to Tier-1/2 drift, never crashes.
- DD-3 reuse-surface corrected: the `.failed-<ts>` rename is NOT a reusable helper and is NOT
  reversed by any existing `--restore`; the gate instead reuses `write_recovery_audit_log`
  + the `preserved/`-shaped COPY quarantine that `restore_from_bundle` already reverses, and
  takes `.recovery-locks` before mutating results/.

## 13. Next Step
Decisions DD-1..DD-5 are code-grounded and ready. On approval:
`/sc:tasklist @.dev/brainstorms/20260602-sprint-auto-resume-default/design.md` for a v4.3.5
sprint bundle, then `/sc:implement` per the §10 phasing.
