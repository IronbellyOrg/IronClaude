# Revise 2: orca-worker-contract-spec.md

Prompt: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy).
Input review: `.dev/orca-command-refactor/review/round2.md` (header `review: 2 of 3`, `verdict: FAIL`; Reviser brief at `round2.md:151-155`).
Confirmed ids (VERIFY step VF2, `round2.md:2`): R2-1, R2-2. Out of scope and not touched: F-1 to F-9, the noted M-ids, and round-1 notes.
Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Verdict: not awarded here (the REVISE prompt does not award a PASS). The next step is a re-review (review 3 of 3).

## Byte accounting

Measured on the candidate before and after this revision, with a byte count of the whole file.

| | Bytes | sha256 |
|---|---|---|
| Before (round-2 candidate) | 59705 | `e28114855e5685eb7f3f2e2652a756ffaac57ed4c9ffb0b7423b91d78a8e8d19` (matches `round2.md:8`) |
| After (this revision) | 60552 | `530bb94dc36fffb71a0dd0f59ecf0aa60e32ab1c485bde6cfedea040d97adda7` |
| Net | +847 | 294 lines before and after; six lines changed, no line added or removed |

Per finding id (bytes deleted and added, per changed spec line):

| Finding | Spec line | Deleted | Added | Net |
|---|---|---|---|---|
| R2-1 | `:189` (step 3) | 0 | 103 | +103 |
| R2-1 | `:201` (AC-0.4) | 87 | 485 | +398 |
| R2-1 total | | 87 | 588 | +501 |
| R2-2 | `:62` (WC-4) | 0 | 110 | +110 |
| R2-2 | `:87` (init-lite row) | 0 | 77 | +77 |
| R2-2 | `:90` (tdd row) | 0 | 77 | +77 |
| R2-2 | `:208` (AC-2.2) | 0 | 82 | +82 |
| R2-2 total | | 0 | 346 | +346 |
| Sum | | 87 | 934 | +847 (equals 60552 - 59705) |

The `:201` figures are the old sentence (87 bytes, `steps 1-3 and 5-7 pass, where step 3's report path is the one the command writes today.`) replaced by a 485-byte sentence.

## Findings

| Id | Status | Where applied | Reason and evidence |
|---|---|---|---|
| R2-1 | applied | `specs/orca-worker-contract-spec.md:201` (AC-0.4) and `:189` (step 3 of 7.2) | Round-2 defect: step 3 requires the `--outcome` to match the contract's `status` and the report path to be the WC-4 contract path, and no contract exists in P0 for `troubleshoot` (report `REPORT.md`, `:91`; `INV-B:242`) or `adversarial` (no filename or field list, `INV-A:35`). AC-0.4 now states the P0 rule. `workflow` keeps the WC-5 check on `status`, because it already writes `.dev/tasks/to-do/<id>/return-contract.yaml` with `status` (`INV-B:272`). For `troubleshoot` and `adversarial`, `--outcome succeeded` is sent exactly when the file step 4 checks is non-empty, and `failed` otherwise. That follows WC-5's "no report exists" branch (`:63`). Step 3 gets a one-sentence pointer to AC-0.4. |
| R2-2 | applied | `specs/orca-worker-contract-spec.md:62` (WC-4), `:87` (init-lite row), `:90` (tdd row), `:208` (AC-2.2) | Round-2 defect: WC-4 defines `<output-dir>` as a directory (`:62`), but the tdd and init-lite rows name `--output <file>` (`:87`, `:90`). The fix follows the reviewer's second option, which names the contract location in the rows as M10 did for three other rows. For tdd and init-lite, the contract is `return-contract.yaml` in the directory containing the `--output` file. WC-4 now says so. AC-2.2 defines `<contract>` for the tdd gate run. The tdd file-valued claim is supported by `inventory/commands-b.md:47` ("TDD file at `--output`") and `:222`. |

## Decisions

- **R2-2, init-lite file-valued claim is UNVERIFIED.** The spec row says `--output <file>` (`:87`), citing `cmd/init-lite.md:32`, which is not in this sandbox. `inventory/commands-a.md:55` says only "`--output`" with no type, citing C:32 and S:70. I applied the file reading because the reviewer and the spec both state it. If `src/superclaude/commands/init-lite.md:32` names a directory, the init-lite text added here is wrong and must be reversed by the next reviser. Marked UNVERIFIED.
- **R2-2, option chosen.** I named the contract location in the rows (reviewer's second option) rather than adding a new directory flag to tdd and init-lite. A new flag would add a mechanism that no blocking finding calls for, which the REVISE brief forbids.
- **R2-1, workflow and the other two commands treated separately.** The rule is kept deterministic and needs no field the inventory does not name.

## Coverage and self-check

- Changed lines were compared with `diff` against the pre-revision copy: exactly six lines differ (`:62`, `:87`, `:90`, `:189`, `:201`, `:208`). No other line changed.
- Citations added: `inventory/commands-a.md:35` (adversarial row, "the skill names no filename", and the contract rule), `inventory/commands-b.md:272` (workflow contract with `status`), `inventory/commands-b.md:47` and `:222` (tdd `--output` is the TDD file), `inventory/commands-a.md:55` (init-lite `--output`, no type), `inventory/commands-b.md:242` (troubleshoot `report_path` = `REPORT.md`), and the spec's troubleshoot row at `specs/orca-worker-contract-spec.md:91`. The repo files `src/superclaude/commands/init-lite.md:32` and `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` are not in this sandbox and are cited only as the spec already cited them: UNVERIFIED.
- Not checked: anything under `src/`, `plugins/`, `.claude/` or the Orca guides (UNVERIFIED).
- No PASS is awarded. The next review is 3 of 3, and the REVISE brief's rules were followed: only the blocking text, no new rule or section, a finding id cited on every addition.
