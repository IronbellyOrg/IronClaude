# Round 1 Advocate: Variant D (devops: deployment, observability, runbooks, SLOs)

## Position summary

Variant D should be the operational backbone of the final spec. It is the only variant that specifies how the poller is rolled out (24 h shadow dry-run), stopped (`DISABLED`), watched (staleness, SLOs reduced from local files) and recovered (exit-code action table, runbook), and its dispatch record resolves every ambiguous state toward "do not launch again" (§7). It is weaker than E on Project reads, weaker than B and C on launch timeouts and binary identity, and weaker than C on identity by node or account ID. The final spec should graft those pieces onto D rather than replace it.

## Steelman per opposing variant

**Variant A (strongest form).** A treats the watcher as a pipeline of replaceable stages behind typed protocols, enforced by an import test (§1, §8, NFR-011), so options B, C or D later replace one module, not the cycle. It is the most careful about configuration: a JSON config file because `tomllib` needs Python 3.11 while the package supports 3.10 (OD-9); `check-config` rejecting a lease under 15 minutes (§7); and `enabled` defaulting to `false`, so a second workspace on the same login is safe unless someone opts in (OD-2). That opt-in default is better deployment hygiene than D's kill switch alone. Its approval check excludes bots both by `type` and by a `[bot]` login suffix (§3). Its rate-limit handling ends the cycle with no state change and a distinct exit 5 (NFR-006), which gives alerting a clean signal.

**Variant B (strongest form).** B grounds every mechanism in a root cause (RC1-RC3, §1.1). It has the best binary safety: it probes `orca-ide` then `orca` and accepts only the `orca-cli` topic, because GNOME `orca` is a screen reader (FR-014, T7). It also verifies that the worktree `origin` is IronClaude before any call (FR-002). Its per-decision audit line carries `approver` and `approval_event_id` (FR-020), the best forensic trail for "who approved this launch". It maps a launch timeout to `unknown` (FR-015), the correct reading of an ambiguous reply. It refuses to enable cron before the live test answers Q6 on permissions (OD-8). Its test kit is the most hardened: `FakeRunner` exits 99 on any unscripted call, and fixtures carry `_assumed_shape` to mark unverified JSON (§8.3).

**Variant C (strongest form).** C is the most rigorous on correctness. Identity is anchored on node and account IDs, which survive renames (§3, §7). The launch slot is consumed and `unknown` committed in one transaction before any external I/O, so no crash point can give a second submission (§7). Missing initialized storage is rejected instead of being silently recreated (NFR-003, §10 "State loss"). Rate limits persist a next-permitted-request time tested with a fake clock (NFR-004). Deployment stays disabled until the narrative-read risk and the session permission policy are accepted (§6). It says honestly that a crash after commit can permanently suppress an issue and accepts that cost (§7).

**Variant E (strongest form).** E has the right cost model. It reads Project membership from each issue's own `projectItems`, so cost scales with candidates rather than Project size, and a Project with more than 100 items still works (FR-008, §5, U-014). It drops untagged and unowned issues before any per-candidate call (FR-004). It enforces a hard per-cycle call cap of 35 (NFR-005) and a daily launch cap of 6 (FR-018), which bounds spend whatever the approval volume. It gives the operator a `reset <N>` verb (FR-023) instead of hand-editing state, and it prunes terminal records after 30 days (NFR-013). Its kill switch matches D's (FR-022).

## Strengths claimed

1. **A rollout plan, not just a feature.** The runbook in §8 (steps 1-6) covers pre-flight (`gh auth status`, `read:project`, `orca` on PATH, worktree exists), label setup, a 24 h shadow `once --dry-run` that compares `would_launch` with expectation, disable and enable, exit and reason codes, and staleness. No other variant has a staged rollout. A has setup text only (§8 "Setup instructions"), B has a live-test checklist (§8.4, F3), and C has a doc outline (§8). U-012 rates this High.
2. **An exit-code table that tells the operator what to do.** §8 maps every code to an "Operator action" (for example, exit 5 means "Inspect and repair the file; never delete blindly", and repeated 75 means a hung cycle). The other variants list codes without actions (A §8, C §8, E FR-023).
3. **SLOs computable from local files.** NFR-013 defines approval-to-`launched` p95 of at most 10 min, at least 99 % of cycles exiting 0/75, and at least 95 % of `launched` reaching `claimed` within the lease. All three come from `audit.jsonl` and `dispatch.json` through a tested helper. SLO (c) is the production detector for R1, the case where the slash command does not run: `claim_not_observed` appears within one lease (§11 R1). FU-4 alerting and FU-5 measurement close the loop (§9).
4. **Every exit path leaves evidence.** FR-020 appends exactly one parseable line on every exit except a crash, and NFR-006 adds `host`, `duration_ms`, `gh_calls` and `rate_remaining`, with no issue text (the `PWNED-TITLE` test). `host` is the only field that makes the same-login, two-workspace hazard (OD-8, T7) visible after the fact.
5. **A safe stop and safe inspection.** `DISABLED` exits 0 before any external call (FR-018), so cron does not start alerting while the poller is paused. `status` is proven read-only: zero calls and unchanged mtimes (FR-021). It also exposes `last_cycle_age_seconds`, and above 900 s the scheduler is down (runbook step 6). Dry-run leaves `dispatch.json` byte-for-byte unchanged (FR-019).
6. **Separate `attempts` and `launches` counters.** A fresh launch requires `launches < max_launches`. `failed` relaunches only while `launches == 0` (§7). This is the cleanest encoding of "retries are allowed only when no session can exist", and it removes the A and B ambiguity over what `attempts` counts (C-007).
7. **Conservative resolution of every ambiguous state.** A `pending` entry found at cycle start becomes `abandoned`/`pending_orphan` (X-002). `unknown` past its lease becomes `abandoned`/`unknown_expired` (C-011). `launched` with no marker becomes `abandoned`/`claim_not_observed` (X-001). Each expiry ends in a terminal state with a named reason rather than a relaunch, which also makes D robust to clock jumps (see A-006).
8. **A corrupt record is never reset.** Exit 5, zero launches, file unchanged (NFR-011), against B's "loads as empty" (NFR-010), which re-opens every issue that has no marker yet (X-003).
9. **Crash-injection acceptance tied to the SLO.** NFR-005 injects a crash at four points and reruns `once` five times, asserting at most 1 fresh launch. The time budget forbids starting a launch after 120 s of a 300 s cadence (NFR-008), so a slow cycle cannot start a session that overlaps the next cycle's reads.
10. **Fixed owner decisions and seed argv kept exactly.** The 12-element argv with `--agent claude` (FR-013), integer-only prompt with a property test (NFR-001), and repo pinning with no `{owner}` (NFR-003). E widens the agent (X-008).
11. **Namespaced labels.** `issue-watch:trigger` and `issue-watch:approved` (OD-1) match the CLI name, so grepping labels, logs and the runbook for one string finds all of them.

## Weaknesses identified in others

1. **A can launch twice after a crash or timeout.** In §7, a `pending` entry found at cycle start becomes "`failed` (`lost_reply`)", and `failed` is retryable after the lease. A crash after the session started therefore gets a second session. The same holds for "`unknown` | ... lease expired | `failed`" (X-002, X-004). FR-018's lock "exits 0 with `outcome=locked`" also hides hung cycles from any exit-code alert.
2. **B relaunches a session that may be running.** §7.3 says "`launched`, `failed` | lease expired ... no marker, attempts left | new launch" (X-001), and "A `pending` entry at cycle start is treated as `launched`" feeds that same path. NFR-010 resets a corrupt file to empty (X-003). R9 has no rate-limit handling, and its 42-call cycle keeps calling into a 403 (X-006). `--label-only` (FR-022) defines a mode that drops two of the issue's own definitions (X-005). With a single verb and "No other verb" (§8.2), the operator has no `status` to inspect state.
3. **C is not testable as written for operations.** Its acceptance criteria are prose ("configuration failure is returned", FR-001) and give no argv, so an implementer must invent the contract (C-010). It has no kill switch, no default state path ("operator-configured", §7) and no runbook steps. Node-ID configuration for labels, Project field and option (§3, §10) makes setup much harder, and C gives no lookup procedure. Its marker check "may inspect bounded comment content" (§6), which brings comment text into the process, against the A/D/E minimization (C-025).
4. **E widens the fixed launch contract and leaves its re-read undecided.** `--agent <agent>` (FR-014) departs from the seed's `--agent claude` (X-008). FR-012 says the record is "deleted or marked `abandoned`", which is not testable as one outcome. A corrupt record is not specified (X-003). The worker-environment refusal rests on an ASSUMPTION that such a marker exists (§6). `~/.superclaude/` is not an XDG state path, so it mixes with installed framework files.
5. **Exit-code drift across all five (X-007).** A lock gives 0, 0, 6, 75 and 5, and a rate limit gives 5, none, 3, 3 and 8. Only D attaches an operator action to each code. The final spec needs one table, not five.

## Concessions

1. **Project reads (C-003).** D's single `item-list -L 100` read fails closed once a Project has more than 100 items (R3), which stops the watcher. Adopt E's per-issue `projectItems` (FR-008).
2. **A launch timeout can give a double launch.** FR-014 maps a timeout or any non-zero exit to `failed`, and `failed` relaunches while `launches == 0`. A timed-out call may still have started a session. Adopt B FR-015 and C §7: a timeout means `unknown`. D's 20 s orca timeout is too short; adopt B's 120 s.
3. **Recovery means hand-editing `dispatch.json`.** Adopt E's `reset <N>` verb (FR-023) and log each reset to the audit file.
4. **Binary and worktree identity.** D only checks that `orca` is on PATH. Adopt B's `orca-cli` topic probe and its `origin` check (FR-002, FR-014).
5. **Approver identity.** D keys approvers on login names. Adopt C's account IDs (§3); see A-003.
6. **The permission gate is advice only.** OD-7 cannot be enforced as written. Adopt the B/C rule that cron stays off until the live test settles the permission mode.
7. **Exit 3 is overloaded.** It covers auth, scope, timeout, rate limit and non-JSON output, so its action column cannot be specific. Split rate limit out (A's distinct code), and add the missing exit-2 and exit-5 cases to the FR-020 test list.
8. **`rate_remaining` has no source.** `gh api rate_limit` is not in the NFR-002 allow-list. Either add it or read the response headers.
9. **Gaps.** D gives no rotation retention for `audit.jsonl`, and NFR-007's whole-cycle fail-closed is too coarse for a candidate-local error. Adopt E's daily cap of 6 (FR-018) and A's `enabled: false` default (OD-2).
10. **SLO (b) can mask a hang.** It counts exit 75 as healthy. Staleness above 900 s partly covers this, but repeated 75s should count against the SLO.

## Shared-assumption responses

- **A-001 QUALIFY:** cron persistence is not proven. Enable only after a pre-flight check confirms that the `coder_script` survives a workspace restart; staleness (runbook step 6) detects the loss.
- **A-002 QUALIFY:** that `/sc:issue --claim` runs in the launched session is gated on the FU-1 live test. SLO (c) and `claim_not_observed` detect a failure in production.
- **A-003 QUALIFY / partial REJECT:** label renames fail closed, which is acceptable. Logins are not stable: GitHub releases renamed logins for reuse, so key approvers on account IDs (C §3).
- **A-004 ACCEPT:** a single workspace per login is a stated limit. Add `host` to every audit line (NFR-006) and A's `enabled: false` default.
- **A-005 ACCEPT:** only assigned issues are considered. Count `unassigned` skips in the audit line so that they are visible.
- **A-006 QUALIFY:** clocks are assumed sane. In D, lease expiry never permits a relaunch (§7), so a clock jump only delays work. A and B need an explicit guard.
- **A-007 QUALIFY:** `flock` works only on a local filesystem. The pre-flight check must refuse a state directory on NFS.
- **A-008 QUALIFY:** bot exclusion uses `type == User` plus the allow-list, plus A's `[bot]` suffix check. Residual risk T3 remains.
- **A-009 QUALIFY:** that the claim marker appears within one lease has not been measured. A miss gives `claim_not_observed`, not a double launch. Tune the lease via FU-5.
- **A-010 QUALIFY:** the allow-list file is trusted. Refuse one that is group- or world-writable.

## Per-point positions

| Point | Level | Superior variant | Confidence % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | D | 60 | Runbook and action table make §8 the deployable section |
| S-002 | L1 | NONE | 50 | Section order is cosmetic; content decides |
| S-003 | L2 | HYBRID | 60 | D's verbs plus E's `reset` (FR-023) |
| S-004 | L2 | HYBRID | 55 | D's flat modules plus A's protocol seams only where options B-D need them |
| S-005 | L3 | D | 60 | One state machine table with a terminal reason per expiry (§7) |
| S-006 | L1 | NONE | 50 | Heading style has no operational effect |
| S-007 | L1 | B | 50 | Root-cause framing (§1.1) explains why each control exists |
| S-008 | L1 | B | 55 | `FakeRunner` exits 99 on any unscripted call (§8.3) |
| C-001 | L3 | D | 60 | `DISABLED` exits 0 before any call (FR-018) |
| C-002 | L3 | HYBRID | 80 | D's audit on every exit plus B's `approver`/`approval_event_id` |
| C-003 | L3 | E | 75 | Per-issue `projectItems` survives Projects over 100 items (FR-008) |
| C-004 | L3 | HYBRID | 60 | D's counters plus E's daily cap of 6 |
| C-005 | L3 | HYBRID | 70 | D's lease rules plus timeout as `unknown` from B/C |
| C-006 | L3 | E | 65 | Pre-filter before per-candidate calls (FR-004) cuts cost |
| C-007 | L3 | D | 60 | Separate `attempts` and `launches` (§7) |
| C-008 | L3 | HYBRID | 70 | A's distinct rate-limit exit plus C's persisted next-permitted time |
| C-009 | L3 | C | 55 | Missing initialized storage is rejected, not recreated (NFR-003) |
| C-010 | L2 | HYBRID | 75 | D's argv and testable criteria plus B's `orca-cli` probe |
| C-011 | L3 | C | 65 | Slot consumed and `unknown` committed before I/O (§7) |
| C-012 | L3 | NONE | 60 | No variant measures the claim latency; defer to FU-5 |
| C-013 | L3 | HYBRID | 65 | D's XDG path plus A's pre-flight `check-config` |
| C-014 | L2 | B | 70 | Worktree `origin` check before any call (FR-002) |
| C-015 | L3 | HYBRID | 70 | D's SLOs plus E's call cap of 35 (NFR-005) |
| C-016 | L3 | HYBRID | 65 | D's `status` plus E's 30-day pruning |
| C-017 | L2 | D | 70 | Shadow dry-run and staged enable (§8 steps 3-5) |
| C-018 | L3 | D | 60 | Exit-code table with an operator action per code |
| C-019 | L2 | HYBRID | 70 | Integer-only prompt (D NFR-001) plus B's fixture shape markers |
| C-020 | L2 | HYBRID | 70 | D's crash injection (NFR-005) plus B's hardened fakes |
| C-021 | L2 | A | 60 | `enabled: false` default (OD-2) protects a second workspace |
| C-022 | L2 | HYBRID | 70 | Account-ID approvers (C) plus the bot suffix check (A) |
| C-023 | L2 | HYBRID | 60 | Enable gate from B/C plus D's pre-flight runbook |
| C-024 | L3 | D | 55 | Namespaced `issue-watch:*` labels (OD-1) |
| C-025 | L2 | HYBRID | 60 | Marker check by presence only (A/D/E); no comment body in process |
| X-001 | L3 | D | 65 | `launched` without marker becomes `abandoned`, not relaunched |
| X-002 | L3 | D | 60 | Orphaned `pending` becomes `abandoned`/`pending_orphan` |
| X-003 | L3 | D | 70 | Corrupt record: exit 5, file unchanged (NFR-011) |
| X-004 | L3 | C | 75 | C commits `unknown` before I/O; D's lapse to `abandoned` is the same outcome |
| X-005 | L3 | D | 65 | No `--label-only` mode; both issue definitions kept |
| X-006 | L3 | HYBRID | 65 | A's halt on rate limit plus C's persisted backoff |
| X-007 | L2 | HYBRID | 60 | One exit table: D's actions plus A's distinct rate-limit code |
| X-008 | L2 | D | 70 | Seed fixes `--agent claude` (FR-013); E widens it |
