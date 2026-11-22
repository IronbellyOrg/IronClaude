# Unification spec: issue watcher, coordinator, dashboard and issue-claim-to-work pipeline

| Field | Value |
|---|---|
| Status | DRAFT for spec-panel review. A recommendation. Nothing in it has been executed, pushed, merged, reverted, commented on or approved. |
| Date | 2026-11-20 |
| Owner | `ironbelly` (the repository admin and the only person who gives rulings). Every verdict here is a recommendation until the owner says so in chat. |
| Precedence rule | The owner's line of work ("OURS") takes precedence. Clay's (login `clayphi`, they/them, "CLAY") clearly better, separable elements are folded in. A verdict is binding unless two verdicts contradict (section 11). |
| Sources | Work folder `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/` (called `<W>` below): verdicts `<W>/debates/<ID>/VERDICT.md` (D01-D16, Q01-Q03, QG1-QG4); `<W>/DECISIONS.md`; `<W>/STATE.md`; merged brainstorm design `<W>/brainstorm/run/nested/adversarial-1/merged-output.md` (called "the merged design", cited by section id, for example "merged 3 K2"); `<W>/inventory/clay-prs.md`; `<W>/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md` and `<W>/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md`; `/home/coder/workspaces/IronClaude/.dev/analyze/pr686-20261120/FULL-REPORT.md`. Code (read-only): snapshots `/home/coder/.cache/ic-snap-20261120/{master,pr-a,pr-p}` and the owner's unpushed worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`. |
| Code baseline | "master" = snapshot of `origin/master` 61ac2c2e6; "pr-a" = PR 686 head `8e5ae29ad`; "pr-p" = PR 690 head `f3bc77981`; "planb" = branch `ironbelly/issue-watcher-zero-setup-plan`, HEAD `d0a0a433b`, uncommitted tree. A citation such as "master cycle.py:228" means `src/superclaude/cli/issue_watch/cycle.py` line 228 of that snapshot; other prefixes are written in full. |

**Terms, each defined once.**

| Term | Meaning |
|---|---|
| Poll | One run of the issue watcher for one repository (`superclaude issue-watch once`). Read-only on GitHub. |
| Dispatcher | `issue-watch run-all`: one cron-started loop that runs one poll per project listed by `orca repo list`. Exists only in planb. |
| Coordinator | The long-running Claude session of one project, named `COORD-<RepoName>`, command `/sc:coordinator`. Clay's design calls it "orchestrator". `Coordinator` (capital C) is its working branch and worktree; `coordinators` is a separate records branch. |
| Worker | A supervised Claude session the coordinator starts with Orca `worker-start` to implement one issue. |
| Wake, ack | A wake is a small file the poll writes to tell the coordinator about a claimed issue (ids only). An ack is the coordinator's reply file. |
| Go | A person's typed answer in live chat that permits one named outward action (one push, one merge, one cleanup apply). An agent records it; the owner never writes a file. |
| Grant | A standing permission for a small class of GitHub writes. Default none. |
| Guard, L1, L2 | The launch-level guard: L1 is `launch-level-guard.sh` (reads each command in a bound session); L2 is the git pre-push hook (refuses pushes to `main` and `master` only). Levels: W (planning only), WA (W plus a `sessions/<id>.ok` file: implement allowed; commit, push and PR refused), F (implement allowed; commit, push and PR refused; `.ok` not read), FS (full submit: commit, push a feature branch and open a PR allowed; never merge). Source: master `hooks/scripts/launch-level-guard.sh:265-272, 785-790`. |
| Route A | The owner's G2 design: after a recorded plan approval the coordinator writes the worker's `.ok` file (verb `release-worker`), turning W into WA. Needs the restored `issue_pipeline` package. |
| MC-n | Mechanical merge check n (defined once in section 8). |
| FR, NFR, SEC | Functional, non-functional and safety requirements (section 4). |
| BS | Requirement or statement whose only source is the merged brainstorm design, not a verdict. Listed in section 12. |
| NEW (author) | Requirement with no verdict, brainstorm or code source. Listed in section 12. |
| OA-n | Owner action n of the merged design (section 10 cross-references it). |
| K-n, S-n, INV-n | K-n: picks of the merged design resolving verdict conflicts; S-n: its stages (here section 8); INV-n: findings of its invariant probe. |
| UNVERIFIED | No source read by the author proves it. Each use names the check that would settle it (section 12). |

## 1. Purpose, scope and non-goals

### 1.1 Purpose

Two lines of work grew in the same files. The owner's line built the issue watcher (PRs 447 and 448, the merged poller), the claim pipeline (`/sc:issue --claim`), the launch guard, the sweep (PR 539, read-only report of Orca sessions), the observer and a plan-approval package (PRs 584 and 591, Plan A and Plan B). Clay's line produced a design (PR 681, merged `docs/designs/orchestrator.md`), a deletion of the owner's plan-approval package (PR 682, merged about 66 minutes after it opened with only a bot review), a watcher rewrite (PR 686, open, 59 files), `/sc:issue --plan` (PR 690, open), `/sc:closeout` (PR 683, merged) and a work-report skill (PR 684, merged). No `ironbelly` review exists on PRs 681 to 684, 686 or 690 (FULL-REPORT sections 1 and 3).

This spec states in one place the local changes, the pull request dispositions (including one revert), the staged migration and the process corrections that remove those conflicts and unify the effort under the owner's rules, with Clay's separable strengths folded in. It is a spec, not an action list: its author executes nothing.

### 1.2 Scope and non-goals

In scope: the issue watcher (poll, dispatcher, wake transport), the project coordinator (command, verbs, authority), the observability stack (sweep, observer, work report), the claim-to-work pipeline (`/sc:issue --claim`, `--plan`, guard, closeout, cleanup) and the process package that prevents a repeat. Not in scope:

- Executing anything: no git write, no GitHub or Orca write, no install. Every PR disposition needs the owner's go in chat (section 6). The watcher is not switched on before S17.
- Reserved or rejected designs: a listener process (Coder issue 477, listener in every workspace), the registry repository, a label write by the poll, the lease comment, interrupting a worker, standing `pr.merge` or `issue.close`, org-wide search, extra info streams, moving brainstorm and design into create (issue 689, Clay's request), the sub-coordinator (issue 444) and the knowledge layer (issue 423).
- Anything touching `SuperClaude-Org/SuperClaude_Framework` (upstream): never.
- Claiming any control closes a risk. Every control "narrows" it (D06 item 10). `master` is unprotected today (`protected: false`, no ruleset, no CODEOWNERS; D16 section E): a person's go is a procedure, not a block, until an admin sets a ruleset.

### 1.3 Built today versus not built

Baseline is the master snapshot. RUNS: code exists, is wired into a normal install and has no switch keeping it off (not proof any machine ran it). STUBBED: code exists but a switch, skipped test or constant keeps it off or unproven. NOT BUILT: no code on master (a branch or open PR may hold a version). REMOVED: deleted by PR 682. Sources: both technical references and merged design section 6; lines re-read by the author.

| State | Piece | Evidence |
|---|---|---|
| RUNS | `/sc:issue --claim` (waves 0-8, levels none, worktree, full, full submit) when a person types it; claim marker `<!-- sc:issue:claim -->` | master `cli/issue_watch/predicates.py:14`; `commands/issue.md` |
| RUNS | Guard L1 and L2, job identity, G2 rule 2, the `pending` verb. Governs only sessions a claim launch bound; no `worker-start` worker has ever been bound | master `hooks/scripts/launch-level-guard.sh:265-272, 785-790`; `skills/sc-issue-protocol/scripts/orca_worktree.py:1515` |
| RUNS | `/sc:sweep` (JSON v1 on stdout plus Markdown report), `superclaude observe`, the report skill's reader side (PR 684), `/sc:closeout` (PR 683), plan sections in the issue templates (PR 661) | master `cli/sweep/commands.py:277-278`; observer reference 2.5 |
| STUBBED | Single-repo poll `issue-watch once`: complete code, `enabled` defaults to false, never ran live, reply fixtures are assumed shapes | master `cycle.py:228`, `launch.py:33`, `record.py:34-35`, `tests/issue_watch/test_github.py:575-583` |
| STUBBED | Missing-L2 refusal off (`IR7_REFUSE = False`); the twelve live guard observations are skipped (issue 442, open); `GOVERNED_LEVELS_ALLOWED = False` exists only in planb | master `orca_worktree.py:822`, `tests/hooks/test_launch_level_observations.py:79-84`; planb `launch.py:48` |
| NOT BUILT on master | Dispatcher `run-all`, per-repo configs, `first_run`, stage-aware `brief.py`, `complete.py` (planb only, 225 uncommitted entries); wake files, ack, `max_in_flight`, plan-check skip, label writer (pr-a only; `wake.py:46-47` still says `orchestrator-wake/1`); `/sc:issue --plan` (pr-p `skills/sc-issue-protocol/scripts/plan_body.py:138`) | planb, pr-a and pr-p reads |
| NOT BUILT anywhere | Coordinator command and skill, `superclaude coordinator` verbs, `merge-gate`, `answer-check`, `E-NO-GRANT`, `refuse(argv)`, AU1-AU8, hand-back, `escalate`, `report-entry` writer, go entries; cleanup script (issue 687, Clay's request); cron in the Coder image (Coder 515); the `Coordinator` worktree (Coder 516); `observe-sweep-contract.md`; sweep `session_id`; ruleset, CODEOWNERS, `docs/decisions.md`; any caller binding a `worker-start` worker to the guard | no coordinator or orchestrator command or skill under master `src/superclaude/{commands,skills}` |
| REMOVED | `src/superclaude/cli/issue_pipeline/`, WC-17 "Issue pipeline duties", guard G2 rule 1, `release-worker` | PR 682, commit `01e7a9e23`; present at `01e7a9e23^` and in planb |

In one line: nothing of the unified flow has run live. The watcher is complete but off; the coordinator is design text; the guard has never bound a coordinator-started worker.

### 1.4 Corrections to the question's wording

Issues 687 and 689 are issues, not PRs; nothing is built for either. Issue 651 (Clay's request for plan sections) is closed by PR 661. PR 693 (owner's PR saving the claim launch result file; issue 691) appeared after the inventory and edits four of PR 690's files. The branches `clayphi/issue-655-pr-p`, `-pr-c`, `-pr-d` and `-spec-pr` have PRs (690, 684, 682, 681); only `clayphi/v61-part-b-map` has none. PR B (the unbuilt coordinator skill) and PR E (the unbuilt runbook rewrite) have no PR or branch.

## 2. Binding decisions

One row per entry of `<W>/DECISIONS.md` (42 entries: D01-D16, Q01-Q03, OD-1 to OD-13 and the ten sub-answers OA-13a to OA-28b of the later debates OAG1 to OAG3). `debates/OA-TRIAGE.md` classed 20 of the 34 owner actions as settled by verdicts, 9 as owner-only (section 10.6) and 5 as debated. Source verdict files are `<W>/debates/<ID>/VERDICT.md`. Winner: OURS (owner's line), CLAY or HYBRID. Confidence is the verdict's own; (p) = partial, with open HIGH findings kept as conditions (section 12). OD answers come from QG1 (OD-1, 2, 13), QG2 (3-5), QG3 (6, 10-12), QG4 (7-9). All are recommendations until the owner rules in chat. Numbers: PR 682 (Clay's merged deletion of the owner's plan-approval package); PR 686 (Clay's open watcher rewrite); PR 690 (Clay's open `/sc:issue --plan` PR); PR 661 (merged plan sections in templates); PR 670 (merged daily PR log); issues 687 (Clay's cleanup request), 689 (Clay's create-time design request).

| ID | Decision (condensed) | Winner | Source verdict | Conf. |
|---|---|---|---|---|
| D01 | Approval, not assignment, starts work; plan check and `hold:backlog` added as read-only skips; start-time re-check repeats every gate (MR-1); claim-marker guard stays (MR-2). | HYBRID | D01 | 78% (p) |
| D02 | Cron stays the scheduler; fix the owner's false reason about automations; Clay's precheck automation is a tested-first fallback. | HYBRID | D02 | 62% (p) |
| D03 | Revert PR 682 as one new PR, re-apply the "no `--to`" bullet; PR 686 never merges ahead of it. | HYBRID | D03 | 78% (p) |
| D04 | Every claim passes `--pipeline none`, one supervised worker follows; Pipeline field unread; low-stakes grants only; merge and close per-PR goes. | HYBRID | D04 | 75% (p) |
| D05 | Guard required for every coordinator-started worker, staged behind a live probe; it never "closes" the unprotected-`master` risk; adopt `refuse(argv)`, head-pinned merge, AU1-AU8. | HYBRID | D05 | 78% (p) |
| D06 | No merge without a person's typed go (head sha pinned); read-only `merge-gate` twice; `/sc:pr-submit` never a worker; every gate "narrows". | HYBRID | D06 | 85% (p) |
| D07 | Project-local coordinators, one dispatcher, per-repo config, no registry repository; adopt cap, guarded restart, `merge` block, `owner/name` keys. | HYBRID | D07 | 80% (p) |
| D08 | Role "coordinator", `/sc:coordinator`, `COORD-<RepoName>`; flags `--wake --hourly --resume --take --sub`; rename persisted names before PR 686 merges. | HYBRID | D08 | 85% |
| D09 | The poll writes nothing to GitHub (NG-2); adopt read-only plan check and person-set `hold:backlog`; label write deferred. | HYBRID | D09 | 78% (p) |
| D10 | Wake file plus ack; mailbox and typed line are id-only nudges; coordinator also pulls; no listener; M1 and M2 mandatory. | HYBRID | D10 | 75% |
| D11 | Sweep JSON is the one session source (adds `session_id`, `worktree_path`); work report is the one report; observer is the one screen; 5-a-day cap only a proposal. | HYBRID | D11 | 72% |
| D12 | Keep PR 661; adapt and merge PR 690; claim keeps its chain plus rule C1; reject moving brainstorm and design into create (issue 689). | HYBRID | D12 | 72% (p) |
| D13 | Closeout, cleanup script (issue 687) and PR 670 complementary; coordinator runs sweep, closeout, cleanup `list` each cycle; `--apply` only on a recorded go. | HYBRID | D13 | 80% |
| D14 | PR 686 adapted in place as one draft; PR 690 adapted then merged; PR 682 reverted only if both gates stay; PR 681 kept with banner; hold step H0 first. | HYBRID | D14 | 80% (p) |
| D15 | 71 Clay elements decided one by one (section 7); four new HIGH conditions C-INV-1 to C-INV-4. | HYBRID | D15 | 72% (p) |
| D16 | Lightest process package: chat decisions, hold, rule text, CODEOWNERS, admin ruleset, throwaway test, `docs/decisions.md`, 14-day review. | HYBRID | D16 | 75% (p) |
| Q01 | Grant rows, `--apply` goes, cleanup-design approval are the owner's chat consent, recorded by an agent; fix `WORKER-CONTRACT.md:57`; adopt `answer-check` checks. | HYBRID | Q01 | 75% (p) |
| Q02 | Cleanup may run local `git branch -d` only, as a backstop, with refusals that keep the whole worktree. | HYBRID | Q02 | 85% |
| Q03 | Replace PR 686's label-writing code with a read-only variant now; `issue.hold` grant removed. | HYBRID | Q03 | 70% (p) |
| OD-1 | `plan_depth` key, default `quick`; no `plan_tier`. | OURS | QG1 | 66% |
| OD-2 | Hand-back round 2: re-plan, person re-approves, whole start gate repeats. | OURS | QG1 | 78% |
| OD-3 | Naming rule scope B: scan only `report-entry` and `escalate`; measure U54 first. | OURS | QG2 | 75% (p) |
| OD-4 | A refused mandatory escalation fails open: written, span masked visibly, original logged. | OURS | QG2 | 75% (p) |
| OD-5 | Audit escalations are entry lines only first; push notice reserved for AU4a, AU4c, AU5. | OURS | QG2 | 60% (p) |
| OD-6 | The coordinator never tags or publishes; N6 unconditional. | OURS | QG3 | 89% |
| OD-7 | No interrupt of a running worker. | OURS | QG4 | 85% |
| OD-8 | No lease comment now; reserved with a trigger. | OURS | QG4 | 75% |
| OD-9 | No list of newly assignable issues; info streams off with a switch. | OURS | QG4 | 85% |
| OD-10 | One per-PR go bound to the head sha covers merge and close; no standing `issue.close`. | OURS | QG3 | 77% |
| OD-11 | Empty `grants` on a fresh install; the owner grants three standing entries once in chat. | OURS | QG3 | 71% |
| OD-12 | Protect per-repo config by verb refusal plus hook, and fail closed on weakening values. | HYBRID | QG3 | 69% |
| OD-13 | A hand-back waiting for re-approval does not count toward `max_in_flight`. | OURS | QG1 | 70% |
| OA-13a | A merge go has no clock expiry in the first build: it ends on the action, a head move or a revoke; merge automation needs an owner-recorded age or "none". | OURS | OAG1 | 80% |
| OA-13b | Merge-time reviewer hold: owner-set `reviewers`, 60 minutes from the final head's checks (UNVERIFIED, owner-settable), then escalate. | OURS | OAG1 | 70% |
| OA-13c | `changes_requested` stays a hard refusal. | OURS | OAG1 | 95% |
| OA-25a | No push notice in the first build; a waiting PR is shown with the age of the wait. | OURS | OAG1 | 75% |
| OA-25b | Silence is never a yes; a waiting merge go counts toward the cap and never expires; only a waiting hand-back may expire, on an owner-set limit. | OURS | OAG1 | 85% |
| OA-9 | The sweep JSON is saved as `<UTC>-sweep.json` beside the Markdown report; readers follow a root, window and age selection rule; WC-16 unchanged. | OURS | OAG2 | 85% |
| OA-17a | The observer shows entry fields from a named allowlist with a length cap; titles and links only while `report-entry` is absent. | HYBRID | OAG2 | 72% |
| OA-17b | The questions panel stays, labelled that a handled question can appear open; "one source for session facts". | OURS | OAG2 | 75% |
| OA-28a | `auto_enable` ships false until the S17 throwaway run, then the owner turns it on once in chat. | HYBRID | OAG3 | 70% (p) |
| OA-28b | NG-2 covers only the poll cycle; init may create the trigger label once, on the owner's chat OK. | OURS | OAG3 | 88% (p) |

## 3. Target architecture

### 3.1 In plain English

One flow runs per project. A cron entry (installed by the Coder image, Coder issue 515: the owner's issue for cron at boot) starts one dispatcher every five minutes, which runs one read-only poll per project. When an issue is open, assigned only to the watcher login, approved by a person (field `Approved`, unedited since), in an allowed Project Status, with its plan sections filled and no `hold:backlog`, the poll starts a claim session as master already does: `/sc:issue --claim <N> --pipeline none` (master `cli/issue_watch/launch.py:33`). When the claim marker appears, the poll saves claim evidence and a delivery intent in one store save and writes an ids-only wake file. The project's coordinator (`COORD-<RepoName>` in the `Coordinator` worktree, Coder issue 516: the owner's issue for that worktree and session) pulls the wake, saves its own record, then acknowledges. It starts one supervised worker bound to guard level W, releases it to WA after the person's recorded plan approval (route A), and commits the work itself. A person's typed go precedes every push and merge. Then closeout and a dry-run cleanup list run. The sweep stays the one source of session facts, the observer shows it, the work report gives plain-English progress. The system is local and at-least-once: a wake may arrive twice, and handling one round twice must have no second effect.

### 3.2 Diagram

Tags: [B] built on master, [P] planb only, [C] open Clay PR, [N] not built, [R] removed by PR 682 (Clay's merged deletion of the plan-approval package), restored by the revert.

```text
 OWNER'S CHAT: approvals, goes, grants, rulings (an agent records each) -----------+
 GITHUB (poll only reads; seven read-only gh calls)                         [B]    |
   assigned only to watcher, Approved, Status ok, plan passes, no hold:backlog  [B][C]
        v                                                                          |
 cron */5 * * * *  flock -n  absolute paths  log                            [N]    |
 issue-watch run-all (ONE dispatcher; orca repo list; zero repos = alarm)   [P]    |
 issue-watch once --config <config_dir>/<repo>.json  start rule, plan, cap [B][C]  |
        v                                                                          |
 CLAIM SESSION  /sc:issue --claim <N> --pipeline none                       [B]    |
        v  marker seen next poll: claimed + delivery intent in ONE save            |
 <state_dir>/wakes/<id>.json  ids only; optional mailbox/typed-line nudge  [C][N]  |
        v                                                                          |
 COORD-<Repo> in <worktrees>/<repo>/Coordinator                            [N] <---+
  1 pull wakes at each check --wait return; save issues/<repo-key>__<N>.json
  2 write <id>.ack.json only after step 1 (M1)
  3 adopt claim files (launch_cwd read through the `state` verb)
  4 pending --level worktree; worker-start with [sc-launch:v1:<nonce>];
    check pending/<nonce> is gone, else stop and escalate               [B][N][R]
  5 W worker plans; person approves; coordinator records, writes .ok -> WA   [R]
  6 WA worker edits and tests, worker_done (no commit, push or PR command)
  7 coordinator commits explicit paths + .dev/tasks (branch and base checked)
  8 person's typed go -> push and /sc:pr-submit --monitor 3 in a person-opened
    top-level session, never a worker                                        [B]
  9 merge-gate -> typed go -> merge-gate -> gh pr merge --match-head-commit  [N]
 10 closeout (close only if the go names it); cleanup list; audit AU1-AU8    [N]
 sweep (read-only) JSON v1 + session_id, worktree_path, saved file       [B][N]
 issue-watch status --json -> observer ; report-entry files -> work report [B][N]
```

If the owner says only the start gate stays (OA-1), PR 682 stands, steps 4-5 change (bind at F, no `.ok` release) and the plan-approval package is not restored (section 8.3).

### 3.3 Interface table

Fuller 41-row version: merged design section 4. Numbers: PR 690 (Clay's open `/sc:issue --plan` PR), PR 683 (merged `/sc:closeout`), issue 687 (Clay's cleanup request). `<config_dir>` = `~/.config/superclaude/issue-watch.d`; `<state_dir>` = per-repo state root named in each config. One writer per file (NFR-02).

| # | Name | Format, path, verbs | Writer | Reader | Built today |
|---|---|---|---|---|---|
| 1 | Cron, dispatcher | `*/5 * * * *` under `flock -n`; `issue-watch run-all [--dry-run]`; child `once --config <config_dir>/<repo>.json`; 270 s cap | Coder template (515); cron | none | cron NOT BUILT in image; `run-all` planb only (`cli.py:432`) |
| 2 | Per-repo config | `<config_dir>/<repo-key>.json`, `schema_version` 1; planb keys plus the keys of FR-12, FR-30, FR-33, FR-34, FR-59 and the `merge` block | generator; later `coordinator repos` on a recorded go | poll, dispatcher, coordinator | shape in planb; added keys NOT BUILT |
| 3 | Store, audit | `<state_dir>/dispatch.json` (pending, launched, claimed, woken, acked, unknown, failed, abandoned, waiting_reapproval; backup `.v<old>.bak`), `audit.jsonl` | poll only | poll, `status` | six states BUILT (master `record.py:34-35`) |
| 4 | Claim prompt, marker | `/sc:issue --claim <N> --pipeline none`; `<!-- sc:issue:claim -->` | poll via `orca agent launch`; claim session | poll `marker_in_window` | BUILT (master `launch.py:33`, `predicates.py:14`) |
| 5 | Wake, ack | `<state_dir>/wakes/<id>.json` (`coordinator-wake/1`; `repo`, `number`, `url`; 0600; at most 64 KiB) and `<id>.ack.json` (`coordinator-wake-ack/1`; accepted, skipped, rejected) | poll; coordinator after its state file | each other | pr-a only, as `orchestrator-wake/1` (pr-a `wake.py:46-47`) |
| 6 | Per-issue state, go, grants | `<state_dir>/issues/<repo-key>__<N>.json`; `goes/<PR>-<sha12>.json`; `grants`, `grants-use.jsonl` | coordinator; recording agent | poll (phase), merge verb | DESIGN ONLY |
| 7 | Launch marker | `[sc-launch:v1:<32 hex nonce>]` in the worker's first prompt; `pending/<nonce>`; `sessions/<sid>.ok` | coordinator (`pending`, `release-worker`) | guard L1 | `pending`, guard BUILT; caller NOT BUILT; `release-worker` REMOVED |
| 8 | Verbs, command | verbs of FR-26; `/sc:coordinator [--wake <id>] [--hourly] [--resume] [--take <owner/repo#N>] [--sub]`; skill `sc-coordinator-protocol` | runner; person | skill, tests | NOT BUILT |
| 9 | Plan check | reference `plan_body.py check`; package copy `issue_watch/plan_check.py`; shared case table | skill; watcher | claim C1, `--plan`, poll, `plan-check` | PR 690 OPEN (pr-p `plan_body.py:138`); copy NOT BUILT |
| 10 | Status, sweep JSON, report entries | `issue-watch status --json` (plus `last_sweep_at`, `recent_skips[]`, stranded deliveries, served-repo count); sweep v1 plus `session_id`, `worktree_path`, saved `<UTC>-sweep.json`; `<report_state_dir>/<repo-key>__<N>.json` | poll (no `gh`); `/sc:sweep`; `report-entry` only | observer, report, coordinator | verb BUILT (master `cli.py:165`); sweep stdout only (master `cli/sweep/commands.py:277-278`); rest NOT BUILT |

## 4. Requirements

Row form: ID, the "shall" sentence, acceptance check (a command, test or observable; NEW = to be written; a path = exists in the snapshot named, under `tests/`), source (verdict id; `BS` = merged brainstorm design only, see 12.4). Long enumerations stay in the verdict item cited. The component is named under each subsection heading. Numbers: PR 686 (Clay's open watcher rewrite, pr-a); PR 682 (Clay's merged plan-approval deletion); PR 690 (Clay's `/sc:issue --plan` PR); PR 661 (merged plan sections in templates); PR 693 (owner's claim-launch-result PR); issue 442 (live guard observations); issues 687, 689 (Clay's cleanup and create-time design requests); Coder issues 515, 516 (cron at boot; `Coordinator` worktree and session); R18, R33 (owner's zero-setup rows: default-on config; `GOVERNED_LEVELS_ALLOWED = False`). The coordinator, merge gate and dashboard items are not built (1.3).

### 4.1 Watcher

Component: watcher (poll, dispatcher, wake transport); exceptions FR-15, FR-16 (and coordinator), NFR-02 (all), NFR-03 (and coordinator).

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| FR-01 | Start a worker only if the issue is open, assigned only to the watcher login, approved (field `Approved`=Yes; label until the field is live) and unedited since, Status in Research, Spec, Plan or Debug, no `hold:backlog`, plan check passing. Assignment alone never starts work. | NEW per-predicate cases in `issue_watch/test_cycle.py` | D01 |
| FR-02 | Repeat every start gate at the moment of start (`_revalidate`, master `cycle.py:979`). | MC-4 | D01, QG1 |
| FR-03 | Keep `marker_in_window` so a hand claim and a watcher start never run two workers; no wake for a claim the poll did not launch. | NEW incl. `test_manual_claim_gets_no_wake` | D01; BS |
| FR-04 | Require the plan before the approval; document that a body edit after approval voids it. | doc; NEW | D01 |
| FR-05 | Run a read-only plan check on the body (memory only) before the approval read; skip as `held_incomplete`; skip `hold:backlog` as `held_backlog`; a `<...>`-only section counts as empty. | NEW: unfilled template fails; body absent from `audit.jsonl` | D09, Q03 |
| FR-06 | Write nothing to GitHub in a poll cycle (NG-2): strip the label writer of PR 686 (`LabelWriter` pr-a `github.py:983-1069`, argv builders `:267-320`, `_hold_write_ok`, `_label_write` `cycle.py:1021-1044`, label rows 3-5 of `_hold_step` `:1064-1119`, `hand_removed`); save the hunk as a patch. | MC-8 | Q03, D09 |
| FR-07 | Create the local `holds` entry with no write; ignore a leftover `hold:plan`; drop the `issue.hold` grant from reference config and fixtures (`tests/issue_watch/conftest.py:286`). | NEW: `writes == []` | Q03 |
| FR-08 | At wake time re-check only the plan check and `hold:backlog` (drop the label test at pr-a `cycle.py:1293-1300`). | NEW | Q03 |
| FR-09 | Put the three info streams behind an off switch (default off) around pr-a `cycle.py:922-935`; a failed info search is a warning, not a stop; if enabled fetch only `could_assign`, after U8. | NEW | QG4 |
| FR-10 | Run from one cron entry `*/5 * * * *` (five fields) under `flock -n`, absolute paths, log `~/.aidev/logs/issue-watch.log`, installed once per boot by the image; no stage installs it before S17. | one `crontab -l` line after two restarts | D02, D14; BS |
| FR-11 | Make cron call `issue-watch run-all`, which runs `once --config <config_dir>/<repo>.json` per project of `orca repo list`; a failed list is an error, never "zero repos"; zero repos served is an alarm; no registry repository, no `repos.yaml`. | planb `test_dispatch.py`; NEW | D07, D02; BS |
| FR-12 | Read per-repo JSON at `schema_version` 1; a key gets loader support in the PR that first reads it; an absent authority key means the most restrictive value; a malformed value is a config error; `reach_daily_max` absent or 0 means no notice cap. | NEW; unknown-key rejection stays (master `cycle.py:216`) | D07, D15 R-3; BS |
| FR-13 | Write each wake by temp file plus rename, mode 0600, at most 64 KiB, before any nudge; items `repo`, `number`, `url` only; three deliveries 10 minutes apart, then mark the Orca workspace unread and exit 7; the poll never writes the ack. | NEW incl. `test_full_wake_with_139_char_repo_names_fits_64_kib` | D10 |
| FR-14 | Treat mailbox and typed line as id-only nudges; type only into an idle person-opened or just-started session (empty draft, 60 s quiet, prompt visible). | NEW; live U5, U25 | D10 |
| FR-15 | Accept an ack only if the per-issue state file exists and matches (M1). | MC-6 | D10 |
| FR-16 | Retarget an abandoned wake with a new linked wake id (M2). | NEW | D10 |
| FR-17 | Treat an unreadable process table as "unknown" and start nothing; prefer `orca agent launch` after the tag spike. | NEW | D10 |
| FR-18 | Use one shared terminal helper with a parity test against `orca_term.py`. | NEW | D10, D15 B9 |
| FR-19 | Rename ack bucket `taken` to `accepted` only with both readers and a pinned schema; an ack names each item. | NEW | D10; BS |
| FR-20 | Hold a reasons table equal to the code: restore the 14 approval reasons; add `coordinator_full`, `name_collision`, `no_checkout`, `coordinator_absent`; remove `registry_invalid`, `repo_not_listed` and four label-write reasons. | MC-10 | D15 E6, R-1 |
| FR-21 | Save claim evidence and the delivery intent (wake id, round, attempt) in ONE store save, release the lock, then publish; replay keeps the wake id and runs even when prechecks fail; an unknown launch receipt never relaunches. | NEW `test_claimed_outbox_replay`, `test_replay_runs_when_prechecks_fail` | BS |
| FR-22 | Back up the store before a schema migration and provide a downgrade step. | MC-11 | BS |
| FR-23 | Keep the watcher off by default: absent `enabled` means off; `DISABLED` works; `GOVERNED_LEVELS_ALLOWED = False` before R18; `auto_enable` ships false (code and defaults file), so `first_run` does not rewrite `enabled: true`; after the S17 throwaway run the owner turns it on once in chat, then repos passing the six `first_run` checks enable themselves (OA-28a). | MC-5; NEW `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing` | D03, D14, OAG3 |
| NFR-01 | Pass absolute `gh` and `orca` paths to every child (cron `PATH` is `/usr/bin:/bin`). | MC-12 | D02; BS |
| NFR-02 | Keep one writer per file (poll: store, audit, wakes; coordinator: acks, per-issue files, go entries; `report-entry`: entry files; `release-worker`: `.ok`). | review against merged section 4 | BS |
| NFR-03 | Read the state root from config `state_dir`; never recompute it. | NEW | BS |
| NFR-04 | Extend `status --json` with `last_sweep_at`, `recent_skips[]`, stranded deliveries, served-repo count, unreadable-state alarm. | NEW | D02, D09; BS |
| FR-82 | Keep NG-2 as "the poll cycle writes nothing to GitHub"; only `repo_init.py` may write, only `gh label create` for the trigger label, only after the owner's chat OK; while `auto_enable` is false the label step reads only and reports `would_create` (design proposal, UNVERIFIED); the go that turns `auto_enable` on covers later repos' trigger label; `hold:backlog` stays by hand. | planb `test_security_invariants.py:1059-1079` unchanged; NEW | OAG3, D09 |

### 4.2 Coordinator

Component: coordinator; exceptions FR-31 (and guard), FR-33, FR-35 (and watcher), FR-39 (cleanup script).

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| FR-24 | Provide role "coordinator", command `/sc:coordinator`, skill `sc-coordinator-protocol`, flags `--wake <id>`, `--hourly`, `--resume`, `--take <owner/repo#N>`, `--sub` (evaluation only); no `commands/orchestrator.md`, no `sc-orchestrator-protocol`. | NEW | D08 |
| FR-25 | Treat flag-less `/sc:coordinator` as person-opened: no grant, no merge; grants have one door (`--wake` or `--take`) on a recorded authorization. | NEW | D08 |
| FR-26 | Provide one verb group `superclaude coordinator` (wake-check, wake-ack, state, plan-check, repos, merge, merge-gate, answer-check, audit, report-entry, escalate, handback) with one JSON contract, one state lock and a closed `refuse(argv)` list with a failing test per pattern; no lease, no interrupt. | NEW `tests/coordinator/test_refuse_argv.py`, `test_state_lock.py` | D15 R-7, D8; QG4 |
| FR-27 | Be opened by a person; a script may start it at depth 0 (never `worker-start`) only when the launch prompt cites an owner authorization recorded in chat, after U3 passes and WC:70, WC:245 are approved; say it is self-attested; `coordinator_autostart` absent means false; a missing coordinator is `coordinator_absent`. | NEW; live U3 | D06; BS |
| FR-28 | Pull the wake folder at every `check --wait` return (at most every 5 minutes); take only wakes addressed to itself. | NEW | D10 |
| FR-29 | Adopt a claim: save `issues/<repo-key>__<N>.json` by exclusive create, then ack; read `launch_cwd` through `state`; copy `.dev/issues/<N>/` into the worker worktree. | NEW; kill-and-restart tests | D07, D10; BS |
| FR-30 | Start every worker bound to the guard: `orca_worktree.py pending --level worktree`, marker `[sc-launch:v1:<nonce>]` in the first prompt (restored `brief.py`), preflight, `pending/<nonce>` gone within a stated timeout (60 s proposed, UNVERIFIED) else stop and escalate; no `jq` means no worker. `WORKER_BINDING_PROVEN` (false) refuses a start for any issue outside per-repo `probe_issues`. | NEW; live probe | D05, D04; BS |
| FR-31 | When both gates stay (OA-1): record the plan approval, run `check-approval` (WC-17), write the worker's `sessions/<id>.ok` through restored `release-worker` (W to WA); if the session id cannot be learned bind at F and say the plan gate then rests on the contract only. | `hooks/test_launch_level_guard_worker.py`; NEW | D03, D14; BS |
| FR-32 | Commit the result after `worker_done` with explicit paths plus `.dev/tasks` (`git commit --only`), never `-A`, never `.dev/issues/`, after a branch and base check; escalate a refused commit, never `--no-verify`; push and `/sc:pr-submit --monitor 3` only on a typed go in a person-opened session. | NEW; `WORKER-CONTRACT.md:244-246` | D06; BS |
| FR-33 | Cap work in flight: `max_in_flight` in the child cycle after the sweep, per coordinator id, counting pending, launched, claimed, woken, acked, unknown entries and open claim files once per issue; an unreadable file counts, named; a full repo records `coordinator_full`. Key default 3 (D07); first build enforces 1 until claim agents have their own worktree. The poll closes a store entry from the per-issue phase. | NEW: drain after orphaned `pending`; one issue counted once | D07, QG1; BS |
| FR-34 | Restart a dead coordinator with a resume wake, at most 3 times (stored counter); an unreadable terminal list restarts nothing; until Coder 516 the duty holder is `ORCH-IronClaude` and nothing restarts; key `coordinator_session`. | NEW | D07; BS |
| FR-35 | Run the hand-back loop (`handback`: stop on empty list, `HANDBACK_MAX` 3 "not measured", `no_progress`; old worker final first; idempotent re-plan marker); round 2 re-plans with `/sc:issue --plan <N> --remaining <file> --depth <d>`, enters `waiting_reapproval` (outside the cap, a visible reason, expiring to `stopped` only on an owner-set limit with no default, which frees no capacity), then the poll gives a NEW wake id and the whole start gate repeats. | NEW: re-plan voids approval; three waiting hand-backs never cause `coordinator_full` | QG1, D15 D18; BS |
| FR-36 | Run audit AU1-AU8 (AU5 narrowed to `<<<<<<< ` or `>>>>>>> `) and state it cannot see a push with no PR. | NEW | D15 D15, D05 |
| FR-37 | Write an escalation or entry first, send nothing if refused; on a name-check failure write anyway with a visible marker, original in the action log; fail closed only on a structurally bad call; scan only `report-entry` and `escalate`, after U54. | NEW | QG2, QG4 |
| FR-38 | Each cycle run `/sc:sweep`, call `/sc:closeout <PR>` per merged PR under a go naming the close, run cleanup `list`; `--apply` only on a recorded go naming it; never run `/sc:closeout` as a worker. | NEW | D13, QG3, Q01 |
| FR-39 | Hold the cleanup script (issue 687, adapted) to Q02: local `git branch -d` only (never `-D`, `--force`, `rm`, `prune`, remote delete); never `master`, `main`, `integration`, the default branch; keep the branch if any PR with this head is OPEN or its `headRepositoryOwner` is not ours; dry run shows the branch action and PR head sha; refusals keep the whole worktree; first week report-only. | NEW: four cases; never-force test stays | Q02, D13 |
| FR-40 | Type into worker terminals only under the four typing rules (never approve a permission prompt); never interrupt a worker; reserve the lease comment (trigger: a second host or user polls; stale-lease rule first; marker `sc:coordinator:lease`). | NEW | D15 D14, QG4 |

### 4.3 Dashboard and observability

Component: observability (sweep FR-41, FR-42; docs FR-43; observer FR-44, FR-79 to FR-81; report FR-45 to FR-47, FR-49, FR-50; coordinator verb FR-48). New numbers: PR 539 (owner's merged `/sc:sweep`), PR 684 (Clay's merged work-report skill move).

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| FR-41 | Add `session_id` and `worktree_path` (empty allowed) to sweep JSON v1 rows with a reviewed golden-test edit (rows have neither: master `cli/sweep/report.py:642-661`); one row per session. | sweep contract test plus NEW | D11 |
| FR-42 | Save the sweep JSON as `<UTC>-sweep.json` in `.dev/sweeps/` beside its Markdown report, same `to_json` call, same stem and suffix, temp file then link, never overwrite (today stdout only: master `cli/sweep/commands.py:277-278`); "each reader sweeps" is not adopted; WC-16 (one coordinator sweep per 5 minutes) unchanged. | NEW: both files exist; a same-second second run overwrites neither | D11, OAG2 |
| FR-43 | Write `docs/designs/observe-sweep-contract.md` (unwritten since 2026-11-13) first: three readers, `session_id` join key, one amendment rule. | file exists before S5 code | D11 |
| FR-44 | Make the observer read `issue-watch status --json` and the saved sweep JSON; no Options, Recommendation or write; empty folder, zero rows and "could not read" are three states; held issues, stranded deliveries and a zero-repos run visible. | NEW in `tests/observe/` | D11, D09; BS |
| FR-45 | Make the report read transcripts for the sweep's session ids PLUS every not-done session of the previous report even if its worktree is gone; remove its own session map only after one LIVE side-by-side run shows parity; write `read: false` when Orca is down. | NEW; live run | D11 |
| FR-46 | Remove person-specific config from the report (`"person": "clayphi"`), make the state path per-user, store only `session_id` in entry files (follow-up to PR 684). | NEW | D11, D15 E1, E2 |
| FR-47 | Use the nine-row table in the notice step only ("the person"; exactly nine rows); keep the 5-a-day cap a proposal (default 0; no generator writes 5). | NEW | D11, QG2 |
| FR-48 | Make `report-entry` the only writer of an entry file. | NEW | D15 E7 |
| FR-49 | Show AU4a, AU4c, AU5 as lines of the issue's entry, marked so the sweep lists them as waiting on a person; reserve a push notice until the owner asks with a cap number, a sender is built and tested, and the verb accepts row 8 alone (UNVERIFIED). | NEW | QG2 |
| FR-50 | Keep the report's silent-loss rules, `check.py`, `run.py gate` and its single `involves` search per org. | `skills/test_agent_work_report.py` | D11, QG4 |
| FR-79 | Make the observer read the newest `*-sweep.json` whose `scope.root` is its own and show `window`, `observed_at` and age; a missing or old file is its own state, never "no sessions". JSON v1 already holds these fields (master `cli/sweep/report.py:621-631`). The report runs its own `sweep run --window <time since its last report>` when a file's window is shorter. | NEW: wrong-root, old, missing files each give their own state | OAG2 |
| FR-80 | Show observer entry fields only from an owner-named allowlist, never `recommend` or `suggested` (model-written, `skills/agent-work-report/scripts/common.py:139-141`), `how` hidden until reviewed; each through `sanitize()` as `rich.Text`, block fields length-capped; titles and links only while `report-entry` is absent. | NEW: `[bold red]x[/]` shows literally; a 5,000-character field is clipped | OAG2 |
| FR-81 | Label the questions panel "questions read from Orca directly; a question already handled can appear open" (`observe/questions.py:9-12`); say "one source for session facts (the sweep); the questions panel is the one exception"; file a follow-up for one shared question id (not a release blocker). | NEW label test | OAG2, D11 |

### 4.4 Claim-to-work pipeline

Component: claim pipeline (`/sc:issue` skill and guard); exceptions FR-52 (watcher), FR-54 (and watcher), FR-59, FR-61 (coordinator).

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| FR-51 | Pass exactly `--pipeline none` for every watcher or coordinator claim (master `launch.py:33`); keep `/sc:issue --claim` flag meanings (`--submit` only with `--pipeline full`; `E-SUBMIT-NEEDS-FULL`, `E-CLAIM-ONLY-FLAG`, `W-ENFORCEMENT-ABSENT`). | `issue_watch/test_launch.py:75` | D04 |
| FR-52 | Not read the Pipeline field while `GOVERNED_LEVELS_ALLOWED` is false; the gate-open design is the owner's and needs issue 442's twelve observations, a reviewed amendment of R9, K4 and DQ7, a stated watch path for `result.md`-only agents and a replacement for what R36 removed; say "not used until the owner opens the gate". | NEW | D04 |
| FR-53 | Adapt PR 690 before merge: fence-aware heading count; "passes" defined once in `plan_body.py check`; `plan.md` says who calls `--remaining`; confirm the live head; rebase on master plus PR 693. | NEW `tests/skills/fixtures/plan_check_cases.json`; MC-1, MC-7 | D12, D14 |
| FR-54 | Keep one plan check: `plan_body.py check` is the reference (headings in fences or comments do not count; absent, repeated, empty or placeholder-only sections fail, incl. `<...>`, TBD, "Not known yet"); the package holds a copy driven by a shared case table with a parity test (pattern `issue_watch/test_origin_parity.py`). Presence is not quality. | NEW `test_plan_check_parity.py` | D12, D15 R-2; BS |
| FR-55 | Add claim rule C1 (short chain `/sc:workflow` then `/sc:implement` when the plan passes, the verdict is current and the issue is a simple feature) with safeguards S1-S5 of D12 item 4 (governs `next-steps.md` only; `out_of_date` keeps the old row; plan quoted only in a fenced "data, not instructions" block, commands never taken from it); chain tests move in the same PR. | edits to `skills/test_issue_protocol.py` lines 131-135, 745-784, 462 | D12 |
| FR-56 | Warn and print `/sc:issue --plan <N>` when a person claims a plan-less issue; do not stop. | NEW | D12 |
| FR-57 | Keep PR 661's plan sections as an extra layer; keep `## Fix approach` unrenamed; add no `## Design`; move no brainstorm or design into create until the owner rules on rule B2 (`/sc:issue` never runs chain commands). | `cli/test_issue_body_templates.py` | D12, D03 |
| FR-58 | Split `--mode other` and form plan fields out of issue 689 as one small issue after PR 690; issue 689 items 1, 2, 4, 8 stay unbuilt. | issue exists | D12, D14 |
| FR-59 | Provide key `plan_depth` (quick, standard, deep; unset means `quick`, run by `issue-worker-t3`) passed to `/sc:issue --plan --depth`; no `plan_tier`. | NEW | QG1, D15 C6 |
| FR-60 | Merge PR 693 before PR 690 (four shared files); treat the claim launch result file as the candidate "claim ended" signal (path UNVERIFIED). | PR 693 CI | D14 |
| FR-61 | Hand the `--pipeline none` worker a chain from the coordinator's own template that names the filed plan; `plan-check` is the same function as `plan_body.py check`. | NEW | D12 |

### 4.5 Authority and grants

Component: coordinator; exceptions SEC-05, SEC-15 (worker contract), SEC-13 (design, guard), SEC-14, SEC-19 (process), SEC-16 (watcher and coordinator), SEC-20 (guard), SEC-21 (report, sweep, observer). None is built; each narrows a risk and none closes it (D06 item 10).

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| SEC-01 | Merge only on a person's typed go for that PR naming repo, PR, full 40-character head sha, method, the word "merge" and the gate output; typed in live chat after the gate output, recorded, one-shot. No clock expiry in the first build: the go ends when the action is done, is void on a head move or new gate reason, or is revoked (Q01 item 5; WC:241). A passing gate never triggers a merge. Merge automation must carry a go age check and refuse to start until the owner records hours or "none" (24 hours UNVERIFIED). | NEW T13 `tests/coordinator/test_merge_path.py`; NEW: automation without a number or "none" refuses | D06, Q01, OAG1 |
| SEC-02 | Run `merge-gate` (13 closed reasons plus "no recorded merge go", read-only) before the go and again before `gh pr merge <N> --repo <R> --<method> --match-head-commit <sha>`; never `--auto`, `--admin`, `--delete-branch`; refuse if reason, thread, review, base or draft state differs. | T13 | D06, D04, D15 D1 |
| SEC-03 | Never let a go override the eleven refusal reasons of D06 item 3 (`head_moved`, `draft`, `changes_requested`, `review_stalled` and the others); only `checks_failing` and `merge_safety` may be overridden, each with its own key. | T13 | D06, D15 D2 |
| SEC-04 | Keep `/sc:pr-submit`'s silent-reviewer skip in its loop; add a merge-time hold: owner-set `reviewers` list (`none` an explicit exception), re-request on the final head, wait 60 minutes from when its checks finish (UNVERIFIED, owner-settable), then escalate; `review_stalled`, `review_none_present` and `changes_requested` are not overridable. | NEW: 59 minutes holds, 60 escalates | D06, D15 D3, OAG1 |
| SEC-05 | Never run `/sc:pr-submit` or `/sc:closeout` as a `worker-start` worker. | `skills/test_worker_contract.py` (WC:23, WC:244) | D06, D15 D11 |
| SEC-06 | Carry no standing `pr.merge` or `issue.close`; refuse both as grant names. | NEW | D04, D06, QG3 |
| SEC-07 | Start with empty `grants`; the owner grants at most `issue.assign`, `issue.comment`, `issue.body.append_plan_sections` once in chat, recorded by an agent with `repos grant`; missing or malformed means none; log each use naming its go. | NEW: one `E-NO-GRANT` case per entry | QG3, Q01, Q03 |
| SEC-08 | Accept a recorded go only with the owner's quoted words, date, exact scope and recorder, plus four checks (typed by a person in their own session, never relayed; right entry; newer than the entry's last edit; question key matches, for a merge `merge_safety:<PR>:<head sha>`); a go ends when done, when the head moves or on revocation; a consumed go is never restored. | NEW | Q01 |
| SEC-09 | Make `answer-check` validate entry, key, head sha and freshness with the owner identity a parameter; state it cannot tell a person from a script (OA-6). | NEW | D06, Q01 |
| SEC-10 | Protect the per-repo config twice: `repos` verbs refuse to write `reach_daily_max`, `grants`, `merge_safety_files`, `reviewers` without an accepted record, plus a Write/Edit hook; and fail closed on weakening values (`merge_safety_files: []`, `reviewers: none`, bad `reach_daily_max`) unless a record names them. | NEW `test_config_weakening_refused` | QG3, D15 C-INV-3 |
| SEC-11 | Refuse unconditionally the tag and publish commands of QG3 item 1 (`git tag`, `gh release create`, `uv publish`, `npm publish` and the others; N6), one test each, none passable by `--answer-ref`; merging a release PR stays allowed on the per-PR go. | NEW (three entries UNVERIFIED against design line 763) | QG3 |
| SEC-12 | Let one per-PR go ("merge PR N at sha X, then close issue M if closeout's verdict is done") cover merge and close; no standing close; a restart between them reads the recorded go; state that a `Fixes` line still closes at merge. | NEW `test_closeout_needs_named_close_go` | QG3, D15 C-INV-4 |
| SEC-13 | Require the guard for every worker, worded "narrows honest drift on master and main"; never claim it closes Clay's risk K12 (workers unguarded on an unprotected `master`); state that a worker's own script can still push a feature branch, open a PR, comment, or on one shared admin login `gh pr merge --admin`. | NEW | D05, D06; BS |
| SEC-14 | Give every approval, go and ruling in the owner's chat; an agent records it (quoted words, date, scope, recorder) in an interim ledger (one file in the unification work's task package under `.dev/tasks/`, always staged), imported at S13 by a local commit on `coordinators`; the owner writes no file; silence is never a yes. | one entry per answer before each stage | Q01, D16; BS |
| SEC-15 | Amend `WORKER-CONTRACT.md` only after the owner's chat approval: line 57 ("given by the owner in chat and recorded by the agent"; installed text says "still written by the owner"; own commit), line 70 (script-started coordinator), line 245 (Full Submit push is the person's go for that push and PR only); lines 23, 244 stay. | `skills/test_worker_contract.py` | Q01, D06, D14 |
| SEC-16 | Let no GitHub text reach a prompt, typed line, mailbox subject or argv; only a pattern-checked builder's value does. | `issue_watch/test_launch.py`; FR-13 test | D10 |
| SEC-17 | Never let marker-bearing text (`[sc-launch:v1:...]`) reach a coordinator session. | NEW | BS |
| SEC-18 | Write every control as "narrows"; list residual risks (spoofed typing, self-attested launch prompt, unprotected `master`, the coordinator's own shell). | NEW grep test | D06 |
| SEC-19 | Record the cleanup `--apply` go and the cleanup-design approval in chat; an agent posts to issue 687 only on an instruction naming that post. | ledger entry | Q01, D13 |
| SEC-20 | Keep G2 rule 2 (a bound worker's `send` and `ask` are one plain call, no `--to`); restore G2 rule 1 with the approval verbs and a TAMPER class for any coordinator verb that writes an approval or release file. | `hooks/test_launch_level_guard_worker.py` | D05, D03 |
| SEC-21 | Show a PR waiting for a go as "waiting on a person" with the age of the wait (report entry lines, sweep, observer); no push notice in the first build; a waiting merge go keeps its slot, counts toward `max_in_flight` and never expires; silence is never a yes; only a `waiting_reapproval` hand-back may expire, on an owner-set limit. | NEW: a go waiting 3 days is shown with its age, no message sent | OAG1, QG1, QG2 |

### 4.6 Names and migration

Component: all; watcher FR-63, FR-67, FR-70; docs FR-64, FR-65, FR-68, FR-69; hosts FR-66.

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| FR-62 | Use "coordinator" for the session role; "orchestrator" only for Orca's layer, the parent-session sense in 63 installed files, quoted issue titles and "orchestrated issue flow"; session `COORD-<RepoName>` (ccsession tag or only an Orca terminal name: UNVERIFIED, U25); the report session keeps tag `coordinator`, prefix `coordinator-`, state `.dev/coordinator/`. | NEW allowlist test | D08 |
| FR-63 | Rename before PR 686 merges: `orchestrator-wake/1` and `-ack/1`, mailbox kind, key `orchestrator_tier`, `.orchestrator/`, golden fixture, typed line, `superclaude orchestrator ...` verbs. | `issue_watch/test_wake.py`, `test_launch.py:98-99` | D08, D15 G3 |
| FR-64 | State that `Coordinator` is the working branch and worktree and `coordinators` the shared records branch. | glossary line | D08 |
| FR-65 | Add a glossary line to `HOW-WE-WORK.md` (with its byte copy in `plugins/superclaude/skills/sc-recommend/refs/` and level-table copy in `core/CLAUDE.md`) and the command; edit `core/CLAUDE.md:58`, `skills/ccsession-tag/README.md:423` and `core/test_orca_session_launch_guidance.py` lines 33, 53 in one PR; the titles of issues 339, 423, 444 (owner's orchestrator-mode, knowledge-layer and sub-coordinator issues) and 655 (Clay's tracking issue) stay. | `cli/test_how_we_work_install.py` | D08 |
| FR-66 | Diff installed guard and contract against the repository on each host before any `superclaude install`; install after the revert; no blanket `--force` until the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) are confirmed (PR 633's retire step would remove skills of 632, 650, 656). | per-host record | D14, D03 |
| FR-67 | Key config, store and worktree on `owner/name`; until then a duplicate short name is a `name_collision` skip. | NEW | D07; BS |
| FR-68 | Amend `docs/designs/orchestrator.md` (PR 681, Clay's merged design) by banner and new PR: banner "contested, not owner-approved; checked 2026-11-20" and correction of the three "gate retired" statements (R1 line 73; section 7 lines 987-1004, 1017, 1095, 1381) in the revert PR; later the rows D15 section 6 names, or a new `docs/designs/coordinator.md`. No builder starts PR B or PR E before it merges. | S10 greps; no control "closes" a risk | D03, D14, D15 G6 |
| FR-69 | Correct the owner's cron rationale (requirements line 18 in planb; Coder 515 text): a precheck that exits non-zero starts no agent; give the real reasons; fix "debated and rejected" and the six-field cron line in `docs/designs/issue-watcher-setup.md`. | text diff | D02, D15 B1 |
| FR-70 | Give claim agents their own worktree or keep `max_in_flight` 1; real rollout stays off until the X-001 live check (claim terminal lifetime, live-agent list, worker worktree path) is recorded and the owner picks the route (OA-23). | S17 record | D07; BS |

### 4.7 Process and governance

Component: process (the owner, Clay, GitHub settings); FR-75 and FR-77 need the repository admin; NFR-05, NFR-06 apply to all.

| ID | The system shall | Acceptance check | Source |
|---|---|---|---|
| FR-71 | Hold PR 686 and PR 690 as drafts until the owner rules (H0). | `gh pr view 686 --repo IronbellyOrg/IronClaude --json isDraft` true; same for 690 | D14, D16 |
| FR-72 | Open the revert of PR 682 (commit `01e7a9e23`) only if the owner says BOTH gates stay, after a clean-checkout dry run at a recorded master sha passes; one new PR, no force push; re-apply the "no `--to`" bullet (`skills/test_worker_contract.py` lines 426-429, 3220); resolve `CHANGELOG.md`; PR 686 merges in no form before it. | dry-run record in the PR body (6.2) | D03, D14, D15 A13 |
| FR-73 | Adapt PR 686 in place as ONE draft after the revert, planb, D08 names and PR 690's check; it drops its deletions of D01's must-keep symbols (14 in `predicates.py`, about 30 in `github.py`), the registry, `repos.py`, `repos.yaml`, `wrong_target`. | MC-1 to MC-11 | D14, D01, D07 |
| FR-74 | Apply MC-1 to MC-12 (8.1) to every PR touching `issue_watch/` or restoring `issue_pipeline`. | CI or recorded runs | D14 |
| FR-75 | Add `.github/CODEOWNERS` (sole owner `@ironbelly`; core lines `docs/designs/`, `src/superclaude/core/WORKER-CONTRACT.md`, `/.github/CODEOWNERS`; temporary lines `src/superclaude/cli/issue_watch/`, `src/superclaude/skills/sc-issue-protocol/`), then an admin-only ruleset on `master` and `integration` (PR required, 0 approvals, code-owner review, dismiss stale approvals, no force push, no deletion, admin bypass for PRs only). | FR-77 | D16 |
| FR-76 | Add "who rules, and what needs a second person" to root `CLAUDE.md` (D16 section B), a pointer in `HOW-WE-WORK.md`, one line in `CONTRIBUTING.md`, two PR-template lines; finish issue 290 (Clay's contribution-rules issue); Clay accepts the roles in writing first. | PR merged; copy tests pass | D16 |
| FR-77 | After the ruleset is active run the throwaway test: Clay's account edits one line under `docs/designs/` with no approval, expected BLOCKED and REVIEW_REQUIRED; repeat on `integration`; an owner-authored PR shows whether the bypass is needed; close all unmerged. Fallbacks: require 1 approval; "required reviewers" rule; or drop the gate and keep the words. | three recorded PR states; owner's go first | D16 |
| FR-78 | Seed `docs/decisions.md` (one file, about 10 ruling groups); 14-day review (gated PRs, median wait, waits over 3 working days, silent passes); drop the temporary CODEOWNERS lines when the owner says the 655 series is reconciled. | file and review exist | D16 |
| NFR-05 | Label every unproven number UNVERIFIED; prove the live unknowns (U5, U25, U28, U30, U3, U8, U54) before the poll is enabled. | 13.2 record | D10, D15 |
| NFR-06 | Run suites through `uv run`; edit installed primitives under `src/superclaude/`, then `make sync-dev` and `make verify-sync`; stage `.dev/tasks` always, `.claude/` never; installed primitives name only installed paths (MC-9). | MC-7, MC-9 | project `CLAUDE.md` |

## 5. Local changes

A local change is an edit in a checkout that becomes a PR only on the owner's go (section 6). Order codes (D14, D15): H0 hold; L1 lane 1 (PR 693, PR 690, claim rule C1); L2 lane 2 (dry run, revert, amendments, planb, design amendment, adapted PR 686); L3 lane 3 (text, sweep, report); O4-O7 coordinator build and live tests; stages S0-S17 are in section 8. Numbers: PR 693 (owner's claim-launch-result PR), PR 690 (Clay's `/sc:issue --plan` PR), PR 685 (owner's runbook PR for issue 442, the guard's live observations), PR 686 (Clay's open watcher rewrite), PR 682 (Clay's merged deletion), issue 687 (Clay's cleanup request).

### 5.1 Changes to make

| # | Files and what | Requirements | Order |
|---|---|---|---|
| L-01 | Interim ledger of owner answers: one file in the unification work's task package under `.dev/tasks/` (name UNVERIFIED); `git add .dev/tasks`; the recorder commits it when the owner says. | SEC-14 | H0 |
| L-02 | Text touching no contested file: glossary line in `src/superclaude/core/HOW-WE-WORK.md` with byte copy and level-table copy; five-field cron line in `docs/designs/issue-watcher-setup.md`; `agent-work-report/SKILL.md:12`; banner on `docs/designs/orchestrator.md`; merge PR 685. | FR-65, FR-68, FR-69 | L3 (S4) |
| L-03 | Sweep: `docs/designs/observe-sweep-contract.md` first; `session_id`, `worktree_path` at `src/superclaude/cli/sweep/report.py:642-661`; saved JSON in `cli/sweep/commands.py`; reviewed golden-test edit. | FR-41 to FR-43, FR-79 | L3 (S5) |
| L-04 | PR 690 adaptation on `clayphi/issue-655-pr-p` (who edits: OA-2): fence-aware count, one "passes", `--remaining` caller, rebase on master plus PR 693. | FR-53, FR-54 | L1 (S2) |
| L-05 | Claim rule C1 and plan-less warning: `skills/sc-issue-protocol/refs/claim.md`, `refs/chains.md`, `templates/next-steps.md`, `tests/skills/test_issue_protocol.py`. | FR-55, FR-56 | L1 (S3) |
| L-06 | Revert dry run in a clean throwaway checkout (6.2 step 2). No PR, nothing pushed. | FR-72 | L2 (S6) |
| L-07 | Contract and guard amendment: `src/superclaude/core/WORKER-CONTRACT.md` lines 57, 70, 245 (master numbering) and pre-deletion lines 298, 300; guard comment lines 441-443 (pre-deletion `launch-level-guard.sh`); `core/CLAUDE.md:58`; `skills/ccsession-tag/README.md:423`; the two contract tests; plugin mirror; `make sync-dev`. Line 57 is its own commit after one confirmation; lines 70 and 245 wait for chat approval of R25 (Full Submit as a per-issue go) and R17, R9 (launch-prompt start under a recorded authorization), rows of the owner's unpushed requirements. Independent guard review. | SEC-15, FR-65 | L2 (S8) |
| L-08 | Planb (5.2) carries: skips `held_incomplete`, `held_backlog`; MR-1, MR-2 tests; absolute child paths; `auto_enable` false; loader support for its keys; corrected requirements line 18 and Coder 515 text. | FR-02, FR-03, FR-05, FR-12, FR-23, FR-82, NFR-01, FR-69 | L2 (S9) |
| L-09 | Design amendment, docs only, after the owner's rulings. | FR-68 | L2 (S10) |
| L-10 | PR 686 adaptation on `clayphi/issue-655-pr-a` (who edits: OA-2): renames, wakes under `<state_dir>/wakes/`, M1, M2, store migration, label code stripped, reasons pin, plan-check copy, info-stream switch, shared terminal helper. | FR-05 to FR-09, FR-13 to FR-22, FR-63 | L2 (S11) |
| L-11 | New code after S10 merges: substrate, merge path with the bound worker route, transport, cap, restart, audit, hand-back, `report-entry`, cleanup `list`, observability glue. | FR-24 to FR-50, FR-79 to FR-81, SEC-01 to SEC-13, SEC-21 | O4-O6 (S12-S16) |
| L-12 | Issue edits by their assignees (agents write nothing): issue 687 acceptance text; issue 655 rescoped; issue 450 stays open with Clay's 2026-11-18 comment answered; issue 689 split. | FR-39, FR-58 | after OA-1 |
| L-13 | Per-host check before any `superclaude install`. | FR-66 | after S8 |

### 5.2 The owner's local branch (planb) and what must be re-checked first

Read by the author on 2026-11-20: worktree `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb`, branch `ironbelly/issue-watcher-zero-setup-plan`, HEAD `d0a0a433b` ("zero-setup requirements R1-R34 and plan v5"), based on master `e3e9d636a`, no upstream, not pushed; 225 `git status` entries (D14 counted 348; the figure moves). It edits `issue_watch/{audit,cli,cycle,github,launch,predicates}.py`, `issue_pipeline/{brief,cli,reads}.py` (deleted by PR 682), `core/WORKER-CONTRACT.md` and `hooks/scripts/launch-level-guard.sh`, and overlaps PR 686 on 23 files (7 source). Requirements: `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (121 lines, R1 to R36).

**The state of its `/sc:implement` run is UNCLEAR and must be re-checked before the revert sequence starts.** The ledger `.dev/tasks/done/TASK-WF-requirements-20261119-143917-2/progress.md` ends `T28: complete`, `FINAL: pass`, `ARCHIVE: start`, and the inventory calls the run finished; D14 and D15 say not to resume its "half-finished" ledger across the rebase. Nobody ran its tests. Re-check, read-only, by a session the owner names: `git -C <planb> status --short | wc -l`; whether the ledger folder is complete; `uv run pytest tests/issue_watch` in planb; then the owner states in chat which is true (X-12).

Disposition: (1) nothing before OA-1 and OA-4 are answered; (2) after S7 and S8 the owner commits planb, pushes it as a DRAFT (pushing needs a go) and rebases it on the post-S8 master; modify/delete conflicts on `issue_pipeline/` disappear because the revert restores the package (D03: its 13-file patch applies to the revert tree and fails on current master); (3) the old ledger is not resumed; (4) if OA-1 is "only the start gate", planb rebases onto a tree without `issue_pipeline`, an untested path (RK-4); (5) the owner may split it into dependency-ordered PRs with the same checks.

## 6. Pull request and branch dispositions

**None of these actions is executed by this spec's author, and none may be executed without the owner's go in chat for that named action** (recorded by an agent, SEC-14). Words: KEEP, KEEP-ADAPT, REVERT (one new PR), CLOSE, DRAFT (set to Draft and hold). Every `gh` call names `--repo IronbellyOrg/IronClaude`; PRs open only through `/sc:pr-submit --monitor 3`; a returned URL must read `github.com/IronbellyOrg/IronClaude/pull/N`; nothing touches `SuperClaude-Org/SuperClaude_Framework`. "Clay" is the account `clayphi`. Order words: H0, lane 1, lane 2, lane 3 (D14).

### 6.1 The contested set

| Item | Disposition | Why (verdict) | Preconditions | Steps (recommendation) | Order |
|---|---|---|---|---|---|
| PR 686 (Clay's open watcher rewrite; branch `clayphi/issue-655-pr-a`; head `8e5ae29ad`; 59 files; CI green; no owner review) | DRAFT now, then KEEP-ADAPT in place as ONE draft; not merge, not split, not close | D14; D01 (deletes approval, trigger, Project, approver code); D03 (with the revert it crashes `superclaude --help`, 29 test modules fail at collection); D09, Q03, D10, D07, D08 | revert merged (if both gates stay); planb landed; names settled; PR 690's check merged; MC-1 to MC-11 | H0: ask Clay to mark Draft; then FR-73 and L-10; owner reviews each push; merge only on go | H0; after S10 |
| PR 690 (Clay's open `/sc:issue --plan` and `--remaining`; branch `clayphi/issue-655-pr-p`; head `f3bc77981`; 13 files) | DRAFT now, then KEEP-ADAPT, merge in lane 1 | D12, D14 | PR 693 merged first (four shared files); D12's four fixes with tests; green CI; merge-only trial onto master plus PR 693 (never run) | FR-53; merge on go; then claim rule C1 (S3) | H0; lane 1 |
| PR 693 (owner's open PR saving the claim launch result file, issue 691) | KEEP, merge | D14 | its own `/sc:pr-submit --monitor 3` loop | merge first | lane 1 |
| PR 685 (owner's open PR: issue 442 runbook and results) | KEEP, merge | D14, D05 | own review loop | merge beside S4 | lane 3 |
| PR 682 (Clay's merged deletion of `issue_pipeline`, WC-17, G2 rule 1; commit `01e7a9e23`; 36 files; merged about 66 minutes after opening) | REVERT, conditional | D03, D14 (X-6), D05 | owner says BOTH gates stay (OA-1); dry run (L-06) passes at the current master sha; H0 in place; planb re-checked (5.2). If only the start gate stays, PR 682 stands under D03's three conditions (8.3) | 6.2 | lane 2, before any merge of PR 686 |
| PR 681 (Clay's merged design `docs/designs/orchestrator.md`, 1,412 lines, "approved by the owner (Clay)") | KEEP, not reverted | D14, D15 G6, D16 | none for the banner | banner and same-PR correction inside the revert PR; later owner-reviewed amendment (FR-68); no builder starts PR B or PR E before it merges | lane 2 |
| PR 683 (merged `/sc:closeout`; issue 668 is its request) | KEEP | D13, D14 | its two `/sc:issue --plan` references resolve when PR 690 merges | wire as coordinator step (FR-38) | none |
| PR 684 (merged move of `agent-work-report` skill) | KEEP-ADAPT by follow-up PR | D11, D08, D14 | D08 names; D11 rulings | FR-46 and `SKILL.md:12` wording | lane 3 |
| PR 661 (merged plan sections in the four issue templates; closes issue 651) | KEEP | D12, D03 | none | none | none |
| PR 670 (merged daily log of merged PRs) | KEEP | D13 | none | opt-in automation outside the coordinator | none |

### 6.2 The revert of PR 682, exactly (recommendation)

1. The owner answers OA-1 ("both gates stay") and OA-4 (revert first, planb after); an agent records both. H0 is in place.
2. Dry run in a throwaway clean checkout bound to a recorded master head sha: `git revert --no-commit 01e7a9e23`; MC-1, MC-2, MC-3; `uv run pytest` over the restored `tests/issue_pipeline`, `tests/hooks/test_launch_level_guard_worker.py`, `tests/skills/test_worker_contract.py` and the full suite including `tests/hooks/test_launch_level_guard.py` (it did not finish in D03); `git apply --check` of planb's 13-file patch on the revert tree. Repeat if master moves. Find which verb exposes `brief.build` (UNVERIFIED).
3. One new revert PR of commit `01e7a9e23` (4,599 lines: 2,969 test, 1,618 source), never a force push; only `CHANGELOG.md` conflicts.
4. By hand in the same PR: re-apply the worker-duties bullet "ask and send carry no `--to`" and its assertions in `tests/skills/test_worker_contract.py` (a bare revert drops both silently and tests still pass; the sentence then appears twice, in WC-17 line 59 and the bullet, or WC-17 points at the bullet).
5. Banner and the three "gate retired" corrections go in the same PR (FR-68). Merge on the owner's go after MC-1 to MC-3 and MC-7; no `superclaude install` in this stage (FR-66); independent guard review, version stamp stays 1.
6. Rollback: revert the revert. Do not let PR 686 merge first: git merges both without conflict and the result breaks `superclaude --help`.

### 6.3 Clay's other PRs (every row of `<W>/inventory/clay-prs.md` tables 2A to 2C)

| PR (what it is) | Disposition | Reason and condition |
|---|---|---|
| 499 (pr-submit: name an unreadable Augment marker) | KEEP | extends owner pr-submit work |
| 615 (removes cleanup-audit runner), 616 (removes prd command-line pipeline), 617 (removes `/sc:spawn`) | KEEP | wave 1 approved by the owner on issue 571 (Clay's 6.0.0 plan thread) |
| 621 (removes `/sc:review-translation`, moved to the snapshot fork) | KEEP | the owner said the fork can be the destination (issue 571, 2026-11-17 18:32Z) |
| 620 (removes `/sc:save`, `/sc:load`), 622 (removes `/sc:build`), 627 (removes `/sc:improve`), 629 (removes cli-portify), 631 (removes `/sc:index`, `/sc:index-repo`), 632 (removes roadmap, tasklist, sprint family; edits `sc-issue-protocol/refs/chains.md`), 650 (removes prd, tdd, tech-research and other skills), 656 (removes task, task-builder, roadmap skills and level 4 of `HOW-WE-WORK.md`) | KEEP, not reverted (D14) | no recorded owner approval of waves 2-6 found (UNVERIFIED, comments read in part); already released in 6.0.0 and 6.1.0; the one question to the owner (OA-21) blocks only a host install (FR-66) |
| 625 (launcher alias fixes), 626 (help text fixes), 633 (installer retire step; the hazard of FR-66), 634 (6.0.0 notes), 639 (merge of master into integration), 640 (release 6.0.0), 646 (installer `filecmp` fix), 649 (post-release sync 6.0.0), 653 (re-points task-file routes to `/sc:workflow` then `/sc:implement`; consistent with the owner's PR 613, which stops recommending `/sc:task`), 657 (6.1.0 notes), 659 (docs: cleanupPeriodDays 90), 667 (post-release docs 6.1.0, on `integration` only) | KEEP | independent of the watcher area |
| 652 (withdrawn `/sc:task` removal) and 663 (empty merge), both closed | KEEP, nothing to do | do not revive `clayphi/v61-pr2-sc-task` without the owner's list |
| 658 (6.1.0 release squash-merged by mistake), 662 (owner's revert of 658), 664 (owner's re-merge, merged by Clay) | KEEP, settled | settled by 662 and 664 |
| 481 (ccsession server-error retry), 494 (v5 test doc fix), 570 (ccsession heading and retention), 608 (plain-English style), 619 (`HOW-WE-WORK` shipping flow), 628 and 630 (ccsession speed), 641 (ccsession human-saved sessions), 666 (confirmation before `--prune --apply`) | KEEP | no watcher-area paths touched |

### 6.4 Owner PRs, issues and branches touched

| Item | Disposition | Note |
|---|---|---|
| PRs 584, 591 (owner's merged Plan A and Plan B: approval package, coordinator handoff) | restored by the revert | D03 |
| Issue 655 (Clay's tracking issue "replaces #450") | KEEP and RESCOPE | assignee drops "replaces #450" (D14) |
| Issue 450 (owner's rollout issue) | KEEP open | Clay's 2026-11-18 17:00:32 comment has no recorded answer; the owner answers |
| Issue 687 (Clay's cleanup request) | KEEP-ADAPT (text; nothing built) | after the owner's chat approval of the design and of `git branch -d` under Q02 |
| Issue 689 (Clay's create-time design request) | SPLIT and DEFER | FR-58 |
| Issue 409 and PR 409 (owner's dashboard design issue, assigned to Clay, and its design package) | KEEP | D11: the observer is the one screen |
| Issues 339, 423, 444 (owner's orchestrator-mode, knowledge-layer, sub-coordinator issues) | KEEP open; titles unchanged | glossary (FR-65) |
| Branches: `clayphi/issue-655-pr-a` (PR 686), `-pr-p` (PR 690) follow their PRs; `-pr-c` (684), `-pr-d` (682), `-spec-pr` (681), `issue-668-build-p3` (683), `release-6.0.0`, `v61-*`, `v6-post-release`, `ccsession-*`, `433-ccsession-orca-resume`, `docs-v5-impact-validation`, `help-472-473`, `issue-651-plan-fields`, `v61-part-b-map` (no PR; planning records), `v61-pr2-sc-task` (closed 652) | KEEP | remote branch deletion is human-only; do not revive `v61-pr2-sc-task` |
| `integration` (2 ahead of master, 10 behind) | KEEP | in the ruleset (FR-75) |

## 7. Clay strengths adopted

Condensed from D15's 71-element table (`debates/D15/VERDICT.md` section 4; ids A1-G7 are D15's element ids, not verdict ids; 13 + 11 + 8 + 20 + 7 + 5 + 7 = 71). ADOPT = as is; ADOPT+CHANGE; DEFER (owner decision or trigger); REJECT. "686a" is PR 686 (Clay's open watcher rewrite) as adapted; "PB" is Clay's unbuilt coordinator verb group (PR B). Order codes O0-O7 are in section 5; stages in section 8. Elements with no change in carrier or strategy share a row.

| Element ids | Decision | Carrier, order | Merge or override strategy |
|---|---|---|---|
| A1 plan check and `held_incomplete`; A2 one "passes"; A3 `hold:backlog` stop | ADOPT+CHANGE | 686a, planb; O1, O3 | placeholder-only rule; before the approval read; poll only reads the label (FR-05, FR-54) |
| A4 plan request after one hour with titles | DEFER | none | a wake item, titles are free GitHub text |
| A5 `hold:plan` label write | REJECT now; deferred PR | 686a; O3 | strip (FR-06); return only with a shown reader, NG-2 amendment, 24-hour shadow run, cron write test |
| A6 plan sections in templates (PR 661) | ADOPT | merged | extra layer, never a replacement for approval |
| A7 `--plan`; A8 `--remaining`; A9 claim reads the plan; A10 `--mode other` | ADOPT+CHANGE | PR 690, claim files, new issue; O1 | four fixes (FR-53); owner's smaller rule C1 (FR-55) |
| A11 brainstorm and design into create | REJECT now | none; O0 | owner decides rule B2 |
| A12 assignment alone as trigger | REJECT | docs; O1 | keep Clay's "conditions to revisit" (guard effective; workers cannot push or merge; skip when claim record exists; owner records the reversal) |
| A13 deletion of plan-approval code (PR 682) | REJECT (revert), on D14's condition | REV; O2 | section 6.2 |
| B1 precheck pattern; B2 Orca automation as scheduler | B1 ADOPT+CHANGE (fallback); B2 REJECT | docs; O1, O7 | correct the reason; cron stays; fallback after the firing test |
| B3 wake file and ack; B4 mailbox; B5 typed line; B6 start a session; B7 read wakes at each `check --wait`; B8 no GitHub text in a typed line | ADOPT+CHANGE (B7, B8 as is) | 686a, PB; O3, O6 | M1, M2, no titles, pinned ack schema (FR-13 to FR-19) |
| B9 copied `orca_term.py` | REJECT | 686a | one helper plus parity test |
| B10 org-wide search; B11 info streams | ADOPT+CHANGE, both off | 686a; O3 | off by default, fail open (FR-09) |
| C1 in-flight cap; C2 guarded restart; C3 per-repo keys; C4 exclusive-create state, `owner/name` keys | ADOPT+CHANGE | planb; O1, O2, O5, O6 | per-repo JSON; closing writer; cap 1 until claim isolation (FR-33, FR-34, FR-12, FR-67) |
| C5 registry repository, allow list, idle end, `wrong_target`; C7 `setup-clone` | REJECT | 686a; O3 | remove; `no_checkout` skip instead |
| C6 tier settings | ADOPT+CHANGE | planb, PB; O2, O6, O7 | requests until U28; `plan_depth` (FR-59) |
| C8 lease comment | DEFER | docs | reserved with trigger (FR-40) |
| D1 `merge-gate`; D2 hard refusal and `merge_safety` (as is); D3 reviewer hold; D4 `answer-check`; D5 `E-NO-GRANT`; D6 standing grants (three) | ADOPT+CHANGE | PB, one tested unit; O5 | per-PR go on head sha; fail closed; default empty (SEC-01 to SEC-10) |
| D7 standing merge and close; D9 interrupt N7; D13 "workers run unbound, decided" | REJECT | docs; O1 | rewrite DQ8, wave 7, K7; delete N7; keep K12 as a risk row |
| D8 closed "may do" list, `refuse(argv)` | ADOPT+CHANGE | PB; O4 | N6 unconditional, no N7 (SEC-11, FR-26) |
| D10 script-started coordinator; D11 "standing-grant coordinator" name (worker running `/sc:pr-submit` REJECT) | ADOPT+CHANGE | contract amendment, PB; O2 | recorded authorization, self-attested (SEC-15) |
| D12 one supervised `worker-start` route | ADOPT+CHANGE | PB; O5, O7 | guard required and staged (FR-30) |
| D14 typing into worker terminals | ADOPT+CHANGE | PB; O6 | reject approving permission prompts |
| D15 audit AU1-AU8; D16 nine-row table; D17 cap of 5 (DEFER); D18 hand-back; D19 naming rule (DEFER); D20 typed answers (as is) | ADOPT+CHANGE unless marked | PB, report; O6 | AU5 narrowed; notice step only (FR-35 to FR-37, FR-47) |
| E1 report skill; E2 living report; E4 transcript reader; E5 item template; E6 reason table; E7 `report-entry`; E3 silent-loss rules (as is) | ADOPT+CHANGE | report follow-up, 686a, PB; O3, O6 | FR-45 to FR-48, FR-20 |
| F1 `/sc:closeout`; F2 `branch-landed.sh`; F5 daily log (PR 670) | ADOPT | merged; O1, O6 | coordinator step under a go naming the close (FR-38) |
| F3 cleanup (nine rules); F4 evidence-repo save | ADOPT+CHANGE | issue 687 build | Q02 refusals; `--apply` on a recorded go (FR-39) |
| G1 tests T1-T13; G2 flags; G3 persisted names; G6 design text (PR 681) | ADOPT+CHANGE | PB, glossary, docs; O1-O7 | T1, T3, T4, T8, T10, T11 logic rewritten, T12 for hand-back; rename sweep (FR-63); amend not revert (FR-68) |
| G4 risk register; G5 removal plan and PR B test rows (as is); G7 open-questions table (process) | ADOPT | docs, process; O1 | carry into the "narrows" wording |

D15's four new HIGH conditions are FR-33 and FR-35 (C-INV-1, C-INV-2), SEC-10 (C-INV-3) and SEC-12 (C-INV-4); its seven resolved conflicts R-1 to R-7 are in section 11.

## 8. Staged migration

Rules for every stage: one reviewable PR, one local action or one consented host operation; a stage never enables a later one; no stage schedules `run-all` or installs cron before S17 (only `run-all --dry-run` runs earlier); `auto_enable` stays false; the `DISABLED` kill file works throughout; every stage reverts by reverting its PR. "Owner gate" is the owner's go for that named action, recorded by an agent (SEC-14); a typed go precedes every push and merge. Run suites with `uv run`; run `make sync-dev`; never stage `.claude/`. A green PR 686 alone does not prove the combined tree. Source: merged design section 5, order fixed by D14 and D15. Numbers: PR 693 (owner's claim-launch-result PR), PR 690 (Clay's `/sc:issue --plan` PR), PR 685 (owner's issue 442 runbook PR), PR 682 (Clay's merged deletion), PR 686 (Clay's watcher rewrite), issue 442 (live guard observations), Coder issues 515 and 516 (cron at boot; `Coordinator` worktree and session).

### 8.1 Mechanical merge checks, defined once

MC-1 `uv run superclaude --help` exits 0. MC-2 every package under `src/superclaude/cli/` imports (NEW `tests/cli/test_cli_packages_import.py`). MC-3 names check: every name the restored `issue_pipeline` imports from `issue_watch` exists (35 names; 9 missing on the PR 686 head, among them `EVENTS_JQ`, `argv_edits`, `github.edits`, `github.events`; NEW `tests/issue_watch/test_restored_package_names.py`). MC-4 removing the approval between wake and start refuses. MC-5 `enabled` absent means off. MC-6 an ack without a state file leaves the wake entry in place. MC-7 `make verify-sync` passes and no `.claude/` path is staged. MC-8 NG-2: `test_every_argv_of_the_cycle_is_an_allowed_form` and `test_the_five_cycles_together_use_every_allowed_form_and_nothing_else` (`tests/issue_watch/test_security_invariants.py:652, 683`) pass with no write verb. MC-9 `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}`: every hit justified. MC-10 the reasons table equals the code's reason set (FR-20). MC-11 an old binary given a new store fails closed with a named reason and the downgrade step restores the backup. MC-12 `env -i PATH=/usr/bin:/bin <abs path>/superclaude issue-watch run-all --dry-run` serves every configured repo or names why not, and generates nothing.

### 8.2 Stages

| Stage | Scope | Preconditions | Deliverables and tests | Rollback | Owner gate | Lane |
|---|---|---|---|---|---|---|
| S0 owner decides in chat and holds the open PRs | no code; ask Clay to make PRs 686 and 690 Drafts; recommend the ruleset; owner answers OA-1 to OA-8, OA-24; agent creates the ledger | none | both `isDraft` true; one ledger entry per answer; read-only check of `master` protection | Clay sets PRs ready; admin deletes any ruleset | owner's chat answers | H0 |
| S1 merge PR 693 | owner's PR | S0 | its CI and loop; MC-1, MC-7 | revert | go for the PR | L1 |
| S2 adapt and merge PR 690 | FR-53, FR-54 | S1; OA-2 | merge-only trial first; fence and case-table tests; MC-1, MC-7 | revert (nothing calls `--plan` yet) | go | L1 |
| S3 claim rule C1, plan-less warning | FR-55, FR-56 | S2 | chain tests moved in the same PR; MC-7 | revert | go | L1 |
| S4 text, names, glossary, cron-line fix, banner, PR 685 | FR-62, FR-65, FR-68 (banner), FR-69; no contested file | S0; OA-10 | HOW-WE-WORK copy tests; MC-7, MC-9 | revert by file | go per PR | L3 |
| S5 sweep note, two fields, saved JSON | FR-41 to FR-43 | none (OA-9 settled) | golden-test edit reviewed by a person; saved file equals stdout | revert | go | L3 |
| S6 revert dry run, no PR | L-06 | OA-1 "both gates stay" | dry-run record for the S7 PR body | delete checkout | none | L2 |
| S7 revert PR 682 | section 6.2 | S0, S6 at current master sha; OA-1, OA-4; planb re-checked | MC-1, MC-2, MC-3, MC-7; `uv run superclaude issue-pipeline --help`; G2 rule 1 tamper tests; restored 117 test functions; no-`--to` sentence test | revert the revert | go | L2 |
| S8 contract and guard amendment | SEC-15, L-07 | S7; OA-7 (line 57 at least) | `test_worker_contract.py` finds no "still written by the owner"; guard tests; MC-7, MC-9; independent guard review; per-host diff before any install | revert; split commits | one confirmation for line 57; chat approval for 70 and 245 | L2 |
| S9 land planb | L-08, 5.2 | S7, S8; OA-4 | planb `test_dispatch.py`, `test_cycle.py`; MC-1 to MC-5, MC-7 to MC-9, MC-12; NEW `test_first_run_keeps_config_off_while_auto_enable_false`, `test_dry_run_generates_nothing`; no governed level launches while R33 is false | revert and restore old config files; master returns to the single-config poll, off | go to commit, to push as a draft, to merge | L2 |
| S10 design amendment | FR-68, docs only | S9; owner rulings recorded | greps of FR-68; MC-7 | revert by file | go | L2 |
| S11 PR 686 adapted, one draft | L-10 | S2, S9, S10; OA-2; D08 names | MC-1 to MC-11; renamed `test_wake.py`; zero-write NG-2 test; tests of FR-13 to FR-22 | revert; `wake_enabled` false; downgrade step | go | L2 |
| S12 status extension, `owner/name` rekey | NFR-04, FR-67 | S9, S11 | schema-pinned status; `name_collision` test; MC-5, MC-8, MC-12 | revert and remove new keys from generated files (loader rejects unknown keys) | go | L3 |
| S13 coordinator substrate | verb skeleton, `refuse(argv)`, JSON contract, state lock, path map, config write guard; ledger import by a LOCAL commit on `coordinators` | S10 merged; OA-26 | `tests/coordinator/test_refuse_argv.py`, `test_state_lock.py`, config tests; extends `tests/skills/test_primitive_dual_surface_lookup.py`; MC-1, MC-2, MC-7, MC-9 | revert | go | O4 |
| S14 merge path as one unit plus bound worker route | SEC-01 to SEC-13, FR-30 to FR-32, `/sc:coordinator` command and skill | S13; OA-6, OA-11, OA-12, OA-13, OA-27 | T13 `tests/coordinator/test_merge_path.py`; binding tests; skill-text scan; MC-1, MC-2, MC-7, MC-9 | revert; merges typed by hand | go | O5 |
| S15 transport, cap, restart, audit, hand-back, `report-entry`, cleanup `list` (four PRs: S15a wake-check and wake-ack with kill-and-restart tests at every persistence boundary; S15b cap with single writers; S15c AU1-AU8, handback, `report-entry`, `escalate`; S15d cleanup `list`) | FR-28 to FR-40, FR-48 | S14; OA-14, OA-15, OA-16, OA-18, OA-25; Coder 516 for restart | tests in 4.2; `orca worktree rm` behaviour proved first (S15d) | revert per PR | go per PR | O6 |
| S16 observability glue | FR-44 to FR-47, FR-49, FR-50 | S5, S12; owner fills the FR-80 allowlist and cap | three observer states; sanitize test; one live side-by-side map run | revert | go per PR | L3 |
| S17 live tests, then enable one throwaway repo | section 13.2 | S14 to S16; Coder 515, 516 landed; per-host diff then install; all HIGH rows of 12.1 proven or accepted in chat; OA-19, OA-20, OA-23 | S17 pass list (a proposal, UNVERIFIED): the six `first_run` checks green on the throwaway repo, a 24-hour `run-all --dry-run` shadow run that generated and wrote nothing, the X-001 check run, the owner's go; then the owner turns `auto_enable` on once (FR-23). Go/no-go record (code head, host, primitive hashes, fixture captures, failed and passed probes) kept by an agent | `DISABLED`, `enabled: false` or remove the cron line; no data deleted | go per enable | O7 |

S1 to S5 do not depend on lane 2 and can run beside it. S17 does not include raising the cap, Pipeline-field governed launches, label writes, `claim_by: coordinator` or a second polling host; those are separate future changes.

### 8.3 Branch if OA-1 is "only the start gate stays"

PR 682 stands under D03's three conditions. S6 and S7 are dropped; S8 shrinks to lines 57, 70, 245 plus D05's marker line in a new handoff template; S9 rebases planb onto a tree without `issue_pipeline` (untested path); workers are bound at F; the plan-approval step and route A leave FR-31. Confidence in the disposition set falls to about 50 percent (D14).

## 9. Course corrections (process)

Source: D16 (`debates/D16/VERDICT.md`); costs are the advocates' estimates. ADMIN ONLY: only `ironbelly` can do it. State read by D16 on 2026-11-20: `master` unprotected (404), no ruleset, `integration` `protected=false`, no CODEOWNERS file, public repository on the Free plan; `ironbelly` is admin, `clayphi` and `IB-JonathanB` maintain; of the last 100 merged PRs 89 were merged by their own author and none has an APPROVED review. Numbers: PR 681 (Clay's merged design), PRs 686 and 690 (Clay's open watcher rewrite and `/sc:issue --plan` PR), issue 290 (Clay's open contribution-rules issue; the owner answered "only file issues until we have an eval framework"), issues 655 and 450 (Clay's tracking issue; owner's rollout issue).

| Rank | Item | Cost | Who | Admin only |
|---|---|---|---|---|
| 1 | Owner decisions in chat: roles by login, sole code owner `@ironbelly`; a deputy or "nobody" and the channel the owner reads; one-directional gate with admin bypass; `integration` in or out; hold on PRs 686 and 690; seed of the decisions file. A session records each; the owner writes no file. | about 20 min | owner; Clay accepts the roles in writing in rank 3's PR | no |
| 2 | Direct hold: PRs 686 and 690 wait for the owner's ruling; Clay sets both to Draft | 5 min | owner says it; Clay converts | no |
| 3 | Rule text in root `CLAUDE.md`, pointer in `HOW-WE-WORK.md`, line in `CONTRIBUTING.md`, two PR-template lines; finishes issue 290 (FR-76) | 60-90 min, one PR | any maintainer | no |
| 4 | `.github/CODEOWNERS` (FR-75); inert until rank 5 | 15 min | any maintainer, by PR | file no; enforcement needs rank 5 |
| 5 | Ruleset on `master` and `integration` (FR-75) | 15-30 min | `ironbelly` | YES |
| 6 | Throwaway test (FR-77); writes to GitHub, so the owner says go first | about 5 min per PR | Clay's account; one owner-authored PR | no (needs rank 5) |
| 7 | Announcement in chat that the gate is live and binds non-owners | few min | owner | no |
| 8 | `docs/decisions.md`, about 10 ruling groups (FR-78) | 1-2 h session time | a session drafts; owner approves wording in chat | no |
| 9 | 14-day review; temporary CODEOWNERS lines out when the owner says the 655 series is reconciled | 20 min | owner and Clay | no |
| 10-12 | Tripwire items only: CI check for deletions of recent code; CODEOWNERS lines on root `CLAUDE.md` and `docs/decisions.md`; optional guard-file lines | 2-4 h; 5 min; 5 min | maintainer writes | required status: YES |

Order: 1, 2, then 3 and 4 in parallel; 5 after 4 merges; 6 after 5; 7 after 6 passes and 3 is merged and accepted by Clay; 8 in parallel; 9 fourteen days after 5. Admin-only list: create the ruleset or branch protection on `master`; add `integration`; require code-owner review; set the approvals count; dismiss stale approvals; block force push and deletion; set the bypass list; make any CI check required (including `.github/workflows/boundary-guard.yml`). Organisation rulesets could not be read (token lacks `admin:org`): UNVERIFIED.


Lightest version that would have prevented the incident: ranks 1, 3, 4, 5, 6, 7, 9 limited to `docs/designs/`, `WORKER-CONTRACT.md` and the CODEOWNERS file, about 120-150 minutes of session, maintainer and chat time plus 15-30 minutes of admin time (arithmetic over the estimates). Words alone would not have prevented it: PR 681's body said "the owner reviews and merges" and its author merged it about 90 minutes after opening. The claim is "probably, UNVERIFIED" until the throwaway test passes.

## 10. Owner actions

De-duplicated from `<W>/DECISIONS.md` ("Actions only the owner can take") and merged design section 7 (OA-1 to OA-34; OD-n are D15's open questions, folded in). "Chat" means the owner says it in chat and an agent records it; the owner writes no file. Until the owner answers, nothing that depends on the answer is switched on; silence is never a yes. The other answers and what each does are in merged design section 7. Numbers: PRs 686, 690 (Clay's open PRs), PR 693 (owner's), issues 450 and 655, issue 687 (Clay's cleanup request), Coder issues 515, 516, 477 (cron at boot; `Coordinator` worktree and session; listener), issue 442 (live guard observations).

### 10.1 Admin settings (only `ironbelly`)

| Action | Needed by | Recommended |
|---|---|---|
| Make any CI check required; check organisation-level rulesets (token cannot read them) | D06, D16 | only on a recorded condition; check and say |

### 10.2 Security and host housekeeping

| Action | Needed by | Note |
|---|---|---|
| Rotate the local Orca runtime auth token a debate agent printed into its own transcript (field `authToken` of `/home/coder/.config/orca/orca-runtime.json`) | D02 | the value is in no file under `<W>`, `.dev/tasks` or `.dev/analyze` (checked by the coordinating session); not rotated |
| Per-host diff of installed guard and contract before any `superclaude install`; no blanket install until OA-21 | D03, D14 | FR-66 |
| Land Coder 515 and 516 before the dispatcher serves any repo; correct the "not a fit for a plain command" wording in 515; post the drafted narrowing of Coder 477; optionally retitle issues 339, 423, 444, 655 | D02, D07, D10, D08 | the dispatcher serves no repo until 516 lands |

### 10.3 Rulings in chat

| Action (OA id) | Needed by | Recommended |
|---|---|---|
| Approval, not assignment, stays the start gate; trigger label (OA-8); answer Clay on issue 450 (OA-22) | D01, D14, D15 | gate stays; label stays; answer Clay |
| Do BOTH gates stay (start approval and plan approval after the claim)? (OA-1) | D03, D14 | both: PR 682 reverted; only start gate: PR 682 stands under three conditions |
| Who adapts PRs 686 and 690 (OA-2); `run-all` or `once` plus `repos.yaml` (OA-3); revert before planb (OA-4) | D14, D02, D07 | Clay in place; `run-all`; revert first |
| Grant rows, `--apply` goes and the cleanup-design approval are given in chat; "narrow d2" did not restore an owner-written row; local `git branch -d` under Q02 (OA-15) | Q01, D13, Q02 | yes |
| Interim ledger home and committer (OA-24); a go per push of `coordinators` (OA-26); branch roles (OA-10) | merged K21, D08 | task-package ledger; go per push; two branches |
| Optional numbers: a go age in hours or "none" (needed only before merge automation is built), another reviewer-hold length than 60 minutes, whether a push notice is wanted and its interval (OA-13, OA-25); close authority (OA-12) | OAG1, QG3 | no clock expiry; 60 minutes; no push notice; per-PR go covers merge and close |
| `plan_depth` (OA-27); hand-back and capacity (OA-14); notice cap (OA-16); observer allowlist fields, cap value, whether `how` may show, and what an "old" sweep file means (OA-17); the sweep file location is settled (OA-9) | QG1, D15, OAG2 | `quick`; re-approve, cap 1; 0 until a number; titles and links only until `report-entry` exists |
| Whether `/sc:issue` may run chain commands at create (rule B2) and who runs brainstorm and design at filing | D12 | until decided, issue 689 items 1, 2, 4, 8 stay unbuilt |
| Who edits PR 686's rework after a sizing count, or Q03's fallback (delete only the write calls and the grant check) | Q03, D09 | count first |

### 10.4 Goes for named actions

Ask Clay to make PRs 686 and 690 Drafts (H0); open the revert PR for PR 682 (after OA-1 and a clean dry run); merge PR 693, then adapted PR 690, then PR 685; commit planb, push it as a draft and land it first; throwaway test PRs (they write to GitHub); one local send into a busy worker (U40) and the live checks U5, U25, U28, U8, U3, U54; switch on one throwaway repo (OA-19); after S17 passes, turn `auto_enable` on once, which also covers creating the trigger label for later repos (OA-28a, OA-28b); posts to issues 450, 655, 687, 689 by their assignees (agents write nothing).

### 10.5 Design approvals

Review and approve the amendment PR for `docs/designs/orchestrator.md` (still marked "approved by the owner (Clay)"); no builder starts PR B or PR E before it merges. Accept or amend each verdict here: they are recommendations, not rulings.

### 10.6 The nine owner-only actions and the default the spec uses until the owner acts

Source: `debates/OA-TRIAGE.md`. The spec never asks again; each default is what the stages assume.

| OA | Only the owner can | Safe default until then |
|---|---|---|
| OA-5 | set the ruleset on `master` and `integration` (admin); recommended: admin bypass for PRs only, `integration` in, sole code owner `@ironbelly` | assume no ruleset: every control "narrows", INV-025 stays open, a person's go is a procedure; a separate agent login (OA-6) plus the ruleset is the only way to make "a worker cannot merge" true |
| OA-6 | name the session kind or a separate agent login that counts as "the owner" for typed answers on the shared login | unnamed: `answer-check` cannot pass; S14 ships but every merge stays typed by hand |
| OA-7 | confirm the wording of `WORKER-CONTRACT.md` lines 57, 70, 245 | line 57 fix prepared as its own commit, shipped only after one confirmation; lines 70 and 245 drafted, not in force; `coordinator_autostart` never true |
| OA-11 | grant any of the three standing writes | empty `grants`; the refusal names the missing entry and the sentence to say; the agent records the owner's words |
| OA-18 | consent per repo to a script-started coordinator and to a typed wake line | `coordinator_autostart` false (`coordinator_absent` reported); typed line refused, file pull and mailbox only (a typed line also needs U25 proof) |
| OA-19 | switch a repo on | every repo off (`enabled: false`, `auto_enable` false); at most one throwaway repo after the shadow run, cap 1, `claim_by: poll` |
| OA-20 | flip `WORKER_BINDING_PROVEN` after the probe; later open level FS | not flipped: no worker on a real issue, probe issues only |
| OA-21 | confirm the eight removal PRs (620, 622, 627, 629, 631, 632, 650, 656) | not confirmed: per-host diff before every install, never a blanket `--force` |
| OA-23 | choose the claim route after the X-001 check (and any Coder 516 change) | poll-launched claims only on a throwaway issue, cap 1, real rollout off; `claim_by` `poll` default, `coordinator` reserved |

## 11. Resolved contradictions

### 11.1 The 26 contradictions of `<W>/DECISIONS.md` ("Where verdicts disagree")

R-1 to R-7 were resolved by D15; X-1 to X-19 were found while writing DECISIONS.md and are resolved by following the verdict named (the later and more specific verdict wins unless it contradicts an owner rule). Numbers: PR 682 (Clay's merged deletion of the plan-approval package), PR 686 (Clay's open watcher rewrite), issue 687 (Clay's cleanup request).

| # | The two sides | Choice | Reason |
|---|---|---|---|
| R-1 | Missing-plan reason: `plan_incomplete` (D01) against `held_incomplete` (D09, code) and `plan_missing` (design line 543) | `held_incomplete`, `held_backlog` (FR-05, FR-20) | they are the code's names (pr-a `audit.py:92-93`); retire the others; recompute the pin |
| R-2 | Plan check in `hold.py` (D01, D09) against `plan_body.py` imported by `hold.py` (D12) | `plan_body.py check` is the one definition; the package keeps a copy with a parity test (FR-54) | D14 agreed; a package must not import an installed skill script (BS K8) |
| R-3 | Settings in `repos.yaml` keys (D04, D06) against per-repo JSON (D07) | per-repo JSON; PR 686's `repos.py` supplies key names only | D07 removes the registry file `repos.py` parses |
| R-4 | Default `grants`: none (D04 item 7) against four standing (D04 action row) | empty; owner grants once in chat | Q01 fail-closed; Clay's parser reads a missing key as empty (pr-a `repos.py:295-299`); SEC-07 |
| R-5 | Closeout needs `issue.close` (D13) against no standing `issue.close` (D04, D06) | the per-PR go covers merge and close | OD-10 (SEC-12) |
| R-6 | Hand-back re-plan voids the approval (D01 item 5) | round 2 passes the start gate again | OD-2 (FR-35) |
| R-7 | Design lists 12 verbs incl. lease and interrupt, no merge verb | build the verbs of FR-26 only | OD-7, OD-8 |
| X-1 | D04 and Q01: four standing grants incl. `issue.hold`; Q03 removes `issue.hold` | three: `issue.assign`, `issue.comment`, `issue.body.append_plan_sections`; default empty | Q03, D15, QG3 |
| X-2 | D13: `git branch -d` "refuses an unmerged branch"; Q02 measured it deleted a pushed unmerged branch and merged `integration` and `master` | Q02: `-d` is a backstop; the nine rules are the gate | measurement beats assertion (FR-39) |
| X-3 | D14 assumed `-d` open and the label writer left out, before Q01-Q03 existed | Q02 and Q03 | later, narrower verdicts |
| X-4 | D09 left open whether dormant label code ships in PR 686 | Q03: read-only variant now | Q03 decides that point (FR-06) |
| X-5 | D15 OD-5: entry lines until the whole nine-row list is ruled; QG2 OD-5: entry lines plus a reserved push notice for AU4a, AU4c, AU5 not waiting on the other eight rows (UNVERIFIED) | QG2 | later and narrower (FR-49) |
| X-6 | D03: PR 682 stands only if D01 ends "assignment is the only trigger"; D14: it also stands if the owner says only the start gate stays | D14: the revert needs "BOTH gates stay" | D01 calls start approval and post-claim plan approval different gates and does not decide PR 682 (FR-72) |
| X-7 | D10 typed line `/sc:orchestrator --wake <id>` and tag `orchestrator-<short>-<n>` against D08 | D08, before PR 686 merges | D10 itself defers the names to D08 (FR-63) |
| X-8 | D02 and D14 leave the poll command open; D07 chose one dispatcher over `orca repo list` | D07; the owner confirms (OA-3) | topology settled, command contract owner's (FR-11) |
| X-9 | D15 assumes info-stream searches fail open; QG4 found no off switch and that one failed search stops the cycle | QG4: switch and warn | pr-a `cycle.py:894-900, 922-935` (FR-09) |
| X-10 | D15's OD-1 row cites D12 item 6; QG1 cites D15 position G-2 | QG1 | minor citation fix |
| X-11 | planb status entries: 223 (D03, inventory), 348 (D14), 225 (analysis) | D14's claim, number marked as moving | the author read 225 on 2026-11-20 (5.2) |
| X-12 | Progress log: planb "FINAL: pass at 03:34Z"; D14, D15: do not resume its "half-finished" ledger | UNVERIFIED; re-check before the revert sequence (5.2) | ledger ends `FINAL: pass`, `ARCHIVE: start`; nobody ran its tests |
| X-13 | D16: the owner is the one authority for CODEOWNERS edits; Clay's design (lines 288, 593): Clay | D16, design amended in a new PR | Clay's written acceptance first (FR-68, FR-76) |
| X-14 | D06 item 1: a merge go "expires" (number an owner decision); Q01 item 5: it ends only on the action, a head move or a revoke | OAG1: Q01 is the default, no clock in the first build; D06's number stays the owner's open option; merge automation needs an age check before it is built | the head pin, the second gate run and WC:241 already cover a stale go; no source gives a number (SEC-01) |
| X-15 | The OA topic text says Clay's ADD4 holds a PR with "no stated wait"; ADD4 states 60 minutes after the head's checks finish | OAG1: ADD4 as written, 60 minutes, owner-settable, UNVERIFIED | the design text states the wait (SEC-04) |
| X-16 | Merged K9: a waiting go counts toward `max_in_flight`; QG1 OD-13: a hand-back waiting for re-approval does not | OAG1: both stand | a waiting merge go has a worker finished and a PR open, so it counts and never expires; a `waiting_reapproval` hand-back has neither, so it does not count and may expire on an owner-set limit (FR-35, SEC-21) |
| X-17 | D11 says "one data source"; OAG2 finds the observer's questions panel reads Orca directly | OAG2: "one source for session facts (the sweep); the questions panel is the one exception" | the unqualified sentence is false (FR-81) |
| X-18 | D09 rule 2 and D15 A3: per-repo init creates both labels; OAG3: planb creates only the trigger label | OAG3: init creates only the trigger label, only after the owner turns `auto_enable` on (read-only `would_create` before); `hold:backlog` stays by hand | matches planb code and the owner's chat-OK rule (FR-82) |
| X-19 | OA-TRIAGE: OA-1 (both gates stay, PR 682 reverted) is SETTLED; D01 does not decide PR 682, D14 makes the revert depend on the owner saying in chat that BOTH gates stay | D14: the owner's chat answer is still needed | an owner rule (approvals in chat) outranks a triage label; the spec writes to "both gates stay" as its plan and does not open the revert PR without that answer (FR-72, OA-1) |

### 11.2 Further contradictions between verdicts found by the author (not in DECISIONS.md)

| # | The two sides | Choice | Reason |
|---|---|---|---|
| E-1 | D05 binds a coordinator-started worker provisionally at level FS (may push a feature branch and open a PR); D06 and D04: a worker never pushes except on a person's go and no governed level is open before the owner decides | Bind at W, release to WA after the recorded plan approval (route A); F if the session id cannot be learned; FS only if the owner opens it (OA-20) | D05 calls FS "provisional" and leaves when binding starts to the owner; WC:245 and D06 item 5 forbid a worker push without the go; the owner's G2 design is route A. D05's binding steps stand (FR-30, FR-31) |
| E-2 | D10 item 8: the poll starts a coordinator session when none is live; D06 item 6: a script may start it only at depth 0 under a recorded owner authorization | D06: autostart off by default, `coordinator_absent`, unreadable table starts nothing | D06 is the stricter authority rule; D10's start is transport (FR-27) |

### 11.3 Brainstorm statements that contradict a verdict (the verdict wins)

| Brainstorm says | Verdict says | Spec follows |
|---|---|---|
| Merged K9: `max_in_flight` default 1 | D07 item 3: key default 3; item 8: hold the cap at 1 until claim agents have their own worktree | key default 3, first build enforces 1 (FR-33) |
| Merged K16: refuse any worker start outside `probe_issues` while binding is unproven | D05 item 3: real issues "unbound-and-flagged" (but item 1: not exempted; D04 item 8: no second issue on the unguarded route before the owner rules) | refuse by default; an unbound real issue runs only if the owner says so in chat (OA-20) (FR-30) |
| Merged K2: bind at W then WA | D05: provisionally FS | E-1 above |

## 12. Risks, unverified items and open points

### 12.1 Risk register (condensed; full 35 rows: merged design section 8.2)

Every mitigation narrows a risk. Numbers: PR 682 (Clay's merged deletion of the plan-approval package), PR 686 (Clay's open watcher rewrite), PR 690 (Clay's `/sc:issue --plan` PR), PR 693 (owner's claim-launch-result PR), Coder issues 515 and 516 (cron at boot; `Coordinator` worktree and session).

| id | Risk | Sev. | Mitigation | Proving check |
|---|---|---|---|---|
| RK-1 | A `worker-start` worker cannot be bound; never observed | High | `WORKER_BINDING_PROVEN` false refuses real issues (FR-30) | S17 binding probe |
| RK-2 | A bound worker's own script pushes a feature branch, opens a PR, comments or merges; `master` unprotected (guard reads command text only: master `hooks/scripts/launch-level-guard.sh:771-772`; L2 refuses only `main`, `master`) | High, carried not solved (INV-025) | ruleset (FR-75) stops pushes to those branches and, if the worker's login cannot bypass it, merges into them; a go is a procedure, not a block; audit detects afterwards; a separate agent login (OA-6) plus the ruleset is the only way to make "a worker cannot merge" true | S17 records that a worker script pushing a feature branch is NOT stopped |
| RK-3 | `answer-check` cannot tell a person from a script on the shared login | High | OA-6 names the session kind; head-sha and key binding; two gate runs | refusal test; no test proves identity |
| RK-4 | Planb does not rebase cleanly on the post-revert master; its run state is unclear | High | dry run (S6); re-check (5.2); old ledger not resumed | S9 trial rebase |
| RK-5 | No cron in the image, no `Coordinator` worktree (until 516 the dispatcher returns `worktree_invalid` for every repo) | High | no cron before S17 | fresh workspace: one cron line, one daemon, `run-all --dry-run` lists every repo |
| RK-6 | Wrong merge order of the revert and PR 686 breaks `superclaude --help` (29 test modules) | High | S7 before S11; H0; MC-1 to MC-3 | MC-1 to MC-3 |
| RK-7 | Claim agent and standing coordinator share the `Coordinator` worktree (X-001) | High | real rollout off; cap 1; OA-23 | S17 X-001 record |
| RK-8 | The coordinator weakens its own controls by editing config | High | SEC-10 two layers | `test_config_weakening_refused` |
| RK-9 | A crash between ack and state loses the issue; an abandoned wake is never woken (pr-a `cycle.py:777-810, 994`) | High | M1, M2 | MC-6; kill-and-restart tests |
| RK-10 | Closeout or a `Fixes` line closes unfinished work; the report loses sessions when a worktree is missing | Medium | close only under the go; old session map kept until a live side-by-side run | SEC-12, FR-45 tests |
| RK-11 | The ruleset does not block a non-owner author at 0 required approvals (UNVERIFIED); `Approved` field or Status allow-list missing in a Project skips every issue silently | High for D16's claim | throwaway test with fallbacks (FR-77); `status --json` shows the reason per repo | three recorded PR states; fixture test |
| RK-12 | Merge state changes between the two gate runs; uncertain merge result | High | head-pinned argv; reconcile the exact head; no reused go | T13 |

HIGH findings left open by the standard-depth debates (no third round) are carried as conditions: D05's seven and D06's seven as RK-1, RK-2, SEC-01 to SEC-04, SEC-08, SEC-09, SEC-13, SEC-18; D15's C-INV-1 to C-INV-4 as FR-33, FR-35, SEC-10, SEC-12; D14's four as MC-1 to MC-6 and FR-72; D01 MR-1, MR-2 as FR-02, FR-03; D10 M1, M2 as FR-15, FR-16; D16's four as FR-75 to FR-77. The merged design's 27 invariant findings are mapped in merged 8.3.

### 12.2 UNVERIFIED items a requirement leans on, and the check that settles each

| Item | Leaned on by | Check |
|---|---|---|
| `worker-start` delivers the task as a first prompt that fires the guard's hook with the marker intact; new session id on `/clear`; how the coordinator learns the worker's session id | FR-30, FR-31 | S17 binding probe |
| Claim terminal lifetime; complete live-agent list; worker worktree path | FR-70, FR-33 | S17 X-001 record at four points |
| U5 mailbox from outside a Run; U25 ccsession tag and `orca agent launch`; `tui-idle` | FR-14, FR-17, FR-62 | send, idle and busy capture, tag spike |
| U3 depth-0 start; U28 effective model; U30 effort levels; U8 info-stream replies; U54 false refusals over the last 50 titles | FR-27, FR-09, FR-37, FR-59 | live capture before enable |
| Planb's tests pass; run finished or half-finished | 5.2, S9, X-12 | re-check; owner's chat statement |
| Revert tree passes the full suite incl. `tests/hooks/test_launch_level_guard.py`; trial of PR 690 on master plus PR 693; verb exposing `brief.build` | FR-72, FR-53, FR-31 | S6 dry run; S2 trial |
| `orca worktree rm` without `--force`: effect on the branch and a dirty worktree | FR-39 | remove a throwaway worktree |
| Code-owner review at 0 approvals blocks a non-owner author; a maintainer can convert to Draft; organisation rulesets | FR-71, FR-75, FR-77 | throwaway test; admin-token read |
| `merge-gate`, `answer-check`, `E-NO-GRANT` exist nowhere (searched `src/` of three exports) | SEC-01 to SEC-09 | `grep -rn` on the live repository before S14 |
| A go can be told from script-typed text on the shared login; a separate agent login | SEC-08, SEC-09, RK-3 | OA-6; Coder check |
| 60-minute hold, go expiry, 60-second timeout, `HANDBACK_MAX` 3, 64 KiB with long names | FR-13, FR-30, FR-35, SEC-01, SEC-04 | owner values; 139-character wake test |
| PR 693's result file path and shape; ledger file name; store backup name; verb spelling | FR-60, SEC-14, FR-22, FR-26 | read PR 693; OA-24; fixed when built |
| "Simple feature" in claim rule C1 has no measurable test; anyone reads `hold:plan`; per-repo `status --json` calls fit the observer's 15-second refresh | FR-55, FR-06, FR-44 | define in S3; show a reader first; measure |

### 12.3 Open weaknesses the later debates left

- The sweep lists Orca session row ids only (`src/superclaude/cli/sweep/models.py:265-266`, `classify.py:994-999`), so a PR waiting for a go has no age or go entry on any built surface; the age needs the `report-entry` writer (S15c) and the display (FR-79, SEC-21). Until then INV-023 is narrowed, not closed (OAG1).
- A long-open coordinator session is not made to re-confirm a go typed in the same conversation (WC:241 does not require it); the guards are the head pin, the second gate run and the owner's revoke. Residual risk, untested (OAG1).
- The 90-second sweep figure is a cap, not a measured time; `how` entry-field content, a retention rule for `.dev/sweeps/` and the multi-root reading are unknown (OAG2). The S17 pass list, the `would_create` label step and a report of self-enabled repos are proposals, not built; the trigger label can exist for a repo that stays off (OAG3).

### 12.4 Requirements without a verdict source

`NEW (author)`: no FR, NFR or SEC row carries that tag; each traces to a verdict, the merged design or the project's `CLAUDE.md`. Acceptance tests marked NEW are the author's proposals. Rows resting on the merged design alone (tag `BS`; the owner should confirm them when ruling): FR-03, FR-10 to FR-12, FR-19, FR-21 to FR-23, NFR-01 to NFR-04, FR-27, FR-29 to FR-35, FR-44, FR-54, FR-67, FR-70, SEC-13, SEC-14, SEC-17.

## 13. Acceptance and test plan

Each stage is shown to work by the "deliverables and tests" column of section 8.2, with MC-1 to MC-12 as the common gate. A test marked NEW is an acceptance requirement, not a passing test; none was run by this spec's author. Paths are under `tests/` of the snapshot named. Numbers: PR 686 (Clay's open watcher rewrite, pr-a), PR 690 (Clay's `/sc:issue --plan` PR), PR 682 (Clay's merged deletion), issue 442 (live guard observations), Coder issues 515, 516 (cron at boot; `Coordinator` worktree and session).

### 13.1 Existing tests that must stay green

Under `tests/` of the snapshot named: master `issue_watch/test_security_invariants.py:652, 683, 936`, `test_launch.py:75`, `test_marker_contract.py:28-48`, `test_origin_parity.py`, `test_audit.py` (reasons pin rewritten, MC-10), `test_cycle.py`; `hooks/test_launch_level_guard.py`, `test_launch_level_guard_worker.py` (G2 rule 1 tamper tests return with the revert), `test_launch_level_observations.py:79-84` (twelve skipped observations; un-skipped only by the owner); `skills/test_worker_contract.py` and `core/test_orca_session_launch_guidance.py:33, 53` (edited with SEC-15, FR-65); `skills/test_issue_protocol.py:131-135, 462, 745-784` (moved with claim rule C1); `skills/test_issue_orca_worktree.py`, `test_primitive_dual_surface_lookup.py`, `test_agent_work_report.py`, `cli/test_how_we_work_install.py`, `cli/test_issue_body_templates.py`, `commands/test_sweep_command.py`, `sweep/`, `observe/` (sweep golden test edited by a person, FR-41); planb `issue_watch/test_dispatch.py`; pr-a `test_hold.py`, `test_wake.py`, `test_repos.py`, `test_route.py` (adapted per FR-06, FR-13 to FR-22); the restored `issue_pipeline/` tests (about 117 functions, present at `01e7a9e23^`, back with S7). Tests to write are named in sections 4 and 8.

### 13.2 Live firing tests the verdicts require (before the poll is enabled)

Nothing below has run. Each needs the owner's go when it writes to GitHub or types into a session.

| Test | Procedure | Pass criterion | Source |
|---|---|---|---|
| Precheck test | Only if an automation is wanted: the owner creates `orchestrator-poll --disabled` whose precheck always returns 1 (tested code), prompt "do nothing and stop"; enable after a scheduled (not Run now) shadow run; watch 1-24 hours | fires on schedule, only `skipped_precheck` rows, no session, still listed after an Orca restart; a boot script creates exactly one automation after two boots | D02 |
| Cron shadow run | the cron line runs `run-all --dry-run` for 24 hours under cron's environment | no agent, no config generated, no GitHub write; real replies captured to replace assumed fixtures. S17 pass list (proposal): six `first_run` checks green, this run clean, X-001 run, owner's go; then `auto_enable` on once | D02, D09; BS |
| Guard probe (issue 442's twelve observations; D05 staging probe) | throwaway issue and repo: receipt; one `send` and one `ask` without `--to` reach the coordinator; implement refused at W before release, allowed at WA after `release-worker`; `git commit`, bare `git push`, compound `git add && git commit` refused; scripted `git push origin master` refused (by GitHub only with the ruleset); a worker script pushing a feature branch recorded as NOT stopped (INV-025); a full `/sc:pr-submit --monitor 3` cycle only if level FS is ever opened | each refusal recorded; observations un-skipped by the owner | D05, D04; BS |
| Worker binding | `worker-start` first prompt carries `[sc-launch:v1:<nonce>]`; `pending/<nonce>` consumed in time; session id learned (else F fallback recorded); marker-less fake triggers the stop; kill and resume after `worker_done`; pre-commit behaviour of the coordinator's commit | all observed; `WORKER_BINDING_PROVEN` flipped only by a reviewed commit | D05; BS |
| Transport gate | U5 mailbox from outside a Run; `tui-idle` meaning; `orca agent launch` with the ccsession tag and first prompt; screen-tail check | each result recorded; failure leaves the file pull as the only channel | D10 |
| Claim isolation (X-001) | claim terminal lifetime, live-agent list, worker worktree path at four points | owner picks OA-23 from the record | BS |
| Depth-0 and model checks | U3 depth-0 start; U28 model and U30 effort in `launch.effective`; U8 three read-only info searches; U54 false refusals over the last 50 titles | values recorded; U54 decides scope B or C | D06, D15, QG2, QG4 |
| Merge-path rehearsal | throwaway repo: gate output, typed go, merge with `--match-head-commit`, head changed between gate runs, uncertain result reconciled | T13 reproduced live; no merge without a go | D06 |
| Ruleset throwaway test | FR-77 | BLOCKED and REVIEW_REQUIRED for a non-owner; bypass shown for the owner | D16 |
| Cron and worktree in the image | after two restarts: one `crontab -l` line, one daemon (Coder 515); `Coordinator` worktree exists (Coder 516); MC-12 under real cron | as stated | D02, D07 |

The S17 go/no-go record names the code head, host, installed primitive hashes, fixture captures and the failed as well as passed probes, and is kept by an agent from the owner's chat go.

## Appendix A. Traceability

Requirement to verdict to source file. Verdict files are `<W>/debates/<ID>/VERDICT.md` (QG1-QG4 carry OD-1 to OD-13); "merged" is the merged brainstorm design by section id; code files are in the snapshots named in the header.

| Requirements | Verdict(s) | Source file(s) |
|---|---|---|
| FR-01 to FR-04 | D01 | `debates/D01`; master `cli/issue_watch/cycle.py:228, 979`, `predicates.py:14` |
| FR-05 to FR-08 | D09, Q03, D15 A1, A3 | `debates/D09`, `debates/Q03`; pr-a `hold.py`, `github.py:267-320, 983-1069`, `cycle.py:1021-1119, 1293-1300` |
| FR-09 | QG4 | `debates/QG4`; pr-a `cycle.py:894-900, 922-935` |
| FR-10, FR-11, FR-69 | D02, D07, D14 | `debates/D02`, `debates/D07`; planb `cli.py:432`, `dispatch.py`; `docs/designs/issue-watcher-setup.md` |
| FR-12, FR-33, FR-34, FR-67, FR-70 | D07, D15 C1-C4, QG1 | `debates/D07`, `debates/QG1`; merged 3 K4, K9, K22, X-001 |
| FR-13 to FR-19 | D10, D15 B3-B9, D08 | `debates/D10`; pr-a `wake.py:46-47, 69, 269-299, 545-581` |
| FR-20 | D15 E6, R-1 | pr-a `audit.py:39, 92-93`, `tests/issue_watch/test_audit.py:86-98` |
| FR-21 to FR-23, FR-82, NFR-01 to NFR-04 | merged (BS), D03, D14, D02, OAG3 | merged 2.1, 2.5, 4, K1, K24, INV-001 to INV-027; `debates/OAG3`; planb `launch.py:48`, `repo_init.py`, `first_run.py` |
| FR-24, FR-25, FR-62 to FR-65 | D08, D15 G2, G3 | `debates/D08` |
| FR-26, FR-36, FR-40, SEC-11 | D15 D8, D15, D14; QG3, QG4 | `debates/D15`, `debates/QG3`, `debates/QG4` |
| FR-27, FR-28, FR-29 | D06, D10, D07 | `debates/D06`, `debates/D10`; merged K11 |
| FR-30, FR-31, SEC-13, SEC-20 | D05, D03, D04, D14 | `debates/D05`; master `hooks/scripts/launch-level-guard.sh:265-272, 785-790`, `skills/sc-issue-protocol/scripts/orca_worktree.py:822, 1515`; merged K2, K3, K16 |
| FR-32 | D06 | master `core/WORKER-CONTRACT.md:244-246`; merged K2 |
| FR-35 | QG1, D15 D18, D01 | `debates/QG1`; merged K15 |
| FR-37, FR-47, FR-49 | QG2, D11, D15 D16, D17 | `debates/QG2`, `debates/D11` |
| FR-38, FR-39, SEC-19 | D13, Q02, Q01 | `debates/D13`, `debates/Q02` |
| FR-41 to FR-46, FR-48, FR-50, FR-79 to FR-81 | D11, D15 E1-E7, OAG2 | `debates/D11`, `debates/OAG2`; master `cli/sweep/report.py:621-661`, `commands.py:153-193, 277-278` |
| FR-51, FR-52 | D04 | `debates/D04`; master `launch.py:33` |
| FR-53 to FR-61 | D12, D14, QG1, D15 A7-A10 | `debates/D12`; pr-p `skills/sc-issue-protocol/scripts/plan_body.py:138` |
| SEC-01 to SEC-04, SEC-21 | D06, D15 D1-D3, D04, OAG1, QG1, QG2 | `debates/D06`, `debates/OAG1` |
| SEC-05, SEC-06, SEC-15, SEC-16 | D06, D04, QG3, Q01, D10 | `debates/D06`, `debates/Q01`; master `core/WORKER-CONTRACT.md:23, 57, 70, 244-246` |
| SEC-07 to SEC-10, SEC-12 | Q01, QG3, D15 C-INV-3, C-INV-4 | `debates/Q01`, `debates/QG3` |
| SEC-14, SEC-17, SEC-18 | Q01, D16, D06; merged K21, INV-017 | `debates/Q01`, `debates/D16` |
| FR-66, FR-68, FR-71 to FR-74 | D14, D03, D15 A13, G6 | `debates/D14`, `debates/D03` |
| FR-75 to FR-78 | D16 | `debates/D16` |
| NFR-05, NFR-06 | D10, D15; project `CLAUDE.md` | `debates/D10`; `/home/coder/workspaces/IronClaude/CLAUDE.md` |
| Sections 5-13 | D14, D15, D16, DECISIONS.md; merged 5, 7, 8 | `debates/D14`, `debates/D15`, `debates/D16`, `<W>/DECISIONS.md`, `<W>/inventory/clay-prs.md`, both technical references |
