review: 1 of 3

# Spec panel report: orca-worker-contract-spec.md (critique mode, focus requirements,architecture)

## Header
- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:29-37` (read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (computed with `sha256sum` in this run).
- Baseline: none given, `--re-review` not given; this is a first review of the full document (`command.md:258`).
- Reviewer model actually used: `claude-sonnet-5-5` (Sonnet 5.5).
- Lint evidence: `.dev/orca-command-refactor/review/lint-1.md:1-5` (sha256 of the lint file `6a70e9a1255ee5d4652078e22f1d02b3383feeb5af682b9017b29610cb1b420a`). It reports `Checks: REF. Findings: 0.` There is no lint id to confirm or dismiss. (The lint header at line 1 carries the candidate's sha256, which matches the hash above.)
- Path conventions in this report: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Source files under `src/`, `~/.claude/` and Orca's install tree are not in the sandbox, so a citation that points only there is marked UNVERIFIED.
- Covered: the whole candidate (lines 1-285), read in full; README (binding context) in full; the inventories by targeted checks (the totals 21/22 and the 10/27/6 split, the CAPS lines the spec leans on for the 60 s limit, depth 1, `worker_done`, `ask`, `consumer_fenced`, `--report-path`). Not covered: line-by-line re-verification of the ~340 per-command citations into `src/` (not readable here).
- Panel: Wiegers, Adzic, Cockburn (requirements focus); Fowler, Newman, Hohpe, Nygard (architecture focus); Whittaker (active in every panel, `command.md:83`). Crispin, Gregory and Hightower have no focus here; testing points they would raise are folded in where they touch acceptance checks.

## Mandatory artifact: Guard Condition Boundary Table
Trigger met: the spec contains thresholds and guards (`SPEC:68` 5-minute heartbeat and 4-minute wait; `SPEC:33`/`SPEC:214` depth 1; `SPEC:59` 60 s readiness; `SPEC:121` confidence below 0.70; `SPEC:51`/`SPEC:228` the `--unattended` token). Built by Nygard, completed by Crispin, attacked by Whittaker. Classes that cannot occur for a guard are left out with the reason in the last column.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| unattended gate -> blocked | SPEC:60 (WC-2) | Typical | gate hit under `--unattended` | true | write contract `status: blocked` + `blocked_question`, stop | OK |
| contract location | SPEC:62 (WC-4) | Typical (`--output` is a directory) | `--output .dev/x/` | true | `.dev/x/return-contract.yaml` | OK |
| contract location | SPEC:62 (WC-4) vs SPEC:90 | Legitimate Edge Case (`--output` is a file) | `--output out/tdd.md` | true | not specified; WC-4 defines only a directory; this is finding B-1 | GAP |
| contract location | SPEC:62 (WC-4) vs SPEC:83, 92 | Legitimate Edge Case (command fixes its own path) | adversarial `<output>/adversarial/...`; workflow `.dev/tasks/to-do/<id>/...` | true | SPEC:83 and SPEC:92 name paths that differ from WC-4; this is finding B-1 | GAP |
| contract location | SPEC:62 (WC-4) | Zero/Empty | `--unattended` with no output directory | n/a | blank: refusal vs default vs blocked is never stated; finding M-1 | GAP |
| `--unattended` switch | SPEC:51, SPEC:228 | Sentinel Value Match | the token inside quoted prompt text, e.g. `/sc:tdd "explain --unattended"` | n/a | blank: only "testable by grep" is stated; finding M-2 | GAP |
| 4-minute wait split | SPEC:68 (WC-10) | Typical | wait of 3 min | false | no split needed | OK |
| 4-minute wait split | SPEC:68 (WC-10) | Maximum/Overflow | single tool call of 600 s | true | split into waits of at most 4 min | OK |
| 4-minute wait split | SPEC:68 (WC-10) | Zero/Empty | wait of 0 | n/a | left out: a zero wait is not a wait | n/a |
| readiness 60 s | SPEC:59 (WC-1) | Maximum/Overflow | prompt takes 45 s / 30 s fallback | true | 30 s fallback passes, above about 45 s fails (EVIDENCE cited at SPEC:59) | OK |
| nesting depth 1 | SPEC:66 (WC-8), SPEC:33 | Maximum/Overflow | command calls `worker-start` | true | refused with `nested_worker_depth_exceeded`; whether `task-create` is also refused is UNVERIFIED (CAPS:103, SPEC:276) | OK (UNVERIFIED sub-case) |
| confidence below 0.70 -> blocked | SPEC:121 (task row) | Legitimate Edge Case | confidence in 0.70-0.89 | n/a | not stated; the band may be a person-gate in the task protocol; the cited lines are not in the sandbox, UNVERIFIED; finding M-6 | GAP (UNVERIFIED) |
| outcome mapping | SPEC:63 (WC-5) | Zero/Empty | no report file exists | true | `--outcome failed` | OK |
| outcome mapping | SPEC:63 (WC-5) | Legitimate Edge Case | file exists but is not valid YAML or has an unknown `status` | n/a | not stated; finding M-4 | GAP |
| circuit breaker | SPEC:64 (WC-6), CAPS:116 | Maximum/Overflow | 3rd failed start for one Task | true | Task failed; a worker's own `failed` report does not count (CAPS:80 is cited at SPEC:263 for this) | OK |

FR-10 check: every guard is enumerated; every row has a status. FR-8/FR-9 grading: the GAP rows are graded under Findings below. B-1 is blocking; the others are Medium because each needs a guess about which reading an implementer picks, or is a requirement the document never states.

## Pipeline Dimensional Analysis
Not triggered as a data pipeline with count divergence. The one count-bearing flow is the command inventory: 43 commands (21 + 22, `INV-A:3`, `INV-B:3`) = 10 ready (SPEC:78-92 lists 10 rows) + 27 needs-change (SPEC:97-125 lists 27 rows) + 6 coordinator-only (SPEC:132-137 lists 6 rows), and the phase lists P1 (9) + P2 (11 needs-change + 4 ready) + P3 (4) + P4 (3) = 31 = 27 + 4 ready commands that need a P2 change (SPEC:159-162). The counts conserve. Inventory split per file also matches: INV-B:289 gives 14 needs-change for B; the A side contributes 13. No Quantity Flow Diagram is needed.

## === REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL as raised, graded BLOCKING): the contract file's location is defined three incompatible ways
- Experts: Wiegers (lead), Adzic, Whittaker (Sentinel Collision / Divergence attack).
- Quoted texts and locations:
  1. SPEC:62 (WC-4): "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the report path is "known before dispatch".
  2. SPEC:90 (tdd row, section 3.1): "Brief must pass: ... `--output <file>`"; report today: "the TDD at `--output`". SPEC:87 (init-lite): "`--output <file>`". SPEC:200 (AC-2.2): "`/sc:tdd "auth" --unattended --output <file>`".
  3. SPEC:83 (adversarial): "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"; SPEC:92 (workflow): report is "`.dev/tasks/to-do/<id>/return-contract.yaml`" and the brief passes only `--handoff none`.
  4. SPEC:182 (7.2 step 3): the worker's report path "is the WC-4 contract path"; SPEC:183 (step 4) runs `test -s <contract>`.
- Grading sentence: An implementer who follows the stated text as written builds a tdd (and init-lite) worker whose contract lands at `<output-dir>/return-contract.yaml` with `<output-dir>` equal to the `--output` value the brief passes, which is a file path, so the contract path is `<TDD file>/return-contract.yaml`, a path that cannot be created beside a file; and a workflow worker whose contract path is chosen by the command (`<id>`), not by the coordinator before dispatch, and an adversarial worker whose contract sits one directory below `<output>`. Each is wrong because AC-2.2 and 7.2 steps 3-4 require the worker's `--report-path` to be the WC-4 path and `test -s` to pass on it, and for these commands that cannot hold. This is two stated texts that contradict (WC-4 vs the tdd, init-lite, adversarial and workflow rows) and a stated text an acceptance criterion cannot pass, so it is blocking.
- Recommendation: state one rule for where the contract goes when `--output` is a file or the command fixes its own path (for example: the contract goes beside the file, or the brief passes a separate report directory), and make the section 3.1 rows and AC-1.4 agree with it. Prefer narrowing WC-4's wording to adding a new flag.
- Priority: High. Quality impact: Completeness and Consistency each about +2.
- Evidence check: SPEC:62, 83, 87, 90, 92, 182-183, 200 read in the candidate. The per-command source lines behind the tdd/workflow rows (`sk/tdd/SKILL.md`, `sk/sc-workflow-protocol/refs/return-contract.md`) are not in the sandbox: UNVERIFIED, but B-1 rests on the spec's own text.

### M-1 (MAJOR as raised, graded Medium): `--unattended` with no output directory is undefined
- Experts: Wiegers, Nygard. SPEC:62 (WC-4) requires an output directory "the coordinator passed" but never says what a command does when `--unattended` arrives without one. The spec-level rule for refusal exists for no other case; SPEC:60 (WC-2) offers only gate resolutions. A requirement the document never states, so Medium. Recommendation: one sentence in WC-4 (refuse, or default to a named path). Priority: Medium. Note the sandbox command definition for spec-panel already refuses before any work without a report directory (`command.md:460`), which shows the case matters; whether that wording is meant to be the model is the spec author's choice.

### M-2 (MAJOR as raised, graded Medium): no rule for how the `--unattended` token is recognized
- Experts: Whittaker (Sentinel Collision), Wiegers. SPEC:51 and SPEC:228 pick the explicit flag and justify it as "testable by grep and cannot misfire on a person". A prompt that quotes the text (`/sc:tdd "explain the --unattended flag"`) would trip a plain grep or substring check. The spec states no tokenisation rule. An implementer picks a reading, so this is a guess and Medium. Recommendation: say the flag counts only as a standalone argument outside quoted content. Priority: Medium.

### M-3 (MAJOR as raised, graded Medium): ordering of a blocked report, an `ask`, and a re-run is unclear for fresh-directory commands
- Experts: Whittaker (Sequence Attack), Nygard. SPEC:60 (WC-2 c) writes `status: blocked` and stops; SPEC:61 (WC-3) lets the worker session then `ask` and "re-invoke or resume the command with the answer"; SPEC:64 (WC-6) says commands without a resume flag write "each run into a fresh output directory" (about 20 rows in SPEC:99-125 say "fresh dir"). State trace: run 1 writes `D/return-contract.yaml` with `blocked`; the answer arrives; run 2 either overwrites `D/` (not "fresh"), or writes `D2/` (then the report path the coordinator knew before dispatch, SPEC:62, is stale). The text allows both readings; the worker may also hold a blocked contract while the re-run succeeds. Medium. Recommendation: say which directory the re-run uses and which contract the worker reports. Priority: Medium.

### M-4 (MAJOR as raised, graded Medium): the unparseable or off-vocabulary contract case has no outcome
- Experts: Whittaker, Adzic. SPEC:63 (WC-5) maps "no report exists" and the four statuses; SPEC:62 says existing contracts "keep their fields and add the missing ones", so a command whose own `status` uses another vocabulary (the spec's Decisions row SPEC:262 sets a fixed four-value set) collides with its legacy field, and a file that exists but fails `yaml.safe_load` (the check at SPEC:183) maps to nothing. Not stated, so Medium. Recommendation: one line in WC-5. Priority: Medium. The legacy status values of workflow, brainstorm, reflect and adversarial contracts are not in the sandbox: UNVERIFIED.

### M-5 (MAJOR as raised, graded Medium): coordinator stall policy is only a test condition
- Experts: Nygard, Hohpe. SPEC:181 (7.2 step 2) makes "`agentWait` is never non-null" a pass condition, and SPEC:44 says a stalled command prompt is "seen only through `worker-show`'s `agentWait` or a missing report". SPEC:73 (section 2.3) lists what the coordinator owes but gives no runtime rule for what it does when `agentWait` is non-null or no `worker_done` arrives (wait, `send`, `worker-stop`, retry). The failure mode named as "the real failure mode" (SPEC:44) therefore has detection but no response. Requirement never stated, so Medium. Priority: Medium. CAPS:129 gives the verb context; CAPS:116 gives the retry and circuit-breaker facts a rule could use.

### M-6 (MAJOR as raised, graded Medium): the confidence band between 0.70 and 0.89 for `/sc:task` is not addressed
- Experts: Wiegers, Whittaker (Divergence). SPEC:121 resolves "confidence below 0.70" as blocked. The repo's confidence rule has a middle band (0.70-0.89 "present alternatives, ask questions", INV-A:36 for `/sc:agent`; `/sc:task`'s own band is in `cmd/task.md` and `sk/sc-task-protocol/SKILL.md`, not in the sandbox: UNVERIFIED). If `/sc:task` also asks in that band, a worker stalls despite the row. Medium, because it needs both an unverified fact and a guess. Recommendation: check `cmd/task.md:80` and state the band's resolution. Priority: Medium.

### M-7 (MAJOR as raised, graded Medium): AC-C5 and "additive" edits conflict with editing a one-line Usage entry
- Experts: Crispin, Adzic. SPEC:176 (AC-C5) passes only when `git diff -U0 ... | grep -E '^-[^-]'` prints nothing, and SPEC:149 (SA-4) says new flags are additive. In the command template read in this sandbox the Usage block is one fenced line per form (`command.md:21-24`); appending `--unattended` to an existing line deletes that line in a unified diff, so AC-C5 fails. The spec does not say to add a new Usage line instead. An implementer must guess to add a second line. Medium. Recommendation: say "new flags go on a new Usage line". Priority: Low-Medium.

### M-8 (MAJOR as raised, graded Medium): AC-C1 vs SA-2 on mentions of Orca in the contract file
- Experts: Crispin, Fowler. SPEC:147 (SA-2) allows "the only allowed mention of Orca ... as an example of a caller's question channel inside the contract file"; SPEC:61 (WC-3) tells the session to use "the preamble's `ask` command". SPEC:172 (AC-C1) scans `src/superclaude/core` (where SPEC:52 places `WORKER-CONTRACT.md`) for `orca(-ide)? orchestration|worktree|terminal|agent` and requires no output. An example written as `orca orchestration ask` satisfies SA-2 and fails AC-C1. Whether the example uses the command string is a guess, so Medium. Recommendation: exclude `core/WORKER-CONTRACT.md` in AC-C1 or forbid the literal command there. Priority: Medium.

## === ARCHITECTURE ANALYSIS ===

### M-9 (Medium): the strongest precedent is described two ways
- Experts: Fowler, Newman. SPEC:23 (E3) cites return contract `invocation_method: "skill-direct"` (`.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10`) as support that Orca workers invoked `/sc:adversarial`, while SPEC:43 (section 1.4 gap 1) says the same run's brief had workers invoke it "through an Agent-tool subagent" (`.dev/codegraph-migration/orchestration/README.md:31`), proving "the nested route, not the direct route". CAPS:156 says the same as SPEC:43. Both are in the spec and SPEC:43 is candid, but E3 in the evidence table reads as support for the direct route, and a reader of E3 alone concludes the opposite. Both source files are outside the sandbox: UNVERIFIED. No wrong implementation follows, because Phase 0 (SPEC:158, SPEC:194) tests the direct route first. Recommendation: reword E3 to name the nested route, or drop `skill-direct` from it. Priority: Low-Medium.

### N-1 (MINOR): "10 ready today" vs gate conversion in P2
- Experts: Cockburn. SPEC:76-79 says 10 commands "run as workers now" while SPEC:88-91 (reflect, release-split, tdd, troubleshoot) list P2 gate changes, and SPEC:160 puts them in P2. The label is true only with the brief's workaround flags; the text says so ("if the brief uses the stated flags", SPEC:79). A note.

### N-2 (MINOR): SPEC:16 says what changes is "limited to" unattended mode, report files and resume
- Experts: Fowler. Section 3 also adds flag refusals, new tools (explain, SPEC:108), a new `--resume` flag (cli-portify, SPEC:105), and interface-drift fixes (SPEC:118, 124-125); SA-4 (SPEC:149) lists the fixes. The summary sentence understates scope. A note.

### N-3 (MINOR): WC-12 vs WC-5
- Experts: Hohpe. SPEC:63 (WC-5) "sends `worker_done` exactly once" and SPEC:70 (WC-12) "stops without sending `worker_done`" on `consumer_fenced`. The second case is a fenced worker; CAPS:67 supports it. Say "at most once" to remove the apparent clash.

### N-4 (MINOR): one skill line is cited at two different line ranges
- Experts: Newman. SPEC:65 and SPEC:11 cite `sk/sc-pr-submit-protocol/SKILL.md:37-39` for the top-level rule (re-read, per SPEC:11); CAPS:161 cites `/home/coder/.claude/skills/sc-pr-submit-protocol/SKILL.md:47-49` for the same quote. The two can differ if the installed copy and `src/` differ. UNVERIFIED either way (neither file is in the sandbox). Also unverifiable here: the spec's own grep claim in E5 (SPEC:25) and its 11 re-read locations (SPEC:11).

## Whittaker attack summary (all five methodologies)
- Zero/Empty: `--unattended` with no output directory, M-1; `--output` empty, B-1 row.
- Divergence: `--output` as file vs directory, B-1; confidence band, M-6.
- Sentinel Collision: `--unattended` inside quoted text, M-2.
- Sequence: blocked report then re-run, M-3; `consumer_fenced` vs exactly-once, N-3.
- Accumulation: three failed starts trip the circuit breaker (CAPS:116); the spec's retry rule (SPEC:64) does not say a `blocked` outcome mapped to `failed` (SPEC:63) counts or not. CAPS:116 says a worker's own `failed` report does not count, so no finding.

## Consensus and disagreements
- Consensus: the decision (Orca on top, commands as units, SPEC:13-17) is well supported and the rejected alternative is argued with checkable Orca facts (SPEC:29-37, `CAPS:97-103`, `CAPS:145-150`); the evidence-strength section (SPEC:41-45) is honest about gaps; the 10/27/6 counts conserve.
- Disagreement: Wiegers and Nygard weigh M-1/M-3/M-5 as the next fixes after B-1; Fowler would fold M-9 into B-1's rewrite of WC-4. They agree none blocks.

## Follow-up candidates (Medium and minor, not blocking, not in the Reviser brief)
Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9. Minor: N-1, N-2, N-3, N-4.
The session that ran this review asks the user once for this loop whether to open an issue for these; this run created none and has no user to ask (output file only), so the list is only recorded.

## Reviser brief
Repair only the blocking finding B-1 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

Blocking finding:
- B-1. Texts: SPEC:62 "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; SPEC:90 "`--output <file>`" (tdd) and SPEC:87 (init-lite) and SPEC:200 (AC-2.2); SPEC:83 "`<output>/adversarial/return-contract.yaml`"; SPEC:92 "`.dev/tasks/to-do/<id>/return-contract.yaml`"; SPEC:182-183 (7.2 steps 3-4). Stated wrong outcome: the contract path for a file-valued `--output` is `<file>/return-contract.yaml`, and for adversarial and workflow it differs from the WC-4 path, so the path is not known before dispatch and the acceptance steps cannot pass.

Brief clauses overridden: none (the coordinator's brief asked for a first review with the FIRST-REVIEW prompt; no clause widened scope or regraded a minor finding).

verdict: FAIL
