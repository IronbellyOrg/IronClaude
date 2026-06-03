---
dd: DD-2
verdict: REFACTOR
confidence: 0.82
---

## Adversarial findings

DD-2's deterministic-first core is sound and well-grounded. The defect is the LLM
placement: as written, the Haiku sign-off **alters the gate verdict** (downgrade flips
`validated_last=False` → `suspects` → gate STOP), and the whole "doubly-validate the
last-completed task" premise rests on an assumption that is **false for one of the two
phase-execution paths**. Three findings, two of them HIGH severity:

1. **The "last-completed task" object does not always exist (INV-001, HIGH).** The
   executor has two phase paths. The per-task path writes per-task transcripts and a
   populated `task_results[]`; the single-process path writes one whole-phase output
   file and an empty `task_results[]`. When the resume boundary's predecessor phase ran
   single-process, there is *no per-task last-completed object* — only a phase-level
   PASS. Signal B (`_classify_transcript` over `task_output_file(...)`) and the Haiku
   coherence call both silently degrade to judging a whole `phase-N-output.txt`, which
   is exactly the unbounded, ill-defined call DD-2 is supposed to avoid. **Fix: scope
   the Haiku read (and per-task Signal B) to `granularity==TASK` with a non-empty
   last-completed transcript + declared deliverables; skip for `granularity==PHASE`.**

2. **Haiku is not the gate's trust anchor — it covers a narrow residual (INV-003, HIGH).**
   A wrong-*target* deliverable is already caught deterministically by the
   `artifacts_ok` existence check; an empty/truncated transcript is already classified
   `INCOMPLETE` by `_classify_transcript` (no terminal result event, or zero output
   tokens) → deterministic suspect. The *only* slice Haiku uniquely detects is
   "declared file exists, is non-empty, transcript shows a clean result, but the content
   is semantically wrong for the task." That is real (R1) but narrow — so the LLM should
   be an **advisory** catch for that slice, not the verdict-setter.

3. **Putting the verdict on the LLM path contradicts the design's own NFR-3 prose.**
   §8 and §12 assert the LLM hooks are "advisory, neither can upgrade a deterministic
   verdict (NFR-3)." But §0/§4(a) have the downgrade flip `validated_last` and feed the
   `passed` boolean — that *is* changing the verdict (conservatively). The design
   conflates "can't upgrade" with "advisory." Reproducibility cost is real: identical
   on-disk state can pass once and STOP next time because Haiku is non-deterministic and
   model-version-dependent; CI without `claude` on PATH gets an ambiguous empty verdict.
   **Fix: `passed` is a pure function of the deterministic signals; Haiku annotates the
   report and is surfaced to the operator, but never flips `validated_last`/`passed`.
   In advisory mode an empty Haiku verdict (claude absent) yields a gate identical to the
   no-Haiku path — CI ambiguity dissolves.**

Probe answers: (a) **Transcript availability** — YES for the per-task path (transcripts
persist in `results/`, not deleted; globbed at `rerun_tasks.py:616`); NO per-task
transcript for the single-process path (the load-bearing gap, finding 1). (b) **Is one
bounded call enough?** — for the narrow residual slice, yes, but only with input
truncation discipline (transcripts can be tens of KB). (c) **Downgrade-only loop / blocked
resume?** — NO infinite loop: the gate runs once per invocation, STOP exits non-zero, and
design §6 has no auto-retry around it (A-002 retired). The real risk is not a loop but
spurious STOPs on legitimate resumes, which advisory mode removes. (d) **Cost/latency** —
~1 call, 30s timeout ceiling, `""` on failure; negligible vs a phase re-run, but it adds a
`claude`-on-PATH dependency to the gate that advisory mode neutralizes. (e) **Determinism**
— the core concern; resolved by making the LLM non-gating.

Not REJECT: the coherence read covers a genuine R1 slice and `invoke_sonnet`
(summarizer.py) makes it cheap and precedented. Not UPHOLD: as written it is on the wrong
side of NFR-3 and rests on the contradicted per-task assumption.

## Code verification (file:line)

- **Two phase paths (the gap):** per-task path `executor.py:1264-1307` (calls
  `execute_phase_tasks`, writes `task_results`, persists JSON via `_write_phase_result_json`
  at `:1304`); single-process path begins `executor.py:1309+` (one phase output, no per-task
  transcripts). `task_output_file` vs `output_file`: `models.py:555-562`.
- **Signal B classifier:** `_classify_transcript` (`rerun_tasks.py:550-598`) is fully
  deterministic — parses the terminal `{"type":"result"}` event + summed `output_tokens`;
  returns `PASS` (not error, tokens>0), `FAIL_RECOVERABLE` (error + transient/zero-token),
  `FAIL_TERMINAL` (error), `INCOMPLETE` (no terminal result `:579-580`, or clean-but-zero-output
  `:597-598`). No LLM, no randomness.
- **Checkpoint/deliverable existence (reusable):** `checkpoints.py:40-116`
  (`extract_checkpoint_paths` + `verify_checkpoint_files`, `path.is_file()`); consumed by
  `_verify_checkpoints` (`executor.py:1844-1924`). Existence checking exists and is reusable
  for `artifacts_ok`.
- **Signal A per-task availability:** `TaskResult` (`models.py:165-182`, `status` field +
  `to_dict`), `TaskStatus` (`models.py:45-52`); persisted in `phase-N-result.json`
  `task_results[]` via `_write_phase_result_json` (`executor.py:2053-2072`). Path
  `phase_result_json` (`models.py:570-571`). Empty-`task_results` fallback documented at
  `rerun_tasks.py:604-612`, used by `discover_failed_tasks_from_transcripts` (`:601-640`,
  globs persisted transcripts at `:616`).
- **Haiku/LLM surface:** `invoke_sonnet` (`summarizer.py:305+`) shells
  `claude --print --model`, 30s timeout, returns `""` on any failure (never raises);
  Haiku already invoked per-phase (`executor.py:1173`) and in `retrospective.py`. A Haiku
  variant is trivially derivable; advisory-empty-on-failure is the existing contract.

## Proposed spec changes

EXACT existing design.md text to replace + EXACT replacement text (copy-pasteable):

### Change 1 — §0 DD-2 row (design.md:24)

REPLACE:
```
| **DD-2** | "Doubly validated" definition | **Deterministic-first, then a final Haiku LLM sign-off.** Signal A = persisted `task_results[].status` in `phase-N-result.json`. Signal B = independent re-derivation: `_classify_transcript()` over the task transcript **AND** checkpoint/deliverable file existence (`_verify_checkpoints` logic). Deterministic reconciliation decides validated/suspect first. **Then** a cheap Haiku agent runs a final coherence sign-off on the last-completed task: it may **downgrade** a deterministically-"validated" task to suspect (flag-only, never silent), but may **not upgrade** a deterministic suspect. Disagreement at either layer ⇒ suspect ⇒ gate STOP/quarantine. | `rerun_tasks.py:550-598`, `executor.py:1844`, `checkpoints.py` + Haiku agent |
```
WITH:
```
| **DD-2** | "Doubly validated" definition | **Deterministic-only gate verdict, plus an advisory Haiku coherence read.** Signal A = persisted `task_results[].status` in `phase-N-result.json`. Signal B = independent re-derivation: `_classify_transcript()` over the task transcript **AND** checkpoint/deliverable file existence (`_verify_checkpoints` logic). Deterministic reconciliation alone sets `validated_last`/`passed`. **Scoped only to `granularity==TASK`** (a per-task last-completed object with a non-empty transcript + declared deliverables exists — see the §0 note below), a cheap Haiku agent then performs an **advisory** coherence read of that task: if it flags incoherence it appends a `coherence_warning` to the report and lists the task for operator review, but it **never** flips `validated_last`/`passed` (NFR-3). When `granularity==PHASE` (single-process path, empty `task_results[]`), the Haiku read is **skipped** and the deterministic checkpoint/deliverable existence checks carry the gate. Disagreement in the **deterministic** layer ⇒ suspect ⇒ gate STOP/quarantine. | `rerun_tasks.py:550-598`, `executor.py:1264-1307` (per-task) vs `1309+` (single-process), `executor.py:1844`, `checkpoints.py`, `summarizer.py:305` (advisory Haiku) |
```

### Change 2 — §4(a) gate algorithm (design.md:154-157)

REPLACE:
```
  # DD-2 final sign-off: cheap Haiku coherence pass — DOWNGRADE-ONLY (never upgrades)
  if validated_last:
      verdict = haiku_signoff(lc, transcript, declared_artifacts)   # bounded, ~1 call
      if verdict.suspect: validated_last = False; suspects += [lc]   # flag, never silently pass
```
WITH:
```
  # DD-2 ADVISORY Haiku coherence read — scoped to granularity==TASK, NEVER changes the verdict.
  # Skipped entirely for granularity==PHASE (no per-task last-completed object: executor.py:1309+).
  if validated_last and plan.granularity == Granularity.TASK \
          and lc is not None and transcript_nonempty(lc) and lc_declared_deliverables:
      verdict = haiku_coherence_read(lc, truncate(transcript), declared_artifacts)  # bounded ~1 call; "" on failure
      if verdict.suspect:
          coherence_warnings += [(lc, verdict.reason)]   # ADVISORY: annotate report + operator review
          # NOTE: validated_last / passed are NOT modified here (NFR-3, §8).
```

### Change 3 — §4(c) gate verdict (design.md:167-169)

REPLACE:
```
  # (c) gate verdict (FR-2.4 — hard gate)
  passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)
  if not passed: blocking_reasons explain exactly what must be resolved → caller STOPs
```
WITH:
```
  # (c) gate verdict (FR-2.4 — hard gate). PURE function of deterministic signals; Haiku
  # coherence_warnings are surfaced in print_plan for the operator but are NOT in `passed` (NFR-3).
  passed = validated_last and (no unresolved suspects) and (partial work quarantined or accepted)
  if not passed: blocking_reasons explain exactly what must be resolved → caller STOPs
  # coherence_warnings (advisory) are reported regardless of `passed`; an empty Haiku verdict
  # (claude absent / timed out) yields a BoundaryReport identical to the no-Haiku path (CI-safe).
```

### Change 4 — §2 BoundaryReport dataclass (design.md:86-92)

REPLACE:
```
@dataclass
class BoundaryReport:
    validated_last: bool
    suspects: list[BoundaryTask]
    quarantined: dict[Path, Path]               # canonical → .failed-<ts>
    passed: bool                                # gate verdict (FR-2.4)
    blocking_reasons: list[str]
```
WITH:
```
@dataclass
class BoundaryReport:
    validated_last: bool
    suspects: list[BoundaryTask]
    quarantined: dict[Path, Path]               # canonical → .failed-<ts>
    passed: bool                                # gate verdict (FR-2.4) — deterministic only
    blocking_reasons: list[str]
    coherence_warnings: list[tuple[BoundaryTask, str]]  # advisory Haiku flags; NOT part of `passed` (NFR-3)
```

### Change 5 — §9 test row (design.md:294)

REPLACE:
```
| `test_haiku_signoff_downgrade_only` | DD-2 | mock Haiku verdict=suspect on a deterministically-validated task ⇒ downgraded; verdict=ok on a deterministic suspect ⇒ stays suspect (no upgrade) |
```
WITH:
```
| `test_haiku_coherence_advisory_only` | DD-2 | (a) mock Haiku verdict=suspect on a deterministically-validated TASK ⇒ `coherence_warnings` populated but `passed`/`validated_last` UNCHANGED; (b) `granularity==PHASE` or empty transcript ⇒ Haiku NOT invoked; (c) claude absent (empty verdict) ⇒ `BoundaryReport` identical to the no-Haiku path |
```
