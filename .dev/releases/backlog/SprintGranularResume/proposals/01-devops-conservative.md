---
proposal_id: 01
persona: devops
model: opus
stance: conservative / minimal-change / ship-fast
created: 2026-06-01T00:00:00Z
---

# Proposal 01 — DevOps / Conservative: "Ship the smallest correct thing"

## Stance

Operational pain is real and recurring (proxy outages will happen again). Ship the minimum that solves SC1 (rerun only failed tasks). Defer schema changes, defer reflect coupling, defer the "umbrella verb." Compose with what already works (`verify-checkpoints --recover`) by chaining, not by re-architecting.

## T1 — Task extraction: A (regex parse of `### T<PP>.<TT>` headings)

Use Python `re.compile(r'^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}|\Z)', re.MULTILINE | re.DOTALL)` to slice task blocks verbatim from `phase-N-tasklist.md`. Preserve original frontmatter, phase goal, dependencies section verbatim. Drop tasks not in the `--tasks` list. **Do not renumber.** Write to `<results_dir>/rerun-<ts>/phase-Nr-tasklist.md` with frontmatter field `rerun_of: phase-N`.

Rationale: regex parsing is the same pattern `checkpoints.py:extract_checkpoint_paths()` uses successfully today. Verbatim slicing eliminates "synthesis bug" risk. The synthetic phase is human-readable and easy to inspect during `--dry-run`.

## T2 — Index construction: A (new sub-index `tasklist-index-Nr.md`)

Generate a fresh `tasklist-index-Nr.md` in the rerun bundle dir that references only the new `phase-Nr-tasklist.md`. The bundle dir lives at `<results_dir>/rerun-<ts>/`. The executor runs against this sub-index exactly like a normal sprint (no executor changes needed for the run itself).

Rationale: clean isolation. Operator can inspect, delete, or re-run the bundle without affecting the parent. The parent index is never mutated.

## T3 — Dependency handling: A (leave deps as-is; trust prior state)

The rerun assumes prior dependencies (passed tasks in this phase, all prior phases) are still satisfied on disk. We do NOT walk the dep graph. We DO print a one-line warning at start: `"Rerun assumes T07.01..T07.10 and T07.13..T07.21 deliverables are still on disk. If you've deleted or modified them, this rerun will likely fail."`

Rationale: 95% of reruns happen minutes/hours after the original failure; deps are still fresh. Graph walking adds complexity for a rare edge case. If a dep is genuinely missing, the task itself will fail loudly during rerun — that's an acceptable failure mode.

Operator escape hatch: a future `--include-deps` flag (NOT v1) for the rare cross-stale-clone case.

## T4 — Checkbox state: B (leave original untouched; flip on `--merge-back` only)

Default behavior: do not touch `phase-N-tasklist.md` checkboxes. Run the rerun in the isolated bundle. On successful run + `--merge-back` (default ON), flip the source tasklist checkboxes from `[ ]` to `[x]` for the rerun tasks AND append a `<!-- rerun_history: T07.11, T07.12 reran 2026-06-01T16:30:00Z -->` HTML comment after the phase goal.

`--no-merge-back` leaves source completely untouched (operator can manually splice).

Rationale: never mutate source files speculatively. The HTML comment is invisible in rendered Markdown but greppable and machine-parseable.

## T5 — Results merge-back

**Transcripts**: rerun produces `<results_dir>/rerun-<ts>/phase-Nr-task-T<PP>.<TT>-output.txt` and `-errors.txt`. On `--merge-back`:

1. Rename the original failed transcripts: `phase-7-task-T07.11-output.txt` → `phase-7-task-T07.11-output.failed-<orig-ts>.txt` (preserve forensic record).
2. Copy rerun transcripts into the canonical `results/` dir at `phase-7-task-T07.11-output.txt`.
3. Same treatment for `phase-7-cp2.md`: rename original (if exists) to `.failed-<ts>.md`, copy rerun output to canonical name.

**`execution-log.jsonl`**: append a new event:
```
{"event": "phase_rerun", "phase": 7, "tasks": ["T07.11", "T07.12"], "rerun_bundle": "<path>", "result": "success|partial|fail", "timestamp": "..."}
```
Do NOT mutate the original `phase_complete` event. The log becomes append-only history.

Rationale: append-only logs are forensically sound. Renaming (not deleting) failed transcripts preserves the retry-storm evidence for debugging.

## T6 — Per-task persistence: B (transcript inspection; NO schema change in v1)

The executor already writes `results/phase-N-task-T<PP>.<TT>-output.txt`. The transcript has a final JSON line with `is_error: bool, output_tokens: int, total_cost_usd: float`. The rerun-tasks command's "discover failed tasks" helper reads these transcripts and infers per-task status (PASS = `is_error: false` AND `output_tokens > 0`; FAIL = `is_error: true` OR `output_tokens == 0` OR transcript < 50KB suggests zero work).

Rationale: zero schema change. No new persistence path. Works against historical sprints today, including the MultiModelSwarm phase 7 that motivated this. Heuristic is good enough for the operator-driven `--tasks T07.11,T07.12` path (operator names the tasks; we just need to read transcripts to confirm).

Trade-off: less robust than persisted `task_results`. If we need that later (for full automation), add it in v2 as additive field.

## T7 — /sc:reflect integration: A (paste-ready command; loose coupling)

`/sc:reflect --mode post` already emits a deviation register. When it identifies Regression/Drift findings tied to specific T-IDs, it prints a paste-ready single-line command:
```
superclaude sprint rerun-tasks /path/to/tasklist-index.md --phase 7 --tasks T07.11,T07.12 --merge-back
```

`rerun-tasks` does NOT need to know about `/sc:reflect` at all. The integration is purely textual.

Rationale: this is the SprintRunReflect brainstorm's preferred path for loose composition. No new flag, no parser coupling. Operator stays in the loop (must paste & run). When the textual contract proves stable, a future `--from-reflect-report` can be added.

## T8 — Failure modes

- **Retry-of-retry**: a second `rerun-tasks` invocation on the same task IDs creates a new bundle `rerun-<ts2>/`. The previous bundle is preserved. On `--merge-back`, the canonical `phase-7-task-T07.11-output.txt` gets renamed `.failed-<rerun1-ts>.txt` and replaced by the rerun2 output. Forensic chain is preserved.
- **Partial-deliverable preservation**: rerun ALWAYS overwrites the canonical transcript/checkpoint. The original is preserved with `.failed-<ts>` suffix. Operators inspecting partial work go to the `.failed-` files.
- **Original tasklist edited mid-flight**: `rerun-tasks` records a SHA256 of `phase-N-tasklist.md` content at extraction time, stores in bundle frontmatter `source_tasklist_sha256:`. On `--merge-back`, re-hash source; if differs, ABORT merge-back with `"Source tasklist modified since rerun started. Bundle preserved at <path>. To force, use --force-merge."`

## T9 — Composition with verify-checkpoints: C (strictly orthogonal in v1)

Do not auto-invoke. Do not create an umbrella verb. After a successful `rerun-tasks --merge-back`, print a recommendation line:
```
Next: superclaude sprint verify-checkpoints /path/to/tasklist-index.md --phase 7
```

Rationale: orthogonality keeps both verbs independently testable and reasoned-about. The umbrella `sprint repair` is appealing but premature — we don't yet know the right semantics for a 3-way (work-rerun, report-regen, log-mutation) compose. Ship the primitives clean, observe the operational patterns, abstract later.

## CLI shape

```
superclaude sprint rerun-tasks <index> --phase N --tasks Tnn.NN[,Tnn.NN,...] [--merge-back / --no-merge-back] [--dry-run] [--force-merge] [--bundle-dir <path>]
```

All single-line. `--merge-back` defaults ON (operator wants the common case). `--bundle-dir` defaults to `<results_dir>/rerun-<isots>/`.

## Implementation cost

- New file: `src/superclaude/cli/sprint/rerun_tasks.py` (~250 LOC: extraction + bundle build + transcript discovery + merge-back).
- Edits to `src/superclaude/cli/sprint/commands.py` (~60 LOC: new `@sprint_group.command("rerun-tasks")` Click block).
- Edits to `executor.py`: zero (rerun invokes the existing single-phase entry point on the synthetic bundle).
- Edits to `models.py`: zero (transcript inspection, no new persisted fields).
- Tests: 8-10 unit tests for extraction/regex/sha256/merge-back semantics; 1 integration test against a fixture tasklist.

**Total LOC delta: ~310 LOC source + ~250 LOC tests = ~560 LOC.**

## Migration path

Ship as new `rerun-tasks` subcommand. No flag on existing `run`. Reasons:
1. The verb has its own argument shape (`--phase`, `--tasks`, `--merge-back`) that doesn't compose with `--start --end`.
2. New verb is opt-in by name — zero risk of accidental activation.
3. Easier to deprecate or rename later if v2 lands `sprint repair`.

## What this proposal sacrifices

- No tight reflect coupling (operator must paste).
- No persisted `task_results` (transcript inspection has edge cases).
- No dep graph validation (trust + loud failure).
- No umbrella verb.

These are deliberate v1 omissions to ship fast.
