# Diff Review — `fix/prd-path-resolution-and-templates` vs `origin/master`

- **Repo:** `/config/workspace/IronClaude`
- **Branch:** `fix/prd-path-resolution-and-templates`
- **Base:** `origin/master`
- **Date:** 2026-05-20
- **Reviewer mode:** without_skill (general-purpose code review)

## Scope

Three commits on the branch:

1. `1150b41` — fix(prd): anchor PRD CLI path resolution to `.claude/`; migrate templates SoT into `src/`
2. `6a7a0dc` — fix(install,Makefile): address PR #63 review feedback (widen "nothing installed" guard, revert stray verify-deps additions, add regression test)
3. `2219545` — merge commit for PR #63

Goal of branch:

- Stop anchoring PRD-pipeline runtime path resolution to `src/superclaude/…` (which doesn't exist on pipx-installed user systems). Anchor instead to `.claude/` (project-local then user-home), with a dev fallback.
- Introduce `src/superclaude/templates/` as the source-of-truth for 15 workflow/document templates; wire sync into `make sync-dev`, `make verify-sync`, and `superclaude install` (new `install_templates.py`).
- Fix a latent installer reporting bug where `not installed and not skipped` early-returned a misleading "nothing installed" message even when every file copy failed.

## Diff Stats

```
40 files changed, 9370 insertions(+), 130 deletions(-)
```

Key buckets:

- **PRD CLI path resolution:** `src/superclaude/cli/prd/{models,config}.py` (+85 / -10)
- **Template installer:** `src/superclaude/cli/install_templates.py` (new, +156); `src/superclaude/cli/main.py` (+31); `install_{agents,commands,core}.py` (+1/-1 each — guard widening)
- **Templates SoT (new):** `src/superclaude/templates/workflow/` (8 files) + `src/superclaude/templates/documents/` (7 files), ~8.6k lines
- **Dev copy / synced:** `.claude/templates/workflow/05_prd_template.md` rewritten in place (1406-line front-mattered template replaces the prior 145-line stub, which was renamed to `.legacy-rf-project.md`)
- **Skill text references rewired:** `[.claude|src/superclaude]/skills/prd/{SKILL,refs/*}.md` — string-level replace of `src/superclaude/examples/prd_template.md` → `.claude/templates/workflow/05_prd_template.md` (8 sites across the dev copy + the SoT copy)
- **Makefile:** sync-dev now copies `src/superclaude/templates/` → `.claude/templates/`; verify-sync gains a Templates section
- **Tests:** new `tests/cli/prd/test_path_resolution.py` (+204), new `tests/cli/test_install_failures.py` (+107), small fixture-string updates in `tests/cli/prd/test_prompts.py`

I ran the two new tests locally — both pass (12/12). `make verify-sync` reports clean.

---

## Findings by Severity

### CRITICAL

_None._ The change set is contained, has regression tests, and `make verify-sync` is clean. The path-resolution refactor is correct and well-isolated.

### HIGH

#### H1 — Commit-message claim mis-cites `install_skills.py` precedent
- **Location:** `6a7a0dc` commit message body; precedent at `src/superclaude/cli/install_skills.py:114`
- **Rationale:** The commit message says "Matches the existing precedent at `install_skills.py:114`." But the actual code at `install_skills.py:114` is `if not installed and not skipped and not served_by_command: return True, "No skills to install"` — it does **not** include `and not failed`, and it returns `True` (not `False`). So the cited precedent does not actually match what the four installers now do. The widened guard is still the right behaviour, but the precedent citation is incorrect — `install_skills.py` has the same bug and was not fixed by this PR. Either the precedent claim should be removed, or `install_skills.py` should get the same widening (and a parametrized test entry).
- **Impact:** Doc/process. The fix is good; the justification text is wrong; and `install_skills.py` retains the same latent bug for any future copy-failure scenario.

#### H2 — `install_templates` reports `success=True` when zero templates exist, but caller treats `False` as fatal
- **Location:** `src/superclaude/cli/install_templates.py:97-103` and `src/superclaude/cli/main.py:204-212`
- **Rationale:** When `installed`, `skipped`, and `failed` are all empty (empty source dir), the installer returns `(False, "No templates were installed (source directory empty?)")`. `main.py` then ORs that into the fatal-exit chain (`or not templates_success`), so `superclaude install` will `sys.exit(1)` on a perfectly normal "wheel built without templates" or "user passed a custom target with nothing to copy" scenario. Compare to `install_skills.py:114-115` which returns `(True, "No skills to install")` for the analogous case. Either: (a) return `(True, "No templates available — nothing to install")` for an empty source, or (b) keep the failure and document that the wheel MUST ship templates (in which case this is correct, but it should be tested).
- **Impact:** Production install can fail loudly for an install that did everything else successfully, with a misleading "source directory empty?" message that the user has no way to act on.

### MEDIUM

#### M1 — `_default_skill_refs_dir` swaps project/home order with `_get_templates_source` — same problem, different policy
- **Location:** `src/superclaude/cli/prd/models.py:36-63` vs. `src/superclaude/cli/install_templates.py:106-128`
- **Rationale:** `_default_skill_refs_dir` resolves in order: project-local `.claude/` → user-home `~/.claude/` → dev `src/superclaude/`. `_get_templates_source` (in the *installer*) only resolves the package-relative editable/wheel paths and ignores `~/.claude/` entirely (which is fine for the installer's purpose). But the related helper `_default_template_path` *does* anchor on `.claude/`. The two helpers in `models.py` and the helper in `install_templates.py` answer fundamentally different questions ("where do I read templates at runtime" vs. "where is the source tree to install from"), but the naming and proximity invite future confusion. Add a docstring on `_get_templates_source` that explicitly says "do NOT use for runtime resolution — see models.py" and on `_default_template_path` that says "do NOT use to locate the installer source — see install_templates.py".
- **Impact:** Maintainability / future-edit risk.

#### M2 — Dev-tree fallback in `_default_*` uses `Path.cwd()` and silently masks misconfiguration
- **Location:** `src/superclaude/cli/prd/models.py:53-58` and `:74-78`
- **Rationale:** The dev fallback is `Path.cwd() / "src" / "superclaude" / ...`. If a user happens to `cd` into *any* directory containing a `src/superclaude/templates/...` (e.g., another checkout) and runs `superclaude prd run`, that unrelated checkout's templates would be used. This is unlikely to bite in practice, but the dev fallback should be anchored on `Path(__file__).resolve().parent.parent / "templates" / ...` (i.e., relative to the installed package), not on CWD. Bonus: that anchor is what `install_templates.py` uses for the same files. The current behaviour was specifically intended (the test `test_skill_refs_falls_back_to_dev_tree` asserts CWD-based dev fallback), so changing this is a behaviour change that needs its own discussion.
- **Impact:** Correctness in edge cases; cosmetic in 99% of cases.

#### M3 — `_PROTECTED_TARGET_SUBDIRS` filter is applied to *source* rel-paths, but the guarantee is about *target* writes
- **Location:** `src/superclaude/cli/install_templates.py:25-26, 65-67, 138-141, 153-156`
- **Rationale:** The docstring promises "The installer NEVER touches `~/.claude/agent-memory/`". The implementation enforces this by filtering source rel-paths whose parts include `"agent-memory"`. That works for the current source tree, but the comment near `_PROTECTED_TARGET_SUBDIRS` says the guard is "defensive — the source tree shouldn't contain these names". A stronger guard would assert against the *target* destination after resolving (`if "agent-memory" in dest.relative_to(target_path).parts: continue`), so a renamed-but-still-malicious source path that happens to symlink into agent-memory cannot escape. Low risk today since `target_path` is fixed by the caller, but worth tightening.
- **Impact:** Defence in depth.

#### M4 — `verify-sync` skip-list whitelists by *filename suffix*, not by an explicit "legacy/" subdir
- **Location:** `Makefile:297`
- **Rationale:** `case "$$rel" in *.legacy-rf-project.md) continue;; esac` whitelists exactly one filename pattern. Any future legacy/transition copies in `.claude/templates/` that follow a different convention (e.g., `*.deprecated.md`) will fail verify-sync as drift. Consider moving legacy/transitional artifacts to `.claude/templates/_legacy/**` and skipping a directory rather than chasing suffixes. Also: the current legacy file `05_prd_template.legacy-rf-project.md` exists only in `.claude/templates/` with no SoT copy, which means the SoT is intentionally incomplete relative to the dev copy — fine but unusual; consider documenting the convention in `.dev/README.md` or in the Makefile.
- **Impact:** Future-proofing.

### LOW

#### L1 — `_default_*` "miss" fallback returns home path even when home was not the chronologically newest miss
- **Location:** `src/superclaude/cli/prd/models.py:58, 78`
- **Rationale:** Comment says "the home-anchored absolute path is returned so any resulting FileNotFoundError cites an absolute path". This is correct, but it would also help to include *all three* candidates in the eventual error message via a custom exception class (or a logger.warning at resolution time), so the user knows whether to populate `<cwd>/.claude/`, `~/.claude/`, or the dev tree. Today they get a single absolute path and have to guess.
- **Impact:** Diagnostics quality.

#### L2 — `_get_templates_source` returns the missing path silently
- **Location:** `src/superclaude/cli/install_templates.py:126-128`
- **Rationale:** Same diagnostic shape as L1: if neither the editable nor the wheel layout matches, the function returns `editable` even though it doesn't exist. The caller at line 48 turns this into `False, f"Template source directory not found: {source}"`, which is fine — but the message only shows one candidate. Including both probed paths (and `Path(__file__).resolve()`) would speed up packaging-bug triage.
- **Impact:** Diagnostics quality.

#### L3 — Newly seeded PRD template (1389 lines) does not have a SoT lint/schema check
- **Location:** `src/superclaude/templates/workflow/05_prd_template.md` (entire file)
- **Rationale:** The new PRD template is the *schema* that every PRD must conform to, per `.claude/skills/prd/SKILL.md:12`. There is no automated check that this file is well-formed YAML front-matter + valid markdown structure, no anchor-link integrity check (the TOC has 28 entries), and the synthesis prompts only string-match against the filename. A minimal `tests/templates/test_prd_template_structure.py` (verify YAML front-matter parses, verify all 28 TOC anchors exist as headers) would prevent silent drift.
- **Impact:** Long-term quality of the schema.

#### L4 — `legacy-rf-project.md` is committed to `.claude/` but never to `src/`; install will not include it
- **Location:** `.claude/templates/workflow/05_prd_template.legacy-rf-project.md` (new, 145 lines)
- **Rationale:** `make sync-dev` only writes from SoT outwards, but `make verify-sync` whitelists the legacy filename, and `superclaude install` only installs from `src/`. So users who `pipx install superclaude` will not get this legacy template, while developers working in-repo will. This may be the intended behaviour ("preserve old default for in-repo PRD work but don't ship it"), but the asymmetry is worth a one-line note in the file itself or in `.dev/README.md`.
- **Impact:** Distribution clarity.

#### L5 — `install_templates` does not print a summary header before the per-file list
- **Location:** `src/superclaude/cli/install_templates.py:75-95`
- **Rationale:** Compare to `install_skills.py` where served-by-command skills get a dedicated section. The templates installer dumps one `Installed N templates:` followed by 15 paths. Fine for now but expect this list to grow. Consider grouping by `workflow/` vs `documents/` subdir for readability.
- **Impact:** UX polish.

### NIT

#### N1 — Emoji prefixes are inconsistent across installer outputs
- **Location:** `src/superclaude/cli/install_templates.py:77, 87, 93, 100`
- **Rationale:** Templates installer uses `✅ ⚠️ ❌ 📁`, matching the existing installers. Fine and intentional, just noting it's locked into the existing convention — any future "monochrome / CI-friendly" toggle will need to handle all five installers together.

#### N2 — `_PRD_REFS_REL` / `_PRD_TEMPLATE_REL` are module-private but their values are duplicated as string literals in tests
- **Location:** `src/superclaude/cli/prd/models.py:31-32` vs. `tests/cli/prd/test_path_resolution.py:42, 50`
- **Rationale:** Tests hard-code `.claude/skills/prd/refs` and `.claude/templates/workflow/05_prd_template.md` as string literals. If the constants ever change, tests will silently still build the OLD paths and only catch the bug if the *new* paths happen not to resolve. Minor; an `import _PRD_REFS_REL` in the tests would tighten the coupling.

#### N3 — Renaming `examples/prd_template.md` → `templates/workflow/05_prd_template.md` may have stale upstream string refs
- **Location:** Cross-cutting; checked via the diff stats above
- **Rationale:** The diff rewires 8 references inside `skills/prd/`, but other places in the codebase (KNOWLEDGE.md, docs/, archived MDTM tasks under `.dev/`) may still cite `src/superclaude/examples/prd_template.md`. A quick `rg "examples/prd_template.md" -g '!*.lock'` after merge would catch any stragglers. The PR commit message acknowledges the `git mv` but I did not see grep evidence in the diff that other dirs were swept.
- **Impact:** Doc consistency.

---

## Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High     | 2 |
| Medium   | 4 |
| Low      | 5 |
| Nit      | 3 |
| **Total**| **14** |

### Top three action items

1. **H2** — Decide whether an empty `templates/` source should be a fatal install failure or a no-op success; today it kills `superclaude install` with a misleading message even when every other step succeeded.
2. **H1** — Fix the commit-message claim (or extend the fix to `install_skills.py:114` and add a 5th parametrized test entry). The cited precedent does not actually match the new code.
3. **M2** — Re-anchor the `models.py` dev fallback on `Path(__file__)` instead of `Path.cwd()` so it matches `install_templates.py` and stops being CWD-dependent.

### What this PR gets right

- Clean separation: runtime resolution helpers in `models.py`, installer source resolution in `install_templates.py`, both with explicit ordered candidate lists.
- Strong regression tests for the actual production bug (`FileNotFoundError` on CWD-relative resolution) and for the installer-message bug (PR review #63 r3275576561) — 12/12 pass locally.
- `make verify-sync` correctly extended, runs clean, distinguishes "missing in SoT" vs "missing in dev copy" vs "differs".
- Commit `6a7a0dc` shows healthy review-driven follow-through (reverts a stray verify-deps tendril that didn't belong to this PR's scope).
- Templates SoT migration is single-commit, atomic, with a corresponding `git mv` of the prior PRD template — git history preserved.
