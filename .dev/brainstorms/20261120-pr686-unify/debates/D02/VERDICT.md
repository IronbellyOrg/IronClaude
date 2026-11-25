# Verdict D02: Scheduler: cron or Orca automation

## Question

Should the poll run from cron with one dispatcher (OURS R6, R16, Coder issue 515 "cron"), or from an Orca automation named `orchestrator-poll` with a no-agent "precheck" step (CLAY R4, spec 4.8, D:76 and D:343-354)? The owner states Orca automations "start an agent session with a prompt on each run" and that this was debated and rejected. Test CLAY's precheck claim against `waker.py` and the Orca automation docs/CLI help (`orca-ide automations --help`, read-only; do NOT create or run an automation).

## Winner

HYBRID. Cron with one dispatcher stays the scheduler (the owner's line wins the tie), but the owner's written reason for it is wrong in one place and must be corrected, and CLAY's precheck automation is kept as a tested-first fallback.

## Winning recommendation

What the unified spec must say (each line can be checked):

1. **Scheduler of record is cron.** One cron entry every 5 minutes, `*/5 * * * *` (five fields), wrapped in `/usr/bin/flock -n <lock file>`, absolute paths for `superclaude` and the Orca shim (cron has only `PATH=/usr/bin:/bin`), output appended to `~/.aidev/logs/issue-watch.log`. This is the line already written in `docs/designs/issue-watcher-zero-setup-coder-handoff.md:23` (worktree `claim-handoff-planb`). The template (Coder issue 515, the Coder-repo issue that installs cron and starts it at boot) must make the entry exist exactly once after every boot. Test: after two workspace restarts `crontab -l` shows the watcher line once and `pgrep -x cron` finds one daemon.
2. **Say which poll the entry runs.** The scheduler cannot be judged apart from the command. Master and Clay's open rewrite (PR 686, the watcher rewrite) have `issue-watch once` reading `repos.yaml`. `run-all` (one dispatcher over `orca repo list`, R16) exists only in the unpushed branch `ironbelly/issue-watcher-zero-setup-plan` (`cli.py:432`). The spec must name one command and its configuration contract before it names the scheduler (invariant INV-023, blocking; settled together with D07 on topology).
3. **State the real reasons, not the false one.** Replace "an Orca automation starts an agent session on each run" (requirements line 18; Coder 515 body) with: (a) a scheduled automation whose precheck exits non-zero starts no agent, so the old sentence is true only when the precheck exits 0; (b) an automation can still start a Claude session by a "Run now" click or `orca automations run`, which bypass the precheck, and by a dropped `exit 1`; cron has no such path; (c) the automation needs one creation step per Orca host, and nobody has written a boot script for it; (d) one cron entry plus one dispatcher covers all repos with no per-project step (R16).
4. **Fallback, conditional.** If cron cannot be installed in the image in time, an automation may bridge, but only after the decisive test below and only in this shape: created `--disabled`, enabled only after a scheduled (not Run now) shadow run, precheck command fixed so it returns 1 on every path (code with a unit test, not a hand-typed `; exit 1`), prompt text "do nothing and stop", created by the owner (the design's rule N5 keeps the orchestrator from creating, editing, removing or running automations).
5. **The two existing report automations stay as they are.** `coordinator-morning-wake` and `coordinator-missed-check` use the same precheck pattern for a different job (a daily wake at fixed hours). Nothing in this verdict changes them.
6. **Fix the doc line.** The FU-2 cron line in `docs/designs/issue-watcher-setup.md` is six fields (`0 */5 * * * *`); cron 3.0pl1 takes five. Change it to `*/5 * * * *` (not run here: UNVERIFIED by a test).
7. **Do not claim the scheduler settles zero setup.** Even with cron, zero setup still needs Coder issue 515, a one-time `superclaude install --force` per host, the owner-created `Approved` field, and Coder issue 516 (the `Coordinator` worktree). INV-024.

Decisive fact that would reverse the choice: a `*/5 * * * *` automation with a `; exit 1` precheck, created `--disabled` and then enabled on this host, fires on schedule for 1 to 24 hours under the present headless Orca server, shows only `skipped_precheck` rows, starts no session, and is still listed after an Orca server restart. If that holds, and a boot script is shown to create exactly one automation after two boots, the automation becomes the better primary (both advocates then moved to about 65 to 70%).

## Strongest points

OURS (cron):
1. Cron has no scheduler-layer path to a model run; an automation has two (Run now bypass, a dropped `exit 1`). Source: `orca-ide automations create --help` ("Run now ... intentionally bypass the precheck"; `--prompt` and `--provider` required); design 4.8 `docs/designs/orchestrator.md:348-349`. The harm is bounded (one idle session per click), so the margin is small.
2. The cron mechanism was tested in cron's empty environment: a per-minute entry fired on time, `orca repo list` and `gh auth status` worked under `PATH=/usr/bin:/bin`. Source: requirements R21 (`requirements.md:49`) and the handoff doc line 28. Limit: the install path was not tested.
3. An automation is not yet working anywhere on this host and needs an owner step: `orca-ide automations list` returns "No automations found"; creation is owner-run (O3, O4, `orchestrator.md:1025`) and a boot script does not exist. One cron entry plus one dispatcher matches R16 (one entry for all repos).

CLAY (automation):
1. The owner's stated blocker is false for the precheck pattern. Source: CLI help ("any other exit, error, or timeout skips the run"), master `src/superclaude/skills/agent-work-report/SKILL.md:30` ("exits non-zero so Orca starts no agent and leaves no terminal (VERIFIED 2026-11-03)"), `waker.py:1-2`. OURS conceded this in its own Risk section.
2. Cron is not in the image today: it was installed by hand on 2026-11-18, the daemon was started by hand (pid 1169996, started Wed Nov 18 20:20:37 2026, which I confirmed with `ps`), and Coder issue 515 is still open. The automation needs no image change. Source: debate Round 2 (apt history and `crontab -l` read by the advocate), Coder 515 (read with `gh`).
3. The automation probably survives image updates and has a built-in catch-up window (default 720 minutes) and a history cap of 100 rows. Source: advocate's reading of the installed Orca code and `~/.config/orca` file dates (Round 2); an inference, not a run.

## Clay strengths to adopt

- **Correct the premise (DOC).** What: the written reason in requirements line 18 and the Coder 515 body. Why: verified defect in OURS's rationale (CLI help and master `SKILL.md:30` contradict it), and the fault-finder (INV-028) notes the next reader will reopen D02 on a false premise. How: restate as in recommendation point 3; keep cron.
- **Precheck automation as a conditional fallback.** What: a scheduler path that needs no image change. Why: a capability OURS lacks today (a scheduler that can run on this host before Coder 515 lands), already shipped as a pattern on master. How: only after the decisive test, in the shape of recommendation point 4; it does not replace the cron decision.
- **Two safety mitigations (suggestions from the Variant 2 advocate, not in master).** What: a fixed command that always returns 1, and a "do nothing and stop" prompt. Why: they remove the dropped-`exit 1` mistake and make a stray click cheap. How: adopt only if any automation is used.
- **Write the comparison per command.** What: name `once` or `run-all` before the scheduler (A-001, INV-023). Why: the papers compared different commands. How: spec section "Which poll is scheduled".

## Our strengths that must be kept

- One cron entry and one dispatcher for all repos (R16), absolute paths, `flock -n`, a log under `~/.aidev/logs/`, and the per-repo lock (master `record.py:382`) on top: two lock layers that do not collide (different lock files; checked in debate Round 2).
- The tested empty-environment facts (R21; handoff doc line 28), stated with their limit.
- The rule that no scheduler-layer mistake can start a model run.
- The owner's zero-setup goal as the test for any scheduler (R1, R17).

## Actions

| Action | Type | Target | Order or dependency |
|--------|------|--------|---------------------|
| Restate the scheduler reason (recommendation point 3) in requirements R6 and line 18 | DOC | `.dev/releases/backlog/issue-watcher-zero-setup/requirements.md` (worktree `claim-handoff-planb`) | Before the unified spec is written |
| Correct the wording in Coder issue 515 ("not a fit for a plain command") by a comment or edit by the owner | DECISION | Coder issue 515 (https://github.com/IronbellyOrg/Coder/issues/515), owner only; not done by this debate | After the owner accepts this verdict |
| Change the six-field FU-2 cron line to five fields | DOC | `docs/designs/issue-watcher-setup.md` (section 8.7 and the FU-2 table row) | Any time; independent |
| Replace R4 and section 4.8 ("Orca automation runs the schedule, not cron") and DQ10 in the design with the cron entry and the fallback text | LOCAL CHANGE | `docs/designs/orchestrator.md` lines 76, 343-354, 120 (via a design PR, owner-reviewed) | After the owner accepts this verdict; with D07 (topology) |
| Keep the scheduler-agnostic part of PR 686; make its runbook and the later runbook rewrite (the design's PR E) follow this verdict | PR KEEP-ADAPT | PR 686 (Clay's watcher rewrite) and PR E (not yet opened) | PR 686's code runs the command `once` and does not need a scheduler choice; whether 686 touches cron or automation docs is UNVERIFIED |
| Decide the poll command contract (`once` plus `repos.yaml`, or `run-all` plus per-repo configs) | DECISION | spec section "Which poll is scheduled"; settled with D07 and D01 | Before any scheduler text is final (INV-023) |
| Run the decisive test only if the owner wants an automation as primary or fallback | DECISION | owner-run on a host: create `orchestrator-poll --disabled`, enable, watch 1 to 24 hours | Optional; blocks nothing else |
| Track that zero setup also needs 515, per-host install, the `Approved` field and 516 | DOC | handoff doc and requirements (INV-024) | With the Coder work |
| Rotate the local Orca auth token (`orca-runtime.json`) that a debate subagent printed into its own transcript | DECISION | this host, owner only | Soon; it is a local-socket token, not copied into any debate file |

## Implications

- **Watcher:** the poll runs unchanged under cron; the scheduler is not the blocker for PR 686's code. Project enrolment follows the poll command, not the scheduler: `run-all` auto-enrols a new project, `once` with `repos.yaml` does not (INV-015). A sweep can last up to about 525 seconds (`LOOP_CAP_S = 270`, `CHILD_TIMEOUT_S = 255`, `dispatch.py:52-53`) against a 300-second tick, so lost ticks can be routine; not measured.
- **Coordinator and orchestrator:** nothing in the coordinator duties changes. The design's N5 stays: the orchestrator never creates or runs an automation.
- **Dashboard and observer (D11):** neither scheduler leaves a "no sweep ran in N minutes" signal (INV-008). Add a last-sweep-time field to the data the observer reads, whichever scheduler is chosen. Orca keeps only the last 100 finished automation runs (about 8 hours at 5 minutes), so Orca history is not an audit trail.
- **Claim pipeline:** unchanged by this topic.
- **What breaks:** design lines R4, 4.8, DQ10 and the design's "cron dropped" rows contradict this verdict and must change; Clay's runbook plan (O3, O4: create `orchestrator-poll`) would be replaced.
- **The owner must know:** (1) the sentence "automations start an agent on each run" is true only when the precheck exits 0; (2) "this was debated and rejected" is not backed by the folder `.dev/releases/backlog/issue-watcher-zero-setup/` (only line 18 mentions automations; the debate there is dispatcher against per-project entries); (3) cron is not in the image yet, so the cron choice depends on the Coder repository; (4) both advocates called it a toss-up (about 50% and 55%), so this verdict leans on the owner's recorded decision and on risk direction, not on a clear technical win.

## Confidence

62% that cron-as-primary with the corrected rationale and a conditional fallback is the right unified rule. About 95% that the rationale text must be corrected. What would change it: the decisive test above (an automation firing headless for 1 to 24 hours, only skip rows, surviving a restart, plus a boot script that creates exactly one automation); Coder issue 515 stalling for a long time; or the owner choosing "no image change" as the top priority.

## Unverified

- That a `*/5 * * * *` automation fires, headless, on this host, and survives an Orca server restart. No automation exists here and none was created.
- That Orca's scheduler runs with no window open (read from the installed code by a debate advocate, minified code; I did not re-read it).
- The 100-row history cap, the 720-minute catch-up default, and the `profile-state.db` storage (same source: the advocate's reading of installed code and file dates).
- That an automation survives an image update (inference from file dates).
- That a template boot script can create the automation once and in time (none exists).
- That the waker automations run on Clay's host as the design says (not visible from this host).
- Whether the owner's cron decision came before or after Clay's #450 comment at 2026-11-18 17:00:32 (history file G-history.md cannot fix the order).
- That the six-field cron line fails under cron 3.0pl1 (not run).
- That `apt install cron` on 2026-11-18 18:40:49 and the empty crontab are as the Round 2 advocate read them; I verified only the daemon's start time with `ps`.
- Whether PR 686 or the later runbook PR touches cron or automation text.
- The 525-second sweep figure is arithmetic from two constants, not a measurement.

## Debate artifacts

- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/position-OURS.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/position-CLAY.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/diff-analysis.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/debate-transcript.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/invariant-probe.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/base-selection.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/refactor-plan.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/merge-log.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/return-contract.yaml`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/merged-position-d02.md`
- `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/return-contract.yaml`
- Round files: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D02/adversarial/adversarial/rounds/` (round1-advocate-1.md, round1-advocate-2.md, round2-advocate-1.md, round2-advocate-2.md, qual-pass2.md)
- Adversarial skill ran in full (Skill tool, nested agents available). Process notes: base selection picked Variant 2 (CLAY) by the tiebreaker rule although Variant 1 scored higher raw (0.875 against 0.831); that is a document-level result and this verdict applies the owner's weighting rule on top. Pass 1 of the qualitative scoring was written after the orchestrator saw Pass 2's totals, so the two passes are not fully independent.
