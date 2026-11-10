# Revise 2: Orca worker contract spec

- Candidate, edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
- Sha256 before: `c0bcf427b1adbc33a7a7d8ed59cafb19f0ae4373145c6ccaac5362de30dbc042` (same as `review/round2.md:6` and `specs/history/spec-v2.md`, used here as the pre-edit copy).
- Sha256 after: `b72ae0165828ae31e6e86c4c17ddcc94a378f90648e36bc5398fab3017942e03`.
- Revise brief: REVISE prompt from `home/.claude/rules/prompts/document_review_loop_prompts.md:58-60`, which is read in the sandbox.
- Ids to repair (`{{IDS}}`): B-2, N-1. These are the two ids that VERIFY step VF2 confirmed (`review/verify-2.md:15`, `confirmed: B-2, N-1`). B-3 and N-2 are not in the brief and were rejected at VF2 (`review/verify-2.md:11,13`), so they are left unchanged.
- Inputs read: `README.md`, `review/round2.md`, `review/verify-2.md`, the spec, `inventory/commands-a.md`, `inventory/commands-b.md`. Not read or used: `command.md`, which is outside the inventory. The `src/`, `tests/` and `.claude/` citations are UNVERIFIED in this sandbox, as before.

## Byte accounting

Size before: 59236 bytes (285 lines). Size after: 59786 bytes (286 lines, the new item 15 at line 286). Net +550 bytes. Bytes deleted: 569. Bytes added: 1119. The per-edit figures are the exact old and new strings, counted with `wc -c`; the item-15 figure includes its leading newline.

| Edit | Spec location (after edit) | Finding ids | Deleted | Added | Net |
|---|---|---|---|---|---|
| WC-4 sentence, flat `--output` rule replaced | spec:62 | B-2 and N-1 (shared edit, counted once) | 346 | 488 | +142 |
| adversarial contract path | spec:83 | N-1 | 77 | 136 | +59 |
| spec-panel directory flag | spec:120 | B-2 | 146 | 156 | +10 |
| UNVERIFIED item 15 (new) | spec:286 | B-2 | 0 | 339 | +339 |
| Total | | | 569 | 1119 | +550 |

Per id: B-2 receives +10 (spec:120) and +339 (spec:286), plus its share of the spec:62 edit. N-1 receives +59 (spec:83), plus its share of the spec:62 edit. The spec:62 edit is shared, so its 346 deleted and 488 added bytes are not split between the two ids.

## Per-finding disposition

| Id | Disposition | Where applied | Reason and citation |
|---|---|---|---|
| B-2 | Applied | spec:62 (WC-4), spec:120 (spec-panel row), spec:286 (item 15) | The old spec:120 said "add a directory flag, not `--output`" without naming it, so the brief could not carry it. The inventory says spec-panel has no output flag today (`inventory/commands-b.md:182`), so the row now names `--output-dir <dir>`. spec:62 says the brief passes the directory "through the output flag that section 3 names for that command". `--output-dir` is already the name pr-submit uses (`inventory/commands-b.md:92`). The unverified `command.md:460` reading moved to item 15 (UNVERIFIED) with a P2 check. Residual: if spec-panel already has a directory flag under another name, the row must be renamed at P2. |
| N-1 | Applied | spec:62 (WC-4, flat sentence removed), spec:83 (adversarial row) | The flat sentence "`--output` is not a directory flag" is deleted. spec:62 now states that `--output <dir>` and `--output-dir <dir>` each take a directory, that a row adding a report path without a flag name adds `--output-dir <dir>`, and that tdd and init-lite `--output <file>` take a file inside a fresh directory. The adversarial contract is set to `<output>/return-contract.yaml`, the WC-4 path, so there is one contract path for that command. Merged output stays under `<output>/adversarial/`. This matches brainstorm's `<output>/return-contract.yaml` (`inventory/commands-a.md:84`). The inventory records that the skill names no contract file and that real runs wrote two different paths (`inventory/commands-a.md:60`), which is why the path is now fixed in the spec. |
| B-3 | Not in brief; rejected at VF2 | Unchanged. spec:112, spec:195 and spec:265 are as they were. | `review/verify-2.md:11`: the stated outcome is not produced, because AC-1.1 already exempts load by name (spec:195). Noted, unactioned. |
| N-2 | Not in brief; rejected at VF2 | Unchanged. spec:61 and spec:235 are as they were. | `review/verify-2.md:13`: the "never" sentence in the same bullet (spec:61) still excludes the gates under D2(b). Noted, unactioned. |
| B-4 | Noted at VF1, no action | Unchanged. | `review/round2.md:62` notes that round 1 lists it as blocking while its VF1 block rejects it. Not in this brief. |
| F-1 | Medium, left alone | Unchanged (spec:61 "informational"). | The revise prompt says to leave Medium and minor findings alone. |
| F-2 | Medium, left alone | Unchanged (spec:79 heading and row). | Same rule. |
| F-3 | Minor, left alone | Unchanged. | Same rule. Note for the coordinator: the prompt requires each addition to cite its finding id, so the new text in spec:62 and spec:286 contains "(B-2)" and "(N-1)". This is the opposite of what F-3 asks for, so the coordinator should decide whether to move those ids out of normative text on the next pass. |
| M-1 to M-17, m-1 to m-4 | Round-1 notes, not re-graded, left alone | Unchanged. | Not in the brief. |

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| spec-panel directory flag name | `--output-dir <dir>`; `--report-dir <dir>` (named in the review's reading of `command.md:460`, not checked here); keep `--output` | `--output-dir` is already used by pr-submit (`inventory/commands-b.md:92`), and the inventory records no spec-panel output flag (`inventory/commands-b.md:182`). The `--report-dir` reading is kept as UNVERIFIED item 15, with a P2 check, instead of being relied on. |
| Adversarial contract path | `<output>/adversarial/return-contract.yaml` (old spec:83); `<output>/return-contract.yaml` | The WC-4 rule (spec:62) gives `<output-dir>/return-contract.yaml`, and brainstorm already uses `<output>/return-contract.yaml` (`inventory/commands-a.md:84`). One path per command lets the coordinator open the file the 7.2 step 3 check expects (spec:182). |
| Meaning of `--output` in section 3 | Keep the flat "not a directory" rule; name the flag per row; read `--output` as a directory when a row adds it | Chose per-row naming plus the rule that a row adding a report path without a flag name uses `--output-dir <dir>`. This keeps the existing `--output <dir>` rows (adversarial, brainstorm, reflect, release-split, roadmap, post-release) unchanged, and the tdd and init-lite file cases stay as they were. |

## Not verified

- `command.md:460` (spec-panel `--report-dir` reading): outside the inventory; not read for this revision. Carried as UNVERIFIED item 15.
- Every `src/`, `tests/`, `.claude/` and `.dev/` citation: UNVERIFIED in this sandbox, unchanged.

## Status

The candidate was revised once, for B-2 and N-1 only. No PASS is awarded here. The next review is the coordinator's.
