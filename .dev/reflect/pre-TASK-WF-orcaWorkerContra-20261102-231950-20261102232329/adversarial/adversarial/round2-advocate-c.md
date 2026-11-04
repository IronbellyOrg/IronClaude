# Round 2 Rebuttal: Variant C (reviewer 3, refactorer)

Cite keys as in earlier rounds: `A:N`, `B:N`, `C:N` = card line; `TL:N` = plan line; `SRC:N` = `source.md` line; `qa:N`, `retry:N`, `mw:N`, `SKILL:N` = the installed `~/.claude/skills/sc-implement-protocol/` files (`refs/qa.md`, `refs/retry.md`, `refs/managed-workspace.md`, `SKILL.md`); `R1-A:N`, `R1-B:N`, `R1-C:N`, `R2-A:N`, `R2-B:N` = debate statement lines. Every TL, SRC and executor line below was opened for this statement (TL:14-116, SRC:55-90, SRC:289-292, SRC:394-397, qa:10-65, qa:186, qa:240-256, qa:284-310, retry:38-46, retry:72, retry:107, mw:34-38, SKILL:40, :79, :97, :160).

## Position summary

The verdict stays FAIL with **exactly one blocking finding: Task 7**. I **concede R3-F3 to should-fix**, top tier. My Round 1 case for raising it (R1-C:23, :69) rested on TL:21 being file-wide. Testing A's narrower reading against the literal text, TL:21 itself, not only its cite, supports a compliant reading: its first clause orders the file to restate spec text, and its "instead of copying them" names the dispatch preamble as the thing not copied. The guard line comes from the spec, not the preamble. Under the blocking test all three advocates now share (a finding is blocking only when no reading the plan's text supports is compliant), R3-F3 does not qualify. I confirm the Task 7 consensus and adopt B's correction of its basis: the irreducible clash is "Then ... run it" against "Make the commit the last action" (TL:110), with the commit-ID point as supporting evidence only.

## 1. Responses to criticisms of Variant C

| Criticism (source) | Response |
|---|---|
| R3-F3 is over-graded; a compliant reading exists that the plan points to four times (R2-A:36, :42; R2-B:60) | **Conceded.** See section 2. I add a fifth pointer the others did not use: TL:21's own wording. |
| R3-F3's list of Orca syntax is too broad; only the guard line cannot be paraphrased (R2-A:34-35; R2-B:57) | **Conceded.** `task-create --spec`, `--retry-of` (SRC:74), `worker-start --worktree new-child --base-branch` (SRC:84) and `orca worktree rm` (SRC:88) have no verbatim AC; Task 2 asks for the rules "in full" (TL:49), not the words. Only TL:52's "exact guard line text" pins `send worker_done --outcome failed` (SRC:86). One addition: the pin is double, because Task 5's test must assert that the template "carries the guard line" (TL:87), so the verbatim text is also fixed by a test. |
| R3-F1's "the acceptance criterion cannot pass" is overstated (C:285; R2-B:41) | **Conceded in Round 1 (R1-C:49), and I now go further with B.** TL:113 itself can only be met by a record written after the commit, so it invites the reading that the record step is not "the last action". The commit-ID point alone would be should-fix. The blocking basis is the install-versus-commit order (section 3). |
| R3-F9 "four `guard refused:` texts" is wrong (R2-A:79) | **Conceded in Round 1 (R1-C:50).** SRC:60 gives three exact texts (case 1, case 2, copies-disagree) and case 3 has no text. Merge A's three-plus-prefix wording, with B's R2-5 phrase list. |
| R3-F2 blocking was wrong (C:285) | **Conceded in Round 1 (R1-C:48).** Should-fix, top tier, with no "vacuous" fallback (now agreed by A, R2-A:20, and B, R2-B:18). |
| R3-F4's dependency half, R3-F6 class, R3-F12 class | **Conceded in Round 1 (R1-C:51-53).** R3-F4 keeps only the path list and the `--only` pathspec point (U-008). R3-F6 is drift. R3-F12 is class none. |
| A-008 graded should-fix by C (R1-C:81); A and B grade it minor (R2-A:94; R2-B:92) | **Conceded to minor.** mw:36 binds the executor itself to "`.dev/tasks/` is always staged", and staging is not committing (TL:22). The gap is only that no AC records the final `git add` after Tasks 8 and 9, so it is a minor recording gap, folded into the closing phase-report task. |

## 2. R3-F3 tested against the literal text: conceded to should-fix

**The lines.**
- TL:21 (Constraints): "`WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 already say; it adds no rule the spec lacks, and for Orca verb syntax and heartbeat cadence it points to the dispatch preamble instead of copying them (section 2.1, "Contract file")."
- TL:42 (Task 1 AC): "no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both."
- TL:49 (Task 2): section 2.3 "in full", including "the brief layout with the exact guard line"; a brief template "that carries the guard line".
- TL:52 (Task 2 AC): "including the exact guard line text from section 2.3 'Brief layout'".
- TL:54 (Task 2 AC): "The file mentions Orca commands only as the coordinator's and worker session's channel".
- SRC:59: the no-copy rule is scoped "For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats)", and the file holds "WC-6 and section 2.3, including its brief template and the template's guard line".
- SRC:86: the guard line ends "send worker_done --outcome failed with a body starting "guard refused:"."

**Testing A's narrower reading.**
1. TL:42 is not breached by the guard line. Its qualifier "copied from Orca's guides" excludes spec text. Agreed with A and B.
2. TL:21 has no such qualifier, which was my Round 1 point (R1-C:23). But reading the sentence literally, end to end, it does not ban spec-sourced syntax either. Its first clause *requires* the file to restate what sections 2.1-2.3 say, and SRC:86 is section 2.3 text. Its second clause says the file "points to the dispatch preamble instead of copying them": the thing not copied is the preamble's own syntax. The guard line is not copied from the preamble. So the compliant reading sits in TL:21's own words, not only in its cite to SRC:59. That is a fifth pointer, beside the four A and B list (TL:21's cite, TL:38, TL:42, TL:54).
3. A literal-minded reviewer can still quote "for Orca verb syntax ... it points to the dispatch preamble instead of copying them" against a file that contains `worker_done --outcome failed`. The B4 Read-back only checks that the quote is byte-present (qa:61), and severity is derived mechanically from the reviewer's yes/no answer (qa:37, :56). So the risk is real. But it needs the reviewer to read "copying" as "containing", against the sentence's own first clause.

**Why that is should-fix under the shared test.** The test all three advocates now use (R2-A:91, R2-B:89, and my R1-C:75) makes a finding blocking only when every reading the plan's text supports forces a breach. Here a supported compliant reading exists, and it is the more natural one. Task 7 is different: no reading of TL:110 lets both the install-after-commit order and "commit last" hold.

**What I keep from Round 1.** The late risk is real and is the reason to fix before the run, not to grade higher. A blocker on task-owned text is never capped (qa:186), and the managed FINAL is never waived (SKILL:160) and returns `issues` when "a plan `## Constraints` item is violated" (qa:310). If a literal FINAL confirms it, the archive stops with `E-ARCHIVE-BLOCKED` (qa:286) after the commit, the install and the live runs. The plan is hash-pinned once Task 1 starts (SKILL:40), so the fix cannot be made mid-run.

**Correction to A's and B's mitigation.** Both say that at Task 2 the adviser's `dispute` route "stops the run for a Ruling before any commit or install" (R2-A:43, R2-B:61). That is right, but it is still a stop: a `dispute` naming the AC appends `halt reason=dispute` and STOPs `E-HALT-QA` (retry:72, :107). It is a safer stop than Task 7's, not a non-event. This does not change the grade.

**Fix (A's, accepted).** Scope TL:21 as SRC:59 does ("for the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it points to the dispatch preamble for Orca verb syntax and cadence instead of copying them"), and add to TL:52 "copied verbatim from `./source.md` section 2.3 'Brief layout', including its `worker_done` text". Class: drift; the spec is consistent here and TL:21 widened it.

## 3. Task 7: blocking consensus confirmed, merged form

**Confirmed: blocking.** I opened TL:106-116 again. TL:110 orders: approval 1, then "stage ... and commit with `git commit --only -- <paths>`"; "Then ask the owner to approve `uv run superclaude install --force` ...; on approval, run it"; "If either approval is refused, stop this task and report"; "Make the commit the last action of the task." Both the install and the commit are actions under any reading, so "Then ... run it" and "commit last" cannot both hold. A reviewer can quote either sentence against either order and pass the B4 Read-back (qa:52, :61). Under qa:41 a confirmed B4 is blocking.

**On the basis, I side with B (R2-B:9, :41).** The commit-ID point (TL:113) is supporting, not the core, because TL:113 can only be met by a record written after the commit, which invites "the commit is the last product action". The install-versus-commit order is the clash no reading removes. My Round 1 wording (R1-C:25) led with the commit ID; I move the weight to the order clash.

**Consequence, verified.** The commit moves HEAD inside Task 7's window. When A2 fails, ladder check 3 fails ("HEAD has not moved", retry:41), the executor appends `halt review=2 reason=head-moved` and STOPs `E-HALT-QA`, and "no adviser is spawned" (retry:44). So the `dispute` route (retry:72) is closed on this task. The halt lands after the owner-approved commit and possibly after the `--force` overwrite of `~/.claude/CLAUDE.md` (TL:25). The refusal sentence is not an executor outcome either: "No other path may stop automation or prompt the user" (qa:288).

**Merged form (A F3 + C R3-F1, with B's additions).** Rewrite TL:110 in one order:
1. Ask both approvals up front, stating the `--force` effect.
2. Run the install.
3. Write `t7-approvals.md` with both questions, the answers verbatim and the install output.
4. Stage the listed P0 paths plus `.dev/tasks` (never `.claude/` mirrors), check AC-C4, then commit with `git commit --only -- <paths> .dev/tasks`, so `.dev/tasks` is named in the pathspec (U-008, R3-F4). This is the last product action.
5. Append the commit ID to `t7-approvals.md` and stage it; say in the task that this record step follows the commit on purpose.
6. List the P0 paths in the task text (R3-F4 and B's addition): `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/cli/install_core.py`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `tests/skills/test_worker_contract.py`, any plugin copy Task 3 adds, and `.dev/tasks`.
7. Replace "stop this task and report" with: a refusal is recorded in `t7-approvals.md` and the task ends in a halt for the person's Ruling; a QA failure after the commit is never retried.

Class: drift for the wording; the commit itself is a necessary deviation (SRC:282).

## 4. Updated assessment and new evidence

**Blocking set: 1 (Task 7).** My Round 1 count of 2 (R1-C:75, "and, as a candidate, R3-F3") is withdrawn.

**Top should-fix items, all to be applied before the run because of the hash pin (SKILL:40):**
1. Cadence run (R3-F2 / R2-1 / F4a): Task 8's AC requires at least one checked run whose top-level session, outside Agent-tool calls, lasts longer than the preamble cadence, with start and end times; if none is achieved, P0 does not pass. SRC:291 forbids the vacuous fallback.
2. R3-F3: scope TL:21 and pin the guard line to SRC:86 (section 2).
3. X-004: three exact refusal texts plus the case-3 prefix, with a spec erratum note (A's F2).

**Minor items C still owns, unchanged:** R3-F5 (red `tests/cli` window between Task 1 and Task 3), R3-F6 (Task 4 runs too few test files), R3-F7 (stale phase-state line in HOW-WE-WORK.md), R3-F8 (unsafe negative checks), R3-F10 (`--report-dir` in the P0 template), R3-F11 (closing phase-report task, now also carrying B's AC-C5 record and the final `git add .dev/tasks`), R3-F13 (`gh api` post patterns), R3-F14 (AC-0.6 fallback).

**New evidence this round:**
1. TL:21's own first clause ("restates only what ... sections 2.1, 2.2 and 2.3 already say") and its object "instead of copying them" (the preamble) give the compliant reading inside the Constraint itself. This is why I concede R3-F3.
2. TL:87 makes Task 5's test assert that the template carries the guard line, so the verbatim `worker_done --outcome failed` text is pinned twice (TL:52 and TL:87). The fix to TL:21 must therefore scope the rule; it cannot be met by paraphrasing.
3. Severity is mechanical: the parent derives it from the reviewer's yes/no answers and a byte-presence Read-back (qa:37, :56, :61). The plan's readiness therefore depends on whether a reasonable reviewer can say yes with no compliant reading available. That is the line between Task 7 and R3-F3.
4. The Task 2 `dispute` route is itself a STOP `E-HALT-QA` (retry:107), so it is a safer halt, not an absence of one.
5. mw:36 puts the always-staged rule on the executor, which is why A-008 drops to minor.

## 5. Shared assumptions

- **A-002 (the executor follows Depends-on edges): REJECT. Unchanged.** SKILL:79 ignores `depends-on`; SKILL:97 runs unmarked tasks in source order; no task is marked `independent`.
- **A-003 (one undefined "blocking" means FAIL): QUALIFY. Converged.** I accept the shared test (R2-A:91 with B's irreversible-effect clause, R2-B:89). Blocking = following the plan as written, in source order under `/sc:implement`, leaves no compliant choice under any reading the plan's text supports: an unmet AC (B1), a breach of a Constraint or explicit task instruction (B4, qa:52), an unguarded irreversible or outward effect, or a P0 pass condition no task performs (SRC:241). When a compliant reading exists and the plan points to it, should-fix. One blocking finding means FAIL. Result: Task 7 only.
- **A-005 (the run is attended): QUALIFY. Unchanged in substance, now shared.** Approvals need a person (TL:25, TL:110), and the person-opened implement session is the coordinator (TL:26). But "stop this task and report" is not an executor outcome (qa:288). Fix: one Constraint line that the run must be attended and never headless, plus the Task 7 refusal line. On B's point (R2-B:83) that a strict reading of qa:288 would cover Task 7's own approval questions: I read qa:288 as closing the list of halts, not banning questions a task's own AC requires, but the attended-run line removes the doubt.
- **A-007 (the spec is a consistent authority): REJECT the assumption. Unchanged,** with A's boundary: SRC:60 against SRC:306 (three texts against "four") and the stale `install_core.py:13-24` range in SRC:59 are spec defects. R3-F3 is not one: SRC:59 is consistent and TL:21 widened it.
- **A-008 (post-commit artifacts need no staging): QUALIFY. Changed from REJECT.** mw:36 binds the executor to stage `.dev/tasks`, and staging is not committing (TL:22). Add one recorded `git add .dev/tasks` at the end of the closing phase-report task. Minor. U-008 stays inside the Task 7 finding.

## 6. Contested points

| Point | Current preferred variant or merged position | Confidence |
|---|---|---|
| S-006 / A-003 (blocking count) | Merged: exactly 1 blocking finding (Task 7), under the shared test. C's Round 1 count of 2 withdrawn. | 0.85 |
| X-005 / U-002 / U-006 (Task 7) | A + C merged, **blocking**. Basis: the install-versus-commit order clash in TL:110 (B4, qa:52), per B; the commit ID is supporting. Consequence: `head-moved` halt with no adviser (retry:41, :44). Fix: the seven-step order in section 3, with the path list and `.dev/tasks` in the `--only` pathspec. Drift for the wording, necessary for the commit. | 0.85 |
| U-007 / R3-F3 (verb syntax) | C's finding with A's narrower reading. **Should-fix (top)**, drift. Only the guard line is unavoidable (SRC:86, pinned by TL:52 and TL:87). Fix: scope TL:21 as SRC:59 does. | 0.80 |
| C-002 / X-002 / X-003 (cadence run) | Should-fix (top), C's wording: a run longer than the cadence outside Agent-tool calls; no vacuous fallback; if none, P0 does not pass. | 0.90 |
| X-004 (exact refusal texts) | A: three exact texts plus the case-3 prefix, with a spec erratum note. | 0.90 |
| C-004 (phase-end checks) | One closing phase-report task (R3-F11 / A's F7) re-running AC-C1, AC-C2 and the AC-C3 comparison, recording AC-C5 with an empty edit set (R2-3), ending with a recorded `git add .dev/tasks`. Minor. | 0.80 |
| C-001 / X-001 (Task 3 dependency) | Minor, drift; residual is R3-F5's red window. | 0.90 |
| X-006 (classes) | Task 3: drift. AC-0.9: drift. Stale cite: none. Task 7: drift for wording, necessary for the commit. R3-F3: drift. | 0.80 |
| A-005 | QUALIFY: attended-run Constraint line plus the Task 7 refusal line (qa:288). | 0.80 |
| A-008 | QUALIFY (moved from REJECT): one recorded closing staging line, minor (mw:36). | 0.75 |
| A-002 / A-007 | REJECT the assumption in both cases. | 0.90 |
