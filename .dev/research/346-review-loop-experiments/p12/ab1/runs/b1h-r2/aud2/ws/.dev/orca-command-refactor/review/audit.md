review: 1 of 3

# /sc:spec-panel audit: orca-worker-contract-spec.md

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, first review (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`, read in full)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (294 lines)
- candidate sha256: `feaa1a31e42a8514d14628b790b646be58d5aee3914f33cd26e8e8f6a0037350`
- baseline: not given (first review; `--re-review` and `--baseline` both absent, so no `baseline: missing` condition)
- reviewer model actually used: claude-sonnet-5-5
- mode flags: no `--unattended`, no `--improve`; the Improve step did not run and no revised specification was written
- brief clauses overridden: none
- binding context read first: `.dev/orca-command-refactor/README.md:1-39`

Citation keys: `SPEC:N` = line N of the candidate. `CAPS:N`, `INV-A:N`, `INV-B:N` = lines of `.dev/orca-command-refactor/inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md`. These four files are the only evidence I could open. Every citation to `src/`, `tests/`, `CLAUDE.md`, `pyproject.toml`, `.dev/evals/`, `.dev/codegraph-migration/` or `~/.claude/skills|commands` is UNVERIFIED here unless an inventory line quotes it, in which case I cite the inventory line.

## Coverage
Read the whole candidate, lines 1-294, and checked it against the three inventories. Checked, by line:
- the section 1.2 and 1.3 evidence tables against `CAPS:44-188`;
- the 10 / 27 / 6 split against `INV-A:73`, `INV-B:271-275` and the section 3 row counts (10 + 27 + 6 = 43, which I recounted);
- the phase partition: 14 + 15 + 4 + 3 = 36 commands, plus brainstorm, which has no fix and so no phase (`SPEC:84`). Together that is the 37 workers;
- the requirements WC-1..WC-12, SA-1..SA-6, AC-C1..AC-C5, the 7.2 live check and AC-0.x to AC-4.x;
- the decisions D1-D5.

Not covered: any source file under `src/`. I cannot open them, so no section 3 "Evidence" cell citing `cmd/` or `sk/` was re-read; I only compared those cells with what the inventories say. Scope is the final spec as one document.

Experts engaged. Requirements focus: Wiegers (lead), Adzic, Cockburn. Architecture focus: Fowler (lead), Newman, Hohpe, Nygard. Whittaker is active on every panel. Crispin, Gregory and Hightower are outside the two focus lists, so they raised nothing of their own.

## Findings table
| id | severity (label) | graded | experts | location |
|---|---|---|---|---|
| F-1 | MAJOR | **blocking** | Wiegers, Nygard, Whittaker (Sequence attack) | SPEC:159, 73, 60, 97-125 |
| F-2 | MAJOR | Medium | Wiegers, Fowler | SPEC:62, 85-86 |
| F-3 | MAJOR | Medium | Nygard, Whittaker | SPEC:64, 85-87, 90, 116 |
| F-4 | MAJOR | Medium | Wiegers, Hohpe | SPEC:62-63, 202, 271 |
| F-5 | MAJOR | Medium | Nygard, Whittaker (Accumulation) | SPEC:68, 104, 114 |
| F-6 | MAJOR | Medium | Fowler, Newman | SPEC:69, 73, 207 |
| F-7 | MAJOR | Medium | Nygard, Whittaker (Divergence) | SPEC:88, 122, 151 |
| F-8 | MINOR | Medium | Adzic, Whittaker (Sentinel) | SPEC:147, 172, 181 |
| F-9 | MINOR | Medium | Wiegers | SPEC:62, 112, 203 |
| F-10 | MAJOR | Medium | Wiegers, Nygard | SPEC:59, 70, 158-162 |
| n-1 | MINOR | minor | Cockburn | SPEC:62, 73, 83 and many |
| n-2 | MINOR | minor | Wiegers | SPEC:11, 294 |
| n-3 | MINOR | minor | Adzic | SPEC:23, 43 |
| n-4 | MINOR | minor | Wiegers | SPEC:154, 234-239 |
| n-5 | MINOR | minor | Adzic | SPEC:206 |
| n-6 | MINOR | minor | Wiegers | SPEC:293-294 |

## === REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] Phase 1 ships `--unattended` on commands whose person-gates are only converted in Phase 2-4, while the coordinator is told to pass it from Phase 1 on
Experts: Wiegers (requirement conflict), Nygard (a silent stall is the worst failure), Whittaker (Sequence attack).

Grading sentence. An implementer who follows the stated text as written builds, in Phase 1, an `--unattended` flag that is accepted by every command in 3.1 and 3.2 except four (`SPEC:159`), and the coordinator brief template tells coordinators to pass `--unattended` "from P1 on" (`SPEC:73`). The gate conversions for `cleanup`, `improve`, `cli-eval`, `cli-portify`, `recommend`, `research`, `review-translation`, `spec-panel`, `tasklist`, `reflect`, `release-split`, `tdd`, `troubleshoot` are assigned to P2 (`SPEC:100,103-105,110,115-117,120,122`, `SPEC:160`); `roadmap`, `save`, `validate-*` to P3 (`SPEC:118-119,124-125`, `SPEC:161`); `implement` to P4 (`SPEC:109`, `SPEC:162`). So after P1 a coordinator that dispatches `/sc:cleanup <dir> --unattended` gets a command that accepts the flag and still prompts "Approval Required" (`SPEC:103` quotes the gate; `INV-A:43`). WC-2 says that under `--unattended` the command "never calls `AskUserQuestion`, never ends its turn on a chat question" (`SPEC:60`). The result is a worker parked on a prompt with no `worker_done`, which Orca reports as "healthy, not failed" (`CAPS:52`, `CAPS:129`) and which the spec itself calls "invisible" (`SPEC:60`). It is wrong because the spec has no stated text under which the flag is accepted but the gate stays; each phase is declared "independently useful" and shippable alone (`SPEC:154`, `SPEC:156`).

The text itself shows the authors saw the problem for outward defaults: four commands "refuse it with an error until their P2 or P4 change lands" (`SPEC:159`, M3). The same refusal is not applied to the stall class. `SPEC:159` reads "(a no-op where a command has no gate)", which under one reading means gated commands do something in P1, contradicting their P2-P4 assignment; under the other it means they stay prompting. Either reading contradicts WC-2 or section 6.

Also: AC-1.1 asserts a `## Unattended mode` section in every 3.1-3.2 command at P1 (`SPEC:203`), but the section "lists only its own gate resolutions" (`SPEC:52`), which do not exist until P2-P4. AC-1.2 live-checks only the P1 command list (`SPEC:204`, `SPEC:159`), so nothing in P1 catches a gated command accepting the flag.

Recommendation (for the reviser, narrow only): extend the P1 refusal rule from the four outward-default commands to every command whose section 3 row has a non-"no gate" resolution assigned to a later phase, until that phase lands; or move the flag to the phase that converts the gate. Priority: High. Quality impact: Completeness and Consistency, about 1.5 points each.

### F-2 [MAJOR, Medium] WC-4 gives no contract path for commands with a fixed output directory
`SPEC:62` defines the path for three cases: output option names a directory, names a file, or the path is generated at run time. `cleanup-audit` (fixed `.claude-audit/`, `SPEC:85`) and `index-repo` (fixed `PROJECT_INDEX.md`, no output option, `SPEC:86`) fit none. Several 3.2 rows say only "add a report path" or "add an output path" and do not say whether the new option is a file or a directory (`SPEC:101,106,111,123`), yet the contract location depends on that. AC-1.2 assumes `--output <dir>` (`SPEC:204`), `SPEC:108` says "write the explanation to a file". The implementer must guess; the worse guess puts the contract where the coordinator is not told to look. It is Medium because the brief fixes the path before dispatch (`SPEC:73`) and the wrong guess is caught by AC-1.2 step 3. Priority: Medium.

### F-3 [MAJOR, Medium] WC-6 "fresh output directory" cannot be met by commands that take a file or write to a fixed path
WC-6 says a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean" and that a retry "must not corrupt the first attempt's output" (`SPEC:64`). The rows then say: `init-lite` "Re-run overwrites its marked report" (`SPEC:87`), `tdd` writes `--output <file>` (`SPEC:90`), `index-repo` and `cleanup-audit` write fixed paths (`SPEC:85-86`), `research` "fresh file" (`SPEC:116`). For these the command cannot choose a fresh directory; only the coordinator can, by passing a new `--output`. The text does not say so. A resume flag passed with missing or corrupt on-disk state (for example `--resume-from <seed-brief>`, `SPEC:84`) has no stated behavior either. It is Medium because a coordinator that varies `--output` per attempt avoids the harm. Priority: Medium.

### F-4 [MAJOR, Medium] WC-4 "keep their fields" versus the fixed four-value `status`, and a required-field case WC-5 never mentions
WC-4 requires `status` to be one of four values and says commands that already write a contract "keep their fields and add the missing ones" (`SPEC:62`). The Decisions table fixes the four values (`SPEC:271`). AC-0.4 defers the four-value assertion to AC-1.2 (`SPEC:202`), which implies the existing contracts of workflow, adversarial, reflect and brainstorm do not satisfy it. The inventories list the `status` field for workflow (`INV-B:272`) but not its values; I could not check what the other three write (UNVERIFIED). If their `status` uses other values, "keep" and "must be one of four" conflict, and AC-1.2 step 4 (`SPEC:204`, `SPEC:191`) fails on a correct existing contract. Separately, WC-5 covers an empty, unparseable or out-of-set report (`SPEC:63`) but not a parseable report with a valid `status` and a missing `command` field, which AC step 4 asserts (`SPEC:191`). Priority: Medium.

### F-9 [MINOR, Medium] AC-1.1 forces a `return-contract.yaml` section onto `/sc:load`, which the spec says writes none
Section 3 says every changed command gains the section (`SPEC:76`); the `load` row says report "none" and "use it as a step inside another worker's brief" (`SPEC:112`); Decisions say a report file "would be an unrequested addition" (`SPEC:274`); AC-1.1 requires the `load` section to name `return-contract.yaml` (`SPEC:203`). An implementer can satisfy the test only by naming a file the command never writes. Priority: Low.

### F-10 [MAJOR, Medium] WC-1 and WC-12 have no phase deliverable and no acceptance check
WC-1 is owned by "Launch setup, not commands" and asks that any launch-path prompt fall back "well inside" the 60 s limit (`SPEC:59`); no number is given (`CAPS:44-45` give the default and the per-start override; `EVIDENCE.md:56` as quoted at `SPEC:59` says about 45 s fails). No phase in `SPEC:158-162` lists a WC-1 task and no AC tests it; 7.2 step 1 only checks `state: ready` (`SPEC:188`). WC-12 (`SPEC:70`) is a worker-session rule with no check either. Cockburn: the launch-setup owner is not an actor in any phase, so nobody is told to do the work. Priority: Medium.

## === ARCHITECTURE ANALYSIS ===

### F-5 [MAJOR, Medium] WC-10 covers only stated polling waits, not foreground fan-out or long tool calls
WC-10 requires a heartbeat every 5 minutes "while working" and splits only "a command step that blocks a single tool call" (`SPEC:68`). It names poll waits and evals and gives rows for `cli-eval` and `pr-submit` (`SPEC:104,114`). A foreground Agent-tool fan-out (adversarial, cleanup-audit "waves of 7-8 concurrent Task agents", `INV-A:42`; tdd, reflect) or a long `build`/`test` run blocks the top-level session just as long, and the session cannot heartbeat during it. WC-7 keeps heartbeats with the top-level session only (`SPEC:65`). Whether a missed heartbeat has any effect is itself UNVERIFIED (`CAPS:130`, `CAPS:182`), so the harm is unknown, not shown. The spec states no behavior for these commands. Priority: Medium.

### F-6 [MAJOR, Medium] WC-11 "never write the same file" has no mechanism for commands that edit the working tree
WC-11 assigns the rule to the command and fixes only default report paths and memory keys (`SPEC:69`). Workers share the current worktree by default (`CAPS:115`). `cleanup`, `improve`, `document`, `implement`, `test --fix` edit project files (`INV-A:43,47,52`; `SPEC:107,109,110`), and nothing stops two workers editing one file. Only `cleanup-audit` and `index-repo` get a serialization rule (`SPEC:73`, M13) and only AC-1.5 tests it (`SPEC:207`). The brief template lists "the worktree placement" (`SPEC:73`) but gives no rule. Fowler: the boundary between "report files the command owns" and "source files the coordinator must partition" is not drawn. Priority: Medium.

### F-7 [MAJOR, Medium] Under `--unattended`, tasklist and reflect adopt the headless auto-accept rule, whose effect on `needs_human_decision` gates is not reconciled with WC-2(c)
The `reflect` row makes `--remediate` "follow the existing headless auto-accept rule" (`SPEC:88`); the `tasklist` row passes `--unattended` to each reflect "so the headless rule applies" (`SPEC:122`); SA-6 keeps that rule unchanged (`SPEC:151`). `INV-B:109` describes the rule as auto-accepting "for auto-fixable registers and skips the gates". WC-2 says an unattended gate resolves as a default, a flag, or blocked (`SPEC:60`), and `INV-B:213` notes that Stage 10.5 `needs_human_decision` items HALT. The spec does not say which wins for a human-decision item. Two further differences from the inventory go unexplained: `INV-B:215` says the per-phase reflect fan-out "must run at the worker's top level, not inside subagents", while the `tasklist` row says "none" and cites `INV-A:14` (a nesting-depth fact) (`SPEC:122`); and UNVERIFIED item 9 (`SPEC:289`) admits it is unknown whether reflect treats an Orca worker as headless. It is Medium because both readings of the sentence depend on how reflect's rule is implemented, which I cannot read. Priority: Medium.

### Guard Condition Boundary Table
Guards found in the spec: WC-5 outcome mapping, WC-10 wait split, WC-6 resume/fresh, WC-9 outward default, WC-2 gate resolution (phase boundary), WC-1 readiness fallback. Classes left out per guard are explained in the note under each group. Status GAP rows are findings under FR-8/FR-9, graded as stated.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 report usable | SPEC:63 | Zero/Empty | empty or unparseable report file | false | `--outcome failed` | OK |
| WC-5 report usable | SPEC:63 | One/Minimal | `status: succeeded`, one artifact | true | `--outcome succeeded` | OK |
| WC-5 report usable | SPEC:63 | Typical | `status: partial` | true | `--outcome succeeded`, body states `partial` | OK |
| WC-5 report usable | SPEC:63 | Sentinel Value Match | `status: blocked` | false | `--outcome failed` | OK |
| WC-5 report usable | SPEC:63, 191 | Legitimate Edge Case | valid `status`, `command` field missing | unspecified | not stated | GAP (F-4, Medium) |
| WC-5 report usable | SPEC:63 | Legitimate Edge Case | audit verdict FAIL, audit ran | true | `--outcome succeeded` | OK |
| WC-10 wait size | SPEC:68 | Zero/Empty | no waiting step | n/a | no splitting needed | OK |
| WC-10 wait size | SPEC:68 | Typical | poll wait of 3 min | true | within 4 min, heartbeat between | OK |
| WC-10 wait size | SPEC:68 | Maximum/Overflow | foreground Agent fan-out or `build` call over 5 min | unspecified | not stated | GAP (F-5, Medium) |
| WC-10 wait size | SPEC:68, 114 | Legitimate Edge Case | `pr-submit` 600 s budget, iteration = poll runtime + sleep | unspecified | "confirm each iteration under 4 minutes", poll runtime UNVERIFIED | GAP (graded Medium under F-5: no wrong outcome shown) |
| WC-6 resume or fresh | SPEC:64 | Zero/Empty | resume flag given, on-disk state missing | unspecified | not stated | GAP (F-3, Medium) |
| WC-6 resume or fresh | SPEC:64, 87, 90 | Typical | no resume flag, `--output <file>` | unspecified | WC-6 says fresh directory; rows say overwrite | GAP (F-3, Medium) |
| WC-6 resume or fresh | SPEC:64, 84 | One/Minimal | resume flag with valid state | true | resumes | OK |
| WC-9 outward default | SPEC:67 | Typical | `--unattended`, no authorizing flag | true | action off | OK |
| WC-9 outward default | SPEC:67, 254 | Sentinel Value Match | `ask` answer carries the flag | false | never supplies it | OK |
| WC-9 outward default | SPEC:159 | Legitimate Edge Case | P1 build, flag passed to auggie-review/task | true | refused with an error | OK |
| WC-2 gate resolution | SPEC:60, 159 | Typical | gated command (cleanup) after P1 | unspecified | accepted, prompt remains | GAP (F-1, **blocking**) |
| WC-2 gate resolution | SPEC:60 | Zero/Empty | command with no gate | true | no-op | OK |
| WC-1 readiness | SPEC:59 | Maximum/Overflow | fallback longer than readiness limit | unspecified | "well inside", no number | GAP (F-10, Medium) |

Omitted classes, one line each: WC-5 Maximum/Overflow (a file has no capacity bound in the spec); WC-9 Zero/Empty and Maximum (a flag is present or absent); WC-1 Zero/One/Typical/Sentinel (the guard is a duration; zero cannot occur and the typical case is the 30 s fallback quoted at `SPEC:59`); WC-6 Maximum (no counter is stated; the Orca three-failure breaker is cited, not specified, `CAPS:80`).

### Pipeline Dimensional Analysis and Quantity Flow Diagram
Triggered: the spec describes a multi-stage partition of commands into verdicts and phases where counts could diverge. I recounted each stage.

```text
[Source: 43 commands in cmd/ (21 INV-A:3 + 22 INV-B:3)]
   --> [Stage 1: verdict split, SPEC:76]
        10 ready | 27 needs-change | 6 coordinator-only (10+27+6 = 43, conserved)
   --> [Stage 2: workers = 10 + 27 = 37]   (6 never dispatched, SPEC:128)
   --> [Stage 3: phase assignment, SPEC:158-162]
        P1: 9 named + 5 fixes = 14   P2: 15   P3: 4   P4: 3   = 36
        brainstorm: ready, "None" fix (SPEC:84), no phase = 1
        36 + 1 = 37 (conserved)
   --> [Consumer: AC-1.1 asserts a section in all 37 at P1, SPEC:203]  <-- sections list gate resolutions that exist only after P2-P4 (see F-1)
```
No count mismatch. The consumer annotation is the one divergence of meaning, not of count, and it is captured in F-1 and F-9.

### Other architecture notes
- Newman: the contract file is versioned by nothing (`SPEC:52`, `SPEC:62`); the four-value `status` has no version field, so a later added status breaks the AC-1.2 assertion silently. Not graded; no stated text is wrong.
- Fowler: the decision itself (Orca above, commands unchanged as units) is consistently argued; R1-R5 (`SPEC:31-37`) match `CAPS:97-101,145-150`. I found no contradiction between section 1 and section 2.
- Hohpe: WC-12 pull-based follow-ups (`SPEC:70`) match `CAPS:66-67`.

### F-8 [MINOR, Medium] AC-C1 does not enforce SA-2, and SA-2's allowed mention is not reconciled with the grep
SA-2 forbids any `orca` or `orca-ide` command in a command, skill or agent, and allows one mention "as an example of a caller's question channel inside the contract file" (`SPEC:147`). AC-C1 greps four subcommands (`orchestration|worktree|terminal|agent`), case-sensitive, over `src/superclaude/core` as well as commands, skills and agents, excluding only `ccsession-tag` (`SPEC:181`). Consequences: `orca status`, `orca open`, `orca skills get`, `ORCA orchestration` (the spec's own placeholder, `SPEC:167`) or `Orca orchestration` pass the grep, while a literal `orca orchestration ask` in the allowed contract-file example, or in the P0 Orca section of `HOW-WE-WORK.md` (`SPEC:158`, which E5 shows has zero Orca mentions today, `SPEC:25`), fails it. Whether either happens depends on the author's wording. Priority: Low.

## Open items from the labelled brief
None of the brief clauses widened or narrowed the scope; the brief asks for a whole-document first review, which is the default of bullet 1.

## Minor notes
- n-1: Labels `M1`..`M13` and `SA-1` are used as bare tags throughout (for example `SPEC:62,73,83`) with no definition in the document; they point at a disposition record that is not part of the candidate.
- n-2: The validation claims at `SPEC:11` (11 locations re-read) and `SPEC:294` (about 340 citations checked) cannot be reproduced from the workspace; I neither confirm nor dispute them.
- n-3: E3 offers `invocation_method: "skill-direct"` as evidence the route "has worked before" (`SPEC:23`), while section 1.4 says that run proves "the nested route, not the direct route" (`SPEC:43`). The text is honest about it, but E3 reads stronger than 1.4 supports.
- n-4: Section 6 says "Phases 1-3 need no user decision" (`SPEC:154`) while D1 (`SPEC:236-239`) is a user decision those phases depend on; section 9 says they proceed on the recommendations (`SPEC:234`).
- n-5: AC-1.4 greps for `return-contract.yaml` and expects "one fixed path" (`SPEC:206`); a grep cannot show uniqueness.
- n-6: UNVERIFIED list item 14 (`SPEC:294`) is a verification claim, not an unverified item, and sits among the open items.

## follow-up candidates
Medium: F-2, F-3, F-4, F-5, F-6, F-7, F-8, F-9, F-10. Minor: n-1 to n-6. None of these triggers a revision, fails this review, or appears in the Reviser brief. Issue offer: the session that runs this review asks the user once whether to open an issue for them; I created none and had no user channel in this sandbox.

## Unverified citations (this reviewer)
All `src/`, `tests/`, `CLAUDE.md`, `pyproject.toml`, `.dev/evals/`, `.dev/codegraph-migration/` and `~/.claude/skills` citations in the spec, including `SPEC:11`, `SPEC:25` (grep results), `SPEC:52`, `SPEC:191` (`pyproject.toml:38`), `SPEC:147-150` (`CLAUDE.md` lines), and every `cmd/…`, `sk/…` cell in sections 3.1 and 3.2 beyond what `INV-A` and `INV-B` quote. Inventory-backed claims checked and found as cited: `SPEC:21` to `CAPS:92,86`; `SPEC:22` to `CAPS:161`; `SPEC:24` to `CAPS:155`; `SPEC:33` to `CAPS:97-103`; `SPEC:34` to `CAPS:147-149`; `SPEC:35` to `CAPS:76,150`; `SPEC:44` to `CAPS:52,129`; `SPEC:61` to `CAPS:58-64`; `SPEC:63` to `CAPS:73,76-77`; `SPEC:68` to `CAPS:130`; `SPEC:70` to `CAPS:66-67`; command counts to `INV-A:73`, `INV-B:271-275`.

### Reviser brief
Blocking finding ids: F-1.
Rules for the reviser (restating the Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on each added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone, and do not award a PASS.

verdict: FAIL
