review: 1 of 3

# /sc:spec-panel audit: Orca worker-contract spec (critique mode, focus requirements,architecture)

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Label | whole-document audit of the final spec; a first review of the whole document (brief) |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 379 lines |
| Candidate sha256 | `95746463446db9b44a66e9389562c81d93a8d4e3fcaaec808dc338416eae8287` |
| Baseline / prior | none given; first review (no `--re-review`, no `--baseline`) |
| Reviser/reviewer model | `claude-sonnet-5-5` (Sonnet 5.5) |
| Review date | 2026-11-10 |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` |
| Brief clauses overridden | none |

Citation shorthand (all paths under the sandbox workspace `ws/`): `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `INV-A:N` / `INV-B:N` / `CAPS:N` = `.dev/orca-command-refactor/inventory/commands-a.md` / `commands-b.md` / `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`; `CMD:N` = the command definition `command.md`; `PROMPTS:N` = the review-loop prompts file.

## Coverage (what was and was not checked)

- Read in full: the spec (SPEC:1-379), the README (README:1-38), all three inventories, `CMD:1-491`, `PROMPTS:1-55`.
- Checked against the inventories: every `INV-A:N`, `INV-B:N`, `CAPS:N` citation in the spec's sections 1, 2, 3, 4, 7, 8 and 9, spot-checked line by line (the section 3 per-row `INV` lines, the section 1.2 and 1.3 evidence tables, the WC-1 to WC-12 evidence cells, the UNVERIFIED items). Two deviations found: R9 and R10. The counts hold: 43 = 21 + 22 (INV-A:3, INV-B:3) = 10 + 27 + 6, and the phase assignment sums to 13 + 15 + 4 + 3 + 2 = 37 = 10 + 27 (SPEC:105, SPEC:187-191).
- UNVERIFIED (not checkable in this sandbox, so taken only as quoted by an inventory line): every citation into `src/`, `CLAUDE.md`, `pyproject.toml`, `EVIDENCE.md`, `.dev/codegraph-migration/`, `.dev/orca-command-refactor/review/spec-panel*.md`, `review/disposition*.md`, `specs/history/spec-v2.md` and the Orca install tree. The spec's own "re-read 11 locations" claim (SPEC:11) and the "340 citations, 9 defects" claim (SPEC:373) are likewise unchecked here.
- Not run: the Improve step (step 6 of the Behavioral Flow). The brief confines writes to this file, and a first review writes no revised specification. The `AskUserQuestion`-style issue offer of the Review Loop (`CMD:260`) was not put to a user: the brief limits the final reply to `DONE <path>`. No issue was opened; the follow-up list below is recorded for the coordinator.

## Mandatory output artifacts (completed before synthesis, `CMD:334`)

### Guard Condition Boundary Table

Triggered: the spec contains threshold checks, boolean guards and sentinel comparisons. Guards enumerated: G1 to G13. The per-command gate rows of SPEC section 3 are the gate resolutions themselves (data), not guards of the contract; a gate left unbriefed is finding R6. Input classes left out are named in the line under each guard.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` token switch | SPEC:52 | Zero/Empty | flag absent | false | normal mode, no contract (SPEC:52, SPEC:177) | OK |
| G1 | SPEC:52 | One/Minimal | `--unattended` alone | true | refuses without `--report-dir` (SPEC:65) | OK |
| G1 | SPEC:52 | Typical | `--unattended --report-dir d` | true | runs, writes contract | OK |
| G1 | SPEC:52 | Sentinel Value Match | `"what does --unattended do"` (quoted topic) | false | stays in normal mode (SPEC:52, AC-1.5 SPEC:246) | OK |
| G1 | SPEC:52 | Legitimate Edge Case | `--unattended=1`, token repeated, token inside pasted text | false / true / false | the form `--unattended=1` is not the standalone token, so normal mode is inferrable; repeat is harmless | OK |
| G2 `--report-dir` usable | SPEC:65 | Zero/Empty | absent, `""` | false | refuse before any work, chat only, nothing written, worker sends `failed` (SPEC:65, AC-1.7 SPEC:248) | OK |
| G2 | SPEC:65 | One/Minimal | `.` or an existing empty directory | true | contract written; replaces an existing `return-contract.yaml` there only (SPEC:65) | OK |
| G2 | SPEC:65 | Typical | fresh existing directory | true | contract written | OK |
| G2 | SPEC:65 | Sentinel Value Match | path inside `.git/` or a `.claude/` sync-dev folder; a file; a read-only directory | false | refuse (SPEC:65) | OK |
| G2 | SPEC:65 | Legitimate Edge Case | nonexistent but creatable path; a symlink or `..` path that resolves into `.git/` | ? | not stated (the unusable list at SPEC:65 names neither creation nor resolved-versus-lexical checking) | GAP |
| G3 `partial` needs `incomplete_items` | SPEC:65, SPEC:66 | Zero/Empty | `partial` with `[]` | false | WC-4 requires a non-empty list; WC-5 still maps `partial` to `succeeded`; only the acceptance assertion (SPEC:228) fails it | GAP |
| G3 | SPEC:65 | One/Minimal | one item | true | `succeeded` outcome; coordinator withholds dependents (SPEC:66) | OK |
| G3 | SPEC:65 | Sentinel Value Match | `blocked` with empty `blocked_question` | ? | "when blocked `blocked_question`" (SPEC:65); non-emptiness asserted only in AC-2.2 (SPEC:253), not in step 4 (SPEC:228) | GAP |
| G4 outcome mapping | SPEC:66 | Zero/Empty | report absent, empty, unparseable | n/a | `--outcome failed` | OK |
| G4 | SPEC:66 | Sentinel Value Match | `status: running`; a status word outside the five with no `native_status` | n/a | `failed` | OK |
| G4 | SPEC:66 | Legitimate Edge Case | `status: succeeded` while a file in `report_path`/`artifacts` is missing | ? | not stated; the coordinator "opens the report" (SPEC:66), step 4 checks only the contract (SPEC:228) | GAP |
| G5 retry cap (2 per Task) | SPEC:66 | Zero/Empty | 0 retries so far | allowed | retry permitted | OK |
| G5 | SPEC:66 | Maximum/Overflow | third retry | false | report the Task to the person | OK |
| G5 | SPEC:66 | Legitimate Edge Case | failed starts plus retries | n/a | Orca's own breaker counts failed starts only (CAPS:80, CAPS:116), cited at SPEC:66 | OK |
| G6 `ask` timeouts (3) | SPEC:64 | Typical | 1 or 2 timeouts | resume | resume same message ID | OK |
| G6 | SPEC:64 | Maximum/Overflow | 3 consecutive timeouts | true | gate resolves blocked | OK |
| G6 | SPEC:64 | Legitimate Edge Case | coordinator replies after the third timeout | ? | not stated; Orca keeps the timed-out question pending (CAPS:60), the worker has already settled `failed` | GAP |
| G7 fan-in minimum M | SPEC:81-84 | Zero/Empty | 0 usable | below M | no aggregator, shortfall report (SPEC:83-84) | OK |
| G7 | SPEC:81-84 | One/Minimal | 1 usable, M = 2 | below M | shortfall report | OK |
| G7 | SPEC:81-84 | Typical | 3 of 4 usable | at or above M | aggregator on 3, dropped count in brief | OK |
| G7 | SPEC:81-84 | Maximum/Overflow | 11 usable for `/sc:adversarial` | ? | not stated; the consumer takes 2-10 (INV-A:35) | GAP |
| G7 | SPEC:82 | Legitimate Edge Case | one producer `partial`, brief silent | decided by brief | rule 3 and worked count (SPEC:82, SPEC:84) | OK |
| G8 edit-capable list | SPEC:72 | Typical | command on the closed list | true | own worktree | OK |
| G8 | SPEC:72 | Legitimate Edge Case | command not on the list; mode-dependent members | false / by flag | "not edit-capable" (SPEC:72); modes named per member (inline, UC-2, `--authorize`) | OK |
| G9 wait size | SPEC:71 | Typical | single Bash/sleep at most 4 min | true | no split needed | OK |
| G9 | SPEC:71 | Maximum/Overflow | single call above 5 min | true | must be split into at most 4 min | OK |
| G9 | SPEC:71 | Legitimate Edge Case | single Agent-tool call above 5 min | n/a | not covered; acknowledged, measured by SPEC:226, SPEC:375 | OK |
| G10 launch fallback (30 s of 60 s) | SPEC:62 | Legitimate Edge Case | fallback 31-59 s | untested | "margin ... untested" (SPEC:62) | OK |
| G11 `contract_version` | SPEC:55 | Zero/Empty | contract file unreadable or missing | n/a | every gate blocked, report still written (SPEC:55) | OK |
| G11 | SPEC:55 | One/Minimal | equal to the command's version | true | proceeds | OK |
| G11 | SPEC:55 | Maximum/Overflow | file version higher than the command's | ? | only "lower" is covered (SPEC:55) | GAP |
| G11 | SPEC:55 | Sentinel Value Match | readable file with no or non-integer `contract_version` | ? | not stated | GAP |
| G12 phase-shipped grep | SPEC:76 | Zero/Empty | neither installed nor project copy has `--unattended` | false | "ready today" form | OK |
| G12 | SPEC:76 | Legitimate Edge Case | only the project `.claude/` copy has it, or only `~/.claude/` | true | "either copy" satisfies (SPEC:76) | GAP |
| G13 precedence (prompt flag with `--unattended`) | SPEC:63, SPEC:102 | Typical | `--unattended --interactive` | block | refuse, name the flag | OK |
| G13 | SPEC:102 | Sentinel Value Match | `--post-pr` with `--no-post-pr` | `--no-post-pr` wins | specified (SPEC:91) | OK |
| G13 | SPEC:63 | Legitimate Edge Case | `--monitor 2` or `3` with `--unattended` | false | allowed; only `--monitor 1` is refused | OK |

Classes left out: G5 Sentinel (a retry cap has no sentinel value); G9 Zero (a zero-length wait needs no split); G10 Zero and Maximum (the 30 s value is a pass margin, not an input); G13 Zero (no flag, no conflict). FR-8 GAP cells yield findings R4, R8, A3, A4, A2 below, all graded Medium; no GAP names a concrete wrong outcome without a further assumption. FR-9: the blank "Specified Behavior" cells are the `?` cells above, graded the same way. FR-10: the table is complete.

### Quantity Flow Diagram (pipeline dimensional analysis triggered: fan-in changes counts)

```text
[Coordinator splits work: K producer Tasks] --> [K producer reports (contract status, or success condition SPEC:108)]
        |
        v
[WC-5 retry stage: each blocked/failed producer retried at most 2 times (SPEC:66, SPEC:83)] --> [K reports, R of the failed ones rescued]
        |
        v
[usability filter: succeeded | partial only if the brief accepts | ready-today by success condition (SPEC:82)] --> [U usable, U <= K]
        |-- U <  M --> [no aggregator; shortfall report to the person]                       (N != M handled, SPEC:83)
        |-- U >= M --> [aggregator Task: U explicit paths, no --deps on dropped, K-U stated]  (SPEC:80, SPEC:83)
                          |
                          v
                    [Consumer /sc:adversarial: expects 2..10 artifacts (INV-A:35)] <-- U > 10 NOT SPECIFIED (A4)

[Orca view of the same K Tasks]: succeeded + partial --> completed --> dependents released; failed + blocked --> failed --> dependents held (SPEC:66, CAPS:90)
        consumer "dependents via --deps" counts completed Tasks, the coordinator counts usable reports: divergence handled by the report check (SPEC:66);
        an answered gate started as a NEW Task leaves the old failed Task holding its dependents (R1)

[Inventory 43] --> [INV-A 21 + INV-B 22] --> [10 ready + 27 change + 6 coordinator-only] --> [phase P1 13, P2 15, P3 4, P4 3, no flag 2 = 37 = 10 + 27]   conserved
```

Consistency check (FR-18 step 4): the spec nowhere assumes U = K; it names M, the explicit list and the dropped count (SPEC:80-84). So no FR-19 conservation mismatch (not CRITICAL). One capacity mismatch (U above the consumer's maximum) is A4, Medium.

## Expert sequence (fixed order, `CMD:99-113`)

- **Wiegers** (lead, requirements): the requirements WC-1 to WC-12 are testable and owner-tagged (SPEC:60-73). Weak spots: the answered-retry path (R1), no production stall rule (R2), success conditions that depend on unknown status words (R3), report-dir path meaning (R4), approval flags with no proof of the person's answer (R5), ready-today briefs that omit a gate (R6).
- **Adzic**: the worked count (SPEC:84) is the only example-driven rule; fan-in, WC-11 separation, WC-12 `consumer_fenced` and the partial rule have no behavioural scenario (R7). Degenerate variants for `partial` and `blocked` are R8.
- **Cockburn**: primary actors are clear (coordinator, worker, person; SPEC:50-76). The person's goal at an approval gate is protected in prose (SPEC:66, SPEC:352) but not in the artifacts (R5). The `--compliance` override the person would use for `/sc:task` is mis-stated (R9).
- **Fowler** (lead, architecture): the Orca-on-top split and the two-part contract file are sound bounded contexts (SPEC:55, SPEC:279-287). Interface smells: WC-1 and WC-8 sit in neither part (A5); the nested-invocation rule is order-dependent (A1); section 4 over-states (A6).
- **Nygard**: failure modes mostly covered (stale `running`, fencing, fail-closed, retry cap: SPEC:55, SPEC:65-66, SPEC:73). Missing: nothing tells a production coordinator to watch for the silent stall (R2); late replies after a resolved gate (R8).
- **Whittaker** (adversarial, below): five attacks, three confirmed findings (R4, R1, A4), two held.
- **Newman**: `contract_version` handles older files only (A3); the phase-shipped probe can pass on a stale copy (A2).
- **Hohpe**: claim-check pattern (report path in `worker_done`, file opened by the coordinator) is right and the delivery rules are explicit (SPEC:65-66, SPEC:80-84). The aggregator's capacity bound is missing (A4); a replacement Task versus `--retry-of` changes message ownership (R1).
- **Crispin**: acceptance checks are concrete and runnable; two are weaker than they look (R11) or static only (R7).
- **Gregory**: the three-amigos gap is the retry/answer mechanics (R1), where coordinator author, command author and Orca owner each assume a different carrier.
- **Hightower**: operational concerns (heartbeats, wait sizes, release) are covered (SPEC:71, SPEC:231); observability for production runs is not (R2).

## Whittaker attack findings (`CMD:76-82`)

1. I can break this specification by **Zero/Empty Attack**. The invariant at **SPEC:65 (refuse an unusable `--report-dir`)** fails when **the value is a nonexistent path or a symlink that resolves into `.git/`**. Concrete attack: before: `ln -s .git/hooks /tmp/rd`; brief passes `--report-dir /tmp/rd`; the lexical test "inside `.git/`" passes; after: the command's first action writes `return-contract.yaml` into `.git/hooks`. For a nonexistent path the text neither creates nor refuses. Severity MAJOR, graded Medium (R4): the harm is a stray file, not data loss, and the gap is a missing restriction.
2. I can break this specification by **Divergence Attack**. The invariant at **SPEC:63 (nested rule, WC-2 (iv))** fails when **the caller's phase has shipped but the invoked command's phase has not**. Concrete attack: P1 has shipped, P2 has not; `/sc:workflow "x" --unattended --report-dir d` reaches Wave 4, which runs reflect (INV-B:271); reflect has a phase (SPEC:189) and takes flags, so the parenthetical "a command that takes no flag" does not clearly exempt it; the step "resolves as blocked"; every happy-path workflow run in P1 ends `blocked`. Severity MAJOR, graded Medium (A1).
3. I can break this specification by **Sentinel Collision Attack**. Probed: the contract word `blocked` versus Orca's Task status `blocked`; `running` versus a real result; `--unattended` inside content. The spec separates all three (SPEC:66, SPEC:65, SPEC:52). Held; no finding.
4. I can break this specification by **Sequence Attack**. The invariant at **SPEC:66 plus SPEC:97 (an answered gate re-runs the work)** fails when **the answer is carried by a new Task rather than `--retry-of`**. Concrete attack: producer P1 (`/sc:tdd "auth"`, bare topic) ends `blocked`, Task T1 settles `failed` (SPEC:66); aggregator A1 was created with `--deps [T1]`; the coordinator follows SPEC:97 and creates T2 with a precise topic; T2 succeeds; T1 stays `failed`, so A1 is never ready (CAPS:90). Severity MAJOR, graded Medium (R1): following SPEC:66 instead (same Task, `--retry-of`, "new brief") avoids this if Orca can carry a changed command, which no inventory line shows.
5. I can break this specification by **Accumulation Attack**. The invariant at **SPEC:81-84 (fan-in)** fails when **usable inputs exceed the consumer's capacity**. Concrete attack: 12 `/sc:troubleshoot` producers all `succeeded`; U = 12 >= M = 2; the aggregator is created with 12 explicit paths; `/sc:adversarial` accepts 2-10 (INV-A:35). Severity MAJOR, graded Medium (A4).

## === REQUIREMENTS ANALYSIS ===

No finding below is blocking. Each MAJOR-labelled item fails the blocking test of `PROMPTS:31`: its wrong outcome needs a guess (the worse of two readings the text allows) or is a requirement the spec never states.

### R1 Answered-gate re-run has two carriers and neither is shown to work
- Severity label: MAJOR. Graded: Medium. Expert: Wiegers, Whittaker (Sequence), Gregory. Priority: High.
- Issue: WC-2 (iii) and SPEC:97 say an unflagged gate is answered by "a new Task whose command line changes the input"; WC-5 says the coordinator "supplies the answer in a new brief ... and runs `worker-start --task <task_id> --retry-of <dispatch_id>`" (SPEC:63, SPEC:66, SPEC:97). A blocked run settles its Task `failed` and holds its dependents until a `--retry-of` replacement completes (SPEC:66, CAPS:90). A new Task does not complete the old one. The inventories show `task-create --spec` (CAPS:84) and list no flag by which `worker-start --retry-of` carries a changed command line (CAPS:84 quotes only part of `[H:worker-start]` line 3, so this is UNVERIFIED). SPEC:359-379 lists neither point.
- Grading check: an implementer who follows SPEC:97 builds a coordinator that answers a `tdd` bare-topic block with a new Task, and that is wrong because the failed T1 keeps its dependents blocked (SPEC:66, CAPS:90). An implementer who follows SPEC:66 builds a retry whose "new brief" has no stated carrier. Which reading is meant is a guess, so Medium.
- Recommendation: state one path. If `--retry-of`: add an UNVERIFIED item and a P0/P2 check that a changed command line on `--retry-of` is applied. If a new Task: say the dependents are created (or re-created) with `--deps` on the new Task. Rationale: this is the path every `blocked` gate takes, and AC-2.8 (SPEC:259) tests only the person-relay step.
- Quality impact: Testability and Completeness, about -1 each.

### R2 No rule makes a production coordinator watch for the silent stall
- Severity label: MAJOR. Graded: Medium. Expert: Wiegers, Nygard, Hightower. Priority: High.
- Issue: the spec's own diagnosis is that a worker parked on a prompt is "healthy" to Orca and is seen only through `agentWait` or a missing report (SPEC:44, CAPS:52, CAPS:129). Ready-today commands keep their unconverted gates (SPEC:108). The only `worker-show` polling is in the acceptance check (SPEC:226); "what the coordinator owes" (SPEC:76) and the WC-5 coordinator procedure (SPEC:66) carry no watch duty. Orca's bound on a Dispatch's run time is unknown (CAPS:188, SPEC:370).
- Grading check: an implementer who follows the text builds a coordinator that waits in `check --wait` on a ready-today worker parked at a gate (for example `release-split` on a tasklist-shaped input, INV-B:119) with no stop, because no stated text tells it to look. This is a requirement the document never states, so Medium.
- Recommendation: add one sentence to SPEC:76: while a worker runs, the coordinator reads `worker-show` for `agentWait` at least once per heartbeat interval, and a non-null value means the brief missed a gate (ask the person; stop only after positive proof, CAPS:126). Rationale: it is the only detector the spec itself says exists.
- Quality impact: Completeness about -1.

### R3 Success conditions of four ready-today commands cannot be evaluated
- Severity label: MAJOR. Graded: Medium. Expert: Adzic. Priority: Medium.
- Issue: the rows for adversarial, brainstorm, reflect and workflow judge success by "its own status word reads as success (words UNVERIFIED, item 17)" (SPEC:112, SPEC:113, SPEC:117, SPEC:121, SPEC:376). The P0 gate AC-0.4 uses exactly these (SPEC:239, step 3 SPEC:227). The reflect, workflow and troubleshoot rows also name `<output>` or `<id>` paths that the "Brief must pass" column does not supply (SPEC:117, SPEC:120, SPEC:121), so the check depends on the worker reporting the path.
- Grading check: not blocking, because the spec labels the gap and the person running P0 can read the file; Medium because the criterion as written has no decidable value until item 17 is resolved.
- Recommendation: resolve item 17 before P0 starts (read the four contracts' status vocabularies) and write the values into the four rows; add `--output` to the reflect and troubleshoot briefs. Rationale: P0 is the gate for the whole decision (SPEC:239).
- Quality impact: Testability about -1.

### R4 `--report-dir`: path meaning and unusable-value list are incomplete
- Severity label: MAJOR (Whittaker attack 1). Graded: Medium. Expert: Wiegers, Whittaker. Priority: Medium.
- Issue (a): the spec says paths are repo-relative (SPEC:4) and gives edit-capable workers their own worktree (SPEC:72) but never says whether `--report-dir` is absolute or in which worktree the coordinator opens the contract. Step 4 and the common checks run `test -s <contract>` from the repo root (SPEC:196, SPEC:228). With a relative `--report-dir` and a separate worktree the file is not where the coordinator looks. Orca does not read the path (CAPS:79). Issue (b): the unusable list (SPEC:65) omits a nonexistent creatable path and a symlink or `..` path resolving into `.git/` (table G2).
- Grading check: needs a guess about which reading the author meant; no stated text forces the wrong result, so Medium.
- Recommendation: say that the brief gives `--report-dir` as an absolute path and that the coordinator reads it from there; say the `.git/` and `.claude/` tests apply to the resolved path and that a nonexistent path is created or refused. Rationale: both are one-clause fixes to the sentence that already lists the values.
- Quality impact: Clarity about -0.5.

### R5 Approval flags carry no evidence of the person's answer
- Severity label: MAJOR. Graded: Medium. Expert: Cockburn, Wiegers. Priority: Medium.
- Issue: for approval gates the spec states the right principle ("an approval given by the agent that is being supervised is not an approval", SPEC:352) and assigns the answer to the person (SPEC:66, SPEC:92, SPEC:95). But `--confirmed-context <file>` and `--resume <contract>` are plain flags: the command cannot tell whether the person or the coordinator passed them (SPEC:92, SPEC:95). Only the coordinator's procedure, tested at AC-2.8 (SPEC:259), enforces it. For implement the spec does ask for the person's words verbatim in the ledger (SPEC:264).
- Grading check: a safety-boundary risk only if the coordinator ignores its own procedure; the text does not itself cause the unsafe outcome, so Medium.
- Recommendation: for the three approval flags, have the brief quote the person's answer and the command copy it into the contract (the pattern of SPEC:264). Rationale: it makes the approval auditable after the fact at no new mechanism.
- Quality impact: Consistency about -0.5.

### R6 Ready-today briefs omit gates the same rows name
- Severity label: MAJOR. Graded: Medium. Expert: Wiegers. Priority: Low-Medium.
- Issue: the troubleshoot row's "Brief must pass" is only "no `--fix`" (SPEC:120) while its own "Small fix" column records a STOP for `--depth deep` with a short input (SPEC:120, INV-B:239). Before P2 ships that STOP is a silent stall (SPEC:44). The same section tells the coordinator to use every flag section 3 lists as required (SPEC:76).
- Grading check: needs a coordinator who picks `--depth deep` with a short symptom; Medium.
- Recommendation: add "symptom of at least 10 words when `--depth deep`" to the troubleshoot brief column. Rationale: mirrors the tdd row (SPEC:119).
- Quality impact: Completeness about -0.5.

### R7 Several requirements have no behavioural acceptance check
- Severity label: MINOR-to-MAJOR. Graded: Medium. Expert: Crispin, Adzic. Priority: Low-Medium.
- Issue: WC-11 separation of edit-capable workers is exercised only for non-edit-capable workers (AC-1.6 (c), SPEC:247); the fan-in rule (SPEC:78-84) and the WC-12 `consumer_fenced` rule are checked only by a static assertion that Part B states them (AC-0.6, SPEC:241); the `partial` coordinator rule has no live scenario. The worked count (SPEC:84) is not a test.
- Grading check: a missing check on a stated rule, no wrong outcome by itself; Medium.
- Recommendation: add the SPEC:84 worked count as a coordinator dry-run scenario (4 producers, 1 blocked, expected 3 usable) to P2. Rationale: it is already written, only unused.
- Quality impact: Testability about -1.

### R8 Contract and gate edge behaviour left unspecified (table GAPs G3, G4, G6)
- Severity label: MAJOR (FR-8). Graded: Medium. Expert: Nygard, Crispin, Whittaker. Priority: Low-Medium.
- Issue: `partial` with an empty `incomplete_items` maps to `succeeded` in production (WC-5 says nothing; only the acceptance assertion rejects it, SPEC:66, SPEC:228); a `blocked` contract with an empty `blocked_question` is not rejected by step 4; a `succeeded` contract whose listed files are missing is not checked; a reply that arrives after the third `ask` timeout lands on a question the worker has abandoned (CAPS:60).
- Grading check: each needs a nonconforming command or a late coordinator, so Medium.
- Recommendation: one clause in WC-5: a `partial` with no items, a `blocked` with no question, or a `succeeded` whose `report_path` is missing counts as `failed`. Rationale: the status mapping then closes all three without a new rule.
- Quality impact: Consistency about -0.5.

### R9 `/sc:task` confidence override: the spec says no flag exists, the inventory shows one
- Severity label: MINOR. Graded: minor note. Expert: Cockburn.
- SPEC:97 says "task's confidence override has no flag and goes to the person". INV-B:199 quotes the prompt as "Override with `--compliance [tier]`", and INV-B:205 recommends defaulting to the higher tier. The behaviour (goes to the person) stands; the flag statement is wrong. Recommendation: name `--compliance` as the carrier of the person's answer.

### R10 WC-1 evidence overstates the recorded failure
- Severity label: MINOR. Graded: minor note. Expert: Nygard.
- SPEC:62 says "a fallback above about 45 s failed in the one run recorded". CAPS:49 records the failure as an unanswered question with no fallback at a 45 s limit, and the 45 s figure for a longer fallback as a prediction ("would make supervised workers fail again"). The 30 s requirement is unaffected. Recommendation: reword to "predicted, not observed".

### R11 The "nothing else is removed" checks cannot see removed bullet lines
- Severity label: MAJOR. Graded: Medium. Expert: Crispin. Priority: Medium.
- Issue: AC-C5 and AC-0.3 print removed lines with `grep -E '^-[^-]'` over `git diff -U0` (SPEC:218, SPEC:272) and require that nothing but the Usage or `argument-hint` line prints (SPEC:205, SPEC:238). A removed markdown list item `- text` appears in the diff as `-- text`, which that pattern does not match. Reproduced in the sandbox: `printf -- '-- a bullet\n' | grep -cE '^-[^-]'` prints `0`, while `grep -cE '^-'` prints `1`. A removed list item therefore passes SA-4 and SA-1 checks (SPEC:175, SPEC:178).
- Grading check: an implementer who follows the stated check deletes a bullet and passes; the criterion cannot detect the thing it guards. The spec states the intent (additive edits) correctly, so Medium.
- Recommendation: use `grep -E '^-' | grep -vE '^--- '` in both commands. Rationale: a one-token change that keeps the intent.
- Quality impact: Testability about -0.5.

## === ARCHITECTURE ANALYSIS ===

### A1 Nested-invocation rule depends on phase order the spec does not fix
- Severity label: MAJOR (Whittaker attack 2). Graded: Medium. Expert: Fowler, Whittaker. Priority: High-Medium.
- Issue: WC-2 (iv) lets a command pass `--unattended` to an invoked command only if that command's phase has shipped, exempts "a command that takes no flag, such as brainstorm", and otherwise "the step ... resolves as blocked" (SPEC:63). But brainstorm itself takes flags (SPEC:113), so the exemption cannot mean "no flags"; it can only mean "no `--unattended`". Workflow (P1) invokes reflect (P2) at Wave 4 (SPEC:121, SPEC:188-189, INV-B:271); tasklist (P2) invokes reflect and `sc:task` (P2, SPEC:151, INV-B:211); cli-eval create (P2) invokes spec-panel (P2, INV-A:44). AC-1.2 requires workflow to pass "all steps" under `--unattended` (SPEC:243), while step 3 and step 4 also accept a `blocked` result (SPEC:227-228), so the criterion would not notice.
- Grading check: an implementer who reads the exemption literally builds a P1 workflow that ends `blocked` on every happy path; one who reads it as "invoked as today" builds the intended behaviour. Two readings, so Medium.
- Recommendation: narrow the sentence: a nested command that is not yet shipped is invoked as today, without `--unattended`, when it has no gate under the caller's flags (reflect without `--remediate`); otherwise blocked. Rationale: that is already how the workflow and tasklist rows treat it (SPEC:121, SPEC:151).
- Quality impact: Consistency about -1.

### A2 The phase-shipped probe accepts either copy of the command
- Severity label: MAJOR. Graded: Medium. Expert: Newman, Fowler. Priority: Medium.
- Issue: the coordinator confirms the phase by grepping `~/.claude/commands/sc/<name>.md` or the project's `.claude/commands/sc/<name>.md`; "if neither copy has it" the ready-today form is used (SPEC:76). The project copies are sync-dev output, never committed (SPEC:179), so a fresh worker worktree has none and runs the installed copy.
- Grading check: an implementer builds a probe that passes on the coordinator's dev checkout (project copy new) while the worker's worktree runs a stale installed copy that ignores `--unattended` and can prompt; this needs a stale install, a guess about the environment, so Medium.
- Recommendation: probe the copy the worker will run (installed first, as the skills precedence goes), or require both to have it. Rationale: the failure it prevents is exactly the stall the contract exists to prevent.
- Quality impact: Consistency about -0.5.

### A3 `contract_version` handles older files only (table G11)
- Severity label: MINOR-to-MAJOR (FR-8). Graded: Medium. Expert: Newman. Priority: Low.
- Issue: fail-closed covers an unreadable file and a file whose version is lower than the command's (SPEC:55). A higher version, and a readable file with no version, are unspecified. Only version 1 exists today (SPEC:55), so no wrong outcome arises before a second version is written.
- Recommendation: state "any version other than the command's named version resolves every gate as blocked". Rationale: removes both holes in one clause.

### A4 The fan-in rule has a floor and no ceiling (table G7)
- Severity label: MAJOR (Whittaker attack 5). Graded: Medium. Expert: Hohpe, Fowler. Priority: Low-Medium.
- Issue: the brief names a minimum M (SPEC:81) and lists "only the usable reports" (SPEC:83). The consumer `/sc:adversarial` takes 2-10 (INV-A:35, SPEC:81). The spec's own example is four producers.
- Grading check: needs a coordinator that splits into more than ten producers; Medium.
- Recommendation: add "and at most the consumer's maximum; above it, aggregate in two stages". Rationale: the same sentence already states M.

### A5 WC-1 and WC-8 sit in neither part of the contract file
- Severity label: MINOR. Graded: minor note. Expert: Fowler.
- SPEC:55 assigns WC-2, 4, 5, 6, 9, 11 to Part A and WC-3, 5, 7, 10, 12 to Part B. WC-1 (launch setup) and WC-8 (no Orca fan-out) are in neither (SPEC:62, SPEC:69). AC-0.6 does not test them (SPEC:241). WC-8 is covered by AC-C1 (SPEC:201); WC-1 by step 1 of SPEC:225.

### A6 Section 4 states an absolute that later text contradicts
- Severity label: MINOR. Graded: minor note. Expert: Fowler.
- SPEC:162 says "workers make no commits or pushes". WC-11 lists pr-submit (one fix commit per cycle) and post-release with `--authorize commit` as workers that commit (SPEC:72), and D4 (a) lets a brief authorize outward actions (SPEC:311). Recommendation: "workers make no commits or pushes unless the brief authorizes them (D4)".

## Synthesis

### Consensus points
- The decision (Orca coordinates, commands stay units of work) is supported by the cited evidence, and the spec states where that evidence is thin (SPEC:41-45, SPEC:360-379).
- The contract is consistent on the main path: the status set, the outcome mapping, the first-write `running` marker and the fail-closed rule agree across SPEC:55, SPEC:65-66, SPEC:228 and SPEC:249-250.
- Counts and phase assignment reconcile (see Coverage).

### Disagreements
- Fowler and Newman want the nested-invocation rule and the phase probe made order-independent (A1, A2); Wiegers would rather fix the answered-retry path first (R1), because every `blocked` gate uses it. Ranked order below puts R1 first.

### Priority-ranked improvements
1. R1 answered-gate carrier; 2. R2 production stall watch; 3. A1 nested-invocation rule; 4. R3 status words before P0; 5. R4 report-dir semantics; 6. A2 phase probe; 7. R11 diff-check pattern; 8. R5 approval evidence; 9. R6, R7, R8, A3, A4 (low).

### Quality metrics (0-10)
Clarity 7, Completeness 7, Testability 7, Consistency 7. Basis: the per-finding impacts above against a spec whose citations, counts and worked examples are otherwise internally consistent.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: R1, R2, R3, R4, R5, R6, R7, R8, R11, A1, A2, A3, A4. Minor: R9, R10, A5, A6. No issue was opened and the user was not asked (see Coverage).

## Reviser brief

No blocking finding is open, so no finding id is listed and no revision is requested. Contract for any later reviser (`CMD:263`): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; cite the finding id on every added paragraph or table; prefer deleting or narrowing; report byte size before and after and bytes added and deleted per finding id. Medium and minor findings above are not to be edited under this brief.

verdict: PASS
