# Revise round 1: orca-worker-contract-spec.md

- prompt followed: REVISE prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full first)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place; no other file changed besides this one
- blocking ids from the Reviser brief (`.dev/orca-command-refactor/review/round1.md:211`): F1, F2, F3. Medium and minor findings (F4-F19, N1-N6) left alone.
- no PASS is claimed. The README (`.dev/orca-command-refactor/README.md`) was read first; the only evidence used is the review report and the spec. The inventories were not needed: every fix narrows or restates text the report already cites, so no inventory line is relied on here (`INV-*` lines inside the spec are untouched).
- line numbers below are for the revised file; the line count is unchanged (285), so they equal the old line numbers.

## Byte accounting
Before: 57763 bytes (sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`, equal to the sha256 the review reports at `review/round1.md:7`; also identical to `specs/history/spec-v1.md`).
After: 58196 bytes (`wc -c`). Net +433.
Added and deleted bytes come from a character-level diff of the baseline against the revised file, per changed line, so a replaced phrase counts only its changed characters.

| Finding id | Lines changed | Bytes added | Bytes deleted |
|---|---|---|---|
| F1 | 76, 112, 159, 195, 196 | 137 (18 + 65 + 18 + 18 + 18) | 0 |
| F2 | 79 | 87 | 11 |
| F3 | 194 | 223 | 3 |
| Total | 7 lines | 447 | 14 |

Check: 447 - 14 = 433 = 58196 - 57763.

## One row per finding id

| Id | Disposition | Where and what | Cited reason |
|---|---|---|---|
| F1 | Applied (narrowed; the report's "state that load is exempt" option, chosen because it keeps the 10 / 27 / 6 split and the phase counts) | Spec:76 now reads "Every changed command except `/sc:load` also gains the `## Unattended mode` section". Spec:112 (load row, Report column) now reads "none; exempt from the `## Unattended mode` section, AC-1.1 and AC-1.2 (see note)". Spec:159 (P1 scope) now reads "every command in sections 3.1 and 3.2 except `/sc:load`". Spec:195 (AC-1.1) now reads "every command in sections 3.1-3.2 except `/sc:load`". Spec:196 (AC-1.2) now reads "each P1 command except `/sc:load`". The load usage-line fix stays in P1 (spec:159 "load (usage line only)", spec:112 Phase cell), so it still has a phase and SA-4 (spec:149) still matches. | `review/round1.md:38-44` (grading sentence and recommendation). The report allows either deleting load from the P1 list and counts or stating the exemption (`review/round1.md:43`); the exemption removes the contradiction at spec:112/265 vs 159/195/196 with fewer edits and no count change. |
| F2 | Applied (replaced the contradicted sentence) | Spec:79 second sentence "The only command changes are the small fixes in the last column." is replaced by "Phase 1 also adds `--unattended` and the `## Unattended mode` section to each of these commands, besides the small fixes in the last column." Spec:159 and AC-1.1 (spec:195) already require the flag and section on 3.1 commands, so after this edit all four texts agree, including for `brainstorm` and `init-lite` whose small fix is "None" (spec:84, spec:87). | `review/round1.md:46-52` (recommendation quoted at `review/round1.md:49`). The remark in the report's evidence that brainstorm already writes a contract (`review/round1.md:48`) is not a blocking defect and no edit was made for it. |
| F3 | Applied (narrowed AC-0.4; no new mechanism) | Spec:194, pass condition now reads: "steps 1-2 and 5-7 pass; step 3 passes with exactly one `worker_done`, an `--outcome` that follows WC-5 from the command's own report (`failed` if none exists) and the command's existing report file as its report path; step 4 is only `test -s` on that file, since the contract arrives in P1; the P0 briefs omit `--unattended`." This drops the contract-`status` and WC-4-path conditions of 7.2 step 3 (spec:182) and the YAML assertion of step 4 (spec:183) from P0 only, and states that P0 briefs carry no `--unattended` (P0 makes no command edit, spec:158). Spec:73, spec:180-183 are unchanged: the P1-P4 checks still use them as written. | `review/round1.md:52-58` (grading sentence and recommendation). The step-4 wording "only `test -s`" is my reading of "step 4 uses the command's existing report file": the YAML assertion cannot hold for `REPORT.md` or an unfixed adversarial contract, which the report's own evidence says (`review/round1.md:54`). |

## Not done
- No change to spec:73, spec:182-183, the 10 / 27 / 6 counts, section 6 phase counts or the UNVERIFIED list.
- Medium findings that touch the same lines were left alone, for example F12 (flag accepted but not honoured between phases) and F9 (worker duties not in the brief).
- Not re-run: the diff check of the Quantity check in `review/round1.md:188-189` was not repeated; no row was added, removed or moved, and the 27 / 10 / 6 rows are unchanged.
- The spec-panel was not run, as instructed.
