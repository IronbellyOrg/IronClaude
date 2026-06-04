---
proposal_id: 03
persona: refactorer
model: haiku
stance: composability / unified-recovery-verb / API-cleanliness
created: 2026-06-01T00:00:00Z
---

# Proposal 03 — Refactorer / Composability: "Design the recovery surface, not just the patch"

## Stance

The codebase has TWO recovery primitives shipping (verify-checkpoints exists; rerun-tasks would be new) and a THIRD on the horizon (reflect-driven nomination, via SprintRunReflect). If we ship rerun-tasks as a third unrelated verb, the operator has to compose them by hand and we lose composability. Design the unified recovery surface NOW: a single `sprint repair` umbrella with sub-verbs, sharing a recovery-bundle data structure, with an event-stream contract that reflect-driven automation can hook into. Ship the minimum behind that surface in v1 (the operator gets a familiar `rerun-tasks`-shaped interaction), and the verb is positioned for v2 enrichment without breakage.

## T1 — Task extraction: C (MDTM template re-render)

Don't regex. Read the source tasklist's frontmatter + phase metadata, then read each task body, and re-render through a normalized MDTM template (the same one task-builder uses to CREATE tasks). The template engine guarantees output is well-formed. Renumber tasks: rerun phase becomes phase Nr where the tasks keep their original T-IDs (so logs and references stay portable) but the synthetic phase number distinguishes the bundle.

Rationale: regex parsing tolerates malformed input by accident. Template-rendering forces well-formedness. Cost is ~30 LOC if a template engine already exists for task-builder (verify); ~150 LOC if we have to vendor a minimal one (probably overkill).

**Fallback**: if no template engine exists in the codebase, fall to Proposal 02's "regex + round-trip parse" approach. The template path is the ideal; the round-trip is the pragmatic.

## T2 — Index construction: A (sub-index, same as P01/P02)

Agreement. The bundle is self-contained and ignorable.

## T3 — Dependency handling: C (transitive auto-include with cost ceiling)

When the operator says `--tasks T07.11,T07.12` and T07.11 declares `depends_on: [T07.05]` where T07.05 also failed (per persisted `task_results` or transcript inspection), automatically include T07.05 in the rerun. Print:
```
T07.05 added to rerun (transitive dep of T07.11). Total tasks: 3.
```

Cost ceiling: if transitive closure exceeds 50% of the original phase, abort with `"Transitive deps include <K> tasks (>50% of phase). Use 'sprint run --start N --end N' to rerun the whole phase, or pass --no-transitive to rerun exactly the named tasks."`.

Operator escape hatch: `--no-transitive` (degrade to Proposal 01's "leave deps as-is" behavior).

Rationale: the operator's mental model is "rerun the failed work." If a named task transitively depends on other failed work, the right behavior is to rerun the chain — that's what makes the named task likely to succeed. The cost ceiling protects against runaway expansion.

## T4 — Checkbox state: A with audit (uncheck-then-recheck + audit log)

Same as Proposal 02 (mutate source tasklist `[x]` → `[ ]` at rerun start; flip back on success). Additionally, every checkbox mutation writes a line to `<results_dir>/recovery-audit.log`:
```
2026-06-01T16:30:00Z UNCHECK phase=7 task=T07.11 bundle=rerun-20260601T163000 reason="rerun-tasks --tasks T07.11,T07.12"
2026-06-01T16:35:42Z CHECK phase=7 task=T07.11 bundle=rerun-20260601T163000 result=PASS
```

The audit log is shared across rerun-tasks, verify-checkpoints --recover, and (future) reflect-driven invocations. ANY recovery verb that mutates source state writes here.

Rationale: shared audit log is the composability primitive. Future "what's the recovery history of this sprint" tooling has one file to read.

## T5 — Results merge-back

Define a `RecoveryBundle` dataclass (in `models.py`) that ALL recovery verbs return:
```python
@dataclass
class RecoveryBundle:
    bundle_id: str             # rerun-<ts> or verify-recover-<ts>
    verb: str                  # "rerun-tasks" | "verify-checkpoints" | etc
    affected_phase: int
    affected_tasks: list[str]
    artifacts_produced: list[Path]
    artifacts_replaced: dict[Path, Path]  # canonical -> preserved
    sha_at_start: str
    sha_at_end: str | None
    status: RecoveryStatus     # SUCCESS | PARTIAL | FAILED | DRYRUN
```

Merge-back semantics work on this dataclass. The verb-specific code populates it; the merge engine is generic. New recovery verbs in v2 (e.g., reflect-driven auto-rerun) plug in by producing a `RecoveryBundle` and calling `merge_recovery_bundle(bundle, source_tasklist)`.

**Transcripts, checkpoint reports, execution-log events**: same as Proposal 02 (rename-with-`.failed-<ts>` suffix, append-only log, `superseded_by` link), but the merge engine handles them generically via the `RecoveryBundle.artifacts_replaced` dict.

Rationale: the merge logic should be written ONCE for all recovery verbs. Otherwise verify-checkpoints, rerun-tasks, and future reflect-rerun will each invent their own slightly-different merge semantics — exactly the bug we're trying to prevent.

## T6 — Per-task persistence: A (extend PhaseResult, same as Proposal 02)

Agreement with Proposal 02. Persisted `task_results` is the right primitive. Additionally, add a `recovery_history: list[RecoveryBundleRef]` field that tracks all recovery actions taken against the phase. Visible in `verify-checkpoints` output.

## T7 — /sc:reflect integration: B (`--from-reflect-report` flag, but via shared `nomination-source` abstraction)

`--from-reflect-report <path>` works as Proposal 02 specs. Additionally, abstract the nomination source: introduce `--nomination-source {reflect-report|manual|qa-failure}` so future T-ID nominators (rf-qa, manual editor, CI signals) plug in via the same mechanism.

In v1, only `reflect-report` (consumes deviation register) and `manual` (from `--tasks` flag) are implemented. The flag enum is forward-compatible.

Rationale: the operator-facing UX is `--tasks T07.11,T07.12` (manual nomination) or `--from-reflect-report <path>` (reflect nomination). Both internally resolve to "a list of T-IDs to rerun" via a shared nominator interface. v2 additions (rf-qa nominator, CI-failure nominator) reuse the same interface.

## T8 — Failure modes

- **Retry-of-retry**: hard limit 3 (same as Proposal 02), but the limit is tracked in `recovery_history` on the persisted `PhaseResult`, not in tasklist frontmatter. Cleaner separation of "data" (PhaseResult) from "human-readable structure" (tasklist).
- **Partial-deliverable preservation**: same as Proposal 02 (stash to `<bundle>/preserved/<relative-path>`), but the stashing is done by the generic merge engine via `RecoveryBundle.artifacts_replaced`. Both rerun-tasks AND verify-checkpoints get the preservation behavior for free.
- **Original tasklist edited mid-flight**: SHA256 check; mismatch aborts merge-back. `--force-merge` allowed with strong WARN.
- **Bundle collision**: auto-suffix with abort at `-9`.
- **Recovery during recovery**: detect via `rerun_in_progress` lock file at `<results_dir>/.recovery-locks/phase-N.lock`. If a recovery is already in progress for phase N (lock file exists with PID), ABORT with `"Recovery already in progress for phase 7 (PID 12345). Kill PID 12345 or remove lock file <path>."`. Lock auto-cleared on process exit.

Rationale: lock file prevents the operator from accidentally launching two reruns of the same phase in parallel — catastrophic with a shared merge-back step.

## T9 — Composition with verify-checkpoints: B (umbrella `sprint repair` verb)

THIS IS THE BIG ONE. Ship `sprint repair` as the umbrella with sub-verbs:
```
superclaude sprint repair tasks <index> --phase N --tasks T07.11,T07.12   # what we've been designing
superclaude sprint repair checkpoints <index> --phase N                    # alias for verify-checkpoints --recover
superclaude sprint repair auto <index> --phase N                          # runs both: tasks first, then checkpoints
superclaude sprint repair from-reflect <index> --report <path>            # reflect-driven recovery
```

Also keep `superclaude sprint verify-checkpoints` as the EXISTING verb (no breakage). `sprint repair checkpoints` is an alias.

Rationale: composability is the surface. Operators learn ONE verb (`sprint repair`) with sub-verbs, instead of having to remember `rerun-tasks` vs `verify-checkpoints --recover` vs (future) `recover-from-reflect`. The umbrella positions us for v2 additions without proliferating top-level verbs.

**Concession**: if the umbrella is judged too speculative for v1, ship rerun-tasks as a standalone verb with the EXPLICIT intent (documented in `--help` and the release notes) to fold it under `sprint repair tasks` in a future minor version, with `sprint rerun-tasks` aliased for compatibility.

## CLI shape

Primary (with umbrella):
```
superclaude sprint repair tasks <index> --phase N --tasks T07.11,T07.12 [--merge-back / --no-merge-back] [--dry-run] [--no-transitive] [--ignore-deps] [--force-merge] [--allow-loop] [--no-verify-checkpoints]
```

Fallback (without umbrella, ship rerun-tasks standalone with the rename plan documented).

## Implementation cost

- New file: `src/superclaude/cli/sprint/recovery.py` (~250 LOC: `RecoveryBundle` dataclass + merge engine + nominator interface).
- New file: `src/superclaude/cli/sprint/rerun_tasks.py` (~250 LOC: extraction + dep transitive closure + integration with recovery.py).
- Edits to `commands.py`: ~120 LOC (`@sprint_group.group("repair")` with sub-commands; `rerun_tasks` standalone alias).
- Edits to `models.py`: ~70 LOC (`task_results` field + `recovery_history` field + `FAIL_RECOVERABLE` status + JSON serialization).
- Edits to `executor.py`: ~40 LOC (write `phase-N-result.json`).
- Edits to `checkpoints.py`: ~30 LOC (wrap `recover_missing_checkpoints` to return `RecoveryBundle`).
- Tests: 30+ unit tests (recovery bundle, merge engine, transitive closure, nominator interface, lock file semantics, umbrella verb routing); 3 integration tests.

**Total LOC delta: ~760 LOC source + ~600 LOC tests = ~1360 LOC.**

## Migration path

Two-stage migration:

**v4.3.0**: Ship `sprint repair` umbrella with `tasks`, `checkpoints`, `auto`, `from-reflect` sub-verbs. Ship `sprint rerun-tasks` as a backward-compatible alias for `sprint repair tasks`. Ship `sprint verify-checkpoints --recover` unchanged (it still works; `sprint repair checkpoints` is the new path). Deprecation warnings on the standalone verbs printed to stderr but not enforced.

**v5.0.0**: Remove the standalone aliases. Only `sprint repair` exists.

If `sprint repair` is judged too speculative, ship `rerun-tasks` standalone in v4.3.0 (same internal structure: `recovery.py` + `rerun_tasks.py`), defer umbrella to v4.4.0 or v5.0.0 based on operational signal.

## What this proposal sacrifices

- Highest LOC of the three (clean architecture costs).
- Speculative umbrella verb that might not survive review.
- More integration with SprintRunReflect (which is itself in brainstorm state, not shipped).

These costs buy a coherent recovery surface that scales to the recovery verbs we know are coming (reflect-driven, rf-qa-driven), instead of accreting one-off verbs.

## What this proposal preserves from the others

- P01's "regex + verbatim slicing" as fallback when no MDTM template engine exists.
- P02's `FAIL_RECOVERABLE` distinction (carried into `RecoveryStatus` enum).
- P02's SHA256-based mid-flight-edit detection.
- P02's `phase-N-result.json` persistence.
- P02's reflect-report integration (carried into the nominator interface).
