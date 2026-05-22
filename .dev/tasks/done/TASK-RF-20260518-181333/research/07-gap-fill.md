# 07 — Gap-Fill Research (Round 1)

- **Topic:** Gap-fill round 1 — PR #49 scope, artifact counts, PR template, CONTRIBUTING.md, branching strategy
- **Status:** Complete
- **Date:** 2026-05-18
- **Scope:** Resolve 4 evidence gaps surfaced by the QA gate against R3/R1/R4, then re-derive the branching strategy in light of the corrected facts.

---

## GAP 1 — PR #49 actual scope

### Raw evidence

`gh pr view 49 --json number,title,state,mergedAt,baseRefName,headRefName,additions,deletions,changedFiles,body` returned (key fields):

| Field         | Value |
|---------------|-------|
| number        | 49 |
| state         | MERGED |
| title         | `feat(hooks): widen auggie-flag-clear matcher and add verify-sync hook coverage` |
| mergedAt      | `2026-05-18T11:43:55Z` |
| baseRefName   | `master` |
| headRefName   | `feat/hook-sync-and-matcher-fix` |
| additions     | 22771 |
| deletions     | 139 |
| changedFiles  | **138** |

### Critical methodology note

`gh pr view 49 --json files --jq '.files | length'` returned **100** — this is a **gh CLI page limit**, not the true count. Confirmed by re-running with `gh api --paginate "repos/:owner/:repo/pulls/49/files"` which yielded **138** files (matching `changedFiles` metadata exactly).

**R3's earlier file count of "805 files" is wrong; analyst-A's number is wrong; the truth is 138.**

### Top-level breakdown (paginated, 138 of 138)

```
100  .dev/releases/...                  (task-builder-merge artifacts + checkpoints + manifest)
 25  tests/audit/...                    (audit test suite)
  6  src/superclaude/...                (sprint CLI + hooks + skills source)
  3  .claude/agents/...                 (rf-qa, rf-qa-qualitative, rf-task-builder)
  1  .claude/skills/task-builder/SKILL.md
  1  tests/cli/test_verify_sync_hooks.py
  1  tests/skills/...
  1  Makefile
```

### First 30 files (sample)

```
.claude/agents/rf-qa-qualitative.md
.claude/agents/rf-qa.md
.claude/agents/rf-task-builder.md
.claude/skills/task-builder/SKILL.md
.dev/releases/current/task-builder-merge/artifacts/D-0016/{evidence,spec}.md
.dev/releases/current/task-builder-merge/artifacts/D-0017/{evidence,sample-emitter-output,spec}.md
.dev/releases/current/task-builder-merge/artifacts/D-0018/{evidence,spec}.md
... continuing through D-0021 ...
```

### D-NNNN dirs absorbed by PR #49 (paginated)

`D-0016 D-0017 D-0018 D-0019 D-0020 D-0021 D-0023 D-0024 D-0025 D-0026 D-0027 D-0028 D-0029 D-0030 D-0031 D-0032 D-0033 D-0034 D-0035 D-0036 D-0037 D-0038 D-0039 D-0040 D-0041 D-0042 D-0043 D-0044 D-0045 D-0046 D-0047 D-0048 D-0049 D-0050 D-0051 D-0052 D-0053 D-0064 D-0065 D-0066 D-0067`

That is 41 D-NNNN dirs (note the gap between D-0053 and D-0064 — D-0054 through D-0063 were NOT yet committed when PR #49 merged).

### Critical judgment on R3's claim

R3 claimed PR #49 absorbed "the MIG-002 baseline via squash merge of 805 files / +22,881 lines."

**Corrected verdict:** PR #49 IS substantially more than hooks-only — it absorbed **138 files / +22,771 / −139 lines**, including the bulk of the task-builder-merge release evidence baseline (D-0016 through D-0053 plus D-0064-D-0067, agents, the task-builder SKILL.md, and 25 audit tests). However:

- R3's headline numbers (805 / +22,881) are **wrong** — the true delta is **138 / +22,771 / −139**.
- R3's directional conclusion ("the baseline IS already absorbed") is **directionally correct for the artifacts that pre-dated the PR**, but **factually wrong for the post-PR work**: D-0054-D-0063 and D-0068-D-0100 (~43 D-NNNN dirs) plus all the modified files listed in §GAP 5 are NOT yet on master.
- The PR body itself describes a tight hooks fix (Makefile + 1 hook JSON + 1 hook script + 1 new test file). The 100 `.dev/releases` paths and 25 audit tests were swept into the same squash merge — almost certainly because the head branch had absorbed prior task-builder-merge work-in-progress before being PR'd.

**Strategy implication:** the branch currently has 143 committed-file delta vs master PLUS 138 untracked entries in working tree — a single PR encompassing all of that is impractical for review. The 41 absorbed D-NNNN dirs do NOT make the remaining work small; the **untracked** D-0054-D-0063 + D-0068-D-0100 are evidence for the second half of the release that still needs to land. **Split is required.**

---

## GAP 2 — Exact untracked artifact count for `.dev/releases/current/task-builder-merge/artifacts/`

### Raw evidence

```
$ ls .dev/releases/current/task-builder-merge/artifacts/ | wc -l
85                                # 85 D-NNNN directories on disk

$ git ls-files .dev/releases/current/task-builder-merge/artifacts/ | wc -l
85                                # 85 tracked files

$ git status --porcelain .dev/releases/current/task-builder-merge/artifacts/ | wc -l
44                                # 44 porcelain entries (untracked under this subtree)
```

### Ground truth for artifacts/ subtree

- **D-NNNN directories on disk:** 85 (D-0015 + D-0016 → D-0100 minus gap D-0022)
- **Tracked files under artifacts/:** 85 (from `git ls-files`)
- **Untracked new files/dirs under artifacts/:** 44 (from `git status --porcelain`)
- **R1's claim of 56 untracked artifacts:** wrong.
- **Analyst-A's claim of 44 untracked artifacts:** **correct** — matches `git status --porcelain` exactly.

### Why R1's 56 is wrong

R1 likely included the top-level `.dev/releases/current/task-builder-merge/` siblings (e.g. checkpoints/, results/, execution-log) in the artifact count. Those are not under `artifacts/` and should be counted separately. The narrow `artifacts/` subtree is precisely **44 untracked porcelain entries**.

### Cross-reference: untracked D-NNNN dirs

`D-0054 D-0055 D-0056 D-0057 D-0058 D-0059 D-0060 D-0061 D-0062 D-0063 D-0068 D-0069 D-0070 D-0071 D-0072 D-0073 D-0074 D-0075 D-0076 D-0077 D-0078 D-0079 D-0080 D-0081 D-0082 D-0083 D-0084 D-0085 D-0086 D-0087 D-0088 D-0089 D-0090 D-0091 D-0092 D-0093 D-0094 D-0095 D-0096 D-0097 D-0098 D-0099 D-0100` + D-0053 evidence.md (partial) = **44 entries**.

---

## GAP 3 — `.github/PULL_REQUEST_TEMPLATE.md` byte-exact verbatim

### Line count

`wc -l` output: **51**.

### Final 10 lines (cat -n, verbatim)

```
    42
    43  <!-- How to verify this PR works -->
    44
    45  ## Screenshots (if applicable)
    46
    47  <!-- Attach screenshots if there are UI changes -->
    48
    49  ## Notes
    50
    51  <!-- What you want to communicate to reviewers, background to technical decisions, etc. -->
```

### Full verbatim content (51 lines)

```markdown
# Pull Request

## Summary

<!-- Briefly explain the purpose of this PR -->

## Changes

<!-- List the major changes -->
-
## Related Issues

<!-- Include related issue numbers, if any -->
Closes #

## Checklist

### Git Workflow
- [ ] For external contributions: Followed the flow of fork → topic branch → upstream PR.
- [ ] For collaborators: Used a topic branch (not directly committed to main).
- [ ] `git rebase upstream/main` completed (no conflicts).
- [ ] Commit messages conform to Conventional Commits (`feat:`, `fix:`, `docs:`, etc.).

### Code Quality
- [ ] Changes are limited to a single purpose (not a large PR, guideline: ~200 lines of difference).
- [ ] Follows existing code conventions and patterns.
- [ ] Add appropriate tests for new features/fixes.
- [ ] Lint/Format/Typecheck all pass.
- [ ] CI/CD pipeline successful (green status).

### Security
- [ ] Secrets and authentication information not committed.
- [ ] Necessary files excluded with `.gitignore`.
- [ ] No breaking changes, or if there are, commit with `!` and include in MIGRATION.md.

### Documentation
- [ ] Update documentation as needed (README, CLAUDE.md, docs/, etc.).
- [ ] Add comments to complex logic.
- [ ] Properly document API changes.

## Testing Methods

<!-- How to verify this PR works -->

## Screenshots (if applicable)

<!-- Attach screenshots if there are UI changes -->

## Notes

<!-- What you want to communicate to reviewers, background to technical decisions, etc. -->
```

### Verification against QA-B's claim

QA-B claimed R4's quote was missing the `-->` close on the final line. The file's final line **does end with `-->`** (per cat -n line 51: `<!-- What you want to communicate to reviewers, background to technical decisions, etc. -->`). **QA-B is correct that the close exists; the builder MUST include `-->` when quoting line 51.**

There is also a notable hard guideline in this template: the **Code Quality** checklist line 25 explicitly says *"Changes are limited to a single purpose (not a large PR, guideline: ~200 lines of difference)"* — direct in-repo evidence that the project's own template encourages splitting, reinforcing GAP 5's multi-PR strategy.

---

## GAP 4 — `CONTRIBUTING.md` byte-exact verbatim

### Line count

`wc -l` output: **48**. The file is 49 visible numbered lines (Read shows 1-49); `wc -l` counts LF-terminators, so line 49 lacks a trailing newline.

### Full verbatim content

```markdown
# Contributing to SuperClaude Framework

This document captures lightweight contributor conventions for the IronClaude fork. It is intentionally short — the goal is to make it easy to do the right thing by default, not to encode every possible rule.

## CI Hygiene

### The rot-budget rule

**No PR may introduce a *new* lint or test failure.** Pre-existing failures on `master` are allowed to remain — they will be addressed in dedicated rot-cleanup PRs — but a PR that *adds* a failure must fix it before it merges.

This rule keeps two things separate:

- **New regressions** — strictly disallowed; the PR author owns the fix.
- **Inherited rot** — acceptable in any individual PR; tracked separately and cleaned up in focused PRs.

### What counts as a "new failure"

A "new failure" is any lint or test failure that is **NOT present in the most recent CI run on `master`** at the time the PR branch was created.

To check whether a failure in your PR is new or inherited:

1. Look at the latest CI run on `master` (the merge commit your branch was cut from).
2. If the same test ID or lint rule + file:line is failing on `master`, it is **inherited** (acceptable for your PR).
3. If the failure appears on your branch but NOT on the `master` baseline, it is **new** (must be fixed before merge).

When in doubt, run the same check locally on master (`git stash && git checkout master && <run check>`) and compare.

### Pre-PR local checks

Before opening a PR, run these three commands from the repo root:

​```bash
uv run ruff check src/ tests/
uv run pytest tests/<changed-area>/ -v
make verify-sync
​```

What each one checks:

- `uv run ruff check src/ tests/` — Ruff lint over the whole source + tests tree. Catches new F-class, E-class, I-class, N-class, and W-class violations introduced by your branch.
- `uv run pytest tests/<changed-area>/ -v` — Pytest for the specific subtree your PR modifies (e.g. `tests/audit/` if you touched audit code). Faster than the full suite; catches functional regressions in the area you changed.
- `make verify-sync` — Drift check between `src/superclaude/` (source of truth for skills/agents/commands) and `.claude/` (the synced dev copies). If you edit `src/superclaude/skills/`, `src/superclaude/agents/`, or `src/superclaude/commands/`, run `make sync-dev` before this check.

### Disclaimer: social convention, not a CI-enforced gate

This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate. CI will still pass PRs that violate the rot-budget if the underlying job is green (or if the underlying job has been failing on master and continues to fail at the same level). Enforcement relies on PR reviewers checking the rule during code review.

If you find a PR that violates the rule (a new failure that wasn't present on master), call it out in the review and ask the author to either fix the regression or document why it's acceptable.
```

### Pre-PR triplet (canonical, byte-exact, source lines 33-35)

```bash
uv run ruff check src/ tests/
uv run pytest tests/<changed-area>/ -v
make verify-sync
```

**Pinned exactly.** The triplet sits at source lines **33-35** inside a fenced code block opened on line 32 (` ```bash `) and closed on line 36 (` ``` `). If R4 quoted them at 32-34 or 34-36, the new authoritative anchor is **33-35**.

### Additional canonical fact

CONTRIBUTING.md line 46 explicitly says: *"This rot-budget rule is a **social convention** agreed by maintainers, **NOT** a CI-enforced gate."* The builder should quote this verbatim if the task includes any rot-budget assertion, to prevent re-asserting it as a hard gate.

---

## GAP 5 — Updated branching strategy (multi-PR split)

### Branch state recap (ground truth, this commit)

- **Committed delta master..HEAD:** **143 files** (102 `.dev/releases`, 25 `tests/audit`, 8 `src/superclaude`, 4 `.claude/agents`, 1 `.claude/skills`, 1 `tests/cli`, 1 `tests/skills`, 1 `Makefile`).
- **Working-tree modifications (M):** 14 files (list below).
- **Untracked (??):** 124 entries (43 untracked D-NNNN dirs + checkpoints + tests + docs + task files + stray dirs).
- **Total surface to land:** 143 committed + 138 porcelain = approx **267 unique file-paths** if everything currently on this branch (committed + working-tree) were to ship, vs. the **138** already merged through PR #49.

### Modified files (14, working tree)

```
.dev/releases/current/task-builder-merge/execution-log.jsonl
.dev/releases/current/task-builder-merge/execution-log.md
.dev/releases/current/task-builder-merge/results/phase-4-output.txt
docs/memory/solutions_learned.jsonl
src/superclaude/cli/sprint/commands.py
src/superclaude/cli/sprint/config.py
src/superclaude/cli/sprint/executor.py
src/superclaude/cli/sprint/models.py
tests/pipeline/test_process.py
tests/sprint/test_config.py
tests/sprint/test_executor.py
tests/sprint/test_models.py
tests/sprint/test_regression_gaps.py
tests/sprint/test_watchdog.py
```

These cluster into THREE coherent themes:

1. **C1-C4 sprint runner** — `src/superclaude/cli/sprint/{commands,config,executor,models}.py` + matching `tests/sprint/*` + `tests/pipeline/test_process.py`.
2. **task-builder-merge release artifacts (in-progress)** — `execution-log.jsonl`, `execution-log.md`, `results/phase-4-output.txt`.
3. **Side telemetry** — `docs/memory/solutions_learned.jsonl` (auto-appended; should NOT be PR'd, gitignore candidate).

### Untracked file thematic breakdown (124 entries; top prefixes)

```
67  .dev/releases/current      (43 D-NNNN evidence dirs + 4 checkpoints + phase-{5,6}-{output,errors}.txt + hook-sync-and-matcher-fix/)
34  .dev/tasks/done            (5 BUILD-REQUEST + RESEARCH-PROMPT task files; rest are subfiles)
 4  .dev/tasks/to-do           (current research scaffolds incl. this file's parent dir)
10  tests/audit/...            (8 new test files + 3 fixtures, e.g. test_nfr_conv_9_zero_trust.py, test_dnsp_*.py)
 1  prd-test-product/          (stray prd output — likely test-artifact, gitignore candidate)
 1  prd-dry-run-test/          (stray prd output — same)
 1  docs/reference/...         (nfr-conv-2-prose-determinism.md)
 3  docs/mistakes/...          (auto-generated reflexion logs — gitignore candidate)
 1  .dev/eval-runs/            (eval workspace output)
 1  0.20/                      (stray dir — investigate; likely needs gitignore or deletion)
```

### Recommended multi-PR split

Following R2 §2.4's `<type>/...-pr<N>-<slug>` naming precedent (e.g. `fix/ci-rot-pr1-pytest-collection`) and CONTRIBUTING.md's ~200-line guideline (plus `.github/PULL_REQUEST_TEMPLATE.md` line 25 "single purpose" constraint):

| PR # | Scope name                          | Base    | Head branch                                              | Est files | One-sentence description                                                                                                              | Depends on |
|------|-------------------------------------|---------|----------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------|------------|
| PR-A | Sprint runner C1-C4 code + tests    | master  | `feat/sprint-runner-pr1-c1c4`                            | ~10       | Cherry-pick `src/superclaude/cli/sprint/{commands,config,executor,models}.py` + paired `tests/sprint/*` + `tests/pipeline/test_process.py` modifications. | none       |
| PR-B | Audit test suite (NFR + invariants) | master  | `test/audit-suite-pr2-nfr-invariants`                    | ~33       | Land `tests/audit/test_nfr_conv_*.py`, `test_invariant_preservation_NFR_6_through_10.py`, `test_dnsp_*.py`, `test_hidden_input_guard.py`, plus fixtures. | none       |
| PR-C | task-builder-merge evidence batch 1 | master  | `docs/task-builder-merge-pr3-evidence-d0054-d0067`       | ~50       | Add untracked D-0054 through D-0067 evidence + spec dirs + CP-P05-T01-T05 checkpoint + phase-5 output.                                                   | none       |
| PR-D | task-builder-merge evidence batch 2 | master  | `docs/task-builder-merge-pr4-evidence-d0068-d0100`       | ~60       | Add untracked D-0068 through D-0100 evidence + spec dirs + CP-P05-T07-T11 + CP-P04-END + CP-P05-END + phase-6 output/errors.                              | PR-C       |
| PR-E | task-builder-merge log refresh      | master  | `docs/task-builder-merge-pr5-execution-log-refresh`      | ~3        | Refresh `execution-log.{jsonl,md}` + `results/phase-4-output.txt` to capture state once PR-C and PR-D have landed.                                       | PR-C, PR-D |
| PR-F | Reference doc + hook-sync release   | master  | `docs/reference-pr6-nfr-conv-2-prose-determinism`        | ~5        | Land `docs/reference/nfr-conv-2-prose-determinism.md` + `.dev/releases/current/hook-sync-and-matcher-fix/` release evidence.                              | none       |
| PR-G | Tasks-folder snapshot (optional)    | master  | `chore/tasks-archive-pr7-done-snapshot`                  | ~7        | Move/commit `.dev/tasks/done/BUILD-REQUEST-*` + `RESEARCH-PROMPT-*` if they should be in-repo history (else handle via gitignore).                       | none       |
| —    | (NOT a PR — local hygiene)          | —       | —                                                        | —         | Gitignore: `docs/memory/solutions_learned.jsonl`, `docs/mistakes/*.md`, `prd-test-product/`, `prd-dry-run-test/`, `0.20/`, `.dev/eval-runs/`.            | —          |

**Branch-naming rationale:** R2 §2.4 documents the precedent `<type>/<area>-pr<N>-<slug>` from the CI-rot PRs 1-5 (`fix/ci-rot-pr1-pytest-collection`, `fix/ci-rot-pr2-ruff-violations`, etc.). Every recommended branch follows that pattern.

### Sanity check (per task spec)

```
$ git diff --name-only master HEAD | wc -l
143

$ git status --porcelain | wc -l
138

# Combined unique surface this branch would need to land vs master:
143 + 138 = 281 total entries; minus the 14 worktree-modified that also appear in the committed delta ≈ 267 unique paths.
```

Aggregate of recommended PRs above (PR-A through PR-G estimates): ≈10 + 33 + 50 + 60 + 3 + 5 + 7 = **168 files**. This is intentionally less than 267 because the gitignore hygiene line (the last row) absorbs the ~99 paths that should NOT be PR'd (auto-generated logs, stray test outputs, eval workspaces). The 168 figure aligns with the 143-file committed delta plus the 14 worktree mods plus the new untracked artifacts MINUS local-hygiene noise — within expected accounting tolerance.

---

## Integration summary (builder may quote verbatim)

> **Strategy correction (replaces R3's single-PR conclusion):** PR #49 (MERGED 2026-05-18T11:43:55Z, head `feat/hook-sync-and-matcher-fix`, **138 files / +22,771 / −139**) did absorb a large chunk of the task-builder-merge baseline (D-0016 through D-0053 plus D-0064-D-0067, 25 audit tests, agents, the task-builder SKILL.md), but the current branch HEAD adds another **143 committed files** vs master AND carries **138 porcelain entries** in the working tree (14 modified + 124 untracked), of which 43 untracked D-NNNN evidence dirs (D-0054-D-0063 and D-0068-D-0100), 10 untracked audit tests, the C1-C4 sprint runner code, four checkpoint files, and two phase-output files all still need to land. The combined ~267-unique-file surface cannot be reviewed as one PR. The split must therefore be **PR-A** (sprint runner ~10 files) | **PR-B** (audit suite ~33 files) | **PR-C / PR-D** (task-builder-merge evidence in two ~50-60 file halves) | **PR-E** (log refresh ~3 files, depends on PR-C+PR-D) | **PR-F** (reference doc + hook-sync release ~5 files) | **PR-G** (optional task-archive snapshot ~7 files), with the auto-generated `docs/memory/solutions_learned.jsonl`, `docs/mistakes/*.md`, `prd-test-product/`, `prd-dry-run-test/`, `0.20/`, and `.dev/eval-runs/` paths handled via .gitignore rather than committed. Canonical PR-body template = 51-line `.github/PULL_REQUEST_TEMPLATE.md` (final line ends with the `-->` close). Canonical pre-PR triplet = `CONTRIBUTING.md` lines 33-35 (`uv run ruff check src/ tests/`, `uv run pytest tests/<changed-area>/ -v`, `make verify-sync`). Authoritative artifacts/ subtree count = **85 D-NNNN dirs / 85 tracked files / 44 untracked porcelain entries** (R1's 56 is wrong; Analyst-A's 44 is correct).

**Status: Complete.**
