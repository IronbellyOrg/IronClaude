# Recommendation: D2, who may give a Ruling when /sc:implement halts inside an Orca worker

Status: COMPLETE (2026-11-02). Independent citation check run; its findings are fixed (section 7). Source of the position: `.dev/orca-command-refactor/decisions/D2/debate/adversarial/merged-output.md` (cited `MO:N`). Debate artifacts in the same folder: `debate-transcript.md` (`DT:N`), `invariant-probe.md`, `base-selection.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`.
Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. Paths are repo-relative unless absolute. `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `QA`, `LEDGER`, `RETRY`, `SKILL` = `src/superclaude/skills/sc-implement-protocol/{refs/qa.md,refs/ledger.md,refs/retry.md,SKILL.md}`; `CR-01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`.

## 1. Recommended option, and agreement with the spec
**Recommended: (a) plus (c).** Keep the `/sc:implement` Ruling rule word for word. Only the person gives a Ruling. They choose one of two routes:
- (a) is the default and the only route for a `dispute` halt. The person resumes the plan in their own session.
- (c) is the way back into Orca. The person types the Ruling line into the ledger themselves, and the coordinator starts a resume Task once a read-only check passes.

The coordinator never relays a Ruling, so (b) is rejected (`MO:8-11`). (c) is an extra route the debate added; it is not one of the spec's two listed options (`SPEC:335-336`).

**Agreement with the spec: agrees, and extends it.** The spec recommends (a) "because the rule exists to stop an agent approving its own work" (`SPEC:337`). The debate keeps that rule and that rejection of (b). It changes the spec in two ways:
- It adds (c).
- It adds coordinator rules that the spec needs **even if (c) is never adopted**. Today's spec lets the coordinator answer a `failed` or `blocked` Task with a WC-6 retry (`SPEC:84`). For a Ruling-halted plan, that retry resumes into ledger row P or H and runs an operator review by automation (`LEDGER:155-156`). The protocol forbids exactly that: operator review is "user-initiated after a halt, never started by automation" (`QA:283`; `MO:51`). The current wording is therefore unsafe under its own recommendation.

## 2. Confidence and the strongest argument that lost
**Confidence is high for "keep the rule; no relay" and medium for "add (c)".**
- **Keep the rule and reject (b): high.**
  - All three advocates reached it in Round 2, including the advocate for (b), who withdrew it (`DT:469`).
  - The key safety points against relaying were won at 95-98% and conceded by (b)'s advocate: the person's own words (C-001), the executor's own explanation (C-003), and the conflict with the rule (X-001) (`DT:592,594,604`). The one exception was who-wrote-the-record (A-010), which was a 2-of-3 majority at 70% (`DT:610`).
- **Add (c): medium.**
  - Diff-point agreement was 27 of 27 (`DT:617-618`). Even so, the independent fault-finder found 6 high-severity gaps in the agreed position, and the debate's status is BLOCKED_BY_INVARIANTS (`DT:630-646`). Of the six, four are specific to (c) (INV-001, INV-014, INV-018, INV-022), one concerns the hand-back after (a) (INV-004), and one affects both routes (INV-017) (`invariant-probe.md:23-44`).
  - The fixes for those gaps were written during the merge, not argued in a debate round (`MO:146`).
  - One independent review of the fix plan failed its first draft (3 blocking, 8 minor findings). All 11 were applied, and the revised plan was not re-reviewed (`refactor-plan.md`, Review Status).
  - Two risks remain open and are accepted (`MO:147-148`).
- **The base pick was close.** Option (c)'s paper scored higher overall: 0.841 against 0.800, a margin of 0.041, inside the 0.05 tie band. Option (a)'s paper won on the tiebreakers: debate points 7 to 6, and correctness 5/5 against 3/5 (`base-selection.md`, Combined Scoring). That choice decides only which paper the merge started from. All three advocates recommended the same final position.

**Strongest argument that lost: (b)'s continuity.**
- One relayed answer lets the same worker carry on with no context switch. (b) won this continuity point outright: C-004, 95% (`DT:595`).
- It needs no access to the worker's files. (b) won this point outright too: A-009, 95% (`DT:609`). These are two of the three points (b) won outright (`DT:614`).
- It is single-writer by construction (C-009, `DT:600`).
- While the worker waits in `ask`, no automated review can start (r2-variant-2 new evidence 3, `DT:424`).

It lost for three reasons:
- The relayed reply is the coordinator's own message, which the rule excludes by name: "another agent's message ... not acceptance" (`QA:254`; `MO:130`). No test can detect a paraphrased relay.
- The gain applies to a rare event. A halt needs a confirmed blocker that a repair could not close (`QA:280`), and minor findings never halt (`QA:274`).
- A bad relayed Ruling becomes permanent: resume skips the completed task for good (`LEDGER:153`; `DT:603`).

## 3. What this means in practice
**What you will see.** Sometimes a build step running in Orca hits a problem that its automatic fix attempts could not solve. When that happens, the step stops and the coordinator tells you four things: which task stopped, what is missing, where the step's log file is, and which folder it ran in. Nothing else in that plan runs until you act (`MO:58`). Other plans keep going.

**What you do.** Choose one of two ways to answer:
1. **Answer in your own session (the default).** Open a session in that folder and run the same plan command. The tool explains exactly what it would accept and what that costs if it is wrong, then asks you. Say yes or no. The rest of the plan then runs in your session. Or you can stop your session there and tell the coordinator "session ended", and Orca picks the plan back up. Use this way whenever the problem is a dispute about the requirement itself.
2. **Write the answer into the log yourself.** Add one line to the log file. The line names the task, what you accept, why, and what it costs if that turns out wrong. Then tell the coordinator "Ruling written". The coordinator checks the line without changing anything. If the check passes, it restarts the plan in Orca in the same folder. If the check fails, it tells you why and sends you to the first way.

**What is different from today's spec.** The spec today offers only the first way. It also lets the coordinator quietly retry a stopped plan, which would run a review you never asked for. Under this recommendation:
- the coordinator never retries a stopped build plan on its own;
- the coordinator never writes or suggests the words of your answer;
- the stopped folder is left untouched until you answer.

**What could go wrong.**
- You write a line that is correctly formatted but accepts the wrong thing. No check can catch that, so the first way stays one choice away (`MO:148`).
- You edit files in that folder while deciding. The check sees changes only to the files the stopped task touched (`MO:147`).
- If the build step was sharing the feature's main folder, that whole folder stays frozen while you decide. Giving every build step its own child folder avoids this, but that is a change to CR-01 (`MO:94`).
- The coordinator's rules are written instructions for an AI session, not a program that enforces them. If the coordinator ignored them and wrote the line itself, nothing in the log could prove who typed it, because the build step checks only where the line sits (`RETRY:498`). This gap already exists today for every hand-written line, and it is accepted rather than closed (`MO:37`).

**What it costs to change later.**
- **Adding or removing the second way** later: spec text only. The Ruling rule files are untouched, and the one `/sc:implement` option change it relies on is needed by Phase 4 anyway (`MO:139-141`).
- **Moving to (b)** later, a relayed answer: the protocol's safety rule (`QA:254`, `LEDGER:68`) and the spec's non-goal 6 (`SPEC:319`) would have to change.
- **The coordinator's no-retry rule** should not be undone: it fixes an existing gap rather than adding a feature.

## 4. Exact spec wording change
Not applied: the spec is left untouched, as instructed. The changes below are for the next consolidated revision, together with D1, D3-D5, git ownership and CR-01. Quoted "current" text was read from the spec on 2026-11-02. Rules marked † were added in the merge and not argued in a debate round (`MO:56-60,71-76,88-101,124-126`).

**4.1 D2 entry, section 9 (`SPEC:334-337`).**
- `SPEC:334`: replace `` (`sk/sc-implement-protocol/refs/qa.md:232,238`) `` with `` (`sk/sc-implement-protocol/refs/qa.md:248-249,254`) ``.
- `SPEC:335`: replace the whole (a) bullet with:
  > - (a) **Keep the rule; the person gives the Ruling in their own session (recommended, with (c)).** The worker stops, writes the halt to its ledger and contract, and ends `failed`. The coordinator shows the person the halt and dispatches nothing for that plan until the person acts (section 2.3, "After an `/sc:implement` stop"). The person runs `/sc:implement <plan>` in their own session, from the halted worktree with the same plan path, and the run resumes from the ledger: the executor explains the scope and records the Ruling. The brief's ask policy does not apply to a Ruling halt (WC-3), so the coordinator never relays one. (a) is the only route for a `reason=dispute` halt.
- After the (b) bullet (`SPEC:336`, unchanged), insert:
  > - (c) **The person writes the Ruling line; the coordinator starts a resume Task.** The rule is unchanged. After the worker has settled, the person types the three-field Ruling line `T<id>: Ruling: <what> — <why> — <cost-if-wrong>` (`sk/sc-implement-protocol/refs/ledger.md:65,71`) into the ledger and tells the coordinator "Ruling written". The coordinator runs the read-only check in section 2.3. If it passes, the coordinator creates a resume Task (WC-6) in the same worktree, and resume row R completes the task with its non-compliant verdict unchanged (`ledger.md:154`). If any condition fails, the person is sent to (a).
- `SPEC:337`: replace `- Recommendation: (a), because the rule exists to stop an agent approving its own work.` with:
  > - Recommendation: (a) as the default, plus (c) as the way back into Orca; not (b). The rule exists to stop an agent approving its own work. Only (a) gives the executor's own explanation before acceptance, and (c) keeps the person's own words with no agent in between. (b) stays a possible later opt-in only if the user explicitly accepts relay risk, and never for `reason=dispute`.

**4.2 WC-3 (`SPEC:67`).** Replace the sentence that begins `A Ruling halt is never asked: while open decision D2 is (a),` and ends `(\`sk/sc-implement-protocol/refs/qa.md:238\`).` with:
> A Ruling halt is never asked: an `/sc:implement` halt for a Ruling (`E-HALT-QA`, `E-NO-RULING`) is reported blocked whatever the policy line says, because a coordinator's reply is "another agent's message", which is not acceptance (`sk/sc-implement-protocol/refs/qa.md:254`). The person gives the Ruling in their own session (D2 (a)) or writes the Ruling line into the ledger themselves after the worker has settled (D2 (c)). A Ruling line written or drafted by the coordinator or by any worker is "executor-invented approval" (`qa.md:249`).

**4.3 WC-4 (`SPEC:68`)†.** Replace `` `blocked_question` when blocked, and `reason` when failed. `` with:
> `blocked_question` when blocked, and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code; section 3.2 implement row).

**4.4 Section 2.3 (`SPEC:84`).** Append to the `failed` or `blocked` bullet:
> Exception: an `/sc:implement` Task follows "After an `/sc:implement` stop" below, because a WC-6 retry of a Ruling-halted plan would start an operator review by automation (`sk/sc-implement-protocol/refs/ledger.md:155-156`), which `refs/qa.md:283` forbids.

Then insert this paragraph after the "Reading a result" bullets (before "Fan-in rule"):
> **After an `/sc:implement` stop (D2).**
> 1. *Freeze.* A plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP code other than `E-RESUME-NEEDED`†. It is also frozen when the ledger's first non-complete task has `halt` or `blocked` as its last record with no eligible Ruling after it†. While a plan is frozen:
>    - The coordinator shows the person the contract and the full halt text, and dispatches no Task for that plan.
>    - No Task that writes outside its own report directory is dispatched into the halted worktree†.
>    - No one runs a git command there that changes HEAD, the index or the working tree. The halted worktree is not merged or removed†.
>
>    `E-RESUME-NEEDED` alone may be re-run by the coordinator without the person, as the same command in the same worktree, and only when the ledger shows no freeze†.
> 2. *Lifting the freeze†.* The freeze lifts only when the person's explicit hand-back is recorded in the coordinator's run notes **and** the ledger shows the matching state:
>    - "Ruling written" requires the check in item 3 to pass.
>    - "session ended" (after (a)) requires the halted task to be `complete` and the ledger's last line to parse. The drift baseline is then re-recorded.
>
>    After a stop with no halted task (for example `E-ARCHIVE-BLOCKED`), only the person's recorded instruction lifts it. After the hand-back the person makes no further edit in that worktree until the resume Task settles.
> 3. *Check before a resume Task under (c).* The coordinator reads the ledger and the worktree, never edits either, and dispatches only if all of the following hold. On any failure it tells the person which condition failed and sends them to (a).
>    - (1) The worker has settled (WC-6).
>    - (2)† After the later of the halted task's latest `halt` and latest `blocked` record, the only new lines are one Ruling line per halted task named in the contract. Each line has that task's id, ends in `\n` with no `\r`, and matches `ledger.md:71`.
>    - (3)† No field is blank, whitespace-only, punctuation-only or an angle-bracket placeholder, and the line has exactly two ` — ` separators.
>    - (4) The line is eligible under either clause of `refs/retry.md:498`.
>    - (5) No `halt` after the task's latest `start` has `reason=dispute`; and† the latest `halt` reason is not `no-evidence`, `no-snapshot` or `head-moved`.
>    - (6)† `HEAD` equals `<retries>/T<id>/q0-head`, and the paths in the `files=` field of the latest `blocked` line are unchanged against the tree its review graded. A missing `q0-head` or graded tree fails this condition.
>    - (7)† The resume brief has no `--force`.
> 4. *Placement†.* The resume Task starts in the halted worktree by selector (`worker-start --worktree path:<absolute worktree path>`), never in a new or child worktree. Under (a) the person runs from that same worktree with the same absolute plan path.

**4.5 Implement row, section 3.2 (`SPEC:132`).**
- Gate-resolution cell: replace `carrying the Ruling question; while D2 is (a), a Ruling halt is never asked, whatever the brief's gate policy (WC-3); the Ruling rule itself is unchanged (see open decision D2)` with:
  > carrying the Ruling question, the STOP code in `reason`†, the halted task id(s), the halt reason (`none` after `E-NO-RULING`)†, the absolute ledger path and the absolute worktree path; a Ruling halt is never asked, whatever the brief's gate policy (WC-3); the Ruling rule itself is unchanged (D2)
- "Other required change" cell: replace `none on the happy path` with:
  > Wave 0 accepts `--unattended` and `--report-dir <dir>` as known options, never part of source resolution or the slug hash†; briefs put every option before the source and pass a plan file or managed package path, never an inline prompt†
- Evidence cell: replace `sk/sc-implement-protocol/refs/qa.md:231-238` with `sk/sc-implement-protocol/refs/qa.md:247-256`.

**4.6 AC-4.1 (`SPEC:274`).** In the pass condition, replace `Under D2 (a): no \`question\` message from the worker and no Ruling in the ledger (WC-3). Under D2 (b): the worker asks, and the ledger's Ruling quotes the person's words verbatim` with:
> No `question` message from the worker and no Ruling in the ledger (WC-3), and the coordinator dispatches no Task for that plan. Then, in the same Orca-created worktree, four results are expected:
> - A Ruling line whose fields are `<what>`, `<why>` and `<cost-if-wrong>` is refused by the section 2.3 check, and nothing is dispatched.
> - A hand-written line with real fields passes the check.
> - The resume Task's contract names the same absolute ledger path as the halted Task's contract.
> - The ledger shows that task `complete` with the unchanged non-compliant verdict.

**4.7 Stale anchors.** The rule moved within `qa.md`. Its old lines now hold the Family probe section (`QA:228-238`).
- `SPEC:14`: replace `qa.md:231-238` with `qa.md:247-256`.
- `SPEC:185`: replace `qa.md:238` with `qa.md:254`.
- `SPEC:319` (non-goal 6): replace `qa.md:238` with `qa.md:254`.

`SPEC:235`'s `.dev/worktrees/` is replaced by CR-01's Orca-created worktree (`CR-01:41`), not by D2.

## 5. Interactions with D1, D3-D5, git ownership and CR-01
The other five recommendation files are final on disk (each `Status: COMPLETE`, line 3 of each file, re-read at 18:30Z on 2026-11-02). Several were written while this one was unfinished, so their D2 rows describe the debate consensus or (a) alone; none conflicts with (a)+(c).

| Decision | Final recommendation | Interaction with this D2 recommendation |
|---|---|---|
| D1, how a command knows it runs unattended | Option (c) as amended: the `--unattended` flag is the only switch, and a worker-session "brief guard" refuses a brief that lacks it (`decisions/D1/RECOMMENDATION.md:11`) | Compatible; D1 says so too (`decisions/D1/RECOMMENDATION.md:92`). The resume Task is an ordinary worker brief, so it carries `--unattended` and `--report-dir`, and D1's guard applies to it unchanged. D2 needs those two flags in `/sc:implement`'s Wave 0 option list, before the source (section 4.5). Under (a) the person runs without `--unattended`, as a normal session. |
| D3, `/sc:pr-submit` as a worker | Option (a), amended: not a worker. Each PR's run happens in one top-level session in that PR's own child worktree, started only when the person names that PR (`decisions/D3/RECOMMENDATION.md:9`) | No conflict; D3 says so too (`decisions/D3/RECOMMENDATION.md:88`). pr-submit commits and pushes, which moves HEAD (`SPEC:340`). Its own child worktree keeps it out of a worktree frozen by a Ruling halt. Merging that PR's branch into a halted worktree is forbidden until the freeze lifts (section 4.4). |
| D4, outward actions in a brief | Option (c′), overturning the spec: no worker acts outside the machine. A worker may make a local commit only when the user asked and it sits alone in its own Orca child worktree (`decisions/D4/RECOMMENDATION.md:7,9`) | Same principle as D2: approval does not cross sessions through an agent. D4 records accepting the coordinator's quotation for a local commit as a known inconsistency with D2, and it adopts D2's no-touch rule for a halted worktree (`decisions/D4/RECOMMENDATION.md:112`). A commit by an implement worker between tasks is safe for D2's drift check, which compares against the task's own `q0-head`, written at that task's start (`SKILL:114`). No commit may run in a frozen worktree. |
| D5, nesting depth | Option (a): keep depth 1 (`decisions/D5/RECOMMENDATION.md:7`) | None. The coordinator creates the resume Task; no worker starts a worker (D5 agrees, `decisions/D5/RECOMMENDATION.md:69`). |
| Git ownership | Option E, the hybrid: the coordinator owns every push, PR, review reply, comment, merge and worktree removal. A worker commits only in its own child worktree and only with the user's quoted grant (`decisions/git-ownership/RECOMMENDATION.md:9`). A child worktree is used when, among other triggers, `/sc:implement` runs beside any other writer (`decisions/git-ownership/RECOMMENDATION.md:14`). | Compatible. Its D2 row requires the person to resume inside the child and forbids removing a child whose ledger is unfinished (`decisions/git-ownership/RECOMMENDATION.md:90`). That matches D2's placement and freeze rules, and D2 extends them: no merge, rebase, reset or other HEAD/index/tree change either (section 4.4). **Open item it raises:** a managed package must already be in the child's checkout before dispatch; getting it there needs a coordinator commit (with the user's ask) or a copy (same line). That affects where the resume Task and the person's (a) session can find the package. UNVERIFIED and unresolved. |
| CR-01, feature worktree hierarchy (PROPOSED, `CR-01:3`) | T2: a child worktree for `/sc:implement` when another worker writes alongside it (`CR-01:18`) | Three effects. (1) A child holding a halted ledger must be neither merged nor removed until the freeze lifts, because a legacy ledger is never `git add`ed (`LEDGER:3`); removing the worktree would destroy the halt record. (2) The resume Task goes into that same child by selector, overriding T2's `new-child` for the resume (section 4.4, item 4). (3) **Recommended for the CR-01 decision:** widen T2 to every `/sc:implement` worker, so a Ruling halt never freezes the shared feature worktree (`MO:94`). This is the user's call under CR-01; D2 works either way. |

## 6. Fixed constraints applied
These are user decisions made after the debate started. They were applied as given, not debated (`MO:22-28`).
- **Orca worktrees only, at Orca's default paths.** The resume Task, the person's (a) session and the AC-4.1 live check all use the Orca-created worktree the halted Task ran in. Nothing goes under `.dev/worktrees/` (`CR-01:41`).
- **SuperClaude upstream is never touched.** D2 adds no outward action. No D2 step uses Orca's issue or PR linking (`CR-01:45`).
- **PR #343.** It changes nothing in the Ruling path.
  - Only blocking findings halt or reach a Ruling; minor findings are recorded and cleared (`QA:274`, `QA:280`, `QA:288`). This is the same "blocking only" rule PR #343 applied to reviews.
  - PR #343 caps review loops at 2 fix cycles, then escalates to the user (`MO:27`). Our reading, not a statement from PR #343 or the protocol: in `/sc:implement` that escalation is the `E-HALT-QA` halt, and D2 keeps the decision with the person.
  - `/sc:implement` now gets one A2 repair (`QA:267`, `RETRY:142`). That changes which fixes run before the adviser route, not the halt or Ruling rules. Whether halts become more frequent is UNVERIFIED (no run data).
  - The installed copy at `~/.claude/skills/sc-implement-protocol/refs/` still has the pre-#343 text in 6 places (`qa.md:267`, `ledger.md:143`, `retry.md:141-142,147-149,189,193`; compared with `diff`). Every Ruling-path line D2 cites is identical in both copies. Re-running the install would bring the copies back in line; that is outside this task.
- **CR-01.** Applied as described in section 5.

## 7. Process notes and UNVERIFIED items
**Process.**
- **Step 3 was not complete on disk when the run resumed.** `base-selection.md` still had four empty sections: position-bias log, combined score, selected base, and strengths to carry over. They were filled from the verdicts already written, and no verdict was changed (`base-selection.md`, Position-Bias Mitigation, first paragraph).
- **Step 4.** `refactor-plan.md` was drafted on resume and reviewed independently. The first draft FAILED with 3 blocking and 8 minor findings. All were applied; the revised plan was not re-reviewed.
- **Step 5.** The merge-executor applied 13 of 13 changes. Post-merge validation passed: 25 cited lines re-opened and 3 wording contradictions fixed (`merge-log.md`, Summary).
- **Return contract.** `status: partial`, because convergence stayed BLOCKED_BY_INVARIANTS (`return-contract.yaml`).

**UNVERIFIED.**
1. Whether halts become more or less frequent after PR #343 removed the second A2 repair. No run data exists.
2. Whether an LLM coordinator follows the freeze, check and placement rules reliably. They are written instructions with no mechanical enforcement in this spec. A coordinator-side script for the check (section 4.4, item 3) would make them testable; none exists.
3. Whether `worker-start --worktree path:<existing Orca-created worktree>` starts a new Task in a worktree that still holds a settled Task's files. The flag is documented (`CR-01:48`), but this case has not been run. AC-4.1's extension would show it.
4. How a managed package reaches a child worktree before dispatch. Git ownership leaves this open (`decisions/git-ownership/RECOMMENDATION.md:90`), and it decides whether route (c) and the person's (a) session can find the package in the halted child.

**Independent citation check.** A fresh `evidence-validator` agent checked about 105 citations, 9 quoted "current" spec strings and every numeric claim in the first full draft. Its verdict was FAIL: 2 wrong, 2 missing, and 7 overstated or stale items. The failures were a stale claim that the sibling recommendations were not final, a wrong "the one point (b) won outright", an uncited "5 of them in (c)", and the installed-copy count.
- All 11 items were fixed in place. Each fix was re-read against its source before editing.
- The fixed draft was not re-checked by a fresh agent.
