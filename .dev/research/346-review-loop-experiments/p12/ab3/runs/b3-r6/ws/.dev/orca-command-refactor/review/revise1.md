# Revise 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Blocking ids repaired: F-01, F-02, F-03 (Reviser brief, `.dev/orca-command-refactor/review/round1.md:228`). Medium and minor findings (F-04 to F-28) were left alone. No PASS is claimed.

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place once. Line count unchanged (285; the edits replace text inside existing lines).

## Byte accounting

| | bytes |
|---|---|
| Size before (`wc -c`) | 57763 |
| Size after (`wc -c`) | 58973 |
| Net | +1210 |
| sha256 before (equals `specs/history/spec-v1.md`, and `round1.md:9`) | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| sha256 after | `361193fc0635fb15c8c62bef7845f79c10650c2ce1378fb6cefbbb9b882a7ae8` |

Method: for each of the 15 replacements, a byte-level `difflib.SequenceMatcher` between the old and new fragment counted inserted and deleted bytes (text kept unchanged inside a replaced fragment counts as neither). The per-finding sums add to the net: 1596 added - 386 deleted = +1210.

| Finding | Replacements | Bytes added | Bytes deleted | Net |
|---|---|---|---|---|
| F-01 | 7 | 570 | 246 | +324 |
| F-02 | 7 | 713 | 129 | +584 |
| F-03 | 1 | 313 | 11 | +302 |
| Total | 15 | 1596 | 386 | +1210 |

The replacement count per id is the number of distinct edits; the F-02 count includes the section 6 rule, the D1 wording and section 2.3. Of the F-01 edits, only AC-1.4 shrinks the text; the rest add words the finding calls for.

## One row per finding id

| id | Result | Where applied (new text, spec line) | Cited reason / evidence |
|---|---|---|---|
| F-01 | Applied | WC-4 title and path rule, spec:62. Path is now "the path its section 3 row names"; default `<output-dir>/return-contract.yaml`; a file-valued `--output` gets `<that file path>.return-contract.yaml`; adversarial and workflow keep their row paths. The "every outcome" sentence (spec:62) now excepts workflow stops before its package folder exists. Section 2.3, spec:73: output directory "or file its row names", and workflow's path is read from its run result. Section 3 intro, spec:76: "Contract" means the file at the path its row names. Workflow row, spec:92: fix column changed from "Write the contract for pre-creation STOPs too (P1)" to "None", the missing file is read as `failed`. SA-4, spec:149: "adversarial and workflow contract gaps" became "the adversarial contract gap". AC-1.4, spec:198: the workflow clause and the workflow ref removed from the check. | Finding text `round1.md:97-100` and the boundary rows `round1.md:31-34`. Adversarial writes under `<output>/adversarial/` (`INV-A:35,60`, `commands-a.md`). Workflow's contract lives in the package folder and "Not written for pre-creation STOPs" (`INV-B:272`); its brief has no output dir (spec:92). tdd, init-lite and spec-panel use a file-valued `--output` (spec:87, 90, 120). I chose to delete the pre-creation requirement (the finding says the text "cannot be built as written") rather than invent a second location; WC-5 already maps a missing file to `failed` (spec:63). Adversarial's row already named `<output>/adversarial/return-contract.yaml` (spec:83), so it needed no edit. |
| F-02 | Applied | Section 6 intro, spec:154: a command accepts `--unattended` only from the phase that resolves all its gates; before then the coordinator briefs it without the flag. P1 row, spec:159: `--unattended`, the section and the output flags apply to the eight no-gate commands (analyze, build, business-panel, design, document, explain, index, test); load (usage line only) and the small fixes to adversarial, cleanup-audit and index-repo add no flag; workflow dropped from the fix list (see F-01). Section 3 intro, spec:76: the section is gained only by commands in a phase scope that lists `--unattended`; the P1 small fixes and the load usage line add none. Section 2.3, spec:73: the brief carries `--unattended` only where the command's phase has added it. AC-1.1, spec:195: asserts the section for the eight P1 commands and that no other command and no section-4 command has one yet. AC-1.2, spec:196: runs the eight commands with `--unattended` and the output flag each row adds. D1(a), spec:228: "every worker's command line" narrowed to workers whose command accepts the flag. | Finding text `round1.md:112-118`. The unsafe interim state named there (auggie-review posting, task commit/push, post-release provisioning, `round1.md:112`) disappears because those commands are P2 and P4 (spec:160-162) and do not take the flag before then, so WC-2 and WC-9 (spec:60, 67) are not contradicted. The brainstorm and init-lite "None" rows (spec:84, 87), load's "none" report (spec:112) and pr-submit under D3(a) (spec:240) no longer conflict with AC-1.1. AC-1.2's `--output <dir>` on index-repo, cleanup-audit and workflow (`round1.md:116`) is gone because those three are not in the checked set. The recommendation (restrict the flag, section and AC-1.x checks to the commands the phase converts) was followed; deleting scope replaced adding rules. |
| F-03 | Applied | AC-0.4 pass condition, spec:194: the P0 reading of 7.2. Step 1's brief is the command line as written with no `--unattended`; step 3's `--outcome` is `succeeded` when the command's existing report file was written and `failed` otherwise, and the report path is that file; step 4 is `test -s` on that file with no `status` check. The WC-4 and WC-5 contract rules start at P1. | Finding text `round1.md:104-106`. P0 has no command edits (spec:158), no WC-4 contract exists before P1 (spec:79, 159), troubleshoot writes `REPORT.md` only (spec:91; `INV-B:242`), and no command accepts `--unattended` until P1 (spec:159, now spec:154). The edit is placed in AC-0.4 only, so 7.2 and the other phases are untouched. |

## Self-check notes

- Every added sentence is limited to the three findings; the ids are cited in this table because the spec itself carries no finding ids (adding ids to the spec text would be an extra edit the findings do not call for).
- Residual points noticed and left alone because they belong to Medium or minor findings: the cleanup-audit and index-repo contract locations when no output flag exists (F-08), `--unattended --interactive` on adversarial, brainstorm and release-split (F-08), nested-command propagation (F-09), and the spec:79 phrase "until Phase 1 adds the contract" for ready commands.
- Citations to `src/superclaude/**` carried in the edited rows are unchanged and remain UNVERIFIED in this sandbox (not readable here). The `INV-A` and `INV-B` lines cited above were read in `inventory/commands-a.md` and `inventory/commands-b.md`.
