review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (spec-panel, critique mode)

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, a labelled whole-document audit, first review.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 287 lines, sha256 `cbaee912425ccadcbc06bd6c2dd562fc87afea9b7b20dc55342bb7c482b347f0`.
- Baseline: none given. Prior report: none given. This is a first review of the full document.
- Reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`).
- Prompt followed: FIRST-REVIEW prompt and grading check in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full. No brief clause was overridden.
- Citation keys: `SPEC:N` = the candidate, line N. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = the spec-panel definition used for this run.

## Coverage
- Read in full: the candidate, the README, all three inventories, and the command definition.
- Checked: every `INV-A`, `INV-B` and `CAPS` line reference in the candidate that I spot-checked against the inventory line it names. Checked: the 10 / 27 / 6 split (`SPEC:76`). It matches `INV-A:73` (5 / 13 / 3) and `INV-B:278` (5 / 14 / 3). The 3.1 table has 10 rows (`SPEC:83-92`), the 3.2 table has 27 (`SPEC:99-125`), and the P2 command list (15, `SPEC:160`) equals the P2 rows of section 3.
- UNVERIFIED (not checkable in the sandbox): every citation into `src/superclaude/{commands,skills,agents,core,cli}`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `tests/`, `EVIDENCE.md`, `.dev/codegraph-migration/**`, `/opt/Orca/**` and the Orca guide output. I treated them as claims carried by the inventories, not as verified facts. This includes the spec's own "re-read 11 locations" (`SPEC:11`) and the grep result at `SPEC:25`.
- Not covered: behavior of the Orca runtime, and whether any slash command runs correctly as a worker. No run was possible.

## Verdict summary
No finding meets the blocking test. The spec contradicts neither its inventories nor itself in a way that holds with no further assumption. It has no stated text that does data loss or breaks a security boundary. Eleven findings are Medium (they depend on a guess about which of two readings an implementer picks, or on a requirement the document never states). They are listed under `follow-up candidates`.

## Guard Condition Boundary Table
Trigger: the spec contains threshold checks, boolean guards and sentinel comparisons (readiness limit, heartbeat and wait sizes, depth, status mapping, authorization flags, acceptance regexes). Pipeline Dimensional Analysis does not trigger: the Task to worker to `worker_done` chain is 1:1:1 (`SPEC:63`, `CAPS:76`) and no stage changes a count that a downstream consumer assumes. `--focus correctness` is not active, so no State Variable Registry is produced.

Classes left out, with one-line reasons: the Maximum/Overflow class is omitted for GC-1, GC-2, GC-6, GC-7 and GC-8 because those guards take no count or size input; the Sentinel class is omitted for GC-4 because no reserved value exists.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GC-1 outcome mapping | SPEC:63 (WC-5) | Zero/Empty | no report file, or empty or unparseable file | no report: true; empty: unspecified | "no report exists" gives `failed`; an existing but empty or unparseable file is not addressed (`SPEC:63`, `SPEC:183` only catches it in a test) | GAP (F-11) |
| GC-1 | SPEC:63 | One/Minimal | contract with only required fields, `status: succeeded` | false | `--outcome succeeded` | OK |
| GC-1 | SPEC:63 | Typical | `status: failed` | true | `--outcome failed` | OK |
| GC-1 | SPEC:63, SPEC:62 | Sentinel Value Match | `status` outside the four-value set, kept from an existing contract ("keep their fields") | unspecified | not addressed | GAP (F-11) |
| GC-1 | SPEC:63 | Legitimate Edge Case | `partial`; an audit with verdict FAIL | false | `succeeded`, status and verdict named in the first body sentence | OK (see F-5 for what `succeeded` does to dependents) |
| GC-2 contract location | SPEC:62 (WC-4) | Zero/Empty | no placing flag (research, recommend, review-translation, task, save), or cleanup-audit and index-repo whose rows name no contract path | true | WC-4 says the coordinator reads the path from `worker_done --report-path`; the command's own placement rule is not stated | GAP (F-3) |
| GC-2 | SPEC:62 | One/Minimal | `--output` is a file in a directory of its own | file | contract in the file's directory | OK |
| GC-2 | SPEC:62 | Typical | `--output-dir <dir>` | directory | `<dir>/return-contract.yaml` | OK |
| GC-2 | SPEC:62, SPEC:64 | Legitimate Edge Case | retry worker with the same `--output <dir>` | directory | WC-6 says fresh output directory, WC-4 says the directory passed; who creates the new path is not stated | GAP (F-3) |
| GC-3 ask once | SPEC:61 (WC-3) | Zero/Empty | worker session holds no preamble | false | gate resolves blocked, no `ask` (`SPEC:60`) | OK |
| GC-3 | SPEC:61 | One/Minimal | one gate hit | true | one `ask`, re-invoke with the answer as a flag | OK |
| GC-3 | SPEC:61, SPEC:105 | Maximum/Overflow | a second gate in the same run (cli-portify has three, review-translation two: `SPEC:105`, `SPEC:117`) | unspecified | "ask the coordinator once" does not say whether once per run or per gate | GAP (F-5) |
| GC-3 | SPEC:61 | Legitimate Edge Case | `ask` times out | true | resume the same message ID, no duplicate | OK |
| GC-4 wait split | SPEC:68 (WC-10) | One/Minimal | one tool call under 4 minutes | false | no change | OK |
| GC-4 | SPEC:68 | Typical | foreground poll plus sleep | false | pr-submit iterations checked (`SPEC:114`) | OK |
| GC-4 | SPEC:68, SPEC:104 | Maximum/Overflow | eval up to 3600 s | true | cli-eval splits into waits of at most 4 minutes (`SPEC:104`) | OK |
| GC-4 | SPEC:68 | Maximum/Overflow | one Agent-tool call that runs longer than 5 minutes (tdd, cleanup-audit, adversarial fan-out: `INV-A:35`, `INV-A:42`, `INV-B:47`) | true | rule says "a single tool call" but only cli-eval and pr-submit are assigned a change | GAP (F-6) |
| GC-4 | SPEC:68 | Legitimate Edge Case | a wait of 4 to 5 minutes | false | neither required nor forbidden; harmless | OK |
| GC-5 readiness | SPEC:59 (WC-1) | Zero/Empty | no startup prompt | false | passes | OK |
| GC-5 | SPEC:59 | Typical | 30 s fallback | false | passes (`CAPS:49`) | OK |
| GC-5 | SPEC:59 | Legitimate Edge Case | fallback above 45 s | true | evidence says it fails again (`CAPS:49`) but WC-1 only says "well inside" 60 s, no number | GAP (M-5, minor) |
| GC-6 outward default | SPEC:67 (WC-9) | Zero/Empty | no authorizing flag in the brief | true | action off | OK |
| GC-6 | SPEC:67, SPEC:100, SPEC:121, SPEC:113 | Legitimate Edge Case | brief authorizes through "the command's own explicit flag" | unspecified | the flag is not shown to exist for auggie-review `--post-pr`, task `commit`/`push`, post-release; "paid external run" is undefined | GAP (F-4) |
| GC-7 additive-edit check | SPEC:176 (AC-C5) | Typical | removed table row or prose line | true | printed, check fails | OK |
| GC-7 | SPEC:176 | Legitimate Edge Case | removed markdown bullet `- text` | false | diff shows `-- text`, regex `^-[^-]` does not match, check passes | GAP (F-2) |
| GC-8 stall check | SPEC:181 (7.2 step 2) | Zero/Empty | `agentWait` field absent | unspecified | "never non-null" passes, yet an absent field means Orca never looked (`CAPS:129`) | GAP (M-4, minor) |
| GC-8 | SPEC:181 | Typical | `agentWait` non-null | true | fail | OK |
| GC-9 depth | SPEC:66 (WC-8) | Typical | depth 1, worker calls `worker-start` | true | forbidden, refused by Orca (`CAPS:97-101`) | OK |
| GC-9 | SPEC:66, SPEC:253 | Legitimate Edge Case | user raises depth (D5 b) | true | WC-8 still forbids | OK |

Every GAP above is Medium or minor under the FR-8/FR-9 grading rule: none names a stated text that causes a concrete wrong outcome, they name a requirement the document does not state. None blocks synthesis.

## === REQUIREMENTS ANALYSIS ===

Experts: Wiegers (lead), Adzic, Cockburn. All findings are graded by consequence. Label is the expert's label; Grade is the grading-check result.

### F-1: Phase 1 scope is stated three ways, and AC-1.1 only passes under one of them
- Expert: Wiegers. Label: MAJOR. Grade: Medium. Priority: High. Quality impact: Consistency, Testability.
- Stated texts: the P1 row says the `--unattended` flag is "accepted by every command in sections 3.1 and 3.2" and the WC-4 contract is written in unattended mode, yet its Commands cell lists only nine commands plus four fixes (`SPEC:159`). The Phase column of section 3 puts roadmap, save, validate-roadmap and validate-tests in P3 and implement, post-release and pr-submit in P4 (`SPEC:112-125`). Section 3.1 says "The only command changes are the small fixes in the last column", and brainstorm and init-lite have "None" (`SPEC:79`, `SPEC:84`, `SPEC:87`). Yet AC-1.1 requires every command in 3.1-3.2 except load to have a `## Unattended mode` section naming `return-contract.yaml` (`SPEC:195`), and `SPEC:76` adds the section to "every changed command".
- Grading check: an implementer who follows the P1 Commands cell builds sections in about 13 commands, and AC-1.1 fails for the other 23. An implementer who follows the scope sentence and AC-1.1 builds a section in all 36 commands in P1, including commands whose gates arrive only in P2 (auggie-review posts to GitHub by default, `INV-A:38`). That second build accepts `--unattended`, WC-9 says the posting default is off under `--unattended` (`SPEC:67`), and the gate conversion is P2 (`SPEC:100`), so a coordinator that follows section 2.3 ("including `--unattended`", `SPEC:73`) between P1 and P2 gets a posting worker. Which reading the implementer picks is a guess, so Medium.
- Recommendation: say which commands get the section and flag in P1, and say that a coordinator must not put `--unattended` in a brief for a command until that command's phase has passed. Restate AC-1.1 for that set.

### F-4: WC-9 authorization mechanism is not defined for the commands that need it
- Expert: Wiegers. Label: MAJOR. Grade: Medium. Priority: Medium.
- WC-9 says an outward default "turns on only through the command's own explicit flag written in the brief" (`SPEC:67`). The auggie-review row relies on "an explicit `--post-pr`" (`SPEC:100`) and D4 names it (`SPEC:245`), but the inventories show only `--no-post-pr` and `--remediation-offer` (`INV-A:38`); `--post-pr` is not shown to exist, and the row's "Other required change" is none. For task, the `commit`/`push` keywords are refused "unless authorized" (`SPEC:121`) and for post-release, VM, install, commit and PR are off "unless the brief authorizes them" (`SPEC:113`), with no flag named for either. "Paid external run" is undefined, and research (Tavily, `INV-B:134`), review-translation (Tavily, `INV-B:144`) and `/sc:recommend --plugin` (web search, `INV-B:104`) are not classified.
- Grading check: the text does not say how a brief authorizes the action, so the implementer must invent a flag or refuse always; the worse of two allowed readings is "refuse always" or "any flag text counts". Guess needed, so Medium.
- Recommendation: list, per outward action, the exact flag (existing or to be added) and define "paid external run" in one sentence.

### F-9: tasklist still has a person-blocking HALT after the stated change
- Expert: Adzic. Label: MAJOR. Grade: Medium. Priority: Medium.
- The tasklist row resolves the reflect offer by passing `--unattended` to each reflect (`SPEC:122`). The inventory records a second stop: `needs_human_decision` items HALT at Stage 10.5 (`INV-B:209`, citing `SKILL.md:1631`). Neither the row nor AC-2.2b (`SPEC:201`) covers it; AC-2.2b checks only that tasklist "passed `--unattended` to reflect". WC-2 says no step may wait on a person (`SPEC:60`).
- Grading check: an implementer who builds the row as written leaves the HALT, and a worker can stall at Stage 10.5 with no `worker_done`. Whether reflect's headless rule skips `needs_human_decision` is not established (`INV-B:109` says it "skips the gates" for auto-fixable registers). Guess needed, so Medium.
- Recommendation: add the `needs_human_decision` case to the tasklist row as a blocked or default resolution, and add it to AC-2.2b.

### F-10: Commands that "never use `--interactive`" are not made safe under `--unattended`
- Expert: Cockburn. Label: MINOR-to-MAJOR. Grade: Medium. Priority: Low.
- WC-2 is absolute: under `--unattended` the command never calls `AskUserQuestion` (`SPEC:60`). For cleanup, improve and roadmap the rows refuse `--interactive` (`SPEC:103`, `SPEC:110`, `SPEC:118`). For adversarial, brainstorm and release-split the 3.1 rows only say the brief must "never" pass `--interactive` (`SPEC:83`, `SPEC:84`, `SPEC:89`), and adversarial's `--interactive` adds 4 `AskUserQuestion` checkpoints (`INV-A:35`). A brief that passes both flags is undefined.
- Grading check: this is a missing restriction, not a stated text that does harm, so Medium.
- Recommendation: one sentence in WC-2: `--interactive` together with `--unattended` is refused for every command.

### F-11: Existing contract schemas and the fixed status set are not reconciled
- Expert: Wiegers. Label: MAJOR. Grade: Medium. UNVERIFIED (the existing schemas are not in the sandbox). Priority: Medium.
- WC-4 says commands with a contract "keep their fields and add the missing ones" and fixes `status` to `succeeded|partial|failed|blocked` (`SPEC:62`); the decision table confirms the fixed set (`SPEC:263`). The inventories show contracts already exist for workflow, reflect, brainstorm, adversarial and, under `--caller task-unified`, troubleshoot (`INV-B:272`, `INV-B:112`, `INV-A:97`, `INV-B:242`), and the spec never lists their `status` values. AC step 4 asserts membership in the four-value set (`SPEC:183`), and GC-1 shows WC-5 has no rule for a value outside it or for an empty file.
- Grading check: if an existing contract uses a different word, "keep their fields" and the test cannot both hold. The inventories do not say whether they do, so Medium.
- Recommendation: add a one-line table of the current `status` values per existing contract, or state that a legacy value maps to one of the four.

## === ARCHITECTURE ANALYSIS ===

Experts: Fowler (lead), Newman, Hohpe, Nygard.

### F-3: Where `return-contract.yaml` goes is undefined for several commands, and WC-4 and WC-6 disagree on retries
- Expert: Fowler. Label: MAJOR. Grade: Medium. Priority: High. Quality impact: Completeness, Consistency.
- WC-4 says a row that names no location or no placing flag overrides the default and the coordinator "reads it from `worker_done --report-path`" (`SPEC:62`). But the rows for cleanup-audit (`SPEC:85`), index-repo (`SPEC:86`), research (`SPEC:116`), recommend (`SPEC:115`), review-translation (`SPEC:117`), task (`SPEC:121`) and save (`SPEC:119`) name a report but not where the contract is written. 7.2 step 4 requires `test -s <contract>` at "the contract path WC-4 gives for that command" (`SPEC:183`, `SPEC:182`), which WC-4 does not give for these seven.
- Retry: WC-6 says a command without a resume flag "writes each run into a fresh output directory" (`SPEC:64`), WC-4 puts the contract in the directory the coordinator passed (`SPEC:62`), and section 2.3 does not say the coordinator passes a new directory on a retry (`SPEC:73`). The 23 "fresh dir" rows depend on this.
- Grading check: if the coordinator retries with the identical brief and `--output <dir>`, the command writes into `<dir>` (WC-4) and overwrites the first attempt's contract and report; if the command creates a subdirectory (WC-6), the path in WC-4 is wrong. The text allows both readings, so Medium.
- Recommendation: add to 2.3 "on `--retry-of` the coordinator passes a new output directory", or state that the command creates `<dir>/<run-id>/`. Name the contract location for the seven rows.

### F-5: What the Task and its dependents do with `blocked` and `partial` is not specified
- Expert: Nygard. Label: MAJOR. Grade: Medium. Priority: High. Quality impact: Completeness.
- WC-5 maps `blocked` and `failed` to `--outcome failed` and `partial` to `succeeded` (`SPEC:63`). Orca keeps dependents of a failed Task blocked until a `--retry-of` replacement completes it (`CAPS:90`, `CAPS:116`), and a completed Task makes its dependents "ready" (`CAPS:84-86`). Section 2.3 says only that the coordinator "opens the report file, then releases or reuses the worker" (`SPEC:73`). It gives no rule for answering a `blocked_question`, for starting the replacement worker with the answer as a flag, or for holding dependents when the upstream report says `partial`. WC-3 also says the worker "may ask the coordinator once" (`SPEC:61`), which GC-3 shows is ambiguous for a command with several gates (cli-portify has three, review-translation two).
- Grading check: following the text, a coordinator that reads Orca's ready view starts the `/sc:implement` Task after a `partial` `/sc:tasklist` run, and a coordinator that sees `blocked` has no stated next step. Whether it opens the report first is covered by 2.3, so the harm needs the coordinator to skip a step. Medium.
- Recommendation: add two lines to 2.3: a `blocked` report is answered by a `--retry-of` worker whose brief carries the answer, and dependents of a `partial` upstream start only after the coordinator has read the report's status. Say whether "once" means once per gate.

### F-6: WC-10 states a general rule but assigns it to two commands
- Expert: Hohpe. Label: MAJOR. Grade: Medium. Priority: Low. Quality impact: Consistency.
- WC-10 applies to "a command step that blocks a single tool call for longer than 5 minutes" (`SPEC:68`). The only changes assigned are cli-eval (`SPEC:104`) and pr-submit (`SPEC:114`). Agent-tool fan-out is a single blocking call too, and the inventories show long fan-out in tdd, cleanup-audit and adversarial (`INV-B:47`, `INV-A:42`, `INV-A:35`). These cannot be split into 4-minute waits. The need for heartbeats rests on this worker's own preamble, and whether Orca uses heartbeat age is UNVERIFIED (`CAPS:130`, `SPEC:283`).
- Grading check: the text cannot be met by tdd, and no stated outcome is wrong, since heartbeat cadence has no verified effect. Medium.
- Recommendation: narrow WC-10 to polling and sleep waits, or state that a blocking Agent-tool call is exempt.

### F-7: Gates that live in skills are resolved only in command files
- Expert: Fowler. Label: MAJOR. Grade: Medium. Priority: Medium.
- The spec adds a `## Unattended mode` section to each command (`SPEC:52`) and limits SA-4 and AC-C5 to command files (`SPEC:149`, `SPEC:176`). The gates the section overrides are in skills (for example review-translation `SKILL.md:76` "STOP AND WAIT", release-split `SKILL.md:88,175`, roadmap `SKILL.md:435`, per the evidence cells at `SPEC:89`, `SPEC:117`, `SPEC:118`). The spec does not say that the command section takes precedence over a skill's blocking text, nor that skill files are edited and checked.
- Grading check: an implementer who adds only the command section leaves the skill text "MUST receive confirmation" in place, and which instruction the model follows is not stated. AC-2.2 would catch this at P2, but only after the fact. Medium.
- Recommendation: state the precedence rule in the contract file, and extend SA-4 and AC-C5 to the skill files the rows cite.

### F-8: How a worker invokes the command is not stated
- Expert: Newman. Label: MAJOR. Grade: Medium. UNVERIFIED. Priority: Medium.
- E2 says a command run by a worker has the same tools as one a person runs (`SPEC:22`), and WC-7 says the worker "runs the command directly in its own session" (`SPEC:65`). The only direct evidence is a return contract with `invocation_method: "skill-direct"` (`SPEC:23`, `INV-A:13`), while section 1.4 says that run used an Agent-tool subagent (`SPEC:43`). The spec does not say whether the command line in the brief is typed as a slash command at the start of a message or loaded through the Skill tool, or what happens to the 13 commands with no skill (`INV-A:70`) and to `$ARGUMENTS` when the Orca preamble precedes the command text. CAPS:47 says the task is passed on the command line for Claude.
- Grading check: this is a mechanism the spec leaves open. AC-0.4 (`SPEC:194`) is built to find out, so the harm is limited to P0 rework. Medium.
- Recommendation: add the invocation method to 2.3 as an explicit P0 question, with the expected answer.

## === ADVERSARIAL ANALYSIS ===

Expert: Whittaker (active in every panel review; attacks in the FR-3 template). Severity labels: CRITICAL / MAJOR / MINOR; Grade is the result of the grading check.

### F-2: AC-C5 cannot detect a deleted markdown bullet
- I can break this specification by **Sequence/Accumulation Attack (check run after a deletion)**. The invariant at **SPEC:176 (AC-C5), restated by SA-4 at SPEC:149 and SA-1 at SPEC:146** fails when **a phase deletes or rewrites a bullet line in a command file**.
- Concrete attack: before, `cmd/cleanup.md` contains the line `- Approval Required (prompts user first) ...` (the format used by command files, for example `CMD:471-481`). The phase removes it. `git diff -U0` prints `-- Approval Required ...` for the removed line. The check is `grep -E '^-[^-]'`: character 1 is `-`, character 2 is `-`, so `[^-]` fails and the line does not match. The command prints nothing, so the check reports "additive", while a standalone gate has been deleted. The same holds for an edited bullet (the old line is dropped from the output, the new one is `+`).
- Severity: MAJOR. Grade: Medium. The defect is in an acceptance check, not in a stated text that causes harm, and AC-2.5 (`SPEC:204`) is a manual standalone check. Priority: Medium. Quality impact: Testability.
- Recommendation: use `grep -E '^-([^-]|-[^-]|$)'` after dropping the `--- a/` header line, or compare with `git diff --numstat` deletions equal to 0.
- Related, minor: AC-C1 (`SPEC:172`) is case-sensitive, so the uppercase `ORCA orchestration` form that the Orca guides use does not match, and the `\|` in the raw cell is a literal pipe in ERE if copied from the raw file. And AC-C1 scans `src/superclaude/core`, where P0 adds the Orca section to `HOW-WE-WORK.md` (`SPEC:158`, `SPEC:150`); SA-2 allows a mention of Orca in the contract file (`SPEC:147`) but AC-C1 does not exempt it. If either file names `orca orchestration ...`, P0 fails its own common check. Guess needed.

## Minor notes
- M-1: the document refers to tags `M1` to `M6` (`SPEC:62`, `SPEC:73`, `SPEC:76`, `SPEC:112`, `SPEC:182`, `SPEC:194-196`, `SPEC:200-201`) and to "ladder rung 2" (`SPEC:262`) that it never defines. They point to a revision log that is not part of the document.
- M-2: the command count of 43 is the sum of the two inventory scopes (`SPEC:76`, `INV-A:3`, `INV-B:3`), not a directory listing, so nothing in the workspace proves the set is complete. UNVERIFIED: the reviewing session's own installed `sc:` skill list also names `sc:graph`, `sc:impact` and `sc:issue`, which neither inventory covers; `sc:issue` is described there as creating an Orca worktree, which would contradict E5 (`SPEC:25`) and the AC-C1 baseline. This is from the session listing, not from a workspace file, and is not graded.
- M-3: section 1.4 point 2 says a command's own `AskUserQuestion` "does not fail `worker-start`" (`SPEC:44`). The cited lines only say a worker waiting after `input_accepted` is healthy (`CAPS:52`, `CAPS:129`), and the task text is passed on the command line for Claude (`CAPS:47`), so whether a first-turn prompt can block readiness is not evidenced. WC-2 forbids the prompt either way.
- M-4: 7.2 step 2 passes on an absent `agentWait` (`SPEC:181`, `CAPS:129`), and step 5 searches the transcript for the string `AskUserQuestion`, which can also appear in loaded command text (`SPEC:184`). Both can give a vacuous pass or a false fail.
- M-5: WC-1 says a fallback must be "well inside" 60 s without a number, while the evidence shows failure above about 45 s under a 45 s limit (`SPEC:59`, `CAPS:49`).
- M-6: the index row asks the command to state that knowledge-base mode "does not wait", while the same row says whether it waits is UNVERIFIED (`SPEC:111`). The text should require the mode to be refused or pinned, as the business-panel and explain rows do.
- M-7: section 1.1 says one worker runs one command (`SPEC:16`), and the load row says to use it as a step inside another worker's brief (`SPEC:112`).
- M-8: AC-0.4 says "no Agent-tool wrapper, verified in the step-5 transcript" (`SPEC:194`), but step 5 states only the `AskUserQuestion` search (`SPEC:184`).

## Cross-expert consensus
- Consensus: the decision (Orca coordinates, commands stay units of work) is supported by the inventories (`SPEC:18-26`, `INV-A:94-98`, `INV-B:289-299`). The rejected alternative is reasoned from Orca facts that the capabilities inventory marks Verified (`CAPS:97-103`, `CAPS:145-150`). The spec states its main evidence gap openly (`SPEC:41-45`).
- Disagreement: Wiegers and Nygard rate F-1 and F-5 as the findings most likely to cause rework in implementation. Fowler and Newman rate F-3 and F-7 higher because they affect every command. None changes the verdict under the grading check.

## follow-up candidates
Medium (warnings, none blocking): F-1, F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10, F-11, and the AC-C1 related note under F-2.
Minor notes: F-2 (the AC-C5 regex, graded Medium as an acceptance-check defect; listed here once), M-1 to M-8.
Whether to open an issue for these: not asked. This run is a worker with no user channel, so the list is recorded only.

## Reviser brief
No blocking finding is open, so there is nothing to revise. Restated contract for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are never in this brief and never trigger a revision.

verdict: PASS
