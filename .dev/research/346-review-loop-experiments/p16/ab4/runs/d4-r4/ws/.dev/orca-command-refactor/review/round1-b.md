review: 1 of 3

# Spec-panel critique, round 1: Orca worker-contract spec

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: none given (first review; `--re-review` and `--baseline` both absent, so no `baseline: missing` note applies)
- reviewer model actually used: `claude-sonnet-5-5`
- lint file: `.dev/orca-command-refactor/review/lint-1.md` (lint says 0 findings, "Checks: REF"). There is no lint id to confirm or dismiss. The lint run did not stop this review.
- panel: Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial). Expert order follows the command's fixed sequence.
- scope of this report: this is ONE first review. The coordinator runs the second first-review and applies the MERGE rule and the VERIFY prompt. Merged ids (`M1`...) are the coordinator's, not mine.
- coverage: whole document (sections 1-9, Decisions, UNVERIFIED), every acceptance criterion in 7.1/7.3, every live-check step in 7.2, and a citation spot check of the inventories and of `orca-capabilities.md`.
- citation check: the workspace holds only `.dev/orca-command-refactor/` (README, three inventories, spec, lint). Every `cmd/…`, `sk/…`, `ag/…`, `CLAUDE.md:…`, `EVIDENCE.md:…`, `orca-data.json` and Orca-guide citation is UNVERIFIED by me except through the inventory line that quotes it. I opened and matched these citations: `INV-A:62,65,66,68,76-83,90-92,94-98,106,113,118,120`; `INV-B:272,285-287,289-301,311,320,323`; and the `CAPS:` lines 12-13, 44-47, 52, 58-80, 86-92, 97-103, 107-116, 128-130, 135-139, 145-151, 155-161, 177-188. All matched what the spec says they hold. `sk/sc-pr-submit-protocol/SKILL.md:37-39` (spec line 65) and `…:47-49` (`CAPS:161`, installed copy) disagree on the line numbers. This is UNVERIFIED, and not a finding.

## Blocking findings

Each finding states the grading sentence, "An implementer who follows the stated text as written builds X, and X is wrong because Y."

### F1. P0 live-check AC-0.4 cannot pass for `/sc:troubleshoot` or `/sc:workflow`
- Stated text A, spec line 194 (AC-0.4): run 7.2 on `/sc:troubleshoot`, `/sc:workflow … --handoff none` and `/sc:adversarial …`; "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". The same cell ends "a failure here reopens section 1".
- Stated text B, spec line 182 (7.2 step 3): the pass condition requires "its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path".
- Stated text C, spec line 91: `/sc:troubleshoot` reports `REPORT.md` and writes no WC-4 contract before P1. Line 92: `/sc:workflow` writes `.dev/tasks/to-do/<id>/return-contract.yaml`, a path the coordinator cannot know before dispatch. WC-4 (line 62) says the path is `<output-dir>/return-contract.yaml`.
- Sentence: an implementer who runs AC-0.4 as written builds a P0 gate whose step 3 requires a contract and a contract path that do not exist for troubleshoot or workflow at P0. The gate is wrong because it fails by construction. The spec then says the failure "reopens section 1", so the core decision (section 1) is reopened on a false failure.
- Only step 4 is carved out; step 3 is not.

### F2. AC-1.1 and AC-1.2 cannot pass for `/sc:load`
- Stated text A, spec line 112: `/sc:load` has Report "none (see note)", and "use it as a step inside another worker's brief, not as its own Task". Decisions line 265 repeats this ("a report file would be an unrequested addition").
- Stated text B, spec line 159: P1 lists `load` (usage line only). Line 195 (AC-1.1) requires every command in 3.1-3.2 to have a `## Unattended mode` section "naming `return-contract.yaml`". Line 196 (AC-1.2) runs the 7.2 live check on each P1 command. 7.2 step 3 needs a `worker_done` report path and step 4 runs `test -s <contract>` (lines 182-183).
- Sentence: an implementer who follows line 112 adds no report file to `/sc:load`. AC-1.1 and AC-1.2 then fail for load, because there is no contract to name or to `test -s`. Following AC-1.1/1.2 instead adds a contract that line 112 and line 265 reject.
- The two texts contradict each other.

### F3. WC-4's "known before dispatch" output location cannot be met for cleanup-audit, index-repo, workflow, or file-valued `--output` commands, so AC-1.2/AC-2.x steps 3-4 cannot pass for them
- WC-4 (line 62): the contract is `<output-dir>/return-contract.yaml`, "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Section 2.3 (line 73): "the output directory, so the report path is known before dispatch". AC-1.2 (line 196) runs each P1 command "with `--unattended --output <dir>`".
- Counter-texts:
  - `cleanup-audit`: "output dir is fixed, so one audit per worktree at a time" (line 85); the P1 fix only names the `--pass all` report, so it adds no `--output <dir>`.
  - `index-repo`: "State the output location" (line 86); no output flag is added.
  - `workflow`: the contract lives under `.dev/tasks/to-do/<id>/` (line 92), where `<id>` is generated by the command. The P1 fix is "write the contract for pre-creation STOPs too", and there is no `<id>` directory before creation, so that fix names no location.
  - `tdd` and `init-lite`: their `--output` is a file ("`--output <file>`", lines 87, 90). `<output-dir>` is then undefined, so 7.2 step 4's `<contract>` has no defined path. Row 3.2 `spec-panel` (line 120, "add `--output`") has the same ambiguity.
- Sentence: an implementer who follows WC-4 and AC-1.2 as written builds an `--output <dir>` and contract-location rule that these commands cannot meet. cleanup-audit, index-repo and workflow have no passable output directory, and tdd, init-lite and spec-panel take a file. The acceptance checks (7.2 steps 3-4) then fail for them, or the implementer invents a location per command.
- This is the same defect as an AC that cannot pass. The invented location is exactly what WC-4's single path rule is meant to prevent.

### F4. WC-4's contract path contradicts the adversarial row, so 7.2 step 3 fails for adversarial
- Stated text A, spec line 62 (WC-4): the contract is `<output-dir>/return-contract.yaml`, with `<output-dir>` the directory passed as `--output`.
- Stated text B, spec line 83 (3.1 adversarial row): "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)". `INV-A` (per-command notes, adversarial) confirms the artifacts live under `<output>/adversarial/`.
- Sentence: an implementer who follows the adversarial row writes the contract at `<output>/adversarial/return-contract.yaml`. 7.2 step 3 (line 182) requires "its report path is the WC-4 contract path", which is `<output>/return-contract.yaml`. The worker's `--report-path` and the check therefore point at different files, and AC-1.2 fails for adversarial.
- Implementing WC-4 instead contradicts line 83 and AC-1.4 (line 198, "adversarial names one fixed path"). Two stated texts contradict.

### F5. AC-2.2 cannot pass for P2 commands whose gate resolves by default instead of "blocked"
- Stated text A, spec line 200 (AC-2.2): "Gate-trigger run per P2 command … input that hits the gate"; pass is `worker_done --outcome failed`, contract `status: blocked` with a non-empty `blocked_question`.
- Stated text B, the section 3 rows for P2 commands (line 160 lists them):
  - `research` (line 116): `--unattended` pins `--strategy planning`; there is no blocked path.
  - `auggie-review` (line 100): posting and the offer are off, so nothing is asked.
  - `cleanup` and `improve` (lines 103, 110): apply the permitted items and list the rest in the report; the report is not blocked.
  - `tasklist` (line 122): passes `--unattended` to reflect so the headless rule applies; nothing is asked.
  - `reflect` (line 88): `--remediate` follows the headless auto-accept rule; nothing is asked.
- Sentence: an implementer who follows the rows builds five or more P2 commands that never write `status: blocked`. AC-2.2 requires every P2 command to produce it when given "input that hits the gate". For these commands no such input exists, so AC-2.2 fails, or its "per P2 command" is applied only to some commands, which the text never says.

### F6. AC-2.3's happy path cannot pass for `/sc:cli-portify`
- Stated text A, spec line 105: "each of the three approval gates resolves as blocked with the artifact to review named in the contract", with no flag or input that supplies an approval. The only new flag is `--resume <contract>`, defined as using the existing `resume_phase`/`resume_substep` fields.
- Stated text B, spec line 201 (AC-2.3): "Happy-path run per P2 command with every required flag in the brief"; pass is 7.2 with `--outcome succeeded`.
- Sentence: an implementer who follows line 105 builds a cli-portify whose every unattended run stops at the first approval gate as `blocked` (outcome `failed`). The text gives no brief flag that approves a gate and does not say that `--resume` counts as approval. AC-2.3 asks for `succeeded`, so it cannot pass as written.

## Acceptance criteria, one by one

Pass means it can pass as written for every command and phase it covers. F# points to the finding for any that cannot.

| ID | Spec line | Can pass as written? | Note |
|---|---|---|---|
| AC-C1 | 172 | Yes, with a Medium risk (M3, M10) | The grep reads as intended once markdown unescapes `\|`. It scans `src/superclaude/core`, which P0 edits (line 158). |
| AC-C2 | 173 | Yes | `make verify-sync` is a repo target (`CLAUDE.md:157`, UNVERIFIED here). |
| AC-C3 | 174 | Yes, with a Medium risk (M7) | Baseline-versus-after is well formed. In P0 "new tests pass" depends on what the new test asserts. |
| AC-C4 | 175 | Yes | |
| AC-C5 | 176 | Yes, with a Medium risk (M4) | Passes only if flags are added on new lines. |
| 7.2 step 1 | 180 | Yes | |
| 7.2 step 2 | 181 | Passes, but can pass vacuously (M5) | |
| 7.2 step 3 | 182 | No for troubleshoot/workflow at P0 (F1), adversarial (F4), and any command without a coordinator-known contract path (F3) | |
| 7.2 step 4 | 183 | No where no contract exists or its path is unknown (F2, F3). Risk for existing contracts' `status` values (M6). | |
| 7.2 step 5 | 184 | Passes. Ambiguous wording (M9). | |
| 7.2 step 6 | 185 | Yes | The "documented artifacts" carve-out covers `.claude-audit/`, `PROJECT_INDEX.md`, `claudedocs/`, `.dev/tasks/`. |
| 7.2 step 7 | 186 | Yes | Matches `CAPS:107-113`. |
| AC-0.1 | 191 | Yes | |
| AC-0.2 | 192 | Yes | |
| AC-0.3 | 193 | Yes | |
| AC-0.4 | 194 | No (F1) | |
| AC-1.1 | 195 | No for `load` (F2). Medium for the P4 commands (M1). | |
| AC-1.2 | 196 | No for load (F2), and for cleanup-audit, index-repo, workflow (F3) | |
| AC-1.3 | 197 | Yes | |
| AC-1.4 | 198 | Yes (a grep can only show a path is named). Its path conflicts with WC-4 (F4). | |
| AC-2.1 | 199 | Yes | Depends on P0's test file (M7). |
| AC-2.2 | 200 | No (F5) | |
| AC-2.3 | 201 | No for cli-portify (F6) | |
| AC-2.4 | 202 | Passes, but can pass vacuously (M8) | |
| AC-2.5 | 203 | Yes (manual) | |
| AC-3.1 | 204 | Yes | Can be satisfied by deleting the unsupported-flag list. |
| AC-3.2 | 205 | Yes, with a Medium risk (M11) | |
| AC-3.3 | 206 | Yes | |
| AC-3.4 | 207 | Yes | |
| AC-4.1 | 208 | Yes | |
| AC-4.2 | 209 | Yes | |
| AC-4.3 | 210 | Yes, conditional on D3 (b) and on the UNVERIFIED poll-script runtime (UNVERIFIED item 12) | |

## Check against the requirements WC-1..WC-12 and SA-1..SA-6

- WC-1, WC-3, WC-6, WC-12 and SA-4 have no acceptance check that exercises them. See M2.
- WC-5, WC-7, WC-8, WC-9 and WC-11 are covered, at least partly (7.2 step 3 and 5, AC-C1, AC-2.4/4.2, AC-3.4).
- WC-10 is checked only for pr-submit (AC-4.3). cli-eval's wait splitting (row 104) has no check.

## Follow-up candidates (Medium and minor; none blocks)

Per the Review Loop these never trigger a revision, fail a review or enter the Reviser brief. The session that ran the review asks the user once per loop whether to open an issue for them. This run is not interactive, so the question is NOT asked here and no issue is created. The coordinator should ask.

- M1 (Medium). P1 versus D2-D4 and the interim flag. Line 159 has every 3.1/3.2 command accept `--unattended` at P1, "a no-op where a command has no gate". Gates convert in P2-P4. Between phases a gated command accepts the flag but still prompts, so WC-2 (line 60, "never calls AskUserQuestion") does not hold. Line 195 also requires a section for pr-submit, but D3(a) (line 240) recommends no pr-submit changes. Needs a guess that someone dispatches a gated command mid-rollout.
- M2 (Medium). No acceptance check for WC-1, WC-3, WC-6 (retry safety) or WC-12. This is a requirement the document never tests, not a stated text that does harm.
- M3 (Medium). AC-C1 scans `src/superclaude/core` (line 172). P0 adds an Orca section to `HOW-WE-WORK.md` and a coordinator brief template (line 158), which can hit `orca-ide orchestration …`. SA-2 (line 147) restricts only command, skill and agent files, and the contract file is exempt only for "an example of a caller's question channel". Whether the new text contains a matching phrase is unknown.
- M4 (Medium). AC-C5 (line 176) fails on any removed line. SA-4 (line 149) allows "new flags". If a flag goes into an existing one-line Usage block, a `-` line appears.
- M5 (Medium). 7.2 step 2 (line 181) passes if `agentWait` is "never non-null". `CAPS:129` says an absent field means Orca never looked, and `CAPS:125` says a null `agentWait` can be absence. Section 1.4(2) (line 44) says a chat-question stall is silent. The check can pass for a stalled worker.
- M6 (Medium). WC-4 keeps an existing contract's fields (line 62), while 7.2 step 4 (line 183) asserts `status` is one of four values. The `status` vocabularies of the existing workflow, brainstorm, reflect and adversarial contracts were not read (`INV-B:272` names only the field). UNVERIFIED.
- M7 (Medium). P0 adds `tests/skills/test_worker_contract.py` (line 158) and AC-C3 needs "new tests pass". AC-1.1 describes that test as asserting an `## Unattended mode` section in every command, which is false at P0. What the P0 version asserts is not stated.
- M8 (Medium). AC-2.4 (line 202) counts with `gh api … --jq length` and no `--paginate`, so counts cap at one page (30). It also reads `pulls/<PR>/reviews` and `pulls/<PR>/comments` but not `issues/<PR>/comments`. A post can go uncounted.
- M9 (Medium). 7.2 step 5 (line 184) searches the transcript for the string `AskUserQuestion`. The loaded command text, the brief and the tool list can contain that string without a call.
- M10 (minor). The AC-C1 cell (line 172) contains `\|`, a markdown escape. Copied raw into `grep -E` it is a literal `|`, so the grep would never match.
- M11 (Medium). AC-3.2 (line 205) starts roadmap "fresh" in a `<dir>` that already holds `.session-memory.md`. WC-6 (line 64) says a re-run uses a fresh output directory so the first attempt is not overwritten.
- M12 (Medium). SA-3 (line 148) says report files are also written "when the caller passes the new output flag", while WC-4 (line 62) writes the contract only "in unattended mode". The text does not say whether `--output` alone writes a contract.
- M13 (Medium, UNVERIFIED). Row 122 (tasklist) has Stage 10.5 pass `--unattended` to reflect so the headless auto-accept rule applies. `INV-B:292` and the inventory's tasklist row say to drop `--remediate` at 10.5. The spec does not say what auto-accept triggers (a `sc:workflow` handoff) or that it is inside a subagent. SA-6 (line 151) and UNVERIFIED item 9 (line 280) say Orca is not treated as headless.
- M14 (minor). `pr-submit` is counted in the 27 "needs a change" (line 76) even though D3(a), the recommendation, makes no pr-submit change. The totals 10 + 27 + 6 = 43 do match both inventories (`INV-A:3`, `INV-B:3`).

## Reviser brief

Blocking finding ids: F1, F2, F3, F4, F5, F6.

Rules for the reviser (restated from the Review Loop, bullet 6; the reviser reads this report, not the command):
- Revise only text a blocking finding names.
- Add no rule, mechanism or section that no blocking finding calls for.
- Each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding.
- Report the byte size of the candidate before and after, and the bytes added and deleted per finding id.
- Leave minor and Medium findings alone. Do not award yourself a PASS.

verdict: FAIL
