# Hypothesis: `_check_verdict_field` excludes digit and underscore decorations before `Verdict`

**Agent**: root-cause-analyst
**Tier**: 1
**Timestamp**: 2026-06-12T23:04:28Z
**Cause class**: Regex character-class false negative
**Claim class**: `static_defect`
**Evidence class**: `runtime_repro`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: conflicts

## Claim

`_check_verdict_field` rejects `1. Verdict: PASS` and `__Verdict__: PASS` because its markdown regex treats every character before and around `Verdict` as decoration only if it is not `\w`. In Python regex semantics, digits and underscores are word characters, so the current `[^^\w\n:]*`-style decoration class stops before `1` and `_` instead of reaching the `Verdict` label. This is a code defect, not a documentation-only issue: the local contract already says agents decorate verdict lines freely and documentation context supports accepting markdown verdicts while preserving the required colon and uppercase `PASS|FAIL` value.

## Evidence

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:47` — `_check_verdict_field` documents the markdown branch as accepting decorated verdict lines: `# Markdown format (case-insensitive key, case-sensitive value). Agents`.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:52` — the comment defines decoration as `any run of non-word / non-colon decoration (``[^\w\n:]*`` -> bullets,`.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:62` — the active markdown regex is `r"(?:^|\n)[^\w\n:]*(?i:verdict)[^\w\n:]*:[^\w\n:]*(PASS|FAIL)(?!\w)"`, so digits in an ordered-list marker and underscores in `__Verdict__` are excluded before the label can match.
- Command from `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/tier1-observation.md:13`: `cd /config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473 && uv run python -c 'from superclaude.cli.prd.gates import _check_verdict_field; cases=["1. Verdict: PASS","__Verdict__: PASS","Verdict: PASS","**Verdict**: PASS"]; print({c: _check_verdict_field(c) for c in cases})'` → `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/tier1-observation.md:18` shows `{'1. Verdict: PASS': "No verdict field found (expected 'verdict: PASS' or 'verdict: FAIL')", '__Verdict__: PASS': "No verdict field found (expected 'verdict: PASS' or 'verdict: FAIL')", 'Verdict: PASS': True, '**Verdict**: PASS': True}`.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:140` through `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:145` cover bullets, headings, emoji, and bold values, but not ordered-list prefixes or underscore emphasis.

## Proposed Fix

Replace the markdown verdict regex with a line-anchored pattern that allows explicit markdown line prefixes and label wrappers instead of using `[^\w\n:]*` as a generic decoration class around `Verdict`. The replacement should continue to require a colon, preserve case-sensitive `PASS|FAIL`, preserve the `(?!\w)` value boundary, and preserve the existing invalid-shape protections for `Verdict PASS`, `Verdict::: PASS`, `PASSING`, and rationale headings without a value.

- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py` — update `_check_verdict_field`'s markdown regex and adjacent comment so ordered-list markers such as `1. ` and underscore emphasis such as `__Verdict__` are valid label decoration.
- `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py` — add accepted-shape cases for `1. Verdict: PASS`, `1. __Verdict__: PASS`, and `__Verdict__: PASS`; keep the existing invalid-shape parametrization as regression coverage.

Proof test: run `uv run pytest /config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py::TestCheckVerdictField -v` after the fix, plus the inline reproducer from the observation card.

## Confidence

Self-reported confidence: 0.96

Per-dimension self-assessment:
- Evidence grounding: 1.0 — The active regex, comments, reproducer output, and missing test shapes are all cited from current files or captured command output.
- Runtime check: 1.0 — `claim_class=static_defect` with `evidence_class=runtime_repro`; the observation card captured an executed UV reproducer that returns the reported false negatives.
- Symptom coverage: 1.0 — The `\w` exclusion explains both reported cases: `1` in numbered lists and `_` in underscore emphasis.
- Reproducibility fit: 1.0 — The reproducer deterministically returns the gate failure string for both reported inputs on PR head `65bac7ed3b267faabcf3ea7844a6fd0cd412e97b`.
- Fix directness: 1.0 — The fix is localized to one regex/comment and targeted unit cases for the missing markdown shapes.
- Domain coherence: 1.0 — Single-domain parser/regex false negative; no environment, performance, security, or multi-component dependency.

## Risks

A too-broad regex could reintroduce false positives that the current tests intentionally reject, especially `Verdict PASS`, `Verdict::: PASS`, `Verdict: PASSING`, and a `Verdict rationale` heading without a value. The fix should avoid returning to arbitrary prose matching by keeping the match line-anchored and preserving the required colon and exact uppercase `PASS|FAIL` value.

## If I'm wrong, it's probably because...

The only likely alternative is that PRD QA outputs intentionally disallow ordered-list markers and underscore emphasis, but the documentation context and existing comments point the other way.

## Falsification standard

This hypothesis is wrong if, after changing only the regex to permit ordered-list prefixes and underscore label emphasis while preserving strict colon/value semantics, the inline reproducer still returns the gate failure string for `1. Verdict: PASS` or `__Verdict__: PASS`, or existing invalid-shape tests begin to pass incorrectly.

## Evidence classification [V2 merged]

- **Claim class**: `static_defect` — The defect is a regex literal and its documented character-class semantics.
- **Evidence class**: `runtime_repro` — The observation card contains an executed UV reproducer with captured output for the reported inputs.
- **Runtime check performed?**: yes — The captured command output in `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/tier1-observation.md:18` shows the two false negatives.
- **If REFUTE verdict, coverage statement**: Not applicable — verdict direction is AFFIRM.

## Alternatives considered

- Test gap only — rejected because the reproducer shows production code currently returns the gate failure string for the reported inputs; tests are missing coverage but are not the root cause.
- Documentation mismatch — rejected because `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/doc-context.md:31` says markdown verdicts with PASS/FAIL are supported while preserving strict colon/value semantics, and line 32 says the bug is implementation excluding word-character decorations.
- JSON parsing path issue — rejected because the failing examples are markdown lines and the JSON branch is bypassed before the markdown regex.

## Grounding gaps

No source edits or post-fix tests were run in this wave because the requested output is a hypothesis card only. The exact replacement regex should be validated against both the new ordered-list/underscore cases and the existing invalid-shape cases before remediation is accepted. Diagnosability verdict is sufficient; `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/diagnosability-context.md:29` classifies this as deterministic source plus reproducer evidence, with no additional instrumentation required.
