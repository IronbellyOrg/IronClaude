# Revision 1: orca-worker-contract-spec.md

- Prompt followed: REVISE in `~/.claude/rules/prompts/document_review_loop_prompts.md` (REVISE prompt section). IDS = F-1, F-2 (`.dev/orca-command-refactor/review/round1.md`, Reviser brief). Medium and minor findings (M-1..M-9, N-1..N-4) untouched. No PASS claimed.
- Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. No lines added or removed; spec line numbers are unchanged. Citations to `INV-B:65` and spec lines were checked against the spec/inventories in the workspace; source-tree paths were not touched.

## Byte accounting (spec file)
- Before: 57763 bytes. After: 58184 bytes. Net +421.

| Finding id | Edits (spec line) | Bytes added | Bytes deleted | Net |
|---|---|---|---|---|
| F-1 | P1 scope text, spec:159 (narrowed from "every command in sections 3.1 and 3.2" to "each command listed in this row except load", with exclusions for P2-P4 and pr-submit under D3(a)) | 255 | 111 | +144 |
| F-1 | AC-1.1, spec:195 (scoped to the P1 row of section 6 except load) | 79 | 61 | +18 |
| F-2 | AC-C1 command, spec:172 (dropped `src/superclaude/core` from the searched paths) | 33 | 54 | -21 |
| F-2 | AC-C1 pass condition, spec:172 (states core files are not searched, and why) | 156 | 29 | +127 |
| F-2 | SA-2, spec:147 (states core files may carry Orca command text and AC-C1 covers commands, skills, agents only) | 180 | 27 | +153 |
| Total | | 703 | 282 | +421 |

Per finding: F-1 added 334, deleted 172 (+162). F-2 added 369, deleted 110 (+259). Each addition carries its `[F-1]` or `[F-2]` tag in the text.

## Per-finding disposition
| Id | Result | Where | Reason |
|---|---|---|---|
| F-1 | Applied (narrowed) | spec:159, spec:195 | The conflicting texts were load with no report (spec:112, spec:265), pr-submit untouched under D3(a) (spec:240), implement and post-release in P4 (spec:162). AC-1.1 and the P1 scope now cover only the commands in the P1 row (spec:159: analyze, build, business-panel, design, document, explain, index, test), minus load. P2-P4 commands get the flag in their own phase; pr-submit gets none under D3(a). The "no section-4 command has one" clause is kept (spec:128). |
| F-2 | Applied (narrowed) | spec:147, spec:172 | Took the recommendation's second option: AC-C1 searches `commands`, `skills`, `agents` only, and SA-2 says so. This resolves the clash with WC-3, the P0 brief template and the `HOW-WE-WORK.md` Orca section (spec:158). Section 1.2 E5's baseline grep (spec:25) is a past observation and is left alone. |
