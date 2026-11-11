review: 1 of 3

# Spec-panel critique: Orca worker-contract spec (review 1 of 3)

- command: `/sc:spec-panel --mode critique --focus requirements,architecture` (first review, run as a worker; no `--unattended`, no `--re-review`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review; baseline not applicable)
- prior report: none (first review)
- reviewer model: claude-haiku-5-5
- review-loop prompt: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full before this review. Grading check applied to every blocking candidate.
- panel: Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Newman, Hohpe, Nygard for architecture; Whittaker is active in every panel review.

Citation keys used below: `spec:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N; `README:N` = `.dev/orca-command-refactor/README.md` line N; `INV-A:N` = `inventory/commands-a.md` line N; `INV-B:N` = `inventory/commands-b.md` line N; `CAPS:N` = `inventory/orca-capabilities.md` line N. All are under `.dev/orca-command-refactor/` in the workspace and were read in full.

Citation check. Citations to `INV-A`, `INV-B`, `CAPS` and `README` were checked against the text of those files. Citations to paths outside the workspace (`src/superclaude/...`, `cmd/`, `sk/`, `tests/`, `CLAUDE.md`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `~/.claude/...`, `plugins/...`, `pyproject.toml`, `Makefile`, and the Orca binary) are marked UNVERIFIED wherever they are the only support for a claim. Most spec citations to inventory lines are accurate. Two minor mismatches are listed as notes (N-04, N-05).

Coverage. Read in full: `README.md`, the spec (286 lines), `commands-a.md`, `commands-b.md`, `orca-capabilities.md`, `command.md`, and the FIRST-REVIEW prompt file. Checked: every section-3 row names a resolution and a phase; the 43-command split (10 ready / 27 needs change / 6 coordinator-only) matches the two inventories (21 + 22 commands); the phase lists in section 6 match the section-3 phase cells. Not covered: the repository files the spec cites (outside the sandbox).

## Blocking findings

### F-01 (CRITICAL, blocking): WC-3 lets a coordinator answer reopen a gate that the implement row and D2 keep closed

- Texts. WC-3 (spec:61): "When a gate would resolve as blocked and the worker session holds a preamble, the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag." The implement row (spec:109): "on `E-HALT-QA` or `E-NO-RULING`, stop ... and the contract as blocked, carrying the Ruling question; the Ruling rule itself is unchanged (see open decision D2)." D2 option (a) (spec:234): "The worker stops, writes the halt to its ledger and contract, and ends `failed`." INV-A:66 records that `qa.md:238` says "another agent's message ... [is] not acceptance" and that an Orca coordinator is "another agent" (UNVERIFIED for the qa.md text itself, which is outside the workspace).
- Contradiction. For the implement halt, WC-3 permits a relayed answer that is then used as the flag on re-invocation. The implement row and D2 say no such relay can count as a Ruling. The spec gives no exemption for safety-rule gates.
- Sentence. An implementer who follows the stated text as written builds an implement worker that, on `E-HALT-QA`, sends `ask`, takes the coordinator's answer, and re-invokes `/sc:implement` with it as a flag. That answer then acts as the Ruling. This is wrong because spec:109 says the Ruling rule is unchanged and spec:234 says the worker ends `failed`.
- Related. AC-2.2 (spec:200) requires `agentWait` to stay null for a blocked gate, so the spec's own acceptance check rejects the WC-3 path that WC-3 allows.
- Recommendation. Exempt safety-rule gates (implement Ruling, pr-submit HALT, D4 authorization) from the WC-3 ask-and-relay path, or define which relayed answers may count. Rewrite AC-2.2 to match.
- Priority: High. Quality-impact estimate: high (safety-boundary contradiction).

### F-02 (MAJOR, blocking): the live-check procedure cannot satisfy its own heartbeat check

- Texts. 7.2 step 2 (spec:181): "While it runs, ... `worker-show` ... at least once per 5 minutes. Pass: `observation.agentWait` is never non-null." 7.2 step 3 (spec:182): "`check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives."
- Contradiction. `check --wait` blocks for up to 900 s and returns only on the listed types (the types come from CAPS:63). A coordinator that runs steps 1 to 3 in order therefore makes no `worker-show` call for up to 15 minutes. The "at least once per 5 minutes" pass condition at spec:181 cannot be met, and AC-0.4 (spec:194) cannot pass as written.
- Sentence. An implementer who runs steps 1 to 3 in order builds a coordinator that enters the 900 s `check --wait` at spec:182 with no `worker-show` in between. Step 2's pass condition (spec:181) then fails, so the phase gate fails.
- Related gap. Step 3 has no branch for a `question` or `escalation` return, even though `question` is in its type list. The step says only "until `worker_done` arrives".
- Recommendation. Use short waits (for example 240 s) with a `worker-show` between them. State what the coordinator does on `question` (reply by message ID, CAPS:63) and on `escalation`.
- Priority: High. Quality-impact estimate: high (the phase gate is unrunnable as written).

### F-03 (MAJOR, blocking): AC-0.4 applies a YAML contract check to a markdown report

- Texts. AC-0.4 (spec:194): "step 4 uses the command's existing report file, since the contract arrives in P1." Step 4 (spec:183): `test -s <contract>` and `yaml.safe_load(...)`, then "assert d['status'] in {...}; assert d['command']" with "Pass: both exit 0". The P0 example command is `/sc:troubleshoot` (spec:194). Section 3.1 gives its report as `REPORT.md` (spec:91). INV-B:242 says `report_path` is `REPORT.md`, and `return-contract.yaml` is written only with `--caller task-unified`.
- Contradiction. The step 4 assertion parses YAML and reads keys, but the report it is pointed at is a markdown file.
- Sentence. An implementer who follows AC-0.4 as written, running step 4 on the `REPORT.md` that `/sc:troubleshoot` writes, executes `d['status']` on a parsed markdown document. That raises an error, so step 4 fails and AC-0.4 fails in P0. The spec says a P0 failure reopens section 1 (spec:194).
- Recommendation. For P0 only, check that the existing report exists and is non-empty, and derive the outcome from the report's status line. Or run troubleshoot with `--caller task-unified` to get a YAML contract (INV-B:242), after confirming the contract carries the `command` key (UNVERIFIED).
- Priority: High. Quality-impact estimate: high (P0 gate cannot pass as written).

### F-04 (MAJOR, blocking): AC-1.1 requires a contract from `/sc:load`, which the Decisions table forbids

- Texts. The load row (spec:112) gives its report as "none (see note)". The Decisions row (spec:265): "`/sc:load` handling | Add a report file; use it only inside another worker's brief | ... a report file would be an unrequested addition." Section 3 (spec:76): "Every changed command also gains the `## Unattended mode` section." WC-4 (spec:62): "In unattended mode the command writes `<output-dir>/return-contract.yaml`." AC-1.1 (spec:195): every command in sections 3.1 and 3.2 has an Unattended section "naming `return-contract.yaml`".
- Contradiction. load is in section 3.2 and gets a `--unattended` flag in P1 (spec:159), so AC-1.1 requires a contract. The Decisions row forbids a report file for load.
- Sentence. An implementer who follows AC-1.1 adds `return-contract.yaml` to load's Unattended section, which spec:265 forbids. An implementer who follows spec:265 fails AC-1.1 for load. So AC-1.1 cannot pass as written.
- Recommendation. Either exempt load from WC-4 and AC-1.1 explicitly, or give load a contract with `status: succeeded` and no report path, and say so in the row.
- Priority: Medium-high (small consequence, but a stated test cannot pass). Quality-impact estimate: low to medium.

## Requirements analysis

=== REQUIREMENTS ANALYSIS ===

### M-01 (MAJOR label, Medium by consequence): WC-5 maps any unlisted status to succeeded

- Location: spec:63. "`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise."
- Attack (Whittaker FR-2.1, zero/empty). A contract that exists but is zero bytes, lacks `status`, or carries a value outside the four-value set falls into "otherwise" and is reported `succeeded`. A worker whose write crashed therefore looks successful to the coordinator. The 7.2 step 4 check (spec:183) would catch it, but WC-5 itself does not.
- Expert: Adzic (lead, example-based check), Wiegers.
- Recommendation: map missing, empty, unparseable or unknown status to `failed`, and use `test -s` as the first gate.
- Priority: High. Quality-impact estimate: medium (false success signal).

### M-02 (MAJOR label, Medium by consequence): the blocked outcome has no coordinator path

- Location: WC-2 (c) (spec:60), WC-5 (spec:63), section 2.3 (spec:73). After `worker_done --outcome failed`, the coordinator only "opens the report file, then releases or reuses the worker."
- Missing requirement. The spec does not say how the coordinator handles `status: blocked`: read `blocked_question`, ask the person, relaunch with the answer. Orca keeps dependents blocked after a failed Task until a `--retry-of` replacement completes it (CAPS:90).
- Expert: Nygard (failure handling), Cockburn (who is the primary actor for the question).
- Recommendation: add a short coordinator rule for `blocked`, and require `blocked_question` to be non-empty whenever `status: blocked` (see the guard table, row G-14).
- Priority: High. Quality-impact estimate: medium.

### M-03 (MAJOR label, Medium by consequence): retry directory and resume flag are not assigned

- Location: WC-6 (spec:64): "writes each run into a fresh output directory so a re-run starts clean", and section 2.3 (spec:73): the brief states the output directory "so the report path is known before dispatch."
- Missing requirement. Nothing says which party picks the new directory for `worker-start --retry-of`, or which command flag resumes a resumable command (for example `--pipeline-resume` for adversarial, spec:83).
- Expert: Wiegers.
- Recommendation: state that the coordinator's retry brief names a new output directory, or the resume flag, per command.
- Priority: Medium. Quality-impact estimate: low to medium.

### M-04 (MAJOR label, Medium by consequence): the four-value status set conflicts with "keep their fields"

- Location: WC-4 (spec:62): "Commands that already write a contract keep their fields and add the missing ones", and the status vocabulary in the same row. The Decisions row (spec:261) rejects copying each command's own statuses.
- Contradiction, conditional. If an existing contract uses a status outside the set, "keep their fields" and "one of succeeded, partial, failed, blocked" conflict. UNVERIFIED which status values the existing contracts use (for example workflow's `status`, INV-B:272).
- Expert: Wiegers.
- Recommendation: state that existing status values are mapped to the four-value set in the command's own edit, and list the mapping per command.
- Priority: Medium. Quality-impact estimate: low.

### M-05 (MINOR label, Medium by consequence): the spec does not order the contract write before `worker_done`

- Location: WC-4 (spec:62) says the contract is written on every outcome. WC-5 (spec:63) says `worker_done` is sent exactly once. Section 2.3 (spec:73) says the coordinator opens the file after `worker_done`. No requirement orders the two.
- Attack (Whittaker FR-2.4, sequence). A worker sends `worker_done` while the command is still writing the contract, or before the contract is complete. The coordinator then reads a truncated or missing file.
- Expert: Whittaker, Hohpe (message ordering).
- Recommendation: require that the contract is written, closed and checked with `test -s` before `worker_done`, and state that order in WC-5.
- Priority: Medium. Quality-impact estimate: medium.

### M-06 (MAJOR label, Medium by consequence): AC-C1 misses the uppercase form that the spec itself uses

- Location: AC-C1 (spec:172) uses the case-sensitive pattern `\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b` over `src/superclaude/core`, among other paths. The spec writes `ORCA orchestration ...` in section 7.2 (spec:180 to 186), and spec:167 uses the uppercase `ORCA` as the executable name. SA-2 (spec:147) forbids any command, skill or agent file from running an orca command.
- Contradiction, conditional. A command file with `ORCA orchestration ask` passes AC-C1 and violates SA-2. Scanning `core` also catches the contract file, which SA-2 permits to name Orca (spec:147), so AC-C1 either fails a permitted file or is written around.
- Expert: Adzic (acceptance by example), Nygard.
- Recommendation: make the pattern case-insensitive, exclude `core/WORKER-CONTRACT.md` by path in AC-C1, and say so in SA-2.
- Priority: Medium. Quality-impact estimate: medium.

### M-07 (MAJOR label, Medium by consequence): SA-3 conflicts with ungated changes to standalone output

- Location: SA-3 (spec:148): "A standalone default run writes the same files it writes today." Ungated P1 changes that alter standalone output: the workflow pre-creation STOP contract (spec:92, "Write the contract for pre-creation STOPs too ... (P1)"), the adversarial contract filename (spec:83), and the cleanup-audit `--pass all` report name (spec:85). SA-4 (spec:149) allows changes that "correct a documented defect", which is not defined.
- Expert: Wiegers, Cockburn.
- Recommendation: gate the pre-creation contract under `--unattended` or the new output flag, or add the three changes to SA-4's named list explicitly.
- Priority: Medium. Quality-impact estimate: low.

### M-08 (MAJOR label, Medium by consequence): D1's "testable by grep" test matches quoted text

- Location: D1 (spec:228): "It is testable by grep and cannot misfire on a person." The example at spec:228 quotes the topic string.
- Attack (Whittaker FR-2.3, sentinel collision). A brief or spec passed as a quoted argument that mentions `--unattended` (for example a worker brief that quotes a sibling command line) makes a grep-based check switch to unattended mode, turning gates off in a run a person did not configure. The command-side rule (a standalone token outside quotes, from the command file's Unattended section) is not stated in the spec.
- Expert: Whittaker (lead on this point), Nygard.
- Recommendation: state the standalone-token rule in D1 and in WC-2.
- Priority: Medium. Quality-impact estimate: low to medium.

### M-09 (MINOR label, Medium by consequence): the reflect headless trigger changes with `--unattended`

- Location: SA-6 (spec:151) says `--unattended` "reuses" the headless rule. Section 3.1 (spec:88) and section 3.2 (spec:122) use it to switch remediation to auto-accept. INV-B:109 defines the headless branch by `claude --print` with no TTY, and the spec does not say `--unattended` changes that trigger.
- Expert: Nygard, Wiegers.
- Recommendation: state that `--unattended` selects the auto-accept branch, and say which registers auto-accept covers.
- Priority: Medium. Quality-impact estimate: low.

## Architecture analysis

=== ARCHITECTURE ANALYSIS ===

### M-10 (MAJOR label, Medium by consequence): the tasklist row relies on an unverified nesting claim and drops a recommended change

- Location: spec:122 gives "Other required change: none (its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`)". INV-B:215 recommends that the per-phase reflect fan-out "must run at the worker's top level, not inside subagents." INV-B:210 and INV-B:314 say nested spawning is UNVERIFIED. The spec's own section 1.4 item 3 says there is "no proven limit" (spec:45).
- Contradiction, conditional. The row treats an external docs claim (INV-A:14, the vendor documentation, UNVERIFIED here) as settled, while the spec's own evidence section does not settle it.
- Expert: Fowler (lead), Newman.
- Recommendation: either adopt INV-B:215 (move the fan-out out of subagents), or keep the row and add an acceptance check that proves the nested reflect fan-out runs in a worker.
- Priority: High. Quality-impact estimate: medium.

### M-11 (MAJOR label, Medium by consequence): the rejected alternative's benefits are not delivered for dynamic internal fan-out

- Location: spec:39 says the coordinator gets per-unit liveness and retry "by splitting the work into separate worker Tasks." Section 3 keeps the dynamic internal fan-outs inside commands: adversarial with 2-10 generator agents (INV-A:35), cleanup-audit with 7-8 concurrent agents (INV-A:42), reflect Tier 2 (INV-B:112). Section 3 does not name a split rule for any of them.
- Trade-off not stated. The spec does not say that these fan-outs keep the cost the rejected alternative was meant to avoid, nor which fan-outs stay internal by design.
- Expert: Fowler.
- Recommendation: list which fan-outs stay internal and accept that the coordinator sees one liveness record for each, or give a split rule.
- Priority: Medium. Quality-impact estimate: medium.

### M-12 (MAJOR label, Medium by consequence): one worktree, one fixed output, no serialization

- Location: spec:85 says cleanup-audit "output dir is fixed, so one audit per worktree at a time (WC-11)." WC-11 (spec:69) says only that default output paths carry a timestamp or slug. The coordinator starts ready Tasks itself (CAPS:92), and Orca's ready view (CAPS:86) does not serialize them. The brief template in section 2.3 has no field for this.
- Concrete case. Two `/sc:cleanup-audit` tasks that are both ready, in one worktree, write the same `.claude-audit/` directory. Also AC-3.4 (spec:207) has two workers in one worktree writing `/sc:save` keys.
- Expert: Hohpe (lead on concurrency), Fowler.
- Recommendation: add a per-worktree exclusion to section 2.3 (the brief names an exclusive resource), and an acceptance check that two ready cleanup-audit tasks are not started together.
- Priority: Medium. Quality-impact estimate: medium.

### M-13 (MINOR label, Medium by consequence): the rejection of the alternative leans on an untraced enforcement point

- Location: R1 (spec:33) says a command calling `worker-start` from inside a worker "would be refused with `nested_worker_depth_exceeded`", and admits which call sites enforce the check is UNVERIFIED (CAPS:103). R2 to R5 still support the rejection on their own.
- Expert: Newman, Nygard.
- Recommendation: say that R1 is contingent on depth 1 (D5) and that R2 to R5 carry the decision.
- Priority: Low. Quality-impact estimate: low.

## Whittaker adversarial analysis

I can break this specification by **FR-2.2 Divergence Attack**. The invariant at **spec:61 and spec:109** fails when **the gate resolves as blocked on an implement halt and the worker holds a preamble**, because both branches apply at once. Concrete attack: the worker takes the WC-3 branch, the coordinator relays an answer, and the re-invocation records it as the Ruling. Severity: CRITICAL (see F-01).

I can break this specification by **FR-2.1 Zero/Empty Attack**. The invariant at **spec:63** fails when **the contract file exists but is empty or has no `status`**. Concrete attack: the file is zero bytes, the "otherwise" branch sets `--outcome succeeded`, and the coordinator reads no content. Severity: MAJOR (see M-01).

I can break this specification by **FR-2.4 Sequence Attack**. The invariant at **spec:62 and spec:73** fails when **`worker_done` is sent before the contract is complete**. Concrete attack: the worker sends `worker_done` after `write` begins, the coordinator reads a truncated YAML file. Severity: MAJOR label, Medium by consequence (see M-05).

I can break this specification by **FR-2.3 Sentinel Collision Attack**. The invariant at **spec:228** fails when **`--unattended` appears inside a quoted argument**. Concrete attack: a brief quotes a sibling command line, the grep-based check switches to unattended mode, and gates turn off in a person's run. Severity: MAJOR label, Medium by consequence (see M-08).

I can break this specification by **FR-2.5 Accumulation Attack**. The invariant at **spec:85 and spec:69** fails when **two cleanup-audit tasks write one fixed output directory**. Concrete attack: two ready tasks in one worktree both write `.claude-audit/pass1-summary.md`, and the second overwrites the first. Severity: MAJOR label, Medium by consequence (see M-12).

## Guard Condition Boundary Table (FR-10 mandatory)

The spec contains guard conditions, so this table is required. Every per-command gate row in sections 3.1 and 3.2 names a resolution (checked), so they are covered as one family, with the rows that need an entry shown. Status key: OK = the spec states the behavior; GAP = blank, undefined, or conflicting (FR-8 finding; blocking only where a finding above says so).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G-01 WC-5 outcome | spec:63 | Zero/Empty: no report | no file | failed | "no report exists" gives failed | OK |
| G-02 WC-5 outcome | spec:63 | Zero/Empty: report exists, status missing or empty | `status` absent | otherwise: succeeded | "otherwise" applies; wrong outcome | GAP (M-01) |
| G-03 WC-5 outcome | spec:63 | Sentinel: status outside four-value set | `complete`, `error` | otherwise: succeeded | "otherwise" applies; wrong outcome | GAP (M-01, M-04) |
| G-04 WC-5 outcome | spec:63 | Typical: partial | `partial` | succeeded | stated | OK |
| G-05 WC-5 outcome | spec:63 | Typical: blocked | `blocked` | failed | stated | OK |
| G-06 WC-3 ask | spec:61 vs spec:109 | Edge: implement Ruling gate | `E-HALT-QA` | ask allowed (WC-3) vs Ruling unchanged | two texts conflict | GAP (F-01, blocking) |
| G-07 WC-3 ask timeout | spec:61 | Zero/Empty: `--timeout-ms` omitted | no value | resume same message ID | default value unstated (CAPS:68, UNVERIFIED) | GAP (minor; the ID is what matters) |
| G-08 WC-2 gate | spec:60 | Zero/Empty: no default, no flag | none | blocked | stated | OK |
| G-09 spec-panel gate | spec:120 | Sentinel: target_release empty or placeholder | `""`, `TBD` | blocked only for absent | empty string and placeholder unstated | GAP (minor) |
| G-10 WC-4 contract | spec:62 | Zero/Empty: crash before write | no contract | no report, so failed (WC-5) | stated through WC-5 | OK |
| G-11 WC-4 blocked | spec:62 | Zero/Empty: blocked, no `blocked_question` | `blocked_question` absent | nothing to answer | "when blocked" requires the field; no check | GAP (M-02) |
| G-12 WC-9 outward | spec:67 | Zero/Empty: no authorization | no flag | off | stated | OK |
| G-13 WC-9 outward | spec:67 vs spec:244 | Typical: flag written without user instruction | `--post-pr` | on | who may authorize is D4 (open) | GAP (N-03, D4 open) |
| G-14 WC-10 wait | spec:68 | Edge: single wait exactly 5 min | 300 s | no split required, heartbeat due | "longer than 5 minutes" | GAP (N-01) |
| G-15 WC-10 wait | spec:68 | Maximum: single wait longer than 5 min | 301 s or more | split into waits of at most 4 min | stated | OK |
| G-16 7.2 step 3 wait | spec:182 | Zero/Empty: no event within 900000 ms | none | loop | no timeout rule; wait blocks heartbeat check | GAP (F-02) |
| G-17 7.2 step 3 wait | spec:182 | Typical: question returned | `question` | no branch | step has no branch for question | GAP (F-02) |
| G-18 WC-12 fenced | spec:70 | Typical: check returns consumer_fenced | `consumer_fenced` | worker stops, no worker_done | coordinator reaction unstated | GAP (N-06) |
| G-19 WC-8 depth | spec:66 | Maximum: depth raised (D5) | depth 2 | no worker-start | absolute rule | OK |
| G-20 D1 flag | spec:228 | Sentinel: `--unattended` inside quoted argument | quoted text | unattended on | grep-testable, no quote rule | GAP (M-08) |
| G-21 implement halt | spec:109 | Typical: E-HALT-QA | halt | stop, ledger and contract blocked, outcome failed | stated | OK |
| G-22 cli-eval run | spec:104 | Zero/Empty: no `--suite` | none | blocked | stated | OK |
| G-23 cli-eval run | spec:104 | Sentinel: `--suite` names a missing suite | unknown name | unstated | not stated | GAP (minor) |
| G-24 standalone | spec:148 and spec:92 | Edge: workflow pre-creation STOP, no flag | no flag | new contract written (ungated P1) | conflicts SA-3 | GAP (M-07) |
| G-25 standalone | spec:146 | Typical: no flag, no new output flag | none | unchanged | stated | OK |
| G-26 retry | not in spec | Maximum: 3 consecutive failures | 3 | Task failed (CAPS:116) | not stated in spec, Orca-enforced | GAP (minor) |

Rows left out, with reasons: no separate empty-string row for G-08 (covered by G-09); no "Maximum" row for WC-1 because the 60 s readiness limit is enforced by Orca (CAPS:44-45) and the spec defers to it.

Pipeline Dimensional Analysis: not triggered. The spec describes dispatch and reporting, with no data stage whose output count may differ from its input count. The cleanup-audit batching (INV-A:42) is inside a command that section 3 does not change. No Quantity Flow Diagram is produced.

Focus-correctness artifacts (State Variable Registry, correctness Guard table, Pipeline Flow Diagram): not produced, because `--focus correctness` is not active.

## Quality metrics (0-10)

- Clarity: 6. Dense cross-references and several rows that mix a resolution with a phase. Acronyms (WC, AC, D, CAPS) are defined in the citation conventions, which helps.
- Completeness: 6. The per-command table covers every command, but the blocked-outcome path, the retry directory, and status mapping are missing (M-02, M-03, M-04).
- Testability: 5. AC-0.4 and 7.2 cannot pass as written (F-02, F-03), AC-1.1 conflicts with the load decision (F-04), and AC-C1 has a case gap (M-06).
- Consistency: 5. Two blocking contradictions (F-01, F-04), one conditional conflict on evidence (N-02), and the tasklist row against its own evidence section (M-10).

## Follow-up candidates (Medium and minor; not blocking; not in the reviser brief)

Medium (listed above as M-01 to M-13 by number; no further action in this loop). The session that ran this review must ask the user once whether to open issues for them. This worker creates none.

Minor notes:
- N-01: WC-10 (spec:68) says "longer than 5 minutes" triggers the split, but the heartbeat is due every 5 minutes. Say "4 minutes or more".
- N-02: E3 (spec:23) cites a `skill-direct` run as evidence the decision has worked, while 1.4 item 1 (spec:43) says the only end-to-end proof is PR #329, which used the nested route. INV-A:13 records the skill-direct run (UNVERIFIED for the file outside the workspace). Make the evidence statement consistent with the direct route being unproven.
- N-03: WC-9 (spec:67) reads as settled, but D4 (spec:244) leaves who may authorize an outward action open.
- N-04: the pr-submit SKILL.md range is cited as 46-64 (spec:68, spec:114), 41-64 (INV-B:299), and 46-48 (spec:283, UNVERIFIED item 12). Use one range.
- N-05: WC-11 (spec:69) paraphrases CAPS:115 as "share the current worktree by default". CAPS:115 says "Use the current or an exact existing workspace by default."
- N-06: WC-12 (spec:70) says the worker stops on `consumer_fenced`, but the coordinator's reaction is unstated.
- N-07: AC-C5 (spec:176) uses `master...HEAD`. The fork's master may be ahead of local master (UNVERIFIED, outside workspace).
- N-08: E2 (spec:22) says the EVIDENCE worker "answered". CAPS:49 quotes only the start result (UNVERIFIED for the evidence file).
- N-09: the troubleshoot ready row (spec:91) does not mention that `--depth deep` with a short input stops (INV-B:239).

## Reviser brief

Blocking finding ids for this loop: F-01, F-02, F-03, F-04. Revise only text that these findings name. Rule (restated from the command's review loop, step 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not part of this brief.

Brief clauses overridden: none.

verdict: FAIL
