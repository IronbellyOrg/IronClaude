# Revise 2 (REVISE prompt, ids R2-1)

candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md. Inputs read: review/round2.md (Reviser brief, round2.md:94-99), the spec, README.md. Prompt: ~/.claude/rules/prompts/document_review_loop_prompts.md:60-62. Spec-panel not run; no PASS awarded.

## Byte accounting
- Size before: 59220 bytes. Size after: 59444 bytes. Net +224.
- R2-1 (only id): edit A (WC-4, spec line 62) deleted 51, added 208 (net +157); edit B (section 3.1, spec line 79) deleted 79, added 146 (net +67). Total deleted 130, added 354, net +224.

(The additions are wording replacing "always" / "Every brief"; the sentences are narrowed by a phase condition, nothing else is added.)

## Findings
| id | disposition | where | reason |
|---|---|---|---|
| R2-1 | applied | spec:62 (WC-4): "the brief always passes" became "the brief passes from the phase that adds it (the Phase column of each row in section 3; before that phase the brief omits it and the worker reports the row's existing report file)". spec:79 (3.1): "Every brief also passes ..." became "From the phase that adds them, the brief also passes `--unattended --report-dir <dir>` ...; a brief before that phase omits them." | Follows the recommendation at round2.md:71. Now consistent with spec:158 (P0, no command edits), spec:192 (AC-0.4, step 4 uses the existing report file) and spec:154/159 (flags added only in the row's phase). |

## Not touched (outside the blocking ids)
- spec:73 (2.3) still says the brief states the exact command line including `--unattended` and the `--report-dir` directory; round2.md:96 limits edits to lines 62 and 79, so it was left. It reads against the same phase rule and may deserve a follow-up note (Medium, not actioned).
- R2-M1 to R2-M4 and the two minor notes: left alone per the REVISE prompt (round2.md:90-92).
