# Round 1: Advocate for Variant A (persona: architect)

Focus: maintainability and extension seams. Section references (§N) are to each variant's own sections; diff IDs are from `diff-analysis.md`.

## Position summary

Variant A should be the structural base of the final spec: it is the only variant that turns each open decision and each documented alternative into a one-module swap behind a named seam (§1, §8 module table, NFR-011), and it has the most offline-checkable configuration surface (`check-config`, JSON config, `enabled` defaulting to false). Its dispatch-record recovery rules are not the best, though: on a crash-orphaned `pending` (X-002) and on a launch timeout (X-004) A can launch twice. The final spec should take C's and D's ambiguity handling and put it into A's `record.py`.

## Steelman per opposing variant

**B (root-cause analyst).** Strongest form: every requirement traces to one of three root causes (§1.1 RC1-RC3), so nothing is decorative. It is the only variant that fails approval closed on a truncated event history (FR-008 `approval-unverifiable`). It guards against the GNOME `orca` screen reader by probing for the `orca-cli` topic (FR-014, T7). It keeps the approval evidence (`approver`, `approval_event_id`) and `launch_cwd` in the record (§7.2), and it refuses to let label toggling reset attempts (OD-6). Its `FakeRunner` exits 99 on any unscripted call, and its `_assumed_shape` fixtures (§4, §8.3) are the most honest way to test against JSON shapes nobody has verified. It is also the clearest about what must happen before enablement (OD-8: no cron before Q6).

**C (readiness scorer).** Strongest form: it is the most rigorous about identity. Node and account IDs instead of names (§3, §7) close the rename-and-reuse attacks that every name-keyed variant leaves open. It is also the most rigorous about at-most-once: "Consuming the slot and entering `unknown` is one durable transaction before external I/O. Expiry never releases a consumed slot" (§7). That is the only rule that makes NFR-002 true under every crash point. It refuses silent reinitialization ("recreating an empty ledger could duplicate every claim", §10). It persists a rate-limit next-permitted-request time (NFR-004). And it says plainly that a successful launch is not a successful claim (§1, FR-012).

**D (operations).** Strongest form: it is the only variant an operator could run on day one. It has an exit-code table with an action for each code (§8), a 24 h shadow dry-run rollout, a `DISABLED` kill switch (FR-018), a staleness signal (`last_cycle_age_seconds` > 900) and SLOs that can be computed from its own logs (NFR-013). Its separate `attempts` and `launches` counters (§7 schema) state the at-most-once invariant as one checkable inequality (`launches < max_launches`). An orphaned `pending` goes to `abandoned` (`pending_orphan`) and an expired `unknown` goes to `abandoned`, so no path leads to a second launch.

**E (cost-to-serve).** Strongest form: its call budget is worked out from first principles (§5), and it reads Project membership from each issue's own `projectItems` (FR-008). That makes cost scale with the number of candidates rather than the Project's size, and it removes the "Project over 100 items always fails closed" trap (D R3) that A and D both fall into. It drops unowned candidates before any per-candidate call (FR-004), has a hard call cap (NFR-005), bounds state growth (NFR-013), and states the cost asymmetry that justifies resolving ambiguity toward not launching (§7, "Cost rationale").

## Strengths claimed (variant A)

1. **Seams line up with the documented alternatives.** The §8 table names one seam per alternative: `IssueSource` (option D label relay, or a B/C event feed), `DispatchStore` (shared ledger on revisit), `Launcher` (B/C push client). §1 states the design rule: an alternative "replaces one stage, not the cycle". The seed requires B and C to stay documented alternatives with revisit conditions (Success Criteria; Q1). A is the only variant whose module plan already gives each of them a landing point. The best ideas from other variants also land in a single A module: E's per-issue `projectItems` changes only `github.py`; C's SQLite store is a second `DispatchStore`; B's `orca-ide` probe goes into `launch.py`/`runner.py`.
2. **The seams cannot drift silently.** NFR-011 checks the seams with an import test: `cycle.py` may import only stage protocols, and no dependency may be added. R-8 names interface drift as a risk and points to that test. No other variant protects its module boundaries mechanically; B NFR-013 and D NFR-012 cover only third-party imports.
3. **Owner routing is a table with a safety predicate shared by every rule.** FR-007 and §3 "Intended owner": "Under every rule, any assignee other than L excludes the issue", and the test runs "under every registered rule". So adding OD-1's alternatives (`person-label`, `project-field`, §8 `routing.py`) cannot weaken the claim-compatibility invariant (`claim.md:41-42`). B, D and E isolate a single function (`is_intended_owner`) but do not make the shared predicate apply to all future rules.
4. **The repo-wide no-write rule is enforced in code, not only in tests.** NFR-003: the GitHub layer raises `ForbiddenCommand` before it starts any process outside the allow-list (`api`, `issue list`, `issue view`, `project item-list`), and FR-002 forces `--method GET` on every `gh api` call. B NFR-001 and D NFR-002 only check recorded argv in tests, so a code path the tests miss could still write.
5. **Configuration can be checked offline, and the choice of format is justified.** OD-9 and §8: JSON, because `tomllib` needs 3.11 and the package declares `requires-python = ">=3.10"` (checked: `pyproject.toml:16`). `check-config` runs with no `gh` call and rejects a lease under 15 min (§7) and a relative or missing worktree (FR-013). B (§8.2, about 15 flags, "No other verb") and D (§8, flags plus a separate approvers file) put the whole configuration into a cron line, which cannot be validated before the scheduler fires.
6. **Same-login double dispatch is opt-in, not only covered by documentation.** OD-2: `enabled` defaults to `false`, so a second workspace on the same login does nothing until someone turns it on. B (OD-2), C (§7), D (OD-8) and E (O-4) rely on a setup instruction alone.
7. **The record is keyed by login.** §7 Location: `<state_dir>/<login>/record.json`, "so a changed login inherits nothing". If the `gh` login changes, the old login's entries cannot block or unblock the new login's issues.
8. **A corrupt record fails closed.** §7: "Unknown version or unparseable file: exit 6, no launch". C (§10) and D (NFR-011) agree; B NFR-010 does not (X-003).
9. **A `launched` issue is never relaunched.** §7: `launched_unclaimed` is reported in the audit and recovery is an operator verb (F-5). This sides with C, D and E against B on X-001.
10. **The prompt builder has an exact type and range rule.** FR-011 accepts an `int` that is not a `bool`, in 1..999999999, and raises a named `InvalidIssueNumber`. The bool exclusion matters because `isinstance(True, int)` is true in Python; a bare `int` check would let `True` through. B FR-013 and D FR-012 list `True` as an input to reject, but A is the only one with a dedicated exception type that callers can catch by name.
11. **The gh call budget is bounded and tested.** NFR-005: at most `3 + 3N` calls; 396 an hour worst case; there is a stub counter test.
12. **Per-entry transition history.** §7 schema `history` (last 20 entries) means an audit can explain any state without parsing the whole log; it is the cheap version of C's append-only transition table.

## Weaknesses identified in others

1. **B resets a corrupt record.** NFR-010: "A corrupt state file loads as empty and is replaced atomically". Every issue that has a `pending` or `launched` entry but no marker yet becomes launchable again, which contradicts B's own NFR-005. C §10 names this exact hazard.
2. **B relaunches a `launched` session.** §7.3: "`launched`, `failed` | lease expired ..., no marker, attempts left | new launch". A claim that runs past 60 minutes gets a second session. B itself calls the 60-minute lease an ASSUMPTION (§7.4), and the seed's `max_launches 1` is broken.
3. **B leaves no room to extend.** §8.2: "No other verb", so there is no `status` and no offline config check. The whole configuration is CLI flags, and `--label-only` (FR-022) is a second discovery mode that drops two of the issue's five definitions (B's own OD-5). Rate limits are "not handled specially" (R9), so B keeps reading per issue into a 403 storm (X-006).
4. **C is hard to test and hard to set up.** FRs are prose with no argv contract (S-001; FR-003 "explicitly scope repository calls"). An implementer cannot write the exact-argv test the seed's success criteria call for. Node IDs for labels, the Project, the Status field and the Backlog option (§3) are four opaque values an operator must look up through GraphQL before the first cycle, and C gives no lookup verb. Its marker check "may inspect bounded comment content" (§6), which weakens the text-minimization that A FR-004 and D §3 keep.
5. **C deliberately accepts permanent loss.** §7: "A crash between commit and submission can permanently suppress an otherwise eligible issue". That is defensible, but C offers no operator recovery verb; A F-5 and E `reset <N>` do.
6. **D ties the repo to the Coder template.** OD-2 ships the approvers file "with the Coder template", so a change to approval policy becomes a template release. D also defines `once` by flags only (§8), with no config file and no `check-config`.
7. **D's pre-launch failure deletes evidence.** FR-011 and §7: "entry removed". That loses the record that a reservation happened, which the audit trail and D's own SLO (c) would want.
8. **D's exit codes are inconsistent.** A Project read failure exits 3 (FR-007), while a Project truncation exits 4 (§8). The same predicate failing gives two different alert classes.
9. **E widens the fixed launch contract.** FR-014 `--agent <agent>` against the seed's `orca agent launch --agent claude` (X-008). A configurable agent is a redirect surface (A §6 "Launch target" row fixes it to `claude`).
10. **E leaves its pre-launch rule undecided.** FR-012: "the record is deleted or marked `abandoned`". A requirement with two outcomes cannot be tested.
11. **E's `claimed` rule is stricter than the claim itself.** FR-017 needs own assignee AND marker. If someone unassigns after a posted claim, the entry falls back to lease expiry and then `abandoned`, even though the claim happened.
12. **E adds speculative knobs.** A daily cap of 6 (FR-018), 30-day pruning (NFR-013) and an Orca-worker detector that depends on an ASSUMPTION "otherwise this requirement is dropped" (§6). These are additions that no source asks for.

## Concessions

1. **X-002: A can launch twice after a crash.** A §7: a `pending` entry found with an expired lease and no marker becomes `failed` (`lost_reply`), and `failed` is retryable. If the process died after Orca started the session but before the reply was stored, A starts a second session. That breaks A's own NFR-004 wording of "whatever step a crash interrupts". D (`pending_orphan` to `abandoned`) and C (slot consumed before I/O) are correct. Fix: an orphaned `pending` becomes `abandoned` (`pending_orphan`), never `failed`.
2. **X-004: A retries after a timeout.** FR-014: "any other failure moves it to `failed`". A timeout is not a definite failure. B and C map it to `unknown`; E defines `failed` as "definite error, no session started". Fix: only an explicit error reply counts as `failed`; a timeout, malformed output or killed process counts as `unknown` with no id, and that goes to `abandoned`, never to a fresh launch. Likewise, A's "`unknown` lease expired goes to `failed`" (§7) must become `abandoned` (D §7).
3. **D's `launches` counter is the better invariant.** Adopt D's `attempts` plus `launches`, so that "a fresh launch requires `launches == 0`" is the checkable at-most-once rule. A's single `attempts` counter mixes "tried" and "may have started".
4. **X-005: drop Project mode `off` from version 1.** OD-5 allows `off` "only by explicit config". That defines a mode that contradicts the issue's own definition, as B's `--label-only` does. The `IssueSource` seam already provides the honest fallback (option D, F-7). C (FR-006) and D (OD-4) are right.
5. **C-003: E's per-issue `projectItems` beats a 100-item Project listing.** A's FR-006 fails closed for good once the Project reaches 100 items (D R3 names the trap). E FR-008 scales with the number of candidates. In A this is a change to `github.py` only.
6. **C-014: B is right to gate enablement on Q6.** A OD-6 only documents the default permission mode. The final spec should state "no cron entry before the live test settles the permission mode" as a requirement (B OD-8, C §6).
7. **C's account IDs for approvers.** A matches the allow-list by `actor.login`. A deleted approver's login can be re-registered by someone else, and the check would then pass for the wrong person. Approvers should be matched by account ID (C §3). Label and Project names can stay names, because a rename only makes the check fail closed.
8. **B's `orca-ide` / `orca-cli` probe (U-004) and B's complete-event-history rule (FR-008) both close real gaps in A.** A trusts `orca` on PATH and does not handle a truncated event page.
9. **D's runbook and `DISABLED` file.** A has `enabled` in config, but D's kill switch works without editing config and is visible in `ls`. Adopt both, plus D's exit-code action column.
10. **A over-abstracts.** Eleven modules, with protocols for `ApproverSource` and `AuditSink` that no documented alternative needs, breaks the ponytail and scope rules. Keep protocols only where a documented alternative lands (`IssueSource`, `DispatchStore`, `Launcher`), and make approval and audit plain functions. `approval.py` can be merged into `predicates.py`.

## Shared-assumption responses

- **A-001** QUALIFY: keep local storage, on two conditions. The path must be persistent, and once the store has been initialized, a missing store must fail closed rather than be recreated (C NFR-003). `check-config` should warn when `state_dir` is under a path the template does not persist.
- **A-002** ACCEPT: every variant gates enablement on the live test (A F-2, B F3, D FU-1). No repo-side design can remove this.
- **A-003** QUALIFY: names are acceptable where a rename can only fail closed (labels, Project, Status option: no match means no launch). They are not acceptable where reuse fails open: an approver's login can be recycled, so approvers are matched by account ID (C §3). The own login stays a login, because the claim itself assigns by `@me` login.
- **A-004** QUALIFY: accepted as a v1 boundary only if it is enforced as opt-in (A OD-2 `enabled: false`) and the audit line carries `host` (D NFR-006). A shared ledger stays a B revisit condition behind `DispatchStore`.
- **A-005** ACCEPT, and state it explicitly: the claim refuses a foreign assignee (`claim.md:41-42`), so assign-before-approve is the setup rule. An approved but unassigned issue is reported under its own skip reason, `unassigned` (D FR-008), so it is visible rather than silently waiting.
- **A-006** QUALIFY: store UTC timestamps. If `now` is earlier than an entry's `updated_at` (the clock went backwards), treat leases as unexpired and back-offs as not elapsed. That means fail closed with an audit reason `clock_skew`, and a fake-clock test covers it.
- **A-007** QUALIFY: `flock` holds only on a local filesystem for one host. The spec states that `state_dir` must be local, and the lock test runs two real processes (C §8 "concurrent invocations").
- **A-008** QUALIFY: the `labeled` actor counts as a human decision only after the bot exclusion (A §3: `type` `Bot` or a `[bot]` login) and an allow-list match by account ID. A human-run automation typed `User` is a residual risk owned by whoever admits accounts to the allow-list (D T3).
- **A-009** QUALIFY: A does not rely on the marker for `launched`, because A never relaunches it (§7). With concession 1, the orphaned `pending` no longer relies on it either. The lease then only bounds when a `launched` entry is reported as `launched_unclaimed`, so a wrong lease length causes noise, not duplicates.
- **A-010** QUALIFY: the allow-list is trusted only if the file is owned by the running user with mode 0600 or 0644 and is not writable by group or others. `check-config` and `once` check this and exit 2 otherwise (in the style of D NFR-011's file modes).

## Per-point positions

| Point | Level | Superior variant | Confidence % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | HYBRID (A/D) | 55 | Each requirement should carry an acceptance line and a test (A Given/Then, D *GWT*/*Test*); C's prose has no argv to test against |
| S-002 | L1 | NONE | 60 | Requirement counts are not a quality signal on their own |
| S-003 | L2 | HYBRID (A+D) | 60 | A's stage protocols (§1, §8) for the developer, D's runbook and SLOs (§8) for the operator |
| S-004 | L2 | A | 70 | `config`, `routing` and `audit` as separate modules (§8) give each extension point one home; merge `approval` into predicates (concession 10) |
| S-005 | L3 | A | 55 | One JSON per login (§7) isolates logins; add C's init and missing-store rule; C's SQLite fits behind `DispatchStore` as a second backend |
| S-006 | L1 | NONE | 60 | Numbered decision IDs (A, B, D) are easier to trace than C's unnumbered table; this is cosmetic |
| S-007 | L1 | B | 55 | B's RD-F / SB / RR codes trace each claim to a source most directly |
| S-008 | L1 | NONE | 50 | B adds likelihood and impact, but every register covers the same core risks |
| C-001 | L3 | A | 60 | Distinct `watch:ready` and `watch:approved` names (OD-4); a rename fails closed (A-003) |
| C-002 | L3 | HYBRID | 75 | A's bot exclusion, B's complete paged events, C's account IDs and fail-on-incomplete-history |
| C-003 | L3 | E | 70 | E's per-issue `projectItems` lookup avoids A's 100-item truncation voiding the predicate for the whole cycle |
| C-004 | L3 | A | 60 | A's routing table keeps the default rule and leaves room for other rules; C's sole-assignee rule is stricter than the claim |
| C-005 | L3 | HYBRID (A+D) | 65 | A's `enabled: false` default (OD-2) plus D's audited `host` (OD-8) |
| C-006 | L3 | E | 65 | E drops untagged and unowned issues before any per-candidate call, which bounds the call count |
| C-007 | L3 | D | 65 | D's separate `attempts` and `launches` counters (concession 3), on top of A's six states and history |
| C-008 | L3 | HYBRID | 55 | A's numbers, plus B's subprocess timeouts and E's failed back-off |
| C-009 | L3 | C | 60 | C commits `unknown` before any I/O, which removes A's orphaned-`pending` window (X-002) |
| C-010 | L2 | HYBRID | 70 | A/D's fixed 12-element argv with `--agent claude`, plus B's binary probe and C's origin check |
| C-011 | L3 | D | 70 | An unknown outcome whose lease expires becomes `abandoned`, never `failed` that could be retried |
| C-012 | L3 | HYBRID (A+D) | 60 | A's int-not-bool range check plus D's property test |
| C-013 | L3 | HYBRID | 60 | A's local list where an empty list approves nothing, keyed by C's account IDs; not D's template-shipped file |
| C-014 | L2 | B | 65 | B gates enabling on Q6 and requires written owner acceptance of skipped permissions (OD-8) |
| C-015 | L3 | A | 60 | A voids a whole-cycle predicate on any unreadable shared input; scope it per issue only where the read is per issue (E) |
| C-016 | L3 | HYBRID (A+C) | 55 | A's exit 5 with no state change and its 3+3N budget, plus C's persisted next-permitted time |
| C-017 | L2 | D | 60 | D's XDG path, 24 h shadow dry run and staleness threshold make rollout observable |
| C-018 | L3 | HYBRID | 60 | Held lock exits 0 (A/B), plus D/E's `DISABLED` kill-switch file |
| C-019 | L2 | D | 60 | D's `audit.jsonl` with `host`, `rate_remaining` and rotation, plus A's closed skip-reason enum |
| C-020 | L2 | A | 60 | `once`, `status` and `check-config` cover the operations without B's flag sprawl; recovery via `--retry-launch` |
| C-021 | L2 | A | 70 | JSON config fits `requires-python >=3.10` (`pyproject.toml:16`); B has no persistent config |
| C-022 | L2 | HYBRID | 65 | A's AST `test_no_shell` and stub e2e, D's crash injection, C's concurrent processes, E's `test_no_text` |
| C-023 | L2 | A | 55 | A's F-1..F-7 name the extension verbs (`release <N>`) and the option-D path |
| C-024 | L3 | A | 55 | The marker comment is the claim's own evidence; assignment alone is not proof (C agrees) |
| C-025 | L2 | HYBRID (A/D) | 55 | A requests no text at all; D's `PWNED-TITLE` fixture proves it |
| X-001 | L3 | A | 60 | A's position is the one consistent with D2 claim-only and the fixed seed contract |
| X-002 | L3 | D | 70 | An orphaned `pending` must not relaunch; A adopts `abandoned` `pending_orphan` (concession 1) |
| X-003 | L3 | A | 70 | Corrupt record gives exit 6 and no launch (§7); B's empty reset re-opens every issue |
| X-004 | L3 | C | 70 | A timeout is `unknown`, never `failed` (concession 2) |
| X-005 | L3 | D | 70 | Fail closed with no label-only mode; A drops Project mode `off` (concession 4) |
| X-006 | L3 | HYBRID (A+C) | 60 | Stop with no state change (A NFR-006) and persist the next-permitted time (C NFR-004) |
| X-007 | L2 | HYBRID | 55 | One exit-code table for all variants: lock 0, unreadable Project 4, rate limit 5, with D's action column |
| X-008 | L2 | A | 75 | A keeps the seed argv `--agent claude` exactly; E's `--agent <agent>` widens the fixed contract |
