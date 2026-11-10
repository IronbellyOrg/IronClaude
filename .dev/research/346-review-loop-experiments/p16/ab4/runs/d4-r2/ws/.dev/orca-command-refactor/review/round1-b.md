review: 1 of 3

# /sc:spec-panel critique, round 1: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (285 lines; the same hash is recorded in `review/lint-1.md:1`)
- baseline: none given (first review of the full document); prior report: none
- reviewer model actually used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full. One reviewer only: the brief did not ask for two first reviews, so the MERGE rule does not apply and ids are the reviewer's own (F1..F5 blocking, FU-1.. follow-up).
- citation keys: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`. Only these inventory files and the candidate exist in the sandbox. Every citation to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `/opt/Orca/...` or an Orca guide is UNVERIFIED here and is used only as quoted by an inventory line.
- improve step: not run (critique review only; the candidate is not edited).

## 0. Lint evidence
`review/lint-1.md:3-5`: Checks REF, Findings 0, "No findings." No lint id exists, so none is confirmed or dismissed. A lint result of zero does not clear the candidate: the lint checks references only, and every finding below is a contradiction or an unpassable check, which REF does not examine.

## 1. What was covered
- Every requirement WC-1..WC-12 (SPEC:57-70), SA-1..SA-6 (SPEC:146-151), every row of sections 3.1, 3.2 and 4 (SPEC:81-137), the phases (SPEC:156-162), all 25 acceptance checks and the 7 live-check steps (SPEC:169-210), the non-goals, D1-D5 and the UNVERIFIED list.
- The counts: 43 commands = 21 + 22 (`INV-A:3`, `INV-B:3`); 10 ready + 27 needing change + 6 coordinator-only agrees with the inventories (`INV-A:73`: 5/13/3; `INV-B:` summary: 5/14/3). I counted the 27 rows of section 3.2 (SPEC:99-125) and the 10 rows of 3.1 (SPEC:83-92): both match.
- Each ready/needs-change row was compared with the inventory row it cites (`INV-A:35-55`, `INV-B:31-52`, per-command notes). Verdicts agree. Where a row asserts a file location, I checked it against the inventory.
- Not covered: the real command, skill and Orca files (absent from the sandbox). Claims that depend on them are listed in section 9 as UNVERIFIED.

## 2. Panel notes (critique mode, focus requirements + architecture)
- **Wiegers (requirements lead)**: the contract rules are mostly testable, but WC-4 fixes the report location as `<output-dir>/return-contract.yaml` (SPEC:62) while the rows of section 3 give at least five different locations and three commands that have no directory-valued output at all. A requirement that cannot be located cannot be verified (F2, F3).
- **Adzic**: the live check (SPEC:178-186) is the only executable specification. Run against the P0 smoke commands it contradicts the phase it belongs to (F1); run against "gate" commands it demands a blocked outcome that six commands never produce (F5).
- **Cockburn**: the primary actor, the coordinator, gets a clear brief template (SPEC:72-73). The secondary actor, the worker session, is never told how it runs a slash command "directly" (FU-5).
- **Fowler (architecture lead)**: the decision itself (Orca on top, commands unchanged except a flag, a report file and a resume rule; SPEC:13-16, 28-39) is coherent and its evidence is stated honestly (SPEC:41-45). The seam to criticise is the shared contract file: one document, installed under `~/.claude/` (SPEC:52), with the report location left to each command's own flags.
- **Newman**: `--unattended` is a versioned interface to 37 commands. The spec makes it additive (SA-4) but the verification (AC-C5) is blind to the most common way of adding a flag (FU-3).
- **Hohpe**: the exchange pattern (task brief in, `worker_done` plus a pointer file out, coordinator opens the file; SPEC:62, 73) is sound, because Orca does not read the file (CAPS:79). It depends entirely on the path being known before dispatch (SPEC:73), which is false for several commands (F3).
- **Nygard**: failure modes mostly handled (blocked status, ask-resume, fence, `consumer_fenced`; SPEC:60-61, 70). Not handled: `--unattended` passed with no usable output location (table row G2, FU-6) and a poll sleep longer than the wait cap (G6).
- **Whittaker (adversarial)**: see the attacks quoted in F1, F2, F3, F5 and the table in section 3.

## 3. Guard Condition Boundary Table (mandatory artifact, completed before synthesis)
Guards are the conditional rules and thresholds of the candidate. Classes left out are named with a reason in the line under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` switch | SPEC:51, 227-231 (D1 a) | Zero/Empty | flag absent | off | SA-1: today's behaviour unchanged (SPEC:146) | OK |
| G1 | SPEC:51 | Sentinel Value Match | the text `--unattended` appears inside a quoted prompt or topic, e.g. `/sc:tdd "explain the --unattended flag"` | undefined | none: the spec never says whether the switch is a standalone token or any substring | GAP (FU-4, Medium: needs a guess that the implementer picks substring matching) |
| G1 | SPEC:60 (WC-2) | Typical | flag present, command has no gate | on, no-op | accepted, still writes contract (SPEC:159) | OK |
| G2 output location | SPEC:62 (WC-4), 73 | Zero/Empty | `--unattended` with no output location passed | no `<output-dir>` | none: where (or whether) a contract is written is not stated | GAP (FU-6, Medium) |
| G2 | SPEC:62 | Typical | `--output <dir>` directory-valued flag | `<dir>/return-contract.yaml` | stated | OK |
| G2 | SPEC:62, 85-87, 90, 92 | Legitimate Edge Case | command whose output is a file (`tdd --output <file>`, `init-lite --output <file>`), has a fixed directory (cleanup-audit, index-repo) or generates the directory itself (workflow `<id>`, implement `<slug>`) | no `<output-dir>` exists | none | GAP, blocking: F3 |
| G2 | SPEC:62, 92 | One/Minimal | stop before any output exists (workflow pre-creation STOP) | no package directory yet | "write the contract for pre-creation STOPs too" (SPEC:92) but no path | GAP, blocking: F3 |
| G3 outcome mapping | SPEC:63 (WC-5) | Typical | status `partial` | succeeded | stated | OK |
| G3 | SPEC:63 | Zero/Empty | no report file exists | failed | stated | OK |
| G3 | SPEC:62-63, 183 | Sentinel Value Match | existing contract whose own `status` value is outside {succeeded, partial, failed, blocked} | step-4 assert fails | WC-4 says existing contracts "keep their fields"; the existing vocabularies are recorded nowhere in the inventories | GAP (FU-7, Medium) |
| G4 ask/question | SPEC:61 (WC-3) | Zero/Empty | worker session holds no preamble | no `ask` | gate resolves as blocked, stop (SPEC:61) | OK |
| G4 | SPEC:61 | Maximum/Overflow | `ask` times out | pending | resume the same message ID, no duplicate | OK |
| G5 readiness | SPEC:59 (WC-1) | Legitimate Edge Case | fallback of 31-59 s | between "well inside" and the 60 s limit | "well inside" has no number; the evidence only shows 30 s passing and "above about 45 s" failing (CAPS:49) | GAP (FU-8, Medium: the owner is "launch setup", not a command, and no check covers it) |
| G6 wait cap | SPEC:68 (WC-10) | Typical | one wait of 3 min | no split | OK | OK |
| G6 | SPEC:68, 210 | Maximum/Overflow | wait of 3600 s (cli-eval, INV-A:65) | split into waits at most 4 min | stated | OK |
| G6 | SPEC:68, 114, 210 | Legitimate Edge Case | pr-submit sleep of "at least `--poll-interval`" with the interval default unstated | sleep may exceed 240 s | none: AC-4.3 demands "no single tool call exceeds 240 s" but the interval default is never given (SPEC:283) | GAP (FU-9, Medium) |
| G7 nested depth | SPEC:33, 66, 250 | Typical | depth 1, worker calls `worker-start` | refused `nested_worker_depth_exceeded` | stated (CAPS:97-99) | OK |
| G8 `--monitor` | SPEC:114 | Legitimate Edge Case | `--monitor 1` with `--unattended` | refused | stated | OK |
| G9 outward default | SPEC:67 (WC-9) | Legitimate Edge Case | `task` EXEMPT keywords `commit`/`push` (no flag exists) | "refused unless authorized" (SPEC:121) | WC-9 says authorization is "the command's own explicit flag"; task has no such flag (INV-B:45) | GAP (FU-10, Medium) |
| G10 task confidence | SPEC:121 | Sentinel Value Match | confidence exactly 0.70 | proceeds | "below 0.70" matches `cmd/task.md:93` as quoted at INV-B:45 | OK |

Classes left out: One/Minimal for G1, G3, G4, G5-G10 and Maximum/Overflow for G1, G2, G5, G7-G10 cannot occur or add no rule beyond the rows shown (the switch is boolean; the thresholds are single numbers). Zero/Empty for G5-G10 is not applicable (a threshold or refusal has no empty input).
The table is complete: all cells are populated and every guard is enumerated.

## 4. Pipeline dimensional analysis (Quantity Flow Diagram)
The only multi-stage flow whose counts diverge is the command classification and phase assignment (SPEC:76, 156-162).

```text
[Commands in cmd/: 43 (INV-A:3 + INV-B:3)] --> [Split] --> [Coordinator-only: 6 (SPEC:130-137)]
                                                  |
                                                  v
                                       [Worker-capable: 37 = 10 ready (3.1) + 27 needs-change (3.2)]
                                                  |
                                                  v
                       [Phase "Commands" columns: P1 9+4 fixes, P2 15, P3 4, P4 3 = 35]  <-- 2 absent: brainstorm, init-lite
                       [P1 scope sentence (SPEC:159): flag on "every command in 3.1 and 3.2" = 37]
                       [AC-1.1 (SPEC:195): section asserted for 37]
```
Divergence: 37 vs 35. FR-19 labels a dimensional mismatch CRITICAL; the Review Loop grades by consequence and the P1 scope sentence (SPEC:159) already covers all 37, so the missing two names cost an implementer a guess, not a wrong build. Graded Medium: FU-1.

## 5. Blocking findings

### F1. CRITICAL (Adzic, Whittaker sequence attack). The P0 acceptance check cannot pass, which stops the whole rollout
- Quoted texts: SPEC:158 "P0 ... (no command edits)"; SPEC:182 step 3 "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path"; SPEC:194 AC-0.4 "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"; SPEC:73 "the exact command line including `--unattended`"; SPEC:167 "A phase passes only when every check ... passes"; SPEC:154 "Later phases do not start until the earlier phase's checks ... pass".
- Wrong outcome: An implementer who follows the stated text as written runs the three P0 smoke commands with no command edits, so no command can write the WC-4 contract and `--unattended` does not exist yet. Step 3 requires "the WC-4 contract path" and a contract `status`, which cannot exist; AC-0.4 itself says the contract "arrives in P1" while requiring step 3 to pass. AC-0.4 therefore cannot pass, P0 never passes, and no later phase may start (SPEC:154). A second contradiction in the same check: AC-0.4 says the absence of an Agent-tool wrapper is "verified in the step-5 transcript" (SPEC:194), but step 5 only passes on "no `AskUserQuestion` call" (SPEC:184) and tests nothing about a wrapper, so that clause cannot be verified as written.
- Attack trace: before = P0 repo, no `return-contract.yaml` writer for `/sc:troubleshoot` (it writes one only with `--caller task-unified`, INV-B:49) ; after step 3 = `worker_done --report-path REPORT.md`, which is not "the WC-4 contract path" => step 3 FAIL.
- Recommendation: for AC-0.4 replace step 3's last two clauses with "its report path is the command's existing report file named in 3.1", drop `--unattended` from the P0 brief (SPEC:73 applies from P1), and move the wrapper check into a step that inspects the transcript for an Agent-tool call. Narrow, do not add.
- Priority High.

### F2. MAJOR (Wiegers, Fowler). WC-4 and the adversarial row name different contract locations, and the checks depend on the location
- Quoted texts: SPEC:62 "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed"; SPEC:83 "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"; SPEC:198 AC-1.4 "adversarial names one fixed path"; SPEC:182 step 3 "its report path is the WC-4 contract path"; evidence that the skill's artifacts sit under `<output>/adversarial/` (`INV-A:35`) and that real runs wrote two different depths (`INV-A:60`).
- Wrong outcome: An implementer who follows SPEC:83 builds the contract at `<output>/adversarial/return-contract.yaml`; one who follows SPEC:62 builds `<output>/return-contract.yaml`. The two stated texts contradict. Whichever is built, AC-1.2 and step 4 (`test -s <contract>`, SPEC:183) check "the WC-4 contract path", so adversarial passes only if the implementer happens to choose the WC-4 reading, and AC-1.4 (which tests for "one fixed path") passes under both. The adversarial case is also one of the three P0 smoke commands (SPEC:194).
- Recommendation: state one rule: either row 83 reads `<output>/return-contract.yaml`, or WC-4 gains the single exception "adversarial: `<output>/adversarial/`". Narrow row 83; add nothing else.
- Priority High.

### F3. MAJOR (Hohpe, Nygard, Whittaker divergence attack). WC-4 gives no usable contract location for commands without a directory-valued output flag, yet P1 and P2 checks require one
- Quoted texts: SPEC:62 (above) and SPEC:73 "the output directory, so the report path is known before dispatch"; SPEC:92 workflow: "Write the contract for pre-creation STOPs too"; the workflow contract lives at `.dev/tasks/to-do/<id>/` with `<id>` generated by the skill (`INV-B:52`, `INV-B:272`); SPEC:85 cleanup-audit "output dir is fixed"; SPEC:86 index-repo "State the output location"; SPEC:87 init-lite and SPEC:90 tdd pass `--output <file>`; SPEC:159 lists cleanup-audit, index-repo and workflow as P1 commands; SPEC:196 AC-1.2 "7.2 live check on each P1 command with `--unattended --output <dir>`"; SPEC:200 AC-2.2 example `/sc:tdd "auth" --unattended --output <file>`; SPEC:109 implement "contract beside the ledger" (ledger path `.dev/implement/<slug>/`, `INV-A:51`).
- Wrong outcome: An implementer follows AC-1.2 and runs workflow, cleanup-audit and index-repo with `--unattended --output <dir>`. None of the three has a directory-valued `--output` in this spec, and workflow's contract directory does not exist until the command creates it (and for a pre-creation STOP it never exists). Step 3 (path known before dispatch, report path equals WC-4 path) and step 4 cannot be met. For AC-2.2 with `tdd`, `--output` is a file, so `<output-dir>/return-contract.yaml` is undefined and the test of `status: blocked` has no file to open. The check cannot pass as written for these commands.
- Recommendation: for each command listed, add one cell stating where its contract goes (for example "beside the `--output` file" for tdd and init-lite; "the fixed directory" for cleanup-audit and index-repo; "workflow: coordinator-supplied `--output`/id, or the contract is read from the printed path") or remove the command from the AC-1.2 and AC-2.2 wording. Narrow WC-4 rather than add a mechanism.
- Priority High.

### F4. MAJOR (Wiegers, Cockburn). AC-1.1 and AC-1.2 require `load` to write and report a contract; its own rows say it has no report and is not a Task
- Quoted texts: SPEC:112 load: "Report (WC-4): none (see note) ... use it as a step inside another worker's brief, not as its own Task"; SPEC:265 "`/sc:load` handling: ... use it inside a brief ... a report file would be an unrequested addition"; SPEC:159 P1 Commands list includes "load (usage line only)"; SPEC:195 AC-1.1 "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"; SPEC:196 AC-1.2 "7.2 live check on each P1 command".
- Wrong outcome: An implementer who follows SPEC:112 and SPEC:265 changes only load's usage line and writes no contract. AC-1.2 then runs the live check on load, whose step 4 requires `test -s <contract>` and a `status` field (SPEC:183), and which presumes a Task for load that the spec says must not exist. AC-1.1 requires a section naming `return-contract.yaml` that load never writes. Both checks fail for load, and P1 cannot pass.
- Recommendation: delete load from the P1 live-check population (one clause in AC-1.2) and from AC-1.1, or state in load's row that its `## Unattended mode` section says "writes no contract". Narrow only.
- Priority High.

### F5. MAJOR (Adzic, Crispin). AC-2.2 demands a blocked outcome from every P2 command, but six P2 commands have no blocking gate
- Quoted texts: SPEC:200 AC-2.2 "Gate-trigger run per P2 command ... `worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`"; SPEC:160 the P2 command list (auggie-review, cleanup, improve, cli-eval, cli-portify, recommend, research, review-translation, spec-panel, task, tasklist, reflect, release-split, tdd, troubleshoot); the rows that do not block: SPEC:88 reflect (rule changed to the headless auto-accept, brief passes no `--remediate`), SPEC:100 auggie-review (`--unattended` implies `--no-post-pr` and `--no-remediation-offer`), SPEC:103 and SPEC:110 cleanup and improve ("apply only items ... list every 'Approval Required' item in the report, unapplied"), SPEC:116 research (`--unattended` pins `--strategy planning`), SPEC:122 tasklist (passes `--unattended` to reflect).
- Wrong outcome: An implementer builds exactly what those five rows state. AC-2.2 then asks each of these commands for an input that hits "the gate" and expects `blocked`; none of them ever writes `status: blocked` (they proceed, default or defer to the report). The criterion cannot pass for reflect, auggie-review, cleanup, improve, research and tasklist (and for spec-panel only a TDD input produces blocked, SPEC:120). AC-2.1 (SPEC:199) has the same "per gate in the row" wording but is satisfiable because it is a static assertion; AC-2.2 is not.
- Recommendation: narrow AC-2.2 to the P2 commands whose row says "blocked" (cli-eval, cli-portify, recommend, review-translation, release-split, tdd, troubleshoot, task, spec-panel with a TDD input) and give the other six a one-line expected result (for example cleanup: contract lists deferred items; auggie-review: PR counts unchanged, AC-2.4).
- Priority High.

## 6. Acceptance-criterion check, one by one
"Can pass" means: can pass as written for every command and phase it covers.

| ID | Can pass as written? | Why / finding |
|---|---|---|
| AC-C1 (SPEC:172) | Conditional | Passes only if the core files avoid the literal `orca (orchestration\|worktree\|terminal\|agent)`. SA-2 (SPEC:147) allows a mention in the contract file, which sits under the grepped `src/superclaude/core`, and P0 adds an Orca section to `HOW-WE-WORK.md` (SPEC:158). Needs a guess either way: FU-2 |
| AC-C2 (SPEC:173) | Yes | `make verify-sync` exits 0; UNVERIFIED target. It does not cover the `plugins/superclaude/commands/` mirror (SPEC:279, FU-11) |
| AC-C3 (SPEC:174) | Yes | baseline-diff form; does not assume a clean suite |
| AC-C4 (SPEC:175) | Yes | checks staged paths only |
| AC-C5 (SPEC:176) | Conditional | any removed line fails it. Adding `--unattended` to an existing Usage or `argument-hint` line removes that line; passes only if the flag goes on a new line: FU-3 |
| AC-0.1 (SPEC:191) | Yes | UNVERIFIED `KNOWN_CORE_FILES` (SPEC:52) |
| AC-0.2 (SPEC:192) | Yes | UNVERIFIED test name (`CLAUDE.md:334`) |
| AC-0.3 (SPEC:193) | Yes | no removed line in `HOW-WE-WORK.md` |
| AC-0.4 (SPEC:194) | **No** | F1 |
| AC-1.1 (SPEC:195) | **No for `load`**; brainstorm and init-lite only if the implementer reads SPEC:159 not SPEC:79 | F4, FU-1 |
| AC-1.2 (SPEC:196) | **No** | F3 (workflow, cleanup-audit, index-repo), F4 (load), F2 (adversarial) |
| AC-1.3 (SPEC:197) | Yes | `claude -p` plain run; two commands |
| AC-1.4 (SPEC:198) | Partly | the grep passes under either path (F2); "workflow states the contract is written for pre-creation STOPs" is checkable, but where it is written is F3 |
| AC-2.1 (SPEC:199) | Yes | static assertions |
| AC-2.2 (SPEC:200) | **No** | F5; the tdd example also needs F3 |
| AC-2.3 (SPEC:201) | Conditional | inherits step 3-4 problems for tdd (F3) and step 6 ambiguity (FU-12) for cleanup, improve |
| AC-2.4 (SPEC:202) | Yes | counts are first-page lengths (no `--paginate`); a PR with more than 30 reviews or comments could hide an added one: minor note |
| AC-2.5 (SPEC:203) | Yes | manual |
| AC-3.1 (SPEC:204) | Yes | the "or the command stops listing it" branch makes it satisfiable |
| AC-3.2 (SPEC:205) | Yes | |
| AC-3.3 (SPEC:206) | Yes | either creating the directory or changing the default satisfies `test -d` |
| AC-3.4 (SPEC:207) | Conditional | "two new per-session files" fails if both workers get the same `<session-or-timestamp>` suffix (INV-B:41 gives a timestamp as an option): FU-13 |
| AC-4.1 (SPEC:208) | Yes | for D2 (a) and (b) |
| AC-4.2 (SPEC:209) | Yes | |
| AC-4.3 (SPEC:210) | Conditional | only if D3 (b); the 240 s bound depends on the unstated `--poll-interval`: FU-9 |

## 7. Live-check steps (SPEC:178-186), one by one
| Step | Can pass as written for every command and phase it covers? | Why / finding |
|---|---|---|
| 1 task-create + worker-start (SPEC:180) | Yes | readiness evidence at CAPS:44-46 |
| 2 worker-show agentWait never non-null (SPEC:181) | Yes | a worker waiting in `ask` is not an `agentWait` prompt (CAPS:129); an absent field also passes |
| 3 one `worker_done`, outcome matches contract status, path is the WC-4 path (SPEC:182) | **No** | P0: F1; adversarial: F2; commands without a directory output: F3; load: F4 |
| 4 `test -s` and YAML assert (SPEC:183) | **No** | same set as step 3; existing contracts may use another `status` vocabulary: FU-7 |
| 5 search transcript for `AskUserQuestion` (SPEC:184) | Ambiguous | the transcript contains the loaded command and skill text and tool lists that name the tool; "no call" is the intent but the check says "search for". FU-12 |
| 6 `git status --short` shows only output-dir files (SPEC:185) | Ambiguous | cleanup, improve, document (inline), test `--fix`, implement edit repository files outside any output directory; whether "the command's documented artifacts" covers them is not stated: FU-12 |
| 7 worker-release then reclaimable list empty (SPEC:186) | Yes | CAPS:107-113 |

## 8. Follow-up candidates (Medium and minor; never trigger a revision)
The session that ran this review asks the user once per loop whether to open an issue for these; no issue has been created. This run is not `--unattended` and the question is left to the coordinator.

Medium:
- **FU-1** Phase "Commands" columns omit `brainstorm` and `init-lite` (35 of 37, section 4 of this report); SPEC:79 says the "only command changes are the small fixes" while SPEC:159 and SPEC:195 apply the flag, contract and section to every 3.1 command. Reading-dependent; resolved by SPEC:159.
- **FU-2** AC-C1 against SA-2 and P0 (table, section 6).
- **FU-3** AC-C5 blind to flag-on-existing-line edits (`grep '^-[^-]'`, SPEC:176).
- **FU-4** G1: a quoted `--unattended` substring; the switch's token rule is not stated (SPEC:51).
- **FU-5** The mechanism by which a worker session "runs the command directly" (SPEC:65) is not stated. The worker is launched with the brief on the command line (CAPS:47); how a `/sc:` command is entered from it (typed, Skill tool) is open, and 1.4 (1) says no such run exists.
- **FU-6** G2: `--unattended` with no usable output location.
- **FU-7** G3: existing contract `status` vocabularies against the fixed set and against "keep their fields" (SPEC:62, 262).
- **FU-8** G5: "well inside" the readiness limit has no number (SPEC:59).
- **FU-9** G6: pr-submit poll interval default is unstated, so 240 s is unproven (SPEC:114, 283, 210).
- **FU-10** G9: task `commit`/`push` have no "explicit flag" to turn on (SPEC:67, 121).
- **FU-11** SPEC:279 admits the `plugins/superclaude/commands/` mirror rule is unread; AC-C2 does not cover it.
- **FU-12** Live-check steps 5 and 6 wording (section 7).
- **FU-13** AC-3.4 timestamp collision; also save's first-write `.superclaude/.gitignore` creation by two workers.
- **FU-14** The installed `WORKER-CONTRACT.md` lives only under `~/.claude/` (core files are not part of `make sync-dev` per the Makefile list in the project instructions), so a dev checkout without `superclaude install` has no copy for a changed command to read; the dual-surface rule names both copies. UNVERIFIED which copies exist.

Minor:
- SPEC:11 says the pr-submit top-level rule was re-read at `SKILL.md:37-39` (also `INV-A:10`, `INV-B:90`) while `CAPS:161` quotes the same rule at `:47-49` of the installed copy. Different copies; line drift not resolvable here.
- AC-C1's `\|` inside backticks is table escaping; copied verbatim into a shell it may not behave as alternation.
- SPEC:285 reports an earlier citation validation of about 340 citations; it cannot be re-run here.

## 9. UNVERIFIED citations used by the candidate (not checkable in the sandbox)
`EVIDENCE.md:39,45,56`; `.dev/codegraph-migration/orchestration/README.md:31,33,42`; `return-contract.yaml:10`; `CLAUDE.md:16,50,72-83,157,334,408`; `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`; `src/superclaude/core/CLAUDE.md:65`; `src/superclaude/cli/install_core.py:4,13-33`; `pyproject.toml:38`; `Makefile:68-74`; every `cmd/` and `sk/` line not reproduced in the inventories; all `[G]`/`[H:*]` guide lines other than as quoted by `CAPS`. The candidate's grep claims (SPEC:25) were not re-run.

## Reviser brief
Blocking ids to repair: **F1, F2, F3, F4, F5**. Rules for the reviser (restated from the command, bullet 6):
- Revise only text a blocking finding names (SPEC:73, 83, 158, 182, 184, 194-196, 200 and the rows named in F3, F4, F5).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding; report the byte size of the candidate before and after, with the bytes added and deleted per finding id.
- Leave every Medium (FU-*) and minor item alone; do not apply them under "apply all findings".
- Return the candidate once and do not award yourself a PASS.

verdict: FAIL
