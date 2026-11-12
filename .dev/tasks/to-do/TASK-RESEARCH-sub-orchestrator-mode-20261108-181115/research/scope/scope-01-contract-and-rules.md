# Scope 01: Worker contract and ownership rules
**Scope:** src/superclaude/core/WORKER-CONTRACT.md, src/superclaude/core/CLAUDE.md, repo-root CLAUDE.md, developer-guide section 7.7, ccsession-tag README (#449 mention)
**Status:** Complete
**Date:** 2026-11-08
---

Source for everything below: `src/superclaude/core/WORKER-CONTRACT.md` (328 lines as read; the task brief said 327) unless another file is named. Paths are relative to the repo root. All line numbers were taken from a Read made in this session.

## 1. WORKER-CONTRACT.md: rule inventory

The file is not ordered by rule number. Section 2 ("Command-side rules", lines 27-47) holds WC-2, 4, 8, 9, 10, 11. Section 3 ("Worker-session duties", lines 49-65) holds WC-3, 5, 7, 12, 13, 14, 15 and an unnumbered "Heartbeats" bullet. Section 4 ("Coordinator rules", from line 67) holds WC-6 as a heading (line 71) plus many unnumbered rules. There is no WC-1 in the file. Decisions D1-D5 are cited but defined elsewhere (see Gaps).

| Rule | Line | Binds | What it forbids or requires | Touches |
|---|---|---|---|---|
| WC-2 | 31 | command, under `--unattended` | No `AskUserQuestion`, no chat question, no STOP AND WAIT; each gate resolves as default, caller flag, or `blocked` | reporting (blocked) |
| WC-4 | 32-39 | command | Writes `<report-dir>/return-contract.yaml` on every outcome; exactly one report directory; `worker_status` in succeeded/partial/failed/blocked | reporting |
| WC-8 | 40 | command | No `worker-start`, `dispatch`, `task-create` from inside a command | fan-out |
| WC-9 | 41-45 | command and worker | Every outward action off; local commit only by grant (user's words quoted, own child worktree, status succeeded); worker never runs `git add`, commit, push otherwise | commits, reporting |
| WC-10 | 46 | command, coordinator | Blocking Bash calls at most 4 minutes; late heartbeat is absence, never death | liveness |
| WC-11 | 47 | command, coordinator | Two workers in one worktree never write the same file; own child worktree needed when commits granted, or `/sc:implement` plus another writer, or parallel experiment | worktree creation |
| WC-3 | 53-58 | worker session | Blocked gate: report blocked, or ask coordinator at most once per Task; Ruling halts never asked | reporting, questions |
| WC-5 | 59 | worker session | `worker_done` exactly once from top-level session; outcome mapping | reporting |
| WC-7 | 60 | worker session | Run command at top level, never inside a subagent; only the top-level session sends lifecycle messages | agent launch (subagents), reporting |
| WC-12 | 61 | worker session | Pull coordinator follow-ups with `check`; ack every answer; stop on `consumer_fenced` | reporting |
| WC-13 | 62 | worker session | No Orca fan-out from the worker session (quoted below) | fan-out, worktree creation, agent launch, depth |
| WC-14 | 63 | worker session | No turn ends between chain steps; only exception is the S6 handoff interrupt | liveness |
| WC-15 | 64 | worker session | Read in pieces of 80 lines or less; write `<report-dir>/handoff/<n>-<command>.md` after each command | reporting, liveness |
| WC-6 | 71-79 | coordinator | Every retry is a new Task (`task-create --spec`), never `worker-start --retry-of` | fan-out (coordinator side) |

Unnumbered rules relevant to a sub-orchestrator (all in section 1 or 4): worker run definition (line 11), brief guard (16-22), never-as-worker list (23), nested propagation rule (24-25), brief contents (83-91), liveness supervision S0-S11 and ladder L0-L5 (95-165), "Never on silence" (182-192), brief layout (202-216), feature worktree and child worktrees (218-225), git and GitHub ownership (227-235), reading a result (237-246), `/sc:implement` freeze (248-269), fan-in rule (271-273).

Tag: [CODE-VERIFIED] (the file is the real source for itself). Test pinning: `tests/skills/test_worker_contract.py:155` pins WC-13 by the phrase "No Orca fan-out from the worker session" [CODE-VERIFIED]; the test file also pins `worker-start --worktree new-child --base-branch <feature branch>` (line 267) and the `--retry-of` ban (line 185), so edits to those rules need test edits.

## 2. Exact wording: WC-13, WC-8 and the coordinator definition

**WC-13** (WORKER-CONTRACT.md:62) [CODE-VERIFIED]:

> **WC-13. No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. Work it finds that needs another worker is stated in its `worker_done` body; the coordinator decides (section 4).

Reading notes:
- It binds the session that carries a live Orca preamble (the "worker run", line 11), not a command and not an ordinary session.
- "at any depth setting" means that raising Orca's `nestedWorkerMaxDepth` would not lift WC-13. The only exit path is the `worker_done` body, then the coordinator's decision.
- The forbidden list closes three doors: Orca orchestration verbs, low-level dispatch, and the two `orca-cli` paths that start a session (`worktree create --agent`, `agent launch`). A sub-orchestrator in a worktree needs exactly these.

**WC-8** (WORKER-CONTRACT.md:40) [CODE-VERIFIED]:

> **WC-8. No Orca fan-out from inside a command.** A command never calls `worker-start`, `dispatch` or `task-create`. Fan-out that needs Orca records is split into separate Tasks by the coordinator.

Reading notes:
- WC-8 binds the command file (what `/sc:` commands may contain), WC-13 binds the session running it. Both are needed because a command could otherwise start workers on its own and a worker session could do so by hand.
- WC-8's list has three verbs; WC-13's list has the same three plus low-level dispatch, `worktree create --agent` and `agent launch`. WC-8 does not mention worktree or agent launch. So a proposed `/sc:orchestrator` command that calls `orca worktree create --agent` or `agent launch` is not literally barred by WC-8, but it is barred by WC-13 if run in a worker session, and by the contract's opening (line 5: "Commands themselves contain no Orca calls") in any case.
- Line 5 [CODE-VERIFIED]: "Each `/sc:` command stays a self-contained unit of work: one worker (a top-level Claude session in its own Orca terminal) runs one command and reports it with `worker_done`. Commands themselves contain no Orca calls." A new `/sc:orchestrator` command whose body issues Orca calls would break this sentence, independent of WC-8.

**Coordinator definition** (WORKER-CONTRACT.md:67-69, section 4 opening) [CODE-VERIFIED]:

> ## 4. Coordinator rules
>
> These bind the coordinator: an Orca coordinator session the person opened. It plans, creates Tasks, starts workers, reads their reports and performs every outward action.

Related coordinator statements:
- Line 5: "A coordinator plans the work, creates Tasks, starts one worker per Task and reads each worker's report."
- Line 220: "Each feature has one feature worktree on its feature branch, where the coordinator runs." (singular coordinator per feature worktree)
- Line 246: "The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text."
- Line 229: "The coordinator performs every git and GitHub outward action ... only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation."
- There is no sentence in the file that defines "orchestrator", "sub-orchestrator" or "coordinator under another orchestrator". Grep for "orchestrator" in the file returns no definition (the word does not appear in the 328 lines as read; the rules say "coordinator" throughout). [CODE-VERIFIED by reading the whole file]

**Worker run definition** (WORKER-CONTRACT.md:11) [CODE-VERIFIED]:

> **Worker run**: a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages; a session the user started, inside or outside Orca, is an ordinary session.

Consequence: a session started by `worktree create --agent --prompt` or `agent launch` gets no Task/Dispatch preamble, so by this definition it is an "ordinary session" and cannot send `heartbeat`, `ask`, `check` or `worker_done`. The contract has no upward reporting channel for such a session.

Grep check, whole contract for "rchestrat": only two hits, both the CLI noun `orca orchestration` (lines 101, 197). The role words "orchestrator" and "sub-orchestrator" appear nowhere in WORKER-CONTRACT.md [CODE-VERIFIED].

## 3. Other contract passages that bear on a nested session

- Line 12 (decision D1): mode is selected only by `--unattended`; "No command detects Orca, its preamble or its environment." A sub-orchestrator mode flag (`--sub`) would be a second, Orca-aware switch, so it would need either an exemption or its own decision. [CODE-VERIFIED]
- Line 23, never-as-worker list: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:issue`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`, plus `/sc:pr-submit` while D3 holds. "The list changes only when the coordinator-only command set or D3 changes." So a coordinator-only command set already exists as a concept; a new `/sc:orchestrator` would have to join the never-as-worker list (and `NEVER_AS_WORKER` at `tests/skills/test_worker_contract.py:382`), or the list's rule. [CODE-VERIFIED: tuple starts at test line 382]
- Line 24-25, nested propagation: concerns a command invoking another command in the same session (Skill or Agent tool). It is not Orca nesting. [CODE-VERIFIED]
- Lines 83-91, what the brief carries: command line, report dir, blocked-gate policy, local commit grant, outward actions "none", worktree placement. No field for "this worker may run its own workers", and none for "you report to orchestrator X, not coordinator Y". [CODE-VERIFIED]
- Line 91 and 221: child worktrees are created by the coordinator with `worker-start --worktree new-child --base-branch <feature branch>`, `--setup skip` by default. This is the only sanctioned way to make a worktree under the contract. [CODE-VERIFIED]
- Line 103-106 and 200: one `check --wait` per Run inbox; Delivery is a shared FIFO batch; `worker_done`, `question`, `escalation`, `handoff`, `merge_ready` are checked against the sender's current Task ID and Dispatch ID and a mismatch is quarantined. Line 200 lists "whether two consumers on one mailbox both get a batch" as UNVERIFIED, and "the coordinator runs one wait per Run inbox". A second-level coordinator that also waits on a mailbox runs straight into this open point. [CODE-VERIFIED as stated text; the Orca behavior itself is UNVERIFIED in the contract]
- Line 246: the coordinator records "each follow-up Task it created because a worker's result showed work that could not be planned before dispatch, with the extra time that cost. This is the evidence decision D5's revisit trigger reads." So D5 has a revisit trigger fed by the coordinator's run notes: the cost of replanning because a worker cannot start sub-workers. [CODE-VERIFIED]
- Line 63 / 124 (WC-14 and S6): a handoff interrupt is the only allowed way for a worker to end its turn without `worker_done`. [CODE-VERIFIED]
- Line 230: all outward actions target `IronbellyOrg/IronClaude`, "never through Orca's issue or PR linking while Orca records the project as the upstream." A sub-orchestrator would inherit this. [CODE-VERIFIED]

## 4. Worktree/agent ownership rule added by PR #449

PR #449 is the commit `24d79b7f feat(orca): require an agent on every worktree create (#449)` seen in the session's recent-commit list [UNVERIFIED beyond that list; I did not run git log or open the PR].

### 4a. src/superclaude/core/CLAUDE.md lines 55-59 [CODE-VERIFIED, Read via the system-reminder copy plus Grep line numbers 55, 58, 59]

> Every Orca worktree gets an agent: create it with `worktree create --agent` (supervised workers
> use `worker-start`, and a supervised worker follows its worker contract, which forbids it from
> creating worktrees), and never create a worktree for your own use. The session that creates a
> worktree becomes its orchestrator, or a coordinator under another orchestrator, and
> owns its agent(s). A hook blocks `orca worktree create` without `--agent`.

The paragraph sits under "### Orca session launches" (heading at line 45; the preceding paragraph ends at line 53 with "this rule does not replace supervised dispatch or commands' internal Agent-tool subagents."; next heading `## Key Docs` at line 61). [CODE-VERIFIED by Grep]

### 4b. Repo-root CLAUDE.md line 312 [CODE-VERIFIED by Read of line 312]

> - **Every worktree gets an agent, and its creator owns it.** Because every worktree gets an agent, a bare `orca worktree create` is wrong: always pass `--agent claude --prompt "<task>"`, and never create a worktree for your own use. The session that creates a worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns its agent(s). A worktree a human creates needs an agent too. Supervised workers are started with `orca orchestration worker-start`, which already creates their worktree with an agent. A PreToolUse hook (`require-orca-worktree-agent.sh`) blocks a Bash call that runs `orca worktree create` without `--agent` once it is installed; the other parts of this rule are instructions only.

Lines 309-311 (same section, "Parallel Development with Git Worktrees") give the creation recipe: `orca worktree create --name <name> --agent claude --prompt "<task>"`, with `--repo`, `--base-branch`, and "`--parent-worktree <selector>` or `--no-parent` as needed". Line 313 bans raw `git worktree add`. Line 315 bans Orca link flags `--issue`, `--pr`. [CODE-VERIFIED for 309-311 via Grep context; 313 and 315 via Grep context]

Note: `--parent-worktree` / `--no-parent` is Orca's own worktree-parent concept. That is a worktree lineage link in Orca's data model, separate from any contract-level sub-orchestrator. [UNVERIFIED what Orca does with a parent worktree beyond this repo text]

### 4c. Hook message (src/superclaude/hooks/scripts/require-orca-worktree-agent.sh:351-356) [CODE-VERIFIED by Read]

```text
ORCA WORKTREE BLOCK: every Orca worktree gets an agent, and this command runs `orca worktree create` without `--agent`.
Use: orca worktree create --name <name> --agent claude --prompt "<task>"
The session that creates the worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns that agent.
Supervised workers use `orca orchestration worker-start`.
```

The same sentence is mirrored at `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh:354` [CODE-VERIFIED by Grep].

### 4d. Tests that pin the wording

- `tests/core/test_orca_session_launch_guidance.py:30,32,49` require the phrases "Every Orca worktree gets an agent" and "owns its agent" and that a paragraph starts with the first. [CODE-VERIFIED by Grep]
- `tests/hooks/test_require_orca_worktree_agent.py:35-36` pins the hook text "The session that creates the worktree becomes its orchestrator (or a coordinator under another orchestrator) and owns that agent." [CODE-VERIFIED by Grep]
- Neither test checks that "coordinator under another orchestrator" is defined anywhere. Changing the phrase requires edits to the hook in `src/` and `plugins/`, both CLAUDE.md copies, the ccsession-tag README, and two test files.

### 4e. What the #449 text does and does not say

- It says: whoever creates a worktree (with `--agent`) becomes the orchestrator, or "a coordinator under another orchestrator", and owns the agent(s). So it presumes two tiers of creator exist: top orchestrator, and a coordinator beneath one. [CODE-VERIFIED]
- It does not say how a session becomes "a coordinator under another orchestrator", what it may do, what it reports and to whom, or how the "orchestrator" relates to the contract's "coordinator" (section 4). [CODE-VERIFIED by absence in all four locations]
- It says a supervised worker "follows its worker contract, which forbids it from creating worktrees". That is WC-13's `worktree create --agent` clause. [CODE-VERIFIED against WORKER-CONTRACT.md:62]
- "never create a worktree for your own use" plus "owns its agent(s)" means every nested worktree already has an agent session whose owner is its creator. In practice this is a parent/child session tree: orchestrator creates worktree and agent A; if A itself creates a worktree it becomes A's owner. WC-13 forbids that only for A when A is a supervised worker (preamble present). For an A started by `worktree create --agent --prompt` the contract does not apply, as shown in section 2 above.

## 5. Developer guide section 7.7 (docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md, lines 972-1013)

Read lines 955-1014 only. Section 7.7 is "Orca Orchestration: Commands as Workers" (heading line 972).

| Line | Claim | Tag |
|---|---|---|
| 974 | Orca can run IronClaude commands as workers under an Orca coordinator; rules live in `~/.claude/WORKER-CONTRACT.md`; the subsection "summarizes the contract and does not replace it" | [CODE-VERIFIED] file `src/superclaude/core/WORKER-CONTRACT.md` exists and is the source of the installed copy (CLAUDE.md in core says it installs to `~/.claude/`; the contract's line 3 says so) |
| 978 | "A coordinator is a session someone opened by hand, never one that Orca started as a worker. It plans the work, creates one Orca Task per unit of work, starts one worker per Task and reads each worker's report" | [CODE-VERIFIED] against WORKER-CONTRACT.md:69 ("an Orca coordinator session the person opened") and line 5. The words "never one that Orca started as a worker" are the guide's own gloss, not in the contract; the contract only says "the person opened". |
| 979 | "A worker is a top-level Claude session that runs one `/sc:` command and reports it with `worker_done`: one command per worker." | [CODE-VERIFIED] against contract line 5. Note the contract also allows several chained `Command:` lines per Task (lines 204, 289-296, WC-14), so "one command per worker" is narrower than the brief layout. |
| 980 | Commands contain no Orca calls; per rollout plan SA-2 none runs an `orca` or `orca-ide` command | [CODE-VERIFIED] for the contract opening (line 5); SA-2 itself [UNVERIFIED], it lives in the rollout plan under `.dev/orca-command-refactor/`, outside this slice |
| 981 | `/orchestration` skill is a discovery stub; coordinator rules are in section 4 of the contract; HOW-WE-WORK has an "Orca coordination" section | [UNVERIFIED] not checked in this slice (skill file and HOW-WE-WORK section not opened) |
| 985 | "At P0 no command accepts `--unattended` or `--report-dir`, and `UNATTENDED_COMMANDS` in `tests/skills/test_worker_contract.py` is empty." | [CODE-CONTRADICTED] `UNATTENDED_COMMANDS` is `frozenset(UNATTENDED_EXPECT)` at tests/skills/test_worker_contract.py:746, and Grep finds `^## Unattended mode` in 31 files under `src/superclaude/commands/`, which equals the contract's 16 P1 + 15 P2 commands (WORKER-CONTRACT.md:303-304). The guide's rollout-state text is stale. |
| 986 | A command gains `--unattended` in the phase that converts its gates, from P1 on | [CODE-VERIFIED] consistent with 31 converted commands |
| 991 | Never-as-worker list matches the contract | [CODE-VERIFIED] same seven commands plus pr-submit as contract line 23; `NEVER_AS_WORKER` at test line 382 |
| 993 | Adding to the list is an edit of the contract and of `NEVER_AS_WORKER` | [CODE-VERIFIED] consistent with test file existing at that tuple |
| 998-1009 | Summaries of the flag parse rule, person-mode refusal, WC-2, WC-4 (four bullets), WC-8, WC-9, WC-10, WC-11, nested propagation | [CODE-VERIFIED] each matches the contract text at lines 13, 14, 31, 15/32-39, 40, 41, 46, 47, 24 |
| 1011-1013 | WC-7 is a duty of the worker session | [CODE-VERIFIED] contract line 60 |

What 7.7 does not say: Grep for `WC-13|WC-12|WC-14|WC-15|sub-orchestrator|coordinator under` in the whole guide returns zero matches. So the guide, as written for people authoring commands, never mentions WC-13 (worker may not start workers), the pull-style follow-ups, the chain rule or the handoff files, and has nothing on a coordinator under another orchestrator. [CODE-VERIFIED by Grep count 0]

The guide's "coordinator vs worker" model is two-tier and flat: coordinator (person-opened) starts workers; worker runs one command; no third role.

## 6. ccsession-tag README (src/superclaude/skills/ccsession-tag/README.md)

Lines 228-243 [CODE-VERIFIED by Read]. Heading "### Orca session launches" at 228. Lines 230-237 are the launch paragraph (adds one sentence the core CLAUDE.md lacks: "This requires the `ccsession-orca` Claude command configuration above; choosing an agent does not configure ccsession automatically."). Lines 239-243 are the #449 paragraph, word for word the same as core CLAUDE.md:55-59:

> Every Orca worktree gets an agent: create it with `worktree create --agent` (supervised workers
> use `worker-start`, and a supervised worker follows its worker contract, which forbids it from
> creating worktrees), and never create a worktree for your own use. The session that creates a
> worktree becomes its orchestrator, or a coordinator under another orchestrator, and
> owns its agent(s). A hook blocks `orca worktree create` without `--agent`.

Line 242 holds "worktree becomes its orchestrator, or a coordinator under another orchestrator, and" (the "line 242" the brief pointed at). The README adds no definition of the phrase. A "The one question rule" section starts at line 245; it concerns ccsession's session-name prompt. [CODE-VERIFIED]

Relevance: the ccsession-orca launch path is how a session created by `worktree create --agent` gets a session name; any sub-orchestrator launched this way carries a ccsession-backed name (the README is about that). I did not read the rest of the README, so how ccsession names a nested session is [UNVERIFIED].

## 7. Pointers to D5 (outside this slice, grep hits only)

D5 is not defined in WORKER-CONTRACT.md; the contract only cites it (line 246) and implies it in WC-13 ("at any depth setting", line 62). Grep over the repo found its records under `.dev/orca-command-refactor/decisions/D5/` (RECOMMENDATION.md, debate/adversarial/merged-output.md, base-selection.md, diff-analysis.md). Hits I saw, not opened in full:
- `.dev/orca-command-refactor/decisions/APPROVED.md:12`: "D5 | Option (a): keep nesting depth 1; corrected reasons; coordinator is a person-opened session; WC-13; AC-0.7; AC-C6" [UNVERIFIED beyond the grep line]. This is where "person-opened" and WC-13 were decided together.
- `.dev/orca-command-refactor/decisions/D5/debate/adversarial/merged-output.md:220`: the question "Should Orca's nesting depth be raised so that a worker could start its own Orca workers?" and line 122: "Nesting depth stays 1 unless the user decides otherwise, and the coordinator is a session the person opened, never one started by `worker-start` (D5)".
- Same file line 117: "Raising the depth would not make this design viable: R2-R5 still apply, and depth cannot reach a command's Agent-tool fan-out (D5)."
- Same file line 167: AC-C6 requires every Orca profile to print `"nestedWorkerMaxDepth":1`; any other value fails the phase until the person confirms D5 changed.
- `.dev/orca-command-refactor/review/issue-326-evaluation.md:80`: "Orca's depth-1 limit only stops workers from starting workers" (cites `SPEC:351`). This is a significant nuance: depth-1 limits worker-started workers, not session creation by `worktree create --agent`.
- `.dev/orca-command-refactor/decisions/D2/RECOMMENDATION.md:136`: D5 agrees "no worker starts a worker".
The sibling scope researchers should cover these in full; this slice only flags that "coordinator is a person-opened session" was a D5 outcome, so a sub-orchestrator that a coordinator (not the person) opens contradicts the D5 wording unless D5 is revisited or the new role is defined as something other than "the coordinator".

---

## Gaps and Questions

1. **"Coordinator under another orchestrator" is named but never defined** (core/CLAUDE.md:58, root CLAUDE.md:312, ccsession-tag README:242, hook line 354, pinned by two test files). WORKER-CONTRACT.md never uses the role word "orchestrator" (grep: zero). It defines only "coordinator" (line 69) and says the coordinator is "a session the person opened". Two vocabularies, one tier of definition. [GAP]
2. **Direct conflict in wording:** #449 admits a coordinator that sits under another orchestrator, but a session opened by an orchestrator is not "a session the person opened" (contract line 69; dev guide line 978; D5 outcome in APPROVED.md:12). Either the sub-coordinator is not a "coordinator" in the contract's sense, or section 4 line 69 needs to change. [CONFLICT]
3. **Reporting channel is undefined.** By line 11 only a session with a Task/Dispatch preamble may send `heartbeat`, `ask`, `check`, `worker_done`. A session started by `worktree create --agent --prompt` has none, so it is an "ordinary session" and the contract gives it no way to take orders from or report to an orchestrator. Possible routes (mailbox, `worker-start` of the sub-orchestrator itself, plain terminal messages) are not described anywhere in this slice. [GAP]
4. **If the sub-orchestrator is a worker (started with `worker-start`), WC-13 forbids it from starting anything, and section 4 forbids workers from acting as coordinators.** If it is not a worker (started with `worktree create --agent`), no contract rule governs it at all: WC-13, WC-5, WC-12, the brief guard and the liveness ladder all assume a preamble. So no existing role fits. [CONFLICT / GAP]
5. **WC-8 vs WC-13 have different forbidden lists.** WC-8 (command) lists three verbs; WC-13 (worker session) lists those plus low-level dispatch, `worktree create --agent` and `agent launch`. A command that creates worktrees or launches agents is not caught by WC-8's text, only by the opening sentence (line 5, "Commands themselves contain no Orca calls") and by WC-13 when run in a worker. A new `/sc:orchestrator` command that calls Orca verbs contradicts line 5 outright. [GAP / CONFLICT]
6. **D1 says no command detects Orca or its environment** (line 12). A `--sub` flag that changes behaviour for a nested role would be a second mode switch; the contract states that `--unattended` is the only command-side change besides report files and resume (line 12). [CONFLICT with D1 unless addressed]
7. **Single-coordinator assumptions.** Line 220 "where the coordinator runs", line 200 "one wait per Run inbox", line 246 "starts only Tasks it created itself", line 229 "performs every git and GitHub outward action" all assume one coordinator per feature worktree/Run. A sub-orchestrator inside a child worktree would need answers for: who owns the inbox, who may push, who merges the child back (line 224 says the coordinator merges). Line 200's "two consumers on one mailbox" is an open UNVERIFIED point. [GAP]
8. **Ownership of outward actions** (lines 229-235) requires the user's instruction in the coordinator's own conversation. A sub-orchestrator has no user conversation; it would need either a delegated instruction quoted in its brief (like the WC-9 commit grant, line 42) or a ban. The contract has a precedent for quoted grants (WC-9, D4) but only for local commits. [GAP]
9. **Dev guide section 7.7 is stale at line 985** ("At P0 no command accepts `--unattended` ... `UNATTENDED_COMMANDS` ... is empty") [CODE-CONTRADICTED: 31 converted commands, `UNATTENDED_COMMANDS = frozenset(UNATTENDED_EXPECT)` at test line 746]. It also omits WC-12/13/14/15 entirely [CODE-VERIFIED by zero grep hits]. Any sub-orchestrator work that updates the guide should fix both.
10. **Not verified in this slice:** the PR #449 diff itself and its description (I relied on the commit title and on the current file text); the `/orchestration` skill stub; HOW-WE-WORK "Orca coordination" section (line 981 claim [UNVERIFIED]); whether Orca applies `nestedWorkerMaxDepth` to `agent launch` / `worktree create --agent` or only to `worker-start` (the issue-326 evaluation line suggests the latter, grep hit only); what `--parent-worktree` means to Orca.
11. **Brief says WORKER-CONTRACT.md is 327 lines; Read showed 328.** Minor; the file may have gained a line since the brief was written.

## Key Takeaways

- WC-13 (WORKER-CONTRACT.md:62) is wider than a depth limit: it names `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent` and `agent launch`, "at any depth setting". Raising Orca's depth would not unlock sub-orchestration; WC-13 would have to be amended, or the sub-orchestrator would have to be a non-worker.
- WC-8 (line 40) is narrower and binds commands; line 5 ("Commands themselves contain no Orca calls") is the stronger barrier against putting Orca calls inside a new `/sc:orchestrator` command.
- The contract's only coordinator is "an Orca coordinator session the person opened" (line 69). #449's phrase "a coordinator under another orchestrator" (core/CLAUDE.md:58, root CLAUDE.md:312, README:242, hook:354) is an undefined, test-pinned reference to a role the contract does not have.
- A session created with `worktree create --agent` has no Task/Dispatch preamble, so under line 11 it is an ordinary session: not bound by WC-13, but also with no sanctioned upward reporting. This is the central structural gap for a `--sub` mode.
- Existing precedents to reuse: the quoted-grant pattern (WC-9/D4), the brief template and `Command:` layout (lines 202-216, 283-305), the never-as-worker list for coordinator-only commands (line 23), and the D5 revisit trigger recorded by the coordinator (line 246).
- Changing the #449 wording is a multi-file edit: hook (src and plugins mirror), two CLAUDE.md files, the ccsession-tag README, and two test files pin it.
- Dev guide 7.7 is stale on rollout state (line 985) and silent on WC-13.

## Summary

WORKER-CONTRACT.md forbids a worker session from starting any further session or worker (WC-13, "at any depth setting") and forbids commands from containing Orca calls (opening line, WC-8), while defining the only coordinator as a session the person opened (line 69). PR #449's text in the two CLAUDE.md files, the ccsession-tag README and the worktree hook says that a session creating a worktree becomes "its orchestrator, or a coordinator under another orchestrator", but no file in this slice defines that second role, and the contract never uses the word "orchestrator". A sub-orchestrator started with `worktree create --agent` falls outside the contract entirely (no preamble, so an ordinary session, no reporting channel); one started with `worker-start` is bound by WC-13. The contract also assumes one coordinator per feature worktree and per Run inbox. Developer guide section 7.7 is two-tier, silent on WC-13, and stale on the rollout state.
