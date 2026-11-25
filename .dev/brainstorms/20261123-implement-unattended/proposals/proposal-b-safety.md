# Proposal B: safety and resume (/sc:implement --unattended)

Read: seed brief, implement command, skill and refs, WORKER-CONTRACT.md, four sibling sections, test_worker_contract.py. UNVERIFIED: test_implement_*.py, hooks, archive_workspace.py, how `issue-pipeline plan-hash` digests.

## 1 Switch and grammar
- `--unattended` counts only as a standalone token outside quoted text (an inline prompt is quoted). Added to Wave 0 step 1 known options.
- Exactly one report directory: `--report-dir <dir>` (implement has no directory output flag). None or two: no work, chat-only WC-4 error.
- `--force` stays E-NO-RULING (blocked). Removed flags stay E-LEGACY (failed). No person-mode flag exists for implement, so none is refused. `--skip-final-review` is allowed but caps the run at partial (managed: E-ARCHIVE-BLOCKED as today).
- NEW optional `--plan-sha256 <hex>` (section 6). Mode never reads Orca or launch level.

## 2 Report directory
Checked before any write, and again after Wave 0 resolves run dir or package. Common rules (not in `.git/`, `.codegraph/`, distributable `.claude/` folders, creatable) plus NEW:
- realpath inside `<checkout>/.dev/`, no `..`, no symlink component. Reason: revert domain rule 6 (retry.md) spares only `.dev/` paths; outside it a revert `rm -f`s untracked report files (handoff, nested impact).
- not inside `.dev/implement/<slug>/` and not inside any `.dev/tasks/to-do|done/<slug>/` package (the package moves on archive, so report_path rots), and it contains neither source nor ledger.
- the mode is the only writer; a task executor never writes there (else `files=` would put it in a revert domain).
- Contract written to a temp name then renamed. At start an existing contract moves to `return-contract.prev.yaml` (NEW) so a crash never leaves a stale status looking current.

## 3 Contract and outcome map
WC-4 fields; `report_path` = ledger path (managed: the actual to-do/done path after the helper). Extra NEW keys: `tasks_complete`, `tasks_total`, `halted_task`, `plan_sha256`, `plan_approval` (`not-asserted|matched`), `staging: deferred`, `unresolved: []`. `artifacts`: notes files, `codegraph.md`, nested contracts; paths git ignores are left out (WC-4).
The status is derived from a fresh ledger parse at exit, never from session memory.
- succeeded: all complete and compliant, FINAL pass or N=1, managed archived/already-archived, repeat of finished work.
- partial (each cause in `unresolved`): task completed by an earlier Ruling; legacy FINAL `issues`; `--skip-final-review` with N>1; safety-scan hit; extras cut by the cap.
- blocked, reason carries the code: E-HALT-QA (any halt reason), E-NO-RULING, E-ARCHIVE-BLOCKED. This matches freeze item 1.
- failed, reason = code: E-RESUME-NEEDED (`reason=<r>`), and every input or integrity STOP (E-NO-SOURCE, E-SOURCE-MISSING, E-NO-TASKS, E-NO-AC, E-LEGACY, E-LEDGER-*, E-MANAGED-*, E-PLAN-CHANGED, E-ARCHIVE-MARKER).

## 4 Each point that asks a person
- Ruling halt, E-HALT-QA: blocked; `blocked_question` is the Ruling request (task, blocking finding, proposed acceptance, why, cost). For no-snapshot, head-moved, no-evidence it asks fix or resume, since a Ruling is ineligible. The mode never writes a Ruling line, for any input.
- Resume rows P, H: refused before any write. They append blocked/halt lines and start an operator review, which retry.md says automation never starts. Report blocked E-HALT-QA for the first non-complete task; ledger untouched. Row R (an eligible Ruling already on disk) runs; so do 1, S, V, X, O, B.
- E-RESUME-NEEDED: failed, no wait; the coordinator may re-run once (freeze exception).
- E-ARCHIVE-BLOCKED, FINAL issues: blocked. `.archiving` marker: failed E-ARCHIVE-MARKER, never cleared.
- Follow-up print: lines go to notes; no offer. Scan hit: partial. Missing scan tool: one line, no change.
- Parallel batches: forced sequential, markers ignored. Batch members get no ladder and halt `batch`, which needs a person; sequential tasks get A3 to A5.
- Long extras: background run, waits of at most 4 minutes (WC-10), NEW cap 20 minutes per extra; on the cap kill, record `skip` (ledger grammar has no timeout value), partial.
- Nested: `sc:impact-protocol` gets `--unattended --output-dir <report-dir>/nested/impact-<n>/`; blocked/failed counts as `graph:absent` as today. Optional managed delegates (adversarial, reflect) are skipped and noted.
- Staging: the three `.dev/tasks` staging lines do not run (WC-9); snapshots, refs, revert and the archive helper still do.

## 5 Crash and re-run
The ledger is the only resume state; the contract is output. No contract after a crash gives WC-5 failed, and the coordinator reads the ledger. The next Task (new report dir, WC-6) resumes through the existing rows; Q0 start reuse, `revert-<k>.done` and sweep refs already make that idempotent. A truncated last line is E-LEDGER-CORRUPT, never repaired. A finished plan re-run answers `already complete` and succeeds with no ledger write. No lock exists (ledger.md precondition); it stays so, because a crash would orphan any lock, and WC-11 plus the freeze rule carry single-writer.

## 6 Plan approval (O3)
Implement never infers approval. Absent flag: `plan_approval: not-asserted`, run proceeds (O3 = no). O3 = yes: the brief's WC-17 line makes the worker ask and run check-approval before the `Command:` line; the coordinator also passes `--plan-sha256` (sha256 of the plan file bytes; managed already pins that in `PLAN:`). A mismatch before the first start line stops failed E-PLAN-CHANGED with nothing written; this closes the gap between approval and execution. Both answers work with no other change.

## 7 Risks, ranked (mitigation; test)
1. Operator review or Ruling started by automation (rows P/H gate; no Ruling write). Test: fixtures with blocked/halt last record, assert ledger bytes unchanged and blocked contract; text pin.
2. Contract status disagrees with ledger, bypassing the freeze. Test: table-driven code-to-status check over the STOP table and halt reasons; fixture ledger versus contract.
3. Report dir in a revert domain or package. Test: one refusal case per rule in section 2.
4. Staging, commit or push slips in. Test: the write-verb audit; the new section holds no write verb; reclassify the three `deferred:P4` entries, whose keys are exact line text; artifacts clause bans "git add".
5. Approved plan edited before start. Test: hash match and mismatch fixtures.
6. Long extras stall the worker. Test: section pins the 4-minute and cap wording.
7. Double dispatch, no lock. Residual. Test: WC-11 text pin.
8. Stale installed or plugin copies trip the brief guard. Test: `make verify-sync`, plugin mirror.
Pins to add in test_worker_contract.py: UNATTENDED_EXPECT `implement` (flags `--report-dir`, `--plan-sha256`; nested `impact`), EXPECTED_NESTING in both copies, the 23-entry count, a P4 set, no `src/superclaude/` or `git add` in the section, and a `nested/impact-` line with `--unattended`.
