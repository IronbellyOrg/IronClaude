# PR #591 relevance to issue #409

Written 2026-11-17. Source of truth for #591: merge commit `6af80d6c0` (merged 2026-11-17T17:28:21Z), read with `gh pr view 591 --repo IronbellyOrg/IronClaude` and `git show origin/master:<path>`. The #591 files are not in this checkout (`6af80d6c0` is an ancestor of `origin/master`, not of HEAD `b967ccd15`), so line numbers below for #591 files are lines of the `origin/master` copy. Observer line numbers are from this checkout.

Method note: `/sc:analyze` was invoked through the Skill tool and followed. Domain: architecture and dependency, over the PR's changed files, read statically. No code was run. Codegraph: index_state=fresh, checked_at=2026-11-17T17:52:37Z; degraded: graph:empty (the #591 files are not in this checkout's index, so they were read with `git show`; the observer's `adapter.py` outline was read with `codegraph_node`, then re-read with Read before citing).

## Verdict

**Relevant: partly.** #591 changes no code, Orca verb, argv, field or Run behaviour that the observer reads or constrains, but it adds a plan-approval question flow and a coordinator-started worker flow that touch alignment items 2, 6 and 9, the "How the pieces fit" diagram, and the write-back idea in `write-back-future-stage.md`.

## What PR #591 changed

PR title: "feat(issue-pipeline): coordinator handoff for the issue watcher (Plan B)". The PR body says it builds on Plan A (#584). The adoption and approval row code (`approval_record.py`) is from Plan A and is not in #591's file list; #591 adds the duties and one helper around it.

| Area | Files (origin/master) | What changed |
|---|---|---|
| Worker contract | `src/superclaude/core/WORKER-CONTRACT.md` (+13/-1) | New rule WC-17 (line 59); new section "Issue pipeline duties" (lines 291-300); brief template accepts `Worktree: path:<existing worktree>` |
| Watcher prompt | `src/superclaude/cli/issue_watch/launch.py:33` | `PROMPT_PATTERN` and `build_claim_prompt` now give `/sc:issue --claim <n> --pipeline none` |
| Claim docs | `commands/issue.md`, `skills/sc-issue-protocol/SKILL.md`, `refs/claim.md` | One "Coordinator handoff for `--pipeline none`" paragraph in each |
| Claim script | `skills/sc-issue-protocol/scripts/orca_worktree.py` | New `pending --level worktree\|full\|full-submit` subcommand (writes one launch record, prints a nonce) |
| Brief | `cli/issue_pipeline/brief.py`, `templates/worker-brief.txt` | Optional 32-hex nonce; optional line `Launch marker: [sc-launch:v1:<nonce>]`; new line `Plan approval: ... follow rule WC-17` (worker-brief.txt:10) |
| Release helper | `cli/issue_pipeline/release.py` (new), `cli.py` | `superclaude issue-pipeline release-worker <session_id>`: creates `sessions/<id>.ok` in the launch-level store |
| Guard (security hook) | `hooks/scripts/launch-level-guard.sh`, plugin copy byte-identical | A bound worker may run `orca orchestration send` and `ask` only with no `--to`; `--to`, `--run`, `--environment`, `--pairing-code` are ESCAPE (lines 489, 506, 527); coordinator-side `issue-pipeline` verbs are TAMPER for a bound worker |
| Docs | `docs/designs/issue-pipeline-guard-g2.md`, `...-g2-no-to.md`, `issue-watcher.md`, `issue-watcher-setup.md`, `sc-issue-*.md`, `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` | Design note for guard G2; watcher decision D2 superseded again (2026-11-17); runbook says a coordinator must run first |
| Tests, task packages | `tests/hooks/test_launch_level_guard_worker.py` (new, 330 lines), `tests/issue_pipeline/`, `tests/issue_watch/`, `tests/skills/`; `.dev/tasks/**` | Pins for all of the above |

Not touched by #591: `src/superclaude/cli/observe/`, `src/superclaude/cli/sweep/`, WC-16 (the sweep duty, WORKER-CONTRACT.md:289), anything under `.dev/issues/409/`.

## (a) What #591 adds

- **Flow.** The watcher launches a claim session with `/sc:issue --claim <n> --pipeline none` (`launch.py:33`). That claim assigns the issue, posts comments and writes `.dev/issues/<N>/` files in the checkout; it creates no worktree and starts no agent (`commands/issue.md`, new paragraph). A person-opened coordinator then runs the `worktree` step of `orca_worktree.py` (creates the worktree with no agent) and straight after `worker-start --worktree path:<path> --agent claude --spec <brief>` (WORKER-CONTRACT.md:295-298). "Nothing starts while it is down" (line 292).
- **States (adoption row):** `reserved`, `started` (with Dispatch id), `uncertain`. Rule: never start again for an `uncertain` row; settle it by reading `worker-list` (line 296). **Approval row:** `recorded`, `instructed`, `acked`, `revoked` (`approval_record.py:44-45`, from Plan A). Neither is an Orca state.
- **Files and records.** Adoption and approval rows live in an "approvals directory of their own" passed as an argument to the `issue-pipeline` verbs (`approval_record.py:3-5`, `cli.py:48`); its location is not fixed in the text I read. `release-worker` writes `~/.claude/state/launch-level/sessions/<id>.ok` (`release.py:30-66`); `pending` writes `pending/<nonce>`. The worker's report directory is `.dev/issues/{N}/worker-plan` (worker-brief.txt:12).
- **Orca verbs named for the coordinator:** `worker-start`, `worker-list`, `reply`, plus the script's agent-less `worktree create` (WORKER-CONTRACT.md:295-298). For the worker: `ask` and `send` (heartbeat, `status` ack, `worker_done`) with no `--to` (WC-17, line 59).
- **Messages.** (1) Worker `ask` with plan path, file list and plan hash (WC-17 step 2). (2) Coordinator `reply` with `approved <record-id> plan-sha256=<hash>` (line 298). (3) Worker `status` ack, body `ack <message_id> applied|refused` (WC-17 step 5, WC-12). (4) `worker_done` stating a refusal word on mismatch. WC-17 says this ask "does not use up WC-3's one ask per Task".
- **Approval flow.** The plan reply is posted on GitHub; approval is read through `stage-status` (label or an `approved` comment); on approval the coordinator writes the approval row, then replies to the worker's ask, then mirrors label and Status (line 298; `issue-watcher.md` D2 text). An approval given in the coordinator session is immediate; one given on GitHub waits until the coordinator's next gate or wake (owner Q36, `issue-watcher.md`, D2 paragraph).
- **New fields on Runs, Tasks, workers, worktrees:** none are defined by #591. The only Orca-side effect it describes is a worktree with an empty `agents` list in `orca worktree ps` between the script and `worker-start` (commands/issue.md, new paragraph); that is the PR's claim, not observed here.

## (b) Data the observer could read, show or misread

What it could read (all through the existing `worker-list` and R2 question read, nothing new in argv):

1. **Plan-approval asks as questions.** If a worker's `orchestration ask` is stored with type `question`, each plan approval would appear in the question read of the coordinator's Run. Evidence it is plausible: `unverified-register.md:33` records 39 of 41 questions on the coordinator's Run with a JSON payload holding `dispatchId`, `taskId`, `question`, `options`. Q-3 ("whether `ask` writes type `question`") is still UNVERIFIED (`unverified-register.md:49`). The question text would carry plan path, file list and a 64-hex hash; the observer shows text screen-only, sanitized, one line, at most 400 characters (`adapter-contract.md:41`).
2. **Coordinator-started workers.** After `worker-start` the worker is an ordinary Dispatch row in `worker-list`, in the coordinator's Run, in worktree `issue-<N>`. Nothing in #591 changes the row shape.

What it must not misread:

- **"Open" is not "unanswered".** A plan-approval question may stay in the window after the person approved on GitHub, until the coordinator's next wake replies. The observer already refuses to claim closure (`adapter-contract.md:60`: "marked `no longer in source window` and never closed"), so no code change; the wording on screen must not suggest the plan was approved or is pending a person's approval.
- **Approval is not an observer fact.** Plan hash, approval row state and GitHub label are not in `worker-list` or the question read. `rendering-rules.md:71` keeps "human approval" as `unavailable (no source)`; #591 gives no source, so that stays right.
- **Acks and heartbeats** are `status` or `heartbeat` messages; the question read filters `--types question`, so they are not read (`adapter.py:32`).
- **The claim session** is started by the watcher through `orca agent launch`, not `worker-start`. Whether it is a Dispatch in `worker-list` is UNVERIFIED; the observer would treat it as absent either way.
- **The gap between script and `worker-start`:** a worktree with no agent and no terminal, and an adoption row `reserved`/`uncertain`. No `worker-list` row exists for it, so the observer cannot show it (it reads no worktree or file source).
- **Launch marker** `[sc-launch:v1:<nonce>]` sits in the worker's first prompt and the terminal title; the observer reads neither.

## (c) What the observer depends on or constrains

- **Allow-listed argv: unchanged.** Three shapes only (`adapter.py:29-32`, `assert_allowed` `:135-170`). #591 adds no verb the observer needs.
- **Forbidden verbs.** The #591 flow uses `reply`, `ask`, `send` and `worker-start`. `reply`, `ask`, `send` are already forbidden prefixes (`adapter.py:34-50`). `worker-start` and `worktree create` are not named in that set; they are refused because they match none of the three templates (`adapter.py:153-154`). So: no change needed, but the forbidden list does not name them (see consideration 6).
- **Run binding and `consumer_fenced`.** #591 does not mention `run-use` and does not change binding. Worker `ask`/`send` default to the owning Run mailbox (Orca help quoted in `issue-pipeline-guard-g2.md:30`). The observer must still run where it holds the Run (`adapter-contract.md:61`). Favourable fact: one coordinator owns every watcher-claimed issue on the host (WORKER-CONTRACT.md:292), so these asks should land in one Run, which fits "one named Run". Whether the coordinator's Run is the Run the owner record names is UNVERIFIED.
- **QUESTION-LINK assumptions.** The observer requires sender `dispatch:<id>` equal to payload `dispatchId` (`adapter-contract.md:41`). #591 does not change how senders are set. A plan ask with no `--to` from an active Dispatch is expected to behave like the other asks, but I did not read a plan ask; UNVERIFIED. G2 note fact 2 itself says it is unverified that a bound worker's `--to`/`--from` reach the guard (`issue-pipeline-guard-g2.md:41`).
- **Message window.** One more ask per claimed issue adds traffic to a window already at 41 rows on the coordinator's Run (`unverified-register.md:34`). The 100-row cap and the `window full` flag are unchanged.
- **Guard and the observer.** The guard binds only workers started with a launch marker. Its Orca allow-list, as changed, admits `orchestration check` but not `orchestration worker-list` (guard diff, the "status / help / --version / ... / orchestration check|inbox|run-current|task-list|worker-show" arm). So if the observer were ever run inside a bound session, its `worker-list` call would be classed ESCAPE. The observer is normally run by a person or the coordinator, which are not bound; no conflict today.

## (d) The ten alignment decisions, acceptance criteria and plan

| # | Affected? | How |
|---|---|---|
| 1 Facts source (sweep JSON) | No | #591 does not touch the sweep. `cli/sweep/` has no reference to `issue_pipeline`, adoption rows, `dispatch.json` or the watcher (searched on origin/master). |
| 2 Navigation versus recommendations | Yes, indirectly | A correct plan-approval answer is not a bare `reply`: it must follow an approval row and a hash-bound text (WORKER-CONTRACT.md:298). `write-back-future-stage.md:38` says Decision Desk "may show a pending question and the exact `orca orchestration reply` command for the human to run themselves". For a WC-17 ask that command would bypass the approval record and the GitHub mirror. See consideration 2. |
| 3 Summaries and links | Lead only | The worker brief (worker-brief.txt:17-18) names steps (`/sc:brainstorm`, `/sc:workflow`) and the claim writes `.dev/issues/<N>/issue-summary.md`. Both are files outside `worker-list`; #591 does not make them readable by the observer. |
| 4 Open a session | No | Nothing about deep links. |
| 5 Several workspaces and hosts | Marginal | "One person-opened coordinator owns every watcher-claimed issue on the host" (WORKER-CONTRACT.md:292): per host. No cross-host mechanism, no Coder#477 reference. |
| 6 One trust design | Yes | G2 adds a third local mechanism: a hook rule (no `--to`), an unsigned `.ok` release file written by the coordinator (route A; the signed route B was not chosen, `issue-pipeline-guard-g2.md:24-26`), and hash-bound plan approval rows. None is signed or expiring. See consideration 3. |
| 7 Chat report versus observer | No | WC-16 unchanged. The latency note (GitHub approval waits for the next coordinator wake) affects what a person sees in either surface, not which one comes first. |
| 8 Orchestrator v2 | No | #591 does not mention #423 or a catalogue. |
| 9 Watcher-started sessions | Yes | The issue text says a watcher-launched session "is an ordinary session to the sweep". After #591 that session only claims and ends; the worker is started by the coordinator. See consideration 1. |
| 10 "Management server" | No | Not mentioned. |

- **Acceptance criteria:** none becomes stale or newly answerable. "Keep collection deterministic and bounded, without a default LLM polling loop" is unaffected (the coordinator, not the observer, polls). The criterion "does not infer ... admission from insufficient evidence" is reinforced: approval now has a defined process the observer cannot see.
- **Stale text in the issue body** (not criteria): the diagram arrow "issue watcher ... --starts a claim session--> project's orchestrator" and the related-issues sentence about #394 ("the watcher starts `/sc:issue --claim <N>` sessions, so the two may need to agree on launch level"). Both are now more specific; see considerations 1 and 4.
- **Plan items:** item 5 "Alongside, owned elsewhere: issue-watcher rollout (#450)" now has a precondition (a running coordinator, see (f)).

## (e) Visual-parity work

- **Nothing new to show or style.** #591 adds no Orca field. Approval, plan state and adoption state have no source, so they stay `unavailable (no source)` (`rendering-rules.md:71`); do not add an approval or plan column, colour or badge to match the mockups.
- **One rendering constraint worth testing.** A plan ask's question text can contain a 64-character hex hash and a file list. The observer cuts text at 400 characters with `...` (`adapter-contract.md:41`). How an 80-column frame renders a long unbroken hex token has not been checked by me (UNVERIFIED); it is cheap to add one fixture question carrying such a token when the visual-parity work touches the Decision Desk block.
- **Mockup cells that imply approval or review state** (the issue's ten per-session dimensions include Approval, Result and Tests/review) must keep showing the "no source" state; #591 does not supply one.

## (f) Overlap and conflict risks (#339, #450, Coder#477)

#591's own text (PR body, changed docs, WORKER-CONTRACT edits) does not mention #409, #339, #450 or Coder#477. The links below are mine, from what #591 touches.

- **#339 (sweep, WC-16):** #591 adds "Issue pipeline duties" directly after the WC-16 paragraph (WORKER-CONTRACT.md:289-291) and leaves WC-16 as it was. The sweep reads `worktree ps` (`cli/sweep/probes.py:58-59,1309-1340`); how it classifies an issue worktree that has an empty `agents` list is UNVERIFIED. No conflict seen. The sweep does not read adoption or approval rows.
- **#450 (watcher rollout):** direct. The prompt now ends in `--pipeline none`; the runbook says a coordinator must be running before the cron entry is installed and before any issue is approved (`issue-watcher-setup.md`, new paragraph at section 6). The PR body warns the prompt switch must not merge before a running coordinator carries the Task 9 duties. The first live test record `docs/designs/issue-pipeline-fu1.md` exists on origin/master (checked by path only; not read).
- **Coder#477 (listener, routing):** not touched. #591's approval path stays inside Orca (`ask` and `reply`) plus GitHub reads; no new channel between workspaces. The sentence "the same approval could also be given inside Orca through the coordinator session or the TUI dashboard" in `docs/designs/issue-watcher.md` is unchanged context in the PR diff, but it is relevant: it names a TUI dashboard as a possible approval surface, which conflicts with this issue's Out of Scope ("approving ... instructing workers").
- **#394 (launch-level hook):** touched. #591 changes the launch-level guard and `docs/designs/sc-issue-launch-level-hook.md`; the issue body's sentence that the two "may need to agree on launch level" is now answered for the watcher path (claim at `none`; a coordinator-started worker is bound by the guard only if its brief carries the marker, and the first test issue runs unbound by owner decision Q34, `issue-watcher.md`).

## Additional considerations for #409

1. **Item 9 and the diagram: the watcher's claim session is no longer the long-lived session.**
   - Evidence: `launch.py:33`; `commands/issue.md` new paragraph; `issue-watcher.md` D2 "claim-only again, with a coordinator handoff".
   - Touches: "How the pieces fit" diagram, alignment item 9, Related Issues (#394, #450).
   - Suggested wording: "Since #591 the watcher's claim session ends after its comments (`--pipeline none`); a coordinator creates the worktree and starts the worker with `worker-start`. The observer sees the worker only once it is a `worker-list` row; the claim session, the reserved/uncertain gap and the adoption and approval rows are not visible through `worker-list`. Whether to show watcher or coordinator-adoption state (item 9) is still open, and would need a source other than `worker-list`."

2. **Item 2: a plan-approval question is answered by a hash-bound process, not a free reply.**
   - Evidence: WORKER-CONTRACT.md:59 (WC-17) and :298 (reply `approved <record-id> plan-sha256=<hash>` after the approval row); `write-back-future-stage.md:38`.
   - Touches: alignment item 2, Out of Scope, the future write-back stage.
   - Suggested wording: "A coordinator question that is a plan approval (WC-17) must be answered by the coordinator after it writes the approval row; a raw `orca orchestration reply` typed by a person would bypass that record. If the observer ever prints a reply command, it must not do so for plan-approval questions. For now it prints none, and question text stays on screen only."

3. **Item 6: a third trust mechanism has arrived, and it is local and unsigned.**
   - Evidence: guard rule at launch-level-guard.sh:489-527 (no `--to`); `release.py:30-66` (`.ok` file, route A); `issue-pipeline-guard-g2.md:22-26` (route B signed approval not chosen).
   - Touches: alignment item 6.
   - Suggested wording: "#591 adds a local, unsigned release file (`sessions/<id>.ok`) and a hook rule that a bound worker may only message its own coordinator (no `--to`). Item 6 should compare this with the Coder#477 and #339 trust proposals before one design is chosen."

4. **The #394 sentence is answered in part.**
   - Evidence: `issue-watcher.md` D2 paragraph (Q34, G1/G2); `sc-issue-launch-level-hook.md` edit.
   - Touches: Related Issues, #394 line.
   - Suggested wording: "#394 and the watcher now agree as follows: the watcher claims at `--pipeline none`, and a coordinator-started worker is bound by the launch-level guard only when its brief carries a launch marker (the one first test issue runs unbound by owner decision Q34)."

5. **Approval latency can make an open question look stale to a person.**
   - Evidence: owner Q36 in `issue-watcher.md` D2 paragraph; observer never closes questions (`adapter-contract.md:60`).
   - Touches: R2 question panel wording, alignment item 7.
   - Suggested wording: "A plan-approval question can still be listed as open after the person approved on GitHub, until the coordinator's next wake. The observer lists it without a closure claim, which is correct; do not add an 'approved' or 'answered' mark without a source."

6. **Observer hardening, optional: name the new write verbs in the forbidden set.**
   - Evidence: `adapter.py:34-50` names `send`, `ask`, `reply`, `run-use`; `worker-start` and `worktree create` are rejected only by the allow-list (`adapter.py:153-154`).
   - Touches: `adapter-contract.md` "Forbidden set"; the "no operational controls" criterion.
   - Suggested wording: "The adapter refuses `worker-start`, `worktree create` and `release-worker` because they match none of the three argv templates; if the forbidden set is meant to document every write verb the neighbouring flows use, add them. No behaviour changes." (Low priority; the "set only grows" rule applies if it is done.)

7. **Do not run the observer inside a bound worker session.**
   - Evidence: guard orca arm (guard diff): `orchestration check` allowed, `worker-list` not, for a bound session.
   - Touches: run instructions and the observer's help text.
   - Suggested wording: "Run the observer from a person's terminal or the coordinator's own session, not from a worker bound by the launch-level guard; the guard blocks `orchestration worker-list` for bound sessions."

8. **Visual-parity test fixture for plan-ask text.**
   - Evidence: WC-17 step 2 (plan path, file list, hash in the ask); 400-character cut (`adapter-contract.md:41`).
   - Touches: the visual-parity sub-issue, Decision Desk block at 80 columns.
   - Suggested wording: "Add one fixture question whose text holds a 64-character hex token and several file paths, and check the 80-column frame wraps or cuts it without breaking the layout."

## UNVERIFIED

- That a worker's plan-approval `ask` is stored as type `question` and so appears in the observer's question read (Q-3 in `unverified-register.md:49`; I did not read a plan ask).
- That plan asks carry sender `dispatch:<id>` equal to payload `dispatchId` (I read no plan ask).
- Whether the coordinator's Run that receives these asks is the Run named in the owner record.
- Whether the watcher-launched claim session (started by `orca agent launch`) appears in `worker-list` (assumed not).
- Whether a worktree with an empty `agents` list shows in `worker-list` (assumed not) and how the sweep classifies it.
- Where the approvals directory lives on a host (it is an argument; no fixed path read) and whether the observer could ever read it (it must not under the current contract).
- The G2 note's own open facts: how the coordinator reads a worker's session id; that `--to` and `--from` reach the guard; that an omitted `--to` reaches the coordinator for every verb (`issue-pipeline-guard-g2.md:38-43`).
- Whether the PR's reported test counts (4265 and 4554 passed) hold; I ran nothing.
- Whether the watcher is enabled on any host (`issue-watcher-setup.md` says disabled until the live test passes; no host state read).
- The content of `docs/designs/issue-pipeline-fu1.md` (existence only).
- How an 80-column frame renders a long unbroken hex token (not tested).
