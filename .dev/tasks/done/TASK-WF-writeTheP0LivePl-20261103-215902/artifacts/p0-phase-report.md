# P0 phase report: Orca worker contract

Plan: `./TASK-WF-writeTheP0LivePl-20261103-215902.md` (live plan, version 2). Spec: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (pass rule at line 238: the phase passes only when both plans' checks pass). Checkout: branch `ironbelly/OrcaCLICommandRefactor-Specs`, HEAD `8db29f1165508187b7a14a48f2f66793e269d596` (unchanged by this plan, `./artifacts/head-final.txt`). Run date: 2026-11-04. Orca runtime 1.4.237, run id `run_0f9350decd8c`. Every evidence file below is under `./artifacts/` of this package unless a full path is given.

## P0 verdict

**P0 verdict: PASS.** Every static check (11 of 11) and every live check (AC-0.4 three checks, AC-0.5, AC-0.6) passes. No AC-0.4 check failed, so spec section 1 is not reopened. The notes in "Notes for the coordinator and owner" below do not change a verdict, but items 1 and 2 there bear on spec section 7.2 step 5 and should be read before P1.

## Static part (from the passed static report)

Source: `.dev/tasks/done/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/p0-static-report.md` (not re-run, evidence not copied).

| Check ID | Verdict recorded there |
|---|---|
| AC-0.1 | PASS |
| AC-0.2 | PASS |
| AC-0.3 | PASS |
| AC-0.7 | PASS |
| AC-0.9 | PASS |
| AC-C1 | PASS |
| AC-C2 | PASS |
| AC-C3 | PASS |
| AC-C4 | PASS |
| AC-C5 | PASS |
| AC-C6 | PASS |

Carried forward from its AC-0.7 finding: `task-create`, `worktree create --agent` and `agent launch` are covered only by WC-13 and section 7.2 step 5; they are not checked in Orca's installed code. In the three live checks, step 5 searched every Bash command of every worker session (top-level and subagents) for those calls and `worker-start` / `dispatch`: no match in any of the three runs (`lc1-step5.md`, `lc2-step5.md`, `lc3-step5.md`, condition 5).

## Live part

| Check | Verdict | Evidence |
|---|---|---|
| AC-0.4, check 1: `/sc:troubleshoot` (steps 1 to 7 and Remove) | PASS | `./artifacts/lc1-result.md` |
| AC-0.4, check 2: `/sc:workflow` (steps 1 to 7 and Remove) | PASS | `./artifacts/lc2-result.md` |
| AC-0.4, check 3: `/sc:adversarial` (steps 1 to 7 and Remove) | PASS | `./artifacts/lc3-result.md` |
| AC-0.5: `worker-start` exit 0, `state: ready`, under 45 s | PASS: 41.995 s | `./artifacts/ac-0.5.md` |
| AC-0.6: do tool calls appear by name in `worker-read --source transcript`? | yes (`Agent`, `Bash`, `Read`, `Write` appear by name in `tool-call` blocks) | `./artifacts/ac-0.6.md` |

Each check's AC-0.4 outcome rule (`--outcome` from the report file's status) matched what the worker sent: check 1 report status `partial` gives succeeded; check 2 contract status `success` gives succeeded; check 3 merge-log `Status: success` gives succeeded. The other two worker starts (not part of AC-0.5, which names one start) took 39.924 s (`lc2-step1.txt`) and 39.920 s (`lc3-step1.txt`). All three are under 45 s with a margin of 3.0, 5.1 and 5.1 s.

### Heartbeat length (spec line 291)

All three checked runs lasted longer than the 5-minute heartbeat cadence the workers' preambles state, so the heartbeat part of step 5 was not passed vacuously:

- check 1 (troubleshoot): 45 min 38 s, 15 heartbeats, `lc1-step5.md`;
- check 2 (workflow): 86 min 55 s, 17 heartbeats, `lc2-step5.md` (the longest run);
- check 3 (adversarial): 31 min 40 s, 7 heartbeats, `lc3-step5.md`.

Raw gaps between heartbeats exceeded 5 minutes in all three runs (up to 7.5, 14.5 and 7.7 min), always while the command's own subagents were running in the background. With subagent time removed, the longest stretch without a heartbeat was 2.2, 2.0 and 3.3 min. Condition 4 was therefore recorded PASS on the reading of `WORKER-CONTRACT.md:44` that a subagent fan-out gap is accepted. See note 2 below.

### Branches that remain after removal

None. `lc1-branch-after.txt`, `lc2-branch-after.txt` and `lc3-branch-after.txt` are all empty: `orca worktree rm --force` deleted each disposable local branch (`ironbelly/p0-live-troubleshoot`, `ironbelly/p0-live-workflow`, `ironbelly/p0-live-adversarial`) itself. The three worktrees are gone from disk and from `orca worktree list`, and the feature worktree's HEAD is unchanged after each (`lc<N>-head-after.txt`).

### Workers or worktrees left for the person

None. All three workers were released (`lc<N>-step7.txt`: state `released`, no reclaimable rows) and all three worktrees removed.

### Staging found inside a disposable worktree (known P0 gap, WC-9)

None. The index of each disposable worktree was empty after its run (`lc1-index-after.txt`, `lc2-index-after.txt`, `lc3-index-after.txt`). The workflow command's protocol says it stages `.dev/tasks` (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:28`), but the worker did not: its `worker_done` body says "I ran no git add" (`lc2-step3.json`).

## Notes for the coordinator and owner

1. **`worker-read` cannot return a whole transcript of a long run.** In all three checks `worker-read --source transcript` returned only the last 40 to 50 messages with `"contentComplete": false` (clipping `message_limit_or_scan_window`), and the returned cursor never ended (it points at the end of the worker's session file; pages after the first were empty). Spec section 7.2 step 5 says to read the whole transcript and follow `--cursor` until no next cursor remains; that is not possible with this Orca version. I checked the five step-5 conditions on each worker's own Claude Code session file instead (read-only; the same file worker-read reads; analysis in `lc<N>-session-analysis.txt`). All five conditions held in all three runs. The step-5 procedure in spec section 7.2 needs a decision before P1: either accept the session file as the source, or keep `worker-read` and accept it covers only the end of a run.
2. **Heartbeat gaps.** The long raw gaps are covered only by the WC-10 reading that a command's subagent fan-out can hold the session longer than the cadence. Because the subagent Agent calls return at once ("Async agent launched successfully"), the literal wording in the plan, "inside an Agent-tool call", does not cover them. In check 3 there was also a 14-second overrun of the plain wall-clock 5 minutes while the worker was editing with no subagent running (`lc3-step5.md`, note on condition 4). If the owner wants the stricter reading, checks 1 to 3 would each be marked FAIL on condition 4 and the P0 verdict would become FAIL.
3. **Extra read attempts.** To look for more transcript, in check 1 I made one `worker-read --limit 1000` read (`--limit` is in the verb's `--help`, not in the plan) and one read after the worker was released; neither returned more (`lc1-transcript-limit1000.json`, `lc1-transcript-after-release.json`).
4. **Sub-statuses are not the check status.** Check 1's report status is `partial` (evidence validator dropped one citation; root cause found). Check 2's contract status is `success`, but its own advisory reflect step returned `plan-needs-revision`. Check 3's merge-log status is `success`, but the skill's own return contract says `partial` (73% agreement against an 80% threshold). Per the plan, only the status in the file named by AC-0.4 counts.
5. **Staging not done by this run.** During this run a `git add .dev/tasks` that this run did not issue (most likely another session in the same checkout) staged the superseded package `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/` and an unrelated new package `.dev/tasks/to-do/TASK-WF-refactorDocsDeve-20261104-062532/`. This run un-staged the superseded package as the plan requires (see `staged.txt`). The unrelated package is staged under `.dev/tasks/`, which is the always-staged location; it is not part of this plan.
6. **Left untouched.** `.dev/brainstorms/`, `.dev/review-loop-convergence/`, `.dev/reflect/` and the superseded package's content were not edited. No commit, push, install or `gh` write was made.
7. **Bare `python3` calls (rule breach, no effect).** The plan constraint is "UV for every Python command" (plan line 23). Three groups of calls broke it, on 2026-11-04. (a) At 08:27:10 UTC, during Task 3, the executor itself ran one bare `python3 - <<'EOF' ... || true` command with an empty body; it ran no code and wrote nothing. Apart from this call, every other Python call the executor itself made used `uv run`. (b) Between 09:10:02 and 09:16:29 UTC the first final-review helper subagent ran 22 read-only analysis commands that used bare `python3`; they only read files and wrote scratch scripts under `/tmp`. (c) At 12:35:19 UTC the third final-review helper subagent ran one `python3 -c 1`, which does nothing. The owner accepted all three groups (24 calls) as one scoped exception, recorded in the last `ARCHIVE: Ruling:` line of `progress.md`, which replaces the narrower earlier ruling line. It changes no verdict above.

## Post-archive check (the coordinator runs this after the executor archives the package)

After `/sc:implement` moves this package to `.dev/tasks/done/` and re-adds `.dev/tasks`, the executor runs `git restore --staged -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`. Then the coordinator runs:

```sh
git diff --cached --name-only
```

It must list nothing under `.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950`.
