review: 1 of 3

# Spec-panel review, round 1: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, 285 lines, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review of the full document; no `--re-review`)
- lint: `.dev/orca-command-refactor/review/lint-1.md`, sha256 of the reviewed candidate matches, `Checks: REF. Findings: 0` (lint-1.md:1-5)
- reviewer model actually used: claude-sonnet-5-5
- input type: not a TDD (9 numbered headings, no TDD frontmatter, no "Technical Design Document" string, score 0 < 5) and not a PRD; no `target_release` question applies
- mode flags: no `--unattended`, so no return-contract file is written; no `--improve`, so no improved spec; the candidate is not edited (brief: write only this file)
- panel (fixed order): Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe (requirements + architecture focus sets)
- citation convention: `S:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. Every `src/`, `~/.claude`, `EVIDENCE.md`, codegraph and Orca-installation path is outside this workspace, so a claim resting only on such a path is UNVERIFIED unless an inventory line quotes it.

## Lint disposition
lint-1.md reports zero findings, so there is no lint id to confirm or dismiss. The REF check does not cover acceptance criteria, so nothing in the findings below comes from lint.

## What was covered
- All of S:1-285 read in full, plus README.md, all three inventories (full) and the command definition.
- Requirements and architecture focus: WC-1..WC-12, SA-1..SA-6, sections 1, 3, 4, 6, 9.
- Every acceptance check one by one: AC-C1..C5, live-check steps 1-7 (S:180-186), AC-0.1..0.4, 1.1..1.4, 2.1..2.5, 3.1..3.4, 4.1..4.3, each tested against every command and phase it covers (table below).
- Counts reconciled: 43 = 10 + 27 + 6 (S:76); the 27 needs-change commands split P1 9 + P2 11 + P3 4 + P4 3 = 27 across S:99-125 and S:159-162; the 10 ready commands match S:82-92; the inventories give 21 + 22 commands (INV-A:3, INV-B:3) and 5+5, 13+14, 3+3 (INV-A:73, INV-B:278). No count mismatch found.
- Not covered: whether any cited `src/` line says what the spec says it does (checked only through the inventory lines that quote it); runtime facts about Orca (CAPS rows are the only evidence).

## Acceptance-check audit (can it pass as written, for every command and phase it covers?)

| Check | Can pass as written? | Reason (cite) | Finding |
|---|---|---|---|
| AC-C1 grep for Orca calls (S:172) | Yes at today's baseline (E5, S:25, UNVERIFIED run); conflicts with SA-2 later | S:147 allows an Orca mention inside the contract file, S:158 adds an Orca section to HOW-WE-WORK.md, S:172 greps all of `src/superclaude/core` for `orca orchestration` etc. | F-13 (Medium) |
| AC-C2 `make verify-sync` (S:173) | Yes | none | none |
| AC-C3 pytest baseline (S:174) | Yes | covers only `tests/skills/`; core-install tests elsewhere are not run (UNVERIFIED) | F-10 note |
| AC-C4 no staged `.claude/` (S:175) | Yes (checks staged files only) | none | none |
| AC-C5 additive diff (S:176) | Passes, but vacuously | `master...HEAD` sees only commits, and `/sc:implement` makes none (INV-A:51); regex `^-[^-]` ignores a deleted `- ` bullet | F-10 (Medium) |
| Live 1 task-create + worker-start (S:180) | Yes | `CAPS:46` | none |
| Live 2 worker-show agentWait (S:181) | Yes; may conflict with WC-3 `ask` | S:61 | F-8 (Medium) |
| Live 3 one worker_done, outcome matches contract, report path is WC-4 path (S:182) | No in P0; No for load; undefined for commands without a WC-4 directory | S:79, 159, 194; S:112; S:62, 73 | F-3, F-4, F-2 |
| Live 4 `test -s <contract>` + yaml assert (S:183) | No where `<contract>` is undefined; status set may not fit existing contracts | S:62, 87, 90, 261 | F-1, F-2, F-9 |
| Live 5 transcript has no AskUserQuestion call (S:184) | Yes (read as a tool call, not a text match) | the contract text itself names the tool (S:60) | none |
| Live 6 git status (S:185) | Yes | "documented artifacts" never listed per command | N-3 |
| Live 7 release + reclaimable list (S:186) | Yes | `CAPS:107-113` | none |
| AC-0.1 KNOWN_CORE_FILES (S:191) | Yes | UNVERIFIED target file, S:52 | none |
| AC-0.2 cmp mirror + level test (S:192) | Yes | none | none |
| AC-0.3 no changed routing row (S:193) | Passes, vacuously if uncommitted | same as AC-C5 | F-10 |
| AC-0.4 three live smoke runs (S:194) | No | steps 1-3 demand a WC-4 contract and `--unattended` that P0 does not have | F-3 |
| AC-1.1 test asserts section in every 3.1-3.2 command (S:195) | No for load | S:112, S:265 | F-4 |
| AC-1.2 live check on each P1 command with `--output <dir>` (S:196) | No for load, cleanup-audit, index-repo | S:112, 85-86 | F-4, F-2 |
| AC-1.3 plain run writes no contract (S:197) | Yes | uses analyze; "scratch worktree" conflicts with the Orca-only worktree rule, which is outside this workspace (UNVERIFIED) | N-2 |
| AC-1.4 adversarial names one fixed path (S:198) | Ambiguous | S:83 vs S:62 | F-2 |
| AC-2.1 one assertion per gate (S:199) | Yes | none | none |
| AC-2.2 gate-trigger run per P2 command expects blocked (S:200) | No for auggie-review, research, tasklist, reflect, cleanup, improve; tdd contract path undefined | S:100, 116, 122, 88, 103, 110, 87, 90 | F-5, F-1 |
| AC-2.3 happy path per P2 command (S:201) | No for research, recommend, review-translation, task | no contract directory exists | F-2 |
| AC-2.4 gh counts unchanged (S:202) | Unreliable | default page size 30, bots can add reviews | F-14 (Medium) |
| AC-2.5 manual SA-1 check (S:203) | Yes | none | none |
| AC-3.1 name/flag reconciliation test (S:204) | Yes | none | none |
| AC-3.2 roadmap starts fresh in an existing dir (S:205) | Yes; clashes with WC-6 | S:64 | F-17 note |
| AC-3.3 default dir + report (S:206) | Yes | none | none |
| AC-3.4 save, hashes unchanged (S:207) | Yes, weakly | "(where present)" is vacuous when the files are absent; two timestamps may collide; no contract directory for save | F-2, F-17 |
| AC-4.1 implement halt (S:208) | Yes once D2 is answered; contract "beside the ledger" has no known path | S:109 | F-2 |
| AC-4.2 post-release no outward action (S:209) | Partly | no check for install/VM; the flags and the pre-tag choice are unnamed | F-15 (Medium) |
| AC-4.3 pr-submit heartbeats <= 5 min, no call > 240 s (S:210) | Only on a PR with no verified finding | the finding path runs sc:troubleshoot with 2-4 agents in one call (INV-B:91) | F-6, F-15 |

## === REQUIREMENTS ANALYSIS ===

### Blocking findings

**F-1 [MAJOR, blocking] WC-4 puts the contract in a directory, while two commands and an acceptance check pass a file.**
- Expert: Wiegers (traceability), Adzic (example). Priority High. Quality impact: Consistency -2, Testability -2.
- Texts: S:62 says the contract is `<output-dir>/return-contract.yaml`, "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". S:87 says init-lite is briefed with `--output <file>`; S:90 says the same for tdd; S:200 runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked`"; S:183 runs `test -s <contract>`.
- Wrong outcome: an implementer who follows the stated text builds, for tdd and init-lite, a contract path of `<TDD file>/return-contract.yaml`, a path under a regular file that cannot be created, and AC-2.2 has no `<contract>` it can test. The two texts (directory versus file) contradict, and no text says where the contract goes instead.
- Recommendation: narrow WC-4 to say where the contract goes when `--output` is a file (for example beside it, `<file-dir>/return-contract.yaml`) and name that path in the tdd and init-lite rows and in AC-2.2.

**F-2 [MAJOR, blocking] WC-4's "directory the coordinator passed, known before dispatch" is false for several commands, and the live check depends on it.**
- Expert: Wiegers, Fowler (interface consistency). Priority High. Quality impact: Testability -2, Completeness -1.
- Texts: S:62 and S:73 say the contract is `<output-dir>/return-contract.yaml` and "the output directory, so the report path is known before dispatch". Contradicting rows: adversarial `<output>/adversarial/return-contract.yaml` (S:83); workflow `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92), whose `<id>` is made by the run (INV-B:272); implement "beside the ledger `progress.md`" (S:109; INV-A:51 gives `.dev/implement/<slug>/progress.md`); cleanup-audit and index-repo have a fixed location and no output flag (S:85-86); research (S:116), recommend (S:115), review-translation (S:117), task (S:121) and save (S:119) name a contract but no flag that sets its directory, and S:159 (P1) adds output flags only for analyze, build, business-panel, design, document, explain, index, test.
- Wrong outcome: live step 3 requires "its report path is the WC-4 contract path" (S:182) and AC-2.3 requires 7.2 to pass "with every required flag" (S:201). For research the implementer builds a command with no flag that places the contract, so the coordinator cannot give the path in the brief and step 3 fails; for adversarial the implementer must choose between `<output>/return-contract.yaml` (WC-4) and `<output>/adversarial/return-contract.yaml` (S:83), and AC-1.4 asks for "one fixed path" (S:198).
- Recommendation: state one rule (contract path = the coordinator-passed directory, or a flag the command gains for it) and list the one added flag for each command above, or state that its report path is read from `worker_done` and remove the "known before dispatch" claim for those commands.

**F-3 [MAJOR, blocking] AC-0.4 requires, in P0, a contract and a flag that P0 does not have.**
- Expert: Adzic, Nygard. Priority High. Quality impact: Testability -2.
- Texts: S:159 puts "the WC-4 contract in unattended mode" and the `--unattended` flag in P1; S:79 says ready commands "report the named file until Phase 1 adds the contract"; S:73 says the brief states "the exact command line including `--unattended`"; S:194 runs the three smoke commands without `--unattended`, says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file"; S:182 (step 3) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Wrong outcome: an implementer runs AC-0.4 as written. For `/sc:troubleshoot` the existing report is `REPORT.md` (S:91), which is not a WC-4 contract and has no WC-4 `status`; step 3 cannot pass. The same holds for workflow (no `command` field, S:92) and adversarial (contract filename not fixed, S:83). Only step 4 was relaxed.
- Recommendation: relax step 3 for P0 the way step 4 was relaxed (outcome matches the command's own verdict, report path is the named existing file), and drop `--unattended` from the P0 brief.

**F-4 [MAJOR, blocking] AC-1.1 and AC-1.2 demand a contract and a worker run for `/sc:load`, which the spec says has none and is not a Task.**
- Expert: Wiegers. Priority High. Quality impact: Consistency -1, Testability -1.
- Texts: S:112 (load row): report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)"; S:265: "a report file would be an unrequested addition"; S:195 (AC-1.1) asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"; S:196 (AC-1.2) runs the 7.2 live check "on each P1 command with `--unattended --output <dir>`"; S:76 says every changed command gains the section; S:159 lists load as a P1 command.
- Wrong outcome: an implementer who follows AC-1.1 gives load a section naming `return-contract.yaml` (or fails the test), which the load row and S:265 forbid; AC-1.2 needs a load Task with a contract and `--output`, which the row says does not exist.
- Recommendation: exclude load from AC-1.1 and AC-1.2 by name, as the row already does, and say its section (if any) names no contract.

**F-5 [MAJOR, blocking] AC-2.2 expects a `blocked` outcome from every P2 command, but several resolve their gate without blocking.**
- Expert: Adzic, Whittaker (Divergence Attack: the condition at the boundary between "default" and "blocked"). Priority High. Quality impact: Testability -2.
- Texts: S:60 gives three resolutions, (a) default, (b) flag, (c) blocked; S:200 requires for "each P2 command" a "gate-trigger run" ending `worker_done --outcome failed` with "`status: blocked` with a non-empty `blocked_question`"; S:160 lists the P2 commands. Rows with no blocked branch: auggie-review turns posting and the offer off (S:100); research pins `--strategy planning` (S:116); tasklist passes `--unattended` to reflect (S:122); reflect follows its headless auto-accept rule (S:88); cleanup and improve apply the allowed items and list the rest (S:103, 110).
- Wrong outcome: an implementer builds each of those commands exactly as its row says, and no input exists that makes it write `status: blocked`, so AC-2.2 cannot pass for them.
- Recommendation: limit AC-2.2 to the P2 commands whose row has a blocked resolution (cli-eval, cli-portify, recommend, review-translation, spec-panel, task, release-split, tdd, troubleshoot, cleanup/improve only for the refused `--interactive`) and give the rest an AC that checks their default.

### Follow-up candidates (Medium)

**F-6 [Medium] WC-10 cannot be met for Agent-tool fan-out.** S:68 requires a heartbeat every 5 minutes and splitting any single tool call over 5 minutes into waits of at most 4 minutes; S:65 forbids subagents from sending lifecycle messages; S:24 keeps Agent-tool fan-out unchanged. A synchronous fan-out call (cleanup-audit waves of 7-8 agents, INV-A:42; tdd, INV-B:221; troubleshoot Tier 2, INV-B:241) can block the top-level session longer than 5 minutes and cannot be split. Whether a missed heartbeat matters is UNVERIFIED (`CAPS:130`). Needs a guess about the consequence, so Medium. Expert: Nygard.

**F-7 [Medium] "Refused" is a fourth resolution that WC-2 does not define.** S:60 allows default, flag or blocked; rows say "refused" for business-panel socratic (S:102), cleanup `--interactive` (S:103), explain interactive (S:108), pr-submit `--monitor 1` (S:114), roadmap `--interactive` (S:118), test `--watch` (S:123). Whether a refusal writes a contract, with which `status`, and which `--outcome` is not stated (WC-5, S:63, maps only failed/blocked/no report). A requirement the document never states. Expert: Whittaker (Sentinel/Zero attack).

**F-8 [Medium] WC-3 lets the worker `ask`; AC-2.2 and live step 3 expect `worker_done`.** S:61 says the session "may instead ask the coordinator once"; S:182 waits for `worker_done,escalation,question` but passes only on "exactly one `worker_done`"; S:200 expects `--outcome failed`. Which path the worker takes depends on the brief, and S:73 does not say. Needs a guess about the worker's choice. Expert: Nygard.

**F-9 [Medium] Existing contracts may not use the four WC-4 status values.** S:62 says commands with a contract "keep their fields and add the missing ones", S:183 asserts `status` is one of four values, S:261 says four commands already write `return-contract.yaml`. The existing status vocabularies of workflow, brainstorm, reflect and adversarial are not recorded in INV-A:35, 39 or INV-B:36, 52, 272 (UNVERIFIED). If any differs, "keep" and "one of four" disagree. Expert: Newman. Also note: no `contract_version` field (minor, N-4).

**F-10 [Medium] AC-C5 and AC-0.3 can pass without checking anything.** `git diff -U0 master...HEAD` compares commits (S:176, 193) while `/sc:implement` makes no commit (INV-A:51) and each phase runs under it (S:164); the pattern `-[^-]` also skips a deleted markdown bullet (`- item` appears as `-- item`). Adding `--unattended` to an existing Usage or `argument-hint` line would fail the check unless it goes on a new line (SA-4, S:149). AC-C3 runs only `tests/skills/` (S:174), so a core-install test elsewhere could break unseen (UNVERIFIED). Expert: Crispin.

**F-11 [Medium] The flag is accepted everywhere in P1, but gates convert in P2-P4.** S:159 accepts `--unattended` on "every command in sections 3.1 and 3.2"; S:100 turns off auggie-review posting only in P2; S:109, 113, 114 convert implement, post-release, pr-submit in P4; WC-9 (S:67) says outward defaults are off under `--unattended`. Between P1 and P2 a brief using the flag on auggie-review would still post. Needs a guess that someone dispatches it in that window. Expert: Nygard.

**F-12 [Medium] Phase text contradicts its own rows.** S:154 says phases 1-3 need no user decision, but D4 (S:244) lists auggie-review `--post-pr` and task `commit`/`push`, both P2 (S:100, 121, 160). S:159 says in P1 "no person gate is involved", but P1 rows resolve refusals (S:102, 108, 123). Expert: Wiegers.

**F-13 [Medium] AC-C1 and SA-2 disagree on what the contract file may say.** S:147 allows an Orca mention "inside the contract file"; S:172 greps `src/superclaude/core` (where `WORKER-CONTRACT.md` and the new HOW-WE-WORK Orca section live, S:52, 158) for `orca orchestration` and similar and requires no output. If either file names `orca orchestration ask`, AC-C1 fails. Not forced by the text. Expert: Fowler.

**F-14 [Medium] AC-2.4 can mis-report.** `gh api .../reviews --jq length` and `.../comments --jq length` (S:202) read the first page (30 entries) only, and a bot review landing between the two reads changes the count (the Augment and Codex reviewers of this fork's PRs are named in the project instructions, not in the workspace, so UNVERIFIED here). Expert: Crispin.

**F-15 [Medium] AC-4.2 and AC-4.3 are under-specified.** AC-4.2 (S:209) names no check for install or VM steps, no authorization flag names (WC-9, S:67, says "the command's own explicit flag"; INV-B:85 shows post-release has none), and omits the "explicit pre-tag choice" of S:113. AC-4.3 (S:210) needs every call under 240 s while the poll-script runtime is UNVERIFIED (S:283, item 12) and the troubleshoot path is long (INV-B:91). Expert: Adzic.

**F-16 [Medium] No requirement says how a worker runs a slash command.** S:16 and WC-7 (S:65) say the worker "runs the command directly", but Orca passes the task in the prompt behind a preamble (`CAPS:47`, `CAPS:73-76`), and a slash command normally needs to start the message. Whether the worker invokes it through the Skill tool, as the repo routes `/sc:` commands, is not stated; the P0 smoke runs (S:194) test the outcome but no text defines the mechanism. Expert: Cockburn.

**F-17 [Medium] Requirements without any acceptance check.** WC-6 (resume or fresh dir; only AC-3.2, which starts fresh in the same directory, S:205), WC-10 splitting for cli-eval, WC-11 for all but save, WC-12. S:154 and S:167 say a phase passes only when its checks pass, so these ship unchecked. Expert: Crispin.

**F-18 [Medium] "Paid external run" is undefined.** S:67 turns off any default that "calls a paid external run"; research and review-translation call Tavily by default (INV-B:134, 144) and cli-eval `run` executes `uv run superclaude eval run` (INV-A:44), and none of their rows turns anything off. Expert: Wiegers.

**F-19 [Medium, UNVERIFIED] Inventory completeness.** S:76 says the 43 commands in `cmd/` are all of them. The reviewing session's installed command list also shows `sc:graph`, `sc:impact` and `sc:issue`; neither inventory covers them (INV-A:3, INV-B:3), and `sc:issue` is described as creating an Orca worktree, which would contradict E5 (S:25) and AC-C1's empty baseline. This list is not a file in the workspace, so it is UNVERIFIED; the spec author should check `ls src/superclaude/commands`.

### Minor notes
- N-1: S:172 shows `\|` inside the code span (table escaping); copied raw into a shell, the alternation breaks. Say "pipe" once or move the command out of the table.
- N-2: AC-1.3 (S:197) says "scratch worktree"; this repo makes worktrees through Orca only (outside the workspace, UNVERIFIED).
- N-3: live step 6 (S:185) says "documented artifacts" with no per-command list.
- N-4: WC-4 has no `contract_version`, while workflow's contract is versioned 1.1 (INV-B:272).
- N-5: E3 (S:23) cites `invocation_method: "skill-direct"` as proof it worked, while S:43 says the same run proves only the nested route; read together they are consistent only if "skill-direct" is a subagent call. Say so in E3.
- N-6: `partial` maps to `--outcome succeeded` (S:63, 263); a coordinator reading `check` output alone cannot tell it from a full success (S:73 requires opening the contract).

## === ARCHITECTURE ANALYSIS ===

Verdict on the architecture: the central decision (Orca coordinates, commands stay the units of work) holds up against the rejected alternative: R1 (depth 1, `CAPS:97-103`), R2 (`CAPS:147-149`), R3 (`CAPS:150`) and R5 (INV-A:90) each rest on an inventory line. The weak point is S:43 (no direct-route run exists), which the spec states plainly and tests in P0. No finding here is architectural-blocking apart from F-1..F-5, which concern the contract interface (Fowler: one interface, WC-4, is described by three different path rules).

Whittaker attacks (only those producing a finding or a table GAP):
- I can break this specification by **Divergence Attack**. The invariant at **S:60 / S:200** fails when **a gate has a default resolution instead of a blocked one**. Concrete attack: `/sc:research "x" --unattended --output d` runs to completion with `--strategy planning`; AC-2.2 expects `status: blocked`; state before: no contract; state after: `status: succeeded`; the check fails. Severity MAJOR, F-5.
- I can break this specification by **Zero/Empty Attack**. The invariant at **S:62** ("contract on every outcome, including stops before any other output exists") fails when **`--output` names a file or is absent**. Concrete attack: `/sc:tdd "auth" --unattended --output docs/T.md` with a bare topic; before: no `docs/T.md`; WC-4 puts the contract at `docs/T.md/return-contract.yaml`; after: no contract anywhere. MAJOR, F-1.
- I can break this specification by **Sequence Attack**. The invariant at **S:194** (P0 runs before P1) fails when **step 3 runs before the contract exists**. Concrete attack: run `/sc:troubleshoot` as in AC-0.4; before: no WC-4 contract; step 3 requires one; after: step 3 fails whatever the worker does. MAJOR, F-3.
- I can break this specification by **Accumulation Attack**. The invariant at **S:68** (heartbeat every 5 minutes) fails when **one synchronous fan-out call runs 12 minutes**. Concrete attack: cleanup-audit with 400 files at 50 files per agent (INV-A:42) runs a wave of 8 agents in one call; before: last heartbeat t=0; after: next possible heartbeat t=12 min. Medium, F-6.

## Guard Condition Boundary Table

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-10 wait size | S:68 | Zero/Empty | none | n/a | left out: a call of zero length cannot block | OK |
| WC-10 wait size | S:68 | Typical | poll wait <= 4 min | within cadence | heartbeat between waits | OK |
| WC-10 wait size | S:68 | Maximum/Overflow | one fan-out call > 5 min | exceeds cadence | not specified; subagents may not send (S:65) | GAP (F-6, Medium) |
| WC-10 wait size | S:68, S:266 | Legitimate Edge Case | wait of exactly 5 min | not split | 4-min margin chosen (S:266) | OK |
| WC-5 outcome map | S:63 | Zero/Empty | no report file | no report | `--outcome failed` | OK |
| WC-5 outcome map | S:63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome map | S:63 | Sentinel Value Match | a status outside the four values (existing contract) | unmatched | not specified | GAP (F-9, Medium) |
| WC-5 outcome map | S:63, S:102-123 | Sentinel Value Match | "refused" (no contract) | unmatched | not specified | GAP (F-7, Medium) |
| WC-5 outcome map | S:63 | Legitimate Edge Case | audit verdict FAIL, `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-4 contract location | S:62 | Zero/Empty | stop before any output, directory not created | no directory | "written on every outcome" but path undefined for file-valued `--output` | GAP (F-1, blocking) |
| WC-4 contract location | S:62, S:83, S:92 | Typical | `--output <dir>` | directory known | `<output-dir>/return-contract.yaml`, but adversarial and workflow differ | GAP (F-2, blocking) |
| WC-2 gate resolution | S:60 | Typical | gate with a default | default applies | default | OK |
| WC-2 gate resolution | S:60, S:200 | Legitimate Edge Case | gate with no blocked branch | never blocked | AC-2.2 expects blocked | GAP (F-5, blocking) |
| WC-1 readiness limit | S:59 | Maximum/Overflow | launch prompt > 45 s | readiness fails | fallback "well inside" 60 s; `EVIDENCE.md` cited via `CAPS:49` | OK |
| Nesting depth 1 | S:33 | One/Minimal | worker calls `worker-start` | refused | `nested_worker_depth_exceeded` (`CAPS:99`) | OK |
| SA-3 new-file rule | S:148 | Legitimate Edge Case | command already has `--output`, no `--unattended` | no new file | same files as today | OK |

Classes left out when they cannot occur: One/Minimal and Sentinel for WC-10 (no value of length one or special value exists); Zero and Maximum for the depth fence (the setting is a whole number >= 1, `CAPS:100`).

## Quantity Flow (Pipeline Dimensional Analysis)
```text
[43 commands: INV-A 21 + INV-B 22] --> [classify] --> [10 ready (S:82-92)]
                                                  --> [27 needs change (S:99-125)] --> P1 9 | P2 11 | P3 4 | P4 3
                                                  --> [6 coordinator-only (S:131-137)]
[10 ready] --> P0 smoke 3 (S:194); P1 fixes 4 (adversarial, cleanup-audit, index-repo, workflow); P2 gate rows 4 (reflect, release-split, tdd, troubleshoot); no phase work 2 (brainstorm, init-lite)
```
Counts conserve at every stage (43 = 10 + 27 + 6; 27 = 9 + 11 + 4 + 3; the 10 ready commands = 4 P1 fixes + 4 P2 gate rows + 2 with no phase work; the 3 smoke runs reuse commands from those sets). No dimensional mismatch.

## Quality assessment (0-10)
Clarity 7, Completeness 6, Testability 4, Consistency 5. Overall 5.5. The decision and the per-command inventory are strong; the acceptance criteria are where it fails.

## Expert consensus
- All experts agree the decision (Orca on top, commands as workers) is supported and the rejected alternative is correctly excluded.
- Wiegers, Adzic and Crispin agree the live check (S:180-186) cannot be applied unchanged to every command; five checks need narrowing (F-1..F-5).
- Fowler and Newman agree WC-4 is the one shared interface and should have one path rule, not three.
- Disagreement: Nygard would grade F-6 and F-11 blocking; held at Medium because each needs a guess about the consequence (Orca's heartbeat use is UNVERIFIED, `CAPS:130`).

## Follow-up candidates (summary list)
F-6 to F-19 above and notes N-1 to N-6. Per the command, the session that ran this review asks the user once per loop whether to open an issue for these; no user is available in this sandbox, so the question is not asked and no issue is created.

## Improve step
Not run: the brief assigns only this report file, and the command lists "modify specifications without explicit user consent" under Will Not. No revised specification is written.

## Reviser brief
Blocking finding ids: F-1, F-2, F-3, F-4, F-5. The reviser reads this report, not the command. Rules: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id. Leave F-6 to F-19 and the notes alone; they never trigger a revision and do not appear here.
- F-1: S:62 (WC-4 directory) versus S:87, S:90, S:200 (`--output <file>`); wrong outcome: contract path under a regular file for tdd and init-lite.
- F-2: S:62, S:73 (directory known before dispatch) versus S:83, S:92, S:109, S:85-86, S:115-117, S:119, S:121; wrong outcome: step 3 and AC-2.3 have no contract path for research, recommend, review-translation, task, save and conflicting paths for adversarial and workflow.
- F-3: S:182 versus S:79, S:159, S:194; wrong outcome: AC-0.4 requires a WC-4 contract in P0.
- F-4: S:195, S:196 versus S:112, S:265; wrong outcome: load gets a contract and a Task it is specified not to have.
- F-5: S:200 versus S:100, S:116, S:122, S:88, S:103, S:110; wrong outcome: no input makes those commands write `blocked`.

verdict: FAIL
