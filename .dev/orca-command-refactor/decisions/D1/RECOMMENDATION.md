# Recommendation: D1, how a command knows it runs without a person

Status: COMPLETE (2026-11-02). Produced by finishing the interrupted `/sc:adversarial --compare` run for D1 (Steps 4 and 5).
Repo root: /home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs. Paths are repo-relative unless absolute.

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `ADV/` = `.dev/orca-command-refactor/decisions/D1/debate/adversarial/`; `MO:N` = `ADV/merged-output.md:N`; `DT:N` = `ADV/debate-transcript.md:N`; `BSel:N` = `ADV/base-selection.md:N`; `RP` = `ADV/refactor-plan.md`; `CR01:N` = `.dev/orca-command-refactor/changes/CR-01-feature-worktree-hierarchy.md:N`.

Process artifacts: `ADV/diff-analysis.md`, `ADV/debate-transcript.md`, `ADV/invariant-probe.md`, `ADV/base-selection.md` (Steps 1-3, written before the restart and used unchanged); `ADV/refactor-plan.md` and its fresh-context review `ADV/refactor-plan-review.md` (Step 4); `ADV/merged-output.md` and `ADV/merge-log.md` (Step 5); `ADV/return-contract.yaml`.

## 1. Recommended option and how it compares with the spec
**Recommended: option (c) as amended.** The `--unattended` flag stays the only thing that switches a command into unattended mode, exactly as option (a) says (`SPEC:55`). On top of that, the Orca worker session runs a "brief guard" from Phase 1: before it runs anything, it checks the command lines of its brief and refuses, with a named failure, when the flag is missing for a command that needs it, present for a command that cannot use it yet, when the installed copies of the command disagree, or when the command must never run as a worker (`MO:9-15`, `MO:64-70`).

**This changes the spec's recommendation, but extends it rather than overturning it.** `SPEC:331` recommends (a). The debate recommends (c), which is (a) plus one check in the worker session. Every command-side rule of (a) is kept unchanged (`MO:9`, `MO:106-107`). Option (b), detecting Orca, stays rejected, now withdrawn by its own advocate (`DT:658`).

All three advocates ended on (c): the advocate for (a) said "I now recommend option (c) as corrected in Round 1, not (a) alone" (`DT:657`), the advocate for (b) withdrew (b) (`DT:658`), and the advocate for (c) kept it (`DT:659`).

## 2. Confidence
**High that the flag is the right switch and that a worker-side guard should be added. Medium that the guard's detailed rules, as written now, will work first time.** (The levels are this author's judgment from the evidence below; the debate itself scores points, not the overall decision.)

What supports the high part:
- The debate agreed on all 31 points it scored (25 unanimous, 6 by majority), above the 80% threshold (`DT:612-616`).
- The two points that decide between (a) and (c) were unanimous for (c): the guard turns a silent stall into a named failure (scored at 98% confidence, `DT:588`), and only the guard enforces the "never run as a worker" ban (97%, `DT:595`).

What holds the detail part to medium:
- On score alone, (a) edged (c), 0.793 to 0.756, inside the 0.05 tie band; (c) was chosen by the debate tiebreaker, 12 points won against 3 (`BSel:154-161`). With the second scoring pass's verdicts alone, (a) would have been selected (`BSel:166`).
- The run ended `BLOCKED_BY_INVARIANTS`: a fault-finding pass found 5 high-severity gaps in the agreed design (`DT:631-653`). Depth "standard" allows no further debate round, so the fixes for those 5 were planned and merged but never argued by the advocates (`RP`, "Invariant Coverage"; `ADV/return-contract.yaml`: `status: partial`).
- A fresh-context review of the first fix plan found 3 blocking defects (`ADV/refactor-plan-review.md:59-77`). They were fixed in one fix cycle and not re-reviewed (`RP`, "Plan review").
- Several guard details rest on UNVERIFIED Orca and Claude Code behaviour (section 7).

## 3. Strongest argument that lost
**Option (a) alone: the flag, and nothing else.** It is the cheapest option, and all three advocates agreed on that (96%, `DT:591`). It also scored highest overall before the tiebreaker (`BSel:156`). Its case against (c):
- The guard catches only "template used, flag wrong". A brief written without the template gets exactly (a)'s behaviour anyway (`DT:608`; `MO:163`).
- Fixing the 5 high-severity gaps made the guard bigger: a guard line in the job template, a guard rule and a never-as-worker list in the contract file, one or two extra file reads per job, a refusal-reading rule for the coordinator, and four more live test runs (`MO:176`). (a)'s known weakness, a forgotten flag causing a stall, is already caught by the spec's existing stall test, though only after the fact (`SPEC:238`).

Why it lost: under (a) a forgotten flag makes the worker sit waiting on a prompt nobody sees, and Orca reports that worker as "healthy, not failed" (`SPEC:47`; `CAPS:52`). (c) turns that into an immediate failed outcome with a reason, which is how Orca asks workers to report failure ("Never encode failure only in prose", `CAPS:73`). (a) also leaves the "never run these as workers" rule as prose only (`SPEC:151`). (a) remains the fallback: removing the guard parts returns (a)'s switch without touching any command file; the job layout, the nested-command rule and the worktree setup are independent of the guard and stay (`MO:177-179`).

Option (b)'s best point, that Orca itself defines a worker by its preamble (`CAPS:148`), was not lost: it became the guard's trigger (`MO:46`).

## 4. What this means in practice

### What a person sees and does differently
- **Working in your own terminal: nothing changes.** Inside or outside Orca, every command asks the same questions and keeps the same defaults as today. Even typing the word `--unattended` inside a quoted request does not change anything (`MO:106-107`).
- **Handing work to Orca workers:** the coordinator (the AI session in Orca that plans the work) writes the unattended switch into each worker's job, but only for commands that have been converted to run without a person. Each job lists its commands on labelled `Command:` lines after one guard line (`MO:239`).
- **When a job is written wrong, you see a failure with a reason instead of a stuck worker.** Today the worker would sit silently waiting for an answer nobody can give, and Orca would show it as healthy. With the guard, the worker stops at once, runs nothing, and reports a failed job whose message starts `guard refused:` and says why, for example `brief lacks --unattended` (`MO:65-69`, `MO:113`).
- **The coordinator retries a refused job at most twice with a corrected job, then asks you** (`MO:155-156`). This follows the same two-fix limit the repo adopted for review loops in PR #343 (`MO:196`).
- **Some commands are refused as workers outright:** the six orchestration or person-only commands (`/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn`, `/sc:swarm-wizard`) and, while decision D3 keeps it that way, `/sc:pr-submit`. You or the coordinator run those yourselves (`MO:65`, `MO:117`).
- **One new decision per rollout phase:** before each phase's live worker tests, you are asked to approve committing that phase's edits to a branch, because Orca builds the test worktree from a branch and cannot see uncommitted edits (`MO:159`, `MO:185-187`).

### What could go wrong
- **The guard refuses jobs that are actually correct.** The first Phase 1 live test of every converted command would show this at once (`MO:141`). Fix: correct the guard text, or remove the guard.
- **An out-of-date installed copy of a command makes every job for it fail** with a reason that names a "stale copy". The cause is the setup step, not the guard: the fix is to bring the installed copy up to date (`MO:67`, `MO:77`).
- **A job written by hand without the template** gets no guard and behaves exactly as under (a): a forgotten switch can again cause a silent stall (`MO:163`).
- **The guard is a written rule an AI follows, not code.** It can be misapplied, just like every other worker rule (`MO:125`, `MO:129`).
- **A worker can still stall inside a converted command whose list of questions was incomplete.** The guard cannot see this; the spec's live stall test catches it only after the fact (`MO:165`).
- **Some Orca and Claude Code behaviour the guard relies on is unverified**, for example whether a job's text could still start with the command itself (section 7).

### What it costs to change later
- **Removing the guard is cheap:** delete the guard line from the job template, the guard rule and list from the shared contract file, the coordinator's refusal-reading rule, the four guard live runs, the guard's static test assertions and the coordinator-session manual run. No command file changes. The switch is then option (a) again (`MO:140`, `MO:145`, `MO:176-179`).
- **Moving to detection later (option (b)) would be expensive:** every command that accepts the flag (35 after Phase 4, `SPEC:195`) would need detection text, and that breaks the rule that commands never mention Orca (`SPEC:170`, `SPEC:314`; `DT:601`).
- **The flag itself is the costly part to change**, and that part is the same under (a) and (c). Inference: each converted command's `## Unattended mode` section is built around the flag (`SPEC:58`), so renaming or replacing it later means editing every one of them.

## 5. Exact spec wording change
Yes, the spec changes. The full set is 16 edits, W1-W16, written once with exact text in `ADV/merged-output.md` (`MO:210-320`); they are not copied here. None is applied by this run: they go into the next consolidated spec revision together with the other decisions and CR-01 (`CR01:3`).

The D1 entry itself (`SPEC:329-331`) changes as follows (W9 and W11, `MO:259-274`):
- `SPEC:329`, option (a): "The coordinator writes it into every worker's command line" becomes "The coordinator writes it into a worker's command line where the command accepts it at this phase (section 6)"; "(recommended)" is removed.
- New option (c) after `SPEC:330`, quoted from `MO:272`:
  > - (c) **Flag plus a worker-session brief guard (recommended).** Commands behave exactly as in (a). From P1 the worker session checks every `Command:` line of its brief before running any, and refuses with `worker_done --outcome failed` (body starting `guard refused:`), running nothing, when the flag is missing while every existing copy of the command file has an `## Unattended mode` section, when the flag is present while no copy has it, when the copies disagree, or when the command is on the never-as-worker list (section 2.1, "Brief guard"). A forgotten flag becomes a named failure instead of a silent stall that Orca reports as healthy (`CAPS:52`, `CAPS:73`). Removing the guard parts returns (a).
- `SPEC:331`: "Recommendation: (a)." becomes "Recommendation: (c), that is (a) plus the brief guard, as amended in `.dev/orca-command-refactor/decisions/D1/debate/adversarial/merged-output.md`."

The other edits, by target:

| Edit | Target | What changes | Text |
|---|---|---|---|
| W1 | `SPEC:54` | D1 is no longer "open"; the mode is selected only by the flag | `MO:215-217` |
| W2, W3 | `SPEC:58` and three new section 2.1 terms | Contract file holds the brief guard, the never-as-worker list and the nested propagation rule | `MO:220-229` |
| W4, W5, W6 | `SPEC:79`, new "Brief layout" paragraph, new bullet after `SPEC:84` | Flag only where accepted at this phase; `Command:` line layout with a guard line; how to read a guard refusal; 2-fix cap | `MO:232-244` |
| W7, W8 | `SPEC:90`, `SPEC:93`; AC-2.2 and AC-2.6 | Worked example and test briefs use the new layout | `MO:247-256` |
| W10, W12 | `SPEC:330`; `SPEC:395` item 13 | Environment route closed by inference, item 13 stays open | `MO:265-267`, `MO:277-279` |
| W13 | New UNVERIFIED items 24-27 | Copy precedence, Task text start, mid-brief invocation, Orca setup running `make sync-dev` | `MO:282-287` |
| W14 | `SPEC:235-236` | 7.2 disposable worktree created by Orca from a branch holding the committed phase edits, synced, removed with `orca worktree rm`; never under `.dev/worktrees/` | `MO:290-295` |
| W15 | AC-1.1, AC-1.3, new AC-1.7, AC-2.1, new AC-2.9, section 7.4 | Guard checks: static, one live run per refusal case, coordinator-session manual run, nested-invocation assertions, discriminating tdd run | `MO:298-311` |
| W16 | `SPEC:183`, `SPEC:107`, `SPEC:115` | Phase 2 section edits for workflow and brainstorm, which call other commands | `MO:314-320` |

W14 overlaps CR-01's own replacement of `SPEC:235` (`CR01:41`); the consolidated revision should apply them as one edit.

## 6. Interactions with D2-D5, git ownership and CR-01
Status of the other decisions, re-read at about 18:50Z on 2026-11-02 after sibling sessions finished them: D3, D4, D5 and git ownership have COMPLETE recommendation files; D2's says COMPLETE pending its citation check (`decisions/D2/RECOMMENDATION.md:3`). The combined file `decisions/RECOMMENDATIONS.md` is still a stub (`decisions/RECOMMENDATIONS.md:5`). Each of those files was written before this one and treats D1 as unfinished; their D1 rows agree with this recommendation (cited below).

| Decision | Its recommendation | How it interacts with D1 |
|---|---|---|
| D2 (who gives a Ruling when `/sc:implement` halts) | (a) plus (c): keep the Ruling rule word for word; the person gives the Ruling, either by resuming in their own session or by writing it into the ledger, after which the coordinator starts a resume Task (`decisions/D2/RECOMMENDATION.md:7-11`) | Compatible. The resume Task is an ordinary worker brief, so it carries `--unattended` and `--report-dir` and the guard applies unchanged; implement accepts the flag from P4 (`SPEC:195`). D2 also needs implement to accept those two options before the source argument (`decisions/D2/RECOMMENDATION.md:133`). The guard never relays or checks a Ruling. |
| D3 (pr-submit as a worker) | (a), amended: pr-submit is not a worker; each PR's run is an ordinary top-level session in that PR's child worktree, started only when the person names the PR; a worker per PR, (b), is deferred (`decisions/D3/RECOMMENDATION.md:9`) | Direct dependency, and the two agree (`decisions/D3/RECOMMENDATION.md:86`). pr-submit stays on the guard's never-as-worker list, which closes the gap where a flagless pr-submit job would run with its outward defaults on (`MO:117`). A person's session, or one the coordinator launches for the person, has no worker preamble (`SPEC:53`), so the guard never applies there; whether a session started with `orca agent launch` carries a preamble is UNVERIFIED, and if it did, the guard would refuse pr-submit visibly rather than run it. If D3 (b) is ever adopted, D3 must say how that route passes the guard (`MO:206`). |
| D4 (may a brief authorize outward actions and commits) | (c′): no worker ever does anything that leaves the machine; one local commit only when the user asked for it and the worker is alone in its own Orca child worktree; (b), "never", is the default otherwise. This overturns the spec's (a) (`decisions/D4/RECOMMENDATION.md:7-9`) | Compatible (`decisions/D4/RECOMMENDATION.md:111`). D1 turns every outward default off under the flag (WC-9, `SPEC:73`; `MO:110`); D4 decides what a brief may add back. The guard checks only the switch and the command name, never outward-action flags or the worker's end-of-Task commit. |
| D5 (raise Orca's nesting depth) | Keep depth 1, plus a new rule WC-13 that the worker session never starts Orca work (`decisions/D5/RECOMMENDATION.md:7`, `:10`) | Compatible. D1's nested propagation rule covers commands calling commands inside one worker (Skill tool or Agent tool), not workers starting workers (`MO:89`). The guard and WC-13 are both worker-session rules in `WORKER-CONTRACT.md` and do not overlap. One wording point: D5's text describes a brief as carrying one command line (`decisions/D5/RECOMMENDATION.md:48`), while D1's brief layout allows several `Command:` lines, such as a `/sc:load` line before the command (`MO:81`); the consolidated revision should use D1's layout. |
| Git ownership | Option E, the hybrid: the coordinator owns every push, PR, comment, merge and worktree removal; a worker may commit locally only in its own child worktree with a quoted grant (`decisions/git-ownership/RECOMMENDATION.md:9`) | Compatible. `/sc:git` is on the never-as-worker list (`MO:228`). The per-phase commit that D1's live tests need (`MO:186`) falls to the coordinator under git ownership's rule for coordinator commits, made only when no worker runs in that worktree (`decisions/git-ownership/RECOMMENDATION.md:15`); it still needs the user's authorization. |
| CR-01 (feature worktree, child worktrees on triggers) | Proposed, not applied (`CR01:3`) | Compatible. The guard is per worker session and works the same in the shared feature worktree or a child (`MO:200`). CR-01's "setup before use" (`CR01:24`) is the same step the guard's every-copy rule needs (`MO:201`). Under D3 (a), CR-01's pr-submit trigger T3 applies to the coordinator's or person's own run (`MO:207`). |

Fixed user decisions applied (not debated):
- **Worktrees only by Orca at its default paths:** the spec's 7.2 test worktree under `.dev/worktrees/` (`SPEC:235`) is replaced by an Orca-created one (W14). The repo rule at `CLAUDE.md:299-300` still says `.dev/worktrees/`; its repo-wide refactor is planned separately (`CR01:41`).
- **SuperClaude upstream never touched:** D1 adds no GitHub or outward action of any kind (`MO:193`).
- **PR #343 review rules:** the guard's retry cap reuses the 2-fix-cycle limit; each phase's own `/sc:implement` review follows PR #343 unchanged (`MO:196-197`).

## 7. Assumptions and unverified points
- UNVERIFIED: which copy Claude Code loads when a project `.claude/commands/sc/` copy and the `~/.claude/commands/sc/` copy both exist. The guard reads both and refuses when they disagree, so it does not depend on the answer (`MO:76`, `MO:284`).
- UNVERIFIED: whether Orca's job text for a worker could still start with the `/sc:` command, which would let the command's skill load before the guard runs (`MO:60`, `MO:118`).
- UNVERIFIED: whether a command run from a labelled `Command:` line in the middle of the brief still counts as run directly at the top level; the spec's first-phase transcript check settles it (`MO:61`).
- UNVERIFIED: whether Orca's worktree setup runs `make sync-dev` (`CR01:42`); if not, the coordinator runs it before starting the worker (`MO:188`).
- UNVERIFIED: whether `ORCA_TERMINAL_HANDLE` is set in a person's own Orca tab (`SPEC:395`). D1 no longer depends on it, because nothing reads the variable (`MO:279`).
- UNVERIFIED: whether reflect's headless rule fires for an Orca worker; assumed not (`SPEC:391`; `MO:40`).
- Assumption: the five high-severity fixes (`ADV/return-contract.yaml`, `unaddressed_invariants`) are correct as planned. They were reviewed once on paper but not argued in a debate round or run live.
- UNVERIFIED: whether a session the coordinator starts with `orca agent launch` (D3's launched pr-submit session) carries an Orca worker preamble (section 6, D3 row).
- Assumption: D2's recommendation is unchanged by its pending citation check.

## 8. Self-Audit
- **Process followed:** `~/.claude/skills/sc-adversarial-protocol/SKILL.md` Steps 4 and 5 with `refs/artifact-templates.md` sections 4-6. Steps 1-3 were used as written, not redone or rescored. Step 4: plan drafted by the orchestrator, then reviewed by a fresh-context agent (`ADV/refactor-plan-review.md`: FAIL, 3 blocking, 14 minor), then one fix cycle. Step 5: `merge-executor` agent applied 24 of 24 changes; its post-merge validation passed with 102 of 102 internal references resolved and one contradiction fixed in place (`ADV/merge-log.md:6`, `:246-265`). Return contract written with `status: partial` (`ADV/return-contract.yaml`).
- **Independent checks of this file:** a fresh-context evidence validator re-read about 128 citations in sections 1-7: 0 missing, 1 wrong (the status of the sibling decisions, which had changed on disk since drafting), 11 overstated. All 12 were corrected: wording narrowed, the second-pass sensitivity named, the guard-part list separated from the independent parts, "exactly (a)" removed, the 35-command figure sourced to `SPEC:195`, section 6 rewritten from the sibling recommendation files, and the author's own estimates and inferences labelled.
- **Read directly for this file:** the spec (all 406 lines), CR-01, the D1 variants, base selection, invariant probe, debate transcript scoring and convergence sections, Round 1 and Round 2 statements cited, merged output (all), the sibling recommendation headers and D1 rows, `src/superclaude/core/CLAUDE.md:74`, `sc-workflow-protocol/SKILL.md:58,60`, `sc-brainstorm-protocol/SKILL.md:179,185`, root `CLAUDE.md:37,88,299-300`, and the PR #343 commit body (`git show 80f934de`).
- **Not done:** no live Orca or Claude Code run (every UNVERIFIED item in section 7 stays open); no second review of the Step 4 fixes; no edit to the spec or to any file outside `decisions/D1/`; no commit, push or GitHub call.
