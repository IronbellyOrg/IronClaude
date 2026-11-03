# Round 2 Rebuttal: Variant B (reviewer 2, qa)

Cite keys as in earlier rounds: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `qa:N`, `retry:N`, `SKILL:N` = the installed `~/.claude/skills/sc-implement-protocol/` files (`refs/qa.md`, `refs/retry.md`, `SKILL.md`); `R1-A:N`, `R1-B:N`, `R1-C:N`, `R2-A:N` = debate statement lines. Every TL, SRC and executor line below was opened for this statement.

## Position summary

I move from 0 blocking to **1 blocking: Task 7**. A is right that my Round 1 test was narrower than the executor's own. The executor treats a breach of an explicit task instruction (B4) as blocking on the same footing as an unmet AC (qa:41, and the B4 row at qa:52). Task 7's body order and its "commit last" sentence cannot both be followed, whatever the executor does. I do not move on R3-F3: it is a real conflict, but the plan gives a compliant reading and points to it, so it is should-fix, at the top of the list with the cadence run. I accept A's narrower reading of R3-F3: the guard line is the only text that cannot be paraphrased. I also withdraw my "record the heartbeat clause as vacuous" fallback.

One correction to A's Task 7 argument: the commit-ID problem on its own would not make Task 7 blocking, because TL:113 itself points to writing the record after the commit. The clash that cannot be removed is between "Then ask ... run it" (the install after the commit) and "Make the commit the last action". Both the install and the commit are actions under any reading.

## 1. Responses to criticisms of Variant B

| Criticism (source) | Response |
|---|---|
| X-003: B grades R2-2 minor because TL:122 delegates step 5, then grades R2-1 blocking although it sits in the same delegated step (R1-A:31, R1-C:41, diff X-003) | **Conceded, as in Round 1 (R1-B:40).** Both clauses are in SRC:291, and the same TL:122 sentence ("steps 1-3 and 5-7") brings both in. Under the merged test in section 5 both are should-fix. R2-1 ranks above R2-2 because it applies on every run, while R2-2 applies only if AC-0.6 answers no. That is a difference in priority, not in grade. |
| R2-1 is "unsatisfiable after the fact" (B:22-23; R1-A:13) | **Conceded.** SRC:291 asks for one checked run longer than the cadence. Another run can be added within the phase. |
| B's Tier-2 troubleshoot suggestion would not count (R1-A:32, R1-C:17) | **Conceded.** SRC:291 excludes time "while the session is inside an Agent-tool call", and Tier 2 is Agent-tool fan-out. The fix must ask for a run whose top-level session, outside Agent-tool calls, lasts longer than the cadence. |
| B's "or record the clause as vacuous and flag it" fallback is ruled out by SRC:291 (R1-C:17, R2-A:20, R2-A:73) | **Conceded now.** I kept this fallback in Round 1 (R1-B:17). That was wrong. SRC:291 reads "A run shorter than the cadence passes the heartbeat part vacuously, **so** each phase report names at least one checked run that lasted longer than the cadence." The duty exists to stop a vacuous pass. I adopt A's merged wording (R2-A:20): Task 8's AC requires at least one such run; if none is achieved, the report records the duty as unmet and P0 does not pass. |
| R2-4's dependency half and U-005 rest on a dependency-driven executor (R1-A:33, R1-C:42) | **Conceded, as in Round 1 (R1-B:43).** SKILL:79 ignores `depends-on`; SKILL:97 runs unmarked tasks in source order. What remains of R2-4 is the phase-end re-run of AC-C1 and AC-C2 (SRC:241). |
| R2-3 cites TL:17 for text at TL:20 (R1-A:34, R1-C:44) | **Conceded.** Cite error only; the finding stands. |
| B omits whole areas: negative-check targets, AC-0.9 class, Task 7 mechanics, `--report-dir` (R1-C:43) | **Conceded, as in Round 1 (R1-B:45).** B's coverage was the narrowest of the three cards. |
| B's 0-blocking test drops the executor's B4 trigger (R2-A:65, R2-A:73) | **Conceded.** My Round 1 test counted only (a) an AC that cannot pass and (b) an unguarded irreversible effect (R1-B:65). The executor's severity model has four co-equal blocking answers. `quoted-constraint-breach` is "yes" when the diff breaks "a parent `## Constraints` ... item or an explicit task instruction" and the reviewer can quote that text (qa:52). Its Read-back only checks that the quote is byte-present (qa:61). A plan that forces the executor to break a quotable task instruction hands any attentive reviewer a confirmed blocker. I adopt A's test and keep my irreversible-effect clause as one more trigger (section 5). |
| B's "0 blocking" needed two loosenings the plan never invites (R2-A:63) | **Half conceded.** See section 2. The "Then" loosening cannot be supported, and that alone makes Task 7 blocking. The other loosening, that writing the record file after the commit is not "an action", is invited by the plan's own AC (TL:113), so I do not accept that half of A's argument. |

What I keep from Round 1, which A and C did not dispute: R2-5's phrase list for the ID-only rules (R2-A:73 accepts it), R2-3 as the smallest correct AC-C5 fix, R2-6 class `none` (C conceded, R1-C:52), the L3 staging point behind A-008 (R2-A:94 now accepts the fix), and the phase-end re-run half of R2-4.

## 2. Ruling on A's Task 7 argument

I opened TL:106-116. The instructions in TL:110 and the AC at TL:113:

- (i) Ask approval 1; "on approval, stage ... and commit with `git commit --only -- <paths>`".
- (ii) "**Then** ask the owner to approve `uv run superclaude install --force` ...; on approval, run it."
- (iii) "If either approval is refused, stop this task and report that the live checks cannot run."
- (iv) "Make the commit the last action of the task."
- (v) TL:113: `t7-approvals.md` records "both questions, the owner's answers verbatim, the commit ID and the install output".

**Does any order meet every instruction and AC? No.**

The clash that no reading removes is (ii) against (iv). The body puts the commit at approval 1 and the install after it ("Then ... run it"). The last sentence puts the commit after everything. The install and the commit are both actions under any meaning of the word. So either the install comes after the commit, which breaks (iv), or the commit comes after the install, which breaks the order that (i) and (ii) set. My Round 1 reading (R1-B:30, :56) needed "Then" to mean "after asking approval 1", not "after the commit". The sentence puts "Then" directly after the commit clause, so that reading is strained. A reviewer can quote either sentence against either order, and the quote passes the Read-back (qa:61).

The commit-ID clash, (iv) against (v), is weaker than A says (R2-A:63). It is true that no file can hold the ID of a commit and also be written before it. But TL:113 is the plan's own AC, and it can only be met by writing the record after the commit. So the plan itself points to the reading "the commit is the last *product* action; the record is written after it". Under A's own should-fix rule ("a compliant reading exists and the plan's own text points to it", R2-A:91), this half alone would be should-fix. It does not change the verdict, because the (ii)/(iv) clash stands without it.

**Do I concede it is blocking under the executor's real QA rules? Yes.**
- A B4 answer is a blocking trigger, the same as B1 (qa:41, qa:52).
- Following Task 7 as written forces a breach of a quotable explicit task instruction, so no executor choice is compliant.
- The consequence lands at the worst point. Task 7's commit moves HEAD. When A2 fails and HEAD has moved, the executor writes `halt review=2 reason=head-moved` and stops, and "no adviser is spawned" (retry:41, retry:44). So the adviser's `dispute` route (retry:72, retry:107) is not available. The run halts for a person's Ruling after the owner-approved commit, and possibly after the `--force` overwrite of `~/.claude/CLAUDE.md` (TL:25).
- A and C are also right that (iii) is not an executor outcome. The closed interrupt list ends "No other path may stop automation or prompt the user" (qa:288). A refusal becomes an unmet TL:113 (B1), not a clean stop.

My Round 1 point still holds as a limit on harm, not on grade: the halt damages nothing, and a Ruling can clear it. But a plan that is certain to hand its executor a confirmable blocker on the irreversible task is not ready to run.

**Merged fix (A's order, with one addition from me).** Rewrite TL:110 as one order: ask both approvals up front, stating the `--force` effect; run the install; write `t7-approvals.md` without the ID; stage the listed P0 paths plus `.dev/tasks`; commit with `--only`, naming `.dev/tasks` in the pathspec (U-008); then append the commit ID to `t7-approvals.md` and stage it, and say in the task text that this record step follows the commit on purpose. Replace (iii) with: a refusal is recorded in `t7-approvals.md`, and the task ends in a halt for the person's Ruling, never a retry. Add: a QA failure after the commit is never retried. My addition: list the P0 paths in the task text (the Task 1-6 outputs, `install_core.py`, any plugin copies), so the `--only` pathspec can be checked. Class: drift for the wording; the commit itself is a necessary deviation (SRC:282).

## 3. Ruling on C's R3-F3 and A's narrower reading

**The text.** TL:21 says the contract file, "for Orca verb syntax and heartbeat cadence ... points to the dispatch preamble instead of copying them (section 2.1, "Contract file")". TL:42 bans verb syntax "copied from Orca's guides". TL:52 requires "the exact guard line text from section 2.3 'Brief layout'". The guard line (SRC:86) contains "send worker_done --outcome failed with a body starting "guard refused:"". SRC:59 limits the never-copy rule to "the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats)", and the same sentence puts "the template's guard line" in the file. TL:54 expects Orca commands in the file "as the coordinator's and worker session's channel".

**A's narrower reading is correct.** In Round 1 I called R3-F3 "overstated" and minor (R1-B:32). I was right that TL:42's qualifier protects text taken from the spec. I missed that TL:21 has no such qualifier and is a Constraints item, which every review and the managed FINAL check (qa:16, qa:310). Most of the syntax C lists can be paraphrased, because no AC asks for it word for word (SRC:74, SRC:84, SRC:88). The guard line cannot be paraphrased, because TL:52 demands it exactly. So a literal reading of TL:21 makes TL:21 and TL:52 impossible to meet together.

**Grade: should-fix, top tier. Not blocking.** Three reasons:
1. A compliant reading exists, and the plan points to it four times: TL:21 cites SRC:59, which is scoped to worker-session duties and includes the guard line; TL:38 scopes "pointing to the dispatch preamble" to those duties; TL:42 limits the ban to text "copied from Orca's guides"; TL:54 expects Orca commands in the file. A careful reviewer answers B4 "no". This is the opposite of Task 7, where the plan's own sentences point to two incompatible orders.
2. If a literal reviewer does confirm it at Task 2, HEAD has not moved. The ladder runs, and the adviser can return `dispute` because "the AC is contradictory or infeasible" (retry:72). That stops the run for a Ruling before any commit or install (retry:107).
3. The one late risk is C's: the managed FINAL is never waived, and it returns `issues` when "a plan `## Constraints` item is violated" (qa:310; SKILL:160). A literal FINAL could block the archive after the live runs. That is why R3-F3 must be fixed before the run, because the plan is hash-pinned once the first task starts (SKILL:40). It is not a reason to grade it blocking, because the FINAL applies the same severity test (qa:294) and needs the same contradicted reading.

New supporting point: the guard line is text that Task 2 adds, so it is task-owned, and "a blocker on task-owned text is never capped" (qa:186). The inherited cap (qa:41, qa:166) gives no protection here. That is one more reason to fix it before the run.

Fix (A's, which I accept): scope TL:21 as SRC:59 does ("for the worker-session duties ... it points to the dispatch preamble"), and add to TL:52 "copied verbatim from SRC:86, including its `worker_done` text". Class: drift. The spec is consistent here; the plan's TL:21 widened the rule.

## 4. Updated assessment and new evidence

**Blocking set: 1 (Task 7).** Not 0, because my Round 1 test dropped B4 (section 1). Not 2, because R3-F3 has a compliant reading that the plan points to (section 3).

**Top should-fix items, to be applied before the run because of the hash pin (SKILL:40):**
1. Cadence run (R2-1 / R3-F2 / F4a): C's wording, outside Agent-tool calls, no vacuous fallback; if no such run is achieved, P0 does not pass.
2. R3-F3: scope TL:21 and pin the guard line to SRC:86.
3. U-008 and the refusal line, folded into the Task 7 fix.
4. X-004: three exact refusal texts plus the case-3 prefix (A's F2), with a spec erratum note.

**Minor items B still owns:** R2-2 (carry the fallback into Task 8's step 5), R2-3 (record AC-C5 as run with an empty edit set), the phase-end half of R2-4 (re-run AC-C1, AC-C2 and the AC-C3 comparison at phase end; C's R3-F8 scratch-skill risk makes this more needed), R2-5 (name the load-bearing phrases for WC-3, WC-5, WC-7 and WC-9), R2-6 (stale cite, class none).

**New evidence this round:**
1. TL:113 can only be met by a record written after the commit. So the plan itself invites the "the record step is not an action" reading. Task 7's blocking basis is the install-versus-commit order clash in TL:110, not the self-referential commit ID.
2. qa:186: task-owned text is never capped. The guard line Task 2 adds gets no inherited-cap protection, either at Task 2's review or at the FINAL.
3. qa:274-276: the closed interrupt list sits in the QA chapter and covers finding-driven stops ("The only non-finding interrupts are the STOP rows"). Read strictly, "No other path may stop automation or prompt the user" (qa:288) would also cover Task 7's own approval questions. I read it as covering halts, not task actions that the spec requires (SRC:282). The text does not say so explicitly, which is one more reason for an explicit attended-run Constraint line (A-005).
4. retry:44 confirms the asymmetry A states: on Task 7 the ladder-off halt comes before any adviser, so the `dispute` route (retry:72) exists for Task 2 but not for Task 7.

## 5. Shared assumptions

- **A-002 (the executor follows Depends-on edges): REJECT. Unchanged.** SKILL:79 and SKILL:97; nothing in the plan is marked `independent`.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY. Changed.** I adopt A's sharpened test (R2-A:91), with one clause added from my Round 1 test. A plan finding is blocking when following the plan as written, in source order under `/sc:implement`, leaves no compliant choice. That is the case when every reading the plan's own text supports forces (a) an unmet AC (B1), (b) a breach of a Constraint or explicit task instruction (B4, qa:52), (c) an irreversible or outward effect with no guard, or (d) a P0 pass condition that no task performs (SRC:241). When a compliant reading exists and the plan's text points to it, the finding is should-fix. One blocking finding means FAIL. Result: Task 7 is blocking; R3-F3, the cadence run, F1/R3-F5, F2 and U-008 are should-fix.
- **A-005 (the run is attended): QUALIFY. Changed in substance, adopting C's point.** The approvals need a person present (TL:25, TL:110). TL:110's "stop this task and report" is not an executor outcome (qa:288). Fix: one Constraint line saying the run must be attended and never headless, plus the Task 7 refusal line from section 2. Folded into the Task 7 finding.
- **A-007 (the spec is a consistent authority): REJECT the assumption. Unchanged,** with A's boundary. SRC:60 against SRC:306 (three exact texts against "four") and the stale SRC:59 range are spec defects the plan inherits. R3-F3 is not one of them: SRC:59 is consistent, and TL:21 caused the conflict.
- **A-008 (post-commit artifacts need no staging): QUALIFY. Unchanged.** The executor already stages `.dev/tasks` as a package rule, and staging is not committing (TL:22). Add one closing `git add .dev/tasks` line, recorded, after Tasks 8 and 9 (SRC:396, L3). Minor. U-008 stays inside the Task 7 finding.

## 6. Contested points

| Point | Current preferred variant or merged position | Confidence |
|---|---|---|
| S-006 / A-003 (blocking count) | Merged: exactly 1 blocking finding (Task 7), under A's test plus my irreversible-effect clause. B's Round 1 count of 0 is withdrawn. | 0.85 |
| X-005 / U-002 / U-006 (Task 7) | A + C merged, **blocking**. Basis: the install-versus-commit order clash in TL:110 (B4, qa:52), plus the `head-moved` halt with no adviser (retry:41, :44). The commit-ID point alone is should-fix, since TL:113 invites it. Fix: A's reordered TL:110, U-008, the refusal line and an explicit path list. | 0.85 |
| U-007 / R3-F3 (verb syntax) | C's finding with A's narrower reading. **Should-fix (top)**, drift. The only unavoidable point is the guard line (SRC:86, TL:52). Fix: scope TL:21 as SRC:59 does. | 0.80 |
| C-002 / X-002 / X-003 (cadence run) | Should-fix (top), C's wording: a run longer than the cadence outside Agent-tool calls; no vacuous fallback (my concession). | 0.90 |
| C-003 (AC-0.6 fallback) | Minor, drift (all agree). | 0.90 |
| C-004 (phase-end checks) | Merged: one closing phase-report task (A's F7 / C's R3-F11) that re-runs AC-C1, AC-C2 and the AC-C3 comparison, records AC-C5 as vacuous (R2-3), and ends with `git add .dev/tasks` (A-008). Minor. | 0.80 |
| C-007 (rule substance in the test) | B's R2-5 phrase list, with A's three-texts correction in place of C's "four". Minor. | 0.80 |
| C-001 / X-001 (Task 3 dependency) | B and C: minor, drift; the residual is R3-F5. | 0.90 |
| X-004 (number of exact refusal texts) | A: three exact texts plus the case-3 prefix, and a spec erratum note. | 0.90 |
| X-006 (classes) | Task 3: drift. AC-0.9: drift. Stale cite: none. Task 7: drift for the wording, necessary for the commit. R3-F3: drift. | 0.80 |
| A-005 | QUALIFY, adopting C's qa:288 point: an attended-run Constraint line plus the Task 7 refusal line. | 0.75 |
| A-008 | QUALIFY. One closing staging line, minor. | 0.75 |
| A-002 / A-007 | REJECT the assumption in both cases. | 0.90 |
