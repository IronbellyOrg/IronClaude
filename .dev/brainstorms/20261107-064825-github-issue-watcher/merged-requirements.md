<!-- Merged spec. Base: variant D. Merge date: 2026-11-07. Applied: refactor-plan.md Changes 1-74 and base-selection.md additional changes AC-1..AC-7 (see merge-log.md). -->
<!-- Source: Base (original, modified) - status line updated for the merged draft; SLO expanded at first use (AC-6); UNVERIFIED convention added (Change 72) -->
# Requirements Specification: GitHub Issue Watcher (issue #331), Option A

- Status: Merged draft after adversarial review
- Issue: IronbellyOrg/IronClaude#331
- Lens: deployment, observability, runbooks, service-level objective (SLO) impact
- Sources: `seed-brief.md` (SB), `enrichment/research-deep.md` (RD), `enrichment/codebase-context.md` (CC)
- Convention: every number not fixed by a source is marked [PROPOSAL]; every assumption about the repo or host is marked ASSUMPTION (collected in Section 13); a source fact not yet verified is marked UNVERIFIED.

## 1. Purpose and scope

<!-- Source: Base (original, modified) - "top-level agent session" wording -->
**Purpose.** Replace the manual hand-off of approved issues with a poller that runs inside each person's Coder workspace, polls IronbellyOrg/IronClaude every 5 minutes with that workspace's own `gh` login, and starts one ordinary top-level agent session per eligible issue with the prompt `/sc:issue --claim <N>` through `orca agent launch` (SB Q1; RD Recommendation).

<!-- Source: invariant probe INV-024 (round 3) - merged per Change #1 -->
**Guarantee.** The poller starts at most one claim session per issue per intact, single dispatch store per login. A restored older backup of the store, or a second store on the same login, breaks this guarantee; both are documented residual risks (Section 11, R11 and R12).

<!-- Source: Variant B, section 1.1 - merged per base-selection item 13 (AC-4) -->
**Root causes addressed.**

| ID | Root cause | Evidence | Consequence for this design |
|---|---|---|---|
| RC1 | No "ready" signal exists | Only the default labels exist and no code reads Projects (RD fact 7) | Define the signal (Section 3) and verify who set it |
| RC2 | The claim routes to whoever runs it | The claim assigns `@me` and refuses other assignees (`refs/claim.md:41-42`) | Start only claims meant for the own login (Section 3, Intended owner) |
| RC3 | Nothing enforces an at-most-once start | The claim is check-then-act and leaves the issue in Backlog (RD fact 4) | Keep an own dispatch record plus the claim's marker (Section 7) |

<!-- Source: Base (original, modified) - one cycle line plus decision lines (Change 34) -->
**Operational framing.** A batch job, not a daemon: each run is one cycle; a `coder_script` cron entry (RD fact 10) gives the cadence; each cycle leaves one audit cycle line, its decision lines and one exit code.

<!-- Source: Base (original) -->
**In scope (mocks only):** package `src/superclaude/cli/issue_watch/`, Click group `superclaude issue-watch` registered after `reflect` in `src/superclaude/cli/main.py`, tests under `tests/issue_watch/`, and design doc `docs/designs/issue-watcher.md` with label setup and an operator runbook. **Out of scope:** anything live; any listener, port, webhook, Action or service; the post-claim pipeline; the Coder template (Section 9).

<!-- Source: Variant A text, ruling C-014 (round 2) - merged per Change #2 -->
**Deployment gate.** No cron entry is enabled until an owner-run live test shows the prompt running as a slash command and records the session's permission mode. The default is no override. A bypass mode requires the owner's written acceptance.

## 2. Fixed constraints and non-goals

<!-- Source: seed brief line 59, verbatim - merged per Change #3 (ruling X-008, Variant A text) -->
Decided by the owner, restated verbatim from the seed brief: "D1 option A (workspace-side poller, pull); D2 claim-only; D3 only a validated integer issue number reaches a session prompt."

<!-- Source: Base (original, modified) - D1-D3 consequences kept below the verbatim line; Coder#477 statement moved to Section 9 (Change 68) -->
- **D1** consequence: no listener, inbound port or address registry (SB Q1).
- **D2** consequence: the job ends when the session has been asked to run `/sc:issue --claim <N>`; the claim stops at `next-steps.md` (RD fact 1).
- **D3** consequence: the prompt is built only by `build_claim_prompt` (FR-012) (SB Q2).
<!-- Source: Variant A text, ruling X-008 (round 2) - merged per Change #3 -->
- The launch uses the Orca agent name fixed by the seed brief exactly (the module constant `ORCA_AGENT`, FR-013), and the agent is not configurable. The poller reads no comment content beyond the boolean marker projection; no bounded comment content is read.
<!-- Source: Base (original) -->
- Every repository-scoped `gh` call names IronbellyOrg/IronClaude; `gh`, `git` and `orca` run as argv lists, never a shell; the poller is a plain process, never an Orca worker (RD fact 2); no secrets or tokens stored.
<!-- Source: invariant probe INV-027 (round 3) - merged per Change #5 -->
- Linux only. On any other platform `once`, `check-config` and `init-state` exit 2. `once` and `check-config` refuse a state directory on a network filesystem, detected from `/proc/self/mountinfo` (deny-list: nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p).

<!-- Source: Variant C, section 2 - merged per base-selection item 3 (AC-2) -->
**Alternatives.** The research scored existing primitives by counting supported readiness criteria, not by weighted preference:

| Alternative | Meets / partly | Disposition |
|---|---|---|
| A: workspace poller | 2 / 8 | Owner-selected; build the mockable portion |
| B: Action plus listener | 1 / 9 | Follow-up only; higher exposure and effort |
| C: central service plus listener | 0 / 10 | Follow-up only; additional hosting and webhook responsibilities |
| D: label relay plus poller | 2 / 8 | First alternative if workspace Project access fails |

The nine revisit conditions: stopped workspaces cause excessive waiting; latency or API use becomes unacceptable; centralized approval or audit becomes necessary; duplicate claims persist; account binding becomes available; workspace tokens cannot read Projects; event-time Project changes matter; a shared ledger becomes necessary; recurring workspace execution proves impossible.

<!-- Source: Base (original, modified) - NG-2 replaced per Change #4 (rulings X-005, INV-018); NG-5 extended per Change #6 (INV-003, K3) -->
**Non-goals:**

- NG-1 Push designs B, C, D (documented alternatives above, with the nine revisit conditions).
- NG-2 The poller never writes to GitHub. It issues no REST call with a verb other than GET. GraphQL requests use POST only with a query string that is a module constant containing no `mutation`. A unit test scans every constant and every recorded argv. (The claim, not the poller, assigns and comments.)
- NG-3 Project writes.
- NG-4 Constraining the launched session beyond the deployment gate (Section 6, T10).
- NG-5 Daemon mode or retry loops inside a cycle. v1 makes no automatic Orca retry. A launch that ends `unknown` stays `unknown` until an own claim marker appears or the operator acts.

## 3. Definitions

<!-- Source: Base (original, modified) - opening sentence extended per base-selection item 2 (AC-1, Variant C section 3) -->
All are evaluated from projected `gh` JSON; label names default per OD-1. The watcher deliberately selects a stricter subset of issues than the existing claim command permits: every condition below must hold.

<!-- Source: rulings C-004 (round 3, Variants A, D, E), INV-007 - merged per Change #7 -->
- **Own login and own account ID.** Read once per cycle from one `gh api user` call (`.login`, `.id`); never cached across cycles. The login must match `^[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})$`. If `owner_account_id` is configured (FR-027) and differs from `.id`, the cycle exits 2 before any other `gh` call.
<!-- Source: Variant A text, ruling C-001 (round 2) - merged per Change #8 -->
- **Tagged.** The issue's `labels[].name` contains the trigger label. The trigger label `issue-watch:trigger` and the approval label `issue-watch:approved` are configurable and matched by exact, case-sensitive name. A missing or renamed label matches nothing, so nothing launches. The owner creates the labels; code never does.
<!-- Source: rulings C-002 (Variants A, B, C), C-013, INV-008, INV-024 - merged per Change #9 -->
- **Approved by a human.** All of:
  - (a) The issue carries the approval label now.
  - (b) The latest `labeled` event for the approval label, read from complete event history, has an actor with `type` `User`, a login not ending `[bot]`, and an account ID in the approver allow-list (OD-2, FR-027).
  - (c) That event is later than the latest `labeled` event for the trigger label; a reversed order skips as `approval_before_trigger`.
  - (d) That event is later than the store's `created_at`; an older one skips as `approval_before_init`.
  - (e) No `unlabeled` event for the approval label follows it.
  - The approving event's `actor.id` and event `id` go into the record as `approver_id` and `approval_event_id`. Only Triage-or-higher accounts can label (RD fact 7). Event shape is UNVERIFIED until the live test; mocks pin it through `_assumed_shape` fixtures.
<!-- Source: invariant probe INV-009 (round 3) - merged per Change #10 -->
- **Complete event history.** Events are read with `per_page=100` as in `poll-augment-review.sh:46-56`: a page under 100 ends the read; a repeated event ID, a page with no progress, or the page cap marks history incomplete. Order is (`created_at`, `id`); an opposing same-second tie fails closed. A GraphQL read is complete only when `hasNextPage` is false. Incomplete history skips `events_incomplete`.
<!-- Source: invariant probe INV-026 (round 3), conflict ruling K9 - merged per Change #11 -->
- **Unchanged since approval.** The issue body and every comment not authored by the own login were created and last edited before the approval event, and no `renamed` event follows it. Otherwise skip `edited_after_approval`; re-applying the approval label re-arms the issue. `lastEditedAt` availability is UNVERIFIED. This check runs after the claim-marker check, and the poller reads timestamps only, never text.
<!-- Source: rulings C-003 (Variant E), X-005, INV-018, K8 - merged per Change #12 (replaces "In a Project", "Backlog" and their ASSUMPTION) -->
- **In a Project and in Backlog.** The issue has exactly one non-archived item in the Project whose node ID is `project_id`, read from the issue's own `projectItems` over all pages, and that item's field named `Status` holds the option named `Backlog`. Any other result skips `project_mismatch`. There is no label-only mode. The `projectItems` shape and its scope are UNVERIFIED (FU-3).
<!-- Source: rulings C-004 (round 3), INV-014, K12 - merged per Change #13; routing sentence per checklist item 6 -->
- **Intended owner.** An issue is intended for the own login when its assignee set equals exactly {own login}, the login being read each cycle by `gh api user`. The rule lives in one pure function, `is_intended_owner`, and equals the claim's own rule (`refs/claim.md:41-42`). The account ID is stored in each record. Discovery pre-filters by `--assignee` (FR-003), so the skip reasons `unassigned` and `assigned_other` arise only in `is_intended_owner` unit tests and in the FR-011 re-read. **Routing:** an issue routes to the one workspace whose poller runs as the assigned login (one enabled workspace per login, T7) and launches in that workspace's configured worktree, whose origin must be IronbellyOrg/IronClaude (FR-013, FR-025).
<!-- Source: ruling C-024 (round 2), INV-021 (round 3) - merged per Change #14 -->
- **Claimed.** `claimed` requires an own-login comment containing `<!-- sc:issue:claim -->` (`refs/claim.md:29`), read over all comment pages through a `--jq` boolean projection; comment bodies never enter the Python process. It counts only if created or last edited after the entry's `pending_at`, or, with no entry, after the current approval event. Assignment alone is not evidence.
<!-- Source: ruling C-015 (round 2) - merged per Change #15 -->
- **Eligible issue.** Open; tagged; assigned to the intended owner; approved; not claimed; unchanged since approval; in the configured Project in Backlog; no record entry with `launches > 0`; not in `failed` backoff. Checks run in this order and the first failure is the skip reason. Absent or incomplete evidence never counts as positive.

## 4. Functional requirements

<!-- Source: Variant A text, ruling S-001 (round 2) - merged per Change #16; GWT expanded at first use (AC-6) -->
Each requirement is one "shall" sentence with an ID, plus one Given/When/Then (GWT) line that names the stub call or file it observes. Argv lists, paths and markers are written verbatim wherever they form the contract. Criteria run with a `FakeRunner` (or stub `gh`, `git` and `orca` executables) recording argv, and a temporary state directory created by `init-state`.

<!-- Source: Base (original, modified) - FR-001 call count aligned with NFR-009 idle budget -->
- **FR-001** `superclaude issue-watch once` shall execute exactly one poll cycle and exit.
  *GWT:* Given an initialised store and stubs returning no issues, when `once` runs, then the process exits 0 within the test timeout and the stub `gh` saw exactly two calls: one `api user` and one discovery `issue list`.
<!-- Source: Base (original, modified) - account ID check per Change #7 -->
- **FR-002** The cycle shall resolve the own login and account ID first, with one `gh api user` call, and shall make no other external call if that fails.
  *GWT:* Given `gh api user` exits 1, when `once` runs, then the exit code is 3, no further `gh` call and no `orca` call is recorded, and the cycle line has reason `gh_auth_failed`; given a configured `owner_account_id` that differs from `.id`, the exit code is 2 with no further `gh` call.
<!-- Source: Variant A text, ruling C-006 (round 2); INV-014 (round 3) - merged per Change #17 -->
- **FR-003** Discovery shall be one `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --assignee <own login> --json number,labels,assignees,state -L 100`. Non-owned issues are dropped before any per-issue call. A `discovery_count` of 80 or more writes a warning audit line.
  *GWT:* Given any run, then the recorded discovery argv equals that list exactly and no recorded argv requests `title`, `body` or `comments` as a field; given 80 results, a warning line carrying `discovery_count` 80 is appended.
<!-- Source: rulings C-006, INV-014 - merged per Change #18 -->
- **FR-004** Discovery that returns exactly the limit (100) shall fail closed: exit 4 with zero launches. The runbook action is to remove the trigger label from claimed issues.
  *GWT:* Given 100 issues returned, when `once` runs, then the exit code is 4, zero launches are recorded and the cycle line has reason `truncated`.
<!-- Source: Base (original, modified) - aligned with the Section 3 approval definition (Change #9, Change #10) -->
- **FR-005** Approval shall be evaluated per Section 3, "Approved by a human", from complete event history projected to event id, type, label name, actor id, actor login, actor type and time.
  *GWT:* Given the latest approval `labeled` event by an account ID not on the allow-list, or by a login ending `[bot]`, the issue skips `not_approved`; given an approval earlier than the trigger event, it skips `approval_before_trigger`; earlier than the store's `created_at`, `approval_before_init`; given an allow-listed `User` after both, it passes and its later entry holds `approver_id` and `approval_event_id`.
<!-- Source: Base (original, modified) - incomplete-history case per Change #10 -->
- **FR-006** Re-labelling shall move approval to the latest `labeled` event, and incomplete history shall never approve.
  *GWT:* Given approver-labeled, outsider-unlabeled, outsider-labeled, the issue skips `not_approved`; given a repeated event ID across pages, it skips `events_incomplete`.
<!-- Source: ruling X-005 (round 3 final), C-015 - merged per Change #19 -->
- **FR-007** Project membership and Backlog status shall be checked per Section 3 from the issue's `projectItems`, filtered to `project_id`. An unreadable Project item skips that issue (`project_unreadable`). A missing `read:project` scope voids the cycle with exit 3.
  *GWT:* Given the `projectItems` read for issue 8 fails, issue 8 skips `project_unreadable` and issue 9 is still examined; given a reply reporting the missing scope, the exit code is 3, zero launches, cycle reason `project_read_failed`; given the item's Status is `In progress`, or two items exist, the issue skips `project_mismatch`.
<!-- Source: Variant A text, ruling C-015 (round 2) - merged per Change #20 -->
- **FR-022** Failures of shared inputs (login, discovery, allow-list, record store, rate limit, Project scope) shall void the cycle with zero launches. Per-issue read failures (events, Project item, marker, re-read) skip only that issue, with a reason. Absent or incomplete evidence never counts as positive.
  *GWT:* Given the discovery read fails, then zero launches and exit 3; given the events read of issue 8 fails while issue 9 is eligible, issue 8 skips `events_incomplete` and issue 9 proceeds.
<!-- Source: Base (original, modified) - exact-set rule per Change #13 and K12 -->
- **FR-008** The intended-owner filter shall keep only issues whose assignee set equals exactly {own login}.
  *GWT:* Given `is_intended_owner` with assignee sets {other}, {}, {own, other} and {own}, only {own} returns true and the others give `assigned_other`, `unassigned` and `assigned_other`; given a re-read showing {own, other} for a discovered issue, it skips `assigned_other`.
<!-- Source: Base (original, modified) - marker freshness per Change #14 -->
- **FR-009** An issue already claimed shall never be launched, and its entry shall move to `claimed` (Section 7).
  *GWT:* Given a `launched` entry for issue 9 with `pending_at` T and an own-login marker comment edited after T, then no launch occurs and the state becomes `claimed`; given only a marker older than T, the state stays `launched`; given no entry and a marker newer than the current approval, an entry in `claimed` with `launches` 0 and no `consumed_at` is written.
<!-- Source: Base (original, modified) - counter and consumed_at in the pending write per Change #56, Change #27 -->
- **FR-010** A `pending` entry, with `launches` incremented and `consumed_at` set, shall be written durably before the launch call.
  *GWT:* Given a stub `orca` that reads `dispatch.json` when invoked, then the stub observes issue 9 in state `pending` with `launches` 1 and `consumed_at` set.
<!-- Source: Variant D round-2 text, ruling C-009; conflict ruling K2 - merged per Change #21; re-read argv aligned with NFR-002 -->
- **FR-011** Under the lock, the poller shall re-read state, labels, assignees, approval and Project Status immediately before the `pending` write, using the read forms of NFR-002 (`gh api --method GET repos/IronbellyOrg/IronClaude/issues/<N>` projected to number, state, labels and assignees; the events read; the `projectItems` query). A failed or unreadable re-read skips `revalidation_failed`, writes no entry and launches nothing; the one exception is a transient re-read error (timeout, 5xx), which writes `failed` (FR-014). Only then is `pending` durably written with `launches` incremented, then Orca called. A `pending` entry found at cycle start becomes `abandoned` `pending_orphan`.
  *GWT:* Given discovery shows issue 9 eligible and the re-read shows it closed, then zero launches, no entry and reason `revalidation_failed`; given the re-read times out, the entry is `failed` with `launches` 0 and `attempts` 1; given a `pending` entry at cycle start, it becomes `abandoned` `pending_orphan` and no launch is recorded.
<!-- Source: Variant A text, ruling C-012 (round 2) - merged per Change #32 -->
- **FR-012** `build_claim_prompt(n)` shall accept only an `int` (not `bool`) in 1..999999999 and return `/sc:issue --claim <n>`; any other value raises `ValueError` and nothing launches. A property test asserts that every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`.
  *GWT:* Given inputs `9`, `"9"`, `True`, `0`, `-1`, `10**9`, `9.0`, then only `9` returns a string; every other input raises `ValueError` and no launch is recorded.
<!-- Source: Variants A and D text, ruling C-010 (round 2) - merged per Change #31; Orca probe from Variant B FR-014 - merged per base-selection item 11 (AC-3); agent token written as the constant ORCA_AGENT (see merge-log) -->
- **FR-013** The launch argv shall be `[<orca>, agent, launch, --agent, <ORCA_AGENT>, --worktree, path:<abs>, --surface, terminal, --prompt, <prompt>, --json]`, where `<ORCA_AGENT>` is the module constant holding the agent name the seed brief fixes. `<orca>` comes from `_find_orca()`, run through the injected runner; its 10 s timeout counts toward the cycle budget. The probe tries `orca-ide`, then `orca`, with `skills list --json` and accepts a binary only when the reply lists the `orca-cli` topic, because `orca` can be the GNOME screen reader; no accepted binary means zero launches and exit 2. `<abs>` must exist and its origin must be IronbellyOrg/IronClaude (FR-025), else exit 2.
  *GWT:* Given a configured worktree `/tmp/x` that exists with the right origin, then the recorded launch argv equals that list with exactly 12 elements; given a relative or missing worktree path, the exit code is 2 before any `gh` call; given `orca` answering non-JSON and no other candidate, zero launches and exit 2.
<!-- Source: invariant probe INV-001 (round 3), ruling C-007, conflict ruling K1 ("pre-pending failed") - merged per Change #22; ruling C-011 (Variant D text), INV-002, X-004 - merged per Change #23 -->
- **FR-014** Per launch the poller shall run, in order: the DISABLED check; the Orca probe, worktree and origin check (shared, cached per cycle; failure exits 2 and writes no entry); the prompt build; the re-read; the `pending` write; the spawn. A prompt `ValueError` or a transient re-read error writes `failed` (`launches` 0, `attempts` + 1). Nothing after `pending` becomes `failed`. Any outcome after Orca is spawned other than confirmed success (timeout, malformed output, `agent_session_operation_unknown`, non-zero exit) is `unknown`, with the slot consumed. An exec `OSError` before the child starts is `abandoned` `spawn_error`.
  *GWT:* For each stub reply: success JSON gives `launched` with `operation_id` stored; a timeout, malformed JSON, `agent_session_operation_unknown` or non-zero exit gives `unknown` and exit 7; an exec `OSError` gives `abandoned` `spawn_error` and exit 7; a failing probe gives exit 2 and no entry. In every case `launches` stays 1.
<!-- Source: invariant probe INV-003 (round 3), conflict ruling K3 - merged per Change #24 (replaces automatic retry) -->
- **FR-015** v1 shall perform no automatic `--retry-launch`. For an `unknown` entry with an `operation_id`, `status` prints the operator retry command, to be run from the stored `launch_cwd`. Enabling retry is a follow-up gated on the live test proving Orca's retry rule (FU-8).
  *GWT:* Given an `unknown` entry with `operation_id` `op-1` and `launch_cwd` `/tmp/x`, when the next cycle runs, then no `orca` argv is recorded for that issue, and `status` prints `<orca> agent launch --retry-launch op-1 --json` with `/tmp/x` as the directory to run it from.
<!-- Source: Variant A text, ruling C-008 (round 2); INV-015; conflict ruling K5 - merged per Change #25 -->
- **FR-016** Per cycle the poller shall examine at most `max_candidates` issues in the FR-023 order and make at most one launch. [PROPOSAL] values: lease 60 min, `max_attempts` 3, one fresh launch per issue, one launch per cycle, `max_candidates` 10, 10-minute backoff after `failed`, `gh` timeout 20 s, `orca` timeout 120 s, and at most 6 fresh launches per rolling 24 hours (FR-024).
  *GWT:* Given 15 eligible issues, then cycle 1 examines 10 (fewer if the 35-call cap of NFR-009 binds) and launches 1; cycle 2 examines the 5 unexamined issues first.
<!-- Source: Variant E text, invariant probe INV-015 (round 3) - merged per Change #26 -->
- **FR-023** A `considered` map (issue to `last_examined_at`) shall be written in the same store write, set for every examined candidate including skips; candidates are taken oldest first, never-examined first, and the map is pruned to the discovery set. It is written only on cycles that examined something, and never in dry-run.
  *GWT:* Given a map {7: T1, 8: T2} with T1 earlier than T2 and a new issue 9, the order is 9, 7, 8; afterwards each examined issue holds the cycle time, and issue 6, no longer discovered, is pruned; a dry-run leaves the map byte-identical.
<!-- Source: invariant probe INV-016 (round 3, Variant E marker-only clause), conflict ruling K10 - merged per Change #27 -->
- **FR-024** Each `pending` write shall set an immutable `consumed_at`. Before a `pending` write, the poller counts entries in any state whose `consumed_at` falls in the last 24 h; at 6, the issue skips `day_cap`. Tombstones and `reset` keep `consumed_at`. An entry recorded from a marker alone has none.
  *GWT:* Given 6 entries in any states with `consumed_at` in the last 24 h, a seventh eligible issue skips `day_cap` and no `pending` is written; after `reset` of one of them, the count is still 6.
<!-- Source: Variant A text, ruling C-018 (round 2); INV-027 (round 3); conflict rulings K6, K7 - merged per Change #28 -->
- **FR-017** A non-blocking `fcntl.flock` on `<state_dir>/lock` shall be held for the whole cycle. If it is held: no external call, audit `lock_held`, exit 75. After acquiring, if the fd's (dev, inode) differs from the path's or its link count is 0, release and exit 75. A missing lock exits 6. Only `init-state` creates it; nothing deletes it.
  *GWT:* Given the lock held by another process, then exit 75, no `gh` call, reason `lock_held`; given the lock path replaced after acquisition, exit 75; given no lock file, exit 6.
<!-- Source: Base (original, modified) - mid-cycle re-check appended per Change #29 (ruling C-018, INV-012) -->
- **FR-018** A kill switch file `<state_dir>/DISABLED` shall make the cycle exit 0 before any external call. DISABLED is checked again before each `pending` write (and before each retry, if retry is ever enabled). If present then, nothing further starts, the audit reason is `disabled_mid_cycle`, and the cycle exits 0 without a health refresh. A spawn already started cannot be stopped.
  *GWT:* Given the file exists, then no `gh` or `orca` call is recorded and the reason is `disabled`; given the file created after discovery and before the `pending` write, then no `pending` entry, reason `disabled_mid_cycle`, exit 0, and `last_completed_cycle_age_seconds` is not refreshed.
<!-- Source: invariant probe INV-011 (round 3), ruling C-010 - merged per Change #30 -->
- **FR-025** The poller shall run `git -C <abs> remote get-url origin` through the injected runner, parse it with the `parse_origin_url` rules (`origin_repo.py:86-99`) and compare it case-insensitively to `ironbellyorg/ironclaude`, at cycle start (mismatch exits 2) and again just before the `pending` write (mismatch exits 2 with no entry). A parity test pins the parser against `parse_origin_url`.
  *GWT:* Given origin `git@github.com:IronbellyOrg/IronClaude.git`, the check passes; given another repository's URL at cycle start, exit 2 before discovery; given the origin changed between cycle start and the `pending` write, exit 2 and no entry.
<!-- Source: invariant probe INV-005 (round 3), conflict ruling K11 - merged per Change #33 -->
- **FR-019** `--dry-run` shall require an initialised store and take the lock. It performs all reads, honours a persisted next-permitted time, and writes audit lines tagged `dry_run`. Store, backoff, rate-limit time, `considered` and health timestamps stay byte-identical. It never calls Orca, reports the probe as skipped, and reports but does not write `pending_orphan` or `claim_not_observed`.
  *GWT:* Given one eligible issue and `--dry-run`, then zero `orca` calls, `dispatch.json` byte-identical, and a decision line tagged `dry_run` naming issue 9 as would-launch; given a `pending` entry at start, `pending_orphan` is reported and the store is unchanged.
<!-- Source: ruling C-019 (Variant D file, Variant A enum, Variant E counters, Variant B decision lines) - merged per Change #34 -->
- **FR-020** Every exit shall append to `<state_dir>/audit.jsonl` one cycle line with `ts`, `host`, `login`, `cycle_id`, `exit`, `gh_calls`, `duration_ms`, `dry_run`, plus per-decision lines with issue number, closed-enum reason, `approver_id` and `approval_event_id`. The file is rotated at 5 MiB. No title, body or comment text is ever logged. A crash is the only exit without a line.
  *GWT:* For each of exits 0, 3, 4, 5, 6 (unparseable store), 7 and 75, the file gains exactly one parseable cycle line whose `exit` matches, and each examined issue adds one decision line.
<!-- Source: Variant D round-2 text, ruling C-018; INV-006; INV-004 - merged per Change #35 -->
- **FR-021** `superclaude issue-watch status [--json]` shall be read-only and report `last_completed_cycle_age_seconds`, refreshed only by an exit-0 cycle that is neither DISABLED nor dry-run; `disabled_since`; entries by state; every `unknown` or `pending_orphan` entry older than 24 h; and the retry command for `unknown` entries with an `operation_id`. Age above 900 s is unhealthy.
  *GWT:* Given a state directory, then `status` records zero `gh`/`orca` calls and leaves every file's mtime unchanged; given a last qualifying cycle 1,000 s ago, it reports unhealthy; given an `unknown` entry 25 h old with an `operation_id`, it lists the entry with its retry command.
<!-- Source: Variant D text, ruling C-020 (round 2); conflict rulings K7, K10 - merged per Change #36 -->
- **FR-026** The CLI shall offer these verbs: `once [--dry-run]`, `status [--json]`, read-only `check-config`, `init-state` (creates the store and lock, and refuses if a store exists), and `reset <N> --forfeit-guarantee` (only on `abandoned` or `unknown`, under the lock, audited, prints that N may launch twice). Exit codes are as in Section 8.
  *GWT:* Given an existing store, `init-state` refuses and changes nothing; `check-config` records zero writes; `reset 9 --forfeit-guarantee` on a `launched` entry refuses; on an `abandoned` entry it removes the entry, keeps `consumed_at` in the day-cap count, appends an audit line and prints the warning.
<!-- Source: Variant A, ruling C-021 (round 1); C-013, INV-019, C-005 - merged per Change #37 -->
- **FR-027** Configuration shall be JSON at `~/.config/superclaude/issue-watch.json` (no `tomllib` on Python 3.10), with `enabled: false` by default, holding the labels, `project_id`, `owner_account_id`, `worktree`, the approvers file path and `state_dir`. Approvers are account IDs in an owner-only file. `once` exits 2 before any `gh` call if that file is missing, empty or group/other-writable, using `check-config`'s validator.
  *GWT:* Given an approvers file with mode 0664, or an empty one, `once` exits 2 with zero `gh` calls; given a valid config and file, `check-config` exits 0 and prints the file's mtime and entry count.
<!-- Source: rulings C-016 and X-006 (Variant C persisted time plus the hard cap), X-007 - merged per Change #38 -->
- **FR-028** On a primary or secondary rate-limit reply the poller shall stop with no state change except a persisted next-permitted-request time (`next_permitted_at`, from `Retry-After` or the reset header), audit `rate_limited` and exit 5. Every later cycle before that time exits 5 with zero `gh` calls.
  *GWT:* Given a rate-limit reply with `Retry-After: 120`, the store holds `next_permitted_at` 120 s ahead, the reason is `rate_limited` and the exit is 5; given a cycle 60 s later, exit 5 with zero `gh` calls.
<!-- Source: invariant probe INV-017 (round 3, Variant E bound), ruling C-008 timeouts - merged per Change #39 -->
- **FR-029** Each `gh` and probe call shall time out at the lesser of its configured value and the time left before a 240 s cycle deadline; no new `gh` call starts with under 5 s left. No launch starts after 120 s. A started launch is never cut short; its own 120 s timeout applies and a timeout gives `unknown`. The record is written before exit.
  *GWT:* Given a stub `gh` that has consumed 236 s, no further `gh` call is recorded and the record is written before exit; given 121 s elapsed at the launch step, no launch is recorded.

## 5. Non-functional requirements

<!-- Source: Base (original) -->
- **NFR-001 Prompt boundary (security).** No byte of issue title, body, comment, label name or login reaches the `--prompt` argument. *Test:* a property test over random `number` values and hostile label/assignee strings asserts every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`.
<!-- Source: rulings C-010, INV-011, INV-018, C-025 - merged per Change #40 -->
- **NFR-002 Read-only GitHub and allowed argv (security).** The poller issues only reads. Every runner argv starts with one of: `gh api user`; `gh issue list`; `gh api --method GET repos/IronbellyOrg/IronClaude/...`; `gh api graphql -f query=<module constant>`; `git -C <abs> remote get-url origin`; the `_find_orca` probe; the Orca launch argv (FR-013). No argv requests `title`, `body` or comment `body` fields; marker and edit checks are `--jq` boolean or timestamp projections. *Test:* any recorded argv of another form fails the test (NG-2).
<!-- Source: rulings C-003, X-005, INV-018 - merged per Change #41 -->
- **NFR-003 Repo and Project pinning.** Every repository-scoped call names `IronbellyOrg/IronClaude` literally. Project reads go only through the issue's `projectItems` filtered to the configured `project_id`. *Test:* scan of all recorded argv; zero occurrences of `SuperClaude-Org` and of `{owner}`.
<!-- Source: Base (original) -->
- **NFR-004 No shell.** `subprocess.run` is called with a list and `shell=False`. *Test:* the injected runner rejects a `str` argv; `test_no_shell` (an AST check) asserts `shell=True` does not appear under `src/superclaude/cli/issue_watch/`.
<!-- Source: ruling C-022 (round 1, all five variants) - merged per Change #42 -->
- **NFR-005 At-most-once and crash safety.** Per store, fresh launches (argv with `--prompt`) per issue never exceed `max_launches` (1 [PROPOSAL]). *Tests:* an AST `test_no_shell`; stub end-to-end; crash injection at every write and spawn boundary, each followed by 5 reruns with zero second launches; two concurrent processes on one state directory; an account rename; a `FakeRunner` exiting 99 on any unexpected argv; `_assumed_shape` fixtures for unverified GitHub shapes; `test_no_text`; a 50-cycle at-most-once run.
<!-- Source: rulings C-019, C-025; Variant D round 2 - merged per Change #43 -->
- **NFR-006 Observability.** Audit lines follow FR-020, carry `host`, never `rate_remaining`, and never issue text. Rotation at 5 MiB [PROPOSAL]. *Test:* schema validation; a `PWNED-TITLE` fixture title and body never appear in any argv, audit line, record or prompt (`test_no_text`).
<!-- Source: Base (original, modified) - scope aligned with FR-022 -->
- **NFR-007 Fail closed.** Any failure of a shared input (FR-022), timeout, non-JSON reply or truncation before the launch phase yields zero launches. *Test:* table-driven failure injection on each read call.
<!-- Source: rulings C-008, INV-017 - merged per Change #44 -->
- **NFR-008 Time budget.** `gh` timeout 20 s [PROPOSAL]; Orca timeout 120 s [PROPOSAL]; cycle deadline 240 s; no launch starts after 120 s (FR-029), inside the 300 s cadence. *Test:* a sleeping stub yields reason `gh_timeout`, exit 3.
<!-- Source: rulings C-006, S-003 (Variant E arithmetic), X-007 - merged per Change #45 -->
- **NFR-009 Rate budget.** Per-issue calls, including every page, stop at a 35-call cap per cycle [PROPOSAL]; candidates beyond it skip `budget_exhausted`. Idle cycle: 2 calls, 24 per hour (0.48% of the 5,000 an hour allowance, RD fact 9). Worst cycle: 35, 420 per hour (8.4%). W workspaces on one login multiply both by W. A rate limit is exit 5 (FR-028). *Test:* call count with 10 candidates; rate-limit stub.
<!-- Source: Base (original) -->
- **NFR-010 Idempotent cycle.** A second `once` against identical stub state launches nothing. *Test:* direct.
<!-- Source: rulings X-003 (round 3 final), S-005, X-007 - merged per Change #46 -->
- **NFR-011 Crash-safe state.** Record writes use `write_prepared_bytes` plus a parent-directory fsync; file mode `0600`, directory `0700`. An unparseable store, an unknown `schema_version`, or a store or lock missing after `init-state` gives exit 6 and zero launches. The file is never changed or reset. Recovery: move the state directory aside and run `init-state`, which sets a new `created_at`, so earlier approvals are not re-dispatched. Backup restore is unsupported. *Test:* truncated JSON fixture; missing-store fixture.
<!-- Source: Base (original) -->
- **NFR-012 Footprint.** No new dependency; at most one new session per cycle. *Test:* dependency list unchanged; FR-016.
<!-- Source: Base (original, modified) - (b) narrowed and (d) added per Change #47 (U-011, INV-004, INV-006) -->
- **NFR-013 SLO signals [PROPOSAL].** (a) approval-to-`launched` p95 ≤ 10 minutes while the workspace runs; (b) ≥ 99 percent of cycles over 7 days exit 0, counting only exit-0 cycles as healthy; (c) ≥ 95 percent of `launched` records reach `claimed` within the lease; (d) no `unknown` or `pending_orphan` entry stays unacknowledged for more than 24 h. All computable from `audit.jsonl` and `dispatch.json`. *Test:* a helper reduces a fixture log to the four numbers.
<!-- Source: Variant A text, ruling S-004 (round 2) - merged per Change #48 -->
- **NFR-014 Module boundaries.** The package `src/superclaude/cli/issue_watch/` holds `runner`, `github`, `predicates`, `record` (store and lock), `launch`, `audit`, `cycle` and `cli`. Protocols exist only for the runner, the store and the launcher. It reuses `swarm/atomic.write_prepared_bytes` and `_find_orca`. No module is named `select`.

## 6. Security model

<!-- Source: Base (original, modified) - rows T4, T7, T8, T10 replaced per Changes #49-#52; T13-T16 added per Change #53; T17 added per base-selection item 11 (AC-3) -->
GitHub content is untrusted; IronbellyOrg/IronClaude is a public repository. The own login, state directory and configuration are trusted at workspace-user level. The poller holds no token of its own.

| # | Asset | Threat | Control | Residual risk |
|---|---|---|---|---|
| T1 | Launch prompt | Prompt injection from issue text | Fields restricted (FR-003, FR-011); jq projections; `build_claim_prompt` integer-only (FR-012); NFR-001 | The launched claim reads title, body and comments live in a PUBLIC repo (RD fact 5); not solved here |
| T2 | Approval gate | Non-approver applies the approval label | Latest-actor check against allow-list; Triage-or-higher needed to label (FR-005, FR-006) | Compromised approver account; allow-list edited by a writer |
| T3 | Approval gate | Bot or automation applies the label | `actor.type == "User"` required | A human-controlled bot account typed `User` |
| T4 | Approval meaning | Body edited after approval | The "unchanged since approval" check (Section 3) skips any issue whose body or non-own comments were created or edited after approval, or renamed (INV-026; merged per Change #49) | Edits after the re-read and before the claim reads the issue; controls are the deployment gate and the permission mode (C-014, R13) |
| T5 | Repository target | gh defaults to the upstream parent | Repo pinning (NFR-003) | None known |
| T6 | Host shell | Metacharacters in data | argv lists, `shell=False` (NFR-004) | None known |
| T7 | Issue ownership | Two workspaces of one login both launch | `enabled` defaults to false. Enable the poller in exactly one workspace per login; a second workspace on the same login is unsupported. Every audit line carries `host` and `login`, so a double enablement is visible (C-005; merged per Change #50) | Two stores on one login (R12); OD-8 |
| T8 | Dispatch record | Tampering, deletion or loss | Mode `0600`; corrupt record fails closed (NFR-011). `init-state` records `created_at`; approvals older than it never count, so a lost store cannot re-dispatch old approvals. A missing store or lock exits 6 (INV-024; merged per Change #51) | A restored older backup (R11) |
| T9 | `gh` token | Scope widened with `read:project` | Poller is GET-only (NFR-002, NG-2) | Token can still write |
| T10 | Launched session | Broad permissions | No cron entry is enabled until an owner-run live test shows the prompt running as a slash command and records the session's permission mode. The default is no override. A bypass mode requires the owner's written acceptance (C-014; merged per Change #52) | `orca agent launch` has no permission flag (RD fact 6); OD-7 |
| T11 | Logs | Issue text leaks into logs | Restricted audit schema (NFR-006); `gh` stderr truncated to 500 bytes [PROPOSAL] | Server messages in truncated stderr |
| T12 | Availability | Flood of tagged issues | Caps (FR-016), truncation fail-closed (FR-004), rate budget (NFR-009), day cap (FR-024) | Legitimate issues delayed |
| T13 | Approver allow-list | Edited by another local user | File must be owner-owned and not group/other-writable, else exit 2 (FR-027; C-013, INV-019; merged per Change #53) | None known |
| T14 | Approval gate | Allow-listed approver demoted or compromised | Not mitigated in v1 (merged per Change #53) | Residual R10 (INV-010); FU-9 |
| T15 | Approval gate | A human-run automation labels as a `User` | None beyond the `[bot]` login check (merged per Change #53) | Residual (A-008) |
| T16 | Dispatch timing | Approval removed after the re-read, or a hand claim while enabled | Runbook forbids hand-claiming trigger-labelled issues while enabled (Section 8, step 10; merged per Change #53) | Residual (INV-023, INV-021; R14, R15) |
| T17 | Launch binary | A binary named `orca` that is not the Orca CLI (the GNOME screen reader) | The probe accepts only a binary whose `skills list --json` reply lists the `orca-cli` topic (FR-013; Variant B, merged per base-selection item 11, AC-3) | None known |

## 7. Dispatch record and at-most-once semantics

<!-- Source: Base (original) -->
**Why a local record.** The claim has no compare-and-set and leaves the issue in Backlog (RD fact 4); under candidate 1 the issue is already assigned to the own login. Only the record, written before launch, prevents a relaunch before the claim marker appears.

<!-- Source: ruling S-005 (round 2, Variant D text), C-017, conflict ruling K7 - merged per Change #54 -->
**Store form and location.** One versioned JSON record file per state directory, `<state_dir>/dispatch.json`, default directory `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` [PROPOSAL], written with `write_prepared_bytes` (0600) plus a parent-directory fsync. Only `init-state` creates it. If it is missing after init, unparseable or of unknown version, `once` exits 6 with no launch and leaves the file untouched. No SQLite. Tombstones (terminal entries) are never pruned. ASSUMPTION: the directory survives a restart only if the Coder template persists `$HOME` (A-001; RD Q15).

<!-- Source: rulings C-007 (round 3 final), INV-007, INV-015, INV-016, INV-024, U-005 - merged per Change #55 -->
**Schema.** Store: `schema_version`, `created_at`, `next_permitted_at`, `considered`. Entry: `issue`, `state`, `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `launch_cwd`, `launch_login`, `launch_account_id`, `consumed_at` (immutable), `pending_at`, `created_at`, `updated_at`, `lease_expires_at`, `last_reason`. All times are UTC ISO 8601. `attempts` counts pre-pending tries; `launches` counts `pending` writes, so a session may exist whenever it is above 0.

<!-- Source: ruling C-007 (round 2 Variant D text, confirmed round 3) - merged per Change #56; re-approval note from Variant B OD-6, merged per base-selection item 12 (AC-5) -->
**Launch counter rule.** `launches` is incremented in the same durable write as `pending`, before Orca is spawned; a fresh launch requires `launches == 0`. Re-labelling, re-approval, lease expiry and login change never reset it; only `reset <N> --forfeit-guarantee` does. A newer approval event is reported as `re-approved` in the decision line and resets neither `attempts` nor `launches`.

<!-- Source: ruling C-007 (round 3), INV-001, conflict ruling K1 - merged per Change #57 -->
**States.** `pending`, `launched`, `unknown`, `failed`, `abandoned`, `claimed`. Resolution "pre-pending failed": `failed` arises only before a `pending` write, has `launches == 0`, and retries after a 10-minute backoff up to `max_attempts` 3, then becomes `abandoned` `attempts_exhausted`. No transition leads from `pending` or later to `failed`.

<!-- Source: rulings C-008 (round 2), INV-015, conflict ruling K5 - merged per Change #59 -->
**Parameters.** All [PROPOSAL]: lease 60 min (reporting only), `max_attempts` 3, `max_launches` 1, `max_candidates` 10, `max_launches_per_cycle` 1, `failed` backoff 10 min, day cap 6 per rolling 24 h, call cap 35 per cycle.

<!-- Source: rulings X-001, X-002 (round 2, Variant D text), INV-004, INV-002, INV-021, C-024, K13, A-009 - merged per Change #58 (replaces the whole base table) -->
**Transitions.**

| From | Trigger | To | Notes |
|---|---|---|---|
| (none) | prompt `ValueError` or transient re-read error | `failed` | `launches` 0, `attempts` + 1 (K1) |
| `failed` | backoff elapsed, `attempts` < 3 | eligible again | re-runs every check |
| `failed` | `attempts` = 3 | `abandoned`, reason `attempts_exhausted` | |
| (none) or `failed` | all checks passed | `pending` | `launches` + 1, `consumed_at` set, `pending_at` set |
| `pending` | Orca confirmed success | `launched` | `operation_id` stored; lease set |
| `pending` | any other outcome after spawn (timeout, malformed output, `agent_session_operation_unknown`, non-zero exit) | `unknown` | slot consumed (INV-002) |
| `pending` | exec `OSError` before the child starts | `abandoned`, reason `spawn_error` | |
| `pending` | found at cycle start | `abandoned`, reason `pending_orphan` | prefers a missed dispatch to a double one (X-002) |
| `launched` | lease end with no marker | `abandoned`, reason `claim_not_observed` | report only; the slot is not released (X-001, A-009) |
| `launched`, `unknown` or `abandoned` | own marker newer than `pending_at` | `claimed` | INV-021 |
| (none) | own marker newer than the current approval | `claimed` | never launched; `launches` 0, no `consumed_at` (C-024) |
| `abandoned` or `unknown` | `reset <N> --forfeit-guarantee` | (none) | `launches` back to 0; `consumed_at` kept in the day cap; the operator has checked the session first (merge decision M1) |

`unknown` never moves on the lease; it leaves only via `claimed` or `reset`. `claimed` is terminal; `abandoned` is terminal except for a later own marker or `reset`. A fresh launch requires `launches == 0`, so at-most-once holds even when Orca's reply is lost. Every row is one test case in `test_record.py`.

<!-- Source: rulings X-003 (round 3 final), C-020, INV-024 - merged per Change #60 -->
**Recovery.** Recovery is never a hand edit. A single stuck entry: `reset <N> --forfeit-guarantee`. A broken store: move the directory aside and run `init-state`; approvals older than the new `created_at` need a re-label.

**Scope.** The guarantee holds per intact, single store per login (Section 1).

## 8. Repo-side deliverables (testable with mocks)

<!-- Source: ruling S-004 (round 2) - merged per Change #61 (filters becomes predicates, state becomes record) -->
**Modules** under `src/superclaude/cli/issue_watch/`, as fixed by NFR-014: `runner.py` (`run_command(argv: list[str], timeout)`, rejects `str` argv); `github.py` (reads, pagination, truncation, rate limits); `predicates.py` (pure Section 3 predicates; `is_intended_owner()` is the one replaceable routing function); `record.py` (store, transitions, lock, kill switch); `launch.py` (`build_claim_prompt`, `_find_orca` reuse, origin check, launch); `audit.py`; `cycle.py`; `cli.py`. Protocols exist only for the runner, the store and the launcher. Registered after `main.add_command(reflect_group, name="reflect")`; no `pyproject.toml` change.

<!-- Source: rulings C-021 (Variant A), C-020, C-005 - merged per Change #62 -->
**CLI verbs and configuration.** Verbs as in FR-026. `once` takes only `--dry-run` and `--config <path>`. Labels, `project_id`, `owner_account_id`, worktree, approvers file and `state_dir` come from the JSON config (FR-027) validated by `check-config`. There is no flag-only interface.

<!-- Source: rulings X-007 (round 2, Variant A text), INV-006 (round 3), conflict rulings K4, K6 - merged per Change #63 -->
**Exit codes** [PROPOSAL]:

| Code | Meaning | Operator action |
|---|---|---|
| 0 | Cycle complete (any number of launches, including zero), or `disabled` | None |
| 2 | Usage, configuration, platform, origin or Orca probe failure | Run `check-config`; fix the config, approvers file, worktree or Orca install |
| 3 | GitHub auth, scope, timeout or non-JSON reply | Check `gh auth status` and scopes; read the cycle line's reason |
| 4 | Discovery truncated (100 results) | Remove the trigger label from claimed issues (R3) |
| 5 | Rate limited; the next permitted time is persisted (FR-028) | None; later cycles exit 5 until that time passes |
| 6 | Record unreadable or unwritable, or store or lock missing after `init-state` | Move the state directory aside and run `init-state` (NFR-011); never hand-edit |
| 7 | A launch ended `failed`, `unknown` or `abandoned` with reason `spawn_error` (merge decision M2) | Read `status`; for `unknown`, check the session and, if needed, run the printed retry command (FR-015) |
| 75 | Lock held by another cycle, or the lock's inode changed | None unless repeated; repeated means a hung cycle |

When several apply, the cycle exits with the first of 2, 6, 7, 5, 3, 4. Every condition is also an audit line. Exit 75 applies only when the lock was not taken (or its inode changed) and nothing else ran.

<!-- Source: Base (original, modified) - test files and acceptance property appended per Change #64 (C-022, seed acceptance criterion, C-012) -->
**Tests** under `tests/issue_watch/`: one file per module, `test_cli_e2e.py` (stub executables on PATH, as in `tests/pr_submit/test_conflict_e2e.py`), `test_security_invariants.py` (NFR-001 to NFR-004), `test_predicates.py`, `test_record.py` (every Section 7 transition row), `test_crash_injection.py`, `test_concurrency.py`, `test_no_shell.py`, `test_no_text.py` and `test_origin_parity.py`. Each FR criterion and each Section 7 row is one test case. Nothing runs live.

**Acceptance.** Given a mocked `gh` returning N matching issues, the poller starts exactly one mocked launch per eligible issue, each with the integer number only, and records each dispatch. Because one launch is made per cycle, the end-to-end test runs N cycles. The prompt-regex property test of FR-012 also holds.

<!-- Source: ruling S-003 (round 1) - merged per Change #66; table in the Variant B style, budget arithmetic in the Variant E style -->
**Gates:** `uv run pytest tests/issue_watch/`, `make lint`, `make sync-dev`, `make test`, `make verify-sync`.

**Failure modes.**

| Failure mode | Root cause | Exit |
|---|---|---|
| Bad config, approvers file, platform, worktree origin or Orca probe | Workspace setup | 2 |
| `gh` auth, missing scope, timeout, non-JSON reply | Token or GitHub availability | 3 |
| Discovery returns 100 results | Too many open trigger issues for the owner (R3) | 4 |
| Rate-limit reply | API allowance spent | 5 |
| Store unparseable, unknown version, missing store or lock | Lost or damaged state directory | 6 |
| Pre-pending `failed`, launch outcome `unknown`, or `abandoned` `spawn_error` | Orca runtime, exec or re-read failure | 7 |
| Lock held or replaced | Overlapping or hung cycle | 75 |
| Per-issue read failure | One issue's events, Project item, marker or re-read | 0 (issue skipped with a reason) |

**Budget arithmetic** (NFR-009, [PROPOSAL]): idle cycle 2 calls (`api user` and discovery), 12 cycles an hour, so 24 calls an hour, 0.48% of 5,000; worst cycle 35 calls, 420 an hour, 8.4%; W workspaces on one login multiply both by W.

<!-- Source: Base (original, modified) - steps 1-5 kept with Change #74 sweep; step 6 replaced and steps 7-10 appended per Change #65 (C-017, C-023, INV-008, INV-014, INV-021, INV-024) -->
**Design doc** `docs/designs/issue-watcher.md` (house format): D1 to D3, options B, C, D with revisit conditions, the Coder#477 statement (Section 9), and an **operator runbook**:

1. Pre-flight: `gh auth status`; `gh auth refresh -s read:project` if the Project read fails; `orca` on PATH; worktree exists; `check-config` exits 0.
2. Label setup (owner-run; `/sc:issue` never creates labels): `gh label create issue-watch:trigger --repo IronbellyOrg/IronClaude` and `gh label create issue-watch:approved --repo IronbellyOrg/IronClaude`.
3. Shadow rollout: run `once --dry-run` on schedule for 24 hours [PROPOSAL]; compare the would-launch decision lines with expectation before removing `--dry-run`.
4. Disable with `touch <state_dir>/DISABLED`; enable by removing it.
5. Exit codes, reason codes, `status --json`; recovering an `abandoned` entry with `reset <N> --forfeit-guarantee`.
6. Alert when `last_completed_cycle_age_seconds` > 900.
7. Run `init-state` before the 24 h shadow; re-apply approval labels on issues approved before init.
8. Setup order per issue: assign the owner, add the trigger label, then the approval label.
9. Before cron: a 24 h shadow `--dry-run` whose audit is reviewed, a two-process lock test on the real state directory, a persistence check that `state_dir` survives a workspace restart, and the staleness alert wired up.
10. While enabled, never hand-claim a trigger-labelled issue; remove the trigger from claimed issues.

## 9. Follow-up not built here

<!-- Source: ruling C-023 (round 2, Variant A text), INV-003, INV-010, Variant D FU-1/FU-2/FU-4/FU-5 detail - merged per Change #67 -->
- **FU-1 Live slash-command and permission test (blocks enablement).** One owner-run launch on a test issue to confirm a leading `/sc:issue` runs as a slash command (RD Q1, Q2), record the session's permission mode (Section 1, Deployment gate), and capture real success and `unknown` JSON plus the event, `lastEditedAt` and `projectItems` shapes for the stub fixtures.
- **FU-2 Coder cron and persisted state.** `coder_script` with `cron = "0 */5 * * * *"` running `superclaude issue-watch once` (RD fact 10), plus a persisted `state_dir` if `$HOME` is not.
- **FU-3 Token scope.** Confirm the `read:project` scope (RD Q7) and the `projectItems` read with a workspace token.
- **FU-4 Alerting** on staleness or on exit 3, 4, 5, 6 or 7 for three consecutive cycles [PROPOSAL]; sink not chosen.
- **FU-5 ETag requests** to cut the cost of unchanged reads.
- **FU-6 Per-actor permission checks** in the launched session; trace whether Orca applies `agentDefaultArgs` (RD Q6); settle OD-7.
- **FU-7 Revisit tracking** against the nine conditions (Section 2); see the Coder#477 statement below.
- **FU-8 Automatic retry**, only after the live test records Orca's retry rule (RD Q3). It uses the cycle's one launch slot, re-runs the DISABLED, re-read and origin checks, starts by 120 s, makes at most 3 tries, and never changes `launches` or the day cap.
- **FU-9 Approver role check** (INV-010, R10), if the collaborator-permission endpoint works with a workspace token.
- **FU-10 SLO measurement** of NFR-013 from two weeks of real logs.

<!-- Source: ruling C-023 (round 2, last sentence); seed brief - merged per Change #68 (statement moved here from Section 2) -->
**Coder#477.** Option A makes IronbellyOrg/Coder#477 unnecessary. Options B and C, and Coder#477, return only on a revisit condition: the workspace cannot run a reliable cron, or one poller per login becomes unworkable.

## 10. Open decisions

<!-- Source: Base (original, modified) - OD-2, OD-5, OD-7, OD-8, OD-9 replaced and OD-10, OD-11 appended per Change #69 (S-006 numbering kept); OD-3 and OD-6 aligned with Section 3 and FR-027 -->

| ID | Decision | Recommended default | Reason |
|---|---|---|---|
| OD-1 | Label names | `issue-watch:trigger`, `issue-watch:approved` | Namespaced against the nine default labels; anyone may propose, only approvers approve |
| OD-2 | Approver allow-list location | Approvers by account ID in an owner-only file named in the config (FR-027); missing, empty or group/other-writable means exit 2 | Decided by ruling C-013; no extra GitHub read; fails closed |
| OD-3 | Intended-owner rule | Candidate 1, assignee set exactly {own login} | Matches the claim's own rule (`claim.md:41-42`); the only race-free candidate; isolated in `is_intended_owner()` |
| OD-4 | Project unreadable | Fail closed; no label-only flag | A silent fallback widens eligibility; Option D is the documented fallback |
| OD-5 | At-most-once parameters | As Section 7, all [PROPOSAL] | Owner confirms after the shadow run |
| OD-6 | State directory | XDG state path, overridable in the config | Persistence is a Coder template fact (FU-2, A-001) |
| OD-7 | Launched-session permission mode | Default interactive, no override; a bypass mode needs the owner's written acceptance | The session reads untrusted text (T1, R18); prompts keep a human before any write |
| OD-8 | Same login, several workspaces | One enabled workspace per login | The local record cannot see other workspaces; `host` in every audit line makes a double enablement visible; a shared ledger is a B/C revisit trigger |
| OD-9 | Claim's reads of issue text | Accepted residual, narrowed by "unchanged since approval" | Same as a manual claim today; changing `/sc:issue` is out of scope |
| OD-10 | Exit precedence | 2, 6, 7, 5, 3, 4 | Majority synthesis (INV-006) |
| OD-11 | `max_candidates` | 10 | 5 and 8 were the alternatives |

## 11. Risks

<!-- Source: Base (original, modified) - R3 and R8 rewritten per Change #70 (INV-014, INV-018, INV-004, A-009); R10-R18 appended per Change #71 (INV-010, INV-021, INV-023, INV-024, INV-025, INV-026, INV-012, A-006, S-008 columns) -->
Mitigations name the requirement that carries them. Likelihood and impact ratings for R11-R18 are [PROPOSAL].

| ID | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | Launch prompt not run as a slash command (RD Q1) | Unknown / nothing works | FU-1 before enablement; `claim_not_observed` surfaces it within one lease |
| R2 | Token lacks `read:project` (RD fact 8) | High today / every cycle exits 3 | Runbook pre-flight; Option D fallback |
| R3 | More than 99 open trigger issues assigned to the owner: exit 4 every cycle | Low / no dispatch | FR-003 warning at 80; runbook removes the trigger from claimed issues (FR-004) |
| R4 | Hung cycle overlaps the next | Low / skipped cycles | Lock, timeouts, exit 75 in health SLO |
| R5 | State directory lost on restart | Medium until FU-2 / second launch | `pending_orphan`, claim marker, OD-8 |
| R6 | Scheduler stopped or always failing, unnoticed | Medium / issues wait | `status` staleness, FU-4 |
| R7 | Launched sessions stay open (RD Q21) | Medium / process build-up | One launch per cycle; runbook note |
| R8 | Launch outcome unknown | Low / issue waits | The entry stays `unknown` and blocks a relaunch; `status` lists it after 24 h (NFR-013 d). The lease is a reporting threshold only (A-009 rejected as a safety premise) |
| R9 | Stopped workspace polls nothing (RD fact 10) | Certain / latency | Accepted under D1; B revisit condition |
| R10 | An allow-listed approver who is demoted, removed or compromised stays a valid approver until the owner edits the file (INV-010) | Low (three Triage-plus accounts) / High | `check-config` prints the file's mtime and entry count (FR-027); FU-9. Accepted residual, not a requirement |
| R11 | A restored older store re-allows launches (INV-024 case 6) | Low / second launch | Backup restore unsupported (NFR-011) |
| R12 | Two stores on one login (INV-024 case 7) | Low / second launch | T7; `host` field (FR-020); API cost multiplies by W (NFR-009) |
| R13 | Edits or comments after the re-read reach the session (INV-026) | Low / injected instructions | Deployment gate (C-014); OD-7 |
| R14 | A concurrent hand claim (INV-021) | Low / duplicate work | Runbook step 10 |
| R15 | An approval removed, or DISABLED created, after the spawn starts cannot stop the session (INV-023, INV-012) | Low / unwanted session | Accepted residual; FR-018 stops anything not yet started |
| R16 | Clock jumps distort lease, backoff, day cap and ordering; none affects `launches` (A-006) | Low / timing only | Accepted residual |
| R17 | Any commenter can stall an approved issue until re-approval (INV-026) | Medium / delay | Re-apply the approval label (Section 3, Unchanged since approval) |
| R18 | The integer-only prompt keeps issue text out of the prompt but not out of the session: the claim reads title, body and comments (`claim.md:26`, `:56`) (INV-025) | Medium / injected instructions | Deployment gate (C-014), OD-7 permission mode, "unchanged since approval". Accepted residual |

## 12. Traceability

<!-- Source: Variant A text, ruling S-007 (round 2) - merged per Change #72; base rows kept and extended; no count summaries (S-002) -->
Every requirement cites its source, using a seed section, research fact, research question or `file:line`. A source that has not been verified is tagged UNVERIFIED. INV, C, X and S identifiers name the adversarial rulings that fixed a requirement.

| Requirement | Source fact |
|---|---|
| FR-001, FR-017, NFR-008, R4 | RD fact 10 (cron); SB Constraints (5 minutes); RD Q15; INV-027 (lock inode) |
| FR-002, FR-003, NFR-001, T1 | SB D3; RD Security model (own login, fields `number,labels,assignees,state`); RD fact 5; C-004; C-006 |
| FR-004, FR-007, OD-4, R2, R3 | RD fact 8; RD Q7, Q8; X-005; INV-014; `projectItems` shape and scope UNVERIFIED |
| FR-005, FR-006, T2, T3 | RD fact 7; SB Q3; C-002; INV-009; `poll-augment-review.sh:46-56`; event shape UNVERIFIED |
| FR-008, OD-3 | RD Intended-owner filter; SB Constraints; `refs/claim.md:41-42`; K12 |
| FR-009 | `refs/claim.md:29` marker; C-024; INV-021 |
| FR-010, FR-011, FR-014, FR-016, FR-020, NFR-005, Section 7 | RD fact 4; SB Enrichment (record before launch, re-read, six states, caps, considered map, audit line); C-007; C-009; INV-001; INV-002 |
| FR-012 | RD plan step 3.2; SB D3; C-012 |
| FR-013, FR-015, T10, T17, OD-7, R8 | RD fact 6; RD Q6; C-010; INV-003; Orca retry rule UNVERIFIED (RD Q3); slash-command prompt execution UNVERIFIED (RD Q1) |
| FR-018, FR-019, FR-021, NFR-006, NFR-007, NFR-012, NFR-013 | Operational additions; SB Success Criteria (observable acceptance); INV-004; INV-005; INV-006; INV-012 |
| NFR-002, NFR-003, NFR-004, T5, T6 | SB Constraints; CC (injectable runner); INV-018; C-025 |
| NFR-009 | RD fact 9; C-006; S-003 |
| NFR-010 | SB Success Criteria |
| NFR-011, OD-6, R5, OD-8, T7 | RD Q14, Q15; X-003; C-005; `$HOME` persistence UNVERIFIED (RD Q15) |
| R1, FU-1, FU-7 | RD Q1; SB Q1; C-014; C-023 |
| FR-022 | C-015 |
| FR-023 | INV-015 |
| FR-024 | INV-016; K10 |
| FR-025 | INV-011; C-010; `origin_repo.py:86-99` |
| FR-026 | C-020; K7; K10 |
| FR-027, T13 | C-021; C-013; INV-019; A-010 |
| FR-028 | C-016; X-006; X-007 |
| FR-029 | INV-017; C-008 |
| NFR-014 | S-004 |
| T4, R13, R17 | INV-026; `lastEditedAt` availability UNVERIFIED |
| T14, R10 | INV-010 |
| T15 | A-008 |
| T16, R14, R15 | INV-021; INV-023; INV-012 |
| R11, R12 | INV-024 |
| R16 | A-006 |
| R18 | INV-025; `claim.md:26`, `:56` |
| A-001..A-010 | Diff-analysis assumptions A-001..A-010 (Section 13) |

## 13. Assumptions and constraints

<!-- Source: diff-analysis A-001..A-010, rounds 1-3 - merged per Change #73 (new section) -->
Each line is an ASSUMPTION (relied on, not yet verified), a CONSTRAINT (enforced by design) or REJECTED (not relied on), with its adopted condition.

- **A-001** ASSUMPTION: `state_dir` survives workspace restarts. Condition: verified by the runbook persistence check before cron (UNVERIFIED until then).
- **A-002** ASSUMPTION: a leading `/sc:issue` in `--prompt` runs as a slash command. Condition: enablement blocked until the live test (FU-1).
- **A-003** CONSTRAINT: labels and the Status field and option are matched by name and fail closed; owner and approvers by account ID; Project by node ID.
- **A-004** CONSTRAINT: one enabled poller per login; a second is unsupported (T7, R12).
- **A-005** CONSTRAINT: the owner is assigned before approval; an approved unassigned issue is never seen (INV-014).
- **A-006** ASSUMPTION: the wall clock is correct; a jump affects timing only, never `launches` (R16).
- **A-007** CONSTRAINT: local Linux filesystem; network filesystems refused (Section 2).
- **A-008** ASSUMPTION: a `User` actor not ending `[bot]` is a human decision; residual T15.
- **A-009** REJECTED as a safety premise: the lease only reports; a late marker still gives `claimed`.
- **A-010** CONSTRAINT: the approver file is owner-only, checked by `check-config` and `once` (INV-019).
