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
