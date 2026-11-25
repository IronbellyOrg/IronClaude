# Position paper: OURS on D10 (wake transport)

Topic: how the poll should wake the coordinator. Author stance: the strongest honest case for the owner's line.
Status: stub, filled below.

Paths below are in the read-only export of origin/master (`/home/coder/.cache/ic-snap-20261120/master`) unless marked otherwise. "D:nnn" is a line of `docs/designs/orchestrator.md` (Clay's design, merged by PR 681, the design pull request).

## The claim

The poll should not grow a new delivery channel. It stays a pull poller that does one thing to start work: it launches a session through Orca's own `orca agent launch` with a prompt built from one validated integer (`/sc:issue --claim <N> --pipeline none`). The person-opened coordinator then picks the claimed issue up from files the claim leaves (the watcher store `dispatch.json`, `issue-summary.md`, `next-steps.md`) and talks to its workers through Orca's own `ask` and `reply`. No listener (Coder issue 477), no typed wake line, no wake-file protocol, no second copy of the Orca terminal code.

## The mechanism

1. The poll finds an approved issue, writes a durable `pending` record before it spawns (so a crash cannot double-launch), and launches one claim session with the fixed prompt. A lost reply is settled with Orca's operation id and `--retry-launch`.
2. The claim session assigns the issue, posts its two comments and writes the summary files, then ends. It makes no worktree and starts no agent (`--pipeline none`, Plan B, owner decision 6).
3. A person-opened coordinator reads the claim's files at each gate or wake, creates the worktree, and starts the worker. Approval is Orca's `ask` and `reply`, never text typed into a terminal.

## Cited facts

1. The poller is pull-only on purpose: "D1 option A ... No listener, inbound port or address registry" and non-goal NG-1 "push designs B/C/D" (`docs/designs/issue-watcher.md:47`, `:76`). The Coder issue 477 statement says option A "makes IronbellyOrg/Coder#477 unnecessary unless B or C is revisited" (`issue-watcher.md:55`). So the listener was already rejected by the owner's design, not only by Clay (D:66 repeats the rejection as a non-goal).
2. The owner already narrowed Coder issue 477 (the workspace listener with prompt routing): Q3 "1 Keep and Narrow", "narrow Coder#477 to read-only status and identity with no prompt routing; the issue stays open" (owner decision record `owner-answers.md:25`, in worktree `claim-handoff-planb`, folder `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/`). A prompt-routing listener is therefore wanted by neither line. Issue 477 itself (opened 2026-11-07, still open) carries the owner's comment of 2026-11-13 "Ensure this aligns with Orchestrator and TUI Panel".
3. The rule "no GitHub text reaches a prompt" is the owner's D3, built and tested: "D3 only a validated integer issue number reaches a session prompt" (`issue-watcher.md:39`, `:49`); `PROMPT_PATTERN` and `build_claim_prompt` (`src/superclaude/cli/issue_watch/launch.py:33`, `:84-92`); `launch_argv` refuses any other prompt (`launch.py:95-116`). Clay's design calls its own version "the carried-over ... rule in its new form" (D:155).
4. Typed text as an approval route was dropped by the owner: decision 6 "Go with B now", "approval is Orca's own `ask` and `reply`, not text typed into the agent's terminal" (`owner-answers.md:139`); the coordinator duties say the coordinator "types nothing into a worker's terminal for this flow" (`WORKER-CONTRACT.md`, section "Issue pipeline duties", in worktree `claim-handoff-planb`, unpushed).
5. The launch path has crash and duplicate protection already merged by the owner's PRs 447 and 448 (the issue watcher poller and its fixes): pending write before spawn, one launch per cycle, operation-id retry (`launch.py:119-132`; `issue-watcher.md:23`).
6. Clay's wake mechanism is unproven by Clay's own register: risk K11 "The wake mechanism is unproven here" (D:1233); unverified U5 "A sender outside any Run ... may post to `run:<id>`" (D:1263; D:163 "no one has run it from a plain shell"); unverified U25, that ccsession accepts the session tag (D:1283). Nothing on master reads a wake file: PR B (the orchestrator skill) does not exist (`FULL-REPORT.md` section 2).
7. PR 686 (Clay's rewrite of the poller, head 8e5ae29ad, export `pr-a`) copies the Orca terminal code: `wake.py` lines 9-12 say it "duplicates that script on purpose" (`claude_processes`, `typing_or_fresh`, `is_idle`, `send`). The master original says the opposite rule: "Shared by the waker (FR-26: reused, never copied)" (`src/superclaude/skills/agent-work-report/scripts/orca_term.py:3`). PR 686 adds parity tests for `find_orca` and the origin check (`tests/issue_watch/test_find_orca_parity.py`, `test_origin_parity.py`) but none for this copy: in `pr-a/tests/issue_watch` the word `orca_term` appears only in a comment (`test_wake.py:495`). Clay's own register accepts the duplication "for now" (K16, D:1238).
8. Clay's delivery logic depends on screen reading and timing: "idle at its prompt, no unsent typing and no output in the last 60 seconds" (D:112; `wake.py:64`, `:746-790`) and on the ccsession name question text "Session name" read from a fresh terminal (`pr-a` `launch.py:50-51`; the `OrcaLauncher` docstring in the same file marks the fresh-terminal behaviour UNVERIFIED). Our launch is one Orca verb with a receipt.

## What it costs

- One Claude session is started per claim (model tokens), where a wake file costs none until a session reads it.
- There is no push signal to a running coordinator in our line. It reads the claim's files "at each gate or wake" and "nothing starts while the coordinator is down" (`issue-watcher.md:43`). The owner accepted that delay "for now" (decision Q36, `owner-answers.md:185`).
- No acknowledgment loop: the poll cannot tell that the coordinator saw a claim.

## What it risks

- The coordinator may sit idle after a claim until someone or a timer wakes it. Coder issue 516 (every project always has a coordinator session) states the gap: "A running coordinator session must then take the claimed issue ... Today nothing provisions that coordinator."
- The launch reply shapes are still `_assumed_shape` fixtures until the live test (FU-1) runs (`issue-watcher.md:33`). Our path is also not yet proven live.

## What it gets right

- Smallest new surface: nothing to secure, no port, no extra Orca call that can fail.
- Keeps the one security rule that matters (integer-only prompt) in one place with a property test.
- Does not copy code and does not add a channel that PR B must also build before anything works.
- Matches both lines' agreement that the listener of Coder issue 477 is out.

