# Verified sources and UNVERIFIED register

Recorded owner decision 5: every fact keeps its evidence label; anything unchecked is UNVERIFIED; no Orca API field is invented. The source-to-dashboard schema (`snapshot-export-schema.md`) is PROPOSED, not an Orca contract. Orca and coordinator policies keep authority.

## Verified today (seed brief, 2026-11-08), and only these

The MVP (R0, R1) needs exactly one live source.

| Need | Verb | Fields used |
|---|---|---|
| Worker rows | `orca orchestration worker-list --json --limit 100` | `result.workers[].dispatchId, taskId, runId, workerState, dispatchStatus, terminalState` |
| Ownership and worktree (verbatim, never joined across hosts) | same | `resource.{id, ownershipState, releaseState, worktreeId, ownerDispatchId, originDispatchId, recoveryAttemptCount}` |
| Next action (verbatim column) | same | `projection.nextAction.kind`, `projection.stage.{worker,dispatch,activity,detail}` |
| Freshness and liveness | same | `projection.liveness.{verdict,source,observedAt}`, `projection.evidence.{durable,liveStatus,lastObservedAt}` |
| Outcome, separate from lifecycle | same | `projection.outcome` (raw; never merged with `workerState` or `terminalState`) |
| Placement | same | `projection.host.{id,kind}`, `projection.workspace.{id,kind}`, `projection.provider.id`, `projection.role` |
| Paging and denominators | same, with `--cursor <page.nextCursor>` | `result.page.{limit,total,hasMore,nextCursor}`, `result.counts.{active,reclaimable,retained,released}`, `result.scope.source`, `result.warnings[]` |
| Binary | existing `_find_orca()` in `cli/install_user_setup.py` | validated through `skills list --json` (one-time discovery, at most one probe per candidate, `adapter-contract.md`) |

- Flags read from `--help` (no new fields): `worker-list` accepts `--run`, `--terminal-state`, `--include-remote`, `--cursor`, `--limit <1-100>`; rows are "newest first"; without `--run` the scope is the bound Run, or every Run when nothing is bound, reported in `scope.source`. `check` accepts `--peek`, `--all`, `--types`, `--run`, `--terminal`. `inbox` accepts `--limit`, `--terminal`, `--full`.
- `check --peek` / `check --all` are non-consuming per help and capped at 100 rows. Plain `check` consumes deliveries; the observer never calls it.
- `page.total` is a field the source can return, but the adapter treats it as optional (`reported unknown`; V1 dissents).
- The evidence timestamp is `projection.evidence.lastObservedAt` (owner correction).

## Candidate message verb (behind QUESTION-OBSERVATION only)

`check --all --types question --run <runId> --json`, for one named Run, is a candidate, never an available source, until the open items in `release-gates.md` (QUESTION-OBSERVATION: not passed) are recorded. Not used in R0 or R1: `check --peek`, the candidate `check --all`, `inbox`. Unfiltered `check --all` and `--peek` are not allowed in any R2 argv; plain `check`, `--ack` and `run-use` are never run.

## Seen on probe Runs and the coordinator's own Run only

Source: `RESEARCH-REPORT-phase2-gate.md` (REPORT, in `.dev/tasks/to-do/TASK-RESEARCH-phase2-gate-20261111-200400/`, evidence files 01 to 27) and `.dev/issues/409/owner-decisions-20261111.md` (OWNER). Probe Runs A `run_c1badaa6576b` and B `run_14cfcbd8edf2`, 2026-11-11. These facts were observed there and nowhere else; they are not verified for any other Run.

- Envelope `{id, ok, result:{acknowledged, count, messages[], runId}, _meta}`; message row keys `id` (`msg_...`), `run_id`, `delivery_contract`, `from_handle`, `to_handle`, `subject`, `body`, `type`, `priority`, `thread_id`, `payload`, `created_at`, `delivered_at` (REPORT 2.2, evidence file 03).
- `--types question` filters on the server side (REPORT, evidence file 24), and the 100-row cap applies after the type filter (OWNER, own Run: 41 rows).
- `check --all` returns at most 100 rows, newest first, with no total, `hasMore` or truncation field (evidence file 14); `check --peek` returns the oldest 100 first and hides acknowledged rows (evidence files 12, 15). `--all` rows carry no read marker.
- A read from a caller bound to another Run answers `{"ok":false,"error":{"code":"consumer_fenced", ...}}` (exit status 1, "Nothing changed"); a caller with no terminal identity answers `no_active_terminal` (evidence files 01, 17 to 19).
- `message.id` was unique in the probe Runs (REPORT 2.2, G-8). It is not recorded for any other Run.

## UNVERIFIED

| Item | How the MVP shows it |
|---|---|
| The inbox JSON shape (its rows add `read` and `sequence`, REPORT 2.2, evidence file 20); whether `inbox` reaches across Runs (REPORT Q-4) | `inbox` stays forbidden; not tested; forbidden |
| Meaning of `result.count` (equals 100 for a 104-row Run, evidence file 14) | No count is ever derived from it |
| Proof (a) as worded, "`--run` narrows `--all`": WITHDRAWN. `--run` is a fence, not a filter (`consumer_fenced`); see `release-gates.md` | Replaced by the one-named-Run rule |
| Proof (b), a terminal that has a handle but holds no Run (Q-1) | UNTESTED, so UNVERIFIED (REPORT 2.1 could not make such a terminal; a caller with no terminal identity at all gets `no_active_terminal`); verification task: Task 16 (gated on a plain terminal supplied by the coordinator) |
| Whether `check --all` ever consumes when the reader is not the Run's owner | UNVERIFIED; verification task: Task 16 (non-consumption is seen only as the owner on a probe Run) |
| Effect of `run-use` on a live coordinator (Q-2) | not tested; forbidden for the observer: `run-use` is a forbidden argv (Task 6) |
| Whether `ask` writes type `question` (Q-3) | UNVERIFIED; not tested; forbidden for the observer (`ask` is a forbidden verb, Task 6); no R2 behaviour depends on it |
| Message rate on any Run, and `message.id` identity on real traffic, for the Run the owner names (the owner has not named it) | UNVERIFIED; verification task: Task 17 (gated on the owner); the label `bounded best effort; coverage unknown; bursts over 100 rows between reads may be lost` stays |
| Meaning of `delivered_at`, which stayed `null` on every probe row even after a consuming read and acknowledgement (REPORT 2.2, evidence files 08, 11) | UNVERIFIED; the observer never reads it as closure |
| What identifies a human question | Decided 2026-11-11 (OWNER, decision 8): coordinator questions only (type `question`); whether the coordinator agent or a person answers is not recorded by Orca |
| Inbox lease fields, terminal-attribution fields | `inbox` and plain `check` are never run; not tested; forbidden |
| Value set of `projection.nextAction.kind`, and whether any value means "a human must answer" | Raw string, never classified |
| Whether `projection.stage.activity` or `.detail` carries question text; value sets of `stage.*` | Inspector only, sanitized, labelled `worker-reported`; `stage.detail`/`.activity` withheld from the R1 snapshot (`snapshot-export-schema.md`) |
| Meaning of `projection.evidence.durable` beyond presence | Shown raw |
| Whether `page.total` counts historical dispatches ("Showing 2 of 287 Dispatches" suggests it, not proven); semantics of `result.counts` | Labelled `reported T`, never "workers"; counts never summed |
| Whether `worker-list` offers a state filter for active workers. `worker-list --help` lists a `--terminal-state <active\|reclaimable\|retained\|release_pending\|release_unknown\|released>` filter (REPORT 5, Orca 1.4.245-aidev02.9cfecdd30b2a); its behaviour was not run, so it is still UNVERIFIED (REPORT Q-6) | INV-007 accepted risk, `not reobserved` |
| Clock and format of `liveness.observedAt` / `evidence.lastObservedAt` | No per-row STALE; plain age only |
| Per-call timeout value | Measured at the first permitted live read (R0 makes no Orca calls); T5 uses a configured value |
| Whether `terminalState` values `released` and `retained` mean historical | Only those two values are hidden behind `h`; absent or other values are shown raw and never counted active (`rendering-rules.md`) |
| Orca parser support for `--opt=value` | Separate arguments only |
| Which production-integration reading the issue intends | Stricter reading applies until the owner confirms |
| Stack table facts (seed brief, nothing run) | `stack.md` |
| AC-1..AC-10 restated from the seed brief; re-checked against issue-409-body.md:19 and :77-87 on 2026-11-08 | Clause coverage table in `acceptance-tests.md` |
| Snapshot key names checked read-only against Orca 1.4.245 on 2026-11-08; the schema itself is PROPOSED | `snapshot-export-schema.md` |
| Orca reply sender rule and pairing-code scoping (future stage) | `write-back-future-stage.md` |

## Not established, never presented as available

Complete message history (beyond the 100-row window), cross-host ownership joins, admission and revision-pinned evidence feeds, cost/usage accounting, durable event replay, native deep links.
