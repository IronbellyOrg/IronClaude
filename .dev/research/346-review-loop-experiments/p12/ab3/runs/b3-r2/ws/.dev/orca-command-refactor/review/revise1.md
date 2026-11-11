# Revise report, round 1: orca-worker-contract-spec

- prompt followed: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:53-55` (read in full)
- candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- ids repaired: B-1, B-2, B-3 (the Reviser brief of `.dev/orca-command-refactor/review/round1.md:288-292`). Medium (M-1 to M-11) and minor (N-1 to N-7) findings were left alone.
- no PASS is claimed; the revised candidate goes to the next review.
- citation legend: `SPEC:N` = candidate line N (line numbers are the same before and after: 285 lines both times, all edits are inside existing lines); `R1:N` = `review/round1.md` line N; `INV-A:N`, `INV-B:N` = the inventories.

## Byte accounting

Method: the candidate before the edits was byte-identical to `specs/history/spec-v1.md` (`cmp` printed nothing) with sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (the hash in `R1:7`). Each edit was an exact one-time string replacement; added and deleted bytes per edit come from a character-level diff of the old and new strings, summed per id (UTF-8 bytes). The totals reconcile with `wc -c`.

| | bytes |
|---|---|
| size before | 57763 |
| size after | 59339 (sha256 `523f1629dc21eaacc3987537a70cf3e5944edf741f8b5368cdaad6f32cf68d9c`) |
| net | +1576 |

| finding id | edits | bytes added | bytes deleted | net |
|---|---|---|---|---|
| B-1 | 7 | 358 | 24 | +334 |
| B-2 | 8 | 926 | 5 | +921 |
| B-3 | 3 | 333 | 12 | +321 |
| total | 18 | 1617 | 41 | +1576 |

No new section, no new table and no new paragraph was added: every addition is a clause inside an existing line, so the id is cited per edit below instead of in the spec text.

## One row per finding id

### B-1: applied (SPEC:76, 84, 87, 159, 195, 196)

Defect (R1:65-90): AC-1.1 asserted the `## Unattended mode` section in all 37 commands of sections 3.1-3.2 at the end of Phase 1, but load, pr-submit, brainstorm and init-lite could not satisfy it, and the SPEC:154 gate then stopped Phase 2.

Applied, narrowing the check and placing the two unplaced commands (no mechanism added):

1. SPEC:195 (AC-1.1): the test now covers "every command listed in the P1 row of section 6, except `load` (no contract to name)". pr-submit is P4 and is not in the P1 row, so it is out of the check without waiting on D3 (the SPEC:240 option (a) no longer conflicts).
2. SPEC:159 (P1 row, two edits): "accepted by every command in sections 3.1 and 3.2" became "accepted by every command listed in this row", which removes the disagreement with the row's own command list that R1:76 names. brainstorm and init-lite were added to the P1 command list "(the section only)", and `load` is marked "(usage line only; no `## Unattended mode` section)".
3. SPEC:84 and SPEC:87 (brainstorm and init-lite "Small fix" cells): "None" became "None; gains the `## Unattended mode` section (P1)", so the 10 ready commands of section 3.1 all have a phase (adversarial, brainstorm, cleanup-audit, index-repo, init-lite, workflow in P1; reflect, release-split, tdd, troubleshoot in P2, SPEC:160).
4. SPEC:76: "Every changed command also gains" became "Every changed command except `load` (it has no report file, so no contract to name) also gains", because load's row says "Report: none" (SPEC:112) and the old sentence made load's section impossible.
5. SPEC:196 (AC-1.2): "each P1 command" became "each P1 command except `load`, with `--unattended` and, where its section 3 row takes one, `--output <dir>`". Same root defect as AC-1.1 (load has no contract for 7.2 step 4 to open, SPEC:183), and without it Phase 1 still could not pass. Counted under B-1 because it is the same finding in the neighbouring check.

Not done: I did not give pr-submit or the P2-P4 commands the section in Phase 1, and I did not change SPEC:154.

### B-2: applied (SPEC:62, 73, 76, 83, 85, 86, 92, 182)

Defect (R1:130-140): WC-4 put the contract at `<output-dir>/return-contract.yaml`, while adversarial (`<output>/adversarial/...`), workflow (`.dev/tasks/to-do/<id>/...`, run-time id), the file-valued `--output` commands and the fixed-location commands cannot satisfy it, and the live check required the report path to equal the WC-4 path.

Applied (R1:140 recommendation: WC-4 default plus a named exception per differing row, one rule for file-valued `--output`; no column added, the exception sits in the existing "Small fix" cell):

1. SPEC:62 (WC-4): the default path now holds "unless the command's section 3 row names another contract path". One rule for file-valued `--output` (init-lite, tdd, the new spec-panel flag): the contract is written beside the file as `<file name>.return-contract.yaml`. The "known before dispatch" claim now has one stated exception, workflow. The one-name decision (`return-contract.yaml`, SPEC:261) is kept as a suffix.
2. SPEC:76: "Contract" means the WC-4 file "or the contract path the row names".
3. SPEC:83 adversarial: the contract path `<output>/adversarial/return-contract.yaml` is named as a WC-4 exception.
4. SPEC:85 cleanup-audit: contract path `.claude-audit/return-contract.yaml` (the fixed output directory SPEC:85 already states; `INV-A:42` shows the `.claude-audit/` location).
5. SPEC:86 index-repo: contract path `PROJECT_INDEX.md.return-contract.yaml` beside the fixed `PROJECT_INDEX.md` (the file rule of item 1; the location of `PROJECT_INDEX.md` itself is implied, UNVERIFIED at `INV-A:53`).
6. SPEC:92 workflow: the path has a run-time `<id>` (`INV-B:272`), so the worker names it in `worker_done` and the coordinator cannot know it before dispatch. Two facts stay UNVERIFIED and are marked so in the row: whether the command prints the package path, and where a pre-creation STOP writes its contract (no `<id>` exists then; `INV-B:272` says the file is not written for pre-creation STOPs and the P1 fix asks for one).
7. SPEC:73 (section 2.3): "the output directory" became "the output directory (or output file)", and the "known before dispatch" clause names workflow as the exception.
8. SPEC:182 (live check step 3): "the WC-4 contract path" became "the contract path WC-4 or the command's section 3 row gives".

Size note: this id is the largest addition (+921). The finding asks for several rows to name a path, so the text could not be a pure deletion; it is clauses only, no new table.

Left alone: the pre-creation STOP location of workflow is not decided here (it is not named by B-2 and no inventory line fixes it); it is recorded as UNVERIFIED in the row.

### B-3: applied (SPEC:64, 73, 205)

Defect (R1:142-150): WC-6 said a retry must not corrupt the first attempt's output and offered "a fresh output directory", while AC-3.2 had the command start fresh inside the same `<dir>` that holds attempt 1's `.session-memory.md`, and nothing told the coordinator to pass a new directory.

Applied (R1:150 recommendation: one sentence in section 2.3, AC-3.2 on a new directory):

1. SPEC:73 (section 2.3): the brief now states, for a `--retry-of` retry, either the command's resume flag with the first attempt's directory or, for a command with no resume flag, a new output directory, never the first attempt's (WC-6). Wording follows WC-6, which already says "resumes ... or ... fresh output directory" (SPEC:64), so a resumable command is not forced to move.
2. SPEC:64 (WC-6): "a fresh output directory" became "a fresh output directory that the coordinator passes (section 2.3)", which answers who makes the 22 "fresh dir" rows fresh (R1:146).
3. SPEC:205 (AC-3.2): the run uses `--output <dir2>`, where `<dir2>` is a copy of an earlier run's `<dir>` holding `.session-memory.md`, with no resume flag; pass condition adds that `<dir>` is not touched. This keeps the test of the removed `[Y/n]` prompt (the roadmap row at SPEC:118) and no longer overwrites a first attempt.

## Checks run after the edit

- `diff history/spec-v1.md orca-worker-contract-spec.md` changes only lines 62, 64, 73, 76, 83-87, 92, 159, 182, 195, 196 and 205; line count is 285 before and after.
- `grep -n 'sections 3.1' <candidate>` prints no match: the phrase that made AC-1.1 and SPEC:159 disagree is gone.
- Every old string was matched exactly once before replacement (the script asserts it); no other file under the workspace was written besides this report.

## Out of scope, noted only

Medium and minor findings stay open as listed at R1:281-284. One interaction to hand to the next reviewer: the `--unattended` flag in the P1 row now covers only the commands listed there, which also narrows M-9 (R1:168-170) as a side effect; M-9 itself was not worked on. No verdict is given.
