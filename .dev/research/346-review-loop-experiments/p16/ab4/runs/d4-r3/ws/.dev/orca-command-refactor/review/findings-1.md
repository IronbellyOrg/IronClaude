Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B-1)
### B-1 (CRITICAL as raised, graded BLOCKING): the contract file's location is defined three incompatible ways
- Quoted texts and locations:
  1. SPEC:62 (WC-4): "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the report path is "known before dispatch".
  2. SPEC:90 (tdd row, section 3.1): "Brief must pass: ... `--output <file>`"; report today: "the TDD at `--output`". SPEC:87 (init-lite): "`--output <file>`". SPEC:200 (AC-2.2): "`/sc:tdd "auth" --unattended --output <file>`".
  3. SPEC:83 (adversarial): "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"; SPEC:92 (workflow): report is "`.dev/tasks/to-do/<id>/return-contract.yaml`" and the brief passes only `--handoff none`.
  4. SPEC:182 (7.2 step 3): the worker's report path "is the WC-4 contract path"; SPEC:183 (step 4) runs `test -s <contract>`.
- Grading sentence: An implementer who follows the stated text as written builds a tdd (and init-lite) worker whose contract lands at `<output-dir>/return-contract.yaml` with `<output-dir>` equal to the `--output` value the brief passes, which is a file path, so the contract path is `<TDD file>/return-contract.yaml`, a path that cannot be created beside a file; and a workflow worker whose contract path is chosen by the command (`<id>`), not by the coordinator before dispatch, and an adversarial worker whose contract sits one directory below `<output>`. Each is wrong because AC-2.2 and 7.2 steps 3-4 require the worker's `--report-path` to be the WC-4 path and `test -s` to pass on it, and for these commands that cannot hold. This is two stated texts that contradict (WC-4 vs the tdd, init-lite, adversarial and workflow rows) and a stated text an acceptance criterion cannot pass, so it is blocking.
- Evidence check: SPEC:62, 83, 87, 90, 92, 182-183, 200 read in the candidate. The per-command source lines behind the tdd/workflow rows (`sk/tdd/SKILL.md`, `sk/sc-workflow-protocol/refs/return-contract.md`) are not in the sandbox: UNVERIFIED, but B-1 rests on the spec's own text.

### M2

#### M2.a (round1-b.md F-1)
**F-1 [MAJOR, blocking] WC-4 puts the contract in a directory, while two commands and an acceptance check pass a file.**
- Texts: S:62 says the contract is `<output-dir>/return-contract.yaml`, "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". S:87 says init-lite is briefed with `--output <file>`; S:90 says the same for tdd; S:200 runs `/sc:tdd "auth" --unattended --output <file>` and requires "contract `status: blocked`"; S:183 runs `test -s <contract>`.
- Wrong outcome: an implementer who follows the stated text builds, for tdd and init-lite, a contract path of `<TDD file>/return-contract.yaml`, a path under a regular file that cannot be created, and AC-2.2 has no `<contract>` it can test. The two texts (directory versus file) contradict, and no text says where the contract goes instead.

### M3

#### M3.a (round1-b.md F-2)
**F-2 [MAJOR, blocking] WC-4's "directory the coordinator passed, known before dispatch" is false for several commands, and the live check depends on it.**
- Texts: S:62 and S:73 say the contract is `<output-dir>/return-contract.yaml` and "the output directory, so the report path is known before dispatch". Contradicting rows: adversarial `<output>/adversarial/return-contract.yaml` (S:83); workflow `.dev/tasks/to-do/<id>/return-contract.yaml` (S:92), whose `<id>` is made by the run (INV-B:272); implement "beside the ledger `progress.md`" (S:109; INV-A:51 gives `.dev/implement/<slug>/progress.md`); cleanup-audit and index-repo have a fixed location and no output flag (S:85-86); research (S:116), recommend (S:115), review-translation (S:117), task (S:121) and save (S:119) name a contract but no flag that sets its directory, and S:159 (P1) adds output flags only for analyze, build, business-panel, design, document, explain, index, test.
- Wrong outcome: live step 3 requires "its report path is the WC-4 contract path" (S:182) and AC-2.3 requires 7.2 to pass "with every required flag" (S:201). For research the implementer builds a command with no flag that places the contract, so the coordinator cannot give the path in the brief and step 3 fails; for adversarial the implementer must choose between `<output>/return-contract.yaml` (WC-4) and `<output>/adversarial/return-contract.yaml` (S:83), and AC-1.4 asks for "one fixed path" (S:198).

### M4

#### M4.a (round1-b.md F-3)
**F-3 [MAJOR, blocking] AC-0.4 requires, in P0, a contract and a flag that P0 does not have.**
- Texts: S:159 puts "the WC-4 contract in unattended mode" and the `--unattended` flag in P1; S:79 says ready commands "report the named file until Phase 1 adds the contract"; S:73 says the brief states "the exact command line including `--unattended`"; S:194 runs the three smoke commands without `--unattended`, says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file"; S:182 (step 3) requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Wrong outcome: an implementer runs AC-0.4 as written. For `/sc:troubleshoot` the existing report is `REPORT.md` (S:91), which is not a WC-4 contract and has no WC-4 `status`; step 3 cannot pass. The same holds for workflow (no `command` field, S:92) and adversarial (contract filename not fixed, S:83). Only step 4 was relaxed.

### M5

#### M5.a (round1-b.md F-4)
**F-4 [MAJOR, blocking] AC-1.1 and AC-1.2 demand a contract and a worker run for `/sc:load`, which the spec says has none and is not a Task.**
- Texts: S:112 (load row): report "none (see note)", resume "n/a", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)"; S:265: "a report file would be an unrequested addition"; S:195 (AC-1.1) asserts "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"; S:196 (AC-1.2) runs the 7.2 live check "on each P1 command with `--unattended --output <dir>`"; S:76 says every changed command gains the section; S:159 lists load as a P1 command.
- Wrong outcome: an implementer who follows AC-1.1 gives load a section naming `return-contract.yaml` (or fails the test), which the load row and S:265 forbid; AC-1.2 needs a load Task with a contract and `--output`, which the row says does not exist.

### M6

#### M6.a (round1-b.md F-5)
**F-5 [MAJOR, blocking] AC-2.2 expects a `blocked` outcome from every P2 command, but several resolve their gate without blocking.**
- Texts: S:60 gives three resolutions, (a) default, (b) flag, (c) blocked; S:200 requires for "each P2 command" a "gate-trigger run" ending `worker_done --outcome failed` with "`status: blocked` with a non-empty `blocked_question`"; S:160 lists the P2 commands. Rows with no blocked branch: auggie-review turns posting and the offer off (S:100); research pins `--strategy planning` (S:116); tasklist passes `--unattended` to reflect (S:122); reflect follows its headless auto-accept rule (S:88); cleanup and improve apply the allowed items and list the rest (S:103, 110).
- Wrong outcome: an implementer builds each of those commands exactly as its row says, and no input exists that makes it write `status: blocked`, so AC-2.2 cannot pass for them.
