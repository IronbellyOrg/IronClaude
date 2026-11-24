# Tier 1 pre-execution reflection card

## Summary

The proposed change is narrowly limited to human-facing help, plus public-root regression tests. Current source still contains the unsupported option in the validate-lenses docstring and scaffold option help; the command reference instead identifies the JobSpec field. The plan is not an applied fix. Independent source-to-task mapping is recorded separately in coverage-matrix.md; review findings remain subject to blind calibration, Tier 2 comparison and evidence validation.

## Coverage and acceptance

Coverage-matrix.md records 0 parsed requirements, 12 quote-pinned inferred requirements and 4 tasks. Literal containment maps 6/12 (coverage_pct_union=0.5, S_dev_density=0.5); parsed-only coverage is null. Semantically the scope constraints are in the plan's Constraints section, which the single-task matcher excludes. No lexical mismatch is silently relabelled covered. The source's sparse labeling mandates Tier 2 regardless of confidence. Tasks 1/2 require expected red help failures and an unchanged parser guard, Task 3 corrects validate-lenses, and Task 4 corrects scaffold with final repaired-surface captures and executor-owned independent review. The historic repair blockers remain open until those future checks actually occur.

## Grounded risks and scope

The two public producers are the `validate_lenses_cmd` docstring and the `scaffold_cmd` lens-option help in `src/superclaude/cli/swarm/commands.py`; they are registered by `swarm_group.add_command` in `src/superclaude/cli/swarm/__init__.py`. The plan changes no registration or parser option.

The current `_apply_custom_prompt_dir` in `preflight.py` gates directory reading on lens custom and a nonempty field. `_custom_prompt_dir_lens_failures` in `schema.py` explicitly allows inline custom prompts without a directory. Plan constraints and Tasks 3/4 preserve these semantics, injection guards and metadata rules.

Risk checks: public help must be observed through root `main`, not only source assertions; parser rejection must remain exit 2; red failures must be actual contract failures, not missing imports; wording must not make directories mandatory for inline custom specs; historical diagnostic status must not be relabelled passed; intentional red checkpoints must be interpreted against each task's acceptance criteria rather than as a claim of a green suite. These are plan-level checks, not claims that future tests have passed.

## Findings

T1 provisional verdict: PASS, no blocking finding in the checked plan/source scope. This is not an independent final approval: the producing context assembled this card, the coverage analyst's received verdict is PASS/no blockers, and the final decision requires fresh Tier 2 readers plus evidence validation. Six literal unmapped rows remain visible as algorithm outputs, with semantic coverage in global Constraints or multi-task acceptance. The reviewer must decide whether any is a real missing obligation rather than accept semantic coverage by assertion.

No tests or public commands have run in this review, no applied-fix correctness is claimed, and historical repaired-state closure remains blocked.

## Recommendation

Proceed only to the mandatory Tier 2 plan review, not implementation. Ask fresh readers to adjudicate the six lexical nonmatches and the coverage reviewer's nonblocking candidates: optional exact review-report filename, possible help-token wrapping (unverified) and already excluded directory placeholders. The plan itself remains immutable. A plan-review PASS would permit a later approval decision, not prove the bug repaired or authorize source/test edits.
