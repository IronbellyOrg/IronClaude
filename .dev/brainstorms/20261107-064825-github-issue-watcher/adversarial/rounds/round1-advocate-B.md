# Round 1 Advocate: Variant B (analyzer persona)

## Position summary

Variant B is the best base for the selection and evidence layer: it derives every mechanism from three named root causes (B §1.1 RC1-RC3), proves approval from the complete event history with fail-closed truncation (B §3, FR-007, FR-008), resolves Orca the way this repo already does (FR-014), and records who approved each launch (FR-020). Its dispatch-record recovery rules are wrong in three places (X-001, X-003, X-006), and the final spec should take those rules from D and E instead.

## Steelman per opposing variant

**A (pipeline of stages).** Strongest form: every open decision and every alternative (B, C, D) replaces one module behind a typed protocol (A §1, §8, NFR-011), so the spec survives decision changes without a rewrite. A gets right: a bot check on the approver (A §3 "type `Bot` or login ending `[bot]`"); a corrupt record fails closed with exit 6 (A §7); rate limits end the cycle with no state change (NFR-006); a per-login state directory so a changed login inherits nothing (A §7 "Location"); `enabled` defaults to false (OD-2), which turns the same-login rule into a guard rather than a note; the JSON config choice is grounded in Python 3.10 support (OD-9).

**C (readiness and strict identity).** Strongest form: identity is anchored to GitHub node and account IDs (C §3, §7), so renames of labels, approvers, owners or Project fields cannot silently change eligibility, and one durable transaction consumes the launch slot before any external call (C §7), giving the strictest at-most-once guarantee of all five. C gets right: "recreating an empty ledger could duplicate every claim" (C §10), a missing initialized store is an error, not a fresh start (NFR-003), and deployment stays disabled until the narrative-read risk is accepted (C §6).

**D (operations).** Strongest form: D is the only variant an operator could run on day one: an exit-code table with an action per code (D §8), a `DISABLED` kill switch (FR-018), a 24-hour shadow dry-run (D §8 runbook step 3), staleness detection (`last_cycle_age_seconds` above 900), and SLOs computable from the audit log (NFR-013). D's record has separate `attempts` and `launches` counters (D §7 Schema), which is the cleanest way to express "a session may exist, so never a fresh launch".

**E (cost).** Strongest form: cost scales with candidates, never with the size of the Project (E §5), because Project membership comes from each issue's own `projectItems` (FR-008); this removes the 100-item ceiling that A, B and D all hit. E drops unowned candidates before any per-candidate call (FR-004), caps launches per day (FR-018), and states the bias explicitly: "every ambiguous state resolves toward not launching" (E §7).

## Strengths claimed

1. **Design traced to root causes, not features.** B §1.1 names three missing mechanisms (no ready signal, claim routes to whoever runs it, no at-most-once start), each with evidence (RD-F7, `refs/claim.md:41-42`, RD-F4) and a design consequence. Every later section maps back to one of them, so a reviewer can check that nothing is built without a cause. I re-checked the RC2 citation: `refs/claim.md:41` stops on an issue "assigned to anyone other than the current login" and line 42 allows a re-claim by the same login, so "assigned to own login only" (B OD-1) is the only routing rule the claim cannot refuse.
2. **Approval is proven from complete evidence, and fails closed when it is incomplete.** B §3 requires "the latest `labeled`/`unlabeled` event for that label" over "the complete REST event list", and FR-008 rejects the issue as `approval-unverifiable` when the page cap is reached. This is the root cause of a subtle defect in A, D and E: the issue-events endpoint is paged, and an issue with a long history needs every page to find the latest event (event order and page size should be confirmed in the live test). E FR-006 specifies "one ... call per examined candidate" and NFR-005 caps calls at 35, which cannot read a multi-page history; A and D are silent on paging. Only B and C (C §3 "incomplete event history ... fails approval") close this.
3. **Orca resolution reuses tested repo code.** B FR-014 probes `orca-ide` then `orca` and accepts only the `orca-cli` topic, because `orca` may be the GNOME screen reader (T7). This is not invented: `src/superclaude/cli/install_user_setup.py:198-221` (`_find_orca`) does exactly this with `_ORCA_CLIS = ("orca-ide", "orca")` (line 35). A, D and E hard-code `"orca"` as argv[0] (A FR-012, D FR-013), which on a Linux host can execute the screen reader. The diff rates this High (U-004).
4. **Accountability for every launch.** B FR-020 writes one line per decision with `approver` and `approval_event_id`, and the record stores both (B §7.2). After an unwanted session, the question "who approved this?" is answered from the local log without another GitHub call. A, D and E log cycle counts; only E stores `approval_actor` (E §7), and none store the event id that makes the evidence checkable.
5. **The cap cannot be bypassed by toggling labels.** B OD-6: a newer approval is reported `re-approved` and "does not reset `attempts`", because resetting "lets label toggling bypass the attempt cap" (U-005). No other variant states this.
6. **Correct split of fail-closed scope.** B NFR-009: a per-issue read error skips that issue; a login or discovery error ends the cycle (exit 2); a record-save error aborts (exit 1). This matches the cause of each failure: a 404 on one issue's events says nothing about other issues, while a failed login read invalidates every routing decision. A §3 voids the Project predicate for the whole cycle, and D NFR-007 makes any read failure yield zero launches, so one deleted issue stops all dispatch.
7. **Strictest reading of D1-D3 and the repo pin.** B NG1 forbids any GitHub write and gives the reason (a second writer without compare-and-set is unsafe, RD-F4); NFR-001 asserts it over every recorded argv; FR-002 checks the worktree `origin` before any call, so a SuperClaude-Org checkout cannot even start a cycle. The argv keeps the seed's fixed `--agent claude` (FR-012), unlike E FR-014.
8. **Test fixtures mark what is unverified.** B §8.3: fixtures for `project item-list` and the Orca reply carry `_assumed_shape` naming Q8 or Q2, and `FakeRunner` exits 99 on any unscripted call (U-006). When the live test reveals the real JSON, the fixtures to update are found by grep, and an unexpected extra call fails loudly instead of returning a silent default.
8a. **Text never enters Python.** B NFR-002: `--json` lists exclude text and marker detection uses `--jq` inside `gh`, tested with a hostile title. C §6 by contrast lets the marker check "inspect bounded comment content" in the process.

## Weaknesses identified in others

- **A: two retry paths can start a second session (X-002, X-004).** A §7 turns a `pending` entry with no marker into `failed` (`lost_reply`), and `failed` is retryable after the lease. But a crash between the record write and the Orca reply is exactly the case where Orca may have started the session: the root cause of RC3 (no at-most-once start) is reintroduced by the recovery path. The same holds for `unknown` becoming `failed` on lease expiry (A FR-014, §7): a timeout says nothing about whether the session exists. Because the claim posts its marker only in Wave 6 (`refs/claim.md` Waves 0-6), "no marker yet" is not evidence of "no session".
- **A, D: discovery capped at 100 items.** A FR-003 (`gh issue list -L 100`) and D's Project read hit a fixed ceiling; D R3 states that a Project over 100 items "always fails", so a growing Project silently becomes a permanent outage. E FR-008 removes the ceiling at the cause by asking each candidate for its own `projectItems`.
- **E: GraphQL conflicts with the read-only checks of A, B and D.** `gh api graphql` sends a POST, so a rule "every gh call is a GET" (A FR-002, D NFR-002, B NFR-001) rejects E's FR-008. The merged spec must define read-only as "no REST write verb and no GraphQL `mutation`", and test that the query string contains no mutation.
- **E: widens the fixed launch contract.** E FR-014 makes `--agent <agent>` configurable, which the seed argv fixes to `claude` (X-008). E FR-012 leaves the record of a removed issue "deleted or marked abandoned", an undecided state transition.
- **C: heavy for the risk it removes.** SQLite, an append-only transition table and an `init-state` verb (C §7, §8) add a schema migration surface to a 5-minute poller whose record holds a few entries. C §6 lets the marker check read bounded comment content in Python, which conflicts with C's own minimization aim (C-025).
- **D: an unenforceable default.** D OD-7 relies on the launched session's "default interactive mode", but the seed argv has no permission flag, so the poller cannot ensure it; the session inherits whatever the workspace sets (C-014).
- **A, D: fail-closed scope too wide (C-015).** One unreadable issue voids the whole cycle (A §3, D NFR-007); the failure's cause is local, so its effect should be local.

## Concessions

1. **X-001, B is wrong.** B §7.3 relaunches `launched` and `failed` entries after the lease when no marker is seen. B §7.4 itself marks the lease length an ASSUMPTION, and `refs/claim.md` posts the marker last. A slow claim therefore gets a second session. Adopt D/E: `launched` with no marker after the lease becomes `abandoned` (`claim_not_observed`), reported, never relaunched.
2. **X-003, B is wrong.** NFR-010 loads a corrupt file as empty. Every issue launched but not yet marked becomes eligible again. Adopt A/D: unparseable or unknown version gives a nonzero exit (D NFR-011), no launch, no reset, operator repair.
3. **X-006, B is wrong.** R9 treats the 5-minute cadence as back-off; a 403/429 mid-cycle then drives more per-issue reads into the limit. Adopt A/D/E: stop the cycle, exit nonzero, change no state. C's persisted next-permitted time is a reasonable addition.
4. **X-005, drop `--label-only`.** It removes two of the issue's own eligibility conditions. Prefer C/D fail closed, and use E's per-issue `projectItems` as the Project check in place of B's Project-as-discovery (C-003).
5. **Bot check missing.** B §3 accepts any allow-listed actor. Add A/D/E's check: `actor.type == "User"` and no `[bot]` login.
6. **Operations surface too thin.** B's single `once` verb and exits 0-3 (FR-021) cannot distinguish lock, rate limit, truncation and corrupt state. Take D's exit table with operator actions, add a `status` verb and D's `DISABLED` kill switch.
7. **Configuration as flags only (C-021).** A cron line with a dozen flags is fragile; A's JSON config (Python 3.10, OD-9) is better.

## Shared-assumption responses

- **A-001 QUALIFY:** only if the state path is verified persistent across workspace restarts (Q15) before enabling; a missing store after initialization fails closed (C NFR-003), never starts fresh.
- **A-002 QUALIFY:** that `/sc:issue --claim <N>` in `--prompt` executes as a command is unverified; gate the cron (B F1, OD-8) on the live test (F3).
- **A-003 QUALIFY:** login routing is safe because the claim itself uses `@me` (`refs/claim.md:47`); approvers should be stored as account IDs (C §3) or re-verified, since a rename transfers trust.
- **A-004 QUALIFY:** setup-only enforcement is weak; add A OD-2 `enabled` default false and audit `host` per cycle so a second poller is visible.
- **A-005 ACCEPT:** B OD-1 states it and RC2 requires it; audit must list `unassigned` skips so waiting issues are visible.
- **A-006 QUALIFY:** store UTC; a timestamp in the future counts as not expired, which errs toward not launching.
- **A-007 QUALIFY:** the state directory must be on a local filesystem on one host; `flock` on a network mount is not trusted.
- **A-008 QUALIFY:** add the `User` type and `[bot]` check; the residual is a human-run automation typed `User`, covered by the allow-list.
- **A-009 REJECT:** as a safety premise. `refs/claim.md` posts the marker in Wave 6 after a multi-agent Wave 4 of unmeasured duration, and B §7.4 calls the 60-minute value an ASSUMPTION. The lease may be a reporting threshold, never a relaunch trigger.
- **A-010 QUALIFY:** refuse a group- or world-writable allow-list file; the residual attacker is a home-directory writer, who can already run the claim by hand (E §6).

## Per-point positions

| Point | Level | Superior variant | Confidence % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | B | 50 | Tables with acceptance column are checkable row by row |
| S-002 | L1 | NONE | 50 | Counts reflect granularity, not quality |
| S-003 | L2 | HYBRID | 50 | B root causes + D runbook framing serve different readers |
| S-004 | L2 | B | 55 | 9 modules with `models` holding `REPO` pin in one place |
| S-005 | L3 | HYBRID | 55 | Single JSON under A's per-login dir; fail closed on corruption (D NFR-011) |
| S-006 | L1 | NONE | 50 | Numbering style only |
| S-007 | L1 | B | 55 | RD-F/SB codes trace to research facts |
| S-008 | L1 | NONE | 50 | All register risks; format immaterial |
| C-001 | L3 | A | 55 | Exact `watch:ready` label is simplest; C node IDs heavier |
| C-002 | L3 | HYBRID | 80 | B complete paging (FR-007/008) + A/D/E bot check |
| C-003 | L3 | E | 70 | Per-issue `projectItems` (FR-008) removes 100-item ceiling |
| C-004 | L3 | B | 55 | Exactly `[own login]` is what `claim.md:41-42` never refuses |
| C-005 | L3 | A | 65 | `enabled` default false (OD-2) makes the rule a guard |
| C-006 | L3 | HYBRID | 65 | E pre-filter (FR-004) + server-side `--assignee @me` |
| C-007 | L3 | HYBRID | 65 | D attempts/launches counters + B `launch_cwd`/approver fields |
| C-008 | L3 | HYBRID | 55 | Seed values; lease as report threshold only (A-009) |
| C-009 | L3 | D | 55 | Record before launch plus re-read; orphan pending becomes abandoned |
| C-010 | L2 | B | 85 | `_find_orca` in `install_user_setup.py:198-221` already does this |
| C-011 | L3 | HYBRID | 70 | B/E: `unknown` never auto-retried; only `--retry-launch` |
| C-012 | L3 | NONE | 50 | All five reject non-integers equivalently |
| C-013 | L3 | B | 60 | Empty list gives loud `E-NO-APPROVERS`, not silent no-op |
| C-014 | L2 | HYBRID | 65 | B no F1 before Q6 + C deployment disabled until accepted |
| C-015 | L3 | B | 65 | Per-issue errors local, global errors end cycle (NFR-009) |
| C-016 | L3 | HYBRID | 75 | A/D/E stop on 403/429, no state change |
| C-017 | L2 | D | 65 | Shadow dry-run and staleness check before cron |
| C-018 | L3 | D | 65 | `flock` plus `DISABLED` kill switch |
| C-019 | L2 | HYBRID | 65 | B per-decision lines with approver + D cycle fields and SLOs |
| C-020 | L2 | A | 60 | `once`, `status`, `check-config` cover operation; B too thin |
| C-021 | L2 | A | 55 | JSON config works on Python 3.10 (OD-9) |
| C-022 | L2 | HYBRID | 60 | B `FakeRunner` 99 + `_assumed_shape` + A AST no-shell test |
| C-023 | L2 | B | 55 | F3 names the live-test questions Q1-Q8 |
| C-024 | L3 | HYBRID | 65 | B own marker implies `claimed` + D `--jq` boolean check |
| C-025 | L2 | HYBRID | 55 | B/D: no text read, hostile-title fixture |
| X-001 | L3 | D | 85 | `launched` without marker becomes `abandoned`; B relaunch wrong |
| X-002 | L3 | HYBRID | 65 | B pending→launched with D/E no-relaunch; A `lost_reply` retry wrong |
| X-003 | L3 | D | 85 | Unparseable record exits nonzero, never reset (NFR-011) |
| X-004 | L3 | HYBRID | 75 | B/D/E timeout→`unknown`, no auto-retry; A wrong |
| X-005 | L3 | HYBRID | 75 | C/D fail closed + E per-issue Project lookup |
| X-006 | L3 | HYBRID | 75 | A/D/E stop and exit nonzero; C persisted next time optional |
| X-007 | L2 | D | 65 | One exit table with an operator action per code |
| X-008 | L2 | HYBRID | 70 | A/B/D keep `--agent claude`; E widens the argv |
