<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (OURS) -->
<!-- Merge date: 2026-11-20 -->

# D04 unified position: claim level and grants

<!-- Source: Base (original, modified): title and question kept from Variant A, status line added so the merged text does not hide non-convergence (Change 9) -->
Question: should the watcher claim at level none with a standing `grants` list, or should the Pipeline field pick the launch level with one grant row per issue?

Status: the debate did not converge (78.9%, threshold 80%), and the invariant probe blocks convergence on five HIGH items. "D:N" means line N of `docs/designs/orchestrator.md` (Clay's design).

<!-- Source: Base (original, modified): Claim replaced per Change 1 (live rule from Variant B Claim and Cited fact 1; Pipeline field kept from Variant A as the gate-open selector); last sentence per Change 3 -->
## Claim

Live rule, stated as a test: the watcher or orchestrator claims only at `--pipeline none` and then starts one supervised `worker-start` worker. The Pipeline field is not read while governed levels are not allowed. The check is that the watcher prompt matches `^/sc:issue --claim N --pipeline none$` (`PROMPT_PATTERN`, master `src/superclaude/cli/issue_watch/launch.py:33`; `commands/issue.md:48`).

The gate-open design stays named: when the owner later opens the gate, the Pipeline field (None, Worktree, Full, Full Submit) picks the launch level per issue (R25, requirements.md line 51, 2026-11-19). That is a later owner decision. It amends R9 (`docs/designs/orchestrator.md:81`, "never used") and the K4 test (D:1226) together.

<!-- Source: Base (original, modified): Mechanism rebuilt. Items 1 and 2 merged from Variant B Mechanism 1 and 2 per Change 2; item 3 merged from Variant B Mechanism 3, 4, 5 per Change 4 and scoped to what the controls cover; item 4 replaces base Mechanism 5 per Change 5 -->
## Mechanism

1. Claim. Wave 1 runs `Skill sc:issue --claim <N> --pipeline none` in the issue's own checkout (D:544). It assigns, checks accuracy, writes the summary and two comments, creates no worktree and launches no agent.
2. One supervised route. The orchestrator starts the worker with `orca orchestration worker-start` in a worktree of the issue's own repo (wave 4, D:519, 5.3). The worker reports on the Run mailbox (`worker_done`, `ask`, heartbeat), and each message is handled once per id (D:1104). K4 (D:1226) gives a reason that does not depend on the gate: `worker-start` only, and a test fails if the skill launches through `orca_worktree.py launch`.
3. Controls adopted. `answer-check` refuses an answer that was relayed, names another entry, is stale or comes from an unknown source (D:688, N1 at D:758). `E-NO-GRANT` refuses and logs a write outside the list, but only through the orchestrator's own verbs (D:696), so it backs at most 2 of the 6 entries. A closed "may do" list and `refuse(argv)` (5.9, D:736) refuse listed commands whatever the grant says. They limit the orchestrator, not the worker.
4. Gate wording. The orchestrator launches only through `worker-start`. The watcher prompt stays pinned to `--pipeline none` (`launch.py:33`). Any governed level waits for the 12 skipped observations (`tests/hooks/test_launch_level_observations.py`; issue 442, the live observations, is open) and for an owner decision. Do not key the spec or a test to `GOVERNED_LEVELS_ALLOWED`, because master does not have it (INV-001).

<!-- Source: Variant B Mechanism 3 (grants list) merged per Change 3, split using Variant A Cited fact 6 and Decision 8 and Round 2 answers (c) and (d) of both advocates; replaces base Mechanism 4 and the base "one grant row per issue" wording -->
## Grants

Clay's design lists six `grants` entries (D:291, D:872). This position keeps four as standing: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`, `issue.hold`. They are bounded, reversible and about the issue's own text (D:116).

`pr.merge` and `issue.close` are not standing. Contract lines 241, 245 and 300 (`WORKER-CONTRACT.md`) say outward action needs an instruction naming it, pushes need the person's go, and an issue write without that issue's grant row is a "Never". Standing merge and close rest only on ruling R10 (D:71, "Ruling (Clay, 2026-11-18)"), and ADD1 (D:135) admits R10 contradicts lines 239-246. Q38 (owner-answers line 187) says any further issue waits for G2.

Release: per PR and head sha, by a go given in chat and recorded by the agent, accepted by an `answer-check`-style verb with the owner identity as a parameter. The key is `merge_safety:<PR>:<head sha>` (D:598). No file row written by the owner is needed, which fits the owner's chat-only order of 2026-11-17.

<!-- Source: Base (original): Mechanism 1 (flag mapping and board values), Mechanism 2 (level state, fail-closed refusal) and Mechanism 3 (Full Submit push rule), kept per Change 7; the watcher line is Variant B Cited fact 1 -->
## Flag semantics of `/sc:issue --claim`

- Board value to flag: None is `--pipeline none`, Worktree is `--pipeline worktree`, Full is `--pipeline full`, Full Submit is `--pipeline full --submit`. An empty Pipeline means None (R25, line 51). Status picks the command and Pipeline picks how far it goes (R23, line 47).
- `--submit` is allowed only with `--pipeline full` (STOP `E-SUBMIT-NEEDS-FULL`). The second STOP rule is `E-CLAIM-ONLY-FLAG`. Wording: `docs/designs/sc-issue-claim-pipeline-flag.md` lines 69-89.
- The watcher always passes `--pipeline none`. Worktree, Full and Full Submit run only after the gate opens.
- The claim records the level in `~/.claude/state/launch-level/pending/<nonce>`, outside the worktree. The launch-level guard (issue 394, closed 2026-11-17) reads it, and the agent cannot edit it. If the guard is missing the claim refuses with `W-ENFORCEMENT-ABSENT` and starts no agent (same doc, lines 117-135).
- Full Submit commits, pushes a feature branch and runs `/sc:pr-submit --monitor 3`. No level merges (same doc, lines 19-26). Pipeline plus the `Approved` field is the person's go for that one issue's push (R25).

<!-- Source: Base (original, modified): Cited facts 3 and 4 and Costs bullets 2 and 5 corrected per Change 6 (X-002, X-003, C-005); Variant B Cited fact 5 withdrawn for the same Q36 misread -->
## Corrected facts

- X-002: the guard plus a level chosen per issue is "the only control that is built", not "the control that exists today", because no governed level can run today.
- X-003: Q36 (owner-answers line 185) is approval latency. The grant row is Decision 8 (line 130). The "accepted for now" claim about the grant row is removed.
- C-005: the Pipeline field is not the only brake. Per repo there are `enabled` (D:278, D:302) and `max_in_flight` (D:289); per PR, the gate reasons (D:582). None is a per-issue stop after the claim, and `hold:backlog` (D:445) stops only the claim wave.

<!-- Source: Variant B Cited fact 7 and Round 2.5 invariant probe (invariant-probe.md), merged per Change 8 as a new section -->
## Conditions the spec must state

HIGH items (these block convergence; none changes the winner):

- INV-001: key the spec and tests to what master has, the `PROMPT_PATTERN` pin to `--pipeline none` (`launch.py:33`) plus the Wave 8 ship-gate text. `GOVERNED_LEVELS_ALLOWED` exists only in the unpushed worktree `claim-handoff-planb` (`launch.py:48`, R33, `requirements.md:59`).
- INV-002: the standing grants sit in `repos.yaml`, which an agent session can write. D:688 says "ours are inside it and are guarded by the verb and by a test", a rule, not a permission boundary. D:300 has no rule for an absent or malformed `grants` value; the spec must give one.
- INV-003: a `worker-start` worker has no L1 guard, no L2 pre-push hook, and `master` is not protected: "nothing on GitHub stops a worker that ignores its prompt" (D:117). `refuse(argv)` (D:1117) limits the orchestrator, not the worker. The contract rewrite (ADD1, D:135) is still to do. Q34 (owner-answers line 147) and Q38 accepted this for the one test issue only.
- INV-004: `pr.merge` runs as a raw `gh pr merge` (D:588), outside `E-NO-GRANT` (D:696). `merge_safety:<PR>:<head sha>` (D:598) keys only the merge-safety hold, and the thirteen gate reasons (D:582) have no "recorded merge go", so `merge_ok: true` can print with no recorded go. The spec must add that reason.
- INV-012: `ironbelly` is "the one login shared by the owner and every session on this host" (`owner-answers.md:162`), and `answer-check` is hardwired to Clay's terminal or ClickUp id (D:694). A chat go does not prove the owner gave it, so the consensus alone does not make unattended claiming safe.

MEDIUM items (warnings):

- INV-005: an issue reassigned or closed after the claim is freed only at the next hourly check (D:1109); no `unassigned` or `closed` gate reason exists (D:582).
- INV-006: `E-NO-GRANT` covers at most 2 of 6 entries (D:696); cover for `issue.comment` (the R24 result comment) is not shown.
- INV-009: `hold:backlog` is created once per repo by hand (D:445). If absent, no person can place the brake, and it stops the claim wave only.
- INV-010: R36 (`requirements.md:62`) withdrew the value-time check, so a Pipeline raised after approval is blocked only while the gate is closed. Opening the gate removes that protection with no replacement.

<!-- Source: Base (original, modified): new final section per Change 9 (unresolved points C-001, C-002, X-001, A-001 and A-003 from debate-transcript.md and diff-analysis.md) -->
## Open points

| ID | Point | Who must decide |
|----|-------|-----------------|
| C-001, X-001 | Whether R9's "never used" yields to R23 and R25. Q35 (owner-answers line 184) supports none live; R9 and R10 are Clay's rulings, not the repository owner's | The repository owner (`ironbelly`); probably topic D01 |
| C-002 | Whether a second launch route (a launched agent reporting through `result.md`) is ever wanted | The owner, at the gate-open decision |
| A-001 | Which signal is the consent for a claim: assignment, the `Approved` field or a label | Topic D01 |
| A-003 | Who "the owner" is: `ironbelly` in one paper, Clay in the other, one shared login (owner-answers line 162) | The owner, with topics D06 and D16 |

Also for `ironbelly`: confirm R10 against ADD1 and G2 before `pr.merge` or `issue.close` can become standing.
