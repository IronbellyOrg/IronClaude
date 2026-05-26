# Stash Recovery — `src/superclaude/cli/prd/{executor,prompts}.py`

Read-only inspection of `stash@{0}` (`7185ed32` "pre-existing dirty state (262 files) — park for Fix B rebase") against `HEAD` on `fix/integration-contracts-mechanism-signature`.

## A. Per-file summary

### `src/superclaude/cli/prd/executor.py`
The `PrdExecutor` class — the v4.2 PRD CLI pipeline driver (Stage B orchestration: `investigation → research-qa → web-research → synthesis → synthesis-qa → assembly → structural-qa → qualitative-qa`, see `executor.py:727-754` HEAD). Last committed on master as part of `27962ddb` "fix(prd): unblock PRD CLI pipeline end-to-end on greenfield repos (#71)" 3 days ago. Stash diff is **9 net +/- lines, all whitespace**: (a) line-broken stage list at L727-735 expanded to one-element-per-line; (b) three `have_*` `any(...)` generators at L741-754 collapsed from 2-line bodies to 1-line bodies. Zero behavior change — `git diff stash^ stash -- executor.py --stat` reports `20 lines changed`, AST-diff against HEAD is **empty** (verified via `ast.dump`).

### `src/superclaude/cli/prd/prompts.py`
Prompt-builder module for the PRD pipeline — houses `build_task_file_prompt`, `_parse_agent_block`, the three `_derive_*_render_kwargs` helpers, `_dual_mode_call` legacy shim, and the public `build_{investigation,web_research,synthesis}_prompt` entrypoints (HEAD `prompts.py:375-1000`). Last committed on master in the same `27962ddb` (PR #71) 3 days ago. Stash diff is **20 net +/- lines, all whitespace**: collapsed `existing_task_file = (…)` parens at L375-378, joined two split f-strings at L584/L657/L685, expanded 3 multi-line literal sets at L607/L612, and reformatted `*args, kwargs,` call lines into separate-argument form at L803/L987. AST-diff against HEAD is **empty**.

### Combined ground-truth check
`ruff format --check src/superclaude/cli/prd/{executor,prompts}.py` on HEAD reports `2 files would be reformatted`. Running `ruff format` on a copy of HEAD produces a file **byte-identical** to the stash version (verified via `diff -q`, both files). The stash content **IS** `ruff format`(HEAD).

## B. The originating workstream

These two files are **collateral** in the parked dirty state, not part of any open PRD workstream. Evidence:

- The completed PRD remediation task `TASK-RF-20260521133223` (.dev/tasks/to-do/TASK-RF-20260521133223/TASK-RF-20260521133223.md:5, status: `🟢 Done`) landed as PR #71 (`27962ddb`) on 2026-05-22. All planned `executor.py`/`prompts.py` edits from PR #71's remediation spec are already in HEAD.
- Recent lint sweep PRs `#83` (`38ca920d` "Issue #60 — eliminate pre-existing ruff debt (441 → 0)"), `1d0c89dc`, `d9097acc` did not touch the two prd files — confirmed via `git show --stat 38ca920d -- src/superclaude/cli/prd/executor.py` (empty).
- Grep of `.dev/tasks/{to-do,done}/` and `.dev/releases/` for `prd/executor` or `prd/prompts` returns **no open task referencing these formatting changes**.
- The stash parent chain (`stash@{0}^^` = `505975ed` "fix(roadmap): mechanism-signature refactor for anti-instinct integration_contracts") shows the dirty state was carried alongside the Fix B integration-contracts work, not PRD work.

**Verdict on origin:** stray `ruff format` output, almost certainly produced by a prior session's quality sweep (or an editor format-on-save), that was never committed because the prd files weren't in scope of Issue #60 PR #83 or any landed PR.

## C. Verdict — **DROP (do not preserve in current Fix B branch)**

Rationale:
1. **Zero functional content** — AST-equivalent to HEAD; preserving adds nothing to the Fix B mechanism-signature work.
2. **Out of scope** — Fix B is `fix/integration-contracts-mechanism-signature`; whitespace churn in PRD files muddies the diff and review.
3. **Already-known-pending lint debt** — `ruff format --check` failure is a real (non-blocking) finding but belongs in its own follow-up PR, not buried in Fix B.
4. **No upstream PR is waiting on this** — `gh pr list` semantics aside, the file's last touch is PR #71 (merged) and no open task lists these files.

## D. Recommended recovery (post Fix-B merge)

If/when the team wants to land the formatting separately, the trivial recovery is **regenerate, don't unstash**:

```bash
# AFTER Fix B is merged to master, on a fresh branch:
git checkout master && git pull
git checkout -b chore/ruff-format-prd-cli
uv run ruff format src/superclaude/cli/prd/executor.py src/superclaude/cli/prd/prompts.py
git add src/superclaude/cli/prd/executor.py src/superclaude/cli/prd/prompts.py
git commit -m "chore(prd): ruff format executor.py + prompts.py (Issue #60 follow-up)"
```

This is **safer than `git checkout stash@{0} -- <files>`** because it (a) avoids dragging in any unrelated 260-file stash content, (b) is reproducible from HEAD + ruff version, and (c) requires no inspection of the stash blob.

**Do NOT** `git stash pop` or `git stash apply` — the stash holds 262 files (`4089 insertions(+), 1714 deletions(-)`) and applying it would contaminate Fix B with unrelated drift across `.claude/agents/`, `.claude/commands/`, `tests/sprint/`, etc.

The stash can be dropped after Fix B merges; the PRD files specifically are recoverable on demand via one `ruff format` invocation.
