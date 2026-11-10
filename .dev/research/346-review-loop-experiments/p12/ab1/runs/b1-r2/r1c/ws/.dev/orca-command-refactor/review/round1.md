review: 1 of 3

# Spec-panel critique, first review: Orca worker contract spec

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review of the full document)
- reviewer model used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). This is one of the three first-review reports; the coordinator merges them.
- Citations: `spec:N` = line N of the candidate. `CAPS:N`, `INV-A:N`, `INV-B:N` = line N of `.dev/orca-command-refactor/inventory/orca-capabilities.md`, `commands-a.md`, `commands-b.md` (read in this sandbox). Any `src/...`, `~/.claude/...` or `.dev/evals/...` path is not in the workspace and is marked UNVERIFIED.

## Coverage

Covered: the whole candidate (286 lines); `README.md` (binding context); the inventory lines the candidate cites for its load-bearing claims (CAPS:44-46, 52, 58-61, 65-68, 72-80, 97-103, 115-116, 129-130, 145-151, 155-161, 178-188; INV-A:3, 35, 60-61, 72-73, 76-83, 95-96, 106; INV-B:31, 52, 65, 267-275, 311, 323). Counts 10 ready / 27 needs-change / 6 coordinator-only were rechecked against INV-A:73 (5/13/3) and the INV-B rows: they add up (spec:76).
Not covered: every `cmd/`, `sk/`, `src/superclaude/cli/`, `CLAUDE.md`, `Makefile`, `EVIDENCE.md` and `~/.claude/` citation (UNVERIFIED, those files are outside the workspace); the spec's own claims of an independent citation check (spec:11, spec:285) are UNVERIFIED.

## Panel (critique mode, review order, requirements + architecture focus)

Wiegers (requirements quality), Adzic (examples/testability), Cockburn (actors and goals), Fowler (architecture/interfaces), Nygard (failure modes), Whittaker (adversarial), Newman, Hohpe as attributed below. Whittaker is active in every review.

## Prior-findings table

Not applicable (first review).

## Blocking findings

### B1: the P1 acceptance test requires an `## Unattended mode` section naming `return-contract.yaml` in `/sc:load`, which the same spec says gets no contract
- Severity: MAJOR, graded blocking (two stated texts contradict). Expert: Wiegers, Adzic. Priority: High.
- Texts:
  - `spec:195`: AC-1.1 "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `spec:112`: the `load` row in 3.2: Report "none (see note)", Resume "n/a", "use it as a step inside another worker's brief, not as its own Task"; `spec:159` lists "load (usage line only)" as the P1 scope.
  - `spec:265` (Decisions): for `/sc:load`, "a report file would be an unrequested addition. Only its usage-line defect is fixed." Supported by INV-B:31 and INV-B:65 ("writes no file").
  - `spec:76`: "Every changed command also gains the `## Unattended mode` section", and load's only change is the usage line.
- Wrong outcome: an implementer who follows the stated text as written builds P1 so that `/sc:load` gets only the usage-line fix (spec:112, 159, 265), and X is wrong because AC-1.1 (spec:195) then fails for `load`, so the P1 gate cannot pass; the only way to pass is to add an unattended section and a contract to `load`, which spec:265 rejects. The same assertion also covers the 3.1 commands whose "small fix" is "None" (brainstorm, init-lite, spec:84, 87) although spec:79 says their only change is that fix; and, as written, the commands that P2-P4 edit (spec:160-162), which P1 does not touch.
- Concrete attack (Whittaker, Sequence): run the P1 gate (spec:154 "Later phases do not start until the earlier phase's checks pass") with the spec's own scope: test goes red on `load` and on every P2-P4 command, P2 never starts.

### B2: WC-4 and section 2.3 say the report is `<output-dir>/return-contract.yaml`, known before dispatch; the spec's own rows put it elsewhere
- Severity: MAJOR, graded blocking (two stated texts contradict; the acceptance check cannot pass). Expert: Fowler, Nygard. Priority: High.
- Texts:
  - `spec:62` (WC-4): the command writes `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed"; "One report file, known before dispatch".
  - `spec:73` (2.3): the brief states "the output directory, so the report path is known before dispatch (WC-4)"; `spec:76`: "Contract means the WC-4 file `<output-dir>/return-contract.yaml`"; `spec:182-183`: 7.2 step 3 "its report path is the WC-4 contract path", step 4 `test -s <contract>`.
  - `spec:83` and `spec:198`: adversarial's contract is `<output>/adversarial/return-contract.yaml` (a subdirectory of the directory passed).
  - `spec:92`: workflow's contract is `.dev/tasks/to-do/<id>/return-contract.yaml`, brief passes only `--handoff none`; no output directory is passed. INV-B:52 and INV-B:272 confirm the `<id>` path and that it is not written for pre-creation STOPs (INV-B:272, `:39`); INV-A:60 and INV-A:115 confirm the adversarial file name is not fixed on disk.
- Wrong outcome: an implementer who follows the stated text builds a coordinator that opens `<dir>/return-contract.yaml` (spec:62, 73, 182-183) for an adversarial worker started with `--output <dir>`, but the file is at `<dir>/adversarial/return-contract.yaml` (spec:83); X is wrong because per WC-5 "or no report exists" maps to `--outcome failed` (spec:63), so a successful adversarial run is reported failed. For workflow the path contains an `<id>` the coordinator never supplies (spec:92), so "known before dispatch" and `test -s <contract>` (spec:183) cannot hold, and spec:92 "write the contract for pre-creation STOPs too" names no location because no `<id>` exists yet at such a stop.
- Concrete attack (Whittaker, Divergence): `/sc:adversarial --compare a.md b.md --output out/ --unattended`; state before: `out/` empty; after: `out/adversarial/return-contract.yaml` exists, `out/return-contract.yaml` absent; the WC-4 reader reports failed.

## Medium findings

Listed under follow-up candidates; none is blocking, none triggers a revision.

## Guard Condition Boundary Table

Trigger met (thresholds and conditional gates exist). Classes that cannot occur for a guard are left out with a one-line reason. Responsibility: Nygard (construction), Crispin (completeness), Whittaker (attack).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|--------------------|--------|
| `--unattended` switch | spec:51, 62, 128 | Zero/Empty (no `--output` dir given) | `--unattended` without an output dir | true | not specified: WC-4 needs `<output-dir>` but no refusal or default is stated | GAP (Medium, F3) |
| `--unattended` switch | spec:128 | Legitimate Edge Case (flag on a section-4 command) | `/sc:pm --unattended` | true | "get no --unattended mode" but refuse/ignore/run is not stated | GAP (Medium, F3) |
| WC-10 wait split | spec:68, 114, 210 | Typical | single wait 3 min | false | no split needed, heartbeat between calls | OK |
| WC-10 wait split | spec:68 vs 210 | Legitimate Edge Case | single wait 4.5 min | false (not "longer than 5 minutes") | WC-10 allows it; AC-4.3 "no single tool call exceeds 240 s" fails it | GAP (Medium, F4) |
| WC-10 wait split | spec:68 | Maximum/Overflow | wait 3600 s (cli-eval) | true | split into waits of at most 4 min | OK |
| WC-5 outcome map | spec:63 | Zero/Empty (no report) | file absent | true | `--outcome failed` | OK |
| WC-5 outcome map | spec:63, 183 | Legitimate Edge Case (report present, `status` missing or outside the four values) | `status: done` | n/a | not specified | GAP (Medium, F5) |
| Task confidence gate | spec:121 | Sentinel Value Match (exactly 0.70) | `0.70` | "below 0.70" is false | the 3.2 row names only "below 0.70"; the boundary's own rule is in `cmd/task.md`, UNVERIFIED | UNVERIFIED |
| Nesting depth | spec:33, 249-253 | Typical | depth 1 | true | worker `worker-start` refused (CAPS:97-99, 103 presumed) | OK |

Left out: Zero/Empty and Maximum for the depth guard and the confidence gate (a depth of 0 is the coordinator itself, CAPS:97 line 12-13 quoted; a confidence over 1.0 cannot occur). FR-10 note: all guards are enumerated and every populated row has a Status, so the table is complete.

Pipeline Dimensional Analysis (FR-17): not triggered; the spec describes no multi-stage data pipeline whose counts diverge (the coordinator-worker flow is control flow). `--focus correctness` is not active, so no State Variable Registry is required.

## Expert notes (non-finding)

- Wiegers: the WC rows state owner and evidence, which makes traceability good; the section-3 rows are the weakest link between a requirement and its test (B1).
- Adzic: AC-0.4 and AC-2.2 give concrete runs; AC-1.1 is the only example-free assertion and is the one that contradicts the rows.
- Cockburn: actors are clear (coordinator, worker session, command, person); D1-D5 are well scoped.
- Fowler/Newman/Hohpe: the decision to keep Orca above commands is consistent with CAPS:97-103 and CAPS:155-161 as read here; the interface between command and coordinator is the report file, which is exactly where B2 sits.
- Nygard: failure modes (silent stall, ask timeout, consumer_fenced) are covered by WC-2, WC-3, WC-12; the blocked-then-reinvoke overwrite of the contract (spec:61) is not described but is harmless.

## Follow-up candidates (Medium and minor; never trigger a revision)

Medium:
- F1: AC-C1 (`spec:172`) greps `src/superclaude/core` for `orca (orchestration|worktree|terminal|agent)` and expects nothing, but P0 adds `WORKER-CONTRACT.md` with a coordinator brief template and an Orca section in `HOW-WE-WORK.md` (`spec:158`), both in `core/`; SA-2 (`spec:147`) allows an Orca mention only inside the contract file. Whether those texts contain a matching phrase is a guess the text does not settle. Missing restriction, not a stated contradiction.
- F2: AC-C5 (`spec:176`) expects no deleted lines in command-file edits; adding `--unattended` to an existing `Usage` line (spec:159, 149) normally deletes that line. Graded Medium because a new usage line avoids it.
- F3: `--unattended` without an output dir, and `--unattended` on a section-4 command, have no stated behavior (spec:62, 73, 128). `command.md` for spec-panel in this sandbox already refuses a run without `--report-dir` and uses `--report-dir`, not `--output`/`--output-dir` (spec-panel `command.md:460`), so WC-4's flag name (spec:62) does not match that command; whether `cmd/spec-panel.md:22` (spec:120) is the same text is UNVERIFIED.
- F4: WC-10 splits only waits longer than 5 minutes into at most 4 minutes (spec:68); AC-4.3 fails any call over 240 s (spec:210) and the pr-submit row requires under 4 minutes (spec:114).
- F5: a report whose `status` is missing or not one of the four values has no outcome mapping (spec:63, 183).
- F6: D4 (spec:244) affects auggie-review `--post-pr` and task `commit`/`push`, which are P2 rows (spec:100, 121), while spec:154 says Phases 1-3 need no decision. Phases proceed on the recommendation (spec:225), so no wrong outcome.

Minor:
- The P1 scope sentence says every command in 3.1-3.2 accepts `--unattended` (spec:159) while its command list names only some (spec:159); `pr-submit` under D3(a) then gets a flag in P1 and "no changes" in P4 (spec:240).
- The independent-check claims at spec:11 and spec:285 (about 340 citations, 9 defects) cannot be checked here: UNVERIFIED.
- The cited `EVIDENCE.md:39,45,56` lines and all `src/` lines are UNVERIFIED in this sandbox; only the inventory quotes of them were checked (CAPS:52, INV-A:95, INV-A:106).

Per the review loop, the session that ran this review asks the user once whether to open an issue for the follow-up candidates; none is created without the user's answer.

## Reviser brief

Blocking finding ids: B1, B2 (to be re-keyed M1, M2... by the coordinator's merge). Rules for the reviser (restating the Review Loop reviser contract; the reviser reads this report, not the command):
- Revise only text a blocking finding names (spec:195 and the load/3.1 rows for B1; spec:62, 73, 76, 83, 92, 182-183, 198 for B2).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.
- Leave Medium and minor findings (F1-F6 and the minor notes) alone.

verdict: FAIL
