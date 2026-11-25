# Step 3 qualitative scoring, pass 2 (reverse order): D02 scheduler, cron vs Orca automation

Evaluator: independent pass 2 (Variant 2 read first, then Variant 1). Rounds files, base-selection.md and other evaluators' scores were not read.
Variant 1 = OURS (cron, one dispatcher). Variant 2 = CLAY (Orca automation, no-agent precheck).
Scale: 1 = MET, 0 = NOT MET. Each row is a CEV entry: the claim is the criterion, the evidence is a quote or section reference, the verdict is the 1 or 0.
Spot checks made (read-only): master `agent-work-report/SKILL.md:30`, `waker.py` lines 1-2, 46-50, 144-146, 314-317, master `scripts/merged_pr_log_orca_automation.md:17-23`, master `docs/designs/orchestrator.md` 4.8, R4 (line 76), U6/U7, N5, O3/O4, `requirements.md` R6, R16, R21, line 18, `dispatch.py` flock, `issue-watcher-setup.md` six-field lines, and `orca-ide automations create --help` (precheck wording and Run now bypass match both papers). Variant 1 cites `issue-watcher-setup.md:288` and `:676`; the six-field lines are actually 289 and 677 (off by one, not scored as a factual error).

Requirements checked for C1: (a) precheck claim tested against waker.py and Orca CLI help/docs; (b) owner's R6/R16 and Coder issue 515; (c) Clay's R4 and design spec 4.8; (d) owner's "debated and rejected" statement; (e) sources cited; (f) unverified items marked.

## Completeness

| Criterion | Variant 2 verdict | Variant 2 evidence | Variant 1 verdict | Variant 1 evidence |
|---|---|---|---|---|
| C1 covers all explicit requirements | 0 | Covers (a) CLI help and waker.py, (b) Coder 515 (fact 6), (c) R4 and 4.8 (Mechanism, fact 9), (e), (f). Misses R6/R16 by name, never addresses the one-dispatcher shape, and never checks the "debated and rejected" statement (fact 9 only says "The owner's reason ... was written afterwards"). | 0 | Covers (b) R6/R16 and 515 (facts 1, 3), (c) 4.8 (facts 6-9), (d) (Risk: "not backed by the owner's debate folder"), (e), (f). Does not test the precheck claim against waker.py (only cites waker.py:46-50 for time zone, never the master skill's "VERIFIED 2026-11-03"), and never names Clay's R4. |
| C2 edge cases and failure scenarios | 1 | Cost: "'Run now' ... bypass the precheck, so a click starts a real Claude session"; fact 5: "exit 75 hidden by the detach"; fact 2: usage-limit error; Risk: schedule when Orca app not running. | 1 | Fact 6 (Run now click starts a Claude session); fact 7 ("ok" and "the poll crashed" look the same); Cost: six-field cron line; crontab "resets on an image update". |
| C3 dependencies and prerequisites | 1 | Mechanism: workspace env `~/.aienv`; Cost: `--prompt` and `--provider` required; fact 7: U6 PATH, U7 `*/5`; Cost: creation is an owner step (O3, O4). | 1 | Mechanism: "install `cron`, start the daemon at every boot, recreate the entry once per boot (Coder issue 515)"; fact 2: `orca repo list` under `PATH=/usr/bin:/bin`, `gh auth` under cron. |
| C4 success or completion criteria | 1 | Fact 7: "a 24-hour shadow run with `--dry-run` as a scheduled run before switch-on" and create `--disabled` then read the next run (U7). A stated gate before switch-on. | 0 | No acceptance or done test for adopting cron. Fact 3 lists the 515 job but not how to know it works; the runbook line fix is "UNVERIFIED by a test" with no plan to test it. |
| C5 out of scope | 0 | No out-of-scope statement. N5 and "owner step" are constraints, not scope exclusions. | 0 | No out-of-scope statement. |
| **Subtotal** | **3** | | **2** | |

## Correctness

| Criterion | Variant 2 verdict | Variant 2 evidence | Variant 1 verdict | Variant 1 evidence |
|---|---|---|---|---|
| K1 no factual errors | 1 | Spot checks hold: SKILL.md:30 quote with "(VERIFIED 2026-11-03)"; waker.py:1-2 "The waker: the Orca automation's only job"; waker.py 144-146 and 314-317 comments; merged_pr_log script shape at 17-23; 4.8 and R4 text; CLI help quote exact. | 1 | Spot checks hold: R6/R16 text, R21 line, line 18 quote, dispatch.py flock, handoff doc gh test, CLI help, `*/5` crontab line. Only a one-line citation drift (288/676 vs 289/677). |
| K2 feasible within stated constraints | 1 | Pattern already runs on master (fact 1); poll detached so 60 s precheck limit not hit (fact 5); N5 respected by owner-run creation (Cost). | 1 | Cron fires on time (fact 2); needs Coder image change (Cost: "issue 515, a separate repo, still open"), stated as a constraint. |
| K3 terminology consistent | 1 | "precheck", "poll", "waker", "automation" used the same way throughout. | 1 | "dispatcher", "cron entry", "poll" used consistently; "cycle" and "tick" are loose but not conflicting. |
| K4 no internal contradictions | 1 | Fact 4 "Gating is documented behaviour" and Risk "Official documentation does not describe a script-only automation" are reconciled (gate documented, script-only mode not). | 1 | Fact 1 (cron decision) and Risk (owner's reason is true only when precheck exits 0) are stated as separate; "What OURS gets right" does not rely on the weak sentence. |
| K5 claims supported by evidence | 1 | Each numbered fact carries file:line or URL; fact 6 flags the image-update survival as "an inference, not a test (UNVERIFIED)". | 1 | Each numbered fact carries file:line or URL; items 7-9 tie to design lines; fact 8 says "nothing is proven here". |
| **Subtotal** | **5** | | **5** | |

## Structure

| Criterion | Variant 2 verdict | Variant 2 evidence | Variant 1 verdict | Variant 1 evidence |
|---|---|---|---|---|
| T1 logical section ordering | 1 | Claim, Mechanism, Cited facts, Cost, Risk, What CLAY gets right. | 1 | Claim, Mechanism, Cited facts, Cost, Risk, What OURS gets right. |
| T2 consistent hierarchy depth | 1 | One H1 and flat H2 sections throughout. | 1 | One H1 and flat H2 sections throughout. |
| T3 separation of concerns | 1 | Cost (known downsides) separate from Risk (unverified parts) and from facts. | 1 | Cost, Risk and facts are separate headings, though the Risk section also holds a self-critique of the argument. |
| T4 navigation aids or cross references | 1 | Numbered facts; cross references such as "(design 4.8, `docs/designs/orchestrator.md:343-354`; ruling R4 at line 76)" and "U6 ... U7". | 1 | Numbered facts; cross references such as "(`orchestrator.md:1264-1265`)" and "R21 (same file, line 49)". |
| T5 position-paper convention | 1 | Section headings are exactly claim, mechanism, evidence, cost, risk. | 1 | Section headings are exactly claim, mechanism, evidence, cost, risk. |
| **Subtotal** | **5** | | **5** | |

## Clarity

| Criterion | Variant 2 verdict | Variant 2 evidence | Variant 1 verdict | Variant 1 evidence |
|---|---|---|---|---|
| L1 unambiguous language | 1 | Claim names the exact command and the exact outcome ("Orca records `skipped_precheck`, starts no agent and leaves no terminal"). | 0 | "The only thing cron needs from outside this repo is the template" never says which template; "the poll", "cycle", "tick" and "dispatcher" are used for overlapping things without a definition. |
| L2 concrete rather than abstract | 1 | Full precheck command shape quoted from SKILL.md; dated firings (2026-11-04, 2026-11-18). | 1 | Full cron line with `flock -n`; dated cron firings (20:25:01Z, 20:26:01Z). |
| L3 each section has a clear purpose | 1 | Each heading states its purpose; Cost and Risk are distinct. | 1 | Each heading states its purpose. |
| L4 terms defined on first use | 1 | "U6 (PATH inside the precheck shell ...)", "N5 forbids the orchestrator", "ruling R4" each glossed in place. | 1 | "R21 (...cron 3.0pl1-197 is installed ...)", "U6 ... U7" glossed; R6/R16 glossed as "one entry, one dispatcher". |
| L5 actionable next steps or decision points | 1 | Fact 7: create `--disabled`, read next run, 24-hour shadow run before switch-on. | 1 | Cost: "The runbook line must be fixed"; Mechanism: boot step per Coder 515. |
| **Subtotal** | **5** | | **4** | |

## Risk coverage

| Criterion | Variant 2 verdict | Variant 2 evidence | Variant 1 verdict | Variant 1 evidence |
|---|---|---|---|---|
| R1 at least 3 risks with probability and impact | 0 | Risk section lists three unverified points but gives no probability or impact for any. | 0 | Risk section lists two items; none has probability or impact. |
| R2 mitigation for each risk | 0 | Mitigation is given only for U6/U7 (fact 7); none for "no script-only documentation" or "app not running". | 0 | "Our argument must not lean on that sentence" is the only response; no mitigation for the unbacked debate claim or the open Coder issue. |
| R3 failure modes and recovery | 0 | Failure modes are named (exit 75, 429 usage limit, Run now click) with detection via `audit.jsonl` and `status`; no recovery step is stated. | 1 | Fact 3 and Mechanism: crontab "resets on an image update, so a boot step recreates it"; dispatcher and per-repo flock layers give a stated recovery path (a locked tick exits, the next tick retries). |
| R4 external dependencies and their failure | 1 | Risk: "Whether the schedule keeps firing when the Orca app or server is not running is not stated"; fact 6: Orca user data on home volume (inference marked UNVERIFIED). | 1 | Cost: Coder image change "still open"; fact 3 crontab reset on image update; fact 2 Orca runtime reachable from cron's environment. |
| R5 monitoring or validation mechanism | 1 | Fact 8: run history and `orca automations list`; Cost: `audit.jsonl` and `issue-watch status`; shadow run. | 1 | Mechanism: log file `issue-watch.log` plus exit code; "a plain, auditable record of every tick". |
| **Subtotal** | **2** | | **3** | |

## Invariant and edge case coverage

| Criterion | Variant 2 verdict | Variant 2 evidence | Variant 1 verdict | Variant 1 evidence |
|---|---|---|---|---|
| I1 boundary conditions for collections (zero, one, many) | 0 | Only one automation and one poll are discussed. The command is `issue-watch once` (one repo); the paper never says what happens with many repos or with a new project. | 1 | Mechanism: "the dispatcher discovers repos on every tick, so a new project needs no scheduler change. An Orca automation is bound to one `--repo` or `--workspace`." Covers one against many. Zero repos is not covered. |
| I2 state variable interactions across component boundaries | 1 | Fact 5: precheck exit and detach versus the poll's own `flock` on `state_dir/lock`, "exit 75 hidden by the detach". | 1 | Mechanism: dispatcher `flock` and per-repo lock "Two layers, no overlap". |
| I3 guard condition gaps | 1 | Cost: "Run now" and `orca automations run` bypass the precheck gate. | 1 | Fact 6 (same bypass) and "What OURS gets right": "no edit mistake, wrong exit code or 'Run now' click can start an agent" under cron. |
| I4 count divergence (tick count, timeouts, history caps) | 1 | Fact 5: "the 60-second precheck limit does not apply to it" (timeout versus 5-minute tick); fact 7: U7 whether `*/5` is accepted. | 1 | Cost: runbook FU-2 is six-field (`0 */5 * * * *`) but "cron 3.0pl1 takes five fields". |
| I5 interaction effects when components combine | 1 | Detached poll plus precheck plus flock: the poll's exit is invisible in Orca history (Cost: "The poll's own outcome is not in Orca's history"). | 1 | `flock -n` wrapper plus dispatcher lock plus per-repo lock; cron plus Orca "two services to keep up at boot". |
| **Subtotal** | **4** | | **5** | |

## Summary

| Dimension | Variant 2 (Clay, Orca automation) | Variant 1 (Ours, cron) |
|---|---|---|
| Completeness (5) | 3 | 2 |
| Correctness (5) | 5 | 5 |
| Structure (5) | 5 | 5 |
| Clarity (5) | 5 | 4 |
| Risk coverage (5) | 2 | 3 |
| Invariant and edge cases (5) | 4 | 5 |
| **Total (/30)** | **24** | **24** |
