# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

Fault-finder: independent opus agent (not an advocate). Raw output: `round2.5-faultfinder-raw.md`. Evidence lines were Read by the fault-finder in the live worktree; the orchestrator re-checked INV-001 against `docs/designs/issue-watcher.md:21` (the design's guarantee sentence names a second store on the same login as documented residual risk R12).

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | sufficiency_challenge | "At-most-once holds" with no further condition (one store per login and repo) | UNADDRESSED | MEDIUM | Lock and store live under `state_dir` (`record.py:380-419`); only cross-store guard is the claim marker (`cycle.py:922-928`), which exists only after the agent posts it. Design line 21 already states the guarantee is "per intact, single dispatch store per login" and names R12 as a documented residual risk; the runbook repeats it (rule "one enabled workspace per login"). Orchestrator note: this is a documented scope condition, not a code defect. |
| INV-002 | sufficiency_challenge | No relaunch path within a single store | ADDRESSED | LOW | `_launch` reachable only from no entry or `failed` after backoff (`cycle.py:913-942`); `mark_pending` accepts only those states (`record.py:544-546`); pending/launched/unknown/abandoned-with-pending_at go through the marker-only branch (`cycle.py:903-912`); durable pending before launch (`cycle.py:1060-1062`, `record.py:370-378`). |
| INV-003 | interaction_effects | The late-launch restore fix adds no double-launch | ADDRESSED (if ordered correctly) | LOW | Re-check and restore must both sit after `_save` (1061) and before `launch` (1062); a crash between save and restore leaves a pending entry that the sweep orphans (`record.py:638-639`), safe but stranded until `reset --forfeit-guarantee`. Restoring beats leaving the entry pending: no agent would ever post a marker. |
| INV-004 | state_variables | A restore puts back exactly the pre-launch state | UNADDRESSED (fix-design constraint) | LOW | `mark_pending` sets launches 1, `consumed_at`, `pending_at` (`record.py:554-567`); `validate` rejects `failed` with launches 1 (`record.py:168-210`), so the restore must reinstate the whole document captured just before `cycle.py:1060`, not undo fields. |
| INV-005 | sufficiency_challenge | The late-launch fix alone keeps the cycle within 240 s | UNADDRESSED | LOW | Launch timeout is a fixed 120 s (`cycle.py:1062`, `Deadline` at 395-412); the save has no time limit; a launch starting at 120 s can end near 240 s plus commit and audit time. |
| INV-006 | guard_conditions | DISABLED stops a launch already being prepared | UNADDRESSED | LOW | DISABLED checked at `cycle.py:1033`, not after the origin git call (1041-1045, up to 10 s) or after the save (1061). |
| INV-007 | count_divergence | 3 reserved calls cover revalidation | UNADDRESSED | LOW | Reserved cap 35 vs 32 (`github.py:448-454`); paged re-reads may exhaust it; `budget_exhausted` is a liveness effect only, candidate retried first next cycle. |
| INV-008 | collection_boundaries | Day cap survives clock steps | UNADDRESSED (known advisory) | LOW | `_in_window` excludes future-dated `t` (`record.py:689-690`); `prune_consumed_log` keeps them (`record.py:696`). |
| INV-009 | interaction_effects | Local `pending_at` and server marker time line up | UNADDRESSED | LOW | `pending_at` from the local clock (`cycle.py:1060`), marker time from GitHub (`predicates.py:274-276, 294-295`); a local clock more than 300 s ahead stops a real marker counting; liveness only. |
| INV-010 | state_variables | `reset` cannot cause an unauthorized second launch | ADDRESSED | LOW | `reset_entry` only abandoned/unknown, keeps `consumed_at` in `consumed_log` (`record.py:706-720`); `--forfeit-guarantee` required (`cli.py:282-348`). |
| INV-011 | guard_conditions | The unconditional sweep cannot orphan a live pending entry | ADDRESSED | LOW | Sweep abandons every pending entry with no age check (`record.py:627-651`), safe because every cycle, dry-run and reset holds the exclusive flock (`record.py:380-419`, `cycle.py:663-683`). |
| INV-012 | interaction_effects | An exception after the launch keeps the record correct | ADDRESSED for safety, UNADDRESSED for the record | LOW | `_locked_body` catches only `_Stop` (`cycle.py:685-690`); disk keeps pending, swept to `pending_orphan`; operation id and retry hint lost (`cycle.py:1271`). |

## Summary

- **Total findings**: 12
- **ADDRESSED**: 4 (INV-002, INV-003, INV-010, INV-011) plus INV-012 partially
- **UNADDRESSED**: 8 (INV-001, 004, 005, 006, 007, 008, 009, 012)
  - HIGH: 0
  - MEDIUM: 1 (INV-001, documented design scope condition R12)
  - LOW: 7

No HIGH-severity UNADDRESSED invariant: the invariant-probe gate does not block convergence. MEDIUM item INV-001 is logged as a warning.
