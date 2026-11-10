# Revise 1: orca-worker-contract-spec.md

- Prompt: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full at `/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p14/haiku-baseline/runs/a3-r3/home/.claude/rules/prompts/document_review_loop_prompts.md`, REVISE section).
- Brief: `review/round1.md` Reviser brief (`review/round1.md:97-101`), ids B1, B2, B3, B4.
- Candidate: `specs/orca-worker-contract-spec.md`
- Candidate sha256 before: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (identical to `specs/history/spec-v1.md`, used as the diff baseline)
- Candidate sha256 after: `90517bb8b39156a6ae96df698dafb7e24324de3cb8682a343273a1cbd2cce875`
- Not run: spec-panel. No PASS awarded. Medium findings M1-M8 and the minor notes in `review/round1.md:61-76` were left alone, as the brief says.

## Byte accounting

Before: 57763 bytes. After: 60320 bytes. Net +2557 bytes. Added 7187 bytes, deleted 4630 bytes.

Method: `diff` against `specs/history/spec-v1.md`, byte counts under `LC_ALL=C`. Each of the 11 diff hunks was attributed to one finding id by its content.

| Finding id | Bytes added | Bytes deleted | Net |
|---|---|---|---|
| B1 | 4387 | 3645 | +742 |
| B2 | 848 | 270 | +578 |
| B3 | 999 | 463 | +536 |
| B4 | 953 | 252 | +701 |
| Total | 7187 | 4630 | +2557 |

Hunk-level split: the B1 hunks are WC-4 (1637/1211), section 2.3 (613/512), the adversarial row (343/317), the workflow row (324/308), SA-4 (588/507), the section 6 P1 row (560/547) and AC-1.4 (322/243). B4 is the spec-panel row (576/252) and the new section 9 item 15 (377/0). B2 is the AC-C1 row and its block (848/270). B3 is AC-0.4 (999/463).

## Finding rows

| Finding | Result | Applied where (`specs/orca-worker-contract-spec.md`) | Reason and evidence |
|---|---|---|---|
| B1 | Applied | WC-4 at line 62; section 2.3 at line 73; section 3.1 adversarial row at line 83; section 3.1 workflow row at line 92; SA-4 at line 149; section 6 P1 row at line 159; AC-1.4 at line 208 | WC-4 required `<output-dir>/return-contract.yaml`, but `/sc:workflow` has no output-directory flag and its contract path `.dev/tasks/to-do/<id>/return-contract.yaml` exists only after the run creates the package (`ws/.dev/orca-command-refactor/inventory/commands-b.md:272`). Its pre-creation STOPs write no contract (same line; `:39` per the inventory). WC-5 therefore maps them to `failed`, so the workflow "write the contract for pre-creation STOPs" fix is removed, and workflow is dropped from the P1 fix list and from SA-4. The adversarial row's `<output>/adversarial/` subdirectory is replaced by the WC-4 path, since the inventory shows the adversarial contract filename is not fixed (`ws/.dev/orca-command-refactor/inventory/commands-a.md:60-61`). |
| B2 | Applied | AC-C1 row at line 172; the corrected command in a fenced block at lines 176-179; exemption note at line 182 | The original pattern put `\|` inside an ERE, which GNU grep reads as a literal pipe. Tested on piped strings, with no file written: `run orca orchestration task-create now` matches (exit 0); `orca-ide worktree create` matches (exit 0); `orca alone and orchestration alone` does not match (exit 1); the original pattern does not match the first sample (exit 1). The exemptions are `src/superclaude/core/WORKER-CONTRACT.md` (SA-2 allows an Orca mention there) and `src/superclaude/core/HOW-WE-WORK.md` (SA-5 requires an Orca section there). Limitation: `HOW-WE-WORK.md` is excluded from the grep entirely, so its Orca section is checked by reading it in P0. |
| B3 | Applied | AC-0.4 at line 204 | AC-0.4 required step 3 (WC-4 contract path) and step 4 (YAML `status` and `command` keys) in P0, before the contract exists until P1 (original AC-0.4 at `specs/history/spec-v1.md:194`). `/sc:troubleshoot` without `--fix` writes `REPORT.md`, not YAML (`ws/.dev/orca-command-refactor/inventory/commands-b.md:242`). The workflow contract has `status`, `plan_path` and `reflect_report_path` and no `command` key (`commands-b.md:272`). The row now checks the outcome against the report's own status, tests the named report file with `test -s`, and names the report file per command. |
| B4 | Applied as a conditional row; the factual conflict stays UNVERIFIED | spec-panel row at line 120; new section 9 item 15 at line 296 | The inventory says no `--output` flag exists (`commands-b.md:43`, `:182`). The reviewer's contradicting evidence is in `command.md` (`command.md:23`, `:455-463`) in the sandbox root, which is outside the workspace. Per the brief, a citation that cannot be checked against a workspace file is UNVERIFIED, so the conflict is not settled here. The row now reads the existing output flag and `## Unattended mode` section first and adds neither again if they exist, so it is correct either way. Not applied: the reviewer's citation-drift corrections (`command.md:224`, `:479`, `:36-37`), because they rest on the same out-of-workspace file. The row keeps its original citations, and item 15 records the open question. |

No finding was rejected.

## Checks

- Self-check of the revised text against the review's quoted lines is not applicable, since this is a REVISE pass, not a re-review.
- Stale references: a search of the revised spec finds no spec text that still names `<output>/adversarial/return-contract.yaml` (the only `adversarial/return-contract` hits are the external evidence citations at `specs/orca-worker-contract-spec.md:11` and `:23`). The remaining `\|` sequences (AC-C4, AC-C5, AC-0.3) are shell pipes in table cells, not ERE alternation, so B2 does not touch them.
- Every added sentence carries its finding id, as the REVISE prompt requires.
