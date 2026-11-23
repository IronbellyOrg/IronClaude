# Comparison: the zero-setup watcher (merged, PR 707) against the orchestrator design of issue 655

Date: 2026-11-21. Status: DECIDED by the owner on 2026-11-21 (requirement R38): the merged watcher is the design and none of Clay's suggestions is adopted. The recommendations below that adopt Clay's parts (plan check, automation, wake file, merge gate, living report and the rest) are therefore void; the "Merged (owner)" column is what stands. Follow-up on 2026-11-23: the decision note was posted on issue 655, the hold on Coder issues 515 and 516 was lifted, Clay's draft PRs 686 and 690 were closed (branches kept), and issue 655 was closed as not planned. Its not-covered features are tracked in issues 716, 717 and 718; `/sc:issue --plan` (PR 690) is not planned. Nothing in this file is built.
Purpose: Clay's note of 2026-11-20 20:43 UTC on issue 655 holds the Coder builds (issues 515 cron and 516 coordinator) until the two designs are compared. This is that comparison, with a recommendation per difference.

## What was read (and what was not)

- Merged side: master `2ea524514` (PR 707, requirements R1 to R37 in `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md`, built code in `src/superclaude/cli/issue_watch/` and `issue_pipeline/`).
- Clay's side: the design `docs/designs/orchestrator.md` on branch `clayphi/archive-orchestrator-655-20261120` (1412 lines; sections 1.1, 1.4, 2.1 DQ1 to DQ13, 4.1 to 4.5, 4.10, 5.7, 7.2, 7.3 read in full) and issue 655 with its newest comment. Clay says the design is unfinished and was written without the owner's requirements file.
- The owner's earlier answer to Clay's work: the unification spec `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/spec/SPEC.md` (43 decisions, written before PR 700 and PR 707; section 2 and 3.1 read). Its rows are recommendations the owner has not ruled on in chat.
- Not read: Clay's poll code (PR 686), his skill branches, the 26 contradictions in the unification spec's DECISIONS.md. Nothing was run against either design except one read-only check (below).

## The two flows in one paragraph each

**Merged (owner).** A cron entry runs one dispatcher (`superclaude issue-watch run-all`) every 5 minutes. For each Orca repo it runs a read-only poll. An issue qualifies when it is assigned to the watcher login, carries the trigger label, has the `Approved` issue field set to Yes by an approver, and its Project Status is Research, Spec, Plan or Debug. The poll starts a claim session in the repo's `Coordinator` worktree with `/sc:issue --claim N --pipeline none`. A standing coordinator session (`COORD-<RepoName>`) then starts a supervised worker, gets plan approval from a person, and on success posts the result comment and moves Status to In review. Higher launch levels exist in code but a closed ship gate (`level_gated`) holds them back. A person gives every push and merge.

**Clay.** An Orca automation runs a no-agent precheck every 5 minutes. The poll finds issues assigned to the user in any listed repo and does nothing if none is new. For a new one it writes a wake file, sends a mailbox message and types one fixed line into the repo's orchestrator session, starting that session if none is running. The orchestrator claims at `--pipeline none`, starts a worker with `worker-start`, watches its pull request, merges when every condition holds, closes the issue and keeps a living work report. Assignment is the only trigger. A repo's orchestrator holds at most 3 issues; a fourth starts another orchestrator, and an idle one ends after 30 minutes.

## The three differences Clay named

| # | Difference | Merged (owner) | Clay | What the evidence says | Recommendation |
|---|---|---|---|---|---|
| A | What starts work | Assignment plus trigger label plus `Approved` field by an approver plus an allowed Status | Assignment only (his ruling R1; assignment is safe because only users with triage or write access can assign, his R2) | The owner's own unification spec D01 kept approval as the gate and adopted Clay's plan check and `hold:backlog` as read-only skip reasons (78%, partial). Clay's design needs a poll that writes a `hold:plan` label; the spec D09 says the poll writes nothing to GitHub. | Keep the `Approved` field as the start gate. Adopt Clay's plan check (Priority, Fix approach, Test plan) as one more skip reason, read-only. This is a policy difference between two rulings, so it is the owner's and Clay's to settle, not mine. |
| B | Scheduler | Cron entry installed by the Coder image (Coder 515) | Orca automation with a precheck, no cron (his R4) | Cron is not installed in this workspace (`dpkg -s cron` says not installed, no `crontab`). `orca automations list` shows none exist, and `orca automations create` takes `--precheck`. The unification spec D02 found the owner's reason for rejecting automations ("an automation starts an agent every run") is true only if the precheck exits 0; a non-zero precheck starts no agent (62%, partial). | Use an Orca automation whose precheck runs `run-all`, once a firing test shows no agent starts on a non-zero exit. It needs no Coder image change and does not wait on 515. `run-all` is the same command under either scheduler, so nothing merged depends on cron. Needs the owner's change of the 2026-11-18 cron decision. |
| C | Coordinator lifecycle | One standing coordinator per project, its branch, worktree and session ensured by the Coder template (Coder 516) | One orchestrator per repo, started by the poll when needed, up to 3 issues each, ended after 30 minutes idle, state in a separate `IronOrchestrator` repo | Both start a missing session. Clay's extra parts (registry, per-orchestrator Run files, routing, `wrong_target`, idle end) cost his design about 9 more hours by his own estimate (115 to 124, section 5.7 point 9). The unification spec D07 already adopted his in-flight cap and guarded restart and rejected the registry repo, the idle end and the extra poll-started orchestrators. | One coordinator per project, with Clay's `max_in_flight` cap and his rule that the poll starts the session when it is down. Move the "check and start" from the Coder template into the dispatcher, so 516 shrinks to the worktree. Revisit more than one orchestrator per repo when a repo really has more than 3 issues at once. |

## Other differences

| Topic | Merged (owner) | Clay | Recommendation |
|---|---|---|---|
| Who merges and closes | A person's typed go for every push and merge; the coordinator comments and moves Status to In review | The orchestrator merges when conditions hold and closes the issue | Keep the person's go (unification spec D06, 85%). Adopt Clay's read-only merge gate and head-pinned merge as the check behind the go. |
| Names | coordinator, `/sc:coordinator`, `COORD-<RepoName>` | orchestrator, `/sc:orchestrator` | coordinator (spec D08, 85%); adopt his flags `--wake --hourly --resume --take`. |
| Handoff to the session | A claim session starts in the `Coordinator` worktree; the coordinator reads the claim evidence | Wake file plus mailbox message plus one typed line, with an acknowledgment | Adopt his wake file and acknowledgment as the transport (spec D10, 75%). It fixes the case where a claim session dies before the coordinator hears of it. |
| Where per-repo settings live | `~/.config/superclaude/issue-watch.d/<name>.json`, written by the generator | `repos.yaml` in a separate `IronOrchestrator` repo | Per-repo config files, no registry repo (spec D07). Add his `merge_method` and `max_in_flight` keys. |
| Models | `plan_depth` | `plan_tier`, `worker_tier`, `orchestrator_tier` in `repos.yaml` | `plan_depth`, default quick (spec OD-1, 66%). |
| Guard for workers | Guard version 2 refuses issue, label and project writes for governed sessions | A `worker-start` worker has no guard; accepted as a risk (his DQ7), and `master` is unprotected | Guard required for every coordinator-started worker, staged behind a live probe (spec D05, 78%). |
| Report | Result comment on the issue | Living work report, one entry per issue | Adopt the living report; keep the result comment (spec D11, 72%). |
| Launch levels (Worktree, Full, Full Submit) | Built, held by the closed ship gate | Never used | Compatible while the gate stays closed. |

## Where they already agree

- The worker starts through `worker-start` after a `--pipeline none` claim.
- Workers never merge and never write to GitHub; a launched agent writes a result file.
- Issues are keyed by repo and number, and each repo has its own origin check.
- The poll sends nothing when nothing is new, and it re-reads an issue before acting.
- Plan sections (Priority, Fix approach, Test plan) are expected on the issue; `/sc:issue --plan` (PR 690) creates them.

## What this means for the open builds

- **Coder 515 (cron):** not needed if B goes to an automation. It stays only if cron is kept.
- **Coder 516 (coordinator):** needed for the `Coordinator` worktree. The "start the session if down" part can move into the dispatcher (C), which both designs already describe.
- **Config:** until a `Coordinator` worktree exists, `check-config` fails with `worktree_invalid`, and the watcher stays `enabled: false`.
- **Clay's PR 686 and 690:** both were closed on 2026-11-23 (branches kept), per R38. This line first said PR 686 would be adapted, not merged as is (spec D14); R38 voids that.

## Decisions only the owner (and Clay) can make

1. **A.** Keep approval as the start gate, or assignment only. Recommended: keep it, add the plan check.
2. **B.** Cron or Orca automation. Recommended: automation, after a firing test.
3. **C.** One standing coordinator per project, or on-demand orchestrators. Recommended: standing, with the cap.
4. **Merge authority.** A person's go, or the orchestrator merges. Recommended: a person's go.

Unverified: whether an Orca automation with a failing precheck starts no agent (the unification spec read it from the CLI help, and no firing test has been run); the size of the Coder change for 516 once the session start moves into the dispatcher; every figure taken from the unification spec is a recommendation the owner has not ruled on.
