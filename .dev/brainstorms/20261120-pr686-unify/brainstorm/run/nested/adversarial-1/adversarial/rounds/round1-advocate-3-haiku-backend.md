# Round 1 advocate: V3, backend

## 1 Position summary

V3 is the strongest starting point for failure recovery: it separates an uncertain claim launch from delivery of an adoption message, makes saved state a condition of acknowledgment, and refuses real work before binding is proved. Keep that operating contract, but borrow V1's separation of machine state from git and V2's readable stages and mechanical checks. I do not defend V3's reversal of the settled plan-check reference or its claim-session workaround as sufficient isolation.

## 2 Steelman of V1

Source V1: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/variant-1-opus-architect.md`.

V1's strongest argument is that a clean ownership model removes whole failure cases rather than merely retrying around them. Section 3 K1 puts the claim inside the coordinator's own session, explicitly to achieve "One agent per worktree". This is stronger isolation than V3's instruction that the standing coordinator stay read-only. V1 does not silently replace the built route: it keeps claim mode until a live test establishes the alternative.

V1 also genuinely gets the storage boundary right. Section 3 K5 says "All machine state" belongs outside a git checkout, while human-readable records remain on the records branch. This prevents worktree removal, branch changes and accidental staging from becoming ordinary runtime hazards. Its section 3 K15 names waiting_reapproval, excludes it from capacity and gives the poll responsibility for waking a new round. Its section 5 S12 keeps merge, consent validation and gate checks as one tested unit. These are substantive strengths, not presentation preferences.

## 3 Steelman of V2

Source V2: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/variant-2-sonnet-analyzer.md`.

V2's strongest case is that a small team needs reviewable changes with visible stopping points, not just a correct destination. Section 5 S11, S12 and S13 separate plan holds, configuration and status, and wake transport. The last part is explicitly "wake transport only" with wake_enabled false by default. Its MC-1 through MC-10 put import compatibility, missing-state acknowledgments, the read-only poll and the reasons table on the review checklist. S6 binds the revert trial to a recorded master head and repeats it if that head moves. S8 distinguishes a host installation from a repository merge.

V2 is also right to put the independent sweep contract and saved session fields early, at S5, rather than making them wait for coordinator recovery code. A skill that stops at "PR ready, person merges by hand" in S15 has real rollout value. I would retain these review boundaries even where the final build order follows V3's closer reading of the settled O4, O5 and O6 groups.

## 4 Strengths claimed

Source V3: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/variant-3-haiku-backend.md`. Variant citations below name sections and rows in these three source files. They describe proposals, not passing tests.

1. **Recovery separates a launch from its notification.** V3 section 4, Integrity rules, says "Separate claim attempt from adoption delivery" and keeps the wake id on replay. Section 8 names tests for a lost launch receipt and for a crash after the claim marker but before wake publication. That distinction prevents a delivery failure from becoming another claim launch. The built starting point really does save pending state before launching, then classify an uncertain result as unknown: `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/cycle.py:1090-1109`. V3 extends that pattern; it does not claim a new outbox already exists.

2. **Acknowledgment has a concrete saved-state contract.** V3 section 4 requires matching repository, issue, target and round; a duplicate cannot overwrite a newer round; the poll checks that the referenced state exists before accepting success. It also specifies lock ordering and release before delivery. V1 and V2 preserve the basic state-before-ack rule, but V3 gives implementers the surrounding rules needed when a process dies or messages arrive twice. This is safe repetition, not a promise of exactly-once delivery.

3. **File integrity reuses real code rather than adding infrastructure.** V3 section 4 requires exclusive creation, temporary replacement, flushing the file and its containing directory, and bounded validated JSON. The existing wake writer already checks size, creates an exclusive no-follow temporary file, flushes it, replaces the target and flushes the directory: `/home/coder/.cache/ic-snap-20261120/pr-a/src/superclaude/cli/issue_watch/wake.py:269-299`. Reuse that pattern with the missing state and acknowledgment checks. This is a small-team alternative to introducing a database or message service, not proof that the present writer makes multiple files transactional.

4. **Unproved binding means no real issue.** V3 section 5 S9 requires the live guard probe before enablement, and section 8 names binding as HIGH risk. The owner's controlling sentence is "Before any other issue runs through the flow, the worker must be bound to the guard" at `/home/coder/.cache/ic-snap-20261120/master/docs/designs/issue-pipeline-guard-g2.md:9`. V3 does not turn the earlier one-issue exception into standing permission.

5. **A restart does not restore spent consent.** V3 section 2, Coordinator, requires reconciliation of an uncertain merge before reuse; section 4 says startup reconciles consumed goes before new work. A local retry must first establish what the remote service actually did to the authorized head. Both other variants demand one-shot consent, but neither describes this recovery boundary as explicitly. Keep V3's stronger rule that consumed consent never becomes fresh permission after restart.

6. **The tests follow actual failure boundaries.** V3 section 8 pairs each failure with a required safe result: unknown launch means no second claim, missing state means no acknowledgment success, restart count survives a crash, unreadable process data means no new start. Section 5 S6 and S7 then put state integrity before the complete merge unit. That is more actionable than a general instruction to add crash tests, and all of it remains explicitly unbuilt.

## 5 Weaknesses identified in V1 and V2

1. **V1's unbound real-issue route loses to the owner's rule.** Section 5 S11 expressly permits real issues "unbound and flagged" before the live probe. A person's go under that proposed route is not evidence that the owner changed the existing G2 restriction. The controlling G2 sentence is quoted in section 4 above. V3's disabled-until-proved path wins C-003 and X-002. This resolves a conflict between existing texts; it does not reopen the settled guard verdict.

2. **V2 gives the binding switch incompatible meanings.** Section 3 K14 permits a real-issue start after a throwaway run while still describing "unbound starts"; section 5 S15 says false "keeps real issues off until the probe". One operational switch needs one truth table. Use V3's rule: no real issue without proved binding, with the separate governed-claim gate still closed. V2's stronger S15 wording should replace K14, not coexist with it.

3. **V2 mixes a mutable permission token with tracked evidence.** Section 4 layout row 14 tracks records, and row 17 puts the one-shot merge go inside them. Restoring an older git revision could restore an apparently unused token unless a separate durable consumed record prevents it. I am identifying a missing recovery rule, not claiming a demonstrated exploit. V3's local consumed-state rule and V1's outside-git runtime layout are safer; quoted owner evidence may still be retained separately. Being ignored by git does not make a file tamper-proof.

4. **V1 pays for two claim meanings before the second is proved necessary.** Section 3 K1 adds claim and wake modes and a second route whose live feasibility is explicitly open. It has a genuine isolation benefit, as the steelman says. For the first rollout, however, V3 and V2 retain one claim owner and make the wake an adoption message. Choose that smaller contract only after fixing claim-session overlap, rather than presenting either mode as ready today.

5. **V1 makes the sweep a watcher collector without an established need.** Section 3 K10 adds a status subprocess and a watcher block; section 5 S10 adds an all-repo status interface. The settled rule is one source of session state, not one file for every domain: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D11/VERDICT.md:17-28`. V2 and V3 preserve that distinction with a named status feed to the screen. V1 need not make a GitHub call to widen the sweep's collection contract, so the objection is added responsibility, not a false allegation of a GitHub write.

6. **Neither competing account is as explicit about recovery after an external effect.** V1's section 5 MC-6 and V2's MC-6 test missing-state acknowledgments, which both get right. Their stage descriptions do not state V3's paired requirements to replay a saved adoption message after claim and never repeat an unknown launch. V2's stored restart counter is good, but it is not the same test as killing the process at each write boundary. Import V3's boundary tests rather than expanding the system with another recovery service.

## 6 Concessions about V3

- **Its prose is too compressed.** Section 7's "Both gates: S2 restoration" makes the reader reconstruct the question, consequence and authority. Replace grouped shorthand with V1's full questions, alternatives and effects. Expand each grouped migration row into independently reviewable changes where it contains several PRs. Eleven rows are not evidence of eleven small changes.
- **Its plan-check reference is wrong for this merge.** Section 2, Issue claim to work pipeline, makes the package canonical. The settled R-2 names the script check as the single definition: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md:28`. Adopt V1/V2's script-reference, package-copy and shared-fixture parity arrangement. Package isolation is a valid concern, not authority to reverse the decision.
- **Its claim-session workaround is not isolation.** Section 2's read-only standing coordinator and section 3 K9's "claim ends before coordinator writes" still leave two live agents sharing a worktree. A marker is expressly not completion. Require proven lifecycle separation before the standing coordinator begins, or a separate claim worktree. If neither can be proved, keep this path off; do not quietly switch to a different claim owner.
- **Its machine state should move outside the checkout.** Section 4 distinguishes ignored runtime from records, which is better than tracking mutable go entries, but V1's outside-git state root better survives worktree cleanup. Retain V3's schemas and recovery rules, not its host-specific illustrative layout.
- **Its outbox is a design requirement, not a complete transaction design.** Section 4 does not fully define how saving claim evidence and saving delivery intent become recoverable together. Put both in the existing dispatch store under its lock, or specify the exact reconciliation rule before coding. Test each partial-write case. Do not claim two separate atomic renames make one transaction.
- **Its rollback and rollout descriptions need precision.** Section 5 says disable consumers and retain files, but that alone does not prove an older loader accepts extended config or state. Borrow V2 S12's compatibility caution, with a version-pair test before rollback. Move the independent sweep fields earlier as V2 does. Keep V3's O4 substrate, O5 complete merge unit, O6 integration order; a fixtures-only review does not authorize live work.
- **Its small-team boundary needs to be explicit.** Retain the existing local store, one host, one issue in flight and the necessary crash tests. Do not add distributed leases, a general recovery framework or speculative claim modes. Binding timeouts and round limits remain proposals, not measured defaults. D16 proposals can be recorded as proposals, never promoted to a settled verdict or consent.

## 7 Responses to A-001..A-005

- **A-001: QUALIFY.** A standing session is a convenience, not a durability guarantee. V3 section 4's startup reconciliation is the right basis, but it needs a context-exhaustion and restart test that reconstructs issue, round, approval binding, worker identity and consumed consent without relying on the previous conversation. Missing or contradictory state must stop new actions. Do not promise that compaction preserves authority or that files prove a remote merge outcome without reading the remote state.
- **A-002: REJECT.** None of these proposals proves that worker-start always creates a distinct worktree. V1 section 8 RK-11 explicitly calls it unobserved. Require recorded worker and coordinator worktree identities, unequal resolved paths, and a live write-isolation check before real work. A capacity of one limits issue count; it does not isolate a worker from its coordinator.
- **A-003: QUALIFY.** Chat-only approval can work before the coordinator exists, but a future records directory cannot serve as today's evidence. From S0, the calling agent should record quoted words, date, scope, source session and recorder in the existing unified plan's owner-action section. Later coordinator setup must import or reference those same entries and test their readability. A file records an answer; it never supplies an answer or asks the owner to edit one.
- **A-004: QUALIFY.** Accept one polling host and one coordinator scope per validated repository identity, as V3 section 2's single-host limit states. Reject the extra inference that the repository has only one checkout: worker worktrees already require several. Forks must keep distinct owner/name identities, while multiple independent project scopes inside one repository and a second polling host remain outside the first rollout. No distributed lease is needed for this bounded first build.
- **A-005: QUALIFY.** Depth 0 is necessary but does not itself authorize PR submission. D06 separates the ordinary top-level PR route from the authorization for a script-started coordinator: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D06/VERDICT.md:18-20`. Require the approved contract wording to cover this session and duty, then verify the session is not an Orca worker and obtain the named push/PR go. Until that is settled, use a person-opened ordinary top-level session for PR submission. Never infer permission from the launch prompt or a passing gate.

## 8 POSITIONS TABLE

Confidence rates the recommended approach, not whether its unbuilt parts already work. HYBRID descriptions name the combination or the missing qualification. All five assumption answers above remain conditions of rollout.

| id | superior approach | confidence | one-line evidence |
|---|---|---|---|
| S-001 | HYBRID: V2 reviewable changes inside V3's O4/O5/O6 order | 90% | V2 section 5 S11-S13 isolates watcher changes; V3 S6-S8 preserves substrate, complete merge unit, then integration. |
| S-002 | V1 | 95% | V1 section 7 states full questions and consequences; V3 section 7's grouped fragments hide the question. |
| S-003 | HYBRID: V2 status tags plus V3's safe-repetition explanation | 90% | V2 section 2.0 separates built and proposed flow; V3 section 2 explains uncertain receipts and repeated delivery. |
| S-004 | HYBRID: V1 readable rows, V2 evidence, V3 validation rules | 88% | Each section 4 names writers and readers; V3 adds matching round/revision and boundary validation. |
| C-001 | HYBRID: V3 poll-owned claim/adoption, conditional on proved session separation | 82% | V3 section 3 K1 retains one claim owner; V1 K1 correctly identifies the shared-worktree defect. |
| C-002 | V1 | 93% | V1 section 3 K5 puts all machine state outside git; V3 section 4 still ties runtime survival to the worktree. |
| C-003 | V3 | 98% | V3 section 5 S9 requires live binding proof before enablement; V1 S11 permits unbound real issues. |
| C-004 | V2 | 98% | V2 section 3 K8 preserves the settled script reference and uses a package copy with fixture parity. |
| C-005 | V3 | 92% | V3 section 2 separates watcher status from sweep session facts without making sweep collect another domain. |
| C-006 | V2 | 94% | V2 section 5 S5 explicitly makes sweep fields and saved JSON independent of lanes 1 and 2. |
| C-007 | HYBRID: V2's three watcher changes with V3's recovery tests | 90% | V2 S11-S13 supplies review boundaries; V3 section 4 supplies replay and acknowledgment integrity. |
| C-008 | V3 | 89% | V3 section 5 S6-S8 follows substrate, one merge unit, then other integration; V2 S15 declares a deviation. |
| C-009 | HYBRID: V1 outside-git root with V3 consumed-go semantics | 95% | V1 section 4 go entry is local machine state; V3 section 2 forbids restoring consumed consent after restart. |
| C-010 | V3 | 96% | V3 section 4 distinguishes launch attempt, outbox replay, retarget generation, lock order and saved state before ack. |
| C-011 | V3 | 90% | V3 section 7 calls D16 wording a proposal; V2 section 5 S0 uses it operationally despite its unsettled status. |
| C-012 | V3 | 93% | V3 owner actions require an expiry answer and label proposed limits unmeasured rather than installing them as facts. |
| C-013 | V2 | 96% | V2 section 3 K15 explicitly limits label creation to person-run init on a chat go, never the poll or cron. |
| C-014 | HYBRID: V2 default-off wake key, V3 restraint on speculative claim modes | 86% | V2 S13 prevents wakes without a consumer; V3 section 4 needs no second claim-mode contract. |
| C-015 | V2 | 92% | V2 S12 explicitly warns rollback may require removing new config keys; V3's retained files alone prove no compatibility. |
| X-001 | HYBRID: V1's no-two-live-agents rule with V3 poll adoption only after isolation proof | 94% | V1 section 3 K1 removes overlap; V3 section 2 admits marker is not completion and offers only read-only coexistence. |
| X-002 | V3 | 99% | V3 S9 keeps real work off until proof; the controlling G2 owner sentence is quoted in section 4 above. |
| X-003 | V3 | 98% | V2 K14's unbound-start wording conflicts with S15; V3 requires one disabled-until-proved outcome. |
| X-004 | V2 | 98% | V2 K8 keeps the script as definition; V3's package-canonical sentence reverses settled R-2. |
| X-005 | HYBRID: V1 local runtime storage with V3 restart-safe consumption | 96% | V2 section 4 rows 14/17 track the go record; V3 separates consumed state from retained owner quotes. |
| X-006 | V3 | 94% | V3 section 2 watcher feed leaves sweep's session contract alone; V1 K10 adds another collector and schema block. |
| A-001 | HYBRID: V3 restart reconciliation plus an exhaustion recovery test | 94% | V3 section 4 names reconciliation but does not prove files alone restore a safe coordinator after exhaustion. |
| A-002 | HYBRID: V1's explicit uncertainty plus mandatory worker-path proof | 97% | V1 RK-11 marks worker worktree isolation unobserved; all variants need a live check rather than an assumption. |
| A-003 | HYBRID: shared chat-record fields in the existing plan from S0, then coordinator import | 91% | All variants' section 7 records answers; none names an available pre-coordinator record and later read path. |
| A-004 | HYBRID: V3 single-host boundary plus V2 repository identity across checkouts | 95% | V3 section 2 rejects cross-host guarantees; V2 section 3 K4/K9 keys one repo while requiring separate worker trees. |
| A-005 | HYBRID: D06-authorized ordinary session, otherwise a person-opened PR session | 94% | V3 section 2 requires the depth-0 amendment; D06 distinguishes that authorization from the top-level PR route. |

Coverage: 4 structural, 15 content, 6 contradiction and 5 assumption rows, 30 total. Recommendation: retain V3's recovery contract, correct its conceded defects, and use the stronger presentation and review boundaries above. No extra service, new claim mode or cross-host coordination is required for the first rollout. No live probes or runtime tests were run for this advocacy; their results remain unverified.
