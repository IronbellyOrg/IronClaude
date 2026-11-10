# Revise 1: Orca worker-contract spec

Prompt followed: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Ids: B-1, B-2, B-3 (`review/round1.md:225-240`). Medium and minor findings left alone. No verdict is awarded.
Line numbers below are the candidate's line numbers before the edit (the edits add no lines).

## Byte accounting (candidate)

| | bytes |
|---|---|
| Before | 57763 |
| After | 58308 |
| Net | +545 |

| id | added | deleted | net |
|---|---|---|---|
| B-1 | 427 | 285 | +142 |
| B-2 | 203 | 0 | +203 |
| B-3 | 212 | 12 | +200 |
| Total | 842 | 297 | +545 |

Counts are the changed span of each edit with the common prefix and suffix trimmed, in UTF-8 bytes.

## One row per finding

| id | Disposition | Where | Reason |
|---|---|---|---|
| B-1 | Applied by narrowing | Spec 6 P1 scope (line 159): the flag is now "accepted by the commands named in this row", and the P2-P4 commands get it in their own phase. Section 3 intro (line 76): "Every changed command except `load` also gains the `## Unattended mode` section ... in its own phase". AC-1.1 (line 195): asserts the section for each command in the P1 row except `load`, and that neither `load` nor any section-4 command has one. | Matches the `load` row (line 112, "none (see note)"), the P4 wait for D2-D4 (lines 154, 162) and D3(a) "no pr-submit changes" (line 240). Deleted the 3.1-3.2 "every command" scope, as `round1.md:58` recommends. The edit to line 76 is needed because the old sentence would still require the section on `load`. |
| B-2 | Applied | Spec 2.2 WC-3 (line 61): one sentence appended. The answer may supply only a value no safety rule or outward-action rule reserves; `implement`'s Ruling (D2(a)) and every flag WC-9 keeps off are excluded, and those gates still resolve as blocked. | Consistent with D2(a) and AC-4.1 (lines 234, 208), WC-9 (line 67) and D4(a) (line 245), as `round1.md:116-117` recommends. |
| B-3 | Applied | Spec WC-4 (line 62): where `--output` is a file (tdd, init-lite, spec-panel) the contract is `<value of --output>.return-contract.yaml`, beside the file and never inside it. Section 2.3 (line 73): the brief names the output directory, or the output file for those three commands, so the contract path is known before dispatch. | One rule for the file-valued `--output` of lines 87, 90 and 120, and AC-2.2 (line 200) can now read the contract at a defined path. A sibling name avoids a `return-contract.yaml` collision in a shared directory such as `docs/x/`; this choice is mine (the finding offered two examples). |

## Not changed (outside the blocking ids)

- Line 76 still reads "the WC-4 file `<output-dir>/return-contract.yaml`" for "Contract"; the WC-4 sentence above now qualifies it. Not edited to avoid an addition no blocking finding names.
- AC-2.2 text unchanged; it needed no edit once WC-4 defines the path.
- Source claims about command files rest on the inventories; none could be checked against `cmd/` or `sk/` in this sandbox. Those citations stay UNVERIFIED.
