review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (first review, critique mode, focus requirements,architecture)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (`SPEC:N` = line N of it)
- candidate sha256: `7a4862cc38412204ffb4afcc88a846d7268c3e6c8447b8a5b344d795ad99f4df`
- baseline: not given, none needed (first review of the whole document; labelled whole-document audit, not a re-review)
- reviewer model used: claude-sonnet-5-5
- prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full)
- evidence checkable here: `.dev/orca-command-refactor/README.md`, `inventory/commands-a.md` (`INV-A`), `inventory/commands-b.md` (`INV-B`), `inventory/orca-capabilities.md` (`CAPS`). Every citation of `CLAUDE.md`, `src/...`, `Makefile`, `pyproject.toml`, `plugins/...`, `.dev/codegraph-migration/...` or `.dev/evals/...` is UNVERIFIED (no such file in the workspace); where an inventory quotes the same line I say so.
- `--unattended` not passed: the "ask the user once whether to open an issue" step is not performed by this worker; follow-up candidates are only recorded below.

## Coverage
Read in full: command.md, the review-loop prompt file, README, the whole candidate. Checked against inventories: the 10/27/6 split (counts add up: INV-A:73 has 5/13/3, INV-B:278 has 5/14/3; SPEC:76-137 lists 10+27+6=43 distinct commands, matching INV-A:3/INV-B:3 scopes), CAPS lines behind E1-E4, R1-R5, WC-1/3/4/5/10, the INV-A/INV-B lines cited in section 3 and 4, and the Phase/AC consistency of sections 2, 3, 6 and 7. Not covered: any claim whose only source is a file outside the workspace (see UNVERIFIED list). Pipeline Dimensional Analysis not triggered (no data pipeline with count divergence; the only count flow is the 43 split, which adds up). `--focus correctness` not active, so no State Variable Registry.

## Findings summary
| id | severity | grade | expert | where |
|---|---|---|---|---|
| R-1 | MAJOR | blocking | Wiegers | WC-5 vs section 3.1 vs section 6 |
| R-2 | MAJOR | blocking | Crispin / Whittaker | AC-C5 (SPEC:176) |
| R-3 | MAJOR | Medium | Wiegers / Cockburn | contract path dir vs file (SPEC:62, 76, 99-115) |
| R-4 | MAJOR | Medium | Nygard / Whittaker | WC-10 vs WC-7 (SPEC:65, 68) |
| R-5 | MAJOR | Medium | Fowler | WC-3 re-invoke vs WC-6 (SPEC:61, 64) |
| R-6 | MINOR | Medium | Wiegers | P1 membership of "fix" commands (SPEC:159, 200) |
| R-7 | MAJOR | Medium | Fowler / Cockburn | how a preamble-wrapped brief invokes a `/sc:` command (SPEC:16, 65) |
| R-8 | MAJOR | Medium | Whittaker | stale-contract / freshness (SPEC:62-64) |
| R-9 | MINOR | Medium | Hohpe | Phase 2 vs D4 dependency (SPEC:154, 249) |
| R-10 | MINOR | Medium | Adzic | workflow row, two contract locations (SPEC:92) |
| R-11 | MINOR | Medium | Crispin | AC-C1 regex narrower than SA-2; census staleness (SPEC:147, 180) |
| N-1..N-4 | MINOR | note | various | see follow-up candidates |

## === REQUIREMENTS ANALYSIS ===

### R-1 (blocking, MAJOR, Wiegers): WC-5 fails successful runs of commands that have no contract until P2
Grading sentence: an implementer who follows the stated text builds a coordinator that, from Phase 1 on, sends `--outcome failed` for every worker whose contract is absent (SPEC:63), and the stated phase plan gives `/sc:tdd`, `/sc:troubleshoot` and `/sc:release-split` no contract until Phase 2 (SPEC:160) while section 3.1 says they "run as workers now" (SPEC:79); a successful troubleshoot, tdd or release-split run between P1 and P2 is therefore reported failed, which is wrong because the run succeeded and left a usable report.
- Contradicting texts: SPEC:63 ("From P1 on (P0 runs have no contract ...) `--outcome failed` when the contract is absent"); SPEC:79 ("the worker reports the named file until Phase 1 adds the contract"); SPEC:159 (P1 list contains none of tdd, troubleshoot, release-split); SPEC:160 (they are P2). SPEC:79 is itself wrong for these three: Phase 1 does not add their contract.
- Evidence the contract is really absent: tdd's report is "the TDD at --output" (SPEC:90; INV-B:47 (d)); release-split's is `release-split-report.md` (SPEC:89; INV-B:37 (d)); troubleshoot writes `return-contract.yaml` only with `--caller task-unified` (INV-B:242), a flag the spec never mentions, and the 3.1 row names only `REPORT.md` (SPEC:91).
- Recommendation: either state in WC-5 that the "contract absent means failed" rule applies per command from the phase that gives that command its contract (P1 list for P1 commands, P2 for the rest), with the interim report being the 3.1 file; or put the contract addition for tdd, troubleshoot and release-split into the phase that precedes any use of WC-5. Fix SPEC:79 to "until the phase named in column Small fix/section 6".
- Priority: High. Quality impact: removes a false-failure window of two phases.

### R-2 (blocking, MAJOR, Crispin/Whittaker): AC-C5 cannot detect deleted or edited bullet lines
Grading sentence: an implementer who follows AC-C5 (SPEC:176, the "edits are additive" gate for SA-4, SPEC:149) builds a check `git diff -U0 ... | grep -E '^-[^-]'` that passes while existing lines are deleted, and that is wrong because a deleted markdown bullet `- foo` appears in a diff as `-- foo`, whose second character is `-`, so the pattern excludes it; the same holds for a deleted `---` frontmatter line (`----`) and for any edited bullet (its old half is `-- ...`).
- Attack (Whittaker, sequence/sentinel collision, the `-` in the pattern is used as the diff marker and as content): reproduced here with `printf -- '-- foo\n----\n- x\n-|row|\n' | grep -E '^-[^-]'`, which prints only `- x` and `-|row|` (a removed `- x` bullet or removed `---` line is missed; only table rows and lines starting with other characters are caught).
- Consequence: SA-1 ("standalone behaviour exactly as today", SPEC:146) is guarded for Phases 1-3 by this single mechanical check (SPEC:176, SPEC:149); command files are bullet-heavy, so an implementer can remove an existing prompt or default bullet and AC-C5 passes. AC-0.3 (SPEC:198) has the same pattern but its target is table rows in the routing guide (`-|...` is matched), so it is only partly exposed.
- Recommendation: replace the filter by one that drops only the file header, for example `grep -E '^-' | grep -vE '^--- (a/|/dev/null)'`, and say that any removed line must be a section-3-named defect fix. This is a narrowing of one command, not new text elsewhere.
- Priority: High.

### R-3 (Medium, Wiegers/Cockburn): the contract path is undeterminable for ~8 commands
WC-4 fixes two path rules, directory (`<output-dir>/return-contract.yaml`) and file (`<file>.return-contract.yaml`) (SPEC:62), and requires the path "known before dispatch". The section 3 lead-in says "Contract means ... `<output-dir>/return-contract.yaml`" (SPEC:76), but rows for document ("require an explicit output", SPEC:107), explain ("write the explanation to a file", SPEC:108), recommend ("write the handoff envelope to a file", SPEC:115), and the "add a report path" rows for build, test, cleanup, improve, design, analyze (SPEC:99, 101, 103, 106, 110, 123) never say whether the new option is a directory or a file. An implementer must guess; the worse guess puts the contract where the coordinator does not look. Graded Medium (needs a guess, not a contradiction). Recommendation: name the option kind per row, or state one default (the new option is always a directory).

### R-4 (Medium, Nygard/Whittaker): WC-10 universal rule contradicts WC-7 "fan-out stays as is"
WC-10 says any step that blocks "a single tool call" longer than 5 minutes "must be split into waits of at most 4 minutes" (SPEC:68). WC-7 says a command's Agent-tool fan-out "stays as it is" and subagents never send lifecycle messages (SPEC:65). A parallel Task fan-out (adversarial 2-10 generators, tdd 2-10+ agents, brainstorm, INV-A:35/39, INV-B:47) is a single blocking call far longer than 5 minutes and cannot be split by the command. Only cli-eval and pr-submit get a WC-10 change (SPEC:104, 114). Whether a missing heartbeat matters is itself UNVERIFIED (CAPS:130). Medium: an implementer following section 3 does the right thing; one following WC-10 literally cannot. Recommendation: scope WC-10 to "waits the command itself controls (Bash polls, background jobs)", or state that Task fan-out is exempt.

### R-5 (Medium, Fowler): WC-3 "re-invoke with the answer" collides with WC-6 "fresh directory per attempt"
WC-3 has the worker ask once and "re-invoke or resume the command with the answer as a flag" (SPEC:61). For the 20 or so commands whose resume column is "fresh dir" (SPEC:99-125) there is no resume, so the re-invocation is a fresh attempt; WC-6 says every fresh attempt gets its own new output path and the report path is fixed before dispatch (SPEC:64, 73). The text does not say whether the re-run overwrites the blocked contract at the same path or uses a new one. Medium (two readings). Recommendation: say the re-invocation overwrites the same path and `worker_done` is sent once at the end (WC-5), or that it counts as a retry with a new path communicated by the worker.

### R-6 (Medium, Wiegers): which P1 commands receive `## Unattended mode`
P1 gives the section "on the commands listed here and no others" and the list ends "fixes to adversarial, cleanup-audit, index-repo, workflow" (SPEC:159). AC-1.1 asserts a section on "every command section 6 lists for P1" (SPEC:200). Whether those four fix-only commands are "listed" is not stated; adversarial and workflow already write their own contract, cleanup-audit and index-repo need a new one (SPEC:85, 86). Recommendation: list them explicitly as either with or without the section.

### R-7 (Medium, Fowler/Cockburn): the invocation mechanism of a `/sc:` command inside a worker is never stated
The decision rests on "one worker runs one command" (SPEC:16) and WC-7 "runs the command directly" (SPEC:65), but the brief is delivered behind an Orca preamble (CAPS:47: prompt typed after readiness), so it does not begin with `/sc:`. The project rule that a message starting with `/sc:` must invoke the skill first cannot fire on a preamble-prefixed brief; the spec never says the brief must tell the worker to call the Skill tool with the command name. The only prior evidence has an unresolved route (SPEC:43, `invocation_method: "skill-direct"` versus an Agent-tool brief). Phase 0 (SPEC:158, AC-0.4) tests the outcome but not a stated mechanism. Medium (a requirement the document never states). Recommendation: one sentence in 2.3 fixing the invocation method the brief uses and AC-0.4 checking it.

### R-8 (Medium, Whittaker; sequence attack): stale contract on reused path
WC-6 lets a run with the resume flag reuse the earlier path (SPEC:64) and WC-4 says the file is written "on every outcome" (SPEC:62), but a worker that dies or is cut off before writing leaves the earlier contract. Attack trace: attempt 1 ends `status: blocked` at path P; attempt 2 resumes into P, is killed after start; the coordinator opens P and reads attempt 1's `blocked` (or a prior `succeeded` if P was reused for a re-run). WC-5 treats the file as authoritative (SPEC:63) and has no freshness field (`command` is the only identity field, SPEC:62). Medium: needs the assumption that a run dies unrecorded. Recommendation: add `started_at`/`dispatch id` to the minimum fields, or have the worker delete or rename a pre-existing contract first.

### R-9 (Medium, Hohpe): Phase 2 depends on D4
SPEC:154 says Phases 1-3 need no user decision, but P2 includes auggie-review `--post-pr` authorization and task `commit`/`push` (SPEC:100, 121, 160), which D4 decides, and D4(b) "never" would reject the explicit-flag route those rows keep (SPEC:249-251). Recommendation: say P2 implements only the "off under `--unattended`" half and the authorization route waits for D4.

### R-10 (Medium, Adzic): workflow row creates two contract locations
The workflow row keeps the package contract at `.dev/tasks/to-do/<id>/return-contract.yaml` ("unchanged") and adds `--output <dir>` plus a contract there "for pre-creation STOPs too" (SPEC:92). The package id is generated by the command, so the main-path report path is not known before dispatch (WC-4, SPEC:62), and AC-0.4 uses the package directory (SPEC:199). It does not say which one `worker_done --report-path` carries on success. Medium (two readings).

## === ARCHITECTURE ANALYSIS ===

Strengths (checked): the decision (SPEC:13-45) is supported by CAPS lines I could read: coordinator-only scheduling (CAPS:92), depth 1 and refusal text (CAPS:97-101), `worker_done` bound to the dispatched pane (CAPS:76), `ask` and resume by ID (CAPS:58-61), report path as pointer only (CAPS:79). The honest gap statement (SPEC:41-45) matches CAPS:103, 155-160, 187-188 and INV-B:323. R1-R5 hold. The 10/27/6 split is arithmetically consistent with both inventories. The six coordinator-only reasons match INV-A:90-92 and INV-B:285-287. Section 3.1/3.2 phase assignments match section 6 for the commands I cross-checked, except R-1/R-6.

Architectural concerns recorded under R-4, R-5, R-7, R-8, R-9, R-10 above, plus:
- **Single point of definition**: the shared `WORKER-CONTRACT.md` (SPEC:52) is correct per the installed-path rule, but SA-2 (SPEC:147) lets only that file mention an Orca command while WC-3 depends on "the preamble's `ask` command"; consistent, no finding.
- **Newman/Hohpe, versioning**: the contract has no version field (compare `contract 1.1` in the workflow ref, INV-B:272), so a later field change cannot be told apart by the coordinator. Minor, N-2.

## Guard Condition Boundary Table
Trigger present (thresholds, status guards, depth). Input classes that cannot occur for a guard are omitted with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| contract valid? | WC-5 SPEC:63 | Zero/Empty | file absent, empty, unparseable | failed | `--outcome failed` (from P1 only) | GAP (R-1: P1-P2 window) |
| contract valid? | WC-5 SPEC:63 | Typical | `status: succeeded` | pass | `--outcome succeeded` | OK |
| contract valid? | WC-5 SPEC:63 | Sentinel Value Match | `status: partial` | pass | maps to succeeded; body says partial | OK |
| contract valid? | WC-5 SPEC:63 | Legitimate Edge Case | `status: blocked` | fail | `--outcome failed`; AC-2.2 | OK |
| contract valid? | WC-5 SPEC:63 | Legitimate Edge Case | stale file from earlier attempt | unspecified | not specified | GAP (R-8) |
| single tool call > 5 min | WC-10 SPEC:68 | Typical | Bash poll 600 s | split | wait <= 4 min | OK |
| single tool call > 5 min | WC-10 SPEC:68 | Maximum/Overflow | parallel Task fan-out > 5 min | split | not specified; WC-7 says unchanged | GAP (R-4) |
| nesting depth | WC-8 SPEC:66 / CAPS:97-101 | Maximum/Overflow | worker calls `worker-start` (depth 2 > 1) | refused | forbidden by WC-8 | OK |
| nesting depth | WC-8 | Legitimate Edge Case | depth-1 worker calls `task-create` | unknown | forbidden anyway | OK (UNVERIFIED CAPS:103) |
| `--unattended` token | WC-2 SPEC:60 | Sentinel Value Match | `--unattended` inside quoted content | unspecified | not specified in the spec | GAP (note N-3) |
| ask rounds | WC-3 SPEC:61 | Maximum/Overflow | second gate after first answer | unspecified | "ask once" per gate, count not bounded | GAP (note N-4) |
| report-path kind | WC-4 SPEC:62 | Legitimate Edge Case | new option names dir or file | unspecified | not specified for ~8 rows | GAP (R-3) |
| output path reuse | WC-6 SPEC:64 | Typical | retry via `--retry-of` | fresh path | new dir per attempt | OK |
| One/Minimal | all | omitted: no guard in the spec has a meaningful one-item class | | | | n/a |

Rows marked GAP are graded per FR-8/FR-9: R-1 is blocking, R-3/R-4/R-8 Medium, the rest are notes.

## Adversarial analysis (Whittaker)
- I can break this specification by **Sequence Attack**. The invariant at **SPEC:62-64** ("one report file ... written on every outcome", report path reused on resume) fails when **a resumed attempt dies before writing**. Concrete attack: attempt 1 writes `status: blocked` at P; coordinator answers; attempt 2 reuses P and is cut off; before: P = blocked/attempt 1; after: P unchanged; coordinator opens P and acts on attempt 1's state. (R-8, Medium)
- I can break this specification by **Sentinel Collision Attack**. The invariant at **SPEC:176** (`^-[^-]` means "a removed line") fails when **the removed line starts with `-`** (every markdown bullet). Concrete attack: delete line `- Will Not: ...` in a command; diff line is `-- Will Not: ...`; grep prints nothing; AC-C5 passes. (R-2, blocking)
- I can break this specification by **Divergence Attack**. The invariant at **SPEC:63** (absent contract means failed "from P1 on") fails when **a command has a report but no contract until P2**. Concrete attack: after P1, dispatch `/sc:tdd ... --output f`; run succeeds, `f` exists, no contract; WC-5 yields `--outcome failed`. (R-1, blocking)
- Accumulation Attack on WC-3 ask rounds: no bound on repeated block/ask/re-run cycles; Orca's circuit breaker does not count a worker's own `failed` (CAPS:80). Note N-4.
- Zero/Empty Attack on `blocked_question`: WC-4 requires it "when blocked" (SPEC:62) but not non-empty; AC-2.2 does (SPEC:205). Note N-5.

## Unverified claims (no checkable file in the workspace)
- E5 grep results and `grep -ci orca ... HOW-WE-WORK.md` printed `0` (SPEC:25); `KNOWN_CORE_FILES` at `install_core.py:13-24` (SPEC:52); PyYAML at `pyproject.toml:38` (SPEC:188; the project instructions I was given list only pytest, click and rich as dependencies, so this is doubtful); every `CLAUDE.md:N`, `Makefile:68-74`, `plugins/...` citation (SPEC:52, 147, 150, 175, 197, 284); the "11 load-bearing locations" re-read and the "~340 citations" check (SPEC:11, 290); `.dev/codegraph-migration/...` and `EVIDENCE.md` lines (SPEC:23, 59, 62; the inventories quote EVIDENCE.md:39,45 identically, INV-A:20-22 area).
- Possible census/E5 staleness (UNVERIFIED): the skill list available to this reviewer includes `sc:issue` (its description says it creates an Orca worktree), `sc:graph` and `sc:impact`, which are in neither inventory. If `src/superclaude/commands/` contains them, "43 commands" (SPEC:76) and E5 "no command ... calls Orca" (SPEC:25) are out of date, and AC-C1 (SPEC:180, expects empty output) would not pass at baseline. Could not be checked from the workspace.

## Follow-up candidates (Medium and minor; none triggers a revision)
Medium: R-3, R-4, R-5, R-6, R-7, R-8, R-9, R-10 (details above), and:
- R-11 (Medium, Crispin): AC-C1's regex lists four subcommand words (SPEC:180) while SA-2 forbids any `orca`/`orca-ide` command (SPEC:147); `orca-ide status`, `orca open`, `orca-ide skills get` would slip through. It also excludes only `skills/ccsession-tag/`, and the staleness note above could make it fail at baseline.
- N-1 (minor): AC-C3 baselines only `tests/skills/` (SPEC:174) although P0 edits `install_core.py` and `HOW-WE-WORK.md`; tests elsewhere are not covered (UNVERIFIED which exist).
- N-2 (minor): no `contract_version` field (see Architecture).
- N-3 (minor): the spec does not say that `--unattended` is honoured only as a standalone argument token (a quoted specification containing the text must not switch the mode).
- N-4 (minor): no cap on block/ask/re-run cycles per Task.
- N-5 (minor): WC-4 does not require `blocked_question` to be non-empty though AC-2.2 does.
- N-6 (minor): AC step 5 (SPEC:189) greps a transcript for the string `AskUserQuestion`; commands and skills quote that word in prose (for example INV-A:62), so a loaded skill text can trigger a false failure; search tool-call events instead.
- N-7 (minor): the 3.2 `load` row counts a command in the "27 needing a change" that is declared not dispatchable as its own Task (SPEC:112, 138); harmless to the arithmetic.
- N-8 (minor): `/sc:pr-submit` top-level rule is cited as `SKILL.md:37-39` (SPEC:65; INV-A:10) and as lines 47-49 of the installed copy (CAPS:161); different files, no conflict, but cite one.

## Reviser brief
Blocking finding ids: R-1, R-2. Rules for the reviser (this report is its only input; it does not read the command): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave Medium and minor findings alone, including "apply all findings"; return the candidate once and do not award yourself a PASS.
- R-1: SPEC:63 and SPEC:79 (and the SPEC:159-160 phase placement of the contract for tdd, troubleshoot, release-split).
- R-2: SPEC:176 (and the same pattern at SPEC:198 only if it shares the defect for non-table lines).

verdict: FAIL
