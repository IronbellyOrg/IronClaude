---
title: "Unified design: issue watcher, coordinator, TUI dashboard and issue-claim-to-work pipeline"
source_topic: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/../TOPIC.md
seed_brief: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/seed-brief.md
generated: 2026-11-20
generated_by: /sc:brainstorm (unattended, depth standard, 3 proposals, codebase enrichment, no research, handoff none)
adversarial_status: partial
convergence_score: 1.0
convergence_status: BLOCKED_BY_INVARIANTS
base_variant: "haiku:backend (variant 3); combined with variants 1 and 2"
unaddressed_invariants: [INV-025]
review: "independent review after the merge found 6 blocking and 14 minor defects; all fixed in place (adversarial-1/adversarial/merge-log.md)"
recommendation_only: true
---

<!-- Merged artifact of the adversarial pipeline (Step 5). Base: variant-3-haiku-backend.md (V3). Incorporated: variant-1-opus-architect.md (V1), variant-2-sonnet-analyzer.md (V2), the debate rounds, the invariant probe and the verdicts D01-D16, Q01-Q03. Executor: merge-executor. Merge date: 2026-11-20. Plan: adversarial/refactor-plan.md. -->

# Unified issue flow: watcher, coordinator, dashboard and claim pipeline

## 0. Status and glossary

<!-- Source: Base (V3 header and section 1 closing paragraph); V1 status line; V2 reading guide; merged per plan change #1 -->

**Status.** This whole document is a RECOMMENDATION. Nothing in it was built, pushed, merged, reverted, commented on or approved. Every decision below is a recommendation for the owner to rule on in chat; a verdict is a settled recommendation, not the owner's consent. Every new contract, verb, file and test named here is proposed and NOT BUILT unless the ledger in section 6 says otherwise. Anything no source proves is marked UNVERIFIED. No live test was run to write it. Code facts were read from snapshots of `origin/master` 61ac2c2e6, PR 686 head `8e5ae29ad`, PR 690 and the owner's unpushed branch (the roots are listed in section 9).

<!-- Source: post-review fix B2 -->

**One condition is carried and not solved (INV-025, HIGH).** Binding a worker to a guard level makes honest mistakes less likely, but it does not stop a worker that writes a script and runs it from pushing a branch, opening a PR, commenting or merging: the guard reads command text only. A ruleset on `master` and `integration` stops a push to those branches and, if the worker's login cannot bypass it, a merge into them. It does not stop a feature-branch push, a pull request or a comment. With the recommended admin bypass on one shared admin login, a worker's own script can still run `gh pr merge --admin`; only a separate login for agents (OA-6, third option) plus the ruleset makes "a worker cannot merge" true. A person's go is a procedure, not a block. Every control here narrows. No ruleset exists today. Sections 1, 3 (K2), 7 (OA-5, OA-20) and 8 (RK-2, INV-025 row) repeat this statement.

**How to read the codes.** Each code is explained here once; later sections use the code.

| Code | Meaning |
|---|---|
| Owner, Clay | The owner is the GitHub login `ironbelly`, the only repository admin. Clay is the login `clayphi` (they), author of PRs 681, 682, 683, 684, 686 and 690. |
| Poll | One run of the issue watcher for one repository (`superclaude issue-watch once`). |
| Coordinator, `Coordinator`, `coordinators` | "Coordinator" (lower case) is the long-running Claude session of one project, named `COORD-<RepoName>`. `Coordinator` (capital C) is the worktree and working branch it runs in. `coordinators` (plural) is a separate branch that carries human-readable records (D08 keeps these as two things). |
| Worker | A supervised Claude session the coordinator starts with Orca `worker-start` to implement one issue. |
| Wake, ack | A wake is a small file the poll writes to tell the coordinator about a claimed issue; it carries ids only. An ack (acknowledgment) is the coordinator's reply file. |
| Go | A person's typed answer in chat that permits one named outward action (one push, one merge, one cleanup apply). An agent records it; the owner never writes a file. |
| Grant | A standing permission for a small class of GitHub writes (at most three, default none), recorded by an agent from the owner's chat words. |
| Guard levels, L1, L2 | <!-- Source: post-review fix B3, N14 --> The launch-level guard has two layers: L1 is the hook that reads each command's text in a bound session (`launch-level-guard.sh`); L2 is the git pre-push hook (`launch-level-pre-push.sh`), which refuses only pushes to `main` and `master`. L1 has four levels. W ("worktree"): planning only; implementation, commit, push and PR refused. WA ("worktree, approved"): level W plus a regular file `sessions/<session id>.ok` in the guard's store (master `hooks/scripts/launch-level-guard.sh:265-272`); implementation allowed, commit, push and PR refused. F ("full"): implementation allowed, commit, push and PR refused, with no `.ok` file read. FS ("full submit"): commit, push and PR allowed (`:785-790`). |
| Route A | The owner's G2 release route (master `docs/designs/issue-pipeline-guard-g2.md:22`): after the coordinator records the plan approval it writes the worker's `.ok` file (restored verb `release-worker`), turning W into WA. The worker cannot write it itself (G2 rule 1, TAMPER class). |
| Throwaway issue | An issue listed in the per-repo config key `probe_issues` (issue numbers set by an agent from the owner's chat words). While `WORKER_BINDING_PROVEN` is false a worker start is refused for any issue not in that list. A throwaway repo is a repository the owner names in chat for live tests. |
| K1 to K24 | The picks that resolve contradictions between verdicts (section 3). They name contradictions, not risk scores. |
| X-001 | The open status item about the claim agent sharing the coordinator's worktree (section 3, after K1). |
| S0 to S17 | The stages of the migration (section 5). |
| MC-1 to MC-12 | The mechanical merge checks that stages must pass (section 5). |
| O0 to O7 | D15's build-order codes (D15:18): O0 hold and owner answers; O1 lane 1 plus text that touches no contested file; O2 lane 2 (revert dry run, revert, contract amendment, planb, design amendment); O3 adapted PR 686; O4 coordinator substrate; O5 merge path as one tested unit; O6 other verbs and transport; O7 live tests, then enable. |
| H0, lane 1, lane 2, lane 3 | D14's hold step (H0: hold PRs 686 and 690) and its three independent lanes (lane 1: PR 693, PR 690, claim rule C1; lane 2: revert, amendments, planb; lane 3: text, sweep and report work). |
| OA-1 to OA-34 | The owner actions: questions only the owner can answer (section 7). |
| RK-1 to RK-35 | Rows of the risk register (section 8). |
| Debate diff points | <!-- Source: post-review fix N14 --> Ids such as S-001, C-001, X-002, A-001 (with a hyphen and three digits) are the diff points of `adversarial/diff-analysis.md` settled in the debate; they are not stages. X-001 is the one still open. |
| Design rows | R9, R10, R17, R19, R25, R36, DQ7, DQ8, OD1 and similar are rows of Clay's design text `docs/designs/orchestrator.md` (PR 681), named at first use; OD1 is a design row, not D15's question OD-1. |
| N6, N7 | Rows of Clay's closed refusal list: N6 refuses a release or tag; N7 was an interrupt exception and is removed. |
| PR B | Clay's planned, unopened PR for the orchestrator skill and verb group; it has no PR or branch. |
| OB-H1 to OB-CTX | The twelve live guard observations of issue 442 (OB-H1, OB-H2, OB-H3, OB-CTX and their items). None has passed. |
| IR7 | The claim's refusal when the L2 hook is missing; built but switched off (`IR7_REFUSE = False`, master `skills/sc-issue-protocol/scripts/orca_worktree.py:822`). |
| Q01's four tests | An answer counts as a go only if it was typed by a person in their own session, names the right entry, is newer than that entry's last edit, and matches the question key (for example `merge_safety:<PR>:<head sha>`). |
| INV-001 to INV-027 | The 27 findings of the invariant probe (`adversarial/invariant-probe.md`), each listed with its handling in section 8. |
| D01 to D16, Q01 to Q03 | The settled verdicts in `debates/<id>/VERDICT.md`. "D15:219" means line 219 of D15's verdict file. |
| OD-1 to OD-13 | D15's open owner questions (D15 section 7), all folded into the OA list: OD-1 is OA-27, OD-2 and OD-13 are OA-14, OD-3 to OD-9 are OA-29 to OA-34 (OD-6 and OD-7 share OA-32), OD-10 is OA-12, OD-11 is OA-11, OD-12 is answered by K4 and C-INV-3 (protected file and fail-closed values). |
| D15 table rows | Letters plus a number without a leading zero (A1, B3, C1, D8, E7, F3, G1) are rows of D15's element table, not verdict ids: "D15 row D8" is the `refuse(argv)` row, never verdict D08. |
| C-INV-1 to C-INV-4 | D15's four HIGH conditions (D15:140-143): waiting hand-backs and the cap, who wakes round 2, config tampering, close authority. |
| MR-1, MR-2 | D01's must-keep rules: MR-1 repeats every start gate at the moment of start (`_revalidate`); MR-2 keeps `marker_in_window`, so a hand claim and a watcher start never run two workers. |
| M1, M2 | D10's wake rules: M1, the coordinator acknowledges only after its per-issue state file exists; M2, an abandoned wake is recovered by a named reader. |
| NG-2 | The rule that the poll writes nothing to GitHub. |
| WC-n, WC:n | Rule n, or line n, of `WORKER-CONTRACT.md` (installed as `~/.claude/WORKER-CONTRACT.md`). WC-17 is the restored plan-approval duty. |
| G2 rule 1, G2 rule 2 | The owner's guard design for coordinator-started workers (`docs/designs/issue-pipeline-guard-g2.md`). Rule 1 comes back with the restored approval verbs; rule 2 (plain `ask` and `send` without `--to`) is built. |
| R33, R18, R22, R35 | Zero-setup requirements: R33 is `GOVERNED_LEVELS_ALLOWED = False`; R18 is the default-on generated config; R22 the Status allow-list; R35 the `Approved` field. |
| U3, U5, U8, U25, U28, U30, U54 | Live unknowns from Clay's test register: U3 depth-0 script start, U5 mailbox from outside an Orca Run, U8 info-stream replies, U25 the ccsession tag and idle detection, U28 the effective model, U30 effort levels, U54 the naming scan. |
| T1 to T13, AU1 to AU8 | Clay's coordinator test plan rows (T13 is the merge-path test) and the eight post-merge audit checks. |
| planb | The owner's unpushed branch `ironbelly/issue-watcher-zero-setup-plan` and its working tree. |
| pr-a, pr-p | Snapshots of PR 686 (Clay's watcher rewrite) and PR 690 (`/sc:issue --plan`). |
| master | The snapshot of `origin/master` 61ac2c2e6. A citation like "master `cycle.py:228`" names a file under that snapshot's `src/superclaude/cli/issue_watch/`; a citation that starts with another folder (for example `core/`, `hooks/scripts/`, `cli/sweep/` or `skills/sc-issue-protocol/`) is relative to the snapshot's `src/superclaude/`, and one that starts with `docs/` or `tests/` is relative to the snapshot's root; "planb `generate.py:252`" and "pr-a `wake.py:69`" work the same way. |
| [B] [P] [C] [N] [D] [R] | Status tags in the diagram: [B] built on master, [P] built only in planb, [C] in an open Clay PR, [N] not built, [D] design text only, [R] removed by PR 682 and pending restoration. |
| BUILT-ON, BUILT-OFF, NOT BUILT, REMOVED, DESIGN ONLY | Ledger words of section 6 (defined there). |

## 1. Summary

<!-- Source: Base (V3 section 1, ten lines) rewritten as full sentences; V1 section 1 (five decisions); V2 section 1 last paragraph ("what cannot be proven yet"); merged per plan change #1 -->

**The architecture in plain words.** One flow runs per project. A cron entry runs one dispatcher every five minutes. The dispatcher runs a read-only poll for each project. When an issue is approved, assigned only to the watcher login, has its plan sections filled, carries no backlog hold, has an allowed Project Status and its body is unchanged since approval, the poll starts a claim session at level none, exactly as the code on master already does. When the claim marker appears on the issue, the poll saves a delivery intent and writes a small wake file that carries ids only. The project's coordinator (`COORD-<RepoName>`, in the `Coordinator` worktree) pulls that wake, saves its own record of the issue, acknowledges the wake, adopts the claim, and starts ONE supervised worker bound to guard level W. The worker writes its plan; after the person's recorded plan approval the coordinator releases it to level WA, where it edits and tests but cannot commit, push or open a PR through any command the guard recognises. The coordinator commits the work. A person's typed go is needed for every push and every merge, and the merge itself is pinned to the exact head commit. Closeout and a dry-run cleanup list follow. The sweep stays the one source of session facts, the observer screen shows them, the observer reads the watcher's own status report for holds and skips, and the work report gives plain-English progress per issue. This is a local, at-least-once system: the same wake may arrive more than once, and handling one issue round twice must have no second effect.

**The decisions that matter most.**

1. **The poll claims; the coordinator adopts (K1).** The poll keeps launching `/sc:issue --claim <N> --pipeline none` as built (master `launch.py:33`). The wake means "claimed, take over", never "please claim". A per-repo key `claim_by` is reserved so the owner can later move the claim into the coordinator. Real rollout stays off until the live check X-001 shows whether the claim agent and the standing coordinator overlap in the same worktree.
2. **Workers are bound by the guard; the coordinator commits; a person's go precedes every push (K2, K16).** <!-- Source: post-review fix B2, B3 --> With both gates kept (OA-1), the worker starts at level W, where implementation is refused, and the coordinator releases it to level WA only after the recorded plan approval (route A), so the guard itself enforces the plan gate. WA and F both allow implementation and refuse commit, push and PR (master `hooks/scripts/launch-level-guard.sh:785-790`); F is used only if the owner keeps the start gate alone, or if the coordinator cannot learn the worker's session id. Until a live probe proves a `worker-start` worker can be bound, the constant `WORKER_BINDING_PROVEN` stays false and no worker starts on an issue outside `probe_issues`. **INV-025, stated plainly: binding narrows honest drift; it does not stop a worker that writes a script and runs it.** A ruleset on `master` and `integration` stops a push to those branches and, if the worker's login cannot bypass it, a merge into them. It does not stop a feature-branch push, a pull request or a comment. With the recommended admin bypass on one shared admin login, a worker's own script can still run `gh pr merge --admin`; only a separate login for agents (OA-6, third option) plus the ruleset makes "a worker cannot merge" true. A person's go is a procedure, not a block. Every control here narrows.
3. **Machine state lives outside any git checkout (K5).** Wakes, acks, per-issue state, go entries and the grant-use log live in the per-repo state root named by the config key `state_dir`; human-readable records live only on the local `coordinators` branch, by local commits that are never part of a PR to master, and pushing that branch is itself an outward action that needs a go (OA-26).
4. **One poll command and one config contract (K4).** Cron runs `issue-watch run-all`, which runs `issue-watch once --config <config_dir>/<repo>.json` for each project. There is no registry repository and no `repos.yaml`. The config stays at `schema_version` 1; each new key is added to the loader in the PR that first reads it; a missing authority key means the most restrictive value. <!-- Source: post-review fix B1 --> Planb's `run-all` is not read-only today: for a repo with no config it generates one, creates the trigger label on GitHub and rewrites the config to `enabled: true` once its checks pass (K24). So `run-all` is not scheduled before S17, and a new defaults key `auto_enable` (false) keeps generated configs off until the owner says otherwise.
5. **Order is fixed by evidence (K20, section 5).** Hold PRs 686 and 690 first; land PR 693, an adapted PR 690 and claim rule C1; dry-run and then revert PR 682 (only if the owner keeps both gates, OA-1); amend the contract and guard; land planb; amend the design; adapt PR 686 in place as one draft; then build the coordinator substrate, the merge path as one tested unit, the transport and the rest; enable one throwaway repo last. PR 686 never merges as it stands (D14).
6. **The poll cycle writes nothing to GitHub (NG-2; the one-time label creation of planb's per-repo init is a separate write that needs the owner's chat OK, K24); merges need a person's typed go; workers never run `/sc:pr-submit`; there is no standing `pr.merge` or `issue.close` grant; every approval is given in chat and recorded by an agent.** These owner rules hold in every stage.

**What is built and what is not.** On master today: the single-repo poll (switched off: `enabled` defaults to false, master `cycle.py:228`), `/sc:issue --claim`, the launch-level guard and its `pending` verb, `/sc:closeout`, the sweep, the observer and the work report. In planb only: the dispatcher `run-all`, per-repo JSON configs and `GOVERNED_LEVELS_ALLOWED = False`. In open PRs only: PR 686's wake files and holds, PR 690's `--plan`. Removed by PR 682: the plan-approval package and G2 rule 1. Design text only: the coordinator command, its verbs, the merge gate, the go entry and the audit checks. Section 6 gives the evidence row by row.

**What cannot be proven yet.** No `worker-start` worker has ever been bound by the guard. Nothing shows the claim terminal closes after the claim ends (X-001). The mailbox from outside a Run (U5), Orca's idle detection and the ccsession tag (U25), cron in the Coder image (Coder issue 515), the `Coordinator` worktree in the image (Coder issue 516), and a chat go on one shared login are all unproven. Section 8 names the test for each. The 27 invariant findings, one HIGH (INV-025) and fifteen MEDIUM still open, are carried as binding conditions.

## 2. Target architecture

<!-- Source: V1 section 2 diagram, merged per plan change #2, with V2 section 2.0 status tags and V3 section 2 flow (saved intent, replay, plan approval) -->

The diagram shows the end state. Nothing below the cron line runs in this shape today; the tags say what exists (glossary). `<config_dir>` is the per-repo config folder (default `~/.config/superclaude/issue-watch.d`), `<state_dir>` is the per-repo state root named in each config, and `<worktrees>` is Orca's worktree root.

```text
 OWNER'S CHAT: approvals, goes, grants, rulings (an agent records each one) ------------+
                                                                                        |
 GITHUB (the poll only reads; seven read-only gh calls, NG-2)                    [B]    |
   issue assigned only to the watcher login, Approved set, Status allowed,              |
   plan sections pass the check, no hold:backlog, body unchanged since approval [B][C]  |
        |                                                                               |
        v                                                                               |
 cron */5 * * * *, flock -n, absolute paths, log                                 [N]    |
        v                                                                               |
 issue-watch run-all (ONE dispatcher; orca repo list; absolute gh and orca       [P]    |
   paths passed to every child; zero repos served is an alarm)                          |
        v                                                                               |
 issue-watch once --config <config_dir>/<repo>.json   (store lock held)          [B]    |
   start rule -> plan check -> cap -> save attempt -> claim launch          [B][C][N]   |
        v                                                                               |
 CLAIM SESSION  /sc:issue --claim <N> --pipeline none                            [B]    |
   posts the claim marker; leaves .dev/issues/<N>/ in launch_cwd                        |
        v                                                                               |
 next poll: marker_in_window -> state claimed -> ONE save of claim evidence      [B]    |
   plus delivery intent (wake id) -> release lock -> publish ids-only wake       [N]    |
   replay keeps the wake id; a retarget creates a linked new id                         |
        |  <state_dir>/wakes/<id>.json ; optional mailbox or typed-line nudge    [C]    |
        v                                                                               |
 COORD-<Repo> session in <worktrees>/<repo>/Coordinator                       [N][D] <--+
   1  pull wakes at every check --wait return; save issues/<repo-key>__<N>.json [N]
   2  write <id>.ack.json only after step 1 (M1)                                  [N]
   3  adopt the claim: read launch_cwd through the `state` verb, copy
      .dev/issues/<N>/ into the worker worktree (claim.md:96)                   [N]
   4  pending --level worktree (W) ; worker-start with [sc-launch:v1:<nonce>]
      from the restored brief.py ; check pending/<nonce> is gone             [B][N]
   5  W worker writes the plan and asks once; person approves; coordinator
      records it (WC-17, check-approval) and writes the worker's .ok
      (release-worker, route A) -> level WA                                    [R]
   6  WA worker: edits and tests, worker_done (no commit, push or PR command)   [N]
      (only the start gate kept, or no session id: bind at F, skip step 5)
   7  coordinator checks branch and base, commits explicit paths + .dev/tasks   [N]
   8  person's typed go -> push and /sc:pr-submit --monitor 3 in a
      person-opened ordinary top-level session (never a worker)                 [B]
   9  merge-gate -> person's typed go -> merge-gate again ->
      gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>           [D]
  10  closeout (linked issue closed only if the go names it), cleanup list
      (dry run), post-merge audit AU1-AU8                                    [B][D]
        |
        v
 sweep (read-only: Orca, transcripts; no GitHub call)                           [B]
   sweep JSON v1 + session_id, worktree_path, saved beside the report           [N]
 issue-watch status --json (holds, skips, stranded deliveries) --> observer  [B][N]
 report-entry files -----------------------------------------------> work report [N]
```

<!-- Source: Base (V3 section 2, at-least-once paragraph) -->

This is a local, at-least-once system: it may deliver the same wake repeatedly, but processing one issue round twice must have no second effect. A claim launch with a lost receipt is uncertain, not a retry instruction. A failed read is unknown, not empty. The system has no cross-host claim guarantee; a second host remains unsupported until a shared lease design is approved and tested. Gates that stay manual: the approval (an issue field set by a person), the typed go for each push and each merge, the chat go for cleanup `--apply`, and a server-side ruleset on `master`, which does not exist today (`protected: false`, D16 section E).

### 2.1 Issue watcher

<!-- Source: Base (V3 section 2 "Issue watcher") as spine; V1 section 2.1 STAYS list and symbol names; V2 section 2.1; merged per plan change #3 -->

**What it is.** The cron-driven, read-only poll that decides which approved issue starts, starts its claim, and tells the coordinator. Master today has the single-repo poll (`once`, `status`, `check-config`, `init-state`, `reset`), switched off by default (master `cycle.py:228`).

**STAYS (ours).**
- D01's start rule and its code: the issue is open and assigned only to the watcher login (`is_intended_owner`); the approval is current (`approval_of`) and the body unchanged since it (`unchanged_since`); the Project Status is in the allow-list Research, Spec, Plan, Debug (R22); `eligibility_order` and the evidence classes. Assignment alone never starts work (D01).
- MR-1: every gate is repeated at the moment of start (`_revalidate`, master `cycle.py:979`). MR-2: the claim marker `<!-- sc:issue:claim -->` (master `predicates.py:14`) is read through `marker_in_window` (master `predicates.py:279`), so a hand claim and a watcher start never both run (D01:12-18).
- NG-2: the poll cycle makes seven read-only `gh` calls and writes nothing to GitHub (planb's one-time init label write is governed by K18 and K24). The integer-only claim prompt (master `launch.py:33`). Off by default: `enabled` absent means off (master `cycle.py:228`), the `DISABLED` kill file, and `GOVERNED_LEVELS_ALLOWED = False` (planb `launch.py:48`). The owner's integer-only prompt rule (decision D3 of `docs/designs/issue-watcher.md:39`) widened by D10 item 6: only pattern-checked values reach a prompt, typed line, mailbox subject or argv.
- The built store and its safeguards: `dispatch.json` with states `pending, launched, unknown, failed, abandoned, claimed` (master `record.py:34-35`); a `pending` entry may start only from no entry or `failed`, never from `unknown`; a later marker turns `launched`, `unknown` or `abandoned` into `claimed` (master `record.py:447`); the 60-minute lease is a reporting lease of a `launched` entry only (master `record.py:440-441`), not a merge-go lifetime and not proof that a process died. The save-before-launch order is built (master `cycle.py:1080-1112`). An `unknown` launch counts toward the cap and only a person's `reset N` clears it (INV-009).
- From planb: `run-all`, `dispatch.py`, `generate.py`, `repo_init.py`, `first_run.py`, `defaults.py`, per-repo JSON under `issue-watch.d/`, the stage-aware `brief.py` and `complete.py`. The trigger label stays for now (OA-8). <!-- Source: post-review fix B1 --> Planb's `run-all` is not read-only and not off by default: for a listed repo with no config it calls `ensure_config` and then `first_run` (planb `dispatch.py:404-417`); `first_run` creates the trigger label on GitHub through `ensure_trigger_label` (planb `first_run.py:193`; `repo_init.py:108`) and rewrites the config to `enabled: true` once its checks pass (planb `first_run.py:16-17, 99-107`). Only `--dry-run` merely reports `would_generate` (planb `dispatch.py:406-410`). K24 governs this.

**ADOPTED from Clay.**
- `plan_check` as a read-only skip reason `held_incomplete`, run before the approval read, where a section holding only `<...>` placeholders counts as empty; `hold:backlog` as a person-set veto read as `held_backlog` (D09; D15 rows A1, A3). The body stays in memory only.
- `would_hold` and a local `holds` entry with no GitHub write (Q03). A leftover `hold:plan` label is ignored with no warning.
- The wake file and its acknowledgment, three deliveries ten minutes apart, then an unread mark and exit code 7 (D10); with M1 and M2 added.
- `max_in_flight` with the skip reason `coordinator_full`, guarded restart, exclusive-create per-issue state, `owner/name` keys with `name_collision` (D07; D15 rows C1, C2, C4).
- The closed reasons table (pr-a `audit.py:39`) with its pin recomputed (MC-10): the 14 approval reasons come back; `coordinator_full`, `name_collision`, `no_checkout` and `coordinator_absent` are added; `registry_invalid`, `repo_not_listed` and the four label-write reasons leave (pr-a `tests/issue_watch/test_audit.py:86-98`).

**REWRITTEN.**
- The cron line: five fields `*/5 * * * *`, `flock -n` on a host lock, absolute paths, output to a log (D02). It calls ONE dispatcher, `run-all`, which discovers projects with `orca repo list` and runs the child `once` per project under that project's own store lock. `run-all` passes absolute `gh` and `orca` paths to every child, because cron's `PATH` is only `/usr/bin:/bin` (INV-006). A run that serves zero repositories is an alarm in `status --json` and on the observer (INV-014). The cron image remains unproved (Coder issue 515); D02's automation fallback needs its 1-24 hour experiment first.
- The claim path follows K1. Today the cycle holds its lock through the final commit (master `cycle.py:682-709`), so "release before delivery" needs an explicit post-commit phase. Replay runs even when the normal path skips a claimed entry (master `cycle.py:920-921`) and when a precheck fails (INV-027). A delivery retry never calls the claim launcher; an unknown receipt never relaunches. <!-- Source: post-review fix N7 --> Today a hand claim with no prior entry becomes `claimed` (master `record.py:660-665`, transition T-11); under K1 it would get a wake. REQUIRED CHANGE: the poll writes a delivery intent only for entries it launched (`launches` of 1 or more); test `test_manual_claim_gets_no_wake` (S11). Ambiguous old `claimed` rows need explicit reconciliation.
- Store states become `pending, launched, claimed, woken, acked, unknown, failed, abandoned, waiting_reapproval`. The store has a strict typed schema (planb `record.py:168-175, 213-278`), so the new fields need a versioned migration, a backup and a downgrade step (INV-004, MC-11).
- Names say coordinator (D08): `coordinator-wake/1`, `coordinator-wake-ack/1`, mailbox kind `coordinator-wake`, typed line `/sc:coordinator --wake <id>` (today orchestrator names at pr-a `wake.py:46-47`). The wake folder moves from pr-a's `.orchestrator/wakes` (pr-a `wake.py:69`) to `<state_dir>/wakes/` (K5).
- Stripped: the label writer, `_hold_write_ok`, `hand_removed` (D09, Q03); the registry, PR 686's `repos.py`, `repos.yaml` and `wrong_target` never land (D07). The plan check is a package copy of `plan_body.py check` (K8).

**INTERFACES.** Consumes: GitHub reads, `orca repo list`, the defaults file, the per-repo config, the claim marker, ack files, the plan check. Exposes: the cron line, `run-all`, wake files and nudges, `issue-watch status --json` (the only public read of watcher state, extended per K10) and `audit.jsonl`; `dispatch.json` stays private to the watcher. Until claim worktrees are separated (X-001), real rollout stays off; the marker alone is not proof that the claim session ended. A missing checkout or a duplicate short name is a skip with a reason (`no_checkout`, `name_collision`). A re-approval after hand-back produces a new wake round, never a new claim (K15).

### 2.2 Coordinator

<!-- Source: Base (V3 section 2 "Coordinator") as spine; V1 section 2.2 verb list and flags; V2 section 2.2; merged per plan change #4 -->

**What it is.** One standing, project-local Claude session (`COORD-<RepoName>`, worktree and working branch `Coordinator`, records on the `coordinators` branch) that adopts a claimed issue, runs one supervised worker, and carries the issue to a person-approved merge. Nothing of it is built: no skill, no command, no verb group. Today only the contract text (`WORKER-CONTRACT.md`) and the design text `docs/designs/orchestrator.md` exist.

**STAYS (ours).**
- Authority. A person opens the session; a script may start it at depth 0 only under an authorization the owner recorded in chat, and only after the depth-0 start is proved (U3) and WC:70 and WC:245 are approved in chat (K11). That authorization is self-attested, and the spec says so. A flag-less `/sc:coordinator` creates no grant and no merge (D08). A person's typed go is needed for every merge; there is no standing `pr.merge` or `issue.close` (D04, D06). `/sc:pr-submit` and `/sc:closeout` never run as a worker (WC:23, WC:244). WC-9: no outward action from a worker (master `core/WORKER-CONTRACT.md:41`); worker commits are pushed only on the person's go (`WORKER-CONTRACT.md:245`). Unanswered means wait: until the owner answers, nothing that depends on the answer is switched on (the spec is written to the recommended answer only as a plan).
- The restored `issue_pipeline` package in planb's stage-aware form (`brief.py` with the marker line, `complete.py`, `release-worker`), WC-17 "Issue pipeline duties" and G2 rule 1, after the revert (K3; D03, D14). G2 rule 2 is built and stays.
- Project-local topology (D07, D08) and the guard required for every worker the coordinator starts (D05).
- Every approval, go and ruling is given in the owner's chat and recorded by an agent (Q01).

**ADOPTED from Clay.**
- One verb group `superclaude coordinator <verb>` with one JSON contract, one state lock and one `refuse(argv)` closed "may do" list (D15 row D8, order O4). N6 (release or tag) is an unconditional refusal; the interrupt exception N7 is removed. These narrow risk; they do not stop raw shell use.
- The verbs listed by D15 R-7 (D15:33): `wake-check`, `wake-ack`, `state`, `plan-check`, `repos`, `merge`, `merge-gate`, `answer-check`, `audit`, `report-entry`, `escalate` (no interrupt) and `handback`. Their spelling under `superclaude coordinator` is UNVERIFIED until built.
- `merge-gate` (13 closed reasons, read-only) run before the go and again before the merge; a head-pinned merge; never `--auto`, `--admin` or `--delete-branch`; `changes_requested` is a hard refusal; only `checks_failing` and `merge_safety` have overrides, each with its own question key; a merge-time reviewer hold (60 minutes is an UNVERIFIED default) (D06; D15 rows D1 to D3).
- `answer-check` as a validator only, with the owner's identity as a parameter, never hard-wired to Clay (Q01). `E-NO-GRANT` with a grant-use log, failing closed on a missing or malformed `grants` key (D04, Q01).
- Audit checks AU1 to AU8 with AU5 narrowed, the hand-back loop (`HANDBACK_MAX` 3, labelled "not measured"), `escalate`, `report-entry`, the nine-row "what reaches the person" notice table, the test plan T1 to T13, and the flags `--wake`, `--hourly`, `--resume`, `--take <owner/repo#N>` and `--sub` (D08, D15 rows D15, D16, D18, G1, G2).

**REWRITTEN.**
- Delivery. The coordinator pulls wakes at every return of its bounded `check --wait`, at least every five minutes. It saves the issue and round state BEFORE it writes the ack; the poll accepts the ack only if the referenced state exists and matches (Rule B, MC-6). An abandoned wake is retargeted with a linked new wake id, never re-claimed (M2). Three deliveries ten minutes apart end as unread with exit 7; three failed restarts require a person.
- Adoption. The wake means "claimed, take over". The coordinator reads the claim's files location (`launch_cwd`, saved in the store entry) through the `state` verb, because the wake carries ids only (INV-018), and copies `.dev/issues/<N>/` into the worker worktree as `refs/claim.md:96` already describes.
<!-- Source: post-review fix B3 -->
- Worker binding (K2, K16). With both gates kept, the coordinator runs `orca_worktree.py pending --level worktree`, which only writes the pending record (master `skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523`), so the preflight is separate. The restored `brief.py` puts the marker in the first prompt; the coordinator checks that `pending/<nonce>` is consumed within a stated timeout (60 seconds proposed, UNVERIFIED), else stops and escalates. The worker is now at level W: it can plan, and implementation is refused (LL-IMPL).
- Plan approval (route A). The worker asks once with the plan path, file list and plan hash; the person approves; the coordinator records the approval, runs `check-approval` (WC-17) and then writes the worker's `sessions/<session id>.ok` through the restored `release-worker`, which turns the worker's level into WA (master `hooks/scripts/launch-level-guard.sh:270-271`; master `docs/designs/issue-pipeline-guard-g2.md:22`). The worker cannot write that file itself (G2 rule 1, TAMPER). The plan gate is then enforced by the guard, not only by the contract. How the coordinator learns the worker's session id is UNVERIFIED (G2 design section 4; FU-1 precondition f); if it cannot, the worker is bound at F and the plan gate rests on the contract only. If OA-1 keeps only the start gate, PR 682 stands, this step disappears, the worker is bound at F, and stages S6 to S9 change (section 5).
- Commit and push (K2). Branch and base check first, because WA and F allow reset, rebase, switch and `branch -f` (INV-007); explicit paths plus `.dev/tasks` with `git commit --only -- <paths>`, as WC:246 already requires; a hook refusal or rewrite is escalated, never `--no-verify` (INV-019). Push and `/sc:pr-submit --monitor 3` only on a typed go, from a person-opened top-level session (A-005).
- Merge. Argv is exactly `gh pr merge <N> --repo <R> --<method> --match-head-commit <40-char-sha>`. A fresh gate precedes both the chat go and the merge. The go entry records the full head, the quoted words, date, recorder, question key and gate snapshot; the answer must follow the entry's latest edit in the owner's own session. A change of head, reviews, base, threads, draft state or gate reason voids the go; the live role overrides `can_merge`; a consumed go is never restored (INV-005).
- Close (K12), grants (K6), session start and restart (K11, K14): as decided in section 3.

**INTERFACES.** Consumes: wake files (pull and nudge), the per-repo config (read only), grants, go entries, `plan-check`, Orca `worker-start`, `check --wait` and the mailbox, `worker_done`, the person's typed answers. Exposes: acks, per-issue state files, go entries, the grant-use log, audit lines, report-entry files, escalations and the worker's first prompt with the launch marker. Restart never restores consumed consent; runtime records and protected authority records stay separate.

### 2.3 TUI dashboard and observability

<!-- Source: Base (V3 section 2 "TUI dashboard and observability"); V1 section 2.3; V2 section 2.3; merged per plan change #5 -->

**What it is.** Three read-only layers over the same facts. TUI means terminal user interface. The sweep (`/sc:sweep`, PR 539) classifies sessions; the observer (`superclaude observe`) is the live terminal screen; the work report (PR 684) says in plain English what is done and what needs a person. The issue 409 dashboard package is a prototype on synthetic fixtures, "not a production integration".

**STAYS (ours).**
- The sweep is the one stateless, zero-model, read-only source of session facts, with eight classes including "could not determine", no GitHub call, at most one sweep per five minutes (WC-16), and it recommends nothing (D11).
- The observer is navigation only: no Options, no Recommendation, no write; entry text passes through `observe/sanitize.py`; an empty folder, zero rows and "could not read" are three different states.

**ADOPTED from Clay.**
- The work report as the plain-English work-item layer (GitHub, ClickUp, per-issue text), the living report with entry files and no-model refresh, the silent-loss rules, `check.py` and `run.py gate`, the transcript-since-last-report reader, and the plain-English item template (D11; D15 rows E1 to E5).
- The nine-row "what reaches the person" table, used in the notice step only. The cap of 5 notices a day stays a proposal; the default is 0, meaning no cap (K23, OA-16).
- `report-entry` as the one writer of an entry file (D15 row E7).

**REWRITTEN.**
- Sweep rows gain `session_id` and `worktree_path` (empty allowed), with a reviewed edit of the golden test that pins the v1 keys. Today a row has neither (master `cli/sweep/report.py:642-661`); the models already hold both (master `cli/sweep/models.py:103`, `:131`).
- The sweep JSON is saved atomically beside the Markdown report as `<UTC>-sweep.json` (K19); today it goes to standard output only (master `cli/sweep/commands.py:277-278`). Timestamps stay visible; a screen refresh is not a new collection.
- The observer reads `issue-watch status --json` directly for watcher facts (K10). Held issues without a label (`held_incomplete`, `held_backlog`, `coordinator_full`, `name_collision`, `no_checkout`) appear there as `recent_skips`. The sweep does not call the watcher.
- The report takes session facts from the sweep and keeps D11's two HIGH rules: it reads transcripts for the sweep's session ids PLUS every not-done session of the previous report, and it keeps its own terminal-to-session map until one LIVE side-by-side run shows parity. It writes `read: false` when Orca is down, never "ended". It drops person-specific config (`"person": "clayphi"`). Entry files store only `session_id`, never a copied session class.
- The contract note `docs/designs/observe-sweep-contract.md` comes first and names the three readers.

**INTERFACES.** Exposes: the sweep JSON with two new fields and a saved file, the observer's existing `snapshot.json`, and report entry files in the report skill's configurable per-user state path (D11), not in a checkout; `.dev/coordinator/orchestrated/` is only the report's own legacy default folder name (singular, D08) <!-- Source: post-review fix N6 -->. Consumes: Orca read verbs, `issue-watch status --json`, entry files; GitHub and ClickUp only in the report. The exception is stated, not hidden: the observer's questions panel still calls Orca itself (master `cli/observe/adapter.py:32`), so "one source" holds for sessions only until the owner rules (OA-17).

### 2.4 Issue claim to work pipeline

<!-- Source: Base (V3 section 2 "Issue claim to work pipeline"); V2 section 2.4; V1 section 2.4; merged per plan change #6 -->

**What it is.** `/sc:issue --claim` (assign, accuracy check, summary, next-step prompt, then an Orca worktree and an agent at the chosen level), the launch-level guard that binds sessions a claim launched, the worker handoff after a level-none claim, and the post-merge closeout and cleanup.

**STAYS (ours).**
- `/sc:issue --claim` waves 0 to 8, its flags and its levels (none, worktree, full, full with `--submit`) for a person who types them; flag meanings unchanged (D04). Every watcher or coordinator claim passes exactly `--pipeline none` (master `launch.py:33`). The claim marker is a duplicate guard, not consent (master `skills/sc-issue-protocol/templates/claim-comment.md:23`). Claim stops only when the issue is assigned to someone else (`refs/claim.md:42`, D16 section F).
- The Pipeline field stays unread while no governed level is allowed (D04, K7).
- The chain (`refs/chains.md`, `/sc:recommend`); `/sc:issue` runs no chain command itself (D12).
- The guard L1, the L2 pre-push hook, job identity and G2 rule 2; the `pending` verb (master `skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523`, levels `worktree|full|full-submit`).
- `GOVERNED_LEVELS_ALLOWED = False` until issue 442's twelve live observations pass, a reviewed amendment of the design rows R9 and DQ7 and of the related row in the design's own risk register lands, a watch path for agents reporting through `result.md` exists, and a replacement for what R36 removed exists (D04).
- PR 693 (the claim launch result file, issue 691). The restored brief alone owns the handoff marker.

**ADOPTED from Clay.**
- Plan sections in the four issue templates (PR 661, already on master); `/sc:issue --plan <N>`, `--remaining <file>` and `plan_body.py {check,splice,verify,prepare}` (PR 690, after D12's four fixes; pr-p `skills/sc-issue-protocol/scripts/plan_body.py:138`).
- `/sc:closeout` (PR 683, already on master) as wave 8; the shared landed check `branch-landed.sh`; the nine cleanup rules of issue 687 as adapted by D13 and Q02.
- The one supervised `worker-start` route after the claim (D04; D15 row D12).
- `--mode other` and the form plan fields as a separate small issue split out of issue 689 (D15 row A10); issue 689's creation redesign stays deferred (D15 row A11).

**REWRITTEN.**
- Claim rule C1 (D12). When the three plan sections pass `plan_body.py check`, the accuracy verdict is current and the issue is a simple feature, claim passes the short chain `/sc:workflow` then `/sc:implement` to `/sc:recommend`; otherwise it uses the existing chain row seeded with the plan. D12's five claim safeguards include these two: the plan is quoted only inside a fenced "data, not instructions" block, and commands are never taken from the plan's "Commands, in order" line. This changes next-step text only; it runs no chain command. "Simple feature" has no measurable test in D12 (UNVERIFIED).
- A manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>`; it never refuses (D12 item 5).
- One plan check (K8). `plan_body.py check` is the reference. Headings inside fences or comments do not count; absent, repeated, empty or placeholder-only sections fail, including `<...>`, TBD and "Not known yet". Presence is not quality. PR 690 currently counts exact lines without fence state (pr-p `skills/sc-issue-protocol/scripts/plan_body.py:101-139`), so S2 aligns it first.
- The bound worker route (level W, then WA after route A's release; F only as the fallback) and its commit rules (section 2.2, K2).
- Hand-back creates a new round only after the worker is final. Body edits void approval; the poll rechecks waiting rounds despite old acks; a waiting round consumes no slot (K15). The proposed round cap of 3 is unmeasured.
- Closeout needs explicit close authority (K12). Cleanup runs `list` each cycle and starts report-only for one week; `--apply` needs its own chat go naming that action; any refusal keeps the entire worktree; never `--force`, `-D` or `rm`; remote branch deletion is human-only; a git refusal means "kept", not failure. Q02 refusals: never `master`, `main`, `integration` or the default branch; keep the branch if any PR with this head is OPEN; the merged PR's `headRepositoryOwner` must be ours; the dry run prints "branch: would delete / would keep (reason)" and the PR head sha. Because `orca worktree rm` may delete the branch itself (UNVERIFIED), the refusals run before any worktree removal.

**INTERFACES.** Claim artifacts and the claim marker flow to coordinator adoption. The guard nonce flows from the pending record through the restored brief to the first prompt. Worker completion flows through `worker_done`, not a guessed idle screen. `--remaining` feeds hand-back; `left_open` from closeout feeds a report entry and, only under a fresh approval, another round. Exposes the claim marker, `next-steps.md`, the launch result file, `plan_body.py check` (states absent, repeated, empty, placeholder, ok), the result comment from planb's `complete.py`.

### 2.5 Integrity rules shared by these interfaces

<!-- Source: Base (V3 section 4 "Integrity rules shared by these interfaces", kept whole) plus invariant probe INV-001, INV-004, INV-006, INV-012, INV-013, INV-016, INV-027; merged per plan change #7 -->

Each write carries one stable action id. Use exclusive creation for a new issue state, a temporary file plus rename for replacement, and flush the file and its parent directory before acknowledging. Reject symlinks, oversize JSON, unsupported schema versions and a mismatched repository, issue, target or round. A duplicate wake returns the existing state and acknowledgment; it cannot overwrite a newer round. Lock contention returns a named busy result and does no outward work. Never take the watcher and coordinator locks in opposite orders: the producer releases its lock before delivery; the consumer commits its state before publishing the ack. The poll verifies that the referenced issue state exists and matches the wake and round before it accepts `accepted`. Missing state leaves the wake in place: this is Rule B, the merge check MC-6.

Separate the claim attempt from the adoption delivery. Outbox replay keeps the wake id; a retarget links a new id and generation. Failed moves remain replayable. Startup reconciles the outbox, wakes, states and consumed goes before any new work. Nudges carry the wake id only. A typed line goes only to an idle person-opened or just-started session: empty draft, 60 seconds quiet, main prompt visible, never busy or in a check wait. An unreadable process list means unknown, and nothing starts. There is no listener process.

The existing PR 686 writer already has a size check, exclusive temporary creation, fsync and rename (pr-a `wake.py:269-299`); its ack parser expects the bucket `taken`, not `accepted` (pr-a `wake.py:545-581`). Rename the schema and both readers together, with a pinned pair test. Never accept an old-schema empty acknowledgment as success. Shared terminal behaviour gets one package helper and a parity fixture test, not another copy of the report helper (pr-a copies about 100 lines of `orca_term.py`; D15 row B9).

<!-- Source: invariant probe INV-001, INV-004, INV-006, INV-012, INV-013, INV-016, INV-027 -->

Additions from the invariant probe:

- **One state root (INV-001).** Every consumer reads `state_dir` from the per-repo config and never recomputes it. Today the cycle default uses `XDG_STATE_HOME` else `HOME`, while `run-all` and the generator use `HOME` and a short-name folder (planb `cycle.py:194-199`, `generate.py:42, 245`); a coordinator that recomputed the root would never see the poll's wake files.
- **Store downgrade (INV-004).** Before the store schema changes, the migration writes a backup. An old binary refuses a newer store (`store_invalid`, planb `record.py:225-228, 263-267`), so every rollback that crosses a store version runs the downgrade step that restores the backup (MC-11).
- **Child PATH (INV-006).** `run-all` passes absolute `gh` and `orca` paths to every child and to its own precheck; a cron-environment run is a merge check (MC-12).
- **One round writer (INV-012).** The poll owns the hand-back round number in the store; the per-issue file copies it; the ack echoes it; a mismatch is refused with a named reason and never retried silently.
- **Attempt counter (INV-013).** The delivery attempt (1 to 3) keeps its value across a replay. A replay increments it only on a real send, so a crash loop can neither reset it forever nor spend attempts without sending.
- **Ack names each item (INV-016).** An ack names each wake item it accepted or skipped; an ack that names no item is invalid. At cap 1 a wake holds one issue, but the rule holds before the cap is raised.
- **Replay despite failing prechecks (INV-027).** Outbox replay must also run when the repository's GitHub prechecks fail, when an earlier launch stops the loop, or when a rate wait applies. `status --json` lists stranded intents older than a limit, and the observer shows them.
- **One writer per counter (INV-011).** The poll is the single writer of the dispatch store; the coordinator is the single writer of its per-issue files; the poll reads the per-issue phase and closes the store entry in its next cycle (K9). Section 4 lists one writer per file.

## 3. Contradictions between verdicts

<!-- Source: union of V1 section 3, V2 section 3 and V3 section 3 into K1 to K23 (K24 added by post-review fix B1), merged per plan change #8; picks are the plan's "Final decisions" (debate round 2 C-001, C-002, C-003, C-009, C-014, X-001 to X-005) -->

The K numbers name contradictions between verdicts, not risk scores. A pick resolves the implementation recommendation; it does not answer an owner-only consent question, and section 7 lists those. D15's later summary governs its own stale action rows: its order-code definition (D15:18) agrees with D14, so this spec uses that definition and D14's lanes. D10 expressly does not choose who claims (D10:28), so K1 changes no settled D10 ruling.

| id | Verdicts in conflict | The pick | The reason | What would reverse it |
|---|---|---|---|---|
| K1 who claims | D04 and the built poll (it launches `/sc:issue --claim <N> --pipeline none`, master `launch.py:33`, `cycle.py:1026-1112`) against D10 and Clay's wave 1 (the poll only wakes; the coordinator claims). D10 leaves it open | The poll claims at `--pipeline none` as built; the coordinator ADOPTS. On the marker the poll sets `claimed` (MR-2 holds), saves the delivery intent in the SAME store save as the claim evidence, releases its lock, then publishes the ids-only wake. Replay keeps the wake id; a retarget creates a linked new id. The wake means "claimed, take over". The coordinator reads `launch_cwd` from the store through `state` (INV-018). Key `claim_by` (`poll` default, `coordinator` reserved) names the reversal, built only if X-001 or the owner calls for it. Poll-launched claims run only on a throwaway issue until X-001 is settled | Keeps MR-2, the tested prompt and the built duplicate guard; `refs/claim.md:96` already describes a coordinator adopting a level-none claim. Cost: one model session per claim | X-001 shows a lingering claim agent, or the owner picks OA-23 (a): `claim_by: coordinator`, and `marker_in_window` moves into the coordinator's re-check |
| K2 guard level of a `worker-start` worker <!-- Source: post-review fix B2, B3 --> | D05 (bind provisionally at FS) against D06 (no outward action by a worker; push only on a person's go; `/sc:pr-submit` never a worker), D04 (no governed level before the ship gate) and the owner's G2 route A (bind at the worktree level; the coordinator writes the worker's `.ok` after the recorded plan approval, master `docs/designs/issue-pipeline-guard-g2.md:14, 22`); the owner's work wins | When both gates stay (OA-1 default), bind at W (`orca_worktree.py pending --level worktree`, marker from the restored `brief.py`, preflight, gone-check on a stated timeout, stop and escalate otherwise). Implementation is refused (LL-IMPL) until the coordinator, after the recorded plan approval, releases the worker by writing its `.ok` (route A, restored `release-worker`), which makes the level WA: implement allowed, commit, push and PR still refused, exactly as at F; the guard then enforces the plan gate. If OA-1 keeps only the start gate, bind at F. Fallback: how the coordinator learns the worker's session id is UNVERIFIED (G2 design section 4; FU-1 precondition f); if it cannot, bind at F and the plan gate rests on the contract only. The coordinator commits after `worker_done` with explicit paths plus `.dev/tasks`, never `-A`, never `.dev/issues/` (INV-020), after a branch and base check (INV-007); a refused or rewritten commit is escalated (INV-019). Push and `/sc:pr-submit --monitor 3` only on a person's typed go, in a person-opened top-level session. No marker-bearing text reaches a coordinator (INV-017). **INV-025 (HIGH, carried): the guard narrows honest drift; a worker that writes and runs a script is not stopped** (master `hooks/scripts/launch-level-guard.sh:771-772`); L2 refuses only `main` and `master` (master `hooks/scripts/launch-level-pre-push.sh:6-9`); `gh` writes have no L2. A ruleset on `master` and `integration` stops a push to those branches and, if the worker's login cannot bypass it, a merge into them. It does not stop a feature-branch push, a pull request or a comment. With the recommended admin bypass on one shared admin login, a worker's own script can still run `gh pr merge --admin`; only a separate login for agents (OA-6, third option) plus the ruleset makes "a worker cannot merge" true. A person's go is a procedure, not a block. Every control here narrows | No built level allows commit without push: IMPL passes at WA, F and FS, and COMMIT, PUSH and SUBMIT are refused at W, WA and F (master `hooks/scripts/launch-level-guard.sh:785-790`); WA is W plus the `.ok` file (`:265-272`), and at F the guard never reads `.ok`, so only W then WA lets the guard enforce the plan gate. FS lets a worker push, which D06 forbids. WC:244-246 already make the coordinator committer and pusher | The probe shows W or WA breaks planning or `/sc:implement`, or the session id cannot be obtained (bind at F), or the owner wants unattended PRs: FS plus a ruleset, or a new reviewed guard level, after issue 442's observations (OA-20) |
| K3 revert of PR 682 against D05 | D03 and D14 (revert restores `brief.py` with the marker slot, `release-worker`, WC-17, G2 rule 1) against D05 (assumes PR 682 stands: marker line in a new template, rule 1 stays removed) | The revert of PR 682 wins, conditional on OA-1. The restored `brief.py` (planb's stage-aware version, marker line kept) is the one builder of the worker's first prompt; there is no second `handoff-prompt.md`. G2 rule 1 returns with the restored verbs; D05's other binding steps stay. WC-17 references in planb's brief are valid again after the revert | D05 item 6 itself requires a tamper class back if approval or release verbs return, which the revert does. One prompt builder, not two | OA-1 answered "only the start gate": PR 682 stands under D03's three conditions and D05 applies as written. Which verb exposes `brief.build` is UNVERIFIED (checked in S6) |
| K4 config file and poll command | D07 and planb (no registry, per-repo files, `run-all`) against D04, D06, D09 and D11 (which cite pr-a `repos.yaml` keys) and D02 (master and pr-a `once` plus `repos.yaml`) | Cron runs `issue-watch run-all`, which runs `once --config <config_dir>/<repo>.json`; no registry, no `repos.yaml`. Config stays `schema_version` 1. The loader's key list (`_TOP_KEYS`, defined at master `cycle.py:58`, checked at `:216`; planb `cycle.py:59-72, 223-233`) widens in the PR that first READS each key: S9 adds loader support for the keys planb reads (authority and merge keys shaped at O1, carried on planb at O2), and each later PR adds support for the keys it first reads (consumed at O5); the `owner/name` rekey is at O6 (D15 rows C3, C4). <!-- Source: post-review fix N2, N4 --> An absent key that grants authority means the most restrictive value; `reach_daily_max` grants nothing (it only limits notices, D11), so absent or 0 means no notice cap; any malformed value is a config error. Rollback restores old config files; the STORE has its own versioned migration with backup and downgrade (INV-004). `run-all` passes absolute `gh` and `orca` paths to children, since cron has `PATH=/usr/bin:/bin` (INV-006). Zero repos served is an alarm (INV-014) | D07 and D15 R-3 chose the home; key names from pr-a `repos.py:47-84, 295-299`. Both loaders reject unknown keys and any version but 1, so a version bump only changes the error text | OA-3 answered "`once` plus `repos.yaml`" (D07 overruled), or Coder issue 516 fails to create the `Coordinator` worktree, so `run-all` serves no repo (`worktree_invalid`) |
| K5 where state lives | D10 (`<orchestrator-repo>/.orchestrator/wakes/`) against D07 (no separate repo; records under `.dev/coordinators/` in each project), D08 renames, and D15's substrate wording "git-ignored" (D15:224) | Machine state in the per-repo state root OUTSIDE any checkout, named by the config key `state_dir` and never recomputed (INV-001): `dispatch.json`, `audit.jsonl`, `DISABLED`, `wakes/`, `issues/<owner>__<repo>__<N>.json`, `goes/`, `grants-use.jsonl`. <!-- Source: post-review fix B5 --> Human-readable records, including the imported interim ledger, live ONLY on the local `coordinators` branch in the `Coordinator` worktree, written by local commits of the recorder and never part of a PR to master; pushing that branch is an outward action needing a person's go (OA-26, INV-024). Go entries are consumable runtime state, never tracked; a consumed go is never restored; an uncertain merge is reconciled against the exact head | State in a worktree invites accidental commits; the state root already holds `dispatch.json` outside git (master `cycle.py:187-192`); git history must not restore a consumed permission | Poll and coordinator on different hosts; then a git-ignored folder in the `Coordinator` worktree with the path passed in the wake line |
| K6 standing grants | D04 and Q01 (four standing, including `issue.hold`) against Q03 (no label write) | Default empty and fail closed; at most three standing (`issue.assign`, `issue.comment`, `issue.body.append_plan_sections`); `issue.hold` dormant (Q03); `pr.merge` and `issue.close` never standing; the owner names the subset once in chat and an agent records it with the `repos` verb | A grant for a write the poll never makes is a trap (Q03); D15 R-4 resolved the count | A later label-write PR lands after its own 24-hour shadow run and cron write test |
| K7 Project reads | D04 (no Project read while no governed level is open) against D01 (Status allow-list R22, `Approved` field R35) | Read Status and `Approved` every cycle and at the start-time re-check; the Status value (Research, Spec, Plan, Debug) picks the worker's stage in the stage-aware brief; the Pipeline field is never read while `GOVERNED_LEVELS_ALLOWED` is false | D04 itself defers approval and Status signals to D01; its concern is Pipeline, which picks a governed level | The owner opens a governed level after D04's gate-open design |
| K8 one plan check | D12 and D15 R-2 (`plan_body.py check`, imported by `hold.py`) against D01 and D09 (`hold.py plan_check`); no package code may import a skill script | `plan_body.py check` is the reference; the package holds a copy `issue_watch/plan_check.py`; one shared case table of fixtures drives both in a parity test (pattern `tests/issue_watch/test_origin_parity.py`). Align first in PR 690's adaptation (S2): commented-out headings and `<...>`-only sections count as empty; the heading count is fence-aware. Presence only, not quality | The package cannot rely on an installed skill folder, and the skill's interpreter cannot rely on the package; copy plus parity is the repo's only precedent. The two checks disagree today on commented-out headings (pr-a `hold.py:122` strips closed comments; `plan_body.py` does not) | A small library both can import, or the skill calling `superclaude coordinator plan-check`; then the copy goes |
| K9 sessions in flight (with K17) | D07 (`max_in_flight` default 3; claim agents share the `Coordinator` worktree) against D10 ("one launch per sweep") | `max_in_flight` = 1 first. One writer per counter: the poll writes the store, the coordinator its per-issue file; the poll reads the per-issue phase and closes the store entry next cycle (INV-011). The poll owns the hand-back round; the file copies it; the ack echoes it; a mismatch is refused with a named reason (INV-012). Counted: `pending, launched, claimed, woken, acked, unknown` plus unclosed claim files, each issue once; an unreadable file counts and `status` says why (INV-008). `waiting_reapproval` is excluded and expires (K15). An issue waiting for a push or merge go counts, is shown "waiting on a person" with a reminder, and never expires away committed work (INV-023) | Master has no cap; D07's closing writer is "not yet designed"; cap 1 limits, but does not remove, the X-001 overlap | Live proof that claim agents and workers each run in their own worktree, plus the closing-writer and expiry tests (C-INV-1); then the owner raises the cap (OA-14) |
| K10 watcher state on the screen | D09 and Q03 (held issues show only in `issue-watch status` and the audit log) against D11 (the sweep makes no GitHub call; one source) | The observer reads `issue-watch status --json` directly (master `cli.py:165`), extended with `last_sweep_at`, `recent_skips`, stranded deliveries, served-repo count with a zero-repos alarm, and an unreadable-state alarm. The sweep stays the one source of SESSION facts, changed only by `session_id`, `worktree_path` and a saved JSON file (S5) | The verb exists, is tested and has no reader; the sweep stays free of watcher calls (debate C-005, X-006) | Per-repo subprocess calls prove too heavy for the observer's 15-second refresh (UNVERIFIED); then `run-all` writes one aggregate status file and the observer reads it |
| K11 who starts a coordinator | D10 item 8 (the poll starts one if none is live) and D07 item 4 (restart) against D06 (script start only at depth 0 under a recorded authorization) | A person opens it. A script start happens only under a recorded owner authorization, after the depth-0 start is proved (U3) and WC:70 and WC:245 are approved in chat. Key `coordinator_autostart` (absent means false); skip reason `coordinator_absent`; an unreadable process table starts nothing. `/sc:pr-submit` runs only in a person-opened ordinary top-level session until then (A-005) | D06 is the stricter authority rule; D10's start is transport, not authority | The owner allows automatic start in chat (OA-18) after U3 passes |
| K12 close after merge | D13 (closeout needs `issue.close`) against D04 and D06 (no standing close); D15 R-5 left it open (C-INV-4) | The merge go entry names the PR and its linked issue; one go covers the merge and that close. A separate close go is the alternative. A `Fixes` line in a PR body still makes GitHub close the issue at merge; this is stated as a limit (C-INV-4) | One answer per PR and no standing close | The owner wants a separate close go per PR (OA-12); a standing close grant is never offered (owner rule) |
| K13 cron timing | D02 and D14 lane 3 (fix the cron line early) against D14 lane 2 (`run-all` lands with planb, after the revert) | Text fixes only before the live test; no stage installs a cron entry before S17; the hand-installed entry on this host does not count as the image | A cron line on `once` plus `repos.yaml` would be a third contract | None expected |
| K14 restart target before Coder issue 516 | D07 item 4 (duty holder `ORCH-IronClaude` until 516) against D08 (`COORD-<RepoName>`) | Per-repo key `coordinator_session` (default `COORD-<RepoName>`; until Coder issue 516 an owner-recorded `ORCH-IronClaude`); nothing restarts any session before 516 creates the worktree; an `ORCH-*` name is never restarted by default | Restarting a retired name would bake it into the store; a later rename costs one config edit, not a code change | Coder issue 516 lands |
| K15 hand-back round 2 | D01 item 5 and D15 R-6 (a re-plan voids approval) against pr-a `cycle.py:993-994` (an acknowledged entry is never woken again) and the D07 cap (C-INV-1, C-INV-2) | New state `waiting_reapproval`: outside the cap, re-checked by the poll each cycle, given a NEW wake id when the start rule passes again, expiring to `stopped` after an owner-set limit | The poll already owns the start rule; a coordinator copy would duplicate it | The owner answers "carry the remaining list, no re-approval" (OA-14) |
| K16 the worker-binding staging constant | D05's staging shorthand "real issues unbound and flagged" (D05:21) against the owner's G2 sentence that no other issue runs before binding (master `docs/designs/issue-pipeline-guard-g2.md:9`, kept by D05:47); also D03 and D04 (R33 in the watcher) against D05 (re-home the switch into the coordinator) | `WORKER_BINDING_PROVEN`, false by default: the coordinator starts NO worker on a real issue; it refuses a worker start for any issue not in the per-repo key `probe_issues` (throwaway issues, recorded by an agent from the owner's chat words), and a probe worker is flagged <!-- Source: post-review fix N8 -->; the worker is bound at W then WA (or F) as K2 says; a reviewed commit flips it after the live probe passes. Separate from `GOVERNED_LEVELS_ALLOWED`, which stays false. The owner's G2 sentence wins over D05's shorthand until the owner says otherwise in chat (D05 action 1) | R33 keeps its watcher meaning; worker binding needs its own switch, and false must refuse, not flag (debate C-003, X-002, X-003) | The owner merges the two gates into one, or approves an unbound real issue in chat (OA-20) |
| K17 cap vocabulary | D07 (counts `pending, launched, unknown`) against K1 (new states `claimed, woken, acked`) | Merged into K9: one counted set and one limits table | Without it a woken but unacknowledged issue would not count and the cap could be exceeded | None expected |
| K18 label creation against NG-2 <!-- Source: post-review fix B1 --> | D09 and Q03 (label creation moves to per-repo init) against D01 and NG-2 (the poll writes nothing) | The poll cycle `once` writes nothing to GitHub (NG-2). The one-time creation of the trigger and `hold:backlog` labels is a GitHub write of planb's init path (`first_run` and `repo_init`, planb `first_run.py:193`, `repo_init.py:108`), which D09 rule 2 allows ("per-repo init creates both labels once"); because `run-all` reaches that path on its own for a new repo, it still needs the owner's chat OK on how NG-2 is read (OA-28) and is held back by K24 until then. The poll reads the labels and skips quietly if one is absent | NG-2 is about the poll cycle; the pinned argv tests (`tests/issue_watch/test_security_invariants.py:652, 683`) keep covering it | The owner wants zero GitHub writes in setup: the labels are created by hand and init only checks |
| K19 sweep JSON location | D11 (owner decides: saved beside the report, or each reader sweeps) against WC-16 (one sweep per five minutes) and the observer's 15-second refresh | Saved beside the Markdown report as `<UTC>-sweep.json` (owner decision OA-9) | An observer running its own sweep every 15 seconds would break WC-16; the sweep already writes one file per run | The owner chooses "each reader sweeps" and WC-16 changes |
| K20 order of planb and the revert | D14's action table (planb after the revert) and D15 O2 ("landed first") against the seed brief ("planb lands first") | Revert, then contract and guard amendment, then planb rebased and landed, then design amendment, then adapted PR 686. "First" means first before PR 686. Planb carries the skip reasons and the start-time re-check (D15:220) | Planb edits `issue_pipeline/`, which exists only after the revert; on a post-682 master that is a modify/delete conflict never tried. D03: the owner's 13-file patch applies to the revert tree and fails on current master | OA-4 answered differently, or the S6 dry run fails: then planb rebases onto master with the package re-added by hand, an untested path |
| K21 where owner answers are recorded before any coordinator exists | Q01 (an agent records every answer) against D07 and D08 (records under `.dev/coordinators/`, which does not exist yet); debate A-003 | An interim ledger: one file in the unification work's task package under `.dev/tasks/` (always staged), one entry per answer with Q01's fields (quoted words, date, exact scope, who recorded). At S13 the recorder imports it by a LOCAL commit on the `coordinators` branch in the `Coordinator` worktree; the import is not part of any PR to master, and pushing the branch needs a go (OA-26) <!-- Source: post-review fix B5 -->. The owner never writes it. The file name is UNVERIFIED. Risk: staged-only content can ride into an unrelated commit or be lost (INV-003), so the recorder commits it when the owner says (OA-24) | No variant named a home; an existing task package can serve today, a future coordinator folder cannot | The owner names another home in chat (OA-24) |
| K22 same short name | Planb keys configs, state folders and worktrees by the Orca short name (planb `dispatch.py:206-207`, `generate.py:205, 245, 252`) against D07 item 7 (`owner/name` keys, at O6) | Until the `owner/name` rekey (S12), a duplicate short name is a `name_collision` skip, tested; `COORD-<RepoName>` collisions are handled by the `coordinator_session` key before any enable (INV-015) | Two repos with one short name would share a config, a state folder and a worktree, the second never served | None expected after the rekey |
| K23 notice cap | D15 row D17 (cap of 5 deferred, default 0) and C-INV-3 (D15:142: a bad value must not silently mean no cap) against pr-a `repos.py:262-269` (invalid values are mapped to 0) | Absent or 0 means no notice cap, because the key grants nothing (D11) <!-- Source: post-review fix N2 -->; malformed input is a config error, never read as 0; the notice mechanism and its authorization stay separate; a cap of 5 remains a proposal (OA-16) | A valid uncapped limit settles no permission; durable entries are never dropped | The owner sets a number in chat |
| K24 planb `first_run` against NG-2 and the one-throwaway-repo rollout <!-- Source: post-review fix B1 --> | Planb's zero-setup requirements R17 and R18 (a listed repo with no config is generated, its label created and its config switched on by `first_run`: planb `dispatch.py:404-417`, `first_run.py:3, 16-17, 99-107, 136-137, 193`, `repo_init.py:72, 108-117`) against NG-2 and the rule that only ONE throwaway repo is enabled, on a go (S17) | `run-all` is NOT scheduled before S17. S9 adds a defaults key `auto_enable` (default false): `first_run` still generates the config and runs its checks, but does not rewrite `enabled: true` until the owner turns the key on (OA-28: keep R18 default-on after the throwaway run, or require a per-repo recorded go). D01 and D03's condition "R33 before R18" is met, because planb has `GOVERNED_LEVELS_ALLOWED = False` (planb `launch.py:48`). `run-all --dry-run` only reports `would_generate` (planb `dispatch.py:406-410`) and is the only form run before S17 | Without it, landing planb and scheduling cron would, with no per-repo go, write a label to GitHub and switch every new repo on | The owner keeps R18 default-on after the throwaway run (OA-28): `auto_enable` true in the defaults file |

<!-- Source: debate round 2 (X-001); rounds/round2-advocate-3-haiku-backend.md section 3c; round2-advocate-1 new evidence -->

**X-001 (open status, blocks real rollout): the shared `Coordinator` worktree.** The poll launches the claim agent into `<worktrees>/<repo>/Coordinator` (planb `generate.py:252`; planb `launch.py:136-157`; planb `cycle.py:1179`), the same worktree where the standing coordinator lives. Nothing shows the claim terminal closes after the claim ends: `refs/claim.md:94` ends the level-none procedure after the comments, and its "no agent is launched" concerns the skipped downstream launch, not the running claim session. REAL ROLLOUT STAYS OFF until a live check records: whether the claim agent is still alive after the claim ends; a complete source of live agents; and the worker's worktree path. Then the owner picks in chat (OA-23):

- (a) `claim_by: coordinator`. Recommended default if a lingering claim agent is seen: it avoids a second agent in that worktree and keeps the claim files where the coordinator copies them from (`refs/claim.md:96`).
- (b) A separate claim worktree. It costs a change to Coder issue 516's single worktree and to the `launch_cwd` handoff.
- (c) A person closes the claim terminal after each claim. This is not zero setup.

A wake-time "refuse writes while another agent is live" check is kept as a narrowing control only if a complete source of agent identities is proved; the claim skill's `worker-list` recovery reconciles supervised workers and does not establish that it lists ordinary poll-launched claim agents. Cap 1 alone does not remove the overlap.

<!-- Source: Base (V3 section 3 code-basis paragraph), citations kept -->

**Code basis.** For K2: master `hooks/scripts/launch-level-guard.sh:785-790` allows IMPL at WA, F and FS and COMMIT, PUSH and SUBMIT at FS only; `:265-272` turn level W into WA when the session's `.ok` file exists <!-- Source: post-review fix B3 -->. For K15: pr-a `cycle.py:992-994` returns early for every non-failed prior entry ("already woken, acknowledged or abandoned: never woken again"). For K16: the owner's G2 sentence is at master `docs/designs/issue-pipeline-guard-g2.md:9` ("Before any other issue runs through the flow, the worker must be bound to the guard").

## 4. Interface table

<!-- Source: V1 section 4 (26 rows), V2 section 4 (27 rows, renumbered), V3 section 4 (validation rules, built column); merged per plan change #9; host paths replaced by variables per debate S-004 -->

The table uses variables and config keys, not host paths; a host resolves them at install time. `<config_dir>` is the per-repo config folder (default `~/.config/superclaude/issue-watch.d`). `<state_dir>` is the per-repo state root named by the config key `state_dir` (K5). `<worktrees>` is Orca's worktree root. `<log_dir>` is the log folder (default `~/.aidev/logs`). `<guard_state>` is the guard's state folder (default `~/.claude/state/launch-level`). `<repo-key>` reversibly encodes a validated `owner/name` as `owner__name` and rejects collisions. "Built" uses the ledger words of section 6 and refers to master unless a branch or PR is named. Evidence retention grants no commit or push authority.

| # | Name | Format or path | Writer | Reader | Owner piece | Built today |
|---|---|---|---|---|---|---|
| 1 | Cron line | Five fields `*/5 * * * *`; `flock -n <host lock>`; absolute path to `superclaude issue-watch run-all`; output to `<log_dir>/issue-watch.log` | Coder template (issue 515), after host consent | cron | Watcher | NOT BUILT in the image (hand-installed on this host 2026-11-18, which does not count) |
| 2 | Dispatcher | `superclaude issue-watch run-all` (options `--dry-run --config-dir --state-dir --worktrees-dir --orca --superclaude`); loops over `orca repo list`; runs `once --config <config_dir>/<repo>.json` per repo with absolute `gh` and `orca` paths; 270-second total cap | cron | none | Watcher | planb only (planb `cli.py:432-518`, `dispatch.py:314`) |
| 3 | Host lock | `run-all.lock` in the dispatcher's state folder; non-blocking | Dispatcher | Other dispatcher runs | Watcher | planb only |
| 4 | Defaults file | `~/.config/superclaude/issue-watch-defaults.json`; gains `auto_enable` (default false, K24) <!-- Source: post-review fix B1 --> | Install or init | Poll, `run-all`, `first_run` | Watcher | planb only; `auto_enable` NOT BUILT |
| 5 | Per-repo config | `<config_dir>/<repo-key>.json`, `schema_version` 1. Planb keys: `enabled` (false), `repo`, `labels`, `project_id`, `owner_account_id`, `worktree`, `approvers_file`, `state_dir`, `approval_excluded_ids`. Added keys (each in the PR that first reads it, K4): `grants` (empty), `max_in_flight` (1), `reach_daily_max` (absent or 0 means no notice cap; malformed refused), `probe_issues` (empty), `coordinator_session`, `coordinator_autostart` (false), `claim_by` (`poll`), `wake_enabled` (false), `coordinator_tier`, `worker_tier`, `plan_depth`, and a `merge` block (`merge_method`, `release_head`, `release_merge_method`, `can_merge`, `reviewers`, `merge_safety_files`). A missing authority key means the most restrictive value | `generate.py` creates it and `first_run` rewrites `enabled: true` only when `auto_enable` is on (K24); afterwards only the `coordinator repos` verb on a recorded chat go, run in a person-opened session (the recording agent in the owner's own session); it refuses when run from a worker-bound or coordinator-started session (`refuse(argv)` plus the C-INV-3 hook) <!-- Source: post-review fix B1, N9 --> | Poll, dispatcher, coordinator (read only), report config reader | Watcher, with coordinator authority validation | planb shape (name-keyed, planb `generate.py:195, 252`); added keys NOT BUILT; Clay's key names only in pr-a `repos.py:47-84, 295-299` |
| 6 | Old single config | `~/.config/superclaude/issue-watch.json` | Person | Master poll; report skill (`orchestrator_repo`) | Watcher | BUILT; retired by S9; report re-pointed in S16 |
| 7 | Dispatch store | `<state_dir>/dispatch.json`, versioned typed JSON, keyed by issue; states `pending, launched, claimed, woken, acked, unknown, failed, abandoned, waiting_reapproval`; typed delivery-intent fields (wake id, repository, issue, round, target generation, attempt); restart counter | Poll only, under its store lock; `reset N` by a person | Poll, `status`, cap check | Watcher (private) | BUILT with six states (master `record.py:34-35`); new states, intent fields and migration NOT BUILT |
| 8 | Store backup | `<state_dir>/dispatch.json.v<old>.bak`, written before a migration; restored by the downgrade step (INV-004) | Migration step | Downgrade step | Watcher | NOT BUILT; file name UNVERIFIED |
| 9 | Kill switches | `enabled` key (absent means off, master `cycle.py:228`); `<state_dir>/DISABLED` file; presence blocks launch and wake delivery | Person or agent with consent | Poll | Watcher | BUILT (master `record.py:283`) |
| 10 | Audit log | `<state_dir>/audit.jsonl`, 5 MiB rotation, one closed reason per line | Poll only | `status`, person | Watcher | BUILT (master `audit.py:124-128`); recomputed reason set NOT BUILT |
| 11 | Local holds | `holds` entries in the dispatch store; `would_hold` reasons `held_incomplete`, `held_backlog`; no GitHub write | Poll only | `status --json` (`recent_skips`) | Watcher | NOT BUILT on master (pr-a has a label-writing variant) |
| 12 | Trigger and `hold:backlog` labels | Issue labels set on an issue by a person; the poll only reads them; created once by planb's per-repo init (`first_run`, `repo_init`), a GitHub write that needs the owner's chat OK (K18, K24, OA-28) | Person (on issues); init (label creation) | Poll | Watcher | Trigger-label creation planb only; `hold:backlog` NOT BUILT on master (pr-a reads it) |
| 13 | Claim prompt | `/sc:issue --claim <N> --pipeline none`, pattern at master `launch.py:33` | Poll through `orca agent launch` | Claim session | Watcher to claim pipeline | BUILT |
| 14 | Claim marker | Exact HTML comment `<!-- sc:issue:claim -->` on the claim comment (master `predicates.py:14`) | `/sc:issue --claim` | Poll `marker_in_window` (master `predicates.py:279`); adoption check | Claim pipeline | BUILT-ON for a person's claim; the timer path is off |
| 15 | Claim files and `launch_cwd` | `.dev/issues/<N>/` (summary, `next-steps.md`) in the checkout that ran the claim; `launch_cwd` saved in the store entry (planb `record.py:184`) | Claim session; poll saves `launch_cwd` | Coordinator, through the `state` verb (INV-018) | Claim pipeline | Files BUILT; read through `state` NOT BUILT |
| 16 | Claim launch result file | Saved by PR 693 (issue 691); exact path and shape UNVERIFIED | `/sc:issue` | Coordinator, report | Claim pipeline | PR 693 OPEN |
| 17 | Wake file | `<state_dir>/wakes/<wake_id>.json`; schema `coordinator-wake/1`; immutable id envelope, target generation, poll evidence ids, attempt 1 to 3; items are `repo`, `number`, `url` only, no titles or free text; temp plus rename, mode 0600, at most 64 KiB | Poll, from the saved delivery intent | `wake-check`; the coordinator's pull at every `check --wait` return | Watcher | pr-a only, as `orchestrator-wake/1` in `.orchestrator/wakes` (pr-a `wake.py:46, 69`) |
| 18 | Acknowledgment | `<state_dir>/wakes/<wake_id>.ack.json`; schema `coordinator-wake-ack/1`; buckets `accepted`, `skipped`, `rejected`; names each item (INV-016); carries the matching issue-state revision and round; written only after the per-issue state exists (M1) | Coordinator (`wake-ack`) | Poll, which records it in the store under its own lock | Coordinator | pr-a only, bucket `taken` (pr-a `wake.py:47`, `:545-581`); M1 NOT BUILT |
| 19 | Nudges | Mailbox message kind `coordinator-wake`, payload `{"kind","wake_id"}`; typed line `/sc:coordinator --wake <id>` only to an idle or just-started session after a screen-tail check; agent start through a fixed `orca agent launch` builder after U25 | Poll | Coordinator session | Watcher | pr-a only, orchestrator names; U5 and U25 UNVERIFIED |
| 20 | Per-issue state | `<state_dir>/issues/<repo-key>__<N>.json`; exclusive create; schema, round (copied from the store), revision, wake id, claim evidence, `launch_cwd`, phase, worker id, nonce, worker worktree path, approval binding, PR, head sha, terminal outcome | Coordinator (`state` verb), single writer under the coordinator lock | Ack validator, poll (phase, to close the store entry), cap, restart, audit, `handback` | Coordinator | DESIGN ONLY |
| 21 | Human records | Only on the local `coordinators` branch in the `Coordinator` worktree, by local commits, never in a PR to master: per-issue `summary.md`, dated audit notes, quoted owner rulings, the imported interim ledger and retained evidence | Coordinator (an agent records consent) | People, report, reviewers | Coordinator | DESIGN ONLY; pushing the branch needs a go (INV-024, OA-26) |
| 22 | Interim owner-answer ledger | One file in the unification work's task package under `.dev/tasks/`; one entry per answer: quoted words, date, exact scope, who recorded | An agent, from the owner's chat words | Every stage's precondition check; imported at S13 by a local commit on the `coordinators` branch | Coordinator (interim) | NOT BUILT; file name UNVERIFIED (K21) |
| 23 | Launch marker and pending file | `[sc-launch:v1:<32 lowercase hex nonce>]` in the worker's first prompt; `<guard_state>/pending/<nonce>` holds the bare level word, mode 0600; binding recorded under `<guard_state>/sessions/<session_id>` | Coordinator runs `orca_worktree.py pending --level worktree` (or `--level full` in the fallback, K2); the restored `brief.py` adds the marker | Guard L1 (master `hooks/scripts/launch-level-guard.sh:318-319`); the coordinator's gone-check | Claim pipeline and guard | `pending` and guard BUILT (master `skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523`); preflight and caller NOT BUILT |
| 23a | Release file | `<guard_state>/sessions/<worker session id>.ok`, a regular file, never a symlink; turns level W into WA <!-- Source: post-review fix B3 --> | Coordinator, through the restored `release-worker`, after the recorded plan approval (route A); the worker cannot write it (G2 rule 1, TAMPER) | Guard L1 for a W-bound session (master `hooks/scripts/launch-level-guard.sh:270-271`) | Claim pipeline and guard | Guard read BUILT; `release-worker` REMOVED by PR 682; how the coordinator learns the session id UNVERIFIED |
| 24 | Worker brief | Restored `issue_pipeline/brief.py` plus `templates/worker-brief.txt`, marker line included, stage-aware (Status picks the stage, K7) | Coordinator | Worker | Coordinator | REMOVED by PR 682; present in planb's working tree |
| 25 | Plan approval | Restored `issue-pipeline` verbs `plan-hash`, `check-approval`, `stage-status`, `release-worker`; approval record and session `.ok` file | Coordinator under plan consent | Guard, worker start | Claim pipeline | REMOVED; restoration pending OA-1 |
| 26 | Worker completion | Run mailbox `worker_done` with worker id and outcome, handled once per message id | Supervised worker | Coordinator state transition | Coordinator | General route BUILT; issue wiring NOT BUILT |
| 27 | Grants and use log | `grants` list in the per-repo config (default empty; names limited to the three of K6; `pr.merge` and `issue.close` refused as names); `<state_dir>/grants-use.jsonl` | An agent through `repos grant` on a recorded go; verbs append uses | `refuse(argv)`, `E-NO-GRANT`, audit | Coordinator | DESIGN ONLY (pr-a reads a YAML list at `repos.py:295`, not landed) |
| 28 | Merge go entry | `<state_dir>/goes/<PR>-<sha12>.json`: repository, PR, 40-character head sha, method, the word `merge`, linked issue to close (optional), gate output id, quoted words, times, recorder, question key, consumed flag; one-shot; void on head move or new gate reason | An agent, after `answer-check` passes on the typed answer | `coordinator merge`, audit | Coordinator | DESIGN ONLY |
| 29 | Merge gate | `coordinator merge-gate --repo <R> --pr <N> --json`: `ok` plus reasons from a closed list of 13, plus "no recorded merge go"; read-only | Coordinator | Person before the go; merge verb again before `gh pr merge` | Coordinator | DESIGN ONLY |
| 30 | `answer-check` | Checks Q01's four tests: right entry, newer than the entry's last edit, question key (for example `merge_safety:<PR>:<head sha>`), owner identity as a parameter | Coordinator | Merge verb, `repos` verb | Coordinator | DESIGN ONLY |
| 31 | Coordinator verbs | `superclaude coordinator wake-check / wake-ack / state / plan-check / repos / merge / merge-gate / answer-check / audit / report-entry / escalate / handback`; one JSON contract; one state lock | Runner | Skill, tests, report | Coordinator | NOT BUILT |
| 32 | Coordinator command | `/sc:coordinator [--wake <id>] [--hourly] [--resume] [--take <owner/repo#N>] [--sub]`, skill `sc-coordinator-protocol`, installed under `~/.claude/commands/sc/` and `~/.claude/skills/` | A person; the dispatcher only when `coordinator_autostart` is recorded | Claude Code | Coordinator | DESIGN ONLY |
| 33 | Escalation | `coordinator escalate --kind <k> --issue <N>`: one entry line, then the notice step through the nine-row table; no interrupt | Coordinator | Person, report | Coordinator | NOT BUILT |
| 34 | Hand-back | `handback` reads `left_open`, re-plans through `/sc:issue --plan --remaining`; round 2 passes the start gate again through the poll (`waiting_reapproval`) | Coordinator | Poll | Coordinator | DESIGN ONLY; `--remaining` in PR 690 OPEN |
| 35 | Watcher status | `superclaude issue-watch status --json`: typed scalars from `dispatch.json` and the `DISABLED` file; added `last_sweep_at`, `recent_skips[]` (closed reason, `owner/name`, number), stranded deliveries older than a limit, served-repo count with a zero-repos alarm, unreadable-state alarm with the reason | Watcher, read-only, no `gh`, no lock | Observer, person | Watcher | Verb BUILT with no reader (master `cli.py:165`); added fields NOT BUILT |
| 36 | Sweep JSON | Schema v1, 12 top-level keys (`schema_version, observed_at, collected, scope, window, orca_available, sources, rows, worktrees, waiting, summary, report_path`); rows gain `session_id`, `worktree_path` (empty allowed); saved as `.dev/sweeps/<UTC>-sweep.json` beside the Markdown report | `/sc:sweep` | Observer, work report, coordinator | Observability | Standard output only BUILT (master `cli/sweep/commands.py:277-278`); fields and saved file NOT BUILT |
| 37 | Report entry files | `<report_state_dir>/<repo-key>__<N>.json` in the report skill's per-user state path (D11); the legacy default folder name is `.dev/coordinator/orchestrated/` (singular, D08); issue narrative, links and `session_id` only, never a copied session class | `report-entry` only | Report `run.py refresh` and exclude, observer | Coordinator writes; observability owns the read contract | Readers BUILT (PR 684); writer NOT BUILT |
| 38 | Report runtime state | Configurable per-user `report_state_dir` (default `~/.local/state/superclaude/work-report/`); no registry lookup | Report runner | Report and observer adapters | Observability | Rehome NOT BUILT |
| 39 | Plan check | Reference: `plan_body.py check` (installed at `~/.claude/skills/sc-issue-protocol/scripts/plan_body.py`); package copy `issue_watch/plan_check.py`; one shared case table; states absent, repeated, empty, placeholder, ok; stdin body, stdout JSON | Skill; watcher copy | Claim rule C1, `--plan`, poll start rule, `coordinator plan-check` | Claim pipeline and watcher | PR 690 OPEN (pr-p `plan_body.py:138`); pr-a `hold.py:122` differs; copy NOT BUILT |
| 40 | Result comment | `<!-- sc:issue:result issue=<N> run=<id> -->` | `complete.py` | Poll, report | Claim pipeline | planb only |
| 41 | Closeout and cleanup | `/sc:closeout <PR>` output with `left_open`; cleanup `list` (dry run, table of worktree, branch action, PR head and keep reason) and `--apply` on a named go | Coordinator (closeout and list), person-approved apply | Coordinator, owner chat, `handback` | Claim pipeline | Closeout BUILT (PR 683); cleanup NOT BUILT (issue 687) |

<!-- Source: invariant probe INV-011 and INV-012; plan change #9 "who writes what" -->

**Who writes what (exactly one writer per file).** A second writer for any file below is a defect. Shared readers are fine.

| File or record | The one writer | When it writes | What the others do |
|---|---|---|---|
| `dispatch.json` (including delivery intents, acks recorded, hand-back round, store-entry close) <!-- Source: post-review fix N3 --> | The poll, under its store lock; the only other writer is a person's `reset N`, a person-run verb that takes the same lock | Each cycle; after reading a matching ack or a closed per-issue phase; on a person's reset | Coordinator reads it only through `status`; never takes the store lock (INV-022) |
| `audit.jsonl` | The poll | Each skip or transition | Read by `status` and people |
| `wakes/<id>.json` | The poll | After the store save that holds the intent | Coordinator reads and never edits it |
| `wakes/<id>.ack.json` | The coordinator (`wake-ack`) | After its per-issue state is saved | Poll reads it and records the result in the store |
| `issues/<repo-key>__<N>.json` | The coordinator (`state`) | Each phase change, under the coordinator lock | Poll reads the phase; copies of the round come from the store (INV-012) |
| `goes/<PR>-<sha12>.json` | Created by the recording agent through the `coordinator` verbs after `answer-check`; marked consumed only by the merge verb | When the owner types a go; at the merge | Nothing restores a consumed go |
| `grants-use.jsonl` | One writer function: the single `coordinator` verb wrapper that every grant-using verb calls | At each use | Audit reads it |
| Per-repo config | `generate.py` at setup and `first_run` (rewrites `enabled` only when `auto_enable` is on, K24); afterwards only `coordinator repos` on a recorded go, in a person-opened session | At setup; on a recorded answer | Poll, dispatcher and coordinator read only |
| Release file `sessions/<sid>.ok` | The coordinator through `release-worker` | After the recorded plan approval | Guard reads it |
| Report entry files | `report-entry` | At each issue status change | Report and observer read |
| Sweep JSON file | `/sc:sweep` | Each sweep | Observer, report and coordinator read |
| Interim ledger | The recording agent | At each owner answer | Imported once at S13 by a local commit on the `coordinators` branch |

## 5. Staged migration

<!-- Source: V2 section 5 (stage structure and MC-1 to MC-10), V1 section 5, V3 section 5 (merge gate M, go/no-go evidence); stage list S0 to S17 from the plan, merged per plan change #10; MC-11 and MC-12 from invariant probe INV-004 and INV-006 -->

**Rules for every stage.** Each stage is one reviewable PR, one local action, or one consented host operation. A stage never enables a later stage by itself. <!-- Source: post-review fix B1, B4 --> No stage schedules `run-all` or installs cron before S17; only `run-all --dry-run` runs earlier; `auto_enable` stays false (K24), so no config is switched on and no label is created on its own, and the `DISABLED` kill file works throughout. Every stage reverts by reverting its PR. "Go" means the owner's chat go for that named action, recorded by an agent in the interim ledger (K21). A person's typed go is REQUIRED before any push or merge; every stage that opens or merges a PR lists "owner's go for this PR" in its preconditions. Every proposed test is an acceptance requirement, not a reported passing test; test names marked NEW are suggestions. Run every suite through `uv run`; run `make sync-dev` but never stage the generated `.claude/` mirrors. A green PR 686 alone does not prove the combined tree.

**Mechanical merge checks, defined once.**

- **MC-1** `uv run superclaude --help` exits 0.
- **MC-2** Every package under `src/superclaude/cli/` imports (NEW `tests/cli/test_cli_packages_import.py`).
- **MC-3** Names check: every name the restored `issue_pipeline` package imports from `issue_watch` exists (35 names; 9 are missing on the PR 686 head, among them `EVENTS_JQ`, `argv_edits`, `github.edits`, `github.events`) (NEW `tests/issue_watch/test_restored_package_names.py`).
- **MC-4** Removing the approval between wake and start refuses (NEW `test_start_refuses_when_approval_removed_between_wake_and_start`, on top of `_revalidate`).
- **MC-5** `enabled` absent means off (NEW `test_enabled_key_absent_means_off`).
- **MC-6** Rule B (M1): an acknowledgment with no per-issue state file leaves the wake entry in place (NEW `test_ack_without_state_file_leaves_wake_entry`).
- **MC-7** `make verify-sync` passes and no `.claude/` path is staged (project rule).
- **MC-8** NG-2: `test_every_argv_of_the_cycle_is_an_allowed_form` and `test_the_five_cycles_together_use_every_allowed_form_and_nothing_else` (`tests/issue_watch/test_security_invariants.py:652, 683`) pass with no write verb in the allowed forms.
- **MC-9** `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`: every hit is justified (installed primitives use `~/.claude/...` paths).
- **MC-10** The reasons table equals the code's reason set: the 14 approval reasons are present; `coordinator_full`, `name_collision`, `no_checkout` and `coordinator_absent` are present; `registry_invalid`, `repo_not_listed` and the four label-write reasons are absent (NEW, rewrites pr-a `tests/issue_watch/test_audit.py:86-98`).
- **MC-11** Store version pair (INV-004): an old binary given a new store fails closed with a named reason, and the downgrade step restores the backup so the old binary runs again (NEW `test_store_downgrade_restores_backup`).
- **MC-12** Cron environment (INV-006): `env -i PATH=/usr/bin:/bin <absolute path>/superclaude issue-watch run-all --dry-run` serves every configured repo or names why it did not; zero repos served is an alarm, never "clean" with exit 0 (INV-014); and the run generates nothing: no config file is created or rewritten and no GitHub call writes (it only reports `would_generate`, K24) <!-- Source: post-review fix B1 -->.

**Stage map.** The bracket after each stage names D14's lane and D15's order code.

| Stage | Lane / order | One line |
|---|---|---|
| S0 | H0 / O0 | Hold PRs 686 and 690; ruleset recommendation; first owner answers; interim ledger |
| S1 | lane 1 / O1 | Merge PR 693 |
| S2 | lane 1 / O1 | Adapt and merge PR 690, with the K8 alignment |
| S3 | lane 1 / O1 to O3 | Claim rule C1 and the plan-less warning |
| S4 | lane 3 / O1 | Text, names, glossary, runbook fixes, PR 685 |
| S5 | lane 3 / O1 | Sweep contract note, two fields, saved JSON |
| S6 | lane 2 / O2 | Revert dry run, no PR |
| S7 | lane 2 / O2 | Revert PR 682 |
| S8 | lane 2 / O2 | Contract and guard amendment |
| S9 | lane 2 / O2 | Land planb |
| S10 | lane 2 / O2 | Design amendment (gate for S13 onward) |
| S11 | O3 | PR 686 adapted in place, one draft |
| S12 | lane 3 / O6 | Watcher status extension and `owner/name` rekey |
| S13 | O4 | Coordinator substrate |
| S14 | O5 | Merge path as one tested unit plus the bound worker route (W, then WA) |
| S15 | O6 | Transport, cap, restart, audit, hand-back, report-entry, cleanup list (four PRs) |
| S16 | lane 3 / O6 | Observability glue |
| S17 | O7 | Live tests, then enable one throwaway repo |

S1 to S5 do not depend on lane 2 and can run beside it. <!-- Source: post-review fix N4 --> S9 adds loader support for the keys planb reads; each later PR adds loader support for the keys it first reads, so no key waits for S12, and S13 and S14 do not depend on S12; S12 carries only the status extension and the `owner/name` rekey, the O6 part (debate C-007; D15 rows C3, C4).

**S0. Hold and first answers [H0, O0].**
- Scope: no code. Ask Clay to mark PRs 686 and 690 drafts and not merge (D14 H0; D16 rank 2). Recommend the ruleset on `master` and `integration` with an admin bypass for pull requests only (D14; D16 rank 5; only the admin can set it). The owner answers OA-1 to OA-8 and OA-24 in chat; an agent creates the interim ledger (K21) and records each answer. D16's other items are listed as proposals under OA-5.
- Checks: read-only, for example `gh pr view 686 --repo IronbellyOrg/IronClaude --json isDraft` and a read of the branch protection of `master`. If the owner creates a ruleset, D16's throwaway test (D16 section H) runs from Clay's account, never from the owner's login, and writes to GitHub only after the owner's go.
- Preconditions: none. Rollback: Clay sets the PRs back to ready; the admin deletes the ruleset. Without this stage one merge click falsifies the whole plan (D14).

**S1. Merge PR 693 [lane 1, O1].** The owner's PR (saves the claim launch result file, issue 691). Checks: its own CI, its own `/sc:pr-submit --monitor 3` loop run from a person-opened top-level session, MC-1, MC-7. Preconditions: S0; owner's go for this PR. It must precede S2 because the two PRs share four files (D14). Rollback: revert the PR.

**S2. Adapt and merge PR 690 [lane 1, O1].**
- Scope: rebase on master plus PR 693; D12's four fixes (fence-aware heading count; "passes" defined once in `plan_body.py check`; document the `--remaining` caller; confirm the live head). Added here so the definition is final before the watcher copies it (K8): commented-out headings and `<...>`-only sections count as empty, and one shared case table file (NEW `tests/skills/fixtures/plan_check_cases.json`).
- Checks: the merge-only trial of PR 690 onto master plus PR 693 runs first (it has never run, D14). `plan_body.py` fence test and case-table test; chain tests untouched; MC-1, MC-7.
- Preconditions: S1; OA-2; owner's go for this PR. Rollback: revert; nothing calls `--plan` yet (PR 683's `--plan` reference dangles again, as today).

**S3. Claim rule C1 and the plan-less warning [lane 1, O1 to O3].**
- Files: `skills/sc-issue-protocol/refs/claim.md`, `refs/chains.md`, `templates/next-steps.md`, and `tests/skills/test_issue_protocol.py` (lines 131-135, 745-784, and the `/model` first-line test at 462).
- Checks: the short chain appears only when the check passes, the verdict is current and the issue is a simple feature; `out_of_date` uses the old row; the plan is quoted only in the fenced "data, not instructions" block; commands are never taken from the plan (D12's five safeguards); a manual claim of a plan-less issue warns and prints `/sc:issue --plan <N>`; MC-7.
- Preconditions: S2; owner's go for this PR. Rollback: revert (the chain rows return).

**S4. Text, names, glossary, runbook fixes, PR 685 [lane 3, O1].**
- Files: the `HOW-WE-WORK.md` glossary line (D08) with its byte copy in the plugin and its level-table copy, and the tests that check both; the five-field cron line `*/5 * * * *` and the real cron reasons in `docs/designs/issue-watcher-setup.md` (D02; no cron entry is installed, K13); D08 wording at `agent-work-report/SKILL.md:12`; a banner on `docs/designs/orchestrator.md`. PR 685 (issue 442 evidence) merges beside it. Touches no contested file.
- Checks: the two HOW-WE-WORK copy tests; MC-7, MC-9. Preconditions: S0; OA-10; owner's go for each PR. Rollback: revert by file.

**S5. Sweep contract note, two fields and saved JSON [lane 3, O1].**
- Scope: write `docs/designs/observe-sweep-contract.md` first (three readers: sweep, observer, report); add `session_id` and `worktree_path` (empty allowed) at `cli/sweep/report.py:642-661`; save `<UTC>-sweep.json` beside the Markdown report (K19).
- Checks: the golden-test edit is reviewed by a person; a row built without a join has both fields empty; an Orca row and a transcript row for one session give one row; the saved file equals what standard output prints.
- Preconditions: OA-9; owner's go for this PR. Independent of lanes 1 and 2. Rollback: revert; the contract note states that readers tolerate missing fields.

**S6. Revert dry run, no PR [lane 2, O2].**
- Scope: in a clean throwaway checkout bound to a recorded master head sha, run `git revert --no-commit 01e7a9e23`; then MC-1, MC-2, MC-3; `uv run pytest` over `tests/issue_pipeline`, `tests/hooks/test_launch_level_guard_worker.py`, `tests/skills/test_worker_contract.py`, and the full suite including `tests/hooks/test_launch_level_guard.py` (it did not finish in D03). Run `git apply --check` of planb's 1,767-line, 13-file patch on the revert tree (D03: it passes there and fails on master). Find which verb exposes `brief.build` (K3).
- Output: a dry-run record (sha, commands, results) kept in the revert PR body. Repeat if master moves.
- Preconditions: OA-1 answered "both gates stay"; otherwise PR 682 stands and S7 to S9 change (K3). Rollback: delete the checkout.

**S7. Revert PR 682 [lane 2, O2].**
- Scope: `git revert 01e7a9e23` as one new PR, never a force push (4,599 lines: 2,969 test, 1,618 source, D03). By hand: re-apply the standalone "ask and send carry no `--to`" bullet and its assertions (`tests/skills/test_worker_contract.py` lines 426-429 and 3220); resolve `CHANGELOG.md`. In the same PR: correct the three "gate retired" statements in `docs/designs/orchestrator.md` and add the banner "contested, not owner-approved; checked 2026-11-20" (D14).
- Checks: MC-1, MC-2, MC-3, MC-7; `uv run superclaude issue-pipeline --help`; G2 rule 1 tamper tests in `tests/hooks/test_launch_level_guard_worker.py`; the restored 117 test functions in `tests/issue_pipeline/`; a test that the no-`--to` sentence is present.
- Preconditions: OA-1, OA-4; S6 passed at the current master sha; S0; owner's go for this PR. It must land before PR 686 merges in any form, because together they break `superclaude --help` (D03). Hosts are untouched: no `superclaude install` here. Rollback: revert the revert (one commit).

**S8. Contract and guard amendment [lane 2, O2].**
- Files: `core/WORKER-CONTRACT.md` lines 57, 70 and 245 (these three match master's numbering: checked) and lines 298 and 300 plus guard comment lines 441-443, which are numbered as in the pre-deletion tree `01e7a9e23^` (on master after PR 682 those lines hold other text) <!-- Source: post-review fix N13, B6 -->; `core/CLAUDE.md:58`; contract tests; plugin mirror; `make sync-dev`. The installed line 57 sentence ("a grant row or a pass record ... still written by the owner") contradicts the owner's standing order that every approval is given in chat and recorded by an agent and that the owner never writes a file. It becomes "given by the owner in chat and recorded by the agent" (Q01 item 2), shipped as its own commit after the owner's ONE chat confirmation. One sentence binds coordinator-started workers at W then WA, or F in the fallback (K2), and states that binding narrows honest drift (INV-025). Lines 70 and 245 (script-started coordinator at depth 0; push for Full Submit as the person's go) are separate commits that wait for the owner's chat approval of R25, R17 and R9 (OA-7); they are not in force until then. The guard change gets an independent review.
- Checks: `tests/skills/test_worker_contract.py` finds no "still written by the owner"; amended sentences pinned; guard tests; MC-7, MC-9.
- Per-host rule: before any `superclaude install` on a host, diff the installed guard and contract against the repository; never a blanket `--force` until the eight removal PRs are confirmed (OA-21; PR 633's retire step would remove skills of PRs 632, 650, 656, D14 NB-1).
- Preconditions: S7; OA-7 for line 57 at least; owner's go for this PR. Rollback: revert; the split commits let line 57 stand alone. If OA-1 keeps only the start gate, S8 shrinks: no restored text, only lines 57, 70 and 245 of master's contract plus D05's marker line in a new handoff template.

**S9. Land planb [lane 2, O2].**
- Scope: commit planb, push it as a DRAFT, rebase onto the post-S8 master; expect modify/delete conflicts on `issue_pipeline/`; do not resume its half-finished `/sc:implement` ledger (D14). Planb carries (D15:220) the skip reasons `held_incomplete` and `held_backlog`, the start-time re-check of approval, `unchanged_since`, Status, `hold:backlog` and the plan check (MR-1), the claim-marker test (MR-2), R33 before R18, loader support for each key it reads including the authority and merge keys planb carries (K4), absolute child paths (INV-006), and the corrected requirements line 18 and Coder issue 515 text (D02 item 3). <!-- Source: post-review fix B1 --> It also adds the defaults key `auto_enable` (false): `first_run` generates the config and runs its checks but does not rewrite `enabled: true` while the key is false, and the trigger-label creation inside `first_run` runs only after OA-28 (K24). It brings `run-all`, `dispatch.py`, `generate.py`, `repo_init.py`, `first_run.py`, `defaults.py`, the stage-aware `brief.py`, `complete.py` and `GOVERNED_LEVELS_ALLOWED = False`.
- Size: 69 code, test and doc files; 23 overlap PR 686, 7 of them source (D14). The owner may split it into dependency-ordered PRs with the same checks.
- Checks: planb's `tests/issue_watch/test_dispatch.py` (loop, rotation, 270-second cap) and `test_cycle.py`; MC-1 to MC-5, MC-7 to MC-9, MC-12; a test that no governed level launches while R33 is false; NEW `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing`. If OA-1 keeps only the start gate, planb rebases onto a tree without `issue_pipeline`, an untested path.
- Preconditions: S7; S8 (at least line 57); OA-4; OA-28; owner's go for this PR. Rollback: revert and restore the old config files; master returns to the single-config poll, still off.

**S10. Design amendment [lane 2, O2]. The gate for all coordinator code.**
- Scope: docs only. Rewrite the contested rows of `docs/designs/orchestrator.md` to this spec (rows 73, 76, 81, 116-118, 135, 138, 267-305, 343-354, 610-620, 749, 763-764 per D15; registry sections 4.4, 5.7, 6.2 per D07; DQ7, OD1 and the design's own "workers run unbound" risk row per D05; DQ8 and R10 per D06; R4 and 4.8 per D02), or write a new `docs/designs/coordinator.md` with the old file bannered. Every control is written as "narrows", never with the opposite verb.
- Checks: a grep test that `orchestrators.json` and `repos.yaml` occur only in a "rejected" table (D07 item 2); a grep that no control is described as fully solving a risk (D06 item 10); MC-7.
- Preconditions: S9; owner rulings recorded; owner's go for this PR. No stage from S13 on starts before this merges (D14, D15). Rollback: revert by file.

**S11. PR 686 adapted in place, ONE draft [O3].**
- Who edits: OA-2. Not split (D15:219).
- Scope: rename every persisted name to coordinator BEFORE any merge (schemas, mailbox kind, tier key, folder, typed line, golden fixture, verb group; D08); wake and ack under `<state_dir>/wakes/` (K5), ids only, `wake_enabled` false by default; typed delivery-intent fields with the store migration, backup and downgrade (MC-11); replay despite failing prechecks with a stranded-delivery alarm (INV-027); M1, M2; unreadable process table means unknown; one shared terminal helper with a parity test against `orca_term.py`; label writer stripped (removed hunk saved as a patch; Q03); reasons pin recomputed (MC-10); `would_hold` and local `holds`; the plan-check copy (K8). Keep every D01 symbol and MC-3's names. No registry, `repos.py`, `repos.yaml` or `wrong_target`.
- Checks: MC-1 to MC-11; `test_hold.py`; NEW `test_plan_check_parity.py` (loads `plan_body.py` by path over the S2 case table); renamed `test_wake.py`; the zero-write NG-2 test restored (pr-a tree `tests/issue_watch/test_security_invariants.py:12`; master's NG-2 bullet is line 10); NEW `test_manual_claim_gets_no_wake` (N7: a delivery intent only for entries the poll launched), `test_abandoned_wake_is_retargeted_with_new_wake_id`, `test_wake_file_has_no_title_or_free_text`, `test_full_wake_with_139_char_repo_names_fits_64_kib` (a title-bearing wake measured 77,271 bytes, D10), `test_replay_runs_when_prechecks_fail`, `test_attempt_counter_survives_replay` (INV-013), `test_ack_naming_no_item_is_invalid` (INV-016).
- Preconditions: S2, S9, S10; OA-2; D08 names; owner's go for this PR. Rollback: revert; `wake_enabled` is false and the downgrade step restores the store; delivery files are kept.

**S12. Watcher status extension and `owner/name` rekey [lane 3, O6].** <!-- Source: post-review fix N4 -->
- Scope: `status --json` gains `last_sweep_at`, `recent_skips` with closed reasons, stranded deliveries older than a limit, the served-repo count with a zero-repos alarm, and an unreadable-state alarm with its reason (K10, INV-008, INV-014). The `owner/name` rekey of config, store and worktree, with the `name_collision` skip (K22). Keys are not added here: each key's loader support lands in the PR that first reads it (S9 for planb's keys, S14 for the merge and grant keys, S15 for the cap and session keys); in each, a malformed `reach_daily_max` is a config error (K23) and `merge_safety_files: []` and empty `reviewers` are refused at load (C-INV-3).
- Checks: NEW `test_two_repos_one_name_both_skipped_name_collision`; `status --json` schema pinned; a fixture with one unreadable store shows `read: false` for that repo only; MC-5, MC-8, MC-12.
- Preconditions: S9, S11; owner's go for this PR. Rollback: revert the PR AND remove the new keys from generated files, because the loader rejects unknown keys (master `cycle.py:216`; planb `cycle.py:223`).

**S13. Coordinator substrate [O4].**
- Scope: the verb group `superclaude coordinator` skeleton: runner, `refuse(argv)` with N6 unconditional and no interrupt, one JSON contract, one state lock, one path map read from the per-repo config (`state_dir`, INV-001); the config-folder write guard for coordinator sessions (C-INV-3). <!-- Source: post-review fix B5 --> Separately, the recorder imports the interim ledger by a LOCAL commit on the `coordinators` branch in the `Coordinator` worktree (K21); that import is not part of this PR or any PR to master. No GitHub write, no skill.
- Checks: one failing test per refusal pattern (NEW `tests/coordinator/test_refuse_argv.py`); `test_state_lock.py`; `test_state_exclusive_create`, `test_state_revision_conflict`, `test_config_weakening_refused`; symlink, size and schema cases; JSON golden; a test that the path map never recomputes the state root; the hook test for the config folder; `tests/skills/test_primitive_dual_surface_lookup.py` extended; MC-1, MC-2, MC-7, MC-9.
- Preconditions: S10 merged; OA-26 (for any push of the records branch); owner's go for this PR. Rollback: revert; nothing calls the verbs yet.

**S14. Merge path as ONE tested unit plus the bound worker route [O5].**
- Merge scope: the `merge` verb, the go entry, `merge-gate` run twice, `answer-check` (Q01's four tests; it narrows a stale or mistyped go and cannot tell a person from a script), `E-NO-GRANT` with the use log, the `repos` verb guard, the reviewer hold, the linked-issue close under the go (K12), T13.
- Worker scope: <!-- Source: post-review fix B3, N8 --> the K2 and K16 route with `WORKER_BINDING_PROVEN` false: `pending --level worktree`, then route A's `release-worker` writing the `.ok` after the recorded plan approval (F in the fallback); loader support for `probe_issues`, the merge block and `grants`; the commit rules of K2; the `/sc:coordinator` command and `sc-coordinator-protocol` skill (person-opened only; edited under `src/superclaude/`, then `make sync-dev`; installed paths only inside them, MC-9), including the restored plan-approval step if OA-1 keeps both gates.
- Checks: T13 as `tests/coordinator/test_merge_path.py`: a passing gate without a go does not merge; a go for head X does not release head Y; a relayed, stale, wrong-entry or wrong-key go is refused; any change of reason, threads, review state, base or draft between gate runs refuses; `--auto`, `--admin`, `--delete-branch` refused; `changes_requested` not overridable; `checks_failing` and `merge_safety` only with their own key; an uncertain result is reconciled; a consumed go is not restored. Binding: a fake `worker-start` without the marker leaves `pending/<nonce>` and triggers the stop; no `jq` means no worker (D05 item 2); NEW `test_worker_start_refused_for_real_issue_while_binding_unproven` (an issue not in `probe_issues`); at W an implementation command is refused before release and allowed after the `.ok` is written; `release-worker` refuses without a recorded plan approval. Invariants: marker-bearing text never reaches the coordinator (INV-017); a hook refusal or rewrite escalates (INV-019); no `.dev/issues/` and no `-A` (INV-020); a moved branch or base stops the commit (INV-007). Skill-text scan for commands outside "Will Not Do". MC-1, MC-2, MC-7, MC-9.
- Preconditions: S13; OA-6, OA-11, OA-12, OA-13, OA-27; C-INV-3 and C-INV-4 choices; owner's go for this PR. Rollback: revert; merges are typed by hand again.

**S15. Transport, cap, restart, audit, hand-back, report-entry, cleanup list [O6; four PRs].**
- **S15a** `wake-check` and `wake-ack` (M1), the pull at each `check --wait` return, nudges with the screen-tail check, session start by `orca agent launch` after the tag spike. Kill-and-restart tests at every persistence boundary: around the joint store save, after publication, after the consumer state save, after the ack, after the producer's ack save (section 8.1). Needs U25 and OA-18 for any typed line.
- **S15b** Cap with single writers (INV-011, INV-012), "waiting on a person" shown with a reminder (INV-023, OA-25); closing writer and expiry first, then `max_in_flight` 1 and `coordinator_full`; guarded restart with a persisted counter of 3 (K11, K14). Tests: drain after an orphaned `pending`; one issue counted once; three `unknown` entries do not block forever; an unreadable file is named; a blind process table starts nothing; restart stops at 3.
- **S15c** AU1 to AU8 (AU5 narrowed), `handback` with `waiting_reapproval` (C-INV-1, C-INV-2), `report-entry`, `escalate`. Tests: round 2 passes the start gate with a NEW wake id; three waiting hand-backs never cause `coordinator_full`; `report-entry` is the only writer.
- **S15d** Cleanup `list` (issue 687 adapted, Q02 refusals before removal, report-only the first week). Tests: refuses `master`, `main`, `integration`, the default branch, a branch with an OPEN PR, a foreign head owner; evidence saved before removal; `orca worktree rm` behaviour proved first.
- Loader support for `max_in_flight`, `coordinator_session`, `coordinator_autostart`, `claim_by` and `wake_enabled` lands in the S15 PR that first reads each.
- Preconditions: S14; OA-14, OA-15, OA-16, OA-18, OA-25; Coder issue 516 for restart; owner's go for each PR. Rollback: revert per PR; the cap key is then ignored.

**S16. Observability glue [lane 3, O6].**
- Scope: the observer reads `issue-watch status --json` (K10) and the saved sweep JSON (K19). The report follow-up PR: remove `"person": "clayphi"`; configurable state path; transcripts for the sweep's session ids plus every not-done session of the previous report; `read: false` when Orca is down; the old terminal map removed only after one live side-by-side run.
- Checks: three distinct observer states (empty folder, zero rows, could not read); a sanitize test for entry text; a fixture with a held issue shown with its reason; a stranded delivery and a zero-repos run shown as alarms; entry files carry only `session_id`.
- Preconditions: S5, S12; OA-17; owner's go for each PR. Rollback: revert.

**S17. Live tests, then enable one throwaway repo [O7].**
- Order: Coder issues 515 and 516 land; per-host diff, then `superclaude install`; live checks U5, U25, U28, U3, U8, U54; the X-001 check (claim terminal lifetime, agent-list completeness, worker worktree path), then OA-23.
- Binding probe on a throwaway issue (in `probe_issues`) <!-- Source: post-review fix B3 -->: marker delivered; `pending/<nonce>` gone; at W an implementation command is refused before release; after the recorded plan approval and `release-worker`, at WA, implementation runs; the coordinator learns the worker's session id (or the fallback to F is recorded); one `send` and one `ask` without `--to`; `git commit`, bare and compound pushes refused at W and WA; a scripted push to `master` on a throwaway repo refused (by GitHub only once the ruleset exists); INV-025 demonstrated and recorded: a worker-written script that pushes a feature branch is NOT stopped by the guard.
- Kill-and-resume after `worker_done` (debate A-001); pre-commit behaviour of the coordinator's commit (INV-019); MC-12; the zero-repos alarm; a 24-hour `--dry-run` shadow run of the cron line first (no agent, no config generated, no GitHub write). D02's automation test only if the fallback is wanted.
- Then, each on a recorded go: `auto_enable` (or `enabled: true`) for ONE throwaway repo only, after OA-28 covers its label creation; cap 1; one approved throwaway issue; a person's go at every push and merge; `WORKER_BINDING_PROVEN` flipped only by a reviewed commit after the binding probe (OA-20). The go/no-go record names code head, host, installed primitive hashes, fixture captures and failed as well as passed probes; an agent records it.
- Preconditions: S14 to S16; OA-19, OA-20, OA-23, OA-28; all HIGH rows of section 8 proven or accepted in chat. Rollback: `DISABLED`, `enabled: false`, or remove the cron line; no data is deleted.

<!-- Source: Base (V3 section 5 closing paragraphs) -->

**What S17 does not include.** Raising the cap, activating Pipeline-field governed launches, adding label writes, `claim_by: coordinator`, and polling from a second host are separate future changes, not completion criteria hidden inside S17. Cleanup never uses `--force`, `-D` or `rm`; remote branch deletion is human-only; a git refusal means "kept", not failure.

**If OA-1 keeps only the start gate.** <!-- Source: post-review fix N5 --> PR 682 stands under D03's three conditions (PR B tests exist first, R33 built before R18, a written owner ruling recorded by an agent). S6 and S7 are dropped; S8 shrinks (no restore; lines 57, 70 and 245 plus D05's marker line in a new handoff template); S9 rebases planb onto a tree without `issue_pipeline`, an untested path; K3 flips to D05 as written; workers are bound at F; the plan-approval step and route A leave section 2.2 and S14.

<!-- Source: V2 section 5 final-stage rollback, V1 section 5 final-stage rollback -->

**Rollback summary.** Every stage up to S16 reverts by reverting its PR, and no repo is switched on before S17 (`auto_enable` false, no scheduled `run-all`). Stages that change the store (S11, S15) also run the downgrade step (MC-11). S12 also removes new keys from generated config files. S17 rolls back with the kill file, `enabled: false` or removing the cron line.

## 6. Built today versus not built

<!-- Source: V2 section 6 (evidence column) as the base table, V1 section 6 rows V2 lacks, V3 section 6 consequences; merged per plan change #11 -->

**Words.** BUILT-ON: code exists on master and is wired into a normal install; it does not say any machine has run it. BUILT-OFF: code exists on master but a switch keeps it off or it was never run live. NOT BUILT: no code on master; a branch or open PR may hold a version, named in the evidence. REMOVED: deleted from master by PR 682. DESIGN ONLY: text, no code anywhere. Baseline is the master snapshot, not the stale main checkout. Open-PR and planb code is not shipped. Source ledgers: the two technical references in this brainstorm (`ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md` lines 317-343; `OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md` lines 242-249).

| Piece | Word | Evidence | Consequence | Stage that changes it |
|---|---|---|---|---|
| Single-repo poll `issue-watch once`, start rule, seven read-only calls, claim launch at level none | BUILT-OFF | master `cycle.py:228` (default false); `launch.py:33`; `cycle.py:1026-1112`; never run live; reply fixtures are assumed shapes (`tests/issue_watch/test_github.py:575-583`) | No live shape proof | S9, S11 extend; S17 enables |
| Watcher verbs `status`, `check-config`, `init-state`, `reset`, `once --dry-run` | BUILT-ON | master `cli.py:111-348`; `status --json` at `cli.py:165` | Status has no reader; audit reducer absent | S12 extends |
| Reader of `status --json` | NOT BUILT | no code in `cli/sweep/` or `cli/observe/` reads `issue_watch` | Watcher facts invisible on the screen | S16 |
| Cron entry | NOT BUILT | not in the image; installed by hand on this host 2026-11-18; Coder issue 515 open (D02) | Zero setup unproved | S17 prerequisite |
| Dispatcher `run-all`, per-repo JSON, defaults file, `generate.py`, `repo_init.py` | NOT BUILT (planb only, uncommitted) | planb `cli.py:432-518`, `dispatch.py`, `generate.py:195, 252` | Not shipped | S9 |
| `GOVERNED_LEVELS_ALLOWED = False` (R33) | NOT BUILT (planb only) | planb `launch.py:48` | Must exist before R18 | S9 |
| `COORD-<RepoName>` session and `Coordinator` worktree | NOT BUILT | Coder issue 516 open; until then planb `dispatch.py` returns `worktree_invalid` for every repo (D07) | Nothing to wake | S17 prerequisite |
| `/sc:issue --claim` waves 0 to 8, levels none, worktree, full, full submit | BUILT-ON | master `commands/issue.md:9, 30, 43-48, 66-69` (levels and flags) <!-- Source: post-review fix N13 --> | A person types it | S3 adds rule C1 |
| Launch guard L1, L2 pre-push, job identity, G2 rule 2 | BUILT-ON | master `hooks/scripts/launch-level-guard.sh:785-803` (levels W, WA, F, FS; `.ok` read at `:265-272`), `launch-level-pre-push.sh`, `launch-job-identity.sh` | Governs only sessions a claim launch bound; text-only matching (INV-025); the `.ok` writer `release-worker` is REMOVED | S8 text; S17 probe |
| Live observations OB-H1 to OB-H3, OB-CTX, ship gate (issue 442) | NOT BUILT as proof | `tests/hooks/test_launch_level_observations.py:79-84` skips; the gate is prose | Runbook or fixtures are not live evidence | S17 |
| IR7 missing-L2 refusal | BUILT-OFF | master `skills/sc-issue-protocol/scripts/orca_worktree.py:822` (`IR7_REFUSE = False`) | A warning is not enforcement | none |
| `pending` verb | BUILT-ON | master `skills/sc-issue-protocol/scripts/orca_worktree.py:1515-1523` | Only writes the record | none |
| Caller of `pending`; binding of a `worker-start` worker | NOT BUILT | technical reference rows 10, 18; never observed | RK-1 | S14, S17 |
| `issue_pipeline` package, WC-17, "Issue pipeline duties", G2 rule 1, `release-worker` | REMOVED | PR 682 commit `01e7a9e23`; present at `01e7a9e23^` and in planb | Restoration is conditional on OA-1 | S7 |
| Coordinator skill, `/sc:coordinator`, verb group, wake handling | DESIGN ONLY | `docs/designs/orchestrator.md` (PR 681); no command or skill on master; Clay's "PR B" has no PR or branch | No mechanical merge-go path today | S13 to S15 |
| `merge-gate`, `answer-check`, `E-NO-GRANT`, `refuse(argv)`, audit AU1 to AU8, hand-back, `escalate`, go entry, reviewer hold | DESIGN ONLY | in none of master, pr-a or pr-p (D06; D15 "Strongest points" OURS 3) | Merges are typed by hand | S13, S14, S15 |
| Wake file, ack file, `route.py` counting and restart | NOT BUILT on master; PR 686 OPEN (CI green, `enabled: false`) | pr-a `wake.py:46-47, 69`; nothing on master reads its wake files | Wrong names and order (no M1, M2) | S11 |
| `max_in_flight`, guarded restart | NOT BUILT on master | pr-a `route.py` `in_flight` (registry-bound) | No cap today | S12, S15b |
| Plan check in the poll | NOT BUILT on master | pr-a `hold.py:122` (PR 686 OPEN) | Differs from `plan_body.py` on comments | S11 |
| Label writer of PR 686 | NOT BUILT on master; stripped by S11 | D09, Q03; pr-a `github.py:983-1069` | Never lands | S11 strips |
| `/sc:issue --plan`, `--remaining`, `plan_body.py` | NOT BUILT on master; PR 690 OPEN | pr-p `skills/sc-issue-protocol/scripts/plan_body.py:138` | Needs adaptation | S2 |
| Plan sections in the issue templates | BUILT-ON | PR 661, already on master | Extra layer, never a replacement for approval | none |
| Claim rule C1 | DESIGN ONLY | D12 | Claim still runs brainstorm and design on planned issues | S3 |
| Package plan-check copy and parity test | DESIGN ONLY | K8 | Two copies by design | S11 |
| Claim launch result file | NOT BUILT on master; PR 693 OPEN | D14 | Candidate "claim ended" signal | S1 |
| `/sc:closeout` | BUILT-ON | PR 683, already on master | Close authority still needs design (K12) | S14 wiring |
| Cleanup script, nine rules | NOT BUILT | issue 687 (an issue, not a PR) | Issues are requests, not features | S15d |
| Issue 689 items | NOT BUILT | an issue; split by D12 | Deferred | later, separate issue |
| Sweep (`/sc:sweep`, JSON v1 to standard output, Markdown report) | BUILT-ON | PR 539; master `cli/sweep/commands.py:277-278` | One sweep per run | S5 |
| Sweep `session_id`, `worktree_path`, saved JSON | NOT BUILT | master `cli/sweep/report.py:642-661` rows lack them | Readers cannot join sessions to worktrees | S5 |
| Observer `superclaude observe` | BUILT-ON (read-only) | master `cli/observe/`; questions panel calls Orca itself (`cli/observe/adapter.py:32`) | One-source rule has a named exception | S16 |
| Work-report skill and living-report reader | BUILT-ON | PR 684 | Carries `"person": "clayphi"` | S16 follow-up |
| Report entry-file writer (`report-entry`) | NOT BUILT | technical reference 2.5 | Reader-side code does not establish the producer | S15c |
| TUI dashboard design package (issue 409) | DESIGN ONLY | synthetic prototype, "not a production integration" | Stays a prototype | none |
| Branch protection or ruleset on `master` and `integration` | NOT BUILT | `protected: false`, rulesets `[]`, no CODEOWNERS (D16 section E) | The person's go is the only brake; INV-025 stands | S0 recommendation; admin action (OA-5) |

Consistency note: where D05 and D14 say "built" for the guard, this table says BUILT-ON only for sessions a claim launch bound; no `worker-start` worker has ever been bound.

## 7. Open owner actions

<!-- Source: V1 section 7 (OA-1 to OA-22) as the base text, merged per plan change #12; V2 section 7 and V3 section 7 answers folded in; D16 rank table for OA-5; new OA-23 to OA-27 from debate X-001 and invariant probe INV-003, INV-023, INV-024 -->

**How answers are recorded.** Every answer is given in the owner's chat. An agent records it with the quoted words, the date, the exact scope and who recorded it: in the interim ledger (K21) until the first coordinator exists, then in the coordinator records. The owner never writes a file. Silence is not a yes; until the owner answers, nothing that depends on the answer is switched on, and the spec is written to the recommended answer only as a plan <!-- Source: post-review fix N10 -->. These are choices, not approvals inferred from this spec. Under each question, each line is one possible answer and what it does.

**Needed at S0**

- **OA-1 Do both gates stay (start approval, and plan approval after the claim)?** (D03; D14 Q1)
  - Both stay (recommended): S6 and S7 revert PR 682; K3 applies (restored `brief.py`, G2 rule 1 back, plan-approval step in section 2.2).
  - Only the start gate: PR 682 stands under D03's three conditions; S6 and S7 are dropped; D05 applies as written; planb rebases onto a tree without `issue_pipeline`.
  - Neither: the rollout stops.
- **OA-2 Who adapts PR 686 and PR 690?** (D14 Q2)
  - Clay, in place: review history and credit are kept; the owner reviews each push.
  - An owner session on a new draft: faster control; D14's "adapt in place" is set aside and Clay closes the old PRs.
- **OA-3 Which poll command does cron run?** (D02; D14 Q3)
  - `run-all` over `orca repo list` with per-repo JSON (recommended): K4 stands.
  - `once` plus `repos.yaml`: D07 is overruled; a registry returns and S9 and S11 change shape.
- **OA-4 Order of planb and the revert.** (D14 Q4)
  - Revert first, planb after (recommended): S7 then S9 (K20).
  - Planb first: planb lands on the PR 682 tree and the later revert conflicts with planb's `issue_pipeline` edits; a compatibility trial comes first.
- **OA-5 Server-side ruleset on `master` and `integration`.** (D14; D16 ranks 1 to 7; only the admin can set it)
<!-- Source: post-review fix B2, N12 -->
  - Yes, with admin bypass for pull requests only (recommended): the ruleset stops a push to `master` and `integration` and binds non-owner logins; the owner's own PRs and reverts do not wait. It does not stop a feature-branch push, a pull request or a comment, and on the one shared admin login a worker's own script can still run `gh pr merge --admin`; the coordinator never passes `--admin`. Only a separate login for agents (OA-6, third option) plus the ruleset makes "a worker cannot merge" true.
  - Yes, symmetric (no bypass): the owner's own PRs need a second code owner, who does not exist today.
  - No: a person's go stays a procedure with nothing on GitHub behind it; the guard narrows honest drift only; INV-025 stays fully open (RK-2). Every control here narrows.
  - `integration` in the ruleset (recommended by D16): both branches are protected.
  - `integration` out: anything can be pushed to `integration`.
  - Sole code owner `@ironbelly` (recommended by D16): the incident author is not a listed owner.
  - Another code owner: named in chat; only after that person agrees in writing.
  - A named deputy: the deputy's scope is recorded; no self-ruling.
  - "Nobody": owner absence means waiting.
  - The channel the owner reads: recorded as given, so questions reach the owner.
  - D16's other items (rule text in root `CLAUDE.md`, `.github/CODEOWNERS`, the throwaway test, the announcement, `docs/decisions.md`, the 14-day review) are proposals for the owner, not part of this spec's build.
- **OA-6 Who counts as "the owner" for typed answers on the shared login `ironbelly`.** (D06 item 9)
  - Name one session kind (for example a person-opened terminal the owner tags): `answer-check` test 1 gets a concrete meaning.
  - Leave it unnamed: `answer-check` cannot pass, so S14 ships but every merge stays typed by hand.
  - A separate GitHub login for agents: GitHub-side checks can then prove who acted; it costs setup (how Coder provisions it is UNVERIFIED).
- **OA-7 Wording of WORKER-CONTRACT lines 57, 70 and 245 (master numbering).** (Q01; D06) <!-- Source: post-review fix B6 --> The installed line 57 sentence ("a grant row or a pass record ... still written by the owner") contradicts the owner's standing order that every approval is given in chat and recorded by an agent and that the owner never writes a file. Recommended: ship the line 57 fix in S8 as its own commit after the owner's ONE chat confirmation.
  - Approve all three: S8 lands in full; a script-started coordinator becomes possible under a recorded authorization.
  - Approve line 57 only (the recommended minimum): S8 lands without 70 and 245; `coordinator_autostart` can never be true.
  - Approve none: the installed text keeps contradicting the owner's order, and every agent that reads the contract is told the owner writes grant rows.
- **OA-8 Keep the trigger label?** (D01)
  - Keep for now (verdict default): no change.
  - Drop it: the start rule loses one predicate; a replacement ordering is reviewed; init creates one label fewer.
- **OA-24 Where the interim ledger lives and who commits it.** (K21; INV-003)
  - The task package under `.dev/tasks/` (recommended), committed by the recording agent when the owner says: answers survive a stash or a worktree removal.
  - Another named file: the agent uses it and records the choice there first.
  - No commit until the first coordinator exists: staged-only answers can ride into an unrelated commit or be lost.

**Needed at S4, S5 and S9**

- **OA-28 Planb's default-on first run and its label write (K24, K18).** <!-- Source: post-review fix B1 -->
  - Keep `auto_enable` false and require a per-repo recorded go (recommended): a new repo gets a config and its checks, but stays off until the owner names it in chat.
  - Turn `auto_enable` on after the throwaway run (R18 kept default-on): every repo that passes `first_run`'s checks is switched on by itself.
  - Read NG-2 as covering the poll cycle only, and allow `first_run` and `repo_init` to create the trigger and `hold:backlog` labels once per repo (D09 rule 2): the label write runs at first run.
  - Read NG-2 as no GitHub write anywhere in setup: labels are created by hand and init only checks.

- **OA-9 Where the sweep JSON lives.** (D11; K19)
  - Beside the Markdown report (recommended): one file all readers share; S5 adds the write.
  - Each reader runs its own sweep: no file; readers may disagree within a minute, and WC-16 must change.
- **OA-10 Branch names: `Coordinator` working branch and `coordinators` records branch as two things.** (D08)
  - Accept: the layout of sections 2.2 and 4 stands.
  - One name: the records move onto the working branch, and record commits mix with work commits.

**Needed at S11 to S15** (each item names the stage that first needs it)

- **OA-11 Which of the three standing grants.** (K6)
  - Any subset of `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`: an agent records it with `coordinator repos grant`; the rest fail closed with `E-NO-GRANT`.
  - None: every such write asks the person each time (safest, slowest).
- **OA-12 Close authority after merge.** (K12; C-INV-4)
  - The merge go names the linked issue (recommended): one answer per PR covers merge and close.
  - A separate close go: two answers per PR; closeout waits.
  - Neither: closeout only reports `left_open`; a `Fixes` line still makes GitHub close the issue at merge.
- **OA-13 Go expiry and reviewer hold.** (Q01; D06)
  - A number of hours for a go (24 hours is a suggestion, UNVERIFIED): a stale go dies even if the head did not move.
  - No expiry: a go lives until used, the head moves or the owner revokes it in chat; merge automation stays off until this is answered.
  - Reviewer hold of 60 minutes (UNVERIFIED default): the test uses it.
  - Another hold, or none: the owner's value is recorded; "none" is recorded as an explicit exception.
  - `changes_requested` stays a hard refusal (recommended): no override exists; "no" means a reviewed redesign, not a generic override.
- **OA-14 Hand-back and capacity.** (K15; OD-2; OD-13; K9)
  - Re-approve after a re-plan (default): K15 applies; the expiry number sets when a waiting issue drops to `stopped`.
  - Keep the body and carry the remaining list: no re-approval; `waiting_reapproval` is not needed.
  - Cap 1 (recommended): issues run one at a time.
  - A higher cap: only after the isolation, closing-writer and concurrency tests pass.
- **OA-15 Local `git branch -d` in cleanup.** (Q02)
  - Yes: with Q02's refusals, report-only for the first week.
  - No: cleanup removes worktrees only and branches stay; if Orca cannot keep the branch, the worktree is kept too.
  - Approve the issue 687 cleanup design in chat: S15d builds `list`; each `--apply` still needs its own go.
- **OA-16 Notice cap.** (D11; D15 row D17; K23; first needed at S15c)
  - Accept 5 a day: `reach_daily_max` 5 is recorded per repo; notices are capped, durable entries never.
  - Keep absent or 0 (current default): no cap on notices; the report and screen carry everything.
  - Another number: recorded as given; malformed values are refused.
- **OA-17 Observer entry text and the questions panel.** (D11)
  - Show entry text: shown through `sanitize.py`.
  - Titles only: links and titles, no entry text.
  - Keep the questions-panel exception: the panel keeps its own Orca call, labelled as an exception.
  - End the exception: a shared questions block is designed first.
- **OA-25 Reminder cadence and the meaning of owner silence on a waiting go.** (INV-023)
  - A reminder every N hours through the notice step (owner sets N): the waiting issue keeps its slot and is shown as "waiting on a person".
  - No reminder: the slot is held silently until the owner acts; at cap 1 the repo stalls visibly but quietly.
  - In every case silence never becomes a yes and no expiry drops committed work.
- **OA-26 Does each push of the `coordinators` records branch need a go?** (INV-024; first needed at S13, when the interim ledger is imported by a local commit on that branch)
  - A go per push (recommended): records reach other readers only when the owner says.
  - Keep records local: readers on other hosts do not see them.
- **OA-18 Per repo: `coordinator_autostart` true or false, and is a typed wake line acceptable?** (K11; D15 row B5; first needed at S15a)
  - True: the dispatcher may start or restart `COORD-<Repo>` at depth 0, after U3 and OA-7.
  - False (default): a missing coordinator is reported as `coordinator_absent`; a person opens it.
  - Typed wake line allowed: only to an idle or just-started session after live screen proof (U25).
  - Typed wake line refused: file pull and mailbox only.
- **OA-27 Which `plan_depth` the planner uses.** (OD-1)
  - `quick` (recommended, the `--plan` default): cheapest; the person's approval is the quality gate.
  - `standard`: middle depth.
  - `deep`: full depth, highest cost.

**Needed at S17**

- **OA-19 Per repo: switch on.** (Coder issues 515 and 516 are owner-run and come first) <!-- Source: post-review fix B1 -->
  - Yes for one throwaway repo: after the `--dry-run` shadow run, one recorded config change (`enabled: true` for that repo, `auto_enable` still false for all others), cap 1, `claim_by: poll`.
  - No: the repo stays off.
- **OA-20 Flip `WORKER_BINDING_PROVEN` after the probe; later, open level FS for workers.** (K2; K16) <!-- Source: post-review fix B2, B3 -->
  - Flip after the binding probe passes (W refuses implementation before release, WA allows it after): real issues get bound workers. INV-025 still holds: a ruleset on `master` and `integration` stops a push to those branches and, if the worker's login cannot bypass it, a merge into them; it does not stop a feature-branch push, a pull request or a comment; on the shared admin login a worker's own script can still run `gh pr merge --admin`; only a separate agent login (OA-6) plus the ruleset makes "a worker cannot merge" true. A person's go is a procedure, not a block.
  - Do not flip: no worker starts on a real issue.
  - Open FS later: workers push feature branches and the coordinator only merges; needs the ruleset and issue 442's observations first.
- **OA-23 The claim route after the X-001 live check.**
  - `claim_by: coordinator` (recommended if a lingering claim agent is seen): one session per worktree; the claim files stay where the coordinator copies them from.
  - A separate claim worktree: changes Coder issue 516's single-worktree layout and the `launch_cwd` handoff.
  - A person closes the claim terminal after each claim: not zero setup.

**Not blocking any stage**

- **OA-21 Confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656).** (D14)
  - Confirm: a reviewed host install may proceed after the per-host diff.
  - Do not confirm: only a blanket install stays blocked.
- **OA-22 Answer Clay on issue 450; ask Clay to drop "replaces #450" from issue 655; split issue 689.** (D14; D12)
  - Yes: coexistence is recorded; `--mode other` and the form fields become a small separate issue; the creation redesign (D12 rule B2) stays a separate design.
  - No: the communication stays pending and issue 689's items stay unbuilt.

<!-- Source: post-review fix N12; D15 section 7 recommended answers -->
- **OA-29 Scope of the naming rule (OD-3).** Gates no stage.
  - B, scan only the coordinator's own writers, after U54 (recommended): workers' PR bodies keep today's practice.
  - A or C (narrower or all surfaces): a reviewed rule; attribution unchanged until authorized.
  - No naming rule: no scan.
- **OA-30 A refused mandatory escalation by the name check (OD-4).** Gates no stage.
  - Fail open on delivery (recommended): the escalation is always written, the matched span masked, the refusal logged.
  - Fail closed: a visible local unread item, never a silent loss.
- **OA-31 Channel for audit escalations (OD-5).** Gates no stage.
  - Entry lines only until the notice table is ruled (recommended).
  - Entry lines plus the notice step: the person is notified as well.
- **OA-32 Tags, publication and interrupts (OD-6, OD-7).** Gates no stage.
  - Never tag or publish, never interrupt a running worker (recommended): N6 refuses, N7 stays removed.
  - Allow either: a reviewed authority contract, and for interrupts a receipt proof, come first.
- **OA-33 Build the lease comment now (OD-8).** Gates no stage.
  - No (recommended): single host only.
  - Yes: a stale-lease design comes before any second host.
- **OA-34 List newly assignable issues, `could_assign` (OD-9).** Gates no stage.
  - No (recommended): the info streams stay off.
  - Yes: after a U8 live capture.

The other D15 questions are folded in: OD-1 is OA-27, OD-2 and OD-13 are OA-14, OD-10 is OA-12, OD-11 is OA-11 (empty default), and OD-12 is settled by K4 and C-INV-3 (protected file and fail-closed values).

## 8. Risks and unverified items

<!-- Source: Base (V3 section 8 failure table and limits paragraph); merged per plan change #13 -->

All live behaviour below is UNVERIFIED until the named experiment passes. Proposed test names describe required behaviour, not existing test functions. Crash tests kill the process at each persistence boundary and restart with the same store. No live test was run by this document. Every control is described as narrowing a risk, never as removing it (D06 item 10).

### 8.1 Failure behaviour the crash and recovery tests must prove

| Severity | Failure or unproven behaviour | Required test and safe failure |
|---|---|---|
| HIGH | Timer overlaps, clock jumps, stale lock or partial store | `test_overlapping_poll_one_reservation`: two invocations, one launches; a killed lock holder releases the OS lock; malformed state blocks and is never reset |
| HIGH | Claim launch succeeds but the receipt or save is lost | `test_unknown_launch_no_second_claim`: inject a timeout after success, reconcile marker and operation, no new launch id; the operator sees `unknown` |
| HIGH | Crash after the claim marker, before wake publication | `test_claimed_outbox_replay`: restart emits the adoption wake once with the same id and never re-claims |
| HIGH | Ack before the state or store save, then a crash | Rule B (MC-6): missing or mismatched state keeps the wake; replay adopts once |
| HIGH | Abandoned target | `test_abandoned_retarget`: a linked new wake, no round restart; exhaustion ends as unread |
| HIGH | Blind process lookup | `test_unreadable_proc_unknown`: no launch; U25 proves tag, idle, draft and screen prompt |
| HIGH | Mailbox from outside a Run fails | U5 plus dropped nudges: the bounded file pull still delivers |
| HIGH | Restart storm or false receipt | `test_restart_budget_survives_crash`: three tries persisted; the screen proves readiness |
| HIGH | Worker unbound, released without approval, or a CLI alias bypasses the guard | Live W pending and session proof; implementation refused at W before release and allowed at WA after `release-worker`; commit, push, PR and merge commands refused; installed aliases and preflight tested; the twelve observations kept separate; INV-025 recorded as not covered |
| HIGH | Approval, body or Status changes before start | `test_revoked_between_wake_and_start` (MC-4): no worker; a manual marker causes no duplicate |
| HIGH | Cap race or hand-back deadlock | `test_concurrent_cap_one`: waits excluded, unknown active counted, re-approval wakes a new round |
| HIGH | Weakened config | `test_config_weakening_refused`: raw edit and `repos` update; a malformed cap refuses |
| HIGH | Shared-login spoof, raw merge, unprotected base | Replay narrows stale consent; only a live ruleset proves a server block, and it still does not prove the person's identity |
| HIGH | Merge uncertainty or state change | T13 changes head, base, review, thread, draft and reason; reconcile the exact head; no reused go |
| HIGH | Closeout or a `Fixes` line closes unfinished work | `test_closeout_needs_named_close_go`; demonstrate the `Fixes` limit; keep `left_open` |
| HIGH | Session loss when a worktree is missing | Live map parity; `test_previous_not_done_carried` with Orca down giving `read: false` |
| HIGH | Cleanup loses evidence or a branch | Nine-rule dry run plus protected, default and `integration` branches, an OPEN PR, a foreign owner, dirty or unsaved evidence; prove Orca's behaviour; week one list only |
| MEDIUM | Plan copies disagree; instruction-like plan text reaches a prompt | Shared fixture parity for fences, comments and placeholders; inject an instruction-like plan into fenced data; zero free GitHub text in a wake, argv, mailbox or typed line |
| MEDIUM | Coder image lacks cron or the coordinator, or an install retires wanted skills | Rebuild a fresh workspace and inspect a single timer and target; compare the installed guard and contract before a consented install; a manual-host success is not image proof |
| MEDIUM | Tier, effort, notice cap, binding timeout and hand-back limit assumed | U28 and U30 capture the requested and effective model; record owner values and measured outcomes; 60 minutes, 60 seconds and 3 rounds remain proposals |

Limits stated plainly: verb checks do not cover raw shell; launch authority is self-attested; the guard is not a sandbox; the audit misses direct pushes that open no PR.

### 8.2 Risk register

<!-- Source: V1 section 8 (RK-1 to RK-17), V2 section 8 (R1 to R25), V3 section 8, invariant probe; merged per plan change #13; likelihood, impact and mitigation columns added per the plan (fixes the K1 and K2 criteria) -->

Severity is the overall grade. Likelihood is how probable the bad outcome is before the mitigation (Low, Medium, High). Impact is how bad it is if it happens (Low: rework; Medium: a stalled repo or lost time; High: lost work, an unreviewed merge or a broken install).

| id | Risk | Severity | Likelihood | Impact | What is unproven | Mitigation | Proving test |
|---|---|---|---|---|---|---|---|
| RK-1 | A `worker-start` worker cannot be bound (marker not seen, `pending/<nonce>` never consumed) | High | Medium | High | No code on master builds a worker prompt with the marker; binding was never observed | `WORKER_BINDING_PROVEN` false refuses workers outside `probe_issues` (K16); stop and escalate on a failed gone-check | S17 binding probe: receipt recorded, `pending/<nonce>` gone within the stated timeout, implementation refused at W before release, `git commit` refused at W and WA |
| RK-2 | INV-025: a bound worker writes a script that pushes a branch, opens a PR, comments or merges; `master` and `integration` are unprotected | High | Medium | High | The guard reads command text only (master `hooks/scripts/launch-level-guard.sh:771-772`); L2 refuses only `main` and `master`; `setsid` escapes job identity; `gh` writes have no L2 | <!-- Source: post-review fix B2 --> A ruleset on `master` and `integration` (OA-5) stops a push to those branches and, if the worker's login cannot bypass it, a merge into them; it does not stop a feature-branch push, a pull request or a comment. With the recommended admin bypass on one shared admin login, a worker's own script can still run `gh pr merge --admin`; only a separate login for agents (OA-6, third option) plus the ruleset makes "a worker cannot merge" true. A person's go per PR is a procedure, not a block; post-merge audit AU1 to AU8 detects after the fact. Every control here narrows | S17: a scripted `git push origin master` on a throwaway repo is refused by GitHub once the ruleset exists; a worker-written script that pushes a feature branch, and one that runs `gh pr merge --admin` on the shared login, are shown NOT stopped, and the record says so |
| RK-3 | `answer-check` cannot tell a person from a script on the shared login | High | Medium | High | Q01 test 1 ("typed by a person in own session") has no mechanical proof | OA-6 names the session kind; go entries carry the head sha and question key; two gate runs | A test shows an answer typed in any other session kind is refused; no test proves identity |
| RK-4 | Planb does not rebase cleanly onto the post-revert master | High | Medium | Medium | Modify/delete conflicts on `issue_pipeline/` never tried | S6 dry run; rebase in a throwaway checkout; do not resume the old ledger | S9 trial rebase, then MC-1 to MC-5 on the result |
| RK-5 | Cron is not in the Coder image; the `Coordinator` worktree is not created | High | Medium | High | Coder issues 515 and 516 open; until 516, planb `dispatch.py` returns `worktree_invalid` for every repo | No stage installs cron before S17 (K13); manual host success does not count | A fresh workspace shows `crontab -l` with the five-field line once, `pgrep -x cron` finds one daemon, and `run-all --dry-run` lists every repo without `worktree_invalid` |
| RK-6 | Revert and PR 686 merged in the wrong order break `superclaude --help` | High | Low | High | Known: 29 test modules fail at collection (D03); guarded only by order and checks | S7 before S11; H0 hold; MC-1 to MC-3 on every later PR touching `issue_watch/` | MC-1, MC-2, MC-3 required on S7 and S11 |
| RK-7 | The claim agent and the standing coordinator live in one `Coordinator` worktree (X-001) | High | High | High | Claim terminal lifetime and a complete agent list are UNVERIFIED | Real rollout off; claims only on a throwaway issue; OA-23 picks the route | S17 X-001 check records all live agent identities and worktree paths before the claim, after the comments, after the result and before coordinator writes |
| RK-8 | Orca transport unknowns: `tui-idle` may not mean idle at the prompt; mailbox from outside a Run (U5) may fail; `orca agent launch` may not carry the ccsession tag (U25), so a lookup misses a session and starts a duplicate | Medium | Medium | Medium | All three are Orca behaviour never observed here | The bounded file pull is the backstop; unreadable process table means unknown and nothing starts | S17 live gate: one mailbox send, an idle and a busy capture, the tag spike, before any typed line |
| RK-9 | A bound worker (WA or F) is blocked by text false positives (a Bash call naming git with commit, merge or push, INV-026) or by a skill that commits on its own | Medium | Medium | Low | `/sc:implement`'s own git use passes; false positives are text matches; not observed bound | WC line 44 has such skills defer staging under `--unattended`; the coordinator stages `.dev/tasks` | S17: a WA worker runs `/sc:implement --unattended` on a throwaway task; the only refusals are the intended commit and push |
| RK-10 | A coordinator weakens its own controls by editing the per-repo config (C-INV-3) | High | Low | High | A hook catches Edit and Write tools, not every shell write | Config folder write guard (S13); fail closed on weakening values at load (in the PR that first reads each key); `coordinator repos` writes only on a recorded go and only in a person-opened session, refusing when run from a worker-bound or coordinator-started session (`refuse(argv)` plus the C-INV-3 hook) <!-- Source: post-review fix N9 --> | `test_config_weakening_refused`; hook test; empty `reviewers`, `merge_safety_files: []`, bad `reach_daily_max` refused |
| RK-11 | A worker shares the `Coordinator` worktree (debate A-002) | Medium | Low | High | Whether `worker-start` always makes its own worktree | `max_in_flight` 1; the per-issue state records the worker worktree path | S17 observation of the worker's resolved worktree path |
| RK-12 | An abandoned wake is never woken again (M2) | Medium | Medium | Medium | pr-a `cycle.py:994` behaviour; the recovery path is new | The poll retargets with a linked new wake id; `status` lists abandoned wakes | `test_abandoned_wake_is_retargeted_with_new_wake_id` (S11) |
| RK-13 | A crash between ack and state loses the issue (M1) | High | Medium | High | Order not enforced in pr-a (`cycle.py:777-810`) | State before ack; poll checks the state revision | MC-6 and `test_wake_ack_m1` (S15a); kill-and-restart at each boundary |
| RK-14 | `orca worktree rm` deletes the branch itself, so cleanup refusals come too late (Q02) | Medium | Medium | Medium | UNVERIFIED Orca behaviour | Refusals run before any removal; any refusal keeps the whole worktree; week one list only | Remove a throwaway worktree with `orca worktree rm` and check whether the branch survives |
| RK-15 | The plan-check copy drifts from `plan_body.py` | Low | Medium | Low | Two copies by design (K8) | One shared case table | `test_plan_check_parity.py` in CI on every change to either file |
| RK-16 | The `Approved` field or the Status allow-list is missing in a Project, so every issue is skipped silently | Low | Medium | Medium | Per-project setup (D02) | `status --json` shows the skip reason per repo; init refuses to enable a repo without the field | Fixture: a project without `Approved` shows the reason in `status --json` |
| RK-17 | An uncertain claim launch is relaunched, giving two claims | High | Low | High | Built safeguards cover today's path; the new outbox path is untested | `pending` never starts from `unknown`; delivery retries never call the launcher | `test_unknown_launch_no_second_claim` (section 8.1) |
| RK-18 | Timer overlap, stale lock or partial store | High | Low | High | Cron timing on the real host | `flock -n`; non-blocking store lock; malformed state blocks | `test_overlapping_poll_one_reservation` (section 8.1) |
| RK-19 | After a rollback the old binary refuses the migrated store and the repo stops (INV-004) | Medium | Medium | Medium | No downgrade path exists today | Backup before migration; downgrade step in every store-changing rollback | MC-11 |
| RK-20 | Under cron's `PATH`, children cannot find `gh` or `orca`; every repo skips and the run still prints "clean" (INV-006, INV-014) | Medium | High | Medium | Runtime under cron never observed | Absolute paths to every child; zero-repos alarm in `status --json` and on the observer | MC-12; S17 cron-PATH run |
| RK-21 | Cap counters diverge or stall: no writer closes the store entry (INV-011); two round writers (INV-012); one corrupt file or one unanswered go stalls the repo (INV-008, INV-023) | Medium | Medium | Medium | Closing writer and expiry not designed in any source | One writer per file (section 4); the poll closes entries from the per-issue phase; "waiting on a person" shown with a reminder (OA-25); `status` names the unreadable file | S15b tests: drain after an orphaned entry; round mismatch refused with a named reason; unreadable file shown with its reason |
| RK-22 | The coordinator's commit goes wrong: pre-commit hooks refuse or rewrite it (INV-019); it sweeps in `.dev/issues/` (INV-020); the worker moved the branch or base (INV-007) | Medium | Medium | Medium | Whether pre-commit is installed in the shared hooks folder is UNVERIFIED | Branch and base check; explicit paths plus `.dev/tasks`; escalate, never `--no-verify` (WC:246) | S14 tests listed under S14; S17 pre-commit observation |
| RK-23 | A coordinator receives text carrying a worker's still-pending marker and binds itself at that pending level (W or F), losing commit, push and Orca verbs (INV-017) | Medium | Low | Medium | Binding lasts until a person deletes the session file (master `hooks/scripts/launch-level-guard.sh:361`) | Ids-only wakes; hand-back and nudge texts never carry a marker | S14 test: a marker-bearing hand-back text is refused before it reaches the coordinator |
| RK-24 | Merge state changes between the two gate runs, or the merge result is uncertain | High | Low | High | Live GitHub timing | Two gate runs; head-pinned argv; reconcile the exact head; no reused go | T13 (S14) |
| RK-25 | Closeout or a `Fixes` line closes an issue whose work is unfinished | Medium | Medium | Medium | `Fixes` closing is GitHub behaviour outside the gate | Close only under the go (K12); keep `left_open`; state the limit | `test_closeout_needs_named_close_go` |
| RK-26 | The report loses sessions when a worktree is missing or Orca is down | Medium | Medium | Medium | Report and sweep maps never compared live | Keep the old map until one live side-by-side run; `read: false` when Orca is down | `test_previous_not_done_carried`; S16 live parity run |
| RK-27 | A blanket `superclaude install --force` removes skills of PRs 632, 650 and 656 (D14 NB-1) | High | Medium | High | Which hosts still carry them | Per-host diff before any install; no blanket install until OA-21 | S8 and S17 per-host diff record |
| RK-28 | All GitHub and Orca reply fixtures are assumed shapes | Medium | High | Medium | No live record exists (`tests/issue_watch/test_github.py:575-583`) | Shadow run records real replies before enabling | S17 24-hour shadow run with captured replies replacing fixtures |
| RK-29 | Instruction-like plan text reaches a prompt, argv or typed line | Medium | Low | High | Untested injection | Plan quoted only inside fenced data; ids-only wakes; pattern-checked argv | Inject an instruction-like plan; assert zero free GitHub text in wake, argv, mailbox and typed line |
| RK-30 | Unsourced numbers are treated as settled (60-minute reviewer hold, 24-hour go expiry, 60-second binding timeout, 3 hand-back rounds) | Low | Medium | Low | No source gives these numbers | Labelled UNVERIFIED; merge automation off until OA-13 is answered; the built 60-minute launched lease is unrelated | Owner values recorded; one measured late-review case |
| RK-31 | Records are lost or duplicated: two homes for human records (INV-002); the staged interim ledger is lost or rides into an unrelated commit (INV-003); records never leave one host (INV-024) | Medium | Medium | Medium | Whether a local-only branch survives worktree cleanup | <!-- Source: post-review fix B5 --> Records, including the imported ledger, live only on the local `coordinators` branch in the `Coordinator` worktree, by local commits, never in a PR to master; the recorder commits the ledger when the owner says (OA-24); pushes of the branch on a go (OA-26) | S13 import check: one copy, a local commit on `coordinators`, nothing in the S13 PR; ledger survives a stash and a worktree removal |
| RK-35 | Planb's `run-all`, once scheduled, generates configs, creates labels on GitHub and switches every new repo on with no per-repo go (K24) <!-- Source: post-review fix B1 --> | High | High | High | Nothing in planb stops `first_run` from rewriting `enabled: true` | `run-all` not scheduled before S17; `auto_enable` false (S9); label creation only after OA-28; the dry run generates nothing (MC-12) | `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing` (S9); MC-12 under cron's environment |
| RK-32 | A saved delivery intent is stranded: replay does not run while prechecks fail or the repo is disabled (INV-027); the attempt counter resets or drains (INV-013); a recomputed state root hides wakes (INV-001) | Medium | Medium | Medium | Replay outside the candidate path is new | Replay despite failing prechecks; stranded-intent alarm; attempt changes only on a real send; `state_dir` read from config | `test_replay_runs_when_prechecks_fail`, `test_attempt_counter_survives_replay`, path-map test (S11, S13) |
| RK-33 | A wake with several items is partly handled and its ack is ambiguous (INV-016) | Medium | Low | Medium | Today's parser defaults missing buckets to empty | Ack names each item; an ack that names no item is invalid; cap 1 keeps one item | `test_ack_naming_no_item_is_invalid` (S11) |
| RK-34 | A restart storm, or a blind process lookup that starts a duplicate coordinator | High | Low | High | Restart method never observed (Coder issue 516 says "restart" with no method) | Restart budget of 3 persisted; unreadable process table means unknown; `coordinator_autostart` false by default | `test_restart_budget_survives_crash`; `test_unreadable_proc_unknown` |

### 8.3 The 27 invariant findings and how this spec handles each

<!-- Source: invariant probe INV-001 to INV-027 (adversarial/invariant-probe.md); status column is the probe's; handling column points to where this spec carries the condition -->

The probe found 27 assumptions: 7 already addressed, 20 not addressed (1 HIGH, 15 MEDIUM, 4 LOW). Because the debate had no third round, every unaddressed finding is carried as a binding condition. "Probe status" is the probe's verdict on the variants, not on this spec.

| id | The assumption it tested, in short | Severity | Probe status | How this spec handles it |
|---|---|---|---|---|
| INV-001 | Cron and an interactive coordinator resolve the same state root | MEDIUM | UNADDRESSED | Every consumer reads `state_dir` from the per-repo config (K5; section 2.5; S13 path-map test; RK-32) |
| INV-002 | Human records have one home | MEDIUM | UNADDRESSED | Records, including the imported ledger, live only on the local `coordinators` branch, by local commits, never in a PR to master (K5, K21; S13; RK-31) |
| INV-003 | The interim ledger is durable | MEDIUM | UNADDRESSED | The recorder commits it when the owner says (K21; OA-24; RK-31) |
| INV-004 | A rollback is safe after the store migrated | MEDIUM | UNADDRESSED | Backup and downgrade step; MC-11 (K4; section 2.5; RK-19) |
| INV-005 | A consumed go is never restored; an uncertain merge is reconciled | LOW | ADDRESSED | Kept (K5; section 2.2) |
| INV-006 | Cron runs the poll with working tools | MEDIUM | UNADDRESSED | Absolute `gh` and `orca` paths to every child; MC-12 (K4; S9; RK-20) |
| INV-007 | A bound worker (WA or F) leaves the branch as the coordinator expects | LOW | UNADDRESSED | Branch and base check before the commit (K2; S14; RK-22) |
| INV-008 | An unreadable per-issue file counts as in flight, and someone learns why | LOW | UNADDRESSED | `status` names the file and reason (K9; S12; RK-21) |
| INV-009 | An `unknown` launch counts toward the cap; only `reset N` clears it | LOW | ADDRESSED | Kept (section 2.1) |
| INV-010 | When the owner never answers, nothing proceeds | LOW | ADDRESSED | Kept (section 7: silence is not a yes) |
| INV-011 | One in-flight count with a named closing writer | MEDIUM | UNADDRESSED | One writer per file; the poll closes the store entry from the per-issue phase (K9; section 4; RK-21) |
| INV-012 | The hand-back round has one writer | MEDIUM | UNADDRESSED | The poll owns the round; mismatch refused with a named reason (K9; section 2.5; RK-21) |
| INV-013 | Wake attempts bound delivery across replays | LOW | UNADDRESSED | Attempt keeps its value; increments only on a real send (section 2.5; S11; RK-32) |
| INV-014 | An empty repo list is visible | MEDIUM | UNADDRESSED | Zero-repos alarm in `status --json` and on the observer (K4, K10; MC-12; RK-20) |
| INV-015 | Repos are keyed uniquely | LOW | ADDRESSED | `name_collision` skip until the rekey; `coordinator_session` key (K22; S12) |
| INV-016 | A wake holds exactly one item | MEDIUM | UNADDRESSED | Ack names each item; an empty ack is invalid (section 2.5; S11; RK-33) |
| INV-017 | The coordinator never receives a worker's launch marker | MEDIUM | UNADDRESSED | Ids-only wakes; marker-bearing text refused before the coordinator (K2; S14; RK-23) |
| INV-018 | A separate claim worktree keeps the file handoff working | MEDIUM | UNADDRESSED | `launch_cwd` saved in the store and read through `state` (K1; X-001; section 4 row 15) |
| INV-019 | The coordinator's commit succeeds as is | MEDIUM | UNADDRESSED | A refused or rewritten commit is escalated, never `--no-verify` (K2; S14; S17; RK-22) |
| INV-020 | What the coordinator commits is defined | MEDIUM | UNADDRESSED | Explicit paths plus `.dev/tasks`; never `-A`; never `.dev/issues/` (K2; S14; RK-22) |
| INV-021 | The guard does not block the coordinator's own commit or push | LOW | ADDRESSED | Kept; the coordinator is unbound (section 2.2) |
| INV-022 | Watcher and coordinator locks never deadlock | LOW | ADDRESSED | Kept; the coordinator never takes the store lock (section 4 "who writes what") |
| INV-023 | Cap 1 and owner silence work together | MEDIUM | UNADDRESSED | A waiting go counts and is shown, with a reminder; no expiry drops committed work (K9; OA-25; RK-21) |
| INV-024 | Records on the `coordinators` branch reach other readers | LOW | UNADDRESSED | Pushing the records branch is an outward action needing a go (K5; OA-26; RK-31) |
| INV-025 | Binding a worker (F in the probe's wording; WA behaves the same) alone makes D06's "a worker cannot push or merge" true | HIGH | UNADDRESSED | **Carried, not solved.** <!-- Source: post-review fix B2 --> The guard narrows honest drift. A ruleset on `master` and `integration` stops a push to those branches and, if the worker's login cannot bypass it, a merge into them. It does not stop a feature-branch push, a pull request or a comment. With the recommended admin bypass on one shared admin login, a worker's own script can still run `gh pr merge --admin`; only a separate login for agents (OA-6, third option) plus the ruleset makes "a worker cannot merge" true. A person's go is a procedure, not a block. Every control here narrows (sections 0 and 1; K2; OA-5; OA-20; RK-2; S17 records it) |
| INV-026 | `/sc:implement` completes at F | LOW | ADDRESSED | Kept; S17 live probe (RK-9) |
| INV-027 | The outbox alone makes a crash between claim and wake safe | MEDIUM | UNADDRESSED | Replay despite failing prechecks; stranded-intent alarm (K1; section 2.5; S11; RK-32) |

### 8.4 Not shown by any source and so UNVERIFIED in this spec

<!-- Source: V1 section 8 closing list, V2 section 8 closing list, D16 "Unverified" -->

- Which restored `issue_pipeline` verb exposes `brief.build` (checked in S6).
- The path and shape of PR 693's launch result file.
- Whether a coordinator session can run the claim skill in its own session (needed only for `claim_by: coordinator`).
- The claim terminal lifetime after a level-none claim and a complete source of live agent identities (X-001).
- U28 model picker id, U30 effort levels, U8 info-stream replies, U3 depth-0 script start, U54.
- The 60-minute reviewer hold, a go expiry, the 60-second binding timeout and `HANDBACK_MAX = 3`.
- How the coordinator learns a worker's session id for route A (G2 design section 4; FU-1 precondition f); without it the worker is bound at F.
- The exact store backup file name, the interim ledger file name, the exact per-repo state subfolder naming in planb, and the spelling of the `superclaude coordinator` verbs.
- Whether pre-commit is installed in the shared hooks folder (INV-019).
- Whether "require review from code owners" at 0 required approvals blocks a non-owner author on this repository (D16 "Unverified"), and organisation-level rulesets.
- What `orca worktree rm` does to the local branch (Q02).
- The meaning of "simple feature" in claim rule C1 (D12 gives no measurable test).
- Whether per-repo subprocess calls are light enough for the observer's 15-second refresh (K10).

## 9. Appendix: provenance

<!-- Source: refactor plan "Planned Changes" table and "Changes NOT Being Made"; merged per plan change #14 -->

**Citation roots.** The short citation prefixes used above resolve to these folders (evidence only; nothing here is a contract path):

| Prefix | Folder |
|---|---|
| master | `/home/coder/.cache/ic-snap-20261120/master/` (snapshot of `origin/master` 61ac2c2e6) |
| pr-a | `/home/coder/.cache/ic-snap-20261120/pr-a/` (PR 686 head `8e5ae29ad`) |
| pr-p | `/home/coder/.cache/ic-snap-20261120/pr-p/` (PR 690) |
| planb | `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/` (branch `ironbelly/issue-watcher-zero-setup-plan`, working tree) |
| Dnn, Qnn | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/<id>/VERDICT.md` |
| invariant probe, debate rounds | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/brainstorm/run/nested/adversarial-1/adversarial/` (`invariant-probe.md`, `debate-transcript.md`, `rounds/`) |
| technical references | `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/` |

**Which part came from where.**

| Part of this document | Main source | Also from | Plan change |
|---|---|---|---|
| 0 Status and glossary | V3 header and closing paragraph | V1 status line, V2 reading guide | #1 |
| 1 Summary | V3 section 1, rewritten as sentences | V1 five decisions, V2 "what cannot be proven" | #1 |
| 2 Diagram | V1 section 2 | V2 status tags, V3 flow and at-least-once paragraph | #2 |
| 2.1 Issue watcher | V3 | V1 symbol names and STAYS list, V2 section 2.1, debate round 2 store evidence (V3 advocate section 3b) | #3 |
| 2.2 Coordinator | V3 | V1 verbs and flags, V2 section 2.2, INV-007, INV-017, INV-018, INV-019, INV-020 | #4 |
| 2.3 Observability | V3 | V1 and V2 section 2.3; debate C-005, C-006, X-006 | #5 |
| 2.4 Claim pipeline | V3 | V2 and V1 section 2.4; D16 section F | #6 |
| 2.5 Integrity rules | V3 section 4 integrity rules (kept whole) | INV-001, INV-004, INV-006, INV-011, INV-012, INV-013, INV-016, INV-027 | #7 |
| 3 Contradictions K1 to K24, X-001 | Plan "Final decisions" | V1, V2 and V3 section 3 reasons and reversals; debate C-001, C-002, C-003, X-001 to X-005; K24 and the K2 rewrite from the post-review fixes | #8 |
| 4 Interface table and single-writer table | V1 and V2 section 4 rows | V3 validation and built columns; INV-011, INV-012 | #9 |
| 5 Stages S0 to S17, MC-1 to MC-12 | V2 section 5 structure, plan stage list | V1 section 5 tests, V3 section 5 evidence and exclusions; INV-004, INV-006 | #10 |
| 6 Ledger | V2 section 6 evidence | V1 rows (defaults file, R33, design package), V3 consequences | #11 |
| 7 Owner actions OA-1 to OA-34 | V1 section 7 | V2 and V3 section 7 answers, D16 ranks, INV-003, INV-023, INV-024, X-001, D15 OD list (OA-29 to OA-34) | #12 |
| 8 Risks, RK-1 to RK-35, INV table | V3 section 8 failure table | V1 RK rows, V2 R rows, invariant probe | #13 |
| 9 Appendix | Plan | none | #14 |
| Post-review fixes B1 to B6, N1 to N14 | Independent reviewer, decisions from the orchestrating session (planb `dispatch.py`, `first_run.py`, `repo_init.py`; master guard `:265-272, 785-790`; G2 design route A) | Tagged `<!-- Source: post-review fix ... -->` in place | after #14 |

**Considered and not used (from the plan).** V1's `start_mode` second claim path in the first build (only the key `claim_by` is reserved); V1's `watcher` block inside the sweep JSON (X-006); V1's `schema_version` 2 (the loaders reject unknown keys at any version); V1's "unbound and flagged" rule for real issues (breaks the owner's G2 sentence); V2's three separate watcher PRs on Clay's PR (D15:219 "not split") and its skill-before-merge bridge (D15 O4, O5, O6 order wins); V2's tracked go entries and V2 and V3's in-worktree runtime state; V3's package-canonical plan check, telegraphic owner list and host-specific paths in contract tables; any wording that a control fully removes a risk (D06 item 10); any statement that binding alone, or a ruleset with the shared-login admin bypass, makes workers unable to push or merge (INV-025); building anything: this document is a recommendation only.
