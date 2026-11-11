review: 1 of 3

# Spec-panel critique, round 1: orca-worker-contract-spec.md

- Command: /sc:spec-panel, `--mode critique --focus requirements,architecture`, first review (no `--re-review`, no `--baseline`; no baseline noted).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (SPEC), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`, 285 lines.
- Prior report: none. Baseline: none.
- Reviewer model: claude-haiku-5-5, one reviewer. `superclaude review panel resolve` and `superclaude review merge` are not installed in this sandbox (`command -v superclaude` printed nothing), so one reviewer ran, as the loop allows. The panel is simulated by the expert lenses below, all run by this one reviewer.
- Review-loop prompt read in full before review: `home/.claude/rules/prompts/document_review_loop_prompts.md` (FIRST-REVIEW prompt applied).
- Command definition read in full: `command.md` (CMD). Its "Unattended mode" section (CMD:457-465) does not apply, because the brief does not pass `--unattended`.

Citation legend (all paths are under the sandbox workspace `ws/`):
- `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N.
- `INV-A:N` = `.dev/orca-command-refactor/inventory/commands-a.md` line N.
- `INV-B:N` = `.dev/orca-command-refactor/inventory/commands-b.md` line N.
- `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md` line N.
- `README:N` = `.dev/orca-command-refactor/README.md` line N.
- `CMD:N` = `command.md` line N.
- Citations to files outside `inventory/` (for example `src/superclaude/...`, `.dev/evals/...`, `CLAUDE.md`, `pyproject.toml`, the `orca-ide` guides and the `gh` output the spec quotes) cannot be checked in this sandbox. They are marked UNVERIFIED and are not counted as support for any claim below.

## Coverage

- Read in full: CMD, the review-loop prompt file, README, SPEC (285 lines), INV-A (120 lines), INV-B (323 lines), CAPS (188 lines).
- Checked: every §3 row against INV-A / INV-B (row citations in `SPEC:83-125` resolve to the matching inventory rows; the 10 / 27 / 6 split reconciles with `INV-A:73` (5+13+3) and `INV-B:278` (5+14+3)). Every `CAPS:N` cited in §1-§2 that falls in the capabilities inventory was read and matches its claim (checked: CAPS:52, 58-61, 64, 66-67, 72-74, 76-77, 79, 80, 97-103, 116, 129, 130, 147, 149, 151, 155, 156, 161, 187).
- Executed one check: the AC-C1 pattern (`SPEC:172`) against a probe file of three Orca calls, in the sandbox, then deleted the probe. Result: the pattern as written matched 0 lines (exit 1); the same pattern with a plain `|` alternation matched 3 lines (exit 0). This is the basis for F3.
- Not run: no command was run as an Orca worker and no Orca runtime exists here. Every verdict and phase claim in SPEC is taken as stated unless a finding says otherwise.
- Consistent with the inventories (no finding): the §3.1 list (10 ready commands) and the §4 list (6 coordinator-only commands) match `INV-A:73`, `INV-B:278`, `INV-A:87-92` and `INV-B:282-287`.

## Findings (grading by consequence)

### Blocking

**F1. WC-3 lets an implement halt receive a Ruling from the coordinator.** Category: safety. Severity: CRITICAL.
- Stated text: WC-3 says that when a gate would resolve as blocked, the session "may instead ask the coordinator once" and then "re-invoke or resume the command with the answer as a flag" (`SPEC:61`). The implement row says that on `E-HALT-QA` or `E-NO-RULING` the command stops and the contract is blocked (`SPEC:109`). D2 option (a), which the spec recommends, says the worker stops and ends `failed` (`SPEC:234`). The Ruling rule says "another agent's message ... [is] not acceptance" (`INV-A:66`, quoting `sc-implement-protocol/refs/qa.md:238`, UNVERIFIED here).
- Grading sentence: An implementer who follows WC-3 as written lets the coordinator answer the worker's `ask` on an implement halt, and the answer is recorded as a Ruling, which is wrong because D2 is still undecided (`SPEC:232-236`) and the Ruling rule forbids a relayed agent message as acceptance.
- Whittaker (Divergence attack): I can break this specification by **Divergence Attack**. The invariant at **WC-3 (`SPEC:61`) against the implement row (`SPEC:109`)** fails when **a blocked gate is a Ruling gate**. Concrete attack: the worker halts at `E-HALT-QA`, applies the blocked rule in WC-3, asks the coordinator, the coordinator relays a yes from the user, the worker re-invokes `/sc:implement` with the answer as a flag, and the Ruling is recorded before D2 is decided.
- Recommendation: state in WC-3 that a gate whose answer would be a Ruling, or any gate the command row says stops, is excluded from the ask path. Alternatively, name the ask path only for gates with a documented default or caller-supplied value.
- Priority: High.

**F2. AC-0.4 cannot pass in P0.** Category: unpassable-check. Severity: MAJOR.
- Stated text: AC-0.4 requires steps 1-3 and 5-7 to pass in P0 (`SPEC:194`). Step 3 requires that the report path "is the WC-4 contract path" and that `--outcome` matches the contract's status (`SPEC:182`). The WC-4 contract is added in P1 (`SPEC:159`, and `SPEC:194` says "the contract arrives in P1").
- Grading sentence: An implementer who follows AC-0.4 runs `/sc:troubleshoot` (which writes `REPORT.md`, `INV-B:49`) in P0, and step 3 cannot pass because no WC-4 contract exists, so P0 never closes.
- Recommendation: make step 3 in P0 check `REPORT.md` or the command's existing report, or move AC-0.4 step 3 to P1.
- Priority: High.

**F3. AC-C1 never fails.** Category: safety. Severity: MAJOR.
- Stated text: AC-C1 is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` and passes when it "prints nothing" (`SPEC:172`). In ERE, `\|` is a literal pipe, not alternation.
- Evidence: the sandbox probe in this review returned exit 1 on three lines containing Orca calls. The same pattern with `|` returned exit 0 and printed all three.
- Grading sentence: An implementer who runs AC-C1 in each phase gets no output on any tree, marks SA-2 and WC-8 satisfied, and a command that calls `orca orchestration ask` passes the gate. Such a call makes the command fail with `runtime_unavailable` outside Orca (`CAPS:147`), which breaks standalone use (`SPEC:147`).
- Recommendation: use `|` with `grep -E` (or `\|` with `grep -G`) and add a positive self-test to AC-C1 that must match a planted line.
- Priority: High.

**F4. `load` is required to write a contract that the spec forbids it to write, and WC-5 then reports a successful run as failed.** Category: contradiction. Severity: MAJOR.
- Stated text: AC-1.1 requires every command in §3.1-3.2 to name `return-contract.yaml` in its Unattended section (`SPEC:195`). The `load` row says the report is "none (see note)" and the note says to use it "as a step inside another worker's brief" (`SPEC:112`). The decision table rejects "Add a report file" for load as "an unrequested addition" (`SPEC:265`). WC-5 says `--outcome failed` when "no report exists" (`SPEC:63`).
- Grading sentence: An implementer who follows `SPEC:265` writes no contract for load and fails AC-1.1, and an implementer who follows AC-1.1 adds a contract that `SPEC:265` rejects. Either way a successful `load` run that writes nothing is sent as `--outcome failed` under WC-5.
- Whittaker (Zero/Empty attack): I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **the command writes no report**. Concrete attack: `/sc:load` completes, loads context into the session, writes no file (`INV-B:31`, `INV-B:65`), and the worker sends `worker_done --outcome failed`.
- Recommendation: either exempt no-output commands from WC-5's "no report exists" rule and from AC-1.1, or give load a contract that records the loaded keys.
- Priority: High.

**F5. The §3.1 intro says brainstorm and init-lite need no change, but P1 and AC-1.1 require both.** Category: contradiction. Severity: MAJOR.
- Stated text: "The only command changes are the small fixes in the last column" (`SPEC:79`). Brainstorm and init-lite have "None" in that column (`SPEC:84`, `SPEC:87`). P1 says "the `--unattended` flag accepted by every command in sections 3.1 and 3.2" (`SPEC:159`), and AC-1.1 requires every §3.1 command to have an Unattended section (`SPEC:195`). Neither command appears in any phase's command list (`SPEC:158-162`).
- Grading sentence: An implementer who follows `SPEC:79` leaves brainstorm and init-lite without `--unattended`, so AC-1.2 (`SPEC:196`) fails on any `--unattended --output` run; an implementer who follows `SPEC:159` has no phase step for init-lite's WC-4 contract, because init-lite writes only `.dev/superclaude/context-audit.md` (`SPEC:87`).
- Recommendation: add brainstorm and init-lite to a phase's command list, state the WC-4 change for init-lite, and correct the §3.1 intro.
- Priority: High.

**F6. init-lite overwrites a prior attempt's report on retry.** Category: data-loss. Severity: MAJOR.
- Stated text: init-lite's WC-6 mechanism is "Re-run overwrites its marked report" (`SPEC:87`). WC-6 allows resume from on-disk state with a resume flag, or a fresh output directory, and says a retry "must not corrupt the first attempt's output" (`SPEC:64`). init-lite has no resume flag (`INV-A:55`).
- Grading sentence: An implementer who follows `SPEC:87` leaves init-lite overwriting its report on a retry, so the first attempt's report is replaced, which WC-6 forbids.
- Recommendation: give init-lite a fresh output directory per run, as WC-6 requires for commands without a resume flag.
- Priority: High.

### Medium (follow-up candidates; not blocking)

**F7. WC-4 names `<output-dir>` for every command, but several commands have no directory argument.** Category: missing-requirement. Severity: MAJOR, graded Medium.
- WC-4 defines `<output-dir>` as "the directory the coordinator passed (`--output` / `--output-dir`)" (`SPEC:62`). tdd takes a file (`--output <file>`, `SPEC:90`, `INV-B:47`). workflow has no output flag and writes to `.dev/tasks/to-do/<id>/` (`SPEC:92`, `INV-B:52`). adversarial writes to `<output>/adversarial/` (`SPEC:83`), not `<output-dir>/`. The spec does not say who creates the directory before a stop with "no other output" (`SPEC:62`).
- Recommendation: define the contract location per command in each §3 row, and give the file-valued tdd a directory form.

**F8. A retry cannot both know its report path before dispatch and get a fresh directory chosen by the command.** Category: missing-requirement. Severity: MAJOR, graded Medium.
- WC-4 says the report file is "known before dispatch" (`SPEC:62`). WC-6 says the command "writes each run into a fresh output directory" (`SPEC:64`). If the command chooses the directory, the path is not known before dispatch. If the coordinator passes a new `--output` on retry, WC-6 is met but the spec does not say so (`SPEC:52-53`, the brief content in §2.3 `SPEC:73`).
- Whittaker (Sequence attack): I can break this specification by **Sequence Attack**. The invariant at **WC-4 and WC-6** fails when **a retry reuses the brief's output directory**. Concrete attack: a first attempt writes its contract, the coordinator starts a `--retry-of` worker with the same brief, the command writes into the same directory, and the first attempt's report is overwritten.
- Recommendation: state that the coordinator sets a fresh `--output` in every retry brief (§2.3), and that the command never picks its own directory.

**F9. cleanup-audit uses one fixed output directory, which WC-11 forbids.** Category: contradiction. Severity: MAJOR, graded Medium.
- The cleanup-audit row says "output dir is fixed, so one audit per worktree at a time (WC-11)" (`SPEC:85`). WC-11 says "Two workers in one worktree must never write the same file. Default output paths carry a timestamp or the slug the coordinator passes" (`SPEC:69`). The fixed directory is also the `progress.json` checkpoint location (`INV-A:42`).
- Consequence: two cleanup-audit workers dispatched in one worktree overwrite each other's checkpoint. The spec's only guard is the coordinator's own convention. Graded Medium because the wrong outcome needs two concurrent dispatches, which the coordinator controls.
- Recommendation: add a per-run slug to the cleanup-audit output path, or make the coordinator serialize it.

**F10. `--unattended` may auto-accept reflect remediation, and that trigger is not the existing rule.** Category: safety. Severity: MAJOR, graded Medium.
- The reflect row says that under `--unattended`, `--remediate` should "follow the existing headless auto-accept rule instead of the `[yes / no]` prompt" (`SPEC:88`). The tasklist row says Stage 10.5 passes `--unattended` "so the headless rule applies" (`SPEC:122`). The existing rule keys on `claude --print` with no TTY (`INV-B:109`, `INV-B:310`). SA-6 says `--unattended` "reuses it" (`SPEC:151`), which changes its trigger without saying so.
- Grading: Medium, because the spec does not say that remediation edits need a person's approval. WC-9 covers push, PR, post, install, provision and paid runs (`SPEC:67`), not code edits. Cleanup and improve already edit code unattended (`SPEC:103`, `SPEC:110`), so the spec may intend this, but it should say so.
- Recommendation: state whether remediation edits are authorized by the brief, and name the trigger that makes the headless rule apply.

**F11. The WC-5 outcome mapping has no rule for a status and `blocked_question` that disagree.** Category: other. Severity: MINOR, graded Medium.
- WC-5 maps `partial` to `succeeded` (`SPEC:63`, `SPEC:263`). Nothing says what happens when a contract has `status: succeeded` (or `partial`) and a non-empty `blocked_question`.
- Whittaker (Sentinel collision attack): I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **`blocked_question` is set but `status` is not `blocked`**. Concrete attack: the worker writes `status: partial` with a question, Orca receives `--outcome succeeded`, and the coordinator reads a successful run that is waiting for an answer.
- Recommendation: a non-empty `blocked_question` forces `status: blocked` and `--outcome failed`.

**F12. A missing, truncated or unparseable contract has no coordinator rule.** Category: other. Severity: MAJOR, graded Medium.
- WC-4 says the contract is "written on success, failure, blocked and partial outcomes" (`SPEC:62`), but gives no atomic-write rule. The coordinator "opens the file" (`SPEC:73`), and AC-2.x parses it (`SPEC:183`). A process killed mid-write leaves a partial YAML, and the spec does not say whether that is `failed`, `blocked` or a retry.
- Recommendation: write to a temporary name and rename, and state the coordinator's handling for missing or unparseable contracts.

**F13. The tasklist nesting claim is stated as settled, but the inventory marks it UNVERIFIED.** Category: other. Severity: MINOR, graded Medium.
- The tasklist row says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" (`SPEC:122`). `INV-A:14` rests on a documentation URL (UNVERIFIED here). `INV-B:46` marks the same nesting UNVERIFIED, and `INV-B:314` item 1 lists it as unknown. The spec's own gap statement says Agent-tool fan-out "has no proven limit" (`SPEC:45`).
- Recommendation: mark the tasklist row UNVERIFIED and add it to the AC-2.2 or AC-4 live checks.

**F14. WC-3 has no bound on ask and resume cycles.** Category: other. Severity: MINOR, graded Medium.
- WC-3 says the session may ask "once" and then re-invoke (`SPEC:61`), but a re-invoked command can block again, and nothing caps the cycles. The circuit breaker counts only `worker-start` failures, not reports (`CAPS:80`). The `ask` default timeout is UNVERIFIED (`SPEC:281` item 10).
- Whittaker (Accumulation attack): I can break this specification by **Accumulation Attack**. The invariant at **WC-3 (`SPEC:61`)** fails when **a command keeps reporting blocked after each answer**. Concrete attack: each re-invocation writes a new blocked contract, and the coordinator keeps answering with no limit.
- Recommendation: allow one ask per gate and one re-invocation, then send `failed`.

**F15. The contract has no schema version, and the coordinator checks only two fields.** Category: other. Severity: MINOR, graded Medium.
- WC-4 says the contract "carries at least: `status` ... `command` ...", and commands "keep their fields and add the missing ones" (`SPEC:62`). The workflow contract is already "contract 1.1" with different fields (`INV-B:52`, `SPEC:92`). AC-2.x checks only `status` and `command` (`SPEC:183`).
- Recommendation: add a `contract_version` field and state which fields are required for each version.

## Expert analysis (by lens)

- **Wiegers (requirements, traceability):** F4 and F5 are traceability failures: AC-1.1 and P1 trace to rows the spec says need no change. F2 and F3 are acceptance criteria that cannot pass or cannot fail.
- **Adzic (examples):** AC-0.4 and AC-2.2 give good concrete examples, but AC-0.4 step 3 is not satisfiable with the example it names (F2). The `load` example (F4) is not in any AC.
- **Cockburn (actor and goal):** the actor who answers an `ask` is the coordinator, but WC-3 does not say whether the coordinator has the user's authority to answer a gate (F1).
- **Fowler (architecture):** the contract is a file the coordinator reads, but its location is defined per command in some rows and in WC-4 in others (F7). The decision to keep commands unchanged (`SPEC:16`) is sound; the per-row exceptions are where the design leaks.
- **Newman (service evolution):** no contract versioning (F15); workflow's contract already differs (`INV-B:52`).
- **Hohpe (integration):** the file-based handoff has no atomic write, no missing-file rule and no ordering rule for retries (F8, F12).
- **Nygard (failure modes):** F6 (overwrite), F12 (partial write) and F14 (unbounded ask cycles) are failure modes the spec does not cover. The 60-second readiness analysis (`SPEC:43-44`) is sound and its evidence is cited.
- **Whittaker (adversarial, active in every review):** five attacks are written above (F1 Divergence, F4 Zero/Empty, F8 Sequence, F11 Sentinel, F14 Accumulation). F3 is an attack on a verification gate, not on the spec's behaviour.
- **Crispin (testing):** F2, F3 and F9's pass condition (AC-C3 is sound). The `test_worker_contract.py` assertions (`SPEC:195-204`) do not test AC-C1's safety property.
- **Hightower (operations):** no finding beyond F12 and F14; the coordinator's release rule (`CAPS:107-113`) is cited correctly.

## Mandatory output: Guard Condition Boundary Table

Triggered: SPEC contains conditional logic (gate resolutions, outcome mapping, the `--unattended` switch, the fresh-directory rule). Every guard is enumerated below. Input classes left out are given a reason. FR-8: every GAP is graded by consequence in the findings above. FR-10: the table is complete.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | `SPEC:51`, `SPEC:228` | Zero/Empty | flag absent | false | standalone behaviour unchanged (`SPEC:146`) | OK |
| `--unattended` switch | `SPEC:51` | Sentinel Value Match | `--unattended` inside quoted spec text | false | the command text says a quoted argument does not switch the mode (`CMD:459`); SPEC is silent | GAP (follow-up, not blocking; the command text covers it) |
| `--unattended` switch | `SPEC:51` | Legitimate Edge Case | `--unattended` on a command with no gate | true | a no-op (`SPEC:159`) | OK |
| WC-2 gate resolution | `SPEC:60` | Typical | gate with no default and no flag | blocked: status `blocked`, stop | defined | OK |
| WC-3 ask branch | `SPEC:61` | Legitimate Edge Case | blocked gate whose answer would be a Ruling | ask allowed (WC-3) vs stop (`SPEC:109`) | conflicting texts | GAP, blocking (F1) |
| WC-3 ask branch | `SPEC:61` | Zero/Empty | ask times out with no reply | resume by message ID | `SPEC:61`; timeout default UNVERIFIED (`SPEC:281` item 10) | GAP, Medium (F14) |
| WC-4 contract path | `SPEC:62` | Zero/Empty | no `--output` flag (workflow; tdd takes a file) | `<output-dir>` undefined | none stated | GAP, Medium (F7) |
| WC-4 contract | `SPEC:62` | Sentinel Value Match | contract missing or unparseable | no coordinator rule | none stated | GAP, Medium (F12) |
| WC-4 contract | `SPEC:62` | One/Minimal | one-field contract (`status` only) | not covered | AC-2.x requires `status` and `command` (`SPEC:183`) | OK for AC-2.x; GAP for the coordinator (F15) |
| WC-5 outcome mapping | `SPEC:63` | Zero/Empty | no report exists | `--outcome failed` | defined | GAP, blocking via F4 for load |
| WC-5 outcome mapping | `SPEC:63` | Typical | status `succeeded`, verdict FAIL | `--outcome succeeded` | defined | OK |
| WC-5 outcome mapping | `SPEC:63` | Sentinel Value Match | status `succeeded` or `partial` with non-empty `blocked_question` | unspecified | none stated | GAP, Medium (F11) |
| WC-6 resume or fresh dir | `SPEC:64` | Zero/Empty | no resume flag and a prior report exists | overwrite (init-lite) vs fresh dir (WC-6) | conflicting texts | GAP, blocking (F6) |
| WC-6 resume or fresh dir | `SPEC:64` | Legitimate Edge Case | retry after a first attempt | fresh dir chosen by whom | command vs coordinator unstated | GAP, Medium (F8) |
| WC-11 parallel-safe output | `SPEC:69` | Legitimate Edge Case | two workers in one worktree | cleanup-audit fixed dir | conflicting texts | GAP, Medium (F9) |
| §3.1 reflect remediation | `SPEC:88` | Typical | `--unattended` with `--remediate` | headless auto-accept | trigger not the existing rule | GAP, Medium (F10) |

Left out with reason: the Maximum/Overflow class for WC-4 and WC-5 (neither guard counts a bounded resource), and the Maximum/Overflow class for the `--unattended` switch (it is a boolean).

## Pipeline Dimensional Analysis: not triggered

The spec describes lifecycle steps (dispatch, check, settle, release) and a contract file, not a data flow whose count changes between stages. No stage filters, aggregates or fans out data in a way that changes the count, so FR-17 does not apply. The State Variable Registry (FR-15.1) is mandatory only under `--focus correctness`, which is not active.

## Consensus and disagreements

- Consensus: the decision to keep commands as units of work (`SPEC:16-18`, `SPEC:39`) is supported by the inventory evidence (`INV-A:95-96`, `INV-B:292`) and by CAPS:97-103. No expert disagrees with it.
- Disagreement: whether the coordinator may answer a worker's ask on a gate that the command row says stops (F1). The Wiegers and Whittaker lenses say no for implement; the spec's WC-3 text implies yes. This is the blocking disagreement.

## Follow-up candidates (Medium and minor, not blocking)

F7, F8, F9, F10, F11, F12, F13, F14, F15 (listed above). Not asked of a user in this run: it is a subagent run with no user channel. The list is recorded only, and no issue was created.

## UNVERIFIED in this review

- Every citation to `src/superclaude/`, `.dev/evals/`, `.dev/codegraph-migration/`, `CLAUDE.md`, `pyproject.toml` and the `orca-ide` guide text: not in this sandbox.
- The quoted `qa.md:238` and `reflect` headless rule: quoted through INV-A and INV-B, not read directly.
- Whether Orca enforces `--report-path` (SPEC:281 item 3) and the `ask` default timeout (SPEC:281 item 10): not checked.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "safety", "anchor": "the session may instead ask the coordinator once with", "anchor2": "stop with the halt recorded in the ledger and the contract as blocked", "refs": ["WC-2", "WC-3", "D2", "implement row"], "claim": "WC-3 lets a blocked worker ask the coordinator and re-invoke with the answer, so the implement halt can receive a Ruling before D2 is decided, which the Ruling rule forbids."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "its report path is the WC-4 contract path", "anchor2": "steps 1-3 and 5-7 pass", "refs": ["AC-0.4", "AC-C3", "WC-4", "P0"], "claim": "AC-0.4 step 3 needs a WC-4 contract, which only arrives in P1, so P0 cannot pass as written."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "safety", "anchor": "\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "In grep -E the escaped pipe is a literal, so AC-C1 never matches an Orca call and always passes, which hides an SA-2 violation."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "use it as a step inside another worker", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming return-contract.yaml", "refs": ["AC-1.1", "WC-4", "WC-5", "load row", "D-load"], "claim": "AC-1.1 requires a contract for load, the decision table rejects it, and WC-5 then sends a successful load run as failed."}
{"id": "F5", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "The only command changes are the small fixes in the last column.", "anchor2": "`--unattended` flag accepted by every command in sections 3.1 and 3.2", "refs": ["§3.1 intro", "P1", "AC-1.1", "AC-1.2", "brainstorm row", "init-lite row"], "claim": "brainstorm and init-lite are listed as needing no change, but P1 and AC-1.1 require the flag and a contract for both, and no phase lists them."}
{"id": "F6", "severity": "MAJOR", "blocking": true, "category": "data-loss", "anchor": "Re-run overwrites its marked report", "anchor2": "must not corrupt the first attempt", "refs": ["WC-6", "init-lite row"], "claim": "init-lite overwrites its report on retry, which replaces the first attempt's report that WC-6 says must be kept."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "where `<output-dir>` is the directory the coordinator passed", "anchor2": "a precise component prompt, not a bare topic; `--output <file>`", "refs": ["WC-4", "tdd row", "workflow row", "adversarial row"], "claim": "WC-4 defines the contract location through an output directory that tdd (file), workflow (none) and adversarial (subfolder) do not provide."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "One report file, known before dispatch, written on every outcome", "refs": ["WC-4", "WC-6", "§2.3"], "claim": "A fresh directory chosen by the command is unknown before dispatch, so WC-4 and WC-6 conflict on retry."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "output dir is fixed, so one audit per worktree at a time", "anchor2": "must never write the same file", "refs": ["WC-11", "cleanup-audit row"], "claim": "cleanup-audit's fixed output directory lets two concurrent workers overwrite each other's checkpoint, which WC-11 forbids."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "safety", "anchor": "make `--remediate` follow the existing headless auto-accept rule", "anchor2": "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies", "refs": ["SA-6", "WC-9", "reflect row", "tasklist row"], "claim": "Unattended reflect may auto-accept remediation that edits code, and the spec does not say the brief must authorize it; the headless trigger also changes from claude --print to a flag."}
{"id": "F11", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5", "D-partial"], "claim": "A contract with status not blocked but a non-empty blocked_question has no outcome rule, so a waiting worker can be sent as succeeded."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "It is written on success, failure, blocked and partial outcomes", "refs": ["WC-4", "§2.3", "AC-2.x"], "claim": "A partial or unparseable contract has no atomic-write rule and no coordinator handling rule."}
{"id": "F13", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker", "refs": ["tasklist row", "INV-B:46", "INV-B:314", "SPEC:45"], "claim": "The tasklist nesting claim rests on an UNVERIFIED docs citation and is stated as settled."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "then re-invoke or resume the command with the answer as a flag", "anchor2": "On an `ask` timeout it resumes the same message ID", "refs": ["WC-3", "CAPS:80", "SPEC:281"], "claim": "Re-invocation and ask cycles have no bound, so a command can block and re-ask indefinitely."}
{"id": "F15", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "refs": ["WC-4", "AC-2.x", "INV-B:52"], "claim": "The contract has no version field, and AC-2.x checks only two fields, so per-command contract evolution is unguarded."}
```

## Reviser brief

Blocking finding ids: F1, F2, F3, F4, F5, F6.

Restated rules for the reviser (review loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (F7-F15) are not part of this brief and must not be revised.

verdict: FAIL
