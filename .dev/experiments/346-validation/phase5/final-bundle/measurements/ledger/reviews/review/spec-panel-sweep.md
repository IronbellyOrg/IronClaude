# Spec panel sweep: Orca worker contract spec

Command: `/sc:spec-panel-ledger @/tmp/review-ledger-sweep-3s8rdl6a/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --sweep`
Task: task_a89bfe5f12dc (dispatch ctx_1f18737f74b8). Date: 2026-11-09.
Input: the frozen sweep copy `/tmp/review-ledger-sweep-3s8rdl6a/orca-worker-contract-spec.md` (70565 bytes). Spec line numbers below (`S:N`) are lines of that copy.
Repo root for every other path: /home/coder/workspaces/worktrees/IronClaude/exp346-v-ledger.
Independence: this sweep did not open the ledger folder, the earlier review reports or the dispositions in `.dev/orca-command-refactor/review/`; it runs no ledger script.

## 1. Resolution table
The sweep did not open the ledger or earlier reports, so it cannot map earlier finding IDs. Instead it checks every revision tag (`Rn`) present in the frozen copy: does the tagged text now hold up on its own? "Holds" means no defect was found in that text; "Defect remains" names the new finding in section 3. Tags R14-R17 and R20 do not occur in the copy (`grep -noE '\(R[0-9]+\)'` plus a read of combined forms such as `(R2, R4)`), so they are not assessed.

| Tag | Spec location | What the tagged text does | Sweep result |
|---|---|---|---|
| R1 | S:63 (WC-4a), S:95 (workflow row) | `--report-dir` for workflow, whose `--output` is retired | Holds: `--output` is retired with `E-LEGACY` (`src/superclaude/skills/sc-workflow-protocol/SKILL.md:24`) and no yaml is written on a pre-creation STOP (`:26`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:39`). AC-1.2 still passes `--output` (finding N6) |
| R2, R4 | S:63 | Report path fixed before dispatch; separate `worker-contract.yaml` beside existing contracts | Holds for WC-4a itself. AC-1.1 still asserts the old filename (finding N12) |
| R3 | S:93 | TFEP troubleshoot keeps its 7-field contract | Holds: as cited (`src/superclaude/skills/sc-task-protocol/SKILL.md:206,216,220`; `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560`). `grep -n output_dir` on the task skill finds only those 3 lines, so the spec's UNVERIFIED on its derivation is correct |
| R5 | S:85 | Adversarial contract filename fixed; WC-4 report separate | Holds |
| R6 | S:197 (AC-0.4) | P0 uses each command's existing report | Holds |
| R7 | S:65 (WC-6) | Same-path re-run with a "started, not finished" report first | Defect remains: the guard covers only commands without a resume flag (finding N4) |
| R8, R21 | S:61 (WC-3) | Questions go to the coordinator; gate runs end blocked | Defect remains: R21's claim that every AC-2.2 gate run ends blocked contradicts the default resolutions of several P2 rows (finding N5) |
| R9, R22 | S:162 (P1) | P2-P4 commands block under `--unattended` until their phase; report flag added in P1 | Holds for the rule; AC-1.2 does not use the per-command flag (finding N6) |
| R10 | S:67 (WC-7a), S:197 | Skill call required, checked in the transcript | Holds (`CLAUDE.md:11`) |
| R11, R23, R24 | S:70 (WC-10) | Heartbeat, 240 s call limit, run-time budget | Defect remains: whether the 240 s limit covers Agent-tool calls is ambiguous (finding N2), and the budget is missing from the section 2.3 list it names (finding N3) |
| R12, R25 | S:188 (7.2 step 6) | New untracked files must be inside named paths; stagers never share a worktree | Holds for workers; tasklist creates the same condition inside one worker (finding N8) |
| R13 | S:179 (AC-C5) | `--numstat` replaces the grep, including for AC-0.3 | Defect remains: the AC-0.3 row still prints the grep (finding N9) |
| R18 | S:63 | P1 adds the report flags | Holds |
| R19 | S:93 | Under `/sc:task --unattended` only the task worker reports | Holds |

## 2. Citation-check table
Sample of the load-bearing citations, re-read in this checkout on 2026-11-09. The spec's own repo root is the `OrcaCLICommandRefactor-Specs` worktree (S:4); every path below was found at the same line here. The three inventories were read in full (`orca-capabilities.md`, `commands-a.md`) or at every line the spec cites (`commands-b.md`).

| Spec claim (location) | Citation | Result |
|---|---|---|
| Orca facts used in sections 1, 2, 7, 9 (E1-E4, R1-R4, WC-1 to WC-12, 7.2, D1, D5, UNVERIFIED 3, 5, 10, 11, 13) | `CAPS:10-21, 44-46, 52, 58-61, 64, 66-68, 72-80, 84-92, 97-103, 107-116, 122-130, 145-161, 178, 180, 187-188` | Match. One wording note: WC-10 (S:70) groups `projection.liveness` with `worker-show` as "process liveness", while `CAPS:123` calls `projection.liveness` the fleet verdict for the agent; the spec's point (liveness is not progress, `CAPS:130`) still holds. Not filed |
| Inventory verdicts and counts (section 3 intro, 3.1, 3.2, 4) | `INV-A:3, 14, 35-55, 60-62, 65, 76-83, 90-98, 106, 113, 118, 120`; `INV-B:3, 31-52, 65, 105, 112, 272, 285-299, 301, 311, 320, 323` | Match. 5 + 5 ready, 13 + 14 needs-change, 3 + 3 coordinator-only = 10 / 27 / 6 |
| 43 commands in `cmd/` (S:78) | `ls src/superclaude/commands` | Match: 43 `.md` files besides `README.md` |
| E5: only `ccsession-tag` mentions Orca (S:25); AC-C1 baseline (S:175) | `grep -rlni orca src/superclaude/{commands,skills,core,agents}`; the AC-C1 regex | Match: only `src/superclaude/skills/ccsession-tag/*`; the regex hits only `ccsession-tag/ccsession` and `ccsession-tag/README.md` |
| Core install and `KNOWN_CORE_FILES` (S:52, AC-0.1) | `src/superclaude/cli/install_core.py:4,13-24,33` | Match |
| Repo rules | `CLAUDE.md:11,16,50,74,76,83,157,334,408` | Match |
| Gate routes in WC-3 | `src/superclaude/commands/task.md:93`; `src/superclaude/commands/recommend.md:44`; `src/superclaude/skills/tdd/SKILL.md:52-61` | Match |
| auggie-review posts by default (WC-9, 3.2, P1) | `src/superclaude/commands/auggie-review.md:51-55` | Match ("No confirmation prompt") |
| Workflow contract and STOPs (WC-4a, 3.1, 7.2 step 6) | `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24,26,28,44,58,66,72`; `refs/return-contract.md:3-19,39,41` | Match |
| TFEP contract (3.1) | `src/superclaude/skills/sc-task-protocol/SKILL.md:206,214,216,220,225-226`; `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:560`; `src/superclaude/commands/troubleshoot.md:56` | Match |
| pr-submit top-level rule and wait budget (WC-7, WC-10, D3) | `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:37-39,46-64`; `src/superclaude/commands/pr-submit.md:49` | Match |
| implement Ruling rule (D2, 3.2) | `src/superclaude/skills/sc-implement-protocol/refs/qa.md:231-238` | Match |
| adversarial contract (3.1) | `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:427-429,436` | Match |
| reflect headless rule (SA-6, 3.1) | `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:228,239-247` | Match |
| save keys (WC-11) | `src/superclaude/commands/save.md:42-45` | Match |
| Routing guide and hard limit (SA-1, section 6) | `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`; `src/superclaude/core/CLAUDE.md:65` | Match |
| tasklist Stage 10.5 (3.2 tasklist row) | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1614,1623,1631` | Match: one `/sc:reflect --mode pre --remediate` agent per phase file, in parallel |
| File output flags (WC-4a) | `src/superclaude/commands/tdd.md:49`; `src/superclaude/commands/init-lite.md:32` | Match: both take a file path |
| PyYAML declared (7.2 step 4) | `pyproject.toml:38` | Match |
| Plugin build (UNVERIFIED 8) | `Makefile:68-74` | Match |
| "the repo itself treats it as unproven" (WC-10, S:70) | `~/.claude/commands/sc/spec-panel-ledger.md:261` | Line matches the installed file, but no `spec-panel-ledger.md` exists in `src/superclaude/commands/` (`ls`), so "the repo itself" is wrong (finding N10) |
| `/sc:git` needs the user's authorization "in this repo" (section 4, S:136) | `.dev/orca-command-refactor/README.md:31` | Overstated: line 31 is this run's worker rule ("No git commits, pushes, PRs or GitHub comments"), not a repo rule (finding N11) |

## 3. New findings
Panel: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard), with Whittaker's attacks, in critique mode. Grades use the panel scale: CRITICAL (provably wrong), MAJOR (ambiguous or incomplete, with a concrete wrong outcome), MINOR (behaviour still inferable). The ledger script decides which rows block; this sweep only grades.

### 3.1 Guard Condition Boundary Table (mandatory artifact)
The spec has guard conditions, so the table is required before findings (FR-10). Four guards carry the worker's outcome and liveness. GAP rows become findings (FR-8).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 outcome from report status | WC-5 (S:64) | Zero/Empty | report file exists but is 0 bytes, unparseable, or has no `status` | does not "say failed or blocked" | falls to "succeeded otherwise" | GAP (N1) |
| G1 | WC-5 | One/Minimal | `status: partial` | succeeded | succeeded, body states `partial` | OK |
| G1 | WC-5 | Typical | `status: succeeded` | succeeded | succeeded | OK |
| G1 | WC-5 | Maximum/Overflow | n/a: a single enum value | n/a | n/a | OK |
| G1 | WC-5 | Sentinel Value Match | `status: success` (the legacy vocabulary of an existing contract, WC-4a) | not failed or blocked | succeeded | GAP (N1) |
| G1 | WC-5 | Legitimate Edge Case | audit with verdict FAIL, `status: succeeded` | succeeded | succeeded, stated in WC-5 | OK |
| G2 single tool call limit | WC-10 (S:70) | Zero/Empty | 0 s call | allowed | allowed | OK |
| G2 | WC-10 | One/Minimal | 240 s call | allowed | allowed ("exactly 240 s is allowed") | OK |
| G2 | WC-10 | Typical | 60 s poll | allowed | allowed | OK |
| G2 | WC-10 | Maximum/Overflow | 300 s Bash call | refused | split into waits of at most 240 s | OK |
| G2 | WC-10 | Sentinel Value Match | Agent-tool subagent call of 10 min | either refused ("No single tool call") or allowed (WC-7 keeps fan-out) | both readings are in the text | GAP (N2) |
| G2 | WC-10 | Legitimate Edge Case | background Bash plus Monitor (cli-eval run) | not a blocking call | cli-eval row splits the wait | OK |
| G3 run-time budget | WC-10 (S:70) | Zero/Empty | brief states no budget | no expiry | undefined: section 2.3 does not list the budget | GAP (N3) |
| G3 | WC-10 | One/Minimal | budget shorter than one 900000 ms wait | wait uses the smaller value | wait ends at the budget, escalate | OK |
| G3 | WC-10 | Typical | budget not yet passed, heartbeats arriving | keep waiting | keep waiting | OK |
| G3 | WC-10 | Maximum/Overflow | budget passed, no `worker_done`, no stall proof | escalate | read transcript, escalate, never stop or retry | OK |
| G3 | WC-10 | Sentinel Value Match | `exited` liveness before the budget | stall proven | stop waiting early | OK |
| G3 | WC-10 | Legitimate Edge Case | heartbeat gap during a subagent call | not a hang by itself | stated | OK |
| G4 retry at the same report path | WC-6 (S:65) | Zero/Empty | no earlier report | first write | "started, not finished" report, then final | OK |
| G4 | WC-6 | One/Minimal | earlier report, command has no resume flag | overwrite at start | overwritten with `failed` first | OK |
| G4 | WC-6 | Typical | retry of a failed run, no resume flag | same path | same path, new artifacts only | OK |
| G4 | WC-6 | Maximum/Overflow | third failure | circuit breaker | Task failed (`CAPS:116`) | OK |
| G4 | WC-6 | Sentinel Value Match | earlier `blocked` report, command resumes (resume flag or implicit resume) and dies before its final write | no overwrite rule | earlier report stays and reads as current | GAP (N4) |
| G4 | WC-6 | Legitimate Edge Case | coordinator wants earlier files kept | move aside first | stated | OK |

### 3.2 Findings

**N1. MAJOR (FR-8). An existing but empty, unparseable or out-of-vocabulary report maps to `--outcome succeeded`.** Section 2.2 WC-5 (S:64). WC-5 says `--outcome failed` "when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise". A report truncated by a crash during its final write, a file with no `status`, or a worker that reads an existing contract whose vocabulary is `success | partial | failed` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`) all fall to "otherwise". Attack: a final write is cut off after `command:`; the file exists, so the worker sends `succeeded` and Orca settles the Task as done. 7.2 step 4 would catch this in a test run, but WC-5 is the run-time rule. Fix direction: `succeeded` only when `status` parses and is `succeeded` or `partial`; anything else is `failed`.

**N2. MAJOR (FR-8). It is ambiguous whether the 240 s single-call limit covers Agent-tool subagent calls.** WC-10 (S:70) says "No single tool call a command makes may block the session for longer than 240 s", and AC-4.3 (S:213) passes only if "no single tool call exceeds 240 s". The same paragraph says an Agent-tool call "can also block the session" and WC-7 (S:66) keeps every command's fan-out. Read literally, every fan-out command breaks WC-10 (for example adversarial advocates, `INV-A:35`, listed as ready with no fix at S:85), and AC-4.3 fails pr-submit whenever its `evidence-validator` subagent runs past 4 minutes (`INV-B:34` lists that subagent). Read the other way, the limit has an unstated exemption. Fix direction: state whether Agent-tool calls are exempt, and make AC-4.3 measure the same thing.

**N3. MAJOR (FR-8). The section 2.3 list of what each brief must state omits two items other rules depend on.** Section 2.3 (S:75) lists four items: the command line, the output directory, authorized outward actions and worktree placement. WC-10 (S:70) says the Task's longest expected run time is "one more item of the section 2.3 list", and WC-3 (S:61) says whether the coordinator answers questions is "one more item of the section 2.3 list". Neither is in the list, and P0's brief template is built from section 2 and the 3.1 flags (S:161). Wrong outcome: a coordinator following 2.3 sends no budget, so WC-10's bound and the "smaller of 900000 ms and the time left" rule have no value, and a stuck subagent is never escalated.

**N4. MAJOR (FR-8). WC-6's stale-report guard does not cover commands that resume.** WC-6 (S:65): "A command either resumes from its on-disk state when given its resume flag, or, if it has none, runs again in the same place: at start it overwrites any earlier WC-4 report ...". The overwrite is only in the second branch. A retry runs the same brief (S:65), so a command whose resume is implicit resumes on every retry: implement resumes "when a ledger matches" (S:112; `INV-A:51`). Attack: attempt 1 ends `status: blocked` with Ruling question Q1; the person rules; the retry resumes and the session dies before its final write; the earlier `blocked` report with Q1 still sits at the recorded path and reads as the retry's result, so the coordinator escalates an already-answered question. Fix direction: apply the start-of-attempt overwrite to both branches.

**N5. MAJOR. AC-2.2 requires every P2 gate-trigger run to end `blocked`, but several P2 gates resolve by a default, not as blocked.** AC-2.2 (S:203) passes only with `worker_done --outcome failed` and `status: blocked`, and WC-3 (S:61) says these runs "end `--outcome failed` with `status: blocked` (R21)". The P2 rows resolve some gates by WC-2 (a): auggie-review turns posting and the offer off (S:103), cleanup and improve apply allowed items and list the rest (S:106, S:113), research pins `--strategy planning` (S:119), tasklist passes `--unattended` to reflect (S:125), and reflect's `--remediate` follows the headless auto-accept rule (S:90). Wrong outcome: a correct `/sc:auggie-review <PR> --unattended` that skips posting and succeeds fails AC-2.2, or an implementer makes it block to pass the check. Fix direction: AC-2.2 applies only to gates that resolve as blocked; default-resolved gates are checked by AC-2.3 plus a check that the default was taken.

**N6. MAJOR. AC-1.2 passes `--output <dir>` to every P1 command, which contradicts the per-command report flag of WC-4a.** AC-1.2 (S:199): "7.2 live check on each P1 command with `--unattended --output <dir>`". P1 (S:162) includes the workflow fix, and workflow must "never `--output` (retired, it stops with `E-LEGACY`)" (S:95; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24`). WC-4a (S:63) gives `--report-dir` to commands with no output flag after their row's additions, which covers index-repo and cleanup-audit (fixed in P1, no output flag added, S:87-88) and the P2-P4 commands that gain `--report-dir` in P1. Wrong outcome: AC-1.2 run as written on workflow stops before any package or report exists, so step 4 fails on a correct implementation. Fix direction: run AC-1.2 with each command's WC-4a flag, and name which commands are "P1 commands".

**N7. MAJOR. `/sc:load` gets `--unattended` in P1 and must carry an Unattended section naming `return-contract.yaml`, but writes no report.** The load row (S:115) says Report "none", P1 change "usage line only", and "use it as a step inside another worker's brief, not as its own Task"; WC-4a excludes it from the report flag (S:63). But P1 makes "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (S:162), WC-4 says "In unattended mode the command writes `<output-dir>/return-contract.yaml`" (S:62), and AC-1.1 (S:198) asserts every 3.1-3.2 command has a `## Unattended mode` section naming `return-contract.yaml`. Wrong outcome: either AC-1.1 fails on the correct load change, or load's section claims a report it never writes. Load's behaviour under `--unattended` is undefined. Fix direction: exclude load from P1's flag rule and AC-1.1, or define its unattended behaviour.

**N8. MAJOR. Under `--unattended`, tasklist runs N parallel reflect remediations in one worktree, which the spec forbids for workers and does not report.** The tasklist row (S:125) has Stage 10.5 pass `--unattended` to each reflect "so the headless rule applies". Stage 10.5 fans out one `/sc:reflect --mode pre --remediate` agent per phase file in parallel (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1614,1623`), and the headless rule auto-accepts and authors the corrective artifact (`src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:239-247`), through `sc:workflow` on the plan route. The spec itself says workflow runs `git add .dev/tasks` and that two staging workers never share a worktree (S:188). Here N authors stage in parallel in one worktree inside one worker, and the new `.dev/tasks/to-do/<id>/` packages are not named in tasklist's report (row: "contract pointing at `tasklist-index.md` and `validation/ValidationReport.md`"), so 7.2 step 6 also fails. Whether workflow itself runs the `git add` is UNVERIFIED (`INV-B:317`); the spec relies on it. Fix direction: under `--unattended`, run Stage 10.5 without `--remediate` (or serially), and list any authored package in the report.

**N9. MINOR. The AC-0.3 row still uses the grep that AC-C5 says it replaced.** AC-C5 (S:179) says AC-0.3 "applies this same `--numstat` test ... in place of its grep (R13)", but AC-0.3 (S:196) still reads `git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md | grep -E '^-[^-]'`, which AC-C5 shows misses a deleted Markdown bullet. Behaviour is inferable from AC-C5, so MINOR.

**N10. MINOR. WC-10 attributes a statement to "the repo itself" that is not in the repo.** WC-10 (S:70) cites `~/.claude/commands/sc/spec-panel-ledger.md:261`. The line matches the installed file, but `src/superclaude/commands/` has no `spec-panel-ledger.md` (`ls`, 43 command files), so the source is an installed experimental command, not this repo. The claim it supports stays UNVERIFIED either way.

**N11. MINOR. The `/sc:git` row cites a run rule as a repo rule.** Section 4 (S:136) says git mutations "need the user's authorization in this repo", citing `.dev/orca-command-refactor/README.md:31`, which is this run's worker rule ("No git commits, pushes, PRs or GitHub comments"). The coordinator-only verdict stands on the other cited lines (`INV-A:49,91`).

**N12. MAJOR. AC-1.1 checks for `return-contract.yaml` where WC-4a requires `worker-contract.yaml`.** AC-1.1 (S:198) passes when each Unattended section names `return-contract.yaml`. For adversarial, brainstorm, reflect, workflow and troubleshoot, WC-4a (S:63) makes the WC-4 report `worker-contract.yaml` and keeps `return-contract.yaml` as the legacy file other commands read. Wrong outcome: a brainstorm section that tells the worker to report the legacy `return-contract.yaml` passes AC-1.1, and P1's live check AC-1.2 does not cover brainstorm (it is not in P1's command list, S:162), so the wrong `--report-path` reaches P2 unchecked. Fix direction: AC-1.1 asserts the WC-4a filename per command.

## 4. Verdict
**FAIL.** The sweep found 12 new findings: 9 MAJOR (N1-N8, N12) and 3 MINOR (N9-N11). The brief makes any finding of any severity a FAIL. No CRITICAL finding: section 1's decision (Orca coordinates, commands stay units of work) and its evidence hold; every defect is in the contract's edge rules (N1-N4), its acceptance checks (N5-N7, N9, N12), one command row (N8) or a citation (N10, N11). Whether these rows block is decided by the ledger script, not by this sweep.

## 5. Self-Audit
Not required: the verdict is FAIL. For the record, the sweep did not check: the roughly 250 section-3 command and skill line citations outside the sample in section 2; the live Orca guide output behind `[G]` and `[H:*]` (taken through the capabilities inventory, as the spec does); and whether core files reach plugin installs (`scripts/build_superclaude_plugin.py` has no `core` match, but the plugin route was not traced, so nothing was filed).

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| What the resolution table resolves | (a) open earlier reports and dispositions to map their IDs; (b) check the spec's own `Rn` revision tags | (b). The sweep must not open the ledger folder (`sc-review-ledger` SKILL, "The sweep context never opens the ledger folder"), and reading earlier reviews would anchor an independent sweep. |
| Repo root for citations | the spec's `OrcaCLICommandRefactor-Specs` worktree (S:4); this checkout | This checkout, as the brief names it. Every sampled citation matched here. |
| Severity of N9-N11 | MAJOR; MINOR | MINOR: the right behaviour is inferable from other spec text (N9) or the claim it supports is unchanged (N10, N11). |
| Guard table scope | every numeric or boolean guard in the spec; the four that decide outcome and liveness | The four (WC-5, WC-10 call limit, WC-10 budget, WC-6). Per-command gates are already resolved row by row in section 3 of the spec. |
| Rule field in ledger rows | FR-8 on every row; FR-8 only where a GAP row produced the finding | FR-8 only for N1-N4, which come from GAP rows; other rows carry no rule. |

## ledger-input
Sweep rows for the coordinator's ledger step (`sweep --input <this report>`). Every anchor was checked to occur exactly once in the frozen copy with `grep -oF ... | wc -l`. No row challenges a verified row (the sweep cannot see row IDs).

```ledger-input
{"rows": [
{"grade": "MAJOR", "rule": "FR-8", "label": "N1 WC-5 empty or unparseable report maps to succeeded", "anchor": "or no report exists; `--outcome succeeded` otherwise, including `partial`", "wrong_outcome": "A report that exists but is empty, truncated, has no status, or uses the legacy value success is mapped to --outcome succeeded, so Orca settles a failed Task as done.", "finding": "WC-5 sends succeeded for any existing report that does not say failed or blocked; it must send succeeded only when status parses as succeeded or partial.", "challenges": null},
{"grade": "MAJOR", "rule": "FR-8", "label": "N2 240 s limit vs Agent-tool calls ambiguous", "anchor": "No single tool call a command makes may block the session for longer than 240 s", "wrong_outcome": "Read literally, every fan-out command (adversarial, troubleshoot Tier 2) breaks WC-10 and AC-4.3 fails pr-submit whenever its evidence-validator subagent runs over 4 minutes; read the other way, the limit has an unstated exemption.", "finding": "WC-10 must say whether Agent-tool subagent calls are exempt from the 240 s single-call limit, and AC-4.3 must measure the same thing.", "challenges": null},
{"grade": "MAJOR", "rule": "FR-8", "label": "N3 section 2.3 brief list omits run-time budget and question-answer item", "anchor": "For each Task the coordinator's brief states:", "wrong_outcome": "A coordinator following section 2.3 sends no run-time budget, so WC-10's escalation bound has no value and a stuck subagent is never escalated; it also omits whether questions are answered.", "finding": "WC-10 and WC-3 each call their item one more item of the section 2.3 list, but the list names only command line, output directory, outward actions and placement.", "challenges": null},
{"grade": "MAJOR", "rule": "FR-8", "label": "N4 WC-6 stale-report guard misses resuming commands", "anchor": "A command either resumes from its on-disk state when given its resume flag", "wrong_outcome": "An implicit-resume retry (implement) that dies before its final write leaves the earlier blocked report and its already-answered question at the recorded path, read as the retry's result.", "finding": "The start-of-attempt overwrite applies only to commands without a resume flag; it must apply to resumed attempts too.", "challenges": null},
{"grade": "MAJOR", "rule": null, "label": "N5 AC-2.2 expects blocked for default-resolved gates", "anchor": "Gate-trigger run per P2 command", "wrong_outcome": "A correct /sc:auggie-review --unattended run that skips posting and succeeds fails AC-2.2, as do cleanup, improve, research, tasklist and reflect gates that resolve by a default.", "finding": "AC-2.2 and WC-3 (R21) require every P2 gate-trigger run to end failed and blocked, but several P2 rows resolve their gate by a documented default.", "challenges": null},
{"grade": "MAJOR", "rule": null, "label": "N6 AC-1.2 passes --output to every P1 command", "anchor": "7.2 live check on each P1 command with `--unattended --output <dir>`", "wrong_outcome": "AC-1.2 run as written on workflow stops with E-LEGACY before any package or report exists, failing a correct implementation; index-repo, cleanup-audit and --report-dir commands get the wrong flag too.", "finding": "AC-1.2 must use each command's WC-4a report flag and name which commands are P1 commands.", "challenges": null},
{"grade": "MAJOR", "rule": null, "label": "N7 load gets --unattended and an Unattended section but writes no report", "anchor": "none: use it as a step inside another worker's brief, not as its own Task", "wrong_outcome": "AC-1.1 fails on the correct usage-line-only load change, or load's Unattended section claims a return-contract.yaml it never writes; load's behaviour under --unattended is undefined.", "finding": "P1 makes every 3.1-3.2 command accept --unattended, WC-4 makes unattended runs write a report, and AC-1.1 requires a section naming return-contract.yaml, while the load row says it writes no report.", "challenges": null},
{"grade": "MAJOR", "rule": null, "label": "N8 tasklist --unattended runs N parallel reflect remediations in one worktree", "anchor": "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies", "wrong_outcome": "N parallel reflect agents auto-author workflow packages that stage .dev/tasks in one worktree, which the spec forbids for workers, and the new packages are not in tasklist's report, so 7.2 step 6 fails.", "finding": "Stage 10.5 fans out one reflect --remediate agent per phase in parallel; with the headless rule each authors a corrective plan through sc:workflow.", "challenges": null},
{"grade": "MINOR", "rule": null, "label": "N9 AC-0.3 row still uses the replaced grep", "anchor": "git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md", "wrong_outcome": null, "finding": "AC-C5 says AC-0.3 uses the --numstat test instead of its grep, but the AC-0.3 row still prints the grep that misses a deleted Markdown bullet.", "challenges": null},
{"grade": "MINOR", "rule": null, "label": "N10 WC-10 attributes an installed file to the repo", "anchor": "the repo itself treats it as unproven until a recorded smoke check shows it", "wrong_outcome": null, "finding": "The cited ~/.claude/commands/sc/spec-panel-ledger.md has no source copy in src/superclaude/commands/, so it is not the repo's statement.", "challenges": null},
{"grade": "MINOR", "rule": null, "label": "N11 git row cites a run rule as a repo rule", "anchor": "need the user's authorization in this repo", "wrong_outcome": null, "finding": ".dev/orca-command-refactor/README.md:31 is this run's worker rule, not a repo-wide authorization rule; the verdict stands on the other citations.", "challenges": null},
{"grade": "MAJOR", "rule": null, "label": "N12 AC-1.1 asserts return-contract.yaml where WC-4a requires worker-contract.yaml", "anchor": "has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`", "wrong_outcome": "A brainstorm Unattended section that points the worker at the legacy return-contract.yaml passes AC-1.1, and no P1 live check covers brainstorm, so the wrong report path reaches P2.", "finding": "For adversarial, brainstorm, reflect, workflow and troubleshoot the WC-4 report is worker-contract.yaml; AC-1.1 must assert the WC-4a filename per command.", "challenges": null}
]}
```

<!-- review-ledger tail: written by review_ledger.py sweep; do not edit -->
## Review ledger sweep

sweep

| id | grade | rule | would block | challenges | location | anchor |
|---|---|---|---|---|---|---|
| R37 | MAJOR | FR-8 | yes |  | outside_hunks | or no report exists; `--outcome succeeded` otherwise, including `partial` |
| R38 | MAJOR | FR-8 | yes |  | in_claimed_span | No single tool call a command makes may block the session for longer than 240 s |
| R39 | MAJOR | FR-8 | yes |  | outside_hunks | For each Task the coordinator's brief states: |
| R40 | MAJOR | FR-8 | yes |  | in_claimed_span | A command either resumes from its on-disk state when given its resume flag |
| R41 | MAJOR |  | yes |  | outside_hunks | Gate-trigger run per P2 command |
| R42 | MAJOR |  | yes |  | outside_hunks | 7.2 live check on each P1 command with `--unattended --output <dir>` |
| R43 | MAJOR |  | yes |  | outside_hunks | none: use it as a step inside another worker's brief, not as its own Task |
| R44 | MAJOR |  | yes |  | outside_hunks | Stage 10.5 passes `--unattended` to each reflect so the headless rule applies |
| R45 | MINOR |  | no |  | outside_hunks | git diff -U0 master...HEAD -- src/superclaude/core/HOW-WE-WORK.md |
| R46 | MINOR |  | no |  | in_claimed_span | the repo itself treats it as unproven until a recorded smoke check shows it |
| R47 | MINOR |  | no |  | outside_hunks | need the user's authorization in this repo |
| R48 | MAJOR |  | yes |  | outside_hunks | has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` |

delivery_outcome: ESCALATE (loop=ESCALATE, S=9, tails_intact=true)
verdict: FAIL
