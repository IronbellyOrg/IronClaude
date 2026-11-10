review: 1 of 3

# Gate review: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt followed: GATE prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md:57-64`) with the FIRST-REVIEW grading check (`:35`). This is a first review of a complete document; no prior rounds exist. `--re-review` and `--baseline` were not given, so `baseline: not applicable (first review)`.
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `f3f06d442b7ecafec248d6a15af6b7f95431da195ed53de987f98ee1119f1751`
- Reviewer model actually used: claude-sonnet-5-5
- Mode: critique. Focus: requirements, architecture. Experts: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, active in every panel, `command.md:70-85`).
- Hard gate read: `~/.claude/rules/prompts/document_review_loop_prompts.md` was read in full before the review; `command.md` was read in full.

Citation keys. `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` (all read in full). `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = `command.md`. Any `src/...`, `~/.claude/skills/...`, `pyproject.toml` or `/opt/Orca/...` line the candidate cites that is not inside the workspace is UNVERIFIED here; where I rely on such a line it is only through an inventory line that quotes it.

## What I covered

Whole document (sections 1-9, Decisions, UNVERIFIED list). I checked: (1) the 10/27/6 split and the 43 count against the two inventories; (2) the phase lists against section 3 (P1 14 + P2 15 + P3 4 + P4 3 = 36 flag-bearing commands, plus `load` = 37 = 10 + 27); (3) each WC rule against the section 3 rows and the section 7 checks; (4) the `CAPS:` citations the Evidence column relies on; (5) the dependent text `command.md:455-465` (the `/sc:spec-panel` Unattended mode section) against the candidate's WC-4 and the spec-panel row. I could not run any `src/` check or any live Orca check; the candidate's own "re-read 11 locations" (`SPEC:11`) and "about 340 citations" (`SPEC:285`) claims are UNVERIFIED here. Counts reconcile; I found no count-conservation mismatch.

## Grading summary

No finding passed the grading check for blocking. For each candidate blocking finding I wrote the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." and kept it blocking only if it held with no further assumption. None did: each needed a guess between two readings the text allows, or is a requirement the document does not state. They are Medium and are listed under follow-up candidates. Minor findings are notes.

| id | grade | location | one line |
|---|---|---|---|
| R-1 | Medium | SPEC:62, 99-125 | WC-4 does not say whether a newly added `--output` is file- or directory-valued, or where the contract goes |
| R-2 | Medium | SPEC:63 | WC-5 maps an empty, unparseable or out-of-vocabulary report to `succeeded` |
| R-3 | Medium | SPEC:68, 114, 210 | WC-10 leaves a 4-5 minute gap that AC-4.3 and the pr-submit row forbid |
| R-4 | Medium | SPEC:194, 182 | AC-0.4 requires step 3 to match a contract that does not exist until P1 for troubleshoot |
| R-5 | Medium | SPEC:67, 113, 121 | WC-9 authorizes outward actions "through the command's own explicit flag", but post-release and task have none |
| R-6 | Medium | SPEC:61, 72-73, 200 | The brief (2.3) omits the ask-or-stop choice WC-3 leaves open; AC-2.2 assumes stop |
| R-7 | Medium | SPEC:51, 59-70 | No rule fixes how the unattended switch is matched, or what it does on a coordinator-only command |
| A-1 | Medium | SPEC:65-66, 118, 122 | No general rule for `--unattended` through nested invocations; only tasklist-to-reflect is handled; roadmap's nested `sc:save` is not |
| A-2 | Medium | SPEC:62, 69, 90 | Fixed contract name in a shared directory (tdd, init-lite file-valued `--output`) can be overwritten by a parallel worker |
| A-3 | Medium | SPEC:172, 147, 158 | AC-C1 scans `src/superclaude/core/`, where P0 adds the contract file and an Orca section that SA-2 allows to mention Orca |
| A-4 | Medium | SPEC:196, 83, 90-92 | AC-1.2 passes `--output <dir>` to commands whose rows give no such flag |
| A-5 | Medium | SPEC:64-69 vs 189-210 | WC-3, WC-6, WC-10 (outside pr-submit), WC-11 (outside save) have no acceptance check |
| A-6 | Medium | SPEC:122, 41-45 | The tasklist row states reflect nesting "inside Claude Code's nesting limit" as settled; INV-B marks it UNVERIFIED and recommends the opposite |

Minor notes are listed at the end.

=== REQUIREMENTS ANALYSIS ===

### R-1 (MAJOR label, Medium grade) WC-4 report-directory rule is not defined for the new output flags
- Expert: Wiegers (lead), Cockburn.
- Issue: WC-4 (`SPEC:62`) names the contract directory as `--output-dir`, a directory-valued `--output`, the directory of a file-valued `--output` for "(tdd, init-lite)" only, or the 3.1 row's directory for a command with no flag. Twenty-odd rows in 3.2 say only "add `--output`" or "add a report path" (`SPEC:99-125`, for example analyze `:99`, build `:101`, design `:106`, explain `:108`, spec-panel `:120`, test `:123`). They do not say whether the new flag is file- or directory-valued, so the contract location, which section 2.3 says the coordinator must know before dispatch (`SPEC:73`), is undefined for them.
- Dependency evidence that this is a live ambiguity: the existing `/sc:spec-panel` Unattended section chose a different flag, `--report-dir`, and states "`--output` is file-valued" (`CMD:460`), while the candidate's row says "add `--output`; contract" (`SPEC:120`).
- Grading sentence: "An implementer who follows the stated text builds a new `--output` for analyze as either a file or a directory, and the contract then lands in a place the coordinator did not expect." That needs a guess about which reading the implementer picks, and it is a requirement the document does not state. Medium.
- Recommendation: add one sentence to WC-4 fixing the form for every flag added in 3.2 (for example "a directory; the contract is `<dir>/return-contract.yaml`") and reconcile with `--report-dir` as the dependent command already uses it. Priority: High. Quality impact: Completeness +1, Testability +1.

### R-2 (Medium) WC-5 outcome mapping has an undefined branch for a bad report
- Expert: Wiegers, Nygard.
- Issue: WC-5 (`SPEC:63`): `--outcome failed` "when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise". An existing but empty, truncated, unparseable or out-of-vocabulary (not one of `succeeded/partial/failed/blocked`, `SPEC:62`) contract falls into "otherwise" and maps to `succeeded`. The Decisions row notes existing contracts keep their own fields (`SPEC:62`, `SPEC:261`), and the workflow contract's `status` vocabulary is not shown in either inventory (`INV-B:272`), so an out-of-vocabulary value is a real input.
- Grading sentence: "A worker that follows WC-5 as written sends `succeeded` for a zero-byte contract, and that is wrong because nothing reports success." This needs an input (a stub or truncated file) that the document does not say can occur; undefined edge case. Medium.
- Recommendation: add "or the report is unreadable or its `status` is not one of the four values" to the `failed` branch. 7.2 step 4 (`SPEC:183`) already checks this offline; make WC-5 agree. Priority: Medium.

### R-3 (Medium) WC-10 threshold and wait size leave a gap
- Expert: Wiegers, Nygard.
- Issue: WC-10 (`SPEC:68`) requires splitting only a step that blocks "longer than 5 minutes", into waits of "at most 4 minutes". A single call of 4 to 5 minutes is neither required to be split nor within the 4-minute maximum. The Decisions row says 4 minutes is chosen "to leave a margin under the 5-minute heartbeat cadence" (`SPEC:266`), the pr-submit row says "each single iteration ... stays under 4 minutes" (`SPEC:114`), and AC-4.3 fails any call over 240 s (`SPEC:210`). A cadence of 5 minutes (`CAPS:130`) with a 4.9-minute call leaves no margin.
- Grading sentence: "An implementer who follows WC-10 builds a 4.5-minute poll wait, and AC-4.3 fails it." That needs the implementer to pick the worse of two allowed readings. Medium. The consequence is bounded: absent heartbeats read as `unverifiable`, which never authorizes stop or release (`CAPS:125`).
- Recommendation: state one number: "no single blocking call longer than 4 minutes". Priority: Medium.

### R-4 (Medium) AC-0.4 cannot be satisfied literally for troubleshoot at P0
- Expert: Adzic, Wiegers.
- Issue: AC-0.4 (`SPEC:194`) requires 7.2 "steps 1-3 and 5-7" to pass and excuses only step 4 ("uses the command's existing report file"). Step 3 (`SPEC:182`) requires the `--outcome` to match "the contract's `status`" and the report path to be "the WC-4 contract path". At P0 troubleshoot reports `REPORT.md` and writes a return contract only with `--caller task-unified` (`INV-B:242`; `SPEC:91`, "Report today: REPORT.md"), and the spec itself says the worker "reports the named file until Phase 1 adds the contract" (`SPEC:79`). So step 3's clause has nothing to match for troubleshoot. AC-0.4 also says "a failure here reopens section 1".
- Grading sentence: "A literal executor marks P0 failed for troubleshoot and reopens the section 1 decision." The intent is recoverable from `SPEC:79` and AC-0.4's own step-4 note, so this needs a guess about reading; Medium.
- Recommendation: extend AC-0.4's exception to "steps 3 and 4 use the command's existing report file". Priority: High (the failure consequence is reopening the core decision). Quality impact: Testability +1.

### R-5 (Medium) WC-9 names a mechanism that two rows do not have
- Expert: Wiegers, Nygard.
- Issue: WC-9 (`SPEC:67`): an outward default "turns on only through the command's own explicit flag written in the brief". The post-release row (`SPEC:113`) says VM, real-target install, commit and PR are off "unless the brief authorizes them (open decision D4)", and the task row (`SPEC:121`) refuses EXEMPT `commit`/`push` "unless authorized (WC-9)". The inventories describe post-release's gates as confirmations "unless the user pre-authorized them this session" (`INV-B:79`) and task's `commit`/`push` as EXEMPT keywords in the prompt (`INV-B:204`), not flags. No flag named in the spec carries the authorization for either command.
- Grading sentence: not blocking, because the stated default is safe (off) and the failure is that the opt-in cannot be expressed, which is an unstated requirement. Medium.
- Recommendation: either name the authorization flag per command in P4 and P2 or add a generic `--authorize <action>` rule to the contract file. Priority: Medium.

### R-6 (Medium) The brief omits the ask-or-stop choice; AC-2.2 assumes stop
- Expert: Cockburn, Adzic.
- Issue: WC-3 (`SPEC:61`) says a worker holding a preamble "may instead ask the coordinator once" when a gate resolves as blocked. Section 2.3 (`SPEC:72-73`) lists what the brief states (command line, output directory, authorized actions, placement) but not whether the worker may ask. AC-2.2 (`SPEC:200`) expects `worker_done --outcome failed`, a blocked contract and no `agentWait`, and 7.2 step 3 waits on `question` events (`SPEC:182`). If the worker asks, the check sees a `question`, not a `worker_done`.
- Grading sentence: not blocking; "may" lets both outcomes pass depending on the worker, a guess about behavior. Medium.
- Recommendation: add "whether the worker may `ask` for blocked gates" to the 2.3 list and set it to "must stop" in the AC-2.2 brief. Priority: Medium.

### R-7 (Medium) The unattended switch has no matching rule and no behavior on excluded commands
- Expert: Whittaker (Sentinel Collision Attack), Wiegers.
- Whittaker finding: I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:51 and SA-1 (`SPEC:146`)** ("without `--unattended`, every prompt ... stays") fails when **the literal text `--unattended` appears inside quoted specification or prompt content that a person passes**, for example `/sc:spec-panel "review the --unattended section"`. Concrete attack: before, person-mode, gates on; the command matches `--unattended` as a substring, after, unattended mode on, `AskUserQuestion` suppressed and a `blocked` contract written in a plain session. The spec does not say the flag is a standalone argument token outside quoted content. The dependent command text does say it (`CMD:459`), which shows the rule is needed, but the candidate does not carry it.
- A second hole: section 4 says coordinator-only commands "get no `--unattended` mode" (`SPEC:128`) but not what `/sc:git --unattended` does (ignore, refuse). WC-2 and WC-9 depend on the answer for `git`.
- Grading sentence: undefined edge case, not a stated text that does harm. Medium.
- Recommendation: add to WC-2 or the contract file: "`--unattended` counts only as a standalone argument token outside quoted content; on a section 4 command it is refused." Priority: Medium.

=== ARCHITECTURE ANALYSIS ===

Overall the decision (Orca on top, commands unchanged units, a shared contract file, `--unattended`) is coherent and its evidence chain checks against the inventories: depth 1 and `nested_worker_depth_exceeded` (`SPEC:33` to `CAPS:97-103`), standalone breakage (`SPEC:34` to `CAPS:147-149`), `worker_done` bound to the dispatched pane (`SPEC:35` to `CAPS:76,150`), no Orca call in any primitive but ccsession-tag (E5, `SPEC:25`, grep result UNVERIFIED here). The gaps stated in 1.4 (`SPEC:41-45`) are honest.

### A-1 (Medium) No rule for composition: `--unattended` through nested invocations
- Expert: Fowler (lead), Hohpe.
- Issue: the contract has WC-7 (no subagent wrapping, `SPEC:65`) and WC-8 (no Orca fan-out, `SPEC:66`) but no rule that `--unattended` and the WC-2 resolutions propagate to a command's own nested `/sc:` or skill calls. Only tasklist-to-reflect is handled (`SPEC:122`). Others: roadmap writes memory "through `sc:save` at every wave" (`INV-B:154`, `INV-B:153`), and WC-11 forbids single-owner keys in unattended mode (`SPEC:69`), but the roadmap row (`SPEC:118`) does not say its nested save is per-session; cli-eval create runs `/sc:spec-panel` and adversarial (`INV-A:44`); brainstorm and release-split nest adversarial and brainstorm (`INV-A:39`, `INV-B:119`); tdd nests `/task` (handled in the tdd row, `SPEC:90`). The dependent spec-panel text says "Nested invocations. None." (`CMD:464`), so the section exists as a per-command slot the spec never describes.
- Grading sentence: not blocking; whether the nested call prompts depends on nested flags the inventories mostly mark default-off. Medium.
- Recommendation: add one WC line: "a command passes `--unattended` to every nested `/sc:` call that accepts it, and lists each nested call in its `## Unattended mode` section", and check roadmap's nested save against WC-11 in P3. Priority: Medium.

### A-2 (Medium) Fixed contract name in a shared directory
- Expert: Newman, Nygard.
- Issue: WC-4 puts `return-contract.yaml` in the directory of a file-valued `--output` for tdd and init-lite (`SPEC:62`, `SPEC:87`, `SPEC:90`). The default tdd output is `docs/[domain]/TDD_[COMPONENT].md` (`INV-B:222`), so sibling TDDs share a directory. Two tdd workers (the splitting the spec recommends, `SPEC:39`) with outputs in one directory write the same contract path, which WC-11 forbids (`SPEC:69`). The same holds for spec-panel if its `--output` is file-valued (R-1).
- Grading sentence: needs the coordinator to put two outputs in one directory; Medium.
- Recommendation: for file-valued flags use `<file-stem>.return-contract.yaml` or require a per-worker report directory. Priority: Medium.

### A-3 (Medium) AC-C1 and SA-2 disagree about the contract file
- Expert: Fowler.
- Issue: SA-2 (`SPEC:147`) allows the contract file to mention Orca "as an example of a caller's question channel". AC-C1 (`SPEC:172`) scans `src/superclaude/core/`, where P0 places `WORKER-CONTRACT.md` and the new Orca section in `HOW-WE-WORK.md` (`SPEC:158`, `SPEC:150`). Its pattern matches the lowercase text `orca orchestration` or `orca worktree`. If the example is written in that form, the P0 check fails for a text SA-2 allows. (Also, when the table cell's `\|` is copied into `grep -E`, it matches a literal `|`, not alternation; the markdown rendering hides this.)
- Grading sentence: needs the author to write the example in the matching form; Medium.
- Recommendation: exempt `core/WORKER-CONTRACT.md` and the Orca section of `HOW-WE-WORK.md` in AC-C1, or forbid the literal form in them. Priority: Low.

### A-4 (Medium) AC-1.2 uses a flag that several P1 commands do not have
- Expert: Adzic.
- Issue: AC-1.2 (`SPEC:196`) runs 7.2 on every P1 flag-set command "with `--unattended --output <dir>`". Section 3.1 gives workflow `--handoff none` and a generated package directory (`SPEC:92`), cleanup-audit a fixed `.claude-audit/` (`SPEC:85`), index-repo no output flag (`SPEC:86`) and init-lite a file-valued `--output` (`SPEC:87`). The same rows say the report directory comes from the row, not from `--output` (WC-4, `SPEC:62`).
- Grading sentence: needs a guess that the executor adapts the flag; Medium.
- Recommendation: replace with "with `--unattended` and the output the section 3 row names". Priority: Low.

### A-5 (Medium) Several requirements have no acceptance check
- Expert: Wiegers, Crispin (verification view).
- Issue: section 7 has no check for WC-3 (ask path), WC-6 (retry or re-run safety, `SPEC:64`), WC-10 outside pr-submit (cli-eval wait splitting is required at `SPEC:104` but only AC-4.3, conditional on D3, measures waits), WC-11 outside save (AC-3.4 only), or WC-12. WC-6 is the only requirement protecting the first attempt's output on a retry (`CAPS:116`).
- Grading sentence: a requirement without a test is a missing acceptance criterion, not a stated text that does harm. Medium.
- Recommendation: add one check each: a `--retry-of` re-run that leaves the first output byte-identical; a cli-eval run whose heartbeats stay within 5 minutes. Priority: Medium.

### A-6 (Medium) The tasklist nesting claim is stronger than its evidence
- Expert: Fowler, Nygard.
- Issue: the tasklist row says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" and lists "other required change: none" (`SPEC:122`). INV-A:14 supports a three-layer allowance; INV-B marks whether nested spawning works UNVERIFIED (`INV-B:210`, `INV-B:314`) and recommends that "the per-phase reflect fan-out must run at the worker's top level, not inside subagents" (`INV-B:215`). The spec's UNVERIFIED list does not carry this item (`SPEC:271-285`).
- Grading sentence: not blocking; the claim may be true, and no acceptance check depends on it. Medium.
- Recommendation: add it to the UNVERIFIED list and to the P2 happy-path run for tasklist. Priority: Low.

### Cross-document drift (note, not graded against the candidate)
The dependent command text `CMD:460-461` differs from the candidate in three places the candidate does not mention: it refuses a run with no `--report-dir` in chat only and writes no contract (`CMD:460`) while WC-4 says the contract is written "on every outcome ... including stops before any other output exists" (`SPEC:62`); it leaves git-ignored paths out of `artifacts` and cites "(WC-4)" for that rule (`CMD:461`), which the candidate's WC-4 does not contain; and it uses `--report-dir` (R-1). Whichever side is right, the candidate and its installed command should agree.

## Adversarial analysis (Whittaker, remaining attacks)

- **Sequence Attack** on WC-5 and WC-6 (`SPEC:63-64`): a re-run into a fixed report directory (cleanup-audit `.claude-audit/`, `SPEC:85`; index-repo; tdd file directory) that dies before writing leaves the previous run's `succeeded` contract in place, and WC-5 treats "a report exists" as success. State trace: before, prior contract `status: succeeded`; run 2 stops at an early crash; after, the worker (if it still reaches `worker_done`) reports run 1's file as `succeeded`. Mitigation: require the command to overwrite or remove the contract at start. Grade: minor note (needs a crash then a still-live worker).
- **Divergence Attack** on WC-2 (`SPEC:60`): the three resolutions (a) default, (b) caller flag, (c) blocked have no stated precedence when a default and a caller flag both apply (research pins `--strategy planning`, `SPEC:116`, while the brief passes `--strategy intent`). See the table row G-A edge.
- **Zero/Empty Attack** on R-1/R-2: empty `--target-release ""` for spec-panel (`SPEC:120`) is neither "absent" nor a value.
- **Accumulation Attack** (`SPEC:69`, WC-11): the spec bounds nothing about many workers in one worktree beyond "must never write the same file"; the single-owner list is not enumerated (`pm_context`, `last_session`, `next_actions` appear only in the save row via `INV-B:165`).
- **Nygard note**: the spec has no coordinator-side procedure for a worker that exits without `worker_done` beyond the 7.2 observation steps; the Orca recovery guide covers it (`CAPS:126`) and the spec could point to it.

## Guard Condition Boundary Table

Guards identified (the spec contains conditional logic and thresholds): G-A WC-2 gate resolution (`SPEC:60`); G-B WC-5 outcome mapping (`SPEC:63`); G-C WC-10 wait threshold (`SPEC:68`); G-D the `--unattended` switch (`SPEC:51`, `SPEC:146`); G-E AC-C5 deleted-line count (`SPEC:176`); G-F nesting depth (`SPEC:33`, `SPEC:249-253`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G-A gate resolves (a)/(b)/(c) | SPEC:60 | Zero/Empty | caller flag `""` (for example `--target-release ""`) | unspecified | "required as a flag, else blocked" (`SPEC:120`) does not say empty equals absent | GAP (R-1/R-7 family, Medium) |
| G-A | SPEC:60 | One/Minimal | exactly one gate | true | resolves per its section 3 row | OK |
| G-A | SPEC:60 | Typical | gate with documented default | (a) | default applies, run continues | OK |
| G-A | SPEC:60 | Legitimate Edge Case | default (a) and caller flag (b) both apply | both | no precedence stated | GAP (Medium) |
| G-B outcome mapping | SPEC:63 | Zero/Empty | no report exists | `failed` | `--outcome failed` | OK |
| G-B | SPEC:63 | One/Minimal | report exists, empty or unparseable | falls to "otherwise" | maps to `succeeded` | GAP (R-2, Medium) |
| G-B | SPEC:63 | Sentinel Value Match | `status` not in the four values | falls to "otherwise" | maps to `succeeded` | GAP (R-2, Medium) |
| G-B | SPEC:63 | Typical | `succeeded`, `partial`, `failed`, `blocked` | per rule | explicit | OK |
| G-B | SPEC:63 | Legitimate Edge Case | audit whose verdict is FAIL | `succeeded` | explicit: the audit itself succeeded | OK |
| G-C wait split | SPEC:68 | Typical | 10-minute poll wait | true (> 5 min) | split into waits of at most 4 minutes | OK |
| G-C | SPEC:68 | Maximum/Overflow | cli-eval 3600 s wait (`INV-A:65`) | true | split into at most 4-minute waits (`SPEC:104`) | OK |
| G-C | SPEC:68 | Legitimate Edge Case | single call of 4 to 5 minutes | false | not required to split; AC-4.3 and `SPEC:114` forbid over 4 minutes | GAP (R-3, Medium) |
| G-C | SPEC:68 | One/Minimal | single call of exactly 5 minutes | false ("longer than 5") | unsplit; no heartbeat margin | GAP (R-3, Medium) |
| G-D `--unattended` | SPEC:51 | Zero/Empty | flag absent | false | SA-1: today's behavior | OK |
| G-D | SPEC:51 | Typical | standalone token present | true | unattended mode | OK |
| G-D | SPEC:51 | Sentinel Value Match | the string inside quoted content | unspecified | no matching rule | GAP (R-7, Medium) |
| G-D | SPEC:128 | Legitimate Edge Case | flag passed to a section 4 command | unspecified | not stated | GAP (R-7, Medium) |
| G-E AC-C5 | SPEC:176 | Zero/Empty | edited file, no change | prints nothing | pass | OK |
| G-E | SPEC:176 | One/Minimal | one added line | `1 0` | pass | OK |
| G-E | SPEC:176 | Legitimate Edge Case | whitespace-only reflow of an existing line | deletion counted | fails, matching "additive" intent (SA-4) | OK |
| G-F depth | SPEC:33 | Typical | depth 1 | worker may not start workers | refused, `nested_worker_depth_exceeded` | OK |
| G-F | SPEC:249-253 | Legitimate Edge Case | user raises depth (D5 b) | limit lifted | D5 rejects it; R1 protection stated | OK |

Classes left out, with reason. G-A Maximum/Overflow and G-D Maximum/Overflow: no capacity or count is attached to the guard. G-A Sentinel: covered by G-D. G-B Maximum/Overflow: a status has no magnitude. G-C Zero/Empty: a step that does not block has no wait. G-E Maximum/Overflow and Sentinel: the count is bounded by file size and has no reserved value. G-F Zero/Empty and One: depth 0 is the coordinator, not a guard input. Every GAP above is graded Medium under FR-8/FR-9: none names a concrete wrong outcome that holds with no further assumption, and none is a security, data-loss or safety-boundary risk. The table is complete (FR-10).

## Quantity flow (Pipeline Dimensional Analysis)

The rollout is a multi-stage filter over the command set:

```text
[cmd/ : 43] --> [inventory split] --> [10 ready + 27 needs-change + 6 coordinator-only = 43]
                                        |
                                        v
[37 worker-capable] --> [P1 flag set 14 + P2 15 + P3 4 + P4 3 = 36 get --unattended]
                        [load: 1, usage-line fix only, no flag]  --> 36 + 1 = 37
[6 coordinator-only]  --> no flag
```

Checked: 21 + 22 = 43 (`INV-A:3`, `INV-B:3`, `SPEC:76`); ready 5 + 5 = 10 (`INV-A:73`, `INV-B:278`); needs-change 13 + 14 = 27; coordinator-only 3 + 3 = 6. No consumer assumes an unfiltered count; no mismatch.

## Minor notes

- WC-1 (`SPEC:59`) says a fallback "well inside" the readiness limit; the evidence gives a number (30 s passes, above about 45 s fails, `CAPS:49`). State it.
- WC-4 (`SPEC:62`) has no `contract_version` field; workflow already ships one ("contract 1.1", `INV-B:272`). A version field costs one line and helps evolution (Newman).
- Line 16 (`SPEC:16`) says the command change is "limited to" unattended mode, report file and resume; section 3.2 "Other required change" adds flag reconciliation, tool lists, a skill write path and a new `--resume` (`SPEC:105`, `SPEC:108`, `SPEC:118`, `SPEC:124-125`). Reword.
- Section 3.1's lead-in says the only command changes are the small fixes in the last column (`SPEC:79`), while section 3 and P1 add `--unattended` to every ready command (`SPEC:76`, `SPEC:159-160`).
- E3 (`SPEC:23`) cites `invocation_method: "skill-direct"` as support while 1.4 (1) says the PR #329 brief used the Agent-tool route and so proves only the nested route (`SPEC:43`). The two should be reconciled in one sentence (INV-A:13 and README:12 are the sources).
- 7.2 step 2 asks for a `worker-show` at least every 5 minutes while step 3 allows one `check --wait` of 900 000 ms (`SPEC:181-182`); say that the wait is looped in shorter slices.
- Stale contract on a re-run into a fixed directory (Sequence Attack above).

## Follow-up candidates

Medium: R-1, R-2, R-3, R-4, R-5, R-6, R-7, A-1, A-2, A-3, A-4, A-5, A-6. Minor: the seven notes above. The review-loop rule is that the session that ran the review asks the user once whether to open an issue for these (`CMD:260`); this worker has no user channel, so it creates none and records the list; the coordinator should ask once.

## Reviser brief

No blocking finding is open, so no reviser is needed: `ids: none`. Rule restated for any later use: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on each addition; prefer deleting or narrowing to adding; report byte size before and after, with bytes added and deleted per finding id. Medium and minor findings are not in this brief and must not be edited under it, including through "apply all findings".

Coverage: whole document, first review (gate); `scoped PASS` does not apply.

verdict: PASS
