review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Kind: labelled whole-document audit of the final spec, a first review of the whole document. Prompt used: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `2d14bcd06b4ba445afa8a700e4b20d34af0ab4a0f9ac87d402e2488534d77270`
- baseline: none given, and `--re-review` not given, so this is a first review of the full document.
- reviewer model used: `claude-sonnet-5-5`
- Citation shorthand: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## What was covered

- Read in full: command definition, README (binding context), the review-loop prompts file, the candidate, all three inventories.
- Checked: every `INV-A/INV-B/CAPS` line citation the spec makes against the inventory files (all spot-checked citations resolved to the claimed content). The 10 / 27 / 6 split (`S:76`) re-counted from `INV-A:73` and `INV-B:278`: 5+5 ready, 13+14 needs-change, 3+3 coordinator-only, 43 commands. The phase membership lists (`S:159-162`) match the Phase column of `S:99-125` row for row.
- Experts applied (fixed order): Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture); Crispin and Gregory only on acceptance checks bearing on the two foci.
- NOT checkable in this sandbox, so UNVERIFIED: every `src/superclaude/...` line cite that the spec carries from the inventories (`S:11` says 11 were re-read; no source tree is in the workspace); `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, `CLAUDE.md`, `Makefile`, `pyproject.toml`, `install_core.py` citations (`S:11`, `S:23`, `S:25`, `S:52`, `S:150`, `S:183`); the spec's own claim of a 340-citation independent check (`S:285`). Where the inventory quotes such a file the quote is taken as the inventory's claim only.
- Guards: Guard Condition Boundary Table produced below. Pipeline Dimensional Analysis not triggered as a defect source: the one counted flow (43 commands into 10/27/6 into phases) conserves counts (verified above); the Task, Dispatch, report flow has no filter or fan-out stage whose count the spec assumes.

=== REQUIREMENTS ANALYSIS ===

### F-01 (CRITICAL, blocking) Phase 1 acceptance check cannot pass; it contradicts the load row, the phase plan and the recommended D3

- Expert: Wiegers (testability), Crispin (acceptance), Adzic.
- Grading sentence: An implementer who follows the stated text as written builds the P1 `## Unattended mode` section (naming `return-contract.yaml`) on all 37 commands of sections 3.1-3.2, including `load`, `pr-submit`, `implement`, `post-release`, and runs the live check on `load`, and that is wrong because the same spec says `load` has no report file, says pr-submit gets no change under its recommended D3(a), and puts the other commands' gate behaviour in later phases, so AC-1.1 and AC-1.2 cannot pass as written.
- Evidence (two stated texts that contradict):
  - `S:195` (AC-1.1) asserts that EVERY command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`; `S:159` makes P1 accept `--unattended` on every command in 3.1 and 3.2.
  - `S:112` says `load` needs "none (see note)" for the report and is "use it as a step inside another worker's brief, not as its own Task"; `S:265` (Decisions) rejects a report file for load as "an unrequested addition". AC-1.2 (`S:196`) then requires the 7.2 live check on "each P1 command", whose steps 3-4 (`S:182-183`) need a contract, and `load` is a P1 command (`S:159`).
  - `S:240` D3(a), the recommendation, says "no pr-submit changes in Phase 4", and `S:139` / `S:128` keep pr-submit a worker candidate "only if the user accepts D3"; AC-1.1 requires its section in P1 regardless. `S:154` says Phases 1-3 "need no user decision", yet P1 would pre-decide pr-submit, implement (D2) and post-release (D4), whose behaviour is scheduled at `S:162`.
  - Consequence beyond the test: after P1 these commands accept `--unattended` as a flag (`S:159`, "a no-op where a command has no gate") while their gates and outward defaults (`S:100`, `S:113`, `S:114`) are still live until P2/P4. A coordinator following `S:73` and passing `--unattended` then gets WC-2 / WC-9 (`S:60`, `S:67`) violated, with no stated rule that it must not dispatch them before their phase.
- Recommendation (narrow): scope AC-1.1 and AC-1.2 and the P1 flag to the commands whose rows are phase P1 plus the 3.1 commands; state that the flag and section for P2-P4 commands arrive in their own phase; drop `load` from the contract-section and live-check requirement (usage-line check only).
- Priority: High.

### F-02 (CRITICAL, blocking) The contract path rule (WC-4) contradicts the per-command rows, so the live check's `test -s <contract>` has no single path

- Expert: Wiegers, Fowler (interface consistency).
- Grading sentence: An implementer who follows the stated text as written builds the adversarial contract at `<output>/adversarial/return-contract.yaml` (the row's explicit fix) and the tdd/init-lite contract beside a `--output <file>`, and that is wrong because WC-4 and the live check require `<output-dir>/return-contract.yaml` in the directory the coordinator passed, so step 3/4 of the check (`test -s`, YAML key check on that path) fails for them.
- Evidence:
  - `S:62` WC-4: the contract is `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", "known before dispatch"; `S:182` step 3 requires the worker's report path to be "the WC-4 contract path"; `S:183` step 4 runs `test -s <contract>`.
  - `S:83` (adversarial): "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" and `S:198` AC-1.4 checks only that the skill "names one fixed path". The two paths differ (`<output>/` versus `<output>/adversarial/`). The inventory confirms the on-disk drift (`INV-A:60`: `.../adversarial/return-contract.yaml` and `.../adversarial/adversarial/return-contract.yaml`).
  - `S:87`, `S:90`: init-lite and tdd must be given `--output <file>`; a file has no `<output-dir>`, and WC-4 does not say whether the contract goes in the file's parent directory (which would collide when two workers write there, against WC-11 `S:69`).
  - `S:92`: workflow's contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml`; the id is derived at run time, so it is not "known before dispatch", and the P1 fix ("write the contract for pre-creation STOPs too") gives no location for a stop that happens before any package directory exists (`INV-B:272`: "Not written for pre-creation STOPs").
- Recommendation (narrow): state one rule for the contract location per brief shape (directory flag, file flag, no flag) and make the adversarial row, AC-1.4 and step 3-4 agree; say where the workflow pre-creation contract goes.
- Priority: High.

=== ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The core decision (Orca above, commands unchanged units, no Orca calls inside commands, `S:16`, `S:28-39`) is consistent with its evidence: R1 matches `CAPS:97-103`, R2 `CAPS:147-149`, R3 `CAPS:76,150`, R4 `CAPS:145`, R5 `INV-A:90`, `INV-B:285-286`. The spec states its own evidence gaps (`S:41-45`, `S:271-285`).

## Follow-up candidates (Medium and minor; none triggers a revision, none is in the Reviser brief)

Per the command, the session that ran the review asks the user once whether to open an issue for these; this sandbox has no user channel, so nothing was asked and no issue was created.

### Medium

- M-01 (MAJOR label, Medium grade; Nygard, Fowler). Tasklist unattended behaviour asks for a nested depth and a headless rule the spec itself lists as unverified. `S:122` makes tasklist pass `--unattended` to each reflect "so the headless rule applies" and says the fan-out runs "inside Claude Code's nesting limit, `INV-A:14`". But `S:280` (UNVERIFIED 9) assumes reflect does NOT treat a worker as headless, the headless rule auto-accepts remediation (`S:88`, `S:151`, `INV-B:109`), and `INV-B:209-210` mark who answers the offer and whether nested spawning works UNVERIFIED. The inventory's own advice was to drop `--remediate` in Stage 10.5 (`INV-B:215`); the spec instead auto-accepts it, which adds a workflow/task-builder hand-off below the reflect agents (worker, reflect, reviewer, remediation = 4 layers against the "three layers below" cited at `INV-A:14`). Needs a guess about which reading holds, so Medium. Also `S:88` and `S:122` leave a `needs_human_decision` HALT (`INV-B:209`) unmapped to blocked.
- M-02 (Medium; Crispin). The 7.2 step 5 pass test (`S:184`) says "search the transcript for `AskUserQuestion`. Pass: no `AskUserQuestion` call". A text search also matches loaded skill text (for example troubleshoot's "never AskUserQuestion", `INV-B:239`), which `worker-read --source transcript` can contain. The check should say "a tool call named AskUserQuestion".
- M-03 (Medium; Wiegers). The P0 live check cannot follow 7.2 step 1. `S:73` requires the brief to carry `--unattended`, `S:158` says P0 edits no command, and AC-0.4 (`S:194`) runs the check on unmodified commands, so `--unattended` is not a flag yet. AC-0.4 should say the P0 brief omits it.
- M-04 (Medium; Nygard). The spec states as fact that a command's own prompt "comes after readiness, so it does not fail `worker-start`" (`S:44`). The evidence is a wrapper prompt that appears before Claude starts (`CAPS:49`, `EVIDENCE.md:39` as quoted); Claude receives the task as an argv prompt (`CAPS:47`), so a command that asks at once may reach its question before the composer is the "fresh input box" Orca waits for. The inventory README line (`README:14`) frames the evidence more broadly. The statement should be UNVERIFIED until a P0 run shows it; P0 smoke runs use commands that rarely ask, so they would not close it. Add a P0 gate-trigger run (for example tdd with a bare topic).
- M-05 (Medium; Whittaker, Sequence Attack). `S:182` ends the coordinator loop "only" on `worker_done`, but WC-12 (`S:70`, `CAPS:67`) tells a fenced worker not to send `worker_done`, and a crashed worker never sends one. The check then never terminates. Orca allows leaving the wait on positive proof of exit (`CAPS:126`); the loop needs that exit.
- M-06 (Medium; Fowler). WC-4 needs the report location "known before dispatch" (`S:62`), while WC-6 (`S:64`) tells 17 commands with no resume flag to "write each run into a fresh output directory" (rows `S:99-125`). If the command makes the fresh directory, the path is not the one passed; if the coordinator passes a fresh one, the command rule is moot. State who creates the fresh directory.
- M-07 (Medium; Whittaker, Zero/Empty Attack). No rule for `--unattended` given with no output directory or file for commands that gain `--output` in P1/P2 (`S:99-125`). WC-4 writes to "the directory the coordinator passed" (`S:62`) with no fallback and no refusal. `/sc:spec-panel`'s own definition refuses before any work and prints in chat only; the spec has no equivalent, so an implementer picks a default (likely the working directory, against SA-3 `S:148`). Also the switch lacks the "standalone argument token outside quoted content" rule, so `"... --unattended ..."` inside a quoted topic could switch a command (`S:51`).
- M-08 (Medium; Whittaker). The status vocabulary is closed at four values (`S:62`, `S:262`) and the live check asserts it (`S:183`), but WC-5 (`S:63`) maps only "report says failed/blocked, or no report exists" and "otherwise" success. A present contract that is malformed or carries an unknown status maps to `succeeded`.
- M-09 (Medium; Crispin). The additive-edit check AC-C5 (`S:176`) only diffs `src/superclaude/commands/<name>.md`, but most gate text lives in skills and agents (`S:84-125` evidence columns, for example `sk/tdd/SKILL.md:52-61`, `sk/sc-tasklist-protocol/SKILL.md:1614-1631`). The spec never says whether the skill files are edited. A command-file "blocked" section may not override a skill instruction to ask (`INV-B:219`). SA-1 / SA-4 are therefore uncovered where the standalone-behaviour risk is highest.
- M-10 (Medium; Nygard). AC-C1 (`S:172`) greps `src/superclaude/core` for `orca orchestration|worktree|terminal|agent` and must print nothing in every phase including P0, but P0 adds a coordinator-facing "Orca section" to `HOW-WE-WORK.md` and writes `WORKER-CONTRACT.md` (`S:158`), and SA-2 (`S:147`) allows an Orca mention "as an example of a caller's question channel inside the contract file". Such text matches the grep. The allowance and the check conflict unless the files avoid the literal `orca orchestration`; say so.
- M-11 (Medium; Hohpe, UNVERIFIED). E5 / `S:25` claim no primitive other than `ccsession-tag` mentions Orca and that there are 43 commands (`S:76`). The host session's skill listing (not a workspace file, so UNVERIFIED here) also names `sc:issue` (creates an Orca worktree and launches an agent), `sc:graph` and `sc:impact`, which are not in either inventory (`INV-A:3`, `INV-B:3`). If they exist in `src/superclaude/commands/`, E5, the 43 count and AC-C1 are wrong for them. Re-run the grep and the command count at P0.
- M-12 (Medium; Crispin). `S:44` / WC-10 assume heartbeat gaps stay under 5 minutes when each wait is at most 4 minutes (`S:68`, `S:210`). pr-submit's iteration is poll runtime plus a sleep of at least the poll interval (`S:68`, `S:114`); the poll runtime is UNVERIFIED (`S:283`), so 4 minutes plus runtime can exceed 5. Listed as a guard GAP below; needs a measured bound or a smaller wait.

### Minor (notes)

- N-01. WC-5 requires a one-sentence body opening (`S:63`); `CAPS:73` quotes the guide's three-sentence executive summary. Consistent in intent, different in wording.
- N-02. Section 1.2 E3 and `S:11` rely on files not checkable here (UNVERIFIED list above); the independent-check note `S:285` is likewise a claim, not a result.
- N-03. `S:182` allows an `ask` answer only "with an answer the brief or the person has given"; D2(b) later has the coordinator relay a person's words (`S:235`). Consistent, but the loop text could point to D2.

## Guard Condition Boundary Table

Guards found: readiness limit, nesting depth, heartbeat/wait bound, confidence threshold (`task`), `--monitor` ordinal, status vocabulary, retry circuit breaker, `--unattended` switch. Classes left out are named.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| readiness limit | S:59 (WC-1) | Typical | prompt falls back at 30 s | pass | worker-start succeeds (`CAPS:49`) | OK |
| readiness limit | S:59, S:44 | Legitimate Edge Case | command asks at once via argv prompt | unknown | S:44 asserts "after readiness"; evidence is wrapper-only | GAP (M-04) |
| nesting depth | S:66 (WC-8), S:33 | Maximum/Overflow | depth > 1 | refused | `nested_worker_depth_exceeded` | OK |
| nesting depth | S:122 | Maximum/Overflow | worker, reflect, reviewer, remediation (4 layers) | unknown | S:122 says "inside the limit" | GAP (M-01) |
| heartbeat gap | S:68 (WC-10) | Maximum/Overflow | wait of 240 s plus tool runtime | maybe > 300 s | S:283 lists runtime UNVERIFIED | GAP (M-12) |
| heartbeat gap | S:68 | Zero/Empty | no tool call in flight | pass | heartbeat every 5 min | OK |
| status vocabulary | S:62-63 | Sentinel Value Match | status outside the four values / malformed file | unknown | WC-5 maps only "failed/blocked/no report" | GAP (M-08) |
| status vocabulary | S:63 | Legitimate Edge Case | `partial`; audit verdict FAIL | pass | mapped to `succeeded`, stated in body | OK |
| `--unattended` switch | S:51, S:159 | Sentinel Value Match | the token inside quoted topic text | unknown | no quoting rule | GAP (M-07) |
| `--unattended` + output | S:62 | Zero/Empty | flag given, no output dir/file | unknown | no refusal or default stated | GAP (M-07) |
| `--unattended` + opt-in flag | S:83-91 | Divergence (both apply) | `--unattended --interactive` on adversarial/brainstorm/release-split | unknown | only "never --interactive" in the brief; roadmap/cleanup/improve refuse (S:118,103,110) | GAP, minor |
| confidence (task) | S:121 | Boundary | 0.70 | `< 0.70` blocked | at exactly 0.70 the existing rule applies (`INV-B:199`) | OK |
| `--monitor` ordinal | S:114 | Typical / boundary | `--monitor 1` | refused under unattended | blocked | OK |
| `--monitor` ordinal | S:114 | Zero/Empty | `--monitor 0` | unknown | not stated | GAP, minor (no outward change implied) |
| circuit breaker | S:64 (WC-6), `CAPS:80,116` | Maximum/Overflow | 3 failed starts | Task failed | blocked-then-retry loop | OK |
| `ask` timeout | S:61 (WC-3) | Maximum/Overflow | timeout | pending | resume same ID (`CAPS:60`) | OK |

Classes not given a row: One/Minimal for the readiness limit and depth (no minimal value exists for a fixed constant).

Every GAP above is Medium or minor: none names a concrete wrong outcome an implementer would produce without a further guess, so none is blocking (FR-8/FR-9 graded per `command.md:259`).

## Summary

- Blocking: 2 (F-01, F-02), both about acceptance criteria that cannot pass as written. Medium: 12 (M-01 to M-12). Minor: 3.
- Not found: any contradiction in the core decision or in the 10/27/6 inventory counts; the inventory line citations checked resolved correctly.

## Reviser brief

Blocking finding ids: F-01, F-02. The reviser reads this report, not the command. Rules: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on every added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id; leave Medium and minor findings alone; return the candidate once and do not award yourself a PASS. Review count: this is review 1 of 3; a re-review with `--re-review` and `--baseline` follows, and at `review: 3` with an open blocker the loop escalates to the user instead.

verdict: FAIL
