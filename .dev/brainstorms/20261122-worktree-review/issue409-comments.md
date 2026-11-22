=== 2026-11-06T14:09:09Z ironbelly
## Versioned design package and embedded previews

The complete design study is published for collaboration on branch **`docs/409-orca-dashboard-designs`**:

- **[View all twenty embedded design images on GitHub](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/PREVIEWS.md)**
- **[Browse the complete editable package](https://github.com/IronbellyOrg/IronClaude/tree/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106)**
- **[Download the complete package ZIP](https://github.com/IronbellyOrg/IronClaude/raw/refs/heads/docs/409-orca-dashboard-designs/.dev/issues/409/orca-observer-design-package.zip)**
- [First ten-page PDF portfolio](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/portfolio.pdf)
- [Additional agent-supervision PDF portfolio](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/agent-focus/portfolio.pdf)
- [Design comparison and recommendations](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/concepts.md)
- [QA and review limitations](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/QA.md)
- [Evidence ledger](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/sources.json) and [integration questions](https://github.com/IronbellyOrg/IronClaude/blob/docs/409-orca-dashboard-designs/.dev/design/orca-observer-20261106/integration-gaps.md)

The issue body already contains **22 actual embedded GitHub image attachments**: all twenty primary designs plus both contact sheets. The new Markdown preview page also renders repository-hosted images directly.

The ZIP contains **406 package files** plus its per-file hash manifest. SHA-256: `5e169becf792219a9ed7f58f4146e0b0d874eb31574783375a2d8160e5860191`.

For interactive inspection, download/extract the ZIP and open `orca-observer-20261106/index.html`. GitHub renders the Markdown/PNG previews and PDF files, but displays gallery HTML as source rather than running it. The galleries need no server or live connection.

All data is synthetic. No production integration, deployment, operational controls or PR is introduced. Please identify the concept name and terminal width when giving feedback here; the human still chooses the direction.

<!-- orca-dashboard:collaboration-branch -->

=== 2026-11-11T14:47:52Z clayphi
@ironbelly (Ryan): this is my reply to your ClickUp DM of 2026-11-06 asking whether the dashboard is worth the effort. You asked me on 2026-11-07 to leave it here. It is copied word for word from the DM.

The Fleet Quilt and Decision Desk screens would be most useful to me, but need a simple plain english summary of the 'task/issue', whats done, whats left to do, and if it needs me. Link to the pr/issue if one exists

Loop Detector or Mission Pulse - if this had a sort of easy to understand flow of what the agent has done with, so instead of "Retry 1" its like Brainstorm - and that is green if its done, yellow in progress, red fail. That kind of thing. Next box is whatever comes next in that spec

Signal bridge could be nice if it was Issue (link) / PR (link) / Lifecycle / Phase. Ya, with colors for running, done, blocked, stuck, at PR

^ esp on Signal bridge if you could click to open that session

=== 2026-11-17T07:09:29Z ironbelly
## Status review 2026-11-17
**Status:** ACTIVE. The observer (`superclaude observe`) is built and had two merged changes plus a live test this week. The issue text itself is stale.

**Findings:**
- #577 (merged 2026-11-17) switched the coordinator-questions panel on (`QUESTION_GATE_PASSED = True`, `src/superclaude/cli/observe/commands.py:67`), applied the 11 agreed cuts, and recorded the owner's direction decision. Earlier releases: #503 and #514.
- #586 (docs, merged 2026-11-17) recorded a live questions test and a synthetic load test.
- An owner-run read on 2026-11-17 listed 41 old questions and two repeat reads of the same Run returned all 41 both times, so the read did not consume them. All 41 were old, so this does not prove a fresh unanswered question survives a read (recorded in #589).
- The issue body still carries a correction banner saying "no observer code exists" in several places. The design package branch `docs/409-orca-dashboard-designs` is not merged (no PR).

**Experiments / evidence:** load test: steady traffic lost 0 of 181 messages; a 130-message burst lost 30 of about 415 (4 of the 130 burst messages, 26 unattributed). Real traffic is unmeasured.

**Next steps:**
1. Owner grants the pending correction pass on this issue body (the record lists it as waiting on the Q8 record fields).
2. Measure the questions read against real traffic, and decide what to do about the burst loss.
3. Decide whether the design package branch gets a PR or stays as a reference.

**Related:** #339 (agent-facing half), #503 and #514 (observer releases), #577, #586, #589, #534.

Posted by Claude Code during the 2026-11-17 open-issue review.

=== 2026-11-17T17:56:55Z ironbelly
## PR #591 (issue watcher coordinator handoff, Plan B): what it means for this issue

Checked 2026-11-17 by a read-only `/sc:analyze` pass over the files #591 changed (merge commit `6af80d6c0`), then spot-checked against the files. Nothing was run.

**Verdict: partly relevant.** #591 changes no code, Orca command, field or Run behaviour that `superclaude observe` reads or constrains: the allow-listed commands, the forbidden verbs, Run binding and the QUESTION-LINK assumptions are all unchanged. It does add a plan-approval flow and a coordinator-started worker flow that touch alignment items 2, 6 and 9, the "How the pieces fit" diagram and the future write-back idea.

**What #591 does.** The watcher now claims with `/sc:issue --claim <n> --pipeline none`; that claim session ends after its comments. A person-opened coordinator then creates the worktree and starts the worker with `worker-start`. A worker's plan is approved through a worker `ask` and a hash-bound coordinator `reply` (rule WC-17). It also adds a local release file and a launch-level guard rule: a bound worker may `send` and `ask` only with no `--to`. #591 defines no new Orca field on Runs, Tasks, workers or worktrees.

### Additional considerations

1. **Alignment item 9 and the diagram.** The watcher's claim session is no longer the long-lived session. The observer sees the worker only once it is a `worker-list` row. The claim session, the gap before `worker-start`, and the adoption and approval rows are not visible through `worker-list`. Showing watcher or coordinator state (item 9) is still open and needs a source other than `worker-list`.
2. **Alignment item 2 and the write-back idea.** A plan-approval question must be answered by the coordinator after it writes the approval row. A raw `orca orchestration reply` typed by a person would bypass that record. `write-back-future-stage.md` line 38 ("the exact `orca orchestration reply` command for the human to run") must not apply to plan-approval questions. Today the observer prints no command.
3. **Alignment item 6.** #591 adds a third local trust mechanism that is unsigned: a hook rule, a `sessions/<id>.ok` release file, and hash-bound approval rows. Compare it with the Coder#477 and #339 proposals before one trust design is chosen.
4. **The #394 sentence is partly answered.** The watcher claims at `--pipeline none`. A coordinator-started worker is bound by the launch-level guard only when its brief carries a launch marker; the first test issue runs unbound by owner decision.
5. **Approval latency.** A plan-approval question can stay listed as open after the person approved on GitHub, until the coordinator's next wake. The observer lists it without a closure claim, which is correct. Do not add an "approved" or "answered" mark without a source.
6. **Optional hardening.** `worker-start` and `worktree create` are refused only because they match none of the three argv templates; the forbidden set does not name them. Naming them would change no behaviour. The set only grows.
7. **Where to run the observer.** Not inside a worker bound by the launch-level guard: the guard blocks `orchestration worker-list` for bound sessions. Run it from a person's terminal or the coordinator's own session.
8. **Visual-parity fixture.** A plan ask carries a plan path, a file list and a 64-character hex hash. Add one fixture question with such a token and check the 80-column Decision Desk frame wraps or cuts it cleanly.

No acceptance criterion becomes stale or newly answerable. Approval and plan state still have no source, so they stay `unavailable (no source)` and must not get a column or badge in the visual-parity work. Item 1 (sweep facts), 4, 7, 8 and 10 are unaffected.

### Stale text in this issue body

The diagram arrow "issue watcher ... starts a claim session" and the sentence in Related Issues that the watcher "starts `/sc:issue --claim <N>` sessions" are now more specific (considerations 1 and 4). `docs/designs/issue-watcher.md` still names a "TUI dashboard" as a possible approval surface, which conflicts with this issue's Out of Scope ("approving ... instructing workers").

### UNVERIFIED

- That a worker's plan-approval `ask` is stored as type `question` and so appears in the observer's question read (Q-3 in `unverified-register.md`).
- That plan asks carry sender `dispatch:<id>` equal to the payload `dispatchId`.
- Whether the coordinator's Run that receives these asks is the Run named in the owner record.
- Whether the claim session and a worktree with no agent appear in `worker-list` (assumed not), and how the sweep classifies such a worktree.
- #591's reported test counts (not re-run).

### Where this issue stands (2026-11-17)

Releases R1 to R3 are merged (#503, #514, #577, #592), and question text is screen-only (#598). Remote fleet (R4) is backlog issue #604. Visual parity with the design mockups is sub-issue #606.

=== 2026-11-17T18:45:05Z ironbelly
Visual parity review done on sub-issue #606: two reviewers (Opus 5.5 and GPT 6 Astra) compared the real renders with the mockups, debated in three rounds and produced one merged list: 18 findings to fix (5 High, 9 Medium, 4 Low), 2 spec guards, 7 accepted divergences, 1 owner decision. Findings: https://github.com/IronbellyOrg/IronClaude/issues/606#issuecomment-6957531081

=== 2026-11-17T21:43:46Z ironbelly
Visual parity redesign spec is ready: #606 (sub-issue of this one). Its body holds the phased spec (P0 to P7, each phase ending in a render gate with a fixed rubric, at most 3 iterations, escalation on a stalled gate), the ANSI colour depth decision, the Zellij go or no-go (optional layout only, not a dependency) and the claim instructions (run `/sc:workflow` on the spec, then `/sc:implement` its plan). The full step tables are in three comments on #606.

Needs the owner: D-1 (adopt two-column layouts at 160 and 116, which reverses the stacked layout recorded in rendering-rules.md lines 43 and 57). Defaults for the other open decisions are listed in the spec, section 10.

Closing #409 still depends on #606 for the visual parity part.

=== 2026-11-18T01:04:29Z ironbelly
Layout decision for #606 recorded: Decision Desk in two columns at 160 and 116, questions screen stays stacked at every width (owner ruling 2026-11-18). Details and the comparison renders: https://github.com/IronbellyOrg/IronClaude/issues/606#issuecomment-6962861444
=== 2026-11-18T03:30:41Z ironbelly
Space-diet rulings for #606 recorded (no hash on screen, each fact once, reasons once, status badge, ledger diet): https://github.com/IronbellyOrg/IronClaude/issues/606
=== 2026-11-20T20:56:48Z ironbelly
Review of the objectives on 2026-11-20: the dashboard core is built and merged (releases 1 to 3 and the visual parity work, #673). Five criteria added on 2026-11-13, the scale tests and three owner decisions are not done. They are tracked in #706. This issue stays open until #706 is done; remote fleet stays in #604.
