# Revise 1: orca-worker-contract-spec.md

Prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:53-55`. Values: candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, IDS = F1 (the only id in the Reviser brief, `.dev/orca-command-refactor/review/round1.md:190`). No spec-panel was run and no PASS is claimed.

Citation keys: `S:N` = line N of the revised spec (line numbers are unchanged by the edits, 285 lines before and after); `R1:N` = `.dev/orca-command-refactor/review/round1.md`; `BASE` = `.dev/orca-command-refactor/specs/history/spec-v1.md` (byte-identical to the pre-revision spec: both sha256 `d3cdbe57...25200d`, `cmp` printed no difference). Inventories were not re-read for this revision: no edit depends on an inventory fact that is not already quoted at the cited spec lines.

## Byte accounting

| Item | Before | After |
|---|---|---|
| Spec size | 57763 bytes | 57939 bytes |
| Spec sha256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` | `a836576df87b59b039072268c20705696ba11a57c7fd7ec19d1e677d12268487` |
| Lines | 285 | 285 |

Net +176 bytes (57939 - 57763), checked with `wc -c` and a per-line byte comparison of BASE against the revised spec: only S:159 (+81) and S:195 (+95) differ.

Bytes per finding id:

| Finding id | Bytes deleted | Bytes added | Net |
|---|---|---|---|
| F1 | 42 | 218 | +176 |
| (any other id) | 0 | 0 | 0 |

Per edit within F1:

| Line | Deleted text (bytes) | Added text (bytes) |
|---|---|---|
| S:159 (P1 scope) | `in sections 3.1 and 3.2` (23) | `named in this row's Commands column` (35); ` Each later phase adds the flag and the section for its own commands.` (69) |
| S:195 (AC-1.1) | `in sections 3.1-3.2` (19) | `named in the P1 row of section 6, except load (it writes no report)` (67); `; commands of Phases 2-4 are not asserted here` (47) |

## Findings

| Id | Disposition | Where | Reason and evidence |
|---|---|---|---|
| F1 | Applied | S:159 and S:195 | See below. |

### F1: applied

Defect (R1:34-44): S:159 and S:195 (AC-1.1) consumed "every command in sections 3.1 and 3.2", which is 37 commands, while the Phase column assigns 9 commands from 3.2 to P1 (analyze S:99, build S:101, business-panel S:102, design S:106, document S:107, explain S:108, index S:111, load S:112, test S:123) and puts implement (S:109), post-release (S:113) and pr-submit (S:114) in P4, which S:154 says waits for D2-D4. AC-1.1 therefore could not pass at the end of P1, and S:154 and S:167 then block Phases 2-4.

Edit 1, S:159 (P1 scope, flag sentence). Before: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)". After: "the `--unattended` flag accepted by every command named in this row's Commands column (a no-op where a command has no gate)", plus the closing sentence "Each later phase adds the flag and the section for its own commands." The Commands column of the same row (S:159) names the nine 3.2 commands and the four ready-command fixes (adversarial, cleanup-audit, index-repo, workflow), 13 commands, which is what R1:43 asks for ("the nine named at S:159 plus the section 3.1 fixes"). The closing sentence is the statement R1:43 asks for ("a later phase adds the section for its own commands"); it adds no mechanism.

Edit 2, S:195 (AC-1.1). Before: the test asserts the section on "every command in sections 3.1-3.2". After: "every command named in the P1 row of section 6, except load (it writes no report)", with the clause "commands of Phases 2-4 are not asserted here" at the end of the assertion. The `load` exception is not extra scope: R1:40 names it as part of the contradiction (load has "Report: none", S:112, so a section "naming `return-contract.yaml`" has nothing to name), and the exception removes that case from the test. `load` keeps the flag as a no-op and its usage-line fix under S:159, unchanged.

Result against the stated requirement (checked on the revised text, not assumed): the AC-1.1 set is the P1 row's 13 named commands less load, 12 commands, all of which the P1 phase touches (S:159 and the Phase column); no command assigned to P2, P3 or P4 is asserted at the end of P1; the section-4 clause is unchanged (6 coordinator-only commands, S:128-137). S:154 and S:167 are unchanged and now satisfiable, and D3(a) (S:240, "no pr-submit changes in Phase 4") no longer conflicts with a P1 assertion on pr-submit.

Cross-check of unchanged text that depends on the edit: S:76 and S:52 say a changed command gains the `## Unattended mode` section; with S:159 now ending "Each later phase adds the flag and the section for its own commands", that wording is consistent with the phase each command is changed in. S:79 ("until Phase 1 adds the contract") concerns the ready commands' report file and is consistent with the S:159 fixes list. UNVERIFIED: whether the four ready-command fixes at S:159 also need the section in P1 (they are named in the Commands column and so are asserted by AC-1.1); R1:43 treats them as in scope, so this revision follows it.

## Not touched

Medium and minor findings F2-F14 and N1-N5 (R1:46-123) were left alone as the Reviser brief requires (R1:197). In particular the `--unattended` flag existence for brief purposes (F6, S:73), AC-0.4's step 3 (F2, S:194), and AC-C1/AC-C5 (F10, F11, S:172, S:176) are unchanged. No file other than the spec and this report was written. `src/superclaude/...` line citations in the spec remain UNVERIFIED in this sandbox, as before.

I have not reviewed or graded the revised candidate; the reviewer decides the verdict.
