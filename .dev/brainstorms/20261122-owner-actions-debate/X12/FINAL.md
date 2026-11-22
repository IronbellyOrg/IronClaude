# X12 (OA-23) Claim route after the X-001 live check. Final proposal

Terms. X-001: the open question "does the claim agent that the poll starts stay alive in the shared `Coordinator` worktree where the standing coordinator lives". Poll: the watcher cycle that launches the claim. Route P: the poll launches the claim in the shared worktree, one at a time. Route W: each claim gets a worktree of its own, made by the poll. 516: Coder issue 516 (IronbellyOrg/Coder; makes the `Coordinator` branch, worktree and session). Stand-in: a test worktree named `Coordinator` with one agent that plays the coordinator.

## 1 Unified proposal
Run X-001 now, by the real poll path, on a throwaway repo, before 516 is built and before any real repo is touched. All writes below happen only after the owner's go in chat.
1. Owner names a throwaway repo and one throwaway issue in chat. An agent reads the claim skill's write steps and tells the owner what the run writes (an assignment, a ClickUp call that is non-fatal on failure, two comments, all under the shared login `ironbelly`). The issue is titled as a test.
2. Setup: an agent makes a `Coordinator` worktree in the throwaway repo through Orca with `--agent`; its one agent is the stand-in. Config, approvers file and state folder sit in a scratch folder, never in `~/.config/superclaude/issue-watch.d/`, so cron cannot pick it up. The config must set `enabled: true` (checked: `once` stops with `not_enabled` otherwise, `cycle.py` 715-716). A `DISABLED` file is ready. Only one claimable issue exists at a time.
3. Runs, one after another, never two claim agents alive together. Run 1 and run 2: `uv run superclaude issue-watch once --config <file>`. Run 3: a claim that stops or is refused, by hand launch with the poll's own argv; if none can be made without an extra GitHub write, record "not observed" and GREEN carries that limit. If the throwaway repo has no board status of Research, Spec, Plan or Debug, run 1 and 2 use the identical hand launch.
4. Record, read-only, at the plan's four points (RK-7; the plan never names them, so: before the launch, after both claim comments, after the claim result, just before the stand-in writes) and at +15 and +30 minutes: the Orca terminal list for that worktree; every `claude` process whose `/proc/<pid>/cwd` is that worktree; `git status --porcelain` and any `.git/index.lock`; the field names of the launch reply (is there a terminal handle); the worktree path Orca reports against 516's literal path. Read the Orca `--help` pages first. No status, runtime file or token is printed or saved.
5. Rule, fixed before the run; the worst run decides.
- GREEN: every launch accepted; claim terminal and process gone by the last point and still gone at +30; both live-agent sources agree; stand-in listed exactly once; only untracked `.dev/issues/<N>/` files changed. Route P: throwaway issue only, cap 1, no coordinator write or wake during a claim. 516 scope unchanged. Provisional until one claim is repeated on the real 516 worktree in S17.
- RED: a claim alive at a late point; a launch refused; stand-in not listed once; a lock or a changed tracked file. Route W. Real rollout stays off until W is built and passes a one-claim check.
- CANNOT TELL (sources unreadable or disagree): repeat once with the process list as the main source; if still unclear, RED.
6. Coder 516 wording, posted only on the owner's chat go, with Clay told (Clay asked on 2026-11-20 that 516 not start). Any result, comment 1: "Correction: the issue watcher's claim does start a Claude terminal through the poll. The line 'claims with --pipeline none, which starts no agent' is wrong. Nothing else in this issue changes." RED only, comment 2: "Correction to the owner decisions of 2026-11-18: the watcher's claim sessions no longer start in the `Coordinator` worktree; each starts in a worktree of its own. This issue's scope is unchanged: one `Coordinator` branch, worktree and session per project."
7. Route W build (RED only, goes on watcher issue 717): the poll creates one worktree per claim with the claim agent as its one agent, saves the path as the launch directory, and cleans finished claim worktrees without `--force`.

## 2 Context
Decision D07 found that `launch_argv` puts every claim agent in the `Coordinator` worktree (`launch.py` 136-157 on origin/master, read), against "one worktree holds one live agent". FR-70 (`SPEC.md` 327) keeps real rollout off until the X-001 record exists and the owner picks the route. RK-7 (`SPEC.md` 651) is rated High. The plan's safe default is poll claims on a throwaway issue, cap 1. The plan lists the check after 515 and 516 land (`merged-requirements.md` 547); both agents moved it earlier, which I accept because the stand-in needs no 516 and a wording change is cheapest before 516 starts. The D07 verdict (line 67) names separate claim worktrees as a local change "before the cap exceeds 1", so P at cap 1 is inside the plan and W is its named remedy.

## 3 Implications
- Changes: OA-23 is answered from a record. A false line in 516 is corrected under every result.
- Stays blocked: every real repo (OA-19), workers (OA-20), raising the cap, `claim_by: coordinator` (S17 excludes it, `SPEC.md` 503). Real rollout also needs the owner's separate chat go.
- Under RED, issue 717 gains the W item and real rollout waits for it.

## 4 Benefits
One fact replaces a guess. The route follows a rule written before the data. The real coordinator worktree is never the test bed. Under GREEN the built poll stays unchanged and 516 stays small.

## 5 Risks and containment
- Three runs prove only the paths tried: GREEN keeps cap 1, throwaway only, and is provisional until the S17 repeat.
- Probable outcome is RED: an interactive Claude terminal that finished its prompt may sit at the prompt (UNVERIFIED). Owner should expect W.
- Cap 1 is a promise, not code (master has only `MAX_LAUNCHES_PER_CYCLE = 1` and `DAY_CAP = 6`, read): one claimable issue at a time, cron kept away, `DISABLED` file ready.
- GitHub and ClickUp writes appear under the owner's login: test-marked issue, the owner's two chat sentences copied into the record.
- A stand-in is milder than the real coordinator: errs safe, plus the S17 repeat.
- Hand launches skip the poll's own record keeping: say so in the record.
- Posting on 516 touches Clay's hold: only a correction, only on the owner's go, Clay told.

## 6 Costs (estimates, nothing measured)
Check about 3.5 hours of agent time (setup 1, runs and the +30 wait 1.5, record 0.5, S17 repeat 0.5). RED adds about 8 to 12 hours for W (build 4 to 6, tests 2 to 3, clean-up 2 to 3; basis: `launch.py` is about 400 lines with one argv builder and one launcher). Optional close step about 2 to 4 hours (basis: one new call plus a test; a guess). Owner time: two chat sentences, plus the 516 go.

## 7 The sentence the owner says in chat
Before: "Run the X-001 check on <throwaway repo> issue <N>: three runs, one at a time, cap 1, no worker, apply the fixed rule; nothing else changes and no real repo is switched on."
After the record: "OA-23: take the route the record shows."
Separate, if wanted: "Post the 516 correction(s) and tell Clay."

## 8 What an agent does after it
Reads the claim skill's write steps and tells the owner what the run writes; reads `--help` pages; builds the stand-in and the scratch config; runs the three runs and records every point with raw outputs; applies the rule and reports GREEN or RED; asks the owner to confirm the route in chat; records both sentences with dates in `STATE.md` and the X-001 record; on the owner's go drafts and posts the 516 comment(s), tells Clay and adds the W item to 717. The owner writes no file.

## 9 Consensus: full on the plan. One owner choice stays open, and only if it arises
Both sides agree on setup, record points, rule, 516 wording, W as the RED route, costs, and that run 2 does not overlap run 1 and Route S (a shared second worktree) is dropped. The residual is only the optional close step: "the poll closes its own claim terminal after both comments". It is offered only if the record shows the launch reply carries a terminal handle and a close by that exact handle removes only the claim.
- Owner picks W (default, my recommendation): safest, the plan's remedy, 8 to 12 hours, real rollout waits.
- Owner picks the close step: about a quarter of the work, real rollout can follow the S17 repeat, but a claim and the coordinator share the folder for minutes (a known breach of D07 item 8) and a wrong handle could close the coordinator.
Not a default and never GREEN, because `outcome_of` (`launch.py` 372-396, read) keeps only an operation id, no terminal handle.

## 10 Not verified
Orca list and close flags; whether the launch reply carries a terminal handle; whether a finished claim terminal exits by itself; the throwaway repo's name, existence and board status; whether the claim writes to ClickUp for a throwaway repo; whether issue 717 already lists a W item; the "one live agent per worktree" source file (cited only through D07). Verified by me: `launch_argv` and `outcome_of` on origin/master; `once` honors `enabled`; caps in `cycle.py`; 516 body text and the 2026-11-18 decision line; D07 verdict lines 22 and 67; FR-70, RK-7, OA-23 default.
