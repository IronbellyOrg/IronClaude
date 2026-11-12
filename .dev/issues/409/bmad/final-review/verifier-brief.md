# Brief for the step-5 fresh-context verifier (orca-observer)

ROOT = /home/coder/workspaces/worktrees/Coder/dashboard-bmad
FR = ROOT/_bmad-output/planning-artifacts/orca-observer/final-review

You did not write any of this. Assume the fixes are wrong until the text proves otherwise. Read `FR/reviewer-brief.md` first (artifacts, source ranking, binding owner decisions, grading rule).

## Your job

1. Your task names the REVIEW number and the INPUTS: the graded findings (`FR/graded/*.json`), the fix results for the cycle (`FR/fixes/cycle<N>-*.json`) and, for review 3, the previous verification.
2. For EVERY BLOCKING finding in scope: read the current text at the fixed location, the other side, and the source of truth. Decide `FIXED` (the defect is gone and the text is correct against its source) or `OPEN` (still wrong, wrongly fixed, or skipped without a valid reason). A `skipped` result is FIXED only when the skip reason is correct (for example the fix would resolve an open owner question) AND the documents still state the question and its default consistently; otherwise OPEN.
3. Regression check: for each changed file, read the changed passages (the fix results list them) and look for new defects the fixes introduced: new contradictions with another artifact or a source, a resolved owner question, a dropped evidence label, unknown shown as zero or false, an invented Orca field, broken references. Each real one is a NEW BLOCKING item.
4. Confirm `ROOT/_bmad-output/specs/spec-orca-observer/ARCHITECTURE-SPINE.md` is byte-identical to `ROOT/_bmad-output/planning-artifacts/orca-observer/architecture/ARCHITECTURE-SPINE.md` (`cmp`); a difference is a NEW BLOCKING item.
5. Minor issues: list them under `minor_notes`; they never fail the verdict.

## Rules

- READ ONLY. Write exactly one file: the output path in your task. No git, no network. Read in ranges of at most 150 lines; grep -n first.

## Output (JSON, write once, complete)

`{"verifier": "...", "review": N, "verdict": "PASS|FAIL", "self_audit": "what you checked", "items": [{"id": "...", "status": "FIXED|OPEN", "location": "path:line", "evidence": "quote <= 30 words", "reason": "one sentence", "fix_in": "path or null", "fix": "for OPEN only: one or two exact sentences"}], "new_blocking": [{"id": "NEW-..", "location": "path:line", "other_side": "path:line or null", "finding": "...", "evidence": "...", "fix_in": "...", "fix": "..."}], "minor_notes": ["..."], "counts": {"fixed": 0, "open": 0, "new_blocking": 0}}`

verdict PASS only when open = 0 and new_blocking = 0. Final reply (and nothing else): the output path, then 3 lines: verdict; counts fixed/open/new; the worst remaining item.
