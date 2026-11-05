# Hypothesis: a resume restart writes into the first attempt's directory under the same cycle_id (C1); the draft per-attempt layout is sound, but the core should compute the attempt number, not the agent

**Agent**: system-architect (lens; worker troubleshoot-analyst)
**Tier**: 2
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: two documented rules collide on one path ("--out must be missing or empty" vs "restart under the same cycle_id")
**Claim class**: `mechanism`
**Evidence class**: `runtime_repro` (parent probe, tier1-observation.md `## Probe`, probe-evidence.out:4-5)
**Verdict direction**: `AFFIRM` (confirms C1, refines the draft fix)
**Consistency with docs**: conflicts (changes the `sync/<cycle_id>/` layout in both refs and design source.md:844, :1012)
runs-in=src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:71 @ Tier 2 resume restart (rows 5 and 7) -> scripts/collect-conflict-evidence.sh (--out check)
producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
Counting `sync_started` records per cycle_id is durable and unambiguous: the JSONL is append-only and fsynced in the same output dir as `sync/`; cycle ids are unique within one JSONL; every attempt that can write files has its own record (steps 0-2 of a restart write nothing before step 3 appends). The count does not depend on `resumed: true` (no core code reads it). The weak point: the draft has the agent count lines by hand, contrary to the ref's rule that the core decides cycle ids, and untestable. Only Tier 2 fails today (Tier 1 never calls the collector). Message, manifest and resolution.md are overwritten safely, but overwriting destroys attempt 1's record, which conflict-intent.md:95 keeps; conflict-intent.md:99 must pass `<cycle_dir>` to the validator or it sees attempt 1's stale evidence.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | command_output | probe-evidence.out:4-5; behaviour-definition: row 2 | second collect into sync/sync-1/1/ -> EVIDENCE_FAIL out_not_empty, exit=2 |
| E2 | source_citation | src/superclaude/pr_submit/run_log.py:87, :91-92 | JSONL = output_dir/monitor-run-<PR>.jsonl; reopening continues the file |
| E3 | source_citation | src/superclaude/pr_submit/run_log.py:133-136 | each append flushed and fsynced |
| E4 | source_citation | src/superclaude/pr_submit/run_log.py:276-294 | conflict_cycles keeps each id once; sync_concluded pops the open cycle; no per-attempt count |
| E5 | source_citation | src/superclaude/pr_submit/conflicts.py:1146-1154, :35 | id from len(conflict_cycles)+1; SYNC_CAP = 1 |
| E6 | source_citation | src/superclaude/pr_submit/conflicts.py:1531-1548 | rows 5 and 7 return the open cycle's cycle_id, hook, review_terminal; no attempt field |
| E7 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:11, :67, :69, :71, :252 | the core decides cycle ids; restart begins at step 0 or 1 |
| E8 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-intent.md:19, :71, :95, :99 | still the old layout; :99 passes the whole sync/<cycle_id>/ |
| E9 | source_citation | tests/pr_submit/test_conflict_e2e.py:259, :287-291, :610, :845-847 | resumed False hardcoded; files under sync/<cycle_id>/ |
| E10 | test_assertion | tests/pr_submit/test_run_log.py:403 | rebuild_state key set pinned |

## Proposed Fix
1. Pure `conflict_attempt(events, cycle_id) -> int` in conflicts.py, exported from `__init__.py`: the number of events with event_type "sync_started" and that cycle_id; ValueError when 0 (called only after the append). Not in rebuild_state (avoids E10).
2. Step 3: `attempt := conflict_attempt(<run-log events>, cycle_id)`; keep the draft's cycle_dir, step 6, step 9, row 5.
3. conflict-intent.md: :19 `--out <cycle_dir><n>/`; :71 `<cycle_dir>resolution.md`; :95 every attempt's record and evidence directories stay; :99 `<cycle_dir>` as output_dir.
4. e2e :610 and :845: sync_dir = output_dir / "sync" / cycle_id / f"a{conflict_attempt(...)}".
5. New Tier 2 e2e regression: abort, sync_concluded{aborted, recovered: true}, sync_started resumed=True, merge again, collect into a2/1/, exit 0, a1/ unchanged.
6. Unit tests: 0 records -> ValueError; 2 -> 2; other ids and non-string ids ignored.

## Confidence
Self-reported 0.82 (calibrator re-grades).

## Risks
- Two consecutive crashes around row 5/7 can close the cycle and hit sync_cap on a new id (predates the fix; out of C1 scope).
- Deleting the JSONL but keeping sync/ collides on a1: fails safe (out_not_empty -> Tier 3).
- An export-list test may need updating (unverified).

## If I'm wrong, it's probably because...
The SKILL appends sync_started through a path that does not re-read the log before step 5, or a writer creates files under sync/<cycle_id>/ before step 3 (none found).

## Falsification standard
(i) the e2e restart collects into a2/1/ with exit 0 and a1/1/ byte-identical; (ii) the :610 and :845 flows pass with a1; (iii) conflict_attempt returns 1 then 2 across one restart; (iv) E4 still passes. (i) failing with out_not_empty refutes the claim.

## Alternatives considered
- Agent counts by hand (draft as is): rejected (no core decision, no test).
- Directory named by the sync_started event_id: opaque to validator and operator.
- Clear on restart: rejected (conflict-intent.md:95).
- New cycle_id on restart: rejected (:253, sync_cap).
