review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (critique, focus requirements + architecture)

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `83f24502ee791d296bebd644adce8eba84b0a7bccbb076f090415ba276880733` (59941 bytes)
- baseline: none given; `--re-review` not given. This is a labelled whole-document first review (FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full before reviewing).
- reviewer model actually used: claude-sonnet-5-5
- mode / focus: `--mode critique --focus requirements,architecture`; format standard (critique buckets). Panel in fixed order: Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower (lead experts per focus: Wiegers for requirements; Fowler for architecture).
- brief clauses overridden: none. The brief narrowed nothing and widened nothing.
- Citation key: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. README was read first, as the brief requires.

## Coverage statement
Covered: the whole candidate (sections 1-9, Decisions, UNVERIFIED items), the three inventories, the README, `command.md` and the review-loop prompts file.
Citation check: I compared about 75 `INV-A`, `INV-B`, `CAPS` and `README` citations in the candidate against the inventory lines. None was wrong (rows, line ranges, counts: 21 + 22 = 43; 10 / 27 / 6; phase membership 9 + 11 + 4 + 3 = 27 rows plus 3 + 4 fixes of ready commands).
UNVERIFIED (not checkable inside the sandbox, so not relied on): every citation to `src/superclaude/{commands,skills,agents,core}/...`, `CLAUDE.md`, `HOW-WE-WORK.md`, `Makefile`, `pyproject.toml`, `install_core.py`, `.dev/evals/...EVIDENCE.md`, `.dev/codegraph-migration/...` and the `grep` result quoted at SPEC:25, except where an inventory quotes the same line (those are marked by the inventory line). The claim at SPEC:11 that 11 locations were re-read is likewise UNVERIFIED here. Not covered: whether the Orca guide text quoted at CAPS:* is current (it is a numbered output of one CLI version, CAPS:8).
Not run: no command could be run (no Orca, no repo), so AC-C1 to AC-4.3 were assessed by reading only.

## Grading rule applied
Each finding passed the FIRST-REVIEW grading check: "An implementer who follows the stated text as written builds X, and X is wrong because Y." A finding is **blocking** only when that sentence holds with no further assumption (two stated texts that contradict, or a stated text that an acceptance criterion cannot pass). A requirement the document never states, or a reading guess, is **Medium** and goes under follow-up candidates even when its label is MAJOR. MINOR is a note.

## Findings table
| id | bucket | label | grade | expert | one line |
|---|---|---|---|---|---|
| F-01 | requirements | MAJOR | **blocking** | Wiegers, Fowler | The contract file is promised for cleanup-audit and init-lite (and a path for index-repo) but section 3, REQ-2 and phase P1 build none |
| F-02 | requirements | MAJOR | Medium | Wiegers, Cockburn | WC-4 location rule cannot be met by rows that add no output flag |
| F-03 | requirements | MAJOR | Medium | Crispin | AC-2.2 says "per P2 command" but five P2 gate resolutions never end blocked |
| F-04 | architecture | MAJOR | Medium | Fowler, Hohpe | No rule for passing `--unattended` to nested invocations except tasklist to reflect |
| F-05 | architecture | MAJOR | Medium | Nygard | WC-10 trigger (more than 5 min) and ceiling (4 min) leave a gap; long Agent-tool calls cannot heartbeat |
| F-06 | requirements | MAJOR | Medium | Cockburn, Nygard | No coordinator procedure for a `blocked` worker or for a worker that dies without `worker_done` |
| F-07 | requirements | MAJOR | Medium | Wiegers | WC-9 needs "the command's own explicit flag" that task and post-release do not have |
| F-08 | architecture | MAJOR | Medium | Newman | Contract has no version field; fixed status set vs "existing contracts keep their fields" |
| F-09 | requirements | MINOR | Medium | Wiegers | Scope statements contradict: section 1.1 / non-goal 8 / SA-1 against load, business-panel, validate-tests, P3 reconciliation |
| F-10 | architecture | MAJOR | Medium | Nygard, Whittaker | WC-6 "re-run starts clean" ignores edits already made in the shared worktree |
| F-11 | requirements | MINOR | Medium | Crispin | AC-C1 scans `core/` where P0 adds Orca text; AC-C5 vs new flags in Usage lines |
| F-12 | requirements | MINOR | Medium | Wiegers | Finding ids REQ-1, REQ-2, ARCH-1, NEW-1 are used as justification but defined nowhere in the document |
| F-13 | requirements | MINOR | Medium | Adzic | `index` row asserts "does not wait" while the same row says that is UNVERIFIED |
| F-14 | requirements | MINOR | Medium | Hightower | WC-1 has no owner phase, no check of its own and an unmeasurable bound |
| N-1 to N-8 | mixed | MINOR | note | various | Notes at the end |

Blocking findings open: **F-01**. Medium and minor findings never fail the review (command.md Review Loop bullet 2).

---

## === REQUIREMENTS ANALYSIS ===

### F-01 (blocking) The WC-4 contract for cleanup-audit and init-lite is required by one text and built by none
- Expert: Karl Wiegers (traceability), Martin Fowler (interface consistency). Severity: MAJOR, blocking. Priority: High.
- Grading sentence: An implementer who follows the stated text as written builds cleanup-audit and init-lite with no `return-contract.yaml` (section 3 intro says these two gain no `## Unattended mode` section, SPEC:76; their small-fix cells add no contract, SPEC:85 and SPEC:87; phase P1 lists "fixes only to adversarial, cleanup-audit, index-repo (no section)", SPEC:159). That is wrong because WC-4 says init-lite's contract is the sibling `<file>.return-contract.yaml` and cleanup-audit's is `.claude-audit/return-contract.yaml` (SPEC:62), section 2.3 says a cleanup-audit retry "rewrites the contract there" (SPEC:73), and WC-5 sends `--outcome failed` when "no report exists" (SPEC:63). A successful audit or context-audit run would therefore be reported failed, or the coordinator would open a file nobody writes.
- Evidence the files do not exist today: cleanup-audit writes pass summaries, a final report and `progress.json`, no contract (INV-A:42); init-lite writes `.dev/superclaude/context-audit.md` or `--output`, no contract (INV-A:55); INV-A:97 says only brainstorm writes a named contract file among the first 21. SPEC:79 says the worker "reports the named file until Phase 1 adds the contract", but P1 never adds one for these two, so the until-clause never ends.
- Also affected (same defect, weaker): index-repo. Brief passes "none" (SPEC:86), no output flag exists (INV-A:53, location "implied, UNVERIFIED"), and WC-4 (SPEC:62) says that without an output path the command refuses. The row says it is ready with no flags.
- Recommendation (rationale: smallest change): either (a) delete cleanup-audit and init-lite from the WC-4 exceptions and from the 2.3 sentence and state that, until they gain a section, the worker passes the named report file from section 3.1, or (b) give both a one-line contract addition in P1 and add them to AC-1.1. Add an acceptance check that fits whichever is chosen (none exists today: AC-1.1 covers only the eight P1 commands, SPEC:195).
- Quality impact: Consistency +1, Testability +1.

### F-02 (Medium) WC-4 cannot be satisfied where a row adds no output flag
- Expert: Wiegers, Cockburn. Label MAJOR, graded Medium (the implementer needs a guess to add a flag). Priority: High.
- WC-4 makes the contract location depend on an output flag and says that with no output path "the command stops with a chat-only refusal ... WC-5 then sends `--outcome failed`" (SPEC:62). Rows whose cells say "contract" but add no flag and give no location: research (SPEC:116; its report name is generated at run time, INV-B:132, yet WC-4 says "known before dispatch"), review-translation (SPEC:117), save (SPEC:119), task (SPEC:121), recommend (SPEC:115), cli-eval (SPEC:104), explain (SPEC:108), implement (contract "beside the ledger", slug-derived, SPEC:109) and validate-tests (existing `--report` is a file flag but is not in the file-flag list, SPEC:62 and SPEC:125).
- If an implementer follows WC-4 literally these commands refuse every unattended run, and AC-2.3 ("happy-path run ... with every required flag in the brief", SPEC:201) cannot pass because no flag exists to pass.
- Recommendation: add one column or sentence to section 3.2 naming, per row, the flag that carries the contract directory (reuse `--output` where a command already has one) and list the file-flag exceptions in full.

### F-03 (Medium) AC-2.2 cannot pass for the P2 commands whose gate does not block
- Expert: Lisa Crispin. Label MAJOR, graded Medium (the natural narrower reading exists). Priority: Medium.
- AC-2.2 reads "Gate-trigger run per P2 command ... Pass: `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`" (SPEC:200). Five P2 rows resolve their gate by a default or a switch, not by "blocked": research pins `--strategy planning` (SPEC:116), auggie-review turns off posting and the offer (SPEC:100), cleanup and improve apply only auto items and list the rest (SPEC:103, SPEC:110), tasklist passes `--unattended` to reflect (SPEC:122). Reflect's `--remediate` follows the headless auto-accept rule (SPEC:88). Section 7 says a phase passes only when every check passes (SPEC:167).
- Recommendation: scope AC-2.2 to "each P2 command whose section 3 row resolves a gate as blocked" and add a second check for default-resolved gates (the run ends `succeeded` and shows no prompt).

### F-06 (Medium) No coordinator procedure for `blocked` outcomes or for a worker that dies silently
- Expert: Alistair Cockburn (primary actor goal), Nygard. Label MAJOR, graded Medium (requirement never stated). Priority: High.
- WC-5 maps `blocked` to `--outcome failed` (SPEC:63). Orca keeps a failed Task's dependents blocked until a `--retry-of` replacement completes it (CAPS:90). Section 2.3 ends with "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker" (SPEC:73) and nothing says how the coordinator answers the `blocked_question`: re-dispatch with `--retry-of`, a new output directory (ARCH-1) and the answer as a flag? For most rows the resume cell is "fresh dir" (SPEC:99-125), so the answer re-runs the command from the start.
- Second hole: the contract is written "on every outcome" (SPEC:62) yet the coordinator reads it only after `worker_done` (SPEC:73). If the worker dies after writing the contract, the spec does not say whether a present contract with no `worker_done` counts as settled. Orca's guidance is that absence never authorizes stop or retry (CAPS:125-126); the spec does not connect the two.
- Recommendation: add a short "coordinator handling" paragraph to 2.3: blocked, failed with contract, failed without contract, no `worker_done`; each with the Orca verb the coordinator uses.

### F-07 (Medium) WC-9 relies on explicit flags that two commands do not have
- Expert: Wiegers. Label MAJOR, graded Medium. Priority: Medium.
- WC-9: outward actions turn on "only through the command's own explicit flag written in the brief" (SPEC:67). task's `commit` and `push` EXEMPT keywords run immediately with no skill and no flag (INV-B:204), and post-release's confirmations are "unless the user pre-authorized them this session" (INV-B:79), not a flag. Rows say "refused unless authorized (WC-9)" (SPEC:121) and "unless the brief authorizes them" (SPEC:113) without naming a flag.
- Also: D4 lists auggie-review and task as affected (SPEC:244) while section 6 says "Phases 1-3 need no user decision" (SPEC:154) and task and auggie-review are P2. Section 9's own sentence "Phases 0-3 can proceed on the recommendations" (SPEC:225) softens this, but the two statements are not reconciled.
- Recommendation: name the flag per command (or state that P2 simply refuses and P4/D4 adds the authorization flag).

### F-09 (Medium) Scope statements disagree with the per-command fixes
- Expert: Wiegers. Label MINOR. Priority: Low.
- Section 1.1 says what changes in commands "is limited to" the worker contract (SPEC:16); non-goal 8 says only defects that stop a command working as a worker are in scope (SPEC:220). Section 3 also fixes the load usage line (SPEC:112), the business-panel frontmatter (SPEC:102, effect UNVERIFIED), the validate-tests default target (SPEC:125) and the roadmap and validate-roadmap drift (SPEC:118, SPEC:124). Section 5 calls "exactly today's behaviour" a hard requirement on every phase (SPEC:142) and SA-1 freezes output paths (SPEC:146), while SA-4 allows defect fixes that "correct a documented defect" (SPEC:149) and AC-3.1 requires command and skill to name the same report filename (SPEC:204), which changes one person-visible path.
- Recommendation: add "or a listed drift defect (SA-4)" to section 1.1 and non-goal 8, and say in SA-1 that SA-4 is its only exception.

### F-12 (Medium) Dangling finding ids
- Expert: Wiegers (traceability). Label MINOR.
- The text cites REQ-1, REQ-2, ARCH-1 and NEW-1 about 20 times as the reason for a rule (for example SPEC:62, SPEC:64, SPEC:73, SPEC:76, SPEC:159, SPEC:182, SPEC:200). None is defined in the candidate; they appear to name findings of the earlier review (`review/spec-panel.md`, `review/disposition.md`, README:21 output table), which this audit was not given. A reader of the spec alone cannot resolve them.
- Recommendation: replace each id with the rule it points to, or add a one-line glossary.

### F-13 (Medium) `index` is handled differently from the two other uncertain interactive modes
- Expert: Gojko Adzic. Label MINOR.
- business-panel `--mode socratic` and explain `--format interactive` are refused under `--unattended` (SPEC:102, SPEC:108). index gets "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)" (SPEC:111). The required text would assert a behaviour the inventory could not confirm (INV-A:54, INV-A:113).
- Recommendation: use the same treatment (refuse, or pin a non-interactive mode) until verified.

### F-14 (Medium) WC-1 has no owner phase and no measurable bound
- Expert: Kelsey Hightower. Label MINOR.
- WC-1 owner is "Launch setup, not commands" (SPEC:59) and no phase in section 6 changes launch setup (the only Orca-aware primitive is `ccsession-tag`, SPEC:25). "Well inside the readiness limit" has no number. The cited evidence puts the failing edge at about 45 s because that test used a 45 s limit (CAPS:49), not the 60 s default (CAPS:44), so "above about 45 s it fails again" (SPEC:59) is not a property of the default.
- Recommendation: give WC-1 a number (for example 30 s as tested) and assign it to P0 or move it to a non-goal.

---

## === ARCHITECTURE ANALYSIS ===

### F-04 (Medium) No general rule for nested invocations
- Expert: Fowler (boundaries), Hohpe (message/flow). Label MAJOR, graded Medium (requirement never stated). Priority: High.
- The only nested propagation rule is tasklist Stage 10.5 passing `--unattended` to reflect (SPEC:122). Other nested calls in the inventories get none: roadmap calls `sc:save` at every wave (INV-B:154) while save's single-owner keys are overwritten whole (INV-B:165) and WC-11 says such files "are not written in unattended mode" (SPEC:69); tasklist Stage 9 calls `sc:task --compliance strict` (INV-B:211) whose confidence-below-0.70 prompt is a gate (SPEC:121); task calls troubleshoot on TFEP (INV-B:201); pr-submit may call auggie-review, whose default posts to GitHub (INV-B:91, INV-A:38). An implementer who builds the roadmap row as written keeps the nested save in its default mode. Which keys that save writes is UNVERIFIED (INV-B:154), so the wrong outcome needs a guess; hence Medium.
- Recommendation: add one WC row, "a command that invokes another `/sc:` command under `--unattended` passes `--unattended` and its output flag", and check it in AC-3.4 (extend it to a roadmap worker).

### F-05 (Medium) WC-10 boundary and long Agent-tool calls
- Expert: Michael Nygard. Label MAJOR, graded Medium. Priority: Medium.
- WC-10 triggers on a call "longer than 5 minutes" but then requires waits "of at most 4 minutes" (SPEC:68); AC-4.3 says "no single tool call exceeds 240 s" (SPEC:210); the Decisions row justifies 4 minutes as a margin (SPEC:266). A single call of 4 min 30 s is allowed by the trigger and rejected by AC-4.3.
- WC-10 and WC-7 together also leave long Agent-tool calls without a heartbeat: WC-7 forbids subagents from sending `heartbeat` (SPEC:65), the top-level session is blocked inside the Agent call, and fan-out stays as it is (SPEC:24, SPEC:219). Wide fan-outs exist (cleanup-audit waves, INV-A:42; tdd, INV-B:221; adversarial, INV-A:35). Whether Orca uses heartbeat age at all is UNVERIFIED (CAPS:130, CAPS:182), so the consequence is unknown.
- Also: no acceptance check enforces the cli-eval wait split in P2 (AC-2.1 asserts text only, SPEC:199).
- Recommendation: state one number for trigger and ceiling; say what a worker does during an Agent-tool call that may exceed it (nothing, if heartbeats are UNVERIFIED as liveness); add a cli-eval live check.

### F-08 (Medium) Contract schema and versioning
- Expert: Sam Newman. Label MAJOR, graded Medium (requirement never stated). Priority: Medium.
- WC-4 sets a minimum field list but no schema version (SPEC:62); workflow's contract is already versioned 1.1 (INV-B:272). The Decisions row fixes the status set to four values (SPEC:262) while WC-4 says existing contracts "keep their fields and add the missing ones" (SPEC:62). The existing status vocabularies of workflow, reflect, brainstorm and adversarial are not recorded in the inventories, so a collision cannot be ruled out (UNVERIFIED). No validator beyond the YAML load in 7.2 step 4 (SPEC:183).
- Recommendation: add `contract_version`, list each existing status vocabulary and its mapping, and say which field wins on conflict.

### F-10 (Medium) "Safe re-run" covers the output directory, not the worktree
- Expert: Nygard, Whittaker. Label MAJOR, graded Medium.
- WC-6 says a fresh output directory means "a re-run starts clean" (SPEC:64). Commands that edit product files (cleanup, improve, task, document, build, test `--fix`; INV-A:43, INV-A:52, INV-B:204, INV-A:47, INV-B:234) leave those edits in the worktree workers share (CAPS:115). A `blocked` task worker (TFEP present-to-user, SPEC:121) retried in a fresh directory runs on an already-edited tree. The spec gives no rule (clean worktree, or contract lists changed files and the retry brief says so). The cleanup row already asks that the contract list every changed file (SPEC:103) but only that row.
- Recommendation: extend the "contract lists every file changed" rule to all editing commands and have the retry brief carry that list.

### F-11 (Medium) Two acceptance commands conflict with deliverables
- Expert: Crispin. Label MINOR.
- AC-C1 greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and requires no output (SPEC:172), yet P0 adds `core/WORKER-CONTRACT.md` and an Orca section to `core/HOW-WE-WORK.md` (SPEC:158); an Orca routing section for a coordinator will naturally contain those words. SA-2 permits a mention only "in a changed command ... inside the contract file" (SPEC:147), which is self-contradictory wording (a command is not the contract file).
- AC-C5 requires no deleted line in a command file (SPEC:176) while SA-4 promises "new flags" (SPEC:149); a flag added to a Usage line changes that line. Only load's usage line is exempt (SPEC:112).
- Recommendation: exclude the two named core files from AC-C1 or state they use `ORCA` placeholders (as section 7 does); state where new flags are documented.

---

## === ADVERSARIAL ANALYSIS (Whittaker) ===
Severity classes: CRITICAL / MAJOR / MINOR as in command.md. Grades follow the same rule as above.

1. I can break this specification by **Sequence Attack**. The invariant at **WC-4 / section 2.3 (SPEC:62, SPEC:73)** fails when **a contract is promised but not built**. Concrete attack: before = P1 merged, init-lite still has no section (SPEC:76); step 1 coordinator dispatches `/sc:init-lite --output a.md`; step 2 command writes `a.md` only; step 3 worker, told by WC-4 that the contract is `a.md.return-contract.yaml`, finds nothing; after = WC-5 sends `--outcome failed` for a successful run. Maps to F-01. MAJOR, blocking.
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-4 (SPEC:62)** fails when **the brief passes `--output ""`**. Concrete attack: before = brief has the flag with an empty value; step 1 command must decide "no output path" or "path = cwd"; after = either a chat-only refusal or a contract in the working directory root. Unspecified. MINOR.
3. I can break this specification by **Sequence Attack** (stale state). The invariant at **WC-4 / 2.3** fails when **a directory already holds an old `return-contract.yaml`**. Concrete attack: before = dir has `status: succeeded` from an earlier dispatch (the coordinator broke 2.3); step 1 command is killed before writing; step 2 coordinator runs 7.2 step 4, which passes (`test -s`, status in set, SPEC:183); after = a dead run reads as succeeded. Nothing requires the command to delete or overwrite the contract at start. MAJOR, Medium (depends on a coordinator error, which 2.3 forbids).
4. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (SPEC:63)** fails when **a legacy contract uses a status outside the four-value set**. Concrete attack: before = workflow writes its own status word (UNVERIFIED which, INV-B:272); step 1 worker applies WC-5 to a value that is neither of the four; after = undefined outcome (the 7.2 assertion fails instead, SPEC:183). Maps to F-08. MAJOR, Medium.
5. I can break this specification by **Divergence Attack**. The invariant at **research row (SPEC:116) vs WC-2(b) (SPEC:60)** fails when **the brief passes `--strategy intent` together with `--unattended`**. Concrete attack: before = both flags present; the row says `--unattended` "pins" planning, WC-2(b) says a caller-supplied value is a valid resolution; after = two readings, one of which asks the user (INV-B:129). MINOR.
6. I can break this specification by **Accumulation Attack**. The invariant at **WC-5 plus Orca's circuit breaker (CAPS:80)** fails when **a command blocks every time**. Concrete attack: before = tdd with a bare topic; attempt 1 `blocked` (outcome failed); attempt 2 same; attempt 3 same; after = a worker's own failed report does not trip the breaker (CAPS:80), so retries can continue without limit and the spec gives the coordinator no stop rule. Maps to F-06. MINOR.
7. I can break this specification by **Divergence Attack**. The invariant at **WC-10 (SPEC:68)** fails when **a single call lasts 4 min 30 s**. Concrete attack: before = trigger false (not longer than 5 min); AC-4.3 limit 240 s; after = the same call passes WC-10 and fails AC-4.3. Maps to F-05. MAJOR, Medium.

---

## Guard Condition Boundary Table (Nygard builds, Crispin completes, Whittaker attacks)
The spec contains conditional logic and numeric thresholds, so the table is produced. Classes left out are named with a one-line reason in the final column of the row group below the table. FR-8 and FR-9 grading: a GAP row is Medium unless it names a concrete wrong outcome; none below reaches that bar except through F-01, which is graded in its own finding.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-4 output-path guard | SPEC:62 | Zero/Empty | no output path in brief, none named by WC-4 | true (refuse) | chat-only refusal, no file, `--outcome failed` | OK |
| WC-4 output-path guard | SPEC:62 | Zero/Empty (blank value) | `--output ""` | unknown | not stated | GAP (F-02, atk 2) |
| WC-4 output-path guard | SPEC:62 | Typical | `--output <new dir>` | false | contract at `<dir>/return-contract.yaml` | OK |
| WC-4 output-path guard | SPEC:62 | Sentinel Value Match | command with no output flag in its row (research, save, task, ...) | true | refusal, so the command can never succeed | GAP (F-02) |
| WC-4 output-path guard | SPEC:62, SPEC:73 | Legitimate Edge Case | directory already holds a contract | n/a | not stated | GAP (atk 3) |
| WC-4 / 2.3 contract existence | SPEC:62, SPEC:76 | Legitimate Edge Case | cleanup-audit, init-lite (no section) | contract required by WC-4 | no change builds it | GAP (F-01, blocking) |
| WC-5 outcome mapping | SPEC:63 | Typical | status `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | status `partial`; audit verdict FAIL | succeeded | `--outcome succeeded`, body states status | OK |
| WC-5 outcome mapping | SPEC:63 | Legitimate Edge Case | status `blocked` or `failed` | failed | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty | no file | failed | `--outcome failed` | OK |
| WC-5 outcome mapping | SPEC:63 | Zero/Empty (empty or unparseable file) | `""` | unknown | not stated ("no report exists" is about absence) | GAP (minor, atk 4) |
| WC-5 outcome mapping | SPEC:63 | Sentinel Value Match | status outside the four values | unknown | not stated | GAP (F-08) |
| WC-10 wait split | SPEC:68 | Typical | one call of 3 min | false | no split | OK |
| WC-10 wait split | SPEC:68 | Legitimate Edge Case | call of exactly 5 min | false (not longer than 5) | no split; heartbeat is due at 5 min | OK (inferrable) |
| WC-10 wait split | SPEC:68, SPEC:210 | Legitimate Edge Case | call of 4 min 30 s | false | passes WC-10, fails AC-4.3 | GAP (F-05, atk 7) |
| WC-10 wait split | SPEC:68 | Maximum/Overflow | eval wait of 3600 s | true | split into waits of at most 4 min | OK |
| WC-10 wait split | SPEC:65, SPEC:68 | Maximum/Overflow | Agent-tool call longer than 5 min | true | cannot be split, subagent cannot heartbeat | GAP (F-05) |
| task confidence guard | SPEC:121 | Typical | 0.50 | true | blocked | OK |
| task confidence guard | SPEC:121 | Legitimate Edge Case | 0.70 | false ("below 0.70") | proceeds | OK |
| task confidence guard | SPEC:121 | Zero/Empty | value missing | unknown | not stated | GAP (minor) |
| `--unattended` pin vs caller flag | SPEC:116, SPEC:60 | Legitimate Edge Case | `--strategy intent --unattended` | both | not stated | GAP (atk 5, minor) |
| ask-once guard | SPEC:61 | Zero/Empty | no preamble held | false | gate resolves as blocked | OK |
| ask-once guard | SPEC:61 | Legitimate Edge Case | a second gate fires after the first answer | unknown | "once" is per run or per gate, not stated | GAP (minor) |
| nesting depth | SPEC:33, CAPS:97 | Typical | depth 1 | true | worker may not start workers | OK |
| readiness limit | SPEC:59 | Typical | fallback 30 s | passes | evidence CAPS:49 | OK |
| readiness limit | SPEC:59 | Maximum/Overflow | fallback above the limit | fails | "well inside" has no number | GAP (F-14) |

Classes left out and why: One/Minimal is left out for the WC-4, WC-5, WC-10, confidence, ask and depth guards because no value distinct from Typical changes the guard result. Maximum/Overflow is left out for the WC-4 and WC-5 guards because neither has a capacity. Sentinel Value Match is left out for WC-10, confidence, ask, depth and readiness because none has a reserved value. Zero/Empty is left out for WC-10 (a zero-length wait never exceeds 5 min), for depth and for readiness (an unset value falls back to the Orca defaults, CAPS:44 and CAPS:100).

## Pipeline Dimensional Analysis
Not triggered: the spec describes no data pipeline whose stage output counts differ from input counts. For coverage I reconciled the one counted partition the spec relies on:

```text
[43 commands, cmd/] --> [3.1 ready: 10]   --> P1 fixes 3 (adversarial, cleanup-audit, index-repo)
                                              P2 gains 4 (reflect, release-split, tdd, troubleshoot)
                                              no change 3 (brainstorm, init-lite, workflow)
                    --> [3.2 change: 27]  --> P1 9 (8 + load usage line)  P2 11  P3 4  P4 3
                    --> [4 coordinator-only: 6]
                    10 + 27 + 6 = 43     counts conserved, no MISMATCH
```
Sources: SPEC:76, SPEC:159-162, INV-A:73, INV-B:278.

## Expert notes (critique voice, one line each)
- Wiegers: the requirement set is largely testable; F-01 and F-02 break traceability from WC-4 to the rows that must implement it.
- Adzic: the 7.2 live check is a real example-driven scenario; add one worked contract file so "the exact command line" and `blocked_question` have a concrete shape.
- Cockburn: the primary actor (the coordinator) has no stated handling for the two non-happy outcomes (F-06).
- Fowler: `--unattended` bundles four concerns (no prompts, report files, outward defaults off, parallel-safe writes); acceptable for one flag only if nested calls inherit it (F-04). The Orca-on-top boundary itself is sound and well argued (SPEC:28-39).
- Nygard: failure modes at the edges of the contract (stale file, silent death, retries without a stop rule) are missing (F-06, F-10, atk 3 and 6).
- Newman: contract versioning is absent (F-08).
- Hohpe: file plus message is a two-channel completion; their reconciliation is unstated (F-06).
- Crispin: acceptance criteria are specific and runnable; two do not fit the rows they test (F-03, F-11).
- Gregory: the quality expectations are explicit in section 7; the open decisions (section 9) are well framed for a decision-maker.
- Hightower: the launch-path requirement has no owner (F-14).

## Quality assessment (0-10)
Clarity 7, Completeness 7, Testability 7, Consistency 6. Overall 6.8.

## Notes (MINOR, no action required)
- N-1: SPEC:23 cites `invocation_method: "skill-direct"` as evidence the run worked, while SPEC:43 says that same run proved only the nested route. Both can be true (a subagent calling the skill directly); a half sentence would remove the apparent clash (INV-A:13).
- N-2: SPEC:60 says a stall is "invisible"; SPEC:44 and SPEC:181 say `agentWait` shows it. Whether `agentWait` detects a plain chat-ended turn (not a tool prompt) is unknown (CAPS:129, INV-A:62), and 7.2 step 5 only searches for `AskUserQuestion`.
- N-3: SPEC:133 and SPEC:67 use README:31 (a rule for this run's workers) as if it were a general repository policy for git and outward actions.
- N-4: UNVERIFIED item 14 (SPEC:285) is a record of a citation check, not an unverified item; it is misfiled and unnumbered in the inventories' style.
- N-5: SPEC:194 says step 5 verifies "no Agent-tool wrapper"; step 5 as written (SPEC:184) only searches for `AskUserQuestion`.
- N-6: CAPS:161 cites the installed `sc-pr-submit-protocol/SKILL.md` at lines 47-49 for the text the spec cites at 37-39 of the source copy (SPEC:65). The two copies differ by ten lines; harmless, but the spec says nothing about installed-versus-source drift.
- N-7: SPEC:183 relies on PyYAML being a declared dependency (`pyproject.toml:38`, UNVERIFIED here).
- N-8: SPEC:23 E2 "and answered" is not in the quoted evidence line (CAPS:49).

## Follow-up candidates (Medium and minor; never trigger a revision)
F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13, F-14, N-1 to N-8, attacks 2 to 7.
Issue offer: the command asks the user once per loop whether to open an issue for these. No user is present in this run, so the question was not asked and no issue was created.

## Reviser brief
Blocking finding ids: **F-01**.
Reviser contract (restated from the command; the reviser reads this report, not the command): revise only text that F-01 names; add no rule, mechanism or section that F-01 does not call for; cite the finding id `F-01` on each added paragraph or table row; prefer deleting or narrowing to adding; report the byte size of the candidate before and after, and the bytes added and deleted for F-01; leave every Medium and minor finding alone; return the candidate once and do not award yourself a PASS. Text F-01 names: SPEC:62 (the exception list for init-lite and cleanup-audit), SPEC:73 (the cleanup-audit clause), SPEC:79 (the "until Phase 1 adds the contract" clause) and, if the contract is kept, SPEC:85, SPEC:87, SPEC:159 and SPEC:195.

verdict: FAIL
