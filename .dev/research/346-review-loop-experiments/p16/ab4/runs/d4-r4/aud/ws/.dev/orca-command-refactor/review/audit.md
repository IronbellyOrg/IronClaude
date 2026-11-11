review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (whole-document audit, first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full before reviewing)
- candidate sha256: `e08236b563e957f919d430bee09f668cc4d154a475a77554660dd7026ed73de4` (59200 bytes, 285 lines)
- baseline: not given, not re-review; this is a first review of the whole document (`baseline: missing` does not apply, neither flag was passed)
- reviewer model actually used: claude-sonnet-5-5
- mode flags: no `--unattended`, no `--improve`; the Improve step is skipped and no revised specification is written (Review Loop bullet 4: one review per run)
- brief clause overrides: none. The brief narrows nothing and widens nothing.
- evidence available: `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md` (cited `INV-A:N`, `INV-B:N`, `CAPS:N`, `README:N`, `SPEC:N` = spec line N). Every citation into `src/`, `~/.claude/`, `.dev/codegraph-migration/`, `.dev/evals/`, `CLAUDE.md`, `Makefile`, `pyproject.toml` or Orca's installed files cannot be opened in this sandbox and is UNVERIFIED unless an inventory quotes it. Citations of the form `INV-x:N` and `CAPS:N` were opened and checked.
- panel: Wiegers (lead, requirements), Adzic, Cockburn, Fowler (lead, architecture), Newman, Hohpe, Nygard, Whittaker (active in every panel). Crispin, Gregory and Hightower are outside the two focus areas and were not convened.

## Coverage statement

Covered: all of SPEC:1-285. Checked every `INV-A`, `INV-B` and `CAPS` citation in sections 1, 2, 3, 4 and 9 against the three inventories (about 120 distinct citations): no wrong line found. Checked the 43 = 10 + 27 + 6 partition against `INV-A:73`, `INV-B:278`, SPEC:78-126 and SPEC:131-137: it holds, each command is in exactly one table. Checked the phase assignment of all 37 non-coordinator commands (SPEC:156-162 against the Phase column of SPEC:81-125): every command has one phase or "None". Not covered: anything that needs the source tree (the quoted `cmd/` and `sk/` lines are carried from the inventories, which say they were citation-checked, `INV-A:106`, `INV-B:320`; this reviewer could not re-open them). The spec's own claim of an independent check (SPEC:11, SPEC:285) is not verifiable here and is not relied on.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, newman, hohpe, nygard, whittaker]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 7.5
  clarity: 8
  completeness: 7
  testability: 7
  consistency: 7
critical_issues:
  - id: F-1
    category: requirements/consistency
    severity: CRITICAL
    blocking: true
    expert: wiegers
    issue: Phase 1 acceptance test and Phase 1 scope require the unattended section on 22 commands that the spec assigns to P2, P3 and P4, including three whose content waits for user decisions D2-D4.
expert_consensus:
  - The decision (Orca coordinates, commands stay units of work) is well supported by CAPS:97-103, CAPS:147-150 and INV-A:13-14; it needs no change.
  - The per-command table is accurate against the inventories; the defects are in the phase plan and in a few unstated edge behaviours.
improvement_roadmap:
  immediate: [F-1]
  short_term: [M-1, M-2, M-3, M-4, M-5]
  long_term: [M-6, M-7, M-8, M-9, M-10, M-11]
adversarial_analysis: see Whittaker findings below (W-1 to W-4)
```

## Prior blocking findings

None (first review).

=== REQUIREMENTS ANALYSIS ===

### F-1 (blocking): the Phase 1 test and scope contradict the per-command phases and decisions D2-D4

- severity: CRITICAL (two stated texts contradict each other)
- expert: Wiegers (consistency, traceability), confirmed by Fowler and Adzic
- priority: High
- quality impact: Completeness 7 to 9, Consistency 7 to 9 once resolved

Grading sentence. An implementer who follows the stated text as written builds, in Phase 1, an `## Unattended mode` section on every command in sections 3.1 and 3.2 except `load`, because AC-1.1 asserts exactly that (SPEC:195) and the Phase 1 scope says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load`" (SPEC:159); and that is wrong because the same document assigns 22 of those commands to Phases 2, 3 and 4 (SPEC:97-125 Phase column, SPEC:160-162), says Phases 1-3 "need no user decision; Phase 4 waits for answers to D2-D4" (SPEC:154), and for `/sc:pr-submit` recommends D3 option (a) with "no pr-submit changes in Phase 4" (SPEC:240).

Trace.
1. SPEC:195 (AC-1.1): "every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". Set size: 10 ready + 27 needing a change - 1 (`load`) = 36 commands.
2. SPEC:159 (Phase 1 command list): analyze, build, business-panel, design, document, explain, index, test, load (usage line only), plus fixes to adversarial, cleanup-audit, index-repo, workflow = 13 commands. The sections 3.1 rows for brainstorm and init-lite say "None" for the small fix (SPEC:84, SPEC:87), so they join only through the blanket sentence. Phase 2 lists 15 (SPEC:160), Phase 3 lists 4 (SPEC:161), Phase 4 lists 3 (SPEC:162). 13 + 15 + 4 + 3 + 2 = 37 = 10 + 27, so the 22 commands in the P2 (15), P3 (4) and P4 (3) groups get their section only in a later phase by the table, but in Phase 1 by AC-1.1. Phase 1 cannot pass AC-1.1 without editing them.
3. The Phase 4 commands make it concrete. The pr-submit row (SPEC:114) puts its gate resolutions in P4, and SPEC:240 recommends no pr-submit change at all (D3 option a). The post-release row (SPEC:113) depends on D4 (SPEC:244-247) and the implement row (SPEC:109) on D2 (SPEC:232-236). A section written in Phase 1 must either leave those gates unresolved (then it is not the section the P4 rows describe) or decide D2-D4 early (then SPEC:154 is false).
4. Under D3 option (a), the recommendation, `/sc:pr-submit` stays coordinator or person only (SPEC:240), yet AC-1.1 requires it to carry an unattended section. SPEC:138-139 itself calls it a worker candidate "only if the user accepts" D3.

Recommendation. Narrow, do not add. Restate AC-1.1 and the Phase 1 sentence to the commands the Phase column assigns to P1 (the 13 above, with `load` excluded), and let each later phase's own check assert its own commands. Do not add new text beyond that. Rationale: the Phase column is the detailed, evidence-cited statement and the rest of the plan (SPEC:154, SPEC:160-162, AC-2.1 to AC-4.3) is built on it.

### M-1 (Medium): the report path is undefined when `--unattended` is passed with no output flag

- severity: MAJOR label, graded Medium (a requirement the document never states; no stated text does harm)
- expert: Wiegers, Whittaker (FR-2.1 zero/empty attack)
- priority: Medium
- location: WC-4 (SPEC:62), section 2.3 (SPEC:73)
- WC-4 says where the contract goes "when the coordinator passed a directory", "when `--output` names a file", or "at the fixed path its section 3 row names". Section 2.3 puts the duty on the brief. The command's own behaviour when none of the three applies (a coordinator error, or a fixed-path-less command like analyze before it gains `--output`) is not stated, although WC-4 also says the contract is "written on every outcome, including stops before any other output exists". Suggested narrowing: one sentence, "with no output flag the command writes the contract to the command's default output location, or refuses at once and says so in chat". Medium because it needs a guess about which of two reasonable readings the implementer picks.

### M-2 (Medium): `--unattended` token parsing and behaviour on commands that do not accept it are unstated

- severity: MAJOR label, graded Medium
- expert: Whittaker (FR-2.3 sentinel collision), Adzic
- location: section 2.1 (SPEC:51), section 4 (SPEC:128), SPEC:159
- Attack. Run `/sc:tdd "add --unattended support to the exporter" --output f.md`: nothing in the spec says whether `--unattended` inside quoted specification or prompt content counts as the switch. Run `/sc:git status --unattended` or `/sc:load --unattended`: section 4 says the six "get no `--unattended` mode" and SPEC:159 excludes `load`, but what the command does with the flag (ignore, refuse, treat as text) is not stated. Both leave the invariant "the switch is on only when the coordinator wrote it" unspecified. A SPEC-conformant but different token rule in 36 commands would diverge. Suggested: one sentence in the contract file requirement (section 2.1): the switch is a standalone argument token outside quoted content; on a command with no mode it is refused with a one-line message.

### M-3 (Medium): `/sc:task` commit and push are "refused unless authorized (WC-9)" but WC-9 names no authorization mechanism for them

- severity: MAJOR label, graded Medium
- expert: Nygard, Wiegers
- location: task row (SPEC:121), WC-9 (SPEC:67); `INV-B:204` ("EXEMPT keywords include `commit` and `push`, which run immediately with no skill")
- WC-9 turns an outward default back on "only through the command's own explicit flag written in the brief". The inventory shows `/sc:task` commit and push are triggered by keywords in the request text, not by a flag. The row therefore has no flag to name. The same applies to the TFEP "committed to git" step (`INV-B:204`). The text does not say what an authorized `/sc:task commit` looks like. Medium: the default-off half is clear and safe; only the authorized path is open.

### M-4 (Medium): the contract `status` vocabulary can collide with the `status` field of contracts that already exist

- severity: MAJOR label, graded Medium
- expert: Hohpe, Wiegers
- location: WC-4 (SPEC:62), decision table (SPEC:262), step 4 of 7.2 (SPEC:183)
- WC-4 fixes `status` to `succeeded|partial|failed|blocked` and also says commands that already write a contract "keep their fields and add the missing ones". The inventories show existing contracts for adversarial, brainstorm, reflect, workflow (`INV-A:97`, `INV-B:112`, `INV-B:272`) but do not list their `status` values; the spec rejects "copy each command's own statuses" (SPEC:262) without showing they already match. If an existing `status` value differs, "keep their fields" and the 7.2 step 4 assertion (`d['status'] in {...}`) cannot both hold. UNVERIFIED (the contracts are outside the sandbox). Suggested: say whether a differing existing value is mapped or written in a new field; check the four existing contracts once in Phase 1.

### M-5 (Medium): workflow's two contracts and an undefined `--output <file>`

- severity: MAJOR label, graded Medium
- expert: Cockburn, Hohpe
- location: workflow row (SPEC:92), WC-4 (SPEC:62), AC-0.4 (SPEC:194)
- WC-4 lists workflow among the commands whose fixed section 3 path overrides the dir and file rules. The row instead adds a new `--output <file>`, writes a second contract at `<file>.return-contract.yaml`, and keeps the package contract. Two contracts exist for one run, and the spec does not say which is the `worker_done --report-path`. It also does not say what, if anything, is written at `<file>` itself. Pre-P1 the report path is the package contract (AC-0.4), post-P1 it is the file contract, so the path the coordinator reads changes between phases. Suggested narrowing: state the single contract to pass to `--report-path` for workflow in each phase.

### M-6 (Medium): `/sc:reflect` is "ready" but its default writes a tracked file and moves folders

- severity: MAJOR label, graded Medium
- expert: Nygard, Newman
- location: reflect row (SPEC:88), WC-11 (SPEC:69); `INV-B:114`
- `INV-B:114` records that reflect writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and performs a default-on Wave 7 folder move in UC-2. The row handles only the move (`--no-promote`). Two reflect workers with the same slug in one worktree write the same tracked file, which WC-11 ("two workers in one worktree must never write the same file") forbids. The spec does not say how the brief avoids this. Medium: reflect with distinct slugs is fine; the requirement is simply not stated.

### M-7 (Medium): decision D4 governs behaviour that Phase 2 builds before D4 is decided

- severity: MAJOR label, graded Medium
- expert: Wiegers, Cockburn
- location: D4 (SPEC:244-247), auggie-review row (SPEC:100), task row (SPEC:121), SPEC:154
- D4 option (b) "Never: workers make no outward changes" would remove the `--post-pr` and commit/push return paths that the auggie-review and task rows (Phase 2) write as authorized by "an explicit flag in the brief". The spec says Phases 1-3 need no user decision (SPEC:154) but D4's own header lists auggie-review `--post-pr` and task commit/push as affected (SPEC:244). The default-off part (WC-9) does not depend on D4, so Phase 2 can proceed; the "returns only with an explicit `--post-pr`" clause does. Suggested: say Phase 2 implements the default-off half and defers the authorized path to D4. Also UNVERIFIED that a `--post-pr` flag exists (`INV-A:38` records only `--no-post-pr`, the inverse).

=== ARCHITECTURE ANALYSIS ===

### M-8 (Medium): the long-wait rule does not say what happens to an Agent-tool call that blocks for longer than five minutes

- severity: MAJOR label, graded Medium
- expert: Nygard, Fowler
- location: WC-10 (SPEC:68) against WC-7 (SPEC:65); `CAPS:130`, `CAPS:155`
- WC-10: "A command step that blocks a single tool call for longer than 5 minutes ... must be split into waits of at most 4 minutes". WC-7: "A command's own Agent-tool fan-out stays as it is." An Agent-tool (Task) fan-out is a single tool call in the worker's top-level session and routinely lasts longer (cleanup-audit waves, tdd research, `INV-A:42`, `INV-B:47`). The text allows two readings: WC-10 covers only polls and evals (the named examples), or it covers every long call and so contradicts WC-7. The evidence that heartbeats matter at all is itself unverified (`CAPS:130`: cadence comes from this run's preamble; whether Orca uses heartbeat age is UNVERIFIED). Medium because the implementer must guess the reading, and the examples point to the narrow one. Suggested: add "(shell or poll waits; Agent-tool calls are exempt)" if that is the intent.

### M-9 (Medium): `/sc:tasklist` is declared inside Claude Code's nesting limit without counting layers

- severity: MAJOR label, graded Medium
- expert: Fowler, Newman
- location: tasklist row (SPEC:122), cites `INV-A:14`; contrast `INV-B:210`, `INV-B:314`
- The row asserts that the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit". `INV-A:14` states the limit (three layers below the main conversation, tool withheld at the limit). `INV-B:210` and `INV-B:314` record that subagent-to-agent spawning in this path is UNVERIFIED. Reflect Tier 2 adds reviewers and then adversarial advocates below each Stage 10.5 reflect subagent, so the real depth is more than one. No layer count is given. The row also sends `--unattended` to reflect, whose headless auto-accept rule does not say how a `needs_human_decision` HALT (`INV-B:209`) resolves; SPEC:88 changes only the `[yes / no]` prompt. Medium: the failure would show in the Phase 2 live check, but the row states a fact the evidence marks unverified.

### M-10 (Medium): AC-C1 scans `src/superclaude/core`, which Phase 0 edits to add Orca guidance

- severity: MAJOR label, graded Medium
- expert: Fowler, Wiegers
- location: AC-C1 (SPEC:172), P0 (SPEC:158), 2.3 (SPEC:73), 7.2 (SPEC:180-186)
- AC-C1 requires no match for `orca(-ide) (orchestration|worktree|terminal|agent)` in commands, skills, agents and core, excluding only `ccsession-tag`. Phase 0 adds an Orca section to `HOW-WE-WORK.md` and a coordinator brief template to `WORKER-CONTRACT.md`, both under `core`. If either names an Orca coordinator command in that form (the 7.2 steps show the natural wording), AC-C1 fails Phase 0 itself. Whether they do is a guess. Suggested: scope AC-C1 to commands, skills and agents, or exempt the two named core files.

### M-11 (Medium): a pass condition cites a check that is not defined

- severity: MAJOR label, graded Medium
- expert: Adzic, Whittaker
- location: AC-0.4 (SPEC:194), 7.2 step 5 (SPEC:184), 1.4 gap 1 (SPEC:43)
- AC-0.4 says each smoke command is "run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)". Step 5 only searches the transcript for `AskUserQuestion`, and a plain text search would also match skill text that says "never AskUserQuestion" (`INV-B:239`). No step defines how a wrapper is told apart from a command's own legitimate Agent-tool fan-out (troubleshoot Tier 2, `INV-B:241`). The criterion that closes evidence gap 1.4(1) has no executable check. Suggested: add to step 5 "the first tool call after the preamble is the Skill or slash-command invocation in the worker's own session" and make the `AskUserQuestion` check "a tool call named", not a text match.

## Whittaker adversarial findings (FR-3 format)

**W-1.** I can break this specification by **Zero/Empty Attack (FR-2.1)**. The invariant at **WC-4 and section 2.3 (SPEC:62, SPEC:73)** fails when **`--unattended` is passed with no directory, no file and no fixed section 3 path**. Concrete attack: before: `/sc:analyze src/x.py --unattended`, analyze has no output flag until P1 (SPEC:99); after P1 it has `--output`, absent here; state trace: contract path = undefined, `status` field cannot be written, "written on every outcome" is unsatisfiable, `worker_done --report-path` has no real value (CAPS:74 forbids placeholders). Severity: MAJOR, graded Medium (see M-1).

**W-2.** I can break this specification by **Sentinel Collision Attack (FR-2.3)**. The invariant at **section 2.1 (SPEC:51)** ("the behaviour a command switches to when its caller passes `--unattended`") fails when **the string `--unattended` occurs inside quoted prompt content**. Concrete attack: `/sc:tdd "document how --unattended works" --output t.md`; before: interactive default; after: if the token is matched as a substring, gates are skipped for a person's own run, breaking SA-1 (SPEC:146). Severity: MAJOR, graded Medium (see M-2).

**W-3.** I can break this specification by **Sequence Attack (FR-2.4)**. The invariant at **section 6 ordering (SPEC:154) and AC-1.1 (SPEC:195)** fails when **Phase 1 is executed in the order the document states**. Concrete attack: complete P0; execute P1 as scoped by SPEC:159 (13 commands); run AC-1.1 over 36 commands: it fails for the 22 later-phase commands; to pass it the implementer edits `pr-submit`, `implement` and `post-release` before D2-D4 are answered. State trace: sections present 14 of 36 (12 P1 commands that get one, plus brainstorm and init-lite through the blanket sentence); P1 gate cannot open (SPEC:154 "Later phases do not start until the earlier phase's checks pass"). Severity: CRITICAL (two stated texts contradict); this is F-1.

**W-4.** I can break this specification by **Accumulation Attack (FR-2.5)**. The invariant at **WC-6 (SPEC:64) and WC-4 (SPEC:62)** fails when **a retry worker (`worker-start --retry-of`) re-runs a command that has a resume flag and the same output path**. Concrete attack: attempt 1 writes `<dir>/return-contract.yaml` with `status: failed`; attempt 2 resumes and overwrites it with `succeeded`; the coordinator, reading after attempt 1's `worker_done`, may open attempt 2's file or the reverse. WC-6 protects the output only for commands without a resume flag ("fresh output directory"). Whether a retry may overwrite the first contract is unstated. Severity: MAJOR, graded Medium (listed with M-5 as a path-semantics follow-up, not a separate id).

## Guard Condition Boundary Table (7 columns)

Triggered: the spec contains conditional logic, thresholds and sentinel comparisons. Responsibility: Nygard (construction), Crispin's completeness check is folded in by Wiegers (Crispin was not convened for these focus areas), Whittaker (attack). Classes left out are stated per guard with a one-line reason. Every guard is enumerated and every cell is populated, so FR-10 is met.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| unattended switch | 2.1, WC-2 (SPEC:51, 60) | Zero/Empty | flag absent | false | SA-1: every prompt and default as today (SPEC:146) | OK |
| unattended switch | 2.1 (SPEC:51) | One/Minimal | flag present, no output flag | true | not stated (see M-1) | GAP |
| unattended switch | 2.1, 3.1 (SPEC:81) | Typical | flag plus `--output <dir>` | true | contract at `<dir>/return-contract.yaml` (SPEC:62) | OK |
| unattended switch | 2.1 (SPEC:51) | Sentinel Value Match | `--unattended` inside quoted content | unspecified | not stated (see M-2) | GAP |
| unattended switch | 4 (SPEC:128) | Legitimate Edge Case | flag passed to a coordinator-only command or to `load` | unspecified | "get no mode" but the response to the flag is not stated (see M-2) | GAP |
| unattended switch | - | Maximum/Overflow | omitted | n/a | boolean flag, no capacity | OK |
| report path | WC-4 (SPEC:62) | Zero/Empty | no dir, no file, no fixed path | unspecified | not stated (M-1) | GAP |
| report path | WC-4 (SPEC:62) | One/Minimal | `--output` names a file | true | `<file>.return-contract.yaml` | OK |
| report path | WC-4, 3.1 (SPEC:83-86, 92) | Legitimate Edge Case | fixed section 3 path and `--output` both apply (workflow) | true | fixed path overrides, but workflow row writes a second contract (M-5) | GAP |
| report path | WC-6, WC-4 (SPEC:62, 64) | Sentinel Value Match | contract already exists from an earlier attempt | true | resume commands: overwrite unstated (W-4); non-resume: fresh dir | GAP |
| outcome mapping | WC-5 (SPEC:63) | Zero/Empty | no report file | true | `--outcome failed` | OK |
| outcome mapping | WC-5 (SPEC:63) | One/Minimal | `status: blocked` or `failed` | true | `--outcome failed` | OK |
| outcome mapping | WC-5, decisions (SPEC:63, 263) | Typical | `succeeded` or `partial` | true | `--outcome succeeded`, body names the status | OK |
| outcome mapping | WC-5 (SPEC:63) | Legitimate Edge Case | audit verdict FAIL with status succeeded | true | `--outcome succeeded` | OK |
| outcome mapping | WC-4 (SPEC:62) | Sentinel Value Match | existing contract whose `status` is outside the four values | unspecified | not stated (M-4) | GAP |
| long-wait split | WC-10 (SPEC:68) | Zero/Empty | no wait in the command | false | no rule needed | OK |
| long-wait split | WC-10 (SPEC:68) | Typical | poll wait of 4 minutes | false | session heartbeats between waits | OK |
| long-wait split | WC-10 (SPEC:68) | Maximum/Overflow | one Agent-tool call longer than 5 minutes | unspecified | not stated (M-8) | GAP |
| long-wait split | WC-10 (SPEC:68), cli-eval row (SPEC:104) | Legitimate Edge Case | eval timeout of 3600 s | true | split into waits of at most 4 minutes | OK |
| nested Orca dispatch | WC-8, R1 (SPEC:66, 33) | One/Minimal | worker calls `worker-start` at depth 1 | true | forbidden; Orca refuses `nested_worker_depth_exceeded` (CAPS:99) | OK |
| nested Orca dispatch | D5 (SPEC:249-253) | Legitimate Edge Case | depth setting raised | true | WC-8 still forbids a command calling Orca | OK |
| outward default | WC-9 (SPEC:67) | Zero/Empty | no authorization flag | false | default off | OK |
| outward default | WC-9, task row (SPEC:67, 121) | Legitimate Edge Case | authorization wanted for `/sc:task` commit or push | unspecified | no flag exists to name (M-3) | GAP |
| outward default | WC-9, D4 (SPEC:67, 244-247) | Typical | flag written in the brief | true | on for that action only; D4 decides who may write it (M-7) | OK |
| readiness limit | WC-1 (SPEC:59) | Typical | startup prompt with fallback | true | fallback "well inside" 60 s (no number; evidence: 30 s passes, over about 45 s fails, CAPS:49) | OK |
| readiness limit | WC-1 (SPEC:59) | Maximum/Overflow | fallback above the limit | true | worker-start fails at `agent_readiness` (CAPS:44-46) | OK |
| fenced consumer | WC-12 (SPEC:70) | Legitimate Edge Case | `check` returns `consumer_fenced` | true | stop, send no `worker_done` | OK |

Grading of the table (FR-8, FR-9): each GAP above names a missing requirement or an undefined behaviour, not a stated text that causes a wrong outcome, data loss or a safety-boundary break. Per the FIRST-REVIEW grading check they are Medium and sit under follow-up candidates. The GAP rows whose cause is the F-1 contradiction (none in this table) would be blocking; the table's gaps reduce to M-1 to M-8.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered by the multi-stage partition 43 commands to class to phase (a count that divides, FR-17). It is the only count flow in the document; no data pipeline with filtering exists.

```text
[Source: 43 commands (INV-A 21 + INV-B 22)]
   --> [Classify]
        |-- 10 ready      (SPEC:81-92)  -> P1 fixes 4 | P2 fixes 4 | no change 2 (brainstorm, init-lite)
        |-- 27 needs-change (SPEC:97-125) -> P1 9 | P2 11 | P3 4 | P4 3   (N=27, M=27, conserved)
        `-- 6 coordinator-only (SPEC:131-137) -> no phase
   --> [Phase tallies]
        P1 listed 13 (SPEC:159) | P2 listed 15 (SPEC:160) | P3 listed 4 | P4 listed 3 | none 2   = 37 = 10 + 27   (conserved)
   --> [Consumer: AC-1.1 (SPEC:195)]  expects 36 (all of 3.1 + 3.2 except load)   <-- MISMATCH with P1 listed 13 (F-1)
```

The partition itself conserves counts (43 = 10 + 27 + 6; 37 = 13 + 15 + 4 + 3 + 2). The divergence is the consumer: the Phase 1 acceptance test expects 36 where Phase 1 delivers 13 or 15. This is the same defect as F-1 and is graded under it (FR-19 would classify a dimensional mismatch as CRITICAL; it is counted once).

## Expert commentary (condensed, critique mode)

- Wiegers: The requirement set WC-1 to WC-12 is individually testable and each carries an owner and evidence. The one place the requirements disagree with each other is the Phase 1 test (F-1). Traceability from each section 3 row to a phase, a check and an inventory line is good.
- Adzic: The 7.2 live check is the strongest part: seven steps, each with a pass condition. The scenarios would gain a degenerate variant (`--unattended` with no output flag, M-1) and a precise transcript check (M-11).
- Cockburn: Primary actors are clear (coordinator, worker session, command, person). The workflow row mixes two contract files for one goal (M-5).
- Fowler: The architectural decision (SPEC:13-39) is sound and its rejection of the alternative cites four independent Orca facts (CAPS:97-103, CAPS:145-150). Section 1.4 states the evidence gaps plainly, which is the right calibration. The tasklist nesting claim (M-9) and the AC-C1 scope (M-10) are the only places the architecture text goes past its evidence.
- Newman: Versioning and compatibility are handled by SA-1 to SA-6 and the opt-in flag; additive-only edits are enforced by AC-C5. One backward-compatibility detail is open: how `plugins/superclaude/commands/` copies follow (UNVERIFIED item 8, SPEC:279), which the document already flags.
- Hohpe: The message pattern (preamble, `ask`, `worker_done` with `--report-path`, coordinator opens the file) is consistent with CAPS:58-79. The status vocabulary needs reconciling with existing contracts (M-4).
- Nygard: Failure modes are covered well (blocked contract, circuit breaker, fenced consumer, retry). Gaps: the long Agent-tool call (M-8), the tracked-file write in reflect (M-6), and no commit/push authorization route for `/sc:task` (M-3).
- Whittaker: see W-1 to W-4.

Disagreements: Wiegers and Fowler agree F-1 is blocking. Fowler would grade M-9 higher if the layer count exceeds three; with the evidence available it is unverifiable, so it stays Medium.

## Follow-up candidates (Medium and minor, never blocking, never in the Reviser brief)

Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10, M-11 (described above); W-4 folds into M-5.

Minor (notes):
- n-1. WC-4 says flatly "Orca does not check the file" (SPEC:62), while the document's own UNVERIFIED item 3 says the spec "assumes it does not" (SPEC:274) and `CAPS:79` marks it UNVERIFIED. Wording only; the instruction to open the file stands either way.
- n-2. E3 (SPEC:23) cites `invocation_method: "skill-direct"` as evidence the direct route worked, while section 1.4(1) (SPEC:43) says the PR #329 brief used an Agent-tool subagent and so proves only the nested route. The two statements are compatible with `INV-A:13` but the spec does not reconcile them; section 1.4 gives the honest reading.
- n-3. WC-1 says the fallback must be "well inside" the 60 s limit without a number (SPEC:59); `CAPS:49` supports 30 s as working and about 45 s as failing, so a number is available.
- n-4. Section 4 says that for `/sc:git` "workers make no commits or pushes" (SPEC:133), which reads as a rule that D4 option (a) and WC-9 later relax; it is a rationale row, not a requirement.
- n-5. `partial` maps to `--outcome succeeded` (SPEC:63, 263); a coordinator that starts dependents on `completed` Tasks will start them after a partial deliverable unless it reads the report first. Section 2.3 already tells the coordinator to open the report; no change needed.
- n-6. The spec assumes `/sc:research` has a `--strategy planning` value equal to the persona's "Planning-Only" (SPEC:116; `INV-B:129`); the match is not shown. UNVERIFIED.
- n-7. SA-3 (SPEC:148) allows the contract "when the caller passes the new output flag" while WC-4 writes it "in unattended mode"; a run with the output flag only is covered by neither reading clearly.
- n-8. SPEC:11 and SPEC:285 report independent citation checks that cannot be verified here. Not relied on.
- n-9. The command definition used by this audit (`command.md`) already contains `--unattended`, `--report-dir`, a file-valued `--output` and a pointer to `~/.claude/WORKER-CONTRACT.md` for spec-panel, whereas SPEC:120 plans to "add `--output <dir>`" for it. This is a difference between the audit sandbox and the repository state the spec describes; UNVERIFIED which is current. If the sandbox definition is current, the spec-panel row should say `--report-dir`.

The session that ran this review would ask the user once whether to open an issue for the follow-up candidates. This worker has no user channel, so it asks nothing and creates nothing; the coordinator should relay the question.

## Reviser brief

Blocking finding ids: **F-1**

Rules for the reviser (restating Review Loop bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names. For F-1 that is the Phase 1 sentence at SPEC:159 and AC-1.1 at SPEC:195.
- Add no rule, mechanism or section that no blocking finding calls for. Cite the finding id on each added paragraph or table.
- Prefer deleting or narrowing to adding. The suggested repair for F-1 is a narrowing: limit both texts to the commands the Phase column assigns to Phase 1.
- Report the byte size before and after (before: 59200 bytes), and the bytes added and deleted per finding id.
- Leave the Medium and minor items alone. Do not award yourself a PASS.

verdict: FAIL
