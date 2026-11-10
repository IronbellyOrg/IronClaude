review: 2 of 3

# Spec-panel review, round 2 (re-review): Orca worker-contract spec

| Field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture --re-review .dev/orca-command-refactor/review/round1.md --baseline .dev/orca-command-refactor/specs/history/spec-v1.md` |
| CANDIDATE (revised text under review) | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (58543 bytes, 285 lines) |
| sha256 (candidate) | `363aad34a552033a79d2d651495b742507e757c6d9545270ee860f0bf999e142` |
| BASELINE (text before the revision) | `.dev/orca-command-refactor/specs/history/spec-v1.md` (57763 bytes, 285 lines) |
| sha256 (baseline) | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (equals the candidate hash recorded in the prior report header, `round1.md:10`) |
| PRIOR (previous review report) | `.dev/orca-command-refactor/review/round1.md`, header `review: 1 of 3` (`round1.md:1`), last line `verdict: FAIL` (`round1.md:212`) |
| sha256 (prior, as read, with the coordinator's verification block inserted at `round1.md:2`) | `d9cdd37a4356732c0c4bc35693839d59eb3c8f49bcb28bb001034b7ec39bb46d` |
| Review number | N = 1 + 1 = 2, so `review: 2 of 3` |
| Reviewer model actually used | `claude-sonnet-5-5` |
| Review date | 2026-11-10 |
| Prompt followed | RE-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (home resolved to the sandbox `home/`), read in full before reviewing (hard gate, `command.md:266-268`) |
| Roles | CANDIDATE = the `@file`; BASELINE = `--baseline`; PRIOR = `--re-review`. Fixed by the command line, not inferred from reading order |
| Brief clauses overridden | none (the brief neither widens the scope nor grades a minor finding as blocking) |

Citation shorthand: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `round1.md:N` = line N of the prior report. Everything under `src/`, `.dev/codegraph-migration/`, `.dev/evals/`, `CLAUDE.md` and `~/.claude` other than the prompt file is not in the sandbox, so a citation that points only there is UNVERIFIED.

## Step 1: the evidence block (before any finding)

Command run: `diff -w specs/history/spec-v1.md specs/orca-worker-contract-spec.md` (BASELINE then CANDIDATE). Result: 6 hunks (five one-line hunks at lines 52, 62, 73, 76, 182 and one three-line hunk at lines 194-196), 8 lines before and 8 after, same line numbers on both sides. Byte change 57763 to 58543 = +780 (sum of the per-line length deltas 28 + 292 + 24 + 184 + 30 + 108 + 51 + 63 = 780). Lines starting `<` are copied under BEFORE (baseline), lines starting `>` under AFTER (candidate), verbatim.

Hunk 52c52

```text
BEFORE (baseline) spec-v1.md:52: - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
AFTER (candidate) orca-worker-contract-spec.md:52: - **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. Core `.md` files install to `~/.claude/` (`src/superclaude/cli/install_core.py:4,33`; `CLAUDE.md:83,408`), and the new name must be added to `KNOWN_CORE_FILES` (`src/superclaude/cli/install_core.py:13-24`). Each changed command that gets a contract (F-02) adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once.
```

Hunk 62c62

```text
BEFORE (baseline) spec-v1.md:62: | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
AFTER (candidate) orca-worker-contract-spec.md:62: | WC-4 | **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`); two commands keep the path they already use, named in their section 3 rows: adversarial `<output-dir>/adversarial/return-contract.yaml`, and workflow `.dev/tasks/to-do/<id>/return-contract.yaml`, whose `<id>` the command generates, so for workflow the worker passes the path it finds (F-03). It follows the return-contract pattern several commands already use and carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), and, when blocked, `blocked_question`. It is written on success, failure, blocked and partial outcomes, including stops before any other output exists. Commands that already write a contract keep their fields and add the missing ones. The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it. | Command writes; worker reports; coordinator reads | `CAPS:72-74` (`--report-path` only with real values); `CAPS:79` (Orca's handling of the file is UNVERIFIED); existing models: `sk/sc-workflow-protocol/refs/return-contract.md:3-19,41` via `INV-B:272`, `sk/sc-brainstorm-protocol/SKILL.md:335` via `INV-A:97` |
```

Hunk 73c73

```text
BEFORE (baseline) spec-v1.md:73: The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
AFTER (candidate) orca-worker-contract-spec.md:73: The contract only works if the brief carries what the command would otherwise ask a person. For each Task the coordinator's brief states: the exact command line including `--unattended` and every flag section 3 lists as required; the output directory, so the report path is known before dispatch (WC-4; not for workflow, F-03); which outward actions, if any, are authorized (WC-9); and the worktree placement (`CAPS:115`). After `worker_done`, the coordinator opens the report file, then releases or reuses the worker (`CAPS:107-113`).
```

Hunk 76c76

```text
BEFORE (baseline) spec-v1.md:76: The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file `<output-dir>/return-contract.yaml`. Every changed command also gains the `## Unattended mode` section (section 2.1). Phase numbers refer to section 6.
AFTER (candidate) orca-worker-contract-spec.md:76: The 43 commands in `cmd/` (21 in `INV-A:3`, 22 in `INV-B:3`) split into 10 ready today, 27 needing a change and 6 coordinator-only (section 4). The inventories hold the full evidence; each row below gives only what changes, with the deciding lines. "Contract" means the WC-4 file: `<output-dir>/return-contract.yaml` unless a row below names another path (adversarial, workflow; F-03). Every changed command that gets a contract also gains the `## Unattended mode` section (section 2.1); `load` (usage-line fix only) and the unchanged `brainstorm` and `init-lite` gain none (F-02). Phase numbers refer to section 6.
```

Hunk 182c182

```text
BEFORE (baseline) spec-v1.md:182: 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path.
AFTER (candidate) orca-worker-contract-spec.md:182: 3. `ORCA orchestration check --wait --types "worker_done,escalation,question" --timeout-ms 900000 --json` until `worker_done` arrives. **Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the contract path WC-4 gives for that command (F-03).
```

Hunk 194,196c194,196

```text
BEFORE (baseline) spec-v1.md:194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1. Record the results in the phase report; a failure here reopens section 1 |
BEFORE (baseline) spec-v1.md:195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
BEFORE (baseline) spec-v1.md:196: | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` | all steps pass |
AFTER (candidate) orca-worker-contract-spec.md:194: | P0 | AC-0.4 | 7.2 live check on `/sc:troubleshoot "<real symptom>"`, `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) | steps 1, 2 and 5-7 pass; in step 3 the `--outcome` and report path are judged against the command's existing report file, and in step 4 only `test -s` on that file applies, since the contract arrives in P1 (F-01). Record the results in the phase report; a failure here reopens section 1 |
AFTER (candidate) orca-worker-contract-spec.md:195: | P1 | AC-1.1 | `uv run pytest tests/skills/test_worker_contract.py -q`; the test asserts that every command in sections 3.1-3.2 except `load`, `brainstorm` and `init-lite` (F-02) has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`, and that no section-4 command has one | passes |
AFTER (candidate) orca-worker-contract-spec.md:196: | P1 | AC-1.2 | 7.2 live check on each P1 command with `--unattended --output <dir>` (workflow: `--unattended --handoff none`, no `--output`; F-03) | all steps pass |
```

## Self-check (run before the verdict)

- Each of the 8 AFTER lines (without `>`), searched with `grep -nF` in the CANDIDATE: found, at lines 52, 62, 73, 76, 182, 194, 195, 196, the same line numbers as in the evidence block.
- Each of the 8 BEFORE lines (without `<`), searched with `grep -nF` in the BASELINE: found, at lines 52, 62, 73, 76, 182, 194, 195, 196.
- Each BEFORE line searched in the CANDIDATE: 0 matches (all 8). Roles are not swapped.
- `rf-qa.md` (Fix Cycle steps 1-5, `command.md:262`): neither the project `.claude/agents/rf-qa.md` (no `.claude/` in the workspace) nor `~/.claude/agents/rf-qa.md` (only `home/.claude/rules/` exists) is readable here. Per `command.md:262` the rules of the Review Loop section stand alone and were applied without it.

## Prior blocking findings: re-check

Decided by comparing each prior defect with the AFTER text only. The verification block at `round1.md:2` confirmed exactly F-01, F-02, F-03 and rejected none, so there are no noted-and-unactioned ids.

| id | Status | Basis (AFTER text against the defect quoted in `round1.md`) |
|---|---|---|
| F-01 | resolved | The defect was that AC-0.4 required step 3 to pass on a contract and `status` that P0 commands do not write (`round1.md:85-95`). AFTER `spec:194` now passes "steps 1, 2 and 5-7", judges step 3 "against the command's existing report file", and limits step 4 to `test -s` on that file, "since the contract arrives in P1 (F-01)". The python `status`/`command` assertion (`spec:183`) no longer applies to P0, and `spec:91-92` plus `INV-B:242` (troubleshoot writes `return-contract.yaml` only with `--caller task-unified`) show why that was needed. `spec:154` therefore no longer blocks P1 on an unpassable check. Residual wording gaps are Medium (R2-05) and a minor note (N2-01), not a restoration of the defect |
| F-02 | resolved | The defect was that AC-1.1 required an `## Unattended mode` section naming `return-contract.yaml` in `load`, which the spec says gets no report file (`round1.md:97-106`). AFTER `spec:195` excludes `load`, `brainstorm` and `init-lite`; AFTER `spec:76` states the same three exclusions and AFTER `spec:52` limits the section to commands "that gets a contract"; these agree with the unchanged `spec:112` (load: report "none", "P1 (usage line only)"), `spec:84` and `spec:87` ("None") and `spec:265`. The two texts that could not both be satisfied now agree. Residual issues on neighbouring checks are Medium (R2-02, R2-03) |
| F-03 | resolved | The defect was that WC-4 stated one contract path while the adversarial and workflow rows and the live check used others (`round1.md:108-117`). AFTER `spec:62` now names both exceptions (adversarial `<output-dir>/adversarial/return-contract.yaml`, workflow `.dev/tasks/to-do/<id>/return-contract.yaml`); this equals `spec:83` (adversarial fix), `spec:92` and `spec:198` (AC-1.4, one fixed path). AFTER `spec:73` drops the "known before dispatch" duty for workflow, AFTER `spec:182` and `spec:196` take "the contract path WC-4 gives for that command" and use `--unattended --handoff none`, no `--output`, for workflow. The adversarial path matches `INV-A:35` ("real runs wrote `<output>/adversarial/return-contract.yaml`"). Residual issues on the same family (rows that name a third and fourth location, how workflow's path is found) are Medium (R2-01, R2-04) |

Regressed: none. Open: none. Deferred or withdrawn by the reviser: none.

## Scope check of the revision (reviser contract, `command.md:263`)

- Only 8 lines changed (evidence block above). Every changed line cites F-01, F-02 or F-03 in the added text (`spec:52`, `62`, `73`, `76`, `182`, `194`, `195`, `196`).
- No line named only by a Medium or minor finding was edited: `spec:68`, `spec:114`, `spec:154`, `spec:172`, `spec:176`, `spec:225` and `spec:244` are identical in both files (no hunk touches them).
- Added text is narrowing or carving out (exclusion lists, a carve-out clause, a path rule that restates existing rows). No new section, rule or mechanism.
- Bytes: baseline 57763, candidate 58543, net +780, all additions. My attribution from the per-line deltas: F-01 `spec:194` +108; F-02 `spec:52` +28, `spec:195` +51; F-03 `spec:62` +292, `spec:73` +24, `spec:182` +30, `spec:196` +63; `spec:76` +184 is shared by F-02 and F-03. The reviser's own per-id byte report was not among the inputs, so a match to it is UNVERIFIED.

## Coverage (what was covered)

- Read in full: the candidate (285 lines), the baseline diff, the prior report (213 lines), `README.md`, `command.md`, the review-loop prompts file. Read for the cited targets: `inventory/commands-a.md:35-55,60,73` and `inventory/commands-b.md:31-52,240-243,267-278`.
- Dependencies of the changed lines that I traced: WC-4/WC-5 (`spec:62-63`), the section 3 rows that name a contract path (`spec:83,85-87,92,105,109,112,114,116,119`), the section 6 P0/P1 rows (`spec:158-159`), the 7.2 steps (`spec:180-186`), AC-0.4, AC-1.1 to AC-1.4 (`spec:194-198`), the decisions table (`spec:265`) and the section 3 count (10 + 27 + 6 = 43, unchanged: rows `spec:83-92`, `spec:99-125`, `spec:132-137`).
- Not covered, UNVERIFIED: every `src/superclaude/...` line the spec cites, `EVIDENCE.md`, the PR #329 run files, whether `/sc:workflow` prints its package path, and whether `/sc:implement` or `/sc:pr-submit` take an output-directory flag (`cmd/implement.md`, `cmd/pr-submit.md` are not in the sandbox).
- Not re-reviewed: unchanged text and the Medium and minor findings of the prior report. They are not re-graded and not carried into this report's findings (the prior report's follow-up list stays as it is).
- Focus: requirements and architecture. All 11 panel experts spoke.

## Panel record (review order)

1. **Wiegers**: the three blocking defects are gone. Traceability of the added text is good (every addition cites its finding id). New requirement conflicts are only in neighbouring checks (R2-02, R2-03).
2. **Adzic**: AC-0.4 gives no example of what "judged against the existing report file" means for `REPORT.md` (R2-05).
3. **Cockburn**: the coordinator's goal for workflow (find the report) now has an unspecified step (R2-04).
4. **Fowler**: the contract path is now a rule with two named exceptions plus a general "unless a row below names another path" (`spec:76`); the count "two" in WC-4 understates the rows (R2-01).
5. **Nygard**: the pre-creation workflow stop remains a hole that the new `<id>` path makes visible (`spec:92`, `spec:62`, `INV-B:272`); already on the prior follow-up list, not re-graded.
6. **Whittaker**: attacks are in the Guard Condition Boundary Table and findings below (Sequence and Accumulation attack on workflow, Divergence attack on AC-1.2).
7. **Newman**: the interface (flag plus file) now has path exceptions listed in WC-4; no version field (prior note, not re-graded).
8. **Hohpe**: message-then-pointer holds for workflow only if the worker can name the right file (R2-04).
9. **Crispin**: AC-0.4 is now passable; AC-1.1 and AC-1.2 quantify over command sets that disagree with the phase table (R2-02, R2-03).
10. **Gregory**: quality expectations per phase stay explicit; the exclusion list in AC-1.1 is clear.
11. **Hightower**: no operational change in the revised lines.

## Guard Condition Boundary Table (guards on changed lines only)

Hard gate (FR-10) completed before synthesis. In a re-review the table covers guards on changed lines only (`command.md:262`). Guards: GA the WC-4 path rule (`spec:62`, `spec:73`, `spec:76`, `spec:182`); GB the P0 carve-out in AC-0.4 (`spec:194`); GC the AC-1.1 exclusion list and the "gets a contract" test (`spec:52`, `spec:76`, `spec:195`); GD the AC-1.2 invocation form (`spec:196`).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| GA path rule | spec:62 | Zero/Empty | `--unattended` with no directory flag | not defined | none: "the directory the coordinator passed" (`spec:62`); a gap that exists in the baseline (`spec:62` before) and is not caused by the revision, already on the prior follow-up list | GAP (not new; Medium, not re-graded) |
| GA path rule | spec:62 | One/Minimal | `--output D` for a standard command | default branch | `D/return-contract.yaml` (`spec:62`) | OK |
| GA path rule | spec:62, 83 | Sentinel Value Match | adversarial, `--output D` where `D` itself ends in `adversarial` | named exception | `D/adversarial/return-contract.yaml` by formula (`spec:62`, `spec:83`); `INV-A:35` records the nested `adversarial/adversarial/` location in real runs, which this formula yields as well | OK |
| GA path rule | spec:62, 92 | Legitimate Edge Case | workflow, `<id>` generated by the command, no coordinator directory | named exception | "the worker passes the path it finds": no method to find it (R2-04) | GAP |
| GA path rule | spec:62, 109, 114 | Legitimate Edge Case | implement ("beside the ledger `progress.md`", ledger at `.dev/implement/<slug>/progress.md`, `INV-A:51`) and pr-submit ("beside `monitor-run-<PR>.jsonl`", `INV-B:34`) | neither default nor one of the two named exceptions | `spec:76` says "unless a row below names another path"; WC-4 says "two commands" | GAP (R2-01) |
| GA path rule | spec:62, 92 | Maximum/Overflow | two workflow workers in one worktree, two packages under `.dev/tasks/to-do/` | named exception | "the path it finds": which package is not specified (R2-04) | GAP |
| GB P0 carve-out | spec:194, 183 | Zero/Empty | the command wrote no report at all | step 4 `test -s` fails | step 4 fails, so AC-0.4 fails and "reopens section 1" (`spec:194`) | OK |
| GB P0 carve-out | spec:194, 91 | Typical | troubleshoot, report `REPORT.md` exists and is non-empty | `test -s` passes | passes (`spec:91`, `spec:194`) | OK |
| GB P0 carve-out | spec:194, 63 | Legitimate Edge Case | existing report has no WC-4 `status` key (troubleshoot `REPORT.md`, `INV-B:242`; workflow's own vocabulary UNVERIFIED, `INV-B:272`) | step 3 "judged against the command's existing report file" | no rule for deriving the expected `--outcome` from such a file (R2-05) | GAP |
| GB P0 carve-out | spec:194, 83 | Legitimate Edge Case | adversarial, whose contract filename and place are "not fixed" before P1 (`spec:83`; `INV-A:35`, `INV-A:60`: two locations seen) | "the command's existing report file" | which file is "that file" is not stated (R2-05) | GAP |
| GC exclusion list | spec:195, 76 | Zero/Empty | a command in 3.1-3.2 with no section and not excluded | test fails | fails; stated by "has a section" (`spec:195`) | OK |
| GC exclusion list | spec:195, 112 | Sentinel Value Match | `load`, `brainstorm`, `init-lite` | excluded | excluded; matches `spec:76`, `spec:112`, `spec:84`, `spec:87` | OK |
| GC exclusion list | spec:195, 159-162 | Legitimate Edge Case | a command whose edit the table schedules for P2, P3 or P4 (22 of the 34 commands the test covers), tested at the P1 gate | test covers "every command in sections 3.1-3.2" | two readings: all 34 get the section in P1 (`spec:159` "accepted by every command") or only the 12 P1-scheduled ones do (R2-03) | GAP |
| GD AC-1.2 form | spec:196 | Typical | analyze with `--unattended --output <dir>` | applies | all 7.2 steps pass | OK |
| GD AC-1.2 form | spec:196, 92 | Legitimate Edge Case | workflow | variant | `--unattended --handoff none`, no `--output` (F-03 carve-out) | OK |
| GD AC-1.2 form | spec:196, 112, 159 | Legitimate Edge Case | `load` (listed in the P1 row), no contract, "use it ... not as its own Task" | "each P1 command" | applies by wording, cannot pass step 4 (R2-02) | GAP |
| GD AC-1.2 form | spec:196, 85, 86 | Legitimate Edge Case | cleanup-audit (output dir fixed) and index-repo (brief passes no flags), both P1 | "`--output <dir>`" | flag form does not exist for them; contract location unstated (R2-02) | GAP |

Classes left out: GA Maximum for the default branch (a path has no capacity beyond the two-workflow case above); GB One/Minimal and Maximum (the carve-out is a phase test with no count); GB Sentinel (no sentinel value); GC One/Minimal and Maximum (a list membership test); GC Typical beyond the Zero row (a command with the section passes); GD Zero/Empty, One/Minimal, Sentinel, Maximum (a command form has no countable input).

Status GAP rows graded under FR-8 and FR-9: none names a concrete wrong outcome without a further assumption about which of two readings an implementer picks, so each is Medium and goes under `follow-up candidates` (R2-01 to R2-05). No blank Specified Behavior entry is left except the first row, which is not new.

Pipeline Dimensional Analysis: not triggered (no changed line adds a multi-stage flow). The one count is the partition 43 = 10 + 27 + 6, unchanged by the revision; the AC-1.1 scope is 37 - 3 = 34 commands (used in R2-03).

## Findings on lines changed against the baseline

Grading used: CRITICAL is blocking. A MAJOR or FR-8/FR-9 finding is blocking only if "An implementer who follows the stated text as written builds X, and X is wrong because Y" holds with no further assumption (two stated texts that contradict, a stated text that causes data loss or breaks a safety boundary, or a stated text that an acceptance criterion cannot pass). Otherwise it is Medium. Every finding below is Medium or minor; for each, the reason it is not blocking is stated.

=== REQUIREMENTS ANALYSIS ===

### R2-02 (MAJOR graded Medium): AC-1.2 asks for a contract check on `load`, which gets no contract, and on commands with no `--output`
- origin=changed (the `spec:196` line is changed; the phrase "each P1 command" is inherited and depends on the changed AC-1.1 and `spec:76`).
- Expert: Wiegers (consistency), Crispin (acceptance criteria), Whittaker (Divergence Attack).
- Texts: `spec:196` (AC-1.2): "7.2 live check on each P1 command with `--unattended --output <dir>` (workflow: ... no `--output`; F-03) | all steps pass"; `spec:159` lists `load (usage line only)`, cleanup-audit and index-repo as P1 commands; `spec:112` and `spec:76`: load writes no report, gets no section, "use it as a step inside another worker's brief, not as its own Task"; `spec:85-86`: cleanup-audit output dir "is fixed", index-repo brief passes "none"; 7.2 steps 3 and 4 (`spec:182-183`) require a contract path and `test -s <contract>`.
- Concrete attack: **Divergence Attack.** The invariant at AC-1.2 (`spec:196`) fails when the P1 command is `load`. State trace: before, `/sc:load --unattended --output D` is started as a Task; after the worker ends, step 3 wants the WC-4 contract path for load (none exists, `spec:76`, `spec:112`) and step 4 `test -s` on it exits non-zero; "all steps pass" cannot hold, and `spec:167` says a phase passes only when every check passes. Only workflow was carved out; cleanup-audit and index-repo have no `--output` flag per `spec:85-86`.
- Why Medium: the same document says load is not run as its own Task (`spec:112`), so a reader can skip it; for cleanup-audit and index-repo the contract location is the prior Medium gap. The sentence needs a guess about which reading the implementer picks. Not blocking.
- Recommendation: add to AC-1.2 "except `load`" and a one-clause form for cleanup-audit and index-repo, the way workflow was handled. Priority: Medium. Quality impact: Consistency +0.5, Testability +0.5.

### R2-03 (MAJOR graded Medium): AC-1.1 and the P1 scope sentence cover 34 commands, but the phase table schedules 22 of them later
- origin=changed (`spec:195` and `spec:76` are changed); `spec:159` and the Phase column are unchanged text that the changed lines depend on.
- Expert: Wiegers (traceability), Crispin, Fowler.
- Texts: `spec:195` (AC-1.1): the test asserts the `## Unattended mode` section for "every command in sections 3.1-3.2 except `load`, `brainstorm` and `init-lite`" (37 - 3 = 34 commands); `spec:159` (P1 scope): "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)", but its Commands cell names only 12 commands that AC-1.1 covers (analyze, build, business-panel, design, document, explain, index, test; adversarial, cleanup-audit, index-repo, workflow); `spec:160-162` assign 15 commands to P2, 4 to P3, 3 to P4 (12 + 15 + 4 + 3 = 34); `spec:162` and `spec:154`: P4 waits for D2-D4; `spec:52`: the section "lists only its own gate resolutions".
- Concrete attack: **Sequence Attack.** The invariant at AC-1.1 fails when the P1 gate runs. State trace: P1 done as the Commands cell and the Phase column say, 12 commands have the section; the test finds none in the 22 commands scheduled P2-P4 (for example `implement.md` and `pr-submit.md`, whose gate rows wait for D2-D4); AC-1.1 fails. The other reading (P1 adds the section and flag to all 34, `spec:159` first clause) writes sections for commands whose gate resolution is not yet decided, contrary to the Phase column. Also `spec:159` "accepted by every command" includes `load`, `brainstorm` and `init-lite`, which `spec:76` says gain nothing.
- Why Medium: `spec:159`'s first clause is a stated reading under which AC-1.1 passes (a section carrying flag, contract path and "gate resolution added in its phase"); the text allows both readings. Not blocking.
- Recommendation: say whether P1 adds a stub section to every command or restrict AC-1.1 to the commands the Phase column assigns to P1 (and re-run per phase). One clause. Priority: Medium. Quality impact: Consistency +0.5.

### R2-05 (MAJOR graded Medium): AC-0.4 step 3 says "judged against the command's existing report file" but gives no rule for the expected outcome
- origin=changed (`spec:194`).
- Expert: Adzic (example), Crispin (acceptance criteria), Nygard.
- Texts: `spec:194` (AC-0.4): "in step 3 the `--outcome` and report path are judged against the command's existing report file"; `spec:63` (WC-5) maps `--outcome` from a report's `status`; `spec:91` and `INV-B:242`: troubleshoot's existing report is `REPORT.md`, a contract file only with `--caller task-unified`; `spec:92`, `INV-B:272`: workflow's own contract carries its own vocabulary (UNVERIFIED); `spec:83`, `INV-A:35`, `INV-A:60`: adversarial's contract name and place are "not fixed" and were seen in two locations.
- Concrete attack: **Divergence Attack.** The invariant at AC-0.4 step 3 fails when the existing report has no `status` key or when its location is not fixed. State trace: troubleshoot ends with a `REPORT.md` that records a failed diagnosis; the worker sends `--outcome succeeded`; the check cannot say whether that matches, because WC-5 maps from `status` and `REPORT.md` has none.
- Why Medium: the P0 reviewer is a person who can read `REPORT.md`; the failure is a missing rule, not a stated text that does harm. Not blocking.
- Recommendation: one clause: "the expected `--outcome` is what the report's own verdict says, read by the person recording the result; for adversarial the file is whichever `return-contract.yaml` the run wrote under `<dir>/adversarial/`". Priority: Medium. Quality impact: Testability +0.5.

=== ARCHITECTURE ANALYSIS ===

### R2-01 (MINOR graded Medium): WC-4 says "two commands" keep their own contract path, but the implement and pr-submit rows name other locations too
- origin=changed (`spec:62`, `spec:76`); the implement and pr-submit rows are unchanged text.
- Expert: Fowler (interface consistency), Wiegers, Whittaker (Divergence Attack).
- Texts: `spec:62` (WC-4): "two commands keep the path they already use, named in their section 3 rows"; `spec:76`: "unless a row below names another path (adversarial, workflow; F-03)"; `spec:109` (implement): "contract beside the ledger `progress.md`", ledger at `.dev/implement/<slug>/progress.md` (`INV-A:51`), which no coordinator directory chooses; `spec:114` (pr-submit): "contract beside `monitor-run-<PR>.jsonl`" (`INV-B:34`); `spec:105` (cli-portify): contract "file location unnamed"; `spec:182` (step 3): the report path is "the contract path WC-4 gives for that command"; `spec:210` (AC-4.3) agrees with the pr-submit row.
- Concrete attack: **Divergence Attack.** The invariant at WC-4 fails for implement: `<output-dir>` is "the directory the coordinator passed" but the implement row puts the contract where the ledger is, so "WC-4 gives" no single path, and the coordinator's `--report-path` target is not known before dispatch for it (`spec:73`).
- Why Medium: the general clause in `spec:76` already lets the rows win, the two commands sit in P4 behind D2-D4 (`spec:162`), and the count "two" is a wording error rather than a path the implementer would build wrongly. Not blocking.
- Recommendation: replace "two commands keep the path they already use" with "a command whose section 3 row names another path keeps it (adversarial, workflow, implement, pr-submit)". Priority: Low. Quality impact: Consistency +0.3.

### R2-04 (MAJOR graded Medium): "the worker passes the path it finds" for workflow has no method and breaks with two packages in one worktree
- origin=changed (`spec:62`, `spec:73`).
- Expert: Hohpe (message-then-pointer), Whittaker (Accumulation Attack), Cockburn.
- Texts: `spec:62` (WC-4): workflow's `<id>` "the command generates, so for workflow the worker passes the path it finds (F-03)"; `spec:69` (WC-11): two workers share one worktree by default; `spec:92`: workflow creates "Fresh package each run"; `INV-B:272`: contract at `.dev/tasks/to-do/<id>/return-contract.yaml`, "Never overwrites or reuses an existing package" (`INV-B:273`).
- Concrete attack: **Accumulation Attack.** The invariant at WC-4 fails when `.dev/tasks/to-do/` holds more than one package. State trace: before, workers A and B each run `/sc:workflow ... --handoff none` in one worktree; after, the directory holds `<idA>/` and `<idB>/`; A "finds" its path by listing the newest package after B finished and sends `worker_done --report-path .dev/tasks/to-do/<idB>/return-contract.yaml`; the coordinator reads B's `status` for A's Task (`spec:63`, `spec:182`).
- Why Medium: the text does not say the worker scans; if the command prints its package path the worker reads it. The sentence needs a guess about "finds". Not blocking.
- Recommendation: say the worker takes the path from the command's own final output (the id the command reports), not from a directory listing. Priority: Medium. Quality impact: Completeness +0.5.

## Minor notes (never fail the review)

- N2-01: `spec:73` says every brief carries "the exact command line including `--unattended`", while AC-0.4 (`spec:194`) lists the P0 command lines without it and P0 commands do not accept it before P1 (`spec:158`). Origin=unchanged; it depends on the changed AC-0.4 line. A reader will use the AC-0.4 command lines.
- N2-02: `spec:79` still reads "The only command changes are the small fixes in the last column", while the changed `spec:76` says a command that gets a contract also gains the section. `spec:79` itself says the contract arrives in Phase 1, so the pair is readable together. Origin=unchanged, depends on `spec:76`.
- N2-03: the revision writes finding ids (F-01, F-02, F-03) into normative spec text (`spec:52`, `62`, `73`, `76`, `182`, `194`, `195`, `196`). This follows the reviser rule ("each added paragraph or table cites its finding id", `command.md:263`) and ties the spec to `review/round1.md`; a later pass may strip them. Not a defect of the revision.
- N2-04: `spec:196` (AC-1.2) uses `--output <dir>` for "each P1 command"; for `explain` the report goes to a file the command must first gain a flag for (`spec:108`), so P1 must add the flag before the check. Origin=unchanged; inferable.

## Follow-up candidates (Medium and minor, no revision, no effect on the verdict)

R2-01, R2-02, R2-03, R2-04, R2-05, and notes N2-01 to N2-04. The Medium and minor findings and notes of the prior report remain on the prior report's follow-up list and are untouched by this review.

Issue question: the command asks the user once per loop whether to open an issue for these. This worker's final reply is restricted to the output path, so the question is left to the coordinator or user; no issue was created and none was asked.

## Quality scores (0-10), scoped to the changed lines and prior blockers

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 8 | Added clauses are short and cite their ids; the "known before dispatch" title of WC-4 still reads absolute (`spec:62`) but is qualified in the body |
| Completeness | 7 | Workflow path discovery and the implement/pr-submit locations are under-specified (R2-01, R2-04) |
| Testability | 7 | P0 check is now passable (`spec:194`); AC-1.1 and AC-1.2 quantifiers disagree with the phase table (R2-02, R2-03) |
| Consistency | 7 | The three prior contradictions are gone (F-01, F-02, F-03 resolved); residual family members are Medium |

Coverage line: scoped PASS: changed lines + prior blockers. This is not whole-document assurance; a whole-document check needs a separate, labelled first review whose blockers are escalated and never start a fourth review.

## Reviser brief

Blocking finding ids: none. No revision is requested; the prior blocking findings F-01, F-02 and F-03 are resolved and no new blocking finding is open. (Contract restated for any later reviser: revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report bytes before and after and the bytes added and deleted per finding id; leave Medium and minor findings alone.)

verdict: PASS
