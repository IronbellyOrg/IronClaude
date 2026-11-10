review: 1 of 3

# Review: Orca worker-contract spec, round 1

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (286 lines)
- Candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: none. Prior report: none. This is a first review (FIRST-REVIEW prompt, `document_review_loop_prompts.md`).
- Reviewer model: claude-haiku-5-5.
- Panel: `superclaude` is not installed in this sandbox, so `superclaude review panel resolve` and `superclaude review merge` were not run. One reviewer ran, and this is the loop summary note the brief asks for.
- Command mode: `/sc:spec-panel --mode critique --focus requirements,architecture` (command.md:256-265 Review Loop). `--focus correctness` is not active, so the State Variable Registry and Guard Condition Boundary Table (command.md:186-216) are not mandatory here. Pipeline Dimensional Analysis (command.md:351-353) does not trigger, because the spec describes no multi-stage data pipeline.
- Unattended mode: not active. The brief has no `--unattended` token, so `~/.claude/WORKER-CONTRACT.md` was not applied (command.md:455-465).

## Scope and coverage

Read in full:
- `command.md` (the `/sc:spec-panel` definition, copied into the sandbox).
- `home/.claude/rules/prompts/document_review_loop_prompts.md` (FIRST-REVIEW prompt).
- `.dev/orca-command-refactor/README.md:1-39` (shared context and rules).
- The candidate spec `specs/orca-worker-contract-spec.md:1-286`.
- `inventory/commands-a.md:1-121`, `inventory/commands-b.md:1-324`, `inventory/orca-capabilities.md:1-189`.

Not read, and why:
- `rf-qa.md` was not read. It applies only to re-review (review-loop item 5), and this is review 1.
- `~/.claude/WORKER-CONTRACT.md` was not read. The unattended mode is not active (see above).
- The workspace holds only `.dev/`. Every spec citation into `src/superclaude/...`, `.dev/codegraph-migration/...`, `.dev/evals/...`, `CLAUDE.md`, `pyproject.toml`, `Makefile`, `~/.claude/...` or the Orca application tree is UNVERIFIED here. Those citations are carried only as far as the inventories quote them.

Checked against the inventories (the only evidence available):
- Inventory-to-spec citations were spot-checked by reading the cited lines. Examples: `CAPS:92` (`orca-capabilities.md:92`, "Orca does not schedule automatically"), `CAPS:44-45` (`orca-capabilities.md:44-45`, 60 s default), `CAPS:73` (`orca-capabilities.md:73`, outcome mandatory), `INV-B:323` (`commands-b.md:323`, no command run end to end), `INV-A:60` (`commands-a.md:60`, adversarial contract filename), `INV-B:242` (`commands-b.md:242`, troubleshoot contract only with `--caller task-unified`). All matched.
- Counts (spec:75 "43 commands ... 10 ready, 27 needing a change, 6 coordinator-only") agree with the inventory summaries: 5 + 5 ready (`commands-a.md:73`, `commands-b.md:278`), 13 + 14 needs-change (`commands-a.md:73`, `commands-b.md:278`), 3 + 3 coordinator-only (`commands-a.md:87-92`, `commands-b.md:282-287`). The spec's 3.1 table has 10 rows (spec:83-92), its 3.2 table has 27 rows (spec:99-125), and its section 4 has 6 rows (spec:132-137). All consistent.
- Phase coverage: every 3.1 and 3.2 command appears in at least one phase row (spec:158-162).

Note on placement: the Findings block is the last section of the report. The Reviser brief sits directly above the verdict line, as the review-loop rule requires, so it comes after the Findings block.

## Blocking findings

### F1. Contradiction: AC-1.1 requires a contract for `/sc:load`, which the spec says must not have one

- Spec:195 (AC-1.1) requires that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`".
- Spec:112 (3.2 load row) gives the WC-4 report as "none (see note)" and the other change as "none: use it as a step inside another worker's brief".
- Spec:265 (Decisions, `/sc:load` handling) says a report file "would be an unrequested addition".
- Grading check: an implementer who follows AC-1.1 as written adds a `return-contract.yaml` to `/sc:load`. The load row and the Decisions table say that file must not exist, so the test and the design cannot both pass. Blocking, because two stated texts contradict each other.
- Inventory support: `commands-b.md:65` ("its only output is context for the current session") and `commands-b.md:31` (no report, load writes none).

### F2. Unpassable check: AC-0.4 step 4 cannot pass for `/sc:troubleshoot` or `/sc:adversarial`

- Spec:194 (AC-0.4) says "step 4 uses the command's existing report file, since the contract arrives in P1".
- Spec:183 (7.2 step 4) requires `test -s <contract>` and a YAML parse asserting `d['status']` and `d['command']`.
- `commands-b.md:242` says `/sc:troubleshoot` writes `return-contract.yaml` only with `--caller task-unified`. Its existing report is `REPORT.md` (`commands-b.md:242`, `:245`), which is not YAML, so the step-4 parse cannot pass.
- `commands-a.md:60` says the `/sc:adversarial` contract filename is not fixed, and spec:83 says the same. Step 4 names `<contract>` with no path, so it cannot be run as written.
- Grading check: an implementer who runs AC-0.4 on `/sc:troubleshoot` finds no YAML contract, and the P0 gate (spec:158) cannot close. Blocking, because an acceptance criterion cannot pass as stated.

### F3. Contradiction: `/sc:workflow` has no contract path known before dispatch

- Spec:62 (WC-4) requires "One report file, known before dispatch, written on every outcome", with `<output-dir>` being "the directory the coordinator passed (`--output` / `--output-dir`)".
- Spec:92 (3.1 workflow row) takes `--handoff none` only, with the report at `.dev/tasks/to-do/<id>/return-contract.yaml`. `<id>` is the package id, which exists only after the package is created (`commands-b.md:52`, `:275`, which says "one new package" and "Fresh package each run").
- Grading check: an implementer who dispatches `/sc:workflow` per row 92 cannot give the coordinator a report path before dispatch, so WC-4 and the 7.2 step-3 check ("its report path is the WC-4 contract path", spec:182) fail. Blocking, because two stated texts contradict each other.

### F4. Contradiction with data-loss risk: WC-4 and WC-6 disagree on where a retry writes

- Spec:62 (WC-4): the output directory is the one "the coordinator passed", and section 2.3 (spec:73) says the brief states it.
- Spec:64 (WC-6): a command without a resume flag "writes each run into a fresh output directory so a re-run starts clean", and a retry "must not corrupt the first attempt's output".
- Grading check: an implementer who follows WC-4 and 2.3 passes the same `--output` on a retry. A command with no resume flag then either overwrites the first attempt's files, which WC-6 forbids, or writes to a directory other than the one WC-4 says is known before dispatch. Blocking, because it names a data-loss outcome and the two texts contradict each other.
- Applies to the fresh-dir rows in 3.1 and 3.2 (for example reflect spec:88, troubleshoot spec:91, release-split spec:89).

## Follow-up candidates (Medium and minor, not blocking)

Each one fails the grading check for blocking: the wrong outcome needs a guess about which reading the implementer picks, or it is a requirement the document never states.

- M1 (Medium, label MAJOR). Spec:117 says "Phase 7 defaults to 'skip implementation'". The inventory's reading of the cited lines gives only "presents six options and waits for a choice" (`commands-b.md:39`), and `commands-b.md:145` says only that the default "should be" skip. The default is therefore not stated in the cited text. Source lines `sk/sc-review-translation-protocol/SKILL.md:174-183` are outside the workspace, so this is UNVERIFIED against the file itself.
- M2 (Medium, label MAJOR). Spec:104 gates `/sc:cli-eval run` on "the safety flags in the brief", but the spec never names them. The inventory cites `sk/sc-cli-eval-protocol/SKILL.md:135-146` for a confirmation of "safety flags" (`commands-a.md:44`), and that list is not reproduced. An implementer cannot tell whether a given brief passes or blocks.
- M3 (Medium, label MAJOR). Spec:61 (WC-3) says the worker may "re-invoke or resume the command with the answer as a flag", without saying how. For a fresh-dir command this repeats work or writes a second output (see F4), so the answered path is undefined.
- M4 (Medium, label MAJOR). Spec:88 says that under `--unattended`, reflect's `--remediate` follows "the existing headless auto-accept rule instead of the `[yes / no]` prompt". The spec does not say which registers that covers. Inventory `commands-b.md:109` gives the headless rule as auto-accepting "for auto-fixable registers", which the spec does not restate. Spec:122 (tasklist row) says Stage 10.5 passes `--unattended` to each reflect, but does not say whether it keeps `--remediate`, which `commands-b.md:46` and `commands-b.md:322` show it does today. Both points are undefined. WC-9 (spec:67) makes outward defaults off without a brief flag, and remediation is not on its list, so this is not counted as a blocking safety finding.
- M5 (Minor). Spec:22 says the worker "reached `state: ready, stage: input_accepted` and answered". The inventory quote of `EVIDENCE.md:45` (`orca-capabilities.md:49`) records only the ready state. "Answered" is not supported by the quoted text. The source file is outside the workspace, so this is UNVERIFIED against it.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "a report file would be an unrequested addition", "refs": ["AC-1.1", "section 3.2 load row", "section 4 Decisions: /sc:load handling"], "claim": "An implementer who follows AC-1.1 adds a return-contract.yaml to /sc:load, which the load row and the Decisions table say must not get a report file, so the test and the load design cannot both pass."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "step 4 uses the command's existing report file, since the contract arrives in P1", "anchor2": "test -s <contract>", "refs": ["AC-0.4", "7.2 step 4", "Phase P0"], "claim": "An implementer who runs AC-0.4 on /sc:troubleshoot finds REPORT.md rather than the YAML contract that step 4 parses, and on /sc:adversarial there is no fixed contract path, so the P0 gate cannot close as written."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "`--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml`", "anchor2": "One report file, known before dispatch, written on every outcome.", "refs": ["WC-4", "section 3.1 workflow row", "7.2 step 3"], "claim": "An implementer who dispatches /sc:workflow with --handoff none and no output directory gets a contract path that exists only after the package id is created, so the coordinator cannot know the report path before dispatch as WC-4 requires."}
{"id": "F4", "severity": "MAJOR", "blocking": true, "category": "data-loss", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "is the directory the coordinator passed", "refs": ["WC-4", "WC-6", "section 2.3"], "claim": "An implementer who passes the same --output on a retry gives a command with no resume flag a directory the first attempt already wrote, so it either overwrites that output, which WC-6 forbids, or writes elsewhere, which WC-4's known-before-dispatch path forbids."}
{"id": "M1", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Phase 7 defaults to \"skip implementation\"", "refs": ["section 3.2 review-translation row", "INV-B:39"], "claim": "The Phase 7 default is not stated in the cited lines (INV-B:39 gives only a six-option menu that waits for a choice), so an implementer must guess the worker's fix-or-skip behaviour."}
{"id": "M2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`run` requires `--suite` and the safety flags in the brief, else blocked", "refs": ["section 3.2 cli-eval row", "SA-1"], "claim": "The spec never names the safety flags, so an implementer cannot decide whether a given cli-eval brief passes or blocks."}
{"id": "M3", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "re-invoke or resume the command with the answer as a flag", "refs": ["WC-3", "WC-6"], "claim": "The spec does not say how a blocked worker re-invokes a command after the coordinator's answer, and a re-invoked fresh-dir command repeats its work or writes a second output, so the answered path is undefined."}
{"id": "M4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt", "refs": ["section 3.1 reflect row", "section 3.2 tasklist row", "SA-6", "WC-9"], "claim": "Adding --unattended to reflect auto-accepts remediation hand-offs for an unstated set of registers, and the tasklist row leaves open whether Stage 10.5 keeps --remediate."}
{"id": "M5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "(worker reached `state: ready, stage: input_accepted` and answered)", "refs": ["section 1.2 E2"], "claim": "The inventory quote of EVIDENCE.md:45 records only the ready state, so the 'answered' claim in E2 is not supported by the quoted evidence."}
```

## Reviser brief

Blocking findings to repair: F1, F2, F3, F4.

Restated rule (command.md:256-263): revise only text a blocking finding names. Add no rule, mechanism or section that a listed finding does not call for. Prefer deleting or narrowing to adding. Each added paragraph or table cites its finding id. Report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings (M1-M5) are not part of this brief and must not be edited.

verdict: FAIL
