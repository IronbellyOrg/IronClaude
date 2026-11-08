# Spec Panel Review: GitHub Issue Watcher (merged-requirements.md)

- Mode: critique; focus: requirements, architecture
- Spec: `merged-requirements.md` (475 lines), read in full; context from `seed-brief.md`
- Fixed and not challenged: D1 (option A), D2 (claim-only), D3 (integer-only prompt). The panel challenges only how the spec realises them.
- Repo facts were checked with Read, Grep and Glob only. The `adversarial/` directory was not opened. Nothing was run.
- Severity: CRITICAL means provably wrong or self-contradictory; MAJOR means ambiguous, incomplete or untestable; MINOR means clearer wording would help.
- Line numbers refer to `merged-requirements.md` unless another file is named.
- Experts spoke in the commissioned order 1 to 11, and PF ids follow that order. Their findings are filed under three headers. Whittaker (speaker 6) is filed under the adversarial header, so Newman's and Hohpe's architecture ids (PF-032 to PF-036) appear before his.

=== REQUIREMENTS ANALYSIS ===

### 1. Karl Wiegers (requirements lead)

"A requirement that cites a source has to agree with it. Four statements here contradict the source they cite, or contradict another requirement."

**PF-001** | CRITICAL | Wiegers | Section 3 "Intended owner" L98; OD-3 L384 | Priority: High
- Issue: L98 says `is_intended_owner` "equals the claim's own rule (`refs/claim.md:41-42`)", and OD-3 repeats it. The claim stops only when the issue is "Assigned to anyone other than the current login" (`refs/claim.md:41`). It continues on an unassigned issue and assigns that issue in Wave 3 (`refs/claim.md:47`). So the claim accepts {} and {own}, while the spec accepts only {own}. L77 itself says the watcher's rule is a "stricter subset".
- Recommendation: Replace the clause in L98: "and is stricter than the claim's own rule (`refs/claim.md:41-42`), which also accepts an unassigned issue; the watcher never launches on an unassigned issue." In OD-3, replace "Matches the claim's own rule" with "A strict subset of the claim's rule". Rationale: a false equivalence would lead a later editor to "align" the two rules and widen what the watcher launches on.
- Quality impact: Consistency; it also keeps the traceability to the claim honest.

**PF-002** | CRITICAL | Wiegers | FR-014 GWT L153 | Priority: High
- Issue: The GWT ends "In every case `launches` stays 1". The same GWT has a failing probe that writes "no entry", so there is no counter at all. A launch that never happened leaves `launches` at 0, and the pre-pending `failed` path explicitly has `launches` 0 (L152, L278).
- Recommendation: Replace the last sentence with: "In every case after the `pending` write, `launches` is 1; a failing probe writes no entry, and a pre-pending `failed` has `launches` 0." Rationale: as written, the test cannot be implemented.
- Quality impact: Testability, Consistency.

**PF-003** | CRITICAL | Wiegers | FR-002 L113; FR-013 GWT L150; FR-025 L173; FR-027 L188; FR-014 L152 | Priority: High
- Issue: The start of a cycle is described in three incompatible ways.
  - FR-002 says the login is resolved "first" and no other external call is made if that fails.
  - The FR-013 GWT says a missing worktree exits 2 "before any `gh` call". FR-027 says the same of the approvers file.
  - FR-025 runs `git` "at cycle start", which is an external call; whether it runs before or after `api user` is not said.
  - FR-014 puts the probe, worktree and origin checks inside "Per launch".
- Recommendation: Add to FR-001: "Cycle order: platform and config validation, approvers file, worktree existence (no external call); lock; DISABLED; `next_permitted_at`; `gh api user`; origin check (`git`); discovery; per-issue reads; Orca probe (only if a candidate is eligible); launch steps (FR-014)." Rationale: every "before X" claim then has one meaning.
- Quality impact: Consistency, Testability.

**PF-004** | CRITICAL | Wiegers | Section 3 "Eligible issue" L102; Section 7 L268, L280, L291 | Priority: High
- Issue: An entry in `abandoned` `attempts_exhausted` has `launches` 0, because `failed` never reaches `pending`. L102 excludes only entries with "`launches > 0`" and entries "in `failed` backoff". Such an entry therefore passes L102 and can move to `pending`. That contradicts L291, "`abandoned` is terminal except for a later own marker or `reset`". The same gap applies to a `claimed` entry recorded from a marker alone (`launches` 0, L288).
- Recommendation: In L102, replace "no record entry with `launches > 0`; not in `failed` backoff" with "no record entry, or an entry in `failed` whose backoff has elapsed with `attempts` < `max_attempts`; any other entry state is ineligible." Rationale: eligibility should come from the state machine, not from a counter.
- Quality impact: Consistency; protects the safety invariant.

**PF-005** | MAJOR | Wiegers | Section 3 "Own login" L80 | Priority: Medium
- Issue: The login "must match" the regex, but the spec never says what a mismatch does: exit code, reason, or whether discovery runs.
- Recommendation: Append to L80: "A login that does not match exits 3 with reason `login_invalid` before discovery." Rationale: an unenforced "must" cannot be tested.
- Quality impact: Completeness, Testability.

**PF-006** | MAJOR | Wiegers | Section 3 "Complete event history" L92 | Priority: Medium
- Issue: The "page cap" has no value. It is unclear whether it is the 1000 pages of `poll-augment-review.sh:51` or something bounded by the 35-call cap. "An opposing same-second tie fails closed" defines neither "opposing" nor the reason code it skips with.
- Recommendation: Replace with: "The page cap is 5 pages per read [PROPOSAL], counted in the NFR-009 cap. An opposing tie is a `labeled` and an `unlabeled` event for the approval label, or approval and trigger `labeled` events, with equal `created_at` seconds; it skips `events_incomplete`." Rationale: the bound and the tie are both test inputs.
- Quality impact: Completeness, Testability.

**PF-007** | MAJOR | Wiegers | FR-020 L179; FR-022 GWT L132 | Priority: Medium
- Issue: FR-020 requires a "closed-enum reason", but the enum is never listed. Reasons are scattered across about 25 names. The FR-022 GWT maps a failed events read to `events_incomplete`, so a transport failure cannot be told apart from a pagination fault, while the analogous Project failure has its own reason, `project_unreadable` (FR-007).
- Recommendation: Add to Section 8: "Reason enum (closed): one table listing each reason, its source requirement and its exit; a failed events read is `events_unreadable`, distinct from `events_incomplete`." Rationale: a closed enum that is never enumerated cannot be schema-validated (NFR-006).
- Quality impact: Completeness, Testability.

### 2. Gojko Adzic

"Specification by example only works when the examples are true. Run the numbers in two of these examples and the spec's own caps make them false."

**PF-008** | CRITICAL | Adzic | Section 8 "Acceptance" L325; FR-024 L164 | Priority: High
- Issue: "The poller starts exactly one mocked launch per eligible issue ... the end-to-end test runs N cycles." The day cap is 6 per rolling 24 h (FR-024), and the cap in effect at the cycle cadence, 5 minutes, is still 6. With N = 10, the 10 cycles fit inside 50 minutes and give 6 launches and 4 `day_cap` skips, not 10 launches. With N ≥ 100, FR-004 exits 4 with 0 launches. The acceptance criterion is false for every N > 6.
- Recommendation: Replace the first two sentences with: "Given N eligible issues (1 ≤ N ≤ 99) and an injected clock, each cycle launches at most one; within 24 h exactly min(N, 6) launch and the rest skip `day_cap`; after the clock advances 24 h the rest launch, one per cycle, each with the integer only." Rationale: the seed's criterion (seed-brief L42) predates the day cap.
- Quality impact: Testability, Consistency.

**PF-009** | CRITICAL | Adzic | FR-016 GWT L159; NFR-009 L216 | Priority: High
- Issue: "Given 15 eligible issues, ... cycle 2 examines the 5 unexamined issues first." An issue that is eligible passes every check, so it is fully read: at least events, the marker comments and `projectItems` (3 calls), plus the unchanged-since-approval timestamps, which need a separate `--jq` projection (4). The launch candidate's re-read adds 3 more (L143). At 4 calls each, the cap allows 4k + 3 ≤ 35, so k = 8. Cycle 1 therefore examines 8, not 10, and cycle 2 finds 7 unexamined issues, not 5. The hedge in the GWT covers cycle 1 only.
- Recommendation: Replace the GWT with: "Given 15 eligible issues of one page each and a per-candidate read count r, cycle 1 examines k = min(10, floor((35 − 3) / r)) and launches 1; cycle 2 examines the 15 − k never-examined issues first." Rationale: the example must follow from the stated caps.
- Quality impact: Testability, Consistency.

**PF-010** | MAJOR | Adzic | NFR-013(a) L224; FR-020 L179; Section 7 schema L262 | Priority: Medium
- Issue: "Approval-to-`launched` p95 ... computable from `audit.jsonl` and `dispatch.json`." Neither file stores the approval time: the entry keeps `approval_event_id` and the decision line keeps `approver_id`, but neither keeps a timestamp. The SLO cannot be computed.
- Recommendation: Add `approved_at` (the approval event's `created_at`) to the entry schema (L262) and to FR-020 decision lines. Rationale: an SLO needs both endpoints recorded.
- Quality impact: Testability.

**PF-011** | MAJOR | Adzic | NFR-013(b), (d) L224; FR-021 L182; FR-026 L185 | Priority: Medium
- Issue: Clause (b) counts every exit-0 cycle as healthy. A DISABLED poller exits 0 on every cycle (L311), so it scores 100 percent, while FR-021 deliberately excludes DISABLED and dry-run cycles from health. Clause (d) uses "unacknowledged", but FR-026 has no acknowledge verb.
- Recommendation: Replace (b) and (d) with: "(b) ≥ 99 percent of non-DISABLED, non-dry-run cycles over 7 days exit 0; (d) no `unknown` or `abandoned` `pending_orphan` entry stays more than 24 h without reaching `claimed` or being `reset`." Rationale: every term then maps to a recorded state.
- Quality impact: Consistency, Testability.

**PF-012** | MINOR | Adzic | R3 L403; FR-004 L119 | Priority: Low
- Issue: "More than 99 open trigger issues" and "exactly the limit (100)" describe the same threshold in two different forms.
- Recommendation: Write R3 as "100 or more open trigger issues assigned to the owner (discovery returns 100)".
- Quality impact: Clarity.

### 3. Alistair Cockburn

"Look at the operator's and the poller's goals one actor at a time. Several main-success paths have no failure branch, and one operator goal has no path at all."

**PF-013** | MAJOR | Cockburn | FR-027 L188; FR-026 L185 | Priority: High
- Issue: The config has `enabled: false` by default, but no requirement says what `once` does when `enabled` is false. It could exit 0, exit 2, or run as a dry run, and it is not said whether it writes an audit line or refreshes health. The runbook (L348-357) never says when to flip it.
- Recommendation: Add to FR-027: "With `enabled: false`, `once` exits 0 before any external call with audit reason `not_enabled`, and does not refresh health; `--dry-run` runs regardless of `enabled`." Add a runbook step: "Set `enabled: true` after step 9." Rationale: this is the main gate, and it has no defined behaviour.
- Quality impact: Completeness.

**PF-014** | MAJOR | Cockburn | Section 3 "Claimed" L100; Section 7 L268, L287-288 | Priority: High
- Issue: Marker freshness is measured "after the entry's `pending_at`, or, with no entry, after the current approval event". Two kinds of entry have no `pending_at`: a `failed` entry, and a `claimed` entry recorded from a marker alone. For them the comparison is undefined. The transitions table has no row for `failed` followed by an own marker, which is a hand claim during backoff. Without that row the next retry launches a second session on an issue that is already claimed.
- Recommendation: Replace the L100 sentence: "It counts only if created or last edited after the entry's `pending_at` when set, otherwise after the current approval event." Add a transition row: "`failed` | own marker newer than the current approval | `claimed` | `launches` 0". Rationale: it closes a path to a duplicate claim.
- Quality impact: Completeness, Consistency.

**PF-015** | MAJOR | Cockburn | FR-020 L179-180; FR-027 L188; Section 8 exit 6 L316 | Priority: Medium
- Issue: "Every exit shall append ... one cycle line; a crash is the only exit without a line." In two cases the poller has no writable audit file:
  - an exit 2 caused by a missing or unparseable config file, because `state_dir` comes from the config;
  - an exit 6 caused by an unwritable state directory.

  The GWT also omits exit 2.
- Recommendation: Replace the last sentence of FR-020: "A crash, an exit 2 before `state_dir` is known, and an exit 6 for an unwritable state directory write one JSON line to stderr instead; every other exit appends to `audit.jsonl`." Add exit 2 (valid config, bad worktree) to the GWT. Rationale: the promise cannot be kept as written.
- Quality impact: Testability, Completeness.

**PF-016** | MINOR | Cockburn | FR-014 L152; Section 7 L278-280 | Priority: Low
- Issue: A prompt `ValueError` is deterministic, because the issue number does not change, yet it is retried 3 times over 20 minutes before reaching `abandoned`.
- Recommendation: Note that a prompt `ValueError` goes straight to `abandoned` with reason `invalid_number`, or state why the retry is kept.
- Quality impact: Clarity.

=== ARCHITECTURE ANALYSIS ===

### 4. Martin Fowler

"A seam that the reused code does not have is not a seam. Check what `_find_orca` really is before promising to run it through the runner."

**PF-017** | CRITICAL | Fowler | FR-013 L149; NFR-002 L202; NFR-014 L226; Section 8 Modules L301 | Priority: High
- Issue: FR-013 says `_find_orca()` is "run through the injected runner; its 10 s timeout counts toward the cycle budget", and NFR-014 says the package "reuses ... `_find_orca`". The reused function (`src/superclaude/cli/install_user_setup.py:198-221`) has no parameters. It calls `shutil.which` and then `subprocess.run([path, "skills", "list", "--json"], ..., timeout=10)` directly. It cannot be run through the runner, so:
  - the FakeRunner of NFR-005 never sees the probe argv;
  - NFR-002's argv allow-list cannot test the probe;
  - FR-029 cannot clamp the probe's timeout;
  - stub-on-PATH tests reach the real binary search.

  Reuse and the runner seam are mutually exclusive as written.
- Recommendation: Replace the FR-013 sentence: "`<orca>` comes from `launch.find_orca(runner)`, which tries `_ORCA_CLIS` (`install_user_setup.py:35`) in order through the injected runner with the same `skills list --json` acceptance rule as `_find_orca`; a parity test pins the candidate list and the acceptance rule." Update NFR-014 and L301 to read "mirrors" in place of "reuses". Rationale: the parity-test pattern is already used for `parse_origin_url` (FR-025).
- Quality impact: Testability, Consistency.

**PF-018** | MAJOR | Fowler | FR-023 L161; FR-028 L191; FR-011 L143 | Priority: Medium
- Issue: "Written in the same store write" has no antecedent, because a cycle can make several store writes: `pending`, then the outcome, `failed` entries, and the `pending_orphan` sweep. FR-028 says a rate-limit reply stops "with no state change except `next_permitted_at`". A rate limit that arrives after a `pending` write and spawn earlier in the same cycle, during a later candidate's read, cannot undo that launch.
- Recommendation: Replace the FR-023 phrase with "written in the cycle's final store write, after the last entry write" and FR-028's with "makes no further state change except `next_permitted_at` and the `considered` stamps of candidates already examined; entries written earlier in the cycle stand." Rationale: it defines the commit point.
- Quality impact: Clarity, Consistency.

**PF-019** | MINOR | Fowler | NFR-014 L226; L301 | Priority: Low
- Issue: There is a launcher Protocol and also a runner that carries the launch argv (FR-013). Two seams for one call invite tests that mock the wrong one.
- Recommendation: Say which seam the tests fake for the launch, or drop the launcher Protocol.
- Quality impact: Clarity.

**PF-020** | MINOR | Fowler | NFR-002 L202; Section 3 L92 | Priority: Low
- Issue: NFR-002 allows argv that starts with `gh api --method GET repos/...`, but the cited script uses `gh api "repos/..." --method GET` (`poll-augment-review.sh:53`). Saying "as in" the script invites a copy that fails the allow-list.
- Recommendation: State that the poller's order is `gh api --method GET <path>` and that the script is cited for the paging rule only.
- Quality impact: Clarity.

### 5. Michael Nygard

"Every external dependency will eventually return something hostile. A failure table that sends one failure to two exit codes is a production incident waiting for a pager."

**PF-021** | CRITICAL | Nygard | Failure modes L339 and L341; FR-022 L131; FR-011 L143; exit table L317 | Priority: High
- Issue: In the failure-mode table, a re-read failure maps to exit 7 ("Pre-pending `failed` ... Orca runtime, exec or re-read failure", L339) and also to exit 0 ("Per-issue read failure ... marker or re-read", L341). FR-022 lists the re-read as a per-issue skip, and FR-011 says a transient re-read error writes `failed`. The exit table (L317) says 7 means "A launch ended `failed`", but a `failed` entry has `launches` 0, so no launch exists. An operator alerting on exit 7 cannot tell which case occurred, and the FR-020 test cannot assert a single code.
- Recommendation: Replace L341's cause with "One issue's events, Project item, marker, or a non-transient re-read failure (`revalidation_failed`)" and L317 with "7 | An entry was written `failed` (pre-pending, `launches` 0), `unknown`, or `abandoned` `spawn_error` in this cycle". Rationale: each failure then has one exit code.
- Quality impact: Consistency, Testability.

**PF-022** | MAJOR | Nygard | FR-028 L191 | Priority: High
- Issue: `next_permitted_at` is taken from `Retry-After` or the reset header with no upper bound. A misparsed reset epoch (epoch seconds read as delta seconds), or a hostile proxy, can set it decades ahead. Every later cycle then exits 5 with zero calls, a state that FR-021 health shows only as "unhealthy" and that no verb clears except moving the state aside, which loses the day cap.
- Recommendation: Append to FR-028: "`next_permitted_at` is clamped to at most 3600 s after the reply; a larger or unparseable value is stored as 3600 s with audit reason `rate_limit_clamped`; `reset --rate-limit` clears it." Rationale: it bounds a silent outage.
- Quality impact: Completeness.

**PF-023** | MAJOR | Nygard | FR-017 L167; FR-020 L179 | Priority: Medium
- Issue: On `lock_held`, the losing process appends an audit line, and so writes `audit.jsonl` without the lock. The lock holder may be rotating the file at 5 MiB at that moment, so the line can land in the rotated file, be lost, or interleave. Nothing says appends are single `O_APPEND` writes of at most `PIPE_BUF`, or that rotation happens under the lock.
- Recommendation: Add to FR-020: "Rotation happens only under the lock. Each line is one `O_APPEND` write; a process without the lock (exit 75) appends but never rotates." Rationale: it makes the unlocked path safe by construction.
- Quality impact: Completeness.

### 6. Sam Newman

"The boundaries here are with GitHub, Orca and the claim command. Two of the three contracts exist only in prose."

**PF-032** | MAJOR | Newman | NFR-011 L220; Section 7 schema L262 | Priority: Medium
- Issue: An unknown `schema_version` gives exit 6, and the only recovery is to move the state directory aside and run `init-state`. That recovery discards every `consumed_at` and every tombstone. Any schema change in v1.1 therefore forces a state reset that empties the day cap and the "never relaunch" history. No migration rule or forward-compatibility rule exists.
- Recommendation: Add to NFR-011: "A store whose `schema_version` is lower than the code's is migrated in place under the lock by a pure, tested function that preserves every entry and `consumed_at`; only a higher or unknown version gives exit 6." Rationale: it keeps at-most-once across upgrades.
- Quality impact: Completeness.

**PF-033** | MAJOR | Newman | Section 3 "Claimed" L100; FR-009 L137 | Priority: Medium
- Issue: The `claimed` state depends on the literal `<!-- sc:issue:claim -->`, which is owned by the claim command (`refs/claim.md:29`, `templates/claim-comment.md:23`). If either file changes, the poller never observes `claimed`. All `launched` entries then age into `claim_not_observed`, and no test fails.
- Recommendation: Add to FR-009: "A contract test asserts that `predicates.CLAIM_MARKER` occurs verbatim in `refs/claim.md` and `templates/claim-comment.md` of the `sc-issue-protocol` skill." Rationale: it turns a cross-component string into a pinned contract.
- Quality impact: Testability.

**PF-034** | MAJOR | Newman | Section 2 L47; FR-013 L149 | Priority: Medium
- Issue: `ORCA_AGENT` is "the agent name the seed brief fixes", but the spec never writes the value. The FR-013 GWT says the recorded argv "equals that list" and cannot be checked without consulting another document. The seed brief (L64) says `claude`.
- Recommendation: Replace the FR-013 clause with "`<ORCA_AGENT>` is the module constant `ORCA_AGENT = \"claude\"` (seed brief, `--agent claude`)". Rationale: the spec must stand alone and the GWT must be literal.
- Quality impact: Completeness, Testability.

### 7. Gregor Hohpe

"Two systems, two clocks, and an ordering that reads the expensive channel before the cheap one."

**PF-035** | MAJOR | Hohpe | Section 3 "Claimed" L100; FR-009 GWT L138; Section 7 L287 | Priority: Medium
- Issue: `pending_at` comes from the workspace clock, and the marker's `created_at` comes from GitHub's clock. If the workspace clock is ahead by more than the time from launch to claim comment, a genuine claim reads as "older than T". The entry then stays `launched`, and later becomes `claim_not_observed`, a false alarm against NFR-013(c). No tolerance is stated, and R16 covers only the day cap.
- Recommendation: Add to the Claimed definition: "Comparison against `pending_at` allows a skew tolerance of 300 s [PROPOSAL]; the cycle line records the `Date` header offset of the discovery reply, and an offset above 60 s writes a `clock_skew` warning line." Rationale: it puts both timestamps on one basis.
- Quality impact: Completeness.

**PF-036** | MAJOR | Hohpe | Section 3 "Eligible issue" L102; FR-024 L164; NFR-009 L216 | Priority: Medium
- Issue: The eligibility order puts the local checks (an entry with `launches > 0`, `failed` backoff) last, after events, marker, timestamps and Project reads. The day cap is checked only before the `pending` write. So:
  - a `launched` entry waiting for its marker is fully network-read on every cycle;
  - at the day cap, every cycle still spends up to 35 calls on candidates that cannot launch.

  With W workspaces on one login this multiplies by W.
- Recommendation: Replace the L102 order with: "Checks run local first: no entry with `launches > 0` unless testing for `claimed`; not in `failed` backoff; day cap not reached (otherwise skip `day_cap` before any per-issue call); then open, tagged, intended owner, approved, not claimed, unchanged, Project/Backlog." Rationale: zero-cost checks come first and keep the reason deterministic.
- Quality impact: Completeness (budget).

=== ADVERSARIAL ANALYSIS ===

### 8. James Whittaker

"I attack the invariants, not the prose. Five attacks, eight breaks."

**PF-024** | CRITICAL | Whittaker (Sentinel Collision) | Section 7 L289; FR-026 L185-186; FR-024 L164 | Priority: High
- I can break this specification by Sentinel Collision. The invariant at FR-024 ("counts entries in any state whose `consumed_at` falls in the last 24 h ... `reset` keeps `consumed_at`") fails when `reset` removes the entry that carries `consumed_at` (L289: To = "(none)"; FR-026 GWT: "it removes the entry, keeps `consumed_at` in the day-cap count").
- Concrete attack:
  - Before: 6 entries with `consumed_at` in the last 24 h, one of them issue 9 `abandoned`.
  - The operator runs `reset 9 --forfeit-guarantee`. Issue 9's entry is gone, and the store schema (L262) has no other field that could hold its `consumed_at`.
  - After: the count of entries is 5. A seventh issue passes `day_cap` and launches, which contradicts the FR-024 GWT ("the count is still 6").
  - Variant: if the implementer keeps the entry so the count is right, then L281 ("(none) or `failed`" → `pending` sets `consumed_at`) cannot fire for issue 9, because "immutable" `consumed_at` cannot be set again.
- Recommendation: Replace the L289 row's To and Notes: "`reset` | (none); the entry's `consumed_at` is appended to the store-level list `consumed_log` (pruned after 24 h), which FR-024 counts together with entries". Add `consumed_log` to the store schema. Rationale: the sentinel needs a home that outlives the entry.
- Quality impact: Consistency, Testability.

**PF-025** | CRITICAL | Whittaker (Sequence) | FR-014 L152; FR-018 L170; FR-025 L173; FR-024 L164 | Priority: High
- I can break this specification by Sequence. The invariant at FR-018 ("DISABLED is checked again before each `pending` write") and at FR-025 (origin "again just before the `pending` write") fails when FR-014's mandated order runs DISABLED and origin before the re-read, and caches origin per cycle.
- Concrete attack:
  - Before: issue 9 is eligible, and DISABLED is absent at the FR-014 step-1 check.
  - The re-read starts. It is 3 calls of up to 20 s each. During it, the operator runs `touch DISABLED` and re-points the worktree's origin.
  - FR-014 proceeds: the re-read passes, then `pending` is written, then Orca is spawned.
  - After: one launch from a disabled poller in a foreign-origin worktree, which violates the FR-018 GWT ("created after discovery and before the `pending` write ... no `pending` entry") and FR-025. The day-cap count of FR-024, also "before a `pending` write", appears nowhere in the FR-014 order.
- Recommendation: Replace the FR-014 order: "the Orca probe and worktree check (cached per cycle); the prompt build; the re-read; the day-cap count; the DISABLED check; the origin re-check (not cached); the `pending` write; the spawn." Rationale: every pre-`pending` guard then sits immediately before the write it guards.
- Quality impact: Consistency, Correctness of the guarantee.

**PF-026** | MAJOR | Whittaker (Zero/Empty) | FR-027 L188; T13 L247 | Priority: High
- I can break this specification by Zero/Empty. The invariant at FR-027 ("exits 2 ... if that file is missing, empty or group/other-writable") fails when the file is not empty in bytes but holds no valid ID.
- Concrete attack:
  - Before: the approvers file contains `\n  \n` or `octocat`, a login instead of an ID.
  - FR-027 sees a non-empty file, so `check-config` passes and reports an "entry count" of 1 or 2.
  - After: the allow-list is effectively empty, and every approval skips `not_approved`, a silent permanent no-op. Alternatively, a parser that accepts `123abc` truncates it to `123`, which approves the wrong account.
- Recommendation: Add to FR-027: "The file holds one decimal account ID per line matching `^[1-9][0-9]{0,19}$`; blank lines and lines starting with `#` are ignored; any other line, or zero IDs after that, exits 2; duplicates are collapsed." Rationale: it defines "empty" semantically.
- Quality impact: Completeness, Security.

**PF-027** | MAJOR | Whittaker (Zero/Empty, Maximum) | FR-004 L119; FR-003 L116 | Priority: Medium
- I can break this specification by a Maximum overflow. The invariant at FR-004 ("returns exactly the limit (100) shall fail closed") fails when a reply holds 101 items, for example from a `gh` version that ignores `-L` or from a pagination glitch.
- Concrete attack: the stub returns 101 objects. "Exactly 100" is false, so the cycle proceeds on a set that was never bounded. It also does not stop on duplicate `number` values in the discovery list.
- Recommendation: Replace the FR-004 sentence: "Discovery returning 100 or more results, or any repeated `number`, shall fail closed: exit 4 with zero launches." Rationale: a guard on `>=` is safe against overflow.
- Quality impact: Testability.

**PF-028** | MAJOR | Whittaker (Accumulation) | FR-020 L179; NFR-006 L210; NFR-013 L224; FU-10 L371 | Priority: Medium
- I can break this specification by Accumulation. The invariant "all computable from `audit.jsonl`" (NFR-013) fails when rotation at 5 MiB discards the history the 7-day and 14-day windows need.
- Concrete attack: 10 candidates per cycle at about 200 B per line, times 11 lines per cycle and 288 cycles a day, is about 630 KB a day. The file rotates after about 8 days. The spec does not say how many rotated files are kept. If none are kept, on day 9 the 7-day SLO and the FU-10 two-week measurement lose all data written before the rotation.
- Recommendation: Append to FR-020: "Rotation keeps `audit.jsonl.1` to `audit.jsonl.4` (at least 25 MiB, about 40 days at 10 candidates per cycle); the NFR-013 helper reads all of them." Rationale: retention must cover the longest stated window.
- Quality impact: Completeness.

**PF-029** | MAJOR | Whittaker (Divergence) | FR-016 L158; FR-023 L161; NFR-009 L216; FR-020 L180 | Priority: Medium
- I can break this specification by Divergence. The invariant "each examined issue adds one decision line" (FR-020) and the FR-023 ordering diverge between two compliant implementations.
- Concrete attack: issues 7 and 8 are both eligible, and the per-cycle launch cap is 1.
  - Implementation A stops examining after launching 7.
  - Implementation B examines 8 and skips it with an unlisted reason (`cycle_cap`?).
  - Implementation B stamps 8 in `considered` and implementation A does not, so in cycle 2 their candidate orders differ.
  - Likewise, a `budget_exhausted` candidate is "examined" in one reading and stamped, which moves it to the back. Under a persistent budget squeeze, with more than 8 candidates at more than 4 calls each, that candidate starves forever.
- Recommendation: Add to FR-016: "After the cycle's launch, remaining candidates are not examined and not stamped. A `budget_exhausted` candidate is not stamped. A second eligible candidate is never reached." Rationale: one behaviour, one test.
- Quality impact: Testability, Consistency.

**PF-030** | MAJOR | Whittaker (Sentinel) | FR-014 L152-153; FR-015 L155; Section 7 L282 | Priority: Medium
- I can break this specification by Sentinel Value. The invariant "success JSON gives `launched` with `operation_id` stored" fails when Orca exits 0 with JSON lacking `operationId`, or with `""` or `null`.
- Concrete attack: the stub prints `{"ok":true}`. Is this "confirmed success", giving `launched` with `operation_id` null, or "malformed output", giving `unknown`? If it becomes `launched`, `status` may print `--retry-launch None` for a later `unknown`, and FR-015 applies to "an `unknown` entry with an `operation_id`", so the empty string matches.
- Recommendation: Add to FR-014: "Confirmed success requires exit 0 and JSON whose operation ID is a non-empty string; anything else is `unknown`; `status` prints a retry command only for a non-empty stored ID." Rationale: it closes the sentinel.
- Quality impact: Testability.

**PF-031** | MINOR | Whittaker (Accumulation) | Section 7 L259 | Priority: Low
- Issue: Tombstones are never pruned, so `dispatch.json` grows by up to 6 entries a day, about 2,200 a year. Every cycle rewrites the whole file with an fsync.
- Recommendation: State the expected size bound, or prune `claimed` tombstones older than 90 days whose issue is closed.
- Quality impact: Clarity.

### 9. Lisa Crispin

"The shadow run is the main pre-production test, and it cannot see past candidate ten."

**PF-037** | MAJOR | Crispin | FR-019 L176; FR-023 L161; runbook steps 3 and 9 L350, L356 | Priority: High
- Issue: Dry-run never writes `considered`. With more than 10 discovered issues, which are all never examined, every dry-run cycle examines the same first 10 in an order that is otherwise unspecified, and reports the same would-launch issue. The 24 h shadow therefore never exercises candidates 11 and above, the ordering of FR-023, or the day cap. Its "compare with expectation" review cannot detect a starvation bug.
- Recommendation: Add to FR-019: "Dry-run keeps a shadow `considered` map and a shadow launch count in `<state_dir>/dry-run.json`, never read by a non-dry-run cycle, so the shadow rotates through candidates and simulates the day cap." Rationale: the rehearsal must follow the production path.
- Quality impact: Testability.

**PF-038** | MAJOR | Crispin | Section 1 L35; NFR-005 L208; FU-1 L362; Section 3 L90 | Priority: Medium
- Issue: Every GitHub and Orca shape the predicates depend on is UNVERIFIED and pinned by `_assumed_shape` fixtures. FU-1 captures real JSON, but the deployment gate (L35) requires only that the slash command and the permission mode are proven. Cron can be enabled while the tests still pass against the guessed shapes.
- Recommendation: Replace L35's first sentence: "No cron entry is enabled until an owner-run live test shows the prompt running as a slash command, records the session's permission mode, and replaces every `_assumed_shape` fixture with captured replies under which `tests/issue_watch/` passes." Rationale: gate on the evidence the tests rely on.
- Quality impact: Testability.

**PF-039** | MINOR | Crispin | Section 8 Gates L328 | Priority: Low
- Issue: `make sync-dev` writes files, so it is a sync step, not a gate. `make verify-sync` is the gate.
- Recommendation: Move `make sync-dev` to a preparation step before the gates.
- Quality impact: Clarity.

### 10. Janet Gregory

"Run the arithmetic as a test, and look for where the boundaries sit."

**PF-040** | CRITICAL | Gregory | NFR-009 L216; Section 8 Budget arithmetic L343; FR-011 L143 | Priority: High
- Issue: The 35-call cap applies to "per-issue calls" only. The 2 shared calls (`api user`, discovery) sit outside it, so the worst cycle is 2 + 35 = 37 `gh` calls: 444 an hour, 8.88 percent, not "35, 420 per hour (8.4%)". The spec does not say whether the 3 re-read calls of FR-011 count toward the 35 cap. If they do not, the worst cycle is 40 calls, 480 an hour. The NFR-009 test ("call count with 10 candidates") cannot assert either figure.
- Recommendation: Replace the NFR-009 sentences: "Per-issue calls, including every page and the FR-011 re-read, stop at a 35-call cap per cycle. Idle cycle: 2 calls, 24 per hour (0.48%). Worst cycle: 37 calls, 444 per hour (8.88%)." Apply the same to L343. Rationale: the numbers must follow from the caps.
- Quality impact: Consistency, Testability.

**PF-041** | MAJOR | Gregory | NFR-014 L226; FR-024 L164; FR-028 L192; Section 7 L268-271 | Priority: High
- Issue: The day cap, backoff, lease, `next_permitted_at`, FR-029 deadlines and the FR-028 GWT ("a cycle 60 s later") all depend on time. NFR-014 says "Protocols exist only for the runner, the store and the launcher", which rules out an injectable clock. These tests then need monkeypatching or real sleeps.
- Recommendation: Replace the NFR-014 sentence: "Protocols exist only for the runner, the store, the launcher and the clock (`now() -> datetime` UTC and `monotonic()`); every time read goes through the clock." Rationale: time-boundary tests must be deterministic.
- Quality impact: Testability.

**PF-042** | MAJOR | Gregory | FR-024 L164; Section 7 L279, L286; FR-021 L182 | Priority: Medium
- Issue: No boundary states its inclusivity:
  - "falls in the last 24 h": is `consumed_at` exactly 24 h ago counted?
  - "backoff elapsed": `>` or `>=` 10 min?
  - "lease end";
  - "older than 24 h";
  - "above 900 s".

  Nor does the spec say when `launched` becomes `abandoned` `claim_not_observed`: in a cycle-start sweep over all entries, or only when the issue is re-examined. If the issue drops out of discovery, for example because its trigger was removed, the entry never transitions.
- Recommendation: Add to Section 7: "Windows are half-open: an instant t is inside [start, start + d) and outside at exactly start + d. Lease expiry and the `pending_orphan` check run at cycle start over every entry, whether or not the issue was discovered." Rationale: each boundary gets one test value.
- Quality impact: Testability.

### 11. Kelsey Hightower

"Operate it before trusting it. The threat model and the requirement disagree about who owns the allow-list."

**PF-043** | CRITICAL | Hightower | T13 L247; FR-027 L188 | Priority: High
- Issue: T13 states the mitigation as "File must be owner-owned and not group/other-writable, else exit 2 (FR-027)". FR-027 checks only "missing, empty or group/other-writable" and calls the file "owner-only" without defining it. A file owned by another local user with mode 0644 passes FR-027 and fails T13, and that user can rewrite the allow-list. The threat row cites a requirement that does not implement it.
- Recommendation: Replace the FR-027 sentence: "`once` exits 2 before any `gh` call if that file is missing, not a regular file, not owned by the effective UID, group/other-writable, or holds no valid ID (PF-026), using `check-config`'s validator." Rationale: the requirement must implement the threat mitigation.
- Quality impact: Consistency, Security.

**PF-044** | MAJOR | Hightower | Section 1 L35; T10 L244; FU-1 L362 | Priority: Medium
- Issue: The deployment gate "records the session's permission mode" but does not say where or in what form. A bypass mode needs "written acceptance", also with no location. Nothing an operator or reviewer can check shows that the gate was passed.
- Recommendation: Append to L35: "The live-test record (date, Orca version, observed prompt handling, permission mode, and any written acceptance) is committed as `docs/designs/issue-watcher-live-test.md`; runbook step 9 requires it." Rationale: a gate needs evidence that can be audited.
- Quality impact: Testability.

**PF-045** | MAJOR | Hightower | FR-017 L167 | Priority: Medium
- Issue: The lock rules cover held, missing and replaced locks. They do not cover a lock path that is a directory (open fails: which exit?), a symlink (followed, so its inode equals the target's and the check passes), or a regular file with the wrong owner or mode.
- Recommendation: Add to FR-017: "The lock is opened with `O_NOFOLLOW`; a lock path that is not a regular file owned by the effective UID exits 6." Rationale: it closes a blank guard cell.
- Quality impact: Completeness.

**PF-046** | MINOR | Hightower | FU-2 L363 | Priority: Low
- Issue: `0 */5 * * * *` is a six-field expression. The spec does not say that the first field is seconds (Coder's format), so a reader may copy it into a five-field crontab.
- Recommendation: Add "(six fields, seconds first: every 5 minutes at second 0)".
- Quality impact: Clarity.

**PF-047** | MINOR | Hightower | Runbook steps 3, 7 and 9, L350-356 | Priority: Low
- Issue: Steps 3, 7 and 9 each describe the 24 h shadow, which reads as two shadow runs.
- Recommendation: Merge them into one step: init-state, the shadow, the review, the lock test, the persistence check, and the alert.
- Quality impact: Clarity.

**PF-048** | MINOR | Hightower | Section 2 L51 | Priority: Low
- Issue: The network-filesystem deny-list omits `ceph`, `glusterfs`, `lustre`, `afs`, `fuse.rclone` and `fuse.gcsfuse`, all of which have unreliable `flock` semantics.
- Recommendation: Use an allow-list of local types (`ext4`, `xfs`, `btrfs`, `tmpfs`, `overlay`, `zfs`) instead.
- Quality impact: Completeness.

## Guard Condition Boundary Table

Cells are filled only from the spec. A blank or contradictory behaviour is a GAP and maps to a finding of at least MAJOR severity.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 build_claim_prompt | FR-012 L146 | Zero/Empty | `n = 0` | reject | `ValueError`, nothing launches; entry `failed` (FR-014) | OK |
| G1 | FR-012 | One/Minimal | `n = 1` | accept | `/sc:issue --claim 1` | OK |
| G1 | FR-012 | Typical | `n = 9` | accept | `/sc:issue --claim 9` | OK |
| G1 | FR-012 | Maximum/Overflow | `999999999` / `10**9` | accept / reject | string / `ValueError` | OK |
| G1 | FR-012 | Sentinel Value Match | `True`, `"9"` | reject | `ValueError` (not `bool`, not `str`) | OK |
| G1 | FR-012 | Legitimate Edge Case | `9.0`, `-1` | reject | `ValueError`; retried 3 times (PF-016, minor) | OK |
| G2 truncation | FR-003/FR-004 L116-119 | Zero/Empty | D = 0 | pass | exit 0, exactly 2 `gh` calls (FR-001) | OK |
| G2 | FR-004 | One/Minimal | D = 1 | pass | normal cycle | OK |
| G2 | FR-003 | Typical | D = 80 | pass + warn | warning line with `discovery_count` 80 | OK |
| G2 | FR-004 | Maximum/Overflow | D = 100 | fail closed | exit 4, zero launches, reason `truncated` | OK |
| G2 | FR-004 | Sentinel Value Match | repeated `number` in reply | none | not specified | GAP (PF-027) |
| G2 | FR-004 | Legitimate Edge Case | D = 101 (`-L` ignored) | "exactly 100" is false | not specified | GAP (PF-027) |
| G3 per-cycle caps | FR-016 L158; NFR-009 L216 | Zero/Empty | C = 0 | none | exit 0 | OK |
| G3 | FR-016 | One/Minimal | 1 eligible | launch 1 | one launch | OK |
| G3 | FR-016 | Typical | 10 candidates, 1 eligible | launch 1 | others skip with reasons | OK |
| G3 | FR-016/NFR-009 | Maximum/Overflow | 15 eligible, at least 4 calls each | cap 35 binds | GWT says 10 examined, then 5 left; arithmetic gives at most 8, then 7 left | GAP (PF-009) |
| G3 | FR-016 | Sentinel Value Match | second eligible after the launch | per-cycle cap 1 | reason and examination not specified | GAP (PF-029) |
| G3 | NFR-009/FR-023 | Legitimate Edge Case | cap reached at candidate k | `budget_exhausted` | `considered` stamping and re-read counting not specified | GAP (PF-029, PF-040) |
| G4 day cap 6 | FR-024 L164 | Zero/Empty | count 0 | pass | `pending` allowed | OK |
| G4 | FR-024 | One/Minimal | count 1 | pass | allowed | OK |
| G4 | FR-024 | Typical | count 5 | pass | sixth `pending` written | OK |
| G4 | FR-024 | Maximum/Overflow | count 6 | block | skip `day_cap`, no `pending` | OK |
| G4 | FR-024/L289 | Sentinel Value Match | one of the 6 was `reset` (entry removed) | count 5 | contradicts "still 6"; no store field keeps it | GAP (PF-024) |
| G4 | FR-024 | Legitimate Edge Case | `consumed_at` exactly 24 h ago | ? | inclusivity not specified; a clock jump is residual R16 | GAP (PF-042) |
| G5 lease 60 min | Section 7 L282, L286 | Zero/Empty | lease age 0 | hold | `launched` | OK |
| G5 | L287 | One/Minimal | marker at 1 min | claim | `claimed` | OK |
| G5 | L286 | Typical | 30 min, no marker | hold | `launched` | OK |
| G5 | L286 | Maximum/Overflow | age exactly 60 min | ? | boundary not specified | GAP (PF-042) |
| G5 | FR-014 L153 | Sentinel Value Match | success JSON, no `operationId` | ? | `launched` or `unknown` not specified | GAP (PF-030) |
| G5 | L286 | Legitimate Edge Case | issue leaves discovery before the lease ends | ? | when the transition runs is not specified | GAP (PF-042) |
| G6 attempts/launches | Section 7 L268, L278-281 | Zero/Empty | `attempts` 0, `launches` 0 | eligible | checks run | OK |
| G6 | L278 | One/Minimal | `attempts` 1 (transient re-read) | backoff | `failed`, 10 min | OK |
| G6 | L279 | Typical | `attempts` 2, backoff elapsed | eligible | re-runs every check | OK |
| G6 | L280 | Maximum/Overflow | `attempts` 3 | stop | `abandoned` `attempts_exhausted` | OK |
| G6 | L102 vs L291 | Sentinel Value Match | `abandoned` with `launches` 0 | passes L102 | re-eligible against "terminal" | GAP (PF-004) |
| G6 | L279 | Legitimate Edge Case | backoff exactly 10 min | ? | `>` or `>=` not specified | GAP (PF-042) |
| G7 allow-list | FR-027 L188; T13 L247 | Zero/Empty | empty file | reject | exit 2, zero `gh` calls | OK |
| G7 | FR-027 | One/Minimal | one valid ID | accept | approval by that ID passes | OK |
| G7 | FR-027 | Typical | mode 0664 | reject | exit 2 | OK |
| G7 | FR-027 | Maximum/Overflow | very large file, duplicates | ? | not specified | GAP (PF-026) |
| G7 | FR-027 | Sentinel Value Match | whitespace only, or a login in place of an ID | accept (non-empty) | silent no-op allow-list | GAP (PF-026) |
| G7 | T13 vs FR-027 | Legitimate Edge Case | other user's file, mode 0644 | FR-027 accepts, T13 rejects | contradictory | GAP (PF-043) |
| G8 lock | FR-017 L167 | Zero/Empty | lock missing | reject | exit 6 | OK |
| G8 | FR-017 | One/Minimal | lock free | acquire | cycle runs | OK |
| G8 | FR-017 | Typical | held by another process | reject | exit 75, no `gh`, `lock_held` | OK |
| G8 | FR-017 | Maximum/Overflow | inode changed or link count 0 | release | exit 75 | OK |
| G8 | FR-017 | Sentinel Value Match | path is a directory or symlink | ? | not specified | GAP (PF-045) |
| G8 | FR-017/FR-020 | Legitimate Edge Case | loser appends audit while holder rotates | ? | unlocked append against rotation | GAP (PF-023) |

## Pipeline Dimensional Analysis

| Stage | Count in | Count out | Rule (spec) |
|---|---|---|---|
| S0 shared | — | 2 calls | `api user` and discovery (FR-001, FR-002) |
| S1 discovery | open, trigger, `--assignee` own | D, 0 ≤ D ≤ 100 | D = 100 exits 4 (FR-004) |
| S2 filtering | D | F ≤ D | exact set {own} (FR-008); {own, other} dropped |
| S3 candidate selection | F | C = min(F, 10) | FR-023 order |
| S4 per-issue reads | C | E ≤ C | 35-call cap; a fully read candidate costs 4 or more calls; with the 3-call re-read reserved, E ≤ floor(32 / 4) = 8 |
| S5 eligibility | E | G ≤ E | Section 3 order |
| S6 caps | G | L = min(1, G) when day count < 6, t < 120 s and DISABLED absent; else 0 | FR-016, FR-024, FR-029, FR-018 |
| S7 launch | L ∈ {0, 1} | 1 Orca call | outcome `launched`, `unknown` or `abandoned` |

Quantity Flow Diagram (worst case, 15 eligible issues, 6 consumed in 24 h already = 5):

```
gh calls:  [S0: 2] -------------------------------------------+
discovery: D=15 --S2--> F=15 --S3--> C=10 --S4(35 cap)--> E=8 --S5--> G=8
                                       |                     |
                                       +- 2 skip budget_exhausted (stamped? PF-029)
S6 caps:   G=8 --(per-cycle 1, day count 5 < 6)--> L=1 --S7--> 1 launch
calls:     2 + 4*8 + 3 (re-read) = 37  (spec says worst 35)            [PF-040]
cycle 2:   unexamined = 15 - 8 = 7     (FR-016 GWT says 5)             [PF-009]
day:       launches over N=10 cycles = min(10, 6) = 6 (L325 says 10)   [PF-008]
```

Consumers that assume conservation:
- L325 acceptance assumes the launches over N cycles equal N. At N = 10 the actual count is 6, with 4 `day_cap` skips. This is CRITICAL, PF-008.
- The FR-016 GWT assumes E = 10, which leaves 5 for cycle 2. The actual E ≤ 8, which leaves 7. This is CRITICAL, PF-009.
- NFR-009 and L343 assume a total of 35 calls. The actual total is 37, or 40 if the re-read sits outside the cap. This is CRITICAL, PF-040.
- The FR-020 GWT assumes the number of decision lines equals E. The candidates after the launch and the `budget_exhausted` candidates make that count either E or C, and the spec does not say which. This is MAJOR, PF-029.
- FR-003's `discovery_count` counts D, not F: issues with assignee {own, other} count toward truncation. This is acceptable fail-closed behaviour and not a finding.

## Scores

- Clarity, 6 of 10: the requirements are precise sentence by sentence, but several cross-references ("same store write", "page cap", "owner-only") have no referent.
- Completeness, 5 of 10: the following are undefined:
  - the cycle order;
  - the approvers file format;
  - the reason enum;
  - schema migration;
  - audit retention;
  - the `enabled: false` behaviour.
- Testability, 6 of 10: every FR has a GWT. Two GWTs are arithmetically false, and the time-dependent tests have no clock seam.
- Consistency, 4 of 10: there are contradictions in:
  - the owner-rule equality;
  - the FR-014 order against FR-018 and FR-025;
  - `reset` against the day cap;
  - re-read failure mapping to both exit 7 and exit 0;
  - T13 against FR-027;
  - the budget arithmetic.
- Overall, 5.3 of 10: the design is sound and D1 to D3 are realised. The guarantees are undermined by internal contradictions that a refactor can fix textually.

## Consensus and disagreements

Consensus:
- At-most-once by a pre-launch `pending` write with an immutable counter is the right core. The panel agrees that the defects are in the guards around it, PF-024 and PF-025, not in the core.
- The per-launch order (FR-014) and the cycle order (PF-003) must be single, explicit lists. Wiegers, Whittaker and Nygard all reached the same point independently.
- The GWT examples must be recomputed from the stated caps (PF-008, PF-009, PF-040).

Disagreements:
- Fowler would delete the launcher Protocol (PF-019). Newman would keep it as the Orca contract boundary. The panel left it MINOR.
- Hohpe wants local checks first (PF-036). Wiegers notes that checking `launches > 0` early hides the `claimed` transition for `launched` entries. The recommended text keeps the marker read for entries awaiting a claim.
- Crispin's shadow `considered` (PF-037) adds a file. Hightower prefers to accept a shadow run that covers only 10 candidates and to document that limit. The panel kept MAJOR, because the runbook relies on the shadow as the rehearsal.
- Nygard would clamp `Retry-After` at 3600 s. Gregory notes that GitHub secondary limits can legitimately exceed that. The clamp value is [PROPOSAL].

## Findings that the refactor must apply

All 12 CRITICAL and 27 MAJOR findings. A row has the same text as the finding's recommendation. Some rows touch the same text, and three of those overlaps need care:
- PF-004 and PF-036 both edit L102. Apply PF-004's state rule in place of the clause "no entry with `launches > 0`" inside PF-036's ordering.
- PF-003 sets the cycle order and PF-025 sets the per-launch order. PF-025's list is the "launch steps" of PF-003.
- PF-026 and PF-043 both edit FR-027. PF-043's sentence includes PF-026's validity rule.

| ID | Sev | Target | Exact text |
|---|---|---|---|
| PF-001 | C | Section 3 Intended owner (L98); OD-3 | L98: "and is stricter than the claim's own rule (`refs/claim.md:41-42`), which also accepts an unassigned issue; the watcher never launches on an unassigned issue." OD-3: "A strict subset of the claim's rule" |
| PF-002 | C | FR-014 GWT | "In every case after the `pending` write, `launches` is 1; a failing probe writes no entry, and a pre-pending `failed` has `launches` 0." |
| PF-003 | C | FR-001 | "Cycle order: platform and config validation, approvers file, worktree existence (no external call); lock; DISABLED; `next_permitted_at`; `gh api user`; origin check (`git`); discovery; per-issue reads; Orca probe (only if a candidate is eligible); launch steps (FR-014)." |
| PF-004 | C | Section 3 Eligible issue (L102) | "no record entry, or an entry in `failed` whose backoff has elapsed with `attempts` < `max_attempts`; any other entry state is ineligible." |
| PF-005 | M | Section 3 Own login (L80) | "A login that does not match exits 3 with reason `login_invalid` before discovery." |
| PF-006 | M | Section 3 Complete event history (L92) | "The page cap is 5 pages per read [PROPOSAL], counted in the NFR-009 cap. An opposing tie is a `labeled` and an `unlabeled` event for the approval label, or approval and trigger `labeled` events, with equal `created_at` seconds; it skips `events_incomplete`." |
| PF-007 | M | Section 8 (new); FR-020; FR-022 | "Reason enum (closed): one table listing each reason, its source requirement and its exit; a failed events read is `events_unreadable`, distinct from `events_incomplete`." |
| PF-008 | C | Section 8 Acceptance (L325) | "Given N eligible issues (1 ≤ N ≤ 99) and an injected clock, each cycle launches at most one; within 24 h exactly min(N, 6) launch and the rest skip `day_cap`; after the clock advances 24 h the rest launch, one per cycle, each with the integer only." |
| PF-009 | C | FR-016 GWT | "Given 15 eligible issues of one page each and a per-candidate read count r, cycle 1 examines k = min(10, floor((35 − 3) / r)) and launches 1; cycle 2 examines the 15 − k never-examined issues first." |
| PF-010 | M | Section 7 Schema; FR-020 | "Add `approved_at` (the approval event's `created_at`) to the entry schema and to FR-020 decision lines." |
| PF-011 | M | NFR-013 (b), (d) | "(b) ≥ 99 percent of non-DISABLED, non-dry-run cycles over 7 days exit 0; (d) no `unknown` or `abandoned` `pending_orphan` entry stays more than 24 h without reaching `claimed` or being `reset`." |
| PF-013 | M | FR-027; runbook | FR-027: "With `enabled: false`, `once` exits 0 before any external call with audit reason `not_enabled`, and does not refresh health; `--dry-run` runs regardless of `enabled`." Runbook: "Set `enabled: true` after step 9." |
| PF-014 | M | Section 3 Claimed (L100); Section 7 transitions | L100: "It counts only if created or last edited after the entry's `pending_at` when set, otherwise after the current approval event." New row: "`failed` \| own marker newer than the current approval \| `claimed` \| `launches` 0" |
| PF-015 | M | FR-020 | "A crash, an exit 2 before `state_dir` is known, and an exit 6 for an unwritable state directory write one JSON line to stderr instead; every other exit appends to `audit.jsonl`." GWT: add exit 2 (valid config, bad worktree). |
| PF-017 | C | FR-013; NFR-014; Section 8 Modules | FR-013: "`<orca>` comes from `launch.find_orca(runner)`, which tries `_ORCA_CLIS` (`install_user_setup.py:35`) in order through the injected runner with the same `skills list --json` acceptance rule as `_find_orca`; a parity test pins the candidate list and the acceptance rule." NFR-014 and L301: "mirrors" in place of "reuses". |
| PF-018 | M | FR-023; FR-028 | FR-023: "written in the cycle's final store write, after the last entry write". FR-028: "makes no further state change except `next_permitted_at` and the `considered` stamps of candidates already examined; entries written earlier in the cycle stand." |
| PF-021 | C | Section 8 Failure modes (L341); exit table (L317) | L341: "One issue's events, Project item, marker, or a non-transient re-read failure (`revalidation_failed`)". L317: "7 \| An entry was written `failed` (pre-pending, `launches` 0), `unknown`, or `abandoned` `spawn_error` in this cycle" |
| PF-022 | M | FR-028 | "`next_permitted_at` is clamped to at most 3600 s after the reply; a larger or unparseable value is stored as 3600 s with audit reason `rate_limit_clamped`; `reset --rate-limit` clears it." |
| PF-023 | M | FR-020 | "Rotation happens only under the lock. Each line is one `O_APPEND` write; a process without the lock (exit 75) appends but never rotates." |
| PF-024 | C | Section 7 transitions (L289); Schema; FR-024 | "`reset` \| (none); the entry's `consumed_at` is appended to the store-level list `consumed_log` (pruned after 24 h), which FR-024 counts together with entries". Add `consumed_log` to the store schema. |
| PF-025 | C | FR-014 | "the Orca probe and worktree check (cached per cycle); the prompt build; the re-read; the day-cap count; the DISABLED check; the origin re-check (not cached); the `pending` write; the spawn." |
| PF-026 | M | FR-027 | "The file holds one decimal account ID per line matching `^[1-9][0-9]{0,19}$`; blank lines and lines starting with `#` are ignored; any other line, or zero IDs after that, exits 2; duplicates are collapsed." |
| PF-027 | M | FR-004 | "Discovery returning 100 or more results, or any repeated `number`, shall fail closed: exit 4 with zero launches." |
| PF-028 | M | FR-020 | "Rotation keeps `audit.jsonl.1` to `audit.jsonl.4` (at least 25 MiB, about 40 days at 10 candidates per cycle); the NFR-013 helper reads all of them." |
| PF-029 | M | FR-016 | "After the cycle's launch, remaining candidates are not examined and not stamped. A `budget_exhausted` candidate is not stamped. A second eligible candidate is never reached." |
| PF-030 | M | FR-014 | "Confirmed success requires exit 0 and JSON whose operation ID is a non-empty string; anything else is `unknown`; `status` prints a retry command only for a non-empty stored ID." |
| PF-032 | M | NFR-011 | "A store whose `schema_version` is lower than the code's is migrated in place under the lock by a pure, tested function that preserves every entry and `consumed_at`; only a higher or unknown version gives exit 6." |
| PF-033 | M | FR-009 | "A contract test asserts that `predicates.CLAIM_MARKER` occurs verbatim in `refs/claim.md` and `templates/claim-comment.md` of the `sc-issue-protocol` skill." |
| PF-034 | M | FR-013; Section 2 (L47) | "`<ORCA_AGENT>` is the module constant `ORCA_AGENT = "claude"` (seed brief, `--agent claude`)" |
| PF-035 | M | Section 3 Claimed (L100) | "Comparison against `pending_at` allows a skew tolerance of 300 s [PROPOSAL]; the cycle line records the `Date` header offset of the discovery reply, and an offset above 60 s writes a `clock_skew` warning line." |
| PF-036 | M | Section 3 Eligible issue (L102) | "Checks run local first: no entry with `launches > 0` unless testing for `claimed`; not in `failed` backoff; day cap not reached (otherwise skip `day_cap` before any per-issue call); then open, tagged, intended owner, approved, not claimed, unchanged, Project/Backlog." (merge with PF-004) |
| PF-037 | M | FR-019 | "Dry-run keeps a shadow `considered` map and a shadow launch count in `<state_dir>/dry-run.json`, never read by a non-dry-run cycle, so the shadow rotates through candidates and simulates the day cap." |
| PF-038 | M | Section 1 Deployment gate (L35) | "No cron entry is enabled until an owner-run live test shows the prompt running as a slash command, records the session's permission mode, and replaces every `_assumed_shape` fixture with captured replies under which `tests/issue_watch/` passes." |
| PF-040 | C | NFR-009; Section 8 Budget arithmetic (L343) | "Per-issue calls, including every page and the FR-011 re-read, stop at a 35-call cap per cycle. Idle cycle: 2 calls, 24 per hour (0.48%). Worst cycle: 37 calls, 444 per hour (8.88%)." |
| PF-041 | M | NFR-014 | "Protocols exist only for the runner, the store, the launcher and the clock (`now() -> datetime` UTC and `monotonic()`); every time read goes through the clock." |
| PF-042 | M | Section 7 | "Windows are half-open: an instant t is inside [start, start + d) and outside at exactly start + d. Lease expiry and the `pending_orphan` check run at cycle start over every entry, whether or not the issue was discovered." |
| PF-043 | C | FR-027; T13 | "`once` exits 2 before any `gh` call if that file is missing, not a regular file, not owned by the effective UID, group/other-writable, or holds no valid ID (PF-026), using `check-config`'s validator." |
| PF-044 | M | Section 1 Deployment gate (L35); runbook step 9 | "The live-test record (date, Orca version, observed prompt handling, permission mode, and any written acceptance) is committed as `docs/designs/issue-watcher-live-test.md`; runbook step 9 requires it." |
| PF-045 | M | FR-017 | "The lock is opened with `O_NOFOLLOW`; a lock path that is not a regular file owned by the effective UID exits 6." |

## Minor findings (notes only)

- PF-012 (Adzic, R3): write the threshold as "100 or more"; do not mix it with "more than 99".
- PF-016 (Cockburn, FR-014): a deterministic prompt `ValueError` should go straight to `abandoned` `invalid_number`, or the spec should say why it is retried.
- PF-019 (Fowler, NFR-014): either name the seam the tests fake for the launch, or drop the launcher Protocol.
- PF-020 (Fowler, NFR-002): the argv order is `gh api --method GET <path>`; the script is cited for its paging rule only.
- PF-031 (Whittaker, Section 7): tombstone growth (about 2,200 entries a year) needs a stated bound or a pruning rule.
- PF-039 (Crispin, Gates): `make sync-dev` is a preparation step, not a gate.
- PF-046 (Hightower, FU-2): say that the cron expression has six fields with seconds first.
- PF-047 (Hightower, runbook): merge steps 3, 7 and 9 into one shadow-rollout step.
- PF-048 (Hightower, Section 2): replace the network-filesystem deny-list with an allow-list of local filesystems.

Totals: 12 CRITICAL, 27 MAJOR, 9 MINOR (48 findings). Overall score 5.3 of 10.
