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
