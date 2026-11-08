# Adversarial Debate Transcript

## Metadata

- Depth: deep
- Rounds completed: 3 (Round 1 parallel statements; Round 2 sequential rebuttals A to E; Round 2.5 invariant probe; Round 3 final arguments, run in parallel, see Deviations)
- Convergence achieved: 98% (50 of 51 diff points resolved; see Convergence Assessment)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 5 (blind: variants A to E; model identities withheld from all debate files)
- Diff points: 41 S/C/X points plus 10 shared assumptions (A-NNN) = 51; taxonomy levels L1 5, L2 14, L3 32 (all three levels covered in every round)
- Deviations: Round 3 advocates ran in parallel, not sequentially (each answered a fixed list of fault-finder findings and the four open points); the per-point agreement counts and the round tallies were computed by the orchestrator with awk from the advocates' tables; Round 2 and 3 files are included below verbatim.

## Round 1: Advocate Statements

### Variant A Advocate

#### Round 1: Advocate for Variant A (persona: architect)

Focus: maintainability and extension seams. Section references (§N) are to each variant's own sections; diff IDs are from `diff-analysis.md`.

##### Position summary

Variant A should be the structural base of the final spec: it is the only variant that turns each open decision and each documented alternative into a one-module swap behind a named seam (§1, §8 module table, NFR-011), and it has the most offline-checkable configuration surface (`check-config`, JSON config, `enabled` defaulting to false). Its dispatch-record recovery rules are not the best, though: on a crash-orphaned `pending` (X-002) and on a launch timeout (X-004) A can launch twice. The final spec should take C's and D's ambiguity handling and put it into A's `record.py`.

##### Steelman per opposing variant

**B (root-cause analyst).** Strongest form: every requirement traces to one of three root causes (§1.1 RC1-RC3), so nothing is decorative. It is the only variant that fails approval closed on a truncated event history (FR-008 `approval-unverifiable`). It guards against the GNOME `orca` screen reader by probing for the `orca-cli` topic (FR-014, T7). It keeps the approval evidence (`approver`, `approval_event_id`) and `launch_cwd` in the record (§7.2), and it refuses to let label toggling reset attempts (OD-6). Its `FakeRunner` exits 99 on any unscripted call, and its `_assumed_shape` fixtures (§4, §8.3) are the most honest way to test against JSON shapes nobody has verified. It is also the clearest about what must happen before enablement (OD-8: no cron before Q6).

**C (readiness scorer).** Strongest form: it is the most rigorous about identity. Node and account IDs instead of names (§3, §7) close the rename-and-reuse attacks that every name-keyed variant leaves open. It is also the most rigorous about at-most-once: "Consuming the slot and entering `unknown` is one durable transaction before external I/O. Expiry never releases a consumed slot" (§7). That is the only rule that makes NFR-002 true under every crash point. It refuses silent reinitialization ("recreating an empty ledger could duplicate every claim", §10). It persists a rate-limit next-permitted-request time (NFR-004). And it says plainly that a successful launch is not a successful claim (§1, FR-012).

**D (operations).** Strongest form: it is the only variant an operator could run on day one. It has an exit-code table with an action for each code (§8), a 24 h shadow dry-run rollout, a `DISABLED` kill switch (FR-018), a staleness signal (`last_cycle_age_seconds` > 900) and SLOs that can be computed from its own logs (NFR-013). Its separate `attempts` and `launches` counters (§7 schema) state the at-most-once invariant as one checkable inequality (`launches < max_launches`). An orphaned `pending` goes to `abandoned` (`pending_orphan`) and an expired `unknown` goes to `abandoned`, so no path leads to a second launch.

**E (cost-to-serve).** Strongest form: its call budget is worked out from first principles (§5), and it reads Project membership from each issue's own `projectItems` (FR-008). That makes cost scale with the number of candidates rather than the Project's size, and it removes the "Project over 100 items always fails closed" trap (D R3) that A and D both fall into. It drops unowned candidates before any per-candidate call (FR-004), has a hard call cap (NFR-005), bounds state growth (NFR-013), and states the cost asymmetry that justifies resolving ambiguity toward not launching (§7, "Cost rationale").

##### Strengths claimed (variant A)

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

##### Weaknesses identified in others

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

##### Concessions

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

##### Shared-assumption responses

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

##### Per-point positions

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

### Variant B Advocate

#### Round 1 Advocate: Variant B (analyzer persona)

##### Position summary

Variant B is the best base for the selection and evidence layer: it derives every mechanism from three named root causes (B §1.1 RC1-RC3), proves approval from the complete event history with fail-closed truncation (B §3, FR-007, FR-008), resolves Orca the way this repo already does (FR-014), and records who approved each launch (FR-020). Its dispatch-record recovery rules are wrong in three places (X-001, X-003, X-006), and the final spec should take those rules from D and E instead.

##### Steelman per opposing variant

**A (pipeline of stages).** Strongest form: every open decision and every alternative (B, C, D) replaces one module behind a typed protocol (A §1, §8, NFR-011), so the spec survives decision changes without a rewrite. A gets right: a bot check on the approver (A §3 "type `Bot` or login ending `[bot]`"); a corrupt record fails closed with exit 6 (A §7); rate limits end the cycle with no state change (NFR-006); a per-login state directory so a changed login inherits nothing (A §7 "Location"); `enabled` defaults to false (OD-2), which turns the same-login rule into a guard rather than a note; the JSON config choice is grounded in Python 3.10 support (OD-9).

**C (readiness and strict identity).** Strongest form: identity is anchored to GitHub node and account IDs (C §3, §7), so renames of labels, approvers, owners or Project fields cannot silently change eligibility, and one durable transaction consumes the launch slot before any external call (C §7), giving the strictest at-most-once guarantee of all five. C gets right: "recreating an empty ledger could duplicate every claim" (C §10), a missing initialized store is an error, not a fresh start (NFR-003), and deployment stays disabled until the narrative-read risk is accepted (C §6).

**D (operations).** Strongest form: D is the only variant an operator could run on day one: an exit-code table with an action per code (D §8), a `DISABLED` kill switch (FR-018), a 24-hour shadow dry-run (D §8 runbook step 3), staleness detection (`last_cycle_age_seconds` above 900), and SLOs computable from the audit log (NFR-013). D's record has separate `attempts` and `launches` counters (D §7 Schema), which is the cleanest way to express "a session may exist, so never a fresh launch".

**E (cost).** Strongest form: cost scales with candidates, never with the size of the Project (E §5), because Project membership comes from each issue's own `projectItems` (FR-008); this removes the 100-item ceiling that A, B and D all hit. E drops unowned candidates before any per-candidate call (FR-004), caps launches per day (FR-018), and states the bias explicitly: "every ambiguous state resolves toward not launching" (E §7).

##### Strengths claimed

1. **Design traced to root causes, not features.** B §1.1 names three missing mechanisms (no ready signal, claim routes to whoever runs it, no at-most-once start), each with evidence (RD-F7, `refs/claim.md:41-42`, RD-F4) and a design consequence. Every later section maps back to one of them, so a reviewer can check that nothing is built without a cause. I re-checked the RC2 citation: `refs/claim.md:41` stops on an issue "assigned to anyone other than the current login" and line 42 allows a re-claim by the same login, so "assigned to own login only" (B OD-1) is the only routing rule the claim cannot refuse.
2. **Approval is proven from complete evidence, and fails closed when it is incomplete.** B §3 requires "the latest `labeled`/`unlabeled` event for that label" over "the complete REST event list", and FR-008 rejects the issue as `approval-unverifiable` when the page cap is reached. This is the root cause of a subtle defect in A, D and E: the issue-events endpoint is paged, and an issue with a long history needs every page to find the latest event (event order and page size should be confirmed in the live test). E FR-006 specifies "one ... call per examined candidate" and NFR-005 caps calls at 35, which cannot read a multi-page history; A and D are silent on paging. Only B and C (C §3 "incomplete event history ... fails approval") close this.
3. **Orca resolution reuses tested repo code.** B FR-014 probes `orca-ide` then `orca` and accepts only the `orca-cli` topic, because `orca` may be the GNOME screen reader (T7). This is not invented: `src/superclaude/cli/install_user_setup.py:198-221` (`_find_orca`) does exactly this with `_ORCA_CLIS = ("orca-ide", "orca")` (line 35). A, D and E hard-code `"orca"` as argv[0] (A FR-012, D FR-013), which on a Linux host can execute the screen reader. The diff rates this High (U-004).
4. **Accountability for every launch.** B FR-020 writes one line per decision with `approver` and `approval_event_id`, and the record stores both (B §7.2). After an unwanted session, the question "who approved this?" is answered from the local log without another GitHub call. A, D and E log cycle counts; only E stores `approval_actor` (E §7), and none store the event id that makes the evidence checkable.
5. **The cap cannot be bypassed by toggling labels.** B OD-6: a newer approval is reported `re-approved` and "does not reset `attempts`", because resetting "lets label toggling bypass the attempt cap" (U-005). No other variant states this.
6. **Correct split of fail-closed scope.** B NFR-009: a per-issue read error skips that issue; a login or discovery error ends the cycle (exit 2); a record-save error aborts (exit 1). This matches the cause of each failure: a 404 on one issue's events says nothing about other issues, while a failed login read invalidates every routing decision. A §3 voids the Project predicate for the whole cycle, and D NFR-007 makes any read failure yield zero launches, so one deleted issue stops all dispatch.
7. **Strictest reading of D1-D3 and the repo pin.** B NG1 forbids any GitHub write and gives the reason (a second writer without compare-and-set is unsafe, RD-F4); NFR-001 asserts it over every recorded argv; FR-002 checks the worktree `origin` before any call, so a SuperClaude-Org checkout cannot even start a cycle. The argv keeps the seed's fixed `--agent claude` (FR-012), unlike E FR-014.
8. **Test fixtures mark what is unverified.** B §8.3: fixtures for `project item-list` and the Orca reply carry `_assumed_shape` naming Q8 or Q2, and `FakeRunner` exits 99 on any unscripted call (U-006). When the live test reveals the real JSON, the fixtures to update are found by grep, and an unexpected extra call fails loudly instead of returning a silent default.
8a. **Text never enters Python.** B NFR-002: `--json` lists exclude text and marker detection uses `--jq` inside `gh`, tested with a hostile title. C §6 by contrast lets the marker check "inspect bounded comment content" in the process.

##### Weaknesses identified in others

- **A: two retry paths can start a second session (X-002, X-004).** A §7 turns a `pending` entry with no marker into `failed` (`lost_reply`), and `failed` is retryable after the lease. But a crash between the record write and the Orca reply is exactly the case where Orca may have started the session: the root cause of RC3 (no at-most-once start) is reintroduced by the recovery path. The same holds for `unknown` becoming `failed` on lease expiry (A FR-014, §7): a timeout says nothing about whether the session exists. Because the claim posts its marker only in Wave 6 (`refs/claim.md` Waves 0-6), "no marker yet" is not evidence of "no session".
- **A, D: discovery capped at 100 items.** A FR-003 (`gh issue list -L 100`) and D's Project read hit a fixed ceiling; D R3 states that a Project over 100 items "always fails", so a growing Project silently becomes a permanent outage. E FR-008 removes the ceiling at the cause by asking each candidate for its own `projectItems`.
- **E: GraphQL conflicts with the read-only checks of A, B and D.** `gh api graphql` sends a POST, so a rule "every gh call is a GET" (A FR-002, D NFR-002, B NFR-001) rejects E's FR-008. The merged spec must define read-only as "no REST write verb and no GraphQL `mutation`", and test that the query string contains no mutation.
- **E: widens the fixed launch contract.** E FR-014 makes `--agent <agent>` configurable, which the seed argv fixes to `claude` (X-008). E FR-012 leaves the record of a removed issue "deleted or marked abandoned", an undecided state transition.
- **C: heavy for the risk it removes.** SQLite, an append-only transition table and an `init-state` verb (C §7, §8) add a schema migration surface to a 5-minute poller whose record holds a few entries. C §6 lets the marker check read bounded comment content in Python, which conflicts with C's own minimization aim (C-025).
- **D: an unenforceable default.** D OD-7 relies on the launched session's "default interactive mode", but the seed argv has no permission flag, so the poller cannot ensure it; the session inherits whatever the workspace sets (C-014).
- **A, D: fail-closed scope too wide (C-015).** One unreadable issue voids the whole cycle (A §3, D NFR-007); the failure's cause is local, so its effect should be local.

##### Concessions

1. **X-001, B is wrong.** B §7.3 relaunches `launched` and `failed` entries after the lease when no marker is seen. B §7.4 itself marks the lease length an ASSUMPTION, and `refs/claim.md` posts the marker last. A slow claim therefore gets a second session. Adopt D/E: `launched` with no marker after the lease becomes `abandoned` (`claim_not_observed`), reported, never relaunched.
2. **X-003, B is wrong.** NFR-010 loads a corrupt file as empty. Every issue launched but not yet marked becomes eligible again. Adopt A/D: unparseable or unknown version gives a nonzero exit (D NFR-011), no launch, no reset, operator repair.
3. **X-006, B is wrong.** R9 treats the 5-minute cadence as back-off; a 403/429 mid-cycle then drives more per-issue reads into the limit. Adopt A/D/E: stop the cycle, exit nonzero, change no state. C's persisted next-permitted time is a reasonable addition.
4. **X-005, drop `--label-only`.** It removes two of the issue's own eligibility conditions. Prefer C/D fail closed, and use E's per-issue `projectItems` as the Project check in place of B's Project-as-discovery (C-003).
5. **Bot check missing.** B §3 accepts any allow-listed actor. Add A/D/E's check: `actor.type == "User"` and no `[bot]` login.
6. **Operations surface too thin.** B's single `once` verb and exits 0-3 (FR-021) cannot distinguish lock, rate limit, truncation and corrupt state. Take D's exit table with operator actions, add a `status` verb and D's `DISABLED` kill switch.
7. **Configuration as flags only (C-021).** A cron line with a dozen flags is fragile; A's JSON config (Python 3.10, OD-9) is better.

##### Shared-assumption responses

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

##### Per-point positions

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

### Variant C Advocate

#### Round 1 — Advocate C (backend)

##### Position summary

C provides the strongest data-integrity contract: consume a durable dispatch slot before external submission, never release it on lease expiry, and distinguish session acceptance from posted claim evidence (C §§1, 4 FR-010–012, 7). Keep that core, but merge B's concrete adapter verification, D's operational controls, and E's candidate-scaled discovery without importing their replay paths (B §4 FR-014; D §8; E §4 FR-008).

##### Steelman per opposing variant

- **A:** Its strongest form is a comprehensible, replaceable pipeline with explicit command allowlisting, testable acceptance criteria, offline inspection, and corrupt-record rejection (A §§1, 4 FR-019–020, 5 NFR-003, 7–8). Those are real implementation aids; stage isolation need not mean adopting A's expired-pending retry rule (A §7).
- **B:** Its strongest form connects root causes to mechanisms, verifies worktree origin and executable identity, preserves retry working directory, and explicitly marks unverified fixtures (B §§1.1, 4 FR-002/014/016, 8.3). Its timeout-without-ID handling and non-resetting reapproval counter correctly recognize ambiguity and abuse risks (B §7.3, §10 OD-6).
- **D:** Its strongest form treats unattended polling as an operated batch job: kill switch, offline status/staleness, private state permissions, exit-code actions, and shadow rollout (D §4 FR-018/021, §5 NFR-011, §8). Orphaned pending records deliberately sacrifice availability rather than risk duplicate starts (D §7).
- **E:** Its strongest form bounds both expensive sessions and API work, filters locally before per-issue requests, and avoids whole-Project discovery through issue-local membership queries (E §4 FR-004/008/018, §5). It correctly states that missed dispatch is cheaper than duplicate launch and treats unknown outcomes conservatively (E §7).

##### Strengths claimed

1. **A genuine submission invariant.** C commits consumed-slot plus `unknown` before I/O, then forbids ordinary resubmission even after expiry or explicit post-consumption failure. That covers the crash-after-submit/before-reply gap without assuming when a marker arrives (C §7; §5 NFR-002). This is at-most-once submission, not exactly-once execution.
2. **Stable identity throughout the contract.** Repository/issue node IDs anchor uniqueness; account IDs anchor owner and approver identity; label, field, and option IDs anchor policy. Renaming a login or moving worktrees cannot silently create another dispatch key (C §§3, 7). C explicitly acknowledges independent ledgers and cloned backups invalidate this boundary (C §11).
3. **Selection evidence is refreshed, not inferred.** C refreshes ownership, approval provenance, and Project evidence, rejects incomplete evidence, excludes PRs/drafts/archived items, and admits the unavoidable refresh-to-launch race (C §3; §4 FR-006/008). Other variants' issue-only refresh does not prove the Project is still Backlog (A FR-010; D FR-011; E FR-012, all §4).
4. **Data loss is not interpreted as permission.** C requires explicit initialization and rejects corrupt or missing-after-initialization state; transitions and slot consumption share a transaction (C §5 NFR-003; §7). The permanent-suppression trade-off is written down rather than hidden behind a retry counter (C §7).
5. **Operational truth is preserved.** Accepted launch, unknown launch, and recognized posted claim are separate outcomes; assignment alone proves none of them (C §§1, 4 FR-011/012). Backoff survives process exit, and deployment remains blocked until narrative-read risk and permissions are addressed (C §5 NFR-004; §6).

##### Weaknesses identified in others

1. **A's lost-reply path reopens the critical window.** Expired `pending` without a marker becomes retryable `failed`; expired `unknown` can also become `failed`. Neither proves a session did not start, so another ordinary submission is possible (A §7 transitions). This cannot support a lifetime at-most-once claim.
2. **B explicitly chooses weaker semantics.** A `launched` issue can launch again after its lease; orphaned `pending` becomes `launched` and inherits that route (B §7.3). Its corrupt-state-as-empty rule also destroys pre-marker exclusion (B §5 NFR-010). These are substantive integrity differences, not notation preferences.
3. **D's success counter is not a submission counter.** `launches` increments on success or recognized unknown, while an “other error” moves to retryable `failed` with zero launches (D §7). Without a complete timeout/malformed-output classification, a possibly started session can follow that retry path. Its recovery instruction to remove an abandoned entry also needs an explicit guarantee-reset warning and evidence checks (D §7).
4. **E's pruning conflicts with durable exclusion.** Removing a 30-day-old `abandoned` record can expose a previously submitted but unmarked issue as new; the claim marker cannot guard an issue whose claim never posted (E §5 NFR-013; §7). “Any other error” becoming `failed` also needs narrowing to proven non-start (E §4 FR-015 versus §7's definition).
5. **Optional Project bypass changes the feature.** A's `off` and B's `--label-only` admit issues without the required Project/Backlog evidence. Explicit opt-in makes degradation visible but does not satisfy the original predicate (A §10 OD-5; B §4 FR-022/§10 OD-5; seed Success Criteria).
6. **Budget certainty exceeds adapter evidence.** E's one-events-call and 33-call arithmetic omit paginated histories; complete approval verification cannot be traded away for a call ceiling (E §4 FR-006; §5). D's observability targets are useful proposals, but SLO success must not obscure unknown submissions or exhausted candidates (D §5 NFR-013; C §5 NFR-005/008).

##### Concessions

- **C is less executable as a contract.** It lacks a literal complete launch/reconciliation argv, a configuration schema, stable decision IDs, and a transition-by-transition test table. Borrow A/B's concrete contracts and D's runbook, without copying retry semantics (C §§4, 7–8, 10 versus A §4 FR-012/015; B §4 FR-014/016; D §8).
- **SQLite is a proposal, not a proof.** C does not specify durability settings, initialization evidence outside the lost store, backup/restore discipline, or how to detect a nonpersistent mount. Losing the whole directory defeats a sentinel stored only there; transactional invariants matter more than storage branding (C §5 NFR-003; §§7, 11). A corrected JSON design could satisfy them.
- **C needs one unambiguous ordering.** FR-008 says refresh before reservation; §7 permits refresh from `pending`. Specify reservation, final refresh, atomic consumed-slot commit, submission; stale reservation may cancel, consumed slot never resets (C §4 FR-008/010; §7). Same-operation retry also needs stored invocation context (B §7.2–3).
- **C's stricter policies impose costs.** Sole assignee, account-ID governance, archived-item exclusion, and permanent consumed keys require owner approval and operator support; no source establishes that one authority is technically enforced (C §§3, 7, 10). Accept the missed-work trade-off only explicitly.
- **C should borrow performance and operations, not overbuild them.** E's issue-local Project strategy and local prefiltering, B's assumed-shape fixtures, and D's disable/staleness controls improve C (E §4 FR-004/008; B §8.3; D §4 FR-018/021). All adapter shapes still need the owner-run validation C §9 requires; no live behavior was verified here.

##### Shared-assumption responses

A-001: QUALIFY — Local storage is acceptable only with verified persistence and controlled restore; a surviving marker does not protect the pre-marker interval (C §§7, 9, 11).

A-002: QUALIFY — Prompt transport remains an unverified deployment prerequisite, not evidence of slash-command execution; require the controlled owner-run test (C §9; seed Enrichment).

A-003: REJECT — Names are not the durable identity contract: C uses account/node IDs and retains logins for display; approved ID mappings must not silently rebind by matching names (C §§3, 7).

A-004: QUALIFY — One nominated authority is an operational boundary, not distributed exclusion; a second independent ledger invalidates at-most-once guarantees (C §§1, 7, 11).

A-005: QUALIFY — Assignment must exist at eligibility evaluation, not necessarily precede the approval event. An unassigned issue waits until assigned; document that human step and rejection reason (C §3; B §10 OD-1).

A-006: QUALIFY — Clock jumps threaten availability, backoff, and fairness, but must never reopen consumed slots. Add jump tests, monotonic in-process deadlines, and a persisted ordering sequence where appropriate (C §5 NFR-004/007; §7: “Expiry never releases a consumed slot”).

A-007: QUALIFY — Validate locking and transaction behavior on the selected persistent local filesystem; no cross-host guarantee follows from a local lock (C §§7, 11).

A-008: QUALIFY — Actor metadata establishes who applied the label, not their actual decision process. Administratively verify human accounts and approval procedure; a `User`-typed automation account remains a residual (C §3; D §6 T3).

A-009: REJECT — A 60-minute marker deadline is not required for exclusion in C, nor for confirmed `launched` entries in A/D/E: expiry does not authorize their fresh launch. B's lease retry does depend on timely evidence, and A's orphan path is unsafe (C §7; A §7; B §7.3; D §7; E §7).

A-010: QUALIFY — Configuration writers must be explicitly trusted administrators, not necessarily only the workspace owner; enforce protected ownership/permissions and govern updates. C names trusted configuration but leaves these mechanics underspecified (C §§3, 6; D §6 T2).

##### Per-point positions

Levels reproduce the diff analysis; confidence concerns the comparative judgment, not production readiness. HYBRID identifies an explicit combination, not a blanket endorsement.

| Point | Level | Superior variant | Confidence % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | NONE | 95 | Every style supplies acceptance criteria; notation alone proves no contract advantage (§§4–5, all variants). |
| S-002 | L1 | NONE | 99 | More numbered requirements do not establish coverage or consistency (§§4–5, all). |
| S-003 | L2 | HYBRID | 93 | B §1.1 explains causes; D §8 supplies operation; E §5 supplies cost; C §2 preserves revisit boundaries. |
| S-004 | L2 | C | 85 | C §8 separates effects, selection, and transactional storage without A §8's speculative replacement interfaces. |
| S-005 | L3 | C | 96 | C §7 couples slot and transition transactionally; initialization/corruption protections require further mechanics. |
| S-006 | L1 | B | 85 | B §10's decision IDs support precise sign-off; C's unnumbered decisions are harder to reference. |
| S-007 | L1 | HYBRID | 88 | C §12 distinguishes proposals from facts; B §12 adds recognizable source identifiers. |
| S-008 | L1 | B | 88 | B §11 provides risk IDs plus impact/mitigation; C §11 is prose, despite the diff calling it a table. |
| C-001 | L3 | C | 95 | C §3 pins label ID, while still proposing display names; name-only equality is weaker identity. |
| C-002 | L3 | C | 96 | C §3 requires trusted account ID, non-bot metadata, and complete history; intent remains administrative. |
| C-003 | L3 | HYBRID | 96 | Combine C §3's field/option identity and exclusions with E §4 FR-008's issue-local Project reads. |
| C-004 | L3 | C | 96 | C §3 anchors sole ownership to account ID and explicitly states its stricter-than-claim policy. |
| C-005 | L3 | HYBRID | 94 | C §7 states unsupported independent authorities; A §10 OD-2 adds disabled-by-default setup protection. |
| C-006 | L3 | HYBRID | 95 | E §4 FR-004 prefilters cheaply; C FR-006 requires complete evidence, not a permanent Project-size ceiling. |
| C-007 | L3 | C | 99 | C §7 makes consumed intent durable before I/O rather than inferring it from reply counters. |
| C-008 | L3 | C | 95 | C §7 separates safe pre-submission attempts from one ordinary submission; numerical defaults remain proposals. |
| C-009 | L3 | C | 98 | C FR-008/010 and §7 preserve final refresh plus atomic consumption; clarify reservation ordering. |
| C-010 | L2 | HYBRID | 96 | A FR-012 supplies fixed argv; B FR-002/014 verifies origin and executable; C needs both (§4). |
| C-011 | L3 | C | 99 | C FR-011 and §7 classify malformed/timeout as unknown; absent ID never licenses fresh retry. |
| C-012 | L3 | HYBRID | 97 | A FR-011 supplies explicit type/range cases; D NFR-001 adds property tests; C §10 fixes the range. |
| C-013 | L3 | C | 94 | C §§3/10 uses trusted account IDs and admission checks; add protected-update mechanics. |
| C-014 | L2 | HYBRID | 97 | C §6 gates narrative-risk acceptance and policy verification; B §10 OD-8 requires explicit bypass-risk acceptance. |
| C-015 | L3 | C | 95 | C NFR-006 separates global integrity/auth failures from candidate-local malformed evidence (§5). |
| C-016 | L3 | HYBRID | 96 | C NFR-004 persists retry timing; E NFR-005 provides a hard call cap; pagination must count (§5). |
| C-017 | L2 | HYBRID | 94 | C §9 checks persistence/shutdown; D §8 adds shadow rollout and observable staleness. |
| C-018 | L3 | HYBRID | 96 | C §7's integrity boundary plus D FR-018's disable-before-effects control is stronger than either alone. |
| C-019 | L2 | HYBRID | 96 | C NFR-005 gives candidate transitions; A NFR-007 closes reasons; D NFR-006 adds runtime context (§5). |
| C-020 | L2 | HYBRID | 94 | Keep C §8's explicit initialization/inspection and D §8's operator actions; avoid unguarded reset semantics. |
| C-021 | L2 | HYBRID | 90 | A §8 JSON configuration plus C §10's ID/authority policy needs one explicit validated schema. |
| C-022 | L2 | HYBRID | 98 | C §8 covers concurrency/rename; B §8.3 marks assumed shapes; E §8 adds repeated-cycle checks. |
| C-023 | L2 | HYBRID | 94 | B §9 validates launch contracts; C §9 checks lifecycle; D §9 adds operational follow-through. |
| C-024 | L3 | C | 96 | C FR-012 distinguishes recognized posted evidence from assignment; §11 denies full-artifact completion proof. |
| C-025 | L2 | HYBRID | 95 | C §6 admits necessary marker inspection; D §3 projects a boolean, minimizing narrative retention. |
| X-001 | L3 | C | 99 | C §7 never releases consumed slots; B §7.3 explicitly relaunches accepted sessions after lease. |
| X-002 | L3 | C | 99 | C §7 separates unconsumed reservation from durable consumed intent; A's lost-reply retry lacks that proof. |
| X-003 | L3 | HYBRID | 99 | C NFR-003, A §7, D NFR-011 reject corruption; B NFR-010 silently resets exclusion (§5). |
| X-004 | L3 | C | 99 | C FR-011 treats timeout/malformed reply as unknown and keeps the slot consumed (§4/§7). |
| X-005 | L3 | HYBRID | 99 | C FR-006, D OD-4, E O-3 refuse Project-free eligibility; A/B's bypasses change the predicate. |
| X-006 | L3 | C | 97 | C NFR-004 honors persisted retry timing across cycles instead of treating five minutes as universal backoff. |
| X-007 | L2 | HYBRID | 92 | C §8 separates unknown-launch attention; D §8 ties codes to actions; choose one mapping, not both. |
| X-008 | L2 | HYBRID | 97 | Preserve all D1–D3; A/B/D §4 fix the agent; C §6 correctly separates marker reads from prompt content. |


### Variant D Advocate

#### Round 1 Advocate: Variant D (devops: deployment, observability, runbooks, SLOs)

##### Position summary

Variant D should be the operational backbone of the final spec. It is the only variant that specifies how the poller is rolled out (24 h shadow dry-run), stopped (`DISABLED`), watched (staleness, SLOs reduced from local files) and recovered (exit-code action table, runbook), and its dispatch record resolves every ambiguous state toward "do not launch again" (§7). It is weaker than E on Project reads, weaker than B and C on launch timeouts and binary identity, and weaker than C on identity by node or account ID. The final spec should graft those pieces onto D rather than replace it.

##### Steelman per opposing variant

**Variant A (strongest form).** A treats the watcher as a pipeline of replaceable stages behind typed protocols, enforced by an import test (§1, §8, NFR-011), so options B, C or D later replace one module, not the cycle. It is the most careful about configuration: a JSON config file because `tomllib` needs Python 3.11 while the package supports 3.10 (OD-9); `check-config` rejecting a lease under 15 minutes (§7); and `enabled` defaulting to `false`, so a second workspace on the same login is safe unless someone opts in (OD-2). That opt-in default is better deployment hygiene than D's kill switch alone. Its approval check excludes bots both by `type` and by a `[bot]` login suffix (§3). Its rate-limit handling ends the cycle with no state change and a distinct exit 5 (NFR-006), which gives alerting a clean signal.

**Variant B (strongest form).** B grounds every mechanism in a root cause (RC1-RC3, §1.1). It has the best binary safety: it probes `orca-ide` then `orca` and accepts only the `orca-cli` topic, because GNOME `orca` is a screen reader (FR-014, T7). It also verifies that the worktree `origin` is IronClaude before any call (FR-002). Its per-decision audit line carries `approver` and `approval_event_id` (FR-020), the best forensic trail for "who approved this launch". It maps a launch timeout to `unknown` (FR-015), the correct reading of an ambiguous reply. It refuses to enable cron before the live test answers Q6 on permissions (OD-8). Its test kit is the most hardened: `FakeRunner` exits 99 on any unscripted call, and fixtures carry `_assumed_shape` to mark unverified JSON (§8.3).

**Variant C (strongest form).** C is the most rigorous on correctness. Identity is anchored on node and account IDs, which survive renames (§3, §7). The launch slot is consumed and `unknown` committed in one transaction before any external I/O, so no crash point can give a second submission (§7). Missing initialized storage is rejected instead of being silently recreated (NFR-003, §10 "State loss"). Rate limits persist a next-permitted-request time tested with a fake clock (NFR-004). Deployment stays disabled until the narrative-read risk and the session permission policy are accepted (§6). It says honestly that a crash after commit can permanently suppress an issue and accepts that cost (§7).

**Variant E (strongest form).** E has the right cost model. It reads Project membership from each issue's own `projectItems`, so cost scales with candidates rather than Project size, and a Project with more than 100 items still works (FR-008, §5, U-014). It drops untagged and unowned issues before any per-candidate call (FR-004). It enforces a hard per-cycle call cap of 35 (NFR-005) and a daily launch cap of 6 (FR-018), which bounds spend whatever the approval volume. It gives the operator a `reset <N>` verb (FR-023) instead of hand-editing state, and it prunes terminal records after 30 days (NFR-013). Its kill switch matches D's (FR-022).

##### Strengths claimed

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

##### Weaknesses identified in others

1. **A can launch twice after a crash or timeout.** In §7, a `pending` entry found at cycle start becomes "`failed` (`lost_reply`)", and `failed` is retryable after the lease. A crash after the session started therefore gets a second session. The same holds for "`unknown` | ... lease expired | `failed`" (X-002, X-004). FR-018's lock "exits 0 with `outcome=locked`" also hides hung cycles from any exit-code alert.
2. **B relaunches a session that may be running.** §7.3 says "`launched`, `failed` | lease expired ... no marker, attempts left | new launch" (X-001), and "A `pending` entry at cycle start is treated as `launched`" feeds that same path. NFR-010 resets a corrupt file to empty (X-003). R9 has no rate-limit handling, and its 42-call cycle keeps calling into a 403 (X-006). `--label-only` (FR-022) defines a mode that drops two of the issue's own definitions (X-005). With a single verb and "No other verb" (§8.2), the operator has no `status` to inspect state.
3. **C is not testable as written for operations.** Its acceptance criteria are prose ("configuration failure is returned", FR-001) and give no argv, so an implementer must invent the contract (C-010). It has no kill switch, no default state path ("operator-configured", §7) and no runbook steps. Node-ID configuration for labels, Project field and option (§3, §10) makes setup much harder, and C gives no lookup procedure. Its marker check "may inspect bounded comment content" (§6), which brings comment text into the process, against the A/D/E minimization (C-025).
4. **E widens the fixed launch contract and leaves its re-read undecided.** `--agent <agent>` (FR-014) departs from the seed's `--agent claude` (X-008). FR-012 says the record is "deleted or marked `abandoned`", which is not testable as one outcome. A corrupt record is not specified (X-003). The worker-environment refusal rests on an ASSUMPTION that such a marker exists (§6). `~/.superclaude/` is not an XDG state path, so it mixes with installed framework files.
5. **Exit-code drift across all five (X-007).** A lock gives 0, 0, 6, 75 and 5, and a rate limit gives 5, none, 3, 3 and 8. Only D attaches an operator action to each code. The final spec needs one table, not five.

##### Concessions

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

##### Shared-assumption responses

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

##### Per-point positions

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

### Variant E Advocate

#### Round 1 advocate: variant E (performance, bottlenecks, scaling, cost-to-serve)

Section references: "E §n" is variant E's own section; "A §n" etc. likewise. Point IDs are from the diff analysis.

##### Position summary

Variant E is the only variant that treats cost as a first-class requirement. It prices the idle cycle (2 calls), the worst cycle (33 calls), the hourly share of the allowance (0.48 and 7.9 percent, E §5) and the expensive event (a launched session, bounded per cycle and per day, E FR-018). Its one structural choice that changes how the system scales is the per-issue `projectItems` query (E FR-008), which makes cost track candidates instead of Project size. On crash recovery, record integrity and pagination, E is weaker than C and D, and the final spec should take those parts from them.

##### Steelman per opposing variant

**Variant A (stages behind typed protocols).** Strongest form: every open decision and every alternative (B, C, D) replaces one module, not the cycle (A §1, §8, NFR-011), and the record is keyed by login so a changed login inherits nothing (A §7). It has the cleanest transition table, with an explicit `attempts -= 1` on a cancelled reservation (A §7), a closed skip-reason enum (A NFR-007), `enabled` defaulting to false so a second workspace on the same login must opt in (A OD-2), and a JSON config chosen because `tomllib` needs Python 3.11 (A OD-9, U-002). Its call bound `3 + 3N` equals E's (A NFR-005). What A gets right that E does not: a mechanical guard against same-login double polling, and a precise cancel transition.

**Variant B (root cause plus Project-first discovery).** Strongest form: three root causes RC1-RC3 (B §1.1) tie each design choice to evidence; discovery is the Project query itself, so "in a Project" and "Backlog" prune the candidate list before any per-issue call (B FR-004); approval reads the complete paged event list and fails closed at the page cap (B FR-007, FR-008); the executable probe that accepts only the `orca-cli` topic handles the GNOME screen-reader name clash (B FR-014, U-004); `re-approved` never resets attempts, so label toggling cannot bypass the cap (B OD-6, U-005). B is right that approval evidence must be complete, not first-page.

**Variant C (identity by node ID, SQLite).** Strongest form: node and account IDs survive renames (C §3, §7, U-007); consuming the slot and entering `unknown` is one durable transaction before any external I/O, and expiry never releases a consumed slot (C §7); an append-only transition table is written in the same transaction; a next-permitted-request time is persisted for rate limits (C NFR-004, U-009); absent evidence is never positive (C §3). C is right that the dispatch record is the safety core and deserves transactional semantics.

**Variant D (operations).** Strongest form: a runbook with a pre-flight, an exit-code action table, a 24-hour shadow `--dry-run` rollout, a kill switch, staleness detection at 900 s and SLOs (D §8, NFR-013, U-011, U-012). Its ambiguity rules are the most conservative: `pending_orphan` is abandoned and never relaunched, and `failed` relaunches only while `launches == 0` (D §7). It states "Default interactive mode, never a bypass mode" for the launched session (D OD-7), the only firm position on the largest residual risk. D is right that a poller nobody can see failing is a liability.

##### Strengths claimed (variant E)

1. **Explicit call-budget model.** E §5 derives idle = 2 calls, worst = 1 + 1 + 10 x 3 + 1 = 33, and 12 cycles an hour = 24 calls (0.48 percent of 5,000) idle and 396 (7.9 percent) worst, and notes the allowance is per login so W workspaces on one login cost W times that. No other variant states the multiplier W; it turns the same-login rule (A-004) from a correctness footnote into a quantified cost argument (E O-4).
2. **Cost scales with candidates, not with Project size (U-014).** E FR-008 reads each examined candidate's own `projectItems`. A, B, D list Project items (A FR-006, B FR-004, D FR-007) and C paginates the Project (C FR-006). A Project also holds Done items and only grows, so a `-L 100` page stops covering it at some point; D concedes "Projects over 100 always fail" (D R3), and A and B fail closed at 100 (A FR-006, B §7.4). Dispatch then stops permanently whatever the Backlog holds. E has no such cliff.
3. **Cheap-first filter order.** E FR-004 drops candidates not assigned exactly to the own login before any per-candidate call, so 50 tagged issues of which 2 are mine cost 2 x 3 calls, not 50 x 3 (E FR-004 AC). No other variant specifies a prefilter ahead of the per-candidate reads.
4. **Hard per-cycle ceiling independent of bugs.** E NFR-005 caps `gh` calls at 35 and aborts remaining examinations (AC: 100 mocked candidates, at most 35 calls). A, C and D rely on `max_candidates` arithmetic alone.
5. **Rate-limit behavior that stops the damage.** E NFR-006 stops all GitHub calls on 403/429 and launches nothing (AC: limit on call 3 means exactly 3 calls). B R9 keeps reading per issue into a 403 storm (X-006).
6. **Launch spend is bounded in absolute terms.** The only paid event is a session. E FR-018 and NFR-012 cap it at 1 per cycle and 6 per day per workspace; A, B, C, D cap only per cycle, so a selection bug could cost up to 288 sessions a day per workspace. E §7 states the asymmetry: a duplicate launch costs a session, a missed one costs one `reset`.
7. **Ambiguity resolves toward not launching.** `pending` after its lease goes to `unknown`, `unknown` without an id goes to `abandoned`, `launched` with no claim goes to `abandoned` (E §7). This matches C and D on X-001 and X-002 and contrasts with B.
8. **Field minimization as a cost and security control.** E NFR-002 whitelists retained fields; E NFR-011 forbids any model-client import. Smaller payloads, no text in logs.
9. **State is bounded.** E NFR-013 prunes terminal records after 30 days and caps `considered` at 1,000. No other variant bounds ledger or `considered` growth.
10. **Per-issue record files** (E §7): a cycle reads and rewrites only the at most 10 records it touches, never a whole ledger, and a damaged file can block one issue rather than all.
11. **Honest scope of optimisations.** ETag requests are listed as follow-up and flagged UNVERIFIED (E §9) rather than baked into the contract.

##### Weaknesses identified in others

1. **A, B, D: Project item-list as the sole Project source** has a permanent fail-closed cliff at 100 items (A FR-006; B §7.4; D R3). Raising D's limit to 500 (D R3) enlarges the payload on every one of 12 cycles an hour without fixing growth.
2. **C: full Project pagination every cycle** (C FR-006) makes cost linear in Project size, and C has no call ceiling; C NFR-008 only requires pagination calls to be counted in reporting, not capped.
3. **B: highest per-candidate cost.** 42 calls per cycle (B NFR-007: `2 + 4 x 10`) with two snapshots, events and comments per candidate, and no rate-limit stop (B R9).
4. **B: relaunch of a `launched` entry after lease with no marker** (B §7.3, X-001) can start a second session beside a possibly running first one, the most expensive failure, and contradicts B's own `max_launches` 1 (B §7.4).
5. **B: corrupt state loads as empty** (B NFR-010, X-003), which re-opens every pre-marker issue to a launch; a cost multiplier.
6. **A: `pending` found after lease becomes `failed` and is retryable** (A §7, X-002), and an unclassified launch failure also reaches `failed` (A FR-014, X-004); both permit a second session.
7. **A, B: label-only escape hatches** (A OD-5 `off`; B FR-022) change the meaning of "in a Project, Backlog" (X-005) to save a scope grant.
8. **C: SQLite plus explicit `init-state`** adds an operator step and a schema-migration surface to a job whose steady state is "two calls, nothing to do". Operator time is part of cost-to-serve. This is a cost, not a disqualifier (see Concessions).
9. **D: `rate_remaining` in every audit line** (D NFR-006) has no stated source; if it needs `gh api rate_limit` it adds a call to each idle cycle, contradicting "idle cycles make 2 calls" (D NFR-009).
10. **D versus A on the lock exit:** D exits 75 and feeds it into alerting (D FR-017, FU-4) while A exits 0 on `locked` (A FR-018). Neither prices a hung-cycle alarm against a benign overlap (X-007).

##### Concessions (real weaknesses of variant E)

1. **Events are fetched with one unpaginated call** (E FR-006). The REST events list is oldest-first and paged; on an issue with a long history the "latest `labeled` event" may sit on a later page and E would judge on stale data. B (FR-007, FR-008) and C (§3) fail closed on incomplete history. E must adopt that rule. This is a safety gap, not a style one.
2. **A timeout is not classified.** E §7 defines `failed` as "definite error, no session started" and `unknown` only for `agent_session_operation_unknown` or a crash; a timed-out or malformed launch reply is left unmapped. C FR-011 maps it to `unknown`. E must do the same (X-004).
3. **Corrupt record handling is unstated** (E NFR-008 covers `gh` and `orca` output, not the record). A, C, D fail closed (X-003).
4. **The daily cap has no stored counter.** The record fields (E §7) hold no date or count; the cap must be derived by scanning `records/*.json`, which pruning bounds but E does not say. 6 per day is an unevidenced [PROPOSAL] and slows a legitimate drain to 6 issues a day.
5. **Label names `claim-ready` and `claim-approved` are not namespaced** (E O-1); A, B, D namespace theirs.
6. **`--agent <agent>` widens the fixed contract** (E FR-014, X-008); the seed says `claude`.
7. **The audit file has no rotation** (E FR-020); D rotates at 5 MiB (D NFR-006). A 300-byte line every 5 minutes is about 30 MB a year: small but unbounded.
8. **Module name `select.py`** (E §8) shadows a standard-library name; use `selection.py`.
9. **`reset <N>` mutates state with no stated lock or audit line** (E FR-023).
10. **Per-issue files are not atomic across files.** Only SQLite (C §7) gives one transaction for slot consumption, transition and daily count.
11. **GraphQL `projectItems` is itself unverified** (E R-5) and needs `read:project` like every other Project read; U-014 is a design hypothesis until the live test.
12. **Dropping unassigned issues before any call** (E FR-004) makes an approved-but-unassigned issue invisible (A-005); E cannot even count them without paying for a call.
##### Shared-assumption responses

- **A-001 QUALIFY:** persistence of the state path must be checked by `check-config` before enabling; E's daily cap (E FR-018) bounds the loss if the record vanishes.
- **A-002 ACCEPT:** all variants gate enablement on the live test; E's 6-per-day cap bounds the cost of sessions that start but do not run the command.
- **A-003 QUALIFY:** the Project field and option and the dispatch key should use immutable IDs (C §7); label names fail closed when renamed. Resolving IDs costs calls unless cached, so cache them in `status`-visible state.
- **A-004 QUALIFY:** accept it as a scope limit and add A's `enabled=false` default (A OD-2); the cost of a violation is W times the call budget (E §5) plus duplicate sessions.
- **A-005 QUALIFY:** accept the rule but add an audit counter of dropped not-owned approved issues so the wait is visible; E FR-004 drops them before paying for a call.
- **A-006 QUALIFY:** treat a backward clock jump as "lease not expired" and test with a fake clock (C NFR-004).
- **A-007 QUALIFY:** the state path must be a local filesystem; `check-config` warns otherwise.
- **A-008 QUALIFY:** require actor type `User` plus the allow-list (D FR-006), and record the human-run-bot residual; actor type and id are free in the events payload.
- **A-009 QUALIFY:** safety does not depend on it in E, because an unclaimed `launched` becomes `abandoned`, never a relaunch; only liveness does. The live test must measure claim duration and set the lease from it.
- **A-010 QUALIFY:** `check-config` should require owner-only mode (0600) and refuse group- or world-writable allow-list files.

##### Per-point positions

| Point | Level | Superior | Conf % | One-line evidence |
|---|---|---|---|---|
| S-001 | L1 | A | 45 | Given/Then bullets map directly to tests (A §4) |
| S-002 | L1 | NONE | 60 | Count is not quality |
| S-003 | L2 | HYBRID | 60 | Take A's stages, B's root causes, D's runbook, E's budget |
| S-004 | L2 | E | 55 | Seven modules suffice; but rename `select.py` (concession 8) |
| S-005 | L3 | C | 50 | Only SQLite gives one transaction for slot, transition and count (C §7) |
| S-006 | L1 | NONE | 70 | ID scheme is cosmetic |
| S-007 | L1 | NONE | 60 | Traceability codes equivalent |
| S-008 | L1 | A | 40 | Table form is the easiest to review |
| C-001 | L3 | HYBRID | 45 | Namespaced names (A, D) resolved to IDs (C §7) |
| C-002 | L3 | HYBRID | 60 | C account IDs, D `User` type, B complete paging |
| C-003 | L3 | E | 65 | Per-issue `projectItems` avoids the 100-item cliff (E FR-008; D R3) |
| C-004 | L3 | NONE | 60 | All reduce to sole-assignee; C's ID match is the only difference |
| C-005 | L3 | A | 55 | `enabled=false` default is a mechanical guard (A OD-2) |
| C-006 | L3 | E | 55 | Prefilter then 35-call cap (E FR-004, NFR-005); add B's paging rule |
| C-007 | L3 | HYBRID | 50 | D's separate `attempts`/`launches` plus E's ambiguity rule |
| C-008 | L3 | E | 65 | Only E adds an absolute daily bound (E FR-018); value unevidenced |
| C-009 | L3 | A | 55 | `attempts -= 1` on cancel is exact (A §7); C is stronger but heavier |
| C-010 | L2 | B | 55 | `orca-cli` probe handles screen-reader clash (B FR-014); E's `--agent` widens |
| C-011 | L3 | C | 60 | Timeout maps to `unknown` (C FR-011); E leaves it unmapped |
| C-012 | L3 | NONE | 70 | All reach integer-only; property test (D) is cheap to add |
| C-013 | L3 | C | 50 | Account IDs plus Triage check (C §3); needs extra calls |
| C-014 | L2 | D | 55 | Only firm "never a bypass mode" (D OD-7) |
| C-015 | L3 | C | 55 | "Absent evidence is never positive" (C §3) |
| C-016 | L3 | HYBRID | 55 | E's stop plus hard cap with C's persisted next-request time |
| C-017 | L2 | D | 55 | Shadow dry-run and staleness check (D §8) |
| C-018 | L3 | D | 50 | Kill switch plus alertable lock exit (D FR-017); price the alarm |
| C-019 | L2 | HYBRID | 55 | D's rotation, E's `gh_calls` and `duration_ms` |
| C-020 | L2 | E | 50 | `check-config` and `status` help; `reset` needs lock and audit |
| C-021 | L2 | A | 55 | JSON avoids the 3.11 `tomllib` need (A OD-9) |
| C-022 | L2 | HYBRID | 50 | C crash injection, D reruns, E 50-cycle at-most-once |
| C-023 | L2 | E | 45 | ETag follow-up kept UNVERIFIED (E §9) |
| C-024 | L3 | A | 45 | Marker count with expired-pending handling (A FR-008/009) |
| C-025 | L2 | E | 50 | Whitelist plus `test_no_text` (E NFR-002) |
| X-001 | L3 | HYBRID | 70 | Only B relaunches; A, C, D, E abandon or never relaunch |
| X-002 | L3 | D | 50 | `pending_orphan` abandoned, never relaunched (D §7) |
| X-003 | L3 | HYBRID | 55 | Fail closed per A, C, D; B empty-reload re-opens every issue |
| X-004 | L3 | C | 65 | Timeout or malformed output gives `unknown` (C FR-011) |
| X-005 | L3 | D | 60 | No label-only flag (D OD-4; C FR-006) |
| X-006 | L3 | HYBRID | 55 | E's stop and cap with C's persisted wait; B's R9 is worst |
| X-007 | L2 | NONE | 55 | No variant prices alarm against benign overlap |
| X-008 | L2 | A | 70 | Seed fixes `--agent claude`; A keeps it |

## Round 1 tally



Votes are in advocate order A,B,C,D,E. Letter = that variant is superior; H = HYBRID; N = NONE (no variant better / not a quality signal). Agreed = at least 4 of 5 advocates give the same answer. 41 S-, C- and X- points: 13 agreed, 28 unresolved. The 10 shared assumptions (A-NNN) are handled by the ACCEPT/REJECT/QUALIFY responses in each round-1 file.

| Point | Level | Votes (A B C D E) | Leading | Count | Status |
|---|---|---|---|---|---|
| C-001 | L3 | A A C D H  | A | 2 | UNRESOLVED |
| C-002 | L3 | H H C H H  | H | 4 | AGREED |
| C-003 | L3 | E E H E E  | E | 4 | AGREED |
| C-004 | L3 | A B C H N  | A | 1 | UNRESOLVED |
| C-005 | L3 | H A H H A  | H | 3 | UNRESOLVED |
| C-006 | L3 | E H H E E  | E | 3 | UNRESOLVED |
| C-007 | L3 | D H C D H  | D | 2 | UNRESOLVED |
| C-008 | L3 | H H C H E  | H | 3 | UNRESOLVED |
| C-009 | L3 | C D C C A  | C | 3 | UNRESOLVED |
| C-010 | L2 | H B H H B  | H | 3 | UNRESOLVED |
| C-011 | L3 | D H C C C  | C | 3 | UNRESOLVED |
| C-012 | L3 | H N H N N  | N | 3 | UNRESOLVED |
| C-013 | L3 | H B C H C  | H | 2 | UNRESOLVED |
| C-014 | L2 | B H H B D  | H | 2 | UNRESOLVED |
| C-015 | L3 | A B C H C  | C | 2 | UNRESOLVED |
| C-016 | L3 | H H H H H  | H | 5 | AGREED |
| C-017 | L2 | D D H D D  | D | 4 | AGREED |
| C-018 | L3 | H D H D D  | D | 3 | UNRESOLVED |
| C-019 | L2 | D H H H H  | H | 4 | AGREED |
| C-020 | L2 | A A H H E  | A | 2 | UNRESOLVED |
| C-021 | L2 | A A H A A  | A | 4 | AGREED |
| C-022 | L2 | H H H H H  | H | 5 | AGREED |
| C-023 | L2 | A B H H E  | H | 2 | UNRESOLVED |
| C-024 | L3 | A H C D A  | A | 2 | UNRESOLVED |
| C-025 | L2 | H H H H E  | H | 4 | AGREED |
| S-001 | L1 | H B N D A  | H | 1 | UNRESOLVED |
| S-002 | L1 | N N N N N  | N | 5 | AGREED |
| S-003 | L2 | H H H H H  | H | 5 | AGREED |
| S-004 | L2 | A B C H E  | A | 1 | UNRESOLVED |
| S-005 | L3 | A H C D C  | C | 2 | UNRESOLVED |
| S-006 | L1 | N N B N N  | N | 4 | AGREED |
| S-007 | L1 | B B H B N  | B | 3 | UNRESOLVED |
| S-008 | L1 | N N B B A  | N | 2 | UNRESOLVED |
| X-001 | L3 | A D C D H  | D | 2 | UNRESOLVED |
| X-002 | L3 | D H C D D  | D | 3 | UNRESOLVED |
| X-003 | L3 | A D H D H  | D | 2 | UNRESOLVED |
| X-004 | L3 | C H C C C  | C | 4 | AGREED |
| X-005 | L3 | D H H D D  | D | 3 | UNRESOLVED |
| X-006 | L3 | H H C H H  | H | 4 | AGREED |
| X-007 | L2 | H D H H N  | H | 3 | UNRESOLVED |
| X-008 | L2 | A H H D A  | H | 2 | UNRESOLVED |

## Round 2: Rebuttals

### Variant A Advocate (rebuttal)

#### Round 2: advocate A (architect; maintainability and extension seams)

Read: blind/variant-A..E, diff-analysis.md, rounds/round1-advocate-A..E, rounds/round1-tally.md. No round-2 file existed yet.

##### 1. Responses to criticisms

1. **Two retry paths: an orphaned `pending` and a lost reply both become retryable `failed` (B, C, D, E; X-002).** CONCEDED. A §7 sends a lease-expired `pending` (`lost_reply`) to `failed`, and FR-014's "any other failure" also maps to `failed`, which is retryable. Either path can start a second session. Adopted: D §7 row "`pending` found at cycle start → `abandoned`, `pending_orphan`".
2. **A timeout is treated as `failed` (B, D, E; X-004).** CONCEDED. Only a definite Orca error is `failed`. A timeout, malformed JSON or `agent_session_operation_unknown` becomes `unknown` (C).
3. **A's 100-item Project cliff (B, E; C-003, C-006).** CONCEDED. `gh project item-list -L 100` fails closed for good once the Project grows past 100 items, and A also voids the whole cycle when that happens. E's per-issue `projectItems` lookup scales with the number of candidates rather than the size of the Project (E §5), and it removes the Project from the inputs a cycle shares.
4. **"Every `gh api` call is `--method GET`" conflicts with GraphQL (B).** CONCEDED. GraphQL reads are POSTs. Replacement rule: "The poller sends no REST write verb (POST/PATCH/PUT/DELETE outside `gh api graphql`) and no GraphQL `mutation`. Every GraphQL query is a module constant, and a test asserts that none of them contains `mutation`." The constant also gives the test one fixed thing to scan.
5. **A whole-cycle fail-closed rule is too wide (B; C-015).** PARTLY CONCEDED. A was right about inputs shared by the whole cycle: the login, the discovery list, the allow-list and the record store. A was wrong to treat the Project that way. Once item 3 is adopted, the Project is a per-issue read, and B's and E's per-issue skip applies to it.
6. **`orca` is hard-coded as argv[0] (B).** CONCEDED, with new evidence that the fix is reuse rather than new code (§3 E1).
7. **The Project-mode `off` bypass and the label-only mode (C, E; X-005).** CONCEDED in round 1, and still conceded. Neither mode exists in the merged spec.
8. **A's pre-launch re-read does not prove the issue is still in Backlog (C).** CONCEDED. The re-read must repeat the per-issue Project Status check as well as state, labels and assignees. The extra cost is one call per launch, and there is at most one launch per cycle.
9. **"Speculative replacement interfaces" (C; S-004).** CONCEDED in part. A §8 declared five protocols plus a routing table. Typed seams are kept only where tests need a fake: the runner, the record store and the launcher. Routing becomes the single pure function `is_intended_owner` that D and E both specify, and the approval module is merged into the predicates.
10. **A held lock exits 0, which hides hung cycles (D, E; C-018, X-007).** CONCEDED. Exit 0 makes "lock held" indistinguishable from a healthy idle cycle in any exit-code alert. D's exit 75 (EX_TEMPFAIL) plus an audit line `lock_held` keeps the overlap visible. D's NFR-013(b) already counts 0 and 75 as healthy, so a single overlap does not page anyone, and D's staleness threshold (900 s) reports a hung holder.

##### 2. Changed views

- **B.** Its Orca probe and its worktree-origin check moved, for me, from hardening to correctness requirements (§3 E1, E2). B's NFR-010 rule, which resets a corrupt record to empty, and §7.3's relaunch of `launched` after the lease are still the two most dangerous rules in any variant.
- **C.** Consuming the launch slot before any I/O is the cleanest statement of at-most-once. D's JSON form reaches the same guarantee: `pending` is written first, an orphaned `pending` is never relaunched, and `launches == 0` is checked before a fresh launch. That makes SQLite and the `init-state` verb optional. I keep C's rules (missing store after initialization fails closed, account IDs, absent evidence is never positive) and drop its storage engine.
- **D.** It is the strongest operational spec: exit 75, the `DISABLED` file, the runbook, staleness, the 24-hour shadow dry run. Its one hole is FR-014's "any other non-zero exit to `failed`", which turns a timeout into a retryable outcome. Its approver file shipped with the Coder template has the same problem as A-010.
- **E.** Its per-issue Project lookup, its pre-filter that drops non-owned issues before any per-issue call, and its 35-call cap are the right ways to keep costs bounded. Its daily cap is sound once it is defined from record timestamps; E conceded that it had no counter. Its `--agent <agent>` and `select.py` are withdrawn in E's own round 1.
- **On my own variant.** A's real contribution is a seam layout and a clear set of states. Where A loses on the safety rows (X-002, X-004, the Project read), I now rank it below C and D.

##### 3. New evidence (checked with Read/Grep this round)

- **E1. The Orca probe already exists.** `src/superclaude/cli/install_user_setup.py:35` reads `_ORCA_CLIS = ("orca-ide", "orca")`. Lines 198-221 hold `_find_orca()`. It runs `[path, "skills", "list", "--json"]` with `timeout=10` and returns only a binary whose `topics` include `orca-cli`. Its docstring says "a bare `orca` ... is usually the GNOME screen reader". The merged spec should reuse this function rather than specify a new probe. A, D and E hard-code `"orca"`, so on a Linux desktop they could launch the screen reader.
- **E2. The worktree's `origin` decides which repo the claim writes to.** `skills/sc-issue-protocol/scripts/origin_repo.py:102-110` (`check_claim`) returns a bare number as an integer with no repo check. `SKILL.md:70` says `<R>` is the `origin` repo and "Nothing else is consulted". D3 makes the prompt a bare integer, so a `--worktree` whose origin is another repo makes the claim assign and comment on issue N in the wrong repo. B's and C's origin check is therefore load-bearing, and A, D and E all lack it.
- **E3. The claim rule matches "exactly {own login}".** `refs/claim.md:41-42`: "Assigned to anyone other than the current login → STOP", and "Already assigned to the current login → continue". An issue assigned to {me, bob} therefore stops the claim, so A's and D's "contains own login, any other excludes" selects the same set as the "exactly {own}" rule in B, C and E. The variants differ in wording only, so C-004 can converge.
- **E4. The claim reads untrusted text itself.** `claim.md:26` runs `gh issue view ... --json number,title,body,...,comments`. Field minimization in the poller protects the prompt only. This confirms that T1 is a residual risk in every variant and supports C-014's gate.
- **E5. An atomic-write helper already exists.** `src/superclaude/cli/swarm/atomic.py:14-39` `write_prepared_bytes` performs mkstemp in the same directory, fsync and `os.replace`. `tempfile.mkstemp` creates the file with mode 0600, so the replaced record is 0600 with no extra chmod. Reuse it rather than re-specify it.
- **E6. No Python file lock exists in the package.** `fcntl` and `flock` appear only in shell hooks and ccsession, so the lock is new code. That supports C's requirement to test it with two real processes (A-007).
- **E7. Registration point.** `src/superclaude/cli/main.py:559-561`: `main.add_command(reflect_group, name="reflect")`. `pyproject.toml:16` reads `requires-python = ">=3.10"`, so the config is JSON (no `tomllib`). `sqlite3` is also in the standard library, so dependencies do not settle S-005 either way.

##### 4. Updated positions (all 28 UNRESOLVED points)

| Point | Superior variant | Confidence % | Merged ruling (≤45 words) |
|---|---|---|---|
| C-001 | HYBRID (D names, A fail-closed) | 60 | The trigger label `issue-watch:trigger` and the approval label `issue-watch:approved` are configurable and matched by exact, case-sensitive name. A missing or renamed label matches nothing, so nothing launches. The owner creates the labels; code never does. |
| C-004 | HYBRID (E rule, D reasons) | 80 | The intended owner is the issue whose assignee set equals exactly {own login}, where the login is read each cycle by `gh api user`. Unassigned and other-assignee issues are skipped as `unassigned` and `assigned_other`. The rule lives in one pure function, `is_intended_owner`. |
| C-005 | HYBRID (A default, D audit, C wording) | 70 | `enabled` defaults to false. Enable the poller in exactly one workspace per login; a second workspace on the same login is unsupported. Every audit line carries `host` and `login`, so a double enablement is visible. |
| C-006 | E | 75 | Discovery is one `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --json number,labels,assignees,state -L 100`; exactly 100 results exits 4. Non-owned issues are dropped before any per-issue call, and per-issue calls stop at a 35-call cap. |
| C-007 | HYBRID (A states, D counters, B fields) | 75 | States: pending, launched, unknown, failed, abandoned, claimed. Fields: `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `launch_cwd`, UTC timestamps, `last_reason`. A fresh launch requires `launches == 0`. |
| C-008 | HYBRID (A/D numbers, B timeouts, E backoff and day cap) | 60 | [PROPOSAL] values: lease 60 min, `max_attempts` 3, one fresh launch per issue, one launch per cycle, `max_candidates` 10, 10-minute backoff after `failed`, `gh` timeout 20 s, `orca` timeout 120 s, and at most 6 fresh launches per rolling 24 hours, counted from record launch timestamps. |
| C-009 | HYBRID (D order, C consume-before-I/O) | 80 | Write `pending` atomically before any launch I/O. Then re-read the issue's state, labels, assignees and Project Status. A failed re-read deletes the entry (`revalidation_failed`) without a launch. A `pending` found at cycle start becomes `abandoned` with reason `pending_orphan`. |
| C-010 | HYBRID (A/D argv, B probe, B/C origin) | 85 | The argv is `[<orca>, agent, launch, --agent, claude, --worktree, path:<abs>, --surface, terminal, --prompt, <prompt>, --json]`. `<orca>` comes from the existing `_find_orca()`. `<abs>` must exist and its `origin` must be IronbellyOrg/IronClaude; otherwise exit 2 before any `gh` call. |
| C-011 | C | 80 | A timeout, malformed output or `agent_session_operation_unknown` gives `unknown`. With an `operationId`, it is retried only through `--retry-launch <id>`. Without an id, or once the lease expires, it becomes `abandoned`. Only a definite Orca error gives retryable `failed`. |
| C-012 | HYBRID (A type rule, D property test) | 80 | `build_claim_prompt(n)` accepts only an `int` (not `bool`) in 1..999999999 and returns `/sc:issue --claim <n>`; any other value raises `ValueError` and nothing launches. A property test asserts that every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`. |
| C-013 | HYBRID (C IDs, A empty-means-none, B fail-on-missing) | 70 | Approvers are listed as GitHub account IDs in a local file owned by the user and not writable by group or others. A missing or empty list approves nothing, and `check-config` then exits 2. The Coder template does not ship the file. |
| C-014 | HYBRID (B gate, D default, C acceptance) | 75 | No cron entry is enabled until an owner-run live test shows the prompt running as a slash command and records the session's permission mode. The default is no override. A bypass mode requires the owner's written acceptance. |
| C-015 | HYBRID (C principle, B/E per-issue scope) | 80 | Failures of shared inputs (login, discovery, allow-list, record store, rate limit, Project scope) void the cycle with zero launches. Per-issue read failures (events, Project item, marker, re-read) skip only that issue, with a reason. Absent or incomplete evidence never counts as positive. |
| C-018 | D | 75 | A non-blocking `flock` on `<state_dir>/lock` is held for the whole cycle. A held lock means no external call, audit `lock_held` and exit 75. The `<state_dir>/DISABLED` file means no external call, audit `disabled` and exit 0. `status` reports `last_cycle_age_seconds`. |
| C-020 | HYBRID (A verbs, E `reset`, C init) | 70 | Verbs: `once [--dry-run]`, `status [--json]`, `check-config` (which also creates the record store) and `reset <N>`. `reset` takes the lock, acts only on an `abandoned` entry and is audited. There is no flag-only interface. Exit codes are as in X-007. |
| C-023 | HYBRID (A, B, D, E lists) | 60 | Follow-ups: a live slash-command and permission test, which blocks enablement; the Coder cron and a persisted `state_dir`; confirmation of the `read:project` scope; alerting on staleness or repeated non-zero exits; ETag requests; per-actor permission checks. Options B and C, and Coder#477, return only on a revisit condition. |
| C-024 | HYBRID (A/D marker, C evidence rule) | 70 | `claimed` requires an own-login comment containing `<!-- sc:issue:claim -->`, read through a `--jq` boolean projection. Assignment alone is not evidence. An own marker with no record also records `claimed`, and that issue is never launched. |
| S-001 | HYBRID (D form, A argv literalness) | 55 | Each requirement is one "shall" sentence with an ID, plus one Given/When/Then line that names the stub call or file it observes. Argv lists, paths and markers are written verbatim wherever they form the contract. |
| S-004 | HYBRID (A trimmed, E size) | 65 | The package `src/superclaude/cli/issue_watch/` holds `runner`, `github`, `predicates`, `record` (store and lock), `launch`, `audit`, `cycle` and `cli`. Protocols exist only for the runner, the store and the launcher. It reuses `swarm/atomic.write_prepared_bytes` and `_find_orca`. No module is named `select`. |
| S-005 | HYBRID (D form, C init rule) | 65 | One JSON record file per state directory, with `schema_version`, written via `write_prepared_bytes` (mode 0600). `check-config` creates it. If it is missing or unparseable, `once` exits 6 with no launch and never resets it. SQLite is not required. |
| S-007 | B | 55 | Every requirement cites its source in a traceability table, using a seed section, research fact, research question or `file:line`. A source that has not been verified is tagged UNVERIFIED. |
| S-008 | HYBRID (B columns, D requirement links) | 50 | The risk table has an ID, the risk, its likelihood, its impact and a mitigation. Each mitigation names the requirement IDs that implement it. |
| X-001 | D | 85 | `launched` is never relaunched. If no own claim marker appears before the lease expires, it becomes `abandoned` with reason `claim_not_observed`, and only an operator `reset <N>` can recover it. |
| X-002 | D | 85 | A `pending` record found at cycle start (a crash between the record write and Orca's reply) becomes `abandoned` with reason `pending_orphan`. It is never relaunched or retried automatically. |
| X-003 | HYBRID (A/C/D) | 85 | An unparseable record or an unknown `schema_version` gives exit 6 and zero launches, and the file is left unchanged. It is never reset to empty. Recovery is a documented operator procedure. |
| X-005 | HYBRID (D no-fallback, E lookup) | 80 | There is no label-only mode and no mode that turns the Project check off. Project membership and Backlog come from the issue's own `projectItems`. An unreadable item skips that issue; a missing `read:project` scope voids the cycle with exit 3. |
| X-007 | HYBRID (D 75 and actions, E split) | 65 | Exit codes: 0 ok or disabled; 2 usage or config; 3 GitHub auth, scope, timeout or non-JSON; 4 discovery truncated; 5 rate limited, with the next permitted time persisted; 6 record unreadable or unwritable; 7 a launch ended `failed` or `unknown`; 75 lock held. Each code has a runbook action. |
| X-008 | HYBRID (A/D) | 85 | The launch uses `--agent claude` exactly, as in the seed, and the agent is not configurable. D1-D3 are restated verbatim. The poller reads no comment content beyond the boolean marker projection, which rejects C §6's "bounded comment content". |

##### 5. Shared-assumption changes

- **A-001** CHANGED, narrower. "Once initialized, a missing store fails closed" now has a mechanism: only `check-config` creates the store, and `once` exits 6 when it is missing. Without that mechanism, losing the directory silently re-arms every launch. The persistence of `$HOME` remains a follow-up for the Coder template.
- **A-002** CHANGED, wider. The live test must run in the configured worktree and confirm that its `origin` is IronbellyOrg/IronClaude, because the claim's repo comes from `origin` alone (E2).
- **A-005** STRENGTHENED. Because of `claim.md:41-42`, "exactly {own login}" is not stricter than the claim; it is the claim's own rule (E3). Assigning before approving remains the setup rule, and an `unassigned` skip reason makes waiting issues visible.
- **A-007** CHANGED, test added. No Python lock exists in the package (E6). The merged spec requires a test that runs two real processes against a local `state_dir`.
- **A-009** CHANGED to "not a safety premise". With X-001 and X-002 ruled as above, no state is relaunched because the lease expired. The lease length only decides when `launched` is reported as `claim_not_observed`, so a wrong value produces noise but never a duplicate. A-006's clock-skew rule (treat leases as unexpired when `now` is earlier than `updated_at`) is unchanged.
- A-003, A-004, A-006, A-008 and A-010 are unchanged from round 1. On A-010, D's approver file shipped with the template is rejected under the same rule (C-013).

### Variant B Advocate (rebuttal)

#### Round 2 rebuttal: advocate B (analyzer lens: root cause, evidence)

##### 1. Responses to criticisms

Criticisms of variant B from round 1 (A, C, D, E) and from round 2 so far (A):

1. **NFR-010 resets a corrupt record to empty (X-003).** Conceded in full. The root cause is that B treated the record as a cache; it is the only at-most-once guard between launch and marker (the claim has no mutual exclusion; `refs/claim.md:41-42` stops only on *another* login). An empty record re-dispatches every `launched` issue whose marker is not yet posted. Adopt A/D: an unreadable or unknown-version record exits 6, launches nothing, never resets.
2. **Section 7.3 relaunches `launched`/`failed` after the lease (X-001).** Conceded in full. Advocate A is right that this and item 1 are B's two most dangerous rules. The lease cannot be a relaunch trigger because the claim posts its marker in Wave 6 after an unmeasured multi-agent Wave 4 (A-009). Adopt D: `launched` without a marker after the lease becomes `abandoned`, reason `claim_not_observed`; only `reset` reopens it.
3. **`pending` found at cycle start is treated as `launched` (X-002).** Conceded. Treating it as `launched` fed item 2's relaunch path. Adopt D: `abandoned`, reason `pending_orphan`.
4. **`--label-only` mode (X-005).** Conceded. A missing `read:project` must not widen eligibility; option D is the documented fallback. Withdrawn.
5. **No rate-limit handling, 42-call worst case (X-006, E).** Conceded on handling: adopt C's persisted next-permitted time plus a distinct exit code. Partly contested on cost: B's 42 had two causes. The Project list (one call, but a 100-item cliff) is fixed by adopting E's per-issue `projectItems`. The complete event history is not a cost bug; it is the correctness requirement round 1 agreed (C-002 HYBRID, 4 of 5). The merge keeps completeness and budgets it: event pages count toward E's 35-call cap, and a cap reached mid-issue skips that issue, never approves it.
6. **One verb, no `status` or `check-config` (C-020, C-021).** Conceded. Adopt A/D verbs and D's `DISABLED` switch.
7. **`--method GET` rule contradicts GraphQL reads, which are POST (my own round-1 finding).** Conceded; A accepted the corrected wording. The rule becomes: REST calls are GET; GraphQL calls send only a `query` document from a fixed set, never `mutation`.
8. **No bot check on the approver.** Conceded: `actor.type == "User"` and login not ending `[bot]` (agreed C-002).
9. **Lock loser exits 0 (FR-019).** Conceded to D's exit 75 `lock_held`: a hung cycle that silently exits 0 every 5 minutes is invisible to the staleness signal.

Points I still defend, with evidence, because other variants dropped them:

- **Origin check before any `gh` call (B FR-002).** A's round-2 E2 shows `origin_repo.py:102` `check_claim` returns a bare int with no repo check, and the claim consults only `origin` for the repository. If the configured worktree's origin is not IronClaude, the launched claim targets the wrong repository. Only B and C test this; it belongs in C-010, and A's ruling now includes it.
- **Orca probe (B FR-014).** A's E1 found `_find_orca()` at `install_user_setup.py:198` already resolving `orca-ide` or `orca`. A literal `"orca"` argv[0] (A, D) fails on a host that has only `orca-ide`. Reuse the helper.
- **Approver and event ID in the audit (B FR-020).** A's C-007 ruling now carries `approver_id` and `approval_event_id`; nothing further needed.
- **Re-approval never resets counters (B OD-6).** No other variant states it. Without it, removing and re-adding the approval label is a free relaunch after `failed`/`abandoned`. Added to the C-007 ruling.
- **Unrecognised argv fails loudly in tests (B FakeRunner exit 99, `_assumed_shape` fixtures).** This is how "read-only" is proven by test rather than by review, and how UNVERIFIED JSON shapes stay marked until the live test. Carried in S-007 (traceability with UNVERIFIED tags).
- **Per-issue fail scope (B NFR-009).** Converged into A's C-015 ruling.

##### 2. Changed views on other variants

- **D** is now my reference for the state machine and operations: `launches` separate from `attempts`, `pending_orphan`, `claim_not_observed`, `DISABLED`, exit 75, `last_cycle_age_seconds`. In round 1 I split votes between B and D; on X-001, X-002, X-003 and C-018 I now vote D outright.
- **E** fixes the one scaling defect every other variant shared: `gh project item-list -L 100` fails closed permanently once the Project passes 100 items (D's own R3 admits it). Per-issue `projectItems` makes cost scale with candidates, not Project size. E's 35-call cap is the right shape for B's pagination concern.
- **C** I underweighted. Its "absent or unreadable evidence is not positive evidence" is the cleanest statement of the fail-closed root cause, and account-ID approvers close the rename hole (A-003). I still reject SQLite (S-005): a JSON file written with the existing `write_prepared_bytes` (`swarm/atomic.py:14`) meets the integrity need with no new storage engine, and C's required properties (no silent reset, explicit init) carry over.
- **A** trimmed its seams in round 2 (protocols only for runner, store, launcher); my round-1 objection to speculative stages is resolved. A's conceded orca argv[0] and origin check now match B.

##### 3. New evidence (checked read-only this round)

- **N1. The house pattern for paged GitHub reads exists and fails closed at a cap.** `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:46-56`: explicit `-F per_page=100 -F page=<n>` with `--method GET`, the comment "Explicit page numbers avoid an unbounded gh --paginate on a broken API cursor", and "fail incomplete at the cap, never silently truncate". No other `--paginate` appears under `src/superclaude` (grep). So complete event and comment reads (C-002, C-024) have a precedent: explicit pages, each page counted, cap reached means incomplete, incomplete means not positive. This settles how C-002 and E's call cap compose.
- **N2. The claim reads comments itself and reuses the latest marker** (`refs/claim.md:26`, `:29`), and re-claim by the same login is "allowed and idempotent" (`:42`) with earlier marked comments edited (`:43`). Consequence: a duplicate launch for the same login does not double-post, but it starts a second full session and a second Wave 4. At-most-once remains a cost and review-load requirement; it never justifies trading a missed launch for a duplicate.
- **N3. The claim stops on a pull request** (`refs/claim.md:39`, `E-NOT-AN-ISSUE`) and on a closed issue (`:40`). The watcher's `state == OPEN` check and `gh issue list` (issues only) are defence in depth; C's explicit non-PR predicate costs nothing and can stay as a pure-function check.
- **N4. The claim proceeds on an unassigned issue** (`refs/claim.md:41-42` stops only on another login). Candidate-1 routing (exactly the own login assigned) is stricter than the claim, which is why A-005 (someone must assign first) is real and must be visible in the audit as `unassigned` skips.
- **N5.** Confirmed A's citations exist: `_find_orca` at `install_user_setup.py:198`, `check_claim` at `origin_repo.py:102`, `write_prepared_bytes` at `swarm/atomic.py:14`.

##### 4. Updated positions

"AGREE" means I accept advocate A's round-2 proposed ruling as written.

| Point | Superior variant | Confidence % | Merged ruling or AGREE with A |
|---|---|---|---|
| C-001 | HYBRID | 85 | AGREE |
| C-004 | A | 85 | AGREE |
| C-005 | HYBRID | 80 | AGREE |
| C-006 | HYBRID (E+B) | 80 | Discovery: `gh issue list --repo IronbellyOrg/IronClaude --state open --label <trigger> --json number,labels,assignees,state -L 100`; 100 results exit 4. Every `gh` call, including each event or comment page (`per_page=100`), counts toward a 35-call cap; cap reached mid-issue skips it `budget_exhausted`. |
| C-007 | D | 85 | A's fields and states, plus: removing and re-adding the trigger or approval label never resets `attempts` or `launches`; only `reset <N>` (audited) does. A fresh launch requires `launches == 0`. |
| C-008 | HYBRID | 75 | AGREE |
| C-009 | HYBRID | 70 | Immediately before launch, re-read state, labels, assignees and Project Status. A failed read or predicate skips the issue `revalidation_failed`, leaves the record unchanged and launches nothing. Only then write `pending` durably and call Orca. |
| C-010 | HYBRID (B+A) | 85 | AGREE |
| C-011 | C | 85 | AGREE |
| C-012 | HYBRID | 80 | AGREE |
| C-013 | HYBRID (C) | 80 | AGREE |
| C-014 | HYBRID | 80 | AGREE |
| C-015 | C | 85 | AGREE |
| C-018 | D | 85 | AGREE |
| C-020 | HYBRID | 85 | AGREE |
| C-023 | HYBRID | 75 | AGREE |
| C-024 | HYBRID | 80 | `claimed` requires a comment by the own login containing `<!-- sc:issue:claim -->`, read over all comment pages and returned only as a `--jq` boolean; an incomplete read is not evidence. Assignment is never evidence. A marker without a record yields `claimed`. |
| S-001 | HYBRID | 70 | AGREE |
| S-004 | A | 75 | AGREE |
| S-005 | HYBRID | 80 | AGREE |
| S-007 | B | 70 | AGREE |
| S-008 | HYBRID | 65 | AGREE |
| X-001 | D | 90 | AGREE |
| X-002 | D | 90 | AGREE |
| X-003 | D | 95 | AGREE |
| X-005 | D | 90 | AGREE |
| X-007 | HYBRID | 75 | AGREE |
| X-008 | HYBRID | 75 | AGREE |

Reasons for the four non-AGREE rows:

- **C-009.** A's text writes `pending` first and then deletes the entry when the re-read fails. Root cause: the deletion is needed only because the write came too early. Re-reading first removes the deletion path and one class of `pending_orphan` (a crash during a failed re-read would otherwise abandon an issue that never launched). The window between re-read and launch grows only by one local `fsync`. The audit line keeps the `revalidation_failed` evidence, so nothing is lost.
- **C-006.** Adds the page-counting rule from N1. Without it, "complete event history" (agreed C-002) and the 35-call cap (E) contradict on an issue with more than 100 events.
- **C-024.** Adds "all comment pages" and "incomplete read is not evidence". A marker on page 2 missed by a one-page read would leave a claimed issue `launched`, and under D's X-001 rule it would end `abandoned` instead of `claimed`: a wrong audit, not a duplicate. Low risk, cheap to state.
- **C-007.** Adds B OD-6 (no counter reset on re-labelling); otherwise A's text.

##### 5. Shared-assumption changes

Only assumptions whose answer changed since my round 1:

- **A-001 (state survives restarts):** QUALIFY, tightened. The store is created only by `check-config` (explicit init); a missing store after init exits 6 and never starts empty, so loss of `$HOME` stops dispatch rather than duplicating it.
- **A-002 (slash command runs from `--prompt`):** QUALIFY, extended. The same owner-run live test must also record the launched session's permission mode (C-014) and the real success and `unknown` JSON, which replace the `_assumed_shape` fixtures.
- **A-003 (logins stable):** changed from QUALIFY to a split ACCEPT. Owner routing stays by login (the claim itself works by login, N4); approvers move to account IDs (C-013), so a rename cannot transfer approval trust.
- **A-007 (`flock` effective):** QUALIFY, plus A's two-process lock test as acceptance; a local, single-host state directory is a documented setup precondition.
- **A-009 (marker within lease):** REJECT unchanged, now reflected in the merge: with D's X-001 and X-002 rules the lease is only a reporting threshold, so no safety property depends on it.

### Variant C Advocate (rebuttal)

#### Round 2 — Advocate C (backend)

##### Responses to criticisms

1. **No concrete launch argv or operator contract (A/B/D round 1). CONCEDED.** C's prose acceptance criteria are testable, but leave adapter behavior unspecified. Adopt A's fixed-agent argv, B's executable/origin checks and assumed-shape fixtures, and D's exit-action table, disable control, inspection, and rollout runbook. Add one configuration schema and numbered decisions. Syntax precision is independent of storage choice.

2. **SQLite, transition table, and initialization are heavy (A/B/E round 1; A/B round 2). PARTLY CONCEDED.** SQLite is unnecessary. One locked, versioned JSON document can atomically contain consumed keys and transition history. However, A/B's existing helper does not alone prove restart durability; see E1. Initialization remains a deliberate mutation, not an incidental effect of `check-config`. A validator that recreates lost state defeats the loss protection we agreed to preserve.

3. **Permanent suppression without recovery (A round 1). CONCEDED on operator support, not the invariant.** Status and the runbook must identify suppressed/unknown issues and explain investigation of the existing operation. A new submission after a consumed slot is a guarantee reset, not normal recovery. A/B's proposed `reset` must not be described as preserving lifetime at-most-once. Defer that mutating verb rather than ship an underspecified reset.

4. **Opaque IDs make setup harder; no lookup procedure (A/D round 1). CONCEDED.** Require reviewed setup instructions resolving display names into IDs, and show bindings in status. No lookup verb is necessary. Retain identity binding: deleting/recreating a label or Status option under the same name can satisfy name equality with a different policy object. A/B's claim that name changes only fail closed overlooks replacement under the old name. Owner/approver IDs also prevent trust following recycled names. Adapter support remains unverified until the controlled test.

5. **Bounded marker content weakens minimization (A/B/D round 1; A round 2). CONCEDED as an implementation choice.** Project marker recognition inside `gh` to booleans and author IDs; do not retain narrative in Python. This does not mean no component reads comments: gh must inspect bodies to recognize the marker. D3 restricts prompt content, not that inspection. Positive markers need authenticated-author matching; incomplete absence must never permit fresh submission.

6. **Full Project pagination costs grow with Project size; no hard request cap (E round 1). PARTLY CONCEDED.** C requires complete evidence but does not mandate whole-Project scans. Nevertheless it leaves query strategy and request ceiling unspecified. Adopt E's issue-local membership lookup and hard budget, with B's page accounting. A projectItems connection can itself paginate; unfinished reads cannot establish approval. Refresh requests count too.

7. **D's counters/JSON equal C's invariant (A/B round 2). ONLY WITH A CORRECTION.** Original D increments `launches` after a success/recognized-unknown reply. A generic error before that increment remains retryable. Increment the durable consumed-submission counter before invoking Orca. A/B still propose retryable `failed` after a “definite error”; error text is not a verified guarantee that no session started. Until the live API contract establishes otherwise, every submitted slot stays consumed.

8. **Final-refresh ordering (A/B round 2). AGREE WITH B'S DIRECTION.** Refresh first, persist launch intent, invoke Orca; canceled preflight need not create/delete an entry. Extend B's refresh beyond labels and Status: approval provenance, owner identity, Project membership, and marker evidence matter. State the unavoidable refresh-to-launch race. Never delete an existing consumed key on failed revalidation.

9. **Operational omissions (D round 1). CONCEDED.** Adopt the XDG default, disabled-by-default configuration, local-filesystem locking, kill switch, shadow rollout, and staleness signals. Neither `enabled=false` nor audited host names enforce one authority across machines; they reduce accidental activation and improve diagnosis only.

##### Changed views

- **A:** Its trimmed seams are adequate; routing registries and future backends are unnecessary. Accept its JSON configuration and concrete launch contract, but reject mutation through `check-config` and unqualified resets.
- **B:** Complete evidence and executable checks are foundational. Its refresh-before-write ordering is simpler than C's reservation wording. B correctly corrects A: unassigned issues can pass the claim, so watcher preassignment is stricter policy.
- **D:** Its runbook, stop switch, and exit-action mapping are the operational base. Its reply-based counter is not the safety base; consume before submission. Repeated lock losses must not count as healthy work merely because they emit current audit lines.
- **E:** Candidate-scaled reads and request budgets replace vague cost accounting. Six-per-day is a proposed availability/spend policy, not an evidenced requirement. Terminal-key pruning remains unacceptable; daily limits cannot protect against whole-ledger loss if their counters disappear too.
- **C:** I no longer prefer SQLite specifically (S-005). I retain durable identity and consumed-slot semantics; JSON is acceptable if it meets the complete durability contract.

##### New evidence

All checks used Read only; no tests, CLI probes, network requests, or live sessions ran. These source facts do not validate API response shapes.

- **E1 — Atomic replacement is not the complete durability contract.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/swarm/atomic.py`, `write_prepared_bytes`, fsyncs the temporary file and calls `os.replace`, but contains no parent-directory fsync. It is useful reuse, not proof that the replaced directory entry survives host/storage failure. State the crash boundary and verify required filesystem durability rather than infer it from the helper's name.
- **E2 — The Orca probe bypasses the proposed injected runner.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/cli/install_user_setup.py`, `_find_orca`, directly calls `shutil.which` and `subprocess.run` with a ten-second timeout. Reusing it unchanged while asserting every effect goes through `Runner` is inconsistent. Mock that boundary explicitly or adapt the probe behind the runner; include probe time in the cycle budget.
- **E3 — Authorized claim effects include ClickUp.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/skills/sc-issue-protocol/refs/claim.md` assigns GitHub in Wave 3 and invokes `clickup_claim.py`; later waves write local artifacts and GitHub comments. Risk acceptance must enumerate the existing claim effects, not call it only “read-and-assign” or authorize GitHub writes alone. The same file permits unassigned issues and posts the marker in Wave 6.
- **E4 — Pagination precedent also rejects repeated IDs.** `/home/coder/workspaces/worktrees/IronClaude/issue-331-github-issue-watcher/src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh`, `fetch_rest`, uses bounded pages and rejects repeated IDs, including a server ignoring page numbers. Carry that progress check into event/comment reads. Its GraphQL thread reader also demonstrates why read-only cannot mean every request uses GET.

##### Updated positions

All 28 UNRESOLVED points are covered. Requirement texts below are at most 45 words each. AGREE accepts that advocate's round-2 ruling for the point, except where this table explicitly replaces or qualifies it.

| Point | Superior variant (letter/HYBRID/NONE) | Confidence % | Merged ruling or AGREE with X |
|---|---|---|---|
| C-001 | HYBRID | 94 | Configure trigger and approval labels by approved immutable IDs, with proposed display names `issue-watch:trigger` and `issue-watch:approved`. Setup resolves and displays bindings; missing or replaced IDs fail closed. Name equality alone never rebinds policy. The poller never creates labels. |
| C-004 | C | 97 | Intended owner requires exactly one assignee whose account ID equals the authenticated, configured authority account. Retain current login for claim compatibility. Unassigned and foreign/multiple assignees receive explicit skip reasons. Preassignment is stricter than the claim and must be documented. |
| C-005 | HYBRID | 97 | Default disabled. Nominate one active authority and persistent ledger per repository/account; independent authorities are unsupported. Audit account ID, current login, authority ID, and host. Local configuration and host auditing do not provide distributed exclusion. |
| C-006 | HYBRID | 94 | AGREE with B; additionally, every Project connection page and final-refresh request counts toward the same budget. |
| C-007 | HYBRID | 99 | Persist states, stable repository/issue IDs, attempts, consumed submissions, approval actor/event IDs, operation ID, invocation context, timestamps, and reason. Increment consumed submissions durably before Orca invocation; fresh submission requires zero. Label changes, expiry, login changes, and reapproval never reset it. |
| C-008 | HYBRID | 92 | Proposed defaults: ten candidates, one fresh submission per cycle and issue, three safe pre-submission attempts, 60-minute reporting threshold, 35 GitHub calls, 20-second GitHub and 120-second Orca deadlines within 240 seconds. Six submissions per rolling day requires owner approval and durable accounting. |
| C-009 | HYBRID | 98 | Under the cycle lock, refresh all eligibility evidence immediately before committing consumed launch intent; stale or unreadable evidence skips without consuming a slot. Commit before invoking Orca. Preserve existing consumed keys. Eligibility is established only at the last completed refresh, not atomically with launch. |
| C-010 | HYBRID | 96 | AGREE with A on literal argv, fixed agent, existing absolute worktree, and origin validation. Probe executable identity through a mockable boundary; account for probe calls and deadlines. |
| C-011 | C | 99 | Timeout, malformed output, interrupted invocation, or unverified error becomes unknown with its slot consumed. Reconcile a known operation only through its stored operation ID and invocation context. Missing ID requires investigation. Expiry and explicit post-submission failure never authorize a fresh launch. |
| C-012 | HYBRID | 98 | AGREE with A. |
| C-013 | HYBRID | 95 | Trusted operator configuration admits human approvers by account ID after role verification. Reject missing/empty lists and unsafe ownership or write permissions, including writable parent paths. Display governance and update procedure. The template never silently supplies approval authority. |
| C-014 | HYBRID | 98 | Disable deployment until an owner-run test verifies slash-command execution and session permission policy, and the owner explicitly accepts live narrative-read risk and existing claim effects, including GitHub, local artifacts, and conditional ClickUp assignment. Bypass permissions require explicit written acceptance. |
| C-015 | HYBRID | 97 | Shared authentication, authorization, discovery, configuration, storage, or rate-limit failures halt further dispatch. Candidate-local unreadable or incomplete evidence skips that candidate. Preserve prior committed outcomes; do not promise retroactive zero launches. Report partial failure distinctly from a clean cycle. |
| C-018 | HYBRID | 96 | AGREE with A on lock, kill switch, and exit 75. Track last completed cycle separately from overlap audit timestamps; repeated overlaps must remain unhealthy. |
| C-020 | HYBRID | 96 | Provide `once --dry-run`, offline `status --json`, read-only `check-config`, and explicit `init-state`. Initialization is operator-controlled, never automatic during validation or polling. Status/runbook describe consumed-slot investigation. Defer reset; any later reset must explicitly acknowledge forfeiting the previous at-most-once guarantee. |
| C-023 | HYBRID | 94 | AGREE with A; add actual Orca reply/reconciliation validation, restart/restore and lock verification, Project ID/query compatibility, and account/approval governance before activation. |
| C-024 | HYBRID | 97 | Recognize the existing marker only with authenticated author-ID matching; project body inspection inside gh to structured evidence. Positive recognized evidence establishes posted claim, not artifact completion. Incomplete absence cannot permit dispatch. Assignment alone proves no claim; marker recognition never resets consumed keys. |
| S-001 | HYBRID | 96 | AGREE with A. |
| S-004 | HYBRID | 92 | Use A's trimmed module separation and mockable runner/store/launch boundaries; reuse existing helpers only where their effect and durability contracts fit. No routing registry, interchangeable backends, or audit plugin surface is required. Do not name a module `select`. |
| S-005 | HYBRID | 96 | Use one locked, versioned JSON document containing consumed keys and transitions. Persist via same-directory replacement with file and parent-directory durability verified on supported storage. Polling never initializes missing storage. Corrupt/incompatible state fails closed; initialization and restore require explicit operator procedures. |
| S-007 | HYBRID | 95 | AGREE with A; distinguish source-verified facts, proposed policies, and externally unverified adapter contracts. |
| S-008 | HYBRID | 94 | AGREE with A. |
| X-001 | HYBRID | 99 | Confirmed launch never permits another fresh submission. Missing claim evidence after the reporting threshold raises `claim_not_observed` without releasing the consumed slot. A later recognized marker may still establish claimed; threshold expiry is not proof the session stopped. |
| X-002 | C | 99 | A recovered record with committed consumed launch intent and no stored outcome becomes unknown; never submit fresh. Only unconsumed preflight work may retry. Absence of a marker or operation ID does not prove non-start. |
| X-003 | HYBRID | 99 | AGREE with A; storage loss and incompatible schema also fail closed. |
| X-005 | HYBRID | 98 | AGREE with A. |
| X-007 | HYBRID | 94 | AGREE with A's exit mapping and action table. Unknown launch or storage-integrity failure outranks ordinary transient errors; terminal output preserves all reasons. A partial cycle is never reported as clean success. |
| X-008 | HYBRID | 98 | AGREE with A; marker projection includes trusted author identity, not narrative content. |

**Already-agreed points needing precision:** C-003 retains issue-local Project reads plus configured Project/field/option IDs; C-016/X-006 persist server retry timing and stop further requests without erasing earlier outcomes. C-025 permits body inspection inside gh only for marker recognition. No request cap, record pruning, or rate-limit rule may discard consumed keys.

##### Shared-assumption changes

- **A-001 — QUALIFY, strengthened:** JSON is acceptable; persistence remains an external activation prerequisite, not something path validation proves. `once` and `check-config` never recreate the store. Whole-directory loss, cloned backups, and operator reinitialization remain guarantee hazards; a sentinel in the lost directory cannot detect them.
- **A-003 — REJECT, refined:** Separate identity from current display names. Pin owner/approver IDs and policy-object IDs; show readable bindings during setup/status. Name replacement can authorize a new object, not merely cause a harmless mismatch.
- **A-005 — QUALIFY, clarified after A/B disagreement:** Sole-assignee routing is stricter than the claim, which permits unassigned issues. Assignment is required at eligibility evaluation, not chronologically before approval. Document the human assignment step and audit `unassigned` skips.
- **A-007 — QUALIFY, made concrete:** Verify cross-process locking and replacement durability on supported persistent local storage. Existing helper reuse is insufficient evidence for host-failure durability; no cross-host exclusion follows.
- **A-010 — QUALIFY, hardened:** Trusted administrators may govern approval configuration; protection includes parent-directory replacement permissions, not just file mode. Updating authority is an explicit administrative action, never issue-controlled input.

A-002, A-004, A-006, A-008, and A-009 retain round-1 positions. Actor metadata proves application identity rather than human intent, and no marker-duration or clock assumption may reopen a consumed slot.

### Variant D Advocate (rebuttal)

#### Round 2 rebuttal: advocate D (devops lens: deployment, observability, runbooks, SLO impact)

##### 1. Responses to criticisms

This section covers the criticisms of variant D from round 1 (A, B, C, E) and from round 2 so far (A, B, C). Concessions come first, then defences.

**Conceded**

1. **FR-014 "any other non-zero exit gives `failed`" (A R2, C R1/R2).** Conceded in full. D counts `launches` on success, so an Orca call that started a session and then returned an error, or was killed by D's own 20 s subprocess timeout, comes back as a retryable `failed`. That is a duplicate-launch path. Adopt C: in the same atomic write as `pending`, increment `launches` durably before Orca is spawned. After the spawn, every outcome other than confirmed success is `unknown`. Only a failure *before* the spawn (no Orca found, prompt or worktree rejected) is a retryable `failed`, and it consumes nothing. D's own principle that a duplicate costs more than a missed launch (§7) requires this. My FR-014 broke that principle.
2. **Orca timeout of 20 s (A R1).** Conceded, as in round 1. Use 120 s for Orca and 20 s for `gh`. A timeout becomes `unknown`, per item 1.
3. **Pre-launch failure deletes the entry (A R1).** Conceded. Adopt the B/C order: refresh first, then commit `pending`, then invoke Orca. A failed refresh never writes an entry, so there is nothing to delete. The audit line keeps `revalidation_failed` as evidence (C-009 below).
4. **Approvers file shipped with the Coder template (A R1/R2, A-010).** Conceded. A template-shipped file turns approval authority into infrastructure-as-code that nobody reviews per workspace. The owner creates it, and `check-config` refuses one that is missing, empty, or group- or world-writable.
5. **`rate_remaining` has no source (E R1).** Conceded. `gh api` would need `--include` to expose `X-RateLimit-Remaining`, and no code in the repo does this (grep, §3 N4). Drop the field and keep `gh_calls` (E NFR-007). The rate-limit case is covered by exit 5 and a persisted next-permitted time.
6. **The 100-item `project item-list` cliff (E R1, B R1).** Conceded. D's own R3 admits the cliff, and raising the limit only moves it. Adopt E's per-issue `projectItems`.
7. **Exit 3 is overloaded and the fail-closed scope covers the whole cycle (B R1, A R1).** Conceded. Adopt A's X-007 table and A's C-015 split: shared inputs void the cycle, and per-issue reads skip only that issue.
8. **Repeated exit 75 counted as healthy (C R2, E R1).** Conceded. SLO (b), "≥99% of cycles exit 0 or 75", lets a hung cycle hold the lock forever while the SLO still reads green. Fix: `status` reports `last_completed_cycle_age_seconds`, a value that exit 75 never refreshes, and SLO (b) counts 75 as healthy only while that age stays under 900 s. Staleness (runbook step 6) then catches a wedged lock holder within three cycles.
9. **Removing an abandoned entry by hand needs a guarantee-reset warning (C R1/R2).** Conceded on the warning. My counter on deferral is in item 12.
10. **OD-7 "default interactive mode, never bypass" is not enforceable (B R1).** Conceded. No launch flag sets the mode (A-002). Replace it with A's C-014 gate: no cron is enabled until a live test records the mode, and bypass needs written owner acceptance.

**Defended**

11. **Flags-only interface with no config file (A R1).** Partly conceded. D has `check-config`, but D also lists every option as a flag. A config file plus `check-config` is the better operator surface, because cron lines stay short and the values are reviewable. I accept A's C-020 verbs, with C's read-only `check-config` (item 12).
12. **Reset should be deferred (C R2).** Contested. Deferral does not remove the reset; it just moves it into "edit `record.json` by hand", which happens without the lock, without an audit line and without a schema check. That is the worst form a reset can take, and an operator *will* hit it: `claim_not_observed` and `pending_orphan` are terminal by design. So the reset must exist as a verb, with C's safeguards. It works only on `abandoned`, takes the cycle lock, requires an explicit `--forfeit-guarantee` flag, prints that issue N may now be launched twice, and writes an audit line. That satisfies C's acknowledgement requirement and keeps the recovery inside a mechanism the system controls.
13. **Exit 75 rather than 0 for a held lock (A R1, E R1: "benign overlaps alert").** Defended. A single 75 is not an alert. The alert rule is staleness (item 8), not "any non-zero exit". 75 is `EX_TEMPFAIL` from BSD `sysexits.h`, which cron wrappers recognise as "try later". B and C now agree with this (B R2 item 9; C C-018 AGREE).
14. **Runbook, `DISABLED` kill switch, 24 h shadow `--dry-run`, staleness rule.** No variant criticised these. A's X-007 ruling and A's C-023 adopt the action-per-exit-code idea. I add the shadow dry-run as an activation gate (C-023 below).
15. **SLO (c), "≥95% of `launched` reach `claimed` within the lease" (C R1: SLO success must not hide unknowns).** Defended with a fix. SLO (c) is the only production detector for R1 (the slash command does not run from `--prompt`). Add an SLO (d): no `unknown` or `pending_orphan` entry stays unacknowledged for more than 24 h. With (d) in place, success on (c) cannot hide them.

##### 2. Changed views on other variants

- **C** is now my reference for the at-most-once core. "Consume before I/O, and expiry never releases a consumed slot" fixes the hole in D's FR-014 that I missed in round 1. I still reject SQLite: one JSON file, written with the existing helper plus a directory fsync, meets C's integrity properties (S-005). I also reject C's "bounded comment content" (X-008).
- **A** produced the most usable merged rulings. I take A's text on 18 of the 28 points. The one place I break from A is C-009: A writes `pending` first and then deletes the entry, and B and C show that ordering is unnecessary.
- **B** conceded every dangerous rule it had: a corrupt record reset to empty, a relaunch after the lease, and the label-only mode. B's page-counting rule (N1) reconciles complete event histories with E's 35-call cap, so I now vote B on C-006 and C-024.
- **E** fixed the scaling defect that every variant, mine included, shared: per-issue `projectItems`. E's daily cap of 6 is the right blast-radius limit for a selection bug, and an operator can read it straight off the audit.

##### 3. New evidence (checked read-only this round)

- **N1. `write_prepared_bytes` already gives 0600 files and fsyncs the file but not the directory.** `src/superclaude/cli/swarm/atomic.py:22-32` creates the temp file with `tempfile.mkstemp` in the target directory, fsyncs it at `:31` and calls `os.replace` at `:32`. `mkstemp` creates the file with mode 0600, and `os.replace` keeps that mode. So D's NFR-012 (atomic writes, mode 0600) needs no new code. No `fsync` of the parent directory exists (only line 31 matches `fsync`), which confirms C's E1. The fix is a small wrapper in `issue_watch/record.py` that fsyncs the directory after the replace. `swarm` itself stays unchanged.
- **N2. A Python `fcntl.flock` precedent exists in installed hooks, not in package code.** `src/superclaude/hooks/scripts/launch-job-identity.sh:146` uses `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` in embedded Python, and `:461-462` refuses any platform other than Linux, or a missing `fcntl`, with `unsupported platform`. `ccsession:415` uses the same call. This qualifies A's E6 ("no Python flock"): the non-blocking form is house practice, and so is refusing when it is unavailable. The watcher's lock should copy both and exit 2 on a platform without flock. That is a pre-flight check an operator can see, not a silent run with no lock.
- **N3. Nothing in `src/superclaude` uses exit 75 or `os.EX_*`** (grep for `EX_TEMPFAIL|exit(75)|return 75|os.EX_` finds nothing). 75 is therefore a new contract for this package, as C's §8 says of all its codes, not a reuse of an existing one. It must be written into the design-doc exit table.
- **N4. No code reads GitHub rate-limit headers.** A case-insensitive grep for `X-RateLimit|rate_limit|ratelimit` finds only unrelated hits: ClickUp's `rate_limited` reason in `sc-issue-protocol/scripts/clickup_claim.py:56,123` and the Anthropic gateway's `rate_limit_error`. This supports conceding `rate_remaining` (item 5). It also shows that `clickup_claim.py` returns `rate_limited` as a reason string, not a dedicated exit code (`:56-58`), so the watcher's exit 5 is a separate, new decision.
- **N5. `_find_orca` cannot be stubbed through an injected runner as written.** `install_user_setup.py:205` calls `shutil.which` and `:209-215` calls `subprocess.run([path, "skills", "list", "--json"], ..., timeout=10)` directly. This confirms C's E2. The C-010 ruling needs the probe to go through the injected runner, either by moving its logic into a runner-taking helper or by wrapping it. It also needs the 10 s probe counted in the cycle's time budget. Separately, I confirmed `poll-augment-review.sh:46-56` (B's N1): explicit `per_page=100` pages, `--method GET`, "fail incomplete at the cap".

##### 4. Updated positions

"AGREE with X" means I accept advocate X's round-2 ruling exactly as written.

| Point | Superior variant | Confidence % | Merged ruling or AGREE with X |
|---|---|---|---|
| C-001 | HYBRID | 75 | AGREE with A. Matching by name fails closed on a rename, and creating labels needs write access. Label node IDs would add a resolve call and a config surface without closing a real gap, because the approval actor check carries the trust. |
| C-004 | HYBRID | 80 | AGREE with A. The claim assigns and checks by login (`@me`), and the login is re-read each cycle from the same token, so login routing stays consistent with the claim. |
| C-005 | HYBRID | 85 | AGREE with A |
| C-006 | HYBRID (E+B) | 85 | AGREE with B |
| C-007 | HYBRID (A+C) | 90 | A's fields and states. `launches` is incremented in the same durable write as `pending`, before Orca is spawned; a fresh launch requires `launches == 0`. Re-labelling, re-approval, lease expiry and login change never reset it; only `reset <N> --forfeit-guarantee` does. |
| C-008 | HYBRID | 80 | AGREE with A |
| C-009 | HYBRID (B/C order) | 85 | Under the lock, re-read state, labels, assignees, approval and Project Status. A failed or unreadable re-read skips `revalidation_failed`, writes no entry, launches nothing. Only then durably write `pending` with `launches` incremented, then call Orca. A `pending` at cycle start becomes `abandoned` `pending_orphan`. |
| C-010 | HYBRID (A+B+C) | 85 | AGREE with A, plus: `_find_orca`'s probe runs through the injected runner (today it calls `subprocess.run` directly) and its 10 s timeout counts toward the cycle time budget. |
| C-011 | C | 90 | Any outcome after Orca is spawned other than confirmed success (timeout, malformed output, `agent_session_operation_unknown`, non-zero exit) is `unknown`, with the slot consumed. With an `operationId`, only `--retry-launch <id>` from the stored cwd; without one, `abandoned`. Retryable `failed` covers only pre-spawn failures. |
| C-012 | HYBRID | 90 | AGREE with A |
| C-013 | HYBRID (C IDs) | 85 | AGREE with A |
| C-014 | HYBRID | 85 | AGREE with C |
| C-015 | HYBRID | 85 | AGREE with A |
| C-018 | D | 90 | A's text, plus: `status` also reports `last_completed_cycle_age_seconds`, which exit 75 never refreshes. An age above 900 s is unhealthy whatever the exit codes, so repeated overlaps raise an alert. |
| C-020 | HYBRID (A+C+E) | 75 | Verbs: `once [--dry-run]`, `status [--json]`, read-only `check-config`, `init-state` (creates the store and refuses if one exists), and `reset <N> --forfeit-guarantee` (only on `abandoned`, under the lock, audited, prints that N may launch twice). Exit codes as in X-007. |
| C-023 | HYBRID (A+D) | 80 | AGREE with A, adding three activation gates before cron is enabled: a 24 h shadow `--dry-run` whose audit is reviewed, a two-process lock test on the real state directory, and the staleness alert (`last_completed_cycle_age_seconds` > 900) wired up. |
| C-024 | HYBRID | 85 | AGREE with B |
| S-001 | HYBRID | 70 | AGREE with A |
| S-004 | HYBRID | 75 | AGREE with A |
| S-005 | HYBRID (D form, C init) | 85 | One versioned JSON record file per state directory, written with `write_prepared_bytes` (0600) plus a parent-directory fsync. Only `init-state` creates it. If it is missing after init, unparseable or of unknown version, `once` exits 6 with no launch and leaves the file untouched. No SQLite. |
| S-007 | B | 70 | AGREE with A |
| S-008 | HYBRID | 65 | AGREE with A |
| X-001 | D | 90 | AGREE with A, plus: a later own marker still moves the `abandoned` entry to `claimed`, and `claim_not_observed` never releases the consumed slot. |
| X-002 | D | 85 | AGREE with A. Under C-007 the slot is already consumed, so C's `unknown` and D's `abandoned` block equally; `pending_orphan` names the cause for the operator. |
| X-003 | D | 95 | AGREE with A |
| X-005 | D | 90 | AGREE with A |
| X-007 | HYBRID | 85 | AGREE with A. Exit 6 also covers a store that is missing after `init-state`. |
| X-008 | HYBRID | 85 | AGREE with A |

Reasons for the non-AGREE rows:

- **C-007 and C-011** carry C's consume-before-spawn rule. Without it, D's own FR-014 relaunches a session that Orca started but timed out on.
- **C-009** uses the B/C order. A's write-then-delete creates an extra `pending_orphan` source, a crash during a re-read that fails, and with it an operator ticket for an issue that was never launched.
- **C-018** separates "the lock was held" from "work completed". Otherwise the observability SLO is blind to a wedged holder.
- **C-020** keeps the reset as an audited verb. A deferred reset becomes an unlocked hand edit of the record.
- **S-005** is A's form plus C's directory durability and explicit init. N1 shows the directory fsync is missing from the helper we reuse.


##### 5. Shared-assumption changes

Only the assumptions whose answer changed since my round 1 are listed here. A-002, A-004, A-005, A-008 and A-010's core answer are unchanged except where noted.

- **A-001 (state survives restarts):** QUALIFY, tightened. Only `init-state` creates the store; a missing store after init exits 6 and never starts empty, so losing `$HOME` stops dispatch instead of duplicating launches. A cleared state directory can only be recovered by a re-init followed by owner review of the open `launched` issues.
- **A-003 (logins and names stable):** changed from a partial REJECT to a split ACCEPT. Owner routing stays by login, because the claim works by login (`refs/claim.md:41-42`, B's N4) and the login is re-read each cycle. Approvers are keyed by account ID (C-013), so a rename cannot transfer approval trust. Label names stay names and fail closed (C-001).
- **A-006 (wall clock trustworthy):** QUALIFY, narrowed. Only the rolling 24 h cap, the backoff and the lease report depend on the clock. A jump can only delay launches, or let at most one extra launch through the daily cap. It can never relaunch an issue, because `launches == 0` and `abandoned` are terminal states that do not depend on the clock. The `status` view reports ages computed from the clock, so a skew shows up there first.
- **A-007 (`flock` effective):** QUALIFY, made checkable. The house lock helper already refuses a non-Linux platform or a missing `fcntl` (`launch-job-identity.sh:461-462`). The watcher does the same and exits 2. A local, single-host state directory is a documented precondition, and A's two-process lock test on the real directory is an activation gate (C-023).
- **A-009 (marker within lease):** changed from QUALIFY to REJECT-as-safety-input. Under X-001 and X-002 the lease is only a reporting threshold that moves the entry to `abandoned` `claim_not_observed`, and a later marker still moves it to `claimed`. No at-most-once property depends on it, so a slow Wave 4 costs a status line, not a duplicate session.
- **A-010 (allow-list file owner-only):** QUALIFY, unchanged on permissions (group- or world-writable gives `check-config` exit 2). Changed on provenance: the template does not ship the file, the owner creates it, it holds account IDs, and an empty file means no approvers rather than "anyone".


### Variant E Advocate (rebuttal)

#### Round 2 rebuttal: advocate E (performance lens: bottlenecks, scaling, cost-to-serve)

Read: blind/variant-A..E, diff-analysis.md, round1-advocate-A..E, round1-tally.md, round2-advocate-A..D. I go last. Blind rules held: I opened nothing outside `adversarial/`, so code facts below are marked as relayed from another advocate unless they are arithmetic on spec values.

##### 1. Responses to criticisms

**Conceded (with the fix I now support)**

1. **FR-006 is one unpaginated events call, and the 33-call arithmetic ignores paging (B, C).** Conceded. Complete approval history may need several pages. Fix is B's N1 rule (the `poll-augment-review.sh` pattern): explicit `per_page=100` pages, each page counts toward the cap, a cap reached mid-issue skips that issue as `budget_exhausted`, incomplete evidence is never positive. The hard cap stays 35, so worst case is now a hard bound, not an estimate: 12 cycles x 35 = 420 calls/h = 8.4% of 5,000/h on one login. Idle stays 2 calls (24/h, 0.48%).
2. **Per-issue record files `records/<N>.json` (S-005; A, C, D).** Conceded. One versioned JSON document needs one durable write for slot plus counter. Per-issue files cannot make "slot consumed and `launches` incremented" atomic with a day-cap count across issues, and a missing directory is harder to detect than a missing file. I adopt D's S-005 text.
3. **30-day pruning of terminal records (NFR-013; C).** Conceded as unsafe: pruning an `abandoned` entry re-opens an issue that may have a live session. Compact terminal entries to tombstones (key, state, timestamps) and never delete a consumed key. Growth cost: roughly 100 bytes per launched issue, so 1,000 issues is about 100 KiB. Pruning saves nothing worth the risk. The `considered` cap of 1000 goes too.
4. **FR-012 leaves a removed issue "deleted or marked abandoned" (A, B, D).** Conceded. Adopt B/C/D order: re-read first, a failed re-read writes no entry (audit `revalidation_failed`), then durable `pending` with `launches` consumed, then Orca.
5. **`--agent <agent>` (X-008).** Withdrawn in round 1, still withdrawn.
6. **GraphQL is POST, so "every call is GET" rejects my FR-008 (B).** Conceded. Adopt A's wording: no REST write verb, no `mutation`; queries are module constants and a test scans them.
7. **`claimed` needs own assignee AND marker (A).** Conceded. The marker by the own login is the claim's evidence; assignment alone is none. Marker alone gives `claimed` (A/B C-024).
8. **Orca-worker detector rests on an ASSUMPTION (A, D).** Dropped. It is not needed once cron stays disabled until the live test.
9. **`~/.superclaude/` state path (D).** Conceded. Use a state directory under the XDG state path, local filesystem only.
10. **Corrupt record unspecified (D).** Conceded. Exit 6, no launch, never reset.
11. **`reset <N>` without a guard (C).** Conceded. D's form: `--forfeit-guarantee`, only `abandoned`, under the lock, audited.

**Defended**

12. **Daily cap of 6 is "speculative" (A R1).** Defended as a cost bound on a selection bug, now defined as a [PROPOSAL] counted from stored launch timestamps (no separate counter that can drift) and surviving tombstoning. A and D now accept it. It needs owner sign-off because it can delay legitimate work; the poller must report `day_cap_reached` so the delay is visible.
13. **Prefilter before per-candidate calls (FR-004).** No one attacked it; B and C now require it in C-006. It is the main reason idle cost is 2 calls.
14. **Per-issue `projectItems`.** Adopted by all variants; scale is candidates (at most 10 per cycle), not Project size.

**Cost-model gap I found in my own text (new, not raised by others)**

15. **A call cap is not a time cap.** 35 calls at a 20 s `gh` timeout is 700 s, more than a 300 s cadence; a 120 s Orca launch plus a 10 s probe adds more. The spec needs a wall-clock budget: reads end at 240 s with exit 3; no launch is started after 120 s elapsed; the Orca probe and re-read count inside it. The non-blocking lock means overlap exits 75 rather than double work.

##### 2. Changed views

- **C.** Consume-before-spawn is the only rule that makes at-most-once true at every crash point. I take it, but in D's JSON form; SQLite buys nothing for a few hundred bytes of state.
- **D.** Best operations spec, and D's concessions made it safer. I take exit 75, `DISABLED`, `last_completed_cycle_age_seconds`, the shadow dry run, `--forfeit-guarantee`.
- **B.** Page counting settles my biggest conflict (complete history versus 35 calls). B's origin check and Orca probe are correctness, not hardening.
- **A.** Its round-2 rulings are the best merge text on 18 or more points; I AGREE with A wherever A and D agree.
- **My own variant.** E wins on C-003 and C-006 only. On state, recovery, and operability E was the weakest variant.

##### 3. New evidence

No file outside `adversarial/` was opened (blind rules). Items marked "relayed" were checked by the named advocate, not by me.

- **N1 (arithmetic, mine).** Hard bounds with the 35-call cap: idle 2 calls/cycle; worst 35. One login, W workspaces: idle 24W/h, worst 420W/h. W=5 gives 120 idle (2.4%) and 2,100 worst (42%) of 5,000/h. A 12th always-busy workspace on the same login would exceed 100%; same-login multi-enablement is therefore a cost problem as well as a duplicate-launch problem, and `host` plus `login` in every audit line matters (C-005).
- **N2 (arithmetic, mine).** Cycle time as in item 15: unbounded by call count alone. Needs the 240 s deadline.
- **N3 (arithmetic, mine).** State growth: tombstones about 100 bytes each; 1,000 launched issues is about 100 KiB, read in full every cycle. That is negligible next to one `gh` call, so no pruning is justified.
- **N4 (relayed, B).** `poll-augment-review.sh:46-56` already fails closed at a page cap; no `--paginate` elsewhere in the package. The pattern is house practice.
- **N5 (relayed, A/D).** `write_prepared_bytes` (`swarm/atomic.py:14-39`) gives 0600 and file fsync but no directory fsync, so a thin wrapper must fsync the parent directory. `_find_orca` (`install_user_setup.py:198-221`) calls `subprocess.run` directly with a 10 s timeout; it must go through the injected runner, and its 10 s counts in the cycle budget (D N5).
- **N6 (relayed, D).** No code in the package reads rate-limit headers, so `rate_remaining` has no source. Keep the idle cycle at exactly 2 calls: do not add a `rate_limit` call to learn the budget.

##### 4. Updated positions (all 28 UNRESOLVED points)

"AGREE with X" = accept advocate X's round-2 ruling exactly as written.

| Point | Superior variant | Confidence % | Merged ruling or AGREE with X |
|---|---|---|---|
| C-001 | HYBRID | 75 | AGREE with A (names, fail closed; D agrees). Label IDs are a follow-up, not v1. |
| C-004 | HYBRID | 80 | AGREE with A |
| C-005 | HYBRID | 85 | AGREE with A, plus: audit lines carry `host` and `login`; N1 shows W workspaces on one login multiply cost by W. |
| C-006 | HYBRID (E+B) | 90 | AGREE with B (page counting; 35-call cap includes every page; cap mid-issue skips `budget_exhausted`). Idle cycle is exactly 2 calls: login read plus discovery. |
| C-007 | D | 85 | AGREE with D (`launches` consumed in the same durable write as `pending`, before Orca; re-labelling never resets; only `reset <N> --forfeit-guarantee`). |
| C-008 | HYBRID | 70 | [PROPOSAL] lease 60 min (report threshold only), `max_attempts` 3, one launch per cycle, `max_candidates` 10, 10-min backoff after `failed`, `gh` 20 s, Orca 120 s, 240 s cycle deadline. Day cap 6 per rolling 24 h from launch timestamps; owner must approve. |
| C-009 | HYBRID | 85 | AGREE with D (re-read first, failed re-read writes no entry, then durable `pending`, then Orca; orphan `pending` becomes `abandoned`). Re-read adds one Project call per launch inside the 35 cap. |
| C-010 | HYBRID | 85 | AGREE with D (A's argv, `_find_orca` through the injected runner, probe 10 s counted in the cycle budget, origin must be IronbellyOrg/IronClaude). |
| C-011 | C | 90 | AGREE with D (anything after spawn other than confirmed success is `unknown`; `--retry-launch <id>` only with an id; otherwise `abandoned`). |
| C-012 | HYBRID | 90 | AGREE with A |
| C-013 | HYBRID | 85 | AGREE with A |
| C-014 | HYBRID | 85 | AGREE with C |
| C-015 | HYBRID | 85 | AGREE with A |
| C-018 | D | 90 | AGREE with D (lock held exits 75, `DISABLED` exits 0 before any call, `last_completed_cycle_age_seconds` above 900 is unhealthy). |
| C-020 | HYBRID | 75 | AGREE with D (`once [--dry-run]`, `status [--json]`, read-only `check-config`, `init-state`, `reset <N> --forfeit-guarantee`). I reject A's "check-config creates the store": a check verb must not write. |
| C-023 | HYBRID | 80 | AGREE with D (A's list plus 24 h shadow dry run, two-process lock test, staleness alert as activation gates). |
| C-024 | HYBRID | 85 | AGREE with B (all comment pages, `--jq` boolean only, incomplete read is not evidence, marker alone gives `claimed`). |
| S-001 | HYBRID | 70 | AGREE with A |
| S-004 | HYBRID | 75 | AGREE with A (module name `select` withdrawn). |
| S-005 | HYBRID | 90 | AGREE with D (one versioned JSON, `write_prepared_bytes` plus parent-directory fsync, only `init-state` creates it, exit 6 if missing, unparseable or unknown version). Terminal entries become tombstones, never deleted. |
| S-007 | B | 70 | AGREE with A |
| S-008 | HYBRID | 65 | AGREE with A |
| X-001 | D | 90 | AGREE with D (A's text plus a later own marker moves `abandoned` to `claimed`; the consumed slot is never released). |
| X-002 | D | 90 | AGREE with A |
| X-003 | D | 95 | AGREE with A |
| X-005 | D | 90 | AGREE with A (no label-only or Project-off mode; per-issue `projectItems`). |
| X-007 | HYBRID | 85 | AGREE with A (0 ok/disabled; 2 usage/config; 3 auth/scope/timeout/non-JSON; 4 truncated; 5 rate limited; 6 record; 7 launch failed/unknown; 75 lock). Deadline overrun is exit 3. |
| X-008 | HYBRID | 90 | AGREE with A |

##### 5. Shared-assumption changes

Only assumptions whose answer changed since my round 1.

- **A-001:** QUALIFY, tightened. Only `init-state` creates the store; missing after init exits 6. Per-issue files are withdrawn because a missing directory is harder to detect than a missing file.
- **A-003:** changed to split ACCEPT. Owner routing stays by login (the claim works by login); approvers by account ID; label names fail closed.
- **A-004:** QUALIFY, now with a cost argument: W workspaces on one login cost W times the budget (N1), so one enabled workspace per login is a cost limit as well as a duplicate-launch limit.
- **A-006:** QUALIFY, narrowed. Clock jumps affect only the 24 h cap, backoff and lease report; no state is relaunched because of time.
- **A-009:** changed from QUALIFY to REJECT as a safety premise. The lease is a reporting threshold only.
- **A-011 (new, mine):** a call cap implies a time bound. It does not; the spec must add a wall-clock deadline (item 15).

## Round 2 tally



Rule: a point is AGREED when at least 4 of 5 advocates give the same answer in their latest statement (letter, H = HYBRID, N = NONE). For the 10 shared assumptions (A-NNN) agreement means at least 4 of 5 advocates ACCEPT or QUALIFY (keep with conditions) rather than REJECT.

| Point | Level | Round used | Votes (A B C D E) | Leading | Count | Status |
|---|---|---|---|---|---|---|
| C-001 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-002 | L3 | 1 | H H C H H  | H | 4 | AGREED |
| C-003 | L3 | 1 | E E H E E  | E | 4 | AGREED |
| C-004 | L3 | 2 | H A C H H  | H | 3 | OPEN (majority 3/5) |
| C-005 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-006 | L3 | 2 | E H H H H  | H | 4 | AGREED |
| C-007 | L3 | 2 | H D H H D  | H | 3 | OPEN (majority 3/5) |
| C-008 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-009 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-010 | L2 | 2 | H H H H H  | H | 5 | AGREED |
| C-011 | L3 | 2 | C C C C C  | C | 5 | AGREED |
| C-012 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-013 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-014 | L2 | 2 | H H H H H  | H | 5 | AGREED |
| C-015 | L3 | 2 | H C H H H  | H | 4 | AGREED |
| C-016 | L3 | 1 | H H H H H  | H | 5 | AGREED |
| C-017 | L2 | 1 | D D H D D  | D | 4 | AGREED |
| C-018 | L3 | 2 | D D H D D  | D | 4 | AGREED |
| C-019 | L2 | 1 | D H H H H  | H | 4 | AGREED |
| C-020 | L2 | 2 | H H H H H  | H | 5 | AGREED |
| C-021 | L2 | 1 | A A H A A  | A | 4 | AGREED |
| C-022 | L2 | 1 | H H H H H  | H | 5 | AGREED |
| C-023 | L2 | 2 | H H H H H  | H | 5 | AGREED |
| C-024 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| C-025 | L2 | 1 | H H H H E  | H | 4 | AGREED |
| S-001 | L1 | 2 | H H H H H  | H | 5 | AGREED |
| S-002 | L1 | 1 | N N N N N  | N | 5 | AGREED |
| S-003 | L2 | 1 | H H H H H  | H | 5 | AGREED |
| S-004 | L2 | 2 | H A H H H  | H | 4 | AGREED |
| S-005 | L3 | 2 | H H H H H  | H | 5 | AGREED |
| S-006 | L1 | 1 | N N B N N  | N | 4 | AGREED |
| S-007 | L1 | 2 | B B H B B  | B | 4 | AGREED |
| S-008 | L1 | 2 | H H H H H  | H | 5 | AGREED |
| X-001 | L3 | 2 | D D H D D  | D | 4 | AGREED |
| X-002 | L3 | 2 | D D C D D  | D | 4 | AGREED |
| X-003 | L3 | 2 | H D H D D  | D | 3 | OPEN (majority 3/5) |
| X-004 | L3 | 1 | C H C C C  | C | 4 | AGREED |
| X-005 | L3 | 2 | H D H D D  | D | 3 | OPEN (majority 3/5) |
| X-006 | L3 | 1 | H H C H H  | H | 4 | AGREED |
| X-007 | L2 | 2 | H H H H H  | H | 5 | AGREED |
| X-008 | L2 | 2 | H H H H H  | H | 5 | AGREED |
| A-001..A-010 | - | 1+2 | see round files | QUALIFY/ACCEPT | A-009: 3/5 non-reject; others 4-5/5 | 9 AGREED, A-009 OPEN |

## Round 2.5: Invariant Probe

Full table in invariant-probe.md (27 findings; 6 HIGH, 15 MEDIUM, 3 LOW unaddressed, 3 addressed).

## Round 3: Final Arguments

### Variant A Advocate (final)

#### Round 3: advocate A (architect; maintainability and extension seams)

Read: invariant-probe.md (complete, including Proposed rulings), rounds/round2-tally.md, rounds/round2-advocate-A, C, D (full) and B, E (rulings for the open points and A-009). Code checked read-only: `src/superclaude/skills/sc-issue-protocol/refs/claim.md`, `scripts/origin_repo.py:86-164`, `src/superclaude/skills/sc-pr-submit-protocol/scripts/poll-augment-review.sh:46-77`.

Code facts used below:

- F1. The claim edits its earlier marker comment in place (`claim.md:29`, `:43`, `:84-88`), so a marker's creation time can predate the current approval while its edit time does not.
- F2. The claim reads origin with `git remote get-url origin` (`origin_repo.py:156-160`, which expands `insteadOf`) and parses it with `parse_origin_url` (`:86-99`): https or `git@` forms only, `.git` stripped, case-sensitive patterns.
- F3. The house paging pattern uses explicit `per_page=100` pages, stops at a short page, rejects repeated IDs and fails incomplete at a cap (`poll-augment-review.sh:48-77`).
- F4. Claim Wave 2 checks only PR, closed and assignee (`claim.md:39-43`), never approval or edits.

##### Findings table

| INV id | Verdict | Final ruling or residual-risk statement | Reason (one line) |
|---|---|---|---|
| INV-001 (H) | MODIFY | The Orca probe, prompt build and origin check run before the `pending` write; their failure writes no entry (exit 2, or a per-issue skip). After `pending`, the only outcomes are `launched`, `unknown`, `abandoned` or `claimed`. State `failed`, `max_attempts` and the 10-minute backoff are deleted. | Once every pre-spawn check precedes the write, `failed` has no producer; a state and two knobs nothing reaches are maintenance debt and false test surface. |
| INV-002 (H) | ACCEPT | As proposed: a non-zero Orca exit after the spawn, including a definite error body, is `unknown` with the slot consumed. My round-2 phrase "definite Orca error gives retryable `failed`" is withdrawn. | It was my text, and it is the duplicate path D conceded; error text proves nothing about whether a session started. |
| INV-003 (H) | MODIFY | `--retry-launch` runs automatically only for `unknown` with an operationId, as the cycle's one launch, after the C-009 re-read, origin and `DISABLED` checks pass, before 120 s. At most 3 tries (`retries`), never `launches`; negative re-read or exhaustion gives `abandoned`. Off until the C-023 live test. | Orca's retry rule is UNVERIFIED (Q3), so the behaviour is gated on evidence; reusing the existing per-cycle launch slot adds no new budget concept. |
| INV-004 (M) | MODIFY | `unknown` with an operationId leaves only through an own marker (`claimed`), retry exhaustion or a negative re-read (`abandoned`), or `reset <N> --forfeit-guarantee`. Without an id it becomes `abandoned` at once. The lease drives no transition; `status` lists every `unknown` older than 24 h. | Adds the reset exit needed while retries are off (INV-003) and D's SLO (d) visibility; consistent with A-009. |
| INV-005 (M) | MODIFY | `once --dry-run` takes the lock, performs every read against an in-memory copy of the store, and reports each transition and launch it would make in audit lines marked `dry_run`. The store, rate-limit time and health age stay byte-identical; Orca is never called. | The C-023 shadow review reads the audit, so dry runs must write audit lines; a no-op must not refresh health. |
| INV-006 (M) | MODIFY | A cycle with several outcomes exits with the first applicable code in the order 6, 7, 2, 3, 5, 4; its audit line lists every reason. Only exit 0 from a cycle that was not `DISABLED` refreshes `last_completed_cycle_age_seconds`; `status` reports `disabled` separately. | An `unknown` launch is a possible duplicate needing a human, so it outranks transient read failures (C's R2 point); 4 never looks healthy. |
| INV-008 (M) | ACCEPT | As proposed: eligible only when the latest approval `labeled` event postdates the latest trigger `labeled` event, ordered per INV-009; a trigger re-added after approval needs a fresh approval. | Uses events already paged; zero extra calls; binds the human act to the current trigger. |
| INV-009 (M) | MODIFY | Every paged read follows `poll-augment-review.sh` `fetch_rest`/`fetch_threads`: explicit REST pages of 100 or GraphQL cursors, stop at the last page; a repeated ID or cursor, or reaching the call cap, marks the read incomplete (skip). Events order by (`created_at`, `id`). | Reuse the house pattern (F3) instead of a new one; event-ID monotonicity is UNVERIFIED, so the timestamp is the primary key and the ID breaks ties. |
| INV-010 (M) | MODIFY | In the C-009 re-read only, one call to `repos/IronbellyOrg/IronClaude/collaborators/<login>/permission` must return the approver's account ID and a role of triage or higher, else skip `approver_not_current`. Endpoint access UNVERIFIED. Residual: a compromised approver who keeps the role still passes. | One call per launch, not per candidate; gives central revocation without editing every workspace's allow-list file. |
| INV-011 (M) | MODIFY | The origin check runs `git -C <abs> remote get-url origin`, parses it with the rules of `origin_repo.parse_origin_url`, and compares owner/repo case-insensitively. It repeats immediately before every spawn and retry. A parity test pins both parsers to one fixture table. | The claim's own resolver (F2) decides the write target, so the watcher must compute the same answer; the parity test stops the two drifting. |
| INV-012 (M) | ACCEPT | As proposed: re-check `DISABLED` immediately before each `pending` write and each `--retry-launch`; if present, start nothing further, record the cycle, exit 0. | Local stat, no cost; makes the kill switch work during an incident. |
| INV-014 (M) | MODIFY | Discovery adds `--assignee <own login>`, so the 100-result exit 4 counts only own-assigned trigger issues. C-004's exact-set check still runs locally. The `unassigned` skip reason is removed, and the setup guide says to assign before approving. | Moves the cliff to one person's own open backlog; states honestly the visibility signal this costs. |
| INV-015 (M) | MODIFY | Each examined issue stores `last_examined_at`, including `budget_exhausted` and `revalidation_failed` skips; candidates run oldest first. Six of the 35 calls are reserved for the single pre-launch re-read. `max_candidates` defaults to 8; budget exhaustion ends the candidate loop, never the reserved re-read. | The probe priced the re-read per candidate, but it runs once per cycle (one launch): 2 + 3×8 + 6 = 32 ≤ 35. 10 does not fit; 5 is needlessly low. |
| INV-016 (M) | ACCEPT | As proposed: count every entry whose `pending_at` lies in the last 24 h, in any state; refuse when the count is already 6; `--retry-launch` adds nothing. | Counts consumed slots whatever their outcome; one meaning, testable with a fake clock. |
| INV-017 (M) | ACCEPT | As proposed: each `gh` and probe call times out at the lesser of its configured value and the time left before 240 s; a started launch is never cut short and its record is written before exit. | With C-008's "no launch after 120 s" the launch ends by 240 s; exit precedence (INV-006) stops an overrun masking 7. |
| INV-018 (M) | ACCEPT | As proposed: exactly one item in the configured Project node ID with Status option Backlog, over all `projectItems` pages; other Projects ignored; none or several skips `project_mismatch`. Field and option stay matched by name and fail closed on a rename, as C-001 does for labels. | Removes the unrelated-Project false positive; one config value; consistent with the name-matching decision. |
| INV-019 (M) | ACCEPT | As proposed: `once` exits 2 before any `gh` call when the approver file is missing, empty or unsafe. | Same check `check-config` already runs; a misconfigured watcher must never read healthy. |
| INV-021 (M) | MODIFY | An own marker counts as `claimed` evidence only if the comment's creation or last edit is later than the entry's `pending_at`, or, with no entry, later than the current approval event. An older marker leaves the issue eligible. Residual: a hand-run claim racing a watcher launch. | The claim edits old markers in place (F1), so the edit time is the signal; the hand-run race cannot be seen before Wave 6 and is documented ("do not hand-run `--claim` on a trigger-labelled issue while enabled"). |
| INV-024 (H) | MODIFY | `init-state` records `created_at`; approval events older than it never count, so a re-created store re-dispatches nothing earlier (the owner re-labels to re-arm). Restoring a store from backup is unsupported; recovery is always `init-state`. Two enabled workspaces on one login remain a documented residual. | Closes path (5) mechanically; paths (6) and (7) cannot be detected without a shared service, which D1 excludes, so they are named residuals, not silent ones. |
| INV-026 (H) | MODIFY | After the C-024 marker check, skip `edited_after_approval` if the body or any comment was created or last edited (GraphQL `lastEditedAt`, UNVERIFIED), or a `renamed` event occurred, after the approval event. Edits after the final re-read are an accepted residual under C-014. | The timestamps come from the comment pages and events already read for C-024 and C-002, so no new call class; titles are covered by `renamed` events. |
| INV-027 (H) | MODIFY | No verb deletes or replaces `<state_dir>/lock`; only `init-state` creates it and `once` never does. After `flock` succeeds, `once` compares the descriptor's device and inode with a fresh `stat` of the path; a mismatch or missing file exits 6. `check-config` refuses network filesystems (NFS, CIFS). | The inode comparison closes the unlink race mechanically instead of relying on operator discipline; the filesystem check turns A-007's precondition into a test. |

LOW findings (not required): INV-007 is closed for free by the `consumer_id` field in C-007 below. INV-022 is mitigated by INV-015, because a `revalidation_failed` issue moves to the back of the queue. INV-023 is accepted as a documented residual: nothing after the re-read can stop a started session (F4), and `DISABLED` stops only later launches.

##### Open points table

| Point | Final ruling (at most 45 words) |
|---|---|
| C-004 | The intended owner is an issue whose assignees equal exactly {own}, matched by login and node ID from one `gh api user` call per cycle, as `claim.md:41-42` requires. Other sets skip `assigned_other`. The rule is the pure function `is_intended_owner`; discovery pre-filters by `--assignee` (INV-014). |
| C-007 | States: pending, launched, unknown, abandoned, claimed. Fields: `launches`, `retries`, `operation_id`, `approver_id`, `approval_event_id`, `consumer_id`, `launch_cwd`, `pending_at`, `last_examined_at`, `last_reason`. `launches` increments in the `pending` write; a fresh launch requires 0; only `reset <N> --forfeit-guarantee` clears it. |
| X-003 | An unparseable store, an unknown `schema_version`, or a store or lock file missing after `init-state` gives exit 6 and zero launches, and the files are left unchanged; nothing resets them to empty. Recovery: move the directory aside, run `init-state` (its `created_at` gate, INV-024, blocks earlier approvals). |
| X-005 | There is no label-only mode and no mode that turns the Project check off. Membership and Backlog come from the issue's own `projectItems` in the configured Project node ID (INV-018). An unreadable item skips that issue; a missing `read:project` scope voids the cycle with exit 3. |
| A-009 | REJECT as a safety premise. The lease only decides when `launched` is reported `claim_not_observed` and moved to `abandoned`. Lease expiry never relaunches, retries or releases a slot, and a later own marker still gives `claimed`. A wrong lease value causes reporting noise only. |

Notes on the open points. C-004: matching the node ID as well as the login concedes C's rename point at zero cost, because `gh issue list --json assignees` already returns each assignee's `id`, and `gh api user` returns `node_id` in the same call that returns the login. C-007: entries that only carry `last_examined_at` (`launches == 0`) may be pruned when the issue leaves discovery; an entry with `launches > 0` is never pruned. `consumer_id` closes INV-007. X-003 and X-005: B, D and E voted "D" but agreed with A's text word for word, so these two were already converged in substance; the text above adds only C's "missing after init" case and the INV-018 Project ID.

##### Conflicts

1. **INV-001 vs C-007 and C-008.** Deleting `failed` removes `max_attempts` 3 and the 10-minute backoff from C-008, and `failed` from C-007's states. INV-001 wins. The `attempts` counter is renamed `retries` and given one meaning: `--retry-launch` tries (INV-003).
2. **INV-014 vs C-004 and A-005.** `--assignee` discovery makes the `unassigned` skip reason unreachable. INV-014 wins: the permanent exit-4 cliff is worse than losing a visibility signal. A-005's "assign before approving" moves from advice to a setup requirement.
3. **INV-015 vs C-008.** `max_candidates` 10 does not fit the 35-call cap. INV-015 (as modified: 8 plus a 6-call reserve) wins over C-008's 10 and over the probe's 5.
4. **INV-003 vs C-008, INV-012, INV-016 and INV-017.** A retry uses the cycle's single launch slot, re-checks `DISABLED`, adds nothing to the day cap, and never starts after 120 s. These are consistent once stated together; no ruling loses.
5. **INV-021 vs INV-026.** The claim's own edited marker comment is newer than the approval. If INV-026 ran first, it would skip the issue as `edited_after_approval` instead of recording `claimed`. Order: the C-024 marker check (with INV-021) runs first; INV-026 applies only to issues without valid marker evidence.
6. **INV-024 vs INV-008 vs INV-021.** All three compare against the approval event. The approval must postdate the trigger label (INV-008) and the store's `created_at` (INV-024); a marker counts only if newer than that same approval (INV-021). They compose; no ruling loses.
7. **INV-005 vs X-001 and X-002.** The dry run reports the `pending_orphan` and `claim_not_observed` transitions but does not write them. INV-005 wins over the cycle-start write wording of X-001 and X-002 in dry-run mode only.
8. **INV-006 vs X-007 and C-018.** X-007 lists codes without precedence; INV-006 adds it. My order (6, 7, 2, 3, 5, 4) replaces the probe's order (6, 5, 3, 4, 7, 2), following C's R2 rule that an `unknown` launch outranks transient errors.
9. **INV-027 vs C-020 and S-005.** `init-state` now creates both the store and the lock file, and it refuses if either exists. `check-config` stays read-only (C's position) but adds the filesystem check.
10. **INV-010 and INV-026 vs INV-015.** Both add reads; INV-010's call sits inside the 6-call re-read reserve, and INV-026 reuses pages already read. If a real issue needs more comment pages than the budget allows, the read is incomplete and the issue is skipped (fail closed), never launched.
11. **INV-018 vs C-001.** The Project is matched by node ID while labels, field and option stay matched by name. This is deliberate: an issue can be in several Projects, but it can carry only one label with a given name.

##### Final concessions

- My round-2 C-011 text ("a definite Orca error gives retryable `failed`") was wrong and is withdrawn (INV-002). With INV-001, `failed` disappears from the design entirely.
- My C-011 text also let the lease abandon an `unknown`, which contradicted my own A-009 ruling (INV-004). Withdrawn.
- My `max_candidates` 10 was never checked against the 35-call cap. Corrected to 8 with a reserve (INV-015).
- My C-004 `unassigned` reason, which I defended in round 2 for visibility, is given up for INV-014.
- C was right that names alone are a weak identity for owners; node-ID matching is adopted for C-004 at zero cost. I still hold names for labels and fields (C-001), because a rename fails closed.
- `check-config` creating the store was already conceded to `init-state` in round 2 (C, D); INV-027 extends `init-state` to the lock file.
- Two residuals cannot be closed under D1 and must be written down rather than argued away: two enabled workspaces on one login (INV-024 path 7, C-005), and edits or approval removal after the final re-read (INV-023, INV-026). Store restore from backup is declared unsupported rather than solved.
- Verification debt that this round adds and that stays UNVERIFIED until the C-023 live test: Orca's retry rule (INV-003), the collaborator-permission endpoint access (INV-010) and GraphQL `lastEditedAt` coverage (INV-026). All three are built and tested here with mocks only.

### Variant B Advocate (final)

#### Round 3: advocate B (analyzer: root cause, evidence)

Evidence checked read-only this round: `refs/claim.md` (Waves 0-6), `scripts/origin_repo.py:86-99` (`parse_origin_url`), the captured Orca help (`.dev/orca-command-refactor/review/p0-live-orca-help.txt:54`), research-deep fact 7 and Q3, Q6, Q11.

##### Findings table

| INV id | Verdict | Final ruling or residual-risk statement | Reason |
|---|---|---|---|
| INV-001 (H) | MODIFY | Shared pre-spawn checks (Orca probe, worktree exists, origin) run at cycle start; a failure exits 2 and writes no entry. The prompt is built before the `pending` write; a `ValueError` writes `failed` with `attempts+1`, `launches` unchanged. After `pending`, only `launched`, `unknown` or `abandoned` follow. | Root cause is ordering; host-wide failures are shared inputs (C-015), so they void the cycle rather than become per-issue retries. |
| INV-002 (H) | ACCEPT | A non-zero Orca exit after the spawn, including a definite error body, is `unknown` with the slot consumed. A's phrase "definite Orca error gives retryable `failed`" is withdrawn. | Orca's own help (`p0-live-orca-help.txt:54`) says to inspect the workspace after a lost reply, so error text does not prove that no session started. |
| INV-003 (H) | MODIFY | v1 never runs `--retry-launch` automatically. `unknown` keeps `operation_id` and `launch_cwd`; `status` and the runbook print the exact retry command for the operator to run after inspecting the workspace. Automatic retry is a follow-up gated on the live test proving Orca's retry rule (Q3). | Help:54 says "older hosts require inspecting the workspace first"; removing the path closes all six open questions at no cost to safety. |
| INV-004 | MODIFY | `unknown` (with or without an id) becomes `claimed` on an own marker; otherwise at lease end it becomes `abandoned` `launch_unconfirmed`. Lease transitions only relabel: they never release a consumed slot or permit a launch, as X-001 already does for `launched`. | The proposed "lease never drives a transition" contradicts agreed X-001; the safety property is non-release, not non-transition. |
| INV-005 | MODIFY | `once --dry-run` takes the lock, honours a persisted rate-limit time, performs every read and writes audit lines tagged `dry_run` naming each transition and launch it would make. It leaves the store byte-identical and never calls `orca agent launch`. | C-023's 24 h shadow gate needs a reviewable audit, so audit lines must be written while the store stays untouched. |
| INV-006 | MODIFY | Exit precedence: 6, 7, 5, 3, 4, 2. The cycle ends after its single launch attempt. Only exit 0 from a cycle that ran (not `disabled`) refreshes `last_completed_cycle_age_seconds`; the audit line keeps every reason. | A possibly live session (7) must outrank transient read errors (C R2); ending after the launch removes most co-occurrence. |
| INV-008 | ACCEPT | The latest approval `labeled` event must postdate the latest trigger `labeled` event; a trigger re-added after approval needs a fresh approval. | It uses the same event pages, so it costs no extra call. A missing trigger `labeled` event is absent evidence and never counts as positive (C-015). |
| INV-009 | MODIFY | Read explicit `per_page=100` pages until a page has fewer than 100 items. A repeated ID, a page that adds no new ID, or reaching the call cap makes the read incomplete. Order events by (`created_at`, `id`). `id` monotonicity is UNVERIFIED, so a same-second `labeled`/`unlabeled` tie on one label does not count as approval. | Ordering by "highest ID" rests on an unverified premise; an ambiguous order must fail closed. Matches `poll-augment-review.sh:46-56` and C's E4. |
| INV-010 | REJECT (residual) | Residual: only Triage-or-higher accounts can label (research fact 7), so a demoted or removed approver cannot add new approvals. Their earlier approvals stay valid until the owner removes the ID and audits the open approved issues (runbook step). A role check does not stop a compromised account. | The check needs an UNVERIFIED endpoint and closes only the case of a past approval. |
| INV-011 | MODIFY | Run `git -C <worktree> remote get-url origin` through the runner, parse it with the claim's own `parse_origin_url` rules (`origin_repo.py:86-99`) and compare `owner/repo` case-insensitively. Run the check at cycle start and again immediately before the `pending` write. | The claim resolves its repo with this script (`claim.md:13-15`), so the watcher compares like with like; `get-url` expands `insteadOf` for both. |
| INV-012 | MODIFY | `once` re-checks `DISABLED` immediately before the `pending` write. If the file is present, it writes nothing, audits `disabled` and exits 0. Residual: a spawn that has already started cannot be stopped. | Same as the proposed ruling, minus the `--retry-launch` clause, which INV-003 removed. |
| INV-014 | MODIFY | Discovery adds `--assignee <own login>`; the exact-set check in C-004 still runs locally. Residual: 100 open trigger-labelled issues assigned to one login still give exit 4. The runbook action is to remove the trigger label from claimed issues. | The claim never changes labels (`refs/labels.md:7`), so the cliff moves to the own login but does not disappear. |
| INV-015 | MODIFY | A prunable `considered` map (issue to `last_examined_at`), kept apart from dispatch entries, orders candidates oldest first, never-examined first. Every examined issue updates it, including skips. The cycle launches the first eligible candidate and stops. `max_candidates` stays 10; the 35-call cap binds. | The proposed 6 calls per candidate count a re-read for every candidate, but only the one launch is re-read: 2 + 3x10 + 3 = 35 fits. |
| INV-016 | MODIFY | Each entry stores an immutable `consumed_at`, set in the `pending` write. The cap counts entries in any state with `consumed_at` in the last 24 h and refuses a launch when that count is already 6. Tombstones keep `consumed_at`. | A named, immutable field cannot drift when `reset` runs or entries become tombstones; the retry clause is moot under INV-003. |
| INV-017 | MODIFY | Each `gh` call and the probe time out at the lesser of their configured value and the time left before 240 s. No launch starts after 120 s. A started launch is never cut short, its record is written, and the cycle ends. | No read follows a launch, so an exit 3 for overrun cannot hide a launch that succeeded. |
| INV-018 | ACCEPT | As proposed: exactly one item in the configured Project node ID, Status option Backlog, read over all `projectItems` pages; otherwise skip `project_mismatch`. | It closes the unrelated-Project hole. The field and option are still matched by exact name, which fails closed on a rename, as in C-001. |
| INV-019 | ACCEPT | As proposed. | The allow-list is a shared input (C-015); `check-config` and `once` must share one validator. |
| INV-021 | REJECT (residual) | Keep the marker for good: an own marker means `claimed`, consistent with C-007, where re-approval never resets. New work needs a new issue or a hand-run claim. Residual: a hand-run claim that races a watcher launch; the runbook forbids hand-claiming a trigger-labelled issue. | The proposed ruling makes hand-claimed issues relaunchable while watcher-claimed ones are not, and the claim re-runs idempotently (`claim.md:42`), so a second full session follows. |
| INV-024 (H) | MODIFY | `init-state` records `created_at`; an approval event older than it is not approval. Restoring the store from a backup is unsupported; recovery is always `init-state`, after which the owner re-applies approvals. Two workspaces on one login stay an accepted residual (C-005). | The fence makes loss plus re-init safe. A restored store keeps its old `created_at`, so restore must be forbidden. Path 7 has no local fix under D1. |
| INV-026 (H) | MODIFY | Eligible only if the body and every comment not authored by the own login or an allow-listed approver ID were created and last edited before the approval event. Timestamps are read as metadata only, from the C-024 comment pages. Otherwise skip `changed_after_approval`; re-approval re-arms. `lastEditedAt` is UNVERIFIED (Q11). | The claim reads the body and comments live (`claim.md:26`, `:56`); this reuses reads already paid. Residual: text added after the re-read stays under C-014; a commenter can delay a dispatch but never cause one. |
| INV-027 (H) | MODIFY | Only `init-state` creates `<state_dir>/lock`. `once` opens it without creating it (missing: exit 6), and no verb deletes it. After `flock`, the fd's (dev, inode) must equal the path's, else exit 75. `check-config` exits 2 on a network filesystem type (from `/proc/self/mountinfo`). | The post-flock identity compare is house practice (`hooks/scripts/launch-job-identity.sh:146-157`) and catches deletion or replacement by anyone. |

##### Open points table

| Point | Final ruling |
|---|---|
| C-004 | The intended owner is an issue whose assignee set equals exactly {own login}, read each cycle by `gh api user`. Discovery passes `--assignee <own login>`. Unassigned and other-assignee issues skip as `unassigned` and `assigned_other`. One pure function, `is_intended_owner`. |
| C-007 | States: pending, launched, unknown, failed, abandoned, claimed. `launches` increments in the durable `pending` write, after pre-spawn checks, with immutable `consumed_at`. A fresh launch needs `launches == 0`; re-approval never resets; only `reset --forfeit-guarantee` clears it. |
| X-003 | An unparseable, unknown-version or missing-after-init store gives exit 6, zero launches and an untouched file; never reset. Recovery: operator moves the file aside and runs `init-state`, whose `created_at` fence (INV-024) ignores earlier approvals. Backup restore unsupported. |
| X-005 | No label-only or Project-off mode. Membership and Backlog come from the issue's own `projectItems`, all pages, for the configured Project node ID (INV-018). An unreadable item skips that issue; a missing `read:project` scope exits 3. |
| A-009 | REJECT as a safety premise. The lease is a reporting threshold that moves `launched` and `unknown` to `abandoned` with a reason. It never releases a consumed slot or permits a launch; a later own marker still yields `claimed`. |

##### Conflicts

1. **INV-004 (proposed) against X-001 (AGREED).** "The lease never drives a transition" contradicts X-001, under which `launched` becomes `abandoned` `claim_not_observed` at lease end. **X-001 wins.** My INV-004 keeps lease transitions but forbids them to release a slot.
2. **INV-003 (proposed auto-retry) against INV-011, INV-012 and INV-016 (proposed).** All three carry `--retry-launch` clauses. **My INV-003 wins** (no automatic retry in v1); those clauses drop. C-011's "`--retry-launch <id>` only with an id" becomes operator-run only.
3. **INV-015 (proposed `max_candidates` 5) against C-008 (AGREED 10).** **C-008 wins.** The arithmetic fits once only the launch candidate is re-read and the cycle stops at the first eligible issue.
4. **INV-021 (proposed) against C-007 (re-approval never resets).** **C-007 wins.** The marker rule must treat hand-claimed and watcher-claimed issues the same way.
5. **INV-010 (proposed role check) against C-013 and the 35-call budget.** **C-013 wins** (static ID list), with the residual recorded.
6. **INV-006 against X-007.** X-007 keeps its codes. INV-006 adds only precedence, and "only exit 0 refreshes" excludes `disabled`, so a watcher left disabled reads as stale, not healthy.
7. **INV-001 against D R2 item 1.** Compatible once the order is fixed. A shared pre-spawn failure is exit 2 (C-015), not a per-issue `failed`.
8. **INV-026 against C-014.** INV-026 narrows the residual C-014 accepts; it does not replace it. C-014's cron gate still requires the owner's acceptance of the text the claim reads.
9. **INV-024 against C-024.** Compatible. A marker without a record still yields `claimed`, and approvals older than `created_at` are ignored, so a re-initialised store dispatches only issues the owner re-approves.
10. **INV-014 against C-004 (C's account-ID routing).** Discovery by `--assignee <login>` assumes login routing, which supports the majority C-004 text.

##### Final concessions

- **INV-002.** My round-2 "AGREE with A" on C-011 carried A's "definite Orca error gives `failed`" phrase, the duplicate path D had already conceded. I withdraw it.
- **INV-001.** My C-009 order (re-read, then `pending`) fixed the delete path but left unstated where the probe and prompt build run. The fault-finder is right that this left a stuck `failed`.
- **INV-009.** My N1 carried the page cap from `poll-augment-review.sh` but dropped its repeated-ID check, which C's E4 had raised.
- **INV-015.** The seed's `considered` ordering was in the research plan, and I did not carry it into C-007.
- **INV-024 and INV-027.** My round-2 A-001 and A-007 qualifiers ("missing store exits 6"; "local FS is a precondition") did not cover re-initialisation, backup restore or lock-file deletion. The `created_at` fence and the inode check are the mechanical fixes I should have proposed.
- **INV-026.** I treated C-014's acceptance as covering every text read. It covers the text the approver saw, not text added afterwards. I concede this is a HIGH gap and that the timestamp check is cheap.

### Variant C Advocate (final)

#### Round 3 — Advocate C (backend)

##### Findings table

| INV id | ACCEPT/MODIFY/REJECT | Final ruling or residual-risk statement | Reason, one line |
|---|---|---|---|
| INV-001 | ACCEPT | The Orca probe, prompt build and worktree origin check all run before the `pending` write. Once `pending` is written, the only outcomes are `launched`, `unknown` or `abandoned`, and `failed` never follows a `pending` write. | Preflight retries cannot undo a durable consumed slot; an uncertain write also stops dispatch. |
| INV-002 | ACCEPT | A non-zero Orca exit after the spawn, including a definite error body, is `unknown` with the slot consumed. A's C-011 phrase "definite Orca error gives retryable `failed`" is withdrawn. | Error text does not prove that no session started. |
| INV-003 | MODIFY | Automatic `--retry-launch` is disabled in v1. Preserve operation ID and cwd for investigation. Manual same-operation retry requires a separately verified Orca idempotency contract; without that evidence, recovery requires explicit guarantee forfeiture. No ordinary cycle invokes a retry. | Three bounded calls can still duplicate sessions if the unverified replay contract is wrong; mock success cannot establish that contract. |
| INV-004 | MODIFY | Treat `unknown` as terminal for automatic dispatch, with or without an operation ID. A later recognized own marker may establish `claimed`; operator-reviewed disposition may mark `abandoned` without releasing the slot. Lease expiry only raises an overdue alert. | A terminal unresolved outcome is honest; inventing an automatic retry exit is unnecessary. |
| INV-005 | MODIFY | Dry-run locks existing storage, simulates transitions and budgets in memory, performs bounded GitHub reads, and emits a shadow audit. It never invokes Orca or changes dispatch, backoff, next-permitted time, or production-health timestamps; probe/launch outcomes remain unverified. | A useful shadow report predicts selection, not external launch success; obey existing request deferrals even though dry-run persists no new ones. |
| INV-006 | MODIFY | Aggregate all reasons; exit precedence is 6, 2, 5, 7, 3, 4, then 0. Lock contention remains 75. Only a complete production exit-0 cycle refreshes completion health; disabled, dry-run, truncated and incomplete cycles never do. | Storage/configuration failures dominate; launch uncertainty stays visible above ordinary read errors. Codes alone must not hide partial completion. |
| INV-008 | ACCEPT | An issue is eligible only when the latest approval `labeled` event postdates the latest trigger `labeled` event. A trigger re-added after approval needs a fresh approval. | The trusted approver authorizes the current trigger; requiring a trusted trigger actor too adds no necessary boundary. |
| INV-009 | MODIFY | REST pagination requires a short terminal page; GraphQL requires `hasNextPage=false`. Duplicate IDs, nonadvancing cursors or budget exhaustion make evidence incomplete. Order events by `created_at`; ambiguous competing timestamp ties fail closed, unless a verified API ordering contract resolves them. | Numeric IDs identify events but are not source-verified chronological clocks; an exactly full last page needs another read. |
| INV-010 | MODIFY | Reverify approval actor's current Triage-or-higher repository permission before submission, in addition to the allow-list. Unavailable, ambiguous or insufficient permission skips `approver_not_current`. Count and refresh this read within shared budgets; endpoint/role semantics remain an activation prerequisite. | Static admission does not revoke stale authority; unavailable permission evidence cannot silently become approval. |
| INV-011 | MODIFY | Parse `git remote get-url origin` using the claim parser's accepted forms; compare owner/repository case-insensitively. Reject unsupported forms. Validate before GitHub reads, before intent commit and immediately before spawn. Local configuration changes after validation remain a trusted-host race. | The real parser accepts HTTPS and GitHub SCP-style SSH, including trailing slash and `.git`; matching arbitrary raw URLs is wrong. |
| INV-012 | MODIFY | Check `DISABLED` at cycle start, before intent commit and immediately before spawn. A post-commit stop records `abandoned/disabled_before_spawn` with the slot consumed. Start no further work, exit 0 unless a higher-priority failure exists; never claim already-running sessions were stopped. | Checking only before commit leaves a preventable post-commit launch; the kill switch is not cancellation of existing sessions. |
| INV-014 | MODIFY | Add server-side own-assignee filtering and paginate discovery under the shared call/time budget. A full 100-item page is not itself truncation; continue to proven completion. Incomplete discovery exits 4, reports capacity blockage, and launches nothing. Claimed entries remain suppressed locally. | Filtering alone only moves the cliff: 100 own-assigned claimed issues still disable discovery forever. |
| INV-015 | MODIFY | Persist an examination sequence per issue; process least-recently-examined first with issue-ID tie-breaks. Mark only candidates actually examined, including partial-budget/revalidation failures; untouched candidates retain priority. Cap at five, but call/time limits always win; five complete evaluations are not guaranteed. | Paging, current-role checks and refreshed evidence invalidate fixed six-call arithmetic; sequences avoid wall-clock ordering failures. |
| INV-016 | MODIFY | Day-cap accounting uses retained immutable intent-commit events, including unknown, orphaned, abandoned and reset attempts. Refuse a new intent when six commits fall in `(now−24h, now]`. Clock rollback blocks new intents until reviewed; reconciliation adds no fresh intent. | Current-entry timestamps lose old submissions on reset; caps need durable history. Correct UTC remains a prerequisite against forward clock jumps. |
| INV-017 | MODIFY | Use monotonic deadlines; subprocess timeout is min(configured timeout, remaining cycle budget). Start no launch after 120 seconds or without its 120-second allowance. Always persist outcome before exit; slow local durability may overrun 240 seconds and must be reported, never hidden. | A launch still has a finite timeout and becomes unknown on timeout; local fsync latency prevents an honest absolute process-duration guarantee. |
| INV-018 | MODIFY | Require exactly one non-archived issue item in the configured Project node ID, with configured Status-field and Backlog-option IDs, over complete `projectItems` pagination. Other Projects never qualify. Missing, duplicate or unreadable target evidence fails closed; unresolved mappings block activation. | A Project ID alone fixes cross-Project confusion but not name replacement or field ambiguity. |
| INV-019 | ACCEPT | `once` exits 2 before any `gh` call when the approver file is missing, empty or unsafe, so a misconfigured watcher never reports a healthy cycle. | Validation must apply during polling, not just an optional setup check; unsafe includes replaceable parent paths. |
| INV-021 | REJECT | Any recognized own marker suppresses fresh dispatch regardless of approval age. Approval changes do not create a new dispatch key. Repeated work requires explicit guarantee-forfeiture recovery. Concurrent manual claims remain an accepted, documented exclusion-boundary risk; operators must serialize them. | Marker edit time identifies neither a new approved task nor its session; allowing older markers to re-arm contradicts lifetime-per-issue suppression. |
| INV-024 | MODIFY | Guarantee at most one fresh submission per issue only within one intact, non-rolled-back ledger and authority. Loss, restore, independent authorities or reset invalidate it; keep activation disabled until operator reconciliation. Neither a new epoch nor reapproval proves an earlier session absent. | Accept this explicitly bounded residual, not a global-start guarantee: `created_at` fixes neither restored backups nor simultaneous independent ledgers. |
| INV-026 | MODIFY | Before intent commit, reject body/comment creation or edit metadata not strictly older than approval, or unverifiable edit evidence. Require reapproval after edits and validate adapters before activation. Post-refresh mutation before the claim's live reads remains a separate owner-accepted residual. | The proposed check improves the snapshot but cannot freeze later reads; role, automation and content-race risks are distinct. |
| INV-027 | MODIFY | Create the lock once by exclusive initialization; all verbs retain its inode and acquire it before state mutation. Reject missing/replaced/symlinked locks and unsupported/nonlocal storage. Verify held-file identity before dispatch; external directory deletion or replacement remains an unsupported guarantee-breaking operator action. | Managed lock lifecycle closes the tool-induced unlink race, not arbitrary same-user filesystem interference; unsupported storage must fail closed. |

##### Open points table

| Point | Final ruling |
|---|---|
| C-004 | Use exactly one current assignee matching this cycle's authenticated login, with authenticated account ID pinned to the ledger authority. Reject account changes and multi-assignee/unassigned issues. This deliberate preassignment policy is stricter than claim; display distinct skip reasons. |
| C-007 | Persist six states, attempts, launches, approver/event IDs, owner account ID, operation context, examination order, timestamps and reasons. Increment launches with durable pending before invocation; fresh launch requires zero. Only unconsumed preflight failures retry; labels, expiry and identity changes never reset consumed keys. |
| X-003 | Missing, corrupt, incompatible or unwritable state exits 6 and stops dispatch; never initialize or reset during polling or validation. Preserve existing bytes where readable. Initialization and restore are explicit operator procedures; restored state is not automatically proof against rollback. |
| X-005 | Project and Backlog are mandatory; no label-only or Project-off mode exists. Use complete issue-local Project evidence bound to configured IDs. Candidate-specific unreadability skips that issue; shared authorization failure stops further dispatch with exit 3, preserving already committed outcomes. |
| A-009 | REJECT as a safety premise. Sixty minutes is an overdue-report threshold, not evidence that a session stopped. Neither missing markers nor elapsed time releases a consumed slot. Later recognized markers can establish claimed, including from unknown or abandoned; claim duration remains unmeasured. |

##### Conflicts

1. **Replay bounds versus idempotency:** INV-003's no-automatic-retry rule wins over the probe's three retries and Round 2 C-011's unconditional replay. INV-004 makes unresolved outcomes terminal for automatic dispatch, not silently successful. Keep three attempts and ten-minute backoff only for provably unconsumed preflight failures; never decrement `launches`.
2. **Final checks versus consume-before-spawn:** INV-001/C-009 require all substantive preflight before commit. INV-011/012/027 add last-moment checks afterward. If one then fails, the slot stays consumed and becomes abandoned, never retryable failed. A crash in that gap remains `pending_orphan`. Lost availability wins over duplicate risk.
3. **Lease wording:** A-009 and INV-004 override any statement that the lease proves completion or makes unknown retryable. The existing `launched` to `abandoned/claim_not_observed` reporting classification may remain, but does not release the slot; both states accept later marker evidence.
4. **Approval versus marker time:** INV-021's conservative suppression wins over the probe's timestamp-based re-arming. INV-026 applies only to a prospective fresh dispatch, not reconciliation of consumed/claimed entries. Claim-generated comments after approval must not erase a valid claimed outcome. Reapproval never resets a consumed key.
5. **Approval freshness versus narrative risk:** INV-008, INV-010 and INV-026 are cumulative. Current role does not prove a human rather than PAT automation acted; preflight timestamps do not freeze the claim's later reads. Existing C-014 acceptance cannot silently cover this additional mutation window. Without explicit residual acceptance, activation stays blocked.
6. **Budgets versus completeness/fairness:** INV-009/014/015/018 win over fixed discovery argv, the 100-result cliff and any promise that five candidates fit 35 calls. Count discovery pages, role/metadata reads and refreshes. Incomplete discovery blocks dispatch; incomplete candidate evidence skips that candidate. Persist actual examination progress, never pretend untouched candidates were examined. Indefinite delay beyond supported capacity is reported, not called healthy.
7. **Timeout versus durability:** INV-017 overrides “a launch already started is never cut short”: the configured subprocess deadline still applies, with consumed unknown on timeout. Durable outcome recording wins over a hard 240-second completion claim; audit overrun and preserve all outcomes under INV-006 precedence.
8. **Local mechanism versus global guarantee:** INV-024/027 win over claims of unconditional per-account or lifetime starts. No initialization epoch, marker, account ID or local inode check supplies distributed exclusion or proves rollback absent. Unsupported independent authorities, concurrent manual claims, destructive cleanup and reset must be explicit operational exclusions, not solved by `enabled=false`.
9. **Reset versus daily cap:** An explicit `reset --forfeit-guarantee` may reopen only an abandoned issue under the lock, with audit and warning. It forfeits the issue guarantee but cannot erase submission-history events or bypass INV-016's daily cap. Read-only `check-config` never creates state.

##### Final concessions

- I retain JSON rather than SQLite, login-compatible sole-assignee routing, the fixed claim-only launch, and no distributed coordinator. Account-ID binding costs no separate identity request when projected with the login. Project/field/option identity remains necessary.
- I accept documented missed dispatch after a consumed-but-unspawned intent. I do not accept calling an intact-ledger guarantee a universal at-most-once-start guarantee, or calling a renewed approval proof that an old session ended.
- I accept a guarded, audited reset rather than forcing unsafe manual file edits. Its warning must name guarantee forfeiture, not “safe retry.”
- Code checks confirm that claim can edit an older marker, posts it only after its analysis/next-steps work, permits unassigned issues, and does not check watcher approval. It also performs conditional ClickUp effects. None of these facts establishes a mutex or content-version binding.
- All new API shapes, role checks, edit metadata, lock/durability checks and failure paths require mocked acceptance tests. Actual Orca replay, slash-command execution, permissions, Project access, supported storage and content-metadata contracts remain owner-run activation follow-ups. This round ran no commands, tests, network calls or live launches; only this requested argument file changed.

### Variant D Advocate (final)

#### Round 3 final arguments: advocate D (devops lens: deployment, observability, runbooks, SLO impact)

Facts checked read-only this round: `refs/claim.md` (Wave 1 reads at `:26`, marker reuse at `:29`, Wave 2 checks at `:39-43`, marker posted only in Wave 6 at `:84-88`), `scripts/origin_repo.py` (`parse_origin_url` at `:86-99` accepts https and `git@` forms, strips `.git` and a trailing `/`, returns owner/repo case as written; `read_origin` at `:156-174` runs `git remote get-url origin`, which applies `insteadOf` rewrites), and `enrichment/research-deep.md` (`--retry-launch` rule fact 6; Q3, Q6, Q11 still UNVERIFIED).

##### Findings table

| INV id | Answer | Final ruling or residual-risk statement | Reason |
|---|---|---|---|
| INV-001 (HIGH) | MODIFY | The `DISABLED` check, Orca probe, prompt build, origin check and C-009 re-read all run before the `pending` write. A failure there writes `failed` with `launches` 0 and `attempts`+1. After `pending`, outcomes are only `launched`, `unknown` or `abandoned` (an exec `OSError` is `abandoned` `spawn_error`). | Probe's order plus the exec-error case it left open, so a single write still consumes the slot. |
| INV-002 (HIGH) | ACCEPT | As proposed: any non-zero Orca exit after the spawn, including a definite error body, is `unknown` with the slot consumed; A's "definite Orca error gives retryable `failed`" is withdrawn. | This is my R2 item 1; the tally counted two texts as one. |
| INV-003 (HIGH) | MODIFY | `--retry-launch` runs only on `unknown` with an operationId, and only after the live test records that Orca deduplicates a repeated id. It re-runs the `DISABLED`, C-009 and origin checks, uses the cycle's one launch slot, never increments `launches`, at most 3 total. | Automatic retry must not rest on UNVERIFIED Q3; a non-deduplicating retry is a second launch. |
| INV-004 (MEDIUM) | MODIFY | At the next cycle start, `unknown` becomes `claimed` on an own marker, else stays `unknown` only while retry-eligible (INV-003); otherwise `abandoned` (`retry_exhausted` or `retry_not_enabled`). The lease never releases a slot and never moves `unknown`. | Gives `unknown` an exit without contradicting X-001's lease-to-`abandoned` reporting move. |
| INV-005 (MEDIUM) | MODIFY | `once --dry-run` requires an initialised store, takes the lock, performs every read and never calls Orca. It writes only audit lines tagged `dry_run=true` ("would" transitions and launches); store, backoff, rate-limit and health timestamps stay byte-identical. | The C-023 shadow gate needs a reviewable audit, which "byte-identical" alone would forbid. |
| INV-006 (MEDIUM) | MODIFY | Several outcomes exit with the first applicable code in the order 2, 6, 7, 3, 4, 5; the audit line and `status --json` list every reason. Only a completed exit-0 cycle refreshes `last_completed_cycle_age_seconds`; a `DISABLED` exit 0 does not, and `status` shows `disabled_since`. | Unknown launches need a human before transient rate limits (C R2); a forgotten kill switch must alert. |
| INV-008 (MEDIUM) | ACCEPT | As proposed: eligible only when the latest approval `labeled` event postdates the latest trigger `labeled` event; a trigger re-added after approval needs a fresh approval. | Same event read, no extra call; binds the human act to the current trigger. |
| INV-009 (MEDIUM) | MODIFY | Event and comment pages (`per_page=100`) are read until a page returns fewer than 100. A repeated ID, or a full page when the call cap is hit, makes the read incomplete. Order by `created_at`, then event ID; opposing approval events in one second fail closed. | Event-ID monotonicity is UNVERIFIED; failing closed on a tie avoids depending on it. |
| INV-010 (MEDIUM) | REJECT, accept as residual | Residual: an allow-listed approver who is demoted, removed or compromised stays valid until the owner edits the file. Runbook: create `DISABLED` first, then edit the file. `status` prints approver IDs and file mtime. Live role check is a follow-up once endpoint access is verified. | The role endpoint and token scope are UNVERIFIED and cost a call per candidate; a v1 must not rest on them. |
| INV-011 (MEDIUM) | MODIFY | The check runs `git -C <launch_cwd> remote get-url origin` (what the claim reads, `insteadOf` applied), parses it with `parse_origin_url` rules, and compares lowercased to `ironbellyorg/ironclaude`. Unparseable gives exit 2. It runs again before every spawn and `--retry-launch`. | Reuses the claim's own parser, so watcher and claim agree on the repo. |
| INV-012 (MEDIUM) | ACCEPT | As proposed: `once` re-checks `DISABLED` immediately before each `pending` write and each `--retry-launch`; if present it starts nothing further, records the cycle and exits 0 (not a health refresh, INV-006). | One `stat` call; makes the kill switch work during an incident. |
| INV-014 (MEDIUM) | MODIFY | As proposed (`--assignee <own login>`, exact local set check still runs), plus `status` reports `discovery_count`, and the runbook treats 80 or more as a warning. A persistent exit 4 goes stale and alerts (INV-006). | The cliff becomes per login, not per repo; it needs an early warning before it bites. |
| INV-015 (MEDIUM) | MODIFY | The store keeps `last_examined_at` per issue, set for every examined candidate including `budget_exhausted` and `revalidation_failed`; candidates run oldest first. Terminal records cost no calls. `max_candidates` stays 10 [PROPOSAL]; the 35-call cap governs. | The C-009 re-read runs once per cycle (one launch), not per candidate, so about 3 calls each fits 10. |
| INV-016 (MEDIUM) | MODIFY | As proposed (every entry whose `pending` time is in the last 24 h, any state; refuse at 6; `--retry-launch` adds nothing), plus `reset` keeps the entry's `pending` time, so a reset cannot raise the cap. | Without that line the reset verb would bypass the blast-radius limit. |
| INV-017 (MEDIUM) | ACCEPT | As proposed: each `gh` and probe call times out at the lesser of its value and the time left before 240 s; a started launch is never cut short and its record is written before exit, with code by INV-006. | No launch starts after 120 s, so the launch ends by 240 s; the 5-minute cron leaves margin. |
| INV-018 (MEDIUM) | ACCEPT | As proposed: exactly one item in the configured Project node ID with Status Backlog, over all `projectItems` pages (each page counts toward the cap); none or several gives `project_mismatch`. | A rename or second Project fails closed; the node ID goes in the config `check-config` reads. |
| INV-019 (MEDIUM) | ACCEPT | As proposed: `once` exits 2 before any `gh` call when the approver file is missing, empty or unsafe. | Exit 2 never refreshes the age, so the staleness alert fires. |
| INV-021 (MEDIUM) | ACCEPT | As proposed: a marker is `claimed` evidence only when its comment was created or last edited after the current approval event; older markers leave the issue eligible. The concurrent hand-claim race stays a documented residual. | The claim PATCHes its marker (`claim.md:84-88`), so a watcher-launched claim still updates it after approval. Whether reactions bump `updated_at` is UNVERIFIED; if they do, the error is a missed launch, the safe direction. |
| INV-024 (HIGH) | MODIFY | `init-state` records `created_at`; `once` treats approval events older than it as not approved, so a re-created store re-arms nothing (the owner re-labels). Restoring a store from backup is unsupported (runbook: re-init). Two watchers on one login stay a documented residual (C-005). | Closes paths 5 and 6 procedurally; nothing local can detect path 7 without shared state. |
| INV-026 (HIGH) | MODIFY | Eligible only if the body and every comment not by the own login were created and last edited before the approval event (GraphQL `lastEditedAt`, UNVERIFIED), checked at evaluation and in the C-009 re-read; else skip `edited_after_approval`. Edits after the re-read stay a residual. | On a public repo a stranger's comment after approval is the main injection path; re-approval re-arms. |
| INV-027 (HIGH) | MODIFY | No verb deletes or replaces `<state_dir>/lock`; only `init-state` creates it, and a missing lock gives exit 6. After `flock`, `once` checks the fd inode equals the path inode, else exit 75. `check-config` rejects network filesystems found in `/proc/self/mountinfo`. | The inode re-check is the standard fix for the unlink race and is mock-testable. |

LOW findings (not required): INV-007 is folded into C-007 (`launch_login` field) and C-004 (configured account ID); INV-022 is covered by INV-015's `last_examined_at`; INV-023 is accepted as a documented residual, since `DISABLED` and approval removal cannot stop a session already spawned.

##### Open points table

| Point | Final ruling |
|---|---|
| C-004 | Intended owner: the assignee set equals exactly {own account}, matched by the ID that `gh api user` returns each cycle. If that ID differs from the configured `owner_account_id`, `once` exits 2 before discovery. Skips: `unassigned`, `assigned_other`. One pure function, `is_intended_owner`. |
| C-007 | States: pending, launched, unknown, failed, abandoned, claimed. Fields: A's list plus `launch_login` and `last_examined_at`. `launches` is incremented in the same durable write as `pending`, before Orca; a fresh launch needs `launches == 0`. Only `reset <N> --forfeit-guarantee` resets it. |
| X-003 | An unparseable store, an unknown `schema_version`, or a missing store or lock file gives exit 6, zero launches and no write. `once` never creates or resets either. Recovery follows the runbook: `init-state`, whose `created_at` blocks earlier approvals (INV-024). |
| X-005 | No label-only mode and no switch that turns the Project check off. Membership and Backlog come from the issue's own `projectItems` in the configured Project node ID (INV-018). An unreadable or incomplete item read skips the issue; a missing `read:project` scope voids the cycle with exit 3. |
| A-009 | REJECT as a safety input. No at-most-once property depends on the marker appearing within the lease. The lease is a reporting threshold: at expiry `launched` becomes `abandoned` `claim_not_observed`, the slot stays consumed, and a later own marker still gives `claimed`. |

C-004 takes C's account-ID point without dropping the login: the claim still assigns `@me` (`claim.md:47`), and the configured ID turns a silent re-auth to another account (INV-007) into a visible exit 2.

##### Conflicts

1. **INV-004 (proposed "the lease never drives a transition") against X-001 and A-009.** X-001 moves `launched` to `abandoned` `claim_not_observed` at lease expiry. **X-001 wins.** That move only reports and releases nothing, so INV-004 is narrowed to "the lease never releases a slot and never moves `unknown`".
2. **INV-003 ("at most once per cycle") against C-008 ("one launch per cycle").** **C-008 wins.** A retry uses the cycle's single launch slot, so no cycle makes two Orca submissions. The 120 s no-new-launch rule (INV-017) applies to retries.
3. **INV-006 proposed order (6, 5, 3, 4, 7, 2) against C's R2 X-007 text ("unknown launch or storage-integrity failure outranks ordinary transient errors").** **C's principle wins**, giving 2, 6, 7, 3, 4, 5. Exit 2 comes first because it happens before any call. A rate limit (5) heals itself, but an `unknown` launch (7) needs a person.
4. **INV-006 ("only exit 0 refreshes") against INV-012 and C-018 (`DISABLED` exits 0).** Resolved: a `DISABLED` exit 0 never refreshes the health age, and `status` shows `disabled_since`. Otherwise a forgotten kill switch would read healthy forever.
5. **INV-015 (proposed `max_candidates` 5) against C-008 (10).** **C-008 wins** with INV-015's persisted ordering. The probe charged the C-009 re-read to every candidate, but it runs once per cycle, for the one launch.
6. **INV-016 against the C-020 `reset` verb.** Resolved: a reset keeps the `pending` time, so the day cap still counts it.
7. **INV-014 amends C-006.** Discovery gains `--assignee <own login>`. C-006's "non-owned issues dropped before any per-issue call" stays as the local check. The idle cost is still 2 calls.
8. **INV-026 against C-024 and INV-021.** No conflict once own-login comments are excluded from INV-026. A hand-run claim's marker posted after approval is own-login, so INV-021 counts it as `claimed` evidence and INV-026 does not block on it.
9. **INV-024 (`created_at`) against the C-023 activation gates.** `init-state` must run before the 24 h shadow dry run (INV-005 requires a store). At go-live, approvals made during the shadow will dispatch, and older ones need a re-label. The runbook must say this.
10. **INV-010 (REJECT) against C's C-013 "after role verification".** My REJECT stands for v1, because the endpoint and token scope are UNVERIFIED. If the owner wants the check, it is a follow-up that must be verified live first, and its call counts toward the 35-call cap.
11. **INV-001 and INV-012 both add pre-`pending` checks.** They do not conflict. The order is `DISABLED`, then probe, prompt, origin, re-read, then `pending`.

##### Final concessions

- **A-001 and A-007 (mine, R2) were incomplete.** I said a missing store exits 6, "so losing `$HOME` stops dispatch". But the documented recovery, `init-state`, then re-dispatched every approved issue that had no marker (INV-024 path 5). I also left the lock file's lifecycle unspecified (INV-027). The `created_at` rule and the inode re-check close both gaps.
- **My SLO (b) and C-018 text were too generous.** "Exit 0 or 75 is healthy" let a stuck discovery cliff (exit 4) or a forgotten kill switch read green. Only a completed exit-0 cycle now counts.
- **My `DISABLED` was checked only at cycle start (INV-012).** That was not a kill switch during an incident. I concede the per-launch re-check.
- **I missed the discovery cliff (INV-014)** while conceding the Project cliff in R2. Both cliffs had the same cause.
- **I accept a liveness cost for INV-026.** Any stranger's comment after approval holds the issue until someone re-approves it. On a public repo, a held issue is the right price, and it shows up in the audit as `edited_after_approval`.
- **I do not concede the probe's arithmetic in INV-015.** The proposed cap of 5 rests on charging the re-read to every candidate.
- **I reject INV-010 as a v1 requirement but concede the risk is real.** It is recorded as a residual with a runbook step, not dismissed.
- **Residuals that the final spec must list as accepted:** INV-010 (stale approver), INV-023 (approval removed after the spawn), INV-024 paths 6 and 7 (backup restore, two watchers on one login), INV-026 (edits after the re-read), INV-021 (concurrent hand claim), INV-025 (claim reads issue text, C-014), and A-006 (clock skew allows at most one extra launch past the day cap). Each needs a runbook line, and where one applies, a `status` field.

### Variant E Advocate (final)

#### Round 3: advocate E (performance lens: bottlenecks, scaling, cost-to-serve)

Read: invariant-probe.md (all, with Proposed rulings), round2-tally.md, round2-advocate-A, D, E (and the open-point rows of B and C), seed-brief.md. Code facts checked read-only: `refs/claim.md:29,43,84-89` (the claim finds the latest own marker comment and edits it, so its `updated_at` moves on a re-run); `scripts/origin_repo.py:86-100` (`parse_origin_url` already strips `.git`, handles ssh and https; `read_origin` calls `subprocess` directly, so the poller must call `git -C <abs> remote get-url origin` through the injected runner and reuse the parser). Nothing live was run. Words in "UNVERIFIED" were not checked against GitHub.

##### 1. Findings table

| INV id | ACCEPT / MODIFY / REJECT | Final ruling or residual-risk statement | Reason |
|---|---|---|---|
| INV-001 (HIGH) | MODIFY | Origin, worktree and prompt checks run at cycle start; the Orca probe runs once per cycle after discovery finds an owned candidate, cached. All pass before the `pending` write; `failed` never follows it. A pre-write failure writes nothing, launches nothing, exits 2. | Probing on every idle cycle wastes a 10 s subprocess 12 times an hour; failing before the per-issue loop saves up to 35 wasted calls. |
| INV-002 (HIGH) | ACCEPT | As written: a non-zero Orca exit after the spawn, including a definite error body, is `unknown` with the slot consumed. A's C-011 phrase "definite Orca error gives retryable `failed`" is withdrawn. | The slot is paid for at the spawn; a cheap retry path is a duplicate path. |
| INV-003 (HIGH) | MODIFY | `--retry-launch` runs only on `unknown` with an id, after re-read, origin and `DISABLED` checks. It is the cycle's one Orca call, before any fresh launch, started by 120 s. Three tries in total, 10 minutes apart; `launches` unchanged; then `abandoned`. | The proposal has no budget rule. Without "it is the cycle's launch", one cycle could make two 120 s Orca calls and break the 240 s deadline. |
| INV-004 | ACCEPT | As written; add that an own marker newer than the approval moves `unknown` to `claimed` at any time. | Every state gets an exit; the lease stays a report threshold (A-009). |
| INV-005 | ACCEPT | As written, plus: the report says the Orca probe was skipped, and `considered` is not updated. | A dry run costs the same real `gh` calls as a live cycle. It validates selection only; the live test covers launch. |
| INV-006 | MODIFY | Precedence 2, 6, 7, 5, 3, 4; every condition is also an audit line. Only exit 0 refreshes `last_completed_cycle_age_seconds`. | The proposal ranks 3 above 7, so a deadline overrun (INV-017) can hide a launch that ended `unknown`, which needs a person. Exit 2 is raised before any call anyway. |
| INV-008 | ACCEPT | As written; "later" uses the INV-009 key. A reversed order is skipped as `approval_before_trigger`; setup doc: trigger first, approval second. | Same event read, zero extra calls. |
| INV-009 | MODIFY | Complete means a final page under 100 items, or a newest-first read holding the latest event of both labels. A repeated id, no progress, or cap reached is incomplete (skip). Latest is the highest event id. | Ascending REST history costs one call per 100 events per issue. Preferred build (UNVERIFIED): one GraphQL `timelineItems(last: 100, itemTypes: [LABELED_EVENT, UNLABELED_EVENT])` per issue. |
| INV-010 | REJECT, residual | Accepted residual: the allow-list is the owner's authority. `check-config` prints the file's mtime and entry count. Follow-up in C-023: best-effort role check if the endpoint works with a workspace token. | The collaborator-permission endpoint probably needs admin or maintain access (UNVERIFIED); a v1 fail-closed check could block every launch forever. Only 3 Triage-plus accounts exist today. |
| INV-011 | MODIFY | As written, with one placement change: the second check runs just before the `pending` write, not after it. Compare lowercased `owner/repo` from `parse_origin_url`; run `git` through the injected runner. | A local git call costs milliseconds, so repeating it is free. After the write, a failure would create the orphan INV-001 forbids. |
| INV-012 | MODIFY | Check `DISABLED` before each `pending` write and each `--retry-launch`; log `disabled_mid_cycle`; exit 0. | One `stat` call. Same placement rule as INV-011: before the write, never after. |
| INV-014 | ACCEPT | As written. Residual: unassigned waiting issues are no longer seen, so `unassigned` and `assigned_other` skip reasons vanish. Exit 4 still fires at 100 open trigger-labelled issues assigned to the own login. | The scaling fix: the cliff moves from all trigger issues to one owner's own backlog. Idle stays 2 calls. |
| INV-015 | MODIFY | Add a `considered` map (issue to `last_examined_at`) in the same store write, set for every examined candidate including skips, oldest first, pruned to the discovery set. Keep `max_candidates` 10 as a ceiling; the 35-call cap binds. | Cutting to 5 is arbitrary because calls per candidate are not fixed (one GraphQL query per candidate would fit 10). Pruning bounds the map at 100 keys; write only on cycles that examined something. |
| INV-016 | ACCEPT | As written, counting every entry that has a `pending` write time (tombstones keep it). An entry recorded from a marker alone has none and does not count. | Counting is O(entries); 1,000 tombstones cost microseconds. |
| INV-017 | ACCEPT | As written. Add the bound: last launch starts by 120 s and takes at most 120 s, so worst wall time is about 245 s inside the 300 s cadence; no new `gh` call with under 5 s left. | My own N2 gap. The bound makes exit 75 an anomaly signal. |
| INV-018 | ACCEPT | As written. Add `project_id` to the config. Status field matched by name `Status`, option by name `Backlog`; a rename gives `project_mismatch` for every issue, visible in the shadow run. Item pages are read until the configured Project's item is found; cap counted. | A typical issue has one or two items, so one call. |
| INV-019 | ACCEPT | As written. | Zero cost; an exit 2 every cycle also trips the staleness alert. |
| INV-021 | ACCEPT | As written, using the comment's `updated_at` compared with the approval event time inside the same `--jq` boolean. | `claim.md:29,43` edits the marker, so `updated_at` moves on a real re-run. No added call. |
| INV-024 (HIGH) | MODIFY | Accept `created_at`: approvals older than the store are not approved; the owner re-applies labels. Backup restore (case 6) and two stores on one login (case 7) are documented residual risks; the state directory is never restored from backup. | `created_at` cannot detect a restore (the backup carries an old value) or a second store. Case 7 also multiplies cost by W (my N1). |
| INV-026 (HIGH) | REJECT, residual | Accepted residual, written into C-014: approval binds to the label act, not to content. Post-approval edits and new comments are read by the claim. The controls are the live-test gate and the permission mode. | "Every comment older than approval" blocks any issue someone commented on after approval, and any commenter can cause that. A new comment is as dangerous as an edit, so the check adds no real protection. |
| INV-027 (HIGH) | MODIFY | After `flock`, confirm the open file is still the one at the path (same inode, link count above 0), else release and exit 75. No verb unlinks the lock. `once` and `check-config` refuse network-filesystem state directories (deny-list via `/proc/self/mountinfo`). | Two syscalls stop the delete-and-recreate race without relying on procedure. Linux is already required for `flock`. Residual: case 4 (separate state dirs, one login). |

##### 2. Open points

| Point | Final ruling (at most 45 words) |
|---|---|
| C-004 | The intended owner is the issue whose assignee set is exactly {own login}. The login is read each cycle with `gh api user`, and its account ID is stored in every record. Unassigned and other-assignee issues are skipped with a reason. This equals the claim's own rule. |
| C-007 | States: pending, launched, unknown, abandoned, claimed (`failed` removed, see Conflicts). Fields: `attempts`, `launches`, `operation_id`, `approver_id`, `approval_event_id`, `launch_cwd`, login, account ID, `pending_at`, timestamps, `last_reason`. `launches` rises in the `pending` write; a fresh launch needs 0; only `reset <N> --forfeit-guarantee` clears it. |
| X-003 | An unparseable store, an unknown `schema_version`, or a store missing after `init-state` gives exit 6 and zero launches. The file is never changed or reset. Recovery is an operator procedure; re-init sets a new `created_at`, so earlier approvals are not re-dispatched. |
| X-005 | No label-only mode and no mode that turns the Project check off. Membership and Backlog come from the issue's own `projectItems` in the configured `project_id`. An unreadable item skips that issue; a missing `read:project` scope voids the cycle (exit 3). |
| A-009 | REJECT as a safety premise. The lease is only a reporting threshold: it moves `launched` to `abandoned` (`claim_not_observed`) and releases nothing. Keep 60 minutes as the default and show the entry's age in `status`. A later own marker still gives `claimed`. |

##### 3. Conflicts between proposed rulings

1. **INV-001 against C-007, C-008 and C-011 (`failed`, `attempts`, 10-minute backoff).** Once checks run before the `pending` write and no failure follows it, `failed` has no producer, and the backoff and `max_attempts` 3 in C-008 have nothing to count. INV-001 wins. Remove `failed`; `attempts` and the 10-minute backoff apply only to `--retry-launch` (INV-003). A pre-write failure is a cycle-level exit 2 with no entry.
2. **INV-011 and INV-012 ("immediately before every spawn") against INV-001.** A check after the `pending` write that fails makes an orphan. INV-001 wins: both run after the re-read and just before the write. INV-003 retries get their own check before the call.
3. **INV-003 against C-008 "one launch per cycle".** Resolved above: the retry is that cycle's one Orca call, so a retry and a fresh launch cannot share a cycle.
4. **INV-006 against INV-017.** The probe's order puts 3 above 7, which lets an overrun hide an `unknown` launch. The modified order (2, 6, 7, 5, 3, 4) wins; INV-017's rule that a started launch always finishes and writes its record is unchanged.
5. **INV-014 against C-004 and A-005 (visible `unassigned` skips).** INV-014 wins on cost. The `unassigned` reason leaves `once` output. If the owner wants waiting issues visible, add a `status`-only count later; do not add a third idle call.
6. **INV-015 against INV-005 and "an idle cycle writes nothing".** The `considered` write happens only when a candidate was examined, and never in a dry run. An idle cycle still costs 2 calls and zero writes.
7. **INV-024 (`created_at`) against the first rollout.** Approvals made before `init-state` are not dispatched. That is intended, but the setup doc must say the owner re-applies approval labels after init. It agrees with INV-008 and INV-021 (all compare against the approval event time).
8. **INV-010 and INV-026 rejections against C-013 and C-014.** They agree: both stay accepted residuals, not open findings.

##### 4. Final concessions

- **INV-024 is not fully closed.** `created_at` covers a lost store; a restored older backup and two stores on one login still break "at most once". The spec must say "at most once per issue per intact, single store per login" and list both as residual risks. I stated the guarantee more strongly in round 2.
- **INV-015.** My round-2 point that the tombstone and `considered` map need no pruning was wrong for `considered`: it is not safety data, and pruning it to the discovery set keeps it at 100 keys. Tombstones still are never pruned.
- **INV-001, INV-017.** My N2 wall-clock rule was incomplete: it did not say where the probe runs or that a retry competes with a fresh launch for the 120 s mark. Both are now fixed above.
- **INV-010 and INV-026 stay open in substance.** I reject the proposed fixes because they are unreliable or self-defeating, not because the gaps are small. A compromised approver or a post-approval comment can still steer the launched session. The owner's acceptance in C-014 and the live permission-mode test are the only controls; the spec should say so plainly.
- **Cost figures to keep:** idle 2 calls and 24 per hour (0.48 percent of 5,000); worst 35 calls per cycle, 420 per hour on one login (8.4 percent); W workspaces on one login multiply both by W.

## Round 3 tally



Adopt = ACCEPT or MODIFY (a final ruling exists in the round-3 files); Reject = REJECT (treated as a documented residual risk when 3 or more of 5 reject). Severity from invariant-probe.md. A finding is ADDRESSED when at least 3 of 5 advocates adopt a ruling; HIGH findings need at least 4 of 5.

| Finding | Adopt | Reject | Votes | Outcome |
|---|---|---|---|---|
| INV-001 | 5 | 0 | C:ACC A:MOD B:MOD D:MOD E:MOD | ADDRESSED |
| INV-002 | 5 | 0 | C:ACC A:ACC B:ACC D:ACC E:ACC | ADDRESSED |
| INV-003 | 5 | 0 | C:MOD A:MOD B:MOD D:MOD E:MOD | ADDRESSED |
| INV-004 | 5 | 0 | B:MOD C:MOD E:ACC A:MOD D:MOD | ADDRESSED |
| INV-005 | 5 | 0 | B:MOD C:MOD E:ACC A:MOD D:MOD | ADDRESSED |
| INV-006 | 5 | 0 | B:MOD C:MOD E:MOD A:MOD D:MOD | ADDRESSED |
| INV-008 | 5 | 0 | B:ACC C:ACC E:ACC A:ACC D:ACC | ADDRESSED |
| INV-009 | 5 | 0 | B:MOD C:MOD E:MOD A:MOD D:MOD | ADDRESSED |
| INV-010 | 2 | 3 | B:REJ C:MOD E:REJ A:MOD D:REJ | RESIDUAL RISK (majority reject) |
| INV-011 | 5 | 0 | B:MOD C:MOD E:MOD A:MOD D:MOD | ADDRESSED |
| INV-012 | 5 | 0 | B:MOD C:MOD E:MOD A:ACC D:ACC | ADDRESSED |
| INV-014 | 5 | 0 | B:MOD C:MOD E:ACC A:MOD D:MOD | ADDRESSED |
| INV-015 | 5 | 0 | B:MOD C:MOD E:MOD A:MOD D:MOD | ADDRESSED |
| INV-016 | 5 | 0 | B:MOD C:MOD E:ACC A:ACC D:MOD | ADDRESSED |
| INV-017 | 5 | 0 | B:MOD C:MOD E:ACC A:ACC D:ACC | ADDRESSED |
| INV-018 | 5 | 0 | B:ACC C:MOD E:ACC A:ACC D:ACC | ADDRESSED |
| INV-019 | 5 | 0 | B:ACC C:ACC E:ACC A:ACC D:ACC | ADDRESSED |
| INV-021 | 3 | 2 | B:REJ C:REJ E:ACC A:MOD D:ACC | ADDRESSED (3/5) |
| INV-024 | 5 | 0 | C:MOD A:MOD B:MOD D:MOD E:MOD | ADDRESSED |
| INV-026 | 4 | 1 | C:MOD A:MOD B:MOD D:MOD E:REJ | ADDRESSED |
| INV-027 | 5 | 0 | C:MOD A:MOD B:MOD D:MOD E:MOD | ADDRESSED |

## Scoring Matrix

Per-point outcomes are in the three tally tables above (Round 1 tally, Round 2 tally, Round 3 tally). Confidence: unanimous 5 of 5 = 90 to 100 percent, 4 of 5 = 70 to 89 percent, 3 of 5 = 60 to 69 percent. HYBRID (H) means the merged ruling combines parts of several variants; the exact text is in the Round 2 and Round 3 "Merged ruling" and "Final ruling" columns.

## Convergence Assessment

- Points resolved: 50 of 51 (37 S/C/X points agreed by 4 of 5 after Rounds 1 and 2; C-004, X-003 and X-005 converged in Round 3; 10 of 10 shared assumptions, with A-009 resolved as REJECT as a safety premise by 5 of 5 in Round 3).
- Alignment: 98 percent. Threshold: 75 percent.
- Invariant gate: 6 HIGH unaddressed findings blocked convergence after Round 2.5; Round 3 adopted a ruling for every HIGH finding (INV-001, 002, 003, 024, 027 by 5 of 5; INV-026 by 4 of 5). INV-010 (MEDIUM) was rejected by 3 of 5 and is recorded as a documented residual risk. INV-021 (MEDIUM) adopted 3 of 5. No HIGH finding remains unaddressed.
- Status: CONVERGED (after the invariant gate cleared in Round 3).
- Unresolved points: C-007 (whether `failed` stays a dispatch-record state; 3 of 5 keep it, 2 of 5 remove it, see rounds/round3-advocate-*.md). Residual risk: INV-010.
