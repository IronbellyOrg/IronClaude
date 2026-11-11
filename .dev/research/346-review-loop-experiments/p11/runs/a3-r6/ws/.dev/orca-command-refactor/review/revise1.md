# Revise 1: Orca worker-contract spec

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:49-51`. Citation keys: `spec:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` after this revision (no line was added or removed, so the numbers equal the baseline's). `r1:N` = line N of `.dev/orca-command-refactor/review/round1.md`. `v1:N` = line N of the baseline `specs/history/spec-v1.md` (byte-identical to the candidate before the edit, checked with `cmp`).

Scope: only the blocking ids in `r1:208-212` (REQ-1, REQ-2, ARCH-1). Medium and minor items (M-1 to M-10, N-1 to N-5) were left alone. Edited file: the spec only. No spec-panel was run. No PASS is claimed.

## Byte accounting

| Item | Value |
|---|---|
| Candidate size before | 57763 bytes (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches `r1:8-9`) |
| Candidate size after | 59765 bytes (285 lines), sha256 `cf9b3e748906ea7675896ba4ee5a7993c98b0ab7a8ec22a0e9311df04e7ebb69` |
| Net | +2002 bytes (2318 added, 316 deleted) |

Per finding id (measured with a word-level diff of the baseline against the revised file, split by which finding each inserted clause cites; where one edit serves two findings it is split by clause):

| Finding | Bytes added | Bytes deleted |
|---|---|---|
| REQ-1 | 1267 | 219 |
| REQ-2 | 678 | 87 |
| ARCH-1 | 373 | 10 |
| Total | 2318 | 316 |

Every added clause carries its finding id in the text.

## Disposition per finding

| Id | Disposition | Where applied | What changed | Why this and not more |
|---|---|---|---|---|
| REQ-1 | Applied | `spec:62` (WC-4), `spec:76`, `spec:92`, `spec:149` (SA-4), `spec:182`, `spec:198` (AC-1.4), plus `spec:73` for the file-valued case | WC-4 now gives the contract path for every case the finding named: a file-valued `--output` (tdd, init-lite, spec-panel: `<file>.return-contract.yaml`, a sibling, so two files in one folder do not collide), adversarial (`<output>/adversarial/return-contract.yaml`, the path already in `spec:83`), cleanup-audit (`.claude-audit/return-contract.yaml`, the fixed directory in `spec:85`), workflow (`.dev/tasks/to-do/<id>/return-contract.yaml`, reported by the worker because `<id>` is unknown before the run, `INV-B:272`). With no output path the command refuses in chat, writes no file, and WC-5 already maps "no report" to `--outcome failed` (`spec:63`). Section 3 intro (`spec:76`) and live-check step 3 (`spec:182`) now say "the path WC-4 gives for that command". | The workflow pre-creation STOP has no directory, so I narrowed rather than invented one: the "write the contract for pre-creation STOPs" small fix at `spec:92` became "None ... writes no contract and ends `failed`", and its dependents were deleted (", workflow" from the P1 command list at `spec:159`; "and workflow" at `spec:149`; the workflow clause of AC-1.4 at `spec:198`). The finding's recommendation allowed "a chat-only refusal" as the default (`r1:99`). |
| REQ-2 | Applied | `spec:76`, `spec:73`, `spec:159`, `spec:195`, `spec:196` | The "every changed command gains `## Unattended mode`" sentence (`spec:76`) is now per phase: 3.2 commands gain it in their own row's phase except load; of the 3.1 commands only reflect, release-split, tdd and troubleshoot (their P2 fixes add gate resolutions) gain it; adversarial, brainstorm, cleanup-audit, index-repo, init-lite and workflow gain none. P1 scope (`spec:159`) is now the eight P1 commands of 3.2 (analyze, build, business-panel, design, document, explain, index, test); load gets the usage line only, adversarial, cleanup-audit and index-repo get their fixes only. AC-1.1 (`spec:195`) asserts the section on exactly those eight; AC-1.2 (`spec:196`) points at them. The brief template (`spec:73`) no longer requires `--unattended` for the 3.1 commands that have no section. | Chose the finding's first recommended option (scope AC-1.1 to the P1 rows, with load and the "None" rows exempt; `r1:115`) over deleting the clause. The `spec:73` parenthetical is the one dependent addition: without it the brief template would still tell the coordinator to pass a flag that brainstorm, init-lite and similar commands do not take. The M-4 point (using `--unattended` before a command's phase, `r1:113`, `r1:161`) is a Medium item and was not touched. |
| ARCH-1 | Applied | `spec:64` (WC-6), `spec:73` (2.3), `spec:62` ("for this dispatch"), `spec:200` (AC-2.2) | WC-6's "fresh output directory" now means "the output directory the coordinator passed for that dispatch, never one an earlier dispatch used". Section 2.3 requires a distinct output directory (or file) per dispatch, a `--retry-of` retry included, so the coordinator reads the contract at the path it passed to that dispatch. WC-4 says "for this dispatch". AC-2.2 gains one retry case: a `worker-start --retry-of` retry with a new `<output-dir>` writes its contract there and leaves the first contract unchanged. | Followed the finding's own recommendation (`r1:132`): one sentence in 2.3, a rewording of WC-6, one retry case in AC-2.2. The "Fresh dir" cells in the section 3 rows (for example `spec:88-91`) are consistent with the new reading and were not edited. The two real exceptions to "distinct per dispatch" are stated in 2.3: cleanup-audit (fixed directory; its retry resumes from `progress.json`, `spec:85`, and rewrites the contract) and workflow (a new package and `<id>` each run, `spec:92`). |

## Residual risks the reviewer may check (not fixed, outside the blocking ids)

- A command whose row names a contract but no output flag (for example research at `spec:116`, recommend at `spec:115`) now falls under the WC-4 no-path refusal until a P-phase row adds an output flag. The rows that say "add an output path" already cover most cases; I did not widen any row (rule: add nothing a blocking finding does not call for). If the reviewer grades this as a new blocking defect it needs a decision on those rows.
- cleanup-audit's contract at `.claude-audit/return-contract.yaml` is a path I chose from the fixed directory in `spec:85` and `INV-A:42`; the inventory does not name a contract file there (UNVERIFIED which filename the skill would use).
- Citations to files outside the sandbox (`src/`, `CLAUDE.md`, `EVIDENCE.md`) were not re-read; I added none. Only `spec:`, `r1:`, `INV-A:42`, `INV-B:272` and the prompts file were checked here.
