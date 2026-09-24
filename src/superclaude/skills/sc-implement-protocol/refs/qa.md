# Spec-compliance rubric

Loaded for Q3–Q5. Do not load reflect-protocol. Do not re-run the full test suite as the review.

## Reviewer contract

Do not trust the implementer's report.

Input is the task brief (Ti text + AC ids + global constraints) and the diff (`git diff "$start"` vs the Q0 snapshot, or tool-trace paths if `nogit`). Not "the tests passed".

One reviewer vs the brief. Never 2+ reviewer agents per task. No Part 2 code-quality ensemble. No `/sc:reflect`. No 6-agent panel.

## Compare the diff to

- that task's AC (`Ti.ACk`) — for informal/prompt sources this is the source text itself; extra = anything not asked there
- parent spec constraints (`## Constraints` / `## Out of scope` / `## Non-goals` / `## Non-negotiable`)
- explicit instructions on the task ("do not X", "file Y only")

| Label | Meaning |
|-------|---------|
| Missing | AC/instruction not in the diff |
| Extra | behavior/files/API the brief did not ask for |
| Misunderstood | work present but solves the wrong thing |

## Citations

For each AC of Ti, cite either `path:line` in the produced diff **or** `Ti.ACk` (optionally `Ti.ACk@path:line`).

Invalid evidence: `the component works`, `tests pass`, `as implemented above`, line-less paths, citations into files not in this task's touched set unless the AC required reading them (then cite the source spec `path:line`).

A verdict with **zero citations** is invalid → treat as `cannot-verify`.

## Verdict (exactly one)

Closed enum: `compliant` | `missing` | `extra` | `misunderstood` | `cannot-verify`.

No other strings. Not `pass`/`fail`/`issues`. Not `spec-compliant`.

Apply in this order:

1. if zero citations → `cannot-verify`
2. if diff empty and no ruling → `cannot-verify`
3. elif any unmet AC → `missing`
4. elif any misunderstood → `misunderstood` (dominates extra)
5. elif extra_scope nonempty → `extra`
6. else → `compliant`

If both missing and extra: verdict `missing`. Record extra findings on the same ledger line after the verdict.

`cannot-verify` is not a pass. Empty diff after "done" → `cannot-verify`. AC not observable from the diff and no check/log/test added → `cannot-verify`. `nogit` and no written-path list → `cannot-verify`.

## Halt table

| Verdict after Q4 (or after Q5 re-QA) | Action | T{i+1}? |
|---|---|---|
| `compliant` (first QA) | Extras, append `complete` line | Yes |
| non-compliant on first QA | Exactly one fix pass + re-QA | No |
| `compliant` after that one fix | Extras, append `complete` line | Yes |
| still non-compliant after one fix | HALT `E-HALT-QA`. Print ledger path, Ti, verdict, missing citations. Next: `fix` \| `ruling` \| `resume` | No, unless operator Ruling |
| operator Ruling with all three fields | Append Ruling line; then `complete` with **unchanged** non-compliant verdict | Yes |
| `--force` or executor-authored Ruling | STOP `E-NO-RULING` | No |

The executor MUST NOT write the Ruling line. Completing a non-compliant task requires an operator-supplied:

```
T<id>: Ruling: <what> — <why> — <cost-if-wrong>
```

## Isolation (fail the rewrite if violated)

- Reviewer instructions include: `Do not trust the implementer's report.`
- Reviewer input includes the task brief and the diff, not extras results.
- Same verdict schema whether inline or one Task subagent.

## Subagent prompt (when not inline)

Inline when **all** are true: N≤3, source file ≤400 lines, session not compacted. Else one Task. If compacted mid-run, remaining QA uses the subagent. One mode for the rest of the run.

Prompt the subagent with: this file, the task brief, global constraints, the diff (or diff path), start sha. Require the closed verdict + citations. Do not trust the implementer's report.
