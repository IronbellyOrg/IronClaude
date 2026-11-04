# Round 2 Rebuttal: Variant A (reviewer 1, analyzer)

Cite keys as in Round 1: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `qa:N`, `retry:N`, `mw:N`, `SKILL:N` = the installed `~/.claude/skills/sc-implement-protocol/` files (`refs/qa.md`, `refs/retry.md`, `refs/managed-workspace.md`, `SKILL.md`); `R1-A:N`, `R1-B:N`, `R1-C:N` = Round 1 statement lines. Every TL, SRC and executor line below was opened for this statement.

## Position summary

The verdict stays FAIL, with **one blocking finding: Task 7** (my F3 merged with C's R3-F1). B's "0 blocking" uses a test that is narrower than the executor's own: the executor treats a breach of an explicit task instruction as a blocker on the same footing as an unmet AC (qa:45-52), and Task 7's instructions cannot all be met in any order. C's R3-F3 is a **real conflict but not blocking**: the exact guard line that Task 2 must copy does contain Orca syntax, but the plan points to a reading under which every instruction holds, and a halt on Task 2 lands before anything irreversible and with the adviser's dispute route still open. It is the top should-fix item, next to the cadence run. I correct one Round 1 claim of my own (U-007) and accept C's point that "record as vacuous" cannot satisfy the cadence duty.

## 1. Responses to criticisms of Variant A

| Criticism (source) | Response |
|---|---|
| F1 blocking/regression rests on the wrong executor model (R1-B:27, R1-C:13, :37) | **Conceded in Round 1, unchanged.** SKILL:79 ignores `depends-on`; SKILL:97 runs unmarked tasks in source order. F1 becomes C's R3-F5 (red window Task 1 to Task 3, no AC observes it): minor, drift. |
| F6 class `none` is wrong (R1-B:28, R1-C:38) | **Conceded.** TL:97 uses a class that is empty at P0. Drift. |
| F8(a) is weak (R1-B:29, R1-C:39) | **Conceded.** "at any depth setting" is WC-13 text (SRC:81), and D5 orders the trace before a depth raise, not before live runs. F8(b) and F8(c) stand as minor. |
| A treats "commit last" as a followable mitigation (R1-C:40; A:60-61) | **Conceded in Round 1** (R1-A:44). Section 3 below goes further: the instruction cannot be met in any order. |
| A misses the TL:21/TL:42 versus TL:49 clash (R1-C:40) | **Conceded as a coverage gap, and I correct my own Round 1 reasoning.** At R1-A:68 I said an executor "can restate section 2.3's rules while pointing to the preamble for verb syntax". That is wrong for one item: TL:52 requires "the exact guard line text from section 2.3", and that line contains `worker_done --outcome failed` (SRC:86). The executor cannot paraphrase it away. See section 2 for the grade. |
| A relies on the executor assumption "with only a hedge" (R1-B:20) | **Conceded.** The hedge at A:16-17 named the right question; the executor rules answered it against me. |
| U-002 (head-moved) is only a "safe halt", so minor (R1-B:56) | **Partly conceded.** B is right that the halt harms nothing: the revert refuses before any change (retry:333-334), and no adviser runs (retry:44). But "safe" is not the test for plan readiness. The halt arrives *after* the owner-approved commit and the `--force` overwrite of `~/.claude`, and it can only be cleared by a person's Ruling. Section 3 shows the halt is the expected outcome of an attentive review, not a remote risk. U-002 stays part of the blocking Task 7 finding, as its consequence rather than its cause. |
| My C-002 merged fix added B's "or record vacuous and flag" (R1-A:56); C says SRC:291 forbids it (R1-C:17, :62) | **Conceded to C.** SRC:291 says a short run "passes the heartbeat part vacuously, so each phase report names at least one checked run that lasted longer than the cadence". A vacuous record is exactly what the sentence exists to prevent. Merged fix: Task 8's AC requires at least one checked run whose top-level session, outside Agent-tool calls, lasts longer than the cadence; if none is achieved, the report records the duty as unmet and P0 does not pass. |

## 2. Ruling on R3-F3 (Task 2 versus the no-verb-syntax rule)

**The text.**
- TL:21 (Constraints): "for Orca verb syntax and heartbeat cadence it points to the dispatch preamble instead of copying them (section 2.1, "Contract file")". As worded, it covers the whole file.
- TL:42 (Task 1 AC): "no `orca orchestration` verb syntax **copied from Orca's guides** and no fixed heartbeat cadence".
- TL:49 and TL:52 (Task 2): section 2.3 "in full", and the AC demands "the exact guard line text from section 2.3 'Brief layout'".
- SRC:86, the guard line: "... on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:"."
- SRC:59 limits the no-copy rule to "the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats)", and in the same sentence puts "the template's guard line" in the file.
- TL:54 (Task 2 AC): "The file mentions Orca commands only as the coordinator's and worker session's channel, which `./source.md` SA-2 permits for this file."

**Is the conflict real? Yes, but narrower than C says.**
1. TL:42 is not breached. Its qualifier "copied from Orca's guides" excludes text copied from the spec, and the guard line comes from SRC:86.
2. Most of the Orca syntax C lists can be paraphrased, because no AC asks for it verbatim: `worker-start --worktree new-child --base-branch` (SRC:84), `orca worktree rm` (SRC:88), `--retry-of` and `task-create --spec` (SRC:74).
3. One item cannot be paraphrased: the guard line's `worker_done --outcome failed`, which TL:52 requires byte for byte. If TL:21 is read literally, as covering the whole file, no executor choice satisfies both TL:21 and TL:52.
4. If TL:21 is read with its own cite, the conflict disappears. The plan points to that reading in four places: TL:21 cites section 2.1 "Contract file" (SRC:59, scoped to worker-session duties, and the guard line is explicitly included); TL:38 scopes "pointing to the dispatch preamble" to the worker-session duties; TL:42 restricts the AC to syntax "copied from Orca's guides"; and TL:54 anticipates Orca commands in this file.

So the plan widened a scoped spec rule in one Constraint sentence. This is a plan defect, not one inherited from the spec (SRC:59 is consistent here). Class: drift.

**Is it blocking under the executor's QA rules? No. It is the top should-fix item.**
- What makes it more than cosmetic: the Read-back for `quoted-constraint-breach` only checks that the quote is byte-present in the Constraints (qa:61). It does not weigh the reading. A Task 2 reviewer who reads TL:21 literally can raise a confirmed blocker. So can the managed FINAL, which returns `issues` when "a plan `## Constraints` item is violated" (qa:310). The fixer then cannot meet TL:52 and the literal TL:21 together.
- Why it is still not blocking under the test I proposed (R1-A:68; section 5, A-003): a compliant path exists, and it is the reading the plan's own text points to four times. The executor is not forced to breach anything. A halt needs a reviewer to adopt a reading the plan contradicts.
- Why the consequence is lighter than Task 7's: Task 2 does not move HEAD, so a failed A2 reaches the adviser, whose `dispute` outcome covers "the AC is contradictory or infeasible" (retry:72). That stops the run for a Ruling (retry:107) before any commit or install has happened. On Task 7 the ladder is off (retry:41, :44).
- One-line fix, which must be made before the run because the plan is hash-pinned once the first task starts (SKILL:40): scope TL:21 as SRC:59 does ("for the worker-session duties ... it points to the dispatch preamble"), and add to TL:52 "copied verbatim from SRC:86, including its `worker_done` text".

## 3. Ruling on B's "0 blocking" claim for Task 7

**No order of Task 7's steps meets every instruction and every AC.** These are the instructions, all in TL:110 unless noted:

- (i) On approval, stage and commit with `git commit --only -- <paths>`.
- (ii) "**Then** ask the owner to approve `uv run superclaude install --force` ...; on approval, run it."
- (iii) "Make the commit the last action of the task."
- (iv) TL:113: `t7-approvals.md` records "both questions, the owner's answers verbatim, **the commit ID** and the install output".
- (v) TL:25 (Constraints): commits need the owner's approval at the moment of action.

| Order | What breaks |
|---|---|
| A. As written: commit, then install, then write `t7-approvals.md` | (iii): the install and the file write both come after the commit. |
| B. Install first, then commit last, writing the file before the commit | (iv): the file cannot hold the ID of a commit that does not exist yet. (ii): the install comes before the commit, against "Then". |
| C. Install, commit, then write the file with the ID (B's reading, R1-B:30) | (iii): the file write is an action after the commit. (ii): "Then". |
| D. Commit, install, write the file, then commit again so a commit is last | (v): the second commit was never approved by the owner. And it is not "the commit" of (iii). |

The core is self-referential. No file can hold the ID of a commit and also be written before that commit. So (iii) and (iv) cannot both hold under any reading in which writing the evidence file counts as an action. B's 0-blocking result needs two loosenings that the plan never invites: "action" must exclude a file write, and "Then" in (ii) must be read as "after the commit approval" rather than "after the commit".

**Why this is blocking under the executor's rules, and why B's test is too narrow.** B's test counts only (a) an AC that cannot pass or (b) an unguarded irreversible effect (R1-B:65). The executor has four co-equal blocking triggers, and one of them is a breach of "an explicit task instruction" that the reviewer can quote (qa:52; also qa:17). "Make the commit the last action of the task" is such an instruction. Its quote passes the Read-back (qa:61). The evidence file that TL:113 requires proves the breach by itself: the commit ID in it shows it was written after the commit. So following the plan as written hands an attentive reviewer a confirmable B4 blocker that no fix pass can close. After the commit, a failed A2 halts `head-moved` with no adviser (retry:41, :44). The run therefore ends in `E-HALT-QA` on the task that has already committed and overwritten `~/.claude/CLAUDE.md` (TL:25). That is the plan not being ready to run, even though the halt itself is safe.

**What I concede to B.** TL:113 on its own can pass (C's calibrator, C:285, and R1-C:49 agree). The halt causes no damage. A Ruling can clear it. My blocking call rests on instruction conflict plus the stage at which the halt arrives, not on harm.

**Merged fix.** Rewrite TL:110 in one order: ask both approvals; run the install; write `t7-approvals.md` without the ID; stage the listed P0 paths plus `.dev/tasks`; commit as the last product action, naming `.dev/tasks` in the `--only` pathspec (U-008); then append the commit ID to `t7-approvals.md` and stage it, and say explicitly that this record step follows the commit. Add one line: a QA failure after the commit, or an owner refusal, ends the task in a halt for the person's Ruling and is never retried. Class: drift for the wording. The commit itself is a necessary deviation (SRC:282).

## 4. Updated assessment of the other variants and new evidence

**Variant B.** R2-1 is the right gap with the wrong grade, as B now admits (R1-B:40-41). Two problems remain in Round 1. First, B's "0 blocking" test drops the executor's B4 trigger (section 3). Second, B keeps "record the clause as vacuous" as a fallback (R1-B:17), which SRC:291 rules out. B's staging point (A-008) and its R2-5 phrase list are sound and belong in the merge.

**Variant C.** C is the strongest card on internal consistency. Its two new Round 1 points both hold up:
- R3-F3 is real, though over-graded (section 2).
- A-005 is better than my own Round 1 answer. qa:288 closes the list of interrupts ("No other path may stop automation or prompt the user"), so TL:110's "stop this task and report" is not an executor outcome. If the commit is refused, TL:113 is unmet, which gives a B1 blocker. The ladder can then run and ask the owner again, or the adviser disputes. If the commit is made and the install is refused, the task halts `head-moved`. This strengthens the Task 7 finding.

C's R3-F9 "four texts" remains wrong, and C conceded it (R1-C:50).

**New evidence this round:**
1. SRC:86's guard line contains `worker_done --outcome failed`, and TL:52 requires it verbatim. That is the one unavoidable point of the R3-F3 conflict.
2. SRC:59 explicitly places "the template's guard line" in the contract file. So the spec is consistent, and the plan's TL:21 is the sentence that widened the rule.
3. TL:54 already anticipates Orca commands in the file, which supports the scoped reading.
4. The adviser's dispute route exists for Task 2 (retry:72, :107) but is skipped for Task 7, where a head-moved halt comes first with no adviser (retry:44). The same kind of defect therefore has different consequences on the two tasks.
5. The self-referential commit ID (section 3) makes the Task 7 conflict a logical one, not only a matter of wording.

## 5. Shared assumptions

- **A-002 (the executor follows Depends-on edges): REJECT. Unchanged.** SKILL:79, SKILL:97, and nothing in the plan is marked `independent`.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY. Sharpened.** A plan finding is blocking when following the plan as written, in source order under `/sc:implement`, leaves the executor no compliant choice. That is the case when every reading of the plan's own words forces either an unmet AC (B1) or a breach of a Constraint or explicit task instruction (B4), the executor's own blocking triggers (qa:41, :49, :52), or leaves a P0 pass condition with no task that performs it (SRC:241). When a compliant reading exists and the plan's own text points to it, the finding is should-fix, even if a literal-minded reviewer could still confirm a blocker. One blocking finding means FAIL. Result: Task 7 is blocking. R3-F3, C-002, F1/R3-F5, F2 and U-008 are should-fix.
- **A-005 (the run is attended): QUALIFY. Changed in substance, adopting C's point.** Attendance is needed, and a person-opened implement session is the coordinator TL:122 asks for (SKILL:118). But a refusal does not produce the clean "stop and report" that TL:110 promises. Under qa:288 it becomes a B1 blocker on TL:113, which leads to a retry or dispute, or to `head-moved` after the commit. Fix: add one Constraint line saying the run must be attended and never headless. Task 7 should record a refusal in `t7-approvals.md` and expect a halt for a Ruling, not a retry. Folded into the Task 7 finding.
- **A-007 (the spec is a consistent authority): REJECT the assumption. Unchanged,** with one boundary. SRC:60 against SRC:306 (three exact texts against "four") and the stale SRC:59 range are spec defects the plan inherits. R3-F3 is not one of them: there the spec is consistent (SRC:59), and the plan's TL:21 caused the conflict.
- **A-008 (post-commit artifacts need no staging): QUALIFY. Slightly changed.** The executor already applies the always-staged rule (mw:36), and staging is not committing (TL:22). So artifacts left uncommitted after Task 7 are expected. I now accept B's and C's fix as one closing line in the phase-report task (`git add .dev/tasks` after Tasks 8 and 9, recorded), graded minor, not a separate should-fix. U-008 (`--only` must name `.dev/tasks`) stays should-fix inside the Task 7 finding.

## 6. Contested points

| Point | Current preferred variant or merged position | Confidence |
|---|---|---|
| S-006 / A-003 (blocking count) | Merged: exactly 1 blocking finding (Task 7). Against B's 0, because B's test drops the executor's B4 trigger (qa:52). Against C's 2, because R3-F3 has a compliant reading that the plan points to. | 0.80 |
| X-005 / U-002 / U-006 (Task 7) | A + C merged, **blocking**, drift for the wording and necessary for the commit. The fix is the reordered TL:110 in section 3, plus U-008 and the refusal line. | 0.85 |
| U-007 / R3-F3 (verb syntax) | C's finding, graded **should-fix (top)**, drift. The only unavoidable point is the guard line (SRC:86, TL:52). Fix: scope TL:21 as SRC:59 does. | 0.75 |
| C-002 / X-002 / X-003 (cadence run) | Should-fix (top), with C's wording. Require a run longer than the cadence outside Agent-tool calls; no "vacuous" fallback (concession to C). | 0.85 |
| C-001 / X-001 (Task 3 dependency) | B and C: minor, drift. The residual is R3-F5. | 0.90 |
| X-004 (number of exact refusal texts) | A: three exact texts plus the case-3 prefix, and a spec erratum note. | 0.90 |
| X-006 (classes) | Task 3: drift. AC-0.9: drift. Stale cite: none. Task 7: drift for the wording, necessary for the commit. R3-F3: drift. | 0.80 |
| A-005 | QUALIFY, adopting C's refusal-path point (qa:288). Folded into Task 7. | 0.75 |
| A-008 | QUALIFY. One closing staging line in the phase-report task, minor. | 0.70 |
| A-002 / A-007 | REJECT the assumption in both cases. Unchanged. | 0.90 |
