# Diagnosability Tasklist

**Issue**: Issue 501: invalid swarm refactor-find recommendation
**Verdict**: partial (event-log coverage); actual disputed string captured
**Complexity**: trivial (score 0)
**failing_component**: src/superclaude/cli/swarm/lenses/refactor_find.py
**Round**: 0 counted emissions of 3; no discriminator required
**re-run permitted**: yes for read-only local/stub checks; no paid run
**discriminator-required**: no
**capability-verdict**: n/a
**branch**: swill-ib/bug-swarm-refactor-find-recommends-unavailable-s
**repro-venue-id**: local-swarm-stub

## Emitter search
emitter-search: n/a (no missing single-expression predicate; disputed command already captured)
emitters-found: 2 in bounded recommendation chain: emit_contract at reduce.py:702 and caller stdout at commands.py:2173. The first is a result-file emitter, not a logger.
already-read-files: 2 direct captured sinks (return-contract.yaml, execution-log.jsonl); source reads are not capture routes.
usable-capture-routes: 1: existing return-contract.yaml at permitted local --output, read-only artifact capture already completed. stdout omits value; event log omits value and is excluded as a datum route. No production edit required.

## Discriminator rows
core-rows=0, pack-rows=0, total-rows=0. One known string producer; full failing datum captured. No disputed primitive, competing mechanism or missing comparator requires a discriminator. No measurements pending.

## Fix candidate
None applied. A future remediation would repair the lens's command template and refactor-find's report-list substitution, with tests; this is a product change, not an instrumentation task, and requires the next agreed step.

## Hard Constraints
Invocation sites only; additive only; reversible; annotated if instrumentation is added. No production edits or paid runs authorized.

## Implementation tasks
No additional instrumentation proposed. Existing invocation and result artifact already expose the exact disputed datum; avoid speculative logging changes.

## Verification
The preserved local-cli-stub-1 return-contract.yaml:64 supplies the complete emitted command. Input compatibility check observed three readable final reports and literal_existing_review_present=True. No automatic rerun is required.

## Rollback
No instrumentation patch exists to revert. Keep the diagnostic evidence; no file deletion or rollback action is proposed.

## Patch-round counter
Discriminator-required is no throughout this run. No counted emission, authoritative counter not opened or modified, no snapshot fabricated. Stable identity is recorded above for provenance only.
