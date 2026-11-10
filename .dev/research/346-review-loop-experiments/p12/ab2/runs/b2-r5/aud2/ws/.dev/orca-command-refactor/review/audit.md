review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md (whole-document first review)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `363aad34a552033a79d2d651495b742507e757c6d9545270ee860f0bf999e142` (285 lines)
- baseline: none given, none needed (first review of the whole document). No prior-findings file.
- reviewer model actually used: claude-sonnet-5-5
- brief clauses overridden: none. The brief narrows the run (write only this file), so the Improve step and any revised specification are not produced.
- coverage: the whole document (sections 1-9, Decisions, UNVERIFIED list), read in full. Requirements focus (Wiegers, Adzic, Cockburn) and architecture focus (Fowler, Newman, Hohpe, Nygard), plus Whittaker's adversarial pass, which is always active. Every `INV-A:N`, `INV-B:N` and `CAPS:N` citation in sections 1-4 and 9 was compared with the inventory line it names. All matched in content. No wrong line was found, and the one that looked off (`CAPS:115`) holds the `[G:placement]` quote at its end. The 43 = 10 + 27 + 6 split and the phase tallies (P1 9, P2 15, P3 4, P4 3 = 31 rows; 4 more commands are fixes to ready commands) reconcile row by row with `INV-A:73` and `INV-B:280-298`.
- not checkable here (marked UNVERIFIED): every citation to a path outside `.dev/orca-command-refactor/` (`src/superclaude/...`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `HOW-WE-WORK.md`, the Orca guides) because those files are not in the workspace. Where an inventory line quotes such a file I checked the inventory only. The spec's claims E5 (grep result, `spec:25`), "11 locations re-read" (`spec:11`) and "about 340 citations re-read" (`spec:285`) are also UNVERIFIED.

## Findings table

| id | severity | grade | location | one line |
|---|---|---|---|---|
| BL-1 | CRITICAL | blocking | `spec:62`, `spec:76`, `spec:87`, `spec:90`, `spec:183`, `spec:200` | WC-4's contract path assumes `--output` is a directory; tdd and init-lite (and the other file-valued `--output` commands) pass a file |
| M-1 | MAJOR | Medium | `spec:122` | tasklist row departs from the inventory without a recorded decision and leaves a Stage 10.5 HALT unresolved |
| M-2 | MAJOR | Medium | `spec:62`, `spec:92`, `spec:198` | workflow's pre-creation contract has no defined path |
| M-3 | MAJOR | Medium | `spec:62`, `spec:104`, `spec:113` | a "blocked because the output flag is missing" stop has nowhere to write the contract |
| M-4 | MAJOR | Medium | `spec:73`, `spec:159`, `spec:160` | P1 accepts `--unattended` on gated commands before P2 converts the gates |
| M-5 | MAJOR | Medium | `spec:88`, `spec:69` | reflect's tracked-file write and default folder move are not covered by WC-9 or WC-11 |
| M-6 | MAJOR | Medium | `spec:149`, `spec:159`, `spec:176` | SA-4 allows new flags; AC-C5 forbids any removed line, and a flag added to a usage line removes one |
| M-7 | MAJOR | Medium | `spec:147`, `spec:158`, `spec:172` | AC-C1 greps `src/superclaude/core`, where P0 adds Orca-bearing text |
| M-8 | MAJOR | Medium | `spec:24`, `spec:68` | WC-10 heartbeat cadence cannot be met across a long foreground Agent-tool call |
| M-9 | MAJOR | Medium | `spec:154`, `spec:225-230` | section 6 says phases 1-3 need no user decision; D1 governs all of them |
| M-10 | MAJOR | Medium | `spec:61`, `spec:200` | WC-3 lets the worker `ask` instead of stopping; AC-2.2 assumes it stops |
| N-1 | MINOR | note | `spec:67`, `spec:133` | `README.md:31` is a rule for this run's workers, cited as repo policy |
| N-2 | MINOR | note | `spec:62`, `spec:76`, `spec:194` | labels F-01, F-02, F-03 are used but never defined in the spec |
| N-3 | MINOR | note | `spec:84`, `spec:87`, `spec:195-196` | brainstorm and init-lite are called ready but no phase runs them as workers |
| N-4 | MINOR | note | `spec:184` | step 5 searches a transcript for the string `AskUserQuestion` |
| N-5 | MINOR | note | `spec:122`, `spec:271-285` | the tasklist nesting claim is absent from the UNVERIFIED list |
| N-6 | MINOR | note | `spec:76`, `spec:112`, `spec:139` | load and recommend are counted among the 27 "needs a change" yet are advised against as Tasks |
| N-7 | MINOR | note | `spec:62`, `spec:262` | existing contracts' `status` vocabulary was not compared with the fixed four values |

## === REQUIREMENTS ANALYSIS ===

### BL-1 [CRITICAL, blocking] Contract path is undefined for commands whose `--output` is a file
- Experts: Wiegers (traceability and testability), Adzic (the example does not run).
- Grading sentence: an implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (`spec:62`). For `/sc:tdd` and `/sc:init-lite` the brief must pass `--output <file>` (`spec:87`, `spec:90`), and `spec:76` names only adversarial and workflow as exceptions to the directory rule. The implementer therefore has to write `<file>/return-contract.yaml`, which cannot exist, or invent a rule. So the acceptance check cannot pass: AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects a contract with `status: blocked` (`spec:200`), and live-check step 3 and step 4 require "the contract path WC-4 gives" and `test -s <contract>` (`spec:182-183`). The text gives no such path for tdd.
- The same split exists for the other file-valued outputs the spec adds or relies on: explain "write the explanation to a file" (`spec:108`), recommend "write the handoff envelope to a file" (`spec:115`), and spec-panel (`spec:120`). The command definition supplied with this run states `--output` is file-valued and uses a separate `--report-dir` (`command.md:23`, `command.md:460`), which confirms the two conventions collide. That file is not part of the audited spec, so it is supporting evidence only.
- Recommendation: state one rule in WC-4. For example, "when `--output` names a file, the contract is `<dirname(--output)>/return-contract.yaml`", or "the brief passes a separate `--report-dir` for every command", and update the `spec:87`, `spec:90`, `spec:120` rows, AC-2.2 and step 3. Prefer the narrower edit: a rule in WC-4 plus the affected rows, not a new flag family.
- Priority: High. Quality impact: testability 5 to 8 of 10.

### M-2 [MAJOR, Medium] workflow pre-creation contract has no path
- WC-4 requires the contract "including stops before any other output exists" (`spec:62`) and the workflow row adds the pre-creation STOP fix (`spec:92`). Workflow's path is `.dev/tasks/to-do/<id>/` with an `<id>` the command generates (`spec:62`; `INV-B:270`, `INV-B:272`: "Not written for pre-creation STOPs"). Before the package exists there is no `<id>`. AC-1.4 only greps for a sentence saying so (`spec:198`).
- Why Medium: the implementer must guess where to write it, rather than building a provably wrong thing from stated text.
- Recommendation: name the pre-creation fallback path (for example the cwd or a brief-supplied directory), or say the worker reports `failed` with no report (WC-5 already covers "no report exists", `spec:63`).

### M-3 [MAJOR, Medium] "Blocked on a missing flag" cannot write the contract
- post-release resolves as blocked when `--output` is absent (`spec:113`), and cli-eval resolves blocked when `--suite` is absent (`spec:104`). WC-4 says the contract goes in the directory the coordinator passed (`spec:62`). When that directory is the missing input, no location exists.
- Why Medium: a requirement the document never states (an undefined state), not a stated text that does harm.
- Recommendation: add a default location for the blocked contract when the output flag is missing, or have the brief always pass the report directory (see BL-1).

### M-4 [MAJOR, Medium] P1 accepts the flag where the gate still waits
- P1 makes every command in 3.1 and 3.2 accept `--unattended`, "a no-op where a command has no gate" (`spec:159`). Gated commands (task, tdd, cli-eval, cleanup, and others) are converted only in P2 (`spec:160`), while section 2.3 tells the coordinator to put `--unattended` in every brief (`spec:73`). Sequence attack: dispatch `/sc:task ... --unattended` after P1 and before P2; the flag is accepted and the confidence prompt still stalls, invisibly (`spec:60`, `CAPS:52`, `CAPS:129`).
- Why Medium: the worse reading needs the coordinator to dispatch ahead of the phase.
- Recommendation: one line in 2.3 or section 6 that a gated command is not dispatched with `--unattended` before its row's phase passes its check.

### M-9 [MAJOR, Medium] Section 6 and section 9 disagree on user decisions
- `spec:154` says phases 1-3 "need no user decision"; `spec:225` says phases 0-3 proceed "on the recommendations"; D1 (`spec:227-230`) decides the mechanism every P1 to P3 edit implements. The two sentences are compatible only if the recommendation is treated as approved.
- Recommendation: say D1 is assumed answered (a) unless the user says otherwise.

### M-10 [MAJOR, Medium] The optional `ask` path versus a deterministic acceptance check
- WC-3 allows a worker to `ask` the coordinator once instead of ending blocked (`spec:61`). AC-2.2 requires `worker_done --outcome failed` and `status: blocked` for a gate-trigger run (`spec:200`). A worker that takes the `ask` path passes WC-3 and fails AC-2.2.
- Recommendation: the AC-2.2 brief should say "do not use `ask`", or AC-2.2 should accept either end state.

## === ARCHITECTURE ANALYSIS ===

### M-1 [MAJOR, Medium] tasklist row departs from the inventory and leaves a HALT open
- The inventory verdict is to run Stage 10.5 without `--remediate`, with the reflect fan-out at the worker's top level (`INV-B:215`), after flagging subagent-to-agent nesting as UNVERIFIED (`INV-B:210`, `INV-B:314`) and "who answers" the offer as UNVERIFIED (`INV-B:209`, `INV-B:322`). The spec instead keeps `--remediate`, passes `--unattended` so reflect's headless auto-accept applies (`spec:122`), and states the fan-out is "inside Claude Code's nesting limit" (`INV-A:14` gives only the 3-layer default). The Decisions table records no choice here.
- Under headless mode reflect "auto-accepts for auto-fixable registers" (`INV-B:109`). Stage 10.5 also HALTs on `needs_human_decision` items (`INV-B:209`). The row does not say how that HALT resolves, which is the WC-2 stall the section exists to remove (`spec:60`).
- Why Medium: whether "skips the gates" in the headless rule covers the HALT needs a guess.
- Recommendation: add a Decisions entry for why `--remediate` stays, and say the `needs_human_decision` HALT resolves as blocked or is listed in the contract.

### M-5 [MAJOR, Medium] reflect's side effects are outside WC-9 and WC-11
- reflect writes the tracked file `docs/memory/reflect/deviation-patterns-<slug>.md` and, in UC-2, moves the work-unit folder by default (`INV-B:114`). The row offers only `--no-promote` (`spec:88`). WC-11 forbids two workers writing the same file and defaults output paths to a slug (`spec:69`); a tracked shared path keyed by slug is a clobber risk for parallel reflect workers.
- Recommendation: list the tracked write in the reflect row, or route it through the output directory under `--unattended`.

### M-6 [MAJOR, Medium] "Additive" and "no removed line" conflict for usage lines
- SA-4 calls the Phase 1-3 edits additive: "a new `## Unattended mode` section and new flags" (`spec:149`). P1 makes each command accept `--unattended` and gain output flags (`spec:159`). AC-C5 fails on any `-` line in the diff of an edited command (`spec:176`). A flag added to an existing usage or `argument-hint` line produces a `-` line; the spec itself treats the load usage-line edit as a named defect fix (`spec:112`, `spec:149`).
- Why Medium: adding the flag on a new line avoids it.
- Recommendation: say new flags go on a new usage line, or exempt the usage line from AC-C5.

### M-7 [MAJOR, Medium] AC-C1 scans the directory P0 writes into
- AC-C1 requires no `orca(-ide) orchestration|worktree|terminal|agent` match under `src/superclaude/core` (`spec:172`). P0 adds `src/superclaude/core/WORKER-CONTRACT.md` and an Orca section to `HOW-WE-WORK.md` (`spec:158`), and SA-2 allows a mention of Orca "inside the contract file" as an example of the caller's question channel (`spec:147`). An `orca orchestration ask` example would trip the grep.
- Recommendation: exclude those two files in AC-C1, or limit SA-2's allowed mention to wording that does not match.

### M-8 [MAJOR, Medium] Heartbeat cadence versus a blocking foreground call
- WC-10 requires a heartbeat every 5 minutes and splits only poll and eval waits (`spec:68`). The spec keeps all Agent-tool fan-out inside commands (`spec:24`), and a foreground fan-out call (tasklist, roadmap, adversarial, cleanup-audit) can block the session for longer than 5 minutes with no chance to heartbeat. Orca's use of heartbeat age is UNVERIFIED (`CAPS:130`), so the harm may be nil.
- Recommendation: restate WC-10 as "where practical" for fan-out calls, or say heartbeats are not required while a foreground tool call is running.

## Guard Condition Boundary Table
Classes left out per guard are given in one line each. Rows follow `spec:` locations.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-1 readiness limit | `spec:59` | Typical | prompt falls back in 30 s | passes | passes at 30 s (`EVIDENCE.md:45`, UNVERIFIED) | OK |
| WC-1 readiness limit | `spec:59` | Maximum/Overflow | fallback between 45 s and 60 s | unspecified | "well inside" with no number; the 45 s failure point is cited at `spec:59` | GAP (note, not blocking) |
| WC-10 wait split | `spec:68` | Legitimate Edge Case | one call blocking exactly 5 min | false ("longer than") | not split; a heartbeat falls due while blocked | GAP (see M-8) |
| WC-10 wait split | `spec:68` | Maximum/Overflow | foreground fan-out call over 5 min | not addressed | unspecified | GAP (M-8) |
| WC-5 outcome mapping | `spec:63` | Zero/Empty | report file present but empty | unclear ("no report exists") | step 4 uses `test -s` (`spec:183`) but WC-5 does not | GAP (minor) |
| WC-5 outcome mapping | `spec:63` | Sentinel Value Match | a `status` outside the four values | unspecified | an existing contract with its own vocabulary (N-7) | GAP (minor) |
| WC-4 report location | `spec:62` | Zero/Empty | no output flag in the brief | false | unspecified | GAP (M-3) |
| WC-4 report location | `spec:62` | Legitimate Edge Case | `--output` is a file | unspecified | unspecified | GAP (BL-1, blocking) |
| WC-3 ask | `spec:61` | Maximum/Overflow | repeated `ask` timeouts | resume same id | no cap on resumptions | GAP (minor) |
| Depth guard (R1, WC-8) | `spec:33`, `spec:66` | Typical | worker calls `worker-start` | refused (`CAPS:99`) | specified | OK |
| Depth guard | `spec:33` | One/Minimal | depth set to 2 by the user | allows nesting | D5 keeps 1 (`spec:249-253`) | OK |
| task confidence guard | `spec:121` | Legitimate Edge Case | exactly 0.70 | false ("below 0.70") | proceeds; matches `INV-B:292` ("< 0.70") | OK |

Left out: the zero/empty and sentinel classes for the depth guard (a depth below 1 falls back to 1, `CAPS:100`) and the task guard (confidence is a computed score, never null); the maximum class for the confidence guard (1.0 proceeds). The FR-8 and FR-9 gaps above are graded by the rule in the Review Loop: BL-1 is blocking, M-3 and M-8 are Medium, the rest are notes.

## Adversarial analysis (Whittaker)
- I can break this specification by **Sequence Attack**. The invariant at **`spec:73` (the brief carries `--unattended`)** fails when **a gated command is dispatched after P1 and before P2**. Concrete attack: P1 lands, the coordinator briefs `/sc:task ... --unattended`, the flag is accepted, confidence is 0.62, the prompt appears, the worker parks with no `worker_done`. Severity MAJOR, graded Medium (M-4).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **`spec:51` (the switch is a flag token)** fails when **quoted user text contains `--unattended`**. State before: a person's quoted topic includes the token; after: the command treats the run as unattended. The spec is silent on token position. Severity MINOR; the supplied command definition handles it (`command.md:459`).
- I can break this specification by **Divergence Attack**. The invariant at **`spec:63`/`spec:200`** fails when **both the `ask` branch and the stop branch of WC-3 apply** (M-10).

## Quantity check (pipeline dimensional analysis)
Stage counts: 21 + 22 = 43 commands (`INV-A:3`, `INV-B:3`); 10 + 27 + 6 = 43 (`spec:76`); per-inventory 5 + 13 + 3 = 21 (`INV-A:73`) and 5 + 14 + 3 = 22 (`INV-B:280-298`). P1 9 + P2 15 + P3 4 + P4 3 = 31, plus 4 fixes to ready commands = 35 rows of work for 37 non-coordinator commands; the 2 not tested after P0 are brainstorm and init-lite (N-3). No mismatch.

## Minor notes (none blocks)
- N-1: `README.md:31` forbids commits and pushes for this run's workers; the spec cites it as evidence for what "needs the user's authorization in this repo" (`spec:133`) and for WC-9 (`spec:67`). The first claim is stronger than the line.
- N-2: F-01, F-02, F-03 are referenced at `spec:62`, `spec:76` and `spec:194` and are not defined in the spec; they appear to name earlier review findings that are not in this workspace.
- N-3: brainstorm and init-lite have no contract change (`spec:84`, `spec:87`, `spec:195`) and AC-1.2 runs only P1 commands (`spec:196`), so neither is run as a worker in any phase.
- N-4: step 5 searches the transcript for `AskUserQuestion` (`spec:184`); loaded command text may contain the string. Say "a tool call named".
- N-5: `INV-B:314` and `INV-B:322` leave nested spawning in tasklist UNVERIFIED; the spec's UNVERIFIED list (`spec:271-285`) omits it.
- N-6: load and recommend are in the 27 "needs a change" (`spec:76`), yet the spec advises against dispatching them (`spec:112`, `spec:139`).
- N-7: WC-4 says existing contracts "keep their fields" and also fixes four `status` values (`spec:62`). `INV-B:272` lists the workflow contract's `status` field but not its values, so a clash is unchecked. The Decisions table (`spec:262`) picks the fixed set without comparing.

## Expert consensus
- Wiegers: the requirements are specific and each carries evidence. The one place the path rule fails is the file-valued output (BL-1).
- Adzic: the live-check procedure (7.2) is a good set of examples. Fix the tdd example so its contract path can be located.
- Cockburn: coordinator and worker roles are clear; the 2.3 duty list is helpful.
- Fowler / Newman: the "Orca on top, commands stay units" boundary is sound and consistently applied (SA-2, WC-8, section 8). The section 3 table mixes three conventions for the report path (BL-1, M-2, M-3).
- Nygard: stalls are the central failure mode and WC-2 handles them; M-4 and M-1 are the remaining stall windows.
- Hohpe: the report-file hand-off is clear; WC-5's outcome mapping is simple and testable.

## Follow-up candidates (Medium and minor findings; none triggers a revision)
M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10 and N-1 to N-7 above. The question whether to open an issue for them was not asked: this run has no user channel and no `--unattended` report directory. No issue was created.

## Reviser brief
Blocking finding ids: **BL-1** only.
Rules (restated for the reviser, who reads this report and not the command):
- Revise only text a blocking finding names; here that is the WC-4 path rule and the rows and checks BL-1 cites (`spec:62`, `spec:87`, `spec:90`, `spec:120`, `spec:182-183`, `spec:200`).
- Add no rule, mechanism or section that BL-1 does not call for.
- Cite the finding id (BL-1) on each added paragraph or table cell.
- Prefer deleting or narrowing to adding.
- Report the file's byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings alone, including by "apply all findings".
- Return the candidate once; do not award yourself a PASS.

verdict: FAIL
