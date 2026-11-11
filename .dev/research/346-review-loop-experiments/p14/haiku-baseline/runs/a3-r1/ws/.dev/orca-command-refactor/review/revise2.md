# Revise 2: orca-worker-contract-spec.md

Brief: repair only the blocking findings F-5 and F-6 from `.dev/orca-command-refactor/review/round2.md` (its Reviser brief, final section). Method: REVISE prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md` (sandbox home copy at `home/.claude/rules/prompts/document_review_loop_prompts.md`). Spec-panel not run. No PASS is awarded; the revised candidate goes back to review.

- Candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- Before revision: 59286 bytes, 286 lines, sha256 `24081c933a7fbedd6b461f8f09d06fe7d90105a4b5e12f7221ed9cf63dc4b40e`
- After revision: 60147 bytes, 286 lines, sha256 `e9171857b793b520e3e6291ce69b77aaa2e13a035d1f119ba47eb5a42eff8f83`
- Net change: +861 bytes (+565 for F-5, +296 for F-6). Line count unchanged; both edits replace text inside existing table cells (`SPEC:194`, `SPEC:195`).

## Byte accounting per finding id

Bytes are counted on the replaced text fragment only (old fragment deleted, new fragment added).

| Finding | Bytes deleted | Bytes added | Net |
|---|---|---|---|
| F-5 | 81 | 646 | +565 |
| F-6 | 235 | 531 | +296 |
| Total | 316 | 1177 | +861 |

Check: 59286 + 861 = 60147.

## Finding rows

| Finding | Applied where | Result |
|---|---|---|
| F-5 (blocking, AC-0.4 step 4) | `SPEC:194`, AC-0.4 cell: the sentence "step 4 uses the command's existing report file, since the contract arrives in P1." is replaced by a P0 variant of step 4 | Applied. Step 4 in P0 is now `test -s` on the command's existing report file, named per command: `.dev/tasks/to-do/<id>/return-contract.yaml` for `/sc:workflow` (cites `inventory/commands-b.md:272`); the run's own output file for `/sc:adversarial` (cites `SPEC:83`, filename not fixed, so the phase report names it before step 3); `REPORT.md` for `/sc:troubleshoot` (status key UNVERIFIED, cites `SKILL.md:57,63-68,209` as already cited in `SPEC:91`). A `status` key, where present, must be one of the four values. The `command` assertion is removed from P0 only, because `inventory/commands-b.md:272` lists no `command` key for workflow and WC-4 (`SPEC:62`) adds it in P1. The generic 7.2 step 4 (`SPEC:183`) is not edited; the AC-0.4 cell states that step 4 is replaced for P0. |
| F-6 (blocking, AC-1.1) | `SPEC:195`, AC-1.1 cell: the clause "every command in sections 3.1-3.2 except `/sc:load` ... has a `## Unattended mode` section" is replaced | Applied. AC-1.1 now asserts the section only for the 12 commands whose section 3 row names phase P1 (3.1 rows adversarial, cleanup-audit, index-repo, workflow at `SPEC:83,85,86,92`; 3.2 rows analyze, build, business-panel, design, document, explain, index, test at `SPEC:99,101,102,106,107,108,111,123`). It asserts no section for brainstorm and init-lite (`SPEC:84,87`, no small fix) and for `/sc:load` (WC-4 exception, F-3, `SPEC:62,112`). Later phases' tests assert the section only for the commands their phase changes (rule stated in the AC-1.1 cell, per F-6's recommendation). Phase membership cross-checked against `SPEC:159` (P1 Commands column) and `SPEC:160-162` (P2-P4). |

## Not changed (outside the blocking ids)

- Medium and minor findings from `review/round2.md` (M-10, m-4, m-5, and the carried M-1 to M-9 and m-1 to m-3) are not revised, per the brief and the REVISE prompt.
- The P1 scope cell at `SPEC:159` says P1 accepts `--unattended` on "every command in sections 3.1 and 3.2". The revised AC-1.1 does not depend on that clause, because it asserts sections only for the P1 list above. The clause is left as written. Whether a flag-only P1 change to a 3.2 command is the intended reading is not decided here.
- No other text was edited. `SPEC:194` is the only line in AC-0.4, and `SPEC:195` is the only line in AC-1.1 that changed.

## Self-check

- `grep -c 'step 4 is replaced by this P0 variant'` matches `SPEC:194` once (F-5).
- `grep -c 'F-6'` matches `SPEC:195` once (F-6). The prior `F-3` citation in the AC-1.1 cell is kept.
- Line count unchanged at 286, so no other line numbers moved.
- Citations added in this revision that point into the workspace were checked: `inventory/commands-b.md:272` (workflow contract fields) and `inventory/commands-b.md:267-273` (workflow row). Citations to `sk/...` files are carried from the spec and are UNVERIFIED in this workspace, as the spec already states.
