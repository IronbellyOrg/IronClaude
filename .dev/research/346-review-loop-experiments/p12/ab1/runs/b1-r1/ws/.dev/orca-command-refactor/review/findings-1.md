Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B1)
### B1. CRITICAL (blocking). WC-4 fixes one contract location that the spec's own per-command rows contradict
- Quoted texts:
  - `spec:62`, WC-4: "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)."
  - `spec:83`, adversarial row: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)".
  - `spec:87` and `spec:90`, init-lite and tdd rows: brief passes `--output <file>`, report is "the TDD at `--output`" / "`.dev/superclaude/context-audit.md` or `--output`".
  - `spec:92`, workflow row: report is "`.dev/tasks/to-do/<id>/return-contract.yaml`" (the id is generated at run time).
  - `spec:73`: the brief states "the output directory, so the report path is known before dispatch (WC-4)".
  - `spec:182`, live check step 3: pass requires "its report path is the WC-4 contract path".
- Wrong outcome: An implementer who follows the stated text as written builds three incompatible things. For adversarial, WC-4 gives `<output>/return-contract.yaml` while the row gives `<output>/adversarial/return-contract.yaml`, so the coordinator opens a path that does not exist. For tdd and init-lite, `--output` is a file, so `<output-dir>` has no value and the implementer must invent where the contract goes. For workflow, the path contains an id that cannot be known before dispatch, which contradicts `spec:73`, and the pre-creation STOP case (`spec:92`, "Write the contract for pre-creation STOPs too") has no id and therefore no stated location at all. The build is wrong because acceptance step 3 (`spec:182`) compares the worker's `--report-path` with a path that the spec defines in two incompatible ways, so it cannot pass for at least adversarial and workflow.

### M2

#### M2.a (round1-a.md B2)
### B2. CRITICAL (blocking). Phase 1 and its acceptance check demand work that other parts of the spec say must not happen
- Quoted texts:
  - `spec:195`, AC-1.1: the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - `spec:159`, P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - Against it, `spec:112`, load row: report "none (see note)"; "use it as a step inside another worker's brief, not as its own Task". And `spec:265`: "a report file would be an unrequested addition."
  - Against it, `spec:240`, D3 recommended option (a): "no pr-submit changes in Phase 4", with `spec:154`: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4", and `spec:162` placing implement, post-release and pr-submit in P4.
  - Against it, `spec:159` itself lists only 13 commands in the P1 Commands column, while reflect, release-split, tdd, troubleshoot are scheduled in P2 (`spec:160`) and brainstorm, init-lite in no phase (see the Quantity Flow above).
- Wrong outcome: An implementer who follows AC-1.1 as written must give `load` an Unattended-mode section naming `return-contract.yaml`, which the load row and decision at `spec:265` say must not exist; and must edit pr-submit, implement and post-release in Phase 1 before the user answers D2 to D4, which `spec:154` and `spec:240` forbid. An implementer who follows the load row and the D3 recommendation builds a Phase 1 that fails its own acceptance check, so the phase gate in `spec:154` ("Later phases do not start until the earlier phase's checks in section 7 pass") blocks every later phase. The two texts cannot both hold.

### M3

#### M3.a (round1-b.md F1)
### F1 - CRITICAL-by-consequence, BLOCKING: AC-1.1 and the P1 sweep contradict the `/sc:load` row and its recorded Decision
- Stated texts that contradict:
  - Spec line 195 (AC-1.1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - Spec line 159 (P1): the `--unattended` flag is "accepted by every command in sections 3.1 and 3.2", and line 76: "Every changed command also gains the `## Unattended mode` section"; WC-4 (line 62): in unattended mode the command "writes `<output-dir>/return-contract.yaml`" on every outcome.
  - Spec line 112 (`load` row, section 3.2): Report column "none (see note)", Resume "n/a", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)". Spec line 265 (Decisions): "Use it inside a brief ... a report file would be an unrequested addition. Only its usage-line defect is fixed." `INV-B:65` supports that: "it only loads context into the current session and writes no file".
- Wrong outcome (grading sentence): An implementer who follows the stated text as written builds either an AC-1.1 test that fails on `load` (it has no `## Unattended mode` section and no contract by the row and the Decision), or a `load` that gains a section and a contract file that the row and Decision say must not exist; both cannot hold, so the P1 gate "every check in its block passes" (spec line 167) cannot be met by following the spec, and the phase can never be declared passed without picking which of the two texts to break.
- Same contradiction, smaller scope: `/sc:init-lite` is in section 3.1 with "Small fix: None" (line 87) yet is inside the P1 sweep of "every command in 3.1" (line 159) and AC-1.1/AC-1.2. Noted under this id, not a separate finding.

### M4

#### M4.a (round1-c.md B1)
### B1 (CRITICAL by label, blocking by consequence). WC-3 lets a blocked gate be answered by `ask`; AC-2.2 and AC-4.1 require the opposite outcome for the same input
- Texts: S:60 (WC-2 (c): on a gate the command writes `status: blocked` "and stops"); S:61 (WC-3: "When a gate would resolve as blocked and the worker session holds a preamble, the session **may instead** ask the coordinator once ... wait, then re-invoke"); S:200 (AC-2.2: gate-trigger run, pass = "`worker_done --outcome failed`; contract `status: blocked` ...; step 2 never shows `agentWait`"); S:208 (AC-4.1 same shape). `CAPS:58,129` (an `ask`-blocked worker is healthy; `agentWait` is how a parked worker shows).
- Wrong outcome: an implementer who follows WC-3 as written builds a worker session that, on the gate input of AC-2.2, calls `ask` and waits. That session sends no `worker_done --outcome failed` and the run is parked, so AC-2.2 fails for a worker that followed the spec. The acceptance criterion cannot be passed by a stated, permitted behaviour. Neither WC-3 nor S:73 (section 2.3, the brief) says which of the two the coordinator selects per Task, so the coordinator cannot make AC-2.2 deterministic.

### M5

#### M5.a (round1-c.md B2)
### B2 (CRITICAL by label, blocking by consequence). WC-4 puts the report at `<output-dir>/return-contract.yaml`, but the spec's own rows pass file-valued `--output` for tdd, init-lite and spec-panel, and AC-2.2 tests tdd that way
- Texts: S:62 (WC-4: `<output-dir>` "is the directory the coordinator passed (`--output` / `--output-dir`)", path "known before dispatch"); S:90 (tdd: "`--output <file>`", report = "the TDD at `--output`"); S:87 (init-lite: "`--output <file>`"); S:120 (spec-panel: "add `--output`", contract added); S:200 (AC-2.2: "`/sc:tdd "auth" --unattended --output <file>` ... contract `status: blocked`"); S:195-196 and S:182 step 4 (`test -s <contract>` on that path); S:148 (SA-3 ties the contract to "the new output flag"). Evidence: `INV-B:222,225` (tdd `--output` is the final TDD file), `INV-B:182,185` (spec-panel has no output flag today). Outside the listed evidence, the command definition `command.md:460-461` (this sandbox) keeps `--output` file-valued and uses a separate `--report-dir` for the contract directory, which is the split the spec does not make.
- Wrong outcome: an implementer who follows WC-4 literally for tdd builds the contract at `<file>/return-contract.yaml`, a path under a regular file that cannot exist. A worker told `--output docs/x/TDD_AUTH.md` has no directory to write to, so the "known before dispatch" path (S:62, S:73) does not exist and AC-2.2 step 4 cannot be run.
