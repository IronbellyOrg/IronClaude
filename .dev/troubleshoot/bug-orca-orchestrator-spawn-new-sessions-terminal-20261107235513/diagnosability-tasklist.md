# Diagnosability Tasklist
**Issue**: Orca orchestrator continues to spawn new sessions via a new terminal session shortcut instead of a new claude session shortcut. Resulting in empty terminals and a waiting orchestrator
**Verdict**: partial  **Complexity**: non-trivial  **failing_component**: none (not localizable)  **Round**: 1 of 3  **re-run permitted**: unknown  **discriminator-required**: yes  **capability-verdict**: n/a
**branch**: ironbelly/fix-flaky-parallel-thread-test  **repro-venue-id**: orca-orchestrator-spawn-session-surface

## Emitter search
emitters-found: 1 (Orca daemon log `startup-command-delivery` records hasCommand true/false per tab, ~/.config/orca/logs/daemon.log; it carries no caller)
already-read-files: 3 (daemon.log, main.trace.ndjson, the orchestrator transcript 1779a921-...jsonl)
usable-capture-routes: 1
Route 1: Claude transcripts under ~/.claude/projects record every orchestrator Bash call (`tool_use` with the full `orca ...` command and timestamp). That is the actual datum (which command created a tab) at an existing artifact sink; no production source edit needed. Join key: daemon.log session start time (within 5 s) against the transcript tool_use timestamp. Permission to run new probes: unknown (nothing refuses a re-run, nothing grants one); reading existing artifacts is allowed and was done.
Excluded: main.trace.ndjson (git spans only, no terminal creation spans); `orca terminal list` (live state only, no creation record). Production-source emit calls: none apply (the actor is a model, not source).

## Discriminator rows
core-rows=5, pack-rows=0, total-rows=5. refs/primitive-differential.md is not applied: its probe forms classify source-code primitives (read/parse and similar), and none of P1-P4 is a code expression. Rows below are custom, one per surviving producer plus a control row.

| ID | Role | Claim | Observable and probe (read-only, parent-run) | value-if-claim-true | value-if-false | Outcome mapping | Provenance | State |
|----|------|-------|-----------------------------------------------|---------------------|----------------|-----------------|------------|-------|
| M-P1 | core | P1: `orca worktree create` with no `--agent` leaves only a plain default terminal | daemon.log sessions for worktree install-core-stale-warning (created by `orca worktree create ... --no-parent` at 2026-11-07T05:36:13Z in transcript 7fd4f558-...jsonl) | one session-created, hasCommand=false, no command-bearing session | a command-bearing session exists | consistent / refuted / inconclusive | daemon.log lines 2026-11-07T05:36:16.234Z | OBSERVED: true-case value (hasCommand=false, no other session). Consistent with P1; it shows P1 makes an empty tab, not that any orchestrator waited on it. |
| M-P2 | core | P2: an orchestrator ran `orca terminal create` to start an agent | jq over all ~/.claude/projects transcripts for Bash tool_use commands matching `orca .*terminal create` (excluding `--help`) | at least one such call followed within 10 s by a daemon hasCommand=false session | zero such calls | consistent / refuted / inconclusive | transcript scan in Wave 1 (tier1-observation.md O4) | OBSERVED: zero real calls in the scanned transcripts. Refutes P2 for those transcripts only; transcripts not on this host, or deleted, are unobserved. |
| M-P3 | core | P3: the empty tabs come from the Orca UI (Mod+T / New Terminal), not from an agent | for each daemon hasCommand=false start in the last 24 h, check whether any transcript Bash call to `orca` falls within 10 s before it | no agent call within 10 s | an agent call within 10 s | consistent / refuted / inconclusive | daemon.log vs transcripts | PENDING for the full 24 h window (could-not-run: artifact-only, join not executed). Spot check done for 2026-11-07T23:52:18Z: no Bash call to `orca` in any transcript active after 23:30Z fits (observed absence, same limits as M-P2). |
| M-P4 | core | P4: a `worker-start`/`agent launch` with `--agent claude` started a tab where Claude never came up | `orca orchestration worker-list --run <run> --json` rows with `unverifiable`/`stale_status` and `orca terminal read --terminal <handle>` of each | tab screen shows a bare shell prompt | tab screen shows Claude Code | consistent / refuted / inconclusive | live Orca state | PENDING (could-not-run: no failing run named; 4 workers show `unverifiable stale_status`, their tab titles all end "· Claude Code" which argues against P4 but does not read the screen). |
| M-C | control | passing arm: coordinator 1779a921 spawns via `worker-start --agent claude` | titles of the resulting tabs | each title ends "· Claude Code" | a plain title | consistent / refuted / inconclusive | `orca terminal list` 2026-11-08T00:00Z | OBSERVED: consistent. CONTROL-PROOF: unknown (the producing line is a transcript tool_use, not a `file:line`; control_unproven). |

Preregistered measurement to settle the user's actual case: M-USER (pending, needs input) — claim: the reporter's failing orchestrator ran command X. Observable: that orchestrator's session id or tab; probe: list its `orca` Bash calls from the transcript. value-if-P1-true: a `worktree create` without `--agent` followed by a `worker-start --terminal`/`dispatch --inject` into the default tab or by a wait; value-if-P2-true: a `terminal create` call; value-if-P3-true: no `orca` call at all. State: PENDING (could-not-run: failing orchestrator not identified).

M-QE (appended in Wave 3 step 4.5; pair P1 vs P4, from the quality-engineer card with the calibrator's defects fixed). Core, pending (could-not-run: failing worktree not identified; artifact-only). Claim A: the empty tab is the P1 seed and a started Claude worker tab exists beside it. Claim B: the worker never came up (P4/recovery shell). Observable (one boolean): in `orca terminal list --json` for the affected worktree, a tab whose title ends "· Claude Code" exists. Do not use presence of a `worker-<taskId>` title: it is set at create time, before readiness (worker-topology.ts:73). A supplementary, non-boolean confirmation: `orca terminal read --terminal <that handle>` should show a Claude Code screen rather than a bare shell prompt; a mismatch is recorded as a note, not folded into the boolean. Probe: read-only `orca terminal list --json`. Reference-context value: `true` (observed reference arm: worktree liveness-v1-contract, tab term_8c37967b titled "liveness-v1-contract-1107-211733-7356 · Claude Code", worker verdict `live`; `orca terminal list --json` and `orca orchestration worker-list` at 2026-11-08T00:00Z; tier1-observation.md O3). Non-reference counter-case (a failing-side style context, not the reference): install-core-stale-warning reads `false` (plain tab only; no worker was started there). | true | A consistent, B refuted for that worktree | | false | A refuted for that worktree, B consistent (a worktree with no worker also gives false) | Complete captures only; an empty or errored capture is unobserved. Equal outcomes for other producers (P2, P3) are non-discriminating. Provenance: live Orca state. Candidate set status: split-pending (P1 vs P4 not yet discriminated; P2 and P3 not excluded).

## Bracket
Not triggered (no threshold measurement).

## Fix candidate
Proposal only, not authorized, not applied. Rows M-P1 and the install check (O5) support two enabling changes, neither of which depends on which producer the reporter hit: (a) get the #415 rule into ~/.claude/CLAUDE.md. CORRECTED in Wave 3 (the system-architect calibration found the earlier wording wrong): a plain `superclaude install` SKIPS an existing ~/.claude/CLAUDE.md (install_core.py:70-72), and the pipx package on this host (built 2026-11-05) predates #415. Delivery needs the package reinstalled from the fork, then `superclaude update` (or `install --force`), which OVERWRITES that file: diff it against src/superclaude/core/CLAUDE.md first and keep local edits; (b) add `--agent claude` guidance next to CLAUDE.md:308. Paired verification: grep -c "Orca session launches" ~/.claude/CLAUDE.md returns 1 after (a); a fresh orchestrator started from the repo creating a worktree for a Claude task issues `worktree create --agent claude` or `worker-start --worktree new-top-level --agent claude`.

## Hard Constraints
- INVOCATION SITES only; ADDITIVE only; each task is annotated `# Diagnosability-tasklist instrumentation: revert after defect closed.`

## Implementation tasks
### Task 1: Name the failing orchestrator (task type 5, fail-closed observed-value emission)
- Invocation site: the next occurrence, at the operator's shell, not production source. Run once: `jq -r 'select(.type=="assistant") | .message.content[]? | select(.type=="tool_use" and .name=="Bash") | .input.command' <failing-orchestrator transcript>.jsonl | grep -E 'orca (terminal|agent launch|worktree create|orchestration worker-start)'` and record `spawn-command=<first matching line>` or `spawn-command=unobserved` if no transcript is found. Links M-USER, M-P2, M-P3. Rationale: answers Where/Why (which command made the tab). Verification: the line names one of the four producers. Rollback: none (read-only).
### Task 2: Record the caller of each Orca tab start (task type 4, artifact capture)
- Invocation site: the orchestrator's own launch wrapper (the orchestrator prompt/skill), by always passing `--title "<run>-<role>"` to any `orca terminal create` it runs, so daemon/tab titles show who made a tab. Links M-P3. Rollback: remove the flag. Not a source change.

## Verification
M-P1, M-P2 and M-C observed (see rows); M-P3, M-P4, M-USER pending.

## Rollback
Tasks 1 and 2 add no persistent change beyond the title flag.

## Patch-round counter
Identity: branch `ironbelly/fix-flaky-parallel-thread-test`, venue `orca-orchestrator-spawn-session-surface`. Authoritative value: 1 (.dev/troubleshoot/diagnosability-rounds.json); snapshot at <output-dir>/diagnosability-rounds.json.
