# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (plus Round 2.5 invariant probe, see invariant-probe.md)
- Convergence achieved: 92% (60 of 65 diff points agreed); status BLOCKED_BY_INVARIANTS (8 HIGH UNADDRESSED invariants); depth standard, so no Round 3 and the base is force-selected by score
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3 (A opus:architect, B sonnet:analyzer, C haiku:devops)

## Round 1: Advocate Statements

### Variant A Advocate (opus:architect)

**Position**

Variant A is the right base for the merge. It is the smallest design that still has a clear owner for every decision (reviewer, script and grader each own one thing, A 2.1). Its install and naming facts check out against the code, and it adds a test that fails when the copied command drifts from `spec-panel.md`. A is wrong on where state is written (X-001). It should take B's report-embedded ledger, B's hunk coverage and C's fail-closed missing-skill rule, and keep its own lifecycle, ownership split and install contract.

**Steelman of Variant B**

- B is the only variant that keeps to the S1 write rule. I checked the saved runs: the flg-r2 review reports say "the brief allows writing only this file" (`exp346-ab-flg-r2/.dev/experiments/346-validation/phase4/flg-r2/reviews/spec-panel-round3.md:176`, `spec-panel-round2.md:227`), and the reviser disposition says "the brief allows writing only the spec and this file" (`disposition-round2.md:61`). B's choice to put the scratch files in `/tmp` and embed the sealed ledger in the report (B 2.0, 2.3 S9) is the one design that fits under the one-line brief substitution without breaking the comparison.
- With the ledger, sentinel and verdict all inside one report, the verdict can be recomputed from the report alone (B S10 `check`). The design gets cross-round state without any extra repository file.
- Hunk coverage (B 2.4: "an uncovered hunk ... is also FAIL, so silence never passes") is the only guard against a PASS that comes from reviewer silence, a failure mode that A and C both leave open (X-015).
- Canaries (U-011), the offline replay of real R3 claims (B 5.1, U-014) and the M1c probe review (U-015) ground B's predictions in counted data. They also give an outcome measure that the mechanism itself does not define. This is the strongest measurement design of the three.

**Steelman of Variant C**

- C treats infrastructure failure as its own state, ERROR or HOLD, outside PASS/FAIL (U-021, C section 6 table). A broken grader can therefore never show up as a verdict. Architecturally this is the cleanest failure semantics of the three.
- A prior-id link is valid only with an identical outcome hash and either an identical quote hash or a changed anchor (C 2.4 step 2, U-027). That mechanically closes the "cite an unrelated prior id" bypass, which A only lists as risk 3.
- The fix-to-id disposition map (C 2.5, U-024) is the only mechanical check that a reviser applied only blocking ids.
- The stratified audit also samples confirmed blockers (C section 5, U-026), so grader accuracy is measured in both directions, not only on demotions.
- A missing skill fails closed (`E-SKILL-MISSING`, C section 3), so a non-stoprule run can never be counted under the variant's name.

**Key strengths claimed**

1. **One owner per decision.** The 3-role table (A 2.1) states what each role "Never writes": the reviewer never writes severity outcome, origin, verdict or Reviser brief, and the script never writes finding text. The reviewer-writes / parent-derives split copies `qa.md:141` (A 2.4), so it reuses an established repository pattern instead of inventing one.
2. **Smallest working surface.** 9 subcommands over pure functions (A 3.4), about 17 script calls and 2-3 agent calls per loop (A 6.2). B needs 27-33 Bash calls and 6-12 agent calls (B 6.1). C needs up to 11 agent calls, plus locks, deadlines and SLOs (C section 6). For an n=2 screen, maintenance and run cost scale with surface, and A's is the smallest that still computes the verdict and enforces the cap.
3. **Drift guard on the copied command.** `test_spec_panel_stoprule.py` pins a computed diff against `spec-panel.md` outside the 5 replaced blocks (A 3.6, U-006). A later spec-panel edit then fails a test instead of drifting silently. B and C copy the file with no such guard, and A's risk 9 names drift as the main maintenance cost.
4. **Install facts verified.** The `-protocol` suffix keeps the skill installed standalone. `_has_corresponding_command` strips only `sc-` (`install_skills.py:13-21, 52-59`), new skills skip-existing without `--force` (`install_skills.py:102-104`), and agents behave the same way (`install_agents.py:51`). So A's claim that "a plain install adds the three new primitives" (A section 4) holds for all three, and A 3.6 pins `_has_corresponding_command("sc-spec-panel-stoprule-protocol") is False` as a test.
5. **The previous review's verdict is checked mechanically.** `verify-prior` recomputes review N-1's verdict and stops on a hand-written line (exit 5, U-002). The prior-status guard forces a fake `resolved` back to `open` (U-003). Neither B nor C checks the previous verdict before the next review starts.
6. **Carried blockers are frozen** (A S4: "their status is frozen, so a grade cannot oscillate between rounds"). This closes a downward-drift path that C opens (X-003).
7. **The conflict is removed at its source.** FR-8/FR-9 text is edited (A 3.1 item 4), not left contradicting bullet 2 (B 3.1). FR-10's synthesis gate is not touched (C removes it). Bullets 1, 4 and 7 are kept byte for byte, so `CANONICAL_CAP_TEXT` and `AT_CAP_CLAUSES` keep matching (A 3.1 item 5, `test_review_severity_rule.py:215-219`).
8. **The grader is a declared, installed primitive.** `stoprule-grader` pins `model: sonnet`, `tools: Read`, `permissionMode: plan` and `maxTurns: 10` (A 3.5). Its independence settings are in reviewable frontmatter, not re-stated in every dispatch (C has no agent file, S-004).
9. **Extension scaffolding is limited to what reuse needs.** One extension point, `--severity-map` (A section 8, U-005). Fit is stated per consumer, with "Do not reuse the stop rule" for `/sc:implement` because of `qa.md:167`. The promotion and retirement path is explicit (A section 8, U-008).
10. **Honest metric.** A keeps the reviewer-label proxy beside the confirmed count, and falsifier 4 ("problem moved, not solved") tests whether the gain is only definitional (A section 5, risk 11). This answers A-011 directly.

**Weaknesses identified in Variant B**

1. **The cap override contradicts B's own script.** Option (g), "authorize one extra cycle limited to the ids in (b)" (B 2.5), has no mechanism, because `begin` exits 4 on a prior review-3 FAIL (B S0). A user who picks (g) gets a refusal (X-012).
2. **The missing-skill fallback contaminates the measurement.** "run the 427 loop unchanged with `stoprule: missing`" (B 3.1) yields a 427 run under the variant's name. With n=2, one such run is half the arm.
3. **The command contradicts itself.** FR-8/FR-9 "MAJOR severity minimum" stays in the file (`spec-panel.md:328-329`), while bullet 2 says a GAP row is "not an automatic MAJOR" (B 3.1). The reviewer reads both. A edits the source text instead.
4. **"No label" only renames the reviewer gate.** The reviewer still appends "one `claim` per candidate blocker" (B S1), so choosing what to claim is the same gate A's `claimed` field makes explicit. Dropping labels also costs the independent proxy: B admits M1b "is no longer independent" (B 5.3) and needs an extra probe session (M1c) to recover a comparison.
5. **B is inconsistent about judged anchors.** B rejects a judged anchor as "the thing already measured to be weak" (B open Q1), yet adds grader Q2=same as a demotion path to `late-found` (B S5). That is a second semantic gate on lateness, which B itself argues against.
6. **The audit is not independent of the grader.** The auditor is `finding-grader` in `audit` mode (B 3.3): the same agent body and framing, with only the model changed. A and C use a fresh auditor with the full spec.
7. **Largest per-review overhead.** 10 subcommands, about 380 script lines, 9-11 Bash calls and 2-4 agent calls per review, 18-30 min and 90-120k tokens per loop (B 6.1). B's own falsifier F7 (> 25 min per review) sits close to its own estimate.
8. **The reuse advice is incoherent.** For `/sc:implement`, B reuses "the ratchet idea" while keeping late blockers blocking (B section 8). A ratchet that never demotes is not a ratchet.

**Weaknesses identified in Variant C**

1. **The installer removes C's skill.** The name `sc-spec-panel-stoprule` maps to `commands/spec-panel-stoprule.md`. Unless that command has a line matching `^\s*>?\s*Skill\s+<name>\s*$` (`install_skills.py:30-32`), `_has_corresponding_command` is True and `install_all_skills` calls `rmtree` on the installed copy (`install_skills.py:88-98`). C's activation is the prose sentence "Load skill sc-spec-panel-stoprule before review work." (C section 3), which does not match. The first ordinary `superclaude install` after deployment deletes the skill, and the command then fails closed every time (S-005).
2. **C breaks the S1 write rule twice.** 13 files per round under `.spec-panel-stoprule/<run-id>/` beside the source (C 2.6), plus persisted baselines (C section 4). The saved briefs allow "writing only this file" (`spec-panel-round3.md:176`).
3. **The fix packet cannot be reached through the unchanged briefs.** 427 bullet 6 says "the reviser reads the report, not the command" (`spec-panel.md:263`). The flg-r2 reviser cited report lines (`R2:111`, `R2:249` in `disposition-round2.md:68,71`). C's growth prediction rests on a `fix-packet.md` that the unchanged reviser brief never names (X-011, A-017).
4. **Re-grading carried blockers allows convergence by attrition.** "a valid grader-minor explicitly demotes it" (C 2.4) lets a confirmed blocker vanish at review 2 or 3 because a later grader was lenient. That is downward drift, and it produces exactly the PASS the experiment is trying to measure.
5. **Too many runs will end with no data.** Malformed envelope gives ERROR, there is "No grader/reviewer automatic retry" (C section 6), a grader timeout gives ERROR, and any audited wrong demotion gives HOLD with a human required "before any delivery is accepted" (C section 5). At 25% audit per round, HOLDs are likely, and one ERROR in an n=2 arm loses half the arm.
6. **Operations are heavier than the experiment needs.** Locks, fsync with atomic rename, a 92-min loop deadline, SLOs and 30-day retention (C 2.6, section 6) are production concerns. The proposed 15-min reviewer budget has no measured baseline and could cut normal reviews short.
7. **The grader is not a declared primitive.** There is no agent file (S-004). The model and tool restrictions are "Prefer" and "when the dispatch supports that" (C 2.4 steps 4-5), so independence depends on whoever dispatches the grader each round.
8. **Scope creep.** C overrides the FR-10 synthesis gate (C 2.1), which is a table-completeness rule unrelated to the stop rule (`spec-panel.md:330`).

**Concessions**

1. **X-001 goes to B, and A breaks the brief.** I checked: the S1 review brief allowed writing only the report (`spec-panel-round3.md:176`). A's `findings-r<N>.json`, ledgers, cards, grades and verdict files in the loop directory (A 2.2-2.3), and A's claim that "The coordinator's brief is unchanged apart from the command name" (A 2.1), cannot both hold. Fix for the merge: keep A's subcommands, but have them write to a private `/tmp` scratch directory, and have `verdict` embed the sealed ledger and sentinel in the report, as B does. Then `verify-prior` reads review N-1 from the prior report, not from `ledger-r<N-1>.json`.
2. **The missing-skill path is unstated in A (X-013).** Adopt C's fail-closed `E-SKILL-MISSING`.
3. **No silence guard in A (X-015).** "zero blocking gives PASS" (A 3.6) lets reviewer silence pass. Adopt B's hunk coverage.
4. **Base file (X-009).** B's same-base copy from the 472-line Arm B file is a cleaner comparison than A's logged covariate.
5. **Reviewer-minor is never raised (A S3).** A reviewer can hide a blocker by labelling it minor, and A's audits sample only demotions, so this path is not measured.
6. **The PASS-time audit is weak.** With k=3, a 1-in-5 error rate is missed about half the time (A risk 1). Grader accuracy on confirmed blockers is not sampled at all; C's two-sided audit is better.
7. **The JSON repair rule is left open in A (A open Q7).** Adopt B's single repair (exit 3 once).
8. **A's growth prediction is optimistic.** The flg-r2 reviser applied minor findings on its own judgement ("Minor findings were applied too when the fix corrects an existing wrong ... statement", `disposition-round2.md:12`), not only because the brief said so. A's brief id list defines "confirmed", but the reviser still reads the full report (A open Q3).
9. **A gap all three variants miss.** The Arm B review brief imposes its own verdict rule, "Under the brief, any finding of any severity is FAIL" (`spec-panel-round3.md:15,170`). Under the one-line substitution that brief text survives. Only command bullet 7 ("may not grade a minor finding as blocking") outranks it, and that is prose. The merged spec must state that the script's verdict wins.

**Shared assumptions (A-NNN: ACCEPT/REJECT/QUALIFY + reason)**

- **A-006: QUALIFY.** Auditor judgement is acceptable ground truth only under three conditions. (a) The auditor sees the full spec and no grader reason; A 2.6 and C section 5 do this, B gives it 15 lines. (b) A human labels a fixed sample independently, and auditor-human agreement is reported as its own number; A's owner spot-check of 5 should be this figure, not a sanity check. (c) A measure outside the auditor exists for cases where grader and auditor are both wrong, such as B's M1c probe review. Without (c), every audit falsifier is bounded by auditor error.
- **A-007: QUALIFY.** The failure-path rate is unestimated, and it decides which kind of result a failure becomes. Merge rule: record each grader-failure event as `grade=missing` with a count in the sentinel. A loop where the failure path fires in more than one review is reported as an invalid replicate (C's ERROR semantics), not counted as a FAIL against the R3 bar. A single failure stays fail-safe toward FAIL (A S5).
- **A-008: QUALIFY.** A seed derived from reviewer-written content (A: findings hash, B: sealed-ledger hash) can be steered in principle. For card order this is harmless. For audit selection it matters. A's PASS-time seed is the final ledger hash, which includes grader output the reviewer cannot predict, so steering is weak but not zero. Merge rule: `init` writes a random nonce to the report sentinel before review 1, and every sample seed is `sha256(nonce || review || ledger)`.
- **A-016 (contradicted, X-001):** settled in B's favour by the saved briefs. The reviewer may write only the report, plus private `/tmp` scratch, which B marks UNVERIFIED; ctl-r1 R3 used a `/tmp/ironclaude-batch.*` dir, as B 2.0 cites.
- **A-017 (contradicted, X-011):** settled against C. The reviser reads the report (`spec-panel.md:263`, `disposition-round2.md:68,71`), so the blocking-only list must live inside the report.

**Contradiction positions (X-NNN: winner A/B/C + one-line reason)**

- **X-001: B.** The saved S1 briefs allow writing only the report (`spec-panel-round3.md:176`); A and C break that.
- **X-002: A.** For an n=2 screen, a fail-safe FAIL keeps every replicate scored and biases against the treatment. C's ERROR can drop half an arm. Adopt C's label only for repeated failure (see A-007).
- **X-003: A.** Freezing carried blockers prevents downgrade by a later lenient grader. C's re-grade lets confirmed blockers vanish.
- **X-004: A.** A grade on a late-found claim cannot change the verdict. A's offline audit already reviews every late-found claim, so C spends grader calls for no change in outcome.
- **X-005: A.** Edit FR-8/FR-9 at the source and leave FR-10, an unrelated completeness gate. B leaves contradictory text and C widens scope.
- **X-006: A.** B's claim-selection is the same reviewer gate without a label. A keeps the label needed for the A-011 proxy comparison.
- **X-007: A.** An audit at PASS that finds a real blocker should recompute FAIL automatically. C's HOLD needs a human in every such run.
- **X-008: A.** Verified: `install_skills.py:102-104` and `install_agents.py:51` skip existing items, and the `-protocol` name installs standalone.
- **X-009: B.** The same 472-line base as Arm B removes a covariate that A only logs.
- **X-010: A.** A and B agree, and the Arm B briefs already pass `--baseline`. C's self-persisted baselines need repository writes the brief forbids.
- **X-011: A.** `spec-panel.md:263` and the flg-r2 disposition show the reviser reads the report, so a separate packet needs a brief change.
- **X-012: A.** The cap is not liftable inside a loop, and a reset is a visible new loop. B's (g) contradicts its own exit 4. C's parent-run-id lineage is worth adopting.
- **X-013: C.** Failing closed on a missing skill keeps non-treatment runs out of the arm; B's fallback contaminates it and A is silent.
- **X-014: B.** One counted repair of form fields keeps a 22-finding JSON review from ending on a typo, without an uncounted cycle.
- **X-015: B.** Hunk coverage is the only guard against a PASS produced by silence.
- **X-016: A.** A model pinned in agent frontmatter is declared and reviewable. B's class swap is dispatch prose, and S1 runs an opus reviewer anyway.
- **X-017: A.** `/sc:implement` keeps late blockers blocking (`qa.md:167`), so no stop-rule part transfers. B's "ratchet idea" without demotion is empty.


### Variant B Advocate (sonnet:analyzer)

**Position**

Variant B is the only design whose repository footprint is exactly the report file, whose verdict cannot be reached by reviewer silence, and whose predictions are derived from counted claims on the real R3 reports. It should be the base for the merge, with A's verified install facts, A's frozen-prior rule and A's FR-8/FR-9 text edit, and C's fail-closed missing-skill path, adopted into it.

**Steelman of Variant A**

The strongest case for A: it separates three roles with one owner each (A 2.1: Reviewer writes findings, `stoprule.py` computes, grader only grades), so no role can both raise and decide a blocker. It keeps the command a near-copy and puts every rule in a reusable skill (A section 8). Three of its mechanics are better than B's. First, prior blockers are frozen and never re-graded (A S4), so a confirmed blocker cannot oscillate out of the ledger. Second, `verify-prior` recomputes review N-1's verdict and stops on a hand-written line (A S1, exit 5), and the prior-status guard forces a `resolved` prior back to `open` when its quote is still present and its section is untouched (A S3). Third, a text test pins a computed diff of the variant against `spec-panel.md` (A 3.6), which turns copy drift into a red test. It edits the FR-8/FR-9 text itself (A 3.1 item 4) so the command does not contradict its own loop. It is cheaper (one grader call per review, A 6.2) and it is the only variant that read `install_skills.py` and got the install story right (A section 4, which I verified against `install_skills.py:100-104`). Its risk list is candid (A 6.3 risk 1: k=3 misses a 1-in-5 error rate about half the time).

**Steelman of Variant C**

The strongest case for C: it treats infrastructure failure as a state of its own, so ERROR and audit HOLD can never be mistaken for PASS or FAIL (C 2.5, section 6 failure table). It closes the crash-and-retry reset of the review count with a durable slot reservation (C 2.2 step 4), which A and B only partly address (A risk 8; B takes N from the prior sentinel). It is the only design that audits both sides of the grader: 25% of nonblocking dispositions and 25% of confirmed blockers, stratified, with inclusion probabilities (C section 5), so it can estimate grader precision and not only the demotion rate. It is the only design that mechanically checks the reviser: a fix-to-id disposition map where unknown ids reject the submission (C 2.5), which B only measures afterwards (B F6). Its prior-id link needs an identical outcome hash plus an identical quote hash or a changed anchor (C 2.4 step 2), closing the "cite an unrelated prior id" bypass that A lists as its risk 3. It treats quotes as inert data, labels every interface PROPOSED, and refuses to claim SLOs that n=2 cannot show (C section 6).

**Key strengths claimed**

1. **Root cause counted, not asserted.** B maps all 8 ctl-r1 R3 blockers to the round-2 fix diff: 5 sit on text the fix wrote, 3 on baseline text (B section 1 point 2). I re-read `ctl-r1/.../spec-panel-round3.md:179-189`: R3-8 says itself "Present in the round-2 input, not flagged then", and flg-r2's only R3 blocker N12 is tagged `origin=changed` (flg-r2 `spec-panel-round3.md:84`). So B's conclusion that a ratchet alone cannot reach the bar is evidenced, and A concedes the same figures (A section 5: the R3 drop "does not come from the ratchet on 427-style runs"). B alone then predicts from a replay (B 5.1: 4.3 of 8 survive on ctl-r1, 0.85 of 1 on flg-r2) and states a chance, not just a point: about 0.5 that both replicates are at or under 3 (B 5.3). A predicts 3 and 1, C predicts 2 and 3, and neither shows a count.
2. **Smallest footprint inside the S1 briefs (X-001).** The dispatched S1 briefs say "Ownership: write ONLY your output file(s) ... planning only, no edits to src/, tests/, docs/, .claude/, ~/.claude" (`exp346-s1-armA-repA/.dev/experiments/346-validation/phase3/S1-armA-repA/evidence/dispatched-task-text/T05-R1-review.txt`, also T07 and T09), and the run validity check includes a `git status --short` that must show only the expected untracked paths (`validity.md:94`, `run-log.md:33` in the same folder). B writes one repository file and keeps scratch in `/tmp` (B 2.0). Worker precedent for `/tmp` use exists: R1 revise and R2 review ran `git init` in throwaway `/tmp` repos (`validity.md:94`) and ctl-r1 R3 ran inside `/tmp/ironclaude-batch.*` (`spec-panel-round3.md:13`). B marked this UNVERIFIED; the record supports it. A writes `findings/ledger/cards/verdict-r<N>` files plus `escalation.md` into the loop dir (A 2.2, default `./.dev/spec-panel-stoprule/<stem>/`) and C writes 13 files per round under `.spec-panel-stoprule/<run-id>/` (C 2.6). Both add untracked repo paths the validity check would list as unexpected.
3. **Silence cannot pass.** B's verdict function (B 2.4) fails on any confirmed claim, any unresolved prior, any `unconfirmed` claim or any uncovered hunk; every changed hunk needs a claim or a `checked` line (B S1/S2). In A and C, "zero blocking gives PASS" (A 3.6; C section 3 "all-minor is PASS"), so a reviewer that writes nothing passes (X-015).
4. **No label to game.** B's ledger has no severity field at all (B 2.2: "there is nothing to read"). This removes the measured drift path (FR-8/FR-9 floor, disagreements resolved to MAJOR; B section 1 point 3) and the hide-a-blocker-as-minor path. A and C keep `claimed` and only grade claimed critical/major (A S3 "A finding the reviewer called minor is never raised"; C 2.4 step 6), so a reviewer can still bury a real blocker under a minor label (X-006).
5. **Calibration inside every run.** Each grader batch carries two canaries (one known-blocking, one known-minor); a wrong canary rejects the batch (B S3/S5). The audit runs on every review, not only at PASS: a FAIL candidate samples up to 3 demotions plus one unclaimed hunk, and a PASS candidate re-judges all demotions and blocks on a contested one (B S6/S7). A audits only at a computed PASS and with k=3 (A 2.6), and has no in-run calibration.
6. **Verdict reproducible from the report alone.** The sealed ledger is embedded in the report with a sentinel, `check` re-derives the verdict (exit 6 on tamper), and `finalize` refuses a hand-typed `verdict:` line (B S9/S10). A's hand-written-verdict check runs at the next review (A S1), and A admits there is no next review after a final PASS (A risk 7).
7. **Measurement that cannot be won by the mechanism alone.** B adds M1c, an unmodified 427 review of the final spec, with F1 and F3 stated against it (B 5.2, 5.4). It gives each prediction as arithmetic (B 5.3), and uses the same 472-line Arm B base file (sha256 prefix `c8d80346a96c`, matching flg-r2 `validity.md:26`) so arms differ only by the stoprule change (X-009). A and C copy today's master file (A section 4, 486 lines; C section 3 "Copy current spec-panel").
8. **Install path that works.** The `-protocol` suffix makes `_has_corresponding_command("sc-spec-panel-stoprule-protocol")` false (it strips only `sc-`, `install_skills.py:40-59`), so the skill installs. The experiment route is `cp` plus `sha256sum -c`, with a one-line `perl` brief substitution that has a `grep -c` check (B section 4).
9. **Honest accounting of what is enforced.** B 2.6 separates script-enforced rules from prose, and 6.2 lists ten ways the loop could get worse, each with a check.

**Weaknesses identified in Variant A**

1. **Breaks the "name substitution only" premise.** A 2.1 says "The coordinator's brief is unchanged apart from the command name", yet A 2.2 has the reviewer write `findings-r<N>.json` and the script write ledgers, cards, verdict files and `escalation.md` into a repo directory. The briefs say "write ONLY your output file(s)" (T05, T07, T09). The first-review default `./.dev/spec-panel-stoprule/<stem>/` adds an untracked path the validity check (`validity.md:94`) would list as unexpected.
2. **Reviewer-silence PASS and label-gated candidates.** `candidate` requires `claimed` critical or major (A S3), and there is no hunk-coverage check (A 3.6 tests "zero blocking gives PASS"). The failure the data show is label drift (A section 1 cites it), yet the gate still reads the label.
3. **Final-PASS verdict is unchecked.** A's `verify-prior` only fires when a later review starts (A S1); A risk 7: "at a final PASS there is no next review, so the recorder (or user) must run verify-prior".
4. **Thin audit.** Audit only at a computed PASS, up to 3 demotions (A 2.6); A's own risk 1 says a 1-in-5 error rate is missed about half the time. On the FAIL path no demotion is checked in-run; at the cap the user is the audit (A 2.6).
5. **Ratchet that its own data say rarely bites.** A S3 anchors on changed-line overlap. A section 5 itself says the R3 drop "does not come from the ratchet on 427-style runs". The prediction (r1=3, r2=1) comes from reasoning with no replay on the real R3 reports.
6. **Confound in the base file.** A copies the 486-line master file while the arms ran the 472-line file, and logs it only as a covariate (A section 4).
7. **JSON file fragility.** One JSON file for all findings with exit 8 on a schema error and no repair path (A open Q7); a single bad character in a 22-finding review stops the run.

**Weaknesses identified in Variant C**

1. **Install defect (S-005), verified.** C names the skill `sc-spec-panel-stoprule` and ships `commands/spec-panel-stoprule.md`. `_has_corresponding_command` strips `sc-`, finds `commands/spec-panel-stoprule.md`, and returns True unless the command has a line that fully matches `^\s*>?\s*Skill\s+<name>\s*$` (`install_skills.py:30-32, 40-59`). C's activation text is a sentence ("Load skill sc-spec-panel-stoprule before review work...", C section 3), so `install_all_skills` marks the skill served-by-command, skips it, and `rmtree`s an existing install (`install_skills.py:97`). The module docstring warns about exactly this. C states "the skill installer's current behavior is UNVERIFIED" (C section 4) for a short file. Under C's own rule ("missing skill always fails closed", C section 4) the variant would not run after a normal install.
2. **Conflicts with the S1 briefs on three points.** (a) The briefs require "a PASS or FAIL verdict" and, in T07, "a binary PASS or FAIL verdict", while C adds ERROR and HOLD as terminal states with exit codes 2 and 3 (C 2.5, section 3). (b) The reviser inputs are the report path (T06 "Inputs: ... review/spec-panel.md"; T08 "edit ONLY the spec and write ONLY disposition-round2.md"), while C adds `fix-packet.md`, `record-fix` and a required disposition map (C 2.5, section 3). That is a brief change, yet C section 4 says "no other review-brief edit". (c) 13 files per round beside the source (C 2.6) against "write ONLY your output file(s)".
3. **Prediction without derivation.** "R3 confirmed 2 and 3 (mean 2.5), growth 22% and 28%" (C section 5) comes with no counted data, no replay and no probability. C's evidence line (C section 1) lists reports it read but shows no count from any R3 report.
4. **Quote-only grader biased toward minor on cross-file claims.** C's rubric ends "Missing context is not evidence of a blocking defect; answer minor when it is insufficient" (C 2.1) and the grader sees only the quote and outcome (C 2.4 step 3). A defect like ctl-r1 R3-2 (a cited rule that the cited source does not state) needs the source line to confirm. B passes evidence entries marked `verified` or `unverified` so the grader can grade as if true (B S3); C has no such channel, so those demotions are structural.
5. **Re-grades carried blockers each round (X-003).** A grader that sees no round and no history (C 2.4 step 3) can answer minor on a blocker it confirmed last round, and the loop loses a confirmed finding to noise. A freezes priors for exactly this reason (A S4).
6. **Machinery out of proportion to n=2.** Exclusive lock, fsync plus atomic rename, slot reservation, 92-minute deadlines, quarantine rollback (C 2.2, 2.6, section 6). C admits the SLOs cannot be shown by S1 and calls the deadlines "proposed ceilings, not measured latency predictions" (C section 6). The experiment question is whether a computed verdict converges; this adds failure surface before that is measured.
7. **No coverage check and a label gate.** "All-minor is PASS" (C section 3) and `claimed_severity` gates which items reach the grader (C 2.3, 2.4). Same silence and hide-as-minor paths as A.
8. **HOLD needs a human.** "A human adjudicates disagreement before any delivery is accepted" (C section 5). The S1 loop is run by workers and a coordinator, so a HOLD has no consumer inside the run, and the loop ends with neither PASS nor FAIL.

**Concessions**

1. X-012: B's option (g) lets the user "authorize one extra cycle" while B's own `begin` exits 4 on a prior review-3 FAIL (B S0 versus 2.5 g). There is no mechanism. C's "a new user-authorized run preserves the old run id as parent" (C 2.5) is the coherent version.
2. X-013: B's fallback "run the 427 loop unchanged with `stoprule: missing`" (B 3.1) produces non-treatment data under the treatment name. A fail-closed stop is better for an experiment. (C's own install defect makes that path live for C, but the principle stands.)
3. X-008: B called skill install behaviour UNVERIFIED (B section 4). `install_skills.py:100-104` skips an existing skill without `--force` and otherwise installs, so A's plain-install claim holds for the `-protocol` name. B's manual route is safe but unnecessarily cautious.
4. X-005: B leaves "MAJOR severity minimum" in FR-8/FR-9 (`spec-panel.md:328-329`) and relies on bullet 2 to override it. A's edit of that text is cleaner.
5. X-003: B has a latent hole. `unresolved` excludes priors "asserted" by a claim line (B 2.4), and a claim that cites a prior still goes to the grader (B S3), which can answer `blocking:false`. A confirmed prior can then leave the ledger. A's freeze should be adopted.
6. B is heavy: 11 steps, 10 subcommands, about 380 lines of script, 6 to 12 agent calls and 18 to 30 added minutes per loop (B 6.1), against A's 2 to 3 agent calls and 4 to 10 minutes (A 6.2). B's own risk 1 says effort may move from finding to form. B's predicted chance of meeting the R3 bar in both replicates is only about 0.5, and of a clean PASS about 0.2 per replicate (B 5.3).
7. The span-novelty ratchet demotes real defects (R3-4 and R3-9 are real and found late, B 5.1 and open Q1), and the quote rule demotes pure omissions (B 6.2 risk 2). On a FAIL path, audit disagreement is only counted, so the verdict depends on which demotions were sampled (B open Q2).
8. B can produce a FAIL with zero confirmed claims (all `unconfirmed` or an uncovered hunk), and the Reviser brief "from confirmed ids only" is then empty. That case is undefined.
9. B says "15 of 15 findings applied, 9 minor"; `disposition-round2.md:35` totals 15 rows as 11 findings plus 4 citation rows. The point stands but the count is looser than stated (A repeats it).
10. All three leave one conflict unaddressed. The Arm A review briefs say "any finding of any severity is FAIL" (T07 and T09), while every variant computes the verdict from confirmed blockers. B's bullet 3 overrides it by implication; the merge should say so explicitly.

**Shared assumptions (A-NNN: ACCEPT/REJECT/QUALIFY + reason)**

- **A-006: QUALIFY.** Accept the auditor as the best available reference only if (a) the reported number is named "contested rate" and not "accuracy", since auditor and grader are the same vendor and errors correlate (B risk 5); (b) the owner spot-check that A has (5 items, A section 5) is added to B; and (c) M1c, the unmodified 427 probe, stays as the instrument that does not depend on the auditor. B's own replay reading in 5.1 is my judgement and carries the same circularity, which B labels.
- **A-007: QUALIFY.** The grader's availability is unmeasured in every variant. Accept for the normal path if the failure path is reported separately: B's sentinel already carries `unconfirmed=f`; add that any run with `unconfirmed>0` is its own stratum for M1, so grader outages do not inflate the R3 metric. Also run one in-worker smoke test of the Agent call before the live runs (B open Q4).
- **A-008: QUALIFY.** B's seed is `sha256(sealed ledger)[:8]` (B 3.2), reviewer-authored content, so a reviewer could in principle grind text to steer the sample, though it has no reason to. Accept for S1 if the seed also mixes in the saved grader replies (`grader-out-K.txt`), which the reviewer cannot know at seal time, and the sampled ids are printed in the sentinel.

**Contradiction positions (X-NNN: winner A/B/C + one-line reason)**

- **X-001: B.** The briefs say "write ONLY your output file(s)" and the validity check includes `git status --short` (`validity.md:94`); B's repo footprint is one file, and worker `/tmp` use has precedent in the same record.
- **X-002: B.** A binary verdict is a brief requirement (T05, T07), and B marks the cause visibly (`grader: unavailable`, `unconfirmed=f`); C's ERROR leaves a review slot consumed with no verdict (see concession 8 on the empty brief).
- **X-003: A.** A's freeze prevents a confirmed blocker from oscillating; C re-grades it and B has the hole in concession 5.
- **X-004: B.** Sending ratchet-demoted claims to the grader (C) costs calls and cannot change a verdict; A and B agree here, and B also lists them in every report and audits them.
- **X-005: A.** A edits the FR-8/FR-9 text so the command does not contradict its loop; C's removal of the FR-10 gate has no evidence behind it.
- **X-006: B.** A ledger with no severity label leaves nothing to hide a blocker behind; A and C let a reviewer's "minor" end a claim.
- **X-007: B.** A PASS the audit contests must not stand; B keeps the verdict recomputable from ledger data, while C leaves a PASS in the artifact beside a HOLD.
- **X-008: A.** `install_skills.py:100-104` confirms plain install works for the `-protocol` name; B and C stayed UNVERIFIED.
- **X-009: B.** Measuring on the 472-line Arm B base file (sha prefix `c8d80346a96c`) keeps the arms identical apart from the treatment.
- **X-010: B.** B states `ratchet=off` and records it in the sentinel when `--baseline` is missing; C's silent persistence is a treatment change the comparison would have to log.
- **X-011: B.** The reviser briefs name the report as input (T06, T08), so a separate `fix-packet.md` breaks the substitution; A agrees (open Q3), B keeps the brief inside the report.
- **X-012: C.** A new user-authorized run with the old run id as parent is coherent; B's option (g) is not.
- **X-013: C.** A stop on a missing skill is the right experimental behaviour; B's downgrade contaminates results.
- **X-014: B.** One bounded, recorded repair of form fields (`repair_used`) saves a review slot that C's ERROR path would consume.
- **X-015: B.** Hunk coverage is the only guard against a PASS produced by reviewer silence.
- **X-016: B.** Requiring a different class than the reviewer is stronger than pinning one model, but it is a prose instruction B cannot check (B risk 5); the impact is low for S1.
- **X-017: A.** "Do not reuse the stop rule" is the safe call against `qa.md:167`; B's row says it reuses "the ratchet idea" and keeps late blockers blocking, which is internally inconsistent.


### Variant C Advocate (haiku:devops)

**Position**

C is the strongest enterprise operating contract: it distinguishes a defective specification from a broken review service, preserves crash evidence, and makes release approval depend on a completed audit rather than a bare PASS (C §§2.2, 2.5–2.6, 6). It is not ready for the promised command-name-only S1 experiment: the installer collision and reviewer/reviser ownership conflicts are real blockers, not details to wave away (diff S-005, X-001, X-011; verified evidence below). Preserve C's deployment and failure semantics while conceding A's stable carried blockers and B's stronger coverage and measurement controls.

**Steelman of Variant A**

A's strongest argument is that a stop rule must stop semantic movement, not merely move judgement into another model. Its three-role table separates raising findings, computing outcomes, and grading; S1 recomputes the previous verdict; S3 rejects an unchanged-section claim of resolution; and S4 freezes confirmed open blockers so later stochastic grading cannot erase them (A §§2.1, 2.3). This is a genuinely maintainable, relatively cheap core, with a computed command-copy diff test and installer-safe protocol skill rather than C's larger operational surface (A §§3.6, 4, 6.2).

**Steelman of Variant B**

B's strongest argument is that lower counted severity is not evidence of a better specification. It adds changed-hunk coverage, canaries, citation read-back, all-demotion auditing at a PASS candidate, and an unmodified final-spec probe measured outside its own classifier (B §§2.3 S2–S7, 5.2–5.4). Its replay explicitly predicts 4.3 surviving blockers from the eight-item control example—above the target—and labels its grader probabilities judgement rather than measurement (B §5.1). That intellectual honesty, report-contained ledger, and use of the Arm B base make B the strongest starting point for an experiment constrained to the existing briefs, subject to resolving scratch-write permission (B §§2.0, 4, 6.2 risk 9).

**Key strengths claimed**

1. **Failure states identify the action an operator should take.** C says a grader timeout produces “ERROR with pending candidates preserved; no demotion, PASS, or fix dispatch”; audit unavailability or a detected real blocker causes HOLD (C §6 failure table). A's missing grade instead “stays blocking,” and B's unconfirmed claims produce FAIL (A §2.3 S5–S6; B §§2.3 S5, 2.4). Stopping delivery is correct in all three, but C avoids treating service failure as a confirmed document defect that can enter a fix cycle. This directly protects the meaning of defect and reliability metrics (diff C-028, X-002).

2. **The cap survives operational interruptions.** C reserves review slots before dispatch, consumes a crashed reservation, requires previous state, and refuses to silently restart a known run (C §2.2). Its audit trail specifies “flush, fsync, then atomically rename” and commits result/state last; late responses cannot revive terminal work (C §§2.6, 6). A's directory guard and B's sentinel constrain completed sequential runs, but neither specifies these interrupted-dispatch and concurrent-writer transitions (A §§2.3 S0–S1, 6.3 risk 8; B §2.3 S0). These are proposed safeguards requiring the crash/lock tests listed in C §3, not proven reliability claims (diff S-006, C-032).

3. **Deployment and rollback are reproducible treatments, not informal copying.** C publishes the verified skill first and command last, checks loaded hashes in a fresh worker, rechecks original-command hashes each round, and quarantines only manifest-owned files after active writers stop (C §4). The experiment coordinator log, phase 4, records an actual machine-wide install disturbance and readiness failures; those are concrete reasons to control loaded versions, not hypothetical enterprise ceremony. C also says rollback does not reverse specification edits, preventing withdrawal of an experiment from being confused with undoing user work (C §4).

4. **The audit measures more than agreement among demoters.** C samples nonblocking dispositions by stratum, confirmed blockers as a comparison group, and every claimed-critical demotion separately; it records inclusion probabilities and requires human adjudication of disagreements (C §5; diff C-013–C-015). It explicitly says this estimates accuracy among reported findings, “not recall of unreported defects,” and may leave rollout quality NOT ESTABLISHED after S1. This is more defensible than interpreting a small favourable sample as production proof; it does not make the auditor infallible.

5. **Blocking-only repair has an explicit submission boundary.** C's separate packet excludes minor findings, and its fix-to-id disposition map rejects unknown or nonblocking ids (C §2.5; diff C-018). A's in-report list and B's “notes are not instructions” are weaker information boundaries (A §2.3 S7; B §3.1 bullet 6). The map checks declared ids, not whether every actual patch is minimal; C acknowledges that semantic limit in §6. This strength requires an authorized reviser contract and cannot be credited to the unchanged S1 briefs.

6. **Provenance checks are tighter than mere membership.** C requires an exact quote at a declared raw span; old-side deletion anchors avoid invented current text; a prior-id exemption needs an identical outcome hash and either an identical quote hash or a changed anchor (C §§2.2–2.4; diff C-010, U-027). A's test only establishes that the cited id was blocking, and B validates membership in the prior confirmed set (A §2.3 S3; B §2.3 S2). C blocks the specific unrelated-prior-id shortcut, although hash equality is brittle under legitimate paraphrase and does not prove semantic identity (C §2.4).

7. **The proposed service objectives have observable sources and bounded scope.** C sets reproducibility, no-fourth-review, independent-grading and latency objectives, exports events/results rather than adding a monitoring service, counts outages in reliability totals, and limits a grader outage to this workflow rather than unrelated deployments (C §§2.6, 5–6). Its 92-minute accepted-work budget excludes human wait, and it explicitly does not promise to bound provider billing without cancellation (C §6). This is useful admission/runbook design, not evidence that any objective has been met (diff U-023, U-029).

**Weaknesses identified in Variant A**

1. **Missing semantic confirmation becomes an actionable blocker.** S5–S6 make a missing grade blocking, while S7 generates a Reviser brief from blocking ids (A §2.3). That can dispatch a specification fix because grading failed, not because an independent judge confirmed harm. C's ERROR preserves the candidate and stops dispatch without inventing that confirmation (C §6; X-002).

2. **The online audit misses dispositions and rounds.** A audits at most three grader-demoted findings only on PASS; its own risk discussion acknowledges that a one-in-five error rate can be missed about half the time (A §§2.6, 6.3 risk 1). Form-failed and late-found items are listed or audited offline, not covered by that release-time sample. C's stratified per-round pool is stronger operational visibility, though B's all-demotions PASS audit is stronger coverage than C's sample (C §5; B §2.3 S7).

3. **The stated brief compatibility is not true.** A writes findings, cards and ledgers into its loop directory while claiming only a command-name substitution (A §§2.2–2.4, 4). The saved S1 T07 task text says “write ONLY your output file” and “no edits to the spec or any other file.” C has the same defect; neither design may turn an instruction to use a command into permission for additional repository outputs (X-001).

4. **The report still supplies competing repair material.** A says minor-applying is removed, but its own open question 3 acknowledges that the reviser reads the full report (A §§6.1, 7). Saved T06 tells the reviser to verify “each numbered finding”; T08 names the report's findings and citation corrections, not a generated blocking-only list. A's tighter list is useful guidance, not a mechanical routing guarantee; C's stronger packet routing also needs a changed brief (X-011).

5. **Line overlap is not defect novelty.** A accepts any matching quote span that touches changed lines and includes neighbours of pure deletions (A §2.3 S3). B's defective-word span and baseline-outcome question are a stronger attempt to distinguish an old defect from a new one inside a touched paragraph (B §2.3 S2–S5). C's line-overlap gate shares A's limitation despite its stronger prior links (diff C-010).

**Weaknesses identified in Variant B**

1. **FAIL conflates defect, coverage omission and unavailable infrastructure.** B's verdict function includes unconfirmed grades and uncovered hunks in FAIL; its missing-agent path also returns FAIL (B §§2.4, 3.2). These conditions should prevent release, but only confirmed findings belong in a defect-repair packet. C's separate ERROR/HOLD states make operator action and SLO accounting clearer (C §§2.5, 6; X-002).

2. **The fallback changes the treatment under the variant name.** B explicitly runs the 427 loop if the skill is missing (B §3.1). The header is honest, but the requested computed gate is absent; this run cannot count as stoprule completion. C's E-SKILL-MISSING stop is the safer admission contract (C §3; X-013).

3. **The experiment copy procedure does not enforce its no-overwrite claim.** B labels its manual route “no overwrite of any existing file” but gives ordinary copy operations without an absence guard or no-clobber publication (B §4). C requires absent destinations and manifest ownership before publication or withdrawal (C §4). This matters especially because an interrupted three-part install can expose a command before its dependencies are ready (B §4 install order; C §4 skill-first publication).

4. **Audit disagreement is actionable only on one branch.** B promotes a real demotion at PASS but only records it as contested on an already-FAIL path; its open question 2 acknowledges this choice (B §§2.3 S7, 7). The same audit evidence should at least HOLD delivery and appear in the handoff regardless of current verdict, as in C §§2.5, 5–6. C's immutable review verdict is defensible only when every release consumer checks audit status too (X-007).

5. **Calibration and cost controls are not equivalent to service reliability.** B's canaries test known simple cases, and B itself says they do not prevent patterned cross-reference mistakes (B §6.2 risk 4). Its 6–12 extra agent calls and 18–30-minute added loop estimate are explicitly unmeasured, while F7 is an after-the-fact usability rejection threshold rather than persisted deadlines (B §§5.4, 6.1). C's accepted-result deadlines and outage states add operational bounds, with the honest limitation that cancellation and billed execution remain unverified (C §6).

**Concessions**

- **S-005 is confirmed, and C must change before deployment.** In `/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/src/superclaude/cli/install_skills.py`, the activation regex accepts a standalone `Skill <name>` line, `_has_corresponding_command` strips only `sc-`, and the served-by-command branch skips installation and removes a stale skill directory. C §3's sentence beginning “Load skill” does not match; C's matching command/skill names therefore enter that removal path. Adopt A/B's protocol-suffixed skill name and explicit activation convention, or supply the exact recognized activation line consistently. I prefer the established protocol name; C's manual deployment merely avoids this installer branch temporarily and does not repair it. No installer change or installation was performed here.

- **X-001 and X-011 defeat C's unchanged-brief claim.** The saved S1 T07 reviewer task permits only the report; T08 permits only the spec and disposition output and directs the reviser to a specific report findings section. C §§2.5–2.6 and 4–5 instead require additional state files, a declared run mapping and a separate packet. C needs separately authorized output and dispatch contracts, recorded as a different treatment, before its growth prediction can be tested. B wins the repository-output comparison, but its private scratch writes still need authorization: “no ... any other file” is not automatically a repository-only restriction.

- **There is another inherited brief conflict.** Saved T07 says “any finding of any severity is FAIL.” That conflicts with every variant's blocking-only verdict, not merely C's state layout. The experiment must resolve instruction precedence explicitly rather than silently treating a substituted command as permission to ignore the task text. This is a design admission issue, not authorization to rewrite the briefs in this debate.

- **A wins carried-blocker stability.** Regrading every open prior in C §2.4 allows a later minor answer to remove an unchanged confirmed defect. Putting reversals in a sampled audit pool does not guarantee they are examined (C §5). A §2.3 S4's freeze avoids that stochastic escape; adopt it, with an explicit adjudicated correction path rather than routine regrading (X-003).

- **B wins coverage, label independence and the external outcome check.** C has no changed-hunk coverage receipt, and a reviewer MINOR cannot be promoted by its grader (C §§2.4, 3). B's coverage checks, label-free claim schema and final unmodified probe reduce these blind spots (B §§2.2–2.4, 5.2). C's claim to audit accuracy among reported findings explicitly does not cover unreported defects (C §5). Adopt those controls without calling a missing coverage receipt a proven document blocker.

- **C's dispatch and size need tightening.** A/B give installed grader definitions; C only specifies a fresh agent and conditional tool isolation (diff S-004; C §§2.4, 7). C needs a pinned dispatch/brief contract and a live capability receipt before independence is claimed. Its many per-round files and crash tests are justified for a resumable enterprise pilot, not necessarily the smallest S1 prototype (diff S-003, S-006; C §§2.6, 3).

- **Predictions remain hypotheses.** C's mean 2.5 blockers and 25% growth are not measured, its original base is not held identical to Arm B, and its audit cannot establish the proposed rollout bar from two replicates (C §5; B §§4, 5.1). B's base-controlled experiment and outside-classifier probe are superior for causal interpretation (X-009). C's bare `verdict: PASS` must never be used alone when an audit HOLD exists: the downstream conjunction in C §6 is mandatory, not optional reassurance.

**Shared assumptions (A-NNN: ACCEPT/REJECT/QUALIFY + reason)**

- A-001: QUALIFY — The helper is specified as stdlib-only with no model calls; readiness still requires the worker's actual runtime and permissions (C §§2.1, 3; A §4).
- A-002: QUALIFY — Fresh context is required, but dispatch and tool restrictions need demonstrated capability; C stops ERROR if fresh context is unavailable (C §§2.4, 7).
- A-003: QUALIFY — A finding on a fix-written line remains eligible, not automatically real or blocking; quote/outcome and confirmation gates still apply (C §2.4; B §2.7).
- A-004: ACCEPT — A cooperating controller is an explicit enforcement boundary, and no text test forces invocation (C §6; B §2.6).
- A-005: QUALIFY — The count is run-scoped; C preserves a parent run id and requires user authorization for a new run, but cannot prevent bypass by a noncooperating caller (C §§2.5, 6).
- A-006: REJECT — C §5 calls audit an estimate, admits it lacks unreported-defect recall, and sends only disagreements to a human; B §6.2 risk 5 admits correlated model limitations. Neither agreement nor a small spot-check establishes ground truth when grader and auditor share an error. A future pilot needs independent human checks of some agreements as well as disagreements; current error rates must remain auditor-relative estimates.
- A-007: QUALIFY — Normal-path availability is an unmeasured precondition, not an accepted reliability fact. C §6 explicitly includes unavailable graders and crashes in reliability totals and routes them to ERROR/HOLD; measure valid-response rate and completion latency across all admitted runs before trusting cost or convergence claims (C §5 says ERROR/HOLD is not successful convergence).
- A-008: REJECT — Reproducible sampling does not prove unbiased or unsteerable selection. A §2.3 S4 and B §3.2 use reviewer-authored content hashes; C §5 specifies pre-response commitment but no independent seed source. A defensible future pilot needs an operator/controller-generated independent seed committed before findings are submitted, with recorded selection probabilities; no variant currently specifies that complete protection.
- A-009: QUALIFY — Less repair material may reduce growth, but proportionality is unverified and C's packet is not routed by existing briefs (B §5.3; C §§2.5, 5; saved T06/T08).
- A-010: QUALIFY — Quote-only grading is deliberately blinded, but context sufficiency remains C §7's open question; full-snapshot audits test its error, not universal adequacy.
- A-011: QUALIFY — Reporting both counts is necessary, not sufficient for comparable quality. C §5 rejects relabeling-only gains; B §5.2's unmodified probe adds an outcome not defined by the gate.
- A-012: QUALIFY — Record requested and observed model identities separately when observation exists; B §7 question 4 and C §7 leave actual dispatch capability unverified.
- A-013: QUALIFY — Different class is a useful experimental distinction, not proof of independent errors; same-class fresh runs need separate reporting (C §7; B §6.2 risk 5).
- A-014: QUALIFY — Scoped loop convergence can stop on late-found debt, but an audited true blocker still HOLDs C's delivery; this is not permission to ship a known critical loss (C §§5–6, 8).
- A-015: ACCEPT — C §§1 and 5 explicitly limit S1 to a large-effect screen and leave later rollout evidence necessary.
- A-016: REJECT — Saved S1 T07 explicitly permits only its output file and forbids edits to any other file. C's additional run tree is not authorized by those words; B's scratch permission also remains unresolved (saved T07; C §2.6; B §6.2 risk 9).
- A-017: REJECT — Saved T06/T08 name the full report and require dispositions for each finding/citation; they do not route a packet-only reviser. C §2.5's isolation and A/B's list priority cannot be assumed from command substitution alone.

**Contradiction positions (X-NNN: winner A/B/C + one-line reason)**

- X-001: winner B — Its report-contained ledger respects the named repository output better than A/C's extra run files; private scratch permission still needs resolution against saved T07's “any other file” restriction (B §2.0; C §2.6).
- X-002: winner C — Grader failure is ERROR without fix dispatch, not independent confirmation of a defect; release stays blocked and reliability accounting remains distinct (C §6; A §2.3 S5; B §2.4).
- X-003: winner A — Freezing an open confirmed blocker prevents an unchanged defect disappearing through stochastic regrading; C's sampled reversal audit is insufficient (A §2.3 S4; C §§2.4, 5).
- X-004: winner C — Grading evidence-valid late-found claims preserves their semantic impact for handoff and audit without reopening the capped fix loop (C §2.4 step 3; A §2.3 S4).
- X-005: winner C — Removing conflicting severity and synthesis gates makes the frozen rubric authoritative; a diagnostic boundary-table blank must not independently stall synthesis (C §2.1; A §3.1 item 4; B §3.1).
- X-006: winner B — Removing reviewer labels from the claim schema closes A/C's MINOR-label veto on independent confirmation (B §2.2; C §2.4 step 6).
- X-007: winner C — Retaining the original computed review result and issuing a separate audit HOLD preserves attribution, provided release checks require PASS plus completed non-HOLD audit; bare-line consumers are unsafe (C §§2.5, 6).
- X-008: winner A — The inspected installer skips existing skills without force and preserves protocol-suffixed skills; C's unsuffixed prose activation instead triggers the command-backed skip/removal branch (install_skills.py; A §§3.1, 4; C §3).
- X-009: winner B — Using the Arm B base for measurement controls the base-text covariate rather than merely logging a different command copy (B §4; A §4; C §3).
- X-010: winner C — Persisted snapshots and prior state keep the ratchet active when historical flags are absent, but supplying a stable run mapping is an added harness contract, not free compatibility (C §§2.2, 4).
- X-011: winner A — A explicitly admits a separate reviser-only file requires a brief change; saved T06/T08 confirm C's packet-only routing cannot follow from name substitution (A §7 question 3; C §§2.5, 5).
- X-012: winner C — A terminal three-review run stays terminal and any authorized continuation preserves parent provenance; B's extra-cycle option lacks a matching bypass for its own cap exit (C §2.5; B §§2.3 S0, 2.5).
- X-013: winner C — A missing controller dependency must stop the experimental workflow rather than run a different treatment under its name (C §3; B §3.1 fallback).
- X-014: winner B — One recorded, field-limited form repair can reduce avoidable infrastructure failures without adding a new document review, if the same reservation/deadline is retained; C currently rejects it outright (B §2.3 S2; C §6).
- X-015: winner B — Requiring a claim or coverage receipt per changed hunk prevents uncovered work silently passing, although missing coverage should be an incomplete review rather than a proven spec defect (B §§2.3 S2, 2.4; C §3).
- X-016: winner C — Prefer cross-class grading but record same-class fresh separately when unavailable; do not claim unavailable capabilities or equivalent independence (C §§2.4, 7; B §2.3 S4).
- X-017: winner C — Preserve implement's existing late-blocker and final-review policy; any transfer needs separate authorization and adapter evidence rather than calling policy change harmless reuse (C §8; B §8).


## Round 2: Rebuttals

### Variant A Rebuttal (opus:architect)

Paths: `D` = this adversarial folder; `FLG2` = `exp346-ab-flg-r2/.dev/experiments/346-validation/phase4/flg-r2/`; `CTL1` = `exp346-ab-ctl-r1/.dev/experiments/346-validation/phase4/ctl-r1/`; `TPL` = `exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/templates/`; `S1A` = `exp346-s1-armA-repA/.dev/experiments/346-validation/phase3/S1-armA-repA/evidence/dispatched-task-text/`. All were read in this round.

#### 1 Response to criticisms

Each item starts with the critic's strongest version of the point.

**B-1 / C-3: A breaks "name substitution only" (X-001). Conceded, with one correction to B's mechanism.**
Steelman: the briefs say "write ONLY your output file" (`S1A/T07-R2-review.txt`), and A's loop directory adds several reviewer- and script-written files. Correction: B says the validity check's `git status --short` "would list" A's files as unexpected. In flg-r2 it shows only `?? .dev/orca-command-refactor/` (`FLG2/validity.md:100`). The review folder is inside that directory (`FLG2/reviews/spec-panel-round3.md:7-9`), so a collapsed untracked-directory line would hide A's files. That makes the problem worse for A, not better: the check would not catch the breach, and the reviewer's own behaviour would. The flg-r2 R3 reviewer skipped a step the command required because "the brief allows writing only this file" (`FLG2/reviews/spec-panel-round3.md:176`; also `spec-panel-round2.md:227`). A reviewer that resolves a command-versus-brief write conflict in favour of the brief would skip `findings-r<N>.json`, and A's `check` would then stop the run. The merge must use B's report-embedded ledger with `/tmp` scratch.

**B-2 / C weakness 7: label-gated candidates let a reviewer hide a blocker as minor (X-006). Conceded in part, so I change my position.**
Steelman: A S3 states "A finding the reviewer called minor is never raised", so the label still gates a decision, and label drift is the measured failure. My Round 1 reply was that B's choice of what to `claim` is the same gate. That holds for silence, which coverage handles, but not for a finding written with a quote and an outcome and then labelled minor. Merge: every finding that passes the form check (quote plus outcome) goes into the one grader batch, whatever its `claimed` value. The cost is tokens in the same call, not extra calls (A 6.2). The `claimed` label stays, for reporting only, so the A-011 proxy survives and B's lost-independence problem with M1b (B 5.3) does not arise.

**B-3: a final PASS is never checked (A risk 7). Conceded.**
`verify-prior` runs only when a next review starts. With the ledger embedded in the report (B S9/S10), the skill runs `check` straight after appending, and the recorder re-runs it. The rest of `verify-prior` (exit 5 on a hand-written line, U-002) stays, and it reads review N-1 from the prior report instead of from `ledger-r<N-1>.json`.

**B-4 / C-2: the audit is thin. Conceded on the in-run audit; the offline audit stays.**
Steelman: with k=3, a 1-in-5 error rate is missed about half the time (A risk 1). Demotions per loop are few, so the merge audits all demotions at a PASS candidate in one auditor call (B S7). The offline audit also samples confirmed blockers (C U-026). I reject C's per-round 25% audit with a human HOLD: the S1 loop has no human inside it (B weakness 8 against C).

**B-5: the ratchet rarely bites, and the prediction has no replay. The first half is not a weakness; the second is conceded with new data.**
A says itself that the R3 drop "does not come from the ratchet on 427-style runs" (A section 5). That is a calibrated statement, not a defect. The prediction, though, was reasoning without a replay. A hand replay is in section 3, item 3: it gives about 4-5 on ctl-r1, not 3. I now accept B's 4.3 as the better point estimate for a control-like run.

**B-6: base-file confound (X-009). Already conceded in Round 1;** use B's 472-line Arm B copy.

**B-7: JSON fragility. Conceded;** take B's single counted repair (exit 3 once). In the merge it also covers uncovered hunks (see the coverage item below).

**C-1: a missing grade becomes a blocker the reviser acts on (X-002). Conceded on dispatch; rejected on the verdict.**
Steelman: in A, S6 counts `grade=missing` as blocking and S7 lists every `final=blocking` id in the Reviser brief. A grader outage can therefore start a spec fix that no judge confirmed. That is a real defect in A, and C names the right fix. C's remedy, a third terminal state, conflicts with the brief, which demands "a binary PASS or FAIL verdict" (`S1A/T07-R2-review.txt`; B weakness 2a against C). Merge: an unconfirmed claim still gives FAIL, but it is listed as `unconfirmed`, never in the Reviser brief. A FAIL whose brief would be empty (B concession 8) is marked `reason: unconfirmed-only` in the sentinel, and no reviser is dispatched. Under the A-007 rule, more than one such review makes the replicate invalid. This keeps C's meaning (infrastructure failure is not a document defect) inside a binary verdict.

**C-4: the report still gives the reviser competing repair material (X-011). Conceded, and the record shows it is worse than any variant said (section 3, item 1).**

**C-5: line overlap is not defect novelty. Rejected, but I take C's prior-link rule.**
Steelman: a quote that touches a changed line may describe an old defect. B's stricter span-novelty rule, however, demotes defects that B's own replay calls real and late (R3-4, R3-9; B 5.1 and open Q1). For a mechanism whose main failure mode is wiping out defects (A risk 1), line overlap is the more conservative demoter. The laundering hole it leaves (A risk 3) is better closed by C's prior-link hash rule (U-027) than by a stricter anchor.

**C weakness 7 against A, and B: no coverage guard (X-015). Conceded in Round 1;** refined below.

#### 2 Updated assessment of B and C after their Round 1 defenses

- **B** conceded the cap override (X-012), the fallback (X-013), the FR-8/FR-9 text (X-005), the hole in its freeze (X-003), the undefined empty brief, and its own weight (B concessions 1-6, 8). What survives is strong and portable: the report-only footprint, hunk coverage, the single repair, the label-free grading input, M1c, the base-file control and the replay. Its weak spots are ones a merge can drop. Span novelty demotes real defects (B concession 7), the two-mode grader audits itself (A weakness 6 against B), and 10 subcommands with 6-12 agent calls cost more than the screen needs. B's reply to my X-006 argument showed that a label is harmful when it gates. It does not show that a label is useless when it only reports. My position changes accordingly.
- **C** conceded every blocker it had against the experiment: the install defect, X-001, X-011, carried-blocker re-grading, coverage and grader pinning (C concessions). Its lasting value is semantic, not operational. That value is: separating infrastructure failure from defects, the prior-link hash, the fix-to-id map, the two-sided audit and fail-closed activation. The locks, fsync, deadlines and SLOs remain out of scale for n=2. C's own advocate says "B is the strongest starting point" for an experiment held to the existing briefs (C steelman of B). I weigh that below.

#### 3 New evidence (not in Round 1)

1. **The reviser brief is a coordinator-filled template that names every finding, including minors.** `TPL/T08-R2-reviser.TEMPLATE.txt` says "findings {{R2_FIRST_ID}}-{{R2_LAST_ID}}", then "verify each finding against live evidence; apply confirmed ones", then "Acceptance: every {{R2_FIRST_ID}}-{{R2_LAST_ID}} ... have a row". In flg-r2 the coordinator filled the range as "N1 to N11", while the report's own `## Reviser brief` named only N1-N6, and 15 of 15 rows were applied (`FLG2/validity.md:76,79`). So "confirmed" in the brief means confirmed by the reviser's own check, not by any list in the report. A's claim that "apply confirmed findings now resolves to the script-written list" (A section 4) is wrong. B's and C's growth predictions share the same premise (A-009/A-017). **Merge fix that keeps the brief text byte-identical:** the script numbers confirmed blocking ids first and contiguously. The coordinator fills `{{R2_FIRST_ID}}-{{R2_LAST_ID}}` from the script's brief and sets `{{R2_CITATION_COUNT}}` to the number of confirmed citation blockers. This is a change to the placeholder values, and the validity check already records placeholder values as "listed substitutions" (`FLG2/validity.md:69,79`). The pre-registration must state it as part of the treatment.
2. **Reviewers obey the brief's write rule over the command** (`FLG2/reviews/spec-panel-round3.md:176`). This explains why X-001 decides the matter, while the `git status` check alone would not (section 1, B-1).
3. **Hand replay of A's rules on ctl-r1 R3 (my judgement, not a measurement).** CTL1's R3 has 8 blocking rows: R3-1 to R3-6, R3-8 and R3-9 (`CTL1/reviews/spec-panel-round3.md:181-189`).
   - R3-8 is late-found ("Present in the round-2 input, not flagged then").
   - R3-9 carries a recorded minor-versus-MAJOR split (`:170`), so rubric R4 sends it to the grader as minor unless R1 holds.
   - R3-2 is a misattributed citation with no wrong build outcome, so R1(b) likely makes it minor.
   - R3-4 survives under line overlap only if its quote touches a fix-written line, which B counts as baseline text.
   Result: about 4-5 survive, against A's committed 3. In flg-r2 R3, N12 is the only blocker. It is "MAJOR, blocking, origin=changed" (`FLG2/reviews/spec-panel-round3.md:84`), states a wrong outcome ("yields a false P0 record", `:177` decisions table), and the panel split on it (`FLG2/validity.md`, V1(c)). Under R4 plus R1 it stays blocking, so 1, as A and B predicted. Conclusion: the R3 bar for both replicates rests on the stoprule arm behaving like Arm B, not like the control. B's chance of about 0.5 is the honest figure, and my 60% was optimistic.
4. **FR-8/FR-9 are worse than "MAJOR minimum".** Today's bullet 2 reads "CRITICAL and FR-8/FR-9 findings are blocking" (`src/superclaude/commands/spec-panel.md:259`), on top of the "MAJOR severity minimum" floors (`:328-329`). B replaces bullet 2 but leaves lines 328-329 in place, so a GAP row still produces a mandatory MAJOR finding that the reviewer reads as weighty. That strengthens X-005 for A. FR-10 (`:330`) gates synthesis on table completeness. It is not about severity, so C's removal of it is still scope creep.
5. **The install facts re-checked.** The installer docstring states the policy outright: protocol skills "are INTENTIONALLY installed standalone" and the match "strips ONLY the 'sc-' prefix" (`src/superclaude/cli/install_skills.py:13-21`). The served-by-command branch runs `shutil.rmtree` on a stale install (`:88-98`), and an existing skill is skipped without `force` (`:102-104`). X-008 and S-005 stand as Round 1 stated.
6. **The inherited verdict rule is handled in practice by reporting both rules.** The flg-r2 reviewers wrote both "the brief's" and "the command's" verdicts (`FLG2/reviews/spec-panel-round3.md:15,170`). Under the stoprule a minors-only review would print a brief-FAIL beside a script-PASS. The merged spec must say that the coordinator and the metric read only the script's last line, and that the brief-rule verdict is recorded as a covariate.

#### 4 Updated contradiction positions

- **X-001: B.** The briefs allow only the report, and the reviewer obeys that over the command (`spec-panel-round3.md:176`). Unchanged.
- **X-002: A, modified toward C.** The verdict stays binary because the brief demands it. Unconfirmed claims never enter the Reviser brief, and an unconfirmed-only FAIL dispatches no reviser. Unchanged winner, changed rule.
- **X-003: A.** Freezing carried blockers stops attrition; B and C both conceded this. Unchanged.
- **X-004: C (changed from A).** Once form-valid findings of every label go into the one batch (X-006), adding late-found claims costs tokens, not calls. It gives the user an independent grade in `escalation.md` and still cannot change the verdict.
- **X-005: A.** Edit lines 328-329 at the source and replace bullet 2 (`:259`); leave FR-10 alone. Unchanged.
- **X-006: B (changed from A).** The label must not gate grading. A keeps it for reporting only, so the proxy survives.
- **X-007: A.** A reinstated demotion recomputes FAIL with no human inside the loop. The pre-audit verdict is recorded in the sentinel, for C's attribution point. Unchanged.
- **X-008: A.** Re-verified in `install_skills.py:13-21, 88-104`. Unchanged.
- **X-009: B.** The same 472-line base as Arm B. Unchanged.
- **X-010: B (changed from A).** A and B agree that the ratchet needs `--baseline`. B also defines the missing-flag path and records `ratchet=off` in the sentinel. C's persisted baselines need repository writes.
- **X-011: A.** No variant routes the reviser through unchanged placeholder values (`T08` template). A alone admitted this. The placeholder-fill rule above is the fix. Unchanged.
- **X-012: C (changed from A).** A and C agree that the cap cannot be lifted inside a loop. C adds parent-run-id lineage, so a user-authorized restart is traceable.
- **X-013: C.** Fail closed on a missing skill. Unchanged.
- **X-014: B.** One counted repair, extended in the merge to uncovered hunks inside the same review. Unchanged.
- **X-015: B.** Hunk coverage. Following C, an uncovered hunk after the repair gives FAIL `unconfirmed-only` (no reviser dispatch), not a confirmed defect. Unchanged winner.
- **X-016: A.** A model pinned in the agent's frontmatter can be reviewed. Record `same-class` when it applies. Unchanged.
- **X-017: A.** "Do not reuse the stop rule" for `/sc:implement`; C's wording is equivalent and B's is inconsistent. Unchanged.

#### 5 Merge recommendation

**Base: Variant A.** This is close. B's and C's advocates both prefer B as the experimental base, and the one structural element A loses, storage, comes from B. I still choose A, for three reasons:

- A's script I/O is confined to one place ("Every subcommand writes only inside `--loop-dir`", A 3.4), so swapping that layer for B's `/tmp` plus embedded ledger is a local change to `main()`, not a redesign.
- A carries the parts no one disputed and B would have to import: the three-role ownership table (2.1), the freeze (X-003), `verify-prior` (U-002), the prior-status guard (U-003), the FR-8/FR-9 edit (X-005), the declared grader agent (X-016), the install contract (X-008), the computed-diff drift test (U-006) and the scoped reuse section (X-017).
- A has 9 subcommands and 2-3 agent calls per loop, against B's 10 and 6-12 (A 6.2, B 6.1).

**Top 5 elements to take from the others:**

1. **From B: storage and the seal.** Private `/tmp` scratch, the sealed ledger plus sentinel embedded in the report, `finalize` refusing a hand-typed verdict, and `check` run at every review including the final PASS (B 2.0, S9-S10). This closes X-001 and A risk 7.
2. **From B: hunk coverage with a single counted repair.** Every changed hunk needs a claim or a `checked` line. Form defects and uncovered hunks get one repair (exit 3) inside the same review, and what remains gives FAIL `unconfirmed-only` (B S2, 2.4; X-014, X-015).
3. **From C: failure semantics inside a binary verdict.** Fail-closed `E-SKILL-MISSING` (X-013). Unconfirmed claims never reach the reviser (X-002). Parent-run-id lineage on a user-authorized restart (X-012). The fix-to-id disposition map checked by `stoprule.py` against the disposition file the brief already requires (U-024).
4. **From C: the prior-link hash rule and the two-sided offline audit.** A `prior` link is valid only with an identical outcome hash and either an identical quote hash or a changed anchor (U-027). The offline audit samples confirmed blockers as well as demotions (U-026). The seed is `sha256(nonce || review || ledger)`, with the nonce written by `init` before review 1 (A-008).
5. **From B: the measurement controls.** The 472-line Arm B base copy (X-009), the M1c unmodified probe (U-015), and the offline replay gate on the real R3 reports before any live run (U-014). The replay is also the place to check this rebuttal's hand estimate of 4-5 for ctl-r1.

**A-side changes the merge also needs (from this round's evidence):**

- (a) Grade every form-valid finding, whatever its label (X-006).
- (b) Number confirmed ids first and contiguously, and have the coordinator fill the reviser template's id range from the script's brief, stated as part of the treatment (new evidence 1).
- (c) The coordinator and the metric read only the script's last line; the brief-rule verdict is recorded as a covariate (new evidence 6).
- (d) Withdraw A's 60% confidence and its r1=3 point estimate in favour of B's replay-derived figures.


### Variant B Rebuttal (sonnet:analyzer)

Paths: `D` = this adversarial folder; `FLG2` = `exp346-ab-flg-r2/.dev/experiments/346-validation/phase4/flg-r2/`; `TPL` = `exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/templates/`; `S1A` = `exp346-s1-armA-repA/.dev/experiments/346-validation/phase3/S1-armA-repA/evidence/dispatched-task-text/`. I re-read all of these in this round.

#### 1 Response to criticisms

Each item gives the critic's strongest form first.

**A-1 (X-012): option (g) "authorize one extra cycle" contradicts B's own `begin` exit 4 (B 2.5 g vs S0). CONCEDED.** There is no mechanism behind (g). Adopt C's rule: a user-authorized restart is a new run that records the old run id as parent (C 2.5). The escalation text offers "accept with known issues" or "start a new run"; it never says the loop lifts its own cap.

**A-2 / C-2 (X-013): the missing-skill fallback runs a 427 loop under the variant's name (B 3.1). CONCEDED.** With n=2, one such run is half the arm. Replace the fallback with C's fail-closed stop (`E-SKILL-MISSING`, no fallback).

**A-3 (X-005): FR-8/FR-9 "MAJOR severity minimum" stays in the file and contradicts the new bullet 2. CONCEDED, and A's evidence is stronger than A said.** I checked `src/superclaude/commands/spec-panel.md:328-329`: "automatically generates a finding with MAJOR severity minimum". Bullet 2 says an FR-8/FR-9 row "is not an automatic MAJOR" (B 3.1). A reviewer reads both. Edit lines 328-329 at the source, as A does. Leave FR-10 (`:330`) alone: it gates synthesis on table completeness, which is not about severity, so C's removal has no evidence behind it.

**A-4 (X-006): "no label" only renames the reviewer's gate; the choice of what to `claim` is still a gate, and without labels the M1b proxy loses its independence (B 5.3). PARTLY CONCEDED.**
- Where A is right: the proxy. I accept A's resolution, a `claimed` field that no computation reads and that exists only for reporting. It gives M1b back at no cost to the grading path, and A has already moved to this position (A R2 section 1).
- Where I stand: the two gates differ. A reviewer who chooses not to claim a changed hunk must write a `checked` line for it (B S1, 2.4). That line is covered by the unclaimed-hunk probe and by the offline audit, so silence is checked and costly. A reviewer who writes a quote and an outcome and then calls it minor, as in A and C, removes the finding with one word that nothing checks. These are not the same gate.

**A-5: B rejects a judged anchor as weak (open Q1) yet adds grader Q2 as a second lateness gate (S5). CONCEDED.** This is an inconsistency in my own text. The replay (B 5.1) shows Q2 moves exactly one of eight claims (R3-8, from about 0.9 to 0.2), and that probability is my own judgement. Q2 is the least verified part of the design. Change: Q2 stays in the batch and in the ledger as data, but it no longer demotes. Only the lexical `span_novel` rule and the `prior` link decide `late-found`.

**A-6: the audit is the same agent body as the grader with only the model changed (B 3.3). CONCEDED in substance.** A 15-line context window cannot catch a cross-reference error, and my own risk 4 says so. The auditor becomes a separate fresh call that sees the full spec and no grader reason, as in A 2.6 and C section 5. The `finding-grader` file keeps only the `grade` mode.

**A-7: largest per-review overhead, 6-12 agent calls and 27-33 Bash calls per loop (B 6.1), with my own F7 sitting close to the estimate. CONCEDED, with a cut I am adopting.** The per-review FAIL-path audit (up to 3 demotions plus one hunk probe) cannot change a FAIL verdict. It only produces a `contested` count (B S7). Move it offline, as A and C already do, and keep the in-run audit for the PASS candidate only. My estimate of the result is 3-7 agent calls per loop (grader batches plus at most one PASS audit), against 6-12 now. That is my judgement, to be measured by M6. Canaries stay: they ride in the same grader call.

**A-8 (X-017): the reuse row says B reuses "the ratchet idea" but keeps late blockers blocking; a ratchet that never demotes is empty. CONCEDED.** `qa.md:167` makes this a policy difference. Adopt "do not reuse the stop rule" for `/sc:implement`.

**A-9 (A R2 new evidence 1, and C weakness 4 against A): the Reviser brief is not what the reviser reads. CONCEDED, and it applies to B as much as to anyone.** I checked `TPL/T08-R2-reviser.TEMPLATE.txt`: it says "section 5, findings {{R2_FIRST_ID}}-{{R2_LAST_ID}}, plus the {{R2_CITATION_COUNT}} overstated citations", then "verify each finding ... apply confirmed ones", then requires a row for every id in that range. In flg-r2 the coordinator filled "N1 to N11" and 4 citations (`FLG2/validity.md` V4, T08 row) while the report's own `## Reviser brief` named only N1-N6 (`FLG2/reviews/spec-panel-round2.md:246-247`), and 15 of 15 rows were applied. My "notes are not instructions" (B 3.1 bullet 6) therefore cannot hold. A's fix is the right one: the script numbers confirmed blocking ids first and contiguously, and the coordinator fills the range and the citation count from the script's brief. It changes placeholder values only, which the validity check already records as listed substitutions (V4). It must be stated in the pre-registration as part of the treatment.

**A-10 (X-001, A's correction of my mechanism): `git status --short` shows one collapsed line, so it would not list A's extra files. ACCEPTED on flg-r2, with one limit that A's own text supplies.** `FLG2/validity.md` V6 item 2 shows only `?? .dev/orca-command-refactor/`, so extra files inside that directory stay hidden. But A's default for a first review is `./.dev/spec-panel-stoprule/<stem>/` (A 2.2, `variant-1-opus-architect.md:32`), which sits outside that directory and would add a new `??` line at review 1. For reviews 2 and 3 the loop directory is the `--re-review` file's directory, so A's point holds there. The stronger ground is the brief's literal text, "write ONLY your output file" (`S1A/T07`), as A now agrees. My own `/tmp` scratch is not exempt from that text; see section 3, item 4.

**C-1: FAIL conflates a document defect, a coverage omission and an infrastructure failure (B 2.4, 3.2). CONCEDED on the reasons, REJECTED on a third state.** `S1A/T07` demands "a binary PASS or FAIL verdict", so C's ERROR and HOLD would leave the brief unmet. Instead keep FAIL, with a reason code in the sentinel: `confirmed`, `unresolved-prior`, or `incomplete` (an `unconfirmed` claim or an uncovered hunk). Only the first two feed the Reviser brief; an `incomplete`-only FAIL dispatches no reviser. That also closes the undefined empty-brief case I raised against myself (B concession 8). More than one `incomplete` review in a loop marks the replicate invalid for M1, which is C's point that infrastructure failure is not a defect, expressed inside a binary verdict (A-007).

**C-3: the "no overwrite" install claim has no guard, and the command is published before its dependencies (B 4). CONCEDED.** Use an absence check before any copy (`test ! -e` on each destination, or `cp -n`), publish the agent and skill first and the command last, then run the `sha256sum -c` check. This is C's order (C 4).

**C-4 (X-007): an audit disagreement is actionable on only one branch (B S7, open Q2). REJECTED as a verdict problem, CONCEDED as a visibility problem.** On a FAIL path the verdict is already FAIL, and a review-3 reinstatement could not start a fourth review anyway. A contested demotion on the FAIL path is listed in the Escalation (c) and in the offline audit. At a PASS candidate the all-demotions audit blocks the PASS, which has the same effect as A's "recompute FAIL". C's HOLD is rejected for the binary-verdict reason in C-1.

**C-5: canaries and F7 are not service reliability (B 5.4, 6.2). CONCEDED.** They are calibration and a usability falsifier, not deadlines. S1 cannot show an SLO and I do not claim one. I do not adopt C's 92-minute loop deadline, which is a proposal with no measured baseline (C section 6).

#### 2 Updated assessment of A and C

**Variant A.** Steelman: A's R2 is the most self-correcting document in the debate. It gives up X-001, the label gate (X-006), the final-PASS gap, the thin audit, its own 60% confidence and its r1=3 estimate, and it found the template evidence in section 1, A-9, that none of us had. Its ownership table (A 2.1), the freeze of carried priors (A S4), the source edit of FR-8/FR-9 and the install facts (X-008) are the best parts of any variant. Critique:
- After its concessions A's R2 imports from B the storage layer, the seal, hunk coverage, the single repair, the replay, the M1c probe, the base file and the label-free grading, nearly the whole of B's section 2. A's own defense of choosing A as base rests on "swapping that layer is a local change to `main()`". It is not local: `verify-prior` reads `ledger-r<N-1>.json` today, `cards` and `grades` are separate files, and "every subcommand writes only inside `--loop-dir`" (A 3.4) would all change.
- A's default loop directory for review 1 is outside the report directory (`variant-1-opus-architect.md:32`), a point A's correction of me did not address.
- A still grades every form-valid finding in one batch. With the label removed from gating, the grader now sees minor-labelled items as well, which is what B does by design; the difference between A and B shrinks to B's hunk coverage and canaries.

**Variant C.** Steelman: C has the best semantics of the three. Infrastructure failure is a different thing from a defect (C 2.5, section 6); the prior-link hash rule closes the "cite an unrelated prior id" hole (C 2.4); the fix-to-id disposition map is the only mechanical reviser check (C 2.5); and the two-sided audit measures the grader in both directions (C section 5). C also conceded every blocker against the experiment, which I respect. Critique:
- C's concessions cover the install defect, the extra files and the packet, but not its terminal states. ERROR and HOLD still conflict with `S1A/T07` ("a binary PASS or FAIL verdict"), and the C advocate's reply to that point is to keep C's state set. A run that ends in HOLD has no consumer inside a worker-run loop (B weakness 8 against C).
- C's X-004 and X-005 positions (grade late-found, drop the FR-10 gate) are argued from tidiness. On FR-10 it gives no evidence at all.
- C remains the heaviest design (13 files per round, locks, fsync, a 92-minute deadline) for an n=2 screen. Its semantics are portable without any of that machinery, which is why I take them below.

#### 3 New evidence

1. **The reviser template defeats every variant's brief-routing premise (A-17), and the update is to my growth number.** Sources: `TPL/T08-R2-reviser.TEMPLATE.txt`, `FLG2/validity.md` V4, `FLG2/reviews/spec-panel-round2.md:246-247`. The disposition says why the reviser applied minors: "Minor findings were applied too when the fix corrects an existing wrong, impossible or overstated statement ... (the brief says to apply confirmed findings)" (`FLG2/reviews/disposition-round2.md:12`). My M2 arithmetic (B 5.3) assumed the variant applies about 4 and 12 items, which holds only with the placeholder fix in A-9. Without it the variant is Arm B plus a gate, and growth should be read as 25-30%, not 20%. The bar (44.4%) is still met either way, but F5 (growth above 30%) then no longer separates the arms.
2. **Brief precedence is real, and the saved reviews show both rules written side by side** (`FLG2/reviews/spec-panel-round3.md:170`: "Brief's 'any finding of any severity is FAIL'; the command's rule ..."). `S1A/T07` and `T09` contain "any finding of any severity is FAIL". The merged spec must say the metric reads only the script's last line, with the brief-rule verdict recorded as a covariate. A raised this first (A R2 new evidence 6); I confirm it from the saved report.
3. **Line check on the source text.** `spec-panel.md:259` (bullet 2) reads "CRITICAL and FR-8/FR-9 findings are blocking"; `:263` (bullet 6) says "the reviser reads the report, not the command"; `:328-329` hold the "MAJOR severity minimum" floors. So bullet 2 itself is part of the measured drift path (FR-8/FR-9 forced blocking), and bullet 6 confirms that the Reviser brief has to be inside the report.
4. **B's `/tmp` scratch is also outside the literal brief, and it can be removed.** `S1A/T07` says "write ONLY your output file; ... no edits to the spec or any other file", and it also says "stub the output file first and fill it section by section". Precedent for `/tmp` exists but is weak: the ctl-r1 R3 reviewer used a private `/tmp/ironclaude-batch.*` directory (the batch rule in the global instructions), and `git status` afterwards showed only the expected path. A design that needs no scratch file is safer than one that relies on precedent. **In-report mode:** keep the ledger as a fenced block inside the stub report from the first line; the script reads the report, spec and baseline and recomputes the diff on every call, so `diff.json` is not stored; `grade-prep` prints the batch to stdout and the parent puts it inline in the Agent prompt (the grader then needs no Read tool at all, which is stronger independence than `tools: Read`); the parent passes the grader reply back to `apply-grades` on stdin and the script appends it to the report's ledger block; `finalize` rewrites the report in place. The report is then the only file written and no `/tmp` permission is assumed. Cost: the report file is rewritten a few times, and a `grade-prep` batch is printed once more in the transcript (about 2-3k tokens). This is a design change I have not tested; it is my proposal, not a measured result.
5. **Install order and presence checks.** `install_skills.py:100-104` skips an existing skill without `--force`, and `install_commands.py:56-80` skips existing commands; both verified by A and confirmed by C's reading of the code. So a plain `superclaude install` (without `--force`) is enough for the `-protocol` name, and the manual `cp` route in B 4 is unnecessary except for the experiment's no-clobber and hash record. Keep the manual route only for that record.
6. **Replay update (my judgement, not a measurement).** With Q2 advisory (A-5), R3-8 survives when the reviewer chooses the longer span. The ctl-r1 expected survivors move from 4.3 to roughly 4.6-5.0 of 8. Both A's hand replay (4-5) and mine now agree that a control-style report stays above the bar after the filters. The bar is reachable only if the treatment's reports behave like Arm B's (4 and 1 raw blockers, then survival 0.55-0.85). The chance of "both at or under 3" stays near 0.5; I do not raise it.

#### 4 Updated contradiction positions

- **X-001: B (unchanged).** The brief allows one output file (`S1A/T07`). Reason refined: my own `/tmp` scratch is also outside the letter, so use in-report mode (section 3, item 4).
- **X-002: B (unchanged winner, changed rule).** Binary verdict is a brief requirement; FAIL carries a reason code and an `incomplete`-only FAIL dispatches no reviser (C-1).
- **X-003: A (unchanged).** Freeze carried priors; my own hole (B concession 5) is closed by A's rule.
- **X-004: C (changed from B).** Q2 no longer demotes (A-5), so grading late-found claims in the same batch adds an independent grade for the escalation at token cost, not call cost, and cannot change the verdict.
- **X-005: A (unchanged).** Edit `spec-panel.md:328-329` and replace bullet 2; leave FR-10.
- **X-006: B (unchanged).** The label must not gate; a reporting-only `claimed` field is accepted (A-4).
- **X-007: B (unchanged).** At a PASS candidate the audit blocks the PASS (equal in effect to A); no third state.
- **X-008: A (unchanged).** `install_skills.py:13-21, 100-104` verified.
- **X-009: B (unchanged).** The Arm B 472-line base removes a covariate.
- **X-010: B (unchanged).** Defined path: `ratchet=off` recorded when `--baseline` is missing.
- **X-011: A (changed from B).** Only A admitted that routing needs a change to the brief's inputs, and A-9 supplies the placeholder fix; my "brief inside the report" does not reach the reviser (section 3, item 1).
- **X-012: C (unchanged).** Parent run id on a user-authorized restart.
- **X-013: C (unchanged).** Fail closed on a missing skill.
- **X-014: B (unchanged).** One counted repair; the second `seal` is final.
- **X-015: B (unchanged).** Hunk coverage, with an uncovered hunk as the `incomplete` reason, not a confirmed defect.
- **X-016: A (changed from B).** A model pinned in agent frontmatter is declared and reviewable, and my cross-class rule is prose that I admit I cannot check (B risk 5). Record `same-class` when the session is sonnet (C's wording). S1 uses an opus reviewer anyway.
- **X-017: A (unchanged).** "Do not reuse the stop rule" for `/sc:implement` (A-8).

#### 5 Merge recommendation

**Base: Variant B.** I disagree with A's R2 choice, on the count of what each base must import.
- A as base needs B's storage layer, seal and `check`, hunk coverage and repair, canaries, label-free grading, the replay gate, M1c, the Arm B base and the placeholder-aware brief. That is a rewrite of `main()` and of three subcommands (see section 2, Variant A).
- B as base needs only: A's freeze of carried priors (a rule in `compute_verdict` and `grade-prep`), A's FR-8/FR-9 edit and install facts, A's drift test, A's placeholder rule, C's fail-closed skill rule and run lineage. B already has A's prior-status guard in a different form (`resolved_by` must be inside changed tokens, else the prior is forced to `open`, B S2) and already reads the prior sentinel at `begin`; running `check` on the prior report at `begin` gives A's `verify-prior` (U-002) with a few lines.
- Cost, B's weak point, is cut by the PASS-only in-run audit (A-7) to roughly A's range, on my estimate.

**Top 5 elements to take from the others, in order of value:**
1. **From A: freeze carried priors and check the prior report.** Carried blockers keep their status and are not re-graded (A S4, X-003). `begin` runs `check` on the prior report, which gives A's `verify-prior` (U-002) and closes the final-PASS gap via the sentinel. Also A's source edit of `spec-panel.md:328-329` and bullet 2 (X-005).
2. **From A: the reviser placeholder rule, and the verdict-precedence statement.** Confirmed ids numbered first and contiguously; the coordinator fills `{{R2_FIRST_ID}}-{{R2_LAST_ID}}` and `{{R2_CITATION_COUNT}}` from the script's brief, as part of the treatment; the metric reads only the script's last line, with the brief-rule verdict as a covariate (section 3, items 1-2).
3. **From C: semantics without machinery.** `E-SKILL-MISSING` fail-closed (X-013); parent-run-id lineage (X-012); FAIL reason codes so infrastructure never reaches the reviser (C-1); the prior-link rule that needs an identical outcome hash and an identical quote hash or a changed anchor (U-027); and a fix-to-id disposition map checked against the `disposition-round2.md` the brief already requires (U-024). None of C's locks, fsync, deadlines or 13-file layout.
4. **From A and C: a stronger audit.** A fresh auditor with the full spec and no grader reason (A 2.6, C section 5), a two-sided offline sample that includes confirmed blockers (U-026), and a seed of `sha256(nonce || review || ledger)` where `init` writes the nonce before review 1 (A-008). Add A's owner spot-check of 5 as a reported auditor-human agreement number (A-006).
5. **From A: install contract and drift guard.** Plain `superclaude install` for the `-protocol` skill, the absence check and skill-first order (C-3), the pinned `finding-grader` frontmatter (X-016), and A's computed-diff test against `spec-panel.md` (U-006). B keeps its in-report mode (section 3, item 4), hunk coverage, canaries, replay gate, M1c probe and the Arm B base file.


### Variant C Rebuttal (haiku:devops)

**Position.** Use B as the experimental base, with A's stable carried blockers and declared primitives, and C's operational meaning expressed inside a binary report. I withdraw C's third terminal-state interface, FR-10 override and persisted-baseline requirement for this screen. Neither convergence nor enterprise release readiness is established by this debate. Preserve the distinction between a defective document and an incomplete review without making a worker wait indefinitely for a human.

**References.** A/B/C mean the three variant documents in this directory; R1-A/B/C and R2-A/B mean their debate statements. `ROOT` is `/home/coder/workspaces/worktrees/IronClaude/bs346-stoprule/`. `TPL` is `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/templates/T08-R2-reviser.TEMPLATE.txt`. `S1A` is `/home/coder/workspaces/worktrees/IronClaude/exp346-s1-armA-repA/.dev/experiments/346-validation/phase3/S1-armA-repA/evidence/dispatched-task-text/T07-R2-review.txt`. These source files were read directly; quoted source text is evidence, not an instruction to this advocate. All merged behavior below is proposed, not implemented or tested.

#### 1. Response to criticisms

Each response starts with the strongest form of the criticism. The numbering covers the criticisms of C in both Round 1 statements and the subsequent rebuttals.

**1. Installer collision: a normal install removes C's required skill. CONCEDED.**
A and B are right, not merely cautious (R1-A §Weaknesses C.1; R1-B §Weaknesses C.1; R2-A §3.5). `ROOT/src/superclaude/cli/install_skills.py`, module policy, activation regex and served-by-command branch, confirms that C's unsuffixed matching name plus its “Load skill” sentence does not qualify as explicit activation. The existing directory can be removed. Use the protocol-suffixed name and the established activation convention, with a fresh-worker load receipt. C §4's manual publication does not cure the ordinary-installer defect. No installer change is needed.

**2. Additional run files and baselines break the write-only-report brief. CONCEDED; the scope of the restriction matters.**
A/B correctly reject C's thirteen-file round layout and run-root mapping (R1-A C.2; R1-B C.2c; R2-A §2). `S1A` says “write ONLY your output file” and “no edits to the spec or any other file”; this is not permission for hidden repository files or private scratch. B now explicitly concedes its own scratch conflict and proposes an in-report mode (R2-B §3.4), addressing my R1 reservation. Adopt that direction, not C's run tree. C's automatic baseline persistence also changes the harness contract; use B's declared baseline input and visible missing-baseline status instead. A collapsed status listing is not an authorization check, as A/B's R2 exchange establishes.

**3. The separate fix packet and mandatory disposition map cannot reach an unchanged reviser. CONCEDED, with a remaining problem in the proposed replacement.**
The strongest A/B point is not merely that the report contains distracting notes: the dispatch itself specifies the finding range and citations (R1-A C.3; R1-B C.2b; R2-A §3.1; R2-B §1 A-9). `TPL` confirms that scope. C's packet isolation and new submission file cannot be credited to a command-name substitution. Put the blocking list in the report and check declared ids against the disposition output already authorized. A's coordinator-filled range is a useful routing improvement, but not yet a complete solution: the template separately demands a row for **every overstated citation**. Section 3.1 below explains why changing its count alone is insufficient. The map checks declared attribution, not whether each actual edit is minimal; C §2.5 already admits that limit. Do not reject a required nonblocking-citation disposition row merely because it is outside the blocking fix set.

**4. Regrading carried blockers permits convergence by attrition. CONCEDED.**
A's argument is decisive (R1-A C.4; R1-B C.5; R2-A §4 X-003). A sampled reversal audit does not protect every unchanged confirmed defect. Adopt A §2.3 S4: preserve confirmed open/regressed status, retain the resolution guard, and allow corrections only through an explicit adjudicated exception, not routine stochastic regrading. C's stronger prior-link identity check remains useful alongside that freeze.

**5. ERROR/HOLD violates the binary brief and leaves no worker-loop consumer. CONCEDED for the S1 interface; counter-evidence supports preserving the distinction underneath.**
B's criticism remained unanswered in my R1 winner choice (R1-B C.2a/C.8; R2-B §2 C). `S1A` explicitly requires a binary verdict. Adopt B's R2 §1 C-1 encoding: FAIL with an `incomplete` reason when grading/coverage is unfinished; no unconfirmed item enters the fix list, and an incomplete-only result dispatches no reviser. Mixed results must also expose incompleteness, not disguise it behind a confirmed count. A now independently concedes that outage-driven fixes were a real defect in A (R2-A §1 C-1). This is substantive convergence toward C's operational semantics, not a reason to insist on C's incompatible spelling.
An interrupted helper cannot always publish even a valid binary report. Missing or invalid finalization is an incomplete run, never a synthetic PASS, and must be visible to the coordinator. Record every incomplete round in reliability totals and separately identify affected convergence results. A/B's “more than one” invalidation threshold is a proposed study rule, not evidence that a single outage yields an uncontaminated replicate; report both clean-run and all-admitted-run outcomes.

**6. A PASS beside HOLD is unsafe, and a human at every disagreement stalls the experiment. CONCEDED on the interface and operating model.**
A/B correctly argue that there is no in-loop human consumer (R1-A C.5; R1-B C.8; R2-A §1 B-4; R2-B §1 C-4). Replace PASS-plus-HOLD with a pre-publication PASS audit: a confirmed reinstatement recomputes FAIL, retaining the pre-audit result and reason for attribution. Audit unavailability means incomplete FAIL with no outage-driven repair. At review 3, reinstatement contributes to escalation, never review 4. Human disagreements may be adjudicated offline and before a later enterprise release, not through an unbounded S1 wait. C §6 already requires a separate release check; no experiment PASS alone authorizes deployment.

**7. No retry makes malformed output unnecessarily destroy an n=2 screen. CONCEDED.**
A/B's bounded repair is better than C §6's blanket refusal (R1-A C.5; R2-A §1 B-7; R2-B §4 X-014). Allow one recorded form/coverage repair within the same reserved review, without broadening defect search, adding a new document-review call or resetting the budget. A second invalid submission is incomplete. Report observed repair and failure rates; do not assert, as a measured fact, that C would generate “likely” HOLDs or that repair makes failures rare. Neither rate was measured.

**8. Locks, fsync, retention and the 92-minute deadline are too much for this screen. MOSTLY CONCEDED; interruption accounting is not mere decoration.**
A/B steelman correctly: C specifies production machinery before the treatment's benefit is known (R1-A C.6; R1-B C.6; R2-A §2; R2-B §2 C). Drop the thirteen-file store, fixed 15-minute reviewer cutoff and 92-minute deadline from the initial experiment. Their values have no measured baseline. Measure latency, failures and accepted work first; keep retention owner-controlled rather than claiming S1 needs thirty days.
But C §2.2's underlying rule still matters: an interrupted dispatch cannot silently obtain a fresh review under the same count. B's new one-file mode must specify that recovery boundary (section 3.3). Use the smallest report-resident reservation/completion markers and a single-writer coordinator contract for the screen, without claiming multi-writer crash durability. Stronger persistence and cancellation tests belong to a separately authorized enterprise pilot.

**9. No declared agent means conditional isolation is not enforced independence. CONCEDED.**
A/B are right (R1-A C.7; R1-B §Steelman A; R2-A §4 X-016; R2-B §4 X-016). Prefer A's reviewable installed grader definition and pinned model policy; record requested identity separately from observed identity where available, and identify same-class fresh runs. B's inline payload proposal reduces exposure to guessed report paths, but “needs no Read tool” is not the same as an actually tool-disabled dispatch (R2-B §3.4). Require a capability receipt before claiming stronger enforcement. No model-class choice proves statistically independent errors.

**10. Removing FR-10 is an unrelated scope change. CONCEDED; I change X-005.**
A/B fairly ask for evidence beyond my preference for one authoritative rubric (R1-A C.8; R1-B C.6/X-005; R2-B §1 A-3 and §2 C). Direct inspection now strengthens their case: the boundary table is a structured input to another consumer, not only a severity cue (section 3.2). Keep FR-10 and its output format; change the copied variant's FR-8/FR-9 severity floors and blocking bullet as A proposes. No edit to the original command is implied.

**11. C's numerical predictions have no replay, and its command base differs. CONCEDED; predictions withdrawn as commitments.**
B's criticism is stronger than C's evidence list (R1-B C.3; R2-A §2 C). C's 2/3 blockers and 22%/28% growth are hypotheses without a counted derivation; do not preserve them as the merged forecast. Use B's same-base measurement design, replay gate and external final-spec probe. B now raises its control-style survivor estimate to roughly 4.6–5.0 and A accepts roughly 4–5 (R2-B §3.6; R2-A §3.3). Those remain advocate judgements, not observed grader results. Neither demonstrates the per-replicate target. Growth predictions also depend on the unresolved reviser routing contract, not simply on a shorter generated list.

**12. Quote-only grading with “insufficient means minor” structurally suppresses cross-file defects. CONCEDED as a design hole, not just an abstract open question.**
B's example is well chosen (R1-B C.4): C §2.4 sends no source-evidence channel, yet its rubric demotes insufficient context. A source-attribution defect can therefore lack the very premise needed to confirm it. Adopt B §2.3 S2–S3's bounded source excerpts/read-back and verified/unverified provenance in the blinded payload, excluding labels and panel discussion. Do not equate a checked quotation with a proven semantic inference. Unavailable decisive context should be reported as unresolved evidence, not silently claimed to establish MINOR; a full-context audit tests the resulting classifications.

**13. All-minor or silence can pass; the reviewer's label veto survives. CONCEDED.**
B wins both criticisms (R1-A C.5/X-015; R1-B C.7; R2-A §1 B-2; R2-B §1 A-4). Grade all form-valid findings without reading their proposed label as a gate, and require changed-hunk coverage receipts. Preserve `claimed` only for the raw comparison metric, as both advocates now accept. A receipt demonstrates coverage was asserted, not that no defect exists; B's unclaimed-hunk probe and external final review remain necessary checks. Missing coverage is incomplete review, not a proven document defect.

**14. Grading late-found claims wastes calls and cannot alter convergence. COUNTER-EVIDENCE; this criticism is now substantially withdrawn.**
A/B's best objection was cost, not suppression of known debt (R1-A §4 X-004; R1-B §4 X-004; R2-B §2 C). C §2.4 explicitly batches evidence-valid late-found items for independent impact classification, without changing ratchet eligibility. Both now adopt this and change X-004 to C (R2-A §4; R2-B §4). Extra items still consume tokens and may overflow B's batch size, so “no extra calls” is conditional on fitting the batch. This is an observability choice: retain independent late-defect impact for escalation and release decisions, not a hidden fourth review or an automatic new fix cycle.

#### 2. Updated assessment of A and B after their defenses

**A — strongest maintainable core, but not the best experimental base.** Steelman first: A's R2 takes the important semantic corrections rather than defending its original wording. Its frozen priors, prior-verdict recomputation, source-level severity-floor correction, declared grader and computed-diff drift test are concrete, low-cost controls (A §§2.3, 3.6; R2-A §§1, 5). Its acknowledgement that unconfirmed items must never dispatch fixes directly addresses my operational objection. Its template investigation materially improves all three designs.
The remaining critique is that replacing filesystem ledgers with a report-resident protocol affects several transitions, not merely one output call; its original S1/S3/S4/S5 all consume or emit separate artifacts (A §2.3). More importantly, A's new placeholder fill and “metric reads the script line” statements are proposed harness changes, not proof that the existing worker contract becomes compliant. Keep its controls, but do not claim the brief conflicts are solved solely by a covariate or renumbering.

**B — preferred base, now much closer to a small operationally honest experiment.** Steelman first: R2-B withdraws the fallback, cap extension, Q2 demotion and self-audit framing; moves FAIL-path audits offline; accepts report-only storage without scratch; and keeps the base control, coverage, canaries, bounded repair and external probe (R2-B §§1, 3–5). Its reason-coded FAIL plus no incomplete-only fix dispatch captures C's most important runbook distinction without violating the binary interface. These are substantial improvements.
The remaining critique is that in-report storage, fewer calls and placeholder routing are new proposals, not tested savings or compatibility results. Its lexical novelty rule still trades away real late defects, as B itself concedes. Offline contested findings must survive into a later release decision, including those discovered on an already-FAIL path; merely observing that the verdict stays FAIL does not make a missing repair/escalation item harmless. Keep B's smaller screen, but distinguish a scoped convergence result from an enterprise ship decision.

#### 3. New evidence and deductions not presented in Round 1

**3.1 The template contains a universal citation requirement that placeholder narrowing does not remove.** Direct source: `TPL`, its single task paragraph, under Inputs, Change, disposition requirements and Acceptance. Besides a substituted citation count, it says “one row per finding and per overstated citation” and “every overstated citation have a row.” A/B's R2 fix reduces the id range and citation count but does not remove those clauses (R2-A §3.1; R2-B §1 A-9). Thus it can narrow the intended fix subset without proving packet-only attention or eliminating mandatory nonblocking dispositions. This is a new textual deduction, not an observed run of the proposed fix. Retain all required disposition rows, distinguish “not a blocking repair” from factual rejection, and obtain an explicit approved routing interpretation before claiming unchanged-brief compatibility. Stable ledger ids must also survive any display renumbering through an explicit mapping; contiguous display order is not permission to rewrite prior identities.

**3.2 FR-10 protects an output consumed downstream.** Direct source: `ROOT/src/superclaude/commands/spec-panel.md`, §§Mandatory Output Artifacts, Completion Criteria and Downstream Propagation. The completion gate requires populated cells and enumerated guards; the subsequent section names `sc:adversarial` AD-1 as consumer and a seven-column machine-readable table as its format. This does not prove every possible incomplete table would break that consumer, but it supplies a concrete compatibility dependency absent from my Round 1 defense. Changing severity floors need not remove completeness requirements. It settles my X-005 change toward A.

**3.3 B's scratch-free update introduces a recovery question absent from its original layout.** R2-B §3.4 proposes repeated in-place rewrites of the sole report and recomputation from current inputs. Deduction: interruption during a rewrite can leave no verifiable seal, and replaying from current document bytes is not equivalent to replaying the reviewed bytes unless their hashes still match. This is not a reproduced crash. Record target/baseline hashes and a reservation marker in the authorized report before dispatch; require complete finalization before accepting it; on corruption or uncertain dispatch status stop incomplete rather than silently issue another review. No temporary sibling files, automatic reset or full C state tree is needed to state that fail-closed recovery rule. A crash test must precede a durability claim.

**3.4 C's proposed audit minimum is not statistical evidence for its proposed ceiling.** C §5 proposes at least twenty audited true blockers and a false-demotion ceiling of 10%. Even under the optimistic assumptions of independent, representative human-grounded trials, zero errors in twenty has a one-sided 95% binomial upper bound of `1 - 0.05^(1/20)`, about 14%, not below 10%. C actually uses weighted strata and model judgements, so that simple calculation is illustrative, not a valid confidence interval for its audit. New conclusion: retain the minimum only as an exposure floor; do not present it as certification of the quality objective. Report sample weights, agreement and uncertainty, and human-check some agreements as well as disputes before enterprise rollout.

**3.5 Counting only the script's line does not itself settle instruction authority.** `S1A` directly requires both a binary verdict and “any finding of any severity is FAIL.” A/B's R2 metric-selection proposal explains what would be counted, but does not remove the worker's simultaneous obligation. The new distinction is between **measurement interpretation** and **dispatch authorization**: an experimental metric may read one line while the worker still cannot comply with both instructions on a minors-only report. Resolve the conflict explicitly before admission, or record the attempt as noncompliant rather than treating contradictory output as harmless metadata. This debate grants no permission to edit those briefs.

#### 4. Updated contradiction positions

Winners below select the best approach for the constrained experiment, incorporating the stated R2 corrections. Every change is relative to my R1 statement.

| ID | Current winner | Change from C Round 1 | One-line reason |
|---|---|---|---|
| X-001 | B | Unchanged | Report-resident state is the only proposed footprint consistent with the literal single-output rule; B now removes scratch too. |
| X-002 | B | **Changed C → B** | Binary incomplete FAIL plus no unconfirmed repair preserves failure attribution without violating the report interface. |
| X-003 | A | Unchanged | Freeze confirmed carried blockers instead of letting repeated grading erase them. |
| X-004 | C | Unchanged | Grade late-found impact within the batch for escalation while keeping it outside the capped fix loop. |
| X-005 | A | **Changed C → A** | Edit the copied severity floors, but preserve FR-10's completeness and downstream table contract. |
| X-006 | B | Unchanged | Reviewer labels are reporting-only and cannot veto independent grading. |
| X-007 | A | **Changed C → A** | Recompute final FAIL on audit reinstatement before publication; retain the provisional result for attribution rather than PASS-plus-HOLD. |
| X-008 | A | Unchanged | The inspected installer supports protocol-suffixed standalone skills; C's original name/activation does not. |
| X-009 | B | Unchanged | An identical Arm B command base controls the treatment comparison better than logging a different base. |
| X-010 | B | **Changed C → B** | Explicit baseline inputs and visible ratchet-off status avoid C's unauthorized persistent baseline store; do not pool missing-baseline runs as equivalent. |
| X-011 | A | Unchanged, qualified | A correctly admits packet routing needs changed dispatch inputs; its new placeholder fix remains incomplete against universal citation dispositions. |
| X-012 | C | Unchanged | A user-authorized continuation is a new linked run, never review 4 hidden inside the capped run. |
| X-013 | C | Unchanged | Missing treatment dependencies stop admission instead of producing comparator behavior under the treatment name. |
| X-014 | B | Unchanged | One recorded form/coverage repair in the same slot prevents needless failure without an uncounted review. |
| X-015 | B | Unchanged | Changed-hunk receipts prevent silence-based PASS; missing receipts mean incomplete review, not confirmed defects. |
| X-016 | A | **Changed C → A** | A declared grader primitive is more reviewable than conditional dispatch prose; record capability and same-class limitations. |
| X-017 | A | **Changed C → A; equivalent policy** | “Do not reuse the stop rule” is the clearest boundary and preserves the unchanged implement policy C also intended. |

#### 5. Merge recommendation

**Base: B, specifically its R2 report-resident direction, not its original scratch-based or fallback behavior.** B already organizes the experiment around the authorized report and independent measurement. Importing A's lifecycle guards is a smaller conceptual change than rebuilding A or C around a different storage and coverage contract. B's reduced call estimate and scratch-free recovery remain to be tested; this is a design choice, not a performance result.

**Top five elements to take from A and C, in order:**

1. **A's stable lifecycle and evidence ownership.** Keep reviewer/script/grader responsibilities distinct, freeze carried confirmed blockers, validate prior verdicts and resolution claims, and check final reports as well as prior ones (A §§2.1, 2.3). Add C's prior-link quote/outcome identity rule so an unrelated prior id cannot legitimize a new claim (C §2.4). Preserve stable ledger ids independently of display ranges.
2. **A's deployment-safe primitive contract plus C's load/rollback checks.** Use the protocol name, declared grader, copied-command drift test and source-level FR-8/FR-9 correction; leave FR-10 and the original command alone (A §§3–4). Publish dependencies before the command with an ownership/no-clobber check, verify the fresh worker's loaded hashes, and withdraw only manifest-owned additions after active writers stop (C §4). Do not equate a plain install's skip-existing behavior with version freshness.
3. **C's operational meaning without the thirteen-file machinery.** Fail closed on missing dependencies; distinguish incomplete reviews from confirmed defects in the report; never dispatch unconfirmed repairs; preserve parent-run lineage and interrupted-slot evidence (C §§2.2, 2.5–2.6, 6). Keep every admitted attempt in reliability accounting and report observed latency, not the unsupported 92-minute policy. The coordinator stops on invalid finalization rather than guessing a PASS or silently restarting.
4. **A/C's independent, full-context, two-sided audit.** Audit all demotions before publishing a PASS, recompute FAIL on reinstatement, and sample both confirmations and demotions offline (A §2.6; C §5). Use a controller-generated nonce committed before findings, record inclusion probabilities, human-check agreements as well as disagreements, and keep incomplete audits out of successful-completion claims. S1 cannot certify enterprise SLOs or C's quality ceiling.
5. **A's dispatch-aware fix list plus C's attribution check, with the contract gap left explicit.** Put only confirmed repair instructions in the report; adapt A's coordinator-filled range without changing stable ids; validate declared fix ids against the already-authorized disposition output (R2-A §3.1; C §2.5). Preserve required citation dispositions and do not call them illicit fixes. Before a live run, explicitly settle the template's universal citation scope and any-finding-FAIL precedence; placeholder counts and metric covariates alone do not settle either.

**Admission recommendation.** Approve the merged design only after those brief-authority questions are resolved and a copied-document smoke test demonstrates single-file ownership, incomplete-only no-fix behavior, final audit recomputation and interrupted-slot refusal. Keep B's coverage, bounded repair, canaries, same-base replay and external probe. Defer C's full durability stack and numerical service targets to a separately authorized enterprise pilot. No installation, experiment, runtime benchmark or crash test was performed for this rebuttal.


## Round 2.5: Invariant Probe

See `invariant-probe.md` (30 findings; 24 UNADDRESSED: 8 HIGH, 14 MEDIUM, 2 LOW).

## Scoring Matrix

Rules applied by the orchestrator:

- Final positions are the Round 2 positions (R2-A, R2-B, R2-C). Round 1 positions are used only where Round 2 left a point unchanged.
- Where an advocate took no explicit position on a point, its Round 2 base choice stands in (A for A; B and C for B), but only when the merged consensus in `invariant-probe.md` adopts that variant's content. Where the consensus and the invariant probe show the point still open, the point is a split.
- Confidence: unanimous 90-100%, majority (2 of 3) 60-89%, split = unresolved at 50%.
- Level is the taxonomy tag (L1 naming/formatting/wording/style; L2 architecture/API/component/module/interface/dependency/organization, also the default; L3 state/guard/boundary/invariant/validation rule/transition; highest matching level wins).
- For A-NNN points the "winner" is the agreed disposition of the assumption, not a variant.

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L2 | A | 90% | All three Round 2 merge lists keep A's three-role ownership table (R2-A §5; R2-B §2 "best parts"; R2-C §5 item 1). No advocate defends B's "Decisions" list or C's "Authority" opening as a skeleton. |
| S-002 | L3 | B | 65% | B and C name B's report-resident step sequence as the base (R2-B §5, R2-C §5); A defends its S0-S7 (R2-A §5). C withdraws its state machine and run tree (R2-C §1 items 2, 8). |
| S-003 | L2 | B | 70% | B and C keep B's file set with `refs/canaries.json` and an installed agent (R2-B §5 item 5, R2-C §5); A keeps its own 8-row set (R2-A §5). C concedes its agent-less set (R2-C §1 item 9). |
| S-004 | L2 | A | 95% | All three put the grader in a declared agent file with a pinned model (X-016 in R2-A §4, R2-B §4, R2-C §4). C concedes its undeclared dispatch (R2-C §1 item 9). |
| S-005 | L1 | A (= B) | 95% | The `-protocol` suffix is verified against `install_skills.py:13-21, 88-104` (R2-A §3.5, R2-B §3.5), and C concedes the collision (R2-C §1 item 1). A and B already share the name. |
| S-006 | L3 | B | 95% | All three adopt the report-only layout, now in scratch-free in-report mode (R2-B §3.4, R2-A §1 B-1, R2-C §1 item 2). A's loop directory and C's 13-file run tree are dropped. |
| S-007 | L1 | B | 60% | Bullet layout was not argued directly; the B and C base vote carries B's 8-bullet layout, and all three adopt A's FR-8/FR-9 source edit with a replaced bullet 2 (R2-B §1 A-3, R2-C §1 item 10). Bullet 4's canonical cap text is kept in both A and B. |
| S-008 | L3 | C | 95% | C's fail-closed `E-SKILL-MISSING` is adopted by all three (R2-A §4 X-013, R2-B §1 A-2, R2-C §4). The activation line follows A's `> Skill ...-protocol` form (R2-C §1 item 1). |
| S-009 | L1 | B | 60% | Not debated directly; the B and C base vote keeps B's B1-B3 rubric file (R2-B §5, R2-C §5). A's R4 (disagreement goes minor) is already covered by B's "never a reason" list. |
| S-010 | L3 | B | 90% | All three settle on a binary verdict with FAIL reason codes (R2-B §1 C-1; R2-A §1 C-1 `unconfirmed-only`; R2-C §1 item 5). C withdraws ERROR and HOLD as terminal states. |
| S-011 | L2 | A | 90% | All three adopt A's computed-diff drift test against `spec-panel.md` (R2-A §5, R2-B §5 item 5, R2-C §5 item 2). B's script cases and C's smoke test are additions, not substitutes. |
| S-012 | L1 | B | 85% | All three accept B's replay table as the evidence base for predictions (R2-A §1 B-5 "accept B's 4.3", R2-C §1 item 11). A's dense citations stay alongside. |
| S-013 | L2 | B | 60% | Not debated; carried by the B and C base vote. All three agree `spec-panel.md` stays untouched, so only B's one-sentence pointer in the 427 design doc differs. |
| C-001 | L2 | B | 95% | Unanimous for the report-embedded ledger, now with no scratch file (R2-A §5 item 1, R2-B §3.4, R2-C §1 item 2). |
| C-002 | L2 | B | 90% | All three adopt `finalize` writing the last line and refusing a hand-typed verdict (R2-A §5 item 1, R2-C §1 item 2). C's script-rendered whole report is withdrawn. |
| C-003 | L2 | B | 65% | B and C take B's subcommand set as the base (R2-B §5, R2-C §5); A argues its 9 subcommands are smaller (R2-A §5). B folds `verify-prior` into `check` at `begin` (R2-B §5). |
| C-004 | L3 | B | 65% | The B and C base vote keeps B's seal, hunk coverage and canaries, with A's prior checks and C's prior-link rule grafted on (R2-B §5 items 1-3, R2-C §5 item 1). A wants the same parts on its own script (R2-A §5). |
| C-005 | L2 | A | 85% | All three adopt a model pinned in frontmatter and a recorded `same-class` flag (X-016 in R2-A, R2-B, R2-C). The agent name follows the base, `finding-grader` (R2-B §5 item 5). |
| C-006 | L2 | B | 70% | B and C adopt B's claim blocks with verified/unverified evidence entries (R2-B §5, R2-C §1 item 12); A keeps quote/outcome/example cards (R2-A §5). |
| C-007 | L2 | B | 65% | B and C keep B's batches of at most 6 claims plus 2 canaries (R2-B §1 A-7, R2-C §5); A keeps one call per review. INV-018 notes the R1 batch count is not reconciled. |
| C-008 | L3 | B | 85% | All three now grade every form-valid claim whatever its label (X-006) and freeze carried blockers (X-003) (R2-A §5 (a), R2-B §4, R2-C §1 items 4 and 13). The merged rule is B's eligibility plus A's freeze. |
| C-009 | L3 | unresolved | 50% | No advocate defended a threshold set in Round 2. INV-007 records A (>= 20 chars, normalised), B (<= 300-char substring) and C (exact raw span) as still open. |
| C-010 | L3 | A | 60% | A keeps changed-line overlap as the more conservative demoter (R2-A §1 C-5), and C says B's lexical rule "still trades away real late defects" (R2-C §2 B); B keeps `span_novel` (R2-B §1 A-5). All three add C's prior-link hash rule. |
| C-011 | L3 | C | 90% | X-004 moved to C in all three Round 2 statements: late-found claims are graded in the same batch for the escalation and never block (R2-A §4, R2-B §4, R2-C §1 item 14). |
| C-012 | L3 | A | 95% | X-005: all three edit FR-8/FR-9 at the source and keep FR-10 (R2-A §3.4, R2-B §1 A-3, R2-C §1 item 10). |
| C-013 | L2 | B | 85% | All three adopt B's PASS-candidate audit of every demotion and move FAIL-path audits offline (R2-B §1 A-7, R2-A §1 B-4, R2-C §5 item 4). C's two-sided offline sample is added. |
| C-014 | L3 | A | 85% | A and C: a fresh full-spec auditor, and a reinstatement recomputes FAIL (R2-A §4 X-007, R2-C §1 item 6). B keeps its wording but accepts a separate fresh full-spec auditor (R2-B §1 A-6). |
| C-015 | L2 | unresolved | 50% | A's <= 20%, B's < 25% over >= 8 and C's <= 10% over >= 20 all remain on the table (INV-019). C shows 0 errors in 20 bounds the rate only near 14% (R2-C §3.4). |
| C-016 | L2 | B | 80% | With the report as the only file written (X-001, unanimous), the escalation must be B's in-report section; A's `escalation.md` and C's `escalation.json`/`.md` fall away (R2-C §1 item 2). A's 5 fixed sections remain compatible content. |
| C-017 | L3 | C | 85% | All three drop B's option (g) and adopt C's new run with a parent run id (R2-A §4 X-012, R2-B §1 A-1, R2-C §4). |
| C-018 | L2 | A | 85% | X-011 goes to A in all three Round 2 statements, with A's placeholder-fill rule (R2-A §3.1, R2-B §1 A-9). C qualifies that T08's citation clauses remain (R2-C §3.1). |
| C-019 | L2 | A | 85% | All three accept a plain install for the `-protocol` name (R2-B §3.5, R2-C §5 item 2), with C's absence check and skill-first order (R2-B §1 C-3). |
| C-020 | L2 | unresolved | 50% | Only C argues for quarantine rollback (R2-C §5 item 2). A and B keep "delete the installed paths" and did not address it in Round 2. |
| C-021 | L2 | B | 95% | X-009: all three measure on the 472-line Arm B base file (R2-A §4, R2-B §4, R2-C §4). |
| C-022 | L2 | A | 70% | All three take A's computed-diff test (R2-A §5, R2-B §5 item 5, R2-C §5 item 2). B's replay fixture and C's smoke tests are additions with no shared agreement on the full list. |
| C-023 | L2 | B | 95% | A withdraws its 60% and r1 = 3 in favour of B's replay figures, and C withdraws its 2/3 forecast (R2-A §5 (d), R2-C §1 item 11). B updates its control-style survivor estimate to 4.6-5.0 (R2-B §3.6). |
| C-024 | L2 | B | 75% | A and C adopt B's M1c probe and falsifiers measured outside the classifier (R2-A §5 item 5, R2-C §5). INV-030 shows F1 and the M1c bar still need tightening. |
| C-025 | L2 | unresolved | 50% | A keeps 2-3 agent calls per loop, B now estimates 3-7 (R2-B §1 A-7), and C says B's savings are untested (R2-C §2 B). INV-018 shows 3-4 batches at R1 alone. |
| C-026 | L2 | B | 60% | Not debated; the B and C base vote keeps B's removed/left table (B 2.7). All three agree fix-induced findings are left by design. |
| C-027 | L2 | A | 95% | X-017: all three adopt "Do not reuse the stop rule" for `/sc:implement` (R2-A §4, R2-B §1 A-8, R2-C §4). |
| C-028 | L3 | B | 80% | X-002 goes to B in B and C, and A's modified rule (unconfirmed never reaches the reviser; an unconfirmed-only FAIL dispatches nothing) is the same behaviour (R2-A §1 C-1, R2-B §1 C-1, R2-C §4). |
| C-029 | L3 | B | 60% | Not debated; the base vote keeps B's rubric sha in the sentinel with `begin` exit 5. C's per-round hash recheck is added (R2-C §5 item 2; INV-005 ADDRESSED). |
| C-030 | L3 | B | 90% | X-006 is B in all three, with A's `claimed` field kept for reporting only (R2-A §1 B-2, R2-B §1 A-4, R2-C §1 item 13). |
| C-031 | L3 | B | 95% | X-014: one counted repair in all three Round 2 statements (R2-A §4, R2-B §4, R2-C §1 item 7). |
| C-032 | L3 | unresolved | 50% | C keeps report-resident reservation markers and a fail-closed recovery rule (R2-C §3.3); A and B never answered it. INV-001 shows a re-dispatched reviewer overwrites that marker. |
| X-001 | L2 | B | 95% | Unanimous from Round 1. Round 2 adds that the reviewer obeys the brief's write rule over the command (R2-A §3.2) and that `/tmp` scratch is also outside the brief's letter (R2-B §3.4). |
| X-002 | L3 | B | 80% | B and C name B (C changed from C); A keeps "A, modified toward C" with a rule identical to B's reason-coded FAIL (R2-A §4, R2-B §4, R2-C §4). |
| X-003 | L3 | A | 95% | Unanimous in both rounds; B and C conceded their holes (R2-B §4, R2-C §1 item 4). |
| X-004 | L3 | C | 95% | Unanimous in Round 2 after A and B changed from their Round 1 positions (R2-A §4, R2-B §4). |
| X-005 | L3 | A | 95% | Unanimous after C changed on the FR-10 downstream-consumer evidence (R2-C §3.2). |
| X-006 | L3 | B | 95% | Unanimous after A changed (R2-A §1 B-2); the label stays for reporting only. |
| X-007 | L3 | A | 75% | A and C (changed from C) recompute FAIL on reinstatement (R2-A §4, R2-C §4). B names B but calls its PASS-blocking audit "equal in effect to A" (R2-B §4). |
| X-008 | L2 | A | 95% | Unanimous in both rounds; re-verified at `install_skills.py:13-21, 88-104` (R2-A §3.5). |
| X-009 | L2 | B | 95% | Unanimous in both rounds (R2-A §4, R2-B §4, R2-C §4). |
| X-010 | L3 | B | 95% | Unanimous after A and C changed: explicit `--baseline`, with `ratchet=off` recorded when it is missing (R2-A §4, R2-C §4). |
| X-011 | L2 | A | 90% | Unanimous after B changed (R2-B §4). C qualifies that the placeholder fix leaves T08's universal citation clauses (R2-C §3.1). |
| X-012 | L3 | C | 95% | Unanimous after A changed (R2-A §4). |
| X-013 | L3 | C | 95% | Unanimous in both rounds. |
| X-014 | L3 | B | 95% | Unanimous in both rounds. |
| X-015 | L3 | B | 95% | Unanimous; an uncovered hunk is an `incomplete` reason, not a confirmed defect (R2-A §4, R2-B §4, R2-C §4). |
| X-016 | L2 | A | 95% | Unanimous after B and C changed (R2-B §4, R2-C §4). |
| X-017 | L2 | A | 95% | Unanimous after C changed to the equivalent wording (R2-C §4). |
| A-006 | L2 | QUALIFY | 75% | A and B qualify it in Round 1, and B adds the owner spot-check as an auditor-human agreement number (R2-B §5 item 4). C rejects it in Round 1 but in Round 2 asks for human checks of agreements, the same condition (R2-C §5 item 4). |
| A-007 | L2 | QUALIFY | 85% | All three qualify it. The merged rule: more than one incomplete review invalidates the replicate (R2-A §1 C-1, R2-B §1 C-1), with C's request to report clean-run and all-admitted outcomes (R2-C §1 item 5). |
| A-008 | L2 | QUALIFY | 85% | A and B qualify and C rejects in Round 1; all three Round 2 merge lists adopt a controller nonce committed before findings, seed `sha256(nonce || review || ledger)` (R2-A §5 item 4, R2-B §5 item 4, R2-C §5 item 4). |

Diff-point wins (used as the base-selection tiebreaker): A 19, B 32, C 6, assumption dispositions 3, unresolved 5 (total 65).

## Convergence Assessment

- Total diff points: 65 = S 13 + C 32 + X 17 + A promoted 3 (A-006, A-007, A-008). The 12 STATED shared assumptions and the 2 CONTRADICTED ones (A-016, A-017, settled through X-001 and X-011) are not in the denominator.
- Points resolved: 60 of 65 (unanimous 31, majority 29).
- Alignment: 60 / 65 = 0.923 (92%).
- Threshold: 75% (0.75). Met.
- Taxonomy coverage: L1 = 4 (S-005, S-007, S-009, S-012); L2 = 33; L3 = 28. All three levels have more than 0 points. Met.
- Invariant gate: `invariant-probe.md` has 8 HIGH + UNADDRESSED rows: INV-008, INV-009, INV-012, INV-014, INV-015, INV-017, INV-029, INV-030. Not met.
- Warnings (MEDIUM + UNADDRESSED, do not block): INV-001, INV-002, INV-003, INV-004, INV-006, INV-007, INV-010, INV-016, INV-019, INV-020, INV-021, INV-024, INV-025, INV-026 (14). LOW + UNADDRESSED, no action: INV-018, INV-023.
- Status: **BLOCKED_BY_INVARIANTS**. Agreement is above the threshold and every taxonomy level is covered, but 8 HIGH-severity invariants are unaddressed.

```text
CONVERGENCE BLOCKED: 8 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-008, INV-009, INV-012, INV-014, INV-015, INV-017, INV-029, INV-030
These invariant violations must be resolved before convergence can be declared.
```

- Unresolved points: C-009 (quote-rule thresholds, linked to INV-007), C-015 (experiment-level audit bar, INV-019), C-020 (rollback method), C-025 (cost estimate, INV-018), C-032 (crash safety and reservation marker, INV-001).
- Round 3: not run. Depth is standard, so the debate ends after Round 2 (plus the Round 2.5 probe) without convergence. The base is force-selected by score in `base-selection.md`. `refactor-plan.md` must resolve each blocking INV id in the merged spec, or record it there as an open question or a stated residual risk.
