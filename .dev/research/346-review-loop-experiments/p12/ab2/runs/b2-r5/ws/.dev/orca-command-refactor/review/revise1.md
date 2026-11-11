# Revise 1

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (home resolved to the sandbox `home/`), read in full. Blocking ids repaired: F-01, F-02, F-03 (`review/round1.md:208`, confirmed in `review/verify-1.md`). Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Line numbers are unchanged by the edits (285 lines, all edits are in-line). Medium and minor findings were left alone. This report awards no PASS.

## Byte accounting

| | bytes | sha256 |
|---|---|---|
| Before | 57763 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| After | 58543 | `363aad34a552033a79d2d651495b742507e757c6d9545270ee860f0bf999e142` |
| Net | +780 | |

Added and deleted bytes are counted by character-level diff of each edited string (an edit that only inserts text deletes 0). Added minus deleted equals the net change; the three net values sum to 780, the file-size difference.

| Finding | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| F-01 | 113 | 5 | +108 |
| F-02 | 194 | 0 | +194 |
| F-03 | 483 | 5 | +478 |
| Total | 790 | 10 | +780 |

## Findings

All spec line numbers below are in the revised candidate. Nothing was deleted at paragraph level: each repair narrows an existing sentence with an exception, because the requirements still hold for the commands the exception leaves out.

| id | Disposition | Where applied | What changed |
|---|---|---|---|
| F-01 | applied | `spec:194` (AC-0.4) | Steps were "1-3 and 5-7 pass; step 4 uses the existing report file". Now "steps 1, 2 and 5-7 pass; in step 3 the `--outcome` and report path are judged against the command's existing report file, and in step 4 only `test -s` on that file applies, since the contract arrives in P1 (F-01)". Step 3's "exactly one `worker_done`" still applies in P0. The 7.2 text itself (`spec:182-183`) is untouched, so P1 onward still requires the WC-4 contract. P0 now passes on unedited commands (`spec:158` "no command edits"), so `spec:154` no longer blocks P1. The old step 4 asserted `status` and `command` in a YAML file, which troubleshoot's `REPORT.md` (`spec:91`) cannot satisfy; narrowing it to `test -s` is the only part of step 4 that can hold in P0. |
| F-02 | applied | `spec:195` (AC-1.1), `spec:76`, `spec:52` | AC-1.1 now asserts the section for "every command in sections 3.1-3.2 except `load`, `brainstorm` and `init-lite` (F-02)". `spec:76` now says only "every changed command that gets a contract" gains the section, and names those three as gaining none. `spec:52` carries the same qualifier so section 2.1 does not contradict it. Those three are exactly the commands whose rows say no contract or no change: load report "none", "P1 (usage line only)" (`spec:112`) and Decisions (`spec:265`); brainstorm and init-lite small fix "None" (`spec:84`, `spec:87`). The "no section-4 command has one" half of AC-1.1 is unchanged. |
| F-03 | applied | `spec:62` (WC-4), `spec:76`, `spec:73`, `spec:182` (7.2 step 3), `spec:196` (AC-1.2) | WC-4 keeps `<output-dir>/return-contract.yaml` as the rule and names the two commands that keep the path they already use: adversarial `<output-dir>/adversarial/return-contract.yaml` (matches `spec:83` and AC-1.4 `spec:198`) and workflow `.dev/tasks/to-do/<id>/return-contract.yaml` (matches `spec:92`), where the id is command-generated and the worker passes the path it finds. I chose to carry the existing paths into WC-4 and not to change the adversarial row, because the real runs wrote under `<output>/adversarial/` (`inventory/commands-a.md:35`, `:60`). `spec:76` ("Contract" definition) and `spec:73` (path "known before dispatch", not for workflow) match. Step 3 now reads "the contract path WC-4 gives for that command (F-03)". AC-1.2 gives workflow `--unattended --handoff none` with no `--output`, because `spec:92` passes no output flag. The WC-4 title still says "known before dispatch" and is not retitled, since the body now states the workflow exception. |

## Notes for the next review

- Two spec texts I did not change but that depend on the repaired text: `spec:159` (P1 scope: "`--unattended` flag accepted by every command in sections 3.1 and 3.2") sits beside `brainstorm` and `init-lite` having "None" as a small fix (`spec:84`, `spec:87`); the repair of F-02 does not touch it because it concerns flag acceptance, not the section or contract. This is a possible Medium or minor item, not a blocking finding in `review/round1.md`.
- Citations I could not check in the sandbox are the same ones the review report marks UNVERIFIED: `src/superclaude/...` line numbers and `INV-B:242` (`review/verify-1.md:3`). The evidence for the F-03 path choice (`inventory/commands-a.md:35`, `:60`) is checked against the inventory file.
