review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

## Report header

| Field | Value |
|---|---|
| command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (format `standard`; one review, `--iterations` does not apply) |
| label | whole-document audit of the final spec; a first review of the whole document, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` |
| candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, 59034 bytes, sha256 `466dcf239d1cdea564cc23de1d5abe284de1d002582065afb592d5d4494fa5a3` |
| baseline / prior | none given; not a re-review (`command.md:258`) |
| reviewer model | claude-sonnet-5-5 (Sonnet 5.5) |
| brief clauses overridden | none |
| unattended | no; `--report-dir` not used. The coordinator's brief fixes the output file |

Citation shorthand: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = the sandbox `command.md`. `PROMPTS:N` = the review-loop prompts file. Any citation to a file that is not in the sandbox (`src/...`, `CLAUDE.md:*`, `EVIDENCE.md:*`, `.dev/codegraph-migration/...`, `/opt/Orca/...`, `Makefile`, `pyproject.toml`) is UNVERIFIED here unless an inventory quotes the line, and the quoting inventory line is then the citation.

## Coverage

All 285 lines of the candidate read. About 60 citations checked against the three inventories (the spec's `INV-A`, `INV-B` and `CAPS` ranges resolve to the lines it says they do; no wrong range found). Arithmetic checked: 43 = 10 + 27 + 6 (spec:76; spec:83-92, spec:99-125, spec:132-137; inventory totals INV-A:73 and INV-B:278); the 27 changed commands split 9 + 11 + 4 + 3 across P1, P2, P3 and P4 (spec:99-125 against spec:159-162), and the four ready commands in P2 (reflect, release-split, tdd, troubleshoot) bring the P2 list to 15 as spec:160 says. Guard Condition Boundary Table and Quantity Flow Diagram below. Not covered: any claim whose only source is outside the sandbox (listed under UNVERIFIED). No command was run; no Orca exists here.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7
  completeness: 6.5
  testability: 6
  consistency: 6.5
critical_issues:   # blocking only; full text below
  - {id: F-01, category: requirements/testability, severity: CRITICAL, expert: Wiegers+Crispin, issue: "P0 acceptance check cannot pass for the troubleshoot smoke run"}
  - {id: F-02, category: requirements/consistency, severity: MAJOR, expert: Wiegers+Cockburn, issue: "load is both a P1 command that gains the unattended contract and a command with no report"}
expert_consensus:
  - "The decision (Orca on top, commands stay units of work) is well argued, with a rejected alternative and honest evidence gaps (spec:41-45)."
  - "Evidence discipline is strong: UNVERIFIED items are carried, citations to inventories resolve, counts reconcile."
  - "Weakest area is the acceptance layer (section 7): several checks do not match what section 3 and section 6 say each phase delivers."
improvement_roadmap:
  immediate: [F-01, F-02]
  short_term: [M-01, M-02, M-03, M-04, M-05]
  long_term: [M-06, M-07, M-08, M-09, M-10, M-11, M-12]
adversarial_analysis: "see ADVERSARIAL ANALYSIS; A-1..A-6 map to F-01, M-01, M-02, M-03, M-06, M-08"
```

Grading note (Review Loop bullet 2, `CMD:259`): a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds without a further assumption. Labels below (CRITICAL/MAJOR/MINOR) are the panel's labels; the grade (Blocking, Medium, minor) is by consequence. Several MAJOR-labelled findings are graded Medium for that reason and sit under follow-up candidates.

=== REQUIREMENTS ANALYSIS === (Wiegers lead, Adzic, Cockburn)

### F-01 (Blocking, label CRITICAL; Wiegers, Crispin) The Phase 0 acceptance check cannot pass, and Phase 0 gates every later phase

Where: `spec:194` (AC-0.4), `spec:182` (7.2 step 3), `spec:79` (3.1 intro), `spec:91` and `spec:160` (troubleshoot is a P2 change), `spec:154` (later phases wait for the earlier phase's checks).

Grading check: An implementer who follows the stated text as written runs AC-0.4 on `/sc:troubleshoot "<real symptom>"` (spec:194) and must satisfy 7.2 step 3, which requires that "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path" (spec:182). Troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242), and the spec itself delivers its WC-4 contract in P2 (spec:91, spec:160). So at P0 there is no contract at the WC-4 path and no `status` to compare, step 3 fails, AC-0.4 fails, and spec:154 then forbids starting P1 to P4. That is wrong because AC-0.4 excuses only step 4 ("since the contract arrives in P1", spec:194); the excuse is false for troubleshoot (P2), as is 3.1's "until Phase 1 adds the contract" (spec:79) for troubleshoot, tdd, reflect and release-split (all P2, spec:160). The third smoke command has the same exposure: adversarial's contract filename is "not fixed" until the P1 fix (spec:83, AC-1.4 at spec:198; INV-A:60 shows two different on-disk locations), so step 3's "WC-4 contract path" is not guaranteed in P0 either.

Recommendation (rationale: the P0 pass condition must be one that P0 can meet): state in AC-0.4 that for P0 steps 3 and 4 use each command's existing report file and that `--outcome` is judged against the report's own verdict; keep the WC-4 path check from P1 (adversarial) and P2 (troubleshoot) onward. Narrow, do not add a mechanism. Priority High. Quality impact: testability +1.5, consistency +0.5.

### F-02 (Blocking, label MAJOR; Wiegers, Cockburn) `/sc:load` is listed both ways, and the P1 acceptance checks select it

Where: `spec:112` (load row), `spec:159` (P1 scope), `spec:76` (every changed command gains the section), `spec:195` (AC-1.1), `spec:196` (AC-1.2), `spec:183` (7.2 step 4).

Grading check: An implementer who follows spec:159 builds, for every P1 command named there, the `--unattended` flag and `## Unattended mode` section; spec:159 names `load (usage line only)` in that list, and spec:76 says every changed command gains the section. AC-1.1 then asserts that "every command whose section 3 phase is P1" has a section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md` (spec:195), and AC-1.2 runs 7.2 on "each P1 command with `--unattended --output <dir>`" (spec:196), which requires a contract file that parses with `status` and `command` (spec:183). But the load row says Report: "none", Resume "n/a", and "use it as a step inside another worker's brief, not as its own Task" (spec:112), and the Decisions table says a report file "would be an unrequested addition" (spec:265). Following the load row fails AC-1.1 and AC-1.2; following the AC adds a contract that spec:265 rejects. The same selector problem catches adversarial, cleanup-audit and index-repo, whose 3.1 rows carry "(P1)" for a small fix only (spec:83, spec:85, spec:86), while spec:159 gives them no `--unattended` section. Two stated texts contradict each other.

Recommendation (rationale: remove the contradiction by narrowing, not adding): in spec:159, spec:195 and spec:196 name the exact P1 set that gains the section (analyze, build, business-panel, design, document, explain, index, test), and say load changes its usage line only and the three small-fix ready commands change no flags. Priority High. Quality impact: consistency +1, testability +0.5.

### Follow-up candidates, requirements bucket (Medium or minor; none triggers a revision)

| id | Label / grade | Expert | Issue (cites) | Recommendation and rationale | Priority | Impact |
|---|---|---|---|---|---|---|
| M-01 | MAJOR / Medium | Wiegers | WC-4 fixes the contract path from whether the flag names a directory or a file (spec:62), but 12 section 3 rows only say "add `--output`", "add a report path", "add an output path", "write ... to a file" without saying which (spec:99, 101-103, 106-108, 110, 115, 123). AC-1.2 then passes `--output <dir>` to every P1 command (spec:196), including test and build whose rows say "report path". The case "`--unattended` with no output flag" has no stated behavior, though WC-4 says the contract is written "including stops before any other output exists" (spec:62); only workflow has an exemption. The sandbox's own `/sc:spec-panel` definition splits it as file-valued `--output` plus a directory flag `--report-dir` (CMD:460-461), so the directory flag name is not uniform. | Add one word per row (dir or file) and one sentence for the no-output case (refuse before any work, as CMD:460 does, or block). Needs a reading choice, so not blocking. | High | testability +0.5 |
| M-03 | MAJOR / Medium | Wiegers | WC-4 says commands that already write a contract "keep their fields and add the missing ones" and WC-5 maps `status` over a four-value set (spec:62-63), but brainstorm and workflow rows say "None" (spec:84, spec:92) and `/sc:init-lite` is named as a file-beside-contract user in WC-4 (spec:62) while spec:154 says init-lite is unchanged and never gets `--unattended`. The inventories name only `status`, `plan_path`, `reflect_report_path` for workflow (INV-B:272); the `command`, `report_path` and `artifacts` fields that 7.2 step 4 asserts (spec:183) and the status vocabularies of the brainstorm and reflect contracts are UNVERIFIED. | List the existing contracts' status values, or exempt frozen commands from WC-4/WC-5 and delete init-lite from spec:62. | Medium | consistency +0.5 |
| M-04 | MAJOR / Medium | Adzic | WC-3 lets a worker holding a preamble "instead" ask the coordinator and wait (spec:61), but AC-2.2 requires `worker_done --outcome failed` and a `blocked` contract for the same gate input (spec:200). A live-check worker always has a preamble, so which path it takes is a guess; the brief template (spec:73) does not say whether `ask` is allowed. | Say in 2.3 whether the brief permits `ask`; AC-2.2 assumes it does not. | Medium | testability +0.5 |
| M-05 | MAJOR / Medium | Cockburn | The cli-portify row turns all three approval gates into `blocked` and adds `--resume <contract>` (spec:105), but names no input that records an approval, and the inventory says how a resume is invoked is UNVERIFIED (INV-A:45, INV-A:116). AC-2.3's happy path "with every required flag in the brief" (spec:201) therefore has no defined passing run for cli-portify. | State whether resuming past a gate counts as approval, or add the approval flag the row implies. | Medium | completeness +0.5 |
| M-10 | MAJOR / Medium | Wiegers | Under `--unattended`, release-split resolves only the tasklist-input and `--r1-scope custom` prompts (spec:89), not its `--interactive` checkpoints (INV-B:119); WC-2 says no person-blocking step at all (spec:60). The spec also says nothing about what a command not yet upgraded does with `--unattended` (spec:154 leaves it to the coordinator; no check covers it). | Add "`--interactive` refused" to the release-split row; one sentence on unknown-flag behavior. | Medium | completeness +0.3 |
| M-11 | MINOR / Medium | Wiegers | "calls a paid external run" in WC-9 (spec:67) is not defined; research and review-translation use web search by default (INV-B:134, INV-B:144) and their rows do not say whether it stays on. The research row's `--strategy planning` pin (spec:116) rests on the persona file being loaded, which INV-B:128 and INV-B:316 mark UNVERIFIED; the spec's UNVERIFIED list (spec:271-285) does not carry it. | Define the term; carry the UNVERIFIED item. | Low | clarity +0.3 |
| M-12 | MINOR / Medium | Wiegers | The tasklist row keeps Stage 10.5's reflect `--remediate` and relies on reflect's headless auto-accept under `--unattended` (spec:122, spec:88), whereas the inventory recommended dropping `--remediate` (INV-B:215). What the auto-accept applies is only described as "auto-fixable registers" (INV-B:109), and spec UNVERIFIED #9 says a worker is not headless (spec:280). No Decisions entry records the choice (spec:255-269). | Add a Decisions row with the rationale, or follow INV-B:215. | Low | consistency +0.3 |

=== ARCHITECTURE ANALYSIS === (Fowler lead, Nygard, Newman, Hohpe)

Fowler: the split of responsibilities is sound (commands carry a mode, one shared contract file, the coordinator owns Orca calls; spec:16, spec:52, SA-2 at spec:147). The one coupling to watch is that `--unattended` bundles four behaviors in one switch (no prompts, outward actions off, mode refusals, contract writing; spec:51, spec:60, spec:67, spec:62). Acceptable, but it is why M-01 and M-10 matter. Nygard: failure modes are mostly covered: crash with no report maps to failed (spec:63), stall detection via `agentWait` (spec:181), release rules (spec:186). Gaps are in retries and waits (M-02, M-06, M-08). Newman and Hohpe: the contract is a file-based message with a path rule but no version and no correlation to the dispatch (M-09). No architecture finding reaches blocking grade.

| id | Label / grade | Expert | Issue (cites) | Recommendation and rationale | Priority | Impact |
|---|---|---|---|---|---|---|
| M-02 | MAJOR / Medium | Fowler, Hohpe, Nygard | WC-6 says a command without a resume flag "writes each run into a fresh output directory" so a retry does not corrupt the first attempt (spec:64). But WC-4 puts the contract at `<dir>/return-contract.yaml` or `<file>.return-contract.yaml` for a path the brief supplies (spec:62), and 2.3 lists "the output directory or file" without saying it must differ per attempt (spec:73); the D1 example reuses a fixed `.dev/troubleshoot/login/` (spec:228). A command cannot create a fresh directory for a path it was handed. So a `--retry-of` worker (CAPS:116) given the same path overwrites attempt 1's report and its contract. Whether the coordinator picks a new path is a guess, so Medium. | Add to 2.3: the brief gives each attempt a path no earlier attempt used. Narrow WC-6 to match. | High | consistency +0.5 |
| M-06 | MAJOR / Medium | Nygard | WC-10 says a step that blocks one call "longer than 5 minutes" is split into waits "of at most 4 minutes" (spec:68); a call of 4 to 5 minutes needs no split under the first clause, yet the Decision (spec:266) wants 4 minutes as the margin under the 5-minute heartbeat and AC-4.3 fails any call over 240 s (spec:210). The pr-submit row describes a "sleep of at least `--poll-interval`" (spec:68), with no upper bound on the flag. | Use one number (at most 4 minutes) in WC-10's trigger and its AC; cap or state `--poll-interval` if D3 (b) is chosen. | Medium | testability +0.3 |
| M-07 | MAJOR / Medium | Fowler | AC-C1 requires zero matches of `orca (orchestration\|worktree\|terminal\|agent)` under `src/superclaude/core` (spec:172), while P0 adds an Orca section to `core/HOW-WE-WORK.md` and a new `core/WORKER-CONTRACT.md` (spec:158) and SA-2 allows an Orca mention "inside the contract file" (spec:147). A natural section ("run `orca orchestration ask`") would fail the common check on P0 itself; whether the text avoids that spelling is not stated. | Exempt the two new core files from AC-C1, or say the mention must avoid the verbs. | Medium | consistency +0.3 |
| M-08 | MAJOR / Medium | Nygard, Whittaker | A worker that ends `blocked` is reported as `--outcome failed` (spec:63), and Orca's circuit breaker does not count "a worker's own `failed` report" (CAPS:80, quoted by the spec at spec:263). The spec sets no cap on repeated blocked-then-retried cycles for one Task. Consequence is unbounded retries by a coordinator, not wrong data, so Medium. | One sentence: after two consecutive `blocked` outcomes for a Task the coordinator escalates to the person. | Medium | completeness +0.3 |
| M-09 | MINOR / Medium | Newman, Hohpe | The new contract names no version or schema field, though the workflow contract it should reuse is versioned ("contract 1.1", INV-B:272), and nothing in it ties the file to a Task or Dispatch, so a stale file in a reused path is indistinguishable from a fresh one (links to M-02). | Add `contract_version`; consider a caller-supplied run token flag. | Low | clarity +0.2 |

=== ADVERSARIAL ANALYSIS === (Whittaker, review order 6 of 11)

A-1. I can break this specification by **Sequence Attack**. The invariant at **spec:154 and spec:194** (a phase passes only when its checks pass, and later phases wait) fails when **P0's check demands an artifact a later phase creates**. Concrete attack: before = P0 done, `troubleshoot` smoke run finished with `REPORT.md` and no `return-contract.yaml` (INV-B:242); 7.2 step 3 needs the WC-4 contract path; after = step 3 fails, P0 never passes, P1 never starts. Severity CRITICAL. Graded Blocking: F-01.

A-2. I can break this specification by **Zero/Empty Attack**. The invariant at **spec:62** (the contract is written on every outcome at a path one rule fixes) fails when **`--unattended` is passed with no output flag**. Concrete attack: `/sc:analyze src --unattended` (spec:99 adds `--output`, P1); no dir, no file; the rule picks no place; before = no contract, after = either a contract in the cwd or none, and the coordinator's `--report-path` has no value. Severity MAJOR. Graded Medium: M-01.

A-3. I can break this specification by **Sequence Attack**. The invariant at **spec:64** (a retry does not corrupt the first attempt) fails when **the retry reuses the path the brief gave attempt 1**. Concrete attack: attempt 1 (`troubleshoot ... --output .dev/troubleshoot/login/`) writes `REPORT.md` and a `blocked` contract; the coordinator answers and starts `--retry-of` with the same brief (CAPS:116); attempt 2 overwrites `REPORT.md`, then its session is lost before the contract is rewritten; the coordinator reads attempt 1's `blocked` contract beside attempt 2's half-written report. Severity MAJOR. Graded Medium: M-02.

A-4. I can break this specification by **Sentinel Collision Attack**. The invariant at **spec:63** (`status` is one of four values) fails when **an existing contract uses another vocabulary**. Concrete attack: a workflow or reflect contract carries a status string outside the set (vocabularies UNVERIFIED, INV-B:272); WC-5's mapping has no row for it. Severity MINOR to MAJOR. Graded Medium: M-03.

A-5. I can break this specification by **Divergence Attack**. The invariant at **spec:68 vs spec:210** (waits stay under the heartbeat cadence) fails when **a single call lasts 270 s**. Concrete attack: a 270-second poll satisfies WC-10's trigger (not longer than 5 minutes) and breaks AC-4.3 (over 240 s); with a heartbeat due every 300 s the next heartbeat is late once any tool overhead is added. Severity MAJOR. Graded Medium: M-06.

A-6. I can break this specification by **Accumulation Attack**. The invariant at **spec:63 with CAPS:80** (failure is reported, and Orca's breaker bounds retries) fails when **every attempt ends `blocked`**. Concrete attack: attempt k ends `blocked`, outcome `failed`, retry k+1 with an answer that does not satisfy the gate; the breaker never counts it, so k grows without limit. Severity MAJOR. Graded Medium: M-08.

Attacks on the count and arithmetic invariants (43 = 10 + 27 + 6; 27 = 9 + 11 + 4 + 3) found nothing: Zero/Empty (a phase with no commands) cannot occur because every phase row lists commands (spec:158-162).

=== REMAINING PANEL === (Newman, Hohpe, Crispin, Gregory, Hightower; outside the two focus areas, run for completeness)

Crispin: boundary cases for the common checks exist (AC-C1 to AC-C5), but AC-C5 passes only if new flags go on new lines, because editing an existing Usage line produces a removed line (N-02). Gregory: the five open decisions are self-contained with recommendations (spec:224-253); good for a three-amigos read. Hightower: observability relies on `worker-show`, the transcript and the contract (spec:181-184), adequate for a file-based design.

### Minor notes (never fail the review)

- N-01: `R1-B1` and `R1-B2` are used as tags (spec:76, spec:154, spec:159, spec:195) but defined nowhere in the document; D5's "R1's protection against runaway fan-out" (spec:252) reads as section 1.3's R1, which says nothing about runaway fan-out (spec:33).
- N-02: AC-C5 (spec:176) forbids any removed line in a command diff; adding `--unattended` to a one-line Usage list edits that line. Say flags go on a new line.
- N-03: 7.2 step 5 searches the transcript for the string `AskUserQuestion` (spec:184); loaded command text contains the word, so the search should look for a tool call, not the string.
- N-04: AC-1.3 uses `claude -p` (print mode) as the "plain session" (spec:197); that tests the headless path, not an interactive one. "Scratch worktree" has no stated creation route (the repo's Orca worktree rule is UNVERIFIED in this sandbox).
- N-05: AC-1.4 is a grep whose pass condition is a judgement (spec:198).
- N-06: E2 says the worker "answered" (spec:22); the inventories quote only `state: ready, stage: input_accepted` (CAPS:49, INV-A:13).
- N-07: item 14 of the UNVERIFIED list (spec:285) is a process claim about an earlier citation check, not an unverified fact, and cannot be checked here. The set of 43 commands rests on the two inventories' own scope lists (INV-A:3, INV-B:3); no directory listing is in the sandbox, so completeness of the set is UNVERIFIED.

## Guard Condition Boundary Table (mandatory artifact, triggered: the spec has thresholds, flags and status guards)

Constructed by Nygard, completeness checked by Crispin, attacked by Whittaker (`CMD:315`). Complete before synthesis (FR-10). Status GAP rows are graded by FR-8/FR-9: none names a concrete wrong outcome without a further assumption except the P0 row, which is F-01; the rest are Medium and listed under follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `readiness_limit` | WC-1, spec:59 | Zero/Empty | no startup prompt | within limit | agent reaches `input_accepted` (CAPS:49) | OK |
| `readiness_limit` | WC-1, spec:59 | One/Minimal | prompt with a 30 s fallback | within limit | start passes at 34 s (CAPS:49) | OK |
| `readiness_limit` | WC-1, spec:59 | Typical | "well inside" 60 s | within limit | no number given for "well inside" | GAP (Medium: step 1 of 7.2 catches a failed start, spec:180) |
| `readiness_limit` | WC-1, spec:59 | Maximum/Overflow | fallback above about 45 s | exceeded | start fails again (spec:59, CAPS:49) | OK |
| `readiness_limit` | WC-1, spec:59 | Sentinel Value Match | `--timeout-ms` raised per start | limit moves | stated as per-start option (spec:59, CAPS:44-45) | OK |
| `unattended_flag` | D1, spec:51, spec:154 | Zero/Empty | flag absent | false | today's behavior unchanged (SA-1, spec:146) | OK |
| `unattended_flag` | D1, spec:154 | Typical | flag on an upgraded command | true | gates resolve per section 3 rows | OK |
| `unattended_flag` | D1, spec:154 | Legitimate Edge Case | flag on a command not yet upgraded or frozen | true | only "the coordinator passes it only to a command whose phase has passed"; no command-side behavior, no check | GAP (Medium, M-10) |
| `unattended_flag` | release-split, spec:89 | Legitimate Edge Case | `--unattended --interactive` | both true | `--interactive` checkpoints not resolved (INV-B:119) | GAP (Medium, M-10) |
| `unattended_flag` | cleanup, improve, roadmap rows, spec:103, spec:110, spec:118 | Legitimate Edge Case | `--unattended --interactive` | both true | refused | OK |
| `output_target` | WC-4, spec:62 | Zero/Empty | `--unattended` with no output flag | no path | not specified | GAP (Medium, M-01) |
| `output_target` | WC-4, spec:62 | One/Minimal | brief passes a directory | dir | `<dir>/return-contract.yaml` | OK |
| `output_target` | WC-4, spec:62 | Typical | brief passes a file | file | `<file>.return-contract.yaml` | OK |
| `output_target` | WC-4, spec:62 | Sentinel Value Match | adversarial and workflow fix their own place | fixed | `<output>/adversarial/...`; workflow stop before package writes none and ends failed | OK |
| `output_target` | WC-4/WC-6, spec:62, spec:64 | Legitimate Edge Case | retry given the same path | path reused | not specified; WC-6 says "fresh output directory" | GAP (Medium, M-02) |
| `status_to_outcome` | WC-5, spec:63 | Zero/Empty | no report exists | none | `--outcome failed` | OK |
| `status_to_outcome` | WC-5, spec:63 | Typical | `succeeded` | succeeded | `--outcome succeeded` | OK |
| `status_to_outcome` | WC-5, spec:63 | Legitimate Edge Case | `partial`; audit verdict FAIL; `blocked` | per status | succeeded; succeeded; failed (spec:63, spec:263) | OK |
| `status_to_outcome` | WC-5, spec:63 | Sentinel Value Match | status string outside the four values (existing contracts) | no match | not specified | GAP (Medium, M-03) |
| `wait_split` | WC-10, spec:68 | Zero/Empty | no long wait | no split | none needed | OK |
| `wait_split` | WC-10, spec:68 | Typical | a 3-minute wait | no split | none needed | OK |
| `wait_split` | WC-10, spec:68, spec:210 | Maximum/Overflow | a 270 s call | trigger (more than 5 min) false; AC-4.3 (more than 240 s) true | the two texts disagree | GAP (Medium, M-06) |
| `wait_split` | WC-10, spec:68 | Legitimate Edge Case | wait over 5 minutes | true | split into waits of at most 4 minutes | OK |
| `confidence_gate` | task row, spec:121 | Zero/Empty | confidence 0.0 | below 0.70 | blocked | OK |
| `confidence_gate` | task row, spec:121 | Legitimate Edge Case | confidence exactly 0.70 | false (command says `< 0.70`, INV-B:199) | proceeds | OK |
| `nested_depth` | R1, spec:33 | Typical | worker calls `worker-start` at depth 1 | refused | `nested_worker_depth_exceeded` (CAPS:99); call sites other than start/dispatch UNVERIFIED (CAPS:103) | OK |
| `nested_depth` | E4, spec:24 | Legitimate Edge Case | Agent-tool subagent inside a worker | not counted | allowed (CAPS:155); limits UNVERIFIED | OK |
| `retry_chain` | WC-6, spec:64 | One/Minimal | one failed attempt then `--retry-of` | retry | allowed (CAPS:116) | OK |
| `retry_chain` | WC-5, spec:63 | Maximum/Overflow | many consecutive `blocked` outcomes | breaker does not count them (CAPS:80) | no cap | GAP (Medium, M-08) |
| `phase_gate` | section 6, spec:154 | Legitimate Edge Case | P0 AC-0.4 on troubleshoot | cannot be true | check unpassable (spec:182, spec:194) | GAP (Blocking, F-01) |
| `ask_timeout` | WC-3, spec:61 | Maximum/Overflow | `ask` times out | pending | resume same message ID, no duplicate | OK |
| `ask_timeout` | WC-3, spec:61 | Zero/Empty | `--timeout-ms` omitted | unknown | spec marks default UNVERIFIED (spec:281) | OK (flagged) |
| `consumer_fenced` | WC-12, spec:70 | Legitimate Edge Case | `check` returns `consumer_fenced` / returns nothing | fenced / not fenced | stop, no `worker_done` (CAPS:67) / continue | OK |

Classes left out, one line each: `readiness_limit` One/Minimal for a limit of zero cannot occur (the default replaces a non-positive `--timeout-ms`, CAPS:44); `confidence_gate` Maximum cannot occur above 1.0 and the row only branches at 0.70; `nested_depth` Zero/Empty (a coordinator, depth 0) is not a worker case; `phase_gate` other classes do not apply to a pass/fail sequence.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, triggered: the coordinator pipeline has stages whose counts can differ)

```text
[Commands in scope: 43] --> [Verdict split: 10 ready + 27 change + 6 coordinator-only = 43] (conserved, spec:76)
        |
        v
[27 changed rows] --> [P1 9 + P2 11 + P3 4 + P4 3 = 27] (conserved, spec:159-162)  [+ 4 ready commands change in P2, 3 ready commands get small fixes in P1]
        |
[Tasks: T] --> [Dispatches: A >= T (retries, CAPS:116)] --> [Contract files: expected 1 per Dispatch]
                                                              actual = number of DISTINCT output paths  <-- MISMATCH when the brief reuses a path (M-02)
        |
        v
[worker_done: exactly 1 per Dispatch (spec:63)] --> [Coordinator reads the contract: assumes 1 contract per worker_done (spec:182)]
        crash or workflow stop before package: contracts < worker_done count  (handled: spec:62-63, "no report exists -> failed")
```

Consistency Check: the command-count stages conserve. The Dispatch-to-contract stage diverges (A dispatches to fewer paths) only if the brief reuses a path; the spec states the intent (WC-6) but gives no mechanism. FR-19 classes a mismatch CRITICAL where the spec assumes count conservation; here the spec handles crash and pre-package stops explicitly and the open case needs the unstated assumption that the coordinator reuses a path, so the finding is M-02 (Medium by consequence, Review Loop bullet 2), not a blocking CRITICAL.

## Follow-up candidates

Medium: M-01 to M-08 and M-10 (labelled MAJOR); M-09, M-11 and M-12 (labelled MINOR, Medium or lower). Minor notes: N-01 to N-07. None of these triggers a revision, fails the review or appears in the Reviser brief. The issue-opening question that Review Loop bullet 3 assigns to the session that ran the review was not asked: this worker's reply channel is limited to one `DONE` line, so the list is recorded only, as an `--unattended` run does (`CMD:260`). No issue was created.

## UNVERIFIED citations (cannot be checked in the sandbox)

Cited by the spec to files that are not in the sandbox, so unchecked here (where an inventory quotes the line it is checked only to that extent): `EVIDENCE.md:35-56` (quoted at CAPS:49-52), `.dev/codegraph-migration/orchestration/README.md:31,33,42` (line 31 quoted at CAPS:156; lines 33 and 42 not), the `return-contract.yaml:10` of the earlier run (quoted at INV-A:13), `CLAUDE.md:16,50,72-83,157,334,408`, `src/superclaude/cli/install_core.py:4,13-24,33`, `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254` and `core/CLAUDE.md:65`, `Makefile:68-74`, `pyproject.toml:38`, the E5 grep results (spec:25), the 11 re-read locations in spec:11, the PR #329 landing beyond README:12, and every `/opt/Orca/...` line (quoted only through CAPS). Source lines in `sk/...` and `cmd/...` are checked only as far as INV-A and INV-B quote them; those two inventories each say they had a fresh-context citation check (INV-A:106, INV-B:320), which cannot be verified here either.

## Decisions

| Decision | Options | Rationale |
|---|---|---|
| Format | `standard` YAML only; markdown report with a standard-format YAML summary | The brief asks for a full report with tables and a fixed last line; the YAML summary keeps the `standard` keys without duplicating each finding. |
| Grade of M-02 (retry path) | CRITICAL under FR-19; Medium | Medium. FR-19 applies where the spec assumes count conservation (`CMD:372`); the spec states the intent in WC-6 and handles crashes, so the defect needs the assumption that a path is reused. |
| Grade of M-01, M-03, M-04, M-05, M-10 | Blocking; Medium | Medium. Each needs a reading choice by the implementer (`PROMPTS:31`), not a text that cannot be followed. |
| F-02 included the three small-fix ready commands | load only; load plus adversarial, cleanup-audit, index-repo | Both: the selector in AC-1.1 is by "section 3 phase" and those rows carry "(P1)" (spec:83, spec:85, spec:86). |
| Issue question | ask the user; record only | Record only; no user channel in this run, and the command lets an unattended run do the same. |

## Reviser brief

Blocking finding ids: F-01, F-02. Reviser contract (restated from `CMD:263`, the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
