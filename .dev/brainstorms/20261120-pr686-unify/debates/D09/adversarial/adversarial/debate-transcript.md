# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 1 (round 2, invariant probe, scoring matrix and convergence are appended below as they finish)
- Convergence achieved: pending
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 OURS, Variant 2 CLAY; both general-purpose agents, default model)

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS)

**Position summary.** CLAY shows one real benefit: an early mechanical plan check. It is separable from the contested rule, so OURS takes it as a hybrid and keeps the poll read-only. The `hold:plan` label write adds only visibility, and it brings its own state and retry machinery with it.

**Steelman of CLAY.** On master nothing stops an empty assigned issue from spending a launch: PR 682 removed the approval code, and assignment is the only trigger (CLAY fact 9, from FULL-REPORT, not re-checked by this advocate). A mechanical check is therefore the only gate. A GitHub label is the cheapest and most visible mark; a person can remove it by hand and it stays removed (`orchestrator.md:446`). The write is narrow: add or remove one label, no comment (`orchestrator.md:444`). A refused write skips the issue and retries next cycle (`orchestrator.md:454`). `--dry-run` shows holds before any write (`orchestrator.md:461`). Switch-on never touches the 17 already-assigned issues (`orchestrator.md:492`). PR 686 rewrote the NG-2 test so the boundary is still enforced (`pr-a/tests/issue_watch/test_security_invariants.py:12`).

**Strengths claimed.**
1. The hold does not need the label. Row 4 skips with `held_incomplete` whenever `plan_check` fails (`orchestrator.md:455`); CLAY's own limit (a) says "a failing check holds the issue whatever the label shows" (`orchestrator.md:494`). The label only displays the gate.
2. The label forces extra machinery: rows 5 and 6, the `hand_removed` state, the live `gh issue view` read, the `holds` store and the label-creation path (`orchestrator.md:445-446`, `:456`, `:486`).
3. The boundary is an owner decision and a tested rule: NG-2 (`issue-watcher.md:76`), D2 (`issue-watcher.md:41-43`, `:48`), master tests (`issue-watcher.md:561`), requirement R24 (`requirements.md:50`).
4. The plan request and the plan body write need no poll write rights: the request is a wake-file item (`orchestrator.md:478`), the body write is the coordinator's under grant `issue.body.append_plan_sections` (`orchestrator.md:480`). The poll's only GitHub write is the label (`orchestrator.md:444`).
5. The visibility gain is small under OURS: `status` and the audit log already show `held_incomplete` (`orchestrator.md:490`). That any other person reads the label is UNVERIFIED.

**Weaknesses identified in CLAY.**
1. The cost is real: section 4.11 spans `orchestrator.md:436-495` and `test_hold.py` was added; the poll becomes stateful about unclaimed issues.
2. CLAY leans on missing gates yet asks for write rights; limit (a), a label seen one cycle late, is mitigated only by extra live reads (`orchestrator.md:456`, `:494`).
3. The one-hour plan request pulls the poll into orchestrator routing (free places, three-issue limit, `plan_stuck`, exit 7; `orchestrator.md:478-484`); CLAY concedes it depends on D07.
4. CLAY's strongest premise is about master, not the owner's line: the owner's local branch has `Approved` plus trigger label as the gate (R35).
5. A plan with three non-empty headings passes (`orchestrator.md:494(b)`), so the hold guards only against empty issues.

**Concessions.**
- X-002: the absolute wording ("the poll stays read-only", "the watcher never creates labels") needs trimming. The owner's local code already writes labels at first run (R11 "the per-project init creates them", `requirements.md:42`; Task 20 built, `requirements.md:90`). Whether that init runs unattended was not confirmed by this advocate.
- X-003: adding an existing label is idempotent, so "repeats every cycle until noticed" overstates; a wrong-issue or wrong-repo write still repeats.
- X-001: the human gate is local and unpushed; on master CLAY's point stands.
- OURS fact 9 about Jay's system is UNVERIFIED and should not count.
- A plan-less issue is not marked on GitHub under OURS: a real visibility loss.

**Shared assumptions.**
- A-001 QUALIFY: three headings guard only against empty issues (`orchestrator.md:494`); the check is a floor.
- A-002 QUALIFY: an assigned issue with no plan may be a deliberate request for a plan; a local plan-request item is worth keeping and the hold must not delay it silently.
- A-003 QUALIFY: one poll per repo matters only if the poll writes; whether two workspaces share the store is UNVERIFIED.
- A-004 QUALIFY: `requirements.md:97`, `:110` show login stayed under cron, not write scope; write scope is UNVERIFIED.

**Per-point positions.** S-001 neutral; C-001 OURS (adopt check read-only as hybrid); C-002 OURS (no poll label write; if a label is wanted the coordinator writes it under a grant row); C-003 CLAY on visibility only; C-004 OURS; C-005 neutral (D07); C-006 OURS; C-007 CLAY on master; X-001 neither (different trees); X-002 CLAY, narrowly; X-003 CLAY on idempotent add, OURS on wrong-issue repeat.

**Proposed rule change if the owner still wants the label:** the poll stays read-only; a separate coordinator step writes `hold:plan` under grant `issue.hold`, one add and one remove, and the `holds` machinery stays out.

### Variant 2 Advocate (CLAY)

**Position summary.** The mechanical plan check and the `held_incomplete` skip are a clear benefit and both sides accept them. The `hold:plan` label write is a narrow, tested, reversible benefit (visibility on GitHub), worth adopting only as a small amendment: NG-2 changes to allow one named poll write, and D2 stands unchanged. The plan request and the lease comment are not poll GitHub writes and should be judged on their own.

**Steelman of OURS.** The unattended poll is the one component nobody watches, so it should be unable to change GitHub state. NG-2 is a tested boundary (`issue-watcher.md:76`; master tests at `:10`, `:245-251`, `:693-698`). The least-privilege chain is consistent: workers never write (WC-9), only the orchestrator writes in `sc-issue-protocol` (`claim.md:9`), completion writes need a grant row (R24). The search index can be one cycle late (`orchestrator.md:456`, `:494`). The write drags in about 60 lines of rules, a four-state `holds` store, four evidence reads and eight audit reasons. OURS also has a human gate (R35) and visibility can live in `status` and the audit log. OURS concedes the read-only `plan_check`.

**Strengths claimed.**
1. The gap on master is real: PR 651 only adds template sections (per Clay's paper, not re-read); section 4.11 states the rule (`orchestrator.md:438`).
2. The write is the narrowest possible: add or remove one label, no comment (`orchestrator.md:444`, `:463`); a person always wins (`:446`, `:456` row 5).
3. Behaviour is specified end to end: `hold_write_failed` skipped and retried (`:454`); `--dry-run` writes nothing (`:461`); switch-on baseline (`:492`).
4. The stop switch needs no config: `hold:backlog` is person-set and poll-read (`:445`, row 1 at `:452`).
5. D2 is not breached: it names assign, comment and Project moves; a label add is none of them. Only NG-2 needs an amendment.
6. OURS is not absolute: the owner's local branch already builds `gh label create` in the poll package (`claim-handoff-planb/.../issue_watch/repo_init.py:72`, `:108`).
7. Repeat risk is smaller than stated: add is idempotent; the entry is dropped once the check passes (`orchestrator.md:453-454`); call budget bounds the rest (`:476`).
8. A launch spent on an empty issue costs money; OURS' accuracy check runs after launch (not independently re-verified).

**Weaknesses identified in OURS.**
1. Its human gate sits only in an unpushed local tree (R35); PR 682 and issue 655 not verified by this advocate.
2. Its "nothing writes" framing is wrong against its own code (`repo_init.py:72`, `:108`; R11 `requirements.md:42`).
3. Its alternative is invisible to non-owners: `status` and the audit log are local.
4. Its fact 7 overstates risk; the real risk is a wrong-issue write, which pure `plan_check` and the grant bound.
5. OURS has no early plan guard at all (it concedes this).

**Concessions.**
1. The poll's only GitHub write is the label; plan request is a wake-file item, plan body is the coordinator's, lease comment is the orchestrator's; they must not be used to justify the label.
2. The state machinery is large (`holds` store, E1 to E4, `plan_stuck`, plan records; `orchestrator.md:467-486`); the label alone does not justify all of it.
3. Section 4.11 has the poll create the label (`orchestrator.md:444`), contradicting R11; creation should move to the init path.
4. The visibility benefit is partly replaceable by `status`; if a human gate lands on master the label's marginal value falls.
5. The label can lag one cycle (`orchestrator.md:494`).
If the owner's weighting is applied strictly, the label write alone is a close call that may tie, and a tie goes to OURS.

**Shared assumptions.** A-001 QUALIFY (floor, not quality gate; `orchestrator.md:494`). A-002 QUALIFY (plan-less issue may be a deliberate request; hold right only if a plan request or person follows; depends on D07). A-003 QUALIFY (design covers a second poll on the same store, not two workspaces with separate stores; make one poll per repo a stated rule). A-004 QUALIFY (`requirements.md:97`, `:110` show login stayed under cron, not label write scope; test before adoption).

**Per-point positions.** S-001 tie; C-001 CLAY for naming the check as the gate but separable, adopt as hybrid; C-002 CLAY conditionally under the narrow grant (weakest CLAY point, could tie); C-003 CLAY; C-004 OURS for now (separable, heavy, topology-dependent, defer to D07); C-005 neither; C-006 CLAY on bounded retry with live read; C-007 tie (name the tree); X-001 tie; X-002 CLAY; X-003 CLAY on idempotence, OURS right on wrong-issue risk.

**Proposed rule change (hybrid).**
1. Poll: one write only, add or remove the existing `hold:plan` label, under grant `issue.hold`, no comment. NG-2 amended to say exactly this.
2. Poll may not create labels; per-repo init does (R11).
3. Person: places `hold:backlog`, may remove `hold:plan` by hand.
4. Coordinator or orchestrator: plan body writes and lease comments, under grant rows (R24).
5. Ship read-only `plan_check` plus `held_incomplete` first with the dry-run shadow run; enable the label write only after the R21 write-scope test passes.

## Round 2: Rebuttals

Common ground after Round 1 (both advocates stated it): (a) read-only `plan_check` plus the `held_incomplete` skip is adopted; (b) the plan request and the lease comment are not poll GitHub writes and are deferred to topology (D07); (c) the poll must not create labels (init does, R11); (d) `hold:backlog` is person-set and only read by the poll. Remaining dispute: may the poll itself add and remove `hold:plan` (C-002, C-003, C-006)?

### Variant 1 Advocate (OURS), rebuttal

**Response to CLAY.** CLAY's strongest point is visibility: the label is the only GitHub-visible hold mark (`orchestrator.md:490` lists three places a hold shows; `:463` ruling 33 "hold label only, no comment"). OURS accepts the visibility gain is real, with two limits: the ruling's owner authority is UNVERIFIED so it cannot decide the outcome, and no evidence shows anyone reads the label (the login `ironbelly` is shared, A-005; R19 names `clayphi` as a second approver but nothing shows they look at `hold:plan`). A benefit nobody has shown to be used is a tie, and a tie goes to OURS.
On X-002: master's design has the poll create the label (`orchestrator.md:444`), pinned by PR A (`test_security_invariants.py:12-14`). In the owner's local code the cron loop never creates it (`dispatch.py:72`, `:353`; `repo_init.py:5`; R11 `requirements.md:42`); only the first run calls `ensure_trigger_label`. The owner's code writes a label definition once per repo at first run, not a per-issue add or remove each cycle. Whether first run is unattended is UNVERIFIED (R18 `requirements.md:44` says "automatic").

**Test of the coordinator-writes alternative.** A held issue is never sent to an orchestrator (`orchestrator.md:459`), so no wake reaches the coordinator. Options: (1) a new wake item per held issue, which needs its own acknowledgment, re-delivery and `abandoned` rules (`:478`, DQ2 `:112`) and a model turn for a two-call job; (2) the coordinator reads `issue-watch status --json` from the poll's `holds` store (`cycle.py:2094`) but is event-woken, not a loop; (3) a second cron script that writes the label, which is a second poll with write rights. The `hand_removed` state (row 5, `:456`) must live with whoever writes the label. The alternative fails on simplicity; if the label is ever wanted the narrowest form is CLAY's: the poll adds or removes one label and creates nothing, behind an amended NG-2.

**R21 check.** `requirements.md:49` (2026-11-18) says "gh login under cron is not yet tested" (stale). `:97` (2026-11-20, Task 27) says `gh auth status` under `env -i HOME PATH=/usr/bin:/bin` stayed logged in; `:110` repeats it, R21 still open for the Coder repo (cron install). The login under cron was tested; label write scope was not (UNVERIFIED; no label add or remove under cron is shown).

**Final positions.** C-002: OURS (the poll stays read-only in this decision; ship `plan_check`, `held_incomplete` and the dry-run first; the label is a later amendment, not a rejection). C-003: CLAY on the fact, OURS on weight (nobody has shown the label is used). C-006: CLAY that it is bounded; it is a cost of having a label and adds no benefit on its own.

**Concessions.** (1) The wording "the poll stays read-only" should read "the poll writes no GitHub state in this decision". (2) The coordinator-writes alternative is harder than the poll writing; withdrawn as the preferred fallback, and CLAY's narrow poll write named as the right fallback. (3) The poll must not create the label, and PR A's test changes from three calls to two (agreed by both). (4) A plan-less issue loses its GitHub mark under OURS: a real visibility loss, accepted as a tie.

### Variant 2 Advocate (CLAY), rebuttal

**Response to OURS.** Visibility is unproven and no evidence closes the gap. No source shows anyone reading or filtering on `hold:plan` (`B-open-issues.md:58` and `D-master-code.md` only record where the label is defined). `orchestrator.md:490` is the design describing itself. Ruling 33 "as Jay does" (`:463`) is unverified (ruling authority and Jay's system not checked). Indirect evidence only: FULL-REPORT lines 98 and 118 show local-only state caused blindness between the two people, about the rebuild and not about holds. By the owner's bar the visibility benefit is a plausible claim with no measured use; conceded as a tie.

**Capability test.** Seeing a hold without local access: real but unmeasured (`status` and the audit log are local). Clearing a hold in the GitHub UI: NOT supported by the design; a hand-removed `hold:plan` becomes `hand_removed`, the issue stays unwoken while the check fails (`orchestrator.md:456`, limit (d) `:494`), so removal stops the plan request and does not release the issue; that claim is withdrawn. A person placing `hold:plan` by hand adds nothing. The person's stop switch is `hold:backlog`, which needs no poll write. Unique effect of the label: a poll-made hold becomes visible on GitHub.

**Cost and switchability (PR 686 head `pr-a`).**
- Cost of the write: `LabelWriter` about 87 lines (`github.py:983` onward); `_hold_write_ok` and `_label_write` (`cycle.py:1021-1044`); the `hand_removed` store state and the live `issue_labels` read; `test_security_invariants.py` pins three label calls; about 22 of 58 tests in `test_hold.py` touch label writes, grant, hand removal or dry-run (rough count by test name). FU-3 (`orchestrator.md:967`) says the poll token needs issue-write scope; label write scope under cron is untested (R21 covers login only).
- A switch exists: every hold write is gated by the `issue.hold` grant in `repos.yaml` (`cycle.py:1024`, `orchestrator.md:300`); `test_hold.py:416-426` asserts that with no grant the poll writes nothing and wakes nothing. So the write can ship dormant and be enabled per repo with no code change.
- The off state is not clean (verified by the moderator at `cycle.py:1021-1027` and `test_hold.py:416-426`): with no grant, a failing issue emits the warning `hold_write_failed` instead of `held_incomplete`, and the test asserts that warning. No store entry is made, so the one-hour plan request cannot start; a person-placed `hold:plan` on an issue that now passes would be skipped forever because the removal write is refused (row 3; the stranded-label part is inferred, not run).
- Removing the label from PR A is not free: rows 3 to 6, `hand_removed`, the plan request timer (row 6 needs the label) and the NG-2 test all assume it; rework of 4.11 crosses into D07 and was not sized.

**Final positions.** C-002: the poll, as a narrow write behind the `issue.hold` grant, ships dormant and is switched on only after the dry-run and an R21 label-write test pass; NG-2 amended to say "one named label, only under the grant, never created by the poll". C-003: tie (conceded). C-006: bounded but a cost of the label; neutral. Label write: ship the code dormant now and enable later; if the owner wants the strictest reading (no label code in PR A) CLAY does not object but marks the 4.11 rework as unsized. Either way the plan check and `held_incomplete` ship first and the off state gets a fix (no grant: row 4 skips as `held_incomplete` without a warning; row 3 ignores the label).

**Concessions.** No evidence shows anyone reads `hold:plan`. The "person clears a hold in the UI" capability is wrong. The poll must not create the label. The state machinery is large and the label alone does not justify it. The dormant form in PR A warns every cycle and can strand a label (a defect). The label can lag one cycle (`orchestrator.md:494`).

## Scoring Matrix (diff points after Round 2)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | Tie | 90% | Same skeleton; both advocates neutral |
| C-001 | HYBRID (adopt read-only check) | 92% | Both advocates adopt `plan_check` plus `held_incomplete` read-only; OURS concedes the gap, CLAY concedes separability |
| C-002 | OURS on timing, CLAY on form | 62% | Both: no live label write now; narrow poll write behind the `issue.hold` grant is the fallback form; split only on whether the code ships dormant in PR A (unresolved) |
| C-003 | OURS (tie goes to OURS) | 75% | Both concede visibility benefit is plausible and unmeasured |
| C-004 | OURS | 90% | Both defer the plan request timer to the topology decision (D07) |
| C-005 | Tie (D07) | 90% | Lease is the orchestrator's, not a poll write |
| C-006 | Neutral | 80% | Cost of having a label; adds no benefit alone |
| C-007 | Tie (name the tree) | 85% | Master has no human gate; the owner's local branch does |
| X-001 | Tie (name the tree) | 85% | Same as C-007 |
| X-002 | CLAY narrowly | 85% | Owner's local code creates a label once per repo at first run; no per-issue write in the cron loop (`dispatch.py:72`, `:353`) |
| X-003 | CLAY on idempotent add; OURS on wrong-issue repeat | 80% | Both advocates agree on the split |
| A-001 | QUALIFY (both) | 95% | Floor, not a quality gate |
| A-002 | QUALIFY (both) | 90% | Plan-less issue may be a deliberate plan request |
| A-003 | QUALIFY (both) | 85% | One poll per repo must be a stated rule if the poll writes |
| A-004 | QUALIFY (both) | 90% | Login under cron tested; label write scope not |

## Convergence Assessment (after Round 2, before the invariant probe)

- Points resolved: 14 of 15 (C-002 split on timing of the code, not on the rule)
- Alignment: 93%
- Threshold: 80%
- Status: CONVERGED pending the taxonomy and invariant gates
- Unresolved points: C-002 (whether the dormant label-write code ships in PR A now or later)
- Taxonomy coverage: L1 (S-001) covered, L2 (C-001, C-002, C-003, C-005, A-001, A-002, A-004) covered, L3 (C-004, C-006, C-007, X-001, X-003, A-003) covered. Gate passes.

## Round 2.5: Invariant Probe (independent fault-finder)

Full table: `invariant-probe.md` in this folder. Summary: 2 HIGH UNADDRESSED (INV-001, INV-002), 6 MEDIUM UNADDRESSED (INV-003 to INV-008), 2 LOW (INV-009, INV-010).

**Gate result before moderator action: CONVERGENCE BLOCKED** by INV-001 and INV-002 (HIGH, UNADDRESSED).

**Moderator verification and resolution (unattended mode: no further debate round is allowed at standard depth, so the moderator verified the HIGH items against the sources and records the outcome; this is a moderator resolution and was not debated by the advocates):**

- INV-002 VERIFIED and CORRECTED. `predicates.approval_of` is still called on master: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/cycle.py:883` and `:998`. The PR 686 head has zero `approval_of` references (grep count 0 under `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch`). So "master has no human gate" (consensus item 5, C-007, X-001, CLAY fact 9) is wrong for master's poll: the poll on master still requires the approver's label before it claims. What is gone on master is the post-claim plan approval (PR 682 deleted the `issue_pipeline` package). The tree with no human gate at all is the PR 686 head and the design in PR 681. C-007 and X-001 are restated: the spec names a commit and a design, not "master". Status: ADDRESSED by correction.
- INV-001 REASONED (the local code claim is agent-reported, `predicates.py:275-297` and R19 `requirements.md:45`, R36 `:62`; the moderator did not re-read `unchanged_since`). By the owner's own rule R19 and R36, an edit to the body after an approval voids it (`edited_after_approval`) and that rule stays. A held issue that a person then fills in therefore needs a fresh approval. That fails closed and follows from an existing owner decision, so no new decision is needed, but the spec must say it and must state that `plan_check` is evaluated before the approval read so that an empty issue never launches. Status: ADDRESSED by an existing owner rule, written into the verdict as a spec line. Residual UNVERIFIED: the local branch has no hold code, so the exact ordering is not tested.

After these two resolutions no HIGH item remains UNADDRESSED. The six MEDIUM items are logged as warnings and become spec lines or follow-ups (see VERDICT): INV-003 grant is document-level and the no-grant path also skips at the live re-read (`cycle.py:1299-1300`, agent-reported); INV-004 `plan_check` strips only HTML comments, so an unfilled `<...>` template passes (moderator verified `hold.py:69-70`, `:140` and the template `issue-bug-simple.md:43-62`); INV-005 exact heading match and the repo's issue forms have no plan fields (agent-reported); INV-006 a failing label write is not remembered and costs calls each cycle (agent-reported, partly UNVERIFIED); INV-007 reading the body conflicts with the owner's no-body rule NFR-002 and master doc `issue-watcher.md:226` (agent-reported); INV-008 two workspaces polling one repo reset the `hand_removed` memory (agent-reported).

## Scoring Matrix (final, after the invariant probe)

Unchanged from the Round 2 table, with these updates: C-007 and X-001 restated as "name the commit" (confidence 90%); A-003 stays QUALIFY and now carries INV-008 as evidence that one poll per repo must be an enforced rule if the poll writes.

## Convergence Assessment (final)

- Points resolved: 14 of 15 (C-002 split on whether the dormant label-write code ships in PR 686 now or later; both sides agree on the rule text)
- Alignment: 93%
- Threshold: 80%
- Invariant gate: initially BLOCKED (INV-001, INV-002), cleared by moderator resolution recorded above
- Taxonomy gate: passes (L1, L2 and L3 all covered)
- Status: CONVERGED with one unresolved point and two moderator-resolved HIGH invariants
- Unresolved points: C-002 (timing of the dormant code)
