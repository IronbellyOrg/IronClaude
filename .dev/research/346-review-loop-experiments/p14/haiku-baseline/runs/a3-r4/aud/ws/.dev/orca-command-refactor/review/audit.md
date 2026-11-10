review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (whole-document audit, first review)

## Header

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 57870 bytes) |
| Candidate SHA-256 | `9bf4886e4a47262c5cf9c862441589e93e25942e3132e8035b411d7bd0318c5f` |
| Baseline | none. No `--re-review` and no `--baseline` was given, so this is a first review of the full document, not a re-review (Review Loop bullet 1). `baseline: missing` does not apply: neither flag was given. |
| Prior findings file | none |
| Reviewer model actually used | claude-sonnet-5-5 (Sonnet 5.5) |
| Review date | 2026-11-10 |
| Prompt followed | FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full before writing this report; `~` is the sandbox `home/` directory) |
| Grading rule applied | Review Loop bullet 2 plus the FIRST-REVIEW grading check: a finding is blocking only if the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption. Everything else is Medium or minor. |
| Brief clauses that narrowed the command | (1) "Write only your output file" and "Do not edit anything else": the Improve step (behavioral-flow step 6) was not performed and no revised specification, `improved-spec.md` or `return-contract.yaml` was written (also consistent with the command's Will Not "modify specifications without explicit user consent" and with `--unattended` not being passed). (2) "Reply with only `DONE <path>`": the once-per-loop question to the user about opening an issue for the follow-up candidates was not asked; the list is only recorded below. No brief clause widened the scope or graded a minor finding as blocking, so no clause was overridden. |

## Citation key and verification status

- `SPEC:N` = line N of the candidate. `README:N` = line N of `.dev/orca-command-refactor/README.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `CMD:N` = line N of the sandbox `command.md` (the definition of this command).
- Checkable in this sandbox: the candidate, README, the three inventories, command.md and the prompts file. Every claim below cites one of these.
- UNVERIFIED (not checkable here): every source the inventories cite but the sandbox does not contain, namely `src/`, `tests/`, `CLAUDE.md`, `~/.claude/commands|skills|agents` files, `.dev/evals/.../EVIDENCE.md`, `.dev/codegraph-migration/...`, Orca's compiled JS and the `orca-ide` guide output. Where I rely on such a fact I say "second-hand via INV-x:N / CAPS:N". The candidate's own attestations (SPEC:11 re-reads of 11 locations, SPEC:25 grep results, SPEC:285 item 14 "about 340 citations") are also UNVERIFIED here and are not relied on.

## What was covered

- Read in full: the candidate (all 285 lines), README, `inventory/orca-capabilities.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, command.md, the prompts file.
- Checked: the 43 / 10 / 27 / 6 accounting (SPEC:76) against INV-A:73 and INV-B:278 (5+5 ready, 13+14 needs-change, 3+3 coordinator-only: the sums hold); the phase assignment of every command in SPEC:81-125 against the P1-P4 rows (SPEC:158-162); the line anchors of the section-3 and section-4 rows to the inventory rows and notes they name (each pointed at the intended row or note; content equivalence was checked for every row quoted in a finding); the CAPS anchors used in SPEC:21-36, 59-70 and 180-186; the acceptance checks of section 7 for whether each can pass as written; the escaped-pipe grep in AC-C1 was run in the sandbox (result in F-12).
- Focus areas applied: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard). Whittaker is active in every review, so adversarial probing is included. Crispin, Gregory and Hightower contributed testing and operations points (assigned to the buckets below). `--focus correctness` was not requested, so the State Variable Registry was not produced. The Guard Condition Boundary Table and the Quantity Flow Diagram were triggered by the content and are produced below.
- Not covered: behavior of any real command or of Orca (no run is possible in the sandbox); the semantic correctness of the inventories' own verdicts beyond the lines the spec cites; sections of the sources outside the sandbox.

## Findings index

| Id | Grade | Label | Bucket | Expert | One-line title |
|---|---|---|---|---|---|
| F-01 | blocking | MAJOR | Requirements | Wiegers, Fowler, Whittaker | WC-4 contract location cannot be followed for file-valued, fixed-location and missing output arguments |
| F-02 | blocking | CRITICAL | Architecture | Fowler, Whittaker | Phase 1 scope and AC-1.1 cover 37 commands; the phase plan touches 13 and defers gates and outward defaults to P2-P4 |
| F-03 | blocking | MAJOR | Requirements | Crispin, Adzic | AC-0.4 step 3 cannot pass in Phase 0 because the WC-4 contract does not exist until P1 |
| F-04 | Medium | MAJOR | Requirements | Wiegers, Newman | WC-4 contract schema: status vocabulary vs existing contracts, no version or run id, path base, no sample |
| F-05 | Medium | MAJOR | Adversarial | Whittaker | WC-5 maps an empty, unparseable or unknown-status report to `succeeded` |
| F-06 | Medium | MAJOR | Requirements | Wiegers, Nygard | No rule that `--unattended` propagates to nested command invocations |
| F-07 | Medium | MAJOR | Architecture | Fowler, Nygard | WC-11 shared-write coverage is incomplete beyond `/sc:save` |
| F-08 | Medium | MAJOR | Architecture | Newman, Whittaker | Handling of the `--unattended` switch: stale installs, coordinator-only commands, switch text inside quoted content |
| F-09 | Medium | MAJOR | Requirements | Crispin, Gregory | Several WC requirements have no acceptance check; "well inside" in WC-1 is unmeasurable |
| F-10 | Medium | MAJOR | Requirements | Nygard, Crispin | WC-10 scope, threshold (5 vs 4 minutes) and its unverified basis |
| F-11 | Medium | MAJOR | Architecture | Nygard | WC-6 "fresh output directory" does not make a re-run safe for commands that edit files in place |
| F-12 | Medium | MAJOR | Requirements | Crispin | AC-C1 conflicts with SA-2 and the P0 deliverables, and its escaped pipes make a copied check pass vacuously |
| F-13 | Medium | MAJOR | Architecture | Fowler, Nygard | Tasklist and reflect under `--unattended`: auto-accepted remediation is unstated, and the nesting claim is stated as fact |
| F-14 | Medium | MAJOR | Architecture | Nygard, Hightower | Stall detection relies on `agentWait`, which the spec's own evidence says does not cover an idle chat offer |
| F-15 | Medium | MAJOR | Architecture | Hohpe, Wiegers | WC-3 `ask` path vs D2(a); "ask once" is undefined for commands with several gates |
| F-16 | minor | MINOR | Requirements | Adzic | `partial` maps to `succeeded`, so a dependent Task shows as ready |
| F-17 | minor | MINOR | Requirements | Wiegers | SPEC:73 cites an undefined "B1" |
| F-18 | minor | MINOR | Requirements | Cockburn | "Phases 1-3 need no user decision" (SPEC:154) vs open decision D1 (SPEC:51, 227) |
| F-19 | minor | MINOR | Requirements | Wiegers | SPEC:16 says command changes are "limited to" section 2; section 3 and SA-4 list other fixes |
| F-20 | minor | MINOR | Architecture | Fowler | The spec-panel row and WC-4 flag names differ from this command's own definition (CMD:22-23, 460-461) |
| F-21 | minor | MINOR | Requirements | Wiegers | Evidence worded stronger than its source in three places (E2, E3, /sc:git) |

## === REQUIREMENTS ANALYSIS ===

### F-01 (blocking, MAJOR): WC-4 contract location cannot be followed for file-valued, fixed-location and missing output arguments
Experts: Wiegers (lead), Fowler, Whittaker. Priority: High. Quality impact: Testability +2, Consistency +1.

Where: SPEC:62 (WC-4), SPEC:87 and SPEC:90 (init-lite and tdd take `--output <file>`), SPEC:85-86 (cleanup-audit and index-repo have a fixed output location), SPEC:113 (post-release "else blocked"), SPEC:183 (check 7.2 step 4), SPEC:200 (AC-2.2).

Grading check: An implementer who follows the stated text as written builds, for a tdd worker, a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (SPEC:62), and the coordinator passes `--output <file>` (SPEC:90); X is wrong because the path becomes `docs/auth/TDD.md/return-contract.yaml`, which cannot exist beside the file the same run writes, and the only other path the text allows (the file's parent directory) is shared by every worker writing into that directory, which SPEC:69 (WC-11) forbids.

Concrete attack (Whittaker, Zero/Empty and Sentinel Collision on the argument that locates the report):
1. File-valued argument. Before: argv `/sc:tdd "auth service" --unattended --output docs/auth/TDD.md`. WC-4 resolves `<output-dir>` to `docs/auth/TDD.md`. After: no contract can be created there. The same applies to init-lite (SPEC:87). The check at SPEC:183 (`test -s <contract>`) and the AC-2.2 example `/sc:tdd "auth" --unattended --output <file>` (SPEC:200, which requires a contract with `status: blocked`) have no location to read.
2. Missing argument. Before: argv `/sc:post-release v1.4.1 --unattended` with no `--output`. SPEC:113 says the run is "else blocked"; SPEC:62 says the blocked contract is written "on every outcome" into a directory that was never passed. After: no file; WC-5 (SPEC:63) then sends `--outcome failed` because "no report exists", and the question that explains the block (`blocked_question`, SPEC:62) is lost. The AC-2.2 example `/sc:cli-eval run --unattended` with no `--suite` (SPEC:200) has the same problem.
3. Fixed location. cleanup-audit and index-repo write to a fixed place (`.claude-audit/`, `PROJECT_INDEX.md`; SPEC:85-86), so there is no coordinator-passed directory; "known before dispatch" (SPEC:62) is unmet and the rows add no location for the contract.

Corroboration, not used for the grade: this command's own definition made the same distinction. `--output` is "file-valued", a separate `--report-dir` carries the contract, and a missing report directory is refused "in chat only" (CMD:460-461).

Recommendation: state, in WC-4 only, one location rule per output-argument class (directory-valued, file-valued, fixed, absent) so every case names where the contract goes and what the worker does when none can be written. Prefer narrowing WC-4's definition of `<output-dir>` over adding new flags to each row.

### F-03 (blocking, MAJOR): AC-0.4 step 3 cannot pass in Phase 0 because the WC-4 contract does not exist until P1
Experts: Crispin, Adzic. Priority: High. Quality impact: Testability +1.
Where: SPEC:182 (7.2 step 3), SPEC:194 (AC-0.4), SPEC:79 (section 3.1 intro), SPEC:154 (phase gate), SPEC:63 (WC-5).

Grading check: An implementer who follows the stated text as written runs 7.2 on `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` for AC-0.4 and requires, in step 3, that the worker's `--outcome` matches "the contract's status under WC-5" and that its report path "is the WC-4 contract path" (SPEC:182); X is wrong because AC-0.4 itself says the contract "arrives in P1" and changes only step 4 (SPEC:194), and section 3.1 says the worker reports the command's existing file until Phase 1 adds the contract (SPEC:79), so in Phase 0 no WC-4 contract exists for step 3 to compare, the check cannot pass, and SPEC:154 then holds back Phase 1 while SPEC:194 says a failure here "reopens section 1" (the core decision).

Recommendation: change step 3's second and third conditions for P0 the same way AC-0.4 changes step 4 (existing report file; the outcome follows the command's stated result).

### F-04 (Medium, MAJOR): WC-4 contract schema is under-specified
Experts: Wiegers, Newman, Adzic. Priority: Medium. Quality impact: Completeness +1, Testability +1.
Where: SPEC:62, SPEC:92, SPEC:183, SPEC:262.
- Status vocabulary. WC-4 says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62), but the Decisions row fixes `status` to `succeeded / partial / failed / blocked` (SPEC:262) and check 7.2 step 4 asserts exactly those four values (SPEC:183). The workflow contract already has its own `status` and a contract version "1.1" (SPEC:92, via INV-B:272); the spec never shows its values (UNVERIFIED), so "keep" and "fixed set" may collide for an existing field.
- No contract version, run or dispatch id, or timestamp. A resumed run writing into the same directory (the `--resume` rows, SPEC:64, 109, 114) leaves the earlier attempt's file in place until overwritten, so a coordinator cannot tell a stale file from a fresh one.
- The path base of `report_path` and each `artifacts` entry (repo-relative or absolute) is not stated, though `worker_done --report-path` wants real values (CAPS:74).
- No sample file.
Why Medium: the text allows more than one reading and the implementer picking the worse one is a guess, not a contradiction.
Recommendation: one example file in WORKER-CONTRACT.md, `contract_version`, and "overwrite the file at start" (or write a `running` status first).

### F-06 (Medium, MAJOR): `--unattended` has no propagation rule for nested invocations
Experts: Wiegers, Nygard. Priority: Medium. Quality impact: Completeness +1.
Where: SPEC:60 (WC-2), SPEC:90 and SPEC:122 (the only two stated propagations: tdd to `/task`, tasklist to reflect), INV-B:154 (roadmap writes memory through `sc:save` at every wave), INV-A:44 (cli-eval create runs `/sc:spec-panel` and `sc:adversarial-protocol`), INV-A:39 (brainstorm passes `--interactive` to adversarial), INV-B:201 (task calls `/sc:troubleshoot`).
Attack: a roadmap worker run with `--unattended` calls save once per wave. Unless save also runs in unattended mode, it overwrites the single-owner keys (SPEC:119, INV-B:165), which WC-11 (SPEC:69) says must not happen. The spec's roadmap row (SPEC:118) does not mention memory writes.
Why Medium: the document never states the rule; no stated text does harm.
Recommendation: one sentence in WC-2 saying whether a nested command receives `--unattended` and what happens when it has no such mode.

### F-09 (Medium, MAJOR): several requirements have no acceptance check
Experts: Crispin (lead), Gregory, Adzic. Priority: Medium. Quality impact: Testability +2.
Where: SPEC:59-70 against SPEC:166-210.

| Requirement | Check that can fail it | Gap |
|---|---|---|
| WC-1 (SPEC:59) | 7.2 step 1 only (SPEC:180) | "well inside the readiness limit" has no number; the evidence is a 30 s fallback that passed and "about 45 s" that failed under a 45 s limit given for that test (CAPS:49, second-hand), which is not the 60 s default |
| WC-3 (SPEC:61) | none | the `ask` and resume path is never exercised; AC-2.2 only checks the blocked contract |
| WC-6 (SPEC:64) | none | no retry (`--retry-of`) or resume run appears in section 7 |
| WC-10 (SPEC:68) | AC-4.3 (SPEC:210), pr-submit only | cli-eval's wait splitting (SPEC:104, 160) has no check |
| WC-11 (SPEC:69) | AC-3.4 (SPEC:207), save only | see F-07 |
| WC-12 (SPEC:70) | none | `consumer_fenced` handling is never tested |

Also: `brainstorm` and `init-lite` have no phase and no live check (SPEC:83-84, 87, 158-162, 194-196), though they count among the 10 "ready" commands whose verdicts come only from reading files (SPEC:43, INV-B:323). AC-1.1 (SPEC:195) is a text-presence test, so it cannot show that a gate no longer stalls.
Why Medium: missing checks, not a stated text that fails.
Recommendation: one check per uncovered WC id, or mark the requirement "not tested" in WC-1/3/6/12.

### F-10 (Medium, MAJOR): WC-10 scope, threshold and unverified basis
Experts: Nygard, Crispin. Priority: Medium. Quality impact: Consistency +1.
Where: SPEC:68, 104, 114, 160, 210, 266; CAPS:130, CAPS:182.
- The rule is general ("a command step that blocks a single tool call for longer than 5 minutes") but only cli-eval and pr-submit receive it (SPEC:104, 114; P2 text names cli-eval only, SPEC:160). `/sc:build` and `/sc:test` run the project's build and test runner (INV-A:40, INV-B:234), cleanup-audit and implement run long agent waves; none is assessed, and a foreground test run is not a poll that can be "split into waits".
- Threshold: WC-10 splits steps above 5 minutes into waits of at most 4 minutes (SPEC:68), but AC-4.3 fails any single call above 240 s (SPEC:210). A step of 270 s is compliant with WC-10 and fails AC-4.3.
- Basis: the 5-minute heartbeat comes from this run's preamble, and whether Orca uses heartbeat age at all is open (CAPS:130, UNVERIFIED item 7 at CAPS:182). The spec's own UNVERIFIED list (SPEC:271-285) does not include it, although WC-10 asks command changes on that basis.
Recommendation: list the heartbeat dependence as UNVERIFIED, align AC-4.3 with WC-10 (or the reverse), and say which other commands WC-10 covers.

### F-16 to F-19, F-21 (minor notes)
- F-16 (Adzic): WC-5 maps `partial` to `succeeded` (SPEC:63, 263). Orca marks the Task completed, so a dependent Task is shown as ready (CAPS:90, 92) even though the work is partial. SPEC:73 already makes the coordinator open the report first, so this is a note only.
- F-17 (Wiegers): SPEC:73 cites "B1, SPEC:158-159" for "no command accepts the flag before P1". "B1" is not defined anywhere in the candidate and SPEC:158-159 is the P0 and P1 table rows.
- F-18 (Cockburn): SPEC:154 says "Phases 1-3 need no user decision"; D1 (SPEC:51, 227) decides the mechanism every phase uses, and SPEC:225 says only that phases 0-3 "can proceed on the recommendations". The two sentences differ.
- F-19 (Wiegers): SPEC:16 says command changes are "limited to the worker contract in section 2"; section 3 "Other required change" and SA-4 (SPEC:149) list further defect fixes (drift, tool lists, usage lines).
- F-21 (Wiegers), evidence stronger than its source: (a) E2 (SPEC:22) says the worker "answered", but the quoted source line (CAPS:49) shows only `state: ready, stage: input_accepted`; (b) E3 (SPEC:23) offers `invocation_method: skill-direct` as proof "it has worked before", while section 1.4 (SPEC:43) says that run used an Agent-tool subagent, and INV-A:13 and CAPS:156 draw opposite readings of the same field; (c) the /sc:git row (SPEC:133) says its operations "need the user's authorization in this repo" and cites README:31, which binds only this run's workers. Which reading of (b) is right is UNVERIFIED.

## === ARCHITECTURE ANALYSIS ===

### F-02 (blocking, CRITICAL): Phase 1 scope and AC-1.1 cover 37 commands; the phase plan touches 13 and defers gates and outward defaults to P2-P4
Experts: Fowler (pipeline and count annotation), Whittaker (Divergence and Sequence attacks), Wiegers. Priority: High. Quality impact: Consistency +2, Testability +1. Labelled CRITICAL because Pipeline Dimensional Analysis classifies a count mismatch as CRITICAL (FR-19); it is blocking on its own consequence, shown below.

Where: SPEC:159 (P1 scope "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"), SPEC:195 (AC-1.1), SPEC:99-125 (phase column), SPEC:160-162 (P2-P4), SPEC:154 and SPEC:225 (Phase 4 waits for D2-D4), SPEC:240 (D3(a)), SPEC:67 (WC-9), SPEC:73 (briefs carry `--unattended` from Phase 1), SPEC:112 (load writes no report).

Grading check: An implementer who follows the stated text as written adds `--unattended` and an `## Unattended mode` section naming `return-contract.yaml` to all 37 commands of sections 3.1 and 3.2 in Phase 1 (SPEC:159, SPEC:195), including auggie-review, whose PR-posting default is switched off only in P2 (SPEC:100, SPEC:160), post-release and pr-submit, whose outward defaults wait for P4 and the user's answers (SPEC:113-114, 154, 162), and load, which writes no report (SPEC:112); X is wrong because SPEC:73 tells the coordinator to put `--unattended` in every brief from Phase 1, so a P1 `auggie-review` run accepts the flag and still posts to GitHub and offers remediation, which WC-9 (SPEC:67) and WC-2 (SPEC:60) say cannot happen under that flag, and because SPEC:154, SPEC:162 and D3(a) (SPEC:240, "no pr-submit changes") say P4 commands stay unchanged until the user decides. The other reading (13 commands, the P1 Commands column) makes AC-1.1 fail for the other 24, so the stated texts cannot both hold.

Concrete attack (Divergence, Sequence): before, P1 shipped, user runs the coordinator brief `/sc:auggie-review 123 --unattended --output d/` (SPEC:73 form). The flag is accepted (SPEC:159). Gate conversion is P2 (SPEC:100, 160), so the command posts the inline review comments and offers remediation (INV-A:38, SPEC:100); after: a GitHub write that the brief never authorized, plus a stall at the remediation offer with no `worker_done`.

Recommendation: narrow the P1 flag sentence and AC-1.1 to the commands P1 actually changes (the 13 in the Quantity Flow Diagram), delete the "every command in sections 3.1 and 3.2" wording, and say in section 2.3 that the brief carries `--unattended` only for a command whose phase has shipped. Do not add new mechanisms.

### F-07 (Medium, MAJOR): WC-11 shared-write coverage is incomplete beyond /sc:save
Experts: Fowler, Nygard. Priority: Medium. Quality impact: Completeness +1.
Where: SPEC:69, 85-86, 207; INV-B:114 (reflect writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md`), INV-B:253 (validate-roadmap writes memory under `.superclaude/memory/validate-roadmap/`), INV-A:53 (index-repo writes `PROJECT_INDEX.md` in the repo root), CAPS:115 (workers share the worktree by default).
Attack: two index-repo workers in one worktree both rewrite `PROJECT_INDEX.md`; the row's fix is only "state the output location" (SPEC:86), which does not make the path parallel-safe. Only save has an acceptance check (AC-3.4, SPEC:207).
Why Medium: a missing restriction, not a stated text that harms.
Recommendation: list in WC-11 every command with a fixed or slug-keyed shared path and say what the brief must do for each.

### F-08 (Medium, MAJOR): handling of the `--unattended` switch
Experts: Newman (versioning), Whittaker (Sentinel Collision). Priority: Medium. Quality impact: Consistency +1.
Where: SPEC:51-52, 73, 128, 195, 227-230; CMD:459 for comparison.
- Stale install. Commands are installed per machine to `~/.claude` (SPEC:52); a coordinator brief from Phase 1 on carries `--unattended` (SPEC:73). An installed copy that predates the change has no such section, so the token is ordinary text or an unknown argument and the gates stay live. That is the WC-2 stall the design exists to avoid, and no check detects it before dispatch.
- Coordinator-only commands "get no `--unattended` mode" (SPEC:128). What they do when handed the flag is not stated; AC-1.1 checks only that their file lacks the section (SPEC:195). For `/sc:git` or `/sc:agent` the result could be a mutation or a stall.
- D1(a) says the flag "cannot misfire on a person" (SPEC:228). No rule says the flag counts only as a standalone argument, not inside quoted content such as a symptom text that mentions it. This command's own definition states such a rule (CMD:459).
Recommendation: add the standalone-token rule and a "refuse with a clear message" behavior for coordinator-only commands, and tell the coordinator how to confirm the installed version before dispatch.

### F-11 (Medium, MAJOR): WC-6 "fresh output directory" does not protect in-place edits
Expert: Nygard. Priority: Medium. Quality impact: Completeness +1.
Where: SPEC:64, 103 (cleanup), 107 (document), 110 (improve), 123 (test, which has `--fix`, INV-B:234), SPEC:70 (WC-12).
Attack: a cleanup worker applies half its auto-fix items to source files and dies. A `--retry-of` worker (SPEC:64) starts a "fresh output directory" and runs again over a tree that already holds the first attempt's edits, so the first attempt's output is not protected and the report lists only the second run's changes. Likewise a worker that receives `consumer_fenced` stops at its next check (SPEC:70) and may keep writing until then.
Why Medium: the rule is silent on edited source, not wrong on what it states.
Recommendation: state that WC-6's safe re-run covers report output only, and name what the retry brief must carry for commands that edit files.

### F-13 (Medium, MAJOR): tasklist and reflect under `--unattended`
Experts: Fowler, Nygard. Priority: Medium. Quality impact: Consistency +1.
Where: SPEC:88, 122; INV-B:109, 209-210, 215, 314.
- The spec has tasklist pass `--unattended` to each reflect so the "headless rule applies" (SPEC:122), and has reflect follow the headless auto-accept rule for `--remediate` (SPEC:88). The inventory says that rule auto-accepts remediation for auto-fixable registers (INV-B:109) and recommends that Stage 10.5 call reflect without `--remediate` (INV-B:215). The spec's choice therefore starts remediation handoffs automatically in every phase of a tasklist run; this effect, and what `needs_human_decision` items do (INV-B:209), are not stated, and the Decisions table has no row for the choice.
- SPEC:122 says tasklist's reflect fan-out is "inside Claude Code's nesting limit" and cites INV-A:14. INV-A:14 gives the limit, not the depth of this chain, and INV-B:210 and INV-B:314 mark nested spawning here UNVERIFIED. The spec states it as fact.
Recommendation: say what auto-accept starts and what a `needs_human_decision` item resolves to, and mark the nesting claim UNVERIFIED.

### F-14 (Medium, MAJOR): stall detection
Experts: Nygard, Hightower. Priority: Medium. Quality impact: Completeness +1.
Where: SPEC:44, 60, 181-182; INV-A:62; CAPS:125, 129.
Section 1.4 says a silent stall is seen "only through `worker-show`'s `agentWait` or a missing report" (SPEC:44), and check 7.2 step 2 passes when `agentWait` is never non-null (SPEC:181). But `agentWait` names a worker parked on "a prompt only a human can answer" and a null value is absence, not proof (CAPS:125, 129), while the stalls the spec fears most are a plain chat offer or a turn ended on a question (SPEC:60, INV-A:62). Step 2 can therefore pass for a worker idling at a chat question; only the missing `worker_done` in step 3 catches it. No coordinator timeout or recovery step is given; the design defers entirely to Orca's guide.
Recommendation: say that step 3 is the stall check and give the coordinator one rule for a Dispatch with no `worker_done` and no heartbeat.

### F-15 (Medium, MAJOR): WC-3 `ask` path vs D2(a); "ask once"
Experts: Hohpe, Wiegers. Priority: Medium. Quality impact: Consistency +1.
Where: SPEC:61, 109, 233-236, SPEC:105; INV-A:66 (second-hand: a Ruling cannot come from another agent).
WC-3 lets the worker session ask the coordinator and "re-invoke or resume the command with the answer as a flag" (SPEC:61). D2(a), the recommended option, has the implement worker stop and end `failed` (SPEC:234). The text does not say that WC-3 is excluded for a Ruling, so a worker could take the coordinator's answer as the missing confirmation. The command's own rule would still refuse it (second-hand), so this is an ambiguity, not a stated bypass. "Ask the coordinator once" is also undefined for cli-portify's three approval gates (SPEC:105).
Recommendation: exclude Ruling and approval gates from WC-3 in one clause, and say "once per gate".

### F-20 (minor): flag names vs this command's own definition
Expert: Fowler. SPEC:62 names `--output` or `--output-dir` as the output argument, and SPEC:120 says spec-panel needs "`--output`" added. The definition of `/sc:spec-panel` used for this review already has `--output` (file-valued), `--target-release`, a separate `--report-dir` and a contract at `<report-dir>/return-contract.yaml` (CMD:22-23, 460-461). Whether the spec predates that definition is UNVERIFIED; nothing here depends on the answer.

## === ADVERSARIAL ANALYSIS ===

Whittaker's attacks on invariants. Most attacks are recorded where they produce a finding (F-01 Zero/Empty and Sentinel Collision, F-02 Divergence and Sequence, F-08 Sentinel Collision, F-11 Accumulation). The remaining one:

### F-05 (Medium, MAJOR): WC-5 maps an empty, unparseable or unknown-status report to `succeeded`
Expert: Whittaker (Zero/Empty Attack and Sentinel Collision). Priority: Medium. Quality impact: Testability +1.
I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:63 (WC-5)** fails when **a report file exists but is empty, unparseable, or has a missing or unknown `status`**. Concrete attack: before: the command crashes after creating `return-contract.yaml` as a 0-byte file (or writes `status: running`); the worker applies WC-5 ("`--outcome failed` when the report says `failed` or `blocked`, or no report exists; `--outcome succeeded` otherwise"); after: `worker_done --outcome succeeded`, the Task is completed and its dependents can start, though the work did not finish. The emptiness check (`test -s`) exists only in the test at SPEC:183, not in the rule the worker follows.
Why Medium: an undefined state (the report exists but cannot be read), not a stated text that does harm.
Recommendation: replace "otherwise" in WC-5 with an explicit list, and treat anything else as `failed`.

### F-12 (Medium, MAJOR): AC-C1 conflicts with SA-2 and the P0 deliverables, and fails vacuously when copied
Expert: Crispin. Priority: Medium. Quality impact: Testability +1.
Where: SPEC:172, 147, 158, 192-193.
- AC-C1 must print nothing for `src/superclaude/core` (SPEC:172), but P0 adds `WORKER-CONTRACT.md` and an Orca section in `HOW-WE-WORK.md` under that directory (SPEC:158), and SA-2 allows a mention of Orca "as an example of a caller's question channel inside the contract file" (SPEC:147). If the contract file spells that example as `orca orchestration ask`, AC-C1 matches it and P0 cannot pass. The exact spelling is not given, hence Medium.
- The pattern is written with `\|` between the alternatives (SPEC:172). Rendered in a table that is a `|`, but copied from the source text into `grep -E` it is a literal pipe. I ran both forms in the sandbox on the line `orca orchestration ask`: the form with `\|` gave a match count of 0 and the form with `|` gave 1. A copied AC-C1 therefore prints nothing for any input and passes vacuously. The same escaping appears in AC-C4 and AC-C5 (SPEC:175-176) and in the P0 checks (SPEC:192-193).
Recommendation: exclude the contract file and the HOW-WE-WORK Orca section from AC-C1 by name, and give the commands in a code block rather than a table cell.

## Guard Condition Boundary Table

Guards were found (thresholds, flag switches, status mappings, phase gates), so the table is produced and is complete before synthesis. Classes that cannot occur for a guard are left out with a reason in the notes below the table. Every GAP is traced to a finding.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `contract-location` | SPEC:62 (WC-4) | Zero/Empty | no output argument | false (no directory) | unspecified; SPEC:113 requires "blocked" but no directory exists to hold the contract (F-01) | GAP |
| `contract-location` | SPEC:62 (WC-4) | One/Minimal | relative directory `out/` | true | contract in `out/`; path base for entries not stated (F-04) | OK |
| `contract-location` | SPEC:62 (WC-4) | Typical | `.dev/x/` | true | `.dev/x/return-contract.yaml` | OK |
| `contract-location` | SPEC:62 (WC-4), SPEC:90 | Sentinel Value Match | `--output docs/a/TDD.md` (a file) | false | unspecified; text yields an impossible or shared path (F-01) | GAP |
| `contract-location` | SPEC:85-86 | Legitimate Edge Case | fixed-location command (cleanup-audit, index-repo) | false | no location named for the contract (F-01) | GAP |
| `outcome-mapping` | SPEC:63 (WC-5) | Zero/Empty | no report file | true | `--outcome failed` | OK |
| `outcome-mapping` | SPEC:63 (WC-5) | Zero/Empty | 0-byte or unparseable report | false | "otherwise" gives `succeeded` (F-05) | GAP |
| `outcome-mapping` | SPEC:63 (WC-5) | One/Minimal | `status: succeeded`, `artifacts: []` | true | `--outcome succeeded` | OK |
| `outcome-mapping` | SPEC:63 (WC-5) | Typical | `status: failed` | true | `--outcome failed` | OK |
| `outcome-mapping` | SPEC:63 (WC-5) | Sentinel Value Match | `status: partial` or `blocked` | true | partial gives `succeeded`; blocked gives `failed` | OK |
| `outcome-mapping` | SPEC:63 (WC-5) | Sentinel Value Match | missing or unknown `status` value | false | "otherwise" gives `succeeded` (F-05) | GAP |
| `outcome-mapping` | SPEC:63 (WC-5) | Legitimate Edge Case | audit verdict FAIL | true | `--outcome succeeded` (stated) | OK |
| `wait-split` | SPEC:68 (WC-10) | One/Minimal | single call of 1 s | false | no split needed | OK |
| `wait-split` | SPEC:68, SPEC:210 | Typical | single call of 270 s | false | compliant with WC-10, fails AC-4.3's 240 s (F-10) | GAP |
| `wait-split` | SPEC:68 (WC-10) | Maximum/Overflow | polled wait of 600 s | true | split into waits of at most 4 minutes | OK |
| `wait-split` | SPEC:68 (WC-10) | Legitimate Edge Case | one foreground test run over 5 minutes (`/sc:test`) | true | unspecified; it is not a poll that can be split (F-10) | GAP |
| `readiness-fallback` | SPEC:59 (WC-1) | Typical | 30 s fallback | true | passes (second-hand, CAPS:49) | OK |
| `readiness-fallback` | SPEC:59 (WC-1) | Legitimate Edge Case | "well inside" the 60 s limit | n/a | no number given (F-09) | GAP |
| `unattended-switch` | SPEC:51, 227 (D1) | Typical | token present on a command that has the mode | true | mode on | OK |
| `unattended-switch` | SPEC:128 | Legitimate Edge Case | token present on a coordinator-only command | n/a | unspecified (F-08) | GAP |
| `unattended-switch` | SPEC:228 | Sentinel Value Match | the token text inside quoted content | n/a | no rule that only a standalone token counts (F-08) | GAP |
| `unattended-switch` | SPEC:52, 73 | Legitimate Edge Case | installed copy older than the change | false | unspecified; gates stay live (F-08) | GAP |
| `confidence-gate` (task) | SPEC:121 | Zero/Empty | confidence 0.0 | true | blocked | OK |
| `confidence-gate` (task) | SPEC:121 | Legitimate Edge Case | confidence exactly 0.70 | false | proceeds ("below 0.70" blocks) | OK |
| `phase-gate` | SPEC:154 | Typical | earlier phase checks pass | true | later phase starts | OK |
| `phase-gate` | SPEC:154, 194 | Legitimate Edge Case | P0 check AC-0.4 evaluated literally | false | cannot pass; failure "reopens section 1" (F-03) | GAP |

Classes left out: Maximum/Overflow for `contract-location`, `outcome-mapping`, `unattended-switch`, `confidence-gate` and `phase-gate` (no count or capacity is involved; path-length limits are not part of this document); Zero/Empty and One/Minimal for `wait-split` beyond the single-second row (a zero-length wait cannot trip the guard); Zero/Empty, One/Minimal and Maximum for `readiness-fallback` (the document gives no numeric domain beyond the 30 s and 60 s figures). `depth` (SPEC:33, 214): the setting is fixed at 1 and a malformed value falls back to 1 (CAPS:100), so no input class changes the spec's behavior; WC-8 forbids the call at any depth.

FR-8 and FR-9 handling: each GAP above carries a finding id. The GAPs in `contract-location` map to blocking F-01 and the `phase-gate` GAP to blocking F-03 (each names a concrete wrong outcome); the other GAPs name an undefined state or a guess between readings and are Medium (F-04, F-05, F-08, F-09, F-10).

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered by the spec's own accounting pipeline: commands are classified, assigned to phases, and each phase has a consumer that expects a count. The Consistency Check found one mismatch (F-02).

```text
[Source: 43 command files = 21 (INV-A:3) + 22 (INV-B:3)]
   |
   v
[Stage 1: verdict, SPEC:76] --> 10 ready (SPEC:81-92) + 27 needs-change (SPEC:97-125) + 6 coordinator-only (SPEC:132-137) = 43   (conserved)
   |
   v
[Stage 2: phase assignment, SPEC:156-162]
   ready 10          --> P1 fix-only 4 (adversarial, cleanup-audit, index-repo, workflow)
                         P2 4 (reflect, release-split, tdd, troubleshoot)
                         no phase 2 (brainstorm, init-lite)                              = 10   (conserved)
   needs-change 27   --> P1 9 + P2 11 + P3 4 + P4 3                                      = 27   (conserved)
   coordinator-only 6 --> no phase, no --unattended (SPEC:128)                           = 6
   |
   +--> [Consumer A: P1 Commands column, SPEC:159: 9 + 4 fix-only = 13 commands touched in P1]
   +--> [Consumer B: P1 scope sentence, SPEC:159: flag accepted by 37 (10 + 27)]       <-- MISMATCH 37 vs 13
   +--> [Consumer C: AC-1.1, SPEC:195: 37 commands have the Unattended mode section]    <-- MISMATCH 37 vs 13
   +--> [Consumer D: SPEC:154, 162, 240: 3 commands (implement, post-release, pr-submit) unchanged until D2-D4]
                                                                                        <-- conflicts with B and C
```

Concrete scenario (FR-19): 13 commands are changed in P1; AC-1.1 expects 37 sections after P1; 22 commands with gate or outward changes are assigned to P2-P4 (15 + 4 + 3); and the P1 scope sentence puts the flag on all 37, including the 3 that SPEC:154 and SPEC:162 hold back.

## Panel notes by expert (review order)

1. Wiegers: acceptance of WC-4 and WC-5 as requirements fails on location and edge states (F-01, F-04, F-05); two small wording gaps (F-17, F-19). Lead on the requirements bucket.
2. Adzic: the document gives concrete examples for D1 and several checks, but WC-4 has no sample file (F-04) and `partial` hides a state (F-16).
3. Cockburn: the primary actor (coordinator, with the person as owner of D1-D5) is clear; the one gap is the decision-timing statement (F-18).
4. Fowler: the abstraction "report file at `<output-dir>`" leaks four different output-argument styles (F-01); the phase pipeline has a count mismatch (F-02); shared state (F-07) and nested reflect (F-13).
5. Nygard: failure modes are only partly covered: stale or empty reports (F-04, F-05), in-place re-runs (F-11), stall detection (F-14), long waits (F-10).
6. Whittaker: five attacks applied; Zero/Empty, Sentinel Collision, Divergence, Sequence and Accumulation each produced a recorded finding or a table row.
7. Newman: no contract version and no handling of older installed commands (F-04, F-08).
8. Hohpe: the report-by-file with a pointer message is a sound pattern; the open points are the ordering of file and message (F-05) and what the `ask` exchange may carry (F-15).
9. Crispin: untested requirements and two checks that cannot pass as written (F-03, F-09, F-12).
10. Gregory: the spec asks the user five questions with recommendations (D1-D5), which is good practice; the quality expectation for the 10 "ready" verdicts is stated only by reading files (F-09).
11. Hightower: operational points are limited to stall detection and heartbeats (F-14, F-10); no cloud-native concern applies.

Consensus: the central decision (Orca coordinates, commands stay the units of work) is supported by the evidence the spec lists, and the spec states its own evidence gaps plainly (SPEC:41-45). Disagreement: none among the experts on the grading; Fowler and Whittaker rate F-02 CRITICAL on count mismatch, the others accept blocking.

## Synthesis

```yaml
quality_assessment:
  clarity: 7
  completeness: 6
  testability: 5
  consistency: 6
  overall: 6
priority_ranking:
  high: [F-01, F-02, F-03]
  medium: [F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15]
  low: [F-16, F-17, F-18, F-19, F-20, F-21]
```

The decision, the command inventory accounting (43 = 10 + 27 + 6) and the per-command rows are consistent with the inventories at the line anchors checked. The blocking defects are all in the contract and rollout mechanics: where the report goes (F-01), what each phase must deliver (F-02) and whether the first gate can pass (F-03). Each is a small edit.

## Follow-up candidates

Medium (warnings; never trigger a revision): F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15.
Minor (notes): F-16, F-17, F-18, F-19, F-20, F-21.
Issue question for the user: not asked in this run (the brief fixes the final reply to `DONE <path>`); the list is only recorded here.

## Reviser brief

Blocking finding ids: F-01, F-02, F-03.

Contract for the reviser (Review Loop bullet 6; the reviser reads this report, not the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size of the candidate before (57870 bytes at the hash above) and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS.

verdict: FAIL
