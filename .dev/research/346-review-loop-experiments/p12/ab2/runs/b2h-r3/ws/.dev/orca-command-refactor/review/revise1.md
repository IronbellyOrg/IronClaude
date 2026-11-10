# Revise 1: orca-worker-contract-spec.md

Input review: `.dev/orca-command-refactor/review/round1.md` (review 1 of 3, verdict FAIL). Its VF1 step confirmed F-02, F-03, F-04, F-05 and rejected F-01 (kept as noted, unactioned).
Revised ids (IDS): F-02, F-03, F-04, F-05. Medium and minor findings (F-06 to F-25) were not touched.

Candidate before revision: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`, 57763 bytes, 285 lines.
Candidate after revision: same path, sha256 `bfe20373dae030b64d0ab846cde01958172f4f46786bcfbad746ac335c6b4df6`, 59081 bytes, 285 lines (no line added or removed; the line numbers cited below are the same before and after).

Citation scope: `SPEC:n` = the revised spec, line n. `INV-A:n` = `inventory/commands-a.md` line n. `INV-B:n` = `inventory/commands-b.md` line n. I read each cited inventory line before citing it. Citations to repo files outside the workspace (`src/superclaude/...`, `~/.claude/...`) are not used in this revision.

## Byte accounting

Size: 57763 bytes before, 59081 bytes after, net +1318 bytes.

Accounting method: each edit is one replacement in the spec. "Added" is the new bytes it writes, "deleted" is the old bytes it removes (for the pure insertions, deleted is 0). Net = added minus deleted.

| # | Location (SPEC line) | Finding id(s) | Added | Deleted | Net |
|---|---|---|---|---|---|
| E1 | WC-4 (`SPEC:62`), inserted sentences | F-02 | 293 | 0 | +293 |
| E2 | WC-5 outcome clause (`SPEC:63`), `;` replaced by a clause | F-05 | 131 | 1 | +130 |
| E3 | WC-5 parse-check sentence (`SPEC:63`) | F-05 | 149 | 0 | +149 |
| E4 | WC-11 (`SPEC:69`), inserted sentence | F-03 | 303 | 0 | +303 |
| E5 | index-repo row (`SPEC:86`), brief cell and fix cell | F-03 | 91 | 34 | +57 |
| E6 | cleanup-audit row (`SPEC:85`), fix cell | F-03 | 131 | 57 | +74 |
| E7 | init-lite row (`SPEC:87`), resume cell (F-03) and fix cell (F-02, F-04) | F-03 (resume cell, 118 added, 35 deleted); F-02, F-04 (fix cell, 72 added, 4 deleted) | 190 | 39 | +151 |
| E8 | workflow row (`SPEC:92`), fix cell | F-02 | 96 | 0 | +96 |
| E9 | P1 scope cell (`SPEC:159`) | F-04 | 28 | 0 | +28 |
| E10 | AC-1.1 (`SPEC:195`) | F-04 | 37 | 0 | +37 |
| | Total | | 1449 | 131 | +1318 |

Per finding id (the init-lite row E7 is split between F-03 and F-02/F-04 as shown above; the 72 added and 4 deleted in its fix cell are counted under both F-02 and F-04 and appear once in the total):

| Finding | Added | Deleted | Net |
|---|---|---|---|
| F-02 | 461 (293 + 96 + 72 shared) | 4 (shared fix cell) | +457 |
| F-03 | 643 (303 + 91 + 131 + 118) | 126 (34 + 57 + 35) | +517 |
| F-04 | 137 (28 + 37 + 72 shared) | 4 (shared fix cell) | +133 |
| F-05 | 280 (131 + 149) | 1 | +279 |
| Total without double counting | 1449 | 131 | +1318 |

## Applied findings

| Finding | Applied where | Change | Citation |
|---|---|---|---|
| F-02 (contract path, Fowler) | WC-4 (`SPEC:62`) | Rule added: a file-valued output (`--output <file>`) uses the file's parent directory as `<output-dir>`. Workflow's `<id>` is created at run time, so the brief passes it by a flag the P1 plan names. | `SPEC:62`; `INV-B:47` (tdd `--output` is a file); `INV-A:55` (init-lite `--output`); `INV-B:52` and `INV-B:273` (workflow `<id>` under `.dev/tasks/to-do/`, never reused) |
| F-02 | Section 3.1 workflow row (`SPEC:92`) | Brief passes `<id>` by the P1 flag, so the path is known before dispatch. | `SPEC:92`; `INV-B:52`, `INV-B:273` |
| F-03 (fixed default outputs, Nygard) | WC-11 (`SPEC:69`) | Rule added: under `--unattended`, each fixed default output (index-repo `PROJECT_INDEX.md`, init-lite `.dev/superclaude/context-audit.md`, cleanup-audit `.claude-audit/`) is written under the `<output-dir>` the brief passes. | `SPEC:69`; `INV-A:53`; `INV-A:55`; `INV-A:107` |
| F-03 | Section 3.1 index-repo row (`SPEC:86`) | Brief passes `<output-dir>`; the write goes to `<output-dir>/PROJECT_INDEX.md` under `--unattended`. | `SPEC:86`; `INV-A:53` |
| F-03 | Section 3.1 cleanup-audit row (`SPEC:85`) | Under `--unattended` the output dir comes from the brief instead of the fixed `.claude-audit/`. The old "one audit per worktree at a time" sentence is removed, because the per-run directory replaces it. | `SPEC:85`; `INV-A:107` |
| F-03 | Section 3.1 init-lite row (`SPEC:87`), resume cell | A fresh `--output` per attempt under `--unattended` (WC-6), so a retry does not overwrite the first attempt's report. Standalone re-run behavior is unchanged. | `SPEC:87`; `INV-A:55` ("a marked report is overwritten on re-run") |
| F-04 (AC-1.1 unmeetable, Wiegers) | AC-1.1 (`SPEC:195`) | `load` is excluded from the check: it writes no report file (`SPEC:112`). | `SPEC:195`; `SPEC:112` |
| F-04 | Phase P1 scope cell (`SPEC:159`) and init-lite row fix cell (`SPEC:87`) | init-lite gets a contract at `<parent of --output>/return-contract.yaml` in P1, so AC-1.1 can pass for it. | `SPEC:87`, `SPEC:159`; `SPEC:195` |
| F-05 (zero-byte contract maps to succeeded, Whittaker) | WC-5 (`SPEC:63`) | A contract that exists but does not parse with one of the four `status` values is `failed`. The worker runs the section 7.2 step 4 parse check before `worker_done`, not after. | `SPEC:63`; `SPEC:183` (7.2 step 4) |

## Rejected findings

None of the four confirmed ids was rejected.

F-01 was rejected by the verifier in VF1 (`review/round1.md`, line 2). It is not revised here, and the review loop lists it as noted, unactioned.

## Open items for the next review

1. F-02: the spec says the workflow brief passes `<id>` "by the flag the P1 plan names". That flag does not exist yet and the spec does not name it. The next review may flag this as an undefined mechanism. This revision did not add a name, because no inventory line names one.
2. F-02: the `<id>` is inferred to be created at run time from `INV-B:52` and `INV-B:273` ("Fresh package each run", "never overwrites or reuses"). The inventories do not state the id-generation step, so this inference is marked UNVERIFIED here.
3. F-02: the rule places the contract for a file-valued output (tdd, init-lite) in the file's parent directory, which can be a docs folder. The directory choice is a design decision, not checked against any inventory line.
4. F-03: the cleanup-audit fix relies on the brief passing a distinct directory per worker. The cleanup-audit SKILL.md was not re-read in this revision; the claim rests on `INV-A:107`.

## Coverage

Read in full: the candidate, the review report `review/round1.md`, the README, the REVISE prompt in `home/.claude/rules/prompts/document_review_loop_prompts.md`, and the inventory lines cited above. Not read: `review/findings-1.md`, `review/verify-1.md` (outside the brief's inputs; VF1 confirmation was taken from `review/round1.md` line 2), and the repo files outside the workspace. No spec-panel was run, and no other file was edited.
