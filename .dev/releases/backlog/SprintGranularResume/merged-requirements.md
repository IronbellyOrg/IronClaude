---
type: Technical Design Document
spec_id: SPEC-SPRINT-RERUN-TASKS-V4.3.0
adversarial_status: pass
convergence_score: 0.82
proposals_synthesized: 3
created: 2026-06-01T00:00:00Z
related_brainstorms:
  - .dev/releases/backlog/SprintRunReflect/merged-requirements.md
  - .dev/releases/backlog/TaskQAComparison/merged-recommendation.md
---

# Merged Requirements — `superclaude sprint rerun-tasks` (Granular Phase Resume)

## Executive summary

Add `superclaude sprint rerun-tasks <index> --phase N --tasks T<PP>.<TT>[,...]` as a standalone sprint subcommand that re-executes only the named tasks within phase N, merges the results back into the canonical results directory and tasklist, and integrates with the existing `verify-checkpoints --recover` machinery. Internally implemented via a new `recovery.py` abstraction (`RecoveryBundle` dataclass + generic merge engine) that will host future `sprint repair` umbrella sub-verbs (`repair tasks` / `repair checkpoints` / `repair from-reflect`) in v4.4.0 or v5.0.0 — no architectural churn at that time, only a CLI re-surface. The data model is extended additively with persisted `task_results: list[TaskResult]` on `PhaseResult` (written to `results/phase-N-result.json` at phase end) plus a new `FAIL_RECOVERABLE` `TaskStatus` member. The verb supports both manual nomination (`--phase --tasks`) and reflect-driven nomination (`--from-reflect-report <path>`), routed through a shared nominator interface that's forward-compatible with rf-qa and CI-failure sources. Failure modes are explicitly defended: SHA256 mid-flight-edit detection, lock file for concurrent-recovery protection, retry-loop cap of 3, `.failed-<ts>` rename for forensics, and stash-and-restore for partial-deliverable preservation.

## T1 — Task extraction (RESOLVED)

**Regex slice with round-trip parser validation.** New helper `rerun_tasks.extract_phase_subset(source_path, target_task_ids)`:

1. Read `phase-N-tasklist.md` verbatim.
2. Apply regex `r'^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}|\Z)'` (MULTILINE | DOTALL) to identify task blocks.
3. Preserve verbatim: frontmatter, phase goal heading, dependencies section, any narrative between frontmatter and first task heading.
4. Slice out only the target task blocks (matching `--tasks` IDs exactly). Preserve original T-IDs (do not renumber).
5. Re-parse the result through the same MDTM parser the executor uses. If `parsed(slice) != parsed(original).filter(target_ids)`, ABORT with `"Sub-tasklist extraction failed round-trip validation. Inspect <bundle>/phase-Nr-tasklist.md vs source."` This catches malformed MDTM before tokens are spent.
6. Write to `<results_dir>/rerun-<ts>/phase-Nr-tasklist.md` with frontmatter fields `rerun_of: phase-N`, `source_tasklist_sha256: <hex>`.

**Rationale**: regex matches `checkpoints.py:extract_checkpoint_paths()`'s proven pattern; round-trip parse is a 50-LOC gate that prevents silent corruption. Template-rendering (P03's preferred path) deferred — only adopt if a re-usable MDTM template engine emerges in the codebase; the regex+round-trip is the pragmatic v1.

## T2 — Index construction (RESOLVED)

**New sub-index `tasklist-index-Nr.md` in the rerun bundle dir.** Generate alongside `phase-Nr-tasklist.md`:

- Bundle dir: `<results_dir>/rerun-<ts>/`
- Contains: `tasklist-index-Nr.md`, `phase-Nr-tasklist.md`, `recovery-bundle.json` (the serialized `RecoveryBundle`).
- The executor runs against this sub-index exactly like a normal single-phase sprint. No executor surgery required for the run itself.

The parent `tasklist-index.md` is never mutated.

## T3 — Dependency handling (RESOLVED)

**Walk-and-warn by default; transitive auto-include behind `--include-transitive`.**

At rerun start, for each target task in `--tasks`:

1. Read declared `depends_on` list from the source tasklist (existing parser).
2. For each dep:
   - In this rerun? OK.
   - `[x]` in source tasklist? OK (assumed satisfied).
   - `[ ]` in source tasklist? **WARN**: `"T07.11 depends on T07.05 which is unchecked. Rerun will likely fail. Add T07.05 to --tasks, pass --include-transitive, or pass --ignore-deps."` ABORT unless `--ignore-deps`.
3. For cross-phase deps (T07.11 → T06.03), confirm phase 6's checkpoint reports exist via a `checkpoints.verify_checkpoint_files()` library call. Missing → same WARN/ABORT.

With `--include-transitive`: automatically include failed-dep tasks (per persisted `task_results` or transcript inspection), up to a 50% cost ceiling. Above 50% → ABORT with the recommendation to use `sprint run --start N --end N`.

## T4 — Checkbox state mutation (RESOLVED)

**Uncheck-then-recheck originals with auto-restore on abort.**

- At rerun start (after extraction validation), mutate `phase-N-tasklist.md`:
  - Flip target task checkboxes `[x]` → `[ ]`.
  - Prepend a `rerun_in_progress:` block to phase frontmatter listing target task IDs, bundle path, start timestamp.
- On successful rerun + merge-back: flip checkboxes back to `[x]`, move entry from `rerun_in_progress` to `rerun_history:` with completion timestamp.
- On rerun ABORT (before merge-back): auto-restore checkboxes to `[x]` and clear `rerun_in_progress`. **Source returns to pre-rerun state.** This satisfies INV-3 ("failed rerun must not leave source worse off") while preserving INV-2 ("second sprint run must see rerun tasks complete") for the success path.
- All mutations write to a shared audit log at `<results_dir>/recovery-audit.log` (see T9).

## T5 — Results merge-back (RESOLVED)

Define `RecoveryBundle` in `models.py`:
```python
@dataclass
class RecoveryBundle:
    bundle_id: str               # rerun-<isots>
    verb: str                    # "rerun-tasks"
    affected_phase: int
    affected_tasks: list[str]
    artifacts_produced: list[Path]
    artifacts_replaced: dict[Path, Path]  # canonical -> preserved-with-.failed-<ts>
    source_tasklist_sha256: str
    end_tasklist_sha256: str | None
    status: RecoveryStatus       # SUCCESS | PARTIAL | FAILED | DRYRUN
    rerun_attempt: int           # 1, 2, 3 — cap at 3
```

A new helper `recovery.merge_recovery_bundle(bundle, source_index)` performs the canonical merge:

1. **Transcripts**: rename original `results/phase-7-task-T07.11-output.txt` → `phase-7-task-T07.11-output.failed-<orig-ts>.txt`. Copy rerun bundle's `phase-Nr-task-T07.11-output.txt` to canonical path.
2. **Checkpoint reports**: same rename-and-replace for `phase-7-cp2.md` and similar artifacts.
3. **Errors files**: same treatment for `-errors.txt`.
4. **`results/phase-7-rerun-manifest.json`**: write enumerating every renamed file and its new name, including original SHA256s.
5. **`execution-log.jsonl`**: append three events:
   - `{"event": "phase_rerun_start", "phase": 7, "tasks": [...], "bundle": "<path>", "source_sha": "..."}`
   - One `{"event": "task_rerun_complete", ...}` per task with PASS/FAIL + tokens + duration.
   - `{"event": "phase_rerun_complete", "phase": 7, "status": "success", "bundle": "<path>"}`
6. **Mutate original `phase_complete` event**: append a `superseded_by: <bundle-path>` field. Log remains append-only at the event level but the link makes the dependency graph explicit.
7. **`phase-N-result.json`**: rewrite with updated `task_results` reflecting the new PASSes, and append the bundle to `recovery_history: list[RecoveryBundleRef]`.

The merge engine is generic over `RecoveryBundle`. `verify-checkpoints --recover` can be retrofitted to produce a `RecoveryBundle` and share the same merge engine in v4.4.0 (no v1 work required).

## T6 — Per-task persistence (RESOLVED)

**Extend `PhaseResult` additively; persist `phase-N-result.json` at phase end.**

In `models.py:PhaseResult`:
```python
task_results: list[TaskResult] = field(default_factory=list)
recovery_history: list[RecoveryBundleRef] = field(default_factory=list)
```

In `models.py:TaskStatus`:
```python
PASS = "pass"
FAIL_TERMINAL = "fail_terminal"      # was FAIL — keep "fail" string for back-compat? See migration note.
FAIL_RECOVERABLE = "fail_recoverable"
INCOMPLETE = "incomplete"
SKIPPED = "skipped"
```

**Back-compat handling**: rename `FAIL` → `FAIL_TERMINAL` BUT keep its serialized string as `"fail"` (Python enum value separate from name). Existing logs deserialize correctly. New code chooses `FAIL_RECOVERABLE` for transient failures (api_retry storms, ConnectionRefused, `output_tokens == 0` with `is_error: true`).

**Classification heuristic** (in `executor.py` post-task):
- `is_error: false` + `output_tokens > 0` → PASS.
- `is_error: true` AND transcript contains `api_retry` events OR `ConnectionRefused` OR `output_tokens == 0` → FAIL_RECOVERABLE.
- `is_error: true` AND none of the above (genuine assertion/test failure) → FAIL_TERMINAL.
- Process killed / mid-task transcript truncation → INCOMPLETE.

In `executor.py`: at phase end, write `<results_dir>/phase-N-result.json` containing serialized `PhaseResult` (~20 LOC). Existing JSONL-event consumers unaffected.

**Legacy-sprint fallback**: `rerun-tasks` first tries to read `phase-N-result.json`. If missing OR `task_results` is empty (legacy sprint), fall to transcript inspection: read each `results/phase-N-task-T<PP>.<TT>-output.txt`, parse the final JSON line, apply the same classification heuristic on-the-fly.

## T7 — `/sc:reflect` integration (RESOLVED)

**`--from-reflect-report <path>` flag via shared nominator interface.**

Introduce `--nomination-source {manual|reflect-report}` (defaults inferred from other flags):
- `--phase N --tasks T07.11,T07.12` → `manual`.
- `--from-reflect-report <path>` → `reflect-report`.
- Mutually exclusive.

For `reflect-report`:
1. Read the path (the SprintRunReflect brainstorm proposes reflect emits a YAML/JSON deviation register; this spec depends on that emitting a stable schema).
2. Filter entries with `classification: regression` OR `classification: drift`.
3. Extract T-IDs into the same `--tasks` resolution path.
4. Print the resolved equivalent command to the operator before executing: `"Resolved from reflect report: rerun T07.11, T07.12. Equivalent manual command: superclaude sprint rerun-tasks <index> --phase 7 --tasks T07.11,T07.12"`.

The nominator interface (`Nominator` protocol with `def nominate(self, context) -> list[TaskID]`) is forward-compatible: future v4.4.0+ can plug in `RfQaNominator`, `CiFailureNominator` without re-architecting.

**Co-dependency note**: `--from-reflect-report` ships in the same release as SprintRunReflect's reflect-report schema commitment. If SprintRunReflect slips, ship `rerun-tasks` v1 with manual-only nomination; add `--from-reflect-report` in a point release.

## T8 — Failure modes (RESOLVED)

**Layered defenses** (all of the following are mandatory):

1. **SHA256 mid-flight-edit detection**: bundle frontmatter records `source_tasklist_sha256:` at extraction. On merge-back, re-hash source; mismatch → ABORT with `"Source tasklist modified since rerun started. Bundle preserved at <path>. To force, use --force-merge."` `--force-merge` allowed but logs strong WARN.
2. **Retry-loop cap of 3**: track in `recovery_history` on `PhaseResult`. 4th attempt on the same T-ID ABORTS with `"Task T07.11 has been rerun 3 times. Manual intervention required. Inspect bundles: <list>"`. `--allow-loop` override allowed for the rare structurally-stubborn case.
3. **`.failed-<ts>` rename for forensics**: never delete original artifacts. Preserved with `.failed-<orig-ts>` suffix.
4. **Stash-and-restore for partial deliverables**: before rerun, stash any file the task is known to deliver to `<bundle>/preserved/<relative-path>` (with the manifest enumerating). `--restore` flag on `rerun-tasks` restores from the most recent bundle.
5. **Lock file for concurrent-recovery protection** (addresses INV-4): write `<results_dir>/.recovery-locks/phase-N.lock` containing PID + timestamp at rerun start. Concurrent invocation detects existing lock → ABORT with PID and remediation. Lock auto-cleared on process exit (atexit handler + signal handler).
6. **Bundle dir collision**: auto-suffix `-1`..`-9`; abort at `-9`.
7. **Auto-restore on rerun ABORT**: see T4. Source returns to pre-rerun state on any pre-merge-back abort.

## T9 — Composition with `verify-checkpoints` (RESOLVED)

**Hybrid: standalone verb in v1, unified architecture under the hood, umbrella deferred.**

**v1 (v4.3.0)**:
- Ship `superclaude sprint rerun-tasks` as a standalone subcommand.
- Internally implemented via `recovery.py` + `RecoveryBundle` (P03's architecture).
- After successful `--merge-back`, auto-invoke `verify-checkpoints --recover --phase N --quiet`. Print: `"Verified checkpoints for phase N. <K> missing reports recovered."` `--no-verify-checkpoints` opt-out.
- Existing `superclaude sprint verify-checkpoints` unchanged. Documented as orthogonal in v1 (`rerun-tasks` re-runs WORK; `verify-checkpoints` regenerates REPORTS) and as the eventual `sprint repair checkpoints` sub-verb.

**v4.4.0 or v5.0.0 (deferred)**:
- Ship `superclaude sprint repair` umbrella with sub-verbs (`tasks`, `checkpoints`, `auto`, `from-reflect`).
- `sprint rerun-tasks` aliased to `sprint repair tasks` for back-compat through v4.x; removed in v5.0.0.
- `sprint verify-checkpoints` aliased to `sprint repair checkpoints` similarly.
- No architectural churn: the umbrella is a CLI re-surface only. `recovery.py` and `RecoveryBundle` are already in v4.3.0.

## CLI shape (v1)

Single-line per memory `feedback_no_multiline_paste.md`:

```
superclaude sprint rerun-tasks <index> --phase N --tasks T07.11,T07.12 [--merge-back / --no-merge-back] [--dry-run] [--include-transitive] [--ignore-deps] [--force-merge] [--allow-loop] [--no-verify-checkpoints] [--bundle-dir <path>] [--restore]
```

Or with reflect:

```
superclaude sprint rerun-tasks <index> --from-reflect-report <path> [--merge-back / --no-merge-back] [--dry-run] [--no-verify-checkpoints]
```

`--phase + --tasks` is mutually exclusive with `--from-reflect-report` (Click group).

Defaults:
- `--merge-back`: ON
- `--include-transitive`: OFF
- `--ignore-deps`: OFF
- `--force-merge`: OFF
- `--allow-loop`: OFF
- `--no-verify-checkpoints`: OFF (i.e., verify-checkpoints runs by default)

## Implementation cost

**Files to change** (all under `src/superclaude/cli/sprint/`):

| File | Action | LOC delta |
|---|---|---|
| `recovery.py` | NEW: `RecoveryBundle`, `RecoveryStatus`, `merge_recovery_bundle()`, `Nominator` protocol, shared audit log writer | ~250 |
| `rerun_tasks.py` | NEW: `extract_phase_subset()`, dep walker, transitive closure, transcript fallback, run orchestration | ~280 |
| `commands.py` | EDIT: new `@sprint_group.command("rerun-tasks")` Click block with mutually-exclusive group | ~90 |
| `models.py` | EDIT: `task_results` + `recovery_history` fields on `PhaseResult`; `FAIL_RECOVERABLE` enum member; JSON serialization | ~70 |
| `executor.py` | EDIT: write `phase-N-result.json` at phase end; FAIL classification heuristic | ~40 |
| `checkpoints.py` | EDIT: wrap `recover_missing_checkpoints()` to return `RecoveryBundle` (forward-compat for v4.4.0) | ~30 |
| Tests | NEW: ~25 unit tests + 2 integration tests | ~500 |

**Total LOC delta: ~760 source + ~500 tests = ~1260 LOC.**

**Dependencies**: none new. Re-uses existing Click, dataclasses, json, hashlib (stdlib), and the project's existing MDTM parser.

**Hook on `make sync-dev`**: zero (this is Python source, not skill/command sync output).

## Migration path

1. **v4.3.0** (next minor):
   - Ship `recovery.py` + `rerun_tasks.py` + `models.py` extensions + `executor.py` phase-result write + `commands.py` Click block.
   - Ship `--phase --tasks` shape (manual nomination).
   - Ship `--from-reflect-report` ONLY IF SprintRunReflect lands a stable deviation-register schema in the same release. Otherwise defer to v4.3.1.
   - Document `sprint rerun-tasks` and `sprint verify-checkpoints` as orthogonal in v1 release notes; flag the intent to unify under `sprint repair` in v4.4.0/v5.0.0.

2. **v4.4.0 or v5.0.0** (deferred, signal-driven):
   - Ship `sprint repair` umbrella with sub-verbs (`tasks`, `checkpoints`, `auto`, `from-reflect`).
   - Alias standalone verbs (`rerun-tasks`, `verify-checkpoints`) for back-compat through v4.x.
   - Remove standalone verbs in v5.0.0.

## Composition with SprintRunReflect brainstorm

The two brainstorms are independent but composable:

- **SprintRunReflect** (convergence 0.85): integrates `/sc:reflect --mode post --depth deep` as a post-phase sidecar. Produces a deviation register with `classification: regression | drift | etc` per task.
- **SprintGranularResume** (this doc, convergence 0.82): the recovery vehicle for reflect's nominations.

**Ship sequencing**:

- **Option A — independent**: ship `rerun-tasks` v1 (manual nomination only) in v4.3.0; ship SprintRunReflect in v4.4.0; add `--from-reflect-report` in v4.4.0 alongside reflect's schema commitment. **Recommended** — reduces v4.3.0 surface, lets each feature prove itself, schema co-design happens once both halves are stable.
- **Option B — co-shipped**: ship both in v4.3.0 with `--from-reflect-report` working out of the gate. Higher coordination cost; both teams must agree on the deviation-register schema in the same release.

Recommendation: **Option A**. The manual-nomination path solves the immediate MultiModelSwarm pain (operator names T07.11+T07.12 and recovers). Reflect-driven automation is incremental value, not a blocker.

## Open questions for user resolution (RESOLVED 2026-06-01)

| # | Question | Decision | Implication |
|---|---|---|---|
| 1 | Umbrella verb `sprint repair` in v4.3.0 vs defer | **DEFER to v4.4.0/v5.0.0** | v4.3.0 ships `rerun-tasks` standalone; `recovery.py` internals pre-position the abstraction so the umbrella verb lands later without re-architecture |
| 2 | Ship sequencing with SprintRunReflect | **INDEPENDENT (Option A)** | `rerun-tasks` v4.3.0 ships with manual `--tasks Tnn.NN,...` nomination only; `--from-reflect-report` flag co-ships with SprintRunReflect in v4.4.0 |
| 3 | `FAIL_RECOVERABLE` TaskStatus enum member | **INTRODUCE in v4.3.0** | Cleaner semantics than overloading existing `FAIL`/`ERROR`; transient-class failures (proxy/transport/API-retry-exhaustion) classified `FAIL_RECOVERABLE`; `rerun-tasks` without explicit `--tasks` defaults to picking up only `FAIL_RECOVERABLE` tasks within the named phase |
| 4 | Auto-invoke `verify-checkpoints --recover` after merge-back | **ON by default** | After successful rerun + merge-back, missing checkpoint markdown reports auto-regenerate; `--no-verify-checkpoints` flag opts out for explicit operator control |

These decisions land in `return-contract.yaml` under `resolved_decisions`. The TDD phase can proceed without further user adjudication on these axes.

## Acceptance criteria (success gates for v4.3.0 ship)

- **AC1** (SC1): `superclaude sprint rerun-tasks <index> --phase 7 --tasks T07.11,T07.12 --dry-run` against the MultiModelSwarm tasklist prints the extraction plan listing exactly those 2 tasks without executing.
- **AC2** (SC2): same command without `--dry-run` re-executes only T07.11 + T07.12, produces fresh transcripts at canonical paths, renames originals with `.failed-<ts>`, flips checkboxes in `phase-7-tasklist.md`, appends `phase_rerun_complete` event to `execution-log.jsonl`, and auto-invokes `verify-checkpoints --recover` producing `phase-7-cp2.md`.
- **AC3**: A round-trip test — clean sprint run vs (failed sprint + rerun-tasks) — produces equivalent on-disk artifact set (modulo timestamps and `recovery_history` entries).
- **AC4**: Concurrent invocation of two `rerun-tasks` against the same phase: second invocation aborts on lock file with clear PID.
- **AC5**: Rerun after source-tasklist edit (SHA mismatch) aborts cleanly; `--force-merge` proceeds with strong WARN.
- **AC6**: Rerun attempt 4 on the same T-ID aborts with retry-cap message; `--allow-loop` overrides.
- **AC7**: Legacy sprint without `phase-N-result.json` falls back to transcript inspection and successfully discovers failed tasks via `is_error`/`output_tokens` heuristic.
- **AC8**: ABORT before merge-back auto-restores source tasklist to pre-rerun state (checkboxes + `rerun_in_progress` cleared).
