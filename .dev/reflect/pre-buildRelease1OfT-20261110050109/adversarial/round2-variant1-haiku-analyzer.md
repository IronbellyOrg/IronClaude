# Round 2 rebuttal: Variant 1 advocate (haiku:analyzer)

Persisted verbatim by the debate-orchestrator from the advocate's returned text.

## Response to criticisms

Citations use the supplied absolute-path files:
- **P:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261110-045742/TASK-WF-buildRelease1OfT-20261110-045742.md`
- **S:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/brainstorms/20261108-132433-orca-observer-mvp/merged-requirements.md`
- **N:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/tuibbs-review/architecture-options.md`

1. **R1-04 — concede the field-suppression remedy, not the entire finding.** N:103 freezes the stage fields, so removing them would break the contract. However, N:77 also explicitly prohibits credentials. Retaining the keys and string types while redacting prohibited content does not remove, rename or retype them. P:45 strips terminal controls, not printable secrets; P:157 exports those strings. The credential-exposure risk is distinct from the wording conflict between P:25 and P:182.

2. **R1-06 — confirmed concession.** It remains **blocking**, as already updated in my Round 1 table. S:172 says the empty variant "must render" the coverage warning; S:385 pins T33. P:75 creates empty data, but P:126 does not assign the required rendering.

3. **R1-01 — accept the stronger citation.** S:369 explicitly requires the cycle to end within 15 seconds. P:97 and P:106 bound individual calls only; P:112 reports an overrun afterward. The finding remains **blocking**, now directly grounded in T5 rather than inference from the plan alone.

4. **R1-02 — accept the narrowing.** S:312 expressly requires `_find_orca()` and its validation probe. Reuse is not the defect. P:23's "only" claim is false against that prescribed discovery behaviour, and P:97/P:105 leave discovery outside the injected runner boundary. Preserve discovery; explicitly accommodate and isolate it in tests.

## Final positions on split points

- **R1-04: narrowed, blocking.** The broad "nothing sensitive printed" wording needs clarification, but weakening that sentence alone does not satisfy N:77's credential prohibition. The remaining finding concerns unprotected free text reaching exports, not proof that credentials have already leaked.
- **QA-09: blocking.** S:352 requires disclosure in **both help and the inspector**. P:173 assigns help disclosure; P:126 and P:142 do not assign the inspector disclosure. P:177 checks option names only. This is a missing required deliverable, not merely an absent assertion or wording nit.

## Assessment of the three missed items

**(a) T16 scenario matrix — holds, blocking.** S:373 requires 27 renders and count/overflow arithmetic. It separately assigns per-owner counts to **T17**. T16 does not require question bodies or per-owner question counts: synthetic worker rows grouped across runs can exercise load and denominators. Therefore P:71's justified exclusion of `uneven` does not exclude T16. P:142 assigns overflow behaviour, but P:146's width checks do not supply the required matrix and arithmetic checks.

**(b) T22 view texts — holds, blocking.** P:82/P:88 build and test model counters and flags. They do not assign their display in P:126 or P:142. S:328 and S:375 require visible duplicate and ordering disclosures. Model correctness is not delivery of the required user-facing warnings.

**(c) Export versus hidden/filtered rows — holds narrowly, minor.** P:126 hides and filters screen rows; P:157 promises "every ledger row." S:189 forbids deleting historical rows from the snapshot. The plan does not explicitly distinguish complete export rows from visible rows, but neither does it instruct deletion. An all-collected-rows invariant and regression test would resolve this; actual data loss is not established.

## Updated per-finding changes

| Finding | Updated position | Change from Round 1 |
|---|---|---|
| R1-02 | Narrowed, blocking | Discovery reuse is required; retain only the false "only" claim and missing injection boundary. |
| R1-04 | Narrowed, blocking | Withdraw whole-field suppression; preserve schema fields while enforcing the prohibited-content boundary. |

Read-only review only; no files changed, commands executed or network used. Runtime behaviour was not checked.
