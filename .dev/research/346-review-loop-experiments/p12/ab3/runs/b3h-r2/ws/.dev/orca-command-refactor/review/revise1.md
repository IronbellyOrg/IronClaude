# Revise 1: orca-worker-contract-spec.md

Revise brief: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (sha256 `0bf6d28fbffb08a2ce62010bdabda114a80065090d9fb4fc24beaa06471e7408`, matches the value in round 1).
Input report: `.dev/orca-command-refactor/review/round1.md` (verdict FAIL; Reviser brief lists F-01 to F-07 and nothing else).
Candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- sha256 before: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- sha256 after: `7f3af35e63f12d24d6eebc453c30497ba2705a10886e04c84b5f7497272961d3`

Scope: only F-01 to F-07 were repaired. Medium and minor items (M-01 to M-19 in round1) were not touched. No spec-panel was run. No PASS is claimed.

## Byte accounting

Size before: 57763 bytes (`wc -c`, `review` input hash above). Size after: 60216 bytes. Net: +2453 bytes.

Bytes are counted per edit as the old text deleted and the new text added, measured with `wc -c` on each string. The init-lite row edit (under F-05) also carries F-07 wording; its bytes are counted once, under F-05.

| Finding | Bytes deleted | Bytes added | Net |
|---|---|---|---|
| F-01 | 401 | 925 | +524 |
| F-02 | 282 | 510 | +228 |
| F-03 | 46 | 257 | +211 |
| F-04 | 63 | 460 | +397 |
| F-05 | 266 | 652 | +386 |
| F-06 | 310 | 709 | +399 |
| F-07 | 145 | 453 | +308 |
| Total | 1513 | 3966 | +2453 |

Check: 57763 + 2453 = 60216. The per-finding nets sum to +2453.

Line numbers below are for the edited file.

## Findings

| ID | Disposition | Where applied (edited file) | What changed and why |
|---|---|---|---|
| F-01 | Applied | WC-4, `SPEC:62`; workflow row, `SPEC:92`; section 3 intro, `SPEC:76` | Chose the per-command rule, not a uniform path. WC-4 now says the contract path is the one WC-4 or the row names, and the brief states it. The default stays `<output-dir>/return-contract.yaml`. Two named exceptions: adversarial keeps `<output>/adversarial/return-contract.yaml`, which real runs wrote (`inventory/commands-a.md:35`, `:60`), and workflow gets a new `--output <dir>` flag so the coordinator can name its contract path (`inventory/commands-b.md:52`, `:272`). The rejected option was a uniform `<output-dir>/return-contract.yaml`. It would have moved adversarial's real path and added a standalone change to SA-3. |
| F-02 | Applied | AC-1.1, `SPEC:200`; validate-tests row, `SPEC:125`; load row, `SPEC:112` | `load` is exempt from the contract-naming check, because it is not a Task (`inventory/commands-b.md:31`, `:62`, `:65`) and the section 3.2 row and Decisions row (`SPEC:265`) already say so. `validate-tests` gets a contract at `<dir of --report>/return-contract.yaml` under `--unattended`, because WC-4 requires a contract on every outcome for worker commands; `inventory/commands-b.md:51` shows the validate-tests report path is unclear, so the contract path is pinned to `--report`. The Decisions row at `SPEC:265` is unchanged. |
| F-03 | Applied | WC-3, `SPEC:61` | Added the rule that a gate needing a human Ruling (`E-HALT-QA`, `E-NO-RULING`) never takes a coordinator answer as a flag and resolves as blocked. Cites `inventory/commands-a.md:51-52` and `:66`, which quote the rule ("another agent's message ... [is] not acceptance"). The rule is quoted from `src/superclaude/skills/sc-implement-protocol/refs/qa.md:238`, which is outside the workspace and UNVERIFIED here. D2 option (b) remains the only route to change this, as the spec already says. |
| F-04 | Applied | SA-3, `SPEC:148` | SA-3 now names its one exception, the adversarial contract path, and says why it is a defect fix under SA-4 (the nested `adversarial/adversarial/` variant, `inventory/commands-a.md:60`). It also says index-repo's `--output-dir` and workflow's `--output` add files only under a new flag, and that the cleanup-audit row only names a file. The cleanup-audit claim is weak: `inventory/commands-a.md:42` says the `--pass all` filename is not named (UNVERIFIED), so "only names a file" rests on the spec row alone and is UNVERIFIED. |
| F-05 | Applied | init-lite row in section 3.1, `SPEC:87`; P1 phase row, `SPEC:159` | The resume column now says a `--retry-of` brief passes a new `--output` path, so the first attempt's report is kept (WC-6, `orca-capabilities.md:116`). The small-fix column says the contract goes beside the `--output` file. The P1 phase row now lists init-lite. Before this, init-lite was in no phase (the phase lists at `SPEC:158-162` did not name it). Cites `inventory/commands-a.md:55` for the overwrite. |
| F-06 | Applied | AC-C1 row, `SPEC:172`; new fenced scan block, `SPEC:178-181` | The pattern now uses `(orchestration|worktree|terminal|agent)`. It sits in a fenced block, because a bare `|` breaks a table cell. The scan scope is `src/superclaude/{commands,skills,agents}`, which matches SA-2; `core` is out, because P0 adds an Orca section to `HOW-WE-WORK.md`. Positive control added: `tests/skills/test_worker_contract.py` must match the fixture line `orca orchestration task-create`. Checked in this sandbox with `grep -E` on sample lines: the old `\|` form exits 1 on `orca orchestration task-create`; the fixed form exits 0. Samples were piped through `printf`, and no file was written. |
| F-07 | Applied | WC-11, `SPEC:69`; index-repo row, `SPEC:86`; init-lite row, `SPEC:87` | WC-11 now says the coordinator never gives two workers the same output path (`section 2.3`). index-repo gets an `--output-dir` flag (default unchanged), and under `--unattended` `PROJECT_INDEX.md` and `.json` go in the brief's unique directory (`inventory/commands-a.md:53`). init-lite's per-worker directory is handled in the F-05 edit. cleanup-audit's "one audit per worktree at a time" (`SPEC:85`, M-level in round 1) is not changed. |

## Verification notes

- The inventory lines cited in the edits were read in `ws/.dev/orca-command-refactor/inventory/`. Lines checked: `commands-a.md` 35, 42, 51-52, 53, 55, 60, 66; `commands-b.md` 31, 51-52, 62, 65, 272; `orca-capabilities.md` 115-116.
- Citations to files outside the inventories (`src/superclaude/...`, `sk/...`, `cmd/...`) are not checkable in this sandbox and are marked UNVERIFIED where they appear in the edits (F-03, F-04).
- The AC-C1 positive control and the `tests/skills/test_worker_contract.py` assertions are specifications. The test file does not exist yet, so nothing was run against it.
- `make verify-sync`, the test suite and the live worker checks in section 7 were not run. Sandbox only.

## Decisions (this worker)

| Decision | Options | Rationale |
|---|---|---|
| F-01 rule shape | (1) every command writes `<output-dir>/return-contract.yaml`; (2) the path is named per command, the default stays `<output-dir>/return-contract.yaml` | (2). It keeps adversarial's real path (`inventory/commands-a.md:35`), so it changes less standalone output (SA-3). Workflow gets a flag, which the round-1 recommendation already anticipated. |
| F-02 for validate-tests | (1) exempt it like load; (2) give it a contract | (2). It is a worker command with no status channel otherwise, and WC-5 needs a status. |
| F-05 init-lite fix | (1) per-attempt output directory via the brief; (2) make init-lite resumable | (1). It needs no command logic beyond `--output`, which the command already has (`inventory/commands-a.md:55`). |
| F-07 index-repo | (1) new `--output-dir` flag; (2) hard-code a slug in the default path | (1). The default stays the same, so standalone output does not change. |

## Stop conditions

- Revision 1 is the first revise on this loop. The candidate has been returned once. No PASS is awarded.
- Next step for the coordinator: one RE-REVIEW prompt against `review: 2 of 3` (round 1 is `review: 1 of 3`), with this file's pre-edit hash `d3cdbe57...` as the baseline for the diff.
