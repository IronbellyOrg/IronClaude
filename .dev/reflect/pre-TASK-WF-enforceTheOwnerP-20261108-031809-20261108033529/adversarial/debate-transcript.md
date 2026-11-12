# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 + Round 2.5 invariant probe (Round 3 is deep-only)
- Convergence achieved: 96.8% diff-point alignment; status BLOCKED_BY_INVARIANTS (INV-001)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (Variant 1 advocate sonnet:analyzer; Variant 2 advocate haiku:qa). Advocates use each card's own reviewer class; the orchestrator and judge (opus) is a different class from both, per the reflect weak-judge rule.
- Diff points: 42 (S 8, C 14, X 4, U 16) + 5 promoted shared assumptions (A-002, A-004, A-005, A-007, A-008) Convergence denominator per the protocol formula = S + C + X + A = 8 + 14 + 4 + 5 = 31; the 16 U points are scored for merge value but are not in the denominator.

## Round 1: Advocate Statements

### Variant 1 Advocate (sonnet:analyzer)
<!-- Returned by advocate (sonnet, read-only), persisted by orchestrator on receipt 2026-11-08T03:58Z. -->

**Position**: Variant 1 classifies the deviations more accurately (Task 3 is a Necessary deviation, with no Drift or Regression) and gives the more precise mechanics for Task 1's scanner, `none`'s stale lines, and the Task 3 reply envelope. Variant 2 finds three things V1 missed that should be merged: the `created_scene()` fixture conflict, the `docs/user-guide` and HOW-WE-WORK gaps, and the missing recorded authorization. V2's "Drift" label and 2/5 grade are not supported by the code evidence.

**Steelman of Variant 2**: "Scope-adherent" is not "execution-ready". Task 3 is the only task that destroys state (a terminal close), and its acceptance cannot reject a wrong implementation. Plan :53 "Otherwise run `terminal list`" lets an unparseable or timed-out reply fall through to list-and-close; `cmd_worktree` already continues on `created.timed_out` (orca_worktree.py:611), and a timed-out create cannot show no setup/default-tab terminal exists. `created_scene()` returns `"opaque, not json"` and FO-11 asserts `warning is None` (test_issue_orca_worktree.py:376, :552-561), so Task 3's five-call acceptance (plan :57) needs an unmentioned valid-reply fixture. The plan departs from an explicit owner sentence (source.md:1) with only "stated to the owner" (plan :20). Real Task 4 gaps: `docs/user-guide/commands.md:367`, `:379` and `HOW-WE-WORK.md:329`. Its Task 2 executable-test remedy beats V1's documentation remedy.

**Key strengths claimed**:
1. Evidence-based deviation classification: `finish()` fails on copy error (orca_worktree.py:521-524), git-common-dir check at :507-513; `cmd_launch` refuses a stale in-worktree prompt (:934-936); the prompt reads `.dev/issues/<N>/launch-prompt.md` inside the worktree (:950). An agent started by `create --agent` runs before these checks. `publish_pending(word)` (:728) takes no worktree, so the pending record does not force the order (U-016).
2. Full source-item coverage table (section 2) tracing scope items (1)-(3), out-of-scope and respect lists; plan additions separated as Authorized expansion.
3. Task 1 scanner mechanics: block-bare-python.sh:97, :106, :132-134; concrete misses `orca … ; orca worktree create --agent x`, heredoc into a shell, `orca` after a pipe.
4. Task 3 reply shape: envelope with `result.setup`/`result.defaultTabs`; current code never parses `created.out`; setup branch creates no plain seed; `terminal close --tab`; `agentIdentity` absent or empty (R1-4, R1-5).
5. Stale `none` lines V2 missed: SKILL.md:17, :170; claim.md:93; claim.md:136 needs a no-worktree branch.
6. Residual risks V2 omitted: R1-8 `W-LAUNCH-FAILED` (orca_worktree.py:956-975); R1-10 WC-13 tension; R1-9 docstring :20-30; R1-12 hook only after `superclaude update`.

**Weaknesses identified in Variant 2**:
1. Inconsistent authority standard (A-003): accepts plan :19 for `none`, rejects plan :20 for Task 3; neither has an artifact. Source.md:1's explicit wording justifies a stronger recording requirement, not a different class.
2. "Drift" has no basis in outcome: V2 concedes copy-before-launch explains the design and never shows agent-on-create feasible; the departure is directed and documented.
3. R2-6 severity overstated: the new row comes from `list_rows(main)` with `--repo` (orca_worktree.py:281-288), must be absent from `ids_before` and match `^issue-<N>(-|$)` (:618-623); a cross-repo path needs an Orca list anomaly.
4. Grade 2/5 vs its own tally (5 adherent, 1 expansion, 0 regression) is mismatched; 0.91 confidence with repo-only evidence and unverified Orca behaviour is miscalibrated.
5. No timing analysis (R1-3).
6. F2 ruling rests on policy alone; claim.md:17 still stops `none` with `E-ORCA-REQUIRED` though `none` calls no Orca afterwards; that is a decision, not a non-defect.

**Concessions**:
- R1-4 under-rated: the `created.timed_out` path (:611) proceeds into the new-row branch, so an unreadable/timed-out reply is a real HIGH risk for a destructive close.
- Missed the `created_scene()`/FO-11 conflict (U-004), the user-guide and HOW-WE-WORK lines (U-002: commands.md:367, :379; HOW-WE-WORK.md:329), and the per-task acceptance review (U-003).
- Should have raised the missing owner-approval artifact as a finding (C-004 omission).
- SKILL.md :89 and :92 are already conditioned on `none` (flagged as leads).
- R1-11 attributes to Constraints :19 an enforcement claim the plan text does not make.
- R1-13's documentation remedy is weaker than V2's executable test.

**Positions on contradictions and high points**:
- X-001: V1 right on class (Necessary deviation, code ordering); V2 right that explicit owner authorization must be recorded. Final: Necessary deviation + authorization-record action.
- X-002: Split. V2 right on HIGH for the unreadable/timed-out reply; V1 right that R2-6's cross-repo case is bounded by the repo-scoped list.
- X-003: V1 (HIGH), narrowly: the hook is the only deterministic enforcement and a scanner carrying `--agent` across commands passes all 12 listed cases; plan :31 already says "that command's words", so the defect is acceptance coverage.
- X-004: Neither; use the union minus verified-not-stale lines.
- C-004: V1 on class, V2 on remedy; merge.
- C-005: V2 on severity HIGH and fixture conflict; V1 on envelope and setup details; merge.
- U-001: Ordering fact correct, severity MEDIUM. Put the close inside `finish()` after the common-dir check (:507-513) and before the copy (:521).
- U-002: V2 right; add commands.md :367, :379 and HOW-WE-WORK.md:329 + plugin mirror to Tasks 4/5.

**Shared assumptions**:
- A-002: QUALIFY. Right layer for agent Bash calls, but the block message teaches the satisfying form, so an own-use create passes with a throwaway `--prompt`; only the `--agent` half is enforced; hook ordering needs an executable test.
- A-004: ACCEPT with note. "Agrees F…" markers show anchoring on T1; V1 findings R1-1..R1-4 rest on cited code, not T1.
- A-005: QUALIFY. Closing the plain tab is the only design that keeps copy-before-agent under the existing fail-closed design; alternatives (absolute-path prompt reading the main checkout) are untested; owner should confirm.
- A-007: QUALIFY. Anchors approximate; `:614-640` vs block ending :646; executors should re-read the symbols.
- A-008: REJECT as stated. Warning alone is adequate only for a leftover tab; for timed-out/unreadable replies the control must be "do not close" plus warning; no plan item checks that a consumer acts on `worktree_warning`.

### Variant 2 Advocate (haiku:qa)
<!-- Returned by advocate (haiku, read-only), persisted by orchestrator on receipt 2026-11-08T03:59Z. Path labels: P = plan, S = source.md, W = orca_worktree.py, K = sc-issue-protocol SKILL.md, U = docs/user-guide/commands.md. -->

**Position**: Variant 2 gives the stronger execution-readiness assessment: the plan can satisfy its listed checks while omitting ownership requirements or closing a terminal without adequate validation. Return the plan for revision; keep V1's ordering analysis, but do not treat the current implementation order as proof that departing from the source is necessary.

**Steelman of Variant 1**: Agent startup must not outrun preparation and validation. The existing implementation rejects repository mismatches and copy failures before completing worktree preparation, so replacing bare creation with agent-on-create is not a simple flag substitution. V1 also genuinely improves the review with its source-requirement coverage table, the launch-failure scenario, and the distinction between enforced command syntax and instruction-only ownership policy.

**Key strengths claimed**:
1. Destructive-operation guard gap: new-row filters establish a new id, matching basename and existing directory, not repository identity (W:618-634); repository validation is inside `finish()` (W:507-513); Task 3's pre-copy close must follow it (P:53). A wrong-repository fixture must assert zero close calls.
2. Distinguishes unknown from known-safe state: Task 3 skips cleanup when setup/default tabs are reported, then "Otherwise run" listing (P:53); malformed, missing or timed-out replies are not excluded and the code continues after a timed-out create (W:611-614). Unknown state must mean no close.
3. Tests the ownership requirement, not nearby words: Tasks 6-7 assertions pin agent wording and no-own-use wording, not ownership or both roles (P:88-103).
4. Public-contract coverage: the user guide promises every value creates a worktree and tells `none` users to run steps there (U:367, 379, 394); Tasks 4-5 omit it (P:64-80). Requires explicit null values for the four worktree fields (K:121-136).

**Weaknesses identified in Variant 1**:
1. "Necessary deviation" asserted too strongly: S:1 explicitly requests agent-on-create and D2/FO-18 changes; P:20, :75 keep bare creation. Copy-failure handling (W:521-524) proves an ordering constraint, not that every source-compliant design is infeasible.
2. Cleanup assessment lacks the repository-guard finding; create targets the right repo (W:599-600), which reduces likelihood but does not validate the returned target before a destructive operation; the existing guard (W:507-513) shows identity is something the code already verifies.
3. Acceptance analysis misses policy omissions that still pass (P:88-103).
4. `none` coverage incomplete: public promises stay contradicted (P:64-80; U:367, 379, 394).

**Concessions**:
- 0.91 confidence overstates certainty about installed Orca behaviour, live hook ordering and owner authorization.
- V1 is right that launch failure after cleanup needs an explicit recovery decision; V2 did not cover it.
- V2 should adopt HIGH for the scanner gap: P:34 has no cross-command flag-isolation test though S:1 requires deterministic enforcement.
- V2's `none` range imprecise: K:90-91 needs conditional wording; K:92 already conditions launch on `none`.
- Accepting the `none` decision while challenging Task 3 needs explanation: P:19 records an owner decision; P:20 says only "stated to the owner" and contradicts S:1. Neither independently proves the conversation.

**Positions on contradictions and high points**:
- X-001: V2. Drift pending demonstrated necessity or explicit authorization; preserving existing ordering does not establish necessity.
- X-002: V2 with qualification. HIGH for closure under unknown state or before identity validation; zero terminals alone is a non-destructive leftover-tab problem.
- X-003: V1. HIGH fits a scanner gap that defeats the deterministic guard while passing the listed cases.
- X-004: Neither; separate stale Wave 6/7 and summary text from already-conditional launch text.
- C-004: V2. Notification is not approval; implementation constraints are not proof the source's approach cannot work.
- C-005: V2. Validated reply types and explicit unknown-state exclusions before cleanup.
- U-001: V2. Identity must be established before closing; targeting the right repo at create is mitigation, not validation.
- U-002: V2. Public docs belong in scope; completeness defect, HIGH runtime severity not established.

**Shared assumptions**:
- A-002: QUALIFY. Requested command-form enforcement point, not proven enforcement of ownership; installation, session coverage and rewrite ordering need evidence; adding `--agent` does not prove the creator owns the agent.
- A-004: REJECT. Agreement after seeing T1 is not independent corroboration; keep findings on their cited evidence.
- A-005: REJECT. Neither card establishes first-tab cleanup as the only alternative.
- A-007: QUALIFY. Anchors are navigation aids; re-read definitions and tests before changing them.
- A-008: QUALIFY. Warn-without-close is the safe response to uncertain state, not automatically a policy success; verify warnings reach the operator or unattended caller.

## Round 2: Rebuttals

### Variant 1 Rebuttal
<!-- Returned by advocate (sonnet, read-only), persisted by orchestrator on receipt 2026-11-08T04:01Z. -->

**Response to criticisms**:
1. V2 weakness 1 ("Necessary deviation" too strong; ordering constraint ≠ infeasibility; X-001, A-005). **Partly.** Concede "only way to meet the intent" overreaches: `publish_pending(word)` takes no worktree (orca_worktree.py:728), so the nonce could precede the create; `cmd_launch` builds the relative prompt `Read .dev/issues/{number}/launch-prompt.md and follow it.` (:950), so an absolute-path prompt reading the main checkout is conceivable, untested. Hold: the class does not depend on infeasibility. sc-reflect-protocol SKILL.md §10.2 (:996-1010) defines Necessary as forced by a technical constraint, documented inline with rationale, *not* pre-authorized; Drift (§10.3, :1012-1024) is a silent change with no inline rationale. Plan :20 opens "Deviation from the source" with a reason, so it is not silent. The constraint is real: `finish()` fails the claim at :509-513 (common dir) and :522-524 (copy) after create returns; agent-on-create would leave a live agent on a missing/stale prompt (`stale_prompt` :878-905). V2's "restore agent-on-create" gives up "failed copy = no agent" unless it adds an agent-kill step, which it never says.
2. V2 weakness 2 (no repository-identity guard before the close; U-001). **Partly.** Concede placement: plan :53 puts the close "before the copy" in `cmd_worktree`; the common-dir check in `finish()` (:507-513) runs after any such point (new-row branch :635-645). Hold MEDIUM: row from `list_rows(main)` with `--repo path:{main}` (:281-289), absent from `ids_before`, matches `^issue-<N>(-|$)`, exists on disk (:618-634), plus plan :53's exactly-one-agentless-terminal limit. Adopt V2's remedy and test (close after :513 or call `git_common_dir` first; foreign-repo row → failed/stale, zero close calls).
3. V2 weakness 3 (ownership assertions in Tasks 6-7; C-008/R2-9). **Concede.** Merge V2's ownership assertions with V1's CLAUDE.md:305, :333-337.
4. V2 weakness 4 (public docs; U-002). **Concede.** Re-read docs/user-guide/commands.md:367 and :379: both stale, absent from Tasks 4-5. HOW-WE-WORK.md:329 grep hit truncated; relying on the diff analysis wording.
5. V2's X-001 position (Drift until necessity/authorization shown). **Rejected on class, accepted on remedy.** Under §10.2 missing approval is a documentation note; authorize-or-revert is Drift's remedy, borrowed by V2.
6. V2's C-004 ("notification is not approval"). **Holds on facts; remedy accepted.** Plan :19 "Owner decisions recorded" vs :20 "stated to the owner" is a real wording difference. Merged remedy: record the owner's confirmation in the plan before Tasks 3 and 5 execute.
7. A-003 asymmetry (V1's Round 1 weakness 1 against V2). **Partly withdrawn.** :19 refines points where the source is silent; :20 contradicts a source.md:1 sentence, so a higher recording bar is defensible. Kept: that bar changes the remedy, not the class.
8. V2 on U-001, U-002: covered in 2 and 4.

**Updated assessment of Variant 2**: Accept R2-5 HIGH + fixture conflict (test_issue_orca_worktree.py:376, :552-561; plan :57 needs a valid-reply fixture); R2-3 executable test; R2-2 full-message and fail-open tests; R2-7 four null fields with ten keys kept; R2-8; R2-9; the destructive-operation framing for unknown replies. Reject: the "Drift" label and "Necessary deviation: none demonstrated"; R2-6 at HIGH; "restore agent-on-create" as a co-equal default remedy; 2/5 grade vs its own tally; 0.91 confidence (V2 conceded).

**New evidence**:
1. The count/agent guard cannot separate a setup terminal from the plain seed: plan :53 closes on exactly one agentless terminal; if the setup branch creates no seed, one agentless setup terminal also matches. The reply's `setup`/`defaultTabs` are the only discriminator; troubleshoot REPORT.md:99 relies on exactly that ("no setup script and no default tabs"). orca_worktree.py:611 continues on `created.timed_out` and nothing parses `created.out`, so an unknown reply must mean no close. Reason V1 moves to V2 on C-005 severity.
2. The source's cited evidence says "keep no `--agent` on create": troubleshoot REPORT.md:25 lists it under "Restrictions honored"; :75 says argv is pinned and changes go through a separate issue; :104 files the `/sc:issue` bare create as backlog. source.md:1 points to that report and asks for the opposite; the source is internally tense. Risk to V1's class: §10.2 says Necessary must not contradict an acceptance criterion and §10.4 treats contradicting an explicit constraint as Regression; source.md has no acceptance-criteria section and scope item (2) is an instruction, not a constraint, but a strict judge could dispute it.
3. X-004: V2 alone catches SKILL.md:90 ("continue with Wave 7 and Wave 8", unconditional); V1 alone SKILL.md:17, :170, claim.md:93, :136. SKILL.md:148 is the Wave 0 `E-ORCA-REQUIRED` row; claim.md:17 calls the Orca check "the only Orca call before Wave 7".
4. C-011: design doc :42 (P4) says `none` "still creates the worktree"; once `none` makes no Orca call, a Wave 0 STOP is a policy choice the plan must write down, not a code defect.

**Final per-point stance**: X-001 V1 on class (Necessary, §10.2), V2 on remedy (record owner confirmation, name alternatives per A-005), provisional until confirmed. X-002 split: V2 HIGH for unknown/timed-out reply; V1 MEDIUM for R2-6 with the close after :513. X-003 V1 (V2 conceded). X-004 neither (union minus SKILL.md:89, :92). C-004 merged. C-005 V2 on severity/fixture, V1 on envelope/timeout path. C-011 mostly V2 (no code change; plan records decision). U-001 V2 on fact/remedy, V1 on MEDIUM. U-002 V2. A-002 agreed QUALIFY. A-004 V2. A-005 V2 (unverified; does not change X-001 class). A-007 agreed. A-008 merged (warn-without-close + check a consumer acts on `worktree_warning`).

### Variant 2 Rebuttal
<!-- Returned by advocate (haiku, read-only), persisted by orchestrator on receipt 2026-11-08T04:03Z. -->

**Response to criticisms**:
1. "A disclosed departure cannot be Drift." Verified §10.3: Drift requires a silent change without recorded justification; the plan identifies and explains its departure. Withdraw the Drift label and "Drift pending authorization". **Concede.**
2. "Therefore it is Necessary." Does not follow automatically: §10.2 requires a divergence *forced* by a technical constraint, not merely explained by one; §10.4 includes contradicting an explicit spec constraint, and §10.5 says rationale does not authorize contradiction. The source expressly limits `agent launch` to existing worktrees; keeping it for new worktrees is a prospective source-constraint violation (a Regression signal, not an observed regression). If the source's authority is ambiguous, §10.6 supports a Grounding Gap rather than automatic Necessary. **Holds.**
3. Inconsistent authorization standards. Both owner claims unverified, but "owner decisions recorded" and "deviation … stated to the owner" assert different things; only the latter opposes scope item (2). V1 now accepts recording confirmation before execution, resolving the practical disagreement. **Partly.**
4. R2-6 HIGH vs MEDIUM. Repo-scoped listing, new-id/name filters, directory existence and the one-agentless-terminal limit materially reduce likelihood; lower R2-6 to MEDIUM. Guard still needed (identity before any close; foreign-repo fixture asserting zero close calls). R2-5 stays HIGH: an unknown reply can admit a setup terminal into cleanup without any cross-repo anomaly. **Concede.**
5. "Restoring agent-on-create loses 'failed copy = no agent'." Correct for a direct flag substitution; the original remedy omitted that property. An absolute-path prompt would not preserve it, nor would stopping the agent afterwards. Any source-compliant redesign must establish safe preparation before startup or get approval to change that guarantee. **Concede.**
6. 2/5 grade vs tally. Coverage and readiness differ, but the grade lacked an explicit basis; revise to **3/5**, keep "revise before execution". **Partly.**
7. 0.91 overstated. Updated confidence **0.75**. **Concede.**
8. No timing analysis. Adopt V1's concern; zero terminals stays non-destructive; bounded retry may help but exhaustion must warn without closing; V1's timing figure not independently verified. **Concede.**
9. F2 rests on policy alone. P1 is documented policy, so keeping Orca mandatory is not an established code defect; once `none` performs no worktree operation, keeping the prerequisite is a decision the revised plan should state and test. **Partly.**

**Updated assessment of Variant 1**: V1 supplies essential ordering analysis, failure scenarios and better source traceability; its concessions close the acceptance-coverage disagreements. Remaining overreach: treating a documented rationale as sufficient for Necessary despite an explicit contrary source instruction. V2's original Drift label was wrong; V1's unconditional "no Regression" is also too strong for a source-relative plan audit. Merged recommendation: obtain recorded confirmation of the Task 3 replacement before execution, then strengthen cleanup guards, acceptance tests and documentation coverage.

**New evidence**:
- sc-reflect-protocol SKILL.md:998-1028 (Necessary requires technical compulsion; Drift requires absent justification; Regression includes explicit spec-constraint contradiction); :1067 (rationale does not authorize contradiction); :1071-1077 (insufficient classification evidence → Grounding Gaps).
- source.md:1 "keep `agent launch` only for an already existing worktree" is an explicit behavioural restriction; §10.4 needs no separate acceptance-criteria heading.
- plan :19-20 (recorded decisions vs notification of a contrary departure are distinct claims); :53-57 (cleanup lacks an unknown-reply exclusion while acceptance requires the cleanup call sequence).
- orca_worktree.py:507-524 (identity and copy-error rejection precede successful preparation); :611-645 (timed-out create continues through new-row selection into that validation).
- docs/designs/sc-issue-claim-pipeline-flag.md:39-45 (P1 mandates Orca; P4, P7 describe earlier behaviour; updating P4 does not decide P1).

**Final per-point stance**: X-001 V2 revised (explicit-source-constraint objection holds; Drift withdrawn; automatic Necessary rejected). X-002 agreed (HIGH unknown-reply cleanup; MEDIUM R2-6). X-003 V1 (HIGH). X-004 agreed. C-004 agreed (record owner confirmation before executing). C-005 agreed (HIGH; V2 fixture/type checks + V1 envelope). C-011 agreed (keep prerequisite unless authorized; record and test). U-001 V2 on guard/test, V1 MEDIUM. U-002 V2. A-002 agreed. A-004 agreed. A-005 V2. A-007 agreed. A-008 agreed.

## Round 2.5: Invariant Probe
Fault-finder (opus, independent, not an advocate) probed the post-Round-2 consensus across all six categories; full table in `invariant-probe.md`. 24 findings: 10 ADDRESSED, 14 UNADDRESSED (HIGH 1, MEDIUM 8, LOW 5).

- **HIGH UNADDRESSED: INV-001.** Task 3 adds the code `W-FIRST-TAB-LEFT` only to the claim.md Wave 7 table. `Outcome.as_dict` ranks notes with `min(..., key=WARNING_ORDER.index)` (orca_worktree.py:232-235) over the fixed list at :198-206, so a created worktree whose only note is the new code raises `ValueError` and prints no JSON. Orchestrator re-read :190-239 and confirmed. No consensus item adds the code to `WARNING_ORDER`.
- MEDIUM UNADDRESSED: INV-002 (list failure, AMBIGUOUS, not-listed or not-on-disk paths after a successful create end with no close, and a re-run matches as reused and launches beside the plain tab), INV-003 (copy or record failure after the close leaves no tab and no agent), INV-004 (a close inside the shared `finish()` must be gated on status `created`), INV-005 (close effectiveness and later UI re-seed unverified), INV-006 (`--agent` with `--activate` or hooks may still seed a plain terminal per REPORT.md:51), INV-007 (`bash -c`, `eval`, `ssh`, `cat <<EOF | bash` forms pass the hook), INV-010 (hook covers only hooked Claude Code Bash calls), INV-012 (unattended runs: warning nobody reads).
- LOW UNADDRESSED: INV-008, INV-009, INV-011, INV-013, INV-014.

Invariant gate: 1 HIGH UNADDRESSED → **convergence BLOCKED_BY_INVARIANTS (INV-001)**. Depth standard has no Round 3, so per the no-convergence rule the base is force-selected by score and INV-001 is carried as an unaddressed invariant into the merged output as a finding. 8 MEDIUM UNADDRESSED logged as warnings and merged as findings.

## Scoring Matrix
Winner = whose position the merged output adopts after Round 2. "Merge" = both positions combined by agreement. Confidence per the calibration rules (unanimous with strong evidence 90-100%, clear majority 70-89%, contested 50-69%; concession +10%).

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|------------|-------|--------|------------|-----------------|
| S-001 | L1 | Merge | 90% | Both skeletons valid; merged card keeps V1's sections and adds V2's per-task table. |
| S-002 | L2 | V1 | 90% | V2 conceded V1's "better source-requirement traceability" (R2 updated assessment). |
| S-003 | L2 | V2 | 90% | V1 conceded the per-task test-impact review (U-003) it lacked (R1 concessions). |
| S-004 | L2 | V1 | 75% | V1 classifies seven departures incl. plan additions; class of the main one disputed (X-001). |
| S-005 | L2 | V2 | 85% | V2 rules on F2/F8/F9; V1 R2 accepted the F2 ruling as "mostly V2". |
| S-006 | L2 | V1 | 85% | V1's Orca-side citations; V2 conceded its 0.91 overstated certainty about Orca. |
| S-007 | L2 | V2 | 90% | Both now agree: revise before execution; record owner confirmation first. |
| S-008 | L1 | Merge | 90% | Severities harmonised in X-002/X-003. |
| C-001 | L3 | V1 | 95% | HIGH; V2 conceded (R1 concessions, R2 X-003). |
| C-002 | L3 | Merge | 95% | Disjoint halves: V1 matching rule + V2 fail-open/message tests. |
| C-003 | L3 | V2 | 95% | V1 conceded the executable-test remedy (R1 concessions). |
| C-004 | L2 | Merge | 90% | Agreed remedy: record owner confirmation before Tasks 3 and 5. Class split into X-001. |
| C-005 | L3 | V2 | 95% | HIGH; V1 conceded and added the setup-terminal discriminator (R2 new evidence 1). |
| C-006 | L3 | V1 | 90% | V2 conceded timing; zero count stays non-destructive. |
| C-007 | L2 | Merge | 95% | Union of lines minus SKILL.md:89, :92. |
| C-008 | L2 | Merge | 95% | V2 ownership assertions + V1 CLAUDE.md:305, :333-337 (V1 conceded). |
| C-009 | L2 | Merge | 85% | V1 "not covered" note + V2 verify-sync caveat. |
| C-010 | L2 | Merge | 85% | V2 revised to 3/5; both at 3/5. |
| C-011 | L2 | V2 | 85% | Keep Orca prerequisite (P1); plan records the decision (V1: "mostly V2"). |
| C-012 | L2 | V2 | 70% | Range 105-134 holds the fields; prose :136 outside (diff analysis); uncontested. |
| C-013 | L2 | V2 | 80% | F8 confirmed; uncontested by V1. |
| C-014 | L2 | Merge | 95% | Both: Authorized expansion. |
| X-001 | L3 | **Unresolved** | 50% | V1: Necessary deviation (§10.2, inline rationale). V2: explicit source restriction "keep `agent launch` only for an already existing worktree" (source.md:1) makes it a prospective Regression signal under §10.4/§10.5, or a Grounding Gap if authority is ambiguous (§10.6). Both withdrew Drift and agree on recording owner confirmation. Class turns on a fact neither can verify: whether the owner approved. |
| X-002 | L3 | Merge | 90% | HIGH for unknown-reply close; MEDIUM for the repository-identity ordering (V2 conceded). |
| X-003 | L3 | V1 | 95% | HIGH; V2 conceded. |
| X-004 | L1 | Merge | 90% | Union minus verified-not-stale lines. |
| A-002 | L3 | Merge | 90% | QUALIFY: hook enforces the `--agent` flag only, not ownership; ordering needs an executable test. |
| A-004 | L2 | V2 | 85% | Agreement with a seen T1 card is anchored; keep findings on their own evidence (V1 R2 accepted). |
| A-005 | L3 | V2 | 85% | First-tab close not shown to be the only alternative (V1 R2 accepted). |
| A-007 | L1 | Merge | 95% | Anchors approximate; re-read symbols before editing. |
| A-008 | L3 | Merge | 90% | Uncertain state → no close + warning; check that a consumer acts on `worktree_warning`. |

Unique contributions (scored for merge value, outside the convergence denominator): all 16 U points are incorporated (U-001 at MEDIUM per X-002; U-009 and U-010 as Orca-side leads, unverified).

## Convergence Assessment
- Points resolved: 30 of 31 (S 8, C 14, X 4, A 5)
- Alignment: 96.8% (30 / 31)
- Threshold: 80%
- Taxonomy coverage: L1 4 points, L2 16, L3 11, all levels covered (no forced round)
- Invariant gate: 1 HIGH UNADDRESSED (INV-001)
- Status: **BLOCKED_BY_INVARIANTS**. Diff-point agreement and taxonomy coverage pass; INV-001 blocks a CONVERGED declaration. Depth standard has no Round 3, so per the no-convergence rule the base is force-selected by score, INV-001 is carried into the merged output as a HIGH finding, and the return contract lists it under `unaddressed_invariants`.
- Unresolved points: X-001 (deviation class of the Task 3/5 approach; depends on unverified owner approval)
