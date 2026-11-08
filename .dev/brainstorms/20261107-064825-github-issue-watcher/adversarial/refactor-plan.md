# Refactoring Plan: Merge into Base (Variant D)

## Overview

- **Base:** Variant D (`adversarial/blind/variant-D.md`, ranked first by both scoring passes). Section numbers below are D's: §1 Purpose and scope, §2 Fixed constraints, §3 Definitions, §4 Functional requirements (FR-001..FR-021), §5 Non-functional requirements (NFR-001..NFR-013), §6 Security model (T1..T12), §7 Dispatch record, §8 Deliverables, §9 Follow-ups (FU-1..FU-7), §10 Open decisions (OD-1..OD-9), §11 Risks (R1..R9), §12 Traceability. One new section is added: §13 Assumptions.
- **Incorporating from:** A (labels, owner function, argv, prompt builder, verbs, config, AST tests, closed skip-reason enum), B (Orca probe, paged events, `approver_id`/`approval_event_id`, FakeRunner exit 99, `_assumed_shape`, root causes), C (account IDs, consume-before-I/O, next-permitted time, `unknown` rule, concurrency and rename tests), E (per-issue `projectItems`, 35-call budget, day cap, `gh_calls`/`duration_ms`, `test_no_text`, budget arithmetic). D's own round-2 and round-3 additions are applied as base edits.
- **Inputs applied:** 24 points agreed in round 2 with a merged ruling; 13 points agreed in round 1 (leading approach); 4 points open after round 2 with round-3 final rulings (C-004, C-007, X-003, X-005) plus A-009; 20 adopted round-3 rulings on fault-finder findings (INV-010 is a documented residual risk only); the 10 shared assumptions A-001..A-010. `base-selection.md` does not exist; no strengths from it are applied.
- **Planned changes:** 74.
- **Overall risk:** Medium. Most changes tighten D's existing text. The structural changes are the dispatch-record states and transitions (§7 changes), the exit-code table (§8) and the removal of automatic `--retry-launch` (§4).
- **Conflict rulings applied throughout (each restated at the change it affects):**
  - **K1, "pre-pending failed" (C-007 vs INV-001).** `failed` is kept (C-007, 3 of 5: B, C, D) and given one producer only: a per-issue preparation failure that happens before the `pending` write (prompt `ValueError`, or a transient read error in the C-009 re-read). Shared host failures (Orca probe, worktree, origin) exit 2 and write no entry (INV-001, B and E). Nothing after `pending` ever becomes `failed` (INV-001, INV-002, unanimous). This keeps the majority's state set and the unanimous INV-001 invariant together; A's and E's request to delete `failed` loses 2 to 3.
  - **K2, C-009 order.** D's round-2 text wins over A's: re-read first, then `pending`, then Orca. INV-001 (5 of 5) requires every check before `pending`; A's "write `pending`, then re-read, then delete" would create entries INV-001 forbids. A negative re-read writes no entry (`revalidation_failed`); a transient re-read error is the K1 `failed` producer.
  - **K3, retry.** INV-003 (5 of 5 MODIFY; B, C: no automatic retry; A, D: gated on the live test; E: automatic) wins over C-011's `--retry-launch` sentence. v1 ships no automatic retry; the operator command and its gate move to §9.
  - **K4, exit precedence.** INV-006: 2, 6, 7, 5, 3, 4 (E's order; matches D and E on the top three, and A, B, D, E all rank 6 and 7 above 3, 4 and 5). Exit 75 is decided before precedence applies (lock not taken, nothing else ran).
  - **K5, `max_candidates`.** 10 (INV-015: B, D, E) wins over 5 (probe, C) and 8 (A). The 35-call cap (C-006) is the binding limit.
  - **K6, lock inode mismatch.** Exit 75 (INV-027: B, D, E) wins over 6 (A).
  - **K7, store creation.** `init-state` creates the store and lock (C-020 D text, INV-027 5 of 5); `check-config` stays read-only. This overrides A's C-020 and S-005 text "`check-config` creates it".
  - **K8, label and Project identity.** Labels by exact name (C-001, 5 of 5); Project by node ID `project_id` (INV-018; U-007 partial); Status field and Backlog option by name (INV-018: A, B, D, E against C).
  - **K9, INV-021 before INV-026.** The marker check runs first; own-login comments are exempt from the INV-026 freshness rule.
  - **K10, `reset` vs day cap.** `reset --forfeit-guarantee` clears `launches` but keeps `consumed_at` (INV-016), so it cannot bypass the day cap.
  - **K11, dry-run vs X-001/X-002.** Dry-run reports `pending_orphan` and `claim_not_observed` but writes neither (INV-005).
  - **K12, INV-014 vs C-004.** Discovery filters by `--assignee <own login>`, so `unassigned` and `assigned_other` are unreachable at discovery. The skip-reason enum keeps both names for `is_intended_owner`'s unit tests and for the C-009 re-read.
  - **K13, X-001 vs INV-004.** The lease moves `launched` to `abandoned` (`claim_not_observed`) as a report; it never moves `unknown` and never releases a slot.

## Planned Changes

### §1 Purpose and scope

#### Change 1: State the delivery guarantee precisely
- **Source:** INV-024 (round 3); E round-3 concession.
- **Target:** §1, after the first paragraph.
- **Approach:** insert.
- **Text:** "The poller starts at most one claim session per issue per intact, single dispatch store per login. A restored older backup of the store, or a second store on the same login, breaks this guarantee; both are documented residual risks (§11)."
- **Rationale:** INV-024 adopted 5 of 5 (all MODIFY); every advocate states the guarantee at this scope.
- **Risk:** Low.

#### Change 2: Mark the spec as deployment-gated
- **Source:** C-014 (round 2, 5 of 5, C's acceptance wording via A text).
- **Target:** §1, end.
- **Approach:** append.
- **Text:** "No cron entry is enabled until an owner-run live test shows the prompt running as a slash command and records the session's permission mode. The default is no override. A bypass mode requires the owner's written acceptance."
- **Rationale:** C-014 AGREED round 2, 5 of 5.
- **Risk:** Low.

### §2 Fixed constraints

#### Change 3: Restate D1-D3 verbatim and fix the agent
- **Source:** X-008 (round 2, 5 of 5, A text).
- **Target:** §2, constraint list.
- **Approach:** replace the D1-D3 lines with the seed-brief wording, then add the agent line.
- **Text:** "The launch uses `--agent claude` exactly, as in the seed, and the agent is not configurable. D1-D3 are restated verbatim. The poller reads no comment content beyond the boolean marker projection, which rejects C §6's 'bounded comment content'."
- **Rationale:** X-008 AGREED round 2, 5 of 5. E's `--agent <agent>` is not adopted.
- **Risk:** Low.

#### Change 4: Replace NG-2 "GET only" with a read-only rule that admits GraphQL queries
- **Source:** X-005 and INV-018 (round 3); C-003 (round 1, E); INV-009 (E's GraphQL timeline, UNVERIFIED).
- **Target:** §2, NG-2.
- **Approach:** replace.
- **Text (synthesized):** "NG-2: The poller never writes to GitHub. It issues no REST call with a verb other than GET. GraphQL requests use POST only with a query string that is a module constant containing no `mutation`. A unit test scans every constant and every recorded argv."
- **Rationale:** X-005's final ruling requires `projectItems`, which is GraphQL; D's "GET only" forbade it. INV-018 5 of 5.
- **Risk:** Medium (the test is the only enforcement).

#### Change 5: Add the platform constraint
- **Source:** INV-027 (round 3, 5 of 5); A-007.
- **Target:** §2, new line after the repo-pinning line.
- **Approach:** insert.
- **Text:** "Linux only. On any other platform `once`, `check-config` and `init-state` exit 2. `once` and `check-config` refuse a state directory on a network filesystem, detected from `/proc/self/mountinfo` (deny-list: nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p)."
- **Rationale:** INV-027 adopted 5 of 5; `flock` semantics need a local filesystem (A-007).
- **Risk:** Low.

#### Change 6: Extend NG-5 with "no automatic retry in v1"
- **Source:** INV-003 (round 3, 5 of 5 MODIFY); K3.
- **Target:** §2, NG-5.
- **Approach:** append.
- **Text:** "v1 makes no automatic Orca retry. A launch that ends `unknown` stays `unknown` until an own claim marker appears or the operator acts."
- **Rationale:** INV-003; conflict K3.
- **Risk:** Low.

### §3 Definitions

#### Change 7: Own login and account ID
- **Source:** C-004 (round 3 final); INV-007 (LOW, closed by the `launch_login` field); C §7 (U-007 partial).
- **Target:** §3, "Own login".
- **Approach:** replace.
- **Text:** "Own login and own account ID are read once per cycle from one `gh api user` call (`.login`, `.id`). The login must match `^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$`. If `owner_account_id` is configured and differs from `.id`, the cycle exits 2 before any other `gh` call."
- **Rationale:** C-004 round 3 majority (A, D, E HYBRID); D adds the configured-ID check. INV-007 adopted as a record field (§7).
- **Risk:** Low.

#### Change 8: Tagged
- **Source:** C-001 (round 2, 5 of 5, A text).
- **Target:** §3, "Tagged".
- **Approach:** replace.
- **Text:** "The trigger label `issue-watch:trigger` and the approval label `issue-watch:approved` are configurable and matched by exact, case-sensitive name. A missing or renamed label matches nothing, so nothing launches. The owner creates the labels; code never does."
- **Rationale:** C-001 AGREED round 2, 5 of 5. K8.
- **Risk:** Low.

#### Change 9: Approved by a human
- **Source:** C-002 (round 1, H, 4 of 5); C-013 (round 2, 5 of 5); INV-008 (round 3, 5 of 5 ACCEPT); INV-024 (round 3, 5 of 5).
- **Target:** §3, "Approved", conditions (a)-(d).
- **Approach:** replace.
- **Text (synthesized from the four rulings):**
  - (a) The issue carries the approval label now.
  - (b) The latest `labeled` event for the approval label, read from complete event history, has an actor with `type` `User`, a login not ending `[bot]`, and an account ID in the approver allow-list.
  - (c) That event is later than the latest `labeled` event for the trigger label; a reversed order skips as `approval_before_trigger` (INV-008).
  - (d) That event is later than the store's `created_at`; an older one skips as `approval_before_init` (INV-024).
  - (e) No `unlabeled` event for the approval label follows it.
  - The approving event's `actor.id` and event `id` go into the record as `approver_id` and `approval_event_id`.
- **Rationale:** C-002 leading H (A bot exclusion, B paged events, C account IDs and fail-on-incomplete, B record fields); INV-008 unanimous; INV-024 5 of 5.
- **Risk:** Medium (event shape UNVERIFIED until the live test; mocks pin it via `_assumed_shape`).

#### Change 10: Complete event history
- **Source:** INV-009 (round 3, 5 of 5 MODIFY).
- **Target:** §3, new definition after "Approved".
- **Approach:** insert.
- **Text (synthesized):** "Events are read with `per_page=100` as in `poll-augment-review.sh:46-56`: a page under 100 ends the read; a repeated event ID, a page with no progress, or the page cap marks history incomplete. Order is (`created_at`, `id`); an opposing same-second tie fails closed. GraphQL is complete only when `hasNextPage` is false. Incomplete history skips `events_incomplete`."
- **Rationale:** INV-009 5 of 5. E's newest-first GraphQL read is allowed as the build choice, tagged UNVERIFIED.
- **Risk:** Medium.

#### Change 11: Unchanged since approval
- **Source:** INV-026 (round 3, 4 of 5; E rejects); K9.
- **Target:** §3, new definition after Change 10's.
- **Approach:** insert.
- **Text (synthesized):** "The issue body and every comment not authored by the own login were created and last edited before the approval event, and no `renamed` event follows it. Otherwise skip `edited_after_approval`; re-applying the approval label re-arms the issue. `lastEditedAt` availability is UNVERIFIED. This check runs after the claim-marker check."
- **Rationale:** INV-026 ADDRESSED 4 of 5 (HIGH threshold met). B's extension (also exempt allow-listed approver IDs) is a minority and not applied. The poller reads timestamps only, never text (C-025).
- **Risk:** Medium (any commenter can stall an issue until re-approval; §11 row).

#### Change 12: In a Project and in Backlog
- **Source:** C-003 (round 1, E, 4 of 5); X-005 (round 3 final); INV-018 (round 3, 5 of 5).
- **Target:** §3, "In a Project" and "Backlog"; delete the ASSUMPTION on `gh project item-list`.
- **Approach:** replace both definitions with one.
- **Text:** "In a Project and in Backlog: the issue has exactly one non-archived item in the Project whose node ID is `project_id`, read from the issue's own `projectItems` over all pages, and that item's field named `Status` holds the option named `Backlog`. Any other result skips `project_mismatch`. There is no label-only mode."
- **Rationale:** X-005 final ruling (D majority 3 of 5 in round 2, confirmed in round 3); INV-018 5 of 5; K8.
- **Risk:** Medium (`read:project` scope UNVERIFIED; §9).

#### Change 13: Intended owner
- **Source:** C-004 (round 3 final); INV-014 (round 3, 5 of 5); K12.
- **Target:** §3, "Intended owner".
- **Approach:** replace.
- **Text:** "The intended owner is the issue whose assignee set equals exactly {own login}, where the login is read each cycle by `gh api user`. The rule lives in one pure function, `is_intended_owner`, and equals the claim's own rule. The account ID is stored in each record."
- **Rationale:** C-004 round 3 majority (A, D, E). Discovery pre-filters by `--assignee` (Change 16).
- **Risk:** Low.

#### Change 14: Claimed
- **Source:** C-024 (round 2, 5 of 5); INV-021 (round 3, 3 of 5).
- **Target:** §3, "Claimed".
- **Approach:** replace.
- **Text:** "`claimed` requires an own-login comment containing `<!-- sc:issue:claim -->`, read over all comment pages through a `--jq` boolean projection. It counts only if created or last edited after the entry's `pending_at`, or, with no entry, after the current approval event. Assignment alone is not evidence."
- **Rationale:** C-024 AGREED 5 of 5; INV-021 ADDRESSED 3 of 5 (A, D, E). `claim.md:29,43,84-88` edits the marker in place, so a re-run moves `updated_at`.
- **Risk:** Medium (residual: hand claims; §11).

#### Change 15: Eligible
- **Source:** composition of Changes 8-14; C-015 (round 2, 4 of 5).
- **Target:** §3, "Eligible".
- **Approach:** replace.
- **Text:** "Eligible: open; tagged; assigned to the intended owner; approved; not claimed; unchanged since approval; in the configured Project in Backlog; no record entry with `launches > 0`; not in `failed` backoff. Checks run in this order and the first failure is the skip reason. Absent or incomplete evidence never counts as positive."
- **Rationale:** C-015 ruling text ("Absent or incomplete evidence never counts as positive"); K9 order.
- **Risk:** Low.

### §4 Functional requirements

#### Change 16: Rewrite every FR in "shall + Given/When/Then" form
- **Source:** S-001 (round 2, 5 of 5, A text).
- **Target:** §4 and §5, all requirements.
- **Approach:** restructure.
- **Text:** "Each requirement is one 'shall' sentence with an ID, plus one Given/When/Then line that names the stub call or file it observes. Argv lists, paths and markers are written verbatim wherever they form the contract."
- **Rationale:** S-001 AGREED round 2, 5 of 5. Keep D's IDs; new requirements take FR-022 onward.
- **Risk:** Low.

#### Change 17: FR-003 discovery
- **Source:** C-006 (round 2, 4 of 5, A text); INV-014 (round 3, 5 of 5); D round-3 warning.
- **Target:** §4, FR-003.
- **Approach:** replace.
- **Text:** "Discovery is one `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <own login> --json number,labels,assignees,state -L 100`. Non-owned issues are dropped before any per-issue call. A `discovery_count` of 80 or more writes a warning audit line."
- **Rationale:** C-006 AGREED; INV-014 adds `--assignee` (the scaling fix; idle stays 2 calls). Paginated discovery (C) is a minority; not applied.
- **Risk:** Low.

#### Change 18: FR-004 truncation
- **Source:** C-006 (round 2); INV-014 (round 3).
- **Target:** §4, FR-004.
- **Approach:** replace.
- **Text:** "Exactly 100 discovery results exits 4 with zero launches. The runbook action is to remove the trigger label from claimed issues."
- **Rationale:** C-006, INV-014 residual (the cliff moves to one owner's own backlog).
- **Risk:** Low.

#### Change 19: FR-007 Project read failure
- **Source:** X-005 (round 3 final); C-015 (round 2).
- **Target:** §4, FR-007.
- **Approach:** replace ("voids the cycle" becomes per-issue).
- **Text:** "An unreadable Project item skips that issue (`project_unreadable`). A missing `read:project` scope voids the cycle with exit 3."
- **Rationale:** X-005 final ruling text; C-015 per-issue scope.
- **Risk:** Low.

#### Change 20: New FR-022, shared versus per-issue failures
- **Source:** C-015 (round 2, 4 of 5, A text).
- **Target:** §4, after FR-007.
- **Approach:** insert.
- **Text:** "Failures of shared inputs (login, discovery, allow-list, record store, rate limit, Project scope) void the cycle with zero launches. Per-issue read failures (events, Project item, marker, re-read) skip only that issue, with a reason. Absent or incomplete evidence never counts as positive."
- **Rationale:** C-015 AGREED round 2.
- **Risk:** Low.

#### Change 21: FR-011 pre-launch re-read and `pending` write
- **Source:** C-009 (round 2, 5 of 5, D text); K2; INV-012; INV-011.
- **Target:** §4, FR-011.
- **Approach:** replace.
- **Text:** "Under the lock, re-read state, labels, assignees, approval and Project Status. A failed or unreadable re-read skips `revalidation_failed`, writes no entry, launches nothing. Only then durably write `pending` with `launches` incremented, then call Orca. A `pending` at cycle start becomes `abandoned` `pending_orphan`."
- **Rationale:** C-009 AGREED 5 of 5; D's ordering wins over A's (K2) because INV-001 forbids a write before every check passes. Exception from K1: a transient re-read I/O error (timeout, 5xx) writes `failed` instead of nothing (Change 22).
- **Risk:** Medium.

#### Change 22: FR-014 launch preparation order and the "pre-pending failed" resolution
- **Source:** INV-001 (round 3, 5 of 5); C-007 (round 3, 3 of 5 keep `failed`); K1.
- **Target:** §4, FR-014.
- **Approach:** replace.
- **Text (synthesized, named resolution "pre-pending failed"):** "Per launch, in order: DISABLED check; Orca probe, worktree and origin check (shared, cached per cycle; failure exits 2, no entry); prompt build; re-read; `pending` write; spawn. A prompt `ValueError` or transient re-read error writes `failed` (`launches` 0, `attempts`+1). Nothing after `pending` becomes `failed`."
- **Rationale:** INV-001 5 of 5 (D's order); C-007 majority keeps `failed`; B and E put shared host checks before any entry. A and E wanted `failed` removed (2 of 5): overruled.
- **Risk:** High (the core at-most-once order; covered by crash-injection tests, Change 44).

#### Change 23: FR-014 continued, outcome after spawn
- **Source:** C-011 (round 2, 5 of 5, D text); INV-002 (round 3, 5 of 5 ACCEPT); X-004 (round 1, C, 4 of 5).
- **Target:** §4, FR-014 second sentence ("any other non-zero exit becomes `failed`").
- **Approach:** replace.
- **Text:** "Any outcome after Orca is spawned other than confirmed success (timeout, malformed output, `agent_session_operation_unknown`, non-zero exit) is `unknown`, with the slot consumed. An exec `OSError` before the child starts is `abandoned` `spawn_error`."
- **Rationale:** C-011 and INV-002 unanimous; A's "definite Orca error gives retryable `failed`" is withdrawn (INV-002). D adds `spawn_error` (round 3).
- **Risk:** Medium.

#### Change 24: FR-015 `--retry-launch` removed from v1
- **Source:** INV-003 (round 3, 5 of 5 MODIFY); K3.
- **Target:** §4, FR-015.
- **Approach:** replace.
- **Text (synthesized):** "v1 performs no automatic `--retry-launch`. For an `unknown` entry with an `operation_id`, `status` prints the operator retry command run from the stored `launch_cwd`. Enabling retry is a follow-up gated on the live test proving Orca's retry rule (§9)."
- **Rationale:** INV-003 majority synthesis (B, C: no retry; A, D: gate on live test). E's automatic retry is a minority. The conditions any later retry must meet are carried to §9 (Change 66).
- **Risk:** Low.

#### Change 25: FR-016 caps
- **Source:** C-008 (round 2, 5 of 5, A text); INV-015 (round 3); K5.
- **Target:** §4, FR-016.
- **Approach:** replace.
- **Text:** "[PROPOSAL] values: lease 60 min, `max_attempts` 3, one fresh launch per issue, one launch per cycle, `max_candidates` 10, 10-minute backoff after `failed`, `gh` timeout 20 s, `orca` timeout 120 s, and at most 6 fresh launches per rolling 24 hours."
- **Rationale:** C-008 AGREED 5 of 5; K5 keeps 10. Day-cap counting moves to Change 27.
- **Risk:** Low.

#### Change 26: New FR-023, least-recently-examined ordering
- **Source:** INV-015 (round 3, 5 of 5 MODIFY); INV-022 (LOW, covered).
- **Target:** §4, after FR-016.
- **Approach:** insert.
- **Text (E text, trimmed):** "A `considered` map (issue to `last_examined_at`) is written in the same store write, set for every examined candidate including skips, oldest first, never-examined first, pruned to the discovery set. Written only on cycles that examined something; never in dry-run."
- **Rationale:** INV-015 5 of 5. Closes INV-022 (a failing re-read no longer starves others).
- **Risk:** Low.

#### Change 27: New FR-024, rolling day cap
- **Source:** INV-016 (round 3, 5 of 5); K10.
- **Target:** §4, after FR-023.
- **Approach:** insert.
- **Text (synthesized):** "Each `pending` write sets an immutable `consumed_at`. Before a `pending` write, count entries in any state whose `consumed_at` falls in the last 24 h; at 6, skip `day_cap`. Tombstones and `reset` keep `consumed_at`. An entry recorded from a marker alone has none."
- **Rationale:** INV-016 5 of 5 (E's marker-only clause).
- **Risk:** Low.

#### Change 28: FR-017 lock
- **Source:** C-018 (round 2, 4 of 5, A text); INV-027 (round 3, 5 of 5); K6; K7.
- **Target:** §4, FR-017.
- **Approach:** replace.
- **Text (synthesized):** "A non-blocking `flock` on `<state_dir>/lock` is held for the whole cycle. Held: no external call, audit `lock_held`, exit 75. After acquiring, if the fd's (dev, inode) differs from the path's or link count is 0, release and exit 75. A missing lock exits 6. Only `init-state` creates it; nothing deletes it."
- **Rationale:** C-018 AGREED; INV-027 adopted 5 of 5; the (dev, inode) check is house practice (`launch-job-identity.sh:146-157`).
- **Risk:** Medium.

#### Change 29: FR-018 DISABLED, including mid-cycle
- **Source:** C-018 (round 2); INV-012 (round 3, 5 of 5).
- **Target:** §4, FR-018.
- **Approach:** append.
- **Text:** "DISABLED is checked again before each `pending` write (and before each retry, if retry is ever enabled). If present, start nothing further, audit `disabled_mid_cycle`, exit 0 without a health refresh. A spawn already started cannot be stopped."
- **Rationale:** INV-012 5 of 5; E's placement (before the write, never after).
- **Risk:** Low.

#### Change 30: New FR-025, origin check
- **Source:** INV-011 (round 3, 5 of 5 MODIFY); C-010 (round 2).
- **Target:** §4, after FR-018.
- **Approach:** insert.
- **Text (synthesized):** "Run `git -C <abs> remote get-url origin` through the injected runner, parse with the `parse_origin_url` rules (`origin_repo.py:86-99`), compare case-insensitively to `ironbellyorg/ironclaude`. Check at cycle start (exit 2) and again just before the `pending` write. A parity test pins the parser against `parse_origin_url`."
- **Rationale:** INV-011 5 of 5; E and B placement (a check after the write would orphan an entry). `read_origin` calls `subprocess` directly, so it is not reused.
- **Risk:** Low.

#### Change 31: Launch argv and Orca probe
- **Source:** C-010 (round 2, 5 of 5, A and D text); U-004 (B probe).
- **Target:** §4, the launch FR (D's FR-012/FR-013 launch text).
- **Approach:** replace.
- **Text:** "The argv is `[<orca>, agent, launch, --agent, claude, --worktree, path:<abs>, --surface, terminal, --prompt, <prompt>, --json]`. `<orca>` comes from `_find_orca()`, run through the injected runner; its 10 s timeout counts toward the cycle budget. `<abs>` must exist and its origin must be IronbellyOrg/IronClaude, else exit 2."
- **Rationale:** C-010 AGREED 5 of 5; D adds the runner rule (`install_user_setup.py:198-221` calls `subprocess.run` today).
- **Risk:** Low.

#### Change 32: Prompt builder
- **Source:** C-012 (round 2, 5 of 5, A text).
- **Target:** §4, the prompt FR.
- **Approach:** replace.
- **Text:** "`build_claim_prompt(n)` accepts only an `int` (not `bool`) in 1..999999999 and returns `/sc:issue --claim <n>`; any other value raises `ValueError` and nothing launches. A property test asserts that every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`."
- **Rationale:** C-012 AGREED; implements D3. Closes INV-013.
- **Risk:** Low.

#### Change 33: FR-019 dry-run
- **Source:** INV-005 (round 3, 5 of 5); K11.
- **Target:** §4, FR-019.
- **Approach:** replace.
- **Text (synthesized):** "`--dry-run` requires an initialised store and takes the lock. It performs all reads, honours a persisted next-permitted time, and writes audit lines tagged `dry_run`. Store, backoff, rate-limit time, `considered` and health timestamps stay byte-identical. It never calls Orca, reports the probe as skipped, and reports but does not write `pending_orphan` or `claim_not_observed`."
- **Rationale:** INV-005 5 of 5.
- **Risk:** Low.

#### Change 34: FR-020 audit log
- **Source:** C-019 (round 1, H, 4 of 5); D round-2 drop of `rate_remaining`; U-013.
- **Target:** §4, FR-020.
- **Approach:** replace.
- **Text (synthesized from the leading H):** "Every exit appends to `audit.jsonl`: `ts`, `host`, `login`, `cycle_id`, `exit`, `gh_calls`, `duration_ms`, `dry_run`, and per-decision lines with issue number, closed-enum reason, `approver_id`, `approval_event_id`. Rotated at 5 MiB. No title, body or comment text is ever logged."
- **Rationale:** C-019 leading H (D file, A enum, E counters, B decision lines). `rate_remaining` dropped (D round 2).
- **Risk:** Low.

#### Change 35: FR-021 status and health
- **Source:** C-018 (round 2, D text); INV-006 (round 3); INV-004 (round 3); D round-2 SLO (d).
- **Target:** §4, FR-021.
- **Approach:** replace.
- **Text (synthesized):** "`status [--json]` reports `last_completed_cycle_age_seconds`, refreshed only by an exit-0 cycle that is neither DISABLED nor dry-run; `disabled_since`; entries by state; every `unknown` or `pending_orphan` older than 24 h; and the retry command for `unknown` entries with an `operation_id`. Age above 900 s is unhealthy."
- **Rationale:** C-018 AGREED 4 of 5 (D); INV-006 health rule; INV-004 24 h listing.
- **Risk:** Low.

#### Change 36: New FR-026, CLI verbs
- **Source:** C-020 (round 2, 5 of 5, D text); K7; K10.
- **Target:** §4, after FR-021.
- **Approach:** insert.
- **Text:** "Verbs: `once [--dry-run]`, `status [--json]`, read-only `check-config`, `init-state` (creates the store and refuses if one exists), and `reset <N> --forfeit-guarantee` (only on `abandoned`, under the lock, audited, prints that N may launch twice). Exit codes as in X-007."
- **Rationale:** C-020 AGREED; D's text wins over A's "`check-config` creates the store" (K7, INV-027). `reset` keeps `consumed_at` (K10).
- **Risk:** Low.

#### Change 37: New FR-027, configuration and approver file
- **Source:** C-021 (round 1, A, 4 of 5); C-013 (round 2, 5 of 5); INV-019 (round 3, 5 of 5); C-005 (round 2).
- **Target:** §4, after FR-026.
- **Approach:** insert.
- **Text (synthesized):** "Config is JSON at `~/.config/superclaude/issue-watch.json` (no `tomllib` on 3.10), `enabled: false` by default, holding labels, `project_id`, `owner_account_id`, `worktree`, `state_dir`. Approvers are account IDs in an owner-only file. `once` exits 2 before any `gh` call if that file is missing, empty or group/other-writable, using `check-config`'s validator."
- **Rationale:** C-021 leading A; C-013 and INV-019 unanimous; C-005 default off.
- **Risk:** Low.

#### Change 38: New FR-028, rate limit
- **Source:** C-016 (round 1, H, 5 of 5); X-006 (round 1, H, 4 of 5); X-007 (round 2).
- **Target:** §4, after FR-027.
- **Approach:** insert.
- **Text (synthesized):** "On a primary or secondary rate-limit reply, stop with no state change except a persisted next-permitted-request time (from `Retry-After` or the reset header), audit `rate_limited`, exit 5. Every later cycle before that time exits 5 with zero `gh` calls."
- **Rationale:** C-016 and X-006 leading H (C's persisted time plus the hard cap).
- **Risk:** Low.

#### Change 39: New FR-029, wall-clock deadline
- **Source:** INV-017 (round 3, 5 of 5); C-008 timeouts.
- **Target:** §4, after FR-028.
- **Approach:** insert.
- **Text (synthesized):** "Each `gh` and probe call times out at the lesser of its configured value and the time left before 240 s; no new `gh` call starts with under 5 s left. No launch starts after 120 s. A started launch is never cut short; its own 120 s timeout applies and a timeout gives `unknown`. The record is written before exit."
- **Rationale:** INV-017 adopted 5 of 5 (E's 5 s bound and wall-time arithmetic: worst about 245 s inside the 300 s cadence).
- **Risk:** Low.

### §5 Non-functional requirements

#### Change 40: NFR-002 allowed external argv
- **Source:** Change 4 (NG-2); C-010; INV-011; INV-018; C-025 (round 1, H, 4 of 5).
- **Target:** §5, NFR-002.
- **Approach:** replace the prefix list.
- **Text (synthesized):** "Every runner argv starts with one of: `gh api user`; `gh issue list`; `gh api --method GET repos/IronbellyOrg/IronClaude/...`; `gh api graphql -f query=<module constant>`; `git -C <abs> remote get-url origin`; the `_find_orca` probe; the Orca launch argv. No argv requests `title`, `body` or comment `body` fields; marker and edit checks are `--jq` boolean or timestamp projections."
- **Rationale:** D's prefix list omitted GraphQL, git and the probe that later rulings require; C-025 requests no text.
- **Risk:** Medium (a missed prefix fails the security test, which is the intent).

#### Change 41: NFR-003 repo and Project pinning
- **Source:** C-003, X-005, INV-018.
- **Target:** §5, NFR-003; delete the `project item-list --owner IronbellyOrg` clause.
- **Approach:** replace.
- **Text:** "Every repository-scoped call names `IronbellyOrg/IronClaude` literally. Project reads go only through the issue's `projectItems` filtered to the configured `project_id`."
- **Rationale:** `gh project item-list` is no longer used (X-005 final ruling).
- **Risk:** Low.

#### Change 42: NFR-005 crash safety and test matrix
- **Source:** C-022 (round 1, H, 5 of 5).
- **Target:** §5, NFR-005.
- **Approach:** replace.
- **Text (synthesized from the leading H):** "Tests cover: an AST `test_no_shell`; stub end-to-end; crash injection at every write and spawn boundary, each followed by 5 reruns with zero second launches; two concurrent processes on one state dir; an account rename; `FakeRunner` exiting 99 on any unexpected argv; `_assumed_shape` fixtures for unverified GitHub shapes; `test_no_text`; a 50-cycle at-most-once run."
- **Rationale:** C-022 AGREED 5 of 5 (A, D, C, B, E parts).
- **Risk:** Low.

#### Change 43: NFR-006 audit content
- **Source:** C-019; C-025; D round 2.
- **Target:** §5, NFR-006.
- **Approach:** replace ("carries `rate_remaining`" removed).
- **Text:** "Audit lines carry `host`, never `rate_remaining`. Rotation at 5 MiB. A `PWNED-TITLE` fixture title and body never appear in any argv, audit line, record or prompt (`test_no_text`)."
- **Rationale:** C-019 and C-025 leading H; D's round-2 drop.
- **Risk:** Low.

#### Change 44: NFR-008 timeouts
- **Source:** C-008, INV-017.
- **Target:** §5, NFR-008.
- **Approach:** replace.
- **Text:** "`gh` timeout 20 s [PROPOSAL]; Orca timeout 120 s [PROPOSAL]; cycle deadline 240 s; no launch starts after 120 s (FR-029)."
- **Rationale:** C-008 5 of 5; INV-017 5 of 5.
- **Risk:** Low.

#### Change 45: NFR-009 call budget
- **Source:** C-006 (round 2, 4 of 5); S-003 (E budget arithmetic); E round-3 cost figures; X-007.
- **Target:** §5, NFR-009 ("33 calls; rate limit is exit 3").
- **Approach:** replace.
- **Text (synthesized):** "Per-issue calls, including every page, stop at a 35-call cap per cycle; candidates beyond it skip `budget_exhausted`. Idle cycle: 2 calls, 24 per hour (0.48% of 5,000). Worst cycle: 35, 420 per hour (8.4%). W workspaces on one login multiply both by W. Rate limit is exit 5 (FR-028)."
- **Rationale:** C-006 AGREED; X-007 moves rate limit to 5.
- **Risk:** Low.

#### Change 46: NFR-011 record integrity
- **Source:** X-003 (round 3 final); S-005 (round 2, 5 of 5, D text); X-007.
- **Target:** §5, NFR-011 ("unparseable record is exit 5").
- **Approach:** replace.
- **Text:** "An unparseable store, an unknown `schema_version`, or a store or lock missing after `init-state` gives exit 6 and zero launches. The file is never changed or reset. Recovery: move the state directory aside and run `init-state`, which sets a new `created_at`, so earlier approvals are not re-dispatched. Backup restore is unsupported."
- **Rationale:** X-003 final ruling (D majority, E text); exit renumbered by X-007.
- **Risk:** Low.

#### Change 47: NFR-013 SLOs
- **Source:** U-011 (D SLOs); D round 2.
- **Target:** §5, NFR-013.
- **Approach:** replace (b), append (d).
- **Text:** "(b) counts only exit-0 cycles. (d) No `unknown` or `pending_orphan` entry stays unacknowledged for more than 24 h."
- **Rationale:** D's round-2 additions; agreed with INV-004 and INV-006.
- **Risk:** Low.

#### Change 48: New NFR-014, module boundaries
- **Source:** S-004 (round 2, 4 of 5, A text).
- **Target:** §5, after NFR-013 (and §8 module list, Change 61).
- **Approach:** insert.
- **Text:** "The package `src/superclaude/cli/issue_watch/` holds `runner`, `github`, `predicates`, `record` (store and lock), `launch`, `audit`, `cycle` and `cli`. Protocols exist only for the runner, the store and the launcher. It reuses `swarm/atomic.write_prepared_bytes` and `_find_orca`. No module is named `select`."
- **Rationale:** S-004 AGREED round 2.
- **Risk:** Low.

### §6 Security model

#### Change 49: T4 body edited after approval
- **Source:** INV-026 (round 3, 4 of 5).
- **Target:** §6, T4 row ("poller has none, RD Q11 UNVERIFIED").
- **Approach:** replace the mitigation cell.
- **Text:** "Mitigation: the 'unchanged since approval' check (§3) skips any issue whose body or non-own comments were created or edited after approval, or renamed. Residual: edits after the re-read and before the claim reads the issue (C-014 controls: live-test gate, permission mode)."
- **Rationale:** INV-026 ADDRESSED; E's rejection recorded as the residual.
- **Risk:** Medium.

#### Change 50: T7 same login
- **Source:** C-005 (round 2, 5 of 5, A text); INV-024 case 7; A-004.
- **Target:** §6, T7.
- **Approach:** replace.
- **Text:** "`enabled` defaults to false. Enable the poller in exactly one workspace per login; a second workspace on the same login is unsupported. Every audit line carries `host` and `login`, so a double enablement is visible."
- **Rationale:** C-005 AGREED 5 of 5. Residual (two stores) goes to §11.
- **Risk:** Low.

#### Change 51: T8 store deletion or loss
- **Source:** INV-024 (round 3, 5 of 5); X-003; INV-027.
- **Target:** §6, T8 ("deletion permits a second launch").
- **Approach:** replace.
- **Text:** "`init-state` records `created_at`; approvals older than it never count, so a lost store cannot re-dispatch old approvals. A missing store or lock exits 6. Residual: a restored older backup."
- **Rationale:** INV-024 5 of 5.
- **Risk:** Low.

#### Change 52: T10 permission mode
- **Source:** C-014 (round 2, 5 of 5).
- **Target:** §6, T10.
- **Approach:** replace the mitigation cell with Change 2's text, and keep the OD-7 link.
- **Text:** as Change 2.
- **Rationale:** C-014 AGREED.
- **Risk:** Low.

#### Change 53: New threat rows T13-T16
- **Source:** C-013, A-010, INV-010 (residual), A-008, INV-021, INV-023.
- **Target:** §6, after T12.
- **Approach:** insert.
- **Text:**
  - "T13 Approver allow-list edited by another local user: file must be owner-owned and not group/other-writable, else exit 2 (C-013, INV-019)."
  - "T14 Allow-listed approver demoted or compromised: not mitigated in v1; residual R-INV-010."
  - "T15 A human-run automation labels as a `User`: residual (A-008)."
  - "T16 Approval removed after the re-read, or hand claim while enabled: residual (INV-023, INV-021); runbook forbids hand-claiming trigger-labelled issues while enabled."
- **Rationale:** Required by the seed's security model; S-008 links to requirement IDs.
- **Risk:** Low.

### §7 Dispatch record

#### Change 54: Store form and creation
- **Source:** S-005 (round 2, 5 of 5, D text); C-017 (round 1, D, 4 of 5); K7.
- **Target:** §7, "Location" and store paragraph.
- **Approach:** replace.
- **Text:** "One versioned JSON record file per state directory, written with `write_prepared_bytes` (0600) plus a parent-directory fsync. Only `init-state` creates it. If it is missing after init, unparseable or of unknown version, `once` exits 6 with no launch and leaves the file untouched. No SQLite."
- **Rationale:** S-005 AGREED; D's form wins over A's "`check-config` creates it" (K7). Location stays `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` (C-017 D). Tombstones are never pruned (U-015).
- **Risk:** Low.

#### Change 55: Schema fields
- **Source:** C-007 (round 3 final, 3 of 5); INV-007; INV-015; INV-016; INV-024; U-005.
- **Target:** §7, "Schema"; replace D's `launches` note ("incremented after the outcome").
- **Approach:** replace.
- **Text (synthesized):** "Store: `schema_version`, `created_at`, `next_permitted_at`, `considered`. Entry: `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at` (immutable), `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason`, all times UTC."
- **Rationale:** C-007 round-3 majority (B, C, D) field list; INV-007 adds the login; INV-016 `consumed_at`; INV-015 `considered`.
- **Risk:** Medium (schema is the contract the crash tests check).

#### Change 56: Launch counter rule
- **Source:** C-007 (round 2 D text, confirmed round 3).
- **Target:** §7, below the schema.
- **Approach:** insert.
- **Text:** "`launches` is incremented in the same durable write as `pending`, before Orca is spawned; a fresh launch requires `launches == 0`. Re-labelling, re-approval, lease expiry and login change never reset it; only `reset <N> --forfeit-guarantee` does."
- **Rationale:** C-007; corrects D's base text, which incremented after the outcome.
- **Risk:** High if missed (it is the at-most-once mechanism); tested by crash injection.

#### Change 57: States, with the "pre-pending failed" resolution named
- **Source:** C-007 (round 3, keep six states: B, C, D); INV-001; K1.
- **Target:** §7, state list.
- **Approach:** replace.
- **Text:** "States: `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed`. Resolution 'pre-pending failed': `failed` arises only before a `pending` write, has `launches == 0`, and retries after a 10-minute backoff up to `max_attempts` 3, then becomes `abandoned` `attempts_exhausted`. No transition leads from `pending` or later to `failed`."
- **Rationale:** C-007 majority 3 of 5 keeps `failed`; INV-001 unanimous forbids `failed` after `pending`. Both hold under this resolution.
- **Risk:** Medium.

#### Change 58: Transition table
- **Source:** X-001 (round 2, 4 of 5, D text); X-002 (round 2, 4 of 5); INV-004 (round 3, 5 of 5); INV-002; INV-021; K13; A-009 (round 3 final).
- **Target:** §7, transitions table (D lines 133-148).
- **Approach:** replace the whole table with these rows.
- **Text (rows, from -> to : trigger):**
  - none -> `failed` : prompt `ValueError` or transient re-read error (K1).
  - `failed` -> (eligible again) : backoff elapsed, `attempts` < 3.
  - `failed` -> `abandoned` `attempts_exhausted` : `attempts` = 3.
  - none or `failed` -> `pending` : all checks passed; `launches`+1, `consumed_at` set.
  - `pending` -> `launched` : Orca confirmed success; `operation_id` stored; lease set.
  - `pending` -> `unknown` : any other outcome after spawn (INV-002).
  - `pending` -> `abandoned` `spawn_error` : exec `OSError` before the child starts.
  - `pending` (found at cycle start) -> `abandoned` `pending_orphan` (X-002).
  - `launched` -> `abandoned` `claim_not_observed` : lease end, report only, slot not released (X-001, A-009).
  - `launched`, `unknown`, `abandoned` -> `claimed` : own marker newer than `pending_at` (INV-021).
  - none -> `claimed` : own marker newer than the current approval, no entry; never launched (C-024).
  - `abandoned` -> none with `launches` 0 : `reset <N> --forfeit-guarantee` only; `consumed_at` kept.
  - `unknown` never moves on the lease; it leaves only via `claimed` or `reset`.
- **Rationale:** X-001 text: "a later own marker still moves the `abandoned` entry to `claimed`, and `claim_not_observed` never releases the consumed slot". INV-004 adopted with v1 retry off (K3): `unknown` waits for a marker or the operator; `status` lists it after 24 h.
- **Risk:** High (state machine); every row needs a test.

#### Change 59: Parameters
- **Source:** C-008 (round 2); INV-015; K5.
- **Target:** §7, "Parameters".
- **Approach:** replace.
- **Text:** "All [PROPOSAL]: lease 60 min (reporting only), `max_attempts` 3, `max_launches` 1, `max_candidates` 10, `max_launches_per_cycle` 1, `failed` backoff 10 min, day cap 6 per rolling 24 h, call cap 35 per cycle."
- **Rationale:** C-008 5 of 5; K5.
- **Risk:** Low.

#### Change 60: Recovery and scope
- **Source:** X-003 (round 3 final); C-020 (round 2); INV-024.
- **Target:** §7, "Recovery" ("operator removes entry") and "Scope".
- **Approach:** replace.
- **Text:** "Recovery is never a hand edit. A single stuck entry: `reset <N> --forfeit-guarantee`. A broken store: move the directory aside and run `init-state`; approvals older than the new `created_at` need a re-label. Scope: the guarantee holds per intact, single store per login."
- **Rationale:** X-003; INV-024 scope wording.
- **Risk:** Low.

### §8 Deliverables

#### Change 61: Module list
- **Source:** S-004 (round 2, 4 of 5).
- **Target:** §8, modules (D: runner, github, filters, launch, state, audit, cycle, cli).
- **Approach:** replace with Change 48's list (`filters` becomes `predicates`, `state` becomes `record`).
- **Rationale:** S-004 AGREED. A's typed stage protocols (U-001) not adopted.
- **Risk:** Low.

#### Change 62: `once` options move to config
- **Source:** C-021 (round 1, A); C-020; C-005.
- **Target:** §8, `once` options list.
- **Approach:** replace.
- **Text:** "`once` takes only `--dry-run` and `--config <path>`. Labels, `project_id`, `owner_account_id`, worktree, approvers file and `state_dir` come from the JSON config validated by `check-config`."
- **Rationale:** C-021 leading A; C-020 "There is no flag-only interface" (A text). Drops D's `--project-number`, `--project-owner`, `--status-name`.
- **Risk:** Low.

#### Change 63: Exit-code table and precedence
- **Source:** X-007 (round 2, 5 of 5, A text); INV-006 (round 3, 5 of 5 MODIFY); K4; K6.
- **Target:** §8, exit table (D: 0, 2, 3, 4, 5 record, 6 launch, 75).
- **Approach:** replace.
- **Text:** "Exit codes: 0 ok or disabled; 2 usage or config; 3 GitHub auth, scope, timeout or non-JSON; 4 discovery truncated; 5 rate limited, with the next permitted time persisted; 6 record unreadable or unwritable; 7 a launch ended `failed` or `unknown`; 75 lock held. Each code has a runbook action."
- **Add:** "When several apply, exit with the first of 2, 6, 7, 5, 3, 4. Every condition is also an audit line. Exit 75 applies only when the lock was not taken (or its inode changed) and nothing else ran."
- **Rationale:** X-007 AGREED 5 of 5 (D adds missing-store to 6); INV-006 precedence per K4; inode mismatch 75 per K6.
- **Risk:** Medium (renumbers D's 5 and 6; every test and runbook line must follow).

#### Change 64: Test files and the acceptance property
- **Source:** C-022 (round 1); seed acceptance criterion; C-012; S-003 (A stage protocols, E arithmetic).
- **Target:** §8, tests.
- **Approach:** append to D's `test_cli_e2e.py` and `test_security_invariants.py` list.
- **Text:** "Add `test_predicates.py`, `test_record.py` (every §7 transition row), `test_crash_injection.py`, `test_concurrency.py`, `test_no_shell.py`, `test_no_text.py`, `test_origin_parity.py`. Acceptance: given a mocked `gh` returning N matching issues, the poller starts exactly one mocked launch per eligible issue, each with the integer number only, and records each dispatch."
- **Rationale:** C-022 AGREED; seed acceptance text. One launch per cycle means the e2e runs N cycles.
- **Risk:** Low.

#### Change 65: Runbook and activation gates
- **Source:** C-017 (round 1, D, 4 of 5); C-023 (round 2, 5 of 5, D text); INV-008; INV-014; INV-021; INV-024; U-012.
- **Target:** §8, runbook steps 1-6.
- **Approach:** replace step 6; append steps 7-10.
- **Text:**
  - Step 6: "Alert when `last_completed_cycle_age_seconds` > 900."
  - Step 7: "Run `init-state` before the 24 h shadow; re-apply approval labels on issues approved before init."
  - Step 8: "Setup order per issue: assign the owner, add the trigger label, then the approval label."
  - Step 9: "Before cron: a 24 h shadow `--dry-run` whose audit is reviewed, a two-process lock test on the real state directory, a persistence check that `state_dir` survives a workspace restart, and the staleness alert wired up."
  - Step 10: "While enabled, never hand-claim a trigger-labelled issue; remove the trigger from claimed issues."
- **Rationale:** C-023 activation gates (D); C-017 leading D plus C's persistence check; INV rulings above.
- **Risk:** Low.

#### Change 66: Gates and failure analysis
- **Source:** S-003 (round 1, H, 5 of 5).
- **Target:** §8, gates paragraph.
- **Approach:** append.
- **Text:** "Keep `uv run pytest tests/issue_watch/`, `make lint`, `make sync-dev`, `make test`, `make verify-sync`. Add one table mapping each failure mode to its root cause and exit code (B), and the budget arithmetic of NFR-009 (E)."
- **Rationale:** S-003 leading H (A stage protocols kept only as the three S-004 protocols).
- **Risk:** Low.

### §9 Follow-ups

#### Change 67: Follow-up list
- **Source:** C-023 (round 2, A text); INV-003; INV-010; INV-026; C-014.
- **Target:** §9, FU-1..FU-7.
- **Approach:** replace FU-1..FU-7 and add FU-8..FU-10.
- **Text (FU-1..FU-6 from C-023):** "a live slash-command and permission test, which blocks enablement; the Coder cron and a persisted `state_dir`; confirmation of the `read:project` scope; alerting on staleness or repeated non-zero exits; ETag requests; per-actor permission checks."
- **Add:** "FU-7 Revisit (Change 68). FU-8 Automatic retry, only after the live test records Orca's retry rule (Q3): it uses the cycle's one launch slot, re-runs DISABLED, re-read and origin checks, starts by 120 s, at most 3 tries, never changes `launches` or the day cap. FU-9 Approver role check (INV-010), if the endpoint works with a workspace token. FU-10 Measure SLOs (D FU-5)."
- **Rationale:** C-023 AGREED; INV-003 conditions (E's budget rule); INV-010 E's follow-up. D's FU-2 cron string `"0 */5 * * * *"` is kept inside FU-2.
- **Risk:** Low.

#### Change 68: Option A makes Coder#477 unnecessary
- **Source:** C-023 (round 2, last sentence); seed brief.
- **Target:** §9, end (D's FU-7 revisit, #477).
- **Approach:** replace.
- **Text:** "Option A makes IronbellyOrg/Coder#477 unnecessary. Options B and C, and Coder#477, return only on a revisit condition: the workspace cannot run a reliable cron, or one poller per login becomes unworkable."
- **Rationale:** C-023 AGREED; the seed asks for this statement explicitly.
- **Risk:** Low.

### §10 Open decisions

#### Change 69: Update OD rows, keep numbering
- **Source:** S-006 (round 1, N, 4 of 5); C-013; C-008; C-014; C-005; INV-026; INV-006; INV-015.
- **Target:** §10, OD-1..OD-9.
- **Approach:** replace OD-2, OD-5, OD-7, OD-8, OD-9; append OD-10, OD-11.
- **Text:**
  - "OD-2 Approvers by account ID in an owner-only file (recommended; decided by C-013)."
  - "OD-5 Parameters as §7, all [PROPOSAL]; owner confirms after the shadow run."
  - "OD-7 Session permission mode: default interactive, no override; bypass needs written acceptance."
  - "OD-8 One enabled workspace per login (recommended)."
  - "OD-9 Claim reads issue text: accepted residual, narrowed by 'unchanged since approval'."
  - "OD-10 Exit precedence 2, 6, 7, 5, 3, 4 (recommended; majority synthesis)."
  - "OD-11 `max_candidates` 10 (recommended; 5 and 8 were the alternatives)."
- **Rationale:** S-006 keeps D's numbering; contents from the cited rulings.
- **Risk:** Low.

### §11 Risks

#### Change 70: Rewrite R3 and R8
- **Source:** INV-014; INV-018; INV-004; A-009 (round 3 final).
- **Target:** §11, R3 ("Project over 100 items") and R8 ("Orca ignores retry; lease expiry moves to `abandoned`").
- **Approach:** replace.
- **Text:**
  - "R3 More than 99 open trigger issues assigned to the owner: exit 4 every cycle. Mitigation: FR-003 warning at 80; runbook removes the trigger from claimed issues."
  - "R8 Launch outcome unknown: the entry stays `unknown` and blocks a relaunch; `status` lists it after 24 h (SLO d). The lease is a reporting threshold only (A-009 rejected as a safety premise)."
- **Rationale:** per-issue `projectItems` removed D's R3 cause; v1 has no retry (K3).
- **Risk:** Low.

#### Change 71: Add residual-risk rows, including INV-010
- **Source:** INV-010 (round 3: B, D, E reject; A, C modify; 3 of 5 reject); INV-023; INV-024; INV-025; INV-026; INV-021; INV-012; A-006; S-008.
- **Target:** §11, after R9.
- **Approach:** insert (S-008 columns: ID, risk, likelihood, impact, mitigation with requirement IDs).
- **Rows:**
  - "R10 (INV-010) An allow-listed approver who is demoted, removed or compromised stays a valid approver until the owner edits the file. Likelihood Low (three Triage-plus accounts). Impact High. Mitigation: `check-config` prints the file's mtime and entry count; FU-9. Accepted residual, not a requirement."
  - "R11 (INV-024 case 6) A restored older store re-allows launches. Mitigation: backup restore unsupported (NFR-011)."
  - "R12 (INV-024 case 7) Two stores on one login. Mitigation: T7, FR-020 `host` field; cost multiplies by W."
  - "R13 (INV-026, E) Edits or comments after the re-read reach the session. Mitigation: C-014 gate, OD-7."
  - "R14 (INV-021) A concurrent hand claim. Mitigation: runbook step 10."
  - "R15 (INV-023, INV-012) An approval removed, or DISABLED created, after the spawn starts cannot stop the session."
  - "R16 (A-006) Clock jumps distort lease, backoff, day cap and ordering; none affects `launches`."
  - "R17 (INV-026) Any commenter can stall an approved issue until re-approval."
  - "R18 (INV-025) The integer-only prompt keeps issue text out of the prompt but not out of the session: the claim reads title, body and comments (`claim.md:26`, `:56`). Mitigation: C-014 gate, OD-7 permission mode, 'unchanged since approval'. Accepted residual."
- **Rationale:** INV-010 must be a residual, not a requirement (3 of 5 reject). The rest are round-3 concessions.
- **Risk:** Low.

### §12 Traceability

#### Change 72: Traceability with UNVERIFIED tags
- **Source:** S-007 (round 2, B, 4 of 5, A text); S-002 (round 1, N).
- **Target:** §12.
- **Approach:** replace and extend.
- **Text:** "Every requirement cites its source in a traceability table, using a seed section, research fact, research question or `file:line`. A source that has not been verified is tagged UNVERIFIED."
- **Add rows** for FR-022..FR-029, NFR-014, T13-T16, R10-R18 and the §13 assumptions. Mark UNVERIFIED: event shape, `lastEditedAt`, `projectItems` shape and scope, Orca retry rule, slash-command prompt execution, `$HOME` persistence. Do not add count summaries (S-002: counts are cosmetic).
- **Rationale:** S-007 AGREED.
- **Risk:** Low.

### §13 Assumptions (new section)

#### Change 73: Add §13 with A-001..A-010
- **Source:** diff-analysis A-001..A-010; round-1/round-2 QUALIFY votes (9 AGREED, A-009 decided in round 3).
- **Target:** new §13, after §12.
- **Approach:** insert.
- **Text (one line each):**
  - "A-001 ASSUMPTION: `state_dir` survives workspace restarts. Condition: verified by the runbook persistence check before cron (UNVERIFIED until then)."
  - "A-002 ASSUMPTION: a leading `/sc:issue` in `--prompt` runs as a slash command. Condition: enablement blocked until the live test (FU-1)."
  - "A-003 CONSTRAINT: labels and the Status field and option are matched by name and fail closed; owner and approvers by account ID; Project by node ID."
  - "A-004 CONSTRAINT: one enabled poller per login; a second is unsupported (T7, R12)."
  - "A-005 CONSTRAINT: the owner is assigned before approval; an approved unassigned issue is never seen (INV-014)."
  - "A-006 ASSUMPTION: the wall clock is correct; a jump affects timing only, never `launches` (R16)."
  - "A-007 CONSTRAINT: local Linux filesystem; network filesystems refused (§2)."
  - "A-008 ASSUMPTION: a `User` actor not ending `[bot]` is a human decision; residual T15."
  - "A-009 REJECTED as a safety premise: the lease only reports; a late marker still gives `claimed`."
  - "A-010 CONSTRAINT: the approver file is owner-only, checked by `check-config` and `once` (INV-019)."
- **Rationale:** Each assumption becomes an ASSUMPTION or CONSTRAINT line with its adopted condition, as the brief requires.
- **Risk:** Low.

#### Change 74: Cross-reference sweep
- **Source:** X-007 renumbering; S-004 renames; K1-K13.
- **Target:** whole document.
- **Approach:** restructure (mechanical).
- **Text:** none. Replace every old exit number (record 5 to 6, launch 6 to 7, rate limit 3 to 5), every `filters`/`state` module name, every `project item-list` reference and every `--retry-launch` automatic-path reference.
- **Rationale:** keeps the merged spec internally consistent after Changes 17-73.
- **Risk:** Medium (a missed reference contradicts the exit table).

**Change count: 74.**

## Required content checklist for the merged spec

The merge executor confirms each item is present in the merged spec, at the location given.

- [ ] **Tagged** defined precisely: exact, case-sensitive trigger label name, configurable, never created by code (§3, Change 8).
- [ ] **Approved by a human** defined precisely: approval label present; latest `labeled` actor is `User`, not `[bot]`, account ID in the allow-list; later than the trigger event and the store's `created_at`; not unlabeled since; complete event history; unchanged since approval (§3, Changes 9-11).
- [ ] **In a Project** and **Backlog** defined precisely: one non-archived item in `project_id`, `Status` = `Backlog`, from `projectItems` (§3, Change 12).
- [ ] **Intended owner** defined precisely: assignee set equals exactly {own login}; `is_intended_owner` (§3, Change 13).
- [ ] **Eligible issue** defined precisely, with check order and "absent evidence is never positive" (§3, Change 15).
- [ ] **Routing rule from issue to workspace:** the issue routes to the one workspace whose poller runs as the assigned login; one enabled workspace per login; launch in the configured worktree whose origin is IronbellyOrg/IronClaude (§3 Change 13, §6 Change 50, FR-025 Change 30, Change 31).
- [ ] **Dispatch record for at-most-once starts:** store form, schema, six states, transition table, launch counter in the `pending` write, lease as report only, caps marked [PROPOSAL] (§7, Changes 54-60).
- [ ] **Security model and residual risk:** public-repo threats T1-T16, permission mode of the launched session (T10, OD-7, C-014), residual rows R10-R18 including INV-010 (§6, §11).
- [ ] **Statement on IronbellyOrg/Coder#477:** "Option A makes IronbellyOrg/Coder#477 unnecessary" unless B or C is revisited (§9, Change 68).
- [ ] **Repo-side deliverables testable with mocks, nothing run live:** module list, CLI verbs, config, test files, `FakeRunner`, `_assumed_shape`, gates (§8, Changes 61-66; NFR-005).
- [ ] **Follow-ups (not built):** FU-1..FU-10 including the live test, Coder cron, scope check, alerting, ETags, per-actor checks, automatic retry, approver role check (§9, Change 67).
- [ ] **Observable acceptance criterion:** "given a mocked `gh` response with N matching issues the poller starts exactly one mocked launch per eligible issue with the integer number only and records each dispatch" (§8, Change 64), plus the prompt-regex property test (Change 32).
- [ ] **Open decisions with recommended defaults:** OD-1..OD-11 (§10, Change 69).
- [ ] **Traceability** with UNVERIFIED tags (§12, Change 72).
- [ ] **D1-D3** restated verbatim (§2, Change 3).
- [ ] **Assumptions** A-001..A-010 each as ASSUMPTION, CONSTRAINT or REJECTED line (§13, Change 73).
- [ ] **Exit-code table** with precedence and runbook actions (§8, Change 63).
- [ ] **Guarantee wording** "at most once per issue per intact, single store per login" (§1, Change 1).

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| INV-010 | Verify the approver's current repository role (triage or higher) before launch; skip `approver_not_current` | Rejected 3 of 5 (B, D, E; A and C modify). The collaborator-permission endpoint probably needs admin or maintain access (UNVERIFIED); a fail-closed v1 check could block every launch. Recorded as residual R10 and follow-up FU-9. |
| C-007 (A, E positions) | Remove the `failed` state | 2 of 5 in round 3. K1 keeps `failed` as a pre-`pending` state, consistent with INV-001. |
| C-009 (A's round-2 order) | Write `pending` before the re-read; delete it on failure | Contradicts INV-001 (5 of 5). D's order wins (K2). |
| C-011 / INV-003 (E) | Automatic `--retry-launch` in v1 | INV-003 majority: no automatic retry until the live test proves Orca's retry rule. Moved to FU-8. |
| C-011 (A's round-2 clause) | "Definite Orca error gives retryable `failed`" | Withdrawn under INV-002 (5 of 5). |
| INV-015 (probe, C; A) | `max_candidates` 5 or 8 | 10 has B, D, E (3 of 5); the 35-call cap binds (K5). |
| INV-006 (probe order; A, B, C, D orders) | Precedence placing 3 above 7, or 2 below 6 | E's order 2, 6, 7, 5, 3, 4 adopted (K4): a deadline overrun must not hide an `unknown` launch. |
| INV-027 (A) | Lock inode mismatch exits 6 | 3 of 5 chose 75 (K6). |
| INV-018 (C) | Match the Status field and Backlog option by option ID | 4 of 5 chose names; a rename fails closed and shows in the shadow run. |
| INV-026 (B extension) | Exempt comments by allow-listed approver IDs | Minority; not applied. |
| INV-026 (E) | Reject the check, treat as residual only | 4 of 5 adopted the check. E's concern kept as R13 and R17. |
| INV-021 (B, C) | No freshness rule on the marker | 3 of 5 adopted it. |
| INV-014 (C) | Paginated discovery instead of `--assignee` | Minority; `--assignee` keeps idle at 2 calls. |
| C-020 / S-005 (A) | `check-config` creates the store | INV-027 and D's C-020 text: only `init-state` creates it; `check-config` is read-only (K7). |
| C-001 / U-007 (C) | Label node IDs | C-001 5 of 5 by name; node IDs only for Project and accounts. |
| U-001 (A) | Typed stage protocols for every stage | S-004 limits protocols to runner, store, launcher. |
| U-003 (A) | Keep a history of 20 entries; lease ≥ 15 min | Not adopted in any ruling; tombstones kept, lease report-only. |
| U-008 (C) | SQLite store | S-005 5 of 5: one JSON file. |
| U-010 (C) | Readiness scoring of candidates | Not adopted; INV-015 ordering suffices. |
| U-015 (E parts) | 30-day pruning of tombstones; refusing to run inside an Orca worker | Pruning breaks at-most-once; the worker detector was not adopted. Day cap 6 kept. |
| B `--label-only` | Mode that skips the Project check | X-005 final ruling: no such mode. |
| E `--agent <agent>` | Configurable agent | X-008 5 of 5: `--agent claude` fixed. |
| Per-issue record files | One file per issue | S-005: one store file. |
| D `rate_remaining` audit field | Keep `rate_remaining` | Dropped in D's round 2 (C-019). |
| D `project item-list` | Read Project membership via `gh project item-list` | C-003 (E, 4 of 5) and X-005: per-issue `projectItems`. |
| S-002 | Reconcile requirement counts | N, 5 of 5: counts are cosmetic. |
| S-006 (C) | Renumber open decisions | N, 4 of 5: keep D's OD numbering. |
| A-009 premise | Lease end releases the slot | Rejected as a safety premise in round 3. |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| 22 | High | Pre-`pending` order wrong: an orphan `pending` or a `failed` after spawn could allow a second launch | Revert to D's FR-014 text and re-run the INV-001 review; crash-injection tests catch it |
| 56 | High | `launches` incremented after the outcome (D's old text): a crash between spawn and write allows a relaunch | Restore Change 56 text; crash tests fail if missed |
| 58 | High | Transition table incomplete: an entry with no exit, or a slot released on lease | Diff the table against the X-001, X-002, INV-004 rulings row by row |
| 4, 40 | Medium | Read-only rule too loose (a mutation slips in) or too tight (GraphQL blocked) | Adjust the prefix list; the scanning test is the gate |
| 9, 10, 11, 12 | Medium | GitHub event, `lastEditedAt` or `projectItems` shape differs from mocks | Fail closed by design; fix shapes after the live test (FU-1, FU-3) |
| 14 | Medium | Marker freshness rejects a real claim | Entry stays `launched`/`abandoned`; operator reviews; slot never re-used |
| 21 | Medium | Transient re-read errors produce `failed` loops | Bounded by `max_attempts` 3 and the 10-minute backoff |
| 28 | Medium | Inode check false positive: every cycle exits 75 | Staleness alert fires; runbook step 6 |
| 55, 57 | Medium | Schema or state names drift from tests | Single schema constant; `test_record.py` per row |
| 63, 74 | Medium | Old exit numbers survive somewhere | Grep the merged spec for "exit 5" and "exit 6" contexts during the sweep |
| All others | Low | Wording or placement error | Re-apply the cited ruling text |

**Residual risks carried into the spec (§11, not requirements):** R10 INV-010 approver demotion; R11 and R12 INV-024 cases 6 and 7; R13 and R17 INV-026; R14 INV-021 hand claim; R15 INV-023 and INV-012 spawn in flight; R16 A-006 clock; R18 INV-025 session reads issue text.

## Review Status

- [x] Plan generated from round 1-3 rulings, invariant-probe and diff-analysis
- [x] All conflicts resolved explicitly (K1-K13)
- [x] Auto-approved (no interactive review in this pipeline)
- **Approved by:** auto
- **Approval timestamp:** 2026-11-07

