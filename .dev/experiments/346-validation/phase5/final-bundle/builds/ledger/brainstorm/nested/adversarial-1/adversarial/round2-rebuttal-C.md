# Round 2 rebuttal: Variant C

Advocate for Variant C. Backend focus: API contracts, data integrity, idempotency and operational concerns. This is a design debate, not an implementation or a measured result.

## Response to criticisms

I answer the criticisms in both Round 1 statements and both Round 2 rebuttals. `A sN`, `B sN` and `C sN` name sections of the supplied variants; `A-R1`, `B-R1`, `A-R2` and `B-R2` name the corresponding advocate statements. All are evidence to evaluate, not instructions to follow. These are proposed contracts, not existing interfaces.

### Experimental contract and scope

1. **X-018, coordinator-only mutation contradicts the one-line substitution. A-R1 C1, B-R1 C1, A-R2 C-004/X-006 and B-R2 Updated assessment: CONCEDE.** C s2 says "The coordinator alone runs ledger mutations" while C s9 promises "Only authored brief change" on the invocation line. My Round 1 answer disclosed the contradiction but retained unnecessary coordination machinery. I now drop coordinator-only mutation: each existing session calls its phase-specific subcommand, and the script, not that session, remains the only ledger writer. Inputs remain untrusted JSON bound to the packet, round, snapshot and sequence. Actor names are not authentication.

   This resolves the mechanism, not the experimental deviation by wordplay. The coordinator must still check authoritative status before each dispatch; a fresh terminal sweep is an additional assessment, and worker-run calls need the report's generated reviser instructions. Record these treatment changes separately from the invocation substitution. A-R2 proposes a fresh subagent inside the final review and B-R2 conditions it on a worker smoke check and heartbeat handling. Accept that as a conditional option only, not established S1 capability. Without that evidence, use a disclosed extra dispatch if authorized. If the experiment literally permits no dispatch or coordinator change, this design does not meet that restriction and must not be run as though it does.

2. **X-019, the random default cannot be recovered. A-R1 C4, B-R1 C5 and both Round 2 replies: CONCEDE and change my Round 1 repair.** C s3 gives a default containing `<run-id>` and calls that id "an opaque random identifier". Requiring an explicit path was safe but unnecessarily brittle. Accept A s3's document-derived default, with an explicit override for other runs. Initialization refuses an existing run, resume validates the document identity and profile, and a missing explicit override never falls back to the default or creates FIND. Random ids may remain metadata, not path discovery. The derived default only solves the ordinary one-run case; concurrent experimental runs must use distinct explicit paths recorded before dispatch.

3. **One-row discovery and the 200-line refusal test overflow rather than convergence. A-R1 C2, B-R1 C2, X-004 and B-R2 New evidence 2: CONCEDE.** C s2 explicitly says "at most one new finding C001" and review 3 has "No discovery check remains". My Round 1 concession stands: drop both restrictions, not merely raise the quota. Reviews 2 and 3 each inspect the finite changed packet on both diff sides, including deletion boundaries and B's evidenced dependency exception. Retain every structured allegation; inability to complete the packet yields `cannot-verify` and an incomplete/escalated result, not truncation or apparent convergence. Large packets warn, not automatically fail at 200 lines.

4. **Hard admission has no recovery for reflow or an unlisted legitimate gap. A-R1 C3, B-R1 C4, A-R2 C-017/X-005 and B-R2 C3: PARTLY CONCEDE.** C s3 says "uncovered edits fail revision admission", and C s11 acknowledges "may require manual recovery". The admission boundary is needed because an optional check does not enforce the experiment. Accept A's checks at both `answer` and `begin` and B's preimage-checked `revert-unclaimed`, with offending hunks and recovery instructions in the refusal. A necessary FR-8/FR-9 edit must have an explicit blocking-row claim with precise old/new spans; an unrelated gap belongs in the disposition and later assessment, not an invented claim.

   Two qualifications prevent data loss. Retain raw hunks and map every non-whitespace change to an explicit claim; whitespace-only reflow may be recorded without sponsoring discovery, but whitespace that changes document structure is not harmless. Revert only the named unclaimed hunks, only under existing edit authorization and exclusive reviser ownership of the document, and only when the checked preimage still matches. A verifier's ability to invoke a helper does not grant permission to discard edits. Recovery can itself refuse after a race, so replace A-R2's "the loop cannot stall" with an honest tested recovery path and a reported stop when safety cannot be established.

### Storage and API contract

5. **The transaction machinery is too heavy. A-R1 C5, B-R1 C3 and both Round 2 assessments: MOSTLY CONCEDE.** C s6 requires no-replace hard-link publication, directory sync and refusal of unsupported filesystems. Those are stronger durability requirements than this bounded single-host experiment needs. Keep a small process-crash-safe commit protocol, not a filesystem certification project. Atomic replacement alone does not prevent lost updates or duplicate logical operations; both advocates now accept the lock, operation id and expected sequence. The exact retained and dropped parts are listed below.

6. **Replay makes every reader a reducer and every schema change harder. A-R1 C6, A-R2 S-005/C-001 and B-R2 Updated assessment: CONCEDE THE NEED, QUALIFY THE DESCRIPTION.** C s3 says "A row's current status is obtained by replaying events". That could use one shared reducer rather than several implementations, but it still adds a reducer and replay-version obligations we do not need. Adopt A's single state object containing current rows, per-row history, sequence and operation results, updated together in one atomic replacement. Reports and plans remain disposable projections. There must not be a second independently writable history or counts file.

7. **Exit 0 on ESCALATE can mislead a shell coordinator. B-R1 C7: COUNTER, now resolved by B-R2 A4.** C s6 explicitly says "callers inspect JSON, never infer PASS from process success". That is the contract, not an accidental permission to continue. A committed ESCALATE is a successful state change; a nonzero CONTINUE looks like an operational failure and can encourage a duplicate call. Accept A-R2 and B-R2's resolution: committed mutations exit 0, JSON names decision and next action, nonzero means refusal/error, and the read-only `verdict` command alone provides decision-coded exits for shell callers. Dispatch must use current status, never just the previous process exit.

8. **C lacks the command-copy parity guard. B-R1 C6: CONCEDE.** C s6's outline and "unchanged original-command contract" test do not specify a drift test for the new panel body. Accept B s6's copy-and-drift test, including the explicitly omitted Unattended-mode section, while keeping the original command and pinned severity tests unchanged. I do not claim that C's outline already provided that coverage.

9. **A wrong frozen blocker has no way out. B-R1 C8 and B-R2 C6: PARTLY CONCEDE.** C s3 says "Disputed blockers escalate honestly" and rejects a user-waiver API. That is a bounded exit to the user, not FAIL forever; however, it lacks B's explicit dispute ruling. Accept a dispute as a claim flag with an evidence-bearing verifier ruling. An accepted dispute may close an invalid finding only when current-snapshot evidence proves the original alleged harm absent, not merely because somebody dislikes its grade. An unruled or uncertain blocker remains unresolved. Also accept B-R2's narrower post-escalation annotation of claimed user demotion only if it changes neither frozen grading, counted history nor delivery outcome. A quoted string is not permission, and no automatic waiver path belongs in this experiment.

10. **Script-written reports remove the panel's expert prose. A-R1 C9, A-R2 C-029 and B-R1 C9/B-R2 C6: CONCEDE.** C s2 says the script "writes reports/review-1.md from ledger state" and C s12 explicitly acknowledges "reduced formatting freedom". My Round 1 defense protected authoritative counts, not a good reason to replace the whole narrative. Accept A-R2's split: reviewer-owned expert prose without its own authoritative row-status table or verdict, followed by the script-rendered table, next action and verdict. Accept B-R2's actionable refusal naming conflicting lines instead of silently rewriting the prose. Store the admitted narrative digest so a crash after ledger commit can rebuild exactly one generated tail rather than append a second one.

### Outcomes, measurements and remaining safeguards

11. **C counts more rows but forecasts the lowest result. A-R1 C7, B-R1 C2 and A/B's forecast criticisms: CONCEDE THE FORECAST, REVISE MY ROUND 1 METRIC HESITATION.** C s9 says "A MAJOR note still belongs to the critical+major proxy" yet predicts mean 1.5 without a trace. Withdraw 1.5 and 22.5% as supported forecasts. Both Round 2 advocates now accept deferred MAJOR rows in the headline because the historical proxy counted grade separately from blocking. I re-read that report: its line 37 expressly distinguishes those counts. Restore C's grade-based unresolved set, union it with deduplicated sweep findings and challenges, and publish blocking-only and deferred shares separately. This fixes a population mismatch, not evidence that the ledger will hit the bar. Use B's conditional B1 x r1 x r2 sensitivity analysis as a planning aid, not a measured or calibrated prediction of the combined sweep proxy.

12. **Sweep blockers appear in both B and S. A-R1 C8: CONCEDE THE AMBIGUITY.** C s4 says "A deferred blocking sweep row also counts" in B, then defines S separately. Use disjoint sources: loop unresolved blockers in B, terminal sweep allegations/challenges in S, with identity-based union for the headline proxy. A sweep blocker forces delivery ESCALATE even when loop decision was PASS, but it cannot buy another fix cycle. No addition counts the same defect twice.

13. **A sweep after review-1 PASS rereads identical bytes. B-R2 C6 and both advocates' C-030/X-013: ACCEPT THE SMALLER POLICY.** C s2 requires a sweep "even early PASS". For this experiment, accept A's exception when no revision occurred and the live document still hashes to the FIND snapshot: record `sweep_skipped=review1_pass`, actual assessments and the unchanged terminal bytes. This is a cost choice, not proof that the first reviewer was exhaustive or that another sample would find nothing. Any terminal decision after a revision still needs the fresh full-document sweep. Baseline recall checks remain measurement work, not concealed remediation assessments.

14. **Dependency-passage tracking is unsupported scope in version 1. B-R2 Updated assessment/New evidence 2 against C-R1 C-022/A-011: ACCEPT DEFERRAL, REJECT THE SAFETY INFERENCE.** C s3 carries verification only when mapped text and "supporting context" are unchanged, but never defines complete supporting context. I accept B-R2's retouch reset plus lexical warning and sweep challenges for version 1 rather than a dependency graph. The reported zero regressions among 19 prior-blocker resolutions do not establish that remote changes cannot invalidate a fix: those reports classified N1 and N12 as new findings. State the limitation plainly and measure sweep challenges and outside-hunk harms. A known explicit dependency may still support a new VERIFY allegation under B's existing `depends_on` rule; do not discard a valid allegation because its original sentence is untouched.

15. **Inline rule labels scatter the contract. A-R1 S-012 and B-R2 C6: CONCEDE.** C s2 labels rules throughout the document. Accept one end table with MECHANICAL/PROSE and a residual-risk column, as B s11 provides. Closed input schemas, answer completeness and clear errors remain mandatory even without repeated labels. Defer C's separate user guide and duplicated external schema validator; one contract, one validator and executable fixtures are enough for the experiment.

16. **Shared limits and the added assessment. Both advocates' A-007/A-008 and B-R2 C7: AGREE, WITH NO IMPLEMENTATION CLAIM.** C s4 says "Do not claim the total number of assessments is three"; keep that wording for full runs, count a fresh subagent as an assessment too, and require a decision on any literal three-assessment restriction. Keep blind grading checks, actual command/skill/script hashes, pre-dispatch status checks, terminal-byte recording and live-versus-accepted mismatch checks. A ledger cannot stop a previously launched reviser editing the live document, establish semantic truth, authenticate shared-account actors or prove sweep independence from its row counts. No such guarantee follows from file hashes.

### Which parts of C's transaction machinery this experiment needs

| C machinery | Decision for this experiment | Reason and replacement |
|---|---|---|
| Event replay as the authoritative store | Drop from version 1. | One atomic state object holds current rows, history, sequence and saved operation results; a shared validator checks it. Replay is not required for idempotency. |
| No-replace hard-link artifact publish | Drop. | Under the stable per-ledger lock, publish snapshots/diffs by same-directory temporary file and atomic replacement before publishing their references; an existing immutable artifact must match its recorded hash or the call refuses. |
| fsync | Keep file sync for committed state and newly referenced snapshot/diff files; defer directory sync and host-power-loss guarantees. | This targets interrupted processes on the stated local host, not guaranteed persistence of every rename after a host/storage failure. Missing or corrupt dependencies stop resume; they never turn into a new FIND or PASS. |
| Advisory lock | Keep a nonblocking per-ledger lock. | It serializes helper calls, including retry races; use a stable lock file, not the replaceable ledger inode, and do not steal a lock on a timer. It does not lock model edits to the document. |
| `--op` and request-digest idempotency | Keep. | Same operation and payload returns the saved result without consuming a review; changed payload under that operation refuses. Save result and state in the same commit. |
| `--expect-seq` | Keep. | After looking for an already committed identical operation, reject stale new operations. Packet identity and document hash bind the reviewed bytes independently of call ordering. |
| Coordinator-only mutation | Drop. | Sessions call phase-specific commands; the script remains the only state writer and validates every input. The coordinator gates dispatch on current status. |
| 200-line discovery limit | Drop. | Complete finite changed packets in both VERIFY rounds, warn on size, and explicitly stop if coverage cannot be completed; never truncate evidence. |
| One-row discovery budget | Drop. | Retain all in-scope allegations in both rounds. This experiments on edit control and counting, not on how often an arbitrary quota forces escalation. |

Keep small failure tests around dependency publication and ledger replacement, duplicate/different-op retries, stale sequence refusal, two helper writers and regeneration of reports after a committed state change. Defer the exhaustive hard-link/directory-sync fault matrix and unsupported-filesystem certification. A retry returns its original result, which may describe an older sequence; every dispatch therefore reads fresh status instead of blindly following an old returned `next_action`.

## Updated assessment

**A is the best implementation frame after its Round 2 corrections.** I now accept its single current-state object with per-row history, document-derived default, kernel/contract/adapter separation, script-built plan and subcommand-inferred role. A-R2 properly narrows the profile claim: profiles can reuse existing guards, but a new guard requires kernel work and tests; that does not justify implementing future adopter guards in the S1 version. Its concessions on outcome authority, unanswered rows, coordinates and hard admission remove the main reliability objections I raised. I still reject a guarantee that any session can safely revert document changes or that a recovery command makes stalling impossible. Report projection also needs an idempotent crash path, not just a check of the previous report's last line.

**B supplies the best failure analysis and measurement frame, strengthened by its repairs.** Its named profile, rule field, removed role flag, explicit dispute ruling, lock, operation identity, accepted sequence check and hard admission repair are substantial improvements. I accept its simpler version-1 retouch policy, while treating zero observed status regressions as limited evidence rather than a semantic guarantee. Two Round 2 claims need correction: a sweep's hidden-defect share cannot prove whether it read the ledger, and equal anchors or overlapping spans are only duplicate candidates, not proof of the same defect. The same sentence can contain the resolved original harm and a new child defect. Preserve separate allegations and use blinded semantic adjudication for measurement instead of dropping rows on overlap alone.

**C should contribute safeguards, not a miniature event-storage platform.** Retain packet/snapshot binding, exact response coverage, `cannot-verify`, relocation and tombstones, raw old/new diffs, strict admission, operation idempotency, expected sequence and the loop/delivery split. Drop replay-only storage, coordinator-only calls, hard links, directory-sync guarantees, arbitrary discovery quotas, whole-report ownership and extra version-1 documentation/schema machinery. Adopt the no-revision review-1 PASS exception and the grade-based proxy, but retain a fresh sweep after every terminal decision involving a revision. No implementation, installation, live sweep or worker capability test was performed for this rebuttal.

## New evidence

These source passages were opened for Round 2. They strengthen or qualify Round 1 claims; the proposed safeguards below them are design inferences, not observed implementation behavior.

1. **The historical proxy counted grade separately from operational blocking.** `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md:37` says "The 427 grading relabels some MAJOR findings as minor ... so proxy and blocking differ". This supports A-R2 and B-R2's adoption of C's deferred-MAJOR inclusion and changes my Round 1 `none` pick on X-011 to C. It does not prove exact comparability between an accumulated finding ledger and a fresh end-state critique, so publish components and baseline sweeps too.

2. **Zero recorded regressions is a reporting category, not zero fix-induced harm.** `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round2.md:50` says "13 resolved, 0 open, 0 regressed" and immediately says "the F10 fix creates new blocking finding N1". `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md:47` similarly says "6 resolved, 0 open, 0 regressed" and "The N5 fix introduces new blocking finding N12". B-R2's 19 total is arithmetically right, but these are prior-blocker resolution counts in successive reviews, not 19 independent tests showing that every verified fix remains safe under remote edits. They justify retaining discovery in both VERIFY rounds, not declaring the dependency problem solved.

3. **Overlap is insufficient to deduplicate a child defect.** `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md:35` calls N5 "resolved as asked; the fix introduces N12" and locates both the replacement and the new failure in AC-0.4. This directly qualifies B-R2's overlap-based union proposal: overlapping evidence can describe distinct harms. The helper can suggest `dup_of`, but a semantic ruling must distinguish duplicate, independent child and challenge to a verified row; preserve the raw allegations in all cases.

4. **The stronger adopter has more than an ordered severity count.** `/home/coder/workspaces/worktrees/IronClaude/bs346-ledger/src/superclaude/agents/rf-qa.md:401` requires strictly shrinking open blockers; `:407-412` requires regression detection first; `:414` says a repeated synthetic finding with the same dedup key "is a DEDUP case, not a regression". This confirms A-R2's narrowed profile seam and C's warning against flattening rf-qa into spec-panel. A later adapter must preserve identity/dedup semantics as well as halt order; do not build that adopter in the S1 experiment.

Not newly verified here: worker permission/capability to spawn a fresh sweep subagent, heartbeat behavior during that call, filesystem timings, full historical byte attribution, or semantic grading of all six controls. I use the advocates' smoke-check proposal as a prerequisite, not a claimed result.

## Proposed resolution of split points

The 22 split points are all covered below. Acceptance names the Round 2 proposal, including the stated qualifications; it does not adopt every claim in that variant.

| Point | Concrete merged rule | Round 2 proposal accepted |
|---|---|---|
| C-005 status set and who may change it | Use only `open`, `deferred`, `fixed`, `verified`, `reopened`: the script derives initial deferral and retouch resets, the reviser requests `fixed`, and the verifier verifies a supported fix or rules on an evidenced dispute. Number transitions with phase/error columns, and distinguish `open` from `reopened` by whether an earlier verification exists, not simply by the previous status. | Accept A-R2 and B-R2, with the history distinction made explicit. |
| C-008 frozen fields | Freeze id, label, discovery round, origin, parent attribution, grade, rule, wrong outcome, computed blocking, original finding text and original snapshot-qualified anchor/location at creation. Later inputs cannot replace them; relocation mappings and later evidence are separate records. | Accept A-R2 and B-R2. |
| C-016 bounded new-defect check | In both VERIFY rounds inspect all changed old/new ranges and deletion boundaries, accepting a row on unchanged text only with an explicit changed-range dependency; no one-row or 200-line discovery cap remains. Oversize packets warn, while incomplete coverage is recorded as `cannot-verify` and escalates rather than silently omitting allegations. | Accept A-R2 and B-R2. |
| C-017 reviser edits outside listed rows | Both `answer` and `begin` refuse admission of non-whitespace edits outside precise spans claimed for listed blocking rows, and preserve raw old/new hunks for inspection. Refusals identify unclaimed hunks and offer preimage-checked restoration under existing reviser authorization; structurally meaningful whitespace is not exempt, and recovery is allowed to stop safely on a race. | Accept A-R2/B-R2's hard gate and recovery; qualify authorization, whitespace and the no-stall claim. |
| C-021 verifier answer per row | Require exactly one `resolved`, `open`, `regressed` or `cannot-verify` answer per planned row with snapshot-bound evidence and touched-sentence assessment; deletion evidence cites the old span and new boundary, not a nonexistent new quote. A broken replacement requires a separately graded child allegation, and a disputed claim requires an explicit evidence-bearing ruling rather than an automatic waiver. | Accept A-R2 and B-R2, adding the deletion evidence case from C. |
| C-022 re-checking verified rows | Reset a verified row to `fixed` when raw mapped claim text is retouched, refuse direct regression of untouched rows, and defer a supporting-passage dependency system in version 1. Keep B-R2's lexical warning, allow evidenced dependent allegations as new rows, and count fresh-sweep challenges to carried verifications in delivery and measurement. | Accept B-R2's smaller version-1 policy, not A-R2's new passage-tracking requirement. |
| C-025 crash, idempotency, concurrency | Under a stable nonblocking per-ledger advisory lock, validate all inputs, publish file-synced snapshot/diff dependencies, then atomically replace the single file-synced state object containing history, sequence and operation result. Check identical operations before rejecting an old expected sequence, refuse changed payloads or stale new operations, and drop hard links/directory-sync guarantees while failing closed on missing dependencies. | Accept A-R2 and B-R2's reduced transaction, with dependency ordering and original-result storage explicit. |
| C-027 script CLI and exit codes | Use A's eight commands (`init`, `find`, `answer`, `begin`, `verify`, `sweep`, `close`, `status`) plus `revert-unclaimed` and read-only `verdict`, with JSON stdout and distinct refusal/error codes. Committed mutations exit 0 regardless of outcome; only `verdict` maps PASS/CONTINUE/ESCALATE to 0/10/11, and incomplete state never defaults to PASS. | Accept A-R2 and B-R2; no role flag, separate renderer or waiver command. |
| C-029 report writing and verdict line | Reviewer prose contains no competing row-status table or verdict; `close` identifies conflicts and asks for correction, then renders one authoritative table, next action, CONTINUE-only reviser brief and final verdict when required assessments are complete. Pin the admitted narrative and regenerate the tail idempotently after a crash, check its digest/tail on later calls and perform a final status check rather than relying only on the next review. | Accept A-R2 and B-R2, adding the crash/retry and final-check requirements. |
| C-031 reflect adoption | Defer adoption: a later adapter admits canonical rows only after synthesis, merge and the evidence gate, supports the actual multi-file/caller-owned loop, and pins its own grading policy. It must preserve reviewer diversity/evidence validation and cannot treat ledger PASS as promotion authority. | Accept A-R2 and B-R2. |
| C-032 rf-qa adoption | Defer adoption: a later adapter preserves regression before monotonicity before cap, current halt messages and synthetic-finding dedup identity, with profile-specific grades rather than spec-panel defaults. Existing guards may be selected by a profile, but a new guard requires kernel changes and its own tests; build only the spec-panel profile now. | Accept A-R2 and B-R2, explicitly preserving dedup semantics and version-1 scope. |
| C-033 implement final review adoption | Do not adopt in this experiment; any later ledger use may track repair rows but cannot replace or narrow the fresh full FINAL required for each archive attempt. Its own retry and archive gates remain separate. | Accept A-R2 and B-R2. |
| C-034 stateful session vs file ledger | The file ledger is authoritative and fresh sessions consume its packets; resumed/cached output must match the current packet digest or be refused. A stateful-session comparison is a later experiment, not an alternate source of truth in this one. | Accept A-R2 and B-R2. |
| C-040 validity checks and controls | Combine script-use/phase compliance, baseline full sweeps on the six historical finals with hidden-defect measurements, and recorded command/skill/script hashes plus live-versus-snapshot checks. Count refusals, incomplete runs, post-terminal edits and all sweep costs; neither a low hidden-defect share nor absence of row ids proves an independent sweep. | Accept A-R2 and B-R2's three-part checks, rejecting an independence guarantee from the metrics. |
| C-043 cap enforcement mechanics | Pin `CAP_REVIEWS = 3` to the canonical cap text and refuse a fourth review, third fix, second sweep or repeated FIND/init on an existing run even under a new operation id. No committed review-3 decision authorizes CONTINUE; identical retries return the old committed result rather than consume a slot. | Accept A-R2 and B-R2. |
| S-008 CLI spec form | Use one table showing command, caller, inputs, state/artifact writes, output, checks and exits, followed by one transaction/crash/rerun subsection. Include the difference between successful execution, pending work and a delivery verdict. | Accept A-R2 and B-R2. |
| S-009 test plan placement | Put named behavior tests, command pins and parity tests in one Tests subsection and list executable fixture files in the file table. Include stale packets, partial inputs, deletions, ambiguous relocation, both admission gates, checked restoration, retry races, dependency publication and report regeneration; defer the discarded durability matrix. | Accept A-R2 and B-R2's placement, reducing tests with the removed mechanisms. |
| S-012 rule classification placement | Use one end table with MECHANICAL/PROSE and residual-risk columns, not repeated inline labels. Separate schema validity, evidence presence and semantic truth instead of calling all three mechanically proven. | Accept A-R2 and B-R2. |
| X-005 unclaimed reviser edits | Enforce the C-017 admission check even when the reviser skipped its own check, and keep a preimage-checked recovery that cannot silently erase newer or authorized claimed work. A refusal is a surfaced failure or recoverable stop, not a counted clean review. | Accept A-R2 and B-R2, with authorization and loss-prevention qualifications. |
| X-006 who calls the script | Each session invokes its phase-specific subcommand; the script validates JSON evidence bound to round, snapshot and sequence, and actor identity is not claimed authenticated. The coordinator checks current next action before every dispatch, never follows a stale retry response and never launches another reviser after termination. | Accept A-R2 and B-R2; drop C's coordinator-only mutation. |
| X-011 deferred MAJOR rows in R3 count | Count unverified CRITICAL/MAJOR findings by grade, including deferred notes, unioned with new sweep findings and challenges to verified rows, and publish loop-only, blocking-only, deferred and raw/deduplicated sweep components. Use overlap only to suggest duplicates, with blinded semantic adjudication preserving distinct harms; carry early terminal bytes/counts to the R3 horizon without inventing a review. | Accept A-R2 and B-R2 on C's grade-based set, qualify B-R2's automatic overlap matching. |
| X-017 intra-B disputed status | `disputed` is a claim flag on an unresolved row, never a sixth status, and the verifier must accept or reject it with evidence about the original alleged harm. Unruled, rejected or uncertain disputes remain unresolved; a quote claiming user permission cannot clear a real blocker or change a recorded escalation. | Accept A-R2 and B-R2, with the evidence/waiver distinction explicit. |

## Positions table

All 85 points are included. Unchanged rows are copied from my Round 1 table; `(changed)` marks a changed pick or reason. Combinations select useful parts, not every original claim. Forecast picks rate the support for a planning method, not evidence of an achieved result.

| Point | Preferred | Reason |
|---|---|---|
| S-001 | A | Specific titles expose compatibility obligations instead of hiding adopter differences. |
| S-002 | B | Explicit citation aliases and unverified markers make provenance easier to audit. |
| S-003 | B | Actor, input, output, and call order are visible together. |
| S-004 | A | Kernel, contract, and adapter boundaries clarify ownership; adapter policy still needs testing. |
| S-005 | A | (changed) One atomic state object with per-row history avoids an unnecessary replay reducer. |
| S-006 | A+B | (changed) B's numbered phase table with A's named refusal codes makes the corrected transitions testable. |
| S-007 | B+C | Combine worked decisions with explicit integrity, pending, and delivery states. |
| S-008 | A+C | (changed) Use A's command table followed by C's closed-input and reduced transaction/rerun contract. |
| S-009 | A+C | (changed) Named cases and executable fixtures belong in one Tests subsection, with B's parity pins included. |
| S-010 | B | Trace-based estimates expose assumptions better than unsupported optimistic point forecasts. |
| S-011 | B | Evidence, residual causes, and self-attack prevent overstating what the ledger fixes. |
| S-012 | B | (changed) One end table with residual risks is easier to audit than scattered inline labels. |
| S-013 | A+B | (changed) One design/contract and executable fixtures suffice; defer the separate guide and duplicated schema machinery. |
| S-014 | B | An explicit unverified inventory is more honest than prematurely declaring completion. |
| S-015 | A | Moderate prose and tables are easier to scan than either dense aliases or repeated labels. |
| C-001 | A | (changed) Current rows, history, sequence and operation results commit together in one closed-schema state object. |
| C-002 | A | (changed) Derive the ordinary default from the document; explicit overrides never fall back or restart FIND. |
| C-003 | C | Snapshot admission and old/new diff ranges bind each accepted revision to its evidence. |
| C-004 | A | (changed) Sessions invoke phase-specific commands; the script validates typed evidence and remains the only state writer. |
| C-005 | B+C | (changed) B's phase table and script retouch reset combine with C's history-based open versus reopened distinction. |
| C-006 | B+C | (changed) Keep disputes as claims and require an evidence-bearing ruling; uncertainty remains unresolved. |
| C-007 | A+C | Escalate grading disputes; avoid a waiver API whose quoted authority cannot be authenticated. |
| C-008 | A+C | (changed) Freeze A's identity/grade/rule fields plus C's original issue text; keep relocation separate. |
| C-009 | A+C | Compute blocking from an explicit criterion and profile, never reviewer-supplied blocking labels. |
| C-010 | C | Incomplete evidence, uncertainty, and integrity failures cannot yield an accidental PASS. |
| C-011 | B+C | Every unresolved blocker affects delivery; keep loop and sweep counts explicit and nonoverlapping. |
| C-012 | C | Count the extra assessment honestly; session naming cannot erase its cost. |
| C-013 | C | Distinct provisional and delivery outcomes prevent publishing PASS before the sweep. |
| C-014 | B+C | Preserve spec-panel's cap; structural uncertainty escalates without importing rf-qa's monotonicity policy. |
| C-015 | B+C | Combine admission refusal for note-sponsored edits with measured minor-span touches. |
| C-016 | A+B | (changed) Both VERIFY rounds inspect complete changed packets without a row quota; C's cannot-verify protects incomplete coverage. |
| C-017 | B+C | (changed) Hard admission at both ends with preimage-checked, authorized restoration is stronger than either original alone. |
| C-018 | C | Exact context and snapshot identity disambiguate anchors without trusting line hints alone. |
| C-019 | C | Explicit relocation and deletion tombstones avoid silent nearest-match errors. |
| C-020 | C | Raw ownership and dual-sided ranges preserve deletions and whitespace-sensitive evidence. |
| C-021 | B+C | (changed) Require explicit uncertainty and snapshot evidence, plus B's graded child allegation and dispute ruling. |
| C-022 | A+B | (changed) Version 1 uses mapped retouch resets and warnings, not a new dependency system; the sweep remains a residual safeguard. |
| C-023 | C | Hunk overlap proves location, not causation; preserve independent causal adjudication. |
| C-024 | A+C | Add accidental-edit checksums to packet binding; neither mechanism authenticates deliberate editors. |
| C-025 | B+C | (changed) Keep lock, operation id, sequence and file-synced atomic state; drop hard links and directory durability guarantees. |
| C-026 | B | Its installation naming analysis supplies the clearest packaging and activation contract. |
| C-027 | A+C | (changed) A's lean command set and C's JSON/decision separation survive; only verdict supplies decision-coded exits. |
| C-028 | B | Drift tests preserve the panel while explicitly excluding unsupported unattended behavior. |
| C-029 | A+B | (changed) Preserve panel prose but generate the authoritative table/tail, with conflict checks and idempotent regeneration. |
| C-030 | A | (changed) Skip the sweep only for a no-revision review-1 PASS on identical pinned bytes, recording the exception. |
| C-031 | B+C | (changed) Defer multi-file/caller-owned adoption; merge and validate before ids, and never grant promotion authority. |
| C-032 | B+C | (changed) Defer adoption while preserving ordered guards, existing halt messages and synthetic dedup identity. |
| C-033 | B+C | Defer adoption; any later sidecar must preserve mandatory fresh independent FINALs. |
| C-034 | C | Session continuity is optional; packet identity and file state remain authoritative. |
| C-035 | A+C | (changed) Use a grade-based unresolved set including deferred MAJORs, unioned with adjudicated sweep findings and challenges. |
| C-036 | B | (changed) The traced conditional formula is useful for sensitivity, not a calibrated combined-proxy forecast. |
| C-037 | B | Byte-share arithmetic is stronger evidence than an unexplained growth forecast. |
| C-038 | B+C | Preserve fixed bars and spread rules; add baseline-sweep, leakage, and operational failure checks. |
| C-039 | none | Disclose coordinator gating and the added sweep separately from unchanged actor brief text. |
| C-040 | A+B | (changed) Combine compliance and baseline sweeps, adding C's activation hashes and live/snapshot checks. |
| C-041 | B+C | Count the sixth session and all calls; distinguish estimates from observed durations. |
| C-042 | B | (changed) Warn on large changed packets and retain allegations; arbitrary discovery thresholds must not manufacture convergence. |
| C-043 | A+C | Preserve pinned cap tests and history-derived refusal of repeated FIND, extra fixes, and sweeps. |
| X-001 | B+C | A sweep blocker prevents final PASS without authorizing another automatic fix cycle. |
| X-002 | B+C | A fresh terminal reviewer reduces anchoring; count its extra session explicitly. |
| X-003 | B+C | No evidence requires an additional spec-panel monotonicity stop; retain adopter-specific guards separately. |
| X-004 | A+B | (changed) Both rounds must retain fix-induced rows; quota removal corrects C rather than hiding the later defect. |
| X-005 | B+C | (changed) Mandatory admission plus checked recovery closes skipped-check bypasses without silently discarding newer edits. |
| X-006 | A | (changed) Sessions call their subcommands; coordinator-only calls add no authentication and are unnecessary. |
| X-007 | C | A committed escalation is operational success; consumers must inspect the explicit decision field. |
| X-008 | A | (changed) A document-derived default tolerates a lost ordinary flag; a missing explicit override still fails closed. |
| X-009 | B | Its explicit omission avoids claiming an unattended contract the variant has not established. |
| X-010 | B | Presence-only baseline checks do not justify changing unrelated installation lists. |
| X-011 | C | (changed) Historical proxy grading supports including deferred MAJORs; publish the blocking and deferred components separately. |
| X-012 | B | Trace-based pessimism is more credible than C's unexplained lowest forecast. |
| X-013 | A | (changed) No revision means unchanged FIND bytes; record a skipped sweep rather than charge an unnecessary remediation assessment. |
| X-014 | A+C | The script derives blocking from criteria instead of trusting reviewer-selected severity classes. |
| X-015 | B | Preserve original resolution plus an explicit graded child; do not accept an unexplained broken-sentence flag. |
| X-016 | A+C | Include criterion in the input and derive FR blocking mechanically. |
| X-017 | B | (changed) B's repaired claim flag and mandatory evidence-based ruling resolve the contradictory sixth status. |
| X-018 | A+B | (changed) Worker-run calls remove C's coordinator-only contradiction, but status gating and sweep changes remain disclosed treatment variables. |
| X-019 | A | (changed) Derive the default from the document, reject existing initialization, and keep random ids as metadata only. |
| X-020 | C | Snapshot-qualified relocation and old/new diff ranges avoid cross-version coordinate comparisons. |
| X-021 | B+C | Require a supported fix or explicit dispute ruling; unanswered rows cannot silently become verified. |
| A-007 | none | Measure blinded review-1 grading disagreement; frozen grades do not prevent initial inflation. |
| A-008 | none | Gate every dispatch on terminal state and detect edits from already-running revisers. |
| A-009 | C | Relocate every live anchor and escalate missing or ambiguous mappings. |
| A-010 | C | Old-side evidence and deletion boundaries allow lost obligations to remain reportable. |
| A-011 | C | (changed) Defer passage tracking, retain sweep challenges and evidenced new dependency allegations, and do not infer safety from zero recorded regressions. |
| A-012 | none | Measure changed FIND behavior; historical initial counts are priors, not treatment invariants. |
