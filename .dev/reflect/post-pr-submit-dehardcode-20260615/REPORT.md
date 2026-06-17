# sc:reflect — UC-2 Post-Execution Deviation Audit

- **mode:** post · **tier_reached:** 2 (forced via `--depth deep`)
- **target:** commit `39dd05ab` "fix(pr-submit): de-hardcode target repo, base branch, and paths to run on any repo"
- **diff:** HEAD~1..HEAD (16 files, +308/−144) · **input_tree_sha256:** cc2879dd…
- **reviewers:** 3 heterogeneous (quality-engineer/sonnet, refactoring-expert/haiku, root-cause-analyst/opus) + adversarial merge
- **evidence-validator:** ran; citations_total≈7, citations_dropped=0 (all re-Read against current state)
- **status:** success · **calibrated confidence:** 0.90 · **convergence:** ~0.82 (PASS)
- **deviation_count_by_class:** authorized 0 · necessary 0 · **drift 3** · **regression 0**

## Verdict

The commit **substantially and correctly satisfies** the spec. Core de-hardcoding is complete and the
safety-critical PR-URL misroute property is genuinely hardened, not merely relabeled. Three **non-blocking
Drift** items (quality improvements) were found; **no Regression**. No item breaks shipped behavior — the
current sources contain no live defect.

## What the audit CONFIRMED (grounded)

- **No surviving pins** — zero `IronbellyOrg`/`IronClaude`/`/config/workspace`/literal-`master`-default in
  src OR the `.claude` mirror (test slugs are parametrized alongside `acme/widgets` = de-hardcoding proof, not pins).
- **DO-NOT-TOUCH preserved** — `augment_bot_login`/`augment_author_association`/`augment_app_slug` and the
  `augment|auggie|augmentcode` trigger regexes are byte-unchanged (detection.py / classifier.py).
- **No scope creep** — all 16 files map to the GOAL scope; the unscoped core files (models/classifier/
  severity_router/loop_guard/recovery) were already generic and correctly left alone.
- **SP2 (misroute HALT) hardened** — `pr_target_ok(pr_url, target_repo)` at `fsm.py:471-473` uses a
  `/{target_repo}/` boundary; misroute→False and prefix-collision (`acme/widgets` vs `acme/widgets-fork`)→False,
  both empirically tested (`test_pre_pr_checks.py:94-104`). The gh-default-to-upstream-parent trap is caught generically.
- **NFR-6 core purity preserved** — `grep \bgh\b|\bgit\b` over all 7 core-pure files → 0 hits; the new
  docstrings are token-clean; `test_tn50` was strengthened (auggie-fallback.md added to the set), not weakened.
- **Gates green** — `uv run pytest tests/pr_submit -q` → 187 passed; ruff check/format clean; verify-sync clean.

## Deviation register (3 × Drift, all non-blocking)

### D1 — `origin_ok` substring match lacks the `/owner/repo/` boundary  (Drift · low · pre-existing root · unreachable)
- **Where:** `src/superclaude/pr_submit/fsm.py:486` — `return bool(origin_url) and bool(target_repo) and target_repo in origin_url`
- **Evidence:** `origin_ok("https://github.com/acme/widgets-upstream.git", "acme/widgets") → True` (false pass).
- **Why non-blocking:** (a) **pre-existing** — `39dd05ab~1` had the identical bare substring (`PR_TARGET_REPO in origin_url`); this commit neither introduced nor worsened it. (b) **unreachable** — `target_repo` is RESOLVED FROM origin in every path (no operator `--repo` override exists), so `origin_url` and `target_repo` tautologically agree.
- **Asymmetry note:** the commit added a boundary guard to `pr_target_ok` but left `origin_ok` bare — worth making symmetric for defense-in-depth.

### D2 — `$REPO` sed fallback mishandles URL-style SSH remotes  (Drift · medium · NEW · fallback-path only)
- **Where:** the resolution line in all three scripts, e.g. `scripts/poll-augment-review.sh:42` —
  `sed -E 's#^git@[^:]+:##; s#^https?://[^/]+/##; s#\.git$##'`
- **Evidence:** `ssh://git@github.com/acme/widgets.git` → `ssh://git@github.com/acme/widgets` (malformed, non-empty → bypasses the `[ -n "$REPO" ] || die` guard). In reply-resolve-thread.sh this yields graphql `owner="ssh:"`.
- **Why bounded:** only fires on the **fallback** (when `gh repo view --json nameWithOwner` fails); scp-style SSH and HTTPS are handled correctly. URL-style SSH (`ssh://…`) is the uncovered shape.

### D3 — `_repo_scoped` static-grep net is substring-permissive  (Drift · medium · NEW · no live escape)
- **Where:** `tests/pr_submit/test_static_grep.py:108-113` — unanchored `"--repo" in line or "repos/" in line or "graphql" in line`.
- **Evidence (constructed bypasses that pass the matcher):** `gh pr create --base x --head y  # see repos/docs` (bare gh defused by a trailing-comment `repos/`); `gh pr create --reposcope foo` (`--repo` as substring of `--reposcope`); `gh pr merge 42  # graphql`.
- **Why non-blocking:** every REAL `gh` line in the current skill sources is legitimately scoped (`--repo "$REPO"` / `repos/${REPO}/`), so **no defect escaped**. This is a catch-strength regression vs the prior literal-slug gate, not a live functional one.

## Informational (not deviations, pre-existing / by-design)
- **SP1 (no-push-to-default-branch)** has no executable guard in the deterministic core — it is prose-only in SKILL.md (`never push to the default/protected branch`). This is **pre-existing** (`39dd05ab~1` was identical) and is a consequence of the NFR-6 "core records, SKILL acts" split. The de-literalization `master → default/protected branch` correctly genericized the prose. The commit message's "Safety preserved generically" is accurate but slightly over-implies a mechanism stronger than prose for SP1.
- `SkillArgs.base` defaults to `None` (the SKILL supplies the repo default at runtime via `defaultBranchRef`); a Python-only consumer of `parse_args` gets `None`. Documentation-level only; matches the pre-commit posture (docstring default, not enforced).

## Recommended (optional) hardening
1. **D1+D2 together** (~5 lines, both in already-touched files): give `origin_ok` the same `/owner/repo/` boundary as `pr_target_ok`, and extend the sed to strip `ssh://[^/]+/` so URL-style SSH resolves. Add an `origin_ok` substring-collision test row + an `ssh://` fixture.
2. **D3:** tighten `_repo_scoped` to test the gh argv (whole-token `--repo`, strip trailing `#` comments, require `repos/`/`graphql` after a `gh api` token).

All three are quality improvements; none blocks the merge. The shipped commit is correct and test-green.
