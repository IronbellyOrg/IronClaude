review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document, first review)

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Label | whole-document audit of the final spec, first review |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full) |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (424 lines) |
| Candidate SHA-256 | `dfd8eb09ad658caf27fb1ccbd22af2c367bacfaff3af8eab38b6eb4f622b5aad` |
| Baseline | not given; neither `--re-review` nor `--baseline` was passed, so this is a first review of the full document |
| Reviewer model actually used | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Date | 2026-11-10 |
| Mode flags | `--unattended` not passed, so the "Unattended mode" section of the command does not apply and no `return-contract.yaml` is written. `~/.claude/WORKER-CONTRACT.md` is not in the sandbox and was not needed. |
| Brief clauses overridden | none |

Citation keys: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `SPCMD:N` = line N of `command.md` in the sandbox (the `/sc:spec-panel` definition). `README:N` = `.dev/orca-command-refactor/README.md`.

## 1. Coverage

Read in full: the candidate (`SPEC:1-425`), `README:1-38`, `INV-A:1-120`, `INV-B:1-323`, `CAPS:1-188`, the command definition and the review-loop prompt file.

Checked against the inventories (all landed on the cited content, no mismatch found): the 43 = 10 + 27 + 6 split and the phase lists (P1 14 + load, P2 15, P3 4, P4 3; 36 commands receive the flags, load gets a usage-line fix, 6 are coordinator-only), every `INV-A:N` and `INV-B:N` row citation in section 3 and 4, every `CAPS:N` citation in sections 1, 2 and 8 and in the UNVERIFIED list, and the Orca-guide facts they quote.

Not checkable from the workspace, therefore UNVERIFIED and not graded: every `src/superclaude/...` source line cited directly (the `cmd/` and `sk/` keys), `CLAUDE.md:N`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `pyproject.toml:38`, `src/superclaude/cli/install_core.py`, E5's grep result (`SPEC:27`) and the Orca guides themselves. The spec already marks several of these (UNVERIFIED items 20 and 8).

Grading rule applied (FIRST-REVIEW grading check): a finding is blocking only if "an implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption. A requirement the document never states is Medium even when its label is MAJOR.

Findings table (ids used below; Medium and minor never fail the review):

| Id | Label | Grade | One line |
|---|---|---|---|
| B-01 | MAJOR | blocking | A retry re-runs the same Task text, so it writes into the first attempt's fixed `--output`, which WC-6 forbids |
| M-01 | MAJOR | Medium | `--report-dir` without `--unattended`: SA-3 and WC-4 disagree |
| M-02 | MAJOR | Medium | `--unattended` with `--interactive` is undefined for the P1/P2 ready commands |
| M-03 | MAJOR | Medium | No path for a `blocked` question's answer to reach a new attempt |
| M-04 | MAJOR | Medium | P2 grant flags depend on D4, but section 6 says Phases 1-3 need only D1 |
| M-05 | MAJOR | Medium | The WC-10 mechanism does not give the "never more than 5 minutes apart" guarantee it claims |
| M-06 | MAJOR | Medium | The report validity rule never checks the deliverable the report names |
| M-07 | MAJOR | Medium | `answer_wait` and the coordinator's silent-worker limit have no default or bound |
| M-08 | MAJOR | Medium | The WC-13 nest list is incomplete; tasklist's Stage 9 `/sc:task` and reflect's `needs_human_decision` HALT are not resolved |
| M-09 | MINOR | Medium | The `--report-dir` refusal list is narrower than the supplied `/sc:spec-panel` definition |
| M-10 | MINOR | Medium | AC-0.4's adversarial smoke run needs a report file the spec says is not yet fixed |
| M-11 | MINOR | Medium | WC-9 promises a flag per command in section 3; cli-eval, research, review-translation have none |
| N-01 | MINOR | minor | Decisions table: two rows fused on `SPEC:354` |
| N-02 | MINOR | minor | AC-C1 says AC-0.3 checks the HOW-WE-WORK Orca section; it checks only deleted lines |
| N-03 | MINOR | minor | WC-1 states a 45 s failure as observed; the evidence predicts it |
| N-04 | MINOR | minor | AC-C5 (`^-[^-]`) fails when a flag is added to an existing Usage line |
| N-05 | MINOR | minor | No rule for an unknown `contract_version` |
| N-06 | MINOR | minor | `k` is defined two ways (invocation count; phase number) |
| N-07 | MINOR | minor | AC-1.3 "scratch worktree" does not say how it is created |
| N-08 | MINOR | minor | 7.2 step 5 transcript search can match protocol text, not only calls |
| N-09 | MINOR | minor | UNVERIFIED observation: installed commands outside the inventory |

## 2. === REQUIREMENTS ANALYSIS ===

Panel order: Wiegers (lead), Adzic, Cockburn.

**Wiegers (testability, completeness).** The spec is unusually testable: 13 numbered requirements, a coverage table (`SPEC:278-292`), per-phase acceptance checks with pass conditions, and every UNVERIFIED assumption names the check that resolves it (`SPEC:363-385`). Two requirements are verified only "by inspection" (WC-1, WC-12; `SPEC:280,291`), which is acceptable because both belong to launch setup and the worker brief. The gaps are in stated-but-unmeasurable edges, listed as M-05, M-06, M-07 below.

**Adzic (examples).** Section 2.4 gives four worked examples (a pre-conversion brief, a converted brief, a success contract, a blocked contract; `SPEC:92-124`). They are useful, and they are also where B-01 shows: the converted-brief example fixes `--output` outside the per-attempt directory. No example covers a retry, an `ask` round trip, or a `partial` contract; M-03 and B-01 would be easier to see with one.

**Cockburn (actors and goals).** Primary actors are clear: the coordinator (plans, briefs, reads reports) and the worker session (runs one command, reports). The person is the secondary actor and the last resort (`SPEC:85,87`). The use case that is missing is the person's turn after `blocked`: the spec stops at "passes a `blocked_question` to the person unchanged" (`SPEC:87`) and never says how the person's answer reaches the next attempt (M-03).

### B-01 (MAJOR, blocking, Wiegers/Adzic): a retry writes into the first attempt's explicit output path

- Issue: WC-6 says a retry "must not corrupt the first attempt's output" and that a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean" (`SPEC:67`). WC-4 says a retry "gets a new directory without the coordinator changing the Task's text" (`SPEC:65`). 2.3 item 2 puts "the exact arguments" in the brief (`SPEC:79`). The converted-brief example passes a fixed `--output .dev/orca-runs/analyze-1/analysis.md` (`SPEC:102`, repeated in the contract at `SPEC:112`); 3.1 requires the brief to pass `--output <dir>` for adversarial, brainstorm and tdd and gives their resume as "else fresh dir" (`SPEC:134-135,141`); WC-11 says default paths carry "the slug the coordinator passes" (`SPEC:72`). WC-6 closes by saying the report directory is new per attempt "so the two never collide" (`SPEC:67`), but only the report directory is made per-attempt; the deliverable path stays whatever the brief says.
- Grading sentence: An implementer who follows the stated text as written builds a brief template with a fixed `--output` and a coordinator that retries with the Task text unchanged, so the retry's command line carries the same `--output`, and X is wrong because WC-6 forbids a retry from corrupting the first attempt's output and no stated text gives the command a way to pick a fresh directory when the caller named one.
- Trace: before: Task text T contains `--output O`; attempt 1 (Dispatch `disp_a`) writes part or all of its deliverable under O and settles `failed`. Retry: `worker-start --retry-of disp_a` (T unchanged, `SPEC:65`) starts `disp_b`; the command has no resume flag in the brief, so by WC-6 it "starts clean" in O. After: O now holds attempt 2's output, or a mix of both, while `<report base>/disp_b/` is new. AC-2.7 then passes, because it hashes only the first contract (`SPEC:264`), so no acceptance check can catch it.
- Recommendation: make the two texts agree by narrowing, not by adding a mechanism. Either (a) state in 2.3 item 2 and in the 2.4 example that a brief's `--output`/`--output-dir` for a "fresh dir" command lives under the per-attempt directory chosen by the worker, or (b) change WC-6 to say that a retry into an explicit output path overwrites it, and that the coordinator reads only the latest attempt's output. Extend AC-2.7 to hash the deliverable, not only the contract.
- Priority: High. Quality impact: Consistency +1, Testability +1.

### Medium findings, requirements (follow-up candidates, not in the Reviser brief)

**M-01 (Wiegers).** SA-3 says the contract and report files are written "only in unattended mode or when the caller passes `--report-dir`" (`SPEC:199`), which reads as `--report-dir` alone writing a contract. WC-4 says "In unattended mode the command writes `<report-dir>/return-contract.yaml`" and refuses `--unattended` without `--report-dir` (`SPEC:65`); the reverse case (a `--report-dir` with no `--unattended`, gates still live) is stated nowhere else. An implementer can pick either reading; neither is shown to be wrong, so Medium. Recommendation: say whether `--report-dir` alone is accepted (and writes the contract with gates live) or is a usage error.

**M-02 (Whittaker, Divergence Attack; detail in section 4).** 3.1 handles `--interactive` for adversarial, brainstorm and release-split only as "Brief must pass: never `--interactive`" (`SPEC:134-135,140`), while 3.2 says "`--interactive` refused" under `--unattended` for cleanup, improve and roadmap (`SPEC:154,161,169`). WC-2 says no `AskUserQuestion` under `--unattended` (`SPEC:63`). Nothing states what a P1 command does with `--unattended --interactive`. Medium: it needs a coordinator that passes both flags.

**M-03 (Cockburn).** After a gate resolves as blocked and `answer_wait` ends, the worker settles `failed` (`SPEC:64`); the coordinator then "passes a `blocked_question` to the person" (`SPEC:87`). The answer must reach the next attempt as an `--answer` or flag in the command line, but a retry keeps the Task's text unchanged (`SPEC:65`) and whether a Task's text can be edited is UNVERIFIED 21 (`SPEC:383`). The spec relies "only on" retry-with-unchanged-text, so the one path it does support cannot carry the answer; a new Task (not a retry) is not mentioned. Also, the 2.3 retry bound counts "a reported failure" (`SPEC:85`) without saying whether a `blocked` report counts. Medium: an undefined state, not a stated text that does harm.

**M-04 (Wiegers).** Section 6 says "Phases 1-3 need no user decision beyond D1" (`SPEC:205`) and section 9 says Phases 0-3 "can proceed on the recommendations" with rework only for D1 (b) (`SPEC:307`). D4 is listed as affecting "auggie-review `--post-pr`, task `commit`/`push`" (`SPEC:326`), and both are P2 rows that add grant flags (`SPEC:151,172,211`). D4 (b) "Never" would make those flags unnecessary. Medium: the recommended answer lets P2 proceed, so no wrong build follows without a guess.

**M-06 (Wiegers, Whittaker Zero/Empty).** The validity rule (`SPEC:66`) requires the file to exist, be non-empty, parse, carry `command` and a valid status. It does not require `report_path` to exist when `status: succeeded`; 2.4's blocked example uses `report_path: null` (`SPEC:121`). A `succeeded` contract with `report_path: null` or a missing file, for a command whose job is a deliverable, passes the rule and 7.2 step 4 (`SPEC:240`). 2.3 says the coordinator opens the report (`SPEC:87`) but does not say it checks the deliverable. Medium.

**M-10.** AC-0.4's third smoke run is `/sc:adversarial --compare <two files> --depth quick --output <dir>` (`SPEC:253`), and the pre-conversion rule makes "the report" the command's own named file from the 3.1 column "Report today" (`SPEC:66`). For adversarial that column says "contract, but filename not fixed" (`SPEC:134`) and the fix lands in P1; INV-A found it written in two different places (`INV-A:60`). The brief for this run therefore has no file name to give `--report-path`. Medium: the brief can name the merged output, but the spec does not say so.

**M-11.** WC-9 says each default that "calls a paid external run" is off unless a flag in the brief turns it on, and "Section 3 names the flag per command" (`SPEC:70`). Section 3 names flags only for auggie-review, task, post-release and pr-submit. cli-eval `run` executes real evals (`INV-A:44`), research and review-translation call Tavily (`INV-B:38,39`); their rows name no grant flag (`SPEC:155,167,168`), and AC-2.8 runs a real eval with only `--suite` and the "safety flags" (`SPEC:265`), which the spec never equates with the grant. Medium: the term "paid external run" is undefined for these rows.

## 3. === ARCHITECTURE ANALYSIS ===

Panel order: Fowler (lead), Nygard, Newman, Hohpe (Whittaker follows in section 4).

**Fowler (boundaries, interfaces).** The central boundary is sound and well argued: the coordinator owns Orca calls, the command owns a self-contained unit of work, and the seam is a flag plus a report file (`SPEC:18`, rejected alternative `SPEC:30-41`, SA-2 `SPEC:198`). Every R1-R5 reason is backed by a checkable `CAPS` line (spot-checked: `CAPS:97-101,103,145,147-150,158`). Responsibility is split cleanly in the "Owner" column of 2.2. Two interface smells: (1) three flags with different meanings of "output" (`--output` file or dir, `--output-dir`, `--report-dir`), which the spec resolves explicitly (Decisions, `SPEC:349`); (2) the `status`/`worker_status` dual vocabulary (`SPEC:65`), where the coordinator "reads `worker_status` when present and `status` otherwise". That works, and the AC-0.5 mapping is the right place to fix it, but it leaves two sources of truth in legacy contracts; accepted as a documented trade-off.

**Nygard (failure modes).** Strong: stall detection uses positive proof only (`SPEC:85`, `CAPS:125-127`); the circuit breaker is read correctly (`CAPS:80,116`); a bounded retry is added on the coordinator side. Weak points are the unbounded values in M-07 and the heartbeat arithmetic in M-05. Not covered: a failed `worker_done` send (Orca not running mid-run; `CAPS:147`) and the `--retry-request` mechanism for lost mutation replies (`CAPS:117`); noted under N-05 as a minor.

**Newman (versioning, evolution).** `contract_version: 1` is added to every contract and legacy version fields are kept (`SPEC:65`). There is no rule for what a coordinator does with a `contract_version` it does not know, or with unknown extra fields (N-05).

**Hohpe (messages).** Correlation is good: the Dispatch ID names the report directory (`SPEC:65,350`). Ordering is stated: contract written completely before `worker_done` (`SPEC:65`). Delivery: `worker_done` "exactly once" (`SPEC:66`) with Orca settling automatically (`CAPS:77`); the report is a pointer Orca does not check (`CAPS:79`), and the spec correctly makes the coordinator open the file.

### Medium findings, architecture (follow-up candidates)

**M-05 (Nygard, Whittaker Accumulation).** WC-10 says "a heartbeat at least every 5 minutes while working", then derives it from: waits of at most 4 minutes, and "a heartbeat immediately before each wait call longer than 1 minute, so two heartbeats are never more than 5 minutes apart" (`SPEC:71`). The derivation fails for a chain of short waits. pr-submit's loop is "one foreground poll, then a sleep of at least `--poll-interval`" repeated (`SPEC:71`, `INV-B:95`); with 30 s sleeps and 40 s polls no call exceeds 1 minute, no heartbeat is required by the mechanism, and 10 iterations leave 11 or more minutes without one. The top-level sentence still requires a heartbeat, so an implementer who reads both gets a conflict, not a wrong build; Medium. Whether Orca uses heartbeat age at all is UNVERIFIED (`CAPS:182`, `SPEC:71`). Recommendation: state the 5-minute rule as the requirement and the 1/4-minute rule as one way to meet it, or require a heartbeat after every 4 minutes of accumulated wait.

**M-07 (Nygard, Whittaker Zero/Empty).** `answer_wait` is "stated in the brief" (`SPEC:64,82`); the spec defines 0 (`SPEC:104,259`) and 15 minutes (`SPEC:263`) but not an omitted value or an upper limit. The coordinator's limit for a silent worker is left to the coordinator: "sets its own limit" with no default (`SPEC:85`). Without defaults the brief template (P0) will invent them. Medium.

**M-08 (Fowler, Whittaker Divergence).** WC-13's "Nests:" evidence lists seven parent-child edges (`SPEC:74`) but the inventories show more: tasklist Stage 9 patches via `/sc:task --compliance strict` (`INV-B:211`), cli-eval runs `/sc:spec-panel` and `sc:adversarial-protocol` (`INV-A:44`), roadmap calls adversarial and `sc:save` (`INV-B:151,154`), pr-submit may call `/sc:auggie-review` (`INV-B:91`). The general rule in WC-13 still applies to them, so an implementer who reads the skills gets it right; the 3.2 tasklist row and AC-2.9 mention only reflect children (`SPEC:173,266`). A second, related gap: tasklist's Stage 10.5 `needs_human_decision` items HALT (`INV-B:209`), and the tasklist row relies on reflect's headless auto-accept rule "so the headless rule applies" (`SPEC:173`) without saying what happens to those HALTs (UNVERIFIED 9, `SPEC:371`, says whether reflect treats a worker as headless is unknown). A silent HALT there is a stall that WC-2 exists to prevent. Medium, since the rule is general and the unknown is already flagged.

**M-09 (Nygard).** WC-4 refuses a report directory "inside `.git/`" only (`SPEC:65`). The `/sc:spec-panel` definition supplied here also refuses `.codegraph/`, any distributable folder under a `.claude/` folder, and an unwritable directory (`SPCMD:460`). Nothing in the spec stops a report base under `src/superclaude/` (a worker would write contracts into source). The spec notes the baseline mismatch in UNVERIFIED 19 (`SPEC:381`) but not this difference. Medium.

## 4. Adversarial analysis (Whittaker)

Scope: specification correctness only. Resilience and testing strategy are Nygard's and Crispin's.

1. I can break this specification by **Sequence Attack** (retry order). The invariant at **WC-6 / WC-4** ("a retry must not corrupt the first attempt's output"; retry reuses the Task text) fails when **the brief carries an explicit `--output`**. Concrete attack: before: `--output O`, attempt 1 wrote `O/a.md` and failed; after retry: attempt 2 starts in the same `O`, writes `O/a.md` again; `<report base>/disp_b/` is new, AC-2.7 hashes only `disp_a`'s contract and passes. Severity: MAJOR. This is B-01.

2. I can break this specification by **Divergence Attack**. The invariant at **WC-2** (no person-blocking step under `--unattended`) fails when **`--unattended` and `--interactive` are both passed to adversarial, brainstorm or release-split**. Concrete attack: brief `/sc:brainstorm "x" --unattended --report-dir D --interactive`; WC-2 forbids `AskUserQuestion`, `SPEC:135` forbids `--interactive` only in the brief, and `INV-A:39` shows `--interactive` adds the Socratic wait; the command either honours `--interactive` and stalls, or ignores it; the spec picks neither (M-02). Severity: MAJOR (ambiguous under attack), Medium.

3. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 validity rule** (`SPEC:66`) fails when **a `succeeded` contract names no deliverable**. Concrete attack: a command crashes after writing its contract skeleton early (or the model writes `report_path: null`) with `status: succeeded`, `artifacts: []`; file exists, non-empty, parses, has `command`, status valid; `worker_done --outcome succeeded`; 7.2 step 4 passes (`SPEC:240`). Severity: MAJOR, Medium (M-06).

4. I can break this specification by **Accumulation Attack**. The invariant at **WC-10** (`SPEC:71`) fails when **a command makes many waits of 1 minute or less**. Concrete attack: 12 iterations of poll (40 s) plus sleep (30 s) leave 14 minutes with no heartbeat, though no call exceeds 1 minute. Severity: MAJOR, Medium (M-05).

5. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-3 `--answer <gate-id>=<text>`** (`SPEC:64`) fails when **the answer text is empty or the argument has no `=`**. Concrete attack: `--answer clarify=` (empty text from a coordinator reply): split at the first `=` gives an empty answer; the gate counts as answered, the command proceeds on an empty clarification (tdd then runs on a bare topic, which `INV-B:219` says it must not). Unknown or repeated gate id is a usage error, but empty text and no-`=` are not stated. Severity: MINOR (behavior inferable as a usage error), minor, folded into N-06.

6. I can break this specification by **Sequence Attack** (phase order). The invariant at **section 6** ("a flag is never accepted while its gate is still live", `SPEC:205`) fails when **a not-yet-converted command receives `--unattended`**. Concrete attack: a brief written from the P0 template passes `--unattended` to `/sc:cleanup` (P2) in Phase 1; the command was not changed, treats the token as free text or ignores it, and waits on its Approval Required prompt (`INV-A:43`). The spec says the coordinator never passes the flag early (`SPEC:79`) but states no behavior for the command; the exposure is the brief template. Severity: MINOR, minor, covered by the AC-1.1 assertion that no command outside the phase list gains the flag.

No CRITICAL attack found. Pipeline Dimensional Analysis triggered (section 6 below); no count mismatch was found, so there is no FR-19 CRITICAL.

Auto-suggestion (advisory only, not forced): the spec introduces several mutable values (report directory contents, `answer_wait` budget, retry count, heartbeat gap) and numeric thresholds (1, 4, 5 minutes; 30 s; three failures). `--focus correctness` would add a State Variable Registry; it was not requested and is not produced.

## 5. Guard Condition Boundary Table

Trigger met (thresholds, boolean guards, sentinel values). Constructed by Nygard, completed by Crispin, attacked by Whittaker. Classes not applicable to a guard are listed in one line after the table. Status GAP rows are graded under FR-8/FR-9: none names a concrete wrong outcome that follows with no further assumption, so each is Medium (follow-up), except where a row repeats B-01 (none does; B-01 is not a guard).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `report-dir present and writable` | WC-4 `SPEC:65` | Zero/Empty | no `--report-dir`, or brief has no report base | false | command stops before work, writes no file, worker settles `failed` | OK |
| `report-dir present and writable` | WC-4 `SPEC:65` | Zero/Empty | `--report-dir ""` (empty value) | unspecified | not stated | GAP (M-09 family) |
| `report-dir present and writable` | WC-4 `SPEC:65` | Typical | `<base>/<dispatch_id>/` new directory | true | contract written | OK |
| `report-dir present and writable` | WC-4 `SPEC:65` | Maximum/Overflow | path too long or disk full | false | "cannot be created or written" stops the command | OK |
| `report-dir present and writable` | WC-4 `SPEC:65` | Sentinel Value Match | inside `.git/` | false | refused | OK |
| `report-dir present and writable` | WC-4 `SPEC:65` | Sentinel Value Match | inside `.codegraph/`, `.claude/` distributables, `src/superclaude/` | true | not stated; SPCMD:460 refuses the first two | GAP (M-09) |
| `report-dir present and writable` | WC-4 `SPEC:65` | Legitimate Edge Case | directory already holds a contract | true | overwritten (WC-3 relies on it) | OK |
| `report valid` | WC-5 `SPEC:66` | Zero/Empty | file missing or empty | false | counts as no report, `failed` | OK |
| `report valid` | WC-5 `SPEC:66` | Zero/Empty | `succeeded` with `report_path: null` or missing file | true | not stated | GAP (M-06) |
| `report valid` | WC-5 `SPEC:66` | Typical | four-value status, `command` present | true | outcome mapped | OK |
| `report valid` | WC-5 `SPEC:66` | Sentinel Value Match | status `blocked` (contract word vs Orca's Task status) | true | mapped to `--outcome failed`; never copied to Orca status | OK |
| `report valid` | WC-5 `SPEC:66` | Legitimate Edge Case | legacy status words, `worker_status` and `status` both present | true | `worker_status` wins; words mapped via AC-0.5 | OK |
| `heartbeat cap` | WC-10 `SPEC:71` | One/Minimal | chain of waits each at most 1 minute | false (no heartbeat required) | not stated; gap can exceed 5 minutes | GAP (M-05) |
| `heartbeat cap` | WC-10 `SPEC:71` | Typical | one wait of 2 to 4 minutes | true | heartbeat immediately before | OK |
| `heartbeat cap` | WC-10 `SPEC:71` | Maximum/Overflow | wait over 4 minutes | true | split into waits of at most 4 minutes | OK |
| `heartbeat cap` | WC-10 `SPEC:71` | Legitimate Edge Case | foreground Agent-tool fan-out over 5 minutes | exempt | worker heartbeats before and after; coordinator does not read the gap as a stall | OK |
| `answer_wait` | WC-3 `SPEC:64` | Zero/Empty | `0` | false | no `ask`, blocked at once | OK |
| `answer_wait` | WC-3 `SPEC:64` | Zero/Empty | omitted from the brief | unspecified | not stated | GAP (M-07) |
| `answer_wait` | WC-3 `SPEC:64` | Typical | 15 minutes, answer arrives | true | one `ask` per gate, re-invoke with `--answer` | OK |
| `answer_wait` | WC-3 `SPEC:64` | Maximum/Overflow | no upper bound; several gates | unspecified | total budget across gates; no maximum | GAP (M-07) |
| `retry bound` | 2.3 `SPEC:85` | One/Minimal | first reported failure | true | one coordinator retry | OK |
| `retry bound` | 2.3 `SPEC:85` | Typical | second reported failure | false | goes to the person with both reports | OK |
| `retry bound` | 2.3 `SPEC:85` | Legitimate Edge Case | first report is `blocked` and a person answers | unspecified | not stated how the answer is carried | GAP (M-03) |
| `unattended with interactive` | WC-2 `SPEC:63`; 3.1 `SPEC:134,135,140` | Legitimate Edge Case | `--unattended --interactive` on adversarial, brainstorm, release-split | unspecified | 3.2 refuses it for cleanup, improve, roadmap; 3.1 only says "never" in the brief | GAP (M-02) |
| `report-dir without unattended` | SA-3 `SPEC:199` vs WC-4 `SPEC:65` | Legitimate Edge Case | `--report-dir D` alone | unspecified | two readings | GAP (M-01) |
| `grant-flag conflict` | WC-9 `SPEC:70` | Legitimate Edge Case | `--post-pr` with `--no-post-pr` | true | usage error, contract `failed`, nothing posted | OK |
| `answer syntax` | WC-3 `SPEC:64` | Zero/Empty | `--answer clarify=` or no `=` | unspecified | not stated for empty text or no `=` | GAP (N-06) |
| `answer syntax` | WC-3 `SPEC:64` | Typical | `--answer clarify=text` | true | split at first `=` | OK |
| `answer syntax` | WC-3 `SPEC:64` | Sentinel Value Match | unknown or repeated gate id | true | usage error, contract `failed` | OK |
| `child index k` | WC-13 `SPEC:74` | Zero/Empty | tasklist `--no-reflect` or one phase | false | no `reflect-<k>` directories; contract accounting not stated | GAP (N-06) |
| `child index k` | WC-13 `SPEC:74` | One/Minimal | N = 1 | true | `reflect-1` | OK |
| `child index k` | WC-13 `SPEC:74` | Typical | N phases, parallel | true | distinct `reflect-1..N` | OK |

Classes left out (one line each): `report-dir` One/Minimal (any non-empty relative path behaves as Typical); `report valid` One/Minimal and Maximum (a file at the minimum fields is Typical; size is bounded only by YAML parsing); `answer_wait` One/Minimal (any positive value is Typical); `retry bound` Zero/Empty and Maximum (no failure means no retry; the bound is two); `grant-flag conflict` all classes except the conflict itself (a boolean pair has no numeric range); `child index k` Maximum (no limit stated, directories are plain names).

Crispin's completeness check: every guard found in sections 2.2, 2.3 and 6 is listed; the 30 s fallback in WC-1 and the `contract_version` value are not guards (no branch depends on them). FR-10 is satisfied: all cells populated, classes given a row or a reason.

## 6. Pipeline Dimensional Analysis and Quantity Flow Diagram

Triggered: the command inventory is a multi-stage count pipeline, and tasklist fans out. Fowler annotated, Whittaker attacked the divergence points.

```text
[Commands in cmd/: 43] --> [Inventory verdicts] --> [ready: 10] [needs change: 27] [coordinator-only: 6]    (10+27+6 = 43, OK)
        ready 10        --> P1: 6 (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow)
                        --> P2: 4 (reflect, release-split, tdd, troubleshoot)
        needs change 27 --> P1: 9 (8 flagged + load, usage line only)   P2: 11   P3: 4   P4: 3     (9+11+4+3 = 27, OK)
        flagged commands: P1 14, P2 15, P3 4, P4 3 = 36; load 1 (no flag); coordinator-only 6   (36+1+6 = 43, OK)
        consumers: AC-1.1 asserts 14 (P1 list minus load)                  [matches 14]
                   section 6 P2 row lists 15                                [matches 15]

[tasklist --unattended: N phases] --> [Stage 7: 2N validators] --> [Stage 9: M /sc:task patches, M >= 0] --> [Stage 10.5: N reflects] --> [reflect-1..N contracts]
        Consumer A: AC-2.9 and the 3.2 row expect N reflect directories             [matches N; `--no-reflect` gives 0, not stated]
        Consumer B: Stage 9 /sc:task children (M)                                   [no directory rule named in 3.2 or AC-2.9, see M-08]

[Task] --> [attempt 1 .. A (A <= 2 by the coordinator's own bound, 3 by the circuit breaker)] --> [A report directories] --> [coordinator reads the latest]
        deliverable path: 1 shared path for all A attempts when the brief fixes `--output`   <-- MISMATCH (B-01)
```

Result: no count mismatch in the command inventory or the phase lists. Two divergence points leave a consumer that assumes one count: the tasklist Stage 9 children (M-08) and the deliverable path across attempts (B-01). The second is already graded blocking on its own text; the first is Medium because WC-13's general rule covers `/sc:task` and the consumer does not "assume count conservation" in a stated sentence. FR-19 labels a mismatch CRITICAL; per the grading rule of the Review Loop (consequence, not label) neither finding is graded above its consequence.

## 7. Verified strengths (no action)

- The decision is evidence-led and states its own weak points plainly (`SPEC:43-47`); the live-run gap is made Phase 0 (`SPEC:209`, `SPEC:363`).
- Counts reconcile everywhere I recomputed them (section 6 diagram above).
- Orca facts are used correctly: `worker_done` only from the dispatched pane (`CAPS:76`), the circuit breaker excludes a worker's own `failed` report (`CAPS:80`), absence never authorizes stop or retry (`CAPS:125-127`), and the 60 s limit applies to startup only (`CAPS:52`).
- AC-2.4 and AC-4.2/4.3 name `IronbellyOrg/IronClaude` explicitly in every `gh` call and URL check (`SPEC:261,272,273`).

## 8. Follow-up candidates (Medium and minor)

Medium (warnings): M-01 to M-11 as described in sections 2 and 3.

Minor (notes):
- **N-01.** `SPEC:354`: two Decisions rows are fused with `||`, so the "Answer channel for gates with no flag" row does not render as its own row. Split the line.
- **N-02.** AC-C1 says HOW-WE-WORK's Orca section "is checked by AC-0.3" (`SPEC:223`); AC-0.3 only checks that no existing line was deleted (`SPEC:250`), and no check confirms the Orca section exists or that the mirrors carry it (AC-0.2 compares only the plugin copy, `SPEC:249`).
- **N-03.** WC-1 says "a fallback above about 45 s failed" (`SPEC:62`). The evidence is a prediction made against a 45 s limit the eval itself set: "Raising `CCSESSION_ASK_TIMEOUT` above about 45 seconds would make supervised workers fail again" (`CAPS:49`, quoting `EVIDENCE.md:56`, UNVERIFIED here). The 30 s rule is safe either way; the wording overstates.
- **N-04.** AC-C5 fails on any removed line (`SPEC:227`). Adding `--unattended` to an existing Usage line is a changed line; the supplied definition adds a second Usage line instead (`SPCMD:23`). Say which form is required.
- **N-05.** No rule for an unknown `contract_version` or extra fields (`SPEC:65,66`). Also unaddressed: a failed `worker_done` send when Orca is down (`CAPS:147`) and `--retry-request` for lost replies (`CAPS:117`).
- **N-06.** `k` is "the 1-based count of that child's invocations" for most parents and "the phase number" for tasklist (`SPEC:74,173`); if phase numbering is not 1-based and contiguous the two differ. Empty `--answer` text and a missing `=` are also not stated (`SPEC:64`).
- **N-07.** AC-1.3 asks for "a scratch worktree" (`SPEC:256`) without saying how it is made. The repo rule in `CLAUDE.md` requires Orca-created worktrees with an agent (UNVERIFIED here: `CLAUDE.md` is not in the sandbox).
- **N-08.** 7.2 step 5 searches the transcript for `AskUserQuestion` (`SPEC:241`); a loaded protocol quotes that word (for example troubleshoot says "never AskUserQuestion", `INV-B:239`). The pass condition says "call", so restrict the search to tool-use records.
- **N-09.** UNVERIFIED observation, not graded: the skill list available to this reviewer names installed commands that are not among the 43 inventoried (`sc:graph`, `sc:impact`, `sc:issue`) and describes `sc:issue` as creating an Orca worktree. If the repo state under review has them, E5 (`SPEC:27`), the AC-C1 baseline and the "43" count are stale. Not checkable from the workspace.

Issue question: the command asks the running session to ask the user once per loop whether to open an issue for the follow-up candidates. This run is a worker with no user channel and no `--unattended` report directory; nothing was asked and no issue was created. The list above is the record.

## 9. Quality scores (0-10)

Clarity 8, Completeness 7, Testability 8, Consistency 6 (B-01, M-01, M-04 and M-05 are the consistency losses).

## Reviser brief

Blocking finding ids: **B-01**.

Rules for the reviser (this restates the Reviser contract; the reviser reads this report, not the command):
- Revise only text a blocking finding names: for B-01, WC-6 (`SPEC:67`), the 2.3 item 2 text on exact arguments (`SPEC:79`), the 2.4 converted-brief example (`SPEC:100-114`), and AC-2.7 (`SPEC:264`).
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id (B-01).
- Prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave every Medium and minor finding alone (M-01 to M-11, N-01 to N-09). Do not award a PASS; return the candidate once.

verdict: FAIL
