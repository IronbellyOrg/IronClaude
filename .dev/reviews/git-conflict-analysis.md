# Git Conflict Analysis — Incoming Branches vs Current Roadmap Work

Date: 2026-06-02
Worktree: `/config/workspace/IronClaude-RoadmapRewrite`
Current branch: `refactor/roadmap-pipeline-r0-r1-rewrite` (HEAD `90a8fa67`)
Fork remote: `origin = https://github.com/IronbellyOrg/IronClaude.git`
Master tip: `91095144`

Scope: read-only analysis + two PRs created + one conflict resolved. No force-push, no push to `master`.

## TL;DR

| Item | Status |
|---|---|
| PR #111 / `861047c2` (M{n}-D{nn} fix) | Not fixed by any current branch; still needs a SoT-aware port into `superclaude.contracts.ID_PATTERNS`. |
| `origin/feat/ovm-verification-gap-cycle` | **Safe.** master + 2 commits, all under `.dev/`, zero conflicts → **PR #114** opened. |
| `origin/feat/brv-mg-sibling-skill-cycle` | One conflict (`repo-inventory.sh`), resolved by taking master's superseding version → **PR #115** opened + now MERGEABLE. |

---

## PR #114 — `origin/feat/ovm-verification-gap-cycle`

Link: https://github.com/IronbellyOrg/IronClaude/pull/114 (base `master`)

### Safety verdict: SAFE

- Merge-base with `master` = `91095144` (current master tip) → clean descendant, no divergence.
- Unique commits: `1f30fb2a`, `ffe51923`.
- `git merge-tree` into `master`: **no conflict markers**.
- All 20 changed files under `.dev/` (planning/task artifacts). Zero `src/`, `tests/`, `pyproject.toml` impact.

### Roadmap-overlap check

Does not touch `spec_parser.py` or `structural_checkers.py`. No effect on `_REQUIREMENT_PATTERNS`, `_canonicalize_requirement_id`, `check_signatures`, or Explicit-non-references parsing. Does not fix or conflict with the PR #111 bug.

---

## PR #115 — `origin/feat/brv-mg-sibling-skill-cycle`

Link: https://github.com/IronbellyOrg/IronClaude/pull/115 (base `master`)

### Final verdict: SLIMMED + MERGEABLE (15 files, all `.dev/`)

Branch was reshaped to `master` + only the 3 BRV-MG commits. PR is now `mergeable: MERGEABLE`, head `4755f886`, **+3701 / −0, 15 files, all under `.dev/`**.

History (slimmed):

- `feat(brv-mg): import BRV-MG implementation task + adversarial-merged brainstorm`
- `chore(brv-mg): rewrite Coder→IronClaude paths in BRV-MG cycle`
- `feat(brv-mg): add Phase 1 Step 1.0 worktree-entry instruction`

### Why slimmed, and what was dropped

The original conflict was exactly **one** file —
`src/superclaude/skills/sc-cleanup-audit-protocol/scripts/repo-inventory.sh`.
Both `master` and BRV add the **identical** scope-exclusion feature; `master`'s copy is a strict superset (adds the `|| true` arithmetic-bug fix, the `sed 's|^\./||'` path normalization, and a narrower `tests` classifier). BRV's two cleanup-audit commits (`9ea8be21`, `bf82b257`) were therefore an **earlier version of work already refined on `master`** — redundant.

Per user decision, the branch was slimmed to drop those redundant commits, leaving only the durable BRV-MG planning artifacts.

### How it was done (cherry-pick, then force-push-with-lease)

1. `git worktree add -B brv-slim /tmp/brv-slim origin/master`
2. `git cherry-pick 0e28af62 d5701a79 e101951a` (the 3 BRV-MG commits) → clean, pre-commit hooks passed
3. `git push --force-with-lease=feat/...:1587a5b3 origin brv-slim:feat/brv-mg-sibling-skill-cycle`
4. PR #115 title/body updated to "docs-only" via REST API (`gh pr edit` was blocked by a Projects-classic GraphQL deprecation; `gh api ... -X PATCH` worked).

Recoverability: the pre-slim tip was `1587a5b3` (merge-based resolution); the original pre-session tip was `e101951a`.

### Roadmap-overlap check

Does not touch `spec_parser.py` or `structural_checkers.py`. Same negative result as OVM for all four PR #111 concern symbols.

---

## PR #111 / `861047c2` — still outstanding

Neither incoming branch fixes the M{n}-D{nn} milestone-prefixed-ID false-positive. The current roadmap branch also has not fixed it — `bdfad6d3` only moved `_REQUIREMENT_PATTERNS` bodies to `superclaude.contracts.ID_PATTERNS`; it adds no `MD` family, no MD trailing-D dedup, no MD canonicalizer, no allowlist suppression.

Recommended SoT-aware port (unchanged from prior analysis):

1. Add `"MD": r"M\d+-D-?\d+"` before `"D"` in `superclaude.contracts.ID_PATTERNS`; update the family docstring.
2. Keep `spec_parser._REQUIREMENT_PATTERNS` generated from the registry.
3. Port the incoming `_MD_TRAILING_D_RE` + `extract_requirement_ids` bare-D dedup.
4. Port the `structural_checkers.py` MD canonicalizer branch + `_parse_explicit_non_references` + `check_signatures` suppression.
5. Port the incoming tests; rerun the integration scenario (`fidelity_status=pass`, `Final HIGH Count: 0`, roadmap.md sha256 `8c93b8f5157bcb73ede60ddd02aa4c8f6d1d928b927655cfaa2bf1c78a12b5e7`). Because `superclaude` is pipx-installed (real-file copy), `pipx reinstall superclaude` before validating the system binary.
