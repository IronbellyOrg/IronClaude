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
