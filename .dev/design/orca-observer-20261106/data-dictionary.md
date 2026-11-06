# Synthetic data dictionary

All fields below belong to this offline design fixture. They are NOT undocumented Orca API names. Every export says SYNTHETIC / READ ONLY. Base clock: 2026-11-06 08:00 UTC.

## Entities and joins

| Entity | Identity and relationship | Interpretation |
|---|---|---|
| Orchestrator | O01 onward; name and mission | Illustrative owner, not a live coordinator binding |
| Session | S001 onward; owner ID and optional worktree ID | Current records counted separately from historical records |
| Worktree | W001 onward; branch, base, head, paths | Inventory is separate from distinct mapped worktrees and mapping relationships |
| Request | Q01 onward; requester, human owner, affected session IDs | Explicit synthetic human question, not inferred from any blocked status |
| Dependency | E01 onward; from/to owner, reason, affected sessions | Declared relationship only; Relay Map cables must follow these records |
| Event | stable id and monotonic fixture seq | Deduplicated by identity, latest sequence retained, displayed in sequence order |
| Source | demo:workers/messages/checks/usage | Coverage, observation time and age accompany measurements |

## Independent state dimensions

- **lifecycle:** running / settled / unknown. Settlement does not admit a result.
- **phase:** work / review / queue / dependency. Phase is not health or percentage complete.
- **health:** no issue observed / failed result / unknown. Stale is handled separately.
- **approval:** none observed / human decision observed. A dependency wait does not imply approval.
- **freshness:** fresh / stale, with age in seconds. A stale pass cannot establish current readiness.
- **result:** succeeded / partial / failed / null. These are report outcomes, not transport events.
- **admission:** admitted / not admitted. Defined by an explicit fixture record, never inferred from settlement, packet completeness or passing tests.
- **evidence:** complete packet / partial packet. Completeness means inspectable, not accepted.
- **policy:** frozen / not frozen. Frozen work remains inert; the gallery cannot lift it.
- **tests/review:** null means unavailable. Tests are tied to check_revision and must match current revision to count as current evidence.

## Measurements

| Value | Unit/window | Coverage rule |
|---|---|---|
| cost_usd | USD, 07:00-08:00 UTC | Sum observed charges only; show measured count / scoped sessions. Null is not zero |
| cpu_pct | percent, synthetic sampled observation | Show measured sample count; do not aggregate into a fabricated capacity score |
| rss_mib | MiB, sampled observation | Missing samples remain unknown |
| retry_count | authoritative fixture attempt-log count | No terminal-output inference; retry_source identifies provenance |
| request age_min | minutes since original question, at frozen clock | Oldest observed only when messages coverage incomplete |
| affected count | distinct current session IDs | Set union, not sum of overlapping requests |
| timeline | 20 buckets, 3 minutes each, 07:00-08:00 UTC | W/R/Q/D/gap; a gap is missing observation, not idle time |

## Fixture variants

Base: 8 owners / 80 sessions / 80 mapped worktrees, equal illustrative ownership. Scale scenarios cross 5/8/10 owners with 50/80/100 sessions. Additional variants: uneven allocation; shared and unmapped trees; historical session; long Unicode identifiers; stale/unavailable source; missing checks and usage; duplicate/out-of-order events; empty inventory; hostile terminal controls.

Overview counts stay global within selected scenario. Gallery owner/search filters apply only to the labeled evidence inspector. Historical records are named separately. No arbitrary session-to-worktree or branch-to-dependency relationship is invented.

## Missing evidence behavior

Unknown values remain unknown. An unavailable source retains explicit unavailable coverage; last-known fixture data cannot be presented as current confirmation. No all-clear, ready-to-merge, resource leak, dangerous worktree or proven Git-conflict inference is authorized by this dataset.
