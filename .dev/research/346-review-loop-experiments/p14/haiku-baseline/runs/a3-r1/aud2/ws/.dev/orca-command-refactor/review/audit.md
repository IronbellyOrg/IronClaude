review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

## Header
- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- kind: labelled whole-document audit of the final spec, a first review of the full document (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`).
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `e9171857b793b520e3e6291ce69b77aaa2e13a035d1f119ba47eb5a42eff8f83`
- baseline: none (neither `--re-review` nor `--baseline` given; not a re-review). `--iterations` ignored: one review.
- reviewer model actually used: claude-sonnet-5-5
- mode: critique; focus: requirements, architecture. `--unattended` not passed, so no return-contract.yaml is written; this file is the report.
- Citation key: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.

## Coverage (what was and was not checked)
- Read in full: the candidate (287 lines), `README.md`, and the three inventories. The candidate's own `INV-A:N`, `INV-B:N` and `CAPS:N` citations were checked line by line against the inventories: all resolved to the content the spec claims, except the one noted in M-9.
- UNVERIFIED (not checkable in this sandbox, which holds only the README, the three inventories and the candidate): every spec citation to `src/superclaude/{commands,skills,core,agents}/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `install_core.py`, `Makefile`, `pyproject.toml`, `tests/`, `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/...`, and the Orca guide line numbers (reachable only through the `CAPS:` quotations). The spec's own claims of re-reads and of a 340-citation fresh check (`SPEC:11`, `SPEC:286`) are also UNVERIFIED. Where a finding rests on such a line it is stated through the inventory line that quotes it.
- No command was run (a sandbox has no Orca). The 43-command arithmetic and the phase counts below were recomputed from the candidate's own tables.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21; Fowler leads, Whittaker attacks divergence points)
Triggered: the spec describes a multi-stage flow (command set, then verdict split, then phase assignment, then acceptance test list) in which counts change.

```text
[43 commands: SPEC:76]
   --> [verdict split] --> [10 ready (SPEC:81-92)] + [27 needs change (SPEC:97-125)] + [6 coordinator-only (SPEC:130-137)] = 43  (conserved)
   --> [37 worker candidates = 10 + 27]
   --> [phase assignment SPEC:159-162]
         P1 13 (9 of 27 + 4 of 10: SPEC:159)   P2 15 (11 + 4)   P3 4 (4 + 0)   P4 3 (3 + 0)   no phase 2 (brainstorm, init-lite)  = 37  (conserved)
   --> [P1 scope: "--unattended accepted by every command in 3.1 and 3.2": SPEC:159]  = 37 consumers
   --> [AC-1.1 test: "## Unattended mode" section on 12 P1 commands, none on brainstorm/init-lite/load: SPEC:195]  = 12 consumers  <-- MISMATCH 37 vs 12 (see R-2)
   --> [WC-4 "contract on every outcome", sole exception /sc:load: SPEC:62]  = 36 consumers  <-- MISMATCH with the 2 "no change" rows (see R-2)
```
Counts for 43, 37 and the phase split are conserved. The two marked divergence points are findings R-2 (blocking) and M-4.

## === REQUIREMENTS ANALYSIS ===

### R-1 [MAJOR, blocking] WC-4 puts the contract in a directory that is a file for the commands whose brief passes a file-valued `--output`
- Expert: Wiegers (lead), Whittaker (FR-2.2 Divergence Attack).
- Grading sentence: an implementer who follows the stated text as written builds a contract path of `<file>/return-contract.yaml` for `/sc:tdd` and `/sc:init-lite`, and that is wrong because `--output` there names a regular file, so the path cannot exist.
- Evidence: WC-4 says the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62). Section 3.1 tells the coordinator to pass `--output <file>` to init-lite (SPEC:87) and to tdd, whose report is "the TDD at `--output`" (SPEC:90; INV-B:222 "TDD file at `--output`"; INV-A:55 "`--output`" is the audit file). The acceptance check for tdd passes `--output <file>` and then requires "contract `status: blocked` with a non-empty `blocked_question`" (SPEC:200). Step 4 of the live check reads `<contract>` (SPEC:183). No stated text gives a contract directory for a file-valued `--output`. The spec-panel row (SPEC:120, "add `--output`; contract") does not say which form `--output` takes either, and the spec-panel command definition in use here (`command.md:459-461`, whose repo state is UNVERIFIED as evidence) separates a file-valued `--output` from a directory flag `--report-dir`, which shows the collision is real.
- Attack (Whittaker, Divergence): `/sc:tdd "auth" --unattended --output docs/auth/TDD.md` with a bare topic. Before: no file, gate fires. After under SPEC:62: contract wanted at `docs/auth/TDD.md/return-contract.yaml`; creation fails or is skipped; nothing records `blocked`; WC-5 then reports `failed` for "no report exists" (SPEC:63) with no question for the coordinator; AC-2.2 cannot pass.
- Recommendation (Wiegers): state where the contract goes when `--output` is a file (for example a dedicated report-directory flag, or the parent directory of the file), and name it in the tdd, init-lite and spec-panel rows. Prefer narrowing WC-4 to one sentence over adding a mechanism. Priority: High. Quality impact: Testability 7 to 9.

### R-2 [MAJOR, blocking] WC-4/WC-5/P1 scope say every command gets unattended mode and a contract; section 3.1 and AC-1.1 say brainstorm and init-lite get none
- Expert: Wiegers (lead), Adzic (concrete counter-example), Fowler (count divergence).
- Grading sentence: an implementer who follows the stated text as written leaves init-lite and brainstorm unchanged (SPEC:84, SPEC:87, SPEC:195) while the coordinator brief still passes `--unattended` from P1 on (SPEC:73) and expects a WC-4 contract from every command except `/sc:load` (SPEC:62); init-lite then writes no `return-contract.yaml`, and WC-5 tells the worker to send `--outcome failed` when "no report exists" (SPEC:63) for a run that succeeded. Two stated texts contradict each other, and AC-1.1 (SPEC:195) asserts the opposite of the P1 scope sentence (SPEC:159).
- Evidence:
  - P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (SPEC:159) = 37 commands.
  - AC-1.1: brainstorm and init-lite "have none" (no `## Unattended mode` section), and the section is asserted on 12 commands only (SPEC:195).
  - WC-4: sole exception is `/sc:load` (SPEC:62). Init-lite's "Report today" is `context-audit.md`, "Small fix: None" (SPEC:87). Brainstorm's existing contract is only said to exist at `<output>/return-contract.yaml` (SPEC:84; INV-A:39, INV-A:97); no inventory line lists its fields, so whether it already has `command`, `artifacts`, the four-value `status` and `blocked_question` that WC-4 requires is UNVERIFIED.
  - Section 2.3 gives the coordinator no per-command rule: `--unattended` goes into every brief from P1 on, "P0 briefs omit it" (SPEC:73).
- Recommendation (Wiegers): make the three texts agree by narrowing one of them, not by adding a mechanism: either list brainstorm and init-lite as exceptions beside `/sc:load` in WC-4 and say what the worker reports for them (their existing report file), or give them the section in P1 and remove "none" from SPEC:84, SPEC:87 and SPEC:195. Priority: High. Quality impact: Consistency 6 to 9.

## === ARCHITECTURE ANALYSIS ===
The decision itself (Orca coordinates, commands stay the unit of work, no Orca calls inside commands) is consistent with the evidence the inventories quote: depth 1 refuses worker-in-worker dispatch (CAPS:97-101), a worker is a top-level Claude session (CAPS:161), and standalone use breaks if commands call Orca (CAPS:145-149). No blocking architecture defect was found in the decision. Findings below are Medium or minor.

### Medium findings (warnings; listed again under follow-up candidates)
- **M-1 [Medium, Fowler, Nygard] WC-3 has no bound on waiting and no carve-out for implement.** A timeout "resumes the same message ID" (SPEC:61); nothing says when the worker gives up and writes `blocked`, so a coordinator that never replies leaves the worker waiting indefinitely (Orca treats a waiting worker as healthy, CAPS:52, CAPS:129). WC-3 also lets the worker re-invoke "with the answer as a flag" for any blocked gate, while the implement row (SPEC:109) and D2 (SPEC:233-237) say a coordinator reply is not a Ruling (INV-A:66). The spec states the Ruling rule is unchanged but WC-3 does not exclude it. Needs a guess about which text wins, so Medium.
- **M-2 [Medium, Wiegers, Nygard] Blocked versus partial after partial work is undefined.** WC-4 allows `partial` and `blocked` (SPEC:62); WC-5 maps `partial` to `succeeded` and `blocked` to `failed` (SPEC:63, SPEC:264). A run that finishes most work and then hits a gate (tasklist Stage 10.5 after a full tasklist, SPEC:122; cleanup after applied items, SPEC:103) has no rule choosing between them, so the coordinator sees `failed` or `succeeded` for the same state.
- **M-3 [Medium, Fowler] The invocation mechanism of the command inside a worker is not specified.** Section 2.3 asks for "the exact command line" in the brief (SPEC:73), but a worker prompt arrives after an Orca preamble and Claude receives its task on argv (CAPS:47). Whether a `/sc:` line placed in that prompt is run as a command or needs the Skill tool is not stated (UNVERIFIED either way); Phase 0 tests it only implicitly (SPEC:194). Add one sentence to the brief template or to AC-0.4.
- **M-4 [Medium, Whittaker FR-2.4 Sequence] WC-6 "fresh output directory" versus WC-4 "directory the coordinator passed, known before dispatch".** A command that creates its own fresh directory per run (SPEC:64) puts the contract somewhere the coordinator could not know in advance; a coordinator that reuses the same `--output` on a `--retry-of` worker (the Task spec is reused) lets the retry overwrite the first attempt's contract, the thing WC-6 forbids. Workflow compounds it: its contract path embeds a run-time id and its pre-creation STOP has no package directory at all (SPEC:92; INV-B:272, which says the contract is not written for pre-creation STOPs), yet the P1 fix says to write it (SPEC:92, SPEC:159). Location is never stated. Section 2.3 should say the coordinator passes a new output directory on each retry, and the workflow row should name where a pre-creation STOP contract goes.
- **M-5 [Medium, Wiegers] The four-value `status` set versus existing contracts.** WC-4 says commands with a contract "keep their fields and add the missing ones" and also fixes `status` to `succeeded|partial|failed|blocked` (SPEC:62, SPEC:263). If an existing contract (workflow `status`, INV-B:272; reflect, brainstorm, adversarial) uses other values, both cannot hold. No inventory line lists the existing value sets: UNVERIFIED.
- **M-6 [Medium, Nygard] 1.4(2) is stronger than its evidence.** The spec says a command's own question "comes after readiness, so it does not fail `worker-start`" (SPEC:44), citing CAPS:52 and CAPS:129, which only say a worker already past `input_accepted` that waits is healthy. CAPS:47 says Claude's task is passed on the command line, so the command can run, and ask, before readiness is judged; CAPS:53 itself states the opposite rule ("must not show any interactive question ... before its agent input is ready"). Treat as UNVERIFIED until the Phase 0 runs and keep WC-1 wording as the safe default.
- **M-7 [Medium, Hohpe, Crispin] Briefs pass `--unattended` from P1 on, but outward defaults are turned off only in P2.** Section 2.3 (SPEC:73) versus the auggie-review row (P2, SPEC:100) and P2 text (SPEC:160). Between phases a coordinator following 2.3 passes `--unattended` to `/sc:auggie-review`, believes WC-9 holds (SPEC:67), and the default PR post still happens (INV-A:38). Safety-adjacent, but it needs a coordinator who ignores the phase table, so Medium. Recommend 2.3 say "from the command's own phase".
- **M-8 [Medium, Nygard] WC-11 does not cover all default-on local side effects.** Reflect's default-on folder promotion in UC-2 (INV-B:114) is turned off only if the brief adds `--no-promote` "when the coordinator owns folder moves" (SPEC:88), and validate-roadmap's shared memory directory (INV-B:253) is not mentioned in its row (SPEC:124). Both are two-worker clobber risks of the kind WC-11 names (SPEC:69).
- **M-9 [minor/Medium, citation] Support gaps in citations.** SPEC:122 cites `INV-B:111` for "adversarial Mode A depth UNVERIFIED"; that inventory line only describes reflect's Tier 2 merge and states no UNVERIFIED depth. The cli-portify row (SPEC:105) turns all three approval gates into `blocked` and adds `--resume <contract>` but names no way to convey the approval (WC-2 route b), so AC-2.3's happy-path run (SPEC:201) has no passing route for that command; Medium because the resume fields may imply approval (INV-A:45) and the spec does not say.

### Minor notes (never fail the review)
- N-1 SPEC:159 says P1 "involves no person gate", yet the P1 rows for explain, business-panel and test refuse modes under `--unattended` (SPEC:102, SPEC:108, SPEC:123).
- N-2 WC-10 requires splitting only calls longer than 5 minutes into waits of at most 4 (SPEC:68), while the pr-submit row and AC-4.3 require every single call under 4 minutes / 240 s (SPEC:114, SPEC:211).
- N-3 AC-C5 (SPEC:176) rejects any `-` diff line, but SA-4 allows "new flags" (SPEC:149); adding a flag to an existing Usage or argument-hint line produces a `-` line, so the flag must go on a new line.
- N-4 E3 (SPEC:23) cites the PR #329 `skill-direct` contract as support for the decision, while 1.4(1) (SPEC:43) concedes that run only proves the nested route; the statements are compatible but E3 reads stronger than 1.4 allows.
- N-5 AC-C1's grep covers `src/superclaude/core` (SPEC:172), where P0 adds an Orca section to the routing guide and the contract file (SPEC:158). SA-2 permits an Orca mention in the contract file (SPEC:147); the grep would flag it if written as `orca orchestration ask`. State the permitted form.
- N-6 WC-1 says a fallback "well inside" the limit (SPEC:59) with no number; the evidence is 30 s passes and about 45 s fails (CAPS:49).

## Adversarial Analysis (Whittaker; five attack methodologies against the spec's invariants)
Invariant I-1 "a contract exists for every worker outcome" (SPEC:62).
- I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **the run is init-lite or a pre-creation STOP of workflow**. Concrete attack: init-lite run succeeds; before: no contract path; after: no file; WC-5 sends `failed` (SPEC:63). (R-2, M-4)
- I can break this specification by **Divergence Attack**. The invariant at **WC-4** fails when **`--output` is a file** (R-1).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (SPEC:63)** fails when **a contract's own `status` value is one of an existing command's other values**: the four-value set has no row for it (M-5).
- I can break this specification by **Sequence Attack**. The invariant at **WC-6 (SPEC:64)** fails when **the coordinator retries with the same output directory**: the second attempt overwrites the first attempt's contract (M-4). Also, the order "blocked then WC-3 `ask` then re-invoke" has no cap (M-1).
- I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (SPEC:61)** fails when **ask timeouts accumulate with no reply**: unlimited waiting (M-1).
Severity: R-1 and R-2 are the only attacks with a state trace that needs no extra assumption; the rest depend on an unstated reading and are Medium.

## Guard Condition Boundary Table (Nygard lead, Crispin completeness, Whittaker attack)
Guards in the spec: contract/outcome guard (WC-5), location guard (WC-4), wait-size guard (WC-10), ask-timeout guard (WC-3), gate-resolution guard (WC-2), readiness guard (WC-1), additive-diff guard (AC-C5). Classes left out: Maximum/Overflow for the contract guard (a file has no capacity), Sentinel for the wait-size guard (no sentinel is defined for it), Maximum for the readiness guard (the maximum is the tool's `--timeout-ms`, unbounded and UNVERIFIED at CAPS:54).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| outcome mapping | SPEC:63 | Zero/Empty | contract missing or zero bytes | true ("no report exists") | `--outcome failed` | OK |
| outcome mapping | SPEC:63 | One/Minimal | contract with only `status: succeeded` | false | `succeeded` (WC-4 requires more keys; checked only at AC step 4, SPEC:183) | OK |
| outcome mapping | SPEC:63 | Typical | `status: failed` or `blocked` | true | `--outcome failed` | OK |
| outcome mapping | SPEC:63, SPEC:264 | Sentinel Value Match | `status: partial` | false | `succeeded`, first body sentence states `partial` | OK |
| outcome mapping | SPEC:63, SPEC:62 | Legitimate Edge Case | `status` outside the four values, or unparsable YAML | unspecified | not specified (M-5) | GAP |
| outcome mapping | SPEC:62-63 | Legitimate Edge Case | work finished, then a gate fires | unspecified | `blocked` vs `partial` not decided (M-2) | GAP |
| contract location | SPEC:62 | Zero/Empty | `--output` omitted under `--unattended` | unspecified | not specified for the command; the brief must pass it (SPEC:73) | GAP |
| contract location | SPEC:62 | Typical | `--output <dir>` | true | `<dir>/return-contract.yaml` | OK |
| contract location | SPEC:62, SPEC:87, SPEC:90 | Legitimate Edge Case | `--output <file>` (tdd, init-lite) | unspecified | `<file>/return-contract.yaml`, impossible (R-1) | GAP |
| wait size | SPEC:68 | Zero/Empty | no blocking call | false | no change | OK |
| wait size | SPEC:68 | Typical | call of 1 minute | false | no split | OK |
| wait size | SPEC:68, SPEC:211 | Legitimate Edge Case | single call of 4 to 5 minutes | false (WC-10), true (AC-4.3) | WC-10 allows it; AC-4.3 and the pr-submit row forbid it (N-2) | GAP |
| wait size | SPEC:68 | Maximum/Overflow | eval of 3600 s | true | split into waits of at most 4 minutes | OK |
| ask timeout | SPEC:61 | Typical | one timeout, then reply | n/a | resume same message ID | OK |
| ask timeout | SPEC:61 | Maximum/Overflow | repeated timeouts, no reply | unspecified | no cap, no fallback to `blocked` (M-1) | GAP |
| ask timeout | SPEC:61, CAPS:68 | Zero/Empty | `--timeout-ms` omitted, default UNVERIFIED | n/a | relies on message-ID resume, not a value | OK |
| gate resolution | SPEC:60 | Typical | gate fires at top level | true | (a) default, (b) flag, or (c) `blocked` | OK |
| gate resolution | SPEC:65 | Legitimate Edge Case | gate fires inside a subagent | true | subagent returns the question; top level resolves `blocked` | OK |
| gate resolution | SPEC:105 | Legitimate Edge Case | cli-portify approval gate | true | `blocked` with no approval input (M-9) | GAP |
| readiness | SPEC:59 | Typical | prompt falls back at 30 s | false | passes (CAPS:49) | OK |
| readiness | SPEC:59 | Legitimate Edge Case | fallback at about 45 s | true | "well inside" the limit, no number (N-6) | GAP |
| readiness | SPEC:59, CAPS:45 | Zero/Empty | `--timeout-ms` raised per start | n/a | WC-1 says "default 60 s" only | GAP |
| additive diff | SPEC:176 | Zero/Empty | empty diff | n/a | prints nothing, passes | OK |
| additive diff | SPEC:176, SPEC:149 | Legitimate Edge Case | flag added to an existing Usage line | true | `-` line appears, check fails though SA-4 allows it (N-3) | GAP |

FR-10: every guard enumerated, every cell populated, omitted classes given a reason above. GAP rows graded per FR-8/FR-9: the location row for a file-valued `--output` is blocking (R-1); the rest are Medium or minor.

## Expert consensus and disagreements
- Wiegers and Adzic agree R-1 and R-2 are the only items where the acceptance criteria cannot pass as written. Fowler adds that the decision and the phase counts (43, 37, 12) are otherwise conserved. Nygard and Whittaker would grade M-1 and M-6 higher if the Phase 0 runs show the behaviour; no disagreement on the verdict.
- Crispin: the acceptance checks in section 7 are concrete and mostly executable; the gaps are the two unreachable ones named in R-1 and M-9.
- Newman/Hightower: no finding; the backward-compatibility rule (SA-1 to SA-6) is stated and testable.

## follow-up candidates (Medium and minor; never trigger a revision)
M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, N-1, N-2, N-3, N-4, N-5, N-6 (all listed above). The session that runs the review asks the user once per loop whether to open an issue for them; this worker run has no user turn and its final reply is restricted, so none was asked and none was created.

## Reviser brief
Blocking finding ids: R-1, R-2. (The reviser reads this report, not the command.)
Repair only the blocking findings R-1 and R-2 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Revise only text a blocking finding names. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every added paragraph or table. Prefer deleting or narrowing text when the requirements are still met. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
