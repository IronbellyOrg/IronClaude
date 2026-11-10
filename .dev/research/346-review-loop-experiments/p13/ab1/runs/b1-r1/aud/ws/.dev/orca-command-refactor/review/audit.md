review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (first review)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `06020a7826f57dcd282a3b34507468f8ee1a370773f0665ff1254c475d92b7fd` (285 lines)
- Baseline: none given, none needed (first review of the whole document). Prior report: none.
- Reviewer model actually used: claude-sonnet-5-5
- Coverage: whole document, all 9 sections plus Decisions and UNVERIFIED. The candidate's `INV-A`/`INV-B`/`CAPS` line citations were checked against `inventory/commands-a.md`, `commands-b.md` and `orca-capabilities.md`. Every `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `tests/` and `/opt/Orca` citation is UNVERIFIED here: none of those files is in the workspace. The only files read were the README, the three inventories, the candidate, `command.md` and the review-loop prompts.
- Prompt used: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). The candidate was not edited and no other review was started.

## Citation check (what could be verified)

- Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in the candidate's sections 1 to 9 was spot-checked against its inventory file. All matched. Examples: `CAPS:92` (spec:21), `CAPS:97-101,103` (spec:33), `CAPS:148-150` (spec:35), `CAPS:178,180,186-188` (spec:274-276), `INV-A:76-83` (spec:26), `INV-B:289-299` (spec:26), `INV-B:272` (spec:261).
- Section 3 per-command `INV-*` row references (spec:83-125) all point at the matching inventory rows.
- Counts: the inventories give 5+5 ready, 13+14 needs-change, 3+3 coordinator-only (`commands-a.md:73`, `commands-b.md:278`). The spec's 10 / 27 / 6 matches (spec:76). The section 3.1 list has 10 rows, the section 3.2 list has 27 rows, the section 4 list has 6 rows. The section 6 phase rows cover 15 + 15 + 4 + 3 = 37 commands, which is 10 + 27 minus `load`, as the spec says (spec:112, 159-162).
- UNVERIFIED (not checkable in this sandbox): spec:11 ("re-read 11 load-bearing locations"), spec:25 (E5 grep results), spec:285 (item 14, "about 340 citations re-read"), and all `src/...:N` citations in sections 2 to 7.

## Guard Condition Boundary Table (hard gate, completed before synthesis)

Triggered: the spec contains thresholds and guards (60 s readiness, 5 and 4 minute waits, nesting depth 1, status and outcome mapping, missing output path). Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 output path present | spec:62 | Zero/Empty | no `--output`, `--output-dir` or `--report-dir` passed | false | "writes nothing and the worker ends `failed`" | OK for commands that take the flag; GAP for troubleshoot, cleanup-audit, index-repo, which have no output flag (see B-1) |
| WC-4 output path present | spec:62 | Typical | `--output <dir>` | true | contract at `<dir>/return-contract.yaml` | OK |
| WC-4 output path present | spec:62 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | true | `<output-file>.return-contract.yaml` | OK for those two; GAP for the new flags in spec:99-125 (file or dir is not said, see M-4) |
| WC-4 output path present | spec:62, 64 | Legitimate Edge Case | path not writable, or an earlier attempt's path | n/a | not stated; WC-6 says the coordinator makes the path new each attempt | GAP, Medium (coordinator-side promise only) |
| WC-5 status mapping | spec:63 | Zero/Empty | no report, empty report, `status` missing | false | `--outcome failed` | OK |
| WC-5 status mapping | spec:63 | Sentinel Value Match | `status: partial` | true | `succeeded`; first body sentence states `partial` | OK |
| WC-5 status mapping | spec:63 | Sentinel Value Match | `status: succeeded` with non-empty `blocked_question` | true | `failed` | OK |
| WC-5 status mapping | spec:63 | Legitimate Edge Case | existing contract version `1.1` (workflow) against `version == 1` check | false | WC-4 keeps existing fields; AC 7.2 step 4 asserts `version == 1` | GAP, Medium (M-5) |
| WC-10 wait split | spec:68, 266 | Typical | one tool call under 4 min | false | no split needed | OK |
| WC-10 wait split | spec:68, 114, 210 | Maximum/Overflow | one tool call between 4 and 5 min | false for WC-10 (">5 min"), true for AC-4.3 ("no call exceeds 240 s") | the two thresholds disagree | GAP, Medium (M-3) |
| WC-10 wait split | spec:68 | Legitimate Edge Case | exactly 5 min, 600 s default wait | n/a | WC-10 says "longer than 5 minutes"; pr-submit row says each iteration stays under 4 min | OK, with the M-3 caveat |
| WC-1 launch-path fallback | spec:59 | Maximum/Overflow | fallback of 45 s or more | true (too slow) | cites `EVIDENCE.md:45,56` ("above about 45 s it fails again") | OK, evidence given; the requirement itself says only "well inside" (minor, m-4) |
| Nesting depth | spec:33, 66, 252 | Typical / Maximum | depth 1 (current), depth raised (D5 b) | true / false | WC-8 forbids Orca fan-out from commands at any depth | OK |
| `--unattended` and TDD input | spec:120 | Zero/Empty | `target_release` absent | true | resolves as blocked | OK |

Input classes left out: One/Minimal for WC-4 and WC-5 (the same as the typical row; a single-file report adds no new branch); Maximum/Overflow for WC-4 and WC-5 (no size or count limit is stated anywhere in the spec, so there is nothing to probe); Zero/Empty for WC-10 (a zero-length wait cannot split further).

The table is complete: every cell is filled and every omitted class has its reason. FR-8 and FR-9 findings from it are graded in the findings below (B-1 blocking; M-3, M-4, M-5 Medium).

Pipeline Dimensional Analysis: the spec describes a plan and a command inventory, not a multi-stage data flow with N-to-M count changes. FR-17 does not trigger, so no Quantity Flow Diagram is produced. The only count conservation in the document (43 commands = 10 + 27 + 6, and 37 phased commands) was checked above and holds.

## Panel (critique mode, fixed review order)

Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower reviewed in that order. Under `--focus requirements,architecture` the lead experts are Wiegers (requirements) and Fowler (architecture). No `--experts` restriction was given.

### Grading statement

Each finding below was put through the FIRST-REVIEW grading check. Only B-1 holds as "an implementer who follows the stated text as written builds X, and X is wrong because Y" with no further assumption. Everything else needs a guess, or is a requirement the document never states, so it is Medium and listed under follow-up candidates, whatever its label.

## === REQUIREMENTS ANALYSIS ===

### B-1 (MAJOR, blocking). The contract path is unknowable for commands that have no output flag, and WC-4 turns that into a guaranteed failure

- Experts: Wiegers (traceability), Whittaker (Zero/Empty Attack and Divergence Attack), Crispin (acceptance cannot pass).
- Priority: High. Quality impact: three of the ten "ready" commands cannot complete an unattended run as specified.
- Grading sentence: An implementer who follows the stated text as written builds `--unattended` for `/sc:troubleshoot`, `/sc:cleanup-audit` and `/sc:index-repo` with no output flag, and WC-4 then makes every such run write nothing and end `failed`, because the same text says the brief passes no output directory (troubleshoot, index-repo) or no contract location exists (cleanup-audit). Acceptance criterion AC-1.2 cannot pass against flags that do not exist.
- The two stated texts that contradict each other:
  - WC-4 (spec:62): the contract is at `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)", and "If the required output path is missing the command writes nothing and the worker ends `failed`". WC-4 also requires the path "known before dispatch" (spec:62, 73).
  - Section 3.1 (spec:85-86, 91): index-repo "Brief must pass: none"; cleanup-audit brief passes only `--pass <N>` and its output dir "is fixed"; troubleshoot brief passes "no `--fix`" and reports `REPORT.md`. None of the three rows adds an output flag or says where the contract goes. The only "small fix" for index-repo is "State the output location" (spec:86); the only fix for troubleshoot is the P2 gate conversion (spec:91).
- Further evidence of the conflict:
  - WC-6 (spec:64) names troubleshoot as having "no output flag" and points the brief at "its timestamped default directory" (`cmd/troubleshoot.md:56`, UNVERIFIED here), then says the coordinator "makes new for every attempt (WC-4)". A timestamped default cannot be named in a brief before dispatch.
  - AC-1.2 (spec:196) runs "each P1 command other than `load` with `--unattended --output <dir>`". P1 contains index-repo and cleanup-audit (spec:159), which per spec:86 and 85 have no `--output`. The P1 scope sentence "output flags for commands that lack one" (spec:159) hints at adding them, but section 3.1 and WC-11 (spec:69, "the fixed paths of cleanup-audit and index-repo") say the opposite: fixed paths, no flag.
  - AC-1.2 also passes `<dir>` to init-lite, whose flag takes a file (spec:62, 87).
  - Inventory support: `INV-B:242` (troubleshoot has `return-contract.yaml` only with `--caller task-unified`); `INV-A:42` and `INV-A:53` (cleanup-audit and index-repo write to fixed locations).
- Concrete attack (state trace): before: troubleshoot has no output flag; brief = `/sc:troubleshoot "login fails" --unattended` (the 3.1 brief plus the flag). Step: the command looks for `<output-dir>`, finds none. After: per WC-4 it writes nothing and the worker sends `worker_done --outcome failed` (WC-5: "no readable report exists"). The coordinator sees a failed Task for a diagnosis that may have completed and produced `REPORT.md`.
- Recommendation: for each of troubleshoot, cleanup-audit, index-repo, either add an output flag in the phase that gives them `--unattended` (and say so in their 3.1 row), or define the contract location as a fixed, documented path next to the existing fixed report. Make AC-1.2 and WC-6 consistent with the choice (and say file versus directory for init-lite).

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The decision (Orca coordinates, commands stay units of work, spec:13-39) is internally consistent and its inventory and capability citations check out. The architecture findings below are all Medium.

## Follow-up candidates (Medium and minor; none blocks)

Medium (warnings, not part of any Reviser brief):

- M-1 (Fowler, Nygard). A blocked worker is answered by "starting a new Task" (WC-3, spec:61), but a failed Task keeps its dependents blocked until a `--retry-of` replacement completes it (`CAPS:90`, `CAPS:142-144` via `CAPS:90`; `[G:recovery]` lines 142-144). The spec's own DAG advice (spec:39, 136) relies on dependents. Only the retry route in WC-6 (spec:64) reopens the Task. Needs the guess that the DAG has dependents. Suggested direction: say that a blocked Task is answered with `worker-start --retry-of`.
- M-2 (Newman, Hohpe). The spec never says whether `--unattended` propagates to commands that other commands invoke. It states the rule only for tasklist-to-reflect (spec:122). Other nested calls: brainstorm to adversarial (`INV-A:39`), release-split to brainstorm and adversarial (`INV-B:119`), cli-eval to spec-panel and adversarial (`INV-A:44`), task to troubleshoot (`INV-B:201`), workflow to reflect (`INV-B:269`). Nested contracts could also collide with the parent's `<output-dir>/return-contract.yaml` (WC-4). This is a requirement the document never states.
- M-3 (Nygard, Crispin). WC-10 triggers at "longer than 5 minutes" and splits to "at most 4 minutes" (spec:68), while the pr-submit row and AC-4.3 use 4 minutes and 240 s (spec:114, 210) and the Decisions row says 4 minutes is the margin (spec:266). A call of 4 to 5 minutes satisfies WC-10 and fails AC-4.3. Pick one threshold.
- M-4 (Wiegers). New output flags (spec:99-125, "add `--output`") do not say whether they take a directory or a file, while WC-4 handles the two cases differently (spec:62). The implementer picks the worse reading in some commands. Name file or directory per row.
- M-5 (Crispin). WC-4 requires `version` `1` and keeps existing fields (spec:62), and AC 7.2 step 4 asserts `d['version'] == 1` (spec:183). The workflow contract is "contract 1.1" (`INV-B:272`). If its version field is 1.1, the check fails. Field name and type are not shown in the inventory, so the grade stays Medium.
- M-6 (Fowler). SA-4 and AC-C5 check additivity of command files only (spec:149, 176). Most gate logic lives in skill files (every section 3 evidence cell cites `sk/...`), so skill edits that alter standalone behaviour (SA-1) have no mechanical check.
- M-7 (Hightower). Section 1.4 (2) states that a command's own question comes "after readiness, so it does not fail `worker-start`" (spec:44). The cited evidence says the Claude task is passed on the command line (`CAPS:47`) and readiness waits for the input box (`CAPS:47-49`), so a command that asks in its first turn may still fail readiness. The README states the failure more broadly (`README.md:14`). Treat the claim as UNVERIFIED. No requirement depends on it, because WC-2 forbids the prompt either way.
- M-8 (Newman, Fowler). Each command's `## Unattended mode` points at `~/.claude/WORKER-CONTRACT.md` and "lists only its own gate resolutions" (spec:52). There is no stated behaviour when the installed contract file is missing in a project where the commands were installed from an older release.
- M-9 (Fowler). The tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (spec:122, citing `INV-A:14`). Inventory B instead recommends running it at the worker's top level and marks nested spawning UNVERIFIED (`INV-B:210, 215, 322`). The spec adopts the optimistic reading without recording the disagreement.
- M-10 (Gregory). AC-C1 (spec:172) greps for four `orca` subcommands (`orchestration`, `worktree`, `terminal`, `agent`), while SA-2 (spec:147) forbids any `orca` or `orca-ide` command. For example `orca status` and `orca open` pass the grep.
- M-11 (Cockburn). Section 6 says "Phases 1-3 need no user decision" (spec:154), but D4 affects P2 rows (auggie-review `--post-pr`, task `commit`/`push`, spec:100, 121, 244) and D1 affects every phase. Section 9 clarifies that phases 0 to 3 proceed on the recommendations (spec:225). Reword one of the two statements.
- M-12 (Nygard). D2 option (b) has the coordinator answer the worker's `ask` (spec:235), but WC-3 says a command gate ends the run as blocked and the worker never re-invokes the command (spec:61). The mechanism for (b) is undefined, so (b) is not implementable as written; (a) is the recommendation.

Minor notes:

- m-1. Section 4 justifies `/sc:git` by "the user's authorization in this repo" and cites `README.md:31` (spec:133, also 67). That README line is a rule for this planning run's workers, not a standing repo policy.
- m-2. Section 2.1 calls the flag "the only command-side change the contract asks for besides report files and resume" (spec:51), yet WC-9, WC-10 and section 3 also ask for wait splitting, tool additions (explain) and a frontmatter move (business-panel).
- m-3. If D3 (a) is accepted, pr-submit leaves the worker list, so the headline counts become 26 / 7 in effect (spec:76, 139). The spec notes the dependence only in section 4.
- m-4. WC-1 says "well inside the readiness limit" without a number (spec:59), although the evidence it cites gives about 45 s as the failure point and 30 s as a passing fallback (`EVIDENCE.md:45,56` via `CAPS:49`).
- m-5. UNVERIFIED claims the spec itself labels, correctly: `CAPS:103` (call sites of the depth check), `CAPS:178` (report-path checking). No action beyond keeping the labels.

Follow-up issue question: the command asks the running session to ask the user once whether to open an issue for the Medium and minor items above. This run has no user channel (sandbox), so the question was not asked and no issue was created.

## Cross-expert consensus and disagreements

- Consensus: the decision and the evidence base are sound and the citations to the capability inventory are accurate; the single blocking defect is a requirements-versus-matrix contradiction, not an architecture error.
- No expert disagreement worth recording. Whittaker's attacks that did not produce a finding: Sentinel Collision on `status` values (WC-5 covers missing and unknown values), Accumulation on retries (circuit breaker, `CAPS:116`), Sequence on `check` before `worker_done` (WC-12 covers `consumer_fenced`).

## Reviser brief

Blocking finding ids only: **B-1**.

Rules for the reviser (restated from the command's Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text that B-1 names (WC-4 at spec:62, WC-6 at spec:64, the three 3.1 rows at spec:85, 86 and 91, and AC-1.2 at spec:196).
- Add no rule, mechanism or section that B-1 does not call for. Cite finding id B-1 on every added paragraph or table cell.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted for B-1.
- Leave all Medium and minor items alone, including "apply all findings" style instructions.
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
