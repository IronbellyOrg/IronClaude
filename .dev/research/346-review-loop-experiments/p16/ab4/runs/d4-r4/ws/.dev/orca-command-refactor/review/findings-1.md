Each Mn below is one finding; its sub-entries Mn.a, Mn.b, ... are the same finding as written by different reviewers. Confirm Mn when any sub-entry holds, and name that sub-entry in the reason.

### M1

#### M1.a (round1-a.md B1)
### B1. Phase 1 acceptance test demands changes to commands whose Phase 4 depends on user decisions D2-D4
- severity: CRITICAL-by-consequence (two stated texts contradict); expert: Wiegers, Whittaker (Sequence Attack)
- cited texts:
  - `specs/orca-worker-contract-spec.md:159` P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - `specs/orca-worker-contract-spec.md:195` AC-1.1: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one".
  - `specs/orca-worker-contract-spec.md:154` "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4."
  - `specs/orca-worker-contract-spec.md:240` D3 (a), the recommended option: "no pr-submit changes in Phase 4"; `specs/orca-worker-contract-spec.md:139` "`/sc:pr-submit` stays a worker candidate only if the user accepts open decision D3".
  - Section 3.2 rows for `implement` (line 109), `post-release` (line 113) and `pr-submit` (line 114) are in sections 3.1-3.2 and carry phase P4.
- stated wrong outcome: An implementer who follows the stated text as written builds, in Phase 1, an `--unattended` flag and a `## Unattended mode` section on `/sc:pr-submit`, `/sc:post-release` and `/sc:implement`, because AC-1.1 passes only when all 37 commands in 3.1-3.2 have one. That is wrong because the spec says Phases 1-3 need no user decision and D3 (a) (recommended) says pr-submit does not become a worker and gets no change; AC-1.1 therefore fails on the spec's own recommended choice. The same Phase 1 also publishes `--unattended` on gated commands (cleanup, cli-portify, task, tdd, pr-submit and others) whose gate resolutions only arrive in P2 or P4 (lines 160, 162). A worker briefed with `--unattended` under section 2.3 (line 73) then stalls on the old prompt while the flag claims no person is needed, which WC-2 (line 60) forbids.
- coverage line: both texts read at the cited lines; the 37-command set is the sum of lines 78-92 and 94-125.

### M2

#### M2.a (round1-a.md B2)
### B2. WC-4 puts the contract at `<output-dir>/return-contract.yaml` but several commands take a file as `--output`
- severity: MAJOR graded blocking (a stated text an acceptance criterion cannot pass); expert: Adzic, Fowler
- cited texts:
  - `specs/orca-worker-contract-spec.md:62` WC-4: "`<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)".
  - `specs/orca-worker-contract-spec.md:90` tdd row: "`--output <file>`; ... the TDD at `--output`".
  - `specs/orca-worker-contract-spec.md:87` init-lite row: "`--output <file>`".
  - `specs/orca-worker-contract-spec.md:200` AC-2.2: "`/sc:tdd "auth" --unattended --output <file>` with a bare topic" must end with "contract `status: blocked` with a non-empty `blocked_question`".
  - `specs/orca-worker-contract-spec.md:182` and `:183` (7.2 steps 3-4): the report path must be "the WC-4 contract path" and `test -s <contract>` must exit 0.
- stated wrong outcome: An implementer who follows the stated text as written builds, for tdd and init-lite, a contract at `<value of --output>/return-contract.yaml`, which is `<file>/return-contract.yaml` inside a regular file. That is wrong because the path cannot be created, so AC-2.2 and 7.2 step 4 cannot pass; the spec gives no other location for the contract of a command whose `--output` names a file. (`spec-panel` at line 120 says "add `--output`" without saying file or directory, and the same split applies to it.)
- coverage line: the file-valued `--output` for tdd and init-lite is the spec's own text (lines 87, 90); no inventory text says tdd's `--output` is a directory.

### M3

#### M3.a (round1-b.md F1)
### F1. P0 live-check AC-0.4 cannot pass for `/sc:troubleshoot` or `/sc:workflow`
- Stated text A, spec line 194 (AC-0.4): run 7.2 on `/sc:troubleshoot`, `/sc:workflow … --handoff none` and `/sc:adversarial …`; "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". The same cell ends "a failure here reopens section 1".
- Stated text B, spec line 182 (7.2 step 3): the pass condition requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Stated text C, spec line 91: `/sc:troubleshoot` reports `REPORT.md` and writes no WC-4 contract before P1. Line 92: `/sc:workflow` writes `.dev/tasks/to-do/<id>/return-contract.yaml`, a path the coordinator cannot know before dispatch. WC-4 (line 62) says the path is `<output-dir>/return-contract.yaml`.
- Sentence: an implementer who runs AC-0.4 as written builds a P0 gate whose step 3 requires a contract and a contract path that do not exist for troubleshoot or workflow at P0. The gate is wrong because it fails by construction. The spec then says the failure "reopens section 1", so the core decision (section 1) is reopened on a false failure.
- Only step 4 is carved out; step 3 is not.

### M4

#### M4.a (round1-b.md F2)
### F2. AC-1.1 and AC-1.2 cannot pass for `/sc:load`
- Stated text A, spec line 112: `/sc:load` has Report "none (see note)", and "use it as a step inside another worker's brief, not as its own Task". Decisions line 265 repeats this ("a report file would be an unrequested addition").
- Stated text B, spec line 159: P1 lists `load` (usage line only). Line 195 (AC-1.1) requires every command in 3.1-3.2 to have a `## Unattended mode` section "naming `return-contract.yaml`". Line 196 (AC-1.2) runs the 7.2 live check on each P1 command. 7.2 step 3 needs a `worker_done` report path and step 4 runs `test -s <contract>` (lines 182-183).
- Sentence: an implementer who follows line 112 adds no report file to `/sc:load`. AC-1.1 and AC-1.2 then fail for load, because there is no contract to name or to `test -s`. Following AC-1.1/1.2 instead adds a contract that line 112 and line 265 reject.
- The two texts contradict each other.

### M5

#### M5.a (round1-b.md F3)
### F3. WC-4's "known before dispatch" output location cannot be met for cleanup-audit, index-repo, workflow, or file-valued `--output` commands, so AC-1.2/AC-2.x steps 3-4 cannot pass for them
- WC-4 (line 62): the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Section 2.3 (line 73): "the output directory, so the report path is known before dispatch". AC-1.2 (line 196) runs each P1 command "with `--unattended --output <dir>`".
- Counter-texts:
  - `cleanup-audit`: "output dir is fixed, so one audit per worktree at a time" (line 85); the P1 fix only names the `--pass all` report, so it adds no `--output <dir>`.
  - `index-repo`: "State the output location" (line 86); no output flag is added.
  - `workflow`: the contract lives under `.dev/tasks/to-do/<id>/` (line 92), where `<id>` is generated by the command. The P1 fix is "write the contract for pre-creation STOPs too", and there is no `<id>` directory before creation, so that fix names no location.
  - `tdd` and `init-lite`: their `--output` is a file ("`--output <file>`", lines 87, 90). `<output-dir>` is then undefined, so 7.2 step 4's `<contract>` has no defined path. Row 3.2 `spec-panel` (line 120, "add `--output`") has the same ambiguity.
- Sentence: an implementer who follows WC-4 and AC-1.2 as written builds an `--output <dir>` and contract-location rule that these commands cannot meet. cleanup-audit, index-repo and workflow have no passable output directory, and tdd, init-lite and spec-panel take a file. The acceptance checks (7.2 steps 3-4) then fail for them, or the implementer invents a location per command.
- This is the same defect as an AC that cannot pass. The invented location is exactly what WC-4's single path rule is meant to prevent.

### M6

#### M6.a (round1-b.md F4)
### F4. WC-4's contract path contradicts the adversarial row, so 7.2 step 3 fails for adversarial
- Stated text A, spec line 62 (WC-4): the contract is `<output-dir>/return-contract.yaml`, with `<output-dir>` the directory passed as `--output`.
- Stated text B, spec line 83 (3.1 adversarial row): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)". `INV-A` (per-command notes, adversarial) confirms the artifacts live under `<output>/adversarial/`.
- Sentence: an implementer who follows the adversarial row writes the contract at `<output>/adversarial/return-contract.yaml`. 7.2 step 3 (line 182) requires "its report path is the WC-4 contract path", which is `<output>/return-contract.yaml`. The worker's `--report-path` and the check therefore point at different files, and AC-1.2 fails for adversarial.
- Implementing WC-4 instead contradicts line 83 and AC-1.4 (line 198, "adversarial names one fixed path"). Two stated texts contradict.

### M7

#### M7.a (round1-b.md F5)
### F5. AC-2.2 cannot pass for P2 commands whose gate resolves by default instead of "blocked"
- Stated text A, spec line 200 (AC-2.2): "Gate-trigger run per P2 command … input that hits the gate"; pass is `worker_done --outcome failed`, contract `status: blocked` with a non-empty `blocked_question`.
- Stated text B, the section 3 rows for P2 commands (line 160 lists them):
  - `research` (line 116): `--unattended` pins `--strategy planning`; there is no blocked path.
  - `auggie-review` (line 100): posting and the offer are off, so nothing is asked.
  - `cleanup` and `improve` (lines 103, 110): apply the permitted items and list the rest in the report; the report is not blocked.
  - `tasklist` (line 122): passes `--unattended` to reflect so the headless rule applies; nothing is asked.
  - `reflect` (line 88): `--remediate` follows the headless auto-accept rule; nothing is asked.
- Sentence: an implementer who follows the rows builds five or more P2 commands that never write `status: blocked`. AC-2.2 requires every P2 command to produce it when given "input that hits the gate". For these commands no such input exists, so AC-2.2 fails, or its "per P2 command" is applied only to some commands, which the text never says.

### M8

#### M8.a (round1-b.md F6)
### F6. AC-2.3's happy path cannot pass for `/sc:cli-portify`
- Stated text A, spec line 105: "each of the three approval gates resolves as blocked with the artifact to review named in the contract", with no flag or input that supplies an approval. The only new flag is `--resume <contract>`, defined as using the existing `resume_phase`/`resume_substep` fields.
- Stated text B, spec line 201 (AC-2.3): "Happy-path run per P2 command with every required flag in the brief"; pass is 7.2 with `--outcome succeeded`.
- Sentence: an implementer who follows line 105 builds a cli-portify whose every unattended run stops at the first approval gate as `blocked` (outcome `failed`). The text gives no brief flag that approves a gate and does not say that `--resume` counts as approval. AC-2.3 asks for `succeeded`, so it cannot pass as written.
