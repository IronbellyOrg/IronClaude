# Spec panel review, round 2: orca-worker-contract-spec.md

review: 1 of 3

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Spec under review | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, revision 1 (326 lines, 71195 bytes by `wc`), not edited by this review |
| Review count | The invocation carries no `--re-review` and no `--baseline`, so Review Loop bullet 1 makes this run a first review of the full document and the header is `review: 1 of 3`. The coordinator keeps the real count (this is the second report on this spec; `review/spec-panel.md` is `review: 1 of 3`) and the saved copy; the per-finding resolution table below is added because the brief asks for it |
| Prior report | `.dev/orca-command-refactor/review/spec-panel.md` (24 findings, verdict FAIL, blocking 1-14) |
| Review date | 2026-11-10 |
| Panel (review order) | Wiegers (lead), Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin (guard-table completeness) |
| Active focus | requirements, architecture. `--focus correctness` is not active, so no State Variable Registry. The Guard Condition Boundary Table and the Quantity Flow Diagram are produced because the spec contains guards and multi-stage counts |
| Grading | Review Loop bullet 2: CRITICAL and FR-8/FR-9 findings are blocking; MINOR is minor; a MAJOR is blocking only if it names a concrete wrong outcome an implementer would produce, otherwise minor. The brief says any finding of any severity is FAIL. Review Loop bullet 7 lets a brief narrow the scope but not grade a minor finding as blocking, so this report grades by bullet 2 and the verdict follows the blocking findings. Here both rules give FAIL |

Citation shorthand. `SPEC:N` = line N of the revised spec `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `V1:N` = line N of `.dev/orca-command-refactor/specs/history/spec-v1.md`. `PANEL:N` = line N of `review/spec-panel.md`. `DISP:N` = line N of `review/disposition.md`. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`. `CMD:N` = line N of `command.md` in this sandbox (the `/sc:spec-panel` definition). N1 to N18 are the new findings of this report.

Verification scope. The workspace holds the revised spec, its v1 copy, the README, the three inventories, the round-1 report and the disposition. It holds no `src/`, no `CLAUDE.md`, no `tests/`, no `Makefile`, no `.dev/evals/`, no `.dev/codegraph-migration/`, nothing under the sandbox `~/.claude`, and I did not run `orca-ide`. So a citation to any of those is UNVERIFIED here. What I could do: (1) check every inventory, capabilities and README line the revision cites against those files; (2) check the spec's quotes of inventory text; (3) run the spec's shell and Python acceptance snippets on sample input (stdin only, nothing written); (4) diff v1 against the revision to find every added or changed line.

## Part 1. Per-finding resolution table

Rule used: `resolved` = the revised spec text closes the wrong outcome the finding named, checked in the spec, not in `DISP`. `open` = that outcome is still reachable. A residual weakness found while checking a resolved finding is raised as a new finding, not re-opened. Notes 15-24 were not revised (`DISP:8`), so each is checked for unchanged text and for whether a revised line now depends on it.

| # | Round-1 finding (short) | Status | Evidence in the revised spec (checked) | Residual or comment |
|---|---|---|---|---|
| 1 | AC-1.1 and P1 count commands the spec excludes or defers | resolved | AC-1.1 is restated per phase over an explicit list (SPEC:228). P1 row names 14 commands: 8 needs-change + 6 ready (SPEC:178). I re-counted against 3.1 and 3.2: 8 + 6 = 14, plus `load` (usage line only, SPEC:118) = the 9 P1 rows of 3.2 and 6 P1 rows of 3.1. `load` and the six section-4 commands carry no section (SPEC:147, 178, 228). pr-submit only under D3 (b) (SPEC:181, 228) | The disposition rejected the sub-part "load carries a section naming no contract"; reasoned at SPEC:298 and acceptable |
| 2 | Flag accepted in P1 before gate rows exist in P2-P4 | resolved | SPEC:173 (a command accepts the flag only in its own phase), SPEC:178 ("14 commands ... and no others"), SPEC:179 ("each of these commands gains its section ... in this phase"), SPEC:78 support check, SPEC:306 | Cross-phase callee case left without an owner: N7 |
| 3 | Retry reuses Task and output dir; stale contract read as outcome | resolved | WC-4 removes a left-over contract before other work (SPEC:63); WC-6 says a retry gets the same path and relies on that removal (SPEC:65); coordinator treats a contract older than the dispatch as stale (SPEC:74); 7.2 step 4 checks mtime later than `worker-start` (SPEC:216); fixed-output commands are one attempt at a time (SPEC:65, 91) | WC-6's first sentence still promises a "fresh output directory" and non-corruption; it contradicts the same paragraph: N3. mtime alone cannot tell a sibling Task's contract from this one's: N4 |
| 4 | Contract placement does not fit file-valued `--output`, adversarial subdir, workflow generated id and STOP, troubleshoot conditional contract | resolved (as named) | Placement rule i / ii / iii at SPEC:63; tdd and init-lite stem rule (SPEC:93, 96); adversarial named path (SPEC:89); workflow generated id and no contract on a pre-creation STOP (SPEC:98); troubleshoot writes it always under `--unattended` (SPEC:97); AC-1.4 and AC-2.2 updated (SPEC:231, 233) | The rule says "in every other case the path is known before dispatch" (SPEC:63). That is false for 11 rows of section 3 (no flag, no place) and unsettled for 2 more (flag implied, not named): N1 |
| 5 | Spec never says how the worker starts the command | resolved | SPEC:77 (Skill tool, command name, argument string, no paraphrase, do not copy the PR #329 wrapper); WC-7 points to 2.3 (SPEC:66); AC-0.4 requires the instruction in the brief and the skill-loaded transcript check (SPEC:227); UNVERIFIED 15 (SPEC:323) | AC-0.4 is itself unsatisfiable on other grounds: N2 |
| 6 | No version or capability check; section-4 commands | resolved | Support check at SPEC:78 (installed command file contains `## Unattended mode`, `~/.claude/WORKER-CONTRACT.md` exists, else flag not passed); step 1 of 7.2 requires it (SPEC:213); section 4 says the check fails for the six by design (SPEC:147); UNVERIFIED 16 | The check reads the coordinator's filesystem only: N9 |
| 7 | No rule that `--unattended` reaches nested skills and commands | resolved | WC-2 propagation sentence (SPEC:61); new section 3.3 table (SPEC:133-144) with caller, callee, callee phase and evidence; every INV line cited there checked (see Part 2) | Table omits chains the inventories show: N8 |
| 8 | AC-C5 / AC-0.3 regex wrong in both directions | resolved | Code block 2 `grep '^-' \| grep -v '^--- a/'` (SPEC:208); SA-4 permits the Usage and `argument-hint` line (SPEC:168); AC-C5 allows exactly those lines (SPEC:195). I ran the pipe on sample diff lines: it prints the removed prose line, the removed bullet `--- bullet` and the removed fence `----` and hides only the `--- a/` header | `master...HEAD` sees committed changes only: N13 |
| 9 | AC-C1 contradicts P0 deliverables; escaped pipe | resolved | AC-C1 moved to a code block with plain pipes, excludes `core/WORKER-CONTRACT.md` and `core/HOW-WE-WORK.md` (SPEC:197-204); SA-2 names exactly those two (SPEC:166). Sample run: `orca-ide orchestration ask` in a command file is printed, the same text in `WORKER-CONTRACT.md` is not | Pattern covers four verbs and lowercase `orca` only, so `orca status` or an `ORCA orchestration` placeholder would pass unseen (noted, not graded) |
| 10 | WC-10 5-minute vs 4-minute disagreement; parallel batches | resolved | One limit, 240 s, in WC-10 (SPEC:69), Decisions (SPEC:299) and AC-4.3 (SPEC:243); parallel Agent-tool batches exempt; silence not read as stall (CAPS:125); UNVERIFIED 17 (SPEC:325) | Single long subprocess calls (build, test, eval) are neither split nor exempt: N6 |
| 11 | `--unattended` semantics: no output location, person-mode flags, quoted token | resolved | Token rule at SPEC:52; person-mode refusal at SPEC:61; no-output-location refusal at SPEC:63; D1 (a) text corrected at SPEC:261 | spec-panel row is silent while the only implemented section in the sandbox differs: N15 |
| 12 | WC-5 only covers a missing report | resolved | WC-5 lists missing, empty, unparseable, status outside the four values, blocked with empty question (SPEC:64); WC-4 requires a non-empty `blocked_question` (SPEC:63); step 4 asserts it (SPEC:216). Python run on sample dicts: empty question FAILs, empty file FAILs (TypeError), list FAILs, valid succeeded PASSes | Applies only to a YAML contract; ready commands before P1 have none: N2. Legacy status vocabulary still never inventoried (note 22) |
| 13 | WC-9 authorization cannot be checked; post-release single flag | resolved | One flag per outward action class, no umbrella flag (SPEC:68, 119); the quote duty moved to the coordinator (SPEC:79); D4 (a) reworded (SPEC:278). Naming of post-release flags deferred to P4 (SPEC:119, DISP:31) | Accepted: the flag surface is not in the inventories. Sentence/class mismatch: N10 |
| 14 | WC-2 no precedence; one `blocked_question` for several gates | resolved (named cases) | Precedence (b) then (a) then (c) and a list of every visible unresolved gate (SPEC:61) | The precedence rule makes the round-1 research example (caller passes `--strategy intent`) produce a stall: N5 |
| 15 | WC-1 / WC-3 / WC-12 no phase owner or check; "well inside" has no number | open (unchanged note) | SPEC:60 still says "well inside the readiness limit"; no traceability row; CAPS:49 gives 30 s works, about 45 s fails | Minor note, not revised by rule (DISP:33) |
| 16 | P0 builds before it tests | open (unchanged note) | SPEC:177 unchanged: contract file, `KNOWN_CORE_FILES`, guide edits and test file are listed before the smoke runs | Minor note. N2 shows a P0 pass-condition defect separate from ordering |
| 17 | Tasklist nesting stated as fact | open (unchanged note) | SPEC:128 still reads "inside Claude Code's nesting limit, `INV-A:14`"; INV-B:210 and INV-B:314 mark nested spawning UNVERIFIED | Minor note; the row is on a changed line (it gained the Stage 10.5 `--unattended` text) so this is now a changed-line dependency, still minor |
| 18 | `partial` mapped to `succeeded` unblocks dependents | open (unchanged note) | SPEC:74 says the coordinator "applies WC-5" but gives no "check status before starting dependents" step (CAPS:85-86, 90, 92) | Minor note |
| 19 | "Phases 1-3 need no user decision" vs D4 | open (unchanged note) | SPEC:173 unchanged; D4 (SPEC:277) still lists auggie-review and task (P2 rows). WC-9 now requires flags named per command section, which makes P2 task depend on the D4 answer | Minor note |
| 20 | AC-1.3 "scratch worktree" | open (unchanged note) | SPEC:230 unchanged; the worktree rule is in `CLAUDE.md`, absent here: UNVERIFIED | Minor note |
| 21 | AC-2.4 `--jq length` reads one page | open (unchanged note) | SPEC:235 unchanged; page size behaviour of `gh api` not run here: UNVERIFIED | Minor note |
| 22 | Existing contract status vocabularies never inventoried | open (unchanged note, now more exposed) | WC-4 still says existing contracts "keep their fields" (SPEC:63) while WC-5 now maps any status outside the four to `failed` (SPEC:64). INV-B:272, INV-B:112, INV-A:39, INV-A:35 still give no values | Minor note: the trigger (a differing legacy value) is UNVERIFIED, so no concrete wrong outcome is provable here |
| 23 | Brainstorm rated ready without noting it answers its own questions | open (unchanged note) | SPEC:90 small fix is "None" | Minor note |
| 24 | No coordinator branch for a worker that ends without `worker_done` | open (unchanged note) | SPEC:74 covers a stale contract only; nothing for a worker that dies | Minor note |

Totals: blocking findings 1-14 resolved as named (14 of 14); notes 15-24 open and unchanged (10 of 10), as the rules intended. New defects found while checking the resolutions: N1, N2, N3, N4 and N5 are blocking; N6 to N18 are minor notes.

## Part 2. Citation-check table

Scope. "Added or changed by the revision" comes from `diff V1 SPEC`: 80 added and 39 removed diff lines (119 in all). The live files for `src/`, `CLAUDE.md`, `pyproject.toml`, `.dev/evals/` and `.dev/codegraph-migration/` are not in the workspace and I did not run `orca-ide`, so for those the only witness available is the inventory or capabilities line that quotes them. "Confirmed" below therefore means: the spec's wording is supported by the quoted inventory or capabilities text; it does not mean the inventory's own quote of the source file was re-read.

### 2A. Wrong, overstated, inconsistent or unsupported citations

| ID | Spec location | Citation and claim | Check | Result |
|---|---|---|---|---|
| C1 | SPEC:69 (WC-10), SPEC:120 (pr-submit row) | "pr-submit's 600 s is a cumulative per-wait budget made of repeated iterations (one foreground poll, then a sleep of at least `--poll-interval`), not one blocking call" citing `cmd/pr-submit.md:49`, `sk/sc-pr-submit-protocol/SKILL.md:46-64` | INV-B:95 and INV-B:299 say "waits up to `--timeout` 600 s per wait over several rounds" and ask for heartbeats; neither mentions a poll-then-sleep structure or `--poll-interval`. The spec's reading is new in the revision and rests on a file I cannot open | UNVERIFIED and a reinterpretation of the inventory. If the sleep default is 240 s or more, "each iteration under 4 minutes" (SPEC:120) cannot hold |
| C2 | SPEC:77 (Start instruction) | "Orca places the Task text inside a preamble (Claude gets its task on the command line, `CAPS:47`)" | CAPS:47 supports only the second half (Claude's `promptInjectionMode: 'argv'`). The preamble and Task block are at CAPS:76 and CAPS:78 | Partly supported; wrong line for the first half |
| C3 | SPEC:119 (post-release row) | `sk/sc-post-release-protocol/SKILL.md:...,292,...` | INV-B:77-85 cite 71-75, 95-99, 129-131, 150-157, 187, 221-235, 266-276, 324, 340, 348, 351. Line 292 is in no inventory row. It already stood in V1:113 | UNVERIFIED, no witness |
| C4 | SPEC:69 | `sk/sc-cli-eval-protocol/SKILL.md:151-152` "eval timeouts up to 3600 s" via `INV-A:65` | INV-A:65 cites `:151` only | Range widened by one line; line 152 unwitnessed |
| C5 | SPEC:120, SPEC:272, SPEC:320 | pr-submit poll loop cited as `46-64`, `41-64` and `46-48` for the same claim; INV-B:299 and INV-B:95 use `41-64` | Three ranges for one fact | Inconsistent; UNVERIFIED which is right |
| C6 | SPEC:106 (auggie-review), SPEC:79, SPEC:278 | "posting returns only with an explicit `--post-pr` in the brief" citing `cmd/auggie-review.md:51-55` | INV-A:38 names `--no-post-pr` (C:52), `--remediation-offer` (C:53) and `--no-remediation-offer` (C:54); posting is described as the default at C:51. No inventory line says an explicit `--post-pr` flag exists today | UNVERIFIED whether `--post-pr` exists; if not, WC-9's "named flag" is a new flag and the row should say so |
| C7 | SPEC:128 (tasklist row) | "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" | INV-A:14 quotes the three-layer docs rule; INV-B:210, INV-B:314 and INV-B:322 mark nested spawning from the Stage 10.5 subagents UNVERIFIED. The row was edited by the revision, the claim was not corrected | Overstated (same as round-1 note 17); now on a changed line |
| C8 | SPEC:23 (E2) | worker "reached `state: ready, stage: input_accepted` and answered", `EVIDENCE.md:45` | CAPS:49 quotes EVIDENCE.md:45 as "worker-start returned after 34s, `state: ready, stage: input_accepted`"; "and answered" is not in the quote | Overstated; carried from V1, not changed by the revision |
| C9 | SPEC:216 | "PyYAML is a declared dependency, `pyproject.toml:38`" | `pyproject.toml` absent. The project instruction file loaded in this session lists only pytest, click and rich under Dependencies (that list may be partial) | UNVERIFIED; check before AC step 4 is relied on |
| C10 | SPEC:26 (E5), SPEC:166 (SA-2), SPEC:191 (AC-C1) | "no command, skill, agent or core file calls Orca today"; `grep -rlni orca ...` run 2026-11-02 | Cannot be re-run. The skill listing loaded in this session (not a workspace file) shows `sc:issue` described as creating an Orca worktree, plus `sc:graph` and `sc:impact`, none of which appears in INV-A:3 or INV-B:3 | UNVERIFIED and possibly stale: N12 |
| C11 | SPEC:12, SPEC:322 | "re-read 11 load-bearing locations" and "about 340 citations re-read ... 9 defects" | No witness in the workspace. SPEC:322 states the revision text was not part of that check | UNVERIFIED; honest about scope |

### 2B. Citations added or changed by the revision and confirmed against workspace files

| File | Lines cited by the revision | What the line says | Supports the spec claim |
|---|---|---|---|
| `CAPS` | 44-45, 46, 49 | 60 s default and `--timeout-ms`; exit 0 only for ready; 30 s fallback passes, about 45 s fails | WC-1, step 1 of 7.2: yes |
| `CAPS` | 47 | Claude gets the task as argv | SPEC:77 second half: yes (C2 for the first half) |
| `CAPS` | 52, 129 | a worker waiting on a prompt is "healthy, not failed" | E-claims in 1.4 (2), WC-2, WC-10: yes |
| `CAPS` | 58-61, 64, 66-67 | `ask` blocking and resume by ID; no heartbeat while in `ask`; `check` and `consumer_fenced` | WC-3, WC-12: yes |
| `CAPS` | 72-74, 76-77, 79 | `--report-path` only with real values; outcome mandatory; dispatched pane only; report is a pointer | WC-4, WC-5, R3: yes |
| `CAPS` | 84-92, 85-86, 90 | Task DAG; `task-list --ready`; failed Task keeps dependents blocked; Orca does not schedule | E1, section 4 spawn row, F18 note: yes |
| `CAPS` | 97-101, 103 | depth 1; refusal code; no workaround; call sites unverified | R1, WC-8: yes |
| `CAPS` | 107-113, 115, 116 | one release decision; placement; retry and circuit breaker | 2.3, 7.2 step 7, WC-6, WC-11: yes |
| `CAPS` | 125, 130 | absence never authorizes stop; heartbeat cadence from the preamble, use by Orca unverified | WC-10: yes |
| `CAPS` | 145-149 | executable name; readiness; `runtime_unavailable`; no preamble no lifecycle; explicit identity outside Orca | R2, R4, SA-2: yes |
| `CAPS` | 150, 155-156, 158-161, 186-187 | worker_done bound to pane; subagents not Orca workers; PR #329; provenance; top-level commands; UNVERIFIED items | R3, E4, WC-7, 1.4 (1), (3): yes |
| `CAPS` | 12-13, 99, 128, 135-139, 149, 151 | guide sources; depth is a setting; remote workers; model/effort; `ORCA_TERMINAL_HANDLE` | non-goals 2, 3, 9, D1 (b), D5: yes |
| `INV-A` | 3, 14, 35-55, 36, 39, 42, 44, 49-50, 53, 55, 60-62, 65-66, 68, 76-83, 90-92, 95-98, 106, 113, 118, 120 | row, note, summary and UNVERIFIED lines | every use in 1.2, 2.2, 3, 3.3, 4, 8 and the UNVERIFIED list: yes (INV-A:14 is overstated for tasklist, C7) |
| `INV-B` | 3, 31-52, 33, 34, 35, 36-52 rows and notes 57-65, 67-75, 77-85, 87-95, 97-105, 107-115, 117-125, 127-135, 137-145, 147-155, 157-165, 167-175, 177-185, 187-195, 197-205, 207-215, 217-225, 227-235, 237-245, 247-255, 257-265, 267-275 | per-command rows and evidence notes | the "Evidence" column of every row in 3.1 and 3.2: yes |
| `INV-B` | 112, 121, 201, 210, 242, 269, 271, 272, 285-287, 289-299, 301, 311, 314, 320, 322, 323 | contract statuses; callee chains; troubleshoot contract only with `--caller task-unified`; gate table; UNVERIFIED items | 3.3 table, WC-4, Decisions: yes |
| `README` | 6, 11-17, 12, 30, 31 | goal; evidence list; PR #329; planning only; no commits, pushes, PRs or GitHub comments | E3, WC-9, section 4 git row, non-goal 10: yes |
| `V1` | 113, 160 | pre-revision post-release and P2 rows | confirms which lines the revision changed |

Method check on the rows of 3.1 and 3.2: for each `sk/` and `cmd/` line number the revision left or added, I compared it with the same command's inventory row and notes. All matched except C3 (292), C4 (152) and C5 (the pr-submit ranges). Counts I re-derived and agree with: 43 = 21 + 22 (INV-A:3, INV-B:3); 10 ready, 27 needs-change, 6 coordinator-only (rows of SPEC:89-98, SPEC:105-131, SPEC:151-156); P1 14, P2 15, P3 4, P4 3 plus `load`.

### 2C. Citations I could not check here (file absent from the workspace, no inventory witness)

| Group | Spec locations | Status |
|---|---|---|
| `CLAUDE.md` lines | SPEC:35 (`:74`), SPEC:53 (`:83,408`), SPEC:169 (`:16,157,334`), SPEC:194 (`:16`), SPEC:225 (`:334`), SPEC:272 (`:50`), SPEC:297 (`:72-83`), SPEC:316 (`:76`) | UNVERIFIED |
| `src/superclaude/cli/install_core.py`, `Makefile`, `pyproject.toml` | SPEC:53 (`:4,33`, `:13-24`), SPEC:316 (`Makefile:68-74`), SPEC:216 | UNVERIFIED |
| `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254`, `core/CLAUDE.md:65` | SPEC:165, SPEC:183 | UNVERIFIED |
| `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:39,45,56`, `.dev/codegraph-migration/...:31,33,42`, `...return-contract.yaml:10` | SPEC:24, SPEC:44-45, SPEC:60, SPEC:193 | Partly witnessed through CAPS:49, CAPS:156; lines 33 and 42 have no witness |
| Orca guide and `--help` output, `orchestration-timing-budgets.js`, `nested-worker-depth.js` | cited via `CAPS` | Not re-run; I trust the capabilities inventory only as far as its own quotes |
| All `src/superclaude/{commands,skills,agents}` lines | sections 3 and 4 | Witnessed by the inventories (2B), not by the files |

Count: 11 findings in 2A (3 wrong or overstated: C2, C7, C8; 4 unwitnessed or inconsistent: C3, C4, C5, C6; 4 unverifiable: C1, C9, C10, C11). None is blocking on its own; C1 matters because WC-10 and the pr-submit row (D3 b) depend on it.

## Part 3. Panel critique of the revised spec

Mode: critique, whole document, with extra attention to lines changed by the revision (80 added and 39 removed diff lines against V1). Scores and consensus come last.

### Guard Condition Boundary Table

Trigger: the spec has flag guards, thresholds and fallbacks. Seven cross-cutting guards are enumerated with the six required input conditions each (42 rows); the per-command gate resolutions of section 3 are instances of G6 and are not repeated. Construction: Nygard. Completeness validation: Crispin. Attacks on entries: Whittaker. All cells are populated, so the FR-10 synthesis gate is met. Each GAP row generates a finding of MAJOR or higher (FR-8) and is blocking; the finding id is in the Status column. No row says "unspecified" without a GAP (FR-9).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 unattended switch | SPEC:52, 165 | Zero/Empty | flag absent | false | Standalone behaviour unchanged (SA-1) | OK |
| G1 | SPEC:63 | One/Minimal | `--unattended`, command needs an output location, brief gave none | true | Stop before any work, chat refusal only, worker ends `failed` | OK |
| G1 | SPEC:52, 63 | Typical | `--unattended --output <dir>` | true | Gates per section 3, contract in `<dir>` | OK |
| G1 | SPEC:61 | Maximum/Overflow | `--unattended --interactive` (or `--watch`, `--mode socratic`, `--format interactive`) | true | Refused, `status: failed` with the reason (spec-panel conflict is N15) | OK |
| G1 | SPEC:52 | Sentinel Value Match | the text `--unattended` inside a quoted topic | false | Counts only as a standalone unquoted token | OK |
| G1 | SPEC:78, 323-324 | Legitimate Edge Case | flag given to a command or install without the section | unknown | Coordinator support check prevents it; the command-side behaviour is UNVERIFIED 16 and avoided | OK |
| G2 contract location | SPEC:63 | Zero/Empty | no output location in the brief for a command that needs one | refuse | Chat-only refusal, no file | OK |
| G2 | SPEC:63, 74, 91-92, 110-111, 114, 121-123, 125, 127-128, 130-131 | One/Minimal | command with no output flag and no fixed subdirectory or generated id named in its row (cleanup-audit, index-repo, cli-eval, cli-portify, research, review-translation, task, tasklist, save, validate-roadmap, validate-tests; flag unnamed for explain, recommend) | unknown | WC-4 says the path is known before dispatch; the rows do not give it | GAP (N1) |
| G2 | SPEC:63 | Typical | directory-valued `--output-dir` or new output flag | true | `<dir>/return-contract.yaml` | OK |
| G2 | SPEC:63, 70, 74, 216 | Maximum/Overflow | two concurrent or retried Tasks given the same output location | collision | Each removes the other's contract at start; the staleness test is mtime only; no duty to give each Task its own location | GAP (N4) |
| G2 | SPEC:63 | Sentinel Value Match | file-valued `--output` whose stem is `return-contract` | stem rule | `<dir>/return-contract.return-contract.yaml`; defined, ugly, harmless | OK |
| G2 | SPEC:63, 98 | Legitimate Edge Case | workflow stops before its `<id>` directory exists | no contract | No contract, worker ends `failed` | OK |
| G3 outcome mapping | SPEC:64 | Zero/Empty | contract missing | failed | `--outcome failed` | OK |
| G3 | SPEC:64 | One/Minimal | empty or unparseable file | failed | `--outcome failed` (run: empty text and a YAML list both fail the step-4 assertion) | OK |
| G3 | SPEC:64 | Typical | `status: succeeded` or `partial` | succeeded | `--outcome succeeded`, first sentence states the status | OK |
| G3 | SPEC:63-64 | Maximum/Overflow | `status: blocked`, empty `blocked_question` | failed | `--outcome failed` (run: assertion fails) | OK |
| G3 | SPEC:63-64 | Sentinel Value Match | existing contract with a `status` word outside the four | failed | `--outcome failed` even on a healthy run; vocabularies never inventoried (note 22) | OK |
| G3 | SPEC:64, 85, 97, 215, 227 | Legitimate Edge Case | a ready command run before its phase adds the contract (troubleshoot `REPORT.md`, release-split report, cleanup-audit summary) | no YAML | Outcome and AC-0.4 steps 3-4 are defined over a contract that does not exist yet | GAP (N2) |
| G4 stale contract | SPEC:63 | Zero/Empty | no earlier contract | none | Nothing to remove | OK |
| G4 | SPEC:63 | One/Minimal | retry of the same Task, earlier contract at the same path | stale | Removed before other work | OK |
| G4 | SPEC:63 | Typical | normal first run | fresh | Written on every outcome | OK |
| G4 | SPEC:74, 216 | Maximum/Overflow | retry dies before the command starts | old file | Older than the dispatch, not read as the outcome | OK |
| G4 | SPEC:70, 74, 216 | Sentinel Value Match | a contract written by a sibling Task after this dispatch started | newer than dispatch | Passes the mtime test; step 4 checks `command` non-empty, not equal to this Task's command line | GAP (N4) |
| G4 | SPEC:63 | Legitimate Edge Case | cli-portify reads its contract, then replaces it | resume | Read first, then replaced; a crash between leaves an older file, caught by mtime | OK |
| G5 retry and re-run | SPEC:65 | Zero/Empty | retry of a Task whose first attempt wrote nothing | clean | Starts clean | OK |
| G5 | SPEC:65 | One/Minimal | command with a resume flag, retry given the flag | resume | Resumes from disk state | OK |
| G5 | SPEC:65, 105-131 | Typical | command without a resume flag ("fresh dir" in 16 rows of 3.2 and 3 of 3.1) | re-run | Sentence 1: new fresh output directory; sentence 3: same path as the first attempt; contract path under each differs | GAP (N3) |
| G5 | SPEC:65, 91-92 | Maximum/Overflow | fixed-output command (cleanup-audit, index-repo) retried | same dir | One attempt at a time per worktree | OK |
| G5 | SPEC:65, 326 | Sentinel Value Match | `--retry-of` with changed Task text | unknown | UNVERIFIED 18; WC-6 does not rely on it | OK |
| G5 | SPEC:65 | Legitimate Edge Case | third consecutive failed start | breaker | Not routed around (CAPS:116) | OK |
| G6 gate resolution | SPEC:61 | Zero/Empty | gate with no default and no caller flag | blocked | `status: blocked` plus question, stop | OK |
| G6 | SPEC:61 | One/Minimal | caller flag answers the gate | resolved | (b) | OK |
| G6 | SPEC:61, 122 | Typical | documented default only | resolved | (a) | OK |
| G6 | SPEC:61 | Maximum/Overflow | several gates block one run (cli-eval three, cli-portify three) | blocked | `blocked_question` lists every unresolved gate visible at the stop | OK |
| G6 | SPEC:61, 122 | Sentinel Value Match | caller flag that itself opens a gate (`/sc:research ... --strategy intent`) while a default exists | conflict | (b) beats (a) says honour the flag, which asks questions; row 122 "pins planning" says the flag is overridden | GAP (N5) |
| G6 | SPEC:111 | Legitimate Edge Case | gate answerable only from a mid-run artifact (cli-portify) | blocked | Stop naming the artifact; `--resume <contract>` added in P2 | OK |
| G7 wait limit | SPEC:69 | Zero/Empty | no blocking call | none | No heartbeat issue | OK |
| G7 | SPEC:69 | One/Minimal | one call of 1 minute | below | No split | OK |
| G7 | SPEC:69 | Typical | one call of 3 minutes | below | No split | OK |
| G7 | SPEC:69, 243 | Maximum/Overflow | one call of 4.5 minutes | above 240 s | Must be split (WC-10 and AC-4.3 now agree) | OK |
| G7 | SPEC:69 | Sentinel Value Match | parallel Agent-tool batch over 5 minutes | exempt | Exempt, silence not read as stall | OK |
| G7 | SPEC:69, 107, 110, 129 | Legitimate Edge Case | one foreground build, test run or eval over 4 minutes | above 240 s | Rule says "split"; build and test rows give no way to; only cli-eval does (N6, minor: the rule is stated, the means are not) | OK |

Table result: 42 rows, 6 GAP (G2 two, G3 one, G4 one, G5 one, G6 one), mapped to blocking findings N1, N2, N3, N4 and N5. The round-1 table had 15 GAP rows; the revision closed those it named.

### Quantity Flow Diagram (Pipeline Dimensional Analysis)

Trigger: the spec filters 43 commands into groups, then phases, then contract-bearing sections, and the counts change at each stage. Fowler annotated the counts; Whittaker attacked each divergence. My re-count from the rows (not from `DISP`):

```text
[Source: 43 commands = 21 INV-A + 22 INV-B]                       (SPEC:82)
   --> [Stage 1: section 4 filter] --> 6 coordinator-only          (SPEC:151-156)
   --> 37 worker-capable                      (N=43 in, M=37 out, divergence 6, accounted)
         |-- 10 ready today                                        (SPEC:89-98)
         `-- 27 needs a change                                     (SPEC:105-131)
   --> [Stage 2: phase assignment]
         P1: 8 needs-change + 6 ready = 14 with a section; load gets a usage-line fix only   (SPEC:178)
         P2: 11 needs-change + 4 ready = 15                         (SPEC:179)
         P3: 4                                                      (SPEC:180)
         P4: 3 (pr-submit only under D3 b)                          (SPEC:181)
         check: 14 + 15 + 4 + 3 = 36 = 37 - load                    OK
   --> [Consumer A: AC-1.1 asserts per phase over the explicit lists]   14, then +15, +4, +3   (SPEC:228)   conserved
   --> [Stage 3: 36 section-bearing commands --> contract location stated]
         23 name a flag or a place the WC-4 rule can use
          2 imply a flag without naming it (explain, recommend)
         11 name neither (cleanup-audit, index-repo, cli-eval, cli-portify, research, review-translation,
            task, tasklist, save, validate-roadmap, validate-tests)
   --> [Consumer B: WC-4 "known before dispatch", step 4 of 7.2 `test -s <contract>`, AC-2.2, AC-2.3]  expects 36   <-- MISMATCH (N1)
   --> [Consumer C: "fresh dir" Resume column]  16 rows of 3.2 + 3 rows of 3.1 expect a fresh directory while WC-6 sentence 3 gives the same path   <-- MISMATCH (N3)
```

Divergence result: the round-1 mismatch (AC-1.1 expecting 37) is closed; the 43 to 37 to 36 counts conserve. Consumers B and C do not conserve. Findings N1 and N3 (blocking under FR-19 reasoning, graded MAJOR with concrete outcomes below).

=== REQUIREMENTS ANALYSIS ===

Each finding: issue, severity, expert, recommendation with rationale, priority, quality-impact estimate.

**N1. WC-4 promises a contract path "known before dispatch" in every case; 11 rows give no place and 2 name no flag.** Severity MAJOR, blocking (FR-8 GAP row G2-2; concrete wrong outcome below). Expert: Wiegers (completeness, testability). Spec: section 2.2 WC-4, section 2.3, section 3.1 and 3.2 report columns, 7.2 step 4, AC-1.1, AC-2.2, AC-2.3.
Issue: WC-4 (SPEC:63) sets three placement cases, then states "In every other case the path is known before dispatch", and 2.3 (SPEC:74) says the brief's output location fixes the contract path by that rule. Case iii requires a command with a fixed subdirectory or generated id to "name its contract path in its section 3 row". Eleven rows do neither and have no output flag the rule can use: cleanup-audit (SPEC:91, fixed `.claude-audit/`), index-repo (SPEC:92, "State the output location"), cli-eval (SPEC:110, "contract for both pipelines", outputs under `.dev/eval-workspaces/...` and `.dev/eval-runs/<date>/<run-id>/`, INV-A:44), cli-portify (SPEC:111, the row says "file location unnamed"), research (SPEC:122, generated `claudedocs/research_[topic]_[timestamp].md`, INV-B:132), review-translation (SPEC:123, run-time suffixes, INV-B:142), task (SPEC:127), tasklist (SPEC:128, `TASKLIST_ROOT` default `.dev/releases/current/<segment>/`, INV-B:212), save (SPEC:125), validate-roadmap (SPEC:130), validate-tests (SPEC:131, which gains the section in P3 yet its row mentions no contract at all). Two more (explain, SPEC:114; recommend, SPEC:121) say "write ... to a file; contract" without naming a flag, so the directory-valued rule of WC-4 cannot be applied.
Concrete wrong outcome: three implementers of `research`, `save` and `task` put the contract in the working directory, in `claudedocs/` and in `.dev/...`. The coordinator cannot build `<contract>` for 7.2 step 4 or `--report-path`; AC-2.2 and AC-2.3 cannot be run for these commands; AC-1.1 (SPEC:228) requires cleanup-audit and index-repo to name `return-contract.yaml` in P1 with no place to write it.
Recommendation: in each of the 13 rows add the flag (name, directory-valued) the brief must pass, or the fixed contract path, or "worker reports the generated path" per WC-4 iii; add the output flag to the "Brief must pass" column of 3.1 for reflect and troubleshoot, whose default output directories carry a timestamp (INV-B:112, INV-B:242), and for release-split, whose default is derived from the spec directory (INV-B:122). Rationale: WC-4's promise is what makes step 4 of 7.2 checkable. Priority High. Quality impact: Completeness +1, Testability +1.

**N2. AC-0.4 and WC-5 cannot be evaluated for the P0 smoke runs.** Severity MAJOR, blocking (FR-8 GAP row G3-6; concrete wrong outcome below). Expert: Adzic (specification by example). Spec: section 2.2 WC-5, section 3.1 intro, section 6 P0, AC-0.4, 7.2 steps 3-4.
Issue: AC-0.4 (SPEC:227) passes when steps 1-3 and 5-7 pass and "step 4 uses the command's existing report file". Step 3 (SPEC:215) requires that the worker's `--outcome` "matches the contract's status under WC-5" and that its report path "is the WC-4 contract path". In P0 no smoke command has a contract at a WC-4 path: troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242; the always-write change is P2, SPEC:97), adversarial's contract filename is not fixed until P1 (SPEC:89, INV-A:60), and workflow's exists but its `status` values are not inventoried (note 22). WC-5 (SPEC:64) is defined only over a parseable YAML file with a `status` in the four values; `REPORT.md` is markdown. Section 3.1 (SPEC:85) says only that "the worker reports the named file until the command's phase adds the contract" and gives no outcome rule for that file.
Scenario. Given `/sc:troubleshoot "login fails"` finishes and writes `REPORT.md` only. When the worker applies WC-5 as written. Then the file is "not parseable YAML", so `--outcome failed` for a healthy run; if instead the worker uses judgement, step 3's "matches the contract's status" has nothing to match.
Concrete wrong outcome: P0, the phase meant to close evidence gap 1.4 (1) and whose failure "reopens section 1" (SPEC:227), either records a false failure on a correct run or is passed by a reader who skips the undefined clause. The decision under test is judged by an undefined rule.
Recommendation: add to 3.1 and WC-5 the outcome rule for a command with no contract (for example: `succeeded` when the named report exists, is non-empty and the command ended without a halt; otherwise `failed`), and restate AC-0.4 steps 3 and 4 over "the report file named in the 3.1 row". Priority High. Quality impact: Testability +2, Consistency +1.

=== ARCHITECTURE ANALYSIS ===

**N6. WC-10 states a limit with no means for single long subprocess calls.** Severity MAJOR graded minor (no concrete wrong outcome: silence is never read as a stall, CAPS:125; Orca's use of heartbeats is UNVERIFIED, SPEC:325). Expert: Nygard. Spec: WC-10 (SPEC:69), build (SPEC:107), test (SPEC:129), AC-4.3.
Issue: WC-10 asks that no single tool call block for over 240 s and exempts only parallel Agent-tool batches. `/sc:build` and `/sc:test` run the project's build or test command (INV-A:40, INV-B:48, INV-B:234), usually one foreground call, and their rows say nothing about splitting it. Only cli-eval (SPEC:110) and pr-submit (SPEC:120) are handled, and AC-4.3 checks the limit for pr-submit alone (D3 b). Recommendation: add "background the job and poll" to the build and test rows, or exempt them with the stated reason. Priority Low. Quality impact: Consistency +0.5.

**N7. The workflow-to-reflect hand-over has no owning phase.** Severity MINOR. Expert: Hohpe. Spec: section 3.3 workflow row (SPEC:143), section 6 P1 and P2.
Issue: workflow is edited in P1 (SPEC:178) and reflect gains its section in P2 (SPEC:179). The 3.3 row says "pass the flag once reflect has it", but P2 lists neither workflow nor a re-edit, and SA-4 keeps Phase 1-3 edits additive. Nobody adds the line to workflow's section. Harmless today because workflow's reflect run fires no gate (INV-B:269). Recommendation: list "workflow: one added line" in the P2 row or drop the sentence. Priority Low.

**N8. Section 3.3 omits chains the inventories show.** Severity MINOR. Expert: Hohpe. Spec: section 3.3 (SPEC:133-144).
Issue: omitted: tasklist Stage 9 calling `sc:task --compliance strict` (INV-B:211), roadmap calling `sc:save` at every wave (INV-B:154; the save default writes single-owner keys, WC-11) and adversarial (INV-B:151), pr-submit calling `sc:troubleshoot-protocol` per finding and an auggie-review fallback (INV-B:91). The table promises that chains with gates are listed. SPEC:134 lets a phase add chains it finds, so this is minor. Recommendation: add the four rows. Priority Low.

**N9. The support check reads the coordinator's filesystem only.** Severity MINOR. Expert: Newman. Spec: section 2.3 (SPEC:78), non-goal 9 (SPEC:254).
Issue: a worker started with `--on <environment>` (CAPS:128) runs against that host's install. The check names `~/.claude/commands/sc/<name>.md` or `.claude/commands/sc/<name>.md` without saying whose. Non-goal 9 leaves remote workers to the coordinator but does not say the check is local-only. A remote worker with an older install runs attended and stalls silently, the case finding 6 was about. Recommendation: one sentence: the check is valid only for workers on the coordinator's host, otherwise run it on the worker's host. Priority Low.

**N10. WC-9's opening sentence and its class list differ.** Severity MINOR. Expert: Wiegers. Spec: WC-9 (SPEC:68).
Issue: the first sentence turns off any default that "pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run"; the list of flag classes is "VM provisioning, real-target install, commit, push, PR, GitHub post". "Paid external run" has no class and no flag, and "commit" appears only in the list. Web search in research (INV-B:134) and review-translation (INV-B:144) is a paid external call; read literally it is off with no way to turn it on, or it is on and the sentence is wrong. Recommendation: make the sentence and the class list the same set and say whether web search counts. Priority Low.

**N11. Output-location validity is unspecified.** Severity MINOR. Expert: Nygard. Spec: WC-4 (SPEC:63).
Issue: WC-4 handles an absent location, not an unwritable one, one inside `.git/`, or one under the distributable skill, agent or command folders of a `.claude/` folder. The sandbox's own spec-panel section treats all of these as "no report directory known" and refuses before any work (CMD:456). Here the run proceeds and fails later; WC-5 then maps the missing contract to `failed`, which is safe but late. Recommendation: apply the same refusal. Priority Low.

**N12. The census, E5 and the AC-C1 baseline may be stale (UNVERIFIED).** Severity MAJOR graded minor, only because the evidence is outside the workspace; if confirmed it is MAJOR. Expert: Fowler. Spec: E5 (SPEC:26), SA-2 (SPEC:166), AC-C1 (SPEC:191), section 3 intro (SPEC:82).
Issue: the grep behind E5 and the 43-command count are dated 2026-11-02 and cannot be re-run here. The skill listing loaded in this session, which is not a workspace file, shows `sc:issue` (described as creating an Orca worktree and launching an agent in it), `sc:graph` and `sc:impact`. None is in INV-A:3 or INV-B:3. If `sc-issue-protocol` text contains `orca worktree`, AC-C1 prints a line on the unmodified tree and no phase can pass it, and the 43 count is short by three. Recommendation: re-run the E5 grep and `ls src/superclaude/commands` at the start of P0 and record the result. Priority Medium.

**N13. AC-C5 and AC-0.3 see committed changes only.** Severity MINOR. Expert: Crispin. Spec: code block 2 (SPEC:208).
Issue: `git diff -U0 master...HEAD` compares the merge-base with `HEAD`; edits not yet committed do not appear, so the check prints nothing before the phase is committed and passes vacuously. AC-C4 uses `--cached` (SPEC:194), so the two checks look at different states. Reasoned from git semantics; not run here. Recommendation: `git diff -U0 master -- <path>` (working tree against master) or say the check runs after the phase commit. Priority Low.

**N14. AC-1.2 gives every P1 command the same flags.** Severity MINOR. Expert: Crispin. Spec: AC-1.2 (SPEC:229).
Issue: it says run the live check "with `--unattended --output <dir>`", but cleanup-audit takes `--pass <N>` (SPEC:91), index-repo takes nothing (SPEC:92), init-lite's `--output` is a file (SPEC:93) and workflow has no output flag (SPEC:98). Recommendation: "with the flags of its 3.1 or 3.2 row". Priority Low.

**N15. spec-panel row and the sandbox's own `## Unattended mode` section disagree with WC-2 and WC-4.** Severity MINOR (which file is newer is UNVERIFIED). Expert: Newman. Spec: WC-2 (SPEC:61), WC-4 (SPEC:63), spec-panel row (SPEC:126).
Issue: SPEC:126 says "add `--output`" and WC-4 makes every new output flag directory-valued, so `--output` is a directory for analyze and spec-panel but a file for tdd and init-lite. CMD:456 uses `--report-dir` for the directory and keeps `--output` file-valued; CMD:458 says no person-mode flag is refused and `--mode socratic` only writes its questions into the report, while WC-2 says every command with `--mode socratic` refuses it. The line numbers cited at SPEC:126 (`cmd/spec-panel.md:22,34-35,222,451,455`) do not match CMD (for example CMD:224 is the Write line), so CMD is a later or different version. Recommendation: reconcile before P2 and give new directory flags a name that is not `--output`. Priority Medium.

**N16. AC-2.2 conflicts with WC-3's optional `ask`.** Severity MINOR. Expert: Crispin. Spec: WC-3 (SPEC:62), AC-2.2 (SPEC:233).
Issue: a gate-trigger run expects `worker_done --outcome failed`; a worker that follows WC-3 ("may instead ask the coordinator") sends a `question`, and step 3 waits on either. The result depends on what the worker chooses. Recommendation: say the test brief forbids `ask`. Priority Low.

**N17. WC-2 and WC-4 are not atomic.** Severity MINOR. Expert: Wiegers. Spec: SPEC:61, SPEC:63.
Issue: WC-2 carries three resolution routes, a precedence rule, a list rule, a person-mode refusal rule and a propagation rule in one cell; WC-4 carries placement, a refusal, a stale-file rule, a field list and the `--report-path` duty, about 370 words. Acceptance checks cite "WC-2 (c)" and "WC-4 (ii)", so sub-parts are already addressed by letter, but a failing check cannot name the sub-requirement. Recommendation: give the sub-parts ids without adding rules. Priority Low.

**N18. Revision text without finding ids.** Severity MINOR. Expert: Wiegers. Spec: SPEC:96, SPEC:119, SPEC:177, SPEC:233.
Issue: the reviser contract (CMD:263) says each added paragraph or table cites its finding id. The tdd row stem rule, the post-release flag text, the P0 row additions and the AC-2.2 example carry no id (the matching entries are in `DISP`). Recommendation: add the ids. Priority Low.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Scope: specification correctness only; resilience patterns and test strategy stay with Nygard and Crispin. The boundary table above carries the zero, sentinel and divergence probes row by row; the three attacks below are the ones that survive it.

**N3. I can break this specification by Sequence Attack on a retry.** The invariant at **WC-6 (SPEC:65) and the "Resume (WC-6)" column of section 3 (SPEC:105-131, 89, 94, 97)** fails when **a command with no resume flag is retried by `worker-start --retry-of`.** Severity MAJOR, blocking (FR-8 GAP row G5-3). Expert: Whittaker with Fowler.
Concrete attack. WC-6 sentence 1 requires that a retry "must not corrupt the first attempt's output" and that a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean". Sentence 3 says "A retry reuses its Task's text, so it gets the same output path", and that the spec "relies on the stale-contract removal in WC-4, not on a new directory". State trace for `/sc:analyze` (a "fresh dir" row, SPEC:105), Task T with `--output D/`: attempt 1 writes `D/report.md` and `D/return-contract.yaml` (`failed`), then dies. Attempt 2 starts with the same `D/`. Reading by sentence 1: it creates a fresh subdirectory, so its contract lands in `D/<fresh>/return-contract.yaml`, which the coordinator, who computed `D/return-contract.yaml` by WC-4 i, never opens; the removal rule then acts on a different path. Reading by sentence 3: it overwrites `D/`, so the first attempt's output is not preserved, which sentence 1 forbids. 16 rows of 3.2 and 3 rows of 3.1 say "fresh dir"; each can be implemented either way.
Recommendation: replace sentence 1 by the rule the spec relies on: a retry runs in the same location, the command removes its old contract and overwrites its own outputs, and a coordinator that wants the first attempt kept gives the retry a new Task and path. Define or drop "fresh dir" in the column. Priority High. Quality impact: Consistency +1, Testability +1.

**N4. I can break this specification by Sequence Attack and Accumulation Attack on a shared output location.** The invariant at **WC-4 stale-file removal (SPEC:63), the coordinator's staleness test (SPEC:74) and step 4 of 7.2 (SPEC:216)** fails when **two Tasks are given the same output location.** Severity MAJOR, blocking (FR-8 GAP rows G2-4 and G4-5). Expert: Whittaker.
Concrete attack. The coordinator creates Tasks A and B for `/sc:analyze` with the same `--output .dev/out/`; nothing in 2.3 asks for one location per Task, and WC-11 (SPEC:70) covers only default paths. t0: A starts and removes `.dev/out/return-contract.yaml`. t1: B starts and removes it again. t2: B finishes and writes `status: succeeded`. t3: A dies before writing. The coordinator opens A's path: the file exists, its mtime is later than A's `worker-start`, it parses, `status` is in the set, `command` is non-empty (the assertion at SPEC:216 checks non-empty, not equal to A's command line). A is accepted as succeeded on B's contract. Variant: A starts after B finished and removes B's contract before B's worker reads it, so B's outcome becomes `failed`.
Recommendation: add to 2.3 a duty that each Task has its own output location (never shared by concurrent or sibling Tasks), and make step 4 compare the contract's `command` with the Task's exact command line, which the contract already carries (WC-4). Priority High. Quality impact: Testability +1, Consistency +1.

**N5. I can break this specification by Divergence Attack on gate resolution.** The invariant at **WC-2 (SPEC:61) against the research row (SPEC:122)** fails when **a caller flag would itself open a gate.** Severity MAJOR, blocking (FR-8 GAP row G6-5). Expert: Whittaker.
Concrete attack. Brief: `/sc:research "topic" --unattended --strategy intent`. WC-2 says the command "never" asks, and says a caller's flag "always beats a documented default". The research row says `--unattended` "pins `--strategy planning` (the strategy that runs without clarification)". Reading 1: pin = default, the caller's `intent` wins, the persona asks "clarifying questions first" (INV-B:129) and the worker stalls silently, the failure WC-2 exists to prevent. Reading 2: pin = forced, the caller's flag is silently ignored and (b) is false for this command. The refusal list in WC-2 names four person-mode flags and not `--strategy`. This is the example the round-1 panel used for finding 14 (PANEL:217); the revision settled the order and left the example failing.
Recommendation: add to WC-2 that a caller flag which opens a gate the command cannot resolve unattended is refused like the person-mode flags (`status: failed`, reason), and make the research row say it refuses `--strategy intent` and `--strategy unified` and whether `planning` is a default or a forced value. Priority High. Quality impact: Completeness +1, Consistency +1.

=== CONSENSUS AND DISAGREEMENTS ===

Consensus.
- All 14 round-1 blocking findings are resolved as named. The decision, the rejected alternative and the evidence-gap statement stay the strongest parts. Counts conserve (43, 37, 36, 14/15/4/3).
- The remaining blocking defects all sit in the contract path and outcome machinery that the revision added or tightened: where the contract is (N1), what it means before it exists (N2), what a retry does (N3), whose file it is (N4) and which flags may open a gate (N5).
- The acceptance checks are now mechanically sound for what they test (F8, F9 verified by run); N2, N13, N14 and N16 are about what they do not reach.

Disagreements.
- Nygard would grade N6 up (a 12-minute test run with no heartbeat); Whittaker and Crispin keep it minor because the spec already forbids reading silence as a stall (CAPS:125) and Orca's use of heartbeat age is UNVERIFIED (SPEC:325).
- Wiegers wants N17 (atomic ids) addressed with N1; Adzic holds that it is a notes item and must not trigger a revision (Review Loop 2).

Positive checks (nothing to fix): AC-1.1 is now satisfiable and phase-scoped; the AC-C5 and AC-C1 pipes behave as described when run on sample input; the step-4 Python assertion rejects empty, list-valued and empty-question inputs; the support check, start instruction and propagation table are specific and carry UNVERIFIED markers where the evidence stops (items 15-18); D1-D5 each carry options and a recommendation; the Decisions and UNVERIFIED sections the README requires are present.

### Standard-format summary

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-10
  expert_panel: [wiegers, adzic, cockburn, fowler, nygard, whittaker, newman, hohpe, crispin]
  focus_areas: [requirements, architecture]
quality_assessment:
  overall_score: 6.3     # round 1 scored 5.8
  clarity: 7
  completeness: 6        # contract location (N1), pre-contract outcome (N2)
  testability: 6         # AC-C1, AC-C5, step 4 verified by run; AC-0.4 not satisfiable (N2)
  consistency: 6         # WC-6 vs itself (N3), WC-2 vs research row (N5)
critical_issues:
  blocking: [N1, N2, N3, N4, N5]
  non_blocking: [N6, N7, N8, N9, N10, N11, N12, N13, N14, N15, N16, N17, N18]
expert_consensus:
  - Round-1 blocking findings 1-14 are resolved as named; counts conserve.
  - The remaining blocking defects sit in the contract path and outcome machinery that the revision added.
improvement_roadmap:
  immediate: [N1, N2, N3, N4, N5]
  short_term: [N12, N15, N9]
  long_term: [N6, N7, N8, N10, N11, N13, N14, N16, N17, N18]
adversarial_analysis: see === ADVERSARIAL ANALYSIS (Whittaker) === (N3, N4, N5)
```

## Numbered list of new findings

Evidence column paths expand as in the shorthand at the top. Findings N1 and N2 are in the requirements analysis, N6 to N18 in the architecture analysis, N3 to N5 in the adversarial analysis.

| # | Finding | Severity | Blocking | Spec section | Evidence path:line |
|---|---|---|---|---|---|
| N1 | WC-4 says the contract path is known before dispatch in every case; 11 rows of section 3 give no flag or place and 2 name no flag (cleanup-audit, index-repo, cli-eval, cli-portify, research, review-translation, task, tasklist, save, validate-roadmap, validate-tests; explain, recommend), so step 4 of 7.2, AC-2.2 and AC-2.3 cannot name a contract path | MAJOR | yes (FR-8 GAP G2-2; concrete outcome: implementers pick different places) | 2.2 WC-4; 2.3; 3.1; 3.2; 7.2 step 4; AC-1.1 | SPEC:63, 74, 91, 92, 110, 111, 114, 121-123, 125, 127, 128, 130, 131, 216, 228, 233-234; INV-A:44, INV-B:132, INV-B:142, INV-B:212 |
| N2 | AC-0.4 steps 3-4 and WC-5 are defined over a YAML contract that does not exist for the P0 smoke commands (troubleshoot has only `REPORT.md`, adversarial's filename is unfixed, workflow's status values are unknown); a healthy run maps to `failed` or the check cannot be evaluated | MAJOR | yes (FR-8 GAP G3-6; concrete outcome: P0 gives a false result) | 2.2 WC-5; 3.1 intro; 6 P0; AC-0.4 | SPEC:64, 85, 89, 97, 177, 215-216, 227; INV-B:242, INV-A:60, INV-B:272 |
| N3 | WC-6 sentence 1 (fresh output directory, do not corrupt the first attempt) contradicts sentence 3 (same path, rely on stale-file removal); 16 "fresh dir" rows of 3.2 and 3 of 3.1 can be built either way, one of which puts the contract where the coordinator does not look | MAJOR | yes (FR-8 GAP G5-3) | 2.2 WC-6; 3.1; 3.2 Resume column | SPEC:63, 65, 74, 89, 94, 97, 105-110, 112-114, 116-117, 119, 126-129 |
| N4 | A contract is judged stale by mtime alone and removed at start, with no duty for one output location per Task; a sibling Task's contract (newer than this dispatch) is accepted as this worker's outcome, or deleted before it is read; step 4 checks `command` is non-empty, not that it matches the Task | MAJOR | yes (FR-8 GAP G2-4, G4-5) | 2.2 WC-4, WC-11; 2.3; 7.2 step 4 | SPEC:63, 70, 74, 216 |
| N5 | WC-2 precedence (caller flag beats default) and the research row ("pins `--strategy planning`") give opposite results for `--strategy intent`; a caller flag that opens a gate is neither answered nor refused, so the worker stalls or the flag is ignored | MAJOR | yes (FR-8 GAP G6-5; concrete outcome: silent stall) | 2.2 WC-2; 3.2 research | SPEC:61, 122; INV-B:129, INV-B:38; PANEL:217 |
| N6 | WC-10 states the 240 s limit but gives no means for a single long build, test or eval call; AC-4.3 checks it only for pr-submit under D3 (b) | MAJOR graded minor | no | 2.2 WC-10; 3.2 build, test | SPEC:69, 107, 129, 243, 325; INV-A:40, INV-B:48, INV-B:234, CAPS:125 |
| N7 | The workflow-to-reflect flag hand-over (3.3) has no owning phase; workflow is edited in P1 only | MINOR | no | 3.3; 6 | SPEC:143, 178-179 |
| N8 | Section 3.3 omits tasklist to task (Stage 9), roadmap to save and adversarial, and pr-submit to troubleshoot and auggie-review | MINOR | no | 3.3 | SPEC:133-144; INV-B:211, INV-B:154, INV-B:151, INV-B:91 |
| N9 | The support check reads the coordinator's filesystem; a remote worker (`--on`) uses another install | MINOR | no | 2.3; 8 non-goal 9 | SPEC:78, 254; CAPS:128 |
| N10 | WC-9's opening sentence lists "calls a paid external run" among default-off actions; the class list has no such class and adds "commit"; research and review-translation web search is a paid call | MINOR | no | 2.2 WC-9 | SPEC:68, 122-123; INV-B:134, INV-B:144 |
| N11 | WC-4 handles an absent output location only; an unwritable one, one inside `.git/` or under the distributable `.claude` folders is unspecified (the sandbox's spec-panel section refuses all of these) | MINOR | no | 2.2 WC-4 | SPEC:63; CMD:456 |
| N12 | E5, SA-2, AC-C1 and the 43-command census cannot be re-run here; the session's skill listing shows `sc:issue` (Orca worktree), `sc:graph`, `sc:impact`, absent from both inventories (UNVERIFIED) | MAJOR graded minor (evidence outside the workspace) | no | 1.2 E5; 3; 5 SA-2; 7.1 AC-C1 | SPEC:26, 82, 166, 191; INV-A:3, INV-B:3 |
| N13 | AC-C5 and AC-0.3 use `master...HEAD`, which ignores uncommitted edits, while AC-C4 uses `--cached` | MINOR | no | 7.1 code block 2; AC-0.3 | SPEC:194-195, 208, 226 |
| N14 | AC-1.2 runs each P1 command "with `--unattended --output <dir>`", which four of the 14 do not take | MINOR | no | 7.3 AC-1.2 | SPEC:91-93, 98, 229 |
| N15 | spec-panel row and WC-2/WC-4 disagree with the sandbox's implemented `## Unattended mode` section on the `--output` meaning and on refusing `--mode socratic`; one flag name carries two meanings across commands | MINOR | no | 2.2 WC-2, WC-4; 3.2 spec-panel | SPEC:61, 63, 126; CMD:456, 458, 224 |
| N16 | AC-2.2 expects `worker_done --outcome failed` but WC-3 lets the worker `ask` instead | MINOR | no | 2.2 WC-3; AC-2.2 | SPEC:62, 233 |
| N17 | WC-2 and WC-4 each bundle five to nine obligations in one cell, so a failing check cannot name the sub-requirement | MINOR | no | 2.2 | SPEC:61, 63 |
| N18 | Revision text without a finding id (tdd row, post-release row, P0 row, AC-2.2 example) against the reviser contract | MINOR | no | 3.1; 3.2; 6; 7.3 | SPEC:96, 119, 177, 233; CMD:263 |

Totals: 0 CRITICAL, 5 MAJOR blocking (N1 to N5), 2 MAJOR graded minor (N6, N12), 11 MINOR. Blocking findings open: N1 to N5. Round-1 notes 15 to 24 remain open and unchanged.

Citation-check summary (Part 2): 11 items in 2A, none blocking on its own; C1 (pr-submit poll structure) and C6 (`--post-pr`) matter because WC-10, WC-9 and D3 (b) depend on them.

## Verdict

The revision resolves all 14 round-1 blocking findings as named, and the checks that were wrong in round 1 (AC-C1, AC-C5, step 4) now behave as the spec says. It adds five blocking defects, all in the machinery it introduced or tightened: the contract path (N1), the outcome before a contract exists (N2), the retry rule (N3), shared-location contracts (N4) and gate-opening caller flags (N5). The brief's rule (any finding is FAIL) and Review Loop bullet 2 (a blocking finding is open) both give FAIL. No Self-Audit is required for a FAIL verdict.

Reviser brief

Blocking finding ids: N1, N2, N3, N4, N5. The reviser reads this report, not the command, so the rules are restated here. Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. The reviser reports the byte size of the spec before and after (before this revision: 71195 bytes, 326 lines). Findings N6 to N18 and round-1 notes 15 to 24 are notes and never trigger a revision. A brief may narrow this scope but may not widen it past the changed lines and the prior blocking findings, and may not grade a minor finding as blocking. At most 2 fix cycles remain by the report header (this is `review: 1 of 3` by the command's count; the coordinator keeps the real count); at review 3 with a FAIL verdict the run escalates to the user instead of revising.

verdict: FAIL
