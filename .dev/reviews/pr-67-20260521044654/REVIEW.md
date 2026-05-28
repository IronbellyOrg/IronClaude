# Code Review: PR #67 — chore: archive working-tree backlog

**Target**: [PR #67](https://github.com/IronbellyOrg/IronClaude/pull/67)
**Reviewer**: `/sc:auggie-review` (depth=standard, focus=default, --remediation-offer)
**Generated**: 2026-05-21 04:46 UTC
**Base ↔ Head**: `master` ↔ `chore/working-tree-archive-2026-05-21` (HEAD `77a5d006`)
**Stats**: 361 files in merge-base diff, 54,329 lines; **but only 1 unique commit (`77a5d006`) on this branch, modifying 0 non-`.dev/` files**

---

## Summary

**Recommendation: Approve with comments.** The single new commit (`77a5d006`) is a clean archival commit landing untracked `.dev/` artifacts — exactly what the PR title and body advertise. The PR has zero critical or high findings.

However, the **PR diff is misleading**: it shows ~13k lines of apparent code changes because the branch's merge base is behind master. Those lines all come from PRs #62, #63, and #64, which have already landed on master. A reviewer scanning the GitHub diff will see code surface area that doesn't actually exist in this PR's contribution. This is the headline observation; the four narrow code-related findings below are all about already-merged code and are retained only as low-priority informational items.

---

## Findings

### 🟡 Medium — Fix in this PR if cheap, otherwise file follow-up

#### M1. PR diff misleads reviewers due to stale merge base

- **Files**: PR-level (no single line); see `inputs/files-full.txt` in the review output dir
- **Category**: process / api-contract (PR hygiene)
- **Source**: orchestrator (cross-cutting, derived from chunk inspection)
- **Evidence**:
  ```
  $ git rev-list master..77a5d00626eabb3e254dc90a5729bc931068af09
  77a5d00626eabb3e254dc90a5729bc931068af09
  ffa35fc57986f840a27d1490863b5af2fbc2ff44   # PR #64 (already merged)
  2219545cc6cb5d3cfbd9e8f1d1c078b74adaa3a3   # PR #63 (already merged)
  f333cdf107405939cec92247b527012314f6d3fe   # PR #62 (already merged)

  $ git show --name-only 77a5d006 | grep -Ev '^\.dev/' | wc -l
  0
  ```
- **Why this matters**: A reviewer reading the GitHub UI will see 361 changed files including 18 `.py` files, `Makefile`, `.claude/settings.json`, `CLAUDE.md`, and 38 files under `src/superclaude/`. They may reasonably assume those represent new work and either over-review (wasting cycles) or under-review (because they trust the "archive only" PR body and skip the code). Both modes are unsafe. The real new content is **only** the `.dev/` archive in commit `77a5d006`.
- **Recommendation**: Either (a) rebase the PR onto current `master` so the diff only shows the new commit (cleanest), or (b) add an explicit note at the top of the PR body explaining the merge-base drift and citing the actual new file count (e.g., `git diff master..HEAD --stat -- ':!.dev/' | wc -l == 0`). The "Pure archive — no production code, no behavior change" claim is **accurate for the new commit** but **contradicted by the GitHub diff view** without this clarification.

---

### 🟢 Low — Nice-to-have

The two findings below are real but **pre-existing in code that this PR does not modify**. They are surfaced for awareness only — the PR-scope adjustment in the severity rubric (step 4) downgrades them from Medium to Low because the diff doesn't touch the cited functions' hunks.

#### L1. `update` command docstring contradicts implementation (skips hooks + templates)

- **File**: `src/superclaude/cli/main.py:266-310`
- **Category**: correctness (docs vs impl drift)
- **Source**: auggie chunk A (F8)
- **Evidence** (from `src/superclaude/cli/main.py:266-280`):
  ```python
  def update(target: str):
      """
      Update SuperClaude to latest version

      Re-installs core framework files and slash commands to match
      the current package version. Equivalent to 'install --force'.
      ...
      """
      from .install_agents import install_agents
      from .install_commands import install_commands
      from .install_core import install_core_files
      from .install_skills import install_all_skills
  ```
  The `install` command (line 46) imports and runs `install_core_files`, `install_commands`, `install_agents`, `install_hooks` (L191), `install_templates` (L201), and `install_all_skills`. The `update` command imports and runs only core, commands, agents, and skills — **`install_hooks` and `install_templates` are missing**.
- **Why this matters**: Users following the docstring will run `superclaude update` expecting full equivalence with `install --force`, but their hooks (e.g. freshness hooks, `offer-pr-review.sh`) and templates (workflow/document templates) will not be refreshed. Behavior diverges silently from documentation.
- **Recommendation**: Either (a) extend `update` to also call `install_hooks(force=True)` and `install_templates(force=True)`, or (b) amend the docstring to read "Re-installs core files, commands, agents, and skills (does not refresh hooks or templates — use `install --force` for a full reinstall)." Option (a) better matches the stated intent.
- **Note**: Not in this PR's hunks; this finding originates from a roll-up of an earlier PR.

#### L2. `_check_task_phases_present` accepts duplicate or non-sequential phase numbers

- **File**: `src/superclaude/cli/prd/gates.py:154-160`
- **Category**: quality / correctness (weak validation)
- **Source**: auggie chunk A (F5)
- **Evidence**:
  ```python
  def _check_task_phases_present(content: str) -> bool | str:
      """Check that the task file contains phase definitions.
      Expects headings like 'Phase 1:', 'Phase 2:', etc.
      """
      phase_headings = re.findall(
          r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+\d", content, re.IGNORECASE
      )
      if len(phase_headings) < 2:
          return f"Expected multiple phase headings, found {len(phase_headings)}"
      return True
  ```
- **Why this matters**: The gate checks only that ≥ 2 matches of `Phase \d` exist. A document with "Phase 1" twice and no other phase would pass; so would "Phase 7" and "Phase 7". For the PRD gates workflow this is a low-impact correctness gap (the next gate likely catches malformed content) but the docstring suggests strictness the regex doesn't enforce.
- **Recommendation**: Extract the digit groups, deduplicate, and require that distinct phase numbers are observed (e.g. `len(set(re.findall(r"Phase\s+(\d)", content, re.IGNORECASE))) >= 2`). Or tighten the docstring to "Expects at least two `Phase N` heading lines (numbers not required to be sequential or unique)".
- **Note**: Not in this PR's hunks; pre-existing from PR #63.

---

### 💬 Nits

- `src/superclaude/templates/workflow/99_mdtm_template_generic_task_old.md` — legacy template retained alongside `01_mdtm_template_generic_task.md`. The `99_` prefix communicates archival intent, but a one-line header pointing readers at the current canonical file would prevent accidental use.
- `.claude/templates/workflow/05_prd_template.legacy-rf-project.md` — explicitly whitelisted in `Makefile:297` (`case "$$rel" in *.legacy-rf-project.md) continue;;`), confirming the legacy-retention pattern is deliberate. Documenting the convention in `CONTRIBUTING.md` would prevent confusion for new contributors.

---

## Architectural / Cross-Cutting Observations

### O1. The PR's `--no-verify` rationale is sound but should not become a habit

The PR body notes that `--no-verify` was used "due to the same three pre-commit infrastructure gaps documented in PR #65 and PR #66." This is reasonable for an archive-only commit, but the cited infrastructure gaps now appear across **at least three PRs** (#65, #66, #67). That's an architectural debt signal — the pre-commit hooks have failure modes that legitimate commits routinely need to bypass, which dilutes their value as a quality gate. Worth a follow-up task to fix the underlying pre-commit issues so future commits don't need `--no-verify`.

(This observation is process-level, not a finding against the PR itself.)

---

## Audit

- **Auggie chunks**: 3 (A=Python source/tests, B=skills/templates, C=config)
  - A: 10 findings + 3 cross-cutting — **9 dropped on validation, 2 kept (Low)**
  - B: 8 findings + 3 cross-cutting — **9 dropped on validation, 2 kept (Nit)**
  - C: 5 findings + 5 cross-cutting — **all dropped on validation; surfaced as informational**
- **Total findings dropped during grounding**: 18 (out of 23 + 9 = 32 raw)
- **Drop reasons**: (a) cited code is correct on close reading (e.g. `printf '%s' "$INPUT"` IS quoted; `_slugify` regex IS correct); (b) finding contradicts repo state (e.g. tests/cli/test_install_hooks.py already exists; `make verify-sync` passes); (c) speculative without concrete vector (e.g. "potential prompt injection" with no actual sink).
- **PR-scope downgrades**: 2 findings downgraded from Medium → Low because cited code is pre-existing and not in the new commit's hunks.
- **Meta-finding (M1)**: not from Auggie — emerged from orchestrator's inspection of the actual new commit vs. the merge-base diff. Strongly grounded in `git rev-list` / `git show` output.
- **Persona cross-check**: not enabled (depth=standard).
- **`make verify-sync`**: PASSES at HEAD (no actual drift between `src/superclaude/` and `.claude/`).

```
<!-- SC:AUGGIE-REVIEW:SUMMARY
status: success
critical: 0 high: 0 medium: 1 low: 2 nit: 2
dropped: 18
auggie_chunks: 3
duration_sec: ~1400
-->
```
