---
status: success
tier_reached: 1
confidence: 0.95
escalation_reason: none
---

# Troubleshoot Report — PR #154 / #153 Review Comments

## Summary

Four Augment review findings across two open PRs were diagnosed. All four are
confirmed real and high-confidence. Two (Issues 1-2) live on the current branch
`fix/prd-parallel-gate-final-phase-exempt` (PR #154). Two (Issues 3-4) live on a
**different** branch `fix/task-builder-post-reflect-diff-base` (PR #153) and
cannot be fixed from the current checkout without switching branches. Issue 1 is
a genuine logic bug (substring false-negative); the other three are
documentation-accuracy issues.

## Targets

| # | PR | Sev | Location | Root cause |
|---|----|----|----------|-----------|
| 1 | 154 | medium | `src/superclaude/cli/prd/gates.py:211-245` | bare substring `in` match: `"complete"` ⊂ `"incomplete"` exempts a real work phase |
| 2 | 154 | low | `tests/cli/prd/test_gates.py:154` | stale class docstring `"phases 2-5"` |
| 3 | 153 | medium | `src/superclaude/skills/task-builder/SKILL.md:2195` | `git diff <ref>` omits untracked files; "whether or not they were committed" overclaims |
| 4 | 153 | medium | `src/superclaude/skills/task-builder/SKILL.md:2195` | hardcoded `origin/master` integration-branch default wrong for `integration`/`origin/main` repos |

---

## Issue 1 — substring false-negative in completion-phase exemption (medium)

### Diagnosis
`gates.py:244` exempts the final phase from the parallel-instructions check when
its heading contains any `completion_signals` entry, tested via
`any(sig in heading_line for sig in completion_signals)`. Because `"complete"`
is a substring of `"incomplete"` (and `"present"` ⊂ `"representation"`), a real
work phase whose heading happens to contain those letters is silently exempted —
a false negative on exactly the max-numbered phase where the check matters most.

### Evidence
- `src/superclaude/cli/prd/gates.py:211-219` — `completion_signals` list incl. `"present"`, `"complete"`.
- `src/superclaude/cli/prd/gates.py:244` — `if any(sig in heading_line for sig in completion_signals):`
- Empirical repro (uv run): heading `## Phase 7: Incomplete Work Review` → OLD exempts (`True`), should be checked.

### Proposed fix
Anchor each signal at a word boundary. Replace the bare `in` test with a
`\b`-prefixed regex search:

```python
if any(re.search(r"\b" + re.escape(sig), heading_line) for sig in completion_signals):
```

Verified empirically: `\bcomplete` does NOT match `incomplete` (no boundary
between `n` and `c`) but DOES match `complete`/`completion`; `\bpresent` rejects
`representation` but accepts `present`/`presentation`/`presents`. Genuine
completion headings (`Completion & Sign-off`, `Finalize and wrap up`) still
exempt — zero regression in the 6-case check.

### Regression test
Add a case to `TestCheckParallelInstructions`: a final phase titled
`## Phase 7: Incomplete ...` with no parallel keywords must return an error
string (NOT be exempted).

---

## Issue 2 — stale class docstring (low)

### Diagnosis
`TestCheckParallelInstructions.__doc__` at `tests/cli/prd/test_gates.py:154`
reads `"""Validate parallel keywords in phases 2-5."""`. After PR #154 the gate
checks phases `>=2` with a final-completion-phase exemption — not "2-5".

### Evidence
- `tests/cli/prd/test_gates.py:154` — `"""Validate parallel keywords in phases 2-5."""`
- `src/superclaude/cli/prd/gates.py:198` — docstring now reads "work phases (>=2)".

### Proposed fix
Update to: `"""Validate parallel keywords in work phases (>=2), with the final
completion phase exempt."""`

---

## Issue 3 — untracked files omitted by `git diff <ref>` (medium) — PR #153 branch

### Diagnosis
SKILL.md:2195 instructs passing `<BASE>` as a single ref so reflect diffs it
against the working tree, "this captures the task's changes whether or not they
were committed." `git diff <ref>` shows tracked modifications (staged + unstaged)
but NOT brand-new **untracked** files (never `git add`-ed). A `/task` run that
creates new files leaves them invisible to the audit unless reflect separately
runs `git status --porcelain` / `git diff --no-index` for untracked paths.

### Evidence
- `git show origin/fix/task-builder-post-reflect-diff-base:.../SKILL.md` line 2195 (verbatim claim).
- Behavior: `git diff <ref>` excludes untracked files by design (no `--include-untracked` exists for plain `git diff`).

### Proposed fix (doc clarification)
Soften the overclaim and name the gap. e.g.:
"...captures the task's changes whether committed or left unstaged in the working
tree. (Brand-new **untracked** files are not shown by `git diff` alone; reflect
additionally enumerates untracked task artifacts via `git status --porcelain`.)"
— wording to be confirmed against actual `/sc:reflect` untracked-handling.

---

## Issue 4 — hardcoded `origin/master` integration-branch default (medium) — PR #153 branch

### Diagnosis
SKILL.md:2195 computes `<BASE>` as `git merge-base HEAD <integration-branch>`
with `<integration-branch>` defaulting to `origin/master` (fallback `main`/
`master`). Repos whose integration branch is `integration`, or whose remote
default is `origin/main`, get a wrong merge-base → skewed audit scope.

### Evidence
- `git show origin/fix/task-builder-post-reflect-diff-base:.../SKILL.md` line 2195 (default `origin/master`).
- This repo itself documents `integration` as a real branch tier (CLAUDE.md "Git Workflow").

### Proposed fix (doc clarification)
Make the default derivation dynamic rather than a hardcoded literal, e.g.:
"`<integration-branch>` defaults to the repo's actual default branch — resolve
via `git symbolic-ref refs/remotes/origin/HEAD` (or `gh repo view
--json defaultBranchRef`), falling back to `origin/main`/`origin/master`. When
the project uses a named integration branch (e.g. `integration`), pass it
explicitly." — wording to be confirmed.

---

## Risk + Rollback
- Issue 1: regex change is behavior-narrowing (exempts strictly fewer phases) → only effect is *more* checking, never less. Low risk. Covered by new + existing tests.
- Issues 2-4: documentation/test-docstring only, no runtime behavior change.

## Next Steps
- Issues 1-2 are applyable on the current branch now.
- Issues 3-4 require checkout of `fix/task-builder-post-reflect-diff-base` (PR #153) — separate commit/PR.
- After edits on the current branch: `make sync-dev` is NOT required (gates.py is package source, test is test source; no `.claude/` mirror). Run `uv run pytest tests/cli/prd/test_gates.py -v`.
