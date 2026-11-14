# QA Report: Reader-clarity lens (docs gate, task T295)

Date: 2026-11-12
Reviewer: qa-docs-readerclarity (rf-qa-qualitative), `fix_authorization: false`
Lens: read sweep.md, the skill, the WC-16 rule, the routing rows and the CHANGELOG entry as a person new to the project.

Method: every cited line was read from disk in this run (chunks of at most 150 lines). The code behind the claims was read in `src/superclaude/cli/sweep/` (`commands.py`, `probes.py`, `classify.py`, `report.py`, `models.py`). Pytest subsets ran: `tests/commands/test_sweep_command.py`, `tests/recommend/test_routing_refresh.py`, `tests/core/test_how_we_work_routing_table.py` (442 passed) and `tests/skills/test_worker_contract.py` (742 passed). `src/superclaude/core/HOW-WE-WORK.md` and the plugin mirror are byte-identical (`cmp`). No file other than this report was written.

## Findings

### RC-1 (MAJOR): "recommends nothing / no removal" is stated flatly, but the report carries "Safe to close", "Removable" and "Next inspection" columns that no file mentions

- Claims: `src/superclaude/commands/sweep.md:55` ("It adds no recommendation and takes no action"), `sweep.md:67` ("Add advice or a next step of its own to the report"), `src/superclaude/skills/sc-sweep-protocol/SKILL.md:61`, `src/superclaude/core/WORKER-CONTRACT.md:277` ("`/sc:sweep` recommends nothing: no stop, retry, release, merge or removal"), `src/superclaude/core/HOW-WE-WORK.md:334` ("recommends nothing"), `CHANGELOG.md:12`.
- The published report has a column `Safe to close (terminal / worktree)` and a column `Next inspection` per session (`src/superclaude/cli/sweep/report.py:402-404`, `:417`, `:419`), and a `Removable` / `Reason` pair per worktree (`report.py:442-454`). `NEXT_INSPECTION` (`report.py:42-55`) holds instructions such as "read the worker's last transcript lines". `classify.safe_to_close` (`classify.py:471`) describes these as "two review values".
- What is wrong: a person new to the project reads "recommends nothing, no removal" and then finds a table that says `Removable: yes` or `Safe to close: yes / no`. None of the five files says these columns are observations about unsaved work and not advice, and `sweep.md:14` (the description of what the report holds) lists neither the Worktrees section nor these columns. The claim is stronger than what the report shows, or the report is stronger than what the claim allows; a reader cannot tell which.
- Smallest fix: one sentence in `sweep.md` (after line 14) and in `SKILL.md` "Boundaries": "The report also states, as facts to review, `Safe to close`, `Removable` and `Next inspection` (what to read next); these are observations, not advice, and the coordinator or person decides." Alternatively narrow the WC-16 and routing wording to "no stop, retry, release or merge action".

### RC-2 (MAJOR): `stalled (proved)` and `fenced` are presented as live classes, but Phase 1 can never produce them, and the chat reply drops the one caveat

- Claims: `sweep.md:14` lists "stalled (proved)" as an example class; `WORKER-CONTRACT.md:277` says "only Orca's stall proofs make a worker stalled"; `SKILL.md:26` and the exempt reply (`SKILL.md:35-43`) print the per-class `counts` with no gloss.
- Code: `classify.py:195-203` makes a row stalled only when `fenced_evidence == "absent"`, and `classify.py:218-221` makes it fenced only when `fenced_evidence == "present"`. `probes.py` never assigns `fenced_evidence` (grep returned no match), and the default is `"unreadable"` (`models.py:87`). So both classes stay at 0 in Phase 1. The report says so (`report.py:36-39`: "Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.") but `sweep.md`, the skill, WC-16 and the chat reply do not.
- What is wrong: a coordinator that gets the exempt reply (counts and path only, no gloss) sees `stalled (proved): 0` and can read it as "nothing stalled". The term "(proved)" is also never defined in `sweep.md`. WC-16 itself reads as if stalls can be reported.
- Smallest fix: add to `sweep.md:14` and to the skill's step 4: "In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so." Keep the exempt reply's wording, but add the caveat sentence to the facts it may print, or tell the coordinator in WC-16 that those two zeros carry no meaning.

### Minor notes (never fail the gate)

- RC-3 (MINOR): two meanings of "sweep" in one rule. `WORKER-CONTRACT.md:110` ("The sweep." = `worker-list`, prompt-wait listing, `stat`) and `/sc:sweep` are both called a sweep; `sweep.md:20` says "its liveness sweep pass", a phrase the contract does not use; `HOW-WE-WORK.md:405` quotes `"The sweep."` without saying it is a run-in heading under "Liveness supervision". WC-16 does state "it does not replace that sweep", which mostly saves it. Fix: name the first one "the liveness sweep" in WC-16, the guide and `sweep.md`.
- RC-4 (MINOR): "Phase 1" (orchestrator mode) versus "P1" and "P0" (the unattended-mode conversion phases used across `WORKER-CONTRACT.md:307-309`, `:299`). WC-16's "Phase 1 adds this duty, not a scheduler" and the CHANGELOG heading "(Phase 1)" do not say which phase series; a reader can confuse them. Fix: write "orchestrator-mode Phase 1" once.
- RC-5 (MINOR): `WORKER-CONTRACT.md:277` says "The coordinator keeps that pass scheduled while work remains" and then "not a scheduler". Who schedules? The preceding sentence ("On every coordinator wake or wait timeout") answers it, but "scheduled" invites a timer reading. Fix: "keeps running that pass on each wake or wait timeout while work remains".
- RC-6 (MINOR): `SKILL.md:26` tells the skill to print `visible`, `historical` and `bound_reached` and never says what they mean. In code `historical` is the idle count and `visible` is the total minus idle (`classify.py:964-971`); `bound_reached` counts worker reads cut by the show cap or time budget. A reader of the reply cannot interpret them. Fix: one gloss each in `sweep.md` or the skill.
- RC-7 (MINOR): "person-run exclusion" (`SKILL.md:45`; same in `pragmatic.md:24`) is named as if defined; neither file defines it before use (the list in "What stays ordinary" does the work later). Fix: say "the rule that ordinary person-run invocations stay ordinary".
- RC-8 (MINOR): `HOW-WE-WORK.md:334` says "prints JSON" and "the bound Orca Run". The `/sc:sweep` reply prints counts and a path (`SKILL.md:26`); the JSON is the CLI's output to the skill. `/sc:sweep` also accepts named `--run` ids (`sweep.md:35`). The row is pinned byte-for-byte to DESIGN row R2 (plan item 13.1), so a change needs the DESIGN row changed first.
- RC-9 (MINOR): `sweep.md:36` "1 to 9999, at most 720h or 30d" reads as contradictory; the code (`commands.py:43-52`) means 1 to 720 for `h` and 1 to 30 for `d`. `sweep.md:35` says the no-Run exit is for "no Run bound and none named"; code also exits 2 with a different message when Orca is unavailable (`probes.py:359-362`). `sweep.md:38` does not say which folders the report folder must stay apart from (`.dev/tasks`, `~/.claude/projects`, the ccsession `orca-tabs` folder, `commands.py:254-262`).
- RC-10 (MINOR): `sweep.md:14` "the report is the one file it adds": the command also creates `.dev/sweeps/` if missing and writes then removes a temp file in it, and a failure can leave that temp file (`commands.py:158`, `:168`, `:142`). `CHANGELOG.md:11` "changes nothing ... in any worktree" is true only because `.dev/sweeps/` is ignored (`.gitignore:256`, confirmed with `git check-ignore`); the report folder lives in the checkout's own worktree. `SKILL.md:19` "reads no environment variable" is true of the skill, but the command reads `ORCA_CLI_COMMAND` and `XDG_STATE_HOME` (`probes.py:193`, `commands.py:253`).
- RC-11 (MINOR): `SKILL.md:27` says "print the standard error line"; exit 1 on a publish failure can print several lines (`commands.py:283-285`). `HOW-WE-WORK.md:405` says "on every wake" and omits "or wait timeout" from WC-16.

### Points checked and found clear

- Exit codes (0 published, 1 internal or publish error, 2 usage error), JSON keys `report_path` and `summary`, and the final line `Report complete` all match `SKILL.md:25-27` (`commands.py:279-288`, `report.py:520`, `report.py:664-672`).
- Run id shape `run_` plus 12 lowercase hex digits, repeat and de-duplicate, default window `6h`, `--root` must hold `.git`, `--output` under `<root>/.dev/sweeps/`: match `commands.py`/`probes.py:44`.
- The style exception text in `pragmatic.md:23-25` and the skill's "Final reply" (`SKILL.md:31-51`) state the same five conditions, the same "what establishes the assignment" limits and the same "what stays ordinary" list.
- Never-as-worker list names `/sc:sweep` in the contract (`WORKER-CONTRACT.md:23`), the developer guide (`...Commands-Skills-Agents.md:991`), `sweep.md:16` and the CHANGELOG.
- WC-16 opening ("On every coordinator wake or wait timeout") and the 5-minute cap on `sweep.md:20` agree with `WORKER-CONTRACT.md:110`; the 300000 ms wait in `WORKER-CONTRACT.md:101` is the same 5 minutes.
- CHANGELOG items check out: `.gitignore:256` has `.dev/sweeps/`; `tests/sweep/` exists with the named test modules.

## Checks

| Check | What it covers | Result |
|---|---|---|
| C1 | `sweep.md` terms defined for a newcomer (Run, eight classes, `stalled (proved)`) | FAIL (RC-2) |
| C2 | `sweep.md` flags, defaults and limits against `commands.py` and `probes.py` | PASS (notes RC-9) |
| C3 | "recommends nothing / no next step / no removal" against the report content | FAIL (RC-1) |
| C4 | "the report is the one file it adds" against `_publish` | PASS (note RC-10) |
| C5 | Skill steps 1-5 against exit codes, JSON keys, last report line | PASS (note RC-11) |
| C6 | Printed summary fields are explained to the reader | PASS (note RC-6) |
| C7 | Skill "Final reply" against `pragmatic.md` exception | PASS (note RC-7) |
| C8 | Command, skill and contract agree on who may run it (coordinator or person, never worker) | PASS |
| C9 | WC-16 internal clarity (two sweeps, scheduled versus not a scheduler, Phase 1 versus P1) | PASS (notes RC-3, RC-4, RC-5) |
| C10 | WC-16 and class wording against what Phase 1 code can output (stalled and fenced) | FAIL (RC-2) |
| C11 | Routing rows (guide row, Orca coordination bullet, plugin mirror, user guide row, developer guide list) agree with each other and with the command | PASS (notes RC-8, RC-11) |
| C12 | CHANGELOG entry against `.gitignore`, tests folder and code behaviour | PASS (note RC-10) |
| C13 | Test subsets run (442 and 742 passed) | PASS |

Verdict: FAIL

Blocking count: 2
