# Revise 2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, edited in place. Prompt: REVISE prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md:60-62`. Input: `review/round2.md` (Reviser brief lists N1 only; `review/verify-2.md` confirmed it per the header of round2.md). Spec-panel not run. No PASS is claimed. The spec's line numbers did not shift.

## Byte accounting

| | bytes |
|---|---|
| Spec before | 58626 |
| Spec after | 58682 |
| Net | +56 |

| Finding id | Added | Deleted |
|---|---|---|
| N1 | 56 | 0 |

## Findings

| id | result | where applied | reasoning |
|---|---|---|---|
| N1 | applied | AC-1.2 at `spec:196`: "each P1 command" became "each P1 command except `load`", plus the clause "(`load` writes no contract, section 3.2)". | `spec:112` and `spec:159` give `load` no `--unattended` flag, no section and no report ("usage line only"), and `spec:265` (Decisions, unchanged) rejects giving it one. So the 7.2 steps 3-4 (`spec:182-183`) cannot pass for it. The fix is one clause, as the recommendation in round2.md asked; no rule or section was added. `load` still gets its usage-line fix under P1. |

## Not done, by rule

Medium and minor findings F1-F6 of round2.md were left alone. `spec:112`, `spec:159`, `spec:182-183` and `spec:265` are unchanged. I read the spec and `round2.md` only; `sk/`, `cmd/` citations stay UNVERIFIED in this sandbox.
