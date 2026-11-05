# Documentation Context Card

## Release context
No release slug. Controlling artifact: design package TASK-WF-design-20261104-164423. The design has no trust model: no "untrusted", "security", "credential" or "build backend" wording; Tier 1 is the default (source.md:602, :1139); the risk table (:1473-1483) has no row for PR-controlled PEP 517 backends; OQ-31 (:1169) treats the tracked pyproject.toml as safe; uv.lock is gitignored in this repo (INV-033, :119), so the gap never shows locally (wave1_5-branch-A.md).

## Architectural docs consulted
- refs/conflict-mechanical.md:46-52 (Tier 3 template), :82-94 (step 5), :126-133 (VAL), :216-223 (abort), :296 (`sync_tier3` row) (CAUTION: currency unknown)
- SKILL.md:219, :311-320 (Will Not Do), :329-330 (CAUTION: currency unknown)
- commands/pr-submit.md:28-30, :54 (CAUTION: currency unknown)
- SECURITY.md:467 "Use safe defaults and explicit opt-in for risky functionality" (CAUTION: currency unknown)

## Restrictions / decisions that constrain the fix
- Owner decision (coordinator answer, audit.log header): keep default tier 1; halt at Tier 3 before `uv lock` naming the field for build-system.backend-path, non-empty project.dynamic, path/editable [tool.uv.sources]; a test per trigger plus a clean test; document the trust limit in the refs and the command doc.
- conflicts.py is stdlib-only and pure (docstring :11-21); the import allowlist test pins {base64, re, dataclasses, typing} (test_conflicts_core.py:2445-2468); `open`/`__import__` banned (:2473). A tomllib parse inside conflicts.py needs the allowlist and docstring extended; the Python floor is 3.10 (pyproject.toml:16), so the import must be guarded and a missing parser must halt.
- No new EventType (43 pinned, test_run_log.py:174-175); reuse `sync_tier3` (HALT_REASONS conflicts.py:145-165).
- Step 5 pins stay verbatim (test_conflict_sync_protocol.py:70-72); fenced commands start with git/gh/uv/make/jq or scripts/ (:40, :514-538); exactly one `git checkout` across the new files (:488-494).

## Re-frame signals
- The defect is a missing trust gate, not a wrong command: `uv lock` is the right regeneration, but its input (the merged pyproject.toml) can name code to execute.
- VAL (`uv run pytest`, `make test`) also runs PR code on the merged tree; that part stays a documented trust limit, per the owner.
