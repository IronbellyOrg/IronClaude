---
proposal_id: 02
persona: analyzer
model: sonnet
stance: strict-correctness / failure-mode-rigor / data-model-first
created: 2026-06-01T00:00:00Z
---

# Proposal 02 — Analyzer / Strict Correctness: "Get the data model right first"

## Stance

The T07.12 incident was masked by a representation gap: the data model has no first-class "this task failed and is recoverable" state. The conservative proposal patches the surface but leaves the underlying ambiguity. We should extend `PhaseResult` with persisted `task_results`, define clear status semantics (PASS / FAIL_RECOVERABLE / FAIL_TERMINAL / INCOMPLETE), and validate every failure mode before merge-back. Better to ship v1 with a clean model than to ship v1 with a heuristic and fight schema migration later.

## T1 — Task extraction: A with safety check (regex + parser validation)

Regex-slice as Proposal 01, BUT also parse the result through the same MDTM parser the executor uses (`classifiers.py` if it has one; otherwise the inline parser in `executor.py`). If the parsed sub-tasklist doesn't round-trip through the parser (i.e., re-parsing produces different task definitions than the original), ABORT with `"Sub-tasklist extraction failed round-trip validation. Tasklist file structure may have non-standard MDTM. Inspect <bundle>/phase-Nr-tasklist.md vs source."`

Rationale: regex is fine but unvalidated regex is a footgun. Round-trip parse is a 50-line gate that catches malformed MDTM before the rerun spends any tokens.

## T2 — Index construction: A (new sub-index, same as Proposal 01)

Agreement. Sub-index isolates the rerun bundle. No deviation.

## T3 — Dependency handling: B (walk dep graph; warn on unsatisfied)

The tasklist files declare dependencies. Read them (existing parser already does). At rerun start, for each `--tasks` entry, walk the declared `depends_on` list. For each dep, check:

1. Is dep in this rerun? OK.
2. Is dep checkbox `[x]` in source tasklist? OK (assumed satisfied).
3. Is dep checkbox `[ ]`? **WARN** with `"T07.11 depends on T07.05 which is unchecked. Rerun will likely fail. Add T07.05 to --tasks or check the source state."` Continue if operator passes `--ignore-deps`; ABORT otherwise.

For cross-phase deps (T07.11 depends on T06.03), confirm phase 6's checkpoint reports exist via `verify-checkpoints` library call. Missing → same WARN/ABORT pattern.

Rationale: silent dep violations cause confusing rerun failures. A 200ms dep walk per task is cheap insurance. `--ignore-deps` is the operator escape hatch.

## T4 — Checkbox state: A (uncheck-then-recheck originals)

Default behavior: at rerun start, mutate `phase-N-tasklist.md` to uncheck the target tasks (`[x]` → `[ ]`) AND prepend a status block to the phase frontmatter:
```yaml
rerun_in_progress:
  - task: T07.11
    started: 2026-06-01T16:30:00Z
    bundle: rerun-20260601T163000/
```
On successful rerun + merge-back, re-check the boxes and move the entry from `rerun_in_progress` to `rerun_history:` with a `completed:` timestamp.

If the rerun fails, the `rerun_in_progress` entry stays → grep-detectable "this sprint has an unfinished rerun" state.

Rationale: makes the rerun state observable in the tasklist itself, which is the canonical source. The F1 executor's "find first unchecked task" semantics naturally compose — if you re-run `sprint run --start 7` after a rerun-tasks abort, it will pick up the unchecked tasks correctly.

## T5 — Results merge-back

**Transcripts**: same as Proposal 01 (rename original to `.failed-<ts>`, copy rerun to canonical). PLUS: write a `results/phase-7-rerun-manifest.json` enumerating every renamed file and its new name. Forensics-grade audit trail.

**`execution-log.jsonl`**:
1. Append `phase_rerun_start` event at rerun start (with `--dry-run: false`, bundle path, source tasklist SHA).
2. Append per-task `task_rerun_complete` events as each task finishes (PASS/FAIL + tokens + duration).
3. Append `phase_rerun_complete` event with aggregate result.

Critically: ALSO mutate the original `phase_complete` event for phase 7 by appending a `superseded_by: <rerun-bundle-path>` field. The log remains append-only at the event level, but the `superseded_by` link makes the dependency graph explicit for log consumers.

**Checkpoint reports**: same rename-and-replace as Proposal 01. ALSO record the checkpoint's original SHA256 in the manifest before rename — proves we didn't lose data.

Rationale: append-only logs are good but referentially opaque. The `superseded_by` link is what makes the log queryable for "what's the current state of phase 7?" without requiring the consumer to recompute by scanning.

## T6 — Per-task persistence: A (extend PhaseResult; this is the right time)

Add to `models.py:PhaseResult`:
```python
task_results: list[TaskResult] = field(default_factory=list)
```
With a new `TaskStatus` member: `FAIL_RECOVERABLE` (distinct from `FAIL` which becomes `FAIL_TERMINAL`). Recoverable = transient (api_retry events, ConnectionRefused, empty output with `output_tokens: 0`). Terminal = explicit assertion failure, test failure, syntactic error.

Persist `PhaseResult` (including `task_results`) to disk as `results/phase-N-result.json` at phase end. The rerun command reads this JSON to know exactly which tasks need rerunning (no transcript-inspection heuristics).

Migration: additive field with `default_factory`. Old phase logs without `task_results` deserialize fine (empty list). Rerun-tasks falls back to transcript inspection (Proposal 01's path) only when `phase-N-result.json` is missing or has empty `task_results` — i.e., for legacy sprints predating this change.

Rationale: the data model bug IS the operational bug. Transcript inspection is a heuristic that will fail on edge cases (e.g., a task that legitimately runs in 14KB because it's a doc edit). Persisted `task_results` is the truth. Cost is ~50 LOC + 2 tests.

## T7 — /sc:reflect integration: B (`--from-reflect-report` flag; tight coupling, but earned)

The SprintRunReflect brainstorm proposes reflect produces a structured deviation register at a known path. Adding:
```
superclaude sprint rerun-tasks <index> --from-reflect-report <path>
```
Reads the deviation register (a YAML/JSON section in the reflect report), filters entries with `classification: regression` or `classification: drift`, extracts T-IDs, and constructs the equivalent `--phase --tasks` invocation. Prints the resolved command back to the operator before executing.

The textual contract (Proposal 01's path) is also supported as a fallback — `--from-reflect-report` is opt-in.

Rationale: when the reflect machinery exists (SprintRunReflect ships), the textual paste is a degradation. Direct flag eliminates the paste step and surfaces "I'm acting on reflect's nominations" in the execution log explicitly. Tight coupling is earned by both sides versioning the deviation-register schema (the reflect brainstorm should commit to a stable schema if this lands).

## T8 — Failure modes

- **Retry-of-retry**: max 3 reruns per phase per task, tracked in `rerun_history` frontmatter. 4th attempt aborts with `"Task T07.11 has been rerun 3 times. Manual intervention required. Inspect bundles: <list>"`. Operator can pass `--allow-loop` to override, but the default protects against retry-storm loops on a structurally broken task.
- **Partial-deliverable preservation**: NEVER overwrite the original deliverable file without taking a backup first. If T07.11's deliverable was `src/superclaude/cli/sprint/commands.py` and the original sprint partially edited it, the rerun produces a NEW patch over the partial state. To get back to pre-rerun: rerun stashes the file's pre-rerun content to `<bundle>/preserved/<relative-path>` and records the stash in the manifest. `--restore` flag on rerun-tasks restores from the most recent bundle.
- **Original tasklist edited mid-flight**: SHA256 check as Proposal 01. ABORT on mismatch. `--force-merge` allowed but logs `"WARNING: source tasklist SHA mismatch; merge-back proceeding under operator override"` to execution log AND to stderr.
- **Bundle dir collision**: `<results_dir>/rerun-<ts>/` collision (extremely rare, ns timestamp). Auto-suffix `-1`, `-2`. After `-9`, ABORT.

## T9 — Composition with verify-checkpoints: A (auto-invoke `--recover` after successful merge-back)

After `rerun-tasks --merge-back` succeeds, automatically invoke `verify-checkpoints --recover --phase N --quiet`. If it finds and regenerates missing checkpoint reports (e.g., `phase-7-cp2.md` that the rerun produced raw artifacts for but didn't synthesize the report), that work is done. If everything is already clean, the invocation is a no-op.

Print: `"Verified checkpoints for phase 7. <K> missing reports recovered."` (or `"all present"`).

Rationale: the two verbs compose naturally — rerun produces work; verify-checkpoints produces reports. Auto-invoking is safe (it's idempotent and read-mostly) and saves the operator a step. `--no-verify` flag disables for the rare case the operator wants to inspect raw artifacts first.

## CLI shape

```
superclaude sprint rerun-tasks <index> [--phase N --tasks T07.11,T07.12 | --from-reflect-report <path>] [--merge-back / --no-merge-back] [--dry-run] [--ignore-deps] [--force-merge] [--allow-loop] [--no-verify]
```

Mutually-exclusive group: `(--phase + --tasks)` XOR `--from-reflect-report`.

## Implementation cost

- New file: `src/superclaude/cli/sprint/rerun_tasks.py` (~350 LOC: extraction + parser round-trip + dep walk + persist `phase-N-result.json` reader + reflect-report parser + merge-back + manifest writer + restore).
- Edits to `commands.py`: ~80 LOC (Click block with mutually-exclusive group).
- Edits to `models.py`: ~50 LOC (`FAIL_RECOVERABLE` status; `task_results` field; JSON serialization).
- Edits to `executor.py`: ~40 LOC (write `phase-N-result.json` at phase end, populate `FAIL_RECOVERABLE` classification heuristic).
- Edits to `checkpoints.py`: 0 (re-use existing `recover_missing_checkpoints()` as a library call).
- Tests: 20+ unit tests (extraction round-trip, dep walk, status classification, manifest integrity, restore semantics, SHA mismatch, rerun-loop bound, mutually-exclusive flags); 2 integration tests.

**Total LOC delta: ~520 LOC source + ~450 LOC tests = ~970 LOC.**

## Migration path

Ship as new `rerun-tasks` subcommand AND ship the data model extension in the same release. Reasons:
1. Data model change is additive (default_factory makes it backward compatible).
2. New verb depends on the data model; shipping separately means v1 is a worse heuristic that we'd have to redo.
3. The operational pain justifies the bigger surface.

The reflect-report flag (`--from-reflect-report`) ships in the same release as the SprintRunReflect feature — they are co-dependent. If SprintRunReflect slips, ship rerun-tasks with the `--phase --tasks` shape only and add `--from-reflect-report` in a point release.

## What this proposal sacrifices

- Bigger LOC. More tests. Longer to ship by ~1 sprint.
- Tighter coupling to SprintRunReflect (mitigated by versioned schema commitment).
- Operator must understand the `FAIL_RECOVERABLE` vs `FAIL_TERMINAL` distinction (mitigated by clear `--help` examples).

These costs buy correctness, observability, and a clean foundation for v2.
