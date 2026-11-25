# Diff Analysis: unified architecture and staged migration, three variants

## Metadata
- Generated: 2026-11-20 (Step 1 of the adversarial protocol, run by the orchestrating session)
- Variants compared: 3. V1 = `variant-1-opus-architect.md` (322 lines, target-architecture-first). V2 = `variant-2-sonnet-analyzer.md` (410 lines, evidence-and-sequence-first). V3 = `variant-3-haiku-backend.md` (356 lines, operations-and-failure-first). All paths under `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/`.
- Total differences found: 30. Categories: structural (4), content (15), contradictions (6), unique contributions (14, listed separately and NOT counted in the debate denominator), shared assumptions (5 promoted UNSTATED, plus 5 STATED or already settled).
- Debate taxonomy tag per point: L1 surface, L2 structural, L3 state-mechanics (auto-tagged by signal words: state, guard, invariant, ordering, ack, transition, concurrency).
- Where the three variants AGREE (not diff points): all three bind workers at guard level F because no built level allows commit without push (`launch-level-guard.sh:785-803`); all three let the coordinator commit after `worker_done` and push only on a person's go; all three let the revert of PR 682 win over D05 and reuse the restored `brief.py` marker slot; all three run `issue-watch run-all` over per-repo JSON in `issue-watch.d/` with Clay's key names and fail-closed defaults; all three keep `Status` and `Approved` reads and leave the Pipeline field dormant; all three set `max_in_flight` to 1 first; all three choose "package copy plus parity test" for the plan check; all three make the merge path ONE tested unit after the substrate; all three order lane 1 (PR 693, PR 690, rule C1) before the revert, and the revert before planb and before the adapted PR 686; all three carry "narrows, not closes" wording; all three mark the live probes (U5, U25, U28, U3, tui-idle, worker binding) UNVERIFIED.

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity | Level |
|---|---|---|---|---|---|---|
| S-001 | Stage granularity | 15 stages S0-S14, one PR each | 21 stages S0-S20 (watcher split into three PRs, skill before merge path) | 11 rows S0-S10 in one table; each row bundles several PRs | Medium | L2 |
| S-002 | Owner-action format | 22 items, each answer on its own line saying what it does | 18 numbered items with the answers inline | grouped bullets, telegraphic ("Hold 686/690: drafts stay.") | Medium | L1 |
| S-003 | Diagram | end-state flow with an "owner's chat" lane and the coordinator's eight steps | same flow with status tags [B] built, [P] planb only, [C] Clay PR, [N] not built, [D] design only | six-line text flow plus an at-least-once paragraph | Low | L1 |
| S-004 | Interface table | 26 rows, all with built/not built | 27 rows, numbering has gaps (no row 4, no row 22), file:line cites | 24 rows with host-specific absolute paths | Low | L1 |

## Content Differences

| # | Topic | V1 approach | V2 approach | V3 approach | Severity | Level |
|---|---|---|---|---|---|---|
| C-001 | Who claims (K1) | End state: the coordinator claims (`start_mode: wake`); built poll-launched claim is the default until the coordinator passes live tests | The poll claims at level none as built; wake is written after the claim marker shows ("claimed, take over") | Same as V2 (poll claims, durable adoption wake after the marker) | High | L3 |
| C-002 | Where wake, ack and issue state live (K5) | One per-repo state folder OUTSIDE any git checkout (`~/.local/state/superclaude/issue-watch/<owner>__<name>/`); `.dev/coordinators/` holds only human-readable records | Inside the project: `.dev/coordinators/wakes/` and `state/`, git-ignored, in the `Coordinator` worktree; `records/` tracked on `coordinators` | Inside the Coordinator worktree `.dev/coordinators/{runtime,wakes,records}/` | High | L3 |
| C-003 | Meaning of the worker-binding switch (K14) | `BOUND_WORKERS_PROVEN = False`: real issues run "unbound and flagged", a person gives a go | `WORKER_BINDING_ENFORCED` false keeps real issues off until the probe (S15), or starts them only after a throwaway run (K14 text) | enabled stays false until a live F probe proves binding; no real issue before | High | L3 |
| C-004 | Direction of the plan-check pair (K8) | `plan_body.py check` is the reference; package copy `issue_watch/plan_check.py` follows | Same as V1 | Package pure checker is canonical; the installed script is the parity-tested copy | Medium | L2 |
| C-005 | Watcher state on the screen (K10) | The sweep copies `issue-watch status --all --json` into a top-level `watcher` block; observer and report read only the sweep JSON | Observer reads `issue-watch status --json` (extended) next to the sweep JSON; sweep untouched | Observer "watcher panel" reads the status JSON; sweep untouched | Medium | L2 |
| C-006 | When sweep fields and saved JSON ship | S10, after the revert and planb (lane 3, beside S9) | S5, early and independent of lanes 1 and 2 (matches D14 lane 3) | S8 (O6), with the observer work | Medium | L2 |
| C-007 | How PR 686 is cut down | One adapted draft (S9) that also carries store-state union, `start_mode`, config v2, parity test, reasons table | Three PRs: plan-check and skip reasons (S11), keys and `owner/name` and `status` (S12), wake-transport-only 686 behind `wake_enabled` default false (S13) | One adapted PR 686 (S5) | Medium | L2 |
| C-008 | Where the coordinator skill starts | S11 substrate plus a person-opened skill, no merge verb | S14 substrate; S15 skill WITHOUT merge path ("PR ready, person merges by hand"); S16 merge path as ONE unit (stated deviation from D15) | S6 runner; S7 merge unit; S8 wake, cap, restart, F binding | Medium | L2 |
| C-009 | Where the merge go entry is stored | `<state folder>/goes/` (outside git) | `.dev/coordinators/records/go/<..>.json` on the TRACKED `coordinators` branch | `runtime/asks/<key>.json` (ignored) with quotes in `records/` | Medium | L3 |
| C-010 | Crash and idempotency depth | Named tests for M1 (ack after state file) and M2; no replay design for a crash between claim marker and wake write | Same level; states `woken`, `acked` added | Explicit per-boundary design: save claim attempt before launch (built), unknown receipt never relaunched, outbox replay of the adoption wake, retarget with linked new id, restart budget survives crash, integrity rules (exclusive create, temp+rename, fsync file and parent dir) | Medium | L3 |
| C-011 | D16 (process to prevent a repeat) | Left out ("no VERDICT.md") | Built in: S0 ruleset recommendation, D16 decisions as owner items 2 and 4, throwaway test | Mentioned as an unbuilt proposal only | Medium | L2 |
| C-012 | Numbers with no source (go expiry, in-flight expiry, binding timeout) | Left to the owner (asks) | Recommends 24 hours for both, labelled UNVERIFIED | Left to the owner; 60 seconds binding timeout and round cap 3 as unmeasured proposals | Low | L1 |
| C-013 | `hold:backlog` label creation against NG-2 | Init creates labels (D09) | Notes it is a GitHub write made by a person-run `repo-init` on the owner's go, never by the poll or cron | Init alone creates labels | Low | L2 |
| C-014 | Per-repo keys beyond Clay's | `start_mode`, `coordinator_autostart`, schema_version 2 | `coordinator_session` (default `COORD-<RepoName>`, `ORCH-IronClaude` until Coder 516), `wake_enabled` | none added; `schema_version` 1 | Low | L2 |
| C-015 | Rollback caution | "readers ignore unknown keys (pinned in the contract note)" | Warns the loader may reject unknown keys (`cycle.py:76-83`, UNVERIFIED for per-repo files), so a rollback must also remove the new keys | Rollback by disabling consumers and keeping files | Low | L3 |

## Contradictions

| # | Point of conflict | V1 position | V2 position | V3 position | Impact |
|---|---|---|---|---|---|
| X-001 | Does a poll-launched claim session in the `Coordinator` worktree break "one worktree, one live agent" (D07 defect)? | Yes: removed only by having the coordinator run the claim in its own session | Partly: kept at cap 1, "coordinator started only after the claim result file exists" | Partly: "standing Coordinator stays read-only while its claim session runs" | High: decides K1 |
| X-002 | May a real issue run with an UNBOUND worker before the live probe? | Yes, "unbound and flagged", on a person's go (D05 item 3 wording) | No: real issues stay off until the probe (S15, S20) | No: enable only after proof (S9) | High: the owner's G2 sentence says no other issue before binding |
| X-003 | (inside V2) Does `WORKER_BINDING_ENFORCED = false` start a real-issue worker after a throwaway run and flag it (K14), or keep real issues off (S15)? | n/a | both statements appear | n/a | Medium |
| X-004 | Which side is the "single definition" of the plan check? | `plan_body.py` | `plan_body.py` | package module | Medium: D12 and D15 R-2 say `plan_body.py` |
| X-005 | Are merge go entries tracked in git? | No | Yes, on the shared `coordinators` branch ("records tracked"), though each entry is one-shot with a `used` flag | No (ignored runtime) | Medium: a mutable tracked file is pushed or conflicts |
| X-006 | Does the sweep read the watcher? | Yes: new `watcher` block, so the sweep's read allow-list grows by one subprocess | No (D11: the sweep has no GitHub call and a fixed read list) | No | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V1 | Per-repo `start_mode: claim | wake`: a rollback to the built claim path by one config value | High |
| U-002 | V1 | Machine state outside git, human records on the `coordinators` branch (clean split) | High |
| U-003 | V1 | `coordinator_autostart` (script start only on a recorded owner go) and `coordinator_absent` reason (K11) | Medium |
| U-004 | V1 | Named state `waiting_reapproval` outside the cap with expiry (meets C-INV-1 and C-INV-2) | High |
| U-005 | V1 | Five extra conflicts (autostart, close after merge, cron timing, restart before Coder 516, hand-back round 2) | Medium |
| U-006 | V2 | Ten mechanical merge checks MC-1..MC-10 with proposed test names, including NG-2 argv test (MC-8) and the reasons-table pin (MC-10) | High |
| U-007 | V2 | S6 revert dry run with a recorded master sha, `git apply --check` of planb's 1,767-line patch, and a per-host diff rule before any `superclaude install` | High |
| U-008 | V2 | Sweep fields and saved JSON early (lane 3 is independent) | Medium |
| U-009 | V2 | `wake_enabled` default false so no wake exists before a coordinator does (avoids three resends then exit 7 for nothing) | Medium |
| U-010 | V2 | `coordinator_session` key so the name before Coder 516 is a config edit | Medium |
| U-011 | V3 | Integrity rules: one stable action id per write, exclusive create, temp+rename, fsync file and parent, reject symlink and oversize, lock order, producer releases before delivery | High |
| U-012 | V3 | Outbox replay for "claim marker seen, wake not yet written" and a no-second-claim test for a lost launch receipt | High |
| U-013 | V3 | Merge result uncertain: reconcile exact head before any reuse of a go; restart never restores a consumed go | Medium |
| U-014 | V3 | Crash tests per persistence boundary and a failure table with the required test per row | High |

## Shared Assumptions (AD-2)

| A-NNN | Agreement source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All three put one long-lived Claude session per project in a `check --wait` loop | A coordinator session survives context exhaustion and compaction between wakes; a restart can resume from files alone (contract rule S6 says exhaustion is a real state) | UNSTATED | yes |
| A-002 | All three cap at 1 and say "workers get separate worktrees" | `worker-start` always gives each worker its own worktree (V1 notes it as unobserved in RK-11; V2 and V3 rely on it) | UNSTATED | yes |
| A-003 | All three have an agent "record each owner answer" from S0 on | Before any coordinator exists (S0 to S10) there is a place and format for recording owner answers, and later sessions read them (none names it; V2 and V1 name only `records/` of a coordinator that does not exist yet) | UNSTATED | yes |
| A-004 | All three give one coordinator per project and one cron on one host | A "project" is one repository checked out once on one host; monorepos, forks and a second host are out of scope | UNSTATED | yes |
| A-005 | All three: `/sc:pr-submit` runs in a top-level session after the person's go | A script-started (depth 0) coordinator is a top-level session where `/sc:pr-submit --monitor 3` may run, though D06 allows `/sc:pr-submit` only in an "ordinary top-level session" and never as an Orca worker | UNSTATED | yes |
| A-006 | All three | The launch guard F level lets `/sc:implement` complete without commits (ledger staging done by the coordinator) | STATED (V1 RK-9, V2 R19) | no |
| A-007 | All three | Coder 515 (cron) and 516 (`Coordinator` worktree) land | STATED | no |
| A-008 | V2, V3 | PR 693's launch result file gives a "claim ended" signal (shape UNVERIFIED) | STATED (V2 R9) | no |
| A-009 | All three | Same host and one login for poll, coordinator and cleanup | STATED in V3, implied in V1 and V2 | no |
| A-010 | All three | Orca idle detection, mailbox from outside a Run and the tag spike work or degrade to the file pull | STATED (U5, U25) | no |

## Summary
- Total structural differences: 4
- Total content differences: 15
- Total contradictions: 6 (X-003 is internal to V2)
- Total unique contributions: 14
- Total shared assumptions surfaced: 5 promoted (UNSTATED 5, STATED 5 not promoted, CONTRADICTED 0)
- Debate denominator: 4 + 15 + 6 + 5 = 30 points. Taxonomy tally (auto-tag priority L3 > L2 > L1; X rows and A rows tagged by the same signals: X-001, X-002, X-003, X-005, A-001, A-005 are L3; X-004, X-006, A-002, A-003, A-004 are L2): L1 = 4 (S-002, S-003, S-004, C-012), L2 = 14, L3 = 12. Every level has coverage.
- Highest-severity items: C-001, C-002, C-003, X-001, X-002.
- Similarity check: the three variants differ on 30 points of about 120 comparable items (25 percent), above the 10 percent skip threshold: debate proceeds.
