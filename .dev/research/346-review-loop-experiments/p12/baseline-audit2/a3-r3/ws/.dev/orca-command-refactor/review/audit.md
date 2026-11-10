review: 1 of 3

# Spec-panel audit: Orca worker-contract spec (whole-document first review)

## Header

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (labelled whole-document audit, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`) |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` |
| Candidate sha256 | `0af4c9147b1078d164edae3da1719df0954c532ee06138e07f894bc91e1ab096` |
| Baseline | none (first review; no `--re-review`, no `--baseline`) |
| Reviewer model actually used | claude-sonnet-5-5 |
| Format | standard (default); critique buckets plus the YAML summary near the end |
| Panel (review order) | Wiegers (lead), Adzic, Cockburn, Fowler (lead), Nygard, Whittaker (always active), Newman, Hohpe |
| Not selected | Crispin, Gregory, Hightower (no `testing` or `compliance` focus asked; testability points are attributed to Wiegers and Adzic) |

Citation keys: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `COMMAND:N` = `command.md` (the /sc:spec-panel definition in the sandbox). `RLP:N` = `~/.claude/rules/prompts/document_review_loop_prompts.md`.

Brief clauses overridden: none. The brief asks for the FIRST-REVIEW prompt, `path:line` for every claim, UNVERIFIED for unchecked citations, and a `DONE <path>` reply only. The command asks the session to ask the user once whether to open an issue for the follow-up candidates (`COMMAND:260`); the brief restricts the reply to `DONE <path>`, so the list is only recorded below and nothing was asked or created.

## Coverage

Whole document, every section (1 to 9, Decisions, UNVERIFIED), read in full. Checked against: the three inventories (every `INV-A`, `INV-B`, `CAPS` citation in sections 1 to 4 that I traced landed on the content the spec claims; no wrong line found), the phase table against the section 3 rows (counts: 43 = 10 + 27 + 6; the 27 = P1 9 + P2 11 + P3 4 + P4 3, conserved), and the acceptance checks against the requirements. One acceptance-check command was run (`diff -U0 | grep -E '^-[^-]'`, see M1). Not checked, because the sandbox holds no repository: every citation to `src/`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `EVIDENCE.md`, the codegraph README and Orca's installed JS. Those are marked UNVERIFIED where they carry weight, and listed at the end.

Grading follows the command: CRITICAL is blocking; MAJOR or FR-8/FR-9 is blocking only when the FIRST-REVIEW sentence ("An implementer who follows the stated text as written builds X, and X is wrong because Y", `RLP:31`) holds with no further assumption; otherwise Medium. Two findings are blocking. Everything else is Medium or minor and sits under follow-up candidates.

---

## === REQUIREMENTS ANALYSIS ===

### B1 [MAJOR, blocking] `--unattended` is promised to mean "no person, no outward default" but the phase plan ships it before the gates exist

- **Grading sentence.** An implementer who follows the stated text builds Phase 1 as written (`SPEC:159`, `SPEC:195`): `--unattended` and a `## Unattended mode` section on every command of sections 3.1 and 3.2 except `/sc:load`. Phases 2 to 4 convert the gates later (`SPEC:160-162`). The result after Phase 1 is a command such as `/sc:auggie-review` that accepts `--unattended`, still posts to GitHub by default and still offers remediation and waits (`INV-A:38`, `SPEC:100` marks that change P2). That is wrong because WC-2 says "under `--unattended` the command never calls AskUserQuestion, never ends its turn on a chat question" (`SPEC:60`) and WC-9 says "under `--unattended`, any default that pushes, opens a PR, posts to GitHub ... is off" (`SPEC:67`). The text also calls each phase "independently useful" (`SPEC:154`), and the contract file that states WC-2 and WC-9 for every command lands in P0 (`SPEC:158`), so a coordinator that trusts the flag can dispatch `--unattended` at P1 and trigger an outward post or a stall.
- **Second contradiction in the same place.** AC-1.1 asserts that every command in 3.1 and 3.2 except load has the section (`SPEC:195`), which includes `/sc:pr-submit`. D3(a), the recommendation, says "no pr-submit changes in Phase 4" and section 4 says pr-submit is a worker candidate "only if the user accepts D3" (`SPEC:240`, `SPEC:139`). So AC-1.1 forces a pr-submit change that D3(a) rules out; the same holds for `/sc:implement` and `/sc:post-release`, whose unattended behaviour waits on D2 and D4 (`SPEC:154`, `SPEC:109`, `SPEC:113`) while the P1 test already requires their sections. Section 2.1 says each section "lists only its own gate resolutions" (`SPEC:52`), which for those commands do not exist at P1.
- **Expert.** Wiegers (consistency of requirements), Fowler (phase boundary and interface), Whittaker (sequence attack, see W1).
- **Recommendation.** Narrow, do not add: attach the flag and section to a command in the phase named in its own row (P1 only for the no-gate commands and the four ready-command fixes), and restrict AC-1.1 to the commands whose phase has landed. Say that pr-submit, implement and post-release get no section until their decision (D3, D2, D4) is made. Rationale: the flag then never claims a guarantee its command cannot yet keep.
- **Priority.** High. **Quality impact.** Consistency +2, safety of the worker boundary.

### B2 [MAJOR, blocking] WC-4's single contract location and the "known before dispatch" claim contradict the section 3 rows and the acceptance checks

- **Grading sentence.** An implementer who follows WC-4 writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)", and the coordinator opens that path (`SPEC:62`, `SPEC:73`). But the rows say otherwise: `/sc:tdd` and `/sc:init-lite` take `--output <file>` (`SPEC:87`, `SPEC:90`), so `<file>/return-contract.yaml` cannot exist; `/sc:adversarial` is fixed to `<output>/adversarial/return-contract.yaml` (`SPEC:83`); `/sc:workflow` keeps `.dev/tasks/to-do/<id>/return-contract.yaml` (`SPEC:92`), where `<id>` is generated at run time and no directory is passed, so the path is not "known before dispatch" and a pre-creation STOP has no package directory to hold it. It is wrong because AC 7.2 steps 3 and 4 require the `worker_done` report path to be "the WC-4 contract path" and `test -s <contract>` to pass for each command (`SPEC:182-183`), which cannot hold for these four commands under the stated rule; AC-1.2 and AC-2.2 reuse the same steps (`SPEC:196`, `SPEC:200`). The "Brief must pass" cells for reflect, troubleshoot and workflow also name no output flag (`SPEC:88`, `SPEC:91`, `SPEC:92`), and whether `/sc:troubleshoot` and `/sc:workflow` have an output flag at all is not shown (`INV-B:242`, `INV-B:272`).
- **Corroboration that this is a real shape problem.** The /sc:spec-panel definition in the sandbox itself has to use `--report-dir` because "`--output` is file-valued" (`COMMAND:460`) and puts `return-contract.yaml` in that directory (`COMMAND:461`). That file is not repository evidence for the spec, only a sign that the file-valued `--output` case occurs.
- **Expert.** Fowler (interface consistency), Cockburn (the coordinator, as primary actor, must locate the report), Adzic (the example in AC step 3 has no commands for which it holds), Hohpe (the message carries a `--report-path` that the rule cannot compute).
- **Recommendation.** Make WC-4 state one lookup rule that the rows can obey, for example a "contract path" value per command in the section 3 tables that the brief copies, and let 7.2 steps 3 and 4 read that value from the brief. Where the path cannot be known before dispatch (workflow), either require the brief to pass a directory or drop "known before dispatch" for that row. Delete the generic claim rather than add a mechanism.
- **Priority.** High. **Quality impact.** Testability +2, Completeness +1.

---

## Requirements findings that are Medium (follow-up candidates; none blocks)

Each: issue, severity as labelled, expert, recommendation, priority, quality impact. All are graded Medium because the FIRST-REVIEW sentence needs a guess about which reading an implementer picks, or the finding is a requirement the document never states.

- **M1 [MAJOR label, Medium] The additive-edit check cannot see removed bullet lines.** AC-C5 and AC-0.3 use `git diff -U0 ... | grep -E '^-[^-]'` (`SPEC:176`, `SPEC:193`). A removed Markdown line `- foo` appears in a diff as `-- foo`, which `^-[^-]` rejects. I ran it: removing two `- bullet` lines printed nothing (exit 1); removing a plain line printed `-plain old line`. Command files are mostly bullets, so SA-4's "edits are additive" (`SPEC:149`) and SA-1's standalone guarantee (`SPEC:146`) have no working mechanical check for them; the routing-table check in AC-0.3 still works because table rows start with `|`. Expert: Wiegers/Adzic (testability). Fix: `grep -E '^-' | grep -vE '^---'`. Priority Medium. Quality impact: Testability +1.
- **M2 [MAJOR label, Medium] The blocked and ask path is under-specified.** WC-2(c) says a gated command writes `status: blocked` and stops (`SPEC:60`); WC-3 says a session "may instead ask the coordinator once" (`SPEC:61`). The spec never says which is the default when a preamble exists, so AC-2.2's expected `worker_done --outcome failed` with `status: blocked` (`SPEC:200`) is only reached if the worker picks the first reading. Neither section says what the coordinator does after a `failed`/`blocked` report (re-dispatch with `--retry-of` and the answer as a flag? new Task?), although section 2.3 lists only "open the report, then release or reuse" (`SPEC:73`). WC-3 has no bound on how long a worker stays in `ask`: "resumes the same message ID" after every timeout (`SPEC:61`), while Orca calls a waiting worker "healthy, not failed" (`CAPS:52`, `CAPS:129`) and total run time is UNVERIFIED (`SPEC:282`, `CAPS:188`). A coordinator that has gone away leaves a worker parked forever with no failure signal. Experts: Cockburn (what the coordinator does with a blocked report), Hohpe (message lifecycle), Nygard (unbounded wait). Fix: name the default (blocked unless the brief says `ask`), add one line on the coordinator's next step, and cap the resume count or total wait. Priority High within Medium. Quality impact: Completeness +1.
- **M3 [MAJOR label, Medium] Outcome mapping and the contract vocabulary have holes.** WC-5 maps `failed`, `blocked` or "no report exists" to `--outcome failed` and "succeeded otherwise" (`SPEC:63`). A report that exists but is empty, unparsable, or has a status outside the four values falls into "otherwise" and is reported as success. The same section says commands that already write a contract "keep their fields" (`SPEC:62`) while 7.2 step 4 asserts `status` is one of `succeeded|partial|failed|blocked` for all of them (`SPEC:183`, `SPEC:262`); the existing vocabularies of workflow, brainstorm, reflect and adversarial are never cited (only field names, `INV-B:272`), so the two statements may conflict. WC-4's "at least" field list has no version or schema field, while workflow's contract is versioned 1.1 (`INV-B:272`), so a reader cannot tell which shape it holds. Experts: Wiegers, Newman (contract evolution), Nygard. Fix: "otherwise" becomes "report exists and its status is succeeded or partial"; cite the existing statuses before claiming a fixed set. Priority Medium. Quality impact: Consistency +1.
- **M4 [MAJOR label, Medium] How a command detects `--unattended` is not defined.** D1(a) selects a flag and says it "cannot misfire on a person" (`SPEC:228`), but the spec gives no parsing rule. Most commands take free text (`/sc:tdd "..."`, `/sc:troubleshoot "..."`, `SPEC:228`, `SPEC:90`); a prompt that merely mentions `--unattended` (for example "add --unattended support to X") could switch a standalone run into unattended mode and break SA-1 (`SPEC:146`). The sandbox command definition does contain such a rule ("standalone argument token outside any quoted argument", `COMMAND:459`), which shows the case is real; the spec does not require it. Expert: Whittaker (sentinel collision), Wiegers. Fix: one sentence in WC-2 or 2.1: the flag counts only as a standalone token outside quoted content. Priority Medium. Quality impact: Correctness.
- **M5 [MAJOR label, Medium] "Fresh dir" is the whole WC-6 answer for about 25 commands, and nobody owns it.** WC-6 says a command "writes each run into a fresh output directory" (`SPEC:64`), while WC-4 says the output directory is the one the coordinator passed (`SPEC:62`). A command cannot make a fresh directory out of a directory that the coordinator fixed before dispatch, and section 2.3 does not tell the coordinator to pass a new directory per retry (`SPEC:73`). With a repeated directory the retry overwrites the first attempt's contract and reports, which is the corruption WC-6 forbids. A superseded worker that later finds `consumer_fenced` (WC-12, `SPEC:70`) may also leave a contract in the same directory. Experts: Nygard, Cockburn. Fix: add "a retry brief passes a new output directory" to 2.3 and delete the sentence that gives the command the job. Priority Medium. Quality impact: Completeness +1.
- **M6 [MAJOR label, Medium] Four requirements have no acceptance check, and WC-1 has no number.** I found no check for WC-3 (ask path), WC-6 (retry safety), WC-12 (check and `consumer_fenced`) and no phase deliverable for WC-1 (`SPEC:59`; section 6 `SPEC:158-162` and section 7 never mention it; the one launcher that caused the evidence, `sk/ccsession-tag`, is named only as the sole Orca-aware primitive, `SPEC:25`). WC-1 says a startup prompt must fall back "well inside" the limit with no figure; the evidence in the spec shows 30 s passes and a value above about 45 s failed, but at a 45 s test limit (`SPEC:59`, `CAPS:49`). Experts: Wiegers, Adzic. Fix: one check each, or mark them as not tested. Priority Medium.
- **M7 [MAJOR label, Medium] WC-9 uses an undefined term and the rows do not apply it.** "Calls a paid external run" (`SPEC:67`) is not defined. `/sc:research` and `/sc:review-translation` call web search (`INV-B:134`, `INV-B:144`), `/sc:cli-eval run` executes real eval runs with "safety flags" the row leaves unnamed (`SPEC:104`, `INV-A:44`); none of those rows says what is off under `--unattended`. Separately, D4 lists auggie-review `--post-pr` and task `commit`/`push` as depending on the user's decision (`SPEC:244`), both P2 rows (`SPEC:100`, `SPEC:121`), while section 6 says "Phases 1-3 need no user decision" (`SPEC:154`) and section 9 says Phases 0-3 may proceed on the recommendations (`SPEC:225`). The two statements differ. Experts: Wiegers, Nygard. Fix: list the external-call commands in WC-9 or drop the term; make section 6 say "on the recommendations". Priority Medium.
- **M8 [MAJOR label, Medium] The shared rules live in a file the command may not be able to read.** Section 2.1 puts WC-2 and WC-9 in `~/.claude/WORKER-CONTRACT.md` and has each command "point to" it (`SPEC:52`). A partial install, a plugin install (the `plugins/superclaude/` mirror, UNVERIFIED `SPEC:279`; the spec adds the new core file only to `KNOWN_CORE_FILES`, `SPEC:158`) or an older install leaves the command without WC-9, the rule that turns outward defaults off. No fail-closed behaviour is stated. Expert: Nygard (failure mode), Newman (compatibility). Fix: one line: if the contract file is unreadable the command refuses with `status: failed`. Priority Medium.
- **M9 [MINOR label, Medium] How the worker actually runs a `/sc:` command is not stated.** The decision rests on "a command run by a worker has the same tools as a command a person runs" (E2, `SPEC:22`). The cited evidence shows only that a worker reached `input_accepted` and answered (`CAPS:49`), not that a slash command in the brief is expanded; the preamble comes first, and the PR #329 route used an Agent-tool subagent (`SPEC:43`). WC-7 says "runs the command directly" (`SPEC:65`) with no mechanism, and AC-0.4 checks only that no Agent-tool wrapper appears (`SPEC:194`). The gap is acknowledged for the end-to-end result (`SPEC:43`, `SPEC:272`) but not for the invocation step. Expert: Cockburn, Fowler. Priority Medium.
- **M10 [MINOR label, Medium] Several acceptance checks can pass while the thing they guard fails.** AC-2.4 counts reviews and comments with `gh api ... --jq length` (`SPEC:202`), which reads only the first page (30 items by default), so a new post on a PR with 30 or more existing items leaves the count unchanged. AC-4.2 says `git log -1 unchanged` and "no new PR" without recording a before value (`SPEC:209`). Step 5 searches a transcript for the string `AskUserQuestion` (`SPEC:184`), which also appears in loaded command text (for example "never AskUserQuestion", `INV-B:239`); "no call" needs a tool-call filter. AC-C1 shows `\|` inside a command (`SPEC:172`), which is only correct once Markdown renders it. Expert: Adzic, Wiegers. Priority Low.

## === ARCHITECTURE ANALYSIS ===

Architecture findings other than B2 (which is both):

- **M11 [MAJOR label, Medium] AC-C1 and the P0 deliverables can contradict each other.** AC-C1 fails a phase if `orca orchestration|worktree|terminal|agent` appears anywhere in `src/superclaude/core` or the other primitive folders (`SPEC:172`). P0 adds an Orca section to `src/superclaude/core/HOW-WE-WORK.md` and a coordinator brief template to `src/superclaude/core/WORKER-CONTRACT.md` (`SPEC:158`), and SA-2 permits an Orca mention "inside the contract file" (`SPEC:147`). Any command text in those two files (the natural content of a coordinator section) makes AC-C1 print a line. The spec does not say which wins. Expert: Fowler (boundary of the "no Orca in primitives" rule). Fix: exclude the two files from the grep or say they carry no command text. Priority Medium.
- **M12 [MAJOR label, Medium] The tasklist row claims more than the evidence supports.** It says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit" (`SPEC:122`), citing only `INV-A:14`, which describes the limit but does not count layers. The chain in the inventories is worker, then N Stage 10.5 subagents each running `/sc:reflect`, then its agents, then (Tier 2) `sc:adversarial-protocol` advocates (`INV-B:210-211`, `INV-B:111`); the inventory itself leaves nested spawning UNVERIFIED (`INV-B:210`, `INV-B:314`, `INV-B:322`). The claim is not in the spec's UNVERIFIED list (`SPEC:271-285`). The row also resolves only the remediation offer; `needs_human_decision` items that "HALT" (`INV-B:209`) are not covered by the "headless rule applies" sentence, and a headless auto-accept means reflect starts a remediation handoff per phase without a person, a side effect WC-9 does not mention (`SPEC:67`). Expert: Fowler, Newman. Priority Medium.
- **M13 [MINOR label, Medium] WC-11 says "must never" and the rows accept collisions.** `cleanup-audit` writes a fixed `.claude-audit/` directory and the row only says one audit per worktree at a time (`SPEC:85`, `SPEC:69`); `index-repo` writes a fixed `PROJECT_INDEX.md` (`INV-A:53`, `SPEC:86`) with no such note; `init-lite` defaults to a fixed report file (`SPEC:87`). The rows rely on the coordinator not running two at once, which section 2.3 does not ask for. Expert: Nygard. Priority Low.
- **M14 [MINOR label, Medium] Two edges of the flag surface are not defined.** (a) What a coordinator-only command (section 4) does if given `--unattended`: "get no `--unattended` mode" (`SPEC:128`) is silent on refuse versus ignore. (b) `/sc:pr-submit` is specified only for `--monitor 1` (refused) and the default `--monitor 3` (`SPEC:114`, `INV-B:89`); the behaviour of `--monitor 0` and `2` is not covered, and the spec's own text about ordinals is not in the inventories. Priority Low.

- **M15 [MINOR label, Medium] The wait-split trigger and its acceptance check use different thresholds.** WC-10 splits only a step that blocks one call "for longer than 5 minutes" into waits of at most 4 minutes (`SPEC:68`); the pr-submit row and AC-4.3 require each wait to stay under 4 minutes (240 s) (`SPEC:114`, `SPEC:210`); the Decisions table gives 4 minutes as a margin under the 5-minute cadence (`SPEC:266`). A single call of 270 s needs no split under WC-10 and fails AC-4.3, and a call of exactly 300 s is neither "longer than" 5 minutes nor inside the margin. Only pr-submit under D3(b) is tested, so the wrong outcome is limited. Expert: Nygard, Wiegers. Fix: state the trigger as "longer than 4 minutes". Priority Low.

### Minor notes (never blocking)

- N1. Contract `status: blocked` and `failed` reuse words that Orca uses for Task states with other meanings (`CAPS:89`); WC-5 maps them explicitly (`SPEC:63`), so this is only a reading hazard.
- N2. `partial` maps to `--outcome succeeded` (`SPEC:63`, `SPEC:263`), which leaves the Task `completed` and its dependents ready (`CAPS:90`); section 2.3 has the coordinator open the report first (`SPEC:73`), so this works only if the coordinator does.
- N3. D5 says raising depth "would ... break R1's protection against runaway fan-out" (`SPEC:252`); R1 is a reason for the rejection (`SPEC:33`), not a protection.
- N4. `explain` gains a Write tool and `business-panel` has its frontmatter moved (`SPEC:108`, `SPEC:102`); these change standalone behaviour or loading, which SA-1 (`SPEC:146`) does not expressly allow (SA-4 names both, `SPEC:149`).
- N5. AC-1.3 uses "a scratch worktree" (`SPEC:197`); the repository's own worktree rule (`CLAUDE.md`, not in the sandbox, UNVERIFIED) requires Orca-created worktrees with an agent.
- N6. Heartbeat cadence of 5 minutes comes from one worker's preamble, not from a guide (`CAPS:130`); the spec treats it as general (`SPEC:68`) and does not list that in its UNVERIFIED section.

---

## Adversarial analysis (Whittaker)

- **W1.** I can break this specification by **Sequence Attack**. The invariant at **WC-2 and WC-9 (`SPEC:60`, `SPEC:67`)** fails when **Phase 1 has shipped and Phases 2 to 4 have not**. Concrete attack: **before** state: contract file installed, `/sc:auggie-review` has no `--unattended` handling. P1 lands: the flag is accepted (`SPEC:159`), the `## Unattended mode` section exists (`SPEC:195`). A coordinator dispatches `/sc:auggie-review <PR> --unattended`; the command still posts to the PR (`INV-A:38`) and then ends its turn on the remediation offer. **After** state: a posted review and a worker with no `worker_done`. Severity **MAJOR** (this is B1).
- **W2.** I can break this specification by **Divergence Attack**. The invariant at **WC-4 (`SPEC:62`)** fails when **`--output` is file-valued or generated**. Concrete attack: coordinator brief `/sc:tdd "<component>" --unattended --output docs/x/TDD_X.md`; the worker writes the contract to `docs/x/TDD_X.md/return-contract.yaml` (fails, a file is there) or to some directory it chooses; the coordinator opens a path that does not exist and AC step 4 fails. Severity **MAJOR** (this is B2).
- **W3.** I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **the contract exists but is empty or has an unknown status**. Concrete attack: the command is cut off after creating `return-contract.yaml` with zero bytes; the worker's rule "no report exists" is false and "succeeded otherwise" applies; Orca records `succeeded` and unblocks dependents (`CAPS:90`). Severity **MAJOR** under the command's label; Medium by the grading check (M3).
- **W4.** I can break this specification by **Sentinel Collision Attack**. The invariant at **D1(a) (`SPEC:228`)** fails when **user text contains the sentinel `--unattended`**. Concrete attack: a person runs `/sc:tdd "add --unattended support to the importer"`; if the command matches the string anywhere, standalone mode flips, prompts vanish and a contract file appears in the working tree, against SA-1 and SA-3 (`SPEC:146`, `SPEC:148`). Severity **MAJOR** (M4).
- **W5.** I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (`SPEC:61`)** fails when **resumes of `ask` accumulate with no answer**. Concrete attack: the coordinator session ends; the worker resumes the same message ID after each timeout; `worker-show` reports a healthy waiting worker (`CAPS:129`); after N timeouts nothing has failed and nothing has finished. Severity **MAJOR** under the label (M2).
- **W6.** I can break this specification by **Sequence Attack**. The invariant at **WC-6 and WC-12 (`SPEC:64`, `SPEC:70`)** fails when **a fenced worker and its replacement share one output directory**. Concrete attack: attempt 1 is fenced after writing `return-contract.yaml` with `status: succeeded`; the retry is briefed with the same `--output`; if the retry stops before its own write, the coordinator reads the first attempt's contract. Severity **MAJOR** under the label (M5).

---

## Guard Condition Boundary Table

Guards identified: the wait-split trigger, the outcome mapping, the `blocked` question, the unattended switch, the confidence gate, retry output, `ask` timeout, readiness, depth, the additive-edit grep, `--monitor`. Classes left out are named per row group. FR-8: each GAP is graded by consequence (B1 is blocking, the rest Medium). FR-9: no blank cell remains. FR-10: the table is complete before the synthesis sections.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| Wait split (`blocks one call > 5 min`) | WC-10 `SPEC:68` | Zero/Empty | wait = 0 s | false | no split; heartbeat on the normal cadence | OK |
| Wait split | WC-10 `SPEC:68` | Typical | wait = 120 s | false | no split | OK |
| Wait split | WC-10 `SPEC:68` | Maximum/Overflow | cli-eval 3600 s (`SPEC:104`) | true | split into waits of at most 4 minutes | OK |
| Wait split | WC-10 vs AC-4.3 `SPEC:68`, `SPEC:210` | Legitimate Edge Case | wait = 270 s (between 240 and 300) | false by WC-10 (not longer than 5 min); true by AC-4.3 (240 s) and the pr-submit row (`SPEC:114`) | WC-10 requires no split; the acceptance check fails the same call | GAP (M15) |
| Wait split | WC-10 `SPEC:68` | Legitimate Edge Case | wait = exactly 300 s | false ("longer than 5 minutes") | cadence "every 5 minutes" leaves no margin; not stated | GAP (M15) |
| Outcome mapping | WC-5 `SPEC:63` | Zero/Empty | contract file of 0 bytes, or no `status` key | "no report exists" false | "succeeded otherwise" | GAP (M3) |
| Outcome mapping | WC-5 `SPEC:63` | One/Minimal | `status: succeeded` | succeeded branch | `--outcome succeeded` | OK |
| Outcome mapping | WC-5 `SPEC:63` | Typical | `status: failed`; `status: blocked` | failed branch | `--outcome failed` (AC-2.2, `SPEC:200`) | OK |
| Outcome mapping | WC-5 `SPEC:63` | Sentinel Value Match | `status: partial`; status outside the four values | partial: succeeded branch; unknown: falls to "otherwise" | partial documented (`SPEC:263`); unknown value undefined | GAP (M3) |
| Outcome mapping | WC-5 `SPEC:63` | Legitimate Edge Case | audit with verdict FAIL | succeeded branch | `--outcome succeeded`, verdict in first sentence | OK |
| `blocked_question` | WC-4 `SPEC:62` | Zero/Empty | `""` with `status: blocked` | requirement false | AC-2.2 demands non-empty (`SPEC:200`) | OK |
| `--unattended` switch | D1(a) `SPEC:228` | Zero/Empty | flag absent | false | today's behaviour (SA-1, `SPEC:146`) | OK |
| `--unattended` switch | D1(a) `SPEC:228` | Typical | standalone token | true | unattended mode | OK |
| `--unattended` switch | D1(a) `SPEC:228` | Sentinel Value Match | token inside quoted user text | undefined | not specified | GAP (M4) |
| `--unattended` switch | section 4 `SPEC:128` | Legitimate Edge Case | flag passed to a coordinator-only command | undefined | "get no `--unattended` mode"; refuse or ignore not stated | GAP (M14) |
| `--unattended` switch | P1 `SPEC:159`, WC-2/WC-9 `SPEC:60`, `SPEC:67` | Legitimate Edge Case | command whose gate lands in P2 to P4, flag accepted at P1 | true | accepts flag, keeps today's prompts and outward defaults | GAP (B1, blocking) |
| Confidence gate | task row `SPEC:121` | Zero/Empty | confidence = 0.0 | true (below 0.70) | blocked | OK |
| Confidence gate | task row `SPEC:121` | Legitimate Edge Case | confidence = 0.70 | false | proceeds (strictly "below 0.70") | OK |
| Confidence gate | task row `SPEC:121` | Zero/Empty | no confidence value produced (null) | undefined | not specified | GAP (follow-up, no wrong outcome named) |
| Retry output | WC-6 `SPEC:64` | One/Minimal | first attempt, no prior output | not a retry | normal run | OK |
| Retry output | WC-6 `SPEC:64`, WC-4 `SPEC:62` | Legitimate Edge Case | retry brief reuses the same `--output` | "fresh dir" cannot apply | overwrites first attempt's files | GAP (M5) |
| `ask` wait | WC-3 `SPEC:61` | Zero/Empty | `--timeout-ms` omitted | default unknown | relies on resume by ID; default UNVERIFIED (`SPEC:281`) | OK (acknowledged as UNVERIFIED) |
| `ask` wait | WC-3 `SPEC:61` | Maximum/Overflow | N consecutive timeouts, no answer | no stop condition | resumes without limit | GAP (M2) |
| Readiness | WC-1 `SPEC:59` | Typical | startup prompt with 30 s fallback | within limit | passes (`CAPS:49`) | OK |
| Readiness | WC-1 `SPEC:59` | Legitimate Edge Case | fallback between 45 s and 60 s | "well inside" has no number | not specified | GAP (M6) |
| Depth | WC-8 `SPEC:66`, R1 `SPEC:33` | Typical | worker at depth 1 calls `worker-start` | true (refused) | `nested_worker_depth_exceeded` | OK |
| Depth | WC-8 `SPEC:66`, D5 `SPEC:249-253` | Legitimate Edge Case | user raises depth to 2 | false | WC-8 still forbids the call | OK |
| Additive grep | AC-C5 `SPEC:176` | Typical | removed plain line | matches | prints the line | OK |
| Additive grep | AC-C5 `SPEC:176` | Legitimate Edge Case | removed Markdown bullet `- foo` (diff shows `-- foo`) | no match | prints nothing (reproduced) | GAP (M1) |
| `--monitor` | pr-submit row `SPEC:114` | Typical | `--monitor 1` | true | refused under `--unattended` | OK |
| `--monitor` | pr-submit row `SPEC:114` | Legitimate Edge Case | `--monitor 0` or `2` | undefined | not specified | GAP (M14) |

Classes not applicable and left out: "One/Minimal" and "Maximum" for the `blocked_question`, `--unattended`, confidence, retry, readiness, depth, grep and `--monitor` guards (they are boolean or ordinal, so zero, typical and edge cover them); "Sentinel Value Match" for the wait split, confidence, retry, `ask`, readiness, depth and grep guards (no reserved value is compared).

Downstream propagation: the GAP rows marked B1, B2-related (M5), M2, M3 and M4 are the priority targets for `sc:adversarial` AD-1 (`COMMAND:342`).

## Pipeline Dimensional Analysis

Not triggered as a data pipeline (no stage filters, aggregates or fans out records, `COMMAND:353`). One count flow was conserved by hand: 21 + 22 = 43 commands (`INV-A:3`, `INV-B:3`, `SPEC:76`) become 10 + 27 + 6 = 43; the 27 split P1 9, P2 11, P3 4, P4 3 (`SPEC:99-125`, `SPEC:159-162`); the 10 ready commands split P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow), P2 gate changes 4 (reflect, release-split, tdd, troubleshoot), and 2 with no phase row of their own (brainstorm, init-lite; they receive only the P1 flag and section). No mismatch.

## Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  sha256: 0af4c9147b1078d164edae3da1719df0954c532ee06138e07f894bc91e1ab096
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.5
  clarity: 7
  completeness: 7
  testability: 6
  consistency: 5
critical_issues:
  - {category: requirements, severity: MAJOR, expert: wiegers, issue: "B1 --unattended shipped before gates (SPEC:159,195 vs SPEC:60,67)", recommendation: "attach flag and section per command in its own phase; scope AC-1.1"}
  - {category: architecture, severity: MAJOR, expert: fowler, issue: "B2 WC-4 contract location vs rows and AC 7.2 steps 3-4 (SPEC:62,83,87,90,92,182-183)", recommendation: "one lookup rule or per-command contract path value"}
expert_consensus:
  - "The decision (Orca on top, commands as workers) is well supported and the gaps in section 1.4 are stated honestly."
  - "The inventory-to-spec traceability is strong; counts and traced citations hold."
  - "The contract's mechanics (location, outcome mapping, retry, blocked path) are the weak part."
improvement_roadmap:
  immediate: [B1, B2]
  short_term: [M1, M2, M3, M4, M5, M7, M8, M11]
  long_term: [M6, M9, M10, M12, M13, M14, M15]
adversarial_analysis:
  - {attack: sequence, severity: MAJOR, location: "WC-2/WC-9", ref: W1}
  - {attack: divergence, severity: MAJOR, location: "WC-4", ref: W2}
  - {attack: zero_empty, severity: MAJOR, location: "WC-5", ref: W3}
  - {attack: sentinel_collision, severity: MAJOR, location: "D1(a)", ref: W4}
  - {attack: accumulation, severity: MAJOR, location: "WC-3", ref: W5}
  - {attack: sequence, severity: MAJOR, location: "WC-6/WC-12", ref: W6}
```

## Follow-up candidates (Medium and minor; recorded only; none triggers a revision)

Medium: M1 to M15, plus the GAP row marked "follow-up" in the Guard Condition Boundary Table (null confidence). Minor notes: N1 to N6. Not asked of the user (see Header).

## UNVERIFIED citations (no repository in the sandbox)

Unchecked: `src/superclaude/cli/install_core.py:4,13-24,33` and `CLAUDE.md` lines cited at `SPEC:52`, `SPEC:34`, `SPEC:150`, `SPEC:264`, `SPEC:279`; `Makefile:68-74`; `pyproject.toml:38`; `HOW-WE-WORK.md:171,249,254`; the grep outputs of E5 (`SPEC:25`); `EVIDENCE.md:35,39,45,56`; `.dev/codegraph-migration/orchestration/README.md:31,33,42` and the return contract at `...P3-command-set/adversarial/return-contract.yaml:10` (these are only seen through `CAPS:49`, `CAPS:156` and `INV-A:35`); every `cmd/` and `sk/` line cited directly in section 3 (checked only as far as the inventory row quotes them); the claim that `/sc:pr-submit`'s 600 s is a cumulative budget over poll-then-sleep iterations (`SPEC:68`, `SPEC:114`, contrasted with `INV-B:95`, `INV-B:299`); the spec's own re-read and 340-citation check (`SPEC:11`, `SPEC:285`).

## Reviser brief

Blocking finding ids: **B1, B2**. This brief restates the command's reviser contract (`COMMAND:263`); the reviser reads this report, not the command.

- Revise only text a blocking finding names (B1: `SPEC:52`, `SPEC:79`, `SPEC:159`, `SPEC:195`, and the D3 and section 4 lines that conflict with them, `SPEC:139`, `SPEC:240`; B2: `SPEC:62`, `SPEC:73`, `SPEC:182-183`, and the rows at `SPEC:83`, `SPEC:87`, `SPEC:90`, `SPEC:92`).
- Add no rule, mechanism or section that a blocking finding does not call for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding. Leave every Medium and minor finding alone (M1 to M15, N1 to N6).
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id (B1, B2).
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
