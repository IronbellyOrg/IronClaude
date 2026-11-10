review: 1 of 3

# Round 1 review: orca-worker-contract-spec (critique mode, focus requirements,architecture)

- Command acted: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full; the file's first-review text is the only brief applied).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (285 lines at the time of review; `sha256sum` output, same hash as `review/lint-1.md:1`).
- Baseline: not applicable (first review; no `--re-review`, no `--baseline` given).
- Reviewer model actually used: `claude-sonnet-5-5`.
- Lint evidence: `.dev/orca-command-refactor/review/lint-1.md` read first. It reports `Checks: REF. Findings: 0` and `No findings.` (`lint-1.md:3,5`). There is no lint id to confirm or dismiss.
- Extra instruction from the brief: every acceptance criterion and every live-check step was checked one by one for every command and phase it covers (section "Acceptance-criterion check" below). Each one that cannot pass as written is a finding under the same blocking rule.
- Evidence limits: only `.dev/orca-command-refactor/README.md` and `inventory/*.md` exist in the workspace. Every citation of `src/superclaude/...`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...`, `install_core.py`, `pyproject.toml`, `Makefile` and `HOW-WE-WORK.md` could not be opened and is marked UNVERIFIED; where the inventories quote the same line it is checked second-hand only. The `CAPS:`/`INV-A:`/`INV-B:` citations in the spec were spot-checked against the inventory files (about 70 of them: sections 1.2, 1.3, 1.4, 2.2, 3.1, 3.2, 4 and the UNVERIFIED list) and each matched its cited line. The command definition `command.md` supplied with this review was used for one finding (F6).
- Coverage: whole document, sections 1-9 and Decisions; requirements and architecture buckets; Whittaker attacks; Guard Condition Boundary Table; Quantity Flow Diagram; 32 acceptance criteria and live-check steps. `--focus correctness` is not active, so no State Variable Registry is produced.

## Summary

The decision (Orca on top, commands stay units of work, no Orca calls inside commands) is well argued and its citations hold. The defects are in the verification layer and in the phase plan: several acceptance criteria and live-check steps cannot pass as written for commands they cover, and the P1 scope contradicts its own acceptance criterion. Five findings are blocking (F1-F5). Nine are Medium and listed under follow-up candidates.

## REQUIREMENTS ANALYSIS

### F1. CRITICAL (blocking). P1 scope names 37 commands, the P1 command list names 13, AC-1.1 asserts 37. Experts: Wiegers (lead), Fowler, Whittaker (divergence attack). Priority High. Quality impact: Completeness and Consistency drop (about -2 each).

Quoted texts:
- Spec `:159` (P1 row, Scope cell): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)".
- Spec `:159` (same row, Commands cell): "analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow". That is 9 commands plus 4 fixes = 13.
- Spec `:195` (AC-1.1): "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`". Sections 3.1-3.2 hold 37 commands (`:78-125`).
- Spec `:84,87` (brainstorm and init-lite, column "Small fix"): "None". Spec `:76`: "Every changed command also gains the `## Unattended mode` section".
- Spec `:114` (pr-submit, phase P4) and `:109` (implement, P4): their report and gate changes are scheduled after P1.

Grading sentence: An implementer who follows the stated P1 Commands cell edits 13 command files, and AC-1.1 then fails for the other 24 (brainstorm, init-lite, reflect, release-split, tdd, troubleshoot, and the P2-P4 commands), because AC-1.1 requires the section in all 37. An implementer who follows the Scope sentence and AC-1.1 instead gives 24 gate or P2-P4 commands an `--unattended` flag in P1 while their gates (P2, `:160`) and contract writes (P2-P4, `:99-125`) do not exist yet, so a worker briefed with `--unattended` on, for example, `/sc:cli-eval run` still stalls on `AskUserQuestion`, which WC-2 (`:60`) forbids under `--unattended`. Both readings produce a wrong result with no further assumption: the three stated texts contradict each other.

Recommendation (narrow, no new rule): make the P1 Scope sentence, the P1 Commands cell and AC-1.1 name the same command set. The smallest repair is to restrict AC-1.1 to the P1 commands listed in the Commands cell and let AC-2.1, AC-3.x and AC-4.x carry the section check for the commands of their own phase; delete the clause "every command in sections 3.1 and 3.2" from the Scope cell.

Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21; the rollout is a multi-stage filter with N != M at each stage):

```text
[Source: 43 commands (INV-A:3 = 21, INV-B:3 = 22)] --> [Stage 1: classify]
   --> 10 ready (3.1) + 27 needs-change (3.2) + 6 coordinator-only (4)      [37 worker-capable]
[37 worker-capable] --> [Stage 2: phase assignment (section 6)]
   P1 = 9 needs-change + 4 ready fixes = 13
   P2 = 11 needs-change + 4 ready (reflect, release-split, tdd, troubleshoot) = 15
   P3 = 4, P4 = 3, no phase = 2 (brainstorm, init-lite)        [13+15+4+3+2 = 37, conserved]
[P1 consumer: AC-1.1 expects 37 sections]           <-- MISMATCH (13 are scheduled in P1)
[P1 consumer: Scope sentence expects 37 flags]      <-- MISMATCH
[P2-P4 consumers: AC-2.1, AC-3.1, AC-4.x]          expect 15 / 4 / 3
```

### F2. MAJOR graded blocking. The WC-4 contract path contradicts the paths in section 3.1 and in AC-0.4, so live-check steps 3 and 4 cannot pass for the P0 smoke commands. Experts: Wiegers, Adzic, Crispin. Priority High. Quality impact: Testability -2.

Quoted texts:
- Spec `:62` (WC-4): "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed ... known before dispatch".
- Spec `:73` (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)".
- Spec `:182` (step 3): "its report path is the WC-4 contract path". Spec `:183` (step 4): `test -s <contract>` and a YAML assertion on `status` and `command`.
- Spec `:194` (AC-0.4): "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file".
- Spec `:83`: adversarial contract is `<output>/adversarial/return-contract.yaml`. Spec `:92`: workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`. Spec `:91`: troubleshoot reports `REPORT.md`; its `return-contract.yaml` exists "only when `--caller task-unified`" (`INV-B:242`).

Grading sentence: An implementer who follows AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow` and `/sc:adversarial` as workers and applies step 3, and step 3 cannot pass because (a) troubleshoot writes no WC-4 contract in P0 (the contract "arrives in P1", `:194`, yet P1 does not list troubleshoot, `:159`), (b) workflow's contract path contains an `<id>` the coordinator does not know before dispatch, which WC-4 and 2.3 require, and (c) adversarial's contract sits in `<output>/adversarial/`, not `<output-dir>/`. The step-4 exception in AC-0.4 does not help: `yaml.safe_load` on the markdown `REPORT.md` has no `d['status']` to assert. The criterion that closes evidence gap 1.4(1) (`:43`) therefore cannot pass as written.

Recommendation: state per command, in section 3.1, the exact path the coordinator passes to step 3, or change step 3 to "the report path the command's section 3.1 row names"; restrict step 4 to commands that already write a YAML contract in that phase.

### F3. MAJOR graded blocking. AC-2.2 and AC-2.3 need a WC-4 contract from commands that no phase makes write one, and from commands whose `--output` is a file. Experts: Wiegers, Crispin. Priority High. Quality impact: Testability -2.

Quoted texts:
- Spec `:200` (AC-2.2): "contract `status: blocked` with a non-empty `blocked_question`", example "`/sc:tdd "auth" --unattended --output <file>`". Spec `:201` (AC-2.3): "7.2 passes with `--outcome succeeded`", which includes step 4 (`:183`).
- Spec `:89-91`: the P2 changes for release-split, tdd and troubleshoot are gate resolutions only. Spec `:79`: "the worker reports the named file until Phase 1 adds the contract". The P1 Commands cell (`:159`) names none of these three commands.
- Spec `:90` (tdd) and `:87` (init-lite): `--output <file>`. WC-4 (`:62`) writes the contract in "the directory the coordinator passed". `INV-B:222` confirms tdd's `--output` is the TDD file.

Grading sentence: An implementer who follows section 3.1 and section 6 builds tdd, troubleshoot and release-split with gate handling but no `return-contract.yaml`, because no phase assigns it; AC-2.2 (blocked contract) and AC-2.3 step 4 (`test -s <contract>`) then cannot pass. For tdd the contract directory is undefined, because `--output` names a file, so `<output-dir>` is not "the directory the coordinator passed"; with two tdd workers writing to files in one directory the one fixed filename would collide (WC-11, `:69`).

Recommendation: add the contract write to the P2 rows of release-split, tdd and troubleshoot (it is the WC-4 text, not a new rule) and state in WC-4 where the contract goes when `--output` is a file (for example `<file-stem>.return-contract.yaml` beside it).

### F4. MAJOR graded blocking. AC-2.2 requires a blocked outcome from P2 commands whose gate does not resolve as blocked. Experts: Adzic, Crispin. Priority High. Quality impact: Testability -1.

Quoted texts:
- Spec `:200` (AC-2.2): "Gate-trigger run per P2 command ... `worker_done --outcome failed`; contract `status: blocked`".
- Spec `:160`: P2 includes auggie-review, cleanup, improve, research, reflect and tasklist.
- Their gate resolutions are defaults, not blocked: auggie-review "implies `--no-post-pr` and `--no-remediation-offer`" (`:100`); cleanup and improve "apply only items the file already allows ... list every 'Approval Required' item" (`:103,110`); research "pins `--strategy planning`" (`:116`); reflect "follow the existing headless auto-accept rule" (`:88`); tasklist "passes `--unattended` to each reflect" (`:122`).

Grading sentence: An implementer who follows section 3 builds these six commands so that `--unattended` resolves the gate by default and the run succeeds; AC-2.2 then asks for `--outcome failed` with `status: blocked` and a non-empty `blocked_question`, which these commands never produce, so AC-2.2 cannot pass for six of the fifteen P2 commands.

Recommendation: scope AC-2.2 to the P2 commands whose row says "blocked" (recommend, cli-eval, cli-portify, review-translation, spec-panel, task, tdd, troubleshoot, release-split) and give the other six a check that the default was applied (flags implied, items listed, strategy pinned).

### F5. MAJOR graded blocking. `/sc:load` is a P1 command under AC-1.1 and AC-1.2 but is defined as never dispatched and as having no report. Experts: Wiegers, Cockburn. Priority Medium. Quality impact: Consistency -1.

Quoted texts:
- Spec `:112` (load): report "none (see note)", "use it as a step inside another worker's brief, not as its own Task"; P1 "(usage line only)". Spec `:268` (Decisions): "a report file would be an unrequested addition".
- Spec `:195` (AC-1.1): the section must name `return-contract.yaml`. Spec `:196` (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>`", which includes steps 3 and 4 (`:182-183`).

Grading sentence: An implementer who follows `:112` writes no contract and adds no output flag for load; AC-1.2 runs load as a worker with `--output <dir>` and step 4 (`test -s <contract>`) cannot pass, and AC-1.1 requires a section that names a file the command never writes.

Recommendation: remove load from AC-1.1/AC-1.2 and check its usage-line fix only (AC-1.4-style grep for `--checkpoint`).

## ARCHITECTURE ANALYSIS

Architecture of the decision (sections 1.1-1.3, 4, 5) holds. Checked: coordinator-only list is consistent with the inventories (`INV-A:90-92`, `INV-B:285-287`), the 10/27/6 split sums to 43, and the depth-1 argument R1 is grounded in `CAPS:97-103`. Findings here are Medium and appear under follow-up candidates (F6-F9, F13). No architecture finding is blocking.

## WHITTAKER ADVERSARIAL ANALYSIS

- Sequence Attack on the rollout (`:154`, "Later phases do not start until the earlier phase's checks pass"): AC-0.4 sits in P0 and "a failure here reopens section 1" (`:194`), yet it cannot pass (F2), so P0 can never close and P1-P4 never start. Recorded as part of F2.
- Divergence Attack on WC-5 (`:63`): a `partial` status maps to `--outcome succeeded` and so settles the Task as completed (`CAPS:77`); Orca does not auto-start dependents (`CAPS:92`) so the coordinator still reads the report first. No wrong outcome without an extra assumption: noted only.
- Sentinel Collision Attack on the `--unattended` token (D1, `:228`): the spec does not say what happens when the token appears inside quoted specification text. The current spec-panel definition handles it (`command.md:459`). Medium, F10.
- Zero/Empty Attack on WC-4 (`:62`): "including stops before any other output exists" while workflow's contract directory is created later (`INV-B:272`: "Not written for pre-creation STOPs"). Medium, F8.
- Accumulation Attack: no counter or buffer is defined in the spec; none found.

## Guard Condition Boundary Table

Classes left out are named in the last rows. Status GAP rows are graded per FR-8/FR-9; none is blocking by itself (no concrete wrong outcome beyond those already in F1-F5), so they appear in follow-up candidates.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome mapping | `:63` | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| WC-5 outcome mapping | `:63` | One/Minimal | report exists, `status` key missing | unspecified | not stated (step 4 asserts the key, `:183`, the worker rule does not) | GAP (Medium, F9) |
| WC-5 outcome mapping | `:63` | Typical | `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `:63` | Sentinel Value Match | `partial`, audit verdict FAIL | succeeded | `--outcome succeeded`, first sentence states status | OK |
| WC-5 outcome mapping | `:63` | Legitimate Edge Case | `blocked` with empty `blocked_question` | failed | not stated (WC-4 says the question is carried "when blocked", `:62`) | GAP (Medium, F9) |
| WC-10 wait split | `:68` | Zero/Empty | wait of 0 s | n/a | no split needed | OK |
| WC-10 wait split | `:68` | Typical | 3 min wait | within 4 min | no split | OK |
| WC-10 wait split | `:68` | Maximum/Overflow | eval timeout 3600 s (`INV-A:65`) | split | waits of at most 4 min | OK (but no AC, F11) |
| WC-10 wait split | `:68` | Legitimate Edge Case | exactly 4 min and 5 min | 4 min allowed, 5 min not | stated ("longer than 5 minutes ... at most 4 minutes") but a 4 to 5 min single call is unspecified | GAP (minor) |
| `--unattended` detection | `:51`, D1 `:228` | Zero/Empty | flag absent | false | today's behaviour (SA-1, `:146`) | OK |
| `--unattended` detection | `:51`, D1 `:228` | Sentinel Value Match | token inside quoted input text | unspecified | not stated | GAP (Medium, F10) |
| WC-3 ask | `:61` | Zero/Empty | no preamble | blocked | write blocked report | OK |
| WC-3 ask | `:61` | Legitimate Edge Case | `ask` timeout | resume same ID | stated | OK |
| WC-3 ask | `:61` | Typical | coordinator answers | re-invoke "with the answer as a flag" | flag per command not named in section 3 | GAP (Medium, F12) |
| AC-C5 additive guard | `:176` | Sentinel Value Match | deleted bullet line `- x` shows as `-- x` | not matched by `^-[^-]` | check passes while a line was deleted | GAP (Medium, F7) |
| AC-C1 regex | `:172` | Typical | raw `\|` inside the ERE | never alternates (tested with GNU grep: no match on `orca orchestration ask`) | check prints nothing | GAP (Medium, F6) |

Left out: Maximum/Overflow for WC-5, WC-3, `--unattended` detection and AC guards (no capacity or numeric range exists for them); One/Minimal for WC-10, WC-3 and the detection guard (no distinct minimal value beyond Typical).

## Acceptance-criterion check (32 items, one by one)

"Pass" means it can pass as written for every command and phase it covers. Findings in the last column.

| ID | Covers | Can pass as written? | Reason | Finding |
|----|--------|----------------------|--------|---------|
| AC-C1 | all phases | Not as raw text | `\|` inside the `grep -E` pattern (`:172`) matches a literal `\|`, so it never alternates; tested: it prints nothing for `orca orchestration ask`. The `grep -v` pipe is also written `\|` (`:172`). It also fails if the contract file uses SA-2's permitted example (`:147`) | F6 |
| AC-C2 | all | Yes | `make verify-sync` (Makefile UNVERIFIED) | none |
| AC-C3 | all | Yes | baseline then re-run, pre-existing failures allowed | none |
| AC-C4 | all | Yes (weak) | checks only staged paths | none |
| AC-C5 | P1-P4 | Passes but can miss deletions | `^-[^-]` ignores deleted bullet lines (`-- `) and flags the Usage-line edit that adding a flag needs | F7 |
| 7.2 step 1 | all | Yes | exit 0 and `state: ready` (`CAPS:46`) | none |
| 7.2 step 2 | all | Yes, with step 3 conflict | worker-show every 5 min while step 3 may block 15 min | F8b (follow-up F14) |
| 7.2 step 3 | P0, P2 | No | report path = WC-4 path undefined for adversarial, workflow, troubleshoot, tdd | F2, F3 |
| 7.2 step 4 | P0, P1, P2 | No for those same commands; status vocabulary of existing contracts unknown | | F2, F3, F9 |
| 7.2 step 5 | all | Yes | wording "AskUserQuestion call" vague but checkable | none |
| 7.2 step 6 | editing commands | Ambiguous | cleanup, improve, implement, document, test `--fix` and reflect (writes a tracked docs file, `INV-B:114`) change files outside the output directory | follow-up F15 |
| 7.2 step 7 | all | Yes | `worker-release` shown without its target; `<run_id>` never created in steps 1-6 | minor note N2 |
| AC-0.1 | P0 | Yes | `install_core.py` UNVERIFIED | none |
| AC-0.2 | P0 | Yes | UNVERIFIED files | none |
| AC-0.3 | P0 | Yes | table rows start `|`, so `-|` lines match | none |
| AC-0.4 | P0 | No | see F2 | F2 |
| AC-1.1 | P1 | No | see F1, F5 | F1, F5 |
| AC-1.2 | P1 | No for load; unclear for the four fixed ready commands | F5; whether "P1 command" includes adversarial, cleanup-audit, index-repo, workflow is not stated | F5 |
| AC-1.3 | P1 | Yes | `claude -p` is headless, not a plain interactive session | N3 |
| AC-1.4 | P1 | Yes | static grep | none |
| AC-2.1 | P2 | Yes | static test | none |
| AC-2.2 | P2 | No | F3, F4 | F3, F4 |
| AC-2.3 | P2 | No | F3 (tdd, troubleshoot, release-split) | F3 |
| AC-2.4 | P2 | Passes, can miss | `gh api ... --jq length` reads page 1 (30 items) only, so a PR with 30 or more reviews or comments shows an unchanged count after a post | follow-up F16 |
| AC-2.5 | P2 | Yes | manual | none |
| AC-3.1 | P3 | Yes | static | none |
| AC-3.2 | P3 | Yes, conflicts with WC-6 | starts fresh in the directory that holds the first attempt's `.session-memory.md` (`:205`, `:64`) | follow-up F17 |
| AC-3.3 | P3 | Yes | contract not checked | none |
| AC-3.4 | P3 | Yes | `.superclaude/memory/*` UNVERIFIED | none |
| AC-4.1 | P4 | Yes | depends on D2, both branches stated | none |
| AC-4.2 | P4 | Uncertain | row `:113` requires an explicit pre-tag choice "else blocked"; AC-4.2 passes none, so an untagged version blocks before any outward step is skipped | follow-up F18 |
| AC-4.3 | P4 | Weak | heartbeats are messages, tool durations need timestamps; the transcript's content is not specified | follow-up F19 |

## Follow-up candidates (Medium and minor; never trigger a revision)

- F6 (Medium, AC-C1). Raw `\|` in the ERE (`:172`) never alternates (tested with GNU grep); and the permitted Orca example in the contract file (SA-2, `:147`) and the new Orca section in `HOW-WE-WORK.md` (P0, `:158`) live under `src/superclaude/core`, which AC-C1 scans with only `ccsession-tag` exempted. Needs a guess about the file wording, so not blocking.
- F7 (Medium, AC-C5/SA-4). `grep -E '^-[^-]'` (`:176`, `:193`) cannot see deleted bullet lines, and adding a flag to a Usage line shows a `-` line, though SA-4 (`:149`) calls flag additions additive.
- F8 (Medium). WC-4 "every outcome" (`:62`) and workflow's pre-creation STOP (`:92`) name no location for the contract when no package directory exists yet.
- F9 (Medium). The fixed status set (`:63`, Decisions `:263`) and the step-4 assertion (`:183`) are applied to contracts that "keep their fields" (`:62`); the existing status values of workflow, brainstorm, reflect and adversarial are not recorded in the spec (`INV-B:272` lists fields only). A blocked contract with an empty question is unspecified.
- F10 (Medium). D1(a) (`:228`) does not say how the `--unattended` token is recognised (standalone token outside quoted input), which the current spec-panel text defines (`command.md:459`).
- F11 (Medium). Requirements with no acceptance check: WC-1 (`:59`), WC-3 (`:61`), WC-6 (`:64`), WC-7 beyond AC-0.4, WC-9 for task commit/push (`:121`), WC-10 for cli-eval (`:104`; only pr-submit has AC-4.3), WC-11 beyond AC-3.4, WC-12 (`:70`).
- F12 (Medium). WC-3 (`:61`) says the session re-invokes "with the answer as a flag"; the blocked rows of section 3 (for example `:105,115,117,121`) do not name that flag. WC-3 also lets the worker ask instead of block, while AC-2.2 expects a blocked contract and `worker_done`; with an `ask` the live check waits on a `question` message (`:182` lists `question`). For implement, D2(a) (`:234`) keeps the Ruling rule but WC-3 does not exclude asking.
- F13 (Medium, stale row). The spec-panel row (`:120`) says "add `--output`; contract". The supplied definition already has `--output <file>` and `--report-dir` (`command.md:22-23`), an `## Unattended mode` section (`command.md:455-465`) that refuses `--unattended` without `--report-dir` (`command.md:460`) and writes `<report-dir>/return-contract.yaml` (`command.md:461`). A brief built from section 3 (`--output <dir>`) would be refused. The spec cites `cmd/spec-panel.md:455` for "no path" (`:120`, `INV-B:182`), but `command.md:455` is the unattended-mode heading, so those citations are stale or wrong. If `command.md` is the current file, spec-panel needs no new flag and the row should be removed from P2; UNVERIFIED because `cmd/spec-panel.md` is not in the workspace.
- F14 (Medium). Step 2 (`:181`, worker-show every 5 min) and step 3 (`:182`, `check --wait` with `--timeout-ms 900000`) cannot both hold in one coordinator turn.
- F15 (Medium). Step 6 (`:185`) lists output directory and "documented artifacts"; edits that are the deliverable (cleanup, improve, implement, document inline, `test --fix`) and the tracked `docs/memory/reflect/deviation-patterns-<slug>.md` that reflect writes by default (`INV-B:114`) are not clearly covered; the reflect default folder move is not turned off by `--unattended` (`:88`).
- F16 (Medium). AC-2.4 pagination (see table).
- F17 (Medium). AC-3.2 vs WC-6: the roadmap row (`:118`) resumes only with the flag; a retry in the same directory without the flag overwrites the first attempt, which WC-6 (`:64`) forbids unless a fresh directory is used.
- F18 (Medium). AC-4.2 vs the post-release row (`:113`).
- F19 (Medium). AC-4.3 evidence for heartbeat spacing and tool-call duration (`CAPS:130` says the cadence comes from the preamble).
- N1 (minor). Sections 1.1 and 2.1 (`:16`, `:51`) say the contract is the only command-side change; section 3 adds tool, flag and drift changes (`:108,118,124,125`).
- N2 (minor). Step 7 lacks the dispatch argument for `worker-release`.
- N3 (minor). AC-1.3 uses `claude -p`, a headless run, not a plain session.
- N4 (minor). Citations that could not be checked here: `EVIDENCE.md:39,45,56`, `.dev/codegraph-migration/orchestration/README.md:31,33,42`, `return-contract.yaml:10`, `CLAUDE.md:16,50,72-83,334,408`, `HOW-WE-WORK.md:22,171,249,254`, `install_core.py:4,13-24,33`, `pyproject.toml:38`, `Makefile:68-74` and every `cmd/` and `sk/` path (UNVERIFIED). The inventories quote most `sk/` and `cmd/` lines, and those were compared with the inventory text.

The session that ran this review has no user to ask whether to open an issue for these follow-up candidates and created none; the coordinator asks once for this loop.

## Reviser brief

Revise only the text a blocking finding names; add no rule, mechanism or section that a blocking finding does not call for; cite the finding id on each added paragraph or table; prefer deleting or narrowing text to adding; report the byte size of the spec before and after, and the bytes added and deleted per finding id. Leave the Medium and minor findings alone. Blocking finding ids: F1, F2, F3, F4, F5.

- F1: reconcile `:159` (Scope and Commands cells) with AC-1.1 (`:195`) so they name one command set.
- F2: make step 3 (`:182`), step 4 (`:183`) and AC-0.4 (`:194`) consistent with the paths in `:83,91,92` and with `:62,73`.
- F3: assign the WC-4 contract to release-split, tdd and troubleshoot (`:89-91`) and say where it goes when `--output` is a file (`:62,87,90`).
- F4: restrict AC-2.2 (`:200`) to the P2 commands whose row says blocked.
- F5: take `/sc:load` out of AC-1.1 and AC-1.2 (`:195-196`), keeping its usage-line fix.

verdict: FAIL
