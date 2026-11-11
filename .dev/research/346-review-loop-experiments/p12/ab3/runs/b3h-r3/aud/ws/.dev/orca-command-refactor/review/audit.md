review: 1 of 3

# Spec-panel audit: orca-worker-contract-spec.md

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `92a25ab664b0803fb12bd23716793e4aba1f0dc0171d60f876c747679cfcf973`
- baseline: not given (first review of the whole document; labelled whole-document audit)
- command: `/sc:spec-panel --mode critique --focus requirements,architecture`; brief says baseline/re-review not used, so no `baseline: missing` mode switch applies
- reviewer model used: claude-sonnet-5-5
- brief clauses overridden: none
- coverage: the whole spec (sections 1-9, Decisions, UNVERIFIED list); every `CAPS:` citation I checked against `.dev/orca-command-refactor/inventory/orca-capabilities.md`, every `INV-A:`/`INV-B:` citation I checked against `commands-a.md`/`commands-b.md`. Citations to `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/` and `~/.claude` paths are UNVERIFIED (not in the sandbox) unless an inventory line quotes them. Experts used: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Newman, Hohpe (architecture); Whittaker (adversarial).

## Citation spot-check result
- Verified in inventories: counts 10 ready / 27 needs-change / 6 coordinator-only recount correctly (spec 3.1 has 10 rows, 3.2 has 27 rows, section 4 has 6 rows; A has 13 needs-change `commands-a.md:75`, B has 14 `commands-b.md:289`; A has 3 coordinator-only `commands-a.md:87`, B has 3 `commands-b.md:283-287`). `CAPS:44-46,52,58,64,66,72-73,76,79-80,97-99,101,103,115-116,129-130,145,147-150,155-156,158-160,177-188` match what the spec says they say. `INV-A:90-98,106,113,118,120`, `INV-B:31,34,45,285-286,289-299,301,311,320,323` match.
- Wrong citation: E2 cites `CAPS:161` for "`[H:worker-start]` line 38, `--agent claude`" (spec line 22). `orca-capabilities.md:161` is about top-level-only commands (pr-submit), and no line in the file quotes `[H:worker-start]` line 38. See M-4.
- UNVERIFIED (cannot check inside the workspace): E5 grep results (spec line 25), `CLAUDE.md:16,50,72-83,157,334,408` (spec lines 34,150,192,239,264), `.dev/evals/.../EVIDENCE.md:35-56` beyond what `orca-capabilities.md:49-52` quotes, `.dev/codegraph-migration/...:31,33,42` beyond `orca-capabilities.md:156`, every `sk/` and `cmd/` line in section 3 that is not quoted by an inventory, `src/superclaude/cli/install_core.py:4,13-24,33`, `pyproject.toml:38`, `Makefile:68-74`. A note: `orca-capabilities.md:161` places the pr-submit top-level rule at `SKILL.md:47-49` (the `~/.claude` copy) while the spec (line 65) and `commands-b.md:34` place it at `SKILL.md:37-39`; the two may be different copies, so the line is UNVERIFIED.

## === REQUIREMENTS ANALYSIS ===

### F-1 (blocking) Phase 1 text contradicts WC-2 and section 2.3 for every command whose gate converts in a later phase
- Severity: MAJOR, graded blocking. Experts: Wiegers, Adzic, Nygard.
- Grading sentence: An implementer who follows the stated text as written builds Phase 1 so that `--unattended` is accepted by cleanup, improve, cli-eval, cli-portify, task, tdd, troubleshoot, implement, post-release, pr-submit and the other gated commands while their gates are still live, and X is wrong because WC-2 says "Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question ..." and section 2.3 tells the coordinator to pass `--unattended` for "a command that already accepts it in the phase being run", so the coordinator passes the flag, the command still stops on a person-only prompt, and the worker stalls silently with no `worker_done` (the stall mode the spec itself describes at spec line 44).
- Evidence (two stated texts that contradict each other):
  - `specs/orca-worker-contract-spec.md:159`: P1 delivers "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 except `load` ... (a no-op where a command has no gate)". Gate resolution for gated commands is scheduled in P2 (`:160`), P3 (`:161`) and P4 (`:162`), and the section 3.2 Phase column agrees (for example cleanup `:103` P2, pr-submit `:114` P4, implement `:109` P4).
  - `specs/orca-worker-contract-spec.md:60`: WC-2 has no phase carve-out.
  - `specs/orca-worker-contract-spec.md:73`: the coordinator passes the flag only where "it already accepts it in the phase being run". After P1 every command accepts it, so the condition is satisfied for commands whose gate still prompts.
  - `specs/orca-worker-contract-spec.md:195` (AC-1.1) requires every command in 3.1-3.2 to carry a `## Unattended mode` section naming `return-contract.yaml` in P1, including pr-submit, post-release and implement, whose gate and outward-action rules wait for decisions D2-D4 (`:154`, `:162`).
  - The "no-op where a command has no gate" parenthesis does not cover gated commands, and P1's own list of commands (`:159`) names only the no-gate ones as "commands", so the sentence reads both ways. The scope sentence and the section 3 phase column cannot both hold.
- Recommendation: narrow P1 to "accepted by the commands whose section 3 phase is P1, plus the no-gate ready commands"; each command then gains the flag in the phase named in its section 3 row; state in 2.3 that the flag is passed only after the command's own phase has passed. Delete rather than add: this is a scope narrowing of one sentence plus AC-1.1.
- Priority: High.

## === ARCHITECTURE ANALYSIS ===

No blocking architecture finding. The central decision (Orca on top, commands stay units of work, section 1) is internally consistent with `CAPS:97-103` (depth 1), `CAPS:147-150` (standalone failure and pane-bound `worker_done`) and `INV-B:311`, and the rejected alternative's reasons R1-R5 check out against the cited lines. Findings below are Medium or minor.

## Follow-up candidates (Medium and minor; never fail the review)

### Medium

**M-1 (Hohpe/Fowler) Contract location is not one path for several commands.** WC-4 (`spec:62`) says every command in section 3 that accepts `--unattended` writes `<output-dir>/return-contract.yaml`, known before dispatch. Rows say otherwise or say nothing: implement "beside the ledger `progress.md`" (`:109`; ledger location not given), pr-submit "beside `monitor-run-<PR>.jsonl`" (`:114`), post-release "pointing at `post-release-report.md`" (`:113`), cli-portify "file location unnamed" (`:105`), and tdd, init-lite and spec-panel use a file-valued `--output` (`:90`, `:87`, `:120`) with no rule for which directory is meant. AC-2.2 runs `/sc:tdd ... --output <file>` and then reads the contract (`:200`, `:182` step 4), but the path is not defined. Needs a guess about which reading the implementer picks, so Medium.

**M-2 (Nygard/Whittaker, Sequence attack) Fresh-directory resume vs a path known before dispatch.** Most 3.2 rows say resume is "fresh dir" (`:99-125`), and WC-6 (`:64`) says a fresh output directory per re-run. WC-3 (`:61`) lets the worker ask, then re-invoke the command with the answer. After a `blocked` run and a re-invoke into a fresh directory, the contract the worker later passes as `--report-path` (WC-4, known before dispatch) may be the stale `blocked` file. The spec does not say whether a re-invoke after `ask` reuses the passed `<output-dir>` or creates a new one. Two readings allowed, so Medium.

**M-3 (Wiegers/Whittaker, Zero/Empty attack) No rule for `--unattended` with no output directory.** WC-4 defines `<output-dir>` as "the directory the coordinator passed" (`:62`); 2.3 says the brief carries it (`:73`) but no requirement says what the command does when `--unattended` is given without one. The only text is a missing-state gap, not a text that does harm, so Medium. A refuse-before-work-in-chat rule exists in the spec-panel command's own Unattended section (`command.md` Unattended mode, Report directory bullet), which suggests the gap is real and already solved elsewhere.

**M-4 (Wiegers) Evidence misattribution at E2.** Spec `:22` cites `CAPS:161` for `[H:worker-start]` line 38 `--agent claude`. `orca-capabilities.md:161` says something else (see Citation spot-check). The claim E2 supports (a worker is a top-level Claude session) is supported by `CAPS:44-52` and the EVIDENCE.md quote at `CAPS:49`, so the decision is not harmed. Fix the citation.

**M-5 (Cockburn/Whittaker, Divergence attack) Section 1.4 (2) overstates what the evidence shows.** The spec states that a command's own `AskUserQuestion` "comes *after* readiness, so it does not fail `worker-start`" (`:44`). `CAPS:47` records that for Claude the task is passed on the command line (`promptInjectionMode: 'argv'`), so the command's first turn can run before Orca sees the composer; `orca-capabilities.md:53` ("Spec consequence") says a question "before its agent input is ready" must not appear. Whether an immediate first-turn gate fails readiness is untested and `README.md:14` (binding context) says the opposite. The mitigation (WC-2, WC-1) is unaffected, so the harm is limited to a wrong failure expectation in AC-2.2 (`:200`, "worker_done --outcome failed ... `agentWait` never shown"). Reword as UNVERIFIED and add it to the UNVERIFIED list.

**M-6 (Crispin/Adzic) AC-0.4 step 4 cannot be applied as written.** AC-0.4 (`:194`) says step 4 "uses the command's existing report file"; step 4 (`:183`) runs `yaml.safe_load` and asserts `d['status']` and `d['command']`. troubleshoot's `REPORT.md` (`:91`) and adversarial's report are not that YAML, and workflow's contract has no `command` field guaranteed before P1. A tester must guess the replacement check.

**M-7 (Nygard) Reflect headless rule rests on an assumption the inventory marks untested.** `spec:88` and SA-6 (`:151`) have `--unattended` reuse the headless auto-accept rule, and tasklist (`:122`) passes `--unattended` to each reflect. `commands-b.md:310` and `:315` assume an Orca worker is not `--print`, and nothing in the spec states what auto-accept of a remediation hands off to (a nested `sc:workflow`) or how WC-8/WC-9 apply to it. UNVERIFIED item 9 (`:280`) covers the assumption but not the outward consequence.

**M-8 (Whittaker, Sentinel Collision) `blocked` and `partial` share the contract with an absent report.** WC-5 (`:63`) maps "no report exists" to `failed`, but a report that exists and is malformed or lacks `status` is not covered. AC step 4 (`:183`) would fail it, WC-5 would not. Missing state, Medium.

### Minor notes
- N-1: WC-10 says waits "at most 4 minutes" (`:68`), the pr-submit row says "under 4 minutes" (`:114`) and AC-4.3 says "no single tool call exceeds 240 s" (`:210`). At exactly 240 s the three differ.
- N-2: task row (`:121`) resolves confidence below 0.70 as blocked, and does not name the command's own override flag `--compliance [tier]` (`commands-b.md:199`) as a way the brief can supply the answer (WC-2 b).
- N-3: AC-C1 (`:172`) is written with `\|` for table rendering; pasted raw into a shell it will not run as written.
- N-4: the "27 needing a change" count includes `load` (`:112`), which receives no `## Unattended mode` section and no report (F-05); the heading "Needs a change (27)" is true but 3.1/3.2 AC-1.1 wording needs the exception each time (already stated).
- N-5: spec `:11` says "re-read 11 load-bearing locations"; I could not check any of the eleven (outside the sandbox), so the claim stays UNVERIFIED.

## Guard Condition Boundary Table
Guards in the spec with a numeric threshold, a sentinel or a boolean switch. Classes left out say why in one line.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | spec:51, 159 | Typical (flag present, command's phase passed) | flag on | true | WC-2 gate resolution | OK |
| `--unattended` switch | spec:73, 159, 160 | Legitimate Edge Case (flag present, command's gate converts in a later phase) | flag on, gate live | true | contradictory (see F-1) | GAP (blocking, F-1) |
| `<output-dir>` presence | spec:62 | Zero/Empty | no dir passed | true/false undefined | not specified (M-3) | GAP (Medium) |
| `<output-dir>` presence | spec:62, 90 | Legitimate Edge Case (`--output` is a file) | file path | undefined | not specified (M-1) | GAP (Medium) |
| WC-5 outcome map | spec:63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| WC-5 outcome map | spec:63 | Sentinel Value Match | file exists, `status` absent or invalid | undefined | not specified (M-8) | GAP (Medium) |
| WC-10 wait size | spec:68, 114, 210 | Maximum/Overflow | exactly 240 s | differs by text | N-1 | GAP (minor) |
| Heartbeat cadence | spec:68 | Typical | 5 min | true | heartbeat between waits | OK |
| Readiness limit | spec:59 | Maximum/Overflow | above ~45 s fallback | fail | WC-1 forbids | OK |
| Nesting depth 1 | spec:33, 66 | Typical | depth 1 | worker may not dispatch | WC-8 forbids | OK |
| task confidence < 0.70 | spec:121 | Typical | below 0.70 | blocked | blocked | OK |
| task confidence | spec:121 | One/Minimal edge (exactly 0.70) | 0.70 | not stated here | defers to command text, UNVERIFIED | UNVERIFIED |
| init-lite overwrite | spec:64, 87 | Legitimate Edge Case (existing unmarked file at `--output`) | unmarked file | undefined | only "marked" report named | GAP (minor) |
| `--monitor 1` | spec:114 | Typical | `--monitor 1` | refused | refused | OK |
| WC-10 wait, pr-submit | spec:114 | Zero/Empty | `--poll-interval 0` | not stated | not specified | GAP (minor) |

Left out: One/Minimal and Maximum/Overflow rows for the boolean and file-valued guards, because they cannot occur for a presence switch.

## Pipeline Dimensional Analysis
The spec describes a multi-stage flow (coordinator -> worker -> command -> contract -> `worker_done` -> coordinator reads). Counts: 1 Task -> 1 Dispatch -> 1 command -> 1 contract -> exactly 1 `worker_done` (WC-5). The one divergence is the retry path: `worker-start --retry-of` can produce N dispatches for one Task and N contracts in N fresh directories (WC-6, M-2), while the coordinator still reads "the" contract. This is already counted under M-2.

```text
[Task: 1] --> [Dispatch: 1..3 (retry-of, circuit breaker CAPS:116)]
                 |--> [Command run: 1 per dispatch] --> [contract in <output-dir> or fresh dir]
                 |                                          <-- MISMATCH when fresh dir (M-2)
                 `--> [worker_done: exactly 1 per dispatch]
```

## Whittaker attack notes
- Sequence attack: P1 before P2 (F-1). Concrete attack: after P1 passes, run `/sc:cleanup <dir> --unattended` (accepted per spec:159); state before: no unattended gate conversion; state after: the command prompts (cleanup `:103` converts in P2) and the worker is parked with no `worker_done`.
- Zero/Empty attack: no output directory (M-3).
- Sentinel collision: a report with `status: blocked` for a command whose WC-5 outcome is `failed` is treated the same as a crash; the coordinator distinguishes only through the contract (accepted by design).
- Accumulation: not applicable (no counters beyond retry cap of 3, `CAPS:80`).

## Coverage statement
Covered: all nine numbered sections, Decisions and UNVERIFIED items; counts; section 3 against the inventories where they quote the same lines; acceptance checks for command syntax and pass conditions. Not covered: `src/`, `CLAUDE.md`, EVIDENCE.md and the codegraph run files (not in the sandbox).

## Reviser brief
Blocking finding ids: F-1.
Rules (restated from the command's Review Loop, bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone.
F-1 text to repair: `specs/orca-worker-contract-spec.md:159` (P1 scope sentence), `:73` (the clause on when the coordinator passes `--unattended`) and `:195` (AC-1.1 scope). Make P1 accept the flag only on the commands whose section 3 phase is P1 plus the no-gate ready commands, and make 2.3 and AC-1.1 consistent with that.

verdict: FAIL
