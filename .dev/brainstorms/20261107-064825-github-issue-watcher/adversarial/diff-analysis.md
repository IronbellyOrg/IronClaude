# Diff Analysis: Requirement Specification Comparison

## Metadata
- Generated: 2026-11-07T12:23:13Z
- Variants compared: 5 (variant-A, variant-B, variant-C, variant-D, variant-E), against `seed-brief.md`
- Total differences found: 56 (structural + content + contradictions + unique); shared assumptions listed separately: 10
- Categories: structural (8), content (25), contradictions (8), unique (15), shared assumptions (10)
- Levels (S, C, X, A rows): L1 (5), L2 (14), L3 (32)
- Section references (§N) are to each variant's own numbered sections.

## Structural Differences

| # | Area | Variant A | Variant B | Variant C | Variant D | Variant E | Severity | Level |
|---|------|-----------|-----------|-----------|-----------|-----------|----------|-------|
| S-001 | Requirement notation (§4-§5) | Bullets with Given/Then sub-bullets | Tables with an acceptance column | Prose FRs with "Acceptance:" lines; no code-level argv | Bullets with *GWT* / *Test* lines | "shall" bullets with AC; YAML frontmatter | Medium | L1 |
| S-002 | Requirement counts (§4, §5) | FR-001..020, NFR-001..011 | FR-001..022, NFR-001..013 | FR-001..013, NFR-001..009 | FR-001..021, NFR-001..013 | FR-001..023, NFR-001..014 | Low | L1 |
| S-003 | Lens-specific framing | Pipeline of replaceable stages behind typed protocols (§1, §8, NFR-011) | Root-cause table RC1-RC3 (§1.1) | Readiness-scoring table A 2/8, B 1/9, C 0/10, D 2/8 (§2) | Operator runbook and SLOs (§8, NFR-013) | Call-budget arithmetic in prose (§5) | Medium | L2 |
| S-004 | Module layout (§8) | 11 modules incl. `config`, `routing`, `approval`, `audit`, `record` | 9 modules incl. `models` (`REPO`), `selection`, `state` | 7 modules incl. `store`, `cli` | 8 modules incl. `filters`, `audit`, `state` | 7 modules incl. `select`, `record` | Medium | L2 |
| S-005 | Dispatch record storage form (§7) | One JSON per login: `<state_dir>/<login>/record.json` | One JSON file keyed `IronbellyOrg/IronClaude#<N>` | SQLite with append-only transition table | One `dispatch.json` per state dir | One file per issue: `records/<N>.json` | High | L3 |
| S-006 | Open-decision IDs (§10) | OD-1..OD-9 | OD-1..OD-10 | Unnumbered table | OD-1..OD-9 | O-1..O-8 | Low | L1 |
| S-007 | Traceability (§12) | "Verified fact N", research and seed refs | RD-F / SB / RR codes | S / R source tags, no line refs | RD fact / SB Q codes | RF- / RQ- / SB codes | Low | L1 |
| S-008 | Risk register (§11) | Table R-1..R-8 | Table R1..R9 with likelihood/impact | Table of named risks, no IDs | Table R1..R7 | List R-1..R-7 | Low | L1 |

## Content Differences

| # | Topic | Variant A Approach | Variant B Approach | Variant C Approach | Variant D Approach | Variant E Approach | Severity | Level |
|---|-------|--------------------|--------------------|--------------------|--------------------|--------------------|----------|-------|
| C-001 | Tagged; label names (§3, §10) | Exact label `watch:ready`; approval `watch:approved` (OD-4) | `watch:claim` / `approved:claim`; tagged includes OPEN (OD-4) | Label resolved by node ID, not name; names left open | `issue-watch:trigger` / `issue-watch:approved` (OD-1, runbook) | `claim-ready` / `claim-approved`; tagged includes open | Medium | L3 |
| C-002 | Approved by a human (§3, FR-005..008) | Latest `labeled` actor allow-listed, not Bot type or `[bot]` login, no later `unlabeled` | Latest labeled/unlabeled over complete paged events is `labeled`, actor allow-listed; no bot check | Account IDs, non-bot, latest application; incomplete history fails; Triage access verified first | Latest event `labeled`, actor allow-listed, `actor.type == "User"` | Most recent `labeled` actor type User and listed; no later `unlabeled` | High | L3 |
| C-003 | In a Project; Backlog (§3, FR-006..009) | `gh project item-list -L 100`; Status exactly `Backlog`; count equal to limit makes predicate false | Project query is the discovery itself; item repository must be IronClaude | Non-archived Projects v2 item by node ID; Status field and option IDs; no drafts/PRs | Item-list fields (ASSUMPTION); other Status gives `not_backlog` | Per-issue `projectItems` GraphQL, one call per candidate | High | L3 |
| C-004 | Intended owner (§3) | Routing table, default `assigned-to-self`; any other assignee excludes | Assignees exactly `[own login]` | Sole assignee matching account ID; deliberately stricter than the claim | Assignees contain own login; others exclude; unassigned belongs to no one | Assignees exactly `{own login}` | Medium | L3 |
| C-005 | Same-login multi-workspace (§10, §11) | Config `enabled` defaults false; enable in one workspace per login (OD-2) | Setup rule one poller per login; `own_login` audited (OD-2) | "Unsupported"; nominate one dispatch authority | Scheduler in one workspace per login; `host` audited (OD-8) | One poller per login by setup instruction (O-4) | Medium | L3 |
| C-006 | Discovery and truncation (FR-003..005) | `gh issue list --label` `-L 100`; 100 items gives exit 4 `truncated` | Project query `-L 100`; truncation gives exit 2 `E-GH-TRUNCATED` | Incomplete pagination blocks affected selection (FR-006) | Same argv as A; 100 items gives exit 4 | Issue list, untagged/unowned dropped before per-candidate calls; truncation exit 4 | High | L3 |
| C-007 | Dispatch record states (§7) | Six states; `failed` retryable after lease while attempts left; `history` of 20 | Six states plus `launch_cwd`, `approver`, `approval_event_id` fields | `unknown` entered before the external call as launch intent | Separate `attempts` and `launches` counters | Six states; `launches`, `approval_actor`; ambiguity resolves toward not launching | High | L3 |
| C-008 | Lease and caps (§7) | Lease 60, attempts 3, 1 launch/cycle, 10 candidates; lease at least 15 min | Lease marked ASSUMPTION; `max_pages` 5; gh 60 s, orca 120 s | Pending lease 60; 3 pre-submission attempts; 1 submission per issue; 10; 1/cycle | 60/3/10 plus `max_launches` 1 and `max_launches_per_cycle` 1 | 60/3/1 per cycle/10 plus 6 per day, 10 min failed backoff | Medium | L3 |
| C-009 | Record before launch; pre-launch re-read (FR-009..012) | `pending` fsync'd first; re-read failure gives `abandoned` `changed_before_launch`, `attempts -= 1` | Unchanged second snapshot is part of eligibility | Slot consumed and `unknown` committed in one transaction before I/O; refresh may cancel reservation | Re-read failure removes the pending entry, `revalidation_failed` | Re-read; record "deleted or marked `abandoned`" with `stale` (left undecided) | High | L3 |
| C-010 | Launch argv contract (FR-013..014) | 12 elements, `--agent claude`; worktree must be absolute and existing, else exit 2 | Probes `orca-ide` then `orca` via `orca-cli` topic; worktree origin must be IronClaude | Prose only; `path:<absolute-path>` selector; origin verified | 12 elements; runner rejects a `str` argv | `--agent <agent>` configurable; list argv, prompt one element | Medium | L2 |
| C-011 | Unknown launch outcome (FR-014..016, §7) | `agent_session_operation_unknown` gives `unknown`+id; retry only `--retry-launch`; lease expiry gives `failed` | Timeout gives `unknown`+null; null-id unknown abandoned after lease | Timeout or malformed output gives `unknown`; missing ID means operator investigation | Unknown whose lease expires becomes `abandoned` | Unknown without id becomes `abandoned`; with id retried | High | L3 |
| C-012 | Prompt integer rule (FR-012/013, FR-009) | int, not bool, 1..999999999; else `InvalidIssueNumber` | Regex `^[1-9][0-9]{0,8}$`; `ValueError` | Positive JSON integer; rejects bool, string, fraction, out of range | Regex with property test; `ValueError` | Range is an eligibility predicate; FR-013 fuzz test | Low | L3 |
| C-013 | Approver allow-list (§10) | Local config list; empty list approves nothing (OD-3) | File `~/.config/superclaude/issue-watch/approvers`; empty gives exit 1 `E-NO-APPROVERS` | Account IDs in trusted configuration, admitted after Triage check | Approvers file shipped with the Coder template (OD-2) | Local list; follow-up per-actor permission check replaces it (§9) | Medium | L3 |
| C-014 | Launched-session permission mode (§6, §10) | `ccsession-orca` default, documented; accepted residual (OD-6) | Do not enable F1 before Q6; skipped permissions need written owner acceptance (OD-8) | Deployment disabled until narrative-read risk accepted and policy verified | "Default interactive mode, never a bypass mode" (OD-7) | No override; live test before cron (O-6) | High | L2 |
| C-015 | Fail-closed scope (NFR-008 etc.) | Unreadable Project or full page voids predicate for the whole cycle | Per-issue error skips issue; full last events page gives `approval-unverifiable` | Absent or unreadable evidence is never positive | Any read failure before launch phase gives zero launches; Projects over 100 always fail (R3) | Unparseable output, timeout, missing executable: no launch for affected issue | High | L3 |
| C-016 | Rate limits (NFR) | 403/429 gives exit 5, no state change; at most 3+3N calls | Not handled specially, cadence is back-off; at most 42 calls, no retry | Persisted next-permitted-request time; fake-clock tests | Exit 3 `rate_limited`; 33 per cycle, idle 2 | Stop, exit 8; hard cap 35 calls aborts examinations | Medium | L3 |
| C-017 | Scheduling; where poller and state live (§7, §9) | `once` batch; F-1 coder_script cron; `~/.local/state/superclaude/issue-watch/<login>` | Cron F1 only after F3 live test; XDG state file | One bounded cycle; operator-configured persistent path; check cron overlap and shutdown | `${XDG_STATE_HOME}` path; 24 h shadow dry-run; staleness 900 s | `~/.superclaude/issue-watch/`; cron after live test | Medium | L2 |
| C-018 | Locking and kill switch (FR-017..019) | `flock`; held lock exits 0 `locked` | `flock`; held lock exits 0 | Exclusive cycle lock; overlap exits 6 | `flock` exits 75; `DISABLED` file kill switch | Lock exits 5; `DISABLED` file kill switch | Medium | L3 |
| C-019 | Observability and audit (FR-017/020, NFR) | One JSON line per cycle; closed skip-reason enum | One line per decision with approver and event id, plus summary | Structured events per candidate and per termination | `audit.jsonl` on every exit, `host`, `rate_remaining`, 5 MiB rotation, SLOs | Per-cycle line with `gh_calls`, `duration_ms`; `status` prints it | Medium | L2 |
| C-020 | CLI verbs and exit codes (§8) | `once [--dry-run]`, `status --json`, `check-config`; exits 0-7 | Single `once` with many flags, "No other verb"; exits 0-3 | `once`, `status`, `init-state`; exits 0, 2-6 | `once`, `status`; exits 0, 2-6, 75 | `once`, `status`, `check-config`, `reset <N>`; exits 0, 2-8 | Medium | L2 |
| C-021 | Configuration surface (§8, §10) | JSON file `~/.config/superclaude/issue-watch.json`, since `tomllib` needs 3.11 (OD-9) | All CLI flags; no config file | Operator configuration of IDs and authority | CLI options plus approvers file | Configuration validated by `check-config` | Medium | L2 |
| C-022 | Test strategy and mocks (§8) | 12 files incl. `test_stub_e2e`, AST `test_no_shell`, `test_sentinel` | `FakeRunner` exit 99, `FakeOrca`, `_assumed_shape` fixtures, hostile title | PATH stubs, concurrent processes, crash injection, account rename | Crash injection then five reruns; `PWNED-TITLE`; `test_security_invariants` | `test_no_text`, 50-cycle at-most-once, stub e2e as in `test_conflict_e2e.py` | Medium | L2 |
| C-023 | Follow-up scope (§9) | F-1..F-7 incl. `release <N>` verb, Coder#477, option D | F1..F7 incl. live test Q1-Q8, session constraint | Cron overlap, shutdown, session effect on workspace lifetime | FU-1..FU-7 incl. alerting, SLO measurement, `agentDefaultArgs` | ETag requests; per-actor permission check | Low | L2 |
| C-024 | Evidence for `claimed` (FR-008/009, FR-017) | Marker comment count; expired pending with marker becomes `claimed` | Own marker sets `claimed` even with no record | Only recognized claim evidence, never assignment alone | `--jq` boolean marker check | `launched` becomes `claimed` with own assignee and own marker | High | L3 |
| C-025 | Issue-text minimization (§6, NFR) | Requests no title, body or comments | No text read; hostile-title test | Marker check may inspect bounded comment content | `PWNED-TITLE` fixture keeps text out of audit | Field minimization; `test_no_text` scan | Medium | L2 |

## Contradictions

Quoted text is verbatim from the variant. "Impact" is the severity of the conflict.

| # | Point of Conflict | Variant A Position | Variant B Position | Variant C Position | Variant D Position | Variant E Position | Impact | Level |
|---|-------------------|--------------------|--------------------|--------------------|--------------------|--------------------|--------|-------|
| X-001 | Relaunch of a `launched` issue after the lease with no marker | §7: "audited as `launched_unclaimed` and never relaunched automatically" | §7 transitions: "`launched`, `failed` \| lease expired ..., no marker, attempts left \| new launch, `attempts + 1`" | §7: "`launched` ... may become `claimed` or `abandoned`"; "Expiry never releases a consumed slot" | §7: "`launched` \| lease expired with no marker \| `abandoned`, reason `claim_not_observed`" | §7: "when `lease_expires_at` passes with no claim, to `abandoned` with reason `lease_expired`" | High: only B re-launches a session that may be running; conflicts with seed `max_launches 1` | L3 |
| X-002 | `pending` entry found at cycle start (crash between write and reply) | §7: "Claim marker present: `claimed`; else `failed` (`lost_reply`)", and `failed` is retryable | §7: "A `pending` entry at cycle start is treated as `launched`" | §7: "Consuming the slot and entering `unknown` is one durable transaction before external I/O" | §7: "`abandoned`, reason `pending_orphan` \| no, never" | §7: `pending` after its lease resolves to `unknown` | High: A can launch twice; D and C accept a missed dispatch | L3 |
| X-003 | Corrupt or unparseable record | §7: "Unknown version or unparseable file: exit 6, no launch" | NFR-010: "A corrupt state file loads as empty and is replaced atomically" | §11: "recreating an empty ledger could duplicate every claim" | NFR-011: "An unparseable record yields exit 5 ... never a silent reset" | NFR-008: unparseable output gives no launch (record case not separately stated) | High: B's reset re-opens every pre-marker issue to launch | L3 |
| X-004 | Launch reply that is neither success nor `operation_unknown` (timeout) | FR-014: "any other failure moves it to `failed`"; §7 `unknown` "lease expired" to `failed` (retryable) | FR-015: "timeout to `unknown`+null" | FR-011 acceptance: "Given timeout or malformed launch output ... the record is `unknown`" | §7: `unknown` lease expiry to `abandoned`; `failed` only relaunches while `launches == 0` | §7: `failed` = "definite error, no session started" | High: A retries after a timeout that may have started a session | L3 |
| X-005 | Eligibility without a readable Project | OD-5: "`required`; `off` only by explicit config", reason "The issue requires Project plus Backlog" | FR-022: "`--label-only` replaces discovery"; OD-5 "It drops two definitions" | FR-006: "rather than substitute label-only eligibility" | OD-4: "Fail closed; no label-only flag" | O-3: "use hybrid option D before it" | High: A and B each define a mode that contradicts the issue's own "in a Project, Backlog" definition | L3 |
| X-006 | Rate-limit handling | NFR-006: "ends the cycle with exit 5 ... no entry state change" | R9: "Rate-limit replies not handled specially ... The 5-minute cadence is the back-off" | NFR-004: "persist a next-permitted-request time, with no busy retry" | NFR-009: "ends the cycle with `result=\"rate_limited\"`, exit 3" | NFR-006: "stop calling GitHub, launch nothing ... exit 8" | Medium: B continues per-issue reads into a 403 storm; C alone persists state | L3 |
| X-007 | Exit codes for the same events | Lock 0, Project unreadable 4, rate limit 5 (§8) | Lock 0 (FR-019); Project query failure is discovery, exit 2 | Overlap 6, rate limit 3 (§8) | Lock 75 (FR-017), Project unreadable 3 (FR-007), rate limit 3 | Lock 5 (FR-019), Project unreadable 3 (FR-009), rate limit 8 (FR-023) | Medium: incompatible alerting and runbook contracts | L2 |
| X-008 | Fixed owner decisions D1-D3 and seed argv | D1/D2/D3 kept; argv `--agent claude` | D1/D2/D3 kept; NG1 forbids any GitHub write | D1 kept: "No inbound sender-authentication mechanism is needed under A"; §6 marker check "may inspect bounded comment content" | D1/D2/D3 kept | FR-014: "`--agent <agent>`" vs seed "`orca agent launch --agent claude ...`" | Medium: E widens the fixed launch contract; no variant breaks D1, D2 or D3 itself | L2 |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | A | Stages (discover, filter, route, record, launch, audit) behind typed protocols, enforced by an import test (NFR-011), so options B/C/D replace one module (§1, §8) | Medium |
| U-002 | A | JSON config file chosen because `tomllib` needs Python 3.11 while the package supports 3.10 (OD-9, §8) | Medium |
| U-003 | A | Per-entry `history` of the last 20 transitions, and `check-config` rejecting a lease under 15 minutes (§7) | Low |
| U-004 | B | Executable probe `orca-ide` then `orca`, accepting only the `orca-cli` topic, because GNOME `orca` is a screen reader (FR-014, T7) | High |
| U-005 | B | Stored `launch_cwd` for retries, and `re-approved` that never resets attempts so label toggling cannot bypass the cap (§7, OD-6) | Medium |
| U-006 | B | Fixtures carry an `_assumed_shape` field marking unverified JSON shapes; `FakeRunner` exits 99 on any unscripted call (§4, §8) | Medium |
| U-007 | C | GitHub node and account IDs instead of names for labels, Project field/option, approvers and owner, surviving renames (§3, §7) | High |
| U-008 | C | SQLite store with explicit `init-state`, append-only transition table, and rejection of missing-after-initialization storage (§7, NFR-003) | Medium |
| U-009 | C | Persisted next-permitted-request time for rate limits, tested with a fake clock (NFR-004) | Medium |
| U-010 | C | Readiness scoring of options A-D and the nine revisit conditions (§2) | Low |
| U-011 | D | SLOs: p95 approval-to-launch at most 10 min, 99 percent of cycles exit 0/75, 95 percent claimed within the lease; staleness 900 s (NFR-013, §8) | Medium |
| U-012 | D | Operator runbook: pre-flight, exit-code action table, 24 h shadow dry-run rollout, disable and recovery steps (§8) | High |
| U-013 | D | Audit line carries `host` and `rate_remaining`, rotated at 5 MiB (NFR-006) | Low |
| U-014 | E | Project membership from the issue's own `projectItems` (GraphQL), so cost scales with candidates and a Project over 100 items still works (FR-008, O-3) | High |
| U-015 | E | Daily launch cap of 6, 30-day pruning with `considered` at most 1000, and a refusal to run inside an Orca worker environment (FR-018, NFR-013, §6) | Medium |

## Shared Assumptions

| # | Agreement | Precondition it depends on | Classification | Level |
|---|-----------|----------------------------|----------------|-------|
| A-001 | All keep the dispatch record in local workspace storage (A/B/D/E §7, C §7) | The state path survives workspace restarts | STATED (A, B, D, E mark `$HOME` persistence ASSUMPTION/UNVERIFIED; C requires an operator-configured persistent path) | L3 |
| A-002 | All launch `/sc:issue --claim <int>` through `--prompt` | A leading slash command in the prompt runs as a command | STATED (all mark it UNVERIFIED and gate enablement on a live test) | L2 |
| A-003 | A, B, D, E key owner, approver and labels by login or name | Logins and label names are stable identifiers | CONTRADICTED (C §7: node IDs "survive login changes, label removal, reopening") | L3 |
| A-004 | All prevent same-login double dispatch only by setup (one poller per login) | No second workspace with the same login enables the poller | STATED (A OD-2, B OD-2, C §7, D OD-8, E O-4) | L3 |
| A-005 | All require the intended owner to be already assigned when the approval is evaluated | Someone assigns the issue before or with approval; unassigned approved issues are never picked up | UNSTATED (only B OD-1 states it) | L3 |
| A-006 | All use leases, backoffs and least-recently-examined ordering on wall-clock time | The workspace clock is correct and does not jump across restarts | UNSTATED | L3 |
| A-007 | All rely on an exclusive file lock against overlapping cycles | `flock` is effective on the state filesystem (local, not network) and the scheduler runs one host | UNSTATED | L3 |
| A-008 | All treat the latest `labeled` event `actor` as the human approver | The event actor is the human who decided, not an automation or a human-run bot typed `User` | UNSTATED (D T3 lists the bot residual; none states the precondition) | L3 |
| A-009 | A, B, D, E treat the claim marker as the durable guard once a lease ends | The claim posts `<!-- sc:issue:claim -->` within the 60-minute lease | UNSTATED (lease length is a [PROPOSAL] with no claim-duration evidence) | L3 |
| A-010 | All load the approver allow-list from a local file or config | Only the workspace owner can write that file | UNSTATED (D T2 names "allow-list edited by a writer" as residual only) | L3 |

Promoted points:
- [SHARED-ASSUMPTION] A-005: approval is only acted on when the owner is already assigned; an approved but unassigned issue waits forever.
- [SHARED-ASSUMPTION] A-006: lease, backoff and ordering correctness depends on a trustworthy wall clock.
- [SHARED-ASSUMPTION] A-007: overlap protection depends on `flock` semantics of the chosen state path.
- [SHARED-ASSUMPTION] A-008: the `labeled` actor is taken as proof of a human decision.
- [SHARED-ASSUMPTION] A-009: the 60-minute lease assumes the claim finishes and posts its marker inside it.
- [SHARED-ASSUMPTION] A-010: the allow-list is trusted because its file is assumed owner-only.

## Summary

- Counts per category: structural 8 (S-001..S-008), content 25 (C-001..C-025), contradictions 8 (X-001..X-008), unique 15 (U-001..U-015), shared assumptions 10 (A-001..A-010; 6 promoted as [SHARED-ASSUMPTION], 3 STATED, 1 CONTRADICTED).
- Counts per Level (S, C, X, A rows; 51 rows): L1 5 (all structural: S-001, S-002, S-006, S-007, S-008); L2 14 (S-003, S-004; C-010, C-014, C-017, C-019, C-020, C-021, C-022, C-023, C-025; X-007, X-008; A-002); L3 32.
- Unique contributions by value: High 4 (U-004, U-007, U-012, U-014), Medium 8, Low 3. By variant: A 3, B 3, C 4, D 3, E 2.
- Highest-severity IDs (High): S-005; C-002, C-003, C-006, C-007, C-009, C-011, C-014, C-015, C-024; X-001, X-002, X-003, X-004, X-005.
- The sharpest divergence is crash and ambiguity recovery in the dispatch record (X-001 to X-004): the variants disagree on whether a `launched`, `pending`, timed-out or corrupt-record issue can be launched again, which is the at-most-once property the seed asks for.
